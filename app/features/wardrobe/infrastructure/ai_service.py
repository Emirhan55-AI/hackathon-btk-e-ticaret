from typing import Optional, Dict, Any
import httpx
import logging
from datetime import datetime

from app.core.config import settings
from app.core.exceptions import ExternalServiceError
from app.features.wardrobe.application.schemas import AITagResponse

logger = logging.getLogger("app.features.wardrobe.infrastructure.ai_service")


class AIServiceClient:
    """Client for AI service integration."""
    
    def __init__(self, http_client: httpx.AsyncClient):
        self.http_client = http_client
        self.base_url = settings.ai_service_url
        self.api_key = settings.ai_service_api_key
        self.timeout = 30.0
    
    async def analyze_clothing_image(
        self, 
        image_data: bytes, 
        filename: str,
        user_provided_info: Optional[Dict[str, Any]] = None
    ) -> AITagResponse:
        """Send image to AI service for analysis."""
        try:
            # Prepare the request
            files = {
                'image': (filename, image_data, 'image/jpeg')
            }
            
            data = {
                'analysis_type': 'clothing_item',
                'include_color_analysis': True,
                'include_style_analysis': True,
                'include_occasion_analysis': True
            }
            
            # Add user-provided information if available
            if user_provided_info:
                data.update({
                    'user_category': user_provided_info.get('category'),
                    'user_color': user_provided_info.get('color'),
                    'user_brand': user_provided_info.get('brand')
                })
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'X-Request-ID': f'wardrobe_{datetime.now().isoformat()}'
            }
            
            # Make request to AI service
            response = await self.http_client.post(
                f"{self.base_url}/analyze/clothing",
                files=files,
                data=data,
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return self._parse_ai_response(result)
            elif response.status_code == 422:
                logger.warning(f"AI service validation error: {response.text}")
                raise ExternalServiceError("Invalid image or parameters")
            elif response.status_code == 429:
                logger.warning("AI service rate limit exceeded")
                raise ExternalServiceError("AI service temporarily unavailable")
            else:
                logger.error(f"AI service error: {response.status_code} - {response.text}")
                raise ExternalServiceError("AI analysis failed")
                
        except httpx.TimeoutException:
            logger.error("AI service timeout")
            raise ExternalServiceError("AI service timeout")
        except httpx.RequestError as e:
            logger.error(f"AI service request error: {e}")
            raise ExternalServiceError("AI service unavailable")
        except Exception as e:
            logger.error(f"Unexpected AI service error: {e}")
            raise ExternalServiceError("AI analysis failed")
    
    def _parse_ai_response(self, response_data: Dict[str, Any]) -> AITagResponse:
        """Parse AI service response into our schema."""
        try:
            # Map AI service response to our schema
            # This is a mock implementation - adjust based on actual AI service response format
            analysis = response_data.get('analysis', {})
            
            return AITagResponse(
                style=analysis.get('style'),
                pattern=analysis.get('pattern'),
                material=analysis.get('material'),
                fit=analysis.get('fit'),
                occasion=analysis.get('occasions', []),
                season=analysis.get('seasons', []),
                color_analysis=analysis.get('color_analysis', {}),
                confidence=analysis.get('confidence', 0.5),
                attributes=analysis.get('additional_attributes', {})
            )
            
        except Exception as e:
            logger.error(f"Error parsing AI response: {e}")
            # Return minimal response if parsing fails
            return AITagResponse(
                confidence=0.0,
                attributes={'parsing_error': str(e)}
            )
    
    async def health_check(self) -> bool:
        """Check if AI service is available."""
        try:
            response = await self.http_client.get(
                f"{self.base_url}/health",
                timeout=5.0
            )
            return response.status_code == 200
        except:
            return False


class MockAIServiceClient(AIServiceClient):
    """Mock AI service client for development/testing."""
    
    async def analyze_clothing_image(
        self, 
        image_data: bytes, 
        filename: str,
        user_provided_info: Optional[Dict[str, Any]] = None
    ) -> AITagResponse:
        """Mock AI analysis - returns sample data."""
        logger.info(f"Mock AI analysis for {filename}")
        
        # Simulate processing delay
        import asyncio
        await asyncio.sleep(1)
        
        # Return mock analysis based on filename or user info
        category = user_provided_info.get('category', 'tops') if user_provided_info else 'tops'
        color = user_provided_info.get('color', 'blue') if user_provided_info else 'blue'
        
        mock_data = {
            'tops': {
                'style': 'casual',
                'pattern': 'solid',
                'material': 'cotton',
                'fit': 'regular',
                'occasion': ['casual', 'work'],
                'season': ['spring', 'summer', 'fall']
            },
            'bottoms': {
                'style': 'casual',
                'pattern': 'solid',
                'material': 'denim',
                'fit': 'straight',
                'occasion': ['casual', 'everyday'],
                'season': ['all-season']
            },
            'dresses': {
                'style': 'elegant',
                'pattern': 'floral',
                'material': 'polyester',
                'fit': 'a-line',
                'occasion': ['formal', 'party'],
                'season': ['spring', 'summer']
            }
        }
        
        data = mock_data.get(category, mock_data['tops'])
        
        return AITagResponse(
            style=data['style'],
            pattern=data['pattern'],
            material=data['material'],
            fit=data['fit'],
            occasion=data['occasion'],
            season=data['season'],
            color_analysis={
                'primary_color': color,
                'secondary_colors': [],
                'color_harmony': 'monochromatic'
            },
            confidence=0.85,
            attributes={
                'mock_analysis': True,
                'analyzed_at': datetime.now().isoformat()
            }
        )
    
    async def health_check(self) -> bool:
        """Mock health check - always returns True."""
        return True
