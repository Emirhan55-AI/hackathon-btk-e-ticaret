import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:dartz/dartz.dart';
import 'package:aura_app/features/ecommerce/domain/usecases/ecommerce_usecases.dart';
import 'package:aura_app/features/ecommerce/domain/entities/product.dart';
import 'package:aura_app/features/ecommerce/presentation/notifiers/product_detail_notifier.dart';
import 'package:aura_app/features/ecommerce/presentation/notifiers/product_detail_state.dart';
import 'package:aura_app/core/error/failures.dart';

// Generate mock classes
@GenerateMocks([GetProductById])
import 'product_detail_notifier_test.mocks.dart';

void main() {
  late ProductDetailNotifier notifier;
  late MockGetProductById mockGetProductById;

  setUp(() {
    mockGetProductById = MockGetProductById();
    notifier = ProductDetailNotifier(getProductById: mockGetProductById);
  });

  group('ProductDetailNotifier', () {
    const tProductId = '1';
    final tProduct = Product(
      id: tProductId,
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
        ProductImage(id: '1', url: 'https://example.com/image1.jpg', altText: 'Image 1'),
        ProductImage(id: '2', url: 'https://example.com/image2.jpg', altText: 'Image 2'),
        ProductImage(id: '3', url: 'https://example.com/image3.jpg', altText: 'Image 3'),
      ],
    );

    test('initial state should be loading false with no product', () {
      // Assert
      expect(notifier.state.isLoading, false);
      expect(notifier.state.product, null);
      expect(notifier.state.error, null);
    });

    test('should set product when setProduct is called', () {
      // Act
      notifier.setProduct(tProduct);

      // Assert
      expect(notifier.state.product, tProduct);
      expect(notifier.state.selectedImageIndex, 0);
      expect(notifier.state.quantity, 1);
      expect(notifier.state.isLoading, false);
    });

    test('should load product successfully when loadProduct is called', () async {
      // Arrange
      when(mockGetProductById(any)).thenAnswer((_) async => Right(tProduct));

      // Act
      await notifier.loadProduct(tProductId);

      // Assert
      expect(notifier.state.isLoading, false);
      expect(notifier.state.product, tProduct);
      expect(notifier.state.error, null);
      verify(mockGetProductById(any));
    });

    test('should update state to loading when loadProduct starts', () async {
      // Arrange
      when(mockGetProductById(any)).thenAnswer((_) async => Right(tProduct));

      // Act
      final future = notifier.loadProduct(tProductId);
      
      // Assert immediate state
      expect(notifier.state.isLoading, true);
      
      // Wait for completion
      await future;
      expect(notifier.state.isLoading, false);
    });

    test('should update state with error when loadProduct fails', () async {
      // Arrange
      final tFailure = ServerFailure(message: 'Server error');
      when(mockGetProductById(any)).thenAnswer((_) async => Left(tFailure));

      // Act
      await notifier.loadProduct(tProductId);

      // Assert
      expect(notifier.state.isLoading, false);
      expect(notifier.state.product, null);
      expect(notifier.state.error, 'Server error');
      verify(mockGetProductById(any));
    });

    test('should select image when selectImage is called', () {
      // Arrange
      notifier.setProduct(tProduct);

      // Act
      notifier.selectImage(2);

      // Assert
      expect(notifier.state.selectedImageIndex, 2);
    });

    test('should update quantity when updateQuantity is called', () {
      // Arrange
      notifier.setProduct(tProduct);

      // Act
      notifier.updateQuantity(5);

      // Assert
      expect(notifier.state.quantity, 5);
    });

    test('should not update quantity below 1', () {
      // Arrange
      notifier.setProduct(tProduct);

      // Act
      notifier.updateQuantity(0);

      // Assert
      expect(notifier.state.quantity, 1);
    });

    test('should toggle favorite status', () {
      // Arrange
      notifier.setProduct(tProduct);
      final initialFavoriteStatus = notifier.state.isFavorite;

      // Act
      notifier.toggleFavorite();

      // Assert
      expect(notifier.state.isFavorite, !initialFavoriteStatus);
    });

    test('should select variant', () {
      // Arrange
      notifier.setProduct(tProduct);

      // Act
      notifier.selectVariant('size', 'L');

      // Assert
      expect(notifier.state.selectedVariants['size'], 'L');
    });

    test('should handle exception during loadProduct', () async {
      // Arrange
      when(mockGetProductById(any)).thenThrow(Exception('Test exception'));

      // Act
      await notifier.loadProduct(tProductId);

      // Assert
      expect(notifier.state.isLoading, false);
      expect(notifier.state.product, null);
      expect(notifier.state.error, contains('An unexpected error occurred'));
    });
  });
}
