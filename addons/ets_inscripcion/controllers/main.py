from odoo import http
from odoo.http import request
from datetime import date

class EtsInscripcion(http.Controller):

    @http.route('/carreras-tecnicas', type='http', auth='public', website=True)
    def formulario_inscripcion(self, **kwargs):
        token = kwargs.get('token')
        lead = None

        if token:
            lead = request.env['crm.lead'].sudo().search([('x_token', '=', token)], limit=1)
            if not lead:
                return request.render('website.404')

        return request.render('ets_inscripcion.formulario_inscripcion', {
            'lead': lead,
        })

    @http.route('/carreras-tecnicas/submit', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def formulario_submit(self, **kwargs):
        token = kwargs.get('token')

        if not token:
            return request.redirect('/contactus-thank-you')

        lead = request.env['crm.lead'].sudo().search([('x_token', '=', token)], limit=1)
        if not lead:
            return request.redirect('/contactus-thank-you')

        # Validar fecha
        fecha_str = kwargs.get('fecha_inscripcion')
        fecha = None
        if fecha_str:
            try:
                fecha = date.fromisoformat(fecha_str)
                if fecha > date.today():
                    fecha = date.today()
            except ValueError:
                fecha = date.today()

        lead.sudo().write({
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
            'x_nombre_alumno': kwargs.get('nombre_alumno'),
            'x_dpi': kwargs.get('dpi'),
            'x_acepta_condiciones': True if kwargs.get('acepta_condiciones') else False,
            'x_formulario_completo': True,
        })

        return request.redirect('/contactus-thank-you')
