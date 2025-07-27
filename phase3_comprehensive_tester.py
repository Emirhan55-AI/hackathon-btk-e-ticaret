# 🚀 PHASE 3: COMPREHENSIVE TEST & VALIDATION SUITE
# Tests Phase 3 AI enhancements and intelligent features

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any

def test_phase3_combination_engine():
    """
    Test Phase 3 enhanced combination engine with AI intelligence.
    """
    print("🧠 PHASE 3: TESTING AI COMBINATION ENGINE")
    print("=" * 50)
    
    base_url = "http://localhost:8004"
    
    # Test 1: Health Check with Phase 3 features
    print("🔍 Test 1: Phase 3 Health Check")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Health Check: Working")
            
            # Check for Phase 3 indicators
            phase3_score = 0
            if "phase" in health_data and "3" in str(health_data["phase"]):
                phase3_score += 25
                print("  • Phase 3 identification: ✅")
            
            if "ai_capabilities" in health_data:
                phase3_score += 25
                print("  • AI capabilities documented: ✅")
            
            if "intelligent" in str(health_data).lower():
                phase3_score += 25
                print("  • Intelligence features: ✅")
                
            if len(health_data.keys()) >= 6:
                phase3_score += 25
                print("  • Comprehensive response: ✅")
            
            print(f"  📊 Phase 3 Health Score: {phase3_score}%")
        else:
            print(f"❌ Health Check: HTTP {response.status_code}")
            phase3_score = 0
    except Exception as e:
        print(f"❌ Health Check: Connection failed - {str(e)}")
        phase3_score = 0
    
    # Test 2: Intelligent Combination Generation
    print(f"\n🔍 Test 2: AI Combination Generation")
    try:
        test_request = {
            "user_id": "phase3_test_user",
            "context": "casual", 
            "occasion": "weekend",
            "season": "spring",
            "weather": "mild",
            "style_preference": "modern",
            "color_preference": ["blue", "white"],
            "ai_analysis_mode": "advanced"
        }
        
        start_time = time.time()
        response = requests.post(f"{base_url}/generate_combination", json=test_request, timeout=10)
        response_time = (time.time() - start_time) * 1000
        
        if response.status_code == 200:
            combination_data = response.json()
            print("✅ AI Combination Generation: Working")
            print(f"  ⏱️  Response time: {response_time:.1f}ms")
            
            # Analyze Phase 3 AI features
            ai_score = 0
            
            if "ai_confidence_score" in combination_data:
                ai_score += 20
                confidence = combination_data["ai_confidence_score"]
                print(f"  • AI Confidence Score: {confidence} ✅")
            
            if "style_analysis" in combination_data:
                ai_score += 20
                print("  • Style Analysis: ✅")
            
            if "color_harmony" in combination_data:
                ai_score += 20
                print("  • Color Harmony Analysis: ✅")
            
            if "styling_tips" in combination_data:
                ai_score += 15
                tips_count = len(combination_data["styling_tips"])
                print(f"  • Styling Tips: {tips_count} tips ✅")
            
            if "alternative_combinations" in combination_data:
                ai_score += 15
                alt_count = len(combination_data["alternative_combinations"])
                print(f"  • Alternative Combinations: {alt_count} alternatives ✅")
            
            if "phase3_features" in combination_data:
                ai_score += 10
                print("  • Phase 3 Features: ✅")
            
            print(f"  📊 AI Intelligence Score: {ai_score}%")
            
            # Show sample AI response
            print(f"\n  📋 Sample AI Response:")
            if "items" in combination_data:
                items = combination_data["items"][:2]  # Show first 2 items
                for item in items:
                    print(f"    - {item.get('type', 'item')}: {item.get('item', 'unknown')} ({item.get('color', 'unknown')} color)")
        else:
            print(f"❌ AI Combination: HTTP {response.status_code}")
            if response.text:
                print(f"  📝 Error: {response.text}")
            ai_score = 0
    except Exception as e:
        print(f"❌ AI Combination: Connection failed - {str(e)}")
        ai_score = 0
    
    # Test 3: Performance Metrics
    print(f"\n🔍 Test 3: Phase 3 Performance Metrics")
    try:
        response = requests.get(f"{base_url}/performance_metrics", timeout=5)
        if response.status_code == 200:
            metrics_data = response.json()
            print("✅ Performance Metrics: Available")
            
            if "ai_performance" in metrics_data:
                print("  • AI Performance Tracking: ✅")
            if "phase3_metrics" in metrics_data:
                print("  • Phase 3 Metrics: ✅")
            
            perf_score = 50
        else:
            print(f"❌ Performance Metrics: HTTP {response.status_code}")
            perf_score = 0
    except Exception as e:
        print(f"❌ Performance Metrics: Failed - {str(e)}")
        perf_score = 0
    
    # Calculate overall Phase 3 score
    overall_score = (phase3_score * 0.3) + (ai_score * 0.5) + (perf_score * 0.2)
    
    print(f"\n📊 PHASE 3 COMBINATION ENGINE RESULTS:")
    print(f"Health Check Score: {phase3_score}%")
    print(f"AI Intelligence Score: {ai_score}%") 
    print(f"Performance Metrics: {perf_score}%")
    print(f"Overall Phase 3 Score: {overall_score:.1f}%")
    
    return {
        "service": "combination_engine",
        "phase3_score": overall_score,
        "health_score": phase3_score,
        "ai_score": ai_score,
        "performance_score": perf_score
    }

