import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:dartz/dartz.dart';
import 'package:aura_app/features/ecommerce/domain/repositories/ecommerce_repository.dart';
import 'package:aura_app/features/ecommerce/domain/usecases/ecommerce_usecases.dart';
import 'package:aura_app/features/ecommerce/domain/entities/product.dart';
import 'package:aura_app/core/error/failures.dart';

// Generate mock classes
@GenerateMocks([EcommerceRepository])
import 'search_products_test.mocks.dart';

void main() {
  late SearchProducts useCase;
  late MockEcommerceRepository mockRepository;

  setUp(() {
    mockRepository = MockEcommerceRepository();
    useCase = SearchProducts(mockRepository);
  });

  group('SearchProducts', () {
    const tQuery = 'test query';
    const tPage = 1;
    const tPageSize = 20;

    const tSearchParams = SearchProductsParams(
      query: tQuery,
      page: tPage,
      pageSize: tPageSize,
    );

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
      tags: ['tag1', 'tag2'],
    );

    final tProductSearchResult = ProductSearchResult(
      products: [tProduct],
      totalCount: 1,
      page: 1,
      pageSize: 20,
      totalPages: 1,
    );

    test('should get products from repository when called', () async {
      // Arrange
      when(mockRepository.searchProducts(
        query: anyNamed('query'),
        filters: anyNamed('filters'),
        page: anyNamed('page'),
        pageSize: anyNamed('pageSize'),
      )).thenAnswer((_) async => Right(tProductSearchResult));

      // Act
      final result = await useCase(tSearchParams);

      // Assert
      expect(result, Right(tProductSearchResult));
      verify(mockRepository.searchProducts(
        query: tQuery,
        filters: null,
        page: tPage,
        pageSize: tPageSize,
      ));
      verifyNoMoreInteractions(mockRepository);
    });

    test('should return failure when repository call fails', () async {
      // Arrange
      final tFailure = ServerFailure(message: 'Server error');
      when(mockRepository.searchProducts(
        query: anyNamed('query'),
        filters: anyNamed('filters'),
        page: anyNamed('page'),
        pageSize: anyNamed('pageSize'),
      )).thenAnswer((_) async => Left(tFailure));

      // Act
      final result = await useCase(tSearchParams);

      // Assert
      expect(result, Left(tFailure));
      verify(mockRepository.searchProducts(
        query: tQuery,
        filters: null,
        page: tPage,
        pageSize: tPageSize,
      ));
    });

    test('should call repository with correct parameters when no optional params provided', () async {
      // Arrange
      const tMinimalParams = SearchProductsParams(query: tQuery);
      when(mockRepository.searchProducts(
        query: anyNamed('query'),
        filters: anyNamed('filters'),
        page: anyNamed('page'),
        pageSize: anyNamed('pageSize'),
      )).thenAnswer((_) async => Right(tProductSearchResult));

      // Act
      await useCase(tMinimalParams);

      // Assert
      verify(mockRepository.searchProducts(
        query: tQuery,
        filters: null,
        page: 1,
        pageSize: 20,
      ));
    });
  });
}
