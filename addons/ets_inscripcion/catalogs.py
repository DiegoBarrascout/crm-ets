"""Catálogos del formulario principal. Values = lo que se guarda en el lead."""

TCU_1ER = 'Técnico Universitario (1er. año Carrera Técnica)'
TCU_2DO = 'Técnico Universitario (2do. año Carrera Técnica)'
TCU_3ER = 'Técnico Universitario (3er. año) AÑO ACADÉMICO'
TCU_NO = 'NO'
OTRO = 'Otras'
VINCULO_EGRESADO = 'egresado'
VINCULO_ESTUDIANTE = 'estudiante'
VINCULO_NINGUNO = 'ninguno'
VINCULOS = [
    (VINCULO_EGRESADO, 'Egresado del Centro Educativo'),
    (VINCULO_ESTUDIANTE, 'Estudiante actual del Centro Educativo'),
    (VINCULO_NINGUNO, 'Ninguno de los anteriores'),
]

TCU_ETS = [
    (TCU_1ER, 'Técnico Superior Universitario (1er. año)'),
    (TCU_2DO, 'Técnico Superior Universitario (2do. año)'),
    (TCU_3ER, 'Técnico Superior Universitario (3er. año) AÑO ACADÉMICO'),
    (TCU_NO, 'No'),
]
TCU_TIC = list(TCU_ETS)

_OTRO = [(OTRO, 'Otro')]

CARRERAS_TIC_1ER = [
    ('Técnico en redes e internet CCNA', 'Técnico en redes e internet CCNA'),
    ('Desarrollador Fullstack JAVA', 'Desarrollador Fullstack JAVA'),
    ('Desarrollador Fullstack .NET', 'Desarrollador Fullstack .NET'),
] + _OTRO

CARRERAS_TIC_2DO = [
    ('Profesional en redes e internet CCNP', 'Profesional en redes e internet CCNP'),
    ('Desarrollador Fullstack JAVA', 'Desarrollador Fullstack JAVA'),
    ('Desarrollador Fullstack .NET', 'Desarrollador Fullstack .NET'),
] + _OTRO

CARRERAS_TIC_LIBRE = [
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
] + _OTRO

CARRERAS_ETS_1ER = [
    ('Instalaciones Eléctricas Generales', 'Instalaciones Eléctricas Generales'),
    ('Fundamentos de Electrónica Industrial', 'Fundamentos de Electrónica Industrial'),
    ('Mecanismos del Automóvil', 'Mecanismos del Automóvil'),
    ('Fundamentos de la Construcción', 'Fundamentos de la Construcción'),
] + _OTRO

CARRERAS_ETS_2DO = [
    ('Controles y Máquinas Eléctricas', 'Controles y Máquinas Eléctricas'),
    ('Electrónica Industrial Aplicada', 'Electrónica Industrial Aplicada'),
    ('Mecánica de Motores', 'Mecánica de Motores'),
    ('Administración de Obras', 'Administración de Obras'),
] + _OTRO

CARRERAS_ETS_LIBRE = [
    ('Topografía', 'Topografía'),
    ('Especialistas en Tecnologías Industrial', 'Especialistas en Tecnologías Industrial'),
    ('Electromecánica Viernes', 'Electromecánica Viernes'),
    ('Mecánica de Motocicletas', 'Mecánica de Motocicletas'),
    ('Electromecánica Automotriz', 'Electromecánica Automotriz'),
    ('Inyección Electrónica', 'Inyección Electrónica'),
    ('Aire Acondicionado Automotriz', 'Aire Acondicionado Automotriz'),
    ('Calderas de Vapor', 'Calderas de Vapor'),
    ('Soldadura Industrial', 'Soldadura Industrial'),
    ('SEA, SOA, MAG, TIG', 'SEA, SOA, MAG, TIG'),
    ('Automatización Industrial', 'Automatización Industrial'),
    ('Mantenimiento Mecánico Industrial', 'Mantenimiento Mecánico Industrial'),
    ('Refrigeración Industrial', 'Refrigeración Industrial'),
    ('Certificación Nacional de Técnico Frigorista', 'Certificación Nacional de Técnico Frigorista'),
    ('Revit Arquitectura / Estructuras / MEP', 'Revit Arquitectura / Estructuras / MEP'),
    ('Autocad 2D/3D', 'Autocad 2D/3D'),
] + _OTRO

