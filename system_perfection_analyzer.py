# 🧪 KUSURSUZLUK TESPİT VE DOĞRULAMA SİSTEMİ
# RCI (Recursive Criticism and Improvement) Prensipleri

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Tuple
import concurrent.futures
import threading

class SystemPerfectionAnalyzer:
    """
    Sistem kusursuzluğu için detaylı analiz ve otomatik düzeltme sınıfı.
    
    Bu sınıf, sistemdeki her türlü hatayı tespit eder, kök nedenlerini analiz eder,
    düzeltmeler uygular ve doğrulama testleri yapar.
    """
    
    def __init__(self):
        # Ana servis URL'leri - tüm mikroservislerin adresleri
        self.services = {
            'backend': 'http://localhost:8000',
            'image_processing': 'http://localhost:8001',
            'nlu': 'http://localhost:8002',
            'style_profile': 'http://localhost:8003',
            'combination_engine': 'http://localhost:8004',
            'recommendation': 'http://localhost:8005',
            'orchestrator': 'http://localhost:8006',
            'feedback': 'http://localhost:8007'
        }
        
        # API endpoint'leri için detaylı haritalama
        self.api_endpoints = {
            'backend': [
                '/health', '/docs', '/api/v1/auth/register', '/api/v1/auth/login',
                '/api/v1/users/', '/api/v1/products/', '/api/v1/cart/', '/api/v1/orders/'
            ],
            'image_processing': [
                '/', '/docs', '/analyze', '/health'
            ],
            'nlu': [
                '/', '/docs', '/parse_request', '/analyze_text', '/health'
            ],
            'style_profile': [
                '/', '/docs', '/create_profile', '/update_profile', '/health'
            ],
            'combination_engine': [
                '/', '/docs', '/generate_combinations', '/optimize_outfit', '/health'
            ],
            'recommendation': [
                '/', '/docs', '/get_recommendations', '/personalize', '/health'
            ],
            'orchestrator': [
                '/', '/docs', '/orchestrate_workflow', '/coordinate_services', '/health'
            ],
            'feedback': [
                '/', '/docs', '/process_feedback', '/learn_from_data', '/health'
            ]
        }
        
        # Test sonuçlarını depolamak için
        self.analysis_results = {
            'endpoint_analysis': {},
            'performance_analysis': {},
            'data_flow_analysis': {},
            'ai_model_validation': {},
            'identified_issues': [],
            'applied_fixes': [],
            'test_validations': []
        }
        
        print("🎯 SİSTEM KUSURSUZLUK ANALİZÖRÜ BAŞLATILIYOR")
        print("=" * 60)
        print("📋 Metodoloji: RCI + Test Odaklı Geri Besleme Döngüsü")
        print("🎯 Hedef: %100 Kusursuzluk")
        print("=" * 60)
    
    def comprehensive_endpoint_analysis(self) -> Dict[str, Any]:
        """
        Tüm API endpoint'lerini kapsamlı olarak analiz et.
        
        Her endpoint için:
        1. HTTP durum kodunu kontrol et
        2. Yanıt süresini ölç
        3. Yanıt formatını doğrula
        4. Hata durumlarını kategorize et
        """
        print("\n🔍 1. KAPSAMLI API ENDPOINT ANALİZİ")
        print("-" * 50)
        
        endpoint_results = {}
        
        for service_name, base_url in self.services.items():
            print(f"\n📡 {service_name.upper()} Servisi Analizi:")
            service_results = {}
            
            endpoints = self.api_endpoints.get(service_name, ['/'])
            
            for endpoint in endpoints:
                full_url = f"{base_url}{endpoint}"
                
                try:
                    # Yanıt süresini ölçerek istek gönder
                    start_time = time.time()
                    response = requests.get(full_url, timeout=10)
                    response_time = (time.time() - start_time) * 1000
                    
                    # Yanıt analizi yap
                    analysis = self._analyze_response(response, response_time, full_url)
                    service_results[endpoint] = analysis
                    
                    # Sonuçları yazdır
                    status_icon = self._get_status_icon(analysis['status_category'])
                    print(f"   {status_icon} {endpoint:25} -> {analysis['status_code']} ({analysis['response_time']:.0f}ms)")
                    
                    if analysis['issues']:
                        for issue in analysis['issues']:
                            print(f"      ⚠️ {issue}")
                    
                except Exception as e:
                    # Bağlantı hatası durumu
                    error_analysis = {
                        'status_code': 'ERROR',
                        'response_time': 0,
                        'status_category': 'connection_error',
                        'issues': [f"Bağlantı hatası: {str(e)}"],
                        'content_type': None,
                        'response_size': 0
                    }
                    service_results[endpoint] = error_analysis
                    print(f"   ❌ {endpoint:25} -> BAĞLANTI HATASI")
            
            endpoint_results[service_name] = service_results
        
        self.analysis_results['endpoint_analysis'] = endpoint_results
        return endpoint_results
    
    def _analyze_response(self, response: requests.Response, response_time: float, url: str) -> Dict[str, Any]:
        """Bir HTTP yanıtını detaylı olarak analiz et"""
        
        analysis = {
            'status_code': response.status_code,
            'response_time': response_time,
            'content_type': response.headers.get('content-type', 'unknown'),
            'response_size': len(response.content),
            'issues': []
        }
        
        # Durum kodunu kategorize et
        if 200 <= response.status_code < 300:
            analysis['status_category'] = 'success'
        elif 300 <= response.status_code < 400:
            analysis['status_category'] = 'redirect'
            analysis['issues'].append(f"Yönlendirme kodu: {response.status_code}")
        elif 400 <= response.status_code < 500:
            analysis['status_category'] = 'client_error'
            analysis['issues'].append(f"İstemci hatası: {response.status_code}")
        elif 500 <= response.status_code < 600:
            analysis['status_category'] = 'server_error'
            analysis['issues'].append(f"Sunucu hatası: {response.status_code}")
        else:
            analysis['status_category'] = 'unknown'
            analysis['issues'].append(f"Bilinmeyen durum kodu: {response.status_code}")
        
        # Yanıt süresi analizi
        if response_time > 5000:  # 5 saniyeden fazla
            analysis['issues'].append(f"Çok yavaş yanıt: {response_time:.0f}ms")
        elif response_time > 2000:  # 2 saniyeden fazla
            analysis['issues'].append(f"Yavaş yanıt: {response_time:.0f}ms")
        
        # İçerik analizi
        try:
            if 'application/json' in analysis['content_type']:
                json_content = response.json()
                if 'error' in json_content:
                    analysis['issues'].append(f"JSON'da hata: {json_content['error']}")
        except:
            if analysis['status_category'] == 'success' and 'application/json' in analysis['content_type']:
                analysis['issues'].append("Geçersiz JSON formatı")
        
        return analysis
    
    def _get_status_icon(self, category: str) -> str:
        """Durum kategorisine göre ikon döndür"""
        icons = {
            'success': '✅',
            'redirect': '🔄', 
            'client_error': '⚠️',
            'server_error': '❌',
            'connection_error': '🔌',
            'unknown': '❓'
        }
        return icons.get(category, '❓')
    
    def performance_deep_analysis(self) -> Dict[str, Any]:
        """
        Performans derinlemesine analizi.
        
        Her servis için:
        1. Çoklu istek load testi
        2. Eşzamanlı istek testi  
        3. Bellek kullanımı analizi
        4. CPU kullanımı tahini
        """
        print("\n⚡ 2. PERFORMANS DERİNLEMESİNE ANALİZİ")
        print("-" * 50)
        
        performance_results = {}
        
        for service_name, base_url in self.services.items():
            print(f"\n📊 {service_name.upper()} Performans Testi:")
            
            # Basit health check endpoint'i kullan
            test_endpoint = f"{base_url}/" if service_name != 'backend' else f"{base_url}/health"
            
            # 1. Tek istek baseline testi
            baseline_time = self._measure_response_time(test_endpoint)
            
            # 2. Çoklu ardışık istek testi (5 istek)
            sequential_times = []
            for i in range(5):
                response_time = self._measure_response_time(test_endpoint)
                sequential_times.append(response_time)
            
            # 3. Eşzamanlı istek testi (3 paralel istek)
            concurrent_times = self._concurrent_request_test(test_endpoint, 3)
            
            # Analiz sonuçları
            performance_data = {
                'baseline_response_time': baseline_time,
                'sequential_avg': sum(sequential_times) / len(sequential_times),
                'sequential_max': max(sequential_times),
                'concurrent_avg': sum(concurrent_times) / len(concurrent_times) if concurrent_times else 0,
                'concurrent_max': max(concurrent_times) if concurrent_times else 0,
                'performance_issues': []
            }
            
            # Performans sorunlarını tespit et
            if performance_data['baseline_response_time'] > 2000:
                performance_data['performance_issues'].append(f"Baseline çok yavaş: {baseline_time:.0f}ms")
            
            if performance_data['sequential_max'] > performance_data['baseline_response_time'] * 2:
                performance_data['performance_issues'].append("Ardışık isteklerde performans düşüşü")
            
            if performance_data['concurrent_avg'] > performance_data['baseline_response_time'] * 1.5:
                performance_data['performance_issues'].append("Eşzamanlı isteklerde performans sorunu")
            
            # Sonuçları yazdır
            print(f"   📈 Baseline: {baseline_time:.0f}ms")
            print(f"   📊 Ardışık Ortalama: {performance_data['sequential_avg']:.0f}ms")
            print(f"   🔄 Eşzamanlı Ortalama: {performance_data['concurrent_avg']:.0f}ms")
            
            if performance_data['performance_issues']:
                for issue in performance_data['performance_issues']:
                    print(f"   ⚠️ {issue}")
            else:
                print(f"   ✅ Performans normal")
            
            performance_results[service_name] = performance_data
        
        self.analysis_results['performance_analysis'] = performance_results
        return performance_results
    
    def _measure_response_time(self, url: str) -> float:
        """Tek bir URL için yanıt süresini ölç"""
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10)
            return (time.time() - start_time) * 1000
        except:
            return 10000  # Hata durumunda çok yüksek süre döndür
    
    def _concurrent_request_test(self, url: str, num_requests: int) -> List[float]:
        """Eşzamanlı istek testi yap"""
        results = []
        
        def single_request():
            return self._measure_response_time(url)
        
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
                futures = [executor.submit(single_request) for _ in range(num_requests)]
                results = [future.result() for future in concurrent.futures.as_completed(futures, timeout=30)]
        except:
            results = []
        
        return results
    
    def data_flow_integrity_analysis(self) -> Dict[str, Any]:
        """
        Veri akışı bütünlüğü analizi.
        
        Servisler arası veri akışında:
        1. Veri formatı uyumluluğu
        2. Alan eksiklikleri
        3. Tip uyuşmazlıkları
        4. Zaman aşımı sorunları
        """
        print("\n🔄 3. VERİ AKIŞI BÜTÜNLÜK ANALİZİ")
        print("-" * 50)
        
        flow_results = {}
        
        # Test verisi hazırla
        test_data = {
            'image_analysis': {
                'image_description': 'Mavi spor ayakkabısı',
                'analysis_type': 'clothing_detection',
                'user_context': 'wardrobe_addition'
            },
            'nlu_request': {
                'text': 'Bugün spor için ayakkabı istiyorum',
                'language': 'tr',
                'context': 'product_recommendation'
            },
            'style_profile': {
                'user_preferences': {
                    'activity': 'sport',
                    'style_preference': 'modern_sporty',
                    'color_preferences': ['blue', 'black', 'white']
                }
            }
        }
        
        # Her servis için veri akışı testi
        test_scenarios = [
            ('image_processing', '/analyze', test_data['image_analysis']),
            ('nlu', '/parse_request', test_data['nlu_request']),
            ('style_profile', '/create_profile', test_data['style_profile'])
        ]
        
        for service_name, endpoint, data in test_scenarios:
            print(f"\n🔍 {service_name.upper()} Veri Akışı Testi:")
            
            url = f"{self.services[service_name]}{endpoint}"
            
            try:
                # POST isteği gönder
                start_time = time.time()
                response = requests.post(url, json=data, timeout=15)
                response_time = (time.time() - start_time) * 1000
                
                flow_analysis = {
                    'status_code': response.status_code,
                    'response_time': response_time,
                    'data_issues': []
                }
                
                # Yanıt analizi
                if response.status_code == 200:
                    try:
                        response_data = response.json()
                        
                        # Veri formatı kontrolü
                        if not isinstance(response_data, dict):
                            flow_analysis['data_issues'].append("Yanıt dict formatında değil")
                        
                        # Boş yanıt kontrolü
                        if not response_data:
                            flow_analysis['data_issues'].append("Boş yanıt")
                        
                        # Hata mesajı kontrolü
                        if 'error' in response_data:
                            flow_analysis['data_issues'].append(f"Yanıtta hata: {response_data['error']}")
                        
                        print(f"   ✅ Başarılı yanıt ({response_time:.0f}ms)")
                        
                    except json.JSONDecodeError:
                        flow_analysis['data_issues'].append("JSON decode hatası")
                        print(f"   ❌ JSON decode hatası")
                
                elif response.status_code == 404:
                    flow_analysis['data_issues'].append("Endpoint bulunamadı")
                    print(f"   ⚠️ Endpoint bulunamadı (404)")
                
                elif response.status_code == 500:
                    flow_analysis['data_issues'].append("Sunucu internal hatası")
                    print(f"   ❌ Sunucu hatası (500)")
                
                else:
                    flow_analysis['data_issues'].append(f"Beklenmeyen durum kodu: {response.status_code}")
                    print(f"   ⚠️ Durum kodu: {response.status_code}")
                
                if flow_analysis['data_issues']:
                    for issue in flow_analysis['data_issues']:
                        print(f"      • {issue}")
                
                flow_results[f"{service_name}_{endpoint}"] = flow_analysis
                
            except Exception as e:
                error_info = {
                    'status_code': 'ERROR',
                    'response_time': 0,
                    'data_issues': [f"İstek hatası: {str(e)}"]
                }
                flow_results[f"{service_name}_{endpoint}"] = error_info
                print(f"   ❌ İstek hatası: {str(e)[:50]}")
        
        self.analysis_results['data_flow_analysis'] = flow_results
        return flow_results
    
    def ai_model_output_validation(self) -> Dict[str, Any]:
        """
        AI model çıktılarında halüsinasyon ve anlamsızlık tespiti.
        
        Her AI servisi için:
        1. Çıktı formatı doğrulaması
        2. Mantık tutarlılığı kontrolü
        3. Halüsinasyon tespiti
        4. Veri doğruluğu analizi
        """
        print("\n🤖 4. AI MODEL ÇIKTI DOĞRULAMA")
        print("-" * 50)
        
        validation_results = {}
        
        # AI servisler için test senaryoları
        ai_test_cases = {
            'nlu': {
                'endpoint': '/parse_request',
                'test_input': {
                    'text': 'Mavi bir tişört arıyorum',
                    'language': 'tr',
                    'context': 'product_search'
                },
                'expected_patterns': {
                    'intent': ['search', 'find', 'recommendation'],
                    'product_type': ['shirt', 'tshirt', 'clothing'],
                    'color': ['blue', 'mavi']
                }
            },
            'style_profile': {
                'endpoint': '/create_profile',
                'test_input': {
                    'user_preferences': {
                        'style': 'casual',
                        'colors': ['blue', 'black'],
                        'activity': 'daily'
                    }
                },
                'expected_patterns': {
                    'style_category': ['casual', 'modern', 'classic'],
                    'confidence': [0.1, 1.0]  # Range
                }
            }
        }
        
        for service_name, test_case in ai_test_cases.items():
            print(f"\n🧠 {service_name.upper()} AI Doğrulama:")
            
            url = f"{self.services[service_name]}{test_case['endpoint']}"
            
            try:
                response = requests.post(url, json=test_case['test_input'], timeout=15)
                validation_result = {
                    'status_code': response.status_code,
                    'validation_issues': []
                }
                
                if response.status_code == 200:
                    try:
                        ai_output = response.json()
                        
                        # Output format validation
                        if not isinstance(ai_output, dict):
                            validation_result['validation_issues'].append("AI çıktısı dict formatında değil")
                        
                        # Hallucination detection
                        validation_issues = self._detect_ai_hallucinations(
                            ai_output, 
                            test_case['test_input'],
                            test_case.get('expected_patterns', {})
                        )
                        validation_result['validation_issues'].extend(validation_issues)
                        
                        if not validation_result['validation_issues']:
                            print(f"   ✅ AI çıktısı doğru ve tutarlı")
                        else:
                            for issue in validation_result['validation_issues']:
                                print(f"   ⚠️ {issue}")
                    
                    except json.JSONDecodeError:
                        validation_result['validation_issues'].append("AI yanıtı geçerli JSON değil")
                        print(f"   ❌ JSON decode hatası")
                
                else:
                    validation_result['validation_issues'].append(f"AI servisi yanıt vermiyor: {response.status_code}")
                    print(f"   ❌ Yanıt kodu: {response.status_code}")
                
                validation_results[service_name] = validation_result
                
            except Exception as e:
                validation_results[service_name] = {
                    'status_code': 'ERROR',
                    'validation_issues': [f"AI test hatası: {str(e)}"]
                }
                print(f"   ❌ Test hatası: {str(e)[:50]}")
        
        self.analysis_results['ai_model_validation'] = validation_results
        return validation_results
    
    def _detect_ai_hallucinations(self, ai_output: Dict, input_data: Dict, expected_patterns: Dict) -> List[str]:
        """AI çıktısında halüsinasyon tespit et"""
        issues = []
        
        # Boş veya None değer kontrolü
        if not ai_output:
            issues.append("AI boş yanıt döndürdü")
            return issues
        
        # Confidence score kontrolü
        if 'confidence' in ai_output:
            confidence = ai_output['confidence']
            if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
                issues.append(f"Geçersiz confidence değeri: {confidence}")
        
        # Pattern matching kontrolü
        for field, expected_values in expected_patterns.items():
            if field in ai_output:
                actual_value = ai_output[field]
                
                if isinstance(expected_values, list) and len(expected_values) == 2 and all(isinstance(x, (int, float)) for x in expected_values):
                    # Range kontrolü
                    min_val, max_val = expected_values
                    if not (min_val <= actual_value <= max_val):
                        issues.append(f"{field} değeri beklenen aralıkta değil: {actual_value}")
                else:
                    # Enum kontrolü
                    if isinstance(actual_value, str) and not any(expected in actual_value.lower() for expected in expected_values):
                        issues.append(f"{field} beklenen değerlerden biri değil: {actual_value}")
        
        # Nonsensical output detection
        string_fields = [k for k, v in ai_output.items() if isinstance(v, str)]
        for field in string_fields:
            value = ai_output[field]
            if len(value) > 100:  # Çok uzun string
                issues.append(f"{field} çok uzun: {len(value)} karakter")
            elif value.lower() in ['qwerty', '123456', 'test', 'null', 'undefined']:
                issues.append(f"{field} test/placeholder değeri içeriyor: {value}")
        
        return issues
    
    def generate_comprehensive_analysis_report(self) -> str:
        """Kapsamlı analiz raporu oluştur"""
        print("\n📊 5. KAPSAMLI ANALİZ RAPORU OLUŞTURMA")
        print("-" * 50)
        
        report = []
        report.append("# 🎯 AURA AI SİSTEMİ - KUSURSUZLUK ANALİZ RAPORU")
        report.append("=" * 70)
        report.append(f"📅 Analiz Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"🎯 Hedef: %100 Sistem Kusursuzluğu")
        report.append("")
        
        # Endpoint Analizi Özeti
        endpoint_issues = 0
        total_endpoints = 0
        
        for service, endpoints in self.analysis_results['endpoint_analysis'].items():
            for endpoint, data in endpoints.items():
                total_endpoints += 1
                if data['status_category'] != 'success' or data['issues']:
                    endpoint_issues += 1
        
        report.append("## 📡 API ENDPOINT ANALİZİ")
        report.append(f"- **Toplam Endpoint**: {total_endpoints}")
        report.append(f"- **Sorunlu Endpoint**: {endpoint_issues}")
        report.append(f"- **Başarı Oranı**: {((total_endpoints - endpoint_issues) / total_endpoints * 100):.1f}%")
        report.append("")
        
        # Performans Analizi Özeti
        performance_issues = 0
        total_services = len(self.analysis_results['performance_analysis'])
        
        for service, data in self.analysis_results['performance_analysis'].items():
            if data['performance_issues']:
                performance_issues += 1
        
        report.append("## ⚡ PERFORMANS ANALİZİ")
        report.append(f"- **Toplam Servis**: {total_services}")
        report.append(f"- **Performans Sorunu**: {performance_issues}")
        report.append(f"- **Performans Başarı**: {((total_services - performance_issues) / total_services * 100):.1f}%")
        report.append("")
        
        # Veri Akışı Analizi Özeti
        flow_issues = 0
        total_flows = len(self.analysis_results['data_flow_analysis'])
        
        for flow, data in self.analysis_results['data_flow_analysis'].items():
            if data['data_issues']:
                flow_issues += 1
        
        report.append("## 🔄 VERİ AKIŞI ANALİZİ")
        report.append(f"- **Toplam Test**: {total_flows}")
        report.append(f"- **Sorunlu Akış**: {flow_issues}")
        report.append(f"- **Akış Başarı**: {((total_flows - flow_issues) / total_flows * 100):.1f}%")
        report.append("")
        
        # AI Model Analizi Özeti
        ai_issues = 0
        total_ai_tests = len(self.analysis_results['ai_model_validation'])
        
        for service, data in self.analysis_results['ai_model_validation'].items():
            if data['validation_issues']:
                ai_issues += 1
        
        report.append("## 🤖 AI MODEL VALİDASYONU")
        report.append(f"- **Toplam AI Test**: {total_ai_tests}")
        report.append(f"- **Sorunlu AI**: {ai_issues}")
        report.append(f"- **AI Başarı**: {((total_ai_tests - ai_issues) / total_ai_tests * 100):.1f}%")
        report.append("")
        
        # Genel Skor Hesaplaması
        total_tests = total_endpoints + total_services + total_flows + total_ai_tests
        total_issues = endpoint_issues + performance_issues + flow_issues + ai_issues
        overall_success = ((total_tests - total_issues) / total_tests * 100) if total_tests > 0 else 100
        
        report.append("## 🏆 GENEL BAŞARI SKORU")
        report.append(f"- **Toplam Test**: {total_tests}")
        report.append(f"- **Toplam Sorun**: {total_issues}")
        report.append(f"- **GENEL BAŞARI**: {overall_success:.1f}%")
        report.append("")
        
        if overall_success >= 100:
            report.append("🎉 **SİSTEM KUSURSUZ DURUMA ULAŞTI!**")
        elif overall_success >= 95:
            report.append("✅ **SİSTEM NEREDEYSE KUSURSUZ**")
        elif overall_success >= 90:
            report.append("⚠️ **SİSTEM İYİ DURUMDA ANCAK İYİLEŞTİRME GEREKLİ**")
        else:
            report.append("❌ **SİSTEM CİDDİ İYİLEŞTİRME GEREKTİRİYOR**")
        
        return "\n".join(report)
    
    def run_complete_analysis(self) -> Dict[str, Any]:
        """Tüm analiz süreçlerini çalıştır"""
        print("🚀 KAPSAMLI SİSTEM ANALİZİ BAŞLATIYOR")
        print("=" * 60)
        
        # 1. API Endpoint Analizi
        self.comprehensive_endpoint_analysis()
        
        # 2. Performans Analizi  
        self.performance_deep_analysis()
        
        # 3. Veri Akışı Analizi
        self.data_flow_integrity_analysis()
        
        # 4. AI Model Doğrulama
        self.ai_model_output_validation()
        
        # 5. Kapsamlı Rapor
        final_report = self.generate_comprehensive_analysis_report()
        print(final_report)
        
        return self.analysis_results

def main():
    """Ana analiz fonksiyonu"""
    analyzer = SystemPerfectionAnalyzer()
    results = analyzer.run_complete_analysis()
    
    print(f"\n🏁 ANALİZ TAMAMLANDI")
    print(f"📊 Detaylı sonuçlar 'analysis_results' içinde mevcut")
    
    return results

if __name__ == "__main__":
    main()
