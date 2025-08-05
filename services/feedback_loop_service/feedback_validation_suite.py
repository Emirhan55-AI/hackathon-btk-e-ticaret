# 🔄 AURA AI FEEDBACK LOOP - COMPREHENSIVE VALIDATION SUITE
# Prompt Engineering Feedback Sisteminin Kapsamlı Validasyonu

import asyncio
import json
import time
import statistics
from typing import Dict, List, Any, Tuple
from datetime import datetime
import colorama
from colorama import Fore, Back, Style

# Import our feedback engine for direct testing
try:
    from feedback_prompt_engineering import create_feedback_prompt_engine, FeedbackType
    DIRECT_TESTING_AVAILABLE = True
except ImportError:
    DIRECT_TESTING_AVAILABLE = False
    print("⚠️ Direct testing modülü yüklenemedi, sadece API testleri yapılacak")

colorama.init(autoreset=True)

class AuraFeedbackValidationSuite:
    """
    AURA Feedback Loop Prompt Engineering sisteminin kapsamlı validation test suite'i.
    Performance, accuracy, reliability ve system integration testlerini içerir.
    """
    
    def __init__(self):
        """Validation suite'ini başlat"""
        self.feedback_engine = None
        self.test_results = {
            "classification_accuracy": [],
            "processing_times": [],
            "confidence_scores": [],
            "service_coordination_success": [],
            "learning_effectiveness": []
        }
        
        # Test veri setini hazırla
        self.prepare_test_dataset()
        
        if DIRECT_TESTING_AVAILABLE:
            self.feedback_engine = create_feedback_prompt_engine()
            print(f"{Fore.GREEN}✅ Direct testing engine initialized{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}🔄 AURA FEEDBACK LOOP VALIDATION SUITE{Style.RESET_ALL}")
        print("=" * 60)
    
    def prepare_test_dataset(self):
        """Comprehensive test dataset hazırla"""
        self.test_dataset = [
            # Negative General Feedback Tests
            {
                "category": "negative_general",
                "samples": [
                    {
                        "feedback_text": "Bu kombini hiç beğenmedim",
                        "expected_type": "negative_general",
                        "confidence_threshold": 0.7,
                        "context": {"occasion": "work", "user_type": "professional"}
                    },
                    {
                        "feedback_text": "Kötü bir öneri, beğenmedim",
                        "expected_type": "negative_general", 
                        "confidence_threshold": 0.6,
                        "context": {"occasion": "casual", "user_type": "young_adult"}
                    },
                    {
                        "feedback_text": "Bu seçimler uygun değil bana",
                        "expected_type": "negative_general",
                        "confidence_threshold": 0.5,
                        "context": {"occasion": "formal", "user_type": "mature"}
                    }
                ]
            },
            
            # Color Dissatisfaction Tests
            {
                "category": "color_dissatisfaction",
                "samples": [
                    {
                        "feedback_text": "Renkleri hiç uyumlu değil",
                        "expected_type": "color_dissatisfaction",
                        "confidence_threshold": 0.8,
                        "context": {"colors": ["red", "green"], "harmony_type": "complementary"}
                    },
                    {
                        "feedback_text": "Bu kırmızı ile mor hiç yakışmıyor",
                        "expected_type": "color_dissatisfaction",
                        "confidence_threshold": 0.9,
                        "context": {"colors": ["red", "purple"], "harmony_type": "clash"}
                    },
                    {
                        "feedback_text": "Color combination is terrible",
                        "expected_type": "color_dissatisfaction",
                        "confidence_threshold": 0.7,
                        "context": {"language": "en", "colors": ["orange", "pink"]}
                    },
                    {
                        "feedback_text": "Bu tonlar birbirine hiç uymuyor",
                        "expected_type": "color_dissatisfaction",
                        "confidence_threshold": 0.8,
                        "context": {"colors": ["yellow", "brown"], "user_preference": "minimalist"}
                    }
                ]
            },
            
            # Positive General & Request Similar Tests
            {
                "category": "positive_similar",
                "samples": [
                    {
                        "feedback_text": "Beğendim, benzer önerilerde bulunabilir misiniz?",
                        "expected_type": "request_similar",
                        "confidence_threshold": 0.9,
                        "context": {"satisfaction": "high", "style": "casual"}
                    },
                    {
                        "feedback_text": "Mükemmel! Daha fazla böyle kombini istiyorum",
                        "expected_type": "request_similar",
                        "confidence_threshold": 0.8,
                        "context": {"satisfaction": "very_high", "style": "elegant"}
                    },
                    {
                        "feedback_text": "Süper olmuş, benzerlerini de göster",
                        "expected_type": "request_similar",
                        "confidence_threshold": 0.7,
                        "context": {"satisfaction": "high", "style": "trendy"}
                    }
                ]
            },
            
            # Occasion Appropriateness Tests
            {
                "category": "occasion_inappropriate",
                "samples": [
                    {
                        "feedback_text": "Bu öneri bana uygun değildi, çok resmi",
                        "expected_type": "occasion_inappropriate",
                        "confidence_threshold": 0.7,
                        "context": {"occasion": "casual", "dress_code": "formal"}
                    },
                    {
                        "feedback_text": "İş toplantısı için fazla rahat bu",
                        "expected_type": "occasion_inappropriate",
                        "confidence_threshold": 0.8,
                        "context": {"occasion": "business", "dress_code": "casual"}
                    },
                    {
                        "feedback_text": "Partiye uygun değil, çok sıradan",
                        "expected_type": "occasion_inappropriate",
                        "confidence_threshold": 0.6,
                        "context": {"occasion": "party", "dress_code": "casual"}
                    }
                ]
            },
            
            # Edge Cases and Complex Feedback
            {
                "category": "complex_cases",
                "samples": [
                    {
                        "feedback_text": "Gömlek güzel ama pantolon rengi uymuyor ve ayakkabılar da uygun değil",
                        "expected_type": "color_dissatisfaction",  # Primary issue
                        "confidence_threshold": 0.5,
                        "context": {"complexity": "high", "multiple_issues": True}
                    },
                    {
                        "feedback_text": "Bu kombini beğendim ama renk tonları biraz farklı olsaydı daha iyi olurdu",
                        "expected_type": "positive_general",  # Overall positive despite suggestion
                        "confidence_threshold": 0.4,
                        "context": {"complexity": "medium", "constructive_feedback": True}
                    },
                    {
                        "feedback_text": "👍👍👍 Harika! 😍",
                        "expected_type": "positive_general",
                        "confidence_threshold": 0.6,
                        "context": {"emoji_feedback": True, "language": "tr"}
                    }
                ]
            }
        ]
    
    def print_section_header(self, title: str, color=Fore.BLUE):
        """Test bölümü başlığı yazdır"""
        print(f"\n{Back.BLUE}{Fore.WHITE} {title} {Style.RESET_ALL}")
        print("─" * 60)
    
    def print_test_result(self, test_name: str, success: bool, details: str = ""):
        """Test sonucunu yazdır"""
        status = f"{Fore.GREEN}✅ PASS" if success else f"{Fore.RED}❌ FAIL"
        print(f"{status} {test_name}{Style.RESET_ALL}")
        if details:
            print(f"   {Fore.YELLOW}ℹ️  {details}{Style.RESET_ALL}")
    
    def test_classification_accuracy(self) -> Dict[str, Any]:
        """Classification accuracy'yi test et"""
        self.print_section_header("CLASSIFICATION ACCURACY TEST")
        
        if not DIRECT_TESTING_AVAILABLE:
            print(f"{Fore.YELLOW}⚠️ Direct testing unavailable, skipping accuracy test{Style.RESET_ALL}")
            return {"accuracy": 0.0, "details": "Direct testing not available"}
        
        total_tests = 0
        correct_predictions = 0
        category_results = {}
        
        for category_data in self.test_dataset:
            category = category_data["category"]
            samples = category_data["samples"]
            
            category_correct = 0
            category_total = len(samples)
            
            print(f"\n{Fore.CYAN}📂 Testing category: {category}{Style.RESET_ALL}")
            
            for i, sample in enumerate(samples, 1):
                feedback_data = {
                    "user_id": f"test_user_{category}_{i}",
                    "recommendation_id": f"test_rec_{category}_{i}",
                    "feedback_text": sample["feedback_text"],
                    "context": sample["context"]
                }
                
                try:
                    result = self.feedback_engine.analyze_feedback_with_prompt_patterns(feedback_data)
                    predicted_type = result['classification_results']['feedback_type']
                    confidence = result['classification_results']['confidence']
                    
                    is_correct = predicted_type == sample["expected_type"]
                    meets_threshold = confidence >= sample["confidence_threshold"]
                    
                    total_tests += 1
                    if is_correct:
                        correct_predictions += 1
                        category_correct += 1
                    
                    # Store results for analysis
                    self.test_results["classification_accuracy"].append({
                        "correct": is_correct,
                        "confidence": confidence,
                        "expected": sample["expected_type"],
                        "predicted": predicted_type,
                        "category": category
                    })
                    
                    status = "✅" if is_correct else "❌"
                    conf_status = "✅" if meets_threshold else "⚠️"
                    
                    print(f"  {status} Test {i}: {sample['feedback_text'][:30]}...")
                    print(f"     Expected: {sample['expected_type']}")
                    print(f"     Predicted: {predicted_type} {conf_status}({confidence:.2f})")
                    
                except Exception as e:
                    print(f"  ❌ Test {i} failed: {e}")
                    total_tests += 1
            
            category_accuracy = category_correct / category_total if category_total > 0 else 0
            category_results[category] = {
                "accuracy": category_accuracy,
                "correct": category_correct,
                "total": category_total
            }
            
            print(f"  📊 Category accuracy: {category_accuracy:.2%} ({category_correct}/{category_total})")
        
        overall_accuracy = correct_predictions / total_tests if total_tests > 0 else 0
        
        print(f"\n{Back.GREEN}{Fore.WHITE} CLASSIFICATION RESULTS {Style.RESET_ALL}")
        print(f"Overall Accuracy: {overall_accuracy:.2%} ({correct_predictions}/{total_tests})")
        
        # Per-category breakdown
        for category, results in category_results.items():
            acc = results["accuracy"]
            color = Fore.GREEN if acc >= 0.8 else Fore.YELLOW if acc >= 0.6 else Fore.RED
            print(f"{color}• {category}: {acc:.2%} ({results['correct']}/{results['total']}){Style.RESET_ALL}")
        
        return {
            "overall_accuracy": overall_accuracy,
            "category_results": category_results,
            "total_tests": total_tests,
            "correct_predictions": correct_predictions
        }
    
    def test_processing_performance(self) -> Dict[str, Any]:
        """Processing performance'ı test et"""
        self.print_section_header("PROCESSING PERFORMANCE TEST")
        
        if not DIRECT_TESTING_AVAILABLE:
            print(f"{Fore.YELLOW}⚠️ Direct testing unavailable, skipping performance test{Style.RESET_ALL}")
            return {"average_time": 0.0, "details": "Direct testing not available"}
        
        processing_times = []
        
        # Sample feedbacks for performance testing
        performance_samples = [
            "Bu kombini beğenmedim",
            "Renkleri uyumlu değil",
            "Mükemmel! Benzer öneriler istiyorum",
            "İş için uygun değil bu",
            "Çok güzel olmuş",
            "Bu tonlar hiç yakışmıyor",
            "Partiye uygun değil",
            "Harika kombinasyon! 👍",
            "Kötü seçim",
            "Bu stil bana göre değil"
        ]
        
        print(f"⏱️ Testing processing speed with {len(performance_samples)} samples...")
        
        for i, feedback_text in enumerate(performance_samples, 1):
            feedback_data = {
                "user_id": f"perf_test_user_{i}",
                "recommendation_id": f"perf_test_rec_{i}",
                "feedback_text": feedback_text
            }
            
            start_time = time.time()
            
            try:
                result = self.feedback_engine.analyze_feedback_with_prompt_patterns(feedback_data)
                processing_time = (time.time() - start_time) * 1000  # Convert to ms
                
                processing_times.append(processing_time)
                self.test_results["processing_times"].append(processing_time)
                
                if processing_time <= 150:  # Target: <150ms
                    status = f"{Fore.GREEN}✅"
                elif processing_time <= 300:  # Acceptable: <300ms
                    status = f"{Fore.YELLOW}⚠️"
                else:  # Slow: >300ms
                    status = f"{Fore.RED}❌"
                
                print(f"  {status} Sample {i}: {processing_time:.1f}ms{Style.RESET_ALL}")
                
            except Exception as e:
                print(f"  ❌ Sample {i} failed: {e}")
        
        if processing_times:
            avg_time = statistics.mean(processing_times)
            median_time = statistics.median(processing_times)
            min_time = min(processing_times)
            max_time = max(processing_times)
            std_dev = statistics.stdev(processing_times) if len(processing_times) > 1 else 0
            
            print(f"\n{Back.GREEN}{Fore.WHITE} PERFORMANCE RESULTS {Style.RESET_ALL}")
            print(f"Average Time: {avg_time:.1f}ms")
            print(f"Median Time: {median_time:.1f}ms")
            print(f"Min Time: {min_time:.1f}ms")
            print(f"Max Time: {max_time:.1f}ms")
            print(f"Std Deviation: {std_dev:.1f}ms")
            
            # Performance rating
            if avg_time <= 150:
                rating = f"{Fore.GREEN}EXCELLENT"
            elif avg_time <= 300:
                rating = f"{Fore.YELLOW}GOOD"
            elif avg_time <= 500:
                rating = f"{Fore.YELLOW}ACCEPTABLE"
            else:
                rating = f"{Fore.RED}NEEDS IMPROVEMENT"
            
            print(f"Performance Rating: {rating}{Style.RESET_ALL}")
            
            return {
                "average_time": avg_time,
                "median_time": median_time,
                "min_time": min_time,
                "max_time": max_time,
                "std_deviation": std_dev,
                "sample_count": len(processing_times)
            }
        
        return {"average_time": 0.0, "error": "No successful processing times recorded"}
    
    def test_prompt_pattern_consistency(self) -> Dict[str, Any]:
        """Prompt pattern tutarlılığını test et"""
        self.print_section_header("PROMPT PATTERN CONSISTENCY TEST")
        
        if not DIRECT_TESTING_AVAILABLE:
            print(f"{Fore.YELLOW}⚠️ Direct testing unavailable, skipping consistency test{Style.RESET_ALL}")
            return {"consistency": 0.0, "details": "Direct testing not available"}
        
        # Same feedback, multiple times to test consistency
        test_feedback = {
            "user_id": "consistency_test_user",
            "recommendation_id": "consistency_test_rec",
            "feedback_text": "Bu kombini beğenmedim, renkleri uyumlu değil"
        }
        
        iterations = 10
        results = []
        
        print(f"🔄 Testing consistency with {iterations} iterations...")
        print(f"Test feedback: \"{test_feedback['feedback_text']}\"")
        
        for i in range(iterations):
            try:
                result = self.feedback_engine.analyze_feedback_with_prompt_patterns(test_feedback)
                
                results.append({
                    "feedback_type": result['classification_results']['feedback_type'],
                    "confidence": result['classification_results']['confidence'],
                    "iteration": i + 1
                })
                
                print(f"  Iteration {i+1}: {result['classification_results']['feedback_type']} "
                      f"({result['classification_results']['confidence']:.2f})")
                
            except Exception as e:
                print(f"  ❌ Iteration {i+1} failed: {e}")
        
        if results:
            # Analyze consistency
            feedback_types = [r['feedback_type'] for r in results]
            confidences = [r['confidence'] for r in results]
            
            most_common_type = max(set(feedback_types), key=feedback_types.count)
            type_consistency = feedback_types.count(most_common_type) / len(feedback_types)
            
            avg_confidence = statistics.mean(confidences)
            confidence_std_dev = statistics.stdev(confidences) if len(confidences) > 1 else 0
            
            print(f"\n{Back.GREEN}{Fore.WHITE} CONSISTENCY RESULTS {Style.RESET_ALL}")
            print(f"Type Consistency: {type_consistency:.2%}")
            print(f"Most Common Type: {most_common_type}")
            print(f"Average Confidence: {avg_confidence:.2f}")
            print(f"Confidence Std Dev: {confidence_std_dev:.3f}")
            
            # Consistency rating
            if type_consistency >= 0.9 and confidence_std_dev <= 0.1:
                rating = f"{Fore.GREEN}EXCELLENT"
            elif type_consistency >= 0.8 and confidence_std_dev <= 0.15:
                rating = f"{Fore.YELLOW}GOOD"
            elif type_consistency >= 0.7:
                rating = f"{Fore.YELLOW}ACCEPTABLE"
            else:
                rating = f"{Fore.RED}INCONSISTENT"
            
            print(f"Consistency Rating: {rating}{Style.RESET_ALL}")
            
            return {
                "type_consistency": type_consistency,
                "most_common_type": most_common_type,
                "average_confidence": avg_confidence,
                "confidence_std_dev": confidence_std_dev,
                "iterations": iterations
            }
        
        return {"consistency": 0.0, "error": "No successful iterations"}
    
    def test_edge_cases(self) -> Dict[str, Any]:
        """Edge case'leri test et"""
        self.print_section_header("EDGE CASES TEST")
        
        if not DIRECT_TESTING_AVAILABLE:
            print(f"{Fore.YELLOW}⚠️ Direct testing unavailable, skipping edge cases test{Style.RESET_ALL}")
            return {"handled_cases": 0, "details": "Direct testing not available"}
        
        edge_cases = [
            {
                "name": "Empty feedback",
                "feedback_text": "",
                "should_handle": True
            },
            {
                "name": "Very short feedback",
                "feedback_text": "kötü",
                "should_handle": True
            },
            {
                "name": "Very long feedback",
                "feedback_text": "Bu kombini gerçekten hiç beğenmedim çünkü " * 20,
                "should_handle": True
            },
            {
                "name": "Special characters",
                "feedback_text": "Bu kombini beğenmedim!!! @#$%^&*()",
                "should_handle": True
            },
            {
                "name": "Mixed language",
                "feedback_text": "Bu combination hiç good değil",
                "should_handle": True
            },
            {
                "name": "Only emojis",
                "feedback_text": "😍😍😍👍👍👌",
                "should_handle": True
            },
            {
                "name": "Numbers and symbols",
                "feedback_text": "5/10 ⭐⭐⭐ rating",
                "should_handle": True
            }
        ]
        
        handled_successfully = 0
        edge_case_results = []
        
        for case in edge_cases:
            print(f"\n🧪 Testing: {case['name']}")
            print(f"   Input: \"{case['feedback_text'][:50]}{'...' if len(case['feedback_text']) > 50 else ''}\"")
            
            feedback_data = {
                "user_id": f"edge_test_user",
                "recommendation_id": f"edge_test_rec",
                "feedback_text": case['feedback_text']
            }
            
            try:
                result = self.feedback_engine.analyze_feedback_with_prompt_patterns(feedback_data)
                
                # Check if we got a reasonable result
                has_classification = 'classification_results' in result
                has_confidence = has_classification and 'confidence' in result['classification_results']
                confidence_reasonable = has_confidence and 0.0 <= result['classification_results']['confidence'] <= 1.0
                
                success = has_classification and has_confidence and confidence_reasonable
                
                if success:
                    handled_successfully += 1
                    status = f"{Fore.GREEN}✅ HANDLED"
                    feedback_type = result['classification_results']['feedback_type']
                    confidence = result['classification_results']['confidence']
                    print(f"   {status}: {feedback_type} (confidence: {confidence:.2f}){Style.RESET_ALL}")
                else:
                    status = f"{Fore.YELLOW}⚠️ PARTIAL"
                    print(f"   {status}: Result incomplete or invalid{Style.RESET_ALL}")
                
                edge_case_results.append({
                    "case": case['name'],
                    "success": success,
                    "result": result if success else None
                })
                
            except Exception as e:
                status = f"{Fore.RED}❌ ERROR"
                print(f"   {status}: {str(e)[:100]}...{Style.RESET_ALL}")
                edge_case_results.append({
                    "case": case['name'],
                    "success": False,
                    "error": str(e)
                })
        
        success_rate = handled_successfully / len(edge_cases)
        
        print(f"\n{Back.GREEN}{Fore.WHITE} EDGE CASES RESULTS {Style.RESET_ALL}")
        print(f"Successfully Handled: {handled_successfully}/{len(edge_cases)}")
        print(f"Success Rate: {success_rate:.2%}")
        
        if success_rate >= 0.8:
            rating = f"{Fore.GREEN}ROBUST"
        elif success_rate >= 0.6:
            rating = f"{Fore.YELLOW}ADEQUATE"
        else:
            rating = f"{Fore.RED}NEEDS IMPROVEMENT"
        
        print(f"Robustness Rating: {rating}{Style.RESET_ALL}")
        
        return {
            "handled_cases": handled_successfully,
            "total_cases": len(edge_cases),
            "success_rate": success_rate,
            "results": edge_case_results
        }
    
    def generate_comprehensive_report(self, test_results: Dict[str, Any]):
        """Kapsamlı test raporu oluştur"""
        self.print_section_header("COMPREHENSIVE VALIDATION REPORT", Fore.MAGENTA)
        
        print(f"{Back.MAGENTA}{Fore.WHITE} AURA FEEDBACK LOOP VALIDATION SUMMARY {Style.RESET_ALL}")
        print(f"Validation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Test Environment: {'Direct Engine Testing' if DIRECT_TESTING_AVAILABLE else 'API Testing Only'}")
        print()
        
        # Overall system rating
        overall_scores = []
        
        if 'classification' in test_results:
            acc = test_results['classification']['overall_accuracy']
            print(f"{Fore.CYAN}📊 CLASSIFICATION ACCURACY{Style.RESET_ALL}")
            print(f"   Overall Accuracy: {acc:.2%}")
            
            if acc >= 0.9:
                acc_rating = f"{Fore.GREEN}EXCELLENT"
                acc_score = 5
            elif acc >= 0.8:
                acc_rating = f"{Fore.GREEN}GOOD"
                acc_score = 4
            elif acc >= 0.7:
                acc_rating = f"{Fore.YELLOW}ACCEPTABLE"
                acc_score = 3
            elif acc >= 0.6:
                acc_rating = f"{Fore.YELLOW}NEEDS IMPROVEMENT"
                acc_score = 2
            else:
                acc_rating = f"{Fore.RED}POOR"
                acc_score = 1
            
            print(f"   Rating: {acc_rating}{Style.RESET_ALL}")
            overall_scores.append(acc_score)
        
        if 'performance' in test_results:
            avg_time = test_results['performance']['average_time']
            print(f"\n{Fore.CYAN}⏱️ PROCESSING PERFORMANCE{Style.RESET_ALL}")
            print(f"   Average Processing Time: {avg_time:.1f}ms")
            
            if avg_time <= 150:
                perf_rating = f"{Fore.GREEN}EXCELLENT"
                perf_score = 5
            elif avg_time <= 300:
                perf_rating = f"{Fore.GREEN}GOOD"
                perf_score = 4
            elif avg_time <= 500:
                perf_rating = f"{Fore.YELLOW}ACCEPTABLE"
                perf_score = 3
            elif avg_time <= 1000:
                perf_rating = f"{Fore.YELLOW}SLOW"
                perf_score = 2
            else:
                perf_rating = f"{Fore.RED}TOO SLOW"
                perf_score = 1
            
            print(f"   Rating: {perf_rating}{Style.RESET_ALL}")
            overall_scores.append(perf_score)
        
        if 'consistency' in test_results:
            consistency = test_results['consistency']['type_consistency']
            print(f"\n{Fore.CYAN}🔄 PATTERN CONSISTENCY{Style.RESET_ALL}")
            print(f"   Type Consistency: {consistency:.2%}")
            
            if consistency >= 0.95:
                cons_rating = f"{Fore.GREEN}EXCELLENT"
                cons_score = 5
            elif consistency >= 0.85:
                cons_rating = f"{Fore.GREEN}GOOD"
                cons_score = 4
            elif consistency >= 0.75:
                cons_rating = f"{Fore.YELLOW}ACCEPTABLE"
                cons_score = 3
            elif consistency >= 0.65:
                cons_rating = f"{Fore.YELLOW}INCONSISTENT"
                cons_score = 2
            else:
                cons_rating = f"{Fore.RED}VERY INCONSISTENT"
                cons_score = 1
            
            print(f"   Rating: {cons_rating}{Style.RESET_ALL}")
            overall_scores.append(cons_score)
        
        if 'edge_cases' in test_results:
            robustness = test_results['edge_cases']['success_rate']
            print(f"\n{Fore.CYAN}🛡️ ROBUSTNESS (Edge Cases){Style.RESET_ALL}")
            print(f"   Edge Case Success Rate: {robustness:.2%}")
            
            if robustness >= 0.9:
                robust_rating = f"{Fore.GREEN}VERY ROBUST"
                robust_score = 5
            elif robustness >= 0.8:
                robust_rating = f"{Fore.GREEN}ROBUST"
                robust_score = 4
            elif robustness >= 0.7:
                robust_rating = f"{Fore.YELLOW}ADEQUATE"
                robust_score = 3
            elif robustness >= 0.5:
                robust_rating = f"{Fore.YELLOW}FRAGILE"
                robust_score = 2
            else:
                robust_rating = f"{Fore.RED}VERY FRAGILE"
                robust_score = 1
            
            print(f"   Rating: {robust_rating}{Style.RESET_ALL}")
            overall_scores.append(robust_score)
        
        # Calculate overall system score
        if overall_scores:
            overall_score = statistics.mean(overall_scores)
            
            print(f"\n{Back.CYAN}{Fore.WHITE} OVERALL SYSTEM RATING {Style.RESET_ALL}")
            
            if overall_score >= 4.5:
                overall_rating = f"{Fore.GREEN}⭐⭐⭐⭐⭐ EXCELLENT"
                recommendation = "System is production-ready with excellent performance"
            elif overall_score >= 3.5:
                overall_rating = f"{Fore.GREEN}⭐⭐⭐⭐ GOOD"
                recommendation = "System is ready for production with minor optimizations"
            elif overall_score >= 2.5:
                overall_rating = f"{Fore.YELLOW}⭐⭐⭐ ACCEPTABLE"
                recommendation = "System needs improvements before production deployment"
            elif overall_score >= 1.5:
                overall_rating = f"{Fore.YELLOW}⭐⭐ NEEDS WORK"
                recommendation = "Significant improvements required"
            else:
                overall_rating = f"{Fore.RED}⭐ POOR"
                recommendation = "Major redesign or fixes required"
            
            print(f"Overall Rating: {overall_rating}{Style.RESET_ALL}")
            print(f"Score: {overall_score:.1f}/5.0")
            print(f"Recommendation: {recommendation}")
        
        # Recommendations
        print(f"\n{Fore.CYAN}💡 IMPROVEMENT RECOMMENDATIONS{Style.RESET_ALL}")
        
        if 'classification' in test_results and test_results['classification']['overall_accuracy'] < 0.8:
            print("• Improve classification accuracy with better training data")
            print("• Fine-tune prompt patterns for edge cases")
        
        if 'performance' in test_results and test_results['performance']['average_time'] > 300:
            print("• Optimize prompt processing pipeline")
            print("• Consider caching mechanisms for repeated patterns")
        
        if 'consistency' in test_results and test_results['consistency']['type_consistency'] < 0.9:
            print("• Stabilize prompt pattern responses")
            print("• Review and strengthen prompt engineering guidelines")
        
        if 'edge_cases' in test_results and test_results['edge_cases']['success_rate'] < 0.8:
            print("• Enhance error handling for edge cases")
            print("• Add more robust input validation and preprocessing")
        
        print(f"\n{Fore.GREEN}✅ Validation completed successfully!{Style.RESET_ALL}")
    
    def run_full_validation(self):
        """Tüm validation testlerini çalıştır"""
        print(f"{Back.MAGENTA}{Fore.WHITE} STARTING COMPREHENSIVE VALIDATION SUITE {Style.RESET_ALL}")
        print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        all_results = {}
        
        # Run all tests
        all_results['classification'] = self.test_classification_accuracy()
        all_results['performance'] = self.test_processing_performance()
        all_results['consistency'] = self.test_prompt_pattern_consistency()
        all_results['edge_cases'] = self.test_edge_cases()
        
        # Generate comprehensive report
        self.generate_comprehensive_report(all_results)
        
        print(f"\n{Back.MAGENTA}{Fore.WHITE} VALIDATION SUITE COMPLETED {Style.RESET_ALL}")
        print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return all_results

