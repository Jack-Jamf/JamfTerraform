"""Tests for the SupportFileHandler and HCL generation with file references."""
import pytest
import zipfile
import io
from support_file_handler import SupportFileHandler
from hcl_generator import HCLGenerator


class TestSupportFileHandler:
    """Tests for SupportFileHandler class."""
    
    def test_sanitize_filename_basic(self):
        """Test basic filename sanitization."""
        handler = SupportFileHandler()
        assert handler._sanitize_filename("My Script") == "my_script"
        # Note: hyphens are allowed in filenames
        assert handler._sanitize_filename("Install-Homebrew") == "install-homebrew"
        assert handler._sanitize_filename("Test!@#$%^&*()Name") == "test_name"
    
    def test_sanitize_filename_empty(self):
        """Test empty filename handling."""
        handler = SupportFileHandler()
        assert handler._sanitize_filename("") == "unnamed"
        assert handler._sanitize_filename("!@#$%") == "unnamed"
    
    def test_detect_script_extension_bash(self):
        """Test bash script detection."""
        handler = SupportFileHandler()
        assert handler._detect_script_extension("#!/bin/bash\necho hello") == ".sh"
        assert handler._detect_script_extension("#!/bin/sh\necho hello") == ".sh"
    
    def test_detect_script_extension_zsh(self):
        """Test zsh script detection."""
        handler = SupportFileHandler()
        assert handler._detect_script_extension("#!/bin/zsh\necho hello") == ".zsh"
    
    def test_detect_script_extension_python(self):
        """Test Python script detection."""
        handler = SupportFileHandler()
        assert handler._detect_script_extension("#!/usr/bin/python3\nprint('hello')") == ".py"
        assert handler._detect_script_extension("#!/usr/bin/env python\nprint('hello')") == ".py"
    
    def test_detect_script_extension_default(self):
        """Test default extension when no shebang."""
        handler = SupportFileHandler()
        assert handler._detect_script_extension("echo hello") == ".sh"
        assert handler._detect_script_extension("") == ".sh"
    
    @pytest.mark.asyncio
    async def test_process_script(self):
        """Test script processing stores correct file info."""
        handler = SupportFileHandler()
        script_data = {
            'id': 123,
            'name': 'Install Homebrew',
            'script_contents': '#!/bin/bash\n/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        }
        
        result = await handler.process_script(123, script_data)
        
        assert result['filename'] == 'install_homebrew.sh'
        assert result['relative_path'] == 'support_files/scripts/install_homebrew.sh'
        assert '#!/bin/bash' in result['content']
        assert ('scripts', 123) in handler.files
    
    @pytest.mark.asyncio
    async def test_process_config_profile(self):
        """Test config profile processing stores correct file info."""
        handler = SupportFileHandler()
        profile_data = {
            'id': 456,
            'general': {
                'id': 456,
                'name': 'WiFi Configuration',
                'payloads': '<?xml version="1.0"?>\n<plist><dict><key>PayloadType</key></dict></plist>'
            }
        }
        
        result = await handler.process_config_profile(456, profile_data)
        
        assert result['filename'] == 'wifi_configuration.mobileconfig'
        assert result['relative_path'] == 'support_files/profiles/wifi_configuration.mobileconfig'
        assert '<?xml' in result['content']
        assert ('config-profiles', 456) in handler.files
    
    def test_get_terraform_file_reference(self):
        """Test Terraform file() reference generation."""
        handler = SupportFileHandler()
        handler.files[('scripts', 123)] = {
            'relative_path': 'support_files/scripts/my_script.sh'
        }
        
        ref = handler.get_terraform_file_reference('scripts', 123)
        assert ref == 'file("${path.module}/support_files/scripts/my_script.sh")'
    
    def test_get_terraform_file_reference_not_found(self):
        """Test None returned for missing resource."""
        handler = SupportFileHandler()
        ref = handler.get_terraform_file_reference('scripts', 999)
        assert ref is None
    
    @pytest.mark.asyncio
    async def test_write_files_to_zip(self):
        """Test writing files to a ZIP archive."""
        handler = SupportFileHandler()
        
        # Add some files
        await handler.process_script(1, {
            'id': 1,
            'name': 'Test Script',
            'script_contents': '#!/bin/bash\necho test'
        })
        
        # Write to ZIP
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zf:
            count = handler.write_files_to_zip(zf)
        
        assert count == 1
        
        # Verify contents
        zip_buffer.seek(0)
        with zipfile.ZipFile(zip_buffer, 'r') as zf:
            names = zf.namelist()
            assert 'support_files/scripts/test_script.sh' in names
            content = zf.read('support_files/scripts/test_script.sh').decode('utf-8')
            assert '#!/bin/bash' in content


class TestHCLGeneratorWithSupportFiles:
    """Tests for HCLGenerator with support file handler integration."""
    
    @pytest.mark.asyncio
    async def test_script_hcl_with_file_reference(self):
        """Test script HCL uses file() when support handler has the file."""
        handler = SupportFileHandler()
        await handler.process_script(123, {
            'id': 123,
            'name': 'My Script',
            'script_contents': '#!/bin/bash\necho hello',
            'priority': 'BEFORE'
        })
        
        hcl_gen = HCLGenerator(support_file_handler=handler)
        
        hcl = hcl_gen.generate_resource_hcl('scripts', {
            'id': 123,
            'name': 'My Script',
            'priority': 'BEFORE'
        })
        
        assert 'file("${path.module}/support_files/scripts/my_script.sh")' in hcl
        assert 'script_contents =' in hcl
    
    def test_script_hcl_without_support_handler(self):
        """Test script HCL falls back to inline content without handler."""
        hcl_gen = HCLGenerator()  # No support handler
        
        hcl = hcl_gen.generate_resource_hcl('scripts', {
            'id': 123,
            'name': 'My Script',
            'script_contents': '#!/bin/bash\necho hello'
        })
        
        # Should have escaped inline content
        assert 'script_contents =' in hcl
        assert 'file(' not in hcl
    
    @pytest.mark.asyncio
    async def test_config_profile_hcl_with_file_reference(self):
        """Test config profile HCL uses file() when support handler has the file."""
        handler = SupportFileHandler()
        await handler.process_config_profile(456, {
            'id': 456,
            'general': {
                'id': 456,
                'name': 'WiFi Profile',
                'payloads': '<?xml version="1.0"?><plist></plist>'
            }
        })
        
        hcl_gen = HCLGenerator(support_file_handler=handler)
        
        hcl = hcl_gen.generate_resource_hcl('config-profiles', {
            'id': 456,
            'general': {
                'id': 456,
                'name': 'WiFi Profile'
            }
        })
        
        assert 'file("${path.module}/support_files/profiles/wifi_profile.mobileconfig")' in hcl
        assert 'payloads' in hcl
    
    def test_package_hcl_includes_required_fields(self):
        """Test package HCL includes all required provider fields."""
        hcl_gen = HCLGenerator()
        
        hcl = hcl_gen.generate_resource_hcl('packages', {
            'id': 789,
            'name': 'Google Chrome',
            'filename': 'GoogleChrome.pkg'
        })
        
        # Check for required fields per provider documentation
        assert 'package_name' in hcl
        assert 'package_file_source' in hcl
        assert 'priority' in hcl
        assert 'reboot_required' in hcl
        assert 'fill_user_template' in hcl
        assert 'os_install' in hcl
        assert 'suppress_updates' in hcl
        assert 'suppress_eula' in hcl
        assert 'suppress_registration' in hcl
        assert 'suppress_from_dock' in hcl
        # Should reference support_files/packages directory
        assert 'support_files/packages' in hcl


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
