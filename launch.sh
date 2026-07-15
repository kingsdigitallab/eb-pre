#!/usr/bin/env bash
# Launch the web application inside Docker (see README "launch & visit the web application")
set -euo pipefail
cd "$(dirname "$0")" || exit 1
docker compose build
docker compose run --rm --publish 8000:8000 --entrypoint bash dev -c "cd docs && npm ci && cd .. && python3 -m http.server 8000"
