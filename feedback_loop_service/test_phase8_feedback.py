# Phase 8: Comprehensive Test Suite for Feedback Loop System
# Tests all feedback collection, learning, and adaptation functionality
# Ensures robust operation of the intelligent learning system

import pytest
import asyncio
import json
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
import tempfile
import os
import sqlite3

# Import the main application and components
from main import app, feedback_processor
from advanced_feedback_processor import AdvancedFeedbackProcessor, FeedbackType, LearningObjective
from fastapi.testclient import TestClient

# Create test client for API testing
client = TestClient(app)

@pytest.fixture
def temp_db():
    """
    Create a temporary database for testing.
    Ensures each test runs with a clean database state.
    """
    # Create temporary database file
    temp_db_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_db_path = temp_db_file.name
    temp_db_file.close()
    
    yield temp_db_path
    
    # Clean up after test
    if os.path.exists(temp_db_path):
        os.unlink(temp_db_path)

@pytest.fixture
def mock_feedback_processor(temp_db):
    """
    Create a mock feedback processor for testing.
    Provides controlled testing environment for feedback operations.
    """
    # Initialize processor with temporary database
    processor = AdvancedFeedbackProcessor(db_path=temp_db)
    
    # Mock some methods for predictable testing
    processor.processing_active = True
    
    return processor

@pytest.fixture
def sample_feedback_data():
    """
    Provide sample feedback data for testing.
    Contains realistic feedback scenarios for comprehensive testing.
    """
    return {
        "explicit_rating": {
            "user_id": "test_user_123",
            "session_id": "test_session_456",
            "feedback_type": "explicit_rating",
            "learning_objective": "recommendation_accuracy",
            "service_source": "recommendation_engine",
            "data": {
                "rating": 4,
                "item_id": "item_789",
                "recommendation_set_id": "rec_set_123"
            },
            "context": {
                "occasion": "work",
                "time_of_day": 14,
                "session_duration": 120,
                "items_viewed": 8
            },
            "confidence": 0.95
        },
        "implicit_engagement": {
            "user_id": "test_user_456",
            "session_id": "test_session_789",
            "feedback_type": "implicit_engagement",
            "learning_objective": "engagement_optimization",
            "service_source": "style_profile_service",
            "data": {
                "time_spent": 45,
                "interactions": 12,
                "scroll_depth": 0.8
            },
            "context": {
                "page_type": "style_profile",
                "device": "mobile",
                "time_of_day": 20
            },
            "confidence": 0.85
        },
        "behavioral_signals": {
            "user_id": "test_user_789",
            "session_id": "test_session_012",
            "feedback_type": "behavioral_signals",
            "learning_objective": "combination_quality",
            "service_source": "combination_engine",
            "data": {
                "action": "save",
                "combination_id": "combo_456",
                "items": ["item_1", "item_2", "item_3"]
            },
            "context": {
                "combination_type": "work_outfit",
                "user_style": "minimalist",
                "season": "spring"
            },
            "confidence": 0.90
        }
    }

class TestHealthEndpoints:
    """
    Test suite for health check and system status endpoints.
    Verifies basic service functionality and system monitoring.
    """
    
    def test_health_check(self):
        """
        Test the main health check endpoint.
        Verifies service is operational and returns correct information.
        """
        # Make health check request
        response = client.get("/")
        
        # Verify response structure and content
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        assert data["service"] == "Aura Feedback Loop and Learning System"
        assert data["phase"] == "Phase 8 - Intelligent Feedback Processing and System Adaptation"
        assert data["status"] == "operational"
        assert data["version"] == "8.0.0"
        
        # Check capabilities list
        assert "multi_modal_feedback_collection" in data["capabilities"]
        assert "real_time_learning_processing" in data["capabilities"]
        assert "intelligent_system_adaptation" in data["capabilities"]
        
        # Check service info
        assert "feedback_types" in data["service_info"]
        assert "learning_objectives" in data["service_info"]
        assert "supported_services" in data["service_info"]
        
        # Check timestamp format
        assert "timestamp" in data
        datetime.fromisoformat(data["timestamp"])  # Validates ISO format
    
    def test_system_health_endpoint(self):
        """
        Test the detailed system health endpoint.
        Verifies comprehensive system monitoring functionality.
        """
        # Make system health request
        response = client.get("/health")
        
        # Verify response structure
        assert response.status_code == 200
        data = response.json()
        
        # Check required health fields
        assert "status" in data
        assert "processing_active" in data
        assert "feedback_queue_size" in data
        assert "learning_models_status" in data
        assert "database_status" in data
        assert "system_load" in data
        
        # Verify system load metrics structure
        system_load = data["system_load"]
        assert "feedback_queue_utilization" in system_load
        assert "learning_insights_memory" in system_load
        assert "user_adaptations_memory" in system_load
        assert "processing_active" in system_load

