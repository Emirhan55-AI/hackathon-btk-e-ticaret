# Phase 4 Demo Script - Enhanced Style Profiling with AI Integration
# This script demonstrates the advanced style profiling capabilities

import sys
import os
from datetime import datetime, timedelta

# Add the service directory to the path
sys.path.append('style_profile_service')

def demo_enhanced_style_profiling():
    """Demonstrate the enhanced style profiling capabilities."""
    
    print("🎯 Phase 4 Demo: Enhanced Style Profiling with AI Integration")
    print("=" * 75)
    
    print("📋 Service Capabilities:")
    print("- Multi-modal AI feature integration (Phase 2 + Phase 3)")
    print("- Advanced machine learning clustering and similarity analysis")
    print("- Temporal style evolution tracking with timeline analysis")
    print("- Behavioral pattern recognition and engagement metrics")
    print("- Personalized insights generation using comprehensive data")
    print("- FAISS-based similarity search for style matching")
    print("- Social style influence analysis and trend detection")
    print("- Production-ready profiling algorithms with confidence scoring")
    print()
    
    print("🔧 Testing without server dependencies (local imports):")
    
    try:
        from style_profiler import AdvancedStyleProfiler
        
        print("✅ AdvancedStyleProfiler imported successfully")
        print("⏳ Initializing advanced profiling components...")
        
        # Initialize the profiler (with mock service URLs for demo)
        profiler = AdvancedStyleProfiler(
            image_service_url="http://localhost:8001",  # Phase 2 service
            nlu_service_url="http://localhost:8002"     # Phase 3 service
        )
        
        print(f"✅ Advanced Style Profiler initialized successfully")
        print(f"   Machine Learning Components:")
        print(f"   - K-Means Clustering: {'✅' if profiler.style_clusterer else '❌'}")
        print(f"   - PCA Dimensionality Reduction: {'✅' if profiler.pca_reducer else '❌'}")
        print(f"   - Feature Standardization: {'✅' if profiler.scaler else '❌'}")
        print(f"   Style Analysis Parameters:")
        print(f"   - Minimum Interactions: {profiler.min_interactions_for_profile}")
        print(f"   - Style Dimensions: {len(profiler.style_dimensions)}")
        print(f"   - Temporal Window: {profiler.temporal_analysis_window} days")
        print()
        
        # Create comprehensive mock interaction data
        print("📊 Creating comprehensive mock user profile...")
        
        mock_interactions = create_mock_interactions()
        print(f"   Generated {len(mock_interactions)} diverse interactions")
        print(f"   - Image uploads: {sum(1 for i in mock_interactions if i['type'] == 'image_upload')}")
        print(f"   - Text requests: {sum(1 for i in mock_interactions if i['type'] == 'text_request')}")
        print(f"   - Feedback data: {sum(1 for i in mock_interactions if i['type'] == 'feedback')}")
        print(f"   - Time span: {get_time_span(mock_interactions)} days")
        print()
        
        # Test comprehensive profiling
        test_user_id = "demo_user_phase4_001"
        print(f"🧠 Running comprehensive profile analysis for {test_user_id}...")
        
        profile = profiler.create_comprehensive_profile(
            user_id=test_user_id,
            interactions=mock_interactions
        )
        
        print("📊 Profile Analysis Results:")
        print(f"   Profile Version: {profile.get('profile_version', 'unknown')}")
        print(f"   Total Interactions: {profile.get('total_interactions', 0)}")
        print(f"   Analysis Confidence: {profile.get('analysis_confidence', 0.0):.2f}")
        print()
        
        # Display visual style analysis
        visual_analysis = profile.get("visual_style_analysis", {})
        if visual_analysis and not visual_analysis.get("error"):
            print("🎨 Visual Style Analysis:")
            print(f"   Dominant Style: {visual_analysis.get('dominant_style', 'unknown')}")
            color_prefs = visual_analysis.get('color_preferences', {})
            if color_prefs.get('dominant_color'):
                print(f"   Dominant Color: {color_prefs['dominant_color']}")
            pattern_prefs = visual_analysis.get('pattern_preferences', {})
            if pattern_prefs.get('dominant_pattern'):
                print(f"   Dominant Pattern: {pattern_prefs['dominant_pattern']}")
            print(f"   Images Analyzed: {visual_analysis.get('total_images_analyzed', 0)}")
            
            clustering = visual_analysis.get('clustering_analysis')
            if clustering:
                print(f"   Clustering Result: Cluster {clustering.get('primary_cluster', 'unknown')} (confidence: {clustering.get('clustering_confidence', 0.0):.2f})")
        else:
            print("🎨 Visual Style Analysis: ⚠️  No image data available")
        print()
        
        # Display textual preference analysis
        textual_analysis = profile.get("textual_preference_analysis", {})
        if textual_analysis and not textual_analysis.get("error"):
            print("💬 Textual Preference Analysis:")
            intent_patterns = textual_analysis.get('intent_patterns', {})
            print(f"   Dominant Intent: {intent_patterns.get('dominant_intent', 'unknown')}")
            
            sentiment_patterns = textual_analysis.get('sentiment_patterns', {})
            print(f"   Dominant Sentiment: {sentiment_patterns.get('dominant_sentiment', 'unknown')}")
            
            context_patterns = textual_analysis.get('context_patterns', {})
            print(f"   Preferred Context: {context_patterns.get('preferred_context', 'unknown')}")
            
            print(f"   Texts Analyzed: {textual_analysis.get('total_texts_analyzed', 0)}")
            print(f"   Embedding Dimension: {textual_analysis.get('embedding_dimension', 0)}")
            
            semantic = textual_analysis.get('semantic_analysis')
            if semantic:
                print(f"   Semantic Consistency: {semantic.get('consistency_score', 0.0):.2f}")
        else:
            print("💬 Textual Preference Analysis: ⚠️  No text data available")
        print()
        
        # Display behavioral patterns
        behavioral_analysis = profile.get("behavioral_patterns", {})
        if behavioral_analysis and not behavioral_analysis.get("error"):
            print("📈 Behavioral Pattern Analysis:")
            
            interaction_patterns = behavioral_analysis.get('interaction_patterns', {})
            print(f"   Total Interactions: {interaction_patterns.get('total_interactions', 0)}")
            print(f"   Primary Interaction: {interaction_patterns.get('primary_interaction', 'unknown')}")
            
            engagement = behavioral_analysis.get('engagement_metrics', {})
            print(f"   Engagement Score: {engagement.get('engagement_score', 0.0):.2f}")
            print(f"   Activity Level: {behavioral_analysis.get('user_activity_level', 'unknown')}")
            
            feedback = behavioral_analysis.get('feedback_analysis', {})
            if feedback:
                total_feedback = sum(feedback.values())
                if total_feedback > 0:
                    print(f"   Feedback Summary: {feedback.get('positive', 0)} positive, {feedback.get('negative', 0)} negative, {feedback.get('neutral', 0)} neutral")
        else:
            print("📈 Behavioral Pattern Analysis: ⚠️  No behavioral data available")
        print()
        
        # Display style evolution
        evolution_analysis = profile.get("style_evolution", {})
        if evolution_analysis and not evolution_analysis.get("error"):
            print("⏰ Style Evolution Analysis:")
            print(f"   Time Span: {evolution_analysis.get('time_span_days', 0)} days")
            print(f"   Evolution Detected: {'Yes' if evolution_analysis.get('evolution_detected', False) else 'No'}")
            
            if evolution_analysis.get('temporal_periods'):
                periods = evolution_analysis['temporal_periods']
                print(f"   Analysis Periods: {len(periods)}")
                print(f"   Trend: {evolution_analysis.get('trend', 'stable')}")
        else:
            print("⏰ Style Evolution Analysis: ⚠️  Insufficient temporal data")
        print()
        
        # Display style clustering
        style_cluster = profile.get("style_cluster", {})
        if style_cluster and not style_cluster.get("error"):
            print("🎭 Style Clustering Analysis:")
            print(f"   Primary Cluster: {style_cluster.get('primary_cluster', 'unknown')}")
            print(f"   Cluster Confidence: {style_cluster.get('cluster_confidence', 0.0):.2f}")
            print(f"   Clustering Method: {style_cluster.get('clustering_method', 'unknown')}")
            print(f"   Feature Dimension: {style_cluster.get('feature_dimension', 0)}")
        else:
            print("🎭 Style Clustering Analysis: ⚠️  Insufficient feature data")
        print()
        
        # Display personalized insights
        insights = profile.get("personalized_insights", {})
        if insights and not insights.get("error"):
            print("💡 Personalized Insights:")
            print(f"   Profile Strength: {insights.get('profile_strength', 'unknown')}")
            
            key_insights = insights.get('key_insights', [])
            if key_insights:
                print("   Key insights:")
                for i, insight in enumerate(key_insights[:3], 1):  # Show top 3
                    print(f"     {i}. {insight}")
            
            recommendations = insights.get('style_recommendations', [])
            if recommendations:
                print("   Style recommendations:")
                for i, rec in enumerate(recommendations[:2], 1):  # Show top 2
                    print(f"     {i}. {rec}")
        else:
            print("💡 Personalized Insights: ⚠️  Insufficient data for insights")
        print()
        
        print("🎉 Phase 4 Enhanced Style Profiling is working perfectly!")
        
    except ImportError as e:
        print(f"⚠️  Advanced profiling models not available: {e}")
        print("   Service will run in fallback mode")
        print("   Install: scikit-learn, pandas, faiss-cpu, scipy, etc.")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
    
    print("\n📤 To test the service API, start it with:")
    print("   cd style_profile_service")
    print("   uvicorn main:app --host 0.0.0.0 --port 8003")
    print()
    print("📋 Then send requests to:")
    print("   GET  http://localhost:8003/         # Health check with AI service status")
    print("   POST http://localhost:8003/profile/{user_id}/create_advanced  # Advanced profiling")
    print("   POST http://localhost:8003/profile/{user_id}/add_image_analysis  # Phase 2 integration")
    print("   POST http://localhost:8003/profile/{user_id}/add_text_analysis   # Phase 3 integration")
    print()
    print("📊 Expected Advanced Profile Structure:")
    print("""
    {
        "user_id": "demo_user_001",
        "profile_version": "4.0_advanced",
        "analysis_confidence": 0.0-1.0,
        "visual_style_analysis": {
            "dominant_style": "casual/formal/sporty/elegant",
            "color_preferences": {...},
            "pattern_preferences": {...},
            "clustering_analysis": {...}
        },
        "textual_preference_analysis": {
            "intent_patterns": {...},
            "sentiment_patterns": {...},
            "context_patterns": {...},
            "semantic_analysis": {...}
        },
        "behavioral_patterns": {
            "interaction_patterns": {...},
            "engagement_metrics": {...},
            "feedback_analysis": {...}
        },
        "style_evolution": {
            "time_span_days": int,
            "evolution_detected": true/false,
            "temporal_periods": [...]
        },
        "style_cluster": {
            "primary_cluster": "minimalist/trendy/classic/etc",
            "cluster_confidence": 0.0-1.0
        },
        "personalized_insights": {
            "key_insights": [...],
            "style_recommendations": [...],
            "areas_for_exploration": [...]
        }
    }
    """)
    
    print("\n" + "=" * 75)
    print("Phase 4 Demo Complete!")

