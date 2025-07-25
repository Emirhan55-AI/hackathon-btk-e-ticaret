/// Authentication token entity
class AuthToken {
  final String accessToken;
  final String refreshToken;
  final String tokenType;
  final DateTime expiresAt;
  final List<String> scopes;

  const AuthToken({
    required this.accessToken,
    required this.refreshToken,
    this.tokenType = 'Bearer',
    required this.expiresAt,
    this.scopes = const [],
  });

  /// Check if token is expired
  bool get isExpired {
    return DateTime.now().isAfter(expiresAt);
  }

  /// Check if token is about to expire (within 5 minutes)
  bool get isAboutToExpire {
    return DateTime.now().add(const Duration(minutes: 5)).isAfter(expiresAt);
  }

  /// Get authorization header value
  String get authorizationHeader {
    return '$tokenType $accessToken';
  }

  /// Time remaining until expiration
  Duration get timeUntilExpiration {
    return expiresAt.difference(DateTime.now());
  }

  /// Create a copy with updated fields
  AuthToken copyWith({
    String? accessToken,
    String? refreshToken,
    String? tokenType,
    DateTime? expiresAt,
    List<String>? scopes,
  }) {
    return AuthToken(
      accessToken: accessToken ?? this.accessToken,
      refreshToken: refreshToken ?? this.refreshToken,
      tokenType: tokenType ?? this.tokenType,
      expiresAt: expiresAt ?? this.expiresAt,
      scopes: scopes ?? this.scopes,
    );
  }

  /// Convert to JSON
  Map<String, dynamic> toJson() {
    return {
      'access_token': accessToken,
      'refresh_token': refreshToken,
      'token_type': tokenType,
      'expires_at': expiresAt.toIso8601String(),
      'scopes': scopes,
    };
  }

  /// Create from JSON
  factory AuthToken.fromJson(Map<String, dynamic> json) {
    // Handle both direct expires_at and expires_in formats
    DateTime expiresAt;
    if (json['expires_at'] != null) {
      expiresAt = DateTime.parse(json['expires_at'].toString());
    } else if (json['expires_in'] != null) {
      final expiresIn = int.tryParse(json['expires_in'].toString()) ?? 3600;
      expiresAt = DateTime.now().add(Duration(seconds: expiresIn));
    } else {
      // Default to 1 hour if no expiration info
      expiresAt = DateTime.now().add(const Duration(hours: 1));
    }

    return AuthToken(
      accessToken: json['access_token']?.toString() ?? '',
      refreshToken: json['refresh_token']?.toString() ?? '',
      tokenType: json['token_type']?.toString() ?? 'Bearer',
      expiresAt: expiresAt,
      scopes: (json['scopes'] as List?)?.cast<String>() ?? [],
    );
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is AuthToken && 
           other.accessToken == accessToken &&
           other.refreshToken == refreshToken;
  }

  @override
  int get hashCode => Object.hash(accessToken, refreshToken);

  @override
  String toString() {
    return 'AuthToken(tokenType: $tokenType, expiresAt: $expiresAt, isExpired: $isExpired)';
  }
}
