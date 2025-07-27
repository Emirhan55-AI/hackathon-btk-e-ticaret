// Mock classes for wardrobe testing - auto-generated mocks for test isolation
// These mock classes provide controlled behavior for testing wardrobe functionality

import 'package:mockito/annotations.dart';
import 'package:aura_app/features/wardrobe/domain/usecases/get_clothing_items.dart';
import 'package:aura_app/features/wardrobe/domain/usecases/add_clothing_item.dart';
import 'package:aura_app/features/wardrobe/domain/usecases/update_clothing_item.dart';
import 'package:aura_app/features/wardrobe/domain/usecases/delete_clothing_item.dart';
import 'package:aura_app/features/wardrobe/domain/usecases/search_clothing_items.dart';

// Generate mock classes for all use cases required for wardrobe testing
// These mocks allow us to control behavior during testing without real API calls
@GenerateMocks([
  GetClothingItems,
  AddClothingItem,
  UpdateClothingItem,
  DeleteClothingItem,
  SearchClothingItems,
])
void main() {}
