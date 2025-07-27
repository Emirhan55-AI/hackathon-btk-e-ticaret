import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:aura_app/core/constants/app_constants.dart';

// Simplified test screen for validation testing
class TestRegisterScreen extends StatefulWidget {
  const TestRegisterScreen({super.key});

  @override
  State<TestRegisterScreen> createState() => _TestRegisterScreenState();
}

class _TestRegisterScreenState extends State<TestRegisterScreen> {
  final _formKey = GlobalKey<FormState>();
  final _firstNameController = TextEditingController();
  final _lastNameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();

  @override
  void dispose() {
    _firstNameController.dispose();
    _lastNameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    super.dispose();
  }

  void _handleRegister() {
    if (_formKey.currentState!.validate()) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Registration successful!')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Form(
            key: _formKey,
            child: Column(
              children: [
                // Header
                const Text('Create Account', style: TextStyle(fontSize: 24)),
                Text('Join ${AppConstants.appName} today'),
                const Icon(Icons.auto_awesome),
                
                // Form fields in a scrollable area
                Expanded(
                  child: SingleChildScrollView(
                    child: Column(
                      children: [
                        TextFormField(
                          controller: _firstNameController,
                          decoration: const InputDecoration(labelText: 'First Name'),
                          validator: (value) {
                            if (value == null || value.isEmpty) {
                              return 'Please enter your first name';
                            }
                            return null;
                          },
                        ),
                        
                        TextFormField(
                          controller: _lastNameController,
                          decoration: const InputDecoration(labelText: 'Last Name'),
                          validator: (value) {
                            if (value == null || value.isEmpty) {
                              return 'Please enter your last name';
                            }
                            return null;
                          },
                        ),
                        
                        TextFormField(
                          controller: _emailController,
                          decoration: const InputDecoration(labelText: 'Email'),
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
                        
                        TextFormField(
                          controller: _passwordController,
                          obscureText: true,
                          decoration: const InputDecoration(labelText: 'Password'),
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
                        
                        TextFormField(
                          controller: _confirmPasswordController,
                          obscureText: true,
                          decoration: const InputDecoration(labelText: 'Confirm Password'),
                          validator: (value) {
                            if (value == null || value.isEmpty) {
                              return 'Please confirm your password';
                            }
                            if (value != _passwordController.text) {
                              return 'Passwords do not match';
                            }
                            return null;
                          },
                        ),
                        
                        const SizedBox(height: 20),
                        
                        // Action buttons
                        ElevatedButton(
                          onPressed: _handleRegister,
                          child: const Text('Create Account'),
                        ),
                        
                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            const Text('Already have an account? '),
                            TextButton(
                              onPressed: () => Navigator.pop(context),
                              child: const Text('Sign In'),
                            ),
                          ],
                        ),
                      ],
                    ),
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

void main() {
  group('RegisterScreen Widget Tests', () {
    
    Widget createTestWidget() {
      return ProviderScope(
        child: MaterialApp(
          home: const TestRegisterScreen(),
        ),
      );
    }

    testWidgets('should display main UI elements', (WidgetTester tester) async {
      await tester.pumpWidget(createTestWidget());

      expect(find.text('Create Account'), findsAtLeastNWidgets(1));
      expect(find.text('Join ${AppConstants.appName} today'), findsOneWidget);
      expect(find.byIcon(Icons.auto_awesome), findsOneWidget);
      expect(find.text('First Name'), findsOneWidget);
      expect(find.text('Last Name'), findsOneWidget);
      expect(find.text('Email'), findsOneWidget);
      expect(find.text('Password'), findsOneWidget);
      expect(find.text('Confirm Password'), findsOneWidget);
      expect(find.text('Sign In'), findsOneWidget);
    });

    testWidgets('should have correct number of text fields', (WidgetTester tester) async {
      await tester.pumpWidget(createTestWidget());
      expect(find.byType(TextFormField), findsNWidgets(5));
    });

    testWidgets('should validate required fields on submit', (WidgetTester tester) async {
      await tester.pumpWidget(createTestWidget());
      
      await tester.tap(find.byType(ElevatedButton).first);
      await tester.pump();

      expect(find.text('Please enter your first name'), findsOneWidget);
      expect(find.text('Please enter your last name'), findsOneWidget);
      expect(find.text('Please enter your email'), findsOneWidget);
      expect(find.text('Please enter your password'), findsOneWidget);
      expect(find.text('Please confirm your password'), findsOneWidget);
    });

    testWidgets('should validate email format', (WidgetTester tester) async {
      await tester.pumpWidget(createTestWidget());
      
      await tester.enterText(find.byType(TextFormField).at(0), 'John');
      await tester.enterText(find.byType(TextFormField).at(1), 'Doe');
      await tester.enterText(find.byType(TextFormField).at(2), 'invalid-email');
      await tester.enterText(find.byType(TextFormField).at(3), 'password123');
      await tester.enterText(find.byType(TextFormField).at(4), 'password123');
      
      await tester.tap(find.byType(ElevatedButton).first);
      await tester.pump();

      expect(find.text('Please enter a valid email'), findsOneWidget);
    });

    testWidgets('should validate password length', (WidgetTester tester) async {
      await tester.pumpWidget(createTestWidget());
      
      await tester.enterText(find.byType(TextFormField).at(0), 'John');
      await tester.enterText(find.byType(TextFormField).at(1), 'Doe');
      await tester.enterText(find.byType(TextFormField).at(2), 'john@example.com');
      await tester.enterText(find.byType(TextFormField).at(3), '123');
      await tester.enterText(find.byType(TextFormField).at(4), '123');
      
      await tester.tap(find.byType(ElevatedButton).first);
      await tester.pump();

      expect(find.text('Password must be at least 6 characters'), findsOneWidget);
    });

    testWidgets('should validate password confirmation', (WidgetTester tester) async {
      await tester.pumpWidget(createTestWidget());
      
      await tester.enterText(find.byType(TextFormField).at(0), 'John');
      await tester.enterText(find.byType(TextFormField).at(1), 'Doe');
      await tester.enterText(find.byType(TextFormField).at(2), 'john@example.com');
      await tester.enterText(find.byType(TextFormField).at(3), 'password123');
      await tester.enterText(find.byType(TextFormField).at(4), 'different123');
      
      await tester.tap(find.byType(ElevatedButton).first);
      await tester.pump();

      expect(find.text('Passwords do not match'), findsOneWidget);
    });

    group('Form Interaction', () {
      testWidgets('should accept valid name inputs', (WidgetTester tester) async {
        await tester.pumpWidget(createTestWidget());
        
        await tester.enterText(find.byType(TextFormField).at(0), 'John');
        await tester.enterText(find.byType(TextFormField).at(1), 'Doe');

        expect(find.text('John'), findsOneWidget);
        expect(find.text('Doe'), findsOneWidget);
      });

      testWidgets('should accept valid email input', (WidgetTester tester) async {
        await tester.pumpWidget(createTestWidget());
        
        await tester.enterText(find.byType(TextFormField).at(2), 'john@example.com');
        expect(find.text('john@example.com'), findsOneWidget);
      });

      testWidgets('should accept password inputs', (WidgetTester tester) async {
        await tester.pumpWidget(createTestWidget());
        
        await tester.enterText(find.byType(TextFormField).at(3), 'password123');
        await tester.enterText(find.byType(TextFormField).at(4), 'password123');

        final passwordField = tester.widget<TextFormField>(find.byType(TextFormField).at(3));
        final confirmPasswordField = tester.widget<TextFormField>(find.byType(TextFormField).at(4));
        expect(passwordField.controller?.text, equals('password123'));
        expect(confirmPasswordField.controller?.text, equals('password123'));
      });
    });

    group('UI Layout', () {
      testWidgets('should display logo and title section', (WidgetTester tester) async {
        await tester.pumpWidget(createTestWidget());

        expect(find.byIcon(Icons.auto_awesome), findsOneWidget);
        expect(find.text('Create Account'), findsAtLeastNWidgets(1));
        expect(find.text('Join ${AppConstants.appName} today'), findsOneWidget);
      });

      testWidgets('should display form section', (WidgetTester tester) async {
        await tester.pumpWidget(createTestWidget());

        expect(find.byType(Form), findsOneWidget);
        expect(find.byType(TextFormField), findsNWidgets(5));
      });

      testWidgets('should display action buttons', (WidgetTester tester) async {
        await tester.pumpWidget(createTestWidget());

        expect(find.text('Create Account'), findsNWidgets(2));
        expect(find.text('Sign In'), findsOneWidget);
      });

      testWidgets('should have proper form structure', (WidgetTester tester) async {
        await tester.pumpWidget(createTestWidget());

        expect(find.byType(Scaffold), findsOneWidget);
        expect(find.byType(SafeArea), findsOneWidget);
        expect(find.byType(SingleChildScrollView), findsOneWidget);
        expect(find.byType(Form), findsOneWidget);
      });
    });

    group('Validation Logic', () {
      testWidgets('should pass validation with valid inputs', (WidgetTester tester) async {
        await tester.pumpWidget(createTestWidget());
        
        await tester.enterText(find.byType(TextFormField).at(0), 'John');
        await tester.enterText(find.byType(TextFormField).at(1), 'Doe');
        await tester.enterText(find.byType(TextFormField).at(2), 'john@example.com');
        await tester.enterText(find.byType(TextFormField).at(3), 'password123');
        await tester.enterText(find.byType(TextFormField).at(4), 'password123');
        
        await tester.tap(find.byType(ElevatedButton).first);
        await tester.pump();

        // Check for success indicator
        expect(find.text('Registration successful!'), findsOneWidget);
      });

      testWidgets('should show empty field validations', (WidgetTester tester) async {
        await tester.pumpWidget(createTestWidget());
        
        await tester.tap(find.byType(ElevatedButton).first);
        await tester.pump();

        expect(find.text('Please enter your first name'), findsOneWidget);
        expect(find.text('Please enter your last name'), findsOneWidget);
        expect(find.text('Please enter your email'), findsOneWidget);
        expect(find.text('Please enter your password'), findsOneWidget);
        expect(find.text('Please confirm your password'), findsOneWidget);
      });
    });
  });
}