def _unique(pairs):
    seen = set()
    out = []
    for value, label in pairs:
        if value in seen:
            continue
        seen.add(value)
        out.append((value, label))
    return out


CARRERAS_ETS = _unique(CARRERAS_ETS_1ER + CARRERAS_ETS_2DO + CARRERAS_ETS_LIBRE)
CARRERAS_TIC = _unique(CARRERAS_TIC_LIBRE)

NOTA_JAVA_NET = (
    'JAVA y .NET pueden cursarse en cualquier orden, siempre que se completen ambos.'
)

COURSES_BY_TCU = {
    'ets': {
        TCU_1ER: CARRERAS_ETS_1ER,
        TCU_2DO: CARRERAS_ETS_2DO,
        TCU_NO: CARRERAS_ETS_LIBRE,
        TCU_3ER: [],
    },
    'tic': {
        TCU_1ER: CARRERAS_TIC_1ER,
        TCU_2DO: CARRERAS_TIC_2DO,
        TCU_NO: CARRERAS_TIC_LIBRE,
        TCU_3ER: [],
    },
}

TCU_NOTES = {
    'ets': {},
    'tic': {
        TCU_1ER: NOTA_JAVA_NET,
        TCU_2DO: NOTA_JAVA_NET,
    },
}

TRABAJADORES_ETS = [
    ('Manuel Barrientos', 'Manuel Barrientos'),
    ('Ruben Rivera', 'Ruben Rivera'),
    ('José Chaj', 'José Chaj'),
    ('Antonio Escobar', 'Antonio Escobar'),
]
TRABAJADORES_TIC = [
    ('Rolando Escot', 'Rolando Escot'),
    ('Pablo Ruiz', 'Pablo Ruiz'),
]

IMG = {
    'ets': '/ets_inscripcion/static/src/img/ets_img.avif',
    'tic': '/ets_inscripcion/static/src/img/tic_img.avif',
}

TITULOS = {
    'ets': 'Datos Personales — Escuela Técnica Superior',
    'tic': 'Datos Personales — TIC',
}


def courses_for(area, tcu):
    return COURSES_BY_TCU.get(area, {}).get(tcu) or []


def carrera_disabled(tcu):
    return tcu == TCU_3ER


def for_area(area):
    key = 'tic' if area == 'tic' else 'ets'
    if key == 'tic':
        return {
            'area': 'tic',
            'titulo': TITULOS['tic'],
            'tcu': TCU_TIC,
            'carreras': CARRERAS_TIC,
            'trabajadores': TRABAJADORES_TIC,
            'label_carrera': 'Curso Técnico',
            'label_tsu': 'Técnico Superior Universitario',
            'label_colaborador': 'Colaborador que lo atendió',
            'img': IMG['tic'],
            'courses_by_tcu': COURSES_BY_TCU['tic'],
            'tcu_notes': TCU_NOTES['tic'],
            'tcu_disable': [TCU_3ER],
            'catalogo_listo': True,
        }
    return {
        'area': 'ets',
        'titulo': TITULOS['ets'],
        'tcu': TCU_ETS,
        'carreras': CARRERAS_ETS,
        'trabajadores': TRABAJADORES_ETS,
        'label_carrera': 'Carrera Técnica a la que se inscribe',
        'label_tsu': 'Técnico Superior Universitario',
        'label_colaborador': 'Colaborador que lo atendió',
        'img': IMG['ets'],
        'courses_by_tcu': COURSES_BY_TCU['ets'],
        'tcu_notes': TCU_NOTES['ets'],
        'tcu_disable': [TCU_3ER],
        'catalogo_listo': True,
    }


def value_allowed(options, value):
    return value in {v for v, _label in options}


def all_course_values():
    return [v for v, _l in CARRERAS_ETS + CARRERAS_TIC]
