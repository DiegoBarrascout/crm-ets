# Contribución — CRM ETS

- Rama: `ETS-018-slug` (ver [GITHUB-WORKFLOW.md](./GITHUB-WORKFLOW.md)).
- Issues: `[ETS-018] …` en GitHub.
- PR: `[ETS-018] …` y `Closes #18`.
- Commits conventional: `feat(ETS-018): …`, `fix(ETS-018): …`, `docs(ETS-018): …`.
- No trabajar ni pushear en `main`.
- No commitear `config/odoo18.conf` con passwords reales, `.env` ni PII.

```bash
pnpm install   # una vez: Husky
git switch main && git pull --ff-only origin main
git switch -c ETS-018-slug
pnpm lint
```
