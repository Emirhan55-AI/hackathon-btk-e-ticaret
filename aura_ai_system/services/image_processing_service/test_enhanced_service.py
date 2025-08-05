#!/usr/bin/env python3
"""
🚀 AURA AI - Enhanced Image Processing Service Test Suite
Computer Vision & AI Engineer: Enhanced Testing for Turkish Fashion Analysis

Test Categories:
1. Service Startup & Health Check
2. Enhanced CV Engine Validation  
3. Prompt Engineering Pattern Testing
4. Turkish Fashion Analysis Validation
5. Service Coordination Testing
6. Performance & Reliability Testing
"""

import asyncio
import base64
import json
import logging
import time
from typing import Dict, Any
import requests
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedImageProcessingTester:
    """Comprehensive test suite for enhanced image processing service"""
    
    def __init__(self, service_url: str = "http://localhost:8002"):
        self.service_url = service_url
        self.test_results = {
            "startup_health": {"passed": 0, "failed": 0, "tests": []},
            "cv_engine": {"passed": 0, "failed": 0, "tests": []},
            "prompt_patterns": {"passed": 0, "failed": 0, "tests": []},
            "turkish_analysis": {"passed": 0, "failed": 0, "tests": []},
            "service_coordination": {"passed": 0, "failed": 0, "tests": []},
            "performance": {"passed": 0, "failed": 0, "tests": []}
        }
    
    def create_test_image_data(self) -> str:
        """Create a minimal test image as base64"""
        # Create a simple 10x10 RGB image (red square)
        import io
        from PIL import Image
        
        img = Image.new('RGB', (100, 100), color='red')
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        return base64.b64encode(buffer.getvalue()).decode()
    
    async def test_service_health(self) -> bool:
        """Test basic service health and startup"""
        logger.info("🔍 Testing service health and startup...")
        
        try:
            # Test health endpoint
            response = requests.get(f"{self.service_url}/health", timeout=10)
            
            if response.status_code == 200:
                health_data = response.json()
                self.test_results["startup_health"]["passed"] += 1
                self.test_results["startup_health"]["tests"].append({
                    "name": "Health Check",
                    "status": "PASSED",
                    "response": health_data
                })
                logger.info("✅ Service health check passed")
                return True
            else:
                raise Exception(f"Health check failed with status {response.status_code}")
                
        except Exception as e:
            self.test_results["startup_health"]["failed"] += 1
            self.test_results["startup_health"]["tests"].append({
                "name": "Health Check",
                "status": "FAILED",
                "error": str(e)
            })
            logger.error(f"❌ Service health check failed: {e}")
            return False
    
    async def test_enhanced_cv_engine(self) -> bool:
        """Test enhanced CV engine functionality"""
        logger.info("🎯 Testing Enhanced CV Engine...")
        
        try:
            test_image = self.create_test_image_data()
            
            test_request = {
                "image_data": test_image,
                "analysis_scenario": "single_shirt_analysis",
                "user_context": {"test_mode": True},
                "enable_service_coordination": False,
                "quality_threshold": 0.6
            }
            
            response = requests.post(
                f"{self.service_url}/analyze/enhanced-prompt-engineering",
                json=test_request,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Validate response structure
                required_fields = ["success", "analysis_id", "scenario_used", "prompt_engineering_metadata"]
                missing_fields = [field for field in required_fields if field not in result]
                
                if not missing_fields and result.get("success"):
                    self.test_results["cv_engine"]["passed"] += 1
                    self.test_results["cv_engine"]["tests"].append({
                        "name": "Enhanced CV Engine Basic Test",
                        "status": "PASSED",
                        "analysis_id": result.get("analysis_id"),
                        "scenario": result.get("scenario_used"),
                        "processing_time": result.get("processing_time_ms")
                    })
                    logger.info("✅ Enhanced CV Engine test passed")
                    return True
                else:
                    raise Exception(f"Invalid response structure or failed analysis. Missing: {missing_fields}")
            else:
                raise Exception(f"CV Engine test failed with status {response.status_code}")
                
        except Exception as e:
            self.test_results["cv_engine"]["failed"] += 1
            self.test_results["cv_engine"]["tests"].append({
                "name": "Enhanced CV Engine Basic Test",
                "status": "FAILED",
                "error": str(e)
            })
            logger.error(f"❌ Enhanced CV Engine test failed: {e}")
            return False
    
    async def test_prompt_patterns(self) -> bool:
        """Test all 4 prompt engineering patterns"""
        logger.info("🔧 Testing Prompt Engineering Patterns...")
        
        patterns_to_test = ["persona", "recipe", "template", "context_instruction"]
        test_image = self.create_test_image_data()
        
        pattern_results = []
        
        for pattern in patterns_to_test:
            try:
                test_request = {
                    "image_data": test_image,
                    "analysis_scenario": "single_dress_analysis",
                    "prompt_pattern": pattern,
                    "user_context": {"pattern_test": pattern},
                    "enable_service_coordination": False
                }
                
                response = requests.post(
                    f"{self.service_url}/analyze/enhanced-prompt-engineering",
                    json=test_request,
                    timeout=25
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        pattern_results.append(f"✅ {pattern}: PASSED")
                        self.test_results["prompt_patterns"]["passed"] += 1
                    else:
                        pattern_results.append(f"❌ {pattern}: FAILED - Analysis unsuccessful")
                        self.test_results["prompt_patterns"]["failed"] += 1
                else:
                    pattern_results.append(f"❌ {pattern}: FAILED - HTTP {response.status_code}")
                    self.test_results["prompt_patterns"]["failed"] += 1
                    
            except Exception as e:
                pattern_results.append(f"❌ {pattern}: FAILED - {str(e)}")
                self.test_results["prompt_patterns"]["failed"] += 1
        
        self.test_results["prompt_patterns"]["tests"].append({
            "name": "All Prompt Patterns Test",
            "results": pattern_results
        })
        
        successful_patterns = len([r for r in pattern_results if "PASSED" in r])
        logger.info(f"🎯 Prompt Patterns Test: {successful_patterns}/{len(patterns_to_test)} patterns working")
        
        return successful_patterns > 0
    
    async def test_turkish_analysis(self) -> bool:
        """Test Turkish fashion analysis capabilities"""
        logger.info("🇹🇷 Testing Turkish Fashion Analysis...")
        
        try:
            test_image = self.create_test_image_data()
            
            test_request = {
                "image_data": test_image,
                "analysis_scenario": "multi_item_analysis",
                "user_context": {
                    "language": "turkish",
                    "cultural_context": "turkish_fashion",
                    "location": "Turkey"
                },
                "enable_service_coordination": True
            }
            
            response = requests.post(
                f"{self.service_url}/analyze/enhanced-prompt-engineering",
                json=test_request,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Check for Turkish-specific features
                turkish_features = []
                
                if result.get("prompt_engineering_metadata", {}).get("turkish_optimization"):
                    turkish_features.append("Turkish optimization enabled")
                
                if result.get("prompt_engineering_metadata", {}).get("cultural_context") == "turkish_fashion":
                    turkish_features.append("Turkish fashion context recognized")
                
                detected_items = result.get("detected_items", [])
                for item in detected_items:
                    if item.get("turkish_description"):
                        turkish_features.append("Turkish descriptions generated")
                        break
                
                if turkish_features:
                    self.test_results["turkish_analysis"]["passed"] += 1
                    self.test_results["turkish_analysis"]["tests"].append({
                        "name": "Turkish Fashion Analysis",
                        "status": "PASSED",
                        "features": turkish_features
                    })
                    logger.info("✅ Turkish Fashion Analysis test passed")
                    logger.info(f"   Features detected: {', '.join(turkish_features)}")
                    return True
                else:
                    raise Exception("No Turkish-specific features detected in response")
            else:
                raise Exception(f"Turkish analysis test failed with status {response.status_code}")
                
        except Exception as e:
            self.test_results["turkish_analysis"]["failed"] += 1
            self.test_results["turkish_analysis"]["tests"].append({
                "name": "Turkish Fashion Analysis",
                "status": "FAILED",
                "error": str(e)
            })
            logger.error(f"❌ Turkish Fashion Analysis test failed: {e}")
            return False
    
    async def test_service_coordination(self) -> bool:
        """Test service coordination functionality"""
        logger.info("🤝 Testing Service Coordination...")
        
        try:
            test_image = self.create_test_image_data()
            
            test_request = {
                "image_data": test_image,
                "analysis_scenario": "accessory_analysis",
                "enable_service_coordination": True,
                "user_context": {"coordination_test": True}
            }
            
            response = requests.post(
                f"{self.service_url}/analyze/enhanced-prompt-engineering",
                json=test_request,
                timeout=35
            )
            
            if response.status_code == 200:
                result = response.json()
                
                coordination_results = result.get("service_coordination_results")
                if coordination_results:
                    coordination_summary = coordination_results.get("coordination_summary", {})
                    services_contacted = coordination_summary.get("total_services_contacted", 0)
                    successful_coordinations = coordination_summary.get("successful_coordinations", 0)
                    
                    self.test_results["service_coordination"]["passed"] += 1
                    self.test_results["service_coordination"]["tests"].append({
                        "name": "Service Coordination Test",
                        "status": "PASSED",
                        "services_contacted": services_contacted,
                        "successful_coordinations": successful_coordinations,
                        "enhanced_features": coordination_summary.get("enhanced_features")
                    })
                    logger.info(f"✅ Service Coordination test passed")
                    logger.info(f"   Services contacted: {services_contacted}, Successful: {successful_coordinations}")
                    return True
                else:
                    raise Exception("No service coordination results in response")
            else:
                raise Exception(f"Service coordination test failed with status {response.status_code}")
                
        except Exception as e:
            self.test_results["service_coordination"]["failed"] += 1
            self.test_results["service_coordination"]["tests"].append({
                "name": "Service Coordination Test",
                "status": "FAILED",
                "error": str(e)
            })
            logger.error(f"❌ Service Coordination test failed: {e}")
            return False
    
    async def test_performance(self) -> bool:
        """Test performance and reliability"""
        logger.info("⚡ Testing Performance & Reliability...")
        
        try:
            test_image = self.create_test_image_data()
            
            # Performance test - 5 consecutive requests
            response_times = []
            for i in range(5):
                start_time = time.time()
                
                test_request = {
                    "image_data": test_image,
                    "analysis_scenario": "auto_detect",
                    "enable_service_coordination": False
                }
                
                response = requests.post(
                    f"{self.service_url}/analyze/enhanced-prompt-engineering",
                    json=test_request,
                    timeout=20
                )
                
                end_time = time.time()
                response_time = (end_time - start_time) * 1000  # Convert to ms
                response_times.append(response_time)
                
                if response.status_code != 200:
                    raise Exception(f"Performance test request {i+1} failed with status {response.status_code}")
            
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            min_response_time = min(response_times)
            
            # Performance criteria: average < 5s, max < 10s
            performance_passed = avg_response_time < 5000 and max_response_time < 10000
            
            self.test_results["performance"]["tests"].append({
                "name": "Performance Test",
                "status": "PASSED" if performance_passed else "FAILED",
                "avg_response_time_ms": avg_response_time,
                "min_response_time_ms": min_response_time,
                "max_response_time_ms": max_response_time,
                "total_requests": len(response_times)
            })
            
            if performance_passed:
                self.test_results["performance"]["passed"] += 1
                logger.info(f"✅ Performance test passed")
                logger.info(f"   Avg: {avg_response_time:.1f}ms, Min: {min_response_time:.1f}ms, Max: {max_response_time:.1f}ms")
            else:
                self.test_results["performance"]["failed"] += 1
                logger.warning(f"⚠️ Performance test concerns")
                logger.warning(f"   Avg: {avg_response_time:.1f}ms, Min: {min_response_time:.1f}ms, Max: {max_response_time:.1f}ms")
            
            return performance_passed
            
        except Exception as e:
            self.test_results["performance"]["failed"] += 1
            self.test_results["performance"]["tests"].append({
                "name": "Performance Test",
                "status": "FAILED",
                "error": str(e)
            })
            logger.error(f"❌ Performance test failed: {e}")
            return False
    
    def generate_test_report(self) -> str:
        """Generate comprehensive test report"""
        
        total_passed = sum(category["passed"] for category in self.test_results.values())
        total_failed = sum(category["failed"] for category in self.test_results.values())
        total_tests = total_passed + total_failed
        
        success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        report = f"""
🚀 AURA AI - Enhanced Image Processing Service Test Report
================================================================

📊 OVERALL RESULTS:
- Total Tests: {total_tests}
- Passed: {total_passed} ✅
- Failed: {total_failed} ❌
- Success Rate: {success_rate:.1f}%

📋 DETAILED RESULTS BY CATEGORY:

"""
        
        category_names = {
            "startup_health": "🔍 Service Startup & Health",
            "cv_engine": "🎯 Enhanced CV Engine",
            "prompt_patterns": "🔧 Prompt Engineering Patterns",
            "turkish_analysis": "🇹🇷 Turkish Fashion Analysis",
            "service_coordination": "🤝 Service Coordination",
            "performance": "⚡ Performance & Reliability"
        }
        
        for category, results in self.test_results.items():
            category_total = results["passed"] + results["failed"]
            category_rate = (results["passed"] / category_total * 100) if category_total > 0 else 0
            
            report += f"{category_names.get(category, category)}\n"
            report += f"   Tests: {category_total}, Passed: {results['passed']}, Failed: {results['failed']} ({category_rate:.1f}%)\n"
            
            for test in results["tests"]:
                status_icon = "✅" if test["status"] == "PASSED" else "❌"
                report += f"   {status_icon} {test['name']}\n"
                
                if test["status"] == "FAILED" and "error" in test:
                    report += f"      Error: {test['error']}\n"
            report += "\n"
        
        report += f"""
🎯 ENHANCED FEATURES VALIDATION:
- Turkish Fashion Analysis: {'✅' if self.test_results['turkish_analysis']['passed'] > 0 else '❌'}
- 4 Prompt Patterns: {'✅' if self.test_results['prompt_patterns']['passed'] > 0 else '❌'}
- Service Coordination: {'✅' if self.test_results['service_coordination']['passed'] > 0 else '❌'}
- Performance Optimization: {'✅' if self.test_results['performance']['passed'] > 0 else '❌'}

🚀 RECOMMENDATION:
{'✅ Service is ready for production deployment!' if success_rate >= 80 else '⚠️ Service needs improvements before deployment.'}

================================================================
Test completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return report
    
    async def run_comprehensive_test(self) -> bool:
        """Run all tests and generate report"""
        logger.info("🚀 Starting Enhanced Image Processing Service Comprehensive Test Suite...")
        logger.info("=" * 80)
        
        test_functions = [
            ("Service Health", self.test_service_health),
            ("Enhanced CV Engine", self.test_enhanced_cv_engine),
            ("Prompt Patterns", self.test_prompt_patterns),
            ("Turkish Analysis", self.test_turkish_analysis),
            ("Service Coordination", self.test_service_coordination),
            ("Performance", self.test_performance)
        ]
        
        overall_success = True
        
        for test_name, test_func in test_functions:
            logger.info(f"🔄 Running {test_name} tests...")
            try:
                result = await test_func()
                if not result:
                    overall_success = False
            except Exception as e:
                logger.error(f"❌ {test_name} test suite failed: {e}")
                overall_success = False
            
            logger.info("-" * 50)
        
        # Generate and save test report
        report = self.generate_test_report()
        
        # Save report to file
        report_file = f"enhanced_service_test_report_{time.strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"📄 Test report saved to: {report_file}")
        logger.info("=" * 80)
        logger.info(report)
        
        return overall_success

async def main():
    """Main test execution"""
    
    print("🚀 AURA AI - Enhanced Image Processing Service Test Suite")
    print("=" * 60)
    print("Computer Vision & AI Engineer Test Validation")
    print("Enhanced Prompt Engineering & Turkish Fashion Analysis")
    print("=" * 60)
    
    # Initialize tester
    tester = EnhancedImageProcessingTester()
    
    # Run comprehensive tests
    success = await tester.run_comprehensive_test()
    
    if success:
        print("\n🎉 ALL TESTS PASSED! Enhanced Image Processing Service is ready!")
    else:
        print("\n⚠️ Some tests failed. Please review the report for details.")
    
    return success

if __name__ == "__main__":
    asyncio.run(main())
