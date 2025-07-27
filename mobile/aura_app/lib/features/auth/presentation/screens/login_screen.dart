import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/constants/app_constants.dart';
import '../../../../core/utils/app_utils.dart';
import '../../domain/entities/auth_state.dart';
import '../notifiers/auth_provider.dart';
import '../components/auth_button.dart';
import '../components/auth_text_field.dart';

/// Login screen with authentication functionality
class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _handleLogin() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    await ref.read(authNotifierProvider.notifier).login(
      email: _emailController.text.trim(),
      password: _passwordController.text,
    );
  }

  void _navigateToRegister() {
    context.push('/register');
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    // Listen to auth state for navigation and error handling
    ref.listen<AuthState>(authNotifierProvider, (previous, next) {
      if (next is AuthAuthenticated) {
        // Navigate to home on successful authentication
        if (context.mounted) {
          context.go('/home');
        }
      } else if (next is AuthError) {
        // Show error message
        if (context.mounted) {
          AppUtils.showErrorSnackbar(context, next.failure.message);
        }
      }
    });

    final authState = ref.watch(authNotifierProvider);

    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const SizedBox(height: 60),
                
                // Logo and Title
                Column(
                  children: [
                    Icon(
                      Icons.auto_awesome,
                      size: 64,
                      color: theme.primaryColor,
                    ),
                    const SizedBox(height: 16),
                    Text(
                      AppConstants.appName,
                      style: theme.textTheme.headlineLarge?.copyWith(
                        fontWeight: FontWeight.bold,
                        color: theme.primaryColor,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'AI-Powered Personal Style Assistant',
                      style: theme.textTheme.bodyMedium?.copyWith(
                        color: theme.colorScheme.outline,
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ],
                ),
                
                const SizedBox(height: 48),
                
                // Email Field
                AuthTextField(
                  controller: _emailController,
                  label: 'Email',
                  keyboardType: TextInputType.emailAddress,
                  prefixIcon: Icons.email_outlined,
                  validator: (value) {
                    if (value == null || value.trim().isEmpty) {
                      return 'Email is required';
                    }
                    final emailRegex = RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
                    if (!emailRegex.hasMatch(value.trim())) {
                      return 'Please enter a valid email';
                    }
                    return null;
                  },
                  enabled: !authState.maybeWhen(
                    loading: () => true,
                    orElse: () => false,
                  ),
                ),
                
                const SizedBox(height: 16),
                
                // Password Field
                AuthTextField(
                  controller: _passwordController,
                  label: 'Password',
                  obscureText: true,
                  prefixIcon: Icons.lock_outlined,
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Password is required';
                    }
                    if (value.length < 6) {
                      return 'Password must be at least 6 characters';
                    }
                    return null;
                  },
                  enabled: !authState.maybeWhen(
                    loading: () => true,
                    orElse: () => false,
                  ),
                ),
                
                const SizedBox(height: 24),
                
                // Login Button
                AuthButton(
                  child: authState.maybeWhen(
                    loading: () => const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                      ),
                    ),
                    orElse: () => const Text('Sign In'),
                  ),
                  onPressed: authState.maybeWhen(
                    loading: () => null,
                    orElse: () => _handleLogin,
                  ),
                ),
                
                const SizedBox(height: 16),
                
                // Forgot Password
                TextButton(
                  onPressed: authState.maybeWhen(
                    loading: () => null,
                    orElse: () => () {
                      AppUtils.showInfoSnackbar(context, 'Password reset feature coming soon!');
                    },
                  ),
                  child: Text(
                    'Forgot Password?',
                    style: TextStyle(color: theme.primaryColor),
                  ),
                ),
                
                const SizedBox(height: 32),
                
                // Divider
                Row(
                  children: [
                    Expanded(child: Divider(color: theme.dividerColor)),
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 16),
                      child: Text(
                        'OR',
                        style: theme.textTheme.bodySmall?.copyWith(
                          color: theme.colorScheme.outline,
                        ),
                      ),
                    ),
                    Expanded(child: Divider(color: theme.dividerColor)),
                  ],
                ),
                
                const SizedBox(height: 32),
                
                // Register Button
                OutlinedButton(
                  onPressed: authState.maybeWhen(
                    loading: () => null,
                    orElse: () => _navigateToRegister,
                  ),
                  style: OutlinedButton.styleFrom(
                    foregroundColor: theme.primaryColor,
                    side: BorderSide(color: theme.primaryColor),
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: const Text('Create Account'),
                ),
                
                const SizedBox(height: 24),
                
                // Demo Info
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: theme.colorScheme.surfaceContainerHighest,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Column(
                    children: [
                      Icon(
                        Icons.info_outline,
                        color: theme.colorScheme.primary,
                        size: 20,
                      ),
                      const SizedBox(height: 8),
                      Text(
                        'Demo Credentials',
                        style: theme.textTheme.titleSmall?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        'Email: demo@aura.com\nPassword: demo123',
                        style: theme.textTheme.bodySmall,
                        textAlign: TextAlign.center,
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
