# JamfTerraform Testing

## Automated Export Testing

**Purpose:** Validate bulk export functionality via Railway API without manual UI testing.

### Quick Start

```bash
# Set credentials
export JAMF_URL="https://your-instance.jamfcloud.com"
export JAMF_USERNAME="your-username"
export JAMF_PASSWORD="your-password"

# Run test
python test_export.py
```

### Or pass credentials as arguments:

```bash
python test_export.py "https://your-instance.jamfcloud.com" "username" "password"
```

### What It Tests

- ✅ Railway production API connectivity
- ✅ Bulk export endpoint functionality
- ✅ Mobile device resource export (groups, prestages)
- ✅ ZIP file generation and validity
- ✅ Presence of mobile device files in export

### Output

The script will:

1. Call the Railway API endpoint
2. Download the exported ZIP file
3. Verify ZIP validity
4. Check for mobile device resource files
5. Save test export with timestamp
6. Exit with code 0 (success) or 1 (failure)

### Example Output

```
================================================================================
🧪 JamfTerraform Bulk Export Test
================================================================================
Testing: https://jamfaform-production.up.railway.app/api/jamf/bulk-export
Jamf Instance: https://example.jamfcloud.com
Timestamp: 2025-12-10T14:25:00
================================================================================

📦 Request Payload:
  Resources to export: 2
    - mobile-device-groups (ID: 1)
    - mobile-device-prestages (ID: 1)

🚀 Sending request to Railway API...

📊 Response Status: 200
✅ SUCCESS: Export completed!
   Content-Type: application/zip
   File Size: 45,231 bytes (44.17 KB)
   Saved to: test_export_20251210_142500.zip

📁 ZIP Contents (15 files):
   ✅ Found 2 mobile device related files:
      - mobile-device-groups.tf
      - mobile-device-prestages.tf

================================================================================
✅ TEST PASSED: Export functionality working correctly
================================================================================
```

### CI/CD Integration

Can be integrated into GitHub Actions or other CI systems:

```yaml
- name: Test Export
  env:
    JAMF_URL: ${{ secrets.JAMF_URL }}
    JAMF_USERNAME: ${{ secrets.JAMF_USERNAME }}
    JAMF_PASSWORD: ${{ secrets.JAMF_PASSWORD }}
  run: python test_export.py
```
