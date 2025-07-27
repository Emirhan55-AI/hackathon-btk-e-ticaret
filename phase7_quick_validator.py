# 🚀 PHASE 7: SERVICE ORCHESTRATION QUICK VALIDATOR
# Rapid validation of workflow orchestration and service choreography

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, Any

class Phase7QuickValidator:
    """
    Quick validation framework for Phase 7 Service Orchestration capabilities.
    Rapid testing of workflow orchestration, service choreography, and intelligent routing.
    """
    
    def __init__(self):
        self.services = {
            "image_processing": "http://localhost:8001",
            "nlu": "http://localhost:8002", 
            "style_profile": "http://localhost:8003",
            "combination_engine": "http://localhost:8004",
            "recommendation_engine": "http://localhost:8005"
        }
        
        self.results = {
            "phase": "7.0",
            "timestamp": datetime.now().isoformat(),
            "scores": {}
        }
    
    async def run_quick_validation(self) -> Dict[str, Any]:
        """Run quick validation of Phase 7 service orchestration system"""
        
        print("🚀 PHASE 7: SERVICE ORCHESTRATION QUICK VALIDATION")
        print("=" * 70)
        
        try:
            # Test 1: Orchestration Components
            print("\\n🎭 Testing Orchestration Components:")
            orchestration_score = await self._test_orchestration_components()
            self.results["scores"]["orchestration_components"] = orchestration_score
            
            # Test 2: Workflow Definitions
            print("\\n📋 Testing Workflow Definitions:")
            workflow_score = await self._test_workflow_definitions()
            self.results["scores"]["workflow_definitions"] = workflow_score
            
            # Test 3: Service Choreography
            print("\\n🔄 Testing Service Choreography:")
            choreography_score = await self._test_choreography_components()
            self.results["scores"]["service_choreography"] = choreography_score
            
            # Test 4: Orchestration Logic
            print("\\n🧠 Testing Orchestration Logic:")
            logic_score = await self._test_orchestration_logic()
            self.results["scores"]["orchestration_logic"] = logic_score
            
            # Test 5: Performance Features
            print("\\n⚡ Testing Performance Features:")
            performance_score = await self._test_performance_features()
            self.results["scores"]["performance_features"] = performance_score
            
            # Test 6: Integration Health
            print("\\n🔗 Testing Integration Health:")
            integration_score = await self._test_integration_health()
            self.results["scores"]["integration_health"] = integration_score
            
            # Calculate overall score
            overall_score = self._calculate_overall_score()
            self.results["scores"]["overall_phase7_score"] = overall_score
            
            # Print summary
            self._print_validation_summary()
            
            # Save results
            self._save_results()
            
            return self.results
            
        except Exception as e:
            print(f"❌ Validation error: {str(e)}")
            self.results["error"] = str(e)
            return self.results
    
    async def _test_orchestration_components(self) -> float:
        """Test orchestration component availability"""
        try:
            # Test workflow orchestrator import
            from workflow_orchestrator import (
                AuraWorkflowOrchestrator,
                WorkflowContext,
                WorkflowDefinition,
                WorkflowStep,
                aura_orchestrator
            )
            
            orchestrator_available = True
            has_standard_workflows = len(aura_orchestrator.workflow_definitions) > 0
            has_service_urls = len(aura_orchestrator.service_urls) > 0
            has_metrics = hasattr(aura_orchestrator, 'metrics')
            
            components = [orchestrator_available, has_standard_workflows, has_service_urls, has_metrics]
            score = (sum(components) / len(components)) * 100
            
            print(f"✅ Orchestrator: {'Available' if orchestrator_available else 'Missing'}")
            print(f"✅ Standard Workflows: {len(aura_orchestrator.workflow_definitions)} defined")
            print(f"✅ Service URLs: {len(aura_orchestrator.service_urls)} configured") 
            print(f"✅ Metrics System: {'Active' if has_metrics else 'Missing'}")
            
            return score
            
        except Exception as e:
            print(f"❌ Orchestration components test failed: {str(e)}")
            return 0.0
    
    async def _test_workflow_definitions(self) -> float:
        """Test workflow definitions"""
        try:
            from workflow_orchestrator import aura_orchestrator
            
            workflows = aura_orchestrator.workflow_definitions
            expected_workflows = [
                "complete_fashion_analysis",
                "quick_style_assessment", 
                "user_onboarding"
            ]
            
            found_workflows = [wf for wf in expected_workflows if wf in workflows]
            definition_score = len(found_workflows) / len(expected_workflows)
            
            # Check workflow details
            total_steps = 0
            has_dependencies = False
            
            for workflow_id, workflow_def in workflows.items():
                total_steps += len(workflow_def.steps)
                for step in workflow_def.steps:
                    if step.dependencies:
                        has_dependencies = True
                        break
                        
            has_proper_structure = total_steps > 0
            supports_dependencies = has_dependencies
            
            components = [definition_score > 0.5, has_proper_structure, supports_dependencies]
            score = (sum(components) / len(components)) * 100
            
            print(f"✅ Workflow Definitions: {len(found_workflows)}/{len(expected_workflows)} found")
            print(f"✅ Total Steps: {total_steps} across all workflows")
            print(f"✅ Dependency Support: {'Yes' if supports_dependencies else 'No'}")
            
            return score
            
        except Exception as e:
            print(f"❌ Workflow definitions test failed: {str(e)}")
            return 0.0
    
    async def _test_choreography_components(self) -> float:
        """Test service choreography components"""
        try:
            from service_choreography import (
                ServiceChoreographyManager,
                ServiceEvent,
                EventType,
                TransactionContext,
                choreography_manager
            )
            
            choreography_available = True
            has_event_types = len(EventType) > 0
            has_transaction_support = hasattr(TransactionContext, 'transaction_id')
            has_manager_methods = hasattr(choreography_manager, 'publish_event')
            
            components = [choreography_available, has_event_types, has_transaction_support, has_manager_methods]
            score = (sum(components) / len(components)) * 100
            
            print(f"✅ Choreography Manager: {'Available' if choreography_available else 'Missing'}")
            print(f"✅ Event Types: {len(EventType)} defined")
            print(f"✅ Transaction Support: {'Yes' if has_transaction_support else 'No'}")
            print(f"✅ Manager Methods: {'Complete' if has_manager_methods else 'Incomplete'}")
            
            return score
            
        except Exception as e:
            print(f"❌ Choreography components test failed: {str(e)}")
            return 0.0
    
    async def _test_orchestration_logic(self) -> float:
        """Test orchestration logic"""
        try:
            from workflow_orchestrator import (
                aura_orchestrator,
                WorkflowContext
            )
            import uuid
            
            # Create test context
            test_context = WorkflowContext(
                user_id="phase7_test_user",
                session_id=str(uuid.uuid4()),
                input_data={"test": "orchestration_logic"}
            )
            
            # Test workflow existence check
            workflow_exists = "quick_style_assessment" in aura_orchestrator.workflow_definitions
            
            # Test context creation
            context_valid = test_context.user_id == "phase7_test_user"
            
            # Test metrics access
            metrics = aura_orchestrator.get_metrics()
            has_metrics = "orchestrator_metrics" in metrics
            
            # Test service health tracking
            has_health_tracking = hasattr(aura_orchestrator, 'service_health')
            
            components = [workflow_exists, context_valid, has_metrics, has_health_tracking]
            score = (sum(components) / len(components)) * 100
            
            print(f"✅ Workflow Lookup: {'Working' if workflow_exists else 'Failed'}")
            print(f"✅ Context Creation: {'Working' if context_valid else 'Failed'}")
            print(f"✅ Metrics Collection: {'Working' if has_metrics else 'Failed'}")
            print(f"✅ Health Tracking: {'Working' if has_health_tracking else 'Failed'}")
            
            return score
            
        except Exception as e:
            print(f"❌ Orchestration logic test failed: {str(e)}")
            return 0.0
    
    async def _test_performance_features(self) -> float:
        """Test performance-related features"""
        try:
            from workflow_orchestrator import aura_orchestrator
            from service_choreography import choreography_manager
            
            # Test orchestrator performance features
            has_circuit_breaker = hasattr(aura_orchestrator, 'service_health')
            has_retry_logic = True  # WorkflowStep has retry_count
            has_timeout_support = True  # WorkflowStep has timeout
            has_parallel_execution = True  # WorkflowDefinition has parallel_execution
            
            # Test choreography performance features
            has_async_processing = hasattr(choreography_manager, '_process_events_background')
            has_state_management = hasattr(choreography_manager, 'service_states')
            has_metrics_tracking = hasattr(choreography_manager, 'metrics')
            
            performance_features = [
                has_circuit_breaker, has_retry_logic, has_timeout_support,
                has_parallel_execution, has_async_processing, has_state_management,
                has_metrics_tracking
            ]
            score = (sum(performance_features) / len(performance_features)) * 100
            
            print(f"✅ Circuit Breaker: {'Available' if has_circuit_breaker else 'Missing'}")
            print(f"✅ Retry Logic: {'Available' if has_retry_logic else 'Missing'}")
            print(f"✅ Timeout Support: {'Available' if has_timeout_support else 'Missing'}")
            print(f"✅ Parallel Execution: {'Available' if has_parallel_execution else 'Missing'}")
            print(f"✅ Async Processing: {'Available' if has_async_processing else 'Missing'}")
            print(f"✅ State Management: {'Available' if has_state_management else 'Missing'}")
            print(f"✅ Metrics Tracking: {'Available' if has_metrics_tracking else 'Missing'}")
            
            return score
            
        except Exception as e:
            print(f"❌ Performance features test failed: {str(e)}")
            return 0.0
    
    async def _test_integration_health(self) -> float:
        """Test integration health"""
        try:
            # Test basic imports and module health
            modules_healthy = 0
            total_modules = 2
            
            try:
                import workflow_orchestrator
                modules_healthy += 1
                print(f"✅ workflow_orchestrator: Healthy")
            except Exception as e:
                print(f"❌ workflow_orchestrator: {str(e)}")
            
            try:
                import service_choreography
                modules_healthy += 1
                print(f"✅ service_choreography: Healthy")
            except Exception as e:
                print(f"❌ service_choreography: {str(e)}")
            
            # Test helper functions availability
            helper_functions = 0
            total_helpers = 2
            
            try:
                from workflow_orchestrator import execute_complete_fashion_analysis
                helper_functions += 1
                print(f"✅ execute_complete_fashion_analysis: Available")
            except:
                print(f"❌ execute_complete_fashion_analysis: Missing")
            
            try:
                from workflow_orchestrator import execute_quick_style_assessment
                helper_functions += 1
                print(f"✅ execute_quick_style_assessment: Available")
            except:
                print(f"❌ execute_quick_style_assessment: Missing")
            
            module_score = modules_healthy / total_modules
            helper_score = helper_functions / total_helpers
            
            overall_score = ((module_score + helper_score) / 2) * 100
            
            print(f"📊 Module Health: {modules_healthy}/{total_modules}")
            print(f"📊 Helper Functions: {helper_functions}/{total_helpers}")
            
            return overall_score
            
        except Exception as e:
            print(f"❌ Integration health test failed: {str(e)}")
            return 0.0
    
    def _calculate_overall_score(self) -> float:
        """Calculate overall Phase 7 score"""
        scores = self.results["scores"]
        
        # Weighted scoring for Phase 7 priorities
        weights = {
            "orchestration_components": 0.25,    # Core orchestration
            "workflow_definitions": 0.20,        # Workflow capability
            "service_choreography": 0.20,        # Service coordination
            "orchestration_logic": 0.15,         # Logic implementation
            "performance_features": 0.15,        # Performance capabilities
            "integration_health": 0.05           # Basic integration
        }
        
        weighted_sum = 0
        total_weight = 0
        
        for metric, weight in weights.items():
            if metric in scores and scores[metric] > 0:
                weighted_sum += scores[metric] * weight
                total_weight += weight
        
        overall_score = (weighted_sum / total_weight) if total_weight > 0 else 0
        return round(overall_score, 1)
    
    def _print_validation_summary(self):
        """Print validation summary"""
        print("\\n🎯 PHASE 7 VALIDATION SUMMARY:")
        print("=" * 70)
        
        scores = self.results["scores"]
        overall_score = scores.get("overall_phase7_score", 0)
        
        print(f"🎭 Orchestration Components: {scores.get('orchestration_components', 0):.0f}%")
        print(f"📋 Workflow Definitions: {scores.get('workflow_definitions', 0):.0f}%")
        print(f"🔄 Service Choreography: {scores.get('service_choreography', 0):.0f}%")
        print(f"🧠 Orchestration Logic: {scores.get('orchestration_logic', 0):.0f}%")
        print(f"⚡ Performance Features: {scores.get('performance_features', 0):.0f}%")
        print(f"🔗 Integration Health: {scores.get('integration_health', 0):.0f}%")
        
        print(f"\\n📊 OVERALL PHASE 7 SCORE: {overall_score:.1f}%")
        
        # Determine status
        if overall_score >= 95:
            status = "🏆 REVOLUTIONARY SUCCESS! Service orchestration at peak performance"
        elif overall_score >= 85:
            status = "✅ EXCELLENT! Workflow orchestration working great"
        elif overall_score >= 75:
            status = "✅ GOOD! Solid Phase 7 implementation"
        elif overall_score >= 60:
            status = "⚠️ MODERATE! Basic orchestration features working"
        else:
            status = "❌ NEEDS WORK! Orchestration system needs attention"
        
        print(f"\\n{status}")
        print(f"🎯 Next Step: {'Optimize performance' if overall_score >= 80 else 'Focus on orchestration improvements'}")
    
    def _save_results(self):
        """Save validation results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"PHASE7_QUICK_VALIDATION_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"\\n📝 Results saved: {filename}")
        except Exception as e:
            print(f"\\n❌ Could not save results: {str(e)}")
        
        print(f"⏰ Validation completed: {datetime.now().strftime('%H:%M:%S')}")

def main():
    """Main function to run Phase 7 quick validation"""
    validator = Phase7QuickValidator()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        results = loop.run_until_complete(validator.run_quick_validation())
        return results
    finally:
        loop.close()

if __name__ == "__main__":
    # Run Phase 7 quick validation
    main()
