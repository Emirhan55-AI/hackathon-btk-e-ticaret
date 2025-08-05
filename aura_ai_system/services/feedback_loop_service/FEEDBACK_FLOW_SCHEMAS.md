# 🔄 AURA AI FEEDBACK LOOP - AKIŞ ŞEMALARı VE SERVİS KOORDİNASYONU
# Kullanıcı Geri Bildirimlerinde Prompt Engineering ve Akış Mühendisliği Örnekleri

"""
AURA AI Feedback Loop Servisi için kapsamlı akış şemaları ve servis koordinasyon planları.
Her geri bildirim türü için özelleştirilmiş prompt kalıpları ve akış mühendisliği.
"""

## ============================================================================
## 1. "BU KOMBİNİ BEĞENMEDİM" - GENEL OLUMSUZ GERİ BİLDİRİM
## ============================================================================

### 📋 PROMPT KALIPLARI

#### PERSONA KALIP:
"""
Sen AURA'nın yapay zeka öğrenme uzmanısın. Kullanıcının olumsuz geri bildirimlerini 
analiz etme konusunda uzmanlaşmışsın. Hedefin, bu geri bildirimin arkasındaki gerçek 
nedenleri tespit edip sistem performansını optimize etmek.
"""

#### TARİF KALIP:
"""
ADIM 1: Geri bildirim verisini al ve konteksti çek
ADIM 2: Kullanıcının profil ve tercih geçmişini analiz et  
ADIM 3: Önerilen kombinasyonun özelliklerini detaylandır
ADIM 4: Beğenmeme nedenlerini kategorize et (renk, stil, durum, beden)
ADIM 5: Model güncelleme parametrelerini hesapla
ADIM 6: Servisler arası koordinasyon planını oluştur
"""

#### ŞABLON KALIP:
```json
{
    "user_id": "[USER_ID]",
    "recommendation_id": "[RECOMMENDATION_ID]", 
    "feedback_type": "negative_general",
    "timestamp": "[TIMESTAMP]",
    "analysis": {
        "root_causes": ["[NEDEN1]", "[NEDEN2]"],
        "confidence_scores": {"style": 0.X, "color": 0.Y, "fit": 0.Z}
    },
    "actions": [
        {"service": "[SERVICE]", "update": "[UPDATE_TYPE]", "params": {}}
    ]
}
```

#### BAĞLAM VE TALİMAT KALIP:
"""
BAĞLAM: Kullanıcı ID-123, akşam partisi için önerilen lacivert elbise + kırmızı ayakkabı 
kombinasyonunu beğenmedi. Kullanıcının geçmişte daha rahat ve nötr renkleri tercih ettiği görülüyor.

TALİMAT: Bu geri bildirimi analiz et, renk uyumsuzluğu ve stil tercihi açısından değerlendir.
Kullanıcının stil profilini güncelle ve öneri motorunda ağırlıkları ayarla.
"""

### 🔄 AKIŞ ŞEMASI:

1. **Geri Bildirim Alımı**
   - Input: "Bu kombini beğenmedim" + recommendation_id + user_id
   - Validation: Geri bildirim formatı ve kullanıcı doğrulaması
   - Storage: Feedback veritabanına kaydet

2. **Kullanıcı Profili Çekme**
   - API Call: GET /users/{user_id}/profile (Style Profile Service)
   - Data: Stil tercihleri, renk profili, geçmiş beğeniler
   - Analysis: Tutarsızlık pattern'lerini tespit et

3. **Öneri İçeriği Analizi**
   - API Call: GET /recommendations/{recommendation_id} (Recommendation Engine)
   - Data: Önerilen kıyafetler, renk paleti, stil kategorisi
   - Analysis: Hangi öğelerin problematik olabileceğini değerlendir

4. **Geri Bildirim Sınıflandırma**
   - Process: Prompt pattern ile root cause analysis
   - Output: Primary/secondary reasons + confidence scores
   - Classification: Style mismatch vs color issue vs occasion inappropriateness

5. **Model Güncellemesi Hesaplama**
   - Calculate: Preference weight adjustments
   - Determine: Update magnitude (minor/moderate/major)
   - Generate: Specific update parameters for each service

6. **Servis Koordinasyonu**
   - Sequence: Style Profile → Combination Engine → Recommendation Engine
   - Updates: Parallel model weight adjustments
   - Validation: Cross-service consistency checks

7. **Loglama ve İzleme**
   - Log: Tüm analiz süreci ve sonuçları
   - Metrics: Feedback response time, accuracy metrics
   - Alert: Anomali detection ve system health monitoring

### 🔗 SERVİSLER ARASI KOORDİNASYON:

**1. Style Profile Service (Öncelik: HIGH)**
- Endpoint: PUT /style-profile/{user_id}/preferences
- Payload: Updated preference weights
- Action: Kullanıcının stil profil parametrelerini güncelle

