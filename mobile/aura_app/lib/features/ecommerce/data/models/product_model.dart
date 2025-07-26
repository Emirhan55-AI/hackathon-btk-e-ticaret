import '../../domain/entities/product.dart';

/// Data model for Product Images
class ProductImageModel extends ProductImage {
  const ProductImageModel({
    required super.id,
    required super.url,
    required super.altText,
    super.isMain = false,
    super.sortOrder = 0,
  });

  /// Create from JSON
  factory ProductImageModel.fromJson(Map<String, dynamic> json) {
    return ProductImageModel(
      id: json['id'] as String,
      url: json['url'] as String,
      altText: json['alt_text'] as String? ?? '',
      isMain: json['is_main'] as bool? ?? false,
      sortOrder: json['sort_order'] as int? ?? 0,
    );
  }

  /// Convert to JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'url': url,
      'alt_text': altText,
      'is_main': isMain,
      'sort_order': sortOrder,
    };
  }

  /// Create from entity
  factory ProductImageModel.fromEntity(ProductImage entity) {
    return ProductImageModel(
      id: entity.id,
      url: entity.url,
      altText: entity.altText,
      isMain: entity.isMain,
      sortOrder: entity.sortOrder,
    );
  }
}

/// Data model for Product
class ProductModel extends Product {
  const ProductModel({
    required super.id,
    required super.name,
    required super.description,
    required super.price,
    required super.currency,
    required super.category,
    super.brand,
    super.sku,
    super.images = const [],
    super.tags = const [],
    super.stockQuantity = 0,
    super.isActive = true,
    super.rating = 0.0,
    super.reviewCount = 0,
    super.discountPercentage,
    super.originalPrice,
    super.createdAt,
    super.updatedAt,
    super.attributes = const {},
  });

  /// Create from JSON
  factory ProductModel.fromJson(Map<String, dynamic> json) {
    // Parse images
    List<ProductImage> images = [];
    if (json['images'] != null) {
      images = (json['images'] as List)
          .map((img) => ProductImageModel.fromJson(img as Map<String, dynamic>))
          .toList();
    }

    // Parse tags
    List<String> tags = [];
    if (json['tags'] != null) {
      tags = (json['tags'] as List).map((tag) => tag.toString()).toList();
    }

    // Parse attributes
    Map<String, dynamic> attributes = {};
    if (json['attributes'] != null) {
      attributes = Map<String, dynamic>.from(json['attributes'] as Map);
    }

    return ProductModel(
      id: json['id'] as String,
      name: json['name'] as String,
      description: json['description'] as String,
      price: (json['price'] as num).toDouble(),
      currency: json['currency'] as String? ?? 'USD',
      category: json['category'] as String,
      brand: json['brand'] as String?,
      sku: json['sku'] as String?,
      images: images,
      tags: tags,
      stockQuantity: json['stock_quantity'] as int? ?? 0,
      isActive: json['is_active'] as bool? ?? true,
      rating: (json['rating'] as num?)?.toDouble() ?? 0.0,
      reviewCount: json['review_count'] as int? ?? 0,
      discountPercentage: (json['discount_percentage'] as num?)?.toDouble(),
      originalPrice: (json['original_price'] as num?)?.toDouble(),
      createdAt: json['created_at'] != null 
          ? DateTime.parse(json['created_at'] as String)
          : null,
      updatedAt: json['updated_at'] != null
          ? DateTime.parse(json['updated_at'] as String)
          : null,
      attributes: attributes,
    );
  }

  /// Convert to JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'price': price,
      'currency': currency,
      'category': category,
      'brand': brand,
      'sku': sku,
      'images': images.map((img) => ProductImageModel.fromEntity(img).toJson()).toList(),
      'tags': tags,
      'stock_quantity': stockQuantity,
      'is_active': isActive,
      'rating': rating,
      'review_count': reviewCount,
      'discount_percentage': discountPercentage,
      'original_price': originalPrice,
      'created_at': createdAt?.toIso8601String(),
      'updated_at': updatedAt?.toIso8601String(),
      'attributes': attributes,
    };
  }

  /// Create from entity
  factory ProductModel.fromEntity(Product entity) {
    return ProductModel(
      id: entity.id,
      name: entity.name,
      description: entity.description,
      price: entity.price,
      currency: entity.currency,
      category: entity.category,
      brand: entity.brand,
      sku: entity.sku,
      images: entity.images,
      tags: entity.tags,
      stockQuantity: entity.stockQuantity,
      isActive: entity.isActive,
      rating: entity.rating,
      reviewCount: entity.reviewCount,
      discountPercentage: entity.discountPercentage,
      originalPrice: entity.originalPrice,
      createdAt: entity.createdAt,
      updatedAt: entity.updatedAt,
      attributes: entity.attributes,
    );
  }
}

