"""Catálogos dinámicos desde API pública de ETS/TIC Kinal."""

from concurrent.futures import ThreadPoolExecutor
import json
import logging
import os
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

from .guatemala import MUNICIPIOS_GT, geo_ok  # noqa: F401

_logger = logging.getLogger(__name__)

# Azul de btn-primary / Contáctanos en el sitio (no el aqua anterior #008f8c).
COLOR_PRIMARY = '#195190'

API_BASE_URL = os.environ.get('ETS_API_BASE_URL', 'http://appets.kinal.edu.gt:3001').rstrip('/')
AREAS_PUBLICAS_URL = f'{API_BASE_URL}/api/areas-publicas'
CURSOS_PUBLICOS_URL = f'{API_BASE_URL}/api/cursos-publicos'
API_TIMEOUT_SECONDS = 5
CACHE_TTL_SECONDS = 300

JORNADAS = [
    ('matutina', 'Matutina - sábados (08:00 a 12:30)'),
    ('vespertina', 'Vespertina - sábados (13:00 a 17:30)'),
    ('entre_semana', 'Entre semana (noches, 1 o 2 días)'),
]

TCU_1ER = 'Técnico Universitario (1er. año Carrera Técnica)'
TCU_2DO = 'Técnico Universitario (2do. año Carrera Técnica)'
TCU_3ER = 'Técnico Universitario (3er. año) AÑO ACADÉMICO'
TCU_NO = 'NO'
MOD_DIPLOMADO = 'Diplomados Virtuales'
MOD_EMPRESA = 'Cursos a Empresas'
OTRO = 'Otras'

VINCULO_EGRESADO = 'egresado'
VINCULO_ESTUDIANTE = 'estudiante'
VINCULO_NINGUNO = 'ninguno'
VINCULOS = [
    (VINCULO_EGRESADO, 'Egresado de Fundación Kinal'),
    (VINCULO_ESTUDIANTE, 'Estudiante actual de Fundación Kinal'),
    (VINCULO_NINGUNO, 'Ninguno de los anteriores'),
]

_OTRO = [(OTRO, 'Otro')]

NOTA_JAVA_NET = (
    'JAVA y .NET pueden cursarse en cualquier orden, siempre que se completen ambos.'
)

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
    'ets': 'Inscripción — Escuela Técnica Superior (ETS)',
    'tic': 'Inscripción — Tecnologías de la Información (TIC)',
}

_ETS_GUIDE_KEYWORDS = (
    'electric', 'electron', 'soldadur', 'caldera', 'refriger', 'aire acond',
    'mecan', 'motociclet', 'montacarga', 'autocad', 'revit', 'tekla', 'civil 3d',
    'sketchup', 'topograf', 'construcc', 'neumat', 'plc', 'logo!', 'siemens',
    'variador', 'motor', 'bombeo', 'tierra fisica', 'instrumentacion', 'planimetria',
    'planiametria', 'ventaneria', 'dibujo tecnico', 'soa ', 'mag', 'tig', 'arduino',
    'automatiz', 'solar', 'costos', 'presupuesto',
)

_TIC_GUIDE_KEYWORDS = (
    'cisco', 'ccna', 'ccnp', 'cibersegur', 'redes', 'cableado',
    'inteligencia artificial', 'ia ', 'ia:', 'power bi', 'power query', 'excel',
    'photoshop', 'bizagi', 'software', 'programacion', 'python', 'java', '.net',
    'sql', 'cloud', 'aws', 'linux', 'servidor', 'it essentials', 'prompts', 'gpt',
)

_CACHE = {
    'timestamp': 0.0,
    'snapshot': None,
}


def _norm_text(val):
    raw = (val or '').lower()
    return ''.join(
        c for c in unicodedata.normalize('NFD', raw)
        if unicodedata.category(c) != 'Mn'
    )


def _guide_affinity(course_name):
    """Clasificación orientativa ('ets', 'tic' o 'ambos') para áreas compartidas."""
    normed = _norm_text(course_name)
    is_ets = any(k in normed for k in _ETS_GUIDE_KEYWORDS)
    is_tic = any(k in normed for k in _TIC_GUIDE_KEYWORDS)
    if is_ets and not is_tic:
        return 'ets'
    if is_tic and not is_ets:
        return 'tic'
    return 'ambos'


