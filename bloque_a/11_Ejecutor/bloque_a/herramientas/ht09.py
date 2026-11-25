"""HT-09: reexporta la implementación de referencia `ht09_validador_g3` (copia literal de 10_Herramientas).

T-165 (PB-47): añade `comprobar_madurez`, la comprobación G3-MET-13 «Madurez declarada» del catálogo de G3 (§6.2 del prompt del
Orquestador técnico, clase B), que la referencia no tiene. Es complementaria del ejecutor (decisión del §1 del registro de
decisiones del Bloque A): la referencia es corpus congelado y no se toca. Coteja lo que dice la entrega de la madurez de un método
(R22) con la del Catálogo que publica el Motor; la integra `sintesis.ht09_validar` (F6 y F7) y `redaccion.generar` (el informe
técnico). Desde la r03 (QA r02 de T-165) el enfoque es estructural: la madurez de un método solo la escribe el ejecutor, en una
forma canónica junto a cada ficha, y la prosa del modelo no se interpreta (INC-T165-01 `[PROPUESTO]`).
"""
from __future__ import annotations  # noqa: I001  (DIR_REFERENCIA va antes que la referencia)

import html as _html
import json
import re
import unicodedata
from bisect import bisect_left
from collections.abc import Callable, Iterable, Mapping
from typing import Any

from . import DIR_REFERENCIA  # noqa: F401  (añade la carpeta de referencia a sys.path)
import ht09_validador_g3 as _ref
from ht09_validador_g3 import *

modulo = _ref


class HerramientaNoDisponible(RuntimeError):
    """La llamada a la herramienta de referencia no puede ejecutarse."""


def validar_disponible(*args):
    try:
        return validar(*args)
    except PermissionError:
        raise
    except (ImportError, OSError) as exc:
        raise HerramientaNoDisponible("HT-09 no disponible") from exc


# ------------------------------------------------------------------ G3-MET-13 (T-165)
ID_MET13 = "G3-MET-13"
NOMBRE_MET13 = "Madurez declarada de los métodos (R22)"
NIVELES = {"DOCUMENTADO": 1, "IMPLEMENTADO": 2, "VALIDADO": 3}   # R22: documentado < implementado < validado

# --- normalización (H-04, H-11): NFKC, sin caracteres de formato (Cf: guion blando, ancho cero…), guiones tipográficos a «-»,
# espacios raros a « », letras cirílicas y griegas que imitan a las latinas a su latina, y minúsculas
_GUIONES = frozenset("‐‑‒–—―−⁃﹘﹣－")
_HOMOGLIFOS = dict(zip("аеорсухіјѕԁһӏАВЕКМНОРСТХІЈЅοαεικνρτυχΑΒΕΖΗΙΚΜΝΟΡΤΥΧ",
                       "aeopcyxijsdhlABEKMHOPCTXIJSoaeiknptuxABEZHIKMNOPTYX", strict=True))


def normalizar(texto: str) -> str:
    out = []
    for c in unicodedata.normalize("NFKC", texto):
        cat = unicodedata.category(c)
        if c in "\n\r":
            out.append("\n")
        elif cat == "Cf":
            continue
        elif c in _GUIONES or cat == "Pd":
            out.append("-")
        elif cat in ("Zs", "Cc"):
            out.append(" ")
        elif cat in ("Zl", "Zp"):
            out.append("\n")
        else:
            out.append(_HOMOGLIFOS.get(c, c))
    return "".join(out).lower()



