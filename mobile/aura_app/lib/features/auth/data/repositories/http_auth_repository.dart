import 'package:dartz/dartz.dart';

import '../../../../core/error/exceptions.dart';
import '../../../../core/error/failures.dart';
import '../datasources/auth_remote_data_source.dart';
import '../../domain/entities/user.dart';
import '../../domain/repositories/auth_repository.dart';

/// HTTP implementation of AuthRepository using data source
class HttpAuthRepository implements AuthRepository {
  final AuthRemoteDataSource _remoteDataSource;

  HttpAuthRepository({
    required AuthRemoteDataSource remoteDataSource,
  }) : _remoteDataSource = remoteDataSource;

  @override
  Future<Either<Failure, User>> login(String email, String password) async {
    try {
      final userModel = await _remoteDataSource.login(email, password);
      return Right(userModel.toEntity());
    } on ApiException catch (e) {
      return Left(ServerFailure(
        message: e.message,
        details: 'Status code: ${e.statusCode}',
      ));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } on UnknownException catch (e) {
      return Left(UnknownFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Unexpected error: ${e.toString()}'));
    }
  }

  @override
  Future<Either<Failure, User>> register({
    required String email,
    required String password,
    String? firstName,
    String? lastName,
  }) async {
    try {
      final userModel = await _remoteDataSource.register(
        email: email,
        password: password,
        firstName: firstName,
        lastName: lastName,
      );
      return Right(userModel.toEntity());
    } on ApiException catch (e) {
      return Left(ServerFailure(
        message: e.message,
        details: 'Status code: ${e.statusCode}',
      ));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } on UnknownException catch (e) {
      return Left(UnknownFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Unexpected error: ${e.toString()}'));
    }
  }

  @override
  Future<Either<Failure, void>> logout() async {
    try {
      await _remoteDataSource.logout();
      return const Right(null);
    } on ApiException catch (e) {
      return Left(ServerFailure(
        message: e.message,
        details: 'Status code: ${e.statusCode}',
      ));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } on UnknownException catch (e) {
      return Left(UnknownFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Unexpected error: ${e.toString()}'));
    }
  }

  @override
  Future<Either<Failure, User>> getCurrentUser() async {
    try {
      final userModel = await _remoteDataSource.getCurrentUser();
      return Right(userModel.toEntity());
    } on ApiException catch (e) {
      return Left(ServerFailure(
        message: e.message,
        details: 'Status code: ${e.statusCode}',
      ));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } on UnknownException catch (e) {
      return Left(UnknownFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Unexpected error: ${e.toString()}'));
    }
  }

  @override
  Future<Either<Failure, User>> refreshToken() async {
    try {
      final userModel = await _remoteDataSource.getCurrentUser();
      return Right(userModel.toEntity());
    } on ApiException catch (e) {
      return Left(ServerFailure(
        message: e.message,
        details: 'Status code: ${e.statusCode}',
      ));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } on UnknownException catch (e) {
      return Left(UnknownFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Unexpected error: ${e.toString()}'));
    }
  }

  @override
  Future<Either<Failure, User>> updateProfile({
    String? firstName,
    String? lastName,
    String? profileImage,
    DateTime? dateOfBirth,
    String? gender,
  }) async {
    try {
      // For Phase 1, we'll use getCurrentUser as placeholder
      // In Phase 2, implement actual profile update API call
      final userModel = await _remoteDataSource.getCurrentUser();
      return Right(userModel.toEntity());
    } on ApiException catch (e) {
      return Left(ServerFailure(
        message: e.message,
        details: 'Status code: ${e.statusCode}',
      ));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } on UnknownException catch (e) {
      return Left(UnknownFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Unexpected error: ${e.toString()}'));
    }
  }

  @override
  Future<Either<Failure, void>> changePassword({
    required String currentPassword,
    required String newPassword,
  }) async {
    try {
      // For Phase 1, we'll implement basic functionality
      // In Phase 2, implement actual password change API call
      await _remoteDataSource.logout();
      return const Right(null);
    } on ApiException catch (e) {
      return Left(ServerFailure(
        message: e.message,
        details: 'Status code: ${e.statusCode}',
      ));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } on UnknownException catch (e) {
      return Left(UnknownFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Unexpected error: ${e.toString()}'));
    }
  }

  @override
  Future<Either<Failure, void>> deleteAccount() async {
    try {
      await _remoteDataSource.logout();
      return const Right(null);
    } on ApiException catch (e) {
      return Left(ServerFailure(
        message: e.message,
        details: 'Status code: ${e.statusCode}',
      ));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } on UnknownException catch (e) {
      return Left(UnknownFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Unexpected error: ${e.toString()}'));
    }
  }
}
