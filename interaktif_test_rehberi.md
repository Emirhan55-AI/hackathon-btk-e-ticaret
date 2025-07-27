# 🎯 AURA AI SİSTEMİ - İNTERAKTİF TEST REHBERİ
# Flow Engineering ile Manual Adım Adım Test

## 🚀 **GİRİŞ: UÇTAN UCA TEST SENARYOSU**

Bu rehber, Aura AI sisteminin Flow Engineering prensipleriyle nasıl çalıştığını
adım adım test etmenizi sağlar. Her adımda beklenen sonuçlar ve alternatif yollar belirtilmiştir.

---

## 📋 **SENARYO: "Akıllı Spor Ayakkabısı Önerisi"**

**Kullanıcı Hikayesi:**
*Ahmet, koşuya başlamak isteyen bir kullanıcı. Sistemden Türkçe olarak "Bugün spor için ayakkabı istiyorum" diye istek yapıyor. Sistem, 7 farklı AI servisini koordine ederek ona en uygun spor ayakkabısı önerilerini sunuyor.*

---

## 🔍 **ADIM 1: SİSTEM SAĞLIK KONTROLÜ**

### Test Komutu:
```powershell
# Tüm servisleri kontrol et
$services = @(8000, 8001, 8002, 8003, 8004, 8005, 8006, 8007)
foreach($port in $services) {
    try {
        $response = Invoke-WebRequest "http://localhost:$port/" -UseBasicParsing -TimeoutSec 3
        Write-Host "✅ Port $port: ÇALIŞIYOR" -ForegroundColor Green
    } catch {
        Write-Host "❌ Port $port: HATA" -ForegroundColor Red
    }
}
```

### Beklenen Sonuç:
- Tüm 8 servis (8000-8007) "ÇALIŞIYOR" durumunda olmalı
- %100 operasyonel durum

### Sorun Giderme:
```powershell
# Eğer servis çalışmıyorsa:
docker-compose ps
docker-compose logs [servis-adı]
```

---

## 👤 **ADIM 2: KULLANICI KAYDI VE GİRİŞ**

### Test URL'si:
```
http://localhost:8000/docs
```

### Manuel Test Adımları:

#### 2.1 Kullanıcı Kaydı:
```json
POST /auth/register
{
  "email": "test@aura.com",
  "password": "test123",
  "full_name": "Test Kullanıcısı"
}
```

#### 2.2 Kullanıcı Girişi:
```json
POST /auth/login
Form Data:
username: test@aura.com
password: test123
```

### Beklenen Sonuç:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### Token'ı Kaydet:
Bu token'ı sonraki isteklerde `Authorization: Bearer <token>` olarak kullan.

---

## 📸 **ADIM 3: GÖRÜNTÜ İŞLEME AI (Servis 1/7)**

### Test URL'si:
```
http://localhost:8001/docs
```

### Test Verisi:
```json
POST /analyze
{
  "image_description": "Mavi spor ayakkabısı",
  "analysis_type": "clothing_detection"
}
```

### Beklenen AI Yanıtı:
```json
{
  "status": "success",
  "detected_items": [
    {
      "type": "shoes",
      "category": "sport",
      "color": "blue",
      "confidence": 0.92
    }
  ],
  "ai_features": {
    "computer_vision": "active",
    "clip_analysis": "processed"
  }
}
```

### Doğrulama:
- ✅ Kıyafet türü doğru tespit edildi mi?
- ✅ Renk analizi çalışıyor mu?
- ✅ Güvenilirlik skoru yüksek mi (>0.8)?

---

## 🗣️ **ADIM 4: DOĞAL DİL İŞLEME AI (Servis 2/7)**

### Test URL'si:
```
http://localhost:8002/docs
```

### Test Verisi (Türkçe):
```json
POST /parse_request
{
  "text": "Bugün spor için ayakkabı istiyorum",
  "language": "tr",
  "context": "product_search"
}
```

### Beklenen AI Yanıtı:
```json
{
  "message": "Text analyzed successfully using advanced XLM-R transformer models",
  "detected_language": "tr",
  "language_confidence": 0.98,
  "analysis": {
    "intent": {
      "predicted_intent": "product_recommendation",
      "confidence": 0.94
    },
    "sentiment": {
      "predicted_sentiment": "positive",
      "confidence": 0.87
    },
    "context": {
      "predicted_context": "sport",
      "confidence": 0.91
    }
  }
}
```

### Çok Dilli Test:
```json
// İngilizce
{"text": "I want sports shoes for running"}

// Fransızca  
{"text": "Je veux des chaussures de sport pour courir"}

// İspanyolca
{"text": "Quiero zapatos deportivos para correr"}

// Almanca
{"text": "Ich möchte Sportschuhe zum Laufen"}
```

### Doğrulama:
- ✅ Dil tespiti doğru mu?
- ✅ Niyet "product_recommendation" olarak tespit edildi mi?
- ✅ Bağlam "sport" olarak anlaşıldı mı?
- ✅ Duygu analizi pozitif mi?

---

## 👤 **ADIM 5: STİL PROFİLİ AI (Servis 3/7)**

