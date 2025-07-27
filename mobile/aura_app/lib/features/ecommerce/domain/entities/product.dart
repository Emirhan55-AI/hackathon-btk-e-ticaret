import 'package:equatable/equatable.dart';

/// Sorting options for products
enum ProductSortBy {
  relevance,
  name,
  price,
  rating,
  newest,
  popular,
}

/// Sort order enum
enum SortOrder {
  asc,
  desc,
}

/// Product image entity
class ProductImage extends Equatable {
  final String id;
  final String url;
  final String altText;
  final bool isMain;
  final int sortOrder;

  const ProductImage({
    required this.id,
    required this.url,
    required this.altText,
    this.isMain = false,
    this.sortOrder = 0,
  });

  @override
  List<Object?> get props => [id, url, altText, isMain, sortOrder];

  ProductImage copyWith({
    String? id,
    String? url,
    String? altText,
    bool? isMain,
    int? sortOrder,
  }) {
    return ProductImage(
      id: id ?? this.id,
      url: url ?? this.url,
      altText: altText ?? this.altText,
      isMain: isMain ?? this.isMain,
      sortOrder: sortOrder ?? this.sortOrder,
    );
  }

  @override
  String toString() => 'ProductImage(id: $id, url: $url, altText: $altText, isMain: $isMain)';
}

/// Product entity representing a product in the e-commerce system
class Product extends Equatable {
  final String id;
  final String name;
  final String description;
  final double price;
  final double? originalPrice;
  final String currency;
  final String category;
  final String? brand;
  final String? sku;
  final List<ProductImage> images;
  final List<String> tags;
  final double rating;
  final int reviewCount;
  final int stockQuantity;
  final bool isActive;
  final double? discountPercentage;
  final DateTime? createdAt;
  final DateTime? updatedAt;
  final Map<String, dynamic> attributes;

  const Product({
    required this.id,
    required this.name,
    required this.description,
    required this.price,
    this.originalPrice,
    required this.currency,
    required this.category,
    this.brand,
    this.sku,
    this.images = const [],
    this.tags = const [],
    this.rating = 0.0,
    this.reviewCount = 0,
    this.stockQuantity = 0,
    this.isActive = true,
    this.discountPercentage,
    this.createdAt,
    this.updatedAt,
    this.attributes = const {},
  });

  /// Get primary image for the product
  ProductImage? get primaryImage {
    try {
      return images.firstWhere((img) => img.isMain);
    } catch (e) {
      return images.isNotEmpty ? images.first : null;
    }
  }

  /// Get secondary images (non-primary)
  List<ProductImage> get secondaryImages {
    return images.where((img) => !img.isMain).toList();
  }

  /// Check if product has discount
  bool get hasDiscount {
    return originalPrice != null && originalPrice! > price;
  }

  /// Calculate discount percentage (computed from price difference)
  double? get computedDiscountPercentage {
    if (!hasDiscount) return null;
    return ((originalPrice! - price) / originalPrice!) * 100;
  }

  /// Get formatted price string
  String get formattedPrice {
    return '$currency ${price.toStringAsFixed(2)}';
  }

  /// Get formatted original price string
  String? get formattedOriginalPrice {
    if (originalPrice == null) return null;
    return '$currency ${originalPrice!.toStringAsFixed(2)}';
  }

  /// Check if product is in stock
  bool get inStock {
    return isActive && stockQuantity > 0;
  }

  /// Get stock status string
  String get stockStatus {
    if (!isActive) return 'Unavailable';
    if (stockQuantity == 0) return 'Out of Stock';
    if (stockQuantity < 5) return 'Low Stock';
    return 'In Stock';
  }

  /// Get rating stars as integer (out of 5)
  int get ratingStars {
    return rating.round().clamp(0, 5);
  }

  @override
  List<Object?> get props => [
        id,
        name,
        description,
        price,
        originalPrice,
        currency,
        category,
        brand,
        sku,
        images,
        tags,
        rating,
        reviewCount,
        stockQuantity,
        isActive,
        discountPercentage,
        createdAt,
        updatedAt,
        attributes,
      ];

