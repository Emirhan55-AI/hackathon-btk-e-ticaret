import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../notifiers/product_search_notifier.dart';
import '../notifiers/product_search_state.dart';
import '../widgets/product_card.dart';
import '../widgets/filter_bottom_sheet.dart';
import '../widgets/sort_bottom_sheet.dart';
import '../../domain/entities/product.dart';

/// Screen for searching and browsing products
class ProductSearchScreen extends ConsumerStatefulWidget {
  final String? initialQuery;
  final String? category;

  const ProductSearchScreen({
    super.key,
    this.initialQuery,
    this.category,
  });

  @override
  ConsumerState<ProductSearchScreen> createState() => _ProductSearchScreenState();
}

class _ProductSearchScreenState extends ConsumerState<ProductSearchScreen> {
  final TextEditingController _searchController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  late final ProductSearchNotifier _notifier;
  bool _isGridView = true;

  @override
  void initState() {
    super.initState();
    _notifier = ref.read(productSearchNotifierProvider.notifier);
    
    // Initialize search controller
    if (widget.initialQuery != null) {
      _searchController.text = widget.initialQuery!;
    }
    
    // Setup scroll listener for pagination
    _scrollController.addListener(_onScroll);
    
    // Perform initial search
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _performInitialSearch();
    });
  }

  @override
  void dispose() {
    _searchController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  void _performInitialSearch() {
    final query = widget.initialQuery ?? '';
    ProductFilter? filter;
    
    if (widget.category != null) {
      filter = ProductFilter(category: widget.category);
    }
    
    if (query.isNotEmpty || filter != null) {
      _notifier.searchProducts(query, filter: filter);
    }
  }

  void _onScroll() {
    if (_scrollController.position.pixels >= 
        _scrollController.position.maxScrollExtent - 200) {
      _notifier.loadMoreProducts();
    }
  }

  void _onSearchSubmitted(String query) {
    if (query.trim().isNotEmpty) {
      _notifier.searchProducts(query.trim());
    }
  }

  void _showFilterSheet() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(16)),
      ),
      builder: (context) => FilterBottomSheet(
        currentFilter: ref.read(productSearchNotifierProvider).activeFilter ?? const ProductFilter(),
        onApplyFilter: (filter) {
          _notifier.applyFilter(filter);
          Navigator.pop(context);
        },
      ),
    );
  }

  void _showSortSheet() {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(16)),
      ),
      builder: (context) => SortBottomSheet(
        currentSortBy: ref.read(productSearchNotifierProvider).activeFilter?.sortBy ?? ProductSortBy.relevance,
        currentSortOrder: ref.read(productSearchNotifierProvider).activeFilter?.sortOrder ?? SortOrder.asc,
        onSortChanged: (sortBy, sortOrder) {
          final currentFilter = ref.read(productSearchNotifierProvider).activeFilter ?? const ProductFilter();
          final newFilter = currentFilter.copyWith(
            sortBy: sortBy,
            sortOrder: sortOrder,
          );
          _notifier.applyFilter(newFilter);
          Navigator.pop(context);
        },
      ),
    );
  }

  void _toggleViewMode() {
    setState(() {
      _isGridView = !_isGridView;
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final state = ref.watch(productSearchNotifierProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Search Products'),
        bottom: PreferredSize(
          preferredSize: const Size.fromHeight(60),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: TextField(
              controller: _searchController,
              decoration: InputDecoration(
                hintText: 'Search products...',
                prefixIcon: const Icon(Icons.search),
                suffixIcon: _searchController.text.isNotEmpty
                    ? IconButton(
                        onPressed: () {
                          _searchController.clear();
                          _notifier.clearSearch();
                        },
                        icon: const Icon(Icons.clear),
                      )
                    : null,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                contentPadding: const EdgeInsets.symmetric(horizontal: 16),
              ),
              onSubmitted: _onSearchSubmitted,
              onChanged: (value) {
                setState(() {}); // Update suffix icon
              },
            ),
          ),
        ),
      ),
      body: Column(
        children: [
          // Filter and Sort Bar
          if (state.searchQuery.isNotEmpty) ...[
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              decoration: BoxDecoration(
                color: theme.colorScheme.surfaceVariant.withOpacity(0.3),
                border: Border(
                  bottom: BorderSide(
                    color: theme.colorScheme.outline.withOpacity(0.2),
                  ),
                ),
              ),
              child: Row(
                children: [
                  // Results Info
                  Expanded(
                    child: Text(
                      state.resultsInfo,
                      style: theme.textTheme.bodySmall,
                    ),
                  ),
                  
                  // Filter Button
                  IconButton(
                    onPressed: _showFilterSheet,
                    icon: Badge(
                      label: state.activeFilter != null && !state.activeFilter!.isEmpty
                          ? const Text('•')
                          : null,
                      child: const Icon(Icons.filter_list),
                    ),
                    tooltip: 'Filter',
                  ),
                  
                  // Sort Button
                  IconButton(
                    onPressed: _showSortSheet,
                    icon: const Icon(Icons.sort),
                    tooltip: 'Sort',
                  ),
                  
                  // View Mode Toggle
                  IconButton(
                    onPressed: _toggleViewMode,
                    icon: Icon(_isGridView ? Icons.view_list : Icons.grid_view),
                    tooltip: _isGridView ? 'List View' : 'Grid View',
                  ),
                ],
              ),
            ),
          ],
          
          // Content
          Expanded(
            child: _buildContent(state),
          ),
        ],
      ),
    );
  }

  Widget _buildContent(ProductSearchState state) {
    if (state.isLoading && state.products.isEmpty) {
      return const Center(child: CircularProgressIndicator());
    }
    
    if (state.hasError && state.products.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.error_outline,
              size: 64,
              color: Theme.of(context).colorScheme.error,
            ),
            const SizedBox(height: 16),
            Text(
              'Something went wrong',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 8),
            Text(
              state.error?.message ?? 'Please try again',
              style: Theme.of(context).textTheme.bodyMedium,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () => _notifier.refresh(),
              child: const Text('Retry'),
            ),
          ],
        ),
      );
    }
    
    if (state.products.isEmpty && state.searchQuery.isNotEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.search_off,
              size: 64,
              color: Theme.of(context).colorScheme.onSurfaceVariant,
            ),
            const SizedBox(height: 16),
            Text(
              'No products found',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 8),
            Text(
              'Try adjusting your search or filters',
              style: Theme.of(context).textTheme.bodyMedium,
            ),
          ],
        ),
      );
    }
    
    if (state.products.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.search,
              size: 64,
              color: Theme.of(context).colorScheme.onSurfaceVariant,
            ),
            const SizedBox(height: 16),
            Text(
              'Search for products',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 8),
            Text(
              'Enter a product name or browse categories',
              style: Theme.of(context).textTheme.bodyMedium,
            ),
          ],
        ),
      );
    }

    return _isGridView ? _buildGridView(state) : _buildListView(state);
  }

  Widget _buildGridView(ProductSearchState state) {
    return RefreshIndicator(
      onRefresh: () async => _notifier.refresh(),
      child: GridView.builder(
        controller: _scrollController,
        padding: const EdgeInsets.all(16),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 2,
          childAspectRatio: 0.7,
          crossAxisSpacing: 12,
          mainAxisSpacing: 12,
        ),
        itemCount: state.products.length + (state.canLoadMore ? 1 : 0),
        itemBuilder: (context, index) {
          if (index >= state.products.length) {
            return const Center(child: CircularProgressIndicator());
          }
          
          final product = state.products[index];
          return ProductCard(
            product: product,
            onTap: () => context.push('/product/${product.id}'),
            onAddToCart: () => _addToCart(product),
          );
        },
      ),
    );
  }

  Widget _buildListView(ProductSearchState state) {
    return RefreshIndicator(
      onRefresh: () async => _notifier.refresh(),
      child: ListView.builder(
        controller: _scrollController,
        padding: const EdgeInsets.all(16),
        itemCount: state.products.length + (state.canLoadMore ? 1 : 0),
        itemBuilder: (context, index) {
          if (index >= state.products.length) {
            return const Padding(
              padding: EdgeInsets.all(16),
              child: Center(child: CircularProgressIndicator()),
            );
          }
          
          final product = state.products[index];
          return Padding(
            padding: const EdgeInsets.only(bottom: 12),
            child: SizedBox(
              height: 120,
              child: ProductCard(
                product: product,
                onTap: () => context.push('/product/${product.id}'),
                onAddToCart: () => _addToCart(product),
              ),
            ),
          );
        },
      ),
    );
  }

  void _addToCart(Product product) {
    // TODO: Implement add to cart functionality
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('${product.name} added to cart'),
        action: SnackBarAction(
          label: 'View Cart',
          onPressed: () {
            // TODO: Navigate to cart
          },
        ),
      ),
    );
  }
}

// Providers
final productSearchNotifierProvider = 
    StateNotifierProvider<ProductSearchNotifier, ProductSearchState>((ref) {
  // TODO: Inject actual use cases from providers
  throw UnimplementedError('ProductSearchNotifier provider not implemented');
});
