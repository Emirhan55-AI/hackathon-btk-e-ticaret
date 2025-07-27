import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;

import '../../../../core/error/failures.dart';
import '../../../../core/storage/secure_storage_service.dart';
import '../../domain/entities/auth_state.dart';
import '../../domain/entities/user.dart';
import '../../domain/repositories/auth_repository.dart';
import '../../domain/usecases/login_usecase.dart';
// import '../../domain/usecases/register_usecase.dart'; // Will be enabled in Phase 2
import '../../domain/usecases/logout_usecase.dart';
import '../../domain/usecases/get_current_user_usecase.dart';
import '../../data/repositories/http_auth_repository.dart';
import '../../data/datasources/auth_remote_data_source.dart';
import '../../data/datasources/auth_remote_data_source_impl.dart';

/// HTTP client provider
final httpClientProvider = Provider<http.Client>((ref) {
  return http.Client();
});

/// Secure storage provider
final secureStorageProvider = Provider<SecureStorageService>((ref) {
  return SecureStorageService();
});

/// Auth remote data source provider
final authRemoteDataSourceProvider = Provider<AuthRemoteDataSource>((ref) {
  return AuthRemoteDataSourceImpl(
    httpClient: ref.read(httpClientProvider),
    secureStorage: ref.read(secureStorageProvider),
  );
});

/// Auth repository provider
final authRepositoryProvider = Provider<AuthRepository>((ref) {
  return HttpAuthRepository(
    remoteDataSource: ref.read(authRemoteDataSourceProvider),
  );
});

/// Login use case provider
final loginUseCaseProvider = Provider<LoginUseCase>((ref) {
  return LoginUseCase(ref.read(authRepositoryProvider));
});

/// Register use case provider - Will be enabled in Phase 2
// final registerUseCaseProvider = Provider<RegisterUseCase>((ref) {
//   return RegisterUseCase(ref.read(authRepositoryProvider));
// });

/// Logout use case provider
final logoutUseCaseProvider = Provider<LogoutUseCase>((ref) {
  return LogoutUseCase(ref.read(authRepositoryProvider));
});

/// Get current user use case provider
final getCurrentUserUseCaseProvider = Provider<GetCurrentUserUseCase>((ref) {
  return GetCurrentUserUseCase(ref.read(authRepositoryProvider));
});

/// Auth state notifier
class AuthNotifier extends StateNotifier<AuthState> {
  final LoginUseCase _loginUseCase;
  // final RegisterUseCase _registerUseCase; // Will be enabled in Phase 2
  final LogoutUseCase _logoutUseCase;
  final GetCurrentUserUseCase _getCurrentUserUseCase;

  AuthNotifier({
    required LoginUseCase loginUseCase,
    // required RegisterUseCase registerUseCase, // Will be enabled in Phase 2
    required LogoutUseCase logoutUseCase,
    required GetCurrentUserUseCase getCurrentUserUseCase,
  })  : _loginUseCase = loginUseCase,
        // _registerUseCase = registerUseCase, // Will be enabled in Phase 2
        _logoutUseCase = logoutUseCase,
        _getCurrentUserUseCase = getCurrentUserUseCase,
        super(const AuthInitial());

  /// Initialize auth state by checking for existing session
  Future<void> initialize() async {
    state = const AuthLoading();
    
    final result = await _getCurrentUserUseCase();
    
    result.fold(
      (failure) => state = const AuthUnauthenticated(),
      (user) => state = AuthAuthenticated(user),
    );
  }

  /// Login user with email and password
  Future<void> login({
    required String email,
    required String password,
  }) async {
    state = const AuthLoading();
    
    final result = await _loginUseCase(
      email: email,
      password: password,
    );
    
    result.fold(
      (failure) => state = AuthError(failure),
      (user) => state = AuthAuthenticated(user),
    );
  }

  /// Register new user - Will be enabled in Phase 2
  Future<void> register({
    required String email,
    required String password,
    String? firstName,
    String? lastName,
  }) async {
    state = const AuthLoading();
    
    // Phase 2: Real registration will be implemented
    state = AuthError(ServerFailure(message: 'Registration will be available in Phase 2'));
  }

  /// Logout current user
  Future<void> logout() async {
    state = const AuthLoading();
    
    final result = await _logoutUseCase();
    
    result.fold(
      (failure) => state = AuthError(failure),
      (success) => state = const AuthUnauthenticated(),
    );
  }

  /// Check if user is authenticated
  bool get isAuthenticated => state.isAuthenticated;

  /// Get current user if authenticated
  User? get currentUser => state.user;

  /// Check if auth operation is in progress
  bool get isLoading => state.isLoading;

  /// Get current error if any
  String? get errorMessage => state.failure?.message;
}

/// Auth state notifier provider
final authNotifierProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier(
    loginUseCase: ref.read(loginUseCaseProvider),
    // registerUseCase: ref.read(registerUseCaseProvider), // Will be enabled in Phase 2
    logoutUseCase: ref.read(logoutUseCaseProvider),
    getCurrentUserUseCase: ref.read(getCurrentUserUseCaseProvider),
  );
});

/// Convenient provider for auth state
final authStateProvider = Provider<AuthState>((ref) {
  return ref.watch(authNotifierProvider);
});

/// Convenient provider for authenticated user
final currentUserProvider = Provider<User?>((ref) {
  return ref.watch(authNotifierProvider.notifier).currentUser;
});

/// Convenient provider for loading state
final authLoadingProvider = Provider<bool>((ref) {
  return ref.watch(authNotifierProvider.notifier).isLoading;
});

/// Convenient provider for error message
final authErrorProvider = Provider<String?>((ref) {
  return ref.watch(authNotifierProvider.notifier).errorMessage;
});

/// Convenient provider for authenticated state
final isAuthenticatedProvider = Provider<bool>((ref) {
  return ref.watch(authNotifierProvider.notifier).isAuthenticated;
});

/// Navigation guard provider - checks if user should be redirected
final navigationGuardProvider = Provider<String?>((ref) {
  final authState = ref.watch(authStateProvider);
  
  if (authState is AuthAuthenticated) {
    return '/home';
  } else if (authState is AuthUnauthenticated || authState is AuthError) {
    return '/login';
  }
  return null; // AuthInitial or AuthLoading
});

/// Auto initialization provider
final authInitializationProvider = FutureProvider<void>((ref) async {
  final authNotifier = ref.read(authNotifierProvider.notifier);
  await authNotifier.initialize();
});
