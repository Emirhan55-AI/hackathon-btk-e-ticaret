# 🖼️ AURA AI - Image Processing Service

Computer Vision ve AI tabanlı kıyafet analizi mikroservisi.

## 📋 Genel Bakış

Image Processing Service, AURA AI sisteminin görsel analiz motorudur. Bu servis, kullanıcıların yüklediği kıyafet görüntülerini analiz ederek renk, stil, tür ve diğer görsel özellikleri tespit eder.

## 🎯 Temel Özellikler

### ✨ Ana Fonksiyonlar
- **Kıyafet Türü Tespiti**: Elbise, pantolon, gömlek vb. türleri tanır
- **Renk Analizi**: Dominant renkleri ve renk paletini çıkarır
- **Stil Sınıflandırması**: Casual, formal, sporty vb. stilleri belirler
- **Kalite Değerlendirmesi**: Görüntü kalitesi ve analiz güvenilirliği
- **Türk Moda Desteği**: Türk moda trendlerine özel optimizasyon

### 🔧 Teknik Özellikler
- **AI Modelleri**: CLIP, Detectron2, Custom Fashion CNN
- **Görüntü Formatları**: JPEG, PNG, WebP desteği
- **Batch İşleme**: Çoklu görüntü analizi
- **Gerçek Zamanlı**: Düşük latency analiz
- **Ölçeklenebilir**: Horizontal scaling desteği

## 🚀 Hızlı Başlangıç

### Docker ile Çalıştırma
```powershell
# Repository'yi klonlayın
git clone https://github.com/Emirhan55-AI/aura-ai-system.git
cd aura-ai-system

# Image Processing Service'i başlatın
docker-compose up image-processing-service
```

### Manuel Kurulum
```powershell
# Servis dizinine gidin
cd services/image_processing_service

# Python ortamını hazırlayın
python -m venv venv
.\venv\Scripts\Activate.ps1

# Bağımlılıkları kurun
pip install -r requirements.txt

# Servisi başlatın
python main.py
```

## 📡 API Endpoints

### Sağlık Kontrolü
```http
GET /health
```
**Yanıt:**
```json
{
    "status": "healthy",
    "service": "image-processing",
    "version": "1.0.0",
    "models_loaded": true
}
```

### Kıyafet Analizi
```http
POST /analyze/clothing
```
**İstek Gövdesi:**
```json
{
    "image_data": "base64_encoded_image_data",
    "user_id": "user_12345",
    "analysis_type": "detailed",
    "return_features": true
}
```

**Yanıt:**
```json
{
    "success": true,
    "analysis_id": "analysis_67890",
    "results": {
        "clothing_items": [
            {
                "type": "dress",
                "confidence": 0.95,
                "colors": ["navy", "white", "gold"],
                "style": "casual",
                "pattern": "striped",
                "material": "cotton",
                "occasion": ["work", "casual"],
                "bbox": [10, 20, 300, 400]
            }
        ],
        "scene_analysis": {
            "background": "indoor",
            "lighting": "natural",
            "quality_score": 0.92
        },
        "turkish_context": {
            "cultural_appropriateness": "high",
            "seasonal_fit": "spring",
            "local_trend_match": 0.88
        }
    },
    "processing_time": 0.45,
    "model_versions": {
        "detection": "detectron2_v1.2",
        "classification": "clip_v2.1",
        "turkish_fashion": "custom_v1.0"
    }
}
```

### Batch Analiz
```http
POST /analyze/batch
```
**İstek Gövdesi:**
```json
{
    "images": [
        {
            "id": "img_001",
            "data": "base64_encoded_image_1"
        },
        {
            "id": "img_002", 
            "data": "base64_encoded_image_2"
        }
    ],
    "user_id": "user_12345",
    "priority": "normal"
}
```

### Renk Paleti Çıkarma
```http
POST /extract/colors
```
**İstek Gövdesi:**
```json
{
    "image_data": "base64_encoded_image_data",
    "color_count": 5,
    "include_percentages": true
}
```

**Yanıt:**
```json
{
    "success": true,
    "colors": [
        {
            "hex": "#2E4A62",
            "rgb": [46, 74, 98],
            "name": "navy",
            "percentage": 45.2
        },
        {
            "hex": "#FFFFFF",
            "rgb": [255, 255, 255],
            "name": "white",
            "percentage": 32.1
        }
    ],
    "dominant_color": "#2E4A62",
    "color_harmony": "complementary"
}
```

