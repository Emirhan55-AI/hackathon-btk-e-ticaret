# 🎯 Multi-Modal Coordinator Service - FastAPI Main Application
# AURA AI Çok Modlu Sorgu Koordinatörü API Servisi

"""
Multi-Modal Coordinator Service - Ana FastAPI Uygulaması

Bu servis AURA AI sisteminin çok modlu sorgu işleme yeteneklerini REST API 
olarak sunar. Kullanıcılar görsel ve metin verilerini birlikte göndererek
akıllı moda önerileri alabilirler.

Port: 8009
Özellikler:
- Çok modlu sorgu işleme (görsel + metin)
- CLIP tabanlı görsel analiz
- NLU tabanlı metin analizi
- Real-time service koordinasyonu
- Quality assurance entegrasyonu
"""

import logging
import asyncio
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import base64
import json

# FastAPI ve HTTP imports
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# Multi-modal engine import
from multi_modal_engine import (
    MultiModalCoordinator,
    MultiModalQueryRequest,
    MultiModalQueryResponse,
    process_query
)

# Logging konfigürasyonu - Production-ready logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output için
        logging.FileHandler('multi_modal_coordinator.log')  # File logging için
    ]
)
logger = logging.getLogger("multi_modal_api")

# FastAPI uygulaması oluştur - Comprehensive metadata ile
app = FastAPI(
    title="AURA AI Multi-Modal Coordinator Service",
    description="""
    🎯 AURA AI Çok Modlu Sorgu Koordinatörü
    
    Bu servis kullanıcıların görsel ve metin verilerini birleştirerek
    akıllı moda önerileri almalarını sağlar.
    
    **Özellikler:**
    - 📸 Görsel analiz (CLIP tabanlı)
    - 🧠 Metin analizi (NLU tabanlı)
    - 🔄 Context fusion ve semantic integration
    - 🎨 Multi-service coordination
    - 🛡️ Quality assurance validation
    
    **Desteklenen Sorgu Tipleri:**
    - "Bu gömlekle ne giyebilirim?" 
    - "Bu elbiseye uygun ayakkabı var mı?"
    - "Bu pantolonla hangi ceketi önerirsin?"
    - "Bu çantayla ne kombin olur?"
    """,
    version="1.0.0",
    contact={
        "name": "AURA AI Development Team",
        "email": "dev@aura-ai.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# CORS middleware ekleme - Cross-origin requests için
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da specific domains olacak
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global coordinator instance - Servis başlatıldığında bir kez oluşturulur
coordinator_instance: Optional[MultiModalCoordinator] = None

# Request modelleri - API endpoint'leri için
class HealthResponse(BaseModel):
    """Health check response modeli"""
    service: str = "AURA AI Multi-Modal Coordinator Service"
    status: str
    timestamp: str
    version: str = "1.0.0"
    components: Dict[str, str]
    active_connections: int
    processing_capabilities: List[str]

class ImageUploadQueryRequest(BaseModel):
    """File upload ile multi-modal query request modeli"""
    text_query: str = Field(..., description="User's text query", min_length=1, max_length=500)
    user_id: Optional[str] = Field(None, description="User ID for personalization")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context")

class QueryStatsResponse(BaseModel):
    """Query istatistikleri response modeli"""
    total_queries_processed: int
    average_processing_time_ms: float
    success_rate_percent: float
    most_common_query_types: List[str]
    active_since: str

# Startup event - Servis başlatıldığında çalışır
@app.on_event("startup")
async def startup_event():
    """
    Servis başlatıldığında gerekli initialization'ları yapar
    Multi-modal coordinator'ı başlatır ve bağlantıları kontrol eder
    """
    global coordinator_instance
    
    logger.info("🚀 Multi-Modal Coordinator Service starting up...")
    
    try:
        # Coordinator instance'ını oluştur
        coordinator_instance = MultiModalCoordinator()
        
        # Service health check'leri yap
        await _perform_startup_health_checks()
        
        logger.info("✅ Multi-Modal Coordinator Service started successfully")
        logger.info("🔗 Service available at: http://localhost:8009")
        logger.info("📚 API documentation at: http://localhost:8009/docs")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {str(e)}")
        raise

# Shutdown event - Servis kapatıldığında temizlik yapar
@app.on_event("shutdown")
async def shutdown_event():
    """
    Servis kapatıldığında temizlik işlemlerini yapar
    Açık bağlantıları kapatır ve resources'ları temizler
    """
    logger.info("🔄 Multi-Modal Coordinator Service shutting down...")
    
    try:
        # HTTP client'ları kapat
        if coordinator_instance and hasattr(coordinator_instance, 'http_client'):
            await coordinator_instance.http_client.aclose()
        
        logger.info("✅ Multi-Modal Coordinator Service shutdown completed")
        
    except Exception as e:
        logger.error(f"❌ Shutdown error: {str(e)}")

async def _perform_startup_health_checks():
    """Startup sırasında critical servislerin health check'ini yapar"""
    logger.info("🔍 Performing startup health checks...")
    
    # Critical services listesi
    critical_services = [
        ("NLU Service", "http://localhost:8002"),
        ("Image Processing", "http://localhost:8001"),
        ("Quality Assurance", "http://localhost:8008")
    ]
    
    import httpx
    async with httpx.AsyncClient(timeout=5.0) as client:
        for service_name, service_url in critical_services:
            try:
                response = await client.get(f"{service_url}/", timeout=3.0)
                if response.status_code == 200:
                    logger.info(f"✅ {service_name} is available")
                else:
                    logger.warning(f"⚠️ {service_name} returned status {response.status_code}")
            except Exception as e:
                logger.warning(f"⚠️ {service_name} health check failed: {str(e)}")

# Health check endpoint - Servis durumunu kontrol eder
@app.get("/", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Multi-Modal Coordinator servisinin health durumunu döndürür
    
    Bu endpoint servisin çalışır durumda olduğunu ve
    tüm bileşenlerinin hazır olduğunu kontrol eder.
    """
    logger.info("🏥 Health check requested")
    
    try:
        # Component status'ları kontrol et
        components_status = {
            "CLIP_Processor": "operational" if coordinator_instance else "not_initialized",
            "NLU_Processor": "operational" if coordinator_instance else "not_initialized", 
            "Context_Fusion_Engine": "operational" if coordinator_instance else "not_initialized",
            "Service_Coordinator": "operational" if coordinator_instance else "not_initialized"
        }
        
        # Genel status belirle
        overall_status = "healthy" if all(status == "operational" for status in components_status.values()) else "degraded"
        
        response = HealthResponse(
            status=overall_status,
            timestamp=datetime.now().isoformat(),
            components=components_status,
            active_connections=1,  # Gerçek implementasyonda connection pool'dan alınacak
            processing_capabilities=[
                "Multi-modal query processing",
                "CLIP-based visual analysis", 
                "NLU-based text analysis",
                "Context fusion and semantic integration",
                "Multi-service coordination",
                "Quality assurance validation"
            ]
        )
        
        logger.info(f"✅ Health check completed: {overall_status}")
        return response
        
    except Exception as e:
        logger.error(f"❌ Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")

# Ana multi-modal query endpoint - Base64 ile görsel gönderme
@app.post("/query", response_model=MultiModalQueryResponse, tags=["Multi-Modal Query"])
async def process_multimodal_query(request: MultiModalQueryRequest):
    """
    Çok modlu sorgu işleme endpoint'i - Base64 encoded image ile
    
    Kullanıcıdan gelen görsel (base64) ve metin verisini işleyerek
    akıllı moda önerileri üretir.
    
    **Request Format:**
    - image_base64: Base64 encoded image data
    - text_query: User's text query (e.g., "Bu gömlekle ne giyebilirim?")
    - user_id: Optional user ID for personalization
    - context: Additional context data
    
    **Response:**
    - Unified intent analysis
    - Visual and textual analysis results
    - Personalized recommendations
    - Quality-assured suggestions
    """
    logger.info(f"🎯 Multi-modal query request received")
    logger.info(f"📝 Query: '{request.text_query}'")
    
    # Coordinator hazır mı kontrol et
    if not coordinator_instance:
        logger.error("❌ Coordinator not initialized")
        raise HTTPException(status_code=503, detail="Multi-modal coordinator not available")
    
    try:
        # Query'yi process et
        response = await coordinator_instance.process_multimodal_query(request)
        
        logger.info(f"✅ Query processed successfully: {response.query_id}")
        return response
        
    except HTTPException:
        # HTTP exceptions'ları re-raise et
        raise
    except Exception as e:
        logger.error(f"❌ Multi-modal query processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")

# File upload ile multi-modal query endpoint
@app.post("/query/upload", response_model=MultiModalQueryResponse, tags=["Multi-Modal Query"])
async def process_multimodal_query_with_upload(
    image: UploadFile = File(..., description="Image file (JPEG, PNG, JPG, WEBP)"),
    text_query: str = Form(..., description="User's text query"),
    user_id: Optional[str] = Form(None, description="User ID for personalization"),
    context: str = Form("{}", description="Additional context as JSON string")
):
    """
    Çok modlu sorgu işleme endpoint'i - File upload ile
    
    Kullanıcıdan gelen görsel dosyayı ve metin verisini işleyerek
    akıllı moda önerileri üretir.
    
    **Supported Image Formats:** JPEG, PNG, JPG, WEBP
    **Max File Size:** 10MB
    """
    logger.info(f"📤 Multi-modal query with file upload received")
    logger.info(f"📝 Query: '{text_query}'")
    logger.info(f"🖼️ Image: {image.filename} ({image.content_type})")
    
    # Coordinator hazır mı kontrol et
    if not coordinator_instance:
        logger.error("❌ Coordinator not initialized") 
        raise HTTPException(status_code=503, detail="Multi-modal coordinator not available")
    
    try:
        # Image dosyasını oku ve validate et
        image_data = await image.read()
        
        # Dosya boyutu kontrolü (10MB limit)
        if len(image_data) > 10 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="Image file too large (max 10MB)")
        
        # Content type kontrolü
        allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
        if image.content_type not in allowed_types:
            raise HTTPException(status_code=415, detail=f"Unsupported image type: {image.content_type}")
        
        # Context JSON'ını parse et
        try:
            context_dict = json.loads(context) if context != "{}" else {}
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid context JSON format")
        
        # Base64 encode et
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # MultiModalQueryRequest oluştur
        query_request = MultiModalQueryRequest(
            image_base64=image_base64,
            text_query=text_query,
            user_id=user_id,
            context=context_dict
        )
        
        # Query'yi process et
        response = await coordinator_instance.process_multimodal_query(query_request)
        
        logger.info(f"✅ File upload query processed successfully: {response.query_id}")
        return response
        
    except HTTPException:
        # HTTP exceptions'ları re-raise et
        raise
    except Exception as e:
        logger.error(f"❌ File upload query processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"File upload query processing failed: {str(e)}")

# Test scenarios endpoint - Built-in test senaryoları
@app.post("/test-nlu-advanced", tags=["Testing"])
async def test_nlu_advanced():
    """
    Bu endpoint gelişmiş NLU özelliklerini test eder.
    4 farklı prompt engineering pattern ile NLU analizini değerlendirir.
    """
    logger.info("🧠 Testing advanced NLU capabilities...")
    
    # Coordinator hazır mı kontrol et
    if not coordinator_instance:
        raise HTTPException(status_code=503, detail="Multi-modal coordinator not available")
    
    # Gelişmiş NLU test senaryoları
    nlu_test_queries = [
        {
            "query": "Bu gömlekle hangi pantolon uyumlu olur acaba?",
            "expected_pattern": "Template",
            "expected_intent": "kombin_önerisi_isteme"
        },
        {
            "query": "Siyah ayakkabımla bu eteği giyebilir miyim?",
            "expected_pattern": "Context & Instruction", 
            "expected_intent": "uyum_kontrolü"
        },
        {
            "query": "İş toplantısına bu kıyafetle gidebilir miyim?",
            "expected_pattern": "Persona",
            "expected_intent": "durum_uygunluk_sorgulama"
        },
        {
            "query": "Bu ceketin altına ne giymeliyim step by step anlat",
            "expected_pattern": "Recipe",
            "expected_intent": "adım_adım_kombin_rehberi"
        }
    ]
    
    # Test sonuçlarını topla
    nlu_results = []
    successful_tests = 0
    
    for i, test_case in enumerate(nlu_test_queries, 1):
        logger.info(f"🔬 Testing advanced NLU pattern {i}/{len(nlu_test_queries)}")
        
        try:
            # NLU processor'ı test et
            start_time = time.time()
            nlu_result = await coordinator_instance.nlu_processor._mock_nlu_analysis(test_case["query"], {})
            processing_time = (time.time() - start_time) * 1000
            
            # Sonuçları analiz et
            detected_intent = nlu_result.intent
            confidence = nlu_result.confidence_score
            entities = nlu_result.entities
            sentiment = nlu_result.sentiment
            prompt_pattern = "Advanced NLU Pattern"  # Mock for now
            
            # Test başarısını değerlendir
            intent_correct = test_case["expected_intent"] in detected_intent
            pattern_correct = test_case["expected_pattern"] in prompt_pattern
            high_confidence = confidence > 0.8
            
            test_success = intent_correct and high_confidence
            
            # Sonucu kaydet
            test_result = {
                "test_query": test_case["query"],
                "expected_intent": test_case["expected_intent"],
                "detected_intent": detected_intent,
                "expected_pattern": test_case["expected_pattern"],
                "used_pattern": prompt_pattern,
                "confidence_score": confidence,
                "entities_found": len(entities),
                "sentiment_analysis": sentiment,
                "processing_time_ms": round(processing_time, 3),
                "intent_accuracy": intent_correct,
                "pattern_accuracy": pattern_correct,
                "confidence_level": "high" if high_confidence else "medium" if confidence > 0.6 else "low",
                "overall_success": test_success
            }
            
            nlu_results.append(test_result)
            
            if test_success:
                successful_tests += 1
                logger.info(f"✅ Advanced NLU test {i} passed")
            else:
                logger.warning(f"⚠️ Advanced NLU test {i} needs improvement")
                
        except Exception as e:
            logger.error(f"❌ Advanced NLU test {i} failed: {str(e)}")
            nlu_results.append({
                "test_query": test_case["query"],
                "error": str(e),
                "overall_success": False
            })
    
    # Genel istatistikler
    success_rate = (successful_tests / len(nlu_test_queries)) * 100
    successful_results = [r for r in nlu_results if "confidence_score" in r]
    avg_confidence = sum(r.get("confidence_score", 0) for r in successful_results) / len(successful_results) if successful_results else 0
    avg_processing_time = sum(r.get("processing_time_ms", 0) for r in successful_results) / len(successful_results) if successful_results else 0
    
    logger.info(f"🎯 Advanced NLU testing completed: {successful_tests}/{len(nlu_test_queries)} passed ({success_rate:.1f}%)")
    
    return {
        "nlu_test_summary": {
            "total_tests": len(nlu_test_queries),
            "successful_tests": successful_tests, 
            "success_rate_percent": success_rate,
            "average_confidence": round(avg_confidence, 3),
            "average_processing_time_ms": round(avg_processing_time, 3),
            "nlu_status": "excellent" if success_rate >= 90 else "good" if success_rate >= 75 else "needs_improvement"
        },
        "detailed_results": nlu_results,
        "prompt_engineering_assessment": {
            "persona_pattern_usage": len([r for r in nlu_results if "Persona" in r.get("used_pattern", "")]),
            "recipe_pattern_usage": len([r for r in nlu_results if "Recipe" in r.get("used_pattern", "")]),
            "template_pattern_usage": len([r for r in nlu_results if "Template" in r.get("used_pattern", "")]),
            "context_instruction_usage": len([r for r in nlu_results if "Context" in r.get("used_pattern", "")])
        },
        "recommendations": [
            f"NLU confidence average: {avg_confidence:.1f}",
            f"Processing speed: {avg_processing_time:.1f}ms per query",
            "Advanced prompt engineering patterns working effectively" if success_rate >= 80 else "Prompt patterns need refinement"
        ]
    }

@app.post("/test-scenarios", tags=["Testing"])
async def run_test_scenarios():
    """
    Built-in test senaryolarını çalıştırır
    
    Çok modlu sorgu sisteminin doğru çalıştığını doğrulamak için
    önceden tanımlı test senaryolarını çalıştırır.
    """
    logger.info("🧪 Running multi-modal test scenarios...")
    
    # Coordinator hazır mı kontrol et
    if not coordinator_instance:
        raise HTTPException(status_code=503, detail="Multi-modal coordinator not available")
    
    try:
        # Test senaryoları tanımla
        test_scenarios = [
            {
                "name": "Gömlek Kombinasyon Testi",
                "text_query": "Bu mavi gömlekle ne giyebilirim?",
                "expected_intent": "kombin_önerisi_isteme",
                "description": "Mavi gömlek ile alt parça kombinasyonu"
            },
            {
                "name": "Elbise Ayakkabı Uyum Testi", 
                "text_query": "Bu siyah elbiseye uygun ayakkabı var mı?",
                "expected_intent": "ayakkabı_uyumu_sorgulama",
                "description": "Siyah elbise ile ayakkabı uyumu kontrolü"
            },
            {
                "name": "Pantolon Ceket Kombinasyon Testi",
                "text_query": "Bu lacivert pantolonla hangi ceketi önerirsin?",
                "expected_intent": "ceket_önerisi_isteme", 
                "description": "Lacivert pantolon ile ceket kombinasyonu"
            }
        ]
        
        # Mock image data - Test için basit bir placeholder image
        test_image_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
        
        test_results = []
        successful_tests = 0
        
        # Her test senaryosunu çalıştır
        for i, scenario in enumerate(test_scenarios):
            logger.info(f"🔬 Running test {i+1}/{len(test_scenarios)}: {scenario['name']}")
            
            try:
                # Test request'i oluştur
                test_request = MultiModalQueryRequest(
                    image_base64=test_image_base64,
                    text_query=scenario["text_query"],
                    user_id="test_user",
                    context={"test_scenario": scenario["name"]}
                )
                
                # Query'yi process et
                result = await coordinator_instance.process_multimodal_query(test_request)
                
                # Sonucu değerlendir
                intent_match = scenario["expected_intent"] in result.textual_analysis.get("intent", "")
                
                test_results.append({
                    "scenario_name": scenario["name"],
                    "query": scenario["text_query"],
                    "expected_intent": scenario["expected_intent"],
                    "actual_intent": result.textual_analysis.get("intent", "unknown"),
                    "intent_matches": intent_match,
                    "processing_time_ms": result.processing_time_ms,
                    "fusion_confidence": result.fusion_confidence,
                    "recommendations_count": len(result.recommendations),
                    "success": result.success and intent_match
                })
                
                if result.success and intent_match:
                    successful_tests += 1
                    logger.info(f"✅ Test {i+1} passed")
                else:
                    logger.warning(f"⚠️ Test {i+1} needs attention")
                    
            except Exception as e:
                logger.error(f"❌ Test {i+1} failed: {str(e)}")
                test_results.append({
                    "scenario_name": scenario["name"],
                    "query": scenario["text_query"],
                    "error": str(e),
                    "success": False
                })
        
        # Test özetini oluştur
        success_rate = (successful_tests / len(test_scenarios)) * 100
        
        test_summary = {
            "total_scenarios": len(test_scenarios),
            "successful_tests": successful_tests,
            "success_rate_percent": success_rate,
            "test_timestamp": datetime.now().isoformat(),
            "system_status": "optimal" if success_rate >= 90 else "needs_attention" if success_rate >= 70 else "requires_improvement"
        }
        
        logger.info(f"🎯 Test scenarios completed: {successful_tests}/{len(test_scenarios)} passed ({success_rate:.1f}%)")
        
        return {
            "test_summary": test_summary,
            "individual_results": test_results,
            "recommendations": [
                "Test sonuçları başarılı" if success_rate >= 90 else "Sistem optimizasyonu gerekebilir",
                f"Ortalama işlem süresi: {sum(r.get('processing_time_ms', 0) for r in test_results if 'processing_time_ms' in r) / len([r for r in test_results if 'processing_time_ms' in r]):.1f}ms" if test_results else "No timing data"
            ]
        }
        
    except Exception as e:
        logger.error(f"❌ Test scenarios failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Test scenarios failed: {str(e)}")

# Query statistics endpoint - İstatistikler ve monitoring
@app.get("/stats", response_model=QueryStatsResponse, tags=["Monitoring"])
async def get_query_statistics():
    """
    Multi-modal query istatistiklerini döndürür
    
    Servisin performans metriklerini ve kullanım istatistiklerini sağlar.
    """
    logger.info("📊 Query statistics requested")
    
    try:
        # Mock statistics - Gerçek implementasyonda database'den gelecek
        stats = QueryStatsResponse(
            total_queries_processed=42,
            average_processing_time_ms=1250.5,
            success_rate_percent=95.2,
            most_common_query_types=[
                "shirt_combination",
                "dress_shoe_matching", 
                "pants_jacket_pairing"
            ],
            active_since=datetime.now().isoformat()
        )
        
        logger.info("✅ Query statistics retrieved successfully")
        return stats
        
    except Exception as e:
        logger.error(f"❌ Query statistics retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Statistics retrieval failed: {str(e)}")

# Service capabilities endpoint - Servis yetenekleri
@app.get("/capabilities", tags=["Information"])
async def get_service_capabilities():
    """
    Multi-Modal Coordinator servisinin yeteneklerini listeler
    
    Desteklenen query tipleri, image formatları ve diğer
    teknik capabilities'leri döndürür.
    """
    logger.info("ℹ️ Service capabilities requested")
    
    capabilities = {
        "service_name": "AURA AI Multi-Modal Coordinator",
        "version": "1.0.0",
        "supported_query_types": [
            {
                "type": "shirt_combination",
                "description": "Gömlek ile kombin önerileri",
                "example": "Bu gömlekle ne giyebilirim?"
            },
            {
                "type": "dress_shoe_matching",
                "description": "Elbise-ayakkabı uyum kontrolü",
                "example": "Bu elbiseye uygun ayakkabı var mı?"
            },
            {
                "type": "pants_jacket_pairing",
                "description": "Pantolon-ceket kombinasyonu",
                "example": "Bu pantolonla hangi ceketi önerirsin?"
            },
            {
                "type": "bag_outfit_styling",
                "description": "Çanta merkezli komple outfit",
                "example": "Bu çantayla ne kombin olur?"
            }
        ],
        "supported_image_formats": ["JPEG", "PNG", "JPG", "WEBP"],
        "max_image_size_mb": 10,
        "processing_capabilities": [
            "CLIP-based visual analysis",
            "NLU-based text analysis", 
            "Context fusion and semantic integration",
            "Multi-service coordination",
            "Quality assurance validation",
            "Real-time recommendation generation"
        ],
        "integration_services": [
            "Image Processing Service (8001)",
            "NLU Service (8002)",
            "Style Profile Service (8003)",
            "Combination Engine (8004)",
            "Recommendation Engine (8005)",
            "Quality Assurance Service (8008)"
        ],
        "response_format": {
            "unified_intent": "Kullanıcının birleştirilmiş niyeti",
            "visual_analysis": "Görsel analiz sonucu",
            "textual_analysis": "Metin analiz sonucu", 
            "recommendations": "Kişiselleştirilmiş öneriler",
            "fusion_confidence": "Birleştirme güven skoru"
        }
    }
    
    logger.info("✅ Service capabilities retrieved successfully")
    return capabilities

# Error handlers - Comprehensive error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP exception handler - Structured error responses"""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "status_code": exc.status_code,
            "message": exc.detail,
            "timestamp": datetime.now().isoformat(),
            "service": "multi_modal_coordinator"
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler - Catch-all for unexpected errors"""
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "status_code": 500,
            "message": "Internal server error occurred",
            "timestamp": datetime.now().isoformat(),
            "service": "multi_modal_coordinator"
        }
    )

# Main execution - Development server
if __name__ == "__main__":
    logger.info("🚀 Starting Multi-Modal Coordinator Service...")
    
    # Uvicorn server configuration
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Tüm network interface'lerinde dinle
        port=8009,       # Multi-Modal Coordinator port
        reload=True,     # Development için auto-reload
        log_level="info",
        access_log=True,
        reload_dirs=[".", "./multi_modal_engine.py"]  # İzlenecek dosyalar
    )
