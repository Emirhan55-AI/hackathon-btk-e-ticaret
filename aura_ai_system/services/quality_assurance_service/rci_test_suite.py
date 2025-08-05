# 🧠 AURA AI Quality Assurance - RCI SYSTEM TEST SUITE
# Comprehensive testing script for Recursive Criticism and Improvement engine

import asyncio
import json
import sys
import time
from typing import Dict, List, Any
import httpx
from datetime import datetime

class AuraRCITestSuite:
    """
    Comprehensive test suite for the AURA AI RCI (Recursive Criticism and Improvement) system.
    Tests all validation capabilities, service integration, and quality assurance features.
    """
    
    def __init__(self, base_url: str = "http://localhost:8008"):
        """
        Initialize the test suite with the RCI service base URL.
        
        Args:
            base_url: Base URL of the RCI Quality Assurance service
        """
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        self.test_results = []
        
        # Define comprehensive test scenarios
        self.test_scenarios = [
            {
                "name": "Critical Color Clash - Red + Green Work Outfit",
                "category": "color_harmony",
                "ai_output": {
                    "items": [
                        {"type": "shirt", "color": "red", "name": "Bright red dress shirt"},
                        {"type": "pants", "color": "green", "name": "Forest green formal pants"},
                        {"type": "shoes", "color": "black", "name": "Black leather shoes"}
                    ],
                    "colors": ["red", "green", "black"],
                    "style_tags": ["business", "formal"],
                    "confidence": 0.75
                },
                "context": {
                    "service_source": "combination_engine",
                    "occasion": "work",
                    "user_id": "test_user_001",
                    "user_preferences": {"style": "conservative", "colors": ["blue", "white", "gray"]},
                    "season": "summer"
                },
                "expected_issues": ["color_harmony"],
                "expected_status": ["needs_improvement", "rejected"],
                "expected_min_suggestions": 2
            },
            {
                "name": "Excellent Classic Combination - Black Dress + Red Accessories",
                "category": "color_harmony",
                "ai_output": {
                    "items": [
                        {"type": "dress", "color": "black", "name": "Classic black cocktail dress"},
                        {"type": "shoes", "color": "red", "name": "Red patent leather heels"},
                        {"type": "accessories", "color": "red", "name": "Red statement necklace"}
                    ],
                    "colors": ["black", "red"],
                    "style_tags": ["elegant", "formal", "classic"],
                    "confidence": 0.92
                },
                "context": {
                    "service_source": "recommendation_engine",
                    "occasion": "dinner",
                    "user_id": "test_user_002",
                    "user_preferences": {"style": "bold", "colors": ["black", "red", "white"]},
                    "season": "winter"
                },
                "expected_issues": [],
                "expected_status": ["approved"],
                "expected_min_suggestions": 0
            },
            {
                "name": "Severe Style Mismatch - Athletic + Formal Mix",
                "category": "style_coherence",
                "ai_output": {
                    "items": [
                        {"type": "pants", "color": "gray", "name": "Sweatpants"},
                        {"type": "shirt", "color": "white", "name": "Formal dress shirt"},
                        {"type": "shoes", "color": "black", "name": "Patent leather formal shoes"},
                        {"type": "accessories", "color": "gold", "name": "Gold cufflinks"}
                    ],
                    "colors": ["gray", "white", "black", "gold"],
                    "style_tags": ["mixed", "athletic", "formal"],
                    "confidence": 0.45
                },
                "context": {
                    "service_source": "combination_engine",
                    "occasion": "business_meeting",
                    "user_id": "test_user_003",
                    "user_preferences": {"style": "professional"},
                    "season": "spring"
                },
                "expected_issues": ["style_coherence"],
                "expected_status": ["rejected"],
                "expected_min_suggestions": 3
            },
            {
                "name": "Perfect Business Casual - Smart Coordination",
                "category": "style_coherence",
                "ai_output": {
                    "items": [
                        {"type": "pants", "color": "navy", "name": "Navy chinos"},
                        {"type": "shirt", "color": "light_blue", "name": "Light blue button-down"},
                        {"type": "shoes", "color": "brown", "name": "Brown leather loafers"},
                        {"type": "jacket", "color": "navy", "name": "Navy blazer"}
                    ],
                    "colors": ["navy", "light_blue", "brown"],
                    "style_tags": ["business_casual", "professional", "polished"],
                    "confidence": 0.88
                },
                "context": {
                    "service_source": "recommendation_engine",
                    "occasion": "business_casual",
                    "user_id": "test_user_004",
                    "user_preferences": {"style": "professional", "colors": ["navy", "blue", "brown"]},
                    "season": "fall"
                },
                "expected_issues": [],
                "expected_status": ["approved"],
                "expected_min_suggestions": 0
            },
            {
                "name": "Multiple Issues - Color + Style Problems",
                "category": "comprehensive",
                "ai_output": {
                    "items": [
                        {"type": "top", "color": "orange", "name": "Bright orange tank top"},
                        {"type": "bottom", "color": "purple", "name": "Purple formal trousers"},
                        {"type": "shoes", "color": "yellow", "name": "Neon yellow sneakers"},
                        {"type": "accessories", "color": "pink", "name": "Pink formal tie"}
                    ],
                    "colors": ["orange", "purple", "yellow", "pink"],
                    "style_tags": ["mixed", "colorful", "casual", "formal"],
                    "confidence": 0.25
                },
                "context": {
                    "service_source": "combination_engine",
                    "occasion": "office_party",
                    "user_id": "test_user_005",
                    "user_preferences": {"style": "conservative"},
                    "season": "summer"
                },
                "expected_issues": ["color_harmony", "style_coherence"],
                "expected_status": ["rejected"],
                "expected_min_suggestions": 4
            }
        ]
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """
        Run the complete RCI test suite and return comprehensive results.
        
        Returns:
            Dictionary containing test results, statistics, and analysis
        """
        print("🧠 AURA AI RCI Quality Assurance - Comprehensive Test Suite")
        print("=" * 80)
        print()
        
        start_time = datetime.now()
        
        # Test 1: Service Health Check
        await self._test_service_health()
        
        # Test 2: Individual Validation Scenarios
        await self._test_validation_scenarios()
        
        # Test 3: Bulk Validation Performance
        await self._test_bulk_validation()
        
        # Test 4: System Capabilities and Validators
        await self._test_system_capabilities()
        
        # Test 5: Predefined Test Scenarios Endpoint
        await self._test_predefined_scenarios()
        
        # Test 6: Edge Cases and Error Handling
        await self._test_edge_cases()
        
        # Calculate overall results
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        results = self._analyze_test_results(duration)
        
        # Display final summary
        self._display_test_summary(results)
        
        await self.client.aclose()
        return results
    
    async def _test_service_health(self):
        """Test RCI service health and basic functionality."""
        print("🏥 Testing Service Health...")
        
        try:
            response = await self.client.get(f"{self.base_url}/")
            
            if response.status_code == 200:
                health_data = response.json()
                self.test_results.append({
                    "test": "service_health",
                    "status": "PASS",
                    "message": f"Service healthy - {health_data.get('rci_engine_status', 'unknown')}",
                    "data": health_data
                })
                print(f"   ✅ Service Status: {health_data.get('status', 'unknown')}")
                print(f"   🔧 RCI Engine: {health_data.get('rci_engine_status', 'unknown')}")
                print(f"   📊 Active Validators: {len(health_data.get('active_validators', []))}")
            else:
                self.test_results.append({
                    "test": "service_health",
                    "status": "FAIL",
                    "message": f"Health check failed with status {response.status_code}",
                    "data": None
                })
                print(f"   ❌ Health check failed: {response.status_code}")
                
        except Exception as e:
            self.test_results.append({
                "test": "service_health",
                "status": "ERROR",
                "message": f"Health check error: {str(e)}",
                "data": None
            })
            print(f"   ❌ Health check error: {str(e)}")
        
        print()
    
    async def _test_validation_scenarios(self):
        """Test individual validation scenarios to verify RCI functionality."""
        print("🧪 Testing Validation Scenarios...")
        
        for i, scenario in enumerate(self.test_scenarios, 1):
            print(f"   Test {i}/{len(self.test_scenarios)}: {scenario['name']}")
            
            try:
                # Prepare validation request
                validation_request = {
                    "ai_output": scenario["ai_output"],
                    "context": scenario["context"]
                }
                
                # Send validation request
                response = await self.client.post(
                    f"{self.base_url}/validate",
                    json=validation_request
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Analyze the validation result
                    analysis = self._analyze_scenario_result(scenario, result)
                    
                    self.test_results.append({
                        "test": f"scenario_{i}",
                        "scenario_name": scenario["name"],
                        "status": "PASS" if analysis["meets_expectations"] else "FAIL",
                        "message": analysis["summary"],
                        "data": {
                            "validation_result": result,
                            "analysis": analysis
                        }
                    })
                    
                    # Display result summary
                    status_symbol = "✅" if analysis["meets_expectations"] else "❌"
                    print(f"      {status_symbol} Status: {result['status']} (Score: {result['overall_score']:.2f})")
                    print(f"         Issues: {result['issues_found']}, Critical: {result['critical_issues_found']}")
                    
                else:
                    self.test_results.append({
                        "test": f"scenario_{i}",
                        "scenario_name": scenario["name"],
                        "status": "ERROR",
                        "message": f"Validation request failed: {response.status_code}",
                        "data": None
                    })
                    print(f"      ❌ Request failed: {response.status_code}")
                
            except Exception as e:
                self.test_results.append({
                    "test": f"scenario_{i}",
                    "scenario_name": scenario["name"],
                    "status": "ERROR",
                    "message": f"Scenario test error: {str(e)}",
                    "data": None
                })
                print(f"      ❌ Error: {str(e)}")
            
            # Brief delay between tests
            await asyncio.sleep(0.5)
        
        print()
    
    async def _test_bulk_validation(self):
        """Test bulk validation performance and functionality."""
        print("📦 Testing Bulk Validation...")
        
        try:
            # Create bulk validation request with multiple scenarios
            bulk_request = {
                "validation_requests": [
                    {
                        "ai_output": scenario["ai_output"],
                        "context": scenario["context"]
                    }
                    for scenario in self.test_scenarios[:3]  # Use first 3 scenarios
                ],
                "processing_mode": "parallel"
            }
            
            start_time = time.time()
            response = await self.client.post(
                f"{self.base_url}/validate-bulk",
                json=bulk_request
            )
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                
                processing_time = (end_time - start_time) * 1000  # Convert to milliseconds
                
                self.test_results.append({
                    "test": "bulk_validation",
                    "status": "PASS",
                    "message": f"Bulk validation successful: {result['successful_validations']}/{result['total_requests']}",
                    "data": {
                        "bulk_result": result,
                        "actual_processing_time_ms": processing_time
                    }
                })
                
                print(f"   ✅ Bulk validation completed")
                print(f"      📊 Success Rate: {result['successful_validations']}/{result['total_requests']}")
                print(f"      ⏱️  Processing Time: {result['processing_duration_ms']:.1f}ms")
                print(f"      📈 Average Score: {result['summary_statistics']['score_statistics']['average_overall_score']:.2f}")
                
            else:
                self.test_results.append({
                    "test": "bulk_validation",
                    "status": "FAIL",
                    "message": f"Bulk validation failed: {response.status_code}",
                    "data": None
                })
                print(f"   ❌ Bulk validation failed: {response.status_code}")
                
        except Exception as e:
            self.test_results.append({
                "test": "bulk_validation",
                "status": "ERROR",
                "message": f"Bulk validation error: {str(e)}",
                "data": None
            })
            print(f"   ❌ Bulk validation error: {str(e)}")
        
        print()
    
    async def _test_system_capabilities(self):
        """Test system capabilities and validator information."""
        print("🔍 Testing System Capabilities...")
        
        try:
            response = await self.client.get(f"{self.base_url}/validators")
            
            if response.status_code == 200:
                validators_info = response.json()
                
                self.test_results.append({
                    "test": "system_capabilities",
                    "status": "PASS",
                    "message": f"Validators info retrieved: {len(validators_info.get('active_validators', []))} active",
                    "data": validators_info
                })
                
                print(f"   ✅ System capabilities retrieved")
                print(f"      🧠 System: {validators_info.get('system_info', {}).get('name', 'unknown')}")
                print(f"      📊 Active Validators: {', '.join(validators_info.get('active_validators', []))}")
                print(f"      🎯 Capabilities: {len(validators_info.get('capabilities', []))} features")
                
            else:
                self.test_results.append({
                    "test": "system_capabilities",
                    "status": "FAIL",
                    "message": f"Capabilities request failed: {response.status_code}",
                    "data": None
                })
                print(f"   ❌ Capabilities request failed: {response.status_code}")
                
        except Exception as e:
            self.test_results.append({
                "test": "system_capabilities",
                "status": "ERROR",
                "message": f"Capabilities test error: {str(e)}",
                "data": None
            })
            print(f"   ❌ Capabilities test error: {str(e)}")
        
        print()
    
    async def _test_predefined_scenarios(self):
        """Test the predefined test scenarios endpoint."""
        print("🎯 Testing Predefined Scenarios...")
        
        try:
            response = await self.client.post(f"{self.base_url}/test-scenarios")
            
            if response.status_code == 200:
                test_result = response.json()
                
                success_rate = test_result.get("test_summary", {}).get("success_rate_percent", 0)
                
                self.test_results.append({
                    "test": "predefined_scenarios",
                    "status": "PASS" if success_rate >= 80 else "FAIL",
                    "message": f"Predefined scenarios: {success_rate}% success rate",
                    "data": test_result
                })
                
                print(f"   ✅ Predefined scenarios completed")
                print(f"      📊 Success Rate: {success_rate}%")
                print(f"      🧪 Total Scenarios: {test_result.get('test_summary', {}).get('total_scenarios', 0)}")
                print(f"      🎯 System Status: {test_result.get('system_status', 'unknown')}")
                
            else:
                self.test_results.append({
                    "test": "predefined_scenarios",
                    "status": "FAIL",
                    "message": f"Predefined scenarios failed: {response.status_code}",
                    "data": None
                })
                print(f"   ❌ Predefined scenarios failed: {response.status_code}")
                
        except Exception as e:
            self.test_results.append({
                "test": "predefined_scenarios",
                "status": "ERROR",
                "message": f"Predefined scenarios error: {str(e)}",
                "data": None
            })
            print(f"   ❌ Predefined scenarios error: {str(e)}")
        
        print()
    
    async def _test_edge_cases(self):
        """Test edge cases and error handling."""
        print("🔬 Testing Edge Cases...")
        
        edge_cases = [
            {
                "name": "Empty AI Output",
                "request": {"ai_output": {}, "context": {"service_source": "test"}},
                "expect_error": False
            },
            {
                "name": "Invalid Color Names",
                "request": {
                    "ai_output": {
                        "items": [{"type": "shirt", "color": "invalid_color_xyz"}],
                        "colors": ["invalid_color_xyz"]
                    },
                    "context": {"service_source": "test"}
                },
                "expect_error": False
            },
            {
                "name": "Missing Context",
                "request": {"ai_output": {"items": [{"type": "shirt", "color": "blue"}]}},
                "expect_error": True
            }
        ]
        
        for i, case in enumerate(edge_cases, 1):
            print(f"   Edge Case {i}: {case['name']}")
            
            try:
                response = await self.client.post(
                    f"{self.base_url}/validate",
                    json=case["request"]
                )
                
                if case["expect_error"]:
                    if response.status_code != 200:
                        print(f"      ✅ Expected error handled correctly: {response.status_code}")
                        status = "PASS"
                    else:
                        print(f"      ❌ Expected error but got success")
                        status = "FAIL"
                else:
                    if response.status_code == 200:
                        print(f"      ✅ Edge case handled gracefully")
                        status = "PASS"
                    else:
                        print(f"      ❌ Edge case failed: {response.status_code}")
                        status = "FAIL"
                
                self.test_results.append({
                    "test": f"edge_case_{i}",
                    "status": status,
                    "message": f"Edge case '{case['name']}': {response.status_code}",
                    "data": {"case": case, "response_code": response.status_code}
                })
                
            except Exception as e:
                self.test_results.append({
                    "test": f"edge_case_{i}",
                    "status": "ERROR",
                    "message": f"Edge case error: {str(e)}",
                    "data": None
                })
                print(f"      ❌ Error: {str(e)}")
        
        print()
    
    def _analyze_scenario_result(self, scenario: Dict, result: Dict) -> Dict[str, Any]:
        """
        Analyze a validation result against scenario expectations.
        
        Args:
            scenario: The test scenario definition
            result: The validation result from RCI system
            
        Returns:
            Analysis of how well the result meets expectations
        """
        analysis = {
            "meets_expectations": True,
            "summary": "",
            "details": []
        }
        
        # Check if status matches expectations
        expected_statuses = scenario.get("expected_status", [])
        actual_status = result.get("status", "unknown")
        
        if expected_statuses and actual_status not in expected_statuses:
            analysis["meets_expectations"] = False
            analysis["details"].append(f"Status mismatch: expected {expected_statuses}, got {actual_status}")
        
        # Check if expected issues were found
        expected_issues = scenario.get("expected_issues", [])
        actual_issues = [issue.get("category") for issue in result.get("issues", [])]
        
        for expected_issue in expected_issues:
            if expected_issue not in actual_issues:
                analysis["meets_expectations"] = False
                analysis["details"].append(f"Expected issue '{expected_issue}' not found")
        
        # Check if minimum suggestions were provided
        min_suggestions = scenario.get("expected_min_suggestions", 0)
        actual_suggestions = len(result.get("improvement_suggestions", []))
        
        if actual_suggestions < min_suggestions:
            analysis["meets_expectations"] = False
            analysis["details"].append(f"Insufficient suggestions: expected >={min_suggestions}, got {actual_suggestions}")
        
        # Generate summary
        if analysis["meets_expectations"]:
            analysis["summary"] = "All expectations met"
        else:
            analysis["summary"] = f"{len(analysis['details'])} expectation(s) not met"
        
        return analysis
    
    def _analyze_test_results(self, duration: float) -> Dict[str, Any]:
        """
        Analyze all test results and generate comprehensive summary.
        
        Args:
            duration: Total test duration in seconds
            
        Returns:
            Comprehensive test analysis
        """
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        error_tests = len([r for r in self.test_results if r["status"] == "ERROR"])
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        return {
            "test_summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "error_tests": error_tests,
                "success_rate_percent": success_rate,
                "duration_seconds": duration,
                "timestamp": datetime.now().isoformat()
            },
            "detailed_results": self.test_results,
            "overall_status": "HEALTHY" if success_rate >= 90 else "NEEDS_ATTENTION" if success_rate >= 70 else "CRITICAL",
            "recommendations": self._generate_recommendations(success_rate, failed_tests, error_tests)
        }
    
    def _generate_recommendations(self, success_rate: float, failed_tests: int, error_tests: int) -> List[str]:
        """Generate recommendations based on test results."""
        recommendations = []
        
        if success_rate < 70:
            recommendations.append("Critical: RCI system needs immediate attention - low success rate")
        
        if failed_tests > 0:
            recommendations.append(f"Review {failed_tests} failed test(s) for functional issues")
        
        if error_tests > 0:
            recommendations.append(f"Investigate {error_tests} error(s) for technical problems")
        
        if success_rate >= 90:
            recommendations.append("Excellent: RCI system is performing optimally")
        
        return recommendations
    
    def _display_test_summary(self, results: Dict[str, Any]):
        """Display a comprehensive test summary."""
        print("📊 AURA AI RCI Quality Assurance - Test Summary")
        print("=" * 80)
        
        summary = results["test_summary"]
        
        print(f"🎯 Overall Status: {results['overall_status']}")
        print(f"📊 Test Results: {summary['passed_tests']}/{summary['total_tests']} passed ({summary['success_rate_percent']:.1f}%)")
        print(f"⚠️  Failed Tests: {summary['failed_tests']}")
        print(f"❌ Error Tests: {summary['error_tests']}")
        print(f"⏱️  Duration: {summary['duration_seconds']:.1f} seconds")
        print()
        
        if results["recommendations"]:
            print("💡 Recommendations:")
            for rec in results["recommendations"]:
                print(f"   • {rec}")
            print()
        
        # Display detailed results for failed/error tests
        problematic_tests = [r for r in self.test_results if r["status"] in ["FAIL", "ERROR"]]
        if problematic_tests:
            print("🔍 Detailed Issues:")
            for test in problematic_tests:
                print(f"   ❌ {test['test']}: {test['message']}")
            print()
        
        print("✅ RCI Quality Assurance Test Suite Completed")

async def main():
    """Main function to run the RCI test suite."""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:8008"
    
    print(f"🧠 Testing AURA AI RCI System at: {base_url}")
    print()
    
    test_suite = AuraRCITestSuite(base_url)
    results = await test_suite.run_all_tests()
    
    # Save results to file
    with open("rci_test_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"📄 Detailed results saved to: rci_test_results.json")
    
    # Exit with appropriate code
    if results["overall_status"] == "CRITICAL":
        sys.exit(1)
    elif results["overall_status"] == "NEEDS_ATTENTION":
        sys.exit(2)
    else:
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
