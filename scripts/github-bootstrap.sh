#!/usr/bin/env bash
# Labels ETS. Idempotente.
# Uso: ./scripts/github-bootstrap.sh
set -euo pipefail

REPO="${GITHUB_REPO:-DiegoBarrascout/crm-ets}"

echo "==> Repositorio: $REPO"

create_label() {
  gh label create "$1" --color "$2" --description "$3" --repo "$REPO" 2>/dev/null || true
}

echo "==> Labels"
create_label "epic" "6f42c1" "Épica"
create_label "feature" "a2eeef" "Nueva funcionalidad"
create_label "bug" "d73a4a" "Error"
create_label "task" "cfd3d7" "Tarea técnica"
create_label "documentation" "0075ca" "Docs"
create_label "security" "b60205" "Seguridad"

echo "==> Listo. Crea issues a mano con título [ETS-XXX] (ver docs/GITHUB-WORKFLOW.md)."