  Product copyWith({
    String? id,
    String? name,
    String? description,
    double? price,
    double? originalPrice,
    String? currency,
    String? category,
    String? brand,
    String? sku,
    List<ProductImage>? images,
    List<String>? tags,
    double? rating,
    int? reviewCount,
    int? stockQuantity,
    bool? isActive,
    double? discountPercentage,
    DateTime? createdAt,
    DateTime? updatedAt,
    Map<String, dynamic>? attributes,
  }) {
    return Product(
      id: id ?? this.id,
      name: name ?? this.name,
      description: description ?? this.description,
      price: price ?? this.price,
      originalPrice: originalPrice ?? this.originalPrice,
      currency: currency ?? this.currency,
      category: category ?? this.category,
      brand: brand ?? this.brand,
      sku: sku ?? this.sku,
      images: images ?? this.images,
      tags: tags ?? this.tags,
      rating: rating ?? this.rating,
      reviewCount: reviewCount ?? this.reviewCount,
      stockQuantity: stockQuantity ?? this.stockQuantity,
      isActive: isActive ?? this.isActive,
      discountPercentage: discountPercentage ?? this.discountPercentage,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      attributes: attributes ?? this.attributes,
    );
  }

  @override
  String toString() {
    return 'Product(id: $id, name: $name, price: $price, category: $category, isActive: $isActive)';
  }
}

/// Product filter entity for search
class ProductFilter extends Equatable {
  final String? category;
  final String? brand;
  final double? minPrice;
  final double? maxPrice;
  final List<String> tags;
  final ProductSortBy sortBy;
  final SortOrder sortOrder;
  final bool inStock;
  final double? minRating;
  final bool hasDiscount;
  final Map<String, dynamic> attributes;

  const ProductFilter({
    this.category,
    this.brand,
    this.minPrice,
    this.maxPrice,
    this.tags = const [],
    this.sortBy = ProductSortBy.relevance,
    this.sortOrder = SortOrder.asc,
    this.inStock = false,
    this.minRating,
    this.hasDiscount = false,
    this.attributes = const {},
  });

  @override
  List<Object?> get props => [
        category,
        brand,
        minPrice,
        maxPrice,
        tags,
        sortBy,
        sortOrder,
        inStock,
        minRating,
        hasDiscount,
        attributes,
      ];

  ProductFilter copyWith({
    String? category,
    String? brand,
    double? minPrice,
    double? maxPrice,
    List<String>? tags,
    ProductSortBy? sortBy,
    SortOrder? sortOrder,
    bool? inStock,
    double? minRating,
    bool? hasDiscount,
    Map<String, dynamic>? attributes,
  }) {
    return ProductFilter(
      category: category ?? this.category,
      brand: brand ?? this.brand,
      minPrice: minPrice ?? this.minPrice,
      maxPrice: maxPrice ?? this.maxPrice,
      tags: tags ?? this.tags,
      sortBy: sortBy ?? this.sortBy,
      sortOrder: sortOrder ?? this.sortOrder,
      inStock: inStock ?? this.inStock,
      minRating: minRating ?? this.minRating,
      hasDiscount: hasDiscount ?? this.hasDiscount,
      attributes: attributes ?? this.attributes,
    );
  }

  /// Check if filter is empty
  bool get isEmpty {
    return category == null &&
        brand == null &&
        minPrice == null &&
        maxPrice == null &&
        tags.isEmpty &&
        !inStock &&
        minRating == null &&
        !hasDiscount &&
        attributes.isEmpty;
  }

  @override
  String toString() {
    return 'ProductFilter(category: $category, brand: $brand, priceRange: $minPrice-$maxPrice, inStock: $inStock)';
  }
}

/// Product search result entity
class ProductSearchResult extends Equatable {
  final List<Product> products;
  final int totalCount;
  final int page;
  final int pageSize;
  final int totalPages;
  final Map<String, List<String>> facets;
  final double? searchTime;

  const ProductSearchResult({
    required this.products,
    required this.totalCount,
    required this.page,
    required this.pageSize,
    required this.totalPages,
    this.facets = const {},
    this.searchTime,
  });

  /// Check if has next page
  bool get hasNextPage {
    return page < totalPages;
  }

  /// Check if has previous page
  bool get hasPreviousPage {
    return page > 1;
  }

  @override
  List<Object?> get props => [
        products,
        totalCount,
        page,
        pageSize,
        totalPages,
        facets,
        searchTime,
      ];

  ProductSearchResult copyWith({
    List<Product>? products,
    int? totalCount,
    int? page,
    int? pageSize,
    int? totalPages,
    Map<String, List<String>>? facets,
    double? searchTime,
  }) {
    return ProductSearchResult(
      products: products ?? this.products,
      totalCount: totalCount ?? this.totalCount,
      page: page ?? this.page,
      pageSize: pageSize ?? this.pageSize,
      totalPages: totalPages ?? this.totalPages,
      facets: facets ?? this.facets,
      searchTime: searchTime ?? this.searchTime,
    );
  }

  @override
  String toString() {
    return 'ProductSearchResult(count: ${products.length}, total: $totalCount, page: $page/$totalPages)';
  }
}
