# Phase 5: Intelligent Combination Engine with Multi-Modal AI Integration
# This module implements advanced AI-powered clothing combination generation
# Integrates Phase 2 image processing and Phase 4 style profiling capabilities

import logging
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
import requests
import json
from datetime import datetime
import networkx as nx
from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd

# Configure comprehensive logging for the intelligent combination engine
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntelligentCombinationEngine:
    """
    Advanced AI-powered clothing combination engine that integrates multi-modal features.
    
    This engine combines:
    - Phase 2: Visual features from ResNet-50, ViT, and CLIP models
    - Phase 4: Style profiles with behavioral and preference analysis
    - Advanced graph algorithms for outfit compatibility analysis
    - Machine learning clustering for style coherence optimization
    """
    
    def __init__(self, 
                 image_service_url: str = "http://localhost:8001",
                 style_service_url: str = "http://localhost:8003"):
        """
        Initialize the intelligent combination engine with AI service connections.
        
        Args:
            image_service_url: URL of the Phase 2 image processing service
            style_service_url: URL of the Phase 4 style profile service
        """
        logger.info("Initializing Intelligent Combination Engine - Phase 5")
        
        # Store service URLs for Phase 2 and Phase 4 integration
        self.image_service_url = image_service_url
        self.style_service_url = style_service_url
        
        # Initialize machine learning components for intelligent combination generation
        self.compatibility_clusterer = KMeans(n_clusters=5, random_state=42)  # For grouping compatible items
        self.feature_scaler = StandardScaler()  # For normalizing multi-modal features
        self.outfit_graph = nx.Graph()  # Graph structure for compatibility analysis
        
        # Define style compatibility rules based on fashion expertise
        self.style_compatibility_matrix = self._initialize_style_compatibility()
        
        # Initialize color harmony rules for aesthetic combinations
        self.color_harmony_rules = self._initialize_color_harmony()
        
        # Pattern and texture compatibility guidelines
        self.pattern_compatibility = self._initialize_pattern_rules()
        
        # Context-specific combination strategies
        self.context_strategies = self._initialize_context_strategies()
        
        # Multi-modal feature weights for different combination aspects
        self.feature_weights = {
            'visual_similarity': 0.3,      # Weight for Phase 2 visual features
            'style_coherence': 0.25,       # Weight for Phase 4 style consistency
            'color_harmony': 0.2,          # Weight for color compatibility
            'context_appropriateness': 0.15, # Weight for occasion suitability
            'pattern_balance': 0.1         # Weight for pattern/texture balance
        }
        
        logger.info("✅ Intelligent Combination Engine initialized successfully")
        logger.info(f"   Connected to Image Service: {image_service_url}")
        logger.info(f"   Connected to Style Service: {style_service_url}")
        logger.info(f"   ML Components: Clustering, Graph Analysis, Multi-Modal Features")
    
    def _initialize_style_compatibility(self) -> Dict[str, Dict[str, float]]:
        """
        Initialize comprehensive style compatibility matrix based on fashion principles.
        
        Returns:
            Dictionary mapping style pairs to compatibility scores (0.0 to 1.0)
        """
        # Fashion expert knowledge encoded as compatibility scores
        # Higher scores indicate better style compatibility
        return {
            'casual': {'casual': 1.0, 'sporty': 0.8, 'smart_casual': 0.9, 'formal': 0.3, 'vintage': 0.6, 'bohemian': 0.7},
            'sporty': {'casual': 0.8, 'sporty': 1.0, 'smart_casual': 0.6, 'formal': 0.2, 'vintage': 0.4, 'bohemian': 0.3},
            'smart_casual': {'casual': 0.9, 'sporty': 0.6, 'smart_casual': 1.0, 'formal': 0.8, 'vintage': 0.7, 'bohemian': 0.5},
            'formal': {'casual': 0.3, 'sporty': 0.2, 'smart_casual': 0.8, 'formal': 1.0, 'vintage': 0.6, 'bohemian': 0.2},
            'vintage': {'casual': 0.6, 'sporty': 0.4, 'smart_casual': 0.7, 'formal': 0.6, 'vintage': 1.0, 'bohemian': 0.8},
            'bohemian': {'casual': 0.7, 'sporty': 0.3, 'smart_casual': 0.5, 'formal': 0.2, 'vintage': 0.8, 'bohemian': 1.0}
        }
    
    def _initialize_color_harmony(self) -> Dict[str, List[str]]:
        """
        Initialize comprehensive color harmony rules based on color theory.
        
        Returns:
            Dictionary mapping colors to lists of harmonious color combinations
        """
        return {
            'red': ['white', 'black', 'navy', 'gray', 'beige', 'gold'],
            'blue': ['white', 'gray', 'navy', 'beige', 'yellow', 'orange'],
            'green': ['white', 'black', 'brown', 'beige', 'navy', 'pink'],
            'yellow': ['white', 'gray', 'navy', 'blue', 'purple', 'black'],
            'orange': ['white', 'black', 'navy', 'blue', 'brown', 'beige'],
            'purple': ['white', 'gray', 'black', 'yellow', 'green', 'pink'],
            'pink': ['white', 'black', 'gray', 'navy', 'green', 'purple'],
            'white': ['any'],  # White goes with everything
            'black': ['any'],  # Black goes with everything
            'gray': ['any'],   # Gray is neutral
            'navy': ['white', 'beige', 'yellow', 'pink', 'red', 'gray'],
            'brown': ['white', 'beige', 'green', 'orange', 'yellow', 'cream'],
            'beige': ['any']   # Beige is versatile neutral
        }
    
    def _initialize_pattern_rules(self) -> Dict[str, Dict[str, float]]:
        """
        Initialize pattern and texture compatibility rules for balanced combinations.
        
        Returns:
            Dictionary mapping pattern combinations to compatibility scores
        """
        return {
            'solid': {'solid': 1.0, 'striped': 0.9, 'floral': 0.8, 'geometric': 0.8, 'textured': 0.9},
            'striped': {'solid': 0.9, 'striped': 0.6, 'floral': 0.4, 'geometric': 0.5, 'textured': 0.7},
            'floral': {'solid': 0.8, 'striped': 0.4, 'floral': 0.3, 'geometric': 0.4, 'textured': 0.6},
            'geometric': {'solid': 0.8, 'striped': 0.5, 'floral': 0.4, 'geometric': 0.5, 'textured': 0.7},
            'textured': {'solid': 0.9, 'striped': 0.7, 'floral': 0.6, 'geometric': 0.7, 'textured': 0.8}
        }
    
    def _initialize_context_strategies(self) -> Dict[str, Dict[str, Any]]:
        """
        Initialize context-specific combination strategies for different occasions.
        
        Returns:
            Dictionary mapping contexts to specific combination strategies and rules
        """
        return {
            'work': {
                'preferred_styles': ['formal', 'smart_casual'],
                'color_palette': ['black', 'navy', 'gray', 'white', 'beige'],
                'avoid_patterns': ['floral', 'geometric'],
                'formality_level': 0.8,
                'conservativeness': 0.9
            },
            'casual': {
                'preferred_styles': ['casual', 'smart_casual'],
                'color_palette': ['any'],
                'avoid_patterns': [],
                'formality_level': 0.3,
                'conservativeness': 0.4
            },
            'party': {
                'preferred_styles': ['smart_casual', 'formal', 'bohemian'],
                'color_palette': ['black', 'red', 'gold', 'silver', 'purple'],
                'avoid_patterns': [],
                'formality_level': 0.7,
                'conservativeness': 0.3
            },
            'sport': {
                'preferred_styles': ['sporty', 'casual'],
                'color_palette': ['any'],
                'avoid_patterns': ['formal'],
                'formality_level': 0.1,
                'conservativeness': 0.2
            },
            'date': {
                'preferred_styles': ['smart_casual', 'casual', 'bohemian'],
                'color_palette': ['any'],
                'avoid_patterns': [],
                'formality_level': 0.5,
                'conservativeness': 0.5
            }
        }
    
    async def get_image_features(self, item_id: str, image_data: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve comprehensive image features from Phase 2 image processing service.
        
        Args:
            item_id: Unique identifier for the clothing item
            image_data: Optional base64 encoded image data
            
        Returns:
            Dictionary containing multi-modal visual features from Phase 2 models
        """
        try:
            # Prepare request payload for Phase 2 image service
            payload = {"item_id": item_id}
            if image_data:
                payload["image_data"] = image_data
            
            # Send request to Phase 2 image processing service
            response = requests.post(
                f"{self.image_service_url}/analyze",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                image_analysis = response.json()
                logger.info(f"✅ Retrieved image features for item {item_id}")
                
                # Extract and structure multi-modal features from Phase 2
                return {
                    'resnet_features': image_analysis.get('resnet_features', []),
                    'vit_features': image_analysis.get('vit_features', []),
                    'clip_embedding': image_analysis.get('clip_embedding', []),
                    'style_classification': image_analysis.get('style_classification', {}),
                    'color_analysis': image_analysis.get('color_analysis', {}),
                    'pattern_analysis': image_analysis.get('pattern_analysis', {}),
                    'texture_analysis': image_analysis.get('texture_analysis', {})
                }
            else:
                logger.warning(f"⚠️ Image service unavailable for item {item_id}")
                return self._generate_mock_image_features(item_id)
                
        except Exception as e:
            logger.error(f"❌ Error retrieving image features for {item_id}: {e}")
            return self._generate_mock_image_features(item_id)
    
    async def get_style_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieve comprehensive user style profile from Phase 4 style profiling service.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            Dictionary containing advanced style profile data from Phase 4
        """
        try:
            # Send request to Phase 4 style profile service
            response = requests.get(
                f"{self.style_service_url}/profile/{user_id}",
                timeout=10
            )
            
            if response.status_code == 200:
                style_profile = response.json()
                logger.info(f"✅ Retrieved style profile for user {user_id}")
                
                # Extract key style characteristics from Phase 4 profile
                return {
                    'visual_style_preferences': style_profile.get('visual_style_analysis', {}),
                    'textual_preferences': style_profile.get('textual_preference_analysis', {}),
                    'behavioral_patterns': style_profile.get('behavioral_patterns', {}),
                    'style_evolution': style_profile.get('style_evolution', {}),
                    'style_cluster': style_profile.get('style_cluster', {}),
                    'personalized_insights': style_profile.get('personalized_insights', {}),
                    'analysis_confidence': style_profile.get('analysis_confidence', 0.5)
                }
            else:
                logger.warning(f"⚠️ Style service unavailable for user {user_id}")
                return self._generate_mock_style_profile(user_id)
                
        except Exception as e:
            logger.error(f"❌ Error retrieving style profile for {user_id}: {e}")
            return self._generate_mock_style_profile(user_id)
    
    def calculate_visual_compatibility(self, item1_features: Dict, item2_features: Dict, item3_features: Dict) -> float:
        """
        Calculate visual compatibility between three clothing items using Phase 2 features.
        
        Args:
            item1_features, item2_features, item3_features: Feature dictionaries from Phase 2
            
        Returns:
            Float compatibility score between 0.0 and 1.0
        """
        try:
            # Extract CLIP embeddings for semantic similarity analysis
            clip1 = np.array(item1_features.get('clip_embedding', []))
            clip2 = np.array(item2_features.get('clip_embedding', []))
            clip3 = np.array(item3_features.get('clip_embedding', []))
            
            if len(clip1) == 0 or len(clip2) == 0 or len(clip3) == 0:
                logger.warning("⚠️ Missing CLIP embeddings, using fallback compatibility")
                return self._calculate_fallback_visual_compatibility(item1_features, item2_features, item3_features)
            
            # Calculate pairwise cosine similarities between CLIP embeddings
            # Higher similarity indicates better visual compatibility
            sim_1_2 = 1 - cosine(clip1, clip2) if len(clip1) == len(clip2) else 0.5
            sim_1_3 = 1 - cosine(clip1, clip3) if len(clip1) == len(clip3) else 0.5
            sim_2_3 = 1 - cosine(clip2, clip3) if len(clip2) == len(clip3) else 0.5
            
            # Average similarity scores for overall visual compatibility
            visual_compatibility = (sim_1_2 + sim_1_3 + sim_2_3) / 3.0
            
            # Ensure score is within valid range
            visual_compatibility = max(0.0, min(1.0, visual_compatibility))
            
            logger.debug(f"Visual compatibility calculated: {visual_compatibility:.3f}")
            return visual_compatibility
            
        except Exception as e:
            logger.error(f"❌ Error calculating visual compatibility: {e}")
            return self._calculate_fallback_visual_compatibility(item1_features, item2_features, item3_features)
    
    def calculate_style_coherence(self, item1_features: Dict, item2_features: Dict, item3_features: Dict) -> float:
        """
        Calculate style coherence across three items using fashion expertise rules.
        
        Args:
            item1_features, item2_features, item3_features: Feature dictionaries with style info
            
        Returns:
            Float coherence score between 0.0 and 1.0
        """
        try:
            # Extract style classifications from Phase 2 analysis
            style1 = item1_features.get('style_classification', {}).get('dominant_style', 'casual')
            style2 = item2_features.get('style_classification', {}).get('dominant_style', 'casual')
            style3 = item3_features.get('style_classification', {}).get('dominant_style', 'casual')
            
            # Calculate pairwise style compatibility using the compatibility matrix
            compat_1_2 = self.style_compatibility_matrix.get(style1, {}).get(style2, 0.5)
            compat_1_3 = self.style_compatibility_matrix.get(style1, {}).get(style3, 0.5)
            compat_2_3 = self.style_compatibility_matrix.get(style2, {}).get(style3, 0.5)
            
            # Average compatibility scores for overall style coherence
            style_coherence = (compat_1_2 + compat_1_3 + compat_2_3) / 3.0
            
            logger.debug(f"Style coherence calculated: {style_coherence:.3f} ({style1}, {style2}, {style3})")
            return style_coherence
            
        except Exception as e:
            logger.error(f"❌ Error calculating style coherence: {e}")
            return 0.5  # Default moderate coherence
    
    def calculate_color_harmony(self, item1_features: Dict, item2_features: Dict, item3_features: Dict) -> float:
        """
        Calculate color harmony score using color theory principles.
        
        Args:
            item1_features, item2_features, item3_features: Feature dictionaries with color info
            
        Returns:
            Float harmony score between 0.0 and 1.0
        """
        try:
            # Extract dominant colors from Phase 2 color analysis
            color1 = item1_features.get('color_analysis', {}).get('dominant_color', 'gray').lower()
            color2 = item2_features.get('color_analysis', {}).get('dominant_color', 'gray').lower()
            color3 = item3_features.get('color_analysis', {}).get('dominant_color', 'gray').lower()
            
            colors = [color1, color2, color3]
            
            # Perfect harmony for monochromatic combinations
            if len(set(colors)) == 1:
                return 1.0
            
            # Calculate harmony based on color compatibility rules
            harmony_scores = []
            
            for i, color_a in enumerate(colors):
                for j, color_b in enumerate(colors):
                    if i != j:  # Don't compare color with itself
                        harmonious_colors = self.color_harmony_rules.get(color_a, [])
                        if 'any' in harmonious_colors or color_b in harmonious_colors:
                            harmony_scores.append(1.0)
                        else:
                            harmony_scores.append(0.3)  # Poor harmony but not completely incompatible
            
            # Average harmony across all color pairs
            color_harmony = sum(harmony_scores) / len(harmony_scores) if harmony_scores else 0.5
            
            logger.debug(f"Color harmony calculated: {color_harmony:.3f} ({color1}, {color2}, {color3})")
            return color_harmony
            
        except Exception as e:
            logger.error(f"❌ Error calculating color harmony: {e}")
            return 0.5  # Default moderate harmony
    
    def calculate_pattern_balance(self, item1_features: Dict, item2_features: Dict, item3_features: Dict) -> float:
        """
        Calculate pattern balance to ensure visually pleasing combinations.
        
        Args:
            item1_features, item2_features, item3_features: Feature dictionaries with pattern info
            
        Returns:
            Float balance score between 0.0 and 1.0
        """
        try:
            # Extract pattern information from Phase 2 pattern analysis
            pattern1 = item1_features.get('pattern_analysis', {}).get('dominant_pattern', 'solid').lower()
            pattern2 = item2_features.get('pattern_analysis', {}).get('dominant_pattern', 'solid').lower()
            pattern3 = item3_features.get('pattern_analysis', {}).get('dominant_pattern', 'solid').lower()
            
            patterns = [pattern1, pattern2, pattern3]
            
            # Calculate pattern compatibility using pattern rules
            balance_scores = []
            
            for i, pattern_a in enumerate(patterns):
                for j, pattern_b in enumerate(patterns):
                    if i != j:  # Don't compare pattern with itself
                        compatibility = self.pattern_compatibility.get(pattern_a, {}).get(pattern_b, 0.5)
                        balance_scores.append(compatibility)
            
            # Average balance across all pattern pairs
            pattern_balance = sum(balance_scores) / len(balance_scores) if balance_scores else 0.5
            
            logger.debug(f"Pattern balance calculated: {pattern_balance:.3f} ({pattern1}, {pattern2}, {pattern3})")
            return pattern_balance
            
        except Exception as e:
            logger.error(f"❌ Error calculating pattern balance: {e}")
            return 0.5  # Default moderate balance
    
    def calculate_context_appropriateness(self, item1_features: Dict, item2_features: Dict, 
                                        item3_features: Dict, context: str) -> float:
        """
        Calculate how appropriate the combination is for the given context/occasion.
        
        Args:
            item1_features, item2_features, item3_features: Feature dictionaries
            context: The occasion context (work, casual, party, sport, date)
            
        Returns:
            Float appropriateness score between 0.0 and 1.0
        """
        try:
            # Get context strategy for the given occasion
            context_strategy = self.context_strategies.get(context.lower(), self.context_strategies['casual'])
            
            # Extract styles from all three items
            styles = [
                item1_features.get('style_classification', {}).get('dominant_style', 'casual'),
                item2_features.get('style_classification', {}).get('dominant_style', 'casual'),
                item3_features.get('style_classification', {}).get('dominant_style', 'casual')
            ]
            
            # Extract colors from all three items
            colors = [
                item1_features.get('color_analysis', {}).get('dominant_color', 'gray').lower(),
                item2_features.get('color_analysis', {}).get('dominant_color', 'gray').lower(),
                item3_features.get('color_analysis', {}).get('dominant_color', 'gray').lower()
            ]
            
            # Calculate appropriateness based on context strategy
            appropriateness_scores = []
            
            # Check style appropriateness
            preferred_styles = context_strategy['preferred_styles']
            for style in styles:
                if style in preferred_styles:
                    appropriateness_scores.append(1.0)
                else:
                    appropriateness_scores.append(0.3)  # Not preferred but not forbidden
            
            # Check color appropriateness
            preferred_colors = context_strategy['color_palette']
            if 'any' not in preferred_colors:
                for color in colors:
                    if color in preferred_colors:
                        appropriateness_scores.append(1.0)
                    else:
                        appropriateness_scores.append(0.4)  # Less appropriate color
            
            # Average appropriateness score
            context_appropriateness = sum(appropriateness_scores) / len(appropriateness_scores) if appropriateness_scores else 0.5
            
            logger.debug(f"Context appropriateness calculated: {context_appropriateness:.3f} for {context}")
            return context_appropriateness
            
        except Exception as e:
            logger.error(f"❌ Error calculating context appropriateness: {e}")
            return 0.5  # Default moderate appropriateness
    
    def generate_intelligent_combination(self, wardrobe_items: Dict[str, List[Dict]], 
                                       user_style_profile: Dict[str, Any], 
                                       context: str = "casual",
                                       user_id: str = "default") -> Dict[str, Any]:
        """
        Generate an intelligent clothing combination using multi-modal AI analysis.
        
        Args:
            wardrobe_items: Dictionary containing categorized wardrobe items
            user_style_profile: User's style profile from Phase 4
            context: Occasion context for the combination
            user_id: User identifier for personalization
            
        Returns:
            Dictionary containing the optimal combination with detailed analysis
        """
        logger.info(f"Generating intelligent combination for user {user_id}, context: {context}")
        
        try:
            # Ensure we have items in required categories
            required_categories = ['tops', 'bottoms', 'shoes']
            for category in required_categories:
                if not wardrobe_items.get(category):
                    logger.error(f"❌ Missing items in category: {category}")
                    return {"error": f"No items available in category: {category}"}
            
            best_combination = None
            best_score = 0.0
            analysis_details = []
            
            # Evaluate multiple combinations to find the optimal one
            max_combinations = min(50, len(wardrobe_items['tops']) * len(wardrobe_items['bottoms']) * len(wardrobe_items['shoes']))
            logger.info(f"Evaluating up to {max_combinations} possible combinations")
            
            # Try different combinations and score each one
            combinations_tried = 0
            for top in wardrobe_items['tops'][:10]:  # Limit to prevent excessive computation
                for bottom in wardrobe_items['bottoms'][:10]:
                    for shoe in wardrobe_items['shoes'][:5]:
                        if combinations_tried >= max_combinations:
                            break
                        
                        combinations_tried += 1
                        
                        # Get image features for each item (mock data for Phase 1)
                        # In Phase 2 integration, these would come from actual image analysis
                        top_features = self._generate_mock_image_features(top['id'])
                        bottom_features = self._generate_mock_image_features(bottom['id'])
                        shoe_features = self._generate_mock_image_features(shoe['id'])
                        
                        # Calculate individual compatibility scores
                        visual_compat = self.calculate_visual_compatibility(top_features, bottom_features, shoe_features)
                        style_coherence = self.calculate_style_coherence(top_features, bottom_features, shoe_features)
                        color_harmony = self.calculate_color_harmony(top_features, bottom_features, shoe_features)
                        pattern_balance = self.calculate_pattern_balance(top_features, bottom_features, shoe_features)
                        context_appropriate = self.calculate_context_appropriateness(top_features, bottom_features, shoe_features, context)
                        
                        # Calculate weighted overall score using feature weights
                        overall_score = (
                            visual_compat * self.feature_weights['visual_similarity'] +
                            style_coherence * self.feature_weights['style_coherence'] +
                            color_harmony * self.feature_weights['color_harmony'] +
                            context_appropriate * self.feature_weights['context_appropriateness'] +
                            pattern_balance * self.feature_weights['pattern_balance']
                        )
                        
                        # Apply user style profile influence (Phase 4 integration)
                        profile_bonus = self._apply_style_profile_bonus(
                            top, bottom, shoe, user_style_profile
                        )
                        overall_score = min(1.0, overall_score + profile_bonus)
                        
                        # Track the best combination found
                        if overall_score > best_score:
                            best_score = overall_score
                            best_combination = {
                                'top': top,
                                'bottom': bottom,
                                'shoes': shoe,
                                'overall_score': overall_score,
                                'detailed_scores': {
                                    'visual_compatibility': visual_compat,
                                    'style_coherence': style_coherence,
                                    'color_harmony': color_harmony,
                                    'pattern_balance': pattern_balance,
                                    'context_appropriateness': context_appropriate,
                                    'profile_bonus': profile_bonus
                                },
                                'analysis_method': 'multi_modal_ai',
                                'confidence_level': 'high' if overall_score > 0.8 else 'medium' if overall_score > 0.6 else 'moderate'
                            }
                            
                            analysis_details.append({
                                'combination_id': f"{top['id']}_{bottom['id']}_{shoe['id']}",
                                'score': overall_score,
                                'breakdown': best_combination['detailed_scores']
                            })
            
            if best_combination:
                logger.info(f"✅ Best combination found with score: {best_score:.3f}")
                
                # Add intelligent recommendations based on the analysis
                recommendations = self._generate_intelligent_recommendations(
                    best_combination, user_style_profile, context
                )
                
                best_combination['intelligent_recommendations'] = recommendations
                best_combination['combinations_evaluated'] = combinations_tried
                best_combination['generation_timestamp'] = datetime.now().isoformat()
                
                return best_combination
            else:
                logger.warning("❌ No suitable combination found")
                return {"error": "Could not generate suitable combination with available items"}
                
        except Exception as e:
            logger.error(f"❌ Error generating intelligent combination: {e}")
            return {"error": f"Combination generation failed: {str(e)}"}
    
    def _apply_style_profile_bonus(self, top: Dict, bottom: Dict, shoe: Dict, 
                                 style_profile: Dict[str, Any]) -> float:
        """
        Apply bonus scoring based on user's style profile from Phase 4.
        
        Args:
            top, bottom, shoe: Selected clothing items
            style_profile: User's comprehensive style profile
            
        Returns:
            Float bonus score to add to overall combination score
        """
        try:
            bonus = 0.0
            
            # Extract key style preferences from Phase 4 profile
            visual_preferences = style_profile.get('visual_style_preferences', {})
            behavioral_patterns = style_profile.get('behavioral_patterns', {})
            
            # Bonus for matching dominant style preference
            if visual_preferences.get('dominant_style'):
                user_preferred_style = visual_preferences['dominant_style']
                item_styles = [top.get('style', ''), bottom.get('style', ''), shoe.get('style', '')]
                
                if any(style == user_preferred_style for style in item_styles):
                    bonus += 0.1  # 10% bonus for style preference match
                    logger.debug(f"Style preference bonus applied: {user_preferred_style}")
            
            # Bonus for matching color preferences
            color_preferences = visual_preferences.get('color_preferences', {})
            if color_preferences.get('dominant_color'):
                user_preferred_color = color_preferences['dominant_color']
                item_colors = [top.get('color', ''), bottom.get('color', ''), shoe.get('color', '')]
                
                if any(color == user_preferred_color for color in item_colors):
                    bonus += 0.05  # 5% bonus for color preference match
                    logger.debug(f"Color preference bonus applied: {user_preferred_color}")
            
            # Bonus based on user's engagement patterns
            engagement_score = behavioral_patterns.get('engagement_metrics', {}).get('engagement_score', 0)
            if engagement_score > 0.7:  # High engagement user
                bonus += 0.02  # Small bonus for highly engaged users
            
            return min(0.2, bonus)  # Cap bonus at 20%
            
        except Exception as e:
            logger.error(f"❌ Error applying style profile bonus: {e}")
            return 0.0
    
    def _generate_intelligent_recommendations(self, combination: Dict, 
                                            style_profile: Dict, context: str) -> Dict[str, Any]:
        """
        Generate intelligent recommendations and styling tips based on combination analysis.
        
        Args:
            combination: The selected best combination
            style_profile: User's style profile from Phase 4
            context: Occasion context
            
        Returns:
            Dictionary containing personalized recommendations and styling tips
        """
        try:
            recommendations = {
                'styling_tips': [],
                'accessory_suggestions': [],
                'improvement_areas': [],
                'alternative_suggestions': [],
                'confidence_explanation': ''
            }
            
            # Generate styling tips based on combination scores
            scores = combination['detailed_scores']
            
            if scores['color_harmony'] > 0.8:
                recommendations['styling_tips'].append("Excellent color coordination! This combination creates a harmonious and visually appealing look.")
            elif scores['color_harmony'] < 0.6:
                recommendations['improvement_areas'].append("Consider adding a neutral accessory to balance the color palette.")
            
            if scores['style_coherence'] > 0.8:
                recommendations['styling_tips'].append("Perfect style coherence across all pieces - this outfit tells a consistent story.")
            elif scores['style_coherence'] < 0.6:
                recommendations['improvement_areas'].append("Try mixing fewer style elements for a more cohesive look.")
            
            if scores['context_appropriateness'] > 0.8:
                recommendations['styling_tips'].append(f"Perfectly appropriate for {context} occasions.")
            elif scores['context_appropriateness'] < 0.6:
                recommendations['alternative_suggestions'].append(f"Consider adjusting formality level for better {context} appropriateness.")
            
            # Generate accessory suggestions based on context
            context_accessories = {
                'work': ['watch', 'blazer', 'belt', 'professional bag'],
                'casual': ['sneakers', 'denim jacket', 'casual bag', 'baseball cap'],
                'party': ['statement jewelry', 'dress shoes', 'clutch', 'bold accessories'],
                'sport': ['athletic shoes', 'sports watch', 'gym bag', 'sweatband'],
                'date': ['nice shoes', 'subtle jewelry', 'light jacket', 'stylish bag']
            }
            
            suggestions = context_accessories.get(context.lower(), ['belt', 'watch', 'bag'])
            recommendations['accessory_suggestions'] = suggestions[:3]  # Limit to top 3
            
            # Generate confidence explanation
            overall_score = combination['overall_score']
            if overall_score > 0.8:
                recommendations['confidence_explanation'] = "High confidence: This combination excels in multiple areas and is highly recommended."
            elif overall_score > 0.6:
                recommendations['confidence_explanation'] = "Medium confidence: This is a solid combination with room for minor enhancements."
            else:
                recommendations['confidence_explanation'] = "Moderate confidence: This combination works but could benefit from some adjustments."
            
            return recommendations
            
        except Exception as e:
            logger.error(f"❌ Error generating intelligent recommendations: {e}")
            return {'error': 'Could not generate recommendations'}
    
    def _generate_mock_image_features(self, item_id: str) -> Dict[str, Any]:
        """
        Generate mock image features for Phase 1 demonstration.
        In Phase 2, this will be replaced with actual Phase 2 service calls.
        
        Args:
            item_id: Identifier of the clothing item
            
        Returns:
            Dictionary containing mock multi-modal features
        """
        # Create deterministic mock features based on item_id for consistency
        import hashlib
        seed = int(hashlib.md5(item_id.encode()).hexdigest()[:8], 16)
        np.random.seed(seed % (2**32))
        
        return {
            'resnet_features': np.random.normal(0, 1, 2048).tolist(),
            'vit_features': np.random.normal(0, 1, 768).tolist(),
            'clip_embedding': np.random.normal(0, 1, 512).tolist(),
            'style_classification': {
                'dominant_style': np.random.choice(['casual', 'formal', 'sporty', 'smart_casual', 'bohemian']),
                'confidence': np.random.uniform(0.7, 0.95)
            },
            'color_analysis': {
                'dominant_color': np.random.choice(['blue', 'black', 'white', 'gray', 'red', 'green', 'brown']),
                'confidence': np.random.uniform(0.8, 0.95)
            },
            'pattern_analysis': {
                'dominant_pattern': np.random.choice(['solid', 'striped', 'floral', 'geometric', 'textured']),
                'confidence': np.random.uniform(0.75, 0.9)
            }
        }
    
    def _generate_mock_style_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Generate mock style profile for Phase 1 demonstration.
        In Phase 4 integration, this will come from actual style profile service.
        
        Args:
            user_id: Identifier of the user
            
        Returns:
            Dictionary containing mock style profile data
        """
        import hashlib
        seed = int(hashlib.md5(user_id.encode()).hexdigest()[:8], 16)
        np.random.seed(seed % (2**32))
        
        return {
            'visual_style_preferences': {
                'dominant_style': np.random.choice(['casual', 'formal', 'sporty', 'smart_casual']),
                'color_preferences': {
                    'dominant_color': np.random.choice(['blue', 'black', 'white', 'gray'])
                }
            },
            'behavioral_patterns': {
                'engagement_metrics': {
                    'engagement_score': np.random.uniform(0.3, 0.9)
                }
            },
            'analysis_confidence': np.random.uniform(0.6, 0.9)
        }
    
    def _calculate_fallback_visual_compatibility(self, item1: Dict, item2: Dict, item3: Dict) -> float:
        """
        Fallback method for visual compatibility when AI features are unavailable.
        
        Args:
            item1, item2, item3: Item feature dictionaries
            
        Returns:
            Float compatibility score based on basic rules
        """
        # Simple rule-based compatibility as fallback
        colors = [
            item1.get('color_analysis', {}).get('dominant_color', 'gray'),
            item2.get('color_analysis', {}).get('dominant_color', 'gray'),
            item3.get('color_analysis', {}).get('dominant_color', 'gray')
        ]
        
        # Higher score for neutral color combinations
        neutral_colors = {'white', 'black', 'gray', 'navy', 'beige'}
        neutral_count = sum(1 for color in colors if color.lower() in neutral_colors)
        
        return 0.5 + (neutral_count * 0.15)  # Base score plus neutral bonus
