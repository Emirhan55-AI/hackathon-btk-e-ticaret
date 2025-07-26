# Phase 4: Enhanced Style Profile Service with AI Integration
# Import FastAPI framework for REST API development
from fastapi import FastAPI, HTTPException, Path
# Import Pydantic for data validation and JSON serialization
from pydantic import BaseModel
# Import List type for type hints
from typing import List, Optional, Dict, Any
# Import JSON for data persistence (will be replaced with database in production)
import json
# Import os for file system operations
import os
# Import the advanced style profiler for Phase 4 capabilities
from style_profiler import AdvancedStyleProfiler
import logging
from datetime import datetime

# Configure logging for service monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the main FastAPI application instance
# This service manages advanced user style profiles with AI integration
app = FastAPI(
    title="Aura Enhanced Style Profile Service - Phase 4",  # Updated title for Phase 4
    description="Creates and manages advanced user style profiles using multi-modal AI features from image processing and NLU analysis",
    version="4.0.0"  # Phase 4 version
)

# Global variable to store the advanced style profiler instance
# This is initialized when the service starts up
style_profiler = None

@app.on_event("startup")
async def startup_event():
    """
    Service startup event handler.
    
    Initializes the advanced style profiler with AI service integrations.
    This runs once when the service starts and connects to Phase 2 & 3 services.
    """
    global style_profiler
    
    logger.info("🚀 Starting Enhanced Style Profile Service - Phase 4")
    logger.info("Initializing AI integrations with Phase 2 & 3 services...")
    
    try:
        # Initialize the advanced style profiler
        # This connects to Image Processing Service (Phase 2) and NLU Service (Phase 3)
        style_profiler = AdvancedStyleProfiler(
            image_service_url="http://localhost:8001",  # Phase 2 Image Processing Service
            nlu_service_url="http://localhost:8002"     # Phase 3 NLU Service
        )
        logger.info("✅ Enhanced Style Profile Service initialized successfully")
        logger.info("Connected to Phase 2 (Image Processing) and Phase 3 (NLU) services")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize style profiler: {e}")
        logger.info("Service will run in fallback mode with basic functionality")
        style_profiler = None

# Enhanced Pydantic models for Phase 4 advanced profiling requests
# These models support multi-modal data from Phase 2 and Phase 3 services

class ProfileUpdateRequest(BaseModel):
    garment_embeddings: Optional[List[List[float]]] = None  # New garment embedding vectors to add
    liked_items: Optional[List[str]] = None  # IDs of items the user liked
    disliked_items: Optional[List[str]] = None  # IDs of items the user disliked
    style_preferences: Optional[Dict[str, Any]] = None  # Additional style preferences

class AdvancedProfileRequest(BaseModel):
    """Enhanced profile request supporting multi-modal AI analysis."""
    user_id: str  # Unique identifier for the user
    interactions: List[Dict[str, Any]]  # List of user interactions with timestamps and data
    include_ai_analysis: bool = True  # Whether to perform advanced AI analysis
    analysis_depth: str = "comprehensive"  # Level of analysis: basic, standard, comprehensive

class ImageAnalysisRequest(BaseModel):
    """Request for integrating image analysis from Phase 2 service."""
    user_id: str  # User identifier
    image_data: str  # Base64 encoded image data
    context: Optional[str] = None  # Context for the image (outfit, single item, etc.)
    timestamp: Optional[str] = None  # When the image was uploaded

class TextAnalysisRequest(BaseModel):
    """Request for integrating text analysis from Phase 3 service."""
    user_id: str  # User identifier
    text_input: str  # User's text input (preferences, requests, etc.)
    context: Optional[str] = None  # Context for the text
    timestamp: Optional[str] = None  # When the text was submitted

# Simple file-based storage for user profiles
# In production, this would be replaced with a proper database
PROFILES_FILE = "user_profiles.json"

def load_profiles():
    """
    Load user profiles from the JSON file.
    If the file doesn't exist, return an empty dictionary.
    This simulates database read operations.
    """
    if os.path.exists(PROFILES_FILE):
        # Open and read the profiles file
        with open(PROFILES_FILE, 'r') as f:
            return json.load(f)
    # Return empty dict if file doesn't exist
    return {}

