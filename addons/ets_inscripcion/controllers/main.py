from odoo import http
from odoo.http import request
from datetime import date
from odoo.addons.ets_inscripcion import catalogs


def _studio_write(vals, field_name, value):
    if field_name in request.env['crm.lead']._fields and value:
        vals[field_name] = value


class EtsInscripcion(http.Controller):

    def _area(self, raw):
        return 'tic' if raw == 'tic' else 'ets' if raw == 'ets' else None

    def _stage_id(self, area):
        xmlid = 'ets_inscripcion.stage_nuevo_tic' if area == 'tic' else 'crm.stage_lead1'
        stage = request.env.ref(xmlid, raise_if_not_found=False)
        return stage.id if stage else False

    @http.route('/formulario-principal', type='http', auth='public', website=True)
    def formulario_principal(self, **kwargs):
        area = self._area(kwargs.get('area'))
        cat = catalogs.for_area(area) if area else catalogs.for_area('ets')
        return request.render('ets_inscripcion.formulario_principal', {
            'area': area,
            'cat': cat,
        })

    @http.route('/formulario-principal/submit', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def formulario_principal_submit(self, **kwargs):
        area = self._area(kwargs.get('area'))
        if not area:
            return request.redirect('/formulario-principal')

        cat = catalogs.for_area(area)
        if not cat['catalogo_listo']:
            return request.redirect('/formulario-principal?area=%s' % area)

        nombre = (kwargs.get('name') or '').strip()
        email = (kwargs.get('email_from') or '').strip()
        telefono = ''.join(c for c in (kwargs.get('phone') or '') if c.isdigit())[:8]
        tcu = kwargs.get('x_CarreraISTMO') or ''
        carrera = kwargs.get('x_CarreraTecnica') or ''
        trabajador = kwargs.get('x_trabajadorQueAtendio') or ''
        curso_otro = (kwargs.get('curso_otro') or '').strip() if carrera == 'Otras' else ''

        if (
            not nombre
            or not email
            or len(telefono) != 8
            or not catalogs.value_allowed(cat['tcu'], tcu)
            or not catalogs.value_allowed(cat['carreras'], carrera)
            or not catalogs.value_allowed(cat['trabajadores'], trabajador)
            or (carrera == 'Otras' and not curso_otro)
        ):
            return request.redirect('/formulario-principal?area=%s' % area)

        vals = {
            'name': nombre,
            'contact_name': nombre,
            'email_from': email,
            'phone': telefono,
            'type': 'opportunity',
            'x_area': area,
        }
        if area == 'tic' and curso_otro:
            vals['x_curso_otro'] = curso_otro
        stage_id = self._stage_id(area)
        if stage_id:
            vals['stage_id'] = stage_id
        _studio_write(vals, 'x_CarreraISTMO', tcu)
        _studio_write(vals, 'x_CarreraTecnica', carrera)
        _studio_write(vals, 'x_trabajadorQueAtendio', trabajador)

        request.env['crm.lead'].sudo().create(vals)
        return request.redirect('/contactus-thank-you')

    @http.route('/carreras-tecnicas', type='http', auth='public', website=True)
    def formulario_inscripcion(self, **kwargs):
        token = kwargs.get('token')
        lead = None

        if token:
            lead = request.env['crm.lead'].sudo().search([('x_token', '=', token)], limit=1)
            if not lead:
                return request.render('website.404')

        area = lead.x_area if lead and lead.x_area else 'ets'
        tcu_val = ''
        if lead and 'x_CarreraISTMO' in lead._fields:
            tcu_val = lead.x_CarreraISTMO or ''
        exige_tcu = area != 'tic' and bool(tcu_val) and tcu_val != 'NO'

        return request.render('ets_inscripcion.formulario_inscripcion', {
            'lead': lead,
            'es_tic': area == 'tic',
            'exige_tcu': exige_tcu,
        })

    @http.route('/carreras-tecnicas/submit', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def formulario_submit(self, **kwargs):
        token = kwargs.get('token')

        if not token:
            return request.redirect('/contactus-thank-you')

        lead = request.env['crm.lead'].sudo().search([('x_token', '=', token)], limit=1)
        if not lead:
            return request.redirect('/contactus-thank-you')

        fecha_str = kwargs.get('fecha_inscripcion')
        fecha = None
        if fecha_str:
            try:
                fecha = date.fromisoformat(fecha_str)
                if fecha > date.today():
                    fecha = date.today()
            except ValueError:
                fecha = date.today()

        nombre_alumno = kwargs.get('nombre_alumno', '').strip()

        vals = {
            'x_cui': kwargs.get('cui'),
            'x_whatsapp': kwargs.get('whatsapp'),
            'x_jornada': kwargs.get('jornada'),
            'x_fecha_inscripcion': fecha,
            'x_edad_numero': int(kwargs.get('edad_numero') or 0),
            'x_edad': kwargs.get('edad'),
            'x_genero': kwargs.get('genero'),
            'x_alumno': kwargs.get('alumno'),
            'x_carne': kwargs.get('carne'),
            'x_direccion_vivienda': kwargs.get('direccion_vivienda'),
            'x_departamento': kwargs.get('departamento'),
            'x_municipio': kwargs.get('municipio'),
            'x_como_se_entero': kwargs.get('como_se_entero'),
            'x_nombre_recomendante': kwargs.get('nombre_recomendante'),
            'x_parentesco': kwargs.get('parentesco'),
            'x_ultimo_grado': kwargs.get('ultimo_grado'),
            'x_empresa': kwargs.get('empresa'),
            'x_telefono_empresa': kwargs.get('telefono_empresa'),
            'x_puesto': kwargs.get('puesto'),
            'x_direccion_empresa': kwargs.get('direccion_empresa'),
            'x_empresa_paga': kwargs.get('empresa_paga'),
            'x_recibo_nombre': kwargs.get('recibo_nombre'),
            'x_nit': kwargs.get('nit'),
            'x_posee_vehiculo': kwargs.get('posee_vehiculo'),
            'x_tipo_vehiculo': kwargs.get('tipo_vehiculo'),
            'x_placa_vehiculo': kwargs.get('placa_vehiculo'),
            'x_carrera_tcu': kwargs.get('carrera_tcu'),
            'x_especialidad_tcu': kwargs.get('especialidad_tcu'),
            'x_nombre_alumno': nombre_alumno,
            'x_dpi': kwargs.get('dpi'),
            'x_acepta_condiciones': True if kwargs.get('acepta_condiciones') else False,
            'x_formulario_completo': True,
        }

        telefono = kwargs.get('telefono', '').strip()
        if telefono:
            vals['phone'] = telefono

        if nombre_alumno:
            vals['name'] = nombre_alumno

        lead.sudo().write(vals)

        return request.redirect('/contactus-thank-you')
