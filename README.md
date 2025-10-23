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
5. No servidor/orquestrador, executar `docker pull`, definir variaveis (`API_ENVIRONMENT=production`, `API_DEBUG=false`) e iniciar o container como serviço.
6. Colocar um proxy reverso (NGINX, Traefik ou load balancer do provedor) para HTTPS, roteamento e observabilidade.
7. Configurar logs centralizados, monitoramento (Prometheus, CloudWatch) e health checks (`GET /api/services` ou endpoint dedicado).
