# Phase 5: Enhanced Combination Engine Service with Multi-Modal AI Integration
# Import FastAPI framework for REST API development
from fastapi import FastAPI, HTTPException
# Import Pydantic for request/response data validation
from pydantic import BaseModel
# Import typing utilities for type hints
from typing import List, Optional, Dict, Any
# Import random for placeholder combination generation (Phase 1 fallback)
import random
# Import the intelligent combination engine for Phase 5 AI capabilities
from intelligent_combiner import IntelligentCombinationEngine
# Import logging for service monitoring
import logging
from datetime import datetime

# Configure comprehensive logging for the enhanced service
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the main FastAPI application instance
# This service generates personalized clothing combinations using multi-modal AI
app = FastAPI(
    title="Aura Intelligent Combination Engine Service - Phase 5",  # Updated title for Phase 5
    description="Generates intelligent clothing combinations using multi-modal AI features from image processing (Phase 2) and style profiling (Phase 4)",  # Enhanced description
    version="5.0.0"  # Phase 5 version
)

# Global variable to store the intelligent combination engine instance
# This integrates Phase 2 and Phase 4 AI capabilities
intelligent_engine = None

@app.on_event("startup")
async def startup_event():
    """
    Initialize the intelligent combination engine when the service starts.
    Connects to Phase 2 (image processing) and Phase 4 (style profiling) services.
    """
    global intelligent_engine
    try:
        logger.info("Initializing Intelligent Combination Engine - Phase 5")
        
        # Initialize the AI-powered combination engine with service URLs
        intelligent_engine = IntelligentCombinationEngine(
            image_service_url="http://localhost:8001",  # Phase 2 image processing service
            style_service_url="http://localhost:8003"   # Phase 4 style profiling service
        )
        
        logger.info("✅ Intelligent Combination Engine initialized successfully")
        logger.info("   Multi-modal AI integration ready")
        logger.info("   Connected to Phase 2 (Image Processing) and Phase 4 (Style Profiling)")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize Intelligent Combination Engine: {e}")
        logger.info("   Service will operate in fallback mode with basic combination logic")

# Enhanced Pydantic models for Phase 5 intelligent combination requests
# Defines comprehensive data structures for multi-modal AI-powered combination generation

class IntelligentCombinationRequest(BaseModel):
    """Enhanced request model for intelligent combination generation with multi-modal AI features."""
    user_id: str  # Unique identifier for the user (required for Phase 4 style profile retrieval)
    style_profile: Optional[Dict[str, Any]] = None  # Optional user's style profile data (from Phase 4)
    context: Optional[str] = "casual"  # Occasion context (work, casual, party, sport, date)
    occasion: Optional[str] = None  # Specific occasion details for fine-tuning
    weather: Optional[str] = None  # Weather conditions to consider for combination
    preferences: Optional[Dict[str, Any]] = None  # Additional user preferences and constraints
    wardrobe_items: Optional[Dict[str, List[Dict]]] = None  # User's available wardrobe items
    ai_features_enabled: Optional[bool] = True  # Whether to use multi-modal AI features
    combination_count: Optional[int] = 1  # Number of combinations to generate
    include_analysis: Optional[bool] = True  # Whether to include detailed compatibility analysis

class CombinationRequest(BaseModel):
    """Legacy request model for backward compatibility with Phase 1 functionality."""
    user_id: str  # Unique identifier for the user
    style_profile: Optional[Dict[str, Any]] = None  # User's style profile data
    context: Optional[str] = "casual"  # Occasion context (sport, work, casual, formal)
    occasion: Optional[str] = None  # Specific occasion details
    weather: Optional[str] = None  # Weather conditions to consider
    preferences: Optional[Dict[str, Any]] = None  # Additional user preferences

