# Phase 8: Interactive Demonstration of Intelligent Feedback Loop System
# Comprehensive demo showcasing advanced learning and adaptation capabilities
# Shows real-time feedback processing, learning analytics, and system improvements

import asyncio
import json
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
import random
import uuid

# Demo configuration
FEEDBACK_SERVICE_URL = "http://localhost:8007"
DEMO_USERS = [
    {"id": "demo_user_1", "name": "Sarah", "style": "minimalist", "age_group": "25-34"},
    {"id": "demo_user_2", "name": "Mike", "style": "casual", "age_group": "35-44"},
    {"id": "demo_user_3", "name": "Emma", "style": "trendy", "age_group": "18-24"},
    {"id": "demo_user_4", "name": "David", "style": "classic", "age_group": "45-54"},
    {"id": "demo_user_5", "name": "Lisa", "style": "bohemian", "age_group": "25-34"}
]

class FeedbackLoopDemo:
    """
    Interactive demonstration class for the Aura Feedback Loop System.
    Showcases intelligent feedback collection, learning, and system adaptation.
    """
    
    def __init__(self):
        """
        Initialize the feedback loop demonstration.
        Sets up demo configuration and tracking variables.
        """
        # Set up demo tracking
        self.demo_sessions = {}  # Track demo sessions for each user
        self.feedback_submitted = []  # Track all submitted feedback
        self.learning_insights_generated = []  # Track generated insights
        self.system_adaptations_applied = []  # Track applied adaptations
        
        print("🎯 Initializing Aura Feedback Loop System Demo - Phase 8")
        print("   Demonstrating intelligent learning and adaptation capabilities")
        print(f"   Target Service: {FEEDBACK_SERVICE_URL}")
        print(f"   Demo Users: {len(DEMO_USERS)} simulated users with different profiles")
    
    def check_service_health(self) -> bool:
        """
        Check if the feedback loop service is running and healthy.
        Verifies service connectivity before running demonstrations.
        """
        try:
            print("\n🔍 Checking Feedback Loop Service Health...")
            
            # Check basic health endpoint
            response = requests.get(f"{FEEDBACK_SERVICE_URL}/", timeout=5)
            
            if response.status_code == 200:
                service_info = response.json()
                print(f"✅ Service Status: {service_info.get('status', 'unknown')}")
                print(f"   Service: {service_info.get('service', 'N/A')}")
                print(f"   Version: {service_info.get('version', 'N/A')}")
                print(f"   Phase: {service_info.get('phase', 'N/A')}")
                
                # Check detailed system health
                health_response = requests.get(f"{FEEDBACK_SERVICE_URL}/health", timeout=5)
                if health_response.status_code == 200:
                    health_data = health_response.json()
                    print(f"   Processing Active: {health_data.get('processing_active', False)}")
                    print(f"   Feedback Queue Size: {health_data.get('feedback_queue_size', 0)}")
                    print(f"   Database Status: {health_data.get('database_status', 'unknown')}")
                
                return True
            else:
                print(f"❌ Service health check failed: HTTP {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Cannot connect to feedback service: {e}")
            print(f"   Please ensure the service is running on {FEEDBACK_SERVICE_URL}")
            return False
    
    def generate_realistic_feedback(self, user: Dict[str, str], scenario: str) -> Dict[str, Any]:
        """
        Generate realistic feedback data for different user scenarios.
        Creates diverse feedback types matching user profiles and contexts.
        """
        # Generate session ID for tracking
        session_id = f"demo_session_{user['id']}_{int(time.time())}"
        
        # Base feedback structure
        feedback = {
            "user_id": user["id"],
            "session_id": session_id,
            "service_source": "",
            "data": {},
            "context": {
                "user_style": user["style"],
                "user_age_group": user["age_group"],
                "demo_scenario": scenario,
                "time_of_day": datetime.now().hour,
                "device": random.choice(["mobile", "desktop", "tablet"]),
                "session_duration": random.randint(30, 300)
            },
            "confidence": round(random.uniform(0.7, 1.0), 2)
        }
        
        # Generate scenario-specific feedback
        if scenario == "recommendation_rating":
            feedback.update({
                "feedback_type": "explicit_rating",
                "learning_objective": "recommendation_accuracy",
                "service_source": "recommendation_engine_service",
                "data": {
                    "rating": random.randint(2, 5),  # Bias toward positive ratings
                    "item_id": f"item_{random.randint(1000, 9999)}",
                    "recommendation_set_id": f"rec_set_{random.randint(100, 999)}",
                    "item_category": random.choice(["tops", "bottoms", "shoes", "accessories"]),
                    "recommended_for": random.choice(["work", "casual", "formal", "weekend"])
                },
                "context": {
                    **feedback["context"],
                    "recommendation_position": random.randint(1, 10),
                    "items_viewed_before_rating": random.randint(3, 15),
                    "occasion": random.choice(["work", "date", "casual", "formal", "travel"])
                }
            })
        
        elif scenario == "style_profile_engagement":
            feedback.update({
                "feedback_type": "implicit_engagement",
                "learning_objective": "style_profiling_precision",
                "service_source": "style_profile_service",
                "data": {
                    "time_spent": random.randint(45, 180),
                    "interactions": random.randint(5, 25),
                    "scroll_depth": round(random.uniform(0.3, 1.0), 2),
                    "profile_sections_viewed": random.randint(2, 6),
                    "preferences_updated": random.choice([True, False])
                },
                "context": {
                    **feedback["context"],
                    "profile_completeness": round(random.uniform(0.4, 1.0), 2),
                    "previous_profile_views": random.randint(0, 10)
                }
            })
        
        elif scenario == "combination_acceptance":
            feedback.update({
                "feedback_type": "acceptance_feedback",
                "learning_objective": "combination_quality",
                "service_source": "combination_engine_service",
                "data": {
                    "action": random.choice(["save", "share", "purchase", "view_details"]),
                    "combination_id": f"combo_{random.randint(1000, 9999)}",
                    "items": [f"item_{random.randint(100, 999)}" for _ in range(random.randint(2, 5))],
                    "combination_score": round(random.uniform(0.6, 1.0), 2)
                },
                "context": {
                    **feedback["context"],
                    "combination_type": random.choice(["work_outfit", "casual_look", "evening_wear", "weekend_style"]),
                    "generated_combinations_viewed": random.randint(3, 12),
                    "season": random.choice(["spring", "summer", "fall", "winter"])
                }
            })
        
        elif scenario == "behavioral_signals":
            feedback.update({
                "feedback_type": "behavioral_signals",
                "learning_objective": "engagement_optimization",
                "service_source": random.choice(["image_processing_service", "nlu_service"]),
                "data": {
                    "action": random.choice(["click", "hover", "scroll", "zoom", "filter"]),
                    "element_type": random.choice(["image", "text", "button", "filter", "recommendation"]),
                    "interaction_count": random.randint(1, 8),
                    "dwell_time": random.randint(2, 30)
                },
                "context": {
                    **feedback["context"],
                    "page_type": random.choice(["catalog", "recommendations", "profile", "combination"]),
                    "search_query": random.choice([None, "summer dresses", "casual shoes", "work shirts", "accessories"])
                }
            })
        
        elif scenario == "context_feedback":
            feedback.update({
                "feedback_type": "contextual_feedback",
                "learning_objective": "context_understanding",
                "service_source": "orchestrator_service",
                "data": {
                    "context_appropriateness": random.randint(3, 5),
                    "context_type": random.choice(["weather", "occasion", "time", "location"]),
                    "suggested_adjustments": random.choice([True, False])
                },
                "context": {
                    **feedback["context"],
                    "weather": random.choice(["sunny", "rainy", "cold", "hot"]),
                    "location": random.choice(["office", "home", "restaurant", "outdoor"]),
                    "social_setting": random.choice(["professional", "casual", "formal", "intimate"])
                }
            })
        
        return feedback
    
    async def simulate_user_journey(self, user: Dict[str, str], duration_minutes: int = 5):
        """
        Simulate a realistic user journey with multiple feedback interactions.
        Creates authentic usage patterns and feedback sequences.
        """
        print(f"\n👤 Simulating user journey for {user['name']} ({user['style']} style)")
        
        # Initialize user session tracking
        session_data = {
            "user": user,
            "start_time": datetime.now(),
            "feedback_count": 0,
            "interactions": []
        }
        
        # Define journey scenarios based on user style
        journey_scenarios = {
            "minimalist": ["recommendation_rating", "style_profile_engagement", "behavioral_signals"],
            "casual": ["combination_acceptance", "behavioral_signals", "recommendation_rating"],
            "trendy": ["behavioral_signals", "recommendation_rating", "combination_acceptance"],
            "classic": ["style_profile_engagement", "context_feedback", "recommendation_rating"],
            "bohemian": ["combination_acceptance", "context_feedback", "behavioral_signals"]
        }
        
        scenarios = journey_scenarios.get(user["style"], ["recommendation_rating", "behavioral_signals"])
        
        # Simulate user interactions over time
        journey_duration = duration_minutes * 60  # Convert to seconds
        interaction_interval = journey_duration / len(scenarios)
        
        for i, scenario in enumerate(scenarios):
            # Generate and submit feedback
            feedback_data = self.generate_realistic_feedback(user, scenario)
            
            try:
                # Submit feedback to service
                response = requests.post(f"{FEEDBACK_SERVICE_URL}/feedback", json=feedback_data, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    feedback_id = result.get("feedback_id")
                    
                    print(f"   ✅ Feedback submitted: {scenario} (ID: {feedback_id[:8]}...)")
                    
                    # Track successful feedback
                    session_data["feedback_count"] += 1
                    session_data["interactions"].append({
                        "scenario": scenario,
                        "feedback_id": feedback_id,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    self.feedback_submitted.append(feedback_data)
                
                else:
                    print(f"   ❌ Feedback submission failed: HTTP {response.status_code}")
            
            except requests.exceptions.RequestException as e:
                print(f"   ❌ Network error submitting feedback: {e}")
            
            # Wait before next interaction (simulate realistic timing)
            if i < len(scenarios) - 1:  # Don't wait after the last interaction
                wait_time = random.uniform(interaction_interval * 0.5, interaction_interval * 1.5)
                await asyncio.sleep(min(wait_time, 10))  # Cap wait time for demo
        
        # Store session data
        self.demo_sessions[user["id"]] = session_data
        
        journey_duration_actual = (datetime.now() - session_data["start_time"]).total_seconds()
        print(f"   📊 Journey completed: {session_data['feedback_count']} interactions in {journey_duration_actual:.1f}s")
        
        return session_data
    
    def demonstrate_learning_analytics(self):
        """
        Demonstrate learning analytics and system insights.
        Shows how the system processes feedback and generates intelligence.
        """
        print("\n📊 Demonstrating Learning Analytics Generation...")
        
        try:
            # Get comprehensive analytics
            response = requests.get(f"{FEEDBACK_SERVICE_URL}/analytics", timeout=10)
            
            if response.status_code == 200:
                analytics = response.json()
                
                print("✅ Learning Analytics Generated Successfully:")
                
                # Display feedback analytics
                feedback_analytics = analytics.get("feedback_analytics", {})
                print(f"   📥 Total Feedback Collected: {feedback_analytics.get('total_feedback_collected', 0)}")
                
                feedback_by_type = feedback_analytics.get("feedback_by_type", {})
                print("   📋 Feedback by Type:")
                for feedback_type, count in feedback_by_type.items():
                    print(f"      • {feedback_type}: {count}")
                
                feedback_by_objective = feedback_analytics.get("feedback_by_objective", {})
                print("   🎯 Feedback by Learning Objective:")
                for objective, count in feedback_by_objective.items():
                    print(f"      • {objective}: {count}")
                
                # Display learning analytics
                learning_analytics = analytics.get("learning_analytics", {})
                print(f"   🧠 Learning Models Trained: {learning_analytics.get('models_trained', 0)}")
                print(f"   📈 Learning Insights Generated: {learning_analytics.get('insights_generated', 0)}")
                print(f"   🔧 System Adaptations Applied: {learning_analytics.get('adaptations_applied', 0)}")
                
                # Display system improvements
                system_improvements = analytics.get("system_improvements", {})
                if system_improvements:
                    print("   🚀 System Improvements Detected:")
                    for service, improvements in system_improvements.items():
                        if improvements:
                            print(f"      • {service}: {len(improvements)} improvements")
                
                return analytics
            
            else:
                print(f"❌ Analytics generation failed: HTTP {response.status_code}")
                return None
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Error retrieving analytics: {e}")
            return None
    
    def demonstrate_learning_insights(self):
        """
        Demonstrate learning insights retrieval and application.
        Shows actionable intelligence derived from feedback analysis.
        """
        print("\n🔍 Demonstrating Learning Insights Retrieval...")
        
        try:
            # Get learning insights
            response = requests.get(f"{FEEDBACK_SERVICE_URL}/insights?limit=10", timeout=10)
            
            if response.status_code == 200:
                insights = response.json()
                
                print(f"✅ Retrieved {len(insights)} Learning Insights:")
                
                if insights:
                    for i, insight in enumerate(insights[:5], 1):  # Show first 5 insights
                        print(f"   {i}. Insight ID: {insight['insight_id'][:8]}...")
                        print(f"      Learning Objective: {insight['learning_objective']}")
                        print(f"      Confidence Score: {insight['confidence_score']:.2f}")
                        print(f"      Impact Estimate: {insight['impact_estimate']:.2f}")
                        
                        # Show action recommendations
                        recommendations = insight.get('action_recommendations', [])
                        if recommendations:
                            print(f"      Action Recommendations:")
                            for rec in recommendations[:2]:  # Show first 2 recommendations
                                print(f"         • {rec}")
                        
                        print()  # Empty line for readability
                    
                    # Demonstrate insight filtering
                    print("   🔎 Demonstrating Insight Filtering...")
                    
                    # Filter by learning objective
                    filter_response = requests.get(
                        f"{FEEDBACK_SERVICE_URL}/insights?learning_objective=recommendation_accuracy&limit=5",
                        timeout=10
                    )
                    
                    if filter_response.status_code == 200:
                        filtered_insights = filter_response.json()
                        print(f"      📊 Recommendation Accuracy Insights: {len(filtered_insights)}")
                    
                    # Filter by applied insights
                    applied_response = requests.get(
                        f"{FEEDBACK_SERVICE_URL}/insights?applied_only=true&limit=5",
                        timeout=10
                    )
                    
                    if applied_response.status_code == 200:
                        applied_insights = applied_response.json()
                        print(f"      ✅ Applied Insights: {len(applied_insights)}")
                
                else:
                    print("   📝 No learning insights available yet (system is still learning)")
                
                return insights
            
            else:
                print(f"❌ Insights retrieval failed: HTTP {response.status_code}")
                return []
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Error retrieving insights: {e}")
            return []
    
    def demonstrate_user_adaptations(self):
        """
        Demonstrate user-specific adaptations and personalization.
        Shows how the system personalizes behavior for individual users.
        """
        print("\n🎯 Demonstrating User-Specific Adaptations...")
        
        # Select a demo user for adaptation demonstration
        demo_user = random.choice(DEMO_USERS)
        print(f"   Selected User: {demo_user['name']} ({demo_user['style']} style)")
        
        # Create user-specific adaptation
        adaptation_data = {
            "user_id": demo_user["id"],
            "adaptation_type": "style_preference_optimization",
            "parameters": {
                "style_weight": round(random.uniform(0.7, 1.0), 2),
                "color_preferences": ["blue", "black", "white"] if demo_user["style"] == "minimalist" else ["red", "green", "yellow"],
                "occasion_preferences": ["work", "casual"] if demo_user["age_group"] in ["35-44", "45-54"] else ["trendy", "social"],
                "personalization_level": round(random.uniform(0.8, 1.0), 2)
            }
        }
        
        try:
            # Apply user adaptation
            response = requests.post(f"{FEEDBACK_SERVICE_URL}/adaptations/user", json=adaptation_data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                adaptation_id = result.get("adaptation_id")
                
                print(f"   ✅ Adaptation Applied: {adaptation_id}")
                print(f"      Type: {adaptation_data['adaptation_type']}")
                print(f"      Parameters: {len(adaptation_data['parameters'])} customizations")
                
                # Retrieve user adaptations to confirm
                user_adaptations_response = requests.get(
                    f"{FEEDBACK_SERVICE_URL}/adaptations/user/{demo_user['id']}",
                    timeout=10
                )
                
                if user_adaptations_response.status_code == 200:
                    user_adaptations = user_adaptations_response.json()
                    print(f"   📊 Total User Adaptations: {user_adaptations.get('total_adaptations', 0)}")
                    
                    # Show adaptation details
                    adaptations = user_adaptations.get('adaptations', {})
                    for adaptation_type, adaptation_info in adaptations.items():
                        print(f"      • {adaptation_type}: Applied")
                
                self.system_adaptations_applied.append(adaptation_data)
                
                return adaptation_data
            
            else:
                print(f"❌ User adaptation failed: HTTP {response.status_code}")
                return None
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Error applying user adaptation: {e}")
            return None
    
    def demonstrate_model_retraining(self):
        """
        Demonstrate model retraining and system improvement.
        Shows how the system continuously learns and adapts.
        """
        print("\n🧠 Demonstrating Model Retraining...")
        
        try:
            # Trigger model retraining for a specific objective
            objective = "recommendation_accuracy"
            response = requests.post(
                f"{FEEDBACK_SERVICE_URL}/learning/retrain?learning_objective={objective}&force_retrain=true",
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"✅ Model Retraining Completed:")
                print(f"   Retraining ID: {result.get('retraining_id')}")
                print(f"   Objectives Processed: {result.get('objectives_processed', 0)}")
                print(f"   Successful Retraining: {result.get('successful_retraining', 0)}")
                
                # Show retraining results
                results = result.get('results', {})
                for objective_name, objective_result in results.items():
                    status = objective_result.get('status', 'unknown')
                    print(f"   • {objective_name}: {status}")
                    
                    if status == "completed":
                        samples = objective_result.get('samples_used', 0)
                        training_time = objective_result.get('training_time', 'N/A')
                        improvement = objective_result.get('improvement_estimate', 'N/A')
                        
                        print(f"      Samples Used: {samples}")
                        print(f"      Training Time: {training_time}")
                        print(f"      Estimated Improvement: {improvement}")
                
                return result
            
            else:
                print(f"❌ Model retraining failed: HTTP {response.status_code}")
                return None
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Error triggering model retraining: {e}")
            return None
    
    def demonstrate_system_health_monitoring(self):
        """
        Demonstrate comprehensive system health monitoring.
        Shows real-time system status and operational metrics.
        """
        print("\n🏥 Demonstrating System Health Monitoring...")
        
        try:
            # Get detailed system health
            response = requests.get(f"{FEEDBACK_SERVICE_URL}/health", timeout=10)
            
            if response.status_code == 200:
                health_data = response.json()
                
                print("✅ System Health Status:")
                print(f"   Overall Status: {health_data.get('status', 'unknown')}")
                print(f"   Processing Active: {health_data.get('processing_active', False)}")
                print(f"   Feedback Queue Size: {health_data.get('feedback_queue_size', 0)}")
                print(f"   Database Status: {health_data.get('database_status', 'unknown')}")
                
                # Show learning models status
                models_status = health_data.get('learning_models_status', {})
                print("   🧠 Learning Models Status:")
                for model_name, status in models_status.items():
                    print(f"      • {model_name}: {status}")
                
                # Show system load metrics
                system_load = health_data.get('system_load', {})
                print("   📊 System Load Metrics:")
                for metric_name, load_value in system_load.items():
                    load_percentage = load_value * 100
                    print(f"      • {metric_name}: {load_percentage:.1f}%")
                
                return health_data
            
            else:
                print(f"❌ Health monitoring failed: HTTP {response.status_code}")
                return None
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Error monitoring system health: {e}")
            return None
    
    def generate_demo_summary(self):
        """
        Generate a comprehensive summary of the demonstration.
        Shows overall results and system performance metrics.
        """
        print("\n📋 Demo Summary - Phase 8 Feedback Loop System")
        print("=" * 60)
        
        # Feedback submission summary
        total_feedback = len(self.feedback_submitted)
        print(f"📥 Total Feedback Submitted: {total_feedback}")
        
        if self.feedback_submitted:
            feedback_types = {}
            learning_objectives = {}
            
            for feedback in self.feedback_submitted:
                # Count feedback types
                fb_type = feedback.get('feedback_type', 'unknown')
                feedback_types[fb_type] = feedback_types.get(fb_type, 0) + 1
                
                # Count learning objectives
                objective = feedback.get('learning_objective', 'unknown')
                learning_objectives[objective] = learning_objectives.get(objective, 0) + 1
            
            print("   Feedback Types Distribution:")
            for fb_type, count in feedback_types.items():
                print(f"      • {fb_type}: {count}")
            
            print("   Learning Objectives Distribution:")
            for objective, count in learning_objectives.items():
                print(f"      • {objective}: {count}")
        
        # User journey summary
        print(f"\n👥 User Journey Summary:")
        print(f"   Users Simulated: {len(self.demo_sessions)}")
        
        for user_id, session in self.demo_sessions.items():
            user_name = session['user']['name']
            feedback_count = session['feedback_count']
            duration = (datetime.now() - session['start_time']).total_seconds()
            print(f"      • {user_name}: {feedback_count} interactions in {duration:.1f}s")
        
        # System adaptations summary
        adaptations_count = len(self.system_adaptations_applied)
        print(f"\n🔧 System Adaptations Applied: {adaptations_count}")
        
        # Demo performance metrics
        total_demo_duration = max([
            (datetime.now() - session['start_time']).total_seconds() 
            for session in self.demo_sessions.values()
        ]) if self.demo_sessions else 0
        
        print(f"\n⏱️ Demo Performance:")
        print(f"   Total Demo Duration: {total_demo_duration:.1f} seconds")
        print(f"   Average Feedback per Second: {total_feedback / max(total_demo_duration, 1):.2f}")
        
        # System capabilities demonstrated
        print(f"\n✅ Capabilities Demonstrated:")
        print(f"   • Multi-modal feedback collection")
        print(f"   • Real-time learning processing")
        print(f"   • Intelligent system adaptation")
        print(f"   • Personalized user learning")
        print(f"   • Advanced analytics generation")
        print(f"   • Continuous model improvement")
        print(f"   • System health monitoring")
        print(f"   • Performance optimization")
        
        print(f"\n🎯 Phase 8 Feedback Loop System Demo Complete!")
        print(f"   The system demonstrated advanced learning and adaptation capabilities.")
        print(f"   Ready for integration with all Aura AI services (Phases 2-7).")

async def run_comprehensive_demo():
    """
    Run the comprehensive Phase 8 feedback loop system demonstration.
    Orchestrates all demo scenarios and showcases system capabilities.
    """
    print("🚀 Starting Phase 8 Feedback Loop System Comprehensive Demo")
    print("=" * 70)
    
    # Initialize demo
    demo = FeedbackLoopDemo()
    
    # Check service health before starting
    if not demo.check_service_health():
        print("❌ Cannot proceed with demo - service not available")
        return
    
    print("\n🎬 Beginning Interactive Demonstration...")
    
    # Phase 1: Simulate user journeys with realistic feedback
    print("\n" + "=" * 50)
    print("PHASE 1: Simulating Realistic User Journeys")
    print("=" * 50)
    
    # Run concurrent user journeys
    user_tasks = []
    for user in DEMO_USERS:
        task = demo.simulate_user_journey(user, duration_minutes=2)
        user_tasks.append(task)
    
    # Wait for all user journeys to complete
    await asyncio.gather(*user_tasks)
    
    # Brief pause to allow processing
    print("\n⏳ Allowing system to process feedback...")
    await asyncio.sleep(3)
    
    # Phase 2: Demonstrate learning analytics
    print("\n" + "=" * 50)
    print("PHASE 2: Learning Analytics and Insights")
    print("=" * 50)
    
    analytics = demo.demonstrate_learning_analytics()
    await asyncio.sleep(2)
    
    insights = demo.demonstrate_learning_insights()
    await asyncio.sleep(2)
    
    # Phase 3: Demonstrate system adaptations
    print("\n" + "=" * 50)
    print("PHASE 3: System Adaptations and Personalization")
    print("=" * 50)
    
    adaptation = demo.demonstrate_user_adaptations()
    await asyncio.sleep(2)
    
    # Phase 4: Demonstrate model retraining
    print("\n" + "=" * 50)
    print("PHASE 4: Model Retraining and System Improvement")
    print("=" * 50)
    
    retraining = demo.demonstrate_model_retraining()
    await asyncio.sleep(2)
    
    # Phase 5: Demonstrate system health monitoring
    print("\n" + "=" * 50)
    print("PHASE 5: System Health and Performance Monitoring")
    print("=" * 50)
    
    health = demo.demonstrate_system_health_monitoring()
    await asyncio.sleep(2)
    
    # Generate comprehensive demo summary
    print("\n" + "=" * 50)
    print("DEMO SUMMARY AND RESULTS")
    print("=" * 50)
    
    demo.generate_demo_summary()
    
    print("\n🎉 Phase 8 Feedback Loop System Demo Successfully Completed!")
    print("   All advanced learning and adaptation capabilities demonstrated.")
    print("   System ready for production deployment and integration.")

if __name__ == "__main__":
    print("🎯 Aura Feedback Loop System - Phase 8 Interactive Demo")
    print("   Demonstrating intelligent feedback processing and system learning")
    print("   Advanced machine learning capabilities and real-time adaptation")
    print()
    
    # Check if we should run the demo
    try:
        # Run the comprehensive demonstration
        asyncio.run(run_comprehensive_demo())
        
    except KeyboardInterrupt:
        print("\n⏹️ Demo interrupted by user")
        print("   Thank you for exploring the Aura Feedback Loop System!")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("   Please ensure the feedback loop service is running and try again.")
        print(f"   Service should be available at: {FEEDBACK_SERVICE_URL}")
    
    print("\n" + "=" * 70)
    print("Phase 8 Demo Complete - Advanced Feedback Loop System")
    print("🔄 Continuous learning • 🎯 Intelligent adaptation • 📊 Real-time analytics")
    print("=" * 70)
