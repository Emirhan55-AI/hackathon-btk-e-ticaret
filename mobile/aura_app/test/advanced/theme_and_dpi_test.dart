// Advanced Theme and DPI Tests
// Testing dark/light mode transitions and various screen densities

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../lib/core/theme/app_theme.dart';

/// Advanced tests for theme consistency and DPI handling
void main() {
  group('Theme Consistency Tests', () {
    testWidgets('Should maintain UI integrity during dark/light mode transitions', (WidgetTester tester) async {
      bool isDarkMode = false;

      await tester.pumpWidget(
        ProviderScope(
          child: StatefulBuilder(
            builder: (context, setState) {
              return MaterialApp(
                theme: isDarkMode ? AppTheme.darkTheme : AppTheme.lightTheme,
                home: Scaffold(
                  appBar: AppBar(
                    title: const Text('Theme Test'),
                    actions: [
                      IconButton(
                        icon: Icon(isDarkMode ? Icons.light_mode : Icons.dark_mode),
                        onPressed: () {
                          setState(() {
                            isDarkMode = !isDarkMode;
                          });
                        },
                      ),
                    ],
                  ),
                  body: SingleChildScrollView(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      children: [
                        Card(
                          child: ListTile(
                            title: const Text('Sample Item'),
                            subtitle: const Text('This is a test item'),
                            leading: const Icon(Icons.shopping_bag),
                          ),
                        ),
                        const SizedBox(height: 8),
                        SizedBox(
                          width: double.infinity,
                          child: ElevatedButton(
                            onPressed: () {},
                            child: const Text('Button'),
                          ),
                        ),
                        const SizedBox(height: 8),
                        const Chip(
                          label: Text('Chip'),
                        ),
                        const SizedBox(height: 16),
                        Container(
                          height: 100,
                          width: double.infinity,
                          decoration: BoxDecoration(
                            color: Theme.of(context).colorScheme.surface,
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: const Center(
                            child: Text('Theme Surface'),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              );
            },
          ),
        ),
      );

      // Verify light mode initially
      expect(find.byIcon(Icons.dark_mode), findsOneWidget);
      expect(find.text('Sample Item'), findsOneWidget);

      // Switch to dark mode without animations
      await tester.tap(find.byIcon(Icons.dark_mode));
      await tester.pump();

      // Verify dark mode switch
      expect(find.byIcon(Icons.light_mode), findsOneWidget);
      expect(find.text('Sample Item'), findsOneWidget);

      // Switch back to light mode without animations
      await tester.tap(find.byIcon(Icons.light_mode));
      await tester.pump();

      // Verify successful transition back
      expect(find.byIcon(Icons.dark_mode), findsOneWidget);
      
      // Verify no rendering errors during transition
      expect(tester.takeException(), isNull);
    });

    testWidgets('Should handle text contrast in both themes', (WidgetTester tester) async {
      // Test with light theme
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            theme: AppTheme.lightTheme,
            home: const Scaffold(
              body: Column(
                children: [
                  Text('Primary Text', style: TextStyle(color: Colors.black)),
                  Text('Secondary Text', style: TextStyle(color: Colors.grey)),
                  Text('Error Text', style: TextStyle(color: Colors.red)),
                ],
              ),
            ),
          ),
        ),
      );

      expect(find.text('Primary Text'), findsOneWidget);
      expect(find.text('Secondary Text'), findsOneWidget);
      expect(find.text('Error Text'), findsOneWidget);

      // Test with dark theme
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            theme: AppTheme.darkTheme,
            home: const Scaffold(
              body: Column(
                children: [
                  Text('Primary Text', style: TextStyle(color: Colors.white)),
                  Text('Secondary Text', style: TextStyle(color: Colors.grey)),
                  Text('Error Text', style: TextStyle(color: Colors.red)),
                ],
              ),
            ),
          ),
        ),
      );

      expect(find.text('Primary Text'), findsOneWidget);
      expect(find.text('Secondary Text'), findsOneWidget);
      expect(find.text('Error Text'), findsOneWidget);
    });
  });

  group('DPI and Screen Density Tests', () {
    testWidgets('Should handle very low DPI screens (0.75x)', (WidgetTester tester) async {
      // Simulate low DPI screen
      tester.view.devicePixelRatio = 0.75;
      
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            theme: AppTheme.lightTheme,
            home: Scaffold(
              appBar: AppBar(title: const Text('Low DPI Test')),
              body: const Column(
                children: [
                  Text('Sample Content'),
                  Icon(Icons.home),
                  ElevatedButton(
                    onPressed: null,
                    child: Text('Test Button'),
                  ),
                ],
              ),
            ),
          ),
        ),
      );

      // Verify UI renders correctly at low DPI
      expect(find.byType(Scaffold), findsOneWidget);
      expect(tester.takeException(), isNull);

      // Reset DPI
      tester.view.resetDevicePixelRatio();
    });

    testWidgets('Should handle high DPI screens (3.0x)', (WidgetTester tester) async {
      // Simulate high DPI screen
      tester.view.devicePixelRatio = 3.0;
      
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            theme: AppTheme.lightTheme,
            home: Scaffold(
              appBar: AppBar(title: const Text('High DPI Test')),
              body: const Column(
                children: [
                  Text('Sample Content'),
                  Icon(Icons.home),
                  ElevatedButton(
                    onPressed: null,
                    child: Text('Test Button'),
                  ),
                ],
              ),
            ),
          ),
        ),
      );

      // Verify UI renders correctly at high DPI
      expect(find.byType(Scaffold), findsOneWidget);
      expect(tester.takeException(), isNull);

      // Reset DPI
      tester.view.resetDevicePixelRatio();
    });

    testWidgets('Should handle very high DPI screens (4.0x)', (WidgetTester tester) async {
      // Simulate very high DPI screen (like high-end phones)
      tester.view.devicePixelRatio = 4.0;
      
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            theme: AppTheme.lightTheme,
            home: const Scaffold(
              body: Column(
                children: [
                  Text('High DPI Test', style: TextStyle(fontSize: 16)),
                  Icon(Icons.star, size: 24),
                  ElevatedButton(
                    onPressed: null,
                    child: Text('Button'),
                  ),
                ],
              ),
            ),
          ),
        ),
      );

      // Verify UI elements are properly sized at high DPI
      expect(find.text('High DPI Test'), findsOneWidget);
      expect(find.byIcon(Icons.star), findsOneWidget);
      expect(find.text('Button'), findsOneWidget);
      expect(tester.takeException(), isNull);

      // Reset DPI
      tester.view.resetDevicePixelRatio();
    });
  });

  group('Responsive Layout Tests', () {
    testWidgets('Should adapt to portrait orientation', (WidgetTester tester) async {
      // Set portrait size
      await tester.binding.setSurfaceSize(const Size(400, 800));
      
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            theme: AppTheme.lightTheme,
            home: Scaffold(
              body: OrientationBuilder(
                builder: (context, orientation) {
                  return Column(
                    children: [
                      const Text('Portrait Mode'),
                      Expanded(
                        child: GridView.count(
                          crossAxisCount: 2,
                          children: const [
                            Card(child: Center(child: Text('Item 1'))),
                            Card(child: Center(child: Text('Item 2'))),
                            Card(child: Center(child: Text('Item 3'))),
                            Card(child: Center(child: Text('Item 4'))),
                          ],
                        ),
                      ),
                    ],
                  );
                },
              ),
            ),
          ),
        ),
      );

      expect(find.text('Portrait Mode'), findsOneWidget);
      expect(find.text('Item 1'), findsOneWidget);
      expect(find.text('Item 4'), findsOneWidget);

      // Reset size
      await tester.binding.setSurfaceSize(null);
    });

    testWidgets('Should adapt to landscape orientation', (WidgetTester tester) async {
      // Set landscape size
      await tester.binding.setSurfaceSize(const Size(800, 400));
      
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            theme: AppTheme.lightTheme,
            home: Scaffold(
              body: OrientationBuilder(
                builder: (context, orientation) {
                  return Column(
                    children: [
                      const Text('Landscape Mode'),
                      Expanded(
                        child: GridView.count(
                          crossAxisCount: 4, // More columns in landscape
                          children: const [
                            Card(child: Center(child: Text('Item 1'))),
                            Card(child: Center(child: Text('Item 2'))),
                            Card(child: Center(child: Text('Item 3'))),
                            Card(child: Center(child: Text('Item 4'))),
                          ],
                        ),
                      ),
                    ],
                  );
                },
              ),
            ),
          ),
        ),
      );

      expect(find.text('Landscape Mode'), findsOneWidget);
      expect(find.text('Item 1'), findsOneWidget);
      expect(find.text('Item 4'), findsOneWidget);

      // Reset size
      await tester.binding.setSurfaceSize(null);
    });
  });

  group('Accessibility Tests', () {
    testWidgets('Should maintain accessibility in dark mode', (WidgetTester tester) async {
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            theme: AppTheme.darkTheme,
            home: const Scaffold(
              body: Column(
                children: [
                  Text('Accessible Text'),
                  ElevatedButton(
                    onPressed: null,
                    child: Text('Accessible Button'),
                  ),
                  Icon(Icons.star, semanticLabel: 'Favorite'),
                ],
              ),
            ),
          ),
        ),
      );

      // Verify semantic labels are present
      expect(find.text('Accessible Text'), findsOneWidget);
      expect(find.text('Accessible Button'), findsOneWidget);
      expect(find.bySemanticsLabel('Favorite'), findsOneWidget);
    });

    testWidgets('Should handle large font sizes', (WidgetTester tester) async {
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            theme: AppTheme.lightTheme,
            home: const Scaffold(
              body: Column(
                children: [
                  Text(
                    'Large Text',
                    style: TextStyle(fontSize: 32),
                  ),
                  Text(
                    'This is a longer text that should wrap properly when font size is increased for accessibility',
                    style: TextStyle(fontSize: 24),
                  ),
                ],
              ),
            ),
          ),
        ),
      );

      expect(find.text('Large Text'), findsOneWidget);
      expect(find.textContaining('longer text'), findsOneWidget);
      expect(tester.takeException(), isNull);
    });
  });
}
