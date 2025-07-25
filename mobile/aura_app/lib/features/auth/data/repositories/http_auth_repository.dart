import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:dartz/dartz.dart';

import '../../../../core/constants/api_constants.dart';
import '../../../../core/error/exceptions.dart';
import '../../../../core/error/failure.dart';
import '../../../../core/storage/secure_storage_service.dart';
import '../../domain/entities/user.dart';
import '../../domain/entities/auth_token.dart';
import '../../domain/repositories/auth_repository.dart';

/// HTTP implementation of AuthRepository
class HttpAuthRepository implements AuthRepository {
  final http.Client httpClient;
  final SecureStorageService secureStorage;

  HttpAuthRepository({
    required this.httpClient,
    required this.secureStorage,
  });

  Map<String, String> get _headers => {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      };

  Map<String, String> _headersWithAuth(String token) => {
        ..._headers,
        'Authorization': 'Bearer $token',
      };

  @override
  Future<Either<Failure, AuthResult>> login(LoginRequest request) async {
    try {
      final response = await httpClient.post(
        Uri.parse('${ApiConstants.baseUrl}/auth/login'),
        headers: _headers,
        body: jsonEncode(request.toJson()),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final result = AuthResult.fromJson(data);
        
        // Store token securely
        await secureStorage.setAccessToken(result.token.accessToken);
        await secureStorage.setRefreshToken(result.token.refreshToken);
        
        return Right(result);
      } else {
        final error = jsonDecode(response.body);
        return Left(ServerFailure(
          message: error['detail'] ?? 'Login failed',
          details: 'Status code: ${response.statusCode}',
        ));
      }
    } on ServerException catch (e) {
      return Left(ServerFailure(
        message: e.message,
        details: 'Status code: ${e.statusCode}',
      ));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } catch (e) {
      return Left(NetworkFailure(message: 'Failed to connect to server'));
    }
  }

  @override
  Future<Either<Failure, AuthResult>> register(RegisterRequest request) async {
    try {
      final response = await httpClient.post(
        Uri.parse('${ApiConstants.baseUrl}/auth/register'),
        headers: _headers,
        body: jsonEncode(request.toJson()),
      );

      if (response.statusCode == 201) {
        final data = jsonDecode(response.body);
        final result = AuthResult.fromJson(data);
        
        // Store token securely
        await secureStorage.setAccessToken(result.token.accessToken);
        await secureStorage.setRefreshToken(result.token.refreshToken);
        
        return Right(result);
      } else {
        final error = jsonDecode(response.body);
        return Left(ServerFailure(
          message: error['detail'] ?? 'Registration failed',
          details: 'Status code: ${response.statusCode}',
        ));
      }
    } on ServerException catch (e) {
      return Left(ServerFailure(
        message: e.message,
        details: 'Status code: ${e.statusCode}',
      ));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } catch (e) {
      return Left(NetworkFailure(message: 'Failed to connect to server'));
    }
  }

  @override
  Future<Either<Failure, void>> logout() async {
    try {
      final token = await secureStorage.getAccessToken();
      if (token != null) {
        await httpClient.post(
          Uri.parse('${ApiConstants.baseUrl}/auth/logout'),
          headers: _headersWithAuth(token),
        );
      }
      
      // Always clear local storage
      await secureStorage.clearAll();
      return const Right(null);
    } catch (e) {
      // Continue with logout even if server request fails
      await secureStorage.clearAll();
      return const Right(null);
    }
  }

