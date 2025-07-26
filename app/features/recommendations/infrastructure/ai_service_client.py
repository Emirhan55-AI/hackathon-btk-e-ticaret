import httpx
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class AIServiceClient:
    """Client for AI recommendation service."""
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = base_url or "https://api.example-ai-service.com"
        self.api_key = api_key or "demo-api-key"
        self.timeout = 30.0
    
    async def generate_outfit_recommendations(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate outfit recommendations based on user data."""
        try:
            logger.info("Generating outfit recommendations via AI service")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/v1/recommendations/outfits",
                    json=request_data,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    }
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.warning(f"AI service returned {response.status_code}: {response.text}")
                    return self._generate_fallback_recommendations(request_data)
                    
        except httpx.TimeoutException:
            logger.warning("AI service request timed out, using fallback")
            return self._generate_fallback_recommendations(request_data)
        except Exception as e:
            logger.error(f"Error calling AI service: {e}")
            return self._generate_fallback_recommendations(request_data)
    
    async def generate_quick_recommendations(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate quick recommendations without full analysis."""
        try:
            logger.info("Generating quick recommendations via AI service")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/v1/recommendations/quick",
                    json=request_data,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    }
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.warning(f"AI service returned {response.status_code}: {response.text}")
                    return self._generate_quick_fallback_recommendations(request_data)
                    
        except httpx.TimeoutException:
            logger.warning("AI service request timed out, using fallback")
            return self._generate_quick_fallback_recommendations(request_data)
        except Exception as e:
            logger.error(f"Error calling AI service: {e}")
            return self._generate_quick_fallback_recommendations(request_data)
    
    def _generate_fallback_recommendations(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback recommendations when AI service is unavailable."""
        logger.info("Generating fallback outfit recommendations")
        
        occasion = request_data.get("occasion", "casual")
        season = request_data.get("season", "spring")
        preferred_colors = request_data.get("preferred_colors", ["navy", "white", "gray"])
        preferred_styles = request_data.get("preferred_styles", ["casual", "comfortable"])
        
        # Generate basic recommendations based on occasion and season
        outfits = []
        
        if occasion == "work" or occasion == "professional":
            outfits.append({
                "name": f"Professional {season.title()} Outfit",
                "item_ids": [],  # Would be populated with actual items
                "occasion": occasion,
                "season": season,
                "confidence_score": 0.7,
                "styling_tips": [
                    "Choose well-fitted pieces for a polished look",
                    "Stick to neutral colors for versatility",
                    "Add minimal accessories for sophistication"
                ]
            })
        elif occasion == "casual":
            outfits.append({
                "name": f"Casual {season.title()} Look",
                "item_ids": [],
                "occasion": occasion,
                "season": season,
                "confidence_score": 0.75,
                "styling_tips": [
                    "Comfort is key for casual outfits",
                    "Mix textures for visual interest",
                    "Add your personal touch with accessories"
                ]
            })
        elif occasion == "formal":
            outfits.append({
                "name": f"Formal {season.title()} Ensemble",
                "item_ids": [],
                "occasion": occasion,
                "season": season,
                "confidence_score": 0.8,
                "styling_tips": [
                    "Choose classic silhouettes",
                    "Pay attention to fit and tailoring",
                    "Keep accessories elegant and minimal"
                ]
            })
        else:
            # Generic recommendation
            outfits.append({
                "name": f"Stylish {season.title()} Outfit",
                "item_ids": [],
                "occasion": occasion or "versatile",
                "season": season,
                "confidence_score": 0.65,
                "styling_tips": [
                    "Choose pieces that reflect your personal style",
                    "Consider the weather and comfort",
                    "Have fun with your outfit choices"
                ]
            })
        
        return {
            "outfits": outfits,
            "status": "fallback",
            "message": "Generated using fallback recommendations"
        }
    
    def _generate_quick_fallback_recommendations(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate quick fallback recommendations."""
        logger.info("Generating quick fallback recommendations")
        
        occasion = request_data.get("occasion", "casual")
        weather = request_data.get("weather", "mild")
        
        outfits = [{
            "name": f"Quick {occasion.title()} Suggestion",
            "item_ids": [],
            "occasion": occasion,
            "confidence_score": 0.6,
            "styling_tips": [
                f"Perfect for {occasion} occasions",
                f"Suitable for {weather} weather",
                "Quick and easy to put together"
            ]
        }]
        
        return {
            "outfits": outfits,
            "status": "quick_fallback",
            "message": "Generated using quick fallback recommendations"
        }
    
    async def analyze_style_preferences(self, quiz_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze user's style preferences from quiz data."""
        try:
            logger.info("Analyzing style preferences via AI service")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/v1/analysis/style-preferences",
                    json={"quiz_data": quiz_data},
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    }
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.warning(f"AI service returned {response.status_code}: {response.text}")
                    return self._generate_style_analysis_fallback(quiz_data)
                    
        except Exception as e:
            logger.error(f"Error analyzing style preferences: {e}")
            return self._generate_style_analysis_fallback(quiz_data)
    
    def _generate_style_analysis_fallback(self, quiz_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate fallback style analysis."""
        return {
            "style_profile": {
                "dominant_style": "classic",
                "confidence": 0.7,
                "secondary_styles": ["casual", "elegant"]
            },
            "preferred_colors": ["navy", "white", "gray", "black"],
            "lifestyle_factors": {
                "activity_level": "moderate",
                "formality_preference": "smart_casual"
            },
            "status": "fallback",
            "message": "Generated using fallback style analysis"
        }