def test_phase3_services_overview():
    """
    Test overview of all services for Phase 3 readiness.
    """
    print(f"\n🚀 PHASE 3: SERVICES OVERVIEW TEST")
    print("=" * 50)
    
    services = {
        "Backend": 8000,
        "Image Processing": 8001,
        "Style Profile": 8002,
        "NLU": 8003,
        "Combination Engine": 8004,
        "Recommendation": 8005,
        "Orchestrator": 8006,
        "Feedback Loop": 8007
    }
    
    working_services = 0
    phase3_ready_services = 0
    
    for service_name, port in services.items():
        try:
            response = requests.get(f"http://localhost:{port}/", timeout=3)
            if response.status_code == 200:
                working_services += 1
                
                # Check for Phase 3 readiness
                data = response.json()
                if "phase" in str(data).lower() and ("3" in str(data) or "advanced" in str(data).lower()):
                    phase3_ready_services += 1
                    print(f"✅ {service_name:20} | Phase 3 Ready")
                else:
                    print(f"🟡 {service_name:20} | Working (needs Phase 3 upgrade)")
            else:
                print(f"❌ {service_name:20} | HTTP {response.status_code}")
        except:
            print(f"❌ {service_name:20} | Connection Failed")
    
    service_availability = (working_services / len(services)) * 100
    phase3_readiness = (phase3_ready_services / len(services)) * 100
    
    print(f"\n📊 SERVICES OVERVIEW:")
    print(f"Working Services: {working_services}/{len(services)} ({service_availability:.1f}%)")
    print(f"Phase 3 Ready: {phase3_ready_services}/{len(services)} ({phase3_readiness:.1f}%)")
    
    return {
        "total_services": len(services),
        "working_services": working_services,
        "phase3_ready_services": phase3_ready_services,
        "service_availability": service_availability,
        "phase3_readiness": phase3_readiness
    }

def generate_phase3_progress_report():
    """
    Generate comprehensive Phase 3 progress report.
    """
    print(f"\n" + "="*60)
    print("🚀 PHASE 3: COMPREHENSIVE PROGRESS REPORT")
    print("="*60)
    
    # Run all tests
    combination_results = test_phase3_combination_engine()
    services_results = test_phase3_services_overview()
    
    # Calculate overall Phase 3 readiness
    combination_score = combination_results["phase3_score"]
    services_score = services_results["service_availability"]
    phase3_readiness = services_results["phase3_readiness"]
    
    overall_phase3_score = (combination_score * 0.4) + (services_score * 0.3) + (phase3_readiness * 0.3)
    
    # Generate report
    report = {
        "phase": "PHASE 3: AI Intelligence & Advanced Features",
        "timestamp": datetime.now().isoformat(),
        "overall_phase3_score": round(overall_phase3_score, 1),
        "target_score": 90.0,
        "combination_engine": combination_results,
        "services_overview": services_results,
        "achievements": [],
        "next_steps": []
    }
    
    # Identify achievements
    if combination_score >= 70:
        report["achievements"].append("AI Combination Engine successfully enhanced")
    if services_score >= 80:
        report["achievements"].append("Service infrastructure stable")
    if phase3_readiness >= 50:
        report["achievements"].append("Phase 3 upgrades in progress")
    
    # Generate next steps
    if overall_phase3_score < 60:
        report["next_steps"].append("🚨 Focus on core AI improvements")
    if phase3_readiness < 70:
        report["next_steps"].append("🔧 Upgrade more services to Phase 3")
    if combination_score >= 80:
        report["next_steps"].append("🚀 Ready for advanced AI features")
    
    # Print summary
    print(f"\n📊 PHASE 3 PROGRESS SUMMARY:")
    print(f"Overall Phase 3 Score: {overall_phase3_score:.1f}% (Target: 90%)")
    print(f"AI Combination Engine: {combination_score:.1f}%")
    print(f"Service Availability: {services_score:.1f}%")
    print(f"Phase 3 Readiness: {phase3_readiness:.1f}%")
    
    if report["achievements"]:
        print(f"\n🎉 Phase 3 Achievements:")
        for achievement in report["achievements"]:
            print(f"  • {achievement}")
    
    print(f"\n💡 Next Steps:")
    for step in report["next_steps"]:
        print(f"  • {step}")
    
    # Save report
    with open("PHASE3_PROGRESS_REPORT.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📝 Detailed report saved to: PHASE3_PROGRESS_REPORT.json")
    print("="*60)
    
    return report

if __name__ == "__main__":
    try:
        report = generate_phase3_progress_report()
    except Exception as e:
        print(f"❌ Phase 3 testing failed: {e}")
        report = {"error": str(e), "overall_phase3_score": 0.0}
