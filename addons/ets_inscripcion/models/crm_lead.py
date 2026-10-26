from odoo import models, fields, api
import uuid
from odoo.addons.ets_inscripcion import catalogs

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    x_token = fields.Char(string='Token de Inscripción', readonly=True, copy=False)
    x_cui = fields.Char(string='CUI')
    x_whatsapp = fields.Selection([('si', 'Sí'), ('no', 'No')], string='WhatsApp')
    x_jornada = fields.Selection([
        ('matutina', 'Matutina - sábados (08:00 a 12:30)'),
        ('vespertina', 'Vespertina - sábados (13:00 a 17:30)'),
    ], string='Jornada')
    x_fecha_inscripcion = fields.Date(string='Fecha de Inscripción')
    x_edad_numero = fields.Integer(string='Edad (en número)')
    x_edad = fields.Selection([('menor', 'Menor de edad'), ('mayor', 'Mayor de edad')], string='Edad')
    x_genero = fields.Selection([('masculino', 'Masculino'), ('femenino', 'Femenino')], string='Género')
    x_alumno = fields.Selection([('primer_ingreso', 'Primer Ingreso'), ('reingreso', 'Reingreso')], string='Alumno')
    x_carne = fields.Char(string='Número de Carné')
    x_direccion_vivienda = fields.Text(string='Dirección Vivienda')
    x_departamento = fields.Char(string='Departamento Regional')
    x_municipio = fields.Char(string='Municipio Regional')
    x_como_se_entero = fields.Selection([
        ('compañero_trabajo', 'Compañero de Trabajo'),
        ('familiar', 'Familiar'),
        ('conocido', 'De un Conocido'),
        ('exalumno_basicos', 'Soy Exalumno de Básicos'),
        ('exalumno_diversificado', 'Soy Exalumno de Diversificado'),
        ('alumno_basicos', 'Soy Alumno de Básicos'),
        ('alumno_diversificado', 'Soy Alumno de Diversificado'),
        ('empresa_familiar', 'Por la Empresa Familiar'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('otros', 'Otros'),
    ], string='¿Cómo se enteró de Kinal?')
    x_nombre_recomendante = fields.Char(string='Nombre del Recomendante')
    x_parentesco = fields.Char(string='Parentesco')
    x_ultimo_grado = fields.Char(string='Último Grado Aprobado')
    x_empresa = fields.Char(string='Empresa donde Labora')
    x_telefono_empresa = fields.Char(string='Teléfono de la Empresa')
    x_puesto = fields.Char(string='Puesto que Desempeña')
    x_direccion_empresa = fields.Char(string='Dirección de la Empresa')
    x_empresa_paga = fields.Selection([('si', 'Sí'), ('no', 'No'), ('parcial', 'Parcial')], string='¿La empresa le paga los estudios?')
    x_recibo_nombre = fields.Char(string='Emitir recibo a nombre de')
    x_nit = fields.Char(string='NIT')
    x_posee_vehiculo = fields.Selection([('si', 'Sí'), ('no', 'No')], string='Posee Vehículo')
    x_tipo_vehiculo = fields.Selection([('carro', 'Carro'), ('moto', 'Moto')], string='Tipo de Vehículo')
    x_placa_vehiculo = fields.Char(string='Placa del Vehículo')
    x_carrera_tcu = fields.Char(string='Carrera Técnica Universitaria')
    x_especialidad_tcu = fields.Char(string='Especialidad TCU')
    x_nombre_alumno = fields.Char(string='Nombre del Alumno')
    x_dpi = fields.Char(string='DPI')
    x_acepta_condiciones = fields.Boolean(string='Acepta Condiciones de Estudio')
    x_formulario_completo = fields.Boolean(string='Formulario Completo', default=False)
    x_area = fields.Selection(
        [('ets', 'ETS'), ('tic', 'TIC')],
        string='Área de interés',
        copy=False,
    )
    x_curso_otro = fields.Char(string='Otro curso técnico')
    x_vinculo_centro = fields.Selection(
        [
            ('egresado', 'Egresado del Centro Educativo'),
            ('estudiante', 'Estudiante actual del Centro Educativo'),
            ('ninguno', 'Ninguno de los anteriores'),
        ],
        string='Vínculo con el Centro Educativo',
    )

    @api.model
    def _ets_ensure_tic_selections(self):
        """Añade valores TIC a campos Studio (selection) si ya existen."""
        Field = self.env['ir.model.fields'].sudo()
        Selection = self.env['ir.model.fields.selection'].sudo()
        extras = {
            'x_CarreraTecnica': catalogs.all_course_values(),
            'x_trabajadorQueAtendio': [v for v, _l in catalogs.TRABAJADORES_ETS + catalogs.TRABAJADORES_TIC],
        }
        for fname, values in extras.items():
            field = Field.search([('model', '=', 'crm.lead'), ('name', '=', fname)], limit=1)
            if not field:
                continue
            existing = set(Selection.search([('field_id', '=', field.id)]).mapped('value'))
            seq = 200
            for val in values:
                if val in existing:
                    continue
                Selection.create({
                    'field_id': field.id,
                    'value': val,
                    'name': val,
                    'sequence': seq,
                })
                seq += 1

    @api.model
    def _ets_align_contact_menu(self):
        """Navbar Contáctanos debe ir al mismo destino que el CTA btn-primary."""
        menus = self.env['website.menu'].sudo().search([('url', '=', '/contactus')])
        if menus:
            menus.write({'url': '/formulario-principal'})

    @api.model
    def _ets_align_primary_color(self):
        tmpl = self.env.ref(
            'ets_inscripcion.mail_template_inscripcion', raise_if_not_found=False
        )
        if tmpl and tmpl.body_html and '#008f8c' in tmpl.body_html:
            tmpl.body_html = tmpl.body_html.replace('#008f8c', catalogs.COLOR_PRIMARY)

    @api.model
    def _ets_after_module_update(self):
        self.env['crm.stage']._ets_apply_stage_order()
        self._ets_ensure_tic_selections()
        self._ets_align_contact_menu()
        self._ets_align_primary_color()
        pages = self.env['website.page'].sudo().search([('url', '=', '/formulario-principal')])
        if pages:
            pages.write({'is_published': False})

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('x_token'):
                vals['x_token'] = str(uuid.uuid4())
        return super().create(vals_list)
