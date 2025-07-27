import 'package:flutter/material.dart';

/// Custom rating bar widget to display star ratings
class CustomRatingBar extends StatelessWidget {
  final double rating;
  final int maxRating;
  final double size;
  final Color? activeColor;
  final Color? inactiveColor;
  final bool allowHalfRating;
  final Function(double)? onRatingUpdate;

  const CustomRatingBar({
    super.key,
    required this.rating,
    this.maxRating = 5,
    this.size = 20,
    this.activeColor,
    this.inactiveColor,
    this.allowHalfRating = true,
    this.onRatingUpdate,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final activeStarColor = activeColor ?? Colors.amber;
    final inactiveStarColor = inactiveColor ?? Colors.grey[300]!;

    return Row(
      mainAxisSize: MainAxisSize.min,
      children: List.generate(maxRating, (index) {
        final starValue = index + 1;
        final isActive = rating >= starValue;
        final isHalfActive = allowHalfRating && 
            rating > index && rating < starValue;

        return GestureDetector(
          onTap: onRatingUpdate != null 
              ? () => onRatingUpdate!(starValue.toDouble())
              : null,
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 1),
            child: _buildStar(
              isActive: isActive,
              isHalfActive: isHalfActive,
              activeColor: activeStarColor,
              inactiveColor: inactiveStarColor,
            ),
          ),
        );
      }),
    );
  }

  Widget _buildStar({
    required bool isActive,
    required bool isHalfActive,
    required Color activeColor,
    required Color inactiveColor,
  }) {
    if (isActive) {
      return Icon(
        Icons.star,
        size: size,
        color: activeColor,
      );
    } else if (isHalfActive) {
      return Stack(
        children: [
          Icon(
            Icons.star,
            size: size,
            color: inactiveColor,
          ),
          ClipRect(
            clipper: _HalfStarClipper(),
            child: Icon(
              Icons.star,
              size: size,
              color: activeColor,
            ),
          ),
        ],
      );
    } else {
      return Icon(
        Icons.star_border,
        size: size,
        color: inactiveColor,
      );
    }
  }
}

/// Clipper to show half star
class _HalfStarClipper extends CustomClipper<Rect> {
  @override
  Rect getClip(Size size) {
    return Rect.fromLTWH(0, 0, size.width / 2, size.height);
  }

  @override
  bool shouldReclip(CustomClipper<Rect> oldClipper) => false;
}

/// Read-only rating display widget
class RatingDisplay extends StatelessWidget {
  final double rating;
  final int reviewCount;
  final double starSize;
  final TextStyle? textStyle;
  final bool showReviewCount;

  const RatingDisplay({
    super.key,
    required this.rating,
    this.reviewCount = 0,
    this.starSize = 16,
    this.textStyle,
    this.showReviewCount = true,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        CustomRatingBar(
          rating: rating,
          size: starSize,
          allowHalfRating: true,
        ),
        if (showReviewCount) ...[
          const SizedBox(width: 4),
          Text(
            '($reviewCount)',
            style: textStyle ?? theme.textTheme.bodySmall?.copyWith(
              color: theme.colorScheme.onSurfaceVariant,
            ),
          ),
        ],
      ],
    );
  }
}

/// Interactive rating input widget
class RatingInput extends StatefulWidget {
  final double initialRating;
  final Function(double) onRatingChanged;
  final int maxRating;
  final double starSize;
  final String? label;

  const RatingInput({
    super.key,
    this.initialRating = 0,
    required this.onRatingChanged,
    this.maxRating = 5,
    this.starSize = 30,
    this.label,
  });

  @override
  State<RatingInput> createState() => _RatingInputState();
}

class _RatingInputState extends State<RatingInput> {
  late double _currentRating;

  @override
  void initState() {
    super.initState();
    _currentRating = widget.initialRating;
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (widget.label != null) ...[
          Text(
            widget.label!,
            style: theme.textTheme.titleMedium,
          ),
          const SizedBox(height: 8),
        ],
        Row(
          children: [
            CustomRatingBar(
              rating: _currentRating,
              maxRating: widget.maxRating,
              size: widget.starSize,
              allowHalfRating: false,
              onRatingUpdate: (rating) {
                setState(() {
                  _currentRating = rating;
                });
                widget.onRatingChanged(rating);
              },
            ),
            const SizedBox(width: 12),
            Text(
              _currentRating.toStringAsFixed(0),
              style: theme.textTheme.titleMedium?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
      ],
    );
  }
}
