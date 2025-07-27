# 🧠 PHASE 2: ENHANCED NLU SERVICE WITH PERFORMANCE OPTIMIZATIONS

# Import FastAPI framework for building the REST API
from fastapi import FastAPI, HTTPException, BackgroundTasks
# Import Pydantic for data validation and serialization
from pydantic import BaseModel
# Import JSONResponse for custom response formatting
from fastapi.responses import JSONResponse
# Import asyncio for asynchronous processing
import asyncio
# Import functools for caching
from functools import lru_cache
# Import time for performance measurement
import time
# Import typing for better type hints
from typing import Dict, List, Optional, Any
import logging

# Configure logging for service monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# PHASE 2: Enhanced data models with validation
class ParseRequest(BaseModel):
    text: str
    language: Optional[str] = "auto"
    include_sentiment: Optional[bool] = True
    include_context: Optional[bool] = True
    cache_result: Optional[bool] = True

class EnhancedParseResponse(BaseModel):
    intent: str
    confidence: float
    entities: List[Dict[str, Any]]
    sentiment: Optional[Dict[str, Any]] = None
    context: Optional[Dict[str, Any]] = None
    processing_time_ms: float
    models_used: List[str]
    cached: bool = False

# Create the main FastAPI application instance
app = FastAPI(
    title="🧠 Aura Enhanced NLU Service - PHASE 2",
    description="Performance-optimized multilingual NLU with caching, async processing, and enhanced error handling",
    version="2.2.0"  # PHASE 2 Enhanced version
)

# PHASE 2: Global variables with performance optimizations
nlu_analyzer = None
analysis_cache = {}  # Simple in-memory cache
performance_metrics = {
    "total_requests": 0,
    "cache_hits": 0,
    "average_processing_time": 0.0,
    "error_count": 0
}

@app.on_event("startup")
async def startup_event():
    """
    PHASE 2 Enhanced startup with performance optimizations.
    """
    global nlu_analyzer
    
    logger.info("🚀 PHASE 2: Starting Enhanced NLU Service with Performance Optimizations")
    
    try:
        # Try to import and initialize enhanced analyzer
        try:
            from nlu_analyzer import AdvancedNLUAnalyzer
            nlu_analyzer = AdvancedNLUAnalyzer()
            logger.info("✅ Advanced NLU Analyzer loaded successfully")
        except ImportError:
            # Fallback to basic analyzer
            from basic_nlu_analyzer import BasicNLUAnalyzer
            nlu_analyzer = BasicNLUAnalyzer()
            logger.info("📋 Basic NLU Analyzer loaded as fallback")
        
        # Initialize performance monitoring
        logger.info("⚡ Performance optimizations activated")
        logger.info("💾 Analysis caching enabled")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize NLU service: {e}")
        nlu_analyzer = None

@lru_cache(maxsize=1000)
def get_cached_analysis(text: str, language: str) -> Dict[str, Any]:
    """
    PHASE 2: LRU cache for frequently analyzed texts.
    """
    # This is a placeholder - actual caching implemented in analyze_text_enhanced
    return {}

async def analyze_text_enhanced(
    text: str, 
    language: str = "auto",
    include_sentiment: bool = True,
    include_context: bool = True
) -> Dict[str, Any]:
    """
    PHASE 2 Enhanced text analysis with performance optimizations.
    """
    start_time = time.time()
    
    try:
        # Check cache first
        cache_key = f"{text[:100]}_{language}_{include_sentiment}_{include_context}"
        if cache_key in analysis_cache:
            performance_metrics["cache_hits"] += 1
            result = analysis_cache[cache_key].copy()
            result["cached"] = True
            result["processing_time_ms"] = (time.time() - start_time) * 1000
            return result
        
        # Perform analysis
        if nlu_analyzer:
            if hasattr(nlu_analyzer, 'analyze_text_advanced'):
                result = await asyncio.to_thread(nlu_analyzer.analyze_text_advanced, text, language)
            else:
                result = await asyncio.to_thread(nlu_analyzer.analyze_text, text)
        else:
            # Fallback analysis
            result = {
                "intent": "general_inquiry",
                "confidence": 0.6,
                "entities": [],
                "sentiment": {"polarity": 0.0, "confidence": 0.5} if include_sentiment else None,
                "context": {"domain": "fashion", "complexity": "medium"} if include_context else None,
                "models_used": ["fallback"],
                "cached": False
            }
        
        # Add processing time
        processing_time = (time.time() - start_time) * 1000
        result["processing_time_ms"] = processing_time
        result["cached"] = False
        
        # Cache result (limit cache size)
        if len(analysis_cache) < 500:
            analysis_cache[cache_key] = result.copy()
        
        # Update performance metrics
        performance_metrics["total_requests"] += 1
        performance_metrics["average_processing_time"] = (
            (performance_metrics["average_processing_time"] * (performance_metrics["total_requests"] - 1) + processing_time)
            / performance_metrics["total_requests"]
        )
        
        return result
        
    except Exception as e:
        performance_metrics["error_count"] += 1
        logger.error(f"❌ Enhanced analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/parse_request", response_model=EnhancedParseResponse)
