# Jamf Pro Terraform Provider - Complete Resource Requirements Map

## Overview

This document provides a comprehensive mapping of **all required fields** for every resource in the `deploymenttheory/jamfpro` Terraform provider based on official documentation and schema analysis.

---

## 📋 **Resource Categories**

### **1. Policies & Management**

#### `jamfpro_policy`

**REQUIRED FIELDS:**

- `enabled` (Boolean) - Whether the policy is active
- `name` (String) - Policy name
- `payloads` (Block List, Min: 1) - At least one payload configuration
- `scope` (Block List, Min: 1, Max: 1) - Scope configuration

**Scope Options** (at least ONE required):

- `all_computers = true`
- `computer_group_ids = [...]`
- `computer_ids = [...]`
- `department_ids = [...]`

**Example:**

```hcl
resource "jamfpro_policy" "example" {
  name    = "Install Software"
  enabled = true

  payloads {
    # Payload configuration
  }

  scope {
    all_computers = true
  }
}
```

---

### **2. Computer Groups**

#### `jamfpro_computer_group` (Static Group)

**REQUIRED FIELDS:**

- `name` (String) - Group name

**Example:**

```hcl
resource "jamfpro_computer_group" "example" {
  name = "Marketing Computers"
}
```

#### `jamfpro_smart_computer_group` (Smart Group)

**REQUIRED FIELDS:**

- `name` (String) - Group name
- `is_smart` (Boolean) - Must be `true`
- `criteria` (Block) - Search criteria

**Example:**

```hcl
resource "jamfpro_smart_computer_group" "macos_14" {
  name     = "macOS 14+ Devices"
  is_smart = true

  criteria {
    name        = "Operating System Version"
    search_type = "greater than or equal"
    value       = "14.0"
  }
}
```

---

### **3. Configuration Profiles**

#### `jamfpro_macos_configuration_profile_plist`

**REQUIRED FIELDS:**

- `name` (String) - Profile name
- `description` (String) - Profile description
- `distribution_method` (String) - Distribution method
- `level` (String) - "Device" or "User"
- `payloads` (List) - Configuration payloads

**Example:**

```hcl
resource "jamfpro_macos_configuration_profile_plist" "wifi" {
  name                = "Corporate WiFi"
  description         = "WiFi configuration"
  distribution_method = "Install Automatically"
  level               = "Device"

  payloads = [
    # Payload configuration
  ]
}
```

#### `jamfpro_mobile_device_configuration_profile_plist`

**REQUIRED FIELDS:**

- Same as macOS configuration profile

---

### **4. Packages & Scripts**

#### `jamfpro_package`

**REQUIRED FIELDS:**

- `package_file_source` (String) - File path or URL source
- `filename` (String) - Package filename

**Example:**

```hcl
resource "jamfpro_package" "chrome" {
  package_file_source = "/path/to/GoogleChrome.pkg"
  filename            = "GoogleChrome.pkg"
}
```

#### `jamfpro_script`

**REQUIRED FIELDS:**

- `name` (String) - Script name
- `script_contents` (String) - Script code

**Example:**

```hcl
resource "jamfpro_script" "install_homebrew" {
  name             = "Install Homebrew"
  script_contents  = file("${path.module}/scripts/install_homebrew.sh")
}
```

---

### **5. Extension Attributes**

#### `jamfpro_computer_extension_attribute`

**REQUIRED FIELDS:**

- `name` (String) - Attribute name
- `enabled` (Boolean) - Whether enabled
- `input_type` (String) - "Text Field", "Pop-up Menu", or "script"

**Optional but Common:**

- `data_type` (String) - "String", "Integer", or "Date"
- `input_script` (String) - Script for "script" input type
- `input_popup` (List) - Choices for "Pop-up Menu"

**Example:**

```hcl
resource "jamfpro_computer_extension_attribute" "battery_cycle_count" {
  name       = "Battery Cycle Count"
  enabled    = true
  input_type = "script"
  data_type  = "Integer"

  input_script = <<-EOT
    #!/bin/bash
    system_profiler SPPowerDataType | grep "Cycle Count" | awk '{print $3}'
  EOT
}
```

---

### **6. Organizational Resources**

#### `jamfpro_building`

**REQUIRED FIELDS:**

- `name` (String) - Building name

**Example:**

```hcl
resource "jamfpro_building" "hq" {
  name = "Headquarters"
}
```

#### `jamfpro_department`

**REQUIRED FIELDS:**

- `name` (String) - Department name

**Example:**

```hcl
resource "jamfpro_department" "it" {
  name = "Information Technology"
}
```

#### `jamfpro_category`

**REQUIRED FIELDS:**

