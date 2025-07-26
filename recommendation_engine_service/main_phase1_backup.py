# Import FastAPI framework for REST API development
from fastapi import FastAPI, HTTPException
# Import Pydantic for data validation and serialization
from pydantic import BaseModel
# Import typing utilities for type hints
from typing import List, Optional, Dict, Any
# Import math for similarity calculations
import math
# Import random for mock data generation
import random

# Create the main FastAPI application instance
# This service provides product recommendations from e-commerce sources
app = FastAPI(
    title="Aura Recommendation Engine Service",  # Service name for API documentation
    description="Provides personalized product recommendations based on user style and preferences",  # Service description
    version="1.0.0"  # API version for compatibility tracking
)

# Pydantic model for recommendation requests
# Defines the structure of data needed to generate recommendations
class RecommendationRequest(BaseModel):
    user_id: str  # Unique identifier for the user
    style_profile: Optional[Dict[str, Any]] = None  # User's style profile with preferences
    context: Optional[str] = "general"  # Context for recommendations (sport, work, casual)
    category: Optional[str] = None  # Specific category to recommend (shoes, tops, etc.)
    budget_range: Optional[Dict[str, float]] = None  # Min/max price range
    preferences: Optional[Dict[str, Any]] = None  # Additional user preferences

# Mock e-commerce product database
# In production, this would connect to real e-commerce APIs or databases
MOCK_PRODUCTS = [
    # Casual wear products
    {"id": "prod_001", "name": "Classic Cotton T-Shirt", "category": "tops", "style": "casual", 
     "color": "white", "price": 25.99, "brand": "BasicWear", "embedding": [0.1, 0.3, 0.5, 0.2, 0.4]},
    {"id": "prod_002", "name": "Relaxed Fit Jeans", "category": "bottoms", "style": "casual", 
     "color": "blue", "price": 89.99, "brand": "DenimCo", "embedding": [0.2, 0.4, 0.3, 0.5, 0.1]},
    {"id": "prod_003", "name": "Canvas Sneakers", "category": "shoes", "style": "casual", 
     "color": "white", "price": 65.99, "brand": "ComfortFeet", "embedding": [0.3, 0.2, 0.4, 0.1, 0.5]},
    
    # Sports wear products
    {"id": "prod_004", "name": "Athletic Performance Shirt", "category": "tops", "style": "sport", 
     "color": "navy", "price": 45.99, "brand": "SportMax", "embedding": [0.4, 0.1, 0.2, 0.5, 0.3]},
    {"id": "prod_005", "name": "Training Shorts", "category": "bottoms", "style": "sport", 
     "color": "black", "price": 35.99, "brand": "FitGear", "embedding": [0.5, 0.3, 0.1, 0.4, 0.2]},
    {"id": "prod_006", "name": "Running Shoes", "category": "shoes", "style": "sport", 
     "color": "gray", "price": 129.99, "brand": "RunFast", "embedding": [0.1, 0.5, 0.3, 0.2, 0.4]},
    
    # Formal wear products
    {"id": "prod_007", "name": "Business Dress Shirt", "category": "tops", "style": "formal", 
     "color": "white", "price": 79.99, "brand": "Professional", "embedding": [0.2, 0.1, 0.5, 0.3, 0.4]},
    {"id": "prod_008", "name": "Tailored Trousers", "category": "bottoms", "style": "formal", 
     "color": "charcoal", "price": 149.99, "brand": "Elegant", "embedding": [0.3, 0.4, 0.2, 0.1, 0.5]},
    {"id": "prod_009", "name": "Oxford Dress Shoes", "category": "shoes", "style": "formal", 
     "color": "black", "price": 199.99, "brand": "ClassicStep", "embedding": [0.4, 0.2, 0.1, 0.5, 0.3]},
    
    # Accessories and additional items
    {"id": "prod_010", "name": "Casual Blazer", "category": "outerwear", "style": "casual", 
     "color": "navy", "price": 159.99, "brand": "StyleMix", "embedding": [0.5, 0.1, 0.4, 0.2, 0.3]},
]

def calculate_cosine_similarity(vec1, vec2):
    """
    Calculate cosine similarity between two vectors.
    This measures how similar two items are based on their feature embeddings.
    
    Args:
        vec1, vec2: Lists representing feature vectors for comparison
    
    Returns:
        Float value between -1 and 1, where 1 means identical, 0 means orthogonal
    """
    # Calculate dot product of the two vectors
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    
    # Calculate magnitude (length) of each vector
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))
    
    # Avoid division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    
    # Return cosine similarity
    return dot_product / (magnitude1 * magnitude2)

