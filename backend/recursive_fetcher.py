import asyncio
from typing import Dict, List, Set, Tuple
from jamf_client import JamfClient
from dependency_resolver import DependencyResolver

class RecursiveFetcher:
    """Fetches a resource and all its dependencies recursively."""
    
    def __init__(self, client: JamfClient):
        self.client = client
        self.resolver = DependencyResolver()
        self.fetched_resources: Dict[Tuple[str, int], dict] = {}
        self.processing_queue: List[Tuple[str, int]] = []
        self.visited: Set[Tuple[str, int]] = set()

    async def fetch_all(self, root_type: str, root_id: int) -> List[Tuple[str, dict]]:
        """
        Fetch resource and all dependencies.
        Returns list of (type, data) tuples.
        """
        # Clear state
        self.fetched_resources = {}
        self.visited = set()
        
        # Start with root
        await self._fetch_node(root_type, root_id)
        
        # Return as list
        return [(t, d) for (t, i), d in self.fetched_resources.items()]

    async def _fetch_node(self, resource_type: str, resource_id: int):
        key = (resource_type, resource_id)
        if key in self.visited:
            return
        
        self.visited.add(key)
        
        # Fetch details
        try:
            data = await self._get_resource_detail(resource_type, resource_id)
            self.fetched_resources[key] = data
            
            # Extract dependencies
            deps = self.resolver.extract_dependencies(resource_type, data)
            
            # Recurse for each dependency
            tasks = []
            for dep_type, dep_ids in deps.items():
                for dep_id in dep_ids:
                    if (dep_type, dep_id) not in self.visited:
                        tasks.append(self._fetch_node(dep_type, dep_id))
            
            if tasks:
                await asyncio.gather(*tasks)
                
        except Exception as e:
            print(f"Error fetching {resource_type} {resource_id}: {e}")
            # Continue even if one dep fails?
            return

    async def _get_resource_detail(self, resource_type: str, resource_id: int) -> dict:
        """Helper to call correct client method."""
        if resource_type == "policies":
            return await self.client.get_policy_detail(resource_id)
        elif resource_type == "scripts":
            return await self.client.get_script_detail(resource_id)
        elif resource_type == "packages":
            return await self.client.get_package_detail(resource_id)
        elif resource_type == "smart-groups":
            return await self.client.get_computer_group_detail(resource_id)
        elif resource_type == "config-profiles":
            return await self.client.get_configuration_profile_detail(resource_id)
        elif resource_type == "jamf-app-catalog":
            return await self.client.get_jamf_app_catalog_detail(resource_id)
        elif resource_type == "categories":
            return await self.client.get_category_detail(resource_id)
        elif resource_type == "buildings":
            return await self.client.get_building_detail(resource_id)
        elif resource_type == "computer_groups" or resource_type == "smart-groups":
            return await self.client.get_computer_group_detail(resource_id)
        # Add categories and others if needed
        # Categories often don't have a specific detail endpoint used here, 
        # but we might need list_categories to look up ID? 
        # Actually JamfClient usually lacks get_category_detail.
        # I should add it or handle it.
        # For now, if generic, skip?
        raise ValueError(f"Unsupported type for detail fetch: {resource_type}")
