# 🧠 AURA AI NLU Service - Advanced Prompt Engineering Framework
# Natural Language Understanding with Sophisticated Prompt Patterns

## 📋 Executive Summary

AURA AI'nın NLU (Natural Language Understanding) servisi, kullanıcıların doğal dil sorgularını anlayarak diğer mikroservisleri koordine eden merkezi analiz birimidir. Bu dokümanta, gelişmiş prompt engineering kalıpları ve akış mühendisliği prensipleri ile NLU servisinin nasıl çalıştığı detaylandırılmıştır.

### 🎯 Core NLU Capabilities

1. **Intent Detection**: Kullanıcının niyetini tespit etme
2. **Entity Extraction**: Sorgu içindeki önemli bilgileri çıkarma
3. **Context Analysis**: Bağlamsal bilgi analizi
4. **Service Coordination**: Diğer mikroservisleri yönlendirme
5. **Prompt Generation**: Optimization için structured prompt oluşturma

## 🔬 Prompt Engineering Patterns (4 Core Patterns)

### 1. 👥 Persona Pattern (Kişilik Kalıbı)

**Amaç**: NLU modelini belirli bir rol/kimlik ile donatarak domain-specific expertise sağlamak

```python
# Persona Pattern Template
PERSONA_TEMPLATES = {
    "style_consultant": {
        "system_prompt": """
        Sen AURA AI'nın uzman stil danışmanısın. 10 yıllık moda endüstrisi deneyimin var.
        
        Kişiliğin:
        - Kullanıcının kişisel stilini anlayan empatik bir danışman
        - Trend ve klasik stil bilgisine sahip uzman
        - Her vücut tipine ve yaşam tarzına uygun öneriler sunan
        - Bütçe dostu ve sürdürülebilir moda yaklaşımını benimseyen
        
        Görevin:
        - Kullanıcının doğal dil sorgusunu anlayarak niyetini tespit etmek
        - Sorgu içindeki stil, renk, etkinlik, hava durumu bilgilerini çıkarmak
        - Kullanıcının gardırop ve stil profili ile tutarlı analiz yapmak
        """,
        "example_queries": [
            "Bugün hava soğuk, ne giymeliyim?",
            "Bu gömlekle ne giyebilirim?",
            "Yarın ofiste çalışacağım, akşam da bir yemekte varım."
        ]
    },
    
    "wardrobe_analyzer": {
        "system_prompt": """
        Sen AURA AI'nın gardırop analisti uzmanısın. Kullanıcının mevcut kıyafetlerini
        ve kombinasyon potansiyellerini derinlemesine anlıyorsun.
        
        Uzmanlığın:
        - Kıyafet türleri, renkler, dokular arası uyum analizi
        - Mevsimsel ve etkinlik bazlı kategorizasyon
        - Eksik parça tespiti ve tamamlayıcı öneriler
        - Sustainable fashion ve mix-match stratejileri
        
        Analiz yaklaşımın:
        - Önce mevcut gardırobu kategorize et
        - Sonra kullanıcının ihtiyacını belirle
        - En uygun kombinasyon seçeneklerini sun
        """,
        "focus_areas": ["garment_types", "color_coordination", "seasonal_matching"]
    }
}
```

### 2. 📋 Recipe Pattern (Tarif Kalıbı)

**Amaç**: NLU işlemlerini adım adım tanımlayarak consistent ve doğru sonuçlar elde etmek

