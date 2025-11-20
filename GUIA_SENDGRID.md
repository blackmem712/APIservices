# Guia Completo: Como Usar SendGrid na API

## 📋 Passo a Passo

### 1. Criar Conta no SendGrid

1. Acesse: https://signup.sendgrid.com/
2. Preencha os dados (nome, email, senha)
3. Confirme seu email
4. Complete o cadastro (pode pular verificação de domínio por enquanto)

### 2. Obter API Key (Token)

1. Faça login no SendGrid: https://app.sendgrid.com/
2. Vá em **Settings** → **API Keys** (menu lateral esquerdo)
3. Clique em **Create API Key**
4. Configure:
   - **API Key Name**: `API Services` (ou qualquer nome)
   - **API Key Permissions**: Selecione **Full Access** (ou apenas **Mail Send** se preferir)
5. Clique em **Create & View**
6. **COPIE O TOKEN** (ele só aparece uma vez!)
   - Formato: `SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - ⚠️ **IMPORTANTE**: Salve este token em local seguro!

### 3. Verificar Remetente (Sender)

O SendGrid exige que você verifique o email remetente antes de enviar.

#### Opção A: Verificar Email Individual (Mais Rápido - Para Testes)

1. Vá em **Settings** → **Sender Authentication**
2. Clique em **Verify a Single Sender**
3. Preencha:
   - **From Email Address**: `noreply@suaempresa.com` (ou seu email)
   - **From Name**: `Sua Empresa`
   - **Reply To**: (mesmo email ou outro)
   - **Company Address**: Endereço da empresa
   - **Website**: Site da empresa
4. Clique em **Create**
5. **Verifique seu email** - SendGrid enviará um link de confirmação
6. Clique no link no email para verificar

#### Opção B: Verificar Domínio (Recomendado para Produção)

1. Vá em **Settings** → **Sender Authentication**
2. Clique em **Authenticate Your Domain**
3. Siga as instruções para adicionar registros DNS
4. Aguarde verificação (pode levar algumas horas)

### 4. Configurar na API

Adicione as variáveis no seu arquivo `.env` (na raiz do projeto):

```bash
# Habilitar email
API_EMAIL_ENABLED=true

# Usar SendGrid
API_EMAIL_PROVIDER=sendgrid

# Email remetente (DEVE ser o email verificado no SendGrid)
API_EMAIL_FROM=noreply@suaempresa.com

# Nome do remetente
API_EMAIL_FROM_NAME="Sua Empresa"

# Token do SendGrid (cole o token que você copiou)
API_EMAIL_API_KEY=SG.seu-token-aqui-coloque-o-token-completo
```

### 5. Testar

1. Certifique-se que sua planilha tem a coluna `email`
2. Execute o endpoint:
   ```bash
   POST http://localhost:8000/api/reminders/billing/run
   ```
3. Verifique os logs ou resposta da API
4. Confira a caixa de entrada do destinatário

## 🔍 Verificar se Funcionou

### No SendGrid Dashboard:

1. Acesse: https://app.sendgrid.com/
2. Vá em **Activity** (menu lateral)
3. Você verá todos os emails enviados com status:
   - ✅ **Delivered**: Enviado com sucesso
   - ⚠️ **Bounced**: Email inválido
   - 📧 **Opened**: Email aberto pelo destinatário

### Na Resposta da API:

A resposta do endpoint incluirá detalhes:
```json
{
  "results": [
    {
      "client_name": "João Silva",
      "status": "sent",
      "detail": "WhatsApp: Mensagem registrada no WAHA. | Email: Email enviado com sucesso via SendGrid."
    }
  ]
}
```

## ⚠️ Problemas Comuns

### Erro: "The from address does not match a verified Sender Identity"

**Solução**: O email em `API_EMAIL_FROM` deve ser exatamente o mesmo que você verificou no SendGrid.

### Erro: "Invalid API Key"

**Solução**: 
- Verifique se copiou o token completo (começa com `SG.`)
- Certifique-se que não há espaços extras
- Gere um novo token se necessário

### Emails não chegam / Vão para spam

**Solução**:
- Use um domínio verificado (não apenas email individual)
- Configure SPF/DKIM no DNS (SendGrid fornece instruções)
- Evite palavras de spam no assunto/corpo

## 📊 Planos SendGrid

- **Free**: 100 emails/dia (perfeito para começar!)
- **Essentials**: $19.95/mês - 50k emails
- **Pro**: $89.95/mês - 100k emails

Para lembretes de boletos, o plano **Free** geralmente é suficiente.

## 🎯 Próximos Passos

1. **Monitorar estatísticas**: Use o dashboard do SendGrid
2. **Personalizar templates**: Modifique `app/services/email_templates.py`
3. **Configurar domínio**: Para melhor entrega em produção
4. **Adicionar tracking**: SendGrid já rastreia aberturas automaticamente

## 📚 Recursos Úteis

- Documentação SendGrid: https://docs.sendgrid.com/
- Status da API: https://status.sendgrid.com/
- Suporte: https://support.sendgrid.com/


