/// Application-wide constants
class AppConstants {
  // App Info
  static const String appName = 'Aura';
  static const String appVersion = '1.0.0';
  
  // API Configuration
  static const String apiBaseUrl = 'http://localhost:8000/api/v1/';
  static const Duration requestTimeout = Duration(seconds: 30);
  
  // Storage Keys
  static const String accessTokenKey = 'access_token';
  static const String refreshTokenKey = 'refresh_token';
  static const String userIdKey = 'user_id';
  static const String userEmailKey = 'user_email';
  
  // Image sizes
  static const double imageQuality = 0.8;
  static const int maxImageWidth = 1024;
  static const int maxImageHeight = 1024;
  
  // UI Constants
  static const double defaultPadding = 16.0;
  static const double smallPadding = 8.0;
  static const double largePadding = 24.0;
  static const double borderRadius = 12.0;
  static const double smallBorderRadius = 8.0;
  static const double largeBorderRadius = 16.0;
  
  // Animation Durations
  static const Duration shortAnimation = Duration(milliseconds: 200);
  static const Duration mediumAnimation = Duration(milliseconds: 400);
  static const Duration longAnimation = Duration(milliseconds: 600);
  
  // Validation
  static const int minPasswordLength = 6;
  static const int maxPasswordLength = 128;
}
