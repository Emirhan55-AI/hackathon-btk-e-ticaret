# Quick test script to verify ImageProcessingService functionality
# This script tests the service without starting a full server

import sys
import os

# Add the current directory to Python path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all imports work correctly"""
    try:
        print("Testing imports...")
        
        # Test basic imports
        from main import app
        print("✓ FastAPI app imported successfully")
        
        # Test if image analyzer can be imported
        try:
            from image_analyzer import ClothingImageAnalyzer
            print("✓ ClothingImageAnalyzer imported successfully")
            
            # Try to initialize the analyzer (this will download models if needed)
            print("Initializing analyzer (this may take a few minutes on first run)...")
            analyzer = ClothingImageAnalyzer()
            print("✓ ClothingImageAnalyzer initialized successfully")
            print(f"✓ Using device: {analyzer.device}")
            
        except Exception as e:
            print(f"⚠ ClothingImageAnalyzer failed to initialize: {e}")
            print("Service will run in placeholder mode")
            
        return True
        
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        from fastapi.testclient import TestClient
        from main import app
        
        client = TestClient(app)
        response = client.get("/")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Health endpoint working: {data['status']}")
            print(f"✓ AI Status: {data['ai_status']}")
            print(f"✓ Version: {data['version']}")
            return True
        else:
            print(f"✗ Health endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Health endpoint test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Aura ImageProcessingService Test ===")
    print("Testing Phase 2 AI Integration...\n")
    
    # Test imports
    imports_ok = test_imports()
    print()
    
    # Test health endpoint
    if imports_ok:
        health_ok = test_health_endpoint()
        print()
        
        if health_ok:
            print("🎉 ImageProcessingService Phase 2 is ready!")
            print("\nTo start the service:")
            print("uvicorn main:app --host 0.0.0.0 --port 8001")
            print("\nAPI Documentation available at:")
            print("http://localhost:8001/docs")
        else:
            print("❌ Service has issues with health endpoint")
    else:
        print("❌ Service has import issues")
        
    print("\n=== Test Complete ===")
