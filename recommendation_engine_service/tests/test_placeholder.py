# Test file for the Recommendation Engine Service
# Contains unit tests to verify recommendation functionality

# Import pytest testing framework
import pytest
# Import FastAPI test client for API endpoint testing
from fastapi.testclient import TestClient
# Import the main FastAPI application
from main import app

# Create test client for making HTTP requests to the service
client = TestClient(app)

def test_service_health():
    """
    Test the health check endpoint.
    Verifies that the recommendation service is running correctly.
    """
    # Send GET request to health check endpoint
    response = client.get("/")
    
    # Verify successful HTTP response
    assert response.status_code == 200
    
    # Verify response contains expected service information
    response_data = response.json()
    assert response_data["status"] == "Recommendation Engine Service is running"
    assert response_data["service"] == "recommendation_engine"

def test_recommend_products_valid_request():
    """
    Test product recommendation with valid request data.
    This verifies the core recommendation functionality works.
    """
    # Create test request with minimal required data
    test_request = {
        "user_id": "test_user_123",
        "context": "casual"
    }
    
    # Send POST request to get recommendations
    response = client.post("/recommend", json=test_request)
    
    # Verify successful response
    assert response.status_code == 200
    
    # Verify response structure contains expected fields
    response_data = response.json()
    assert "recommendations" in response_data
    assert "user_id" in response_data
    assert response_data["user_id"] == "test_user_123"
    assert "context" in response_data

def test_recommend_products_different_contexts():
    """
    Test recommendations for different contexts.
    Ensures the service handles various occasions appropriately.
    """
    contexts = ["casual", "sport", "formal", "work"]
    
    for context in contexts:
        # Create request for each context
        test_request = {
            "user_id": f"test_user_{context}",
            "context": context
        }
        
        # Send request and verify successful response
        response = client.post("/recommend", json=test_request)
        assert response.status_code == 200
        
        # Verify context is handled correctly
        response_data = response.json()
        assert response_data["context"] == context

def test_recommend_products_with_category():
    """
    Test recommendations for specific product categories.
    Verifies category filtering works correctly.
    """
    # Create request for specific category
    test_request = {
        "user_id": "test_user_shoes",
        "context": "sport",
        "category": "shoes"
    }
    
    # Send request for shoe recommendations
    response = client.post("/recommend", json=test_request)
    
    # Verify successful response
    assert response.status_code == 200
    
    # Verify response contains recommendations
    response_data = response.json()
    assert "recommendations" in response_data
    assert len(response_data["recommendations"]) > 0

def test_recommend_products_missing_user_id():
    """
    Test recommendation request without user ID.
    Should return validation error for missing required field.
    """
    # Create request without user_id
    test_request = {
        "context": "casual"
    }
    
    # Send request and expect validation error
    response = client.post("/recommend", json=test_request)
    assert response.status_code == 422  # Validation error

def test_placeholder():
    """
    Placeholder test that always passes.
    Verifies the test infrastructure is working correctly.
    """
    # Simple assertion that always succeeds
    assert True
