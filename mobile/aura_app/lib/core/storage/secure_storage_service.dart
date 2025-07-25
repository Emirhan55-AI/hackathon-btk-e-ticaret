import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../constants/app_constants.dart';
import '../error/exceptions.dart';

/// Service for secure storage operations
class SecureStorageService {
  static const _storage = FlutterSecureStorage(
    aOptions: AndroidOptions(
      encryptedSharedPreferences: true,
    ),
    iOptions: IOSOptions(
      accessibility: KeychainAccessibility.first_unlock_this_device,
    ),
  );

  /// Store access token
  Future<void> setAccessToken(String token) async {
    try {
      await _storage.write(key: AppConstants.accessTokenKey, value: token);
    } catch (e) {
      throw CacheException(
        message: 'Failed to store access token',
        details: e.toString(),
      );
    }
  }

  /// Get access token
  Future<String?> getAccessToken() async {
    try {
      return await _storage.read(key: AppConstants.accessTokenKey);
    } catch (e) {
      throw CacheException(
        message: 'Failed to retrieve access token',
        details: e.toString(),
      );
    }
  }

  /// Store refresh token
  Future<void> setRefreshToken(String token) async {
    try {
      await _storage.write(key: AppConstants.refreshTokenKey, value: token);
    } catch (e) {
      throw CacheException(
        message: 'Failed to store refresh token',
        details: e.toString(),
      );
    }
  }

  /// Get refresh token
  Future<String?> getRefreshToken() async {
    try {
      return await _storage.read(key: AppConstants.refreshTokenKey);
    } catch (e) {
      throw CacheException(
        message: 'Failed to retrieve refresh token',
        details: e.toString(),
      );
    }
  }

  /// Store user ID
  Future<void> setUserId(String userId) async {
    try {
      await _storage.write(key: AppConstants.userIdKey, value: userId);
    } catch (e) {
      throw CacheException(
        message: 'Failed to store user ID',
        details: e.toString(),
      );
    }
  }

  /// Get user ID
  Future<String?> getUserId() async {
    try {
      return await _storage.read(key: AppConstants.userIdKey);
    } catch (e) {
      throw CacheException(
        message: 'Failed to retrieve user ID',
        details: e.toString(),
      );
    }
  }

  /// Store user email
  Future<void> setUserEmail(String email) async {
    try {
      await _storage.write(key: AppConstants.userEmailKey, value: email);
    } catch (e) {
      throw CacheException(
        message: 'Failed to store user email',
        details: e.toString(),
      );
    }
  }

  /// Get user email
  Future<String?> getUserEmail() async {
    try {
      return await _storage.read(key: AppConstants.userEmailKey);
    } catch (e) {
      throw CacheException(
        message: 'Failed to retrieve user email',
        details: e.toString(),
      );
    }
  }

  /// Check if user is logged in
  Future<bool> isLoggedIn() async {
    try {
      final accessToken = await getAccessToken();
      return accessToken != null && accessToken.isNotEmpty;
    } catch (e) {
      return false;
    }
  }

  /// Clear all stored data (logout)
  Future<void> clearAll() async {
    try {
      await _storage.deleteAll();
    } catch (e) {
      throw CacheException(
        message: 'Failed to clear stored data',
        details: e.toString(),
      );
    }
  }

  /// Clear specific key
  Future<void> clearKey(String key) async {
    try {
      await _storage.delete(key: key);
    } catch (e) {
      throw CacheException(
        message: 'Failed to clear stored data for key: $key',
        details: e.toString(),
      );
    }
  }

  /// Check if storage contains key
  Future<bool> containsKey(String key) async {
    try {
      return await _storage.containsKey(key: key);
    } catch (e) {
      return false;
    }
  }

  /// Get all stored keys
  Future<Map<String, String>> getAll() async {
    try {
      return await _storage.readAll();
    } catch (e) {
      throw CacheException(
        message: 'Failed to retrieve all stored data',
        details: e.toString(),
      );
    }
  }
}
