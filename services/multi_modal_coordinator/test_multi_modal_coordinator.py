# 🧪 Multi-Modal Coordinator Service Test Suite
# AURA AI Çok Modlu Sorgu Koordinatörü Comprehensive Testing

"""
Multi-Modal Coordinator Service Test Suite

Bu test dosyası çok modlu sorgu sisteminin tüm bileşenlerini kapsamlı
bir şekilde test eder:
- CLIP tabanlı görsel analiz
- NLU tabanlı metin analizi
- Context fusion algoritması
- Service coordination matrix
- Quality assurance entegrasyonu
"""

import pytest
import asyncio
import base64
import json
import time
from datetime import datetime
from typing import Dict, List, Any
from unittest.mock import AsyncMock, MagicMock, patch
import tempfile
import os

# Test dependencies
import httpx
from fastapi.testclient import TestClient
from PIL import Image
import io

# Application imports
from main import app
from multi_modal_engine import (
    MultiModalCoordinator,
    MultiModalQueryRequest,
    MultiModalQueryResponse,
    CLIPImageProcessor,
    NLUTextProcessor,
    ContextFusionEngine
)

# Test client oluştur - FastAPI test için
client = TestClient(app)

class TestMultiModalCoordinator:
    """Multi-Modal Coordinator ana test sınıfı"""
    
    def setup_method(self):
        """Her test öncesi çalışan setup metodu"""
        # Test verileri hazırla
        self.test_image_base64 = self._create_test_image_base64()
        self.test_queries = [
            "Bu mavi gömlekle ne giyebilirim?",
            "Bu siyah elbiseye uygun ayakkabı var mı?",
            "Bu lacivert pantolonla hangi ceketi önerirsin?",
            "Bu çantayla ne kombin olur?"
        ]
        
        # Mock coordinator instance
        self.coordinator = MultiModalCoordinator()
    
    def _create_test_image_base64(self) -> str:
        """Test için basit bir image oluştur ve base64'e çevir"""
        # Basit bir test image'i oluştur (100x100 mavi kare)
        image = Image.new('RGB', (100, 100), color='blue')
        
        # BytesIO buffer'ına kaydet
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG')
        
        # Base64 encode et
        image_data = buffer.getvalue()
        return base64.b64encode(image_data).decode('utf-8')
    
    @pytest.mark.asyncio
    async def test_health_check_endpoint(self):
        """Health check endpoint'ini test et"""
        # Health check isteği gönder
        response = client.get("/")
        
        # Response kontrolü
        assert response.status_code == 200
        data = response.json()
        
        # Health check response structure kontrolü
        assert "service" in data
        assert "status" in data
        assert "timestamp" in data
        assert "components" in data
        assert "processing_capabilities" in data
        
        # Service name kontrolü
        assert data["service"] == "AURA AI Multi-Modal Coordinator Service"
        
        print("✅ Health check endpoint test passed")
    
    @pytest.mark.asyncio
    async def test_service_capabilities_endpoint(self):
        """Service capabilities endpoint'ini test et"""
        # Capabilities isteği gönder
        response = client.get("/capabilities")
        
        # Response kontrolü
        assert response.status_code == 200
        data = response.json()
        
        # Capabilities structure kontrolü
        assert "service_name" in data
        assert "supported_query_types" in data
        assert "supported_image_formats" in data
        assert "processing_capabilities" in data
        assert "integration_services" in data
        
        # Query types kontrolü
        query_types = [qt["type"] for qt in data["supported_query_types"]]
        expected_types = ["shirt_combination", "dress_shoe_matching", "pants_jacket_pairing", "bag_outfit_styling"]
        assert all(qt in query_types for qt in expected_types)
        
        print("✅ Service capabilities endpoint test passed")
    
    @pytest.mark.asyncio 
    @patch('multi_modal_engine.MultiModalCoordinator.process_multimodal_query')
    async def test_multimodal_query_endpoint(self, mock_process):
        """Multi-modal query endpoint'ini test et"""
        # Mock response hazırla
        mock_response = MultiModalQueryResponse(
            query_id="test_query_123",
            success=True,
            unified_intent="kombin_önerisi_isteme",
            visual_analysis={
                "dominant_colors": ["blue", "white"],
                "clothing_type": "shirt",
                "style_category": "casual",
                "formality_level": "informal"
            },
            textual_analysis={
                "intent": "kombin_önerisi_isteme",
                "entities": ["gömlek", "mavi"],
                "query_type": "shirt_combination"
            },
            recommendations=[
                {
                    "item_type": "pants",
                    "suggestion": "Beyaz chino pantolon",
                    "confidence": 0.92,
                    "reasoning": "Mavi gömlek ile klassik beyaz kombinasyon"
                }
            ],
            fusion_confidence=0.89,
            processing_time_ms=1250.5,
            services_used=["image_processing", "nlu_service", "style_profile"],
            metadata={"test": True}
        )
        
        mock_process.return_value = mock_response
        
        # Test request hazırla
        test_request = {
            "image_base64": self.test_image_base64,
            "text_query": "Bu mavi gömlekle ne giyebilirim?",
            "user_id": "test_user",
            "context": {"test_scenario": "gömlek_kombinasyon"}
        }
        
        # Query endpoint'ine istek gönder
        response = client.post("/query", json=test_request)
        
        # Response kontrolü
        assert response.status_code == 200
        data = response.json()
        
        # Response structure kontrolü
        assert "query_id" in data
        assert "success" in data
        assert "unified_intent" in data
        assert "visual_analysis" in data
        assert "textual_analysis" in data
        assert "recommendations" in data
        assert "fusion_confidence" in data
        
        # Mock çağrısı kontrolü
        mock_process.assert_called_once()
        
        print("✅ Multi-modal query endpoint test passed")
    
    @pytest.mark.asyncio
    async def test_file_upload_endpoint(self):
        """File upload endpoint'ini test et"""
        # Test image dosyası oluştur
        test_image = Image.new('RGB', (100, 100), color='red')
        buffer = io.BytesIO()
        test_image.save(buffer, format='JPEG')
        buffer.seek(0)
        
        # Mock MultiModalCoordinator.process_multimodal_query
        with patch('multi_modal_engine.MultiModalCoordinator.process_multimodal_query') as mock_process:
            # Mock response
            mock_response = MultiModalQueryResponse(
                query_id="upload_test_123",
                success=True,
                unified_intent="elbise_ayakkabı_uyumu",
                visual_analysis={"clothing_type": "dress"},
                textual_analysis={"intent": "ayakkabı_uyumu_sorgulama"},
                recommendations=[{"item_type": "shoes", "suggestion": "Siyah topuklu ayakkabı"}],
                fusion_confidence=0.85,
                processing_time_ms=1100.0,
                services_used=["image_processing", "nlu_service"],
                metadata={}
            )
            mock_process.return_value = mock_response
            
            # File upload request
            files = {"image": ("test.jpg", buffer, "image/jpeg")}
            data = {
                "text_query": "Bu elbiseye uygun ayakkabı var mı?",
                "user_id": "test_user",
                "context": "{\"test\": true}"
            }
            
            response = client.post("/query/upload", files=files, data=data)
            
            # Response kontrolü
            assert response.status_code == 200
            response_data = response.json()
            
            assert "query_id" in response_data
            assert response_data["success"] == True
            assert "unified_intent" in response_data
            
        print("✅ File upload endpoint test passed")
    
    @pytest.mark.asyncio
    async def test_test_scenarios_endpoint(self):
        """Built-in test scenarios endpoint'ini test et"""
        # Mock MultiModalCoordinator.process_multimodal_query
        with patch('multi_modal_engine.MultiModalCoordinator.process_multimodal_query') as mock_process:
            # Mock response for test scenarios
            mock_response = MultiModalQueryResponse(
                query_id="scenario_test_123",
                success=True,
                unified_intent="kombin_önerisi_isteme",
                visual_analysis={"clothing_type": "shirt"},
                textual_analysis={"intent": "kombin_önerisi_isteme"},
                recommendations=[{"item_type": "pants", "suggestion": "Chino pantolon"}],
                fusion_confidence=0.88,
                processing_time_ms=1000.0,
                services_used=["image_processing", "nlu_service"],
                metadata={}
            )
            mock_process.return_value = mock_response
            
            # Test scenarios endpoint'ine istek gönder
            response = client.post("/test-scenarios")
            
            # Response kontrolü
            assert response.status_code == 200
            data = response.json()
            
            # Test results structure kontrolü
            assert "test_summary" in data
            assert "individual_results" in data
            assert "recommendations" in data
            
            # Test summary kontrolü
            summary = data["test_summary"]
            assert "total_scenarios" in summary
            assert "successful_tests" in summary
            assert "success_rate_percent" in summary
            assert "system_status" in summary
            
        print("✅ Test scenarios endpoint test passed")
    
    @pytest.mark.asyncio
    async def test_query_statistics_endpoint(self):
        """Query statistics endpoint'ini test et"""
        # Statistics endpoint'ine istek gönder
        response = client.get("/stats")
        
        # Response kontrolü
        assert response.status_code == 200
        data = response.json()
        
        # Statistics structure kontrolü
        assert "total_queries_processed" in data
        assert "average_processing_time_ms" in data
        assert "success_rate_percent" in data
        assert "most_common_query_types" in data
        assert "active_since" in data
        
        # Data types kontrolü
        assert isinstance(data["total_queries_processed"], int)
        assert isinstance(data["average_processing_time_ms"], (int, float))
        assert isinstance(data["success_rate_percent"], (int, float))
        assert isinstance(data["most_common_query_types"], list)
        
        print("✅ Query statistics endpoint test passed")

