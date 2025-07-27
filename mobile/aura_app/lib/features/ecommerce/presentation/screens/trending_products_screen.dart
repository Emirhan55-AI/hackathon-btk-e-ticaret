import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../widgets/product_card.dart';
import '../../domain/entities/product.dart';

/// Screen showing trending and popular products
class TrendingProductsScreen extends ConsumerStatefulWidget {
  final String? category;

  const TrendingProductsScreen({
    super.key,
    this.category,
  });

  @override
  ConsumerState<TrendingProductsScreen> createState() => _TrendingProductsScreenState();
}

class _TrendingProductsScreenState extends ConsumerState<TrendingProductsScreen>
    with TickerProviderStateMixin {
  late TabController _tabController;
  late ScrollController _scrollController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 4, vsync: this);
    _scrollController = ScrollController();
  }

  @override
  void dispose() {
    _tabController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: CustomScrollView(
        controller: _scrollController,
        slivers: [
          // App bar with tabs
          _buildSliverAppBar(context),
          
          // Tab content
          SliverFillRemaining(
            child: TabBarView(
              controller: _tabController,
              children: [
                _buildTrendingTab(context),
                _buildPopularTab(context),
                _buildNewArrivalsTab(context),
                _buildTopRatedTab(context),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSliverAppBar(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return SliverAppBar(
      expandedHeight: 120,
      pinned: true,
      backgroundColor: colorScheme.surface,
      foregroundColor: colorScheme.onSurface,
      flexibleSpace: FlexibleSpaceBar(
        title: Text(
          widget.category != null 
              ? 'Trending in ${widget.category}'
              : 'Trending Products',
          style: theme.textTheme.titleLarge?.copyWith(
            fontWeight: FontWeight.bold,
          ),
        ),
        titlePadding: const EdgeInsets.only(left: 16, bottom: 60),
      ),
      bottom: TabBar(
        controller: _tabController,
        isScrollable: true,
        tabAlignment: TabAlignment.start,
        tabs: const [
          Tab(text: 'Trending'),
          Tab(text: 'Popular'),
          Tab(text: 'New'),
          Tab(text: 'Top Rated'),
        ],
      ),
    );
  }

  Widget _buildTrendingTab(BuildContext context) {
    return _buildProductGrid(
      context: context,
      products: _getTrendingProducts(),
      emptyMessage: 'No trending products found',
    );
  }

  Widget _buildPopularTab(BuildContext context) {
    return _buildProductGrid(
      context: context,
      products: _getPopularProducts(),
      emptyMessage: 'No popular products found',
    );
  }

  Widget _buildNewArrivalsTab(BuildContext context) {
    return _buildProductGrid(
      context: context,
      products: _getNewProducts(),
      emptyMessage: 'No new arrivals found',
    );
  }

  Widget _buildTopRatedTab(BuildContext context) {
    return _buildProductGrid(
      context: context,
      products: _getTopRatedProducts(),
      emptyMessage: 'No top rated products found',
    );
  }

  Widget _buildProductGrid({
    required BuildContext context,
    required List<Product> products,
    required String emptyMessage,
  }) {
    if (products.isEmpty) {
      return _buildEmptyState(context, emptyMessage);
    }

    return RefreshIndicator(
      onRefresh: () async {
        // TODO: Implement refresh logic
        await Future.delayed(const Duration(seconds: 1));
      },
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: GridView.builder(
          physics: const AlwaysScrollableScrollPhysics(),
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2,
            childAspectRatio: 0.75,
            crossAxisSpacing: 16,
            mainAxisSpacing: 16,
          ),
          itemCount: products.length,
          itemBuilder: (context, index) {
            final product = products[index];
            return ProductCard(
              product: product,
              onTap: () => _navigateToProductDetail(context, product),
            );
          },
        ),
      ),
    );
  }

  Widget _buildEmptyState(BuildContext context, String message) {
    final theme = Theme.of(context);
    
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.trending_up_outlined,
              size: 64,
              color: theme.colorScheme.onSurface.withOpacity(0.5),
            ),
            const SizedBox(height: 16),
            Text(
              'No Products Found',
              style: theme.textTheme.headlineSmall?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              message,
              style: theme.textTheme.bodyLarge,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 24),
            FilledButton.icon(
              onPressed: () {
                // TODO: Navigate to search or refresh
              },
              icon: const Icon(Icons.refresh),
              label: const Text('Refresh'),
            ),
          ],
        ),
      ),
    );
  }

  void _navigateToProductDetail(BuildContext context, Product product) {
    // TODO: Navigate to product detail screen
    // context.push('/product/${product.id}', extra: product);
    
    // For now, show a snackbar
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Navigate to ${product.name}'),
        behavior: SnackBarBehavior.floating,
      ),
    );
  }

  // API integration ready - using mock data for demo purposes
  List<Product> _getTrendingProducts() {
    return [
      Product(
        id: 'trending_1',
        name: 'Wireless Earbuds Pro',
        description: 'High-quality wireless earbuds with noise cancellation',
        price: 149.99,
        originalPrice: 199.99,
        currency: '\$',
        category: 'Electronics',
        brand: 'TechBrand',
        sku: 'WE-PRO-001',
        images: [
          const ProductImage(
            id: 'img1',
            url: 'https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=300&h=300&fit=crop',
            altText: 'Wireless Earbuds',
            isMain: true,
          ),
        ],
        rating: 4.5,
        reviewCount: 128,
        stockQuantity: 25,
        attributes: {
          'variants': {
            'Color': ['Black', 'White', 'Blue'],
          },
        },
      ),
      Product(
        id: 'trending_2',
        name: 'Smart Fitness Watch',
        description: 'Advanced fitness tracking with heart rate monitor',
        price: 299.99,
        currency: '\$',
        category: 'Electronics',
        brand: 'FitTech',
        sku: 'SFW-001',
        images: [
          const ProductImage(
            id: 'img2',
            url: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300&h=300&fit=crop',
            altText: 'Fitness Watch',
            isMain: true,
          ),
        ],
        rating: 4.8,
        reviewCount: 89,
        stockQuantity: 15,
        attributes: {
          'variants': {
            'Size': ['38mm', '42mm'],
            'Color': ['Silver', 'Gold', 'Space Gray'],
          },
        },
      ),
      Product(
        id: 'trending_3',
        name: 'Portable Bluetooth Speaker',
        description: 'Waterproof speaker with 360-degree sound',
        price: 89.99,
        originalPrice: 119.99,
        currency: '\$',
        category: 'Electronics',
        brand: 'SoundWave',
        sku: 'PBS-360',
        images: [
          const ProductImage(
            id: 'img3',
            url: 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=300&h=300&fit=crop',
            altText: 'Bluetooth Speaker',
            isMain: true,
          ),
        ],
        rating: 4.3,
        reviewCount: 67,
        stockQuantity: 30,
      ),
      Product(
        id: 'trending_4',
        name: 'Wireless Charging Pad',
        description: 'Fast wireless charging for all Qi-enabled devices',
        price: 39.99,
        currency: '\$',
        category: 'Electronics',
        brand: 'ChargeTech',
        sku: 'WCP-FAST',
        images: [
          const ProductImage(
            id: 'img4',
            url: 'https://via.placeholder.com/300x300/9B59B6/FFFFFF?text=Charger',
            altText: 'Wireless Charger',
            isMain: true,
          ),
        ],
        rating: 4.1,
        reviewCount: 45,
        stockQuantity: 50,
      ),
    ];
  }

  List<Product> _getPopularProducts() {
    return [
      Product(
        id: 'popular_1',
        name: 'Laptop Stand Adjustable',
        description: 'Ergonomic aluminum laptop stand',
        price: 59.99,
        currency: '\$',
        category: 'Accessories',
        brand: 'ErgoDesk',
        sku: 'LSA-001',
        images: [
          const ProductImage(
            id: 'img5',
            url: 'https://via.placeholder.com/300x300/E74C3C/FFFFFF?text=Stand',
            altText: 'Laptop Stand',
            isMain: true,
          ),
        ],
        rating: 4.6,
        reviewCount: 156,
        stockQuantity: 20,
      ),
      Product(
        id: 'popular_2',
        name: 'USB-C Hub 7-in-1',
        description: 'Multi-port hub with 4K HDMI, USB 3.0, and SD card reader',
        price: 79.99,
        originalPrice: 99.99,
        currency: '\$',
        category: 'Accessories',
        brand: 'ConnectPro',
        sku: 'UCH-7IN1',
        images: [
          const ProductImage(
            id: 'img6',
            url: 'https://via.placeholder.com/300x300/F39C12/FFFFFF?text=Hub',
            altText: 'USB-C Hub',
            isMain: true,
          ),
        ],
        rating: 4.4,
        reviewCount: 92,
        stockQuantity: 35,
      ),
    ];
  }

  List<Product> _getNewProducts() {
    return [
      Product(
        id: 'new_1',
        name: 'Smart Home Camera',
        description: '4K security camera with AI detection',
        price: 199.99,
        currency: '\$',
        category: 'Smart Home',
        brand: 'SecureTech',
        sku: 'SHC-4K',
        images: [
          const ProductImage(
            id: 'img7',
            url: 'https://via.placeholder.com/300x300/1ABC9C/FFFFFF?text=Camera',
            altText: 'Smart Camera',
            isMain: true,
          ),
        ],
        rating: 4.7,
        reviewCount: 23,
        stockQuantity: 12,
        createdAt: DateTime.now().subtract(const Duration(days: 5)),
      ),
    ];
  }

  List<Product> _getTopRatedProducts() {
    return [
      Product(
        id: 'rated_1',
        name: 'Premium Keyboard',
        description: 'Mechanical keyboard with RGB backlighting',
        price: 159.99,
        currency: '\$',
        category: 'Accessories',
        brand: 'KeyMaster',
        sku: 'PKB-RGB',
        images: [
          const ProductImage(
            id: 'img8',
            url: 'https://via.placeholder.com/300x300/8E44AD/FFFFFF?text=Keyboard',
            altText: 'Mechanical Keyboard',
            isMain: true,
          ),
        ],
        rating: 4.9,
        reviewCount: 234,
        stockQuantity: 18,
        attributes: {
          'variants': {
            'Switch Type': ['Blue', 'Brown', 'Red'],
            'Layout': ['US', 'UK', 'German'],
          },
        },
      ),
    ];
  }
}
