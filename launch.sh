#!/usr/bin/env bash
# Launch the web application inside Docker (see README "launch & visit the web application")
set -euo pipefail

PORT=8000
URL="http://localhost:${PORT}/docs/"
MAX_ATTEMPTS=120

open_browser() {
  local ret=1
  if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$URL" >/dev/null 2>&1 || :
    ret=0
  elif command -v open >/dev/null 2>&1; then
    open "$URL" >/dev/null 2>&1 || :
    ret=0
  elif command -v wslview >/dev/null 2>&1; then
    wslview "$URL" >/dev/null 2>&1 || :
    ret=0
  fi
  return "$ret"
}

open_browser_when_ready() {
  local i
  for ((i = 0; i < MAX_ATTEMPTS; i++)); do
    if (echo > /dev/tcp/localhost/"$PORT") 2>/dev/null; then
      if ! open_browser; then
        echo "Server ready at ${URL} (no browser command found — open it manually)"
      fi
      break
    fi
    sleep 1
  done
}

cd "$(dirname "$0")" || exit 1
docker compose build

# Poll for the server in the background, then open the browser once it is up
open_browser_when_ready &
POLLER_PID=$!
trap 'kill "$POLLER_PID" 2>/dev/null || true' EXIT

# Run the server in the foreground (Ctrl+C stops it)
docker compose run --rm --publish "${PORT}:${PORT}" --entrypoint bash dev \
  -c "cd docs && npm ci && cd .. && python3 -m http.server ${PORT}"
