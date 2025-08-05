# 📚 AURA AI - API Referans Dokümantasyonu

## 🌐 Genel Bakış

AURA AI sistemi, RESTful API prensiplerine uygun olarak tasarlanmış 7 mikroservisten oluşur. Bu dokümantasyon, tüm API endpoint'lerini, request/response formatlarını ve kullanım örneklerini detaylandırır.

## 🔗 Base URL'ler

```
Orchestrator Service:     http://localhost:8007
Image Processing:         http://localhost:8001  
NLU Service:             http://localhost:8002
Style Profile:           http://localhost:8003
Combination Engine:      http://localhost:8004
Recommendation Engine:   http://localhost:8005
Feedback Loop:           http://localhost:8006
```

## 🔐 Kimlik Doğrulama

### JWT Token Authentication

Tüm API çağrıları için `Authorization` header'ında JWT token gönderilmesi gerekir:

```http
Authorization: Bearer <your_jwt_token>
```

### API Key Authentication (Service-to-Service)

Servisler arası iletişimde API Key kullanılır:

```http
X-API-Key: <your_api_key>
```

## 📋 Ortak Response Formatı

Tüm API response'ları aşağıdaki standart formatı kullanır:

```json
{
  "success": true,
  "data": {},
  "message": "İşlem başarılı",
  "timestamp": "2024-01-15T10:30:00Z",
  "request_id": "req_123456789"
}
```

### Hata Response Formatı

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Geçersiz veri formatı",
    "details": {
      "field": "email",
      "reason": "Geçerli bir email adresi giriniz"
    }
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "request_id": "req_123456789"
}
```

---

## 🎯 1. Orchestrator Service API

### 🔍 **GET** `/health`

Sistem sağlık kontrolü

#### Response:
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "services": {
      "image_processing": "healthy",
      "nlu_service": "healthy",
      "style_profile": "healthy",
      "combination_engine": "healthy",
      "recommendation_engine": "healthy",
      "feedback_loop": "healthy"
    },
    "system_metrics": {
      "cpu_usage": 45.2,
      "memory_usage": 67.8,
      "disk_usage": 23.1
    }
  }
}
```

### 🚀 **POST** `/workflow/analyze_outfit`

Komple outfit analizi workflow'u

#### Request:
```json
{
  "user_id": "user_123",
  "images": [
    {
      "type": "base64",
      "data": "iVBORw0KGgoAAAANSUhEUgAA...",
      "filename": "shirt.jpg"
    }
  ],
  "context": {
    "occasion": "business",
    "weather": "spring",
    "preferences": ["casual", "modern"]
  }
}
```

#### Response:
```json
{
  "success": true,
  "data": {
    "workflow_id": "wf_123456",
    "analysis_results": {
      "detected_items": [...],
      "style_analysis": {...},
      "recommendations": [...]
    },
    "processing_time_ms": 1250
  }
}
```

---

## 🖼️ 2. Image Processing Service API

### 🔍 **POST** `/analyze`

Kıyafet görüntüsü analizi

#### Request:
```json
{
  "image": {
    "type": "base64",
    "data": "iVBORw0KGgoAAAANSUhEUgAA..."
  },
  "analysis_options": {
    "detect_objects": true,
    "extract_colors": true,
    "classify_style": true,
    "detect_patterns": true
  }
}
```

#### Response:
```json
{
  "success": true,
  "data": {
    "detected_objects": [
      {
        "class": "shirt",
        "confidence": 0.95,
        "bounding_box": [100, 150, 300, 400],
        "attributes": {
          "color": ["blue", "white"],
          "pattern": "striped",
          "material": "cotton",
          "sleeve_type": "long_sleeve"
        }
      }
    ],
    "dominant_colors": [
      {"hex": "#1E40AF", "percentage": 60.5},
      {"hex": "#FFFFFF", "percentage": 35.2}
    ],
    "style_classification": {
      "category": "business_casual",
      "confidence": 0.87,
      "subcategories": ["formal", "professional"]
    }
  }
}
```

### 📊 **GET** `/models`

Kullanılabilir AI modelleri

