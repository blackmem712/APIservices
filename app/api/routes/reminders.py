from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_billing_reminder_service
from app.models.reminder import BillingReminderRequest, BillingReminderResponse
from app.services.billing_reminder import (
    BillingReminderError,
    BillingReminderService,
)

router = APIRouter()


@router.post(
    "/billing/run",
    response_model=BillingReminderResponse,
    status_code=status.HTTP_200_OK,
    summary="Executa o job diario que envia avisos de boleto por WhatsApp.",
)
def run_billing_reminders(
    payload: BillingReminderRequest,
    reminder_service: BillingReminderService = Depends(
        get_billing_reminder_service
    ),
) -> BillingReminderResponse:
    """Trigger the reminder workflow for the configured XLSX file."""
    try:
        return reminder_service.run(payload)
    except BillingReminderError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
