#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"
python3 -m compileall -q addons
python3 scripts/check-xml.py
git diff --check
git diff --cached --check
