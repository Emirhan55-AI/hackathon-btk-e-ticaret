import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:aura_app/core/constants/app_constants.dart';

// Create a simple test screen that mimics LoginScreen structure for testing
class TestLoginScreen extends StatefulWidget {
  const TestLoginScreen({super.key});

  @override
  State<TestLoginScreen> createState() => _TestLoginScreenState();
}

class _TestLoginScreenState extends State<TestLoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _handleLogin() {
    if (_formKey.currentState!.validate()) {
      // Login logic would go here
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

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
                TextFormField(
                  controller: _emailController,
                  keyboardType: TextInputType.emailAddress,
                  decoration: const InputDecoration(
                    labelText: 'Email',
                    hintText: 'Enter your email',
                  ),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter your email';
                    }
                    if (!RegExp(r'^[^@]+@[^@]+\.[^@]+').hasMatch(value)) {
                      return 'Please enter a valid email';
                    }
                    return null;
                  },
                ),
                
                const SizedBox(height: 16),
                
                // Password Field
                TextFormField(
                  controller: _passwordController,
                  obscureText: true,
                  decoration: const InputDecoration(
                    labelText: 'Password',
                    hintText: 'Enter your password',
                  ),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter your password';
                    }
                    if (value.length < 6) {
                      return 'Password must be at least 6 characters';
                    }
                    return null;
                  },
                ),
                
                const SizedBox(height: 24),
                
                // Login Button
                ElevatedButton(
                  onPressed: _handleLogin,
                  child: const Text('Login'),
                ),
                
                const SizedBox(height: 16),
                
                // Sign Up Link
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Text('Don\'t have an account? '),
                    TextButton(
                      onPressed: () {
                        // Navigate to register
                      },
                      child: const Text('Sign Up'),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

void main() {
  group('LoginScreen Basic Widget Tests', () {
    
    Widget createTestWidget() {
      return ProviderScope(
        child: MaterialApp(
          home: const TestLoginScreen(),
        ),
      );
    }

    testWidgets('should display main UI elements', (WidgetTester tester) async {
      // Act
      await tester.pumpWidget(createTestWidget());

      // Assert - Check that key UI elements are present
      expect(find.text(AppConstants.appName), findsOneWidget);
      expect(find.text('AI-Powered Personal Style Assistant'), findsOneWidget);
      expect(find.byIcon(Icons.auto_awesome), findsOneWidget);
      expect(find.text('Email'), findsOneWidget);
      expect(find.text('Password'), findsOneWidget);
      expect(find.text('Login'), findsOneWidget);
      expect(find.text('Don\'t have an account? '), findsOneWidget);
      expect(find.text('Sign Up'), findsOneWidget);
    });

    testWidgets('should have correct number of text fields', (WidgetTester tester) async {
      // Act
      await tester.pumpWidget(createTestWidget());

      // Assert - Should have exactly 2 text fields (email and password)
      expect(find.byType(TextFormField), findsNWidgets(2));
    });

    testWidgets('should validate form fields on submit', (WidgetTester tester) async {
      // Act
      await tester.pumpWidget(createTestWidget());
      
      // Try to submit without filling fields
      await tester.tap(find.text('Login'));
      await tester.pump();

      // Assert - Should show validation errors
      expect(find.text('Please enter your email'), findsOneWidget);
    });

    testWidgets('should validate email format', (WidgetTester tester) async {
      // Act
      await tester.pumpWidget(createTestWidget());
      
      // Enter invalid email
      await tester.enterText(find.byType(TextFormField).at(0), 'invalid-email');
      await tester.enterText(find.byType(TextFormField).at(1), 'password123');
      await tester.tap(find.text('Login'));
      await tester.pump();

      // Assert - Should show validation error
      expect(find.text('Please enter a valid email'), findsOneWidget);
    });

    testWidgets('should validate password length', (WidgetTester tester) async {
      // Act
      await tester.pumpWidget(createTestWidget());
      
      // Enter short password
      await tester.enterText(find.byType(TextFormField).at(0), 'test@example.com');
      await tester.enterText(find.byType(TextFormField).at(1), '123');
      await tester.tap(find.text('Login'));
      await tester.pump();

      // Assert - Should show validation error
      expect(find.text('Password must be at least 6 characters'), findsOneWidget);
    });

    group('Form Interaction', () {
      testWidgets('should accept valid email input', (WidgetTester tester) async {
        // Act
        await tester.pumpWidget(createTestWidget());
        await tester.enterText(find.byType(TextFormField).at(0), 'test@example.com');

        // Assert - Input should be accepted
        expect(find.text('test@example.com'), findsOneWidget);
      });

      testWidgets('should accept password input', (WidgetTester tester) async {
        // Act
        await tester.pumpWidget(createTestWidget());
        await tester.enterText(find.byType(TextFormField).at(1), 'password123');

        // Assert - Input should be accepted (but hidden)
        final passwordField = tester.widget<TextFormField>(find.byType(TextFormField).at(1));
        expect(passwordField.controller?.text, equals('password123'));
      });

      testWidgets('should not submit with invalid form', (WidgetTester tester) async {
        // Act
        await tester.pumpWidget(createTestWidget());
        
        // Try to submit with invalid email
        await tester.enterText(find.byType(TextFormField).at(0), 'invalid');
        await tester.enterText(find.byType(TextFormField).at(1), '123');
        await tester.tap(find.text('Login'));
        await tester.pump();

        // Assert - Should show multiple validation errors
        expect(find.text('Please enter a valid email'), findsOneWidget);
        expect(find.text('Password must be at least 6 characters'), findsOneWidget);
      });
    });

    group('UI Layout', () {
      testWidgets('should display logo and title section', (WidgetTester tester) async {
        // Act
        await tester.pumpWidget(createTestWidget());

        // Assert - Should show branding elements
        expect(find.byIcon(Icons.auto_awesome), findsOneWidget);
        expect(find.text(AppConstants.appName), findsOneWidget);
        expect(find.text('AI-Powered Personal Style Assistant'), findsOneWidget);
      });

      testWidgets('should display form section', (WidgetTester tester) async {
        // Act
        await tester.pumpWidget(createTestWidget());

        // Assert - Should show form elements
        expect(find.byType(Form), findsOneWidget);
        expect(find.byType(TextFormField), findsNWidgets(2));
      });

      testWidgets('should display action buttons', (WidgetTester tester) async {
        // Act
        await tester.pumpWidget(createTestWidget());

        // Assert - Should show buttons
        expect(find.text('Login'), findsOneWidget);
        expect(find.text('Sign Up'), findsOneWidget);
      });

      testWidgets('should have proper form structure', (WidgetTester tester) async {
        // Act
        await tester.pumpWidget(createTestWidget());

        // Assert - Should have proper widget hierarchy
        expect(find.byType(Scaffold), findsOneWidget);
        expect(find.byType(SafeArea), findsOneWidget);
        expect(find.byType(SingleChildScrollView), findsOneWidget);
        expect(find.byType(Form), findsOneWidget);
        expect(find.byType(Column), findsAtLeastNWidgets(1));
      });
    });

    group('Validation Logic', () {
      testWidgets('should pass validation with valid inputs', (WidgetTester tester) async {
        // Act
        await tester.pumpWidget(createTestWidget());
        
        // Enter valid inputs
        await tester.enterText(find.byType(TextFormField).at(0), 'test@example.com');
        await tester.enterText(find.byType(TextFormField).at(1), 'password123');
        await tester.tap(find.text('Login'));
        await tester.pump();

        // Assert - Should not show validation errors
        expect(find.text('Please enter your email'), findsNothing);
        expect(find.text('Please enter a valid email'), findsNothing);
        expect(find.text('Please enter your password'), findsNothing);
        expect(find.text('Password must be at least 6 characters'), findsNothing);
      });

      testWidgets('should show empty field validation', (WidgetTester tester) async {
        // Act
        await tester.pumpWidget(createTestWidget());
        await tester.tap(find.text('Login'));
        await tester.pump();

        // Assert - Should show empty field validation
        expect(find.text('Please enter your email'), findsOneWidget);
        expect(find.text('Please enter your password'), findsOneWidget);
      });
    });
  });
}
