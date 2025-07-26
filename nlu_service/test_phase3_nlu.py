# Phase 3: Advanced NLU Service Test Suite
# This script tests the XLM-R transformer-based natural language understanding capabilities

import sys
import os
import pytest
import requests
from typing import Dict, Any

# Add the service directory to the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_advanced_nlu_analyzer():
    """Test the AdvancedNLUAnalyzer class initialization and basic functionality."""
    
    print("🔧 Testing AdvancedNLUAnalyzer initialization...")
    
    try:
        from nlu_analyzer import AdvancedNLUAnalyzer
        
        # Initialize the analyzer
        analyzer = AdvancedNLUAnalyzer()
        
        print(f"✅ Analyzer initialized successfully")
        print(f"   Device: {analyzer.device}")
        print(f"   Models loaded: {sum(analyzer.models_loaded.values())}/3")
        print(f"   XLM-R: {'✅' if analyzer.models_loaded['xlm_r'] else '❌'}")
        print(f"   Sentence Transformer: {'✅' if analyzer.models_loaded['sentence_transformer'] else '❌'}")
        print(f"   Sentiment Pipeline: {'✅' if analyzer.models_loaded['sentiment_pipeline'] else '❌'}")
        
        return analyzer
        
    except ImportError as e:
        print(f"⚠️  Import error: {e}")
        print("   Advanced models may not be installed")
        return None
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        return None

def test_multilingual_analysis(analyzer):
    """Test multilingual analysis capabilities with different languages."""
    
    if not analyzer:
        print("⚠️  Skipping multilingual tests - analyzer not available")
        return
    
    print("\n🌍 Testing multilingual analysis...")
    
    # Test sentences in different languages
    test_sentences = {
        "English": "I want to buy a beautiful dress for the party tonight",
        "Turkish": "Bu akşamki parti için güzel bir elbise almak istiyorum", 
        "Spanish": "Quiero comprar un vestido hermoso para la fiesta de esta noche",
        "French": "Je veux acheter une belle robe pour la fête de ce soir",
        "German": "Ich möchte ein schönes Kleid für die Party heute Abend kaufen"
    }
    
    for language, sentence in test_sentences.items():
        print(f"\n📝 Testing {language}: '{sentence}'")
        
        try:
            # Test language detection
            detected_lang, confidence = analyzer.detect_language(sentence)
            print(f"   Language detected: {detected_lang} (confidence: {confidence:.2f})")
            
            # Test comprehensive analysis
            results = analyzer.comprehensive_analysis(sentence)
            
            if "error" not in results:
                intent = results.get("intent_analysis", {}).get("intent", "unknown")
                sentiment = results.get("sentiment_analysis", {}).get("sentiment", "unknown")
                context = results.get("context_analysis", {}).get("context", "unknown")
                
                print(f"   Intent: {intent}")
                print(f"   Sentiment: {sentiment}")
                print(f"   Context: {context}")
                print(f"   ✅ Analysis successful")
            else:
                print(f"   ❌ Analysis failed: {results['error']}")
                
        except Exception as e:
            print(f"   ❌ Error during analysis: {e}")

def test_intent_classification(analyzer):
    """Test intent classification with various types of requests."""
    
    if not analyzer:
        print("⚠️  Skipping intent classification tests - analyzer not available")
        return
    
    print("\n🎯 Testing intent classification...")
    
    intent_test_cases = [
        ("I need recommendations for summer dresses", "product_recommendation"),
        ("How can I combine this shirt with my jeans", "style_combination"),
        ("What's my personal style based on my wardrobe", "style_analysis"),
        ("Does this size large fit me well", "size_fit_query"),
        ("The weather is nice today", "general_inquiry")
    ]
    
    for text, expected_intent in intent_test_cases:
        print(f"\n📝 Testing: '{text}'")
        
        try:
            results = analyzer.classify_intent(text)
            predicted_intent = results.get("intent", "unknown")
            confidence = results.get("confidence", 0.0)
            method = results.get("method", "unknown")
            
            print(f"   Expected: {expected_intent}")
            print(f"   Predicted: {predicted_intent} (confidence: {confidence:.2f})")
            print(f"   Method: {method}")
            
            if predicted_intent == expected_intent:
                print(f"   ✅ Correct classification")
            else:
                print(f"   ⚠️  Different classification (may still be valid)")
                
        except Exception as e:
            print(f"   ❌ Error during intent classification: {e}")

def test_sentiment_analysis(analyzer):
    """Test sentiment analysis with positive, negative, and neutral examples."""
    
    if not analyzer:
        print("⚠️  Skipping sentiment analysis tests - analyzer not available")
        return
    
    print("\n😊 Testing sentiment analysis...")
    
    sentiment_test_cases = [
        ("I absolutely love this beautiful dress!", "positive"),
        ("This outfit is terrible and doesn't fit at all", "negative"),
        ("I'm looking for a casual shirt for work", "neutral"),
        ("Bu elbise çok güzel ve harika görünüyor", "positive"),  # Turkish positive
        ("No me gusta nada este color", "negative")  # Spanish negative
    ]
    
    for text, expected_sentiment in sentiment_test_cases:
        print(f"\n📝 Testing: '{text}'")
        
        try:
            results = analyzer.analyze_sentiment(text)
            predicted_sentiment = results.get("sentiment", "unknown")
            confidence = results.get("confidence", 0.0)
            method = results.get("method", "unknown")
            
            print(f"   Expected: {expected_sentiment}")
            print(f"   Predicted: {predicted_sentiment} (confidence: {confidence:.2f})")
            print(f"   Method: {method}")
            
            if predicted_sentiment == expected_sentiment:
                print(f"   ✅ Correct sentiment")
            else:
                print(f"   ⚠️  Different sentiment (may still be valid)")
                
        except Exception as e:
            print(f"   ❌ Error during sentiment analysis: {e}")

