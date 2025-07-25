import 'package:dartz/dartz.dart';
import '../../../../core/error/failure.dart';
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
    final request = LoginRequest(email: email, password: password);
    final result = await _repository.login(request);
    
    return result.fold(
      (failure) => Left(failure),
      (authResult) => Right(authResult.user),
    );
  }
}
