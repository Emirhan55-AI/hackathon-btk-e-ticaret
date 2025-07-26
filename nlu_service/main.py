# Phase 3: Advanced NLU Service with XLM-R Transformer Integration
# Import FastAPI framework for building the REST API
from fastapi import FastAPI, HTTPException
# Import Pydantic for data validation and serialization
from pydantic import BaseModel
# Import JSONResponse for custom response formatting
from fastapi.responses import JSONResponse
# Import the advanced NLU analyzer for Phase 3 capabilities
from nlu_analyzer import AdvancedNLUAnalyzer
import logging

# Configure logging for service monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the main FastAPI application instance
# This handles all API routes and requests for advanced natural language understanding
app = FastAPI(
    title="Aura Advanced NLU Service - Phase 3",  # Updated title for Phase 3
    description="Advanced multilingual natural language understanding using XLM-R transformer for intent classification, sentiment analysis, and context detection",
    version="3.0.0"  # Phase 3 version
)

# Global variable to store the NLU analyzer instance
# This is initialized when the service starts up
nlu_analyzer = None

@app.on_event("startup")
async def startup_event():
    """
    Service startup event handler.
    
    Initializes the advanced NLU analyzer with XLM-R transformer model
    and other AI components. This runs once when the service starts.
    """
    global nlu_analyzer
    
    logger.info("🚀 Starting Advanced NLU Service - Phase 3")
    logger.info("Loading XLM-R transformer and multilingual models...")
    
    try:
        # Initialize the advanced NLU analyzer
        # This loads XLM-R, sentence transformers, and sentiment analysis models
        nlu_analyzer = AdvancedNLUAnalyzer()
        logger.info("✅ Advanced NLU Service initialized successfully")
        logger.info(f"Models loaded: {sum(nlu_analyzer.models_loaded.values())}/3")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize NLU analyzer: {e}")
        logger.info("Service will run in fallback mode with basic functionality")
        nlu_analyzer = None

# Pydantic model for the text input request  
# Enhanced for Phase 3 with additional multilingual support information
class TextRequest(BaseModel):
    text: str  # The user's natural language request (supports EN, TR, ES, FR, DE)
    language_hint: str = None  # Optional language hint to improve processing accuracy
    include_features: bool = False  # Whether to include XLM-R feature embeddings in response

# Enhanced Pydantic model for the analysis response
class NLUResponse(BaseModel):
    message: str
    original_text: str
    detected_language: str
    analysis: dict
    processing_method: str
    model_info: dict

# Root endpoint for health monitoring and service status
# Enhanced for Phase 3 with model status information
@app.get("/")
async def health_check():
    """
    Enhanced health check endpoint for Phase 3 Advanced NLU Service.
    
    Returns service status, model availability, and capabilities information.
    This endpoint is used by load balancers and monitoring systems.
    """
    
    # Get model status if analyzer is available
    model_status = {}
    total_models = 0
    
    if nlu_analyzer:
        model_status = nlu_analyzer.models_loaded
        total_models = sum(model_status.values())
    
    return {
        "status": "Advanced NLU Service is running - Phase 3",
        "service": "nlu",
        "version": "3.0.0",
        "capabilities": [
            "Multilingual support (EN, TR, ES, FR, DE)",
            "XLM-R transformer integration", 
            "Advanced intent classification",
            "Sentiment analysis with confidence scoring",
            "Context and occasion detection",
            "Feature embedding extraction"
        ],
        "model_status": model_status,
        "models_loaded": f"{total_models}/3",
        "processing_mode": "advanced" if total_models >= 2 else "fallback"
    }

