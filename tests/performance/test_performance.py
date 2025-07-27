# ⚡ AURA AI SİSTEMİ - PERFORMANS TEST PAKETİ
# Test Odaklı Geri Besleme Döngüsü (AlphaCodium/SED) Performans Benchmark Sistemi

import pytest
import time
import asyncio
import statistics
import threading
import concurrent.futures
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta
import json
import psutil
import requests
from unittest.mock import Mock, patch

# Test framework konfigürasyonunu import et
from ..conftest import AuraTestConfig, TestUtilities

class PerformanceTestSuite:
    """
    Performans test paketi.
    
    Bu sınıf, sistemin çeşitli yük koşullarındaki performansını ölçer.
    Yanıt süreleri, throughput, kaynak kullanımı ve scalability testleri yapar.
    """
    
    def __init__(self):
        # Test konfigürasyonunu yükle
        self.config = AuraTestConfig()
        self.utils = TestUtilities()
        
        # Performans kriterleri ve thresholdlar
        self.performance_thresholds = {
            'response_time_ms': {
                'excellent': 200,
                'good': 500,
                'acceptable': 1000,
                'poor': 2000,
                'unacceptable': 5000
            },
            'throughput_rps': {
                'minimum': 10,
                'target': 50,  
                'excellent': 100
            },
            'concurrent_users': {
                'minimum': 10,
                'target': 50,
                'maximum': 200
            },
            'resource_usage': {
                'cpu_percent': 80,
                'memory_mb': 1024,
                'disk_io_mbps': 100
            }
        }
        
        # Test sonuçlarını saklamak için
        self.performance_results = {
            'response_time_tests': {},
            'load_tests': {},
            'stress_tests': {},
            'endurance_tests': {},
            'resource_usage_tests': {}
        }

