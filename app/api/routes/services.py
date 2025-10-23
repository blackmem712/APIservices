from __future__ import annotations

from typing import Iterable
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_service_manager
from app.models.service import Service, ServiceCreate, ServiceUpdate
from app.services.service_manager import ServiceManager, ServiceNotFoundError

router = APIRouter()


@router.get("/", response_model=list[Service])
def list_services(
    service_manager: ServiceManager = Depends(get_service_manager),
) -> Iterable[Service]:
    """Return all registered services."""
    return service_manager.list_services()


@router.post(
    "/",
    response_model=Service,
    status_code=status.HTTP_201_CREATED,
)
def create_service(
    payload: ServiceCreate,
    service_manager: ServiceManager = Depends(get_service_manager),
) -> Service:
    """Create a new service entry."""
    return service_manager.create_service(payload)


@router.get(
    "/{service_id}",
    response_model=Service,
)
def get_service(
    service_id: UUID,
    service_manager: ServiceManager = Depends(get_service_manager),
) -> Service:
    """Retrieve a service by identifier."""
    try:
        return service_manager.get_service(service_id)
    except ServiceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.put(
    "/{service_id}",
    response_model=Service,
)
def update_service(
    service_id: UUID,
    payload: ServiceUpdate,
    service_manager: ServiceManager = Depends(get_service_manager),
) -> Service:
    """Update an existing service."""
    try:
        return service_manager.update_service(service_id, payload)
    except ServiceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{service_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_service(
    service_id: UUID,
    service_manager: ServiceManager = Depends(get_service_manager),
) -> None:
    """Remove a service."""
    try:
        service_manager.delete_service(service_id)
    except ServiceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
