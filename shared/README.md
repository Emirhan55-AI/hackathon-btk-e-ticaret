# AURA AI Shared Components

Bu dizin, AURA AI mikroservis ekosisteminde paylaşılan bileşenleri içerir.

## Dizin Yapısı

```
shared/
├── models/                 # Pydantic model tanımları
│   ├── __init__.py        # Model paketi başlatıcı
│   ├── base.py            # Temel model sınıfları
│   ├── user.py            # Kullanıcı modelleri
│   ├── clothing.py        # Kıyafet modelleri
│   ├── recommendation.py  # Öneri modelleri
│   ├── feedback.py        # Geri bildirim modelleri
│   └── api_responses.py   # API yanıt modelleri
├── utils/                 # Yardımcı fonksiyonlar
│   ├── __init__.py        # Utils paketi başlatıcı
│   ├── logging.py         # Loglama yardımcıları
│   ├── validation.py      # Doğrulama fonksiyonları
│   ├── image_processing.py # Görüntü işleme yardımcıları
│   ├── text_processing.py # Metin işleme yardımcıları
│   ├── date_utils.py      # Tarih/zaman yardımcıları
│   └── security.py        # Güvenlik yardımcıları
├── database/              # Veritabanı ortak bileşenleri
│   ├── __init__.py        # Database paketi başlatıcı
│   ├── connection.py      # Veritabanı bağlantı yönetimi
│   ├── models.py          # SQLAlchemy model tanımları
│   ├── migrations/        # Veritabanı migration dosyaları
│   └── repositories/      # Ortak repository sınıfları
├── external_apis/         # Harici API istemcileri
│   ├── __init__.py        # External APIs paketi başlatıcı
│   ├── base_client.py     # Temel API istemci sınıfı
│   ├── fashion_apis.py    # Moda API istemcileri
│   ├── weather_api.py     # Hava durumu API istemcisi
│   └── translation_api.py # Çeviri API istemcisi
├── constants/             # Sabit değerler
│   ├── __init__.py        # Constants paketi başlatıcı
│   ├── clothing_types.py  # Kıyafet türü sabitleri
│   ├── colors.py          # Renk sabitleri
│   ├── styles.py          # Stil sabitleri
│   ├── occasions.py       # Durum sabitleri
│   └── languages.py       # Dil sabitleri
├── middleware/            # Ortak middleware bileşenleri
│   ├── __init__.py        # Middleware paketi başlatıcı
│   ├── auth.py            # Kimlik doğrulama middleware
│   ├── cors.py            # CORS middleware
│   ├── logging.py         # Loglama middleware
│   ├── rate_limiting.py   # Hız sınırlama middleware
│   └── error_handling.py  # Hata yönetimi middleware
├── cache/                 # Önbellekleme bileşenleri
│   ├── __init__.py        # Cache paketi başlatıcı
│   ├── redis_client.py    # Redis istemci yönetimi
│   ├── memory_cache.py    # Bellek önbelleği
│   └── decorators.py      # Önbellekleme dekoratörleri
├── monitoring/            # İzleme ve metrik bileşenleri
│   ├── __init__.py        # Monitoring paketi başlatıcı
│   ├── metrics.py         # Metrik toplama
│   ├── health_checks.py   # Sağlık kontrolleri
│   └── alerting.py        # Alarm sistemi
├── config/                # Konfigürasyon yönetimi
│   ├── __init__.py        # Config paketi başlatıcı
│   ├── settings.py        # Uygulama ayarları
│   ├── database.py        # Veritabanı konfigürasyonu
│   └── logging.py         # Loglama konfigürasyonu
├── exceptions/            # Özel hata sınıfları
│   ├── __init__.py        # Exceptions paketi başlatıcı
│   ├── base.py            # Temel hata sınıfları
│   ├── api_errors.py      # API hata sınıfları
│   ├── validation_errors.py # Doğrulama hata sınıfları
│   └── business_errors.py # İş mantığı hata sınıfları
├── ai_common/             # AI modelleri ortak bileşenleri
│   ├── __init__.py        # AI common paketi başlatıcı
│   ├── model_base.py      # Temel AI model sınıfı
│   ├── embeddings.py      # Embedding yardımcıları
│   ├── preprocessing.py   # Veri ön işleme
│   └── postprocessing.py  # Veri son işleme
└── tests/                 # Paylaşılan test yardımcıları
    ├── __init__.py        # Test utils paketi başlatıcı
    ├── fixtures.py        # Ortak test fixture'ları
    ├── mocks.py           # Mock objeler
    └── helpers.py         # Test yardımcı fonksiyonları
```

## Bileşen Kullanımı

### Model Kullanımı
```python
from shared.models.user import UserProfile
from shared.models.clothing import ClothingItem
from shared.models.api_responses import SuccessResponse

# Kullanıcı profili oluşturma
user_profile = UserProfile(
    user_id="12345",
    preferences={"style": "casual", "colors": ["blue", "black"]}
)

# API yanıtı oluşturma
response = SuccessResponse(
    message="Profile updated successfully",
    data=user_profile.dict()
)
```

