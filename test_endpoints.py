#!/usr/bin/env python3
"""
Diagnostic test - directly test each mobile device endpoint to find which one is failing.
"""
import asyncio
import httpx

JAMF_URL = "https://kickthetires.jamfcloud.com"
JAMF_USERNAME = "admin"
JAMF_PASSWORD = "adminadmin"

async def test_single_endpoint(client, token, endpoint_name, url):
    """Test a single Jamf API endpoint."""
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    
    print(f"\n🔍 Testing: {endpoint_name}")
    print(f"   URL: {url}")
    
    try:
        response = await client.get(url, headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS - Type: {type(data)}")
            if isinstance(data, dict):
                print(f"   Keys: {list(data.keys())}")
            elif isinstance(data, list):
                print(f"   Length: {len(data)}")
            else:
                print(f"   ❌ ERROR: Unexpected type {type(data)}")
            return True
        else:
            print(f"   ❌ FAILED: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"   ❌ EXCEPTION: {e}")
        return False

async def main():
    base_url = JAMF_URL
    
    print("=" * 80)
    print("🔬 Mobile Device Endpoint Diagnostic")
    print("=" * 80)
    print(f"Instance: {JAMF_URL}")
    
    async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
        # Get auth token
        print("\n🔐 Getting auth token...")
        auth_url = f"{base_url}/api/v1/auth/token"
        auth_response = await client.post(
            auth_url,
            auth=(JAMF_USERNAME, JAMF_PASSWORD)
        )
        
        if auth_response.status_code != 200:
            print(f"❌ Auth failed: {auth_response.status_code}")
            return
        
        token = auth_response.json()["token"]
        print(f"✅ Token obtained")
        
        # Test each mobile device endpoint
        endpoints = {
            "Mobile Device Groups": f"{base_url}/JSSResource/mobiledevicegroups",
            "Mobile Device Prestages": f"{base_url}/api/v2/mobile-device-prestages",
            "Mobile Device Config Profiles": f"{base_url}/JSSResource/mobiledeviceconfigurationprofiles",
            "Advanced Mobile Device Searches": f"{base_url}/JSSResource/advancedmobiledevicesearches",
            "Mobile Device Extension Attributes": f"{base_url}/JSSResource/mobiledeviceextensionattributes",
        }
        
        results = {}
        for name, url in endpoints.items():
            results[name] = await test_single_endpoint(client, token, name, url)
        
        print("\n" + "=" * 80)
        print("📊 Results Summary")
        print("=" * 80)
        for name, success in results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} - {name}")

if __name__ == "__main__":
    asyncio.run(main())
