import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../entities/user.dart';
import '../repositories/auth_repository.dart';

/// Use case for user login functionality
class LoginUseCase {
  final AuthRepository _repository;

  const LoginUseCase(this._repository);

  /// Execute login with email and password
  Future<Either<Failure, User>> call({
    required String email,
    required String password,
  }) async {
    return await _repository.login(email, password);
  }
}
