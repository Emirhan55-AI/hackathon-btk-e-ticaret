# 🛡️ PHASE 2: CIRCUIT BREAKER PATTERN FOR SERVICE RESILIENCE

import asyncio
import time
import logging
from enum import Enum
from typing import Callable, Any, Optional, Dict
from dataclasses import dataclass
from functools import wraps

logger = logging.getLogger(__name__)

class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, requests blocked
    HALF_OPEN = "half_open"  # Testing if service recovered

@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker"""
    failure_threshold: int = 5           # Number of failures before opening
    timeout: float = 60.0               # Seconds to wait before trying again
    expected_exception: type = Exception # Exception type to monitor
    recovery_timeout: float = 30.0      # Half-open state timeout

class CircuitBreaker:
    """
    PHASE 2 Enhanced Circuit Breaker for service resilience.
    Prevents cascade failures by monitoring service health.
    """
    
    def __init__(self, config: CircuitBreakerConfig):
        self.config = config
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self.success_count = 0
        self.total_requests = 0
        
    def __call__(self, func: Callable) -> Callable:
        """Decorator to wrap functions with circuit breaker"""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await self.call(func, *args, **kwargs)
        return wrapper
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with circuit breaker protection.
        """
        self.total_requests += 1
        
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                logger.info(f"🔄 Circuit breaker HALF-OPEN for {func.__name__}")
            else:
                raise CircuitBreakerOpenException(
                    f"Circuit breaker OPEN for {func.__name__}. "
                    f"Next attempt in {self._time_until_next_attempt():.1f}s"
                )
        
        try:
            # Execute the protected function
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
                
            # Success - reset failure count
            self._on_success()
            return result
            
        except self.config.expected_exception as e:
            # Expected failure - increment counter
            self._on_failure()
            raise e
        except Exception as e:
            # Unexpected exception - still count as failure
            self._on_failure()
            raise e
    
    def _on_success(self):
        """Handle successful call"""
        self.failure_count = 0
        self.success_count += 1
        
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED
            logger.info(f"✅ Circuit breaker CLOSED - Service recovered")
    
    def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.config.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning(
                f"🚨 Circuit breaker OPEN - "
                f"{self.failure_count} failures exceeded threshold"
            )
    
    def _should_attempt_reset(self) -> bool:
        """Check if we should attempt to reset the circuit breaker"""
        return (
            self.last_failure_time and 
            time.time() - self.last_failure_time >= self.config.timeout
        )
    
    def _time_until_next_attempt(self) -> float:
        """Time remaining until next attempt"""
        if not self.last_failure_time:
            return 0.0
        return self.config.timeout - (time.time() - self.last_failure_time)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get circuit breaker statistics"""
        return {
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "total_requests": self.total_requests,
            "success_rate": self.success_count / max(self.total_requests, 1) * 100,
            "last_failure_time": self.last_failure_time,
            "time_until_next_attempt": self._time_until_next_attempt() if self.state == CircuitState.OPEN else 0
        }

class CircuitBreakerOpenException(Exception):
    """Exception raised when circuit breaker is open"""
    pass

# PHASE 2: Service-specific circuit breakers
class ServiceCircuitBreakers:
    """
    Manages circuit breakers for all microservices.
    """
    
    def __init__(self):
        # Different configurations for different service types
        self.breakers = {
            "image_processing": CircuitBreaker(CircuitBreakerConfig(
                failure_threshold=3,
                timeout=30.0,
                recovery_timeout=15.0
            )),
            "nlu_service": CircuitBreaker(CircuitBreakerConfig(
                failure_threshold=5,
                timeout=45.0,
                recovery_timeout=20.0
            )),
            "style_profile": CircuitBreaker(CircuitBreakerConfig(
                failure_threshold=4,
                timeout=60.0,
                recovery_timeout=25.0
            )),
            "combination_engine": CircuitBreaker(CircuitBreakerConfig(
                failure_threshold=3,
                timeout=40.0,
                recovery_timeout=15.0
            )),
            "recommendation": CircuitBreaker(CircuitBreakerConfig(
                failure_threshold=5,
                timeout=50.0,
                recovery_timeout=20.0
            )),
            "feedback_loop": CircuitBreaker(CircuitBreakerConfig(
                failure_threshold=6,
                timeout=35.0,
                recovery_timeout=10.0
            ))
        }
    
    def get_breaker(self, service_name: str) -> CircuitBreaker:
        """Get circuit breaker for specific service"""
        return self.breakers.get(service_name)
    
    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all circuit breakers"""
        return {
            service: breaker.get_stats() 
            for service, breaker in self.breakers.items()
        }
    
    def get_healthy_services(self) -> list:
        """Get list of services with closed circuit breakers"""
        return [
            service for service, breaker in self.breakers.items()
            if breaker.state == CircuitState.CLOSED
        ]
    
    def get_failing_services(self) -> list:
        """Get list of services with open circuit breakers"""
        return [
            service for service, breaker in self.breakers.items()
            if breaker.state == CircuitState.OPEN
        ]

