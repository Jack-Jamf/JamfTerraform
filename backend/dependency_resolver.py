"""Dependency resolver for Jamf Pro resources."""
from typing import Dict, List, Set, Any
from collections import defaultdict, deque


class DependencyResolver:
    """Analyzes Jamf Pro resources and resolves dependencies."""
    
    # Define which resource types can have dependencies on other types
    DEPENDENCY_MAP = {
        'policies': ['categories', 'scripts', 'packages', 'buildings', 'smart-groups'],
        'config-profiles': ['categories'],
        'smart-groups': ['smart-groups'],  # Can reference other groups in criteria
    }
    
    def __init__(self):
        self.dependency_graph: Dict[str, Set[str]] = defaultdict(set)
    
    def extract_dependencies(self, resource_type: str, resource_data: dict) -> Dict[str, List[int]]:
        """
        Extract dependency IDs from a resource's data.
        
        Args:
            resource_type: Type of resource (e.g., 'policies')
            resource_data: Full resource data from Jamf API
            
        Returns:
            Dictionary mapping dependency types to lists of IDs
            Example: {'categories': [5], 'scripts': [10, 12], 'packages': [3]}
        """
        dependencies = defaultdict(list)
        
        if resource_type == 'policies':
            dependencies.update(self._extract_policy_deps(resource_data))
        elif resource_type == 'config-profiles':
            dependencies.update(self._extract_config_profile_deps(resource_data))
        elif resource_type == 'smart-groups':
            dependencies.update(self._extract_smart_group_deps(resource_data))
        
        return dict(dependencies)
    
    def _extract_policy_deps(self, policy_data: dict) -> Dict[str, List[int]]:
        """Extract dependencies from a policy."""
        deps = defaultdict(list)
        
        # Category
        if 'general' in policy_data and 'category' in policy_data['general']:
            category = policy_data['general']['category']
            if isinstance(category, dict) and 'id' in category:
                if category['id'] not in [-1, 0]:  # Skip "No category"
                    deps['categories'].append(category['id'])
        
        # Scripts (from payloads)
        if 'scripts' in policy_data:
            scripts = policy_data['scripts']
            if isinstance(scripts, list):
                for script in scripts:
                    if isinstance(script, dict) and 'id' in script:
                        script_id = int(script['id']) if script['id'] not in ['', None] else None
                        if script_id and script_id not in [-1, 0]:
                            deps['scripts'].append(script_id)
        
        # Packages
        if 'package_configuration' in policy_data:
            packages = policy_data['package_configuration'].get('packages', [])
            if isinstance(packages, list):
                for package in packages:
                    if isinstance(package, dict) and 'id' in package:
                        pkg_id = int(package['id']) if package['id'] not in ['', None] else None
                        if pkg_id and pkg_id not in [-1, 0]:
                            deps['packages'].append(pkg_id)
        
        # Scope - Buildings
        if 'scope' in policy_data:
            scope = policy_data['scope']
            if isinstance(scope, dict):
                # Buildings
                buildings = scope.get('buildings', [])
                if isinstance(buildings, list):
                    for building in buildings:
                        if isinstance(building, dict) and 'id' in building:
                            bldg_id = int(building['id']) if building['id'] not in ['', None] else None
                            if bldg_id and bldg_id not in [-1, 0]:
                                deps['buildings'].append(bldg_id)
                
                # Computer Groups (normalize to smart-groups type)
                computer_groups = scope.get('computer_groups', [])
                if isinstance(computer_groups, list):
                    for group in computer_groups:
                        if isinstance(group, dict) and 'id' in group:
                            grp_id = int(group['id']) if group['id'] not in ['', None] else None
                            if grp_id and grp_id not in [-1, 0]:
                                deps['smart-groups'].append(grp_id)
        
        return deps
    
    def _extract_config_profile_deps(self, profile_data: dict) -> Dict[str, List[int]]:
        """Extract dependencies from a configuration profile."""
        deps = defaultdict(list)
        
        # Category
        if 'general' in profile_data and 'category' in profile_data['general']:
            category = profile_data['general']['category']
            if isinstance(category, dict) and 'id' in category:
                if category['id'] not in [-1, 0]:
                    deps['categories'].append(category['id'])
        
        return deps
    
    def _extract_smart_group_deps(self, group_data: dict) -> Dict[str, List[int]]:
        """Extract dependencies from a smart computer group (can reference other groups)."""
        deps = defaultdict(list)
        
        # Check criteria for group references
        if 'criteria' in group_data:
            criteria = group_data['criteria']
            if isinstance(criteria, list):
                for criterion in criteria:
                    if isinstance(criterion, dict):
                        # Smart groups can have criteria like "member of group X"
                        if criterion.get('name') == 'Computer Group' and 'value' in criterion:
                            # This would need parsing of the value to get group ID
                            # For now, skip circular dependency handling
                            pass
        
        return deps
    
    def topological_sort(self, resources_by_type: Dict[str, List[dict]]) -> List[tuple]:
        """
        Sort resources in dependency order using topological sort.
        
        Args:
            resources_by_type: Dict mapping resource type to list of resources
                Example: {'categories': [...], 'scripts': [...], 'policies': [...]}
        
        Returns:
            List of (resource_type, resource) tuples in dependency order
        """
        # Build dependency graph at resource level
        in_degree = defaultdict(int)
        graph = defaultdict(list)
        resource_map = {}  # Maps (type, id) -> resource
        
        # First pass: catalog all resources
        for res_type, resources in resources_by_type.items():
            for resource in resources:
                # Extract ID - try direct id first, then general.id (policies, profiles)
                res_id = resource.get('id')
                if res_id is None:
                    res_id = resource.get('general', {}).get('id')
                
                key = (res_type, res_id)
                resource_map[key] = resource
                in_degree[key] = 0
        
        # Second pass: build edges based on dependencies
        for res_type, resources in resources_by_type.items():
            for resource in resources:
                # Extract ID - try direct id first, then general.id (policies, profiles)
                res_id = resource.get('id')
                if res_id is None:
                    res_id = resource.get('general', {}).get('id')
                
                res_key = (res_type, res_id)
                deps = self.extract_dependencies(res_type, resource)
                
                for dep_type, dep_ids in deps.items():
                    for dep_id in dep_ids:
                        dep_key = (dep_type, dep_id)
                        if dep_key in resource_map:
                            # dep_key must come before res_key
                            graph[dep_key].append(res_key)
                            in_degree[res_key] += 1
        
        # Kahn's algorithm for topological sort
        queue = deque([key for key in resource_map.keys() if in_degree[key] == 0])
        sorted_resources = []
        
        while queue:
            current = queue.popleft()
            sorted_resources.append((current[0], resource_map[current]))
            
            for neighbor in graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # Check for cycles
        if len(sorted_resources) != len(resource_map):
            # There's a cycle - just return in type order as fallback
            fallback = []
            type_order = ['categories', 'buildings', 'scripts', 'packages', 'computer_groups', 'config-profiles', 'policies']
            for res_type in type_order:
                if res_type in resources_by_type:
                    for resource in resources_by_type[res_type]:
                        fallback.append((res_type, resource))
            return fallback
        
        return sorted_resources
