# 🧠 AURA AI QUALITY ASSURANCE SERVICE - RCI SYSTEM
# FastAPI service implementing Recursive Criticism and Improvement for AI output validation

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import asyncio
import json
import httpx
from contextlib import asynccontextmanager

# Import our RCI Quality Engine
from rci_quality_engine import (
    RCIQualityEngine, 
    ValidationResult, 
    ValidationStatus, 
    CriticalityLevel,
    ValidationCriteria,
    create_rci_engine,
    validate_fashion_recommendation
)

# Configure comprehensive logging for RCI service tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global RCI engine instance - initialized on startup
rci_engine: Optional[RCIQualityEngine] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager - handles startup and shutdown tasks.
    Initializes the RCI engine when the service starts.
    """
    global rci_engine
    
    # Startup: Initialize RCI Quality Engine
    logger.info("🧠 Initializing AURA AI Quality Assurance Service")
    logger.info("🔧 Setting up RCI (Recursive Criticism and Improvement) Engine")
    
    try:
        # Create RCI engine with default criteria
        rci_engine = create_rci_engine()
        logger.info("✅ RCI Quality Engine initialized successfully")
        
        # Log system capabilities
        summary = rci_engine.get_validation_summary()
        logger.info(f"📊 Active validators: {', '.join(summary['active_validators'])}")
        logger.info(f"🎯 Minimum quality score: {summary['validation_criteria']['minimum_overall_score']}")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize RCI engine: {str(e)}")
        raise
    
    yield
    
    # Shutdown: Clean up resources
    logger.info("🔄 Shutting down AURA AI Quality Assurance Service")

# Create FastAPI application with lifespan management
app = FastAPI(
    title="AURA AI Quality Assurance Service",
    description="RCI (Recursive Criticism and Improvement) system for validating AI fashion recommendations",
    version="1.0.0",
    lifespan=lifespan
)

# Pydantic models for API request/response handling

class ValidationRequest(BaseModel):
    """
    Request model for AI output validation.
    Contains the AI recommendation and context for comprehensive analysis.
    """
    ai_output: Dict[str, Any] = Field(
        ..., 
        description="The AI-generated recommendation to validate",
        example={
            "items": [
                {"type": "shirt", "color": "red", "name": "Red dress shirt"},
                {"type": "pants", "color": "green", "name": "Green formal pants"}
            ],
            "colors": ["red", "green"],
            "style_tags": ["business", "formal"],
            "confidence": 0.85
        }
    )
    
    context: Dict[str, Any] = Field(
        ...,
        description="Context information for validation (user profile, occasion, etc.)",
        example={
            "service_source": "combination_engine",
            "occasion": "work",
            "user_id": "user_123",
            "user_preferences": {"style": "conservative", "colors": ["blue", "white"]},
            "season": "summer",
            "budget_range": "medium"
        }
    )
    
    custom_criteria: Optional[Dict[str, float]] = Field(
        None,
        description="Optional custom validation criteria to override defaults",
        example={
            "minimum_overall_score": 0.8,
            "color_harmony_threshold": 0.75,
            "style_coherence_threshold": 0.8
        }
    )

class ValidationIssueResponse(BaseModel):
    """
    Response model for individual validation issues found in AI output.
    """
    category: str = Field(..., description="Type of issue (color_harmony, style_coherence, etc.)")
    description: str = Field(..., description="Human-readable description of the issue")
    criticality: str = Field(..., description="Severity level: low, medium, high, critical")
    confidence: float = Field(..., description="Confidence in this issue assessment (0.0-1.0)")
    improvement_suggestion: str = Field(..., description="Specific suggestion for fixing this issue")
    affected_components: List[str] = Field(..., description="Components affected by this issue")
    validation_rule_id: str = Field(..., description="ID of the validation rule that found this issue")

class ValidationResponse(BaseModel):
    """
    Comprehensive response model for AI output validation results.
    Contains scores, issues, improvements, and alternatives.
    """
    # Basic validation metadata
    output_id: str = Field(..., description="Unique identifier for this validation")
    service_source: str = Field(..., description="AI service that generated the original output")
    timestamp: datetime = Field(..., description="When this validation was performed")
    
    # Overall validation results
    status: str = Field(..., description="Overall validation status: approved, needs_improvement, rejected")
    overall_score: float = Field(..., description="Overall quality score (0.0-1.0)")
    confidence: float = Field(..., description="Confidence in validation results (0.0-1.0)")
    
    # Detailed scoring breakdown
    color_harmony_score: float = Field(..., description="Color combination quality score (0.0-1.0)")
    style_coherence_score: float = Field(..., description="Style consistency score (0.0-1.0)")
    occasion_appropriateness_score: float = Field(..., description="Occasion matching score (0.0-1.0)")
    user_preference_score: float = Field(..., description="User preference alignment score (0.0-1.0)")
    
    # Issues and improvements
    issues_found: int = Field(..., description="Total number of issues identified")
    critical_issues_found: int = Field(..., description="Number of critical issues identified")
    issues: List[ValidationIssueResponse] = Field(..., description="Detailed list of all issues found")
    improvement_suggestions: List[str] = Field(..., description="Concrete suggestions for improvement")
    alternative_recommendations: List[Dict[str, Any]] = Field(..., description="Alternative recommendation options")
    
    # Performance and learning metadata
    validation_duration_ms: float = Field(..., description="Time taken for validation in milliseconds")
    revalidation_required: bool = Field(..., description="Whether this output needs to be validated again")
    
class ServiceHealthResponse(BaseModel):
    """
    Response model for service health check.
    """
    service: str = Field(..., description="Service name and description")
    status: str = Field(..., description="Service status: healthy, degraded, unhealthy")
    version: str = Field(..., description="Service version")
    rci_engine_status: str = Field(..., description="RCI engine initialization status")
    active_validators: List[str] = Field(..., description="List of active validation modules")
    validation_criteria: Dict[str, float] = Field(..., description="Current validation thresholds")
    timestamp: datetime = Field(..., description="Health check timestamp")

class BulkValidationRequest(BaseModel):
    """
    Request model for validating multiple AI outputs at once.
    Useful for batch processing and performance testing.
    """
    validation_requests: List[ValidationRequest] = Field(
        ...,
        description="List of validation requests to process",
        max_items=50  # Limit batch size for performance
    )
    
    processing_mode: str = Field(
        "parallel",
        description="Processing mode: parallel or sequential",
        pattern="^(parallel|sequential)$"
    )

class BulkValidationResponse(BaseModel):
    """
    Response model for bulk validation results.
    """
    total_requests: int = Field(..., description="Total number of validation requests processed")
    successful_validations: int = Field(..., description="Number of successful validations")
    failed_validations: int = Field(..., description="Number of failed validations")
    processing_duration_ms: float = Field(..., description="Total processing time in milliseconds")
    results: List[ValidationResponse] = Field(..., description="Individual validation results")
    summary_statistics: Dict[str, Any] = Field(..., description="Summary statistics across all validations")

# API Endpoints

@app.get("/", response_model=ServiceHealthResponse)
async def health_check():
    """
    Health check endpoint that returns service status and RCI engine information.
    Used by other services and monitoring systems to verify service availability.
    """
    global rci_engine
    
    logger.info("🏥 Health check requested")
    
    if rci_engine is None:
        logger.error("❌ RCI engine not initialized")
        raise HTTPException(status_code=503, detail="RCI engine not initialized")
    
    try:
        # Get RCI engine summary for health status
        summary = rci_engine.get_validation_summary()
        
        return ServiceHealthResponse(
            service="AURA AI Quality Assurance Service - RCI System",
            status="healthy",
            version="1.0.0",
            rci_engine_status="operational",
            active_validators=summary["active_validators"],
            validation_criteria=summary["validation_criteria"],
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"❌ Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")

@app.post("/validate", response_model=ValidationResponse)
async def validate_ai_output(request: ValidationRequest):
    """
    Main validation endpoint that analyzes AI output quality using RCI methodology.
    
    This endpoint implements the core RCI (Recursive Criticism and Improvement) process:
    1. Receives AI recommendation and context
    2. Runs comprehensive validation using multiple validators
    3. Generates quality scores and identifies issues
    4. Provides improvement suggestions and alternatives
    5. Returns comprehensive validation results
    """
    global rci_engine
    
    if rci_engine is None:
        logger.error("❌ RCI engine not available for validation")
        raise HTTPException(status_code=503, detail="RCI engine not initialized")
    
    logger.info(f"🔍 Validation requested for output from {request.context.get('service_source', 'unknown')}")
    
    try:
        # Create custom RCI engine if custom criteria provided
        engine = rci_engine
        if request.custom_criteria:
            logger.info("🔧 Using custom validation criteria")
            custom_criteria = ValidationCriteria(
                minimum_overall_score=request.custom_criteria.get("minimum_overall_score", 0.7),
                color_harmony_threshold=request.custom_criteria.get("color_harmony_threshold", 0.7),
                style_coherence_threshold=request.custom_criteria.get("style_coherence_threshold", 0.75)
            )
            engine = create_rci_engine(custom_criteria)
        
        # Perform comprehensive validation
        validation_result = await engine.validate_ai_output(request.ai_output, request.context)
        
        # Convert internal result to API response format
        issues_response = []
        for issue in validation_result.issues:
            issues_response.append(ValidationIssueResponse(
                category=issue.category,
                description=issue.description,
                criticality=issue.criticality.value,
                confidence=issue.confidence,
                improvement_suggestion=issue.improvement_suggestion,
                affected_components=issue.affected_components,
                validation_rule_id=issue.validation_rule_id
            ))
        
        response = ValidationResponse(
            output_id=validation_result.output_id,
            service_source=validation_result.service_source,
            timestamp=validation_result.timestamp,
            status=validation_result.status.value,
            overall_score=validation_result.overall_score,
            confidence=validation_result.confidence,
            color_harmony_score=validation_result.color_harmony_score,
            style_coherence_score=validation_result.style_coherence_score,
            occasion_appropriateness_score=validation_result.occasion_appropriateness_score,
            user_preference_score=validation_result.user_preference_score,
            issues_found=len(validation_result.issues),
            critical_issues_found=len(validation_result.critical_issues),
            issues=issues_response,
            improvement_suggestions=validation_result.improvement_suggestions,
            alternative_recommendations=validation_result.alternative_recommendations,
            validation_duration_ms=validation_result.validation_duration_ms,
            revalidation_required=validation_result.revalidation_required
        )
        
        # Log validation outcome
        logger.info(f"✅ Validation {validation_result.output_id} completed: {validation_result.status.value}, score={validation_result.overall_score:.2f}")
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Validation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")

@app.post("/validate-bulk", response_model=BulkValidationResponse)
async def validate_bulk_outputs(request: BulkValidationRequest):
    """
    Bulk validation endpoint for processing multiple AI outputs efficiently.
    Supports both parallel and sequential processing modes.
    """
    global rci_engine
    
    if rci_engine is None:
        raise HTTPException(status_code=503, detail="RCI engine not initialized")
    
    logger.info(f"📦 Bulk validation requested: {len(request.validation_requests)} items, mode={request.processing_mode}")
    
    start_time = datetime.now()
    results = []
    successful_count = 0
    failed_count = 0
    
    try:
        if request.processing_mode == "parallel":
            # Process all validations in parallel for speed
            tasks = []
            for val_request in request.validation_requests:
                task = asyncio.create_task(validate_single_output_safely(val_request))
                tasks.append(task)
            
            # Wait for all validations to complete
            validation_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results and count successes/failures
            for result in validation_results:
                if isinstance(result, ValidationResponse):
                    results.append(result)
                    successful_count += 1
                else:
                    failed_count += 1
                    logger.error(f"Bulk validation item failed: {str(result)}")
        
        else:  # Sequential processing
            for val_request in request.validation_requests:
                try:
                    result = await validate_single_output_safely(val_request)
                    if result:
                        results.append(result)
                        successful_count += 1
                    else:
                        failed_count += 1
                except Exception as e:
                    logger.error(f"Sequential validation item failed: {str(e)}")
                    failed_count += 1
        
        # Calculate processing duration
        duration = (datetime.now() - start_time).total_seconds() * 1000
        
        # Generate summary statistics
        summary_stats = generate_bulk_validation_summary(results)
        
        response = BulkValidationResponse(
            total_requests=len(request.validation_requests),
            successful_validations=successful_count,
            failed_validations=failed_count,
            processing_duration_ms=duration,
            results=results,
            summary_statistics=summary_stats
        )
        
        logger.info(f"📊 Bulk validation completed: {successful_count}/{len(request.validation_requests)} successful, {duration:.1f}ms")
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Bulk validation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Bulk validation failed: {str(e)}")

@app.get("/validators", response_model=Dict[str, Any])
async def get_validator_info():
    """
    Get information about available validators and their capabilities.
    Useful for understanding what aspects of AI output are being validated.
    """
    global rci_engine
    
    if rci_engine is None:
        raise HTTPException(status_code=503, detail="RCI engine not initialized")
    
    try:
        summary = rci_engine.get_validation_summary()
        
        return {
            "system_info": {
                "name": summary["system_name"],
                "version": summary["version"]
            },
            "active_validators": summary["active_validators"],
            "validation_criteria": summary["validation_criteria"],
            "capabilities": summary["capabilities"],
            "validator_details": {
                "ColorHarmonyValidator": {
                    "description": "Validates color combinations using color theory principles",
                    "checks": ["complementary colors", "analogous colors", "color temperature", "contrast levels"],
                    "output_format": "color harmony score (0.0-1.0) with specific color improvement suggestions"
                },
                "StyleCoherenceValidator": {
                    "description": "Ensures style consistency and appropriate formality levels",
                    "checks": ["formality gap analysis", "style category compatibility", "occasion appropriateness"],
                    "output_format": "style coherence score (0.0-1.0) with style improvement recommendations"
                }
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get validator info: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get validator info: {str(e)}")

@app.post("/test-scenarios", response_model=Dict[str, Any])
async def test_validation_scenarios():
    """
    Test endpoint that runs predefined validation scenarios to verify system functionality.
    Useful for system testing and demonstrating RCI capabilities.
    """
    global rci_engine
    
    if rci_engine is None:
        raise HTTPException(status_code=503, detail="RCI engine not initialized")
    
    logger.info("🧪 Running validation test scenarios")
    
    # Define test scenarios that demonstrate different validation outcomes
    test_scenarios = [
        {
            "name": "Problematic Red + Green Combination",
            "ai_output": {
                "items": [
                    {"type": "shirt", "color": "red", "name": "Red dress shirt"},
                    {"type": "pants", "color": "green", "name": "Green formal pants"}
                ],
                "colors": ["red", "green"],
                "style_tags": ["business", "formal"]
            },
            "context": {
                "service_source": "combination_engine",
                "occasion": "work",
                "user_preferences": {"style": "conservative"}
            },
            "expected_outcome": "needs_improvement_or_rejected"
        },
        {
            "name": "Classic Black + Red Combination",
            "ai_output": {
                "items": [
                    {"type": "dress", "color": "black", "name": "Black cocktail dress"},
                    {"type": "shoes", "color": "red", "name": "Red statement heels"}
                ],
                "colors": ["black", "red"],
                "style_tags": ["elegant", "formal"]
            },
            "context": {
                "service_source": "recommendation_engine",
                "occasion": "dinner",
                "user_preferences": {"style": "bold"}
            },
            "expected_outcome": "approved"
        },
        {
            "name": "Formality Mismatch - Denim + Suit",
            "ai_output": {
                "items": [
                    {"type": "jacket", "color": "blue", "name": "Denim jacket"},
                    {"type": "pants", "color": "black", "name": "Formal suit pants"},
                    {"type": "shirt", "color": "white", "name": "Dress shirt"}
                ],
                "colors": ["blue", "black", "white"],
                "style_tags": ["mixed", "casual", "formal"]
            },
            "context": {
                "service_source": "combination_engine",
                "occasion": "business_casual",
                "user_preferences": {"style": "creative"}
            },
            "expected_outcome": "needs_improvement"
        }
    ]
    
    test_results = []
    
    try:
        for scenario in test_scenarios:
            logger.info(f"🧪 Testing scenario: {scenario['name']}")
            
            # Run validation for this scenario
            validation_result = await rci_engine.validate_ai_output(scenario["ai_output"], scenario["context"])
            
            # Evaluate if the result matches expectations
            outcome_match = evaluate_test_outcome(validation_result.status.value, scenario["expected_outcome"])
            
            test_results.append({
                "scenario_name": scenario["name"],
                "validation_status": validation_result.status.value,
                "overall_score": validation_result.overall_score,
                "issues_found": len(validation_result.issues),
                "critical_issues": len(validation_result.critical_issues),
                "expected_outcome": scenario["expected_outcome"],
                "outcome_matches_expectation": outcome_match,
                "improvement_suggestions": validation_result.improvement_suggestions[:2],  # First 2 suggestions
                "validation_duration_ms": validation_result.validation_duration_ms
            })
        
        # Calculate overall test success rate
        successful_tests = sum(1 for result in test_results if result["outcome_matches_expectation"])
        success_rate = (successful_tests / len(test_results)) * 100
        
        return {
            "test_summary": {
                "total_scenarios": len(test_scenarios),
                "successful_tests": successful_tests,
                "success_rate_percent": success_rate,
                "test_timestamp": datetime.now().isoformat()
            },
            "individual_results": test_results,
            "system_status": "healthy" if success_rate >= 80 else "needs_attention"
        }
        
    except Exception as e:
        logger.error(f"❌ Test scenarios failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Test scenarios failed: {str(e)}")

# Helper functions

async def validate_single_output_safely(request: ValidationRequest) -> Optional[ValidationResponse]:
    """
    Safely validate a single output with error handling for bulk operations.
    """
    try:
        # Use the main validation endpoint logic
        return await validate_ai_output(request)
    except Exception as e:
        logger.error(f"Single validation failed in bulk operation: {str(e)}")
        return None

def generate_bulk_validation_summary(results: List[ValidationResponse]) -> Dict[str, Any]:
    """
    Generate summary statistics for bulk validation results.
    """
    if not results:
        return {"message": "No successful validations to summarize"}
    
    # Calculate score statistics
    scores = [result.overall_score for result in results]
    color_scores = [result.color_harmony_score for result in results]
    style_scores = [result.style_coherence_score for result in results]
    
    # Calculate status distribution
    status_counts = {}
    for result in results:
        status = result.status
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Calculate issue statistics
    total_issues = sum(result.issues_found for result in results)
    total_critical_issues = sum(result.critical_issues_found for result in results)
    
    return {
        "score_statistics": {
            "average_overall_score": sum(scores) / len(scores),
            "average_color_harmony_score": sum(color_scores) / len(color_scores),
            "average_style_coherence_score": sum(style_scores) / len(style_scores),
            "min_score": min(scores),
            "max_score": max(scores)
        },
        "status_distribution": status_counts,
        "issue_statistics": {
            "total_issues_found": total_issues,
            "total_critical_issues": total_critical_issues,
            "average_issues_per_validation": total_issues / len(results),
            "percentage_with_critical_issues": (sum(1 for r in results if r.critical_issues_found > 0) / len(results)) * 100
        },
        "performance_statistics": {
            "average_validation_time_ms": sum(result.validation_duration_ms for result in results) / len(results),
            "total_validations": len(results)
        }
    }

def evaluate_test_outcome(actual_status: str, expected_outcome: str) -> bool:
    """
    Evaluate if a test scenario outcome matches expectations.
    """
    if expected_outcome == "approved":
        return actual_status == "approved"
    elif expected_outcome == "needs_improvement":
        return actual_status == "needs_improvement"
    elif expected_outcome == "rejected":
        return actual_status == "rejected"
    elif expected_outcome == "needs_improvement_or_rejected":
        return actual_status in ["needs_improvement", "rejected"]
    else:
        return False

# Background task for sending validation feedback to other services
async def send_validation_feedback_to_services(validation_result: ValidationResult, context: Dict[str, Any]):
    """
    Send validation feedback to the AI service that generated the original output.
    This enables the RCI system to help other services learn and improve.
    """
    service_source = context.get("service_source")
    if not service_source:
        return
    
    # Map service names to their endpoints
    service_endpoints = {
        "image_processing": "http://localhost:8001/feedback/validation",
        "nlu_service": "http://localhost:8002/feedback/validation",
        "style_profile": "http://localhost:8003/feedback/validation",
        "combination_engine": "http://localhost:8004/feedback/validation",
        "recommendation_engine": "http://localhost:8005/feedback/validation"
    }
    
    endpoint = service_endpoints.get(service_source)
    if not endpoint:
        logger.warning(f"Unknown service source for feedback: {service_source}")
        return
    
    # Prepare feedback data
    feedback_data = {
        "output_id": validation_result.output_id,
        "validation_score": validation_result.overall_score,
        "status": validation_result.status.value,
        "issues": [
            {
                "category": issue.category,
                "description": issue.description,
                "improvement": issue.improvement_suggestion
            }
            for issue in validation_result.issues
        ],
        "learning_feedback": validation_result.learning_feedback
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(endpoint, json=feedback_data, timeout=5.0)
            if response.status_code == 200:
                logger.info(f"✅ Validation feedback sent to {service_source}")
            else:
                logger.warning(f"⚠️ Feedback to {service_source} failed: {response.status_code}")
    except Exception as e:
        logger.warning(f"⚠️ Failed to send feedback to {service_source}: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    # Run the RCI Quality Assurance service
    logger.info("🚀 Starting AURA AI Quality Assurance Service")
    uvicorn.run(app, host="0.0.0.0", port=8008, log_level="info")
