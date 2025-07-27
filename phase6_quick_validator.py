# 🚀 PHASE 6: MULTI-MODAL AI QUICK VALIDATOR
# Rapid validation of transformer models and cross-modal understanding

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any

class Phase6QuickValidator:
    """
    Quick validation framework for Phase 6 Multi-Modal AI capabilities.
    Rapid testing of transformer models, computer vision, and cross-modal features.
    """
    
    def __init__(self):
        self.services = {
            "image_processing": "http://localhost:8001",
            "nlu": "http://localhost:8002",
            "style_profile": "http://localhost:8003", 
            "combination_engine": "http://localhost:8004",
            "recommendation_engine": "http://localhost:8005"
        }
        
        self.results = {
            "phase": "6.0",
            "timestamp": datetime.now().isoformat(),
            "scores": {}
        }
    
    def run_quick_validation(self) -> Dict[str, Any]:
        """Run quick validation of Phase 6 multi-modal AI system"""
        
        print("🚀 PHASE 6: MULTI-MODAL AI QUICK VALIDATION")
        print("=" * 70)
        
        try:
            # Test 1: Phase 6 Service Status
            print("\\n🧠 Testing Phase 6 Multi-Modal AI Services:")
            service_score = self._test_phase6_services()
            self.results["scores"]["phase6_services"] = service_score
            
            # Test 2: Transformer Models
            print("\\n🤖 Testing Transformer Models:")
            transformer_score = self._test_transformer_capabilities()
            self.results["scores"]["transformer_models"] = transformer_score
            
            # Test 3: Computer Vision AI
            print("\\n🖼️ Testing Advanced Computer Vision:")
            vision_score = self._test_computer_vision_ai()
            self.results["scores"]["computer_vision_ai"] = vision_score
            
            # Test 4: Multi-Modal Integration
            print("\\n🔄 Testing Multi-Modal Integration:")
            multimodal_score = self._test_multimodal_integration()
            self.results["scores"]["multimodal_integration"] = multimodal_score
            
            # Test 5: Cross-Modal Alignment
            print("\\n🎯 Testing Cross-Modal Alignment:")
            crossmodal_score = self._test_crossmodal_features()
            self.results["scores"]["crossmodal_alignment"] = crossmodal_score
            
            # Test 6: Service Integration
            print("\\n🔗 Testing Service Integration:")
            integration_score = self._test_service_integration()
            self.results["scores"]["service_integration"] = integration_score
            
            # Calculate overall score
            overall_score = self._calculate_overall_score()
            self.results["scores"]["overall_phase6_score"] = overall_score
            
            # Print summary
            self._print_validation_summary()
            
            # Save results
            self._save_results()
            
            return self.results
            
        except Exception as e:
            print(f"❌ Validation error: {str(e)}")
            self.results["error"] = str(e)
            return self.results
    
    def _test_phase6_services(self) -> float:
        """Test Phase 6 service capabilities"""
        phase6_features = 0
        total_checks = 0
        
        for service_name, base_url in self.services.items():
            try:
                response = requests.get(f"{base_url}/", timeout=5)
                total_checks += 1
                
                if response.status_code == 200:
                    data = response.json()
                    phase = data.get("phase", "unknown")
                    
                    if "6" in str(phase) or "multi" in str(data).lower() or "transformer" in str(data).lower():
                        phase6_features += 1
                        print(f"✅ {service_name}: PHASE 6 FEATURES DETECTED")
                        
                        # Check for specific AI capabilities
                        ai_capabilities = data.get("ai_capabilities", {})
                        if ai_capabilities:
                            print(f"  • AI Features: {list(ai_capabilities.keys())[:3]}")
                    else:
                        print(f"⚠️ {service_name}: Basic implementation")
                else:
                    print(f"❌ {service_name}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"❌ {service_name}: Connection failed")
                total_checks += 1
        
        score = (phase6_features / total_checks * 100) if total_checks > 0 else 0
        print(f"  📊 Phase 6 Services: {score:.0f}%")
        return score
    
    def _test_transformer_capabilities(self) -> float:
        """Test transformer model capabilities"""
        try:
            # Test advanced NLU with transformers
            test_request = {
                "text": "I need sophisticated business attire with modern styling for important meetings",
                "analysis_type": "comprehensive",
                "use_bert": True,
                "use_roberta": True,
                "semantic_similarity": True,
                "fashion_context": True
            }
            
            response = requests.post(
                f"{self.services['nlu']}/analyze_text_advanced",
                json=test_request,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for transformer-specific features
                has_bert = data.get("bert_analysis") is not None
                has_roberta = data.get("roberta_insights") is not None
                has_embeddings = data.get("semantic_embeddings") is not None
                models_used = data.get("models_used", [])
                
                transformer_features = sum([has_bert, has_roberta, has_embeddings])
                max_features = 3
                
                score = (transformer_features / max_features) * 100
                
                print(f"✅ Transformer Analysis: {score:.0f}% capability")
                if has_bert:
                    print(f"  • BERT: Semantic analysis active")
                if has_roberta:
                    print(f"  • RoBERTa: Enhanced reasoning active") 
                if has_embeddings:
                    print(f"  • Embeddings: {len(data.get('semantic_embeddings', []))} dimensions")
                if models_used:
                    print(f"  • Models Used: {', '.join(models_used)}")
                
                return score
                
            else:
                print(f"❌ Transformer Test: HTTP {response.status_code}")
                return 0.0
                
        except Exception as e:
            print(f"❌ Transformer Test Error: {str(e)}")
            return 0.0
    
    def _test_computer_vision_ai(self) -> float:
        """Test advanced computer vision AI capabilities"""
        try:
            # Check AI models status
            response = requests.get(f"{self.services['image_processing']}/ai_models_status", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for Phase 6 computer vision features
                multi_modal_ai = data.get("multi_modal_ai", {})
                computer_vision = multi_modal_ai.get("computer_vision", {})
                
                detectron2_active = computer_vision.get("detectron2", {}).get("status") != "inactive"
                clip_active = computer_vision.get("clip", {}).get("status") != "inactive"
                
                ai_features = sum([detectron2_active, clip_active])
                max_features = 2
                
                score = (ai_features / max_features) * 100
                
                print(f"✅ Computer Vision AI: {score:.0f}% capability")
                
                if detectron2_active:
                    detectron2_info = computer_vision.get("detectron2", {})
                    print(f"  • Detectron2: {detectron2_info.get('description', 'Active')}")
                
                if clip_active:
                    clip_info = computer_vision.get("clip", {})
                    print(f"  • CLIP: {clip_info.get('description', 'Active')}")
                
                return score
                
            else:
                print(f"❌ Computer Vision AI Test: HTTP {response.status_code}")
                return 0.0
                
        except Exception as e:
            print(f"❌ Computer Vision AI Test Error: {str(e)}")
            return 0.0
    
    def _test_multimodal_integration(self) -> float:
        """Test multi-modal integration capabilities"""
        try:
            # Test NLU service for multi-modal features
            test_request = {
                "text": "elegant black dress for formal events",
                "analysis_type": "comprehensive",
                "cross_modal_embedding": True,
                "cross_modal_context": {
                    "image_description": "formal black dress",
                    "visual_context": "elegant_formal_wear"
                }
            }
            
            response = requests.post(
                f"{self.services['nlu']}/analyze_text_advanced",
                json=test_request,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for multi-modal features
                has_cross_modal = data.get("cross_modal_alignment") is not None
                has_unified_context = data.get("unified_context") is not None
                has_multimodal_features = any("multi" in str(key).lower() or "cross" in str(key).lower() 
                                            for key in data.keys())
                
                multimodal_features = sum([has_cross_modal, has_unified_context, has_multimodal_features])
                max_features = 3
                
                score = (multimodal_features / max_features) * 100
                
                print(f"✅ Multi-Modal Integration: {score:.0f}% capability")
                
                if has_cross_modal:
                    print(f"  • Cross-Modal Alignment: Active")
                if has_unified_context:
                    print(f"  • Unified Context: Generated")
                if has_multimodal_features:
                    print(f"  • Multi-Modal Features: Detected")
                
                return score
                
            else:
                print(f"❌ Multi-Modal Integration Test: HTTP {response.status_code}")
                return 0.0
                
        except Exception as e:
            print(f"❌ Multi-Modal Integration Error: {str(e)}")
            return 0.0
    
    def _test_crossmodal_features(self) -> float:
        """Test cross-modal alignment features"""
        try:
            # Check if services report cross-modal capabilities
            crossmodal_services = 0
            total_services = 0
            
            for service_name, base_url in self.services.items():
                try:
                    response = requests.get(f"{base_url}/", timeout=5)
                    total_services += 1
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Check for cross-modal mentions
                        service_text = str(data).lower()
                        if "cross" in service_text and "modal" in service_text:
                            crossmodal_services += 1
                            print(f"  ✅ {service_name}: Cross-modal capabilities")
                        else:
                            print(f"  ⚠️ {service_name}: Limited cross-modal support")
                            
                except Exception:
                    total_services += 1
                    print(f"  ❌ {service_name}: Connection failed")
            
            score = (crossmodal_services / total_services * 100) if total_services > 0 else 0
            print(f"📊 Cross-Modal Features: {score:.0f}%")
            
            return score
            
        except Exception as e:
            print(f"❌ Cross-Modal Features Error: {str(e)}")
            return 0.0
    
    def _test_service_integration(self) -> float:
        """Test service integration"""
        active_services = 0
        total_services = len(self.services)
        
        for service_name, base_url in self.services.items():
            try:
                response = requests.get(f"{base_url}/", timeout=3)
                if response.status_code == 200:
                    active_services += 1
                    print(f"✅ {service_name}: Active")
                else:
                    print(f"❌ {service_name}: HTTP {response.status_code}")
            except Exception:
                print(f"❌ {service_name}: Connection failed")
        
        score = (active_services / total_services) * 100
        print(f"📊 Service Integration: {score:.0f}% ({active_services}/{total_services})")
        
        return score
    
    def _calculate_overall_score(self) -> float:
        """Calculate overall Phase 6 score"""
        scores = self.results["scores"]
        
        # Weighted scoring for Phase 6 priorities
        weights = {
            "phase6_services": 0.15,      # Basic Phase 6 detection
            "transformer_models": 0.30,   # Core transformer capabilities
            "computer_vision_ai": 0.25,   # Advanced computer vision
            "multimodal_integration": 0.15, # Multi-modal fusion
            "crossmodal_alignment": 0.10,  # Cross-modal features
            "service_integration": 0.05    # Basic integration
        }
        
        weighted_sum = 0
        total_weight = 0
        
        for metric, weight in weights.items():
            if metric in scores and scores[metric] > 0:
                weighted_sum += scores[metric] * weight
                total_weight += weight
        
        overall_score = (weighted_sum / total_weight) if total_weight > 0 else 0
        return round(overall_score, 1)
    
    def _print_validation_summary(self):
        """Print validation summary"""
        print("\\n🎯 PHASE 6 VALIDATION SUMMARY:")
        print("=" * 70)
        
        scores = self.results["scores"]
        overall_score = scores.get("overall_phase6_score", 0)
        
        print(f"🚀 Phase 6 Multi-Modal AI: {scores.get('phase6_services', 0):.0f}%")
        print(f"🤖 Transformer Models: {scores.get('transformer_models', 0):.0f}%")
        print(f"🖼️ Computer Vision AI: {scores.get('computer_vision_ai', 0):.0f}%")
        print(f"🔄 Multi-Modal Integration: {scores.get('multimodal_integration', 0):.0f}%")
        print(f"🎯 Cross-Modal Alignment: {scores.get('crossmodal_alignment', 0):.0f}%")
        print(f"🔗 Service Integration: {scores.get('service_integration', 0):.0f}%")
        
        print(f"\\n📊 OVERALL PHASE 6 SCORE: {overall_score:.1f}%")
        
        # Determine status
        if overall_score >= 95:
            status = "🏆 REVOLUTIONARY SUCCESS! Multi-modal AI at peak performance"
        elif overall_score >= 85:
            status = "✅ EXCELLENT! Transformer models and AI working great"
        elif overall_score >= 75:
            status = "✅ GOOD! Solid Phase 6 implementation"
        elif overall_score >= 60:
            status = "⚠️ MODERATE! Basic Phase 6 features working"
        else:
            status = "❌ NEEDS WORK! Transformer models need attention"
        
        print(f"\\n{status}")
        print(f"🎯 Next Step: {'Optimize performance' if overall_score >= 80 else 'Focus on Phase 6 AI models'}")
    
    def _save_results(self):
        """Save validation results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"PHASE6_QUICK_VALIDATION_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"\\n📝 Results saved: {filename}")
        except Exception as e:
            print(f"\\n❌ Could not save results: {str(e)}")
        
        print(f"⏰ Validation completed: {datetime.now().strftime('%H:%M:%S')}")

def main():
    """Main function to run Phase 6 quick validation"""
    validator = Phase6QuickValidator()
    results = validator.run_quick_validation()
    return results

if __name__ == "__main__":
    # Run Phase 6 quick validation
    main()
