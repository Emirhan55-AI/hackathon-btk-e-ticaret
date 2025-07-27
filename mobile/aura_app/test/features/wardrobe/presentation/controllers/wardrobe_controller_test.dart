// Phase 3 Wardrobe Controller Main Tests
// Core functionality tests for wardrobe controller

import 'package:flutter_test/flutter_test.dart';

// Import the controller and its state classes
import '../../../../../lib/features/wardrobe/presentation/controllers/wardrobe_controller.dart';

/// Main test suite for wardrobe controller core functionality
/// Testing basic operations, state management, and controller behavior
void main() {
  group('WardrobeController Core Tests', () {
    test('WardrobeLoading state should be properly initialized', () {
      // Test loading state initialization
      const loadingState = WardrobeLoading();
      
      expect(loadingState, isA<WardrobeState>());
      expect(loadingState, isA<WardrobeLoading>());
      expect(loadingState.toString(), contains('WardrobeLoading'));
    });
    
    test('WardrobeError state should store error messages correctly', () {
      // Test error state functionality
      const errorMessage = 'Failed to load wardrobe items';
      const errorState = WardrobeError(message: errorMessage);
      
      expect(errorState, isA<WardrobeState>());
      expect(errorState, isA<WardrobeError>());
      expect(errorState.message, equals(errorMessage));
      expect(errorState.toString(), isNotEmpty); // Contains class name
    });
    
    test('WardrobeSuccess state should handle items correctly', () {
      // Test success state with different item scenarios
      const successStateEmpty = WardrobeSuccess(items: []);
      
      expect(successStateEmpty, isA<WardrobeState>());
      expect(successStateEmpty, isA<WardrobeSuccess>());
      expect(successStateEmpty.items, isEmpty);
      expect(successStateEmpty.isLoadingMore, isFalse);
      expect(successStateEmpty.hasMore, isTrue); // Default is true
    });
    
    test('WardrobeSuccess should handle pagination states', () {
      // Test pagination functionality
      const paginatingState = WardrobeSuccess(
        items: [],
        isLoadingMore: true,
        hasMore: true,
      );
      
      expect(paginatingState.isLoadingMore, isTrue);
      expect(paginatingState.hasMore, isTrue);
      expect(paginatingState.items, isEmpty);
    });
    
    test('State equality should work correctly', () {
      // Test state equality and comparison
      const loading1 = WardrobeLoading();
      const loading2 = WardrobeLoading();
      
      const error1 = WardrobeError(message: 'Same error');
      const error2 = WardrobeError(message: 'Same error');
      const error3 = WardrobeError(message: 'Different error');
      
      expect(loading1, equals(loading2));
      expect(error1, equals(error2));
      expect(error1, isNot(equals(error3)));
      expect(loading1, isNot(equals(error1)));
    });
    
    test('State hashCode should be consistent', () {
      // Test hashCode consistency for state objects
      const loading1 = WardrobeLoading();
      const loading2 = WardrobeLoading();
      
      expect(loading1.hashCode, equals(loading2.hashCode));
      
      const error1 = WardrobeError(message: 'Test');
      const error2 = WardrobeError(message: 'Test');
      
      expect(error1.hashCode, equals(error2.hashCode));
    });
  });
  
  group('WardrobeController State Transitions', () {
    test('Should support all state types', () {
      // Test that all state types are supported
      const states = <WardrobeState>[
        WardrobeLoading(),
        WardrobeError(message: 'Test error'),
        WardrobeSuccess(items: []),
      ];
      
      for (final state in states) {
        expect(state, isA<WardrobeState>());
        expect(state.toString(), isNotEmpty);
      }
    });
    
    test('States should have proper type hierarchy', () {
      // Test type hierarchy
      const loading = WardrobeLoading();
      const error = WardrobeError(message: 'Type test');
      const success = WardrobeSuccess(items: []);
      
      expect(loading, isA<WardrobeState>());
      expect(error, isA<WardrobeState>());
      expect(success, isA<WardrobeState>());
      
      expect(loading, isNot(isA<WardrobeError>()));
      expect(error, isNot(isA<WardrobeSuccess>()));
      expect(success, isNot(isA<WardrobeLoading>()));
    });
  });
  
  group('WardrobeController Edge Cases', () {
    test('Should handle empty error messages', () {
      // Test edge case with empty error message
      const emptyError = WardrobeError(message: '');
      
      expect(emptyError.message, isEmpty);
      expect(emptyError, isA<WardrobeError>());
    });
    
    test('Should handle success state variations', () {
      // Test different success state configurations
      const defaultSuccess = WardrobeSuccess(items: []);
      const loadingMoreSuccess = WardrobeSuccess(
        items: [],
        isLoadingMore: true,
      );
      const hasMoreSuccess = WardrobeSuccess(
        items: [],
        hasMore: true,
      );
      
      expect(defaultSuccess.isLoadingMore, isFalse);
      expect(loadingMoreSuccess.isLoadingMore, isTrue);
      expect(hasMoreSuccess.hasMore, isTrue);
    });
  });
}