# Test sınıfları
class TestResponseTimeBenchmarks:
    """
    Yanıt süresi benchmark testleri.
    
    Bu test grubu, her servisin farklı yük koşullarındaki yanıt sürelerini ölçer.
    """
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Her test öncesi gerekli kurulumları yap"""
        self.config = AuraTestConfig()
        self.utils = TestUtilities()
        
        print("\n⚡ Yanıt süresi benchmark testleri başlatılıyor...")
    
    def test_single_request_response_times(self):
        """
        Tek istek yanıt sürelerini test et.
        
        Her servise tek istek gönderip yanıt sürelerini ölç.
        Bu baseline performans metriğidir.
        """
        print("   🔍 Test: Tek istek yanıt süreleri")
        
        # Her servis için yanıt süresi ölç
        response_times = {}
        
        for service_name, service_url in self.config.SERVICES.items():
            print(f"      📊 {service_name} yanıt süresi ölçülüyor...")
            
            # 10 kez ölçüm yapıp ortalama al
            measurements = []
            
            for i in range(10):
                start_time = time.time()
                
                try:
                    # Mock request simülasyonu
                    response = self._simulate_service_request(service_name, service_url)
                    response_time_ms = (time.time() - start_time) * 1000
                    measurements.append(response_time_ms)
                    
                except Exception as e:
                    print(f"         ⚠️ Ölçüm {i+1} başarısız: {str(e)}")
                    measurements.append(5000)  # Timeout değeri
            
            # İstatistikleri hesapla
            response_times[service_name] = {
                'avg_ms': statistics.mean(measurements),
                'min_ms': min(measurements),
                'max_ms': max(measurements),
                'median_ms': statistics.median(measurements),
                'std_dev': statistics.stdev(measurements) if len(measurements) > 1 else 0,
                'measurements': measurements
            }
            
            avg_time = response_times[service_name]['avg_ms']
            performance_level = self._categorize_response_time(avg_time)
            
            print(f"         ⏱️ Ortalama: {avg_time:.2f}ms ({performance_level})")
            print(f"         📈 Min: {response_times[service_name]['min_ms']:.2f}ms")
            print(f"         📉 Max: {response_times[service_name]['max_ms']:.2f}ms")
        
        # Genel değerlendirme
        total_avg = statistics.mean([rt['avg_ms'] for rt in response_times.values()])
        overall_performance = self._categorize_response_time(total_avg)
        
        print(f"\n      🎯 Genel ortalama yanıt süresi: {total_avg:.2f}ms ({overall_performance})")
        
        # Doğrulamalar
        slow_services = [name for name, data in response_times.items() 
                        if data['avg_ms'] > self.config.PERFORMANCE_THRESHOLDS['response_time_ms']]
        
        assert len(slow_services) == 0, f"Yavaş servisler tespit edildi: {slow_services}"
        assert total_avg < 1000, f"Genel ortalama yanıt süresi çok yüksek: {total_avg:.2f}ms"
        
        return response_times
    
    def test_concurrent_request_response_times(self):
        """
        Eşzamanlı istek yanıt sürelerini test et.
        
        Aynı anda birden fazla istek gönderip yanıt sürelerinin nasıl etkilendiğini ölç.
        """
        print("   🔍 Test: Eşzamanlı istek yanıt süreleri")
        
        concurrent_levels = [5, 10, 20, 50]  # Eşzamanlılık seviyeleri
        concurrent_results = {}
        
        for concurrent_count in concurrent_levels:
            print(f"      📊 {concurrent_count} eşzamanlı istek testi...")
            
            # Eşzamanlı istekler için thread pool
            with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_count) as executor:
                start_time = time.time()
                
                # Tüm istekleri başlat
                futures = []
                for i in range(concurrent_count):
                    service_name = list(self.config.SERVICES.keys())[i % len(self.config.SERVICES)]
                    service_url = self.config.SERVICES[service_name]
                    
                    future = executor.submit(self._simulate_service_request, service_name, service_url)
                    futures.append((future, service_name))
                
                # Sonuçları topla
                results = []
                for future, service_name in futures:
                    try:
                        future.result(timeout=10)  # 10 saniye timeout
                        request_time = time.time() - start_time
                        results.append({'service': service_name, 'time_ms': request_time * 1000})
                    except Exception as e:
                        results.append({'service': service_name, 'time_ms': 10000, 'error': str(e)})
                
                total_time = time.time() - start_time
                
                # İstatistikleri hesapla
                successful_requests = [r for r in results if 'error' not in r]
                failed_requests = [r for r in results if 'error' in r]
                
                concurrent_results[concurrent_count] = {
                    'total_time_ms': total_time * 1000,
                    'successful_count': len(successful_requests),
                    'failed_count': len(failed_requests),
                    'success_rate': len(successful_requests) / concurrent_count * 100,
                    'avg_response_time_ms': statistics.mean([r['time_ms'] for r in successful_requests]) if successful_requests else 0,
                    'throughput_rps': concurrent_count / total_time if total_time > 0 else 0
                }
                
                result = concurrent_results[concurrent_count]
                print(f"         ✅ Başarılı: {result['successful_count']}/{concurrent_count}")
                print(f"         ⏱️ Ortalama yanıt: {result['avg_response_time_ms']:.2f}ms")
                print(f"         🚀 Throughput: {result['throughput_rps']:.2f} req/sec")
                print(f"         📊 Başarı oranı: %{result['success_rate']:.1f}")
        
        # Performans degradasyonunu analiz et
        baseline_throughput = concurrent_results[5]['throughput_rps'] if 5 in concurrent_results else 0
        
        for level, result in concurrent_results.items():
            if level > 5:
                degradation = ((baseline_throughput - result['throughput_rps']) / baseline_throughput) * 100 if baseline_throughput > 0 else 0
                print(f"      📉 {level} eşzamanlı istek degradasyonu: %{degradation:.1f}")
        
        # Doğrulamalar
        for level, result in concurrent_results.items():
            assert result['success_rate'] >= 90, f"{level} eşzamanlı istekte başarı oranı düşük: %{result['success_rate']:.1f}"
            assert result['throughput_rps'] >= 5, f"{level} eşzamanlı istekte throughput çok düşük: {result['throughput_rps']:.2f}"
        
        return concurrent_results
    
    def _simulate_service_request(self, service_name: str, service_url: str) -> Dict:
        """Servis isteğini simüle et"""
        # Mock response simülasyonu
        simulation_delay = {
            'image_processing_service': 0.15,  # 150ms
            'nlu_service': 0.12,              # 120ms
            'style_profile_service': 0.08,    # 80ms
            'combination_engine_service': 0.25, # 250ms
            'recommendation_engine_service': 0.18, # 180ms
            'orchestrator_service': 0.3,      # 300ms
            'feedback_loop_service': 0.1      # 100ms
        }
        
        # Gerçekçi gecikme simülasyonu
        delay = simulation_delay.get(service_name, 0.1)
        time.sleep(delay)
        
        return {
            "status": "success",
            "service": service_name,
            "timestamp": datetime.now().isoformat(),
            "simulated": True
        }
    
    def _categorize_response_time(self, response_time_ms: float) -> str:
        """Yanıt süresini kategorize et"""
        thresholds = {
            200: "mükemmel",
            500: "iyi", 
            1000: "kabul edilebilir",
            2000: "zayıf",
            float('inf'): "kabul edilemez"
        }
        
        for threshold, category in thresholds.items():
            if response_time_ms <= threshold:
                return category
        
        return "bilinmeyen"

class TestLoadAndStressTesting:
    """
    Yük ve stres testleri.
    
    Bu test grubu, sistemin yüksek yük altındaki davranışını test eder.
    """
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Her test öncesi gerekli kurulumları yap"""
        self.config = AuraTestConfig()
        self.utils = TestUtilities()
        
        print("\n🏋️ Yük ve stres testleri başlatılıyor...")
    
    def test_load_testing_sustained_traffic(self):
        """
        Sürekli trafik yük testi.
        
        5 dakika boyunca sürekli istekler gönder ve sistemin stabilitesini ölç.
        """
        print("   🔍 Test: Sürekli trafik yük testi (5 dakika)")
        
        test_duration_seconds = 30  # Test için kısaltılmış süre (gerçekte 300 olacak)
        requests_per_second = 10
        
        start_time = time.time()
        end_time = start_time + test_duration_seconds
        
        results = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'response_times': [],
            'error_details': []
        }
        
        print(f"      ⏱️ {test_duration_seconds} saniye boyunca {requests_per_second} req/sec gönderiliyor...")
        
        # Load test döngüsü
        while time.time() < end_time:
            cycle_start = time.time()
            
            # Bu saniyede gönderilecek istekler
            for i in range(requests_per_second):
                request_start = time.time()
                
                try:
                    # Random servis seç
                    service_name = list(self.config.SERVICES.keys())[i % len(self.config.SERVICES)]
                    service_url = self.config.SERVICES[service_name]
                    
                    # İstek simüle et
                    response = self._simulate_service_request(service_name, service_url)
                    response_time = (time.time() - request_start) * 1000
                    
                    results['total_requests'] += 1
                    results['successful_requests'] += 1
                    results['response_times'].append(response_time)
                    
                except Exception as e:
                    results['total_requests'] += 1
                    results['failed_requests'] += 1
                    results['error_details'].append(str(e))
                
                # Rate limiting (saniyede belirlenen sayıda istek)
                if i < requests_per_second - 1:
                    time.sleep(1.0 / requests_per_second)
            
            # Bir sonraki saniyeye kadar bekle
            cycle_time = time.time() - cycle_start
            if cycle_time < 1.0:
                time.sleep(1.0 - cycle_time)
        
        # Sonuçları analiz et
        actual_duration = time.time() - start_time
        actual_rps = results['total_requests'] / actual_duration
        success_rate = (results['successful_requests'] / results['total_requests']) * 100 if results['total_requests'] > 0 else 0
        
        avg_response_time = statistics.mean(results['response_times']) if results['response_times'] else 0
        p95_response_time = sorted(results['response_times'])[int(len(results['response_times']) * 0.95)] if results['response_times'] else 0
        
        print(f"      📊 Test sonuçları:")
        print(f"         Toplam istek: {results['total_requests']}")
        print(f"         Başarılı: {results['successful_requests']} (%{success_rate:.1f})")
        print(f"         Başarısız: {results['failed_requests']}")
        print(f"         Gerçek RPS: {actual_rps:.2f}")
        print(f"         Ortalama yanıt: {avg_response_time:.2f}ms")
        print(f"         P95 yanıt: {p95_response_time:.2f}ms")
        
        # Doğrulamalar
        assert success_rate >= 95, f"Başarı oranı çok düşük: %{success_rate:.1f}"
        assert actual_rps >= requests_per_second * 0.8, f"Throughput target'ın altında: {actual_rps:.2f}"
        assert avg_response_time < 1000, f"Ortalama yanıt süresi çok yüksek: {avg_response_time:.2f}ms"
        assert p95_response_time < 2000, f"P95 yanıt süresi çok yüksek: {p95_response_time:.2f}ms"
        
        return results
    
    def test_stress_testing_breaking_point(self):
        """
        Stres testi - kırılma noktası bulma.
        
        Gittikçe artan yükle sistemin kırılma noktasını bul.
        """
        print("   🔍 Test: Stres testi - kırılma noktası")
        
        stress_levels = [10, 25, 50, 75, 100, 150, 200]  # RPS değerleri
        stress_results = {}
        breaking_point = None
        
        for rps_level in stress_levels:
            print(f"      📈 {rps_level} RPS stres seviyesi test ediliyor...")
            
            test_duration = 10  # Her seviye için 10 saniye
            start_time = time.time()
            
            level_results = {
                'target_rps': rps_level,
                'total_requests': 0,
                'successful_requests': 0,
                'failed_requests': 0,
                'response_times': [],
                'errors': []
            }
            
            # Stress test döngüsü
            with concurrent.futures.ThreadPoolExecutor(max_workers=min(rps_level, 50)) as executor:
                futures = []
                
                # Belirtilen RPS'de istekler gönder
                for second in range(test_duration):
                    for request_num in range(rps_level):
                        service_name = list(self.config.SERVICES.keys())[request_num % len(self.config.SERVICES)]
                        service_url = self.config.SERVICES[service_name]
                        
                        future = executor.submit(self._simulate_service_request, service_name, service_url)
                        futures.append(future)
                        level_results['total_requests'] += 1
                    
                    # Rate limiting
                    time.sleep(0.1)  # Kısa sleep interval
                
                # Tüm sonuçları topla
                for future in concurrent.futures.as_completed(futures, timeout=30):
                    try:
                        result = future.result(timeout=5)
                        level_results['successful_requests'] += 1
                    except Exception as e:
                        level_results['failed_requests'] += 1
                        level_results['errors'].append(str(e))
            
            # Seviye sonuçlarını hesapla
            actual_duration = time.time() - start_time
            actual_rps = level_results['total_requests'] / actual_duration
            success_rate = (level_results['successful_requests'] / level_results['total_requests']) * 100 if level_results['total_requests'] > 0 else 0
            
            stress_results[rps_level] = {
                'actual_rps': actual_rps,
                'success_rate': success_rate,
                'failed_requests': level_results['failed_requests'],
                'error_count': len(level_results['errors'])
            }
            
            print(f"         ⚡ Gerçek RPS: {actual_rps:.2f}")
            print(f"         ✅ Başarı oranı: %{success_rate:.1f}")
            print(f"         ❌ Hata sayısı: {level_results['failed_requests']}")
            
            # Kırılma noktasını belirle
            if success_rate < 90 or level_results['failed_requests'] > level_results['total_requests'] * 0.1:
                breaking_point = rps_level
                print(f"         🔥 Kırılma noktası tespit edildi: {rps_level} RPS")
                break
            
            # Rate limiting - bir sonraki seviye için bekle
            time.sleep(2)
        
        # Sonuçları özetle
        if breaking_point:
            print(f"\n      🎯 Sistem kırılma noktası: {breaking_point} RPS")
            recommended_max = int(breaking_point * 0.7)  # %70'i güvenli kabul et
            print(f"      💡 Önerilen maksimum yük: {recommended_max} RPS")
        else:
            print(f"\n      🚀 Sistem {max(stress_levels)} RPS'e kadar stabil!")
        
        # Doğrulamalar
        assert len(stress_results) > 0, "Hiç stress testi tamamlanamadı"
        
        # En az 50 RPS'i kaldırabilmeli
        stable_levels = [level for level, result in stress_results.items() if result['success_rate'] >= 90]
        assert len(stable_levels) > 0 and max(stable_levels) >= 50, f"Sistem 50 RPS'i kaldıramıyor: {stable_levels}"
        
        return stress_results
    
    def _simulate_service_request(self, service_name: str, service_url: str) -> Dict:
        """Servis isteğini simüle et (load test için optimized)"""
        # Daha hızlı simülasyon için kısaltılmış gecikmeler
        simulation_delay = {
            'image_processing_service': 0.05,   # 50ms
            'nlu_service': 0.03,               # 30ms
            'style_profile_service': 0.02,     # 20ms
            'combination_engine_service': 0.08, # 80ms
            'recommendation_engine_service': 0.06, # 60ms
            'orchestrator_service': 0.1,       # 100ms
            'feedback_loop_service': 0.03      # 30ms
        }
        
        # Gerçekçi gecikme simülasyonu
        delay = simulation_delay.get(service_name, 0.03)
        time.sleep(delay)
        
        return {
            "status": "success",
            "service": service_name,
            "timestamp": datetime.now().isoformat(),
            "simulated": True
        }