  @override
  Future<Either<Failure, AuthToken>> refreshToken(String refreshToken) async {
    try {
      final response = await httpClient.post(
        Uri.parse('${ApiConstants.baseUrl}/auth/refresh'),
        headers: _headers,
        body: jsonEncode({'refresh_token': refreshToken}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final token = AuthToken.fromJson(data);
        
        // Store new token
        await secureStorage.setAccessToken(token.accessToken);
        await secureStorage.setRefreshToken(token.refreshToken);
        
        return Right(token);
      } else {
        return Left(ServerFailure(
          message: 'Token refresh failed',
          details: 'Status code: ${response.statusCode}',
        ));
      }
    } on ServerException catch (e) {
      return Left(ServerFailure(
        message: e.message,
        details: 'Status code: ${e.statusCode}',
      ));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } catch (e) {
      return const Left(NetworkFailure(message: 'Failed to refresh token'));
    }
  }

  @override
  Future<Either<Failure, User?>> getCurrentUser() async {
    try {
      final token = await secureStorage.getAccessToken();
      if (token == null) {
        return const Left(AuthFailure(message: 'No authentication token found'));
      }

      final response = await httpClient.get(
        Uri.parse('${ApiConstants.baseUrl}/auth/me'),
        headers: _headersWithAuth(token),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return Right(User.fromJson(data));
      } else {
        return Left(ServerFailure(
          message: 'Failed to get user profile',
          details: 'Status code: ${response.statusCode}',
        ));
      }
    } on AuthException catch (e) {
      return Left(AuthFailure(message: e.message));
    } on ServerException catch (e) {
      return Left(ServerFailure(
        message: e.message,
        details: 'Status code: ${e.statusCode}',
      ));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } catch (e) {
      return const Left(NetworkFailure(message: 'Failed to get user profile'));
    }
  }

  @override
  Future<User> updateProfile(Map<String, dynamic> updates) async {
    try {
      final token = await secureStorage.getAccessToken();
      if (token == null) {
        throw const AuthException(message: 'No authentication token found');
      }

      final response = await httpClient.put(
        Uri.parse('${ApiConstants.baseUrl}/auth/profile'),
        headers: _headersWithAuth(token),
        body: jsonEncode(updates),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return User.fromJson(data);
      } else {
        final error = jsonDecode(response.body);
        throw ServerException(
          message: error['detail'] ?? 'Failed to update profile',
          statusCode: response.statusCode,
        );
      }
    } catch (e) {
      if (e is ServerException || e is AuthException) rethrow;
      throw const NetworkException(message: 'Failed to update profile');
    }
  }

  @override
  Future<void> changePassword({
    required String currentPassword,
    required String newPassword,
  }) async {
    try {
      final token = await secureStorage.getAccessToken();
      if (token == null) {
        throw const AuthException(message: 'No authentication token found');
      }

      final response = await httpClient.post(
        Uri.parse('${ApiConstants.baseUrl}/auth/change-password'),
        headers: _headersWithAuth(token),
        body: jsonEncode({
          'current_password': currentPassword,
          'new_password': newPassword,
        }),
      );

      if (response.statusCode != 200) {
        final error = jsonDecode(response.body);
        throw ServerException(
          message: error['detail'] ?? 'Failed to change password',
          statusCode: response.statusCode,
        );
      }
    } catch (e) {
      if (e is ServerException || e is AuthException) rethrow;
      throw const NetworkException(message: 'Failed to change password');
    }
  }

  @override
  Future<void> sendPasswordResetEmail(String email) async {
    try {
      final response = await httpClient.post(
        Uri.parse('${ApiConstants.baseUrl}/auth/forgot-password'),
        headers: _headers,
        body: jsonEncode({'email': email}),
      );

      if (response.statusCode != 200) {
        final error = jsonDecode(response.body);
        throw ServerException(
          message: error['detail'] ?? 'Failed to send reset email',
          statusCode: response.statusCode,
        );
      }
    } catch (e) {
      if (e is ServerException) rethrow;
      throw const NetworkException(message: 'Failed to send reset email');
    }
  }

  @override
  Future<void> resetPassword({
    required String token,
    required String newPassword,
  }) async {
    try {
      final response = await httpClient.post(
        Uri.parse('${ApiConstants.baseUrl}/auth/reset-password'),
        headers: _headers,
        body: jsonEncode({
          'token': token,
          'new_password': newPassword,
        }),
      );

      if (response.statusCode != 200) {
        final error = jsonDecode(response.body);
        throw ServerException(
          message: error['detail'] ?? 'Failed to reset password',
          statusCode: response.statusCode,
        );
      }
    } catch (e) {
      if (e is ServerException) rethrow;
      throw const NetworkException(message: 'Failed to reset password');
    }
  }

  @override
  Future<void> verifyEmail(String token) async {
    try {
      final response = await httpClient.post(
        Uri.parse('${ApiConstants.baseUrl}/auth/verify-email'),
        headers: _headers,
        body: jsonEncode({'token': token}),
      );

      if (response.statusCode != 200) {
        final error = jsonDecode(response.body);
        throw ServerException(
          message: error['detail'] ?? 'Failed to verify email',
          statusCode: response.statusCode,
        );
      }
    } catch (e) {
      if (e is ServerException) rethrow;
      throw const NetworkException(message: 'Failed to verify email');
    }
  }

  @override
  Future<void> resendEmailVerification() async {
    try {
      final token = await secureStorage.getAccessToken();
      if (token == null) {
        throw const AuthException(message: 'No authentication token found');
      }

      final response = await httpClient.post(
        Uri.parse('${ApiConstants.baseUrl}/auth/resend-verification'),
        headers: _headersWithAuth(token),
      );

      if (response.statusCode != 200) {
        final error = jsonDecode(response.body);
        throw ServerException(
          message: error['detail'] ?? 'Failed to resend verification email',
          statusCode: response.statusCode,
        );
      }
    } catch (e) {
      if (e is ServerException || e is AuthException) rethrow;
      throw const NetworkException(message: 'Failed to resend verification email');
    }
  }

  @override
  Future<void> deleteAccount() async {
    try {
      final token = await secureStorage.getAccessToken();
      if (token == null) {
        throw const AuthException(message: 'No authentication token found');
      }

      final response = await httpClient.delete(
        Uri.parse('${ApiConstants.baseUrl}/auth/account'),
        headers: _headersWithAuth(token),
      );

      if (response.statusCode == 200) {
        // Clear local storage after successful deletion
        await secureStorage.clearAll();
      } else {
        final error = jsonDecode(response.body);
        throw ServerException(
          message: error['detail'] ?? 'Failed to delete account',
          statusCode: response.statusCode,
        );
      }
    } catch (e) {
      if (e is ServerException || e is AuthException) rethrow;
      throw const NetworkException(message: 'Failed to delete account');
    }
  }
}