### Test URL'si:
```
http://localhost:8003/docs
```

### Test Verisi:
```json
POST /create_profile
{
  "user_preferences": {
    "activity": "sport",
    "style_preference": "modern_casual",
    "color_preferences": ["blue", "black", "white"]
  },
  "context_analysis": {
    "occasion": "sport",
    "weather": "moderate"
  }
}
```

### Beklenen AI Yanıtı:
```json
{
  "status": "Profile created successfully",
  "profile_data": {
    "style_type": "athletic_modern",
    "activity_match": "sport",
    "color_palette": ["blue", "black", "white"],
    "personality_traits": ["active", "health_conscious"],
    "confidence_score": 0.89
  },
  "ai_analysis": {
    "multi_modal_processing": "active",
    "style_clustering": "complete"
  }
}
```

### Doğrulama:
- ✅ Stil tipi spor aktivitelerine uygun mu?
- ✅ Renk tercihleri korundu mu?
- ✅ Güvenilirlik skoru yüksek mi?

---

## 🎨 **ADIM 6: KOMBİNASYON MOTORU AI (Servis 4/7)**

### Test URL'si:
```
http://localhost:8004/docs
```

### Test Verisi:
```json
POST /generate_combinations
{
  "style_profile": {
    "style_type": "athletic_modern",  
    "activity": "sport",
    "color_palette": ["blue", "black", "white"]
  },
  "occasion": "running",
  "weather": "mild"
}
```

### Beklenen AI Yanıtı:
```json
{
  "status": "Combinations generated successfully",
  "combinations": [
    {
      "combination_id": 1,
      "outfit_type": "running_ensemble",
      "items": {
        "shoes": "running_shoes_blue",
        "bottom": "sport_shorts_black", 
        "top": "moisture_wicking_tshirt_white"
      },
      "match_score": 0.93,
      "occasion_fit": "perfect"
    },
    {
      "combination_id": 2,
      "outfit_type": "gym_workout",
      "items": {
        "shoes": "cross_training_shoes",
        "bottom": "athletic_leggings",
        "top": "tank_top"
      },
      "match_score": 0.87
    }
  ],
  "ai_reasoning": "Intelligent graph-based combination algorithm"
}
```

### Doğrulama:
- ✅ Kombinasyonlar spor aktivitesine uygun mu?
- ✅ Renk uyumu korundu mu?
- ✅ Multiple kombinasyon seçeneği sunuldu mu?

---

## 🎯 **ADIM 7: ÖNERİ MOTORU AI (Servis 5/7)**

### Test URL'si:
```
http://localhost:8005/docs
```

### Test Verisi:
```json
POST /get_recommendations
{
  "user_profile": {
    "style_type": "athletic_modern",
    "budget_range": "medium",
    "size": "42"
  },
  "search_criteria": {
    "category": "shoes",
    "activity": "sport",
    "color_preference": "blue"
  }
}
```

### Beklenen AI Yanıtı:
```json
{
  "status": "Recommendations generated successfully",
  "recommendations": [
    {
      "product_id": 1,
      "name": "Nike Air Max 270",
      "price": 1299,
      "currency": "TRY",
      "match_score": 0.94,
      "similarity_reasons": [
        "Color match: Blue",
        "Activity fit: Running/Sport", 
        "Style compatibility: Modern athletic"
      ],
      "faiss_similarity": 0.91
    },
    {
      "product_id": 2,
      "name": "Adidas Ultraboost 22",
      "price": 1599,
      "match_score": 0.89,
      "faiss_similarity": 0.87
    }
  ],
  "ai_engine": "FAISS-powered similarity matching",
  "personalization_level": "high"
}
```

### Doğrulama:
- ✅ Ürünler kullanıcı kriterlerine uygun mu?
- ✅ Fiyat aralığı uygun mu?
- ✅ FAISS benzerlik skorları yüksek mi?
- ✅ Eşleşme sebepleri mantıklı mı?

---

## 🔄 **ADIM 8: AI ORKESTRATOR (Servis 6/7)**

### Test URL'si:
```
http://localhost:8006/docs
```

### Test Verisi:
```json
POST /orchestrate_workflow
{
  "workflow_type": "complete_recommendation",
  "user_input": {
    "text": "Bugün spor için ayakkabı istiyorum",
    "image": "blue_sports_shoe.jpg"
  },
  "services_to_coordinate": [
    "image_processing",
    "nlu", 
    "style_profile",
    "combination_engine",
    "recommendation"
  ]
}
```

### Beklenen AI Yanıtı:
```json
{
  "status": "Workflow orchestrated successfully",
  "orchestration_result": {
    "workflow_id": "wf_123456",
    "services_coordinated": 5,
    "execution_time": "2.3 seconds",
    "success_rate": 0.98,
    "final_recommendations": [
      "Nike Air Max 270 - Match: 94%",
      "Adidas Ultraboost - Match: 89%"
    ]
  },
  "service_flow": [
    "Image Processing → NLU → Style Profile → Combinations → Recommendations",
    "Cross-service data validation completed",
    "AI decision tree executed successfully"
  ],
  "ai_coordination": "Multi-agent system active"
}
```

