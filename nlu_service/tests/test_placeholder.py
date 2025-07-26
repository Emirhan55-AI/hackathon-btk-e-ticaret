# Test file for the Natural Language Understanding Service
# Contains unit tests to verify NLU functionality and API endpoints

# Import pytest testing framework
import pytest
# Import FastAPI test client for API endpoint testing
from fastapi.testclient import TestClient
# Import the main FastAPI application
from main import app

# Create a test client for making HTTP requests to the application
client = TestClient(app)

def test_service_health():
    """
    Test the health check endpoint to verify service is running.
    This ensures the basic API functionality works correctly.
    """
    # Send GET request to the root health check endpoint
    response = client.get("/")
    
    # Verify the HTTP response status is 200 (OK)
    assert response.status_code == 200
    
    # Verify the response contains expected service information
    response_data = response.json()
    assert response_data["status"] == "NLU Service is running"
    assert response_data["service"] == "nlu"

def test_parse_request_valid_text():
    """
    Test the parse_request endpoint with valid text input.
    This verifies that the NLU service can process text and return analysis.
    """
    # Create a test request with sample text
    test_request = {"text": "I want sporty sneakers today"}
    
    # Send POST request to the parse_request endpoint
    response = client.post("/parse_request", json=test_request)
    
    # Verify the response is successful
    assert response.status_code == 200
    
    # Verify the response structure contains expected fields
    response_data = response.json()
    assert "analysis" in response_data
    assert "intent" in response_data["analysis"]
    assert "sentiment" in response_data["analysis"]
    assert "context" in response_data["analysis"]

def test_parse_request_empty_text():
    """
    Test the parse_request endpoint with empty text.
    This should return a 400 error for invalid input.
    """
    # Create request with empty text
    test_request = {"text": ""}
    
    # Send POST request with empty text
    response = client.post("/parse_request", json=test_request)
    
    # Verify that a 400 Bad Request error is returned
    assert response.status_code == 400

def test_placeholder():
    """
    Placeholder test that always passes.
    Used to verify the test infrastructure is working correctly.
    """
    # Simple assertion that always passes
    assert True
