import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;

import '../../../../core/storage/secure_storage_service.dart';
import '../../domain/entities/auth_state.dart';
import '../../domain/entities/user.dart';
import '../../domain/entities/auth_token.dart';
import '../../domain/repositories/auth_repository.dart';
import '../../domain/usecases/login_usecase.dart';
import '../../domain/usecases/register_usecase.dart';
import '../../domain/usecases/logout_usecase.dart';
import '../../domain/usecases/get_current_user_usecase.dart';
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

/// Use case providers
final loginUseCaseProvider = Provider<LoginUseCase>((ref) {
  return LoginUseCase(ref.read(authRepositoryProvider));
});

final registerUseCaseProvider = Provider<RegisterUseCase>((ref) {
  return RegisterUseCase(ref.read(authRepositoryProvider));
});

final logoutUseCaseProvider = Provider<LogoutUseCase>((ref) {
  return LogoutUseCase(ref.read(authRepositoryProvider));
});

final getCurrentUserUseCaseProvider = Provider<GetCurrentUserUseCase>((ref) {
  return GetCurrentUserUseCase(ref.read(authRepositoryProvider));
});

/// Auth state notifier
class AuthNotifier extends StateNotifier<AuthState> {
  final LoginUseCase _loginUseCase;
  final RegisterUseCase _registerUseCase;
  final LogoutUseCase _logoutUseCase;
  final GetCurrentUserUseCase _getCurrentUserUseCase;
  final AuthRepository _authRepository;
  final SecureStorageService _secureStorage;

  AuthNotifier({
    required LoginUseCase loginUseCase,
    required RegisterUseCase registerUseCase,
    required LogoutUseCase logoutUseCase,
    required GetCurrentUserUseCase getCurrentUserUseCase,
    required AuthRepository authRepository,
    required SecureStorageService secureStorage,
  })  : _loginUseCase = loginUseCase,
        _registerUseCase = registerUseCase,
        _logoutUseCase = logoutUseCase,
        _getCurrentUserUseCase = getCurrentUserUseCase,
        _authRepository = authRepository,
        _secureStorage = secureStorage,
        super(AuthState.initial);

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

      // Try to get current user using use case
      final result = await _getCurrentUserUseCase();
      
      result.fold(
        (failure) {
          // Token might be expired, try to refresh
          _tryRefreshToken();
        },
        (user) {
          if (user != null) {
            // Create auth token (we don't have expiry info from storage)
            final authToken = AuthToken(
              accessToken: token,
              refreshToken: refreshToken,
              expiresAt: DateTime.now().add(const Duration(hours: 1)), // Default expiry
            );

            state = AuthState.authenticated(user: user, token: authToken);
          } else {
            state = AuthState.unauthenticated();
          }
        },
      );
    } catch (e) {
      // Token might be expired, try to refresh
      await _tryRefreshToken();
    }
  }

  /// Login with email and password
  Future<void> login(String email, String password) async {
    state = AuthState.loading;

    final result = await _loginUseCase(email: email, password: password);

    result.fold(
      (failure) => state = AuthState.error(failure.message),
      (user) {
        // We need to get the token from storage since LoginUseCase only returns User
        // In a real app, you might want to return both user and token from use case
        state = state.copyWith(
          status: AuthStatus.authenticated,
          user: user,
          errorMessage: null,
          isLoading: false,
        );
      },
    );
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
    final result = await _logoutUseCase();
    
    result.fold(
      (failure) {
        // Even if logout fails on server, clear local state
        state = AuthState.unauthenticated();
      },
      (_) {
        state = AuthState.unauthenticated();
      },
    );
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
    loginUseCase: ref.read(loginUseCaseProvider),
    registerUseCase: ref.read(registerUseCaseProvider),
    logoutUseCase: ref.read(logoutUseCaseProvider),
    getCurrentUserUseCase: ref.read(getCurrentUserUseCaseProvider),
    authRepository: ref.read(authRepositoryProvider),
    secureStorage: ref.read(secureStorageProvider),
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
