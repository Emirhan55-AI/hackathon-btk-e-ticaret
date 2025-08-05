# 🎯 AURA AI - Çok Modlu Sorgu Desteği Sistemi Tasarımı
*Çok Modlu AI Koordinatörü - Görsel + Metin Entegrasyonu*

## 📋 Sistem Genel Bakış

AURA AI sistemine **Multi-Modal Query Coordinator** servisi (Port 8009) eklenerek, kullanıcıların görsel ve metin verilerini birlikte kullanarak sorgu yapabilmelerini sağlayacağız.

### 🏗️ Yeni Servis Mimarisi
```
🎯 Multi-Modal Query Coordinator (Port 8009)
├── 📸 Görsel İşleme Modülü (CLIP Entegrasyonu)
├── 🧠 Metin Analizi Modülü (NLU Entegrasyonu)
├── 🔄 Koordinasyon Motoru
├── 📊 Context Fusion Engine
└── 🎨 Response Generation Engine
```

## 🎭 Prompt Kalıpları Metodolojisi

### 1. Persona Kalıbı - Çok Modlu AI Koordinatörü
```
Sen AURA AI sisteminin Çok Modlu Sorgu Koordinatörüsün. 
Kullanıcılardan gelen görsel ve metin verilerini entegre ederek, 
moda ve stil konularında akıllı öneriler üretirsin. 
Görsel analiz yeteneklerin ve doğal dil anlama becerilerini 
birleştirerek kullanıcı deneyimini optimize edersin.
```

### 2. Tarif Kalıbı - Adım Adım İşlem
```
Çok Modlu Sorgu İşleme Tarifi:
1. Kullanıcıdan gelen görsel ve metin verilerini al
2. Görseli CLIP modeli ile analiz et (etiket, renk, stil)
3. Metni NLU servisi ile analiz et (intent, entity, context)
4. Görsel ve metin analizlerini birleştir
5. Kullanıcının gardırop verilerini kontrol et
6. Combination Engine ile uyumlu öneriler üret
7. Kişiselleştirilmiş yanıt hazırla
8. Kullanıcıya çok modlu yanıt sun
```

### 3. Şablon Kalıbı - Yapılandırılmış Format
```
MULTI_MODAL_QUERY_TEMPLATE = {
    "görsel_data": {
        "url": "[IMAGE_URL]",
        "analiz": "[CLIP_ANALYSIS]",
        "etiketler": "[VISUAL_TAGS]",
        "renk_paleti": "[COLOR_PALETTE]",
        "stil_kategori": "[STYLE_CATEGORY]"
    },
    "metin_data": {
        "sorgu": "[USER_TEXT]",
        "intent": "[EXTRACTED_INTENT]",
        "entities": "[EXTRACTED_ENTITIES]",
        "bağlam": "[CONTEXT_INFO]"
    },
    "fusion_result": {
        "birleştirilmiş_anlam": "[FUSED_MEANING]",
        "öneri_tipi": "[RECOMMENDATION_TYPE]",
        "güven_skoru": "[CONFIDENCE_SCORE]"
    },
    "yanıt": {
        "öneriler": "[RECOMMENDATIONS]",
        "açıklamalar": "[EXPLANATIONS]",
        "görsel_referanslar": "[VISUAL_REFS]"
    }
}
```

### 4. Bağlam ve Talimat Kalıbı - Kontekstüel Rehberlik
```
BAĞLAM: Kullanıcı "{user_text}" sorusu ile birlikte {item_type} görseli gönderdi.
Görsel analizi: Renk={colors}, Stil={style}, Kategori={category}
Kullanıcı profili: {user_preferences}
Gardırop durumu: {wardrobe_items}

TALİMAT: Bu bağlamda kullanıcıya en uygun kombin önerilerini üret.
Önerilerde görsel uyumu, stil tutarlılığı ve kullanıcı tercihlerini dikkate al.
Yanıtını hem metin hem de görsel referanslarla destekle.
```

## 🔄 Kullanıcı Sorguları ve Akış Şemaları

### Sorgu 1: "Bu gömlekle ne giyebilirim?"

#### 🎭 Prompt Kalıpları Uygulaması

