from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging
import time

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.exceptions import (
    AuraException,
    aura_exception_handler,
    http_exception_handler,
    general_exception_handler
)
from app.core.database import init_database
# from app.core.di import setup_container

logger = logging.getLogger("app.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown."""
    # Startup
    logger.info("Starting Aura Backend API...")
    
    try:
        # Setup logging
        setup_logging()
        
        # Initialize database
        database = init_database(settings.database_url)
        await database.connect()
        
        # Setup dependency injection (disabled for now)
        # setup_container()
        
        # Check external services (AI service health check)
        await check_external_services()
        
        logger.info("Aura Backend API started successfully")
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Aura Backend API...")
    
    try:
        # Close database connection
        await database.disconnect()
        
        logger.info("Aura Backend API shutdown complete")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


async def check_external_services():
    """Check if external services are available."""
    import httpx
    
    try:
        async with httpx.AsyncClient() as client:
            # Check AI service health
            response = await client.get(
                f"{settings.ai_service_url}/health",
                timeout=5.0
            )
            if response.status_code == 200:
                logger.info("AI service is available")
            else:
                logger.warning(f"AI service health check failed: {response.status_code}")
                
    except Exception as e:
        logger.warning(f"Could not reach AI service: {e}")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="AI-powered Personal Style Assistant Backend API",
    version=settings.app_version,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware (security)
if not settings.debug:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0"]
    )

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request, call_next):
    """Add request processing time to response headers."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log request details
    logger.info(
        f"{request.method} {request.url.path}",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "process_time": process_time,
            "client_ip": request.client.host if request.client else None
        }
    )
    
    return response

# Exception handlers
app.add_exception_handler(AuraException, aura_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version
    }

# API Routes
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Aura Backend API",
        "docs": "/docs",
        "health": "/health"
    }

# Include feature routers
from app.features.auth.presentation.routers_simple import router as auth_router
from app.features.wardrobe.presentation.routers import router as wardrobe_router
from app.features.style_quiz.presentation.routers import router as style_quiz_router
from app.features.recommendations.presentation.routers import router as recommendations_router
from app.features.ecommerce.presentation.routers import router as ecommerce_router

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(wardrobe_router, prefix="/api/v1", tags=["Wardrobe"])
app.include_router(style_quiz_router, prefix="/api/v1/style-quiz", tags=["Style Quiz"])
app.include_router(recommendations_router, prefix="/api/v1/recommendations", tags=["Recommendations"])
app.include_router(ecommerce_router, prefix="/api/v1", tags=["E-commerce"])
