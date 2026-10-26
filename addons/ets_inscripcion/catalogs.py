"""Catálogos del formulario principal.

ETS: valores Studio (dump). TIC: mismo TCU; curso técnico y trabajadores del form actual.
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

# TCU idéntico a ETS. Curso técnico y trabajadores: formulario TIC actual (Forms).
TCU_TIC = list(TCU_ETS)
CARRERAS_TIC = [
    ('Analista jr en Ciberseguridad', 'Analista jr en Ciberseguridad'),
    ('Arquitectura y Operación de Sistemas basados en la nube (AWS)', 'Arquitectura y Operación de Sistemas basados en la nube (AWS)'),
    ('Técnico en redes e internet CCNA', 'Técnico en redes e internet CCNA'),
    ('Profesional en redes e internet CCNP', 'Profesional en redes e internet CCNP'),
    ('Desarrollo Avanzado: Integración de modelos GPT y servicios de IA', 'Desarrollo Avanzado: Integración de modelos GPT y servicios de IA'),
    ('Especialista en Gestión de Servicios IT', 'Especialista en Gestión de Servicios IT'),
    ('Desarrollador Fullstack JAVA', 'Desarrollador Fullstack JAVA'),
    ('Desarrollador Fullstack .NET', 'Desarrollador Fullstack .NET'),
    ('Fundamentos base de datos SQL', 'Fundamentos base de datos SQL'),
    ('Fundamentos de programación Java', 'Fundamentos de programación Java'),
    ('Fundamentos de Python', 'Fundamentos de Python'),
    ('Introducción Profesional a la Administración de Base de Datos', 'Introducción Profesional a la Administración de Base de Datos'),
    ('IT Essentials', 'IT Essentials'),
    ('Java Backend Essentials: Bases Solidas para el Desarrollo Fullstack', 'Java Backend Essentials: Bases Solidas para el Desarrollo Fullstack'),
    ('Python Avanzado', 'Python Avanzado'),
    ('Otras', 'Otras'),
]
TRABAJADORES_TIC = [
    ('Rolando Escot', 'Rolando Escot'),
    ('Pablo Ruiz', 'Pablo Ruiz'),
]

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
            'label_carrera': 'Curso Técnico',
            'catalogo_listo': True,
        }
    return {
        'area': 'ets',
        'titulo': TITULOS['ets'],
        'tcu': TCU_ETS,
        'carreras': CARRERAS_ETS,
        'trabajadores': TRABAJADORES_ETS,
        'label_carrera': 'Carrera Técnica a la que se inscribe',
        'catalogo_listo': True,
    }


def value_allowed(options, value):
    return value in {v for v, _label in options}