class TestFeedbackSubmission:
    """
    Test suite for feedback submission endpoints.
    Covers single feedback, batch feedback, and validation scenarios.
    """
    
    def test_submit_valid_feedback(self, sample_feedback_data):
        """
        Test submission of valid feedback data.
        Verifies successful feedback collection and processing.
        """
        # Submit explicit rating feedback
        feedback_data = sample_feedback_data["explicit_rating"]
        response = client.post("/feedback", json=feedback_data)
        
        # Verify successful submission
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "feedback_id" in data
        assert data["status"] == "collected"
        assert "message" in data
        assert "processing_info" in data
        
        # Verify processing info
        processing_info = data["processing_info"]
        assert processing_info["learning_enabled"] == True
        assert processing_info["real_time_adaptation"] == True
        assert processing_info["feedback_type"] == feedback_data["feedback_type"]
        assert processing_info["learning_objective"] == feedback_data["learning_objective"]
    
    def test_submit_different_feedback_types(self, sample_feedback_data):
        """
        Test submission of different feedback types.
        Ensures all feedback types are handled correctly.
        """
        # Test each feedback type
        for feedback_name, feedback_data in sample_feedback_data.items():
            response = client.post("/feedback", json=feedback_data)
            
            # Each should be successful
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "collected"
            assert data["processing_info"]["feedback_type"] == feedback_data["feedback_type"]
    
    def test_submit_invalid_feedback_type(self):
        """
        Test submission with invalid feedback type.
        Verifies proper validation and error handling.
        """
        # Create feedback with invalid type
        invalid_feedback = {
            "user_id": "test_user",
            "feedback_type": "invalid_type",
            "learning_objective": "recommendation_accuracy",
            "service_source": "test_service",
            "data": {},
            "context": {}
        }
        
        # Submit invalid feedback
        response = client.post("/feedback", json=invalid_feedback)
        
        # Should return validation error
        assert response.status_code == 422
        error_detail = response.json()["detail"]
        assert any("feedback_type" in str(error) for error in error_detail)
    
    def test_submit_invalid_learning_objective(self):
        """
        Test submission with invalid learning objective.
        Verifies proper validation of learning objectives.
        """
        # Create feedback with invalid learning objective
        invalid_feedback = {
            "user_id": "test_user",
            "feedback_type": "explicit_rating",
            "learning_objective": "invalid_objective",
            "service_source": "test_service",
            "data": {},
            "context": {}
        }
        
        # Submit invalid feedback
        response = client.post("/feedback", json=invalid_feedback)
        
        # Should return validation error
        assert response.status_code == 422
        error_detail = response.json()["detail"]
        assert any("learning_objective" in str(error) for error in error_detail)
    
    def test_submit_feedback_batch(self, sample_feedback_data):
        """
        Test batch feedback submission.
        Verifies efficient processing of multiple feedback entries.
        """
        # Create batch of feedback entries
        feedback_batch = [
            sample_feedback_data["explicit_rating"],
            sample_feedback_data["implicit_engagement"],
            sample_feedback_data["behavioral_signals"]
        ]
        
        # Submit batch
        response = client.post("/feedback/batch", json=feedback_batch)
        
        # Verify successful batch processing
        assert response.status_code == 200
        data = response.json()
        
        # Check batch response structure
        assert "batch_id" in data
        assert data["total_entries"] == 3
        assert data["successful_entries"] == 3
        assert data["failed_entries"] == 0
        assert len(data["feedback_ids"]) == 3
        assert len(data["processing_results"]) == 3
        
        # Verify all entries were successful
        for result in data["processing_results"]:
            assert result["status"] == "success"
            assert "feedback_id" in result
    
    def test_submit_large_feedback_batch(self, sample_feedback_data):
        """
        Test batch size limit enforcement.
        Verifies proper handling of oversized batches.
        """
        # Create oversized batch (more than 100 entries)
        large_batch = [sample_feedback_data["explicit_rating"]] * 101
        
        # Submit oversized batch
        response = client.post("/feedback/batch", json=large_batch)
        
        # Should return error for batch too large
        assert response.status_code == 400
        assert "Batch size too large" in response.json()["detail"]

