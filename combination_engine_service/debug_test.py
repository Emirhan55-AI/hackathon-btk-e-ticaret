# Debug test to find the exact error
import sys
sys.path.append('.')

from main import app
from fastapi.testclient import TestClient
import traceback

# Create test client for making HTTP requests to the application
client = TestClient(app)

print("🔍 DEBUG: Testing API endpoint...")

try:
    # Simple test request
    test_request = {
        "user_id": "test_user_debug",
        "context": "casual"
    }
    
    print(f"📤 Sending request: {test_request}")
    response = client.post("/generate-combination", json=test_request)
    
    print(f"📥 Response status: {response.status_code}")
    
    if response.status_code == 200:
        print(f"✅ Response data: {response.json()}")
    else:
        print(f"❌ Error response: {response.text}")
        
except Exception as e:
    print(f"💥 Exception occurred: {str(e)}")
    print("📋 Full traceback:")
    traceback.print_exc()
