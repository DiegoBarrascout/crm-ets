---
name: odoo-addon-ets
description: Develop, install, and update the Odoo 18 addon ets_inscripcion in this repo. Use when adding models, views, security, installing the module, changing __manifest__.py, or working with addons_path / -u ets_inscripcion.
---

# Addon Odoo 18 — ets_inscripcion

## Layout

```
addons/ets_inscripcion/
  __init__.py / catalogs.py / guatemala.py
  __manifest__.py      # license Other proprietary; author Fundación Kinal
  models/crm_lead.py, crm_stage.py, mail_inscripcion.py
  controllers/main.py
  views/crm_lead_views.xml, formulario_principal.xml
  views/inscripcion_templates.xml, mail_templates.xml
```

Nuevos XML van en `data` del manifiesto, en orden de dependencia (vistas backend antes que QWeb si hay refs).

## Checklist al cambiar el módulo

1. `__manifest__.py` version bump solo si el equipo lo pide; por defecto deja `1.0`.
2. Importar nuevos Python en el `__init__.py` del paquete.
3. No añadir `security/ir.model.access.csv` para inherit de `crm.lead` salvo modelos nuevos.
4. Probar con `-u ets_inscripcion` contra una base que ya tenga `crm` y `website`.
5. Si creas un modelo nuevo: ACL + menú + views.

## Comandos típicos (ajustar paths locales)

```bash
# actualizar módulo
python3 odoo-bin -c /ruta/odoo18.conf -d NOMBRE_BD -u ets_inscripcion --stop-after-init
```

`addons_path` debe incluir este `addons/` (el `config/odoo18.conf` de ejemplo apunta a `/opt/odoo18/...`; en local cámbialo, no lo dejes hardcoded en código).

## Qué no hacer

- No instalar dependencias pip extra salvo que Odoo las necesite.
- No versionar `__pycache__`, logs ni `.env`.
- No copiar addons oficiales al repo.

Para el formulario público, token y correo, usa el skill `ets-inscripcion-form`.
