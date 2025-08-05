# 🔄 AURA AI FEEDBACK LOOP - PROMPT ENGINEERING DEMO
# Geri Bildirim Analizi ve Öğrenme Optimizasyonu Test Sistemi

import asyncio
import json
import requests
from typing import Dict, List, Any
from datetime import datetime
import colorama
from colorama import Fore, Back, Style

# Colorama'yı başlat
colorama.init(autoreset=True)

class AuraFeedbackDemoTester:
    """
    AURA Feedback Loop servisini test etmek için interaktif demo sistemi.
    Farklı feedback türlerini test eder ve prompt engineering kalıplarını değerlendirir.
    """
    
    def __init__(self, base_url: str = "http://localhost:8007"):
        """Demo tester'ı başlat"""
        self.base_url = base_url
        self.session = requests.Session()
        
        print(f"{Fore.CYAN}🔄 AURA FEEDBACK LOOP PROMPT ENGINEERING DEMO{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Base URL: {base_url}{Style.RESET_ALL}")
        print("=" * 70)
    
    def print_section_header(self, title: str):
        """Bölüm başlığı yazdır"""
        print(f"\n{Back.BLUE}{Fore.WHITE} {title} {Style.RESET_ALL}")
        print("-" * 50)
    
    def print_success(self, message: str):
        """Başarı mesajı yazdır"""
        print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")
    
    def print_error(self, message: str):
        """Hata mesajı yazdır"""
        print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")
    
    def print_info(self, message: str):
        """Bilgi mesajı yazdır"""
        print(f"{Fore.CYAN}ℹ️  {message}{Style.RESET_ALL}")
    
    def print_json(self, data: Dict[str, Any], title: str = ""):
        """JSON verisini güzel formatta yazdır"""
        if title:
            print(f"{Fore.MAGENTA}📊 {title}:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{json.dumps(data, indent=2, ensure_ascii=False)}{Style.RESET_ALL}")
    
    def check_service_health(self) -> bool:
        """Servis sağlığını kontrol et"""
        self.print_section_header("SERVICE HEALTH CHECK")
        
        try:
            response = self.session.get(f"{self.base_url}/")
            
            if response.status_code == 200:
                health_data = response.json()
                self.print_success("Feedback Loop servisi çalışıyor!")
                
                print(f"{Fore.YELLOW}📋 Servis Bilgileri:{Style.RESET_ALL}")
                print(f"  • Versiyon: {health_data.get('version', 'N/A')}")
                print(f"  • Durum: {health_data.get('status', 'N/A')}")
                print(f"  • Açıklama: {health_data.get('description', 'N/A')}")
                
                if 'prompt_engineering_capabilities' in health_data:
                    print(f"{Fore.YELLOW}🧠 Prompt Engineering Yetenekleri:{Style.RESET_ALL}")
                    for key, value in health_data['prompt_engineering_capabilities'].items():
                        print(f"  • {key}: {value}")
                
                return True
            else:
                self.print_error(f"Servis erişilemiyor: HTTP {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.print_error("Servis bağlantısı kurulamadı. Servisin çalıştığından emin olun.")
            return False
        except Exception as e:
            self.print_error(f"Beklenmeyen hata: {e}")
            return False
    
    def test_feedback_analysis(self):
        """Feedback analiz endpoint'lerini test et"""
        self.print_section_header("FEEDBACK ANALYSIS TEST")
        
        # Test feedback örnekleri
        test_feedbacks = [
            {
                "name": "Olumsuz Genel Geri Bildirim",
                "feedback": {
                    "user_id": "user_123",
                    "recommendation_id": "rec_456",
                    "feedback_text": "Bu kombini hiç beğenmedim",
                    "feedback_rating": 2,
                    "context": {
                        "occasion": "work_meeting",
                        "weather": "rainy"
                    }
                },
                "expected_type": "negative_general"
            },
            {
                "name": "Renk Uyumsuzluğu",
                "feedback": {
                    "user_id": "user_456",
                    "recommendation_id": "rec_789",
                    "feedback_text": "Renkleri hiç uyumlu değil, kırmızı ile mor hiç yakışmıyor",
                    "feedback_rating": 1,
                    "context": {
                        "occasion": "date_night",
                        "style_preference": "elegant"
                    }
                },
                "expected_type": "color_dissatisfaction"
            },
            {
                "name": "Pozitif Geri Bildirim - Benzer İstek",
                "feedback": {
                    "user_id": "user_789",
                    "recommendation_id": "rec_123",
                    "feedback_text": "Bu kombini çok beğendim! Benzer önerilerde bulunabilir misiniz?",
                    "feedback_rating": 5,
                    "context": {
                        "occasion": "casual_daily",
                        "mood": "happy"
                    }
                },
                "expected_type": "request_similar"
            },
            {
                "name": "Uygunluk Sorunu",
                "feedback": {
                    "user_id": "user_321",
                    "recommendation_id": "rec_654",
                    "feedback_text": "Bu öneri bana uygun değildi, çok resmi bir etkinlik için fazla casual",
                    "feedback_rating": 2,
                    "context": {
                        "occasion": "formal_event",
                        "dress_code": "business_formal"
                    }
                },
                "expected_type": "occasion_inappropriate"
            }
        ]
        
        successful_tests = 0
        total_tests = len(test_feedbacks)
        
        for i, test_case in enumerate(test_feedbacks, 1):
            print(f"\n{Fore.YELLOW}🧪 Test {i}/{total_tests}: {test_case['name']}{Style.RESET_ALL}")
            print(f"Geri Bildirim: \"{test_case['feedback']['feedback_text']}\"")
            
            try:
                response = self.session.post(
                    f"{self.base_url}/feedback/analyze",
                    json=test_case['feedback']
                )
                
                if response.status_code == 200:
                    result = response.json()
                    classified_type = result['classification']['feedback_type']
                    confidence = result['confidence']
                    processing_time = result['processing_time']
                    
                    print(f"📊 Sınıflandırma: {Fore.BLUE}{classified_type}{Style.RESET_ALL}")
                    print(f"📈 Güven Skoru: {Fore.BLUE}{confidence:.2f}{Style.RESET_ALL}")
                    print(f"⏱️  İşlem Süresi: {Fore.BLUE}{processing_time:.2f}ms{Style.RESET_ALL}")
                    
                    # Check if classification matches expected
                    if classified_type == test_case['expected_type']:
                        self.print_success("Doğru sınıflandırma!")
                        successful_tests += 1
                    else:
                        self.print_error(f"Beklenen: {test_case['expected_type']}, Elde edilen: {classified_type}")
                    
                    # Show learning actions
                    if result['learning_actions']:
                        print(f"{Fore.MAGENTA}🎯 Öğrenme Aksiyonları:{Style.RESET_ALL}")
                        for action in result['learning_actions'][:2]:  # Show first 2 actions
                            print(f"  • {action['service']}: {action['action_type']}")
                
                else:
                    self.print_error(f"API hatası: HTTP {response.status_code}")
                    print(f"Hata detayı: {response.text}")
                    
            except Exception as e:
                self.print_error(f"Test hatası: {e}")
        
        # Test özeti
        print(f"\n{Back.GREEN}{Fore.WHITE} TEST ÖZETİ {Style.RESET_ALL}")
        print(f"Başarılı Testler: {successful_tests}/{total_tests}")
        print(f"Başarı Oranı: {(successful_tests/total_tests)*100:.1f}%")
        
        if successful_tests == total_tests:
            self.print_success("Tüm testler başarılı! 🎉")
        elif successful_tests >= total_tests * 0.8:
            print(f"{Fore.YELLOW}⚠️  Çoğu test başarılı, bazı iyileştirmeler gerekli{Style.RESET_ALL}")
        else:
            self.print_error("Birçok test başarısız, sistem kontrolü gerekli")
    
    def test_batch_analysis(self):
        """Batch feedback analizi test et"""
        self.print_section_header("BATCH ANALYSIS TEST")
        
        batch_feedbacks = [
            {
                "user_id": "batch_user_1",
                "recommendation_id": "batch_rec_1", 
                "feedback_text": "Güzel kombinasyon",
                "feedback_rating": 4
            },
            {
                "user_id": "batch_user_2",
                "recommendation_id": "batch_rec_2",
                "feedback_text": "Renkleri beğenmedim",
                "feedback_rating": 2
            },
            {
                "user_id": "batch_user_3", 
                "recommendation_id": "batch_rec_3",
                "feedback_text": "Mükemmel! Daha fazlası",
                "feedback_rating": 5
            }
        ]
        
        print(f"📦 {len(batch_feedbacks)} feedback'li batch test...")
        
        try:
            response = self.session.post(
                f"{self.base_url}/feedback/batch-analyze",
                json=batch_feedbacks
            )
            
            if response.status_code == 200:
                result = response.json()
                
                self.print_success("Batch analizi başarılı!")
                print(f"Batch ID: {result['batch_id']}")
                print(f"İşlenen Adet: {result['processed_count']}")
                print(f"Toplam Süre: {result['total_processing_time']:.2f}ms")
                print(f"Ortalama Süre: {result['average_processing_time']:.2f}ms")
                
                print(f"\n{Fore.MAGENTA}📊 Batch Sonuçları:{Style.RESET_ALL}")
                for i, item_result in enumerate(result['results'], 1):
                    print(f"  {i}. {item_result['classification']['feedback_type']} "
                          f"(güven: {item_result['confidence']:.2f})")
            
            else:
                self.print_error(f"Batch analizi hatası: HTTP {response.status_code}")
                print(response.text)
                
        except Exception as e:
            self.print_error(f"Batch test hatası: {e}")
    
    def test_learning_insights(self):
        """Learning insights endpoint'ini test et"""
        self.print_section_header("LEARNING INSIGHTS TEST")
        
        try:
            response = self.session.get(f"{self.base_url}/feedback/insights")
            
            if response.status_code == 200:
                insights = response.json()
                
                self.print_success("Learning insights alındı!")
                
                # General patterns
                if 'insights' in insights and 'general_patterns' in insights['insights']:
                    general = insights['insights']['general_patterns']
                    
                    print(f"\n{Fore.YELLOW}📈 Genel Pattern'ler:{Style.RESET_ALL}")
                    print(f"  • En Yaygın Feedback Türleri:")
                    for feedback_type in general.get('most_common_feedback_types', []):
                        print(f"    - {feedback_type['type']}: %{feedback_type['percentage']}")
                    
                    print(f"  • Kullanıcı Memnuniyet Trendi: {general.get('user_satisfaction_trend', 'N/A')}")
                    print(f"  • Öneri İyileştirmesi: {general.get('recommendation_improvement', 'N/A')}")
                
                # Color learning
                if 'insights' in insights and 'color_learning' in insights['insights']:
                    color = insights['insights']['color_learning']
                    
                    print(f"\n{Fore.YELLOW}🎨 Renk Öğrenmesi:{Style.RESET_ALL}")
                    print(f"  • Problemli Kombinasyonlar:")
                    for combo in color.get('problematic_combinations', []):
                        colors = ' + '.join(combo['colors'])
                        rate = combo['rejection_rate']
                        print(f"    - {colors}: %{rate*100:.0f} ret oranı")
                
                # Coordination performance
                if 'insights' in insights and 'coordination_performance' in insights['insights']:
                    coord = insights['insights']['coordination_performance']
                    
                    print(f"\n{Fore.YELLOW}🔄 Koordinasyon Performansı:{Style.RESET_ALL}")
                    print(f"  • Başarı Oranı: %{coord.get('service_update_success_rate', 0)*100:.0f}")
                    print(f"  • Ortalama Süre: {coord.get('average_coordination_time', 'N/A')}")
                    print(f"  • Başarısız Güncellemeler: {coord.get('failed_updates', 'N/A')}")
            
            else:
                self.print_error(f"Insights alınamadı: HTTP {response.status_code}")
                
        except Exception as e:
            self.print_error(f"Insights test hatası: {e}")
    
    def test_analytics(self):
        """Analytics endpoint'ini test et"""
        self.print_section_header("ANALYTICS TEST")
        
        try:
            response = self.session.get(f"{self.base_url}/feedback/analytics")
            
            if response.status_code == 200:
                analytics = response.json()
                
                self.print_success("Analytics alındı!")
                
                if 'analytics' in analytics:
                    data = analytics['analytics']
                    
                    # System performance
                    if 'system_performance' in data:
                        perf = data['system_performance']
                        print(f"\n{Fore.YELLOW}⚡ Sistem Performansı:{Style.RESET_ALL}")
                        print(f"  • Toplam İşlenen Feedback: {perf.get('total_feedback_processed', 'N/A'):,}")
                        print(f"  • Ortalama İşlem Süresi: {perf.get('avg_processing_time', 'N/A')}")
                        print(f"  • Sınıflandırma Doğruluğu: %{perf.get('classification_accuracy', 0)*100:.0f}")
                    
                    # Prompt engineering metrics
                    if 'prompt_engineering_metrics' in data:
                        prompt = data['prompt_engineering_metrics']
                        print(f"\n{Fore.YELLOW}🧠 Prompt Engineering Metrikleri:{Style.RESET_ALL}")
                        print(f"  • Persona Etkinliği: %{prompt.get('persona_effectiveness', 0)*100:.0f}")
                        print(f"  • Recipe Tamamlanma: %{prompt.get('recipe_completion_rate', 0)*100:.0f}")
                        print(f"  • Template Tutarlılığı: %{prompt.get('template_consistency', 0)*100:.0f}")
                        print(f"  • Bağlam Uygunluğu: %{prompt.get('context_relevance', 0)*100:.0f}")
                        print(f"  • Talimat Takibi: %{prompt.get('instruction_following', 0)*100:.0f}")
                    
                    # Real-time stats
                    if 'real_time_stats' in data:
                        realtime = data['real_time_stats']
                        print(f"\n{Fore.YELLOW}📊 Gerçek Zamanlı İstatistikler:{Style.RESET_ALL}")
                        print(f"  • Saatlik Feedback: {realtime.get('feedback_per_hour', 'N/A')}")
                        print(f"  • Aktif Öğrenme Oturumları: {realtime.get('active_learning_sessions', 'N/A')}")
                        print(f"  • Bekleyen Model Güncellemeleri: {realtime.get('pending_model_updates', 'N/A')}")
                        print(f"  • Sistem Yükü: %{realtime.get('system_load', 0)*100:.0f}")
            
            else:
                self.print_error(f"Analytics alınamadı: HTTP {response.status_code}")
                
        except Exception as e:
            self.print_error(f"Analytics test hatası: {e}")
    
    def test_prompt_patterns(self):
        """Prompt pattern test endpoint'ini kullan"""
        self.print_section_header("PROMPT PATTERNS TEST")
        
        custom_test = {
            "user_id": "pattern_test_user",
            "recommendation_id": "pattern_test_rec",
            "feedback_text": "Bu elbise güzel ama ayakkabılar hiç uymamış, farklı renk olsaydı daha iyi olurdu"
        }
        
        print(f"🧪 Özel test feedback'i: \"{custom_test['feedback_text']}\"")
        
        try:
            response = self.session.post(
                f"{self.base_url}/feedback/test-patterns",
                json=custom_test
            )
            
            if response.status_code == 200:
                result = response.json()
                
                self.print_success("Prompt pattern testi başarılı!")
                
                print(f"\n{Fore.YELLOW}📋 Test Sonuçları:{Style.RESET_ALL}")
                for test_result in result['test_results']:
                    print(f"  • {test_result['test_case']}: {test_result.get('classified_as', 'N/A')} "
                          f"(güven: {test_result.get('confidence', 0):.2f})")
                    
                    if 'match' in test_result:
                        status = "✅" if test_result['match'] else "❌"
                        print(f"    {status} Beklenen: {test_result.get('expected', 'N/A')}")
                
                accuracy = result.get('overall_accuracy', 0)
                print(f"\n📈 Genel Doğruluk: %{accuracy*100:.1f}")
                print(f"🔧 Prompt Engine Durumu: {result.get('prompt_engine_status', 'N/A')}")
            
            else:
                self.print_error(f"Pattern test hatası: HTTP {response.status_code}")
                
        except Exception as e:
            self.print_error(f"Pattern test hatası: {e}")
    
    def run_comprehensive_test(self):
        """Kapsamlı test suite'ini çalıştır"""
        print(f"{Back.MAGENTA}{Fore.WHITE} AURA FEEDBACK LOOP - COMPREHENSIVE TEST SUITE {Style.RESET_ALL}")
        print(f"Test başlangıç zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Health check
        if not self.check_service_health():
            self.print_error("Servis sağlık kontrolü başarısız. Testler durduruluyor.")
            return
        
        # Run all tests
        self.test_feedback_analysis()
        self.test_batch_analysis()
        self.test_learning_insights()
        self.test_analytics()
        self.test_prompt_patterns()
        
        print(f"\n{Back.GREEN}{Fore.WHITE} COMPREHENSIVE TEST COMPLETED {Style.RESET_ALL}")
        print(f"Test bitiş zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.print_info("Tüm testler tamamlandı! Sonuçları yukarıda inceleyebilirsiniz.")

def main():
    """Ana demo fonksiyonu"""
    print(f"{Fore.CYAN}🚀 AURA AI Feedback Loop Demo'ya Hoş Geldiniz!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Bu demo, AURA'nın feedback loop prompt engineering sistemini test eder.{Style.RESET_ALL}")
    print()
    
    # Demo tester'ı başlat
    demo = AuraFeedbackDemoTester()
    
    while True:
        print(f"\n{Fore.CYAN}📋 MENÜ SEÇENEKLERİ:{Style.RESET_ALL}")
        print("1. 🏥 Servis Sağlık Kontrolü")
        print("2. 🧪 Feedback Analizi Testi")
        print("3. 📦 Batch Analizi Testi")
        print("4. 📊 Learning Insights Testi")
        print("5. 📈 Analytics Testi")
        print("6. 🧠 Prompt Patterns Testi")
        print("7. 🎯 Kapsamlı Test Suite")
        print("0. ❌ Çıkış")
        
        try:
            choice = input(f"\n{Fore.YELLOW}Seçiminiz (0-7): {Style.RESET_ALL}").strip()
            
            if choice == "0":
                print(f"{Fore.CYAN}👋 Demo'dan çıkılıyor...{Style.RESET_ALL}")
                break
            elif choice == "1":
                demo.check_service_health()
            elif choice == "2":
                demo.test_feedback_analysis()
            elif choice == "3":
                demo.test_batch_analysis()
            elif choice == "4":
                demo.test_learning_insights()
            elif choice == "5":
                demo.test_analytics()
            elif choice == "6":
                demo.test_prompt_patterns()
            elif choice == "7":
                demo.run_comprehensive_test()
            else:
                print(f"{Fore.RED}❌ Geçersiz seçim. Lütfen 0-7 arasında bir sayı girin.{Style.RESET_ALL}")
                
        except KeyboardInterrupt:
            print(f"\n{Fore.CYAN}👋 Demo iptal edildi.{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}❌ Beklenmeyen hata: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
