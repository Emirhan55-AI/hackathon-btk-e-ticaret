import 'package:flutter/material.dart';

/// Quantity selector widget for product detail
class QuantitySelector extends StatelessWidget {
  final int quantity;
  final int maxQuantity;
  final int minQuantity;
  final Function(int) onQuantityChanged;
  final bool enabled;

  const QuantitySelector({
    super.key,
    required this.quantity,
    required this.onQuantityChanged,
    this.maxQuantity = 999,
    this.minQuantity = 1,
    this.enabled = true,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Container(
      decoration: BoxDecoration(
        border: Border.all(color: colorScheme.outline),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Decrease button
          _buildButton(
            context: context,
            icon: Icons.remove,
            onPressed: enabled && quantity > minQuantity
                ? () => onQuantityChanged(quantity - 1)
                : null,
          ),
          
          // Quantity display
          Container(
            constraints: const BoxConstraints(minWidth: 60),
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            child: Text(
              quantity.toString(),
              textAlign: TextAlign.center,
              style: theme.textTheme.titleMedium?.copyWith(
                fontWeight: FontWeight.w600,
                color: enabled ? null : colorScheme.onSurface.withOpacity(0.38),
              ),
            ),
          ),
          
          // Increase button
          _buildButton(
            context: context,
            icon: Icons.add,
            onPressed: enabled && quantity < maxQuantity
                ? () => onQuantityChanged(quantity + 1)
                : null,
          ),
        ],
      ),
    );
  }

  Widget _buildButton({
    required BuildContext context,
    required IconData icon,
    required VoidCallback? onPressed,
  }) {
    final colorScheme = Theme.of(context).colorScheme;
    
    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: onPressed,
        borderRadius: BorderRadius.circular(6),
        child: Container(
          padding: const EdgeInsets.all(8),
          child: Icon(
            icon,
            size: 20,
            color: onPressed != null 
                ? colorScheme.onSurface 
                : colorScheme.onSurface.withOpacity(0.38),
          ),
        ),
      ),
    );
  }
}

/// Quantity selector with label
class LabeledQuantitySelector extends StatelessWidget {
  final String label;
  final int quantity;
  final int maxQuantity;
  final int minQuantity;
  final Function(int) onQuantityChanged;
  final bool enabled;
  final String? subtitle;

  const LabeledQuantitySelector({
    super.key,
    required this.label,
    required this.quantity,
    required this.onQuantityChanged,
    this.maxQuantity = 999,
    this.minQuantity = 1,
    this.enabled = true,
    this.subtitle,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: theme.textTheme.titleMedium?.copyWith(
            fontWeight: FontWeight.w600,
          ),
        ),
        if (subtitle != null) ...[
          const SizedBox(height: 4),
          Text(
            subtitle!,
            style: theme.textTheme.bodyMedium?.copyWith(
              color: theme.colorScheme.onSurface.withOpacity(0.7),
            ),
          ),
        ],
        const SizedBox(height: 12),
        Row(
          children: [
            QuantitySelector(
              quantity: quantity,
              maxQuantity: maxQuantity,
              minQuantity: minQuantity,
              onQuantityChanged: onQuantityChanged,
              enabled: enabled,
            ),
            const SizedBox(width: 16),
            if (maxQuantity < 999) // Show stock info if limited
              Text(
                '($maxQuantity available)',
                style: theme.textTheme.bodySmall?.copyWith(
                  color: theme.colorScheme.onSurface.withOpacity(0.6),
                ),
              ),
          ],
        ),
      ],
    );
  }
}

/// Compact quantity selector for cart items
class CompactQuantitySelector extends StatelessWidget {
  final int quantity;
  final int maxQuantity;
  final Function(int) onQuantityChanged;
  final bool enabled;

  const CompactQuantitySelector({
    super.key,
    required this.quantity,
    required this.onQuantityChanged,
    this.maxQuantity = 999,
    this.enabled = true,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Container(
      decoration: BoxDecoration(
        color: colorScheme.surfaceContainerHighest,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Decrease button
          _buildCompactButton(
            context: context,
            icon: Icons.remove,
            onPressed: enabled && quantity > 1
                ? () => onQuantityChanged(quantity - 1)
                : null,
          ),
          
          // Quantity display
          Container(
            constraints: const BoxConstraints(minWidth: 32),
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
            child: Text(
              quantity.toString(),
              textAlign: TextAlign.center,
              style: theme.textTheme.bodyMedium?.copyWith(
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
          
          // Increase button
          _buildCompactButton(
            context: context,
            icon: Icons.add,
            onPressed: enabled && quantity < maxQuantity
                ? () => onQuantityChanged(quantity + 1)
                : null,
          ),
        ],
      ),
    );
  }

  Widget _buildCompactButton({
    required BuildContext context,
    required IconData icon,
    required VoidCallback? onPressed,
  }) {
    final colorScheme = Theme.of(context).colorScheme;
    
    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: onPressed,
        borderRadius: BorderRadius.circular(16),
        child: Container(
          padding: const EdgeInsets.all(6),
          child: Icon(
            icon,
            size: 16,
            color: onPressed != null 
                ? colorScheme.onSurface 
                : colorScheme.onSurface.withOpacity(0.38),
          ),
        ),
      ),
    );
  }
}
