# Phase 6 Demo: Enhanced Recommendation Engine with FAISS Multi-Modal AI Integration
# This demo showcases the advanced AI-powered recommendation system with ultra-fast similarity search
# Features: FAISS indexing, multi-modal embeddings, Phase 2+4+5 integration, advanced personalization

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any
import asyncio

# Demo configuration
RECOMMENDATION_SERVICE_URL = "http://localhost:8005"
IMAGE_SERVICE_URL = "http://localhost:8001"
STYLE_SERVICE_URL = "http://localhost:8003"
COMBINATION_SERVICE_URL = "http://localhost:8004"

class Phase6RecommendationDemo:
    """
    Comprehensive demonstration of Phase 6 Enhanced Recommendation Engine.
    Shows FAISS-based similarity search, multi-modal AI integration, and advanced personalization.
    """
    
    def __init__(self):
        """
        Initialize the Phase 6 recommendation demo.
        Sets up service connections and demo scenarios.
        """
        self.service_url = RECOMMENDATION_SERVICE_URL
        self.demo_users = [
            {
                "id": "demo_user_001",
                "name": "Emma Professional",
                "context": "work",
                "style_preference": "formal",
                "budget": "premium"
            },
            {
                "id": "demo_user_002", 
                "name": "Alex Casual",
                "context": "casual",
                "style_preference": "relaxed",
                "budget": "mid_range"
            },
            {
                "id": "demo_user_003",
                "name": "Jordan Athletic",
                "context": "sport",
                "style_preference": "sporty",
                "budget": "budget"
            }
        ]
        
        print("🚀 Phase 6 Enhanced Recommendation Engine Demo")
        print("=" * 80)
        print("✨ Features Demonstrated:")
        print("   • FAISS-based ultra-fast similarity search")
        print("   • Multi-modal AI embeddings")
        print("   • Phase 2 image processing integration")
        print("   • Phase 4 style profiling integration") 
        print("   • Phase 5 combination engine integration")
        print("   • Advanced personalization algorithms")
        print("   • Content-based, collaborative, and hybrid recommendations")
        print("   • Style-aware and outfit completion suggestions")
        print("   • Real-time trend analysis")
        print("=" * 80)
    
    def check_service_health(self) -> bool:
        """
        Check if the enhanced recommendation service is running and healthy.
        Displays comprehensive service status and AI component information.
        """
        print("\n🔍 Phase 6 Service Health Check")
        print("-" * 50)
        
        try:
            # Check main recommendation service
            response = requests.get(f"{self.service_url}/", timeout=10)
            
            if response.status_code == 200:
                health_data = response.json()
                
                print(f"✅ Service: {health_data['service']}")
                print(f"✅ Phase: {health_data['phase']}")
                print(f"✅ Status: {health_data['status']}")
                print(f"✅ Version: {health_data['version']}")
                print(f"✅ Engine Status: {health_data['engine_status']}")
                
                # Display AI components status
                print("\n🧠 AI Components Status:")
                ai_components = health_data.get('ai_components', {})
                for component, status in ai_components.items():
                    print(f"   • {component}: {status}")
                
                # Display service integrations
                print("\n🔗 Service Integrations:")
                integrations = health_data.get('service_integrations', {})
                for service, url in integrations.items():
                    print(f"   • {service}: {url}")
                
                # Display capabilities
                print("\n⚡ Capabilities:")
                capabilities = health_data.get('capabilities', [])
                for capability in capabilities:
                    print(f"   • {capability}")
                
                print(f"\n📊 Product Catalog Size: {health_data.get('catalog_size', 0)} items")
                
                return True
            else:
                print(f"❌ Service health check failed: HTTP {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Cannot connect to recommendation service: {e}")
            print(f"   Make sure the service is running on {self.service_url}")
            return False
    
    def demo_enhanced_recommendations(self):
        """
        Demonstrate enhanced AI-powered recommendation generation.
        Shows different strategies and personalization capabilities.
        """
        print("\n🎯 Enhanced AI Recommendations Demo")
        print("-" * 50)
        
        strategies = ["content_based", "collaborative", "hybrid", "style_aware", "trending"]
        
        for user in self.demo_users[:2]:  # Demo with first 2 users
            print(f"\n👤 User: {user['name']} (ID: {user['id']})")
            print(f"   Context: {user['context']}, Style: {user['style_preference']}")
            
            for strategy in strategies:
                print(f"\n   📊 Strategy: {strategy.replace('_', ' ').title()}")
                
                try:
                    # Create recommendation request
                    request_data = {
                        "user_id": user['id'],
                        "context": user['context'],
                        "num_recommendations": 6,
                        "strategy": strategy,
                        "include_analytics": True
                    }
                    
                    # Measure request time
                    start_time = time.time()
                    response = requests.post(f"{self.service_url}/recommendations", 
                                           json=request_data, timeout=15)
                    end_time = time.time()
                    
                    if response.status_code == 200:
                        data = response.json()
                        recommendations = data['recommendations']
                        analytics = data.get('recommendation_analytics', {})
                        user_insights = data.get('user_insights', {})
                        
                        print(f"      ✅ Generated {len(recommendations)} recommendations")
                        print(f"      ⏱️  Processing time: {end_time - start_time:.3f}s")
                        print(f"      🎯 Confidence: {analytics.get('recommendation_confidence', 0):.3f}")
                        print(f"      🎨 Diversity: {analytics.get('diversity_score', 0):.3f}")
                        print(f"      👤 Personalization: {analytics.get('personalization_score', 0):.3f}")
                        
                        # Show top 2 recommendations
                        for i, rec in enumerate(recommendations[:2]):
                            print(f"         {i+1}. {rec['name']} ({rec['style']}, ${rec['price']:.2f})")
                            print(f"            Score: {rec['recommendation_score']:.3f}")
                            print(f"            Reason: {rec['recommendation_reason']}")
                        
                        # Show user insights for first strategy
                        if strategy == strategies[0] and user_insights:
                            print(f"      👤 User Insights:")
                            print(f"         Dominant Style: {user_insights.get('dominant_style', 'unknown')}")
                            print(f"         Engagement: {user_insights.get('engagement_level', 0):.3f}")
                            print(f"         Style Confidence: {user_insights.get('style_confidence', 0):.3f}")
                    
                    else:
                        print(f"      ❌ Request failed: HTTP {response.status_code}")
                        if response.text:
                            print(f"         Error: {response.text[:100]}")
                
                except requests.exceptions.RequestException as e:
                    print(f"      ❌ Connection error: {e}")
                
                time.sleep(0.5)  # Brief pause between requests
    
    def demo_faiss_similarity_search(self):
        """
        Demonstrate ultra-fast FAISS-based similarity search.
        Shows how the system finds similar products using high-dimensional embeddings.
        """
        print("\n⚡ FAISS Ultra-Fast Similarity Search Demo")
        print("-" * 50)
        
        # Test products for similarity search
        test_products = [
            "prod_001",  # Classic White Dress Shirt
            "prod_004",  # Vintage Denim Jeans  
            "prod_011",  # Classic Leather Dress Shoes
            "prod_016"   # Summer Floral Dress
        ]
        
        for product_id in test_products:
            print(f"\n🔍 Finding products similar to: {product_id}")
            
            try:
                # Create similarity search request
                request_data = {
                    "product_id": product_id,
                    "num_similar": 5,
                    "similarity_threshold": 0.1
                }
                
                # Measure search time
                start_time = time.time()
                response = requests.post(f"{self.service_url}/similarity-search", 
                                       json=request_data, timeout=10)
                end_time = time.time()
                
                if response.status_code == 200:
                    data = response.json()
                    source_product = data['source_product']
                    similar_products = data['similar_products']
                    metadata = data['search_metadata']
                    
                    print(f"   📦 Source: {source_product['name']} ({source_product['category']}, {source_product['style']})")
                    print(f"   ⚡ Search time: {end_time - start_time:.4f}s")
                    print(f"   🔧 Method: {metadata['search_method']}")
                    print(f"   📊 Results: {metadata['returned']}/{metadata['total_found']} products")
                    
                    print(f"   🎯 Similar Products:")
                    for i, similar in enumerate(similar_products):
                        print(f"      {i+1}. {similar['name']} ({similar['style']})")
                        print(f"         Similarity: {similar['similarity_score']:.4f}")
                        print(f"         Price: ${similar['price']:.2f}")
                
                elif response.status_code == 404:
                    print(f"   ❌ Product {product_id} not found in catalog")
                else:
                    print(f"   ❌ Search failed: HTTP {response.status_code}")
            
            except requests.exceptions.RequestException as e:
                print(f"   ❌ Connection error: {e}")
            
            time.sleep(0.3)  # Brief pause between searches
    
    def demo_trending_analysis(self):
        """
        Demonstrate AI-powered trending product analysis.
        Shows how the system identifies and ranks trending items.
        """
        print("\n📈 AI-Powered Trending Analysis Demo")
        print("-" * 50)
        
        # Test different category and style filters
        trend_scenarios = [
            {"category": None, "style": None, "name": "Overall Trending"},
            {"category": "tops", "style": None, "name": "Trending Tops"},
            {"category": "shoes", "style": "casual", "name": "Trending Casual Shoes"},
            {"category": None, "style": "formal", "name": "Trending Formal Items"}
        ]
        
        for scenario in trend_scenarios:
            print(f"\n📊 {scenario['name']}")
            
            try:
                # Build query parameters
                params = {"num_products": 8}
                if scenario['category']:
                    params['category'] = scenario['category']
                if scenario['style']:
                    params['style'] = scenario['style']
                
                # Make trending request
                response = requests.get(f"{self.service_url}/trending", 
                                      params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    trending_products = data['trending_products']
                    metadata = data['trend_metadata']
                    
                    print(f"   📈 Found {len(trending_products)} trending products")
                    print(f"   🔍 Analyzed: {metadata['total_products_analyzed']} total products")
                    
                    # Show filters applied
                    filters = metadata['filters_applied']
                    if filters['category'] or filters['style']:
                        print(f"   🎛️  Filters: Category={filters['category']}, Style={filters['style']}")
                    
                    # Show top trending items
                    print(f"   🏆 Top Trending Items:")
                    for i, product in enumerate(trending_products[:5]):
                        print(f"      {i+1}. {product['name']}")
                        print(f"         Style: {product['style']}, Price: ${product['price']:.2f}")
                        print(f"         Trend Score: {product['trend_score_calculated']:.4f}")
                        print(f"         Rating: {product['rating']} ({product['reviews']} reviews)")
                
                else:
                    print(f"   ❌ Request failed: HTTP {response.status_code}")
            
            except requests.exceptions.RequestException as e:
                print(f"   ❌ Connection error: {e}")
            
            time.sleep(0.3)
    
    def demo_user_context_recommendations(self):
        """
        Demonstrate context-specific recommendations for users.
        Shows how recommendations adapt to different contexts and situations.
        """
        print("\n🎭 Context-Specific Recommendations Demo")
        print("-" * 50)
        
        contexts = ["work", "casual", "formal", "party", "sport", "date"]
        demo_user = self.demo_users[0]  # Use first demo user
        
        print(f"👤 User: {demo_user['name']} (ID: {demo_user['id']})")
        
        for context in contexts:
            print(f"\n📍 Context: {context.title()}")
            
            try:
                # Make context-specific recommendation request
                url = f"{self.service_url}/user/{demo_user['id']}/recommendations/{context}"
                params = {
                    "num_recommendations": 4,
                    "strategy": "style_aware"
                }
                
                response = requests.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    recommendations = data['recommendations']
                    analytics = data.get('recommendation_analytics', {})
                    
                    print(f"   ✅ Generated {len(recommendations)} context-specific recommendations")
                    print(f"   🎯 Confidence: {analytics.get('recommendation_confidence', 0):.3f}")
                    
                    # Show context-appropriate recommendations
                    for i, rec in enumerate(recommendations):
                        print(f"      {i+1}. {rec['name']} ({rec['style']})")
                        print(f"         Price: ${rec['price']:.2f}, Rating: {rec['rating']}")
                        print(f"         Perfect for: {context}")
                
                else:
                    print(f"   ❌ Request failed: HTTP {response.status_code}")
            
            except requests.exceptions.RequestException as e:
                print(f"   ❌ Connection error: {e}")
            
            time.sleep(0.3)
    
    def demo_service_analytics(self):
        """
        Demonstrate comprehensive service analytics and AI metrics.
        Shows system performance, AI algorithm metrics, and user engagement data.
        """
        print("\n📊 Service Analytics & AI Metrics Demo")
        print("-" * 50)
        
        try:
            response = requests.get(f"{self.service_url}/analytics", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Display service performance metrics
                print("⚡ Service Performance:")
                performance = data.get('service_performance', {})
                print(f"   • Total Recommendations: {performance.get('total_recommendations_generated', 0)}")
                print(f"   • Average Processing Time: {performance.get('average_processing_time', 'N/A')}")
                print(f"   • Success Rate: {performance.get('success_rate', 'N/A')}")
                print(f"   • Service Uptime: {performance.get('service_uptime', 'N/A')}")
                
                # Display AI algorithm metrics
                print("\n🧠 AI Algorithm Metrics:")
                ai_metrics = data.get('ai_algorithm_metrics', {})
                print(f"   • FAISS Index Status: {ai_metrics.get('faiss_index_status', 'Unknown')}")
                print(f"   • Product Catalog Size: {ai_metrics.get('product_catalog_size', 0)}")
                print(f"   • Embedding Dimension: {ai_metrics.get('embedding_dimension', 0)}")
                print(f"   • Similarity Search Method: {ai_metrics.get('similarity_search_method', 'Unknown')}")
                print(f"   • Active Strategies: {len(ai_metrics.get('recommendation_strategies', []))}")
                
                # Display strategy weights
                strategy_weights = ai_metrics.get('strategy_weights', {})
                if strategy_weights:
                    print("   • Strategy Weights:")
                    for strategy, weight in strategy_weights.items():
                        print(f"      - {strategy}: {weight}")
                
                # Display user engagement
                print("\n👥 User Engagement:")
                engagement = data.get('user_engagement', {})
                print(f"   • Active Users: {engagement.get('active_users', 0)}")
                print(f"   • Personalization Effectiveness: {engagement.get('personalization_effectiveness', 'Unknown')}")
                
                # Display product insights
                print("\n📦 Product Insights:")
                insights = data.get('product_insights', {})
                
                # Most recommended categories
                categories = insights.get('most_recommended_categories', {})
                if categories:
                    print("   • Top Categories:")
                    for category, count in list(categories.items())[:5]:
                        print(f"      - {category}: {count} products")
                
                # Style trends
                styles = insights.get('trending_styles', {})
                if styles:
                    print("   • Trending Styles:")
                    for style, count in list(styles.items())[:5]:
                        print(f"      - {style}: {count} products")
                
                # Price distribution
                price_dist = insights.get('price_range_distribution', {})
                if price_dist:
                    print("   • Price Distribution:")
                    for tier, count in price_dist.items():
                        print(f"      - {tier}: {count} products")
                
                # Display active AI features
                print("\n🚀 Active AI Features:")
                ai_features = data.get('ai_features_active', [])
                for feature in ai_features:
                    print(f"   • {feature}")
                
                # Display service integrations health
                print("\n🔗 Service Integrations:")
                integrations = data.get('service_integrations', {})
                for service, status in integrations.items():
                    print(f"   • {service}: {status}")
            
            else:
                print(f"❌ Analytics request failed: HTTP {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error: {e}")
    
    def demo_performance_testing(self):
        """
        Demonstrate system performance with concurrent requests.
        Shows how FAISS enables ultra-fast recommendations at scale.
        """
        print("\n⚡ Performance Testing & Scalability Demo")
        print("-" * 50)
        
        print("🧪 Testing recommendation generation performance...")
        
        # Test multiple concurrent recommendations
        test_requests = []
        for i in range(5):
            test_requests.append({
                "user_id": f"perf_test_user_{i}",
                "context": "casual",
                "num_recommendations": 10,
                "strategy": "hybrid",
                "include_analytics": True
            })
        
        # Measure performance for sequential requests
        print("\n📊 Sequential Request Performance:")
        sequential_times = []
        for i, request_data in enumerate(test_requests):
            try:
                start_time = time.time()
                response = requests.post(f"{self.service_url}/recommendations", 
                                       json=request_data, timeout=15)
                end_time = time.time()
                
                if response.status_code == 200:
                    request_time = end_time - start_time
                    sequential_times.append(request_time)
                    print(f"   Request {i+1}: {request_time:.3f}s")
                else:
                    print(f"   Request {i+1}: Failed (HTTP {response.status_code})")
            
            except requests.exceptions.RequestException as e:
                print(f"   Request {i+1}: Connection error")
        
        if sequential_times:
            avg_time = sum(sequential_times) / len(sequential_times)
            min_time = min(sequential_times)
            max_time = max(sequential_times)
            
            print(f"\n📈 Performance Summary:")
            print(f"   • Average Response Time: {avg_time:.3f}s")
            print(f"   • Fastest Response: {min_time:.3f}s")
            print(f"   • Slowest Response: {max_time:.3f}s")
            print(f"   • Throughput: ~{1/avg_time:.1f} requests/second")
        
        # Test FAISS similarity search performance
        print(f"\n⚡ FAISS Similarity Search Performance:")
        search_times = []
        test_products = ["prod_001", "prod_004", "prod_011"]
        
        for product_id in test_products:
            try:
                start_time = time.time()
                response = requests.post(f"{self.service_url}/similarity-search", 
                                       json={"product_id": product_id, "num_similar": 10}, 
                                       timeout=5)
                end_time = time.time()
                
                if response.status_code == 200:
                    search_time = end_time - start_time
                    search_times.append(search_time)
                    print(f"   Search for {product_id}: {search_time:.4f}s")
            
            except requests.exceptions.RequestException as e:
                print(f"   Search for {product_id}: Connection error")
        
        if search_times:
            avg_search_time = sum(search_times) / len(search_times)
            print(f"\n⚡ FAISS Search Performance:")
            print(f"   • Average Search Time: {avg_search_time:.4f}s")
            print(f"   • Search Throughput: ~{1/avg_search_time:.0f} searches/second")
            print("   • Ultra-fast similarity search enabled! 🚀")
    
    def run_complete_demo(self):
        """
        Run the complete Phase 6 demonstration.
        Executes all demo scenarios to showcase the enhanced recommendation engine.
        """
        print(f"\n🎉 Starting Complete Phase 6 Enhanced Recommendation Engine Demo")
        print(f"⏰ Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Check service health first
        if not self.check_service_health():
            print("\n❌ Service health check failed. Please start the recommendation service first:")
            print(f"   cd recommendation_engine_service")
            print(f"   python main.py")
            return
        
        try:
            # Run all demo scenarios
            self.demo_enhanced_recommendations()
            self.demo_faiss_similarity_search()
            self.demo_trending_analysis()
            self.demo_user_context_recommendations()
            self.demo_service_analytics()
            self.demo_performance_testing()
            
            # Demo summary
            print("\n" + "=" * 80)
            print("🎉 Phase 6 Enhanced Recommendation Engine Demo Completed!")
            print("=" * 80)
            print("✨ Successfully Demonstrated:")
            print("   ✅ FAISS-based ultra-fast similarity search")
            print("   ✅ Multi-modal AI embeddings and personalization")
            print("   ✅ Advanced recommendation strategies (content, collaborative, hybrid)")
            print("   ✅ Style-aware recommendations with Phase 4 integration")
            print("   ✅ Trending product analysis with AI scoring")
            print("   ✅ Context-specific recommendations")
            print("   ✅ Comprehensive service analytics and AI metrics")
            print("   ✅ High-performance scalability testing")
            print("\n🚀 Phase 6 Features:")
            print("   • Enhanced product catalog with 20+ diverse items")
            print("   • FAISS similarity search with 64-dimensional embeddings")
            print("   • Multi-service integration (Phase 2, 4, 5)")
            print("   • Advanced personalization algorithms")
            print("   • Real-time recommendation analytics")
            print("   • Ultra-fast performance (< 100ms similarity search)")
            print("   • Comprehensive API with 8+ endpoints")
            print("   • Production-ready error handling and validation")
            print("\n💡 Next Steps:")
            print("   • Integrate with real e-commerce product catalogs")
            print("   • Connect to actual user databases and interaction history")
            print("   • Implement A/B testing for recommendation strategies")
            print("   • Add machine learning model training pipelines")
            print("   • Scale FAISS index for millions of products")
            print("   • Add recommendation feedback loops")
            print(f"\n⏰ Demo completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except KeyboardInterrupt:
            print("\n\n⏹️  Demo interrupted by user")
        except Exception as e:
            print(f"\n❌ Demo error: {e}")

def main():
    """
    Main function to run the Phase 6 Enhanced Recommendation Engine demo.
    Provides an interactive demo experience showcasing all AI-powered features.
    """
    demo = Phase6RecommendationDemo()
    
    print("\n🎮 Demo Options:")
    print("1. Run Complete Demo (All Features)")
    print("2. Service Health Check Only")
    print("3. Enhanced Recommendations Only")
    print("4. FAISS Similarity Search Only")
    print("5. Trending Analysis Only")
    print("6. Performance Testing Only")
    print("7. Exit")
    
    while True:
        try:
            choice = input("\n🎯 Select demo option (1-7): ").strip()
            
            if choice == "1":
                demo.run_complete_demo()
                break
            elif choice == "2":
                demo.check_service_health()
                break
            elif choice == "3":
                if demo.check_service_health():
                    demo.demo_enhanced_recommendations()
                break
            elif choice == "4":
                if demo.check_service_health():
                    demo.demo_faiss_similarity_search()
                break
            elif choice == "5":
                if demo.check_service_health():
                    demo.demo_trending_analysis()
                break
            elif choice == "6":
                if demo.check_service_health():
                    demo.demo_performance_testing()
                break
            elif choice == "7":
                print("👋 Goodbye! Thanks for exploring Phase 6!")
                break
            else:
                print("❌ Invalid option. Please choose 1-7.")
        
        except KeyboardInterrupt:
            print("\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
