"""Utilidades cambiarias del ejecutor del Bloque A Forex: notación BASE/COTIZADA, composición y dirección (2.4),
exposición agregada por divisa (14.1), carry orientado a la tesis, nombres llanos y banderas de las divisas."""
from __future__ import annotations

from typing import Dict, List, Optional

from .herramientas.ht01_datos import parsear_composicion

LADOS = ("LARGO", "CORTO")

# Nombre llano (con artículo) y bandera de cada divisa, para el informe visual y los textos del Analista simulado
DIVISAS: Dict[str, tuple] = {
    "USD": ("el dólar de EE. UU.", "dólar", "🇺🇸"), "EUR": ("el euro", "euro", "🇪🇺"), "JPY": ("el yen japonés", "yen", "🇯🇵"),
    "GBP": ("la libra esterlina", "libra", "🇬🇧"), "CHF": ("el franco suizo", "franco suizo", "🇨🇭"),
    "AUD": ("el dólar australiano", "dólar australiano", "🇦🇺"), "NZD": ("el dólar neozelandés", "dólar neozelandés", "🇳🇿"),
    "CAD": ("el dólar canadiense", "dólar canadiense", "🇨🇦"), "NOK": ("la corona noruega", "corona noruega", "🇳🇴"),
    "SEK": ("la corona sueca", "corona sueca", "🇸🇪"), "CNY": ("el yuan chino", "yuan", "🇨🇳"), "CNH": ("el yuan chino", "yuan", "🇨🇳"),
    "INR": ("la rupia india", "rupia india", "🇮🇳"), "KRW": ("el won coreano", "won", "🇰🇷"), "TWD": ("el dólar taiwanés", "dólar taiwanés", "🇹🇼"),
    "IDR": ("la rupia indonesia", "rupia indonesia", "🇮🇩"), "SGD": ("el dólar de Singapur", "dólar de Singapur", "🇸🇬"),
    "THB": ("el baht tailandés", "baht", "🇹🇭"), "HKD": ("el dólar de Hong Kong", "dólar de Hong Kong", "🇭🇰"),
    "MXN": ("el peso mexicano", "peso mexicano", "🇲🇽"), "BRL": ("el real brasileño", "real", "🇧🇷"),
    "CLP": ("el peso chileno", "peso chileno", "🇨🇱"), "COP": ("el peso colombiano", "peso colombiano", "🇨🇴"),
    "PEN": ("el sol peruano", "sol peruano", "🇵🇪"), "PLN": ("el esloti polaco", "esloti", "🇵🇱"), "HUF": ("el florín húngaro", "florín", "🇭🇺"),
    "CZK": ("la corona checa", "corona checa", "🇨🇿"), "TRY": ("la lira turca", "lira turca", "🇹🇷"), "ZAR": ("el rand sudafricano", "rand", "🇿🇦"),
    "ILS": ("el shekel israelí", "shekel", "🇮🇱"), "EGP": ("la libra egipcia", "libra egipcia", "🇪🇬"),
}


def llano(divisa: str, articulo: bool = True) -> str:
    d = DIVISAS.get(divisa)
    if not d:
        return divisa
    return d[0] if articulo else d[1]


def bandera(divisa: str) -> str:
    return (DIVISAS.get(divisa) or ("", "", "🏳️"))[2]


def lados_par(par: str, direccion: str) -> Dict[str, str]:
    base, cot = par.split("/")
    return {base: "LARGO", cot: "CORTO"} if direccion == "ALCISTA_BASE" else {base: "CORTO", cot: "LARGO"}


def composicion_par(par: str, direccion: str) -> List[Dict]:
    return [{"divisa": d, "peso": 1.0, "lado": l} for d, l in lados_par(par, direccion).items()]


def invertir(composicion: List[Dict]) -> List[Dict]:
    return [{**c, "lado": "CORTO" if c["lado"] == "LARGO" else "LARGO"} for c in composicion]


def composicion_fila(fila: Dict) -> List[Dict]:
    """Composición del indicador tal como cotiza (lo que gana cuando el indicador sube)."""
    if fila.get("composicion"):
        return parsear_composicion(fila["composicion"])
    if fila.get("base") and fila.get("cotizada"):
        return composicion_par(f"{fila['base']}/{fila['cotizada']}", "ALCISTA_BASE")
    return []


