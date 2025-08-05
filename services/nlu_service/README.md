# 🧠 AURA AI - NLU Service

Doğal Dil İşleme ve Türkçe moda terminolojisi anlayışı mikroservisi.

## 📋 Genel Bakış

NLU (Natural Language Understanding) Service, AURA AI sisteminin dil anlayış motorudur. Bu servis, kullanıcıların Türkçe moda ve stil ile ilgili isteklerini, geri bildirimlerini ve sorularını anlayarak uygun yanıtlar ve aksiyonlar üretir.

## 🎯 Temel Özellikler

### ✨ Ana Fonksiyonlar
- **Türkçe Moda NLU**: Moda terminolojisinde uzmanlaşmış dil anlayışı
- **Geri Bildirim Analizi**: Kullanıcı memnuniyeti ve öneri değerlendirmesi
- **İstek Sınıflandırması**: Stil tavsiyeleri, ürün arama, kombinasyon istekleri
- **Sentiment Analysis**: Duygusal analiz ve memnuniyet ölçümü
- **Intent Recognition**: Kullanıcı amacının belirlenmesi

### 🔧 Teknik Özellikler
- **AI Modelleri**: XLM-R, Turkish BERT, Custom Fashion NLU
- **Dil Desteği**: Türkçe odaklı, İngilizce destekli
- **Real-time Processing**: Düşük latency metin analizi
- **Context Awareness**: Konversasyon geçmişi ve bağlam takibi
- **Fashion Domain**: Moda terminolojisine özel optimizasyon

## 🚀 Hızlı Başlangıç

### Docker ile Çalıştırma
```powershell
# Repository'yi klonlayın
git clone https://github.com/Emirhan55-AI/aura-ai-system.git
cd aura-ai-system

# NLU Service'i başlatın
docker-compose up nlu-service
```

### Manuel Kurulum
```powershell
# Servis dizinine gidin
cd services/nlu_service

# Python ortamını hazırlayın
python -m venv venv
.\venv\Scripts\Activate.ps1

# Bağımlılıkları kurun
pip install -r requirements.txt

# Model dosyalarını indirin
python scripts/download_models.py

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
    "service": "nlu-service",
    "version": "1.0.0",
    "models_loaded": {
        "turkish_bert": true,
        "xlm_r": true,
        "fashion_nlu": true
    },
    "languages": ["tr", "en"]
}
```

### Metin Analizi
```http
POST /analyze/text
```
**İstek Gövdesi:**
```json
{
    "text": "Bu elbiseyi çok beğendim, benzer öneriler istiyorum",
    "user_id": "user_12345",
    "context": {
        "conversation_id": "conv_67890",
        "previous_recommendations": ["rec_001", "rec_002"]
    },
    "analysis_level": "detailed"
}
```

**Yanıt:**
```json
{
    "success": true,
    "analysis_id": "nlu_analysis_123",
    "results": {
        "intent": {
            "primary": "request_similar_recommendations",
            "confidence": 0.94,
            "secondary": ["positive_feedback", "style_preference"]
        },
        "sentiment": {
            "polarity": "positive",
            "score": 0.87,
            "intensity": "strong"
        },
        "entities": [
            {
                "text": "elbise",
                "type": "clothing_type",
                "confidence": 0.98,
                "normalized": "dress"
            }
        ],
        "fashion_context": {
            "style_preferences": ["elegant", "formal"],
            "color_mentions": [],
            "occasion_context": "general",
            "brand_mentions": []
        },
        "turkish_specifics": {
            "formality_level": "informal",
            "regional_dialect": "standard",
            "cultural_context": "urban_turkish"
        }
    },
    "processing_time": 0.12,
    "language_detected": "tr"
}
```

### Geri Bildirim Sınıflandırması
```http
POST /classify/feedback
```
**İstek Gövdesi:**
```json
{
    "feedback_text": "Renkleri hiç uyumlu değil, başka bir şey önerir misiniz?",
    "recommendation_id": "rec_12345",
    "user_id": "user_67890",
    "context": {
        "recommended_items": ["item_001", "item_002"],
        "user_style": "minimalist"
    }
}
```

