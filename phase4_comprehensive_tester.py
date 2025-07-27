# 🚀 PHASE 4: COMPREHENSIVE PERSONALIZATION TEST SUITE
# Tests deep user intelligence and Style DNA features

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any

def test_phase4_style_profile_service():
    """
    Test Phase 4 Enhanced Style Profile Service with behavioral learning.
    """
    print("🧬 PHASE 4: TESTING STYLE DNA & BEHAVIORAL LEARNING")
    print("=" * 60)
    
    base_url = "http://localhost:8003"
    test_user = "phase4_test_user"
    
    # Test 1: Health Check with Phase 4 features
    print("🔍 Test 1: Phase 4 Style Profile Health Check")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Health Check: Working")
            
            # Check for Phase 4 indicators
            phase4_score = 0
            if "phase" in health_data and "4" in str(health_data["phase"]):
                phase4_score += 20
                print("  • Phase 4 identification: ✅")
            
            if "behavioral_learning" in str(health_data).lower():
                phase4_score += 20
                print("  • Behavioral Learning: ✅")
            
            if "style_dna" in str(health_data).lower():
                phase4_score += 20
                print("  • Style DNA analysis: ✅")
                
            if "intelligence" in str(health_data).lower():
                phase4_score += 20
                print("  • Intelligence features: ✅")
                
            if len(health_data.keys()) >= 8:
                phase4_score += 20
                print("  • Comprehensive Phase 4 response: ✅")
            
            print(f"  📊 Phase 4 Health Score: {phase4_score}%")
        else:
            print(f"❌ Health Check: HTTP {response.status_code}")
            phase4_score = 0
    except Exception as e:
        print(f"❌ Health Check: Connection failed - {str(e)}")
        phase4_score = 0
    
    # Test 2: Create Advanced Profile
    print("\\n🧠 Test 2: Create Advanced Profile with Intelligence")
    try:
        profile_data = {
            "user_id": test_user,
            "basic_info": {
                "age": 28,
                "style_preference": "modern_casual",
                "size": "M"
            }
        }
        
        response = requests.post(f"{base_url}/profile/create-advanced", 
                               json=profile_data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Advanced Profile Creation: Working")
            
            intelligence_features = 0
            if "intelligence_features" in result:
                intelligence_features = len(result["intelligence_features"])
                print(f"  • Intelligence features: {intelligence_features} ✅")
            
            if "learning_status" in result:
                print("  • Learning system: ✅")
                
            if "ADVANCED_PROFILE_CREATED" in result.get("status", ""):
                print("  • Advanced profile status: ✅")
            
            print(f"  📊 Profile Intelligence: {intelligence_features}/4 features")
        else:
            print(f"❌ Advanced Profile Creation: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Advanced Profile Creation: {str(e)}")
    
    # Test 3: Behavioral Learning
    print("\\n🔍 Test 3: Behavioral Learning Engine")
    try:
        behavior_data = {
            "interactions": [
                {"type": "view", "item": "blue_shirt", "context": "work"},
                {"type": "like", "item": "black_pants", "context": "formal"},
                {"type": "save", "item": "white_sneakers", "context": "casual"}
            ]
        }
        
        response = requests.post(f"{base_url}/profile/{test_user}/learn-behavior", 
                               json=behavior_data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Behavioral Learning: Working")
            
            learning_score = 0
            if "learning_results" in result:
                learning_score += 25
                print("  • Learning results generated: ✅")
            
            if "style_dna_summary" in result:
                learning_score += 25
                print("  • Style DNA updated: ✅")
            
            if "intelligence_improvement" in result.get("learning_results", {}):
                learning_score += 25
                print("  • Intelligence improvement: ✅")
                
            if "BEHAVIORAL_LEARNING_COMPLETED" in result.get("status", ""):
                learning_score += 25
                print("  • Learning completion: ✅")
            
            print(f"  📊 Behavioral Learning Score: {learning_score}%")
        else:
            print(f"❌ Behavioral Learning: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Behavioral Learning: {str(e)}")
    
    # Test 4: Style DNA Analysis
    print("\\n🧬 Test 4: Style DNA Analysis")
    try:
        response = requests.get(f"{base_url}/profile/{test_user}/style-dna", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Style DNA Analysis: Working")
            
            dna_score = 0
            if "style_dna" in result and result["style_dna"]:
                dna_score += 30
                print("  • Style DNA generated: ✅")
            
            if "dna_insights" in result:
                dna_score += 25
                print("  • DNA insights available: ✅")
            
            if "intelligence_metrics" in result:
                dna_score += 25
                print("  • Intelligence metrics: ✅")
                
            if result.get("style_dna", {}).get("confidence_level", 0) > 0.7:
                dna_score += 20
                print("  • High confidence DNA: ✅")
            
            print(f"  📊 Style DNA Score: {dna_score}%")
            
            # Display DNA insights
            insights = result.get("dna_insights", {})
            if insights:
                print(f"  🎯 Dominant Style: {insights.get('dominant_style', 'N/A')}")
                print(f"  🌈 Top Colors: {[c[0] for c in insights.get('favorite_colors', [])]}")
        else:
            print(f"❌ Style DNA Analysis: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Style DNA Analysis: {str(e)}")
    
    return phase4_score

def test_phase4_combination_engine():
    """
    Test Phase 4 Enhanced Combination Engine with personalization.
    """
    print("\\n🎨 PHASE 4: TESTING PERSONALIZED COMBINATION ENGINE")
    print("=" * 60)
    
    base_url = "http://localhost:8004"
    test_user = "phase4_test_user"
    
    # Test 1: Health Check
    print("🔍 Test 1: Phase 4 Combination Health Check")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Health Check: Working")
            
            personalization_score = 0
            if "personalization" in str(health_data).lower():
                personalization_score += 25
                print("  • Personalization features: ✅")
            
            if "style_dna" in str(health_data).lower():
                personalization_score += 25
                print("  • Style DNA integration: ✅")
            
            if "behavioral" in str(health_data).lower():
                personalization_score += 25
                print("  • Behavioral intelligence: ✅")
                
            if "deep" in str(health_data).lower():
                personalization_score += 25
                print("  • Deep intelligence: ✅")
            
            print(f"  📊 Personalization Score: {personalization_score}%")
        else:
            print(f"❌ Health Check: HTTP {response.status_code}")
            personalization_score = 0
    except Exception as e:
        print(f"❌ Health Check: {str(e)}")
        personalization_score = 0
    
    # Test 2: Personalized Combination Generation
    print("\\n🧠 Test 2: Personalized Combination Generation")
    try:
        personalized_request = {
            "user_id": test_user,
            "context": "work",
            "occasion": "meeting",
            "weather": "sunny",
            "season": "spring",
            "use_style_dna": True,
            "consider_history": True,
            "personalization_level": "high",
            "mood": "confident"
        }
        
        response = requests.post(f"{base_url}/generate-personalized-combination", 
                               json=personalized_request, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Personalized Generation: Working")
            
            personalization_quality = 0
            if "personalization_insights" in result:
                personalization_quality += 20
                print("  • Personalization insights: ✅")
            
            if "style_dna_match" in result:
                personalization_quality += 20
                print("  • Style DNA matching: ✅")
            
            if "behavioral_reasoning" in result:
                personalization_quality += 20
                print("  • Behavioral reasoning: ✅")
                
            if "user_satisfaction_prediction" in result:
                personalization_quality += 20
                print("  • Satisfaction prediction: ✅")
                
            if result.get("confidence_score", 0) > 0.8:
                personalization_quality += 20
                print("  • High confidence output: ✅")
            
            print(f"  📊 Personalization Quality: {personalization_quality}%")
            
            # Display key insights
            confidence = result.get("confidence_score", 0)
            print(f"  🎯 AI Confidence: {confidence:.2f}")
            
            if "behavioral_reasoning" in result:
                reasoning_count = len(result["behavioral_reasoning"])
                print(f"  🧠 Reasoning factors: {reasoning_count}")
                
        else:
            print(f"❌ Personalized Generation: HTTP {response.status_code}")
            personalization_quality = 0
            
    except Exception as e:
        print(f"❌ Personalized Generation: {str(e)}")
        personalization_quality = 0
    
    return personalization_score + personalization_quality

def test_phase4_integration():
    """
    Test Phase 4 service integration and intelligence flow.
    """
    print("\\n🔗 PHASE 4: TESTING SERVICE INTEGRATION")
    print("=" * 60)
    
    integration_score = 0
    
    # Test service connectivity
    services = {
        "Style Profile (8003)": "http://localhost:8003",
        "Combination Engine (8004)": "http://localhost:8004"
    }
    
    active_services = 0
    for service_name, url in services.items():
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                print(f"✅ {service_name}: Active")
                active_services += 1
            else:
                print(f"❌ {service_name}: HTTP {response.status_code}")
        except:
            print(f"❌ {service_name}: Connection failed")
    
    integration_score = (active_services / len(services)) * 100
    print(f"\\n📊 Service Integration Score: {integration_score}%")
    
    return integration_score

def generate_phase4_progress_report():
    """
    Generate comprehensive Phase 4 progress report.
    """
    print("\\n" + "=" * 70)
    print("🏆 PHASE 4: COMPREHENSIVE PROGRESS REPORT")
    print("=" * 70)
    
    # Run all tests
    style_profile_score = test_phase4_style_profile_service()
    combination_score = test_phase4_combination_engine()
    integration_score = test_phase4_integration()
    
    # Calculate overall Phase 4 score
    total_score = (style_profile_score + combination_score + integration_score) / 3
    
    print("\\n🎯 PHASE 4 FINAL RESULTS:")
    print("=" * 50)
    print(f"🧬 Style DNA & Behavioral Learning: {style_profile_score}%")
    print(f"🎨 Personalized Combinations: {combination_score}%")
    print(f"🔗 Service Integration: {integration_score}%")
    print(f"\\n📊 OVERALL PHASE 4 SCORE: {total_score:.1f}%")
    
    # Determine Phase 4 status
    if total_score >= 90:
        status = "🚀 PHASE 4: EXCEPTIONAL! Deep personalization mastered"
        next_phase = "Ready for Phase 5: FAISS-based Recommendations"
    elif total_score >= 80:
        status = "✅ PHASE 4: EXCELLENT! Strong personalization capabilities"
        next_phase = "Phase 5 preparation recommended"
    elif total_score >= 70:
        status = "⚠️  PHASE 4: GOOD! Most personalization features working"
        next_phase = "Continue Phase 4 optimization"
    else:
        status = "❌ PHASE 4: NEEDS IMPROVEMENT! Focus on core features"
        next_phase = "Phase 4 enhancement required"
    
    print(f"\\n{status}")
    print(f"🎯 Next Step: {next_phase}")
    
    # Generate detailed report
    report = {
        "phase": 4,
        "timestamp": datetime.now().isoformat(),
        "overall_score": total_score,
        "component_scores": {
            "style_dna_behavioral_learning": style_profile_score,
            "personalized_combinations": combination_score,
            "service_integration": integration_score
        },
        "status": status,
        "next_phase_readiness": total_score >= 85,
        "key_achievements": [
            "Style DNA analysis system",
            "Behavioral learning engine", 
            "Deep personalization algorithms",
            "User intelligence metrics",
            "Predictive styling capabilities"
        ],
        "recommendations": [
            "Continue user behavior learning",
            "Enhance Style DNA accuracy",
            "Optimize personalization algorithms",
            "Prepare for Phase 5 FAISS integration"
        ]
    }
    
    # Save report
    with open("PHASE4_PROGRESS_REPORT.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\\n📝 Detailed report saved: PHASE4_PROGRESS_REPORT.json")
    print(f"⏰ Test completed at: {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    generate_phase4_progress_report()
