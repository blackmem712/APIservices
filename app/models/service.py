from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import AnyHttpUrl, BaseModel, Field


class ServiceStatus(str, Enum):
    """Possible states for a managed service."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"


class ServiceBase(BaseModel):
    """Base attributes present on all service representations."""

    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    endpoint_url: AnyHttpUrl
    status: ServiceStatus = ServiceStatus.ACTIVE


class ServiceCreate(ServiceBase):
    """Payload for creating a new service."""

    pass


class ServiceUpdate(BaseModel):
    """Payload for updating an existing service."""

    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    endpoint_url: Optional[AnyHttpUrl] = None
    status: Optional[ServiceStatus] = None


class Service(ServiceBase):
    """Service model returned by the API."""

    id: UUID
    created_at: datetime
    updated_at: datetime
