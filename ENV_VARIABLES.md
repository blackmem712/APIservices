# Variáveis de Ambiente

Este documento lista todas as variáveis de ambiente necessárias para configurar o projeto.

## Configurações Gerais da API

```bash
API_ENVIRONMENT=development
API_DEBUG=true
```

## Configurações do MySQL

```bash
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_DATABASE=contas_receber
MYSQL_USER=apiuser
MYSQL_PASSWORD=apipassword
MYSQL_PORT=3306
MYSQL_HOST=mysql
```

**Nota:** As variáveis `MYSQL_*` são usadas pelo Docker Compose. Para a aplicação Python, use o prefixo `API_`:

```bash
API_MYSQL_HOST=mysql
API_MYSQL_PORT=3306
API_MYSQL_DATABASE=contas_receber
API_MYSQL_USER=apiuser
API_MYSQL_PASSWORD=apipassword
```

## Configurações do WhatsApp (WAHA)

```bash
API_BILLING_SHEET_PATH=/caminho/para/clientes.xlsx
API_REMINDER_DAYS_BEFORE_DUE="[3,1]"
API_WAHA_BASE_URL=http://waha:3000
API_WAHA_API_TOKEN=
API_WAHA_DEFAULT_SENDER=5547999999999
API_WAHA_TIMEOUT_SECONDS=15

# Configurações do WAHA Container
WAHA_ADMIN_USER=admin
WAHA_ADMIN_PASS=change-me
```

## Configurações de Email

### Opção 1: SMTP (Gmail, Outlook, servidor próprio)

```bash
API_EMAIL_ENABLED=true
API_EMAIL_PROVIDER=smtp
API_EMAIL_FROM=noreply@suaempresa.com
API_EMAIL_FROM_NAME="Sua Empresa"
API_EMAIL_SMTP_HOST=smtp.gmail.com
API_EMAIL_SMTP_PORT=587
API_EMAIL_SMTP_USER=seu@email.com
API_EMAIL_SMTP_PASSWORD=sua-senha-ou-app-password
API_EMAIL_SMTP_USE_TLS=true
```

### Opção 2: SendGrid

```bash
API_EMAIL_ENABLED=true
API_EMAIL_PROVIDER=sendgrid
API_EMAIL_FROM=noreply@suaempresa.com
API_EMAIL_FROM_NAME="Sua Empresa"
API_EMAIL_API_KEY=SG.seu-token-sendgrid
```

### Opção 3: Resend

```bash
API_EMAIL_ENABLED=true
API_EMAIL_PROVIDER=resend
API_EMAIL_FROM=noreply@suaempresa.com
API_EMAIL_FROM_NAME="Sua Empresa"
API_EMAIL_API_KEY=re_seu-token-resend
```

## Como Usar

1. Copie este arquivo para `.env` na raiz do projeto
2. Ajuste os valores conforme necessário
3. O arquivo `.env` está no `.gitignore` e não será versionado

## Exemplo Completo

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```bash
# Configurações Gerais
API_ENVIRONMENT=production
API_DEBUG=false

# MySQL
MYSQL_ROOT_PASSWORD=seu_root_password_seguro
MYSQL_DATABASE=contas_receber
MYSQL_USER=apiuser
MYSQL_PASSWORD=seu_password_seguro
MYSQL_PORT=3306
MYSQL_HOST=mysql

API_MYSQL_HOST=mysql
API_MYSQL_PORT=3306
API_MYSQL_DATABASE=contas_receber
API_MYSQL_USER=apiuser
API_MYSQL_PASSWORD=seu_password_seguro

# WAHA
API_WAHA_BASE_URL=http://waha:3000
API_WAHA_DEFAULT_SENDER=5547999999999
WAHA_ADMIN_USER=admin
WAHA_ADMIN_PASS=senha_segura_admin

# Email (SendGrid)
API_EMAIL_ENABLED=true
API_EMAIL_PROVIDER=sendgrid
API_EMAIL_FROM=noreply@suaempresa.com
API_EMAIL_FROM_NAME="Sua Empresa"
API_EMAIL_API_KEY=SG.seu-token-aqui
```