#### Response:
```json
{
  "success": true,
  "data": {
    "object_detection": {
      "name": "YOLO-v5-Fashion",
      "version": "1.2.0",
      "accuracy": 0.94,
      "supported_classes": ["shirt", "pants", "dress", "shoes", "accessories"]
    },
    "color_extraction": {
      "name": "ColorNet",
      "version": "2.1.0",
      "supported_formats": ["RGB", "HSV", "LAB"]
    }
  }
}
```

---

## 🧠 3. NLU Service API

### 💬 **POST** `/understand`

Doğal dil isteği analizi

#### Request:
```json
{
  "text": "İş toplantısı için koyu renk bir takım elbise kombinini öner",
  "language": "tr",
  "context": {
    "user_id": "user_123",
    "session_id": "session_456"
  }
}
```

#### Response:
```json
{
  "success": true,
  "data": {
    "intent": {
      "name": "request_outfit_recommendation",
      "confidence": 0.92
    },
    "entities": [
      {
        "type": "occasion",
        "value": "business_meeting",
        "confidence": 0.89
      },
      {
        "type": "color_preference",
        "value": "dark",
        "confidence": 0.94
      },
      {
        "type": "clothing_type",
        "value": "suit",
        "confidence": 0.97
      }
    ],
    "sentiment": {
      "polarity": "neutral",
      "confidence": 0.78
    }
  }
}
```

### 🏷️ **POST** `/classify`

Metin sınıflandırma

#### Request:
```json
{
  "text": "Bu kombinasyonu hiç beğenmedim, renkleri uyumsuz",
  "classification_types": ["sentiment", "feedback_category"]
}
```

#### Response:
```json
{
  "success": true,
  "data": {
    "classifications": {
      "sentiment": {
        "label": "negative",
        "confidence": 0.91,
        "score": -0.75
      },
      "feedback_category": {
        "label": "color_dissatisfaction",
        "confidence": 0.88
      }
    }
  }
}
```

---

## 👤 4. Style Profile Service API

### 👨‍💼 **POST** `/profile`

Kullanıcı profili oluşturma

#### Request:
```json
{
  "user_id": "user_123",
  "basic_info": {
    "age": 28,
    "gender": "male",
    "body_type": "athletic",
    "size_info": {
      "shirt": "L",
      "pants": "32/34",
      "shoes": "42"
    }
  },
  "style_preferences": {
    "styles": ["casual", "business_casual", "modern"],
    "colors": ["blue", "grey", "white", "black"],
    "brands": ["zara", "h&m", "uniqlo"],
    "avoid": {
      "colors": ["pink", "yellow"],
      "patterns": ["floral"],
      "styles": ["vintage"]
    }
  },
  "lifestyle": {
    "occupation": "software_engineer",
    "lifestyle_type": "urban_professional",
    "budget_range": "mid_range"
  }
}
```

#### Response:
```json
{
  "success": true,
  "data": {
    "profile_id": "prof_789012",
    "user_id": "user_123",
    "style_score": 85.5,
    "generated_tags": ["tech_professional", "minimalist", "color_conscious"],
    "recommendations": {
      "priority_items": ["white_dress_shirt", "navy_blazer", "dark_jeans"],
      "style_direction": "smart_casual_professional"
    }
  }
}
```

### 📊 **GET** `/profile/{user_id}`

Kullanıcı profili getirme

#### Response:
```json
{
  "success": true,
  "data": {
    "user_id": "user_123",
    "profile": {...},
    "style_evolution": {
      "initial_score": 70.2,
      "current_score": 85.5,
      "improvement_areas": ["color_coordination", "formal_wear"]
    },
    "wardrobe_stats": {
      "total_items": 45,
      "most_worn_category": "shirts",
      "least_worn_category": "accessories",
      "style_distribution": {
        "casual": 60,
        "business": 30,
        "formal": 10
      }
    }
  }
}
```

### 🎯 **POST** `/preferences/learn`

Tercih öğrenme

#### Request:
```json
{
  "user_id": "user_123",
  "interaction_data": {
    "action": "liked_outfit",
    "item_ids": ["item_456", "item_789"],
    "context": {
      "occasion": "date_night",
      "season": "autumn"
    },
    "feedback_score": 4.5
  }
}
```

