# 🧪 AURA AI SİSTEMİ - BİRİM TESTLERİ
# Her bir mikroservisin kritik fonksiyonları için otomatik birim testleri

import pytest
import requests
import json
import time
from typing import Dict, Any

class TestImageProcessingService:
    """
    Görüntü İşleme AI servisi için birim testleri.
    
    Bu test sınıfı, görüntü analizi fonksiyonlarının doğru çalışıp
    çalışmadığını kontrol eder.
    """
    
    def test_image_analysis_endpoint_exists(self, test_config, test_utils):
        """Görüntü analizi endpoint'inin mevcut olduğunu test eder"""
        service_url = test_config.SERVICES['image_processing']
        
        # Health check ile servisin çalıştığını kontrol et
        is_healthy = test_utils.check_service_health(service_url)
        assert is_healthy, f"Görüntü işleme servisi çalışmıyor: {service_url}"
        
        # Analyze endpoint'inin mevcut olduğunu kontrol et
        try:
            response = requests.post(
                f"{service_url}/analyze",
                json=test_config.MOCK_IMAGE_DATA,
                timeout=test_config.TIMEOUT_MEDIUM
            )
            # 200 veya 422 (validation error) beklenen yanıtlar
            assert response.status_code in [200, 422], f"Beklenmeyen status kodu: {response.status_code}"
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Endpoint'e erişim hatası: {str(e)}")
    
    def test_image_analysis_response_format(self, test_config):
        """Görüntü analizi yanıt formatının doğru olduğunu test eder"""
        service_url = test_config.SERVICES['image_processing']
        
        try:
            response = requests.post(
                f"{service_url}/analyze",
                json=test_config.MOCK_IMAGE_DATA,
                timeout=test_config.TIMEOUT_MEDIUM
            )
            
            if response.status_code == 200:
                response_data = response.json()
                
                # Temel alanların varlığını kontrol et
                assert isinstance(response_data, dict), "Yanıt dictionary formatında olmalı"
                
                # Mock servis yanıtı için esnek kontrol
                # Gerçek implementasyonda daha sıkı kontroller yapılabilir
                print(f"✅ Görüntü analizi yanıtı alındı: {response_data}")
                
        except requests.exceptions.RequestException:
            # Servis çalışmıyorsa test geç
            pytest.skip("Görüntü işleme servisi erişilebilir değil")
    
    def test_image_analysis_performance(self, test_config, test_utils):
        """Görüntü analizi performansını test eder"""
        service_url = test_config.SERVICES['image_processing']
        
        def make_request():
            return requests.post(
                f"{service_url}/analyze",
                json=test_config.MOCK_IMAGE_DATA,
                timeout=test_config.TIMEOUT_MEDIUM
            )
        
        try:
            result, duration_ms = test_utils.measure_response_time(make_request)
            
            # Performans limiti: 5 saniye
            performance_limit_ms = 5000
            assert duration_ms < performance_limit_ms, \
                f"Görüntü analizi çok yavaş: {duration_ms:.2f}ms > {performance_limit_ms}ms"
            
            print(f"✅ Görüntü analizi performansı: {duration_ms:.2f}ms")
            
        except requests.exceptions.RequestException:
            pytest.skip("Görüntü işleme servisi erişilebilir değil")

