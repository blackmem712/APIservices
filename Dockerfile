# syntax=docker/dockerfile:1.7-labs

############################
# Builder stage
############################
FROM python:3.12-slim AS builder

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependências de sistema mínimas para compilar algumas wheels (psycopg2, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential gcc libc6-dev libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Se você usa requirements.txt:
COPY requirements.txt ./requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# (Se usar Poetry, veja nota no fim.)

############################
# Runtime stage
############################
FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Usuário não-root
RUN useradd -m appuser

# Utilitário leve (para healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Bibliotecas instaladas no builder
COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=builder /usr/local/bin /usr/local/bin

# Copie seu código (ajuste paths conforme seu repo)
# Se o seu código está todo na raiz, use: COPY . /app
# Aqui, assumimos que o pacote/código está em ./app
COPY app ./app
COPY README.md ./README.md

# Porta padrão do serviço
EXPOSE 8000

# Módulo ASGI (ajuste se necessário)
ENV APP_MODULE=app.main:app

# Processo em produção: gunicorn + uvicorn worker
USER appuser
CMD ["bash", "-lc", "exec gunicorn --workers=2 --threads=4 --timeout=60 -k uvicorn.workers.UvicornWorker \"$APP_MODULE\" --bind 0.0.0.0:8000"]
