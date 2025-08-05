# 🧪 AURA AI Feedback Loop - Advanced Prompt Engineering Test Suite
# Gelişmiş Prompt Engineering Kalıpları için Kapsamlı Test Sistemi

"""
Bu test suite, AURA AI Feedback Loop Service'inin gelişmiş prompt engineering
kalıplarını test eder ve doğrular.

Test Alanları:
1. 4 Prompt Engineering Pattern testi
2. Akış mühendisliği doğrulaması
3. Servisler arası koordinasyon testi
4. Performance ve accuracy metrikleri
"""

import asyncio
import time
import json
from typing import Dict, List, Any
from datetime import datetime
import requests
import sys
import os

# Test configuration
FEEDBACK_SERVICE_URL = "http://localhost:8007"
TEST_TIMEOUT = 30
EXPECTED_ACCURACY_THRESHOLD = 0.80

class PromptEngineeringTester:
    """Gelişmiş Prompt Engineering Test Sınıfı"""
    
    def __init__(self):
        self.test_results = {}
        self.service_available = False
        print("🧪 AURA AI Prompt Engineering Test Suite Initializing...")
    
    async def run_comprehensive_tests(self):
        """Kapsamlı test suite'ini çalıştır"""
        print("🚀 Starting Comprehensive Prompt Engineering Tests...\n")
        
        # 1. Service availability check
        if not await self._check_service_availability():
            print("❌ Feedback Loop Service is not available. Tests cannot proceed.")
            return False
        
        # 2. Test 4 Prompt Engineering Patterns
        await self._test_prompt_patterns()
        
        # 3. Test Flow Engineering Scenarios
        await self._test_flow_engineering()
        
        # 4. Test Service Coordination
        await self._test_service_coordination()
        
        # 5. Performance and Accuracy Tests
        await self._test_performance_metrics()
        
        # 6. Generate comprehensive report
        self._generate_test_report()
        
        return True
    
    async def _check_service_availability(self):
        """Servis erişilebilirlik kontrolü"""
        print("🔍 Checking Feedback Loop Service availability...")
        
        try:
            response = requests.get(f"{FEEDBACK_SERVICE_URL}/", timeout=5)
            if response.status_code == 200:
                self.service_available = True
                print("✅ Feedback Loop Service is available and healthy")
                return True
        except Exception as e:
            print(f"❌ Service check failed: {str(e)}")
        
        return False
    
    async def _test_prompt_patterns(self):
        """4 Prompt Engineering Pattern'ını test et"""
        print("🎭 Testing Prompt Engineering Patterns...\n")
        
        pattern_tests = [
            {
                "name": "Persona Pattern Test",
                "feedback": "Bu kombini hiç beğenmedim, bana uygun değil",
                "expected_pattern": "persona",
                "expected_type": "negative_general",
                "description": "AI öğrenme uzmanı persona ile negatif feedback analizi"
            },
            {
                "name": "Recipe Pattern Test", 
                "feedback": "Bu ceketin altına ne giymeliyim adım adım anlat",
                "expected_pattern": "recipe",
                "expected_type": "request_similar",
                "description": "Adım adım rehber istegi için recipe pattern"
            },
            {
                "name": "Template Pattern Test",
                "feedback": "Bu renk kombinasyonu uyumlu değil",
                "expected_pattern": "template", 
                "expected_type": "color_dissatisfaction",
                "description": "Yapılandırılmış renk analizi için template pattern"
            },
            {
                "name": "Context & Instruction Pattern Test",
                "feedback": "İş toplantısına bu kıyafet uygun değil",
                "expected_pattern": "context_instruction",
                "expected_type": "occasion_inappropriate", 
                "description": "Bağlamsal analiz için context & instruction pattern"
            }
        ]
        
        pattern_results = {}
        
        for test in pattern_tests:
            print(f"  🔬 {test['name']}")
            print(f"     Feedback: '{test['feedback']}'")
            
            try:
                # API call to analyze feedback
                response = requests.post(
                    f"{FEEDBACK_SERVICE_URL}/feedback/analyze",
                    json={
                        "user_id": "test_user_patterns",
                        "recommendation_id": f"rec_{test['name'].lower().replace(' ', '_')}",
                        "feedback_text": test["feedback"],
                        "context": {"test_scenario": test["name"]}
                    },
                    timeout=TEST_TIMEOUT
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result["success"]:
                        analysis = result["analysis_results"]
                        used_pattern = analysis.get("prompt_pattern_used", "unknown")
                        detected_type = analysis.get("feedback_type", "unknown")
                        confidence = analysis.get("confidence_score", 0)
                        
                        # Pattern accuracy check
                        pattern_match = used_pattern == test["expected_pattern"]
                        type_match = test["expected_type"] in detected_type
                        high_confidence = confidence > 0.8
                        
                        test_success = pattern_match and high_confidence
                        
                        pattern_results[test["name"]] = {
                            "success": test_success,
                            "pattern_used": used_pattern,
                            "expected_pattern": test["expected_pattern"],
                            "pattern_match": pattern_match,
                            "type_match": type_match,
                            "confidence": confidence,
                            "processing_time": analysis.get("processing_time_ms", 0),
                            "description": test["description"]
                        }
                        
                        status = "✅ PASSED" if test_success else "⚠️ NEEDS ATTENTION"
                        print(f"     Result: {status}")
                        print(f"     Pattern: {used_pattern} (Expected: {test['expected_pattern']})")
                        print(f"     Confidence: {confidence:.3f}")
                        print(f"     Processing Time: {analysis.get('processing_time_ms', 0):.2f}ms")
                        
                    else:
                        pattern_results[test["name"]] = {
                            "success": False,
                            "error": result.get("message", "Analysis failed")
                        }
                        print(f"     Result: ❌ FAILED - {result.get('message', 'Unknown error')}")
                
                else:
                    pattern_results[test["name"]] = {
                        "success": False,
                        "error": f"HTTP {response.status_code}"
                    }
                    print(f"     Result: ❌ FAILED - HTTP {response.status_code}")
                    
            except Exception as e:
                pattern_results[test["name"]] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"     Result: ❌ FAILED - {str(e)}")
            
            print()  # Empty line for readability
        
        self.test_results["prompt_patterns"] = pattern_results
        
        # Pattern summary
        successful_patterns = sum(1 for r in pattern_results.values() if r.get("success", False))
        pattern_success_rate = (successful_patterns / len(pattern_tests)) * 100
        
        print(f"📊 Prompt Pattern Test Summary:")
        print(f"   Total Patterns Tested: {len(pattern_tests)}")
        print(f"   Successful Patterns: {successful_patterns}")
        print(f"   Success Rate: {pattern_success_rate:.1f}%")
        print(f"   Status: {'✅ EXCELLENT' if pattern_success_rate >= 90 else '✅ GOOD' if pattern_success_rate >= 75 else '⚠️ NEEDS IMPROVEMENT'}\n")
    
    async def _test_flow_engineering(self):
        """Akış mühendisliği senaryolarını test et"""
        print("🔄 Testing Flow Engineering Scenarios...\n")
        
        flow_scenarios = [
            {
                "name": "Negative General Feedback Flow",
                "user_feedback": "Bu kombini beğenmedim",
                "expected_flow_steps": [
                    "feedback_reception",
                    "context_gathering", 
                    "nlu_analysis",
                    "classification_scoring",
                    "system_learning_update",
                    "response_generation",
                    "logging_monitoring"
                ],
                "expected_services": ["style_profile", "recommendation_engine", "quality_assurance"]
            },
            {
                "name": "Color Dissatisfaction Flow",
                "user_feedback": "Bu renk uyumlu değil",
                "expected_flow_steps": [
                    "specialized_color_analysis",
                    "enhanced_nlu_processing",
                    "targeted_learning_updates",
                    "intelligent_response_generation"
                ],
                "expected_services": ["image_processing", "style_profile", "combination_engine"]
            },
            {
                "name": "Appropriateness Issue Flow", 
                "user_feedback": "Bu öneri bana uygun değildi",
                "expected_flow_steps": [
                    "context_appropriateness_analysis",
                    "advanced_persona_processing",
                    "multi_dimensional_updates",
                    "contextual_response_strategy"
                ],
                "expected_services": ["style_profile", "recommendation_engine", "nlu_service"]
            },
            {
                "name": "Positive Reinforcement Flow",
                "user_feedback": "Beğendim, benzer önerilerde bulunabilir misin?",
                "expected_flow_steps": [
                    "positive_reinforcement_processing",
                    "enhancement_learning",
                    "proactive_recommendation_generation",
                    "engagement_optimization"
                ],
                "expected_services": ["combination_engine", "style_profile", "recommendation_engine"]
            }
        ]
        
        flow_results = {}
        
        for scenario in flow_scenarios:
            print(f"  🌊 {scenario['name']}")
            print(f"     Feedback: '{scenario['user_feedback']}'")
            
            try:
                # Test the flow with timing
                start_time = time.time()
                
                response = requests.post(
                    f"{FEEDBACK_SERVICE_URL}/feedback/analyze",
                    json={
                        "user_id": "test_user_flow",
                        "recommendation_id": f"rec_flow_{scenario['name'].lower().replace(' ', '_')}",
                        "feedback_text": scenario["user_feedback"],
                        "context": {"flow_test": scenario["name"]}
                    },
                    timeout=TEST_TIMEOUT
                )
                
                flow_time = (time.time() - start_time) * 1000
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result["success"]:
                        # Check flow completion
                        has_analysis = "analysis_results" in result
                        has_user_response = "user_response" in result
                        has_system_updates = "system_updates" in result
                        
                        flow_complete = has_analysis and has_user_response and has_system_updates
                        
                        # Check service coordination
                        system_updates = result.get("system_updates", {})
                        coordinated_services = len([k for k in system_updates.keys() if "update" in k or "check" in k])
                        
                        flow_results[scenario["name"]] = {
                            "success": flow_complete,
                            "flow_time_ms": flow_time,
                            "analysis_present": has_analysis,
                            "user_response_present": has_user_response,
                            "system_updates_present": has_system_updates,
                            "coordinated_services": coordinated_services,
                            "expected_services": len(scenario["expected_services"]),
                            "service_coordination_rate": min(100, (coordinated_services / len(scenario["expected_services"])) * 100)
                        }
                        
                        status = "✅ PASSED" if flow_complete else "⚠️ INCOMPLETE"
                        print(f"     Result: {status}")
                        print(f"     Flow Time: {flow_time:.2f}ms")
                        print(f"     Service Coordination: {coordinated_services}/{len(scenario['expected_services'])} services")
                        print(f"     Flow Completeness: {'Complete' if flow_complete else 'Incomplete'}")
                        
                    else:
                        flow_results[scenario["name"]] = {
                            "success": False,
                            "error": result.get("message", "Flow failed")
                        }
                        print(f"     Result: ❌ FAILED - {result.get('message', 'Unknown error')}")
                
                else:
                    flow_results[scenario["name"]] = {
                        "success": False, 
                        "error": f"HTTP {response.status_code}"
                    }
                    print(f"     Result: ❌ FAILED - HTTP {response.status_code}")
                    
            except Exception as e:
                flow_results[scenario["name"]] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"     Result: ❌ FAILED - {str(e)}")
            
            print()
        
        self.test_results["flow_engineering"] = flow_results
        
        # Flow summary
        successful_flows = sum(1 for r in flow_results.values() if r.get("success", False))
        flow_success_rate = (successful_flows / len(flow_scenarios)) * 100
        avg_flow_time = sum(r.get("flow_time_ms", 0) for r in flow_results.values()) / len(flow_results) if flow_results else 0
        
        print(f"📊 Flow Engineering Test Summary:")
        print(f"   Total Flows Tested: {len(flow_scenarios)}")
        print(f"   Successful Flows: {successful_flows}")
        print(f"   Success Rate: {flow_success_rate:.1f}%")
        print(f"   Average Flow Time: {avg_flow_time:.2f}ms")
        print(f"   Status: {'✅ EXCELLENT' if flow_success_rate >= 90 else '✅ GOOD' if flow_success_rate >= 75 else '⚠️ NEEDS IMPROVEMENT'}\n")
    
    async def _test_service_coordination(self):
        """Servisler arası koordinasyon testleri"""
        print("🔗 Testing Service Coordination...\n")
        
        coordination_tests = [
            {
                "name": "Multi-Service Coordination",
                "feedback": "Bu kombinasyonun renkleri ve stili uygun değil",
                "expected_services": ["style_profile", "recommendation_engine", "quality_assurance"],
                "coordination_type": "parallel_processing"
            },
            {
                "name": "Sequential Service Updates",
                "feedback": "Beğendim ama daha formal olmalı",
                "expected_services": ["style_profile", "combination_engine", "recommendation_engine"],
                "coordination_type": "sequential_updates"
            }
        ]
        
        coordination_results = {}
        
        for test in coordination_tests:
            print(f"  🤝 {test['name']}")
            print(f"     Feedback: '{test['feedback']}'")
            
            try:
                response = requests.post(
                    f"{FEEDBACK_SERVICE_URL}/feedback/analyze",
                    json={
                        "user_id": "test_user_coordination",
                        "recommendation_id": f"rec_coord_{test['name'].lower().replace(' ', '_')}",
                        "feedback_text": test["feedback"],
                        "context": {"coordination_test": test["name"]}
                    },
                    timeout=TEST_TIMEOUT
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result["success"]:
                        system_updates = result.get("system_updates", {})
                        
                        # Check service coordination evidence
                        profile_update = "style_profile_update" in system_updates
                        rec_update = "recommendation_update" in system_updates  
                        qa_check = "quality_assurance" in system_updates
                        
                        coordination_score = sum([profile_update, rec_update, qa_check])
                        coordination_success = coordination_score >= 2  # At least 2 services coordinated
                        
                        coordination_results[test["name"]] = {
                            "success": coordination_success,
                            "services_coordinated": coordination_score,
                            "expected_services": len(test["expected_services"]),
                            "profile_updated": profile_update,
                            "recommendation_updated": rec_update,
                            "quality_assured": qa_check,
                            "coordination_details": system_updates
                        }
                        
                        status = "✅ PASSED" if coordination_success else "⚠️ PARTIAL"
                        print(f"     Result: {status}")
                        print(f"     Services Coordinated: {coordination_score}/{len(test['expected_services'])}")
                        print(f"     Style Profile: {'✅' if profile_update else '❌'}")
                        print(f"     Recommendation Engine: {'✅' if rec_update else '❌'}")
                        print(f"     Quality Assurance: {'✅' if qa_check else '❌'}")
                        
                    else:
                        coordination_results[test["name"]] = {
                            "success": False,
                            "error": result.get("message", "Coordination failed")
                        }
                        print(f"     Result: ❌ FAILED - {result.get('message', 'Unknown error')}")
                
                else:
                    coordination_results[test["name"]] = {
                        "success": False,
                        "error": f"HTTP {response.status_code}"
                    }
                    print(f"     Result: ❌ FAILED - HTTP {response.status_code}")
                    
            except Exception as e:
                coordination_results[test["name"]] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"     Result: ❌ FAILED - {str(e)}")
            
            print()
        
        self.test_results["service_coordination"] = coordination_results
        
        # Coordination summary
        successful_coord = sum(1 for r in coordination_results.values() if r.get("success", False))
        coord_success_rate = (successful_coord / len(coordination_tests)) * 100
        
        print(f"📊 Service Coordination Test Summary:")
        print(f"   Total Coordination Tests: {len(coordination_tests)}")
        print(f"   Successful Coordinations: {successful_coord}")
        print(f"   Success Rate: {coord_success_rate:.1f}%")
        print(f"   Status: {'✅ EXCELLENT' if coord_success_rate >= 90 else '✅ GOOD' if coord_success_rate >= 75 else '⚠️ NEEDS IMPROVEMENT'}\n")
    
    async def _test_performance_metrics(self):
        """Performance ve doğruluk metriklerini test et"""
        print("⚡ Testing Performance Metrics...\n")
        
        # Performance test with multiple requests
        print("  📈 Performance Load Test...")
        
        test_feedbacks = [
            "Bu kombin çok güzel", 
            "Renkleri uyumlu değil",
            "Daha casual olmalı",
            "Mükemmel, benzer istiyorum",
            "Bu stil bana uygun değil"
        ] * 5  # 25 total requests
        
        response_times = []
        successful_requests = 0
        
        start_batch_time = time.time()
        
        for i, feedback in enumerate(test_feedbacks):
            try:
                start_req_time = time.time()
                
                response = requests.post(
                    f"{FEEDBACK_SERVICE_URL}/feedback/analyze",
                    json={
                        "user_id": f"perf_test_user_{i}",
                        "recommendation_id": f"perf_rec_{i}",
                        "feedback_text": feedback,
                        "context": {"performance_test": True}
                    },
                    timeout=10
                )
                
                req_time = (time.time() - start_req_time) * 1000
                response_times.append(req_time)
                
                if response.status_code == 200:
                    result = response.json()
                    if result["success"]:
                        successful_requests += 1
                        
            except Exception as e:
                print(f"     Request {i+1} failed: {str(e)}")
        
        batch_time = (time.time() - start_batch_time) * 1000
        
        # Calculate metrics
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        min_response_time = min(response_times) if response_times else 0
        max_response_time = max(response_times) if response_times else 0
        throughput = (successful_requests / (batch_time / 1000)) if batch_time > 0 else 0
        success_rate = (successful_requests / len(test_feedbacks)) * 100
        
        performance_results = {
            "total_requests": len(test_feedbacks),
            "successful_requests": successful_requests,
            "success_rate": success_rate,
            "average_response_time_ms": avg_response_time,
            "min_response_time_ms": min_response_time,
            "max_response_time_ms": max_response_time,
            "throughput_req_per_sec": throughput,
            "total_batch_time_ms": batch_time,
            "performance_grade": "A" if avg_response_time < 200 and success_rate > 95 else "B" if avg_response_time < 500 and success_rate > 90 else "C"
        }
        
        self.test_results["performance_metrics"] = performance_results
        
        print(f"     Total Requests: {len(test_feedbacks)}")
        print(f"     Successful: {successful_requests}")
        print(f"     Success Rate: {success_rate:.1f}%")
        print(f"     Average Response Time: {avg_response_time:.2f}ms")
        print(f"     Min Response Time: {min_response_time:.2f}ms")
        print(f"     Max Response Time: {max_response_time:.2f}ms")
        print(f"     Throughput: {throughput:.2f} req/sec")
        print(f"     Performance Grade: {performance_results['performance_grade']}")
        print()
        
        # Test analytics endpoint
        print("  📊 Analytics Endpoint Test...")
        
        try:
            analytics_response = requests.get(f"{FEEDBACK_SERVICE_URL}/feedback/analytics", timeout=10)
            
            if analytics_response.status_code == 200:
                analytics_data = analytics_response.json()
                
                analytics_results = {
                    "endpoint_available": True,
                    "system_statistics_present": "system_statistics" in analytics_data,
                    "pattern_effectiveness_present": "prompt_pattern_effectiveness" in analytics_data,
                    "recent_performance_present": "recent_performance" in analytics_data,
                    "analytics_completeness": 100 if all([
                        "system_statistics" in analytics_data,
                        "prompt_pattern_effectiveness" in analytics_data,
                        "recent_performance" in analytics_data
                    ]) else 66 if len([k for k in analytics_data.keys() if k in ["system_statistics", "prompt_pattern_effectiveness", "recent_performance"]]) >= 2 else 33
                }
                
                print(f"     Analytics Endpoint: ✅ Available")
                print(f"     Completeness: {analytics_results['analytics_completeness']}%")
                print(f"     Data Quality: {'✅ Complete' if analytics_results['analytics_completeness'] == 100 else '⚠️ Partial'}")
                
            else:
                analytics_results = {
                    "endpoint_available": False,
                    "error": f"HTTP {analytics_response.status_code}"
                }
                print(f"     Analytics Endpoint: ❌ Failed - HTTP {analytics_response.status_code}")
                
        except Exception as e:
            analytics_results = {
                "endpoint_available": False,
                "error": str(e)
            }
            print(f"     Analytics Endpoint: ❌ Failed - {str(e)}")
        
        self.test_results["analytics_test"] = analytics_results
        print()
    
    def _generate_test_report(self):
        """Kapsamlı test raporu oluştur"""
        print("📋 COMPREHENSIVE TEST REPORT")
        print("=" * 80)
        
        # Overall statistics
        total_tests = 0
        passed_tests = 0
        
        for category, results in self.test_results.items():
            if isinstance(results, dict):
                for test_name, test_result in results.items():
                    if isinstance(test_result, dict) and "success" in test_result:
                        total_tests += 1
                        if test_result["success"]:
                            passed_tests += 1
        
        overall_success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n🎯 EXECUTIVE SUMMARY")
        print(f"   Total Tests Executed: {total_tests}")
        print(f"   Tests Passed: {passed_tests}")
        print(f"   Overall Success Rate: {overall_success_rate:.1f}%")
        print(f"   System Status: {'🌟 EXCELLENT' if overall_success_rate >= 90 else '✅ GOOD' if overall_success_rate >= 75 else '⚠️ NEEDS IMPROVEMENT' if overall_success_rate >= 50 else '❌ CRITICAL ISSUES'}")
        
        # Detailed category results
        print(f"\n📊 DETAILED RESULTS BY CATEGORY")
        
        for category, results in self.test_results.items():
            print(f"\n   {category.upper().replace('_', ' ')}:")
            
            if isinstance(results, dict):
                category_tests = 0
                category_passed = 0
                
                for test_name, test_result in results.items():
                    if isinstance(test_result, dict):
                        if "success" in test_result:
                            category_tests += 1
                            status = "✅ PASS" if test_result["success"] else "❌ FAIL"
                            print(f"     • {test_name}: {status}")
                            
                            if test_result["success"]:
                                category_passed += 1
                            
                            # Show additional details for failed tests
                            if not test_result["success"] and "error" in test_result:
                                print(f"       Error: {test_result['error']}")
                        else:
                            # Handle performance metrics separately
                            if category == "performance_metrics":
                                print(f"     • Response Time: {test_result.get('average_response_time_ms', 0):.2f}ms")
                                print(f"     • Success Rate: {test_result.get('success_rate', 0):.1f}%")
                                print(f"     • Performance Grade: {test_result.get('performance_grade', 'N/A')}")
                
                if category_tests > 0:
                    category_rate = (category_passed / category_tests) * 100
                    print(f"     Category Success Rate: {category_rate:.1f}%")
        
        # Recommendations
        print(f"\n🔧 RECOMMENDATIONS")
        
        if overall_success_rate >= 90:
            print("   • System performing excellently")
            print("   • Continue monitoring and maintain current quality")
            print("   • Consider expanding test coverage for edge cases")
        elif overall_success_rate >= 75:
            print("   • System performing well with minor issues")
            print("   • Address failed test cases for improvement")
            print("   • Monitor performance metrics regularly")
        elif overall_success_rate >= 50:
            print("   • System needs improvement in several areas")
            print("   • Focus on failed prompt patterns and service coordination")
            print("   • Review error logs and optimize processing")
        else:
            print("   • Critical issues detected - immediate attention required")
            print("   • Review service availability and configuration")
            print("   • Check network connectivity and service dependencies")
        
        # Test completion timestamp
        print(f"\n⏰ Test Completed: {datetime.now().isoformat()}")
        print("=" * 80)
        
        # Save detailed results to file
        try:
            with open("prompt_engineering_test_results.json", "w", encoding="utf-8") as f:
                json.dump({
                    "test_summary": {
                        "total_tests": total_tests,
                        "passed_tests": passed_tests,
                        "overall_success_rate": overall_success_rate,
                        "test_timestamp": datetime.now().isoformat()
                    },
                    "detailed_results": self.test_results
                }, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Detailed results saved to: prompt_engineering_test_results.json")
            
        except Exception as e:
            print(f"\n⚠️ Could not save results file: {str(e)}")

async def main():
    """Ana test fonksiyonu"""
    print("🚀 AURA AI Feedback Loop - Advanced Prompt Engineering Test Suite")
    print("=" * 80)
    print("Testing advanced prompt engineering patterns and flow engineering...")
    print()
    
    tester = PromptEngineeringTester()
    success = await tester.run_comprehensive_tests()
    
    if success:
        print("\n🎉 Test suite completed successfully!")
        return 0
    else:
        print("\n❌ Test suite failed to complete.")
        return 1

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        sys.exit(result)
    except KeyboardInterrupt:
        print("\n⏹️ Test suite interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test suite crashed: {str(e)}")
        sys.exit(1)
