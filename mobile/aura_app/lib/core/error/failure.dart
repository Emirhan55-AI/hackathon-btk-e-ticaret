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
    required super.message,
    super.details,
  });
}

/// Authentication related failures
class AuthFailure extends Failure {
  const AuthFailure({
    required super.message,
    super.details,
  });
}

/// Server related failures
class ServerFailure extends Failure {
  const ServerFailure({
    required super.message,
    super.details,
  });
}

/// Validation related failures
class ValidationFailure extends Failure {
  const ValidationFailure({
    required super.message,
    super.details,
  });
}

/// Cache related failures
class CacheFailure extends Failure {
  const CacheFailure({
    required super.message,
    super.details,
  });
}

/// Image related failures
class ImageFailure extends Failure {
  const ImageFailure({
    required super.message,
    super.details,
  });
}
