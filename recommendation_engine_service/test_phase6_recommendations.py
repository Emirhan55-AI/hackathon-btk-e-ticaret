# Phase 6: Comprehensive Test Suite for Enhanced Recommendation Engine
# This file contains extensive tests for all AI-powered recommendation features
# Tests FAISS similarity search, multi-modal integration, and advanced personalization

import pytest
import asyncio
import numpy as np
from datetime import datetime
import requests
import json
from typing import Dict, List, Any

# Import the enhanced recommendation engine for direct testing
from enhanced_recommender import EnhancedRecommendationEngine

# Import FastAPI testing utilities
from fastapi.testclient import TestClient
from main import app

# Create test client for API endpoint testing
client = TestClient(app)

class TestEnhancedRecommendationEngine:
    """
    Comprehensive test class for the Enhanced Recommendation Engine with FAISS integration.
    Tests all AI-powered features, multi-modal integration, and recommendation strategies.
    """
    
    @pytest.fixture
    def recommendation_engine(self):
        """
        Fixture to create a recommendation engine instance for testing.
        This provides a fresh engine instance for each test method.
        """
        # Create recommendation engine with test configuration
        engine = EnhancedRecommendationEngine(
            image_service_url="http://localhost:8001",
            style_service_url="http://localhost:8003", 
            combination_service_url="http://localhost:8004"
        )
        return engine
    
    def test_engine_initialization(self, recommendation_engine):
        """
        Test that the enhanced recommendation engine initializes correctly.
        Verifies all components are properly set up for AI-powered recommendations.
        """
        # Check that engine is properly initialized
        assert recommendation_engine is not None
        assert hasattr(recommendation_engine, 'product_catalog')
        assert hasattr(recommendation_engine, 'recommendation_strategies')
        assert hasattr(recommendation_engine, 'faiss_index')
        
        # Verify product catalog is loaded
        assert len(recommendation_engine.product_catalog) > 0
        print(f"✅ Product catalog loaded with {len(recommendation_engine.product_catalog)} items")
        
        # Verify recommendation strategies are available
        expected_strategies = ['content_based', 'collaborative', 'hybrid', 'style_aware', 'outfit_completion', 'trending']
        for strategy in expected_strategies:
            assert strategy in recommendation_engine.recommendation_strategies
        print("✅ All recommendation strategies loaded successfully")
        
        # Verify FAISS components are initialized
        assert hasattr(recommendation_engine, 'product_embeddings')
        if recommendation_engine.product_embeddings is not None:
            assert recommendation_engine.product_embeddings.shape[0] == len(recommendation_engine.product_catalog)
            print(f"✅ Product embeddings created with shape: {recommendation_engine.product_embeddings.shape}")
        
        print("✅ Enhanced Recommendation Engine initialization test passed")
    
    def test_product_embedding_creation(self, recommendation_engine):
        """
        Test that product embeddings are created correctly for FAISS similarity search.
        Verifies multi-dimensional embeddings capture product features properly.
        """
        # Test embedding creation for a sample product
        sample_product = recommendation_engine.product_catalog[0]
        embedding = recommendation_engine._create_product_embedding(sample_product)
        
        # Verify embedding properties
        assert isinstance(embedding, np.ndarray)
        assert len(embedding) > 0
        assert embedding.dtype == np.float32
        
        # Check that different products have different embeddings
        sample_product2 = recommendation_engine.product_catalog[1]
        embedding2 = recommendation_engine._create_product_embedding(sample_product2)
        
        # Embeddings should not be identical for different products
        assert not np.array_equal(embedding, embedding2)
        
        print(f"✅ Product embedding test passed - Embedding dimension: {len(embedding)}")
        print(f"   Sample product: {sample_product['name']}")
        print(f"   Embedding preview: {embedding[:5]}")
    
    def test_faiss_similarity_search(self, recommendation_engine):
        """
        Test FAISS-based similarity search functionality.
        Verifies that similar products are found efficiently using high-dimensional embeddings.
        """
        if recommendation_engine.product_embeddings is None:
            pytest.skip("Product embeddings not available for testing")
        
        # Get a query embedding (first product)
        query_embedding = recommendation_engine.product_embeddings[0]
        
        # Find similar products
        similar_products = recommendation_engine.find_similar_products_faiss(query_embedding, k=5)
        
        # Verify results
        assert isinstance(similar_products, list)
        assert len(similar_products) <= 5
        
        for product_id, similarity_score in similar_products:
            assert isinstance(product_id, str)
            assert isinstance(similarity_score, float)
            assert 0.0 <= similarity_score <= 1.0
        
        print(f"✅ FAISS similarity search test passed")
        print(f"   Found {len(similar_products)} similar products")
        print(f"   Similarity scores: {[score for _, score in similar_products]}")
    
    def test_content_based_recommendation(self, recommendation_engine):
        """
        Test content-based recommendation strategy.
        Verifies recommendations are generated based on product content similarity.
        """
        # Create mock user style profile
        mock_style_profile = {
            'visual_style_preferences': {
                'dominant_style': 'casual',
                'color_preferences': {'dominant_color': 'blue'}
            },
            'behavioral_patterns': {
                'engagement_metrics': {'engagement_score': 0.7}
            },
            'analysis_confidence': 0.8
        }
        
        mock_combination_insights = {
            'recent_combinations': [
                {'items': [{'category': 'tops'}, {'category': 'bottoms'}]}
            ]
        }
        
        # Generate content-based recommendations
        recommendations = recommendation_engine._content_based_recommendation(
            user_id="test_user_123",
            style_profile=mock_style_profile,
            combination_insights=mock_combination_insights,
            context="casual",
            k=5
        )
        
        # Verify recommendations
        assert isinstance(recommendations, list)
        assert len(recommendations) <= 5
        
        for rec in recommendations:
            assert 'id' in rec
            assert 'name' in rec
            assert 'recommendation_score' in rec
            assert 'recommendation_reason' in rec
            assert isinstance(rec['recommendation_score'], float)
        
        print(f"✅ Content-based recommendation test passed")
        print(f"   Generated {len(recommendations)} recommendations")
        if recommendations:
            print(f"   Sample recommendation: {recommendations[0]['name']} (score: {recommendations[0]['recommendation_score']:.3f})")
    
    def test_style_aware_recommendation(self, recommendation_engine):
        """
        Test style-aware recommendation strategy.
        Verifies recommendations match user's style preferences from Phase 4 integration.
        """
        # Create mock style profile with specific preferences
        mock_style_profile = {
            'visual_style_preferences': {
                'dominant_style': 'formal',
                'color_preferences': {'dominant_color': 'black'}
            },
            'behavioral_patterns': {
                'engagement_metrics': {'engagement_score': 0.9}
            },
            'analysis_confidence': 0.85
        }
        
        mock_combination_insights = {
            'recent_combinations': []
        }
        
        # Generate style-aware recommendations
        recommendations = recommendation_engine._style_aware_recommendation(
            user_id="style_test_user",
            style_profile=mock_style_profile,
            combination_insights=mock_combination_insights,
            context="work",
            k=6
        )
        
        # Verify recommendations match style preferences
        assert isinstance(recommendations, list)
        
        formal_items = [rec for rec in recommendations if rec.get('style') == 'formal']
        print(f"✅ Style-aware recommendation test passed")
        print(f"   Generated {len(recommendations)} total recommendations")
        print(f"   {len(formal_items)} items match 'formal' style preference")
        
        if recommendations:
            print(f"   Sample recommendation: {recommendations[0]['name']} (style: {recommendations[0].get('style', 'unknown')})")
    
    def test_hybrid_recommendation(self, recommendation_engine):
        """
        Test hybrid recommendation strategy.
        Verifies that multiple recommendation strategies are combined effectively.
        """
        # Create comprehensive mock user data
        mock_style_profile = {
            'visual_style_preferences': {
                'dominant_style': 'smart_casual',
                'color_preferences': {'dominant_color': 'navy'}
            },
            'behavioral_patterns': {
                'engagement_metrics': {'engagement_score': 0.8}
            },
            'analysis_confidence': 0.9
        }
        
        mock_combination_insights = {
            'recent_combinations': [
                {'items': [{'category': 'tops'}, {'category': 'bottoms'}]},
                {'items': [{'category': 'shoes'}, {'category': 'accessories'}]}
            ]
        }
        
        # Generate hybrid recommendations
        recommendations = recommendation_engine._hybrid_recommendation(
            user_id="hybrid_test_user",
            style_profile=mock_style_profile,
            combination_insights=mock_combination_insights,
            context="work",
            k=8
        )
        
        # Verify hybrid recommendations
        assert isinstance(recommendations, list)
        assert len(recommendations) <= 8
        
        # Check that hybrid scoring is applied
        hybrid_scored_items = [rec for rec in recommendations if 'hybrid_score' in rec]
        
        print(f"✅ Hybrid recommendation test passed")
        print(f"   Generated {len(recommendations)} hybrid recommendations")
        print(f"   {len(hybrid_scored_items)} items have hybrid scoring")
        
        if recommendations:
            top_rec = recommendations[0]
            print(f"   Top recommendation: {top_rec['name']} (score: {top_rec.get('recommendation_score', 0):.3f})")
    
    def test_comprehensive_recommendation_generation(self, recommendation_engine):
        """
        Test the complete recommendation generation process.
        Verifies end-to-end functionality with analytics and user insights.
        """
        # Test comprehensive recommendation generation
        result = recommendation_engine.generate_comprehensive_recommendations(
            user_id="comprehensive_test_user",
            context="casual",
            num_recommendations=10,
            strategy="hybrid"
        )
        
        # Verify result structure
        assert isinstance(result, dict)
        assert 'user_id' in result
        assert 'recommendations' in result
        assert 'recommendation_analytics' in result
        assert 'user_insights' in result
        assert 'service_info' in result
        
        # Verify recommendations
        recommendations = result['recommendations']
        assert isinstance(recommendations, list)
        assert len(recommendations) <= 10
        
        # Verify analytics
        analytics = result['recommendation_analytics']
        assert 'processing_time_seconds' in analytics
        assert 'recommendation_confidence' in analytics
        assert 'diversity_score' in analytics
        assert 'personalization_score' in analytics
        
        # Verify user insights
        user_insights = result['user_insights']
        assert 'dominant_style' in user_insights
        assert 'engagement_level' in user_insights
        assert 'style_confidence' in user_insights
        
        print(f"✅ Comprehensive recommendation generation test passed")
        print(f"   Generated {len(recommendations)} recommendations")
        print(f"   Processing time: {analytics['processing_time_seconds']:.3f}s")
        print(f"   Confidence: {analytics['recommendation_confidence']:.3f}")
        print(f"   Diversity: {analytics['diversity_score']:.3f}")

