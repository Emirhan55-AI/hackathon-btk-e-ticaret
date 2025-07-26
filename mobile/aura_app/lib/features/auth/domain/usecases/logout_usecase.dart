import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../repositories/auth_repository.dart';

/// Use case for user logout functionality
class LogoutUseCase {
  final AuthRepository _repository;

  const LogoutUseCase(this._repository);

  /// Execute logout
  Future<Either<Failure, void>> call() async {
    return await _repository.logout();
  }
}
