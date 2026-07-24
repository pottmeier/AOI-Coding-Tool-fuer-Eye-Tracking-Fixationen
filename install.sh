#!/usr/bin/env bash
set -euo pipefail

echo "=== AOI Coding Tool — Installation ==="

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Fertig. Starten mit:"
echo "  source .venv/bin/activate"
echo "  python main.py video.mp4 fixationen.csv"
