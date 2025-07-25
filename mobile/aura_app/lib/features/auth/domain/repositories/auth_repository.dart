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
