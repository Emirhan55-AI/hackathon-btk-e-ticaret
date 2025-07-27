# 🚀 PHASE 3: COMPREHENSIVE AI RECOVERY & TESTING SUITE
# Emergency AI recovery and advanced testing for PHASE 3 objectives

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, List

class Phase3AITester:
    """
    PHASE 3: Comprehensive AI testing and recovery system.
    Tests all AI endpoints and measures Phase 3 improvements.
    """
    
    def __init__(self):
        self.base_url = "http://localhost:8001"
        self.test_results = {
            "phase3_score": 0.0,
            "ai_endpoints": {},
            "ai_features": [],
            "performance_metrics": {},
            "recovery_status": {}
        }
    
    def test_phase3_endpoints(self) -> Dict[str, Any]:
        """
        Test all Phase 3 AI endpoints and features.
        """
        print("🧠 PHASE 3: AI ENDPOINT RECOVERY TEST")
        print("=" * 50)
        
        endpoints_to_test = [
            {"path": "/", "method": "GET", "name": "Health Check"},
            {"path": "/health", "method": "GET", "name": "Detailed Health"},
            {"path": "/analyze", "method": "POST", "name": "PHASE 3 AI Analysis"},
            {"path": "/analyze_image", "method": "POST", "name": "Image Upload Analysis"},
            {"path": "/performance_metrics", "method": "GET", "name": "Performance Monitoring"},
            {"path": "/ai_model_status", "method": "GET", "name": "AI Model Status"}
        ]
        
        working_endpoints = 0
        total_endpoints = len(endpoints_to_test)
        
        for endpoint in endpoints_to_test:
            endpoint_name = endpoint["name"]
            endpoint_path = endpoint["path"]
            method = endpoint["method"]
            
            try:
                start_time = time.time()
                
                if method == "GET":
                    response = requests.get(f"{self.base_url}{endpoint_path}", timeout=5)
                elif method == "POST":
                    # Different test data for different endpoints
                    if endpoint_path == "/analyze":
                        test_data = {
                            "image_url": "https://example.com/shirt.jpg",
                            "image_description": "A stylish blue cotton shirt with classic design",
                            "analysis_type": "advanced"
                        }
                    else:
                        test_data = {"test": "data"}
                    
                    response = requests.post(
                        f"{self.base_url}{endpoint_path}", 
                        json=test_data, 
                        timeout=5
                    )
                
                response_time = (time.time() - start_time) * 1000
                
                if response.status_code == 200:
                    working_endpoints += 1
                    status = "✅ Working"
                    
                    # Check for Phase 3 features
                    try:
                        data = response.json()
                        phase3_features = []
                        
                        if isinstance(data, dict):
                            if "phase3" in str(data).lower():
                                phase3_features.append("Phase 3 indicators")
                            if "advanced" in str(data).lower():
                                phase3_features.append("Advanced features")
                            if "ai" in str(data).lower():
                                phase3_features.append("AI capabilities")
                        
                        self.test_results["ai_endpoints"][endpoint_name] = {
                            "status": "working",
                            "response_time_ms": round(response_time, 1),
                            "phase3_features": phase3_features,
                            "response_size": len(str(data))
                        }
                        
                        if phase3_features:
                            self.test_results["ai_features"].extend(phase3_features)
                            
                    except:
                        pass
                        
                    print(f"✅ {endpoint_name:25} | {response_time:6.1f}ms")
                    
                elif response.status_code == 404:
                    status = "❌ Not Found"
                    print(f"❌ {endpoint_name:25} | 404 Not Found")
                elif response.status_code == 500:
                    status = "⚠️ Server Error"
                    print(f"⚠️ {endpoint_name:25} | 500 Server Error")
                else:
                    status = f"⚠️ HTTP {response.status_code}"
                    print(f"⚠️ {endpoint_name:25} | HTTP {response.status_code}")
                
                self.test_results["ai_endpoints"][endpoint_name] = {
                    "status": status,
                    "response_time_ms": round(response_time, 1),
                    "http_code": response.status_code
                }
                
            except requests.exceptions.ConnectionError:
                print(f"❌ {endpoint_name:25} | Connection Failed")
                self.test_results["ai_endpoints"][endpoint_name] = {
                    "status": "connection_failed",
                    "error": "Connection failed"
                }
            except requests.exceptions.Timeout:
                print(f"⏰ {endpoint_name:25} | Timeout")
                self.test_results["ai_endpoints"][endpoint_name] = {
                    "status": "timeout",
                    "error": "Request timeout"
                }
            except Exception as e:
                print(f"❌ {endpoint_name:25} | Error: {str(e)}")
                self.test_results["ai_endpoints"][endpoint_name] = {
                    "status": "error",
                    "error": str(e)
                }
        
        # Calculate Phase 3 AI score
        endpoint_score = (working_endpoints / total_endpoints) * 100
        self.test_results["phase3_score"] = endpoint_score
        
        print(f"\n📊 PHASE 3 AI ENDPOINT RESULTS:")
        print(f"Working Endpoints: {working_endpoints}/{total_endpoints} ({endpoint_score:.1f}%)")
        print(f"Phase 3 Features Detected: {len(self.test_results['ai_features'])}")
        
        return self.test_results
    
    def test_ai_analysis_quality(self) -> Dict[str, Any]:
        """
        Test AI analysis quality and accuracy.
        """
        print(f"\n🎯 PHASE 3: AI ANALYSIS QUALITY TEST")
        print("-" * 50)
        
        quality_results = {
            "ai_analysis_working": False,
            "response_quality": 0,
            "ai_features_detected": [],
            "confidence_scoring": False,
            "multi_dimensional_analysis": False
        }
        
        # Test /analyze endpoint specifically
        try:
            test_data = {
                "image_description": "A professional navy blue blazer with silver buttons",
                "analysis_type": "detailed"
            }
            
            response = requests.post(
                f"{self.base_url}/analyze", 
                json=test_data, 
                timeout=10
            )
            
            if response.status_code == 200:
                quality_results["ai_analysis_working"] = True
                result = response.json()
                
                print("✅ AI Analysis Endpoint: Working")
                print(f"📝 Response Keys: {list(result.keys()) if isinstance(result, dict) else 'Non-dict response'}")
                
                # Check for Phase 3 quality indicators
                if isinstance(result, dict):
                    quality_score = 0
                    
                    if "detected_items" in result:
                        quality_score += 25
                        quality_results["ai_features_detected"].append("Item detection")
                    
                    if "style_analysis" in result:
                        quality_score += 25
                        quality_results["ai_features_detected"].append("Style analysis")
                    
                    if "confidence" in str(result):
                        quality_score += 20
                        quality_results["confidence_scoring"] = True
                        quality_results["ai_features_detected"].append("Confidence scoring")
                    
                    if "phase3" in str(result).lower():
                        quality_score += 15
                        quality_results["ai_features_detected"].append("Phase 3 enhancements")
                    
                    if len(result.keys()) >= 5:
                        quality_score += 15
                        quality_results["multi_dimensional_analysis"] = True
                        quality_results["ai_features_detected"].append("Multi-dimensional analysis")
                    
                    quality_results["response_quality"] = quality_score
                    
                    print(f"🎯 AI Quality Score: {quality_score}%")
                    print(f"🚀 AI Features: {quality_results['ai_features_detected']}")
                    
                    # Show sample of actual response
                    print(f"\n📋 Sample AI Response:")
                    print(json.dumps(result, indent=2)[:300] + "..." if len(str(result)) > 300 else json.dumps(result, indent=2))
                    
            else:
                print(f"❌ AI Analysis Endpoint: HTTP {response.status_code}")
                print(f"📝 Error Response: {response.text}")
                
        except Exception as e:
            print(f"❌ AI Analysis Test Failed: {str(e)}")
        
        return quality_results
    
    def generate_phase3_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive Phase 3 recovery and progress report.
        """
        print(f"\n" + "="*60)
        print("🚀 PHASE 3: AI RECOVERY & PROGRESS REPORT")
        print("="*60)
        
        # Run all tests
        endpoint_results = self.test_phase3_endpoints()
        quality_results = self.test_ai_analysis_quality()
        
        # Calculate overall Phase 3 score
        endpoint_score = endpoint_results.get("phase3_score", 0)
        quality_score = quality_results.get("response_quality", 0)
        overall_phase3_score = (endpoint_score * 0.4) + (quality_score * 0.6)  # Quality weighted higher
        
        # Generate comprehensive report
        final_report = {
            "phase": "PHASE 3: AI Recovery & Enhancement",
            "timestamp": datetime.now().isoformat(),
            "overall_phase3_score": round(overall_phase3_score, 1),
            "target_score": 90.0,
            "recovery_status": "partial" if overall_phase3_score > 30 else "critical",
            "endpoint_availability": f"{sum(1 for ep in endpoint_results['ai_endpoints'].values() if 'working' in ep.get('status', ''))}/{len(endpoint_results['ai_endpoints'])}",
            "ai_analysis_working": quality_results["ai_analysis_working"],
            "phase3_features_detected": list(set(endpoint_results.get("ai_features", []) + quality_results.get("ai_features_detected", []))),
            "detailed_results": {
                "endpoint_tests": endpoint_results,
                "quality_tests": quality_results
            },
            "next_actions": []
        }
        
        # Generate recommendations
        if not quality_results["ai_analysis_working"]:
            final_report["next_actions"].append("🚨 CRITICAL: Fix /analyze endpoint immediately")
        
        if overall_phase3_score < 50:
            final_report["next_actions"].append("🔧 URGENT: AI model recovery needed")
        
        if quality_results["response_quality"] < 70:
            final_report["next_actions"].append("🧠 Enhance AI analysis quality and features")
        
        if overall_phase3_score >= 70:
            final_report["next_actions"].append("🚀 Ready for advanced Phase 3 features")
        
        # Print summary
        print(f"\n📊 PHASE 3 RECOVERY RESULTS:")
        print(f"Overall Score: {overall_phase3_score:.1f}% (Target: 90%)")
        print(f"Endpoint Availability: {final_report['endpoint_availability']}")
        print(f"AI Analysis Working: {'✅' if quality_results['ai_analysis_working'] else '❌'}")
        print(f"Phase 3 Features: {len(final_report['phase3_features_detected'])}")
        
        if final_report["phase3_features_detected"]:
            print(f"\n🎉 Phase 3 Features Detected:")
            for feature in final_report["phase3_features_detected"]:
                print(f"  • {feature}")
        
        print(f"\n💡 Next Actions:")
        for action in final_report["next_actions"]:
            print(f"  • {action}")
        
        # Save report
        with open("PHASE3_AI_RECOVERY_REPORT.json", "w") as f:
            json.dump(final_report, f, indent=2)
        
        print(f"\n📝 Detailed report saved to: PHASE3_AI_RECOVERY_REPORT.json")
        print("="*60)
        
        return final_report

def main():
    """Run comprehensive Phase 3 AI recovery and testing"""
    tester = Phase3AITester()
    return tester.generate_phase3_report()

if __name__ == "__main__":
    try:
        report = main()
    except Exception as e:
        print(f"❌ Phase 3 testing failed: {e}")
        report = {"error": str(e), "overall_phase3_score": 0.0}
