# AGENTS.md — CRM ETS (Odoo 18)

Este repositorio es un **addon custom de Odoo 18**, no un proyecto Node/Python genérico. El producto es el CRM de inscripción de la Escuela Técnica Superior Kinal.

## Qué tocar

- Código de producto: `addons/ets_inscripcion/`
- Config de ejemplo: `config/odoo18.conf` (placeholders; nunca credenciales reales)
- `db/crmets.sql` es un dump enorme de referencia. No lo edites. No lo uses como fuente de verdad del modelo: el modelo vive en Python/XML del addon.

## Stack y dependencias

- Odoo 18, Python 3 del runtime de Odoo
- Dependencias del módulo: `crm`, `website`
- UI pública: QWeb (`website.layout`) + JS inline en la plantilla
- Backend: inherit de `crm.lead` y vista formulario CRM

## Flujo que no debes romper

GET `/formulario-principal` (modal ETS/TIC) → POST crea `crm.lead` con `x_area` y etapa Nuevo o Nuevo TIC → `x_token` → correo con `?token=` → GET `/carreras-tecnicas` → POST `/carreras-tecnicas/submit` → `x_formulario_completo=True`.

Catálogos del primer form: `catalogs.py`. TIC vacío hasta que Admisiones entregue listas. No exigir TCU ISTMO si `x_area == tic`.

Campos Studio ajenos a este repo, leídos por QWeb/correo:

- `x_trabajadorQueAtendio`
- `x_CarreraISTMO`
- `x_CarreraTecnica`

Trátalos como API estable.

## Cómo trabajar

1. Cambios de modelo: `models/crm_lead.py` + vista `views/crm_lead_views.xml` si deben verse en CRM.
2. Cambios del formulario público: `views/inscripcion_templates.xml` **y** el mapping del POST en `controllers/main.py`.
3. Correo: `views/mail_templates.xml` (`noupdate="1"`: en bases ya instaladas hay que actualizar el registro a mano o con un script).
4. Tras XML/Python: `-u ets_inscripcion`.
5. No inventes un frontend SPA ni assets webpack; el JS del wizard está en la plantilla.

## Seguridad

- Rutas `auth='public'` + `sudo()`: solo escribir campos previstos, nunca `active`, `user_id`, `team_id`, ni HTML crudo.
- CSRF obligatorio en el POST.
- Token inválido en GET → 404. Token ausente/inválido en POST → redirect thank-you (no filtrar existencia).
- No loguear tokens ni PII (CUI, DPI, NIT).

## Git (estilo Echovate)

- **No trabajar en `main`.** Issue `[ETS-XXX]`, rama `ETS-XXX-slug`, commit `feat(ETS-XXX): …`, PR `[ETS-XXX] …` + `Closes #N`, squash.
- Si el trabajo empezó en `main` y no está en origin: `git switch -c ETS-XXX-slug`.
- Husky (como Nexo): `pnpm install` activa hooks. `pnpm lint` = compileall + XML. No `--no-verify`.
- Push, PR y merge solo con autorización. `gh auth login` si no hay sesión; nunca pedir PAT.
- Detalle: [docs/GITHUB-WORKFLOW.md](docs/GITHUB-WORKFLOW.md).

## Estilo

- Español en strings de usuario, claves de selection en snake_case ASCII salvo las que ya existen con tilde (`compañero_trabajo`). No las renombres: rompen datos y el JS.
- Heredar vistas con `xpath`; no reemplazar el form CRM entero.
- Commits conventional con el ID del ticket.

## Skills del proyecto

Lee y sigue `.cursor/skills/` cuando el usuario pida:

- desarrollar o instalar el addon (`odoo-addon-ets`)
- cambiar el formulario, validaciones, token o correo (`ets-inscripcion-form`)
- issues, ramas y PRs (`ets-github-workflow`)
