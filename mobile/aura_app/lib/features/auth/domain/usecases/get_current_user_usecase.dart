import 'package:dartz/dartz.dart';
import '../../../../core/error/failure.dart';
import '../entities/user.dart';
import '../repositories/auth_repository.dart';

/// Use case for getting current authenticated user
class GetCurrentUserUseCase {
  final AuthRepository _repository;

  const GetCurrentUserUseCase(this._repository);

  /// Execute get current user
  Future<Either<Failure, User?>> call() async {
    try {
      final user = await _repository.getCurrentUser();
      return Right(user);
    } catch (e) {
      return Left(AuthFailure(message: e.toString()));
    }
  }
}
