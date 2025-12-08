"""Support file handler for downloading and organizing Jamf Pro resource files."""
import re
import zipfile
from typing import Dict, Optional, Tuple
from jamf_client import JamfClient


class SupportFileHandler:
    """
    Handles downloading and organizing support files from Jamf Pro.
    
    Downloads scripts and configuration profile payloads to be included
    as local files in the Terraform export, referenced via file() function.
    """
    
    # Directory structure for support files
    SCRIPTS_DIR = "support_files/scripts"
    PROFILES_DIR = "support_files/profiles"
    PACKAGES_DIR = "support_files/packages"
    
    def __init__(self, client: Optional[JamfClient] = None):
        """
        Initialize the handler.
        
        Args:
            client: Optional JamfClient for fetching file contents.
                    If not provided, must call set_client() before downloading.
        """
        self.client = client
        # Maps (resource_type, resource_id) -> {filename, content, relative_path}
        self.files: Dict[Tuple[str, int], dict] = {}
    
    def set_client(self, client: JamfClient) -> None:
        """Set the Jamf client for API requests."""
        self.client = client
    
    def _sanitize_filename(self, name: str) -> str:
        """
        Convert a resource name to a safe filename.
        
        Args:
            name: Original resource name
            
        Returns:
            Filesystem-safe filename
        """
        # Replace spaces and special chars with underscores
        sanitized = re.sub(r'[^\w\-.]', '_', name.lower())
        # Remove consecutive underscores
        sanitized = re.sub(r'_+', '_', sanitized)
        # Remove leading/trailing underscores
        sanitized = sanitized.strip('_')
        return sanitized or 'unnamed'
    
    def _detect_script_extension(self, script_contents: str) -> str:
        """
        Detect appropriate file extension from script shebang.
        
        Args:
            script_contents: The script content
            
        Returns:
            File extension (e.g., '.sh', '.zsh', '.py')
        """
        if not script_contents:
            return '.sh'
        
        first_line = script_contents.split('\n')[0].strip()
        
        if first_line.startswith('#!'):
            shebang = first_line.lower()
            if 'python' in shebang:
                return '.py'
            elif 'zsh' in shebang:
                return '.zsh'
            elif 'perl' in shebang:
                return '.pl'
            elif 'ruby' in shebang:
                return '.rb'
            elif 'osascript' in shebang:
                if '-l javascript' in script_contents[:200].lower():
                    return '.js'
                return '.scpt'
            elif 'swift' in shebang:
                return '.swift'
        
        # Default to shell script
        return '.sh'
    
    async def process_script(self, script_id: int, script_data: dict) -> dict:
        """
        Process a script resource and store its file info.
        
        Args:
            script_id: The script ID
            script_data: Script data from Jamf API (must include script_contents)
            
        Returns:
            Dict with file info: {filename, content, relative_path}
        """
        name = script_data.get('name', f'script_{script_id}')
        script_contents = script_data.get('script_contents', '')
        
        if not script_contents:
            # No content available, can't create file
            return {}
        
        # Determine extension and filename
        extension = self._detect_script_extension(script_contents)
        safe_name = self._sanitize_filename(name)
        filename = f"{safe_name}{extension}"
        relative_path = f"{self.SCRIPTS_DIR}/{filename}"
        
        file_info = {
            'filename': filename,
            'content': script_contents,
            'relative_path': relative_path,
            'resource_type': 'scripts',
            'resource_id': script_id,
            'resource_name': name
        }
        
        self.files[('scripts', script_id)] = file_info
        return file_info
    
    async def process_config_profile(self, profile_id: int, profile_data: dict) -> dict:
        """
        Process a configuration profile and store its payload file info.
        
        Args:
            profile_id: The profile ID
            profile_data: Profile data from Jamf API (must include general.payloads)
            
        Returns:
            Dict with file info: {filename, content, relative_path}
        """
        general = profile_data.get('general', {})
        name = general.get('name', f'profile_{profile_id}')
        payloads = general.get('payloads', '')
        
        if not payloads:
            # No payloads available, can't create file
            return {}
        
        # Configuration profiles are always .mobileconfig (XML plist)
        safe_name = self._sanitize_filename(name)
        filename = f"{safe_name}.mobileconfig"
        relative_path = f"{self.PROFILES_DIR}/{filename}"
        
        file_info = {
            'filename': filename,
            'content': payloads,
            'relative_path': relative_path,
            'resource_type': 'config-profiles',
            'resource_id': profile_id,
            'resource_name': name
        }
        
        self.files[('config-profiles', profile_id)] = file_info
        return file_info
    
    def process_package_metadata(self, package_id: int, package_data: dict) -> dict:
        """
        Process package metadata (does NOT download the actual package file).
        
        Args:
            package_id: The package ID
            package_data: Package data from Jamf API
            
        Returns:
            Dict with metadata info including JCDS URL if available
        """
        name = package_data.get('name', f'package_{package_id}')
        filename = package_data.get('filename', '')
        
        # Build metadata for reference
        metadata = {
            'resource_type': 'packages',
            'resource_id': package_id,
            'resource_name': name,
            'filename': filename,
            'notes': package_data.get('notes', ''),
            'category': package_data.get('category', ''),
            # Package files are too large to download - provide reference info
            'download_note': f"Package file '{filename}' must be obtained separately from Jamf Pro."
        }
        
        return metadata
    
    def get_file_path(self, resource_type: str, resource_id: int) -> Optional[str]:
        """
        Get the relative path for a downloaded file.
        
        Args:
            resource_type: Type of resource ('scripts', 'config-profiles')
            resource_id: Resource ID
            
        Returns:
            Relative path string or None if not found
        """
        key = (resource_type, resource_id)
        if key in self.files:
            return self.files[key].get('relative_path')
        return None
    
    def get_terraform_file_reference(self, resource_type: str, resource_id: int) -> Optional[str]:
        """
        Get the Terraform file() function reference for a resource.
        
        Args:
            resource_type: Type of resource
            resource_id: Resource ID
            
        Returns:
            Terraform file() expression or None if not found
        """
        path = self.get_file_path(resource_type, resource_id)
        if path:
            return f'file("${{path.module}}/{path}")'
        return None
    
    def write_files_to_zip(self, zip_file: zipfile.ZipFile) -> int:
        """
        Write all downloaded files to a ZIP archive.
        
        Args:
            zip_file: An open ZipFile object to write to
            
        Returns:
            Number of files written
        """
        count = 0
        for key, file_info in self.files.items():
            if 'content' in file_info and 'relative_path' in file_info:
                zip_file.writestr(
                    file_info['relative_path'],
                    file_info['content']
                )
                count += 1
        return count
    
    def get_files_summary(self) -> dict:
        """
        Get a summary of all processed files.
        
        Returns:
            Dict with counts and file lists by type
        """
        summary = {
            'scripts': [],
            'profiles': [],
            'total_count': 0
        }
        
        for key, file_info in self.files.items():
            resource_type = key[0]
            if resource_type == 'scripts':
                summary['scripts'].append({
                    'name': file_info.get('resource_name'),
                    'path': file_info.get('relative_path')
                })
            elif resource_type == 'config-profiles':
                summary['profiles'].append({
                    'name': file_info.get('resource_name'),
                    'path': file_info.get('relative_path')
                })
        
        summary['total_count'] = len(self.files)
        return summary
    
    def clear(self) -> None:
        """Clear all stored file info."""
        self.files.clear()