class TestCLIPImageProcessor:
    """CLIP Image Processor test sınıfı"""
    
    def setup_method(self):
        """Test setup"""
        self.processor = CLIPImageProcessor()
        self.test_image_base64 = self._create_test_image()
    
    def _create_test_image(self) -> str:
        """Test image oluştur"""
        image = Image.new('RGB', (224, 224), color='navy')
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG')
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    @pytest.mark.asyncio
    async def test_analyze_image(self):
        """Image analysis fonksiyonunu test et"""
        # Mock CLIP model responses
        with patch.object(self.processor, '_extract_dominant_colors') as mock_colors, \
             patch.object(self.processor, '_detect_clothing_type') as mock_clothing, \
             patch.object(self.processor, '_categorize_style') as mock_style, \
             patch.object(self.processor, '_assess_formality') as mock_formality:
            
            # Mock return values
            mock_colors.return_value = ["navy", "blue"]
            mock_clothing.return_value = "shirt"
            mock_style.return_value = "business_casual"
            mock_formality.return_value = "formal"
            
            # Analyze image
            result = await self.processor.analyze_image(self.test_image_base64)
            
            # Result kontrolü
            assert "dominant_colors" in result
            assert "clothing_type" in result
            assert "style_category" in result
            assert "formality_level" in result
            assert "confidence_score" in result
            
            # Values kontrolü
            assert result["dominant_colors"] == ["navy", "blue"]
            assert result["clothing_type"] == "shirt"
            assert result["style_category"] == "business_casual"
            assert result["formality_level"] == "formal"
            
        print("✅ CLIP Image Processor test passed")

