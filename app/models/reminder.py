from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ReminderStatus(str, Enum):
    """Possible outcomes when evaluating a billing reminder."""

    SENT = "sent"
    DRY_RUN = "dry-run"
    SKIPPED = "skipped"
    FAILED = "failed"


class BillingReminderRequest(BaseModel):
    """Payload accepted by the reminder endpoint."""

    sheet_path: Optional[str] = Field(
        default=None,
        description="Caminho do XLSX; usa configuracao padrao quando omitido.",
    )
    reference_date: Optional[date] = Field(
        default=None,
        description="Data base para o calculo dos dias restantes.",
    )
    dry_run: bool = Field(
        default=False,
        description="Quando verdadeiro, nao envia mensagens para o WAHA.",
    )
    sender_whatsapp_number: Optional[str] = Field(
        default=None,
        description="Numero/instancia do WAHA utilizado para o envio.",
    )


class ReminderDispatchResult(BaseModel):
    """Detalhes por cliente analisado."""

    client_name: str
    whatsapp_number: str
    due_date: date
    days_until_due: int
    status: ReminderStatus
    message_preview: str
    detail: Optional[str] = None


class BillingReminderResponse(BaseModel):
    """Resumo da execucao do job."""

    sheet_path: str
    reference_date: date
    days_watched: list[int]
    dry_run: bool
    total_rows: int
    eligible_rows: int
    dispatched: int
    results: list[ReminderDispatchResult]
