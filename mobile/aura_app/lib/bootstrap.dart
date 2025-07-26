import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'core/constants/app_colors.dart';

/// Bootstrap the application
Future<void> bootstrap() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Set system UI overlay style
  SystemChrome.setSystemUIOverlayStyle(
    const SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.dark,
      systemNavigationBarColor: AppColors.surface,
      systemNavigationBarIconBrightness: Brightness.dark,
    ),
  );

  // Set preferred orientations
  await SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);
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
