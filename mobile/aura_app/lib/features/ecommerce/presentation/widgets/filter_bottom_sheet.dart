import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../domain/entities/product.dart';

/// Bottom sheet for filtering products
class FilterBottomSheet extends ConsumerStatefulWidget {
  final ProductFilter currentFilter;
  final Function(ProductFilter) onApplyFilter;
  final List<String> availableCategories;
  final List<String> availableBrands;

  const FilterBottomSheet({
    super.key,
    required this.currentFilter,
    required this.onApplyFilter,
    this.availableCategories = const [],
    this.availableBrands = const [],
  });

  @override
  ConsumerState<FilterBottomSheet> createState() => _FilterBottomSheetState();

  /// Show filter bottom sheet
  static Future<void> show(
    BuildContext context, {
    required ProductFilter currentFilter,
    required Function(ProductFilter) onApplyFilter,
    List<String> availableCategories = const [],
    List<String> availableBrands = const [],
  }) {
    return showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => FilterBottomSheet(
        currentFilter: currentFilter,
        onApplyFilter: onApplyFilter,
        availableCategories: availableCategories,
        availableBrands: availableBrands,
      ),
    );
  }
}

class _FilterBottomSheetState extends ConsumerState<FilterBottomSheet> {
  late ProductFilter _filter;
  final TextEditingController _minPriceController = TextEditingController();
  final TextEditingController _maxPriceController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _filter = widget.currentFilter;
    _minPriceController.text = _filter.minPrice?.toString() ?? '';
    _maxPriceController.text = _filter.maxPrice?.toString() ?? '';
  }

  @override
  void dispose() {
    _minPriceController.dispose();
    _maxPriceController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Container(
      decoration: BoxDecoration(
        color: colorScheme.surface,
        borderRadius: const BorderRadius.vertical(top: Radius.circular(20)),
      ),
      child: DraggableScrollableSheet(
        initialChildSize: 0.8,
        minChildSize: 0.5,
        maxChildSize: 0.95,
        builder: (context, scrollController) {
          return Column(
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
                padding: const EdgeInsets.symmetric(horizontal: 24),
                child: Row(
                  children: [
                    Text(
                      'Filter Products',
                      style: theme.textTheme.headlineSmall?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const Spacer(),
                    TextButton(
                      onPressed: _resetFilters,
                      child: const Text('Reset'),
                    ),
                  ],
                ),
              ),

              const Divider(),

              // Filter Content
              Expanded(
                child: ListView(
                  controller: scrollController,
                  padding: const EdgeInsets.symmetric(horizontal: 24),
                  children: [
                    // Category Filter
                    if (widget.availableCategories.isNotEmpty) ...[
                      _buildSectionTitle('Category'),
                      _buildCategoryFilter(),
                      const SizedBox(height: 24),
                    ],

                    // Brand Filter
                    if (widget.availableBrands.isNotEmpty) ...[
                      _buildSectionTitle('Brand'),
                      _buildBrandFilter(),
                      const SizedBox(height: 24),
                    ],

                    // Price Range Filter
                    _buildSectionTitle('Price Range'),
                    _buildPriceRangeFilter(),
                    const SizedBox(height: 24),

                    // Rating Filter
                    _buildSectionTitle('Minimum Rating'),
                    _buildRatingFilter(),
                    const SizedBox(height: 24),

                    // Stock Filter
                    _buildSectionTitle('Availability'),
                    _buildStockFilter(),
                    const SizedBox(height: 24),

                    // Discount Filter
                    _buildSectionTitle('Special Offers'),
                    _buildDiscountFilter(),
                    const SizedBox(height: 100), // Space for bottom buttons
                  ],
                ),
              ),

              // Bottom Actions
              Container(
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  color: colorScheme.surface,
                  border: Border(
                    top: BorderSide(
                      color: colorScheme.outlineVariant.withOpacity(0.5),
                    ),
                  ),
                ),
                child: Row(
                  children: [
                    Expanded(
                      child: OutlinedButton(
                        onPressed: () => Navigator.of(context).pop(),
                        child: const Text('Cancel'),
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: FilledButton(
                        onPressed: _applyFilters,
                        child: const Text('Apply Filters'),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          );
        },
      ),
    );
  }

  Widget _buildSectionTitle(String title) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Text(
        title,
        style: Theme.of(context).textTheme.titleMedium?.copyWith(
          fontWeight: FontWeight.w600,
        ),
      ),
    );
  }

  Widget _buildCategoryFilter() {
    return Wrap(
      spacing: 8,
      runSpacing: 8,
      children: widget.availableCategories.map((category) {
        final isSelected = _filter.category == category;
        return FilterChip(
          label: Text(category),
          selected: isSelected,
          onSelected: (selected) {
            setState(() {
              _filter = _filter.copyWith(
                category: selected ? category : null,
              );
            });
          },
        );
      }).toList(),
    );
  }

  Widget _buildBrandFilter() {
    return Wrap(
      spacing: 8,
      runSpacing: 8,
      children: widget.availableBrands.map((brand) {
        final isSelected = _filter.brand == brand;
        return FilterChip(
          label: Text(brand),
          selected: isSelected,
          onSelected: (selected) {
            setState(() {
              _filter = _filter.copyWith(
                brand: selected ? brand : null,
              );
            });
          },
        );
      }).toList(),
    );
  }

  Widget _buildPriceRangeFilter() {
    return Row(
      children: [
        Expanded(
          child: TextField(
            controller: _minPriceController,
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(
              labelText: 'Min Price',
              prefixText: '\$ ',
              border: OutlineInputBorder(),
            ),
            onChanged: (value) {
              final price = double.tryParse(value);
              setState(() {
                _filter = _filter.copyWith(minPrice: price);
              });
            },
          ),
        ),
        const SizedBox(width: 16),
        const Text('to'),
        const SizedBox(width: 16),
        Expanded(
          child: TextField(
            controller: _maxPriceController,
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(
              labelText: 'Max Price',
              prefixText: '\$ ',
              border: OutlineInputBorder(),
            ),
            onChanged: (value) {
              final price = double.tryParse(value);
              setState(() {
                _filter = _filter.copyWith(maxPrice: price);
              });
            },
          ),
        ),
      ],
    );
  }

  Widget _buildRatingFilter() {
    return Column(
      children: [1, 2, 3, 4, 5].map((rating) {
        final isSelected = _filter.minRating == rating.toDouble();
        return RadioListTile<double>(
          title: Row(
            children: [
              ...List.generate(5, (index) {
                return Icon(
                  index < rating ? Icons.star : Icons.star_border,
                  color: Colors.amber,
                  size: 20,
                );
              }),
              const SizedBox(width: 8),
              Text('$rating stars & up'),
            ],
          ),
          value: rating.toDouble(),
          groupValue: _filter.minRating,
          onChanged: (value) {
            setState(() {
              _filter = _filter.copyWith(
                minRating: isSelected ? null : value,
              );
            });
          },
          contentPadding: EdgeInsets.zero,
        );
      }).toList(),
    );
  }

  Widget _buildStockFilter() {
    return SwitchListTile(
      title: const Text('In Stock Only'),
      subtitle: const Text('Show only available products'),
      value: _filter.inStock,
      onChanged: (value) {
        setState(() {
          _filter = _filter.copyWith(inStock: value);
        });
      },
      contentPadding: EdgeInsets.zero,
    );
  }

  Widget _buildDiscountFilter() {
    return SwitchListTile(
      title: const Text('On Sale'),
      subtitle: const Text('Show only discounted products'),
      value: _filter.hasDiscount,
      onChanged: (value) {
        setState(() {
          _filter = _filter.copyWith(hasDiscount: value);
        });
      },
      contentPadding: EdgeInsets.zero,
    );
  }

  void _resetFilters() {
    setState(() {
      _filter = const ProductFilter();
      _minPriceController.clear();
      _maxPriceController.clear();
    });
  }

  void _applyFilters() {
    widget.onApplyFilter(_filter);
    Navigator.of(context).pop();
  }
}
