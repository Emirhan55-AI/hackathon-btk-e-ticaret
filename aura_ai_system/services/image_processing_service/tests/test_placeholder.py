# Advanced Test file for the Image Processing Service (Phase 2)
# This file contains comprehensive unit tests for AI-powered image analysis

# Import pytest testing framework
import pytest
# Import FastAPI test client for API endpoint testing
from fastapi.testclient import TestClient
# Import IO operations for creating test images
import io
# Import PIL for creating test images
from PIL import Image
# Import the main FastAPI application
from main import app

# Create a test client for making HTTP requests to the application
client = TestClient(app)

def create_test_image(width=224, height=224, color=(255, 0, 0)):
    """
    Create a test image for upload testing.
    This generates a simple colored image that can be used for testing the analysis endpoints.
    
    Args:
        width: Image width in pixels
        height: Image height in pixels  
        color: RGB color tuple
        
    Returns:
        BytesIO object containing PNG image data
    """
    # Create a new RGB image with the specified dimensions and color
    image = Image.new('RGB', (width, height), color)
    
    # Save the image to a BytesIO buffer in PNG format
    image_buffer = io.BytesIO()
    image.save(image_buffer, format='PNG')
    image_buffer.seek(0)  # Reset buffer position to beginning
    
    return image_buffer

def test_service_health():
    """
    Test the health check endpoint to ensure the service is running.
    This verifies basic API functionality and service status.
    """
    # Make a GET request to the root endpoint
    response = client.get("/")
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Assert that the response contains the expected status message
    response_data = response.json()
    assert response_data["status"] == "Image Processing Service is running"
    assert response_data["service"] == "image_processing"
    assert response_data["version"] == "2.0.0"
    
    # Verify that AI status information is included
    assert "ai_status" in response_data
    assert "capabilities" in response_data
    
    # Check that the service advertises its AI capabilities
    capabilities = response_data["capabilities"]
    expected_capabilities = [
        "clothing_detection", "style_analysis", "color_analysis", 
        "pattern_recognition", "feature_extraction", "clip_embeddings"
    ]
    for capability in expected_capabilities:
        assert capability in capabilities

def test_analyze_image_with_valid_png():
    """
    Test the analyze_image endpoint with a valid PNG image.
    This verifies that the service can process image uploads correctly.
    """
    # Create a test PNG image
    test_image = create_test_image(224, 224, (0, 255, 0))  # Green image
    
    # Prepare the file upload
    files = {"file": ("test_image.png", test_image, "image/png")}
    
    # Send POST request to analyze the image
    response = client.post("/analyze_image", files=files)
    
    # Verify successful response
    assert response.status_code == 200
    
    # Verify response structure contains expected fields
    response_data = response.json()
    assert "message" in response_data
    assert "filename" in response_data
    assert response_data["filename"] == "test_image.png"
    assert "analysis_results" in response_data
    assert "processing_method" in response_data
    
    # Verify analysis results structure
    analysis = response_data["analysis_results"]
    assert "detected_items" in analysis
    assert "style_analysis" in analysis
    assert "color_analysis" in analysis
    assert "pattern_analysis" in analysis
    
    # If AI models are loaded, verify advanced features
    if response_data["processing_method"] == "ai_powered_analysis":
        assert "features" in analysis
        assert "model_info" in response_data
        # Verify that feature embeddings are present
        features = analysis["features"]
        assert "resnet_features" in features or "vit_features" in features or "clip_embedding" in features

def test_analyze_image_with_valid_jpeg():
    """
    Test the analyze_image endpoint with a valid JPEG image.
    This ensures the service handles different image formats correctly.
    """
    # Create a test JPEG image
    test_image = create_test_image(300, 200, (0, 0, 255))  # Blue image
    
    # Convert to JPEG format
    jpeg_buffer = io.BytesIO()
    image = Image.open(test_image)
    image.save(jpeg_buffer, format='JPEG')
    jpeg_buffer.seek(0)
    
    # Prepare the file upload
    files = {"file": ("test_image.jpg", jpeg_buffer, "image/jpeg")}
    
    # Send POST request to analyze the image
    response = client.post("/analyze_image", files=files)
    
    # Verify successful response
    assert response.status_code == 200
    
    # Verify that the service handled JPEG format correctly
    response_data = response.json()
    assert response_data["filename"] == "test_image.jpg"
    assert response_data["content_type"] == "image/jpeg"

