# 🤖 AURA AI SİSTEMİ - OTOMATİK TEST VE RAPOR SİSTEMİ
# Test Odaklı Geri Besleme Döngüsü (AlphaCodium/SED) Otomasyon Platformu

import os
import sys
import time
import json
import subprocess
import schedule
import shutil
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

class AuraTestAutomation:
    """
    Aura AI sistemi için otomatik test ve raporlama platformu.
    
    Bu sınıf, testlerin otomatik çalıştırılması, raporların oluşturulması
    ve sonuçların ilgili kişilere iletilmesi işlemlerini yönetir.
    """
    
    def __init__(self, config_file: Optional[str] = None):
        # Konfigürasyon dosyasını yükle
        self.config = self._load_configuration(config_file)
        
        # Test sonuçları ve raporlar için dizinler
        self.base_dir = Path(__file__).parent.parent
        self.reports_dir = self.base_dir / "tests" / "reports"
        self.archive_dir = self.reports_dir / "archive"
        self.logs_dir = self.base_dir / "logs"
        
        # Dizinleri oluştur
        self._ensure_directories()
        
        # Test scheduling durumu
        self.is_scheduled = False
        self.current_schedule = {}
        
        print("🤖 AURA AI OTOMATİK TEST SİSTEMİ")
        print("=" * 50)
        print("📅 Sistem başlatıldı:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print("📁 Rapor dizini:", self.reports_dir)
        print("📊 Test otomasyonu hazır!")
        print("=" * 50)
    
    def _load_configuration(self, config_file: Optional[str]) -> Dict:
        """Test otomasyon konfigürasyonunu yükle"""
        default_config = {
            "test_schedule": {
                "daily_full_tests": "02:00",  # Her gün saat 02:00'da tam test
                "hourly_health_checks": True,  # Her saatte sağlık kontrolü
                "weekly_performance_tests": "Sunday 01:00",  # Haftalık performans testi
                "continuous_monitoring": True  # Sürekli izleme aktif
            },
            "test_types": {
                "unit_tests": True,
                "integration_tests": True,
                "e2e_tests": True,
                "fault_tolerance_tests": True,
                "performance_tests": True
            },
            "reporting": {
                "html_reports": True,
                "json_reports": True,
                "email_notifications": False,  # E-posta bildirimleri kapalı (demo için)
                "slack_notifications": False,  # Slack bildirimleri kapalı
                "dashboard_updates": True
            },
            "thresholds": {
                "max_failure_rate": 5,  # %5'den fazla başarısızlık varsa alarm
                "max_response_time_ms": 2000,  # 2 saniyeden uzun yanıt süresi alarm
                "min_uptime_percentage": 99.5  # %99.5'den az uptime alarm
            },
            "retention": {
                "keep_daily_reports_days": 30,  # 30 gün günlük rapor sakla
                "keep_weekly_reports_weeks": 12,  # 12 hafta haftalık rapor sakla
                "archive_old_reports": True
            }
        }
        
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"⚠️ Konfigürasyon dosyası yüklenemedi: {e}")
                print("🔧 Varsayılan konfigürasyon kullanılıyor")
        
        return default_config
    
    def _ensure_directories(self):
        """Gerekli dizinleri oluştur"""
        directories = [
            self.reports_dir,
            self.archive_dir,
            self.logs_dir,
            self.reports_dir / "daily",
            self.reports_dir / "weekly",
            self.reports_dir / "hourly",
            self.reports_dir / "html"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def start_scheduled_testing(self):
        """
        Zamanlanmış testlerin çalıştırılmasını başlat.
        
        Bu fonksiyon, konfigürasyona göre testleri otomatik olarak zamanlar.
        """
        print("\n⏰ ZAMANLANMIŞ TEST SİSTEMİ BAŞLATILIYOR")
        print("-" * 50)
        
        # Günlük tam testler
        if self.config["test_schedule"]["daily_full_tests"]:
            daily_time = self.config["test_schedule"]["daily_full_tests"]
            schedule.every().day.at(daily_time).do(self.run_full_test_suite)
            print(f"📅 Günlük tam testler zamanlandı: Her gün {daily_time}")
        
        # Saatlik sağlık kontrolleri
        if self.config["test_schedule"]["hourly_health_checks"]:
            schedule.every().hour.do(self.run_health_check_suite)
            print(f"🏥 Saatlik sağlık kontrolleri zamanlandı: Her saat")
        
        # Haftalık performans testleri
        if self.config["test_schedule"]["weekly_performance_tests"]:
            weekly_schedule = self.config["test_schedule"]["weekly_performance_tests"]
            day, time_str = weekly_schedule.split(" ")
            
            schedule_func = getattr(schedule.every(), day.lower())
            schedule_func.at(time_str).do(self.run_performance_test_suite)
            print(f"📊 Haftalık performans testleri zamanlandı: {weekly_schedule}")
        
        # Sürekli izleme
        if self.config["test_schedule"]["continuous_monitoring"]:
            schedule.every(15).minutes.do(self.run_monitoring_check)
            print(f"🔍 Sürekli izleme zamanlandı: Her 15 dakikada")
        
        self.is_scheduled = True
        self.current_schedule = {
            "daily_full_tests": self.config["test_schedule"]["daily_full_tests"],
            "hourly_health_checks": self.config["test_schedule"]["hourly_health_checks"],
            "weekly_performance_tests": self.config["test_schedule"]["weekly_performance_tests"],
            "continuous_monitoring": self.config["test_schedule"]["continuous_monitoring"]
        }
        
        print("\n✅ Zamanlanmış testler aktif!")
        print("🔄 Testler otomatik olarak çalışacak")
        
        return True
    
    def run_scheduled_tests_loop(self):
        """
        Zamanlanmış testlerin ana döngüsü.
        
        Bu fonksiyon, schedule kütüphanesi ile zamanlanmış testleri sürekli kontrol eder.
        """
        if not self.is_scheduled:
            print("⚠️ Önce zamanlanmış testleri başlatın: start_scheduled_testing()")
            return
        
        print("\n🔄 ZAMANLANMIŞ TEST DÖNGÜSÜ BAŞLADI")
        print("=" * 50)
        print("⌚ Testler zamanlarına göre otomatik çalışacak")
        print("⏹️ Durdurmak için Ctrl+C kullanın")
        print("=" * 50)
        
        try:
            while True:
                # Zamanlanmış testleri kontrol et ve çalıştır
                schedule.run_pending()
                
                # 60 saniye bekle
                time.sleep(60)
                
                # Her saatte bir durum raporu
                current_time = datetime.now()
                if current_time.minute == 0:
                    self._print_scheduler_status()
        
        except KeyboardInterrupt:
            print("\n⏹️ Zamanlanmış testler durduruldu")
            print("📊 Son rapor oluşturuluyor...")
            self._generate_scheduler_summary()
    
    def run_full_test_suite(self):
        """
        Tam test paketini çalıştır.
        
        Bu fonksiyon, tüm test türlerini sırasıyla çalıştırır ve kapsamlı rapor oluşturur.
        """
        print("\n🧪 TAM TEST PAKETİ ÇALIŞILIYOR")
        print("=" * 50)
        print("📅 Başlama zamanı:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        test_start_time = time.time()
        
        # Test sonuçlarını toplamak için
        full_test_results = {
            "test_suite": "full_test_suite",
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "total_duration_ms": 0,
            "test_types": {},
            "overall_status": "running",
            "summary": {}
        }
        
        # 1. Unit testleri çalıştır
        if self.config["test_types"]["unit_tests"]:
            print("\n🔬 Unit testleri çalıştırılıyor...")
            unit_results = self._run_test_type("unit")
            full_test_results["test_types"]["unit_tests"] = unit_results
        
        # 2. Integration testleri çalıştır
        if self.config["test_types"]["integration_tests"]:
            print("\n🔗 Integration testleri çalıştırılıyor...")
            integration_results = self._run_test_type("integration")
            full_test_results["test_types"]["integration_tests"] = integration_results
        
        # 3. End-to-end testleri çalıştır
        if self.config["test_types"]["e2e_tests"]:
            print("\n🎬 End-to-end testleri çalıştırılıyor...")
            e2e_results = self._run_test_type("e2e")
            full_test_results["test_types"]["e2e_tests"] = e2e_results
        
        # 4. Fault tolerance testleri çalıştır
        if self.config["test_types"]["fault_tolerance_tests"]:
            print("\n🛡️ Fault tolerance testleri çalıştırılıyor...")
            fault_results = self._run_test_type("fault_tolerance")
            full_test_results["test_types"]["fault_tolerance_tests"] = fault_results
        
        # 5. Performance testleri çalıştır
        if self.config["test_types"]["performance_tests"]:
            print("\n⚡ Performance testleri çalıştırılıyor...")
            performance_results = self._run_test_type("performance")
            full_test_results["test_types"]["performance_tests"] = performance_results
        
        # Test süresini hesapla
        test_duration = time.time() - test_start_time
        full_test_results["end_time"] = datetime.now().isoformat()
        full_test_results["total_duration_ms"] = test_duration * 1000
        
        # Genel durumu belirle
        overall_status = self._determine_overall_status(full_test_results["test_types"])
        full_test_results["overall_status"] = overall_status
        
        # Özet bilgileri oluştur
        full_test_results["summary"] = self._generate_test_summary(full_test_results["test_types"])
        
        # Rapor oluştur
        report_file = self._generate_full_test_report(full_test_results)
        
        print(f"\n📊 TAM TEST PAKETİ TAMAMLANDI")
        print("=" * 50) 
        print(f"⏱️ Toplam süre: {test_duration:.2f} saniye")
        print(f"🎯 Genel durum: {overall_status.upper()}")
        print(f"📄 Rapor dosyası: {report_file}")
        print("=" * 50)
        
        # Alarm kontrolü
        self._check_test_alarms(full_test_results)
        
        return full_test_results
    
    def run_health_check_suite(self):
        """
        Sağlık kontrolü test paketini çalıştır.
        
        Bu fonksiyon, sistemin temel sağlığını hızlıca kontrol eder.
        """
        print("\n🏥 SAĞLIK KONTROLÜ PAKETİ ÇALIŞILIYOR")
        print("-" * 40)
        
        health_start_time = time.time()
        
        health_results = {
            "test_suite": "health_check_suite",
            "start_time": datetime.now().isoformat(),
            "services_checked": {},
            "overall_health": "unknown"
        }
        
        # Servis sağlık kontrolleri (mock)
        services = [
            "image_processing_service",
            "nlu_service", 
            "style_profile_service",
            "combination_engine_service",
            "recommendation_engine_service",
            "orchestrator_service",
            "feedback_loop_service"
        ]
        
        healthy_services = 0
        total_services = len(services)
        
        for service in services:
            print(f"   🔍 {service} kontrol ediliyor...")
            
            # Mock health check (gerçekte HTTP request olacak)
            is_healthy = self._mock_service_health_check(service)
            response_time = 150 + (hash(service) % 200)  # Mock response time
            
            health_results["services_checked"][service] = {
                "healthy": is_healthy,
                "response_time_ms": response_time,
                "status": "healthy" if is_healthy else "unhealthy"
            }
            
            if is_healthy:
                healthy_services += 1
                print(f"      ✅ Sağlıklı ({response_time}ms)")
            else:
                print(f"      ❌ Sağlıksız")
        
        # Genel sağlık durumunu belirle
        health_percentage = (healthy_services / total_services) * 100
        
        if health_percentage >= 95:
            overall_health = "excellent"
        elif health_percentage >= 80:
            overall_health = "good"
        elif health_percentage >= 60:
            overall_health = "warning"
        else:
            overall_health = "critical"
        
        health_results["overall_health"] = overall_health
        health_results["healthy_services"] = healthy_services
        health_results["total_services"] = total_services
        health_results["health_percentage"] = health_percentage
        health_results["end_time"] = datetime.now().isoformat()
        health_results["duration_ms"] = (time.time() - health_start_time) * 1000
        
        # Sağlık raporu oluştur
        health_report_file = self._generate_health_report(health_results)
        
        print(f"\n📊 SAĞLIK KONTROLÜ TAMAMLANDI")
        print("-" * 40)
        print(f"⏱️ Süre: {health_results['duration_ms']:.2f}ms")
        print(f"🎯 Genel sağlık: {overall_health.upper()}")
        print(f"📈 Sağlık oranı: %{health_percentage:.1f} ({healthy_services}/{total_services})")
        print(f"📄 Rapor: {health_report_file}")
        
        # Sağlık alarmları
        if health_percentage < 90:
            print(f"🚨 ALARM: Sistem sağlığı düşük! %{health_percentage:.1f}")
        
        return health_results
    
    def run_performance_test_suite(self):
        """
        Performans test paketini çalıştır.
        
        Bu fonksiyon, sistemin performans metriklerini detaylı olarak test eder.
        """
        print("\n⚡ PERFORMANS TEST PAKETİ ÇALIŞILIYOR")
        print("-" * 40)
        
        perf_start_time = time.time()
        
        performance_results = {
            "test_suite": "performance_test_suite",
            "start_time": datetime.now().isoformat(),
            "performance_metrics": {},
            "benchmarks": {}
        }
        
        # 1. Response time benchmarks
        print("   📊 Yanıt süresi benchmarkları...")
        response_benchmarks = self._run_response_time_benchmarks()
        performance_results["benchmarks"]["response_times"] = response_benchmarks
        
        # 2. Throughput tests
        print("   🚀 Throughput testleri...")
        throughput_results = self._run_throughput_tests()
        performance_results["benchmarks"]["throughput"] = throughput_results
        
        # 3. Load tests
        print("   🏋️ Yük testleri...")
        load_results = self._run_load_tests()
        performance_results["benchmarks"]["load_handling"] = load_results
        
        # 4. Resource usage
        print("   📈 Kaynak kullanımı...")
        resource_results = self._monitor_resource_usage()
        performance_results["benchmarks"]["resource_usage"] = resource_results
        
        # Performans skorunu hesapla
        performance_score = self._calculate_performance_score(performance_results["benchmarks"])
        performance_results["overall_score"] = performance_score
        performance_results["performance_grade"] = self._grade_performance(performance_score)
        
        performance_results["end_time"] = datetime.now().isoformat()
        performance_results["duration_ms"] = (time.time() - perf_start_time) * 1000
        
        # Performans raporu oluştur
        perf_report_file = self._generate_performance_report(performance_results)
        
        print(f"\n📊 PERFORMANS TESTLERİ TAMAMLANDI")
        print("-" * 40)
        print(f"⏱️ Süre: {performance_results['duration_ms']:.2f}ms")
        print(f"🏆 Performans skoru: {performance_score:.1f}/100")
        print(f"🎯 Performans notu: {performance_results['performance_grade']}")
        print(f"📄 Rapor: {perf_report_file}")
        
        return performance_results
    
    def run_monitoring_check(self):
        """
        Kısa monitoring kontrolü çalıştır.
        
        Bu fonksiyon, sistemin anlık durumunu hızlıca kontrol eder.
        """
        print(f"\n🔍 MONITORING KONTROLÜ - {datetime.now().strftime('%H:%M:%S')}")
        
        monitoring_results = {
            "timestamp": datetime.now().isoformat(),
            "quick_checks": {}
        }
        
        # Hızlı sistem kontrolleri
        checks = {
            "system_uptime": self._check_system_uptime(),
            "service_connectivity": self._check_service_connectivity(), 
            "response_times": self._check_quick_response_times(),
            "error_rates": self._check_error_rates()
        }
        
        monitoring_results["quick_checks"] = checks
        
        # Kritik durumları kontrol et
        critical_issues = []
        for check_name, check_result in checks.items():
            if check_result.get("status") == "critical":
                critical_issues.append(f"{check_name}: {check_result.get('message', 'Unknown issue')}")
        
        if critical_issues:
            print("🚨 KRİTİK SORUNLAR TESPİT EDİLDİ:")
            for issue in critical_issues:
                print(f"   ❌ {issue}")
        else:
            print("   ✅ Tüm kontrollerden geçti")
        
        # Monitoring log'a kaydet
        self._log_monitoring_result(monitoring_results)
        
        return monitoring_results
    
    def _run_test_type(self, test_type: str) -> Dict:
        """Belirli bir test türünü çalıştır"""
        try:
            # Mock test execution (gerçekte pytest subprocess çalıştırılacak)
            test_start = time.time()
            
            # Test türüne göre simüle edilmiş sonuçlar
            mock_results = {
                "unit": {
                    "total_tests": 45,
                    "passed": 43,
                    "failed": 2,
                    "skipped": 0,
                    "duration_ms": 2340
                },
                "integration": {
                    "total_tests": 12, 
                    "passed": 11,
                    "failed": 1,
                    "skipped": 0,
                    "duration_ms": 8700
                },
                "e2e": {
                    "total_tests": 8,
                    "passed": 8,
                    "failed": 0,
                    "skipped": 0,
                    "duration_ms": 15600
                },
                "fault_tolerance": {
                    "total_tests": 15,
                    "passed": 14,
                    "failed": 1,
                    "skipped": 0,
                    "duration_ms": 5200
                },
                "performance": {
                    "total_tests": 10,
                    "passed": 9,
                    "failed": 1,
                    "skipped": 0,
                    "duration_ms": 25800
                }
            }
            
            result = mock_results.get(test_type, {
                "total_tests": 5,
                "passed": 4,
                "failed": 1,
                "skipped": 0,
                "duration_ms": 3000
            })
            
            # Başarı oranını hesapla
            if result["total_tests"] > 0:
                success_rate = (result["passed"] / result["total_tests"]) * 100
            else:
                success_rate = 0
            
            result["success_rate"] = success_rate
            result["status"] = "passed" if success_rate >= 90 else "failed" if success_rate < 70 else "warning"
            
            actual_duration = (time.time() - test_start) * 1000
            print(f"      ✅ {test_type} testleri tamamlandı ({actual_duration:.0f}ms)")
            print(f"         📊 {result['passed']}/{result['total_tests']} test başarılı (%{success_rate:.1f})")
            
            return result
            
        except Exception as e:
            print(f"      ❌ {test_type} testleri başarısız: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "success_rate": 0
            }
    
    def _mock_service_health_check(self, service_name: str) -> bool:
        """Mock servis sağlık kontrolü"""
        # Hash'e dayalı deterministic ama realistic sonuçlar
        health_score = hash(service_name + str(int(time.time() / 3600))) % 100
        return health_score > 15  # %85 uptime simülasyonu
    
    def _determine_overall_status(self, test_results: Dict) -> str:
        """Test sonuçlarından genel durumu belirle"""
        if not test_results:
            return "no_tests"
        
        statuses = [result.get("status", "unknown") for result in test_results.values()]
        
        if all(status == "passed" for status in statuses):
            return "passed"
        elif any(status == "error" for status in statuses):
            return "error"
        elif any(status == "failed" for status in statuses):
            return "failed"
        else:
            return "warning"
    
    def _generate_test_summary(self, test_results: Dict) -> Dict:
        """Test sonuçlarından özet bilgiler oluştur"""
        summary = {
            "total_test_suites": len(test_results),
            "total_tests": 0,
            "total_passed": 0,
            "total_failed": 0,
            "total_skipped": 0,
            "overall_success_rate": 0
        }
        
        for result in test_results.values():
            summary["total_tests"] += result.get("total_tests", 0)
            summary["total_passed"] += result.get("passed", 0)
            summary["total_failed"] += result.get("failed", 0)
            summary["total_skipped"] += result.get("skipped", 0)
        
        if summary["total_tests"] > 0:
            summary["overall_success_rate"] = (summary["total_passed"] / summary["total_tests"]) * 100
        
        return summary
    
    def _generate_full_test_report(self, test_results: Dict) -> str:
        """Tam test raporu oluştur"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f"full_test_report_{timestamp}.json"
        report_filepath = self.reports_dir / "daily" / report_filename
        
        # JSON raporu kaydet
        with open(report_filepath, 'w', encoding='utf-8') as f:
            json.dump(test_results, f, indent=2, ensure_ascii=False)
        
        # HTML raporu da oluştur
        if self.config["reporting"]["html_reports"]:
            html_filename = f"full_test_report_{timestamp}.html"
            html_filepath = self.reports_dir / "html" / html_filename
            self._generate_html_report(test_results, html_filepath)
        
        return str(report_filepath)
    
    def _generate_health_report(self, health_results: Dict) -> str:
        """Sağlık kontrolü raporu oluştur"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f"health_check_{timestamp}.json"
        report_filepath = self.reports_dir / "hourly" / report_filename
        
        with open(report_filepath, 'w', encoding='utf-8') as f:
            json.dump(health_results, f, indent=2, ensure_ascii=False)
        
        return str(report_filepath)
    
    def _generate_performance_report(self, perf_results: Dict) -> str:
        """Performans test raporu oluştur"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f"performance_report_{timestamp}.json"
        report_filepath = self.reports_dir / "weekly" / report_filename
        
        with open(report_filepath, 'w', encoding='utf-8') as f:
            json.dump(perf_results, f, indent=2, ensure_ascii=False)
        
        return str(report_filepath)
    
    def _generate_html_report(self, test_results: Dict, output_file: Path):
        """HTML formatında rapor oluştur"""
        html_content = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aura AI Test Raporu</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; color: #333; }}
        .status-passed {{ color: #28a745; }}
        .status-failed {{ color: #dc3545; }}
        .status-warning {{ color: #ffc107; }}
        .metric {{ display: inline-block; margin: 10px; padding: 15px; background: #f8f9fa; border-radius: 5px; text-align: center; }}
        .test-suite {{ margin: 20px 0; padding: 15px; border-left: 4px solid #007bff; background: #f8f9fa; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #343a40; color: white; }}
        .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 Aura AI Sistem Test Raporu</h1>
            <p>Test Tarihi: {test_results.get('start_time', 'N/A')}</p>
            <p class="status-{test_results.get('overall_status', 'unknown').lower()}">
                Genel Durum: {test_results.get('overall_status', 'UNKNOWN').upper()}
            </p>
        </div>
        
        <div class="metrics">
            <div class="metric">
                <h3>⏱️ Toplam Süre</h3>
                <p>{test_results.get('total_duration_ms', 0)/1000:.2f} saniye</p>
            </div>
            <div class="metric">
                <h3>📊 Test Türleri</h3>
                <p>{len(test_results.get('test_types', {}))}</p>
            </div>
            <div class="metric">
                <h3>✅ Başarı Oranı</h3>
                <p>%{test_results.get('summary', {}).get('overall_success_rate', 0):.1f}</p>
            </div>
        </div>
        
        <h2>📋 Test Sonuçları Detayı</h2>
        <table>
            <thead>
                <tr>
                    <th>Test Türü</th>
                    <th>Durum</th>
                    <th>Toplam</th>
                    <th>Başarılı</th>
                    <th>Başarısız</th>
                    <th>Başarı Oranı</th>
                </tr>
            </thead>
            <tbody>
"""
        
        # Test türleri tablosunu doldur
        for test_type, results in test_results.get('test_types', {}).items():
            status_class = f"status-{results.get('status', 'unknown').lower()}"
            html_content += f"""
                <tr>
                    <td>{test_type.replace('_', ' ').title()}</td>
                    <td class="{status_class}">{results.get('status', 'UNKNOWN').upper()}</td>
                    <td>{results.get('total_tests', 0)}</td>
                    <td>{results.get('passed', 0)}</td>
                    <td>{results.get('failed', 0)}</td>
                    <td>%{results.get('success_rate', 0):.1f}</td>
                </tr>
"""
        
        html_content += f"""
            </tbody>
        </table>
        
        <div class="footer">
            <p>Bu rapor Aura AI Test Otomasyon Sistemi tarafından otomatik olarak oluşturulmuştur.</p>
            <p>Rapor oluşturulma zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _check_test_alarms(self, test_results: Dict):
        """Test sonuçlarında alarm durumlarını kontrol et"""
        summary = test_results.get('summary', {})
        overall_success_rate = summary.get('overall_success_rate', 0)
        
        # Başarı oranı alarm kontrolü
        if overall_success_rate < (100 - self.config['thresholds']['max_failure_rate']):
            print(f"🚨 ALARM: Test başarı oranı çok düşük! %{overall_success_rate:.1f}")
            self._send_alarm_notification("Test Başarı Oranı Düşük", f"Başarı oranı: %{overall_success_rate:.1f}")
        
        # Duration alarm kontrolü  
        total_duration_ms = test_results.get('total_duration_ms', 0)
        if total_duration_ms > (self.config['thresholds']['max_response_time_ms'] * 10):  # Test suite 10x threshold
            print(f"🚨 ALARM: Test süresi çok uzun! {total_duration_ms/1000:.2f} saniye")
            self._send_alarm_notification("Test Süresi Uzun", f"Süre: {total_duration_ms/1000:.2f}s")
    
    def _send_alarm_notification(self, title: str, message: str):
        """Alarm bildirimi gönder"""
        # Demo için sadece log'a yaz
        alarm_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        alarm_log = f"[{alarm_time}] ALARM: {title} - {message}\n"
        
        alarm_log_file = self.logs_dir / "alarms.log"
        with open(alarm_log_file, 'a', encoding='utf-8') as f:
            f.write(alarm_log)
    
    def _print_scheduler_status(self):
        """Scheduler durumunu yazdır"""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n📅 Scheduler Durumu ({current_time}):")
        print(f"   🔄 Aktif zamanlamalar: {len(schedule.jobs)}")
        
        # Bir sonraki çalışacak job'ları göster
        next_jobs = sorted(schedule.jobs, key=lambda x: x.next_run)[:3]
        print(f"   ⏰ Sonraki testler:")
        for job in next_jobs:
            print(f"      - {job.next_run.strftime('%H:%M')} - {job.job_func.__name__}")
    
    def _generate_scheduler_summary(self):
        """Scheduler özet raporu oluştur"""
        summary = {
            "scheduler_session": {
                "start_time": datetime.now().isoformat(),
                "total_scheduled_jobs": len(schedule.jobs),
                "active_schedules": self.current_schedule
            }
        }
        
        summary_file = self.reports_dir / f"scheduler_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Scheduler özet raporu: {summary_file}")
    
    # Mock performance test functions
    def _run_response_time_benchmarks(self) -> Dict:
        return {"avg_response_ms": 245, "p95_response_ms": 890, "status": "good"}
    
    def _run_throughput_tests(self) -> Dict:
        return {"requests_per_second": 67, "concurrent_users": 25, "status": "good"}
    
    def _run_load_tests(self) -> Dict:
        return {"max_load_handled": 150, "breaking_point_rps": 200, "status": "good"}
    
    def _monitor_resource_usage(self) -> Dict:
        return {"avg_cpu_percent": 45, "avg_memory_mb": 512, "status": "good"}
    
    def _calculate_performance_score(self, benchmarks: Dict) -> float:
        return 78.5  # Mock performance score
    
    def _grade_performance(self, score: float) -> str:
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    # Mock monitoring functions
    def _check_system_uptime(self) -> Dict:
        return {"status": "healthy", "uptime_hours": 72, "message": "System running normally"}
    
    def _check_service_connectivity(self) -> Dict:
        return {"status": "healthy", "services_online": 7, "services_total": 8, "message": "Most services online"}
    
    def _check_quick_response_times(self) -> Dict:
        return {"status": "healthy", "avg_response_ms": 230, "message": "Response times normal"}
    
    def _check_error_rates(self) -> Dict:
        return {"status": "healthy", "error_rate_percent": 0.5, "message": "Error rates low"}
    
    def _log_monitoring_result(self, result: Dict):
        """Monitoring sonucunu log'a kaydet"""
        log_file = self.logs_dir / "monitoring.log"
        log_entry = f"[{result['timestamp']}] MONITORING: {json.dumps(result['quick_checks'])}\n"
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

def main():
    """Ana test otomasyon sistemi"""
    print("🤖 AURA AI TEST OTOMASYON SİSTEMİ")
    print("=" * 60)
    
    # Test otomasyon nesnesini oluştur
    automation = AuraTestAutomation()
    
    # Komut satırı argümanlarını kontrol et
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "schedule":
            # Zamanlanmış testleri başlat
            automation.start_scheduled_testing()
            automation.run_scheduled_tests_loop()
            
        elif command == "full":
            # Tam test paketini çalıştır
            results = automation.run_full_test_suite()
            return 0 if results['overall_status'] in ['passed', 'warning'] else 1
            
        elif command == "health":
            # Sağlık kontrolü çalıştır
            results = automation.run_health_check_suite()
            return 0 if results['overall_health'] in ['excellent', 'good'] else 1
            
        elif command == "performance":
            # Performans testleri çalıştır
            results = automation.run_performance_test_suite()
            return 0 if results['overall_score'] >= 70 else 1
            
        elif command == "monitor":
            # Monitoring kontrolü çalıştır
            results = automation.run_monitoring_check()
            return 0
            
        else:
            print(f"❌ Bilinmeyen komut: {command}")
            print("💡 Kullanılabilir komutlar: schedule, full, health, performance, monitor")
            return 1
    else:
        # Argüman verilmemişse interactive mode
        print("🎮 İNTERAKTİF MOD")
        print("-" * 40)
        print("1. Zamanlanmış testleri başlat (schedule)")
        print("2. Tam test paketi çalıştır (full)")
        print("3. Sağlık kontrolü (health)")
        print("4. Performans testleri (performance)")
        print("5. Monitoring kontrolü (monitor)")
        print("-" * 40)
        
        choice = input("Seçiminizi yapın (1-5): ").strip()
        
        if choice == "1":
            automation.start_scheduled_testing()
            automation.run_scheduled_tests_loop()
        elif choice == "2":
            results = automation.run_full_test_suite()
            return 0 if results['overall_status'] in ['passed', 'warning'] else 1
        elif choice == "3":
            results = automation.run_health_check_suite()
            return 0 if results['overall_health'] in ['excellent', 'good'] else 1
        elif choice == "4":
            results = automation.run_performance_test_suite()
            return 0 if results['overall_score'] >= 70 else 1
        elif choice == "5":
            results = automation.run_monitoring_check()
            return 0
        else:
            print("❌ Geçersiz seçim")
            return 1
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⏹️ Test otomasyonu kullanıcı tarafından durduruldu")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Test otomasyonunda beklenmeyen hata: {str(e)}")
        sys.exit(1)