# Mock wardrobe data for demonstration purposes
# In production, this would come from the user's actual wardrobe data
MOCK_WARDROBE = {
    "tops": [
        {"id": "top_001", "type": "shirt", "color": "blue", "style": "casual", "pattern": "solid"},
        {"id": "top_002", "type": "t-shirt", "color": "white", "style": "casual", "pattern": "solid"},
        {"id": "top_003", "type": "blouse", "color": "black", "style": "formal", "pattern": "solid"},
        {"id": "top_004", "type": "polo", "color": "navy", "style": "sport", "pattern": "solid"},
        {"id": "top_005", "type": "tank top", "color": "gray", "style": "sport", "pattern": "solid"}
    ],
    "bottoms": [
        {"id": "bottom_001", "type": "jeans", "color": "blue", "style": "casual", "pattern": "denim"},
        {"id": "bottom_002", "type": "chinos", "color": "khaki", "style": "casual", "pattern": "solid"},
        {"id": "bottom_003", "type": "dress pants", "color": "black", "style": "formal", "pattern": "solid"},
        {"id": "bottom_004", "type": "shorts", "color": "navy", "style": "sport", "pattern": "solid"},
        {"id": "bottom_005", "type": "leggings", "color": "black", "style": "sport", "pattern": "solid"}
    ],
    "shoes": [
        {"id": "shoe_001", "type": "sneakers", "color": "white", "style": "casual", "pattern": "solid"},
        {"id": "shoe_002", "type": "dress shoes", "color": "black", "style": "formal", "pattern": "leather"},
        {"id": "shoe_003", "type": "athletic shoes", "color": "gray", "style": "sport", "pattern": "solid"},
        {"id": "shoe_004", "type": "loafers", "color": "brown", "style": "casual", "pattern": "leather"}
    ]
}

def filter_items_by_context(context: str):
    """
    Filter wardrobe items based on the context/occasion.
    This helps ensure combinations are appropriate for the situation.
    
    Args:
        context: The occasion context (sport, work, casual, formal)
    
    Returns:
        Dictionary containing filtered items by category
    """
    # Create filtered wardrobe based on context
    filtered_wardrobe = {"tops": [], "bottoms": [], "shoes": []}
    
    # Filter each category based on context appropriateness
    for category in ["tops", "bottoms", "shoes"]:
        for item in MOCK_WARDROBE[category]:
            # Include items that match the context or are versatile (casual)
            if item["style"] == context or (context == "work" and item["style"] == "formal"):
                filtered_wardrobe[category].append(item)
            # Include casual items for most contexts as they're versatile
            elif context in ["casual", "sport"] and item["style"] == "casual":
                filtered_wardrobe[category].append(item)
    
    return filtered_wardrobe

def check_color_compatibility(item1, item2, item3):
    """
    Basic color compatibility check for clothing combinations.
    This implements simple color matching rules for aesthetically pleasing outfits.
    
    Args:
        item1, item2, item3: Clothing items to check for color compatibility
    
    Returns:
        Float value representing compatibility score (0.0 to 1.0)
    """
    colors = [item1["color"], item2["color"], item3["color"]]
    
    # Perfect score for monochromatic (same color) combinations
    if len(set(colors)) == 1:
        return 1.0
    
    # High score for neutral color combinations
    neutral_colors = {"white", "black", "gray", "navy", "beige"}
    if all(color in neutral_colors for color in colors):
        return 0.9
    
    # Good score if at least one neutral color is present
    if any(color in neutral_colors for color in colors):
        return 0.7
    
    # Basic complementary color rules (simplified)
    complementary_pairs = [
        ("blue", "white"), ("black", "white"), ("navy", "white"),
        ("blue", "khaki"), ("gray", "blue"), ("brown", "navy")
    ]
    
    # Check if any two colors form a complementary pair
    for color1 in colors:
        for color2 in colors:
            if (color1, color2) in complementary_pairs or (color2, color1) in complementary_pairs:
                return 0.8
    
    # Default compatibility score
    return 0.5