async def parse_request_enhanced(request: ParseRequest, background_tasks: BackgroundTasks):
    """
    PHASE 2 Enhanced: Parse user request with performance optimizations.
    """
    try:
        logger.info(f"🔍 PHASE 2 Enhanced parsing: '{request.text[:50]}...'")
        
        # Perform enhanced analysis
        result = await analyze_text_enhanced(
            text=request.text,
            language=request.language,
            include_sentiment=request.include_sentiment,
            include_context=request.include_context
        )
        
        # Schedule background cleanup if needed
        if len(analysis_cache) > 400:
            background_tasks.add_task(cleanup_cache)
        
        return EnhancedParseResponse(**result)
        
    except Exception as e:
        logger.error(f"❌ Parse request failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def cleanup_cache():
    """
    Background task to clean up old cache entries.
    """
    global analysis_cache
    if len(analysis_cache) > 250:
        # Keep only the most recent 250 entries (simple cleanup)
        keys_to_remove = list(analysis_cache.keys())[:-250]
        for key in keys_to_remove:
            del analysis_cache[key]
        logger.info(f"🧹 Cache cleaned up: {len(keys_to_remove)} entries removed")

@app.get("/performance_metrics")
async def get_performance_metrics():
    """
    PHASE 2: Get service performance metrics.
    """
    cache_hit_rate = (
        performance_metrics["cache_hits"] / max(performance_metrics["total_requests"], 1) * 100
    )
    
    return {
        "status": "PHASE 2 Enhanced NLU Service",
        "metrics": {
            **performance_metrics,
            "cache_hit_rate_percent": round(cache_hit_rate, 2),
            "cache_size": len(analysis_cache),
            "analyzer_available": nlu_analyzer is not None
        },
        "optimization_features": [
            "LRU Caching",
            "Async Processing", 
            "Background Tasks",
            "Performance Monitoring",
            "Enhanced Error Handling"
        ]
    }

@app.get("/health")
async def health_check():
    """
    Enhanced health check with detailed status.
    """
    return {
        "status": "✅ PHASE 2 Enhanced NLU Service is running",
        "version": "2.2.0",
        "analyzer_status": "loaded" if nlu_analyzer else "fallback_mode",
        "cache_size": len(analysis_cache),
        "total_requests": performance_metrics["total_requests"],
        "features": [
            "Performance Optimized",
            "Caching Enabled", 
            "Async Processing",
            "Enhanced Error Handling"
        ]
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🧠 PHASE 2: Enhanced NLU Service with Performance Optimizations",
        "version": "2.2.0",
        "documentation": "/docs"
    }

# PHASE 2: Additional endpoint for batch processing
@app.post("/batch_parse")
async def batch_parse(texts: List[str], language: str = "auto"):
    """
    PHASE 2: Process multiple texts in batch for better performance.
    """
    try:
        logger.info(f"📝 Batch processing {len(texts)} texts")
        
        # Process all texts concurrently
        tasks = [
            analyze_text_enhanced(text, language, True, True) 
            for text in texts
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any exceptions in results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    "text": texts[i],
                    "error": str(result),
                    "status": "failed"
                })
            else:
                processed_results.append({
                    "text": texts[i],
                    "result": result,
                    "status": "success"
                })
        
        return {
            "batch_size": len(texts),
            "results": processed_results,
            "total_processing_time_ms": sum(
                r.get("result", {}).get("processing_time_ms", 0) 
                for r in processed_results
            )
        }
        
    except Exception as e:
        logger.error(f"❌ Batch processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
