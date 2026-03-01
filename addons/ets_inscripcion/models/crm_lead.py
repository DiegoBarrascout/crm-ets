from odoo import models, fields, api
import uuid

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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('x_token'):
                vals['x_token'] = str(uuid.uuid4())
        return super().create(vals_list)