def save_profiles(profiles):
    """
    Save user profiles to the JSON file.
    This simulates database write operations.
    
    Args:
        profiles: Dictionary containing all user profiles
    """
    # Write profiles to JSON file with proper formatting
    with open(PROFILES_FILE, 'w') as f:
        json.dump(profiles, f, indent=2)

def calculate_style_vector(embeddings):
    """
    Calculate the average style vector from a list of garment embeddings.
    This creates a numerical representation of the user's overall style.
    
    Args:
        embeddings: List of embedding vectors (each vector represents a garment)
    
    Returns:
        List representing the average style vector
    """
    if not embeddings:
        # Return zero vector if no embeddings provided
        return [0.0] * 512  # Assuming 512-dimensional embeddings
    
    # Calculate the average across all embeddings
    # This assumes all embeddings have the same dimension
    num_embeddings = len(embeddings)
    embedding_dim = len(embeddings[0])
    
    # Initialize average vector with zeros
    avg_vector = [0.0] * embedding_dim
    
    # Sum all embeddings element-wise
    for embedding in embeddings:
        for i in range(embedding_dim):
            avg_vector[i] += embedding[i]
    
    # Divide by count to get average
    for i in range(embedding_dim):
        avg_vector[i] /= num_embeddings
    
    return avg_vector

# Root endpoint for health monitoring and service status
# Enhanced for Phase 4 with AI service connectivity information
@app.get("/")
async def health_check():
    """
    Enhanced health check endpoint for Phase 4 Style Profile Service.
    
    Returns service status, AI service connectivity, and profiling capabilities.
    Used by monitoring systems and load balancers.
    """
    
    # Check AI service connections
    service_status = {
        "advanced_profiler_available": style_profiler is not None,
        "phase2_integration": "pending",  # Will be checked during actual requests
        "phase3_integration": "pending"   # Will be checked during actual requests
    }
    
    return {
        "status": "Enhanced Style Profile Service is running - Phase 4",
        "service": "style_profile",
        "version": "4.0.0",
        "capabilities": [
            "Multi-modal AI profile analysis",
            "Phase 2 Image Processing integration",
            "Phase 3 NLU analysis integration", 
            "Advanced style clustering and similarity",
            "Temporal style evolution tracking",
            "Behavioral pattern analysis",
            "Personalized insights generation"
        ],
        "ai_services": service_status,
        "profiling_mode": "advanced" if style_profiler else "basic",
        "supported_features": [
            "Visual style analysis using ResNet-50, ViT, CLIP",
            "Textual preference analysis using XLM-R",
            "Multi-modal feature fusion",
            "Machine learning-based clustering",
            "FAISS similarity search",
            "Temporal pattern analysis"
        ]
    }

# Endpoint to retrieve a user's style profile
@app.get("/profile/{user_id}")
async def get_profile(user_id: str = Path(..., description="Unique identifier for the user")):
    """
    Retrieve a user's complete style profile.
    Enhanced for Phase 4 with advanced AI analysis results.
    
    Args:
        user_id: Unique string identifier for the user
    
    Returns:
        JSON response containing the user's enhanced style profile and AI insights
    """
    # Load all profiles from storage
    profiles = load_profiles()
    
    # Check if the user profile exists
    if user_id not in profiles:
        # Return HTTP 404 if user not found
        raise HTTPException(status_code=404, detail=f"Profile not found for user {user_id}")
    
    # Return the user's profile data with Phase 4 enhancements
    return {
        "user_id": user_id,
        "profile": profiles[user_id],
        "message": "Enhanced profile retrieved successfully",
        "profile_type": profiles[user_id].get("profile_version", "1.0_basic"),
        "ai_analysis_available": profiles[user_id].get("profile_version", "").startswith("4.0")
    }

