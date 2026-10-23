#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
PYTHON_BIN=python3
if ! "$PYTHON_BIN" -c 'import sys; assert sys.version_info >= (3,10)' 2>/dev/null; then
  echo "Python 3.10 or newer is required." >&2; exit 1
fi
if ! "$PYTHON_BIN" -m venv .venv; then
  echo "Install Ubuntu's venv support, then rerun:" >&2
  echo "  sudo apt update && sudo apt install python3-venv" >&2
  exit 1
fi
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip freeze > installed_versions.txt
.venv/bin/python campaign.py --preflight
echo
echo "Ready. Run: bash run.sh --hours 8"
