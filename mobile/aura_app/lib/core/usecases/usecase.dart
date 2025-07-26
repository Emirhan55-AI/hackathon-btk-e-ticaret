import 'package:dartz/dartz.dart';
import '../error/failures.dart';

/// Base interface for use cases with parameters
abstract class UseCase<Type, Params> {
  Future<Either<Failure, Type>> call(Params params);
}

/// Base interface for use cases without parameters
abstract class UseCaseNoParams<Type> {
  Future<Either<Failure, Type>> call();
}

/// Empty parameters class for use cases that don't require input
class NoParams {
  const NoParams();
}