# PHASE 2: Global circuit breaker manager
circuit_breakers = ServiceCircuitBreakers()

# PHASE 2: Decorators for easy use
def with_circuit_breaker(service_name: str):
    """
    Decorator to add circuit breaker protection to service calls.
    
    Usage:
    @with_circuit_breaker("image_processing")
    async def call_image_service():
        # Service call here
        pass
    """
    def decorator(func: Callable):
        breaker = circuit_breakers.get_breaker(service_name)
        if breaker:
            return breaker(func)
        else:
            logger.warning(f"No circuit breaker configured for {service_name}")
            return func
    return decorator

# PHASE 2: Utility functions
async def call_with_fallback(
    primary_service: str,
    fallback_service: str,
    primary_func: Callable,
    fallback_func: Callable,
    *args, **kwargs
) -> Any:
    """
    Call primary service with fallback to secondary service.
    """
    primary_breaker = circuit_breakers.get_breaker(primary_service)
    
    try:
        if primary_breaker:
            return await primary_breaker.call(primary_func, *args, **kwargs)
        else:
            return await primary_func(*args, **kwargs)
    except (CircuitBreakerOpenException, Exception) as e:
        logger.warning(f"Primary service {primary_service} failed: {e}")
        logger.info(f"🔄 Falling back to {fallback_service}")
        
        fallback_breaker = circuit_breakers.get_breaker(fallback_service)
        if fallback_breaker:
            return await fallback_breaker.call(fallback_func, *args, **kwargs)
        else:
            return await fallback_func(*args, **kwargs)

def get_service_health_summary() -> Dict[str, Any]:
    """
    Get overall service health summary based on circuit breaker states.
    """
    all_stats = circuit_breakers.get_all_stats()
    healthy_services = circuit_breakers.get_healthy_services()
    failing_services = circuit_breakers.get_failing_services()
    
    total_services = len(all_stats)
    healthy_count = len(healthy_services)
    
    return {
        "overall_health_percentage": (healthy_count / total_services * 100) if total_services > 0 else 0,
        "healthy_services": healthy_services,
        "failing_services": failing_services,
        "total_services": total_services,
        "detailed_stats": all_stats,
        "status": "healthy" if len(failing_services) == 0 else "degraded" if len(failing_services) < total_services / 2 else "critical"
    }

# PHASE 2: Example usage patterns
async def example_protected_service_call():
    """
    Example of how to use circuit breaker protection.
    """
    
    @with_circuit_breaker("image_processing")
    async def call_image_service(image_data):
        # Simulate service call
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post("http://localhost:8001/analyze_image", data=image_data) as response:
                return await response.json()
    
    try:
        result = await call_image_service({"image": "test_data"})
        return {"status": "success", "result": result}
    except CircuitBreakerOpenException as e:
        return {"status": "circuit_open", "message": str(e)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # Test circuit breaker functionality
    async def test_circuit_breaker():
        logger.info("🧪 Testing Circuit Breaker functionality...")
        
        # Get health summary
        health = get_service_health_summary()
        print(f"Service Health: {health['overall_health_percentage']:.1f}%")
        print(f"Healthy: {health['healthy_services']}")
        print(f"Failing: {health['failing_services']}")
    
    asyncio.run(test_circuit_breaker())
