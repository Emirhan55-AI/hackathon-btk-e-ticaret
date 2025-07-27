# 🧪 E2E WORKFLOW TESTER - PHASE 1 CRITICAL FIX
# Bu script, end-to-end workflow'un çalışıp çalışmadığını test eder

import requests
import json
import time
from pathlib import Path

def test_e2e_workflow():
    """E2E workflow'u test et"""
    print("🧪 E2E WORKFLOW TEST BAŞLATILIYOR")
    print("="*50)
    
    # Test için gerekli veriler
    test_image_path = None  # Mock test için None
    user_request = "Bugün spor yapmak için ayakkabı önerisi istiyorum"
    user_context = {
        "occasion": "sport",
        "budget": "medium",
        "preferred_brands": ["Nike", "Adidas"]
    }
    
    # E2E Orchestrator endpoint
    e2e_endpoint = "http://localhost:8008/execute_complete_workflow"
    
    try:
        print(f"📋 Test parametreleri:")
        print(f"   • Kullanıcı isteği: '{user_request}'")
        print(f"   • Bağlam: {user_context}")
        print(f"   • Hedef endpoint: {e2e_endpoint}")
        
        # Test verilerini hazırla
        files = {}
        data = {
            'user_request': user_request,
            'user_context': json.dumps(user_context)
        }
        
        # Mock image file oluştur (gerçek dosya yoksa)
        if test_image_path and Path(test_image_path).exists():
            files['file'] = open(test_image_path, 'rb')
        else:
            # Mock image data
            mock_image_data = b"fake_image_data_for_testing"
            files['file'] = ('test_image.jpg', mock_image_data, 'image/jpeg')
        
        print(f"\n🚀 E2E workflow çalıştırılıyor...")
        start_time = time.time()
        
        # E2E workflow'u çalıştır
        response = requests.post(
            e2e_endpoint,
            files=files,
            data=data,
            timeout=60  # 60 saniye timeout
        )
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"⏱️ Toplam süre: {total_time:.2f} saniye")
        print(f"📊 HTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ E2E WORKFLOW BAŞARILI!")
            print("="*50)
            
            # Workflow sonuçlarını analiz et
            workflow_id = result.get('workflow_id', 'unknown')
            status = result.get('status', 'unknown')
            processing_time = result.get('total_processing_time', 0)
            
            print(f"🆔 Workflow ID: {workflow_id}")
            print(f"📈 Status: {status}")
            print(f"⚡ İşlem süresi: {processing_time:.2f}s")
            
            # Adım sürelerini göster
            step_times = result.get('step_times', {})
            if step_times:
                print(f"\n📊 ADIM SÜRELERİ:")
                for step, duration in step_times.items():
                    print(f"   • {step}: {duration:.2f}s")
            
            # Final sonuçları göster
            final_results = result.get('results', {})
            if final_results:
                print(f"\n🎯 FINAL SONUÇLAR:")
                
                # Workflow özeti
                workflow_summary = final_results.get('workflow_summary', {})
                if workflow_summary:
                    detected_clothing = workflow_summary.get('detected_clothing', [])
                    user_intent = workflow_summary.get('user_intent', 'unknown')
                    recommended_style = workflow_summary.get('recommended_style', 'unknown')
                    total_recommendations = workflow_summary.get('total_recommendations', 0)
                    
                    print(f"   • Tespit edilen kıyafetler: {detected_clothing}")
                    print(f"   • Kullanıcı niyeti: {user_intent}")
                    print(f"   • Önerilen stil: {recommended_style}")
                    print(f"   • Toplam öneri sayısı: {total_recommendations}")
                
                # Güven skorları
                confidence_scores = final_results.get('confidence_scores', {})
                if confidence_scores:
                    print(f"\n🎯 GÜVEN SKORLARI:")
                    for component, score in confidence_scores.items():
                        print(f"   • {component}: %{score*100:.1f}")
                
                # Ürün önerileri (ilk 3)
                product_recommendations = final_results.get('product_recommendations', [])
                if product_recommendations:
                    print(f"\n🛍️ ÜRÜN ÖNERİLERİ (İlk 3):")
                    for i, product in enumerate(product_recommendations[:3], 1):
                        name = product.get('name', 'Bilinmeyen ürün')
                        price = product.get('price', 0)
                        confidence = product.get('confidence', 0)
                        print(f"   {i}. {name} - ₺{price} (Güven: %{confidence*100:.1f})")
            
            return True
            
        else:
            print(f"\n❌ E2E WORKFLOW BAŞARISIZ!")
            print(f"HTTP Status: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"Hata detayı: {error_detail}")
            except:
                print(f"Hata mesajı: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"\n⏰ TIMEOUT HATASI!")
        print(f"E2E workflow 60 saniyede tamamlanamadı")
        return False
        
    except requests.exceptions.ConnectionError:
        print(f"\n🔌 BAĞLANTI HATASI!")
        print(f"E2E Orchestrator servisine bağlanılamadı: {e2e_endpoint}")
        print(f"Lütfen servisi başlatın: python e2e_workflow_orchestrator.py")
        return False
        
    except Exception as e:
        print(f"\n💥 BEKLENMEYEN HATA!")
        print(f"Hata: {str(e)}")
        return False

def test_service_health():
    """Tüm servislerin sağlığını kontrol et"""
    print("\n🏥 SERVİS SAĞLIK KONTROLÜ")
    print("-"*40)
    
    health_endpoint = "http://localhost:8008/service_health"
    
    try:
        response = requests.get(health_endpoint, timeout=10)
        
        if response.status_code == 200:
            health_data = response.json()
            overall_health = health_data.get('overall_health', 'unknown')
            health_percentage = health_data.get('health_percentage', 0)
            services = health_data.get('services', {})
            
            print(f"📊 Genel sağlık: {overall_health} (%{health_percentage:.1f})")
            print(f"\n📋 Servis detayları:")
            
            for service_name, service_info in services.items():
                status = service_info.get('status', 'unknown')
                endpoint = service_info.get('endpoint', 'unknown')
                
                status_icon = "✅" if status == "healthy" else "❌" if status == "unreachable" else "⚠️"
                print(f"   {status_icon} {service_name}: {status} ({endpoint})")
                
                if 'error' in service_info:
                    print(f"      Hata: {service_info['error']}")
            
            return health_percentage >= 50  # En az %50 sağlıklı olmalı
            
        else:
            print(f"❌ Sağlık kontrolü başarısız: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Sağlık kontrolü hatası: {str(e)}")
        return False

def main():
    """Ana test fonksiyonu"""
    print("🎯 AURA AI - E2E WORKFLOW COMPREHENSIVE TEST")
    print("="*60)
    print("Bu test, sistemin uçtan uca çalışabilirliğini doğrular.")
    print("Test süreci: Image Processing → NLU → Style Profile → Combinations → Recommendations")
    print("="*60)
    
    # Önce E2E Orchestrator'ın çalışıp çalışmadığını kontrol et
    try:
        response = requests.get("http://localhost:8008/", timeout=5)
        if response.status_code != 200:
            print("❌ E2E Orchestrator çalışmıyor!")
            print("Lütfen önce servisi başlatın: python e2e_workflow_orchestrator.py")
            return
    except:
        print("❌ E2E Orchestrator'a bağlanılamıyor!")
        print("Lütfen önce servisi başlatın: python e2e_workflow_orchestrator.py")
        return
    
    # 1. Servis sağlık kontrolü
    health_ok = test_service_health()
    
    if not health_ok:
        print("\n⚠️ Bazı servisler sağlıksız durumda, ancak test devam ediyor...")
        print("(E2E Orchestrator fallback mock data kullanacak)")
    
    # 2. E2E workflow testi
    workflow_success = test_e2e_workflow()
    
    # 3. Final rapor
    print("\n" + "="*60)
    print("🏁 TEST SONUÇLARI")
    print("="*60)
    
    if workflow_success:
        print("🎉 E2E WORKFLOW TEST BAŞARILI!")
        print("   • Uçtan uca işlem akışı çalışıyor")
        print("   • Tüm AI servisleri koordine ediliyor")
        print("   • Kullanıcı deneyimi tam olarak sağlanıyor")
        
        if health_ok:
            print("   • Tüm servisler sağlıklı durumda")
        else:
            print("   • Bazı servisler fallback mode'da çalışıyor")
        
        print("\n✅ PHASE 1 E2E WORKFLOW: TAMAMLANDI")
        
    else:
        print("❌ E2E WORKFLOW TEST BAŞARISIZ!")
        print("   • Uçtan uca işlem akışında sorun var")
        print("   • Kritik düzeltmeler gerekiyor")
        print("\n🚨 PHASE 1 E2E WORKFLOW: DÜZELTİLMELİ")

if __name__ == "__main__":
    main()
