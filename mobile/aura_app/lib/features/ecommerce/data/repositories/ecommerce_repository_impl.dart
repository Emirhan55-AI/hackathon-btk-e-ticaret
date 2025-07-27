import 'package:dartz/dartz.dart';
import '../../domain/entities/product.dart';
import '../../domain/repositories/ecommerce_repository.dart';
import '../datasources/ecommerce_remote_data_source.dart';
import '../models/product_model.dart';
import '../../../../core/error/failures.dart';
import '../../../../core/error/exceptions.dart';

/// Implementation of EcommerceRepository
class EcommerceRepositoryImpl implements EcommerceRepository {
  final EcommerceRemoteDataSource remoteDataSource;

  EcommerceRepositoryImpl({
    required this.remoteDataSource,
  });

  @override
  Future<Either<Failure, ProductSearchResult>> searchProducts({
    required String query,
    ProductFilter? filters,
    int page = 1,
    int pageSize = 20,
  }) async {
    try {
      // Convert filter to model if provided
      ProductFilterModel? filterModel;
      if (filters != null) {
        filterModel = ProductFilterModel.fromEntity(filters);
      }

      final result = await remoteDataSource.searchProducts(
        query: query,
        filters: filterModel,
        page: page,
        pageSize: pageSize,
      );

      return Right(result);
    } on ApiException catch (e) {
      return Left(ApiFailure(
        message: e.message,
        details: 'Status code: ${e.statusCode}',
      ));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Unexpected error: $e'));
    }
  }

  @override
  Future<Either<Failure, Product?>> getProductById(String productId) async {
    try {
      final result = await remoteDataSource.getProductById(productId);
      return Right(result);
    } on ApiException catch (e) {
      return Left(ApiFailure(
        message: e.message,
        details: 'Status code: ${e.statusCode}',
      ));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Unexpected error: $e'));
    }
  }

  @override
  Future<Either<Failure, ProductSearchResult>> getTrendingProducts({
    String? category,
    String timePeriod = 'week',
    int page = 1,
    int pageSize = 20,
  }) async {
    try {
      final result = await remoteDataSource.getTrendingProducts(
        category: category,
        timePeriod: timePeriod,
        page: page,
        pageSize: pageSize,
      );

      return Right(result);
    } on ApiException catch (e) {
      return Left(ApiFailure(
        message: e.message,
        details: 'Status code: ${e.statusCode}',
      ));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Unexpected error: $e'));
    }
  }

  @override
  Future<Either<Failure, List<Product>>> getProductRecommendations({
    String? productId,
    String? category,
    List<String>? tags,
    int limit = 10,
  }) async {
    try {
      final result = await remoteDataSource.getProductRecommendations(
        productId: productId,
        category: category,
        tags: tags,
        limit: limit,
      );

      // Convert models to entities
      final products = result.map((model) => model as Product).toList();
      return Right(products);
    } on ApiException catch (e) {
      return Left(ApiFailure(
        message: e.message,
        details: 'Status code: ${e.statusCode}',
      ));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Unexpected error: $e'));
    }
  }

  @override
  Future<Either<Failure, ProductSearchResult>> getProductsByCategory({
    required String category,
    ProductFilter? filters,
    int page = 1,
    int pageSize = 20,
  }) async {
    try {
      // Convert filter to model if provided
      ProductFilterModel? filterModel;
      if (filters != null) {
        filterModel = ProductFilterModel.fromEntity(filters);
      }

      final result = await remoteDataSource.getProductsByCategory(
        category: category,
        filters: filterModel,
        page: page,
        pageSize: pageSize,
      );

      return Right(result);
    } on ApiException catch (e) {
      return Left(ApiFailure(
        message: e.message,
        details: 'Status code: ${e.statusCode}',
      ));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Unexpected error: $e'));
    }
  }

  @override
  Future<Either<Failure, List<String>>> getCategories() async {
    try {
      final result = await remoteDataSource.getCategories();
      return Right(result);
    } on ApiException catch (e) {
      return Left(ApiFailure(
        message: e.message,
        details: 'Status code: ${e.statusCode}',
      ));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Unexpected error: $e'));
    }
  }

  @override
  Future<Either<Failure, List<String>>> getBrands({String? category}) async {
    try {
      final result = await remoteDataSource.getBrands(category: category);
      return Right(result);
    } on ApiException catch (e) {
      return Left(ApiFailure(
        message: e.message,
        details: 'Status code: ${e.statusCode}',
      ));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Unexpected error: $e'));
    }
  }
}