```python
# Recipe Pattern Templates
RECIPE_TEMPLATES = {
    "query_analysis_recipe": {
        "title": "Kullanıcı Sorgusu Analiz Tarifi",
        "steps": [
            {
                "step": 1,
                "action": "Girdi Ön İşleme",
                "description": "Kullanıcının sorgusunu temizle, normalize et ve dil tespiti yap",
                "prompt": """
                Sorgu: {user_query}
                
                Adım 1: Temizleme ve Normalizasyon
                - Yazım hatalarını düzelt
                - Gereksiz boşlukları kaldır
                - Emoji ve özel karakterleri analiz et
                - Dil tespiti yap (TR/EN)
                
                Çıktı formatı:
                {{
                    "cleaned_query": "temizlenmiş sorgu",
                    "detected_language": "tr/en",
                    "confidence": 0.95
                }}
                """
            },
            {
                "step": 2,
                "action": "Intent Classification",
                "description": "Kullanıcının ana niyetini belirle",
                "prompt": """
                Temizlenmiş Sorgu: {cleaned_query}
                
                Adım 2: Niyet Sınıflandırması
                
                Mümkün Intent'ler:
                1. "combination_request" - Kombin önerisi isteme
                2. "single_item_query" - Tek parça hakkında soru
                3. "wardrobe_analysis" - Gardırop analizi talebi
                4. "shopping_assistance" - Alışveriş yardımı
                5. "style_consultation" - Stil danışmanlığı
                6. "weather_based_outfit" - Hava durumu bazlı kıyafet
                7. "occasion_specific" - Özel etkinlik kıyafeti
                
                Intent tespiti için ipuçları:
                - "ne giyeyim", "kombin" → combination_request
                - "bu ... ile" → single_item_query
                - "gardırobum", "kıyafetlerim" → wardrobe_analysis
                - "satın al", "öneri", "arıyorum" → shopping_assistance
                
                Çıktı:
                {{
                    "primary_intent": "intent_name",
                    "confidence": 0.85,
                    "secondary_intents": ["intent2", "intent3"]
                }}
                """
            },
            {
                "step": 3,
                "action": "Entity Extraction",
                "description": "Sorgu içindeki önemli bilgileri çıkar",
                "prompt": """
                Sorgu: {cleaned_query}
                Intent: {primary_intent}
                
                Adım 3: Varlık Çıkarımı
                
                Çıkarılacak Entity'ler:
                
                1. CLOTHING_ITEMS:
                   - Türkçe: gömlek, pantolon, elbise, ayakkabı, çanta, ceket, kazak
                   - İngilizce: shirt, pants, dress, shoes, bag, jacket, sweater
                
                2. COLORS:
                   - Temel renkler: kırmızı/red, mavi/blue, siyah/black, beyaz/white
                   - Nüanslar: lacivert/navy, bordo/burgundy, krem/cream
                
                3. OCCASIONS:
                   - İş: ofis, toplantı, iş/work, meeting
                   - Sosyal: buluşma, yemek, parti/party, date
                   - Günlük: evde, alışveriş, spor/casual, home
                
                4. WEATHER:
                   - Sıcaklık: soğuk/cold, sıcak/hot, ılık/warm
                   - Durum: yağmurlu/rainy, güneşli/sunny, kar/snowy
                
                5. TIME_REFERENCES:
                   - Bugün, yarın, akşam, sabah, öğlen
                   - Today, tomorrow, evening, morning, afternoon
                
                Çıktı:
                {{
                    "entities": {{
                        "clothing_items": ["gömlek", "pantolon"],
                        "colors": ["mavi", "siyah"],
                        "occasions": ["ofis", "yemek"],
                        "weather": ["soğuk"],
                        "time_references": ["bugün", "akşam"]
                    }},
                    "entity_confidence": {{
                        "clothing_items": 0.92,
                        "colors": 0.87,
                        "occasions": 0.78
                    }}
                }}
                """
            },
            {
                "step": 4,
                "action": "Context Enrichment",
                "description": "Kullanıcı profili ve external data ile zenginleştirme",
                "prompt": """
                Extracted Data:
                - Intent: {primary_intent}
                - Entities: {extracted_entities}
                - User ID: {user_id}
                
                Adım 4: Bağlam Zenginleştirme
                
                Toplanacak Bağlamsal Bilgiler:
                
                1. USER_PROFILE (Style Profile Service - Port 8003):
                   - Stil tercihleri: casual, formal, bohemian, minimalist
                   - Renk paletleri: warm, cool, neutral, bold
                   - Vücut tipi ve ölçüler
                   - Yaşam tarzı: active, professional, student
                
                2. WARDROBE_DATA (User Wardrobe):
                   - Mevcut kıyafetler
                   - Favori kombinler
                   - Son kullanım tarihleri
                   - Eksik parçalar
                
                3. EXTERNAL_CONTEXT:
                   - Hava durumu (API çağrısı)
                   - Mevsim bilgisi
                   - Coğrafi konum
                   - Günün saati
                
                Context Fusion Strategy:
                {{
                    "user_context": {{
                        "style_preferences": ["casual", "minimalist"],
                        "favorite_colors": ["navy", "white", "gray"],
                        "body_type": "rectangle",
                        "lifestyle": "professional"
                    }},
                    "wardrobe_context": {{
                        "available_items": [...],
                        "frequent_combinations": [...],
                        "missing_pieces": [...]
                    }},
                    "environmental_context": {{
                        "weather": {{"temperature": 22, "condition": "cloudy"}},
                        "season": "spring",
                        "time_of_day": "morning"
                    }}
                }}
                """
            },
            {
                "step": 5,
                "action": "Service Routing Decision",
                "description": "Hangi servislerin çağrılacağına karar ver",
                "prompt": """
                Analysis Results:
                - Intent: {primary_intent}
                - Entities: {entities}
                - Context: {enriched_context}
                
                Adım 5: Servis Yönlendirme Kararı
                
                Intent-Based Service Routing:
                
                1. combination_request → 
                   Primary: Combination Engine (8004)
                   Secondary: Style Profile (8003), Image Processing (8001)
                
                2. single_item_query →
                   Primary: Image Processing (8001)
                   Secondary: Recommendation Engine (8005)
                
                3. wardrobe_analysis →
                   Primary: Style Profile (8003)
                   Secondary: Combination Engine (8004)
                
                4. shopping_assistance →
                   Primary: Recommendation Engine (8005)
                   Secondary: Style Profile (8003)
                
                Service Coordination Plan:
                {{
                    "primary_service": "combination_engine",
                    "secondary_services": ["style_profile", "image_processing"],
                    "execution_order": ["parallel", "sequential"],
                    "fallback_services": ["recommendation_engine"]
                }}
                """
            },
            {
                "step": 6,
                "action": "Structured Prompt Generation",
                "description": "Target servisleri için optimize edilmiş prompt oluştur",
                "prompt": """
                Final Analysis:
                - Intent: {intent}
                - Entities: {entities}
                - Context: {context}
                - Target Services: {target_services}
                
                Adım 6: Yapılandırılmış Prompt Oluşturma
                
                Service-Specific Prompt Templates:
                
                FOR COMBINATION_ENGINE:
                "Kullanıcı Profili: {user_style_profile}
                Mevcut Gardırop: {wardrobe_items}
                İhtiyaç: {intent_description}
                Kısıtlamalar: {constraints}
                Hava Durumu: {weather_info}
                Etkinlik: {occasion}
                
                Görev: {specific_task}
                Beklenen Çıktı: {expected_output_format}"
                
                FOR RECOMMENDATION_ENGINE:
                "Arama Kriterleri: {search_criteria}
                Stil Profili: {user_preferences}
                Bütçe: {budget_range}
                Kategori: {item_categories}
                
                Recommendation Parametreleri: {recommendation_params}"
                
                Generated Prompts:
                {{
                    "combination_engine_prompt": "...",
                    "recommendation_engine_prompt": "...",
                    "style_profile_query": "..."
                }}
                """
            }
        ]
    }
}
```

