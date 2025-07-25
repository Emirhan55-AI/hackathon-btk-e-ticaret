import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;

import '../../../../core/storage/secure_storage_service.dart';
import '../../domain/entities/auth_state.dart';
import '../../domain/entities/user.dart';
import '../../domain/entities/auth_token.dart';
import '../../domain/repositories/auth_repository.dart';
import '../../data/repositories/http_auth_repository.dart';

/// HTTP client provider
final httpClientProvider = Provider<http.Client>((ref) {
  return http.Client();
});

/// Secure storage provider
final secureStorageProvider = Provider<SecureStorageService>((ref) {
  return SecureStorageService();
});

/// Auth repository provider
final authRepositoryProvider = Provider<AuthRepository>((ref) {
  return HttpAuthRepository(
    httpClient: ref.read(httpClientProvider),
    secureStorage: ref.read(secureStorageProvider),
  );
});

/// Auth state notifier
class AuthNotifier extends StateNotifier<AuthState> {
  final AuthRepository _authRepository;
  final SecureStorageService _secureStorage;

  AuthNotifier(this._authRepository, this._secureStorage)
      : super(AuthState.initial);

  /// Check current authentication status
  Future<void> checkAuthStatus() async {
    state = AuthState.loading;

    try {
      final token = await _secureStorage.getAccessToken();
      final refreshToken = await _secureStorage.getRefreshToken();

      if (token == null || refreshToken == null) {
        state = AuthState.unauthenticated();
        return;
      }

      // Try to get current user
      final user = await _authRepository.getCurrentUser();
      
      // Create auth token (we don't have expiry info from storage)
      final authToken = AuthToken(
        accessToken: token,
        refreshToken: refreshToken,
        expiresAt: DateTime.now().add(const Duration(hours: 1)), // Default expiry
      );

      state = AuthState.authenticated(user: user, token: authToken);
    } catch (e) {
      // Token might be expired, try to refresh
      await _tryRefreshToken();
    }
  }

  /// Login with email and password
  Future<void> login(String email, String password) async {
    state = AuthState.loading;

    try {
      final request = LoginRequest(email: email, password: password);
      final result = await _authRepository.login(request);

      state = AuthState.authenticated(
        user: result.user,
        token: result.token,
      );
    } catch (e) {
      state = AuthState.error(e.toString());
    }
  }

  /// Register new user
  Future<void> register({
    required String email,
    required String password,
    String? firstName,
    String? lastName,
  }) async {
    state = AuthState.loading;

    try {
      final request = RegisterRequest(
        email: email,
        password: password,
        firstName: firstName,
        lastName: lastName,
      );
      final result = await _authRepository.register(request);

      state = AuthState.authenticated(
        user: result.user,
        token: result.token,
      );
    } catch (e) {
      state = AuthState.error(e.toString());
    }
  }

  /// Logout current user
  Future<void> logout() async {
    try {
      await _authRepository.logout();
    } catch (e) {
      // Continue with logout even if server request fails
    } finally {
      state = AuthState.unauthenticated();
    }
  }

  /// Update user profile
  Future<void> updateProfile(Map<String, dynamic> updates) async {
    if (!state.isAuthenticated) return;

    state = state.copyWith(isLoading: true);

    try {
      final updatedUser = await _authRepository.updateProfile(updates);
      state = state.copyWith(
        user: updatedUser,
        isLoading: false,
      );
    } catch (e) {
      state = state.copyWith(
        errorMessage: e.toString(),
        isLoading: false,
      );
    }
  }

  /// Change password
  Future<void> changePassword({
    required String currentPassword,
    required String newPassword,
  }) async {
    if (!state.isAuthenticated) return;

    state = state.copyWith(isLoading: true);

    try {
      await _authRepository.changePassword(
        currentPassword: currentPassword,
        newPassword: newPassword,
      );
      state = state.copyWith(isLoading: false);
    } catch (e) {
      state = state.copyWith(
        errorMessage: e.toString(),
        isLoading: false,
      );
    }
  }

  /// Send password reset email
  Future<void> sendPasswordResetEmail(String email) async {
    state = AuthState.loading;

    try {
      await _authRepository.sendPasswordResetEmail(email);
      state = AuthState.unauthenticated(
        message: 'Password reset email sent successfully',
      );
    } catch (e) {
      state = AuthState.error(e.toString());
    }
  }

  /// Try to refresh token
  Future<void> _tryRefreshToken() async {
    try {
      final refreshToken = await _secureStorage.getRefreshToken();
      if (refreshToken == null) {
        state = AuthState.unauthenticated();
        return;
      }

      final newToken = await _authRepository.refreshToken(refreshToken);
      final user = await _authRepository.getCurrentUser();

      state = AuthState.authenticated(user: user, token: newToken);
    } catch (e) {
      // Refresh failed, user needs to login again
      await _secureStorage.clearAll();
      state = AuthState.unauthenticated();
    }
  }

  /// Clear any error state
  void clearError() {
    state = state.copyWith(clearError: true);
  }

  /// Get current user
  User? get currentUser => state.user;

  /// Get current token
  AuthToken? get currentToken => state.token;
}

/// Auth state notifier provider
final authNotifierProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier(
    ref.read(authRepositoryProvider),
    ref.read(secureStorageProvider),
  );
});

/// Current user provider
final currentUserProvider = Provider<User?>((ref) {
  return ref.watch(authNotifierProvider).user;
});

/// Authentication status provider
final isAuthenticatedProvider = Provider<bool>((ref) {
  return ref.watch(authNotifierProvider).isAuthenticated;
});

/// Loading status provider
final isLoadingProvider = Provider<bool>((ref) {
  return ref.watch(authNotifierProvider).isLoading;
});

/// Auth error provider
final authErrorProvider = Provider<String?>((ref) {
  return ref.watch(authNotifierProvider).errorMessage;
});