def _unique_pairs(pairs):
    seen = set()
    out = []
    for value, label in pairs:
        if not value or value in seen:
            continue
        seen.add(value)
        out.append((value, label))
    return out


def _http_get_json(url):
    req = urllib.request.Request(
        url,
        headers={'Accept': 'application/json', 'User-Agent': 'Odoo-CRM-ETS/1.0'},
    )
    with urllib.request.urlopen(req, timeout=API_TIMEOUT_SECONDS) as resp:
        payload = resp.read().decode('utf-8')
        return json.loads(payload)


def fetch_areas_publicas():
    """Obtiene la lista de categorías y áreas desde /api/areas-publicas."""
    data = _http_get_json(AREAS_PUBLICAS_URL)
    return data if isinstance(data, list) else []


def fetch_cursos_por_area(area_id):
    """Obtiene los cursos de un área desde /api/cursos-publicos?area_id=<id>."""
    query = urllib.parse.urlencode({'area_id': area_id})
    data = _http_get_json(f'{CURSOS_PUBLICOS_URL}?{query}')
    return data if isinstance(data, list) else []


def _fetch_full_snapshot():
    categorias = fetch_areas_publicas()
    cat_by_key = {}
    unique_area_ids = set()

    for item in categorias:
        if not isinstance(item, dict):
            continue
        cat_key = (item.get('categoria') or '').strip()
        if not cat_key:
            continue
        areas_clean = []
        for area in item.get('areas') or []:
            if isinstance(area, dict) and area.get('id') is not None and area.get('nombre'):
                aid = area['id']
                unique_area_ids.add(aid)
                areas_clean.append({
                    'id': aid,
                    'nombre': str(area['nombre']).strip(),
                })
        cat_by_key[cat_key] = {
            'categoria': cat_key,
            'nombre': str(item.get('nombre') or cat_key).strip(),
            'areas': areas_clean,
        }

    cursos_by_area = {}
    if unique_area_ids:
        sorted_ids = sorted(unique_area_ids)
        max_workers = min(8, len(sorted_ids))

        def _load_one(aid):
            return aid, fetch_cursos_por_area(aid)

        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            for aid, raw_courses in pool.map(_load_one, sorted_ids):
                cleaned = []
                for c in raw_courses:
                    if not isinstance(c, dict) or not c.get('nombre'):
                        continue
                    cleaned.append({
                        'id': c.get('id'),
                        'nombre': str(c['nombre']).strip(),
                        'anio_curso': c.get('anio_curso'),
                    })
                cursos_by_area[aid] = cleaned

    return {
        'cat_by_key': cat_by_key,
        'cursos_by_area': cursos_by_area,
        'ok': bool(cat_by_key and cursos_by_area),
    }


def get_api_snapshot(force_refresh=False):
    """Devuelve el snapshot de la API con caché en memoria y fallback seguro."""
    now = time.time()
    cached = _CACHE.get('snapshot')
    if not force_refresh and cached and (now - _CACHE.get('timestamp', 0.0)) < CACHE_TTL_SECONDS:
        return cached

    try:
        snapshot = _fetch_full_snapshot()
        if snapshot.get('ok'):
            _CACHE['snapshot'] = snapshot
            _CACHE['timestamp'] = now
            return snapshot
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
        _logger.warning('No se pudo consultar la API pública de cursos ETS: %s', exc)

    if cached:
        return cached
    return {'cat_by_key': {}, 'cursos_by_area': {}, 'ok': False}


