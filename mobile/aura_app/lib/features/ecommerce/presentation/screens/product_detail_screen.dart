import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../widgets/product_image_gallery.dart';
import '../widgets/quantity_selector.dart';
import '../widgets/variant_selector.dart';
import '../widgets/rating_bar.dart';
import '../../domain/entities/product.dart';
import '../notifiers/product_detail_state.dart';
import '../../../../core/providers/app_providers.dart';

/// Product detail screen showing comprehensive product information
class ProductDetailScreen extends ConsumerStatefulWidget {
  final String productId;
  final Product? product;

  const ProductDetailScreen({
    super.key,
    required this.productId,
    this.product,
  });

  @override
  ConsumerState<ProductDetailScreen> createState() => _ProductDetailScreenState();
}

class _ProductDetailScreenState extends ConsumerState<ProductDetailScreen> {
  late ScrollController _scrollController;

  @override
  void initState() {
    super.initState();
    _scrollController = ScrollController();
    
    // Initialize with product if provided, otherwise load from API
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (widget.product != null) {
        ref.read(productDetailNotifierProvider.notifier).setProduct(widget.product!);
      } else {
        ref.read(productDetailNotifierProvider.notifier).loadProduct(widget.productId);
      }
    });
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(productDetailNotifierProvider);

    return Scaffold(
      body: state.isLoading
          ? const Center(child: CircularProgressIndicator())
          : state.error != null
              ? _buildErrorState(context, state.error!)
              : state.product == null
                  ? _buildNotFoundState(context)
                  : _buildProductDetail(context, state),
      bottomNavigationBar: state.product != null && !state.isLoading
          ? _buildBottomBar(context, state)
          : null,
    );
  }

  Widget _buildProductDetail(BuildContext context, ProductDetailState state) {
    final product = state.product!;
    
    return CustomScrollView(
      controller: _scrollController,
      slivers: [
        // App bar
        _buildSliverAppBar(context, product, state),
        
        // Product content
        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Product images
                ProductImageGallery(
                  images: product.images,
                  initialIndex: state.selectedImageIndex,
                  onImageChanged: (index) {
                    // TODO: Update selected image when provider is available
                    // ref.read(productDetailNotifierProvider.notifier).selectImage(index);
                  },
                ),
                
                const SizedBox(height: 24),
                
                // Product info section
                _buildProductInfo(context, product),
                
                const SizedBox(height: 24),
                
                // Price section
                _buildPriceSection(context, product, state),
                
                const SizedBox(height: 24),
                
                // Variants section
                if (_hasVariants(product))
                  _buildVariantsSection(context, product, state),
                
                const SizedBox(height: 24),
                
                // Quantity section
                _buildQuantitySection(context, state),
                
                const SizedBox(height: 24),
                
                // Description section
                _buildDescriptionSection(context, product),
                
                const SizedBox(height: 24),
                
                // Stock and shipping info
                _buildStockAndShippingInfo(context, product),
                
                const SizedBox(height: 100), // Space for bottom bar
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildSliverAppBar(BuildContext context, Product product, ProductDetailState state) {
    final colorScheme = Theme.of(context).colorScheme;
    
    return SliverAppBar(
      expandedHeight: 0,
      pinned: true,
      backgroundColor: colorScheme.surface,
      foregroundColor: colorScheme.onSurface,
      leading: IconButton(
        onPressed: () => context.pop(),
        icon: const Icon(Icons.arrow_back),
      ),
      actions: [
        IconButton(
          onPressed: () {
            // TODO: Implement share functionality
          },
          icon: const Icon(Icons.share),
        ),
        IconButton(
          onPressed: () {
            ref.read(productDetailNotifierProvider.notifier).toggleFavorite();
          },
          icon: Icon(
            state.isFavorite ? Icons.favorite : Icons.favorite_border,
            color: state.isFavorite ? Colors.red : null,
          ),
        ),
        const SizedBox(width: 8),
      ],
    );
  }

  Widget _buildProductInfo(BuildContext context, Product product) {
    final theme = Theme.of(context);
    
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Brand
        if (product.brand != null)
          Text(
            product.brand!,
            style: theme.textTheme.titleSmall?.copyWith(
              color: theme.colorScheme.primary,
              fontWeight: FontWeight.w600,
            ),
          ),
        
        const SizedBox(height: 8),
        
        // Product name
        Text(
          product.name,
          style: theme.textTheme.headlineSmall?.copyWith(
            fontWeight: FontWeight.bold,
          ),
        ),
        
        const SizedBox(height: 12),
        
        // Rating and reviews
        Row(
          children: [
            CustomRatingBar(
              rating: product.rating,
              size: 20,
            ),
            const SizedBox(width: 8),
            Text(
              '${product.rating.toStringAsFixed(1)}',
              style: theme.textTheme.titleMedium?.copyWith(
                fontWeight: FontWeight.w600,
              ),
            ),
            const SizedBox(width: 8),
            Text(
              '(${product.reviewCount} reviews)',
              style: theme.textTheme.bodyMedium?.copyWith(
                color: theme.colorScheme.onSurface.withOpacity(0.7),
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildPriceSection(BuildContext context, Product product, ProductDetailState state) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: colorScheme.surfaceContainerHighest,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              // Current price
              Text(
                product.formattedPrice,
                style: theme.textTheme.headlineMedium?.copyWith(
                  fontWeight: FontWeight.bold,
                  color: colorScheme.primary,
                ),
              ),
              
              const SizedBox(width: 12),
              
              // Original price (if discounted)
              if (product.hasDiscount && product.formattedOriginalPrice != null)
                Text(
                  product.formattedOriginalPrice!,
                  style: theme.textTheme.titleMedium?.copyWith(
                    decoration: TextDecoration.lineThrough,
                    color: colorScheme.onSurface.withOpacity(0.6),
                  ),
                ),
            ],
          ),
          
          const SizedBox(height: 8),
          
          // Discount percentage
          if (product.hasDiscount)
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
              decoration: BoxDecoration(
                color: Colors.red,
                borderRadius: BorderRadius.circular(4),
              ),
              child: Text(
                '${product.computedDiscountPercentage?.toStringAsFixed(0)}% OFF',
                style: theme.textTheme.labelMedium?.copyWith(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          
          const SizedBox(height: 12),
          
          // Total price for quantity
          if (state.quantity > 1)
            Text(
              'Total: ${state.formattedTotalPrice}',
              style: theme.textTheme.titleMedium?.copyWith(
                fontWeight: FontWeight.w600,
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildVariantsSection(BuildContext context, Product product, ProductDetailState state) {
    final variants = product.attributes['variants'] as Map<String, dynamic>?;
    if (variants == null) return const SizedBox.shrink();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Options',
          style: Theme.of(context).textTheme.titleLarge?.copyWith(
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 16),
        MultiVariantSelector(
          variants: variants.map((key, value) => MapEntry(
            key,
            (value as List).cast<String>(),
          )),
          selectedVariants: state.selectedVariants,
          onVariantSelected: (type, option) {
            // TODO: Update variant selection when provider is available
            // ref.read(productDetailNotifierProvider.notifier).selectVariant(type, option);
          },
        ),
      ],
    );
  }

  Widget _buildQuantitySection(BuildContext context, ProductDetailState state) {
    return LabeledQuantitySelector(
      label: 'Quantity',
      quantity: state.quantity,
      maxQuantity: state.product?.stockQuantity ?? 1,
      onQuantityChanged: (quantity) {
        // TODO: Update quantity when provider is available
        // ref.read(productDetailNotifierProvider.notifier).updateQuantity(quantity);
      },
      subtitle: 'Select the number of items',
    );
  }

  Widget _buildDescriptionSection(BuildContext context, Product product) {
    final theme = Theme.of(context);
    
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Description',
          style: theme.textTheme.titleLarge?.copyWith(
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 12),
        Text(
          product.description,
          style: theme.textTheme.bodyLarge?.copyWith(
            height: 1.6,
          ),
        ),
      ],
    );
  }

  Widget _buildStockAndShippingInfo(BuildContext context, Product product) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    
    return Column(
      children: [
        // Stock status
        _buildInfoCard(
          context: context,
          icon: Icons.inventory_2_outlined,
          title: 'Stock Status',
          content: product.stockStatus,
          color: product.inStock ? Colors.green : Colors.red,
        ),
        
        const SizedBox(height: 12),
        
        // SKU
        if (product.sku != null)
          _buildInfoCard(
            context: context,
            icon: Icons.qr_code,
            title: 'SKU',
            content: product.sku!,
          ),
      ],
    );
  }

  Widget _buildInfoCard({
    required BuildContext context,
    required IconData icon,
    required String title,
    required String content,
    Color? color,
  }) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        border: Border.all(color: colorScheme.outlineVariant),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Row(
        children: [
          Icon(
            icon,
            color: color ?? colorScheme.onSurface.withOpacity(0.7),
          ),
          const SizedBox(width: 12),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: theme.textTheme.labelMedium?.copyWith(
                  color: colorScheme.onSurface.withOpacity(0.7),
                ),
              ),
              Text(
                content,
                style: theme.textTheme.titleMedium?.copyWith(
                  fontWeight: FontWeight.w600,
                  color: color,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildBottomBar(BuildContext context, ProductDetailState state) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: colorScheme.surface,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 8,
            offset: const Offset(0, -2),
          ),
        ],
      ),
      child: SafeArea(
        child: Row(
          children: [
            // Favorite button
            OutlinedButton(
              onPressed: () {
                // TODO: Toggle favorite when provider is available
                // ref.read(productDetailNotifierProvider.notifier).toggleFavorite();
              },
              style: OutlinedButton.styleFrom(
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
                padding: const EdgeInsets.all(12),
              ),
              child: Icon(
                state.isFavorite ? Icons.favorite : Icons.favorite_border,
                color: state.isFavorite ? Colors.red : null,
              ),
            ),
            
            const SizedBox(width: 12),
            
            // Add to cart button
            Expanded(
              child: FilledButton(
                onPressed: state.canAddToCart
                    ? () {
                        // TODO: Add to cart when provider is available
                        // ref.read(productDetailNotifierProvider.notifier).addToCart();
                        _showAddToCartSuccess(context);
                      }
                    : null,
                style: FilledButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8),
                  ),
                ),
                child: state.isAddingToCart
                    ? const SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(
                          strokeWidth: 2,
                          valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                        ),
                      )
                    : const Text('Add to Cart'),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildErrorState(BuildContext context, String error) {
    final theme = Theme.of(context);
    
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.error_outline,
              size: 64,
              color: theme.colorScheme.error,
            ),
            const SizedBox(height: 16),
            Text(
              'Error',
              style: theme.textTheme.headlineSmall?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              error,
              style: theme.textTheme.bodyLarge,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 24),
            FilledButton(
              onPressed: () {
                // TODO: Retry loading when provider is available
                // ref.read(productDetailNotifierProvider.notifier).loadProduct(widget.productId);
              },
              child: const Text('Retry'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildNotFoundState(BuildContext context) {
    final theme = Theme.of(context);
    
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.search_off,
              size: 64,
              color: theme.colorScheme.onSurface.withOpacity(0.5),
            ),
            const SizedBox(height: 16),
            Text(
              'Product Not Found',
              style: theme.textTheme.headlineSmall?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'The product you are looking for could not be found.',
              style: theme.textTheme.bodyLarge,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 24),
            FilledButton(
              onPressed: () => context.pop(),
              child: const Text('Go Back'),
            ),
          ],
        ),
      ),
    );
  }

  bool _hasVariants(Product product) {
    final variants = product.attributes['variants'];
    return variants != null && variants is Map && variants.isNotEmpty;
  }

  void _showAddToCartSuccess(BuildContext context) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: const Row(
          children: [
            Icon(Icons.check_circle, color: Colors.white),
            SizedBox(width: 8),
            Text('Added to cart successfully!'),
          ],
        ),
        backgroundColor: Colors.green,
        behavior: SnackBarBehavior.floating,
        action: SnackBarAction(
          label: 'View Cart',
          textColor: Colors.white,
          onPressed: () {
            // TODO: Navigate to cart screen
          },
        ),
      ),
    );
  }
}
