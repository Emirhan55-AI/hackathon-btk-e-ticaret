/// Base class for all application exceptions
abstract class AppException implements Exception {
  final String message;
  final String? details;
  final int? statusCode;

  const AppException({
    required this.message,
    this.details,
    this.statusCode,
  });

  @override
  String toString() {
    return 'AppException: $message${details != null ? ' - $details' : ''}';
  }
}

/// Network related exceptions
class NetworkException extends AppException {
  const NetworkException({
    required super.message,
    super.details,
    super.statusCode,
  });
}

/// Authentication related exceptions
class AuthException extends AppException {
  const AuthException({
    required super.message,
    super.details,
    super.statusCode,
  });
}

/// API related exceptions
class ApiException extends AppException {
  const ApiException({
    required super.message,
    super.details,
    super.statusCode,
  });
}

/// Unknown/Generic exceptions
class UnknownException extends AppException {
  const UnknownException({
    required super.message,
    super.details,
    super.statusCode,
  });
}

/// Server related exceptions
class ServerException extends AppException {
  const ServerException({
    required super.message,
    super.details,
    super.statusCode,
  });
}

/// Validation related exceptions
class ValidationException extends AppException {
  const ValidationException({
    required super.message,
    super.details,
    super.statusCode,
  });
}

/// Cache related exceptions
class CacheException extends AppException {
  const CacheException({
    required super.message,
    super.details,
    super.statusCode,
  });
}

/// Image related exceptions
class ImageException extends AppException {
  const ImageException({
    required super.message,
    super.details,
    super.statusCode,
  });
}

/// Data parsing related exceptions
class DataParsingException extends AppException {
  const DataParsingException({
    required super.message,
    super.details,
    super.statusCode,
  });
}
