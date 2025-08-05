# 🧠 AURA AI - ADVANCED NLU WITH PROMPT ENGINEERING
# Prompt Kalıpları ve Akış Mühendisliği ile Gelişmiş Doğal Dil Anlama Servisi

import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import re
from datetime import datetime

# Configure detailed logging for prompt engineering analysis
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntentType(Enum):
    """Kullanıcı amaç kategorileri"""
    OUTFIT_RECOMMENDATION = "outfit_recommendation"  # Kıyafet önerisi
    STYLE_COMBINATION = "style_combination"         # Kombinasyon önerisi
    OCCASION_DRESSING = "occasion_dressing"         # Durum/etkinlik giyimi
    COLOR_MATCHING = "color_matching"               # Renk uyumu
    WARDROBE_ANALYSIS = "wardrobe_analysis"         # Gardırop analizi
    SIZE_FIT_QUERY = "size_fit_query"               # Beden/uyum sorgusu
    TREND_INQUIRY = "trend_inquiry"                 # Trend/moda sorgusu
    SHOPPING_ASSISTANCE = "shopping_assistance"     # Alışveriş yardımı

class ContextType(Enum):
    """Bağlam/durum kategorileri"""
    WORK_OFFICE = "work_office"                     # İş/ofis
    CASUAL_DAILY = "casual_daily"                   # Günlük/rahat
    FORMAL_EVENT = "formal_event"                   # Resmi etkinlik
    SOCIAL_PARTY = "social_party"                   # Sosyal/parti
    SPORTS_ACTIVE = "sports_active"                 # Spor/aktif
    TRAVEL_VACATION = "travel_vacation"             # Seyahat/tatil
    DATE_ROMANTIC = "date_romantic"                 # Randevu/romantik
    WEATHER_SPECIFIC = "weather_specific"           # Hava durumu özel

@dataclass
class PromptPattern:
    """Prompt Kalıbı yapısı - her kalıp beş bileşen içerir"""
    persona: str        # Kişilik - AI'nın rolü ve uzmanlığı
    recipe: str         # Tarif - Görevin adım adım açıklaması  
    template: str       # Şablon - Çıktı formatı ve yapısı
    context: str        # Bağlam - Mevcut durum ve kısıtlamalar
    instruction: str    # Talimat - Spesifik eylem yönergeleri