class TestLearningAnalytics:
    """
    Test suite for learning analytics and insights endpoints.
    Covers analytics generation, insight retrieval, and system metrics.
    """
    
    def test_get_learning_analytics(self):
        """
        Test learning analytics endpoint.
        Verifies comprehensive analytics data generation.
        """
        # Get learning analytics
        response = client.get("/analytics")
        
        # Verify successful response
        assert response.status_code == 200
        data = response.json()
        
        # Check analytics structure
        assert "feedback_analytics" in data
        assert "learning_analytics" in data
        assert "system_improvements" in data
        assert "real_time_metrics" in data
        
        # Verify feedback analytics structure
        feedback_analytics = data["feedback_analytics"]
        assert "total_feedback_collected" in feedback_analytics
        assert "feedback_by_type" in feedback_analytics
        assert "feedback_by_objective" in feedback_analytics
        assert "feedback_by_service" in feedback_analytics
    
    def test_get_learning_insights(self):
        """
        Test learning insights retrieval.
        Verifies insight generation and filtering functionality.
        """
        # Get all insights
        response = client.get("/insights")
        
        # Verify successful response
        assert response.status_code == 200
        insights = response.json()
        
        # Should return list of insights
        assert isinstance(insights, list)
        
        # Check insight structure if any exist
        if insights:
            insight = insights[0]
            assert "insight_id" in insight
            assert "learning_objective" in insight
            assert "insight_data" in insight
            assert "confidence_score" in insight
            assert "impact_estimate" in insight
            assert "action_recommendations" in insight
            assert "created_at" in insight
    
    def test_get_learning_insights_with_filters(self):
        """
        Test learning insights with filtering parameters.
        Verifies proper filtering and pagination functionality.
        """
        # Test with limit parameter
        response = client.get("/insights?limit=10")
        assert response.status_code == 200
        insights = response.json()
        assert len(insights) <= 10
        
        # Test with learning objective filter
        response = client.get("/insights?learning_objective=recommendation_accuracy")
        assert response.status_code == 200
        insights = response.json()
        
        # All returned insights should match the filter
        for insight in insights:
            assert insight["learning_objective"] == "recommendation_accuracy"
        
        # Test with applied_only filter
        response = client.get("/insights?applied_only=true")
        assert response.status_code == 200
        insights = response.json()
        
        # All returned insights should be applied
        for insight in insights:
            assert insight["applied_at"] is not None
    
    def test_get_learning_insights_invalid_objective(self):
        """
        Test learning insights with invalid learning objective.
        Verifies proper validation of filter parameters.
        """
        # Request with invalid learning objective
        response = client.get("/insights?learning_objective=invalid_objective")
        
        # Should return validation error
        assert response.status_code == 400
        assert "Invalid learning_objective" in response.json()["detail"]

