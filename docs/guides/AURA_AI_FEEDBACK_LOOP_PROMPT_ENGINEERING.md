# 🔄 AURA AI Feedback Loop Service - Advanced Prompt Engineering Framework

## 📋 Proje Özeti
AURA - Personal Style Assistant AI System'inin Feedback Loop servisi için gelişmiş prompt engineering kalıpları ve akış mühendisliği prensipleri kullanılarak tasarlanmış kapsamlı bir framework.

## 🎯 Prompt Engineering Kalıpları

### 1. Persona Kalıbı (Role-Based Prompting)

#### 1.1 AI Öğrenme Uzmanı Persona
```
Sen bir AI öğrenme uzmanısın ve kullanıcı geri bildirimlerinden model davranışlarını optimize etmek konusunda uzmanlaşmışsın. 

Görevin:
- Kullanıcı geri bildirimlerini derinlemesine analiz etmek
- Geri bildirimin kökenini (renk, stil, uygunluk, etkinlik) tespit etmek
- Öneri motorunun öğrenme parametrelerini optimize etmek
- Kullanıcı stil profilini sürekli iyileştirmek

Sen, moda trendleri, renk teorisi ve kişisel stil analizi konularında da uzman seviyede bilgiye sahipsin.
```

#### 1.2 Moda Danışmanı Persona
```
Sen deneyimli bir moda danışmanısın ve kullanıcıların stil tercihlerini anlamak konusunda uzmanlaşmışsın.

Yeteneklerin:
- Kullanıcının geri bildiriminden gizli tercihlerini çıkarmak
- Renk uyumu, stil harmonisi ve etkinliğe uygunluk değerlendirmesi
- Kültürel ve demografik faktörleri göz önünde bulundurma
- Trend analizi ve sezonsal uyum değerlendirmesi

Her geri bildirimi, kullanıcının uzun vadeli stil yolculuğu bağlamında değerlendiriyorsun.
```

### 2. Tarif Kalıbı (Recipe Pattern)

#### 2.1 Genel Geri Bildirim İşleme Tarifi
```
Kullanıcı geri bildirimi işleme tarifi:

1. GERİ BİLDİRİM ALMA
   - Kullanıcı ID'sini kaydet
   - Öneri ID'sini bağlı
   - Geri bildirim metnini al
   - Zaman damgasını ekle

2. BAĞLAM TOPLAMA
   - Kullanıcı stil profilini çek
   - İlgili öneri detaylarını al
   - Geçmiş geri bildirimleri kontrol et
   - Mevcut trend verilerini çek

3. ANALİZ YAPMA
   - Geri bildirim türünü sınıflandır
   - Duygusal tonu belirle
   - Problem alanını tespit et
   - Güven skorunu hesapla

4. ÖĞRENME GÜNCELLEMESİ
   - Öneri motorunu bilgilendir
   - Stil profilini güncelle
   - Model ağırlıklarını ayarla
   - Preference skorlarını revize et

5. YANIT ÜRETİMİ
   - Kullanıcıya teşekkür mesajı
   - İyileştirme önerisi
   - Alternatif öneriler
   - Takip soruları

6. LOGLAMA VE İZLEME
   - İşlem sonucunu kaydet
   - Performans metriklerini güncelle
   - Alert sistemini kontrol et
   - Rapor verilerini topla
```

#### 2.2 Olumsuz Geri Bildirim Özel Tarifi
```
Olumsuz geri bildirim işleme özel tarifi:

1. HIZLI MÜDAHALE
   - Negatif sentiment tespiti
   - Aciliyet seviyesi belirleme
   - Kullanıcı memnuniyetsizlik skoru güncelleme

2. DETAY ANALİZİ
   - Problemin kaynağını tespit et (renk/stil/uygunluk/etkinlik)
   - Benzer geçmiş olumsuz geri bildirimleri kontrol et
   - Pattern tanıma algoritması çalıştır

3. TATLAŞTıRMA STRATEJİSİ
   - Anlayışlı yanıt formüle et
   - Alternatif öneriler hazırla
   - Kişiselleştirme seviyesini artır

4. SİSTEM ÖĞRENMESİ
   - Benzer önerileri geçici olarak devre dışı bırak
   - Kullanıcı profil ağırlıklarını güncelle
   - Model confidence skorunu azalt
```

