# Phase 5 Demo Script - Intelligent Combination Engine with Multi-Modal AI Integration
# This script demonstrates the advanced AI-powered clothing combination capabilities

import sys
import os
from datetime import datetime, timedelta
import json

# Add the service directory to the path
sys.path.append('combination_engine_service')

def demo_intelligent_combination_engine():
    """Demonstrate the intelligent combination engine capabilities."""
    
    print("🎯 Phase 5 Demo: Intelligent Combination Engine with Multi-Modal AI Integration")
    print("=" * 85)
    
    print("📋 Service Capabilities:")
    print("- Multi-modal AI integration (Phase 2 image features + Phase 4 style profiles)")
    print("- Visual compatibility analysis using CLIP embeddings")
    print("- Style coherence assessment with fashion expertise rules")
    print("- Color harmony calculation using advanced color theory")
    print("- Pattern balance optimization for aesthetic appeal")
    print("- Context appropriateness evaluation for different occasions")
    print("- Personalized recommendations based on user style profiles")
    print("- Graph-based outfit compatibility analysis")
    print("- Machine learning clustering for style optimization")
    print("- Production-ready intelligent combination algorithms")
    print()
    
    print("🔧 Testing intelligent combination engine (local imports):")
    
    try:
        from intelligent_combiner import IntelligentCombinationEngine
        
        print("✅ IntelligentCombinationEngine imported successfully")
        print("⏳ Initializing multi-modal AI components...")
        
        # Initialize the intelligent combination engine
        engine = IntelligentCombinationEngine(
            image_service_url="http://localhost:8001",  # Phase 2 integration
            style_service_url="http://localhost:8003"   # Phase 4 integration
        )
        
        print(f"✅ Intelligent Combination Engine initialized successfully")
        print(f"   Multi-Modal AI Components:")
        print(f"   - K-Means Clustering: {'✅' if engine.compatibility_clusterer else '❌'}")
        print(f"   - Feature Standardization: {'✅' if engine.feature_scaler else '❌'}")
        print(f"   - Outfit Graph Analysis: {'✅' if engine.outfit_graph else '❌'}")
        print(f"   Fashion Expertise Integration:")
        print(f"   - Style Compatibility Matrix: {len(engine.style_compatibility_matrix)} styles")
        print(f"   - Color Harmony Rules: {len(engine.color_harmony_rules)} colors")
        print(f"   - Pattern Compatibility: {len(engine.pattern_compatibility)} patterns")
        print(f"   - Context Strategies: {len(engine.context_strategies)} contexts")
        print(f"   Feature Weights Distribution:")
        for feature, weight in engine.feature_weights.items():
            print(f"   - {feature}: {weight:.1%}")
        print()
        
        # Create comprehensive mock wardrobe for demonstration
        print("👔 Creating comprehensive mock wardrobe...")
        mock_wardrobe = create_comprehensive_mock_wardrobe()
        print(f"   Wardrobe Categories:")
        for category, items in mock_wardrobe.items():
            print(f"   - {category.title()}: {len(items)} items")
            styles = list(set(item.get('style', 'unknown') for item in items))
            colors = list(set(item.get('color', 'unknown') for item in items))
            print(f"     Styles: {', '.join(styles)}")
            print(f"     Colors: {', '.join(colors)}")
        print()
        
        # Create mock user style profile
        print("👤 Creating comprehensive mock user style profile...")
        mock_style_profile = create_comprehensive_style_profile()
        print(f"   Profile Components:")
        print(f"   - Dominant Style: {mock_style_profile['visual_style_preferences']['dominant_style']}")
        print(f"   - Preferred Color: {mock_style_profile['visual_style_preferences']['color_preferences']['dominant_color']}")
        print(f"   - Engagement Score: {mock_style_profile['behavioral_patterns']['engagement_metrics']['engagement_score']:.2f}")
        print(f"   - Analysis Confidence: {mock_style_profile['analysis_confidence']:.2f}")
        print()
        
        # Test intelligent combination generation for different contexts
        test_contexts = ["casual", "work", "party", "sport", "date"]
        
        for context in test_contexts:
            print(f"🧠 Generating intelligent combination for '{context}' context...")
            
            combination_result = engine.generate_intelligent_combination(
                wardrobe_items=mock_wardrobe,
                user_style_profile=mock_style_profile,
                context=context,
                user_id="demo_user_phase5_001"
            )
            
            if combination_result.get("error"):
                print(f"   ❌ Error: {combination_result['error']}")
                continue
            
            print(f"   ✅ Combination Generated - Overall Score: {combination_result['overall_score']:.3f}")
            print(f"   📊 AI Analysis Breakdown:")
            
            detailed_scores = combination_result.get('detailed_scores', {})
            for score_type, score_value in detailed_scores.items():
                score_name = score_type.replace('_', ' ').title()
                score_bar = "█" * int(score_value * 10) + "░" * (10 - int(score_value * 10))
                print(f"     {score_name:<20}: {score_bar} {score_value:.3f}")
            
            print(f"   🎯 Selected Combination:")
            print(f"     Top: {combination_result['top']['type']} ({combination_result['top']['color']}, {combination_result['top']['style']})")
            print(f"     Bottom: {combination_result['bottom']['type']} ({combination_result['bottom']['color']}, {combination_result['bottom']['style']})")
            print(f"     Shoes: {combination_result['shoes']['type']} ({combination_result['shoes']['color']}, {combination_result['shoes']['style']})")
            
            print(f"   💡 Confidence Level: {combination_result.get('confidence_level', 'unknown').title()}")
            print(f"   🔄 Combinations Evaluated: {combination_result.get('combinations_evaluated', 'unknown')}")
            
            # Display intelligent recommendations if available
            recommendations = combination_result.get('intelligent_recommendations', {})
            if recommendations and not recommendations.get('error'):
                print(f"   🌟 Intelligent Recommendations:")
                
                styling_tips = recommendations.get('styling_tips', [])
                if styling_tips:
                    print(f"     Styling Tips:")
                    for tip in styling_tips[:2]:  # Show top 2 tips
                        print(f"       • {tip}")
                
                accessory_suggestions = recommendations.get('accessory_suggestions', [])
                if accessory_suggestions:
                    print(f"     Suggested Accessories: {', '.join(accessory_suggestions[:3])}")
                
                confidence_explanation = recommendations.get('confidence_explanation', '')
                if confidence_explanation:
                    print(f"     Analysis: {confidence_explanation}")
            
            print()
        
        # Test individual AI component functionality
        print("🔬 Testing Individual AI Components:")
        
        # Test visual compatibility calculation
        print("   Testing Visual Compatibility Analysis...")
        mock_features_1 = engine._generate_mock_image_features("test_top")
        mock_features_2 = engine._generate_mock_image_features("test_bottom")
        mock_features_3 = engine._generate_mock_image_features("test_shoes")
        
        visual_compat = engine.calculate_visual_compatibility(mock_features_1, mock_features_2, mock_features_3)
        print(f"   ✅ Visual Compatibility Score: {visual_compat:.3f}")
        
        # Test style coherence calculation
        style_coherence = engine.calculate_style_coherence(mock_features_1, mock_features_2, mock_features_3)
        print(f"   ✅ Style Coherence Score: {style_coherence:.3f}")
        
        # Test color harmony calculation
        color_harmony = engine.calculate_color_harmony(mock_features_1, mock_features_2, mock_features_3)
        print(f"   ✅ Color Harmony Score: {color_harmony:.3f}")
        
        # Test pattern balance calculation
        pattern_balance = engine.calculate_pattern_balance(mock_features_1, mock_features_2, mock_features_3)
        print(f"   ✅ Pattern Balance Score: {pattern_balance:.3f}")
        
        # Test context appropriateness calculation
        context_appropriate = engine.calculate_context_appropriateness(mock_features_1, mock_features_2, mock_features_3, "work")
        print(f"   ✅ Context Appropriateness Score: {context_appropriate:.3f}")
        
        # Test style profile bonus application
        top_item = {"id": "test_top", "style": "casual", "color": "blue"}
        bottom_item = {"id": "test_bottom", "style": "casual", "color": "navy"}
        shoe_item = {"id": "test_shoe", "style": "casual", "color": "white"}
        
        profile_bonus = engine._apply_style_profile_bonus(top_item, bottom_item, shoe_item, mock_style_profile)
        print(f"   ✅ Style Profile Bonus: {profile_bonus:.3f}")
        print()
        
        print("🎉 Phase 5 Intelligent Combination Engine is working perfectly!")
        
    except ImportError as e:
        print(f"⚠️  Intelligent combination engine not available: {e}")
        print("   Service will run in fallback mode")
        print("   Install: torch, torchvision, transformers, clip-by-openai, scipy, networkx, etc.")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
    
    print("\n📤 To test the intelligent combination service API, start it with:")
    print("   cd combination_engine_service")
    print("   uvicorn main:app --host 0.0.0.0 --port 8004")
    print()
    print("📋 Then send requests to:")
    print("   GET  http://localhost:8004/         # Health check with AI engine status")
    print("   POST http://localhost:8004/generate_intelligent_combination  # AI-powered combinations")
    print("   POST http://localhost:8004/generate_combination              # Legacy endpoint")
    print()
    print("📊 Expected Intelligent Combination Response Structure:")
    print("""
    {
        "message": "Intelligent combination generated successfully using multi-modal AI",
        "user_id": "demo_user_001",
        "context": "casual",
        "generation_method": "multi_modal_ai_phase5",
        "combination": {
            "top": {...},
            "bottom": {...},
            "shoes": {...},
            "overall_score": 0.0-1.0,
            "detailed_scores": {
                "visual_compatibility": 0.0-1.0,
                "style_coherence": 0.0-1.0,
                "color_harmony": 0.0-1.0,
                "pattern_balance": 0.0-1.0,
                "context_appropriateness": 0.0-1.0,
                "profile_bonus": 0.0-0.2
            },
            "confidence_level": "high/medium/moderate",
            "combinations_evaluated": int
        },
        "intelligent_recommendations": {
            "styling_tips": [...],
            "accessory_suggestions": [...],
            "improvement_areas": [...],
            "confidence_explanation": "..."
        },
        "ai_analysis": {
            "confidence_level": "high/medium/moderate",
            "overall_score": 0.0-1.0,
            "detailed_scores": {...}
        }
    }
    """)
    
    print("\n" + "=" * 85)
    print("Phase 5 Demo Complete!")

