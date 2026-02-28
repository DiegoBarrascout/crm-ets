from odoo import http
from odoo.http import request

class EtsInscripcion(http.Controller):

    @http.route('/carreras-tecnicas', type='http', auth='public', website=True)
    def formulario_inscripcion(self, **kwargs):
        lead_id = kwargs.get('id')
        lead = None

        if lead_id:
            lead = request.env['crm.lead'].sudo().browse(int(lead_id))
            if not lead.exists():
                lead = None

        return request.render('ets_inscripcion.formulario_inscripcion', {
            'lead': lead,
        })

    @http.route('/carreras-tecnicas/submit', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def formulario_submit(self, **kwargs):
        lead_id = kwargs.get('lead_id')

        if not lead_id:
            return request.redirect('/contactus-thank-you')

        lead = request.env['crm.lead'].sudo().browse(int(lead_id))
        if not lead.exists():
            return request.redirect('/contactus-thank-you')

        lead.sudo().write({
            'x_whatsapp': kwargs.get('whatsapp'),
            'x_jornada': kwargs.get('jornada'),
            'x_edad_numero': int(kwargs.get('edad_numero') or 0),
            'x_edad': kwargs.get('edad'),
            'x_genero': kwargs.get('genero'),
            'x_alumno': kwargs.get('alumno'),
            'x_direccion_vivienda': kwargs.get('direccion_vivienda'),
            'x_departamento': kwargs.get('departamento'),
            'x_municipio': kwargs.get('municipio'),
            'x_como_se_entero': kwargs.get('como_se_entero'),
            'x_ultimo_grado': kwargs.get('ultimo_grado'),
            'x_empresa': kwargs.get('empresa'),
            'x_telefono_empresa': kwargs.get('telefono_empresa'),
            'x_puesto': kwargs.get('puesto'),
            'x_direccion_empresa': kwargs.get('direccion_empresa'),
            'x_empresa_paga': kwargs.get('empresa_paga'),
            'x_recibo_nombre': kwargs.get('recibo_nombre'),
            'x_nit': kwargs.get('nit'),
            'x_posee_vehiculo': kwargs.get('posee_vehiculo'),
            'x_acepta_condiciones': True if kwargs.get('acepta_condiciones') else False,
            'x_formulario_completo': True,
        })

        return request.redirect('/contactus-thank-you')
