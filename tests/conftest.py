# AURA AI Test Configuration
# Global pytest configuration and shared fixtures for all test suites

import os  # Standard library for operating system interface functions
import sys  # System-specific parameters and functions for Python interpreter interaction
import pytest  # Testing framework for creating and running test cases
import asyncio  # Asynchronous I/O, event loop, coroutines and tasks library
from unittest.mock import Mock, patch  # Mock object library for creating test doubles
from typing import Dict, Any, Generator  # Type hints for better code documentation
import tempfile  # Temporary file and directory creation utilities
import shutil  # High-level file operations for copying and removing files

# Add the project root directory to Python path for importing modules
# This allows test files to import from the main project modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Test environment configuration settings
# These settings ensure tests run in isolated environment
TEST_ENV_VARS = {
    "TESTING": "true",  # Flag to indicate we're in testing mode
    "TEST_DATABASE_URL": "postgresql://test:test@localhost:5433/aura_test",  # Test database connection
    "TEST_REDIS_URL": "redis://localhost:6380",  # Test Redis instance connection
    "LOG_LEVEL": "WARNING",  # Reduce log noise during testing
    "DISABLE_EXTERNAL_APIS": "true",  # Prevent real API calls during tests
}

# Apply test environment variables for all test sessions
# This ensures consistent test environment across all test runs
for key, value in TEST_ENV_VARS.items():
    os.environ[key] = value

# Pytest configuration settings
# These settings control how pytest behaves during test execution
pytest_plugins = [
    "pytest_asyncio",  # Enable async/await support in tests
    "pytest_mock",     # Enhanced mocking capabilities
    "pytest_cov",     # Code coverage measurement
]

# Test markers for categorizing and filtering tests
# Markers allow running specific categories of tests
pytest.ini_content = """
[tool:pytest]
markers =
    unit: Unit tests for individual components
    integration: Integration tests for component interaction
    e2e: End-to-end tests for complete workflows
    slow: Tests that take longer than usual to run
    fast: Tests that run quickly (under 1 second)
    database: Tests that require database connection
    api: Tests that involve API endpoints
    security: Security-focused tests
    performance: Performance and load tests
    ai_model: Tests involving AI model operations
    mock_external: Tests using external service mocks
"""

@pytest.fixture(scope="session")
def event_loop():
    """
    Create an event loop for async test support.
    Session-scoped fixture that provides event loop for all async tests.
    This ensures consistent async behavior across test suite.
    """
    # Create a new event loop for the test session
    loop = asyncio.new_event_loop()
    
    # Set the created loop as the current event loop
    asyncio.set_event_loop(loop)
    
    # Yield the loop to tests (this makes it available to test functions)
    yield loop
    
    # Cleanup: close the loop after all tests complete
    loop.close()

@pytest.fixture(scope="session")
def test_database_url() -> str:
    """
    Provide test database URL for database-dependent tests.
    This fixture ensures all tests use the same test database configuration.
    Returns the database URL that should be used for testing.
    """
    # Return the test database URL from environment variables
    return os.getenv("TEST_DATABASE_URL", "postgresql://test:test@localhost:5433/aura_test")

@pytest.fixture(scope="session")
def test_redis_url() -> str:
    """
    Provide test Redis URL for cache and session tests.
    This fixture ensures all tests use the same test Redis configuration.
    Returns the Redis URL that should be used for testing.
    """
    # Return the test Redis URL from environment variables
    return os.getenv("TEST_REDIS_URL", "redis://localhost:6380")

@pytest.fixture
def temp_directory() -> Generator[str, None, None]:
    """
    Create a temporary directory for file-based tests.
    This fixture provides a clean temporary directory for each test.
    The directory is automatically cleaned up after test completion.
    """
    # Create a temporary directory with a descriptive prefix
    temp_dir = tempfile.mkdtemp(prefix="aura_test_")
    
    # Yield the directory path to the test function
    yield temp_dir
    
    # Cleanup: remove the temporary directory and all its contents
    shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture
def mock_external_apis():
    """
    Mock all external API calls to prevent real network requests during tests.
    This fixture ensures tests run in isolation without external dependencies.
    """
    # Dictionary to store all the mocked objects
    mocks = {}
    
    # Mock HTTP requests library to prevent real API calls
    with patch('requests.get') as mock_get, \
         patch('requests.post') as mock_post, \
         patch('requests.put') as mock_put, \
         patch('requests.delete') as mock_delete:
        
        # Configure default responses for different HTTP methods
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"status": "mocked"}
        
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"status": "created", "id": "mock_id"}
        
        mock_put.return_value.status_code = 200
        mock_put.return_value.json.return_value = {"status": "updated"}
        
        mock_delete.return_value.status_code = 204
        
        # Store mocks in dictionary for test access
        mocks.update({
            'get': mock_get,
            'post': mock_post,
            'put': mock_put,
            'delete': mock_delete
        })
        
        # Yield mocks to test functions
        yield mocks

