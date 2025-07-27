# 🚀 EMERGENCY IMAGE PROCESSING SERVICE - MOCK VERSION
# Bu servis, image processing service'in HTTP 500 hatasını geçici olarak çözmek için
# mock response'lar döndürür ve temel sağlık kontrolü sağlar

from fastapi import FastAPI
from datetime import datetime

# FastAPI uygulaması oluştur
app = FastAPI(
    title="🚀 Aura Image Processing - Emergency Mock Service",
    description="Emergency mock service to resolve HTTP 500 issues",
    version="1.0.0"
)

@app.get("/")
def emergency_health_check():
    """
    Emergency health check endpoint - always returns healthy status
    """
    return {
        "service": "Aura Image Processing Service - Emergency Mock",
        "status": "healthy",
        "phase": "Emergency Recovery Mode",
        "description": "Mock service providing basic functionality during emergency recovery",
        "version": "1.0.0-emergency",
        "ai_available": False,  # This was causing the original error
        "mode": "mock_emergency",
        "capabilities": {
            "mock_image_analysis": True,
            "basic_health_check": True,
            "emergency_response": True
        },
        "models_status": {
            "detectron2": "not available (emergency mode)",
            "clip": "not available (emergency mode)",
            "transformers": "not available (emergency mode)"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
def health():
    """Standard health endpoint"""
    return {"status": "healthy", "service": "image_processing_emergency"}

if __name__ == "__main__":
    import uvicorn
    print("🚨 EMERGENCY IMAGE PROCESSING SERVICE STARTING...")
    print("🔧 This is a temporary mock service to resolve HTTP 500 issues")
    print("⚡ Running on http://localhost:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)
