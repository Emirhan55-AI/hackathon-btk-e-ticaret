import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../features/auth/presentation/screens/simple_home_screen.dart';
import '../../features/auth/presentation/pages/login_screen.dart';
import '../../features/auth/presentation/pages/register_screen.dart';
import '../../features/ecommerce/presentation/pages/product_search_page.dart';
import '../../features/ecommerce/presentation/screens/product_detail_screen.dart';
import '../../features/ecommerce/presentation/screens/trending_products_screen.dart';
import '../../features/ecommerce/presentation/screens/favorites_screen.dart';
import '../../features/ecommerce/presentation/screens/cart_screen.dart';
import '../../features/ecommerce/presentation/screens/profile_screen.dart';
import '../../features/recommendations/presentation/pages/outfit_recommendations_page.dart';

/// Complete app router with all essential routes for Phase 1
final appRouterProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    initialLocation: '/home',
    routes: [
      // Home route
      GoRoute(
        path: '/home',
        builder: (context, state) => const HomeScreen(),
      ),
      
      // Auth routes
      GoRoute(
        path: '/login',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: '/register',
        builder: (context, state) => const RegisterScreen(),
      ),
      
      // E-commerce routes
      GoRoute(
        path: '/search',
        builder: (context, state) {
          final query = state.uri.queryParameters['q'];
          return ProductSearchPage(initialQuery: query);
        },
      ),
      GoRoute(
        path: '/trending',
        builder: (context, state) => const TrendingProductsScreen(),
      ),
      GoRoute(
        path: '/product/:id',
        builder: (context, state) {
          final productId = state.pathParameters['id']!;
          return ProductDetailScreen(productId: productId);
        },
      ),
      
      // Additional e-commerce routes
      GoRoute(
        path: '/favorites',
        builder: (context, state) => const FavoritesScreen(),
      ),
      GoRoute(
        path: '/cart',
        builder: (context, state) => const CartScreen(),
      ),
      GoRoute(
        path: '/profile',
        builder: (context, state) => const ProfileScreen(),
      ),
      
      // Recommendations routes
      GoRoute(
        path: '/recommendations',
        builder: (context, state) => const OutfitRecommendationsPage(),
      ),
    ],
  );
});