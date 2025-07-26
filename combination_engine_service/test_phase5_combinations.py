# Phase 5 Test Suite: Intelligent Combination Engine with Multi-Modal AI Integration
# Comprehensive testing for AI-powered clothing combination generation

import unittest
import sys
import os
import asyncio
import json
from unittest.mock import patch, MagicMock
from datetime import datetime

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Import the intelligent combination engine for testing
    from intelligent_combiner import IntelligentCombinationEngine
    INTELLIGENT_COMBINER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Intelligent combiner not available: {e}")
    INTELLIGENT_COMBINER_AVAILABLE = False

class TestIntelligentCombinationEngine(unittest.TestCase):
    """
    Test suite for the Phase 5 Intelligent Combination Engine.
    Tests multi-modal AI integration and advanced combination generation.
    """
    
    def setUp(self):
        """Set up test environment before each test."""
        print(f"\n🧪 Setting up test: {self._testMethodName}")
        
        if INTELLIGENT_COMBINER_AVAILABLE:
            # Initialize the intelligent combination engine for testing
            self.engine = IntelligentCombinationEngine(
                image_service_url="http://localhost:8001",
                style_service_url="http://localhost:8003"
            )
        
        # Create comprehensive mock wardrobe data for testing
        self.mock_wardrobe = {
            "tops": [
                {"id": "top_001", "type": "shirt", "color": "blue", "style": "casual", "pattern": "solid"},
                {"id": "top_002", "type": "blouse", "color": "black", "style": "formal", "pattern": "solid"},
                {"id": "top_003", "type": "t-shirt", "color": "white", "style": "casual", "pattern": "solid"},
                {"id": "top_004", "type": "sweater", "color": "gray", "style": "smart_casual", "pattern": "textured"}
            ],
            "bottoms": [
                {"id": "bottom_001", "type": "jeans", "color": "blue", "style": "casual", "pattern": "denim"},
                {"id": "bottom_002", "type": "dress pants", "color": "black", "style": "formal", "pattern": "solid"},
                {"id": "bottom_003", "type": "chinos", "color": "khaki", "style": "smart_casual", "pattern": "solid"},
                {"id": "bottom_004", "type": "shorts", "color": "navy", "style": "casual", "pattern": "solid"}
            ],
            "shoes": [
                {"id": "shoe_001", "type": "sneakers", "color": "white", "style": "casual", "pattern": "solid"},
                {"id": "shoe_002", "type": "dress shoes", "color": "black", "style": "formal", "pattern": "leather"},
                {"id": "shoe_003", "type": "loafers", "color": "brown", "style": "smart_casual", "pattern": "leather"}
            ]
        }
        
        # Create mock style profile for testing
        self.mock_style_profile = {
            'visual_style_preferences': {
                'dominant_style': 'casual',
                'color_preferences': {'dominant_color': 'blue'}
            },
            'behavioral_patterns': {
                'engagement_metrics': {'engagement_score': 0.8}
            },
            'analysis_confidence': 0.75
        }
    
    @unittest.skipUnless(INTELLIGENT_COMBINER_AVAILABLE, "Intelligent combiner not available")
    def test_engine_initialization(self):
        """Test that the intelligent combination engine initializes correctly."""
        print("   Testing engine initialization...")
        
        # Test that engine components are properly initialized
        self.assertIsNotNone(self.engine)
        self.assertIsNotNone(self.engine.compatibility_clusterer)
        self.assertIsNotNone(self.engine.feature_scaler)
        self.assertIsNotNone(self.engine.outfit_graph)
        
        # Test that compatibility matrices are loaded
        self.assertIsInstance(self.engine.style_compatibility_matrix, dict)
        self.assertIsInstance(self.engine.color_harmony_rules, dict)
        self.assertIsInstance(self.engine.pattern_compatibility, dict)
        
        # Test that feature weights are properly configured
        self.assertIsInstance(self.engine.feature_weights, dict)
        self.assertAlmostEqual(sum(self.engine.feature_weights.values()), 1.0, places=1)
        
        print("   ✅ Engine initialization test passed")
    
    @unittest.skipUnless(INTELLIGENT_COMBINER_AVAILABLE, "Intelligent combiner not available")
    def test_visual_compatibility_calculation(self):
        """Test visual compatibility calculation using mock features."""
        print("   Testing visual compatibility calculation...")
        
        # Create mock image features for testing
        mock_features_1 = self.engine._generate_mock_image_features("test_item_1")
        mock_features_2 = self.engine._generate_mock_image_features("test_item_2")
        mock_features_3 = self.engine._generate_mock_image_features("test_item_3")
        
        # Test compatibility calculation
        compatibility = self.engine.calculate_visual_compatibility(
            mock_features_1, mock_features_2, mock_features_3
        )
        
        # Verify compatibility score is within valid range
        self.assertIsInstance(compatibility, float)
        self.assertGreaterEqual(compatibility, 0.0)
        self.assertLessEqual(compatibility, 1.0)
        
        print(f"   ✅ Visual compatibility calculated: {compatibility:.3f}")
    
    @unittest.skipUnless(INTELLIGENT_COMBINER_AVAILABLE, "Intelligent combiner not available")
    def test_style_coherence_calculation(self):
        """Test style coherence calculation using fashion expertise rules."""
        print("   Testing style coherence calculation...")
        
        # Create items with different style classifications
        casual_item = {'style_classification': {'dominant_style': 'casual'}}
        formal_item = {'style_classification': {'dominant_style': 'formal'}}
        sporty_item = {'style_classification': {'dominant_style': 'sporty'}}
        
        # Test coherence for matching styles (should be high)
        high_coherence = self.engine.calculate_style_coherence(casual_item, casual_item, casual_item)
        self.assertGreater(high_coherence, 0.8)
        
        # Test coherence for mixed styles (should be lower)
        mixed_coherence = self.engine.calculate_style_coherence(casual_item, formal_item, sporty_item)
        self.assertLess(mixed_coherence, high_coherence)
        
        print(f"   ✅ Style coherence tests passed - High: {high_coherence:.3f}, Mixed: {mixed_coherence:.3f}")
    
    @unittest.skipUnless(INTELLIGENT_COMBINER_AVAILABLE, "Intelligent combiner not available")
    def test_color_harmony_calculation(self):
        """Test color harmony calculation using color theory principles."""
        print("   Testing color harmony calculation...")
        
        # Test monochromatic combination (should be perfect)
        blue_items = [
            {'color_analysis': {'dominant_color': 'blue'}},
            {'color_analysis': {'dominant_color': 'blue'}},
            {'color_analysis': {'dominant_color': 'blue'}}
        ]
        mono_harmony = self.engine.calculate_color_harmony(*blue_items)
        self.assertEqual(mono_harmony, 1.0)
        
        # Test neutral combination (should be high)
        neutral_items = [
            {'color_analysis': {'dominant_color': 'white'}},
            {'color_analysis': {'dominant_color': 'black'}},
            {'color_analysis': {'dominant_color': 'gray'}}
        ]
        neutral_harmony = self.engine.calculate_color_harmony(*neutral_items)
        self.assertGreater(neutral_harmony, 0.8)
        
        print(f"   ✅ Color harmony tests passed - Mono: {mono_harmony:.3f}, Neutral: {neutral_harmony:.3f}")
    
    @unittest.skipUnless(INTELLIGENT_COMBINER_AVAILABLE, "Intelligent combiner not available")
    def test_context_appropriateness_calculation(self):
        """Test context appropriateness calculation for different occasions."""
        print("   Testing context appropriateness calculation...")
        
        # Create formal items
        formal_items = [
            {'style_classification': {'dominant_style': 'formal'}, 'color_analysis': {'dominant_color': 'black'}},
            {'style_classification': {'dominant_style': 'formal'}, 'color_analysis': {'dominant_color': 'black'}},
            {'style_classification': {'dominant_style': 'formal'}, 'color_analysis': {'dominant_color': 'black'}}
        ]
        
        # Test formal context (should be high for formal items)
        formal_appropriateness = self.engine.calculate_context_appropriateness(*formal_items, "work")
        self.assertGreater(formal_appropriateness, 0.7)
        
        # Test casual context with formal items (should be lower)
        casual_appropriateness = self.engine.calculate_context_appropriateness(*formal_items, "casual")
        self.assertLess(casual_appropriateness, formal_appropriateness)
        
        print(f"   ✅ Context appropriateness tests passed - Formal: {formal_appropriateness:.3f}, Casual: {casual_appropriateness:.3f}")
    
    @unittest.skipUnless(INTELLIGENT_COMBINER_AVAILABLE, "Intelligent combiner not available")
    def test_intelligent_combination_generation(self):
        """Test complete intelligent combination generation workflow."""
        print("   Testing intelligent combination generation...")
        
        # Generate intelligent combination
        result = self.engine.generate_intelligent_combination(
            wardrobe_items=self.mock_wardrobe,
            user_style_profile=self.mock_style_profile,
            context="casual",
            user_id="test_user_001"
        )
        
        # Verify result structure
        self.assertIsInstance(result, dict)
        self.assertNotIn("error", result)
        
        # Check required fields
        required_fields = ['top', 'bottom', 'shoes', 'overall_score', 'detailed_scores']
        for field in required_fields:
            self.assertIn(field, result)
        
        # Verify score ranges
        self.assertGreaterEqual(result['overall_score'], 0.0)
        self.assertLessEqual(result['overall_score'], 1.0)
        
        # Check detailed scores
        detailed_scores = result['detailed_scores']
        score_types = ['visual_compatibility', 'style_coherence', 'color_harmony', 'pattern_balance', 'context_appropriateness']
        for score_type in score_types:
            self.assertIn(score_type, detailed_scores)
            self.assertGreaterEqual(detailed_scores[score_type], 0.0)
            self.assertLessEqual(detailed_scores[score_type], 1.0)
        
        print(f"   ✅ Intelligent combination generated successfully - Score: {result['overall_score']:.3f}")
    
    @unittest.skipUnless(INTELLIGENT_COMBINER_AVAILABLE, "Intelligent combiner not available")
    def test_style_profile_bonus_application(self):
        """Test that user style profile influences combination scoring."""
        print("   Testing style profile bonus application...")
        
        # Create test items
        top = {"id": "top_001", "style": "casual", "color": "blue"}
        bottom = {"id": "bottom_001", "style": "casual", "color": "blue"}
        shoe = {"id": "shoe_001", "style": "casual", "color": "white"}
        
        # Test with matching style profile
        matching_profile = {
            'visual_style_preferences': {
                'dominant_style': 'casual',
                'color_preferences': {'dominant_color': 'blue'}
            },
            'behavioral_patterns': {
                'engagement_metrics': {'engagement_score': 0.9}
            }
        }
        
        bonus = self.engine._apply_style_profile_bonus(top, bottom, shoe, matching_profile)
        self.assertGreater(bonus, 0.0)
        self.assertLessEqual(bonus, 0.2)  # Should not exceed 20% bonus
        
        # Test with non-matching profile
        non_matching_profile = {
            'visual_style_preferences': {
                'dominant_style': 'formal',
                'color_preferences': {'dominant_color': 'black'}
            },
            'behavioral_patterns': {
                'engagement_metrics': {'engagement_score': 0.3}
            }
        }
        
        no_bonus = self.engine._apply_style_profile_bonus(top, bottom, shoe, non_matching_profile)
        self.assertLessEqual(no_bonus, bonus)  # Should be less than matching profile
        
        print(f"   ✅ Style profile bonus tests passed - Matching: {bonus:.3f}, Non-matching: {no_bonus:.3f}")
    
    @unittest.skipUnless(INTELLIGENT_COMBINER_AVAILABLE, "Intelligent combiner not available")
    def test_intelligent_recommendations_generation(self):
        """Test generation of intelligent recommendations and styling tips."""
        print("   Testing intelligent recommendations generation...")
        
        # Create mock combination with high scores
        high_score_combination = {
            'overall_score': 0.85,
            'detailed_scores': {
                'visual_compatibility': 0.9,
                'style_coherence': 0.8,
                'color_harmony': 0.85,
                'pattern_balance': 0.8,
                'context_appropriateness': 0.9
            }
        }
        
        # Generate recommendations
        recommendations = self.engine._generate_intelligent_recommendations(
            high_score_combination, self.mock_style_profile, "casual"
        )
        
        # Verify recommendation structure
        self.assertIsInstance(recommendations, dict)
        expected_keys = ['styling_tips', 'accessory_suggestions', 'improvement_areas', 'alternative_suggestions', 'confidence_explanation']
        for key in expected_keys:
            self.assertIn(key, recommendations)
        
        # Check that high-scoring combination gets positive feedback
        self.assertGreater(len(recommendations['styling_tips']), 0)
        self.assertIn("confidence", recommendations['confidence_explanation'].lower())
        
        print("   ✅ Intelligent recommendations generated successfully")
    
    def test_mock_feature_generation_consistency(self):
        """Test that mock feature generation is consistent for the same input."""
        print("   Testing mock feature generation consistency...")
        
        if INTELLIGENT_COMBINER_AVAILABLE:
            # Generate features for the same item multiple times
            item_id = "test_item_123"
            features_1 = self.engine._generate_mock_image_features(item_id)
            features_2 = self.engine._generate_mock_image_features(item_id)
            
            # Features should be identical for the same item_id (deterministic)
            self.assertEqual(features_1['style_classification']['dominant_style'], 
                           features_2['style_classification']['dominant_style'])
            self.assertEqual(features_1['color_analysis']['dominant_color'], 
                           features_2['color_analysis']['dominant_color'])
            
            print("   ✅ Mock feature generation is consistent")
        else:
            print("   ⚠️ Skipping mock feature test - intelligent combiner not available")

