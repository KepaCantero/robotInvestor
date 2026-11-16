"""HT-09: reexporta la implementación de referencia `ht09_validador_g3` (copia literal de 10_Herramientas).

T-165 (PB-47): añade `comprobar_madurez`, la comprobación G3-MET-13 «Madurez declarada» del catálogo de G3 (§6.2 del prompt del
Orquestador técnico, clase B), que la referencia no tiene. Es complementaria del ejecutor: la referencia es corpus congelado y no
se toca. Coteja lo que dice la entrega de la madurez de un método (R22) con la del Catálogo que publica el Motor; la integra
`sintesis.ht09_validar` (F6 y F7) y `redaccion.generar` (el informe técnico). Lo que el diseño no dice: INC-T165-01 `[PROPUESTO]`.
"""
from __future__ import annotations  # noqa: I001  (DIR_REFERENCIA va antes que la referencia)

import html as _html
import re
from collections.abc import Callable, Iterable, Mapping
from typing import Any

from . import DIR_REFERENCIA  # noqa: F401  (añade la carpeta de referencia a sys.path)
import ht09_validador_g3 as _ref
from ht09_validador_g3 import *

modulo = _ref

# ------------------------------------------------------------------ G3-MET-13 (T-165)
ID_MET13 = "G3-MET-13"
NOMBRE_MET13 = "Madurez declarada de los métodos (R22)"
NIVELES = {"DOCUMENTADO": 1, "IMPLEMENTADO": 2, "VALIDADO": 3}   # R22: documentado < implementado < validado

# Forma de una ficha del Catálogo (la de la tabla §4, con los segmentos intermedios empezando por letra): «ML-CLUS-001»,
# «FX-MC10-003». No lo son «CALC-2026-0001», «OPP-2026-0003», «G3-MET-13» ni «DEC-2026-001».
RE_FICHA = re.compile(r"(?<![\w-])([A-Z]+(?:-[A-Z][A-Z0-9]*)+-\d{3})(?!\w|-\w)")
RE_MADUREZ = re.compile(r"(?<!\w)(?:(?P<VALIDADO>validad[oa]s?|validated)|(?P<IMPLEMENTADO>implementad[oa]s?|implemented)"
                        r"|(?P<DOCUMENTADO>documentad[oa]s?|documented))(?!\w)", re.IGNORECASE)
# Una negación justo delante, con hasta tres auxiliares de una lista cerrada: «no validado», «aún no ha sido implementado»
_AUX = (r"aún|todavía|ya|está|están|estaba|estaban|es|son|era|eran|fue|fueron|ha|han|había|habían|haya|hayan|sido|se|sea|sean|"
        r"esté|estén|plenamente|totalmente|formalmente|is|are|was|were|been|has|have|yet|fully|formally")
RE_NEGACION = re.compile(rf"(?<!\w)(?:no|sin|nunca|jamás|ni|not|never)(?:\s+(?:{_AUX})){{0,3}}\s*$", re.IGNORECASE)
# «… validado por el operador», «… validada por el dato de empleo»: la palabra describe lo que hizo una persona o un dato (lista
# cerrada), no la madurez R22 de un método, aunque la frase cite una ficha
RE_AGENTE = re.compile(r"^\s+por\s+(?:(?:el|la|los|las|un|una|unos|unas|dos|tres|varios|varias|otro|otra|otros|otras)\s+)?"
                       r"(?:operador(?:es|as?)?|usuari[oa]s?|broker|asesor(?:es|as?)?|client[ea]s?|inversor(?:es|as?)?|datos?|fuentes?|"
                       r"mercados?|evidencias?)(?!\w)", re.IGNORECASE)
# Declaraciones de que un método no se usa (además de «documentado» y «no implementado»): las del Motor y las del ejecutor
RE_NO_SIRVE = re.compile(r"(?<!\w)(?P<p>rechazad[oa]s|no\s+se\s+sirven|no\s+servid[oa]s)(?!\w)"
                         r"|(?<!\w)(?:rechazad[oa]|rejected|no\s+servid[oa]|no\s+se\s+sirve|not\s+served)(?!\w)"
                         r"|METODO_NO_IMPLEMENTADO|OPERACION_SIN_FICHA", re.IGNORECASE)