@pytest.fixture
def sample_user_data() -> Dict[str, Any]:
    """
    Provide sample user data for user-related tests.
    This fixture creates consistent test user data across all tests.
    """
    # Return a dictionary with sample user information
    return {
        "user_id": "test_user_12345",  # Unique identifier for test user
        "username": "testuser",        # Username for authentication tests
        "email": "test@example.com",   # Email for communication tests
        "preferences": {               # User preferences for style tests
            "style": "casual",         # Preferred clothing style
            "colors": ["blue", "black", "white"],  # Preferred colors
            "occasions": ["work", "casual", "formal"]  # Occasion preferences
        },
        "profile": {                   # User profile information
            "age_range": "25-35",      # Age group for style recommendations
            "body_type": "average",    # Body type for fit recommendations
            "location": "Turkey"       # Location for cultural style preferences
        }
    }

@pytest.fixture
def sample_clothing_data() -> Dict[str, Any]:
    """
    Provide sample clothing item data for clothing analysis tests.
    This fixture creates consistent test clothing data for image processing tests.
    """
    # Return a dictionary with sample clothing information
    return {
        "item_id": "clothing_item_123",  # Unique identifier for clothing item
        "type": "dress",                 # Type of clothing item
        "colors": ["red", "blue"],       # Colors present in the item
        "style": "casual",               # Style category of the item
        "occasion": "work",              # Appropriate occasion for the item
        "brand": "TestBrand",            # Brand name for filtering
        "price": 99.99,                  # Price for budget filtering
        "size": "M",                     # Size for fit matching
        "material": "cotton",            # Material for comfort preferences
        "description": "Beautiful casual dress perfect for work"  # Item description
    }

@pytest.fixture
def sample_image_analysis_result() -> Dict[str, Any]:
    """
    Provide sample image analysis result for computer vision tests.
    This fixture simulates the output of image processing AI models.
    """
    # Return a dictionary with sample image analysis results
    return {
        "success": True,                 # Indicates successful analysis
        "confidence": 0.95,              # Confidence score of the analysis
        "clothing_items": [              # List of detected clothing items
            {
                "type": "dress",         # Detected clothing type
                "confidence": 0.95,      # Confidence for this detection
                "colors": ["red", "blue"],  # Detected colors
                "style": "casual",       # Detected style
                "bbox": [10, 20, 100, 200]  # Bounding box coordinates
            }
        ],
        "scene_context": {               # Context information from the image
            "background": "indoor",      # Background setting
            "lighting": "natural",       # Lighting conditions
            "occasion": "casual"         # Inferred occasion
        },
        "processing_time": 0.25          # Time taken for analysis in seconds
    }

@pytest.fixture
def sample_recommendation_data() -> Dict[str, Any]:
    """
    Provide sample recommendation data for recommendation engine tests.
    This fixture creates consistent test recommendation data.
    """
    # Return a dictionary with sample recommendation information
    return {
        "recommendation_id": "rec_12345",  # Unique recommendation identifier
        "user_id": "test_user_12345",      # User who received the recommendation
        "recommended_items": [             # List of recommended clothing items
            "clothing_item_123",           # Item ID from sample clothing data
            "clothing_item_124",           # Additional recommended item
            "clothing_item_125"            # Third recommended item
        ],
        "recommendation_reason": "Based on your style preferences",  # Explanation
        "confidence_score": 0.88,          # How confident the system is
        "category": "work_outfit",         # Category of recommendation
        "created_at": "2024-01-15T10:30:00Z"  # Timestamp of recommendation
    }

@pytest.fixture
def sample_feedback_data() -> Dict[str, Any]:
    """
    Provide sample feedback data for feedback loop tests.
    This fixture creates consistent test feedback data for NLU processing.
    """
    # Return a dictionary with sample feedback information
    return {
        "feedback_id": "feedback_12345",        # Unique feedback identifier
        "user_id": "test_user_12345",           # User who provided feedback
        "recommendation_id": "rec_12345",       # Related recommendation
        "feedback_text": "Bu kombini hiç beğenmedim",  # Turkish feedback text
        "feedback_type": "negative_general",    # Classified feedback type
        "confidence": 0.92,                     # Classification confidence
        "context": {                            # Additional context information
            "occasion": "work",                 # Occasion context
            "weather": "cold",                  # Weather context
            "mood": "professional"              # User mood context
        },
        "timestamp": "2024-01-15T14:30:00Z"     # When feedback was given
    }