class AdvancedPromptNLU:
    """
    Prompt Kalıpları ve Akış Mühendisliği ile Gelişmiş NLU Servisi
    
    Bu sınıf, kullanıcı sorgularını anlama işlemini beş temel bileşenle yapar:
    1. PERSONA: Moda uzmanı AI kişiliği
    2. RECIPE: Analiz sürecinin adımları  
    3. TEMPLATE: Yapılandırılmış çıktı formatı
    4. CONTEXT: Kullanıcı bağlamı ve kısıtlamalar
    5. INSTRUCTION: Spesifik görev talimatları
    """
    
    def __init__(self):
        """Gelişmiş NLU servisini başlat ve prompt kalıplarını yükle"""
        
        logger.info("🧠 Gelişmiş Prompt Engineering NLU başlatılıyor...")
        
        # PERSONA: AI'nın temel kişiliği ve uzmanlığı
        self.core_persona = """
        Sen AURA'nın yapay zeka moda uzmanısın. Özellik ve yeteneklerin:
        - 10+ yıllık moda danışmanlığı deneyimi
        - Kültürlerarası stil anlayışı (TR, EN, ES, FR, DE)
        - Renk teorisi ve stil harmoni uzmanı
        - Beden analizi ve fit optimizasyonu
        - Trend analizi ve sezonsal adaptasyon
        - Kişisel stil DNA çıkarımı
        - Durum-bazlı giyim önerileri
        
        Yaklaşımın: Empatik, anlayışlı, pratik ve kişiselleştirilmiş
        Hedefiniz: Her kullanıcıya benzersiz stil çözümleri sunmak
        """
        
        # Gelişmiş intent tanıma prompt kalıpları
        self.intent_patterns = self._initialize_intent_patterns()
        
        # Context analiz prompt kalıpları  
        self.context_patterns = self._initialize_context_patterns()
        
        # Entity extraction prompt kalıpları
        self.entity_patterns = self._initialize_entity_patterns()
        
        # Fashion domain bilgi tabanı
        self.fashion_knowledge = self._initialize_fashion_knowledge()
        
        logger.info("✅ Prompt Engineering NLU hazır!")
    
    def _initialize_intent_patterns(self) -> Dict[IntentType, PromptPattern]:
        """Intent tanıma için prompt kalıpları"""
        
        return {
            IntentType.OUTFIT_RECOMMENDATION: PromptPattern(
                persona=self.core_persona + "\nŞu anda kıyafet önerisi uzmanı olarak çalışıyorsun.",
                
                recipe="""
                ADIM 1: Kullanıcının stilini ve tercihlerini analiz et
                ADIM 2: Durum ve bağlamı belirle (iş, günlük, özel etkinlik)
                ADIM 3: Vücut tipini ve fit gereksinimlerini değerlendir
                ADIM 4: Renk paleti ve stil uyumunu hesapla
                ADIM 5: Bütçe ve erişilebilirlik faktörlerini dahil et
                ADIM 6: Kişiselleştirilmiş öneri listesi oluştur
                """,
                
                template="""
                {
                    "intent": "outfit_recommendation",
                    "confidence": <0.0-1.0>,
                    "user_request": "<kullanıcı isteği özet>",
                    "style_preferences": ["<style1>", "<style2>"],
                    "occasion": "<durum>",
                    "specific_items": ["<item1>", "<item2>"],
                    "constraints": {"budget": "<bütçe>", "season": "<sezon>"}
                }
                """,
                
                context="Kullanıcı yeni kıyafet kombinleri veya önerileri arıyor. Mevcut gardırobu ve tercihleri dikkate alınmalı.",
                
                instruction="Kullanıcının giyim ihtiyacını tam olarak anlayıp, pratik ve uygulanabilir öneriler sun."
            ),
            
            IntentType.STYLE_COMBINATION: PromptPattern(
                persona=self.core_persona + "\nŞu anda stil koordinasyonu uzmanı olarak çalışıyorsun.",
                
                recipe="""
                ADIM 1: Mevcut kıyafet parçalarını tanımla
                ADIM 2: Renk uyumu ve harmoniyi analiz et
                ADIM 3: Stil tutarlılığını değerlendir
                ADIM 4: Orantı ve fit uyumunu kontrol et
                ADIM 5: Aksesuar ve tamamlayıcı önerileri ekle
                ADIM 6: Alternatif kombinasyon seçenekleri sun
                """,
                
                template="""
                {
                    "intent": "style_combination",
                    "confidence": <0.0-1.0>,
                    "base_items": ["<mevcut_parça1>", "<mevcut_parça2>"],
                    "combination_suggestions": [
                        {
                            "items": ["<item1>", "<item2>", "<item3>"],
                            "color_harmony": "<renk_analizi>",
                            "style_coherence": "<stil_tutarlılık>",
                            "confidence": <0.0-1.0>
                        }
                    ],
                    "accessories": ["<aksesuar1>", "<aksesuar2>"]
                }
                """,
                
                context="Kullanıcı mevcut kıyafetlerini nasıl kombineleyeceğini öğrenmek istiyor.",
                
                instruction="Mevcut parçaları en iyi şekilde koordine edecek kombinasyon önerileri oluştur."
            ),
            
            IntentType.OCCASION_DRESSING: PromptPattern(
                persona=self.core_persona + "\nŞu anda etkinlik giyimi uzmanı olarak çalışıyorsun.",
                
                recipe="""
                ADIM 1: Etkinlik türünü ve dress code'unu belirle
                ADIM 2: Sosyal beklentileri ve normları analiz et
                ADIM 3: Hava durumu ve mekan faktörlerini dahil et
                ADIM 4: Kullanıcının komfort zonunu değerlendir
                ADIM 5: Uygun stil seviyesini ve formallik derecesini hesapla
                ADIM 6: Durum-spesifik giyim önerileri oluştur
                """,
                
                template="""
                {
                    "intent": "occasion_dressing",
                    "confidence": <0.0-1.0>,
                    "occasion_type": "<etkinlik_türü>",
                    "formality_level": "<resmilik_seviyesi>",
                    "dress_code": "<giyim_kodu>",
                    "recommendations": [
                        {
                            "outfit": ["<item1>", "<item2>", "<item3>"],
                            "appropriateness": "<uygunluk_skoru>",
                            "reasoning": "<gerekçe>"
                        }
                    ],
                    "do_not_wear": ["<uygunsuz_item1>", "<uygunsuz_item2>"]
                }
                """,
                
                context="Kullanıcı belirli bir etkinlik veya durum için ne giyeceğini planlıyor.",
                
                instruction="Etkinliğe uygun, sosyal beklentileri karşılayan giyim önerileri sun."
            )
        }
    
    def _initialize_context_patterns(self) -> Dict[ContextType, PromptPattern]:
        """Context analizi için prompt kalıpları"""
        
        return {
            ContextType.WORK_OFFICE: PromptPattern(
                persona=self.core_persona + "\nŞu anda iş dünyası giyim uzmanı olarak çalışıyorsun.",
                
                recipe="""
                ADIM 1: Şirket kültürünü ve dress code'unu analiz et
                ADIM 2: Pozisyon ve rol gereksinimlerini değerlendir
                ADIM 3: Mesleki güvenilirlik ve otoriteyi destekle
                ADIM 4: Komfort ve fonksiyonelliği dahil et
                ADIM 5: Mevsim ve klima faktörlerini hesapla
                ADIM 6: Profesyonel görünüm optimizasyonu yap
                """,
                
                template="""
                {
                    "context": "work_office",
                    "confidence": <0.0-1.0>,
                    "professional_level": "<profesyonellik_seviyesi>",
                    "industry_norms": "<sektör_normları>",
                    "key_factors": ["<faktör1>", "<faktör2>"],
                    "style_guidelines": {
                        "colors": ["<renk1>", "<renk2>"],
                        "patterns": ["<desen1>", "<desen2>"],
                        "fits": ["<kesim1>", "<kesim2>"]
                    }
                }
                """,
                
                context="İş ortamı giyimi analizi - profesyonellik ve uygunluk öncelikli",
                
                instruction="İş ortamına uygun, profesyonel ve güvenilir görünüm sağlayan stil önerileri geliştir."
            ),
            
            ContextType.CASUAL_DAILY: PromptPattern(
                persona=self.core_persona + "\nŞu anda günlük stil uzmanı olarak çalışıyorsun.",
                
                recipe="""
                ADIM 1: Günlük aktivite planını analiz et
                ADIM 2: Komfort ve fonksiyonellik ihtiyacını belirle
                ADIM 3: Kişisel stil ifadesini destekle
                ADIM 4: Pratiklik ve bakım kolaylığını dahil et
                ADIM 5: Çok amaçlı giyim seçeneklerini öncelikle
                ADIM 6: Rahat ama şık görünüm dengesi kur
                """,
                
                template="""
                {
                    "context": "casual_daily",
                    "confidence": <0.0-1.0>,
                    "comfort_level": "high",
                    "versatility": "<çok_amaçlılık>",
                    "activities": ["<aktivite1>", "<aktivite2>"],
                    "style_approach": "<stil_yaklaşımı>",
                    "practical_considerations": ["<praktik_faktör1>", "<praktik_faktör2>"]
                }
                """,
                
                context="Günlük yaşam giyimi - komfort ve stil dengesi",
                
                instruction="Günlük hayatta rahat, pratik ama stil sahibi görünüm sağlayan öneriler sun."
            )
        }
    
    def _initialize_entity_patterns(self) -> Dict[str, PromptPattern]:
        """Entity extraction için prompt kalıpları"""
        
        return {
            "fashion_items": PromptPattern(
                persona=self.core_persona + "\nŞu anda moda ürünleri tanıma uzmanı olarak çalışıyorsun.",
                
                recipe="""
                ADIM 1: Metindeki giyim eşyalarını tespit et
                ADIM 2: Marka ve model bilgilerini çıkar
                ADIM 3: Renk ve desen tanımlamalarını belirle
                ADIM 4: Beden ve fit bilgilerini analiz et
                ADIM 5: Fiyat ve bütçe referanslarını yakala
                ADIM 6: Strukturlu veri formatında organize et
                """,
                
                template="""
                {
                    "fashion_entities": {
                        "clothing_items": [
                            {
                                "item": "<ürün_adı>",
                                "category": "<kategori>",
                                "color": "<renk>",
                                "brand": "<marka>",
                                "size": "<beden>",
                                "confidence": <0.0-1.0>
                            }
                        ],
                        "accessories": ["<aksesuar1>", "<aksesuar2>"],
                        "colors": ["<renk1>", "<renk2>"],
                        "patterns": ["<desen1>", "<desen2>"]
                    }
                }
                """,
                
                context="Metin içerisinden moda ve giyim ile ilgili tüm entity'leri çıkarma",
                
                instruction="Metindeki tüm moda öğelerini yüksek doğrulukla tanımla ve kategorize et."
            ),
            
            "occasion_entities": PromptPattern(
                persona=self.core_persona + "\nŞu anda etkinlik ve durum analiz uzmanı olarak çalışıyorsun.",
                
                recipe="""
                ADIM 1: Zaman referanslarını tespit et (sabah, akşam, hafta sonu)
                ADIM 2: Etkinlik türlerini tanımla (toplantı, parti, buluşma)
                ADIM 3: Mekan bilgilerini çıkar (ofis, restoran, ev)
                ADIM 4: Sosyal bağlamı analiz et (arkadaşlar, iş, aile)
                ADIM 5: Hava durumu ve mevsim faktörlerini belirle
                ADIM 6: Durum kompleksitesini değerlendir
                """,
                
                template="""
                {
                    "occasion_entities": {
                        "time_references": ["<zaman1>", "<zaman2>"],
                        "events": ["<etkinlik1>", "<etkinlik2>"],
                        "locations": ["<mekan1>", "<mekan2>"],
                        "social_context": "<sosyal_bağlam>",
                        "weather_season": "<hava_mevsim>",
                        "formality_level": "<resmilik_seviyesi>"
                    }
                }
                """,
                
                context="Kullanıcının bahsettiği durum ve etkinlik bilgilerini çıkarma",
                
                instruction="Metindeki tüm durum ve etkinlik bilgilerini sistematik olarak analiz et."
            )
        }
    
    def _initialize_fashion_knowledge(self) -> Dict[str, Any]:
        """Moda domain bilgi tabanı"""
        
        return {
            "style_categories": {
                "casual": ["jeans", "t-shirt", "sneakers", "hoodie", "denim jacket"],
                "formal": ["suit", "dress shirt", "tie", "dress shoes", "blazer"],
                "business": ["blazer", "dress pants", "button-down", "loafers", "pencil skirt"],
                "party": ["cocktail dress", "heels", "jewelry", "clutch", "statement piece"],
                "sport": ["athletic wear", "sneakers", "moisture-wicking", "leggings", "sports bra"]
            },
            
            "color_harmonies": {
                "complementary": [["blue", "orange"], ["red", "green"], ["purple", "yellow"]],
                "analogous": [["blue", "green"], ["red", "orange"], ["purple", "pink"]],
                "monochromatic": [["navy", "sky blue"], ["forest", "mint"], ["burgundy", "pink"]],
                "neutral": ["black", "white", "gray", "beige", "brown", "navy"]
            },
            
            "occasion_mapping": {
                "work": ["business", "professional", "conservative"],
                "casual": ["relaxed", "comfortable", "everyday"],
                "formal": ["elegant", "sophisticated", "dressy"],
                "party": ["fun", "trendy", "statement"],
                "date": ["romantic", "attractive", "confident"]
            },
            
            "season_guidelines": {
                "spring": ["light colors", "breathable fabrics", "layers"],
                "summer": ["light fabrics", "bright colors", "minimal layers"],
                "fall": ["earth tones", "layers", "transitional pieces"],
                "winter": ["dark colors", "warm fabrics", "heavy layers"]
            }
        }
    
    def analyze_with_prompt_patterns(self, user_text: str, analysis_context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Prompt kalıpları kullanarak kapsamlı NLU analizi yap
        
        Args:
            user_text: Kullanıcının doğal dil sorgusu
            analysis_context: Ek bağlam bilgileri
            
        Returns:
            Yapılandırılmış analiz sonuçları
        """
        
        logger.info(f"🔍 Prompt pattern analizi başlıyor: '{user_text[:50]}...'")
        
        try:
            # ADIM 1: Intent Classification (Amaç Belirleme)
            intent_result = self._classify_intent_with_patterns(user_text)
            
            # ADIM 2: Context Analysis (Bağlam Analizi)
            context_result = self._analyze_context_with_patterns(user_text)
            
            # ADIM 3: Entity Extraction (Öğe Çıkarımı)
            entity_result = self._extract_entities_with_patterns(user_text)
            
            # ADIM 4: Fashion Domain Reasoning (Moda Domain Mantığı)
            domain_result = self._apply_fashion_reasoning(user_text, intent_result, context_result, entity_result)
            
            # ADIM 5: Response Generation (Yanıt Üretimi)
            structured_response = self._generate_structured_response(
                user_text, intent_result, context_result, entity_result, domain_result
            )
            
            logger.info("✅ Prompt pattern analizi tamamlandı")
            return structured_response
            
        except Exception as e:
            logger.error(f"❌ Prompt pattern analizi hatası: {e}")
            return self._generate_fallback_response(user_text, str(e))
    
    def _classify_intent_with_patterns(self, text: str) -> Dict[str, Any]:
        """Intent classification using prompt patterns"""
        
        # Text preprocessing
        text_lower = text.lower()
        
        # Intent scoring based on keyword presence and context
        intent_scores = {}
        
        for intent_type, pattern in self.intent_patterns.items():
            score = 0.0
            
            # Keyword-based scoring (fallback implementation)
            if intent_type == IntentType.OUTFIT_RECOMMENDATION:
                keywords = ["ne giyebilirim", "kıyafet öner", "öneri", "recommend", "suggest", "what to wear"]
                score = sum(1 for keyword in keywords if keyword in text_lower) / len(keywords)
                
            elif intent_type == IntentType.STYLE_COMBINATION:
                keywords = ["kombinle", "uyar mı", "kombine", "match", "goes with", "coordinate"]
                score = sum(1 for keyword in keywords if keyword in text_lower) / len(keywords)
                
            elif intent_type == IntentType.OCCASION_DRESSING:
                keywords = ["etkinlik", "toplantı", "parti", "iş", "work", "meeting", "event", "party"]
                score = sum(1 for keyword in keywords if keyword in text_lower) / len(keywords)
            
            intent_scores[intent_type.value] = score
        
        # Find best intent
        best_intent = max(intent_scores, key=intent_scores.get)
        confidence = intent_scores[best_intent]
        
        return {
            "intent": best_intent,
            "confidence": confidence,
            "all_scores": intent_scores,
            "method": "prompt_pattern_classification"
        }
    
    def _analyze_context_with_patterns(self, text: str) -> Dict[str, Any]:
        """Context analysis using prompt patterns"""
        
        text_lower = text.lower()
        context_scores = {}
        
        # Context detection based on keywords and patterns
        for context_type, pattern in self.context_patterns.items():
            score = 0.0
            
            if context_type == ContextType.WORK_OFFICE:
                keywords = ["iş", "ofis", "toplantı", "work", "office", "meeting", "professional"]
                score = sum(1 for keyword in keywords if keyword in text_lower) / len(keywords)
                
            elif context_type == ContextType.CASUAL_DAILY:
                keywords = ["günlük", "rahat", "casual", "daily", "everyday", "comfortable"]
                score = sum(1 for keyword in keywords if keyword in text_lower) / len(keywords)
        
            context_scores[context_type.value] = score
        
        # Find dominant context
        best_context = max(context_scores, key=context_scores.get) if context_scores else "casual_daily"
        confidence = context_scores.get(best_context, 0.5)
        
        return {
            "context": best_context,
            "confidence": confidence,
            "all_scores": context_scores,
            "method": "prompt_pattern_context"
        }
    
    def _extract_entities_with_patterns(self, text: str) -> Dict[str, Any]:
        """Entity extraction using prompt patterns"""
        
        # Simple regex-based entity extraction (can be enhanced with NER models)
        entities = {
            "clothing_items": [],
            "colors": [],
            "occasions": [],
            "time_references": [],
            "brands": []
        }
        
        # Clothing items detection
        clothing_patterns = [
            r'\b(gömlek|shirt|blouse)\b',
            r'\b(pantolon|pants|trousers|jeans)\b', 
            r'\b(elbise|dress)\b',
            r'\b(ceket|jacket|blazer)\b',
            r'\b(ayakkabı|shoes|heels|sneakers)\b'
        ]
        
        for pattern in clothing_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["clothing_items"].extend(matches)
        
        # Color detection
        color_patterns = [
            r'\b(siyah|black|kara)\b',
            r'\b(beyaz|white)\b',
            r'\b(mavi|blue)\b',
            r'\b(kırmızı|red)\b',
            r'\b(yeşil|green)\b',
            r'\b(sarı|yellow)\b'
        ]
        
        for pattern in color_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["colors"].extend(matches)
        
        # Time and occasion detection
        time_patterns = [
            r'\b(sabah|morning)\b',
            r'\b(akşam|evening)\b',
            r'\b(bugün|today)\b',
            r'\b(yarın|tomorrow)\b'
        ]
        
        for pattern in time_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["time_references"].extend(matches)
        
        return {
            "entities": entities,
            "method": "prompt_pattern_extraction",
            "confidence": 0.7
        }
    
    def _apply_fashion_reasoning(self, text: str, intent: Dict, context: Dict, entities: Dict) -> Dict[str, Any]:
        """Fashion domain-specific reasoning"""
        
        reasoning = {
            "style_compatibility": 0.8,
            "occasion_appropriateness": 0.9,
            "color_harmony": 0.7,
            "season_fit": 0.8,
            "recommendations": []
        }
        
        # Apply domain knowledge based on intent and context
        if intent["intent"] == "outfit_recommendation":
            if context["context"] == "work_office":
                reasoning["recommendations"] = ["blazer", "dress pants", "button-down shirt"]
            elif context["context"] == "casual_daily":
                reasoning["recommendations"] = ["jeans", "t-shirt", "sneakers"]
        
        return reasoning
    
    def _generate_structured_response(self, text: str, intent: Dict, context: Dict, 
                                    entities: Dict, domain: Dict) -> Dict[str, Any]:
        """Generate final structured response"""
        
        return {
            "nlu_analysis": {
                "user_input": text,
                "processing_timestamp": datetime.now().isoformat(),
                "analysis_method": "prompt_pattern_engineering"
            },
            "intent_analysis": intent,
            "context_analysis": context,
            "entity_extraction": entities,
            "fashion_reasoning": domain,
            "confidence_overall": (intent["confidence"] + context["confidence"]) / 2,
            "next_actions": self._suggest_next_actions(intent, context, entities),
            "api_calls_needed": self._determine_service_calls(intent, context, entities)
        }
    
    def _suggest_next_actions(self, intent: Dict, context: Dict, entities: Dict) -> List[str]:
        """Suggest next actions based on analysis"""
        
        actions = []
        
        if intent["intent"] == "outfit_recommendation":
            actions.extend([
                "call_style_profile_service",
                "call_combination_engine",
                "call_recommendation_engine"
            ])
        elif intent["intent"] == "style_combination":
            actions.extend([
                "call_combination_engine",
                "analyze_color_harmony"
            ])
        
        return actions
    
    def _determine_service_calls(self, intent: Dict, context: Dict, entities: Dict) -> Dict[str, Any]:
        """Determine which microservices to call"""
        
        service_calls = {
            "image_processing": False,
            "style_profile": True,  # Almost always needed
            "combination_engine": False,
            "recommendation_engine": False,
            "feedback_loop": True   # For learning
        }
        
        if intent["intent"] in ["outfit_recommendation", "style_combination"]:
            service_calls["combination_engine"] = True
            service_calls["recommendation_engine"] = True
        
        return service_calls
    
    def _generate_fallback_response(self, text: str, error: str) -> Dict[str, Any]:
        """Generate fallback response when analysis fails"""
        
        return {
            "nlu_analysis": {
                "user_input": text,
                "processing_timestamp": datetime.now().isoformat(),
                "status": "fallback_mode",
                "error": error
            },
            "intent_analysis": {
                "intent": "general_inquiry",
                "confidence": 0.3,
                "method": "fallback"
            },
            "context_analysis": {
                "context": "casual_daily",
                "confidence": 0.3,
                "method": "fallback"
            },
            "entity_extraction": {
                "entities": {"clothing_items": [], "colors": [], "occasions": []},
                "method": "fallback"
            },
            "next_actions": ["request_clarification"],
            "confidence_overall": 0.3
        }

# Factory function for easy initialization
def create_advanced_nlu() -> AdvancedPromptNLU:
    """Create and return an instance of Advanced Prompt NLU"""
    return AdvancedPromptNLU()
