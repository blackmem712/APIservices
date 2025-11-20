# Configuração do MySQL

Este diretório contém os scripts de inicialização do banco de dados MySQL.

## Estrutura

- `init/01_init_schema.sql`: Script SQL que cria as tabelas necessárias para armazenar os dados de contas a receber.

## Tabelas Criadas

### `contas_receber`
Tabela principal que armazena todos os dados importados do XML de contas a receber.

**Campos principais:**
- Dados do cliente (nome, CPF, endereço, telefone)
- Dados da operação (nota fiscal, contrato, parcela)
- Valores e datas (vencimento, valor do documento)
- Flags de controle de envio (email_enviado, whatsapp_enviado)

### `historico_envios`
Tabela para registrar o histórico de envios de emails e WhatsApp.

**Campos:**
- Referência à conta a receber
- Tipo de envio (email ou whatsapp)
- Status do envio
- Data e hora do envio
- Mensagens de erro (se houver)

### `configuracao_sistema`
Tabela para configurações gerais do sistema.

## Variáveis de Ambiente

Adicione as seguintes variáveis ao seu arquivo `.env`:

```bash
# MySQL Configuration
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_DATABASE=contas_receber
MYSQL_USER=apiuser
MYSQL_PASSWORD=apipassword
MYSQL_PORT=3306
MYSQL_HOST=mysql
```

## Como Usar

1. O script SQL será executado automaticamente quando o container MySQL for iniciado pela primeira vez.
2. Os scripts em `init/` são executados em ordem alfabética.
3. O volume `mysql_data` persiste os dados mesmo após parar o container.

## Conectando ao Banco

Para conectar ao banco de dados a partir do host:

```bash
mysql -h localhost -P 3306 -u apiuser -p contas_receber
```

Ou usando o Docker:

```bash
docker exec -it mysql_db mysql -u apiuser -p contas_receber
```

## Backup e Restore

### Backup
```bash
docker exec mysql_db mysqldump -u apiuser -p contas_receber > backup.sql
```

### Restore
```bash
docker exec -i mysql_db mysql -u apiuser -p contas_receber < backup.sql
```