### 3. Şablon Kalıbı (Template Pattern)

#### 3.1 Geri Bildirim Veri Şablonu
```
=== AURA AI GERİ BİLDİRİM KAYDI ===
Kullanıcı ID: [USER_ID]
Öneri ID: [RECOMMENDATION_ID]
Geri Bildirim: "[FEEDBACK_TEXT]"
Geri Bildirim Türü: [FEEDBACK_TYPE]
Sentiment: [POSITIVE/NEUTRAL/NEGATIVE]
Güven Skoru: [CONFIDENCE_SCORE]
Zaman: [TIMESTAMP]
İşlem Süresi: [PROCESSING_TIME_MS]

=== ANALİZ SONUÇLARI ===
Problem Alanı: [PROBLEM_AREA]
Sınıflandırma: [CLASSIFICATION]
Önem Derecesi: [PRIORITY_LEVEL]
Önerilen Aksiyon: [RECOMMENDED_ACTION]

=== SİSTEM GÜNCELLEMELERİ ===
Stil Profili Güncellemesi: [PROFILE_UPDATES]
Öneri Motoru Güncellemesi: [RECOMMENDATION_UPDATES]
Model Parametreleri: [MODEL_PARAMETER_CHANGES]

=== KULLANICI YANITI ===
Teşekkür Mesajı: "[THANK_YOU_MESSAGE]"
İyileştirme Önerisi: "[IMPROVEMENT_SUGGESTION]"
Takip Sorusu: "[FOLLOW_UP_QUESTION]"
```

#### 3.2 Servis Koordinasyon Şablonu
```
=== SERVİS KOORDİNASYON AKIŞI ===
Tetikleyici Servis: [TRIGGER_SERVICE]
Hedef Servisler: [TARGET_SERVICES]
Koordinasyon Türü: [COORDINATION_TYPE]
Veri Transferi: [DATA_TRANSFER_FORMAT]

=== ASYNC GÖREV PLANI ===
1. [SERVICE_NAME] → [ACTION] → [EXPECTED_RESULT]
2. [SERVICE_NAME] → [ACTION] → [EXPECTED_RESULT]
3. [SERVICE_NAME] → [ACTION] → [EXPECTED_RESULT]

=== BAŞARI KRİTERLERİ ===
- [SUCCESS_METRIC_1]: [TARGET_VALUE]
- [SUCCESS_METRIC_2]: [TARGET_VALUE]
- [SUCCESS_METRIC_3]: [TARGET_VALUE]

=== HATA YÖNETİMİ ===
Olası Hatalar: [POTENTIAL_ERRORS]
Geri Dönüş Planı: [FALLBACK_STRATEGY]
Escalation Kriterleri: [ESCALATION_CONDITIONS]
```

### 4. Bağlam ve Talimat Kalıbı (Context & Instruction Pattern)

#### 4.1 Renk Uyumsuzluğu Bağlamı
```
BAĞLAM: Kullanıcı bir kombin önerisini "renkleri uyumlu değil" şeklinde değerlendirdi. 
Bu geri bildirim, sistem tarafından önerilen renk kombinasyonlarının kullanıcının 
estetik algısı veya kişisel renk tercihleri ile uyuşmadığını gösteriyor.

TALİMATLAR:
1. Önerilen kombinasyondaki renkleri analiz et
2. Kullanıcının geçmiş renk tercihlerini kontrol et
3. Renk teorisi kurallarını (komplementer, analog, triad) uygula
4. Kullanıcının cilt tonu, saç rengi gibi kişisel özelliklerini faktörize et
5. Renk öğrenme modelini bu geri bildirimin ışığında güncelle
6. Alternatif renk kombinasyonları öneri havuzuna ekle

BEKLENEN SONUÇ: Kullanıcının renk tercihleri daha doğru modellenmiş olacak ve 
gelecekteki önerilerde benzer renk uyumsuzlukları azalacak.
```