# --- r03 (QA r02 de T-165): enfoque estructural, sin interpretar la prosa del modelo (INC-T165-01 `[PROPUESTO]`)
# 1. La madurez de un método solo la escribe el ejecutor, en una forma canónica fija junto a cada mención de una ficha:
#    «ST-DESC-001 [madurez: IMPLEMENTADO]» o, si el Motor no la sirve, «ML-CLUS-001 [madurez: DOCUMENTADO; no la sirve el Motor]».
#    Se comprueba contra el Catálogo: una forma canónica que no coincide bloquea (regla C).
# 2. El vocabulario de madurez no se interpreta: no hay negaciones, sinónimos, personas ni prosa financiera que analizar. La raíz
#    «valid-» (validado, validación, validated, validation…; no «invalid-») en un ámbito que nombra un método bloquea mientras
#    alguna ficha nombrada no esté en VALIDADO (regla A), y la raíz «implement-» si alguna está por debajo de IMPLEMENTADO.
# 3. Una ficha que el Motor no sirve no se nombra sin su forma canónica (regla B). Un campo JSON de madurez solo admite la forma
#    canónica (regla C): lo escribe el ejecutor (`sintesis.canonizar_madurez`).
# El ámbito es el registro de la ruta (una opción OPP-, una candidata) o, fuera de él, el documento (el paquete, el técnico, el
# visual): las palabras, las fichas y los sustantivos de método se miran en todo él, no en la frase ni en el párrafo.
# r04 (QA r03, H-28): la regla que el ejecutor añade a las instrucciones de los agentes que redactan prosa (los prompts del
# corpus piden declarar «documentado, implementado o validado», R22; esa declaración la escribe ahora el ejecutor)
REGLA_R22_REDACCION = ("R22: la madurez de los métodos la escribe el ejecutor junto a cada ficha, desde el Catálogo. No uses la "
                       "raíz «valid-» (validado, validación, validar, validez, válido) en ningún texto: escribe «confirmar», "
                       "«comprobar» o «pendiente de confirmar». Tampoco califiques con otra palabra la madurez o la fiabilidad "
                       "de un método (comprobado, probado, fiable): la escribe el ejecutor.")   # r06 (H-39)
# r06 (H-40): los agentes cuyo texto no llega al paquete ni a los entregables; todos los demás pasan por la reescritura R22 en
# `Bloque._invocar` (lista de exclusión: un agente nuevo queda cubierto por defecto, falla cerrado). AG-12 (curación: clasifica
# las piezas de evidencia), AG-13 (plan del Motor: operaciones y parámetros), AG-14, AG-15, AG-16 y AG-28 (búsqueda y lectura de
# evidencia: sus piezas van a F2 y a los Analistas, que son quienes redactan; el paquete las cita por su identificador),
# AG-18 (dictamen G3: va a HA), AG-19 (auditoría: F9 y HA) y AG-20 (aprendizaje: F6)
AGENTES_SIN_TEXTO_ENTREGADO = frozenset({"AG-12", "AG-13", "AG-14", "AG-15", "AG-16", "AG-18", "AG-19", "AG-20", "AG-28"})
CANON_NO_SIRVE = "no la sirve el Motor"
NOMBRE_CANONICO = {0: "SIN FICHA EN EL CATÁLOGO", 1: "DOCUMENTADO", 2: "IMPLEMENTADO", 3: "VALIDADO"}
SIN_FICHAS = "sin fichas del Catálogo citadas"     # valor canónico de un campo de madurez sin fichas
VENTANA = 80   # caracteres del extracto a cada lado de la palabra (presentación, no un umbral del sistema)
_L = "a-záéíóúüñàèìòùâêîôûç"
RE_VALID = re.compile(rf"(?<![{_L}])(?:re|con|pre)?v[aá]lid[{_L}]*")           # también «válido» (H-30); no «invalidación»
RE_IMPLEMENT = re.compile(rf"(?<![{_L}])(?:re)?implement[{_L}]*")
# Sustantivos que nombran un método sin su ficha, y los de madurez o validación de un método
RE_METODO = re.compile(r"(?<!\w)(?:métodos?|metodos?|metodolog[ií]as?|sistemas?|fichas?|modelos?|cálculos?|calculos?|algoritmos?|estimador(?:es)?|enfoques?"
                       r"|herramientas?|indicador(?:es)?|estrategias?|methods?|models?|algorithms?|estimators?|indicators?"
                       r"|strateg(?:y|ies)|approach(?:es)?|tools?|madurez|maturity|backtests?|fuera\s+de\s+(?:la\s+)?muestra"
                       r"|out[\s-]+of[\s-]+sample)(?!\w)")
