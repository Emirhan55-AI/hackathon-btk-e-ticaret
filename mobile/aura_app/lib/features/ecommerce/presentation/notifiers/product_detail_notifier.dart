import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'product_detail_state.dart';
import '../../domain/entities/product.dart';
import '../../domain/usecases/ecommerce_usecases.dart';

/// Product detail notifier for managing product detail screen state
class ProductDetailNotifier extends StateNotifier<ProductDetailState> {
  final GetProductById _getProductById;

  ProductDetailNotifier({
    required GetProductById getProductById,
  })  : _getProductById = getProductById,
        super(const ProductDetailState());

  /// Load product details by ID
  Future<void> loadProduct(String productId) async {
    state = state.copyWith(isLoading: true, error: null);

    try {
      final result = await _getProductById(GetProductByIdParams(productId: productId));
      
      result.fold(
        (failure) {
          state = state.copyWith(
            isLoading: false,
            error: failure.message,
          );
        },
        (product) {
          state = state.copyWith(
            isLoading: false,
            product: product,
            selectedImageIndex: 0,
            quantity: 1,
            selectedVariants: {},
          );
        },
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: 'An unexpected error occurred: ${e.toString()}',
      );
    }
  }

  /// Set product directly (for navigation from other screens)
  void setProduct(Product product) {
    state = state.copyWith(
      product: product,
      selectedImageIndex: 0,
      quantity: 1,
      selectedVariants: {},
      error: null,
    );
  }

  /// Change selected image index
  void selectImage(int index) {
    if (state.product == null) return;
    
    final imageCount = state.product!.images.length;
    if (index >= 0 && index < imageCount) {
      state = state.copyWith(selectedImageIndex: index);
    }
  }

  /// Update quantity
  void updateQuantity(int newQuantity) {
    if (state.product == null) return;
    
    final maxQuantity = state.product!.stockQuantity;
    final validQuantity = newQuantity.clamp(1, maxQuantity);
    
    state = state.copyWith(quantity: validQuantity);
  }

  /// Increment quantity
  void incrementQuantity() {
    updateQuantity(state.quantity + 1);
  }

  /// Decrement quantity
  void decrementQuantity() {
    updateQuantity(state.quantity - 1);
  }

  /// Select variant option
  void selectVariant(String variantType, String variantValue) {
    final updatedVariants = Map<String, String>.from(state.selectedVariants);
    updatedVariants[variantType] = variantValue;
    
    state = state.copyWith(selectedVariants: updatedVariants);
  }

  /// Toggle favorite status
  void toggleFavorite() {
    if (state.product == null) return;
    
    // Implement actual favorite toggle logic with use case
    // For Phase 1, we'll implement basic state management
    state = state.copyWith(isFavorite: !state.isFavorite);
    
    // In Phase 2, add API call:
    // await favoriteUseCase.toggle(state.product?.id);
  }

  /// Add product to cart
  Future<void> addToCart() async {
    if (!state.canAddToCart) return;
    
    state = state.copyWith(isAddingToCart: true);

    try {
      // Implement actual add to cart logic with use case
      // For Phase 1, we'll simulate the cart functionality
      await Future.delayed(const Duration(milliseconds: 500));
      
      state = state.copyWith(
        isAddingToCart: false,
        addToCartSuccess: true,
      );
      
      // Reset success state after a delay
      Future.delayed(const Duration(seconds: 2), () {
        if (mounted) {
          state = state.resetAddToCart();
        }
      });
    } catch (e) {
      state = state.copyWith(
        isAddingToCart: false,
        error: 'Failed to add product to cart: ${e.toString()}',
      );
    }
  }

  /// Clear error state
  void clearError() {
    state = state.clearError();
  }

  /// Reset state
  void reset() {
    state = const ProductDetailState();
  }
}

/// Provider for product detail notifier is defined in app_providers.dart
