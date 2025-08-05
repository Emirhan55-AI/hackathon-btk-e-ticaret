# 🎯 AURA AI - PROMPT ENGINEERING NLU DEMO
# Gelişmiş Doğal Dil Anlama Sistemi - Interaktif Demo

import requests
import json
import time
from typing import Dict, Any
import colorama
from colorama import Fore, Back, Style

# Initialize colorama for colored output
colorama.init()

class PromptEngineeringNLUDemo:
    """
    AURA AI Prompt Engineering NLU servisinin interaktif demo sistemi.
    
    Bu demo, beş temel prompt kalıbının nasıl çalıştığını gösterir:
    1. PERSONA: Moda uzmanı AI kişiliği
    2. RECIPE: Analiz sürecinin adımları
    3. TEMPLATE: Yapılandırılmış çıktı formatı  
    4. CONTEXT: Durum-bazlı analiz
    5. INSTRUCTION: Görev-spesifik talimatlar
    """
    
    def __init__(self, base_url: str = "http://localhost:8002"):
        """Demo sistemini başlat"""
        self.base_url = base_url
        self.session_count = 0
        
        print(f"{Fore.CYAN}{'=' * 80}")
        print(f"{Fore.CYAN}🎯 AURA AI - PROMPT ENGINEERING NLU DEMO")
        print(f"{Fore.CYAN}Gelişmiş Doğal Dil Anlama ve Moda AI Sistemi")
        print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}")
        
        # Test connection
        self.test_connection()
    
    def test_connection(self):
        """Servise bağlantıyı test et"""
        
        print(f"\n{Fore.YELLOW}🔗 NLU servisine bağlanılıyor...{Style.RESET_ALL}")
        
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                print(f"{Fore.GREEN}✅ Bağlantı başarılı!")
                print(f"   📍 Service: {data.get('service', 'Unknown')}")
                print(f"   📊 Phase: {data.get('phase', 'Unknown')}")
                print(f"   🧠 Version: {data.get('version', 'Unknown')}{Style.RESET_ALL}")
                
                # Check prompt engineering availability
                pe_status = data.get('systems_status', {}).get('prompt_engineering', 'unknown')
                if pe_status == 'active':
                    print(f"{Fore.GREEN}   🎯 Prompt Engineering: Aktif{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}   ⚠️ Prompt Engineering: {pe_status}{Style.RESET_ALL}")
                
            else:
                print(f"{Fore.RED}❌ Bağlantı hatası: HTTP {response.status_code}{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}❌ Bağlantı hatası: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 NLU servisinin çalıştığından emin olun: python main.py{Style.RESET_ALL}")
    
    def show_prompt_patterns_info(self):
        """Prompt kalıpları hakkında bilgi göster"""
        
        print(f"\n{Fore.MAGENTA}📋 PROMPT PATTERNS BİLGİSİ{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'-' * 50}{Style.RESET_ALL}")
        
        try:
            response = requests.get(f"{self.base_url}/prompt_patterns_info")
            
            if response.status_code == 200:
                data = response.json()
                
                patterns = data.get("prompt_patterns", {})
                print(f"\n{Fore.CYAN}🧠 PROMPT KALIPLARIMIZ:{Style.RESET_ALL}")
                
                for pattern_name, pattern_info in patterns.items():
                    print(f"\n{Fore.YELLOW}   {pattern_name.upper()}:")
                    print(f"   📝 {pattern_info.get('description', 'N/A')}")
                    print(f"   🎯 Amaç: {pattern_info.get('purpose', 'N/A')}{Style.RESET_ALL}")
                
                # Supported features
                intents = data.get("supported_intents", [])
                contexts = data.get("supported_contexts", [])
                languages = data.get("fashion_domain_features", {}).get("multilingual_support", [])
                
                print(f"\n{Fore.GREEN}🎯 DESTEKLENEN ÖZELLIKLER:")
                print(f"   Intent Türleri: {len(intents)} ({', '.join(intents[:3])}...)")
                print(f"   Bağlam Türleri: {len(contexts)} ({', '.join(contexts[:3])}...)")
                print(f"   Diller: {', '.join(languages)}{Style.RESET_ALL}")
                
            else:
                print(f"{Fore.RED}❌ Bilgi alınamadı: HTTP {response.status_code}{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}❌ Hata: {e}{Style.RESET_ALL}")
    
    def analyze_user_text(self, text: str, language: str = "tr", context_hint: str = None):
        """Kullanıcı metnini prompt patterns ile analiz et"""
        
        self.session_count += 1
        
        print(f"\n{Fore.BLUE}{'=' * 60}")
        print(f"{Fore.BLUE}🔍 ANALİZ #{self.session_count}: PROMPT ENGINEERING{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{'=' * 60}{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}📝 Girdi: \"{text}\"")
        print(f"🌍 Dil: {language}")
        if context_hint:
            print(f"💡 Bağlam İpucu: {context_hint}")
        print(f"{Style.RESET_ALL}")
        
        try:
            # Prepare request
            request_data = {
                "text": text,
                "language": language,
                "analysis_method": "prompt_patterns",
                "context_hint": context_hint,
                "enable_entity_extraction": True,
                "enable_fashion_reasoning": True,
                "return_explanations": True
            }
            
            # Send request and measure time
            print(f"{Fore.YELLOW}⏳ Analiz yapılıyor...{Style.RESET_ALL}")
            start_time = time.time()
            
            response = requests.post(
                f"{self.base_url}/analyze_with_prompt_patterns",
                json=request_data,
                headers={"Content-Type": "application/json"}
            )
            
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Display results step by step
                self._display_analysis_results(data, processing_time)
                
                return data
                
            else:
                print(f"{Fore.RED}❌ Analiz hatası: HTTP {response.status_code}{Style.RESET_ALL}")
                return None
                
        except Exception as e:
            print(f"{Fore.RED}❌ Analiz hatası: {e}{Style.RESET_ALL}")
            return None
    
    def _display_analysis_results(self, data: Dict[str, Any], processing_time: float):
        """Analiz sonuçlarını güzel formatta göster"""
        
        # 1. Intent Analysis
        intent_analysis = data.get("intent_analysis", {})
        detected_intent = intent_analysis.get("intent", "unknown")
        intent_confidence = intent_analysis.get("confidence", 0.0)
        
        print(f"\n{Fore.GREEN}🎯 INTENT ANALİZİ:")
        print(f"   Tespit Edilen Amaç: {detected_intent}")
        print(f"   Güven Skoru: {intent_confidence:.2f}{Style.RESET_ALL}")
        
        # 2. Context Analysis
        context_analysis = data.get("context_analysis", {})
        detected_context = context_analysis.get("context", "unknown")
        context_confidence = context_analysis.get("confidence", 0.0)
        
        print(f"\n{Fore.CYAN}🌍 BAĞLAM ANALİZİ:")
        print(f"   Tespit Edilen Bağlam: {detected_context}")
        print(f"   Güven Skoru: {context_confidence:.2f}{Style.RESET_ALL}")
        
        # 3. Entity Extraction
        entity_extraction = data.get("entity_extraction", {})
        entities = entity_extraction.get("entities", {})
        
        print(f"\n{Fore.MAGENTA}🏷️ ÖĞE ÇIKARIMI:")
        clothing_items = entities.get("clothing_items", [])
        colors = entities.get("colors", [])
        time_refs = entities.get("time_references", [])
        
        if clothing_items:
            print(f"   Kıyafet Eşyaları: {', '.join(clothing_items)}")
        if colors:
            print(f"   Renkler: {', '.join(colors)}")
        if time_refs:
            print(f"   Zaman Referansları: {', '.join(time_refs)}")
        
        if not any([clothing_items, colors, time_refs]):
            print(f"   (Özel öğe bulunamadı)")
        print(f"{Style.RESET_ALL}")
        
        # 4. Fashion Reasoning
        fashion_reasoning = data.get("fashion_reasoning", {})
        recommendations = fashion_reasoning.get("recommendations", [])
        
        if recommendations:
            print(f"\n{Fore.YELLOW}💡 MODA ÖNERİLERİ:")
            for rec in recommendations[:3]:  # Show top 3
                print(f"   • {rec}")
            print(f"{Style.RESET_ALL}")
        
        # 5. Next Actions
        next_actions = data.get("next_actions", [])
        if next_actions:
            print(f"\n{Fore.BLUE}🔄 ÖNERİLEN SONRAKI İŞLEMLER:")
            for action in next_actions:
                action_name = action.replace("_", " ").title()
                print(f"   • {action_name}")
            print(f"{Style.RESET_ALL}")
        
        # 6. Overall Confidence & Performance
        overall_confidence = data.get("confidence_overall", 0.0)
        print(f"\n{Fore.WHITE}{Back.BLUE} GENEL SONUÇ {Style.RESET_ALL}")
        print(f"{Fore.GREEN}📊 Genel Güven Skoru: {overall_confidence:.2f}")
        print(f"⏱️ İşlem Süresi: {processing_time:.3f} saniye{Style.RESET_ALL}")
    
    def run_predefined_examples(self):
        """Önceden tanımlanmış örnekleri çalıştır"""
        
        examples = [
            {
                "name": "İş Kıyafeti Önerisi",
                "text": "Yarın önemli bir sunumum var, ne giysem iyi olur?",
                "language": "tr",
                "context_hint": "work_office"
            },
            {
                "name": "Günlük Kombinasyon",
                "text": "Bu mavi gömlek hangi pantolon ile güzel durur?",
                "language": "tr",
                "context_hint": "casual_daily"
            },
            {
                "name": "Parti Hazırlığı",
                "text": "Bu akşam arkadaşlarımla partiye gidiyorum, şık gözükmek istiyorum",
                "language": "tr",
                "context_hint": "social_party"
            },
            {
                "name": "English Style Query",
                "text": "I need something elegant but comfortable for a dinner date",
                "language": "en",
                "context_hint": "date_romantic"
            }
        ]
        
        print(f"\n{Fore.CYAN}🎭 ÖNCEDEFİNİ ÖRNEKLER{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-' * 50}{Style.RESET_ALL}")
        
        for i, example in enumerate(examples, 1):
            print(f"\n{Fore.YELLOW}{i}. {example['name']}{Style.RESET_ALL}")
            input(f"{Fore.WHITE}Devam etmek için Enter'a basın...{Style.RESET_ALL}")
            
            self.analyze_user_text(
                text=example["text"],
                language=example["language"],
                context_hint=example["context_hint"]
            )
            
            if i < len(examples):
                time.sleep(1)  # Brief pause between examples
    
    def interactive_mode(self):
        """Interaktif mod - kullanıcı kendi metinlerini girebilir"""
        
        print(f"\n{Fore.GREEN}💬 İNTERAKTİF MOD{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'-' * 30}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Moda ile ilgili sorularınızı yazın. Çıkmak için 'exit' yazın.{Style.RESET_ALL}")
        
        while True:
            try:
                # Get user input
                user_text = input(f"\n{Fore.WHITE}Soru: {Style.RESET_ALL}").strip()
                
                if not user_text:
                    continue
                    
                if user_text.lower() in ['exit', 'quit', 'çıkış', 'çık']:
                    print(f"{Fore.YELLOW}👋 Demo sonlandırılıyor...{Style.RESET_ALL}")
                    break
                
                # Optional context hint
                context_hint = input(f"{Fore.CYAN}Bağlam ipucu (opsiyonel - iş/günlük/parti/vs): {Style.RESET_ALL}").strip()
                if not context_hint:
                    context_hint = None
                
                # Analyze
                self.analyze_user_text(user_text, "tr", context_hint)
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}👋 Demo sonlandırılıyor...{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Hata: {e}{Style.RESET_ALL}")
    
    def run_demo(self):
        """Ana demo fonksiyonu"""
        
        while True:
            print(f"\n{Fore.CYAN}🎯 DEMO MENÜSÜ{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'-' * 20}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}1. 📋 Prompt Kalıpları Bilgisi")
            print(f"2. 🎭 Örnek Analizler") 
            print(f"3. 💬 İnteraktif Mod")
            print(f"4. 🚪 Çıkış{Style.RESET_ALL}")
            
            try:
                choice = input(f"\n{Fore.YELLOW}Seçiminiz (1-4): {Style.RESET_ALL}").strip()
                
                if choice == "1":
                    self.show_prompt_patterns_info()
                elif choice == "2":
                    self.run_predefined_examples()
                elif choice == "3":
                    self.interactive_mode()
                elif choice == "4":
                    print(f"{Fore.GREEN}🎯 AURA AI Demo tamamlandı. Teşekkürler!{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED}❌ Geçersiz seçim. Lütfen 1-4 arası bir sayı girin.{Style.RESET_ALL}")
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.GREEN}🎯 AURA AI Demo tamamlandı. Teşekkürler!{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Hata: {e}{Style.RESET_ALL}")

def main():
    """Ana demo başlatıcısı"""
    
    print(f"{Fore.GREEN}🚀 AURA AI Prompt Engineering NLU Demo başlatılıyor...{Style.RESET_ALL}")
    
    # Create and run demo
    demo = PromptEngineeringNLUDemo()
    demo.run_demo()

if __name__ == "__main__":
    main()
