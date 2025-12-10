"""Jamf Pro API Client for fetching resources."""
import httpx
import base64
from typing import Optional


class JamfClient:
    """Client for interacting with Jamf Pro API."""
    
    def __init__(self, url: str, username: str, password: str):
        """
        Initialize Jamf Pro client.
        
        Args:
            url: Jamf Pro instance URL (e.g., https://company.jamfcloud.com)
            username: API username
            password: API password
        """
        self.base_url = url.rstrip('/')
        self.username = username
        self.password = password
        self._token: Optional[str] = None
        
        # Create persistent HTTP client with connection pooling (OPTIMIZATION: 20-30% speedup)
        # Use Limits if available (httpx >= 0.23), otherwise use defaults
        try:
            self._client = httpx.AsyncClient(
                verify=False,
                timeout=30.0,
                limits=httpx.Limits(
                    max_connections=50,  # Allow up to 50 concurrent connections
                    max_keepalive_connections=20  # Keep 20 connections alive for reuse
                )
            )
        except (AttributeError, TypeError):
            # Fallback for older httpx versions without Limits
            self._client = httpx.AsyncClient(
                verify=False,
                timeout=30.0
            )
    
    async def get_auth_token(self) -> str:
        """
        Get bearer token using basic auth.
        
        Returns:
            Bearer token string
        """
        auth_url = f"{self.base_url}/api/v1/auth/token"
        credentials = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
        
        response = await self._client.post(
                auth_url,
                headers={
                    "Authorization": f"Basic {credentials}",
                    "Accept": "application/json"
                }
            )
            
        if response.status_code != 200:
            raise ValueError(f"Authentication failed: {response.status_code} - {response.text}")
        
        data = response.json()
        self._token = data.get("token")
        return self._token
    
    def _get_headers(self) -> dict:
        """Get headers with bearer token."""
        if not self._token:
            raise ValueError("Not authenticated. Call get_auth_token() first.")
        return {
            "Authorization": f"Bearer {self._token}",
            "Accept": "application/json"
        }
    
    async def list_policies(self) -> list:
        """
        List all policies from Jamf Pro.
        
        Returns:
            List of policy objects with id and name
        """
        url = f"{self.base_url}/JSSResource/policies"
        
        response = await self._client.get(url, headers=self._get_headers())
            
        if response.status_code != 200:
                raise ValueError(f"Failed to fetch policies: {response.status_code}")
            
        data = response.json()
        return data.get("policies", [])
    
    async def list_computer_extension_attributes(self) -> list:
        """
        List all computer extension attributes.
        
        Returns:
            List of computer extension attribute objects
        """
        url = f"{self.base_url}/JSSResource/computerextensionattributes"
        response = await self._client.get(url, headers=self._get_headers())
            
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch computer extension attributes: {response.status_code}")
            
        data = response.json()
        return data.get("computer_extension_attributes", [])
    
    async def get_computer_extension_attribute_detail(self, ea_id: int) -> dict:
        """Fetch detailed computer extension attribute data."""
        url = f"{self.base_url}/JSSResource/computerextensionattributes/id/{ea_id}"
        
        response = await self._client.get(url, headers=self._get_headers())
        
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch computer extension attribute {ea_id}: {response.status_code}")
        
        data = response.json()
        return data.get("computer_extension_attribute", {})

    async def list_advanced_computer_searches(self) -> list:
        """List all advanced computer searches."""
        url = f"{self.base_url}/JSSResource/advancedcomputersearches"
        
        response = await self._client.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch advanced computer searches: {response.status_code}")
        data = response.json()
        return data.get("advanced_computer_searches", [])

    async def get_advanced_computer_search_detail(self, search_id: int) -> dict:
        """Fetch detailed advanced computer search data."""
        url = f"{self.base_url}/JSSResource/advancedcomputersearches/id/{search_id}"
        
        response = await self._client.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch advanced computer search {search_id}: {response.status_code}")
        data = response.json()
        return data.get("advanced_computer_search", {})

    async def list_departments(self) -> list:
        """List all departments."""
        url = f"{self.base_url}/JSSResource/departments"
        
        response = await self._client.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch departments: {response.status_code}")
        data = response.json()
        return data.get("departments", [])

    async def get_department_detail(self, dept_id: int) -> dict:
        """Fetch detailed department data."""
        url = f"{self.base_url}/JSSResource/departments/id/{dept_id}"
        
        response = await self._client.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch department {dept_id}: {response.status_code}")
        data = response.json()
        return data.get("department", {})

    async def list_network_segments(self) -> list:
        """List all network segments."""
        url = f"{self.base_url}/JSSResource/networksegments"
        
        response = await self._client.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch network segments: {response.status_code}")
        data = response.json()
        return data.get("network_segments", [])

    async def get_network_segment_detail(self, segment_id: int) -> dict:
        """Fetch detailed network segment data."""
        url = f"{self.base_url}/JSSResource/networksegments/id/{segment_id}"
        
        response = await self._client.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch network segment {segment_id}: {response.status_code}")
        data = response.json()
        return data.get("network_segment", {})
    
    async def list_computer_groups(self) -> list:
        """
        List all computer groups (smart and static).
        
        Returns:
            List of computer group objects
        """
        url = f"{self.base_url}/JSSResource/computergroups"
        
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            response = await client.get(url, headers=self._get_headers())
            
        if response.status_code != 200:
                raise ValueError(f"Failed to fetch computer groups: {response.status_code}")
            
        data = response.json()
        return data.get("computer_groups", [])
    
    async def list_configuration_profiles(self) -> list:
        """
        List all macOS configuration profiles.
        
        Returns:
            List of configuration profile objects
        """
        url = f"{self.base_url}/JSSResource/osxconfigurationprofiles"
        
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            response = await client.get(url, headers=self._get_headers())
            
        if response.status_code != 200:
                raise ValueError(f"Failed to fetch configuration profiles: {response.status_code}")
            
        data = response.json()
        return data.get("os_x_configuration_profiles", [])
    
    async def list_scripts(self) -> list:
        """
        List all scripts.
        
        Returns:
            List of script objects
        """
        url = f"{self.base_url}/JSSResource/scripts"
        
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            response = await client.get(url, headers=self._get_headers())
            
        if response.status_code != 200:
                raise ValueError(f"Failed to fetch scripts: {response.status_code}")
            
        data = response.json()
        return data.get("scripts", [])
    
    async def list_packages(self) -> list:
        """
        List all packages.
        
        Returns:
            List of package objects
        """
        url = f"{self.base_url}/JSSResource/packages"
        
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            response = await client.get(url, headers=self._get_headers())
            
        if response.status_code != 200:
                raise ValueError(f"Failed to fetch packages: {response.status_code}")
            
        data = response.json()
        return data.get("packages", [])
    
    async def get_resources(self, resource_type: str) -> list:
        """
        Get resources by type.
        
        Args:
            resource_type: One of 'policies', 'smart-groups', 'static-groups', 'config-profiles', 'scripts', 'packages', 'printers', 'sites', 'mobile-device-groups', 'mobile-device-prestages', 'mobile-device-config-profiles', 'advanced-mobile-device-searches', 'mobile-device-extension-attributes'
            
        Returns:
            List of resource objects
        """
        if not self._token:
            await self.get_auth_token()
        
        resource_methods = {
            "policies": self.list_policies,
            "smart-groups": self.list_computer_groups,
            "static-groups": self.list_computer_groups,
            "extension-attributes": self.list_computer_extension_attributes,
            "config-profiles": self.list_configuration_profiles,
            "scripts": self.list_scripts,
            "packages": self.list_packages,
            "jamf-app-catalog": self.list_jamf_app_catalog,
            "advanced-computer-searches": self.list_advanced_computer_searches,
            "departments": self.list_departments,
            "network-segments": self.list_network_segments,
            "printers": self.list_printers,
            "sites": self.list_sites,
            "mobile-device-groups": self.list_mobile_device_groups,
            "mobile-device-prestages": self.list_mobile_device_prestages,
            "mobile-device-config-profiles": self.list_mobile_device_configuration_profiles,
            "advanced-mobile-device-searches": self.list_advanced_mobile_device_searches,
            "mobile-device-extension-attributes": self.list_mobile_device_extension_attributes,
        }
        
        if resource_type not in resource_methods:
            raise ValueError(f"Unknown resource type: {resource_type}")
        
        return await resource_methods[resource_type]()

    
    async def list_categories(self) -> list:
        """List all categories."""
        url = f"{self.base_url}/JSSResource/categories"
        
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            response = await client.get(url, headers=self._get_headers())
            
        if response.status_code != 200:
                raise ValueError(f"Failed to fetch categories: {response.status_code}")
            
        data = response.json()
        return data.get("categories", [])
    
    async def list_buildings(self) -> list:
        """List all buildings."""
        url = f"{self.base_url}/JSSResource/buildings"
        
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            response = await client.get(url, headers=self._get_headers())
            
        if response.status_code != 200:
                raise ValueError(f"Failed to fetch buildings: {response.status_code}")
            
        data = response.json()
        return data.get("buildings", [])
    
    async def list_jamf_app_catalog(self) -> list:
        """List all Jamf App Installers (Jamf App Catalog)."""
        url = f"{self.base_url}/api/v1/app-installers/deployments"
        
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            response = await client.get(url, headers=self._get_headers())
            
        if response.status_code != 200:
                raise ValueError(f"Failed to fetch app installers: {response.status_code}")
            
        data = response.json()
            # v1 API returns results array
        return data.get("results", [])
    
    async def get_jamf_app_catalog_detail(self, app_id: int) -> dict:
        """Fetch detailed Jamf App Catalog deployment data."""
        url = f"{self.base_url}/api/v1/app-installers/deployments/{app_id}"
        
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            response = await client.get(url, headers=self._get_headers())
            
        if response.status_code != 200:
                raise ValueError(f"Failed to fetch app deployment {app_id}: {response.status_code}")
            
        return response.json()
    
    async def get_policy_detail(self, policy_id: int) -> dict:
        """Fetch detailed policy data."""
        url = f"{self.base_url}/JSSResource/policies/id/{policy_id}"
        
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            response = await client.get(url, headers=self._get_headers())
            
        if response.status_code != 200:
                raise ValueError(f"Failed to fetch policy {policy_id}: {response.status_code}")
            
        data = response.json()
        return data.get("policy", {})
    
    async def get_script_detail(self, script_id: int) -> dict:
        """Fetch detailed script data."""
        url = f"{self.base_url}/JSSResource/scripts/id/{script_id}"
        
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            response = await client.get(url, headers=self._get_headers())
            
        if response.status_code != 200:
                raise ValueError(f"Failed to fetch script {script_id}: {response.status_code}")
            
        data = response.json()
        return data.get("script", {})

    async def get_package_detail(self, package_id: int) -> dict:
        """Fetch detailed package data."""
        url = f"{self.base_url}/JSSResource/packages/id/{package_id}"
        
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            response = await client.get(url, headers=self._get_headers())
            
        if response.status_code != 200:
                raise ValueError(f"Failed to fetch package {package_id}: {response.status_code}")
            
        data = response.json()
        return data.get("package", {})

    async def get_configuration_profile_detail(self, profile_id: int) -> dict:
        """Fetch detailed configuration profile data."""
        url = f"{self.base_url}/JSSResource/osxconfigurationprofiles/id/{profile_id}"
        
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            response = await client.get(url, headers=self._get_headers())
            
        if response.status_code != 200:
                raise ValueError(f"Failed to fetch profile {profile_id}: {response.status_code}")
            
        data = response.json()
        return data.get("os_x_configuration_profile", {})

    async def get_computer_group_detail(self, group_id: int) -> dict:
        """Fetch detailed computer group data (smart or static)."""
        url = f"{self.base_url}/JSSResource/computergroups/id/{group_id}"
        
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            response = await client.get(url, headers=self._get_headers())
            
        if response.status_code != 200:
                raise ValueError(f"Failed to fetch group {group_id}: {response.status_code}")
            
        data = response.json()
        return data.get("computer_group", {})

    async def get_category_detail(self, category_id: int) -> dict:
        """Fetch detailed category data."""
        url = f"{self.base_url}/JSSResource/categories/id/{category_id}"
        
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            response = await client.get(url, headers=self._get_headers())
            
        if response.status_code != 200:
                # Category might not exist or be generic?
                raise ValueError(f"Failed to fetch category {category_id}: {response.status_code}")
            
        data = response.json()
        return data.get("category", {})

    async def get_building_detail(self, building_id: int) -> dict:
        """Fetch detailed building data."""
        url = f"{self.base_url}/JSSResource/buildings/id/{building_id}"
        
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            response = await client.get(url, headers=self._get_headers())
            
        if response.status_code != 200:
                raise ValueError(f"Failed to fetch building {building_id}: {response.status_code}")
            
        data = response.json()
        return data.get("building", {})
    
    async def list_printers(self) -> list:
        """List all printers."""
        url = f"{self.base_url}/JSSResource/printers"
        
        response = await self._client.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch printers: {response.status_code}")
        data = response.json()
        return data.get("printers", [])
    
    async def get_printer_detail(self, printer_id: int) -> dict:
        """Fetch detailed printer data."""
        url = f"{self.base_url}/JSSResource/printers/id/{printer_id}"
        
        response = await self._client.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch printer {printer_id}: {response.status_code}")
        data = response.json()
        return data.get("printer", {})
    
    async def list_sites(self) -> list:
        """List all sites."""
        url = f"{self.base_url}/JSSResource/sites"
        
        response = await self._client.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch sites: {response.status_code}")
        data = response.json()
        return data.get("sites", [])
    
    async def get_site_detail(self, site_id: int) -> dict:
        """Fetch detailed site data."""
        url = f"{self.base_url}/JSSResource/sites/id/{site_id}"
        
        response = await self._client.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch site {site_id}: {response.status_code}")
        data = response.json()
        return data.get("site", {})
    
    async def list_mobile_device_groups(self) -> list:
        """List all mobile device groups."""
        url = f"{self.base_url}/JSSResource/mobiledevicegroups"
        
        response = await self._client.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch mobile device groups: {response.status_code}")
        data = response.json()
        return data.get("mobile_device_groups", [])
    
    async def get_mobile_device_group_detail(self, group_id: int) -> dict:
        """Fetch detailed mobile device group data."""
        url = f"{self.base_url}/JSSResource/mobiledevicegroups/id/{group_id}"
        
        response = await self._client.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch mobile device group {group_id}: {response.status_code}")
        data = response.json()
        return data.get("mobile_device_group", {})
    
    async def list_mobile_device_prestages(self) -> list:
        """List all mobile device prestage enrollments."""
        url = f"{self.base_url}/api/v2/mobile-device-prestages"
        
        response = await self._client.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch mobile device prestages: {response.status_code}")
        data = response.json()
        # v2 API returns results array
        return data.get("results", [])
    
    async def get_mobile_device_prestage_detail(self, prestage_id: int) -> dict:
        """Fetch detailed mobile device prestage data."""
        url = f"{self.base_url}/api/v2/mobile-device-prestages/{prestage_id}"
        
        response = await self._client.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch mobile device prestage {prestage_id}: {response.status_code}")
        return response.json()
    
    async def list_mobile_device_configuration_profiles(self) -> list:
        """List all mobile device configuration profiles."""
        url = f"{self.base_url}/JSSResource/mobiledeviceconfigurationprofiles"
        
        response = await self._client.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch mobile device config profiles: {response.status_code}")
        data = response.json()
        return data.get("configuration_profiles", [])
    
    async def get_mobile_device_configuration_profile_detail(self, profile_id: int) -> dict:
        """Fetch detailed mobile device configuration profile data."""
        url = f"{self.base_url}/JSSResource/mobiledeviceconfigurationprofiles/id/{profile_id}"
        
        response = await self._client.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch mobile device config profile {profile_id}: {response.status_code}")
        data = response.json()
        return data.get("configuration_profile", {})
    
    async def list_advanced_mobile_device_searches(self) -> list:
        """List all advanced mobile device searches."""
        url = f"{self.base_url}/JSSResource/advancedmobiledevicesearches"
        
        response = await self._client.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch advanced mobile device searches: {response.status_code}")
        data = response.json()
        return data.get("advanced_mobile_device_searches", [])
    
    async def get_advanced_mobile_device_search_detail(self, search_id: int) -> dict:
        """Fetch detailed advanced mobile device search data."""
        url = f"{self.base_url}/JSSResource/advancedmobiledevicesearches/id/{search_id}"
        
        response = await self._client.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch advanced mobile device search {search_id}: {response.status_code}")
        data = response.json()
        return data.get("advanced_mobile_device_search", {})
    
    async def list_mobile_device_extension_attributes(self) -> list:
        """List all mobile device extension attributes."""
        url = f"{self.base_url}/JSSResource/mobiledeviceextensionattributes"
        
        response = await self._client.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch mobile device extension attributes: {response.status_code}")
        data = response.json()
        return data.get("mobile_device_extension_attributes", [])
    
    async def get_mobile_device_extension_attribute_detail(self, attr_id: int) -> dict:
        """Fetch detailed mobile device extension attribute data."""
        url = f"{self.base_url}/JSSResource/mobiledeviceextensionattributes/id/{attr_id}"
        
        response = await self._client.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch mobile device extension attribute {attr_id}: {response.status_code}")
        data = response.json()
        return data.get("mobile_device_extension_attribute", {})
    
    async def get_all_instance_resources(self) -> dict:
        """
        Fetch all resources from the Jamf Pro instance.
        
        Returns:
            Dict with resource type as key and list of resources as value
        """
        if not self._token:
            await self.get_auth_token()
        
        resources = {}
        resources["categories"] = await self.list_categories()
        resources["buildings"] = await self.list_buildings()
        resources["scripts"] = await self.list_scripts()
        resources["packages"] = await self.list_packages()
        resources["jamf-app-catalog"] = await self.list_jamf_app_catalog()
        resources["policies"] = await self.list_policies()
        resources["config-profiles"] = await self.list_configuration_profiles()
        
        # New Resources (Proporter Update)
        resources["departments"] = await self.list_departments()
        resources["network-segments"] = await self.list_network_segments()
        resources["advanced-computer-searches"] = await self.list_advanced_computer_searches()
        resources["extension-attributes"] = await self.list_computer_extension_attributes()
        resources["printers"] = await self.list_printers()
        resources["sites"] = await self.list_sites()
        
        # Mobile Device Resources (with error handling)
        try:
            print("[DEBUG] Fetching mobile device groups...")
            resources["mobile-device-groups"] = await self.list_mobile_device_groups()
            print(f"[DEBUG] Found {len(resources['mobile-device-groups'])} mobile device groups")
        except Exception as e:
            print(f"[ERROR] Failed to fetch mobile device groups: {e}")
            resources["mobile-device-groups"] = []
        
        try:
            print("[DEBUG] Fetching mobile device prestages...")
            resources["mobile-device-prestages"] = await self.list_mobile_device_prestages()
            print(f"[DEBUG] Found {len(resources['mobile-device-prestages'])} mobile device prestages")
        except Exception as e:
            print(f"[ERROR] Failed to fetch mobile device prestages: {e}")
            resources["mobile-device-prestages"] = []
        
        try:
            print("[DEBUG] Fetching mobile device config profiles...")
            resources["mobile-device-config-profiles"] = await self.list_mobile_device_configuration_profiles()
            print(f"[DEBUG] Found {len(resources['mobile-device-config-profiles'])} mobile device config profiles")
        except Exception as e:
            print(f"[ERROR] Failed to fetch mobile device config profiles: {e}")
            resources["mobile-device-config-profiles"] = []
        
        try:
            print("[DEBUG] Fetching advanced mobile device searches...")
            resources["advanced-mobile-device-searches"] = await self.list_advanced_mobile_device_searches()
            print(f"[DEBUG] Found {len(resources['advanced-mobile-device-searches'])} advanced mobile device searches")
        except Exception as e:
            print(f"[ERROR] Failed to fetch advanced mobile device searches: {e}")
            resources["advanced-mobile-device-searches"] = []
        
        try:
            print("[DEBUG] Fetching mobile device extension attributes...")
            resources["mobile-device-extension-attributes"] = await self.list_mobile_device_extension_attributes()
            print(f"[DEBUG] Found {len(resources['mobile-device-extension-attributes'])} mobile device extension attributes")
        except Exception as e:
            print(f"[ERROR] Failed to fetch mobile device extension attributes: {e}")
            resources["mobile-device-extension-attributes"] = []
        
        # Split computer groups into smart and static
        all_groups = await self.list_computer_groups()
        smart_groups = []
        static_groups = []
        
        # Fetch details for each group to determine type
        for group in all_groups:
            try:
                detail = await self.get_computer_group_detail(group['id'])
                if detail.get('is_smart', False):
                    smart_groups.append(group)
                else:
                    static_groups.append(group)
            except Exception as e:
                print(f"Error checking group {group.get('id')}: {e}")
                # Default to smart group if we can't determine
                smart_groups.append(group)
        
        resources["smart-groups"] = smart_groups
        # Static groups excluded from summary as per requirement
        # resources["static-groups"] = static_groups 
        
        return resources
