# 🧪 AURA AI SİSTEMİ - GELİŞMİŞ TEST KONFİGÜRASYONU
# Test Odaklı Geri Besleme Döngüsü (AlphaCodium/SED) Prensipleri

import pytest
import asyncio
import requests
import time
import json
from datetime import datetime
from typing import AsyncGenerator, Dict, List, Optional, Any
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
import logging

from app.main import app
from app.core.database import Base, get_db_session
from app.core.config import settings

# Test için logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tests/reports/test_execution.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Test database URL (in-memory SQLite for faster tests)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

class AuraTestConfig:
    """
    Aura AI sistemi için merkezi test konfigürasyonu sınıfı.
    
    Bu sınıf, tüm test senaryolarında kullanılacak ortak konfigürasyonları,
    servis URL'lerini ve test verilerini yönetir.
    """
    
    # Servis URL'leri - tüm mikroservislerin test adresleri
    SERVICES = {
        'backend': 'http://localhost:8000',           # Ana e-ticaret platformu
        'image_processing': 'http://localhost:8001',  # Görüntü işleme AI servisi
        'nlu': 'http://localhost:8002',               # Doğal dil işleme AI servisi
        'style_profile': 'http://localhost:8003',     # Stil profili AI servisi
        'combination_engine': 'http://localhost:8004', # Kombinasyon AI servisi
        'recommendation': 'http://localhost:8005',    # Öneri motoru AI servisi
        'orchestrator': 'http://localhost:8006',      # AI koordinatörü servisi
        'feedback': 'http://localhost:8007'           # Geri bildirim AI servisi
    }
    
    # Test zaman aşımı ayarları (saniye)
    TIMEOUT_SHORT = 5    # Hızlı health check'ler için
    TIMEOUT_MEDIUM = 15  # Normal AI işlemleri için
    TIMEOUT_LONG = 30    # Uzun workflow işlemleri için
    
    # Test kullanıcı verileri
    TEST_USER = {
        'email': 'test@aura.com',
        'password': 'test123',
        'full_name': 'Aura Test Kullanıcısı'
    }
    
    # Mock test verileri
    MOCK_IMAGE_DATA = {
        'image_description': 'Mavi business gömlek',
        'analysis_type': 'clothing_detection',
        'user_context': 'wardrobe_addition'
    }
    
    MOCK_NLU_DATA = {
        'text': 'Bugün işe gideceğim, şık bir ayakkabıya ihtiyacım var',
        'language': 'tr',
        'context': 'product_recommendation'
    }

class TestUtilities:
    """Test yardımcı fonksiyonları sınıfı"""
    
    @staticmethod
    def check_service_health(service_url: str, timeout: int = 5) -> bool:
        """
        Bir servisin sağlık durumunu kontrol eder.
        
        Args:
            service_url: Kontrol edilecek servisin URL'i
            timeout: İstek zaman aşımı süresi
            
        Returns:
            bool: Servis sağlıklı ise True, aksi halde False
        """
        try:
            # Backend servisi için /health endpoint'i kullan
            endpoint = f"{service_url}/health" if 'localhost:8000' in service_url else f"{service_url}/"
            response = requests.get(endpoint, timeout=timeout)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Servis sağlık kontrolü başarısız: {service_url} - {str(e)}")
            return False
    
    @staticmethod
    def measure_response_time(func, *args, **kwargs) -> tuple:
        """
        Bir fonksiyonun çalışma süresini ölçer.
        
        Returns:
            tuple: (sonuç, süre_ms)
        """
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration_ms = (end_time - start_time) * 1000
        return result, duration_ms


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
        echo=False,
    )
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Clean up
    await engine.dispose()


@pytest.fixture
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    async_session = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client(test_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test HTTP client."""
    
    # Override database dependency
    async def override_get_db():
        yield test_session
    
    app.dependency_overrides[get_db_session] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """Test user data."""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }


@pytest.fixture
def test_clothing_item_data():
    """Test clothing item data."""
    return {
        "name": "Test T-Shirt",
        "category": "tops",
        "color": "blue",
        "brand": "Test Brand",
        "tags": {
            "style": "casual",
            "season": "summer",
            "pattern": "solid"
        }
    }
