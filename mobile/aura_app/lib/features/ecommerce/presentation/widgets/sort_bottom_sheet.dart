import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../domain/entities/product.dart';

/// Bottom sheet for sorting products
class SortBottomSheet extends ConsumerWidget {
  final ProductSortBy currentSortBy;
  final SortOrder currentSortOrder;
  final Function(ProductSortBy, SortOrder) onSortChanged;

  const SortBottomSheet({
    super.key,
    required this.currentSortBy,
    required this.currentSortOrder,
    required this.onSortChanged,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Container(
      decoration: BoxDecoration(
        color: colorScheme.surface,
        borderRadius: const BorderRadius.vertical(top: Radius.circular(20)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Handle
          Container(
            width: 40,
            height: 4,
            margin: const EdgeInsets.symmetric(vertical: 12),
            decoration: BoxDecoration(
              color: colorScheme.onSurfaceVariant.withOpacity(0.4),
              borderRadius: BorderRadius.circular(2),
            ),
          ),

          // Header
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8),
            child: Row(
              children: [
                Text(
                  'Sort By',
                  style: theme.textTheme.headlineSmall?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const Spacer(),
                IconButton(
                  onPressed: () => Navigator.of(context).pop(),
                  icon: const Icon(Icons.close),
                ),
              ],
            ),
          ),

          const Divider(),

          // Sort Options
          Flexible(
            child: ListView(
              shrinkWrap: true,
              padding: const EdgeInsets.symmetric(horizontal: 8),
              children: [
                _buildSortOption(
                  context,
                  ProductSortBy.relevance,
                  'Relevance',
                  Icons.search,
                  'Most relevant results',
                ),
                _buildSortOption(
                  context,
                  ProductSortBy.name,
                  'Name',
                  Icons.sort_by_alpha,
                  'Alphabetical order',
                ),
                _buildSortOption(
                  context,
                  ProductSortBy.price,
                  'Price',
                  Icons.attach_money,
                  'By price range',
                ),
                _buildSortOption(
                  context,
                  ProductSortBy.rating,
                  'Rating',
                  Icons.star,
                  'By customer rating',
                ),
                _buildSortOption(
                  context,
                  ProductSortBy.newest,
                  'Newest',
                  Icons.new_releases,
                  'Latest products first',
                ),
                _buildSortOption(
                  context,
                  ProductSortBy.popular,
                  'Popular',
                  Icons.trending_up,
                  'Most popular items',
                ),
              ],
            ),
          ),

          const SizedBox(height: 16),
        ],
      ),
    );
  }

  Widget _buildSortOption(
    BuildContext context,
    ProductSortBy sortBy,
    String title,
    IconData icon,
    String subtitle,
  ) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    final isSelected = currentSortBy == sortBy;

    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
      elevation: 0,
      color: isSelected ? colorScheme.primaryContainer : null,
      child: ListTile(
        leading: Icon(
          icon,
          color: isSelected ? colorScheme.onPrimaryContainer : null,
        ),
        title: Text(
          title,
          style: TextStyle(
            fontWeight: isSelected ? FontWeight.w600 : FontWeight.normal,
            color: isSelected ? colorScheme.onPrimaryContainer : null,
          ),
        ),
        subtitle: Text(
          subtitle,
          style: TextStyle(
            color: isSelected 
                ? colorScheme.onPrimaryContainer.withOpacity(0.7) 
                : null,
          ),
        ),
        trailing: isSelected
            ? Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  // Sort order toggle for applicable sort types
                  if (_canToggleSortOrder(sortBy)) ...[
                    IconButton(
                      onPressed: () => _toggleSortOrder(sortBy),
                      icon: Icon(
                        currentSortOrder == SortOrder.asc
                            ? Icons.arrow_upward
                            : Icons.arrow_downward,
                        color: colorScheme.onPrimaryContainer,
                      ),
                      tooltip: currentSortOrder == SortOrder.asc
                          ? 'Ascending'
                          : 'Descending',
                    ),
                  ],
                  Icon(
                    Icons.check_circle,
                    color: colorScheme.onPrimaryContainer,
                  ),
                ],
              )
            : null,
        onTap: () => _selectSort(context, sortBy),
      ),
    );
  }

  bool _canToggleSortOrder(ProductSortBy sortBy) {
    // Only these sort types support order toggle
    return [
      ProductSortBy.name,
      ProductSortBy.price,
      ProductSortBy.rating,
      ProductSortBy.newest,
    ].contains(sortBy);
  }

  void _selectSort(BuildContext context, ProductSortBy sortBy) {
    // If same sort is selected, toggle order; otherwise use default order
    SortOrder newOrder = currentSortOrder;
    
    if (currentSortBy != sortBy) {
      // New sort selected, use default order
      newOrder = _getDefaultSortOrder(sortBy);
    }

    onSortChanged(sortBy, newOrder);
    // Don't close immediately for order toggle, but close for new selection
    if (currentSortBy != sortBy) {
      Navigator.of(context).pop();
    }
  }

  void _toggleSortOrder(ProductSortBy sortBy) {
    final newOrder = currentSortOrder == SortOrder.asc 
        ? SortOrder.desc 
        : SortOrder.asc;
    
    onSortChanged(sortBy, newOrder);
  }

  SortOrder _getDefaultSortOrder(ProductSortBy sortBy) {
    switch (sortBy) {
      case ProductSortBy.relevance:
      case ProductSortBy.popular:
        return SortOrder.desc; // Most relevant/popular first
      case ProductSortBy.name:
        return SortOrder.asc; // A-Z
      case ProductSortBy.price:
        return SortOrder.asc; // Low to high
      case ProductSortBy.rating:
        return SortOrder.desc; // Highest rating first
      case ProductSortBy.newest:
        return SortOrder.desc; // Newest first
    }
  }

  /// Show sort bottom sheet
  static Future<void> show(
    BuildContext context, {
    required ProductSortBy currentSortBy,
    required SortOrder currentSortOrder,
    required Function(ProductSortBy, SortOrder) onSortChanged,
  }) {
    return showModalBottomSheet<void>(
      context: context,
      backgroundColor: Colors.transparent,
      builder: (context) => SortBottomSheet(
        currentSortBy: currentSortBy,
        currentSortOrder: currentSortOrder,
        onSortChanged: onSortChanged,
      ),
    );
  }
}
