#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if ! command -v uv >/dev/null 2>&1; then
  echo 'Install uv 0.13.1 first: https://docs.astral.sh/uv/getting-started/installation/' >&2
  exit 2
fi
uv sync --locked --all-packages
uv run --locked kit doctor
