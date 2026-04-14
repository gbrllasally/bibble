#!/usr/bin/env bash
set -euo pipefail

echo "[render_build] working directory: $(pwd)"
echo "[render_build] python: $(python --version 2>&1 || true)"

if [[ ! -f requirements.txt ]]; then
  echo "[render_build][ERROR] requirements.txt not found in $(pwd)"
  echo "[render_build][HINT] In Render settings, Root Directory should be empty or '.'"
  exit 1
fi

if [[ "${DRY_RUN:-0}" == "1" ]]; then
  echo "[render_build] DRY_RUN=1 set; skipping pip install"
  exit 0
fi

pip install -r requirements.txt
