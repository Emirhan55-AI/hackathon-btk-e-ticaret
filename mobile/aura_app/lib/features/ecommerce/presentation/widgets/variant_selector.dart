import 'package:flutter/material.dart';

/// Variant selector widget for product options
class VariantSelector extends StatelessWidget {
  final String variantType;
  final List<String> options;
  final String? selectedOption;
  final Function(String) onOptionSelected;
  final bool enabled;

  const VariantSelector({
    super.key,
    required this.variantType,
    required this.options,
    required this.onOptionSelected,
    this.selectedOption,
    this.enabled = true,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          variantType,
          style: theme.textTheme.titleMedium?.copyWith(
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 12),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          children: options.map((option) => _buildOptionChip(
            context: context,
            option: option,
            isSelected: option == selectedOption,
            onSelected: enabled ? () => onOptionSelected(option) : null,
          )).toList(),
        ),
      ],
    );
  }

  Widget _buildOptionChip({
    required BuildContext context,
    required String option,
    required bool isSelected,
    required VoidCallback? onSelected,
  }) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return FilterChip(
      label: Text(option),
      selected: isSelected,
      onSelected: onSelected != null ? (_) => onSelected() : null,
      backgroundColor: colorScheme.surface,
      selectedColor: colorScheme.primaryContainer,
      checkmarkColor: colorScheme.onPrimaryContainer,
      labelStyle: TextStyle(
        color: isSelected 
            ? colorScheme.onPrimaryContainer 
            : colorScheme.onSurface,
        fontWeight: isSelected ? FontWeight.w600 : FontWeight.normal,
      ),
    );
  }
}

/// Color variant selector with color swatches
class ColorVariantSelector extends StatelessWidget {
  final List<ColorVariant> colors;
  final String? selectedColor;
  final Function(String) onColorSelected;
  final bool enabled;

  const ColorVariantSelector({
    super.key,
    required this.colors,
    required this.onColorSelected,
    this.selectedColor,
    this.enabled = true,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Color',
          style: theme.textTheme.titleMedium?.copyWith(
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 12),
        Wrap(
          spacing: 12,
          runSpacing: 12,
          children: colors.map((colorVariant) => _buildColorOption(
            context: context,
            colorVariant: colorVariant,
            isSelected: colorVariant.name == selectedColor,
            onSelected: enabled 
                ? () => onColorSelected(colorVariant.name) 
                : null,
          )).toList(),
        ),
      ],
    );
  }

  Widget _buildColorOption({
    required BuildContext context,
    required ColorVariant colorVariant,
    required bool isSelected,
    required VoidCallback? onSelected,
  }) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return GestureDetector(
      onTap: onSelected,
      child: Column(
        children: [
          Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
              color: colorVariant.color,
              shape: BoxShape.circle,
              border: Border.all(
                color: isSelected 
                    ? colorScheme.primary 
                    : colorScheme.outline,
                width: isSelected ? 3 : 1,
              ),
            ),
            child: isSelected
                ? Icon(
                    Icons.check,
                    color: _getContrastColor(colorVariant.color),
                    size: 20,
                  )
                : null,
          ),
          const SizedBox(height: 4),
          Text(
            colorVariant.name,
            style: theme.textTheme.bodySmall?.copyWith(
              fontWeight: isSelected ? FontWeight.w600 : FontWeight.normal,
            ),
          ),
        ],
      ),
    );
  }

  Color _getContrastColor(Color color) {
    // Calculate luminance to determine if white or black text should be used
    final luminance = (0.299 * color.red + 0.587 * color.green + 0.114 * color.blue) / 255;
    return luminance > 0.5 ? Colors.black : Colors.white;
  }
}

/// Size variant selector with size badges
class SizeVariantSelector extends StatelessWidget {
  final List<String> sizes;
  final String? selectedSize;
  final Function(String) onSizeSelected;
  final bool enabled;

  const SizeVariantSelector({
    super.key,
    required this.sizes,
    required this.onSizeSelected,
    this.selectedSize,
    this.enabled = true,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Size',
          style: theme.textTheme.titleMedium?.copyWith(
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 12),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          children: sizes.map((size) => _buildSizeOption(
            context: context,
            size: size,
            isSelected: size == selectedSize,
            onSelected: enabled ? () => onSizeSelected(size) : null,
          )).toList(),
        ),
      ],
    );
  }

  Widget _buildSizeOption({
    required BuildContext context,
    required String size,
    required bool isSelected,
    required VoidCallback? onSelected,
  }) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return GestureDetector(
      onTap: onSelected,
      child: Container(
        width: 48,
        height: 48,
        decoration: BoxDecoration(
          color: isSelected 
              ? colorScheme.primary 
              : colorScheme.surface,
          border: Border.all(
            color: isSelected 
                ? colorScheme.primary 
                : colorScheme.outline,
          ),
          borderRadius: BorderRadius.circular(8),
        ),
        child: Center(
          child: Text(
            size,
            style: theme.textTheme.titleMedium?.copyWith(
              color: isSelected 
                  ? colorScheme.onPrimary 
                  : colorScheme.onSurface,
              fontWeight: FontWeight.w600,
            ),
          ),
        ),
      ),
    );
  }
}

/// Data model for color variants
class ColorVariant {
  final String name;
  final Color color;

  const ColorVariant({
    required this.name,
    required this.color,
  });
}

/// Multi-variant selector for complex product options
class MultiVariantSelector extends StatelessWidget {
  final Map<String, List<String>> variants;
  final Map<String, String> selectedVariants;
  final Function(String variantType, String option) onVariantSelected;
  final bool enabled;

  const MultiVariantSelector({
    super.key,
    required this.variants,
    required this.selectedVariants,
    required this.onVariantSelected,
    this.enabled = true,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: variants.entries.map((entry) {
        final variantType = entry.key;
        final options = entry.value;
        
        return Padding(
          padding: const EdgeInsets.only(bottom: 24),
          child: VariantSelector(
            variantType: variantType,
            options: options,
            selectedOption: selectedVariants[variantType],
            onOptionSelected: (option) => onVariantSelected(variantType, option),
            enabled: enabled,
          ),
        );
      }).toList(),
    );
  }
}