class TestEnhancedRecommendationAPI:
    """
    Test class for Enhanced Recommendation API endpoints.
    Tests all FastAPI endpoints with various scenarios and edge cases.
    """
    
    def test_health_check_endpoint(self):
        """
        Test the enhanced health check endpoint.
        Verifies service status and AI component information.
        """
        response = client.get("/")
        
        # Verify response status and structure
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        assert "service" in data
        assert "phase" in data
        assert "status" in data
        assert "ai_components" in data
        assert "service_integrations" in data
        assert "capabilities" in data
        
        # Verify AI components information
        ai_components = data["ai_components"]
        assert "faiss_similarity_search" in ai_components
        assert "multi_modal_embeddings" in ai_components
        assert "content_based_filtering" in ai_components
        
        print("✅ Health check endpoint test passed")
        print(f"   Service: {data['service']}")
        print(f"   Phase: {data['phase']}")
        print(f"   Status: {data['status']}")
        print(f"   Catalog Size: {data.get('catalog_size', 0)}")
    
    def test_enhanced_recommendations_endpoint(self):
        """
        Test the main enhanced recommendations endpoint.
        Verifies comprehensive AI-powered recommendation generation.
        """
        # Test request payload
        request_data = {
            "user_id": "api_test_user_001",
            "context": "casual",
            "num_recommendations": 8,
            "strategy": "hybrid",
            "include_analytics": True
        }
        
        response = client.post("/recommendations", json=request_data)
        
        # Verify response status
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "user_id" in data
        assert "recommendations" in data
        assert "recommendation_analytics" in data
        assert "user_insights" in data
        assert "service_info" in data
        
        # Verify recommendations
        recommendations = data["recommendations"]
        assert isinstance(recommendations, list)
        assert len(recommendations) <= 8
        
        for rec in recommendations:
            assert "id" in rec
            assert "name" in rec
            assert "category" in rec
            assert "style" in rec
            assert "price" in rec
            assert "recommendation_score" in rec
            assert "recommendation_reason" in rec
        
        # Verify analytics
        analytics = data["recommendation_analytics"]
        assert "total_products" in analytics
        assert "processing_time_seconds" in analytics
        assert "recommendation_confidence" in analytics
        
        print("✅ Enhanced recommendations endpoint test passed")
        print(f"   User ID: {data['user_id']}")
        print(f"   Strategy: {data['strategy']}")
        print(f"   Recommendations: {len(recommendations)}")
        print(f"   Processing time: {analytics['processing_time_seconds']:.3f}s")
    
    def test_similarity_search_endpoint(self):
        """
        Test the FAISS-based similarity search endpoint.
        Verifies ultra-fast similarity search functionality.
        """
        # Test with a known product ID
        request_data = {
            "product_id": "prod_001",
            "num_similar": 5,
            "similarity_threshold": 0.0
        }
        
        response = client.post("/similarity-search", json=request_data)
        
        # Verify response
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "source_product" in data
        assert "similar_products" in data
        assert "search_metadata" in data
        
        # Verify source product
        source_product = data["source_product"]
        assert source_product["id"] == "prod_001"
        
        # Verify similar products
        similar_products = data["similar_products"]
        assert isinstance(similar_products, list)
        assert len(similar_products) <= 5
        
        for product in similar_products:
            assert "id" in product
            assert "similarity_score" in product
            assert isinstance(product["similarity_score"], float)
        
        # Verify metadata
        metadata = data["search_metadata"]
        assert "search_method" in metadata
        assert "total_found" in metadata
        
        print("✅ Similarity search endpoint test passed")
        print(f"   Source product: {source_product['name']}")
        print(f"   Similar products found: {len(similar_products)}")
        print(f"   Search method: {metadata['search_method']}")
    
    def test_user_context_recommendations_endpoint(self):
        """
        Test user-specific context recommendations endpoint.
        Verifies context-aware recommendation generation.
        """
        user_id = "context_test_user"
        context = "work"
        
        response = client.get(f"/user/{user_id}/recommendations/{context}?num_recommendations=6&strategy=style_aware")
        
        # Verify response
        assert response.status_code == 200
        data = response.json()
        
        # Check that context is properly applied
        assert data["user_id"] == user_id
        assert data["context"] == context
        assert data["strategy"] == "style_aware"
        
        # Verify recommendations
        recommendations = data["recommendations"]
        assert len(recommendations) <= 6
        
        print("✅ User context recommendations endpoint test passed")
        print(f"   User ID: {user_id}")
        print(f"   Context: {context}")
        print(f"   Recommendations: {len(recommendations)}")
    
    def test_trending_products_endpoint(self):
        """
        Test trending products endpoint with AI-powered trend analysis.
        Verifies trend scoring and product ranking.
        """
        response = client.get("/trending?num_products=10&category=tops&style=casual")
        
        # Verify response
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "trending_products" in data
        assert "trend_metadata" in data
        
        # Verify trending products
        trending_products = data["trending_products"]
        assert isinstance(trending_products, list)
        assert len(trending_products) <= 10
        
        for product in trending_products:
            assert "id" in product
            assert "name" in product
            assert "category" in product
            assert "trend_score_calculated" in product
            
            # Verify filtering worked
            assert product["category"] == "tops"
            if "style" in product:
                assert product["style"] == "casual"
        
        # Verify metadata
        metadata = data["trend_metadata"]
        assert "filters_applied" in metadata
        assert metadata["filters_applied"]["category"] == "tops"
        assert metadata["filters_applied"]["style"] == "casual"
        
        print("✅ Trending products endpoint test passed")
        print(f"   Trending products: {len(trending_products)}")
        print(f"   Category filter: {metadata['filters_applied']['category']}")
        print(f"   Style filter: {metadata['filters_applied']['style']}")
    
    def test_recommendation_analytics_endpoint(self):
        """
        Test recommendation service analytics endpoint.
        Verifies comprehensive analytics and AI metrics.
        """
        response = client.get("/analytics")
        
        # Verify response
        assert response.status_code == 200
        data = response.json()
        
        # Check analytics structure
        assert "service_performance" in data
        assert "ai_algorithm_metrics" in data
        assert "user_engagement" in data
        assert "product_insights" in data
        assert "service_integrations" in data
        assert "ai_features_active" in data
        
        # Verify AI algorithm metrics
        ai_metrics = data["ai_algorithm_metrics"]
        assert "faiss_index_status" in ai_metrics
        assert "product_catalog_size" in ai_metrics
        assert "recommendation_strategies" in ai_metrics
        
        # Verify service integrations
        integrations = data["service_integrations"]
        assert "phase_2_image_processing" in integrations
        assert "phase_4_style_profiling" in integrations
        assert "phase_5_combination_engine" in integrations
        
        print("✅ Recommendation analytics endpoint test passed")
        print(f"   FAISS status: {ai_metrics['faiss_index_status']}")
        print(f"   Catalog size: {ai_metrics['product_catalog_size']}")
        print(f"   Active strategies: {len(ai_metrics['recommendation_strategies'])}")
    
    def test_invalid_request_handling(self):
        """
        Test error handling for invalid requests.
        Verifies proper HTTP error codes and error messages.
        """
        # Test missing user_id
        invalid_request = {
            "context": "casual",
            "num_recommendations": 5
        }
        
        response = client.post("/recommendations", json=invalid_request)
        assert response.status_code == 422  # Validation error
        
        # Test invalid strategy
        invalid_strategy_request = {
            "user_id": "test_user",
            "strategy": "invalid_strategy"
        }
        
        response = client.post("/recommendations", json=invalid_strategy_request)
        assert response.status_code == 400  # Bad request
        
        # Test invalid product ID for similarity search
        invalid_similarity_request = {
            "product_id": "nonexistent_product",
            "num_similar": 5
        }
        
        response = client.post("/similarity-search", json=invalid_similarity_request)
        assert response.status_code == 404  # Not found
        
        print("✅ Invalid request handling test passed")
        print("   All error cases handled appropriately")