class TestNLUTextProcessor:
    """NLU Text Processor test sınıfı"""
    
    def setup_method(self):
        """Test setup"""
        self.processor = NLUTextProcessor()
    
    @pytest.mark.asyncio
    async def test_analyze_text(self):
        """Text analysis fonksiyonunu test et"""
        test_query = "Bu mavi gömlekle ne giyebilirim?"
        
        # Mock NLU service response
        with patch.object(self.processor, '_detect_intent') as mock_intent, \
             patch.object(self.processor, '_extract_entities') as mock_entities, \
             patch.object(self.processor, '_classify_query_type') as mock_query_type:
            
            # Mock return values
            mock_intent.return_value = "kombin_önerisi_isteme"
            mock_entities.return_value = ["gömlek", "mavi"]
            mock_query_type.return_value = "shirt_combination"
            
            # Analyze text
            result = await self.processor.analyze_text(test_query)
            
            # Result kontrolü
            assert "intent" in result
            assert "entities" in result
            assert "query_type" in result
            assert "confidence_score" in result
            
            # Values kontrolü
            assert result["intent"] == "kombin_önerisi_isteme"
            assert result["entities"] == ["gömlek", "mavi"]
            assert result["query_type"] == "shirt_combination"
            
        print("✅ NLU Text Processor test passed")

class TestContextFusionEngine:
    """Context Fusion Engine test sınıfı"""
    
    def setup_method(self):
        """Test setup"""
        self.fusion_engine = ContextFusionEngine()
    
    @pytest.mark.asyncio
    async def test_fuse_contexts(self):
        """Context fusion fonksiyonunu test et"""
        # Test data hazırla
        visual_analysis = {
            "dominant_colors": ["blue", "white"],
            "clothing_type": "shirt",
            "style_category": "casual",
            "formality_level": "informal"
        }
        
        textual_analysis = {
            "intent": "kombin_önerisi_isteme",
            "entities": ["gömlek", "mavi"],
            "query_type": "shirt_combination"
        }
        
        user_context = {
            "user_id": "test_user",
            "preferences": {"style": "casual", "colors": ["blue", "white"]}
        }
        
        # Fuse contexts
        result = await self.fusion_engine.fuse_contexts(
            visual_analysis, 
            textual_analysis, 
            user_context
        )
        
        # Result kontrolü
        assert "unified_intent" in result
        assert "combined_analysis" in result
        assert "confidence_score" in result
        assert "fusion_strategy" in result
        
        # Unified intent kontrolü
        assert result["unified_intent"] == "kombin_önerisi_isteme"
        
        # Combined analysis kontrolü
        combined = result["combined_analysis"]
        assert "item_type" in combined
        assert "colors" in combined
        assert "style_preferences" in combined
        
        print("✅ Context Fusion Engine test passed")

