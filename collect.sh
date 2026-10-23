#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
PYTHON_BIN=python3
if [[ -x .venv/bin/python ]]; then PYTHON_BIN=.venv/bin/python; fi
exec "$PYTHON_BIN" campaign.py --collect
