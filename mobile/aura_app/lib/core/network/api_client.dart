import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../constants/api_constants.dart';
import '../error/exceptions.dart';
import '../storage/secure_storage_service.dart';

/// Main API client for network requests
class ApiClient {
  final SecureStorageService _storageService;
  late final http.Client _client;

  ApiClient({
    required SecureStorageService storageService,
    http.Client? client,
  }) : _storageService = storageService {
    _client = client ?? http.Client();
  }

  /// GET request
  Future<Map<String, dynamic>> get(
    String endpoint, {
    Map<String, String>? queryParameters,
    bool requiresAuth = true,
  }) async {
    try {
      final uri = _buildUri(endpoint, queryParameters);
      final headers = await _buildHeaders(requiresAuth);

      final response = await _client
          .get(uri, headers: headers)
          .timeout(ApiConstants.connectionTimeout);

      return _handleResponse(response);
    } on SocketException {
      throw const NetworkException(
        message: 'No internet connection',
        details: 'Please check your network connection and try again',
      );
    } on HttpException catch (e) {
      throw NetworkException(
        message: 'Network error occurred',
        details: e.message,
      );
    } catch (e) {
      throw NetworkException(
        message: 'Unexpected error occurred',
        details: e.toString(),
      );
    }
  }

  /// POST request
  Future<Map<String, dynamic>> post(
    String endpoint, {
    Map<String, dynamic>? body,
    bool requiresAuth = true,
  }) async {
    try {
      final uri = _buildUri(endpoint);
      final headers = await _buildHeaders(requiresAuth);

      final response = await _client
          .post(
            uri,
            headers: headers,
            body: body != null ? jsonEncode(body) : null,
          )
          .timeout(ApiConstants.connectionTimeout);

      return _handleResponse(response);
    } on SocketException {
      throw const NetworkException(
        message: 'No internet connection',
        details: 'Please check your network connection and try again',
      );
    } on HttpException catch (e) {
      throw NetworkException(
        message: 'Network error occurred',
        details: e.message,
      );
    } catch (e) {
      throw NetworkException(
        message: 'Unexpected error occurred',
        details: e.toString(),
      );
    }
  }

  /// PUT request
  Future<Map<String, dynamic>> put(
    String endpoint, {
    Map<String, dynamic>? body,
    bool requiresAuth = true,
  }) async {
    try {
      final uri = _buildUri(endpoint);
      final headers = await _buildHeaders(requiresAuth);

      final response = await _client
          .put(
            uri,
            headers: headers,
            body: body != null ? jsonEncode(body) : null,
          )
          .timeout(ApiConstants.connectionTimeout);

      return _handleResponse(response);
    } on SocketException {
      throw const NetworkException(
        message: 'No internet connection',
        details: 'Please check your network connection and try again',
      );
    } on HttpException catch (e) {
      throw NetworkException(
        message: 'Network error occurred',
        details: e.message,
      );
    } catch (e) {
      throw NetworkException(
        message: 'Unexpected error occurred',
        details: e.toString(),
      );
    }
  }

  /// DELETE request
  Future<Map<String, dynamic>> delete(
    String endpoint, {
    bool requiresAuth = true,
  }) async {
    try {
      final uri = _buildUri(endpoint);
      final headers = await _buildHeaders(requiresAuth);

      final response = await _client
          .delete(uri, headers: headers)
          .timeout(ApiConstants.connectionTimeout);

      return _handleResponse(response);
    } on SocketException {
      throw const NetworkException(
        message: 'No internet connection',
        details: 'Please check your network connection and try again',
      );
    } on HttpException catch (e) {
      throw NetworkException(
        message: 'Network error occurred',
        details: e.message,
      );
    } catch (e) {
      throw NetworkException(
        message: 'Unexpected error occurred',
        details: e.toString(),
      );
    }
  }

  /// Upload multipart request (for images)
  Future<Map<String, dynamic>> uploadMultipart(
    String endpoint,
    String fieldName,
    String filePath, {
    Map<String, String>? fields,
    bool requiresAuth = true,
  }) async {
    try {
      final uri = _buildUri(endpoint);
      final headers = await _buildHeaders(requiresAuth, isMultipart: true);

      final request = http.MultipartRequest('POST', uri);
      request.headers.addAll(headers);

      // Add file
      final file = await http.MultipartFile.fromPath(fieldName, filePath);
      request.files.add(file);

      // Add additional fields
      if (fields != null) {
        request.fields.addAll(fields);
      }

      final streamedResponse = await request.send();
      final response = await http.Response.fromStream(streamedResponse);

      return _handleResponse(response);
    } on SocketException {
      throw const NetworkException(
        message: 'No internet connection',
        details: 'Please check your network connection and try again',
      );
    } on HttpException catch (e) {
      throw NetworkException(
        message: 'Network error occurred',
        details: e.message,
      );
    } catch (e) {
      throw NetworkException(
        message: 'Upload failed',
        details: e.toString(),
      );
    }
  }

  /// Build URI with query parameters
  Uri _buildUri(String endpoint, [Map<String, String>? queryParameters]) {
    final baseUri = Uri.parse(ApiConstants.baseUrl);
    final uri = baseUri.replace(
      path: baseUri.path + endpoint,
      queryParameters: queryParameters,
    );
    return uri;
  }

  /// Build request headers
  Future<Map<String, String>> _buildHeaders(
    bool requiresAuth, {
    bool isMultipart = false,
  }) async {
    final headers = <String, String>{
      'Accept': 'application/json',
    };

    if (!isMultipart) {
      headers['Content-Type'] = 'application/json';
    }

    if (requiresAuth) {
      final accessToken = await _storageService.getAccessToken();
      if (accessToken != null) {
        headers['Authorization'] = 'Bearer $accessToken';
      }
    }

    return headers;
  }

  /// Handle API response
  Map<String, dynamic> _handleResponse(http.Response response) {
    switch (response.statusCode) {
      case 200:
      case 201:
      case 202:
        if (response.body.isEmpty) {
          return <String, dynamic>{};
        }
        return jsonDecode(response.body) as Map<String, dynamic>;

      case 400:
        throw ValidationException(
          message: 'Invalid request',
          details: _extractErrorMessage(response),
          statusCode: response.statusCode,
        );

      case 401:
        throw AuthException(
          message: 'Unauthorized',
          details: 'Please login again',
          statusCode: response.statusCode,
        );

      case 403:
        throw AuthException(
          message: 'Access forbidden',
          details: _extractErrorMessage(response),
          statusCode: response.statusCode,
        );

      case 404:
        throw ServerException(
          message: 'Resource not found',
          details: _extractErrorMessage(response),
          statusCode: response.statusCode,
        );

      case 422:
        throw ValidationException(
          message: 'Validation error',
          details: _extractErrorMessage(response),
          statusCode: response.statusCode,
        );

      case 500:
      case 502:
      case 503:
        throw ServerException(
          message: 'Server error',
          details: 'Please try again later',
          statusCode: response.statusCode,
        );

      default:
        throw ServerException(
          message: 'Unknown error occurred',
          details: 'Status code: ${response.statusCode}',
          statusCode: response.statusCode,
        );
    }
  }

  /// Extract error message from response
  String _extractErrorMessage(http.Response response) {
    try {
      final body = jsonDecode(response.body) as Map<String, dynamic>;
      return body['detail']?.toString() ?? 
             body['message']?.toString() ?? 
             'Unknown error';
    } catch (e) {
      return 'Unknown error';
    }
  }

  /// Dispose client
  void dispose() {
    _client.close();
  }
}
