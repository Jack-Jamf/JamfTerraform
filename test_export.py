#!/usr/bin/env python3
"""
Automated test script for JamfTerraform bulk export functionality.
Tests the Railway production API to verify mobile device resource export.
"""
import asyncio
import httpx
import json
import sys
from datetime import datetime

# Railway Production API
PRODUCTION_API = "https://jamfaform-production.up.railway.app"
API_ENDPOINT = f"{PRODUCTION_API}/api/jamf/bulk-export"

# Test configuration
TEST_RESOURCES = [
    {"type": "mobile-device-groups", "id": 1},  # Test mobile device group
    {"type": "mobile-device-prestages", "id": 1},  # Test mobile device prestage
]

async def test_bulk_export(jamf_url: str, jamf_username: str, jamf_password: str):
    """
    Test the bulk export endpoint with real Jamf credentials.
    
    Args:
        jamf_url: Jamf Pro instance URL
        jamf_username: Jamf Pro username
        jamf_password: Jamf Pro password
    """
    print("=" * 80)
    print("🧪 JamfTerraform Bulk Export Test")
    print("=" * 80)
    print(f"Testing: {API_ENDPOINT}")
    print(f"Jamf Instance: {jamf_url}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 80)
    
    # Prepare request payload
    payload = {
        "credentials": {
            "url": jamf_url,
            "username": jamf_username,
            "password": jamf_password
        },
        "resources": TEST_RESOURCES,
        "include_dependencies": False  # Faster test, just check if export works
    }
    
    print("\n📦 Request Payload:")
    print(f"  Resources to export: {len(TEST_RESOURCES)}")
    for res in TEST_RESOURCES:
        print(f"    - {res['type']} (ID: {res['id']})")
    
    # Make API request
    print("\n🚀 Sending request to Railway API...")
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(
                API_ENDPOINT,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"\n📊 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                # Success - got ZIP file
                content_type = response.headers.get("content-type", "")
                content_length = len(response.content)
                
                print(f"✅ SUCCESS: Export completed!")
                print(f"   Content-Type: {content_type}")
                print(f"   File Size: {content_length:,} bytes ({content_length / 1024:.2f} KB)")
                
                # Save ZIP for inspection
                output_file = f"test_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                print(f"   Saved to: {output_file}")
                
                # Verify it's a valid ZIP
                import zipfile
                try:
                    with zipfile.ZipFile(output_file, 'r') as zip_ref:
                        files = zip_ref.namelist()
                        print(f"\n📁 ZIP Contents ({len(files)} files):")
                        
                        # Check for mobile device resources
                        mobile_files = [f for f in files if 'mobile' in f.lower()]
                        if mobile_files:
                            print(f"   ✅ Found {len(mobile_files)} mobile device related files:")
                            for f in mobile_files[:5]:  # Show first 5
                                print(f"      - {f}")
                            if len(mobile_files) > 5:
                                print(f"      ... and {len(mobile_files) - 5} more")
                        else:
                            print(f"   ⚠️  No mobile device files found in ZIP")
                        
                        # Show sample of other files
                        other_files = [f for f in files if 'mobile' not in f.lower()][:5]
                        if other_files:
                            print(f"\n   Other files (sample):")
                            for f in other_files:
                                print(f"      - {f}")
                    
                    return True
                    
                except zipfile.BadZipFile:
                    print(f"   ❌ ERROR: Downloaded file is not a valid ZIP")
                    return False
                    
            elif response.status_code == 500:
                # Server error
                print(f"❌ FAILED: Server returned 500 Internal Server Error")
                try:
                    error_data = response.json()
                    print(f"\n🔍 Error Details:")
                    print(json.dumps(error_data, indent=2))
                except:
                    print(f"\n🔍 Raw Response:")
                    print(response.text[:500])
                return False
                
            else:
                # Other error
                print(f"❌ FAILED: Unexpected status code {response.status_code}")
                print(f"\n🔍 Response Body:")
                print(response.text[:500])
                return False
                
        except httpx.TimeoutException:
            print(f"❌ FAILED: Request timed out after 120 seconds")
            return False
        except Exception as e:
            print(f"❌ FAILED: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return False

async def main():
    """Main test runner."""
    # Check for credentials in environment or use defaults
    import os
    
    jamf_url = os.getenv("JAMF_URL", "https://kickthetires.jamfcloud.com")
    jamf_username = os.getenv("JAMF_USERNAME", "admin")
    jamf_password = os.getenv("JAMF_PASSWORD", "adminadmin")
    
    # Allow command line override
    if len(sys.argv) == 4:
        jamf_url = sys.argv[1]
        jamf_username = sys.argv[2]
        jamf_password = sys.argv[3]
    
    print(f"Using credentials: {jamf_username}@{jamf_url}")
    
    # Run test
    success = await test_bulk_export(jamf_url, jamf_username, jamf_password)
    
    print("\n" + "=" * 80)
    if success:
        print("✅ TEST PASSED: Export functionality working correctly")
        sys.exit(0)
    else:
        print("❌ TEST FAILED: Export functionality has issues")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
