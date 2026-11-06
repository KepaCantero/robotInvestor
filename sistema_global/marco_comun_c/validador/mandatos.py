"""SC-1 — perfil y mandato de cada cartera (código de referencia V0.32, T-51).

La Constitución (§7 y tabla de servicios) pone el mandato de cada cartera en SC-1, fuente única de objetivos, horizonte,
benchmark, riesgo y límites. El encargo CT-G-01 0.2.0 ya no lleva el mandato dentro: lo cita por versión y huella
(`mandato_ref`) y, si hace falta, lo estrecha con `restricciones` (nunca lo amplía). C y quien valide el encargo leen el
mandato de aquí. Determinista, sin LLM y sin reloj. Los valores son de partida [PROPUESTO] (P-03, D-28).
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import re
import unicodedata

VERSION_SC1 = "SC1-0.1.0"
CARTERAS = ("TRADING", "TACTICA", "LARGO_PLAZO")
# Rango de horizonte de cada clase de cartera (§7: el trading opera en días y semanas) [PROPUESTO]: el mandato vive dentro
HORIZONTE_CARTERA = {"TRADING": (1, 28), "TACTICA": (14, 183), "LARGO_PLAZO": (1095, 7300)}
CLAVES = {"version", "benchmark_ref", "horizonte_dias", "apalancamiento_max", "tamano_max_pct_cartera", "instrumentos_permitidos", "exclusiones"}
CLAVES_RESTRICCIONES = {"horizonte_dias", "tamano_max_pct_cartera", "exclusiones"}
_ID = re.compile(r"^[A-Za-z0-9._:/-]{1,64}\Z")
_VERSION = re.compile(r"^MAN-\d+\.\d+\.\d+\Z")


def _mandato(c, tamano=10.0):
    lo, hi = HORIZONTE_CARTERA[c]
    return {"version": "MAN-0.1.0", "benchmark_ref": "BENCH-EFECTIVO", "horizonte_dias": {"min": lo, "max": hi},
            "apalancamiento_max": 1, "tamano_max_pct_cartera": tamano,
            "instrumentos_permitidos": None,   # None: cualquiera del universo admitido; una lista: solo esos
            "exclusiones": []}


MANDATOS_DEFECTO = {c: _mandato(c) for c in CARTERAS}


def _num(x):
    try:
        return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)
    except OverflowError:
        return False


def _entero(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _texto(x):
    return isinstance(x, str) and x.strip() == x and 0 < len(x) <= 120


def norm(t):
    """Identidad única de un instrumento en todo el sistema (revisión T-51, H1): NFKC, mayúsculas y solo letras y cifras
    latinas, de modo que «EUR/USD», «eur-usd», «EUR USD» o «EUR\u200bUSD» son el mismo instrumento. None si no es texto."""
    if not isinstance(t, str):
        return None
    return re.sub(r"[^A-Z0-9]", "", unicodedata.normalize("NFKC", t).upper())


def _horizonte_ok(h):
    return isinstance(h, dict) and set(h) == {"min", "max"} and _entero(h["min"]) and _entero(h["max"]) and 1 <= h["min"] <= h["max"]


def _lista_textos(x, vacia=True):
    """Lista de instrumentos: textos con identidad no vacía y sin repetir identidad (H1)."""
    return (isinstance(x, list) and bool(vacia or x) and all(_texto(i) and norm(i) for i in x)
            and len({norm(i) for i in x}) == len(x))


def mandato_ok(cartera, m, apalancamiento_permitido=False):
    """Motivo por el que el mandato de una cartera no vale, o None. Lo comprueba el Orquestador al arrancar."""
    if cartera not in CARTERAS:
        return f"cartera desconocida: {cartera!r}"
    if not (isinstance(m, dict) and set(m) == CLAVES):
        return f"el mandato de {cartera} debe tener exactamente {sorted(CLAVES)}"
    if not (isinstance(m["version"], str) and _VERSION.match(m["version"])):
        return "versión del mandato mal formada (MAN-x.y.z)"
    if not (isinstance(m["benchmark_ref"], str) and _ID.match(m["benchmark_ref"])):
        return "benchmark_ref mal formado"
    lo, hi = HORIZONTE_CARTERA[cartera]
    if not (_horizonte_ok(m["horizonte_dias"]) and lo <= m["horizonte_dias"]["min"] and m["horizonte_dias"]["max"] <= hi):
        return f"horizonte del mandato fuera del rango {lo}–{hi} días de {cartera}"
    ap = m["apalancamiento_max"]
    if not (_num(ap) and 1 <= ap <= 10 and (ap == 1 or apalancamiento_permitido is True)):
        return "apalancamiento_max: 1 (sin apalancar) salvo que el apalancamiento esté permitido, y nunca más de 10"
    if not (_num(m["tamano_max_pct_cartera"]) and 0 < m["tamano_max_pct_cartera"] <= 100):
        return "tamano_max_pct_cartera entre 0 (sin incluir) y 100"
    if m["instrumentos_permitidos"] is not None and not _lista_textos(m["instrumentos_permitidos"], vacia=False):
        return "instrumentos_permitidos: None o una lista no vacía de textos distintos"
    if not _lista_textos(m["exclusiones"]):
        return "exclusiones: una lista de textos distintos"
    return None


def _canon(x):
    """La misma forma canónica que la huella de configuración del Orquestador: 10 y 10.0 cuentan igual (revisión T-51, H6)."""
    if isinstance(x, dict):
        return {str(k): _canon(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_canon(v) for v in x]
    if isinstance(x, int) and not isinstance(x, bool):
        return float(x)
    return x


def huella(m) -> str:
    return hashlib.sha256(json.dumps(_canon(m), sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()


def referencia(m) -> dict:
    """Lo que un encargo cita del mandato: su versión y su huella."""
    return {"version": m["version"], "huella": huella(m)}


def restricciones_fallos(m, r):
    """(regla, ruta, mensaje) por cada restricción del encargo que no estrecha el mandato (E-05, E-07, E-10)."""
    out = []
    if r is None:
        return out
    if not (isinstance(r, dict) and r and set(r) <= CLAVES_RESTRICCIONES):
        return [("E-01", "payload.restricciones", f"solo admite {sorted(CLAVES_RESTRICCIONES)} y al menos una")]
    if "horizonte_dias" in r:
        h, hm = r["horizonte_dias"], m["horizonte_dias"]
        if not _horizonte_ok(h):
            out.append(("E-05", "payload.restricciones.horizonte_dias", "min mayor que max o mal formado"))
        elif h["min"] < hm["min"] or h["max"] > hm["max"]:
            out.append(("E-05", "payload.restricciones.horizonte_dias", f"más amplio que el del mandato ({hm['min']}–{hm['max']} días)"))
    if "tamano_max_pct_cartera" in r and not (_num(r["tamano_max_pct_cartera"]) and 0 < r["tamano_max_pct_cartera"] <= m["tamano_max_pct_cartera"]):
        out.append(("E-07", "payload.restricciones.tamano_max_pct_cartera", f"mayor que el del mandato ({m['tamano_max_pct_cartera']} %)"))
    if "exclusiones" in r and not _lista_textos(r["exclusiones"], vacia=False):
        out.append(("E-01", "payload.restricciones.exclusiones", "una lista no vacía de textos distintos"))
    return out


def efectivo(m, r=None) -> dict:
    """El mandato con las restricciones del encargo aplicadas (solo estrechan; se supone ya comprobado)."""
    e = copy.deepcopy(m)
    r = r or {}
    if "horizonte_dias" in r:
        e["horizonte_dias"] = dict(r["horizonte_dias"])
    if "tamano_max_pct_cartera" in r:
        e["tamano_max_pct_cartera"] = r["tamano_max_pct_cartera"]
    e["exclusiones"] = list(m["exclusiones"]) + [x for x in r.get("exclusiones", []) if norm(x) not in {norm(y) for y in m["exclusiones"]}]
    return e


def instrumento_fallo(m_efectivo, instrumento):
    """Motivo por el que el mandato (ya con las restricciones) no admite el instrumento, o None (E-10)."""
    i = norm(instrumento)
    if m_efectivo["instrumentos_permitidos"] is not None and i not in {norm(x) for x in m_efectivo["instrumentos_permitidos"]}:
        return "no figura entre los instrumentos permitidos del mandato"
    if i in {norm(x) for x in m_efectivo["exclusiones"]}:
        return "figura en las exclusiones del mandato o del encargo"
    return None