**Persona Kalıbı:**
```
Sen bir moda danışmanı ve stil koordinatörüsün. Kullanıcının gönderdiği 
gömlek görselini analiz ederek, onunla en uyumlu alt parça ve aksesuar 
önerilerini sunacaksın. Renk uyumu, stil tutarlılığı ve modern moda 
trendlerini göz önünde bulundurarak öneriler yapacaksın.
```

**Tarif Kalıbı:**
```
Gömlek Kombin Önerisi Süreci:
1. Gömlek görselini al ve CLIP ile analiz et
2. "ne giyebilirim" metnini NLU ile analiz et
3. Gömleğin rengini, stilini ve özelliklerini belirle
4. Kullanıcının gardırobundan uyumlu alt parçaları filtrele
5. Renk teorisi kurallarına göre uyumlu kombinler oluştur
6. Stil tutarlılığını kontrol et (formal/casual uyumu)
7. En iyi 3-5 kombin önerisini hazırla
8. Her öneri için açıklama ve stil ipuçları ekle
```

**Şablon Kalıbı:**
```
Gömlek Analizi:
- Renk: [SHIRT_COLOR]
- Stil: [SHIRT_STYLE] (formal/casual/business)
- Desen: [PATTERN_TYPE]
- Yakalık: [COLLAR_TYPE]

Öneri Format:
- Alt Parça: [BOTTOM_RECOMMENDATION]
- Renk Uyumu: [COLOR_HARMONY_EXPLANATION]
- Stil Uyumu: [STYLE_COMPATIBILITY]
- Aksesuar Önerileri: [ACCESSORY_SUGGESTIONS]
- Ayakkabı Önerisi: [SHOE_RECOMMENDATION]
```

#### 📊 Akış Şeması
```
1. 📸 Görsel Alımı
   └── Kullanıcıdan gömlek görseli
   
2. 🧠 CLIP Görsel Analizi
   ├── Gömlek tipi belirleme (formal/casual/business)
   ├── Renk paleti çıkarımı
   ├── Desen analizi (düz/çizgili/desenli)
   └── Kumaş dokusuna yönelik tahmin
   
3. 📝 NLU Metin Analizi
   ├── Intent: "kombin_önerisi_isteme"
   ├── Entity: "gömlek", "ne_giyebilirim"
   └── Context: "alt_parça_arayışı"
   
4. 🔄 Bilgi Birleştirme
   ├── Görsel + Metin verisi füzyonu
   ├── Kullanıcı profili entegrasyonu
   └── Gardırop inventarı kontrolü
   
5. 🎨 Combination Engine Koordinasyonu
   ├── Uyumlu alt parça filtreleme
   ├── Renk uyumu hesaplama
   ├── Stil tutarlılığı kontrolü
   └── Sezon uygunluğu değerlendirmesi
   
6. 💡 Öneri Üretimi
   ├── En iyi 3-5 kombin seçimi
   ├── Her kombin için açıklama
   ├── Görsel referans ekleme
   └── Stil ipuçları ekleme
   
7. 📱 Yanıt Sunumu
   ├── Çok modlu yanıt hazırlama
   ├── Görsel ve metin entegrasyonu
   └── Kullanıcıya sunma
```

#### 🔗 Servisler Arası Koordinasyon
```
Multi-Modal Coordinator (8009) →
├── Image Processing (8001): Gömlek analizi
├── NLU Service (8002): Metin intent analizi  
├── Style Profile (8003): Kullanıcı tercihleri
├── Combination Engine (8004): Kombin önerileri
├── Recommendation Engine (8005): Kişiselleştirme
└── Quality Assurance (8008): Kalite kontrolü
```

---

### Sorgu 2: "Bu elbiseye uygun ayakkabı var mı?"

#### 🎭 Prompt Kalıpları Uygulaması

**Persona Kalıbı:**
```
Sen bir ayakkabı ve aksesuar uzmanısın. Kullanıcının gönderdiği elbise 
görselini analiz ederek, onunla perfect uyum sağlayacak ayakkabı 
önerilerini sunacaksın. Elbiseninormal durumu, rengi, stili ve 
topuklu/düz tercihlerini göz önünde bulundurarak öneriler yapacaksın.
```

