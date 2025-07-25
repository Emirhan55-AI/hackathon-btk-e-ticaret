// Mocks generated by Mockito 5.4.5 from annotations
// in aura_app/test/features/ecommerce/presentation/screens/product_search_screen_test.dart.
// Do not manually edit this file.

// ignore_for_file: no_leading_underscores_for_library_prefixes
import 'dart:async' as _i5;

import 'package:aura_app/features/ecommerce/domain/entities/product.dart'
    as _i6;
import 'package:aura_app/features/ecommerce/presentation/notifiers/product_search_notifier.dart'
    as _i3;
import 'package:aura_app/features/ecommerce/presentation/notifiers/product_search_state.dart'
    as _i2;
import 'package:flutter_riverpod/flutter_riverpod.dart' as _i4;
import 'package:mockito/mockito.dart' as _i1;
import 'package:state_notifier/state_notifier.dart' as _i7;

// ignore_for_file: type=lint
// ignore_for_file: avoid_redundant_argument_values
// ignore_for_file: avoid_setters_without_getters
// ignore_for_file: comment_references
// ignore_for_file: deprecated_member_use
// ignore_for_file: deprecated_member_use_from_same_package
// ignore_for_file: implementation_imports
// ignore_for_file: invalid_use_of_visible_for_testing_member
// ignore_for_file: must_be_immutable
// ignore_for_file: prefer_const_constructors
// ignore_for_file: unnecessary_parenthesis
// ignore_for_file: camel_case_types
// ignore_for_file: subtype_of_sealed_class

class _FakeProductSearchState_0 extends _i1.SmartFake
    implements _i2.ProductSearchState {
  _FakeProductSearchState_0(
    Object parent,
    Invocation parentInvocation,
  ) : super(
          parent,
          parentInvocation,
        );
}

/// A class which mocks [ProductSearchNotifier].
///
/// See the documentation for Mockito's code generation for more information.
class MockProductSearchNotifier extends _i1.Mock
    implements _i3.ProductSearchNotifier {
  @override
  set onError(_i4.ErrorListener? _onError) => super.noSuchMethod(
        Invocation.setter(
          #onError,
          _onError,
        ),
        returnValueForMissingStub: null,
      );

  @override
  bool get mounted => (super.noSuchMethod(
        Invocation.getter(#mounted),
        returnValue: false,
        returnValueForMissingStub: false,
      ) as bool);

  @override
  _i5.Stream<_i2.ProductSearchState> get stream => (super.noSuchMethod(
        Invocation.getter(#stream),
        returnValue: _i5.Stream<_i2.ProductSearchState>.empty(),
        returnValueForMissingStub: _i5.Stream<_i2.ProductSearchState>.empty(),
      ) as _i5.Stream<_i2.ProductSearchState>);

  @override
  _i2.ProductSearchState get state => (super.noSuchMethod(
        Invocation.getter(#state),
        returnValue: _FakeProductSearchState_0(
          this,
          Invocation.getter(#state),
        ),
        returnValueForMissingStub: _FakeProductSearchState_0(
          this,
          Invocation.getter(#state),
        ),
      ) as _i2.ProductSearchState);

  @override
  set state(_i2.ProductSearchState? value) => super.noSuchMethod(
        Invocation.setter(
          #state,
          value,
        ),
        returnValueForMissingStub: null,
      );

  @override
  _i2.ProductSearchState get debugState => (super.noSuchMethod(
        Invocation.getter(#debugState),
        returnValue: _FakeProductSearchState_0(
          this,
          Invocation.getter(#debugState),
        ),
        returnValueForMissingStub: _FakeProductSearchState_0(
          this,
          Invocation.getter(#debugState),
        ),
      ) as _i2.ProductSearchState);

  @override
  bool get hasListeners => (super.noSuchMethod(
        Invocation.getter(#hasListeners),
        returnValue: false,
        returnValueForMissingStub: false,
      ) as bool);

  @override
  _i5.Future<void> searchProducts(
    String? query, {
    _i6.ProductFilter? filter,
  }) =>
      (super.noSuchMethod(
        Invocation.method(
          #searchProducts,
          [query],
          {#filter: filter},
        ),
        returnValue: _i5.Future<void>.value(),
        returnValueForMissingStub: _i5.Future<void>.value(),
      ) as _i5.Future<void>);

  @override
  _i5.Future<void> loadMoreProducts() => (super.noSuchMethod(
        Invocation.method(
          #loadMoreProducts,
          [],
        ),
        returnValue: _i5.Future<void>.value(),
        returnValueForMissingStub: _i5.Future<void>.value(),
      ) as _i5.Future<void>);

  @override
  _i5.Future<void> applyFilter(_i6.ProductFilter? filter) =>
      (super.noSuchMethod(
        Invocation.method(
          #applyFilter,
          [filter],
        ),
        returnValue: _i5.Future<void>.value(),
        returnValueForMissingStub: _i5.Future<void>.value(),
      ) as _i5.Future<void>);

  @override
  _i5.Future<void> clearFilters() => (super.noSuchMethod(
        Invocation.method(
          #clearFilters,
          [],
        ),
        returnValue: _i5.Future<void>.value(),
        returnValueForMissingStub: _i5.Future<void>.value(),
      ) as _i5.Future<void>);

  @override
  _i5.Future<void> refresh() => (super.noSuchMethod(
        Invocation.method(
          #refresh,
          [],
        ),
        returnValue: _i5.Future<void>.value(),
        returnValueForMissingStub: _i5.Future<void>.value(),
      ) as _i5.Future<void>);

  @override
  void clearSearch() => super.noSuchMethod(
        Invocation.method(
          #clearSearch,
          [],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void updateSearchQuery(String? query) => super.noSuchMethod(
        Invocation.method(
          #updateSearchQuery,
          [query],
        ),
        returnValueForMissingStub: null,
      );

  @override
  _i5.Future<List<String>> getCategories() => (super.noSuchMethod(
        Invocation.method(
          #getCategories,
          [],
        ),
        returnValue: _i5.Future<List<String>>.value(<String>[]),
        returnValueForMissingStub: _i5.Future<List<String>>.value(<String>[]),
      ) as _i5.Future<List<String>>);

  @override
  _i5.Future<List<String>> getBrands({String? category}) => (super.noSuchMethod(
        Invocation.method(
          #getBrands,
          [],
          {#category: category},
        ),
        returnValue: _i5.Future<List<String>>.value(<String>[]),
        returnValueForMissingStub: _i5.Future<List<String>>.value(<String>[]),
      ) as _i5.Future<List<String>>);

  @override
  bool updateShouldNotify(
    _i2.ProductSearchState? old,
    _i2.ProductSearchState? current,
  ) =>
      (super.noSuchMethod(
        Invocation.method(
          #updateShouldNotify,
          [
            old,
            current,
          ],
        ),
        returnValue: false,
        returnValueForMissingStub: false,
      ) as bool);

  @override
  _i4.RemoveListener addListener(
    _i7.Listener<_i2.ProductSearchState>? listener, {
    bool? fireImmediately = true,
  }) =>
      (super.noSuchMethod(
        Invocation.method(
          #addListener,
          [listener],
          {#fireImmediately: fireImmediately},
        ),
        returnValue: () {},
        returnValueForMissingStub: () {},
      ) as _i4.RemoveListener);

  @override
  void dispose() => super.noSuchMethod(
        Invocation.method(
          #dispose,
          [],
        ),
        returnValueForMissingStub: null,
      );
}