### 3. 🎨 Template Pattern (Şablon Kalıbı)

**Amaç**: Tutarlı ve yeniden kullanılabilir NLU çıktı formatları oluşturmak

```python
# Template Pattern Definitions
TEMPLATE_PATTERNS = {
    "nlu_analysis_template": {
        "structure": """
        {
            "query_metadata": {
                "original_query": "[USER_ORIGINAL_QUERY]",
                "cleaned_query": "[PROCESSED_QUERY]",
                "language": "[DETECTED_LANGUAGE]",
                "timestamp": "[ANALYSIS_TIMESTAMP]"
            },
            "intent_analysis": {
                "primary_intent": "[PRIMARY_INTENT]",
                "confidence": "[CONFIDENCE_SCORE]",
                "intent_category": "[CATEGORY]",
                "secondary_intents": ["[INTENT_2]", "[INTENT_3]"]
            },
            "entity_extraction": {
                "clothing_items": ["[ITEM_1]", "[ITEM_2]"],
                "colors": ["[COLOR_1]", "[COLOR_2]"],
                "occasions": ["[OCCASION_1]"],
                "weather_references": ["[WEATHER_CONDITION]"],
                "time_references": ["[TIME_REF]"],
                "style_modifiers": ["[STYLE_1]", "[STYLE_2]"]
            },
            "context_analysis": {
                "formality_level": "[FORMAL|CASUAL|MIXED]",
                "urgency": "[HIGH|MEDIUM|LOW]",
                "complexity": "[SIMPLE|MODERATE|COMPLEX]",
                "personalization_level": "[GENERIC|PERSONALIZED|HIGHLY_PERSONALIZED]"
            },
            "service_routing": {
                "primary_service": "[TARGET_SERVICE]",
                "secondary_services": ["[SERVICE_1]", "[SERVICE_2]"],
                "execution_strategy": "[PARALLEL|SEQUENTIAL|CONDITIONAL]",
                "fallback_plan": "[FALLBACK_STRATEGY]"
            },
            "generated_prompts": {
                "combination_engine": "[STRUCTURED_PROMPT_FOR_COMBINATIONS]",
                "recommendation_engine": "[STRUCTURED_PROMPT_FOR_RECOMMENDATIONS]",
                "style_profile": "[STRUCTURED_PROMPT_FOR_PROFILE]"
            }
        }
        """,
        
        "validation_rules": [
            "primary_intent must be one of predefined intents",
            "confidence scores must be between 0.0 and 1.0",
            "at least one clothing_item or occasion must be extracted",
            "service_routing must include valid service names"
        ]
    },
    
    "service_prompt_templates": {
        "combination_engine_template": """
        KULLANICI PROFİLİ:
        - Stil Tercihi: [USER_STYLE_PREFERENCE]
        - Favori Renkler: [USER_FAVORITE_COLORS]
        - Vücut Tipi: [USER_BODY_TYPE]
        - Yaşam Tarzı: [USER_LIFESTYLE]
        
        MEVCUT GARDIROP:
        [WARDROBE_ITEMS_LIST]
        
        SORGU ANALİZİ:
        - Niyet: [PRIMARY_INTENT]
        - Kıyafet Öğeleri: [EXTRACTED_CLOTHING_ITEMS]
        - Etkinlik: [EXTRACTED_OCCASIONS]
        - Hava Durumu: [WEATHER_CONTEXT]
        
        GÖREV: [SPECIFIC_TASK_DESCRIPTION]
        
        BEKLENEN ÇIKTI:
        - En az 3 kombin önerisi
        - Her kombin için uygun olma nedeni
        - Alternatif parça önerileri
        - Stil tutarlılığı skoru
        """,
        
        "recommendation_engine_template": """
        ARAMA KRİTERLERİ:
        - Kategori: [ITEM_CATEGORIES]
        - Renk Tercihi: [COLOR_PREFERENCES]
        - Stil: [STYLE_PREFERENCES]
        - Bütçe Aralığı: [BUDGET_RANGE]
        
        KULLANICI BAĞLAMI:
        - Yaş Grubu: [AGE_GROUP]
        - Cinsiyet: [GENDER]
        - Beden: [SIZE_INFO]
        - Konum: [LOCATION]
        
        ETKİNLİK DETAYLARI:
        - Etkinlik Türü: [OCCASION_TYPE]
        - Formallık: [FORMALITY_LEVEL]
        - Mevsim: [SEASON]
        - Hava Durumu: [WEATHER]
        
        HEDEF: [RECOMMENDATION_GOAL]
        
        ÇIKTI FORMAT:
        - Öneri listesi (5-10 ürün)
        - Her ürün için uygunluk puanı
        - Fiyat karşılaştırması
        - Kullanıcı yorumları özeti
        """
    }
}
```