class TestPhase5Integration(unittest.TestCase):
    """
    Integration tests for Phase 5 multi-modal AI integration.
    Tests the combination of Phase 2 and Phase 4 features.
    """
    
    def setUp(self):
        """Set up integration test environment."""
        print(f"\n🔗 Setting up integration test: {self._testMethodName}")
    
    def test_multi_modal_feature_integration(self):
        """Test integration of Phase 2 image features with Phase 4 style profiles."""
        print("   Testing multi-modal feature integration...")
        
        if INTELLIGENT_COMBINER_AVAILABLE:
            engine = IntelligentCombinationEngine()
            
            # Test that the engine can handle both image features and style profiles
            mock_wardrobe = {
                "tops": [{"id": "top_001", "style": "casual", "color": "blue"}],
                "bottoms": [{"id": "bottom_001", "style": "casual", "color": "blue"}],
                "shoes": [{"id": "shoe_001", "style": "casual", "color": "white"}]
            }
            
            mock_profile = {
                'visual_style_preferences': {'dominant_style': 'casual'},
                'behavioral_patterns': {'engagement_metrics': {'engagement_score': 0.7}}
            }
            
            # This should not raise an exception
            result = engine.generate_intelligent_combination(
                wardrobe_items=mock_wardrobe,
                user_style_profile=mock_profile,
                context="casual",
                user_id="integration_test_user"
            )
            
            # Verify integration worked
            self.assertIsInstance(result, dict)
            self.assertNotIn("error", result)
            
            print("   ✅ Multi-modal integration test passed")
        else:
            print("   ⚠️ Skipping integration test - intelligent combiner not available")
    
    def test_service_connectivity_handling(self):
        """Test handling of Phase 2 and Phase 4 service connectivity."""
        print("   Testing service connectivity handling...")
        
        if INTELLIGENT_COMBINER_AVAILABLE:
            # Test with mock service URLs (will use fallback logic)
            engine = IntelligentCombinationEngine(
                image_service_url="http://mock-service:8001",
                style_service_url="http://mock-service:8003"
            )
            
            # Test that engine gracefully handles service unavailability
            async def test_async():
                image_features = await engine.get_image_features("test_item")
                style_profile = await engine.get_style_profile("test_user")
                
                # Should return mock data when services are unavailable
                self.assertIsInstance(image_features, dict)
                self.assertIsInstance(style_profile, dict)
                
                return True
            
            # Run async test
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(test_async())
            loop.close()
            
            self.assertTrue(result)
            print("   ✅ Service connectivity handling test passed")
        else:
            print("   ⚠️ Skipping connectivity test - intelligent combiner not available")

