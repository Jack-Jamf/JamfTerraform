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
    
    async def get_auth_token(self) -> str:
        """
        Get bearer token using basic auth.
        
        Returns:
            Bearer token string
        """
        auth_url = f"{self.base_url}/api/v1/auth/token"
        credentials = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
        
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            response = await client.post(
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
        
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            response = await client.get(url, headers=self._get_headers())
            
            if response.status_code != 200:
                raise ValueError(f"Failed to fetch policies: {response.status_code}")
            
            data = response.json()
            return data.get("policies", [])
    
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
            resource_type: One of 'policies', 'smart-groups', 'config-profiles', 'scripts', 'packages'
            
        Returns:
            List of resource objects
        """
        if not self._token:
            await self.get_auth_token()
        
        resource_methods = {
            "policies": self.list_policies,
            "smart-groups": self.list_computer_groups,
            "config-profiles": self.list_configuration_profiles,
            "scripts": self.list_scripts,
            "packages": self.list_packages,
            "jamf-app-catalog": self.list_jamf_app_catalog,
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
        resources["smart-groups"] = await self.list_computer_groups()
        
        return resources
