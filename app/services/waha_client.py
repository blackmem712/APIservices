from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import httpx


class WahaClientError(Exception):
    """Raised when WAHA API returns an error."""

    pass


@dataclass
class WahaClient:
    """Small HTTP client responsible for sending WhatsApp messages."""

    base_url: str
    api_token: Optional[str] = None
    default_sender: Optional[str] = None
    timeout_seconds: float = 10.0

    def send_text_message(
        self,
        recipient: str,
        message: str,
        sender: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send a WhatsApp text message using WAHA."""
        payload = {
            "phone": self._sanitize_phone(recipient),
            "message": message,
        }
        sender_to_use = sender or self.default_sender
        if sender_to_use:
            payload["sender"] = sender_to_use

        try:
            response = httpx.post(
                self._build_url("/api/sendText"),
                json=payload,
                headers=self._build_headers(),
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise WahaClientError(
                f"WAHA respondeu com status {exc.response.status_code}: "
                f"{exc.response.text}"
            ) from exc
        except httpx.HTTPError as exc:  # network issues, timeouts, etc.
            raise WahaClientError(f"Falha ao contatar WAHA: {exc}") from exc

        return self._safe_json(response)

    def _build_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        return headers

    def _build_url(self, path: str) -> str:
        base = self.base_url.rstrip("/")
        suffix = path.lstrip("/")
        return f"{base}/{suffix}"

    @staticmethod
    def _sanitize_phone(phone: str) -> str:
        digits = "".join(ch for ch in phone if ch.isdigit())
        if phone.strip().startswith("+"):
            return f"+{digits}"
        return digits

    @staticmethod
    def _safe_json(response: httpx.Response) -> Dict[str, Any]:
        try:
            data = response.json()
            if isinstance(data, dict):
                return data
        except ValueError:
            pass
        return {"raw": response.text}