def generate_style_appropriate_combination(filtered_wardrobe, context):
    """
    Generate a clothing combination that's appropriate for the given context.
    Uses basic rules to ensure style coherence and appropriateness.
    
    Args:
        filtered_wardrobe: Dictionary of filtered clothing items
        context: The occasion context
    
    Returns:
        Dictionary containing the generated combination with compatibility score
    """
    # Ensure we have items in each category
    if not all(filtered_wardrobe[category] for category in ["tops", "bottoms", "shoes"]):
        return None
    
    best_combination = None
    best_score = 0.0
    
    # Try multiple random combinations and pick the best one
    for _ in range(20):  # Try 20 different combinations
        # Randomly select one item from each category
        top = random.choice(filtered_wardrobe["tops"])
        bottom = random.choice(filtered_wardrobe["bottoms"])
        shoe = random.choice(filtered_wardrobe["shoes"])
        
        # Calculate compatibility score for this combination
        compatibility_score = check_color_compatibility(top, bottom, shoe)
        
        # Keep track of the best combination
        if compatibility_score > best_score:
            best_score = compatibility_score
            best_combination = {
                "top": top,
                "bottom": bottom,
                "shoes": shoe,
                "compatibility_score": compatibility_score,
                "style_coherence": "high" if compatibility_score > 0.8 else "medium" if compatibility_score > 0.6 else "basic"
            }
    
    return best_combination

# Enhanced root endpoint for comprehensive health monitoring with AI service status
@app.get("/")
async def health_check():
    """
    Enhanced health check endpoint that monitors AI service integration status.
    Provides detailed information about Phase 2 and Phase 4 service connectivity.
    Used by monitoring systems, load balancers, and developers for service status.
    """
    try:
        # Basic service status
        status_info = {
            "status": "Intelligent Combination Engine Service is running - Phase 5",
            "service": "intelligent_combination_engine",
            "version": "5.0.0",
            "phase": "5 - Multi-Modal AI Integration",
            "timestamp": datetime.now().isoformat()
        }
        
        # Check intelligent engine initialization status
        if intelligent_engine:
            status_info["ai_engine_status"] = "initialized"
            status_info["multi_modal_ai"] = "enabled"
            status_info["integrated_services"] = {
                "phase_2_image_processing": "connected",
                "phase_4_style_profiling": "connected"
            }
            status_info["ai_capabilities"] = [
                "Visual compatibility analysis using CLIP embeddings",
                "Style coherence assessment with fashion expertise",
                "Color harmony calculation using color theory",
                "Pattern balance optimization",
                "Context appropriateness evaluation",
                "Personalized recommendations with user profiles"
            ]
        else:
            status_info["ai_engine_status"] = "fallback_mode"
            status_info["multi_modal_ai"] = "disabled"
            status_info["message"] = "Operating in basic combination mode"
        
        logger.info("Health check completed successfully")
        return status_info
        
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Service health check failed: {str(e)}")

