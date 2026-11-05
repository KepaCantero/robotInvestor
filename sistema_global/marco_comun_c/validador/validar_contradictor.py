"""Validador determinista del informe del Contradictor CT-G-03 0.2.0 (reglas C-01 a C-13).

0.2.0 (T-48): autoría con diversidad respecto a C (C-11), escenarios en que la tesis falla con disparador medible (C-12) y
objeciones mayores o críticas ligadas a ellos (C-13). La 0.1.0 está retirada.

Sin LLM, sin red, sin reloj propio. Nunca lanza excepciones por un mensaje mal formado.
"""
from __future__ import annotations

import hashlib
import json
import unicodedata
from pathlib import Path

from jsonschema import Draft202012Validator

from validar_sobre import _dt, _numeros_no_finitos

AQUI = Path(__file__).resolve().parent
ORDEN = {"MENOR": 0, "MAYOR": 1, "CRITICA": 2}
VEREDICTO_DE = {0: "SIN_OBJECIONES_RELEVANTES", 1: "OBJECION_MAYOR", 2: "OBJECION_CRITICA"}
ERRORES = (KeyError, TypeError, AttributeError, ValueError, IndexError, OverflowError, RecursionError, MemoryError)


def hash_contenido(x) -> str:
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _esquema():
    return json.loads((AQUI.parent / "esquemas" / "ct-g-03_0.2.0.schema.json").read_text(encoding="utf-8"))


VERSION = "0.2.0"
VERSIONES_RETIRADAS = {"0.1.0"}


def _norma(x):
    """Identificador de modelo o proveedor comparable: NFKC, sin mayúsculas y sin nada que no sea letra o cifra
    («Proveedor A.», «proveedor_a» y «PROVEEDOR A» son el mismo)."""
    return "".join(c for c in unicodedata.normalize("NFKC", x).casefold() if c.isalnum())


def misma_autoria(a, b):
    return _norma(a["modelo"]) == _norma(b["modelo"]) and _norma(a["proveedor"]) == _norma(b["proveedor"])


def diversidad(autor, autoria_c):
    """MISMO_MODELO (el mismo modelo, lo sirva quien lo sirva), OTRO_PROVEEDOR u OTRO_MODELO respecto a la autoría de C;
    None si no se conoce la de C."""
    if not (isinstance(autoria_c, dict) and isinstance(autoria_c.get("modelo"), str) and isinstance(autoria_c.get("proveedor"), str)):
        return None
    if _norma(autor["modelo"]) == _norma(autoria_c["modelo"]):
        return "MISMO_MODELO"   # T-48 (revisión): un mismo modelo revendido por otro proveedor no aporta diversidad
    return "OTRO_PROVEEDOR" if _norma(autor["proveedor"]) != _norma(autoria_c["proveedor"]) else "OTRO_MODELO"


def validar_informe(msg, ctx) -> list[dict]:
    """ctx: ahora (ISO con zona), sobre (el sobre CT-G-02 revisado) y, opcionales, autoria_c ({modelo, proveedor} de C) y
    autoria_contradictor ({modelo, proveedor} del Contradictor que el operador tiene configurado)."""
    try:
        return _validar(msg, ctx)
    except ERRORES as e:
        return [{"regla": "C-01", "ruta": "(interno)", "mensaje": f"entrada o contexto mal formado: {type(e).__name__}: {e}"}]


