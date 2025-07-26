# Test file for the Style Profile Service
# Contains unit tests to verify profile management functionality

# Import pytest testing framework
import pytest
# Import FastAPI test client for API testing
from fastapi.testclient import TestClient
# Import JSON for test data manipulation
import json
# Import os for file operations in tests
import os
# Import the main FastAPI application
from main import app

# Create test client for making HTTP requests
client = TestClient(app)

def test_service_health():
    """
    Test the health check endpoint.
    Verifies that the service is running and responds correctly.
    """
    # Make GET request to health endpoint
    response = client.get("/")
    
    # Verify successful response
    assert response.status_code == 200
    
    # Verify response contains expected service information
    response_data = response.json()
    assert response_data["status"] == "Style Profile Service is running"
    assert response_data["service"] == "style_profile"

def test_get_profile_not_found():
    """
    Test retrieving a non-existent user profile.
    Should return 404 error when profile doesn't exist.
    """
    # Request profile for non-existent user
    response = client.get("/profile/nonexistent_user")
    
    # Verify 404 Not Found response
    assert response.status_code == 404

def test_update_profile_new_user():
    """
    Test updating profile for a new user.
    This should create a new profile and return success.
    """
    # Define test user ID
    test_user_id = "test_user_123"
    
    # Create update request with sample data
    update_data = {
        "garment_embeddings": [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]],
        "liked_items": ["item_001", "item_002"],
        "style_preferences": {"preferred_colors": ["blue", "green"]}
    }
    
    # Send update request
    response = client.post(f"/profile/{test_user_id}/update", json=update_data)
    
    # Verify successful update
    assert response.status_code == 200
    
    # Verify response contains expected fields
    response_data = response.json()
    assert response_data["user_id"] == test_user_id
    assert "updated_profile" in response_data
    
    # Clean up test data
    if os.path.exists("user_profiles.json"):
        os.remove("user_profiles.json")

def test_get_profile_existing_user():
    """
    Test retrieving an existing user profile.
    First creates a profile, then retrieves it.
    """
    # Define test user ID
    test_user_id = "test_user_456"
    
    # Create a profile first
    update_data = {
        "garment_embeddings": [[0.7, 0.8, 0.9]],
        "liked_items": ["item_003"]
    }
    
    # Update profile to create it
    client.post(f"/profile/{test_user_id}/update", json=update_data)
    
    # Now retrieve the profile
    response = client.get(f"/profile/{test_user_id}")
    
    # Verify successful retrieval
    assert response.status_code == 200
    
    # Verify response contains profile data
    response_data = response.json()
    assert response_data["user_id"] == test_user_id
    assert "profile" in response_data
    
    # Clean up test data
    if os.path.exists("user_profiles.json"):
        os.remove("user_profiles.json")

def test_placeholder():
    """
    Placeholder test that always passes.
    Ensures the test framework is working properly.
    """
    # Simple assertion that always succeeds
    assert True
