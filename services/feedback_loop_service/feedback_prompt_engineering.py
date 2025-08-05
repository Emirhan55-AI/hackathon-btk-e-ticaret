# 🔄 AURA AI - FEEDBACK LOOP PROMPT ENGINEERING
# Kullanıcı Geri Bildirim Analizi ve Öğrenme Optimizasyonu için Gelişmiş Prompt Kalıpları

import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import re
from datetime import datetime

# Configure detailed logging for feedback analysis
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FeedbackType(Enum):
    """Kullanıcı geri bildirim kategorileri"""
    POSITIVE_GENERAL = "positive_general"          # Genel beğeni
    NEGATIVE_GENERAL = "negative_general"          # Genel beğenmeme
    COLOR_DISSATISFACTION = "color_dissatisfaction"    # Renk uyumsuzluğu
    STYLE_MISMATCH = "style_mismatch"             # Stil uyumsuzluğu
    OCCASION_INAPPROPRIATE = "occasion_inappropriate"  # Durum uygunsuzluğu
    SIZE_FIT_ISSUE = "size_fit_issue"             # Beden/fit sorunu
    PREFERENCE_ALIGNMENT = "preference_alignment"  # Tercih uyumu
    REQUEST_SIMILAR = "request_similar"           # Benzer öneriler isteği

class FeedbackImpact(Enum):
    """Geri bildirimin sistem üzerindeki etkisi"""
    STYLE_PROFILE_UPDATE = "style_profile_update"      # Stil profili güncelleme
    RECOMMENDATION_SCORING = "recommendation_scoring"   # Öneri skorlama
    COLOR_PREFERENCE_LEARNING = "color_preference_learning"  # Renk tercihi öğrenme
    COMBINATION_RULES_UPDATE = "combination_rules_update"     # Kombinasyon kuralları
    USER_BEHAVIOR_MODELING = "user_behavior_modeling"         # Kullanıcı davranış modeli

@dataclass
class FeedbackPromptPattern:
    """Feedback Loop için özelleştirilmiş prompt kalıbı"""
    persona: str        # AI Öğrenme Uzmanı kişiliği
    recipe: str         # Geri bildirim analiz süreci adımları
    template: str       # Yapılandırılmış çıktı formatı
    context: str        # Feedback bağlamı ve kısıtlamalar
    instruction: str    # Öğrenme optimizasyonu talimatları

