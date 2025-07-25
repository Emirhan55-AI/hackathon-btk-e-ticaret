import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

import '../models/user_model.dart';
import 'auth_remote_data_source.dart';
import '../../../core/constants/app_constants.dart';
import '../../../core/error/exceptions.dart';

/// HTTP implementation of authentication remote data source
class AuthRemoteDataSourceImpl implements AuthRemoteDataSource {
  final http.Client _httpClient;
  final String _baseUrl;

  AuthRemoteDataSourceImpl({
    required http.Client httpClient,
    String? baseUrl,
  })  : _httpClient = httpClient,
        _baseUrl = baseUrl ?? AppConstants.apiBaseUrl;

  @override
  Future<UserModel> login(String email, String password) async {
    try {
      final response = await _httpClient.post(
        Uri.parse('${_baseUrl}auth/login'),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: jsonEncode({
          'email': email,
          'password': password,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as Map<String, dynamic>;
        
        // Backend returns user data directly or nested in 'user' key
        final userJson = data.containsKey('user') 
            ? data['user'] as Map<String, dynamic>
            : data;
        
        return UserModel.fromJson(userJson);
      } else {
        // Handle API errors
        final errorData = _parseErrorResponse(response);
        final errorMessage = errorData['detail'] ?? 
                           errorData['message'] ?? 
                           'Login failed';
        
        throw ApiException(
          message: errorMessage,
          statusCode: response.statusCode,
        );
      }
    } on SocketException {
      throw NetworkException(message: 'No internet connection');
    } on HttpException {
      throw NetworkException(message: 'Network error occurred');
    } on FormatException {
      throw ApiException(
        message: 'Invalid response format',
        statusCode: 0,
      );
    } catch (e) {
      if (e is ApiException || e is NetworkException) {
        rethrow;
      }
      throw UnknownException(message: 'Unexpected error: ${e.toString()}');
    }
  }

  @override
  Future<UserModel> register({
    required String email,
    required String password,
    String? firstName,
    String? lastName,
  }) async {
    try {
      final response = await _httpClient.post(
        Uri.parse('${_baseUrl}auth/register'),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: jsonEncode({
          'email': email,
          'password': password,
          if (firstName != null) 'first_name': firstName,
          if (lastName != null) 'last_name': lastName,
        }),
      );

      if (response.statusCode == 201 || response.statusCode == 200) {
        final data = jsonDecode(response.body) as Map<String, dynamic>;
        
        final userJson = data.containsKey('user') 
            ? data['user'] as Map<String, dynamic>
            : data;
        
        return UserModel.fromJson(userJson);
      } else {
        final errorData = _parseErrorResponse(response);
        final errorMessage = errorData['detail'] ?? 
                           errorData['message'] ?? 
                           'Registration failed';
        
        throw ApiException(
          message: errorMessage,
          statusCode: response.statusCode,
        );
      }
    } on SocketException {
      throw NetworkException(message: 'No internet connection');
    } on HttpException {
      throw NetworkException(message: 'Network error occurred');
    } on FormatException {
      throw ApiException(
        message: 'Invalid response format',
        statusCode: 0,
      );
    } catch (e) {
      if (e is ApiException || e is NetworkException) {
        rethrow;
      }
      throw UnknownException(message: 'Unexpected error: ${e.toString()}');
    }
  }

  @override
  Future<void> logout() async {
    try {
      final response = await _httpClient.post(
        Uri.parse('${_baseUrl}auth/logout'),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      if (response.statusCode != 200 && response.statusCode != 204) {
        final errorData = _parseErrorResponse(response);
        final errorMessage = errorData['detail'] ?? 
                           errorData['message'] ?? 
                           'Logout failed';
        
        throw ApiException(
          message: errorMessage,
          statusCode: response.statusCode,
        );
      }
    } on SocketException {
      throw NetworkException(message: 'No internet connection');
    } on HttpException {
      throw NetworkException(message: 'Network error occurred');
    } catch (e) {
      if (e is ApiException || e is NetworkException) {
        rethrow;
      }
      throw UnknownException(message: 'Unexpected error: ${e.toString()}');
    }
  }

  @override
  Future<UserModel> getCurrentUser() async {
    try {
      final response = await _httpClient.get(
        Uri.parse('${_baseUrl}auth/me'),
        headers: {
          'Accept': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as Map<String, dynamic>;
        return UserModel.fromJson(data);
      } else {
        final errorData = _parseErrorResponse(response);
        final errorMessage = errorData['detail'] ?? 
                           errorData['message'] ?? 
                           'Failed to get user data';
        
        throw ApiException(
          message: errorMessage,
          statusCode: response.statusCode,
        );
      }
    } on SocketException {
      throw NetworkException(message: 'No internet connection');
    } on HttpException {
      throw NetworkException(message: 'Network error occurred');
    } on FormatException {
      throw ApiException(
        message: 'Invalid response format',
        statusCode: 0,
      );
    } catch (e) {
      if (e is ApiException || e is NetworkException) {
        rethrow;
      }
      throw UnknownException(message: 'Unexpected error: ${e.toString()}');
    }
  }

  @override
  Future<UserModel> refreshToken() async {
    try {
      final response = await _httpClient.post(
        Uri.parse('${_baseUrl}auth/refresh'),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as Map<String, dynamic>;
        
        final userJson = data.containsKey('user') 
            ? data['user'] as Map<String, dynamic>
            : data;
        
        return UserModel.fromJson(userJson);
      } else {
        final errorData = _parseErrorResponse(response);
        final errorMessage = errorData['detail'] ?? 
                           errorData['message'] ?? 
                           'Token refresh failed';
        
        throw ApiException(
          message: errorMessage,
          statusCode: response.statusCode,
        );
      }
    } on SocketException {
      throw NetworkException(message: 'No internet connection');
    } on HttpException {
      throw NetworkException(message: 'Network error occurred');
    } on FormatException {
      throw ApiException(
        message: 'Invalid response format',
        statusCode: 0,
      );
    } catch (e) {
      if (e is ApiException || e is NetworkException) {
        rethrow;
      }
      throw UnknownException(message: 'Unexpected error: ${e.toString()}');
    }
  }

  @override
  Future<UserModel> updateProfile({
    String? firstName,
    String? lastName,
    String? profileImage,
    DateTime? dateOfBirth,
    String? gender,
  }) async {
    try {
      final body = <String, dynamic>{};
      if (firstName != null) body['first_name'] = firstName;
      if (lastName != null) body['last_name'] = lastName;
      if (profileImage != null) body['profile_image'] = profileImage;
      if (dateOfBirth != null) body['date_of_birth'] = dateOfBirth.toIso8601String();
      if (gender != null) body['gender'] = gender;

      final response = await _httpClient.put(
        Uri.parse('${_baseUrl}auth/profile'),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: jsonEncode(body),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as Map<String, dynamic>;
        return UserModel.fromJson(data);
      } else {
        final errorData = _parseErrorResponse(response);
        final errorMessage = errorData['detail'] ?? 
                           errorData['message'] ?? 
                           'Profile update failed';
        
        throw ApiException(
          message: errorMessage,
          statusCode: response.statusCode,
        );
      }
    } on SocketException {
      throw NetworkException(message: 'No internet connection');
    } on HttpException {
      throw NetworkException(message: 'Network error occurred');
    } on FormatException {
      throw ApiException(
        message: 'Invalid response format',
        statusCode: 0,
      );
    } catch (e) {
      if (e is ApiException || e is NetworkException) {
        rethrow;
      }
      throw UnknownException(message: 'Unexpected error: ${e.toString()}');
    }
  }

  @override
  Future<void> changePassword({
    required String currentPassword,
    required String newPassword,
  }) async {
    try {
      final response = await _httpClient.put(
        Uri.parse('${_baseUrl}auth/password'),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: jsonEncode({
          'current_password': currentPassword,
          'new_password': newPassword,
        }),
      );

      if (response.statusCode != 200 && response.statusCode != 204) {
        final errorData = _parseErrorResponse(response);
        final errorMessage = errorData['detail'] ?? 
                           errorData['message'] ?? 
                           'Password change failed';
        
        throw ApiException(
          message: errorMessage,
          statusCode: response.statusCode,
        );
      }
    } on SocketException {
      throw NetworkException(message: 'No internet connection');
    } on HttpException {
      throw NetworkException(message: 'Network error occurred');
    } catch (e) {
      if (e is ApiException || e is NetworkException) {
        rethrow;
      }
      throw UnknownException(message: 'Unexpected error: ${e.toString()}');
    }
  }

  @override
  Future<void> deleteAccount() async {
    try {
      final response = await _httpClient.delete(
        Uri.parse('${_baseUrl}auth/account'),
        headers: {
          'Accept': 'application/json',
        },
      );

      if (response.statusCode != 200 && response.statusCode != 204) {
        final errorData = _parseErrorResponse(response);
        final errorMessage = errorData['detail'] ?? 
                           errorData['message'] ?? 
                           'Account deletion failed';
        
        throw ApiException(
          message: errorMessage,
          statusCode: response.statusCode,
        );
      }
    } on SocketException {
      throw NetworkException(message: 'No internet connection');
    } on HttpException {
      throw NetworkException(message: 'Network error occurred');
    } catch (e) {
      if (e is ApiException || e is NetworkException) {
        rethrow;
      }
      throw UnknownException(message: 'Unexpected error: ${e.toString()}');
    }
  }

  /// Parse error response and extract error data
  Map<String, dynamic> _parseErrorResponse(http.Response response) {
    try {
      return jsonDecode(response.body) as Map<String, dynamic>;
    } catch (e) {
      return {
        'message': 'HTTP ${response.statusCode}: ${response.reasonPhrase}',
        'status_code': response.statusCode,
      };
    }
  }
}
