/// API constants for the Aura backend
class ApiConstants {
  static const String baseUrl = 'http://localhost:8000';
  
  // Auth endpoints
  static const String loginEndpoint = '/api/v1/auth/login';
  static const String registerEndpoint = '/api/v1/auth/register';
  static const String logoutEndpoint = '/api/v1/auth/logout';
  static const String refreshEndpoint = '/api/v1/auth/refresh';
  
  // Wardrobe endpoints
  static const String wardrobeItemsEndpoint = '/api/v1/wardrobe/items';
  
  // Recommendations endpoints
  static const String recommendationsEndpoint = '/api/v1/recommendations/outfits';
  
  // E-commerce endpoints
  static const String ecommerceTrendingEndpoint = '/api/v1/ecommerce/trending';
  static const String ecommerceSearchEndpoint = '/api/v1/ecommerce/search';
  static const String ecommerceProductEndpoint = '/api/v1/ecommerce/products';
  
  // Cart endpoints
  static const String cartEndpoint = '/api/v1/cart';
  static const String cartItemsEndpoint = '/api/v1/cart/items';
  static const String wishlistEndpoint = '/api/v1/cart/wishlist';
  
  // Request timeouts
  static const Duration connectionTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 30);
}
