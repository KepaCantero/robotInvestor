#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HT-07 · Medidor de legibilidad (implementación de referencia).

Bloque A · Robot Investor · Versión óptima V5.0 · 02/11/2026 · Subordinado al
Documento 0 óptima V5.0 (secciones 4.4 y 14.2).

Calcula, sobre texto plano o HTML (solo texto visible):
  * índice de Fernández-Huerta en su versión corregida (Law, 2011): L = 206,84 − 0,60·P − 1,02·F, con
    P = sílabas por cada 100 palabras y F = palabras por frase (la fórmula original, con F = frases por
    100 palabras, se informa aparte porque penaliza las frases cortas);

  * longitud media de frase (palabras) y % de frases de más de 20 palabras;
  * jerga detectada a partir de una lista configurable (lista inicial de
    términos financieros incluida), indicando si la primera aparición va
    explicada entre paréntesis (regla de lenguaje de 14.2).

El silabeo es por reglas del español: dígrafos (ch, ll, rr), «qu»/«gu» con u
muda, diptongos y triptongos, hiatos (dos vocales fuertes o vocal débil
tildada junto a fuerte), «y» vocálica final, y reparto de grupos consonánticos
con los grupos inseparables (pr, br, tr, dr, cr, gr, fr, kr, pl, bl, cl, gl,
fl, kl). «tl» se separa (norma peninsular: at-lán-ti-co).

Solo biblioteca estándar. Estado de madurez (R22): implementada (referencia),
pruebas unitarias superadas; pendiente de integración.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import unicodedata
from html.parser import HTMLParser
from typing import Dict, Iterable, List, Optional, Sequence

VERSION = "4.0"
UMBRAL_FH_POR_DEFECTO = 70.0
MAX_PALABRAS_FRASE = 20
SILABAS_POR_NUMERO = 2  # estimación declarada para tokens numéricos

# ---------------------------------------------------------------------------
# Lista inicial de jerga financiera (configurable con --jerga ARCHIVO).
# ---------------------------------------------------------------------------
JERGA_FINANCIERA_POR_DEFECTO: List[str] = [
    "volatilidad", "volatilidad implícita", "liquidez", "diversificación",
    "rentabilidad", "dividendo", "bono", "renta fija", "renta variable",
    "cupón", "duración modificada", "convexidad", "diferencial", "spread",
    "prima de riesgo", "rendimiento a vencimiento", "TIR", "PER", "BPA",
    "EBITDA", "flujo de caja", "apalancamiento", "apalancado", "derivado",
    "contrato de futuros", "opción call", "opción put", "ETF", "ETC",
    "fondo indexado", "benchmark", "índice de referencia", "capitalización",
    "small caps", "large caps", "momentum", "carry", "carry trade", "contango",
    "backwardation", "cobertura de riesgos", "hedge", "alfa", "beta",
    "ratio de Sharpe", "drawdown", "valor liquidativo", "NAV", "REIT",
    "SOCIMI", "cap rate", "tasa de capitalización", "FFO", "stablecoin",
    "halving", "blockchain", "cadena de bloques", "DeFi", "staking",
    "capital riesgo", "private equity", "deuda privada", "hedge fund",
    "high yield", "grado de inversión", "investment grade", "curva de tipos",
    "pendiente de la curva", "breakeven", "inflación implícita",
    "quantitative easing", "flexibilización cuantitativa", "tapering",
    "política monetaria", "tipo de interés real", "paridad de poder adquisitivo",
    "OPV", "IPO", "dilución", "recompra de acciones", "buyback", "múltiplo",
    "CAPE", "descuento sobre NAV", "rolldown", "subyacente", "posición corta",
    "venta en corto", "posición larga", "alcista", "bajista", "rally",
    "sell-off", "correlación", "riesgo de cola", "VaR", "valor en riesgo",
    "desviación típica", "puntos básicos", "TAE", "crowding", "riesgo de crédito",
]

# ---------------------------------------------------------------------------
# Extracción de texto visible de HTML
# ---------------------------------------------------------------------------
_ETIQUETAS_INVISIBLES = {"script", "style", "noscript", "template", "head", "svg", "math", "iframe", "object"}
_ETIQUETAS_BLOQUE = {
    "p", "div", "section", "article", "header", "footer", "main", "aside", "nav",
    "h1", "h2", "h3", "h4", "h5", "h6", "li", "ul", "ol", "dl", "dt", "dd",
    "table", "tr", "td", "th", "thead", "tbody", "caption", "figure", "figcaption",
    "blockquote", "pre", "br", "hr", "form", "fieldset", "legend", "details", "summary",
    "title", "button", "label",
}


