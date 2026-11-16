"""T-157 (Fase 0) · Verificador de consistencia de identificadores del Bloque A.

Mide qué está desincronizado entre el corpus vigente del Bloque A y el código del ejecutor. Todo dato del informe sale de lo
escaneado: el Documento 0 (§1, §5.1, §6.1, §9.3 y el título de §7.3), el Catálogo de cálculos del Motor, los archivos de
`05_Archivos_operativos` (por identificador: F7, F8 y F9 no se cargan, solo se extraen sus identificadores), el resto de `.md`
del corpus y el código importado (`motor/servicio.py` y `contratos.py`).

Clases del informe:
  a. Contratos CT citados frente a §6.1 y a `contratos.py` (`CANALES`, `CANALES_V6`, `CAMPOS_MINIMOS`, `canal_permitido`).
  b. Reglas R citadas frente a §1.
  c. Archivos F citados frente a §5.1, con el mapa código → archivo real de `05_Archivos_operativos` por su H1.
  d. Fichas del Catálogo (encabezados `### ID`) frente a `FICHAS_CATALOGO`, `IMPLEMENTADAS` y `SERVICIOS_CT10`
     (IMPLEMENTADO, SOLO_CATALOGO, SOLO_CODIGO, ID_DISTINTO), la madurez del índice §4, la versión del Catálogo y las menciones
     de otra versión.
  e. Referencias RF/TA/TM/TF/ANA-DOC/DOC-MOT citadas en prompts y funciones frente a `05_Archivos_operativos`.
  f. Puertas PS citadas frente a §9.3.

Entradas sin nombre fijo: el Documento 0 y el Catálogo se buscan por patrón y el verificador falla cerrado (salida 2, sin
informe) si no hay exactamente uno. No lee `11_Ejecutor/` como corpus ni ninguna carpeta `99_Historico*`.

Uso (desde `bloque_a/11_Ejecutor`):
    python -m bloque_a.herramientas.verificador_ids [--raiz DIR] [--json RUTA] [--md RUTA] [--auditoria RUTA]
Sin `--json`, `--md` ni `--auditoria`, escribe el Markdown por la salida estándar. `--auditoria` sustituye solo el bloque entre
las marcas `<!-- INFORME:INICIO -->` y `<!-- INFORME:FIN -->` del documento dado (lo demás se conserva).
Salida: 0 sin errores · 1 con errores · 2 fallo cerrado (entrada ausente, ambigua o ilegible).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, NamedTuple

import jsonschema

VERSION = "1.0.0"
NIVELES = ("ERROR", "AVISO", "INFO")
CLASES = {"entradas": "Entradas", "a": "Contratos CT", "b": "Reglas R", "c": "Archivos F", "d": "Fichas del Catálogo",
          "e": "Referencias de los archivos operativos", "f": "Puertas PS"}
CLASES_FICHA = ("IMPLEMENTADO", "SOLO_CATALOGO", "SOLO_CODIGO", "ID_DISTINTO")

DIR_GOBERNANZA = "01_Gobernanza"
DIR_PROMPTS = "02_System_prompts"
DIR_FUNCIONES = "03_Funciones"
DIR_CATALOGO = "04_Motor_conocimiento_y_catalogo"
DIR_OPERATIVOS = "05_Archivos_operativos"
DIR_EJECUTOR = "11_Ejecutor"
PREFIJO_HISTORICO = "99_Historico"
PATRON_DOC0 = re.compile(r"^Documento 0\b.*\.md$")
PATRON_CATALOGO = re.compile(r"^Catálogo de cálculos del Motor\b.*\.md$")
MARCA_INICIO = "<!-- INFORME:INICIO -->"
MARCA_FIN = "<!-- INFORME:FIN -->"

# Patrones de cita (frontera de palabra a los dos lados; «CT-B-01» o «CT-G-02», de otros bloques, no casan)
RE_CT = re.compile(r"(?<![\w-])CT-(\d+)\b(?!-)")
RE_R = re.compile(r"(?<![\w-])R(\d{1,2})\b(?!-)")
RE_F = re.compile(r"(?<![\w-])F(\d{1,2})\b(?!-)")
RE_PS = re.compile(r"(?<![\w-])PS(\d{1,2})\b(?!-)")
RE_REFERENCIA = re.compile(r"(?<![\w-])(RF-\d+|TA-\d+|TM-\d+|TF-\d+|ANA-DOC-\d+|DOC-MOT-\d+)\b(?!-)")
RE_VERSION = re.compile(r"V(\d+(?:\.\d+)+)")
RE_MENCION_CATALOGO = re.compile(r"Catálogo(?: de cálculos)?(?: del Motor)?[\s\-–]*(?:óptima\s+)?V(\d+(?:\.\d+)+)"
                                 r'|"catalog_version"\s*:\s*"(\d+(?:\.\d+)+)"')
RE_ENCABEZADO = re.compile(r"^(#{1,6}) (.*)$")
RE_ID_FICHA = r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d{3}"
RE_ENCABEZADO_FICHA = re.compile(rf"^### ({RE_ID_FICHA})(?=\s|$)")
# Criterio técnico del verificador [PROPUESTO INC-T157-01, técnico]: dos ID son «parecidos» si coinciden quitando los
# separadores, si comparten el tallo y solo cambia el número, o si su distancia de edición no pasa de este tope
DISTANCIA_PARECIDO = 2
# Contextos en los que un ID con forma de cita es otra cosa (cada uno se deduce del propio texto y se informa como INFO
# CITA_EN_CONTEXTO_AJENO, con su ubicación; solo se consultan para citas que de otro modo serían error)
RE_JEL = re.compile(r"\bJEL\b")
RE_OPERADOR = re.compile(r"[−/+*=×]")
RE_FUNCION_LOCAL = re.compile(r"^\|\s*[A-Z]+-(F\d+)\s*\|")
RE_CAMPO_JSON = re.compile(r'"([A-Za-z_][A-Za-z0-9_]*)"\s*:\s*"[^"]*$')
CAMPOS_FICHA = ("ficha_id", "method_id", "operacion")   # campos de un mensaje CT-09 que llevan el ID de una ficha


class EntradaInvalida(Exception):
    """Entrada ausente, ambigua o ilegible: el verificador falla cerrado y no emite informe."""


# ----------------------------------------------------------------------------------------------- código del ejecutor
@dataclass(frozen=True)
class Codigo:
    """Lo que el código declara. `desde_paquete` lo lee importando el ejecutor; las pruebas lo construyen a mano."""
    catalog_version: str
    fichas_catalogo: tuple[str, ...]
    manejadores: frozenset[str]
    servicios_ct10: frozenset[str] = frozenset()
    documentadas_con_codigo: frozenset[str] = frozenset()
    alternativas: Mapping[str, str] = field(default_factory=dict)
    ruta_catalogo: tuple[str, ...] = ()
    canales: frozenset[str] = frozenset()             # contratos con entrada en CANALES
    canales_admitidos: frozenset[str] = frozenset()   # contratos para los que canal_permitido admite algún par
    canales_v6: frozenset[str] = frozenset()
    campos_minimos: frozenset[str] = frozenset()
    madurez_leida: Mapping[str, str] | None = None    # madurez_catalogo(raiz) del código
    servibles: frozenset[str] | None = None           # fichas con servible(f, raiz)
    # (archivo, línea, versión, es_literal) de cada versión del Catálogo escrita en los .py del paquete: un literal
    # `"catalog_version": "4.0"` (lo que el código emite) o una mención en prosa («Catálogo de cálculos V4.0»)
    versiones_en_codigo: tuple[tuple[str, int, str, bool], ...] = ()
    fuentes: Mapping[str, str] = field(default_factory=dict)   # archivo → sha256

    @classmethod
    def desde_paquete(cls, raiz: Path) -> Codigo:
        from .. import contratos as ct
        from ..motor import servicio as sv
        fichas = tuple(sv.FICHAS_CATALOGO)
        universo = set(fichas) | set(sv.IMPLEMENTADAS) | set(sv.SERVICIOS_CT10)
        admitidos = frozenset(c for c, pares in ct.CANALES.items()
                              if any(ct.canal_permitido(c, e, r) for em, rc in pares for e in em for r in rc))
        base = Path(sv.__file__).resolve().parents[2]
        fuentes = {Path(str(m.__file__)).resolve().relative_to(base).as_posix(): _sha256(Path(str(m.__file__))) for m in (sv, ct)}
        versiones: list[tuple[str, int, str, bool]] = []
        for py in sorted(Path(sv.__file__).resolve().parents[1].rglob("*.py")):
            if py.resolve() == Path(__file__).resolve() or "__pycache__" in py.parts:
                continue   # el propio verificador cita versiones en sus patrones
            try:
                rel = py.resolve().relative_to(Path(raiz).resolve()).as_posix()
            except ValueError:
                rel = py.resolve().relative_to(base).as_posix()
            for n, linea in enumerate(_leer(py).splitlines(), 1):
                for m in RE_MENCION_CATALOGO.finditer(linea):
                    versiones.append((rel, n, m.group(1) or m.group(2), m.group(2) is not None))
        return cls(catalog_version=str(sv.CATALOG_VERSION), fichas_catalogo=fichas, manejadores=frozenset(sv.IMPLEMENTADAS),
                   servicios_ct10=frozenset(sv.SERVICIOS_CT10), documentadas_con_codigo=frozenset(sv.DOCUMENTADAS_CON_CODIGO),
                   alternativas=dict(sv.ALTERNATIVAS), ruta_catalogo=tuple(sv.RUTA_CATALOGO), canales=frozenset(ct.CANALES),
                   canales_admitidos=admitidos, canales_v6=frozenset(ct.CANALES_V6),
                   campos_minimos=frozenset(ct.CAMPOS_MINIMOS), madurez_leida=dict(sv.madurez_catalogo(raiz)),
                   servibles=frozenset(f for f in sorted(universo) if sv.servible(f, raiz)), fuentes=fuentes,
                   versiones_en_codigo=tuple(versiones))


# ----------------------------------------------------------------------------------------------- lectura del corpus
def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def _sha256(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def _leer(ruta: Path) -> str:
    try:
        return _nfc(ruta.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError) as e:
        raise EntradaInvalida(f"no se puede leer {ruta.name}: {e}") from e


def _excluida(rel: Path) -> bool:
    return any(p == DIR_EJECUTOR or p.startswith((PREFIJO_HISTORICO, ".")) or p == "__pycache__"
               for p in rel.parts[:-1])


def _unico(raiz: Path, carpeta: str, patron: re.Pattern[str], que: str) -> Path:
    d = raiz / carpeta
    if not d.is_dir():
        raise EntradaInvalida(f"{que}: no existe la carpeta {carpeta}/")
    cand = sorted((p for p in d.iterdir() if p.is_file() and patron.match(_nfc(p.name))), key=lambda p: _nfc(p.name))
    if len(cand) != 1:
        nombres = ", ".join(_nfc(p.name) for p in cand) or "ninguno"
        raise EntradaInvalida(f"{que}: se esperaba exactamente uno en {carpeta}/ y hay {len(cand)} ({nombres})")
    return cand[0]


@dataclass(frozen=True)
class Documento:
    rel: str
    texto: str
    sha256: str

    @property
    def lineas(self) -> list[str]:
        return self.texto.splitlines()


def _corpus(raiz: Path) -> list[Documento]:
    docs = []
    for p in raiz.rglob("*.md"):
        rel = p.relative_to(raiz)
        if p.is_file() and not _excluida(rel):
            docs.append(Documento(_nfc(rel.as_posix()), _leer(p), _sha256(p)))
    return sorted(docs, key=lambda d: d.rel)


class Cita(NamedTuple):
    archivo: str
    linea: int
    texto: str
    inicio: int


def _citas(docs: Iterable[Documento], patron: re.Pattern[str], formato: str = "{0}") -> dict[str, list[Cita]]:
    """id → cada aparición (archivo, línea, texto de la línea, columna), en orden de archivo y línea."""
    out: dict[str, list[Cita]] = {}
    for d in docs:
        for n, linea in enumerate(d.lineas, 1):
            for m in patron.finditer(linea):
                out.setdefault(formato.format(*m.groups(), m.group(0)), []).append(Cita(d.rel, n, linea, m.start()))
    return out


def _contexto_general(c: Cita) -> str | None:
    if RE_JEL.search(c.texto):
        return "código JEL de clasificación de la literatura económica"
    for m in re.finditer(r"`([^`]*)`", c.texto):
        if m.start() < c.inicio < m.end() and RE_OPERADOR.search(m.group(1)):
            return "notación dentro de una fórmula"
    return None


def _inexistentes(h: _Hallazgos, clase: str, codigo: str, ids: Iterable[str], citas: Mapping[str, list[Cita]],
                  mensaje: Callable[[str], str], contexto: Callable[[str, Cita], str | None]) -> None:
    """ERROR por cada ID citado que no existe, salvo las apariciones que su contexto explica (INFO, con su ubicación)."""
    for x in sorted(ids, key=_clave_id):
        explicadas: dict[str, list[Cita]] = {}
        resto: list[Cita] = []
        for c in citas[x]:
            motivo = contexto(x, c)
            if motivo:
                explicadas.setdefault(motivo, []).append(c)
            else:
                resto.append(c)
        if resto:
            h(clase, "ERROR", codigo, x, mensaje(x), resto)
        for motivo, cs in sorted(explicadas.items()):
            h(clase, "INFO", "CITA_EN_CONTEXTO_AJENO", x, f"{x} aparece como {motivo}: no se cuenta como cita", cs)


def _seccion(doc: Documento, nivel: int, numero: str) -> tuple[int, list[str]]:
    """(línea del título, líneas de la sección hasta el siguiente título de nivel igual o mayor). Falla cerrado si no está o
    si hay más de una."""
    lineas = doc.lineas
    patron = re.compile(rf"^{'#' * nivel} {re.escape(numero)}[.\s]")
    inicios = [i for i, x in enumerate(lineas) if patron.match(x)]
    if len(inicios) != 1:
        raise EntradaInvalida(f"{doc.rel}: se esperaba una sección {'#' * nivel} {numero} y hay {len(inicios)}")
    i = inicios[0]
    fin = len(lineas)
    for j in range(i + 1, len(lineas)):
        m = RE_ENCABEZADO.match(lineas[j])
        if m and len(m.group(1)) <= nivel:
            fin = j
            break
    return i + 1, lineas[i:fin]


def _celdas(linea: str) -> list[str] | None:
    s = linea.strip()
    if not (s.startswith("|") and s.endswith("|")) or re.fullmatch(r"\|[\s:|-]+\|", s):
        return None
    return [c.strip() for c in s[1:-1].split("|")]


def _filas(lineas: list[str], primera: re.Pattern[str]) -> list[list[str]]:
    filas = []
    for x in lineas:
        c = _celdas(x)
        if c and primera.fullmatch(c[0]):
            filas.append(c)
    return filas


def _rango(titulo: str, prefijo: str) -> list[str]:
    """IDs del rango del título («R1–R27», «CT-01 a CT-25», «F0–F8 … F9–F10»), con el relleno de ceros con que se escriben."""
    out: list[str] = []
    for m in re.finditer(rf"{re.escape(prefijo)}(\d+)\s*(?:–|-|a)\s*{re.escape(prefijo)}(\d+)", titulo):
        a, b, ancho = int(m.group(1)), int(m.group(2)), len(m.group(1))
        out += [f"{prefijo}{i:0{ancho}d}" for i in range(a, b + 1)]
    return out


def _ubic(lista: Iterable[tuple[Any, ...]]) -> list[dict[str, Any]]:
    return [{"archivo": x[0], "linea": x[1]} for x in lista]


def _version_titulo(doc: Documento) -> str | None:
    for x in doc.lineas[:12]:
        m = re.search(r"Versión(?: óptima)? V(\d+(?:\.\d+)+)", x)
        if m:
            return m.group(1)
    return None


def _version_nombre(rel: str) -> str | None:
    m = RE_VERSION.search(Path(rel).name)
    return m.group(1) if m else None


def _levenshtein(a: str, b: str) -> int:
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def _parecido(a: str, b: str) -> int | None:
    """Menor es más parecido; None si no se parecen (criterio de DISTANCIA_PARECIDO)."""
    if a == b:
        return None
    if re.sub(r"[^A-Z0-9]", "", a.upper()) == re.sub(r"[^A-Z0-9]", "", b.upper()):
        return 0
    if a.rsplit("-", 1)[0] == b.rsplit("-", 1)[0]:
        return 1
    d = _levenshtein(a, b)
    return d if d <= DISTANCIA_PARECIDO else None


def _mas_parecido(x: str, candidatos: Iterable[str]) -> str | None:
    puntos = sorted((p, c) for c in candidatos if (p := _parecido(x, c)) is not None)
    return puntos[0][1] if puntos else None


# ----------------------------------------------------------------------------------------------- verificación
class _Hallazgos:
    def __init__(self) -> None:
        self.lista: list[dict[str, Any]] = []

    def __call__(self, clase: str, nivel: str, codigo: str, id_: str, mensaje: str,
                 ubicaciones: Iterable[tuple[Any, ...]] = ()) -> None:
        self.lista.append({"clase": clase, "nivel": nivel, "codigo": codigo, "id": id_, "mensaje": mensaje,
                           "ubicaciones": _ubic(ubicaciones)})

    def ordenados(self) -> list[dict[str, Any]]:
        orden_clase = list(CLASES)
        return sorted(self.lista, key=lambda h: (orden_clase.index(h["clase"]), NIVELES.index(h["nivel"]), _clave_id(h["id"]),
                                                 h["codigo"]))


def _clave_id(x: str) -> tuple[Any, ...]:
    return tuple(int(t) if t.isdigit() else t for t in re.split(r"(\d+)", x))


def _resumen_citas(citas: Mapping[str, list[Cita]], id_: str) -> dict[str, int]:
    lista = citas.get(id_, [])
    return {"citas": len(lista), "archivos": len({c.archivo for c in lista})}


def _comprobar_rango(h: _Hallazgos, clase: str, titulo: str, esperado: list[str], definidos: list[str], donde: str,
                     linea: tuple[str, int]) -> None:
    if not esperado:
        h(clase, "AVISO", "RANGO_SIN_TITULO", donde, f"El título de {donde} no declara un rango; no se contrasta", [linea])
        return
    for x in sorted(set(esperado) - set(definidos), key=_clave_id):
        h(clase, "ERROR", "FALTA_EN_TABLA", x, f"El título de {donde} («{titulo}») incluye {x}, que no tiene fila en su tabla",
          [linea])
    for x in sorted(set(definidos) - set(esperado), key=_clave_id):
        h(clase, "ERROR", "FUERA_DE_RANGO", x, f"{x} tiene fila en {donde} pero queda fuera del rango del título («{titulo}»)",
          [linea])
    for x in sorted({d for d in definidos if definidos.count(d) > 1}, key=_clave_id):
        h(clase, "ERROR", "FILA_DUPLICADA", x, f"{x} tiene más de una fila en {donde}", [linea])


def _limpiar_nombre(s: str) -> str:
    s = re.sub(r"\*+", "", s)
    s = re.sub(r"\s*\([^)]*\)\s*$", "", s)
    return re.sub(r"\s+", " ", s).strip()


def verificar(raiz: Path, codigo: Codigo | None = None) -> dict[str, Any]:
    """Escanea el corpus de `raiz` (la carpeta del bloque) y el código, y devuelve el informe validado contra ESQUEMA_INFORME.
    Lanza EntradaInvalida si falta una entrada o es ambigua."""
    raiz = Path(raiz)
    if not raiz.is_dir():
        raise EntradaInvalida(f"no existe la raíz del bloque: {raiz}")
    ruta_doc0 = _unico(raiz, DIR_GOBERNANZA, PATRON_DOC0, "Documento 0")
    ruta_cat = _unico(raiz, DIR_CATALOGO, PATRON_CATALOGO, "Catálogo de cálculos del Motor")
    if codigo is None:
        codigo = Codigo.desde_paquete(raiz)
    corpus = _corpus(raiz)
    por_rel = {d.rel: d for d in corpus}
    rel_doc0 = _nfc(ruta_doc0.relative_to(raiz).as_posix())
    rel_cat = _nfc(ruta_cat.relative_to(raiz).as_posix())
    doc0, cat = por_rel[rel_doc0], por_rel[rel_cat]
    h = _Hallazgos()

    # ---------------------------------------------------------------- entradas
    v_nombre, v_titulo = _version_nombre(rel_doc0), _version_titulo(doc0)
    if v_nombre is None or v_titulo is None or v_nombre != v_titulo:
        h("entradas", "AVISO", "VERSION_DOC0_DISTINTA", rel_doc0,
          f"La versión del nombre del Documento 0 ({v_nombre}) no coincide con la de su título ({v_titulo})", [(rel_doc0, 1)])

    # ---------------------------------------------------------------- (a) contratos CT
    l61, s61 = _seccion(doc0, 3, "6.1")
    ct_def = [c[0] for c in _filas(s61, re.compile(r"CT-\d+"))]
    if not ct_def:
        raise EntradaInvalida(f"{rel_doc0}: §6.1 sin tabla de contratos")
    _comprobar_rango(h, "a", s61[0], _rango(s61[0], "CT-"), ct_def, "§6.1", (rel_doc0, l61))
    citas_ct = _citas(corpus, RE_CT, "CT-{0}")
    _inexistentes(h, "a", "CT_INEXISTENTE", set(citas_ct) - set(ct_def), citas_ct,
                  lambda x: f"Se cita {x}, que no está en §6.1 del Documento 0"
                  + (" (el código sí le da canal)" if x in codigo.canales else " (tampoco lo define el código)"),
                  lambda x, c: _contexto_general(c))
    for x in sorted(set(ct_def) - codigo.canales, key=_clave_id):
        h("a", "ERROR", "CT_SIN_CANAL", x, f"{x} está en §6.1 pero no en CANALES de contratos.py: R2 rechazaría todo mensaje")
    for x in sorted((codigo.canales & set(ct_def)) - codigo.canales_admitidos, key=_clave_id):
        h("a", "ERROR", "CT_CANAL_VACIO", x, f"{x} está en CANALES pero canal_permitido no admite ningún par emisor-receptor")
    for nombre, conjunto in (("CANALES", codigo.canales), ("CANALES_V6", codigo.canales_v6),
                             ("CAMPOS_MINIMOS", codigo.campos_minimos)):
        for x in sorted(conjunto - set(ct_def), key=_clave_id):
            h("a", "ERROR", "CT_SOLO_CODIGO", x, f"{x} está en {nombre} de contratos.py pero no en §6.1 del Documento 0")
    contratos = {"titulo": s61[0].lstrip("# "), "definidos_doc0": ct_def, "definidos_codigo": sorted(codigo.canales, key=_clave_id),
                 "filas": [{"id": x, "en_doc0": x in ct_def, "canal_codigo": x in codigo.canales,
                            "canal_admitido": x in codigo.canales_admitidos, "canal_v6": x in codigo.canales_v6,
                            "campos_minimos": x in codigo.campos_minimos, **_resumen_citas(citas_ct, x)}
                           for x in sorted(set(ct_def) | codigo.canales | set(citas_ct), key=_clave_id)]}

    # ---------------------------------------------------------------- (b) reglas R
    l1, s1 = _seccion(doc0, 2, "1")
    r_def = [c[0] for c in _filas(s1, re.compile(r"R\d+"))]
    if not r_def:
        raise EntradaInvalida(f"{rel_doc0}: §1 sin tabla de reglas")
    _comprobar_rango(h, "b", s1[0], _rango(s1[0], "R"), r_def, "§1", (rel_doc0, l1))
    citas_r = _citas(corpus, RE_R, "R{0}")
    _inexistentes(h, "b", "R_INEXISTENTE", set(citas_r) - set(r_def), citas_r,
                  lambda x: f"Se cita {x}, que no está en §1 del Documento 0", lambda x, c: _contexto_general(c))
    reglas = {"titulo": s1[0].lstrip("# "), "definidas": r_def,
              "filas": [{"id": x, "en_doc0": x in r_def, **_resumen_citas(citas_r, x)}
                        for x in sorted(set(r_def) | set(citas_r), key=_clave_id)]}

    # ---------------------------------------------------------------- (c) archivos F
    l51, s51 = _seccion(doc0, 3, "5.1")
    inventario = {c[0]: _limpiar_nombre(c[1]) for c in _filas(s51, re.compile(r"[A-Z]{1,3}\d{0,2}")) if len(c) > 1}
    inventario.pop("Código", None)
    if not any(re.fullmatch(r"F\d+", k) for k in inventario):
        raise EntradaInvalida(f"{rel_doc0}: §5.1 sin inventario de archivos F")
    l73, s73 = _seccion(doc0, 3, "7.3")
    fases = _rango(s73[0], "F")
    mapa: dict[str, list[dict[str, str]]] = {}
    for d in corpus:
        if not d.rel.startswith(DIR_OPERATIVOS + "/"):
            continue
        h1 = next((x[2:].strip() for x in d.lineas if x.startswith("# ")), "")
        m = re.search(r"(?<![\w-])(F\d{1,2}|" + "|".join(re.escape(k) for k in sorted(inventario)) + r")(?![\w-])", h1)
        if not m:
            h("c", "AVISO", "H1_SIN_CODIGO", d.rel, f"El H1 de {d.rel} no lleva un código de §5.1 («{h1}»)", [(d.rel, 1)])
            continue
        nombre_h1 = _limpiar_nombre(h1[m.end():].lstrip(" —-–") or h1[:m.start()].rstrip(" —-–"))
        mapa.setdefault(m.group(1), []).append({"archivo": d.rel, "h1": h1, "nombre_h1": nombre_h1})
    filas_mapa = []
    for cod in sorted(set(inventario) | set(mapa), key=_clave_id):
        archivos = mapa.get(cod, [])
        if cod not in inventario:
            for a in archivos:
                h("c", "ERROR", "F_SOLO_ARCHIVO", cod, f"{a['archivo']} se declara {cod} en su H1, pero {cod} no está en §5.1",
                  [(a["archivo"], 1)])
        elif not archivos:
            if re.fullmatch(r"F\d+", cod):
                h("c", "ERROR", "F_SIN_ARCHIVO", cod, f"{cod} («{inventario[cod]}») está en §5.1 pero ningún archivo de "
                  f"{DIR_OPERATIVOS}/ lo declara en su H1", [(rel_doc0, l51)])
            else:
                h("c", "INFO", "CODIGO_FUERA_DE_05", cod, f"{cod} («{inventario[cod]}») no es un archivo de {DIR_OPERATIVOS}/",
                  [(rel_doc0, l51)])
        if len(archivos) > 1:
            h("c", "ERROR", "F_DUPLICADO", cod, f"{cod} lo declaran {len(archivos)} archivos en su H1",
              [(a["archivo"], 1) for a in archivos])
        for a in archivos:
            if cod in inventario and a["nombre_h1"].casefold() != inventario[cod].casefold():
                h("c", "AVISO", "F_NOMBRE_DISTINTO", cod, f"§5.1 llama a {cod} «{inventario[cod]}» y el H1 de {a['archivo']}, "
                  f"«{a['nombre_h1']}»", [(a["archivo"], 1), (rel_doc0, l51)])
        filas_mapa.append({"codigo": cod, "nombre_doc0": inventario.get(cod), "archivo": archivos[0]["archivo"] if archivos else None,
                           "nombre_h1": archivos[0]["nombre_h1"] if archivos else None})
    # el H1 de un archivo de 05 declara su código (se contrasta en el mapa): no es una cita
    citas_f = {k: v for k, v in ((k, [c for c in v if not (c.archivo.startswith(DIR_OPERATIVOS + "/") and c.texto.startswith("# "))])
                                 for k, v in _citas(corpus, RE_F, "F{0}").items()) if v}
    locales: dict[str, dict[str, str]] = {}   # documento → {«F05»: «ORQ-F05»} de las filas de su propia tabla de funciones
    for d in corpus:
        for x in d.lineas:
            m = RE_FUNCION_LOCAL.match(x)
            if m:
                locales.setdefault(d.rel, {}).setdefault(m.group(1), x.split("|")[1].strip())

    def contexto_f(x: str, c: Cita) -> str | None:
        local = locales.get(c.archivo, {}).get(x)
        return f"abreviatura de la función {local} del mismo documento" if local else _contexto_general(c)

    _inexistentes(h, "c", "F_INEXISTENTE", set(citas_f) - set(inventario) - set(fases), citas_f,
                  lambda x: f"Se cita {x}, que no es un archivo de §5.1 ni una fase de §7.3", contexto_f)
    archivos_f = {"titulo_fases": s73[0].lstrip("# "), "fases": fases, "mapa": filas_mapa,
                  "citas": [{"id": x, "archivo": x in inventario, "fase": x in fases, **_resumen_citas(citas_f, x)}
                            for x in sorted(set(citas_f) | {k for k in inventario if re.fullmatch(r"F\d+", k)}, key=_clave_id)]}

    # ---------------------------------------------------------------- (d) fichas del Catálogo
    fichas = _fichas(h, cat, corpus, codigo, rel_cat)

    # ---------------------------------------------------------------- (e) referencias de los archivos operativos
    referencias = _referencias(h, corpus)

    # ---------------------------------------------------------------- (f) puertas PS
    l93, s93 = _seccion(doc0, 3, "9.3")
    ps_def = [c[0].split()[0] for c in _filas(s93, re.compile(r"PS\d+(?:\s.*)?"))]
    if not ps_def:
        raise EntradaInvalida(f"{rel_doc0}: §9.3 sin tabla de puertas")
    _comprobar_rango(h, "f", s93[0], _rango(s93[0], "PS"), ps_def, "§9.3", (rel_doc0, l93))
    citas_ps = _citas(corpus, RE_PS, "PS{0}")
    _inexistentes(h, "f", "PS_INEXISTENTE", set(citas_ps) - set(ps_def), citas_ps,
                  lambda x: f"Se cita {x}, que no está en §9.3 del Documento 0", lambda x, c: _contexto_general(c))
    puertas = {"titulo": s93[0].lstrip("# "), "definidas": ps_def,
               "filas": [{"id": x, "en_doc0": x in ps_def, **_resumen_citas(citas_ps, x)}
                         for x in sorted(set(ps_def) | set(citas_ps), key=_clave_id)]}

    hallazgos = h.ordenados()
    resumen = {c: {n: sum(1 for x in hallazgos if x["clase"] == c and x["nivel"] == n) for n in NIVELES} for c in CLASES}
    huella = hashlib.sha256("".join(f"{d.rel}\t{d.sha256}\n" for d in corpus).encode("utf-8")).hexdigest()
    informe = {
        "verificador": {"nombre": "verificador_ids", "version": VERSION, "ticket": "T-157"},
        "entradas": {
            "raiz": _nfc(raiz.resolve().name),
            "documento_0": {"archivo": rel_doc0, "version_nombre": v_nombre, "version_titulo": v_titulo, "sha256": doc0.sha256},
            "catalogo": {"archivo": rel_cat, "version_nombre": _version_nombre(rel_cat), "sha256": cat.sha256},
            "codigo": dict(sorted(codigo.fuentes.items())),
            "md_escaneados": len(corpus),
            "huella_corpus": huella,
            "excluidos": [f"{DIR_EJECUTOR}/", f"{PREFIJO_HISTORICO}*/"],
            "secciones_doc0": {"§1": l1, "§5.1": l51, "§6.1": l61, "§7.3 (solo el título)": l73, "§9.3": l93},
        },
        "resumen": resumen,
        "errores": sum(v["ERROR"] for v in resumen.values()),
        "contratos": contratos, "reglas": reglas, "archivos": archivos_f, "fichas": fichas, "referencias": referencias,
        "puertas": puertas, "hallazgos": hallazgos,
    }
    validar_informe(informe)
    return informe


def _fichas(h: _Hallazgos, cat: Documento, corpus: list[Documento], codigo: Codigo, rel_cat: str) -> dict[str, Any]:
    lineas = cat.lineas
    encabezados: dict[str, int] = {}
    seccion_de: dict[str, str] = {}
    secciones: list[dict[str, Any]] = []
    for n, x in enumerate(lineas, 1):
        if x.startswith("## "):
            secciones.append({"titulo": x[3:].strip(), "linea": n, "fichas": 0})
        m = RE_ENCABEZADO_FICHA.match(x)
        if m:
            if m.group(1) in encabezados:
                h("d", "ERROR", "FICHA_DUPLICADA", m.group(1), f"{m.group(1)} tiene más de un encabezado en el Catálogo",
                  [(rel_cat, encabezados[m.group(1)]), (rel_cat, n)])
            encabezados.setdefault(m.group(1), n)
            if secciones:
                secciones[-1]["fichas"] += 1
                seccion_de.setdefault(m.group(1), secciones[-1]["titulo"])
    if not encabezados:
        raise EntradaInvalida(f"{rel_cat}: el Catálogo no tiene fichas (encabezados «### ID»)")
    # índice §4: la columna «Madurez» por su cabecera
    l4, s4 = _seccion(cat, 2, "4")
    cab = next((c for c in map(_celdas, s4) if c and "Madurez" in c), None)
    if cab is None:
        raise EntradaInvalida(f"{rel_cat}: §4 sin tabla con columna «Madurez»")
    col = cab.index("Madurez")
    indice: dict[str, str] = {}
    for c in (c for c in map(_celdas, s4) if c and re.fullmatch(RE_ID_FICHA, c[0]) and len(c) > col):
        indice.setdefault(c[0], c[col])
    v_nombre = _version_nombre(rel_cat)
    m_decl = re.search(r"`catalog_version`\s+(\S+?)[.,;]?(?:\s|$)", cat.texto)
    v_decl = m_decl.group(1) if m_decl else None
    if v_decl is None:
        h("d", "AVISO", "CATALOGO_SIN_VERSION", rel_cat, "El Catálogo no declara `catalog_version`", [(rel_cat, 1)])
    for nombre, v in (("el nombre del archivo", v_nombre), ("`catalog_version` del Catálogo", v_decl)):
        if v is not None and v != codigo.catalog_version:
            h("d", "ERROR", "CATALOG_VERSION_DISTINTA", "CATALOG_VERSION",
              f"CATALOG_VERSION del código es {codigo.catalog_version} y {nombre} dice {v}", [(rel_cat, 1)])
    if codigo.ruta_catalogo and _nfc("/".join(codigo.ruta_catalogo)) != rel_cat:
        h("d", "ERROR", "RUTA_CATALOGO_DISTINTA", "RUTA_CATALOGO",
          f"El código lee la madurez de {'/'.join(codigo.ruta_catalogo)} y el Catálogo vigente es {rel_cat}")
    m_total = re.search(r"^Total: (\d+) fichas", cat.texto, re.MULTILINE)
    total = int(m_total.group(1)) if m_total else None
    if total is not None and total != len(encabezados):
        h("d", "ERROR", "TOTAL_DISTINTO", "Total", f"El Catálogo declara {total} fichas y tiene {len(encabezados)} encabezados",
          [(rel_cat, cat.texto[:m_total.start()].count("\n") + 1)] if m_total else [])
    for s in secciones:
        s["nueva_en_version"] = bool(v_nombre and f"V{v_nombre}" in s["titulo"])
    secciones = [s for s in secciones if s["fichas"]]

    lista_codigo = list(codigo.fichas_catalogo)
    for x in sorted({f for f in lista_codigo if lista_codigo.count(f) > 1}, key=_clave_id):
        h("d", "ERROR", "FICHA_DUPLICADA_CODIGO", x, f"{x} aparece más de una vez en FICHAS_CATALOGO")
    en_lista, con_manejador = set(lista_codigo), set(codigo.manejadores) | set(codigo.servicios_ct10)
    del_codigo = en_lista | con_manejador | set(codigo.documentadas_con_codigo)
    cat_ids = set(encabezados)
    # emparejar lo que el código tiene y el Catálogo no con la ficha del Catálogo más parecida que el código no tenga
    libres = cat_ids - del_codigo
    parejas: dict[str, str] = {}
    for x in sorted(del_codigo - cat_ids, key=_clave_id):
        p = _mas_parecido(x, libres)
        if p is not None:
            parejas[x] = p
            libres.discard(p)
    pareja_de = {v: k for k, v in parejas.items()}
    filas = []
    for x in sorted(cat_ids | set(indice) | del_codigo, key=_clave_id):
        manejador = "CT-09" if x in codigo.manejadores else "CT-10" if x in codigo.servicios_ct10 else None
        madurez = indice.get(x)
        if x in cat_ids:
            clase = "ID_DISTINTO" if x in pareja_de else "IMPLEMENTADO" if manejador else "SOLO_CATALOGO"
        elif x in del_codigo:
            clase = "ID_DISTINTO" if x in parejas else "SOLO_CODIGO"
        else:
            clase = "SOLO_CATALOGO"
        similar = parejas.get(x) or pareja_de.get(x)
        ubic_cat = [(rel_cat, encabezados[x])] if x in cat_ids else []
        if clase == "ID_DISTINTO" and x in parejas:
            h("d", "ERROR", "ID_DISTINTO", x, f"El código usa {x} y el Catálogo tiene {similar}: mismo método con otro ID",
              [(rel_cat, encabezados[parejas[x]])])
        elif clase == "SOLO_CODIGO":
            h("d", "ERROR", "SOLO_CODIGO", x, f"{x} está en el código ({_donde(x, codigo)}) sin ficha en el Catálogo")
        elif clase == "SOLO_CATALOGO" and x in cat_ids:
            nivel = "ERROR" if madurez and _citable(madurez) else "AVISO"
            h("d", nivel, "SOLO_CATALOGO", x, f"{x} tiene ficha en el Catálogo (madurez «{madurez}») y el código no la sirve"
              + ("" if x in en_lista else "; tampoco está en FICHAS_CATALOGO (respondería OPERACION_SIN_FICHA)"), ubic_cat)
        if x in cat_ids and x not in indice:
            h("d", "ERROR", "FICHA_SIN_INDICE", x, f"{x} tiene encabezado en el Catálogo pero no fila en el índice §4", ubic_cat)
        if x in indice and x not in cat_ids:
            h("d", "ERROR", "INDICE_SIN_FICHA", x, f"{x} está en el índice §4 del Catálogo pero no tiene encabezado «### {x}»",
              [(rel_cat, l4)])
        if x in cat_ids and x not in en_lista and clase != "ID_DISTINTO":
            h("d", "ERROR", "FALTA_EN_FICHAS_CATALOGO", x, f"{x} tiene ficha en el Catálogo pero no está en FICHAS_CATALOGO "
              "(el código la marcaría op_sin_ficha)", ubic_cat)
        if manejador and x in cat_ids and not (madurez and _citable(madurez)):
            h("d", "AVISO", "CODIGO_SIN_PROMOVER", x, f"{x} tiene manejador pero el índice §4 la da por «{madurez}»: no se sirve",
              ubic_cat)
        if x in codigo.documentadas_con_codigo:
            h("d", "INFO", "DOCUMENTADA_CON_CODIGO", x, f"{x} está en DOCUMENTADAS_CON_CODIGO: tiene código y no se sirve")
        if codigo.madurez_leida is not None and x in indice and codigo.madurez_leida.get(x) != madurez:
            h("d", "ERROR", "MADUREZ_LEIDA_DISTINTA", x, f"madurez_catalogo() del código lee «{codigo.madurez_leida.get(x)}» "
              f"para {x} y el índice §4 dice «{madurez}»", [(rel_cat, l4)])
        servible = None if codigo.servibles is None else x in codigo.servibles
        if servible is False and manejador == "CT-09" and madurez and _citable(madurez) and x not in codigo.documentadas_con_codigo:
            h("d", "AVISO", "NO_SERVIBLE_HOY", x, f"{x} tiene manejador y madurez citable, pero servible() da falso en este entorno"
              " (dependencia opcional ausente)", ubic_cat)
        filas.append({"id": x, "clase": clase, "seccion": seccion_de.get(x), "madurez_indice": madurez,
                      "en_fichas_catalogo": x in en_lista, "manejador": manejador, "servible": servible, "similar_a": similar})
    for k, v in sorted(codigo.alternativas.items()):
        for y in (k, v):
            if y not in cat_ids:
                h("d", "ERROR", "ALTERNATIVA_SIN_FICHA", y, f"ALTERNATIVAS del código cita {y} ({k} → {v}), que no tiene ficha")
    # fichas citadas en el corpus (familias de los ID del Catálogo y del código)
    # la forma de los segmentos intermedios sale de los ID del Catálogo (hoy todos empiezan por letra: «FX-TREND-001»)
    familias = sorted({x.split("-")[0] for x in cat_ids | del_codigo}, key=len, reverse=True)
    medio = r"[A-Z][A-Z0-9]*" if all(re.fullmatch(r"[A-Z][A-Z0-9]*", s) for x in cat_ids for s in x.split("-")[1:-1]) \
        else r"[A-Z0-9]+"
    re_cita = re.compile(r"(?<![\w-])((?:" + "|".join(map(re.escape, familias)) + rf")(?:-{medio})+-\d{{3}})(?![\w-])")
    # las filas del índice §4 son declaraciones (se contrastan arriba con los encabezados), no citas
    citas = {k: v for k, v in ((k, [c for c in v if not (c.archivo == rel_cat and l4 <= c.linea < l4 + len(s4))])
                               for k, v in _citas(corpus, re_cita).items()) if v}

    def contexto_d(x: str, c: Cita) -> str | None:
        m = RE_CAMPO_JSON.search(c.texto[:c.inicio])
        if m and m.group(1) not in CAMPOS_FICHA:
            return f"valor del campo JSON «{m.group(1)}», que no es el de una ficha"
        return _contexto_general(c)

    _inexistentes(h, "d", "FICHA_CITADA_INEXISTENTE", set(citas) - cat_ids, citas,
                  lambda x: f"Se cita la ficha {x}, que no está en el Catálogo"
                  + (f" (¿{p}?)" if (p := _mas_parecido(x, cat_ids)) else ""), contexto_d)
    # menciones de una versión del Catálogo distinta de la vigente
    menciones: dict[str, list[tuple[str, int]]] = {}
    for d in corpus:
        for n, linea in enumerate(d.lineas, 1):
            for m in RE_MENCION_CATALOGO.finditer(linea):
                v = m.group(1) or m.group(2)
                if v_nombre and v != v_nombre:
                    menciones.setdefault(v, []).append((d.rel, n))
    filas_menciones = []
    for v, ubic in sorted(menciones.items()):
        en_prompts = [u for u in ubic if u[0].startswith(DIR_PROMPTS + "/")]
        h("d", "AVISO", "MENCION_OTRA_VERSION", f"Catálogo V{v}",
          f"{len(ubic)} menciones a la versión {v} del Catálogo («Catálogo V{v}» o `catalog_version` {v}; {len(en_prompts)} en "
          f"{DIR_PROMPTS}/); el vigente es V{v_nombre}", ubic)
        filas_menciones.append({"version": v, "menciones": len(ubic), "en_prompts": len(en_prompts),
                                "archivos": sorted({a for a, _ in ubic})})
    for v, lit in sorted({(v, lit) for _, _, v, lit in codigo.versiones_en_codigo if v_nombre and v != v_nombre}):
        ubic = [(a, n) for a, n, v2, l2 in codigo.versiones_en_codigo if (v2, l2) == (v, lit)]
        if lit:
            h("d", "ERROR", "CATALOG_VERSION_LITERAL", f"catalog_version {v}",
              f"El código escribe `catalog_version` {v} en {len(ubic)} sitio(s) y el Catálogo vigente es V{v_nombre} "
              f"(CATALOG_VERSION = {codigo.catalog_version})", ubic)
        else:
            h("d", "AVISO", "MENCION_OTRA_VERSION_CODIGO", f"Catálogo V{v} (código)",
              f"{len(ubic)} mención(es) a «Catálogo V{v}» en comentarios o docstrings del código; el vigente es V{v_nombre}", ubic)
    nuevas = sum(s["fichas"] for s in secciones if s["nueva_en_version"])
    return {"catalog_version_codigo": codigo.catalog_version, "catalog_version_declarada": v_decl, "version_nombre": v_nombre,
            "total_declarado": total, "encabezados": len(cat_ids), "en_indice": len(indice), "en_fichas_catalogo": len(en_lista),
            "manejadores_ct09": len(codigo.manejadores), "servicios_ct10": sorted(codigo.servicios_ct10),
            "secciones": secciones, "nuevas_en_version": nuevas, "anteriores_a_version": len(cat_ids) - nuevas,
            "conteo_clases": {c: sum(1 for f in filas if f["clase"] == c) for c in CLASES_FICHA},
            "filas": filas, "menciones_otra_version": filas_menciones}


def _citable(madurez: str) -> bool:
    return madurez.startswith(("IMPLEMENTADO", "VALIDADO"))


def _donde(x: str, codigo: Codigo) -> str:
    sitios = [n for n, s in (("FICHAS_CATALOGO", set(codigo.fichas_catalogo)), ("IMPLEMENTADAS", codigo.manejadores),
                             ("SERVICIOS_CT10", codigo.servicios_ct10),
                             ("DOCUMENTADAS_CON_CODIGO", codigo.documentadas_con_codigo)) if x in s]
    return ", ".join(sitios)


def _referencias(h: _Hallazgos, corpus: list[Documento]) -> dict[str, Any]:
    definidas: dict[str, tuple[str, int]] = {}
    bajas: dict[str, tuple[str, int, str | None]] = {}
    for d in corpus:
        if not d.rel.startswith(DIR_OPERATIVOS + "/"):
            continue
        en_bajas = False
        for n, x in enumerate(d.lineas, 1):
            m = RE_ENCABEZADO.match(x)
            if m and len(m.group(1)) == 2:
                en_bajas = "Registro de bajas" in m.group(2)
            if m and len(m.group(1)) >= 2:
                r = re.match(r"(RF-\d+|TA-\d+|TM-\d+|TF-\d+|ANA-DOC-\d+|DOC-MOT-\d+)(?![\w-])", m.group(2))
                if r:
                    definidas.setdefault(r.group(1), (d.rel, n))
            c = _celdas(x) if en_bajas else None
            if c and RE_REFERENCIA.fullmatch(c[0]):
                sust = c[-1] if len(c) > 1 and RE_REFERENCIA.fullmatch(c[-1]) else None
                bajas.setdefault(c[0], (d.rel, n, sust))
    citadores = [d for d in corpus if d.rel.startswith((DIR_PROMPTS + "/", DIR_FUNCIONES + "/"))]
    citas = _citas(citadores, RE_REFERENCIA)
    for x in sorted(set(definidas) & set(bajas), key=_clave_id):
        h("e", "AVISO", "REF_DEFINIDA_Y_DE_BAJA", x, f"{x} tiene entrada y además figura en un Registro de bajas",
          [definidas[x][:2], bajas[x][:2]])
    cifras: dict[str, set[int]] = {}   # prefijo → número de cifras de sus entradas (RF-0001: 4)
    for x in definidas:
        p, num = x.rsplit("-", 1)
        cifras.setdefault(p, set()).add(len(num))
    for x in sorted(set(citas), key=_clave_id):
        p, num = x.rsplit("-", 1)
        if x in definidas:
            continue
        if x in bajas:
            sust = bajas[x][2]
            h("e", "AVISO", "REF_DE_BAJA", x, f"Se cita {x}, dada de baja en {bajas[x][0]}"
              + (f" (sustituta {sust})" if sust else " (sin sustituta)"), citas[x])
        elif p in cifras and len(num) not in cifras[p]:
            h("e", "AVISO", "REF_FORMA_DISTINTA", x, f"{x} no tiene la forma de las entradas {p}- "
              f"({'/'.join(map(str, sorted(cifras[p])))} cifras): probablemente es otro identificador", citas[x])
        else:
            h("e", "ERROR", "REF_INEXISTENTE", x, f"Se cita {x}, que no tiene entrada en {DIR_OPERATIVOS}/", citas[x])
    prefijos: dict[str, dict[str, Any]] = {}
    for x, ubic in citas.items():
        p = x.rsplit("-", 1)[0]
        e = prefijos.setdefault(p, {"prefijo": p, "citas": 0, "distintas": 0, "existentes": 0, "de_baja": 0, "inexistentes": 0,
                                         "otra_forma": 0})
        e["citas"] += len(ubic)
        e["distintas"] += 1
        forma = p not in cifras or len(x.rsplit("-", 1)[1]) in cifras[p]
        e["existentes" if x in definidas else "de_baja" if x in bajas else "inexistentes" if forma else "otra_forma"] += 1
    definidas_por: dict[str, set[str]] = {}
    for x, (archivo, _) in definidas.items():
        definidas_por.setdefault(x.rsplit("-", 1)[0], set()).add(archivo)
    return {"citadores": [f"{DIR_PROMPTS}/", f"{DIR_FUNCIONES}/"], "definidas": len(definidas), "de_baja": len(bajas),
            "definidas_en": {p: sorted(a) for p, a in sorted(definidas_por.items())},
            "prefijos": [prefijos[p] for p in sorted(prefijos)]}


# ----------------------------------------------------------------------------------------------- esquema del informe
_UBIC = {"type": "object", "required": ["archivo", "linea"], "additionalProperties": False,
         "properties": {"archivo": {"type": "string", "minLength": 1}, "linea": {"type": "integer", "minimum": 1}}}
_CONTEO = {"type": "object", "required": list(NIVELES), "additionalProperties": False,
           "properties": {n: {"type": "integer", "minimum": 0} for n in NIVELES}}
_FILA_CITAS = {"citas": {"type": "integer", "minimum": 0}, "archivos": {"type": "integer", "minimum": 0}}
_SHA = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
_VER = {"type": ["string", "null"]}
ESQUEMA_INFORME: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Informe de consistencia de identificadores del Bloque A (T-157)",
    "type": "object",
    "required": ["verificador", "entradas", "resumen", "errores", "contratos", "reglas", "archivos", "fichas", "referencias",
                 "puertas", "hallazgos"],
    "additionalProperties": False,
    "properties": {
        "verificador": {"type": "object", "required": ["nombre", "version", "ticket"],
                        "properties": {"nombre": {"const": "verificador_ids"}, "version": {"type": "string"},
                                       "ticket": {"const": "T-157"}}},
        "entradas": {"type": "object", "required": ["raiz", "documento_0", "catalogo", "codigo", "md_escaneados", "huella_corpus",
                                                    "excluidos", "secciones_doc0"],
                     "properties": {
                         "documento_0": {"type": "object", "required": ["archivo", "version_nombre", "version_titulo", "sha256"],
                                         "properties": {"archivo": {"type": "string"}, "version_nombre": _VER,
                                                        "version_titulo": _VER, "sha256": _SHA}},
                         "catalogo": {"type": "object", "required": ["archivo", "version_nombre", "sha256"],
                                      "properties": {"archivo": {"type": "string"}, "version_nombre": _VER, "sha256": _SHA}},
                         "codigo": {"type": "object", "additionalProperties": _SHA},
                         "md_escaneados": {"type": "integer", "minimum": 1},
                         "huella_corpus": _SHA,
                         "secciones_doc0": {"type": "object", "additionalProperties": {"type": "integer", "minimum": 1}}}},
        "resumen": {"type": "object", "required": list(CLASES), "additionalProperties": False,
                    "properties": {c: _CONTEO for c in CLASES}},
        "errores": {"type": "integer", "minimum": 0},
        "contratos": {"type": "object", "required": ["titulo", "definidos_doc0", "definidos_codigo", "filas"],
                      "properties": {"filas": {"type": "array", "items": {
                          "type": "object", "required": ["id", "en_doc0", "canal_codigo", "canal_admitido", "canal_v6",
                                                         "campos_minimos", "citas", "archivos"],
                          "properties": {"id": {"type": "string", "pattern": "^CT-\\d+$"}, **_FILA_CITAS}}}}},
        "reglas": {"type": "object", "required": ["titulo", "definidas", "filas"],
                   "properties": {"filas": {"type": "array", "items": {
                       "type": "object", "required": ["id", "en_doc0", "citas", "archivos"],
                       "properties": {"id": {"type": "string", "pattern": "^R\\d+$"}, **_FILA_CITAS}}}}},
        "archivos": {"type": "object", "required": ["titulo_fases", "fases", "mapa", "citas"],
                     "properties": {"mapa": {"type": "array", "items": {
                         "type": "object", "required": ["codigo", "nombre_doc0", "archivo", "nombre_h1"]}}}},
        "fichas": {"type": "object",
                   "required": ["catalog_version_codigo", "catalog_version_declarada", "version_nombre", "total_declarado",
                                "encabezados", "en_indice", "en_fichas_catalogo", "manejadores_ct09", "servicios_ct10",
                                "secciones", "nuevas_en_version", "anteriores_a_version", "conteo_clases", "filas",
                                "menciones_otra_version"],
                   "properties": {
                       "conteo_clases": {"type": "object", "required": list(CLASES_FICHA), "additionalProperties": False,
                                         "properties": {c: {"type": "integer", "minimum": 0} for c in CLASES_FICHA}},
                       "filas": {"type": "array", "items": {
                           "type": "object",
                           "required": ["id", "clase", "seccion", "madurez_indice", "en_fichas_catalogo", "manejador", "servible",
                                        "similar_a"],
                           "properties": {"clase": {"enum": list(CLASES_FICHA)},
                                          "manejador": {"enum": ["CT-09", "CT-10", None]},
                                          "servible": {"type": ["boolean", "null"]}}}}}},
        "referencias": {"type": "object", "required": ["citadores", "definidas", "de_baja", "definidas_en", "prefijos"]},
        "puertas": {"type": "object", "required": ["titulo", "definidas", "filas"]},
        "hallazgos": {"type": "array", "items": {
            "type": "object", "required": ["clase", "nivel", "codigo", "id", "mensaje", "ubicaciones"],
            "additionalProperties": False,
            "properties": {"clase": {"enum": list(CLASES)}, "nivel": {"enum": list(NIVELES)},
                           "codigo": {"type": "string", "pattern": "^[A-Z0-9_]+$"}, "id": {"type": "string", "minLength": 1},
                           "mensaje": {"type": "string", "minLength": 1}, "ubicaciones": {"type": "array", "items": _UBIC}}}},
    },
}


def validar_informe(informe: Mapping[str, Any]) -> None:
    """Falla (jsonschema.ValidationError) si el informe no cumple ESQUEMA_INFORME o si su resumen no cuadra con sus hallazgos."""
    jsonschema.validate(informe, ESQUEMA_INFORME, cls=jsonschema.Draft202012Validator)
    for c in CLASES:
        for n in NIVELES:
            real = sum(1 for x in informe["hallazgos"] if x["clase"] == c and x["nivel"] == n)
            if informe["resumen"][c][n] != real:
                raise jsonschema.ValidationError(f"resumen[{c}][{n}] = {informe['resumen'][c][n]} y hay {real} hallazgos")
    if informe["errores"] != sum(informe["resumen"][c]["ERROR"] for c in CLASES):
        raise jsonschema.ValidationError("«errores» no cuadra con el resumen")


# ----------------------------------------------------------------------------------------------- salidas
def a_json(informe: Mapping[str, Any]) -> str:
    validar_informe(informe)
    return json.dumps(informe, ensure_ascii=False, indent=1, sort_keys=False) + "\n"


def _si(b: bool | None) -> str:
    return "—" if b is None else "sí" if b else "no"


def _tabla(cab: list[str], filas: Iterable[Iterable[Any]]) -> list[str]:
    out = ["| " + " | ".join(cab) + " |", "|" + "---|" * len(cab)]
    for f in filas:
        out.append("| " + " | ".join(str("—" if v is None else v).replace("|", "\\|") for v in f) + " |")
    return out


def _ubic_md(u: list[dict[str, Any]], tope: int = 6) -> str:
    if not u:
        return "—"
    partes = [f"`{x['archivo']}:{x['linea']}`" for x in u[:tope]]
    return ", ".join(partes) + (f" y {len(u) - tope} más" if len(u) > tope else "")


def a_markdown(informe: Mapping[str, Any]) -> str:
    validar_informe(informe)
    e, hall = informe["entradas"], informe["hallazgos"]
    md = ["# Informe de consistencia de identificadores del Bloque A", "",
          (f"Generado por `bloque_a/herramientas/verificador_ids.py` {informe['verificador']['version']} (T-157). Todo dato sale "
           "del corpus y del código escaneados; las huellas permiten comprobar que se leyó exactamente esto."), "",
          "## Entradas", ""]
    md += _tabla(["Entrada", "Archivo", "Versión", "SHA-256"], [
        ["Documento 0", f"`{e['documento_0']['archivo']}`",
         f"V{e['documento_0']['version_nombre']} (título: V{e['documento_0']['version_titulo']})", f"`{e['documento_0']['sha256']}`"],
        ["Catálogo", f"`{e['catalogo']['archivo']}`", f"V{e['catalogo']['version_nombre']}", f"`{e['catalogo']['sha256']}`"],
        *[["Código", f"`{k}`", "—", f"`{v}`"] for k, v in e["codigo"].items()],
        ["Corpus", f"{e['md_escaneados']} `.md` (sin {', '.join(e['excluidos'])})", "—", f"`{e['huella_corpus']}`"]])
    md += ["", "Secciones del Documento 0 leídas (línea del título): "
           + ", ".join(f"{k} l. {v}" for k, v in e["secciones_doc0"].items()) + ".", "", "## Resumen", ""]
    md += _tabla(["Clase", "Errores", "Avisos", "Info"],
                 [[f"{k} · {v}" if k != "entradas" else v, *(informe["resumen"][k][n] for n in NIVELES)] for k, v in CLASES.items()])
    md += ["", f"**Total de errores: {informe['errores']}.**", ""]

    def hallazgos_de(clase: str) -> list[str]:
        hs = [x for x in hall if x["clase"] == clase]
        if not hs:
            return ["", "Sin hallazgos.", ""]
        return ["", *_tabla(["Nivel", "Código", "ID", "Motivo", "Dónde"],
                            [[x["nivel"], x["codigo"], x["id"], x["mensaje"], _ubic_md(x["ubicaciones"])] for x in hs]), ""]

    if any(x["clase"] == "entradas" for x in hall):
        md += ["## Entradas: hallazgos", *hallazgos_de("entradas")]
    c = informe["contratos"]
    md += ["## (a) Contratos CT", "", (f"§6.1: «{c['titulo']}». Definidos en §6.1: {len(c['definidos_doc0'])}; con canal en "
                                       f"`contratos.py`: {len(c['definidos_codigo'])}."), ""]
    md += _tabla(["CT", "§6.1", "CANALES", "canal_permitido", "CANALES_V6", "CAMPOS_MINIMOS", "Citas", "Archivos"],
                 [[f["id"], _si(f["en_doc0"]), _si(f["canal_codigo"]), _si(f["canal_admitido"]), _si(f["canal_v6"]),
                   _si(f["campos_minimos"]), f["citas"], f["archivos"]] for f in c["filas"]])
    md += hallazgos_de("a")
    r = informe["reglas"]
    md += ["## (b) Reglas R", "", f"§1: «{r['titulo']}». Definidas: {len(r['definidas'])}.", ""]
    md += _tabla(["Regla", "§1", "Citas", "Archivos"], [[f["id"], _si(f["en_doc0"]), f["citas"], f["archivos"]] for f in r["filas"]])
    md += hallazgos_de("b")
    a = informe["archivos"]
    md += ["## (c) Archivos F", "", ("Mapa código de §5.1 → archivo real de `05_Archivos_operativos`, por su H1 (la numeración "
                                      "no coincide con el nombre del archivo):"), ""]
    md += _tabla(["Código", "Nombre en §5.1", "Archivo real (por H1)", "Nombre en el H1"],
                 [[f["codigo"], f["nombre_doc0"], f"`{f['archivo']}`" if f["archivo"] else None, f["nombre_h1"]] for f in a["mapa"]])
    md += ["", (f"Las fases salen del título de §7.3 («{a['titulo_fases']}»): {', '.join(a['fases'])}. Una cita «F3» puede ser "
                "el archivo o la fase; solo es error si no es ninguna de las dos."), ""]
    md += _tabla(["F", "Archivo de §5.1", "Fase de §7.3", "Citas", "Archivos"],
                 [[f["id"], _si(f["archivo"]), _si(f["fase"]), f["citas"], f["archivos"]] for f in a["citas"]])
    md += hallazgos_de("c")
    f_ = informe["fichas"]
    md += ["## (d) Fichas del Catálogo", "",
           (f"`CATALOG_VERSION` del código: {f_['catalog_version_codigo']}; `catalog_version` del Catálogo: "
            f"{f_['catalog_version_declarada']}; nombre del archivo: V{f_['version_nombre']}. Encabezados `### ID`: "
            f"{f_['encabezados']} (el Catálogo declara {f_['total_declarado']}); filas del índice §4: {f_['en_indice']}; "
            f"`FICHAS_CATALOGO`: {f_['en_fichas_catalogo']}; manejadores CT-09 (`IMPLEMENTADAS`): {f_['manejadores_ct09']}; "
            f"servicios CT-10 (`SERVICIOS_CT10`): {', '.join(f_['servicios_ct10']) or 'ninguno'}."), "",
           "Clases: " + ", ".join(f"{k} {v}" for k, v in f_["conteo_clases"].items()) + ".", "",
           (f"Fichas por sección del Catálogo (las de secciones con «V{f_['version_nombre']}» en el título son las nuevas de esa "
            f"versión: {f_['nuevas_en_version']}; las demás, {f_['anteriores_a_version']}):"), ""]
    md += _tabla(["Sección", "Fichas", f"Nueva en V{f_['version_nombre']}"],
                 [[s["titulo"], s["fichas"], _si(s["nueva_en_version"])] for s in f_["secciones"]])
    md += ["", "Menciones a otra versión del Catálogo:", ""]
    md += (_tabla(["Versión", "Menciones", f"En {DIR_PROMPTS}/", "Archivos"],
                  [[f"V{m['version']}", m["menciones"], m["en_prompts"], "; ".join(f"`{x}`" for x in m["archivos"])]
                   for m in f_["menciones_otra_version"]]) if f_["menciones_otra_version"] else ["Ninguna."])
    md += ["", "Ficha a ficha:", ""]
    md += _tabla(["Ficha", "Clase", "Madurez (índice §4)", "FICHAS_CATALOGO", "Manejador", "servible()", "Parecida a"],
                 [[x["id"], x["clase"], x["madurez_indice"], _si(x["en_fichas_catalogo"]), x["manejador"], _si(x["servible"]),
                   x["similar_a"]] for x in f_["filas"]])
    md += hallazgos_de("d")
    rf = informe["referencias"]
    md += ["## (e) Referencias de los archivos operativos", "",
           f"Citadas en {', '.join(f'`{x}`' for x in rf['citadores'])}; entradas en `05_Archivos_operativos`: {rf['definidas']} "
           f"(más {rf['de_baja']} en los Registros de bajas). Dónde se definen: "
           + "; ".join(f"{p} en {', '.join(f'`{x}`' for x in a_)}" for p, a_ in rf["definidas_en"].items()) + ".", ""]
    md += (_tabla(["Prefijo", "Citas", "ID distintos", "Existen", "De baja", "No existen", "Otra forma"],
                  [[p["prefijo"], p["citas"], p["distintas"], p["existentes"], p["de_baja"], p["inexistentes"], p["otra_forma"]]
                   for p in rf["prefijos"]]) if rf["prefijos"] else ["Ninguna cita."])
    md += hallazgos_de("e")
    p_ = informe["puertas"]
    md += ["## (f) Puertas PS", "", f"§9.3: «{p_['titulo']}». Definidas: {len(p_['definidas'])}.", ""]
    md += _tabla(["Puerta", "§9.3", "Citas", "Archivos"], [[f["id"], _si(f["en_doc0"]), f["citas"], f["archivos"]] for f in p_["filas"]])
    md += hallazgos_de("f")
    return "\n".join(md).rstrip() + "\n"


def actualizar_auditoria(ruta: Path, markdown: str) -> None:
    """Sustituye el bloque entre MARCA_INICIO y MARCA_FIN. Sin las dos marcas (una vez cada una y en orden), falla cerrado."""
    texto = _leer(ruta)
    i, j = texto.find(MARCA_INICIO), texto.find(MARCA_FIN)
    if i < 0 or j < i or texto.count(MARCA_INICIO) != 1 or texto.count(MARCA_FIN) != 1:
        raise EntradaInvalida(f"{ruta.name}: faltan las marcas {MARCA_INICIO} … {MARCA_FIN}, o están repetidas o al revés")
    cuerpo = "\n".join("#" + x if x.startswith("#") else x for x in markdown.splitlines())   # un nivel por debajo
    ruta.write_text(texto[:i + len(MARCA_INICIO)] + "\n\n" + cuerpo + "\n" + texto[j:], encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    from ..configuracion import DIR_EJECUTOR as DIR_EJ
    ap = argparse.ArgumentParser(prog="python -m bloque_a.herramientas.verificador_ids",
                                 description="Verificador de consistencia de identificadores del Bloque A (T-157)")
    ap.add_argument("--raiz", type=Path, default=DIR_EJ.parent, help="carpeta del bloque (por defecto, la del ejecutor)")
    ap.add_argument("--json", type=Path, help="escribe aquí el informe JSON")
    ap.add_argument("--md", type=Path, help="escribe aquí el informe Markdown")
    ap.add_argument("--auditoria", type=Path, help="sustituye el informe entre las marcas de este documento")
    args = ap.parse_args(argv)
    try:
        informe = verificar(args.raiz)
        texto_json, texto_md = a_json(informe), a_markdown(informe)
        if args.auditoria:
            actualizar_auditoria(args.auditoria, texto_md)
    except EntradaInvalida as e:
        print(f"verificador_ids: FALLO CERRADO: {e}", file=sys.stderr)
        return 2
    except jsonschema.ValidationError as e:
        print(f"verificador_ids: FALLO CERRADO: el informe no cumple su esquema y no se escribe: {e.message}", file=sys.stderr)
        return 2
    if args.json:
        args.json.write_text(texto_json, encoding="utf-8")
    if args.md:
        args.md.write_text(texto_md, encoding="utf-8")
    if not (args.json or args.md or args.auditoria):
        sys.stdout.write(texto_md)
    r = informe["resumen"]
    print(f"verificador_ids: {informe['errores']} errores, {sum(v['AVISO'] for v in r.values())} avisos "
          f"({informe['entradas']['documento_0']['archivo']}, Catálogo V{informe['fichas']['version_nombre']})", file=sys.stderr)
    return 1 if informe["errores"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