/// Data model for Product Filter
class ProductFilterModel extends ProductFilter {
  const ProductFilterModel({
    super.category,
    super.brand,
    super.minPrice,
    super.maxPrice,
    super.tags = const [],
    super.sortBy = ProductSortBy.relevance,
    super.sortOrder = SortOrder.asc,
    super.inStock = false,
    super.minRating,
    super.hasDiscount = false,
    super.attributes = const {},
  });

  /// Create from JSON
  factory ProductFilterModel.fromJson(Map<String, dynamic> json) {
    // Parse tags
    List<String> tags = [];
    if (json['tags'] != null) {
      tags = (json['tags'] as List).map((tag) => tag.toString()).toList();
    }

    // Parse attributes
    Map<String, dynamic> attributes = {};
    if (json['attributes'] != null) {
      attributes = Map<String, dynamic>.from(json['attributes'] as Map);
    }

    // Parse sort by
    ProductSortBy sortBy = ProductSortBy.relevance;
    if (json['sort_by'] != null) {
      final sortByStr = json['sort_by'] as String;
      sortBy = ProductSortBy.values.firstWhere(
        (e) => e.toString().split('.').last == sortByStr,
        orElse: () => ProductSortBy.relevance,
      );
    }

    // Parse sort order
    SortOrder sortOrder = SortOrder.asc;
    if (json['sort_order'] != null) {
      final sortOrderStr = json['sort_order'] as String;
      sortOrder = SortOrder.values.firstWhere(
        (e) => e.toString().split('.').last == sortOrderStr,
        orElse: () => SortOrder.asc,
      );
    }

    return ProductFilterModel(
      category: json['category'] as String?,
      brand: json['brand'] as String?,
      minPrice: (json['min_price'] as num?)?.toDouble(),
      maxPrice: (json['max_price'] as num?)?.toDouble(),
      tags: tags,
      sortBy: sortBy,
      sortOrder: sortOrder,
      inStock: json['in_stock'] as bool? ?? false,
      minRating: (json['min_rating'] as num?)?.toDouble(),
      hasDiscount: json['has_discount'] as bool? ?? false,
      attributes: attributes,
    );
  }

  /// Convert to JSON
  Map<String, dynamic> toJson() {
    return {
      'category': category,
      'brand': brand,
      'min_price': minPrice,
      'max_price': maxPrice,
      'tags': tags,
      'sort_by': sortBy.toString().split('.').last,
      'sort_order': sortOrder.toString().split('.').last,
      'in_stock': inStock,
      'min_rating': minRating,
      'has_discount': hasDiscount,
      'attributes': attributes,
    };
  }

  /// Create from entity
  factory ProductFilterModel.fromEntity(ProductFilter entity) {
    return ProductFilterModel(
      category: entity.category,
      brand: entity.brand,
      minPrice: entity.minPrice,
      maxPrice: entity.maxPrice,
      tags: entity.tags,
      sortBy: entity.sortBy,
      sortOrder: entity.sortOrder,
      inStock: entity.inStock,
      minRating: entity.minRating,
      hasDiscount: entity.hasDiscount,
      attributes: entity.attributes,
    );
  }
}

/// Data model for Product Search Result
class ProductSearchResultModel extends ProductSearchResult {
  const ProductSearchResultModel({
    required super.products,
    required super.totalCount,
    required super.page,
    required super.pageSize,
    required super.totalPages,
    super.facets = const {},
    super.searchTime,
  });

  /// Create from JSON
  factory ProductSearchResultModel.fromJson(Map<String, dynamic> json) {
    // Parse products
    List<Product> products = [];
    if (json['products'] != null) {
      products = (json['products'] as List)
          .map((product) => ProductModel.fromJson(product as Map<String, dynamic>))
          .toList();
    }

    // Parse facets
    Map<String, List<String>> facets = {};
    if (json['facets'] != null) {
      final facetsData = json['facets'] as Map<String, dynamic>;
      facetsData.forEach((key, value) {
        if (value is List) {
          facets[key] = value.map((item) => item.toString()).toList();
        }
      });
    }

    return ProductSearchResultModel(
      products: products,
      totalCount: json['total_count'] as int,
      page: json['page'] as int,
      pageSize: json['page_size'] as int,
      totalPages: json['total_pages'] as int,
      facets: facets,
      searchTime: (json['search_time'] as num?)?.toDouble(),
    );
  }

  /// Convert to JSON
  Map<String, dynamic> toJson() {
    return {
      'products': products.map((product) => ProductModel.fromEntity(product).toJson()).toList(),
      'total_count': totalCount,
      'page': page,
      'page_size': pageSize,
      'total_pages': totalPages,
      'facets': facets,
      'search_time': searchTime,
    };
  }

  /// Create from entity
  factory ProductSearchResultModel.fromEntity(ProductSearchResult entity) {
    return ProductSearchResultModel(
      products: entity.products,
      totalCount: entity.totalCount,
      page: entity.page,
      pageSize: entity.pageSize,
      totalPages: entity.totalPages,
      facets: entity.facets,
      searchTime: entity.searchTime,
    );
  }
}
