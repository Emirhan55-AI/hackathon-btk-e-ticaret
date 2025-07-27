// Unit tests for WardrobeController - Comprehensive Phase 3 test coverage
// Tests all state management operations and business logic for wardrobe feature
// Ensures proper error handling, state transitions, and data management for 100% Phase 3 completion

import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:dartz/dartz.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../../lib/features/wardrobe/presentation/controllers/wardrobe_controller.dart';
import '../../../../../lib/features/wardrobe/domain/entities/clothing_item.dart';
import '../../../../../lib/features/wardrobe/domain/usecases/get_clothing_items.dart';
import '../../../../../lib/features/wardrobe/domain/usecases/add_clothing_item.dart';
import '../../../../../lib/features/wardrobe/domain/usecases/update_clothing_item.dart';
import '../../../../../lib/features/wardrobe/domain/usecases/delete_clothing_item.dart';
import '../../../../../lib/core/error/failures.dart';
import '../../../../../lib/core/usecases/usecase.dart';
import '../../../../../lib/features/wardrobe/wardrobe_injection.dart' as injection;

// Mock classes for testing dependencies - manual implementation to avoid build_runner issues
class MockGetClothingItems extends Mock implements GetClothingItems {}
class MockAddClothingItem extends Mock implements AddClothingItem {}
class MockUpdateClothingItem extends Mock implements UpdateClothingItem {}
class MockDeleteClothingItem extends Mock implements DeleteClothingItem {}