#### 4.2 Etkinlik Uygunsuzluğu Bağlamı
```
BAĞLAM: Kullanıcı "bu öneri bana uygun değildi" geri bildirimi verdi. Bu durum, 
önerilen kıyafet kombinasyonunun kullanıcının bulunduğu sosyal ortam, etkinlik türü 
veya kişisel stil kimliği ile uyuşmadığını işaret ediyor.

TALİMATLAR:
1. Önerinin verildiği bağlamı (etkinlik, hava durumu, zaman) analiz et
2. Kullanıcının yaşam tarzı profilini gözden geçir
3. Sosyal ortam ve etkinlik uygunluk parametrelerini değerlendir
4. Formallik seviyesi uyumunu kontrol et
5. Kişisel stil kimliği (minimalist, bohem, klasik, modern) ile eşleşmeyi kontrol et
6. Bağlamsal öğrenme algoritmasını bu veriye göre güncelle

BEKLENEN SONUÇ: Etkinlik ve bağlam bazlı öneriler daha hassas hale gelecek ve 
kullanıcı memnuniyeti artacak.
```

## 🔄 Akış Şemaları (Flow Engineering)

### 1. "Bu kombini beğenmedim" Geri Bildirimi Akışı

#### Akış Adımları:
1. **Giri̧ş Noktas ı**
   - Kullanıcı feedback endpoint'ine POST request gönderir
   - Request validation (user_id, recommendation_id, feedback_text kontrolü)
   - Rate limiting ve güvenlik kontrolleri

2. **Bağlam Toplama Aşaması**
   - Style Profile Service'ten kullanıcı profili çekilir
   - Recommendation Engine'den orijinal öneri detayları alınır
   - Image Processing Service'ten görsel analiz verileri alınır
   - Historical feedback data sorgulanır

3. **NLU Analiz Aşaması**
   - NLU Service ile feedback text analiz edilir
   - Sentiment analysis (negative/neutral/positive)
   - Intent classification (general dislike, color issue, style mismatch, etc.)
   - Entity extraction (specific clothing items, colors, styles mentioned)

4. **Sınıflandırma ve Skorlama**
   - Feedback türü belirlenir (negative_general, color_dissatisfaction, style_inappropriate, etc.)
   - Confidence score hesaplanır
   - Priority level atanır (high/medium/low)
   - Impact assessment yapılır

5. **Sistem Öğrenme Güncellemesi**
   - Recommendation Engine'e negative feedback iletilir
   - Style Profile Service'te user preferences güncellenir
   - Combination Engine'de problematic combinations flag'lenir
   - ML model weights adjusted (if applicable)

6. **Yanıt Üretimi**
   - Empathetic response generated
   - Alternative recommendations prepared
   - Follow-up questions formulated
   - Personalized improvement suggestions created

7. **Loglama ve Monitoring**
   - Feedback event logged to database
   - Analytics metrics updated
   - Performance monitoring alerts checked
   - A/B testing buckets updated (if applicable)

#### Servisler Arası Koordinasyon:
```
Feedback Loop Service (8007) 
    ↓ GET /profile/{user_id}
Style Profile Service (8003)
    ↓ GET /recommendation/{rec_id}
Recommendation Engine (8005)
    ↓ POST /analyze
NLU Service (8002)
    ↓ PUT /update_preferences
Style Profile Service (8003)
    ↓ POST /negative_feedback
Recommendation Engine (8005)
    ↓ POST /flag_combination
Combination Engine (8004)
```

### 2. "Bu renk uyumlu değil" Geri Bildirimi Akışı

#### Akış Adımları:
1. **Specialized Color Analysis**
   - Color extraction from recommended outfit
   - Color theory compliance check (complementary, analogous, triadic)
   - User's historical color preferences analysis
   - Skin tone and personal coloring consideration

2. **Enhanced NLU Processing**
   - Persona Pattern: "Sen bir renk teorisi uzmanısın"
   - Recipe Pattern: 6-step color feedback processing
   - Context Pattern: Color dissatisfaction specific analysis

3. **Targeted Learning Updates**
   - Color preference weights adjustment
   - Color combination blacklisting
   - Seasonal color palette updates
   - Personal color profile refinement

4. **Intelligent Response Generation**
   - Color education content
   - Alternative color combinations
   - Color theory explanations (optional)
   - Personalized color recommendations

