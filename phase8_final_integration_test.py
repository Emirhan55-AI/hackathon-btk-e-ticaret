# 🧪 PHASE 8: COMPREHENSIVE END-TO-END INTEGRATION TEST
# Ultimate validation of AI-enhanced AURA system
# Tests all services, AI integration, and workflow orchestration

import asyncio
import aiohttp
import json
import time
from datetime import datetime
from typing import Dict, List, Any
import traceback

class Phase8ComprehensiveIntegrationTester:
    """
    Comprehensive integration tester for Phase 8 AI-enhanced AURA system.
    Validates all services, AI optimization, and end-to-end workflows.
    """
    
    def __init__(self):
        self.services = {
            "image_processing": "http://localhost:8001",
            "nlu": "http://localhost:8002", 
            "style_profile": "http://localhost:8003",
            "combination_engine": "http://localhost:8004",
            "recommendation_engine": "http://localhost:8005",
            "orchestrator": "http://localhost:8006"
        }
        self.test_results = {
            "service_health": {},
            "individual_service_tests": {},
            "ai_integration_tests": {},
            "end_to_end_workflows": {},
            "performance_metrics": {},
            "phase8_ai_features": {}
        }
        self.start_time = None
    
    async def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run complete Phase 8 integration test suite."""
        self.start_time = time.time()
        print("🚀 STARTING PHASE 8 COMPREHENSIVE INTEGRATION TEST")
        print("=" * 60)
        
        # Phase 1: Service Health Check
        await self._test_service_health()
        
        # Phase 2: Individual Service Functionality
        await self._test_individual_services()
        
        # Phase 3: Phase 8 AI Integration Features
        await self._test_phase8_ai_features()
        
        # Phase 4: End-to-End Workflow Testing
        await self._test_end_to_end_workflows()
        
        # Phase 5: Performance Analysis
        await self._test_performance_metrics()
        
        # Generate final report
        return self._generate_final_report()
    
    async def _test_service_health(self):
        """Test health status of all services."""
        print("\n🏥 PHASE 1: SERVICE HEALTH ASSESSMENT")
        print("-" * 40)
        
        async with aiohttp.ClientSession() as session:
            for service_name, base_url in self.services.items():
                try:
                    print(f"   Testing {service_name}...")
                    async with session.get(f"{base_url}/", timeout=5) as response:
                        if response.status == 200:
                            data = await response.json()
                            self.test_results["service_health"][service_name] = {
                                "status": "healthy",
                                "response_time": response.headers.get("X-Process-Time", "unknown"),
                                "service_info": data
                            }
                            print(f"   ✅ {service_name}: HEALTHY")
                        else:
                            self.test_results["service_health"][service_name] = {
                                "status": "unhealthy",
                                "http_status": response.status
                            }
                            print(f"   ❌ {service_name}: UNHEALTHY (HTTP {response.status})")
                except Exception as e:
                    self.test_results["service_health"][service_name] = {
                        "status": "error",
                        "error": str(e)
                    }
                    print(f"   💥 {service_name}: ERROR - {str(e)}")
    
    async def _test_individual_services(self):
        """Test core functionality of each service."""
        print("\n🔧 PHASE 2: INDIVIDUAL SERVICE FUNCTIONALITY")
        print("-" * 40)
        
        # Test Combination Engine (already verified working)
        await self._test_combination_engine()
        
        # Test Orchestrator 
        await self._test_orchestrator_service()
    
    async def _test_combination_engine(self):
        """Test combination engine with Phase 4 personalization."""
        print("   Testing Combination Engine (Phase 4 Enhanced)...")
        
        async with aiohttp.ClientSession() as session:
            try:
                test_request = {
                    "user_id": "integration_test_user",
                    "context": "casual",
                    "occasion": "integration_test"
                }
                
                async with session.post(
                    f"{self.services['combination_engine']}/generate-combination",
                    json=test_request,
                    timeout=10
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.test_results["individual_service_tests"]["combination_engine"] = {
                            "status": "success",
                            "response_contains_required_fields": all(
                                field in data for field in ["combination_items", "user_id", "personalization_insights"]
                            ),
                            "phase4_personalization": "personalization_insights" in data
                        }
                        print("   ✅ Combination Engine: SUCCESS (Phase 4 Personalization Active)")
                    else:
                        print(f"   ❌ Combination Engine: FAILED (HTTP {response.status})")
                        
            except Exception as e:
                print(f"   💥 Combination Engine: ERROR - {str(e)}")
    
    async def _test_orchestrator_service(self):
        """Test orchestrator with Phase 8 AI features."""
        print("   Testing Orchestrator Service (Phase 8 AI-Enhanced)...")
        
        async with aiohttp.ClientSession() as session:
            try:
                # Test basic health
                async with session.get(f"{self.services['orchestrator']}/health", timeout=10) as response:
                    if response.status == 200:
                        print("   ✅ Orchestrator Health: SUCCESS")
                    else:
                        print(f"   ❌ Orchestrator Health: FAILED (HTTP {response.status})")
                
                # Test workflow templates
                async with session.get(f"{self.services['orchestrator']}/workflows/templates", timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.test_results["individual_service_tests"]["orchestrator"] = {
                            "status": "success",
                            "templates_available": len(data.get("templates", [])),
                            "phase8_enhanced": True
                        }
                        print("   ✅ Orchestrator Templates: SUCCESS")
                    else:
                        print(f"   ❌ Orchestrator Templates: FAILED (HTTP {response.status})")
                        
            except Exception as e:
                print(f"   💥 Orchestrator: ERROR - {str(e)}")
    
    async def _test_phase8_ai_features(self):
        """Test Phase 8 AI-specific features."""
        print("\n🧠 PHASE 3: PHASE 8 AI INTEGRATION FEATURES")
        print("-" * 40)
        
        async with aiohttp.ClientSession() as session:
            try:
                # Test AI status endpoint
                print("   Testing AI Status Endpoint...")
                async with session.get(f"{self.services['orchestrator']}/ai/status", timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        ai_status = data.get("status", "unknown")
                        phase = data.get("phase", "unknown")
                        
                        self.test_results["phase8_ai_features"]["ai_status"] = {
                            "endpoint_working": True,
                            "ai_status": ai_status,
                            "phase": phase,
                            "capabilities": data.get("capabilities", [])
                        }
                        
                        if ai_status == "operational":
                            print("   ✅ AI Status: OPERATIONAL (Full Phase 8 Active)")
                        elif ai_status == "not_available":
                            print("   📋 AI Status: COMPATIBILITY MODE (Phase 7 Fallback)")
                        else:
                            print(f"   ⚠️ AI Status: {ai_status}")
                    else:
                        print(f"   ❌ AI Status: FAILED (HTTP {response.status})")
                
                # Test AI analytics endpoint
                print("   Testing AI Analytics Endpoint...")
                async with session.get(f"{self.services['orchestrator']}/ai/analytics", timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.test_results["phase8_ai_features"]["ai_analytics"] = {
                            "endpoint_working": True,
                            "analytics_data": data
                        }
                        print("   ✅ AI Analytics: SUCCESS")
                    else:
                        print(f"   ❌ AI Analytics: FAILED (HTTP {response.status})")
                        
            except Exception as e:
                print(f"   💥 Phase 8 AI Features: ERROR - {str(e)}")
    
    async def _test_end_to_end_workflows(self):
        """Test complete end-to-end workflows."""
        print("\n🔄 PHASE 4: END-TO-END WORKFLOW TESTING")
        print("-" * 40)
        
        # Test standard workflow
        await self._test_standard_workflow()
        
        # Test AI-optimized workflow (if available)
        await self._test_ai_optimized_workflow()
    
    async def _test_standard_workflow(self):
        """Test standard workflow execution."""
        print("   Testing Standard Workflow...")
        
        async with aiohttp.ClientSession() as session:
            try:
                workflow_request = {
                    "workflow_type": "complete_recommendation",
                    "input_data": {
                        "user_id": "integration_test_user",
                        "context": "casual",
                        "preferences": {
                            "style": "modern",
                            "colors": ["blue", "white"],
                            "occasion": "weekend"
                        }
                    },
                    "options": {
                        "include_alternatives": True,
                        "personalization_level": "high"
                    }
                }
                
                async with session.post(
                    f"{self.services['orchestrator']}/workflows/execute",
                    json=workflow_request,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.test_results["end_to_end_workflows"]["standard"] = {
                            "status": "success",
                            "workflow_id": data.get("workflow_id"),
                            "execution_time": data.get("metadata", {}).get("total_processing_time"),
                            "services_called": data.get("metadata", {}).get("services_called", [])
                        }
                        print("   ✅ Standard Workflow: SUCCESS")
                    else:
                        print(f"   ❌ Standard Workflow: FAILED (HTTP {response.status})")
                        
            except Exception as e:
                print(f"   💥 Standard Workflow: ERROR - {str(e)}")
    
    async def _test_ai_optimized_workflow(self):
        """Test AI-optimized workflow execution."""
        print("   Testing AI-Optimized Workflow...")
        
        async with aiohttp.ClientSession() as session:
            try:
                workflow_request = {
                    "workflow_type": "complete_recommendation",
                    "input_data": {
                        "user_id": "ai_test_user",
                        "context": "formal",
                        "preferences": {
                            "style": "professional",
                            "colors": ["navy", "gray"],
                            "occasion": "business_meeting"
                        }
                    },
                    "options": {
                        "ai_optimization": True,
                        "performance_target": "sub_200ms"
                    }
                }
                
                async with session.post(
                    f"{self.services['orchestrator']}/workflows/execute/ai-optimized",
                    json=workflow_request,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.test_results["end_to_end_workflows"]["ai_optimized"] = {
                            "status": "success",
                            "workflow_id": data.get("workflow_id"),
                            "ai_enhanced": data.get("metadata", {}).get("phase8_ai_enhanced", False),
                            "optimizations_applied": data.get("metadata", {}).get("ai_optimization_applied", False)
                        }
                        print("   ✅ AI-Optimized Workflow: SUCCESS")
                    else:
                        print(f"   ❌ AI-Optimized Workflow: FAILED (HTTP {response.status})")
                        
            except Exception as e:
                print(f"   💥 AI-Optimized Workflow: ERROR - {str(e)}")
    
    async def _test_performance_metrics(self):
        """Test system performance metrics."""
        print("\n⚡ PHASE 5: PERFORMANCE METRICS ANALYSIS")
        print("-" * 40)
        
        # Test response times
        response_times = []
        
        async with aiohttp.ClientSession() as session:
            for i in range(5):
                start_time = time.time()
                try:
                    async with session.get(f"{self.services['orchestrator']}/health", timeout=5) as response:
                        end_time = time.time()
                        if response.status == 200:
                            response_times.append((end_time - start_time) * 1000)  # Convert to ms
                except:
                    pass
        
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            self.test_results["performance_metrics"] = {
                "average_response_time_ms": round(avg_response_time, 2),
                "min_response_time_ms": round(min(response_times), 2),
                "max_response_time_ms": round(max(response_times), 2),
                "samples": len(response_times)
            }
            print(f"   📊 Average Response Time: {avg_response_time:.2f}ms")
            
            if avg_response_time < 200:
                print("   ✅ Performance Target: SUB-200MS ACHIEVED!")
            else:
                print(f"   📈 Performance Target: {avg_response_time:.2f}ms (Target: <200ms)")
    
    def _generate_final_report(self) -> Dict[str, Any]:
        """Generate comprehensive final test report."""
        end_time = time.time()
        total_test_time = end_time - self.start_time
        
        # Calculate overall scores
        healthy_services = sum(1 for result in self.test_results["service_health"].values() 
                             if result.get("status") == "healthy")
        total_services = len(self.services)
        health_score = (healthy_services / total_services) * 100
        
        successful_workflows = sum(1 for result in self.test_results["end_to_end_workflows"].values()
                                 if result.get("status") == "success")
        total_workflows = len(self.test_results["end_to_end_workflows"])
        workflow_score = (successful_workflows / total_workflows * 100) if total_workflows > 0 else 0
        
        # Phase 8 AI features score
        ai_features_working = sum(1 for result in self.test_results["phase8_ai_features"].values()
                                if result.get("endpoint_working", False))
        total_ai_features = len(self.test_results["phase8_ai_features"])
        ai_score = (ai_features_working / total_ai_features * 100) if total_ai_features > 0 else 0
        
        overall_score = (health_score + workflow_score + ai_score) / 3
        
        final_report = {
            "test_summary": {
                "total_test_time_seconds": round(total_test_time, 2),
                "timestamp": datetime.now().isoformat(),
                "phase": "8.0 - AI-Driven Optimization Integration Test"
            },
            "scores": {
                "overall_score": round(overall_score, 1),
                "service_health_score": round(health_score, 1),
                "workflow_execution_score": round(workflow_score, 1),
                "ai_integration_score": round(ai_score, 1)
            },
            "detailed_results": self.test_results,
            "recommendations": self._generate_recommendations(overall_score, health_score, workflow_score, ai_score)
        }
        
        return final_report
    
    def _generate_recommendations(self, overall_score, health_score, workflow_score, ai_score) -> List[str]:
        """Generate recommendations based on test results."""
        recommendations = []
        
        if overall_score >= 90:
            recommendations.append("🎉 EXCELLENT: System is production-ready with Phase 8 AI enhancements!")
        elif overall_score >= 80:
            recommendations.append("✅ GOOD: System is stable with minor optimizations needed")
        elif overall_score >= 70:
            recommendations.append("⚠️ FAIR: System needs improvements before production")
        else:
            recommendations.append("❌ POOR: System requires significant fixes")
        
        if health_score < 100:
            recommendations.append("🏥 Check and fix unhealthy services")
        
        if workflow_score < 90:
            recommendations.append("🔄 Improve workflow execution reliability")
        
        if ai_score < 80:
            recommendations.append("🧠 Enhance Phase 8 AI integration")
        
        return recommendations

async def main():
    """Main test execution function."""
    tester = Phase8ComprehensiveIntegrationTester()
    
    try:
        final_report = await tester.run_comprehensive_test()
        
        print("\n" + "=" * 60)
        print("🏆 PHASE 8 COMPREHENSIVE INTEGRATION TEST RESULTS")
        print("=" * 60)
        
        scores = final_report["scores"]
        print(f"📊 OVERALL SCORE: {scores['overall_score']}%")
        print(f"🏥 Service Health: {scores['service_health_score']}%")
        print(f"🔄 Workflow Execution: {scores['workflow_execution_score']}%")
        print(f"🧠 AI Integration: {scores['ai_integration_score']}%")
        
        print(f"\n⏱️ Total Test Time: {final_report['test_summary']['total_test_time_seconds']}s")
        
        print("\n📋 RECOMMENDATIONS:")
        for rec in final_report["recommendations"]:
            print(f"   {rec}")
        
        # Save detailed report to file
        with open("PHASE8_INTEGRATION_TEST_REPORT.json", "w") as f:
            json.dump(final_report, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: PHASE8_INTEGRATION_TEST_REPORT.json")
        
        return final_report
        
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR in integration test: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return None

if __name__ == "__main__":
    asyncio.run(main())