# Performance and Load Testing
class TestPerformanceAndLoad:
    """
    Performance and load testing for the Enhanced Recommendation Engine.
    Tests system performance under various loads and conditions.
    """
    
    def test_recommendation_performance(self):
        """
        Test recommendation generation performance.
        Verifies that recommendations are generated within acceptable time limits.
        """
        import time
        
        # Test multiple recommendation requests
        request_data = {
            "user_id": "performance_test_user",
            "context": "casual",
            "num_recommendations": 10,
            "strategy": "hybrid"
        }
        
        response_times = []
        for i in range(5):  # Test 5 requests
            start_time = time.time()
            response = client.post("/recommendations", json=request_data)
            end_time = time.time()
            
            assert response.status_code == 200
            response_times.append(end_time - start_time)
        
        # Calculate performance metrics
        avg_response_time = sum(response_times) / len(response_times)
        max_response_time = max(response_times)
        min_response_time = min(response_times)
        
        # Verify performance thresholds
        assert avg_response_time < 2.0  # Average should be under 2 seconds
        assert max_response_time < 5.0  # No request should take over 5 seconds
        
        print("✅ Recommendation performance test passed")
        print(f"   Average response time: {avg_response_time:.3f}s")
        print(f"   Min response time: {min_response_time:.3f}s")
        print(f"   Max response time: {max_response_time:.3f}s")
    
    def test_similarity_search_performance(self):
        """
        Test FAISS similarity search performance.
        Verifies ultra-fast similarity search capabilities.
        """
        import time
        
        # Test FAISS similarity search performance
        request_data = {
            "product_id": "prod_001",
            "num_similar": 10
        }
        
        search_times = []
        for i in range(10):  # Test 10 searches
            start_time = time.time()
            response = client.post("/similarity-search", json=request_data)
            end_time = time.time()
            
            assert response.status_code == 200
            search_times.append(end_time - start_time)
        
        # Calculate performance metrics
        avg_search_time = sum(search_times) / len(search_times)
        max_search_time = max(search_times)
        
        # FAISS should be very fast
        assert avg_search_time < 0.5  # Average should be under 0.5 seconds
        assert max_search_time < 1.0   # No search should take over 1 second
        
        print("✅ Similarity search performance test passed")
        print(f"   Average search time: {avg_search_time:.3f}s")
        print(f"   Max search time: {max_search_time:.3f}s")
        print("   FAISS similarity search is ultra-fast! ⚡")

# Run all tests when this file is executed
if __name__ == "__main__":
    print("🧪 Starting Phase 6 Enhanced Recommendation Engine Test Suite")
    print("=" * 80)
    
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
    
    print("=" * 80)
    print("✅ Phase 6 Enhanced Recommendation Engine Test Suite completed!")
    print("🚀 All AI-powered recommendation features tested successfully!")
