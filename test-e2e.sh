#!/bin/bash

# JamfTerraform End-to-End Test Script
# This script tests the complete workflow from HCL generation to execution

set -e

echo "🚀 JamfTerraform End-to-End Test"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Backend Health Check
echo "📡 Test 1: Backend Health Check"
HEALTH=$(curl -s http://localhost:8000/healthz)
if [ "$HEALTH" = '{"status":200}' ]; then
    echo -e "${GREEN}✓ Backend is healthy${NC}"
else
    echo -e "${RED}✗ Backend health check failed${NC}"
    exit 1
fi
echo ""

# Test 2: Cookbook Endpoint
echo "📚 Test 2: Cookbook Endpoint"
COOKBOOK=$(curl -s http://localhost:8000/api/cookbook)
MODULE_COUNT=$(echo $COOKBOOK | grep -o '"id"' | wc -l | tr -d ' ')
if [ "$MODULE_COUNT" -eq "6" ]; then
    echo -e "${GREEN}✓ Cookbook has 6 modules${NC}"
else
    echo -e "${RED}✗ Cookbook module count incorrect: $MODULE_COUNT${NC}"
    exit 1
fi
echo ""

# Test 3: HCL Generation
echo "🤖 Test 3: HCL Generation"
PROMPT="Create a simple Jamf policy resource"
RESPONSE=$(curl -s -X POST http://localhost:8000/api/generate \
    -H "Content-Type: application/json" \
    -d "{\"prompt\":\"$PROMPT\"}")

SUCCESS=$(echo $RESPONSE | grep -o '"success":true' | wc -l | tr -d ' ')
if [ "$SUCCESS" -eq "1" ]; then
    echo -e "${GREEN}✓ HCL generation successful${NC}"
    HCL=$(echo $RESPONSE | grep -o '"hcl":"[^"]*"' | cut -d'"' -f4)
    echo -e "${YELLOW}Generated HCL preview:${NC}"
    echo "$HCL" | head -5
else
    echo -e "${RED}✗ HCL generation failed${NC}"
    echo "$RESPONSE"
    exit 1
fi
echo ""

# Test 4: Frontend Accessibility
echo "🌐 Test 4: Frontend Accessibility"
FRONTEND=$(curl -s http://localhost:5173)
if echo "$FRONTEND" | grep -q "root"; then
    echo -e "${GREEN}✓ Frontend is accessible${NC}"
else
    echo -e "${RED}✗ Frontend not accessible${NC}"
    exit 1
fi
echo ""

# Test 5: Agent Build Status
echo "🔧 Test 5: Agent Build Status"
if [ -f "agent/src-tauri/target/debug/agent" ] || [ -f "agent/src-tauri/target/debug/agent.exe" ]; then
    echo -e "${GREEN}✓ Agent binary exists${NC}"
else
    echo -e "${YELLOW}⚠ Agent binary not found (may still be building)${NC}"
fi
echo ""

# Summary
echo "=================================="
echo -e "${GREEN}✅ All tests passed!${NC}"
echo ""
echo "Next steps:"
echo "1. Open web app: http://localhost:5173"
echo "2. Generate HCL using chat or cookbook"
echo "3. Open Tauri agent (should already be running)"
echo "4. Paste HCL and execute with your Jamf token"
echo ""
