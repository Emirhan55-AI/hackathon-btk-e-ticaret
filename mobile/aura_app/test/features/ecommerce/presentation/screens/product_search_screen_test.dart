import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:aura_app/features/ecommerce/presentation/screens/product_search_screen.dart';
import 'package:aura_app/features/ecommerce/presentation/notifiers/product_search_notifier.dart';
import 'package:aura_app/features/ecommerce/presentation/notifiers/product_search_state.dart';
import 'package:aura_app/features/ecommerce/domain/entities/product.dart';
import 'package:aura_app/core/providers/app_providers.dart';
import 'package:aura_app/core/error/failures.dart';
import 'package:aura_app/features/ecommerce/domain/usecases/ecommerce_usecases.dart';
import 'package:aura_app/features/ecommerce/domain/repositories/ecommerce_repository.dart';
import 'package:aura_app/core/usecases/usecase.dart';
import 'package:dartz/dartz.dart';
import 'package:mockito/mockito.dart';

// Mock Repository for testing
class _MockRepository extends Mock implements EcommerceRepository {}

// Method 1: Create a TestProductSearchNotifier using Riverpod's ProviderScope overrides
class TestProductSearchNotifier extends ProductSearchNotifier {
  TestProductSearchNotifier({
    ProductSearchState? initialState,
  }) : super(
          // Provide mock use cases with proper repository dependencies
          searchProducts: _MockSearchProducts(_MockRepository()),
          getCategories: _MockGetCategories(_MockRepository()),
          getBrands: _MockGetBrands(_MockRepository()),
        ) {
    // Set initial state if provided
    if (initialState != null) {
      state = initialState;
    }
  }
}

// Mock implementation for SearchProducts use case
class _MockSearchProducts extends SearchProducts {
  _MockSearchProducts(EcommerceRepository repository) : super(repository);

  @override
  Future<Either<Failure, ProductSearchResult>> call(SearchProductsParams params) async {
    // Return a mock successful result for testing
    return const Right(ProductSearchResult(
      products: [],
      totalCount: 0,
      page: 1,
      pageSize: 20,
      totalPages: 1,
    ));
  }
}

// Mock implementation for GetCategories use case
class _MockGetCategories extends GetCategories {
  _MockGetCategories(EcommerceRepository repository) : super(repository);

  @override
  Future<Either<Failure, List<String>>> call(NoParams params) async {
    // Return mock categories for testing
    return const Right(['Electronics', 'Clothing', 'Books']);
  }
}

// Mock implementation for GetBrands use case
class _MockGetBrands extends GetBrands {
  _MockGetBrands(EcommerceRepository repository) : super(repository);

  @override
  Future<Either<Failure, List<String>>> call(GetBrandsParams params) async {
    // Return mock brands for testing
    return const Right(['Brand A', 'Brand B', 'Brand C']);
  }
}

