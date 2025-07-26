import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../features/auth/domain/entities/auth_state.dart';
import '../../features/auth/presentation/notifiers/auth_provider.dart';
import '../../features/auth/presentation/screens/login_screen.dart';
import '../../features/auth/presentation/screens/register_screen.dart';
import '../../features/auth/presentation/screens/home_screen.dart';
import '../../features/auth/presentation/pages/splash_screen.dart';

/// App router configuration with authentication guard
final appRouterProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    initialLocation: '/splash',
    redirect: (context, state) {
      final authState = ref.read(authNotifierProvider);
      final currentPath = state.matchedLocation;
      
      // If we're on splash, let it proceed
      if (currentPath == '/splash') {
        return null;
      }
      
      return authState.when(
        initial: () => '/splash',
        loading: () => null, // Stay where we are
        authenticated: (user) {
          // If authenticated and trying to access auth pages, redirect to home
          if (currentPath == '/login' || currentPath == '/register') {
            return '/home';
          }
          return null; // Stay where we are
        },
        unauthenticated: () {
          // If not authenticated and trying to access protected pages, redirect to login
          if (currentPath != '/login' && currentPath != '/register') {
            return '/login';
          }
          return null; // Stay where we are
        },
        error: (failure) {
          // On error, redirect to login
          return '/login';
        },
      );
    },
    routes: [
      GoRoute(
        path: '/splash',
        builder: (context, state) => const SplashScreen(),
      ),
      GoRoute(
        path: '/login',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: '/register',
        builder: (context, state) => const RegisterScreen(),
      ),
      GoRoute(
        path: '/home',
        builder: (context, state) => const HomeScreen(),
      ),
      // Redirect root to splash
      GoRoute(
        path: '/',
        redirect: (context, state) => '/splash',
      ),
    ],
  );
});

/// Authentication guard widget for protected routes
class AuthGuard extends ConsumerWidget {
  final Widget child;

  const AuthGuard({super.key, required this.child});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authNotifierProvider);

    return authState.when(
      initial: () => const SplashScreen(),
      loading: () => const SplashScreen(),
      authenticated: (user) => child,
      unauthenticated: () => const LoginScreen(),
      error: (failure) => const LoginScreen(),
    );
  }
}
