# 🎯 AURA AI - END-TO-END WORKFLOW ORCHESTRATOR (PHASE 1 CRITICAL)
# Bu sistem, kullanıcının fotoğraf yüklemesinden öneriye kadar tüm süreci koordine eder
# Akış Mühendisliği (Flow Engineering) prensipleriyle tasarlanmıştır

# FastAPI framework imports
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Standard library imports
import asyncio
import aiohttp
import time
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI application instance for E2E workflow coordination
app = FastAPI(
    title="🔄 Aura E2E Workflow Orchestrator",
    description="End-to-end workflow orchestration for complete AI-powered shopping experience",
    version="1.0.0"
)

# Enable CORS for web interface integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service endpoint configuration - all microservices in the Aura ecosystem
SERVICE_ENDPOINTS = {
    'image_processing': 'http://localhost:8001',
    'nlu': 'http://localhost:8002', 
    'style_profile': 'http://localhost:8003',
    'combination_engine': 'http://localhost:8004',
    'recommendation': 'http://localhost:8005',
    'orchestrator': 'http://localhost:8006',
    'feedback': 'http://localhost:8007',
    'backend': 'http://localhost:8000'
}

@dataclass
class WorkflowState:
    """Workflow execution state tracking"""
    workflow_id: str
    user_request: str
    current_step: int
    total_steps: int
    status: str
    results: Dict[str, Any]
    errors: List[str]
    start_time: float
    step_times: Dict[str, float]

