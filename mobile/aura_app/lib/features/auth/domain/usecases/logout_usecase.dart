import 'package:dartz/dartz.dart';
import '../../../../core/error/failure.dart';
import '../repositories/auth_repository.dart';

/// Use case for user logout functionality
class LogoutUseCase {
  final AuthRepository _repository;

  const LogoutUseCase(this._repository);

  /// Execute logout
  Future<Either<Failure, Unit>> call() async {
    try {
      await _repository.logout();
      return const Right(unit);
    } catch (e) {
      return Left(AuthFailure(message: e.toString()));
    }
  }
}
