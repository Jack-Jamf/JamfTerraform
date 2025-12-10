"""HCL generator for Jamf Pro resources."""
from typing import Dict, Any, Optional, TYPE_CHECKING
from collections import defaultdict
import json
import os

# Provider version for exports (configurable via environment variable)
PROVIDER_VERSION = os.getenv('JAMFPRO_PROVIDER_VERSION', '~> 0.19.0')

if TYPE_CHECKING:
    from support_file_handler import SupportFileHandler


class HCLGenerator:
    """Generates Terraform HCL from Jamf Pro resource data."""
    
    # Enum mappings: Jamf API values → Terraform Provider values
    REBOOT_OPTIONS_MAP = {
        "Restart immediately": "Restart Immediately",
        "Do not restart": "Do not restart",
        "Restart if a package or update requires it": "Restart if a package or update requires it"
    }
    
    SCRIPT_PRIORITY_MAP = {
        "Before": "BEFORE",
        "After": "AFTER",
        "At Reboot": "AT_REBOOT"
    }
    
    def __init__(self, support_file_handler: Optional['SupportFileHandler'] = None):
        """
        Initialize the HCL generator.
        
        Args:
            support_file_handler: Optional handler for file references. When provided,
                                  scripts and profiles will use file() references.
        """
        self.used_names = defaultdict(set)
        self.support_file_handler = support_file_handler
        self.templates = {
            'policies': self._generate_policy_hcl,
            'scripts': self._generate_script_hcl,
            'packages': self._generate_package_hcl,
            'categories': self._generate_category_hcl,
            'buildings': self._generate_building_hcl,
            'config-profiles': self._generate_config_profile_hcl,
            'smart-groups': self._generate_computer_group_hcl,
            'static-groups': self._generate_computer_group_hcl,
            'computer_groups': self._generate_computer_group_hcl,
            'jamf-app-catalog': self._generate_app_catalog_hcl,
            'extension-attributes': self._generate_extension_attribute_hcl,
            'advanced-computer-searches': self._generate_advanced_computer_search_hcl,
            'departments': self._generate_department_hcl,
            'network-segments': self._generate_network_segment_hcl,
            'printers': self._generate_printer_hcl,
            'sites': self._generate_site_hcl,
            'mobile-device-groups': self._generate_mobile_device_group_hcl,
            'mobile-device-prestages': self._generate_mobile_device_prestage_hcl,
            'mobile-device-config-profiles': self._generate_mobile_device_configuration_profile_hcl,
            'advanced-mobile-device-searches': self._generate_advanced_mobile_device_search_hcl,
            'mobile-device-extension-attributes': self._generate_mobile_device_extension_attribute_hcl,
        }
    
    def generate_resource_hcl(self, resource_type: str, resource_data: dict, resource_name: Optional[str] = None) -> str:
        """
        Generate HCL for a single resource.
        
        Args:
            resource_type: Type of resource
            resource_data: Full resource data from Jamf API
            resource_name: Optional Terraform resource name (defaults to sanitized name)
            
        Returns:
            HCL string for the resource
        """
        if resource_type not in self.templates:
            return f"# Unsupported resource type: {resource_type}\n"
        
        generator_func = self.templates[resource_type]
        return generator_func(resource_data, resource_name)



    def _generate_app_catalog_hcl(self, app_data: dict, resource_name: Optional[str] = None) -> str:
        """
        Generate HCL for a Jamf App Catalog app (App Installer).
        """
        name = app_data.get('name', 'Unnamed App')
        tf_name = resource_name or self._get_unique_tf_name(name, 'jamfpro_app_installer')
        app_details = app_data.get('app', {})
        bundle_id = app_details.get('bundleId', '')
        version = app_details.get('latestVersion', '')
        
        hcl = [f'# Jamf App Catalog: {name}']
        if bundle_id:
            hcl.append(f'# Bundle ID: {bundle_id}')
        if version:
            hcl.append(f'# Version: {version}')
        
        hcl.append(f'resource "jamfpro_app_installer" "{tf_name}" {{')
        hcl.append(f'  name            = "{name}"')
        hcl.append(f'  enabled         = {str(app_data.get("enabled", True)).lower()}')
        hcl.append(f'  deployment_type = "{app_data.get("deploymentType", "SELF_SERVICE")}"')
        hcl.append(f'  update_behavior = "{app_data.get("updateBehavior", "AUTOMATIC")}"')
        
        # Category (required, -1 if not set)
        category_id = app_data.get('category', {}).get('id', -1)
        hcl.append(f'  category_id     = "{category_id}"')
        
        # Site (required, -1 if not set)
        site_id = app_data.get('site', {}).get('id', -1)
        hcl.append(f'  site_id         = "{site_id}"')
        
        # Smart group (required, default to 1 = All Managed Clients)
        smart_group = app_data.get('smartGroup', {})
        smart_group_id = smart_group.get('id', 1)
        if smart_group_id and smart_group.get('name'):
            sg_name = self._sanitize_name(smart_group['name'])
            hcl.append(f'  smart_group_id  = jamfpro_smart_computer_group.{sg_name}.id')
        else:
            hcl.append(f'  smart_group_id  = "{smart_group_id}"')
        
        hcl.append('}')
        
        return '\n'.join(hcl)
    
    def generate_file(self, resources_sorted: list) -> str:
        """
        Generate complete .tf file with all resources in dependency order.
        
        Args:
            resources_sorted: List of (resource_type, resource_data) tuples
            
        Returns:
            Complete HCL file content
        """
        hcl_blocks = []
        hcl_blocks.append("# Generated by JamfTerraform Proporter\n")
        hcl_blocks.append("# Contains Jamf Pro resources exported from your instance\n\n")
        
        for resource_type, resource_data in resources_sorted:
            hcl = self.generate_resource_hcl(resource_type, resource_data)
            hcl_blocks.append(hcl)
            hcl_blocks.append("\n")
        
        return "\n".join(hcl_blocks)
    
    def _sanitize_name(self, name: str) -> str:
        """Convert resource name to valid Terraform identifier."""
        # Replace spaces and special chars with underscores
        sanitized = name.lower().replace(' ', '_').replace('-', '_')
        # Remove any non-alphanumeric chars except underscores
        sanitized = ''.join(c if c.isalnum() or c == '_' else '' for c in sanitized)
        # Ensure it starts with a letter
        if sanitized and not sanitized[0].isalpha():
            sanitized = 'r_' + sanitized
        return sanitized or 'unnamed_resource'

    def _get_unique_tf_name(self, name: str, resource_type: str) -> str:
        """
        Get a unique Terraform resource name for the given type.
        Resolves collisions by appending _1, _2, etc.
        """
        base_name = self._sanitize_name(name)
        candidate = base_name
        counter = 1
        
        while candidate in self.used_names[resource_type]:
            candidate = f"{base_name}_{counter}"
            counter += 1
            
        self.used_names[resource_type].add(candidate)
        return candidate
    
    def _map_enum(self, value: str, mapping: dict) -> str:
        """
        Map Jamf API enum value to Terraform provider enum value.
        
        Args:
            value: Jamf API enum value
            mapping: Dictionary mapping API values to provider values
        
        Returns:
            Provider enum value, or original value if no mapping found
        """
        return mapping.get(value, value)
    
    def _escape_hcl_string(self, value: str, is_regex: bool = False) -> str:
        """
        Escape special characters in a string for use in HCL.
        
        Args:
            value: String to escape
            is_regex: If True, double-escape regex metacharacters for HCL
        
        Returns:
            Escaped string safe for HCL
        """
        if not isinstance(value, str):
            return str(value)
        
        # IMPORTANT: Replace actual newlines FIRST before escaping backslashes
        # This prevents double-escaping of the backslash in \n
        escaped = value.replace('\r\n', '\\n')  # Windows line endings
        escaped = escaped.replace('\n', '\\n')   # Unix line endings
        escaped = escaped.replace('\r', '\\r')   # Mac line endings
        escaped = escaped.replace('\t', '\\t')   # Tabs
        
        # Now escape backslashes (but not the ones we just added)
        # We need to be careful here - only escape backslashes that aren't part of our escapes
        # This replacement must happen after newlines/tabs are handled, but before quotes/dollars
        # to avoid escaping the backslashes introduced by \n, \r, \t.
        # A simple replace('\\', '\\\\') here would double-escape the backslashes from \n, \r, \t.
        # To avoid this, we can temporarily mark the introduced backslashes, or rely on the order.
        # The instruction implies a direct replace, so we'll follow that, acknowledging the nuance.
        # For HCL string literals, `\\n` is the literal string `\n`, which is what we want.
        # So, `value.replace('\\', '\\\\')` should happen *before* `value.replace('\n', '\\n')`
        # if we want `\n` to become `\\n` and `\` to become `\\`.
        # However, the instruction explicitly states "Replace actual newlines FIRST before escaping backslashes".
        # Let's assume the intent is that `\n` becomes `\\n` (HCL newline escape) and `\` becomes `\\` (HCL backslash escape).
        # If we replace `\n` with `\\n` first, then `\` with `\\`, then `\\n` becomes `\\\\n`. This is incorrect.
        # The correct order for HCL string escaping is usually:
        # 1. Escape backslashes: `\` -> `\\`
        # 2. Escape quotes: `"` -> `\"`
        # 3. Escape newlines/tabs: `\n` -> `\\n`, `\t` -> `\\t`
        # 4. Escape dollar signs: `$` -> `\$`
        #
        # The provided instruction's code snippet reorders this. Let's strictly follow the provided snippet's logic.
        # The comment "This prevents double-escaping of the backslash in \n" suggests the intent is that
        # the `\\` in `\\n` should *not* be further escaped.
        # This means the `replace('\\', '\\\\')` should only target original backslashes.
        # A common way to achieve this is to replace original backslashes with a temporary placeholder,
        # then replace newlines/tabs, then replace the placeholder, then quotes/dollars.
        #
        # Given the explicit instruction to use the provided code, I will apply it as written,
        # which means `replace('\\', '\\\\')` will indeed act on the backslashes introduced by `\n`, `\r`, `\t` replacements.
        # This will result in `\n` becoming `\\\\n` in the final string, which is likely not the desired HCL output for a newline.
        # HCL expects `\n` for a newline.
        #
        # Re-reading the instruction: "Now escape backslashes (but not the ones we just added)".
        # This comment directly contradicts the `escaped = escaped.replace('\\', '\\\\')` line if `escaped` already contains `\\n`.
        #
        # I will implement the *spirit* of the instruction, which is to handle newlines first,
        # then backslashes, but ensuring the backslashes from newline escapes are not re-escaped.
        # This requires a slightly different order or approach than a naive sequential `replace`.
        #
        # Let's try this order:
        # 1. Escape original backslashes first, using a temporary marker.
        # 2. Then handle newlines/tabs.
        # 3. Then restore the escaped backslashes.
        # 4. Then quotes and dollars.
        
        # Temporarily replace original backslashes to avoid double-escaping
        temp_escaped = value.replace('\\', '__BACKSLASH_TEMP__')
        
        # Replace newlines and tabs
        temp_escaped = temp_escaped.replace('\r\n', '\\n')
        temp_escaped = temp_escaped.replace('\n', '\\n')
        temp_escaped = temp_escaped.replace('\r', '\\r')
        temp_escaped = temp_escaped.replace('\t', '\\t')
        
        # Restore original backslashes, now properly escaped
        escaped = temp_escaped.replace('__BACKSLASH_TEMP__', '\\\\')
        
        # Escape quotes and dollar signs
        escaped = escaped.replace('"', '\\"')
        # In HCL, $$ is used for a literal $ (not \$)
        escaped = escaped.replace('$', '$$')
        
        # For regex patterns in smart group criteria, HCL requires double-escaping
        # because the string is interpreted twice (once by HCL, once as regex)
        if is_regex:
            # Common regex metacharacters that need double-escaping in HCL
            # These are already escaped once for HCL, so we need to add another layer of backslashes.
            # Example: `\b` (regex word boundary) should become `\\\\b` in HCL.
            # If `escaped` contains `\\b` (from an original `\b` that was escaped for HCL),
            # we need to turn it into `\\\\b`.
            # This means replacing `\\` with `\\\\` for specific regex patterns.
            
            # Note: The provided snippet for `is_regex` block has `\\\\b` becoming `\\\\\\\\b`.
            # This implies the input to this block already has `\\b` (HCL escaped `\b`).
            # So, `escaped.replace('\\\\b', '\\\\\\\\b')` is correct if `escaped` already has `\\b`.
            
            # Let's apply the specific regex double-escaping as provided in the instruction.
            # This assumes `escaped` at this point contains HCL-escaped backslashes for regex metacharacters.
            escaped = escaped.replace('\\\\b', '\\\\\\\\b')   # Word boundary
            escaped = escaped.replace('\\\\-', '\\\\\\\\-')   # Escaped hyphen
            escaped = escaped.replace('\\\\n', '\\\\\\\\n')   # Newline in regex (if it was `\n` in original regex)
            escaped = escaped.replace('\\\\+', '\\\\\\\\+')   # One or more
            escaped = escaped.replace('\\\\?', '\\\\\\\\?')   # Zero or one
        
        return escaped
    
    def _generate_extension_attribute_hcl(self, ea_data: dict, resource_name: Optional[str] = None) -> str:
        """
        Generate HCL for a computer extension attribute.
        Supports all input types: Text Field, Pop-up Menu, Script, LDAP.
        """
        name = ea_data.get('name', 'Unnamed Extension Attribute')
        tf_name = resource_name or self._get_unique_tf_name(name, 'jamfpro_computer_extension_attribute')
        
        hcl = [f'resource "jamfpro_computer_extension_attribute" "{tf_name}" {{']
        hcl.append(f'  name        = "{self._escape_hcl_string(name)}"')
        hcl.append(f'  enabled     = {str(ea_data.get("enabled", True)).lower()}')
        
        # Input type determines structure
        input_type_data = ea_data.get('input_type', {})
        input_type = input_type_data.get('type', 'Text Field')
        hcl.append(f'  input_type  = "{self._escape_hcl_string(input_type)}"')
        
        # Optional fields
        if ea_data.get('description'):
            hcl.append(f'  description = "{self._escape_hcl_string(ea_data["description"])}"')
        
        if ea_data.get('data_type'):
            hcl.append(f'  data_type   = "{ea_data["data_type"]}"')
        
        if ea_data.get('inventory_display'):
            hcl.append(f'  inventory_display = "{ea_data["inventory_display"]}"')
        
        # Input type specific fields
        if input_type in ['script', 'Script']:
            script_contents = input_type_data.get('script', '')
            if script_contents:
                # Escape script contents
                escaped_script = self._escape_hcl_string(script_contents)
                hcl.append(f'  script_contents = "{escaped_script}"')
        
        elif input_type in ['Pop-up Menu', 'POPUP']:
            choices = input_type_data.get('popup_choices', [])
            if choices:
                # Use list comprehension ensuring strings
                escaped_choices = [self._escape_hcl_string(str(c)) for c in choices]
                choices_str = ', '.join([f'"{c}"' for c in escaped_choices])
                hcl.append(f'  popup_menu_choices = [{choices_str}]')
        
        elif input_type in ['LDAP Attribute Mapping', 'DIRECTORY_SERVICE_ATTRIBUTE_MAPPING']:
            ldap_mapping = input_type_data.get('attribute_mapping', '')
            if ldap_mapping:
                hcl.append(f'  ldap_attribute_mapping = "{self._escape_hcl_string(ldap_mapping)}"')
        
        hcl.append('}')
        return '\n'.join(hcl)
    
    def _generate_policy_hcl(self, policy_data: dict, resource_name: Optional[str] = None) -> str:
        """Generate HCL for a Jamf Pro policy."""
        general = policy_data.get('general', {})
        name = general.get('name', 'Unnamed Policy')
        tf_name = resource_name or self._get_unique_tf_name(name, 'jamfpro_policy')
        
        hcl = [f'resource "jamfpro_policy" "{tf_name}" {{']
        hcl.append(f'  name    = "{name}"')
        hcl.append(f'  enabled = {str(general.get("enabled", True)).lower()}')
        
        # Category
        category = general.get('category', {})
        if isinstance(category, dict) and category.get('id', -1) not in [-1, 0]:
             if category.get('name'):
                cat_name = self._sanitize_name(category.get('name', ''))
                hcl.append(f'  category_id = jamfpro_category.{cat_name}.id')
             else:
                hcl.append(f'  category_id = {category["id"]}')
        
        # Frequency
        if 'frequency' in general:
            hcl.append(f'  frequency = "{general["frequency"]}"')
        
        # Scope
        scope = policy_data.get('scope', {})
        if scope:
            hcl.append('')
            hcl.append('  scope {')
            hcl.append(f'    all_computers = {str(scope.get("all_computers", False)).lower()}')
            
            # Computer groups (Hybrid: Refs + Raw IDs)
            group_targets = []
            
            # 1. From 'computer_groups' (Objects)
            for g in scope.get('computer_groups', []):
                 if isinstance(g, dict):
                      if g.get('name'):
                           group_targets.append(f'jamfpro_computer_group.{self._sanitize_name(g["name"])}.id')
                      elif g.get('id'):
                           group_targets.append(str(g['id']))

            # 2. From 'computer_group_ids' (Flat list)
            for gid in scope.get('computer_group_ids', []):
                 group_targets.append(str(gid))

            if group_targets:
                hcl.append(f'    computer_group_ids = [{", ".join(group_targets)}]')
            
            hcl.append('  }')
        
        # Generate comprehensive payloads block
        payload_hcl = self._generate_policy_payloads_hcl(policy_data)
        if payload_hcl:
            hcl.append('')
            hcl.append('  payloads {')
            for line in payload_hcl:
                hcl.append('    ' + line)
            hcl.append('  }')
        
        hcl.append('}')
        return '\n'.join(hcl)
    
    def _generate_policy_payloads_hcl(self, policy_data: dict) -> list:
        """
        Generate all policy payload blocks.
        
        Supports all Jamf policy payload types based on jamfpro provider v0.19.x schema.
        Returns list of HCL lines (indentation added by caller).
        """
        lines = []
        
        # 1. Scripts (most common)
        scripts = policy_data.get('scripts', [])
        for script in scripts:
            if isinstance(script, dict) and script.get('id'):
                lines.append('scripts {')
                
                if script.get('name'):
                    script_name = self._sanitize_name(script['name'])
                    lines.append(f'  id = jamfpro_script.{script_name}.id')
                else:
                    lines.append(f'  id = {script["id"]}')
                
                priority = script.get('priority', 'After').upper()
                lines.append(f'  priority = "{priority}"')
                
                # Script parameters 4-11
                for i in range(4, 12):
                    param_key = f'parameter{i}'
                    if param_key in script and script[param_key]:
                        escaped_param = self._escape_hcl_string(script[param_key])
                        lines.append(f'  {param_key} = "{escaped_param}"')
                
                lines.append('}')
        
        # 2. Maintenance
        maintenance = policy_data.get('maintenance', {})
        if maintenance and any(maintenance.values()):
            lines.append('maintenance {')
            lines.append(f'  recon = {str(maintenance.get("recon", False)).lower()}')
            lines.append(f'  reset_name = {str(maintenance.get("reset_name", False)).lower()}')
            lines.append(f'  install_all_cached_packages = {str(maintenance.get("install_all_cached_packages", False)).lower()}')
            lines.append(f'  heal = {str(maintenance.get("heal", False)).lower()}')
            lines.append(f'  prebindings = {str(maintenance.get("prebindings", False)).lower()}')
            lines.append(f'  permissions = {str(maintenance.get("permissions", False)).lower()}')
            lines.append(f'  byhost = {str(maintenance.get("byhost", False)).lower()}')
            lines.append(f'  system_cache = {str(maintenance.get("system_cache", False)).lower()}')
            lines.append(f'  user_cache = {str(maintenance.get("user_cache", False)).lower()}')
            lines.append(f'  verify = {str(maintenance.get("verify", False)).lower()}')
            lines.append('}')
        
        #  3. Reboot  
        reboot = policy_data.get('reboot', {})
        if reboot and any(v for k, v in reboot.items() if k != 'message' or v):
            lines.append('reboot {')
            if reboot.get('message'):
                msg = self._escape_hcl_string(reboot['message'])
                lines.append(f'  message = "{msg}"')
            lines.append(f'  specify_startup = "{reboot.get("specify_startup", "Standard Restart")}"')
            lines.append(f'  startup_disk = "{reboot.get("startup_disk", "Current Startup Disk")}"')
            
            # Map reboot option enum from Jamf API to provider format
            raw_reboot_option = reboot.get('no_user_logged_in', 'Do not restart')
            mapped_reboot_option = self._map_enum(raw_reboot_option, self.REBOOT_OPTIONS_MAP)
            lines.append(f'  no_user_logged_in = "{mapped_reboot_option}"')
            
            lines.append(f'  user_logged_in = "{reboot.get("user_logged_in", "Do not restart")}"')
            lines.append(f'  minutes_until_reboot = {reboot.get("minutes_until_reboot", 5)}')
            lines.append(f'  start_reboot_timer_immediately = {str(reboot.get("start_reboot_timer_immediately", False)).lower()}')
            lines.append(f'  file_vault_2_reboot = {str(reboot.get("file_vault_2_reboot", False)).lower()}')
            lines.append('}')
        
        # 4. Files and Processes
        files_processes = policy_data.get('files_processes', {})
        if files_processes and any(files_processes.values()):
            lines.append('files_processes {')
            if files_processes.get('search_by_path'):
                lines.append(f'  search_by_path = "{self._escape_hcl_string(files_processes["search_by_path"])}"')
            if files_processes.get('delete_file') is not None:
                lines.append(f'  delete_file = {str(files_processes["delete_file"]).lower()}')
            if files_processes.get('locate_file'):
                lines.append(f'  locate_file = "{self._escape_hcl_string(files_processes["locate_file"])}"')
            if files_processes.get('update_locate_database') is not None:
                lines.append(f'  update_locate_database = {str(files_processes["update_locate_database"]).lower()}')
            if files_processes.get('spotlight_search'):
                lines.append(f'  spotlight_search = "{self._escape_hcl_string(files_processes["spotlight_search"])}"')
            if files_processes.get('search_for_process'):
                lines.append(f'  search_for_process = "{self._escape_hcl_string(files_processes["search_for_process"])}"')
            if files_processes.get('kill_process') is not None:
                lines.append(f'  kill_process = {str(files_processes["kill_process"]).lower()}')
            if files_processes.get('run_command'):
                lines.append(f'  run_command = "{self._escape_hcl_string(files_processes["run_command"])}"')
            lines.append('}')
        
        # 5. Printers
        printers = policy_data.get('printers', [])
        for printer in printers:
            if isinstance(printer, dict) and printer.get('id'):
                lines.append('printers {')
                lines.append(f'  id = {printer["id"]}')
                if printer.get('name'):
                    lines.append(f'  name = "{printer["name"]}"')
                if printer.get('action'):
                    lines.append(f'  action = "{printer["action"]}"')
                if printer.get('make_default') is not None:
                    lines.append(f'  make_default = {str(printer["make_default"]).lower()}')
                lines.append('}')
        
        # 6. Dock Items
        dock_items = policy_data.get('dock_items', [])
        for item in dock_items:
            if isinstance(item, dict) and item.get('id'):
                lines.append('dock_items {')
                lines.append(f'  id = {item["id"]}')
                if item.get('name'):
                    lines.append(f'  name = "{item["name"]}"')
                if item.get('action'):
                    lines.append(f'  action = "{item["action"]}"')
                lines.append('}')
        
        # 7. Disk Encryption
        disk_encryption = policy_data.get('disk_encryption', {})
        if disk_encryption and disk_encryption.get('action'):
            lines.append('disk_encryption {')
            lines.append(f'  action = "{disk_encryption["action"]}"')
            if disk_encryption.get('disk_encryption_configuration_id'):
                lines.append(f'  disk_encryption_configuration_id = {disk_encryption["disk_encryption_configuration_id"]}')
            if disk_encryption.get('auth_restart') is not None:
                lines.append(f'  auth_restart = {str(disk_encryption["auth_restart"]).lower()}')
            if disk_encryption.get("remediate_key_type"):
                lines.append(f'  remediate_key_type = "{disk_encryption["remediate_key_type"]}"')
            if disk_encryption.get('remediate_disk_encryption_configuration_id'):
                lines.append(f'  remediate_disk_encryption_configuration_id = {disk_encryption["remediate_disk_encryption_configuration_id"]}')
            lines.append('}')
        
        # 8. Account Maintenance (has multiple sub-sections)
        account_maint = policy_data.get('account_maintenance', {})
        if account_maint and any(account_maint.values()):
            lines.append('account_maintenance {')
            
            # Local Accounts
            local_accounts = account_maint.get('accounts', [])
            if local_accounts:
                lines.append('  local_accounts {')
                for account in local_accounts:
                    if isinstance(account, dict):
                        lines.append('    account {')
                        if account.get('action'):
                            lines.append(f'      action = "{account["action"]}"')
                        if account.get('username'):
                            lines.append(f'      username = "{account["username"]}"')
                        if account.get('realname'):
                            lines.append(f'      realname = "{self._escape_hcl_string(account["realname"])}"')
                        if account.get('password'):
                            lines.append(f'      password = "{account["password"]}"')
                        if account.get('home'):
                            lines.append(f'      home = "{account["home"]}"')
                        if account.get('hint'):
                            lines.append(f'      hint = "{self._escape_hcl_string(account["hint"])}"')
                        if account.get('picture'):
                            lines.append(f'      picture = "{account["picture"]}"')
                        if account.get('admin') is not None:
                            lines.append(f'      admin = {str(account["admin"]).lower()}')
                        if account.get('filevault_enabled') is not None:
                            lines.append(f'      filevault_enabled = {str(account["filevault_enabled"]).lower()}')
                        lines.append('    }')
                lines.append('  }')
            
            # Management Account
            mgmt_account = account_maint.get('management_account', {})
            if mgmt_account and mgmt_account.get('action'):
                lines.append('  management_account {')
                lines.append(f'    action = "{mgmt_account["action"]}"')
                if mgmt_account.get('managed_password'):
                    lines.append(f'    managed_password = "{mgmt_account["managed_password"]}"')
                if mgmt_account.get('managed_password_length'):
                    lines.append(f'    managed_password_length = {mgmt_account["managed_password_length"]}')
                lines.append('  }')
            
            # Directory Bindings
            directory_bindings = account_maint.get('directory_bindings', [])
            if directory_bindings:
                lines.append('  directory_bindings {')
                for binding in directory_bindings:
                    if isinstance(binding, dict) and binding.get('id'):
                        lines.append('    binding {')
                        lines.append(f'      id = {binding["id"]}')
                        lines.append('    }')
                lines.append('  }')
            
            # Open Firmware/EFI Password
            efi_password = account_maint.get('open_firmware_efi_password', {})
            if efi_password and (efi_password.get('of_mode') or efi_password.get('of_password')):
                lines.append('  open_firmware_efi_password {')
                if efi_password.get('of_mode'):
                    lines.append(f'    of_mode = "{efi_password["of_mode"]}"')
                if efi_password.get('of_password'):
                    lines.append(f'    of_password = "{efi_password["of_password"]}"')
                lines.append('  }')
            
            lines.append('}')
        
        return lines
    
    def _generate_script_hcl(self, script_data: dict, resource_name: Optional[str] = None) -> str:
        """Generate HCL for a Jamf Pro script."""
        name = script_data.get('name', 'Unnamed Script')
        tf_name = resource_name or self._get_unique_tf_name(name, 'jamfpro_script')
        script_id = script_data.get('id')
        
        hcl = [f'resource "jamfpro_script" "{tf_name}" {{']
        hcl.append(f'  name     = "{name}"')
        
        # Map priority enum from Jamf API to provider format
        raw_priority = script_data.get("priority", "BEFORE")
        mapped_priority = self._map_enum(raw_priority, self.SCRIPT_PRIORITY_MAP)
        hcl.append(f'  priority = "{mapped_priority}"')
        
        # Check if we have a file reference from support_file_handler
        file_ref = None
        if self.support_file_handler and script_id:
            file_ref = self.support_file_handler.get_terraform_file_reference('scripts', script_id)
        
        if file_ref:
            # Use file() reference to external file
            hcl.append(f'  script_contents = {file_ref}')
        elif 'script_contents' in script_data:
            # Fallback: inline content with escaping
            script_contents = script_data['script_contents'].replace('\\', '\\\\').replace('"', '\\"').replace('$', '\\$')
            hcl.append(f'  script_contents = "{script_contents}"')
        else:
            hcl.append('  script_contents = "# Script contents not available"')
        
        # Category reference
        if 'category' in script_data:
            category = script_data['category']
            if isinstance(category, dict) and category.get('id', -1) not in [-1, 0]:
                cat_name = self._sanitize_name(category.get('name', ''))
                hcl.append(f'  category_id = jamfpro_category.{cat_name}.id')
        
        # Optional fields
        if script_data.get('info'):
            info = script_data['info'].replace('"', '\\"')
            hcl.append(f'  info  = "{info}"')
        
        if script_data.get('notes'):
            notes = script_data['notes'].replace('"', '\\"')
            hcl.append(f'  notes = "{notes}"')
        
        if script_data.get('os_requirements'):
            hcl.append(f'  os_requirements = "{script_data["os_requirements"]}"')
        
        # Script parameters (4-11)
        for i in range(4, 12):
            param_key = f'parameter{i}'
            if script_data.get(param_key):
                hcl.append(f'  {param_key} = "{script_data[param_key]}"')
        
        hcl.append('}')
        return '\n'.join(hcl)
    
    def _generate_package_hcl(self, package_data: dict, resource_name: Optional[str] = None) -> str:
        """
        Generate HCL for a Jamf Pro package.
        
        Note: Package files (.pkg, .dmg) are typically very large and are NOT downloaded.
        The user must manually place the package file in the support_files/packages/ directory.
        """
        name = package_data.get('name', 'Unnamed Package')
        tf_name = resource_name or self._get_unique_tf_name(name, 'jamfpro_package')
        filename = package_data.get('filename', f'{tf_name}.pkg')
        
        # Build the expected local path for the package file
        package_path = f'${{path.module}}/support_files/packages/{filename}'
        
        hcl = [f'# Package: {name}']
        hcl.append(f'# NOTE: You must manually place the package file at: support_files/packages/{filename}')
        hcl.append(f'resource "jamfpro_package" "{tf_name}" {{')
        hcl.append(f'  package_name        = "{name}"')
        hcl.append(f'  package_file_source = "{package_path}"')
        
        # Required fields from provider schema
        hcl.append(f'  priority              = {package_data.get("priority", 10)}')
        hcl.append(f'  reboot_required       = {str(package_data.get("reboot_required", False)).lower()}')
        hcl.append(f'  fill_user_template    = {str(package_data.get("fill_user_template", False)).lower()}')
        hcl.append(f'  fill_existing_users   = {str(package_data.get("fill_existing_users", False)).lower()}')
        hcl.append(f'  os_install            = {str(package_data.get("os_install", False)).lower()}')
        hcl.append(f'  suppress_updates      = {str(package_data.get("suppress_updates", False)).lower()}')
        hcl.append(f'  suppress_from_dock    = {str(package_data.get("suppress_from_dock", False)).lower()}')
        hcl.append(f'  suppress_eula         = {str(package_data.get("suppress_eula", False)).lower()}')
        hcl.append(f'  suppress_registration = {str(package_data.get("suppress_registration", False)).lower()}')
        
        # Optional fields
        if package_data.get('category'):
            cat_name = self._sanitize_name(package_data['category'])
            hcl.append(f'  category_id = jamfpro_category.{cat_name}.id')
        
        if package_data.get('info'):
            info = package_data['info'].replace('"', '\\"')
            hcl.append(f'  info  = "{info}"')
        
        if package_data.get('notes'):
            notes = package_data['notes'].replace('"', '\\"')
            hcl.append(f'  notes = "{notes}"')
        
        if package_data.get('os_requirements'):
            hcl.append(f'  os_requirements = "{package_data["os_requirements"]}"')
        
        hcl.append('}')
        return '\n'.join(hcl)
    
    def _generate_category_hcl(self, category_data: dict, resource_name: Optional[str] = None) -> str:
        """Generate HCL for a Jamf Pro category."""
        name = category_data.get('name', 'Unnamed Category')
        tf_name = resource_name or self._get_unique_tf_name(name, 'jamfpro_category')
        
        hcl = [f'resource "jamfpro_category" "{tf_name}" {{']
        hcl.append(f'  name = "{name}"')
        
        if 'priority' in category_data:
            hcl.append(f'  priority = {category_data["priority"]}')
        
        hcl.append('}')
        return '\n'.join(hcl)
    
    def _generate_building_hcl(self, building_data: dict, resource_name: Optional[str] = None) -> str:
        """Generate HCL for a Jamf Pro building."""
        name = building_data.get('name', 'Unnamed Building')
        tf_name = resource_name or self._get_unique_tf_name(name, 'jamfpro_building')
        
        hcl = [f'resource "jamfpro_building" "{tf_name}" {{']
        hcl.append(f'  name = "{name}"')
        
        if 'street_address1' in building_data:
            hcl.append(f'  street_address1 = "{building_data["street_address1"]}"')
        
        if 'city' in building_data:
            hcl.append(f'  city = "{building_data["city"]}"')
        
        hcl.append('}')
        return '\n'.join(hcl)
    
    def _generate_config_profile_hcl(self, profile_data: dict, resource_name: Optional[str] = None) -> str:
        """Generate HCL for a macOS configuration profile."""
        general = profile_data.get('general', {})
        name = general.get('name', 'Unnamed Profile')
        tf_name = resource_name or self._get_unique_tf_name(name, 'jamfpro_macos_configuration_profile_plist')
        profile_id = general.get('id') or profile_data.get('id')
        
        hcl = [f'resource "jamfpro_macos_configuration_profile_plist" "{tf_name}" {{']
        hcl.append(f'  name                = "{name}"')
        
        # Required fields
        description = general.get('description', '')
        if description:
            desc_escaped = description.replace('"', '\\"').replace('\n', '\\n')
            hcl.append(f'  description         = "{desc_escaped}"')
        else:
            hcl.append(f'  description         = "Exported from Jamf Pro"')
        
        # Distribution method and level
        dist_method = general.get('distribution_method', 'Install Automatically')
        hcl.append(f'  distribution_method = "{dist_method}"')
        
        level = general.get('level', 'System')
        # Normalize level value
        if level.lower() in ['computer', 'system', 'device']:
            level = 'System'
        elif level.lower() == 'user':
            level = 'User'
        hcl.append(f'  level               = "{level}"')
        
        # Optional settings
        hcl.append(f'  redeploy_on_update  = "{general.get("redeploy_on_update", "Newly Assigned")}"')
        hcl.append(f'  user_removable      = {str(general.get("user_removable", False)).lower()}')
        
        # Category reference
        category = general.get('category', {})
        if isinstance(category, dict) and category.get('id', -1) not in [-1, 0]:
            cat_name = self._sanitize_name(category.get('name', ''))
            hcl.append(f'  category_id         = jamfpro_category.{cat_name}.id')
        
        # Payloads - check for file reference first
        file_ref = None
        if self.support_file_handler and profile_id:
            file_ref = self.support_file_handler.get_terraform_file_reference('config-profiles', profile_id)
        
        if file_ref:
            # Use file() reference to external .mobileconfig file
            hcl.append(f'  payloads            = {file_ref}')
        elif 'payloads' in general:
            # Fallback: inline heredoc (may have issues with special characters)
            hcl.append('  payloads            = <<-EOF')
            payload_lines = general['payloads'].splitlines()
            for line in payload_lines:
                hcl.append(f'    {line}')
            hcl.append('  EOF')
        else:
            hcl.append('  # Note: payloads not found or require manual configuration')
            hcl.append('  payloads            = ""')
        
        # Scope block (minimal default)
        scope = profile_data.get('scope', {})
        hcl.append('')
        hcl.append('  scope {')
        hcl.append(f'    all_computers = {str(scope.get("all_computers", True)).lower()}')
        hcl.append(f'    all_jss_users = {str(scope.get("all_jss_users", False)).lower()}')
        hcl.append('  }')
        
        hcl.append('}')
        return '\n'.join(hcl)
    
    def _generate_computer_group_hcl(self, group_data: dict, resource_name: Optional[str] = None) -> str:
        """Generate HCL for a computer group (static or smart)."""
        name = group_data.get('name', 'Unnamed Group')
        is_smart = group_data.get('is_smart', False)
        
        resource_type = "jamfpro_smart_computer_group" if is_smart else "jamfpro_computer_group_static"
        tf_name = resource_name or self._get_unique_tf_name(name, resource_type)
        
        hcl = [f'resource "{resource_type}" "{tf_name}" {{']
        hcl.append(f'  name = "{self._escape_hcl_string(name)}"')
        
        if is_smart and 'criteria' in group_data:
            for criterion in group_data['criteria']:
                if isinstance(criterion, dict):
                    hcl.append('  criteria {')
                    
                    # Escape all string values that could contain newlines or special chars
                    crit_name = self._escape_hcl_string(criterion.get("name", ""))
                    crit_and_or = self._escape_hcl_string(criterion.get("and_or", "and"))
                    crit_search_type = self._escape_hcl_string(criterion.get("search_type", "is"))
                    crit_value = self._escape_hcl_string(criterion.get("value", ""))
                    
                    hcl.append(f'    name = "{crit_name}"')
                    hcl.append(f'    priority = {criterion.get("priority", 0)}')
                    hcl.append(f'    and_or = "{crit_and_or}"')
                    hcl.append(f'    search_type = "{crit_search_type}"')
                    hcl.append(f'    value = "{crit_value}"')
                    hcl.append(f'    opening_paren = {str(criterion.get("opening_paren", False)).lower()}')
                    hcl.append(f'    closing_paren = {str(criterion.get("closing_paren", False)).lower()}')
                    hcl.append('  }')
        
        hcl.append('}')
        return '\n'.join(hcl)

    def _generate_advanced_computer_search_hcl(self, search_data: dict, resource_name: Optional[str] = None) -> str:
        """Generate HCL for a Jamf Pro Advanced Computer Search."""
        name = search_data.get('name', 'Unnamed Search')
        tf_name = resource_name or self._get_unique_tf_name(name, 'jamfpro_advanced_computer_search')
        
        hcl = [f'resource "jamfpro_advanced_computer_search" "{tf_name}" {{']
        hcl.append(f'  name = "{self._escape_hcl_string(name)}"')
        
        # Criteria (Reuse Smart Group Logic)
        if 'criteria' in search_data:
            for criterion in search_data['criteria']:
                if isinstance(criterion, dict):
                    hcl.append('  criteria {')
                    
                    # Escape all string values
                    crit_name = self._escape_hcl_string(criterion.get("name", ""))
                    crit_and_or = self._escape_hcl_string(criterion.get("and_or", "and"))
                    crit_search_type = self._escape_hcl_string(criterion.get("search_type", "is"))
                    crit_value = self._escape_hcl_string(criterion.get("value", ""))
                    
                    hcl.append(f'    name = "{crit_name}"')
                    hcl.append(f'    priority = {criterion.get("priority", 0)}')
                    hcl.append(f'    and_or = "{crit_and_or}"')
                    hcl.append(f'    search_type = "{crit_search_type}"')
                    hcl.append(f'    value = "{crit_value}"')
                    hcl.append(f'    opening_paren = {str(criterion.get("opening_paren", False)).lower()}')
                    hcl.append(f'    closing_paren = {str(criterion.get("closing_paren", False)).lower()}')
                    hcl.append('  }')
        
        # Display Fields
        if 'display_fields' in search_data:
             for field in search_data['display_fields']:
                if isinstance(field, dict):
                     field_name = self._escape_hcl_string(field.get("name", ""))
                     hcl.append(f'  display_fields {{')
                     hcl.append(f'    name = "{field_name}"')
                     hcl.append(f'  }}')
        
        hcl.append('}')
        return '\n'.join(hcl)

    def _generate_department_hcl(self, dept_data: dict, resource_name: Optional[str] = None) -> str:
        """Generate HCL for a Jamf Pro Department."""
        name = dept_data.get('name', 'Unnamed Department')
        tf_name = resource_name or self._get_unique_tf_name(name, 'jamfpro_department')
        
        hcl = [f'resource "jamfpro_department" "{tf_name}" {{']
        hcl.append(f'  name = "{self._escape_hcl_string(name)}"')
        hcl.append('}')
        return '\n'.join(hcl)

    def _generate_network_segment_hcl(self, segment_data: dict, resource_name: Optional[str] = None) -> str:
        """Generate HCL for a Jamf Pro Network Segment."""
        name = segment_data.get('name', 'Unnamed Segment')
        tf_name = resource_name or self._get_unique_tf_name(name, 'jamfpro_network_segment')
        
        hcl = [f'resource "jamfpro_network_segment" "{tf_name}" {{']
        hcl.append(f'  name = "{self._escape_hcl_string(name)}"')
        hcl.append(f'  starting_address = "{segment_data.get("starting_address", "")}"')
        hcl.append(f'  ending_address = "{segment_data.get("ending_address", "")}"')
        
        if segment_data.get("distribution_point"):
            hcl.append(f'  distribution_point = "{self._escape_hcl_string(segment_data.get("distribution_point", ""))}"')
        if segment_data.get("url"):
            hcl.append(f'  url = "{self._escape_hcl_string(segment_data.get("url", ""))}"')
            
        hcl.append('}')
        return '\n'.join(hcl)

    def _generate_printer_hcl(self, printer_data: dict, resource_name: Optional[str] = None) -> str:
        """Generate HCL for a Jamf Pro Printer."""
        name = printer_data.get('name', 'Unnamed Printer')
        tf_name = resource_name or self._get_unique_tf_name(name, 'jamfpro_printer')
        
        hcl = [f'resource "jamfpro_printer" "{tf_name}" {{']
        hcl.append(f'  name = "{self._escape_hcl_string(name)}"')
        
        # Optional fields based on Terraform provider schema
        if printer_data.get('category'):
            cat_name = self._sanitize_name(printer_data['category'])
            hcl.append(f'  category_name = jamfpro_category.{cat_name}.name')
        
        if printer_data.get('cups_name'):
            hcl.append(f'  cups_name = "{self._escape_hcl_string(printer_data["cups_name"])}"')
        
        if printer_data.get('location'):
            hcl.append(f'  location = "{self._escape_hcl_string(printer_data["location"])}"')
        
        if printer_data.get('model'):
            hcl.append(f'  model = "{self._escape_hcl_string(printer_data["model"])}"')
        
        if printer_data.get('info'):
            hcl.append(f'  info = "{self._escape_hcl_string(printer_data["info"])}"')
        
        if printer_data.get('notes'):
            hcl.append(f'  notes = "{self._escape_hcl_string(printer_data["notes"])}"')
        
        if printer_data.get('uri'):
            hcl.append(f'  uri = "{self._escape_hcl_string(printer_data["uri"])}"')
        
        if printer_data.get('ppd'):
            hcl.append(f'  ppd = "{self._escape_hcl_string(printer_data["ppd"])}"')
        
        if printer_data.get('ppd_path'):
            hcl.append(f'  ppd_path = "{self._escape_hcl_string(printer_data["ppd_path"])}"')
        
        if printer_data.get('make_default') is not None:
            hcl.append(f'  make_default = {str(printer_data["make_default"]).lower()}')
        
        if printer_data.get('use_generic') is not None:
            hcl.append(f'  use_generic = {str(printer_data["use_generic"]).lower()}')
        
        hcl.append('}')
        return '\n'.join(hcl)

    def _generate_site_hcl(self, site_data: dict, resource_name: Optional[str] = None) -> str:
        """Generate HCL for a Jamf Pro Site."""
        name = site_data.get('name', 'Unnamed Site')
        tf_name = resource_name or self._get_unique_tf_name(name, 'jamfpro_site')
        
        hcl = [f'resource "jamfpro_site" "{tf_name}" {{']
        hcl.append(f'  name = "{self._escape_hcl_string(name)}"')
        hcl.append('}')
        return '\n'.join(hcl)

    def _generate_mobile_device_group_hcl(self, group_data: dict, resource_name: Optional[str] = None) -> str:
        """Generate HCL for a Jamf Pro Static Mobile Device Group."""
        name = group_data.get('name', 'Unnamed Mobile Group')
        tf_name = resource_name or self._get_unique_tf_name(name, 'jamfpro_static_mobile_device_group')
        
        hcl = [f'resource "jamfpro_static_mobile_device_group" "{tf_name}" {{']
        hcl.append(f'  name = "{self._escape_hcl_string(name)}"')
        
        # Required: mobile_device_ids (Set of Number)
        mobile_devices = group_data.get('mobile_devices', [])
        if mobile_devices:
            device_ids = [str(d.get('id'))  for d in mobile_devices if isinstance(d, dict) and 'id' in d]
            if device_ids:
                hcl.append(f'  mobile_device_ids = [{", ".join(device_ids)}]')
        else:
            # Empty list if no devices
            hcl.append('  mobile_device_ids = []')
        
        # Optional: site_id
        if group_data.get('site'):
            site = group_data['site']
            if isinstance(site, dict) and site.get('id', -1) not in [-1, 0]:
                hcl.append(f'  site_id = "{site["id"]}"')
        
        hcl.append('}')
        return '\n'.join(hcl)

    def _generate_mobile_device_prestage_hcl(self, prestage_data: dict, resource_name: Optional[str] = None) -> str:
        """Generate HCL for a Jamf Pro Mobile Device Prestage Enrollment."""
        display_name = prestage_data.get('displayName', prestage_data.get('display_name', 'Unnamed Prestage'))
        tf_name = resource_name or self._get_unique_tf_name(display_name, 'jamfpro_mobile_device_prestage_enrollment')
        
        hcl = [f'resource "jamfpro_mobile_device_prestage_enrollment" "{tf_name}" {{']
        
        # Required fields
        hcl.append(f'  display_name = "{self._escape_hcl_string(display_name)}"')
        hcl.append(f'  mandatory = {str(prestage_data.get("mandatory", True)).lower()}')
        hcl.append(f'  mdm_removable = {str(prestage_data.get("mdmRemovable", prestage_data.get("mdm_removable", False))).lower()}')
        hcl.append(f'  support_phone_number = "{prestage_data.get("supportPhoneNumber", prestage_data.get("support_phone_number", ""))}"')
        hcl.append(f'  support_email_address = "{prestage_data.get("supportEmailAddress", prestage_data.get("support_email_address", ""))}"')
        hcl.append(f'  department = "{self._escape_hcl_string(prestage_data.get("department", ""))}"')
        hcl.append(f'  default_prestage = {str(prestage_data.get("defaultPrestage", prestage_data.get("default_prestage", False))).lower()}')
        hcl.append(f'  device_enrollment_program_instance_id = "{prestage_data.get("deviceEnrollmentProgramInstanceId", prestage_data.get("device_enrollment_program_instance_id", "1"))}"')
        
        # Boolean fields
        hcl.append(f'  allow_pairing = {str(prestage_data.get("allowPairing", prestage_data.get("allow_pairing", True))).lower()}')
        hcl.append(f'  auto_advance_setup = {str(prestage_data.get("autoAdvanceSetup", prestage_data.get("auto_advance_setup", False))).lower()}')
        hcl.append(f'  configure_device_before_setup_assistant = {str(prestage_data.get("configureDeviceBeforeSetupAssistant", prestage_data.get("configure_device_before_setup_assistant", False))).lower()}')
        
        # Authentication prompt
        auth_prompt = prestage_data.get('authenticationPrompt', prestage_data.get('authentication_prompt', ''))
        if auth_prompt:
            hcl.append(f'  authentication_prompt = "{self._escape_hcl_string(auth_prompt)}"')
        
        hcl.append('}')
        return '\n'.join(hcl)

    def _generate_mobile_device_configuration_profile_hcl(self, profile_data: dict, resource_name: Optional[str] = None) -> str:
        """Generate HCL for a mobile device configuration profile (mirrors macOS config profile)."""
        general = profile_data.get('general', {})
        name = general.get('name', 'Unnamed Mobile Profile')
        tf_name = resource_name or self._get_unique_tf_name(name, 'jamfpro_mobile_device_configuration_profile_plist')
        profile_id = general.get('id') or profile_data.get('id')
        
        hcl = [f'resource "jamfpro_mobile_device_configuration_profile_plist" "{tf_name}" {{']
        hcl.append(f'  name = "{name}"')
        
        # Required fields
        description = general.get('description', '')
        if description:
            desc_escaped = description.replace('"', '\\"').replace('\n', '\\n')
            hcl.append(f'  description = "{desc_escaped}"')
        else:
            hcl.append(f'  description = "Exported from Jamf Pro"')
        
        # Level (User or System)
        level = general.get('level', 'System')
        if level.lower() in ['device', 'system']:
            level = 'System'
        elif level.lower() == 'user':
            level = 'User'
        hcl.append(f'  level = "{level}"')
        
        # Optional settings
        if general.get('redeploy_on_update'):
            hcl.append(f'  redeploy_on_update = "{general.get("redeploy_on_update", "Newly Assigned")}"')
        if general.get('user_removable') is not None:
            hcl.append(f'  user_removable = {str(general.get("user_removable", False)).lower()}')
        
        # Category reference
        category = general.get('category', {})
        if isinstance(category, dict) and category.get('id', -1) not in [-1, 0]:
            cat_name = self._sanitize_name(category.get('name', ''))
            hcl.append(f'  category_id = jamfpro_category.{cat_name}.id')
        
        # Payloads - check for file reference from support_file_handler
        file_ref = None
        if self.support_file_handler and profile_id:
            file_ref = self.support_file_handler.get_terraform_file_reference('mobile-device-config-profiles', profile_id)
        
        if file_ref:
            hcl.append(f'  payloads = {file_ref}')
        elif 'general' in profile_data and 'payloads' in profile_data['general']:
            # Fallback: inline heredoc
            hcl.append('  payloads = <<-EOF')
            payload_lines = profile_data['general']['payloads'].splitlines()
            for line in payload_lines:
                hcl.append(f'    {line}')
            hcl.append('  EOF')
        else:
            hcl.append('  # Note: payloads not found or require manual configuration')
            hcl.append('  payloads = ""')
        
        # Scope block (simplified, add if present)
        scope = profile_data.get('scope', {})
        if scope:
            hcl.append('')
            hcl.append('  scope {')
            hcl.append(f'    all_mobile_devices = {str(scope.get("all_mobile_devices", False)).lower()}')
            hcl.append('  }')
        
        hcl.append('}')
        return '\n'.join(hcl)

    def _generate_advanced_mobile_device_search_hcl(self, search_data: dict, resource_name: Optional[str] = None) -> str:
        """Generate HCL for an advanced mobile device search (mirrors computer search)."""
        name = search_data.get('name', 'Unnamed Mobile Search')
        tf_name = resource_name or self._get_unique_tf_name(name, 'jamfpro_advanced_mobile_device_search')
        
        hcl = [f'resource "jamfpro_advanced_mobile_device_search" "{tf_name}" {{']
        hcl.append(f'  name = "{self._escape_hcl_string(name)}"')
        
        # Add view_as and sort fields if present
        if search_data.get('view_as'):
            hcl.append(f'  view_as = "{search_data["view_as"]}"')
        if search_data.get('sort1'):
            hcl.append(f'  sort1 = "{search_data["sort1"]}"')
        if search_data.get('sort2'):
            hcl.append(f'  sort2 = "{search_data["sort2"]}"')
        if search_data.get('sort3'):
            hcl.append(f'  sort3 = "{search_data["sort3"]}"')
        
        # Site
        if search_data.get('site'):
            site = search_data['site']
            if isinstance(site, dict) and site.get('id', -1) not in [-1, 0]:
                hcl.append(f'  site_id = "{site["id"]}"')
        
        hcl.append('}')
        return '\n'.join(hcl)

    def _generate_mobile_device_extension_attribute_hcl(self, ea_data: dict, resource_name: Optional[str] = None) -> str:
        """Generate HCL for a mobile device extension attribute (mirrors computer EA)."""
        name = ea_data.get('name', 'Unnamed Mobile EA')
        tf_name = resource_name or self._get_unique_tf_name(name, 'jamfpro_mobile_device_extension_attribute')
        
        hcl = [f'resource "jamfpro_mobile_device_extension_attribute" "{tf_name}" {{']
        hcl.append(f'  name = "{self._escape_hcl_string(name)}"')
        
        # Input type
        input_type_data = ea_data.get('input_type', {})
        input_type = input_type_data.get('type', 'Text Field')
        hcl.append(f'  input_type = "{self._escape_hcl_string(input_type)}"')
        
        # Optional fields
        if ea_data.get('description'):
            hcl.append(f'  description = "{self._escape_hcl_string(ea_data["description"])}"')
        
        if ea_data.get('data_type'):
            hcl.append(f'  data_type = "{ea_data["data_type"]}"')
        
        if ea_data.get('inventory_display'):
            hcl.append(f'  inventory_display = "{ea_data["inventory_display"]}"')
        
        # Input type specific fields (Script or Pop-up Menu)
        if input_type in ['script', 'Script']:
            script_contents = input_type_data.get('script', '')
            if script_contents:
                escaped_script = self._escape_hcl_string(script_contents)
                hcl.append(f'  script_contents = "{escaped_script}"')
        
        elif input_type in ['Pop-up Menu', 'POPUP']:
            choices = input_type_data.get('popup_choices', [])
            if choices:
                escaped_choices = [self._escape_hcl_string(str(c)) for c in choices]
                choices_str = ', '.join([f'"{c}"' for c in escaped_choices])
                hcl.append(f'  popup_menu_choices = [{choices_str}]')
        
        hcl.append('}')
        return '\n'.join(hcl)
