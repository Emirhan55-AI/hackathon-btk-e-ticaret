import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'core/utils/logger.dart';

/// Bootstrap the application
/// This function initializes all necessary components before running the app
Future<void> bootstrap() async {
  final logger = Logger('Bootstrap');
  
  try {
    logger.info('Starting app bootstrap...');
    
    // Ensure Flutter binding is initialized
    WidgetsFlutterBinding.ensureInitialized();

    // Set system UI overlay style for consistent look across platforms
    SystemChrome.setSystemUIOverlayStyle(
      const SystemUiOverlayStyle(
        statusBarColor: Colors.transparent,
        statusBarIconBrightness: Brightness.dark,
        systemNavigationBarColor: Colors.white,
        systemNavigationBarIconBrightness: Brightness.dark,
      ),
    );

    // Set preferred orientations to portrait only
    await SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
      DeviceOrientation.portraitDown,
    ]);

    // Initialize database (disabled for web compatibility)
    logger.info('Skipping database initialization for web compatibility...');
    // await DatabaseService.initialize();
    logger.info('Database initialization skipped');

    // Initialize secure storage if needed
    // This ensures the storage is ready before the app starts
    logger.info('Bootstrap completed successfully');
    
  } catch (e, stackTrace) {
    logger.error('Bootstrap failed', e, stackTrace);
    // Don't rethrow - allow app to start even if some initialization fails
    debugPrint('Bootstrap error: ${e.toString()}');
  }
}

/// Provider wrapper to initialize Riverpod
class ProviderWrapper extends StatelessWidget {
  final Widget child;
  
  const ProviderWrapper({
    super.key,
    required this.child,
  });

  @override
  Widget build(BuildContext context) {
    return ProviderScope(
      child: child,
    );
  }
}