# Enhanced main endpoint for intelligent clothing combination generation using multi-modal AI
@app.post("/generate_intelligent_combination")
async def generate_intelligent_combination(request: IntelligentCombinationRequest):
    """
    Generate intelligent clothing combinations using multi-modal AI integration.
    
    This endpoint leverages:
    - Phase 2: Image processing features (ResNet-50, ViT, CLIP embeddings)
    - Phase 4: Advanced style profiling with behavioral analysis
    - Phase 5: Intelligent combination algorithms with graph analysis
    
    Args:
        request: IntelligentCombinationRequest with comprehensive user and context data
    
    Returns:
        JSON response with AI-powered clothing combination and detailed analysis
    """
    try:
        # Validate that user_id is provided for personalization
        if not request.user_id:
            raise HTTPException(status_code=400, detail="User ID is required for intelligent combination generation")
        
        logger.info(f"Generating intelligent combination for user: {request.user_id}")
        logger.info(f"Context: {request.context}, AI Features: {request.ai_features_enabled}")
        
        # Use provided context or default to casual
        context = request.context or "casual"
        
        # Get user's wardrobe items (use provided or fetch from mock data)
        if request.wardrobe_items:
            wardrobe_items = request.wardrobe_items
            logger.info("Using provided wardrobe items")
        else:
            # Use enhanced mock wardrobe for demonstration
            wardrobe_items = get_enhanced_mock_wardrobe()
            logger.info("Using enhanced mock wardrobe items")
        
        # Check if intelligent engine is available and AI features are enabled
        if intelligent_engine and request.ai_features_enabled:
            logger.info("Using intelligent AI-powered combination generation")
            
            # Get or use provided style profile
            if request.style_profile:
                user_style_profile = request.style_profile
                logger.info("Using provided style profile")
            else:
                # Retrieve style profile from Phase 4 service
                user_style_profile = await intelligent_engine.get_style_profile(request.user_id)
                logger.info("Retrieved style profile from Phase 4 service")
            
            # Generate intelligent combination using multi-modal AI
            combination_result = intelligent_engine.generate_intelligent_combination(
                wardrobe_items=wardrobe_items,
                user_style_profile=user_style_profile,
                context=context,
                user_id=request.user_id
            )
            
            # Check if combination generation was successful
            if combination_result.get("error"):
                logger.warning(f"Intelligent combination failed: {combination_result['error']}")
                raise HTTPException(status_code=404, detail=combination_result["error"])
            
            # Prepare enhanced response with AI analysis
            response = {
                "message": "Intelligent combination generated successfully using multi-modal AI",
                "user_id": request.user_id,
                "context": context,
                "generation_method": "multi_modal_ai_phase5",
                "combination": combination_result,
                "ai_analysis": {
                    "confidence_level": combination_result.get("confidence_level", "medium"),
                    "overall_score": combination_result.get("overall_score", 0.0),
                    "detailed_scores": combination_result.get("detailed_scores", {}),
                    "combinations_evaluated": combination_result.get("combinations_evaluated", 0)
                },
                "intelligent_recommendations": combination_result.get("intelligent_recommendations", {}),
                "service_info": {
                    "phase": "5 - Multi-Modal AI Integration",
                    "ai_features_used": [
                        "Visual compatibility (Phase 2 CLIP embeddings)",
                        "Style coherence (Fashion expertise rules)",
                        "Color harmony (Color theory algorithms)",
                        "Context appropriateness (Occasion analysis)",
                        "Pattern balance (Aesthetic optimization)",
                        "User personalization (Phase 4 style profiles)"
                    ]
                }
            }
            
            logger.info(f"✅ Intelligent combination generated with score: {combination_result.get('overall_score', 0.0):.3f}")
            return response
            
        else:
            # Fallback to basic combination generation (Phase 1 functionality)
            logger.info("Using fallback basic combination generation")
            return await generate_basic_combination_fallback(request.user_id, context, wardrobe_items)
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"❌ Error in intelligent combination generation: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Intelligent combination generation failed: {str(e)}"
        )

# Legacy endpoint for backward compatibility with Phase 1 functionality
@app.post("/generate_combination")
async def generate_combination(request: CombinationRequest):
    """
    Legacy combination generation endpoint for backward compatibility.
    Maintains Phase 1 functionality while providing upgrade path to intelligent features.
    
    Args:
        request: CombinationRequest with basic user and context data
    
    Returns:
        JSON response with clothing combination (basic or intelligent based on availability)
    """
    try:
        logger.info(f"Legacy combination request for user: {request.user_id}")
        
        # Convert legacy request to intelligent request format
        intelligent_request = IntelligentCombinationRequest(
            user_id=request.user_id,
            style_profile=request.style_profile,
            context=request.context or "casual",
            occasion=request.occasion,
            weather=request.weather,
            preferences=request.preferences,
            ai_features_enabled=True  # Enable AI features by default
        )
        
        # Use the intelligent combination generation
        return await generate_intelligent_combination(intelligent_request)
        
    except Exception as e:
        logger.error(f"❌ Error in legacy combination generation: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Combination generation failed: {str(e)}"
        )

