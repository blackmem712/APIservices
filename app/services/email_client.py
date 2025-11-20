from __future__ import annotations

import smtplib
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict, Optional

import httpx


class EmailClientError(Exception):
    """Raised when email sending fails."""

    pass


@dataclass
class EmailClient:
    """Client for sending emails via SMTP or transactional API."""

    # SMTP settings
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_use_tls: bool = True

    # API settings (for SendGrid, Resend, etc.)
    api_provider: Optional[str] = None  # "sendgrid", "resend", "ses", etc.
    api_key: Optional[str] = None
    api_base_url: Optional[str] = None

    # Default sender
    default_from_email: str = "noreply@example.com"
    default_from_name: Optional[str] = None

    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send an email using SMTP or API provider.

        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML body content
            text_content: Plain text fallback (optional)
            from_email: Sender email (uses default if not provided)
            from_name: Sender name (optional)

        Returns:
            Dict with result information

        Raises:
            EmailClientError: If sending fails
        """
        if self.api_provider:
            return self._send_via_api(
                to_email=to_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content,
                from_email=from_email or self.default_from_email,
                from_name=from_name or self.default_from_name,
            )
        else:
            return self._send_via_smtp(
                to_email=to_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content,
                from_email=from_email or self.default_from_email,
                from_name=from_name or self.default_from_name,
            )

    def _send_via_smtp(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str],
        from_email: str,
        from_name: Optional[str],
    ) -> Dict[str, Any]:
        """Send email using SMTP."""
        if not self.smtp_host:
            raise EmailClientError(
                "SMTP não configurado. Defina API_EMAIL_SMTP_HOST ou use API_EMAIL_PROVIDER."
            )

        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = (
                f'"{from_name}" <{from_email}>' if from_name else from_email
            )
            msg["To"] = to_email

            # Add text and HTML parts
            if text_content:
                msg.attach(MIMEText(text_content, "plain", "utf-8"))
            msg.attach(MIMEText(html_content, "html", "utf-8"))

            # Send via SMTP
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.smtp_use_tls:
                    server.starttls()
                if self.smtp_user and self.smtp_password:
                    server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            return {
                "success": True,
                "method": "smtp",
                "to": to_email,
                "message": "Email enviado com sucesso via SMTP.",
            }

        except smtplib.SMTPException as exc:
            raise EmailClientError(f"Erro SMTP: {exc}") from exc
        except Exception as exc:
            raise EmailClientError(f"Falha ao enviar email: {exc}") from exc

    def _send_via_api(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str],
        from_email: str,
        from_name: Optional[str],
    ) -> Dict[str, Any]:
        """Send email using transactional API."""
        if not self.api_key:
            raise EmailClientError(
                f"API key não configurada para {self.api_provider}."
            )

        provider = self.api_provider.lower()

        if provider == "sendgrid":
            return self._send_via_sendgrid(
                to_email, subject, html_content, text_content, from_email, from_name
            )
        elif provider == "resend":
            return self._send_via_resend(
                to_email, subject, html_content, text_content, from_email, from_name
            )
        else:
            raise EmailClientError(f"Provedor de API não suportado: {provider}")

    def _send_via_sendgrid(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str],
        from_email: str,
        from_name: Optional[str],
    ) -> Dict[str, Any]:
        """Send email via SendGrid API."""
        url = "https://api.sendgrid.com/v3/mail/send"
        payload = {
            "personalizations": [{"to": [{"email": to_email}]}],
            "from": {
                "email": from_email,
                "name": from_name or "API Services",
            },
            "subject": subject,
            "content": [
                {"type": "text/html", "value": html_content},
            ],
        }

        if text_content:
            payload["content"].append({"type": "text/plain", "value": text_content})

        try:
            response = httpx.post(
                url,
                json=payload,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                timeout=30.0,
            )
            response.raise_for_status()
            return {
                "success": True,
                "method": "sendgrid",
                "to": to_email,
                "message": "Email enviado com sucesso via SendGrid.",
            }
        except httpx.HTTPStatusError as exc:
            raise EmailClientError(
                f"SendGrid respondeu com status {exc.response.status_code}: "
                f"{exc.response.text}"
            ) from exc
        except httpx.HTTPError as exc:
            raise EmailClientError(f"Falha ao contatar SendGrid: {exc}") from exc

    def _send_via_resend(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str],
        from_email: str,
        from_name: Optional[str],
    ) -> Dict[str, Any]:
        """Send email via Resend API."""
        url = "https://api.resend.com/emails"
        payload = {
            "from": f"{from_name or 'API Services'} <{from_email}>",
            "to": [to_email],
            "subject": subject,
            "html": html_content,
        }

        if text_content:
            payload["text"] = text_content

        try:
            response = httpx.post(
                url,
                json=payload,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                timeout=30.0,
            )
            response.raise_for_status()
            data = response.json()
            return {
                "success": True,
                "method": "resend",
                "to": to_email,
                "message": f"Email enviado com sucesso via Resend (ID: {data.get('id', 'N/A')}).",
            }
        except httpx.HTTPStatusError as exc:
            raise EmailClientError(
                f"Resend respondeu com status {exc.response.status_code}: "
                f"{exc.response.text}"
            ) from exc
        except httpx.HTTPError as exc:
            raise EmailClientError(f"Falha ao contatar Resend: {exc}") from exc


