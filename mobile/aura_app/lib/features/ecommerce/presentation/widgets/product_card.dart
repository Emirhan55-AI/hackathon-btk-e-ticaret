import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../../domain/entities/product.dart';
import 'rating_bar.dart';

/// A card widget to display product information in lists and grids
class ProductCard extends StatelessWidget {
  final Product product;
  final VoidCallback? onTap;
  final VoidCallback? onFavoritePressed;
  final bool isFavorite;
  final bool showAddToCart;
  final VoidCallback? onAddToCart;

  const ProductCard({
    super.key,
    required this.product,
    this.onTap,
    this.onFavoritePressed,
    this.isFavorite = false,
    this.showAddToCart = true,
    this.onAddToCart,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    
    return Card(
      clipBehavior: Clip.antiAlias,
      elevation: 2,
      child: InkWell(
        onTap: onTap,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Product Image
            Expanded(
              flex: 3,
              child: Stack(
                children: [
                  // Main Image
                  SizedBox(
                    width: double.infinity,
                    child: CachedNetworkImage(
                      imageUrl: product.primaryImage?.url ?? '',
                      fit: BoxFit.cover,
                      placeholder: (context, url) => Container(
                        color: colorScheme.surfaceVariant,
                        child: const Center(
                          child: CircularProgressIndicator(),
                        ),
                      ),
                      errorWidget: (context, url, error) => Container(
                        color: colorScheme.surfaceVariant,
                        child: Icon(
                          Icons.image_not_supported,
                          color: colorScheme.onSurfaceVariant,
                          size: 40,
                        ),
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
                          horizontal: 6,
                          vertical: 2,
                        ),
                        decoration: BoxDecoration(
                          color: colorScheme.error,
                          borderRadius: BorderRadius.circular(4),
                        ),
                        child: Text(
                          '-${product.computedDiscountPercentage?.toStringAsFixed(0)}%',
                          style: theme.textTheme.labelSmall?.copyWith(
                            color: colorScheme.onError,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ),
                  
                  // Favorite Button
                  if (onFavoritePressed != null)
                    Positioned(
                      top: 8,
                      right: 8,
                      child: Material(
                        color: Colors.white.withOpacity(0.9),
                        shape: const CircleBorder(),
                        child: InkWell(
                          onTap: onFavoritePressed,
                          customBorder: const CircleBorder(),
                          child: Padding(
                            padding: const EdgeInsets.all(6),
                            child: Icon(
                              isFavorite ? Icons.favorite : Icons.favorite_border,
                              color: isFavorite ? colorScheme.error : Colors.grey[600],
                              size: 18,
                            ),
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
                      style: theme.textTheme.bodyMedium?.copyWith(
                        fontWeight: FontWeight.w500,
                      ),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                    
                    const SizedBox(height: 4),
                    
                    // Rating
                    Row(
                      children: [
                        CustomRatingBar(
                          rating: product.rating,
                          size: 14,
                        ),
                        const SizedBox(width: 4),
                        Text(
                          '(${product.reviewCount})',
                          style: theme.textTheme.labelSmall?.copyWith(
                            color: colorScheme.onSurfaceVariant,
                          ),
                        ),
                      ],
                    ),
                    
                    const Spacer(),
                    
                    // Price Row
                    Row(
                      children: [
                        // Current Price
                        Text(
                          product.formattedPrice,
                          style: theme.textTheme.titleMedium?.copyWith(
                            fontWeight: FontWeight.bold,
                            color: colorScheme.primary,
                          ),
                        ),
                        
                        const SizedBox(width: 6),
                        
                        // Original Price (if discounted)
                        if (product.hasDiscount && product.formattedOriginalPrice != null)
                          Text(
                            product.formattedOriginalPrice!,
                            style: theme.textTheme.bodySmall?.copyWith(
                              decoration: TextDecoration.lineThrough,
                              color: colorScheme.onSurfaceVariant,
                            ),
                          ),
                        
                        const Spacer(),
                        
                        // Add to Cart Button
                        if (showAddToCart && product.inStock)
                          SizedBox(
                            height: 32,
                            child: IconButton.outlined(
                              onPressed: onAddToCart,
                              icon: const Icon(Icons.add_shopping_cart),
                              iconSize: 16,
                              style: IconButton.styleFrom(
                                padding: const EdgeInsets.all(4),
                              ),
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
