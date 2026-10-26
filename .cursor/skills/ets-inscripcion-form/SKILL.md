---
name: ets-inscripcion-form
description: Change the public ETS/TIC enrollment forms, token lookup, POST mapping, catalogs, stages, or the inscription mail template. Use when editing /formulario-principal, /carreras-tecnicas, catalogs.py, x_area, Nuevo TIC, CUI, DPI, TCU, or crm.lead inscription fields.
---

# Formulario de inscripción ETS

## Archivos juntos

Cualquier campo nuevo exige los tres (o cuatro) sitios:

| Sitio | Archivo |
|-------|---------|
| Modelo | `addons/ets_inscripcion/models/crm_lead.py` |
| CRM | `views/crm_lead_views.xml` si debe verse en backend |
| Form 1 | `views/formulario_principal.xml` + `catalogs.py` |
| Form 2 QWeb + JS | `views/inscripcion_templates.xml` |
| Persistencia | `controllers/main.py` |

Olvidar el controller deja el dato en el POST y no en el lead.

## Token

- Generado en `CrmLead.create` si falta.
- GET: `search([('x_token', '=', token)], limit=1)`; sin registro → `website.404`.
- POST: sin token o lead inexistente → `/contactus-thank-you` (no 500, no mensaje de “token inválido”).
- El correo arma `http://crm-ets.kinal.edu.gt:8069/carreras-tecnicas?token=` + `x_token`. Si cambias host, cambia `mail_templates.xml` y documenta que `noupdate="1"` no actualiza bases viejas.

## Pasos del wizard

1. Personales: teléfono, CUI, WhatsApp, jornada, TCU condicional
2. Adicional: edad, género, alumno/carné, depto/municipio, cómo se enteró, grado
3. Laboral + facturación + vehículo
4. Condiciones, fecha, nombre alumno, DPI → submit

JS relevante: `nextStep`, `verificarCondiciones`, `actualizarEdad`, `toggleCarne`, `toggleRecomendante`, `toggleVehiculo`. Indicadores `#ind-1`…`#ind-4`, color activo `#195190`. Geo: `#departamento` / `#municipio` desde `guatemala.py`. Confirmación TSU: `#tcu_confirm`, `#carrera_confirm`.

## Mapping POST → lead

Además de `x_*`, el submit puede:

- `phone` ← `telefono`
- `name` ← `nombre_alumno` (si no vacío)
- `x_formulario_completo` = True
- `x_acepta_condiciones` = checkbox presente
- `x_fecha_inscripcion` parseada con `date.fromisoformat`; futuras → hoy
- `x_jornada` incluye `entre_semana`
- `x_departamento` / `x_municipio` validados con `catalogs.geo_ok`
- Si cambian TSU/curso: escribe Studio `x_CarreraISTMO` / `x_CarreraTecnica` si existen en `_fields`

## Área y etapas

- `x_area`: `ets` \| `tic`. Etapa al crear: Nuevo (`crm.stage_lead1`) o Nuevo TIC (`ets_inscripcion.stage_nuevo_tic`). Enviar el correo de inscripción mueve a Información Enviada (`crm.stage_lead2`).
- Catálogos: `catalogs.py` (`COURSES_BY_TCU`, `JORNADAS`) y `guatemala.py`. Curso deshabilitado hasta TSU; año académico no pide curso. Imágenes en `static/src/img/`. Colaborador, no Trabajador.
- El segundo formulario confirma TSU y curso (editables). No pedir Carrera TCU ni Especialidad.
- Kanban CRM: `x_kanban_curso`, `x_kanban_detalle` (`views/crm_lead_views.xml`). Correo → etapa: `models/mail_inscripcion.py`.

## Studio (el primer form ya los escribe)

`x_trabajadorQueAtendio`, `x_CarreraISTMO`, `x_CarreraTecnica`. No redefinirlos en Python (conflicto con Studio). Escribir solo si existen en `_fields`.

## Tras el cambio

Actualizar módulo. Probar GET con token real, validaciones de cada paso, POST y lead en CRM (pestaña Datos de Inscripción).