**Yanıt:**
```json
{
    "success": true,
    "classification": {
        "feedback_type": "color_dissatisfaction",
        "confidence": 0.91,
        "sentiment": "negative",
        "actionable": true,
        "priority": "high"
    },
    "extracted_issues": [
        {
            "issue": "color_harmony",
            "severity": "high",
            "specific_complaint": "colors_not_matching"
        }
    ],
    "suggested_actions": [
        {
            "action": "provide_alternative_color_combinations",
            "priority": 1,
            "parameters": {
                "avoid_colors": ["clashing_combination"],
                "prefer_style": "minimalist"
            }
        },
        {
            "action": "update_user_color_preferences",
            "priority": 2,
            "parameters": {
                "negative_color_combination": ["red", "green"]
            }
        }
    ]
}
```

### Intent Recognition
```http
POST /recognize/intent
```
**İstek Gövdesi:**
```json
{
    "query": "İş görüşmesi için ne giysem?",
    "user_id": "user_12345",
    "context": {
        "weather": "cold",
        "season": "winter",
        "location": "Istanbul"
    }
}
```

**Yanıt:**
```json
{
    "success": true,
    "intent": {
        "category": "outfit_recommendation",
        "subcategory": "occasion_specific",
        "confidence": 0.96,
        "parameters": {
            "occasion": "job_interview",
            "formality": "formal",
            "urgency": "medium",
            "gender_specific": false
        }
    },
    "context_understanding": {
        "weather_considered": true,
        "season_considered": true,
        "location_considered": true,
        "cultural_context": "turkish_business"
    },
    "recommended_approach": {
        "style_direction": "formal_conservative",
        "color_palette": "neutral_professional",
        "clothing_types": ["suit", "dress_shirt", "formal_shoes"]
    }
}
```

### Dil Tespiti
```http
POST /detect/language
```
**İstek Gövdesi:**
```json
{
    "texts": [
        "Bu ayakkabı çok güzel",
        "This dress is beautiful",
        "J'aime cette robe"
    ]
}
```

**Yanıt:**
```json
{
    "success": true,
    "results": [
        {
            "text": "Bu ayakkabı çok güzel",
            "language": "tr",
            "confidence": 0.99,
            "script": "latin"
        },
        {
            "text": "This dress is beautiful",
            "language": "en",
            "confidence": 0.97,
            "script": "latin"
        },
        {
            "text": "J'aime cette robe",
            "language": "fr",
            "confidence": 0.94,
            "script": "latin"
        }
    ]
}
```

### Sentiment Analysis
```http
POST /analyze/sentiment
```
**İstek Gövdesi:**
```json
{
    "text": "Bu kombini kesinlikle tavsiye etmem, çok kötü görünüyor",
    "domain": "fashion",
    "include_emotions": true
}
```

**Yanıt:**
```json
{
    "success": true,
    "sentiment": {
        "polarity": "negative",
        "score": -0.82,
        "confidence": 0.94,
        "intensity": "strong"
    },
    "emotions": {
        "disappointment": 0.85,
        "frustration": 0.73,
        "dissatisfaction": 0.91
    },
    "fashion_specific": {
        "aesthetic_judgment": "negative",
        "recommendation_attitude": "strong_rejection",
        "style_satisfaction": "very_low"
    }
}
```

## 🧠 AI Modelleri

### 1. Turkish BERT - Türkçe Dil Modeli
- **Amaç**: Türkçe metin anlayışı ve representation
- **Eğitim**: Turkish Wikipedia + Fashion texts
- **Size**: 110M parameters
- **Performance**: 92% accuracy on Turkish NLU tasks

### 2. XLM-R - Multilingual Understanding
- **Amaç**: Çok dilli anlayış ve cross-lingual transfer
- **Dil**: 100+ dil desteği, TR-EN odaklı
- **Size**: 270M parameters
- **Kullanım**: Intent classification, entity extraction

### 3. Fashion Domain NLU
- **Amaç**: Moda terminolojisine özel dil anlayışı
- **Eğitim**: Turkish fashion corpus (500K sentences)
- **Özellik**: Fashion entities, style terminology
- **Performance**: 88% F1-score on fashion NER

### 4. Sentiment Classifier
- **Amaç**: Moda bağlamında duygusal analiz
- **Eğitim**: Turkish fashion reviews (100K labels)
- **Classes**: positive, negative, neutral + intensities
- **Domain**: Fashion-specific sentiment patterns

