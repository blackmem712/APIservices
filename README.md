# API Services

Base FastAPI para gerenciar servicos internos.

## Requisitos

- Python 3.10+
- Dependencias listadas em `requirements.txt`

## Configuracao local

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Aplicacao disponivel em `http://127.0.0.1:8000` com docs em `/api/docs`.

## Variaveis de ambiente (.env)

- O `docker-compose` e o `deploy.sh` leem um arquivo `.env` **na raiz do projeto** (mesmo nivel de `docker-compose.yml`).
- Use `app/.env` apenas como referencia/exemplo; copie seu conteudo para `.env` e ajuste os valores reais (tokens do WAHA, caminhos de planilha, etc).
- Esse arquivo ja esta listado no `.gitignore`, entao nao sera versionado.

## Documentacao (Swagger)

- Acesse `http://127.0.0.1:8000/api/docs` para o Swagger UI gerado automaticamente.
- O endpoint raiz (`/`) retorna links uteis para a documentacao e para o JSON `openapi`.
- Utilize a tag **services** para visualizar e testar o CRUD de servicos diretamente pelo Swagger.
- Utilize a tag **reminders** para acionar manualmente o job que le o XLSX e envia avisos de boleto por WhatsApp.

## Lembretes de boletos (WhatsApp + WAHA)

### Configuracao

Defina as variaveis abaixo no `.env` (ou direto no ambiente) para apontar para sua planilha e instancia WAHA:

```bash
API_BILLING_SHEET_PATH=/caminho/para/clientes.xlsx
API_REMINDER_DAYS_BEFORE_DUE="[3,1]"  # opcional, dias que geram alerta
API_WAHA_BASE_URL=https://seu-servidor-waha:3000
API_WAHA_API_TOKEN=seu-token-do-waha     # opcional
API_WAHA_DEFAULT_SENDER=5547999999999    # numero/dispositivo configurado no WAHA
API_WAHA_TIMEOUT_SECONDS=15              # opcional
```

A planilha deve conter pelo menos as colunas `cliente`, `telefone/whatsapp` e `vencimento` (nomes podem variar, o servico reconhece alias comuns). Outras colunas sao ignoradas.

### Endpoint

`POST /api/reminders/billing/run`

Payload aceito:

```jsonc
{
  "sheet_path": null,              // opcional: sobrescreve API_BILLING_SHEET_PATH
  "reference_date": "2025-10-24",  // opcional: data base; default = hoje
  "dry_run": false,                // true = apenas simula, nao envia
  "sender_whatsapp_number": null   // opcional: instancia especifica do WAHA
}
```

Resposta traz o resumo da execucao (linhas analisadas, quantos envios feitos) e o detalhamento de cada cliente que estava a 3 ou 1 dia do vencimento.

### Como agendar diariamente

1. Garanta que o WAHA esteja ativo e autenticado com o numero que enviara as mensagens.
2. No servidor/deploy, crie um script que chame o endpoint (ex.: `curl -X POST http://localhost:8000/api/reminders/billing/run`).
3. Agende o script usando `cron` (Linux) ou Task Scheduler (Windows) para o horario desejado.
4. Opcional: use `dry_run=true` em um primeiro disparo para validar a leitura da planilha sem enviar mensagens.

## Execucao com Docker

```bash
docker build -t apiservices .
docker run --rm -p 8000:8000 apiservices
```

Envios para producao podem definir variaveis de ambiente:

```bash
docker run --rm -p 8000:8000 -e API_ENVIRONMENT=production -e API_DEBUG=false apiservices
```

## Estrutura

- `app/core`: Configuracoes e utilitarios globais.
- `app/api`: Rotas organizadas por dominio.
- `app/models`: Modelos Pydantic compartilhados.
- `app/services`: Regras de negocio e camadas de servico.

## Proximos passos

- Adicionar persistencia real (PostgreSQL, Redis ou outro backend).
- Criar testes automatizados com `pytest`.
- Configurar Docker e pipeline de deploy quando estiver pronto para producao.

## Guia rapido para producao

1. Construir e testar localmente: `docker build -t apiservices:latest .` e validar com `docker run`.
2. Rodar seus testes (`pytest`) para garantir estabilidade antes de publicar.
3. Versionar a imagem: `docker tag apiservices:latest <seu-registro>/apiservices:0.1.0`.
4. Autenticar no registro (Docker Hub, ECR, etc.) e fazer push: `docker push <seu-registro>/apiservices:0.1.0`.
5. No servidor/orquestrador, executar `docker pull`, definir variaveis (`API_ENVIRONMENT=production`, `API_DEBUG=false`) e iniciar o container como servico.
6. Colocar um proxy reverso (NGINX, Traefik ou load balancer do provedor) para HTTPS, roteamento e observabilidade.
7. Configurar logs centralizados, monitoramento (Prometheus, CloudWatch) e health checks (`GET /api/services` ou endpoint dedicado).

## Deploy via script (VM + GitHub)

1. Copie o repositorio e o arquivo `deploy.sh` para a VM (ex.: `~/apiservices`).
2. Garanta que exista um `.env` com as variaveis desejadas (`API_ENVIRONMENT=production`, etc) e de permissao de execucao: `chmod +x deploy.sh`.
3. Sempre que quiser atualizar a partir do GitHub, rode:
   ```bash
   REPO_DIR=/home/ubuntu/apiservices \
   BRANCH=main \
   IMAGE_TAG=latest \
   ./deploy.sh
   ```
   Ajuste `IMAGE_TAG`, `PORT` ou `CONTAINER_NAME` se precisar.
4. O script faz `git pull`, constroi a imagem, derruba o container anterior e sobe outro com `--restart unless-stopped`. Consulte os logs com `sudo docker logs -f apiservices`.
