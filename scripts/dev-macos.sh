#!/usr/bin/env bash
# Start MongoDB (if needed), FastAPI, and the React dev server (macOS).
# Usage: from repo root: ./scripts/dev-macos.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

MONGO_PID=""
UVICORN_PID=""

cleanup() {
  if [[ -n "${UVICORN_PID:-}" ]]; then
    kill "$UVICORN_PID" 2>/dev/null || true
    wait "$UVICORN_PID" 2>/dev/null || true
  fi
  if [[ -n "${MONGO_PID:-}" ]]; then
    kill "$MONGO_PID" 2>/dev/null || true
    wait "$MONGO_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

port_listening() {
  local port="$1"
  lsof -iTCP:"$port" -sTCP:LISTEN -Pn >/dev/null 2>&1
}

if [[ "${SKIP_MONGO:-}" == "1" ]]; then
  echo "SKIP_MONGO=1: not starting mongod (using existing MongoDB)."
elif port_listening 27017; then
  echo "Port 27017 already in use — assuming MongoDB is running."
else
  mkdir -p "${MONGO_DATA:-$HOME/mongodb-data}"
  if ! command -v mongod >/dev/null 2>&1; then
    echo "mongod not found in PATH. Install MongoDB or set SKIP_MONGO=1 if MongoDB runs elsewhere." >&2
    exit 1
  fi
  echo "Starting MongoDB (dbpath ${MONGO_DATA:-$HOME/mongodb-data})..."
  mongod --dbpath "${MONGO_DATA:-$HOME/mongodb-data}" &
  MONGO_PID=$!
  sleep 2
fi

if [[ ! -f "$ROOT/.venv/bin/activate" ]]; then
  echo "Missing .venv. Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt" >&2
  exit 1
fi

# shellcheck source=/dev/null
source "$ROOT/.venv/bin/activate"

echo "Starting FastAPI (uvicorn)..."
cd "$ROOT"
export PYTHONPATH=src
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 &
UVICORN_PID=$!
sleep 1

if [[ ! -d "$ROOT/frontend/node_modules" ]]; then
  echo "Installing frontend dependencies (first run)..."
  ( cd "$ROOT/frontend" && npm install )
fi

echo "Starting React (npm start). Press Ctrl+C to stop all services."
cd "$ROOT/frontend"
npm start
