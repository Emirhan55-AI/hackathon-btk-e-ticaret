# Simple dependency injection without external library
# This is a simplified version for development

class Container:
    """Simple DI container."""
    
    def __init__(self):
        self._services = {}
    
    def set(self, name: str, service):
        self._services[name] = service
    
    def get(self, name: str):
        return self._services.get(name)


# Global container instance
_container = Container()


def get_container() -> Container:
    """Get the global container instance."""
    return _container


def setup_container():
    """Setup dependency injection container."""
    # For now, this is a placeholder
    # In a full implementation, we would register all dependencies here
    pass
