import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../../../../core/usecases/usecase.dart';
import '../entities/product.dart';
import '../repositories/ecommerce_repository.dart';

/// Parameters for searching products
class SearchProductsParams {
  final String query;
  final ProductFilter? filters;
  final int page;
  final int pageSize;

  const SearchProductsParams({
    required this.query,
    this.filters,
    this.page = 1,
    this.pageSize = 20,
  });
}

/// Use case for searching products
class SearchProducts implements UseCase<ProductSearchResult, SearchProductsParams> {
  final EcommerceRepository repository;

  SearchProducts(this.repository);

  @override
  Future<Either<Failure, ProductSearchResult>> call(SearchProductsParams params) async {
    return await repository.searchProducts(
      query: params.query,
      filters: params.filters,
      page: params.page,
      pageSize: params.pageSize,
    );
  }
}

/// Parameters for getting a product by ID
class GetProductByIdParams {
  final String productId;

  const GetProductByIdParams({required this.productId});
}

/// Use case for getting a product by ID
class GetProductById implements UseCase<Product?, GetProductByIdParams> {
  final EcommerceRepository repository;

  GetProductById(this.repository);

  @override
  Future<Either<Failure, Product?>> call(GetProductByIdParams params) async {
    return await repository.getProductById(params.productId);
  }
}

/// Parameters for getting trending products
class GetTrendingProductsParams {
  final String? category;
  final String timePeriod;
  final int page;
  final int pageSize;

  const GetTrendingProductsParams({
    this.category,
    this.timePeriod = 'week',
    this.page = 1,
    this.pageSize = 20,
  });
}

/// Use case for getting trending products
class GetTrendingProducts implements UseCase<ProductSearchResult, GetTrendingProductsParams> {
  final EcommerceRepository repository;

  GetTrendingProducts(this.repository);

  @override
  Future<Either<Failure, ProductSearchResult>> call(GetTrendingProductsParams params) async {
    return await repository.getTrendingProducts(
      category: params.category,
      timePeriod: params.timePeriod,
      page: params.page,
      pageSize: params.pageSize,
    );
  }
}

/// Parameters for getting product recommendations
class GetProductRecommendationsParams {
  final String? productId;
  final String? category;
  final List<String>? tags;
  final int limit;

  const GetProductRecommendationsParams({
    this.productId,
    this.category,
    this.tags,
    this.limit = 10,
  });
}

/// Use case for getting product recommendations
class GetProductRecommendations implements UseCase<List<Product>, GetProductRecommendationsParams> {
  final EcommerceRepository repository;

  GetProductRecommendations(this.repository);

  @override
  Future<Either<Failure, List<Product>>> call(GetProductRecommendationsParams params) async {
    return await repository.getProductRecommendations(
      productId: params.productId,
      category: params.category,
      tags: params.tags,
      limit: params.limit,
    );
  }
}

/// Parameters for getting products by category
class GetProductsByCategoryParams {
  final String category;
  final ProductFilter? filters;
  final int page;
  final int pageSize;

  const GetProductsByCategoryParams({
    required this.category,
    this.filters,
    this.page = 1,
    this.pageSize = 20,
  });
}

/// Use case for getting products by category
class GetProductsByCategory implements UseCase<ProductSearchResult, GetProductsByCategoryParams> {
  final EcommerceRepository repository;

  GetProductsByCategory(this.repository);

  @override
  Future<Either<Failure, ProductSearchResult>> call(GetProductsByCategoryParams params) async {
    return await repository.getProductsByCategory(
      category: params.category,
      filters: params.filters,
      page: params.page,
      pageSize: params.pageSize,
    );
  }
}

/// Use case for getting available categories
class GetCategories implements UseCase<List<String>, NoParams> {
  final EcommerceRepository repository;

  GetCategories(this.repository);

  @override
  Future<Either<Failure, List<String>>> call(NoParams params) async {
    return await repository.getCategories();
  }
}

/// Parameters for getting brands
class GetBrandsParams {
  final String? category;

  const GetBrandsParams({this.category});
}

/// Use case for getting brands
class GetBrands implements UseCase<List<String>, GetBrandsParams> {
  final EcommerceRepository repository;

  GetBrands(this.repository);

  @override
  Future<Either<Failure, List<String>>> call(GetBrandsParams params) async {
    return await repository.getBrands(category: params.category);
  }
}
