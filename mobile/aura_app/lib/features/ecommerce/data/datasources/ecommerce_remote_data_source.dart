import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/product_model.dart';
import '../../../../core/error/exceptions.dart';

/// Abstract interface for remote e-commerce data operations
abstract class EcommerceRemoteDataSource {
  /// Search for products
  Future<ProductSearchResultModel> searchProducts({
    required String query,
    ProductFilterModel? filters,
    int page = 1,
    int pageSize = 20,
  });

  /// Get product by ID
  Future<ProductModel?> getProductById(String productId);

  /// Get trending products
  Future<ProductSearchResultModel> getTrendingProducts({
    String? category,
    String timePeriod = 'week',
    int page = 1,
    int pageSize = 20,
  });

  /// Get product recommendations
  Future<List<ProductModel>> getProductRecommendations({
    String? productId,
    String? category,
    List<String>? tags,
    int limit = 10,
  });

  /// Get products by category
  Future<ProductSearchResultModel> getProductsByCategory({
    required String category,
    ProductFilterModel? filters,
    int page = 1,
    int pageSize = 20,
  });

  /// Get available categories
  Future<List<String>> getCategories();

  /// Get brands for category
  Future<List<String>> getBrands({String? category});
}

/// Implementation of remote data source using HTTP client
class EcommerceRemoteDataSourceImpl implements EcommerceRemoteDataSource {
  final http.Client client;
  final String baseUrl;

  EcommerceRemoteDataSourceImpl({
    required this.client,
    this.baseUrl = 'http://localhost:8000/api/v1',
  });

  @override
  Future<ProductSearchResultModel> searchProducts({
    required String query,
    ProductFilterModel? filters,
    int page = 1,
    int pageSize = 20,
  }) async {
    try {
      // Build query parameters
      final Map<String, String> queryParams = {
        'q': query,
        'page': page.toString(),
        'size': pageSize.toString(),
      };

      // Add filter parameters if provided
      if (filters != null) {
        if (filters.category != null) {
          queryParams['category'] = filters.category!;
        }
        if (filters.brand != null) {
          queryParams['brand'] = filters.brand!;
        }
        if (filters.minPrice != null) {
          queryParams['min_price'] = filters.minPrice!.toString();
        }
        if (filters.maxPrice != null) {
          queryParams['max_price'] = filters.maxPrice!.toString();
        }
        if (filters.tags.isNotEmpty) {
          queryParams['tags'] = filters.tags.join(',');
        }
        if (filters.inStock) {
          queryParams['in_stock'] = 'true';
        }
        if (filters.minRating != null) {
          queryParams['min_rating'] = filters.minRating!.toString();
        }
        if (filters.hasDiscount) {
          queryParams['has_discount'] = 'true';
        }
        queryParams['sort_by'] = filters.sortBy.toString().split('.').last;
        queryParams['sort_order'] = filters.sortOrder.toString().split('.').last;
      }

      // Build URI
      final uri = Uri.parse('$baseUrl/products/search').replace(
        queryParameters: queryParams,
      );

      // Make request
      final response = await client.get(
        uri,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final jsonData = json.decode(response.body) as Map<String, dynamic>;
        return ProductSearchResultModel.fromJson(jsonData);
      } else {
        throw ApiException(
          message: 'Failed to search products: ${response.statusCode}',
          statusCode: response.statusCode,
        );
      }
    } catch (e) {
      if (e is ApiException) rethrow;
      throw ApiException(
        message: 'Network error during product search: $e',
        statusCode: 0,
      );
    }
  }

  @override
  Future<ProductModel?> getProductById(String productId) async {
    try {
      final uri = Uri.parse('$baseUrl/products/$productId');

      final response = await client.get(
        uri,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final jsonData = json.decode(response.body) as Map<String, dynamic>;
        return ProductModel.fromJson(jsonData);
      } else if (response.statusCode == 404) {
        return null; // Product not found
      } else {
        throw ApiException(
          message: 'Failed to get product: ${response.statusCode}',
          statusCode: response.statusCode,
        );
      }
    } catch (e) {
      if (e is ApiException) rethrow;
      throw ApiException(
        message: 'Network error during product fetch: $e',
        statusCode: 0,
      );
    }
  }

  @override
  Future<ProductSearchResultModel> getTrendingProducts({
    String? category,
    String timePeriod = 'week',
    int page = 1,
    int pageSize = 20,
  }) async {
    try {
      final Map<String, String> queryParams = {
        'time_period': timePeriod,
        'page': page.toString(),
        'size': pageSize.toString(),
      };

      if (category != null) {
        queryParams['category'] = category;
      }

      final uri = Uri.parse('$baseUrl/products/trending').replace(
        queryParameters: queryParams,
      );

      final response = await client.get(
        uri,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final jsonData = json.decode(response.body) as Map<String, dynamic>;
        return ProductSearchResultModel.fromJson(jsonData);
      } else {
        throw ApiException(
          message: 'Failed to get trending products: ${response.statusCode}',
          statusCode: response.statusCode,
        );
      }
    } catch (e) {
      if (e is ApiException) rethrow;
      throw ApiException(
        message: 'Network error during trending products fetch: $e',
        statusCode: 0,
      );
    }
  }