@pytest.fixture
def mock_ai_models():
    """
    Mock AI model responses to avoid loading actual models during tests.
    This fixture provides consistent mock responses for all AI models.
    """
    # Dictionary to store all mocked AI model responses
    mocks = {}
    
    # Mock computer vision model (CLIP/Detectron2)
    with patch('services.ai_models.vision.CLIPModel') as mock_clip, \
         patch('services.ai_models.vision.Detectron2Model') as mock_detectron:
        
        # Configure CLIP model mock responses
        mock_clip.return_value.encode_image.return_value = [0.1, 0.2, 0.3]  # Mock image embedding
        mock_clip.return_value.encode_text.return_value = [0.4, 0.5, 0.6]   # Mock text embedding
        
        # Configure Detectron2 model mock responses
        mock_detectron.return_value.detect.return_value = {
            "boxes": [[10, 20, 100, 200]],  # Bounding box coordinates
            "classes": ["dress"],            # Detected object classes
            "scores": [0.95]                 # Detection confidence scores
        }
        
        # Store mocks for test access
        mocks.update({
            'clip': mock_clip,
            'detectron': mock_detectron
        })
        
        # Yield mocks to test functions
        yield mocks

@pytest.fixture(autouse=True)
def setup_test_environment():
    """
    Automatically set up test environment for each test.
    This fixture runs before every test to ensure clean state.
    The autouse=True parameter makes this fixture run automatically.
    """
    # Clear any cached data that might interfere with tests
    # This ensures each test starts with a clean slate
    
    # Set up test-specific logging configuration
    import logging
    logging.getLogger().setLevel(logging.WARNING)  # Reduce log noise during tests
    
    # Yield control to the test function
    yield
    
    # Cleanup after test completion
    # Reset any global state that might have been modified during the test
    pass

# Custom assertions for AURA AI specific testing
class AuraAssertions:
    """
    Custom assertion methods specific to AURA AI testing needs.
    These methods provide domain-specific test validations.
    """
    
    @staticmethod
    def assert_valid_clothing_analysis(result: Dict[str, Any]) -> None:
        """
        Assert that a clothing analysis result has the expected structure.
        This method validates the output format of image processing services.
        """
        # Check that result is a dictionary
        assert isinstance(result, dict), "Clothing analysis result must be a dictionary"
        
        # Check required fields are present
        assert "success" in result, "Result must contain 'success' field"
        assert "clothing_items" in result, "Result must contain 'clothing_items' field"
        assert "confidence" in result, "Result must contain 'confidence' field"
        
        # Validate data types
        assert isinstance(result["success"], bool), "Success field must be boolean"
        assert isinstance(result["clothing_items"], list), "Clothing items must be a list"
        assert isinstance(result["confidence"], (int, float)), "Confidence must be numeric"
        
        # Validate confidence range
        assert 0 <= result["confidence"] <= 1, "Confidence must be between 0 and 1"
    
    @staticmethod
    def assert_valid_recommendation(recommendation: Dict[str, Any]) -> None:
        """
        Assert that a recommendation has the expected structure.
        This method validates the output format of recommendation services.
        """
        # Check that recommendation is a dictionary
        assert isinstance(recommendation, dict), "Recommendation must be a dictionary"
        
        # Check required fields are present
        required_fields = ["recommendation_id", "user_id", "recommended_items"]
        for field in required_fields:
            assert field in recommendation, f"Recommendation must contain '{field}' field"
        
        # Validate recommended items
        items = recommendation["recommended_items"]
        assert isinstance(items, list), "Recommended items must be a list"
        assert len(items) > 0, "Must recommend at least one item"
        
        # Validate confidence score if present
        if "confidence_score" in recommendation:
            confidence = recommendation["confidence_score"]
            assert isinstance(confidence, (int, float)), "Confidence score must be numeric"
            assert 0 <= confidence <= 1, "Confidence score must be between 0 and 1"

# Make custom assertions available as a fixture
@pytest.fixture
def aura_assert():
    """
    Provide custom AURA AI assertion methods to tests.
    This fixture makes domain-specific assertions available to all tests.
    """
    # Return the custom assertion class instance
    return AuraAssertions()

