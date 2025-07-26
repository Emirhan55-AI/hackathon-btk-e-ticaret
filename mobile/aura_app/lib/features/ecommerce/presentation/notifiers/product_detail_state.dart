import 'package:equatable/equatable.dart';
import '../../domain/entities/product.dart';

/// State for product detail screen
class ProductDetailState extends Equatable {
  final Product? product;
  final bool isLoading;
  final String? error;
  final int selectedImageIndex;
  final int quantity;
  final bool isFavorite;
  final Map<String, String> selectedVariants;
  final bool isAddingToCart;
  final bool addToCartSuccess;

  const ProductDetailState({
    this.product,
    this.isLoading = false,
    this.error,
    this.selectedImageIndex = 0,
    this.quantity = 1,
    this.isFavorite = false,
    this.selectedVariants = const {},
    this.isAddingToCart = false,
    this.addToCartSuccess = false,
  });

  /// Check if all required variants are selected
  bool get allVariantsSelected {
    if (product == null) return true;
    
    // Get required variant keys from product attributes
    final requiredVariants = product!.attributes['variants'] as Map<String, dynamic>?;
    if (requiredVariants == null) return true;
    
    // Check if all required variants have selections
    for (final variantKey in requiredVariants.keys) {
      if (!selectedVariants.containsKey(variantKey) || 
          selectedVariants[variantKey]?.isEmpty == true) {
        return false;
      }
    }
    return true;
  }

  /// Check if product can be added to cart
  bool get canAddToCart {
    return product != null && 
           product!.inStock && 
           allVariantsSelected && 
           quantity > 0 && 
           quantity <= product!.stockQuantity &&
           !isAddingToCart;
  }

  /// Get current selected image
  ProductImage? get currentImage {
    if (product == null || product!.images.isEmpty) return null;
    if (selectedImageIndex >= product!.images.length) return product!.images.first;
    return product!.images[selectedImageIndex];
  }

  /// Get total price for selected quantity
  double get totalPrice {
    if (product == null) return 0.0;
    return product!.price * quantity;
  }

  /// Get formatted total price
  String get formattedTotalPrice {
    if (product == null) return '';
    return '${product!.currency} ${totalPrice.toStringAsFixed(2)}';
  }

  @override
  List<Object?> get props => [
        product,
        isLoading,
        error,
        selectedImageIndex,
        quantity,
        isFavorite,
        selectedVariants,
        isAddingToCart,
        addToCartSuccess,
      ];

  ProductDetailState copyWith({
    Product? product,
    bool? isLoading,
    String? error,
    int? selectedImageIndex,
    int? quantity,
    bool? isFavorite,
    Map<String, String>? selectedVariants,
    bool? isAddingToCart,
    bool? addToCartSuccess,
  }) {
    return ProductDetailState(
      product: product ?? this.product,
      isLoading: isLoading ?? this.isLoading,
      error: error,
      selectedImageIndex: selectedImageIndex ?? this.selectedImageIndex,
      quantity: quantity ?? this.quantity,
      isFavorite: isFavorite ?? this.isFavorite,
      selectedVariants: selectedVariants ?? this.selectedVariants,
      isAddingToCart: isAddingToCart ?? this.isAddingToCart,
      addToCartSuccess: addToCartSuccess ?? this.addToCartSuccess,
    );
  }

  /// Clear error state
  ProductDetailState clearError() {
    return copyWith(error: null);
  }

  /// Reset add to cart state
  ProductDetailState resetAddToCart() {
    return copyWith(
      addToCartSuccess: false,
      isAddingToCart: false,
    );
  }
}