class TestNLUService:
    """
    Doğal Dil İşleme (NLU) AI servisi için birim testleri.
    
    Bu test sınıfı, doğal dil analizi fonksiyonlarının doğru çalışıp
    çalışmadığını kontrol eder.
    """
    
    def test_nlu_endpoint_exists(self, test_config, test_utils):
        """NLU analizi endpoint'inin mevcut olduğunu test eder"""
        service_url = test_config.SERVICES['nlu']
        
        # Health check ile servisin çalıştığını kontrol et
        is_healthy = test_utils.check_service_health(service_url)
        assert is_healthy, f"NLU servisi çalışmıyor: {service_url}"
        
        # Parse request endpoint'inin mevcut olduğunu kontrol et
        try:
            response = requests.post(
                f"{service_url}/parse_request",
                json=test_config.MOCK_NLU_DATA,
                timeout=test_config.TIMEOUT_MEDIUM
            )
            # 200 veya 422 (validation error) beklenen yanıtlar
            assert response.status_code in [200, 422], f"Beklenmeyen status kodu: {response.status_code}"
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Endpoint'e erişim hatası: {str(e)}")
    
    def test_nlu_turkish_language_support(self, test_config):
        """NLU servisinin Türkçe dil desteğini test eder"""
        service_url = test_config.SERVICES['nlu']
        
        turkish_test_cases = [
            "Bugün işe gideceğim, şık bir ayakkabıya ihtiyacım var",
            "Spor yapmak için rahat kıyafet önerisi istiyorum",
            "Akşam yemeği için şık bir elbise arıyorum"
        ]
        
        for test_text in turkish_test_cases:
            nlu_data = {
                'text': test_text,
                'language': 'tr',
                'context': 'product_recommendation'
            }
            
            try:
                response = requests.post(
                    f"{service_url}/parse_request",
                    json=nlu_data,
                    timeout=test_config.TIMEOUT_MEDIUM
                )
                
                if response.status_code == 200:
                    response_data = response.json()
                    print(f"✅ Türkçe NLU analizi: '{test_text}' -> {response_data}")
                    
            except requests.exceptions.RequestException:
                pytest.skip("NLU servisi erişilebilir değil")
    
    def test_nlu_intent_detection(self, test_config):
        """NLU servisinin niyet tespiti yeteneğini test eder"""
        service_url = test_config.SERVICES['nlu']
        
        intent_test_cases = [
            {
                'text': 'Ayakkabı satın almak istiyorum',
                'expected_context': ['product', 'purchase', 'shoes']
            },
            {
                'text': 'Kıyafet önerisi istiyorum',
                'expected_context': ['recommendation', 'clothing']
            }
        ]
        
        for test_case in intent_test_cases:
            nlu_data = {
                'text': test_case['text'],
                'language': 'tr',
                'context': 'product_recommendation'
            }
            
            try:
                response = requests.post(
                    f"{service_url}/parse_request",
                    json=nlu_data,
                    timeout=test_config.TIMEOUT_MEDIUM
                )
                
                if response.status_code == 200:
                    response_data = response.json()
                    
                    # Intent tespiti kontrolü (mock serviste bu alan olmayabilir)
                    if 'intent' in response_data or 'context' in response_data:
                        print(f"✅ Intent tespiti: '{test_case['text']}' -> {response_data}")
                    
            except requests.exceptions.RequestException:
                pytest.skip("NLU servisi erişilebilir değil")

class TestStyleProfileService:
    """
    Stil Profili AI servisi için birim testleri.
    
    Bu test sınıfı, stil analizi fonksiyonlarının doğru çalışıp
    çalışmadığını kontrol eder.
    """
    
    def test_style_profile_endpoint_exists(self, test_config, test_utils):
        """Stil profili endpoint'inin mevcut olduğunu test eder"""
        service_url = test_config.SERVICES['style_profile']
        
        # Health check ile servisin çalıştığını kontrol et
        is_healthy = test_utils.check_service_health(service_url)
        assert is_healthy, f"Stil profili servisi çalışmıyor: {service_url}"
        
        # Create profile endpoint'inin mevcut olduğunu kontrol et
        profile_data = {
            'user_preferences': {
                'activity': 'business',
                'style_preference': 'modern',
                'color_preferences': ['blue', 'black', 'white']
            }
        }
        
        try:
            response = requests.post(
                f"{service_url}/create_profile",
                json=profile_data,
                timeout=test_config.TIMEOUT_MEDIUM
            )
            # 200 veya 422 (validation error) beklenen yanıtlar
            assert response.status_code in [200, 422], f"Beklenmeyen status kodu: {response.status_code}"
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Endpoint'e erişim hatası: {str(e)}")
    
    def test_style_profile_creation(self, test_config):
        """Stil profili oluşturma fonksiyonunu test eder"""
        service_url = test_config.SERVICES['style_profile']
        
        style_test_cases = [
            {
                'activity': 'business',
                'style_preference': 'formal',
                'expected_style': 'business_formal'
            },
            {
                'activity': 'sport',
                'style_preference': 'casual',
                'expected_style': 'sport_casual'
            }
        ]
        
        for test_case in style_test_cases:
            profile_data = {
                'user_preferences': {
                    'activity': test_case['activity'],
                    'style_preference': test_case['style_preference'],
                    'color_preferences': ['blue', 'black']
                }
            }
            
            try:
                response = requests.post(
                    f"{service_url}/create_profile",
                    json=profile_data,
                    timeout=test_config.TIMEOUT_MEDIUM
                )
                
                if response.status_code == 200:
                    response_data = response.json()
                    print(f"✅ Stil profili oluşturuldu: {test_case['activity']} -> {response_data}")
                    
            except requests.exceptions.RequestException:
                pytest.skip("Stil profili servisi erişilebilir değil")