class TestInsightApplication:
    """
    Test suite for applying learning insights and adaptations.
    Covers insight application and user-specific adaptations.
    """
    
    def test_apply_nonexistent_insight(self):
        """
        Test applying a non-existent learning insight.
        Verifies proper error handling for missing insights.
        """
        # Try to apply non-existent insight
        response = client.post("/insights/nonexistent_insight/apply")
        
        # Should return not found error
        assert response.status_code == 404
        assert "Learning insight not found" in response.json()["detail"]
    
    def test_apply_user_adaptation(self):
        """
        Test applying user-specific adaptations.
        Verifies user adaptation functionality.
        """
        # Define user adaptation request
        adaptation_data = {
            "user_id": "test_user_123",
            "adaptation_type": "recommendation_weight_adjustment",
            "parameters": {
                "style_weight": 0.8,
                "color_weight": 0.6,
                "context_weight": 0.9
            }
        }
        
        # Apply user adaptation
        response = client.post("/adaptations/user", json=adaptation_data)
        
        # Verify successful application
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "adaptation_id" in data
        assert data["user_id"] == adaptation_data["user_id"]
        assert data["status"] == "applied"
        assert "message" in data
    
    def test_get_user_adaptations(self):
        """
        Test retrieving user-specific adaptations.
        Verifies user adaptation tracking functionality.
        """
        # First apply an adaptation
        adaptation_data = {
            "user_id": "test_user_456",
            "adaptation_type": "style_preference_update",
            "parameters": {"preferred_colors": ["blue", "black", "white"]}
        }
        
        apply_response = client.post("/adaptations/user", json=adaptation_data)
        assert apply_response.status_code == 200
        
        # Then retrieve user adaptations
        response = client.get(f"/adaptations/user/{adaptation_data['user_id']}")
        
        # Verify successful retrieval
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert data["user_id"] == adaptation_data["user_id"]
        assert "total_adaptations" in data
        assert "adaptations" in data
        assert data["total_adaptations"] >= 1
        
        # Verify the applied adaptation is included
        adaptations = data["adaptations"]
        assert adaptation_data["adaptation_type"] in adaptations

class TestUtilityEndpoints:
    """
    Test suite for utility and reference endpoints.
    Covers feedback types, model retraining, and system utilities.
    """
    
    def test_get_feedback_types(self):
        """
        Test feedback types reference endpoint.
        Verifies comprehensive feedback type documentation.
        """
        # Get feedback types
        response = client.get("/feedback/types")
        
        # Verify successful response
        assert response.status_code == 200
        data = response.json()
        
        # Check structure
        assert "feedback_types" in data
        assert "learning_objectives" in data
        assert "feedback_type_descriptions" in data
        assert "learning_objective_descriptions" in data
        
        # Verify all expected feedback types are present
        expected_types = [ft.value for ft in FeedbackType]
        assert all(ft in data["feedback_types"] for ft in expected_types)
        
        # Verify all expected learning objectives are present
        expected_objectives = [lo.value for lo in LearningObjective]
        assert all(lo in data["learning_objectives"] for lo in expected_objectives)
    
    def test_trigger_model_retraining(self):
        """
        Test model retraining endpoint.
        Verifies model update functionality.
        """
        # Trigger retraining for all objectives
        response = client.post("/learning/retrain?force_retrain=true")
        
        # Verify successful response
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "retraining_id" in data
        assert "timestamp" in data
        assert "objectives_processed" in data
        assert "successful_retraining" in data
        assert "results" in data
        assert "message" in data
        
        # Verify retraining results structure
        results = data["results"]
        expected_objectives = [lo.value for lo in LearningObjective]
        
        for objective in expected_objectives:
            assert objective in results
            result = results[objective]
            assert "status" in result
            # Status should be either "completed", "skipped", or "failed"
            assert result["status"] in ["completed", "skipped", "failed"]
    
    def test_trigger_model_retraining_specific_objective(self):
        """
        Test model retraining for specific learning objective.
        Verifies targeted retraining functionality.
        """
        # Trigger retraining for specific objective
        objective = "recommendation_accuracy"
        response = client.post(f"/learning/retrain?learning_objective={objective}&force_retrain=true")
        
        # Verify successful response
        assert response.status_code == 200
        data = response.json()
        
        # Should only process one objective
        assert data["objectives_processed"] == 1
        assert objective in data["results"]
    
    def test_trigger_model_retraining_invalid_objective(self):
        """
        Test model retraining with invalid objective.
        Verifies proper validation of learning objectives.
        """
        # Try retraining with invalid objective
        response = client.post("/learning/retrain?learning_objective=invalid_objective")
        
        # Should return validation error
        assert response.status_code == 400
        assert "Invalid learning_objective" in response.json()["detail"]

