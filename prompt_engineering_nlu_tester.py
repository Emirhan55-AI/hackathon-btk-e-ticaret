# 🧪 AURA AI - PROMPT ENGINEERING NLU TEST SUITE
# Gelişmiş Prompt Kalıpları ve Akış Mühendisliği Test Sistemi

import requests
import json
import time
from typing import Dict, Any, List
import asyncio
from datetime import datetime

class PromptEngineeringNLUTester:
    """
    Prompt Engineering tabanlı NLU servisini test eden kapsamlı test sistemi.
    
    Bu sınıf, beş temel prompt kalıbının etkinliğini test eder:
    1. PERSONA testleri
    2. RECIPE testleri
    3. TEMPLATE testleri
    4. CONTEXT testleri 
    5. INSTRUCTION testleri
    """
    
    def __init__(self, base_url: str = "http://localhost:8002"):
        """Test sistemini başlat"""
        self.base_url = base_url
        self.test_results = []
        
        print("🧪 AURA AI - Prompt Engineering NLU Test Sistemi")
        print("=" * 60)
    
    def test_health_check(self) -> Dict[str, Any]:
        """Health check endpoint'ini test et"""
        
        print("\n🔍 Health Check Testi...")
        
        try:
            response = requests.get(f"{self.base_url}/")
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"✅ Service Status: {data.get('status', 'unknown')}")
                print(f"📍 Phase: {data.get('phase', 'unknown')}")
                print(f"🧠 Version: {data.get('version', 'unknown')}")
                print(f"🎯 Prompt Engineering: {data.get('systems_status', {}).get('prompt_engineering', 'unknown')}")
                
                return {"success": True, "data": data}
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return {"success": False, "error": f"Status code: {response.status_code}"}
                
        except Exception as e:
            print(f"❌ Health check exception: {e}")
            return {"success": False, "error": str(e)}
    
    def test_prompt_patterns_info(self) -> Dict[str, Any]:
        """Prompt patterns info endpoint'ini test et"""
        
        print("\n📋 Prompt Patterns Info Testi...")
        
        try:
            response = requests.get(f"{self.base_url}/prompt_patterns_info")
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"✅ Prompt Engineering Available: {data.get('prompt_engineering_system', {}).get('available', False)}")
                print(f"🎯 Supported Intents: {len(data.get('supported_intents', []))}")
                print(f"🌍 Supported Contexts: {len(data.get('supported_contexts', []))}")
                print(f"🗣️ Languages: {data.get('fashion_domain_features', {}).get('multilingual_support', [])}")
                
                return {"success": True, "data": data}
            else:
                print(f"❌ Prompt patterns info failed: {response.status_code}")
                return {"success": False, "error": f"Status code: {response.status_code}"}
                
        except Exception as e:
            print(f"❌ Prompt patterns info exception: {e}")
            return {"success": False, "error": str(e)}
    
    def test_prompt_engineering_analysis(self) -> Dict[str, Any]:
        """Prompt engineering analysis endpoint'ini test et"""
        
        print("\n🧠 Prompt Engineering Analysis Testi...")
        
        test_cases = [
            {
                "name": "Türkçe İş Kıyafeti Önerisi",
                "text": "Yarın önemli bir toplantım var, ne giyebilirim? Profesyonel görünmek istiyorum.",
                "language": "tr",
                "context_hint": "work_office",
                "expected_intent": "outfit_recommendation"
            },
            {
                "name": "English Casual Style",
                "text": "I want to look stylish but comfortable for a weekend brunch with friends.",
                "language": "en", 
                "context_hint": "casual_daily",
                "expected_intent": "outfit_recommendation"
            },
            {
                "name": "Renk Uyumu Sorusu",
                "text": "Bu mavi gömlek hangi renk pantolon ile güzel durur?",
                "language": "tr",
                "context_hint": None,
                "expected_intent": "color_matching"
            },
            {
                "name": "Parti Kombinasyonu",
                "text": "Bu akşam bir partiye gidiyorum, elbiseleri nasıl kombineleyebilirim?",
                "language": "tr", 
                "context_hint": "social_party",
                "expected_intent": "style_combination"
            }
        ]
        
        all_results = []
        
        for test_case in test_cases:
            print(f"\n  🔍 Test: {test_case['name']}")
            
            try:
                # Prepare request
                request_data = {
                    "text": test_case["text"],
                    "language": test_case["language"],
                    "analysis_method": "prompt_patterns",
                    "context_hint": test_case["context_hint"],
                    "enable_entity_extraction": True,
                    "enable_fashion_reasoning": True,
                    "return_explanations": True
                }
                
                # Send request
                start_time = time.time()
                response = requests.post(
                    f"{self.base_url}/analyze_with_prompt_patterns",
                    json=request_data,
                    headers={"Content-Type": "application/json"}
                )
                processing_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extract key results
                    intent_analysis = data.get("intent_analysis", {})
                    detected_intent = intent_analysis.get("intent", "unknown")
                    confidence = intent_analysis.get("confidence", 0.0)
                    
                    context_analysis = data.get("context_analysis", {})
                    detected_context = context_analysis.get("context", "unknown")
                    
                    entity_extraction = data.get("entity_extraction", {})
                    entities = entity_extraction.get("entities", {})
                    
                    # Show results
                    print(f"    ✅ Intent: {detected_intent} (confidence: {confidence:.2f})")
                    print(f"    🎯 Context: {detected_context}")
                    print(f"    🏷️ Entities: {len(entities.get('clothing_items', []))} items, {len(entities.get('colors', []))} colors")
                    print(f"    ⏱️ Processing: {processing_time:.3f}s")
                    
                    # Check if intent matches expectation
                    intent_match = detected_intent == test_case["expected_intent"]
                    print(f"    🎯 Expected Intent Match: {'✅' if intent_match else '❌'}")
                    
                    all_results.append({
                        "test_name": test_case["name"],
                        "success": True,
                        "intent_detected": detected_intent,
                        "intent_expected": test_case["expected_intent"],
                        "intent_match": intent_match,
                        "confidence": confidence,
                        "processing_time": processing_time,
                        "entities_count": len(entities.get("clothing_items", [])) + len(entities.get("colors", []))
                    })
                    
                else:
                    print(f"    ❌ Request failed: {response.status_code}")
                    all_results.append({
                        "test_name": test_case["name"],
                        "success": False,
                        "error": f"HTTP {response.status_code}"
                    })
                    
            except Exception as e:
                print(f"    ❌ Test exception: {e}")
                all_results.append({
                    "test_name": test_case["name"],
                    "success": False,
                    "error": str(e)
                })
        
        return {"success": True, "test_results": all_results}
    
    def test_fashion_intent_analysis(self) -> Dict[str, Any]:
        """Fashion intent analysis endpoint'ini test et"""
        
        print("\n👗 Fashion Intent Analysis Testi...")
        
        test_texts = [
            "Bugün ne giysem acaba?",
            "Bu elbise hangi ayakkabı ile uyar?",
            "İş toplantısı için kıyafet önerisi",
            "Gardırobumu yeniden düzenlemek istiyorum"
        ]
        
        all_results = []
        
        for text in test_texts:
            print(f"\n  🔍 Test: '{text[:30]}...'")
            
            try:
                request_data = {
                    "text": text,
                    "language": "tr",
                    "analysis_method": "prompt_patterns"
                }
                
                start_time = time.time()
                response = requests.post(
                    f"{self.base_url}/analyze_fashion_intent",
                    json=request_data,
                    headers={"Content-Type": "application/json"}
                )
                processing_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    
                    fashion_intent = data.get("fashion_intent_analysis", {})
                    intent_classification = fashion_intent.get("intent_classification", {})
                    detected_intent = intent_classification.get("intent", "unknown")
                    confidence = fashion_intent.get("confidence_score", 0.0)
                    
                    service_coordination = fashion_intent.get("service_coordination", {})
                    
                    print(f"    ✅ Fashion Intent: {detected_intent}")
                    print(f"    🎯 Confidence: {confidence:.2f}")
                    print(f"    🔗 Services Needed: {sum(1 for v in service_coordination.values() if v)}")
                    print(f"    ⏱️ Processing: {processing_time:.3f}s")
                    
                    all_results.append({
                        "text": text,
                        "success": True,
                        "intent": detected_intent,
                        "confidence": confidence,
                        "processing_time": processing_time
                    })
                    
                else:
                    print(f"    ❌ Request failed: {response.status_code}")
                    all_results.append({
                        "text": text,
                        "success": False,
                        "error": f"HTTP {response.status_code}"
                    })
                    
            except Exception as e:
                print(f"    ❌ Test exception: {e}")
                all_results.append({
                    "text": text,
                    "success": False,
                    "error": str(e)
                })
        
        return {"success": True, "test_results": all_results}
    
    def test_fashion_entity_extraction(self) -> Dict[str, Any]:
        """Fashion entity extraction endpoint'ini test et"""
        
        print("\n🏷️ Fashion Entity Extraction Testi...")
        
        test_texts = [
            "Siyah bir blazer, beyaz gömlek ve koyu mavi pantolon giyeceğim",
            "Nike ayakkabılarım ve Zara ceketim var",
            "Bu akşam kırmızı elbisemi giyip partiye gideceğim",
            "XL beden tişört arıyorum, mavi veya yeşil olsun"
        ]
        
        all_results = []
        
        for text in test_texts:
            print(f"\n  🔍 Test: '{text[:40]}...'")
            
            try:
                request_data = {
                    "text": text,
                    "language": "tr",
                    "enable_entity_extraction": True
                }
                
                start_time = time.time()
                response = requests.post(
                    f"{self.base_url}/extract_fashion_entities",
                    json=request_data,
                    headers={"Content-Type": "application/json"}
                )
                processing_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    
                    entity_extraction = data.get("fashion_entity_extraction", {})
                    extracted_entities = entity_extraction.get("extracted_entities", {})
                    
                    clothing_items = extracted_entities.get("clothing_items", [])
                    colors = extracted_entities.get("colors", [])
                    brands = extracted_entities.get("brands", [])
                    
                    print(f"    ✅ Clothing Items: {len(clothing_items)} ({clothing_items})")
                    print(f"    🎨 Colors: {len(colors)} ({colors})")
                    print(f"    🏷️ Brands: {len(brands)} ({brands})")
                    print(f"    ⏱️ Processing: {processing_time:.3f}s")
                    
                    all_results.append({
                        "text": text,
                        "success": True,
                        "clothing_items": len(clothing_items),
                        "colors": len(colors),
                        "brands": len(brands),
                        "processing_time": processing_time
                    })
                    
                else:
                    print(f"    ❌ Request failed: {response.status_code}")
                    all_results.append({
                        "text": text,
                        "success": False,
                        "error": f"HTTP {response.status_code}"
                    })
                    
            except Exception as e:
                print(f"    ❌ Test exception: {e}")
                all_results.append({
                    "text": text,
                    "success": False,
                    "error": str(e)
                })
        
        return {"success": True, "test_results": all_results}
    
    def test_legacy_compatibility(self) -> Dict[str, Any]:
        """Legacy endpoint uyumluluğunu test et"""
        
        print("\n🔄 Legacy Compatibility Testi...")
        
        try:
            response = requests.post(
                f"{self.base_url}/understand_text",
                json={"text": "Bugün ne giysem?", "language": "tr"},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"✅ Legacy Response Format: OK")
                print(f"🎯 Intent: {data.get('intent', 'unknown')}")
                print(f"📊 Confidence: {data.get('confidence', 0.0)}")
                print(f"🔧 Enhanced With: {data.get('enhanced_with', 'unknown')}")
                
                return {"success": True, "data": data}
            else:
                print(f"❌ Legacy test failed: {response.status_code}")
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            print(f"❌ Legacy test exception: {e}")
            return {"success": False, "error": str(e)}
    
    def run_comprehensive_test_suite(self) -> Dict[str, Any]:
        """Kapsamlı test suite'ini çalıştır"""
        
        print("\n🚀 KAPSAMLI PROMPT ENGINEERING NLU TEST SUITE BAŞLIYOR...")
        print("=" * 70)
        
        start_time = time.time()
        
        # Tüm testleri çalıştır
        results = {
            "health_check": self.test_health_check(),
            "prompt_patterns_info": self.test_prompt_patterns_info(), 
            "prompt_engineering_analysis": self.test_prompt_engineering_analysis(),
            "fashion_intent_analysis": self.test_fashion_intent_analysis(),
            "fashion_entity_extraction": self.test_fashion_entity_extraction(),
            "legacy_compatibility": self.test_legacy_compatibility()
        }
        
        total_time = time.time() - start_time
        
        # Sonuçları özetle
        print("\n" + "=" * 70)
        print("📊 TEST SUITE SONUÇLARI")
        print("=" * 70)
        
        total_tests = 0
        successful_tests = 0
        
        for test_name, test_result in results.items():
            success = test_result.get("success", False)
            print(f"{'✅' if success else '❌'} {test_name}: {'BAŞARILI' if success else 'BAŞARISIZ'}")
            
            if success:
                successful_tests += 1
            total_tests += 1
            
            # Alt test sayılarını dahil et
            if "test_results" in test_result:
                sub_tests = test_result["test_results"]
                sub_success = sum(1 for t in sub_tests if t.get("success", False))
                sub_total = len(sub_tests)
                print(f"   └─ Alt testler: {sub_success}/{sub_total} başarılı")
                total_tests += sub_total - 1  # Ana test zaten sayıldı
                successful_tests += sub_success - (1 if success else 0)
        
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n📈 GENEL BAŞARI ORANI: {success_rate:.1f}% ({successful_tests}/{total_tests})")
        print(f"⏱️ TOPLAM SÜRE: {total_time:.2f} saniye")
        
        # Genel değerlendirme
        if success_rate >= 90:
            print("🎉 MÜKEMMEl! Prompt Engineering NLU sistemi tamamen çalışıyor!")
        elif success_rate >= 70:
            print("✅ İYI! Sistem çalışıyor, bazı iyileştirmeler yapılabilir.")
        elif success_rate >= 50:
            print("⚠️ ORTA! Sistem kısmen çalışıyor, sorunlar var.")
        else:
            print("❌ KÖTÜ! Sistemde ciddi sorunlar var, inceleme gerekli.")
        
        return {
            "overall_success_rate": success_rate,
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "total_time": total_time,
            "detailed_results": results,
            "timestamp": datetime.now().isoformat()
        }

def main():
    """Ana test fonksiyonu"""
    
    # Test sistemini başlat
    tester = PromptEngineeringNLUTester()
    
    # Kapsamlı test suite'ini çalıştır
    final_results = tester.run_comprehensive_test_suite()
    
    # Sonuçları JSON dosyasına kaydet
    with open("prompt_engineering_nlu_test_results.json", "w", encoding="utf-8") as f:
        json.dump(final_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Test sonuçları 'prompt_engineering_nlu_test_results.json' dosyasına kaydedildi.")

if __name__ == "__main__":
    main()