## 📁 Proje Yapısı

```
nlu_service/
├── src/
│   ├── models/
│   │   ├── turkish_bert.py        # Turkish BERT model wrapper
│   │   ├── xlm_r_model.py         # XLM-R model implementation
│   │   ├── fashion_nlu.py         # Fashion domain NLU
│   │   └── sentiment_model.py     # Sentiment analysis model
│   ├── api/
│   │   ├── routes.py              # API endpoint definitions
│   │   ├── middleware.py          # Request/response middleware
│   │   └── validators.py          # Input validation
│   ├── core/
│   │   ├── processor.py           # Main NLU processing engine
│   │   ├── intent_classifier.py   # Intent recognition
│   │   ├── entity_extractor.py    # Named entity recognition
│   │   └── context_manager.py     # Context and conversation state
│   ├── utils/
│   │   ├── text_preprocessor.py   # Text cleaning and preprocessing
│   │   ├── turkish_nlp.py         # Turkish language specifics
│   │   ├── fashion_lexicon.py     # Fashion terminology dictionary
│   │   └── performance.py         # Performance monitoring
│   └── config/
│       ├── settings.py            # Service configuration
│       └── model_config.py        # Model configurations
├── models/
│   ├── turkish_bert/             # Turkish BERT model files
│   ├── xlm_r/                    # XLM-R model files
│   ├── fashion_nlu/              # Fashion domain models
│   └── sentiment/                # Sentiment analysis models
├── data/
│   ├── lexicons/                 # Fashion terminology dictionaries
│   ├── training/                 # Training data samples
│   └── evaluation/               # Evaluation datasets
├── tests/
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   └── fixtures/                 # Test data and examples
├── docs/
│   ├── API.md                    # Detailed API documentation
│   ├── MODELS.md                 # Model documentation
│   └── TURKISH_NLP.md            # Turkish NLP specifics
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker configuration
└── README.md                    # This file
```

## 🔧 Konfigürasyon

### Environment Variables
```bash
# Service Configuration
NLU_SERVICE_PORT=8002
NLU_SERVICE_HOST=0.0.0.0
NLU_SERVICE_WORKERS=2

# Model Paths
TURKISH_BERT_PATH=/models/turkish_bert/
XLM_R_PATH=/models/xlm_r/
FASHION_NLU_PATH=/models/fashion_nlu/

# Processing Settings
MAX_TEXT_LENGTH=512
BATCH_SIZE=16
GPU_ENABLED=true
CUDA_DEVICE=0

# Cache Settings
REDIS_URL=redis://localhost:6379/2
CACHE_TTL=1800

# Turkish NLP Settings
TURKISH_MORPHOLOGY=true
DIACRITIC_RESTORATION=true
COLLOQUIAL_SUPPORT=true

# Monitoring
LOG_LEVEL=INFO
METRICS_ENABLED=true
```

### Model Configuration
```python
# models/config.py
TURKISH_BERT_CONFIG = {
    "model_name": "dbmdz/bert-base-turkish-cased",
    "max_length": 512,
    "device": "cuda" if torch.cuda.is_available() else "cpu"
}

FASHION_NLU_CONFIG = {
    "intent_threshold": 0.7,
    "entity_threshold": 0.8,
    "max_entities": 10,
    "context_window": 5
}

SENTIMENT_CONFIG = {
    "model_type": "fashion_sentiment_v1",
    "emotion_detection": true,
    "intensity_levels": 5
}
```

## 🧪 Test Etme

### Unit Testler
```powershell
# Tüm testleri çalıştır
python -m pytest tests/unit/ -v

# Model testleri
python -m pytest tests/unit/test_turkish_bert.py -v

# Fashion NLU testleri
python -m pytest tests/unit/test_fashion_nlu.py -v
```

### Integration Testler
```powershell
# API testleri
python -m pytest tests/integration/test_api.py -v

# End-to-end pipeline testleri
python -m pytest tests/integration/test_pipeline.py -v
```

### Turkish NLP Testler
```powershell
# Türkçe dil testleri
python -m pytest tests/turkish/ -v

# Moda terminolojisi testleri
python -m pytest tests/fashion_domain/ -v
```