class E2EWorkflowOrchestrator:
    """
    End-to-End Workflow Orchestrator for Aura AI System
    
    This class coordinates the complete flow from image upload to final recommendation:
    1. Image Processing (Clothing Detection & Analysis)
    2. NLU Processing (User Intent Understanding)  
    3. Style Profile Creation (User Style Analysis)
    4. Combination Generation (Outfit Suggestions)
    5. Recommendation Engine (Product Suggestions)  
    6. Feedback Processing (Learning & Improvement)
    """
    
    def __init__(self):
        self.active_workflows: Dict[str, WorkflowState] = {}
        self.session = None
        
    async def initialize(self):
        """Initialize HTTP session for service communication"""
        if self.session is None:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30)
            )
            logger.info("🚀 E2E Workflow Orchestrator initialized")
    
    async def cleanup(self):
        """Clean up HTTP session"""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def execute_complete_workflow(
        self, 
        image_file: UploadFile, 
        user_request: str,
        user_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Execute the complete end-to-end workflow
        
        This method orchestrates all AI services to provide a complete
        shopping recommendation experience from image upload to final suggestions.
        """
        workflow_id = f"workflow_{int(time.time())}"
        
        # Initialize workflow state
        workflow_state = WorkflowState(
            workflow_id=workflow_id,
            user_request=user_request,
            current_step=0,
            total_steps=6,
            status="initializing",
            results={},
            errors=[],
            start_time=time.time(),
            step_times={}
        )
        
        self.active_workflows[workflow_id] = workflow_state
        
        try:
            logger.info(f"🎬 Starting E2E workflow {workflow_id}")
            
            # Step 1: Image Processing & Clothing Analysis
            workflow_state.current_step = 1
            workflow_state.status = "processing_image"
            step_start = time.time()
            
            image_analysis = await self.process_image_analysis(image_file)
            workflow_state.results['image_analysis'] = image_analysis
            workflow_state.step_times['image_processing'] = time.time() - step_start
            
            logger.info(f"✅ Step 1 completed: Image analysis")
            
            # Step 2: Natural Language Understanding
            workflow_state.current_step = 2
            workflow_state.status = "processing_nlu"
            step_start = time.time()
            
            nlu_analysis = await self.process_nlu_analysis(user_request, user_context)
            workflow_state.results['nlu_analysis'] = nlu_analysis
            workflow_state.step_times['nlu_processing'] = time.time() - step_start
            
            logger.info(f"✅ Step 2 completed: NLU analysis")
            
            # Step 3: Style Profile Creation
            workflow_state.current_step = 3
            workflow_state.status = "creating_profile"
            step_start = time.time()
            
            style_profile = await self.create_style_profile(
                image_analysis, nlu_analysis, user_context
            )
            workflow_state.results['style_profile'] = style_profile
            workflow_state.step_times['style_profiling'] = time.time() - step_start
            
            logger.info(f"✅ Step 3 completed: Style profile creation")
            
            # Step 4: Combination Generation
            workflow_state.current_step = 4
            workflow_state.status = "generating_combinations"
            step_start = time.time()
            
            combinations = await self.generate_combinations(
                style_profile, nlu_analysis, image_analysis
            )
            workflow_state.results['combinations'] = combinations
            workflow_state.step_times['combination_generation'] = time.time() - step_start
            
            logger.info(f"✅ Step 4 completed: Combination generation")
            
            # Step 5: Recommendation Engine
            workflow_state.current_step = 5
            workflow_state.status = "generating_recommendations"
            step_start = time.time()
            
            recommendations = await self.generate_recommendations(
                combinations, style_profile, nlu_analysis
            )
            workflow_state.results['recommendations'] = recommendations
            workflow_state.step_times['recommendation_generation'] = time.time() - step_start
            
            logger.info(f"✅ Step 5 completed: Recommendation generation")
            
            # Step 6: Workflow Completion & Result Compilation
            workflow_state.current_step = 6
            workflow_state.status = "compiling_results"
            step_start = time.time()
            
            final_results = await self.compile_final_results(workflow_state)
            workflow_state.results['final_output'] = final_results
            workflow_state.step_times['result_compilation'] = time.time() - step_start
            
            workflow_state.status = "completed"
            total_time = time.time() - workflow_state.start_time
            
            logger.info(f"🎉 E2E workflow {workflow_id} completed in {total_time:.2f}s")
            
            return {
                "workflow_id": workflow_id,
                "status": "success",
                "total_processing_time": total_time,
                "step_times": workflow_state.step_times,
                "results": final_results,
                "metadata": {
                    "steps_completed": workflow_state.current_step,
                    "total_steps": workflow_state.total_steps,
                    "user_request": user_request,
                    "timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            workflow_state.status = "failed"
            workflow_state.errors.append(str(e))
            logger.error(f"❌ E2E workflow {workflow_id} failed: {str(e)}")
            
            return {
                "workflow_id": workflow_id,
                "status": "failed",
                "error": str(e),
                "step_failed": workflow_state.current_step,
                "partial_results": workflow_state.results
            }
    
    async def process_image_analysis(self, image_file: UploadFile) -> Dict[str, Any]:
        """Step 1: Process image through AI image analysis service"""
        try:
            # Prepare image data for upload
            image_data = await image_file.read()
            
            # Create multipart form data
            data = aiohttp.FormData()
            data.add_field('file', image_data, 
                          filename=image_file.filename,
                          content_type=image_file.content_type)
            
            # Send request to image processing service
            async with self.session.post(
                f"{SERVICE_ENDPOINTS['image_processing']}/analyze_image",
                data=data
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    logger.info("🖼️ Image analysis completed successfully")
                    return result
                else:
                    # Fallback to mock data if service unavailable
                    logger.warning(f"Image service unavailable ({response.status}), using fallback")
                    return await self.get_mock_image_analysis(image_file.filename)
                    
        except Exception as e:
            logger.error(f"Image analysis error: {e}")
            return await self.get_mock_image_analysis(image_file.filename)
    
    async def process_nlu_analysis(self, user_request: str, context: Dict = None) -> Dict[str, Any]:
        """Step 2: Process user request through NLU service"""
        try:
            payload = {
                "text": user_request,
                "language": "tr",
                "context": context or {}
            }
            
            async with self.session.post(
                f"{SERVICE_ENDPOINTS['nlu']}/parse_request",
                json=payload
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    logger.info("🗣️ NLU analysis completed successfully")
                    return result
                else:
                    logger.warning(f"NLU service unavailable ({response.status}), using fallback")
                    return await self.get_mock_nlu_analysis(user_request)
                    
        except Exception as e:
            logger.error(f"NLU analysis error: {e}")
            return await self.get_mock_nlu_analysis(user_request)
    
    async def create_style_profile(self, image_analysis: Dict, nlu_analysis: Dict, context: Dict = None) -> Dict[str, Any]:
        """Step 3: Create user style profile"""
        try:
            payload = {
                "image_analysis": image_analysis,
                "nlu_analysis": nlu_analysis,
                "user_context": context or {}
            }
            
            async with self.session.post(
                f"{SERVICE_ENDPOINTS['style_profile']}/create_profile",
                json=payload
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    logger.info("👤 Style profile created successfully")
                    return result
                else:
                    logger.warning(f"Style profile service unavailable ({response.status}), using fallback")
                    return await self.get_mock_style_profile()
                    
        except Exception as e:
            logger.error(f"Style profile error: {e}")
            return await self.get_mock_style_profile()
    
    async def generate_combinations(self, style_profile: Dict, nlu_analysis: Dict, image_analysis: Dict) -> Dict[str, Any]:
        """Step 4: Generate clothing combinations"""
        try:
            payload = {
                "style_profile": style_profile,
                "nlu_analysis": nlu_analysis,
                "image_analysis": image_analysis
            }
            
            async with self.session.post(
                f"{SERVICE_ENDPOINTS['combination_engine']}/generate_combinations",
                json=payload
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    logger.info("🎨 Combinations generated successfully")
                    return result
                else:
                    logger.warning(f"Combination service unavailable ({response.status}), using fallback")
                    return await self.get_mock_combinations()
                    
        except Exception as e:
            logger.error(f"Combination generation error: {e}")
            return await self.get_mock_combinations()
    
    async def generate_recommendations(self, combinations: Dict, style_profile: Dict, nlu_analysis: Dict) -> Dict[str, Any]:
        """Step 5: Generate product recommendations"""
        try:
            payload = {
                "combinations": combinations,
                "style_profile": style_profile,
                "nlu_analysis": nlu_analysis
            }
            
            async with self.session.post(
                f"{SERVICE_ENDPOINTS['recommendation']}/get_recommendations",
                json=payload
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    logger.info("🎯 Recommendations generated successfully")
                    return result
                else:
                    logger.warning(f"Recommendation service unavailable ({response.status}), using fallback")
                    return await self.get_mock_recommendations()
                    
        except Exception as e:
            logger.error(f"Recommendation generation error: {e}")
            return await self.get_mock_recommendations()
    
    async def compile_final_results(self, workflow_state: WorkflowState) -> Dict[str, Any]:
        """Step 6: Compile all results into final output"""
        try:
            results = workflow_state.results
            
            # Extract key information from each step
            detected_items = results.get('image_analysis', {}).get('analysis_result', {}).get('detected_items', [])
            user_intent = results.get('nlu_analysis', {}).get('intent', 'product_search')
            style_type = results.get('style_profile', {}).get('style_type', 'casual')
            combinations = results.get('combinations', {}).get('combinations', [])
            recommendations = results.get('recommendations', {}).get('recommendations', [])
            
            # Compile comprehensive final results
            final_output = {
                "workflow_summary": {
                    "user_request": workflow_state.user_request,
                    "detected_clothing": [item.get('category', 'unknown') for item in detected_items],
                    "user_intent": user_intent,
                    "recommended_style": style_type,
                    "total_combinations": len(combinations),
                    "total_recommendations": len(recommendations)
                },
                "image_analysis_summary": {
                    "items_detected": len(detected_items),
                    "primary_colors": results.get('image_analysis', {}).get('analysis_result', {}).get('color_analysis', {}).get('dominant_colors', [])[:3],
                    "style_detected": results.get('image_analysis', {}).get('analysis_result', {}).get('style_analysis', {}).get('overall_style', 'casual')
                },
                "user_intent_summary": {
                    "primary_intent": user_intent,
                    "context": results.get('nlu_analysis', {}).get('context', 'shopping'),
                    "sentiment": results.get('nlu_analysis', {}).get('sentiment', 'positive')
                },
                "style_recommendations": {
                    "recommended_style": style_type,
                    "style_confidence": results.get('style_profile', {}).get('confidence', 0.8),
                    "style_attributes": results.get('style_profile', {}).get('style_attributes', [])
                },
                "outfit_combinations": combinations[:5],  # Top 5 combinations
                "product_recommendations": recommendations[:10],  # Top 10 products
                "confidence_scores": {
                    "image_analysis": results.get('image_analysis', {}).get('analysis_result', {}).get('metadata', {}).get('confidence_overall', 0.75),
                    "nlu_analysis": results.get('nlu_analysis', {}).get('confidence', 0.85),
                    "style_matching": results.get('style_profile', {}).get('confidence', 0.8),
                    "recommendations": results.get('recommendations', {}).get('confidence_avg', 0.82)
                },
                "processing_metadata": {
                    "workflow_id": workflow_state.workflow_id,
                    "total_processing_time": time.time() - workflow_state.start_time,
                    "step_breakdown": workflow_state.step_times,
                    "services_used": list(SERVICE_ENDPOINTS.keys()),
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            logger.info("📋 Final results compiled successfully")
            return final_output
            
        except Exception as e:
            logger.error(f"Result compilation error: {e}")
            return {"error": "Failed to compile final results", "details": str(e)}
    
    # Mock data methods for fallback when services are unavailable
    
    async def get_mock_image_analysis(self, filename: str) -> Dict[str, Any]:
        """Mock image analysis for fallback"""
        return {
            "status": "✅ Analysis completed successfully (MOCK)",
            "analysis_result": {
                "detected_items": [
                    {
                        "category": "shirt",
                        "confidence": 0.87,
                        "bounding_box": [0.2, 0.1, 0.8, 0.7],
                        "attributes": {
                            "color": "blue",
                            "style": "casual",
                            "pattern": "solid",
                            "material": "cotton"
                        }
                    }
                ],
                "style_analysis": {
                    "overall_style": "casual",
                    "formality_score": 0.3,
                    "trendiness_score": 0.7
                },
                "color_analysis": {
                    "dominant_colors": [
                        {"color": "blue", "percentage": 45.2, "hex": "#4169E1"},
                        {"color": "white", "percentage": 30.1, "hex": "#FFFFFF"}
                    ]
                },
                "metadata": {
                    "analysis_type": "mock",
                    "confidence_overall": 0.75
                }
            }
        }
    
    async def get_mock_nlu_analysis(self, user_request: str) -> Dict[str, Any]:
        """Mock NLU analysis for fallback"""
        return {
            "intent": "product_recommendation",
            "context": "shopping",
            "sentiment": "positive",
            "entities": {
                "product_category": "clothing",
                "style_preference": "casual"
            },
            "confidence": 0.85,
            "analysis_type": "mock"
        }
    
    async def get_mock_style_profile(self) -> Dict[str, Any]:
        """Mock style profile for fallback"""
        return {
            "style_type": "modern_casual",
            "confidence": 0.8,
            "style_attributes": ["casual", "modern", "comfortable"],
            "color_preferences": ["blue", "white", "black"],
            "analysis_type": "mock"
        }
    
    async def get_mock_combinations(self) -> Dict[str, Any]:
        """Mock combinations for fallback"""
        return {
            "combinations": [
                {
                    "id": 1,
                    "style": "casual_smart",
                    "items": ["shirt", "jeans", "sneakers"],
                    "confidence": 0.9
                },
                {
                    "id": 2,
                    "style": "sporty_casual",
                    "items": ["t-shirt", "shorts", "running_shoes"],
                    "confidence": 0.85
                }
            ],
            "analysis_type": "mock"
        }
    
    async def get_mock_recommendations(self) -> Dict[str, Any]:
        """Mock recommendations for fallback"""
        return {
            "recommendations": [
                {
                    "product_id": 1,
                    "name": "Premium Cotton Shirt",
                    "price": 299.99,
                    "confidence": 0.92,
                    "match_reason": "Perfect style match"
                },
                {
                    "product_id": 2,
                    "name": "Classic Blue Jeans",
                    "price": 199.99,
                    "confidence": 0.88,
                    "match_reason": "Color coordination"
                }
            ],
            "confidence_avg": 0.9,
            "analysis_type": "mock"
        }

# Global orchestrator instance
orchestrator = E2EWorkflowOrchestrator()

@app.on_event("startup")
async def startup_event():
    """Initialize the orchestrator on application startup"""
    await orchestrator.initialize()
    logger.info("🚀 E2E Workflow Orchestrator started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up the orchestrator on application shutdown"""
    await orchestrator.cleanup()
    logger.info("🛑 E2E Workflow Orchestrator shut down")

# API Endpoints

@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "🟢 E2E Workflow Orchestrator is running",
        "service": "e2e_workflow_orchestrator",
        "version": "1.0.0",
        "capabilities": [
            "complete_workflow_orchestration",
            "image_processing_coordination",
            "nlu_processing_coordination", 
            "style_profile_coordination",
            "combination_generation_coordination",
            "recommendation_coordination",
            "fallback_mock_data_support"
        ],
        "active_workflows": len(orchestrator.active_workflows)
    }