#### Servisler Arası Koordinasyon:
```
Feedback Loop Service (8007)
    ↓ POST /analyze_colors
Image Processing Service (8001)
    ↓ GET /color_preferences/{user_id}
Style Profile Service (8003)
    ↓ POST /update_color_weights
Recommendation Engine (8005)
    ↓ POST /blacklist_color_combo
Combination Engine (8004)
```

### 3. "Bu öneri bana uygun değildi" Geri Bildirimi Akışı

#### Akış Adımları:
1. **Context Appropriateness Analysis**
   - Occasion/event context verification
   - Formality level mismatch detection
   - Lifestyle compatibility assessment
   - Cultural/social appropriateness check

2. **Advanced Persona Processing**
   - Moda Danışmanı Persona aktivasyonu
   - Kültürel sensitivite analizi
   - Yaşam tarzı uyumluluk değerlendirmesi

3. **Multi-dimensional Updates**
   - Occasion-based preference updates
   - Formality level recalibration
   - Lifestyle profile refinement
   - Context-aware learning enhancement

4. **Contextual Response Strategy**
   - Occasion-appropriate alternatives
   - Lifestyle-aligned suggestions
   - Educational content about appropriateness
   - Future context preferences inquiry

#### Servisler Arası Koordinasyon:
```
Feedback Loop Service (8007)
    ↓ GET /lifestyle_profile/{user_id}
Style Profile Service (8003)
    ↓ GET /occasion_context/{rec_id}
Recommendation Engine (8005)
    ↓ POST /analyze_appropriateness
NLU Service (8002)
    ↓ PUT /update_context_preferences
Style Profile Service (8003)
    ↓ POST /adjust_formality_weights
Recommendation Engine (8005)
```

### 4. "Beğendim, benzer önerilerde bulunabilir misin?" Geri Bildirimi Akışı

#### Akış Adımları:
1. **Positive Reinforcement Processing**
   - Success pattern identification
   - Liked elements extraction
   - Style preference confirmation
   - Positive feedback amplification

2. **Enhancement Learning**
   - Successful combination analysis
   - Preference weight strengthening
   - Similar style search
   - Trend alignment verification

3. **Proactive Recommendation Generation**
   - Similar outfit creation
   - Style variation generation
   - Seasonal adaptation
   - Trend-based extensions

4. **Engagement Optimization**
   - Positive user experience reinforcement
   - Loyalty building responses
   - Engagement metrics improvement
   - User satisfaction tracking

#### Servisler Arası Koordinasyon:
```
Feedback Loop Service (8007)
    ↓ POST /analyze_success
Combination Engine (8004)
    ↓ POST /strengthen_preferences
Style Profile Service (8003)
    ↓ GET /similar_combinations
Combination Engine (8004)
    ↓ POST /generate_similar
Recommendation Engine (8005)
    ↓ PUT /boost_confidence
Style Profile Service (8003)
```

## 📊 Prompt Engineering Success Metrics

### Performance Indicators
1. **Classification Accuracy**: >90% feedback categorization accuracy
2. **Response Relevance**: >85% user satisfaction with generated responses
3. **Learning Effectiveness**: >20% improvement in subsequent recommendations
4. **Processing Speed**: <500ms average feedback processing time
5. **User Engagement**: >30% increase in feedback provision rate

### A/B Testing Framework
- Persona Pattern vs Template Pattern effectiveness
- Recipe Pattern step optimization
- Context Pattern specificity levels
- Multi-pattern combination strategies

## 🔧 Implementation Roadmap

### Phase 1: Core Prompt Patterns (Week 1-2)
- Implement 4 core prompt patterns
- Basic feedback classification system
- Simple service coordination

### Phase 2: Advanced Flow Engineering (Week 3-4)
- Complex workflow orchestration
- Multi-service coordination patterns
- Advanced context analysis

### Phase 3: Machine Learning Integration (Week 5-6)
- ML model integration for classification
- Adaptive prompt pattern selection
- Continuous learning optimization

### Phase 4: Production Optimization (Week 7-8)
- Performance tuning
- Scalability improvements
- Monitoring and alerting systems

---

Bu framework, AURA AI'nin Feedback Loop servisinin gelişmiş prompt engineering teknikleri kullanarak kullanıcı geri bildirimlerini etkili bir şekilde işlemesini ve sistem genelinde öğrenmeyi optimize etmesini sağlar.