---

## 🎨 5. Combination Engine Service API

### 🔀 **POST** `/combine`

Kıyafet kombinasyonu oluşturma

#### Request:
```json
{
  "user_id": "user_123",
  "base_items": [
    {
      "item_id": "item_123",
      "category": "shirt",
      "color": "white",
      "style": "formal"
    }
  ],
  "requirements": {
    "occasion": "business_meeting",
    "weather": "spring",
    "color_scheme": "monochromatic",
    "style_preference": "professional"
  },
  "constraints": {
    "budget_max": 500,
    "brands_avoid": ["luxury_brand_x"],
    "colors_avoid": ["bright_red"]
  }
}
```

#### Response:
```json
{
  "success": true,
  "data": {
    "combinations": [
      {
        "combination_id": "comb_456789",
        "score": 92.5,
        "items": [
          {
            "item_id": "item_123",
            "category": "shirt",
            "role": "base"
          },
          {
            "item_id": "item_456",
            "category": "blazer",
            "role": "outer_layer"
          },
          {
            "item_id": "item_789",
            "category": "trousers",
            "role": "bottom"
          }
        ],
        "analysis": {
          "color_harmony_score": 95,
          "style_coherence_score": 90,
          "occasion_appropriateness": 94,
          "overall_balance": "excellent"
        },
        "styling_tips": [
          "Kravatı koyu mavi seçerek kontrast yaratabilirsiniz",
          "Ayakkabı olarak siyah deri oxford önerilir"
        ]
      }
    ]
  }
}
```

### ✅ **POST** `/validate`

Kombinasyon doğrulama

#### Request:
```json
{
  "combination": {
    "items": [
      {"item_id": "item_123", "category": "shirt"},
      {"item_id": "item_456", "category": "pants"}
    ]
  },
  "validation_rules": ["color_harmony", "style_coherence", "season_appropriateness"]
}
```

#### Response:
```json
{
  "success": true,
  "data": {
    "is_valid": true,
    "validation_score": 87.5,
    "rule_results": {
      "color_harmony": {
        "passed": true,
        "score": 90,
        "details": "Renkler uyumlu"
      },
      "style_coherence": {
        "passed": true,
        "score": 85,
        "details": "Stil tutarlı"
      }
    },
    "suggestions": [
      "Aksesuar olarak kemer ekleyebilirsiniz"
    ]
  }
}
```

---

## 💡 6. Recommendation Engine Service API

### 🎯 **GET** `/recommendations/{user_id}`

Kişiselleştirilmiş öneriler

#### Query Parameters:
- `limit`: Öneri sayısı (default: 10)
- `category`: Kategori filtresi
- `occasion`: Durum filtresi  
- `budget_range`: Bütçe aralığı

#### Response:
```json
{
  "success": true,
  "data": {
    "recommendations": [
      {
        "recommendation_id": "rec_123456",
        "type": "outfit_complete",
        "score": 94.5,
        "reason": "Stil tercihiniz ve son aktivitelerinize göre",
        "items": [...],
        "estimated_budget": 250,
        "occasion_tags": ["work", "casual_friday"],
        "confidence": 0.92
      }
    ],
    "personalization_factors": {
      "style_match": 90,
      "color_preference": 95,
      "brand_affinity": 80,
      "budget_alignment": 85
    }
  }
}
```

### 📈 **GET** `/trending`

Trend analizleri

#### Response:
```json
{
  "success": true,
  "data": {
    "current_trends": [
      {
        "trend_id": "trend_789",
        "name": "Oversized Blazers",
        "category": "outerwear",
        "popularity_score": 87,
        "demographic": "25-35_female",
        "season": "spring_2024",
        "related_items": ["blazer_oversized", "wide_leg_pants"]
      }
    ],
    "user_trend_alignment": {
      "matching_trends": 3,
      "alignment_score": 72,
      "suggested_adoptions": ["minimalist_jewelry", "earth_tones"]
    }
  }
}
```

### 👍 **POST** `/feedback`

Öneri değerlendirme

