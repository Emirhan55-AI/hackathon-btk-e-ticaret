import 'package:flutter/material.dart';
import 'bootstrap.dart';
import 'core/constants/app_constants.dart';
import 'core/theme/app_theme.dart';
import 'features/auth/presentation/pages/splash_screen.dart';

void main() async {
  // Initialize the app
  await bootstrap();
  
  // Run the app
  runApp(
    const ProviderWrapper(
      child: AuraApp(),
    ),
  );
}

class AuraApp extends StatelessWidget {
  const AuraApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: AppConstants.appName,
      theme: AppTheme.lightTheme,
      debugShowCheckedModeBanner: false,
      home: const SplashScreen(),
    );
  }
}
