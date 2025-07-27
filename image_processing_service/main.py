# Import FastAPI framework - this is the core web framework for building REST APIs
from fastapi import FastAPI, File, UploadFile, HTTPException
# Import JSONResponse for custom response formatting
from fastapi.responses import JSONResponse
# Import Path for type hints when working with file paths
from pathlib import Path
# Import os for operating system interface operations
import os
# Import logging for debugging and monitoring
import logging
# Import PIL for image processing
from PIL import Image
# Import io for handling byte streams
import io

# Import our advanced image analyzer module
try:
    from image_analyzer import ClothingImageAnalyzer
    # Global analyzer instance (initialized once for efficiency)
    analyzer = None
except ImportError as e:
    # If AI libraries are not installed, fall back to placeholder mode
    logging.warning(f"AI libraries not available: {e}. Running in placeholder mode.")
    analyzer = None

# Configure logging for the service
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the main FastAPI application instance
# This object handles all the API routes and requests for the Image Processing Service
app = FastAPI(
    title="Aura Image Processing Service",  # Service name shown in API docs
    description="Analyzes clothing photos using advanced AI models (Advanced CV Detection, CLIP, ResNet-50, ViT)",  # Enhanced description
    version="2.0.0"  # Updated version for Phase 2
)

@app.on_event("startup")
async def startup_event():
    """
    Initialize the image analyzer when the service starts.
    This loads all AI models into memory for faster processing.
    """
    global analyzer
    try:
        if analyzer is None:
            logger.info("Initializing ClothingImageAnalyzer with AI models...")
            # Initialize the analyzer with all AI models
            # This may take a few minutes on first startup as models are downloaded
            analyzer = ClothingImageAnalyzer()
            logger.info("Image analyzer initialized successfully!")
    except Exception as e:
        logger.error(f"Failed to initialize image analyzer: {e}")
        logger.info("Service will run in placeholder mode without AI models.")
        analyzer = None

# Root endpoint for health checks
# This endpoint helps other services and monitoring tools verify the service is running
@app.get("/")
async def health_check():
    """
    Health check endpoint that returns the service status.
    This is used by load balancers and monitoring systems to verify service availability.
    """
    # Check if AI models are loaded
    ai_status = "AI models loaded" if analyzer is not None else "Running in placeholder mode"
    
    return {
        "status": "Image Processing Service is running", 
        "service": "image_processing",
        "version": "2.0.0",
        "ai_status": ai_status,
        "capabilities": [
            "clothing_detection",
            "style_analysis", 
            "color_analysis",
            "pattern_recognition",
            "feature_extraction",
            "clip_embeddings"
        ]
    }

# Main image analysis endpoint - this is where users upload photos for comprehensive analysis
@app.post("/analyze_image")
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyzes an uploaded clothing photo using advanced AI models.
    This endpoint now uses real AI models (ResNet-50, ViT, CLIP) for comprehensive analysis.
    
    Args:
        file: The uploaded image file (JPEG, PNG, etc.)
    
    Returns:
        JSON response containing detailed analysis results including:
        - Detected clothing items using advanced computer vision algorithms
        - Style attributes (casual, formal, sporty, etc.)
        - Color analysis (dominant colors and color distribution)
        - Pattern recognition (solid, striped, floral, etc.)
        - Feature embeddings for similarity matching
    """
    
    # Validate that a file was actually uploaded
    if not file:
        # Return HTTP 400 error if no file provided
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    # Check if the uploaded file is an image by examining its content type
    if not file.content_type or not file.content_type.startswith("image/"):
        # Return HTTP 400 error if file is not an image
        raise HTTPException(status_code=400, detail="File must be an image (JPEG, PNG, etc.)")
    
    try:
        # Read the uploaded file content into memory
        # This loads the entire image file for processing
        file_content = await file.read()
        logger.info(f"Processing uploaded image: {file.filename} ({len(file_content)} bytes)")
        
        # Convert file content to PIL Image object
        # PIL (Python Imaging Library) is used for image manipulation
        image = Image.open(io.BytesIO(file_content))
        logger.info(f"Image loaded: {image.size[0]}x{image.size[1]} pixels, mode: {image.mode}")
        
        # Check if AI analyzer is available
        if analyzer is not None:
            # Use advanced AI models for comprehensive analysis
            logger.info("Performing AI-powered comprehensive analysis...")
            
            # Run comprehensive analysis using all AI models
            # This includes ResNet-50, ViT, CLIP, and various attribute analyzers
            analysis_results = analyzer.comprehensive_analysis(image)
            
            # Prepare the response with complete analysis results
            response_data = {
                "message": "Image analyzed successfully using advanced AI models",
                "filename": file.filename,
                "file_size_bytes": len(file_content),
                "image_dimensions": {
                    "width": image.size[0],
                    "height": image.size[1]
                },
                "content_type": file.content_type,
                "processing_method": "ai_powered_analysis",
                "analysis_results": analysis_results,
                "model_info": {
                    "feature_extractors": ["ResNet-50", "Vision Transformer (ViT)"],
                    "embedding_model": "CLIP (openai/clip-vit-base-patch32)",
                    "detection_model": "Advanced Computer Vision Detection System",
                    "total_models": 4
                },
                "performance_notes": [
                    "Analysis includes deep learning-based feature extraction",
                    "Style and color analysis using CLIP text-image understanding",
                    "Pattern recognition through semantic similarity matching",
                    "Feature embeddings suitable for similarity search and recommendations"
                ]
            }
            
            logger.info("AI-powered analysis completed successfully!")
            return response_data
            
        else:
            # Fall back to placeholder analysis if AI models are not available
            logger.info("AI models not available, using placeholder analysis...")
            
            # Basic placeholder analysis without AI models
            # This provides a response structure similar to the AI version
            placeholder_results = {
                "detected_items": [
                    {
                        "item_id": "placeholder_001",
                        "category": "clothing_item",
                        "confidence": 0.75,
                        "bbox": [0, 0, image.size[0], image.size[1]],  # Full image bounding box
                        "attributes": {
                            "color": "unknown",
                            "pattern": "unknown", 
                            "style": "unknown"
                        }
                    }
                ],
                "features": {
                    "placeholder_embedding": [0.1] * 512,  # Mock 512-dimensional embedding
                    "feature_dimensions": {"placeholder": 512}
                },
                "style_analysis": {
                    "dominant_style": "casual",
                    "style_confidence": 0.5
                },
                "color_analysis": {
                    "dominant_color": "unknown",
                    "color_confidence": 0.5
                },
                "pattern_analysis": {
                    "dominant_pattern": "solid",
                    "pattern_confidence": 0.5
                }
            }
            
            response_data = {
                "message": "Image processed using placeholder analysis (AI models not loaded)",
                "filename": file.filename,
                "file_size_bytes": len(file_content),
                "image_dimensions": {
                    "width": image.size[0],
                    "height": image.size[1]
                },
                "content_type": file.content_type,
                "processing_method": "placeholder_mode",
                "analysis_results": placeholder_results,
                "note": "Install PyTorch, transformers, and other AI libraries for full functionality"
            }
            
            return response_data
            
    except Exception as e:
        # Handle any errors that occur during image processing
        logger.error(f"Error processing image {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing image: {str(e)}"
        )

# Run the server when this file is executed directly
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Aura Image Processing Service...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
