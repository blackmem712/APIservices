from __future__ import annotations

from datetime import datetime
from threading import RLock
from typing import Dict, Iterable
from uuid import UUID, uuid4

from app.models.service import Service, ServiceCreate, ServiceUpdate


class ServiceNotFoundError(Exception):
    """Raised when a service could not be located."""

    def __init__(self, service_id: UUID) -> None:
        super().__init__(f"Service {service_id} not found")
        self.service_id = service_id


class ServiceManager:
    """Simple in-memory service registry."""

    def __init__(self) -> None:
        self._services: Dict[UUID, Service] = {}
        self._lock = RLock()

    def list_services(self) -> Iterable[Service]:
        """Return all services ordered by creation time."""
        with self._lock:
            return sorted(self._services.values(), key=lambda svc: svc.created_at)

    def get_service(self, service_id: UUID) -> Service:
        """Return a service by id or raise."""
        with self._lock:
            service = self._services.get(service_id)
            if not service:
                raise ServiceNotFoundError(service_id)
            return service

    def create_service(self, payload: ServiceCreate) -> Service:
        """Persist a new service and return it."""
        now = datetime.utcnow()
        service = Service(
            id=uuid4(),
            created_at=now,
            updated_at=now,
            **payload.model_dump(),
        )
        with self._lock:
            self._services[service.id] = service
        return service

    def update_service(self, service_id: UUID, payload: ServiceUpdate) -> Service:
        """Apply partial updates to an existing service."""
        with self._lock:
            if service_id not in self._services:
                raise ServiceNotFoundError(service_id)

            current = self._services[service_id]
            data = current.model_dump()
            update_data = payload.model_dump(exclude_unset=True)
            data.update(update_data)
            data["updated_at"] = datetime.utcnow()

            updated = Service(**data)
            self._services[service_id] = updated
            return updated

    def delete_service(self, service_id: UUID) -> None:
        """Remove a service from the registry."""
        with self._lock:
            if service_id not in self._services:
                raise ServiceNotFoundError(service_id)
            del self._services[service_id]