### 4. 🧭 Context & Instruction Pattern (Bağlam ve Talimat Kalıbı)

**Amaç**: Zengin bağlamsal bilgi ve net talimatlarla NLU performansını optimize etmek

```python
# Context & Instruction Pattern Framework
CONTEXT_INSTRUCTION_PATTERNS = {
    "contextual_analysis_framework": {
        "temporal_context": {
            "instruction": """
            Zaman bağlamını analiz ederken şu faktörleri göz önünde bulundur:
            
            ZAMAN DİLİMLERİ:
            - Sabah (06:00-11:00): İş kıyafetleri, formal öğeler
            - Öğlen (11:00-14:00): Casual-smart kombinler
            - Öğleden sonra (14:00-18:00): İş sonrası geçiş kıyafetleri
            - Akşam (18:00-23:00): Sosyal etkinlik kıyafetleri
            - Gece (23:00-06:00): Rahat, konforlu öğeler
            
            MEVSİMSEL BAĞLAM:
            - İlkbahar: Katmanlı giyim, geçiş parçaları
            - Yaz: Hafif kumaşlar, açık renkler
            - Sonbahar: Orta kalınlık, earth tones
            - Kış: Kalın katmanlar, koyu renkler
            
            Kullanıcının zaman referansını bu bağlamla eşleştir.
            """,
            
            "context_variables": {
                "current_time": "[SYSTEM_TIME]",
                "season": "[CURRENT_SEASON]",
                "user_timezone": "[USER_TIMEZONE]",
                "cultural_calendar": "[LOCAL_HOLIDAYS_EVENTS]"
            }
        },
        
        "social_context": {
            "instruction": """
            Sosyal bağlamı değerlendirirken şu unsurları analiz et:
            
            ETKİNLİK TİPLERİ:
            1. Profesyonel:
               - İş toplantısı → Formal business attire
               - Sunum → Confident, authoritative look
               - Network etkinliği → Smart casual
            
            2. Sosyal:
               - Arkadaş buluşması → Casual, personal style
               - Romantik yemek → Elegant, appealing
               - Parti → Trendy, fun elements
            
            3. Kişisel:
               - Evde → Comfort-focused
               - Spor → Functional, athletic
               - Alışveriş → Practical, stylish
            
            SOSYAL KODLAR:
            - Dress code belirtildi mi?
            - Katılımcı profili nasıl?
            - Beklenen davranış normları?
            - Kültürel hassasiyetler var mı?
            
            Bu analizi kullanarak uygun formality seviyesini belirle.
            """,
            
            "social_variables": {
                "event_type": "[EVENT_CATEGORY]",
                "attendee_profile": "[ATTENDEE_DEMOGRAPHICS]",
                "cultural_context": "[CULTURAL_NORMS]",
                "dress_code": "[FORMAL|SEMI_FORMAL|CASUAL|THEMED]"
            }
        },
        
        "environmental_context": {
            "instruction": """
            Çevresel faktörleri comprehensive olarak değerlendir:
            
            HAVA DURUMU İMPLİKASYONLARI:
            - Sıcaklık → Katman sayısı, kumaş ağırlığı
            - Nem → Kumaş nefes alabilirliği, anti-perspirant özellikler
            - Rüzgar → Etek boyu, saç düzeni etkileri
            - Yağış → Su geçirmez özellikler, şemsiye koordinasyonu
            
            MEKAN ÖZELLİKLERİ:
            - İç mekan → Klimatizasyon, aydınlatma etkileri
            - Dış mekan → Güneş koruması, pratiklik
            - Karma → Transition pieces, çıkarılabilir katmanlar
            
            AKTİVİTE GEREKSİNİMLERİ:
            - Çok yürüme → Rahat ayakkabı, esnek kumaşlar
            - Uzun oturma → Wrinkle-resistant, comfortable fit
            - Fiziksel aktivite → Stretch, moisture-wicking
            
            Bu faktörleri combination önerilerinde öncelikle.
            """,
            
            "environmental_variables": {
                "weather_data": "[DETAILED_WEATHER_INFO]",
                "venue_type": "[INDOOR|OUTDOOR|MIXED]",
                "activity_level": "[SEDENTARY|MODERATE|ACTIVE]",
                "duration": "[SHORT|MEDIUM|LONG]"
            }
        }
    },
    
    "advanced_instruction_sets": {
        "personalization_instructions": """
        Kişiselleştirme seviyesini belirlerken şu kriterler uygulan:
        
        PERSONALIZATION LEVELS:
        
        1. GENERIC (Kişiselleştirme yok):
           - Yeni kullanıcı, profil bilgisi minimal
           - Genel stil kuralları uygula
           - Trend-based öneriler sun
           - Universal flattering seçenekler öner
        
        2. BASIC (Temel kişiselleştirme):
           - Temel profil bilgisi mevcut (yaş, cinsiyet, beden)
           - Genel stil tercihi belirlendi
           - Renk paletleri uygulan
           - Body type considerations dahil et
        
        3. ADVANCED (İleri kişiselleştirme):
           - Detaylı stil profili mevcut
           - Geçmiş seçimler analiz edildi
           - Feedback history var
           - Lifestyle patterns belirlendi
        
        4. EXPERT (Uzman seviye kişiselleştirme):
           - Comprehensive style DNA oluşturuldu
           - Micro-preferences tespit edildi
           - Predictive modeling aktif
           - Contextual learning patterns var
        
        Her seviye için farklı prompt complexity ve detail level uygula.
        """,
        
        "quality_assurance_instructions": """
        NLU çıktısının kalitesini garanti etmek için şu kontrolleri yap:
        
        ACCURACY CHECKS:
        1. Intent-Entity Consistency:
           - Çıkarılan entity'ler intent ile uyumlu mu?
           - Contradiction var mı?
           - Missing critical entities?
        
        2. Context Relevance:
           - Bağlamsal bilgiler sorgu ile relevant mi?
           - Temporal inconsistencies var mı?
           - Cultural appropriateness?
        
        3. Service Routing Logic:
           - Target service intent'e uygun mu?
           - Backup options mantıklı mı?
           - Execution order optimized mi?
        
        QUALITY METRICS:
        - Intent confidence > 0.7
        - At least 2 entities extracted
        - Context relevance > 0.8
        - Service routing coverage > 90%
        
        Bu thresholdları karşılamayan analysis'leri re-process et.
        """
    }
}
```

