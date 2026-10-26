# Flujo de trabajo en GitHub — CRM ETS

Repositorio: [DiegoBarrascout/crm-ets](https://github.com/DiegoBarrascout/crm-ets.git)

Mismo esquema que Echovate Nexo (`NX-XXX`) y Criterio (`AUTO-XXX`), con prefijo **ETS**.

| Elemento  | Formato                                  |
| --------- | ---------------------------------------- |
| ID visible | `ETS-XXX` (3 dígitos)                   |
| Issue     | `[ETS-012] Título`                       |
| Rama      | `ETS-012-slug-corto`                     |
| Commit    | `feat(ETS-012): …` (Conventional Commits)|
| PR        | `[ETS-012] …` + `Closes #N`              |
| Merge     | squash + borrar rama                     |
| Principal | `main` (solo por PR)                     |

GitHub usa `#N` internamente; **ETS-XXX** es la referencia del backlog. La rama por defecto de este repo ya es `main` (en Nexo es `master`): no la renombres.

## Nunca trabajar sobre `main`

`main` solo recibe PR mergeados. Antes de editar: rama `ETS-XXX-slug-corto`.

Si el trabajo empezó por error en `main` y **no se ha publicado**:

```bash
git switch -c ETS-012-slug-corto
```

No uses `git reset --hard` para “arreglarlo”.

## Flujo diario

### 1. Issue

```bash
gh issue list --state all --limit 5 --json number,title
gh issue create \
  --title "[ETS-012] Título" \
  --body "$(cat <<'EOF'
## Objetivo
...

## Criterios de aceptación
- [ ] ...
EOF
)" \
  --label feature
```

El número `ETS-XXX` es incremental en el título. Consulta el último issue antes de crear uno. El `#N` de GitHub puede no coincidir con `XXX` si hay issues previos sin prefijo.

### 2. Rama

```bash
git switch main
git pull --ff-only origin main
git switch -c ETS-012-slug-corto
```

### 3. Validar

Una vez por clone: `pnpm install` (activa Husky). El `pre-commit` corre `pnpm lint` (`scripts/check-addon.sh`: compileall, XML, `git diff --check`). El `commit-msg` exige `tipo(ETS-XXX): …`.

```bash
pnpm lint
```

Tras XML/Python del addon: actualizar `ets_inscripcion` en Odoo (`-u ets_inscripcion`) y probar el flujo del ticket.

No uses `--no-verify` en commits.

### 4. Commit

```bash
git commit -m "feat(ETS-012): describe el porqué"
```

Sin `.env`, secretos, dumps nuevos ni cambios ajenos al issue.

### 5. Push y PR

```bash
git push -u origin ETS-012-slug-corto
gh pr create \
  --title "[ETS-012] Título" \
  --body "$(cat <<'EOF'
## Cambios
- ...

## Validación
- python3 -m compileall -q addons
- flujo Odoo del ticket

Closes #12
EOF
)"
```

Push y merge solo con autorización explícita del usuario.

### 6. Merge

El dueño revisa. Estrategia: **squash**.

```bash
gh pr checks <n>
gh pr merge <n> --squash --delete-branch
git switch main
git pull --ff-only origin main
```

## Labels

`epic`, `feature`, `task`, `bug`, `documentation`, `security`.

Bootstrap (idempotente):

```bash
./scripts/github-bootstrap.sh
```

## Convenciones

- Tickets y PRs en español.
- Un issue ≈ un PR.
- Agentes: no pushear a `main`, no force-push a `main`, no `--no-verify`.
