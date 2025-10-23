from functools import lru_cache

from app.services.service_manager import ServiceManager


@lru_cache
def get_service_manager() -> ServiceManager:
    """Provide a singleton ServiceManager instance."""
    return ServiceManager()
