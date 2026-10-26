{
    'name': 'ETS Inscripción',
    'version': '1.0',
    'summary': 'Módulo de inscripción Escuela Técnica Superior',
    'category': 'CRM',
    'author': 'Fundación Kinal',
    'license': 'Other proprietary',
    'depends': ['crm', 'website'],
    'data': [
        'data/crm_stage_data.xml',
        'views/crm_lead_views.xml',
        'views/formulario_principal.xml',
        'views/inscripcion_templates.xml',
        'views/mail_templates.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'auto_install': False,
}