# Test data generators for creating varied test scenarios
class TestDataGenerator:
    """
    Generate varied test data for comprehensive testing scenarios.
    This class provides methods to create different types of test data.
    """
    
    @staticmethod
    def generate_user_variations(count: int = 5) -> list:
        """
        Generate multiple user profiles for testing different scenarios.
        This method creates varied user data for comprehensive testing.
        """
        # List to store generated user data
        users = []
        
        # Generate specified number of user variations
        for i in range(count):
            user = {
                "user_id": f"test_user_{i + 1:05d}",  # Zero-padded user ID
                "username": f"testuser{i + 1}",       # Sequential username
                "email": f"test{i + 1}@example.com",  # Sequential email
                "preferences": {
                    "style": ["casual", "formal", "sporty", "bohemian", "classic"][i % 5],
                    "colors": [
                        ["blue", "black", "white"],
                        ["red", "pink", "purple"],
                        ["green", "brown", "beige"],
                        ["yellow", "orange", "coral"],
                        ["gray", "navy", "burgundy"]
                    ][i % 5],
                    "occasions": ["work", "casual", "formal", "sport", "party"]
                },
                "profile": {
                    "age_range": ["18-25", "25-35", "35-45", "45-55", "55+"][i % 5],
                    "body_type": ["petite", "average", "plus", "tall", "athletic"][i % 5],
                    "location": ["Turkey", "Europe", "USA", "Asia", "Global"][i % 5]
                }
            }
            users.append(user)
        
        # Return the list of generated users
        return users

# Make test data generator available as a fixture
@pytest.fixture
def test_data_generator():
    """
    Provide test data generation utilities to tests.
    This fixture makes data generation methods available to all tests.
    """
    # Return the test data generator class
    return TestDataGenerator()

# Pytest hooks for custom test behavior
def pytest_configure(config):
    """
    Configure pytest with custom settings and markers.
    This function runs once when pytest starts up.
    """
    # Register custom markers to avoid warnings
    config.addinivalue_line("markers", "unit: Unit tests for individual components")
    config.addinivalue_line("markers", "integration: Integration tests for component interaction")
    config.addinivalue_line("markers", "e2e: End-to-end tests for complete workflows")
    config.addinivalue_line("markers", "slow: Tests that take longer than usual to run")
    config.addinivalue_line("markers", "fast: Tests that run quickly (under 1 second)")
    config.addinivalue_line("markers", "database: Tests that require database connection")
    config.addinivalue_line("markers", "api: Tests that involve API endpoints")
    config.addinivalue_line("markers", "security: Security-focused tests")
    config.addinivalue_line("markers", "performance: Performance and load tests")
    config.addinivalue_line("markers", "ai_model: Tests involving AI model operations")
    config.addinivalue_line("markers", "mock_external: Tests using external service mocks")

def pytest_collection_modifyitems(config, items):
    """
    Modify test collection to add automatic markers based on test location.
    This function automatically assigns markers to tests based on their file path.
    """
    # Iterate through all collected test items
    for item in items:
        # Get the test file path relative to the tests directory
        test_path = str(item.fspath.relative_to(item.fspath.common(item.fspath)))
        
        # Add markers based on test file location
        if "/unit/" in test_path:
            item.add_marker(pytest.mark.unit)      # Mark as unit test
            item.add_marker(pytest.mark.fast)      # Unit tests should be fast
        elif "/integration/" in test_path:
            item.add_marker(pytest.mark.integration)  # Mark as integration test
        elif "/e2e/" in test_path:
            item.add_marker(pytest.mark.e2e)       # Mark as end-to-end test
            item.add_marker(pytest.mark.slow)      # E2E tests are typically slow
        elif "/performance/" in test_path:
            item.add_marker(pytest.mark.performance)  # Mark as performance test
            item.add_marker(pytest.mark.slow)         # Performance tests are slow
        elif "/security/" in test_path:
            item.add_marker(pytest.mark.security)  # Mark as security test
        
        # Add database marker for tests that need database
        if "database" in test_path.lower() or "db" in test_path.lower():
            item.add_marker(pytest.mark.database)
        
        # Add API marker for tests that involve API endpoints
        if "api" in test_path.lower() or "endpoint" in test_path.lower():
            item.add_marker(pytest.mark.api)
        
        # Add AI model marker for tests involving AI models
        if "ai" in test_path.lower() or "model" in test_path.lower():
            item.add_marker(pytest.mark.ai_model)
