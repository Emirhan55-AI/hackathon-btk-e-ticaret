import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../entities/user.dart';

/// Abstract repository interface for authentication operations
abstract class AuthRepository {
  /// Login user with email and password
  Future<Either<Failure, User>> login(String email, String password);

  /// Register new user
  Future<Either<Failure, User>> register({
    required String email,
    required String password,
    String? firstName,
    String? lastName,
  });

  /// Logout current user
  Future<Either<Failure, void>> logout();

  /// Get current authenticated user
  Future<Either<Failure, User>> getCurrentUser();

  /// Refresh authentication token
  Future<Either<Failure, User>> refreshToken();

  /// Update user profile
  Future<Either<Failure, User>> updateProfile({
    String? firstName,
    String? lastName,
    String? profileImage,
    DateTime? dateOfBirth,
    String? gender,
  });

  /// Change user password
  Future<Either<Failure, void>> changePassword({
    required String currentPassword,
    required String newPassword,
  });

  /// Delete user account
  Future<Either<Failure, void>> deleteAccount();
}
  final AuthToken token;

  const AuthResult({
    required this.user,
    required this.token,
  });

  factory AuthResult.fromJson(Map<String, dynamic> json) {
    return AuthResult(
      user: User.fromJson(json['user'] ?? {}),
      token: AuthToken.fromJson(json['token'] ?? json),
    );
  }
}

/// Abstract authentication repository
abstract class AuthRepository {
  /// Login with email and password
  Future<Either<Failure, AuthResult>> login(LoginRequest request);

  /// Register new user
  Future<Either<Failure, AuthResult>> register(RegisterRequest request);

  /// Logout current user
  Future<Either<Failure, void>> logout();

  /// Refresh authentication token
  Future<Either<Failure, AuthToken>> refreshToken(String refreshToken);

  /// Get current user profile
  Future<Either<Failure, User?>> getCurrentUser();

  /// Update user profile
  Future<Either<Failure, User>> updateProfile(Map<String, dynamic> updates);

  /// Change password
  Future<Either<Failure, void>> changePassword({
    required String currentPassword,
    required String newPassword,
  });

  /// Send password reset email
  Future<Either<Failure, void>> sendPasswordResetEmail(String email);

  /// Reset password with token
  Future<Either<Failure, void>> resetPassword({
    required String token,
    required String newPassword,
  });

  /// Verify email with token
  Future<Either<Failure, void>> verifyEmail(String token);

  /// Resend email verification
  Future<Either<Failure, void>> resendEmailVerification();

  /// Delete user account
  Future<Either<Failure, void>> deleteAccount();
}