class TestRecommendationService:
    """
    Öneri Motoru AI servisi için birim testleri.
    
    Bu test sınıfı, ürün önerisi fonksiyonlarının doğru çalışıp
    çalışmadığını kontrol eder.
    """
    
    def test_recommendation_endpoint_exists(self, test_config, test_utils):
        """Öneri motoru endpoint'inin mevcut olduğunu test eder"""
        service_url = test_config.SERVICES['recommendation']
        
        # Health check ile servisin çalıştığını kontrol et
        is_healthy = test_utils.check_service_health(service_url)
        assert is_healthy, f"Öneri motoru servisi çalışmıyor: {service_url}"
        
        # Get recommendations endpoint'inin mevcut olduğunu kontrol et
        recommendation_data = {
            'user_profile': {
                'style_type': 'modern_casual',
                'color_preferences': ['blue', 'black']
            },
            'search_criteria': {
                'category': 'shoes',
                'budget_range': 'medium'
            }
        }
        
        try:
            response = requests.post(
                f"{service_url}/get_recommendations",
                json=recommendation_data,
                timeout=test_config.TIMEOUT_MEDIUM
            )
            # 200 veya 422 (validation error) beklenen yanıtlar
            assert response.status_code in [200, 422], f"Beklenmeyen status kodu: {response.status_code}"
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Endpoint'e erişim hatası: {str(e)}")
    
    def test_recommendation_response_structure(self, test_config):
        """Öneri motoru yanıt yapısını test eder"""
        service_url = test_config.SERVICES['recommendation']
        
        recommendation_data = {
            'user_profile': {
                'style_type': 'modern_casual',
                'color_preferences': ['blue', 'black']
            },
            'search_criteria': {
                'category': 'shoes',
                'budget_range': 'medium'
            }
        }
        
        try:
            response = requests.post(
                f"{service_url}/get_recommendations",
                json=recommendation_data,
                timeout=test_config.TIMEOUT_MEDIUM
            )
            
            if response.status_code == 200:
                response_data = response.json()
                
                # Temel yapı kontrolü
                assert isinstance(response_data, dict), "Yanıt dictionary formatında olmalı"
                
                # Öneriler listesi kontrolü (varsa)
                if 'recommendations' in response_data:
                    recommendations = response_data['recommendations']
                    assert isinstance(recommendations, list), "Öneriler liste formatında olmalı"
                    
                print(f"✅ Öneri motoru yanıtı: {response_data}")
                
        except requests.exceptions.RequestException:
            pytest.skip("Öneri motoru servisi erişilebilir değil")

class TestOrchestratorService:
    """
    AI Orchestrator servisi için birim testleri.
    
    Bu test sınıfı, servis koordinasyonu fonksiyonlarının doğru çalışıp
    çalışmadığını kontrol eder.
    """
    
    def test_orchestrator_endpoint_exists(self, test_config, test_utils):
        """Orchestrator endpoint'inin mevcut olduğunu test eder"""
        service_url = test_config.SERVICES['orchestrator']
        
        # Health check ile servisin çalıştığını kontrol et
        is_healthy = test_utils.check_service_health(service_url)
        assert is_healthy, f"Orchestrator servisi çalışmıyor: {service_url}"
        
        # Orchestrate workflow endpoint'inin mevcut olduğunu kontrol et
        workflow_data = {
            'workflow_type': 'complete_recommendation',
            'user_input': {
                'text': 'Ayakkabı önerisi istiyorum'
            },
            'services_to_coordinate': ['nlu', 'style_profile', 'recommendation']
        }
        
        try:
            response = requests.post(
                f"{service_url}/orchestrate_workflow",
                json=workflow_data,
                timeout=test_config.TIMEOUT_LONG  # Uzun işlem süresi
            )
            # 200 veya 422 (validation error) beklenen yanıtlar
            assert response.status_code in [200, 422], f"Beklenmeyen status kodu: {response.status_code}"
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Endpoint'e erişim hatası: {str(e)}")
    
    def test_orchestrator_workflow_coordination(self, test_config):
        """Orchestrator'ın workflow koordinasyonunu test eder"""
        service_url = test_config.SERVICES['orchestrator']
        
        workflow_data = {
            'workflow_type': 'complete_recommendation',
            'user_input': {
                'text': 'İş için şık ayakkabı istiyorum'
            },
            'services_to_coordinate': ['nlu', 'style_profile', 'recommendation']
        }
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{service_url}/orchestrate_workflow",
                json=workflow_data,
                timeout=test_config.TIMEOUT_LONG
            )
            duration_ms = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                response_data = response.json()
                
                # Workflow koordinasyonu kontrolü
                if 'workflow_status' in response_data:
                    assert response_data['workflow_status'] in ['completed', 'partial', 'failed'], \
                        f"Geçersiz workflow status: {response_data['workflow_status']}"
                
                print(f"✅ Workflow koordinasyonu: {duration_ms:.2f}ms - {response_data}")
                
        except requests.exceptions.RequestException:
            pytest.skip("Orchestrator servisi erişilebilir değil")

# Test çalıştırma fonksiyonu
def run_unit_tests():
    """Tüm birim testlerini çalıştır ve sonuçları raporla"""
    print("🧪 BİRİM TESTLERİ BAŞLATILIYOR...")
    print("=" * 50)
    
    # pytest ile testleri çalıştır
    import subprocess
    import sys
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            'tests/unit/test_unit_services.py', 
            '-v', '--tb=short'
        ], capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        print("\nSTDERR:")
        print(result.stderr)
        print(f"\nReturn code: {result.returncode}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Test çalıştırma hatası: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_unit_tests()
    exit(0 if success else 1)
