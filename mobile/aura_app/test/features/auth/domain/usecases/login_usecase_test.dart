import 'package:flutter_test/flutter_test.dart';
import 'package:dartz/dartz.dart';

import 'package:aura_app/core/error/failures.dart';
import 'package:aura_app/features/auth/domain/entities/user.dart';
import 'package:aura_app/features/auth/domain/repositories/auth_repository.dart';
import 'package:aura_app/features/auth/domain/usecases/login_usecase.dart';

/// Mock implementation of AuthRepository for testing
class MockAuthRepository implements AuthRepository {
  late Either<Failure, User> _loginResult;
  late Either<Failure, User> _registerResult;
  late Either<Failure, void> _logoutResult;
  late Either<Failure, User> _getCurrentUserResult;

  void setLoginResult(Either<Failure, User> result) {
    _loginResult = result;
  }

  void setRegisterResult(Either<Failure, User> result) {
    _registerResult = result;
  }

  void setLogoutResult(Either<Failure, void> result) {
    _logoutResult = result;
  }

  void setGetCurrentUserResult(Either<Failure, User> result) {
    _getCurrentUserResult = result;
  }

  @override
  Future<Either<Failure, User>> login(String email, String password) async {
    return _loginResult;
  }

  @override
  Future<Either<Failure, User>> register({
    required String email,
    required String password,
    String? firstName,
    String? lastName,
  }) async {
    return _registerResult;
  }

  @override
  Future<Either<Failure, void>> logout() async {
    return _logoutResult;
  }

  @override
  Future<Either<Failure, User>> getCurrentUser() async {
    return _getCurrentUserResult;
  }

  @override
  Future<Either<Failure, User>> refreshToken() async {
    return _getCurrentUserResult;
  }

  @override
  Future<Either<Failure, User>> updateProfile({
    String? firstName,
    String? lastName,
    String? profileImage,
    DateTime? dateOfBirth,
    String? gender,
  }) async {
    return _getCurrentUserResult;
  }

  @override
  Future<Either<Failure, void>> changePassword({
    required String currentPassword,
    required String newPassword,
  }) async {
    return _logoutResult;
  }

  @override
  Future<Either<Failure, void>> deleteAccount() async {
    return _logoutResult;
  }
}

void main() {
  late MockAuthRepository mockAuthRepository;
  late LoginUseCase usecase;

  setUp(() {
    mockAuthRepository = MockAuthRepository();
    usecase = LoginUseCase(mockAuthRepository);
  });

  final tUser = User(
    id: '1',
    email: 'test@example.com',
    firstName: 'Test',
    lastName: 'User',
    createdAt: DateTime.now(),
    updatedAt: DateTime.now(),
  );

  const tEmail = 'test@example.com';
  const tPassword = 'password123';

  group('LoginUseCase', () {
    test('should return User when login is successful', () async {
      // arrange
      mockAuthRepository.setLoginResult(Right(tUser));

      // act
      final result = await usecase(email: tEmail, password: tPassword);

      // assert
      expect(result, equals(Right(tUser)));
    });

    test('should return ApiFailure when login fails with invalid credentials', () async {
      // arrange
      const failure = ApiFailure(message: 'Invalid credentials');
      mockAuthRepository.setLoginResult(const Left(failure));

      // act
      final result = await usecase(email: tEmail, password: tPassword);

      // assert
      expect(result, equals(const Left(failure)));
    });

    test('should return NetworkFailure when there is no internet connection', () async {
      // arrange
      const failure = NetworkFailure(message: 'No internet connection');
      mockAuthRepository.setLoginResult(const Left(failure));

      // act
      final result = await usecase(email: tEmail, password: tPassword);

      // assert
      expect(result, equals(const Left(failure)));
    });

    test('should return UnknownFailure when an unexpected error occurs', () async {
      // arrange
      const failure = UnknownFailure(message: 'Unexpected error');
      mockAuthRepository.setLoginResult(const Left(failure));

      // act
      final result = await usecase(email: tEmail, password: tPassword);

      // assert
      expect(result, equals(const Left(failure)));
    });
  });
}
