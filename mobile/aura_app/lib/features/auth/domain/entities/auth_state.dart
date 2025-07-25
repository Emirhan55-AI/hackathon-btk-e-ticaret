import 'package:freezed_annotation/freezed_annotation.dart';
import 'user.dart';
import '../../../../core/error/failures.dart';

part 'auth_state.freezed.dart';

/// Authentication state using freezed for immutability
@freezed
class AuthState with _$AuthState {
  const factory AuthState.initial() = _Initial;
  const factory AuthState.loading() = _Loading;
  const factory AuthState.authenticated(User user) = _Authenticated;
  const factory AuthState.unauthenticated() = _Unauthenticated;
  const factory AuthState.error(Failure failure) = _Error;
}
