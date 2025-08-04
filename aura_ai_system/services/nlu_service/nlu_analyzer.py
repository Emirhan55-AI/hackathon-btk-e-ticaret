# Phase 3: Advanced NLU Analyzer with XLM-R Transformer
# This module provides multilingual natural language understanding capabilities
# using state-of-the-art transformer models for intent classification and entity extraction

import torch
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from transformers import (
    AutoTokenizer, AutoModel, AutoConfig,
    pipeline, Pipeline
)
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from langdetect import detect, DetectorFactory
import logging
import warnings
import re

# Set consistent seed for reproducible language detection
DetectorFactory.seed = 42

# Configure logging for detailed analysis tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress transformer warnings for cleaner output
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")

class AdvancedNLUAnalyzer:
    """
    Advanced Natural Language Understanding analyzer using XLM-R transformer model.
    
    This class provides comprehensive multilingual text analysis including:
    - Intent classification using transformer embeddings
    - Entity extraction and recognition
    - Sentiment analysis with confidence scoring
    - Context and occasion detection
    - Multilingual support for EN, TR, ES, FR, DE
    
    The analyzer uses XLM-R (Cross-lingual Language Model - RoBERTa) for
    multilingual understanding and sentence transformers for semantic analysis.
    """
    
    def __init__(self):
        """
        Initialize the NLU analyzer with XLM-R and supporting models.
        
        Loads and configures:
        - XLM-R base model for multilingual understanding
        - Sentence transformer for semantic embeddings
        - Sentiment analysis pipeline
        - Intent and entity recognition components
        """
        
        logger.info("Initializing Advanced NLU Analyzer with XLM-R...")
        
        # Detect available device (GPU/CPU) for optimal performance
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        
        # Initialize model loading success tracking
        self.models_loaded = {
            'xlm_r': False,
            'sentence_transformer': False,
            'sentiment_pipeline': False
        }
        
        try:
            # Load XLM-R model for multilingual understanding
            # XLM-R is trained on 100 languages and excels at cross-lingual tasks
            self.xlm_r_model_name = "xlm-roberta-base"
            logger.info(f"Loading XLM-R model: {self.xlm_r_model_name}")
            
            self.xlm_r_tokenizer = AutoTokenizer.from_pretrained(self.xlm_r_model_name)
            self.xlm_r_model = AutoModel.from_pretrained(self.xlm_r_model_name)
            self.xlm_r_model.to(self.device)
            self.xlm_r_model.eval()  # Set to evaluation mode for inference
            
            self.models_loaded['xlm_r'] = True
            logger.info("✅ XLM-R model loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to load XLM-R model: {e}")
            self.xlm_r_model = None
            self.xlm_r_tokenizer = None
        
        try:
            # Load sentence transformer for semantic similarity
            # This model creates dense vector representations for semantic analysis
            self.sentence_model_name = "all-MiniLM-L6-v2"
            logger.info(f"Loading sentence transformer: {self.sentence_model_name}")
            
            self.sentence_model = SentenceTransformer(self.sentence_model_name)
            self.sentence_model.to(self.device)
            
            self.models_loaded['sentence_transformer'] = True
            logger.info("✅ Sentence transformer loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to load sentence transformer: {e}")
            self.sentence_model = None
        
        try:
            # Load sentiment analysis pipeline
            # Uses a pre-trained model optimized for multilingual sentiment detection
            logger.info("Loading sentiment analysis pipeline...")
            
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-xlm-roberta-base-sentiment",
                device=0 if torch.cuda.is_available() else -1,
                return_all_scores=True
            )
            
            self.models_loaded['sentiment_pipeline'] = True
            logger.info("✅ Sentiment analysis pipeline loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to load sentiment pipeline: {e}")
            self.sentiment_pipeline = None
        
        # Initialize predefined intent categories with example phrases
        # These serve as reference points for intent classification
        self.intent_categories = {
            "product_recommendation": [
                "I want to buy a dress", "recommend me shoes", "looking for a jacket",
                "suggest some clothes", "I need new clothes", "show me fashion items",
                # Turkish examples
                "elbise önerir misin", "ayakkabı arıyorum", "kıyafet önerisi",
                # Spanish examples  
                "busco un vestido", "recomiéndame zapatos", "necesito ropa nueva",
                # French examples
                "je cherche une robe", "recommandez-moi des chaussures", "j'ai besoin de vêtements",
                # German examples
                "ich suche ein kleid", "empfehlen sie mir schuhe", "ich brauche neue kleidung"
            ],
            "style_combination": [
                "how to combine this outfit", "what goes with this shirt", "style suggestions",
                "match my clothes", "outfit coordination", "clothing combinations",
                # Turkish examples
                "bu kıyafetle ne giyebilirim", "kombinleme önerisi", "stil önerisi",
                # Spanish examples
                "qué combina con esta camisa", "sugerencias de estilo", "coordinación de ropa",
                # French examples
                "qu'est-ce qui va avec cette chemise", "suggestions de style", "coordination vestimentaire", 
                # German examples
                "was passt zu diesem hemd", "stil vorschläge", "kleidung koordination"
            ],
            "style_analysis": [
                "what's my style", "analyze my fashion", "describe my look",
                "what style am I", "fashion personality", "style assessment",
                # Turkish examples
                "stilim nedir", "tarzımı analiz et", "moda kişiliğim",
                # Spanish examples
                "cuál es mi estilo", "analiza mi moda", "personalidad de moda",
                # French examples
                "quel est mon style", "analysez ma mode", "personnalité de mode",
                # German examples
                "was ist mein stil", "analysiere meine mode", "mode persönlichkeit"
            ],
            "size_fit_query": [
                "what size should I buy", "does this fit me", "size recommendation",
                "fit advice", "sizing help", "measurement guidance",
                # Turkish examples
                "hangi beden almalıyım", "bu bana uyar mı", "beden önerisi",
                # Spanish examples
                "qué talla debería comprar", "me queda bien esto", "recomendación de talla",
                # French examples
                "quelle taille dois-je acheter", "est-ce que ça me va", "recommandation de taille",
                # German examples
                "welche größe soll ich kaufen", "passt mir das", "größenempfehlung"
            ]
        }
        
        # Initialize context categories for occasion detection
        self.context_categories = {
            "casual": ["daily", "everyday", "casual", "relaxed", "comfortable", "günlük", "rahat", "diario", "quotidien", "alltäglich"],
            "formal": ["business", "work", "professional", "formal", "office", "iş", "profesyonel", "resmi", "trabajo", "profesional", "travail", "formel", "geschäft", "formell"],
            "party": ["party", "celebration", "event", "festive", "party", "parti", "kutlama", "etkinlik", "fiesta", "celebración", "fête", "événement", "feier", "veranstaltung"],
            "sport": ["sport", "gym", "workout", "athletic", "exercise", "fitness", "spor", "jimnastik", "antrenman", "deporte", "gimnasio", "ejercicio", "sport", "gymnastique", "entraînement", "sport", "fitnessstudio", "training"],
            "travel": ["travel", "vacation", "trip", "holiday", "journey", "seyahat", "tatil", "gezi", "viaje", "vacaciones", "voyage", "vacances", "reise", "urlaub"],
            "date": ["date", "romantic", "dinner", "restaurant", "evening", "randevu", "romantik", "akşam yemeği", "cita", "romántico", "cena", "rendez-vous", "romantique", "dîner", "date", "romantisch", "abendessen"]
        }
        
        # Precompute embeddings for intent and context categories if models are available
        self._precompute_category_embeddings()
        
        logger.info(f"Advanced NLU Analyzer initialized. Models loaded: {sum(self.models_loaded.values())}/3")
    
    def _precompute_category_embeddings(self):
        """
        Precompute embeddings for intent and context categories for efficient classification.
        
        This method creates dense vector representations of all predefined categories
        using the sentence transformer model. These embeddings are used for fast
        similarity-based classification during inference.
        """
        
        if not self.sentence_model:
            logger.warning("Sentence model not available - using fallback classification")
            self.intent_embeddings = {}
            self.context_embeddings = {}
            return
        
        try:
            logger.info("Precomputing category embeddings for efficient classification...")
            
            # Compute intent category embeddings
            self.intent_embeddings = {}
            for intent, examples in self.intent_categories.items():
                # Combine all examples for this intent into embeddings
                embeddings = self.sentence_model.encode(examples)
                # Use mean embedding as the representative vector for this intent
                self.intent_embeddings[intent] = np.mean(embeddings, axis=0)
            
            # Compute context category embeddings  
            self.context_embeddings = {}
            for context, keywords in self.context_categories.items():
                # Create simple phrases from keywords for better embedding quality
                phrases = [f"I want something for {keyword} occasions" for keyword in keywords[:3]]
                embeddings = self.sentence_model.encode(phrases)
                self.context_embeddings[context] = np.mean(embeddings, axis=0)
            
            logger.info("✅ Category embeddings precomputed successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to precompute embeddings: {e}")
            self.intent_embeddings = {}
            self.context_embeddings = {}
    
    def detect_language(self, text: str) -> Tuple[str, float]:
        """
        Detect the language of input text with confidence scoring.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Tuple of (language_code, confidence_score)
            
        Supported languages: en, tr, es, fr, de
        """
        
        try:
            # Use langdetect library for language identification
            detected_lang = detect(text)
            
            # Map to supported languages or default to English
            supported_langs = {'en', 'tr', 'es', 'fr', 'de'}
            if detected_lang in supported_langs:
                return detected_lang, 0.95  # High confidence for direct match
            else:
                return 'en', 0.7  # Default to English with lower confidence
                
        except Exception as e:
            logger.warning(f"Language detection failed: {e}, defaulting to English")
            return 'en', 0.5  # Default with low confidence
    
    def extract_xlm_r_features(self, text: str) -> Optional[np.ndarray]:
        """
        Extract XLM-R transformer features from input text.
        
        Args:
            text: Input text to process
            
        Returns:
            768-dimensional feature vector from XLM-R model, or None if model unavailable
        """
        
        if not self.xlm_r_model or not self.xlm_r_tokenizer:
            return None
        
        try:
            # Tokenize input text for XLM-R model
            inputs = self.xlm_r_tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            ).to(self.device)
            
            # Extract features using XLM-R model
            with torch.no_grad():
                outputs = self.xlm_r_model(**inputs)
                # Use [CLS] token embedding as sentence representation
                cls_embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy()
                
            return cls_embedding.flatten()
            
        except Exception as e:
            logger.error(f"XLM-R feature extraction failed: {e}")
            return None
    
    def classify_intent(self, text: str) -> Dict[str, Any]:
        """
        Classify user intent using semantic similarity with predefined categories.
        
        Args:
            text: User input text
            
        Returns:
            Dictionary with intent classification results
        """
        
        if self.sentence_model and self.intent_embeddings:
            try:
                # Get embedding for input text
                text_embedding = self.sentence_model.encode([text])
                
                # Calculate similarity with each intent category
                similarities = {}
                for intent, intent_embedding in self.intent_embeddings.items():
                    similarity = cosine_similarity(text_embedding, [intent_embedding])[0][0]
                    similarities[intent] = float(similarity)
                
                # Find best matching intent
                best_intent = max(similarities, key=similarities.get)
                confidence = similarities[best_intent]
                
                return {
                    "intent": best_intent,
                    "confidence": confidence,
                    "all_scores": similarities,
                    "method": "transformer_similarity"
                }
                
            except Exception as e:
                logger.error(f"Transformer-based intent classification failed: {e}")
                
        # Fallback to keyword-based classification
        return self._fallback_intent_classification(text)
    
    def _fallback_intent_classification(self, text: str) -> Dict[str, Any]:
        """
        Fallback intent classification using keyword matching.
        
        Args:
            text: Input text to classify
            
        Returns:
            Intent classification result with lower confidence
        """
        
        text_lower = text.lower()
        
        # Check for product recommendation keywords
        if any(word in text_lower for word in ["recommend", "suggest", "want", "need", "looking for", "buy", "purchase"]):
            return {"intent": "product_recommendation", "confidence": 0.7, "method": "keyword_fallback"}
        
        # Check for style combination keywords
        elif any(word in text_lower for word in ["combine", "match", "outfit", "coordination", "goes with"]):
            return {"intent": "style_combination", "confidence": 0.7, "method": "keyword_fallback"}
        
        # Check for style analysis keywords
        elif any(word in text_lower for word in ["my style", "analyze", "what am i", "fashion personality"]):
            return {"intent": "style_analysis", "confidence": 0.7, "method": "keyword_fallback"}
        
        # Check for size/fit keywords
        elif any(word in text_lower for word in ["size", "fit", "measurement", "does this fit"]):
            return {"intent": "size_fit_query", "confidence": 0.7, "method": "keyword_fallback"}
        
        else:
            return {"intent": "general_inquiry", "confidence": 0.5, "method": "keyword_fallback"}
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of input text using multilingual sentiment model.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Sentiment analysis results with confidence scores
        """
        
        if self.sentiment_pipeline:
            try:
                # Use transformer-based sentiment analysis
                results = self.sentiment_pipeline(text)
                
                # Process results to get cleaner output
                sentiment_scores = {result['label'].lower(): result['score'] for result in results[0]}
                
                # Map labels to standardized sentiment categories
                label_mapping = {
                    'positive': 'positive',
                    'negative': 'negative', 
                    'neutral': 'neutral',
                    'label_1': 'negative',  # Some models use numbered labels
                    'label_2': 'neutral',
                    'label_3': 'positive'
                }
                
                # Find dominant sentiment
                best_label = max(sentiment_scores, key=sentiment_scores.get)
                mapped_sentiment = label_mapping.get(best_label, 'neutral')
                confidence = sentiment_scores[best_label]
                
                return {
                    "sentiment": mapped_sentiment,
                    "confidence": confidence,
                    "all_scores": sentiment_scores,
                    "method": "transformer_pipeline"
                }
                
            except Exception as e:
                logger.error(f"Transformer sentiment analysis failed: {e}")
        
        # Fallback to simple keyword-based sentiment analysis
        return self._fallback_sentiment_analysis(text)
    
    def _fallback_sentiment_analysis(self, text: str) -> Dict[str, Any]:
        """
        Fallback sentiment analysis using keyword matching.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Basic sentiment classification
        """
        
        text_lower = text.lower()
        
        # Positive sentiment keywords (multilingual)
        positive_words = ["good", "great", "excellent", "amazing", "beautiful", "love", "perfect", "wonderful",
                         "güzel", "harika", "mükemmel", "seviyorum", "bueno", "excelente", "perfecto",
                         "bon", "excellent", "parfait", "gut", "ausgezeichnet", "perfekt"]
        
        # Negative sentiment keywords (multilingual)  
        negative_words = ["bad", "terrible", "awful", "hate", "horrible", "worst", "disgusting",
                         "kötü", "berbat", "nefret", "malo", "terrible", "odio", "mauvais", "terrible",
                         "schlecht", "schrecklich", "hasse"]
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return {"sentiment": "positive", "confidence": 0.6, "method": "keyword_fallback"}
        elif negative_count > positive_count:
            return {"sentiment": "negative", "confidence": 0.6, "method": "keyword_fallback"}
        else:
            return {"sentiment": "neutral", "confidence": 0.5, "method": "keyword_fallback"}
    
    def detect_context(self, text: str) -> Dict[str, Any]:
        """
        Detect context/occasion from input text using semantic similarity.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Context classification results
        """
        
        if self.sentence_model and self.context_embeddings:
            try:
                # Get embedding for input text
                text_embedding = self.sentence_model.encode([text])
                
                # Calculate similarity with each context category
                similarities = {}
                for context, context_embedding in self.context_embeddings.items():
                    similarity = cosine_similarity(text_embedding, [context_embedding])[0][0]
                    similarities[context] = float(similarity)
                
                # Find best matching context
                best_context = max(similarities, key=similarities.get)
                confidence = similarities[best_context]
                
                return {
                    "context": best_context,
                    "confidence": confidence,
                    "all_scores": similarities,
                    "method": "transformer_similarity"
                }
                
            except Exception as e:
                logger.error(f"Transformer-based context detection failed: {e}")
        
        # Fallback to keyword-based context detection
        return self._fallback_context_detection(text)
    
    def _fallback_context_detection(self, text: str) -> Dict[str, Any]:
        """
        Fallback context detection using keyword matching.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Context classification using keyword matching
        """
        
        text_lower = text.lower()
        
        # Check each context category for keyword matches
        for context, keywords in self.context_categories.items():
            if any(keyword in text_lower for keyword in keywords):
                return {"context": context, "confidence": 0.7, "method": "keyword_fallback"}
        
        # Default to casual context
        return {"context": "casual", "confidence": 0.5, "method": "keyword_fallback"}
    
    def comprehensive_analysis(self, text: str) -> Dict[str, Any]:
        """
        Perform comprehensive NLU analysis combining all components.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Complete analysis results including intent, sentiment, context, and language
        """
        
        logger.info(f"Performing comprehensive NLU analysis on: '{text[:50]}...'")
        
        try:
            # Language detection
            language, lang_confidence = self.detect_language(text)
            
            # Intent classification
            intent_results = self.classify_intent(text)
            
            # Sentiment analysis
            sentiment_results = self.analyze_sentiment(text)
            
            # Context detection
            context_results = self.detect_context(text)
            
            # Extract XLM-R features if available
            xlm_r_features = self.extract_xlm_r_features(text)
            
            # Combine all analysis results
            analysis_results = {
                "language_detection": {
                    "detected_language": language,
                    "confidence": lang_confidence
                },
                "intent_analysis": intent_results,
                "sentiment_analysis": sentiment_results,
                "context_analysis": context_results,
                "features": {
                    "xlm_r_embedding": xlm_r_features.tolist() if xlm_r_features is not None else None,
                    "embedding_dimension": len(xlm_r_features) if xlm_r_features is not None else 0
                },
                "model_status": self.models_loaded,
                "processing_metadata": {
                    "total_models_used": sum(1 for method in [
                        intent_results.get('method', ''),
                        sentiment_results.get('method', ''),
                        context_results.get('method', '')
                    ] if 'transformer' in method),
                    "text_length": len(text),
                    "analysis_quality": "high" if sum(self.models_loaded.values()) >= 2 else "medium"
                }
            }
            
            logger.info(f"✅ Comprehensive analysis completed successfully")
            return analysis_results
            
        except Exception as e:
            logger.error(f"❌ Comprehensive analysis failed: {e}")
            return {
                "error": str(e),
                "fallback_available": True,
                "model_status": self.models_loaded
            }
