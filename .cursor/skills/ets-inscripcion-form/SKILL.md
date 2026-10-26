---
name: ets-inscripcion-form
description: Change the public ETS enrollment wizard, token lookup, POST mapping, client validations, or the inscription mail template. Use when editing /carreras-tecnicas, inscripcion_templates.xml, mail_templates.xml, x_token, CUI, DPI, TCU, or crm.lead inscription fields.
---

# Formulario de inscripción ETS

## Archivos juntos

Cualquier campo nuevo exige los tres (o cuatro) sitios:

| Sitio | Archivo |
|-------|---------|
| Modelo | `addons/ets_inscripcion/models/crm_lead.py` |
| CRM | `views/crm_lead_views.xml` si debe verse en backend |
| Form QWeb + JS | `views/inscripcion_templates.xml` |
| Persistencia | `controllers/main.py` → dict `vals` |

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

JS relevante: `nextStep`, `verificarCondiciones`, `actualizarEdad`, `toggleCarne`, `toggleRecomendante`, `toggleVehiculo`. Indicadores `#ind-1`…`#ind-4`, color activo `#008f8c`.

## Mapping POST → lead

Además de `x_*`, el submit puede:

- `phone` ← `telefono`
- `name` ← `nombre_alumno` (si no vacío)
- `x_formulario_completo` = True
- `x_acepta_condiciones` = checkbox presente
- `x_fecha_inscripcion` parseada con `date.fromisoformat`; futuras → hoy

## Studio (solo lectura en QWeb)

`x_trabajadorQueAtendio`, `x_CarreraISTMO`, `x_CarreraTecnica`. TCU extra se muestra si `x_CarreraISTMO` tiene valor distinto de `NO`.

## Tras el cambio

Actualizar módulo. Probar GET con token real, validaciones de cada paso, POST y lead en CRM (pestaña Datos de Inscripción).
