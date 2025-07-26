import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:aura_app/features/ecommerce/presentation/screens/product_detail_screen.dart';
import 'package:aura_app/features/ecommerce/presentation/notifiers/product_detail_notifier.dart';
import 'package:aura_app/features/ecommerce/presentation/notifiers/product_detail_state.dart';
import 'package:aura_app/features/ecommerce/domain/entities/product.dart';
import 'package:aura_app/core/providers/app_providers.dart';

// Generate mock classes
@GenerateMocks([ProductDetailNotifier])
import 'product_detail_screen_test.mocks.dart';

void main() {
  late MockProductDetailNotifier mockNotifier;

  setUp(() {
    mockNotifier = MockProductDetailNotifier();
    // Stub the addListener method to prevent MissingStubError
    when(mockNotifier.addListener(any, fireImmediately: anyNamed('fireImmediately')))
        .thenReturn(() {});
    when(mockNotifier.removeListener(any)).thenReturn(() {});
  });

  group('ProductDetailScreen Widget Tests', () {
    const productId = 'test-product-id';
    
    final tProduct = Product(
      id: productId,
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

    Widget createWidgetUnderTest() {
      return ProviderScope(
        overrides: [
          productDetailNotifierProvider.overrideWith((ref) => mockNotifier),
        ],
        child: MaterialApp(
          home: ProductDetailScreen(productId: productId),
        ),
      );
    }

    testWidgets('should display loading indicator when loading', (WidgetTester tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(const ProductDetailState(isLoading: true));

      // Act
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('should display error message when error occurs', (WidgetTester tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(const ProductDetailState(
        error: 'Network error',
      ));

      // Act
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.text('Network error'), findsOneWidget);
      expect(find.text('Retry'), findsOneWidget);
    });

    testWidgets('should display product details when loaded', (WidgetTester tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(ProductDetailState(
        product: tProduct,
        isLoading: false,
      ));

      // Act
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.text('Test Product'), findsOneWidget);
      expect(find.text('Test Description'), findsOneWidget);
      expect(find.text('\$50.0'), findsOneWidget);
      expect(find.text('Test Brand'), findsOneWidget);
    });

    testWidgets('should display product rating', (WidgetTester tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(ProductDetailState(
        product: tProduct,
        isLoading: false,
      ));

      // Act
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.text('4.5'), findsOneWidget);
      expect(find.text('(100 reviews)'), findsOneWidget);
    });

    testWidgets('should display add to cart button', (WidgetTester tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(ProductDetailState(
        product: tProduct,
        isLoading: false,
      ));

      // Act
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.text('Add to Cart'), findsOneWidget);
    });

    testWidgets('should display quantity selector', (WidgetTester tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(ProductDetailState(
        product: tProduct,
        isLoading: false,
        quantity: 1,
      ));

      // Act
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.byIcon(Icons.remove), findsOneWidget);
      expect(find.byIcon(Icons.add), findsOneWidget);
      expect(find.text('1'), findsOneWidget);
    });

    testWidgets('should call addToCart when add to cart button is pressed', (WidgetTester tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(ProductDetailState(
        product: tProduct,
        isLoading: false,
      ));
      when(mockNotifier.addToCart()).thenAnswer((_) async => {});

      // Act
      await tester.pumpWidget(createWidgetUnderTest());
      await tester.tap(find.text('Add to Cart'));
      await tester.pump();

      // Assert
      verify(mockNotifier.addToCart()).called(1);
    });

    testWidgets('should call updateQuantity when quantity buttons are pressed', (WidgetTester tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(ProductDetailState(
        product: tProduct,
        isLoading: false,
        quantity: 2,
      ));

      // Act
      await tester.pumpWidget(createWidgetUnderTest());
      
      // Test increase quantity
      await tester.tap(find.byIcon(Icons.add));
      await tester.pump();
      verify(mockNotifier.updateQuantity(3)).called(1);

      // Test decrease quantity
      await tester.tap(find.byIcon(Icons.remove));
      await tester.pump();
      verify(mockNotifier.updateQuantity(1)).called(1);
    });

    testWidgets('should display image carousel', (WidgetTester tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(ProductDetailState(
        product: tProduct,
        isLoading: false,
      ));

      // Act
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.byType(PageView), findsOneWidget);
    });

    testWidgets('should display share button', (WidgetTester tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(ProductDetailState(
        product: tProduct,
        isLoading: false,
      ));

      // Act
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.byIcon(Icons.share), findsOneWidget);
    });

    testWidgets('should display favorite button', (WidgetTester tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(ProductDetailState(
        product: tProduct,
        isLoading: false,
        isFavorite: false,
      ));

      // Act
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.byIcon(Icons.favorite_border), findsOneWidget);
    });

    testWidgets('should display filled favorite button when product is favorite', (WidgetTester tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(ProductDetailState(
        product: tProduct,
        isLoading: false,
        isFavorite: true,
      ));

      // Act
      await tester.pumpWidget(createWidgetUnderTest());

      // Assert
      expect(find.byIcon(Icons.favorite), findsOneWidget);
    });

    testWidgets('should call toggleFavorite when favorite button is pressed', (WidgetTester tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(ProductDetailState(
        product: tProduct,
        isLoading: false,
        isFavorite: false,
      ));
      when(mockNotifier.toggleFavorite()).thenAnswer((_) async => {});

      // Act
      await tester.pumpWidget(createWidgetUnderTest());
      await tester.tap(find.byIcon(Icons.favorite_border));
      await tester.pump();

      // Assert
      verify(mockNotifier.toggleFavorite()).called(1);
    });
  });
}
