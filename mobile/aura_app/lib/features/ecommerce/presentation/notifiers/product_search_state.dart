import 'package:equatable/equatable.dart';
import '../../domain/entities/product.dart';
import '../../../../core/error/failures.dart';

/// State for product search functionality
class ProductSearchState extends Equatable {
  final List<Product> products;
  final int totalCount;
  final int currentPage;
  final int pageSize;
  final int totalPages;
  final String searchQuery;
  final ProductFilter? activeFilter;
  final bool isLoading;
  final bool isLoadingMore;
  final bool hasError;
  final Failure? error;
  final Map<String, List<String>> facets;
  final bool hasReachedEnd;
  final double? searchTime;

  const ProductSearchState({
    this.products = const [],
    this.totalCount = 0,
    this.currentPage = 1,
    this.pageSize = 20,
    this.totalPages = 0,
    this.searchQuery = '',
    this.activeFilter,
    this.isLoading = false,
    this.isLoadingMore = false,
    this.hasError = false,
    this.error,
    this.facets = const {},
    this.hasReachedEnd = false,
    this.searchTime,
  });

  /// Check if search results are available
  bool get hasResults => products.isNotEmpty;

  /// Check if we can load more products
  bool get canLoadMore => currentPage < totalPages && !isLoadingMore && !hasReachedEnd;

  /// Check if this is the first page
  bool get isFirstPage => currentPage == 1;

  /// Get results info text
  String get resultsInfo {
    if (totalCount == 0) return 'No products found';
    final start = (currentPage - 1) * pageSize + 1;
    final end = (currentPage * pageSize).clamp(0, totalCount);
    return 'Showing $start-$end of $totalCount products';
  }

  ProductSearchState copyWith({
    List<Product>? products,
    int? totalCount,
    int? currentPage,
    int? pageSize,
    int? totalPages,
    String? searchQuery,
    ProductFilter? activeFilter,
    bool? isLoading,
    bool? isLoadingMore,
    bool? hasError,
    Failure? error,
    Map<String, List<String>>? facets,
    bool? hasReachedEnd,
    double? searchTime,
  }) {
    return ProductSearchState(
      products: products ?? this.products,
      totalCount: totalCount ?? this.totalCount,
      currentPage: currentPage ?? this.currentPage,
      pageSize: pageSize ?? this.pageSize,
      totalPages: totalPages ?? this.totalPages,
      searchQuery: searchQuery ?? this.searchQuery,
      activeFilter: activeFilter ?? this.activeFilter,
      isLoading: isLoading ?? this.isLoading,
      isLoadingMore: isLoadingMore ?? this.isLoadingMore,
      hasError: hasError ?? this.hasError,
      error: error ?? this.error,
      facets: facets ?? this.facets,
      hasReachedEnd: hasReachedEnd ?? this.hasReachedEnd,
      searchTime: searchTime ?? this.searchTime,
    );
  }

  @override
  List<Object?> get props => [
        products,
        totalCount,
        currentPage,
        pageSize,
        totalPages,
        searchQuery,
        activeFilter,
        isLoading,
        isLoadingMore,
        hasError,
        error,
        facets,
        hasReachedEnd,
        searchTime,
      ];

  @override
  String toString() {
    return 'ProductSearchState(products: ${products.length}, totalCount: $totalCount, currentPage: $currentPage, isLoading: $isLoading)';
  }
}
