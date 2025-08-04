#!/usr/bin/env python3
"""
Aura AI Complete System Startup and Management Script
Comprehensive system initialization, health monitoring, and interaction examples
Built for BTK Hackathon 2025 - Advanced AI-Powered E-Commerce Platform
"""

import json
import time
import sys
import subprocess
import os
import urllib.request
import urllib.error
from datetime import datetime
from typing import Dict, List, Optional

class AuraSystemManager:
    """
    Comprehensive system manager for the complete Aura AI + E-commerce platform
    Handles system startup, health monitoring, and provides interactive examples
    """
    
    def __init__(self):
        """
        Initialize the Aura System Manager with service configurations
        Defines all services, their ports, and health check endpoints
        """
        # Define all services in the complete Aura AI system
        self.services = {
            'postgres': {
                'name': 'PostgreSQL Database',
                'port': 5432,
                'health_url': None,  # Database doesn't have HTTP health check
                'container': 'aura_postgres',
                'description': 'Central database for e-commerce platform'
            },
            'redis': {
                'name': 'Redis Cache',
                'port': 6379,
                'health_url': None,  # Redis doesn't have HTTP health check
                'container': 'aura_redis',
                'description': 'High-performance caching layer'
            },
            'backend': {
                'name': 'E-Commerce Backend',
                'port': 8000,
                'health_url': 'http://localhost:8000/health',
                'container': 'aura_backend',
                'description': 'Main e-commerce platform API'
            },
            'image_processing': {
                'name': 'Image Processing Service',
                'port': 8001,
                'health_url': 'http://localhost:8001/health',
                'container': 'aura-image-processing',
                'description': 'Computer vision and image analysis AI'
            },
            'nlu': {
                'name': 'NLU Service',
                'port': 8002,
                'health_url': 'http://localhost:8002/health',
                'container': 'aura-nlu',
                'description': 'Natural language understanding AI'
            },
            'style_profile': {
                'name': 'Style Profile Service',
                'port': 8003,
                'health_url': 'http://localhost:8003/health',
                'container': 'aura-style-profile',
                'description': 'Advanced user style profiling AI'
            },
            'combination_engine': {
                'name': 'Combination Engine',
                'port': 8004,
                'health_url': 'http://localhost:8004/health',
                'container': 'aura-combination-engine',
                'description': 'Intelligent outfit combination AI'
            },
            'recommendation_engine': {
                'name': 'Recommendation Engine',
                'port': 8005,
                'health_url': 'http://localhost:8005/health',
                'container': 'aura-recommendation-engine',
                'description': 'FAISS-powered recommendation AI'
            },
            'orchestrator': {
                'name': 'Orchestrator Service',
                'port': 8006,
                'health_url': 'http://localhost:8006/health',
                'container': 'aura-orchestrator',
                'description': 'Advanced workflow coordination'
            },
            'feedback_loop': {
                'name': 'Feedback Loop Service',
                'port': 8007,
                'health_url': 'http://localhost:8007/health',
                'container': 'aura-feedback-loop',
                'description': 'Intelligent learning and adaptation'
            }
        }
        
        # System status tracking
        self.system_status = {}
        self.startup_time = None
    
    def display_welcome_banner(self):
        """
        Display welcome banner with system information
        Shows the comprehensive nature of the AI system
        """
        print("=" * 80)
        print("🌟 AURA AI COMPLETE SYSTEM 🌟")
        print("Advanced AI-Powered E-Commerce Platform")
        print("BTK Hackathon 2025 - Full-Stack AI Integration")
        print(f"System initialized at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        print()
    
    def check_docker_compose(self) -> bool:
        """
        Verify that Docker Compose is available and system is ready
        Ensures all prerequisites are met before system startup
        """
        try:
            # Check if Docker daemon is running first
            result = subprocess.run(['docker', 'ps'], 
                                 capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                print("❌ Docker daemon is not running!")
                print("💡 Please start Docker Desktop and try again.")
                print("   - On Windows: Start Docker Desktop from Start Menu")
                print("   - Wait for Docker Desktop to fully initialize")
                print("   - Look for the Docker whale icon in system tray")
                return False
            
            print("✅ Docker daemon is running")
            
            # Check if Docker Compose is available  
            result = subprocess.run(['docker-compose', '--version'], 
                                 capture_output=True, text=True, check=True)
            print(f"✅ Docker Compose available: {result.stdout.strip()}")
            
            # Check if docker-compose.yml exists
            if not os.path.exists('docker-compose.yml'):
                print("❌ docker-compose.yml not found in current directory")
                return False
                
            print("✅ docker-compose.yml found")
            return True
            
        except subprocess.TimeoutExpired:
            print("❌ Docker daemon check timed out")
            print("💡 Docker Desktop may be starting up. Please wait and try again.")
            return False
        except subprocess.CalledProcessError:
            print("❌ Docker Compose not available")
            return False
        except FileNotFoundError:
            print("❌ Docker not installed or not in PATH")
            print("💡 Please install Docker Desktop from: https://www.docker.com/products/docker-desktop")
            return False
    
    def start_system(self, build: bool = True):
        """
        Start the complete Aura AI system using Docker Compose
        Builds and starts all services with proper dependency management
        """
        print("🚀 Starting Aura AI Complete System...")
        
        try:
            # Build and start command
            cmd = ['docker-compose', 'up', '-d']
            if build:
                cmd.append('--build')
            
            print(f"Executing: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ System started successfully!")
                print("🎉 All services are starting up!")
                self.startup_time = datetime.now()
                return True
            else:
                print(f"❌ Failed to start system:")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ Error starting system: {e}")
            return False
    
    def check_service_health(self, service_key: str, service_info: Dict) -> Dict:
        """
        Check health status of individual service
        Uses HTTP health checks for API services, container checks for databases
        """
        if not service_info.get('health_url'):
            # For services without HTTP health checks (databases), check container status
            try:
                result = subprocess.run(
                    ['docker', 'ps', '--filter', f"name={service_info['container']}", '--format', 'table {{.Status}}'],
                    capture_output=True, text=True
                )
                if 'Up' in result.stdout:
                    return {'status': 'healthy', 'response_time': 0, 'details': 'Container running'}
                else:
                    return {'status': 'unhealthy', 'response_time': 0, 'details': 'Container not running'}
            except:
                return {'status': 'unknown', 'response_time': 0, 'details': 'Unable to check container'}
        
        # For HTTP services, perform actual health check
        try:
            start_time = time.time()
            with urllib.request.urlopen(service_info['health_url'], timeout=10) as response:
                response_time = round((time.time() - start_time) * 1000, 2)
                
                if response.status == 200:
                    return {
                        'status': 'healthy',
                        'response_time': response_time,
                        'details': f'HTTP {response.status}'
                    }
                else:
                    return {
                        'status': 'unhealthy',
                        'response_time': response_time,
                        'details': f'HTTP {response.status}'
                    }
        except urllib.error.URLError as e:
            return {'status': 'error', 'response_time': 0, 'details': str(e)}
        except Exception as e:
            return {'status': 'error', 'response_time': 0, 'details': str(e)}
    
    def monitor_system_health(self):
        """
        Comprehensive system health monitoring
        Checks all services and displays detailed status information
        """
        print("🔍 Checking system health...")
        print()
        
        # Check all services
        healthy_count = 0
        total_count = len(self.services)
        
        print(f"{'Service':<25} {'Status':<12} {'Response':<12} {'Description'}")
        print("-" * 80)
        
        for service_key, service_info in self.services.items():
            status_info = self.check_service_health(service_key, service_info)
            self.system_status[service_key] = status_info
            
            # Determine status display
            if status_info['status'] == 'healthy':
                status_display = "✅ Healthy"
                healthy_count += 1
            elif status_info['status'] == 'unhealthy':
                status_display = "❌ Unhealthy"
            elif status_info['status'] == 'timeout':
                status_display = "⏰ Timeout"
            else:
                status_display = "❓ Unknown"
            
            # Format response time
            if status_info['response_time'] > 0:
                response_time = f"{status_info['response_time']}ms"
            else:
                response_time = "N/A"
            
            print(f"{service_info['name']:<25} {status_display:<12} {response_time:<12} {service_info['description']}")
        
        print("-" * 80)
        
        # System summary
        health_percentage = (healthy_count / total_count) * 100
        if health_percentage == 100:
            print(f"🎉 System Status: Perfect! ({healthy_count}/{total_count} services healthy)")
        elif health_percentage >= 80:
            print(f"✅ System Status: Good ({healthy_count}/{total_count} services healthy)")
        elif health_percentage >= 60:
            print(f"⚠️ System Status: Degraded ({healthy_count}/{total_count} services healthy)")
        else:
            print(f"❌ System Status: Critical ({healthy_count}/{total_count} services healthy)")
        
        print()
        return health_percentage
    
    def display_access_information(self):
        """
        Display comprehensive access information for all system components
        Shows URLs, API documentation, and usage instructions
        """
        print("🌐 System Access Information:")
        print("-" * 80)
        print(f"{'Component':<25} {'URL':<35} {'Purpose'}")
        print("-" * 80)
        
        # Main platform access points
        access_info = [
            ("E-Commerce Platform", "http://localhost:8000", "Main shopping platform"),
            ("AI Orchestrator", "http://localhost:8006", "AI workflow coordination"),
            ("Image Analysis AI", "http://localhost:8001", "Computer vision analysis"),
            ("Language AI", "http://localhost:8002", "Natural language processing"),
            ("Style Profiling AI", "http://localhost:8003", "User style analysis"),
            ("Combination AI", "http://localhost:8004", "Outfit generation"),
            ("Recommendation AI", "http://localhost:8005", "Product recommendations"),
            ("Learning AI", "http://localhost:8007", "Feedback processing"),
        ]
        
        for component, url, purpose in access_info:
            print(f"{component:<25} {url:<35} {purpose}")
        
        print("-" * 80)
        print("📚 API Documentation available at: [URL]/docs for each service")
        print()
    
    def run_ai_demo(self):
        """
        Interactive AI demonstration showing system capabilities
        Demonstrates AI services working together in real scenarios
        """
        print("🤖 AI System Demonstration:")
        print("-" * 50)
        
        # Demo scenarios
        demo_scenarios = [
            {
                'name': 'Image Analysis Demo',
                'description': 'Analyze clothing image using computer vision AI',
                'service': 'image_processing',
                'endpoint': '/analyze_image'
            },
            {
                'name': 'Natural Language Demo',
                'description': 'Process fashion query in multiple languages',
                'service': 'nlu',
                'endpoint': '/analyze_text'
            },
            {
                'name': 'Style Profile Demo',
                'description': 'Generate comprehensive user style profile',
                'service': 'style_profile',
                'endpoint': '/create_profile'
            },
            {
                'name': 'AI Recommendation Demo',
                'description': 'Get personalized product recommendations',
                'service': 'recommendation_engine',
                'endpoint': '/get_recommendations'
            }
        ]
        
        for i, scenario in enumerate(demo_scenarios, 1):
            print(f"{i}. {scenario['name']}: {scenario['description']}")
            
            service_info = self.services.get(scenario['service'])
            if service_info:
                demo_url = f"http://localhost:{service_info['port']}{scenario['endpoint']}"
                print(f"   📡 Available at: {demo_url}")
                print(f"   ✅ Service ready for testing!")
            else:
                print(f"   ❌ Service {scenario['service']} not found")
            print()
    
    def display_management_commands(self):
        """
        Display system management commands and usage instructions
        Provides comprehensive system administration guidance
        """
        print("🛠️ System Management Commands:")
        print("-" * 80)
        
        management_commands = [
            ("Health Check", "python run_aura.py --health", "Check all service health"),
            ("Start System", "docker-compose up -d --build", "Start all services"),
            ("Stop System", "docker-compose down", "Stop all services"),
            ("View Logs", "docker-compose logs -f [service-name]", "View service logs"),
            ("Scale Service", "docker-compose up --scale [service]=3", "Scale specific service"),
            ("Restart Service", "docker-compose restart [service-name]", "Restart specific service"),
            ("System Status", "docker-compose ps", "Check container status"),
            ("Remove All Data", "docker-compose down -v", "Clear all volumes"),
        ]
        
        for command, usage, description in management_commands:
            print(f"• {command:<20} {usage:<40} {description}")
        
        print("-" * 80)
        print()
    
    def stop_system(self):
        """
        Gracefully stop the complete Aura AI system
        Ensures proper shutdown of all services and containers
        """
        print("🛑 Stopping Aura AI Complete System...")
        
        try:
            result = subprocess.run(['docker-compose', 'down'], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ System stopped successfully!")
                return True
            else:
                print(f"❌ Error stopping system:")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ Error stopping system: {e}")
            return False

def main():
    """
    Main function for Aura AI system management
    Provides interactive system control and monitoring
    """
    manager = AuraSystemManager()
    
    # Display welcome banner
    manager.display_welcome_banner()
    
    # Check prerequisites
    if not manager.check_docker_compose():
        print("❌ Prerequisites not met. Please install Docker and Docker Compose.")
        return
    
    # Parse command line arguments for different operations
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == '--health':
            manager.monitor_system_health()
        elif command == '--start':
            if manager.start_system():
                print("⏳ Waiting for services to initialize (30 seconds)...")
                time.sleep(30)
                manager.monitor_system_health()
                manager.display_access_information()
        elif command == '--stop':
            manager.stop_system()
        elif command == '--demo':
            manager.run_ai_demo()
        else:
            print(f"❌ Unknown command: {command}")
            manager.display_management_commands()
    else:
        # Interactive mode - full system management
        print("🚀 Starting complete system initialization...")
        
        # Start the system
        if manager.start_system():
            print("⏳ Waiting for services to initialize (30 seconds)...")
            time.sleep(30)
            
            # Check system health
            health_percentage = manager.monitor_system_health()
            
            # Display access information
            manager.display_access_information()
            
            # Run AI demonstration if system is healthy
            if health_percentage >= 80:
                print("🎉 System is ready! AI services available for testing:")
                manager.run_ai_demo()
            
            # Display management commands
            manager.display_management_commands()
            
            print("🌟 Aura AI Complete System is now running!")
            print("🌐 Access the main platform at: http://localhost:8000")
            print("🤖 Access AI services at: http://localhost:8006")
        else:
            print("❌ Failed to start system. Please check Docker and try again.")

if __name__ == "__main__":
    main()
