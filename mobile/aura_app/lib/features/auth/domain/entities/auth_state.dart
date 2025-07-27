import 'user.dart';
import '../../../../core/error/failures.dart';

/// Authentication state
abstract class AuthState {
  const AuthState();

  /// Check if auth operation is in progress
  bool get isLoading => this is AuthLoading;
  
  /// Check if user is authenticated
  bool get isAuthenticated => this is AuthAuthenticated;
  
  /// Check if there's an error
  bool get isError => this is AuthError;
  
  /// Get current user if authenticated
  User? get user {
    if (this is AuthAuthenticated) {
      return (this as AuthAuthenticated).user;
    }
    return null;
  }
  
  /// Get current failure if error
  Failure? get failure {
    if (this is AuthError) {
      return (this as AuthError).failure;
    }
    return null;
  }

  /// Pattern matching for auth states
  T when<T>({
    required T Function() initial,
    required T Function() loading,
    required T Function(User user) authenticated,
    required T Function() unauthenticated,
    required T Function(Failure failure) error,
  }) {
    if (this is AuthInitial) {
      return initial();
    } else if (this is AuthLoading) {
      return loading();
    } else if (this is AuthAuthenticated) {
      return authenticated((this as AuthAuthenticated).user);
    } else if (this is AuthUnauthenticated) {
      return unauthenticated();
    } else if (this is AuthError) {
      return error((this as AuthError).failure);
    }
    throw Exception('Unknown AuthState: $this');
  }

  /// Maybe pattern matching for auth states
  T maybeWhen<T>({
    T Function()? initial,
    T Function()? loading,
    T Function(User user)? authenticated,
    T Function()? unauthenticated,
    T Function(Failure failure)? error,
    required T Function() orElse,
  }) {
    if (this is AuthInitial && initial != null) {
      return initial();
    } else if (this is AuthLoading && loading != null) {
      return loading();
    } else if (this is AuthAuthenticated && authenticated != null) {
      return authenticated((this as AuthAuthenticated).user);
    } else if (this is AuthUnauthenticated && unauthenticated != null) {
      return unauthenticated();
    } else if (this is AuthError && error != null) {
      return error((this as AuthError).failure);
    }
    return orElse();
  }
}

class AuthInitial extends AuthState {
  const AuthInitial();
}

class AuthLoading extends AuthState {
  const AuthLoading();
}

class AuthAuthenticated extends AuthState {
  final User user;
  const AuthAuthenticated(this.user);
}

class AuthUnauthenticated extends AuthState {
  const AuthUnauthenticated();
}

class AuthError extends AuthState {
  final Failure failure;
  const AuthError(this.failure);
}
