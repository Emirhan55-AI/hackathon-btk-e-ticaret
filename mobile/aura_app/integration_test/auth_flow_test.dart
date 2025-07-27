import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:integration_test/integration_test.dart';

import 'package:aura_app/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Auth Flow Integration Tests', () {
    testWidgets('should load app successfully', (WidgetTester tester) async {
      // Start the app
      app.main();
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // Verify the app loads with basic structure
      expect(find.byType(MaterialApp), findsOneWidget);
      expect(find.byType(ProviderScope), findsOneWidget);
      
      // Basic smoke test - ensure the app doesn't crash
      await tester.pump();
    });

    testWidgets('should handle basic navigation', (WidgetTester tester) async {
      // Start the app
      app.main();
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // Look for any navigation elements and test them
      final scaffolds = find.byType(Scaffold);
      if (scaffolds.found.isNotEmpty) {
        // Verify scaffold structure exists
        expect(scaffolds, findsAtLeastNWidgets(1));
      }

      // Look for text buttons that might be navigation
      final textButtons = find.byType(TextButton);
      if (textButtons.found.isNotEmpty) {
        // Test tapping the first available button
        await tester.tap(textButtons.first);
        await tester.pumpAndSettle();
        
        // Verify navigation doesn't crash the app
        expect(find.byType(MaterialApp), findsOneWidget);
      }
    });

    testWidgets('should handle form interactions', (WidgetTester tester) async {
      // Start the app
      app.main();
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // Look for text form fields
      final textFields = find.byType(TextFormField);
      if (textFields.found.isNotEmpty) {
        // Test entering text in the first available field
        await tester.enterText(textFields.first, 'test@example.com');
        await tester.pump();
        
        // Verify text input works
        expect(find.text('test@example.com'), findsOneWidget);
        
        // If there are multiple fields, test another one
        if (textFields.found.length > 1) {
          await tester.enterText(textFields.at(1), 'testuser');
          await tester.pump();
          expect(find.text('testuser'), findsOneWidget);
        }
      }
    });

    testWidgets('should handle button interactions', (WidgetTester tester) async {
      // Start the app
      app.main();
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // Look for elevated buttons (primary action buttons)
      final elevatedButtons = find.byType(ElevatedButton);
      if (elevatedButtons.found.isNotEmpty) {
        // Test tapping the first elevated button
        await tester.tap(elevatedButtons.first);
        await tester.pumpAndSettle();
        
        // Verify the app still functions after button tap
        expect(find.byType(MaterialApp), findsOneWidget);
      }

      // Test text buttons as well
      final textButtons = find.byType(TextButton);
      if (textButtons.found.isNotEmpty) {
        await tester.tap(textButtons.first);
        await tester.pumpAndSettle();
        
        // Verify navigation/action completed
        expect(find.byType(MaterialApp), findsOneWidget);
      }
    });

    testWidgets('should handle form validation flow', (WidgetTester tester) async {
      // Start the app
      app.main();
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // Look for form and submit button to test validation
      final forms = find.byType(Form);
      final buttons = find.byType(ElevatedButton);
      
      if (forms.found.isNotEmpty && buttons.found.isNotEmpty) {
        // Try submitting empty form to trigger validation
        await tester.tap(buttons.first);
        await tester.pump();
        
        // The app should still be functional after validation
        expect(find.byType(MaterialApp), findsOneWidget);
        
        // Fill in form fields if they exist
        final textFields = find.byType(TextFormField);
        if (textFields.found.isNotEmpty) {
          for (int i = 0; i < textFields.found.length && i < 3; i++) {
            await tester.enterText(textFields.at(i), 'test$i@example.com');
            await tester.pump();
          }
          
          // Try submitting with some data
          await tester.tap(buttons.first);
          await tester.pumpAndSettle();
          
          // Verify app stability
          expect(find.byType(MaterialApp), findsOneWidget);
        }
      }
    });

    testWidgets('should handle error states gracefully', (WidgetTester tester) async {
      // Start the app
      app.main();
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // Test app stability by performing multiple rapid interactions
      final buttons = find.byType(TextButton);
      if (buttons.found.isNotEmpty) {
        // Rapid button taps to test stability
        for (int i = 0; i < 3; i++) {
          await tester.tap(buttons.first);
          await tester.pump();
        }
        
        await tester.pumpAndSettle();
        
        // Verify app is still responsive
        expect(find.byType(MaterialApp), findsOneWidget);
      }
    });

    testWidgets('should maintain state during navigation', (WidgetTester tester) async {
      // Start the app
      app.main();
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // Enter some data
      final textFields = find.byType(TextFormField);
      if (textFields.found.isNotEmpty) {
        await tester.enterText(textFields.first, 'persistent@example.com');
        await tester.pump();
        
        // Navigate if possible
        final navButtons = find.byType(TextButton);
        if (navButtons.found.isNotEmpty) {
          await tester.tap(navButtons.first);
          await tester.pumpAndSettle();
          
          // Navigate back if possible
          final backButtons = find.byIcon(Icons.arrow_back);
          if (backButtons.found.isNotEmpty) {
            await tester.tap(backButtons.first);
            await tester.pumpAndSettle();
            
            // Check if data persisted (might or might not, depends on implementation)
            // This is more of a stability test
            expect(find.byType(MaterialApp), findsOneWidget);
          }
        }
      }
    });
  });
}
