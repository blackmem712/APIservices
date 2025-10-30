from functools import lru_cache

from app.core.config import get_settings
from app.services.billing_reminder import BillingReminderService
from app.services.service_manager import ServiceManager
from app.services.waha_client import WahaClient


@lru_cache
def get_service_manager() -> ServiceManager:
    """Provide a singleton ServiceManager instance."""
    return ServiceManager()


@lru_cache
def get_waha_client() -> WahaClient:
    """Create a singleton WAHA HTTP client."""
    settings = get_settings()
    return WahaClient(
        base_url=settings.waha_base_url,
        api_token=settings.waha_api_token,
        default_sender=settings.waha_default_sender,
        timeout_seconds=settings.waha_timeout_seconds,
    )


@lru_cache
def get_billing_reminder_service() -> BillingReminderService:
    """Create a singleton reminder service configured with defaults."""
    settings = get_settings()
    return BillingReminderService(
        default_sheet_path=settings.billing_sheet_path,
        reminder_days=settings.reminder_days_before_due,
        waha_client=get_waha_client(),
    )
