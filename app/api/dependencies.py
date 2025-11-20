from functools import lru_cache

from app.core.config import get_settings
from app.services.billing_reminder import BillingReminderService
from app.services.email_client import EmailClient
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
def get_email_client() -> EmailClient | None:
    """Create a singleton email client if email is enabled."""
    settings = get_settings()
    if not settings.email_enabled:
        return None

    return EmailClient(
        smtp_host=settings.email_smtp_host,
        smtp_port=settings.email_smtp_port,
        smtp_user=settings.email_smtp_user,
        smtp_password=settings.email_smtp_password,
        smtp_use_tls=settings.email_smtp_use_tls,
        api_provider=settings.email_provider,
        api_key=settings.email_api_key,
        api_base_url=settings.email_api_base_url,
        default_from_email=settings.email_from,
        default_from_name=settings.email_from_name,
    )


@lru_cache
def get_billing_reminder_service() -> BillingReminderService:
    """Create a singleton reminder service configured with defaults."""
    settings = get_settings()
    email_client = get_email_client()
    return BillingReminderService(
        default_sheet_path=settings.billing_sheet_path,
        reminder_days=settings.reminder_days_before_due,
        waha_client=get_waha_client(),
        email_client=email_client,
        email_enabled=settings.email_enabled,
    )