def _validar(msg, ctx) -> list[dict]:
    fallos: list[dict] = []

    def f(regla, ruta, m):
        fallos.append({"regla": regla, "ruta": ruta, "mensaje": m})

    try:
        ahora, sobre = _dt(ctx["ahora"]), ctx["sobre"]
        sobre["event_id"], sobre["payload"], sobre["data_refs"]
    except ERRORES as e:
        return [{"regla": "C-01", "ruta": "contexto", "mensaje": f"contexto de validación inválido: {e}"}]
    ver = msg.get("version_esquema") if isinstance(msg, dict) else None
    if ver != VERSION:
        estado = "retirada" if ver in VERSIONES_RETIRADAS else "desconocida"
        return [{"regla": "C-01", "ruta": "version_esquema", "mensaje": f"versión {estado}: {ver!r} (vigente {VERSION})"}]
    for ruta in _numeros_no_finitos(msg):
        f("C-01", ruta, "número no finito")
    if fallos:
        return fallos
    for e in sorted(Draft202012Validator(_esquema()).iter_errors(msg), key=lambda e: [str(x) for x in e.absolute_path]):
        f("C-01", ".".join(str(x) for x in e.absolute_path) or "(raíz)", e.message[:200])
    if fallos:
        return fallos

    p = msg["payload"]
    # C-02 el informe revisa exactamente este sobre
    if p["sobre_ref"]["event_id"] != sobre["event_id"] or p["sobre_ref"]["hash"] != hash_contenido(sobre):
        f("C-02", "payload.sobre_ref", "no coincide con el sobre del expediente (id o hash)")
    if msg["expediente_id"] != sobre.get("expediente_id") or msg["correlation_id"] != sobre.get("correlation_id"):
        f("C-02", "expediente_id", "el informe no pertenece a este expediente o petición")
    # C-03 independencia
    for k, v in p["independencia"].items():
        if v is not False:
            f("C-03", f"payload.independencia.{k}", "el Contradictor no puede haber visto la conclusión, la confianza ni el contexto de C")
    # C-04 objeciones bien formadas
    ids = [o["id"] for o in p["objeciones"]]
    if msg["event_id"] == sobre["event_id"]:
        f("C-04", "event_id", "el informe no puede reutilizar el event_id del sobre")
    if len(set(ids)) != len(ids):
        f("C-04", "payload.objeciones", "ids de objeción repetidos")
    # C-05 las objeciones mayores o críticas citan evidencia del sobre
    refs_sobre = set(sobre["data_refs"])
    for i, o in enumerate(p["objeciones"]):
        if o["gravedad"] != "MENOR" and not o["evid_refs"]:
            f("C-05", f"payload.objeciones.{i}.evid_refs", "una objeción MAYOR o CRITICA debe citar evidencia")
        for r in o["evid_refs"]:
            if r not in refs_sobre:
                f("C-05", f"payload.objeciones.{i}.evid_refs", f"{r!r} no está en la evidencia del sobre")
    # C-06 el veredicto es el que dicen las objeciones
    esperado = VEREDICTO_DE[max((ORDEN[o["gravedad"]] for o in p["objeciones"]), default=0)]
    if p["veredicto"] != esperado:
        f("C-06", "payload.veredicto", f"debe ser {esperado} según las objeciones")
    # C-07 y C-10 cobertura
    secciones = set(sobre["payload"])
    rev = set(p["cobertura"]["revisadas"])
    no_rev = [x["seccion"] for x in p["cobertura"]["no_revisadas"]]
    if len(set(no_rev)) != len(no_rev) or rev & set(no_rev) or not (rev | set(no_rev)) <= secciones:
        f("C-10", "payload.cobertura", "la cobertura repite partes, las mezcla o cita partes que no existen en el sobre")
    if (rev | set(no_rev)) != secciones:
        f("C-10", "payload.cobertura", "la cobertura debe cubrir todas las partes del sobre, revisadas o no")
    if no_rev and p["veredicto"] == "SIN_OBJECIONES_RELEVANTES":
        f("C-10", "payload.veredicto", "con partes sin revisar no puede ser SIN_OBJECIONES_RELEVANTES")
    if not p["objeciones"] and no_rev:
        f("C-07", "payload.cobertura", "un informe sin objeciones debe haber revisado todo el sobre")
    # C-11 autoría y diversidad
    a = p["autoria"]
    if (a["diversidad"] == "MISMO_MODELO") != ("motivo_mismo_modelo" in a):
        f("C-11", "payload.autoria.motivo_mismo_modelo", "MISMO_MODELO exige motivo (y solo él lo lleva)")
    esperada = ctx.get("autoria_contradictor")
    if isinstance(esperada, dict) and not misma_autoria(a, esperada):
        f("C-11", "payload.autoria", "no es el Contradictor que tiene configurado el operador (modelo y proveedor)")
    real = diversidad(a, ctx.get("autoria_c"))
    if real is not None and real != a["diversidad"]:
        f("C-11", "payload.autoria.diversidad", f"declara {a['diversidad']} pero, con la autoría de C, es {real}")
    # C-12 escenarios en que la tesis falla
    esc = p["escenarios_fallo"]
    ids_esc = [e["id"] for e in esc]
    if len(set(ids_esc)) != len(ids_esc):
        f("C-12", "payload.escenarios_fallo", "ids de escenario repetidos")
    for i, e in enumerate(esc):
        if e["consecuencia"] == "PERDIDA":
            if not ("perdida_pct" in e and -100 <= e["perdida_pct"] < 0):
                f("C-12", f"payload.escenarios_fallo.{i}.perdida_pct", "una PERDIDA declara perdida_pct entre -100 y 0 (sin incluir 0)")
        elif "perdida_pct" in e:
            f("C-12", f"payload.escenarios_fallo.{i}.perdida_pct", "solo una PERDIDA lleva perdida_pct")
        for r in e["evid_refs"]:
            if r not in refs_sobre:
                f("C-12", f"payload.escenarios_fallo.{i}.evid_refs", f"{r!r} no está en la evidencia del sobre")
    # C-13 las objeciones apuntan a escenarios de fallo que existen; las mayores y críticas, al menos a uno
    for i, o in enumerate(p["objeciones"]):
        if o["gravedad"] != "MENOR" and not o["escenarios"]:
            f("C-13", f"payload.objeciones.{i}.escenarios", "una objeción MAYOR o CRITICA dice en qué escenario falla la tesis")
        for x in o["escenarios"]:
            if x not in ids_esc:
                f("C-13", f"payload.objeciones.{i}.escenarios", f"{x!r} no es un escenario de fallo del informe")
    # C-08 nivel
    if p["nivel_analisis"] != sobre["payload"].get("identificacion", {}).get("nivel_analisis"):
        f("C-08", "payload.nivel_analisis", "distinto del nivel del sobre")
    # C-09 tiempos
    em, vu = _dt(msg["emitido_en"]), _dt(msg["valid_until"])
    if em < _dt(sobre["emitido_en"]) or em > ahora:
        f("C-09", "emitido_en", "el informe debe emitirse después del sobre y no en el futuro")
    if not (em < vu <= _dt(sobre["valid_until"])) or ahora > vu:
        f("C-09", "valid_until", "el informe debe vencer después de emitirse, no más tarde que el sobre, y no haber vencido")
    return fallos