def filter_products_by_context(context, category=None):
    """
    Filter products based on context and optionally by category.
    This ensures recommendations are appropriate for the user's needs.
    
    Args:
        context: The context for recommendations (sport, work, casual, formal)
        category: Optional specific category to filter by
    
    Returns:
        List of filtered products matching the criteria
    """
    filtered_products = []
    
    for product in MOCK_PRODUCTS:
        # Check if product matches the style context
        style_match = (
            product["style"] == context or 
            (context == "work" and product["style"] == "formal") or
            (context == "general" and product["style"] in ["casual", "formal"])
        )
        
        # Check if product matches the category (if specified)
        category_match = category is None or product["category"] == category
        
        # Include product if both criteria are met
        if style_match and category_match:
            filtered_products.append(product)
    
    return filtered_products

def detect_missing_categories(user_profile):
    """
    Analyze user's style profile to detect missing clothing categories.
    This helps suggest items the user might need to complete their wardrobe.
    
    Args:
        user_profile: Dictionary containing user's style and wardrobe information
    
    Returns:
        List of categories that appear to be missing or underrepresented
    """
    # Basic categories that most users should have
    essential_categories = ["tops", "bottoms", "shoes", "outerwear"]
    missing_categories = []
    
    # Check if user profile contains wardrobe information
    if not user_profile or "wardrobe_categories" not in user_profile:
        # If no wardrobe info, suggest starting with basics
        return ["tops", "bottoms", "shoes"]
    
    # Check which essential categories are missing or have few items
    wardrobe_categories = user_profile.get("wardrobe_categories", {})
    
    for category in essential_categories:
        item_count = wardrobe_categories.get(category, 0)
        
        # Consider category missing if user has fewer than 2 items
        if item_count < 2:
            missing_categories.append(category)
    
    return missing_categories

def generate_recommendations(user_profile, context, category=None, limit=5):
    """
    Generate product recommendations based on user profile and context.
    Uses similarity matching and category analysis to suggest relevant items.
    
    Args:
        user_profile: User's style profile with preferences and history
        context: Context for recommendations
        category: Optional specific category to focus on
        limit: Maximum number of recommendations to return
    
    Returns:
        List of recommended products with similarity scores
    """
    # Filter products based on context and category
    candidate_products = filter_products_by_context(context, category)
    
    if not candidate_products:
        return []
    
    # If user has no style profile, return popular items for the context
    if not user_profile or "style_vector" not in user_profile:
        # Return a random selection of products for the context
        recommendations = random.sample(candidate_products, min(limit, len(candidate_products)))
        return [{"product": prod, "similarity_score": 0.5, "reason": "Popular item for context"} 
                for prod in recommendations]
    
    # Calculate similarity between user's style and each product
    user_style_vector = user_profile["style_vector"]
    product_similarities = []
    
    for product in candidate_products:
        # Calculate how well the product matches user's style
        similarity = calculate_cosine_similarity(user_style_vector, product["embedding"])
        
        product_similarities.append({
            "product": product,
            "similarity_score": similarity,
            "reason": f"Matches your style preferences (similarity: {similarity:.2f})"
        })
    
    # Sort by similarity score (highest first) and return top recommendations
    product_similarities.sort(key=lambda x: x["similarity_score"], reverse=True)
    
    return product_similarities[:limit]

# Root endpoint for health monitoring
@app.get("/")
async def health_check():
    """
    Health check endpoint to verify service availability.
    Used by monitoring systems and load balancers.
    """
    return {"status": "Recommendation Engine Service is running", "service": "recommendation_engine"}

# Main endpoint for generating product recommendations
@app.post("/recommend")
async def recommend_products(request: RecommendationRequest):
    """
    Generate personalized product recommendations for a user.
    
    Args:
        request: RecommendationRequest containing user profile and preferences
    
    Returns:
        JSON response with recommended products and reasoning
    """
    # Validate that user_id is provided
    if not request.user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    # Use provided context or default to general
    context = request.context or "general"
    
    # Generate recommendations based on user profile and context
    recommendations = generate_recommendations(
        user_profile=request.style_profile,
        context=context,
        category=request.category,
        limit=5
    )
    
    # Detect missing categories in user's wardrobe
    missing_categories = detect_missing_categories(request.style_profile) if request.style_profile else ["tops", "bottoms", "shoes"]
    
    # If no recommendations found, return helpful message
    if not recommendations:
        raise HTTPException(
            status_code=404,
            detail=f"No suitable products found for context '{context}'" + 
                   (f" and category '{request.category}'" if request.category else "")
        )
    
    # Prepare response with recommendations and insights
    return {
        "message": "Recommendations generated successfully",
        "user_id": request.user_id,
        "context": context,
        "recommendations": recommendations,
        "wardrobe_analysis": {
            "missing_categories": missing_categories,
            "suggestion": f"Consider adding items from: {', '.join(missing_categories)}" if missing_categories else "Your wardrobe looks well-rounded!"
        },
        "recommendation_method": "cosine_similarity_placeholder",  # Indicates Phase 1 implementation
        "total_products_considered": len(MOCK_PRODUCTS),
        "filters_applied": {
            "context": context,
            "category": request.category,
            "budget_considered": bool(request.budget_range)
        }
    }
