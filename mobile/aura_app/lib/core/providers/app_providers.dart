import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;

// E-commerce imports
import '../../features/ecommerce/domain/repositories/ecommerce_repository.dart';
import '../../features/ecommerce/domain/usecases/ecommerce_usecases.dart';
import '../../features/ecommerce/data/repositories/ecommerce_repository_impl.dart';
import '../../features/ecommerce/data/datasources/ecommerce_remote_data_source.dart';
import '../../features/ecommerce/presentation/notifiers/product_search_notifier.dart';
import '../../features/ecommerce/presentation/notifiers/product_search_state.dart';
import '../../features/ecommerce/presentation/notifiers/product_detail_notifier.dart';
import '../../features/ecommerce/presentation/notifiers/product_detail_state.dart';

/// Basic HTTP client provider
final httpClientProvider = Provider<http.Client>((ref) => http.Client());

/// E-commerce remote data source provider
final ecommerceRemoteDataSourceProvider = Provider<EcommerceRemoteDataSource>((ref) {
  return EcommerceRemoteDataSourceImpl(
    client: ref.read(httpClientProvider),
  );
});

/// E-commerce repository provider
final ecommerceRepositoryProvider = Provider<EcommerceRepository>((ref) {
  return EcommerceRepositoryImpl(
    remoteDataSource: ref.read(ecommerceRemoteDataSourceProvider),
  );
});

/// E-commerce use case providers
final searchProductsProvider = Provider<SearchProducts>((ref) {
  return SearchProducts(ref.read(ecommerceRepositoryProvider));
});

final getProductByIdProvider = Provider<GetProductById>((ref) {
  return GetProductById(ref.read(ecommerceRepositoryProvider));
});

final getTrendingProductsProvider = Provider<GetTrendingProducts>((ref) {
  return GetTrendingProducts(ref.read(ecommerceRepositoryProvider));
});

final getProductRecommendationsProvider = Provider<GetProductRecommendations>((ref) {
  return GetProductRecommendations(ref.read(ecommerceRepositoryProvider));
});

final getProductsByCategoryProvider = Provider<GetProductsByCategory>((ref) {
  return GetProductsByCategory(ref.read(ecommerceRepositoryProvider));
});

final getCategoriesProvider = Provider<GetCategories>((ref) {
  return GetCategories(ref.read(ecommerceRepositoryProvider));
});

final getBrandsProvider = Provider<GetBrands>((ref) {
  return GetBrands(ref.read(ecommerceRepositoryProvider));
});

/// E-commerce presentation layer providers
final productSearchNotifierProvider = 
    StateNotifierProvider<ProductSearchNotifier, ProductSearchState>((ref) {
  return ProductSearchNotifier(
    searchProducts: ref.read(searchProductsProvider),
    getCategories: ref.read(getCategoriesProvider),
    getBrands: ref.read(getBrandsProvider),
  );
});

final productDetailNotifierProvider = 
    StateNotifierProvider<ProductDetailNotifier, ProductDetailState>((ref) {
  return ProductDetailNotifier(
    getProductById: ref.read(getProductByIdProvider),
  );
});

/// Additional utility providers
final availableCategoriesProvider = Provider<List<String>>((ref) {
  return [
    'Electronics',
    'Clothing',
    'Home & Garden',
    'Sports',
    'Books',
    'Beauty',
    'Automotive',
    'Toys',
    'Health',
    'Food',
  ];
});

final availableBrandsProvider = Provider<List<String>>((ref) {
  return [
    'TechBrand',
    'FitTech',
    'SoundWave',
    'ChargeTech',
    'ErgoDesk',
    'ConnectPro',
    'SecureTech',
    'KeyMaster',
    'StyleCorp',
    'HomeLife',
  ];
});

/// App-wide state providers
final currentThemeProvider = StateProvider<ThemeMode>((ref) {
  return ThemeMode.system;
});

final navigationHistoryProvider = StateProvider<List<String>>((ref) {
  return [];
});

final cartItemCountProvider = StateProvider<int>((ref) {
  return 0;
});

final userFavoritesProvider = StateProvider<Set<String>>((ref) {
  return {};
});

final searchHistoryProvider = StateProvider<List<String>>((ref) {
  return [];
});
