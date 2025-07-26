# Phase 7: Service Orchestration Testing Suite
# Comprehensive tests for workflow orchestration, dependency management, and service coordination

import pytest
import asyncio
import json
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
import aiohttp
from typing import Dict, Any

# Import the orchestration components
from workflow_orchestrator import (
    AuraOrchestrator, 
    WorkflowStatus, 
    ServiceType, 
    WorkflowStep, 
    Workflow
)

class TestAuraOrchestrator:
    """
    Comprehensive test suite for the Aura Service Orchestration Engine.
    Tests workflow creation, execution, dependency management, and error handling.
    """
    
    @pytest.fixture
    async def orchestrator(self):
        """
        Create a test orchestrator instance with mocked HTTP session.
        Provides isolated testing environment for orchestration logic.
        """
        orchestrator = AuraOrchestrator()
        
        # Mock HTTP session for testing
        mock_session = AsyncMock()
        orchestrator.http_session = mock_session
        
        return orchestrator
    
    @pytest.fixture
    def sample_workflow_context(self):
        """
        Sample context data for workflow testing.
        Represents typical user input for style analysis workflows.
        """
        return {
            "image_url": "https://example.com/test-outfit.jpg",
            "user_description": "Looking for casual office wear recommendations",
            "occasion": "business_casual",
            "budget_range": "medium",
            "style_preferences": ["minimalist", "professional"]
        }
    
    @pytest.mark.asyncio
    async def test_orchestrator_initialization(self):
        """
        Test that orchestrator initializes correctly with all required components.
        Verifies service endpoints, templates, and internal state setup.
        """
        orchestrator = AuraOrchestrator()
        
        # Verify service endpoints are configured
        assert len(orchestrator.service_endpoints) == 5
        assert ServiceType.IMAGE_PROCESSING in orchestrator.service_endpoints
        assert ServiceType.NLU_SERVICE in orchestrator.service_endpoints
        assert ServiceType.STYLE_PROFILE in orchestrator.service_endpoints
        assert ServiceType.COMBINATION_ENGINE in orchestrator.service_endpoints
        assert ServiceType.RECOMMENDATION_ENGINE in orchestrator.service_endpoints
        
        # Verify workflow templates are available
        assert len(orchestrator.workflow_templates) == 5
        assert 'complete_style_analysis' in orchestrator.workflow_templates
        assert 'outfit_recommendation' in orchestrator.workflow_templates
        
        # Verify internal state initialization
        assert isinstance(orchestrator.active_workflows, dict)
        assert isinstance(orchestrator.completed_workflows, dict)
        assert isinstance(orchestrator.orchestration_metrics, dict)
        
        # Verify metrics are initialized correctly
        assert orchestrator.orchestration_metrics['total_workflows_executed'] == 0
        assert orchestrator.orchestration_metrics['successful_workflows'] == 0
        assert orchestrator.orchestration_metrics['failed_workflows'] == 0
    
    @pytest.mark.asyncio
    async def test_service_health_check(self, orchestrator):
        """
        Test comprehensive service health checking functionality.
        Verifies health check execution and response processing.
        """
        # Mock successful health responses for all services
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "service": "test_service",
            "status": "operational",
            "version": "1.0.0",
            "capabilities": ["test_capability"],
            "service_info": {"description": "Test service"}
        })
        
        orchestrator.http_session.get.return_value.__aenter__.return_value = mock_response
        
        # Perform health check
        health_results = await orchestrator.check_service_health()
        
        # Verify results
        assert len(health_results) == 5
        for service_type, health_data in health_results.items():
            assert 'status' in health_data
            assert 'response_time' in health_data
            assert 'capabilities' in health_data
            assert 'last_checked' in health_data
        
        # Verify internal state is updated
        assert orchestrator.service_health == health_results
        assert orchestrator.last_health_check is not None
    
    @pytest.mark.asyncio
    async def test_service_health_check_with_failures(self, orchestrator):
        """
        Test health check handling of service failures and timeouts.
        Verifies graceful handling of unhealthy services.
        """
        # Mock mixed health responses (some healthy, some failed)
        def mock_get_response(url, **kwargs):
            mock_response = AsyncMock()
            
            if "8001" in url:  # Image processing service - healthy
                mock_response.status = 200
                mock_response.json = AsyncMock(return_value={"status": "operational"})
            elif "8002" in url:  # NLU service - unhealthy
                mock_response.status = 500
                mock_response.text = AsyncMock(return_value="Internal server error")
            elif "8003" in url:  # Style profile service - timeout
                raise asyncio.TimeoutError("Service timeout")
            else:  # Other services - healthy
                mock_response.status = 200 
                mock_response.json = AsyncMock(return_value={"status": "operational"})
            
            return mock_response
        
        orchestrator.http_session.get.return_value.__aenter__ = mock_get_response
        
        # Perform health check
        health_results = await orchestrator.check_service_health()
        
        # Verify mixed results are handled correctly
        assert len(health_results) == 5
        
        # Count healthy vs unhealthy services
        healthy_count = sum(1 for health in health_results.values() if health['status'] == 'healthy')
        unhealthy_count = sum(1 for health in health_results.values() if health['status'] in ['unhealthy', 'timeout', 'error'])
        
        assert healthy_count + unhealthy_count == 5
        assert unhealthy_count > 0  # At least some services should be unhealthy
    
    def test_workflow_creation_from_template(self, orchestrator, sample_workflow_context):
        """
        Test workflow creation from templates with proper dependency setup.
        Verifies that workflows are created with correct steps and dependencies.
        """
        user_id = "test_user_123"
        template_name = "complete_style_analysis"
        
        # Create workflow from template
        workflow = orchestrator.create_workflow(template_name, user_id, sample_workflow_context)
        
        # Verify workflow properties
        assert workflow.workflow_id.startswith("workflow_")
        assert workflow.name == "Complete Style Analysis"
        assert workflow.user_id == user_id
        assert workflow.context == sample_workflow_context
        assert workflow.status == WorkflowStatus.PENDING
        assert workflow.created_at is not None
        
        # Verify workflow steps
        assert len(workflow.steps) == 5
        step_ids = [step.step_id for step in workflow.steps]
        assert "image_analysis" in step_ids
        assert "text_analysis" in step_ids
        assert "style_profiling" in step_ids
        assert "outfit_combinations" in step_ids
        assert "recommendations" in step_ids
        
        # Verify dependencies are set correctly
        style_profiling_step = next(s for s in workflow.steps if s.step_id == "style_profiling")
        assert "image_analysis" in style_profiling_step.depends_on
        assert "text_analysis" in style_profiling_step.depends_on
        
        # Verify workflow is stored in active workflows
        assert workflow.workflow_id in orchestrator.active_workflows
    
    def test_invalid_workflow_template(self, orchestrator, sample_workflow_context):
        """
        Test handling of invalid workflow template names.
        Verifies proper error handling for unknown templates.
        """
        user_id = "test_user_123"
        invalid_template = "nonexistent_template"
        
        # Attempt to create workflow with invalid template
        with pytest.raises(ValueError, match="Unknown workflow template"):
            orchestrator.create_workflow(invalid_template, user_id, sample_workflow_context)
    
    def test_dependency_graph_building(self, orchestrator):
        """
        Test dependency graph building for workflow steps.
        Verifies correct graph construction and cycle detection.
        """
        # Create test workflow steps with dependencies
        steps = [
            WorkflowStep(
                step_id="step_a",
                service_type=ServiceType.IMAGE_PROCESSING,
                endpoint="/test"
            ),
            WorkflowStep(
                step_id="step_b",
                service_type=ServiceType.NLU_SERVICE,
                endpoint="/test"
            ),
            WorkflowStep(
                step_id="step_c",
                service_type=ServiceType.STYLE_PROFILE,
                endpoint="/test",
                depends_on=["step_a", "step_b"]
            ),
            WorkflowStep(
                step_id="step_d",
                service_type=ServiceType.COMBINATION_ENGINE,
                endpoint="/test",
                depends_on=["step_c"]
            )
        ]
        
        # Build dependency graph
        graph = orchestrator._build_dependency_graph(steps)
        
        # Verify graph structure
        assert len(graph.nodes) == 4
        assert len(graph.edges) == 3
        
        # Verify specific dependencies
        assert graph.has_edge("step_a", "step_c")
        assert graph.has_edge("step_b", "step_c")
        assert graph.has_edge("step_c", "step_d")
        
        # Verify graph is acyclic
        import networkx as nx
        assert nx.is_directed_acyclic_graph(graph)
    
    def test_circular_dependency_detection(self, orchestrator):
        """
        Test detection of circular dependencies in workflow steps.
        Verifies that circular dependencies are properly caught and reported.
        """
        # Create steps with circular dependency
        steps = [
            WorkflowStep(
                step_id="step_a",
                service_type=ServiceType.IMAGE_PROCESSING,
                endpoint="/test",
                depends_on=["step_b"]  # Circular dependency
            ),
            WorkflowStep(
                step_id="step_b",
                service_type=ServiceType.NLU_SERVICE,
                endpoint="/test",
                depends_on=["step_a"]  # Circular dependency
            )
        ]
        
        # Attempt to build dependency graph
        with pytest.raises(ValueError, match="Circular dependencies detected"):
            orchestrator._build_dependency_graph(steps)
    
    @pytest.mark.asyncio
    async def test_single_step_execution_success(self, orchestrator):
        """
        Test successful execution of a single workflow step.
        Verifies service calls and result processing.
        """
        # Create test step
        step = WorkflowStep(
            step_id="test_step",
            service_type=ServiceType.IMAGE_PROCESSING,
            endpoint="/analyze",
            payload={"image_url": "test.jpg"}
        )
        
        # Mock successful service response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "status": "success",
            "analysis_results": {"detected_items": ["shirt", "pants"]},
            "processing_time": 0.5
        })
        
        orchestrator.http_session.post.return_value.__aenter__.return_value = mock_response
        
        # Execute step
        result = await orchestrator._execute_single_step(step, {})
        
        # Verify step completion
        assert step.status == WorkflowStatus.COMPLETED
        assert step.result is not None
        assert step.execution_time is not None
        assert step.start_time is not None
        assert step.end_time is not None
        
        # Verify result content
        assert result["status"] == "success"
        assert "analysis_results" in result
    
    @pytest.mark.asyncio
    async def test_single_step_execution_with_retry(self, orchestrator):
        """
        Test step execution with retry logic on failures.
        Verifies retry behavior and eventual success.
        """
        # Create test step with retry configuration
        step = WorkflowStep(
            step_id="test_step",
            service_type=ServiceType.IMAGE_PROCESSING,
            endpoint="/analyze",
            payload={"image_url": "test.jpg"},
            retry_count=2
        )
        
        # Mock first two calls fail, third succeeds
        call_count = 0
        async def mock_post_response(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            
            mock_response = AsyncMock()
            if call_count <= 2:
                # First two calls fail
                mock_response.status = 500
                mock_response.text = AsyncMock(return_value="Temporary error")
                return mock_response
            else:
                # Third call succeeds
                mock_response.status = 200
                mock_response.json = AsyncMock(return_value={"status": "success"})
                return mock_response
        
        orchestrator.http_session.post.return_value.__aenter__ = mock_post_response
        
        # Execute step (should succeed after retries)
        result = await orchestrator._execute_single_step(step, {})
        
        # Verify eventual success
        assert step.status == WorkflowStatus.COMPLETED
        assert call_count == 3  # Two failures, one success
        assert result["status"] == "success"
    
    @pytest.mark.asyncio
    async def test_single_step_execution_failure(self, orchestrator):
        """
        Test step execution failure after all retries exhausted.
        Verifies proper error handling and status updates.
        """
        # Create test step with limited retries
        step = WorkflowStep(
            step_id="test_step",
            service_type=ServiceType.IMAGE_PROCESSING,
            endpoint="/analyze",
            payload={"image_url": "test.jpg"},
            retry_count=1
        )
        
        # Mock all calls fail
        mock_response = AsyncMock()
        mock_response.status = 500
        mock_response.text = AsyncMock(return_value="Persistent error")
        
        orchestrator.http_session.post.return_value.__aenter__.return_value = mock_response
        
        # Execute step (should fail after retries)
        with pytest.raises(Exception, match="HTTP 500"):
            await orchestrator._execute_single_step(step, {})
        
        # Verify failure status
        assert step.status == WorkflowStatus.FAILED
        assert step.error is not None
        assert "HTTP 500" in step.error
    
    @pytest.mark.asyncio
    async def test_workflow_execution_success(self, orchestrator, sample_workflow_context):
        """
        Test complete workflow execution with multiple steps.
        Verifies end-to-end workflow orchestration and result aggregation.
        """
        # Create test workflow
        user_id = "test_user_123"
        workflow = orchestrator.create_workflow("outfit_recommendation", user_id, sample_workflow_context)
        
        # Mock all service calls to succeed
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "status": "success",
            "results": {"recommendation": "test_recommendation"}
        })
        
        orchestrator.http_session.get.return_value.__aenter__.return_value = mock_response
        orchestrator.http_session.post.return_value.__aenter__.return_value = mock_response
        
        # Execute workflow
        execution_results = await orchestrator.execute_workflow(workflow)
        
        # Verify workflow completion
        assert execution_results["status"] == "completed"
        assert execution_results["workflow_id"] == workflow.workflow_id
        assert execution_results["steps_executed"] > 0
        assert execution_results["steps_failed"] == 0
        assert execution_results["execution_time"] is not None
        
        # Verify workflow moved to completed
        assert workflow.workflow_id not in orchestrator.active_workflows
        assert workflow.workflow_id in orchestrator.completed_workflows
        
        # Verify metrics updated
        assert orchestrator.orchestration_metrics['total_workflows_executed'] == 1
        assert orchestrator.orchestration_metrics['successful_workflows'] == 1
        assert orchestrator.orchestration_metrics['failed_workflows'] == 0
    
    @pytest.mark.asyncio
    async def test_workflow_execution_with_step_failure(self, orchestrator, sample_workflow_context):
        """
        Test workflow execution handling of step failures.
        Verifies partial execution and error reporting.
        """
        # Create test workflow
        user_id = "test_user_123"
        workflow = orchestrator.create_workflow("complete_style_analysis", user_id, sample_workflow_context)
        
        # Mock some calls succeed, some fail
        call_count = 0
        async def mock_service_call(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            
            mock_response = AsyncMock()
            if call_count <= 2:
                # First two calls succeed
                mock_response.status = 200
                mock_response.json = AsyncMock(return_value={"status": "success"})
            else:
                # Later calls fail
                mock_response.status = 500
                mock_response.text = AsyncMock(return_value="Service error")
            
            return mock_response
        
        orchestrator.http_session.get.return_value.__aenter__ = mock_service_call
        orchestrator.http_session.post.return_value.__aenter__ = mock_service_call
        
        # Execute workflow (should fail due to step failures)
        execution_results = await orchestrator.execute_workflow(workflow)
        
        # Verify workflow failure handling
        assert execution_results["status"] == "failed"
        assert "error" in execution_results
        assert "partial_results" in execution_results
        
        # Verify metrics updated for failure
        assert orchestrator.orchestration_metrics['failed_workflows'] == 1
    
    def test_orchestration_analytics_generation(self, orchestrator):
        """
        Test generation of comprehensive orchestration analytics.
        Verifies analytics data structure and content.
        """
        # Simulate some workflow history
        orchestrator.orchestration_metrics.update({
            'total_workflows_executed': 10,
            'successful_workflows': 8,
            'failed_workflows': 2,
            'average_execution_time': 15.5,
            'service_call_count': {
                'image_processing': 25,
                'nlu_service': 20,
                'style_profile': 15
            }
        })
        
        # Generate analytics
        analytics = orchestrator.get_orchestration_analytics()
        
        # Verify analytics structure
        assert 'performance_metrics' in analytics
        assert 'service_health' in analytics
        assert 'active_workflows' in analytics
        assert 'completed_workflows' in analytics
        assert 'workflow_templates' in analytics
        assert 'system_status' in analytics
        
        # Verify performance metrics
        perf_metrics = analytics['performance_metrics']
        assert perf_metrics['total_workflows_executed'] == 10
        assert perf_metrics['successful_workflows'] == 8
        assert perf_metrics['failed_workflows'] == 2
        assert perf_metrics['average_execution_time'] == 15.5
    
    def test_workflow_template_availability(self, orchestrator):
        """
        Test that all expected workflow templates are available and functional.
        Verifies template registration and accessibility.
        """
        expected_templates = [
            'complete_style_analysis',
            'outfit_recommendation', 
            'style_evolution_analysis',
            'personalized_shopping',
            'trend_analysis'
        ]
        
        # Verify all templates are registered
        available_templates = list(orchestrator.workflow_templates.keys())
        for template in expected_templates:
            assert template in available_templates
        
        # Test each template can create a workflow
        user_id = "test_user"
        context = {"test": "context"}
        
        for template_name in expected_templates:
            workflow = orchestrator.create_workflow(template_name, user_id, context)
            assert workflow is not None
            assert workflow.name is not None
            assert len(workflow.steps) > 0
            
            # Clean up
            if workflow.workflow_id in orchestrator.active_workflows:
                del orchestrator.active_workflows[workflow.workflow_id]

@pytest.mark.asyncio
class TestWorkflowTemplates:
    """
    Specialized tests for individual workflow templates.
    Verifies template-specific logic and step configurations.
    """
    
    @pytest.fixture
    async def orchestrator(self):
        """Create orchestrator for template testing."""
        return AuraOrchestrator()
    
    def test_complete_style_analysis_template(self, orchestrator):
        """
        Test the complete style analysis workflow template.
        Verifies comprehensive analysis workflow structure.
        """
        context = {
            "image_url": "test.jpg",
            "user_description": "Test description",
            "occasion": "business_casual"
        }
        
        workflow = orchestrator.create_workflow("complete_style_analysis", "user123", context)
        
        # Verify workflow structure
        assert workflow.name == "Complete Style Analysis"
        assert len(workflow.steps) == 5
        
        # Verify step sequence and dependencies
        step_ids = [step.step_id for step in workflow.steps]
        assert "image_analysis" in step_ids
        assert "text_analysis" in step_ids
        assert "style_profiling" in step_ids
        assert "outfit_combinations" in step_ids
        assert "recommendations" in step_ids
        
        # Verify dependencies
        style_step = next(s for s in workflow.steps if s.step_id == "style_profiling")
        assert "image_analysis" in style_step.depends_on
        assert "text_analysis" in style_step.depends_on
    
    def test_outfit_recommendation_template(self, orchestrator):
        """
        Test the outfit recommendation workflow template.
        Verifies focused recommendation workflow structure.
        """
        context = {
            "num_outfits": 5,
            "occasion": "casual"
        }
        
        workflow = orchestrator.create_workflow("outfit_recommendation", "user123", context)
        
        # Verify workflow structure
        assert workflow.name == "Outfit Recommendation"
        assert len(workflow.steps) == 3
        
        # Verify step configuration
        step_ids = [step.step_id for step in workflow.steps]
        assert "style_profile_check" in step_ids
        assert "generate_combinations" in step_ids
        assert "get_recommendations" in step_ids
    
    def test_personalized_shopping_template(self, orchestrator):
        """
        Test the personalized shopping workflow template.
        Verifies shopping-focused workflow structure.
        """
        context = {"budget": "medium"}
        
        workflow = orchestrator.create_workflow("personalized_shopping", "user123", context)
        
        # Verify workflow structure
        assert workflow.name == "Personalized Shopping"
        assert len(workflow.steps) == 3
        
        # Verify shopping-specific steps
        step_ids = [step.step_id for step in workflow.steps]
        assert "user_preferences" in step_ids
        assert "wardrobe_analysis" in step_ids
        assert "shopping_recommendations" in step_ids

if __name__ == "__main__":
    print("🧪 Running Phase 7 Orchestration Service Tests")
    print("   Testing workflow orchestration, dependency management, and service coordination")
    print("   Comprehensive test coverage for multi-service AI workflows")
    
    # Run tests with verbose output
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--color=yes",
        "-x"  # Stop on first failure for debugging
    ])
