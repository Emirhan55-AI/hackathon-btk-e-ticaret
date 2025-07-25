/// Form validation utilities
class FormValidators {
  FormValidators._();

  /// Email validation
  static String? validateEmail(String? value) {
    if (value == null || value.trim().isEmpty) {
      return 'Email is required';
    }
    
    final emailRegex = RegExp(
      r'^[a-zA-Z0-9.!#$%&*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
    );
    
    if (!emailRegex.hasMatch(value.trim())) {
      return 'Please enter a valid email address';
    }
    
    return null;
  }

  /// Password validation
  static String? validatePassword(String? value) {
    if (value == null || value.isEmpty) {
      return 'Password is required';
    }
    
    if (value.length < 6) {
      return 'Password must be at least 6 characters long';
    }
    
    // Check for at least one letter and one number
    if (!RegExp(r'^(?=.*[A-Za-z])(?=.*\d)').hasMatch(value)) {
      return 'Password must contain at least one letter and one number';
    }
    
    return null;
  }

  /// Confirm password validation
  static String? validateConfirmPassword(String? value, String? password) {
    if (value == null || value.isEmpty) {
      return 'Please confirm your password';
    }
    
    if (value != password) {
      return 'Passwords do not match';
    }
    
    return null;
  }

  /// Name validation
  static String? validateName(String? value, {String fieldName = 'Name'}) {
    if (value == null || value.trim().isEmpty) {
      return '$fieldName is required';
    }
    
    if (value.trim().length < 2) {
      return '$fieldName must be at least 2 characters long';
    }
    
    if (value.trim().length > 50) {
      return '$fieldName cannot exceed 50 characters';
    }
    
    // Only letters, spaces, hyphens, and apostrophes
    if (!RegExp(r'^[a-zA-Z\s\-]+$').hasMatch(value.trim())) {
      return '$fieldName can only contain letters, spaces, and hyphens';
    }
    
    return null;
  }

  /// Phone number validation
  static String? validatePhone(String? value) {
    if (value == null || value.trim().isEmpty) {
      return null; // Phone is optional
    }
    
    // Remove all non-digit characters
    final digitsOnly = value.replaceAll(RegExp(r'\D'), '');
    
    if (digitsOnly.length < 10) {
      return 'Phone number must be at least 10 digits';
    }
    
    if (digitsOnly.length > 15) {
      return 'Phone number cannot exceed 15 digits';
    }
    
    return null;
  }

  /// Required field validation
  static String? validateRequired(String? value, {String fieldName = 'Field'}) {
    if (value == null || value.trim().isEmpty) {
      return '$fieldName is required';
    }
    return null;
  }

  /// Age validation (for date of birth)
  static String? validateAge(DateTime? dateOfBirth, {int minAge = 13, int maxAge = 120}) {
    if (dateOfBirth == null) {
      return null; // Optional field
    }
    
    final now = DateTime.now();
    final age = now.year - dateOfBirth.year;
    
    if (dateOfBirth.isAfter(now)) {
      return 'Date of birth cannot be in the future';
    }
    
    if (age < minAge) {
      return 'You must be at least $minAge years old';
    }
    
    if (age > maxAge) {
      return 'Please enter a valid date of birth';
    }
    
    return null;
  }

  /// URL validation
  static String? validateUrl(String? value) {
    if (value == null || value.trim().isEmpty) {
      return null; // URL is optional
    }
    
    try {
      final uri = Uri.parse(value);
      if (!uri.hasScheme || (!uri.scheme.startsWith('http') && !uri.scheme.startsWith('https'))) {
        return 'Please enter a valid URL';
      }
      return null;
    } catch (e) {
      return 'Please enter a valid URL';
    }
  }

  /// Generic length validation
  static String? validateLength(
    String? value, {
    int? minLength,
    int? maxLength,
    String fieldName = 'Field',
  }) {
    if (value == null || value.trim().isEmpty) {
      return null; // Let required validation handle empty values
    }
    
    final trimmedValue = value.trim();
    
    if (minLength != null && trimmedValue.length < minLength) {
      return '$fieldName must be at least $minLength characters long';
    }
    
    if (maxLength != null && trimmedValue.length > maxLength) {
      return '$fieldName cannot exceed $maxLength characters';
    }
    
    return null;
  }

  /// Combine multiple validators
  static String? combineValidators(String? value, List<String? Function(String?)> validators) {
    for (final validator in validators) {
      final result = validator(value);
      if (result != null) {
        return result;
      }
    }
    return null;
  }
}