class TestDataPrivacy:
    """
    Test suite for data privacy and GDPR compliance features.
    Covers feedback deletion and data management.
    """
    
    def test_delete_feedback(self, sample_feedback_data):
        """
        Test feedback deletion functionality.
        Verifies GDPR compliance and data privacy features.
        """
        # First submit feedback to get a valid feedback ID
        feedback_data = sample_feedback_data["explicit_rating"]
        submit_response = client.post("/feedback", json=feedback_data)
        assert submit_response.status_code == 200
        
        feedback_id = submit_response.json()["feedback_id"]
        
        # Now delete the feedback
        delete_response = client.delete(f"/feedback/{feedback_id}")
        
        # Verify successful deletion
        assert delete_response.status_code == 200
        data = delete_response.json()
        
        # Check response structure
        assert data["feedback_id"] == feedback_id
        assert data["status"] == "deleted"
        assert "message" in data
    
    def test_delete_nonexistent_feedback(self):
        """
        Test deletion of non-existent feedback.
        Verifies proper error handling for invalid feedback IDs.
        """
        # Try to delete non-existent feedback
        response = client.delete("/feedback/nonexistent_feedback_id")
        
        # Should return not found error
        assert response.status_code == 404
        assert "Feedback not found" in response.json()["detail"]

class TestErrorHandling:
    """
    Test suite for error handling and edge cases.
    Ensures robust operation under various failure conditions.
    """
    
    def test_missing_required_fields(self):
        """
        Test handling of requests with missing required fields.
        Verifies proper validation error responses.
        """
        # Submit feedback missing required fields
        incomplete_feedback = {
            "user_id": "test_user"
            # Missing feedback_type, learning_objective, service_source
        }
        
        response = client.post("/feedback", json=incomplete_feedback)
        
        # Should return validation error
        assert response.status_code == 422
        error_detail = response.json()["detail"]
        
        # Should mention missing required fields
        missing_fields = ["feedback_type", "learning_objective", "service_source"]
        for field in missing_fields:
            assert any(field in str(error) for error in error_detail)
    
    def test_invalid_confidence_value(self):
        """
        Test handling of invalid confidence values.
        Verifies proper validation of numeric ranges.
        """
        # Submit feedback with invalid confidence (outside 0-1 range)
        invalid_feedback = {
            "user_id": "test_user",
            "feedback_type": "explicit_rating",
            "learning_objective": "recommendation_accuracy",
            "service_source": "test_service",
            "data": {},
            "context": {},
            "confidence": 1.5  # Invalid: > 1.0
        }
        
        response = client.post("/feedback", json=invalid_feedback)
        
        # Should return validation error
        assert response.status_code == 422
        error_detail = response.json()["detail"]
        assert any("confidence" in str(error) for error in error_detail)
    
    def test_404_handler(self):
        """
        Test custom 404 error handler.
        Verifies helpful error responses for non-existent endpoints.
        """
        # Request non-existent endpoint
        response = client.get("/nonexistent-endpoint")
        
        # Should return custom 404 response
        assert response.status_code == 404
        data = response.json()
        
        # Should provide helpful error information
        assert "error" in data
        assert "message" in data
        assert "available_endpoints" in data

