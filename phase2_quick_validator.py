# 🚀 PHASE 2: QUICK SERVICE HEALTH & ENHANCEMENT VALIDATOR

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any

def test_phase2_enhancements():
    """
    Quick test of PHASE 2 enhancements without heavy dependencies.
    """
    
    print("🚀 PHASE 2: Quick Enhancement Validation")
    print("=" * 60)
    
    services = {
        "Backend": "http://localhost:8000",
        "Image Processing": "http://localhost:8001", 
        "Style Profile": "http://localhost:8002",
        "NLU": "http://localhost:8003",
        "Combination Engine": "http://localhost:8004",
        "Recommendation": "http://localhost:8005",
        "Orchestrator": "http://localhost:8006",
        "Feedback Loop": "http://localhost:8007"
    }
    
    results = {
        "phase2_score": 0.0,
        "service_status": {},
        "enhancements_detected": [],
        "performance_metrics": {}
    }
    
    total_score = 0.0
    working_services = 0
    
    print("\n🔍 Testing Service Availability & Enhancements:")
    print("-" * 50)
    
    for service_name, base_url in services.items():
        try:
            # Test health endpoint
            start_time = time.time()
            response = requests.get(f"{base_url}/health", timeout=5)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                working_services += 1
                service_score = 70.0  # Base score for working
                
                # Check for PHASE 2 enhancements in response
                try:
                    health_data = response.json()
                    
                    # Enhanced service indicators
                    if isinstance(health_data, dict):
                        if len(health_data) > 2:  # More detailed health info
                            service_score += 10.0
                            results["enhancements_detected"].append(f"{service_name}: Enhanced health check")
                        
                        if "version" in health_data and "2." in str(health_data.get("version", "")):
                            service_score += 10.0
                            results["enhancements_detected"].append(f"{service_name}: PHASE 2 version")
                        
                        if "features" in health_data or "optimization" in str(health_data).lower():
                            service_score += 5.0
                            results["enhancements_detected"].append(f"{service_name}: Feature enhancements")
                    
                    if response_time < 1000:  # Fast response
                        service_score += 5.0
                
                except:
                    pass  # Basic health check still counts
                
                results["service_status"][service_name] = {
                    "status": "✅ Working",
                    "response_time_ms": round(response_time, 1),
                    "score": service_score
                }
                
                total_score += service_score
                print(f"✅ {service_name:20} | {response_time:6.0f}ms | Score: {service_score:.0f}%")
                
            else:
                results["service_status"][service_name] = {
                    "status": f"❌ HTTP {response.status_code}",
                    "response_time_ms": round(response_time, 1),
                    "score": 20.0
                }
                total_score += 20.0
                print(f"❌ {service_name:20} | {response_time:6.0f}ms | HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            results["service_status"][service_name] = {
                "status": "❌ Connection Failed",
                "error": str(e),
                "score": 0.0
            }
            print(f"❌ {service_name:20} | Connection Failed")
    
    # Calculate overall PHASE 2 score
    overall_score = total_score / len(services)
    results["phase2_score"] = round(overall_score, 1)
    
    # Test specific PHASE 2 features
    print(f"\n🧪 Testing PHASE 2 Specific Features:")
    print("-" * 50)
    
    # Test Image Processing Enhanced Features
    try:
        response = requests.get("http://localhost:8001/", timeout=3)
        if response.status_code == 200:
            content = response.text.lower()
            if "phase 2" in content or "enhanced" in content:
                results["enhancements_detected"].append("Image Processing: PHASE 2 enhancement detected")
                print("✅ Image Processing: PHASE 2 enhancements detected")
            else:
                print("📋 Image Processing: Standard version")
    except:
        print("❌ Image Processing: Could not test enhancements")
    
    # Test NLU Performance Features
    try:
        response = requests.get("http://localhost:8003/performance_metrics", timeout=3)
        if response.status_code == 200:
            results["enhancements_detected"].append("NLU: Performance metrics available")
            print("✅ NLU: Performance monitoring active")
        else:
            print("📋 NLU: Basic monitoring")
    except:
        print("❌ NLU: Performance metrics not available")
    
    # Performance summary
    avg_response_time = sum(
        s.get("response_time_ms", 5000) 
        for s in results["service_status"].values() 
        if "response_time_ms" in s
    ) / max(len(results["service_status"]), 1)
    
    results["performance_metrics"] = {
        "working_services": working_services,
        "total_services": len(services),
        "availability_percentage": round((working_services / len(services)) * 100, 1),
        "average_response_time_ms": round(avg_response_time, 1)
    }
    
    # Generate report
    print(f"\n📊 PHASE 2 QUICK VALIDATION RESULTS:")
    print("=" * 60)
    print(f"Overall PHASE 2 Score: {results['phase2_score']:.1f}%")
    print(f"Service Availability: {results['performance_metrics']['availability_percentage']:.1f}% ({working_services}/{len(services)})")
    print(f"Average Response Time: {results['performance_metrics']['average_response_time_ms']:.1f}ms")
    print(f"Enhancements Detected: {len(results['enhancements_detected'])}")
    
    # Enhancement details
    if results["enhancements_detected"]:
        print(f"\n🎉 PHASE 2 Enhancements Found:")
        for enhancement in results["enhancements_detected"]:
            print(f"  • {enhancement}")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    if results["phase2_score"] >= 85:
        print("  ✅ Excellent! Ready for PHASE 3")
    elif results["phase2_score"] >= 70:
        print("  🟡 Good progress, minor improvements needed")
    else:
        print("  🔴 Needs attention before proceeding to PHASE 3")
    
    # Save results
    results["timestamp"] = datetime.now().isoformat()
    with open("PHASE2_QUICK_VALIDATION.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📝 Detailed results saved to: PHASE2_QUICK_VALIDATION.json")
    print("=" * 60)
    
    return results

if __name__ == "__main__":
    try:
        results = test_phase2_enhancements()
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        results = {"error": str(e), "phase2_score": 0.0}
