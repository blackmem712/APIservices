#!/usr/bin/env bash
set -euo pipefail

# ===== Configs (podem ser exportadas antes de rodar) =====
GIT_REPO="${GIT_REPO:-git@github.com:blackmem712/APIservices.git}"
BRANCH="${BRANCH:-main}"
APP_DIR="${APP_DIR:-/opt/apiservices}"
PORT_API="${PORT_API:-8000}"
PORT_WAHA="${PORT_WAHA:-3000}"

echo ">> Repositório: $GIT_REPO"
echo ">> Branch.....: $BRANCH"
echo ">> App dir....: $APP_DIR"

# 1) Pré-requisitos
command -v docker >/dev/null 2>&1 || { echo "Docker não encontrado"; exit 1; }
docker compose version >/dev/null 2>&1 || { echo "Docker Compose v2 não encontrado"; exit 1; }

# 2) Acesso SSH ao GitHub (garante known_hosts)
mkdir -p ~/.ssh
chmod 700 ~/.ssh
ssh -o StrictHostKeyChecking=accept-new -T git@github.com || true

# 3) Clona ou atualiza
if [[ ! -d "$APP_DIR/.git" ]]; then
  echo ">> Clonando repositório em $APP_DIR"
  sudo mkdir -p "$APP_DIR"
  sudo chown -R "$USER":"$USER" "$APP_DIR"
  git clone "$GIT_REPO" "$APP_DIR"
fi

cd "$APP_DIR"
echo ">> Atualizando branch $BRANCH"
git fetch --all --prune
git checkout "$BRANCH"
git pull --ff-only origin "$BRANCH"

# 4) .env
if [[ ! -f ".env" ]]; then
  if [[ -f ".env.example" ]]; then
    echo ">> Criando .env a partir de .env.example (ajuste depois se precisar)"
    cp .env.example .env
  else
    echo ">> AVISO: .env não existe e .env.example não encontrado. Configure manualmente."
  fi
fi

# 5) Subir (build + up)
echo ">> Subindo containers com docker compose"
docker compose up -d --build

# 6) Status + dicas
echo
echo "====== STATUS ======"
docker compose ps

echo
echo "====== ENDPOINTS ======"
echo "API   -> http://SEU_IP:${PORT_API}/  (docs em /api/docs)"
echo "WAHA  -> http://SEU_IP:${PORT_WAHA}/  (login admin e QR Code)"
echo
echo ">> Logs iniciais (apiservices):"
docker logs --tail 50 apiservices || true

echo
echo ">> Logs iniciais (waha):"
docker logs --tail 50 waha || true
