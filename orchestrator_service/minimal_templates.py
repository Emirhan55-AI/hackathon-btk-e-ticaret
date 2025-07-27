#!/usr/bin/env python3
"""
Minimal templates endpoint without complex FastAPI validation.
Emergency workaround for orchestrator templates issue.
"""

from fastapi import FastAPI, HTTPException
import json

# Create minimal app
minimal_app = FastAPI(title="Minimal Templates Service", version="1.0.0")

@minimal_app.get("/templates")
async def get_templates():
    """Minimal templates endpoint"""
    try:
        return {
            "available_templates": [
                "complete_style_analysis",
                "outfit_recommendation", 
                "style_evolution_analysis",
                "personalized_shopping",
                "trend_analysis"
            ],
            "template_descriptions": {
                "complete_style_analysis": "Comprehensive style analysis including image processing, NLU, profiling, combinations, and recommendations",
                "outfit_recommendation": "Generate outfit recommendations based on user style profile",
                "style_evolution_analysis": "Analyze user's style evolution and predict future trends",
                "personalized_shopping": "Generate personalized shopping recommendations based on wardrobe gaps", 
                "trend_analysis": "Analyze current trends and provide personalized trend recommendations"
            }
        }
    except Exception as e:
        return {"error": str(e)}

@minimal_app.get("/health")
async def health():
    """Minimal health check"""
    return {"status": "ok", "message": "Minimal templates service is working"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(minimal_app, host="0.0.0.0", port=8007)
