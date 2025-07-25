import '../entities/user.dart';
import '../entities/auth_token.dart';

/// Login request data
class LoginRequest {
  final String email;
  final String password;

  const LoginRequest({
    required this.email,
    required this.password,
  });

  Map<String, dynamic> toJson() {
    return {
      'email': email,
      'password': password,
    };
  }
}

/// Register request data
class RegisterRequest {
  final String email;
  final String password;
  final String? firstName;
  final String? lastName;

  const RegisterRequest({
    required this.email,
    required this.password,
    this.firstName,
    this.lastName,
  });

  Map<String, dynamic> toJson() {
    return {
      'email': email,
      'password': password,
      if (firstName != null) 'first_name': firstName,
      if (lastName != null) 'last_name': lastName,
    };
  }
}

/// Authentication result
class AuthResult {
  final User user;
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
  Future<AuthResult> login(LoginRequest request);

  /// Register new user
  Future<AuthResult> register(RegisterRequest request);

  /// Logout current user
  Future<void> logout();

  /// Refresh authentication token
  Future<AuthToken> refreshToken(String refreshToken);

  /// Get current user profile
  Future<User> getCurrentUser();

  /// Update user profile
  Future<User> updateProfile(Map<String, dynamic> updates);

  /// Change password
  Future<void> changePassword({
    required String currentPassword,
    required String newPassword,
  });

  /// Send password reset email
  Future<void> sendPasswordResetEmail(String email);

  /// Reset password with token
  Future<void> resetPassword({
    required String token,
    required String newPassword,
  });

  /// Verify email with token
  Future<void> verifyEmail(String token);

  /// Resend email verification
  Future<void> resendEmailVerification();

  /// Delete user account
  Future<void> deleteAccount();
}