#### Request:
```json
{
  "user_id": "user_123",
  "recommendation_id": "rec_123456",
  "feedback": {
    "rating": 4,
    "liked_aspects": ["color_combination", "style"],
    "disliked_aspects": ["price_point"],
    "would_purchase": true,
    "comments": "Çok güzel bir kombinasyon ama biraz pahalı"
  }
}
```

---

## 🔄 7. Feedback Loop Service API

### 📝 **POST** `/feedback`

Kullanıcı geribildirimi gönderme

#### Request:
```json
{
  "user_id": "user_123",
  "feedback_type": "outfit_rating",
  "content": {
    "outfit_id": "outfit_456",
    "rating": 4.5,
    "aspects": {
      "color_harmony": 5,
      "style_coherence": 4,
      "comfort": 4,
      "appropriateness": 5
    },
    "text_feedback": "Renkleri çok uyumlu ama pantolon biraz dar geldi",
    "tags": ["color_positive", "fit_negative"]
  },
  "context": {
    "occasion_worn": "dinner_date",
    "weather_conditions": "mild_spring",
    "user_mood": "confident"
  }
}
```

#### Response:
```json
{
  "success": true,
  "data": {
    "feedback_id": "fb_789012",
    "processed": true,
    "impact": {
      "profile_update": "preferences_updated",
      "model_contribution": "training_data_added",
      "immediate_actions": ["size_preference_adjusted"]
    },
    "thank_you_points": 10
  }
}
```

### 📊 **GET** `/analytics/{user_id}`

Kullanıcı analitikleri

#### Response:
```json
{
  "success": true,
  "data": {
    "feedback_summary": {
      "total_feedbacks": 45,
      "average_rating": 4.2,
      "feedback_frequency": "weekly"
    },
    "improvement_metrics": {
      "style_satisfaction_trend": "increasing",
      "recommendation_accuracy": 87.5,
      "outfit_success_rate": 82.3
    },
    "insights": [
      "Mavi tonlarında yüksek memnuniyet",
      "Formal giyimde daha fazla çeşitlilik arayışı",
      "Aksesuar kullanımında artış trendi"
    ]
  }
}
```

---

## 🚨 HTTP Status Kodları

| Kod | Açıklama |
|-----|----------|
| 200 | İşlem başarılı |
| 201 | Kaynak başarıyla oluşturuldu |
| 400 | Geçersiz istek |
| 401 | Kimlik doğrulama hatası |
| 403 | Yetkisiz erişim |
| 404 | Kaynak bulunamadı |
| 422 | İşlenemeyen veri |
| 429 | Rate limit aşıldı |
| 500 | Sunucu hatası |
| 503 | Servis geçici olarak kullanılamıyor |

## 🔄 Rate Limiting

Tüm API endpoint'leri için rate limiting uygulanır:

- **Authenticated Users**: 1000 request/hour
- **Service-to-Service**: 10000 request/hour  
- **Public Endpoints**: 100 request/hour

Rate limit aşıldığında `429 Too Many Requests` hatası döner.

## 📝 Örnek Kullanım Senaryoları

### Senaryo 1: Komple Outfit Analizi

```python
import requests

# 1. Görüntü analizi
image_response = requests.post(
    'http://localhost:8001/analyze',
    json={
        'image': {'type': 'base64', 'data': 'base64_image_data'},
        'analysis_options': {'detect_objects': True, 'extract_colors': True}
    },
    headers={'Authorization': 'Bearer your_token'}
)

# 2. Kombinasyon önerisi
combo_response = requests.post(
    'http://localhost:8004/combine',
    json={
        'user_id': 'user_123',
        'base_items': image_response.json()['data']['detected_objects'],
        'requirements': {'occasion': 'business', 'weather': 'spring'}
    },
    headers={'Authorization': 'Bearer your_token'}
)

# 3. Kişiselleştirilmiş öneri
rec_response = requests.get(
    'http://localhost:8005/recommendations/user_123?occasion=business',
    headers={'Authorization': 'Bearer your_token'}
)
```

Bu dokümantasyon, AURA AI sisteminin tüm API functionality'sini kapsamlı bir şekilde açıklar ve geliştiricilerin sistemi etkili bir şekilde kullanmasını sağlar.
