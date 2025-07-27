# 🔧 PHASE 2: Standardized Health Check Enhancement
# This module provides enhanced health check functionality for all services
# with comprehensive monitoring and service discovery capabilities

from typing import Dict, Any, List, Optional
import time
import logging
import platform
import psutil
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class StandardHealthChecker:
    """
    PHASE 2 ENHANCEMENT: Standardized health check implementation for all services.
    
    This class provides comprehensive health monitoring including:
    - Service availability status
    - Performance metrics
    - Resource utilization
    - AI model status (if applicable)
    - Integration health
    """
    
    def __init__(self, service_name: str, version: str = "2.0", port: int = 8000):
        """
        Initialize health checker for a specific service.
        
        Args:
            service_name: Name of the service (e.g., "image_processing")
            version: Service version
            port: Service port number
        """
        self.service_name = service_name
        self.version = version
        self.port = port
        self.startup_time = time.time()
        
        # Service-specific health checkers
        self.custom_checks: List[callable] = []
        
    def add_custom_check(self, check_function: callable, name: str):
        """
        Add custom health check function.
        
        Args:
            check_function: Function that returns (bool, str) - (status, message)
            name: Name of the custom check
        """
        self.custom_checks.append((check_function, name))
        
    def get_comprehensive_health(self) -> Dict[str, Any]:
        """
        Get comprehensive health status including system metrics and custom checks.
        
        Returns:
            Detailed health status dictionary
        """
        try:
            # Basic service info
            health_data = {
                "status": "healthy",
                "service": self.service_name,
                "version": self.version,
                "port": self.port,
                "timestamp": datetime.now().isoformat(),
                "uptime_seconds": round(time.time() - self.startup_time, 2)
            }
            
            # System metrics
            try:
                health_data["system_metrics"] = {
                    "cpu_percent": psutil.cpu_percent(interval=0.1),
                    "memory_percent": psutil.virtual_memory().percent,
                    "disk_percent": psutil.disk_usage('/').percent if platform.system() != 'Windows' else psutil.disk_usage('C:').percent
                }
            except Exception as e:
                logger.warning(f"Could not get system metrics: {e}")
                health_data["system_metrics"] = {"error": "metrics_unavailable"}
            
            # Performance indicators
            health_data["performance"] = {
                "response_time_ms": 0.5,  # Will be updated by actual measurements
                "requests_handled": getattr(self, 'request_count', 0),
                "average_processing_time": getattr(self, 'avg_processing_time', 0.0)
            }
            
            # Run custom health checks
            custom_results = {}
            overall_healthy = True
            
            for check_func, check_name in self.custom_checks:
                try:
                    status, message = check_func()
                    custom_results[check_name] = {
                        "status": "healthy" if status else "unhealthy",
                        "message": message
                    }
                    if not status:
                        overall_healthy = False
                except Exception as e:
                    custom_results[check_name] = {
                        "status": "error",
                        "message": f"Check failed: {str(e)}"
                    }
                    overall_healthy = False
            
            if custom_results:
                health_data["custom_checks"] = custom_results
            
            # Update overall status based on custom checks
            if not overall_healthy:
                health_data["status"] = "degraded"
            
            # PHASE 2 indicators
            health_data["phase2_features"] = {
                "enhanced_monitoring": True,
                "custom_health_checks": len(self.custom_checks),
                "comprehensive_metrics": True,
                "standardized_format": True
            }
            
            return health_data
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "error",
                "service": self.service_name,
                "version": self.version,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_basic_health(self) -> Dict[str, Any]:
        """
        Get basic health status for lightweight checks.
        
        Returns:
            Basic health status dictionary
        """
        return {
            "status": "healthy",
            "service": self.service_name,
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
            "phase2_enhanced": True
        }

def create_ai_model_health_check(models_dict: Dict[str, bool]) -> callable:
    """
    Create health check function for AI models.
    
    Args:
        models_dict: Dictionary of model_name -> availability_status
        
    Returns:
        Health check function
    """
    def check_ai_models():
        try:
            available_models = sum(1 for available in models_dict.values() if available)
            total_models = len(models_dict)
            
            if available_models == 0:
                return False, "No AI models available"
            elif available_models < total_models:
                return True, f"Partial AI capability: {available_models}/{total_models} models"
            else:
                return True, f"Full AI capability: {available_models}/{total_models} models"
        except Exception as e:
            return False, f"AI model check failed: {str(e)}"
    
    return check_ai_models

def create_service_integration_check(service_urls: List[str]) -> callable:
    """
    Create health check function for service integrations.
    
    Args:
        service_urls: List of service URLs to check
        
    Returns:
        Health check function
    """
    def check_service_integrations():
        try:
            import requests
            available_services = 0
            
            for url in service_urls:
                try:
                    response = requests.get(f"{url}/health", timeout=2)
                    if response.status_code == 200:
                        available_services += 1
                except:
                    pass
            
            total_services = len(service_urls)
            if available_services == total_services:
                return True, f"All {total_services} services available"
            elif available_services > 0:
                return True, f"Partial integration: {available_services}/{total_services} services"
            else:
                return False, "No integrated services available"
                
        except Exception as e:
            return False, f"Integration check failed: {str(e)}"
    
    return check_service_integrations
