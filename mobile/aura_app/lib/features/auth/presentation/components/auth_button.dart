import 'package:flutter/material.dart';

/// Custom button for authentication actions
class AuthButton extends StatelessWidget {
  final VoidCallback? onPressed;
  final Widget child;
  final bool isLoading;
  final bool isSecondary;
  final EdgeInsetsGeometry? padding;
  final Size? minimumSize;
  final Color? backgroundColor;
  final Color? foregroundColor;
  final double? elevation;

  const AuthButton({
    super.key,
    required this.onPressed,
    required this.child,
    this.isLoading = false,
    this.isSecondary = false,
    this.padding,
    this.minimumSize,
    this.backgroundColor,
    this.foregroundColor,
    this.elevation,
  });

  /// Secondary button constructor
  const AuthButton.secondary({
    super.key,
    required this.onPressed,
    required this.child,
    this.isLoading = false,
    this.padding,
    this.minimumSize,
    this.backgroundColor,
    this.foregroundColor,
    this.elevation,
  }) : isSecondary = true;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDisabled = onPressed == null || isLoading;

    if (isSecondary) {
      return OutlinedButton(
        onPressed: isDisabled ? null : onPressed,
        style: OutlinedButton.styleFrom(
          padding: padding ?? const EdgeInsets.symmetric(vertical: 16),
          minimumSize: minimumSize ?? const Size(double.infinity, 56),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          side: BorderSide(
            color: isDisabled
                ? theme.colorScheme.outline.withOpacity(0.3)
                : (foregroundColor ?? theme.colorScheme.primary),
            width: 1.5,
          ),
          foregroundColor: isDisabled
              ? theme.colorScheme.onSurface.withOpacity(0.38)
              : (foregroundColor ?? theme.colorScheme.primary),
          elevation: elevation,
        ),
        child: _buildChild(context, theme),
      );
    }

    return ElevatedButton(
      onPressed: isDisabled ? null : onPressed,
      style: ElevatedButton.styleFrom(
        padding: padding ?? const EdgeInsets.symmetric(vertical: 16),
        minimumSize: minimumSize ?? const Size(double.infinity, 56),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
        backgroundColor: isDisabled
            ? theme.colorScheme.surfaceVariant
            : (backgroundColor ?? theme.colorScheme.primary),
        foregroundColor: isDisabled
            ? theme.colorScheme.onSurface.withOpacity(0.38)
            : (foregroundColor ?? theme.colorScheme.onPrimary),
        elevation: elevation ?? (isDisabled ? 0 : 2),
        shadowColor: theme.colorScheme.shadow.withOpacity(0.2),
      ),
      child: _buildChild(context, theme),
    );
  }

  Widget _buildChild(BuildContext context, ThemeData theme) {
    if (isLoading) {
      return Row(
        mainAxisAlignment: MainAxisAlignment.center,
        mainAxisSize: MainAxisSize.min,
        children: [
          SizedBox(
            width: 20,
            height: 20,
            child: CircularProgressIndicator(
              strokeWidth: 2.5,
              valueColor: AlwaysStoppedAnimation<Color>(
                isSecondary
                    ? theme.colorScheme.primary
                    : theme.colorScheme.onPrimary,
              ),
            ),
          ),
          const SizedBox(width: 12),
          Text(
            'Loading...',
            style: theme.textTheme.labelLarge?.copyWith(
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      );
    }

    if (child is Text) {
      return DefaultTextStyle(
        style: theme.textTheme.labelLarge?.copyWith(
              fontWeight: FontWeight.w600,
            ) ??
            const TextStyle(),
        child: child,
      );
    }

    return child;
  }
}

/// Icon button variant for auth actions
class AuthIconButton extends StatelessWidget {
  final VoidCallback? onPressed;
  final IconData icon;
  final String? label;
  final bool isLoading;
  final Color? backgroundColor;
  final Color? foregroundColor;

  const AuthIconButton({
    super.key,
    required this.onPressed,
    required this.icon,
    this.label,
    this.isLoading = false,
    this.backgroundColor,
    this.foregroundColor,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDisabled = onPressed == null || isLoading;

    return OutlinedButton(
      onPressed: isDisabled ? null : onPressed,
      style: OutlinedButton.styleFrom(
        padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 24),
        minimumSize: const Size(double.infinity, 56),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
        side: BorderSide(
          color: theme.colorScheme.outline.withOpacity(0.3),
          width: 1,
        ),
        backgroundColor: backgroundColor ?? Colors.transparent,
        foregroundColor: foregroundColor ?? theme.colorScheme.onSurface,
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          if (isLoading)
            SizedBox(
              width: 20,
              height: 20,
              child: CircularProgressIndicator(
                strokeWidth: 2.5,
                valueColor: AlwaysStoppedAnimation<Color>(
                  theme.colorScheme.primary,
                ),
              ),
            )
          else
            Icon(icon, size: 20),
          if (label != null) ...[
            const SizedBox(width: 12),
            Text(
              label!,
              style: theme.textTheme.labelLarge?.copyWith(
                fontWeight: FontWeight.w500,
              ),
            ),
          ],
        ],
      ),
    );
  }
}