**2. Combination Engine (Öncelik: MEDIUM)**
- Endpoint: POST /combination-engine/rules/update
- Payload: Negative combination patterns to avoid
- Action: Problematik kombinasyon kurallarını güncelle

**3. Recommendation Engine (Öncelik: MEDIUM)**
- Endpoint: POST /recommendations/scoring/update
- Payload: Item scoring adjustments
- Action: Öneri skorlama algoritmalarını güncelle

**4. Feedback Loop (Öncelik: LOW)**
- Endpoint: POST /feedback/learning/consolidate
- Payload: Aggregated learning insights
- Action: Genel öğrenme pattern'lerini güncellle

## ============================================================================
## 2. "BU RENK UYUMLU DEĞİL" - RENK UYUMSUZLUĞU GERİ BİLDİRİMİ
## ============================================================================

### 📋 PROMPT KALIPLARI

#### PERSONA KALIP:
"""
Sen AURA'nın renk teorisi ve uyumu uzmanısın. Renk kombinasyonlarını analiz etme ve 
kullanıcıların renk tercihlerini öğrenme konusunda derin uzmanlığın var.
"""

#### TARİF KALIP:
"""
ADIM 1: Problematik renk kombinasyonunu tespit et
ADIM 2: Renk teorisi kuralları açısından analiz et
ADIM 3: Kullanıcının renk tercih geçmişini çek
ADIM 4: Cilt tonu ve kişisel renk paleti faktörlerini dahil et
ADIM 5: Renk uyum skorlarını yeniden hesapla
ADIM 6: Renk tercih modelini güncelle
"""

### 🔄 AKIŞ ŞEMASI:

1. **Renk Analizi Başlatma**
   - Input: Color dissatisfaction feedback
   - Extract: Specific colors mentioned in combination
   - Identify: Primary problematic color pairs

2. **Renk Teorisi Analizi**
   - Check: Complementary/analogous/triadic harmony rules
   - Assess: Color temperature compatibility
   - Evaluate: Saturation and brightness levels

3. **Kullanıcı Renk Profili Analizi**
   - Retrieve: Historical color preferences
   - Analyze: Seasonal color palette preferences
   - Identify: Personal color DNA patterns

4. **Renk Uyumsuzluğu Teşhisi**
   - Determine: Specific harmony violation type
   - Calculate: Severity of color clash
   - Classify: User-specific vs universal issue

5. **Renk Modeli Güncelleme**
   - Adjust: Color preference weights
   - Update: Harmony rule parameters
   - Modify: Personal color palette boundaries

6. **Alternativ Renk Önerileri**
   - Generate: Compatible color suggestions
   - Test: New combinations against user profile
   - Validate: Harmony compliance

### 🔗 SERVİSLER ARASI KOORDİNASYON:

**1. Style Profile Service**
- Update: Color preference matrix
- Action: Renk tercih skorlarını güncelle

**2. Combination Engine**
- Update: Color harmony rules
- Action: Uyumsuz renk kombinasyonlarını engelle

**3. Image Processing Service**
- Update: Color detection algorithms
- Action: Renk analiz hassasiyetini artır

## ============================================================================
## 3. "BU ÖNERİ BANA UYGUN DEĞİLDİ" - UYGUNLUK SORUNU
## ============================================================================

### 📋 PROMPT KALIPLARI

#### PERSONA KALIP:
"""
Sen AURA'nın durum-bazlı giyim uzmanısın. Kullanıcıların yaşam tarzı, etkinlik türleri 
ve kişisel tercihlerine uygun öneriler sunma konusunda uzmanlaşmışsın.
"""

#### TARİF KALIP:
"""
ADIM 1: Öneri bağlamını analiz et (etkinlik, mekan, zaman)
ADIM 2: Kullanıcının yaşam tarzı profilini çek
ADIM 3: Uygunsuzluk türünü belirle (formallik, mekan, aktivite)
ADIM 4: Contextual appropriateness modelini güncelle
ADIM 5: Benzer durumlar için öneri kriterlerini revize et
ADIM 6: Personalization parametrelerini optimize et
"""

### 🔄 AKIŞ ŞEMASI:

1. **Bağlam Analizi**
   - Extract: Occasion/event context from recommendation
   - Identify: Formal vs casual appropriateness issue
   - Classify: Time, place, activity constraints

2. **Yaşam Tarzı Profili Analizi**
   - Retrieve: User lifestyle preferences
   - Analyze: Professional vs personal style needs
   - Assess: Comfort zone boundaries

3. **Uygunsuzluk Teşhisi**
   - Determine: Specific inappropriateness factor
   - Measure: Severity of context mismatch
   - Categorize: Occasion vs personal vs cultural misfit

4. **Contextual Model Güncelleme**
   - Adjust: Occasion-based recommendation weights
   - Update: Appropriateness scoring algorithms
   - Refine: Context detection parameters