def par_de_fila(fila: Dict) -> Optional[str]:
    return f"{fila['base']}/{fila['cotizada']}" if fila.get("base") and fila.get("cotizada") else None


def indicador_sube(op: Dict, fila: Dict) -> bool:
    """True si la tesis espera que suba la serie del indicador de seguimiento."""
    tipo = op.get("tipo_opcion")
    if tipo == "VOLATILIDAD":
        return (op.get("vista_volatilidad") or {}).get("sentido", "ALZA") == "ALZA"
    if op.get("direccion") in ("ALCISTA_BASE", "BAJISTA_BASE"):
        return op["direccion"] == "ALCISTA_BASE"
    base = {c["divisa"]: c["lado"] for c in composicion_fila(fila)}
    propia = {c["divisa"]: c["lado"] for c in (op.get("composicion") or [])}
    comunes = [d for d in base if d in propia]
    return not comunes or base[comunes[0]] == propia[comunes[0]]


def exposicion_neta(opciones: List[Dict]) -> Dict[str, float]:
    neta: Dict[str, float] = {}
    for o in opciones:
        for c in o.get("composicion") or []:
            neta[c["divisa"]] = neta.get(c["divisa"], 0.0) + float(c["peso"]) * (1 if c["lado"] == "LARGO" else -1)
    return {d: round(v, 6) for d, v in neta.items() if abs(v) > 1e-9}


def categoria_exposicion(v: float) -> str:
    if abs(v) < 1e-9:
        return "neutra"
    lado = "larga" if v > 0 else "corta"
    if abs(v) < 1 - 1e-9:
        return f"{lado} moderada"
    if abs(v) >= 2 - 1e-9:
        return f"{lado} fuerte"
    return lado


def signo_carry(v: Optional[float], tipo: str) -> str:
    if v is None:
        return "no aplicable" if tipo == "VOLATILIDAD" else "neutro"
    return "a favor" if v > 0.25 else ("en contra" if v < -0.25 else "neutro")


def sube_baja_llano(composicion: List[Dict], maximo: int = 3) -> str:
    sube = [llano(c["divisa"]) for c in composicion if c["lado"] == "LARGO"][:maximo]
    baja = [llano(c["divisa"]) for c in composicion if c["lado"] == "CORTO"][:maximo]

    def _lista(xs):
        return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " y " + xs[-1]
    if not sube or not baja:
        return ""
    v1 = "Sube" if len(sube) == 1 else "Suben"
    v2 = "baja" if len(baja) == 1 else "bajan"
    t = f"{v1} {_lista(sube)} y {v2} {_lista(baja)}"
    return (t if t.endswith(".") else t + ".")[:160]


JERGA_LLANA = (("carry", "diferencia de intereses"), ("momentum", "tendencia"), ("volatilidad implícita", "movimientos esperados"),
               ("volatilidad", "movimientos"), ("G10", "grandes monedas"))


def sin_jerga(texto: str) -> str:
    """Sustituye la jerga cambiaria más común por su equivalente llano (informe visual, HT-07)."""
    import re
    out = str(texto or "")
    for k, v in JERGA_LLANA:
        out = re.sub(rf"(?i)\b{re.escape(k)}\b", v, out)
    return out[:1].upper() + out[1:] if out else out


def nombre_llano(composicion: List[Dict], tipo: str, nombre: str) -> str:
    largos = [c["divisa"] for c in composicion if c["lado"] == "LARGO"]
    cortos = [c["divisa"] for c in composicion if c["lado"] == "CORTO"]
    if tipo in ("PAR", "CRUCE", "REGIMEN") and len(largos) == 1 and len(cortos) == 1:
        t = f"{llano(largos[0])} podría ganar valor frente a {llano(cortos[0])}"
        t = t.replace("frente a el ", "frente al ")
        return (t[0].upper() + t[1:])[:70]
    if tipo == "VOLATILIDAD":
        return sin_jerga(f"Los movimientos de {nombre}")[:70]
    return sin_jerga(nombre)[:70]