### Model Bilgileri
```http
GET /models/info
```
**Yanıt:**
```json
{
    "models": {
        "detectron2": {
            "version": "v1.2",
            "accuracy": 0.94,
            "classes": 50,
            "last_updated": "2024-01-15"
        },
        "clip": {
            "version": "v2.1",
            "accuracy": 0.91,
            "features": 512,
            "languages": ["en", "tr"]
        }
    },
    "total_analyses": 150420,
    "avg_processing_time": 0.42
}
```

## 🧠 AI Modelleri

### 1. Detectron2 - Object Detection
- **Amaç**: Kıyafet objelerini tespit etme ve sınıflandırma
- **Eğitim**: 100K+ Türk moda görüntüsü
- **Sınıflar**: 50+ kıyafet türü
- **Performans**: 94% accuracy, 0.3s inference time

### 2. CLIP - Visual-Text Understanding
- **Amaç**: Görsel-metin ilişkisi kurma ve stil analizi
- **Dil Desteği**: Türkçe ve İngilizce
- **Features**: 512-dimensional embeddings
- **Kullanım**: Stil sınıflandırma, context understanding

### 3. Custom Fashion CNN
- **Amaç**: Türk moda trendlerine özel analiz
- **Eğitim**: Turkish fashion dataset (50K images)
- **Özellik**: Cultural context, seasonal trends
- **Performans**: 88% accuracy on Turkish fashion

### 4. Color Analysis Model
- **Amaç**: Renk çıkarma ve harmonik analiz
- **Algoritma**: K-means clustering + color theory
- **Output**: Hex codes, RGB values, color names
- **Dil**: Türkçe renk isimleri desteği

## 📁 Proje Yapısı

```
image_processing_service/
├── src/
│   ├── models/
│   │   ├── detectron2_model.py    # Object detection model
│   │   ├── clip_model.py          # CLIP model wrapper
│   │   ├── fashion_cnn.py         # Custom fashion CNN
│   │   └── color_analyzer.py      # Color analysis model
│   ├── api/
│   │   ├── routes.py              # API endpoint definitions
│   │   ├── middleware.py          # Request/response middleware
│   │   └── validators.py          # Input validation
│   ├── core/
│   │   ├── processor.py           # Main processing engine
│   │   ├── pipeline.py            # Analysis pipeline
│   │   └── postprocessor.py       # Result post-processing
│   ├── utils/
│   │   ├── image_utils.py         # Image manipulation utilities
│   │   ├── turkish_fashion.py     # Turkish fashion specifics
│   │   └── performance.py         # Performance monitoring
│   └── config/
│       ├── settings.py            # Service configuration
│       └── model_config.py        # Model configurations
├── models/
│   ├── detectron2/               # Detectron2 model files
│   ├── clip/                     # CLIP model files
│   ├── fashion_cnn/              # Custom CNN weights
│   └── color_models/             # Color analysis models
├── tests/
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   └── fixtures/                 # Test data and images
├── docs/
│   ├── API.md                    # Detailed API documentation
│   ├── MODELS.md                 # Model documentation
│   └── DEPLOYMENT.md             # Deployment guide
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker configuration
├── docker-compose.yml           # Local development setup
└── README.md                    # This file
```

## 🔧 Konfigürasyon

### Environment Variables
```bash
# Service Configuration
IMAGE_SERVICE_PORT=8001
IMAGE_SERVICE_HOST=0.0.0.0
IMAGE_SERVICE_WORKERS=4

# Model Paths
DETECTRON2_MODEL_PATH=/models/detectron2/model.pth
CLIP_MODEL_PATH=/models/clip/
FASHION_CNN_PATH=/models/fashion_cnn/weights.pt

# Performance Settings
MAX_IMAGE_SIZE=2048
BATCH_SIZE=8
GPU_ENABLED=true
CUDA_DEVICE=0

# Cache Settings
REDIS_URL=redis://localhost:6379/1
CACHE_TTL=3600

# Monitoring
LOG_LEVEL=INFO
METRICS_ENABLED=true
```

### Model Configuration
```python
# models/config.py
DETECTRON2_CONFIG = {
    "model_zoo": "COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml",
    "confidence_threshold": 0.7,
    "nms_threshold": 0.3,
    "max_detections": 10
}

CLIP_CONFIG = {
    "model_name": "ViT-B/32",
    "language": "multilingual",
    "device": "cuda" if torch.cuda.is_available() else "cpu"
}
```

## 🧪 Test Etme

