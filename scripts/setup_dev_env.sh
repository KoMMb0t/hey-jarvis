#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
PYTHON_BINARY=${PYTHON:-python3}

if ! command -v "$PYTHON_BINARY" >/dev/null 2>&1; then
  echo "Python interpreter '$PYTHON_BINARY' not found. Set PYTHON to your preferred Python executable." >&2
  exit 1
fi

cd "$PROJECT_ROOT"

VENV_DIR="$PROJECT_ROOT/.venv"
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment in $VENV_DIR"
  "$PYTHON_BINARY" -m venv "$VENV_DIR"
else
  echo "Virtual environment already exists at $VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo
echo "Development environment is ready. Activate it with:"
echo "  source .venv/bin/activate"