**Tarif Kalıbı:**
```
Elbise-Ayakkabı Uyumu Süreci:
1. Elbise görselini CLIP ile detaylı analiz et
2. "ayakkabı var mı" sorgusunu NLU ile anlat
3. Elbisenin formal/casual düzeyini belirle
4. Renk paleti ve stil kategorisini çıkar
5. Kullanıcının ayakkabı koleksiyonunu kontrol et
6. Uygun ayakkabı alternatiflerini filtrele
7. Boy-kilo oranına uygun topuk önerisi yap
8. Her öneri için stil gerekçesi sun
```

**Şablon Kalıbı:**
```
Elbise Profili:
- Tip: [DRESS_TYPE] (midi/maxi/mini/kokteyl)
- Renk: [DRESS_COLOR]
- Stil: [STYLE_LEVEL] (çok formal/formal/smart casual/casual)
- Kumaş: [FABRIC_TYPE]
- Ocasyon: [SUITABLE_OCCASION]

Ayakkabı Önerisi:
- Tip: [SHOE_TYPE] (stiletto/block heel/flat/sneaker)
- Renk: [RECOMMENDED_COLOR]
- Topuk Yüksekliği: [HEEL_HEIGHT]
- Uyum Skoru: [COMPATIBILITY_SCORE]
- Stil Gerekçesi: [STYLE_REASONING]
```

#### 📊 Akış Şeması
```
1. 📸 Elbise Görseli Alımı
   └── Yüksek çözünürlük elbise fotoğrafı
   
2. 🧠 CLIP Elbise Analizi
   ├── Elbise tipi sınıflandırması
   ├── Uzunluk analizi (mini/midi/maxi)
   ├── Renk dominantlığı çıkarımı
   ├── Formal/casual seviye belirleme
   └── Kumaş dokusu tahmini
   
3. 📝 NLU Sorgu Analizi
   ├── Intent: "ayakkabı_uyumu_sorgulama"
   ├── Entity: "elbise", "ayakkabı", "uygun"
   └── Context: "mevcut_koleksiyon_kontrolü"
   
4. 👤 Kullanıcı Profili Entegrasyonu
   ├── Ayakkabı tercihleri (topuklu/düz)
   ├── Boy-kilo bilgisi (topuk yüksekliği için)
   ├── Stil tercihleri profili
   └── Rahatlık vs. şıklık dengesi
   
5. 👠 Ayakkabı Koleksiyonu Analizi
   ├── Mevcut ayakkabı envanteri tarama
   ├── Renk uyumu hesaplama
   ├── Stil uyumu değerlendirme
   └── Ocasyon uygunluğu kontrolü
   
6. 🎯 Uyum Skorlama
   ├── Renk uyumu (0-100)
   ├── Stil uyumu (0-100)
   ├── Ocasyon uyumu (0-100)
   └── Toplam uyum skoru hesaplama
   
7. 💡 Öneri Üretimi
   ├── En uygun 3-5 ayakkabı seçimi
   ├── Yoksa alternatif öneriler
   ├── Satın alma tavsiyeleri
   └── Stil açıklamaları
   
8. 📱 Görsel Yanıt
   ├── Elbise + Ayakkabı görsel kombinasyonu
   ├── Renk uyumu gösterimi
   └── Stil ipuçları ekleme
```

#### 🔗 Servisler Arası Koordinasyon
```
Multi-Modal Coordinator (8009) →
├── Image Processing (8001): Elbise detay analizi
├── NLU Service (8002): Sorgu intent çıkarımı
├── Style Profile (8003): Ayakkabı tercihleri + boy bilgisi
├── Combination Engine (8004): Elbise-ayakkabı uyumu
├── Recommendation Engine (8005): Eksik ayakkabı önerileri
└── Quality Assurance (8008): Öneri kalite kontrolü
```

---

### Sorgu 3: "Bu pantolonla hangi ceketi önerirsin?"

#### 🎭 Prompt Kalıpları Uygulaması

**Persona Kalıbı:**
```
Sen bir erkek ve kadın üst giyim uzmanısın. Kullanıcının gönderdiği 
pantolon görselini analiz ederek, onunla mükemmel uyum sağlayacak 
ceket önerilerini sunacaksın. Pantolonun kesimi, rengi, kumaşı ve 
formallik düzeyini analiz ederek uygun ceket alternatiflerini 
önerecekin.
```