- `name` (String) - Category name

**Example:**

```hcl
resource "jamfpro_category" "productivity" {
  name = "Productivity Apps"
}
```

---

### **7. Mobile Device Groups**

#### `jamfpro_mobile_device_group`

**REQUIRED FIELDS:**

- `name` (String) - Group name

**Example:**

```hcl
resource "jamfpro_mobile_device_group" "ipads" {
  name = "All iPads"
}
```

---

### **8. Network & Infrastructure**

#### `jamfpro_network_segment`

**REQUIRED FIELDS:**

- `name` (String) - Segment name
- `starting_address` (String) - Starting IP
- `ending_address` (String) - Ending IP

**Example:**

```hcl
resource "jamfpro_network_segment" "office" {
  name              = "Office Network"
  starting_address  = "192.168.1.1"
  ending_address    = "192.168.1.254"
}
```

#### `jamfpro_dock_item`

**REQUIRED FIELDS:**

- `name` (String) - Dock item name
- `path` (String) - Application path

**Example:**

```hcl
resource "jamfpro_dock_item" "chrome" {
  name = "Google Chrome"
  path = "/Applications/Google Chrome.app"
}
```

---

### **9. Accounts & Access**

#### `jamfpro_account`

**REQUIRED FIELDS:**

- `name` (String) - Account username
- `access_level` (String) - Access level
- `privilege_set` (String) - Privilege set name

**Example:**

```hcl
resource "jamfpro_account" "admin" {
  name          = "admin_user"
  access_level  = "Full Access"
  privilege_set = "Administrator"
}
```

#### `jamfpro_account_group`

**REQUIRED FIELDS:**

- `name` (String) - Group name
- `access_level` (String) - Access level

---

### **10. Advanced Searches**

#### `jamfpro_advanced_computer_search`

**REQUIRED FIELDS:**

- `name` (String) - Search name
- `criteria` (Block) - Search criteria

**Example:**

```hcl
resource "jamfpro_advanced_computer_search" "outdated_os" {
  name = "Outdated macOS Versions"

  criteria {
    name        = "Operating System Version"
    search_type = "less than"
    value       = "14.0"
  }
}
```

#### `jamfpro_advanced_mobile_device_search`

**REQUIRED FIELDS:**

- `name` (String) - Search name
- `criteria` (Block) - Search criteria

#### `jamfpro_advanced_user_search`

**REQUIRED FIELDS:**

- `name` (String) - Search name
- `criteria` (Block) - Search criteria

---

### **11. Applications**

#### `jamfpro_mac_application`

**REQUIRED FIELDS:**

- `name` (String) - Application name

**Example:**

```hcl
resource "jamfpro_mac_application" "slack" {
  name = "Slack"
}
```

#### `jamfpro_mobile_device_application`

**REQUIRED FIELDS:**

- `name` (String) - Application name
- `bundle_id` (String) - App bundle identifier

**Example:**

```hcl
resource "jamfpro_mobile_device_application" "zoom" {
  name      = "Zoom"
  bundle_id = "us.zoom.videomeetings"
}
```

---

### **12. Enrollment & Prestage**

#### `jamfpro_computer_prestage_enrollment`

**REQUIRED FIELDS:**

- `display_name` (String) - Prestage name
- `is_mandatory` (Boolean) - Whether mandatory
- `is_mdm_removable` (Boolean) - Whether MDM is removable
- `support_phone_number` (String) - Support phone
- `support_email_address` (String) - Support email
- `department` (String) - Department name
- `is_default_prestage` (Boolean) - Whether default

**Example:**

```hcl
resource "jamfpro_computer_prestage_enrollment" "standard" {
  display_name           = "Standard Enrollment"
  is_mandatory           = true
  is_mdm_removable       = false
  support_phone_number   = "555-1234"
  support_email_address  = "support@company.com"
  department             = "IT"
  is_default_prestage    = true
}
```

#### `jamfpro_mobile_device_prestage_enrollment`

**REQUIRED FIELDS:**

- Same as computer prestage enrollment

---

### **13. API & Integrations**

#### `jamfpro_api_integration`

**REQUIRED FIELDS:**

- `display_name` (String) - Integration name
- `enabled` (Boolean) - Whether enabled

**Example:**

```hcl
resource "jamfpro_api_integration" "sso" {
  display_name = "SSO Integration"
  enabled      = true
}
```

#### `jamfpro_api_role`

**REQUIRED FIELDS:**

- `display_name` (String) - Role name
- `privileges` (List) - List of privileges

---

### **14. Security & Encryption**

#### `jamfpro_disk_encryption_configuration`

**REQUIRED FIELDS:**

