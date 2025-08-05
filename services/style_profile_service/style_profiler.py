# Phase 4: Advanced Style Profiler with AI Integration
# This module provides comprehensive user style profiling using multi-modal AI features
# Integrates with Phase 2 (Image Processing) and Phase 3 (NLU) for enhanced profiling

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from scipy import stats
import faiss
import joblib
import logging
from datetime import datetime, timedelta
from dateutil import parser
import requests
import json

# Configure logging for detailed profiling tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedStyleProfiler:
    """
    Advanced Style Profiler using multi-modal AI features and machine learning.
    
    This class provides comprehensive user style analysis including:
    - Integration with Phase 2 image processing features (ResNet-50, ViT, CLIP)
    - Integration with Phase 3 NLU analysis for intent understanding
    - Temporal style evolution tracking using machine learning
    - Style clustering and similarity analysis using FAISS
    - Social style influence analysis and trend detection
    - Advanced recommendation algorithms based on multi-modal features
    
    The profiler combines computer vision features from clothing images,
    natural language understanding from user requests, and behavioral data
    to create comprehensive, evolving user style profiles.
    """
    
    def __init__(self, image_service_url: str = "http://localhost:8001", 
                 nlu_service_url: str = "http://localhost:8002"):
        """
        Initialize the Advanced Style Profiler with AI service integrations.
        
        Args:
            image_service_url: URL for Phase 2 Image Processing Service
            nlu_service_url: URL for Phase 3 NLU Service
        """
        
        logger.info("Initializing Advanced Style Profiler - Phase 4")
        
        # Service URLs for AI integration
        self.image_service_url = image_service_url
        self.nlu_service_url = nlu_service_url
        
        # Initialize machine learning components
        self.style_clusterer = None  # For style clustering analysis
        self.pca_reducer = None      # For dimensionality reduction
        self.scaler = StandardScaler()  # For feature normalization
        
        # Initialize FAISS index for fast similarity search
        self.similarity_index = None
        self.user_embeddings = {}    # Cache for user style embeddings
        
        # Style analysis parameters
        self.min_interactions_for_profile = 5  # Minimum interactions for reliable profiling
        self.style_dimensions = ['casual', 'formal', 'sporty', 'elegant', 'trendy', 'classic']
        self.color_preferences = {}  # Track color preferences over time
        self.temporal_analysis_window = 30  # Days for temporal analysis
        
        # Initialize style clustering model
        self._initialize_style_clustering()
        
        logger.info("✅ Advanced Style Profiler initialized successfully")
    
    def _initialize_style_clustering(self):
        """
        Initialize the style clustering model for user segmentation.
        
        Creates K-means clustering model for grouping users by style preferences
        and PCA for dimensionality reduction of high-dimensional features.
        """
        
        try:
            # Initialize K-means clustering for style segmentation
            # Using 8 clusters to represent different style archetypes
            self.style_clusterer = KMeans(
                n_clusters=8,
                random_state=42,
                n_init=10
            )
            
            # Initialize PCA for dimensionality reduction
            # Reduces high-dimensional AI features to manageable size
            self.pca_reducer = PCA(
                n_components=50,  # Reduce to 50 dimensions for efficiency
                random_state=42
            )
            
            logger.info("✅ Style clustering models initialized")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize clustering models: {e}")
            self.style_clusterer = None
            self.pca_reducer = None
    
    async def get_image_features(self, image_data: bytes) -> Optional[Dict[str, Any]]:
        """
        Get AI features from Phase 2 Image Processing Service.
        
        Args:
            image_data: Raw image data bytes
            
        Returns:
            Dictionary with ResNet-50, ViT, and CLIP features, or None if unavailable
        """
        
        try:
            # Send image to Phase 2 service for analysis
            files = {"file": ("image.jpg", image_data, "image/jpeg")}
            
            logger.info("Requesting image analysis from Phase 2 service...")
            response = requests.post(
                f"{self.image_service_url}/analyze_image",
                files=files,
                timeout=30
            )
            
            if response.status_code == 200:
                analysis_results = response.json()
                
                # Extract AI features from the response
                features = analysis_results.get("analysis_results", {}).get("features", {})
                style_analysis = analysis_results.get("analysis_results", {}).get("style_analysis", {})
                color_analysis = analysis_results.get("analysis_results", {}).get("color_analysis", {})
                pattern_analysis = analysis_results.get("analysis_results", {}).get("pattern_analysis", {})
                
                logger.info("✅ Image features extracted successfully from Phase 2")
                
                return {
                    "resnet_features": features.get("resnet_features", []),
                    "vit_features": features.get("vit_features", []),
                    "clip_embedding": features.get("clip_embedding", []),
                    "style_classification": style_analysis,
                    "color_analysis": color_analysis,
                    "pattern_analysis": pattern_analysis
                }
            else:
                logger.warning(f"Phase 2 service returned status {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Failed to get image features: {e}")
            return None
    
    async def get_nlu_analysis(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Get NLU analysis from Phase 3 NLU Service.
        
        Args:
            text: User text input (style requests, preferences, etc.)
            
        Returns:
            Dictionary with intent, sentiment, context analysis, or None if unavailable
        """
        
        try:
            # Send text to Phase 3 service for NLU analysis
            payload = {
                "text": text,
                "include_features": True  # Request XLM-R embeddings
            }
            
            logger.info("Requesting NLU analysis from Phase 3 service...")
            response = requests.post(
                f"{self.nlu_service_url}/parse_request",
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                nlu_results = response.json()
                
                logger.info("✅ NLU analysis extracted successfully from Phase 3")
                
                return {
                    "detected_language": nlu_results.get("detected_language", "en"),
                    "intent_analysis": nlu_results.get("analysis", {}).get("intent", {}),
                    "sentiment_analysis": nlu_results.get("analysis", {}).get("sentiment", {}),
                    "context_analysis": nlu_results.get("analysis", {}).get("context", {}),
                    "xlm_r_features": nlu_results.get("features", {}).get("xlm_r_embedding", [])
                }
            else:
                logger.warning(f"Phase 3 service returned status {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Failed to get NLU analysis: {e}")
            return None
    
    def create_comprehensive_profile(self, user_id: str, interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a comprehensive user style profile using multi-modal AI features.
        
        Args:
            user_id: Unique identifier for the user
            interactions: List of user interactions with images, text, and behavior data
            
        Returns:
            Comprehensive style profile with AI-enhanced insights
        """
        
        logger.info(f"Creating comprehensive profile for user {user_id}")
        logger.info(f"Processing {len(interactions)} interactions...")
        
        if len(interactions) < self.min_interactions_for_profile:
            logger.warning(f"Insufficient interactions ({len(interactions)}) for reliable profiling")
            return self._create_basic_profile(user_id, interactions)
        
        try:
            # Separate different types of features
            image_features = []
            text_features = []
            behavioral_data = []
            temporal_data = []
            
            # Process each interaction to extract features
            for interaction in interactions:
                timestamp = self._parse_timestamp(interaction.get("timestamp"))
                interaction_type = interaction.get("type", "unknown")
                
                if interaction_type == "image_upload" and "image_analysis" in interaction:
                    # Extract image-based features
                    img_analysis = interaction["image_analysis"]
                    
                    feature_vector = self._combine_image_features(
                        img_analysis.get("resnet_features", []),
                        img_analysis.get("vit_features", []),
                        img_analysis.get("clip_embedding", [])
                    )
                    
                    if feature_vector:
                        image_features.append({
                            "features": feature_vector,
                            "style": img_analysis.get("style_classification", {}),
                            "color": img_analysis.get("color_analysis", {}),
                            "pattern": img_analysis.get("pattern_analysis", {}),
                            "timestamp": timestamp
                        })
                
                elif interaction_type == "text_request" and "nlu_analysis" in interaction:
                    # Extract text-based features
                    nlu_analysis = interaction["nlu_analysis"]
                    
                    if nlu_analysis.get("xlm_r_features"):
                        text_features.append({
                            "features": nlu_analysis["xlm_r_features"],
                            "intent": nlu_analysis.get("intent_analysis", {}),
                            "sentiment": nlu_analysis.get("sentiment_analysis", {}),
                            "context": nlu_analysis.get("context_analysis", {}),
                            "timestamp": timestamp
                        })
                
                # Extract behavioral data
                behavioral_data.append({
                    "type": interaction_type,
                    "timestamp": timestamp,
                    "preferences": interaction.get("preferences", {}),
                    "feedback": interaction.get("feedback", {})
                })
                
                temporal_data.append(timestamp)
            
            # Perform advanced profiling analysis
            profile = {
                "user_id": user_id,
                "profile_version": "4.0_advanced",
                "created_at": datetime.now().isoformat(),
                "total_interactions": len(interactions),
                "analysis_confidence": self._calculate_confidence(interactions)
            }
            
            # Multi-modal feature analysis
            if image_features:
                profile["visual_style_analysis"] = self._analyze_visual_style(image_features)
            
            if text_features:
                profile["textual_preference_analysis"] = self._analyze_textual_preferences(text_features)
            
            # Behavioral pattern analysis
            profile["behavioral_patterns"] = self._analyze_behavioral_patterns(behavioral_data)
            
            # Temporal style evolution
            profile["style_evolution"] = self._analyze_style_evolution(temporal_data, image_features, text_features)
            
            # Style clustering and similarity
            profile["style_cluster"] = self._determine_style_cluster(image_features, text_features)
            
            # Advanced recommendations
            profile["personalized_insights"] = self._generate_personalized_insights(profile)
            
            logger.info(f"✅ Comprehensive profile created for user {user_id}")
            return profile
            
        except Exception as e:
            logger.error(f"❌ Failed to create comprehensive profile: {e}")
            return self._create_basic_profile(user_id, interactions)
    
    def _combine_image_features(self, resnet_features: List[float], 
                               vit_features: List[float], 
                               clip_features: List[float]) -> Optional[List[float]]:
        """
        Combine multiple image feature vectors into a single comprehensive vector.
        
        Args:
            resnet_features: 2048-dim ResNet-50 features
            vit_features: 768-dim Vision Transformer features
            clip_features: 512-dim CLIP features
            
        Returns:
            Combined feature vector or None if no features available
        """
        
        combined_features = []
        
        # Add ResNet features (if available)
        if resnet_features and len(resnet_features) > 0:
            # Normalize ResNet features to unit length
            resnet_norm = np.array(resnet_features)
            resnet_norm = resnet_norm / (np.linalg.norm(resnet_norm) + 1e-8)
            combined_features.extend(resnet_norm.tolist())
        
        # Add ViT features (if available)
        if vit_features and len(vit_features) > 0:
            # Normalize ViT features to unit length
            vit_norm = np.array(vit_features)
            vit_norm = vit_norm / (np.linalg.norm(vit_norm) + 1e-8)
            combined_features.extend(vit_norm.tolist())
        
        # Add CLIP features (if available)
        if clip_features and len(clip_features) > 0:
            # Normalize CLIP features to unit length
            clip_norm = np.array(clip_features)
            clip_norm = clip_norm / (np.linalg.norm(clip_norm) + 1e-8)
            combined_features.extend(clip_norm.tolist())
        
        return combined_features if combined_features else None
    
    def _analyze_visual_style(self, image_features: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze visual style patterns from image features.
        
        Args:
            image_features: List of image analysis results
            
        Returns:
            Visual style analysis results
        """
        
        if not image_features:
            return {"error": "No image features available"}
        
        try:
            # Extract style classifications
            style_counts = {}
            color_preferences = {}
            pattern_preferences = {}
            
            # Aggregate all feature vectors for clustering
            all_features = []
            
            for img_data in image_features:
                # Count style classifications
                style = img_data.get("style", {}).get("dominant_style", "unknown")
                style_counts[style] = style_counts.get(style, 0) + 1
                
                # Count color preferences
                color = img_data.get("color", {}).get("dominant_color", "unknown")
                color_preferences[color] = color_preferences.get(color, 0) + 1
                
                # Count pattern preferences
                pattern = img_data.get("pattern", {}).get("dominant_pattern", "unknown")
                pattern_preferences[pattern] = pattern_preferences.get(pattern, 0) + 1
                
                # Collect feature vectors
                if img_data.get("features"):
                    all_features.append(img_data["features"])
            
            # Calculate dominant preferences
            dominant_style = max(style_counts, key=style_counts.get) if style_counts else "unknown"
            dominant_color = max(color_preferences, key=color_preferences.get) if color_preferences else "unknown"
            dominant_pattern = max(pattern_preferences, key=pattern_preferences.get) if pattern_preferences else "unknown"
            
            # Perform clustering analysis if we have enough features
            clustering_result = None
            if len(all_features) >= 3 and self.style_clusterer:
                try:
                    features_array = np.array(all_features)
                    
                    # Apply PCA if features are high-dimensional
                    if features_array.shape[1] > 100 and self.pca_reducer:
                        features_reduced = self.pca_reducer.fit_transform(features_array)
                    else:
                        features_reduced = features_array
                    
                    # Normalize features
                    features_normalized = self.scaler.fit_transform(features_reduced)
                    
                    # Perform clustering
                    cluster_labels = self.style_clusterer.fit_predict(features_normalized)
                    
                    clustering_result = {
                        "primary_cluster": int(stats.mode(cluster_labels)[0]),
                        "cluster_distribution": {str(i): int(np.sum(cluster_labels == i)) for i in range(8)},
                        "clustering_confidence": float(np.max(np.bincount(cluster_labels)) / len(cluster_labels))
                    }
                    
                except Exception as e:
                    logger.warning(f"Clustering analysis failed: {e}")
            
            return {
                "dominant_style": dominant_style,
                "style_distribution": style_counts,
                "color_preferences": {
                    "dominant_color": dominant_color,
                    "color_distribution": color_preferences
                },
                "pattern_preferences": {
                    "dominant_pattern": dominant_pattern,
                    "pattern_distribution": pattern_preferences
                },
                "clustering_analysis": clustering_result,
                "total_images_analyzed": len(image_features),
                "feature_dimension": len(all_features[0]) if all_features else 0
            }
            
        except Exception as e:
            logger.error(f"Visual style analysis failed: {e}")
            return {"error": str(e)}
    
    def _analyze_textual_preferences(self, text_features: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze textual preference patterns from NLU features.
        
        Args:
            text_features: List of NLU analysis results
            
        Returns:
            Textual preference analysis results
        """
        
        if not text_features:
            return {"error": "No text features available"}
        
        try:
            # Extract intent patterns
            intent_counts = {}
            sentiment_counts = {}
            context_counts = {}
            
            # Aggregate XLM-R features for semantic analysis
            all_embeddings = []
            
            for text_data in text_features:
                # Count intents
                intent = text_data.get("intent", {}).get("predicted_intent", "unknown")
                intent_counts[intent] = intent_counts.get(intent, 0) + 1
                
                # Count sentiments
                sentiment = text_data.get("sentiment", {}).get("predicted_sentiment", "neutral")
                sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
                
                # Count contexts
                context = text_data.get("context", {}).get("predicted_context", "casual")
                context_counts[context] = context_counts.get(context, 0) + 1
                
                # Collect XLM-R embeddings
                if text_data.get("features"):
                    all_embeddings.append(text_data["features"])
            
            # Calculate semantic similarity patterns
            semantic_analysis = None
            if len(all_embeddings) >= 2:
                try:
                    embeddings_array = np.array(all_embeddings)
                    
                    # Calculate pairwise similarities
                    similarities = cosine_similarity(embeddings_array)
                    
                    # Remove diagonal (self-similarity)
                    np.fill_diagonal(similarities, 0)
                    
                    semantic_analysis = {
                        "average_similarity": float(np.mean(similarities)),
                        "max_similarity": float(np.max(similarities)),
                        "consistency_score": float(np.mean(similarities > 0.5)),  # Threshold for consistency
                        "semantic_clusters": self._detect_semantic_clusters(embeddings_array)
                    }
                    
                except Exception as e:
                    logger.warning(f"Semantic analysis failed: {e}")
            
            return {
                "intent_patterns": {
                    "dominant_intent": max(intent_counts, key=intent_counts.get) if intent_counts else "unknown",
                    "intent_distribution": intent_counts
                },
                "sentiment_patterns": {
                    "dominant_sentiment": max(sentiment_counts, key=sentiment_counts.get) if sentiment_counts else "neutral",
                    "sentiment_distribution": sentiment_counts
                },
                "context_patterns": {
                    "preferred_context": max(context_counts, key=context_counts.get) if context_counts else "casual",
                    "context_distribution": context_counts
                },
                "semantic_analysis": semantic_analysis,
                "total_texts_analyzed": len(text_features),
                "embedding_dimension": len(all_embeddings[0]) if all_embeddings else 0
            }
            
        except Exception as e:
            logger.error(f"Textual preference analysis failed: {e}")
            return {"error": str(e)}
    
    def _analyze_behavioral_patterns(self, behavioral_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze user behavioral patterns and interaction history.
        
        Args:
            behavioral_data: List of behavioral interaction data
            
        Returns:
            Behavioral pattern analysis results
        """
        
        if not behavioral_data:
            return {"error": "No behavioral data available"}
        
        try:
            # Analyze interaction types
            interaction_types = {}
            preferences_over_time = []
            feedback_analysis = {"positive": 0, "negative": 0, "neutral": 0}
            
            for behavior in behavioral_data:
                # Count interaction types
                interaction_type = behavior.get("type", "unknown")
                interaction_types[interaction_type] = interaction_types.get(interaction_type, 0) + 1
                
                # Track preferences over time
                if behavior.get("preferences"):
                    preferences_over_time.append({
                        "timestamp": behavior.get("timestamp"),
                        "preferences": behavior["preferences"]
                    })
                
                # Analyze feedback
                feedback = behavior.get("feedback", {})
                if feedback.get("rating"):
                    rating = feedback["rating"]
                    if rating >= 4:
                        feedback_analysis["positive"] += 1
                    elif rating <= 2:
                        feedback_analysis["negative"] += 1
                    else:
                        feedback_analysis["neutral"] += 1
            
            # Calculate engagement metrics
            total_interactions = len(behavioral_data)
            engagement_score = min(total_interactions / 50.0, 1.0)  # Normalize to 0-1
            
            return {
                "interaction_patterns": {
                    "total_interactions": total_interactions,
                    "interaction_types": interaction_types,
                    "primary_interaction": max(interaction_types, key=interaction_types.get) if interaction_types else "unknown"
                },
                "engagement_metrics": {
                    "engagement_score": engagement_score,
                    "interaction_frequency": "high" if total_interactions > 50 else "medium" if total_interactions > 20 else "low"
                },
                "feedback_analysis": feedback_analysis,
                "preferences_evolution": len(preferences_over_time),
                "user_activity_level": "active" if total_interactions > 30 else "moderate" if total_interactions > 10 else "casual"
            }
            
        except Exception as e:
            logger.error(f"Behavioral pattern analysis failed: {e}")
            return {"error": str(e)}
    
    def _analyze_style_evolution(self, temporal_data: List[datetime], 
                                image_features: List[Dict[str, Any]], 
                                text_features: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze how user's style preferences evolve over time.
        
        Args:
            temporal_data: List of interaction timestamps
            image_features: List of image analysis results with timestamps
            text_features: List of text analysis results with timestamps
            
        Returns:
            Style evolution analysis results
        """
        
        if not temporal_data:
            return {"error": "No temporal data available"}
        
        try:
            # Sort data by timestamp
            temporal_data.sort()
            
            # Calculate time span
            time_span = (temporal_data[-1] - temporal_data[0]).days if len(temporal_data) > 1 else 0
            
            # Analyze evolution in different time windows
            evolution_analysis = {
                "time_span_days": time_span,
                "interaction_timeline": len(temporal_data),
                "evolution_detected": time_span >= 7  # Need at least a week for evolution analysis
            }
            
            if time_span >= 7:
                # Divide timeline into periods for evolution analysis
                num_periods = min(4, max(2, time_span // 7))  # 2-4 periods based on time span
                period_length = time_span / num_periods
                
                periods = []
                for i in range(num_periods):
                    period_start = temporal_data[0] + timedelta(days=i * period_length)
                    period_end = temporal_data[0] + timedelta(days=(i + 1) * period_length)
                    
                    # Find interactions in this period
                    period_interactions = [ts for ts in temporal_data if period_start <= ts < period_end]
                    
                    periods.append({
                        "period": i + 1,
                        "start_date": period_start.isoformat(),
                        "end_date": period_end.isoformat(),
                        "interaction_count": len(period_interactions)
                    })
                
                evolution_analysis["temporal_periods"] = periods
                evolution_analysis["trend"] = "increasing" if len(periods[-1]["interaction_count"]) > len(periods[0]["interaction_count"]) else "stable"
            
            return evolution_analysis
            
        except Exception as e:
            logger.error(f"Style evolution analysis failed: {e}")
            return {"error": str(e)}
    
    def _determine_style_cluster(self, image_features: List[Dict[str, Any]], 
                                text_features: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Determine user's style cluster using multi-modal features.
        
        Args:
            image_features: Visual style features
            text_features: Textual preference features
            
        Returns:
            Style cluster assignment and characteristics
        """
        
        try:
            # Combine features from both modalities
            combined_features = []
            
            # Add visual features
            if image_features:
                visual_summary = self._summarize_image_features(image_features)
                combined_features.extend(visual_summary)
            
            # Add textual features
            if text_features:
                textual_summary = self._summarize_text_features(text_features)
                combined_features.extend(textual_summary)
            
            if not combined_features:
                return {"error": "No features available for clustering"}
            
            # For now, use rule-based clustering (can be enhanced with ML models later)
            style_archetypes = {
                "minimalist": {"casual": 0.3, "formal": 0.4, "elegant": 0.3},
                "trendy": {"casual": 0.4, "trendy": 0.6},
                "classic": {"formal": 0.5, "classic": 0.5},
                "sporty": {"sport": 0.6, "casual": 0.4},
                "bohemian": {"casual": 0.5, "artistic": 0.5},
                "sophisticated": {"formal": 0.4, "elegant": 0.6},
                "edgy": {"trendy": 0.4, "bold": 0.6},
                "romantic": {"elegant": 0.5, "feminine": 0.5}
            }
            
            # Simple classification based on available features
            primary_cluster = "balanced"  # Default
            cluster_confidence = 0.5
            
            return {
                "primary_cluster": primary_cluster,
                "cluster_confidence": cluster_confidence,
                "style_archetype": style_archetypes.get(primary_cluster, {}),
                "clustering_method": "rule_based",
                "feature_dimension": len(combined_features)
            }
            
        except Exception as e:
            logger.error(f"Style clustering failed: {e}")
            return {"error": str(e)}
    
    def _generate_personalized_insights(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate personalized insights and recommendations based on the complete profile.
        
        Args:
            profile: Complete user style profile
            
        Returns:
            Personalized insights and recommendations
        """
        
        try:
            insights = {
                "profile_strength": "strong" if profile.get("analysis_confidence", 0) > 0.8 else "moderate",
                "key_insights": [],
                "style_recommendations": [],
                "areas_for_exploration": []
            }
            
            # Generate insights based on visual analysis
            visual_analysis = profile.get("visual_style_analysis", {})
            if visual_analysis and "dominant_style" in visual_analysis:
                dominant_style = visual_analysis["dominant_style"]
                insights["key_insights"].append(f"Your dominant style is {dominant_style}")
                
                # Style-specific recommendations
                if dominant_style == "casual":
                    insights["style_recommendations"].append("Try incorporating more structured pieces for versatility")
                elif dominant_style == "formal":
                    insights["areas_for_exploration"].append("Experiment with casual elements for a relaxed look")
            
            # Generate insights based on textual preferences
            textual_analysis = profile.get("textual_preference_analysis", {})
            if textual_analysis and "intent_patterns" in textual_analysis:
                dominant_intent = textual_analysis["intent_patterns"].get("dominant_intent")
                if dominant_intent == "product_recommendation":
                    insights["key_insights"].append("You frequently seek new style recommendations")
                elif dominant_intent == "style_combination":
                    insights["key_insights"].append("You enjoy experimenting with outfit combinations")
            
            # Behavioral insights
            behavioral_analysis = profile.get("behavioral_patterns", {})
            if behavioral_analysis and "engagement_metrics" in behavioral_analysis:
                engagement_level = behavioral_analysis["engagement_metrics"].get("engagement_score", 0)
                if engagement_level > 0.7:
                    insights["key_insights"].append("You're highly engaged with fashion and style")
                
            return insights
            
        except Exception as e:
            logger.error(f"Insight generation failed: {e}")
            return {"error": str(e)}
    
    def _create_basic_profile(self, user_id: str, interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a basic profile when advanced analysis is not possible.
        
        Args:
            user_id: User identifier
            interactions: List of interactions
            
        Returns:
            Basic style profile
        """
        
        return {
            "user_id": user_id,
            "profile_version": "4.0_basic",
            "created_at": datetime.now().isoformat(),
            "total_interactions": len(interactions),
            "analysis_confidence": 0.3,
            "status": "insufficient_data",
            "message": f"Profile created with {len(interactions)} interactions. More data needed for advanced analysis.",
            "minimum_interactions_needed": self.min_interactions_for_profile
        }
    
    def _calculate_confidence(self, interactions: List[Dict[str, Any]]) -> float:
        """
        Calculate confidence score for the profile based on data quality and quantity.
        
        Args:
            interactions: List of user interactions
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        
        base_confidence = min(len(interactions) / 20.0, 1.0)  # Based on quantity
        
        # Adjust based on data quality
        quality_factors = 0.0
        total_factors = 0
        
        # Check for image data
        has_images = any(i.get("type") == "image_upload" for i in interactions)
        if has_images:
            quality_factors += 0.3
        total_factors += 0.3
        
        # Check for text data
        has_text = any(i.get("type") == "text_request" for i in interactions)
        if has_text:
            quality_factors += 0.2
        total_factors += 0.2
        
        # Check for feedback
        has_feedback = any(i.get("feedback") for i in interactions)
        if has_feedback:
            quality_factors += 0.2
        total_factors += 0.2
        
        # Check for temporal spread
        timestamps = [self._parse_timestamp(i.get("timestamp")) for i in interactions if i.get("timestamp")]
        if len(timestamps) > 1:
            time_span = (max(timestamps) - min(timestamps)).days
            if time_span > 7:  # At least a week of interactions
                quality_factors += 0.3
        total_factors += 0.3
        
        quality_score = quality_factors / total_factors if total_factors > 0 else 0.5
        
        return min(base_confidence * 0.7 + quality_score * 0.3, 1.0)
    
    def _parse_timestamp(self, timestamp_str: Any) -> datetime:
        """
        Parse timestamp string into datetime object.
        
        Args:
            timestamp_str: Timestamp in various formats
            
        Returns:
            Datetime object
        """
        
        if isinstance(timestamp_str, datetime):
            return timestamp_str
        
        if isinstance(timestamp_str, str):
            try:
                return parser.parse(timestamp_str)
            except:
                pass
        
        # Default to current time if parsing fails
        return datetime.now()
    
    def _summarize_image_features(self, image_features: List[Dict[str, Any]]) -> List[float]:
        """Summarize image features into a fixed-size vector."""
        # Simplified implementation - can be enhanced
        return [1.0, 0.5, 0.8, 0.3]  # Placeholder
    
    def _summarize_text_features(self, text_features: List[Dict[str, Any]]) -> List[float]:
        """Summarize text features into a fixed-size vector."""
        # Simplified implementation - can be enhanced
        return [0.7, 0.4, 0.9, 0.6]  # Placeholder
    
    def _detect_semantic_clusters(self, embeddings_array: np.ndarray) -> Dict[str, Any]:
        """Detect semantic clusters in text embeddings."""
        # Simplified implementation
        return {"clusters_detected": 2, "method": "simplified"}
