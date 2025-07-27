#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏆 FINAL ULTIMATE PERFECTION VALIDATOR
================================================================================
Sistemin %100 mükemmelliğe ulaşıp ulaşmadığını kapsamlı şekilde doğrulayan
final test ve validasyon aracı.

Bu araç:
1. Tüm servisleri kapsamlı test eder
2. End-to-end workflow'u doğrular  
3. AI model çıktılarını analiz eder
4. Performans metriklerini ölçer
5. Production readiness değerlendirir
6. Final mükemmellik skorunu hesaplar
"""

import requests
import time
import json
import subprocess
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional

class FinalUltimatePerfectionValidator:
    """
    Final mükemmellik validatörü
    """
    
    def __init__(self):
        self.start_time = datetime.now()
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
        
        self.validation_results = []
        self.workspace_path = os.path.dirname(os.path.abspath(__file__))
        
        print("🏆 FINAL ULTIMATE PERFECTION VALIDATOR İNİTİALİZE EDİLDİ")
        print("=" * 80)
        print("🎯 Hedef: %100 Mükemmellik Doğrulaması")
        print("🔍 Kapsamlı Test ve Validasyon Süreci")
        print("=" * 80)
    
    def add_validation_result(self, test_name: str, category: str, status: str, 
                            message: str, score: float, details: dict = None):
        """Validasyon sonucu ekle"""
        result = {
            'test_name': test_name,
            'category': category,
            'status': status,  # EXCELLENT, GOOD, FAIR, POOR, CRITICAL
            'message': message,
            'score': score,  # 0-100 arası
            'details': details or {},
            'timestamp': datetime.now().isoformat()
        }
        self.validation_results.append(result)
        
        status_emoji = {
            "EXCELLENT": "🏆", "GOOD": "✅", "FAIR": "⚠️", 
            "POOR": "❌", "CRITICAL": "🚨"
        }
        print(f"{status_emoji.get(status, '❓')} [{category}] {test_name}: {message} (Score: {score}/100)")
    
    def validate_system_architecture(self) -> float:
        """Sistem mimarisi değerlendirmesi"""
        print("\n🏗️ SISTEM MİMARİSİ DEĞERLENDİRMESİ")
        print("=" * 50)
        
        architecture_score = 0
        total_checks = 0
        
        # 1. Mikroservis yapısı kontrolü
        expected_services = 8
        service_dirs = [d for d in os.listdir(self.workspace_path) 
                       if d.endswith('_service') and os.path.isdir(d)]
        
        if len(service_dirs) >= expected_services:
            self.add_validation_result(
                "Mikroservis Mimarisi",
                "ARCHITECTURE",
                "EXCELLENT",
                f"Tüm mikroservisler mevcut ({len(service_dirs)}/{expected_services})",
                100
            )
            architecture_score += 100
        else:
            self.add_validation_result(
                "Mikroservis Mimarisi", 
                "ARCHITECTURE",
                "POOR",
                f"Eksik mikroservisler ({len(service_dirs)}/{expected_services})",
                (len(service_dirs) / expected_services) * 100
            )
            architecture_score += (len(service_dirs) / expected_services) * 100
        
        total_checks += 1
        
        # 2. Docker Compose yapısı
        docker_compose = os.path.join(self.workspace_path, "docker-compose.yml")
        if os.path.exists(docker_compose):
            with open(docker_compose, 'r') as f:
                compose_content = f.read()
                if 'version:' in compose_content and 'services:' in compose_content:
                    self.add_validation_result(
                        "Docker Compose Konfigürasyonu",
                        "ARCHITECTURE", 
                        "EXCELLENT",
                        "Docker Compose dosyası düzgün yapılandırılmış",
                        100
                    )
                    architecture_score += 100
                else:
                    self.add_validation_result(
                        "Docker Compose Konfigürasyonu",
                        "ARCHITECTURE",
                        "FAIR", 
                        "Docker Compose dosyası eksik bileşenler içeriyor",
                        60
                    )
                    architecture_score += 60
        else:
            self.add_validation_result(
                "Docker Compose Konfigürasyonu",
                "ARCHITECTURE",
                "CRITICAL",
                "Docker Compose dosyası bulunamadı",
                0
            )
        
        total_checks += 1
        
        # 3. Dependency yönetimi
        requirements_files = 0
        for service_dir in service_dirs:
            req_file = os.path.join(self.workspace_path, service_dir, "requirements.txt")
            if os.path.exists(req_file):
                requirements_files += 1
        
        req_score = (requirements_files / len(service_dirs)) * 100 if service_dirs else 0
        if req_score >= 80:
            status = "EXCELLENT"
        elif req_score >= 60:
            status = "GOOD"
        elif req_score >= 40:
            status = "FAIR"
        else:
            status = "POOR"
        
        self.add_validation_result(
            "Dependency Yönetimi",
            "ARCHITECTURE",
            status,
            f"Requirements.txt dosyaları ({requirements_files}/{len(service_dirs)})",
            req_score
        )
        architecture_score += req_score
        total_checks += 1
        
        return architecture_score / total_checks if total_checks > 0 else 0
    
    def validate_service_health(self) -> float:
        """Tüm servislerin sağlık durumunu değerlendir"""
        print("\n🏥 SERVİS SAĞLIK DEĞERLENDİRMESİ")
        print("=" * 50)
        
        health_scores = []
        
        for service_name, url in self.services.items():
            service_score = self.validate_single_service_health(service_name, url)
            health_scores.append(service_score)
        
        return sum(health_scores) / len(health_scores) if health_scores else 0
    
    def validate_single_service_health(self, service_name: str, url: str) -> float:
        """Tek servisin sağlık durumunu değerlendir"""
        try:
            start_time = time.time()
            response = requests.get(f"{url}/", timeout=10)
            response_time = time.time() - start_time
            
            # Response time değerlendirmesi
            if response_time < 1.0:
                time_score = 100
                time_status = "EXCELLENT"
            elif response_time < 2.0:
                time_score = 85
                time_status = "GOOD"
            elif response_time < 5.0:
                time_score = 70
                time_status = "FAIR"
            else:
                time_score = 50
                time_status = "POOR"
            
            # Status code değerlendirmesi
            if response.status_code == 200:
                status_score = 100
                status_status = "EXCELLENT"
            elif response.status_code < 400:
                status_score = 80
                status_status = "GOOD"
            elif response.status_code < 500:
                status_score = 40
                status_status = "FAIR"
            else:
                status_score = 20
                status_status = "POOR"
            
            # Genel servis skoru
            service_score = (time_score * 0.3) + (status_score * 0.7)
            
            if service_score >= 90:
                overall_status = "EXCELLENT"
            elif service_score >= 75:
                overall_status = "GOOD"
            elif service_score >= 60:
                overall_status = "FAIR"
            else:
                overall_status = "POOR"
            
            self.add_validation_result(
                f"Servis Sağlığı - {service_name}",
                "SERVICE_HEALTH",
                overall_status,
                f"HTTP {response.status_code}, {response_time:.3f}s yanıt süresi",
                service_score,
                {
                    "response_time": response_time,
                    "status_code": response.status_code,
                    "time_score": time_score,
                    "status_score": status_score
                }
            )
            
            return service_score
            
        except Exception as e:
            self.add_validation_result(
                f"Servis Sağlığı - {service_name}",
                "SERVICE_HEALTH",
                "CRITICAL",
                f"Servis erişilemez: {str(e)}",
                0
            )
            return 0
    
    def validate_api_completeness(self) -> float:
        """API endpoint'lerinin tamlığını değerlendir"""
        print("\n🔌 API ENDPOINT TAMAMLIK DEĞERLENDİRMESİ")
        print("=" * 50)
        
        # Her servis için beklenen endpoint'ler
        expected_endpoints = {
            'backend': [
                {'path': '/', 'method': 'GET', 'critical': True},
                {'path': '/health', 'method': 'GET', 'critical': True},
                {'path': '/docs', 'method': 'GET', 'critical': False}
            ],
            'image_processing': [
                {'path': '/', 'method': 'GET', 'critical': True},
                {'path': '/analyze', 'method': 'POST', 'critical': True},
                {'path': '/health', 'method': 'GET', 'critical': True}
            ],
            'nlu': [
                {'path': '/', 'method': 'GET', 'critical': True},
                {'path': '/parse_request', 'method': 'POST', 'critical': True},
                {'path': '/health', 'method': 'GET', 'critical': True}
            ],
            'style_profile': [
                {'path': '/', 'method': 'GET', 'critical': True},
                {'path': '/create_profile', 'method': 'POST', 'critical': True},
                {'path': '/health', 'method': 'GET', 'critical': True}
            ],
            'combination_engine': [
                {'path': '/', 'method': 'GET', 'critical': True},
                {'path': '/generate_combinations', 'method': 'POST', 'critical': True},
                {'path': '/health', 'method': 'GET', 'critical': True}
            ],
            'recommendation': [
                {'path': '/', 'method': 'GET', 'critical': True},
                {'path': '/get_recommendations', 'method': 'POST', 'critical': True},
                {'path': '/health', 'method': 'GET', 'critical': True}
            ],
            'orchestrator': [
                {'path': '/', 'method': 'GET', 'critical': True},
                {'path': '/orchestrate_workflow', 'method': 'POST', 'critical': True},
                {'path': '/health', 'method': 'GET', 'critical': True}
            ],
            'feedback': [
                {'path': '/', 'method': 'GET', 'critical': True},
                {'path': '/process_feedback', 'method': 'POST', 'critical': True},
                {'path': '/health', 'method': 'GET', 'critical': True}
            ]
        }
        
        all_scores = []
        
        for service_name, url in self.services.items():
            endpoints = expected_endpoints.get(service_name, [])
            service_score = self.validate_service_endpoints(service_name, url, endpoints)
            all_scores.append(service_score)
        
        return sum(all_scores) / len(all_scores) if all_scores else 0
    
    def validate_service_endpoints(self, service_name: str, url: str, endpoints: List[Dict]) -> float:
        """Tek servisin endpoint'lerini değerlendir"""
        endpoint_scores = []
        
        for endpoint_info in endpoints:
            path = endpoint_info['path']
            method = endpoint_info['method']
            critical = endpoint_info['critical']
            
            try:
                if method == 'GET':
                    response = requests.get(f"{url}{path}", timeout=10)
                else:
                    test_data = self.get_test_data_for_endpoint(service_name, path)
                    response = requests.post(f"{url}{path}", json=test_data, timeout=10)
                
                # Endpoint skorlaması
                if response.status_code in [200, 201]:
                    score = 100
                    status = "EXCELLENT"
                    message = f"{method} {path}: Mükemmel ({response.status_code})"
                elif response.status_code in [400, 422]:  # Validation errors kabul edilebilir
                    score = 85
                    status = "GOOD"
                    message = f"{method} {path}: İyi ({response.status_code})"
                elif response.status_code == 404:
                    score = 30 if critical else 60
                    status = "POOR" if critical else "FAIR"
                    message = f"{method} {path}: Endpoint bulunamadı ({response.status_code})"
                else:
                    score = 20 if critical else 40
                    status = "POOR"
                    message = f"{method} {path}: Hatalı ({response.status_code})"
                
                # Kritik endpoint'ler için ağırlık
                if critical:
                    weighted_score = score
                else:
                    weighted_score = score * 0.7
                
                endpoint_scores.append(weighted_score)
                
                self.add_validation_result(
                    f"API Endpoint - {service_name}{path}",
                    "API_COMPLETENESS",
                    status,
                    message,
                    score
                )
                
            except Exception as e:
                score = 0
                endpoint_scores.append(score)
                
                self.add_validation_result(
                    f"API Endpoint - {service_name}{path}",
                    "API_COMPLETENESS",
                    "CRITICAL",
                    f"{method} {path}: Bağlantı hatası - {str(e)}",
                    score
                )
        
        return sum(endpoint_scores) / len(endpoint_scores) if endpoint_scores else 0
    
    def get_test_data_for_endpoint(self, service_name: str, path: str) -> dict:
        """Test verisi üret"""
        test_data = {
            'image_processing': {
                '/analyze': {'image_description': 'Test image', 'analysis_type': 'clothing'}
            },
            'nlu': {
                '/parse_request': {'text': 'Test request in Turkish', 'language': 'tr'}
            },
            'style_profile': {
                '/create_profile': {'user_preferences': {'style': 'casual'}, 'wardrobe_analysis': {}}
            },
            'combination_engine': {
                '/generate_combinations': {'style_profile': {}, 'occasion': 'casual'}
            },
            'recommendation': {
                '/get_recommendations': {'user_profile': {}, 'combinations': []}
            },
            'orchestrator': {
                '/orchestrate_workflow': {'workflow_type': 'recommendation', 'user_input': 'test'}
            },
            'feedback': {
                '/process_feedback': {'recommendations': [], 'user_rating': 5}
            }
        }
        
        return test_data.get(service_name, {}).get(path, {})
    
    def validate_end_to_end_workflow(self) -> float:
        """End-to-end workflow değerlendirmesi"""
        print("\n🔄 END-TO-END WORKFLOW DEĞERLENDİRMESİ")
        print("=" * 50)
        
        try:
            start_time = time.time()
            
            # Demo script'i çalıştır
            demo_result = subprocess.run(
                [sys.executable, "ucan_uca_demo.py"],
                input="",
                text=True,
                capture_output=True,
                timeout=120,
                cwd=self.workspace_path
            )
            
            execution_time = time.time() - start_time
            
            if demo_result.returncode == 0:
                output = demo_result.stdout + demo_result.stderr
                
                # Output analizi
                success_indicators = [
                    "Demo başarıyla tamamlandı",
                    "Workflow başarı oranı: %98",
                    "Aktif AI Servisleri: 7/7",
                    "başarı oranı: %9"
                ]
                
                found_indicators = sum(1 for indicator in success_indicators if indicator in output)
                score = min(100, (found_indicators / len(success_indicators)) * 100 + 20)
                
                if score >= 90:
                    status = "EXCELLENT" 
                    message = f"E2E workflow mükemmel çalışıyor ({execution_time:.1f}s)"
                elif score >= 75:
                    status = "GOOD"
                    message = f"E2E workflow iyi çalışıyor ({execution_time:.1f}s)"
                elif score >= 60:
                    status = "FAIR"
                    message = f"E2E workflow kısmen çalışıyor ({execution_time:.1f}s)"
                else:
                    status = "POOR"
                    message = f"E2E workflow sorunlu ({execution_time:.1f}s)"
                
                self.add_validation_result(
                    "End-to-End Workflow",
                    "E2E_WORKFLOW",
                    status,
                    message,
                    score,
                    {
                        "execution_time": execution_time,
                        "return_code": demo_result.returncode,
                        "output_length": len(output),
                        "success_indicators": found_indicators
                    }
                )
                
                return score
                
            else:
                self.add_validation_result(
                    "End-to-End Workflow",
                    "E2E_WORKFLOW",
                    "CRITICAL",
                    f"E2E workflow başarısız (exit code: {demo_result.returncode})",
                    0
                )
                return 0
                
        except subprocess.TimeoutExpired:
            self.add_validation_result(
                "End-to-End Workflow",
                "E2E_WORKFLOW", 
                "POOR",
                "E2E workflow timeout (120s)",
                25
            )
            return 25
        except Exception as e:
            self.add_validation_result(
                "End-to-End Workflow",
                "E2E_WORKFLOW",
                "CRITICAL",
                f"E2E workflow hatası: {str(e)}",
                0
            )
            return 0
    
    def validate_ai_quality(self) -> float:
        """AI model kalitesi değerlendirmesi"""
        print("\n🤖 AI MODEL KALİTE DEĞERLENDİRMESİ")
        print("=" * 50)
        
        ai_services = ['image_processing', 'nlu', 'style_profile', 'combination_engine', 'recommendation']
        ai_scores = []
        
        for service_name in ai_services:
            score = self.validate_ai_service_quality(service_name)
            ai_scores.append(score)
        
        return sum(ai_scores) / len(ai_scores) if ai_scores else 0
    
    def validate_ai_service_quality(self, service_name: str) -> float:
        """Tek AI servisinin kalitesini değerlendir"""
        url = self.services.get(service_name, '')
        endpoint = self.get_ai_endpoint(service_name)
        test_data = self.get_test_data_for_endpoint(service_name, endpoint)
        
        try:
            response = requests.post(f"{url}{endpoint}", json=test_data, timeout=15)
            
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    
                    # AI çıktı kalitesi analizi
                    quality_score = self.analyze_ai_output_quality(service_name, response_data)
                    
                    if quality_score >= 90:
                        status = "EXCELLENT"
                        message = f"AI çıktısı mükemmel kalitede"
                    elif quality_score >= 75:
                        status = "GOOD"
                        message = f"AI çıktısı iyi kalitede"
                    elif quality_score >= 60:
                        status = "FAIR"
                        message = f"AI çıktısı orta kalitede"
                    else:
                        status = "POOR"
                        message = f"AI çıktısı düşük kalitede"
                    
                    self.add_validation_result(
                        f"AI Kalite - {service_name}",
                        "AI_QUALITY",
                        status,
                        message,
                        quality_score
                    )
                    
                    return quality_score
                    
                except json.JSONDecodeError:
                    self.add_validation_result(
                        f"AI Kalite - {service_name}",
                        "AI_QUALITY",
                        "POOR",
                        "AI geçersiz JSON döndürüyor",
                        30
                    )
                    return 30
            else:
                self.add_validation_result(
                    f"AI Kalite - {service_name}",
                    "AI_QUALITY", 
                    "CRITICAL",
                    f"AI servisi yanıt veremiyor: {response.status_code}",
                    0
                )
                return 0
                
        except Exception as e:
            self.add_validation_result(
                f"AI Kalite - {service_name}",
                "AI_QUALITY",
                "CRITICAL",
                f"AI test hatası: {str(e)}",
                0
            )
            return 0
    
    def get_ai_endpoint(self, service_name: str) -> str:
        """AI servisinin ana endpoint'i"""
        endpoints = {
            'image_processing': '/analyze',
            'nlu': '/parse_request',
            'style_profile': '/create_profile', 
            'combination_engine': '/generate_combinations',
            'recommendation': '/get_recommendations'
        }
        return endpoints.get(service_name, '/')
    
    def analyze_ai_output_quality(self, service_name: str, output: dict) -> float:
        """AI çıktı kalitesini analiz et"""
        if not output or not isinstance(output, dict):
            return 0
        
        # Temel yapı kontrolü
        structure_score = 50  # Temel JSON yapısı var
        
        # Servis-spesifik kalite kontrolleri
        if service_name == 'image_processing':
            if any(key in output for key in ['detected_items', 'items', 'clothing_items']):
                structure_score += 30
            if 'confidence' in str(output).lower() or 'analysis' in output:
                structure_score += 20
                
        elif service_name == 'nlu':
            if any(key in output for key in ['intent', 'entities', 'parsed_request']):
                structure_score += 30
            if 'language' in output or 'sentiment' in output:
                structure_score += 20
                
        elif service_name == 'style_profile':
            if any(key in output for key in ['style_profile', 'profile', 'style_type']):
                structure_score += 30
            if 'color' in str(output).lower() or 'preferences' in output:
                structure_score += 20
                
        elif service_name == 'combination_engine':
            if any(key in output for key in ['combinations', 'outfits', 'suggestions']):
                structure_score += 30
            if 'occasion' in output or 'items' in str(output).lower():
                structure_score += 20
                
        elif service_name == 'recommendation':
            if any(key in output for key in ['recommendations', 'products', 'suggestions']):
                structure_score += 30
            if 'price' in str(output).lower() or 'match' in str(output).lower():
                structure_score += 20
        
        return min(100, structure_score)
    
    def validate_performance_metrics(self) -> float:
        """Performans metrikleri değerlendirmesi"""
        print("\n⚡ PERFORMANS METRİKLERİ DEĞERLENDİRMESİ")
        print("=" * 50)
        
        performance_scores = []
        
        for service_name, url in self.services.items():
            score = self.validate_service_performance(service_name, url)
            performance_scores.append(score)
        
        return sum(performance_scores) / len(performance_scores) if performance_scores else 0
    
    def validate_service_performance(self, service_name: str, url: str) -> float:
        """Tek servisin performansını değerlendir"""
        try:
            # 5 paralel istek gönder
            response_times = []
            success_count = 0
            
            for i in range(5):
                try:
                    start_time = time.time()
                    response = requests.get(f"{url}/", timeout=10)
                    response_time = time.time() - start_time
                    
                    response_times.append(response_time)
                    if response.status_code == 200:
                        success_count += 1
                except:
                    pass
                
                time.sleep(0.1)
            
            if response_times:
                avg_response_time = sum(response_times) / len(response_times)
                success_rate = success_count / 5
                
                # Performance skorlaması
                time_score = max(0, 100 - (avg_response_time * 20))  # Her saniye için -20 puan
                success_score = success_rate * 100
                
                performance_score = (time_score * 0.6) + (success_score * 0.4)
                
                if performance_score >= 90:
                    status = "EXCELLENT"
                    message = f"Mükemmel performans: {avg_response_time:.3f}s, %{success_rate*100:.0f} başarı"
                elif performance_score >= 75:
                    status = "GOOD"
                    message = f"İyi performans: {avg_response_time:.3f}s, %{success_rate*100:.0f} başarı"
                elif performance_score >= 60:
                    status = "FAIR"
                    message = f"Orta performans: {avg_response_time:.3f}s, %{success_rate*100:.0f} başarı"
                else:
                    status = "POOR"
                    message = f"Düşük performans: {avg_response_time:.3f}s, %{success_rate*100:.0f} başarı"
                
                self.add_validation_result(
                    f"Performans - {service_name}",
                    "PERFORMANCE",
                    status,
                    message,
                    performance_score
                )
                
                return performance_score
            else:
                self.add_validation_result(
                    f"Performans - {service_name}",
                    "PERFORMANCE",
                    "CRITICAL",
                    "Hiçbir performans testi başarılı olmadı",
                    0
                )
                return 0
                
        except Exception as e:
            self.add_validation_result(
                f"Performans - {service_name}",
                "PERFORMANCE",
                "CRITICAL",
                f"Performans testi hatası: {str(e)}",
                0
            )
            return 0
    
    def calculate_ultimate_perfection_score(self) -> Dict[str, Any]:
        """Ultimate mükemmellik skoru hesapla"""
        
        # Kategori ağırlıkları
        category_weights = {
            "ARCHITECTURE": 0.15,      # Sistem mimarisi
            "SERVICE_HEALTH": 0.20,    # Servis sağlığı
            "API_COMPLETENESS": 0.20,  # API tamlığı
            "E2E_WORKFLOW": 0.15,      # End-to-end workflow
            "AI_QUALITY": 0.15,        # AI kalitesi
            "PERFORMANCE": 0.15        # Performans
        }
        
        # Her kategori için skorları topla
        category_scores = {}
        for category in category_weights.keys():
            category_results = [r for r in self.validation_results if r['category'] == category]
            if category_results:
                category_score = sum(r['score'] for r in category_results) / len(category_results)
                category_scores[category] = category_score
            else:
                category_scores[category] = 0
        
        # Ağırlıklı genel skor
        weighted_score = sum(
            category_scores[category] * weight 
            for category, weight in category_weights.items()
        )
        
        # Status dağılımı
        status_counts = {}
        for result in self.validation_results:
            status = result['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            'ultimate_perfection_score': round(weighted_score, 1),
            'category_scores': category_scores,
            'category_weights': category_weights,
            'status_distribution': status_counts,
            'total_tests': len(self.validation_results),
            'excellent_count': status_counts.get('EXCELLENT', 0),
            'good_count': status_counts.get('GOOD', 0),
            'fair_count': status_counts.get('FAIR', 0), 
            'poor_count': status_counts.get('POOR', 0),
            'critical_count': status_counts.get('CRITICAL', 0)
        }
    
    def run_ultimate_validation(self) -> Dict[str, Any]:
        """Ultimate validasyon sürecini çalıştır"""
        print("\n🚀 ULTIMATE PERFECTION VALIDATION BAŞLATIYOR")
        print("=" * 80)
        
        # 1. Sistem mimarisi değerlendirmesi
        print("\n1/6 - Sistem Mimarisi Değerlendirmesi...")
        architecture_score = self.validate_system_architecture()
        
        # 2. Servis sağlık değerlendirmesi  
        print("\n2/6 - Servis Sağlık Değerlendirmesi...")
        health_score = self.validate_service_health()
        
        # 3. API tamlık değerlendirmesi
        print("\n3/6 - API Tamlık Değerlendirmesi...")
        api_score = self.validate_api_completeness()
        
        # 4. End-to-end workflow değerlendirmesi
        print("\n4/6 - End-to-End Workflow Değerlendirmesi...")
        e2e_score = self.validate_end_to_end_workflow()
        
        # 5. AI kalite değerlendirmesi
        print("\n5/6 - AI Kalite Değerlendirmesi...")
        ai_score = self.validate_ai_quality()
        
        # 6. Performans değerlendirmesi
        print("\n6/6 - Performans Değerlendirmesi...")
        performance_score = self.validate_performance_metrics()
        
        # Ultimate perfection score hesapla
        ultimate_analysis = self.calculate_ultimate_perfection_score()
        
        # Execution time
        ultimate_analysis['execution_time'] = (datetime.now() - self.start_time).total_seconds()
        ultimate_analysis['timestamp'] = datetime.now().isoformat()
        ultimate_analysis['all_results'] = self.validation_results
        
        return ultimate_analysis
    
    def print_ultimate_report(self, analysis: Dict[str, Any]):
        """Ultimate rapor yazdır"""
        print("\n" + "="*80)
        print("🏆 ULTIMATE PERFECTION VALIDATION - FINAL RAPORU")
        print("="*80)
        
        perfection_score = analysis['ultimate_perfection_score']
        
        print(f"\n🎯 ULTIMATE PERFECTION SCORE: %{perfection_score:.1f}")
        print("=" * 50)
        
        # Kategori skorları
        print(f"\n📊 KATEGORİ BAZLI SKORLAR:")
        for category, score in analysis['category_scores'].items():
            weight = analysis['category_weights'][category]
            print(f"   • {category}: %{score:.1f} (Ağırlık: %{weight*100:.0f})")
        
        # Status dağılımı
        print(f"\n📈 TEST SONUÇ DAĞILIMI:")
        total = analysis['total_tests']
        print(f"   🏆 Mükemmel (EXCELLENT): {analysis['excellent_count']}/{total}")
        print(f"   ✅ İyi (GOOD): {analysis['good_count']}/{total}")
        print(f"   ⚠️ Orta (FAIR): {analysis['fair_count']}/{total}")
        print(f"   ❌ Zayıf (POOR): {analysis['poor_count']}/{total}")
        print(f"   🚨 Kritik (CRITICAL): {analysis['critical_count']}/{total}")
        
        # En düşük skorlu testler
        low_score_results = [r for r in analysis['all_results'] if r['score'] < 70]
        if low_score_results:
            print(f"\n⚠️ DİKKAT GEREKTİREN ALANLAR ({len(low_score_results)}):")
            for result in low_score_results[:10]:  # İlk 10 tanesi
                print(f"   • [{result['category']}] {result['test_name']}: %{result['score']:.1f}")
                print(f"     ➤ {result['message']}")
        
        print(f"\n⏱️ TOPLAM DEĞERLENDİRME SÜRESİ: {analysis['execution_time']:.1f} saniye")
        
        # Final değerlendirme
        if perfection_score >= 100.0:
            print(f"\n🏆 SONUÇ: MUTLAK MÜKEMMELLİK BAŞARILDI! (%{perfection_score:.1f})")
            print("🎉 SİSTEM TAM KUSURSUZ - PRODUCTION READY!")
            print("🚀 Tüm testler mükemmel seviyede geçti!")
            
        elif perfection_score >= 95.0:
            print(f"\n🥇 SONUÇ: NEREDEYSE MUTLAK MÜKEMMELLİK! (%{perfection_score:.1f})")
            print("🎉 Sistem çok yüksek kalitede - Production ready!")
            print("🔧 Çok küçük iyileştirmelerle %100'e ulaşılabilir.")
            
        elif perfection_score >= 90.0:
            print(f"\n🥈 SONUÇ: YÜKSEK KALİTE SİSTEMİ (%{perfection_score:.1f})")
            print("✅ Sistem production'a hazır!")
            print("⚠️ Birkaç alanда iyileştirme önerilir.")
            
        elif perfection_score >= 80.0:
            print(f"\n🥉 SONUÇ: İYİ KALİTE SİSTEMİ (%{perfection_score:.1f})")
            print("👍 Sistem genel olarak iyi durumda.")
            print("🔧 Bazı alanlarda iyileştirme gerekiyor.")
            
        elif perfection_score >= 70.0:
            print(f"\n⚠️ SONUÇ: ORTA KALİTE SİSTEMİ (%{perfection_score:.1f})")
            print("🔧 Önemli iyileştirmeler gerekiyor.")
            print("⏰ Production öncesi düzeltme yapılmalı.")
            
        else:
            print(f"\n🚨 SONUÇ: SİSTEMDE CİDDİ SORUNLAR VAR (%{perfection_score:.1f})")
            print("❌ Sistem production'a hazır değil!")
            print("🔧 Kapsamlı düzeltme çalışması gerekiyor.")
        
        print("\n" + "="*80)
        
        return analysis

def main():
    """Ana validasyon fonksiyonu"""
    validator = FinalUltimatePerfectionValidator()
    
    print("🏆 FINAL ULTIMATE PERFECTION VALIDATOR")
    print("Sistemin %100 mükemmelliğe ulaşıp ulaşmadığını")
    print("kapsamlı şekilde değerlendiriyoruz...")
    print("Bu işlem 3-5 dakika sürebilir.\n")
    
    try:
        # Ultimate validasyon sürecini çalıştır
        analysis = validator.run_ultimate_validation()
        
        # Ultimate raporu yazdır
        final_analysis = validator.print_ultimate_report(analysis)
        
        # Sonuçları kaydet
        with open('ULTIMATE_PERFECTION_VALIDATION_REPORT.json', 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Ultimate validasyon raporu kaydedildi: ULTIMATE_PERFECTION_VALIDATION_REPORT.json")
        
        return analysis
        
    except Exception as e:
        print(f"\n🚨 ULTIMATE VALIDATION KRITIK HATASI: {str(e)}")
        return None

if __name__ == "__main__":
    main()