**Tarif Kalıbı:**
```
Pantolon-Ceket Uyumu Süreci:
1. Pantolon görselini CLIP ile kapsamlı analiz et
2. "hangi ceketi önerirsin" sorgusunu NLU ile çözümle
3. Pantolonun kesim tipini ve formallik düzeyini belirle
4. Renk paleti ve desen analizini yap
5. Uyumlu ceket tiplerini kategorize et
6. Kullanıcının ceket koleksiyonunu tara
7. Sezon ve ocasyon uygunluğunu değerlendir
8. En uygun 3-5 ceket önerisini detaylandır
```

**Şablon Kalıbı:**
```
Pantolon Analizi:
- Tip: [PANTS_TYPE] (chino/jean/kumaş/takım)
- Kesim: [CUT_TYPE] (slim/regular/wide leg)
- Renk: [PANTS_COLOR]
- Formal Düzey: [FORMALITY_LEVEL]
- Kumaş: [FABRIC_TYPE]

Ceket Önerisi:
- Tip: [JACKET_TYPE] (blazer/bomber/denim/sport)
- Renk Önerisi: [RECOMMENDED_COLOR]
- Stil Uyumu: [STYLE_MATCH_REASON]
- Ocasyon: [SUITABLE_OCCASION]
- Uyum Skoru: [COMPATIBILITY_SCORE]
```

#### 📊 Akış Şeması
```
1. 📸 Pantolon Görseli Alımı
   └── Detaylı pantolon fotoğrafı
   
2. 🧠 CLIP Pantolon Analizi
   ├── Pantolon tipi sınıflandırması
   ├── Kesim analizi (slim/regular/wide)
   ├── Renk ve desen çıkarımı
   ├── Kumaş tipi tahmini
   └── Formallik düzeyi belirleme
   
3. 📝 NLU Ceket Sorgusu Analizi
   ├── Intent: "ceket_önerisi_isteme"
   ├── Entity: "pantolon", "ceket", "öner"
   └── Context: "üst_giyim_kombinasyonu"
   
4. 👤 Stil Profili Kontrolü
   ├── Kullanıcının ceket tercihleri
   ├── Formal/casual denge tercihi
   ├── Renk kombinasyon geçmişi
   └── Mevsimsel tercihler
   
5. 🧥 Ceket Koleksiyonu Tarama
   ├── Mevcut ceket envanteri
   ├── Pantolon-ceket uyum matrisi
   ├── Renk uyumu hesaplama
   └── Stil kategorisi eşleştirme
   
6. 🎨 Combination Engine İşlemi
   ├── Klasik kombinasyon kuralları
   ├── Modern trend entegrasyonu
   ├── Renk teorisi uygulaması
   └── Proportion balansı kontrolü
   
7. 📊 Skorlama ve Sıralama
   ├── Stil uyumu (0-100)
   ├── Renk uyumu (0-100)
   ├── Ocasyon uygunluğu (0-100)
   ├── Trend uyumluluğu (0-100)
   └── Toplam skor hesaplama
   
8. 💡 Ceket Önerisi Üretimi
   ├── Top 3-5 ceket seçimi
   ├── Her öneri için detaylı açıklama
   ├── Alternatif styling ipuçları
   └── Eksik parça önerileri
   
9. 📱 Görsel Sunum
   ├── Pantolon + Ceket görsel kombinasyonu
   ├── Farklı açılardan görüntü
   └── Stil ipuçları overlayı
```

#### 🔗 Servisler Arası Koordinasyon
```
Multi-Modal Coordinator (8009) →
├── Image Processing (8001): Pantolon detay analizi
├── NLU Service (8002): Ceket sorgusu analizi
├── Style Profile (8003): Üst giyim tercihleri
├── Combination Engine (8004): Pantolon-ceket uyum hesabı
├── Recommendation Engine (8005): Trend bazlı öneriler
└── Quality Assurance (8008): Kombinasyon kalite kontrolü
```

---

### Sorgu 4: "Bu çantayla ne kombin olur?"

#### 🎭 Prompt Kalıpları Uygulaması

**Persona Kalıbı:**
```
Sen bir aksesuar ve kombin uzmanısın. Kullanıcının gönderdiği çanta 
görselini merkeze alarak, onunla perfect uyum sağlayacak tam bir 
outfit önerisi sunacaksın. Çantanın stilini, rengini, boyutunu ve 
formallik düzeyini analiz ederek komple bir look hazırlayacaksın.
```