RE_CANON = re.compile(r"\s*\[\s*madurez\s*:\s*([^\]\n]{0,120})\]")                 # tras una mención (texto normalizado)
RE_CORCHETE_MADUREZ = re.compile(r"\[\s*madurez\s*:")
RE_CLAVE_MADUREZ = re.compile(r"madurez|maturity")                                  # campos JSON que solo escribe el ejecutor
RE_OPP_TEXTO = re.compile(r"opp-(\d{4})-(\d{4,})", re.IGNORECASE)   # H-09: el extracto no lleva OPP- (F6 lo tomaría por una opción)
RE_AMBITO = re.compile(r"^(.*\[(?!\d+\])[^\]]+\])")                 # hasta el último [registro] que no es un índice

# --- HTML (H-11): las etiquetas de formato en línea se quitan sin espacio («vali</b>dado»); las demás separan; las entidades se
# resuelven; title, alt y aria-label se leen también
RE_ETIQUETA = re.compile(r"<[^>]*>")
RE_EN_LINEA = re.compile(r"</?(?:a|abbr|b|code|em|i|mark|s|small|span|strong|sub|sup|u|font|q|cite|var|kbd)(?:\s[^>]*)?/?>",
                         re.IGNORECASE)
RE_CELDA = re.compile(r"</?(?:td|th)(?:\s[^>]*)?/?>", re.IGNORECASE)
RE_BR = re.compile(r"<br(?:\s[^>]*)?/?>", re.IGNORECASE)
RE_ATRIBUTO = re.compile(r"""\b(?:title|alt|aria-label)\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.IGNORECASE)


def nivel_catalogo(estado: Any) -> int:
    """0 (sin ficha o ilegible), 1 DOCUMENTADO, 2 IMPLEMENTADO, 3 VALIDADO; «Implementado (referencia)» cuenta como IMPLEMENTADO."""
    e = str(estado or "").strip().upper()
    return next((n for k, n in NIVELES.items() if e.startswith(k)), 0)


def texto_html(contenido: str) -> str:
    """El texto de un HTML para G3-MET-13: las etiquetas en línea no cortan, las demás separan; las entidades se resuelven y
    title, alt y aria-label se añaden aparte."""
    atributos = [a or b for a, b in RE_ATRIBUTO.findall(contenido)]
    t = RE_EN_LINEA.sub("", contenido)
    t = RE_CELDA.sub(" | ", t)
    t = RE_BR.sub("\n", t)
    t = RE_ETIQUETA.sub("\n\n", t)
    return _html.unescape("\n\n".join([t, *atributos]))


# ------------------------------------------------------------------ reconocimiento de fichas
_SEP = r"[-_.]"


class Fichas:
    """Las fichas del Catálogo y cómo se reconocen en un texto normalizado: completas con guion, guion bajo o punto, con tres o
    cuatro cifras (también una ficha desconocida con el prefijo de una del Catálogo), completas con espacios y parciales (prefijo
    y familia, o familia y número). Una parcial que corresponde a una sola ficha es esa ficha; a varias, una ficha que no se
    puede reconocer con seguridad («?…»), que la regla B bloquea (falla cerrado)."""

    def __init__(self, conocidas: Iterable[str]) -> None:
        self.conocidas = {str(f).upper() for f in conocidas}
        self.prefijos = {f.split("-", 1)[0] for f in self.conocidas}
        segs = sorted((f.lower().split("-") for f in self.conocidas), key=lambda s: -len("-".join(s)))
        self.re_completa = re.compile(rf"(?<![a-z0-9])([a-z][a-z0-9]*(?:{_SEP}[a-z0-9]+)*{_SEP}\d{{3,4}})(?![a-z0-9]|{_SEP}[a-z0-9])")
        self.re_espacios = re.compile(r"(?<![a-z0-9])(" + "|".join(r"[\s_.-]+".join(map(re.escape, s)) for s in segs)
                                      + r")(?![a-z0-9])")
        parciales: dict[str, set[str]] = {}
        for s in segs:
            f = "-".join(s).upper()
            parciales.setdefault("-".join(s[:-1]), set()).add(f)          # prefijo y familia: «vol-garch»
            if len(s) >= 3:
                parciales.setdefault("-".join(s[-2:]), set()).add(f)      # familia y número: «garch-001»
        self.parciales = parciales
        self.re_parcial = re.compile(r"(?<![a-z0-9_-])(" + "|".join(map(re.escape, sorted(parciales, key=len, reverse=True)))
                                     + r")(?![a-z0-9_]|-[a-z0-9]|\s*-\s*\d)")

    def _resolver(self, crudo: str) -> str | None:
        segs = re.split(_SEP, crudo.upper())
        if len(segs[-1]) == 4:                  # «ST-DESC-0001» es ST-DESC-001; «ST-DESC-1001», una desconocida
            segs[-1] = segs[-1].removeprefix("0")
        for i in range(len(segs) - 1):          # «texto-st-desc-001» (un guion largo pegado) es ST-DESC-001
            cand = "-".join(segs[i:])
            if cand in self.conocidas:
                return cand
        for i in range(len(segs) - 1):          # desconocida con el prefijo de una ficha y segmentos que empiezan por letra
            if segs[i] in self.prefijos and all(x[:1].isalpha() for x in segs[i + 1:-1]) and len(segs) - i >= 3:
                return "-".join(segs[i:])
        return None

    def buscar(self, t: str) -> list[tuple[int, int, str]]:
        """Las menciones (inicio, fin, ficha) de `t`, ordenadas. Cada pasada solo toma lo que no tomó una anterior; el solape se
        mira con `bisect` sobre los tramos ya tomados (H-22: lineal en el número de fichas, salvo el logaritmo)."""
        out: list[tuple[int, int, str]] = []
        for m in self.re_completa.finditer(t):
            f = self._resolver(m.group(1))
            if f:
                out.append((m.start(1), m.end(1), f))
        pasadas: list[tuple[re.Pattern[str], Callable[[str], str]]] = [
            (self.re_espacios, lambda g: re.sub(r"[\s_.-]+", "-", g).upper()),
            (self.re_parcial, lambda g: next(iter(self.parciales[g])) if len(self.parciales[g]) == 1 else f"?{g.upper()}")]
        for patron, nombre in pasadas:
            tomados = sorted(out)
            inicios = [a for a, _, _ in tomados]
            for m in patron.finditer(t):
                a, b = m.start(1), m.end(1)
                k = bisect_left(inicios, b)
                if k > 0 and tomados[k - 1][1] > a:     # solapa con el tramo tomado anterior más cercano
                    continue
                out.append((a, b, nombre(m.group(1))))
        return sorted(out)


_CACHE_FICHAS: dict[frozenset[str], Fichas] = {}


def fichas_de(conocidas: Iterable[str]) -> Fichas:
    """Un `Fichas` por conjunto de fichas (se compila una vez)."""
    clave = frozenset(str(f).upper() for f in conocidas)
    if clave not in _CACHE_FICHAS:
        _CACHE_FICHAS[clave] = Fichas(clave)
    return _CACHE_FICHAS[clave]


# ------------------------------------------------------------------ la forma canónica (la escribe el ejecutor)
def madurez_canonica(ficha: str, madurez: Mapping[str, str], sirve: Callable[[str], bool]) -> str:
    """El contenido canónico de la madurez de `ficha`: «madurez: IMPLEMENTADO» o «madurez: DOCUMENTADO; no la sirve el Motor»."""
    s = f"madurez: {NOMBRE_CANONICO[nivel_catalogo(madurez.get(ficha))]}"
    return s if sirve(ficha) else f"{s}; {CANON_NO_SIRVE}"


def _re_exactas(conocidas: Iterable[str]) -> re.Pattern[str]:
    fichas = sorted({str(f).upper() for f in conocidas}, key=len, reverse=True)
    return re.compile(r"(?<![A-Za-z0-9_-])(" + "|".join(map(re.escape, fichas)) + r")(?![A-Za-z0-9_]|-[A-Za-z0-9])(?!\s*\[madurez:)")


_CACHE_EXACTAS: dict[frozenset[str], re.Pattern[str]] = {}


def anotar_madurez(texto: str, madurez: Mapping[str, str], sirve: Callable[[str], bool], conocidas: Iterable[str]) -> str:
    """Añade la forma canónica tras cada mención de una ficha del Catálogo escrita con su grafía («ST-DESC-001» →
    «ST-DESC-001 [madurez: IMPLEMENTADO]»). Una mención que ya la lleva no se toca. Las grafías raras no se anotan (G3-MET-13 las
    reconoce igual: una ficha no servida bloquea; la madurez solo la dice esta forma)."""
    clave = frozenset(str(f).upper() for f in conocidas) | frozenset(madurez)
    if not clave:
        return texto
    if clave not in _CACHE_EXACTAS:
        _CACHE_EXACTAS[clave] = _re_exactas(clave)
    return _CACHE_EXACTAS[clave].sub(lambda m: f"{m.group(1)} [{madurez_canonica(m.group(1), madurez, sirve)}]", texto)


def fichas_citadas(texto: str, conocidas: Iterable[str]) -> list[str]:
    """Las fichas del Catálogo escritas con su grafía en `texto`, sin repetir y ordenadas."""
    clave = frozenset(str(f).upper() for f in conocidas)
    if not clave:
        return []
    if clave not in _CACHE_EXACTAS:
        _CACHE_EXACTAS[clave] = _re_exactas(clave)
    patron = re.compile(_CACHE_EXACTAS[clave].pattern.removesuffix(r"(?!\s*\[madurez:)"))
    return sorted(set(patron.findall(texto)))


def resumen_madurez(fichas: Iterable[str], madurez: Mapping[str, str], sirve: Callable[[str], bool]) -> str:
    """La declaración R22 de un entregable en forma canónica: cada ficha con su madurez del Catálogo, o «sin fichas…»."""
    fs = sorted(set(fichas))
    return "; ".join(f"{f} [{madurez_canonica(f, madurez, sirve)}]" for f in fs) if fs else SIN_FICHAS


def tiene_raiz_valid(obj: Any) -> bool:
    """Si algún texto de `obj` (cadenas de un JSON, también las claves) lleva la raíz «valid-» tras normalizar: lo que lleva a
    reescribir la redacción de un agente fuera de una opción (r04, H-28)."""
    if isinstance(obj, str):
        return bool(RE_VALID.search(normalizar(obj)))
    if isinstance(obj, dict):
        return any(tiene_raiz_valid(str(k)) or tiene_raiz_valid(v) for k, v in obj.items())
    if isinstance(obj, (list, tuple)):
        return any(tiene_raiz_valid(v) for v in obj)
    return False


def frases_con_raiz(obj: Any, maximo: int, ruta: str = "") -> list[tuple[str, str]]:
    """r05 (H-37): como `tiene_raiz_valid`, pero devuelve hasta `maximo` textos con la raíz, con su ruta (recortados a 200
    caracteres): lo que la reescritura dice al agente que corrija."""
    out: list[tuple[str, str]] = []

    def ir(x: Any, r: str) -> None:
        if len(out) >= maximo:
            return
        if isinstance(x, str):
            if RE_VALID.search(normalizar(x)):
                out.append((r or ".", x[:200]))
        elif isinstance(x, dict):
            for k, v in x.items():
                if tiene_raiz_valid(str(k)) and len(out) < maximo:
                    out.append((f"{r}.{k}" if r else str(k), str(k)[:200]))
                ir(v, f"{r}.{k}" if r else str(k))
        elif isinstance(x, (list, tuple)):
            for i, v in enumerate(x):
                ir(v, f"{r}[{i}]")
    ir(obj, ruta)
    return out


# ------------------------------------------------------------------ textos de un JSON
def textos_de(obj: Any, ruta: str = "", fichas: Iterable[str] | Fichas | None = None) -> list[tuple[str, str]]:
    """Las hojas de un JSON con su ruta, como «clave: valor» (la clave cuenta: «validado: sí», «is_validated: 1»). Un elemento
    de lista con `opp_id` lleva el OPP- en la ruta (F6 localiza el bloqueo en esa opción; es también el ámbito de la lectura).
    Una hoja bajo una clave de madurez (`estado_madurez_metodos`…) solo admite la forma canónica, que escribe el ejecutor: si el
    valor no lo es, se lee con una marca que la regla C bloquea. `fichas` se admite por compatibilidad (no hace falta)."""
    del fichas
    out: list[tuple[str, str]] = []
    _hojas(obj, ruta, (), False, out)
    return out


def _es_canonico(v: str) -> bool:
    """Si `v` es solo formas canónicas («FICHA [madurez: …]» separadas por «;») o el valor sin fichas. Que cada una coincida con
    el Catálogo lo comprueba la regla C."""
    t = normalizar(v).strip()
    if t == normalizar(SIN_FICHAS):
        return True
    resto = re.sub(r"[a-z0-9][a-z0-9_.-]*\s*\[\s*madurez\s*:[^\]\n]*\]", "", t)
    return bool(t) and resto != t and not re.sub(r"[\s;]", "", resto)


def _hojas(obj: Any, ruta: str, claves: tuple[str, ...], bajo_madurez: bool, out: list[tuple[str, str]]) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            k = str(k)
            _hojas(v, f"{ruta}.{k}" if ruta else k, (*claves, k), bajo_madurez or bool(RE_CLAVE_MADUREZ.search(k.lower())), out)
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            marca = v.get("opp_id") if isinstance(v, dict) and isinstance(v.get("opp_id"), str) else i
            _hojas(v, f"{ruta}[{marca}]", claves, bajo_madurez, out)
    elif obj is not None:
        valor = obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False)
        # las claves del camino (una ficha como clave de un objeto, «validado», «nivel_madurez»…) se leen con el valor
        texto = f"{' · '.join(k.replace('_', ' ') for k in claves)}: {valor}" if claves else valor
        if bajo_madurez and not (isinstance(obj, str) and _es_canonico(obj)):
            texto += " [madurez: valor que no escribe el ejecutor]"
        out.append((ruta or ".", texto))


# ------------------------------------------------------------------ lectura
def ambito_de(ruta: str) -> str:
    """El ámbito de una ruta: hasta su último registro («…opciones[OPP-2026-0001]», «…no_entregada[SPY]»); fuera de un
    registro, el documento (lo que va antes del primer «.», «[» o «,»: «paquete», «informe_tecnico», «informe_visual»)."""
    m = RE_AMBITO.match(ruta)
    return m.group(1) if m else re.split(r"[.\[,]", ruta, maxsplit=1)[0]


def _extracto(t: str, a: int, b: int) -> str:
    return RE_OPP_TEXTO.sub(r"opp \1/\2", " ".join(t[max(0, a - VENTANA):b + VENTANA].split())[:2 * VENTANA])


class _Lectura:
    """Lo que G3-MET-13 necesita de un texto normalizado: las menciones de ficha (con si llevan su forma canónica correcta), las
    palabras «valid-» e «implement-» y los sustantivos de método fuera de las formas canónicas correctas."""

    def __init__(self, ruta: str, crudo: str, sev: str, fx: Fichas, madurez: Mapping[str, str],
                 sirve: Callable[[str], bool]) -> None:
        self.ruta, self.sev = ruta, sev
        t = normalizar(crudo)
        self.t = t
        self.menciones: list[tuple[int, int, str, bool]] = []     # (inicio, fin, ficha, con su forma canónica correcta)
        self.canon_mal: list[tuple[int, int, str, str]] = []      # (inicio, fin, ficha, lo que dice)
        blanco: list[tuple[int, int]] = []
        for a, b, f in fx.buscar(t):
            m = RE_CANON.match(t, b)
            if not m:
                self.menciones.append((a, b, f, False))
                continue
            dice = " ".join(m.group(1).split())
            debe = " ".join(normalizar(madurez_canonica(f, madurez, sirve)).split(":", 1)[1].split())
            if not f.startswith("?") and dice == debe:
                self.menciones.append((a, b, f, True))
                blanco.append((m.start(), m.end()))
            else:
                self.menciones.append((a, b, f, False))
                self.canon_mal.append((a, m.end(), f, dice))
        tb = list(t)
        for a, b in blanco:
            tb[a:b] = " " * (b - a)
        limpio = "".join(tb)
        ocupado = {(a, b) for a, b, _, _ in self.menciones}
        en_canon = [m.start() for m in RE_CORCHETE_MADUREZ.finditer(limpio)
                    if not any(a <= m.start() < b for a, b, _, _ in self.canon_mal)]
        self.corchetes_sueltos = en_canon                              # «[madurez: …]» que no sigue a una ficha
        self.valid = [(m.start(), m.end(), m.group(0)) for m in RE_VALID.finditer(limpio)
                      if not any(a <= m.start() < b for a, b in ocupado)]
        self.implement = [(m.start(), m.end(), m.group(0)) for m in RE_IMPLEMENT.finditer(limpio)]
        self.metodo = bool(RE_METODO.search(limpio))

    def ficha_cercana(self, pos: int, cumple: Callable[[str], bool]) -> str | None:
        cands = [(min(abs(pos - a), abs(pos - b)), f) for a, b, f, _ in self.menciones if cumple(f)]
        return min(cands)[1] if cands else None


def comprobar_madurez(textos: Iterable[tuple[str, str, str]], madurez: Mapping[str, str], sirve: Callable[[str], bool],
                      fichas: Iterable[str] | Fichas = ()) -> dict:
    """G3-MET-13. `textos`: (ruta, texto, severidad), con severidad BLOQUEO o ADVERTENCIA. `madurez`: la del Catálogo por ficha
    (`servicio.madurez_catalogo`). `sirve(ficha)`: si el Motor la sirve. `fichas`: las del índice del Catálogo.

    Reglas (r03, INC-T165-01): (A) la raíz «valid-» en un ámbito que nombra un método (una ficha que no está en VALIDADO o un
    sustantivo de método), o la raíz «implement-» en uno que nombra una ficha por debajo de IMPLEMENTADO; (B) una ficha que el
    Motor no sirve nombrada sin su forma canónica; (C) una forma canónica que no coincide con el Catálogo, o un «[madurez: …]»
    que no sigue a una ficha (también el campo de madurez de un JSON que no escribe el ejecutor). Las formas canónicas correctas
    no se leen. Devuelve una comprobación con el formato de HT-09."""
    fx = fichas if isinstance(fichas, Fichas) else fichas_de(set(madurez) | set(fichas))
    incidencias: list[dict] = []
    vistas: set[tuple[str, str, str]] = set()
    citadas: set[str] = set()

    def anotar(sev: str, ruta: str, clave: str, regla: str, detalle: str, extracto: str) -> None:
        if (ruta, clave, regla) not in vistas:
            vistas.add((ruta, clave, regla))
            incidencias.append({"severidad": sev, "ruta": ruta, "_regla": regla,
                                "detalle": detalle + (f": «{extracto}»" if sev == "BLOQUEO" else "")})

    def en_cat(f: str) -> str:
        estado = madurez.get(f)
        return (f"«{estado}» en el Catálogo" if estado else
                ("una ficha que no se puede reconocer con seguridad" if f.startswith("?") else "sin ficha en el Catálogo"))

    lecturas: list[_Lectura] = []
    por_ambito: dict[str, list[_Lectura]] = {}
    for ruta, crudo, sev in textos:
        if not isinstance(crudo, str):
            continue
        lec = _Lectura(ruta, crudo, sev, fx, madurez, sirve)
        lecturas.append(lec)
        por_ambito.setdefault(ambito_de(ruta), []).append(lec)
    for lec in lecturas:   # reglas B y C, mención a mención
        for a, b, f, canonica in lec.menciones:
            citadas.add(f)
            if not canonica and not (not f.startswith("?") and sirve(f)):
                anotar(lec.sev, lec.ruta, f, "B", f"G3-MET-13 (R22): se nombra {f} y el Motor no la sirve ({en_cat(f)}); solo "
                       f"se nombra con su forma canónica «{f} [{madurez_canonica(f, madurez, sirve)}]», que escribe el ejecutor",
                       _extracto(lec.t, a, b))
        for a, b, f, dice in lec.canon_mal:
            anotar(lec.sev, lec.ruta, f, "C", f"G3-MET-13 (R22): «[madurez: {dice}]» para {f}, {en_cat(f)}: la forma canónica es "
                   f"«[{madurez_canonica(f, madurez, sirve)}]»", _extracto(lec.t, a, b))
        for pos in lec.corchetes_sueltos:
            anotar(lec.sev, lec.ruta, f"[{pos}]", "C", "G3-MET-13 (R22): una madurez que no escribe el ejecutor (la forma canónica "
                   "va detrás de su ficha y la pone el ejecutor desde el Catálogo)", _extracto(lec.t, pos, pos))
    for grupo in por_ambito.values():   # regla A, en todo el ámbito
        bajo_validado = [f for x in grupo for _, _, f, _ in x.menciones if nivel_catalogo(madurez.get(f)) < NIVELES["VALIDADO"]]
        bajo_impl = [f for x in grupo for _, _, f, _ in x.menciones if nivel_catalogo(madurez.get(f)) < NIVELES["IMPLEMENTADO"]]
        metodo = any(x.metodo for x in grupo)
        for lec in grupo:
            for nivel, palabras, debajo in (("VALIDADO", lec.valid, bajo_validado), ("IMPLEMENTADO", lec.implement, bajo_impl)):
                if not palabras or not (debajo or (nivel == "VALIDADO" and metodo)):
                    continue
                a, b, palabra = palabras[0]
                cerca = lec.ficha_cercana(a, set(debajo).__contains__) or (debajo[0] if debajo else None)
                quien = f"{cerca}, {en_cat(cerca)}" if cerca else "un método nombrado sin su ficha (ninguna ficha está en VALIDADO)"
                anotar(lec.sev, lec.ruta, cerca or "?", "A", f"G3-MET-13 (R22): «{palabra}» para {quien}; la madurez de un método "
                       "solo la escribe el ejecutor, desde el Catálogo", _extracto(lec.t, a, b))
    incidencias.sort(key=lambda i: "ACB".index(i.pop("_regla")))   # primero la madurez afirmada; el orden de cada regla se mantiene
    sevs = {i["severidad"] for i in incidencias}
    resultado = "BLOQUEO" if "BLOQUEO" in sevs else ("ADVERTENCIA" if sevs else "OK")
    return {"id": ID_MET13, "nombre": NOMBRE_MET13, "resultado": resultado, "incidencias": incidencias,
            "datos": {"fichas_citadas": sorted(citadas)}}