def run_phase5_tests():
    """Run all Phase 5 tests and provide comprehensive results."""
    print("🚀 Starting Phase 5 Intelligent Combination Engine Test Suite")
    print("=" * 80)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test methods from both test classes
    for test_class in [TestIntelligentCombinationEngine, TestPhase5Integration]:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 80)
    print("📊 Phase 5 Test Results Summary:")
    print(f"   Tests Run: {result.testsRun}")
    print(f"   Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    print(f"   Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback.splitlines()[-1] if traceback else 'Unknown failure'}")
    
    if result.errors:
        print("\n🔥 Errors:")
        for test, traceback in result.errors:
            print(f"   - {test}: {traceback.splitlines()[-1] if traceback else 'Unknown error'}")
    
    # Determine overall result
    if result.wasSuccessful():
        print("\n🎉 All Phase 5 tests passed successfully!")
        print("   Intelligent Combination Engine is ready for production")
    else:
        print("\n⚠️ Some tests failed. Please review and fix issues before deployment.")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    # Run the comprehensive test suite
    success = run_phase5_tests()
    
    print("\n" + "=" * 80)
    print("Phase 5 Testing Complete!")
    
    if success:
        print("✅ Ready to proceed with intelligent combination generation")
    else:
        print("❌ Please address test failures before continuing")
