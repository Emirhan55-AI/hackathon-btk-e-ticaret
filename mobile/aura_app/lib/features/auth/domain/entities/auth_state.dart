import 'user.dart';
import 'auth_token.dart';

/// Authentication state representing the current auth status
enum AuthStatus {
  initial,
  loading,
  authenticated,
  unauthenticated,
  error,
}

/// Authentication state entity
class AuthState {
  final AuthStatus status;
  final User? user;
  final AuthToken? token;
  final String? errorMessage;
  final bool isLoading;

  const AuthState({
    this.status = AuthStatus.initial,
    this.user,
    this.token,
    this.errorMessage,
    this.isLoading = false,
  });

  /// Initial state
  static const AuthState initial = AuthState(
    status: AuthStatus.initial,
  );

  /// Loading state
  static const AuthState loading = AuthState(
    status: AuthStatus.loading,
    isLoading: true,
  );

  /// Check if user is authenticated
  bool get isAuthenticated => 
      status == AuthStatus.authenticated && 
      user != null && 
      token != null && 
      !token!.isExpired;

  /// Check if authentication is in progress
  bool get isAuthenticating => 
      status == AuthStatus.loading || isLoading;

  /// Check if there's an authentication error
  bool get hasError => 
      status == AuthStatus.error && errorMessage != null;

  /// Create authenticated state
  AuthState.authenticated({
    required User user,
    required AuthToken token,
  }) : this(
         status: AuthStatus.authenticated,
         user: user,
         token: token,
         isLoading: false,
       );

  /// Create unauthenticated state
  AuthState.unauthenticated({String? message})
      : this(
          status: AuthStatus.unauthenticated,
          errorMessage: message,
          isLoading: false,
        );

  /// Create error state
  AuthState.error(String message)
      : this(
          status: AuthStatus.error,
          errorMessage: message,
          isLoading: false,
        );

  /// Create a copy with updated fields
  AuthState copyWith({
    AuthStatus? status,
    User? user,
    AuthToken? token,
    String? errorMessage,
    bool? isLoading,
    bool clearError = false,
    bool clearUser = false,
    bool clearToken = false,
  }) {
    return AuthState(
      status: status ?? this.status,
      user: clearUser ? null : (user ?? this.user),
      token: clearToken ? null : (token ?? this.token),
      errorMessage: clearError ? null : (errorMessage ?? this.errorMessage),
      isLoading: isLoading ?? this.isLoading,
    );
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is AuthState &&
           other.status == status &&
           other.user == user &&
           other.token == token &&
           other.errorMessage == errorMessage &&
           other.isLoading == isLoading;
  }

  @override
  int get hashCode => Object.hash(
        status,
        user,
        token,
        errorMessage,
        isLoading,
      );

  @override
  String toString() {
    return 'AuthState(status: $status, user: ${user?.email}, isLoading: $isLoading, hasError: $hasError)';
  }
}
