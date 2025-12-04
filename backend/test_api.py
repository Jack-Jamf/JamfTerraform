#!/usr/bin/env python3
"""
Test script for the LLM service.
This demonstrates how to use the backend API.
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def test_health():
    """Test the health endpoint."""
    print("Testing /healthz endpoint...")
    response = requests.get(f"{BASE_URL}/healthz")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")


def test_generate(prompt: str, context: str = None):
    """Test the HCL generation endpoint."""
    print(f"Testing /generate endpoint with prompt: '{prompt}'")
    
    payload = {"prompt": prompt}
    if context:
        payload["context"] = context
    
    response = requests.post(
        f"{BASE_URL}/api/generate",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    
    if result.get("success"):
        print("✓ Generation successful!")
        print(f"Generated HCL:\n{result['hcl']}\n")
    else:
        print(f"✗ Generation failed: {result.get('error')}\n")
    
    return result


if __name__ == "__main__":
    print("=== JamfTerraform Backend Test ===\n")
    
    # Test health endpoint
    test_health()
    
    # Test HCL generation
    # Note: This will fail without a valid GEMINI_API_KEY in .env
    test_generate("Create a Jamf policy to install Google Chrome on all computers")
    
    # Test with context
    test_generate(
        "Add a scope to target only MacBooks",
        context="resource \"jamfpro_policy\" \"install_chrome\" { ... }"
    )
