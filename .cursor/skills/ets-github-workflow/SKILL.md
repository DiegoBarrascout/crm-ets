---
name: ets-github-workflow
description: Issues ETS-XXX, ramas, commits conventional y PRs squash hacia main. Use when creating issues, branches, pull requests, or when the user mentions GitHub workflow, tickets, or Echovate-style git.
---

# Workflow GitHub CRM ETS

Fuente: `docs/GITHUB-WORKFLOW.md`.

- Issue `[ETS-018] …` (GitHub `#N`)
- Rama `ETS-018-slug` desde `main` actualizado — **nunca trabajar en `main`**
- Commit `feat(ETS-018): …`
- PR `[ETS-018] …` + `Closes #N`
- Squash merge; `git pull --ff-only origin main`
- Husky: `pnpm install` una vez. pre-commit → `pnpm lint`. commit-msg → `tipo(ETS-XXX): …`. No `--no-verify`.
- `gh` para issues/PRs. Si `gh auth status` falla: pedir `gh auth login`. Nunca pedir PAT.
- Push y merge solo con autorización del usuario
- Si el trabajo empezó en `main` y no está pusheado: `git switch -c ETS-018-slug`

Bootstrap de labels: `./scripts/github-bootstrap.sh`.