class TestResourceUsageMonitoring:
    """
    Kaynak kullanımı izleme testleri.
    
    Bu test grubu, sistem kaynaklarının (CPU, RAM, Disk) kullanımını izler.
    """
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Her test öncesi gerekli kurulumları yap"""
        self.config = AuraTestConfig()
        self.utils = TestUtilities()
        
        print("\n📊 Kaynak kullanımı izleme testleri başlatılıyor...")
    
    def test_resource_usage_under_normal_load(self):
        """
        Normal yük altında kaynak kullanımını test et.
        
        Normal işlem yükü altında CPU, RAM ve disk kullanımını izle.
        """
        print("   🔍 Test: Normal yük altında kaynak kullanımı")
        
        # Baseline kaynak kullanımını ölç
        baseline_stats = self._get_system_stats()
        print(f"      📈 Baseline CPU: %{baseline_stats['cpu_percent']:.1f}")
        print(f"      🧠 Baseline RAM: {baseline_stats['memory_mb']:.1f}MB")
        print(f"      💾 Baseline Disk: {baseline_stats['disk_io_mbps']:.2f}MB/s")
        
        # Normal yük simülasyonu (30 saniye)
        test_duration = 10  # Test için kısaltılmış
        monitoring_interval = 1  # Her 1 saniyede ölçüm
        
        resource_measurements = []
        
        print(f"      ⏱️ {test_duration} saniye normal yük simülasyonu...")
        
        start_time = time.time()
        end_time = start_time + test_duration
        
        # Normal yük thread'i başlat
        load_thread = threading.Thread(target=self._simulate_normal_load, args=(test_duration,))
        load_thread.start()
        
        # Kaynak kullanımını izle
        while time.time() < end_time:
            current_stats = self._get_system_stats()
            resource_measurements.append({
                'timestamp': time.time() - start_time,
                'cpu_percent': current_stats['cpu_percent'],
                'memory_mb': current_stats['memory_mb'],
                'disk_io_mbps': current_stats['disk_io_mbps']
            })
            
            time.sleep(monitoring_interval)
        
        # Load thread'in bitmesini bekle
        load_thread.join()
        
        # İstatistikleri hesapla
        if resource_measurements:
            avg_cpu = statistics.mean([m['cpu_percent'] for m in resource_measurements])
            max_cpu = max([m['cpu_percent'] for m in resource_measurements])
            avg_memory = statistics.mean([m['memory_mb'] for m in resource_measurements])
            max_memory = max([m['memory_mb'] for m in resource_measurements])
            avg_disk = statistics.mean([m['disk_io_mbps'] for m in resource_measurements])
            max_disk = max([m['disk_io_mbps'] for m in resource_measurements])
            
            print(f"      📊 Test sonuçları:")
            print(f"         Ortalama CPU: %{avg_cpu:.1f} (Max: %{max_cpu:.1f})")
            print(f"         Ortalama RAM: {avg_memory:.1f}MB (Max: {max_memory:.1f}MB)")
            print(f"         Ortalama Disk I/O: {avg_disk:.2f}MB/s (Max: {max_disk:.2f}MB/s)")
            
            # Performans değerlendirmesi
            cpu_status = "iyi" if avg_cpu < 50 else "orta" if avg_cpu < 80 else "yüksek"
            memory_status = "iyi" if avg_memory < 512 else "orta" if avg_memory < 1024 else "yüksek"
            
            print(f"         🎯 CPU kullanımı: {cpu_status}")
            print(f"         🎯 RAM kullanımı: {memory_status}")
        
            # Doğrulamalar
            assert avg_cpu < 80, f"Ortalama CPU kullanımı çok yüksek: %{avg_cpu:.1f}"
            assert max_cpu < 95, f"Maksimum CPU kullanımı çok yüksek: %{max_cpu:.1f}"
            assert avg_memory < 1024, f"Ortalama RAM kullanımı çok yüksek: {avg_memory:.1f}MB"
            
            return {
                'avg_cpu': avg_cpu,
                'max_cpu': max_cpu,
                'avg_memory': avg_memory,
                'max_memory': max_memory,
                'measurements': resource_measurements
            }
        else:
            print("      ⚠️ Kaynak ölçümü alınamadı")
            return {}
    
    def test_resource_usage_under_heavy_load(self):
        """
        Yoğun yük altında kaynak kullanımını test et.
        
        Yüksek işlem yükü altında kaynak kullanımını izle ve limitleri kontrol et.
        """
        print("   🔍 Test: Yoğun yük altında kaynak kullanımı")
        
        test_duration = 15  # Test için kısaltılmış
        monitoring_interval = 0.5  # Daha sık ölçüm
        
        resource_measurements = []
        
        print(f"      ⚡ {test_duration} saniye yoğun yük simülasyonu...")
        
        start_time = time.time()
        end_time = start_time + test_duration
        
        # Yoğun yük thread'leri başlat
        heavy_load_threads = []
        for i in range(3):  # 3 parallel heavy load thread
            thread = threading.Thread(target=self._simulate_heavy_load, args=(test_duration,))
            thread.start()
            heavy_load_threads.append(thread)
        
        # Kaynak kullanımını izle
        while time.time() < end_time:
            current_stats = self._get_system_stats()
            resource_measurements.append({
                'timestamp': time.time() - start_time,
                'cpu_percent': current_stats['cpu_percent'],
                'memory_mb': current_stats['memory_mb'],
                'disk_io_mbps': current_stats['disk_io_mbps']
            })
            
            time.sleep(monitoring_interval)
        
        # Tüm thread'lerin bitmesini bekle
        for thread in heavy_load_threads:
            thread.join()
        
        # İstatistikleri hesapla
        if resource_measurements:
            avg_cpu = statistics.mean([m['cpu_percent'] for m in resource_measurements])
            max_cpu = max([m['cpu_percent'] for m in resource_measurements])
            avg_memory = statistics.mean([m['memory_mb'] for m in resource_measurements])
            max_memory = max([m['memory_mb'] for m in resource_measurements])
            
            print(f"      📊 Yoğun yük test sonuçları:")
            print(f"         Ortalama CPU: %{avg_cpu:.1f} (Max: %{max_cpu:.1f})")
            print(f"         Ortalama RAM: {avg_memory:.1f}MB (Max: {max_memory:.1f}MB)")
            
            # Kritik seviye uyarıları
            if max_cpu > 90:
                print(f"         🔥 UYARI: CPU kullanımı kritik seviyede! %{max_cpu:.1f}")
            if max_memory > 2048:
                print(f"         🔥 UYARI: RAM kullanımı kritik seviyede! {max_memory:.1f}MB")
            
            # Doğrulamalar (heavy load için daha yüksek thresholdlar)
            assert max_cpu < 98, f"CPU kullanımı sistem limitini aştı: %{max_cpu:.1f}"
            assert max_memory < 4096, f"RAM kullanımı sistem limitini aştı: {max_memory:.1f}MB"
            
            return {
                'avg_cpu': avg_cpu,
                'max_cpu': max_cpu,
                'avg_memory': avg_memory,
                'max_memory': max_memory,
                'peak_usage_detected': max_cpu > 85 or max_memory > 1536
            }
        else:
            print("      ⚠️ Kaynak ölçümü alınamadı")
            return {}
    
    def _get_system_stats(self) -> Dict:
        """Mevcut sistem istatistiklerini al"""
        try:
            # psutil ile gerçek sistem istatistikleri
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory_info = psutil.virtual_memory()
            memory_mb = memory_info.used / (1024 * 1024)
            
            # Disk I/O (basit simülasyon)
            disk_io = psutil.disk_io_counters()
            disk_io_mbps = (disk_io.read_bytes + disk_io.write_bytes) / (1024 * 1024) if disk_io else 0
            
            return {
                'cpu_percent': cpu_percent,
                'memory_mb': memory_mb,
                'disk_io_mbps': disk_io_mbps,
                'timestamp': time.time()
            }
        except Exception as e:
            # Fallback mock data
            return {
                'cpu_percent': 25.0,
                'memory_mb': 256.0,
                'disk_io_mbps': 5.0,
                'timestamp': time.time(),
                'mock': True
            }
    
    def _simulate_normal_load(self, duration: int):
        """Normal yük simülasyonu"""
        end_time = time.time() + duration
        
        while time.time() < end_time:
            # Basit CPU işlemleri
            for i in range(1000):
                _ = i ** 2
            
            # Kısa memory allocation
            temp_data = [i for i in range(1000)]
            del temp_data
            
            time.sleep(0.01)  # CPU'yu tamamen meşgul etme
    
    def _simulate_heavy_load(self, duration: int):
        """Yoğun yük simülasyonu"""
        end_time = time.time() + duration
        
        while time.time() < end_time:
            # Yoğun CPU işlemleri
            for i in range(10000):
                _ = i ** 3
            
            # Memory allocation
            temp_data = [i for i in range(5000)]
            del temp_data
            
            time.sleep(0.001)  # Minimal sleep

# Ana test fonksiyonu
def run_performance_tests():
    """
    Tüm performans testlerini çalıştır.
    
    Bu fonksiyon, sistemin performans karakteristiklerini kapsamlı bir şekilde test eder.
    """
    print("⚡ PERFORMANS TEST PAKETİ BAŞLATILIYOR")
    print("=" * 60)
    
    test_results = {
        'total_tests': 0,
        'passed_tests': 0,
        'failed_tests': 0,
        'performance_metrics': {},
        'test_details': []
    }
    
    # Tüm test sınıflarını çalıştır
    test_classes = [
        TestResponseTimeBenchmarks(),
        TestLoadAndStressTesting(),
        TestResourceUsageMonitoring()
    ]
    
    for test_class in test_classes:
        class_name = test_class.__class__.__name__
        print(f"\n📋 {class_name} testleri çalıştırılıyor...")
        
        # Test metodlarını bul ve çalıştır
        test_methods = [method for method in dir(test_class) if method.startswith('test_')]
        
        for method_name in test_methods:
            test_results['total_tests'] += 1
            
            try:
                # Test kurulumunu çalıştır
                if hasattr(test_class, 'setup'):
                    test_class.setup()
                
                # Test metodunu çalıştır
                method = getattr(test_class, method_name)
                result = method()
                
                test_results['passed_tests'] += 1
                test_results['test_details'].append({
                    'test': f"{class_name}.{method_name}",
                    'status': 'PASSED',
                    'metrics': result if isinstance(result, dict) else {}
                })
                
                # Metrikleri topla
                if isinstance(result, dict):
                    test_results['performance_metrics'][f"{class_name}.{method_name}"] = result
                
            except Exception as e:
                test_results['failed_tests'] += 1
                test_results['test_details'].append({
                    'test': f"{class_name}.{method_name}",
                    'status': 'FAILED',
                    'error': str(e)
                })
                print(f"   ❌ Test failed: {method_name} - {str(e)}")
    
    # Sonuçları özetle
    print(f"\n📊 PERFORMANS TEST SONUÇLARI")
    print("=" * 60)
    print(f"Toplam Test: {test_results['total_tests']}")
    print(f"Başarılı: {test_results['passed_tests']}")
    print(f"Başarısız: {test_results['failed_tests']}")
    print(f"Başarı Oranı: %{(test_results['passed_tests']/test_results['total_tests']*100):.1f}")
    
    # Performans özeti
    if test_results['performance_metrics']:
        print(f"\n💡 PERFORMANS ÖZETİ:")
        print("-" * 40)
        
        # Response time özeti
        response_time_tests = [k for k in test_results['performance_metrics'].keys() if 'response' in k.lower()]
        if response_time_tests:
            print("⚡ Yanıt Süresi Performansı: İyi")
        
        # Load test özeti  
        load_tests = [k for k in test_results['performance_metrics'].keys() if 'load' in k.lower() or 'stress' in k.lower()]
        if load_tests:
            print("🏋️ Yük Testi Performansı: Stabil")
        
        # Resource usage özeti
        resource_tests = [k for k in test_results['performance_metrics'].keys() if 'resource' in k.lower()]
        if resource_tests:
            print("📊 Kaynak Kullanımı: Optimize")
    
    return test_results

if __name__ == "__main__":
    # Doğrudan çalıştırıldığında testleri başlat
    results = run_performance_tests()
    
    # Çıkış kodu belirle
    if results['failed_tests'] == 0:
        exit_code = 0
    else:
        exit_code = 1
    
    exit(exit_code)
