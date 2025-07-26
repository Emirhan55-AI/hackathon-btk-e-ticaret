# Test file for the Combination Engine Service
# Contains unit tests to verify combination generation functionality

# Import pytest testing framework
import pytest
# Import FastAPI test client for API endpoint testing
from fastapi.testclient import TestClient
# Import the main FastAPI application
from main import app

# Create test client for making HTTP requests to the application
client = TestClient(app)

def test_service_health():
    """
    Test the health check endpoint.
    Ensures the service is running and responding correctly.
    """
    # Send GET request to the health endpoint
    response = client.get("/")
    
    # Verify successful HTTP response
    assert response.status_code == 200
    
    # Verify response contains expected service information
    response_data = response.json()
    assert response_data["status"] == "Combination Engine Service is running"
    assert response_data["service"] == "combination_engine"

def test_generate_combination_valid_request():
    """
    Test generating a combination with valid request data.
    This verifies the core combination generation functionality.
    """
    # Create test request with required fields
    test_request = {
        "user_id": "test_user_123",
        "context": "casual",
        "occasion": "weekend"
    }
    
    # Send POST request to generate combination
    response = client.post("/generate_combination", json=test_request)
    
    # Verify successful response
    assert response.status_code == 200
    
    # Verify response structure contains expected fields
    response_data = response.json()
    assert "combination" in response_data
    assert "user_id" in response_data
    assert response_data["user_id"] == "test_user_123"
    assert "context" in response_data

def test_generate_combination_different_contexts():
    """
    Test combination generation for different contexts.
    Ensures the service can handle various occasions appropriately.
    """
    contexts = ["casual", "sport", "formal", "work"]
    
    for context in contexts:
        # Create request for each context
        test_request = {
            "user_id": f"test_user_{context}",
            "context": context
        }
        
        # Send request and verify successful response
        response = client.post("/generate_combination", json=test_request)
        assert response.status_code == 200
        
        # Verify context is properly handled
        response_data = response.json()
        assert response_data["context"] == context

def test_generate_combination_missing_user_id():
    """
    Test combination generation without user ID.
    Should return 400 error for missing required field.
    """
    # Create request without user_id
    test_request = {
        "context": "casual"
    }
    
    # Send request and expect validation error
    response = client.post("/generate_combination", json=test_request)
    assert response.status_code == 422  # Validation error

def test_placeholder():
    """
    Placeholder test that always passes.
    Verifies the test infrastructure is working correctly.
    """
    # Simple assertion that always succeeds
    assert True