## 🔄 Flow Engineering Schemas (Akış Şemaları)

### Query 1: "Bugün hava soğuk, ne giymeliyim?"

#### Akış Şeması:
```
1. [INPUT] User Query Reception
   ↓
2. [NLU-PREPROCESS] Text Cleaning & Language Detection
   ↓ 
3. [NLU-INTENT] Intent Classification → "weather_based_outfit"
   ↓
4. [NLU-ENTITY] Entity Extraction → {weather: "soğuk", time: "bugün"}
   ↓
5. [CONTEXT-GATHER] External Context Collection
   ↓ ┌─[WEATHER-API] Current weather data
   ↓ ├─[STYLE-PROFILE-8003] User style preferences
   ↓ └─[WARDROBE-DATA] Available clothing items
   ↓
6. [CONTEXT-FUSION] Context Integration & Analysis
   ↓
7. [PROMPT-GENERATION] Service-specific prompts
   ↓
8. [SERVICE-ROUTING] Primary: Combination Engine (8004)
   ↓                  Secondary: Style Profile (8003)
   ↓
9. [COMBINATION-ENGINE] Weather-appropriate outfit generation
   ↓
10. [QUALITY-CHECK] Recommendation validation
    ↓
11. [RESPONSE] Structured outfit recommendations
```

