# CRM ETS — Escuela Técnica Superior Kinal

Repositorio de addons personalizados de **Odoo 18** para el CRM de la Escuela Técnica Superior (ETS) de Fundación Kinal. El módulo principal es `ets_inscripcion`: formulario público de inscripción ligado a oportunidades (`crm.lead`).

## Flujo de negocio

1. El interesado entra a `/formulario-principal`, elige ETS o TIC en el modal y envía datos personales/carrera.
2. Se crea el lead (`x_area`, etapa **Nuevo** o **Nuevo TIC**) y un `x_token` UUID.
3. Se envía el correo `mail_template_inscripcion` con el enlace `/carreras-tecnicas?token=<x_token>`.
4. Completa el segundo formulario en 4 pasos (mismos campos; TCU ISTMO solo si el área es ETS).
5. El POST `/carreras-tecnicas/submit` actualiza el mismo lead y marca `x_formulario_completo`.
6. Redirect a `/contactus-thank-you`.

Campos de Studio que **no** define este addon pero el formulario y el correo sí leen: `x_trabajadorQueAtendio`, `x_CarreraISTMO`, `x_CarreraTecnica`. No los elimines ni los renombres sin actualizar plantillas.

## Estructura

```
addons/ets_inscripcion/   # addon Odoo 18 (crm + website)
config/odoo18.conf        # ejemplo de configuración del servidor
db/crmets.sql             # dump PostgreSQL de referencia (grande; no es el entorno de desarrollo diario)
```

## Requisitos

- Odoo 18
- PostgreSQL (el dump de referencia es 16.x)
- Módulos base: `crm`, `website`

## Instalación local

1. Clonar este repositorio.
2. Añadir `addons/` al `addons_path` de Odoo (junto a los addons oficiales).
3. Copiar `config/odoo18.conf` y rellenar `admin_passwd` y `db_password`. **No commitear secretos.**
4. Actualizar la lista de aplicaciones e instalar **ETS Inscripción**.
5. Comprobar:
   - formulario: `http://localhost:8069/carreras-tecnicas?token=<token-de-un-lead>`
   - plantilla de correo en Ajustes → Técnico → Plantillas de correo: *Correo proceso inscripción*

Tras cambios en Python o XML: actualizar el módulo (`-u ets_inscripcion`) y recargar.

## Rutas HTTP

| Ruta | Auth | Método | Rol |
|------|------|--------|-----|
| `/formulario-principal` | public | GET | Modal ETS/TIC y formulario inicial. `?area=ets` o `?area=tic` omite el modal. |
| `/formulario-principal/submit` | public | POST + CSRF | Crea el lead (`x_area`, etapa, token). Catálogo inválido → redirect. |
| `/carreras-tecnicas` | public | GET | Segundo formulario. Token inválido → 404. Sin token → formulario vacío (el submit no persiste). |
| `/carreras-tecnicas/submit` | public | POST + CSRF | Escribe el lead identificado por `token`. |

El controlador usa `sudo()` porque es un flujo público. Cualquier campo nuevo que se escriba desde el POST debe validarse (longitud, catálogo, fecha no futura).

## Convenciones de campos

Prefijo `x_` para campos propios del lead. Selecciones usan claves en minúsculas (`matutina`, `primer_ingreso`, `compañero_trabajo`). Validaciones de formato (CUI/DPI 13 dígitos, teléfono GT 8 dígitos, NIT) viven en el JS del QWeb; el servidor debe seguir siendo la fuente de verdad para datos críticos.

## Git

No se trabaja en `main`. Tickets `ETS-XXX`, rama, PR squash: [docs/GITHUB-WORKFLOW.md](docs/GITHUB-WORKFLOW.md) y [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md).

```bash
pnpm install   # Husky (pre-commit / commit-msg)
pnpm lint      # Python compileall + XML
```

## Documentación para agentes

- [AGENTS.md](AGENTS.md) — contexto persistente para Cursor y otros agentes.
- `.cursor/rules/` — reglas por tipo de archivo.
- `.cursor/skills/` — addon Odoo, formulario de inscripción, workflow Git.
