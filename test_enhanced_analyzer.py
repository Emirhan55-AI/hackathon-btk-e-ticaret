# 🧪 PHASE 2: Enhanced Image Analysis Tester

import requests
import json
import time

def test_enhanced_analyzer():
    """Test the enhanced image analyzer from Phase 2"""
    
    print("🧪 PHASE 2: Enhanced Image Analysis Test")
    print("=" * 50)
    
    # Test URL
    base_url = "http://localhost:8001"
    
    # Test data
    test_request = {
        "image_url": "https://example.com/shirt.jpg",
        "image_description": "A stylish blue cotton shirt with classic design",
        "analysis_type": "advanced"
    }
    
    try:
        print(f"🔍 Testing enhanced analyzer...")
        start_time = time.time()
        
        # Make request
        response = requests.post(
            f"{base_url}/analyze",
            json=test_request,
            timeout=10
        )
        
        response_time = (time.time() - start_time) * 1000
        
        print(f"⏱️  Response time: {response_time:.1f}ms")
        print(f"📡 Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Analysis successful!")
            print(f"📋 Result keys: {list(result.keys())}")
            
            # Check for Phase 2 enhancements
            phase2_features = []
            
            if "confidence_score" in result:
                phase2_features.append("Confidence scoring")
            
            if "analysis_method" in result:
                phase2_features.append("Analysis method tracking")
            
            if "processing_time" in result:
                phase2_features.append("Performance metrics")
            
            if "model_used" in result:
                phase2_features.append("Model identification")
            
            if len(str(result)) > 200:  # Detailed response
                phase2_features.append("Enhanced detail level")
            
            print(f"\n🎉 Phase 2 Features Detected: {len(phase2_features)}")
            for feature in phase2_features:
                print(f"  • {feature}")
            
            print(f"\n📝 Sample result:")
            print(json.dumps(result, indent=2)[:500] + "..." if len(str(result)) > 500 else json.dumps(result, indent=2))
            
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"📝 Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
    
    # Test basic endpoint
    try:
        print(f"\n🔍 Testing basic endpoint...")
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"📡 Status: {response.status_code}")
        
        if "phase 2" in response.text.lower() or "enhanced" in response.text.lower():
            print("✅ Phase 2 indicators found in main page")
        else:
            print("📋 Standard service response")
            
    except:
        print("❌ Could not test basic endpoint")

if __name__ == "__main__":
    test_enhanced_analyzer()