void main() {
  group('ProductSearchScreen Widget Tests - Method 1 Approach', () {
    final tProduct = Product(
      id: '1',
      name: 'Test Product',
      description: 'Test Description',
      price: 50.0,
      currency: 'USD',
      category: 'electronics',
      brand: 'Test Brand',
      rating: 4.5,
      reviewCount: 100,
      stockQuantity: 10,
      images: [
        const ProductImage(
          id: '1', 
          url: 'https://example.com/image.jpg', 
          altText: 'Image',
          isMain: true,
          sortOrder: 0,
        ),
      ],
    );

    final tNetworkFailure = NetworkFailure(message: 'Test error');

    // Method 1: Use ProviderScope overrides with our TestProductSearchNotifier
    Widget createWidgetUnderTest({String? initialQuery, String? category}) {
      return ProviderScope(
        overrides: [
          // Override the provider to return our custom test notifier
          productSearchNotifierProvider.overrideWith((ref) => TestProductSearchNotifier()),
        ],
        child: MaterialApp(
          home: ProductSearchScreen(
            initialQuery: initialQuery,
            category: category,
          ),
        ),
      );
    }

    testWidgets('should display search bar using Method 1', (WidgetTester tester) async {
      // Act
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.byType(TextField), findsOneWidget);
      expect(find.text('Search products...'), findsOneWidget);
    });

    testWidgets('should display initial query in search field using Method 1', (WidgetTester tester) async {
      // Arrange
      const initialQuery = 'test query';

      // Act
      await tester.pumpWidget(createWidgetUnderTest(initialQuery: initialQuery));

      // Assert
      expect(find.text(initialQuery), findsOneWidget);
    });

    testWidgets('should display loading indicator when isLoading is true using Method 1', (WidgetTester tester) async {
      // Act - Create test notifier with loading state
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            productSearchNotifierProvider.overrideWith((ref) => 
              TestProductSearchNotifier(
                initialState: const ProductSearchState(isLoading: true),
              )
            ),
          ],
          child: const MaterialApp(home: ProductSearchScreen()),
        ),
      );

      // Assert
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('should display error message when error exists using Method 1', (WidgetTester tester) async {
      // Act - Create test notifier with error state
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            productSearchNotifierProvider.overrideWith((ref) => 
              TestProductSearchNotifier(
                initialState: ProductSearchState(
                  hasError: true,
                  error: tNetworkFailure,
                ),
              )
            ),
          ],
          child: const MaterialApp(home: ProductSearchScreen()),
        ),
      );

      // Assert
      expect(find.text('Test error'), findsOneWidget);
      expect(find.text('Retry'), findsOneWidget);
    });

    testWidgets('should display empty state when no products found using Method 1', (WidgetTester tester) async {
      // Act - Create test notifier with empty state
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            productSearchNotifierProvider.overrideWith((ref) => 
              TestProductSearchNotifier(
                initialState: const ProductSearchState(
                  products: [],
                  searchQuery: 'test',
                ),
              )
            ),
          ],
          child: const MaterialApp(home: ProductSearchScreen()),
        ),
      );

      // Assert - Use findsAtLeastNWidgets to handle multiple instances
      expect(find.text('No products found'), findsAtLeastNWidgets(1));
      expect(find.text('Try adjusting your search or filters'), findsOneWidget);
    });

    testWidgets('should display products when loaded using Method 1', (WidgetTester tester) async {
      // Act - Create test notifier with products
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            productSearchNotifierProvider.overrideWith((ref) => 
              TestProductSearchNotifier(
                initialState: ProductSearchState(
                  products: [tProduct],
                  searchQuery: 'test',
                ),
              )
            ),
          ],
          child: const MaterialApp(home: ProductSearchScreen()),
        ),
      );

      // Assert - Check product display
      expect(find.text('Test Product'), findsOneWidget);
      expect(find.textContaining('50'), findsAtLeastNWidgets(1));
    });

    testWidgets('should display grid/list toggle buttons using Method 1', (WidgetTester tester) async {
      // Act - Create test with search query to show buttons
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            productSearchNotifierProvider.overrideWith((ref) => 
              TestProductSearchNotifier(
                initialState: ProductSearchState(
                  products: [tProduct],
                  searchQuery: 'test',
                ),
              )
            ),
          ],
          child: const MaterialApp(home: ProductSearchScreen()),
        ),
      );

      // Assert - Check for view toggle button (initially shows list icon since _isGridView = true)
      expect(find.byIcon(Icons.view_list), findsOneWidget);
    });

    testWidgets('should display filter and sort buttons using Method 1', (WidgetTester tester) async {
      // Act - Create test with search query to show buttons
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            productSearchNotifierProvider.overrideWith((ref) => 
              TestProductSearchNotifier(
                initialState: ProductSearchState(
                  products: [tProduct],
                  searchQuery: 'test',
                ),
              )
            ),
          ],
          child: const MaterialApp(home: ProductSearchScreen()),
        ),
      );

      // Assert
      expect(find.byIcon(Icons.filter_list), findsOneWidget);
      expect(find.byIcon(Icons.sort), findsOneWidget);
    });

    testWidgets('should show search suggestion when no input using Method 1', (WidgetTester tester) async {
      // Act - Create test with empty search query
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            productSearchNotifierProvider.overrideWith((ref) => 
              TestProductSearchNotifier(
                initialState: const ProductSearchState(
                  products: [],
                  searchQuery: '',
                ),
              )
            ),
          ],
          child: const MaterialApp(home: ProductSearchScreen()),
        ),
      );

      // Assert - Check for search suggestion
      expect(find.text('Search for products'), findsOneWidget);
      expect(find.text('Enter a product name or browse categories'), findsOneWidget);
    });

    testWidgets('should display product count when products are loaded using Method 1', (WidgetTester tester) async {
      // Act - Create test notifier with products and count
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            productSearchNotifierProvider.overrideWith((ref) => 
              TestProductSearchNotifier(
                initialState: ProductSearchState(
                  products: [tProduct],
                  totalCount: 100,
                  searchQuery: 'test',
                ),
              )
            ),
          ],
          child: const MaterialApp(home: ProductSearchScreen()),
        ),
      );

      // Assert - Use findsAtLeastNWidgets for multiple count instances
      expect(find.textContaining('100'), findsAtLeastNWidgets(1));
    });
  });
}
