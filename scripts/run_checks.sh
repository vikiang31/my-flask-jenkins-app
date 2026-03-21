#!/usr/bin/env bash
set -euo pipefail

echo "Starting checks..."

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Running tests..."
pytest -v

echo "All checks passed."