# Frases: punto y espacio, «;», «!», «?», saltos de línea y celdas de tabla. No «:» ni «,» («FX-PPA-001, FX-COINT-001: implementados»)
RE_FRASE = re.compile(r"(?<=[.!?])\s+|[;!?|\n\r]")
RE_ETIQUETA = re.compile(r"<[^>]*>")
# Las etiquetas de formato en línea no cortan la frase («ST-DESC-001 está <b>validado</b>»); las demás, sí
RE_EN_LINEA = re.compile(r"</?(?:a|abbr|b|code|em|i|mark|s|small|span|strong|sub|sup|u)(?:\s[^>]*)?/?>", re.IGNORECASE)
CLAVES_METODO = ("metodo", "method_id", "ficha", "operacion", "metodos")   # hermanos de un campo «…madurez…»


def nivel_catalogo(estado: Any) -> int:
    """0 (sin ficha o ilegible), 1 DOCUMENTADO, 2 IMPLEMENTADO, 3 VALIDADO; «Implementado (referencia)» cuenta como IMPLEMENTADO."""
    e = str(estado or "").strip().upper()
    return next((n for k, n in NIVELES.items() if e.startswith(k)), 0)


def texto_html(contenido: str) -> str:
    """El texto de un HTML para G3-MET-13: una etiqueta de bloque separa frases, una de formato en línea no; las entidades se
    resuelven."""
    return _html.unescape(RE_ETIQUETA.sub("\n", RE_EN_LINEA.sub(" ", contenido)))


def textos_de(obj: Any, ruta: str = "") -> list[tuple[str, str]]:
    """Los textos de un JSON con su ruta. Un elemento de lista con `opp_id` lleva el OPP- en la ruta (F6 localiza el bloqueo en esa
    opción). Un diccionario con un campo `…madurez…` se lee junto con sus hermanos de método (`metodo`, `method_id`…) como una
    sola frase, y esos hermanos no se leen sueltos."""
    out: list[tuple[str, str]] = []
    if isinstance(obj, str):
        out.append((ruta, obj))
    elif isinstance(obj, dict):
        claves_mad = [k for k, v in obj.items() if isinstance(k, str) and "madurez" in k.lower() and isinstance(v, str)]
        hermanos = [k for k in CLAVES_METODO if k in obj] if claves_mad else []
        for k in claves_mad:
            partes = [" ".join(map(str, obj[h])) if isinstance(obj[h], list) else str(obj[h]) for h in hermanos]
            out.append((f"{ruta}.{k}" if ruta else str(k), " ".join(partes + [obj[k]])))
        for k, v in obj.items():
            if k in claves_mad or k in hermanos:
                continue
            out.extend(textos_de(v, f"{ruta}.{k}" if ruta else str(k)))
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            marca = v.get("opp_id") if isinstance(v, dict) and isinstance(v.get("opp_id"), str) else i
            out.extend(textos_de(v, f"{ruta}[{marca}]"))
    return out


def _cercana(menciones: list[tuple[int, int, str]], ini: int, fin: int) -> int:
    """La mención de ficha más cercana a [ini, fin); en empate, la que va delante."""
    def distancia(m: tuple[int, int, str]) -> tuple[int, int]:
        return (ini - m[1], 0) if m[1] <= ini else (m[0] - fin, 1)
    return min(range(len(menciones)), key=lambda i: distancia(menciones[i]))