class AuraFeedbackPromptEngine:
    """
    AURA AI Feedback Loop için Gelişmiş Prompt Engineering Sistemi
    
    Bu sınıf, kullanıcı geri bildirimlerini analiz etme işlemini beş temel bileşenle yapar:
    1. PERSONA: AI Öğrenme ve Optimizasyon Uzmanı kişiliği
    2. RECIPE: Geri bildirim analizi ve öğrenme süreci adımları
    3. TEMPLATE: Sistem güncellemeleri için yapılandırılmış çıktı formatı
    4. CONTEXT: Kullanıcı geçmişi ve öneri bağlamı
    5. INSTRUCTION: Model optimizasyonu ve öğrenme talimatları
    """
    
    def __init__(self):
        """Feedback Loop Prompt Engineering sistemini başlat"""
        
        logger.info("🔄 AURA Feedback Loop Prompt Engineering başlatılıyor...")
        
        # PERSONA: AI Öğrenme ve Optimizasyon Uzmanı kişiliği
        self.core_persona = """
        Sen AURA'nın yapay zeka öğrenme ve optimizasyon uzmanısın. Özellik ve yeteneklerin:
        - Kullanıcı geri bildirimlerinden pattern tanıma uzmanı
        - Makine öğrenmesi model optimizasyonu uzmanı
        - Kişiselleştirme algoritmaları geliştirme uzmanı
        - Kullanıcı davranış analizi ve modelleme uzmanı
        - Öneri sistem performansı iyileştirme uzmanı
        - Real-time learning ve adaptasyon uzmanı
        - Multi-dimensional feedback analysis uzmanı
        
        Yaklaşımın: Veri-odaklı, analitik, sürekli öğrenme odaklı
        Hedefiniz: Her geri bildirimden maksimum öğrenme çıkarıp sistem performansını artırmak
        """
        
        # Geri bildirim türü bazlı prompt kalıpları
        self.feedback_patterns = self._initialize_feedback_patterns()
        
        # Öğrenme etkisi bazlı prompt kalıpları
        self.learning_patterns = self._initialize_learning_patterns()
        
        # Servisler arası koordinasyon kalıpları
        self.coordination_patterns = self._initialize_coordination_patterns()
        
        # Feedback domain bilgi tabanı
        self.feedback_knowledge = self._initialize_feedback_knowledge()
        
        logger.info("✅ Feedback Loop Prompt Engineering hazır!")
    
    def _initialize_feedback_patterns(self) -> Dict[FeedbackType, FeedbackPromptPattern]:
        """Geri bildirim türü bazlı prompt kalıpları"""
        
        return {
            FeedbackType.NEGATIVE_GENERAL: FeedbackPromptPattern(
                persona=self.core_persona + "\nŞu anda genel beğenmeme geri bildirimi analiz uzmanı olarak çalışıyorsun.",
                
                recipe="""
                ADIM 1: Geri bildirimin bağlamını ve kullanıcı profilini çek
                ADIM 2: Önerilen kombinasyon detaylarını analiz et
                ADIM 3: Potansiel beğenmeme nedenlerini kategorize et (renk, stil, uygunluk, beden)
                ADIM 4: Kullanıcının geçmiş tercihlerini ve tutarsızlıkları belirle
                ADIM 5: Öneri algoritmasındaki zayıf noktaları tespit et
                ADIM 6: Öğrenme parametrelerini güncellemek için action plan oluştur
                """,
                
                template="""
                {
                    "feedback_analysis": {
                        "type": "negative_general",
                        "confidence": <0.0-1.0>,
                        "user_id": "<kullanıcı_id>",
                        "recommendation_id": "<öneri_id>",
                        "timestamp": "<zaman_damgası>"
                    },
                    "root_cause_analysis": {
                        "primary_reasons": ["<neden1>", "<neden2>"],
                        "style_mismatch_score": <0.0-1.0>,
                        "color_harmony_score": <0.0-1.0>,
                        "occasion_fit_score": <0.0-1.0>,
                        "personal_preference_alignment": <0.0-1.0>
                    },
                    "learning_actions": [
                        {
                            "service": "<hedef_servis>",
                            "action": "<güncelleme_aksiyonu>",
                            "parameters": {"<param1>": "<değer1>"},
                            "priority": "high|medium|low"
                        }
                    ],
                    "model_updates": {
                        "recommendation_scoring": {"weight_adjustment": <değer>},
                        "style_profile": {"preference_update": "<güncelleme>"},
                        "combination_engine": {"rule_modification": "<kural>"}
                    }
                }
                """,
                
                context="Kullanıcı bir kombin önerisini genel olarak beğenmedi. Sistemin hangi aşamada hata yaptığını tespit etmek kritik.",
                
                instruction="Geri bildirimi derinlemesine analiz et ve sistem performansını artıracak spesifik öğrenme aksiyonları belirle."
            ),
            
            FeedbackType.COLOR_DISSATISFACTION: FeedbackPromptPattern(
                persona=self.core_persona + "\nŞu anda renk uyumu analiz uzmanı olarak çalışıyorsun.",
                
                recipe="""
                ADIM 1: Önerilen kombinasyondaki renk paletini detaylı analiz et
                ADIM 2: Kullanıcının renk tercih geçmişini ve reddettiklerini çek
                ADIM 3: Renk teorisi kuralları açısından kombinasyonu değerlendir
                ADIM 4: Kullanıcının cilt tonu, saç rengi ve kişisel stil faktörlerini dahil et
                ADIM 5: Renk uyumsuzluğunun spesifik nedenini belirle
                ADIM 6: Renk tercih modelini güncellemek için parametreler hesapla
                """,
                
                template="""
                {
                    "feedback_analysis": {
                        "type": "color_dissatisfaction",
                        "confidence": <0.0-1.0>,
                        "problematic_colors": ["<renk1>", "<renk2>"],
                        "color_combination_type": "<renk_kombinasyon_türü>",
                        "harmony_violation": "<uyumsuzluk_türü>"
                    },
                    "color_analysis": {
                        "suggested_colors": ["<önerilen_renk1>", "<önerilen_renk2>"],
                        "user_color_preferences": {
                            "liked_colors": ["<sevilen_renk>"],
                            "disliked_colors": ["<sevilmeyen_renk>"],
                            "neutral_tolerance": <tolerans_skoru>
                        },
                        "color_theory_compliance": <uyum_skoru>
                    },
                    "learning_adjustments": {
                        "color_weight_updates": {"<renk>": <yeni_ağırlık>},
                        "harmony_rule_modifications": ["<kural_güncellemesi>"],
                        "personal_color_profile_update": "<profil_güncelleme>"
                    }
                }
                """,
                
                context="Kullanıcı önerilen kombinasyondaki renk uyumunu beğenmedi. Renk tercih modelinin güncellenmesi gerekiyor.",
                
                instruction="Renk uyumsuzluğunun kök nedenini belirle ve kullanıcının renk tercih profilini optimize et."
            ),
            
            FeedbackType.POSITIVE_GENERAL: FeedbackPromptPattern(
                persona=self.core_persona + "\nŞu anda pozitif geri bildirim analiz uzmanı olarak çalışıyorsun.",
                
                recipe="""
                ADIM 1: Beğenilen kombinasyonun özelliklerini detaylandır
                ADIM 2: Hangi faktörlerin başarıya katkıda bulunduğunu analiz et
                ADIM 3: Kullanıcının tercih modelindeki doğru pattern'leri güçlendir
                ADIM 4: Benzer başarılı önerilerin tekrarlanabilirliğini sağla
                ADIM 5: Pozitif pattern'leri diğer kullanıcılara da genelle
                ADIM 6: Başarılı model parametrelerini pekiştir
                """,
                
                template="""
                {
                    "feedback_analysis": {
                        "type": "positive_general",
                        "confidence": <0.0-1.0>,
                        "successful_elements": ["<başarılı_öğe1>", "<başarılı_öğe2>"],
                        "satisfaction_score": <memnuniyet_skoru>
                    },
                    "success_factors": {
                        "style_alignment": <stil_uyum_skoru>,
                        "color_harmony": <renk_uyum_skoru>,
                        "occasion_appropriateness": <durum_uygunluk_skoru>,
                        "personal_taste_match": <kişisel_tercih_skoru>
                    },
                    "reinforcement_actions": [
                        {
                            "pattern": "<başarılı_pattern>",
                            "amplification_factor": <güçlendirme_faktörü>,
                            "application_scope": "user_specific|general"
                        }
                    ],
                    "model_strengthening": {
                        "successful_weights": {"<parametre>": <güçlendirilecek_ağırlık>"},
                        "pattern_reinforcement": ["<pekiştirilecek_pattern>"],
                        "similarity_expansion": "<benzer_öneri_genişletme>"
                    }
                }
                """,
                
                context="Kullanıcı bir kombin önerisini beğendi. Bu başarılı pattern'i güçlendirmek ve tekrarlamak gerekiyor.",
                
                instruction="Başarılı faktörleri analiz et ve bu pattern'leri güçlendirerek gelecek önerilerin kalitesini artır."
            ),
            
            FeedbackType.REQUEST_SIMILAR: FeedbackPromptPattern(
                persona=self.core_persona + "\nŞu anda benzer öneri talep analiz uzmanı olarak çalışıyorsun.",
                
                recipe="""
                ADIM 1: Beğenilen kombinasyonun core özelliklerini çıkar
                ADIM 2: Hangi benzerlik boyutlarının önemli olduğunu belirle (renk, stil, formallik)
                ADIM 3: Kullanıcının 'benzerlik' tanımını tercih geçmişinden çıkar
                ADIM 4: Variasyon aralığını hesapla (çok benzer vs yaratıcı varyasyon)
                ADIM 5: Benzer öneriler için arama kriterlerini optimize et
                ADIM 6: Öneri çeşitliliği ve benzerlik dengesini kur
                """,
                
                template="""
                {
                    "feedback_analysis": {
                        "type": "request_similar",
                        "confidence": <0.0-1.0>,
                        "reference_recommendation": "<referans_öneri_id>",
                        "similarity_request_strength": <benzerlik_talep_gücü>
                    },
                    "similarity_dimensions": {
                        "color_palette": {"importance": <önem>, "variation_range": <varyasyon>},
                        "style_category": {"importance": <önem>, "variation_range": <varyasyon>},
                        "formality_level": {"importance": <önem>, "variation_range": <varyasyon>},
                        "item_types": {"importance": <önem>, "variation_range": <varyasyon>}
                    },
                    "recommendation_strategy": {
                        "similarity_threshold": <benzerlik_eşiği>,
                        "diversity_factor": <çeşitlilik_faktörü>,
                        "exploration_rate": <keşif_oranı>
                    },
                    "search_optimization": {
                        "primary_filters": ["<ana_filtre>"],
                        "secondary_preferences": ["<ikincil_tercih>"],
                        "avoided_patterns": ["<kaçınılacak_pattern>"]
                    }
                }
                """,
                
                context="Kullanıcı beğendiği bir kombinasyona benzer öneriler istiyor. Benzerlik boyutlarını optimize etmek gerekiyor.",
                
                instruction="Beğenilen kombinasyonun özelliklerini analiz et ve optimal benzerlik-çeşitlilik dengesinde yeni öneriler üret."
            )
        }
    
    def _initialize_learning_patterns(self) -> Dict[FeedbackImpact, FeedbackPromptPattern]:
        """Öğrenme etkisi bazlı prompt kalıpları"""
        
        return {
            FeedbackImpact.STYLE_PROFILE_UPDATE: FeedbackPromptPattern(
                persona=self.core_persona + "\nŞu anda kullanıcı stil profili güncelleme uzmanı olarak çalışıyorsun.",
                
                recipe="""
                ADIM 1: Mevcut stil profili parametrelerini yükle
                ADIM 2: Geri bildirimin stil profili üzerindeki etkilerini hesapla
                ADIM 3: Güncelleme gerektirecek parametreleri belirle
                ADIM 4: Güncelleme büyüklüğünü ve yönünü hesapla
                ADIM 5: Profil tutarlılığını koruyacak şekilde optimize et
                ADIM 6: Güncellenen profili validate et
                """,
                
                template="""
                {
                    "profile_update": {
                        "user_id": "<kullanıcı_id>",
                        "update_type": "style_profile",
                        "confidence": <güven_skoru>,
                        "update_magnitude": "minor|moderate|major"
                    },
                    "parameter_updates": {
                        "style_preferences": {
                            "<stil_kategorisi>": {"old": <eski_değer>, "new": <yeni_değer>}
                        },
                        "color_preferences": {
                            "<renk>": {"preference_score": <yeni_skor>}
                        },
                        "formality_tendencies": {
                            "formal_preference": <formallik_tercihi>,
                            "casual_tolerance": <rahat_giyim_toleransı>
                        }
                    },
                    "validation_checks": {
                        "consistency_score": <tutarlılık_skoru>,
                        "profile_completeness": <tamamlanma_oranı>,
                        "conflicting_preferences": ["<çelişkili_tercih>"]
                    }
                }
                """,
                
                context="Geri bildirim kullanıcının stil profilinde güncelleme gerektiriyor.",
                
                instruction="Stil profili güncellemelerini tutarlı ve doğru şekilde hesapla ve uygula."
            )
        }
    
    def _initialize_coordination_patterns(self) -> Dict[str, FeedbackPromptPattern]:
        """Servisler arası koordinasyon prompt kalıpları"""
        
        return {
            "recommendation_engine_sync": FeedbackPromptPattern(
                persona=self.core_persona + "\nŞu anda servisler arası koordinasyon uzmanı olarak çalışıyorsun.",
                
                recipe="""
                ADIM 1: Geri bildirimin hangi servisleri etkileyeceğini belirle
                ADIM 2: Her servis için gerekli güncellemeleri hesapla
                ADIM 3: Güncelleme sırasını ve bağımlılıklarını planla
                ADIM 4: Her servis için uygun format ve API çağrısını hazırla
                ADIM 5: Koordinasyon mesajlarını sıralı şekilde gönder
                ADIM 6: Güncelleme başarısını doğrula ve loglama yap
                """,
                
                template="""
                {
                    "coordination_plan": {
                        "affected_services": ["<servis1>", "<servis2>"],
                        "update_sequence": [
                            {"service": "<servis>", "order": <sıra>, "dependency": "<bağımlılık>"}
                        ],
                        "coordination_type": "sync|async"
                    },
                    "service_updates": {
                        "<servis_adı>": {
                            "endpoint": "<güncelleme_endpoint>",
                            "payload": {"<parametre>": "<değer>"},
                            "method": "POST|PUT|PATCH",
                            "priority": "high|medium|low"
                        }
                    },
                    "validation_steps": [
                        {"service": "<servis>", "validation_endpoint": "<endpoint>"}
                    ]
                }
                """,
                
                context="Geri bildirim birden fazla serviste güncelleme gerektiriyor.",
                
                instruction="Servisler arası koordinasyonu optimize et ve tutarlı güncellemeleri sağla."
            )
        }
    
    def _initialize_feedback_knowledge(self) -> Dict[str, Any]:
        """Feedback domain bilgi tabanı"""
        
        return {
            "feedback_impact_mapping": {
                "color_related": ["recommendation_engine", "style_profile", "combination_engine"],
                "style_related": ["style_profile", "combination_engine"],
                "occasion_related": ["style_profile", "recommendation_engine"],
                "general_preference": ["all_services"]
            },
            
            "learning_rates": {
                "high_confidence_feedback": 0.8,
                "medium_confidence_feedback": 0.5,
                "low_confidence_feedback": 0.2,
                "contradictory_feedback": 0.1
            },
            
            "update_priorities": {
                "critical": ["user_safety", "major_preference_violation"],
                "high": ["consistent_negative_pattern", "strong_positive_signal"],
                "medium": ["minor_preference_adjustment", "style_refinement"],
                "low": ["exploratory_feedback", "one_off_opinion"]
            },
            
            "coordination_strategies": {
                "immediate_update": ["style_profile", "user_preferences"],
                "batch_update": ["recommendation_scoring", "model_weights"],
                "scheduled_update": ["trend_analysis", "population_insights"]
            }
        }
    
    def analyze_feedback_with_prompt_patterns(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prompt kalıpları kullanarak kullanıcı geri bildirimini kapsamlı analiz et
        
        Args:
            feedback_data: Kullanıcı geri bildirim verisi
            
        Returns:
            Yapılandırılmış analiz sonuçları ve öğrenme aksiyonları
        """
        
        logger.info(f"🔄 Feedback analizi başlıyor: {feedback_data.get('feedback_text', '')[:50]}...")
        
        try:
            # ADIM 1: Feedback Type Classification
            feedback_type = self._classify_feedback_type(feedback_data)
            
            # ADIM 2: Context Analysis
            context_analysis = self._analyze_feedback_context(feedback_data)
            
            # ADIM 3: Impact Assessment
            impact_assessment = self._assess_learning_impact(feedback_data, feedback_type)
            
            # ADIM 4: Learning Action Generation
            learning_actions = self._generate_learning_actions(feedback_type, context_analysis, impact_assessment)
            
            # ADIM 5: Service Coordination Planning
            coordination_plan = self._plan_service_coordination(learning_actions)
            
            # ADIM 6: Structured Response Generation
            structured_response = self._generate_feedback_response(
                feedback_data, feedback_type, context_analysis, impact_assessment, 
                learning_actions, coordination_plan
            )
            
            logger.info("✅ Feedback analizi tamamlandı")
            return structured_response
            
        except Exception as e:
            logger.error(f"❌ Feedback analizi hatası: {e}")
            return self._generate_fallback_feedback_response(feedback_data, str(e))
    
    def _classify_feedback_type(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Geri bildirim türünü sınıflandır"""
        
        feedback_text = feedback_data.get('feedback_text', '').lower()
        
        # Keyword-based classification (can be enhanced with ML models)
        type_scores = {}
        
        # Negative feedback patterns
        negative_keywords = ["beğenmedim", "uygun değil", "hoşuma gitmedi", "kötü", "yanlış"]
        if any(keyword in feedback_text for keyword in negative_keywords):
            type_scores[FeedbackType.NEGATIVE_GENERAL.value] = 0.8
        
        # Color-related feedback
        color_keywords = ["renk", "uyumlu değil", "renkler", "ton", "color"]
        if any(keyword in feedback_text for keyword in color_keywords):
            type_scores[FeedbackType.COLOR_DISSATISFACTION.value] = 0.9
        
        # Positive feedback patterns
        positive_keywords = ["beğendim", "güzel", "hoşuma gitti", "mükemmel", "benzer"]
        if any(keyword in feedback_text for keyword in positive_keywords):
            type_scores[FeedbackType.POSITIVE_GENERAL.value] = 0.8
            
        # Similar request patterns
        similar_keywords = ["benzer", "aynı şekilde", "böyle", "daha fazla"]
        if any(keyword in feedback_text for keyword in similar_keywords):
            type_scores[FeedbackType.REQUEST_SIMILAR.value] = 0.9
        
        best_type = max(type_scores, key=type_scores.get) if type_scores else FeedbackType.NEGATIVE_GENERAL.value
        confidence = type_scores.get(best_type, 0.5)
        
        return {
            "feedback_type": best_type,
            "confidence": confidence,
            "all_scores": type_scores
        }
    
    def _analyze_feedback_context(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Geri bildirim bağlamını analiz et"""
        
        return {
            "user_context": {
                "user_id": feedback_data.get('user_id'),
                "recommendation_id": feedback_data.get('recommendation_id'),
                "session_context": feedback_data.get('session_context', {}),
                "feedback_timestamp": datetime.now().isoformat()
            },
            "recommendation_context": {
                "recommended_items": feedback_data.get('recommended_items', []),
                "occasion": feedback_data.get('occasion'),
                "style_category": feedback_data.get('style_category'),
                "color_palette": feedback_data.get('color_palette', [])
            }
        }
    
    def _assess_learning_impact(self, feedback_data: Dict[str, Any], feedback_type: Dict[str, Any]) -> Dict[str, Any]:
        """Öğrenme etkisini değerlendir"""
        
        feedback_type_value = feedback_type['feedback_type']
        confidence = feedback_type['confidence']
        
        # Determine which services need updates
        affected_services = []
        if 'color' in feedback_type_value:
            affected_services.extend(['style_profile', 'combination_engine', 'recommendation_engine'])
        elif 'positive' in feedback_type_value:
            affected_services.extend(['recommendation_engine', 'style_profile'])
        else:
            affected_services.extend(['style_profile', 'recommendation_engine'])
        
        return {
            "impact_score": confidence,
            "affected_services": affected_services,
            "update_priority": "high" if confidence > 0.7 else "medium",
            "learning_magnitude": "major" if confidence > 0.8 else "moderate"
        }
    
    def _generate_learning_actions(self, feedback_type: Dict[str, Any], 
                                 context_analysis: Dict[str, Any], 
                                 impact_assessment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Öğrenme aksiyonlarını üret"""
        
        actions = []
        
        # Generate service-specific actions based on feedback type
        for service in impact_assessment['affected_services']:
            action = {
                "service": service,
                "action_type": "update_model_weights",
                "parameters": {
                    "user_id": context_analysis['user_context']['user_id'],
                    "feedback_type": feedback_type['feedback_type'],
                    "confidence": feedback_type['confidence'],
                    "recommendation_id": context_analysis['user_context']['recommendation_id']
                },
                "priority": impact_assessment['update_priority']
            }
            actions.append(action)
        
        return actions
    
    def _plan_service_coordination(self, learning_actions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Servis koordinasyonunu planla"""
        
        # Group actions by service and priority
        service_groups = {}
        for action in learning_actions:
            service = action['service']
            if service not in service_groups:
                service_groups[service] = []
            service_groups[service].append(action)
        
        return {
            "coordination_strategy": "sequential",
            "service_update_order": list(service_groups.keys()),
            "service_groups": service_groups,
            "estimated_duration": len(service_groups) * 100  # ms per service
        }
    
    def _generate_feedback_response(self, feedback_data: Dict[str, Any], 
                                  feedback_type: Dict[str, Any],
                                  context_analysis: Dict[str, Any],
                                  impact_assessment: Dict[str, Any],
                                  learning_actions: List[Dict[str, Any]],
                                  coordination_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Final structured response oluştur"""
        
        return {
            "feedback_analysis": {
                "processing_timestamp": datetime.now().isoformat(),
                "feedback_input": feedback_data,
                "analysis_method": "prompt_pattern_engineering"
            },
            "classification_results": feedback_type,
            "context_analysis": context_analysis,
            "impact_assessment": impact_assessment,
            "learning_actions": learning_actions,
            "coordination_plan": coordination_plan,
            "system_updates": {
                "immediate_updates": [action for action in learning_actions if action['priority'] == 'high'],
                "scheduled_updates": [action for action in learning_actions if action['priority'] != 'high']
            },
            "confidence_overall": feedback_type['confidence'],
            "processing_status": "success"
        }
    
    def _generate_fallback_feedback_response(self, feedback_data: Dict[str, Any], error: str) -> Dict[str, Any]:
        """Fallback response oluştur"""
        
        return {
            "feedback_analysis": {
                "processing_timestamp": datetime.now().isoformat(),
                "feedback_input": feedback_data,
                "status": "fallback_mode",
                "error": error
            },
            "classification_results": {
                "feedback_type": "general_feedback",
                "confidence": 0.3
            },
            "learning_actions": [],
            "processing_status": "error"
        }

# Factory function for easy initialization
def create_feedback_prompt_engine() -> AuraFeedbackPromptEngine:
    """Create and return an instance of Feedback Prompt Engine"""
    return AuraFeedbackPromptEngine()
