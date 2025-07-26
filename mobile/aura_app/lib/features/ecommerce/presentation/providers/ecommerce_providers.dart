import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../notifiers/product_search_notifier.dart';
import '../notifiers/product_search_state.dart';
import '../notifiers/product_detail_notifier.dart';
import '../notifiers/product_detail_state.dart';

// TODO: Import actual use cases when data layer is connected
// import '../../domain/usecases/search_products.dart';
// import '../../domain/usecases/get_categories.dart';
// import '../../domain/usecases/get_brands.dart';
// import '../../domain/usecases/get_product_details.dart';

/// Product search provider - temporarily disabled until use cases are available
// final productSearchNotifierProvider = 
//     StateNotifierProvider<ProductSearchNotifier, ProductSearchState>((ref) {
//   return ProductSearchNotifier(
//     searchProducts: ref.read(searchProductsProvider),
//     getCategories: ref.read(getCategoriesProvider),
//     getBrands: ref.read(getBrandsProvider),
//   );
// });

/// Product detail provider - temporarily disabled until use cases are available  
// final productDetailNotifierProvider = 
//     StateNotifierProvider<ProductDetailNotifier, ProductDetailState>((ref) {
//   return ProductDetailNotifier(
//     getProductDetails: ref.read(getProductDetailsProvider),
//   );
// });

/// Mock providers for development - Remove when actual providers are implemented

/// Mock product search provider
final mockProductSearchNotifierProvider = 
    StateNotifierProvider<MockProductSearchNotifier, ProductSearchState>((ref) {
  return MockProductSearchNotifier();
});

/// Mock product detail provider
final mockProductDetailNotifierProvider = 
    StateNotifierProvider<MockProductDetailNotifier, ProductDetailState>((ref) {
  return MockProductDetailNotifier();
});

/// Mock implementation of ProductSearchNotifier for testing
class MockProductSearchNotifier extends StateNotifier<ProductSearchState> {
  MockProductSearchNotifier() : super(const ProductSearchState());

  void searchProducts(String query) {
    // Mock search implementation
    state = state.copyWith(
      isLoading: true,
      searchQuery: query,
    );
    
    // Simulate API delay
    Future.delayed(const Duration(milliseconds: 500), () {
      if (mounted) {
        state = state.copyWith(
          isLoading: false,
          products: [], // Mock empty results
          totalCount: 0,
        );
      }
    });
  }

  void loadMoreProducts() {
    // Mock load more implementation
  }

  void applyFilter(filter) {
    // Mock apply filter implementation
    state = state.copyWith(
      activeFilter: filter,
      isLoading: true,
    );
    
    Future.delayed(const Duration(milliseconds: 300), () {
      if (mounted) {
        state = state.copyWith(
          isLoading: false,
        );
      }
    });
  }

  void clearFilters() {
    // Mock clear filters implementation
  }

  void refreshProducts() {
    // Mock refresh implementation
  }
}

/// Mock implementation of ProductDetailNotifier for testing
class MockProductDetailNotifier extends StateNotifier<ProductDetailState> {
  MockProductDetailNotifier() : super(const ProductDetailState());

  void setProduct(product) {
    state = state.copyWith(product: product);
  }

  void selectImage(int index) {
    state = state.copyWith(selectedImageIndex: index);
  }

  void updateQuantity(int quantity) {
    state = state.copyWith(quantity: quantity);
  }

  void selectVariant(String type, String value) {
    final variants = Map<String, String>.from(state.selectedVariants);
    variants[type] = value;
    state = state.copyWith(selectedVariants: variants);
  }

  void toggleFavorite() {
    state = state.copyWith(isFavorite: !state.isFavorite);
  }

  Future<void> addToCart() async {
    state = state.copyWith(isAddingToCart: true);
    
    // Simulate API call
    await Future.delayed(const Duration(milliseconds: 500));
    
    if (mounted) {
      state = state.copyWith(
        isAddingToCart: false,
        addToCartSuccess: true,
      );
    }
  }
}

/// Available categories provider
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

/// Available brands provider
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

/// Current app theme provider
final currentThemeProvider = StateProvider<ThemeMode>((ref) {
  return ThemeMode.system;
});

/// Navigation history provider
final navigationHistoryProvider = StateProvider<List<String>>((ref) {
  return [];
});

/// Shopping cart item count provider
final cartItemCountProvider = StateProvider<int>((ref) {
  return 0;
});

/// User favorites provider
final userFavoritesProvider = StateProvider<Set<String>>((ref) {
  return {};
});

/// Search history provider
final searchHistoryProvider = StateProvider<List<String>>((ref) {
  return [];
});
