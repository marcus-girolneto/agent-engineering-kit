#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [ ! -x .venv/bin/python ]; then
  echo 'Environment missing. Run ./scripts/setup.sh first.' >&2
  exit 2
fi
exec .venv/bin/python -m agent_kit.cli doctor
