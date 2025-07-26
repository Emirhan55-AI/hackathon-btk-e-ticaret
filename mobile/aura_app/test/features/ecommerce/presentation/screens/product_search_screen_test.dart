import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:aura_app/features/ecommerce/presentation/screens/product_search_screen.dart';
import 'package:aura_app/features/ecommerce/presentation/notifiers/product_search_notifier.dart';
import 'package:aura_app/features/ecommerce/presentation/notifiers/product_search_state.dart';
import 'package:aura_app/features/ecommerce/domain/entities/product.dart';
import 'package:aura_app/core/providers/app_providers.dart';
import 'package:aura_app/core/error/failures.dart';

// Generate mock classes
@GenerateMocks([ProductSearchNotifier])
import 'product_search_screen_test.mocks.dart';

void main() {
  late MockProductSearchNotifier mockNotifier;

  setUp(() {
    mockNotifier = MockProductSearchNotifier();
  });

  group('ProductSearchScreen Widget Tests', () {
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
        ProductImage(id: '1', url: 'https://example.com/image.jpg', altText: 'Image'),
      ],
    );

    final tNetworkFailure = NetworkFailure(message: 'Test error');

    Widget createWidgetUnderTest({String? initialQuery, String? category}) {
      return ProviderScope(
        overrides: [
          productSearchNotifierProvider.overrideWith((ref) => mockNotifier),
        ],
        child: MaterialApp(
          home: ProductSearchScreen(
            initialQuery: initialQuery,
            category: category,
          ),
        ),
      );
    }

    testWidgets('should display search bar', (WidgetTester tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(const ProductSearchState());

      // Act
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.byType(TextField), findsOneWidget);
      expect(find.text('Search products...'), findsOneWidget);
    });

    testWidgets('should display initial query in search field', (WidgetTester tester) async {
      // Arrange
      const initialQuery = 'test query';
      when(mockNotifier.state).thenReturn(const ProductSearchState());

      // Act
      await tester.pumpWidget(createWidgetUnderTest(initialQuery: initialQuery));

      // Assert
      expect(find.text(initialQuery), findsOneWidget);
    });

    testWidgets('should display loading indicator when isLoading is true', (WidgetTester tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(const ProductSearchState(isLoading: true));

      // Act
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('should display error message when error exists', (WidgetTester tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(ProductSearchState(
        hasError: true,
        error: tNetworkFailure,
      ));

      // Act
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.text('Test error'), findsOneWidget);
      expect(find.text('Retry'), findsOneWidget);
    });

    testWidgets('should display empty state when no products found', (WidgetTester tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(const ProductSearchState(
        products: [],
        searchQuery: 'test',
      ));

      // Act
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.text('No products found'), findsOneWidget);
      expect(find.text('Try adjusting your search or filters'), findsOneWidget);
    });

    testWidgets('should display products when loaded', (WidgetTester tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(ProductSearchState(
        products: [tProduct],
        searchQuery: 'test',
      ));

      // Act
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.text('Test Product'), findsOneWidget);
      expect(find.text('\$50.0'), findsOneWidget);
    });

    testWidgets('should display grid/list toggle buttons', (WidgetTester tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(const ProductSearchState());

      // Act
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.byIcon(Icons.grid_view), findsOneWidget);
      expect(find.byIcon(Icons.list), findsOneWidget);
    });

    testWidgets('should display filter and sort buttons', (WidgetTester tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(const ProductSearchState());

      // Act
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.byIcon(Icons.filter_list), findsOneWidget);
      expect(find.byIcon(Icons.sort), findsOneWidget);
    });

    testWidgets('should call searchProducts when search button is pressed', (WidgetTester tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(const ProductSearchState());
      when(mockNotifier.searchProducts(any)).thenAnswer((_) async => {});

      // Act
      await tester.pumpWidget(createWidgetUnderTest());
      
      // Enter text in search field
      await tester.enterText(find.byType(TextField), 'test query');
      await tester.testTextInput.receiveAction(TextInputAction.search);
      await tester.pump();

      // Assert
      verify(mockNotifier.searchProducts('test query')).called(1);
    });

    testWidgets('should show search suggestion when no input', (WidgetTester tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(const ProductSearchState());

      // Act
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.text('Start typing to search for products'), findsOneWidget);
    });

    testWidgets('should display product count when products are loaded', (WidgetTester tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(ProductSearchState(
        products: [tProduct],
        totalCount: 100,
        searchQuery: 'test',
      ));

      // Act
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.textContaining('100'), findsOneWidget);
    });

    testWidgets('should trigger loadMoreProducts when scrolled to bottom', (WidgetTester tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(ProductSearchState(
        products: List.generate(10, (index) => tProduct.copyWith(id: index.toString())),
        searchQuery: 'test',
        currentPage: 1,
        totalPages: 2,
      ));
      when(mockNotifier.loadMoreProducts()).thenAnswer((_) async => {});

      // Act
      await tester.pumpWidget(createWidgetUnderTest());
      
      // Scroll to bottom
      await tester.drag(find.byType(GridView), const Offset(0, -1000));
      await tester.pump();

      // Assert
      verify(mockNotifier.loadMoreProducts()).called(1);
    });
  });
}