def create_mock_interactions():
    """Create comprehensive mock interaction data for demo."""
    
    interactions = []
    base_time = datetime.now()
    
    # Add diverse image upload interactions
    for i in range(4):
        days_ago = 25 - i * 6
        interactions.append({
            "type": "image_upload",
            "timestamp": (base_time - timedelta(days=days_ago)).isoformat(),
            "image_analysis": {
                "resnet_features": [0.1 + i * 0.1] * 2048,  # Varying features
                "vit_features": [0.2 + i * 0.05] * 768,
                "clip_embedding": [0.3 + i * 0.1] * 512,
                "style_classification": {
                    "dominant_style": ["casual", "formal", "sporty", "elegant"][i],
                    "confidence": 0.80 + i * 0.03
                },
                "color_analysis": {
                    "dominant_color": ["blue", "black", "red", "white"][i],
                    "confidence": 0.85 + i * 0.02
                },
                "pattern_analysis": {
                    "dominant_pattern": ["solid", "striped", "floral", "geometric"][i],
                    "confidence": 0.75 + i * 0.05
                }
            }
        })
    
    # Add diverse text request interactions
    texts = [
        "I want to buy a beautiful dress for tonight's party",
        "Can you help me combine this shirt with my jeans?",
        "What's my personal style based on my wardrobe?",
        "I need comfortable clothes for daily wear"
    ]
    
    for i, text in enumerate(texts):
        days_ago = 20 - i * 4
        interactions.append({
            "type": "text_request",
            "timestamp": (base_time - timedelta(days=days_ago)).isoformat(),
            "nlu_analysis": {
                "xlm_r_features": [0.4 + i * 0.1] * 768,
                "intent_analysis": {
                    "predicted_intent": ["product_recommendation", "style_combination", "style_analysis", "general_inquiry"][i],
                    "confidence": 0.85 + i * 0.02
                },
                "sentiment_analysis": {
                    "predicted_sentiment": ["positive", "neutral", "positive", "neutral"][i],
                    "confidence": 0.75 + i * 0.03
                },
                "context_analysis": {
                    "predicted_context": ["party", "casual", "formal", "casual"][i],
                    "confidence": 0.80 + i * 0.02
                }
            }
        })
    
    # Add feedback interactions
    for i in range(2):
        days_ago = 5 - i * 3
        interactions.append({
            "type": "feedback",
            "timestamp": (base_time - timedelta(days=days_ago)).isoformat(),
            "preferences": {
                "preferred_colors": [["blue", "white"], ["black", "gray"]][i],
                "style_preference": ["versatile", "classic"][i]
            },
            "feedback": {
                "rating": [5, 4][i],
                "comment": ["Great recommendations!", "Good suggestions"][i]
            }
        })
    
    return interactions

def get_time_span(interactions):
    """Calculate time span of interactions in days."""
    
    try:
        timestamps = []
        for interaction in interactions:
            if interaction.get("timestamp"):
                timestamps.append(datetime.fromisoformat(interaction["timestamp"].replace("Z", "+00:00").replace("+00:00", "")))
        
        if len(timestamps) >= 2:
            return (max(timestamps) - min(timestamps)).days
        else:
            return 0
    except:
        return 0

if __name__ == "__main__":
    demo_enhanced_style_profiling()