class TestPerformanceAndScaling:
    """
    Test suite for performance and scaling considerations.
    Verifies system behavior under load and stress conditions.
    """
    
    def test_concurrent_feedback_submission(self, sample_feedback_data):
        """
        Test concurrent feedback submission handling.
        Simulates multiple users submitting feedback simultaneously.
        """
        import concurrent.futures
        import threading
        
        # Create multiple feedback entries with different user IDs
        feedback_entries = []
        for i in range(10):
            feedback = sample_feedback_data["explicit_rating"].copy()
            feedback["user_id"] = f"concurrent_user_{i}"
            feedback_entries.append(feedback)
        
        # Function to submit single feedback
        def submit_feedback(feedback_data):
            return client.post("/feedback", json=feedback_data)
        
        # Submit all feedback concurrently
        responses = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_feedback = {executor.submit(submit_feedback, feedback): feedback 
                                for feedback in feedback_entries}
            
            for future in concurrent.futures.as_completed(future_to_feedback):
                response = future.result()
                responses.append(response)
        
        # Verify all submissions were successful
        assert len(responses) == 10
        for response in responses:
            assert response.status_code == 200
            assert response.json()["status"] == "collected"
    
    def test_large_feedback_data(self):
        """
        Test handling of large feedback data payloads.
        Verifies system handles complex feedback scenarios.
        """
        # Create feedback with large data payload
        large_feedback = {
            "user_id": "test_user_large_data",
            "feedback_type": "implicit_engagement",
            "learning_objective": "engagement_optimization",
            "service_source": "test_service",
            "data": {
                "large_list": list(range(1000)),
                "complex_dict": {f"key_{i}": f"value_{i}" for i in range(100)},
                "nested_structure": {
                    "level1": {
                        "level2": {
                            "level3": ["item" for _ in range(50)]
                        }
                    }
                }
            },
            "context": {
                "detailed_context": {f"context_key_{i}": f"context_value_{i}" for i in range(50)}
            }
        }
        
        # Submit large feedback
        response = client.post("/feedback", json=large_feedback)
        
        # Should handle large data successfully
        assert response.status_code == 200
        assert response.json()["status"] == "collected"

# Test configuration and fixtures
@pytest.fixture(scope="session")
def event_loop():
    """
    Create event loop for async testing.
    Ensures proper async test execution.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Performance benchmarks
class TestPerformanceBenchmarks:
    """
    Performance benchmark tests for the feedback system.
    Measures system performance under various conditions.
    """
    
    def test_feedback_submission_performance(self, sample_feedback_data):
        """
        Benchmark feedback submission performance.
        Measures processing time for feedback collection.
        """
        import time
        
        feedback_data = sample_feedback_data["explicit_rating"]
        
        # Measure submission time
        start_time = time.time()
        response = client.post("/feedback", json=feedback_data)
        end_time = time.time()
        
        submission_time = end_time - start_time
        
        # Verify successful submission
        assert response.status_code == 200
        
        # Performance assertion (should complete within reasonable time)
        assert submission_time < 1.0  # Should complete within 1 second
        
        print(f"Feedback submission time: {submission_time:.3f} seconds")
    
    def test_analytics_generation_performance(self):
        """
        Benchmark analytics generation performance.
        Measures time to generate comprehensive analytics.
        """
        import time
        
        # Measure analytics generation time
        start_time = time.time()
        response = client.get("/analytics")
        end_time = time.time()
        
        generation_time = end_time - start_time
        
        # Verify successful generation
        assert response.status_code == 200
        
        # Performance assertion
        assert generation_time < 2.0  # Should complete within 2 seconds
        
        print(f"Analytics generation time: {generation_time:.3f} seconds")

if __name__ == "__main__":
    # Run the tests
    print("🧪 Running Phase 8 Feedback Loop System Tests")
    print("   Testing intelligent feedback collection and learning functionality")
    print("   Comprehensive test coverage for all system components")
    
    # Configure pytest arguments for detailed output
    pytest_args = [
        __file__,
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--strict-markers",  # Strict marker checking
        "--disable-warnings",  # Disable warnings for cleaner output
    ]
    
    # Run the tests
    exit_code = pytest.main(pytest_args)
    
    if exit_code == 0:
        print("\n✅ All tests passed! Phase 8 Feedback Loop System is working correctly.")
        print("   🎯 Intelligent feedback collection: ✅")
        print("   🧠 Machine learning processing: ✅")
        print("   📊 Learning analytics generation: ✅")
        print("   🔧 System adaptation capabilities: ✅")
        print("   🔒 Data privacy compliance: ✅")
        print("   ⚡ Performance benchmarks: ✅")
    else:
        print(f"\n❌ Some tests failed (exit code: {exit_code})")
        print("   Please review the test output and fix any issues.")
    
    exit(exit_code)