def test_analyze_image_different_dimensions():
    """
    Test image analysis with different image dimensions.
    This verifies that the service can handle various image sizes.
    """
    # Test with different image dimensions
    test_cases = [
        (100, 100),   # Small square image
        (512, 256),   # Rectangular image
        (1024, 768),  # Large image
    ]
    
    for width, height in test_cases:
        # Create test image with specific dimensions
        test_image = create_test_image(width, height, (128, 128, 128))  # Gray image
        
        # Prepare file upload
        files = {"file": (f"test_{width}x{height}.png", test_image, "image/png")}
        
        # Send analysis request
        response = client.post("/analyze_image", files=files)
        
        # Verify successful processing
        assert response.status_code == 200
        
        # Verify that dimensions are correctly reported
        response_data = response.json()
        assert response_data["image_dimensions"]["width"] == width
        assert response_data["image_dimensions"]["height"] == height

def test_analyze_image_no_file():
    """
    Test the analyze_image endpoint when no file is uploaded.
    This should return a 422 error (Unprocessable Entity).
    """
    # Make a POST request without uploading a file
    response = client.post("/analyze_image")
    
    # Assert that the response status code is 422 (validation error)
    assert response.status_code == 422

def test_analyze_image_invalid_file_type():
    """
    Test the analyze_image endpoint with a non-image file.
    This should return a 400 error for invalid file type.
    """
    # Create a text file instead of an image
    text_content = b"This is not an image file"
    text_buffer = io.BytesIO(text_content)
    
    # Prepare the file upload with text content
    files = {"file": ("test.txt", text_buffer, "text/plain")}
    
    # Send POST request with non-image file
    response = client.post("/analyze_image", files=files)
    
    # Assert that a 400 Bad Request error is returned
    assert response.status_code == 400
    
    # Verify error message mentions file type requirement
    response_data = response.json()
    assert "must be an image" in response_data["detail"].lower()

def test_analyze_image_corrupted_image():
    """
    Test the analyze_image endpoint with corrupted image data.
    This verifies proper error handling for invalid image files.
    """
    # Create corrupted image data (random bytes with image mime type)
    corrupted_data = b"fake_image_data_that_cannot_be_parsed"
    corrupted_buffer = io.BytesIO(corrupted_data)
    
    # Prepare the file upload with corrupted data but image mime type
    files = {"file": ("corrupted.png", corrupted_buffer, "image/png")}
    
    # Send POST request with corrupted image
    response = client.post("/analyze_image", files=files)
    
    # Should return 500 error for processing failure
    assert response.status_code == 500
    
    # Verify error message indicates processing failure
    response_data = response.json()
    assert "error processing image" in response_data["detail"].lower()

def test_service_handles_ai_model_unavailability():
    """
    Test that the service gracefully handles when AI models are not available.
    This ensures the service can run in placeholder mode if needed.
    """
    # This test verifies the service's fallback behavior
    # The actual AI model availability depends on the installation
    
    # Make a health check request
    response = client.get("/")
    assert response.status_code == 200
    
    response_data = response.json()
    ai_status = response_data["ai_status"]
    
    # Verify that the service reports its AI status clearly
    assert ai_status in ["AI models loaded", "Running in placeholder mode"]
    
    # Test image analysis regardless of AI model availability
    test_image = create_test_image(224, 224, (255, 255, 0))  # Yellow image
    files = {"file": ("test_fallback.png", test_image, "image/png")}
    
    response = client.post("/analyze_image", files=files)
    assert response.status_code == 200
    
    # Verify that the service provides a response regardless of AI availability
    response_data = response.json()
    assert "processing_method" in response_data
    assert response_data["processing_method"] in ["ai_powered_analysis", "placeholder_mode"]

def test_placeholder():
    """
    Placeholder test that always passes.
    This ensures the test infrastructure is working correctly.
    """
    # Simple assertion that always succeeds
    assert True
