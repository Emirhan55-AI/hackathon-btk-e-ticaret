import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:dartz/dartz.dart';

import 'package:aura_app/core/error/exceptions.dart';
import 'package:aura_app/core/error/failures.dart';
import 'package:aura_app/features/auth/data/repositories/http_auth_repository.dart';
import 'package:aura_app/features/auth/domain/entities/user.dart';
import 'package:aura_app/features/auth/data/models/user_model.dart';
import 'package:aura_app/features/auth/data/datasources/auth_remote_data_source.dart';

import 'http_auth_repository_test.mocks.dart';

@GenerateMocks([AuthRemoteDataSource])
void main() {
  late MockAuthRemoteDataSource mockRemoteDataSource;
  late HttpAuthRepository repository;

  setUp(() {
    mockRemoteDataSource = MockAuthRemoteDataSource();
    repository = HttpAuthRepository(remoteDataSource: mockRemoteDataSource);
  });

  final tUserModel = UserModel(
    id: '1',
    email: 'test@example.com',
    firstName: 'Test',
    lastName: 'User',
    createdAt: DateTime.now(),
    updatedAt: DateTime.now(),
  );

  final tUser = tUserModel.toEntity();

  group('login', () {
    const tEmail = 'test@example.com';
    const tPassword = 'password123';

    test('should return User when the call to remote data source is successful', () async {
      // arrange
      when(mockRemoteDataSource.login(any, any))
          .thenAnswer((_) async => tUserModel);

      // act
      final result = await repository.login(tEmail, tPassword);

      // assert
      expect(result, equals(Right(tUser)));
      verify(mockRemoteDataSource.login(tEmail, tPassword));
      verifyNoMoreInteractions(mockRemoteDataSource);
    });

    test('should return ApiFailure when the call to remote data source throws ApiException', () async {
      // arrange
      final apiException = ApiException(message: 'Invalid credentials', statusCode: 401);
      when(mockRemoteDataSource.login(any, any))
          .thenThrow(apiException);

      // act
      final result = await repository.login(tEmail, tPassword);

      // assert
      expect(result, equals(Left(ServerFailure(
        message: 'Invalid credentials',
        details: 'Status code: 401',
      ))));
      verify(mockRemoteDataSource.login(tEmail, tPassword));
      verifyNoMoreInteractions(mockRemoteDataSource);
    });

    test('should return NetworkFailure when the call to remote data source throws NetworkException', () async {
      // arrange
      when(mockRemoteDataSource.login(any, any))
          .thenThrow(NetworkException(message: 'No internet connection'));

      // act
      final result = await repository.login(tEmail, tPassword);

      // assert
      expect(result, equals(Left(NetworkFailure(message: 'No internet connection'))));
      verify(mockRemoteDataSource.login(tEmail, tPassword));
      verifyNoMoreInteractions(mockRemoteDataSource);
    });

    test('should return UnknownFailure when the call to remote data source throws UnknownException', () async {
      // arrange
      when(mockRemoteDataSource.login(any, any))
          .thenThrow(UnknownException(message: 'Unknown error'));

      // act
      final result = await repository.login(tEmail, tPassword);

      // assert
      expect(result, equals(Left(UnknownFailure(message: 'Unknown error'))));
      verify(mockRemoteDataSource.login(tEmail, tPassword));
      verifyNoMoreInteractions(mockRemoteDataSource);
    });
  });

  group('register', () {
    const tEmail = 'test@example.com';
    const tPassword = 'password123';
    const tFirstName = 'Test';
    const tLastName = 'User';

    test('should return User when the call to remote data source is successful', () async {
      // arrange
      when(mockRemoteDataSource.register(
        email: anyNamed('email'),
        password: anyNamed('password'),
        firstName: anyNamed('firstName'),
        lastName: anyNamed('lastName'),
      )).thenAnswer((_) async => tUserModel);

      // act
      final result = await repository.register(
        email: tEmail,
        password: tPassword,
        firstName: tFirstName,
        lastName: tLastName,
      );

      // assert
      expect(result, equals(Right(tUser)));
      verify(mockRemoteDataSource.register(
        email: tEmail,
        password: tPassword,
        firstName: tFirstName,
        lastName: tLastName,
      ));
      verifyNoMoreInteractions(mockRemoteDataSource);
    });

    test('should return ApiFailure when registration fails', () async {
      // arrange
      final apiException = ApiException(message: 'Email already exists', statusCode: 400);
      when(mockRemoteDataSource.register(
        email: anyNamed('email'),
        password: anyNamed('password'),
        firstName: anyNamed('firstName'),
        lastName: anyNamed('lastName'),
      )).thenThrow(apiException);

      // act
      final result = await repository.register(
        email: tEmail,
        password: tPassword,
        firstName: tFirstName,
        lastName: tLastName,
      );

      // assert
      expect(result, equals(Left(ServerFailure(
        message: 'Email already exists',
        details: 'Status code: 400',
      ))));
    });
  });

  group('logout', () {
    test('should return void when the call to remote data source is successful', () async {
      // arrange
      when(mockRemoteDataSource.logout())
          .thenAnswer((_) async => {});

      // act
      final result = await repository.logout();

      // assert
      expect(result, equals(const Right(null)));
      verify(mockRemoteDataSource.logout());
      verifyNoMoreInteractions(mockRemoteDataSource);
    });

    test('should return ApiFailure when logout fails', () async {
      // arrange
      final apiException = ApiException(message: 'Logout failed', statusCode: 500);
      when(mockRemoteDataSource.logout())
          .thenThrow(apiException);

      // act
      final result = await repository.logout();

      // assert
      expect(result, equals(Left(ServerFailure(
        message: 'Logout failed',
        details: 'Status code: 500',
      ))));
    });
  });

  group('getCurrentUser', () {
    test('should return User when the call to remote data source is successful', () async {
      // arrange
      when(mockRemoteDataSource.getCurrentUser())
          .thenAnswer((_) async => tUserModel);

      // act
      final result = await repository.getCurrentUser();

      // assert
      expect(result, equals(Right(tUser)));
      verify(mockRemoteDataSource.getCurrentUser());
      verifyNoMoreInteractions(mockRemoteDataSource);
    });

    test('should return ApiFailure when user is not authenticated', () async {
      // arrange
      final apiException = ApiException(message: 'Unauthorized', statusCode: 401);
      when(mockRemoteDataSource.getCurrentUser())
          .thenThrow(apiException);

      // act
      final result = await repository.getCurrentUser();

      // assert
      expect(result, equals(Left(ServerFailure(
        message: 'Unauthorized',
        details: 'Status code: 401',
      ))));
    });
  });
}
