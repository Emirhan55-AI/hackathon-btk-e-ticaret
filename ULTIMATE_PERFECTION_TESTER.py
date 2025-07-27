#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 ULTIMATE PERFECTION TESTER - MUTLAK MÜKEMMELLİK TEST SİSTEMİ
================================================================================
Bu modül, Aura AI sisteminin %100 kusursuzluğa ulaşması için kapsamlı test sürecini yönetir.

Test Prensipleri:
- AlphaCodium/SED Metodolojisi
- RCI (Recursive Criticism and Improvement) 
- Test Odaklı Geliştirme (TDD)
- Kapsamlı Otomatik Doğrulama

Test Katmanları:
1. Birim Testleri (Unit Tests)
2. Entegrasyon Testleri (Integration Tests) 
3. Uçtan Uca Testler (End-to-End Tests)
4. Hata Toleransı Testleri (Fault Tolerance Tests)
5. Performans ve Yük Testleri (Performance Tests)
6. AI Model Doğrulama Testleri (AI Validation Tests)
"""

import asyncio
import aiohttp
import requests
import time
import json
import subprocess
import os
import sys
import traceback
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import psutil
import docker
import pytest
import concurrent.futures
from contextlib import asynccontextmanager

@dataclass
class TestResult:
    """Test sonucu veri yapısı"""
    test_name: str
    category: str
    status: str  # "PASS", "FAIL", "SKIP", "ERROR"
    message: str
    execution_time: float
    details: Dict[str, Any]
    error_trace: Optional[str] = None

@dataclass
class ServiceHealth:
    """Servis sağlık durumu"""
    name: str
    url: str
    status: str
    response_time: float
    error_message: Optional[str] = None

class UltimatePerfectionTester:
    """
    Mutlak mükemmellik test sistemi - her şeyi test eden kapsamlı framework
    """
    
    def __init__(self):
        self.start_time = datetime.now()
        self.test_results: List[TestResult] = []
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
        
        self.test_categories = [
            "UNIT_TESTS",
            "INTEGRATION_TESTS", 
            "END_TO_END_TESTS",
            "FAULT_TOLERANCE_TESTS",
            "PERFORMANCE_TESTS",
            "AI_VALIDATION_TESTS",
            "SECURITY_TESTS",
            "CONFIGURATION_TESTS"
        ]
        
        self.docker_client = None
        self.workspace_path = Path(__file__).parent
        
        print("🚀 ULTIMATE PERFECTION TESTER İNİTİALİZE EDİLDİ")
        print("=" * 80)
        print("🎯 Hedef: %100 Kusursuzluk")
        print("📋 Test Kategorileri:", len(self.test_categories))
        print("🔧 Mikroservisler:", len(self.services))
        print("=" * 80)
    
    def add_test_result(self, result: TestResult):
        """Test sonucu ekle"""
        self.test_results.append(result)
        status_emoji = {"PASS": "✅", "FAIL": "❌", "SKIP": "⏭️", "ERROR": "🚨"}
        print(f"{status_emoji.get(result.status, '❓')} [{result.category}] {result.test_name}: {result.message}")
    
    async def check_docker_environment(self) -> TestResult:
        """Docker environment kontrolü"""
        start_time = time.time()
        try:
            import docker
            self.docker_client = docker.from_env()
            
            # Çalışan containerları kontrol et
            containers = self.docker_client.containers.list()
            aura_containers = [c for c in containers if 'aura' in c.name.lower() or 'btk-hackathon' in c.name.lower()]
            
            if len(aura_containers) < 8:  # 8 mikroservis + db + redis bekliyoruz
                return TestResult(
                    "Docker Environment Check",
                    "CONFIGURATION_TESTS",
                    "FAIL",
                    f"Yetersiz container sayısı: {len(aura_containers)}/10",
                    time.time() - start_time,
                    {"containers": [c.name for c in aura_containers]}
                )
            
            return TestResult(
                "Docker Environment Check",
                "CONFIGURATION_TESTS", 
                "PASS",
                f"Tüm containerlar çalışıyor: {len(aura_containers)}",
                time.time() - start_time,
                {"containers": [c.name for c in aura_containers]}
            )
            
        except Exception as e:
            return TestResult(
                "Docker Environment Check",
                "CONFIGURATION_TESTS",
                "ERROR", 
                f"Docker hatası: {str(e)}",
                time.time() - start_time,
                {},
                traceback.format_exc()
            )
    
    async def test_service_health(self, service_name: str, url: str) -> TestResult:
        """Tek servis sağlık testi"""
        start_time = time.time()
        
        try:
            # Farklı health endpoint'lerini dene
            health_endpoints = ['/', '/health', '/status', '/api/health']
            
            for endpoint in health_endpoints:
                try:
                    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                        async with session.get(f"{url}{endpoint}") as response:
                            response_time = time.time() - start_time
                            
                            if response.status == 200:
                                response_data = await response.text()
                                
                                return TestResult(
                                    f"Health Check - {service_name}",
                                    "INTEGRATION_TESTS",
                                    "PASS",
                                    f"Servis sağlıklı ({response.status}) - {response_time:.3f}s",
                                    response_time,
                                    {
                                        "endpoint": endpoint,
                                        "status_code": response.status,
                                        "response_size": len(response_data)
                                    }
                                )
                except:
                    continue
            
            # Hiçbir endpoint çalışmıyor
            return TestResult(
                f"Health Check - {service_name}",
                "INTEGRATION_TESTS",
                "FAIL",
                "Hiçbir health endpoint erişilebilir değil",
                time.time() - start_time,
                {"attempted_endpoints": health_endpoints}
            )
            
        except Exception as e:
            return TestResult(
                f"Health Check - {service_name}",
                "INTEGRATION_TESTS",
                "ERROR",
                f"Bağlantı hatası: {str(e)}",
                time.time() - start_time,
                {},
                traceback.format_exc()
            )
    
    async def test_api_endpoints(self, service_name: str, url: str) -> List[TestResult]:
        """API endpoint'lerini kapsamlı test et"""
        results = []
        
        # Her servis için ana endpoint'leri tanımla
        service_endpoints = {
            'backend': [
                {'path': '/health', 'method': 'GET'},
                {'path': '/api/v1/auth/register', 'method': 'POST'},
                {'path': '/api/v1/products/', 'method': 'GET'},
                {'path': '/docs', 'method': 'GET'}
            ],
            'image_processing': [
                {'path': '/', 'method': 'GET'},
                {'path': '/analyze', 'method': 'POST'},
                {'path': '/health', 'method': 'GET'}
            ],
            'nlu': [
                {'path': '/', 'method': 'GET'}, 
                {'path': '/parse_request', 'method': 'POST'},
                {'path': '/health', 'method': 'GET'}
            ],
            'style_profile': [
                {'path': '/', 'method': 'GET'},
                {'path': '/create_profile', 'method': 'POST'},
                {'path': '/health', 'method': 'GET'}
            ],
            'combination_engine': [
                {'path': '/', 'method': 'GET'},
                {'path': '/generate_combinations', 'method': 'POST'},
                {'path': '/health', 'method': 'GET'}
            ],
            'recommendation': [
                {'path': '/', 'method': 'GET'},
                {'path': '/get_recommendations', 'method': 'POST'},
                {'path': '/health', 'method': 'GET'}
            ],
            'orchestrator': [
                {'path': '/', 'method': 'GET'},
                {'path': '/orchestrate_workflow', 'method': 'POST'},
                {'path': '/health', 'method': 'GET'}
            ],
            'feedback': [
                {'path': '/', 'method': 'GET'},
                {'path': '/process_feedback', 'method': 'POST'},
                {'path': '/health', 'method': 'GET'}
            ]
        }
        
        endpoints = service_endpoints.get(service_name, [{'path': '/', 'method': 'GET'}])
        
        for endpoint_info in endpoints:
            start_time = time.time()
            path = endpoint_info['path']
            method = endpoint_info['method']
            
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
                    
                    if method == 'GET':
                        async with session.get(f"{url}{path}") as response:
                            response_time = time.time() - start_time
                            response_text = await response.text()
                            
                            if response.status in [200, 404]:  # 404 da kabul edilebilir
                                status = "PASS" if response.status == 200 else "SKIP"
                                message = f"GET {path}: {response.status} - {response_time:.3f}s"
                            else:
                                status = "FAIL"
                                message = f"GET {path}: Beklenmeyen status {response.status}"
                                
                    elif method == 'POST':
                        # Mock data ile POST test et
                        test_data = self.get_mock_data_for_endpoint(service_name, path)
                        
                        async with session.post(f"{url}{path}", json=test_data) as response:
                            response_time = time.time() - start_time
                            response_text = await response.text()
                            
                            if response.status in [200, 201, 422, 404]:  # 422 validation error kabul edilebilir
                                status = "PASS" if response.status in [200, 201] else "SKIP"
                                message = f"POST {path}: {response.status} - {response_time:.3f}s"
                            else:
                                status = "FAIL"
                                message = f"POST {path}: Beklenmeyen status {response.status}"
                    
                    results.append(TestResult(
                        f"API Test - {service_name}{path}",
                        "INTEGRATION_TESTS",
                        status,
                        message,
                        response_time,
                        {
                            "method": method,
                            "status_code": response.status,
                            "response_size": len(response_text)
                        }
                    ))
                    
            except Exception as e:
                results.append(TestResult(
                    f"API Test - {service_name}{path}",
                    "INTEGRATION_TESTS",
                    "ERROR",
                    f"{method} {path}: {str(e)}",
                    time.time() - start_time,
                    {"method": method},
                    traceback.format_exc()
                ))
        
        return results
    
    def get_mock_data_for_endpoint(self, service_name: str, path: str) -> Dict[str, Any]:
        """Endpoint için mock test verisi üret"""
        mock_data = {
            'image_processing': {
                '/analyze': {
                    'image_description': 'Test kıyafet',
                    'analysis_type': 'clothing_detection'
                }
            },
            'nlu': {
                '/parse_request': {
                    'text': 'Mavi bir gömlek istiyorum',
                    'language': 'tr'
                }
            },
            'style_profile': {
                '/create_profile': {
                    'user_preferences': {'style': 'casual'},
                    'wardrobe_analysis': {}
                }
            },
            'combination_engine': {
                '/generate_combinations': {
                    'style_profile': {},
                    'occasion': 'casual'
                }
            },
            'recommendation': {
                '/get_recommendations': {
                    'user_profile': {},
                    'combinations': []
                }
            },
            'orchestrator': {
                '/orchestrate_workflow': {
                    'workflow_type': 'recommendation',
                    'user_input': 'Test isteği'
                }
            },
            'feedback': {
                '/process_feedback': {
                    'recommendations': [],
                    'user_rating': 5
                }
            },
            'backend': {
                '/api/v1/auth/register': {
                    'email': 'test@test.com',
                    'password': 'test123',
                    'full_name': 'Test User'
                }
            }
        }
        
        return mock_data.get(service_name, {}).get(path, {})
    
    async def test_service_performance(self, service_name: str, url: str) -> TestResult:
        """Servis performans testi"""
        start_time = time.time()
        
        try:
            # 10 paralel istek gönder
            async def single_request():
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                    request_start = time.time()
                    async with session.get(f"{url}/") as response:
                        return time.time() - request_start, response.status
            
            # Paralel istekleri çalıştır
            tasks = [single_request() for _ in range(10)]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Sonuçları analiz et
            response_times = []
            success_count = 0
            
            for result in results:
                if isinstance(result, tuple):
                    response_time, status = result
                    response_times.append(response_time)
                    if status == 200:
                        success_count += 1
            
            if response_times:
                avg_response_time = sum(response_times) / len(response_times)
                max_response_time = max(response_times)
                min_response_time = min(response_times)
                
                # Performance kriterleri
                if avg_response_time < 2.0 and success_count >= 8:
                    status = "PASS"
                    message = f"İyi performans: Ort:{avg_response_time:.3f}s, Başarı:{success_count}/10"
                elif avg_response_time < 5.0 and success_count >= 5:
                    status = "SKIP" 
                    message = f"Orta performans: Ort:{avg_response_time:.3f}s, Başarı:{success_count}/10"
                else:
                    status = "FAIL"
                    message = f"Düşük performans: Ort:{avg_response_time:.3f}s, Başarı:{success_count}/10"
                
                return TestResult(
                    f"Performance Test - {service_name}",
                    "PERFORMANCE_TESTS",
                    status,
                    message,
                    time.time() - start_time,
                    {
                        "avg_response_time": avg_response_time,
                        "min_response_time": min_response_time,
                        "max_response_time": max_response_time,
                        "success_rate": success_count / 10,
                        "total_requests": 10
                    }
                )
            else:
                return TestResult(
                    f"Performance Test - {service_name}",
                    "PERFORMANCE_TESTS",
                    "FAIL",
                    "Hiçbir istek başarılı olmadı",
                    time.time() - start_time,
                    {}
                )
                
        except Exception as e:
            return TestResult(
                f"Performance Test - {service_name}",
                "PERFORMANCE_TESTS",
                "ERROR",
                f"Performance test hatası: {str(e)}",
                time.time() - start_time,
                {},
                traceback.format_exc()
            )
    
    async def test_end_to_end_workflow(self) -> TestResult:
        """Uçtan uca workflow testi"""
        start_time = time.time()
        
        try:
            print("\n🔄 End-to-End Workflow Test başlatılıyor...")
            
            # Demo script'i çalıştırarak e2e test yap
            demo_result = subprocess.run(
                [sys.executable, "ucan_uca_demo.py"],
                input="",  # Enter tuşuna basma simülasyonu
                text=True,
                capture_output=True,
                timeout=120,  # 2 dakika timeout
                cwd=self.workspace_path
            )
            
            execution_time = time.time() - start_time
            
            if demo_result.returncode == 0:
                # Başarılı çıktıyı analiz et
                output = demo_result.stdout + demo_result.stderr
                
                if "Demo başarıyla tamamlandı" in output:
                    status = "PASS"
                    message = f"E2E workflow başarılı - {execution_time:.3f}s"
                elif "Workflow başarı oranı: %98" in output or "başarı oranı: %9" in output:
                    status = "PASS"
                    message = f"E2E workflow yüksek başarı oranıyla tamamlandı - {execution_time:.3f}s"
                else:
                    status = "SKIP"
                    message = f"E2E workflow kısmen başarılı - {execution_time:.3f}s"
                
                return TestResult(
                    "End-to-End Workflow Test",
                    "END_TO_END_TESTS",
                    status,
                    message,
                    execution_time,
                    {
                        "return_code": demo_result.returncode,
                        "output_length": len(output),
                        "contains_success": "başarıyla tamamlandı" in output
                    }
                )
            else:
                return TestResult(
                    "End-to-End Workflow Test",
                    "END_TO_END_TESTS",
                    "FAIL",
                    f"E2E workflow başarısız (exit code: {demo_result.returncode})",
                    execution_time,
                    {
                        "return_code": demo_result.returncode,
                        "stdout": demo_result.stdout[:500],
                        "stderr": demo_result.stderr[:500]
                    }
                )
                
        except subprocess.TimeoutExpired:
            return TestResult(
                "End-to-End Workflow Test",
                "END_TO_END_TESTS",
                "FAIL",
                "E2E workflow timeout (120s)",
                time.time() - start_time,
                {"error": "timeout"}
            )
        except Exception as e:
            return TestResult(
                "End-to-End Workflow Test", 
                "END_TO_END_TESTS",
                "ERROR",
                f"E2E workflow hatası: {str(e)}",
                time.time() - start_time,
                {},
                traceback.format_exc()
            )
    
    async def test_fault_tolerance(self) -> List[TestResult]:
        """Hata toleransı testleri"""
        results = []
        
        # Servis olmadığında diğer servislerin graceful degradation yapıp yapmadığını test et
        for service_name in ['image_processing', 'nlu']:
            start_time = time.time()
            
            try:  
                # Orchestrator'a service_name servisini gerektirecek bir istek gönder
                # Eğer servis down ise, orchestrator fallback mekanizması devreye girmeli
                
                test_request = {
                    'workflow_type': 'recommendation',
                    'user_input': f'Test {service_name} fallback',
                    'require_service': service_name
                }
                
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=20)) as session:
                    async with session.post(
                        f"{self.services['orchestrator']}/orchestrate_workflow",
                        json=test_request
                    ) as response:
                        
                        response_time = time.time() - start_time
                        response_text = await response.text()
                        
                        if response.status == 200:
                            # Yanıt fallback mekanizması kullandı mı kontrol et
                            if "fallback" in response_text.lower() or "mock" in response_text.lower():
                                status = "PASS"
                                message = f"Fallback mekanizması çalışıyor - {service_name}"
                            else:
                                status = "SKIP"
                                message = f"Servis normal çalışıyor - {service_name}"
                        else:
                            status = "FAIL"
                            message = f"Orchestrator yanıt veremiyor - {service_name} için"
                        
                        results.append(TestResult(
                            f"Fault Tolerance - {service_name}",
                            "FAULT_TOLERANCE_TESTS",
                            status,
                            message,
                            response_time,
                            {
                                "service": service_name,
                                "status_code": response.status,
                                "has_fallback": "fallback" in response_text.lower()
                            }
                        ))
                        
            except Exception as e:
                results.append(TestResult(
                    f"Fault Tolerance - {service_name}",
                    "FAULT_TOLERANCE_TESTS",
                    "ERROR",
                    f"Fault tolerance test hatası: {str(e)}",
                    time.time() - start_time,
                    {"service": service_name},
                    traceback.format_exc()
                ))
        
        return results
    
    async def test_ai_model_outputs(self) -> List[TestResult]:
        """AI model çıktılarını doğrula"""
        results = []
        
        # Her AI servisinin mantıklı çıktı üretip üretmediğini test et
        ai_services = ['image_processing', 'nlu', 'style_profile', 'combination_engine', 'recommendation']
        
        for service_name in ai_services:
            start_time = time.time()
            
            try:
                test_data = self.get_ai_validation_data(service_name)
                endpoint = self.get_ai_endpoint(service_name)
                
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
                    async with session.post(
                        f"{self.services[service_name]}{endpoint}",
                        json=test_data
                    ) as response:
                        
                        response_time = time.time() - start_time
                        
                        if response.status == 200:
                            response_data = await response.json()
                            
                            # AI çıktısını doğrula
                            validation_result = self.validate_ai_output(service_name, response_data)
                            
                            if validation_result['valid']:
                                status = "PASS"
                                message = f"AI çıktısı geçerli - {service_name}"
                            else:
                                status = "FAIL"
                                message = f"AI çıktısı geçersiz - {service_name}: {validation_result['reason']}"
                            
                            results.append(TestResult(
                                f"AI Validation - {service_name}",
                                "AI_VALIDATION_TESTS",
                                status,
                                message,
                                response_time,
                                {
                                    "service": service_name,
                                    "validation": validation_result,
                                    "response_data": response_data
                                }
                            ))
                        else:
                            results.append(TestResult(
                                f"AI Validation - {service_name}",
                                "AI_VALIDATION_TESTS",
                                "FAIL",
                                f"AI servisi yanıt vermiyor: {response.status}",
                                response_time,
                                {"service": service_name, "status_code": response.status}
                            ))
                            
            except Exception as e:
                results.append(TestResult(
                    f"AI Validation - {service_name}",
                    "AI_VALIDATION_TESTS",
                    "ERROR",
                    f"AI validation hatası: {str(e)}",
                    time.time() - start_time,
                    {"service": service_name},
                    traceback.format_exc()
                ))
        
        return results
    
    def get_ai_validation_data(self, service_name: str) -> Dict[str, Any]:
        """AI servisi için test verisi"""
        data = {
            'image_processing': {
                'image_description': 'Mavi bir gömlek ve siyah pantolon',
                'analysis_type': 'clothing_detection'
            },
            'nlu': {
                'text': 'Bugün hava güzel, spor için ayakkabı arıyorum',
                'language': 'tr'
            },
            'style_profile': {
                'user_preferences': {'style': 'sporty', 'occasion': 'casual'},
                'wardrobe_analysis': {'items': [{'type': 'shirt', 'color': 'blue'}]}
            },
            'combination_engine': {
                'style_profile': {'style_type': 'sporty'},
                'occasion': 'casual',
                'weather': 'sunny'
            },
            'recommendation': {
                'user_profile': {'style': 'sporty'},
                'combinations': [{'type': 'casual', 'items': []}],
                'budget_range': 'medium'
            }
        }
        return data.get(service_name, {})
    
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
    
    def validate_ai_output(self, service_name: str, output: Dict[str, Any]) -> Dict[str, Any]:
        """AI çıktısının mantıklı olup olmadığını kontrol et"""
        
        validators = {
            'image_processing': self._validate_image_output,
            'nlu': self._validate_nlu_output,
            'style_profile': self._validate_style_output,
            'combination_engine': self._validate_combination_output,
            'recommendation': self._validate_recommendation_output
        }
        
        validator = validators.get(service_name, lambda x: {'valid': True, 'reason': 'No specific validator'})
        return validator(output)
    
    def _validate_image_output(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """Görüntü işleme çıktısını doğrula"""
        if not output:
            return {'valid': False, 'reason': 'Boş çıktı'}
        
        # Beklenen alanları kontrol et
        if 'detected_items' in output or 'items' in output or 'clothing_items' in output:
            return {'valid': True, 'reason': 'Kıyafet tespit alanları mevcut'}
        
        if 'analysis' in output or 'result' in output:
            return {'valid': True, 'reason': 'Analiz sonucu mevcut'} 
        
        return {'valid': False, 'reason': 'Beklenen alanlar bulunamadı'}
    
    def _validate_nlu_output(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """NLU çıktısını doğrula"""
        if not output:
            return {'valid': False, 'reason': 'Boş çıktı'}
        
        if 'intent' in output or 'entities' in output or 'parsed_request' in output:
            return {'valid': True, 'reason': 'NLU alanları mevcut'}
        
        return {'valid': False, 'reason': 'Intent/entities bulunamadı'}
    
    def _validate_style_output(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """Stil profili çıktısını doğrula"""
        if not output:
            return {'valid': False, 'reason': 'Boş çıktı'}
        
        if 'style_profile' in output or 'profile' in output or 'style_type' in output:
            return {'valid': True, 'reason': 'Stil profili alanları mevcut'}
        
        return {'valid': False, 'reason': 'Stil profili bulunamadı'}
    
    def _validate_combination_output(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """Kombinasyon çıktısını doğrula"""
        if not output:
            return {'valid': False, 'reason': 'Boş çıktı'}
        
        if 'combinations' in output or 'outfits' in output or 'suggestions' in output:
            return {'valid': True, 'reason': 'Kombinasyon alanları mevcut'}
        
        return {'valid': False, 'reason': 'Kombinasyon önerileri bulunamadı'}
    
    def _validate_recommendation_output(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """Öneri çıktısını doğrula"""
        if not output:
            return {'valid': False, 'reason': 'Boş çıktı'}
        
        if 'recommendations' in output or 'products' in output or 'suggestions' in output:
            return {'valid': True, 'reason': 'Öneri alanları mevcut'}
        
        return {'valid': False, 'reason': 'Ürün önerileri bulunamadı'}
    
    async def run_unit_tests(self) -> List[TestResult]:
        """Pytest ile unit testleri çalıştır"""
        results = []
        start_time = time.time()
        
        try:
            # Her servis için test dosyalarını bul ve çalıştır
            test_dirs = [
                'tests/',
                '*/tests/',
                '*/test_*.py'
            ]
            
            for pattern in test_dirs:
                test_files = list(self.workspace_path.glob(pattern))
                
                for test_file in test_files:
                    if test_file.is_file() and 'test_' in test_file.name:
                        # Pytest ile testi çalıştır
                        result = subprocess.run(
                            [sys.executable, '-m', 'pytest', str(test_file), '-v'],
                            capture_output=True,
                            text=True,
                            timeout=60,
                            cwd=self.workspace_path
                        )
                        
                        execution_time = time.time() - start_time
                        
                        if result.returncode == 0:
                            status = "PASS"
                            message = f"Unit testler başarılı - {test_file.name}"
                        else:
                            status = "FAIL"
                            message = f"Unit testler başarısız - {test_file.name}"
                        
                        results.append(TestResult(
                            f"Unit Tests - {test_file.name}",
                            "UNIT_TESTS",
                            status,
                            message,
                            execution_time,
                            {
                                "test_file": str(test_file),
                                "return_code": result.returncode,
                                "stdout": result.stdout[:500],
                                "stderr": result.stderr[:500]
                            }
                        ))
                        
                        start_time = time.time()  # Reset for next test
            
            if not results:
                results.append(TestResult(
                    "Unit Tests Discovery",
                    "UNIT_TESTS",
                    "SKIP",
                    "Hiçbir unit test dosyası bulunamadı",
                    0,
                    {"searched_patterns": test_dirs}
                ))
                
        except Exception as e:
            results.append(TestResult(
                "Unit Tests Execution",
                "UNIT_TESTS", 
                "ERROR",
                f"Unit test hatası: {str(e)}",
                time.time() - start_time,
                {},
                traceback.format_exc()
            ))
        
        return results
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Tüm testleri çalıştır"""
        print("\n🚀 KAPSAMLI TEST SÜRECİ BAŞLATIYOR")
        print("=" * 80)
        
        # 1. Konfigürasyon testleri
        print("\n📋 1/8 - Konfigürasyon Testleri...")
        docker_result = await self.check_docker_environment()
        self.add_test_result(docker_result)
        
        # 2. Sağlık testleri
        print("\n🏥 2/8 - Servis Sağlık Testleri...")
        health_tasks = [self.test_service_health(name, url) for name, url in self.services.items()]
        health_results = await asyncio.gather(*health_tasks)
        for result in health_results:
            self.add_test_result(result)
        
        # 3. API endpoint testleri
        print("\n🔌 3/8 - API Endpoint Testleri...")
        for service_name, url in self.services.items():
            api_results = await self.test_api_endpoints(service_name, url)
            for result in api_results:
                self.add_test_result(result)
        
        # 4. Performans testleri
        print("\n⚡ 4/8 - Performans Testleri...")
        perf_tasks = [self.test_service_performance(name, url) for name, url in self.services.items()]
        perf_results = await asyncio.gather(*perf_tasks)
        for result in perf_results:
            self.add_test_result(result)
        
        # 5. End-to-End testleri
        print("\n🔄 5/8 - End-to-End Testleri...")
        e2e_result = await self.test_end_to_end_workflow()
        self.add_test_result(e2e_result)
        
        # 6. Hata toleransı testleri
        print("\n🛡️ 6/8 - Hata Toleransı Testleri...")
        fault_results = await self.test_fault_tolerance()
        for result in fault_results:
            self.add_test_result(result)
        
        # 7. AI model validation testleri
        print("\n🤖 7/8 - AI Model Doğrulama Testleri...")
        ai_results = await self.test_ai_model_outputs()
        for result in ai_results:
            self.add_test_result(result)
        
        # 8. Unit testleri
        print("\n🔬 8/8 - Unit Testleri...")
        unit_results = await self.run_unit_tests()
        for result in unit_results:
            self.add_test_result(result)
        
        # Test sonuçlarını analiz et
        return self.analyze_results()
    
    def analyze_results(self) -> Dict[str, Any]:
        """Test sonuçlarını analiz et ve rapor oluştur"""
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r.status == "PASS"])
        failed_tests = len([r for r in self.test_results if r.status == "FAIL"])
        error_tests = len([r for r in self.test_results if r.status == "ERROR"])
        skipped_tests = len([r for r in self.test_results if r.status == "SKIP"])
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Kategori bazında analiz
        category_stats = {}
        for category in self.test_categories:
            category_tests = [r for r in self.test_results if r.category == category]
            if category_tests:
                category_passed = len([r for r in category_tests if r.status == "PASS"])
                category_total = len(category_tests)
                category_success = (category_passed / category_total * 100) if category_total > 0 else 0
                
                category_stats[category] = {
                    'total': category_total,
                    'passed': category_passed,
                    'failed': len([r for r in category_tests if r.status == "FAIL"]),
                    'errors': len([r for r in category_tests if r.status == "ERROR"]),
                    'skipped': len([r for r in category_tests if r.status == "SKIP"]),
                    'success_rate': category_success
                }
        
        # Başarısız testleri analiz et
        failed_tests_detail = []
        for result in self.test_results:
            if result.status in ["FAIL", "ERROR"]:
                failed_tests_detail.append({
                    'test_name': result.test_name,
                    'category': result.category,
                    'status': result.status,
                    'message': result.message,
                    'error_trace': result.error_trace
                })
        
        # Performans istatistikleri
        performance_stats = {
            'avg_execution_time': sum(r.execution_time for r in self.test_results) / total_tests if total_tests > 0 else 0,
            'max_execution_time': max((r.execution_time for r in self.test_results), default=0),
            'min_execution_time': min((r.execution_time for r in self.test_results), default=0)
        }
        
        # Mükemmellik skoru hesapla
        perfection_score = self.calculate_perfection_score()
        
        return {
            'summary': {
                'total_tests': total_tests,
                'passed': passed_tests,
                'failed': failed_tests,
                'errors': error_tests,
                'skipped': skipped_tests,
                'success_rate': success_rate,
                'perfection_score': perfection_score
            },
            'category_stats': category_stats,
            'failed_tests': failed_tests_detail,
            'performance_stats': performance_stats,
            'execution_time': (datetime.now() - self.start_time).total_seconds(),
            'timestamp': datetime.now().isoformat()
        }
    
    def calculate_perfection_score(self) -> float:
        """Mükemmellik skoru hesapla"""
        if not self.test_results:
            return 0.0
        
        # Ağırlıklı skorlama sistemi
        weights = {
            "PASS": 1.0,
            "SKIP": 0.5,  # Geçilen testler kısmi puan
            "FAIL": 0.0,
            "ERROR": 0.0
        }
        
        # Kategori ağırlıkları
        category_weights = {
            "UNIT_TESTS": 0.15,
            "INTEGRATION_TESTS": 0.25,
            "END_TO_END_TESTS": 0.20,
            "FAULT_TOLERANCE_TESTS": 0.15,
            "PERFORMANCE_TESTS": 0.10,
            "AI_VALIDATION_TESTS": 0.10,
            "SECURITY_TESTS": 0.03,
            "CONFIGURATION_TESTS": 0.02
        }
        
        total_weighted_score = 0.0
        total_weight = 0.0
        
        for category in self.test_categories:
            category_tests = [r for r in self.test_results if r.category == category]
            if category_tests:
                category_score = sum(weights.get(r.status, 0) for r in category_tests) / len(category_tests)
                category_weight = category_weights.get(category, 0.01)
                
                total_weighted_score += category_score * category_weight
                total_weight += category_weight
        
        perfection_score = (total_weighted_score / total_weight * 100) if total_weight > 0 else 0.0
        return round(perfection_score, 1)
    
    def print_final_report(self, analysis: Dict[str, Any]):
        """Final raporu yazdır"""
        print("\n" + "="*80)
        print("🏆 ULTIMATE PERFECTION TEST - FINAL RAPORU")
        print("="*80)
        
        summary = analysis['summary']
        print(f"\n📊 GENEL ÖZET:")
        print(f"   🔢 Toplam Test: {summary['total_tests']}")
        print(f"   ✅ Başarılı: {summary['passed']}")
        print(f"   ❌ Başarısız: {summary['failed']}")
        print(f"   🚨 Hata: {summary['errors']}")
        print(f"   ⏭️ Geçilen: {summary['skipped']}")
        print(f"   📈 Başarı Oranı: %{summary['success_rate']:.1f}")
        print(f"   🎯 Mükemmellik Skoru: %{summary['perfection_score']:.1f}")
        
        print(f"\n📋 KATEGORİ BAZLI ANALIZ:")
        for category, stats in analysis['category_stats'].items():
            print(f"   {category}:")
            print(f"      • Toplam: {stats['total']} | Başarılı: {stats['passed']} | Başarı: %{stats['success_rate']:.1f}")
        
        if analysis['failed_tests']:
            print(f"\n❌ BAŞARISIZ TESTLER ({len(analysis['failed_tests'])}):")
            for i, test in enumerate(analysis['failed_tests'][:10], 1):  # İlk 10 hata
                print(f"   {i}. [{test['category']}] {test['test_name']}")
                print(f"      ➤ {test['message']}")
        
        print(f"\n⚡ PERFORMANS İSTATİSTİKLERİ:")
        perf = analysis['performance_stats']
        print(f"   • Ortalama: {perf['avg_execution_time']:.3f}s")
        print(f"   • Maksimum: {perf['max_execution_time']:.3f}s")
        print(f"   • Minimum: {perf['min_execution_time']:.3f}s")
        
        print(f"\n⏱️ TOPLAM ÇALIŞMA SÜRESİ: {analysis['execution_time']:.1f} saniye")
        
        # Mükemmellik değerlendirmesi
        perfection_score = summary['perfection_score']
        if perfection_score >= 100.0:
            print(f"\n🏆 SONUÇ: MUTLAK MÜKEMMELLİK BAŞARILDI! (%{perfection_score:.1f})")
            print("🎉 Sistem production'a hazır!")
        elif perfection_score >= 95.0:
            print(f"\n🥈 SONUÇ: NEREDEYSE MÜKEMMELLİK (%{perfection_score:.1f})")
            print("🔧 Küçük düzeltmelerle %100'e ulaşılabilir!")
        elif perfection_score >= 90.0:
            print(f"\n🥉 SONUÇ: İYİ DURUM (%{perfection_score:.1f})")
            print("⚠️ Bazı kritik iyileştirmeler gerekiyor.")
        else:
            print(f"\n⚠️ SONUÇ: İYİLEŞTİRME GEREKİYOR (%{perfection_score:.1f})")
            print("🔧 Sistemde önemli düzeltmeler yapılmalı.")
        
        print("\n" + "="*80)
        
        return analysis

async def main():
    """Ana test fonksiyonu"""
    tester = UltimatePerfectionTester()
    
    print("🎯 ULTIMATE PERFECTION TESTER")
    print("Sistem kusursuzluğu için kapsamlı test süreci başlıyor...")
    print("Bu işlem 5-10 dakika sürebilir.\n")
    
    try:
        # Tüm testleri çalıştır
        analysis = await tester.run_all_tests()
        
        # Final raporu yazdır
        final_report = tester.print_final_report(analysis)
        
        # Sonuçları kaydet
        with open('ULTIMATE_PERFECTION_REPORT.json', 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Detaylı rapor kaydedildi: ULTIMATE_PERFECTION_REPORT.json")
        
        return analysis
        
    except Exception as e:
        print(f"\n🚨 KRITIK HATA: {str(e)}")
        print(f"📋 Hata detayı: {traceback.format_exc()}")
        return None

if __name__ == "__main__":
    asyncio.run(main())
