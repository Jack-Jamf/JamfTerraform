"""
Test script to verify hot-reload functionality of LLMService.

This simulates updating the app_catalog.json and verifies the service reloads it.
"""

import json
import time
from pathlib import Path
import sys
import os

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

def test_hot_reload():
    """Test that LLMService detects and reloads catalog changes."""
    
    catalog_path = Path("backend/app_catalog.json")
    backup_path = Path("backend/app_catalog.json.backup")
    
    print("🧪 Testing LLMService Hot Reload Functionality")
    print("=" * 60)
    
    # Backup original catalog
    print("\n1️⃣  Backing up original catalog...")
    with open(catalog_path, 'r') as f:
        original_catalog = json.load(f)
    
    with open(backup_path, 'w') as f:
        json.dump(original_catalog, f, indent=2)
    
    print(f"   ✅ Backed up {len(original_catalog)} titles")
    
    try:
        # Import LLMService (this will load the catalog)
        print("\n2️⃣  Initializing LLMService...")
        from llm_service import get_llm_service
        
        service = get_llm_service()
        initial_count = len(service.app_catalog)
        print(f"   ✅ Service initialized with {initial_count} titles")
        
        # Modify the catalog file
        print("\n3️⃣  Modifying catalog (adding test entry)...")
        test_catalog = original_catalog + ["TEST_APP_RELOAD_VERIFICATION"]
        
        with open(catalog_path, 'w') as f:
            json.dump(test_catalog, f, indent=2)
        
        print(f"   ✅ Updated catalog to {len(test_catalog)} titles")
        
        # Wait a moment to ensure file system updates timestamp
        time.sleep(0.5)
        
        # Trigger a generation to test hot-reload
        print("\n4️⃣  Triggering catalog freshness check...")
        # We'll just check the internal method directly
        service._check_catalog_freshness()
        
        new_count = len(service.app_catalog)
        print(f"   ✅ Service now has {new_count} titles")
        
        # Verify reload worked
        if new_count == len(test_catalog):
            print("\n✅ HOT RELOAD TEST PASSED!")
            print(f"   • Detected catalog change")
            print(f"   • Reloaded from {initial_count} to {new_count} titles")
            return True
        else:
            print("\n❌ HOT RELOAD TEST FAILED!")
            print(f"   • Expected {len(test_catalog)} titles, got {new_count}")
            return False
            
    finally:
        # Restore original catalog
        print("\n5️⃣  Restoring original catalog...")
        with open(catalog_path, 'w') as f:
            json.dump(original_catalog, f, indent=2)
        
        backup_path.unlink()
        print("   ✅ Restored and cleaned up")


if __name__ == "__main__":
    success = test_hot_reload()
    sys.exit(0 if success else 1)
