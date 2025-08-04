#!/usr/bin/env python3
"""
🌟 AURA AI Sistem Demo Scripti 🌟
Ultra-clean AI mikroservisleri için interaktif demo

Bu script AURA AI sisteminin tüm yeteneklerini gösterir:
- 7 AI mikroservisi
- Gerçek zamanlı AI analizi
- Stil DNA profilleme
- Akıllı kombinasyon önerileri
"""

import json
import time
import requests
from datetime import datetime
from colorama import init, Fore, Back, Style

# Colorama'yı başlat
init(autoreset=True)

class AuraAIDemo:
    def __init__(self):
        self.base_url = "http://localhost"
        self.services = {
            "image_processing": 8001,
            "nlu_service": 8002,
            "style_profile": 8003,
            "combination_engine": 8004,
            "recommendation_engine": 8005,
            "orchestrator": 8006,
            "feedback_loop": 8007
        }
    
    def print_header(self):
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.YELLOW}🤖 AURA AI SİSTEMİ - ULTRA-CLEAN AI DEMO 🤖")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}⚡ 7 AI Mikroservisi | Production Ready | Enterprise Grade")
        print(f"{Fore.WHITE}🕒 Demo Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    def check_services(self):
        print(f"{Fore.CYAN}🔍 SERVİS DURUMU KONTROLÜ:")
        print("-" * 50)
        
        healthy_services = 0
        for service_name, port in self.services.items():
            try:
                response = requests.get(f"{self.base_url}:{port}", timeout=5)
                if response.status_code == 200:
                    print(f"{Fore.GREEN}✅ {service_name:20} Port {port} - ÇALIŞIYOR")
                    healthy_services += 1
                else:
                    print(f"{Fore.RED}❌ {service_name:20} Port {port} - HATA")
            except:
                print(f"{Fore.RED}❌ {service_name:20} Port {port} - ERİŞİLEMİYOR")
        
        print(f"\n{Fore.YELLOW}📊 Durum: {healthy_services}/{len(self.services)} servis aktif")
        return healthy_services == len(self.services)
    
    def demo_combination_engine(self):
        print(f"\n{Fore.MAGENTA}🧠 AI COMBINATION ENGINE DEMO")
        print("-" * 40)
        
        # Test verisi
        demo_request = {
            "user_id": "demo_user_2025",
            "context": "business",
            "occasion": "önemli toplantı"
        }
        
        try:
            print(f"{Fore.CYAN}📤 İstek gönderiliyor...")
            print(f"   User ID: {demo_request['user_id']}")
            print(f"   Context: {demo_request['context']}")
            print(f"   Occasion: {demo_request['occasion']}")
            
            response = requests.post(
                f"{self.base_url}:8004/generate-combination",
                json=demo_request,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"\n{Fore.GREEN}🎉 AI KOMBINASYON ÜRETİLDİ!")
                print(f"   Kombinasyon ID: {result.get('combination_id', 'N/A')}")
                print(f"   Güven Skoru: {result.get('confidence_score', 0):.2f}")
                
                if 'combination_items' in result:
                    print(f"\n{Fore.YELLOW}👔 ÖNERİLEN KIYAFETLER:")
                    for i, item in enumerate(result['combination_items'][:3], 1):
                        print(f"   {i}. {item.get('item_type', 'N/A')} - {item.get('color', 'N/A')}")
                
                if 'color_harmony_analysis' in result:
                    harmony = result['color_harmony_analysis']
                    print(f"\n{Fore.CYAN}🎨 RENK UYUMU ANALİZİ:")
                    print(f"   Uyum Skoru: {harmony.get('harmony_score', 0):.2f}")
                    print(f"   Renk Paleti: {', '.join(harmony.get('color_palette', []))}")
                
                return True
            else:
                print(f"{Fore.RED}❌ Hata: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ Bağlantı hatası: {str(e)}")
            return False
    
    def demo_image_processing(self):
        print(f"\n{Fore.BLUE}📸 IMAGE PROCESSING AI DEMO")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.base_url}:8001", timeout=5)
            if response.status_code == 200:
                result = response.json()
                print(f"{Fore.GREEN}✨ Görsel AI Sistemi Aktif!")
                print(f"   Servis: {result.get('service', 'N/A')}")
                print(f"   Versiyon: {result.get('version', 'N/A')}")
                
                if 'ai_capabilities' in result:
                    caps = result['ai_capabilities']
                    print(f"\n{Fore.YELLOW}🧠 AI YETENEKLERİ:")
                    for capability, description in caps.items():
                        print(f"   • {capability}: {description}")
                
                return True
            else:
                print(f"{Fore.RED}❌ Hata: {response.status_code}")
                return False
        except Exception as e:
            print(f"{Fore.RED}❌ Bağlantı hatası: {str(e)}")
            return False
    
    def demo_nlu_service(self):
        print(f"\n{Fore.GREEN}💬 NLU AI DEMO")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.base_url}:8002", timeout=5)
            if response.status_code == 200:
                result = response.json()
                print(f"{Fore.GREEN}🤖 Doğal Dil AI Sistemi Aktif!")
                print(f"   Açıklama: {result.get('description', 'N/A')}")
                
                if 'transformer_capabilities' in result:
                    caps = result['transformer_capabilities']
                    print(f"\n{Fore.YELLOW}🧠 TRANSFORMER YETENEKLERİ:")
                    for model, description in caps.items():
                        print(f"   • {model.upper()}: {description}")
                
                return True
            else:
                print(f"{Fore.RED}❌ Hata: {response.status_code}")
                return False
        except Exception as e:
            print(f"{Fore.RED}❌ Bağlantı hatası: {str(e)}")
            return False
    
    def performance_summary(self):
        print(f"\n{Fore.CYAN}📊 SİSTEM PERFORMANS ÖZETİ")
        print("-" * 50)
        
        # Basit performans metrikleri
        start_time = time.time()
        successful_tests = 0
        total_tests = 0
        
        # Her servisi test et
        for service_name, port in self.services.items():
            total_tests += 1
            try:
                test_start = time.time()
                response = requests.get(f"{self.base_url}:{port}", timeout=2)
                response_time = (time.time() - test_start) * 1000
                
                if response.status_code == 200:
                    successful_tests += 1
                    status = f"{Fore.GREEN}OK"
                else:
                    status = f"{Fore.RED}HATA"
                
                print(f"   {service_name:20} - {status} ({response_time:.0f}ms)")
                
            except:
                print(f"   {service_name:20} - {Fore.RED}ERİŞİLEMİYOR")
        
        total_time = (time.time() - start_time) * 1000
        success_rate = (successful_tests / total_tests) * 100
        
        print(f"\n{Fore.YELLOW}📈 ÖZET:")
        print(f"   Başarı Oranı: {success_rate:.1f}%")
        print(f"   Toplam Test Süresi: {total_time:.0f}ms")
        print(f"   Aktif Servis: {successful_tests}/{total_tests}")
    
    def run_full_demo(self):
        """Tam demo'yu çalıştır"""
        self.print_header()
        
        # Servis durumu kontrolü
        if not self.check_services():
            print(f"\n{Fore.RED}⚠️  Bazı servisler çalışmıyor. Lütfen 'docker-compose up -d' çalıştırın.")
            return
        
        print(f"\n{Fore.GREEN}🎉 TÜM SERVİSLER AKTIF! Demo başlıyor...")
        time.sleep(2)
        
        # AI servislerini demo et
        self.demo_image_processing()
        time.sleep(1)
        
        self.demo_nlu_service()
        time.sleep(1)
        
        self.demo_combination_engine()
        time.sleep(1)
        
        # Performans özeti
        self.performance_summary()
        
        # Kapanış
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.YELLOW}🏆 AURA AI DEMO TAMAMLANDI!")
        print(f"{Fore.GREEN}✨ Ultra-clean AI sistemi başarıyla çalışıyor!")
        print(f"{Fore.WHITE}🌐 Swagger UI: http://localhost:8006/docs")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        demo = AuraAIDemo()
        demo.run_full_demo()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}🛑 Demo kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Demo hatası: {str(e)}")
