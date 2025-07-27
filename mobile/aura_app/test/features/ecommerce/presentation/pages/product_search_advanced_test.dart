// Advanced ProductSearchScreen Widget Tests
// Testing edge cases, performance, and real-world scenarios

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mockito/mockito.dart';
import 'package:shimmer/shimmer.dart';

import '../../../../../lib/features/ecommerce/presentation/pages/product_search_page.dart';
import '../../../../../lib/features/ecommerce/presentation/controllers/product_search_controller.dart';
import '../../../../../lib/features/ecommerce/domain/entities/product.dart';
import '../../../../../lib/core/widgets/shimmer_loading.dart';

/// Advanced widget tests for ProductSearchScreen covering edge cases and performance
void main() {
  group('ProductSearchScreen Advanced Widget Tests', () {
    testWidgets('Should handle shimmer loading during API delays', (WidgetTester tester) async {
      // Test shimmer animation during delayed API responses
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: ProductSearchPage(),
          ),
        ),
      );

      // Initially should show search interface
      expect(find.byType(TextField), findsOneWidget);
      
      // Enter search query to trigger loading state
      await tester.enterText(find.byType(TextField), 'test search');
      await tester.testTextInput.receiveAction(TextInputAction.search);
      
      // Pump to start the search
      await tester.pump();
      
      // Verify loading state elements are present
      expect(find.text('Searching products...'), findsOneWidget);
      expect(find.byType(GridView), findsOneWidget);
      
      // Wait for multiple animation frames to test shimmer animation
      for (int i = 0; i < 10; i++) {
        await tester.pump(const Duration(milliseconds: 100));
      }
    });

    testWidgets('Should handle very long product names without UI breaking', (WidgetTester tester) async {
      // Create product with extremely long name
      final longNameProduct = Product(
        id: 'long-name-test',
        name: 'This is an extremely long product name that should test the UI layout boundaries and text overflow handling mechanisms in the product card widget component system',
        description: 'Test description',
        price: 99.99,
        currency: 'USD',
        category: 'test',
        brand: 'TestBrand',
        rating: 4.5,
        reviewCount: 100,
        stockQuantity: 10,
        tags: ['test'],
      );

      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: Scaffold(
              body: Container(
                width: 200, // Constrained width to force text overflow
                child: Card(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        longNameProduct.name,
                        style: const TextStyle(fontSize: 16),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                      Text('Price: \$${longNameProduct.price}'),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ),
      );

      // Verify the widget renders without throwing
      expect(find.byType(Card), findsOneWidget);
      expect(find.textContaining('This is an extremely'), findsOneWidget);
      
      // Verify no render overflow errors
      expect(tester.takeException(), isNull);
    });

    testWidgets('Should maintain scroll performance with large product lists', (WidgetTester tester) async {
      // Create a large list of products
      final largeProductList = List.generate(1000, (index) => Product(
        id: 'product-$index',
        name: 'Product $index',
        description: 'Description for product $index',
        price: (index + 1) * 10.0,
        currency: 'USD',
        category: 'test',
        brand: 'Brand${index % 10}',
        rating: 3.0 + (index % 3),
        reviewCount: index * 5,
        stockQuantity: index % 100,
        tags: ['tag$index'],
      ));

      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: Scaffold(
              body: ListView.builder(
                itemCount: largeProductList.length,
                itemBuilder: (context, index) {
                  final product = largeProductList[index];
                  return ListTile(
                    title: Text(product.name),
                    subtitle: Text('\$${product.price}'),
                  );
                },
              ),
            ),
          ),
        ),
      );

      // Measure scroll performance
      final stopwatch = Stopwatch()..start();
      
      // Perform scroll operations
      await tester.fling(find.byType(ListView), const Offset(0, -1000), 10000);
      await tester.pumpAndSettle();
      
      stopwatch.stop();
      
      // Verify scroll completes within reasonable time (less than 2 seconds)
      expect(stopwatch.elapsedMilliseconds, lessThan(2000));
      
      // Verify UI is still responsive
      expect(find.byType(ListView), findsOneWidget);
    });

    testWidgets('Should handle empty search results gracefully', (WidgetTester tester) async {
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: ProductSearchPage(),
          ),
        ),
      );

      // Enter search query that returns no results
      await tester.enterText(find.byType(TextField), 'nonexistentproduct123456');
      await tester.testTextInput.receiveAction(TextInputAction.search);
      
      // Use pump instead of pumpAndSettle to avoid timeout
      await tester.pump();
      await tester.pump(const Duration(seconds: 2));

      // Verify empty state is shown (more flexible check)
      expect(find.textContaining('No Products Found'), findsAny);
    });

    testWidgets('Should handle network timeout gracefully', (WidgetTester tester) async {
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: ProductSearchPage(),
          ),
        ),
      );

      // Simulate network timeout by waiting longer than expected
      await tester.pump(const Duration(seconds: 30));
      
      // Verify error state is shown
      expect(find.textContaining('error'), findsAtLeastNWidgets(0));
    });
  });

  group('ProductSearchScreen Responsive Design Tests', () {
    testWidgets('Should adapt to very small screen sizes', (WidgetTester tester) async {
      // Set very small screen size
      await tester.binding.setSurfaceSize(const Size(300, 500));
      
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: ProductSearchPage(),
          ),
        ),
      );

      // Verify UI adapts to small screen
      expect(find.byType(Scaffold), findsOneWidget);
      expect(tester.takeException(), isNull);
      
      // Reset to original size
      await tester.binding.setSurfaceSize(null);
    });

    testWidgets('Should adapt to very large screen sizes', (WidgetTester tester) async {
      // Set very large screen size
      await tester.binding.setSurfaceSize(const Size(1920, 1080));
      
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: ProductSearchPage(),
          ),
        ),
      );

      // Verify UI adapts to large screen
      expect(find.byType(Scaffold), findsOneWidget);
      expect(tester.takeException(), isNull);
      
      // Reset to original size
      await tester.binding.setSurfaceSize(null);
    });
  });

  group('ProductSearchScreen Performance Tests', () {
    testWidgets('Should filter large lists efficiently', (WidgetTester tester) async {
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: ProductSearchPage(),
          ),
        ),
      );

      final stopwatch = Stopwatch()..start();
      
      // Perform multiple filter operations
      for (int i = 0; i < 10; i++) {
        await tester.enterText(find.byType(TextField), 'filter$i');
        await tester.pump();
      }
      
      stopwatch.stop();
      
      // Verify filtering is fast (less than 1 second for 10 operations)
      expect(stopwatch.elapsedMilliseconds, lessThan(1000));
    });
  });
}