class _ExtractorTexto(HTMLParser):
    _VACIAS = {"br", "hr", "img", "meta", "link", "input", "source", "wbr", "area", "base", "col", "embed", "param", "track"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.partes: List[str] = []
        self._oculto_tag: Optional[str] = None  # etiqueta que abrió la región oculta
        self._oculto_prof = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in self._VACIAS:
            if tag in ("br", "hr") and self._oculto_tag is None:
                self.partes.append("\n\n")
            return
        if self._oculto_tag is not None:
            if tag == self._oculto_tag:
                self._oculto_prof += 1
            return
        a = {k.lower(): (v or "") for k, v in attrs}
        oculto = (
            tag in _ETIQUETAS_INVISIBLES
            or "hidden" in a
            or a.get("aria-hidden", "").lower() == "true"
            or re.search(r"display\s*:\s*none|visibility\s*:\s*hidden", a.get("style", ""), re.I)
        )
        if oculto:
            self._oculto_tag, self._oculto_prof = tag, 1
            return
        if tag in _ETIQUETAS_BLOQUE:
            self.partes.append("\n\n")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if self._oculto_tag is not None:
            if tag == self._oculto_tag:
                self._oculto_prof -= 1
                if self._oculto_prof == 0:
                    self._oculto_tag = None
            return
        if tag in _ETIQUETAS_BLOQUE:
            self.partes.append("\n\n")

    def handle_startendtag(self, tag, attrs):
        if tag.lower() in ("br", "hr") and self._oculto_tag is None:
            self.partes.append("\n\n")

    def handle_data(self, data):
        if self._oculto_tag is None:
            self.partes.append(data)


def extraer_texto_html(contenido_html: str) -> str:
    """Devuelve el texto visible de un documento HTML (bloques separados por línea en blanco)."""
    p = _ExtractorTexto()
    p.feed(contenido_html)
    p.close()
    texto = "".join(p.partes)
    texto = html.unescape(texto)
    texto = re.sub(r"[ \t\r\f\v ]+", " ", texto)
    texto = re.sub(r" *\n *", "\n", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto.strip()


def parece_html(texto: str) -> bool:
    return bool(re.search(r"<\s*(html|body|p|div|h[1-6]|span|section|article)\b", texto[:5000], re.I))


# ---------------------------------------------------------------------------
# Silabeo español por reglas
# ---------------------------------------------------------------------------
_FUERTES = set("aeoáéó")
_DEBILES_TILDADAS = set("íú")
_DEBILES = set("iuü")
_VOCALES = _FUERTES | _DEBILES_TILDADAS | _DEBILES | {"à", "è", "ò", "ì", "ù"}
_INSEPARABLES = {"pr", "br", "tr", "dr", "cr", "kr", "gr", "fr", "pl", "bl", "cl", "kl", "gl", "fl"}
_LETRA = "a-zA-ZáéíóúüñÁÉÍÓÚÜÑàèìòùÀÈÌÒÙçÇ"


def _unidades(palabra: str) -> List[tuple]:
    """Divide la palabra en unidades (texto, tipo) con tipo 'V' o 'C'."""
    w = palabra.lower()
    u: List[tuple] = []
    i = 0
    n = len(w)
    while i < n:
        c = w[i]
        dos = w[i:i + 2]
        sig = w[i + 2] if i + 2 < n else ""
        if dos in ("ch", "ll", "rr"):
            u.append((dos, "C"))
            i += 2
            continue
        if dos in ("qu", "gu") and sig in ("e", "i", "é", "í"):
            u.append((dos, "C"))  # u muda
            i += 2
            continue
        if c == "y":
            siguiente = w[i + 1] if i + 1 < n else ""
            if siguiente and siguiente in _VOCALES:
                u.append((c, "C"))
            else:
                u.append((c, "V"))  # y vocálica (hoy, rey, muy, «y»)
            i += 1
            continue
        if c in _VOCALES:
            u.append((c, "V"))
        else:
            u.append((c, "C"))
        i += 1
    return u


def _es_fuerte(v: str) -> bool:
    return v in _FUERTES or v in "àèò"


def _separa_vocales(p: str, c: str) -> bool:
    """True si entre las vocales contiguas p y c hay frontera silábica (hiato)."""
    pf, cf = _es_fuerte(p), _es_fuerte(c)
    pt, ct = p in _DEBILES_TILDADAS, c in _DEBILES_TILDADAS
    if pf and cf:
        return True
    if (pt and cf) or (ct and pf):
        return True
    if pt and ct:
        return True
    if p == c and p in "iu":  # chiita, duunviro
        return True
    return False


def _nucleos(vocales: List[str]) -> List[List[str]]:
    grupos: List[List[str]] = [[vocales[0]]]
    for v in vocales[1:]:
        prev = grupos[-1][-1]
        y_prev = prev == "y"
        if not y_prev and _separa_vocales(prev, v):
            grupos.append([v])
            continue
        # un núcleo no puede contener dos vocales fuertes (o tildadas)
        fuertes = sum(1 for x in grupos[-1] if _es_fuerte(x) or x in _DEBILES_TILDADAS)
        if fuertes and (_es_fuerte(v) or v in _DEBILES_TILDADAS):
            grupos.append([v])
            continue
        grupos[-1].append(v)
    return grupos


def silabear(palabra: str) -> List[str]:
    """Separa una palabra española en sílabas (ortográficas, aproximación por reglas)."""
    palabra = re.sub(rf"[^{_LETRA}]", "", palabra)
    if not palabra:
        return []
    unidades = _unidades(palabra)
    # Construir secuencia de segmentos: consonantes sueltas y núcleos vocálicos
    segmentos: List[tuple] = []  # ('C', texto) o ('N', [unidades vocálicas])
    i = 0
    while i < len(unidades):
        t, tipo = unidades[i]
        if tipo == "V":
            j = i
            vs = []
            while j < len(unidades) and unidades[j][1] == "V":
                vs.append(unidades[j][0])
                j += 1
            for g in _nucleos(vs):
                segmentos.append(("N", "".join(g)))
            i = j
        else:
            segmentos.append(("C", t))
            i += 1
    nucleos_idx = [k for k, s in enumerate(segmentos) if s[0] == "N"]
    if not nucleos_idx:
        return [palabra]
    # Repartir consonantes entre núcleos
    silabas: List[str] = []
    inicio_actual = 0
    for n_i, k in enumerate(nucleos_idx):
        if n_i + 1 < len(nucleos_idx):
            k2 = nucleos_idx[n_i + 1]
            consonantes = [segmentos[x][1] for x in range(k + 1, k2)]
            nc = len(consonantes)
            if nc == 0:
                corte = k + 1
            elif nc == 1:
                corte = k + 1
            elif nc == 2:
                par = consonantes[0] + consonantes[1]
                corte = k + 1 if par in _INSEPARABLES else k + 2
            elif nc == 3:
                par = consonantes[1] + consonantes[2]
                corte = k + 2 if par in _INSEPARABLES else k + 3
            else:
                corte = k2 - 2
            silabas.append("".join(s[1] for s in segmentos[inicio_actual:corte]))
            inicio_actual = corte
        else:
            silabas.append("".join(s[1] for s in segmentos[inicio_actual:]))
    # Restaurar mayúsculas aproximadas no es necesario para el recuento.
    return silabas


def contar_silabas(palabra: str) -> int:
    if re.fullmatch(r"\d+(?:[.,]\d+)*", palabra):
        return SILABAS_POR_NUMERO
    total = 0
    for parte in re.split(r"[-'’]", palabra):
        s = silabear(parte)
        total += len(s) if s else 0
    return max(total, 1) if re.search(rf"[{_LETRA}]", palabra) else total


# ---------------------------------------------------------------------------
# Frases y palabras
# ---------------------------------------------------------------------------
_ABREVIATURAS = {
    "p. ej.", "ej.", "etc.", "sr.", "sra.", "srta.", "dr.", "dra.", "núm.", "n.º", "art.",
    "pág.", "págs.", "vol.", "cap.", "aprox.", "ee. uu.", "uu.", "ee.", "s. a.", "s.a.",
    "vs.", "fig.", "cf.", "máx.", "mín.", "ed.", "eds.", "tel.", "av.", "avda.", "dpto.",
}
_RE_PALABRA = re.compile(rf"[{_LETRA}]+(?:[-'’][{_LETRA}]+)*|\d+(?:[.,]\d+)*")


def _proteger_abreviaturas(texto: str) -> str:
    def repl(m):
        return m.group(0).replace(".", "․")  # punto de una sola línea
    for ab in sorted(_ABREVIATURAS, key=len, reverse=True):
        patron = r"(?<![\w])" + re.escape(ab).replace(r"\ ", r"\s*")
        texto = re.sub(patron, repl, texto, flags=re.I)
    return texto


def dividir_frases(texto: str) -> List[str]:
    """Divide en frases: signos . ! ? … seguidos de espacio, líneas en blanco y viñetas/títulos."""
    texto = _proteger_abreviaturas(texto)
    bloques = re.split(r"\n\s*\n|\n(?=\s*(?:[-*•]|\d+[.)]|#{1,6})\s)", texto)
    frases: List[str] = []
    for b in bloques:
        b = b.strip()
        if not b:
            continue
        b = re.sub(r"^\s*(?:[-*•]|\d+[.)]|#{1,6})\s+", "", b)
        b = re.sub(r"\s*\n\s*", " ", b)
        for f in re.split(r"(?<=[.!?…])[\"»”')\]]*\s+", b):
            f = f.strip().replace("․", ".")
            if _RE_PALABRA.search(f):
                frases.append(f)
    return frases


def palabras(texto: str) -> List[str]:
    return _RE_PALABRA.findall(texto.replace("․", "."))


# ---------------------------------------------------------------------------
# Jerga
# ---------------------------------------------------------------------------
def _sin_tildes(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


def cargar_jerga(ruta: Optional[str]) -> List[str]:
    if not ruta:
        return list(JERGA_FINANCIERA_POR_DEFECTO)
    with open(ruta, encoding="utf-8") as fh:
        if ruta.lower().endswith(".json"):
            datos = json.load(fh)
            return [str(t) for t in (datos.get("terminos", []) if isinstance(datos, dict) else datos)]
        return [ln.strip() for ln in fh if ln.strip() and not ln.lstrip().startswith("#")]


def detectar_jerga(texto: str, terminos: Iterable[str]) -> List[Dict]:
    """Detecta términos (sin distinguir mayúsculas ni tildes; coincidencia más larga primero)."""
    base = _sin_tildes(texto)
    if len(base) != len(texto):  # salvaguarda: normalización alteró longitudes
        base = texto.lower()
    ocupado = [False] * len(base)
    resultados: Dict[str, Dict] = {}
    for termino in sorted({t for t in terminos if t.strip()}, key=lambda t: (-len(t), t)):
        tn = _sin_tildes(termino)
        patron = re.compile(r"(?<![\w])" + re.escape(tn).replace(r"\ ", r"\s+") + r"(?![\w])")
        for m in patron.finditer(base):
            if any(ocupado[m.start():m.end()]):
                continue
            for k in range(m.start(), m.end()):
                ocupado[k] = True
            r = resultados.setdefault(termino, {"termino": termino, "apariciones": 0, "primera_posicion": m.start(),
                                                "explicado_primera_vez": None})
            r["apariciones"] += 1
            if m.start() <= r["primera_posicion"]:
                r["primera_posicion"] = m.start()
                resto = texto[m.end():m.end() + 40]
                r["explicado_primera_vez"] = bool(re.match(r"\s*(\(|,\s*es decir|,\s*o sea|:\s)", resto, re.I))
    return sorted(resultados.values(), key=lambda r: r["primera_posicion"])


# ---------------------------------------------------------------------------
# Índice
# ---------------------------------------------------------------------------
def interpretar_fh(valor: float) -> str:
    if valor >= 90:
        return "muy fácil"
    if valor >= 80:
        return "fácil"
    if valor >= 70:
        return "algo fácil"
    if valor >= 60:
        return "normal"
    if valor >= 50:
        return "algo difícil"
    if valor >= 30:
        return "difícil"
    return "muy difícil"


def analizar(texto: str, es_html: Optional[bool] = None, terminos_jerga: Optional[Sequence[str]] = None,
             umbral_fh: float = UMBRAL_FH_POR_DEFECTO, max_palabras_frase: int = MAX_PALABRAS_FRASE) -> Dict:
    if es_html is None:
        es_html = parece_html(texto)
    plano = extraer_texto_html(texto) if es_html else texto
    frases = dividir_frases(plano)
    lista_palabras = [p for f in frases for p in palabras(f)]
    n_pal = len(lista_palabras)
    n_sil = sum(contar_silabas(p) for p in lista_palabras)
    n_fr = len(frases)
    longitudes = [len(palabras(f)) for f in frases]
    largas = [{"frase": f, "palabras": n} for f, n in zip(frases, longitudes) if n > max_palabras_frase]
    fh_original = None
    if n_pal == 0:
        fh = None
    else:
        P = 100.0 * n_sil / n_pal
        # Versión corregida (Law, 2011), exigida por el Documento 0 (14.2): F = palabras por frase.
        F = n_pal / n_fr if n_fr else 0.0
        fh = round(206.84 - 0.60 * P - 1.02 * F, 2)
        # Fórmula original publicada (F = frases por 100 palabras), solo informativa: penaliza las frases cortas.
        fh_original = round(206.84 - 0.60 * P - 1.02 * (100.0 * n_fr / n_pal), 2)
    jerga = detectar_jerga(plano, terminos_jerga if terminos_jerga is not None else JERGA_FINANCIERA_POR_DEFECTO)
    sin_explicar = [j["termino"] for j in jerga if not j["explicado_primera_vez"]]
    pct_largas = round(100.0 * len(largas) / n_fr, 2) if n_fr else 0.0
    return {
        "herramienta": "HT-07",
        "version": VERSION,
        "entrada_html": es_html,
        "palabras": n_pal,
        "silabas": n_sil,
        "frases": n_fr,
        "silabas_por_palabra": round(n_sil / n_pal, 3) if n_pal else None,
        "fernandez_huerta": fh,
        "fernandez_huerta_formula": "corregida (Law, 2011): F = palabras por frase",
        "fernandez_huerta_original_informativo": fh_original,
        "interpretacion": interpretar_fh(fh) if fh is not None else None,
        "umbral_fh": umbral_fh,
        "cumple_fh": (fh is not None and fh >= umbral_fh),
        "longitud_media_frase": round(n_pal / n_fr, 2) if n_fr else None,
        "pct_frases_mas_de_20": pct_largas,
        "max_palabras_frase": max_palabras_frase,
        "frases_largas": largas,
        "cumple_frases_cortas": not largas,
        "jerga": jerga,
        "jerga_sin_explicar": sin_explicar,
        "notas": [
            f"Tokens numéricos contados como palabra con {SILABAS_POR_NUMERO} sílabas (estimación).",
            "Silabeo ortográfico por reglas; la «h» intercalada se trata como consonante.",
        ],
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="HT-07 · Medidor de legibilidad (Fernández-Huerta, frases, jerga)")
    ap.add_argument("entrada", help="Archivo de texto plano o HTML ('-' para stdin)")
    ap.add_argument("--html", dest="html", action="store_true", default=None, help="Forzar interpretación HTML")
    ap.add_argument("--texto", dest="html", action="store_false", help="Forzar texto plano")
    ap.add_argument("--jerga", help="Lista de jerga (txt, un término por línea; o JSON lista / {terminos: []})")
    ap.add_argument("--umbral", type=float, default=UMBRAL_FH_POR_DEFECTO, help="Umbral Fernández-Huerta (defecto 70)")
    ap.add_argument("--salida", help="Archivo JSON de salida (por defecto, stdout)")
    a = ap.parse_args(argv)
    try:
        if a.entrada == "-":
            contenido = sys.stdin.read()
        else:
            with open(a.entrada, encoding="utf-8", errors="replace") as fh:
                contenido = fh.read()
        es_html = a.html
        if es_html is None and a.entrada.lower().endswith((".html", ".htm")):
            es_html = True
        res = analizar(contenido, es_html=es_html, terminos_jerga=cargar_jerga(a.jerga), umbral_fh=a.umbral)
    except (OSError, ValueError) as e:
        print(json.dumps({"herramienta": "HT-07", "error": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 3
    salida = json.dumps(res, ensure_ascii=False, indent=2)
    if a.salida:
        with open(a.salida, "w", encoding="utf-8") as fh:
            fh.write(salida + "\n")
    else:
        print(salida)
    return 0 if res["cumple_fh"] else 1


if __name__ == "__main__":
    sys.exit(main())