def comprobar_madurez(textos: Iterable[tuple[str, str, str]], madurez: Mapping[str, str], sirve: Callable[[str], bool],
                      fichas: Iterable[str] = ()) -> dict:
    """G3-MET-13. `textos`: (ruta, texto, severidad), con severidad BLOQUEO o ADVERTENCIA. `madurez`: la del Catálogo por ficha
    (`servicio.madurez_catalogo`). `sirve(ficha)`: si el Motor la sirve. `fichas`: las del índice del Catálogo.

    Frase a frase, cada palabra de madurez (validado, implementado, documentado) se atribuye a la ficha más cercana de su frase, o
    a todas si va en plural; sin ficha en la frase no se atribuye a ningún método («validado por el operador»). Falla:
    (A) una madurez afirmada por encima de la del Catálogo; (B) una ficha que el Motor no sirve, nombrada sin declarar en su
    frase que no se usa («documentado», «rechazado», «no implementado», «no servido» o los códigos del Motor).
    Devuelve una comprobación con el formato de HT-09."""
    conocidas = set(madurez) | set(fichas)
    prefijos = {f.split("-", 1)[0] for f in conocidas}
    incidencias: list[dict] = []
    vistas: set[tuple[str, str, str]] = set()
    citadas: set[str] = set()

    def anotar(sev: str, ruta: str, ficha: str, detalle: str) -> None:
        if (ruta, ficha, detalle) not in vistas:
            vistas.add((ruta, ficha, detalle))
            incidencias.append({"severidad": sev, "ruta": ruta, "detalle": detalle})

    for ruta, texto, sev in textos:
        if not isinstance(texto, str) or "-" not in texto:
            continue
        for frase in RE_FRASE.split(texto):
            menciones = [(m.start(1), m.end(1), m.group(1)) for m in RE_FICHA.finditer(frase)
                         if m.group(1) in conocidas or m.group(1).split("-", 1)[0] in prefijos]
            if not menciones:
                continue
            afirma: list[dict[str, str]] = [{} for _ in menciones]   # nivel → palabra
            declara = [False] * len(menciones)
            for m in RE_MADUREZ.finditer(frase):
                nivel = next(k for k in NIVELES if m.group(k))
                palabra = m.group(0)
                destino = range(len(menciones)) if palabra.lower().endswith("s") else [_cercana(menciones, m.start(), m.end())]
                if RE_AGENTE.match(frase[m.end():]):
                    continue
                negada = bool(RE_NEGACION.search(frase[:m.start()]))
                for i in destino:
                    if negada:   # «no implementado» declara que no se usa; «no validado» no dice nada de eso
                        declara[i] = declara[i] or nivel == "IMPLEMENTADO"
                    else:
                        afirma[i].setdefault(nivel, palabra)
                        declara[i] = declara[i] or nivel == "DOCUMENTADO"
            for m in RE_NO_SIRVE.finditer(frase):
                destino = range(len(menciones)) if m.group("p") else [_cercana(menciones, m.start(), m.end())]
                for i in destino:
                    declara[i] = True
            for i, (ini, fin, ficha) in enumerate(menciones):
                citadas.add(ficha)
                estado = madurez.get(ficha)
                cat = nivel_catalogo(estado)
                en_cat = f"«{estado}» en el Catálogo" if estado else "sin ficha en el Catálogo"
                extracto = frase.strip()[:160]
                sobre = [(n, p) for n, p in afirma[i].items() if NIVELES[n] > cat]
                if sobre:
                    _, p = max(sobre, key=lambda x: NIVELES[x[0]])
                    anotar(sev, ruta, ficha, f"G3-MET-13 (R22): «{p}» para {ficha}, {en_cat}"
                                             + (f": «{extracto}»" if sev == "BLOQUEO" else ""))
                elif not sirve(ficha) and not declara[i]:
                    anotar(sev, ruta, ficha, f"G3-MET-13 (R22): se nombra {ficha} y el Motor no la sirve ({en_cat}) sin declararla "
                                             "documentada o rechazada" + (f": «{extracto}»" if sev == "BLOQUEO" else ""))
    sevs = {i["severidad"] for i in incidencias}
    resultado = "BLOQUEO" if "BLOQUEO" in sevs else ("ADVERTENCIA" if sevs else "OK")
    return {"id": ID_MET13, "nombre": NOMBRE_MET13, "resultado": resultado, "incidencias": incidencias,
            "datos": {"fichas_citadas": sorted(citadas)}}