#### Service Coordination:
- **Primary Service**: Combination Engine (8004)
- **Data Sources**: Weather API, Style Profile (8003), User Wardrobe
- **Coordination Type**: Sequential with parallel data gathering
- **Fallback**: Generic weather-based recommendations

#### Prompt Engineering:
```python
# Persona Pattern
"Sen soğuk hava uzmanı bir stil danışmanısın..."

# Recipe Pattern  
"1. Mevcut sıcaklığı değerlendir
 2. Katmanlı giyim stratejisi uygula
 3. Fonksiyonel ve şık parçaları birleştir"

# Template Pattern
"Hava: {weather_temp}°C, {weather_condition}
Kullanıcı profili: {user_style}
Mevcut parçalar: {wardrobe_items}
Öneri: {layered_outfit_suggestion}"

# Context & Instruction
"Bugün sıcaklık {temp}°C. Kullanıcı {activity} yapacak.
Katmanlı giyim prensipleri uygulayarak..."
```

### Query 2: "Bu gömlekle ne giyebilirim?"

#### Akış Şeması:
```
1. [INPUT] User Query + Potential Image
   ↓
2. [MODALITY-DETECTION] Text + Image analysis
   ↓ ┌─[NLU-PROCESSING] "single_item_query" intent
   ↓ └─[IMAGE-PROCESSING-8001] Shirt analysis (if image provided)
   ↓
3. [ENTITY-EXTRACTION] → {clothing_item: "gömlek", modifier: "bu"}
   ↓
4. [CONTEXT-ENRICHMENT]
   ↓ ┌─[WARDROBE-SCAN] Find user's shirts
   ↓ ├─[STYLE-ANALYSIS] Shirt style categorization
   ↓ └─[COMPATIBILITY-CHECK] Matching possibilities
   ↓
5. [MULTI-MODAL-FUSION] If image: visual + text analysis
   ↓
6. [COMBINATION-LOGIC] Generate pairing options
   ↓ ┌─[BOTTOM-PAIRING] Pants, skirts, shorts
   ↓ ├─[LAYER-PAIRING] Jackets, cardigans, vests
   ↓ └─[ACCESSORIES] Shoes, bags, jewelry
   ↓
7. [CONTEXT-FILTERING] User preferences + occasion suitability
   ↓
8. [RANKING-ALGORITHM] Score combinations
   ↓
9. [RESPONSE-GENERATION] Top 5 combination suggestions
```

#### Service Coordination:
- **Primary Service**: Combination Engine (8004)
- **Secondary Services**: Image Processing (8001), Style Profile (8003)
- **Multi-Modal Integration**: Text + potential image analysis
- **Coordination Pattern**: Parallel processing with fusion point

#### Prompt Engineering:
```python
# Persona Pattern
"Sen gömlek kombinasyon uzmanısın. Her gömlek tipinin hangi parçalarla 
uyumlu olduğunu biliyorsun..."

# Recipe Pattern
"1. Gömlek tipini ve rengini belirle
 2. Kullanıcının gardıropdan uyumlu alt parçaları filtrele
 3. Stil tutarlılığı kontrolü yap
 4. En uygun 5 kombinasyonu puanla"

# Template Pattern
"Gömlek: {shirt_type} - {shirt_color}
Stil: {shirt_style}
Uyumlu alt parçalar: {compatible_bottoms}
Önerilen kombinler: {ranked_combinations}"

# Context & Instruction
"Kullanıcının {shirt_color} gömlegi var. Bu gömlek {style_category} 
stilinde. Gardırobundaki {available_bottoms} ile hangi kombinasyonlar 
oluşturulabilir? Renk uyumu ve stil tutarlılığı önceliğinde..."
```

### Query 3: "Yarın ofiste çalışacağım, akşam da bir yemekte varım. Uygun bir kombin önerir misin?"

#### Akış Şeması:
```
1. [INPUT] Complex Multi-Context Query
   ↓
2. [COMPLEXITY-ANALYSIS] Multi-occasion detection
   ↓
3. [TEMPORAL-PARSING] 
   ↓ ┌─[TIME-1] "yarın ofiste" → work context
   ↓ └─[TIME-2] "akşam yemekte" → dinner context
   ↓
4. [DUAL-INTENT-PROCESSING]
   ↓ ┌─[INTENT-1] "professional_attire"
   ↓ └─[INTENT-2] "dinner_outfit"
   ↓
5. [ENTITY-EXTRACTION] 
   ↓ → {occasions: ["ofis", "yemek"], time: ["yarın", "akşam"]}
   ↓
6. [CONTEXT-MATRIX] Build dual-context framework
   ↓ ┌─[WORK-CONTEXT] Professional requirements
   ↓ ├─[DINNER-CONTEXT] Social dinner requirements
   ↓ └─[TRANSITION-ANALYSIS] Work-to-dinner transition
   ↓
7. [STRATEGY-SELECTION]
   ↓ ┌─[STRATEGY-A] Single versatile outfit
   ↓ ├─[STRATEGY-B] Core + transformation pieces
   ↓ └─[STRATEGY-C] Complete outfit change
   ↓
8. [COMBINATION-GENERATION] Multi-context solutions
   ↓
9. [TRANSITION-OPTIMIZATION] Minimize change requirements
   ↓
10. [PRACTICAL-VALIDATION] Feasibility check
    ↓
11. [RANKED-RECOMMENDATIONS] Best transition solutions
```

