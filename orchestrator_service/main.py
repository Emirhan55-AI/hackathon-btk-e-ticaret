# Phase 7: Service Orchestration FastAPI Application
# Main FastAPI application for coordinating complex workflows across all Aura AI services
# Provides unified API endpoints for multi-service orchestration and workflow management

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import logging
import json
from datetime import datetime
import asyncio
import uuid
import traceback
from contextlib import asynccontextmanager

# Import the workflow orchestrator
from workflow_orchestrator import AuraOrchestrator, WorkflowStatus, ServiceType

# Configure comprehensive logging for the orchestration service
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global orchestrator instance
orchestrator: Optional[AuraOrchestrator] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for proper startup and shutdown.
    Initializes orchestrator and manages HTTP session lifecycle.
    """
    global orchestrator
    logger.info("🚀 Starting Aura Service Orchestration System - Phase 7")
    
    # Initialize orchestrator with HTTP session
    orchestrator = AuraOrchestrator()
    async with orchestrator:
        # Perform initial health check
        try:
            health_status = await orchestrator.check_service_health()
            healthy_services = sum(1 for health in health_status.values() if health['status'] == 'healthy')
            logger.info(f"✅ Initial health check: {healthy_services}/{len(health_status)} services healthy")
        except Exception as e:
            logger.warning(f"⚠️ Initial health check failed: {e}")
        
        logger.info("🎯 Orchestration service ready for workflow coordination")
        yield
    
    logger.info("🔄 Shutting down Aura Service Orchestration System")

# Create FastAPI application with comprehensive configuration
app = FastAPI(
    title="Aura Service Orchestration Engine",
    description="""
    # Aura Service Orchestration Engine - Phase 7
    
    Advanced orchestration system for coordinating complex AI workflows across all Aura services.
    
    ## Key Features
    - **Multi-Service Workflows**: Coordinate image processing, NLU, style profiling, combinations, and recommendations
    - **Dependency Management**: Execute workflow steps in correct order with parallel processing
    - **Error Handling**: Comprehensive retry logic and graceful degradation
    - **Performance Analytics**: Real-time monitoring and workflow optimization
    - **Template System**: Pre-built workflows for common use cases
    - **Health Monitoring**: Continuous service health checking and reporting
    
    ## Services Orchestrated
    - **Image Processing Service** (Port 8001): Computer vision and clothing analysis
    - **NLU Service** (Port 8002): Natural language understanding
    - **Style Profile Service** (Port 8003): User style profiling and analysis
    - **Combination Engine Service** (Port 8004): Intelligent outfit combinations
    - **Recommendation Engine Service** (Port 8005): FAISS-powered recommendations
    
    ## Workflow Templates
    - **complete_style_analysis**: Full pipeline analysis
    - **outfit_recommendation**: Generate outfit suggestions
    - **style_evolution_analysis**: Track style changes over time
    - **personalized_shopping**: Shopping recommendations
    - **trend_analysis**: Current trend analysis
    """,
    version="7.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
class WorkflowRequest(BaseModel):
    """
    Request model for creating and executing workflows.
    Contains all information needed to orchestrate multi-service workflows.
    """
    template_name: str = Field(..., description="Name of the workflow template to use")
    user_id: str = Field(..., description="User identifier for personalization")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context for workflow execution")
    
    class Config:
        schema_extra = {
            "example": {
                "template_name": "complete_style_analysis",
                "user_id": "user123",
                "context": {
                    "image_url": "https://example.com/outfit.jpg",
                    "user_description": "Looking for casual office wear",
                    "occasion": "business_casual"
                }
            }
        }

class WorkflowResponse(BaseModel):
    """
    Response model for workflow execution results.
    Contains comprehensive execution information and analytics.
    """
    workflow_id: str
    status: str
    execution_time: Optional[float] = None
    steps_executed: Optional[int] = None
    steps_failed: Optional[int] = None
    results: Optional[Dict[str, Any]] = None
    analytics: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    partial_results: Optional[Dict[str, Any]] = None

class ServiceHealthResponse(BaseModel):
    """
    Response model for service health information.
    Contains detailed health status for all orchestrated services.
    """
    services: Dict[str, Dict[str, Any]]
    overall_health: str
    healthy_services: int
    total_services: int
    last_check: Optional[str] = None

class OrchestrationAnalyticsResponse(BaseModel):
    """
    Response model for orchestration analytics and metrics.
    Provides comprehensive performance and operational insights.
    """
    performance_metrics: Dict[str, Any]
    service_health: Dict[str, Any]
    active_workflows: int
    completed_workflows: int
    workflow_templates: List[str]
    system_status: str

# API Endpoints

@app.get("/", response_model=Dict[str, Any])
async def health_check():
    """
    Health check endpoint for the orchestration service.
    Provides service status, capabilities, and availability information.
    """
    return {
        "service": "Aura Service Orchestration Engine",
        "phase": "Phase 7 - Service Orchestration and Workflow Management",
        "status": "operational",
        "version": "7.0.0",
        "capabilities": [
            "multi_service_workflow_orchestration",
            "dependency_management",
            "parallel_step_execution", 
            "error_handling_retry_logic",
            "performance_analytics",
            "workflow_templates",
            "service_health_monitoring",
            "real_time_orchestration"
        ],
        "service_info": {
            "description": "Advanced orchestration engine for coordinating complex AI workflows",
            "orchestrated_services": 5,
            "workflow_templates": 5,
            "supported_operations": [
                "complete_style_analysis",
                "outfit_recommendation", 
                "style_evolution_analysis",
                "personalized_shopping",
                "trend_analysis"
            ]
        },
        "timestamp": datetime.now().isoformat(),
        "documentation": "/docs"
    }

@app.get("/health", response_model=ServiceHealthResponse)
async def check_service_health():
    """
    Comprehensive health check for all orchestrated services.
    Monitors service availability, response times, and capabilities.
    """
    try:
        logger.info("Performing comprehensive service health check")
        
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not initialized")
        
        # Perform health check on all services
        health_status = await orchestrator.check_service_health()
        
        # Calculate overall health metrics
        healthy_services = sum(1 for health in health_status.values() if health['status'] == 'healthy')
        total_services = len(health_status)
        
        # Determine overall health status
        if healthy_services == total_services:
            overall_health = "excellent"
        elif healthy_services >= total_services * 0.8:
            overall_health = "good"
        elif healthy_services >= total_services * 0.5:
            overall_health = "degraded"
        else:
            overall_health = "critical"
        
        logger.info(f"✅ Health check completed: {healthy_services}/{total_services} services healthy")
        
        return ServiceHealthResponse(
            services=health_status,
            overall_health=overall_health,
            healthy_services=healthy_services,
            total_services=total_services,
            last_check=orchestrator.last_health_check.isoformat() if orchestrator.last_health_check else None
        )
        
    except Exception as e:
        logger.error(f"❌ Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.get("/workflows/templates", response_model=Dict[str, List[str]])
async def get_workflow_templates():
    """
    Get list of available workflow templates.
    Returns all pre-configured workflow templates with descriptions.
    """
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not initialized")
        
        templates = {
            "available_templates": list(orchestrator.workflow_templates.keys()),
            "template_descriptions": {
                "complete_style_analysis": "Comprehensive style analysis including image processing, NLU, profiling, combinations, and recommendations",
                "outfit_recommendation": "Generate outfit recommendations based on user style profile",
                "style_evolution_analysis": "Analyze user's style evolution and predict future trends", 
                "personalized_shopping": "Generate personalized shopping recommendations based on wardrobe gaps",
                "trend_analysis": "Analyze current trends and provide personalized trend recommendations"
            }
        }
        
        logger.info(f"📋 Returning {len(templates['available_templates'])} workflow templates")
        return templates
        
    except Exception as e:
        logger.error(f"❌ Failed to get workflow templates: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get templates: {str(e)}")

@app.post("/workflows/execute", response_model=WorkflowResponse)
async def execute_workflow(request: WorkflowRequest):
    """
    Execute a workflow using a specified template.
    Orchestrates multi-service AI workflows with dependency management and error handling.
    """
    try:
        logger.info(f"🎯 Executing workflow: {request.template_name} for user {request.user_id}")
        
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not initialized")
        
        # Validate template exists
        if request.template_name not in orchestrator.workflow_templates:
            available_templates = list(orchestrator.workflow_templates.keys())
            raise HTTPException(
                status_code=400, 
                detail=f"Unknown workflow template: {request.template_name}. Available: {available_templates}"
            )
        
        # Create workflow from template
        workflow = orchestrator.create_workflow(
            template_name=request.template_name,
            user_id=request.user_id,
            context=request.context
        )
        
        # Execute workflow asynchronously
        execution_results = await orchestrator.execute_workflow(workflow)
        
        logger.info(f"✅ Workflow executed successfully: {workflow.workflow_id}")
        
        return WorkflowResponse(**execution_results)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Workflow execution failed: {str(e)}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Workflow execution failed: {str(e)}")

@app.post("/workflows/execute/async", response_model=Dict[str, str])
async def execute_workflow_async(request: WorkflowRequest, background_tasks: BackgroundTasks):
    """
    Execute a workflow asynchronously in the background.
    Returns workflow ID immediately and executes workflow in background.
    """
    try:
        logger.info(f"🔄 Starting async workflow: {request.template_name} for user {request.user_id}")
        
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not initialized")
        
        # Validate template exists
        if request.template_name not in orchestrator.workflow_templates:
            available_templates = list(orchestrator.workflow_templates.keys())
            raise HTTPException(
                status_code=400,
                detail=f"Unknown workflow template: {request.template_name}. Available: {available_templates}"
            )
        
        # Create workflow from template
        workflow = orchestrator.create_workflow(
            template_name=request.template_name,
            user_id=request.user_id,
            context=request.context
        )
        
        # Add workflow execution to background tasks
        background_tasks.add_task(execute_workflow_background, workflow.workflow_id)
        
        logger.info(f"📤 Async workflow queued: {workflow.workflow_id}")
        
        return {
            "workflow_id": workflow.workflow_id,
            "status": "queued",
            "message": "Workflow execution started in background",
            "check_status_endpoint": f"/workflows/{workflow.workflow_id}/status"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Async workflow creation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Async workflow creation failed: {str(e)}")

async def execute_workflow_background(workflow_id: str):
    """
    Background task for executing workflows asynchronously.
    Handles workflow execution without blocking the API response.
    """
    try:
        if not orchestrator or workflow_id not in orchestrator.active_workflows:
            logger.error(f"❌ Cannot execute background workflow: {workflow_id}")
            return
        
        workflow = orchestrator.active_workflows[workflow_id]
        await orchestrator.execute_workflow(workflow)
        
        logger.info(f"✅ Background workflow completed: {workflow_id}")
        
    except Exception as e:
        logger.error(f"❌ Background workflow failed: {workflow_id} - {str(e)}")

@app.get("/workflows/{workflow_id}/status", response_model=Dict[str, Any])
async def get_workflow_status(workflow_id: str):
    """
    Get the current status of a workflow execution.
    Provides real-time status updates for both active and completed workflows.
    """
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not initialized")
        
        # Check active workflows first
        if workflow_id in orchestrator.active_workflows:
            workflow = orchestrator.active_workflows[workflow_id]
            return {
                "workflow_id": workflow_id,
                "status": workflow.status.value,
                "name": workflow.name,
                "created_at": workflow.created_at.isoformat(),
                "started_at": workflow.started_at.isoformat() if workflow.started_at else None,
                "steps_total": len(workflow.steps),
                "steps_completed": len([s for s in workflow.steps if s.status == WorkflowStatus.COMPLETED]),
                "steps_failed": len([s for s in workflow.steps if s.status == WorkflowStatus.FAILED]),
                "current_step": next((s.step_id for s in workflow.steps if s.status == WorkflowStatus.RUNNING), None)
            }
        
        # Check completed workflows
        elif workflow_id in orchestrator.completed_workflows:
            workflow = orchestrator.completed_workflows[workflow_id]
            return {
                "workflow_id": workflow_id,
                "status": workflow.status.value,
                "name": workflow.name,
                "created_at": workflow.created_at.isoformat(),
                "started_at": workflow.started_at.isoformat() if workflow.started_at else None,
                "completed_at": workflow.completed_at.isoformat() if workflow.completed_at else None,
                "execution_time": workflow.total_execution_time,
                "steps_total": len(workflow.steps),
                "steps_completed": len([s for s in workflow.steps if s.status == WorkflowStatus.COMPLETED]),
                "steps_failed": len([s for s in workflow.steps if s.status == WorkflowStatus.FAILED])
            }
        
        else:
            raise HTTPException(status_code=404, detail=f"Workflow not found: {workflow_id}")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get workflow status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get workflow status: {str(e)}")

@app.get("/workflows", response_model=Dict[str, Any])
async def list_workflows(limit: int = 50, offset: int = 0, status: Optional[str] = None):
    """
    List workflows with pagination and filtering.
    Returns active and completed workflows with optional status filtering.
    """
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not initialized")
        
        # Combine active and completed workflows
        all_workflows = {}
        all_workflows.update(orchestrator.active_workflows)
        all_workflows.update(orchestrator.completed_workflows)
        
        # Filter by status if specified
        if status:
            filtered_workflows = {
                wid: workflow for wid, workflow in all_workflows.items()
                if workflow.status.value == status
            }
        else:
            filtered_workflows = all_workflows
        
        # Apply pagination
        workflow_items = list(filtered_workflows.items())
        paginated_workflows = workflow_items[offset:offset + limit]
        
        # Format response
        workflows_data = []
        for workflow_id, workflow in paginated_workflows:
            workflows_data.append({
                "workflow_id": workflow_id,
                "name": workflow.name,
                "status": workflow.status.value,
                "user_id": workflow.user_id,
                "created_at": workflow.created_at.isoformat(),
                "execution_time": workflow.total_execution_time,
                "steps_total": len(workflow.steps),
                "steps_completed": len([s for s in workflow.steps if s.status == WorkflowStatus.COMPLETED])
            })
        
        return {
            "workflows": workflows_data,
            "total_count": len(filtered_workflows),
            "page_info": {
                "offset": offset,
                "limit": limit,
                "has_more": offset + limit < len(filtered_workflows)
            },
            "filters": {
                "status": status
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to list workflows: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list workflows: {str(e)}")

@app.get("/analytics", response_model=OrchestrationAnalyticsResponse)
async def get_orchestration_analytics():
    """
    Get comprehensive orchestration analytics and performance metrics.
    Provides insights into system performance, service health, and workflow statistics.
    """
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not initialized")
        
        analytics = orchestrator.get_orchestration_analytics()
        
        logger.info("📊 Returning orchestration analytics")
        
        return OrchestrationAnalyticsResponse(**analytics)
        
    except Exception as e:
        logger.error(f"❌ Failed to get analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get analytics: {str(e)}")

@app.delete("/workflows/{workflow_id}", response_model=Dict[str, str])
async def cancel_workflow(workflow_id: str):
    """
    Cancel an active workflow execution.
    Stops workflow execution and marks it as cancelled.
    """
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not initialized")
        
        if workflow_id not in orchestrator.active_workflows:
            raise HTTPException(status_code=404, detail=f"Active workflow not found: {workflow_id}")
        
        workflow = orchestrator.active_workflows[workflow_id]
        workflow.status = WorkflowStatus.CANCELLED
        workflow.completed_at = datetime.now()
        
        if workflow.started_at:
            workflow.total_execution_time = (workflow.completed_at - workflow.started_at).total_seconds()
        
        # Move to completed workflows
        orchestrator.completed_workflows[workflow_id] = workflow
        del orchestrator.active_workflows[workflow_id]
        
        logger.info(f"🚫 Workflow cancelled: {workflow_id}")
        
        return {
            "workflow_id": workflow_id,
            "status": "cancelled",
            "message": "Workflow execution cancelled successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to cancel workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to cancel workflow: {str(e)}")

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 Not Found errors with helpful information."""
    return {
        "error": "Resource not found",
        "message": "The requested resource could not be found",
        "available_endpoints": [
            "/docs - API documentation",
            "/health - Service health check", 
            "/workflows/templates - Available workflow templates",
            "/workflows/execute - Execute workflow",
            "/analytics - Orchestration analytics"
        ]
    }

@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    """Handle 500 Internal Server Error with debugging information."""
    logger.error(f"Internal server error: {exc}")
    return {
        "error": "Internal server error",
        "message": "An unexpected error occurred in the orchestration service",
        "support": "Check logs for detailed error information"
    }

if __name__ == "__main__":
    import uvicorn
    
    logger.info("🚀 Starting Aura Service Orchestration Engine")
    logger.info("   Phase 7: Advanced Multi-Service Workflow Orchestration")
    logger.info("   Port: 8006")
    logger.info("   Documentation: http://localhost:8006/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8006,
        reload=True,
        log_level="info"
    )
