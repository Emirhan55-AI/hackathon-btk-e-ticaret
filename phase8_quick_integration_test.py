# 🧪 PHASE 8: QUICK INTEGRATION TEST
# Simplified version for rapid validation

import requests
import json
import time
from datetime import datetime

class QuickIntegrationTester:
    """Quick integration test for Phase 8 AI-enhanced AURA system."""
    
    def __init__(self):
        self.services = {
            "combination_engine": "http://localhost:8004",
            "orchestrator": "http://localhost:8006"
        }
        self.results = {}
    
    def run_quick_test(self):
        """Run quick integration test."""
        print("🚀 STARTING PHASE 8 QUICK INTEGRATION TEST")
        print("=" * 50)
        
        start_time = time.time()
        
        # Test 1: Service Health
        self.test_service_health()
        
        # Test 2: Core Functionality  
        self.test_core_functionality()
        
        # Test 3: Phase 8 AI Features
        self.test_phase8_ai_features()
        
        # Generate Report
        self.generate_report(time.time() - start_time)
    
    def test_service_health(self):
        """Test basic service health."""
        print("\n🏥 TESTING SERVICE HEALTH")
        print("-" * 30)
        
        for service_name, base_url in self.services.items():
            try:
                print(f"   Testing {service_name}...")
                response = requests.get(f"{base_url}/", timeout=5)
                
                if response.status_code == 200:
                    self.results[f"{service_name}_health"] = "✅ HEALTHY"
                    print(f"   ✅ {service_name}: HEALTHY")
                else:
                    self.results[f"{service_name}_health"] = f"❌ UNHEALTHY ({response.status_code})"
                    print(f"   ❌ {service_name}: UNHEALTHY ({response.status_code})")
                    
            except Exception as e:
                self.results[f"{service_name}_health"] = f"💥 ERROR: {str(e)}"
                print(f"   💥 {service_name}: ERROR - {str(e)}")
    
    def test_core_functionality(self):
        """Test core service functionality."""
        print("\n🔧 TESTING CORE FUNCTIONALITY")
        print("-" * 30)
        
        # Test Combination Engine
        try:
            print("   Testing Combination Generation...")
            response = requests.post(
                f"{self.services['combination_engine']}/generate-combination",
                json={
                    "user_id": "quick_test_user",
                    "context": "casual",
                    "occasion": "test"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                has_required_fields = all(
                    field in data for field in ["combination_items", "user_id", "personalization_insights"]
                )
                
                if has_required_fields:
                    self.results["combination_generation"] = "✅ SUCCESS (Phase 4 Enhanced)"
                    print("   ✅ Combination Generation: SUCCESS")
                else:
                    self.results["combination_generation"] = "⚠️ PARTIAL (Missing fields)"
                    print("   ⚠️ Combination Generation: PARTIAL")
            else:
                self.results["combination_generation"] = f"❌ FAILED ({response.status_code})"
                print(f"   ❌ Combination Generation: FAILED ({response.status_code})")
                
        except Exception as e:
            self.results["combination_generation"] = f"💥 ERROR: {str(e)}"
            print(f"   💥 Combination Generation: ERROR - {str(e)}")
        
        # Test Orchestrator Templates
        try:
            print("   Testing Orchestrator Templates...")
            response = requests.get(f"{self.services['orchestrator']}/workflows/templates", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                template_count = len(data.get("templates", []))
                self.results["orchestrator_templates"] = f"✅ SUCCESS ({template_count} templates)"
                print(f"   ✅ Orchestrator Templates: SUCCESS ({template_count} templates)")
            else:
                self.results["orchestrator_templates"] = f"❌ FAILED ({response.status_code})"
                print(f"   ❌ Orchestrator Templates: FAILED ({response.status_code})")
                
        except Exception as e:
            self.results["orchestrator_templates"] = f"💥 ERROR: {str(e)}"
            print(f"   💥 Orchestrator Templates: ERROR - {str(e)}")
    
    def test_phase8_ai_features(self):
        """Test Phase 8 AI-specific features."""
        print("\n🧠 TESTING PHASE 8 AI FEATURES")
        print("-" * 30)
        
        # Test AI Status
        try:
            print("   Testing AI Status...")
            response = requests.get(f"{self.services['orchestrator']}/ai/status", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                ai_status = data.get("status", "unknown")
                phase = data.get("phase", "unknown")
                
                if ai_status == "operational":
                    self.results["ai_status"] = "✅ OPERATIONAL (Full Phase 8)"
                    print("   ✅ AI Status: OPERATIONAL (Full Phase 8 Active)")
                elif ai_status == "not_available":
                    self.results["ai_status"] = "📋 COMPATIBILITY MODE (Phase 7)"
                    print("   📋 AI Status: COMPATIBILITY MODE (Phase 7 Fallback)")
                else:
                    self.results["ai_status"] = f"⚠️ {ai_status.upper()}"
                    print(f"   ⚠️ AI Status: {ai_status}")
            else:
                self.results["ai_status"] = f"❌ FAILED ({response.status_code})"
                print(f"   ❌ AI Status: FAILED ({response.status_code})")
                
        except Exception as e:
            self.results["ai_status"] = f"💥 ERROR: {str(e)}"
            print(f"   💥 AI Status: ERROR - {str(e)}")
        
        # Test AI Analytics
        try:
            print("   Testing AI Analytics...")
            response = requests.get(f"{self.services['orchestrator']}/ai/analytics", timeout=10)
            
            if response.status_code == 200:
                self.results["ai_analytics"] = "✅ WORKING"
                print("   ✅ AI Analytics: WORKING")
            else:
                self.results["ai_analytics"] = f"❌ FAILED ({response.status_code})"
                print(f"   ❌ AI Analytics: FAILED ({response.status_code})")
                
        except Exception as e:
            self.results["ai_analytics"] = f"💥 ERROR: {str(e)}"
            print(f"   💥 AI Analytics: ERROR - {str(e)}")
        
        # Test AI-Optimized Workflow
        try:
            print("   Testing AI-Optimized Workflow...")
            response = requests.post(
                f"{self.services['orchestrator']}/workflows/execute/ai-optimized",
                json={
                    "workflow_type": "complete_recommendation",
                    "input_data": {
                        "user_id": "ai_test_user",
                        "context": "formal"
                    },
                    "options": {"ai_optimization": True}
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_enhanced = data.get("metadata", {}).get("phase8_ai_enhanced", False)
                
                if ai_enhanced:
                    self.results["ai_workflow"] = "✅ AI-ENHANCED"
                    print("   ✅ AI-Optimized Workflow: AI-ENHANCED")
                else:
                    self.results["ai_workflow"] = "📋 STANDARD (No AI enhancement)"
                    print("   📋 AI-Optimized Workflow: STANDARD")
            else:
                self.results["ai_workflow"] = f"❌ FAILED ({response.status_code})"
                print(f"   ❌ AI-Optimized Workflow: FAILED ({response.status_code})")
                
        except Exception as e:
            self.results["ai_workflow"] = f"💥 ERROR: {str(e)}"
            print(f"   💥 AI-Optimized Workflow: ERROR - {str(e)}")
    
    def generate_report(self, test_duration):
        """Generate final test report."""
        print("\n" + "=" * 50)
        print("🏆 PHASE 8 QUICK INTEGRATION TEST RESULTS")
        print("=" * 50)
        
        # Count successes
        success_count = sum(1 for result in self.results.values() if "✅" in result)
        partial_count = sum(1 for result in self.results.values() if "📋" in result or "⚠️" in result)
        error_count = sum(1 for result in self.results.values() if "❌" in result or "💥" in result)
        total_tests = len(self.results)
        
        success_rate = (success_count / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"📊 OVERALL RESULTS:")
        print(f"   ✅ Successful: {success_count}/{total_tests}")
        print(f"   ⚠️ Partial/Warning: {partial_count}/{total_tests}")
        print(f"   ❌ Failed/Error: {error_count}/{total_tests}")
        print(f"   📈 Success Rate: {success_rate:.1f}%")
        print(f"   ⏱️ Test Duration: {test_duration:.2f}s")
        
        print(f"\n📋 DETAILED RESULTS:")
        for test_name, result in self.results.items():
            print(f"   {test_name}: {result}")
        
        # Final Assessment
        print(f"\n🎯 FINAL ASSESSMENT:")
        if success_rate >= 90:
            print("   🎉 EXCELLENT: System is ready for production!")
        elif success_rate >= 80:
            print("   ✅ GOOD: System is stable with minor issues")
        elif success_rate >= 70:
            print("   ⚠️ FAIR: System needs improvements")
        else:
            print("   ❌ POOR: System requires significant fixes")
        
        # Save report
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "test_duration_seconds": round(test_duration, 2),
            "success_rate": round(success_rate, 1),
            "total_tests": total_tests,
            "successful_tests": success_count,
            "partial_tests": partial_count,
            "failed_tests": error_count,
            "detailed_results": self.results
        }
        
        with open("PHASE8_QUICK_TEST_REPORT.json", "w") as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📄 Report saved to: PHASE8_QUICK_TEST_REPORT.json")
        
        return report_data

if __name__ == "__main__":
    tester = QuickIntegrationTester()
    tester.run_quick_test()