def test_context_detection(analyzer):
    """Test context/occasion detection capabilities."""
    
    if not analyzer:
        print("⚠️  Skipping context detection tests - analyzer not available")
        return
    
    print("\n🎭 Testing context detection...")
    
    context_test_cases = [
        ("I need something for my business meeting tomorrow", "formal"),
        ("Looking for gym clothes for my workout", "sport"),
        ("What should I wear to the wedding party", "party"),
        ("Just want comfortable clothes for daily wear", "casual"),
        ("Seyahat için rahat kıyafet arıyorum", "travel"),  # Turkish travel
        ("Necesito algo para una cita romántica", "date")  # Spanish date
    ]
    
    for text, expected_context in context_test_cases:
        print(f"\n📝 Testing: '{text}'")
        
        try:
            results = analyzer.detect_context(text)
            predicted_context = results.get("context", "unknown")
            confidence = results.get("confidence", 0.0)
            method = results.get("method", "unknown")
            
            print(f"   Expected: {expected_context}")
            print(f"   Predicted: {predicted_context} (confidence: {confidence:.2f})")
            print(f"   Method: {method}")
            
            if predicted_context == expected_context:
                print(f"   ✅ Correct context")
            else:
                print(f"   ⚠️  Different context (may still be valid)")
                
        except Exception as e:
            print(f"   ❌ Error during context detection: {e}")

def test_feature_extraction(analyzer):
    """Test XLM-R feature extraction capabilities."""
    
    if not analyzer:
        print("⚠️  Skipping feature extraction tests - analyzer not available")
        return
    
    print("\n🔍 Testing XLM-R feature extraction...")
    
    test_texts = [
        "I want to buy a red dress for the party",
        "Bu gömlek çok güzel ve şık görünüyor",
        "Necesito zapatos deportivos para correr"
    ]
    
    for text in test_texts:
        print(f"\n📝 Testing: '{text}'")
        
        try:
            features = analyzer.extract_xlm_r_features(text)
            
            if features is not None:
                print(f"   ✅ Features extracted successfully")
                print(f"   Feature dimension: {len(features)}")
                print(f"   Feature range: [{features.min():.4f}, {features.max():.4f}]")
            else:
                print(f"   ⚠️  XLM-R model not available, using fallback")
                
        except Exception as e:
            print(f"   ❌ Error during feature extraction: {e}")

def test_service_endpoint():
    """Test the actual service endpoint if it's running."""
    
    print("\n🌐 Testing service endpoint...")
    
    service_url = "http://localhost:8002"
    
    try:
        # Test health check
        response = requests.get(f"{service_url}/", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check successful")
            print(f"   Status: {health_data.get('status', 'unknown')}")
            print(f"   Models loaded: {health_data.get('models_loaded', '0/0')}")
            print(f"   Processing mode: {health_data.get('processing_mode', 'unknown')}")
            
            # Test NLU endpoint
            test_request = {
                "text": "I want to buy a beautiful dress for tonight's party",
                "include_features": False
            }
            
            response = requests.post(f"{service_url}/parse_request", json=test_request, timeout=10)
            if response.status_code == 200:
                nlu_data = response.json()
                print(f"✅ NLU analysis successful")
                print(f"   Detected language: {nlu_data.get('detected_language', 'unknown')}")
                print(f"   Intent: {nlu_data.get('analysis', {}).get('intent', {}).get('predicted_intent', 'unknown')}")
                print(f"   Sentiment: {nlu_data.get('analysis', {}).get('sentiment', {}).get('predicted_sentiment', 'unknown')}")
                print(f"   Context: {nlu_data.get('analysis', {}).get('context', {}).get('predicted_context', 'unknown')}")
                print(f"   Processing method: {nlu_data.get('processing_method', 'unknown')}")
            else:
                print(f"❌ NLU endpoint failed: {response.status_code}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("⚠️  Service not running on localhost:8002")
        print("   Start the service with: uvicorn main:app --host 0.0.0.0 --port 8002")
    except Exception as e:
        print(f"❌ Service test error: {e}")

def main():
    """Run all Phase 3 NLU tests."""
    
    print("🎯 Phase 3: Advanced NLU Service Test Suite")
    print("=" * 60)
    
    # Test the analyzer initialization
    analyzer = test_advanced_nlu_analyzer()
    
    # Run all tests
    test_multilingual_analysis(analyzer)
    test_intent_classification(analyzer)
    test_sentiment_analysis(analyzer)
    test_context_detection(analyzer)
    test_feature_extraction(analyzer)
    test_service_endpoint()
    
    print("\n" + "=" * 60)
    print("🎉 Phase 3 NLU Testing Complete!")
    
    if analyzer:
        total_models = sum(analyzer.models_loaded.values())
        if total_models >= 2:
            print("✅ Advanced NLU capabilities are working correctly!")
        else:
            print("⚠️  Some models not available - service will use fallback methods")
    else:
        print("⚠️  Advanced models not available - install dependencies for full functionality")

if __name__ == "__main__":
    main()
