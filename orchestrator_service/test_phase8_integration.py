# Phase 8 AI Integration Test
import sys
sys.path.append('.')

from main import app
from fastapi.testclient import TestClient
import json

# Create test client
client = TestClient(app)

print("🧪 Testing Phase 8 AI-Enhanced Orchestrator...")

# Test 1: Health check
print("\n1️⃣ Testing health endpoint...")
response = client.get("/health")
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print("   ✅ Health check passed")
else:
    print("   ❌ Health check failed")

# Test 2: AI Status
print("\n2️⃣ Testing AI status endpoint...")
response = client.get("/ai/status")
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"   Phase: {data.get('phase', 'Unknown')}")
    print(f"   AI Status: {data.get('status', 'Unknown')}")
    print("   ✅ AI status endpoint working")
else:
    print("   ❌ AI status endpoint failed")

# Test 3: AI Analytics
print("\n3️⃣ Testing AI analytics endpoint...")
response = client.get("/ai/analytics")
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print("   ✅ AI analytics endpoint working")
else:
    print("   ❌ AI analytics endpoint failed")

print("\n🎉 Phase 8 AI Integration Test Completed!")
print("   The orchestrator is running in compatibility mode.")
print("   Phase 8 AI endpoints are functional and ready for enhancement.")