def _build_area_catalog(area_key, snapshot):
    key = 'tic' if area_key == 'tic' else 'ets'
    cat_by_key = snapshot.get('cat_by_key') or {}
    cursos_by_area = snapshot.get('cursos_by_area') or {}
    catalogo_listo = bool(snapshot.get('ok'))

    tecnico_cat = cat_by_key.get('tecnico') or {'nombre': 'Curso Técnico', 'areas': []}
    tecnologia_cat = cat_by_key.get('tecnologia') or {'nombre': 'Curso de Tecnología', 'areas': []}
    tsu_cat = cat_by_key.get('tsu') or {'nombre': 'Técnico Superior Universitario (3 años)', 'areas': []}
    diplomado_cat = cat_by_key.get('diplomado') or {'nombre': 'Diplomados Virtuales', 'areas': []}
    empresa_cat = cat_by_key.get('empresa') or {'nombre': 'Cursos a Empresas', 'areas': []}

    tic_area_ids = {a['id'] for a in tecnologia_cat['areas']}
    ets_tecnico_ids = {a['id'] for a in tecnico_cat['areas']}
    tsu_areas_all = tsu_cat['areas']

    tsu_anio3_area_ids = {
        a['id']
        for a in tsu_areas_all
        if any(c.get('anio_curso') == 3 for c in cursos_by_area.get(a['id'], []))
    }
    ets_tsu_only_ids = {
        a['id']
        for a in tsu_areas_all
        if a['id'] not in tic_area_ids and a['id'] not in tsu_anio3_area_ids
    }
    ets_exclusive_ids = ets_tecnico_ids | ets_tsu_only_ids

    # 1.1 Cursos ETS o Cursos TIC según el card inicial
    base_cat = tecnologia_cat if key == 'tic' else tecnico_cat
    cursos_area_groups = []
    cursos_area_flat = []
    seen_flat = set()
    for a in base_cat['areas']:
        aid = a['id']
        aname = a['nombre']
        c_list = []
        for c in cursos_by_area.get(aid, []):
            item = {
                'id': c['id'],
                'nombre': c['nombre'],
                'anio_curso': c.get('anio_curso'),
                'area_id': aid,
                'area_nombre': aname,
                'affinity': key,
            }
            c_list.append(item)
            if c['nombre'] not in seen_flat:
                seen_flat.add(c['nombre'])
                cursos_area_flat.append(item)
        if c_list:
            cursos_area_groups.append({
                'id': aid,
                'nombre': aname,
                'cursos': c_list,
            })

    # 1.2 Técnico Superior Universitario (TSU) filtrado dinámicamente por área y año
    if key == 'tic':
        tsu_areas_for_side = [
            a for a in tsu_areas_all
            if a['id'] in tic_area_ids or a['id'] in tsu_anio3_area_ids
        ]
    else:
        tsu_areas_for_side = [
            a for a in tsu_areas_all
            if a['id'] not in tic_area_ids
        ]

    tsu_by_year = {1: [], 2: [], 3: []}
    for yr in (1, 2, 3):
        seen_yr = set()
        for a in tsu_areas_for_side:
            aid = a['id']
            aname = a['nombre']
            for c in cursos_by_area.get(aid, []):
                if c.get('anio_curso') == yr and c['nombre'] not in seen_yr:
                    seen_yr.add(c['nombre'])
                    tsu_by_year[yr].append({
                        'id': c['id'],
                        'nombre': c['nombre'],
                        'anio_curso': yr,
                        'area_id': aid,
                        'area_nombre': aname,
                        'affinity': key,
                    })

    # 2. Diplomados Virtuales y 3. Cursos a Empresas
    def _build_shared_category(cat_obj):
        all_areas = cat_obj.get('areas') or []
        if key == 'tic':
            filtered_areas = [a for a in all_areas if a['id'] not in ets_exclusive_ids] or all_areas
        else:
            filtered_areas = [a for a in all_areas if a['id'] not in tic_area_ids] or all_areas

        groups = []
        recommended_courses = []
        all_courses = []
        seen_all = set()
        seen_rec = set()

        for a in filtered_areas:
            aid = a['id']
            aname = a['nombre']
            area_is_exclusive = (aid in ets_exclusive_ids) or (aid in tic_area_ids)
            group_courses = []
            for c in cursos_by_area.get(aid, []):
                affinity = (
                    'ets' if aid in ets_exclusive_ids
                    else 'tic' if aid in tic_area_ids
                    else _guide_affinity(c['nombre'])
                )
                matches_side = area_is_exclusive or affinity in (key, 'ambos')
                item = {
                    'id': c['id'],
                    'nombre': c['nombre'],
                    'anio_curso': c.get('anio_curso'),
                    'area_id': aid,
                    'area_nombre': aname,
                    'affinity': affinity,
                    'recommended': matches_side,
                }
                group_courses.append(item)
                if c['nombre'] not in seen_all:
                    seen_all.add(c['nombre'])
                    all_courses.append(item)
                if matches_side and c['nombre'] not in seen_rec:
                    seen_rec.add(c['nombre'])
                    recommended_courses.append(item)
            if group_courses:
                groups.append({
                    'id': aid,
                    'nombre': aname,
                    'cursos': group_courses,
                })

        if not recommended_courses:
            recommended_courses = list(all_courses)
        return groups, recommended_courses, all_courses

    dip_groups, dip_rec, dip_all = _build_shared_category(diplomado_cat)
    emp_groups, emp_rec, emp_all = _build_shared_category(empresa_cat)

    tcu_options = [
        (TCU_NO, 'Cursos TIC (Curso de Tecnología)' if key == 'tic' else 'Cursos ETS (Curso Técnico)'),
        (TCU_1ER, 'Técnico Superior Universitario (1er. año)'),
        (TCU_2DO, 'Técnico Superior Universitario (2do. año)'),
        (TCU_3ER, 'Técnico Superior Universitario (3er. año) AÑO ACADÉMICO'),
        (MOD_DIPLOMADO, diplomado_cat['nombre']),
        (MOD_EMPRESA, empresa_cat['nombre']),
    ]

    courses_by_tcu = {
        TCU_NO: _unique_pairs([(c['nombre'], c['nombre']) for c in cursos_area_flat] + _OTRO),
        TCU_1ER: _unique_pairs([(c['nombre'], c['nombre']) for c in tsu_by_year[1]] + _OTRO),
        TCU_2DO: _unique_pairs([(c['nombre'], c['nombre']) for c in tsu_by_year[2]] + _OTRO),
        TCU_3ER: _unique_pairs([(c['nombre'], c['nombre']) for c in tsu_by_year[3]] + _OTRO),
        MOD_DIPLOMADO: _unique_pairs([(c['nombre'], c['nombre']) for c in dip_all] + _OTRO),
        MOD_EMPRESA: _unique_pairs([(c['nombre'], c['nombre']) for c in emp_all] + _OTRO),
    }

    all_area_pairs = _unique_pairs(
        courses_by_tcu[TCU_NO]
        + courses_by_tcu[TCU_1ER]
        + courses_by_tcu[TCU_2DO]
        + courses_by_tcu[TCU_3ER]
        + courses_by_tcu[MOD_DIPLOMADO]
        + courses_by_tcu[MOD_EMPRESA]
    )

    tcu_notes = (
        {TCU_1ER: NOTA_JAVA_NET, TCU_2DO: NOTA_JAVA_NET}
        if key == 'tic'
        else {}
    )

    steps_tree = {
        'area': key,
        'area_upper': key.upper(),
        'catalogo_listo': catalogo_listo,
        'otro_value': OTRO,
        'options': [
            {
                'id': 'carrera_curso',
                'num': '1',
                'title': 'Carrera Técnica o Curso',
                'subtitle': (
                    'Cursos técnicos prácticos en talleres y laboratorios o carrera universitaria TSU.'
                    if key == 'ets'
                    else 'Cursos de desarrollo de software, redes, nube e IA o carrera universitaria TSU.'
                ),
                'icon': 'graduation',
                'suboptions': [
                    {
                        'id': 'cursos_area',
                        'title': 'Cursos TIC' if key == 'tic' else 'Cursos ETS',
                        'subtitle': base_cat['nombre'],
                        'badge': f"{len(cursos_area_flat)} cursos",
                        'icon': 'code' if key == 'tic' else 'tools',
                        'modality_value': TCU_NO,
                        'modality_label': 'Cursos TIC' if key == 'tic' else 'Cursos ETS',
                        'areas': cursos_area_groups,
                        'courses': cursos_area_flat,
                    },
                    {
                        'id': 'tsu',
                        'title': 'Técnico Superior Universitario',
                        'subtitle': tsu_cat['nombre'],
                        'badge': '1er, 2do y 3er año',
                        'icon': 'university',
                        'years': [
                            {
                                'anio': 1,
                                'title': 'TSU — 1er. Año',
                                'subtitle': 'Primer año de Carrera Técnica Universitaria',
                                'modality_value': TCU_1ER,
                                'modality_label': 'TSU 1er. Año',
                                'note': tcu_notes.get(TCU_1ER, ''),
                                'courses': tsu_by_year[1],
                            },
                            {
                                'anio': 2,
                                'title': 'TSU — 2do. Año',
                                'subtitle': 'Segundo año de Carrera Técnica Universitaria',
                                'modality_value': TCU_2DO,
                                'modality_label': 'TSU 2do. Año',
                                'note': tcu_notes.get(TCU_2DO, ''),
                                'courses': tsu_by_year[2],
                            },
                            {
                                'anio': 3,
                                'title': 'TSU — 3er. Año (Año Académico)',
                                'subtitle': 'Cursos Académicos de Técnico Universitario',
                                'modality_value': TCU_3ER,
                                'modality_label': 'TSU 3er. Año Académico',
                                'note': '',
                                'courses': tsu_by_year[3],
                            },
                        ],
                    },
                ],
            },
            {
                'id': 'diplomado',
                'num': '2',
                'title': diplomado_cat['nombre'],
                'subtitle': 'Capacitaciones virtuales, programas online y Kinal Language School.',
                'badge': f"{len(dip_rec)} disponibles",
                'icon': 'laptop',
                'modality_value': MOD_DIPLOMADO,
                'modality_label': diplomado_cat['nombre'],
                'areas': dip_groups,
                'courses': dip_rec,
                'all_courses': dip_all,
            },
            {
                'id': 'empresa',
                'num': '3',
                'title': empresa_cat['nombre'],
                'subtitle': 'Formación especializada y actualización técnica para equipos corporativos.',
                'badge': f"{len(emp_rec)} disponibles",
                'icon': 'briefcase',
                'modality_value': MOD_EMPRESA,
                'modality_label': empresa_cat['nombre'],
                'areas': emp_groups,
                'courses': emp_rec,
                'all_courses': emp_all,
            },
        ],
    }

    return {
        'area': key,
        'titulo': TITULOS[key],
        'tcu': tcu_options,
        'carreras': all_area_pairs,
        'trabajadores': TRABAJADORES_TIC if key == 'tic' else TRABAJADORES_ETS,
        'label_carrera': 'Curso o Carrera Seleccionada',
        'label_tsu': 'Modalidad / Programa',
        'label_colaborador': 'Colaborador que lo atendió',
        'img': IMG[key],
        'courses_by_tcu': courses_by_tcu,
        'tcu_notes': tcu_notes,
        'tcu_disable': [],
        'steps_tree': steps_tree,
        'catalogo_listo': catalogo_listo,
    }


def for_area(area):
    snapshot = get_api_snapshot()
    return _build_area_catalog(area, snapshot)


def courses_for(area, tcu):
    cat = for_area(area)
    return cat['courses_by_tcu'].get(tcu) or []


def carrera_disabled(tcu):
    """En el segundo formulario, 3er año académico permite omitir curso si ya venía vacío."""
    return False


def value_allowed(options, value):
    return value in {v for v, _label in options}


def all_modality_values():
    return [TCU_NO, TCU_1ER, TCU_2DO, TCU_3ER, MOD_DIPLOMADO, MOD_EMPRESA]


def all_course_values():
    snapshot = get_api_snapshot()
    cursos_by_area = snapshot.get('cursos_by_area') or {}
    names = []
    seen = set()
    for c_list in cursos_by_area.values():
        for c in c_list:
            name = c.get('nombre')
            if name and name not in seen:
                seen.add(name)
                names.append(name)
    if OTRO not in seen:
        names.append(OTRO)
    return names
