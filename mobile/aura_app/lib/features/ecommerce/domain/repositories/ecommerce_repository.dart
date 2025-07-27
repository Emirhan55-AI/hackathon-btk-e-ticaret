import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../entities/product.dart';

/// Abstract repository interface for e-commerce operations
abstract class EcommerceRepository {
  /// Search for products based on query and filters
  Future<Either<Failure, ProductSearchResult>> searchProducts({
    required String query,
    ProductFilter? filters,
    int page = 1,
    int pageSize = 20,
  });

  /// Get a specific product by ID
  Future<Either<Failure, Product?>> getProductById(String productId);

  /// Get trending/popular products
  Future<Either<Failure, ProductSearchResult>> getTrendingProducts({
    String? category,
    String timePeriod = 'week',
    int page = 1,
    int pageSize = 20,
  });

  /// Get product recommendations based on user preferences or product
  Future<Either<Failure, List<Product>>> getProductRecommendations({
    String? productId,
    String? category,
    List<String>? tags,
    int limit = 10,
  });

  /// Get products by category
  Future<Either<Failure, ProductSearchResult>> getProductsByCategory({
    required String category,
    ProductFilter? filters,
    int page = 1,
    int pageSize = 20,
  });

  /// Get product categories
  Future<Either<Failure, List<String>>> getCategories();

  /// Get brands for a specific category
  Future<Either<Failure, List<String>>> getBrands({String? category});
}