def create_comprehensive_mock_wardrobe():
    """Create comprehensive mock wardrobe data for demonstration."""
    
    return {
        "tops": [
            {"id": "top_001", "type": "dress shirt", "color": "white", "style": "formal", "pattern": "solid", "formality": 0.9},
            {"id": "top_002", "type": "casual shirt", "color": "blue", "style": "casual", "pattern": "solid", "formality": 0.6},
            {"id": "top_003", "type": "t-shirt", "color": "black", "style": "casual", "pattern": "solid", "formality": 0.3},
            {"id": "top_004", "type": "polo shirt", "color": "navy", "style": "smart_casual", "pattern": "solid", "formality": 0.5},
            {"id": "top_005", "type": "blouse", "color": "cream", "style": "formal", "pattern": "solid", "formality": 0.8},
            {"id": "top_006", "type": "sweater", "color": "gray", "style": "casual", "pattern": "textured", "formality": 0.4},
            {"id": "top_007", "type": "tank top", "color": "white", "style": "sporty", "pattern": "solid", "formality": 0.2},
            {"id": "top_008", "type": "blazer", "color": "charcoal", "style": "formal", "pattern": "solid", "formality": 0.9}
        ],
        "bottoms": [
            {"id": "bottom_001", "type": "dress pants", "color": "black", "style": "formal", "pattern": "solid", "formality": 0.9},
            {"id": "bottom_002", "type": "jeans", "color": "blue", "style": "casual", "pattern": "denim", "formality": 0.4},
            {"id": "bottom_003", "type": "chinos", "color": "khaki", "style": "smart_casual", "pattern": "solid", "formality": 0.6},
            {"id": "bottom_004", "type": "shorts", "color": "navy", "style": "casual", "pattern": "solid", "formality": 0.2},
            {"id": "bottom_005", "type": "dress skirt", "color": "gray", "style": "formal", "pattern": "solid", "formality": 0.8},
            {"id": "bottom_006", "type": "leggings", "color": "black", "style": "sporty", "pattern": "solid", "formality": 0.1},
            {"id": "bottom_007", "type": "casual pants", "color": "brown", "style": "casual", "pattern": "solid", "formality": 0.5}
        ],
        "shoes": [
            {"id": "shoe_001", "type": "dress shoes", "color": "black", "style": "formal", "pattern": "leather", "formality": 0.9},
            {"id": "shoe_002", "type": "sneakers", "color": "white", "style": "casual", "pattern": "solid", "formality": 0.3},
            {"id": "shoe_003", "type": "loafers", "color": "brown", "style": "smart_casual", "pattern": "leather", "formality": 0.7},
            {"id": "shoe_004", "type": "athletic shoes", "color": "gray", "style": "sporty", "pattern": "solid", "formality": 0.1},
            {"id": "shoe_005", "type": "boots", "color": "brown", "style": "casual", "pattern": "leather", "formality": 0.5},
            {"id": "shoe_006", "type": "heels", "color": "black", "style": "formal", "pattern": "solid", "formality": 0.8}
        ]
    }

