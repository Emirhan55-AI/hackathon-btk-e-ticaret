import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:aura_app/main.dart' as app;
import 'package:aura_app/features/ecommerce/presentation/screens/product_search_screen.dart';
import 'package:aura_app/features/ecommerce/presentation/screens/product_detail_screen.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('E-Commerce Integration Tests', () {
    testWidgets('Complete product search to detail flow', (WidgetTester tester) async {
      // Start the app
      app.main();
      await tester.pumpAndSettle();

      // Navigate to product search if not already there
      await tester.tap(find.text('Products').first);
      await tester.pumpAndSettle();

      // Verify we're on the search screen
      expect(find.byType(ProductSearchScreen), findsOneWidget);
      expect(find.byType(TextField), findsOneWidget);

      // Enter search query
      await tester.enterText(find.byType(TextField), 'laptop');
      await tester.testTextInput.receiveAction(TextInputAction.search);
      await tester.pumpAndSettle();

      // Wait for search results
      await tester.pump(const Duration(seconds: 2));

      // Verify search results are displayed
      expect(find.text('laptop'), findsOneWidget);

      // Tap on the first product (if any results)
      final productTiles = find.byType(Card);
      if (productTiles.evaluate().isNotEmpty) {
        await tester.tap(productTiles.first);
        await tester.pumpAndSettle();

        // Verify we're on product detail screen
        expect(find.byType(ProductDetailScreen), findsOneWidget);

        // Verify product detail elements
        expect(find.byType(PageView), findsOneWidget); // Image carousel
        expect(find.text('Add to Cart'), findsOneWidget);
        expect(find.byIcon(Icons.favorite_border), findsOneWidget);

        // Test quantity selector
        final addButton = find.byIcon(Icons.add);
        if (addButton.evaluate().isNotEmpty) {
          await tester.tap(addButton);
          await tester.pumpAndSettle();
        }

        // Test favorite toggle
        final favoriteButton = find.byIcon(Icons.favorite_border);
        if (favoriteButton.evaluate().isNotEmpty) {
          await tester.tap(favoriteButton);
          await tester.pumpAndSettle();
          // Should now show filled favorite icon
          expect(find.byIcon(Icons.favorite), findsOneWidget);
        }

        // Test add to cart
        final addToCartButton = find.text('Add to Cart');
        if (addToCartButton.evaluate().isNotEmpty) {
          await tester.tap(addToCartButton);
          await tester.pumpAndSettle();
          // Should show some confirmation (snackbar, dialog, etc.)
        }

        // Navigate back to search
        await tester.pageBack();
        await tester.pumpAndSettle();

        // Verify we're back to search screen
        expect(find.byType(ProductSearchScreen), findsOneWidget);
      }
    });

    testWidgets('Product filtering and sorting flow', (WidgetTester tester) async {
      // Start the app
      app.main();
      await tester.pumpAndSettle();

      // Navigate to product search
      await tester.tap(find.text('Products').first);
      await tester.pumpAndSettle();

      // Test filter functionality
      final filterButton = find.byIcon(Icons.filter_list);
      if (filterButton.evaluate().isNotEmpty) {
        await tester.tap(filterButton);
        await tester.pumpAndSettle();

        // Interact with filter options
        final categoryFilter = find.text('electronics');
        if (categoryFilter.evaluate().isNotEmpty) {
          await tester.tap(categoryFilter);
          await tester.pumpAndSettle();
        }

        // Apply filters
        final applyButton = find.text('Apply');
        if (applyButton.evaluate().isNotEmpty) {
          await tester.tap(applyButton);
          await tester.pumpAndSettle();
        }
      }

      // Test sorting functionality
      final sortButton = find.byIcon(Icons.sort);
      if (sortButton.evaluate().isNotEmpty) {
        await tester.tap(sortButton);
        await tester.pumpAndSettle();

        // Select sort option
        final priceSort = find.text('Price: Low to High');
        if (priceSort.evaluate().isNotEmpty) {
          await tester.tap(priceSort);
          await tester.pumpAndSettle();
        }
      }

      // Test view toggle
      final gridButton = find.byIcon(Icons.grid_view);
      final listButton = find.byIcon(Icons.list);
      
      if (gridButton.evaluate().isNotEmpty) {
        await tester.tap(gridButton);
        await tester.pumpAndSettle();
      }
      
      if (listButton.evaluate().isNotEmpty) {
        await tester.tap(listButton);
        await tester.pumpAndSettle();
      }
    });

    testWidgets('Error handling and retry flow', (WidgetTester tester) async {
      // This test would require network manipulation to simulate errors
      // For now, we'll test the UI elements that should be present
      
      app.main();
      await tester.pumpAndSettle();

      // Navigate to product search
      await tester.tap(find.text('Products').first);
      await tester.pumpAndSettle();

      // Search for something that might not exist
      await tester.enterText(find.byType(TextField), 'nonexistentproduct12345');
      await tester.testTextInput.receiveAction(TextInputAction.search);
      await tester.pumpAndSettle();

      // Wait for potential error or empty state
      await tester.pump(const Duration(seconds: 3));

      // Check for error handling UI elements
      final retryButton = find.text('Retry');
      final errorMessage = find.textContaining('error');
      final noResultsMessage = find.text('No products found');

      // If any error handling UI is present, test it
      if (retryButton.evaluate().isNotEmpty) {
        await tester.tap(retryButton);
        await tester.pumpAndSettle();
      }

      // Verify appropriate empty state or error messages
      expect(
        errorMessage.evaluate().isNotEmpty || 
        noResultsMessage.evaluate().isNotEmpty,
        isTrue,
        reason: 'Should show either error message or no results message'
      );
    });

    testWidgets('Load more products pagination', (WidgetTester tester) async {
      app.main();
      await tester.pumpAndSettle();

      // Navigate to product search
      await tester.tap(find.text('Products').first);
      await tester.pumpAndSettle();

      // Search for products
      await tester.enterText(find.byType(TextField), 'product');
      await tester.testTextInput.receiveAction(TextInputAction.search);
      await tester.pumpAndSettle();

      // Wait for results
      await tester.pump(const Duration(seconds: 2));

      // Try to scroll to trigger load more
      final scrollableWidget = find.byType(Scrollable);
      if (scrollableWidget.evaluate().isNotEmpty) {
        // Scroll down to potentially trigger load more
        await tester.drag(scrollableWidget.first, const Offset(0, -500));
        await tester.pumpAndSettle();

        // Check if load more indicator appears
        expect(
          find.byType(CircularProgressIndicator).evaluate().isNotEmpty ||
          find.text('Load More').evaluate().isNotEmpty,
          isTrue,
          reason: 'Should show load more indicator when scrolling'
        );
      }
    });
  });
}
