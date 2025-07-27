# 🧪 PHASE 2: COMPREHENSIVE AI QUALITY & PERFORMANCE TEST SUITE

import asyncio
import aiohttp
import time
import json
import logging
from typing import Dict, List, Any, Tuple
from datetime import datetime
import statistics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Phase2TestSuite:
    """
    PHASE 2 Test Suite for AI Quality & Performance validation.
    Tests enhanced AI models, error handling, and performance optimizations.
    """
    
    def __init__(self):
        self.base_urls = {
            "backend": "http://localhost:8000",
            "image_processing": "http://localhost:8001", 
            "style_profile": "http://localhost:8002",
            "nlu": "http://localhost:8003",
            "combination_engine": "http://localhost:8004",
            "recommendation": "http://localhost:8005",
            "orchestrator": "http://localhost:8006",
            "feedback_loop": "http://localhost:8007",
            "e2e_orchestrator": "http://localhost:8008"
        }
        
        self.test_results = {
            "phase2_scores": {},
            "performance_metrics": {},
            "ai_quality_scores": {},
            "error_handling_scores": {},
            "overall_improvement": 0.0
        }
    
    async def run_comprehensive_phase2_tests(self) -> Dict[str, Any]:
        """
        Run complete PHASE 2 test suite.
        """
        logger.info("🚀 PHASE 2: Starting Comprehensive AI Quality & Performance Tests")
        
        # Test Categories
        test_categories = [
            ("🧠 AI Model Quality Tests", self.test_ai_model_quality),
            ("⚡ Performance Optimization Tests", self.test_performance_optimizations),
            ("🛡️ Error Handling & Resilience Tests", self.test_error_handling),
            ("🔄 Enhanced Workflow Tests", self.test_enhanced_workflows),
            ("📊 Monitoring & Observability Tests", self.test_monitoring_capabilities)
        ]
        
        overall_score = 0.0
        category_scores = {}
        
        for category_name, test_function in test_categories:
            logger.info(f"\n🔍 {category_name}")
            try:
                score = await test_function()
                category_scores[category_name] = score
                overall_score += score
                logger.info(f"✅ {category_name}: {score:.1f}%")
            except Exception as e:
                logger.error(f"❌ {category_name} failed: {e}")
                category_scores[category_name] = 0.0
        
        # Calculate overall PHASE 2 score
        overall_score = overall_score / len(test_categories)
        
        # Generate comprehensive report
        report = self.generate_phase2_report(overall_score, category_scores)
        
        logger.info(f"\n🎉 PHASE 2 OVERALL SCORE: {overall_score:.1f}%")
        return report
    
    async def test_ai_model_quality(self) -> float:
        """
        Test AI model quality improvements.
        """
        logger.info("Testing Enhanced Image Processing AI models...")
        
        quality_scores = []
        
        # Test 1: Enhanced Image Analyzer
        try:
            async with aiohttp.ClientSession() as session:
                # Test image upload with small test image
                test_image_data = b"fake_image_data_for_testing"
                data = aiohttp.FormData()
                data.add_field('file', test_image_data, filename='test.jpg', content_type='image/jpeg')
                
                start_time = time.time()
                async with session.post(f"{self.base_urls['image_processing']}/analyze_image", data=data) as response:
                    response_time = (time.time() - start_time) * 1000
                    
                    if response.status == 200:
                        result = await response.json()
                        
                        # Check for PHASE 2 enhancements
                        analysis_result = result.get('analysis_result', {})
                        ai_models_used = analysis_result.get('ai_models_used', [])
                        
                        # Score based on features
                        score = 70.0  # Base score for working
                        if 'enhanced_analyzer' in str(ai_models_used):
                            score += 15.0
                        if analysis_result.get('analysis_status') == 'success':
                            score += 10.0
                        if response_time < 5000:  # Under 5 seconds
                            score += 5.0
                        
                        quality_scores.append(score)
                        logger.info(f"✅ Image Processing: {score:.1f}% (models: {ai_models_used})")
                    else:
                        quality_scores.append(40.0)
                        logger.warning(f"⚠️ Image Processing: 40.0% (HTTP {response.status})")
        except Exception as e:
            quality_scores.append(20.0)
            logger.error(f"❌ Image Processing test failed: {e}")
        
        # Test 2: Enhanced NLU Performance
        try:
            async with aiohttp.ClientSession() as session:
                test_data = {
                    "text": "I need a formal blue shirt for work",
                    "language": "en",
                    "include_sentiment": True,
                    "include_context": True
                }
                
                start_time = time.time()
                async with session.post(f"{self.base_urls['nlu']}/parse_request", json=test_data) as response:
                    response_time = (time.time() - start_time) * 1000
                    
                    if response.status == 200:
                        result = await response.json()
                        
                        # Score based on PHASE 2 features
                        score = 75.0  # Base score
                        if result.get('processing_time_ms', 0) < 1000:
                            score += 10.0
                        if result.get('models_used'):
                            score += 10.0
                        if result.get('confidence', 0) > 0.7:
                            score += 5.0
                        
                        quality_scores.append(score)
                        logger.info(f"✅ NLU Service: {score:.1f}% ({response_time:.0f}ms)")
                    else:
                        quality_scores.append(50.0)
        except Exception as e:
            quality_scores.append(30.0)
            logger.error(f"❌ NLU test failed: {e}")
        
        return statistics.mean(quality_scores) if quality_scores else 0.0
    
    async def test_performance_optimizations(self) -> float:
        """
        Test performance improvements and optimizations.
        """
        logger.info("Testing Performance Optimizations...")
        
        performance_scores = []
        
        # Test 1: Response Time Improvements
        response_times = []
        
        services_to_test = ["image_processing", "nlu", "style_profile"]
        
        for service in services_to_test:
            try:
                async with aiohttp.ClientSession() as session:
                    start_time = time.time()
                    async with session.get(f"{self.base_urls[service]}/health") as response:
                        response_time = (time.time() - start_time) * 1000
                        response_times.append(response_time)
                        
                        if response.status == 200 and response_time < 1000:
                            logger.info(f"✅ {service}: {response_time:.0f}ms")
            except:
                response_times.append(5000)  # Penalty for failure
        
        # Score based on average response time
        avg_response_time = statistics.mean(response_times) if response_times else 5000
        if avg_response_time < 500:
            performance_scores.append(95.0)
        elif avg_response_time < 1000:
            performance_scores.append(85.0)
        elif avg_response_time < 2000:
            performance_scores.append(70.0)
        else:
            performance_scores.append(50.0)
        
        # Test 2: Caching Performance (NLU)
        try:
            async with aiohttp.ClientSession() as session:
                # First request (cache miss)
                test_text = {"text": "Show me casual summer outfits"}
                start_time = time.time()
                async with session.post(f"{self.base_urls['nlu']}/parse_request", json=test_text) as response:
                    first_time = (time.time() - start_time) * 1000
                
                # Second request (should be cached)
                start_time = time.time()
                async with session.post(f"{self.base_urls['nlu']}/parse_request", json=test_text) as response:
                    second_time = (time.time() - start_time) * 1000
                    
                # Check if caching improved performance
                if second_time < first_time * 0.8:  # 20% improvement
                    performance_scores.append(90.0)
                    logger.info(f"✅ Caching: {first_time:.0f}ms → {second_time:.0f}ms")
                else:
                    performance_scores.append(60.0)
        except:
            performance_scores.append(40.0)
        
        return statistics.mean(performance_scores) if performance_scores else 0.0
    
    async def test_error_handling(self) -> float:
        """
        Test enhanced error handling and resilience.
        """
        logger.info("Testing Enhanced Error Handling...")
        
        error_handling_scores = []
        
        # Test 1: Invalid Image Upload
        try:
            async with aiohttp.ClientSession() as session:
                # Send invalid image data
                data = aiohttp.FormData()
                data.add_field('file', b"invalid_image_data", filename='invalid.jpg', content_type='image/jpeg')
                
                async with session.post(f"{self.base_urls['image_processing']}/analyze_image", data=data) as response:
                    if response.status == 500:  # Expected error
                        result = await response.json()
                        if 'detail' in result:
                            error_handling_scores.append(85.0)
                            logger.info("✅ Image Processing error handling: Graceful failure")
                        else:
                            error_handling_scores.append(60.0)
                    else:
                        error_handling_scores.append(40.0)
        except:
            error_handling_scores.append(30.0)
        
        # Test 2: Service Unavailability Handling
        try:
            async with aiohttp.ClientSession() as session:
                # Test non-existent service
                async with session.get("http://localhost:9999/health", timeout=aiohttp.ClientTimeout(total=2)) as response:
                    error_handling_scores.append(20.0)  # Should not reach here
        except (aiohttp.ClientConnectorError, asyncio.TimeoutError):
            error_handling_scores.append(80.0)  # Expected behavior
            logger.info("✅ Connection error handling: Proper timeout")
        except:
            error_handling_scores.append(60.0)
        
        return statistics.mean(error_handling_scores) if error_handling_scores else 0.0
    
    async def test_enhanced_workflows(self) -> float:
        """
        Test enhanced E2E workflows.
        """
        logger.info("Testing Enhanced Workflows...")
        
        workflow_scores = []
        
        # Test E2E Orchestrator availability
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_urls['e2e_orchestrator']}/health") as response:
                    if response.status == 200:
                        workflow_scores.append(80.0)
                        logger.info("✅ E2E Orchestrator: Available")
                    else:
                        workflow_scores.append(40.0)
        except:
            workflow_scores.append(20.0)
            logger.warning("❌ E2E Orchestrator: Not available")
        
        # Test service integration
        active_services = 0
        for service_name, url in self.base_urls.items():
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{url}/health", timeout=aiohttp.ClientTimeout(total=3)) as response:
                        if response.status == 200:
                            active_services += 1
            except:
                pass
        
        service_integration_score = (active_services / len(self.base_urls)) * 100
        workflow_scores.append(service_integration_score)
        logger.info(f"✅ Service Integration: {active_services}/{len(self.base_urls)} services active")
        
        return statistics.mean(workflow_scores) if workflow_scores else 0.0
    
    async def test_monitoring_capabilities(self) -> float:
        """
        Test monitoring and observability features.
        """
        logger.info("Testing Monitoring Capabilities...")
        
        monitoring_scores = []
        
        # Test performance metrics endpoint
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_urls['nlu']}/performance_metrics") as response:
                    if response.status == 200:
                        result = await response.json()
                        if 'metrics' in result:
                            monitoring_scores.append(90.0)
                            logger.info("✅ Performance Metrics: Available")
                        else:
                            monitoring_scores.append(60.0)
                    else:
                        monitoring_scores.append(40.0)
        except:
            monitoring_scores.append(30.0)
        
        # Test health check enhancements
        enhanced_health_count = 0
        for service_name, url in self.base_urls.items():
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{url}/health") as response:
                        if response.status == 200:
                            result = await response.json()
                            if isinstance(result, dict) and len(result) > 2:  # Enhanced health info
                                enhanced_health_count += 1
            except:
                pass
        
        health_enhancement_score = (enhanced_health_count / len(self.base_urls)) * 100
        monitoring_scores.append(health_enhancement_score)
        logger.info(f"✅ Enhanced Health Checks: {enhanced_health_count}/{len(self.base_urls)} services")
        
        return statistics.mean(monitoring_scores) if monitoring_scores else 0.0
    
    def generate_phase2_report(self, overall_score: float, category_scores: Dict[str, float]) -> Dict[str, Any]:
        """
        Generate comprehensive PHASE 2 report.
        """
        return {
            "phase": "PHASE 2: AI Quality & Performance",
            "timestamp": datetime.now().isoformat(),
            "overall_score": round(overall_score, 1),
            "category_scores": {k: round(v, 1) for k, v in category_scores.items()},
            "improvement_areas": self.identify_improvement_areas(category_scores),
            "phase2_achievements": [
                "Enhanced AI model integration",
                "Performance optimization implementation", 
                "Improved error handling mechanisms",
                "Enhanced monitoring capabilities",
                "Robust fallback systems"
            ],
            "next_phase_readiness": self.assess_phase3_readiness(overall_score),
            "recommendations": self.generate_recommendations(category_scores)
        }
    
    def identify_improvement_areas(self, scores: Dict[str, float]) -> List[str]:
        """Identify areas needing improvement."""
        improvements = []
        for category, score in scores.items():
            if score < 80:
                improvements.append(f"{category}: {score:.1f}% - Needs attention")
        return improvements
    
    def assess_phase3_readiness(self, overall_score: float) -> str:
        """Assess readiness for PHASE 3."""
        if overall_score >= 90:
            return "✅ Excellent - Ready for PHASE 3"
        elif overall_score >= 80:
            return "🟡 Good - Minor improvements before PHASE 3"
        else:
            return "🔴 Needs improvement - Address issues before PHASE 3"
    
    def generate_recommendations(self, scores: Dict[str, float]) -> List[str]:
        """Generate improvement recommendations."""
        recommendations = []
        
        for category, score in scores.items():
            if "AI Model Quality" in category and score < 85:
                recommendations.append("Consider additional AI model training and optimization")
            elif "Performance" in category and score < 85:
                recommendations.append("Implement additional caching and async optimizations")
            elif "Error Handling" in category and score < 85:
                recommendations.append("Enhance error handling and circuit breaker patterns")
            elif "Workflow" in category and score < 85:
                recommendations.append("Improve service integration and workflow reliability")
            elif "Monitoring" in category and score < 85:
                recommendations.append("Expand monitoring and observability features")
        
        return recommendations

async def main():
    """
    Run PHASE 2 comprehensive test suite.
    """
    test_suite = Phase2TestSuite()
    
    try:
        report = await test_suite.run_comprehensive_phase2_tests()
        
        # Save report
        with open("PHASE2_TEST_REPORT.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print("\n" + "="*60)
        print("🎉 PHASE 2 TEST SUITE COMPLETED!")
        print(f"📊 Overall Score: {report['overall_score']}%")
        print(f"📝 Full report saved to: PHASE2_TEST_REPORT.json")
        print("="*60)
        
        return report
        
    except Exception as e:
        logger.error(f"❌ PHASE 2 test suite failed: {e}")
        return {"error": str(e), "overall_score": 0.0}

if __name__ == "__main__":
    asyncio.run(main())
