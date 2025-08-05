# Phase 7: Service Orchestration and Workflow Engine
# This service orchestrates complex workflows across all Aura AI services
# Coordinates multi-step processes involving image analysis, style profiling, combination generation, and recommendations

import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
import aiohttp
import json
from datetime import datetime, timedelta
import uuid
from enum import Enum
from dataclasses import dataclass, asdict
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import networkx as nx
from collections import deque
import warnings
warnings.filterwarnings("ignore")

# Configure comprehensive logging for workflow orchestration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowStatus(Enum):
    """
    Enumeration for workflow execution status.
    Tracks the current state of orchestrated workflows.
    """
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"

class ServiceType(Enum):
    """
    Enumeration for different service types in the Aura ecosystem.
    Each service has specific capabilities and integration patterns.
    """
    IMAGE_PROCESSING = "image_processing"
    NLU_SERVICE = "nlu_service"
    STYLE_PROFILE = "style_profile"
    COMBINATION_ENGINE = "combination_engine"
    RECOMMENDATION_ENGINE = "recommendation_engine"
    FEEDBACK_LOOP = "feedback_loop"

@dataclass
class WorkflowStep:
    """
    Data class representing a single step in an orchestrated workflow.
    Contains all information needed to execute and track workflow steps.
    """
    step_id: str
    service_type: ServiceType
    endpoint: str
    method: str = "POST"
    payload: Optional[Dict[str, Any]] = None
    depends_on: List[str] = None
    timeout: int = 30
    retry_count: int = 3
    status: WorkflowStatus = WorkflowStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    execution_time: Optional[float] = None

