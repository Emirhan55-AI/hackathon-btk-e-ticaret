import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../domain/usecases/ecommerce_usecases.dart';
import 'product_search_state.dart';
import '../../domain/entities/product.dart';
import '../../../../core/error/failures.dart';
import '../../../../core/usecases/usecase.dart';

/// Notifier for managing product search state
class ProductSearchNotifier extends StateNotifier<ProductSearchState> {
  final SearchProducts _searchProducts;
  final GetCategories _getCategories;
  final GetBrands _getBrands;

  ProductSearchNotifier({
    required SearchProducts searchProducts,
    required GetCategories getCategories,
    required GetBrands getBrands,
  })  : _searchProducts = searchProducts,
        _getCategories = getCategories,
        _getBrands = getBrands,
        super(const ProductSearchState());

  /// Search for products
  Future<void> searchProducts(String query, {ProductFilter? filter}) async {
    if (state.isLoading) return;

    state = state.copyWith(
      isLoading: true,
      hasError: false,
      error: null,
      searchQuery: query,
      currentPage: 1,
    );

    final result = await _searchProducts(SearchProductsParams(
      query: query,
      filters: filter,
      page: 1,
      pageSize: state.pageSize,
    ));

    result.fold(
      (failure) {
        state = state.copyWith(
          isLoading: false,
          hasError: true,
          error: failure,
          products: [],
          totalCount: 0,
          totalPages: 0,
        );
      },
      (searchResult) {
        state = state.copyWith(
          isLoading: false,
          hasError: false,
          error: null,
          products: searchResult.products,
          totalCount: searchResult.totalCount,
          totalPages: searchResult.totalPages,
          currentPage: searchResult.page,
          facets: searchResult.facets,
          searchTime: searchResult.searchTime,
          hasReachedEnd: searchResult.products.length < state.pageSize,
          activeFilter: filter,
        );
      },
    );
  }

  /// Load more products (pagination)
  Future<void> loadMoreProducts() async {
    if (!state.canLoadMore || state.isLoadingMore) return;

    state = state.copyWith(isLoadingMore: true);

    final result = await _searchProducts(SearchProductsParams(
      query: state.searchQuery,
      filters: state.activeFilter,
      page: state.currentPage + 1,
      pageSize: state.pageSize,
    ));

    result.fold(
      (failure) {
        state = state.copyWith(
          isLoadingMore: false,
          hasError: true,
          error: failure,
        );
      },
      (searchResult) {
        final newProducts = [...state.products, ...searchResult.products];
        state = state.copyWith(
          isLoadingMore: false,
          hasError: false,
          error: null,
          products: newProducts,
          currentPage: searchResult.page,
          hasReachedEnd: searchResult.products.length < state.pageSize,
        );
      },
    );
  }

  /// Apply filters to current search
  Future<void> applyFilter(ProductFilter filter) async {
    await searchProducts(state.searchQuery, filter: filter);
  }

  /// Clear all filters
  Future<void> clearFilters() async {
    await searchProducts(state.searchQuery, filter: null);
  }

  /// Refresh current search
  Future<void> refresh() async {
    await searchProducts(state.searchQuery, filter: state.activeFilter);
  }

  /// Clear search and reset state
  void clearSearch() {
    state = const ProductSearchState();
  }

  /// Update search query without triggering search
  void updateSearchQuery(String query) {
    state = state.copyWith(searchQuery: query);
  }

  /// Get available categories (for filter)
  Future<List<String>> getCategories() async {
    final result = await _getCategories(const NoParams());
    return result.fold(
      (failure) => [],
      (categories) => categories,
    );
  }

  /// Get available brands (for filter)
  Future<List<String>> getBrands({String? category}) async {
    final result = await _getBrands(GetBrandsParams(category: category));
    return result.fold(
      (failure) => [],
      (brands) => brands,
    );
  }
}
