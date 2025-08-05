# AURA AI Test Suite

Bu dizin, AURA AI sisteminin kapsamlı test altyapısını içerir.

## Test Yapısı

```
tests/
├── unit/                    # Birim testleri
│   ├── services/           # Her mikroservis için birim testleri
│   ├── shared/             # Paylaşılan bileşenler için testler
│   └── utils/              # Yardımcı fonksiyonlar için testler
├── integration/            # Entegrasyon testleri
│   ├── api/                # API entegrasyon testleri
│   ├── database/           # Veritabanı entegrasyon testleri
│   └── services/           # Servis-servis entegrasyon testleri
├── e2e/                    # Uçtan uca testler
│   ├── workflows/          # İş akışı testleri
│   ├── user_scenarios/     # Kullanıcı senaryoları
│   └── performance/        # Performans testleri
├── fixtures/               # Test verileri ve sabit değerler
│   ├── images/             # Test görüntüleri
│   ├── json/               # JSON test verileri
│   └── databases/          # Test veritabanı verileri
├── mocks/                  # Mock objeler ve stub'lar
│   ├── external_apis/      # Harici API mock'ları
│   ├── databases/          # Veritabanı mock'ları
│   └── services/           # Servis mock'ları
├── load/                   # Yük testleri
│   ├── stress/             # Stres testleri
│   ├── volume/             # Hacim testleri
│   └── concurrent/         # Eşzamanlılık testleri
├── security/               # Güvenlik testleri
│   ├── auth/               # Kimlik doğrulama testleri
│   ├── permissions/        # Yetki testleri
│   └── vulnerability/      # Güvenlik açığı testleri
└── conftest.py            # Pytest konfigürasyonu ve fixture'lar
```

## Test Kategorileri

### 1. Unit Tests (Birim Testleri)
- Her mikroservisin bireysel bileşenlerini test eder
- Hızlı çalışır ve izole edilmiştir
- 90%+ kod kapsamı hedeflenir

### 2. Integration Tests (Entegrasyon Testleri)
- Servisler arası iletişimi test eder
- API endpoint'lerini doğrular
- Veritabanı bağlantılarını test eder

### 3. End-to-End Tests (Uçtan Uca Testler)
- Gerçek kullanıcı senaryolarını simüle eder
- Tüm sistem bileşenlerini birlikte test eder
- İş akışlarının doğruluğunu kontrol eder

### 4. Performance Tests (Performans Testleri)
- Sistem performansını ölçer
- Yük altında davranışları test eder
- Bottleneck'leri tespit eder

### 5. Security Tests (Güvenlik Testleri)
- Kimlik doğrulama ve yetkilendirme
- Veri güvenliği ve gizliliği
- API güvenlik açıklarını test eder

## Test Çalıştırma

### Tüm Testler
```bash
# scripts/test.ps1 kullanarak
./scripts/test.ps1 -TestType all

# Doğrudan pytest ile
python -m pytest tests/ -v
```

### Kategorik Test Çalıştırma
```bash
# Sadece birim testleri
./scripts/test.ps1 -TestType unit

# Sadece entegrasyon testleri
./scripts/test.ps1 -TestType integration

# Sadece e2e testleri
./scripts/test.ps1 -TestType e2e
```

### Servis Bazlı Test Çalıştırma
```bash
# Belirli bir servis için testler
pytest tests/unit/services/image_processing/ -v

# Birden fazla servis
pytest tests/unit/services/image_processing/ tests/unit/services/nlu/ -v
```

## Test Konfigürasyonu

### conftest.py
Global pytest konfigürasyonu ve paylaşılan fixture'lar:
- Database fixtures
- Service client fixtures
- Mock data generators
- Test environment setup

### Environment Variables
```bash
# Test ortamı değişkenleri
export TESTING=true
export TEST_DATABASE_URL=postgresql://test:test@localhost/aura_test
export TEST_REDIS_URL=redis://localhost:6380
```

## Test Verileri

### Fixtures Dizini
- **images/**: Test için kullanılacak örnek kıyafet görüntüleri
- **json/**: API request/response test verileri
- **databases/**: Test veritabanı seed verileri

### Mock Objeler
- **external_apis/**: Harici API'lar için mock responses
- **databases/**: Veritabanı operasyonları için mock'lar
- **services/**: Mikroservis iletişimi için mock'lar

## Continuous Integration

### GitHub Actions
Test suite'i her commit'te otomatik olarak çalışır:
1. Unit tests (hızlı feedback)
2. Integration tests (API validation)
3. Security tests (vulnerability scanning)
4. Performance baseline tests

### Coverage Reporting
- Minimum %85 kod kapsamı gerekli
- Coverage raporu her test çalışmasında güncellenir
- HTML coverage raporu `htmlcov/` dizininde

## Test Yazma Standartları

### Naming Convention
```python
# Test dosya isimleri
test_image_processing_service.py
test_nlu_classifier.py
test_style_profile_api.py

# Test fonksiyon isimleri
def test_analyze_clothing_success():
def test_classify_feedback_invalid_input():
def test_get_user_profile_not_found():
```

### Test Structure
```python
def test_function_name():
    # Arrange - Test verilerini hazırla
    user_id = "test_user_123"
    test_image = load_test_image("dress.jpg")
    
    # Act - Test edilecek fonksiyonu çalıştır
    result = image_service.analyze_clothing(test_image, user_id)
    
    # Assert - Sonuçları doğrula
    assert result.success is True
    assert result.clothing_type == "dress"
    assert len(result.colors) > 0
```

### Mock Usage
```python
@pytest.fixture
def mock_image_analysis():
    with patch('services.external.vision_api.analyze') as mock:
        mock.return_value = {
            "clothing_type": "dress",
            "colors": ["red", "blue"],
            "style": "casual"
        }
        yield mock

def test_with_mock(mock_image_analysis):
    # Test implementation using the mock
    pass
```

## Troubleshooting

### Common Issues
1. **Test Database Connection**: Test ortamında PostgreSQL çalışıyor mu?
2. **Port Conflicts**: Test servisleri farklı portlarda çalışıyor mu?
3. **Mock Data**: Test verileri güncel ve geçerli mi?

### Debug Mode
```bash
# Detaylı debug output ile test çalıştırma
pytest tests/ -v -s --tb=long

# Specific test debug
pytest tests/unit/services/image_processing/test_analyzer.py::test_analyze_clothing_success -v -s
```

## Best Practices

1. **Test Isolation**: Her test bağımsız olmalı
2. **Fast Feedback**: Unit testler hızlı çalışmalı (<1s)
3. **Realistic Data**: Test verileri gerçek senaryoları yansıtmalı
4. **Clear Assertions**: Assert mesajları açıklayıcı olmalı
5. **Cleanup**: Test sonrası temizlik yapılmalı

Bu test suite'i ile AURA AI sisteminin güvenilirliği ve kalitesi garanti altına alınır.
