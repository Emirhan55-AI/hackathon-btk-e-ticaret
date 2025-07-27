# 🚀 PHASE 3 QUICK VALIDATOR
# Simplified test for Phase 3 status

import requests
import json
from datetime import datetime

print("🧠 PHASE 3: QUICK AI VALIDATION")
print("=" * 50)

services = {
    "Image Processing": "http://localhost:8001",
    "NLU Service": "http://localhost:8002", 
    "Style Profile": "http://localhost:8003",
    "Combination Engine": "http://localhost:8004",
    "Recommendation Engine": "http://localhost:8005"
}

phase3_score = 0
total_tests = 0

print("\n📊 PHASE 3 SERVICE STATUS:")
print("-" * 40)

for service_name, url in services.items():
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {service_name}: Active")
            
            # Check for Phase 3 indicators
            phase3_indicators = 0
            
            if "phase" in str(data).lower() and "3" in str(data):
                phase3_indicators += 1
                
            if "ai" in str(data).lower() or "intelligent" in str(data).lower():
                phase3_indicators += 1
                
            if len(data.keys()) >= 5:
                phase3_indicators += 1
                
            phase3_score += phase3_indicators
            total_tests += 3
            
            print(f"   📈 Phase 3 Features: {phase3_indicators}/3")
            
        else:
            print(f"❌ {service_name}: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ {service_name}: Connection failed")

print("\n🎯 PHASE 3 COMBINATION ENGINE TEST:")
print("-" * 40)

try:
    # Test combination generation
    test_data = {
        "user_id": "test_user",
        "occasion": "business_meeting",
        "weather": "sunny",
        "season": "spring"
    }
    
    response = requests.post("http://localhost:8004/generate-combination", 
                            json=test_data, timeout=10)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Combination Generation: Working")
        
        # Check for AI features
        ai_features = 0
        
        if "confidence_score" in result:
            ai_features += 1
            print("  • Confidence scoring: ✅")
            
        if "color_harmony" in str(result).lower():
            ai_features += 1
            print("  • Color analysis: ✅")
            
        if "style_coherence" in str(result).lower():
            ai_features += 1 
            print("  • Style analysis: ✅")
            
        if len(result.get("combination_items", [])) > 0:
            ai_features += 1
            print("  • Item recommendations: ✅")
            
        phase3_score += ai_features
        total_tests += 4
        
        print(f"   📊 AI Features Score: {ai_features}/4")
        
    else:
        print(f"❌ Combination Generation: HTTP {response.status_code}")
        
except Exception as e:
    print(f"❌ Combination Generation: {str(e)}")

print("\n🔍 PHASE 3 IMAGE ANALYSIS TEST:")
print("-" * 40)

try:
    # Test new /analyze endpoint
    test_data = {
        "description": "red casual t-shirt with denim jeans"
    }
    
    response = requests.post("http://localhost:8001/analyze", 
                            json=test_data, timeout=10)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Image Analysis: Working")
        
        # Check for Phase 3 analysis features
        analysis_features = 0
        
        if "ai_confidence" in result:
            analysis_features += 1
            print("  • AI confidence: ✅")
            
        if "style_analysis" in result:
            analysis_features += 1
            print("  • Style analysis: ✅")
            
        if "color_analysis" in result:
            analysis_features += 1
            print("  • Color analysis: ✅")
            
        if "recommendations" in result:
            analysis_features += 1
            print("  • Recommendations: ✅")
            
        phase3_score += analysis_features
        total_tests += 4
        
        print(f"   📊 Analysis Features: {analysis_features}/4")
        
    else:
        print(f"❌ Image Analysis: HTTP {response.status_code}")
        
except Exception as e:
    print(f"❌ Image Analysis: {str(e)}")

# Calculate final score
if total_tests > 0:
    final_percentage = (phase3_score / total_tests) * 100
else:
    final_percentage = 0

print("\n🎯 PHASE 3 VALIDATION SUMMARY:")
print("=" * 50)
print(f"📊 Phase 3 Score: {phase3_score}/{total_tests} ({final_percentage:.1f}%)")

if final_percentage >= 80:
    print("🚀 PHASE 3: EXCELLENT! AI features operational")
elif final_percentage >= 60:
    print("✅ PHASE 3: GOOD! Most AI features working")
elif final_percentage >= 40:
    print("⚠️  PHASE 3: MODERATE! Some AI features working") 
else:
    print("❌ PHASE 3: NEEDS WORK! Limited AI functionality")

print(f"\n⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Save results
results = {
    "phase": 3,
    "timestamp": datetime.now().isoformat(),
    "score": final_percentage,
    "tests_passed": phase3_score,
    "total_tests": total_tests,
    "status": "EXCELLENT" if final_percentage >= 80 else 
             "GOOD" if final_percentage >= 60 else
             "MODERATE" if final_percentage >= 40 else "NEEDS_WORK"
}

with open("PHASE3_VALIDATION_RESULTS.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n📝 Results saved to: PHASE3_VALIDATION_RESULTS.json")