**Tarif Kalıbı:**
```
Çanta Merkezli Kombin Süreci:
1. Çanta görselini CLIP ile detaylı analiz et
2. "ne kombin olur" sorgusunu NLU ile anlamlandır
3. Çantanın stil kategorisini ve ocasyon uygunluğunu belirle
4. Çanta rengi ile uyumlu color palette oluştur
5. Çantanın formality level'ına uygun giyim parçalarını filtrele
6. Head-to-toe kombin önerisi hazırla
7. Çanta ile tüm parçaların uyumunu doğrula
8. Alternatif styling seçenekleri sun
```

**Şablon Kalıbı:**
```
Çanta Profili:
- Tip: [BAG_TYPE] (tote/clutch/crossbody/backpack)
- Boyut: [SIZE_CATEGORY] (mini/small/medium/large)
- Renk: [BAG_COLOR]
- Stil: [STYLE_CATEGORY] (casual/formal/sport/bohemian)
- Malzeme: [MATERIAL_TYPE] (leather/fabric/synthetic)

Kombin Önerisi:
- Ana Parça: [MAIN_GARMENT]
- Alt Parça: [BOTTOM_PIECE]
- Ayakkabı: [SHOE_CHOICE]
- Aksesuar: [ADDITIONAL_ACCESSORIES]
- Toplam Look: [OVERALL_STYLE_DESCRIPTION]
```

#### 📊 Akış Şeması
```
1. 📸 Çanta Görseli Alımı
   └── Yüksek kalite çanta fotoğrafı
   
2. 🧠 CLIP Çanta Analizi
   ├── Çanta tipi sınıflandırması
   ├── Boyut kategorisi belirleme
   ├── Renk dominantlığı çıkarımı
   ├── Malzeme tipi tahmini
   ├── Handle/strap tip analizi
   └── Formallik düzeyi belirleme
   
3. 📝 NLU Kombin Sorgusu Analizi
   ├── Intent: "komple_kombin_isteme"
   ├── Entity: "çanta", "kombin", "ne_olur"
   └── Context: "çanta_merkezli_styling"
   
4. 🎨 Renk Paleti Oluşturma
   ├── Çanta ana rengi extraction
   ├── Uyumlu renk kombinasyonları
   ├── Kontrast ve complement analizi
   └── Sezon uygunluğu kontrolü
   
5. 👤 Kullanıcı Profili Entegrasyonu
   ├── Stil tercihleri analizi
   ├── Vücut tipi ve proportion tercihleri
   ├── Lifestyle ve occasion pattern'leri
   └── Renk kombinasyon geçmişi
   
6. 🎯 Ocasyon Belirleme
   ├── Çanta stilinden ocasyon çıkarımı
   ├── Formal/casual/sport kategorilendirme
   ├── Gündüz/gece uygunluk analizi
   └── Mevsim faktörü entegrasyonu
   
7. 🎨 Kombin Motoru Koordinasyonu
   ├── Ana giyim parçası seçimi
   ├── Alt parça uyum hesaplaması
   ├── Ayakkabı-çanta uyum analizi
   ├── Aksesuar dengeleme
   └── Toplam look tutarlılığı
   
8. 💡 Head-to-Toe Öneri Üretimi
   ├── 3-5 komple outfit alternatifi
   ├── Her look için detaylı açıklama
   ├── Çanta'nın outfit'teki rolü
   ├── Alternative styling options
   └── Shopping recommendations
   
9. 📱 Çok Modlu Sunum
   ├── Çanta + outfit görsel kombinasyonu
   ├── 360° styling perspektifi
   ├── Renk uyumu gösterimi
   └── İnteraktif stil ipuçları
```

#### 🔗 Servisler Arası Koordinasyon
```
Multi-Modal Coordinator (8009) →
├── Image Processing (8001): Çanta detay analizi + renk extraction
├── NLU Service (8002): Kombin sorgusu intent analizi
├── Style Profile (8003): Kullanıcı stil profili + ocasyon tercihleri
├── Combination Engine (8004): Çanta-merkezli komple outfit hesabı
├── Recommendation Engine (8005): Kişiselleştirilmiş alternatifler
└── Quality Assurance (8008): Outfit tutarlılığı ve kalite kontrolü
```