### 🔗 SERVİSLER ARASI KOORDİNASYON:

**1. Style Profile Service**
- Update: Lifestyle and occasion preferences
- Action: Contextual profil parametrelerini güncelle

**2. Recommendation Engine**
- Update: Context-aware scoring
- Action: Durum-bazlı öneri ağırlıklarını revise et

**3. NLU Service**
- Update: Context extraction patterns
- Action: Bağlam analizi doğruluğunu artır

## ============================================================================
## 4. "BEĞENDİM, BENZER ÖNERİLERDE BULUNABİLİR MİSİN?" - POZİTİF GERİ BİLDİRİM
## ============================================================================

### 📋 PROMPT KALIPLARI

#### PERSONA KALIP:
"""
Sen AURA'nın başarı pattern'i analiz uzmanısın. Beğenilen önerilerin özelliklerini 
çıkarıp benzer başarılı deneyimler yaratma konusunda uzmanlaşmışsın.
"""

#### TARİF KALIP:
"""
ADIM 1: Beğenilen kombinasyonun core özelliklerini çıkar
ADIM 2: Başarı faktörlerini analiz et ve skorla
ADIM 3: Benzerlik boyutlarını belirle ve önceliklendír
ADIM 4: Varyasyon aralıklarını hesapla
ADIM 5: Başarılı pattern'leri güçlendir
ADIM 6: Benzer öneri stratejisini optimize et
"""

### 🔄 AKIŞ ŞEMASI:

1. **Başarı Analizi**
   - Extract: Successful recommendation features
   - Identify: Key satisfaction factors
   - Score: Individual element contributions

2. **Pattern Güçlendirme**
   - Amplify: Successful combination weights
   - Reinforce: Positive preference patterns
   - Strengthen: Model confidence in similar recommendations

3. **Benzerlik Stratejisi**
   - Define: Similarity dimensions (color, style, formality)
   - Calculate: Optimal variation ranges
   - Balance: Similarity vs diversity needs

4. **Recommendation Expansion**
   - Generate: Similar style combinations
   - Test: New variations against success pattern
   - Validate: User preference alignment

### 🔗 SERVİSLER ARASI KOORDİNASYON:

**1. Recommendation Engine (Öncelik: HIGH)**
- Action: Başarılı pattern'leri önceliklendír
- Update: Similarity search algorithms

**2. Style Profile Service (Öncelik: HIGH)**
- Action: Pozitif tercihleri güçlendir
- Update: Preference confidence scores

**3. Combination Engine (Öncelik: MEDIUM)**
- Action: Başarılı kombinasyon kurallarını genişlet
- Update: Pattern generation algorithms

## ============================================================================
## GENEL SERVİS KOORDİNASYON STRATEJİSİ
## ============================================================================

### 🎯 KOORDINASYON PRİORİTELERİ:

**HIGH PRIORITY (Immediate Update):**
- Style Profile Service: Kullanıcı tercihlerinin gerçek zamanlı güncellenmesi
- User Experience: Anında sonuç feedback'i

**MEDIUM PRIORITY (Batch Update):**
- Recommendation Engine: Model skorlama parametrelerinin güncelenmesi
- Combination Engine: Kombinasyon kurallarının revize edilmesi

**LOW PRIORITY (Scheduled Update):**
- Analytics Service: Trend analizi ve genel pattern'ler
- ML Infrastructure: Model retraining ve optimization

### 🔄 COORDINATION FLOW:

```
Feedback Input → Classification → Context Analysis → Impact Assessment
                                        ↓
                            Learning Actions Generation
                                        ↓
                   ┌────────────────────────────────────┐
                   │        Service Coordination        │
                   └────────────────────────────────────┘
                                        ↓
        ┌─────────────┬──────────────┬──────────────┬─────────────┐
        │   Style     │  Combination │ Recommendation│  Feedback   │
        │   Profile   │   Engine     │    Engine     │    Loop     │
        └─────────────┴──────────────┴──────────────┴─────────────┘
                                        ↓
                    Validation → Logging → Monitoring → Alerting
```

### 📊 PERFORMANS METRİKLERİ:

- **Response Time**: <100ms için feedback processing
- **Accuracy**: >85% feedback classification accuracy
- **Consistency**: >90% cross-service update consistency
- **Learning Rate**: Improvement in recommendation satisfaction after feedback

### 🚨 HATA YÖNETİMİ:

- **Circuit Breaker**: Servis erişilemezliği durumunda fallback mekanizması
- **Retry Logic**: Başarısız güncellemeler için exponential backoff
- **Rollback**: Problematik güncellemelerin geri alınması
- **Monitoring**: Real-time system health ve performance tracking

Bu yapılandırılmış sistem, AURA AI'nın sürekli öğrenmesini ve kullanıcı memnuniyetinin artırılmasını sağlar.