# Main advanced natural language processing endpoint
# Completely rewritten for Phase 3 with XLM-R transformer capabilities
@app.post("/parse_request", response_model=dict)
async def parse_request(request: TextRequest):
    """
    Advanced multilingual natural language understanding using XLM-R transformer.
    
    This endpoint performs comprehensive analysis including:
    - Language detection for multilingual support
    - Intent classification using transformer embeddings  
    - Sentiment analysis with confidence scoring
    - Context/occasion detection
    - Feature extraction for downstream tasks
    
    Args:
        request: TextRequest object containing user text and optional parameters
    
    Returns:
        Comprehensive NLU analysis results with confidence scores and model information
    """
    
    # Validate that text was provided in the request
    if not request.text or not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Text field is required and cannot be empty"
        )
    
    # Log the incoming request for monitoring
    logger.info(f"Processing NLU request: '{request.text[:50]}{'...' if len(request.text) > 50 else ''}'")
    
    try:
        # Check if advanced analyzer is available
        if nlu_analyzer is None:
            # Fallback to basic Phase 1 functionality if models aren't loaded
            logger.warning("Advanced models not available, using fallback processing")
            return await _fallback_processing(request.text)
        
        # Perform comprehensive analysis using XLM-R and advanced models
        analysis_results = nlu_analyzer.comprehensive_analysis(request.text)
        
        # Check if analysis was successful
        if "error" in analysis_results:
            logger.error(f"Analysis failed: {analysis_results['error']}")
            return await _fallback_processing(request.text)
        
        # Extract key results for clean response
        language_info = analysis_results.get("language_detection", {})
        intent_info = analysis_results.get("intent_analysis", {})
        sentiment_info = analysis_results.get("sentiment_analysis", {})
        context_info = analysis_results.get("context_analysis", {})
        features_info = analysis_results.get("features", {})
        processing_meta = analysis_results.get("processing_metadata", {})
        
        # Build the response structure
        response = {
            "message": "Text analyzed successfully using advanced XLM-R transformer models",
            "original_text": request.text,
            "detected_language": language_info.get("detected_language", "en"),
            "language_confidence": language_info.get("confidence", 0.0),
            "analysis": {
                "intent": {
                    "predicted_intent": intent_info.get("intent", "unknown"),
                    "confidence": intent_info.get("confidence", 0.0),
                    "method": intent_info.get("method", "unknown"),
                    "all_intent_scores": intent_info.get("all_scores", {})
                },
                "sentiment": {
                    "predicted_sentiment": sentiment_info.get("sentiment", "neutral"),
                    "confidence": sentiment_info.get("confidence", 0.0),
                    "method": sentiment_info.get("method", "unknown"),
                    "all_sentiment_scores": sentiment_info.get("all_scores", {})
                },
                "context": {
                    "predicted_context": context_info.get("context", "casual"),
                    "confidence": context_info.get("confidence", 0.0),
                    "method": context_info.get("method", "unknown"),
                    "all_context_scores": context_info.get("all_scores", {})
                }
            },
            "model_info": {
                "xlm_r_available": nlu_analyzer.models_loaded.get("xlm_r", False),
                "sentence_transformer_available": nlu_analyzer.models_loaded.get("sentence_transformer", False),
                "sentiment_pipeline_available": nlu_analyzer.models_loaded.get("sentiment_pipeline", False),
                "total_models_active": sum(nlu_analyzer.models_loaded.values()),
                "processing_quality": processing_meta.get("analysis_quality", "medium")
            },
            "processing_method": "xlm_r_transformer_ensemble"
        }
        
        # Include feature embeddings if requested
        if request.include_features and features_info.get("xlm_r_embedding"):
            response["features"] = {
                "xlm_r_embedding": features_info["xlm_r_embedding"],
                "embedding_dimension": features_info["embedding_dimension"],
                "note": "768-dimensional XLM-R transformer features for downstream tasks"
            }
        
        logger.info(f"✅ Advanced analysis completed successfully")
        return response
        
    except Exception as e:
        logger.error(f"❌ Unexpected error during analysis: {e}")
        # Return fallback processing in case of any errors
        return await _fallback_processing(request.text)

async def _fallback_processing(text: str) -> dict:
    """
    Fallback processing function using basic keyword-based analysis.
    
    This function is used when advanced models are not available or fail.
    It provides basic functionality similar to Phase 1 implementation.
    
    Args:
        text: Input text to process
        
    Returns:
        Basic analysis results using keyword matching
    """
    
    logger.info("Using fallback processing (keyword-based)")
    
    # Convert text to lowercase for basic processing
    text_lower = text.lower()
    
    # Basic intent detection using keywords
    intent = "unknown"
    if any(word in text_lower for word in ["recommend", "suggest", "want", "need", "looking for"]):
        intent = "product_recommendation"
    elif any(word in text_lower for word in ["combine", "match", "outfit", "style"]):
        intent = "style_combination"
    elif any(word in text_lower for word in ["analyze", "what am i", "my style"]):
        intent = "style_analysis"
    
    # Basic sentiment detection
    sentiment = "neutral"
    if any(word in text_lower for word in ["good", "great", "excellent", "love", "amazing"]):
        sentiment = "positive"
    elif any(word in text_lower for word in ["bad", "terrible", "hate", "awful"]):
        sentiment = "negative"
    
    # Basic context detection
    context = "casual"
    if any(word in text_lower for word in ["sport", "gym", "workout", "exercise"]):
        context = "sport"
    elif any(word in text_lower for word in ["work", "office", "business", "professional"]):
        context = "formal"
    elif any(word in text_lower for word in ["party", "event", "celebration"]):
        context = "party"
    
    return {
        "message": "Text processed using fallback keyword-based analysis",
        "original_text": text,
        "detected_language": "en",  # Default to English in fallback mode
        "language_confidence": 0.5,
        "analysis": {
            "intent": {
                "predicted_intent": intent,
                "confidence": 0.6,
                "method": "keyword_fallback",
                "all_intent_scores": {}
            },
            "sentiment": {
                "predicted_sentiment": sentiment,
                "confidence": 0.6, 
                "method": "keyword_fallback",
                "all_sentiment_scores": {}
            },
            "context": {
                "predicted_context": context,
                "confidence": 0.6,
                "method": "keyword_fallback", 
                "all_context_scores": {}
            }
        },
        "model_info": {
            "xlm_r_available": False,
            "sentence_transformer_available": False,
            "sentiment_pipeline_available": False,
            "total_models_active": 0,
            "processing_quality": "basic"
        },
        "processing_method": "keyword_fallback"
    }
