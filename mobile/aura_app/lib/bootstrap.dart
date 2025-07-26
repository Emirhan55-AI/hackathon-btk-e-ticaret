import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// Bootstrap the application
/// This function initializes all necessary components before running the app
Future<void> bootstrap() async {
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

  // Initialize secure storage if needed
  // This ensures the storage is ready before the app starts
  try {
    // Any additional initialization can be added here
    // For example: await SecureStorage.initialize();
  } catch (e) {
    // Log error but don't block app startup
    debugPrint('Bootstrap warning: ${e.toString()}');
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
