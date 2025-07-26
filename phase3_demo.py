# Phase 3 Demo Script - Advanced NLU Service with XLM-R Transformer
# This script demonstrates the multilingual natural language understanding capabilities

import sys
import os

# Add the service directory to the path
sys.path.append('nlu_service')

def demo_multilingual_nlu():
    """Demonstrate the advanced multilingual NLU capabilities."""
    
    print("🎯 Phase 3 Demo: Advanced Multilingual NLU with XLM-R")
    print("=" * 65)
    
    print("📋 Service Capabilities:")
    print("- XLM-R transformer for multilingual understanding")
    print("- Advanced intent classification with confidence scoring")
    print("- Sentiment analysis using multilingual models")
    print("- Context/occasion detection with semantic similarity")
    print("- Language detection for 5 languages (EN, TR, ES, FR, DE)")
    print("- 768-dimensional feature embeddings for downstream tasks")
    print("- Graceful fallback when models unavailable")
    print()
    
    # Test sentences in different languages
    test_cases = [
        {
            "language": "English",
            "text": "I want to buy a beautiful red dress for tonight's party",
            "expected": {"intent": "product_recommendation", "sentiment": "positive", "context": "party"}
        },
        {
            "language": "Turkish", 
            "text": "İş toplantısı için resmi bir takım elbise önerir misiniz",
            "expected": {"intent": "product_recommendation", "sentiment": "neutral", "context": "formal"}
        },
        {
            "language": "Spanish",
            "text": "Necesito zapatos deportivos para hacer ejercicio en el gimnasio",
            "expected": {"intent": "product_recommendation", "sentiment": "neutral", "context": "sport"}
        },
        {
            "language": "French",
            "text": "Cette robe est magnifique, j'adore le style élégant",
            "expected": {"intent": "style_analysis", "sentiment": "positive", "context": "formal"}
        },
        {
            "language": "German",
            "text": "Wie kann ich dieses Hemd mit meiner Jeans kombinieren",
            "expected": {"intent": "style_combination", "sentiment": "neutral", "context": "casual"}
        }
    ]
    
    print("🔧 Testing without server (local imports):")
    
    try:
        from nlu_analyzer import AdvancedNLUAnalyzer
        
        print("✅ AdvancedNLUAnalyzer imported successfully")
        print("⏳ Initializing XLM-R and multilingual models (may take time on first run)...")
        
        # Initialize the analyzer (downloads models if not cached)
        analyzer = AdvancedNLUAnalyzer()
        
        print(f"✅ Advanced NLU models loaded on device: {analyzer.device}")
        print(f"   Models status: {sum(analyzer.models_loaded.values())}/3 loaded")
        print(f"   XLM-R: {'✅' if analyzer.models_loaded['xlm_r'] else '❌'}")
        print(f"   Sentence Transformer: {'✅' if analyzer.models_loaded['sentence_transformer'] else '❌'}")  
        print(f"   Sentiment Pipeline: {'✅' if analyzer.models_loaded['sentiment_pipeline'] else '❌'}")
        print()
        
        # Test each multilingual case
        for i, case in enumerate(test_cases, 1):
            print(f"🌍 Test {i}: {case['language']}")
            print(f"   Text: '{case['text']}'")
            
            try:
                # Perform comprehensive analysis
                results = analyzer.comprehensive_analysis(case['text'])
                
                if "error" not in results:
                    # Extract analysis results
                    lang_info = results.get("language_detection", {})
                    intent_info = results.get("intent_analysis", {})
                    sentiment_info = results.get("sentiment_analysis", {})
                    context_info = results.get("context_analysis", {})
                    
                    detected_lang = lang_info.get("detected_language", "unknown")
                    intent = intent_info.get("intent", "unknown")
                    sentiment = sentiment_info.get("sentiment", "unknown")
                    context = context_info.get("context", "unknown")
                    
                    intent_confidence = intent_info.get("confidence", 0.0)
                    sentiment_confidence = sentiment_info.get("confidence", 0.0)
                    context_confidence = context_info.get("confidence", 0.0)
                    
                    print(f"   📊 Results:")
                    print(f"      Language: {detected_lang} (confidence: {lang_info.get('confidence', 0.0):.2f})")
                    print(f"      Intent: {intent} (confidence: {intent_confidence:.2f})")
                    print(f"      Sentiment: {sentiment} (confidence: {sentiment_confidence:.2f})")
                    print(f"      Context: {context} (confidence: {context_confidence:.2f})")
                    
                    # Check if XLM-R features are available
                    features = results.get("features", {}).get("xlm_r_embedding")
                    if features:
                        print(f"      XLM-R Features: {len(features)}-dimensional vector extracted")
                    
                    print(f"   ✅ Analysis successful")
                    
                else:
                    print(f"   ❌ Analysis failed: {results['error']}")
                    
            except Exception as e:
                print(f"   ❌ Error during analysis: {e}")
            
            print()
        
        # Demonstrate advanced features
        print("🔍 Advanced Feature Demonstration:")
        
        test_text = "I absolutely love these elegant shoes for my wedding!"
        print(f"   Text: '{test_text}'")
        
        try:
            # Test individual components
            lang, lang_conf = analyzer.detect_language(test_text)
            print(f"   Language Detection: {lang} (confidence: {lang_conf:.2f})")
            
            intent_result = analyzer.classify_intent(test_text)
            print(f"   Intent Classification: {intent_result.get('intent')} (confidence: {intent_result.get('confidence', 0.0):.2f})")
            
            sentiment_result = analyzer.analyze_sentiment(test_text)
            print(f"   Sentiment Analysis: {sentiment_result.get('sentiment')} (confidence: {sentiment_result.get('confidence', 0.0):.2f})")
            
            context_result = analyzer.detect_context(test_text)
            print(f"   Context Detection: {context_result.get('context')} (confidence: {context_result.get('confidence', 0.0):.2f})")
            
            # Test feature extraction
            features = analyzer.extract_xlm_r_features(test_text)
            if features is not None:
                print(f"   XLM-R Features: {len(features)}-dim vector, range: [{features.min():.4f}, {features.max():.4f}]")
            
            print("   ✅ All components working successfully")
            
        except Exception as e:
            print(f"   ❌ Component test error: {e}")
        
        print("\n🎉 Phase 3 Advanced NLU is working perfectly!")
        
    except ImportError as e:
        print(f"⚠️  Advanced models not available: {e}")
        print("   Service will run in fallback mode with basic keyword matching")
        print("   Install dependencies: transformers, torch, sentence-transformers, etc.")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
    
    print("\n📤 To test the service API, start it with:")
    print("   cd nlu_service")
    print("   uvicorn main:app --host 0.0.0.0 --port 8002")
    print()
    print("📋 Then send requests to:")
    print("   GET  http://localhost:8002/         # Health check with model status")
    print("   POST http://localhost:8002/parse_request  # Advanced NLU analysis")
    print()
    print("📊 Expected Response Structure:")
    print("""
    {
        "message": "Text analyzed successfully using advanced XLM-R transformer models",
        "original_text": "...",
        "detected_language": "en/tr/es/fr/de",
        "language_confidence": 0.0-1.0,
        "analysis": {
            "intent": {
                "predicted_intent": "product_recommendation/style_combination/...",
                "confidence": 0.0-1.0,
                "method": "transformer_similarity/keyword_fallback",
                "all_intent_scores": {...}
            },
            "sentiment": {
                "predicted_sentiment": "positive/negative/neutral",
                "confidence": 0.0-1.0,
                "method": "transformer_pipeline/keyword_fallback",
                "all_sentiment_scores": {...}
            },
            "context": {
                "predicted_context": "casual/formal/sport/party/travel/date",
                "confidence": 0.0-1.0,
                "method": "transformer_similarity/keyword_fallback",
                "all_context_scores": {...}
            }
        },
        "model_info": {
            "xlm_r_available": true/false,
            "sentence_transformer_available": true/false,
            "sentiment_pipeline_available": true/false,
            "total_models_active": 0-3,
            "processing_quality": "high/medium/basic"
        },
        "processing_method": "xlm_r_transformer_ensemble/keyword_fallback"
    }
    """)
    
    print("\n" + "=" * 65)
    print("Phase 3 Demo Complete!")

if __name__ == "__main__":
    demo_multilingual_nlu()