### Utility Kullanımı
```python
from shared.utils.validation import validate_email, validate_image
from shared.utils.logging import get_logger
from shared.utils.image_processing import resize_image, extract_colors

# Loglama
logger = get_logger(__name__)
logger.info("Processing user request")

# Doğrulama
if validate_email("user@example.com"):
    logger.info("Valid email provided")

# Görüntü işleme
resized_image = resize_image(image_data, (224, 224))
colors = extract_colors(resized_image)
```

### Veritabanı Kullanımı
```python
from shared.database.connection import get_database_session
from shared.database.repositories.user_repository import UserRepository

# Veritabanı oturumu
async with get_database_session() as session:
    user_repo = UserRepository(session)
    user = await user_repo.get_by_id("12345")
```

### Cache Kullanımı
```python
from shared.cache.decorators import cache_result
from shared.cache.redis_client import get_redis_client

@cache_result(expiry=3600)  # 1 saat önbellekleme
async def get_user_recommendations(user_id: str):
    # Önerileri hesapla
    return recommendations

# Redis doğrudan kullanımı
redis = get_redis_client()
await redis.set("key", "value", ex=3600)
```

### Middleware Kullanımı
```python
from shared.middleware.auth import require_authentication
from shared.middleware.rate_limiting import rate_limit

@require_authentication
@rate_limit(max_requests=100, window=3600)
async def protected_endpoint():
    return {"message": "Authenticated and rate limited"}
```

## Konfigürasyon

### Environment Variables
```bash
# Veritabanı
DATABASE_URL=postgresql://user:pass@localhost/aura_ai
REDIS_URL=redis://localhost:6379

# API Keys
OPENAI_API_KEY=your_openai_key
HUGGINGFACE_API_KEY=your_hf_key

# Güvenlik
JWT_SECRET_KEY=your_secret_key
ENCRYPTION_KEY=your_encryption_key

# Monitoring
LOG_LEVEL=INFO
ENABLE_METRICS=true
```

### Settings Usage
```python
from shared.config.settings import get_settings

settings = get_settings()
database_url = settings.database_url
redis_url = settings.redis_url
log_level = settings.log_level
```

## Sabitler

### Clothing Types
```python
from shared.constants.clothing_types import CLOTHING_TYPES, ClothingCategory

# Kıyafet türlerini al
all_types = CLOTHING_TYPES
dress_category = ClothingCategory.DRESSES
```

### Colors
```python
from shared.constants.colors import COLOR_PALETTE, ColorFamily

# Renk paletini al
colors = COLOR_PALETTE
warm_colors = ColorFamily.WARM
```

## Hata Yönetimi

### Custom Exceptions
```python
from shared.exceptions.api_errors import NotFoundError, ValidationError
from shared.exceptions.business_errors import InsufficientDataError

# Hata fırlatma
if not user_exists:
    raise NotFoundError("User not found")

if not valid_data:
    raise ValidationError("Invalid input data")
```

### Error Handling
```python
from shared.middleware.error_handling import handle_api_errors

@handle_api_errors
async def api_endpoint():
    # API logic here
    pass
```

## AI Model Ortak Bileşenleri

### Model Base Class
```python
from shared.ai_common.model_base import BaseAIModel

class CustomModel(BaseAIModel):
    def __init__(self):
        super().__init__(model_name="custom_model")
    
    async def predict(self, input_data):
        # Model prediction logic
        return predictions
```

### Embeddings
```python
from shared.ai_common.embeddings import generate_text_embedding, generate_image_embedding

# Metin embedding'i
text_vector = generate_text_embedding("Bu elbise çok güzel")

# Görüntü embedding'i
image_vector = generate_image_embedding(image_data)
```

## Test Yardımcıları

### Fixture Kullanımı
```python
from shared.tests.fixtures import sample_user, sample_clothing_item

def test_user_processing(sample_user):
    # Test logic using shared fixture
    assert sample_user.user_id is not None
```

### Mock Usage
```python
from shared.tests.mocks import MockImageAnalysisService

async def test_with_mock():
    with MockImageAnalysisService() as mock_service:
        result = await mock_service.analyze_image(test_image)
        assert result.success is True
```

## Monitoring ve Metrikler

### Health Checks
```python
from shared.monitoring.health_checks import check_database, check_redis

# Sağlık kontrolleri
db_healthy = await check_database()
redis_healthy = await check_redis()
```

### Metrics Collection
```python
from shared.monitoring.metrics import record_request_duration, increment_counter

# Metrik toplama
with record_request_duration("api_request"):
    # API request logic
    pass

increment_counter("successful_predictions")
```

## Best Practices

1. **Import Conventions**: Shared bileşenleri her zaman `shared.` prefix ile import edin
2. **Type Hints**: Tüm shared fonksiyonlarda type hint kullanın
3. **Documentation**: Her public fonksiyon için docstring yazın
4. **Error Handling**: Shared bileşenlerde tutarlı hata yönetimi uygulayın
5. **Testing**: Shared bileşenler için kapsamlı testler yazın
6. **Versioning**: Breaking changes için semantic versioning kullanın

Bu shared bileşenler sayesinde AURA AI mikroservisleri arasında kod tekrarı önlenir ve tutarlılık sağlanır.
