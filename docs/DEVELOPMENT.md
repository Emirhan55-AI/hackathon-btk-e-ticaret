# 🛠️ AURA AI - Geliştirici Kılavuzu

## 🎯 Giriş

Bu kılavuz, AURA AI Personal Style Assistant sisteminde geliştirme yapmak isteyen geliştiriciler için hazırlanmıştır. Mikroservis mimarisi, kod standartları, test stratejileri ve best practice'ler hakkında detaylı bilgi içerir.

## 📋 İçindekiler

1. [Geliştirme Ortamı Kurulumu](#geliştirme-ortamı-kurulumu)
2. [Mikroservis Geliştirme](#mikroservis-geliştirme)
3. [Kod Standartları](#kod-standartları)
4. [Test Stratejileri](#test-stratejileri)
5. [AI Model Entegrasyonu](#ai-model-entegrasyonu)
6. [Debugging ve Monitoring](#debugging-ve-monitoring)
7. [Performance Optimization](#performance-optimization)
8. [Security Best Practices](#security-best-practices)

---

## 🔧 Geliştirme Ortamı Kurulumu

### Önkoşullar

```bash
# Python 3.9+ gerekli
python --version
# Python 3.9.0 veya üzeri olmalı

# Docker ve Docker Compose
docker --version
docker-compose --version

# Git
git --version
```

### 1. Repository Klonlama

```powershell
# Repository'yi klonla
git clone https://github.com/your-org/aura-ai.git
cd aura-ai

# Development branch'ine geç
git checkout develop
```

### 2. Virtual Environment Kurulumu

```powershell
# Python virtual environment oluştur
python -m venv venv

# Virtual environment'ı aktifleştir (Windows)
.\venv\Scripts\Activate.ps1

# Virtual environment'ı aktifleştir (Linux/Mac)
# source venv/bin/activate

# Dependencies yükle
pip install -r requirements-dev.txt
```

### 3. Environment Dosyaları

```powershell
# Environment dosyalarını oluştur
Copy-Item .env.example .env
Copy-Item .env.test.example .env.test

# .env dosyasını düzenle
# Notepad veya preferred editor ile açın
notepad .env
```

#### .env Dosyası Örneği:

```env
# Database
DATABASE_URL=postgresql://aura_user:aura_pass@localhost:5432/aura_ai
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET_KEY=your-super-secret-jwt-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=24

# AI Models
OPENAI_API_KEY=your-openai-api-key
HUGGINGFACE_API_KEY=your-huggingface-key

# Services
IMAGE_SERVICE_URL=http://localhost:8001
NLU_SERVICE_URL=http://localhost:8002
STYLE_PROFILE_URL=http://localhost:8003
COMBINATION_ENGINE_URL=http://localhost:8004
RECOMMENDATION_ENGINE_URL=http://localhost:8005
FEEDBACK_LOOP_URL=http://localhost:8006

# Monitoring
ENABLE_METRICS=true
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000

# Development
DEBUG=true
LOG_LEVEL=DEBUG
DEVELOPMENT_MODE=true
```

### 4. Veritabanı Kurulumu

```powershell
# PostgreSQL Docker container başlat
docker run -d `
  --name aura-postgres `
  -e POSTGRES_DB=aura_ai `
  -e POSTGRES_USER=aura_user `
  -e POSTGRES_PASSWORD=aura_pass `
  -p 5432:5432 `
  postgres:14

# Redis Docker container başlat
docker run -d `
  --name aura-redis `
  -p 6379:6379 `
  redis:7-alpine

# Database migration çalıştır
python -m alembic upgrade head
```

### 5. Pre-commit Hooks Kurulumu

```powershell
# Pre-commit yükle
pip install pre-commit

# Hooks'ları kur
pre-commit install

# İlk çalıştırma
pre-commit run --all-files
```

---

## 🏗️ Mikroservis Geliştirme

### Yeni Mikroservis Oluşturma

#### 1. Servis Dizini Yapısı

```
services/
└── yeni_servis/
    ├── __init__.py
    ├── main.py                 # FastAPI app entry point
    ├── config.py               # Configuration management
    ├── models/
    │   ├── __init__.py
    │   ├── database.py         # Database models (SQLAlchemy)
    │   └── schemas.py          # Pydantic models
    ├── routes/
    │   ├── __init__.py
    │   ├── health.py           # Health check endpoints
    │   └── api.py              # Main API endpoints
    ├── services/
    │   ├── __init__.py
    │   └── business_logic.py   # Business logic implementation
    ├── utils/
    │   ├── __init__.py
    │   ├── logging.py          # Logging utilities
    │   └── helpers.py          # Helper functions
    ├── tests/
    │   ├── __init__.py
    │   ├── conftest.py         # Test configuration
    │   ├── test_routes.py      # Route tests
    │   └── test_services.py    # Service logic tests
    ├── Dockerfile              # Container definition
    ├── requirements.txt        # Service dependencies
    └── README.md              # Service documentation
```

#### 2. FastAPI Servis Template

```python
# services/yeni_servis/main.py

"""
AURA AI - Yeni Mikroservis
Bu dosya FastAPI uygulamasının ana giriş noktasıdır.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn
import time
import logging

# Servis modüllerini import et
from .config import settings
from .routes import health, api
from .utils.logging import setup_logging

# Logging sistemini kur
setup_logging()
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """
    FastAPI uygulamasını oluştur ve yapılandır.
    Bu fonksiyon tüm middleware'leri, route'ları ve
    konfigürasyonları uygulama nesnesine ekler.
    
    Returns:
        FastAPI: Yapılandırılmış FastAPI uygulama nesnesi
    """
    
    # FastAPI uygulaması oluştur
    # title: API dokümantasyonunda görünecek başlık
    # description: API'nin ne yaptığını açıklayan metin
    # version: Servis versiyonu (semantic versioning)
    app = FastAPI(
        title="AURA AI - Yeni Mikroservis",
        description="Personal Style Assistant AI System - Yeni Servis Modülü",
        version="1.0.0",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None
    )
    
    # CORS middleware ekle
    # Bu middleware, farklı domain'lerden gelen istekleri kabul etmek için gerekli
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,  # İzin verilen origin'ler
        allow_credentials=True,                   # Cookie ve auth header'lara izin
        allow_methods=["*"],                      # Tüm HTTP methodlarına izin
        allow_headers=["*"],                      # Tüm header'lara izin
    )
    
    # Trusted host middleware ekle
    # Bu middleware, güvenilir host'lardan gelen istekleri kontrol eder
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )
    
    # Request timing middleware
    # Her request'in ne kadar sürdüğünü loglamak için custom middleware
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        """
        HTTP request'lerinin işlem süresini ölç ve header'a ekle.
        Bu middleware her request için çalışır ve processing time'ı hesaplar.
        """
        start_time = time.time()  # İşlem başlangıç zamanını kaydet
        response = await call_next(request)  # Request'i işle
        process_time = time.time() - start_time  # İşlem süresini hesapla
        
        # Response header'ına processing time ekle
        response.headers["X-Process-Time"] = str(process_time)
        
        # Loglama için request bilgilerini kaydet
        logger.info(
            f"Request: {request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.4f}s"
        )
        
        return response
    
    # Route'ları uygulamaya ekle
    # Health check endpoint'leri (sistem durumu kontrolü)
    app.include_router(
        health.router,
        prefix="/health",
        tags=["Health Check"]
    )
    
    # Ana API endpoint'leri (servisin temel işlevselliği)
    app.include_router(
        api.router,
        prefix="/api/v1",
        tags=["API"]
    )
    
    return app

# FastAPI uygulaması instance'ını oluştur
app = create_app()

# Startup event handler
@app.on_event("startup")
async def startup_event():
    """
    Uygulama başlatıldığında çalışacak kodlar.
    Database bağlantısı, cache initialization, vb.
    """
    logger.info("🚀 Yeni Mikroservis başlatılıyor...")
    
    # Database bağlantısını test et
    # Bu kısımda database connection pool oluşturulabilir
    
    # Cache sistemini başlat
    # Redis veya in-memory cache initialize edilebilir
    
    # ML modellerini yükle
    # AI modelleri burada memory'e yüklenebilir
    
    logger.info("✅ Yeni Mikroservis başarıyla başlatıldı!")

# Shutdown event handler  
@app.on_event("shutdown")
async def shutdown_event():
    """
    Uygulama kapatıldığında çalışacak kodlar.
    Database connections, cache cleanup, vb.
    """
    logger.info("🔄 Yeni Mikroservis kapatılıyor...")
    
    # Database bağlantılarını kapat
    # Connection pool'ları temizle
    
    # Cache'i temizle
    # Memory'deki geçici verileri temizle
    
    # Logları flush et
    # Pending log entries'leri kaydet
    
    logger.info("✅ Yeni Mikroservis başarıyla kapatıldı!")

# Development server çalıştırma fonksiyonu
if __name__ == "__main__":
    """
    Bu blok sadece dosya direkt çalıştırıldığında (development) çalışır.
    Production'da genelde Gunicorn veya Uvicorn ile çalıştırılır.
    """
    uvicorn.run(
        "main:app",                    # Uygulama modülü ve instance
        host="0.0.0.0",               # Tüm interface'lerde dinle
        port=8000,                     # Port numarası (servis bazlı değişir)
        reload=True,                   # Kod değişikliklerinde otomatik restart
        log_level="debug" if settings.DEBUG else "info"  # Log seviyesi
    )
```

#### 3. Configuration Management

```python
# services/yeni_servis/config.py

"""
AURA AI Yeni Mikroservis - Konfigürasyon Yönetimi
Bu modül servisin tüm konfigürasyon ayarlarını merkezi olarak yönetir.
Environment variables, default değerler ve validation'lar burada tanımlanır.
"""

from pydantic import BaseSettings, validator
from typing import List, Optional
import os
from functools import lru_cache

class Settings(BaseSettings):
    """
    Pydantic BaseSettings kullanarak environment variable'ları yönet.
    Bu class environment'tan gelen değerleri otomatik olarak parse eder
    ve type safety sağlar.
    """
    
    # Servis temel ayarları
    SERVICE_NAME: str = "yeni-mikroservis"
    SERVICE_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"  # development, staging, production
    
    # Server ayarları
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    
    # Database ayarları
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/aura_ai"
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    
    # Redis/Cache ayarları
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 3600  # Cache timeout in seconds
    
    # Security ayarları
    SECRET_KEY: str = "super-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 24
    
    # CORS ayarları
    ALLOWED_ORIGINS: List[str] = ["*"]
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # API ayarları
    API_PREFIX: str = "/api/v1"
    MAX_REQUEST_SIZE: int = 50 * 1024 * 1024  # 50MB
    REQUEST_TIMEOUT: int = 30  # seconds
    
    # Logging ayarları
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json veya standard
    
    # Monitoring ayarları
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    HEALTH_CHECK_INTERVAL: int = 30  # seconds
    
    # AI Model ayarları
    MODEL_PATH: str = "./models"
    MODEL_CACHE_SIZE: int = 100
    ENABLE_GPU: bool = False
    
    # External service URL'leri
    IMAGE_SERVICE_URL: str = "http://localhost:8001"
    NLU_SERVICE_URL: str = "http://localhost:8002"
    STYLE_PROFILE_URL: str = "http://localhost:8003"
    
    # Rate limiting ayarları
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # File upload ayarları
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = [".jpg", ".jpeg", ".png", ".gif"]
    
    @validator("DEBUG", pre=True)
    def parse_debug(cls, v):
        """
        DEBUG environment variable'ını boolean'a çevir.
        String değerler: 'true', '1', 'yes', 'on' -> True
        Diğer değerler -> False
        """
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'on')
        return bool(v)
    
    @validator("DATABASE_URL")
    def validate_database_url(cls, v):
        """
        Database URL formatını kontrol et.
        PostgreSQL URL formatı: postgresql://user:pass@host:port/db
        """
        if not v.startswith(('postgresql://', 'postgres://')):
            raise ValueError('Database URL must start with postgresql:// or postgres://')
        return v
    
    @validator("ALLOWED_ORIGINS")
    def validate_cors_origins(cls, v):
        """
        CORS origins listesini validate et.
        Development'ta "*" allowed, production'da specific domains olmalı.
        """
        if isinstance(v, str):
            # String gelirse comma-separated parse et
            return [origin.strip() for origin in v.split(',')]
        return v
    
    @validator("LOG_LEVEL")
    def validate_log_level(cls, v):
        """
        Log level'inin geçerli değerlerden biri olduğunu kontrol et.
        """
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'Log level must be one of: {valid_levels}')
        return v.upper()
    
    @validator("ENVIRONMENT")
    def validate_environment(cls, v):
        """
        Environment'ın geçerli değerlerden biri olduğunu kontrol et.
        """
        valid_envs = ['development', 'staging', 'production']
        if v.lower() not in valid_envs:
            raise ValueError(f'Environment must be one of: {valid_envs}')
        return v.lower()
    
    class Config:
        """
        Pydantic configuration.
        Environment file'dan değerleri okumak için ayarlar.
        """
        env_file = ".env"  # Environment dosyası adı
        env_file_encoding = 'utf-8'  # Dosya encoding
        case_sensitive = True  # Environment variable'lar case sensitive

    def is_development(self) -> bool:
        """Development environment olup olmadığını kontrol et."""
        return self.ENVIRONMENT == "development"
    
    def is_production(self) -> bool:
        """Production environment olup olmadığını kontrol et."""
        return self.ENVIRONMENT == "production"
    
    def get_database_config(self) -> dict:
        """Database konfigürasyon dictionary'si döndür."""
        return {
            "url": self.DATABASE_URL,
            "pool_size": self.DATABASE_POOL_SIZE,
            "max_overflow": self.DATABASE_MAX_OVERFLOW,
            "pool_pre_ping": True,
            "pool_recycle": 3600
        }
    
    def get_cors_config(self) -> dict:
        """CORS konfigürasyon dictionary'si döndür."""
        return {
            "allow_origins": self.ALLOWED_ORIGINS,
            "allow_credentials": True,
            "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["*"]
        }

@lru_cache()
def get_settings() -> Settings:
    """
    Settings singleton instance döndür.
    lru_cache decorator sayesinde tek instance oluşturulur
    ve her çağrıda aynı instance döndürülür.
    
    Returns:
        Settings: Konfigürasyon ayarları instance'ı
    """
    return Settings()

# Global settings instance
# Bu instance tüm modüllerde import edilerek kullanılabilir
settings = get_settings()

# Development ayarları için shortcut fonksiyonlar
def is_development() -> bool:
    """Development mode olup olmadığını kontrol et."""
    return settings.is_development()

def is_production() -> bool:
    """Production mode olup olmadığını kontrol et."""
    return settings.is_production()

# Database URL parsing için utility fonksiyon
def parse_database_url(url: str) -> dict:
    """
    Database URL'sini parse ederek connection parametrelerini çıkar.
    
    Args:
        url: Database connection URL
        
    Returns:
        dict: Connection parametreleri (host, port, user, password, database)
    """
    from urllib.parse import urlparse
    
    parsed = urlparse(url)
    
    return {
        "host": parsed.hostname,
        "port": parsed.port or 5432,
        "user": parsed.username,
        "password": parsed.password,
        "database": parsed.path.lstrip('/') if parsed.path else None
    }
```

---

## 📏 Kod Standartları

### Python Kod Standartları

#### 1. Dosya Header Template

```python
"""
AURA AI Personal Style Assistant System
[Servis Adı] - [Modül Açıklaması]

Bu modül [modülün ne yaptığını açıkla].
[Varsa özel notlar, usage examples, vs.]

Author: [Your Name]
Created: [Date]
Version: 1.0.0
"""

import os
import sys
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta

# Third-party imports
import requests
import numpy as np
from fastapi import FastAPI, HTTPException, Depends

# Local imports  
from .config import settings
from .models import schemas
from .utils import logging
```

#### 2. Fonksiyon Dokümantasyonu

```python
def analyze_clothing_style(
    image_data: bytes,
    user_preferences: Optional[Dict[str, Any]] = None,
    confidence_threshold: float = 0.8
) -> Dict[str, Any]:
    """
    Kıyafet görüntüsünü analiz ederek stil özelliklerini çıkarır.
    
    Bu fonksiyon verilen görüntüyü AI modeli ile işleyerek:
    1. Kıyafet türünü tespit eder (gömlek, pantolon, elbise vb.)
    2. Renk paletini çıkarır 
    3. Stil kategorisini belirler (casual, formal, sporty vb.)
    4. Kullanıcı tercihlerine göre uyumluluk skorunu hesaplar
    
    Args:
        image_data (bytes): Analiz edilecek görüntünün binary datası.
                           JPEG, PNG formatları desteklenir.
        user_preferences (Optional[Dict[str, Any]]): Kullanıcının stil tercihleri.
                                                    Keys: colors, styles, brands
        confidence_threshold (float): Minimum güven skoru eşiği (0.0-1.0).
                                     Bu değerin altındaki sonuçlar filtrelenir.
    
    Returns:
        Dict[str, Any]: Analiz sonuçları dictionary'si:
            - detected_items: Tespit edilen kıyafet öğeleri listesi
            - color_palette: Dominant renkler ve yüzdeleri  
            - style_category: Ana stil kategorisi
            - confidence_score: Genel güven skoru
            - recommendations: Öneriler listesi
    
    Raises:
        ValueError: Geçersiz image data veya threshold değeri
        AIModelError: AI model inference hatası
        ProcessingError: Görüntü işleme hatası
        
    Example:
        >>> with open('shirt.jpg', 'rb') as f:
        ...     image_data = f.read()
        >>> preferences = {'colors': ['blue', 'white'], 'styles': ['casual']}
        >>> result = analyze_clothing_style(image_data, preferences, 0.85)
        >>> print(result['style_category'])
        'business_casual'
    """
    
    # Input validation - Giriş parametrelerini kontrol et
    if not image_data:
        raise ValueError("Image data boş olamaz")
    
    if not 0.0 <= confidence_threshold <= 1.0:
        raise ValueError("Confidence threshold 0.0-1.0 arasında olmalı")
        
    # Log the function call - Fonksiyon çağrısını logla
    logger.info(
        f"Clothing style analysis başlatıldı. "
        f"Image size: {len(image_data)} bytes, "
        f"Threshold: {confidence_threshold}"
    )
    
    try:
        # AI model inference - Yapay zeka modeli ile analiz
        model_results = ai_model.predict(image_data)
        
        # Post-process results - Sonuçları işle
        processed_results = _process_model_output(
            model_results, 
            confidence_threshold
        )
        
        # Apply user preferences - Kullanıcı tercihlerini uygula
        if user_preferences:
            processed_results = _apply_user_preferences(
                processed_results, 
                user_preferences
            )
            
        # Generate recommendations - Önerileri oluştur
        recommendations = _generate_style_recommendations(processed_results)
        processed_results['recommendations'] = recommendations
        
        logger.info("Clothing style analysis tamamlandı")
        return processed_results
        
    except Exception as e:
        logger.error(f"Clothing style analysis hatası: {str(e)}")
        raise ProcessingError(f"Analiz işlemi başarısız: {str(e)}") from e
```

#### 3. Class Dokümantasyonu

```python
class StyleAnalyzer:
    """
    Kıyafet stil analizi için ana class.
    
    Bu class AI modellerini yönetir ve stil analizi işlemlerini koordine eder.
    Farklı model tiplerini (CNN, Transformer) destekler ve ensemble sonuçlar üretir.
    
    Attributes:
        model_config (Dict[str, Any]): Model konfigürasyon ayarları
        confidence_threshold (float): Minimum güven skoru eşiği
        supported_formats (List[str]): Desteklenen görüntü formatları
        _models (Dict[str, Any]): Yüklenmiş AI modelleri cache'i
        _analytics (AnalyticsManager): Performans metrikleri yöneticisi
    
    Example:
        >>> analyzer = StyleAnalyzer(confidence_threshold=0.8)
        >>> analyzer.load_models()
        >>> result = analyzer.analyze(image_data)
        >>> print(f"Detected style: {result['style_category']}")
    """
    
    def __init__(
        self, 
        confidence_threshold: float = 0.8,
        enable_gpu: bool = True,
        model_config: Optional[Dict[str, Any]] = None
    ):
        """
        StyleAnalyzer instance'ını initialize eder.
        
        Args:
            confidence_threshold: Minimum güven skoru (0.0-1.0)
            enable_gpu: GPU kullanımını etkinleştir
            model_config: Özel model konfigürasyonu
        """
        # Instance variables tanımla ve initialize et
        self.confidence_threshold = confidence_threshold
        self.enable_gpu = enable_gpu
        self.model_config = model_config or self._get_default_config()
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.gif']
        
        # Private attributes
        self._models: Dict[str, Any] = {}
        self._analytics = AnalyticsManager()
        self._is_initialized = False
        
        # Validation
        self._validate_config()
        
        logger.info(f"StyleAnalyzer initialized with threshold={confidence_threshold}")
```

### 4. Error Handling Pattern

```python
# Custom exception classes
class AuraAIException(Exception):
    """AURA AI sistemi için base exception class."""
    pass

class AIModelError(AuraAIException):
    """AI model ile ilgili hatalar için exception."""
    pass

class ProcessingError(AuraAIException):
    """Veri işleme hatalar için exception."""
    pass

class ValidationError(AuraAIException):
    """Input validation hataları için exception."""
    pass

# Error handling decorator
def handle_errors(func):
    """
    Fonksiyon hatalarını yakalar ve loglar.
    Bu decorator tüm service fonksiyonlarında kullanılabilir.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValidationError as e:
            logger.warning(f"Validation error in {func.__name__}: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except AIModelError as e:
            logger.error(f"AI model error in {func.__name__}: {str(e)}")
            raise HTTPException(status_code=503, detail="AI service temporarily unavailable")
        except ProcessingError as e:
            logger.error(f"Processing error in {func.__name__}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal processing error")
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    return wrapper
```

---

## 🧪 Test Stratejileri

### Test Dizin Yapısı

```
tests/
├── __init__.py
├── conftest.py                 # Pytest configuration
├── unit/                       # Unit tests
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/                # Integration tests
│   ├── __init__.py
│   ├── test_api_endpoints.py
│   └── test_service_communication.py
├── e2e/                       # End-to-end tests
│   ├── __init__.py
│   └── test_workflows.py
├── performance/               # Performance tests
│   ├── __init__.py
│   └── test_load.py
└── fixtures/                  # Test data
    ├── images/
    ├── json/
    └── mock_responses/
```

### Test Configuration (conftest.py)

```python
"""
AURA AI Test Configuration
Bu dosya pytest için global configuration ve fixture'ları tanımlar.
"""

import pytest
import asyncio
from typing import Generator, AsyncGenerator
from httpx import AsyncClient
from fastapi.testclient import TestClient
import tempfile
import os
from unittest.mock import Mock, patch

# Test için gerekli importlar
from services.image_processing.main import app
from services.image_processing.config import get_settings
from shared.database import get_database
from shared.models.schemas import UserProfile, StyleAnalysis

# Test database configuration
@pytest.fixture(scope="session")
def test_database_url():
    """
    Test için geçici database URL'si oluştur.
    Her test session'ı için yeni bir test database kullanılır.
    """
    return "postgresql://test_user:test_pass@localhost:5432/aura_ai_test"

@pytest.fixture(scope="session")  
def override_get_settings():
    """
    Test environment için settings override et.
    Production ayarları test environment'a uygun olarak değiştirilir.
    """
    from services.image_processing.config import Settings
    
    # Test ayarlarını tanımla
    test_settings = Settings(
        DEBUG=True,
        ENVIRONMENT="test",
        DATABASE_URL="postgresql://test_user:test_pass@localhost:5432/aura_ai_test",
        REDIS_URL="redis://localhost:6379/1",  # Test için farklı DB
        SECRET_KEY="test-secret-key",
        LOG_LEVEL="DEBUG",
        ENABLE_METRICS=False,  # Test'te metrics disable
        AI_MODEL_PATH="./tests/fixtures/models"  # Mock model path
    )
    
    return test_settings

@pytest.fixture(scope="function")
async def db_session():
    """
    Her test için temiz database session oluştur.
    Test sonunda rollback yaparak database'i temizler.
    """
    from shared.database import SessionLocal, engine, Base
    
    # Test database'de tabloları oluştur
    Base.metadata.create_all(bind=engine)
    
    # Session oluştur
    session = SessionLocal()
    
    try:
        yield session
    finally:
        session.rollback()  # Test değişikliklerini geri al
        session.close()
        
        # Test sonunda tabloları temizle
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_client(override_get_settings) -> Generator[TestClient, None, None]:
    """
    FastAPI test client oluştur.
    Bu client HTTP request'leri test etmek için kullanılır.
    """
    # Settings'i override et
    app.dependency_overrides[get_settings] = lambda: override_get_settings
    
    with TestClient(app) as client:
        yield client
    
    # Test sonunda override'ı temizle
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
async def async_client(override_get_settings) -> AsyncGenerator[AsyncClient, None]:
    """
    Async HTTP client oluştur.
    Async endpoint'leri test etmek için kullanılır.
    """
    app.dependency_overrides[get_settings] = lambda: override_get_settings
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def sample_image_data():
    """
    Test için örnek görüntü datası oluştur.
    Gerçek görüntü dosyası okuyarak binary data döndürür.
    """
    image_path = "tests/fixtures/images/sample_shirt.jpg"
    
    if not os.path.exists(image_path):
        # Eğer fixture yoksa mock binary data oluştur
        return b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
    
    with open(image_path, 'rb') as f:
        return f.read()

@pytest.fixture(scope="function")
def sample_user_profile():
    """
    Test için örnek kullanıcı profili oluştur.
    Standartlaştırılmış test verisi sağlar.
    """
    return UserProfile(
        user_id="test_user_123",
        basic_info={
            "age": 28,
            "gender": "male",
            "body_type": "athletic"
        },
        style_preferences={
            "styles": ["casual", "business_casual"],
            "colors": ["blue", "white", "grey"],
            "brands": ["zara", "h&m"]
        },
        lifestyle={
            "occupation": "software_engineer",
            "budget_range": "mid_range"
        }
    )

@pytest.fixture(scope="function")
def mock_ai_model():
    """
    AI model'i için mock object oluştur.
    Gerçek AI model'e bağımlı olmadan test yapmayı sağlar.
    """
    mock_model = Mock()
    
    # Mock model response'u tanımla
    mock_model.predict.return_value = {
        "detected_objects": [
            {
                "class": "shirt",
                "confidence": 0.95,
                "bounding_box": [100, 150, 300, 400],
                "attributes": {
                    "color": ["blue", "white"],
                    "pattern": "striped",
                    "material": "cotton"
                }
            }
        ],
        "processing_time": 0.25
    }
    
    return mock_model

@pytest.fixture(scope="function")
def mock_external_services():
    """
    External service call'ları için mock'lar oluştur.
    Test'lerde gerçek service'lere bağımlı olmamayı sağlar.
    """
    with patch('requests.post') as mock_post, \
         patch('requests.get') as mock_get:
        
        # Mock successful responses
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"success": True, "data": {}}
        
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"success": True, "data": {}}
        
        yield {
            'post': mock_post,
            'get': mock_get
        }

# Test event loop configuration
@pytest.fixture(scope="session")
def event_loop():
    """
    Async test'ler için event loop oluştur.
    Session scope'da tek bir loop kullanılır.
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

# Test environment setup/teardown
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    Test environment'ı otomatik olarak setup/teardown yapar.
    autouse=True sayesinde her test session'ında otomatik çalışır.
    """
    print("\n🧪 Test environment setup başlatılıyor...")
    
    # Test database oluştur
    os.system("createdb aura_ai_test 2>/dev/null || true")
    
    # Test cache temizle
    os.system("redis-cli -n 1 FLUSHDB 2>/dev/null || true")
    
    # Test log directory oluştur
    os.makedirs("logs/test", exist_ok=True)
    
    yield
    
    print("\n🧹 Test environment cleanup yapılıyor...")
    
    # Test database sil
    os.system("dropdb aura_ai_test 2>/dev/null || true")
    
    # Test cache temizle
    os.system("redis-cli -n 1 FLUSHDB 2>/dev/null || true")

# Pytest marks tanımla
def pytest_configure(config):
    """
    Custom pytest marks tanımla.
    Bu marks test'leri kategorize etmek için kullanılır.
    """
    config.addinivalue_line(
        "markers", "unit: Unit test'leri işaretler"
    )
    config.addinivalue_line(
        "markers", "integration: Integration test'leri işaretler" 
    )
    config.addinivalue_line(
        "markers", "e2e: End-to-end test'leri işaretler"
    )
    config.addinivalue_line(
        "markers", "slow: Yavaş çalışan test'leri işaretler"
    )
    config.addinivalue_line(
        "markers", "ai_model: AI model gerektiren test'leri işaretler"
    )
```

### Unit Test Örneği

```python
"""
AURA AI Image Processing Service - Unit Tests
Bu dosya image processing servisinin unit test'lerini içerir.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
import base64
from fastapi import HTTPException

# Test edilecek modülleri import et
from services.image_processing.services.style_analyzer import StyleAnalyzer
from services.image_processing.models.schemas import ImageAnalysisRequest, ImageAnalysisResponse
from services.image_processing.utils.image_processor import ImageProcessor
from shared.exceptions import AIModelError, ValidationError

class TestStyleAnalyzer:
    """StyleAnalyzer class'ı için unit test'ler."""
    
    def test_init_with_default_params(self):
        """
        StyleAnalyzer'ın default parametrelerle initialize olduğunu test et.
        Bu test constructor'ın doğru çalıştığını ve default değerlerin 
        beklendiği gibi set edildiğini kontrol eder.
        """
        # Arrange - Test setup
        # Herhangi bir özel parametre vermeden analyzer oluştur
        
        # Act - Test edilen action
        analyzer = StyleAnalyzer()
        
        # Assert - Sonuçları kontrol et
        assert analyzer.confidence_threshold == 0.8  # Default threshold
        assert analyzer.enable_gpu == True  # Default GPU setting
        assert analyzer.supported_formats == ['.jpg', '.jpeg', '.png', '.gif']
        assert not analyzer._is_initialized  # İlk başta initialize olmamış olmalı
        assert analyzer._models == {}  # Model cache boş olmalı
    
    def test_init_with_custom_params(self):
        """
        StyleAnalyzer'ın custom parametrelerle initialize olduğunu test et.
        """
        # Arrange
        custom_threshold = 0.9
        custom_gpu = False
        custom_config = {"model_type": "yolo", "batch_size": 4}
        
        # Act  
        analyzer = StyleAnalyzer(
            confidence_threshold=custom_threshold,
            enable_gpu=custom_gpu,
            model_config=custom_config
        )
        
        # Assert
        assert analyzer.confidence_threshold == custom_threshold
        assert analyzer.enable_gpu == custom_gpu
        assert analyzer.model_config == custom_config
    
    def test_init_invalid_threshold_raises_error(self):
        """
        Geçersiz confidence threshold değeriyle initialize edildiğinde hata fırlattığını test et.
        """
        # Arrange & Act & Assert
        # Threshold 0'dan küçük
        with pytest.raises(ValidationError, match="Confidence threshold"):
            StyleAnalyzer(confidence_threshold=-0.1)
        
        # Threshold 1'den büyük
        with pytest.raises(ValidationError, match="Confidence threshold"):
            StyleAnalyzer(confidence_threshold=1.5)
    
    @patch('services.image_processing.services.style_analyzer.ai_model')
    def test_analyze_valid_image_success(self, mock_ai_model, sample_image_data):
        """
        Geçerli görüntü ile analiz işleminin başarılı olduğunu test et.
        """
        # Arrange
        analyzer = StyleAnalyzer(confidence_threshold=0.8)
        
        # Mock AI model response
        mock_ai_model.predict.return_value = {
            "detected_objects": [
                {
                    "class": "shirt",
                    "confidence": 0.95,
                    "bounding_box": [100, 150, 300, 400],
                    "attributes": {"color": ["blue"], "pattern": "solid"}
                }
            ],
            "processing_time": 0.25
        }
        
        # Act
        result = analyzer.analyze(sample_image_data)
        
        # Assert
        assert result is not None
        assert "detected_objects" in result
        assert len(result["detected_objects"]) == 1
        assert result["detected_objects"][0]["class"] == "shirt"
        assert result["detected_objects"][0]["confidence"] == 0.95
        
        # Mock'un doğru çağrıldığını kontrol et
        mock_ai_model.predict.assert_called_once_with(sample_image_data)
    
    def test_analyze_empty_image_raises_error(self):
        """
        Boş görüntü datası ile analiz yapıldığında hata fırlattığını test et.
        """
        # Arrange
        analyzer = StyleAnalyzer()
        
        # Act & Assert
        with pytest.raises(ValidationError, match="Image data boş olamaz"):
            analyzer.analyze(b'')  # Boş bytes
    
    def test_analyze_invalid_image_format_raises_error(self):
        """
        Geçersiz görüntü formatı ile analiz yapıldığında hata fırlattığını test et.
        """
        # Arrange
        analyzer = StyleAnalyzer()
        invalid_image_data = b'invalid_image_data'
        
        # Act & Assert
        with pytest.raises(ValidationError, match="Geçersiz görüntü formatı"):
            analyzer.analyze(invalid_image_data)
    
    @patch('services.image_processing.services.style_analyzer.ai_model')
    def test_analyze_ai_model_error_handling(self, mock_ai_model, sample_image_data):
        """
        AI model'de hata oluştuğunda exception handling'in doğru çalıştığını test et.
        """
        # Arrange
        analyzer = StyleAnalyzer()
        
        # Mock AI model'in hata fırlatmasını sağla
        mock_ai_model.predict.side_effect = Exception("AI model inference failed")
        
        # Act & Assert
        with pytest.raises(AIModelError, match="AI model inference failed"):
            analyzer.analyze(sample_image_data)
    
    @patch('services.image_processing.services.style_analyzer.ai_model')
    def test_analyze_low_confidence_filtering(self, mock_ai_model, sample_image_data):
        """
        Düşük confidence skorlu sonuçların filtrelendiğini test et.
        """
        # Arrange
        analyzer = StyleAnalyzer(confidence_threshold=0.9)  # Yüksek threshold
        
        # Mock AI model - düşük confidence response
        mock_ai_model.predict.return_value = {
            "detected_objects": [
                {
                    "class": "shirt",
                    "confidence": 0.85,  # Threshold'dan düşük
                    "bounding_box": [100, 150, 300, 400]
                },
                {
                    "class": "pants", 
                    "confidence": 0.95,  # Threshold'dan yüksek
                    "bounding_box": [100, 400, 300, 600]
                }
            ]
        }
        
        # Act
        result = analyzer.analyze(sample_image_data)
        
        # Assert
        # Sadece yüksek confidence'li object kalmalı
        assert len(result["detected_objects"]) == 1
        assert result["detected_objects"][0]["class"] == "pants"
        assert result["detected_objects"][0]["confidence"] == 0.95

class TestImageProcessor:
    """ImageProcessor utility class'ı için unit test'ler."""
    
    def test_validate_image_format_valid_formats(self):
        """
        Geçerli görüntü formatlarının doğru şekilde validate edildiğini test et.
        """
        # Arrange
        processor = ImageProcessor()
        
        # JPEG header
        jpeg_data = b'\xff\xd8\xff\xe0\x00\x10JFIF'
        
        # PNG header  
        png_data = b'\x89PNG\r\n\x1a\n'
        
        # Act & Assert
        assert processor.validate_image_format(jpeg_data) == True
        assert processor.validate_image_format(png_data) == True
    
    def test_validate_image_format_invalid_formats(self):
        """
        Geçersiz görüntü formatlarının reject edildiğini test et.
        """
        # Arrange
        processor = ImageProcessor()
        
        # Invalid data
        invalid_data = b'not_an_image'
        text_data = b'this is text content'
        
        # Act & Assert
        assert processor.validate_image_format(invalid_data) == False
        assert processor.validate_image_format(text_data) == False
    
    def test_resize_image_maintains_aspect_ratio(self):
        """
        Görüntü resize işleminin aspect ratio'yu koruduğunu test et.
        """
        # Arrange
        processor = ImageProcessor()
        # Mock image data (gerçek test'te PIL Image kullanılabilir)
        
        # Act & Assert
        # Bu test gerçek implementation'a göre düzenlenecek
        pass
    
    @pytest.mark.parametrize("image_size,expected_result", [
        (1024 * 1024, True),      # 1MB - valid
        (5 * 1024 * 1024, True),  # 5MB - valid
        (15 * 1024 * 1024, False) # 15MB - too large
    ])
    def test_validate_image_size(self, image_size, expected_result):
        """
        Görüntü boyutu validation'ının doğru çalıştığını test et.
        Parametrize decorator ile farklı boyutları test eder.
        """
        # Arrange
        processor = ImageProcessor()
        image_data = b'x' * image_size  # Mock image data
        
        # Act
        result = processor.validate_image_size(image_data, max_size=10*1024*1024)
        
        # Assert
        assert result == expected_result

@pytest.mark.asyncio
class TestImageAnalysisAPI:
    """Image Analysis API endpoint'leri için async unit test'ler."""
    
    async def test_analyze_endpoint_success(self, async_client, sample_image_data, mock_ai_model):
        """
        /analyze endpoint'inin başarılı response döndürdüğünü test et.
        """
        # Arrange
        base64_image = base64.b64encode(sample_image_data).decode()
        request_data = {
            "image": {
                "type": "base64",
                "data": base64_image
            },
            "analysis_options": {
                "detect_objects": True,
                "extract_colors": True,
                "classify_style": True
            }
        }
        
        # Act
        response = await async_client.post("/analyze", json=request_data)
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] == True
        assert "data" in response_data
        assert "detected_objects" in response_data["data"]
    
    async def test_analyze_endpoint_invalid_image(self, async_client):
        """
        Geçersiz görüntü ile /analyze endpoint'inin hata döndürdüğünü test et.
        """
        # Arrange
        request_data = {
            "image": {
                "type": "base64", 
                "data": "invalid_base64_data"
            },
            "analysis_options": {"detect_objects": True}
        }
        
        # Act
        response = await async_client.post("/analyze", json=request_data)
        
        # Assert
        assert response.status_code == 400  # Bad Request
        response_data = response.json()
        assert response_data["success"] == False
        assert "error" in response_data
    
    async def test_analyze_endpoint_missing_required_fields(self, async_client):
        """
        Gerekli field'lar eksik olduğunda validation error döndürdüğünü test et.
        """
        # Arrange
        request_data = {
            # image field eksik
            "analysis_options": {"detect_objects": True}
        }
        
        # Act
        response = await async_client.post("/analyze", json=request_data)
        
        # Assert
        assert response.status_code == 422  # Unprocessable Entity
    
    async def test_health_endpoint(self, async_client):
        """
        Health check endpoint'inin doğru çalıştığını test et.
        """
        # Act
        response = await async_client.get("/health")
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["status"] == "healthy"
        assert "service_name" in response_data
        assert "version" in response_data

# Test utilities
def create_mock_image_data(width: int = 100, height: int = 100) -> bytes:
    """
    Test için mock görüntü datası oluştur.
    """
    # Basit bir PNG header oluştur
    png_header = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
    png_data = png_header + b'\x00' * 50  # Mock PNG data
    return png_data

def assert_valid_analysis_response(response_data: dict):
    """
    Analysis response'ın geçerli formatda olduğunu assert et.
    """
    assert "detected_objects" in response_data
    assert "color_palette" in response_data
    assert "style_classification" in response_data
    assert "confidence_score" in response_data
    
    # Detected objects validation
    for obj in response_data["detected_objects"]:
        assert "class" in obj
        assert "confidence" in obj
        assert "bounding_box" in obj
        assert 0.0 <= obj["confidence"] <= 1.0
```

Bu kapsamlı geliştirici kılavuzu, AURA AI sisteminde profesyonel düzeyde geliştirme yapmak için gereken tüm bilgileri içerir.