@dataclass
class Workflow:
    """
    Data class representing a complete orchestrated workflow.
    Manages multiple steps with dependencies and execution coordination.
    """
    workflow_id: str
    name: str
    description: str
    steps: List[WorkflowStep]
    status: WorkflowStatus = WorkflowStatus.PENDING
    created_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    total_execution_time: Optional[float] = None
    user_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class AuraOrchestrator:
    """
    Advanced orchestration engine for coordinating complex AI workflows across all Aura services.
    
    This orchestrator manages:
    - Multi-service workflow execution with dependency management
    - Asynchronous task coordination and parallel processing
    - Error handling, retries, and graceful degradation
    - Performance monitoring and analytics
    - Dynamic workflow adaptation based on service availability
    """
    
    def __init__(self):
        """
        Initialize the Aura Orchestration Engine with comprehensive service management.
        Sets up service connections, workflow templates, and execution infrastructure.
        """
        logger.info("Initializing Aura Service Orchestration Engine - Phase 7")
        
        # Service endpoint configuration for Docker Compose environment
        # Uses container hostnames for internal service communication
        self.service_endpoints = {
            ServiceType.IMAGE_PROCESSING: "http://image-processing:8001",
            ServiceType.NLU_SERVICE: "http://nlu-service:8002",
            ServiceType.STYLE_PROFILE: "http://style-profile:8003",
            ServiceType.COMBINATION_ENGINE: "http://combination-engine:8004",
            ServiceType.RECOMMENDATION_ENGINE: "http://recommendation-engine:8005",
            ServiceType.FEEDBACK_LOOP: "http://feedback-loop:8007"
        }
        
        # E-commerce backend integration
        self.ecommerce_backend_url = "http://backend:8000"
        self.feedback_service_url = "http://feedback-loop:8007"
        
        # Active workflows tracking
        self.active_workflows: Dict[str, Workflow] = {}
        self.completed_workflows: Dict[str, Workflow] = {}
        self.workflow_history: List[Dict[str, Any]] = []
        
        # Service health monitoring
        self.service_health: Dict[ServiceType, Dict[str, Any]] = {}
        self.last_health_check: Optional[datetime] = None
        
        # Performance metrics
        self.orchestration_metrics = {
            'total_workflows_executed': 0,
            'successful_workflows': 0,
            'failed_workflows': 0,
            'average_execution_time': 0.0,
            'service_call_count': {},
            'error_patterns': {}
        }
        
        # Workflow templates for common use cases
        self.workflow_templates = {
            'complete_style_analysis': self._create_complete_style_analysis_template,
            'outfit_recommendation': self._create_outfit_recommendation_template,
            'style_evolution_analysis': self._create_style_evolution_template,
            'personalized_shopping': self._create_personalized_shopping_template,
            'trend_analysis': self._create_trend_analysis_template
        }
        
        # Asynchronous HTTP session for service communication
        self.http_session: Optional[aiohttp.ClientSession] = None
        
        # Thread pool for CPU-intensive orchestration tasks
        self.executor = ThreadPoolExecutor(max_workers=10)
        
        # Workflow dependency graph for complex orchestration
        self.dependency_graph = nx.DiGraph()
        
        logger.info("✅ Aura Orchestration Engine initialized successfully")
        logger.info(f"   Service Endpoints: {len(self.service_endpoints)} configured")
        logger.info(f"   Workflow Templates: {len(self.workflow_templates)} available")
        logger.info("   Ready for multi-service workflow orchestration")
    
    async def __aenter__(self):
        """
        Async context manager entry - initialize HTTP session.
        Enables efficient connection pooling for service communications.
        """
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=20)
        timeout = aiohttp.ClientTimeout(total=60, connect=10)
        self.http_session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={'Content-Type': 'application/json'}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Async context manager exit - cleanup HTTP session.
        Ensures proper resource cleanup and connection closing.
        """
        if self.http_session:
            await self.http_session.close()
    
    async def check_service_health(self) -> Dict[ServiceType, Dict[str, Any]]:
        """
        Comprehensive health check for all Aura services.
        Monitors service availability, response times, and capabilities.
        
        Returns:
            Dictionary containing health status for each service
        """
        logger.info("Performing comprehensive service health check")
        
        health_results = {}
        start_time = time.time()
        
        # Check each service concurrently
        health_tasks = []
        for service_type, endpoint in self.service_endpoints.items():
            task = self._check_single_service_health(service_type, endpoint)
            health_tasks.append(task)
        
        # Wait for all health checks to complete
        health_responses = await asyncio.gather(*health_tasks, return_exceptions=True)
        
        # Process health check results
        for i, (service_type, result) in enumerate(zip(self.service_endpoints.keys(), health_responses)):
            if isinstance(result, Exception):
                health_results[service_type] = {
                    'status': 'unhealthy',
                    'error': str(result),
                    'response_time': None,
                    'capabilities': []
                }
            else:
                health_results[service_type] = result
        
        # Update internal health tracking
        self.service_health = health_results
        self.last_health_check = datetime.now()
        
        # Calculate overall health metrics
        healthy_services = sum(1 for health in health_results.values() if health['status'] == 'healthy')
        total_services = len(health_results)
        overall_health = healthy_services / total_services
        
        total_time = time.time() - start_time
        
        logger.info(f"✅ Service health check completed in {total_time:.3f}s")
        logger.info(f"   Healthy services: {healthy_services}/{total_services} ({overall_health:.1%})")
        
        return health_results
    
    async def _check_single_service_health(self, service_type: ServiceType, endpoint: str) -> Dict[str, Any]:
        """
        Check health of a single service with detailed metrics.
        
        Args:
            service_type: Type of service to check
            endpoint: Service endpoint URL
            
        Returns:
            Dictionary with service health information
        """
        start_time = time.time()
        
        try:
            async with self.http_session.get(f"{endpoint}/", timeout=aiohttp.ClientTimeout(total=10)) as response:
                response_time = time.time() - start_time
                
                if response.status == 200:
                    health_data = await response.json()
                    
                    return {
                        'status': 'healthy',
                        'response_time': response_time,
                        'version': health_data.get('version', 'unknown'),
                        'capabilities': health_data.get('capabilities', []),
                        'service_info': health_data.get('service_info', {}),
                        'last_checked': datetime.now().isoformat()
                    }
                else:
                    return {
                        'status': 'unhealthy',
                        'response_time': response_time,
                        'error': f'HTTP {response.status}',
                        'capabilities': [],
                        'last_checked': datetime.now().isoformat()
                    }
        
        except asyncio.TimeoutError:
            return {
                'status': 'timeout',
                'response_time': time.time() - start_time,
                'error': 'Service timeout',
                'capabilities': [],
                'last_checked': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'status': 'error',
                'response_time': time.time() - start_time,
                'error': str(e),
                'capabilities': [],
                'last_checked': datetime.now().isoformat()
            }
    
    def create_workflow(self, template_name: str, user_id: str, context: Dict[str, Any]) -> Workflow:
        """
        Create a new workflow from a template with user-specific context.
        
        Args:
            template_name: Name of the workflow template to use
            user_id: User identifier for personalization
            context: Additional context for workflow execution
            
        Returns:
            Configured workflow ready for execution
        """
        logger.info(f"Creating workflow '{template_name}' for user {user_id}")
        
        if template_name not in self.workflow_templates:
            raise ValueError(f"Unknown workflow template: {template_name}")
        
        # Generate unique workflow ID
        workflow_id = f"workflow_{uuid.uuid4().hex[:8]}_{int(time.time())}"
        
        # Create workflow from template
        template_func = self.workflow_templates[template_name]
        workflow = template_func(workflow_id, user_id, context)
        
        # Store workflow
        self.active_workflows[workflow_id] = workflow
        
        logger.info(f"✅ Workflow created: {workflow_id} with {len(workflow.steps)} steps")
        return workflow
    
    async def execute_workflow(self, workflow: Workflow) -> Dict[str, Any]:
        """
        Execute a complete workflow with dependency management and error handling.
        
        Args:
            workflow: Workflow to execute
            
        Returns:
            Dictionary containing execution results and analytics
        """
        logger.info(f"Executing workflow: {workflow.workflow_id} ({workflow.name})")
        
        # Update workflow status
        workflow.status = WorkflowStatus.RUNNING
        workflow.started_at = datetime.now()
        
        try:
            # Build dependency graph for the workflow
            dependency_graph = self._build_dependency_graph(workflow.steps)
            
            # Execute steps in dependency order
            execution_results = await self._execute_workflow_steps(workflow, dependency_graph)
            
            # Update workflow completion status
            workflow.status = WorkflowStatus.COMPLETED
            workflow.completed_at = datetime.now()
            workflow.total_execution_time = (workflow.completed_at - workflow.started_at).total_seconds()
            
            # Move to completed workflows
            self.completed_workflows[workflow.workflow_id] = workflow
            if workflow.workflow_id in self.active_workflows:
                del self.active_workflows[workflow.workflow_id]
            
            # Update metrics
            self._update_orchestration_metrics(workflow, True)
            
            # Generate comprehensive results
            results = {
                'workflow_id': workflow.workflow_id,
                'status': workflow.status.value,
                'execution_time': workflow.total_execution_time,
                'steps_executed': len([step for step in workflow.steps if step.status == WorkflowStatus.COMPLETED]),
                'steps_failed': len([step for step in workflow.steps if step.status == WorkflowStatus.FAILED]),
                'results': execution_results,
                'analytics': self._generate_workflow_analytics(workflow)
            }
            
            logger.info(f"✅ Workflow completed: {workflow.workflow_id} in {workflow.total_execution_time:.3f}s")
            return results
            
        except Exception as e:
            # Handle workflow failure
            workflow.status = WorkflowStatus.FAILED
            workflow.completed_at = datetime.now()
            workflow.total_execution_time = (workflow.completed_at - workflow.started_at).total_seconds()
            
            self._update_orchestration_metrics(workflow, False)
            
            logger.error(f"❌ Workflow failed: {workflow.workflow_id} - {str(e)}")
            
            return {
                'workflow_id': workflow.workflow_id,
                'status': workflow.status.value,
                'error': str(e),
                'execution_time': workflow.total_execution_time,
                'partial_results': self._collect_partial_results(workflow)
            }
    
    def _build_dependency_graph(self, steps: List[WorkflowStep]) -> nx.DiGraph:
        """
        Build a dependency graph for workflow steps to determine execution order.
        
        Args:
            steps: List of workflow steps with dependencies
            
        Returns:
            NetworkX directed graph representing step dependencies
        """
        graph = nx.DiGraph()
        
        # Add all steps as nodes
        for step in steps:
            graph.add_node(step.step_id, step=step)
        
        # Add dependency edges
        for step in steps:
            if step.depends_on:
                for dependency in step.depends_on:
                    if dependency in [s.step_id for s in steps]:
                        graph.add_edge(dependency, step.step_id)
        
        # Verify no circular dependencies
        if not nx.is_directed_acyclic_graph(graph):
            raise ValueError("Circular dependencies detected in workflow")
        
        return graph
    
    async def _execute_workflow_steps(self, workflow: Workflow, dependency_graph: nx.DiGraph) -> Dict[str, Any]:
        """
        Execute workflow steps in dependency order with parallel processing where possible.
        
        Args:
            workflow: Workflow being executed
            dependency_graph: Dependency graph for step ordering
            
        Returns:
            Dictionary containing results from all executed steps
        """
        # Get topological order for step execution
        execution_order = list(nx.topological_sort(dependency_graph))
        
        # Track step results for dependency injection
        step_results = {}
        
        # Execute steps in batches (parallel where no dependencies)
        remaining_steps = set(execution_order)
        
        while remaining_steps:
            # Find steps that can be executed now (all dependencies completed)
            ready_steps = []
            for step_id in remaining_steps:
                step_node = dependency_graph.nodes[step_id]
                step = step_node['step']
                
                # Check if all dependencies are completed
                dependencies_met = True
                if step.depends_on:
                    for dep in step.depends_on:
                        if dep not in step_results:
                            dependencies_met = False
                            break
                
                if dependencies_met:
                    ready_steps.append(step)
            
            if not ready_steps:
                # No steps can be executed - check for errors
                failed_steps = [s for s in workflow.steps if s.status == WorkflowStatus.FAILED]
                if failed_steps:
                    raise Exception(f"Workflow blocked by failed steps: {[s.step_id for s in failed_steps]}")
                else:
                    raise Exception("Workflow execution deadlock - no steps can proceed")
            
            # Execute ready steps in parallel
            if len(ready_steps) == 1:
                # Single step execution
                step = ready_steps[0]
                result = await self._execute_single_step(step, step_results)
                step_results[step.step_id] = result
                remaining_steps.remove(step.step_id)
            else:
                # Parallel step execution
                step_tasks = []
                for step in ready_steps:
                    task = self._execute_single_step(step, step_results)
                    step_tasks.append((step.step_id, task))
                
                # Wait for all parallel steps to complete
                completed_results = await asyncio.gather(*[task for _, task in step_tasks], return_exceptions=True)
                
                # Process results
                for (step_id, _), result in zip(step_tasks, completed_results):
                    if isinstance(result, Exception):
                        # Find the step and mark as failed
                        for step in ready_steps:
                            if step.step_id == step_id:
                                step.status = WorkflowStatus.FAILED
                                step.error = str(result)
                                break
                        logger.error(f"Step {step_id} failed: {result}")
                    else:
                        step_results[step_id] = result
                    
                    remaining_steps.remove(step_id)
        
        return step_results
    
    async def _execute_single_step(self, step: WorkflowStep, previous_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a single workflow step with retry logic and error handling.
        
        Args:
            step: Workflow step to execute
            previous_results: Results from previously executed steps
            
        Returns:
            Dictionary containing step execution results
        """
        logger.info(f"Executing step: {step.step_id} ({step.service_type.value})")
        
        step.status = WorkflowStatus.RUNNING
        step.start_time = datetime.now()
        
        # Prepare payload with dependency injection
        payload = step.payload.copy() if step.payload else {}
        
        # Inject results from dependencies
        if step.depends_on and previous_results:
            payload['dependency_results'] = {
                dep_id: previous_results.get(dep_id) for dep_id in step.depends_on
            }
        
        # Execute with retry logic
        last_error = None
        for attempt in range(step.retry_count + 1):
            try:
                if attempt > 0:
                    logger.info(f"Retrying step {step.step_id}, attempt {attempt + 1}")
                    await asyncio.sleep(min(2 ** attempt, 10))  # Exponential backoff
                
                # Make service call
                result = await self._make_service_call(step, payload)
                
                # Step completed successfully
                step.status = WorkflowStatus.COMPLETED
                step.end_time = datetime.now()
                step.execution_time = (step.end_time - step.start_time).total_seconds()
                step.result = result
                
                logger.info(f"✅ Step completed: {step.step_id} in {step.execution_time:.3f}s")
                return result
                
            except Exception as e:
                last_error = e
                logger.warning(f"Step {step.step_id} attempt {attempt + 1} failed: {e}")
                
                if attempt == step.retry_count:
                    # All retries exhausted
                    step.status = WorkflowStatus.FAILED
                    step.end_time = datetime.now()
                    step.execution_time = (step.end_time - step.start_time).total_seconds()
                    step.error = str(last_error)
                    
                    logger.error(f"❌ Step failed after {step.retry_count + 1} attempts: {step.step_id}")
                    raise last_error
    
    async def _make_service_call(self, step: WorkflowStep, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make an HTTP call to a service endpoint.
        
        Args:
            step: Workflow step containing service information
            payload: Request payload
            
        Returns:
            Dictionary containing service response
        """
        service_endpoint = self.service_endpoints[step.service_type]
        url = f"{service_endpoint}{step.endpoint}"
        
        # Update service call metrics
        service_name = step.service_type.value
        if service_name not in self.orchestration_metrics['service_call_count']:
            self.orchestration_metrics['service_call_count'][service_name] = 0
        self.orchestration_metrics['service_call_count'][service_name] += 1
        
        try:
            if step.method.upper() == "GET":
                async with self.http_session.get(url, params=payload) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        raise Exception(f"HTTP {response.status}: {error_text}")
            
            elif step.method.upper() == "POST":
                async with self.http_session.post(url, json=payload) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        raise Exception(f"HTTP {response.status}: {error_text}")
            
            else:
                raise Exception(f"Unsupported HTTP method: {step.method}")
                
        except aiohttp.ClientError as e:
            raise Exception(f"Service communication error: {e}")
    
    # Workflow template methods
    def _create_complete_style_analysis_template(self, workflow_id: str, user_id: str, context: Dict[str, Any]) -> Workflow:
        """
        Create a complete style analysis workflow template.
        Includes image processing, NLU analysis, style profiling, and recommendations.
        """
        steps = [
            WorkflowStep(
                step_id="image_analysis",
                service_type=ServiceType.IMAGE_PROCESSING,
                endpoint="/analyze",
                payload={
                    "image_data": context.get("image_url"),
                    "analysis_type": "comprehensive",
                    "user_id": user_id
                }
            ),
            WorkflowStep(
                step_id="text_analysis", 
                service_type=ServiceType.NLU_SERVICE,
                endpoint="/analyze",
                payload={
                    "text": context.get("user_description", ""),
                    "user_id": user_id,
                    "context": "style_analysis"
                }
            ),
            WorkflowStep(
                step_id="style_profiling",
                service_type=ServiceType.STYLE_PROFILE,
                endpoint="/analyze",
                depends_on=["image_analysis", "text_analysis"],
                payload={
                    "user_id": user_id,
                    "analysis_type": "comprehensive"
                }
            ),
            WorkflowStep(
                step_id="outfit_combinations",
                service_type=ServiceType.COMBINATION_ENGINE,
                endpoint="/generate",
                depends_on=["style_profiling"],
                payload={
                    "user_id": user_id,
                    "num_combinations": 5,
                    "context": context.get("occasion", "casual")
                }
            ),
            WorkflowStep(
                step_id="recommendations",
                service_type=ServiceType.RECOMMENDATION_ENGINE,
                endpoint="/recommendations",
                depends_on=["style_profiling", "outfit_combinations"],
                payload={
                    "user_id": user_id,
                    "context": context.get("occasion", "casual"),
                    "num_recommendations": 10,
                    "strategy": "hybrid"
                }
            )
        ]
        
        return Workflow(
            workflow_id=workflow_id,
            name="Complete Style Analysis",
            description="Comprehensive style analysis including image processing, NLU, profiling, combinations, and recommendations",
            steps=steps,
            created_at=datetime.now(),
            user_id=user_id,
            context=context
        )
    
    def _create_outfit_recommendation_template(self, workflow_id: str, user_id: str, context: Dict[str, Any]) -> Workflow:
        """Create outfit recommendation workflow template."""
        steps = [
            WorkflowStep(
                step_id="style_profile_check",
                service_type=ServiceType.STYLE_PROFILE,
                endpoint=f"/profile/{user_id}",
                method="GET"
            ),
            WorkflowStep(
                step_id="generate_combinations",
                service_type=ServiceType.COMBINATION_ENGINE,
                endpoint="/generate",
                depends_on=["style_profile_check"],
                payload={
                    "user_id": user_id,
                    "num_combinations": context.get("num_outfits", 3),
                    "context": context.get("occasion", "casual")
                }
            ),
            WorkflowStep(
                step_id="get_recommendations",
                service_type=ServiceType.RECOMMENDATION_ENGINE,
                endpoint="/recommendations",
                depends_on=["style_profile_check"],
                payload={
                    "user_id": user_id,
                    "context": context.get("occasion", "casual"),
                    "num_recommendations": 8,
                    "strategy": "style_aware"
                }
            )
        ]
        
        return Workflow(
            workflow_id=workflow_id,
            name="Outfit Recommendation",
            description="Generate outfit recommendations based on user style profile",
            steps=steps,
            created_at=datetime.now(),
            user_id=user_id,
            context=context
        )
    
    def _create_style_evolution_template(self, workflow_id: str, user_id: str, context: Dict[str, Any]) -> Workflow:
        """Create style evolution analysis workflow template."""
        steps = [
            WorkflowStep(
                step_id="historical_analysis",
                service_type=ServiceType.STYLE_PROFILE,
                endpoint="/evolution",
                method="GET",
                payload={"user_id": user_id, "time_range": context.get("time_range", "6_months")}
            ),
            WorkflowStep(
                step_id="trend_predictions",
                service_type=ServiceType.RECOMMENDATION_ENGINE,
                endpoint="/trending",
                method="GET",
                depends_on=["historical_analysis"]
            )
        ]
        
        return Workflow(
            workflow_id=workflow_id,
            name="Style Evolution Analysis",
            description="Analyze user's style evolution and predict future trends",
            steps=steps,
            created_at=datetime.now(),
            user_id=user_id,
            context=context
        )
    
    def _create_personalized_shopping_template(self, workflow_id: str, user_id: str, context: Dict[str, Any]) -> Workflow:
        """Create personalized shopping workflow template."""
        steps = [
            WorkflowStep(
                step_id="user_preferences",
                service_type=ServiceType.STYLE_PROFILE,
                endpoint=f"/profile/{user_id}",
                method="GET"
            ),
            WorkflowStep(
                step_id="wardrobe_analysis",
                service_type=ServiceType.COMBINATION_ENGINE,
                endpoint="/wardrobe/gaps",
                depends_on=["user_preferences"],
                payload={"user_id": user_id}
            ),
            WorkflowStep(
                step_id="shopping_recommendations",
                service_type=ServiceType.RECOMMENDATION_ENGINE,
                endpoint="/recommendations",
                depends_on=["wardrobe_analysis"],
                payload={
                    "user_id": user_id,
                    "context": "shopping",
                    "num_recommendations": 15,
                    "strategy": "outfit_completion"
                }
            )
        ]
        
        return Workflow(
            workflow_id=workflow_id,
            name="Personalized Shopping",
            description="Generate personalized shopping recommendations based on wardrobe gaps",
            steps=steps,
            created_at=datetime.now(),
            user_id=user_id,
            context=context
        )
    
    def _create_trend_analysis_template(self, workflow_id: str, user_id: str, context: Dict[str, Any]) -> Workflow:
        """Create trend analysis workflow template."""
        steps = [
            WorkflowStep(
                step_id="trending_products",
                service_type=ServiceType.RECOMMENDATION_ENGINE,
                endpoint="/trending",
                method="GET",
                payload={"num_products": 20}
            ),
            WorkflowStep(
                step_id="style_trends",
                service_type=ServiceType.STYLE_PROFILE,
                endpoint="/trends",
                method="GET"
            ),
            WorkflowStep(
                step_id="personalized_trends",
                service_type=ServiceType.RECOMMENDATION_ENGINE,
                endpoint="/recommendations",
                depends_on=["trending_products", "style_trends"],
                payload={
                    "user_id": user_id,
                    "context": "trending",
                    "num_recommendations": 10,
                    "strategy": "trending"
                }
            )
        ]
        
        return Workflow(
            workflow_id=workflow_id,
            name="Trend Analysis",
            description="Analyze current trends and provide personalized trend recommendations",
            steps=steps,
            created_at=datetime.now(),
            user_id=user_id,
            context=context
        )
    
    def _update_orchestration_metrics(self, workflow: Workflow, success: bool):
        """Update orchestration performance metrics."""
        self.orchestration_metrics['total_workflows_executed'] += 1
        
        if success:
            self.orchestration_metrics['successful_workflows'] += 1
        else:
            self.orchestration_metrics['failed_workflows'] += 1
        
        # Update average execution time
        if workflow.total_execution_time:
            current_avg = self.orchestration_metrics['average_execution_time']
            total_count = self.orchestration_metrics['total_workflows_executed']
            
            new_avg = ((current_avg * (total_count - 1)) + workflow.total_execution_time) / total_count
            self.orchestration_metrics['average_execution_time'] = new_avg
    
    def _generate_workflow_analytics(self, workflow: Workflow) -> Dict[str, Any]:
        """Generate comprehensive analytics for a completed workflow."""
        completed_steps = [s for s in workflow.steps if s.status == WorkflowStatus.COMPLETED]
        failed_steps = [s for s in workflow.steps if s.status == WorkflowStatus.FAILED]
        
        return {
            'total_steps': len(workflow.steps),
            'completed_steps': len(completed_steps),
            'failed_steps': len(failed_steps),
            'success_rate': len(completed_steps) / len(workflow.steps) if workflow.steps else 0,
            'average_step_time': sum(s.execution_time for s in completed_steps if s.execution_time) / len(completed_steps) if completed_steps else 0,
            'services_used': list(set(s.service_type.value for s in workflow.steps)),
            'parallel_execution_efficiency': self._calculate_parallel_efficiency(workflow)
        }
    
    def _calculate_parallel_efficiency(self, workflow: Workflow) -> float:
        """Calculate efficiency of parallel step execution."""
        total_sequential_time = sum(s.execution_time for s in workflow.steps if s.execution_time)
        actual_execution_time = workflow.total_execution_time
        
        if total_sequential_time and actual_execution_time:
            return min(total_sequential_time / actual_execution_time, 1.0)
        return 0.0
    
    def _collect_partial_results(self, workflow: Workflow) -> Dict[str, Any]:
        """Collect partial results from a failed workflow."""
        partial_results = {}
        for step in workflow.steps:
            if step.status == WorkflowStatus.COMPLETED and step.result:
                partial_results[step.step_id] = step.result
        return partial_results
    
    def get_orchestration_analytics(self) -> Dict[str, Any]:
        """Get comprehensive orchestration analytics and metrics."""
        return {
            'performance_metrics': self.orchestration_metrics,
            'service_health': self.service_health,
            'active_workflows': len(self.active_workflows),
            'completed_workflows': len(self.completed_workflows),
            'workflow_templates': list(self.workflow_templates.keys()),
            'last_health_check': self.last_health_check.isoformat() if self.last_health_check else None,
            'system_status': 'operational' if len(self.service_health) > 0 else 'initializing'
        }
    
    async def process_user_feedback(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process user feedback through the feedback loop service using prompt engineering patterns.
        This orchestrates the feedback analysis workflow across multiple services.
        """
        workflow_id = str(uuid.uuid4())
        logger.info(f"Processing user feedback - Workflow ID: {workflow_id}")
        
        try:
            # Step 1: Analyze feedback using prompt engineering patterns
            feedback_analysis_step = WorkflowStep(
                step_id=f"feedback_analysis_{workflow_id}",
                service_type=ServiceType.FEEDBACK_LOOP,
                endpoint="/feedback/analyze",
                payload=feedback_data,
                dependencies=[],
                timeout=30
            )
            
            # Execute feedback analysis
            analysis_result = await self._execute_step(feedback_analysis_step)
            
            if not analysis_result.get('success'):
                return {
                    'success': False,
                    'error': 'Feedback analysis failed',
                    'workflow_id': workflow_id
                }
            
            feedback_type = analysis_result['data']['classification_results']['feedback_type']
            
            # Step 2: Based on feedback type, trigger appropriate actions
            action_steps = []
            
            if feedback_type in ['negative_general', 'color_dissatisfaction', 'occasion_inappropriate']:
                # Negative feedback - trigger improvement workflows
                
                # Update style profile based on feedback
                style_update_step = WorkflowStep(
                    step_id=f"style_update_{workflow_id}",
                    service_type=ServiceType.STYLE_PROFILE,
                    endpoint="/profile/update-from-feedback",
                    payload={
                        'user_id': feedback_data.get('user_id'),
                        'feedback_analysis': analysis_result['data'],
                        'improvement_focus': feedback_type
                    },
                    dependencies=[feedback_analysis_step.step_id]
                )
                action_steps.append(style_update_step)
                
                # Request new recommendations based on feedback
                new_recommendation_step = WorkflowStep(
                    step_id=f"new_recommendation_{workflow_id}",
                    service_type=ServiceType.RECOMMENDATION_ENGINE,
                    endpoint="/recommendations/generate-improved",
                    payload={
                        'user_id': feedback_data.get('user_id'),
                        'feedback_context': analysis_result['data'],
                        'avoid_issues': [feedback_type]
                    },
                    dependencies=[style_update_step.step_id]
                )
                action_steps.append(new_recommendation_step)
                
            elif feedback_type == 'request_similar':
                # Positive feedback - generate similar recommendations
                similar_recommendation_step = WorkflowStep(
                    step_id=f"similar_recommendation_{workflow_id}",
                    service_type=ServiceType.RECOMMENDATION_ENGINE,
                    endpoint="/recommendations/generate-similar",
                    payload={
                        'user_id': feedback_data.get('user_id'),
                        'reference_recommendation': feedback_data.get('recommendation_id'),
                        'similarity_factors': analysis_result['data']['insights']['improvement_suggestions']
                    },
                    dependencies=[feedback_analysis_step.step_id]
                )
                action_steps.append(similar_recommendation_step)
                
                # Update positive preferences in style profile
                preference_update_step = WorkflowStep(
                    step_id=f"preference_update_{workflow_id}",
                    service_type=ServiceType.STYLE_PROFILE,
                    endpoint="/profile/update-preferences",
                    payload={
                        'user_id': feedback_data.get('user_id'),
                        'positive_feedback': analysis_result['data'],
                        'reinforcement_type': 'positive'
                    },
                    dependencies=[feedback_analysis_step.step_id]
                )
                action_steps.append(preference_update_step)
            
            # Execute all action steps in parallel where possible
            action_results = []
            for step in action_steps:
                try:
                    result = await self._execute_step(step)
                    action_results.append({
                        'step_id': step.step_id,
                        'result': result
                    })
                except Exception as e:
                    logger.error(f"Action step {step.step_id} failed: {e}")
                    action_results.append({
                        'step_id': step.step_id,
                        'error': str(e)
                    })
            
            # Step 3: Store feedback learning for future improvements
            learning_step = WorkflowStep(
                step_id=f"learning_storage_{workflow_id}",
                service_type=ServiceType.FEEDBACK_LOOP,
                endpoint="/feedback/store-learning",
                payload={
                    'feedback_analysis': analysis_result['data'],
                    'action_results': action_results,
                    'workflow_id': workflow_id
                },
                dependencies=[step['step_id'] for step in action_results if 'error' not in step]
            )
            
            learning_result = await self._execute_step(learning_step)
            
            return {
                'success': True,
                'workflow_id': workflow_id,
                'feedback_analysis': analysis_result['data'],
                'actions_taken': action_results,
                'learning_stored': learning_result.get('success', False),
                'processing_summary': {
                    'feedback_type': feedback_type,
                    'confidence': analysis_result['data']['classification_results']['confidence'],
                    'actions_count': len(action_results),
                    'processing_time': time.time() - time.time()  # Will be calculated properly
                }
            }
            
        except Exception as e:
            logger.error(f"Feedback processing workflow failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'workflow_id': workflow_id
            }
    
    async def get_feedback_insights(self, user_id: Optional[str] = None, 
                                   time_range: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Get comprehensive feedback insights and analytics.
        Aggregates learning patterns and improvement trends.
        """
        try:
            # Get insights from feedback loop service
            insights_payload = {}
            if user_id:
                insights_payload['user_id'] = user_id
            if time_range:
                insights_payload['time_range'] = time_range
            
            async with aiohttp.ClientSession() as session:
                feedback_endpoint = f"{self.service_endpoints[ServiceType.FEEDBACK_LOOP]}/feedback/insights"
                
                async with session.post(feedback_endpoint, json=insights_payload) as response:
                    if response.status == 200:
                        insights_data = await response.json()
                        
                        # Enrich with orchestration context
                        insights_data['orchestration_context'] = {
                            'total_workflows': len(self.completed_workflows),
                            'feedback_workflows': len([w for w in self.completed_workflows 
                                                     if any('feedback' in step.step_id for step in w.steps)]),
                            'average_feedback_processing_time': self._calculate_avg_feedback_time(),
                            'service_coordination_success_rate': self._calculate_coordination_success_rate()
                        }
                        
                        return {
                            'success': True,
                            'insights': insights_data
                        }
                    else:
                        error_detail = await response.text()
                        return {
                            'success': False,
                            'error': f"Failed to get insights: {error_detail}"
                        }
                        
        except Exception as e:
            logger.error(f"Error getting feedback insights: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _calculate_avg_feedback_time(self) -> float:
        """Calculate average processing time for feedback workflows."""
        feedback_workflows = [w for w in self.completed_workflows 
                            if any('feedback' in step.step_id for step in w.steps)]
        
        if not feedback_workflows:
            return 0.0
        
        total_time = sum(w.total_execution_time for w in feedback_workflows if w.total_execution_time)
        return total_time / len(feedback_workflows) if feedback_workflows else 0.0
    
    def _calculate_coordination_success_rate(self) -> float:
        """Calculate success rate of service coordination in feedback workflows."""
        feedback_workflows = [w for w in self.completed_workflows 
                            if any('feedback' in step.step_id for step in w.steps)]
        
        if not feedback_workflows:
            return 0.0
        
        successful_workflows = [w for w in feedback_workflows if w.status == WorkflowStatus.COMPLETED]
        return len(successful_workflows) / len(feedback_workflows) if feedback_workflows else 0.0
