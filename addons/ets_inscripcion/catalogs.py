"""Catálogos del formulario principal. Valores = claves Studio (dump producción).

TIC: listas vacías a propósito hasta que Admisiones entregue opciones.
"""

# (value, label) — value se guarda en x_CarreraISTMO / x_CarreraTecnica / x_trabajadorQueAtendio

TCU_ETS = [
    ('Técnico Universitario (1er. año Carrera Técnica)', 'Técnico Universitario (1er. año Carrera Técnica)'),
    ('Técnico Universitario (2do. año Carrera Técnica)', 'Técnico Universitario (2do. año Carrera Técnica)'),
    ('Técnico Universitario (3er. año) AÑO ACADÉMICO', 'Técnico Universitario (3er. año) AÑO ACADÉMICO'),
    ('Egresado del Centro Educativo', 'Egresado del Centro Educativo'),
    ('Estudiante del Centro Educativo', 'Estudiante del Centro Educativo'),
    ('NO', 'No'),
]

CARRERAS_ETS = [
    ('Topografía', 'Topografía'),
    ('Autodesk AutoCAD 2D & 3D', 'Autodesk AutoCAD 2D & 3D'),
    ('Autodesk Revit Architecture', 'Autodesk Revit Architecture'),
    ('Autodesk Revit Structure & MEP', 'Autodesk Revit Structure & MEP'),
    ('Calderas de Vapor', 'Calderas de Vapor'),
    ('Mecanismos del Automóvil (1er. año de Mecánica Automotriz)', 'Mecanismos del Automóvil (1er. año de Mecánica Automotriz)'),
    ('Mecánica de Motores Gasolina (2do. año de Mecánica Automotriz)', 'Mecánica de Motores Gasolina (2do. año de Mecánica Automotriz)'),
    ('Instalaciones Eléctricas Generales (1er. año de Electricidad Industrial)', 'Instalaciones Eléctricas Generales (1er. año de Electricidad Industrial)'),
    ('Controles y Máquinas Eléctricas (2do. año de Electricidad Industrial)', 'Controles y Máquinas Eléctricas (2do. año de Electricidad Industrial)'),
    ('Electrónica Industrial Analógica (1er. año de Electrónica Industrial)', 'Electrónica Industrial Analógica (1er. año de Electrónica Industrial)'),
    ('Control Industrial y Sistemas programables (2do. año de Electrónica Industrial)', 'Control Industrial y Sistemas programables (2do. año de Electrónica Industrial)'),
    ('Fundamentos de la Construcción (1er. año Técnico en Construcción)', 'Fundamentos de la Construcción (1er. año Técnico en Construcción)'),
    ('Administración de Obras (2do. año Técnico en Construcción)', 'Administración de Obras (2do. año Técnico en Construcción)'),
    ('Electromecánica Automotriz', 'Electromecánica Automotriz'),
    ('Especialistas en Tecnologías Industrial', 'Especialistas en Tecnologías Industrial'),
    ('Inyección Electrónica Automotriz', 'Inyección Electrónica Automotriz'),
    ('Mantenimiento Mecánico Industrial', 'Mantenimiento Mecánico Industrial'),
    ('Mecánica de Motocicletas', 'Mecánica de Motocicletas'),
    ('Refrigeración Industrial y Aire Acondicionado', 'Refrigeración Industrial y Aire Acondicionado'),
    ('Soldadura Industrial', 'Soldadura Industrial'),
    ('Aire Acondicionado Automotriz', 'Aire Acondicionado Automotriz'),
    ('Soldadura Industrial TIG', 'Soldadura Industrial TIG'),
    ('Certificación Nacional Técnico Frigorista', 'Certificación Nacional Técnico Frigorista'),
    ('Automatización Industrial', 'Automatización Industrial'),
    ('Electromecánica Viernes', 'Electromecánica Viernes'),
]

TRABAJADORES_ETS = [
    ('Manuel Barrientos', 'Manuel Barrientos'),
    ('Ruben Rivera', 'Ruben Rivera'),
    ('William Francisco', 'William Francisco'),
    ('José Chaj', 'José Chaj'),
    ('Antonio Escobar', 'Antonio Escobar'),
]

# Rellenar cuando Admisiones entregue el catálogo TIC (mismos campos, otras opciones).
TCU_TIC = []
CARRERAS_TIC = []
TRABAJADORES_TIC = []

TITULOS = {
    'ets': 'Datos Personales — Escuela Técnica Superior',
    'tic': 'Datos Personales — TIC',
}


def for_area(area):
    if area == 'tic':
        return {
            'area': 'tic',
            'titulo': TITULOS['tic'],
            'tcu': TCU_TIC,
            'carreras': CARRERAS_TIC,
            'trabajadores': TRABAJADORES_TIC,
            'catalogo_listo': bool(TCU_TIC and CARRERAS_TIC and TRABAJADORES_TIC),
        }
    return {
        'area': 'ets',
        'titulo': TITULOS['ets'],
        'tcu': TCU_ETS,
        'carreras': CARRERAS_ETS,
        'trabajadores': TRABAJADORES_ETS,
        'catalogo_listo': True,
    }


def value_allowed(options, value):
    return value in {v for v, _label in options}
