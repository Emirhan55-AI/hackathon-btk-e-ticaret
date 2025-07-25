import '../models/user_model.dart';

/// Abstract interface for authentication remote data source
abstract class AuthRemoteDataSource {
  /// Login user with email and password
  Future<UserModel> login(String email, String password);

  /// Register new user
  Future<UserModel> register({
    required String email,
    required String password,
    String? firstName,
    String? lastName,
  });

  /// Logout current user
  Future<void> logout();

  /// Get current authenticated user
  Future<UserModel> getCurrentUser();

  /// Refresh authentication token
  Future<UserModel> refreshToken();

  /// Update user profile
  Future<UserModel> updateProfile({
    String? firstName,
    String? lastName,
    String? profileImage,
    DateTime? dateOfBirth,
    String? gender,
  });

  /// Change user password
  Future<void> changePassword({
    required String currentPassword,
    required String newPassword,
  });

  /// Delete user account
  Future<void> deleteAccount();
}