class TestErrorHandling:
    """Error handling test sınıfı"""
    
    @pytest.mark.asyncio
    async def test_invalid_image_format(self):
        """Invalid image format error handling"""
        # Invalid base64 string
        invalid_request = {
            "image_base64": "invalid_base64_string",
            "text_query": "Test query",
            "user_id": "test_user"
        }
        
        response = client.post("/query", json=invalid_request)
        
        # Error response kontrolü
        assert response.status_code == 500  # Internal server error expected
        
        print("✅ Invalid image format error handling test passed")
    
    @pytest.mark.asyncio
    async def test_empty_text_query(self):
        """Empty text query error handling"""
        # Empty text query
        empty_request = {
            "image_base64": "valid_base64_string",
            "text_query": "",
            "user_id": "test_user"
        }
        
        response = client.post("/query", json=empty_request)
        
        # Validation error kontrolü
        assert response.status_code == 422  # Validation error expected
        
        print("✅ Empty text query error handling test passed")
    
    @pytest.mark.asyncio
    async def test_large_file_upload(self):
        """Large file upload error handling"""
        # Create a large test image (simulate >10MB)
        large_image = Image.new('RGB', (5000, 5000), color='red')
        buffer = io.BytesIO()
        large_image.save(buffer, format='JPEG', quality=95)
        buffer.seek(0)
        
        files = {"image": ("large_test.jpg", buffer, "image/jpeg")}
        data = {"text_query": "Test query", "user_id": "test_user"}
        
        response = client.post("/query/upload", files=files, data=data)
        
        # File too large error kontrolü
        assert response.status_code == 413  # Payload too large expected
        
        print("✅ Large file upload error handling test passed")

# Integration tests
class TestIntegration:
    """Integration test sınıfı"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_multimodal_flow(self):
        """End-to-end multi-modal flow test"""
        # Mock all external services
        with patch('httpx.AsyncClient.get') as mock_get, \
             patch('httpx.AsyncClient.post') as mock_post:
            
            # Mock service responses
            mock_get.return_value = AsyncMock(status_code=200, json=lambda: {"status": "healthy"})
            mock_post.return_value = AsyncMock(status_code=200, json=lambda: {"result": "success"})
            
            # Create coordinator
            coordinator = MultiModalCoordinator()
            
            # Test request
            request = MultiModalQueryRequest(
                image_base64="test_image_base64",
                text_query="Bu mavi gömlekle ne giyebilirim?",
                user_id="test_user",
                context={"test": True}
            )
            
            # Process query (will use mocked services)
            result = await coordinator.process_multimodal_query(request)
            
            # Result kontrolü
            assert result.success == True
            assert "query_id" in result.query_id
            assert result.processing_time_ms > 0
            
        print("✅ End-to-end multi-modal flow test passed")

# Performance tests
class TestPerformance:
    """Performance test sınıfı"""
    
    @pytest.mark.asyncio
    async def test_query_processing_performance(self):
        """Query processing performance test"""
        # Mock coordinator for performance test
        with patch('multi_modal_engine.MultiModalCoordinator.process_multimodal_query') as mock_process:
            # Fast mock response
            mock_response = MultiModalQueryResponse(
                query_id="perf_test_123",
                success=True,
                unified_intent="test_intent",
                visual_analysis={},
                textual_analysis={},
                recommendations=[],
                fusion_confidence=0.8,
                processing_time_ms=500.0,
                services_used=[],
                metadata={}
            )
            mock_process.return_value = mock_response
            
            # Performance test
            start_time = time.time()
            
            # Multiple concurrent requests
            tasks = []
            for i in range(10):
                request_data = {
                    "image_base64": "test_image",
                    "text_query": f"Test query {i}",
                    "user_id": "test_user"
                }
                task = asyncio.create_task(
                    asyncio.to_thread(client.post, "/query", json=request_data)
                )
                tasks.append(task)
            
            # Wait for all requests
            responses = await asyncio.gather(*tasks)
            
            end_time = time.time()
            total_time = end_time - start_time
            
            # Performance assertions
            assert total_time < 5.0  # Should complete within 5 seconds
            assert all(r.status_code == 200 for r in responses)  # All should succeed
            
        print(f"✅ Performance test passed: {len(tasks)} requests in {total_time:.2f}s")

# Test runner
if __name__ == "__main__":
    print("🧪 Multi-Modal Coordinator Service Test Suite")
    print("=" * 60)
    
    # Run tests with pytest
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--asyncio-mode=auto",
        "-x"  # Stop on first failure
    ])