## 🔄 Multi-Modal Coordinator Servisi Teknik Tasarım

### 🏗️ Servis Mimarisi
```python
# Multi-Modal Query Coordinator Service (Port 8009)

class MultiModalCoordinator:
    def __init__(self):
        self.clip_processor = CLIPImageProcessor()
        self.nlu_client = NLUServiceClient()
        self.fusion_engine = ContextFusionEngine()
        self.response_generator = MultiModalResponseGenerator()
        
    async def process_multimodal_query(self, image_data, text_query, user_context):
        # 1. Paralel işleme başlat
        image_task = self.analyze_image(image_data)
        text_task = self.analyze_text(text_query)
        
        # 2. Sonuçları bekle ve birleştir
        image_result, text_result = await asyncio.gather(image_task, text_task)
        
        # 3. Context fusion
        fused_context = self.fusion_engine.fuse(image_result, text_result, user_context)
        
        # 4. Service koordinasyonu
        recommendations = await self.coordinate_services(fused_context)
        
        # 5. Multi-modal response generation
        response = await self.response_generator.generate(recommendations, fused_context)
        
        return response
```

### 📊 Context Fusion Engine
```python
class ContextFusionEngine:
    def fuse(self, image_analysis, text_analysis, user_context):
        """
        Görsel ve metin analizlerini birleştirerek unified context oluşturur
        """
        return {
            "visual_context": {
                "item_type": image_analysis.item_type,
                "colors": image_analysis.color_palette,
                "style": image_analysis.style_category,
                "formality": image_analysis.formality_level
            },
            "textual_context": {
                "intent": text_analysis.intent,
                "entities": text_analysis.entities,
                "context": text_analysis.context,
                "preference_indicators": text_analysis.preferences
            },
            "user_context": user_context,
            "fusion_confidence": self.calculate_fusion_confidence(),
            "recommendation_type": self.determine_recommendation_type()
        }
```

### 🎯 Service Koordinasyon Matrisi
```
Query Type          | Primary Services              | Secondary Services
=================== | ============================= | =========================
Gömlek + Kombin     | Image(8001) + Combination(8004) | Style(8003) + QA(8008)
Elbise + Ayakkabı   | Image(8001) + Style(8003)       | Combination(8004) + Rec(8005)  
Pantolon + Ceket    | Image(8001) + Combination(8004) | Style(8003) + QA(8008)
Çanta + Kombin      | Image(8001) + Combination(8004) | All Services (full coordination)
```

## 📈 Başarı Metrikleri

### Sistem Performansı
- **Görsel Analiz Süresi**: < 2 saniye (CLIP processing)
- **Metin Analiz Süresi**: < 500ms (NLU processing)  
- **Context Fusion Süresi**: < 300ms
- **Toplam Response Süresi**: < 5 saniye
- **Çok Modlu Doğruluk**: > 85%

### Kullanıcı Deneyimi
- **Intent Accuracy**: > 90% (metin anlama)
- **Visual Classification**: > 88% (görsel sınıflandırma)
- **Recommendation Relevance**: > 85% (öneri kalitesi)
- **User Satisfaction**: > 8.5/10 (kullanıcı memnuniyeti)

## 🚀 Implementation Roadmap

### Phase 1: Core Infrastructure (Hafta 1-2)
- Multi-Modal Coordinator servisi geliştirme
- CLIP entegrasyonu ve görsel analiz pipeline'ı
- NLU servisi ile text analysis entegrasyonu
- Context Fusion Engine implementasyonu

### Phase 2: Service Integration (Hafta 3)
- Mevcut AURA servisleri ile koordinasyon
- API endpoint'leri ve request/response formatları
- Error handling ve fallback mechanisms
- Performance optimization

### Phase 3: Testing & Validation (Hafta 4)
- Unit testing ve integration testing
- User acceptance testing
- Performance benchmarking
- Quality assurance validation

### Phase 4: Deployment & Monitoring (Hafta 5)
- Production deployment
- Monitoring ve analytics setup
- User feedback collection
- Continuous improvement cycle

Bu çok modlu sorgu desteği sistemi, AURA AI'nın kullanıcı deneyimini önemli ölçüde artırarak, kullanıcıların daha doğal ve sezgisel bir şekilde moda önerileri almasını sağlayacaktır.