# New Phase 4 endpoint for advanced profile creation using AI analysis
@app.post("/profile/{user_id}/create_advanced")
async def create_advanced_profile(
    user_id: str = Path(..., description="Unique identifier for the user"),
    request: AdvancedProfileRequest = None
):
    """
    Create an advanced user style profile using multi-modal AI analysis.
    
    This endpoint integrates with Phase 2 (Image Processing) and Phase 3 (NLU) 
    to create comprehensive style profiles using machine learning and AI features.
    
    Args:
        user_id: Unique string identifier for the user
        request: AdvancedProfileRequest containing interaction data and analysis preferences
    
    Returns:
        JSON response with the created advanced profile and AI insights
    """
    
    if not style_profiler:
        # Fallback to basic profile creation if advanced profiler not available
        logger.warning("Advanced profiler not available, creating basic profile")
        return await _create_basic_profile_fallback(user_id, request)
    
    if not request or not request.interactions:
        raise HTTPException(
            status_code=400,
            detail="Interactions data is required for advanced profile creation"
        )
    
    logger.info(f"Creating advanced profile for user {user_id} with {len(request.interactions)} interactions")
    
    try:
        # Use the advanced style profiler to create comprehensive profile
        advanced_profile = style_profiler.create_comprehensive_profile(
            user_id=user_id,
            interactions=request.interactions
        )
        
        # Load existing profiles and add/update the new advanced profile
        profiles = load_profiles()
        profiles[user_id] = advanced_profile
        save_profiles(profiles)
        
        logger.info(f"✅ Advanced profile created successfully for user {user_id}")
        
        return {
            "user_id": user_id,
            "message": "Advanced profile created successfully using multi-modal AI analysis",
            "profile": advanced_profile,
            "analysis_summary": {
                "total_interactions_processed": len(request.interactions),
                "ai_analysis_performed": True,
                "profile_confidence": advanced_profile.get("analysis_confidence", 0.0),
                "features_integrated": [
                    "Phase 2: ResNet-50, ViT, CLIP image features",
                    "Phase 3: XLM-R multilingual text features", 
                    "Advanced ML clustering and similarity analysis",
                    "Temporal style evolution tracking"
                ],
                "analysis_depth": request.analysis_depth
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to create advanced profile: {e}")
        # Fall back to basic profile creation
        return await _create_basic_profile_fallback(user_id, request)

# New Phase 4 endpoint for image-based profile updates
@app.post("/profile/{user_id}/add_image_analysis")
async def add_image_analysis(
    user_id: str = Path(..., description="Unique identifier for the user"),
    request: ImageAnalysisRequest = None
):
    """
    Add image analysis to user profile using Phase 2 Image Processing Service.
    
    Args:
        user_id: Unique string identifier for the user
        request: ImageAnalysisRequest containing image data and context
    
    Returns:
        JSON response confirming the image analysis integration
    """
    
    if not style_profiler:
        raise HTTPException(
            status_code=503,
            detail="Advanced profiling service not available"
        )
    
    if not request or not request.image_data:
        raise HTTPException(
            status_code=400,
            detail="Image data is required"
        )
    
    try:
        # Convert base64 image data to bytes (simplified - would need proper base64 decoding)
        # This is a placeholder - in production, proper base64 decoding would be implemented
        image_bytes = request.image_data.encode('utf-8')  # Placeholder conversion
        
        # Get image features from Phase 2 service
        image_features = await style_profiler.get_image_features(image_bytes)
        
        if not image_features:
            raise HTTPException(
                status_code=503,
                detail="Failed to analyze image with Phase 2 service"
            )
        
        # Load existing profile and add image analysis
        profiles = load_profiles()
        
        if user_id not in profiles:
            # Initialize basic profile if it doesn't exist
            profiles[user_id] = {
                "user_id": user_id,
                "created_at": datetime.now().isoformat() if 'datetime' in globals() else "2025-01-01",
                "image_analyses": [],
                "profile_version": "4.0_incremental"
            }
        
        # Add the new image analysis
        profiles[user_id]["image_analyses"] = profiles[user_id].get("image_analyses", [])
        profiles[user_id]["image_analyses"].append({
            "timestamp": request.timestamp or datetime.now().isoformat() if 'datetime' in globals() else "2025-01-01",
            "context": request.context,
            "analysis_results": image_features
        })
        
        # Update interaction count
        profiles[user_id]["total_interactions"] = len(profiles[user_id]["image_analyses"])
        
        save_profiles(profiles)
        
        return {
            "user_id": user_id,
            "message": "Image analysis added successfully to profile",
            "analysis_summary": {
                "features_extracted": list(image_features.keys()),
                "style_detected": image_features.get("style_classification", {}),
                "color_analysis": image_features.get("color_analysis", {}),
                "pattern_analysis": image_features.get("pattern_analysis", {})
            },
            "total_image_analyses": len(profiles[user_id]["image_analyses"])
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to add image analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Image analysis failed: {str(e)}")

# New Phase 4 endpoint for text-based profile updates
@app.post("/profile/{user_id}/add_text_analysis")
async def add_text_analysis(
    user_id: str = Path(..., description="Unique identifier for the user"),
    request: TextAnalysisRequest = None
):
    """
    Add text analysis to user profile using Phase 3 NLU Service.
    
    Args:
        user_id: Unique string identifier for the user
        request: TextAnalysisRequest containing text input and context
    
    Returns:
        JSON response confirming the text analysis integration
    """
    
    if not style_profiler:
        raise HTTPException(
            status_code=503,
            detail="Advanced profiling service not available"
        )
    
    if not request or not request.text_input:
        raise HTTPException(
            status_code=400,
            detail="Text input is required"
        )
    
    try:
        # Get NLU analysis from Phase 3 service
        nlu_analysis = await style_profiler.get_nlu_analysis(request.text_input)
        
        if not nlu_analysis:
            raise HTTPException(
                status_code=503,
                detail="Failed to analyze text with Phase 3 service"
            )
        
        # Load existing profile and add text analysis
        profiles = load_profiles()
        
        if user_id not in profiles:
            # Initialize basic profile if it doesn't exist
            profiles[user_id] = {
                "user_id": user_id,
                "created_at": datetime.now().isoformat() if 'datetime' in globals() else "2025-01-01",
                "text_analyses": [],
                "profile_version": "4.0_incremental"
            }
        
        # Add the new text analysis
        profiles[user_id]["text_analyses"] = profiles[user_id].get("text_analyses", [])
        profiles[user_id]["text_analyses"].append({
            "timestamp": request.timestamp or datetime.now().isoformat() if 'datetime' in globals() else "2025-01-01",
            "original_text": request.text_input,
            "context": request.context,
            "analysis_results": nlu_analysis
        })
        
        # Update interaction count
        profiles[user_id]["total_interactions"] = len(profiles[user_id].get("text_analyses", []) + profiles[user_id].get("image_analyses", []))
        
        save_profiles(profiles)
        
        return {
            "user_id": user_id,
            "message": "Text analysis added successfully to profile",
            "analysis_summary": {
                "detected_language": nlu_analysis.get("detected_language", "unknown"),
                "intent_detected": nlu_analysis.get("intent_analysis", {}),
                "sentiment_detected": nlu_analysis.get("sentiment_analysis", {}),
                "context_detected": nlu_analysis.get("context_analysis", {}),
                "xlm_r_features_available": bool(nlu_analysis.get("xlm_r_features"))
            },
            "total_text_analyses": len(profiles[user_id]["text_analyses"])
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to add text analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Text analysis failed: {str(e)}")

# Helper function for fallback profile creation
async def _create_basic_profile_fallback(user_id: str, request: AdvancedProfileRequest) -> Dict[str, Any]:
    """
    Create a basic profile when advanced profiling is not available.
    
    Args:
        user_id: User identifier
        request: Profile request with interaction data
        
    Returns:
        Basic profile with interaction count
    """
    
    basic_profile = {
        "user_id": user_id,
        "profile_version": "4.0_fallback",
        "created_at": datetime.now().isoformat(),
        "total_interactions": len(request.interactions) if request and request.interactions else 0,
        "analysis_confidence": 0.3,
        "status": "basic_mode",
        "message": "Advanced AI analysis not available. Basic profile created.",
        "available_data": {
            "interactions": len(request.interactions) if request and request.interactions else 0
        }
    }
    
    # Save the basic profile
    profiles = load_profiles()
    profiles[user_id] = basic_profile
    save_profiles(profiles)
    
    return {
        "user_id": user_id,
        "message": "Basic profile created (advanced AI analysis unavailable)",
        "profile": basic_profile,
        "analysis_summary": {
            "total_interactions_processed": basic_profile["total_interactions"],
            "ai_analysis_performed": False,
            "profile_confidence": basic_profile["analysis_confidence"],
            "recommendation": "Install Phase 2 & 3 services for advanced analysis"
        }
    }

# Endpoint to update a user's style profile (Enhanced for Phase 4)
@app.post("/profile/{user_id}/update")
async def update_profile(
    user_id: str = Path(..., description="Unique identifier for the user"),
    update_request: ProfileUpdateRequest = None
):
    """
    Update a user's style profile with new data.
    Enhanced for Phase 4 to maintain compatibility with basic profile updates.
    
    Args:
        user_id: Unique string identifier for the user
        update_request: ProfileUpdateRequest containing the data to update
    
    Returns:
        JSON response confirming the profile update
    """
    # Load existing profiles
    profiles = load_profiles()
    
    # Initialize profile if it doesn't exist
    if user_id not in profiles:
        profiles[user_id] = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "garment_embeddings": [],  # List of embedding vectors for user's garments
            "style_vector": [],  # Average style representation
            "liked_items": [],  # Items the user explicitly liked
            "disliked_items": [],  # Items the user explicitly disliked
            "style_preferences": {},  # Additional preference data
            "interaction_count": 0,  # Number of interactions for profile confidence
            "profile_version": "4.0_basic"  # Updated for Phase 4
        }
    
    user_profile = profiles[user_id]
    
    # Update garment embeddings if provided
    if update_request and update_request.garment_embeddings:
        # Add new embeddings to the existing list
        user_profile["garment_embeddings"].extend(update_request.garment_embeddings)
        
        # Recalculate the style vector with all embeddings
        user_profile["style_vector"] = calculate_style_vector(user_profile["garment_embeddings"])
    
    # Update liked items if provided
    if update_request and update_request.liked_items:
        # Add new liked items, avoiding duplicates
        for item in update_request.liked_items:
            if item not in user_profile["liked_items"]:
                user_profile["liked_items"].append(item)
    
    # Update disliked items if provided
    if update_request and update_request.disliked_items:
        # Add new disliked items, avoiding duplicates
        for item in update_request.disliked_items:
            if item not in user_profile["disliked_items"]:
                user_profile["disliked_items"].append(item)
    
    # Update style preferences if provided
    if update_request and update_request.style_preferences:
        # Merge new preferences with existing ones
        user_profile["style_preferences"].update(update_request.style_preferences)
    
    # Increment interaction count to track profile confidence
    user_profile["interaction_count"] += 1
    user_profile["last_updated"] = datetime.now().isoformat()
    
    # Save updated profiles back to storage
    save_profiles(profiles)
    
    return {
        "user_id": user_id,
        "message": "Profile updated successfully (Phase 4 enhanced)",
        "updated_profile": user_profile,
        "update_summary": {
            "embeddings_added": len(update_request.garment_embeddings) if update_request and update_request.garment_embeddings else 0,
            "liked_items_added": len(update_request.liked_items) if update_request and update_request.liked_items else 0,
            "disliked_items_added": len(update_request.disliked_items) if update_request and update_request.disliked_items else 0,
            "total_interactions": user_profile["interaction_count"],
            "profile_version": user_profile.get("profile_version", "4.0_basic")
        },
        "recommendations": {
            "next_steps": "Consider using /create_advanced endpoint for AI-powered profile analysis",
            "ai_analysis_available": style_profiler is not None
        }
    }
