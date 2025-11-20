from __future__ import annotations

from datetime import date


def get_billing_reminder_html(
    client_name: str, due_date: date, days_until_due: int
) -> str:
    """
    Generate HTML email template for billing reminder.

    Args:
        client_name: Client's name
        due_date: Due date of the bill
        days_until_due: Days until due date

    Returns:
        HTML content as string
    """
    urgency_color = "#e74c3c" if days_until_due <= 1 else "#f39c12"
    urgency_text = "URGENTE" if days_until_due <= 1 else "ATENÇÃO"

    return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lembrete de Boleto</title>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px; line-height: 1.6;">
    <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <!-- Header -->
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center;">
            <h1 style="margin: 0; font-size: 24px; font-weight: 600;">Lembrete de Boleto</h1>
        </div>
        
        <!-- Content -->
        <div style="padding: 30px;">
            <p style="font-size: 16px; color: #333; margin-bottom: 20px;">
                Olá <strong style="color: #667eea;">{client_name}</strong>,
            </p>
            
            <div style="background: #fff3cd; border-left: 4px solid {urgency_color}; padding: 15px; margin: 20px 0; border-radius: 4px;">
                <p style="margin: 0; font-size: 14px; color: #856404; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">
                    {urgency_text}
                </p>
            </div>
            
            <p style="font-size: 16px; color: #666; line-height: 1.6; margin-bottom: 15px;">
                Este é um lembrete de que seu boleto vence em 
                <span style="color: {urgency_color}; font-weight: bold; font-size: 18px;">
                    {days_until_due} dia{'s' if days_until_due > 1 else ''}
                </span>
            </p>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 6px; margin: 20px 0;">
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="padding: 8px 0; color: #666; font-size: 14px;">Cliente:</td>
                        <td style="padding: 8px 0; color: #333; font-size: 14px; font-weight: 600; text-align: right;">{client_name}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #666; font-size: 14px;">Data de Vencimento:</td>
                        <td style="padding: 8px 0; color: {urgency_color}; font-size: 14px; font-weight: 600; text-align: right;">{due_date.strftime('%d/%m/%Y')}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #666; font-size: 14px;">Dias Restantes:</td>
                        <td style="padding: 8px 0; color: {urgency_color}; font-size: 14px; font-weight: 600; text-align: right;">{days_until_due} dia{'s' if days_until_due > 1 else ''}</td>
                    </tr>
                </table>
            </div>
            
            <p style="font-size: 14px; color: #999; margin-top: 20px; margin-bottom: 0;">
                Por favor, verifique seu boleto e efetue o pagamento antes do vencimento para evitar multas e juros.
            </p>
        </div>
        
        <!-- Footer -->
        <div style="background: #f8f9fa; padding: 20px; text-align: center; border-top: 1px solid #dee2e6;">
            <p style="font-size: 12px; color: #999; margin: 0 0 10px 0;">
                Este é um email automático, por favor não responda.
            </p>
            <p style="font-size: 11px; color: #bbb; margin: 0;">
                © {date.today().year} - Todos os direitos reservados
            </p>
        </div>
    </div>
</body>
</html>
"""


def get_billing_reminder_text(
    client_name: str, due_date: date, days_until_due: int
) -> str:
    """
    Generate plain text email template for billing reminder.

    Args:
        client_name: Client's name
        due_date: Due date of the bill
        days_until_due: Days until due date

    Returns:
        Plain text content as string
    """
    return f"""
Olá {client_name},

Este é um lembrete de que seu boleto vence em {days_until_due} dia{'s' if days_until_due > 1 else ''}.

Data de Vencimento: {due_date.strftime('%d/%m/%Y')}
Dias Restantes: {days_until_due} dia{'s' if days_until_due > 1 else ''}

Por favor, verifique seu boleto e efetue o pagamento antes do vencimento para evitar multas e juros.

Este é um email automático, por favor não responda.
""".strip()