def main():
    """Ana validation fonksiyonu"""
    print(f"{Fore.CYAN}🔄 AURA AI Feedback Loop Validation Suite{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Bu suite, feedback loop prompt engineering sisteminin kapsamlı validasyonunu yapar.{Style.RESET_ALL}")
    print()
    
    if not DIRECT_TESTING_AVAILABLE:
        print(f"{Fore.YELLOW}⚠️ Direct testing modülü bulunamadı.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Lütfen feedback_prompt_engineering.py dosyasının mevcut olduğundan emin olun.{Style.RESET_ALL}")
        print()
    
    validator = AuraFeedbackValidationSuite()
    
    while True:
        print(f"\n{Fore.CYAN}📋 VALIDATION MENU:{Style.RESET_ALL}")
        print("1. 📊 Classification Accuracy Test")
        print("2. ⏱️ Processing Performance Test")
        print("3. 🔄 Prompt Pattern Consistency Test")
        print("4. 🛡️ Edge Cases Robustness Test")
        print("5. 🎯 Full Comprehensive Validation")
        print("0. ❌ Exit")
        
        try:
            choice = input(f"\n{Fore.YELLOW}Select option (0-5): {Style.RESET_ALL}").strip()
            
            if choice == "0":
                print(f"{Fore.CYAN}👋 Exiting validation suite...{Style.RESET_ALL}")
                break
            elif choice == "1":
                validator.test_classification_accuracy()
            elif choice == "2":
                validator.test_processing_performance()
            elif choice == "3":
                validator.test_prompt_pattern_consistency()
            elif choice == "4":
                validator.test_edge_cases()
            elif choice == "5":
                validator.run_full_validation()
            else:
                print(f"{Fore.RED}❌ Invalid choice. Please select 0-5.{Style.RESET_ALL}")
                
        except KeyboardInterrupt:
            print(f"\n{Fore.CYAN}👋 Validation interrupted.{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}❌ Unexpected error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
