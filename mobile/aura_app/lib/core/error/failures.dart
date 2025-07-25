/// Base class for all failures
abstract class Failure {
  final String message;
  final String? details;

  const Failure({
    required this.message,
    this.details,
  });

  @override
  String toString() {
    return 'Failure: $message${details != null ? ' - $details' : ''}';
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is Failure && 
           other.message == message && 
           other.details == details;
  }

  @override
  int get hashCode => message.hashCode ^ details.hashCode;
}

/// Network related failures
class NetworkFailure extends Failure {
  const NetworkFailure({
    required String message,
    String? details,
  }) : super(message: message, details: details);
}

/// Server related failures
class ServerFailure extends Failure {
  const ServerFailure({
    required String message,
    String? details,
  }) : super(message: message, details: details);
}

/// Authentication related failures
class AuthFailure extends Failure {
  const AuthFailure({
    required String message,
    String? details,
  }) : super(message: message, details: details);
}

/// Validation related failures
class ValidationFailure extends Failure {
  const ValidationFailure({
    required String message,
    String? details,
  }) : super(message: message, details: details);
}

/// Cache related failures
class CacheFailure extends Failure {
  const CacheFailure({
    required String message,
    String? details,
  }) : super(message: message, details: details);
}

/// Unknown/unexpected failures
class UnknownFailure extends Failure {
  const UnknownFailure({
    required String message,
    String? details,
  }) : super(message: message, details: details);
}

/// Permission related failures
class PermissionFailure extends Failure {
  const PermissionFailure({
    required String message,
    String? details,
  }) : super(message: message, details: details);
}

/// Storage related failures
class StorageFailure extends Failure {
  const StorageFailure({
    required String message,
    String? details,
  }) : super(message: message, details: details);
}