#### Service Coordination:
- **Primary Service**: Combination Engine (8004) 
- **Secondary Services**: Style Profile (8003), Recommendation Engine (8005)
- **Coordination Type**: Complex sequential with multiple context processing
- **Special Logic**: Transition planning and dual-occasion optimization

#### Prompt Engineering:
```python
# Persona Pattern
"Sen kariyerli profesyonellerin stil danışmanısın. İş ve sosyal yaşam 
arasındaki geçişlerde optimal çözümler sunuyorsun..."

# Recipe Pattern
"1. Her iki occasion için requirements belirle
 2. Ortak stil elements tespit et
 3. Transition-friendly parçaları seç
 4. Minimal değişiklik stratejisi oluştur
 5. Hem professional hem elegant çözüm sun"

# Template Pattern
"GÜN PROGRAMI:
Sabah-Öğlen: {work_context}
Akşam: {dinner_context}

TEMEL KOMBIN: {core_outfit}
İŞ İÇİN: {work_accessories}
YEMEK İÇİN: {dinner_additions}

GEÇİŞ STRATEJİSİ: {transition_plan}"

# Context & Instruction
"Kullanıcının yarın çifte program var: ofis çalışması + akşam yemeği. 
İki etkinlik için de uygun, aralarında kolay geçiş yapabileceği bir 
kombina ihtiyaç var. Ofis dress code: business casual. 
Yemek: nice restaurant. Transition time: 30 dakika..."
```

### Query 4: "Siyah bir elbise arıyorum, öneri var mı?"

#### Akış Şeması:
```
1. [INPUT] Shopping Assistance Query
   ↓
2. [INTENT-CLASSIFICATION] → "shopping_assistance"
   ↓
3. [PRODUCT-ENTITY-EXTRACTION] 
   ↓ → {product: "elbise", color: "siyah", intent: "arıyorum"}
   ↓
4. [SHOPPING-CONTEXT-ANALYSIS]
   ↓ ┌─[PURPOSE-ANALYSIS] Dress occasion inference
   ↓ ├─[BUDGET-DETECTION] Price range hints
   ↓ └─[URGENCY-ASSESSMENT] Timeline requirements
   ↓
5. [USER-PROFILE-INTEGRATION]
   ↓ ┌─[STYLE-PREFERENCES] Personal style alignment
   ↓ ├─[SIZE-INFO] Measurement data
   ↓ ├─[PREVIOUS-PURCHASES] Purchase history
   ↓ └─[BRAND-PREFERENCES] Preferred retailers
   ↓
6. [RECOMMENDATION-ENGINE-8005] Product search & filtering
   ↓
7. [PRODUCT-CATEGORIZATION]
   ↓ ┌─[OCCASION-BASED] Work, casual, formal, party
   ↓ ├─[STYLE-BASED] A-line, bodycon, maxi, midi
   ↓ └─[PRICE-BASED] Budget, mid-range, luxury
   ↓
8. [AVAILABILITY-CHECK] Stock and delivery options
   ↓
9. [PERSONALIZED-RANKING] User-specific scoring
   ↓
10. [COMPREHENSIVE-RECOMMENDATIONS] Product suggestions + styling tips
```

#### Service Coordination:
- **Primary Service**: Recommendation Engine (8005)
- **Supporting Services**: Style Profile (8003), External E-commerce APIs
- **Data Integration**: Product databases, user history, trend data
- **Real-time Elements**: Stock check, pricing, availability

#### Prompt Engineering:
```python
# Persona Pattern
"Sen siyah elbise uzmanı bir personal shopperisn. Her vücut tipine, 
her occasion'a uygun siyah elbise seçeneklerini biliyorsun..."

# Recipe Pattern
"1. Kullanıcının vücut tipini ve stil tercihini analiz et
 2. Occasion ihtiyaçlarını belirle (belirtilmemişse çok amaçlı seç)
 3. Budget range'i tespit et
 4. Mevcut siyah elbise optionlarını filtrele
 5. User preference'lara göre rank et"

# Template Pattern
"ARAMA KRİTERLERİ:
Ürün: {product_type}
Renk: {color}
Stil Tercihi: {user_style}
Beden: {size_info}
Budget: {price_range}

ÖNERİLER:
1. {dress_option_1} - {price} - {occasion_fit}
2. {dress_option_2} - {price} - {occasion_fit}
3. {dress_option_3} - {price} - {occasion_fit}"

# Context & Instruction
"Kullanıcı siyah elbise arıyor. Profil bilgileri: {user_profile}.
Geçmiş alışverişler: {purchase_history}. 
Mevcut gardırop: {current_wardrobe}.
Kişiselleştirilmiş elbise önerileri sun. Her öneri için:
- Neden uygun olduğunu açıkla
- Styling tips ver
- Benzer alternatifler sun
- Fiyat-performans değerlendirmesi yap"
```

