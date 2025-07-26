# Phase 2 Demo Script - ImageProcessingService with AI Models
# This script demonstrates the advanced AI capabilities implemented in Phase 2

import requests
import base64
from PIL import Image
import io

def create_demo_image():
    """Create a simple demo image for testing"""
    # Create a simple test image (blue shirt representation)
    image = Image.new('RGB', (300, 400), color=(70, 130, 180))  # Steel blue color
    
    # Add some simple patterns to make it more interesting
    for y in range(100, 200, 20):
        for x in range(50, 250):
            if (x + y) % 40 < 20:
                image.putpixel((x, y), (255, 255, 255))  # White stripes
    
    return image

def demo_image_analysis():
    """Demonstrate the image analysis capabilities"""
    print("🎯 Phase 2 Demo: Advanced AI Image Analysis")
    print("=" * 50)
    
    # Note: This demo shows how to use the service
    # The actual service needs to be running on localhost:8001
    
    service_url = "http://localhost:8001"
    
    print("📋 Service Capabilities:")
    print("- ResNet-50 feature extraction")
    print("- Vision Transformer (ViT) analysis") 
    print("- CLIP image-text embeddings")
    print("- Style attribute detection")
    print("- Color and pattern analysis")
    print("- Multi-model ensemble processing")
    print()
    
    # Create demo image
    print("🖼️  Creating demo clothing image...")
    demo_image = create_demo_image()
    
    # Convert image to bytes for upload
    img_buffer = io.BytesIO()
    demo_image.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    print("📤 To test the service, start it with:")
    print("   uvicorn main:app --host 0.0.0.0 --port 8001")
    print()
    print("📋 Then send requests to:")
    print(f"   GET  {service_url}/         # Health check")
    print(f"   POST {service_url}/analyze_image  # Image analysis")
    print()
    print("📊 Expected Response Structure:")
    print("""
    {
        "message": "Image analyzed successfully using advanced AI models",
        "analysis_results": {
            "detected_items": [...],
            "features": {
                "resnet_features": [2048-dim vector],
                "vit_features": [768-dim vector], 
                "clip_embedding": [512-dim vector]
            },
            "style_analysis": {
                "dominant_style": "casual/formal/sporty",
                "style_confidence": 0.0-1.0
            },
            "color_analysis": {
                "dominant_color": "blue/red/green/etc",
                "color_confidence": 0.0-1.0
            },
            "pattern_analysis": {
                "dominant_pattern": "solid/striped/floral/etc",
                "pattern_confidence": 0.0-1.0
            }
        },
        "model_info": {
            "feature_extractors": ["ResNet-50", "ViT"],
            "embedding_model": "CLIP",
            "total_models": 3
        }
    }
    """)
    
    print("🔧 Testing without server (local imports):")
    try:
        # Test local imports
        import sys
        import os
        sys.path.append('image_processing_service')
        
        from image_analyzer import ClothingImageAnalyzer
        
        print("✅ ClothingImageAnalyzer imported successfully")
        print("⏳ Initializing AI models (may take time on first run)...")
        
        # This will download models if not cached
        analyzer = ClothingImageAnalyzer()
        print(f"✅ AI models loaded on device: {analyzer.device}")
        
        # Test analysis
        print("🔍 Running analysis on demo image...")
        results = analyzer.comprehensive_analysis(demo_image)
        
        print("📊 Analysis Results:")
        print(f"   Style: {results['style_analysis']['dominant_style']} "
              f"(confidence: {results['style_analysis']['style_confidence']:.2f})")
        print(f"   Color: {results['color_analysis']['dominant_color']} "
              f"(confidence: {results['color_analysis']['color_confidence']:.2f})")
        print(f"   Pattern: {results['pattern_analysis']['dominant_pattern']} "
              f"(confidence: {results['pattern_analysis']['pattern_confidence']:.2f})")
        print(f"   Feature dimensions: ResNet={len(results['features']['resnet_features'])}, "
              f"ViT={len(results['features']['vit_features'])}, "
              f"CLIP={len(results['features']['clip_embedding'])}")
        
        print("\n🎉 Phase 2 ImageProcessingService is working perfectly!")
        
    except ImportError as e:
        print(f"⚠️  AI models not available: {e}")
        print("   Service will run in placeholder mode")
        print("   Install: torch, torchvision, transformers, timm")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
    
    print("\n" + "=" * 50)
    print("Phase 2 Demo Complete!")

if __name__ == "__main__":
    demo_image_analysis()