void main() {
  // Main test group for comprehensive wardrobe controller testing
  group('WardrobeController - Phase 3 Comprehensive Tests', () {
    // Test dependencies - mock objects to simulate external services
    late MockGetClothingItems mockGetClothingItems;
    late MockAddClothingItem mockAddClothingItem;
    late MockUpdateClothingItem mockUpdateClothingItem;
    late MockDeleteClothingItem mockDeleteClothingItem;
    late ProviderContainer container;

    // Test data - sample clothing items for testing various scenarios
    final testClothingItem1 = ClothingItem(
      id: 'test-id-1',
      userId: 'user-1',
      name: 'Blue Cotton Shirt',
      category: 'Tops',
      subcategory: 'Shirts',
      color: 'Blue',
      brand: 'Test Brand',
      size: 'M',
      material: 'Cotton',
      style: 'Casual',
      pattern: 'Solid',
      fit: 'Regular',
      occasions: ['Casual', 'Work'],
      seasons: ['Spring', 'Summer'],
      imageUrl: 'https://example.com/blue-shirt.jpg',
      aiTags: {'style': 'casual', 'color_confidence': 0.95},
      userTags: {'favorite': true},
      description: 'Comfortable blue shirt for daily wear',
      isFavorite: true,
      purchasePrice: 29.99,
      purchaseDate: DateTime(2024, 1, 15),
      notes: 'Great for work meetings',
      tags: ['professional', 'comfortable'],
      price: 29.99,
      createdAt: DateTime(2024, 1, 15),
      updatedAt: DateTime(2024, 1, 15),
    );

    final testClothingItem2 = ClothingItem(
      id: 'test-id-2',
      userId: 'user-1',
      name: 'Black Formal Pants',
      category: 'Bottoms',
      subcategory: 'Trousers',
      color: 'Black',
      brand: 'Formal Wear Co',
      size: 'L',
      material: 'Wool Blend',
      style: 'Formal',
      pattern: 'Solid',
      fit: 'Slim',
      occasions: ['Work', 'Formal'],
      seasons: ['Fall', 'Winter'],
      imageUrl: 'https://example.com/black-pants.jpg',
      aiTags: {'style': 'formal', 'color_confidence': 0.98},
      userTags: {'workwear': true},
      description: 'Professional black pants for formal occasions',
      isFavorite: false,
      purchasePrice: 89.99,
      purchaseDate: DateTime(2024, 2, 1),
      notes: 'Perfect for business meetings',
      tags: ['professional', 'formal'],
      price: 89.99,
      createdAt: DateTime(2024, 2, 1),
      updatedAt: DateTime(2024, 2, 1),
    );

    // Setup method - initializes all mock objects and test container before each test
    setUp(() {
      // Create fresh mock instances for isolated testing
      mockGetClothingItems = MockGetClothingItems();
      mockAddClothingItem = MockAddClothingItem();
      mockUpdateClothingItem = MockUpdateClothingItem();
      mockDeleteClothingItem = MockDeleteClothingItem();

      // Create provider container with dependency overrides for testing
      container = ProviderContainer(
        overrides: [
          // Override production providers with mock implementations
          getClothingItemsProvider.overrideWithValue(mockGetClothingItems),
          addClothingItemProvider.overrideWithValue(mockAddClothingItem),
          updateClothingItemProvider.overrideWithValue(mockUpdateClothingItem),
          deleteClothingItemProvider.overrideWithValue(mockDeleteClothingItem),
        ],
      );
    });

    // Cleanup method - disposes resources after each test to prevent memory leaks
    tearDown(() {
      container.dispose();
    });

    // Test: Controller initialization and initial state verification
    test('should initialize with loading state', () {
      // When: Reading the initial controller state
      final state = container.read(wardrobeControllerProvider);
      
      // Then: State should be WardrobeLoading initially
      expect(state, isA<WardrobeLoading>());
    });

    // Test: Successful clothing items loading scenario
    test('should load clothing items successfully', () async {
      // Given: Mock returns successful result with test data
      final testItems = [testClothingItem1, testClothingItem2];
      when(mockGetClothingItems.call(NoParams())).thenAnswer(
        (_) async => Right(testItems),
      );

      // When: Controller loads clothing items
      final controller = container.read(wardrobeControllerProvider.notifier);
      await controller.loadClothingItems();

      // Then: State should contain the loaded items
      final state = container.read(wardrobeControllerProvider);
      expect(state, isA<WardrobeSuccess>());
      final successState = state as WardrobeSuccess;
      expect(successState.items, equals(testItems));
      expect(successState.items.length, equals(2));

      // Verify that the use case was called exactly once
      verify(mockGetClothingItems.call(NoParams())).called(1);
    });

    // Test: Failed clothing items loading scenario  
    test('should handle loading failure with proper error state', () async {
      // Given: Mock returns failure result
      const failure = ServerFailure();
      when(mockGetClothingItems.call(NoParams())).thenAnswer(
        (_) async => Left(failure),
      );

      // When: Controller attempts to load items but fails
      final controller = container.read(wardrobeControllerProvider.notifier);
      await controller.loadClothingItems();

      // Then: State should contain error information
      final state = container.read(wardrobeControllerProvider);
      expect(state, isA<WardrobeError>());
      final errorState = state as WardrobeError;
      expect(errorState.message, contains('failed'));

      // Verify that the use case was called
      verify(mockGetClothingItems.call(NoParams())).called(1);
    });

    // Test: Successful clothing item addition scenario
    test('should add clothing item successfully and reload list', () async {
      // Given: Mock returns successful addition and updated list
      final newItem = testClothingItem1;
      when(mockAddClothingItem.call(AddClothingItemParams(clothingItem: newItem))).thenAnswer(
        (_) async => Right(newItem),
      );
      when(mockGetClothingItems.call(NoParams())).thenAnswer(
        (_) async => Right([newItem]),
      );

      // When: Controller adds a new clothing item
      final controller = container.read<WardrobeController>(wardrobeControllerProvider.notifier);
      await controller.addClothingItem(newItem);

      // Then: Item should be added and list reloaded
      verify(mockAddClothingItem.call(AddClothingItemParams(clothingItem: newItem))).called(1);
      verify(mockGetClothingItems.call(NoParams())).called(1);
    });

    // Test: Failed clothing item addition scenario
    test('should handle clothing item addition failure', () async {
      // Given: Mock returns failure for addition
      const failure = ServerFailure();
      when(mockAddClothingItem.call(AddClothingItemParams(clothingItem: testClothingItem1))).thenAnswer(
        (_) async => Left(failure),
      );

      // When: Controller attempts to add item but fails
      final controller = container.read<WardrobeController>(wardrobeControllerProvider.notifier);
      await controller.addClothingItem(testClothingItem1);

      // Then: Addition should be attempted but fail
      verify(mockAddClothingItem.call(AddClothingItemParams(clothingItem: testClothingItem1))).called(1);
      // Verify that reload is not called when addition fails
      verifyNever(mockGetClothingItems.call(NoParams()));
    });

    // Test: Successful clothing item update scenario
    test('should update clothing item successfully and reload list', () async {
      // Given: Mock returns successful update and updated list
      final updatedItem = testClothingItem1.copyWith(
        name: 'Updated Blue Shirt',
        isFavorite: false,
      );
      when(mockUpdateClothingItem.call(UpdateClothingItemParams(updatedItem: updatedItem))).thenAnswer(
        (_) async => Right(updatedItem),
      );
      when(mockGetClothingItems.call(NoParams())).thenAnswer(
        (_) async => Right([updatedItem]),
      );

      // When: Controller updates the clothing item
      final controller = container.read<WardrobeController>(wardrobeControllerProvider.notifier);
      await controller.updateClothingItem(updatedItem);

      // Then: Item should be updated and list reloaded
      verify(mockUpdateClothingItem.call(UpdateClothingItemParams(updatedItem: updatedItem))).called(1);
      verify(mockGetClothingItems.call(NoParams())).called(1);
    });

    // Test: Successful clothing item deletion scenario
    test('should delete clothing item successfully and reload list', () async {
      // Given: Mock returns successful deletion and empty list
      const itemId = 'test-id-1';
      when(mockDeleteClothingItem.call(DeleteClothingItemParams(itemId: itemId))).thenAnswer(
        (_) async => const Right(null),
      );
      when(mockGetClothingItems.call(NoParams())).thenAnswer(
        (_) async => const Right([]),
      );

      // When: Controller deletes the clothing item
      final controller = container.read<WardrobeController>(wardrobeControllerProvider.notifier);
      await controller.deleteClothingItem(itemId);

      // Then: Item should be deleted and list reloaded
      verify(mockDeleteClothingItem.call(DeleteClothingItemParams(itemId: itemId))).called(1);
      verify(mockGetClothingItems.call(NoParams())).called(1);
    });

    // Test: Failed clothing item deletion scenario
    test('should handle clothing item deletion failure', () async {
      // Given: Mock returns deletion failure
      const itemId = 'test-id-1';
      const failure = ServerFailure();
      when(mockDeleteClothingItem.call(DeleteClothingItemParams(itemId: itemId))).thenAnswer(
        (_) async => Left(failure),
      );

      // When: Controller attempts to delete item but fails
      final controller = container.read<WardrobeController>(wardrobeControllerProvider.notifier);
      await controller.deleteClothingItem(itemId);

      // Then: Deletion should be attempted but fail
      verify(mockDeleteClothingItem.call(DeleteClothingItemParams(itemId: itemId))).called(1);
      // Verify that reload is not called when deletion fails
      verifyNever(mockGetClothingItems.call(NoParams()));
    });

    // Test: Filter by category functionality
    test('should filter clothing items by category correctly', () async {
      // Given: Multiple items with different categories loaded
      final allItems = [testClothingItem1, testClothingItem2];
      when(mockGetClothingItems.call(NoParams())).thenAnswer(
        (_) async => Right(allItems),
      );

      // When: Controller loads items and applies category filter
      final controller = container.read(wardrobeControllerProvider.notifier);
      await controller.loadClothingItems();
      controller.filterByCategory('Tops');

      // Then: Only items with matching category should be visible
      final state = container.read(wardrobeControllerProvider);
      expect(state, isA<WardrobeSuccess>());
      final successState = state as WardrobeSuccess;
      expect(successState.items.length, equals(1));
      expect(successState.items.first.category, equals('Tops'));
      expect(successState.items.first.name, equals('Blue Cotton Shirt'));
    });

    // Test: Search items by name functionality
    test('should search clothing items by name correctly', () async {
      // Given: Multiple items with different names loaded
      final allItems = [testClothingItem1, testClothingItem2];
      when(mockGetClothingItems.call(NoParams())).thenAnswer(
        (_) async => Right(allItems),
      );

      // When: Controller loads items and applies search filter
      final controller = container.read(wardrobeControllerProvider.notifier);
      await controller.loadClothingItems();
      controller.searchItems('Blue');

      // Then: Only items matching search term should be visible
      final state = container.read(wardrobeControllerProvider);
      expect(state, isA<WardrobeSuccess>());
      final successState = state as WardrobeSuccess;
      expect(successState.items.length, equals(1));
      expect(successState.items.first.name, contains('Blue'));
    });

    // Test: Clear all filters functionality
    test('should clear all filters and show all items', () async {
      // Given: Items are loaded and filter is applied
      final allItems = [testClothingItem1, testClothingItem2];
      when(mockGetClothingItems.call(NoParams())).thenAnswer(
        (_) async => Right(allItems),
      );

      // When: Controller applies filter then clears it
      final controller = container.read(wardrobeControllerProvider.notifier);
      await controller.loadClothingItems();
      controller.filterByCategory('Tops'); // Apply filter first
      controller.clearFilters(); // Then clear filters

      // Then: All items should be visible again
      final state = container.read(wardrobeControllerProvider);
      expect(state, isA<WardrobeSuccess>());
      final successState = state as WardrobeSuccess;
      expect(successState.items.length, equals(2)); // All items should be visible
    });

    // Test: Multiple filter operations
    test('should handle multiple filter operations correctly', () async {
      // Given: Multiple items with various properties
      final allItems = [testClothingItem1, testClothingItem2];
      when(mockGetClothingItems.call(NoParams())).thenAnswer(
        (_) async => Right(allItems),
      );

      // When: Controller applies multiple filters in sequence
      final controller = container.read(wardrobeControllerProvider.notifier);
      await controller.loadClothingItems();
      
      // Apply category filter
      controller.filterByCategory('Bottoms');
      final afterCategoryFilter = container.read(wardrobeControllerProvider);
      expect(afterCategoryFilter, isA<WardrobeSuccess>());
      expect((afterCategoryFilter as WardrobeSuccess).items.length, equals(1));
      
      // Apply search filter on top of category filter
      controller.searchItems('Formal');
      final afterSearchFilter = container.read(wardrobeControllerProvider);
      expect(afterSearchFilter, isA<WardrobeSuccess>());
      expect((afterSearchFilter as WardrobeSuccess).items.length, equals(1));
      expect((afterSearchFilter as WardrobeSuccess).items.first.name, contains('Formal'));
    });

    // Test: Error handling during filter operations
    test('should handle errors gracefully during filter operations', () async {
      // Given: Initial loading fails
      const failure = ServerFailure();
      when(mockGetClothingItems.call(NoParams())).thenAnswer(
        (_) async => Left(failure),
      );

      // When: Controller attempts to load and filter
      final controller = container.read(wardrobeControllerProvider.notifier);
      await controller.loadClothingItems();
      controller.filterByCategory('Tops'); // Should not crash

      // Then: State should still contain error
      final state = container.read(wardrobeControllerProvider);
      expect(state, isA<WardrobeError>());
    });

    // Test: State persistence across operations
    test('should maintain state consistency across multiple operations', () async {
      // Given: Successful initial load
      final initialItems = [testClothingItem1];
      when(mockGetClothingItems.call(NoParams())).thenAnswer(
        (_) async => Right(initialItems),
      );

      // When: Performing multiple operations
      final controller = container.read(wardrobeControllerProvider.notifier);
      await controller.loadClothingItems();
      
      // Verify initial state
      final initialState = container.read(wardrobeControllerProvider);
      expect(initialState, isA<WardrobeSuccess>());
      expect((initialState as WardrobeSuccess).items.length, equals(1));

      // Add new item
      when(mockAddClothingItem.call(AddClothingItemParams(item: testClothingItem2))).thenAnswer(
        (_) async => Right(testClothingItem2),
      );
      when(mockGetClothingItems.call(NoParams())).thenAnswer(
        (_) async => Right([testClothingItem1, testClothingItem2]),
      );
      
      await controller.addClothingItem(testClothingItem2);

      // Then: State should be updated correctly
      final finalState = container.read(wardrobeControllerProvider);
      expect(finalState, isA<WardrobeSuccess>());
      expect((finalState as WardrobeSuccess).items.length, equals(2));
    });
  });
}