def create_comprehensive_style_profile():
    """Create comprehensive mock style profile for demonstration."""
    
    return {
        'visual_style_preferences': {
            'dominant_style': 'smart_casual',
            'color_preferences': {
                'dominant_color': 'navy',
                'secondary_colors': ['white', 'gray', 'beige']
            },
            'pattern_preferences': {
                'dominant_pattern': 'solid',
                'acceptable_patterns': ['textured', 'subtle_stripe']
            }
        },
        'textual_preferences': {
            'intent_patterns': {
                'dominant_intent': 'style_combination',
                'confidence': 0.85
            },
            'sentiment_patterns': {
                'dominant_sentiment': 'positive',
                'confidence': 0.78
            },
            'context_patterns': {
                'preferred_context': 'work',
                'confidence': 0.82
            }
        },
        'behavioral_patterns': {
            'interaction_patterns': {
                'total_interactions': 45,
                'primary_interaction': 'combination_request'
            },
            'engagement_metrics': {
                'engagement_score': 0.75,
                'consistency_score': 0.68
            },
            'feedback_analysis': {
                'positive': 12,
                'neutral': 3,
                'negative': 1
            }
        },
        'style_evolution': {
            'time_span_days': 90,
            'evolution_detected': True,
            'trend': 'toward_smart_casual'
        },
        'style_cluster': {
            'primary_cluster': 'professional_versatile',
            'cluster_confidence': 0.72
        },
        'personalized_insights': {
            'profile_strength': 'strong',
            'key_insights': [
                'Prefers versatile pieces that work for multiple occasions',
                'Shows strong preference for neutral color palette',
                'Gravitates toward smart-casual aesthetic'
            ],
            'style_recommendations': [
                'Continue building versatile wardrobe with quality basics',
                'Experiment with subtle textures while maintaining classic silhouettes'
            ]
        },
        'analysis_confidence': 0.78
    }

if __name__ == "__main__":
    demo_intelligent_combination_engine()