def get_enhanced_mock_wardrobe() -> Dict[str, List[Dict]]:
    """
    Get enhanced mock wardrobe data with comprehensive item information for Phase 5 demonstration.
    In production, this would integrate with user's actual wardrobe data from database or Phase 2 analysis.
    
    Returns:
        Dictionary containing categorized wardrobe items with detailed attributes
    """
    return {
        "tops": [
            {"id": "top_001", "type": "shirt", "color": "blue", "style": "casual", "pattern": "solid", "formality": 0.6},
            {"id": "top_002", "type": "t-shirt", "color": "white", "style": "casual", "pattern": "solid", "formality": 0.3},
            {"id": "top_003", "type": "blouse", "color": "black", "style": "formal", "pattern": "solid", "formality": 0.8},
            {"id": "top_004", "type": "polo", "color": "navy", "style": "smart_casual", "pattern": "solid", "formality": 0.5},
            {"id": "top_005", "type": "tank top", "color": "gray", "style": "sporty", "pattern": "solid", "formality": 0.2},
            {"id": "top_006", "type": "sweater", "color": "beige", "style": "casual", "pattern": "textured", "formality": 0.4},
            {"id": "top_007", "type": "blazer", "color": "charcoal", "style": "formal", "pattern": "solid", "formality": 0.9}
        ],
        "bottoms": [
            {"id": "bottom_001", "type": "jeans", "color": "blue", "style": "casual", "pattern": "denim", "formality": 0.4},
            {"id": "bottom_002", "type": "chinos", "color": "khaki", "style": "smart_casual", "pattern": "solid", "formality": 0.6},
            {"id": "bottom_003", "type": "dress pants", "color": "black", "style": "formal", "pattern": "solid", "formality": 0.8},
            {"id": "bottom_004", "type": "shorts", "color": "navy", "style": "casual", "pattern": "solid", "formality": 0.2},
            {"id": "bottom_005", "type": "leggings", "color": "black", "style": "sporty", "pattern": "solid", "formality": 0.1},
            {"id": "bottom_006", "type": "skirt", "color": "gray", "style": "smart_casual", "pattern": "solid", "formality": 0.7}
        ],
        "shoes": [
            {"id": "shoe_001", "type": "sneakers", "color": "white", "style": "casual", "pattern": "solid", "formality": 0.3},
            {"id": "shoe_002", "type": "dress shoes", "color": "black", "style": "formal", "pattern": "leather", "formality": 0.9},
            {"id": "shoe_003", "type": "athletic shoes", "color": "gray", "style": "sporty", "pattern": "solid", "formality": 0.1},
            {"id": "shoe_004", "type": "loafers", "color": "brown", "style": "smart_casual", "pattern": "leather", "formality": 0.7},
            {"id": "shoe_005", "type": "boots", "color": "black", "style": "casual", "pattern": "leather", "formality": 0.5}
        ]
    }