### Unit Testler
```powershell
# Tüm testleri çalıştır
python -m pytest tests/unit/ -v

# Specific test
python -m pytest tests/unit/test_detectron2_model.py -v

# Coverage ile
python -m pytest tests/unit/ --cov=src --cov-report=html
```

### Integration Testler
```powershell
# API testleri
python -m pytest tests/integration/test_api.py -v

# Model pipeline testleri
python -m pytest tests/integration/test_pipeline.py -v
```

### Performance Testler
```powershell
# Latency testleri
python tests/performance/test_latency.py

# Throughput testleri
python tests/performance/test_throughput.py
```

## 📊 İzleme ve Metrikler

### Sağlık Kontrolleri
- **Model Availability**: AI modellerinin yüklenme durumu
- **GPU Memory**: GPU bellek kullanımı
- **Processing Queue**: İşlem kuyruğu durumu
- **Response Time**: Ortalama yanıt süresi

### Metrikler
- `image_processing_requests_total`: Toplam istek sayısı
- `image_processing_duration_seconds`: İşlem süresi
- `model_inference_duration_seconds`: Model çıkarım süresi
- `image_processing_errors_total`: Hata sayısı
- `gpu_memory_usage_bytes`: GPU bellek kullanımı

### Alerting
```yaml
# Prometheus rules
- alert: HighResponseTime
  expr: image_processing_duration_seconds > 2.0
  labels:
    severity: warning
  annotations:
    summary: "Image processing response time is high"

- alert: ModelNotLoaded
  expr: model_loaded{service="image-processing"} == 0
  labels:
    severity: critical
  annotations:
    summary: "AI model is not loaded"
```

## 🚀 Deployment

### Docker Deployment
```powershell
# Build image
docker build -t aura-ai/image-processing:latest .

# Run container
docker run -d \
  --name image-processing \
  --gpus all \
  -p 8001:8001 \
  -v ./models:/app/models \
  aura-ai/image-processing:latest
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: image-processing-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: image-processing
  template:
    metadata:
      labels:
        app: image-processing
    spec:
      containers:
      - name: image-processing
        image: aura-ai/image-processing:latest
        ports:
        - containerPort: 8001
        resources:
          requests:
            nvidia.com/gpu: 1
            memory: "4Gi"
            cpu: "2"
          limits:
            nvidia.com/gpu: 1
            memory: "8Gi"
            cpu: "4"
```

## 🔗 Diğer Servislerle Entegrasyon

### Orchestrator Service
- **Kullanım**: Workflow koordinasyonu
- **Endpoint**: `/orchestrate/image-analysis`
- **Async**: Uzun işlemler için queue desteği

### Style Profile Service
- **Kullanım**: Kullanıcı stil tercihleri
- **Data**: User preferences for analysis customization
- **Cache**: User-specific model optimizations

### Recommendation Engine
- **Kullanım**: Görsel özellik transferi
- **Data**: Image embeddings ve visual features
- **ML Pipeline**: Feature extraction for recommendations

## 🐛 Troubleshooting

### Yaygın Sorunlar

**1. Model Loading Hatası**
```
Error: Could not load Detectron2 model
Solution: Check DETECTRON2_MODEL_PATH and model file existence
```

**2. GPU Memory Error**
```
Error: CUDA out of memory
Solution: Reduce BATCH_SIZE or enable CPU fallback
```

**3. Yavaş İşlem**
```
Error: Processing time > 5 seconds
Solution: Check GPU availability and model optimization
```

### Debug Modu
```powershell
# Debug mode ile çalıştırma
export LOG_LEVEL=DEBUG
export CUDA_LAUNCH_BLOCKING=1
python main.py
```

## 📚 Ek Dokümantasyon

- [API Reference](docs/API.md) - Detaylı API dokümantasyonu
- [Model Guide](docs/MODELS.md) - AI modelleri rehberi
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment
- [Turkish Fashion Dataset](docs/DATASET.md) - Veri seti bilgileri

## 🤝 Katkıda Bulunma

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 👥 Takım

- **AI Engineer**: Computer Vision model development
- **Backend Developer**: API ve mikroservis altyapısı
- **Turkish Fashion Expert**: Kültürel context ve trend analizi
- **DevOps Engineer**: Deployment ve monitoring

## 📞 İletişim

- **Issue Tracker**: [GitHub Issues](https://github.com/Emirhan55-AI/aura-ai-system/issues)
- **Documentation**: [Wiki](https://github.com/Emirhan55-AI/aura-ai-system/wiki)
- **Email**: support@aura-ai.com