- `name` (String) - Configuration name
- `key_type` (String) - "Individual" or "Institutional"
- `file_vault_enabled_users` (String) - User type

**Example:**

```hcl
resource "jamfpro_disk_encryption_configuration" "filevault" {
  name                      = "FileVault Configuration"
  key_type                  = "Individual"
  file_vault_enabled_users  = "Management Account"
}
```

---

### **15. Printers**

#### `jamfpro_printer`

**REQUIRED FIELDS:**

- `name` (String) - Printer name
- `uri` (String) - Printer URI
- `ppd` (String) - PPD file path

**Example:**

```hcl
resource "jamfpro_printer" "office_printer" {
  name = "Office Printer"
  uri  = "lpd://192.168.1.100"
  ppd  = "/Library/Printers/PPDs/Contents/Resources/HP LaserJet.ppd"
}
```

---

### **16. LDAP & Directory Services**

#### `jamfpro_ldap_server`

**REQUIRED FIELDS:**

- `name` (String) - Server name
- `hostname` (String) - LDAP hostname
- `port` (Number) - LDAP port
- `use_ssl` (Boolean) - Whether to use SSL

**Example:**

```hcl
resource "jamfpro_ldap_server" "ad" {
  name     = "Active Directory"
  hostname = "ad.company.com"
  port     = 636
  use_ssl  = true
}
```

---

## 📊 **Summary Table**

| Resource                                    | Key Required Fields                                                                                                                      |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `jamfpro_policy`                            | `name`, `enabled`, `payloads`, `scope`                                                                                                   |
| `jamfpro_computer_group`                    | `name`                                                                                                                                   |
| `jamfpro_smart_computer_group`              | `name`, `is_smart`, `criteria`                                                                                                           |
| `jamfpro_macos_configuration_profile_plist` | `name`, `description`, `distribution_method`, `level`, `payloads`                                                                        |
| `jamfpro_package`                           | `package_file_source`, `filename`                                                                                                        |
| `jamfpro_script`                            | `name`, `script_contents`                                                                                                                |
| `jamfpro_computer_extension_attribute`      | `name`, `enabled`, `input_type`                                                                                                          |
| `jamfpro_building`                          | `name`                                                                                                                                   |
| `jamfpro_department`                        | `name`                                                                                                                                   |
| `jamfpro_category`                          | `name`                                                                                                                                   |
| `jamfpro_network_segment`                   | `name`, `starting_address`, `ending_address`                                                                                             |
| `jamfpro_dock_item`                         | `name`, `path`                                                                                                                           |
| `jamfpro_account`                           | `name`, `access_level`, `privilege_set`                                                                                                  |
| `jamfpro_advanced_computer_search`          | `name`, `criteria`                                                                                                                       |
| `jamfpro_mac_application`                   | `name`                                                                                                                                   |
| `jamfpro_mobile_device_application`         | `name`, `bundle_id`                                                                                                                      |
| `jamfpro_computer_prestage_enrollment`      | `display_name`, `is_mandatory`, `is_mdm_removable`, `support_phone_number`, `support_email_address`, `department`, `is_default_prestage` |
| `jamfpro_api_integration`                   | `display_name`, `enabled`                                                                                                                |
| `jamfpro_disk_encryption_configuration`     | `name`, `key_type`, `file_vault_enabled_users`                                                                                           |
| `jamfpro_printer`                           | `name`, `uri`, `ppd`                                                                                                                     |
| `jamfpro_ldap_server`                       | `name`, `hostname`, `port`, `use_ssl`                                                                                                    |

---

## 🔍 **Common Patterns**

### Pattern 1: Name-Only Resources

Many organizational resources only require a `name`:

- `jamfpro_building`
- `jamfpro_department`
- `jamfpro_category`
- `jamfpro_computer_group`

### Pattern 2: Name + Configuration

Resources that need name plus specific config:

- `jamfpro_policy` (+ payloads, scope)
- `jamfpro_script` (+ script_contents)
- `jamfpro_package` (+ package_file_source)

### Pattern 3: Smart/Dynamic Resources

Resources with criteria/search logic:

- `jamfpro_smart_computer_group` (+ criteria)
- `jamfpro_advanced_*_search` (+ criteria)

---

## 💡 **Recommendations for System Prompt**

Based on this analysis, the system prompt should include:

1. **Always include terraform + provider blocks**
2. **Resource-specific templates** for top 10 most common resources
3. **Payload requirements** for policies and profiles
4. **Scope requirements** with `all_computers = true` default
5. **Criteria structure** for smart groups and searches

---

**Last Updated**: 2025-12-04  
**Provider Version**: 0.1.x  
**Source**: Terraform Registry + Provider Documentation