@app.post("/execute_complete_workflow")
async def execute_complete_workflow(
    file: UploadFile = File(...),
    user_request: str = Form(...),
    user_context: str = Form(default="{}")
):
    """
    Execute the complete end-to-end workflow
    
    This endpoint coordinates all AI services to process:
    1. Image analysis
    2. NLU processing  
    3. Style profiling
    4. Combination generation
    5. Product recommendations
    6. Result compilation
    """
    try:
        context = json.loads(user_context) if user_context != "{}" else {}
        
        logger.info(f"🎬 Starting complete workflow for request: '{user_request}'")
        
        result = await orchestrator.execute_complete_workflow(
            image_file=file,
            user_request=user_request,
            user_context=context
        )
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Workflow execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Workflow failed: {str(e)}")

@app.get("/workflow_status/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    """Get the status of a specific workflow"""
    if workflow_id in orchestrator.active_workflows:
        workflow = orchestrator.active_workflows[workflow_id]
        return {
            "workflow_id": workflow_id,
            "status": workflow.status,
            "current_step": workflow.current_step,
            "total_steps": workflow.total_steps,
            "progress_percentage": (workflow.current_step / workflow.total_steps) * 100,
            "elapsed_time": time.time() - workflow.start_time,
            "errors": workflow.errors
        }
    else:
        raise HTTPException(status_code=404, detail="Workflow not found")

@app.get("/active_workflows")
async def get_active_workflows():
    """Get all active workflows"""
    return {
        "active_workflows": len(orchestrator.active_workflows),
        "workflows": [
            {
                "workflow_id": wf.workflow_id,
                "status": wf.status,
                "current_step": wf.current_step,
                "user_request": wf.user_request
            }
            for wf in orchestrator.active_workflows.values()
        ]
    }

@app.get("/service_health")
async def check_service_health():
    """Check health of all dependent services"""
    health_status = {}
    
    for service_name, endpoint in SERVICE_ENDPOINTS.items():
        try:
            async with orchestrator.session.get(f"{endpoint}/", timeout=5) as response:
                health_status[service_name] = {
                    "status": "healthy" if response.status == 200 else "unhealthy",
                    "response_code": response.status,
                    "endpoint": endpoint
                }
        except Exception as e:
            health_status[service_name] = {
                "status": "unreachable",
                "error": str(e),
                "endpoint": endpoint
            }
    
    healthy_services = sum(1 for s in health_status.values() if s["status"] == "healthy")
    total_services = len(SERVICE_ENDPOINTS)
    
    return {
        "overall_health": f"{healthy_services}/{total_services} services healthy",
        "health_percentage": (healthy_services / total_services) * 100,
        "services": health_status
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8008)