  @override
  Future<List<ProductModel>> getProductRecommendations({
    String? productId,
    String? category,
    List<String>? tags,
    int limit = 10,
  }) async {
    try {
      final Map<String, String> queryParams = {
        'limit': limit.toString(),
      };

      if (productId != null) {
        queryParams['product_id'] = productId;
      }
      if (category != null) {
        queryParams['category'] = category;
      }
      if (tags != null && tags.isNotEmpty) {
        queryParams['tags'] = tags.join(',');
      }

      final uri = Uri.parse('$baseUrl/products/recommendations').replace(
        queryParameters: queryParams,
      );

      final response = await client.get(
        uri,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final jsonData = json.decode(response.body);
        if (jsonData is List) {
          return jsonData
              .map((item) => ProductModel.fromJson(item as Map<String, dynamic>))
              .toList();
        } else {
          throw ApiException(
            message: 'Unexpected response format for recommendations',
            statusCode: response.statusCode,
          );
        }
      } else {
        throw ApiException(
          message: 'Failed to get product recommendations: ${response.statusCode}',
          statusCode: response.statusCode,
        );
      }
    } catch (e) {
      if (e is ApiException) rethrow;
      throw ApiException(
        message: 'Network error during recommendations fetch: $e',
        statusCode: 0,
      );
    }
  }

  @override
  Future<ProductSearchResultModel> getProductsByCategory({
    required String category,
    ProductFilterModel? filters,
    int page = 1,
    int pageSize = 20,
  }) async {
    try {
      final Map<String, String> queryParams = {
        'page': page.toString(),
        'size': pageSize.toString(),
      };

      // Add filter parameters if provided
      if (filters != null) {
        if (filters.brand != null) {
          queryParams['brand'] = filters.brand!;
        }
        if (filters.minPrice != null) {
          queryParams['min_price'] = filters.minPrice!.toString();
        }
        if (filters.maxPrice != null) {
          queryParams['max_price'] = filters.maxPrice!.toString();
        }
        if (filters.tags.isNotEmpty) {
          queryParams['tags'] = filters.tags.join(',');
        }
        if (filters.inStock) {
          queryParams['in_stock'] = 'true';
        }
        if (filters.minRating != null) {
          queryParams['min_rating'] = filters.minRating!.toString();
        }
        if (filters.hasDiscount) {
          queryParams['has_discount'] = 'true';
        }
        queryParams['sort_by'] = filters.sortBy.toString().split('.').last;
        queryParams['sort_order'] = filters.sortOrder.toString().split('.').last;
      }

      final uri = Uri.parse('$baseUrl/products/category/$category').replace(
        queryParameters: queryParams,
      );

      final response = await client.get(
        uri,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final jsonData = json.decode(response.body) as Map<String, dynamic>;
        return ProductSearchResultModel.fromJson(jsonData);
      } else {
        throw ApiException(
          message: 'Failed to get products by category: ${response.statusCode}',
          statusCode: response.statusCode,
        );
      }
    } catch (e) {
      if (e is ApiException) rethrow;
      throw ApiException(
        message: 'Network error during category products fetch: $e',
        statusCode: 0,
      );
    }
  }

  @override
  Future<List<String>> getCategories() async {
    try {
      final uri = Uri.parse('$baseUrl/products/categories');

      final response = await client.get(
        uri,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final jsonData = json.decode(response.body);
        if (jsonData is List) {
          return jsonData.map((item) => item.toString()).toList();
        } else {
          throw ApiException(
            message: 'Unexpected response format for categories',
            statusCode: response.statusCode,
          );
        }
      } else {
        throw ApiException(
          message: 'Failed to get categories: ${response.statusCode}',
          statusCode: response.statusCode,
        );
      }
    } catch (e) {
      if (e is ApiException) rethrow;
      throw ApiException(
        message: 'Network error during categories fetch: $e',
        statusCode: 0,
      );
    }
  }

  @override
  Future<List<String>> getBrands({String? category}) async {
    try {
      final Map<String, String> queryParams = {};
      if (category != null) {
        queryParams['category'] = category;
      }

      final uri = Uri.parse('$baseUrl/products/brands').replace(
        queryParameters: queryParams.isNotEmpty ? queryParams : null,
      );

      final response = await client.get(
        uri,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final jsonData = json.decode(response.body);
        if (jsonData is List) {
          return jsonData.map((item) => item.toString()).toList();
        } else {
          throw ApiException(
            message: 'Unexpected response format for brands',
            statusCode: response.statusCode,
          );
        }
      } else {
        throw ApiException(
          message: 'Failed to get brands: ${response.statusCode}',
          statusCode: response.statusCode,
        );
      }
    } catch (e) {
      if (e is ApiException) rethrow;
      throw ApiException(
        message: 'Network error during brands fetch: $e',
        statusCode: 0,
      );
    }
  }
}
