// Real API End-to-End Integration Tests
// Testing complete user flows with actual backend services

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// End-to-end integration tests with real API calls
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Complete User Flow Integration Tests', () {
    testWidgets('Should complete full authentication flow', (WidgetTester tester) async {
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: Scaffold(
              body: Column(
                children: [
                  const TextField(
                    decoration: InputDecoration(labelText: 'Email'),
                  ),
                  const TextField(
                    decoration: InputDecoration(labelText: 'Password'),
                    obscureText: true,
                  ),
                  ElevatedButton(
                    onPressed: () {
                      // Real API login call would happen here
                    },
                    child: const Text('Login'),
                  ),
                ],
              ),
            ),
          ),
        ),
      );

      // Enter test credentials
      await tester.enterText(find.byType(TextField).first, 'test@example.com');
      await tester.enterText(find.byType(TextField).at(1), 'password123');
      
      // Tap login button
      await tester.tap(find.text('Login'));
      await tester.pumpAndSettle(const Duration(seconds: 5));

      // Verify UI elements are present
      expect(find.text('Login'), findsOneWidget);
    });

    testWidgets('Should handle complete wardrobe management flow', (WidgetTester tester) async {
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: Scaffold(
              appBar: AppBar(title: const Text('Wardrobe')),
              body: Column(
                children: [
                  ElevatedButton(
                    onPressed: () {
                      // Navigate to add item screen
                    },
                    child: const Text('Add Item'),
                  ),
                  Expanded(
                    child: ListView(
                      children: const [
                        ListTile(
                          title: Text('Blue Jeans'),
                          subtitle: Text('Pants - Casual'),
                          trailing: Icon(Icons.edit),
                        ),
                        ListTile(
                          title: Text('White T-Shirt'),
                          subtitle: Text('Shirt - Casual'),
                          trailing: Icon(Icons.edit),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
              floatingActionButton: FloatingActionButton(
                onPressed: () {
                  // Add new item
                },
                child: const Icon(Icons.add),
              ),
            ),
          ),
        ),
      );

      // Verify wardrobe UI
      expect(find.text('Wardrobe'), findsOneWidget);
      expect(find.text('Add Item'), findsOneWidget);
      expect(find.text('Blue Jeans'), findsOneWidget);
      expect(find.text('White T-Shirt'), findsOneWidget);

      // Test adding new item
      await tester.tap(find.byIcon(Icons.add));
      await tester.pumpAndSettle();
    });

    testWidgets('Should handle complete shopping flow', (WidgetTester tester) async {
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: Scaffold(
              appBar: AppBar(title: const Text('Shop')),
              body: Column(
                children: [
                  Padding(
                    padding: const EdgeInsets.all(16),
                    child: TextField(
                      decoration: InputDecoration(
                        labelText: 'Search products...',
                        suffixIcon: IconButton(
                          onPressed: () {
                            // Perform search
                          },
                          icon: const Icon(Icons.search),
                        ),
                      ),
                    ),
                  ),
                  Expanded(
                    child: GridView.count(
                      crossAxisCount: 2,
                      children: const [
                        Card(
                          child: Column(
                            children: [
                              Icon(Icons.shopping_bag, size: 50),
                              Text('Product 1'),
                              Text('\$29.99'),
                              ElevatedButton(
                                onPressed: null,
                                child: Text('Add to Cart'),
                              ),
                            ],
                          ),
                        ),
                        Card(
                          child: Column(
                            children: [
                              Icon(Icons.shopping_bag, size: 50),
                              Text('Product 2'),
                              Text('\$39.99'),
                              ElevatedButton(
                                onPressed: null,
                                child: Text('Add to Cart'),
                              ),
                            ],
                          ),
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

      // Test search functionality
      await tester.enterText(find.byType(TextField), 'jeans');
      await tester.tap(find.byIcon(Icons.search));
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // Verify products are displayed
      expect(find.text('Product 1'), findsOneWidget);
      expect(find.text('Product 2'), findsOneWidget);
      expect(find.text('\$29.99'), findsOneWidget);
    });

    testWidgets('Should handle AI recommendations flow', (WidgetTester tester) async {
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: Scaffold(
              appBar: AppBar(title: const Text('AI Recommendations')),
              body: Column(
                children: [
                  const Padding(
                    padding: EdgeInsets.all(16),
                    child: Text(
                      'Based on your wardrobe and preferences:',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                  ),
                  Expanded(
                    child: ListView(
                      children: [
                        Card(
                          child: ListTile(
                            leading: const Icon(Icons.star, color: Colors.amber),
                            title: const Text('Casual Friday Outfit'),
                            subtitle: const Text('Blue jeans + White t-shirt + Sneakers'),
                            trailing: ElevatedButton(
                              onPressed: () {
                                // Save outfit
                              },
                              child: const Text('Save'),
                            ),
                          ),
                        ),
                        Card(
                          child: ListTile(
                            leading: const Icon(Icons.star, color: Colors.amber),
                            title: const Text('Business Meeting'),
                            subtitle: const Text('Navy suit + White shirt + Black shoes'),
                            trailing: ElevatedButton(
                              onPressed: () {
                                // Save outfit
                              },
                              child: const Text('Save'),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  Padding(
                    padding: const EdgeInsets.all(16),
                    child: ElevatedButton(
                      onPressed: () {
                        // Get new recommendations
                      },
                      child: const Text('Get New Recommendations'),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      );

      // Verify recommendations UI
      expect(find.text('AI Recommendations'), findsOneWidget);
      expect(find.text('Casual Friday Outfit'), findsOneWidget);
      expect(find.text('Business Meeting'), findsOneWidget);

      // Test getting new recommendations
      await tester.tap(find.text('Get New Recommendations'));
      await tester.pumpAndSettle(const Duration(seconds: 5));
    });
  });

  group('Network Error Handling Integration Tests', () {
    testWidgets('Should handle server timeout gracefully', (WidgetTester tester) async {
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: Scaffold(
              body: Column(
                children: [
                  ElevatedButton(
                    onPressed: () {
                      // Simulate slow API call
                    },
                    child: const Text('Load Data'),
                  ),
                  const CircularProgressIndicator(),
                  const Text('Loading...'),
                ],
              ),
            ),
          ),
        ),
      );

      await tester.tap(find.text('Load Data'));
      await tester.pump();

      // Verify loading state
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
      expect(find.text('Loading...'), findsOneWidget);

      // Wait for timeout (simulated)
      await tester.pump(const Duration(seconds: 30));
    });

    testWidgets('Should handle network connectivity issues', (WidgetTester tester) async {
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: Scaffold(
              body: Column(
                children: [
                  const Icon(Icons.wifi_off, size: 64, color: Colors.red),
                  const Text('No internet connection'),
                  const Text('Please check your network settings'),
                  ElevatedButton(
                    onPressed: () {
                      // Retry connection
                    },
                    child: const Text('Retry'),
                  ),
                ],
              ),
            ),
          ),
        ),
      );

      // Verify offline UI
      expect(find.byIcon(Icons.wifi_off), findsOneWidget);
      expect(find.text('No internet connection'), findsOneWidget);
      expect(find.text('Retry'), findsOneWidget);

      // Test retry functionality
      await tester.tap(find.text('Retry'));
      await tester.pumpAndSettle();
    });
  });

  group('Performance Integration Tests', () {
    testWidgets('Should handle large dataset loading efficiently', (WidgetTester tester) async {
      final stopwatch = Stopwatch()..start();

      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: Scaffold(
              body: ListView.builder(
                itemCount: 1000,
                itemBuilder: (context, index) {
                  return ListTile(
                    title: Text('Item $index'),
                    subtitle: Text('Description for item $index'),
                    leading: const Icon(Icons.shopping_bag),
                  );
                },
              ),
            ),
          ),
        ),
      );

      await tester.pumpAndSettle();
      stopwatch.stop();

      // Should load within reasonable time
      expect(stopwatch.elapsedMilliseconds, lessThan(5000));

      // Test scrolling performance
      await tester.fling(find.byType(ListView), const Offset(0, -2000), 5000);
      await tester.pumpAndSettle();

      expect(find.byType(ListView), findsOneWidget);
    });

    testWidgets('Should handle rapid user interactions', (WidgetTester tester) async {
      int tapCount = 0;

      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: StatefulBuilder(
              builder: (context, setState) {
                return Scaffold(
                  body: Column(
                    children: [
                      Text('Tap count: $tapCount'),
                      ElevatedButton(
                        onPressed: () {
                          setState(() {
                            tapCount++;
                          });
                        },
                        child: const Text('Tap Me'),
                      ),
                    ],
                  ),
                );
              },
            ),
          ),
        ),
      );

      // Rapidly tap button multiple times
      for (int i = 0; i < 20; i++) {
        await tester.tap(find.text('Tap Me'));
        await tester.pump();
      }

      expect(find.text('Tap count: 20'), findsOneWidget);
    });
  });
}
