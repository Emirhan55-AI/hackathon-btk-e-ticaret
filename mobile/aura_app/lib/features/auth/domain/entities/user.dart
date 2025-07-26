/// User entity representing a user in the system
class User {
  final String id;
  final String email;
  final String? firstName;
  final String? lastName;
  final String? profileImage;
  final DateTime? dateOfBirth;
  final String? gender;
  final Map<String, dynamic>? preferences;
  final bool isEmailVerified;
  final DateTime createdAt;
  final DateTime updatedAt;

  const User({
    required this.id,
    required this.email,
    this.firstName,
    this.lastName,
    this.profileImage,
    this.dateOfBirth,
    this.gender,
    this.preferences,
    this.isEmailVerified = false,
    required this.createdAt,
    required this.updatedAt,
  });

  /// Get user's full name
  String get fullName {
    if (firstName != null && lastName != null) {
      return '$firstName $lastName';
    } else if (firstName != null) {
      return firstName!;
    } else if (lastName != null) {
      return lastName!;
    } else {
      return email.split('@').first;
    }
  }

  /// Get user's display name (first name or email prefix)
  String get displayName {
    return firstName ?? email.split('@').first;
  }

  /// Check if user profile is complete
  bool get isProfileComplete {
    return firstName != null && 
           lastName != null && 
           dateOfBirth != null && 
           gender != null;
  }

  /// Create a copy of user with updated fields
  User copyWith({
    String? id,
    String? email,
    String? firstName,
    String? lastName,
    String? profileImage,
    DateTime? dateOfBirth,
    String? gender,
    Map<String, dynamic>? preferences,
    bool? isEmailVerified,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return User(
      id: id ?? this.id,
      email: email ?? this.email,
      firstName: firstName ?? this.firstName,
      lastName: lastName ?? this.lastName,
      profileImage: profileImage ?? this.profileImage,
      dateOfBirth: dateOfBirth ?? this.dateOfBirth,
      gender: gender ?? this.gender,
      preferences: preferences ?? this.preferences,
      isEmailVerified: isEmailVerified ?? this.isEmailVerified,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }

  /// Convert to JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'first_name': firstName,
      'last_name': lastName,
      'profile_image': profileImage,
      'date_of_birth': dateOfBirth?.toIso8601String(),
      'gender': gender,
      'preferences': preferences,
      'is_email_verified': isEmailVerified,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }

  /// Create from JSON
  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id']?.toString() ?? '',
      email: json['email']?.toString() ?? '',
      firstName: json['first_name']?.toString(),
      lastName: json['last_name']?.toString(),
      profileImage: json['profile_image']?.toString(),
      dateOfBirth: json['date_of_birth'] != null 
          ? DateTime.tryParse(json['date_of_birth'].toString())
          : null,
      gender: json['gender']?.toString(),
      preferences: json['preferences'] as Map<String, dynamic>?,
      isEmailVerified: json['is_email_verified'] == true,
      createdAt: DateTime.tryParse(json['created_at']?.toString() ?? '') ?? DateTime.now(),
      updatedAt: DateTime.tryParse(json['updated_at']?.toString() ?? '') ?? DateTime.now(),
    );
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is User && other.id == id;
  }

  @override
  int get hashCode => id.hashCode;

  @override
  String toString() {
    return 'User(id: $id, email: $email, fullName: $fullName)';
  }
}