## 📊 İzleme ve Metrikler

### Sağlık Kontrolleri
- **Model Availability**: NLU modellerinin yüklenme durumu
- **Language Detection**: Dil tespit doğruluğu
- **Processing Speed**: Ortalama işlem süresi
- **Memory Usage**: Model bellek kullanımı

### Metrikler
- `nlu_requests_total`: Toplam NLU isteği sayısı
- `nlu_processing_duration_seconds`: İşlem süresi
- `intent_classification_accuracy`: Intent doğruluğu
- `sentiment_analysis_accuracy`: Sentiment doğruluğu
- `turkish_text_ratio`: Türkçe metin oranı

### Model Performance
```yaml
# Model accuracy metrics
- turkish_bert_accuracy: 0.92
- xlm_r_multilingual_accuracy: 0.89
- fashion_nlu_f1_score: 0.88
- sentiment_classification_accuracy: 0.85
```

## 🚀 Deployment

### Docker Deployment
```powershell
# Build image
docker build -t aura-ai/nlu-service:latest .

# Run container
docker run -d \
  --name nlu-service \
  -p 8002:8002 \
  -v ./models:/app/models \
  -e CUDA_VISIBLE_DEVICES=0 \
  aura-ai/nlu-service:latest
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nlu-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nlu-service
  template:
    metadata:
      labels:
        app: nlu-service
    spec:
      containers:
      - name: nlu-service
        image: aura-ai/nlu-service:latest
        ports:
        - containerPort: 8002
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        env:
        - name: TURKISH_MORPHOLOGY
          value: "true"
```

## 🔗 Diğer Servislerle Entegrasyon

### Feedback Loop Service
- **Kullanım**: Geri bildirim analizi ve sınıflandırma
- **Data**: User feedback texts and sentiment
- **Output**: Actionable insights and improvement suggestions

### Orchestrator Service
- **Kullanım**: Workflow koordinasyonu ve intent routing
- **Endpoint**: `/orchestrate/nlu-analysis`
- **Processing**: Async text processing for complex workflows

### Style Profile Service
- **Kullanım**: Kullanıcı tercihleri çıkarımı
- **Data**: Intent ve entity bilgileri
- **Learning**: User preference pattern discovery

## 🐛 Troubleshooting

### Yaygın Sorunlar

**1. Model Loading Hatası**
```
Error: Could not load Turkish BERT model
Solution: Check model path and download models using scripts/download_models.py
```

**2. Low Confidence Scores**
```
Error: Intent confidence < 0.5
Solution: Check text quality, enable preprocessing, or retrain model
```

**3. Turkish Character Issues**
```
Error: Turkish characters not recognized
Solution: Ensure UTF-8 encoding and enable diacritic restoration
```

### Debug Modu
```powershell
# Debug mode ile çalıştırma
export LOG_LEVEL=DEBUG
export TURKISH_NLP_DEBUG=true
python main.py
```

## 📚 Ek Dokümantasyon

- [API Reference](docs/API.md) - Detaylı API dokümantasyonu
- [Model Guide](docs/MODELS.md) - NLU modelleri rehberi
- [Turkish NLP](docs/TURKISH_NLP.md) - Türkçe NLP özellikleri
- [Fashion Terminology](docs/FASHION_LEXICON.md) - Moda terminolojisi

## 🤝 Katkıda Bulunma

1. Fork the repository
2. Create feature branch (`git checkout -b feature/TurkishNLU`)
3. Commit changes (`git commit -m 'Add Turkish NLU feature'`)
4. Push to branch (`git push origin feature/TurkishNLU`)
5. Open Pull Request

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 👥 Takım

- **NLP Engineer**: Türkçe dil modelleri geliştirme
- **Computational Linguist**: Turkish morphology ve syntax
- **Fashion Domain Expert**: Moda terminolojisi ve context
- **ML Engineer**: Model optimization ve deployment

## 📞 İletişim

- **Issue Tracker**: [GitHub Issues](https://github.com/Emirhan55-AI/aura-ai-system/issues)
- **Documentation**: [Wiki](https://github.com/Emirhan55-AI/aura-ai-system/wiki)
- **Email**: nlp-support@aura-ai.com
