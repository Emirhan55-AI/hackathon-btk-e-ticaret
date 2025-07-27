import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../domain/entities/product.dart';
import '../providers/cart_notifier.dart';
import '../providers/favorites_notifier.dart';

class ProductCard extends ConsumerWidget {
  final Product product;
  final VoidCallback? onTap;
  final bool showFavoriteButton;

  const ProductCard({
    super.key,
    required this.product,
    this.onTap,
    this.showFavoriteButton = true,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    final favorites = ref.watch(favoritesNotifierProvider);
    final isFavorite = favorites.contains(product.id);

    return Card(
      clipBehavior: Clip.antiAlias,
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Product Image Section
            Expanded(
              flex: 3,
              child: Stack(
                children: [
                  // Product Image
                  Container(
                    width: double.infinity,
                    decoration: BoxDecoration(
                      color: colorScheme.surfaceVariant.withOpacity(0.3),
                    ),
                    child: product.primaryImage?.url != null
                        ? ClipRRect(
                            borderRadius: const BorderRadius.vertical(
                              top: Radius.circular(12),
                            ),
                            child: Image.network(
                              product.primaryImage!.url,
                              fit: BoxFit.cover,
                              errorBuilder: (context, error, stackTrace) {
                                return Container(
                                  color: colorScheme.surfaceVariant,
                                  child: Icon(
                                    Icons.image_not_supported,
                                    color: colorScheme.onSurfaceVariant,
                                    size: 48,
                                  ),
                                );
                              },
                            ),
                          )
                        : Container(
                            color: colorScheme.surfaceVariant,
                            child: Icon(
                              Icons.image,
                              color: colorScheme.onSurfaceVariant,
                              size: 48,
                            ),
                          ),
                  ),
                  
                  // Favorite Button
                  Positioned(
                    top: 8,
                    right: 8,
                    child: Container(
                      decoration: BoxDecoration(
                        color: Colors.white.withOpacity(0.9),
                        shape: BoxShape.circle,
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withOpacity(0.1),
                            blurRadius: 4,
                            offset: const Offset(0, 2),
                          ),
                        ],
                      ),
                      child: IconButton(
                        onPressed: () {
                          ref.read(favoritesNotifierProvider.notifier).toggleFavorite(product.id);
                        },
                        icon: Icon(
                          isFavorite ? Icons.favorite : Icons.favorite_border,
                          color: isFavorite ? Colors.red : Colors.grey[600],
                          size: 20,
                        ),
                        constraints: const BoxConstraints(
                          minWidth: 36,
                          minHeight: 36,
                        ),
                        padding: const EdgeInsets.all(8),
                      ),
                    ),
                  ),
                  
                  // Discount Badge
                  if (product.hasDiscount)
                    Positioned(
                      top: 8,
                      left: 8,
                      child: Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 8,
                          vertical: 4,
                        ),
                        decoration: BoxDecoration(
                          color: colorScheme.error,
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Text(
                          '-${product.computedDiscountPercentage?.toInt() ?? 0}%',
                          style: theme.textTheme.labelSmall?.copyWith(
                            color: colorScheme.onError,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ),
                  
                  // Stock Status
                  if (!product.inStock)
                    Positioned.fill(
                      child: Container(
                        color: Colors.black.withOpacity(0.6),
                        child: Center(
                          child: Text(
                            'OUT OF STOCK',
                            style: theme.textTheme.labelMedium?.copyWith(
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ),
                    ),
                ],
              ),
            ),
            
            // Product Information
            Expanded(
              flex: 2,
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Brand
                    if (product.brand != null)
                      Text(
                        product.brand!,
                        style: theme.textTheme.labelSmall?.copyWith(
                          color: colorScheme.primary,
                          fontWeight: FontWeight.w500,
                        ),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                    
                    const SizedBox(height: 2),
                    
                    // Product Name
                    Text(
                      product.name,
                      style: theme.textTheme.titleSmall?.copyWith(
                        fontWeight: FontWeight.w600,
                      ),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                    
                    const SizedBox(height: 4),
                    
                    // Rating
                    if (product.rating > 0)
                      Row(
                        children: [
                          Icon(
                            Icons.star,
                            color: Colors.amber,
                            size: 16,
                          ),
                          const SizedBox(width: 4),
                          Text(
                            product.rating.toStringAsFixed(1),
                            style: theme.textTheme.labelSmall?.copyWith(
                              color: colorScheme.onSurfaceVariant,
                            ),
                          ),
                          if (product.reviewCount > 0) ...[
                            const SizedBox(width: 4),
                            Text(
                              '(${product.reviewCount})',
                              style: theme.textTheme.labelSmall?.copyWith(
                                color: colorScheme.onSurfaceVariant,
                              ),
                            ),
                          ],
                        ],
                      ),
                    
                    const Spacer(),
                    
                    // Price Section
                    Row(
                      children: [
                        // Current Price
                        Text(
                          '\$${product.price.toStringAsFixed(2)}',
                          style: theme.textTheme.titleMedium?.copyWith(
                            fontWeight: FontWeight.bold,
                            color: colorScheme.primary,
                          ),
                        ),
                        
                        // Original Price (if discounted)
                        if (product.originalPrice != null && product.originalPrice! > product.price) ...[
                          const SizedBox(width: 8),
                          Text(
                            '\$${product.originalPrice!.toStringAsFixed(2)}',
                            style: theme.textTheme.labelMedium?.copyWith(
                              decoration: TextDecoration.lineThrough,
                              color: colorScheme.onSurfaceVariant,
                            ),
                          ),
                        ],
                        
                        const Spacer(),
                        
                        // Add to Cart Button
                        Container(
                          decoration: BoxDecoration(
                            color: product.inStock ? colorScheme.primary : colorScheme.surfaceVariant,
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: IconButton(
                            onPressed: product.inStock
                                ? () {
                                    ref.read(cartNotifierProvider.notifier).addToCart(product, 1);
                                    ScaffoldMessenger.of(context).showSnackBar(
                                      SnackBar(
                                        content: Text('${product.name} added to cart'),
                                        duration: const Duration(seconds: 2),
                                      ),
                                    );
                                  }
                                : null,
                            icon: Icon(
                              Icons.add_shopping_cart,
                              color: product.inStock ? colorScheme.onPrimary : colorScheme.onSurfaceVariant,
                              size: 20,
                            ),
                            constraints: const BoxConstraints(
                              minWidth: 32,
                              minHeight: 32,
                            ),
                            padding: const EdgeInsets.all(6),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
