import os
from typing import Dict, Any

from app.features.wardrobe.infrastructure.ai_service import AIServiceClient, MockAIServiceClient
from app.core.config import settings


class AIServiceFactory:
    """Factory for creating AI service clients."""
    
    @staticmethod
    def create_ai_service() -> AIServiceClient:
        """Create appropriate AI service client based on environment."""
        if settings.environment == "development" or not settings.ai_service_url:
            # Use mock service in development or when AI service is not configured
            import httpx
            http_client = httpx.AsyncClient()
            return MockAIServiceClient(http_client)
        else:
            # Use real AI service in production
            import httpx
            http_client = httpx.AsyncClient()
            return AIServiceClient(http_client)


# Global AI service instance
_ai_service: AIServiceClient = None


async def get_ai_service() -> AIServiceClient:
    """Dependency injection for AI service."""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIServiceFactory.create_ai_service()
    return _ai_service