async def generate_basic_combination_fallback(user_id: str, context: str, wardrobe_items: Dict) -> Dict[str, Any]:
    """
    Generate basic clothing combination using Phase 1 fallback logic when AI features are unavailable.
    Maintains service functionality even when intelligent engine initialization fails.
    
    Args:
        user_id: User identifier
        context: Occasion context for the combination
        wardrobe_items: Available wardrobe items
    
    Returns:
        Dictionary containing basic combination with simple compatibility analysis
    """
    try:
        logger.info(f"Generating basic combination fallback for {user_id}, context: {context}")
        
        # Filter wardrobe items based on the context using original Phase 1 logic
        filtered_wardrobe = filter_items_by_context_enhanced(context, wardrobe_items)
        
        # Generate the best combination for this context using enhanced Phase 1 logic
        combination = generate_style_appropriate_combination_enhanced(filtered_wardrobe, context)
        
        if not combination:
            raise HTTPException(
                status_code=404, 
                detail=f"Could not generate combination for context '{context}'. Insufficient wardrobe items."
            )
        
        # Create response with combination details (Phase 1 format but enhanced)
        return {
            "message": "Basic combination generated successfully (fallback mode)",
            "user_id": user_id,
            "context": context,
            "combination": combination,
            "generation_method": "enhanced_rule_based_fallback",
            "ai_analysis": {
                "confidence_level": combination.get('style_coherence', 'basic'),
                "overall_score": combination.get('compatibility_score', 0.5),
                "note": "AI features unavailable - using enhanced rule-based generation"
            },
            "recommendations": {
                "style_tips": [
                    f"This {combination.get('style_coherence', 'basic')} combination works for {context} occasions",
                    f"Color compatibility score: {combination.get('compatibility_score', 0.5):.1f}/1.0"
                ],
                "alternative_suggestions": "Consider accessories to enhance the look" if combination.get('compatibility_score', 0.5) < 0.8 else "Good combination!",
                "note": "Enhanced recommendations available with AI features enabled"
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Error in basic combination fallback: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Basic combination generation failed: {str(e)}"
        )

def filter_items_by_context_enhanced(context: str, wardrobe_items: Dict) -> Dict[str, List[Dict]]:
    """
    Enhanced version of context-based filtering with better style matching.
    Improves upon Phase 1 logic with more sophisticated filtering rules.
    
    Args:
        context: The occasion context (sport, work, casual, formal, party, date)
        wardrobe_items: Dictionary containing all available wardrobe items
    
    Returns:
        Dictionary containing filtered items by category with better context matching
    """
    # Create filtered wardrobe based on context with enhanced logic
    filtered_wardrobe = {"tops": [], "bottoms": [], "shoes": []}
    
    # Define context-specific style preferences (enhanced from Phase 1)
    context_style_map = {
        "work": ["formal", "smart_casual"],
        "formal": ["formal", "smart_casual"],
        "casual": ["casual", "smart_casual"],
        "party": ["formal", "smart_casual", "bohemian"],
        "sport": ["sporty", "casual"],
        "date": ["smart_casual", "casual", "bohemian"]
    }
    
    preferred_styles = context_style_map.get(context.lower(), ["casual", "smart_casual"])
    
    # Filter each category based on enhanced context appropriateness
    for category in ["tops", "bottoms", "shoes"]:
        for item in wardrobe_items.get(category, []):
            item_style = item.get("style", "casual")
            
            # Include items that match preferred styles for this context
            if item_style in preferred_styles:
                filtered_wardrobe[category].append(item)
            # Also include versatile casual items for most contexts
            elif item_style == "casual" and context.lower() not in ["formal", "work"]:
                filtered_wardrobe[category].append(item)
    
    return filtered_wardrobe

def generate_style_appropriate_combination_enhanced(filtered_wardrobe: Dict, context: str) -> Optional[Dict[str, Any]]:
    """
    Enhanced version of combination generation with better compatibility scoring.
    Improves upon Phase 1 logic with more sophisticated matching algorithms.
    
    Args:
        filtered_wardrobe: Dictionary of filtered clothing items
        context: The occasion context
    
    Returns:
        Dictionary containing the best combination with enhanced compatibility analysis
    """
    # Ensure we have items in each category
    if not all(filtered_wardrobe.get(category) for category in ["tops", "bottoms", "shoes"]):
        return None
    
    best_combination = None
    best_score = 0.0
    
    # Try multiple combinations and pick the best one (enhanced from Phase 1)
    for _ in range(30):  # Increased from 20 for better coverage
        # Randomly select one item from each category
        top = random.choice(filtered_wardrobe["tops"])
        bottom = random.choice(filtered_wardrobe["bottoms"])
        shoe = random.choice(filtered_wardrobe["shoes"])
        
        # Calculate enhanced compatibility score
        compatibility_score = check_color_compatibility_enhanced(top, bottom, shoe)
        
        # Add style coherence bonus (enhanced logic)
        style_bonus = calculate_style_coherence_bonus(top, bottom, shoe)
        compatibility_score = min(1.0, compatibility_score + style_bonus)
        
        # Add context appropriateness bonus
        context_bonus = calculate_context_bonus(top, bottom, shoe, context)
        compatibility_score = min(1.0, compatibility_score + context_bonus)
        
        # Keep track of the best combination
        if compatibility_score > best_score:
            best_score = compatibility_score
            best_combination = {
                "top": top,
                "bottom": bottom,
                "shoes": shoe,
                "compatibility_score": compatibility_score,
                "style_coherence": "high" if compatibility_score > 0.8 else "medium" if compatibility_score > 0.6 else "basic",
                "analysis_components": {
                    "color_compatibility": check_color_compatibility_enhanced(top, bottom, shoe),
                    "style_bonus": style_bonus,
                    "context_bonus": context_bonus
                }
            }
    
    return best_combination

def check_color_compatibility_enhanced(item1: Dict, item2: Dict, item3: Dict) -> float:
    """
    Enhanced color compatibility check with more sophisticated color theory.
    Improves upon Phase 1 logic with better color matching rules.
    
    Args:
        item1, item2, item3: Clothing items to check for color compatibility
    
    Returns:
        Float value representing compatibility score (0.0 to 1.0)
    """
    colors = [item1.get("color", "gray").lower(), item2.get("color", "gray").lower(), item3.get("color", "gray").lower()]
    
    # Perfect score for monochromatic (same color) combinations
    if len(set(colors)) == 1:
        return 1.0
    
    # Enhanced neutral color combinations
    neutral_colors = {"white", "black", "gray", "grey", "navy", "beige", "charcoal"}
    neutral_count = sum(1 for color in colors if color in neutral_colors)
    
    # Excellent score for combinations with 2+ neutral colors
    if neutral_count >= 2:
        return 0.95
    
    # Good score if at least one neutral color is present
    if neutral_count >= 1:
        return 0.8
    
    # Enhanced complementary color rules
    complementary_pairs = [
        ("blue", "white"), ("blue", "beige"), ("blue", "gray"),
        ("black", "white"), ("black", "beige"), ("black", "gray"),
        ("navy", "white"), ("navy", "beige"), ("navy", "khaki"),
        ("brown", "beige"), ("brown", "white"), ("brown", "navy"),
        ("red", "white"), ("red", "black"), ("red", "navy"),
        ("green", "white"), ("green", "black"), ("green", "beige")
    ]
    
    # Check for complementary color combinations
    pair_score = 0.0
    pair_count = 0
    
    for i, color1 in enumerate(colors):
        for j, color2 in enumerate(colors):
            if i != j:  # Don't compare color with itself
                if (color1, color2) in complementary_pairs or (color2, color1) in complementary_pairs:
                    pair_score += 0.8
                pair_count += 1
    
    if pair_count > 0:
        average_pair_score = pair_score / pair_count
        if average_pair_score > 0.6:
            return average_pair_score
    
    # Default compatibility score for other combinations
    return 0.5

def calculate_style_coherence_bonus(top: Dict, bottom: Dict, shoe: Dict) -> float:
    """
    Calculate bonus points for style coherence across items.
    Rewards combinations where all items share similar formality levels.
    
    Args:
        top, bottom, shoe: Clothing items with style information
    
    Returns:
        Float bonus score (0.0 to 0.2)
    """
    styles = [top.get("style", "casual"), bottom.get("style", "casual"), shoe.get("style", "casual")]
    
    # Bonus for matching styles
    if len(set(styles)) == 1:
        return 0.15  # Strong bonus for identical styles
    
    # Bonus for compatible style combinations
    compatible_combinations = [
        {"casual", "smart_casual"},
        {"smart_casual", "formal"},
        {"casual", "sporty"}
    ]
    
    style_set = set(styles)
    for compatible_set in compatible_combinations:
        if style_set.issubset(compatible_set):
            return 0.1  # Moderate bonus for compatible styles
    
    return 0.0  # No bonus for incompatible styles

def calculate_context_bonus(top: Dict, bottom: Dict, shoe: Dict, context: str) -> float:
    """
    Calculate bonus points for context appropriateness.
    Rewards combinations that are particularly well-suited for the given context.
    
    Args:
        top, bottom, shoe: Clothing items
        context: Occasion context
    
    Returns:
        Float bonus score (0.0 to 0.1)
    """
    # Get formality levels if available
    formalities = [
        top.get("formality", 0.5),
        bottom.get("formality", 0.5),
        shoe.get("formality", 0.5)
    ]
    avg_formality = sum(formalities) / len(formalities)
    
    # Context-specific formality targets
    context_formality_targets = {
        "work": 0.8,
        "formal": 0.9,
        "party": 0.7,
        "casual": 0.4,
        "sport": 0.2,
        "date": 0.6
    }
    
    target_formality = context_formality_targets.get(context.lower(), 0.5)
    
    # Calculate how close the combination is to target formality
    formality_difference = abs(avg_formality - target_formality)
    
    # Give bonus for combinations close to target formality
    if formality_difference < 0.1:
        return 0.1  # Perfect match
    elif formality_difference < 0.2:
        return 0.05  # Good match
    else:
        return 0.0  # No bonus