## 🔗 Advanced Service Coordination Matrix

### Multi-Service Integration Patterns

```python
SERVICE_COORDINATION_MATRIX = {
    "weather_based_outfit": {
        "primary_flow": [
            {"service": "nlu_service", "port": 8002, "role": "query_analysis"},
            {"service": "weather_api", "external": True, "role": "environmental_context"},
            {"service": "style_profile", "port": 8003, "role": "user_preferences"},
            {"service": "combination_engine", "port": 8004, "role": "outfit_generation"},
            {"service": "multi_modal_coordinator", "port": 8009, "role": "final_coordination"}
        ],
        "fallback_flow": [
            {"service": "recommendation_engine", "port": 8005, "role": "generic_suggestions"}
        ],
        "coordination_type": "sequential_with_parallel_enrichment"
    },
    
    "single_item_query": {
        "primary_flow": [
            {"service": "nlu_service", "port": 8002, "role": "query_analysis"},
            {"service": "image_processing", "port": 8001, "role": "visual_analysis", "conditional": True},
            {"service": "combination_engine", "port": 8004, "role": "pairing_logic"},
            {"service": "style_profile", "port": 8003, "role": "preference_filtering"}
        ],
        "multi_modal_integration": {
            "coordinator": "multi_modal_coordinator",
            "port": 8009,
            "fusion_strategy": "visual_text_fusion"
        },
        "coordination_type": "multi_modal_parallel"
    },
    
    "complex_multi_occasion": {
        "primary_flow": [
            {"service": "nlu_service", "port": 8002, "role": "complex_parsing"},
            {"service": "style_profile", "port": 8003, "role": "lifestyle_analysis"},
            {"service": "combination_engine", "port": 8004, "role": "multi_context_planning"},
            {"service": "orchestrator", "port": 8006, "role": "workflow_coordination"}
        ],
        "coordination_type": "hierarchical_orchestration"
    },
    
    "shopping_assistance": {
        "primary_flow": [
            {"service": "nlu_service", "port": 8002, "role": "shopping_intent_analysis"},
            {"service": "recommendation_engine", "port": 8005, "role": "product_discovery"},
            {"service": "style_profile", "port": 8003, "role": "personalization"},
            {"service": "external_commerce_apis", "external": True, "role": "inventory_check"}
        ],
        "coordination_type": "commerce_optimized"
    }
}
```

## 🎯 Implementation Roadmap

### Phase 1: Core NLU Enhancement (Completed ✅)
- [x] Advanced prompt engineering patterns
- [x] Multi-modal query support
- [x] Context fusion algorithms
- [x] Service coordination matrix

### Phase 2: Advanced Features (In Progress 🔄)
- [ ] Dynamic prompt optimization
- [ ] Learning-based intent refinement
- [ ] Multi-language support expansion
- [ ] Real-time context adaptation

### Phase 3: AI Enhancement (Planned 📋)
- [ ] Transformer-based intent classification
- [ ] Contextual embedding models
- [ ] Personalized prompt generation
- [ ] Predictive query understanding

### Phase 4: Production Optimization (Future 🚀)
- [ ] Performance optimization (<500ms response)
- [ ] Scalability enhancements
- [ ] A/B testing framework
- [ ] Advanced analytics integration

## 🏆 Success Metrics

### Accuracy Metrics
- **Intent Classification Accuracy**: >95%
- **Entity Extraction Precision**: >90%
- **Context Relevance Score**: >85%
- **Service Routing Accuracy**: >98%

### Performance Metrics
- **Query Processing Time**: <800ms
- **Multi-Modal Fusion Time**: <1200ms
- **Service Coordination Latency**: <300ms
- **End-to-End Response Time**: <2000ms

### User Experience Metrics
- **Query Understanding Rate**: >92%
- **Successful Task Completion**: >88%
- **User Satisfaction Score**: >4.2/5
- **Personalization Effectiveness**: >80%

---

*AURA AI NLU Service - Advanced Prompt Engineering Framework v2.0*
*Implementation Date: August 5, 2025*
*Status: ✅ PRODUCTION READY with Multi-Modal Integration*