### Doğrulama:
- ✅ Tüm 5 servis koordine edildi mi?
- ✅ Execution time makul mu (<5 saniye)?
- ✅ Success rate yüksek mi (>95%)?
- ✅ Final recommendations tutarlı mı?

---

## 📊 **ADIM 9: GERİ BİLDİRİM AI (Servis 7/7)**

### Test URL'si:
```
http://localhost:8007/docs
```

### Test Verisi:
```json
POST /process_feedback
{
  "user_id": "test_user",
  "interaction_data": {
    "recommended_products": ["Nike Air Max 270", "Adidas Ultraboost"],
    "user_choice": "Nike Air Max 270",
    "satisfaction_rating": 4.5,
    "feedback_text": "Tam aradığım ürünü buldum, teşekkürler!"
  },
  "behavioral_data": {
    "time_spent": 120,
    "pages_viewed": 5,
    "will_purchase": true
  }
}
```

### Beklenen AI Yanıtı:
```json
{
  "status": "Feedback processed successfully",
  "learning_update": {
    "user_preference_update": "completed",
    "model_improvement": "+3.2% accuracy gain",
    "recommendation_engine_tuning": "enhanced",
    "future_personalization": "improved"
  },
  "ai_insights": {
    "user_satisfaction": "high",
    "recommendation_quality": "excellent", 
    "purchase_probability": 0.87,
    "loyalty_indicator": "positive"
  },
  "adaptive_learning": "Real-time model updates applied"
}
```

### Doğrulama:
- ✅ Kullanıcı memnuniyeti kaydedildi mi?
- ✅ Model improvement kaydedildi mi?
- ✅ Gelecek öneriler için öğrenme gerçekleşti mi?

---

## 🛒 **ADIM 10: E-TİCARET İŞLEMİ (FULL CIRCLE)**

### Test URL'si:
```
http://localhost:8000/docs
```

### Token ile Authentication:
```
Authorization: Bearer <your_token_from_step_2>
```

### 10.1 Sepete Ekleme:
```json
POST /cart/add
{
  "product_id": 1,
  "quantity": 1,
  "size": "42",
  "color": "blue"
}
```

### 10.2 Sepeti Görüntüleme:
```json
GET /cart/
```

### 10.3 Sipariş Oluşturma:
```json
POST /orders/
{
  "shipping_address": {
    "street": "Test Sokak No:1",
    "city": "İstanbul", 
    "country": "Turkey",
    "postal_code": "34000"
  },
  "payment_method": "credit_card"
}
```

### Beklenen Sonuç:
```json
{
  "order_id": 12345,
  "status": "created",
  "total_amount": 1299.00,
  "estimated_delivery": "2-3 business days",
  "items": [
    {
      "product": "Nike Air Max 270",
      "quantity": 1,
      "price": 1299.00
    }
  ]
}
```

---

## 🎉 **DEMO BAŞARI KRİTERLERİ**

### ✅ **Sistem Seviyesi:**
- [ ] 8/8 servis operasyonel
- [ ] Tüm API endpoint'leri yanıt veriyor
- [ ] Cross-service communication çalışıyor

### ✅ **AI Seviyesi:**
- [ ] 7 AI servis koordineli çalışıyor
- [ ] Multilingual NLU çalışıyor (5 dil)
- [ ] Computer vision analiz çalışıyor
- [ ] Personalization algoritmaları aktif
- [ ] FAISS recommendation engine çalışıyor
- [ ] Adaptive learning çalışıyor

### ✅ **İş Süreci Seviyesi:**
- [ ] Kullanıcı journey'i kesintisiz
- [ ] AI önerileri relevant ve accurate
- [ ] E-ticaret işlemleri tamamlanabiliyor
- [ ] Flow Engineering prensipleri uygulanıyor

---

## 🚀 **SONUÇ VE DEĞERLENDİRME**

Bu test rehberini tamamladıktan sonra şunları elde etmiş olacaksınız:

1. **Teknik Yeterlilik Kanıtı**: 8 mikroservisin koordineli çalıştığı bir sistem
2. **AI Entegrasyon Kanıtı**: 7 farklı AI teknolojisinin bir arada çalıştığı ecosystem
3. **Flow Engineering Kanıtı**: Servislerin birbirleriyle akıllı bir şekilde veri paylaştığı workflow
4. **Production Ready Kanıtı**: Gerçek kullanıcı senaryolarını karşılayabilen sistem

### 📊 **Performans Metrikleri:**
- Sistem yanıt süresi: <3 saniye
- AI doğruluk oranı: >90%
- Service availability: %100
- User satisfaction: >4.5/5

### 🏆 **Elde Edilen Yetenekler:**
- Mikroservis mimarisi
- AI/ML entegrasyonu
- Docker orchestration
- API design & development
- Flow engineering
- Real-time personalization

---

**🎯 Bu test rehberi, sisteminizin production-ready olduğunu ve modern yazılım geliştirme prensiplerini başarıyla uyguladığınızı kanıtlar!**
