# 🎯 Multi-Modal Coordinator Service - Core Engine Implementation
# AURA AI Çok Modlu Sorgu Desteği Sistemi

"""
Multi-Modal Query Coordinator - Ana Engine

Bu modül AURA AI sisteminin çok modlu sorgu işleme yeteneklerini sağlar.
Kullanıcılardan gelen görsel ve metin verilerini entegre ederek,
akıllı moda önerileri üretir.

Özellikler:
- CLIP tabanlı görsel analiz
- NLU tabanlı metin analizi  
- Context fusion ve semantic integration
- Multi-service coordination
- Real-time response generation
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import base64
import io
from PIL import Image
import numpy as np

# FastAPI ve Pydantic imports
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, Field
import httpx

# Logging configuration - Her satırda açıklama yaparak takip edilebilirlik sağlıyoruz
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("multi_modal_coordinator")

class QueryType(Enum):
    """Çok modlu sorgu tiplerini tanımlayan enum sınıfı"""
    SHIRT_COMBINATION = "shirt_combination"          # Gömlek kombin sorguları
    DRESS_SHOE_MATCHING = "dress_shoe_matching"      # Elbise ayakkabı uyumu
    PANTS_JACKET_PAIRING = "pants_jacket_pairing"    # Pantolon ceket kombinasyonu
    BAG_OUTFIT_STYLING = "bag_outfit_styling"        # Çanta merkezli styling
    GENERAL_STYLING = "general_styling"              # Genel styling sorguları

class FormalityLevel(Enum):
    """Giyim parçalarının formallik düzeylerini tanımlayan enum"""
    VERY_CASUAL = "very_casual"      # Çok rahat (spor, ev)
    CASUAL = "casual"                # Günlük (arkadaş buluşması, alışveriş)
    SMART_CASUAL = "smart_casual"    # Şık günlük (iş yemeği, sosyal etkinlik)
    BUSINESS = "business"            # İş (ofis, toplantı)
    FORMAL = "formal"                # Resmi (özel davet, tiyatro)
    BLACK_TIE = "black_tie"          # Çok resmi (gala, kokteyl)

@dataclass
class ImageAnalysisResult:
    """Görsel analiz sonuçlarını tutan veri sınıfı"""
    item_type: str                    # Giyim parçası tipi (gömlek, pantolon vb.)
    color_palette: List[str]          # Renk paleti listesi
    dominant_color: str               # Baskın renk
    style_category: str               # Stil kategorisi (casual, formal vb.)
    formality_level: FormalityLevel   # Formallik düzeyi
    fabric_type: Optional[str]        # Kumaş tipi tahmini
    pattern_type: str                 # Desen tipi (düz, çizgili, desenli)
    confidence_score: float           # Analiz güven skoru (0-1)
    detailed_features: Dict[str, Any] # Detaylı özellikler sözlüğü
    processing_time_ms: float        # İşlem süresi (milisaniye)

@dataclass  
class TextAnalysisResult:
    """Metin analiz sonuçlarını tutan veri sınıfı"""
    intent: str                       # Kullanıcı niyeti (kombin_isteme, uyum_sorgulama vb.)
    entities: List[str]               # Çıkarılan varlıklar (gömlek, ayakkabı vb.)
    context_markers: List[str]        # Bağlam belirteçleri (renk, stil, ocasyon)
    preference_indicators: List[str]  # Tercih göstergeleri
    query_type: QueryType            # Sorgu tipi kategorizasyonu
    confidence_score: float          # Analiz güven skoru (0-1)
    sentiment: str                    # Duygu durumu (positive, neutral, negative)
    urgency_level: str               # Aciliyet düzeyi (low, medium, high)
    processing_time_ms: float        # İşlem süresi (milisaniye)

@dataclass
class FusedContext:
    """Görsel ve metin analizlerinin birleştirilmiş bağlamını tutan sınıf"""
    visual_context: ImageAnalysisResult      # Görsel analiz sonucu
    textual_context: TextAnalysisResult     # Metin analiz sonucu
    user_profile: Dict[str, Any]            # Kullanıcı profil bilgileri
    unified_intent: str                     # Birleştirilmiş kullanıcı niyeti
    recommendation_type: str                # Öneri tipi
    fusion_confidence: float                # Birleştirme güven skoru
    contextual_priorities: List[str]        # Bağlamsal öncelikler
    processing_metadata: Dict[str, Any]     # İşleme metadata'sı

class CLIPImageProcessor:
    """CLIP modeli tabanlı görsel analiz işlemcisi"""
    
    def __init__(self):
        """CLIPImageProcessor sınıfını başlatır ve gerekli model yüklemelerini yapar"""
        logger.info("🎨 CLIP Image Processor initializing...")
        # Gerçek implementasyonda burada CLIP model yükleme işlemi olacak
        # Şimdilik mock implementation kullanıyoruz
        self.model_loaded = True
        self.supported_formats = ['JPEG', 'PNG', 'JPG', 'WEBP']
        logger.info("✅ CLIP Image Processor initialized successfully")
    
    async def analyze_image(self, image_data: bytes, query_context: str = "") -> ImageAnalysisResult:
        """
        Görsel analizi gerçekleştiren ana metod
        
        Args:
            image_data: Görsel verisi (bytes formatında)
            query_context: Sorgu bağlamı (opsiyonel)
            
        Returns:
            ImageAnalysisResult: Detaylı görsel analiz sonucu
        """
        start_time = datetime.now()
        logger.info(f"🔍 Starting image analysis with context: {query_context}")
        
        try:
            # Görseli PIL Image objesine dönüştür
            image = Image.open(io.BytesIO(image_data))
            
            # Görsel format kontrolü
            if image.format not in self.supported_formats:
                raise ValueError(f"Unsupported image format: {image.format}")
            
            # Görsel boyut ve kalite kontrolü
            width, height = image.size
            logger.info(f"📐 Image dimensions: {width}x{height}")
            
            # Mock CLIP analysis - Gerçek implementasyonda CLIP model inference olacak
            analysis_result = await self._mock_clip_analysis(image, query_context)
            
            # İşlem süresini hesapla
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            analysis_result.processing_time_ms = processing_time
            
            logger.info(f"✅ Image analysis completed in {processing_time:.2f}ms")
            logger.info(f"🏷️ Detected item: {analysis_result.item_type} with {analysis_result.confidence_score:.2f} confidence")
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"❌ Image analysis failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Image analysis failed: {str(e)}")
    
    async def _mock_clip_analysis(self, image: Image, context: str) -> ImageAnalysisResult:
        """
        Mock CLIP analizi - Gerçek implementasyon için placeholder
        Gerçek projede burada CLIP model inference yapılacak
        """
        # Simulated processing delay - gerçek model inference süresini simüle eder
        await asyncio.sleep(0.1)
        
        # Context'e göre farklı sonuçlar döner (akıllı mock)
        if "gömlek" in context.lower() or "shirt" in context.lower():
            return ImageAnalysisResult(
                item_type="gömlek",
                color_palette=["mavi", "beyaz"],
                dominant_color="mavi",
                style_category="business_casual",
                formality_level=FormalityLevel.BUSINESS,
                fabric_type="pamuk",
                pattern_type="düz",
                confidence_score=0.92,
                detailed_features={
                    "collar_type": "klasik",
                    "sleeve_length": "uzun",
                    "fit_type": "slim",
                    "button_style": "standart"
                },
                processing_time_ms=0.0  # Gerçek süre sonradan set edilecek
            )
        elif "elbise" in context.lower() or "dress" in context.lower():
            return ImageAnalysisResult(
                item_type="elbise",
                color_palette=["siyah", "gümüş"],
                dominant_color="siyah",
                style_category="formal",
                formality_level=FormalityLevel.FORMAL,
                fabric_type="polyester",
                pattern_type="düz",
                confidence_score=0.89,
                detailed_features={
                    "dress_length": "midi",
                    "neckline": "V_neck",
                    "fit_type": "A_line",
                    "occasion_suitability": "evening"
                },
                processing_time_ms=0.0
            )
        else:
            # Genel analiz sonucu
            return ImageAnalysisResult(
                item_type="giyim_parçası",
                color_palette=["belirtilmemiş"],
                dominant_color="belirtilmemiş",
                style_category="genel",
                formality_level=FormalityLevel.CASUAL,
                fabric_type="belirtilmemiş",
                pattern_type="belirtilmemiş",
                confidence_score=0.75,
                detailed_features={},
                processing_time_ms=0.0
            )

class NLUTextProcessor:
    """Natural Language Understanding tabanlı metin analiz işlemcisi"""
    
    def __init__(self):
        """NLUTextProcessor sınıfını başlatır ve NLU servis bağlantısını kurar"""
        logger.info("🧠 NLU Text Processor initializing...")
        self.nlu_service_url = "http://localhost:8002"  # NLU Service endpoint
        self.client = httpx.AsyncClient(timeout=10.0)
        logger.info("✅ NLU Text Processor initialized successfully")
    
    async def analyze_text(self, text_query: str, image_context: str = "") -> TextAnalysisResult:
        """
        Metin analizi gerçekleştiren ana metod
        
        Args:
            text_query: Kullanıcının metin sorgusu
            image_context: Görsel bağlam bilgisi (opsiyonel)
            
        Returns:
            TextAnalysisResult: Detaylı metin analiz sonucu
        """
        start_time = datetime.now()
        logger.info(f"📝 Starting text analysis for query: '{text_query}'")
        
        try:
            # NLU servisine istek gönder
            nlu_request = {
                "text": text_query,
                "context": {"image_context": image_context},
                "analysis_type": "fashion_query"
            }
            
            # Mock NLU analysis - Gerçek implementasyonda NLU service çağrısı olacak
            analysis_result = await self._mock_nlu_analysis(text_query, image_context)
            
            # İşlem süresini hesapla
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            analysis_result.processing_time_ms = processing_time
            
            logger.info(f"✅ Text analysis completed in {processing_time:.2f}ms")
            logger.info(f"🎯 Detected intent: {analysis_result.intent} with {analysis_result.confidence_score:.2f} confidence")
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"❌ Text analysis failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Text analysis failed: {str(e)}")
    
    async def _mock_nlu_analysis(self, text: str, context: str) -> TextAnalysisResult:
        """
        Advanced NLU analysis with Prompt Engineering Patterns
        Implements: Persona, Recipe, Template, and Context & Instruction patterns
        """
        # Simulate realistic processing delay
        await asyncio.sleep(0.08)
        
        logger.info(f"🧠 Advanced NLU analysis starting for: '{text[:50]}...'")
        
        # PERSONA PATTERN: Expert Style Consultant Role
        persona_context = """
        Sen AURA AI'nın uzman stil danışmanısın. 10 yıllık moda endüstrisi deneyimin var.
        Kişiliğin: Kullanıcının kişisel stilini anlayan empatik danışman
        Uzmanlığın: Trend ve klasik stil bilgisi, her vücut tipine uygun öneriler
        """
        
        # RECIPE PATTERN: Step-by-step analysis framework
        analysis_steps = [
            "1. Sorguyu temizle ve normalize et",
            "2. Ana niyeti tespit et",
            "3. Varlıkları (entities) çıkar",
            "4. Bağlamsal işaretleri belirle",
            "5. Tercih göstergelerini analiz et",
            "6. Güven skorunu hesapla"
        ]
        
        # TEMPLATE PATTERN: Structured intent classification
        intent_templates = {
            "combination_request": {
                "patterns": ["ne giyeyim", "kombin", "öner", "uygun", "birlikte", "hangi kıyafet"],
                "entities": ["kombin", "giyim", "öneri", "uygun", "stil"],
                "confidence_base": 0.92
            },
            "single_item_query": {
                "patterns": ["bu ... ile", "hangi", "ne giyebilirim", "uyumlu", "eşleştir"],
                "entities": ["eşleştirme", "uyum", "birlikte"],
                "confidence_base": 0.89
            },
            "shoe_matching": {
                "patterns": ["ayakkabı", "uygun", "var mı", "hangi ayakkabı", "shoe"],
                "entities": ["ayakkabı", "uygun", "uyum"],
                "confidence_base": 0.91
            },
            "jacket_pairing": {
                "patterns": ["ceket", "öner", "hangi ceket", "jacket", "blazer"],
                "entities": ["ceket", "öneri", "uygun"],
                "confidence_base": 0.88
            },
            "weather_based": {
                "patterns": ["hava", "soğuk", "sıcak", "yağmur", "kar", "weather"],
                "entities": ["hava", "soğuk", "sıcak", "mevsim"],
                "confidence_base": 0.94
            },
            "occasion_specific": {
                "patterns": ["ofis", "toplantı", "parti", "yemek", "buluşma", "work", "meeting"],
                "entities": ["etkinlik", "durum", "ortam"],
                "confidence_base": 0.87
            }
        }
        
        # CONTEXT & INSTRUCTION PATTERN: Rich contextual analysis
        text_lower = text.lower()
        
        # Advanced pattern matching with confidence scoring
        detected_intent = "general_styling"
        detected_entities = []
        context_markers = []
        preference_indicators = []
        confidence = 0.70
        query_type = QueryType.GENERAL_STYLING
        
        # Weather-based outfit query detection
        if any(pattern in text_lower for pattern in intent_templates["weather_based"]["patterns"]):
            detected_intent = "hava_durumu_bazli_outfit"
            detected_entities = ["hava", "giyim", "uygun"]
            context_markers = ["mevsimsel", "praktik", "koruma"]
            preference_indicators = ["uygun", "rahat", "fonksiyonel"]
            confidence = intent_templates["weather_based"]["confidence_base"]
            query_type = QueryType.GENERAL_STYLING
            
        # Shoe matching query detection
        elif any(pattern in text_lower for pattern in intent_templates["shoe_matching"]["patterns"]):
            detected_intent = "ayakkabı_uyumu_sorgulama"
            detected_entities = ["ayakkabı", "uygun", "elbise"]
            context_markers = ["renk", "stil", "uyum", "formallık"]
            preference_indicators = ["uygun", "uyumlu", "yakışır"]
            confidence = intent_templates["shoe_matching"]["confidence_base"]
            query_type = QueryType.DRESS_SHOE_MATCHING
            
        # Jacket pairing query detection
        elif any(pattern in text_lower for pattern in intent_templates["jacket_pairing"]["patterns"]):
            detected_intent = "ceket_önerisi_isteme"
            detected_entities = ["ceket", "pantolon", "öneri"]
            context_markers = ["stil", "uyum", "kombin", "profesyonel"]
            preference_indicators = ["öneri", "uygun", "yakışır"]
            confidence = intent_templates["jacket_pairing"]["confidence_base"]
            query_type = QueryType.PANTS_JACKET_PAIRING
            
        # Single item pairing query detection
        elif any(pattern in text_lower for pattern in intent_templates["single_item_query"]["patterns"]):
            detected_intent = "tek_parça_eşleştirme"
            detected_entities = ["eşleştirme", "uyum", "kombinasyon"]
            context_markers = ["renk", "stil", "uyum"]
            preference_indicators = ["uygun", "güzel", "yakışır"]
            confidence = intent_templates["single_item_query"]["confidence_base"]
            query_type = QueryType.SHIRT_COMBINATION
            
        # Occasion-specific query detection
        elif any(pattern in text_lower for pattern in intent_templates["occasion_specific"]["patterns"]):
            detected_intent = "etkinlik_bazli_kiyafet"
            detected_entities = ["etkinlik", "durum", "uygun"]
            context_markers = ["formallık", "ortam", "sosyal"]
            preference_indicators = ["uygun", "yakışır", "profesyonel"]
            confidence = intent_templates["occasion_specific"]["confidence_base"]
            query_type = QueryType.GENERAL_STYLING
            
        # General combination request
        elif any(pattern in text_lower for pattern in intent_templates["combination_request"]["patterns"]):
            detected_intent = "kombin_önerisi_isteme"
            detected_entities = ["giyim", "kombin", "öneri"]
            context_markers = ["günlük", "uygun", "stil"]
            preference_indicators = ["beğeni", "uyum", "güzel"]
            confidence = intent_templates["combination_request"]["confidence_base"]
            query_type = QueryType.SHIRT_COMBINATION
        
        # Sentiment analysis based on language patterns
        sentiment = "neutral"
        if any(word in text_lower for word in ["mükemmel", "harika", "güzel", "beğeniyorum"]):
            sentiment = "positive"
        elif any(word in text_lower for word in ["hiç", "berbat", "kötü", "beğenmiyorum"]):
            sentiment = "negative"
        
        # Urgency level detection
        urgency = "medium"
        if any(word in text_lower for word in ["acil", "hemen", "şimdi", "bugün"]):
            urgency = "high"
        elif any(word in text_lower for word in ["gelecekte", "sonra", "belki"]):
            urgency = "low"
        
        # Apply confidence boost for multi-pattern matches
        pattern_matches = sum(1 for template in intent_templates.values() 
                            if any(pattern in text_lower for pattern in template["patterns"]))
        if pattern_matches > 1:
            confidence = min(0.98, confidence + 0.05)
        
        logger.info(f"🎯 NLU Analysis Results:")
        logger.info(f"  Intent: {detected_intent} (confidence: {confidence:.2f})")
        logger.info(f"  Entities: {detected_entities}")
        logger.info(f"  Query Type: {query_type}")
        logger.info(f"  Sentiment: {sentiment}, Urgency: {urgency}")
        
        return TextAnalysisResult(
            intent=detected_intent,
            entities=detected_entities,
            context_markers=context_markers,
            preference_indicators=preference_indicators,
            query_type=query_type,
            confidence_score=confidence,
            sentiment=sentiment,
            urgency_level=urgency,
            processing_time_ms=0.0
        )

class ContextFusionEngine:
    """Görsel ve metin analizlerini birleştiren bağlam füzyon motoru"""
    
    def __init__(self):
        """ContextFusionEngine sınıfını başlatır"""
        logger.info("🔄 Context Fusion Engine initializing...")
        self.fusion_strategies = {
            QueryType.SHIRT_COMBINATION: self._fuse_shirt_combination,
            QueryType.DRESS_SHOE_MATCHING: self._fuse_dress_shoe_matching,
            QueryType.PANTS_JACKET_PAIRING: self._fuse_pants_jacket_pairing,
            QueryType.BAG_OUTFIT_STYLING: self._fuse_bag_outfit_styling,
            QueryType.GENERAL_STYLING: self._fuse_general_styling
        }
        logger.info("✅ Context Fusion Engine initialized successfully")
    
    def fuse_contexts(self, 
                     visual_analysis: ImageAnalysisResult, 
                     textual_analysis: TextAnalysisResult,
                     user_profile: Dict[str, Any]) -> FusedContext:
        """
        Görsel ve metin analizlerini birleştirerek unified context oluşturur
        
        Args:
            visual_analysis: Görsel analiz sonucu
            textual_analysis: Metin analiz sonucu
            user_profile: Kullanıcı profil bilgileri
            
        Returns:
            FusedContext: Birleştirilmiş bağlam
        """
        logger.info("🔀 Starting context fusion process...")
        
        try:
            # Query type'a göre uygun fusion strategy'yi seç
            fusion_strategy = self.fusion_strategies.get(
                textual_analysis.query_type, 
                self._fuse_general_styling
            )
            
            # Fusion strategy'yi uygula
            fused_context = fusion_strategy(visual_analysis, textual_analysis, user_profile)
            
            # Fusion confidence hesapla
            fused_context.fusion_confidence = self._calculate_fusion_confidence(
                visual_analysis, textual_analysis
            )
            
            logger.info(f"✅ Context fusion completed with confidence: {fused_context.fusion_confidence:.2f}")
            logger.info(f"🎯 Unified intent: {fused_context.unified_intent}")
            
            return fused_context
            
        except Exception as e:
            logger.error(f"❌ Context fusion failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Context fusion failed: {str(e)}")
    
    def _fuse_shirt_combination(self, visual: ImageAnalysisResult, textual: TextAnalysisResult, profile: Dict) -> FusedContext:
        """Gömlek kombinasyon sorguları için özel fusion logic"""
        return FusedContext(
            visual_context=visual,
            textual_context=textual,
            user_profile=profile,
            unified_intent=f"Kullanıcı {visual.dominant_color} renkte {visual.style_category} tarzında bir gömlek için kombin önerisi istiyor",
            recommendation_type="alt_parça_ve_aksesuar_önerisi",
            fusion_confidence=0.0,  # Sonradan hesaplanacak
            contextual_priorities=["renk_uyumu", "stil_tutarlılığı", "formallik_uyumu"],
            processing_metadata={
                "primary_focus": "gömlek",
                "secondary_focus": "alt_parça",
                "tertiary_focus": "aksesuar"
            }
        )
    
    def _fuse_dress_shoe_matching(self, visual: ImageAnalysisResult, textual: TextAnalysisResult, profile: Dict) -> FusedContext:
        """Elbise-ayakkabı uyum sorguları için özel fusion logic"""
        return FusedContext(
            visual_context=visual,
            textual_context=textual,
            user_profile=profile,
            unified_intent=f"Kullanıcı {visual.dominant_color} renkte {visual.style_category} elbiseye uygun ayakkabı arıyor",
            recommendation_type="ayakkabı_uyum_önerisi",
            fusion_confidence=0.0,
            contextual_priorities=["renk_uyumu", "formality_matching", "ocasyon_uygunluğu"],
            processing_metadata={
                "primary_focus": "elbise",
                "secondary_focus": "ayakkabı",
                "style_constraints": visual.formality_level.value
            }
        )
    
    def _fuse_pants_jacket_pairing(self, visual: ImageAnalysisResult, textual: TextAnalysisResult, profile: Dict) -> FusedContext:
        """Pantolon-ceket kombinasyon sorguları için özel fusion logic"""
        return FusedContext(
            visual_context=visual,
            textual_context=textual,
            user_profile=profile,
            unified_intent=f"Kullanıcı {visual.dominant_color} renkte pantolonla uyumlu ceket önerisi istiyor",
            recommendation_type="ceket_önerisi",
            fusion_confidence=0.0,
            contextual_priorities=["stil_uyumu", "renk_uyumu", "proportion_balance"],
            processing_metadata={
                "primary_focus": "pantolon",
                "secondary_focus": "ceket",
                "style_considerations": ["formal_casual_balance", "color_theory"]
            }
        )
    
    def _fuse_bag_outfit_styling(self, visual: ImageAnalysisResult, textual: TextAnalysisResult, profile: Dict) -> FusedContext:
        """Çanta merkezli styling sorguları için özel fusion logic"""
        return FusedContext(
            visual_context=visual,
            textual_context=textual,
            user_profile=profile,
            unified_intent=f"Kullanıcı {visual.dominant_color} renkte çantaya uygun komple outfit istiyor",
            recommendation_type="komple_outfit_önerisi",
            fusion_confidence=0.0,
            contextual_priorities=["çanta_uyumu", "head_to_toe_balance", "ocasyon_uygunluğu"],
            processing_metadata={
                "primary_focus": "çanta",
                "secondary_focus": "komple_outfit",
                "styling_approach": "çanta_merkezli"
            }
        )
    
    def _fuse_general_styling(self, visual: ImageAnalysisResult, textual: TextAnalysisResult, profile: Dict) -> FusedContext:
        """Genel styling sorguları için default fusion logic"""
        return FusedContext(
            visual_context=visual,
            textual_context=textual,
            user_profile=profile,
            unified_intent="Kullanıcı genel stil önerisi arıyor",
            recommendation_type="genel_stil_önerisi",
            fusion_confidence=0.0,
            contextual_priorities=["kullanıcı_tercihleri", "trend_uyumu", "praktiklik"],
            processing_metadata={
                "approach": "genel",
                "flexibility": "yüksek"
            }
        )
    
    def _calculate_fusion_confidence(self, visual: ImageAnalysisResult, textual: TextAnalysisResult) -> float:
        """
        Görsel ve metin analizlerinin güven skorlarına göre fusion confidence hesaplar
        """
        # Ağırlıklı ortalama ile confidence hesaplama
        visual_weight = 0.6  # Görsel analiz biraz daha ağırlıklı
        textual_weight = 0.4
        
        fusion_confidence = (visual.confidence_score * visual_weight + 
                           textual.confidence_score * textual_weight)
        
        # 0.1 ile 1.0 arasında clamp et
        return max(0.1, min(1.0, fusion_confidence))

# Request/Response models için Pydantic sınıfları
class MultiModalQueryRequest(BaseModel):
    """Çok modlu sorgu isteği için model"""
    image_base64: str = Field(..., description="Base64 encoded image data")
    text_query: str = Field(..., description="User's text query", min_length=1, max_length=500)
    user_id: Optional[str] = Field(None, description="User ID for personalization")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context")

class MultiModalQueryResponse(BaseModel):
    """Çok modlu sorgu yanıtı için model"""
    success: bool
    query_id: str
    unified_intent: str
    recommendation_type: str
    visual_analysis: Dict[str, Any]
    textual_analysis: Dict[str, Any]
    fusion_confidence: float
    recommendations: List[Dict[str, Any]]
    processing_time_ms: float
    timestamp: str

# Ana koordinatör sınıfı
class MultiModalCoordinator:
    """AURA AI Çok Modlu Sorgu Koordinatörü - Ana sınıf"""
    
    def __init__(self):
        """MultiModalCoordinator sınıfını başlatır ve tüm bileşenleri hazırlar"""
        logger.info("🎯 Multi-Modal Coordinator initializing...")
        
        # Bileşenleri başlat
        self.clip_processor = CLIPImageProcessor()
        self.nlu_processor = NLUTextProcessor()
        self.fusion_engine = ContextFusionEngine()
        
        # Service client'ları başlat
        self.service_clients = {
            "style_profile": "http://localhost:8003",
            "combination_engine": "http://localhost:8004", 
            "recommendation_engine": "http://localhost:8005",
            "quality_assurance": "http://localhost:8008"
        }
        
        self.http_client = httpx.AsyncClient(timeout=30.0)
        
        logger.info("✅ Multi-Modal Coordinator initialized successfully")
    
    async def process_multimodal_query(self, request: MultiModalQueryRequest) -> MultiModalQueryResponse:
        """
        Çok modlu sorguyu işleyen ana metod
        
        Args:
            request: Çok modlu sorgu isteği
            
        Returns:
            MultiModalQueryResponse: İşlenmiş sorgu yanıtı
        """
        start_time = datetime.now()
        query_id = f"mmq_{int(start_time.timestamp())}_{hash(request.text_query) % 10000}"
        
        logger.info(f"🚀 Processing multi-modal query {query_id}")
        logger.info(f"📝 Text query: '{request.text_query}'")
        
        try:
            # 1. Base64 image'ı decode et
            image_data = base64.b64decode(request.image_base64)
            
            # 2. Parallel processing - Görsel ve metin analizini aynı anda başlat
            image_task = self.clip_processor.analyze_image(image_data, request.text_query)
            text_task = self.nlu_processor.analyze_text(request.text_query)
            
            # 3. Her iki analizi tamamlanmasını bekle
            visual_analysis, textual_analysis = await asyncio.gather(image_task, text_task)
            
            # 4. Kullanıcı profilini al (eğer user_id varsa)
            user_profile = await self._get_user_profile(request.user_id) if request.user_id else {}
            
            # 5. Context fusion - Analizleri birleştir
            fused_context = self.fusion_engine.fuse_contexts(
                visual_analysis, textual_analysis, user_profile
            )
            
            # 6. Service koordinasyonu ile önerileri al
            recommendations = await self._coordinate_recommendation_services(fused_context)
            
            # 7. Kalite kontrolü yap
            validated_recommendations = await self._validate_recommendations(recommendations, fused_context)
            
            # 8. Response hazırla
            total_processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            response = MultiModalQueryResponse(
                success=True,
                query_id=query_id,
                unified_intent=fused_context.unified_intent,
                recommendation_type=fused_context.recommendation_type,
                visual_analysis={
                    "item_type": visual_analysis.item_type,
                    "dominant_color": visual_analysis.dominant_color,
                    "style_category": visual_analysis.style_category,
                    "confidence": visual_analysis.confidence_score
                },
                textual_analysis={
                    "intent": textual_analysis.intent,
                    "entities": textual_analysis.entities,
                    "query_type": textual_analysis.query_type.value,
                    "confidence": textual_analysis.confidence_score
                },
                fusion_confidence=fused_context.fusion_confidence,
                recommendations=validated_recommendations,
                processing_time_ms=total_processing_time,
                timestamp=start_time.isoformat()
            )
            
            logger.info(f"✅ Multi-modal query {query_id} completed in {total_processing_time:.2f}ms")
            logger.info(f"🎯 Generated {len(validated_recommendations)} recommendations")
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Multi-modal query {query_id} failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Multi-modal query processing failed: {str(e)}")
    
    async def _get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Kullanıcı profilini Style Profile servisinden alır"""
        try:
            response = await self.http_client.get(f"{self.service_clients['style_profile']}/profile/{user_id}")
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"⚠️ Could not fetch user profile for {user_id}")
                return {}
        except Exception as e:
            logger.error(f"❌ Error fetching user profile: {str(e)}")
            return {}
    
    async def _coordinate_recommendation_services(self, context: FusedContext) -> List[Dict[str, Any]]:
        """Fused context'e göre appropriate servisleri koordine eder"""
        logger.info(f"🔄 Coordinating services for {context.recommendation_type}")
        
        recommendations = []
        
        try:
            # Query type'a göre farklı service coordination strategies
            if context.textual_context.query_type == QueryType.SHIRT_COMBINATION:
                recommendations = await self._handle_shirt_combination(context)
            elif context.textual_context.query_type == QueryType.DRESS_SHOE_MATCHING:
                recommendations = await self._handle_dress_shoe_matching(context)
            elif context.textual_context.query_type == QueryType.PANTS_JACKET_PAIRING:
                recommendations = await self._handle_pants_jacket_pairing(context)
            elif context.textual_context.query_type == QueryType.BAG_OUTFIT_STYLING:
                recommendations = await self._handle_bag_outfit_styling(context)
            else:
                recommendations = await self._handle_general_styling(context)
            
            logger.info(f"📦 Generated {len(recommendations)} initial recommendations")
            return recommendations
            
        except Exception as e:
            logger.error(f"❌ Service coordination failed: {str(e)}")
            # Fallback önerileri döndür
            return await self._generate_fallback_recommendations(context)
    
    async def _handle_shirt_combination(self, context: FusedContext) -> List[Dict[str, Any]]:
        """Gömlek kombinasyon önerileri için özel koordinasyon"""
        try:
            # Combination Engine'e istek gönder
            combination_request = {
                "base_item": {
                    "type": context.visual_context.item_type,
                    "color": context.visual_context.dominant_color,
                    "style": context.visual_context.style_category
                },
                "request_type": "bottom_piece_recommendation",
                "user_preferences": context.user_profile.get("preferences", {}),
                "formality_level": context.visual_context.formality_level.value
            }
            
            response = await self.http_client.post(
                f"{self.service_clients['combination_engine']}/recommend_combination",
                json=combination_request
            )
            
            if response.status_code == 200:
                combination_data = response.json()
                return combination_data.get("recommendations", [])
            else:
                logger.warning("⚠️ Combination Engine request failed, using fallback")
                return self._mock_shirt_recommendations(context)
                
        except Exception as e:
            logger.error(f"❌ Shirt combination handling failed: {str(e)}")
            return self._mock_shirt_recommendations(context)
    
    async def _handle_dress_shoe_matching(self, context: FusedContext) -> List[Dict[str, Any]]:
        """Elbise-ayakkabı uyum önerileri için özel koordinasyon"""
        # Mock implementation - gerçek service koordinasyonu burada olacak
        return [
            {
                "type": "ayakkabı_önerisi",
                "item": "Siyah stiletto",
                "reason": f"Bu {context.visual_context.dominant_color} elbise ile mükemmel uyum sağlar",
                "confidence": 0.88,
                "style_notes": "Formal etkinlikler için ideal seçim"
            },
            {
                "type": "ayakkabı_önerisi", 
                "item": "Nude block heel",
                "reason": "Renk uyumu ve konfor dengesini sağlar",
                "confidence": 0.85,
                "style_notes": "Günlük şıklık için mükemmel"
            }
        ]
    
    async def _handle_pants_jacket_pairing(self, context: FusedContext) -> List[Dict[str, Any]]:
        """Pantolon-ceket kombinasyon önerileri için özel koordinasyon"""
        # Mock implementation
        return [
            {
                "type": "ceket_önerisi",
                "item": "Lacivert blazer",
                "reason": f"Bu {context.visual_context.dominant_color} pantolon ile klasik uyum",
                "confidence": 0.91,
                "style_notes": "Business casual için ideal"
            }
        ]
    
    async def _handle_bag_outfit_styling(self, context: FusedContext) -> List[Dict[str, Any]]:
        """Çanta merkezli komple outfit önerileri için özel koordinasyon"""
        # Mock implementation
        return [
            {
                "type": "komple_outfit",
                "items": ["Beyaz gömlek", "Siyah pantolon", "Siyah stiletto"],
                "reason": f"Bu {context.visual_context.dominant_color} çanta ile profesyonel look",
                "confidence": 0.87,
                "style_notes": "Ofis ve akşam etkinlikleri için uygun"
            }
        ]
    
    async def _handle_general_styling(self, context: FusedContext) -> List[Dict[str, Any]]:
        """Genel styling önerileri için koordinasyon"""
        # Mock implementation
        return [
            {
                "type": "genel_stil_önerisi",
                "suggestion": "Minimalist ve şık bir kombin",
                "reason": "Kullanıcı profiline uygun genel öneri",
                "confidence": 0.75,
                "style_notes": "Çok amaçlı kullanım için uygundur"
            }
        ]
    
    def _mock_shirt_recommendations(self, context: FusedContext) -> List[Dict[str, Any]]:
        """Gömlek için fallback önerileri"""
        return [
            {
                "type": "alt_parça_önerisi",
                "item": "Siyah kumaş pantolon", 
                "reason": f"Bu {context.visual_context.dominant_color} gömlek ile professional look yaratır",
                "confidence": 0.85,
                "style_notes": "İş ve sosyal etkinlikler için ideal"
            },
            {
                "type": "alt_parça_önerisi",
                "item": "Lacivert chino pantolon",
                "reason": "Smart casual look için mükemmel seçim",
                "confidence": 0.82,
                "style_notes": "Rahat ve şık günlük kombinler için"
            }
        ]
    
    async def _generate_fallback_recommendations(self, context: FusedContext) -> List[Dict[str, Any]]:
        """Genel fallback önerileri üretir"""
        return [
            {
                "type": "fallback_öneri",
                "suggestion": "Temel kombin önerisi",
                "reason": "Güvenli ve klasik seçim",
                "confidence": 0.70,
                "style_notes": "Her zaman uygun olan temel kombinasyon"
            }
        ]
    
    async def _validate_recommendations(self, recommendations: List[Dict[str, Any]], context: FusedContext) -> List[Dict[str, Any]]:
        """Quality Assurance servisi ile önerileri doğrular"""
        try:
            # Quality Assurance servisine validation isteği gönder
            validation_request = {
                "ai_output": {
                    "recommendations": recommendations,
                    "context": context.unified_intent
                },
                "context": {
                    "service_source": "multi_modal_coordinator",
                    "query_type": context.textual_context.query_type.value,
                    "fusion_confidence": context.fusion_confidence
                }
            }
            
            response = await self.http_client.post(
                f"{self.service_clients['quality_assurance']}/validate",
                json=validation_request
            )
            
            if response.status_code == 200:
                validation_result = response.json()
                if validation_result.get("status") == "approved":
                    logger.info("✅ Recommendations validated successfully")
                    return recommendations
                else:
                    logger.warning("⚠️ Recommendations need improvement")
                    # Improvement suggestions'ları apply et
                    return self._apply_quality_improvements(recommendations, validation_result)
            else:
                logger.warning("⚠️ Quality validation failed, returning original recommendations")
                return recommendations
                
        except Exception as e:
            logger.error(f"❌ Quality validation failed: {str(e)}")
            return recommendations
    
    def _apply_quality_improvements(self, recommendations: List[Dict[str, Any]], validation_result: Dict) -> List[Dict[str, Any]]:
        """Quality Assurance önerilerine göre recommendations'ları improve eder"""
        # Basit implementation - gerçek projede daha sophisticated logic olacak
        improvements = validation_result.get("improvement_suggestions", [])
        
        # Her recommendation'a improvement note ekle
        for rec in recommendations:
            rec["quality_notes"] = improvements[:2] if improvements else []
            rec["validated"] = True
        
        return recommendations

# Ana service instance'ı
coordinator = MultiModalCoordinator()

# Export edilecek ana fonksiyon
async def process_query(request: MultiModalQueryRequest) -> MultiModalQueryResponse:
    """Multi-modal query processing için ana entry point"""
    return await coordinator.process_multimodal_query(request)
