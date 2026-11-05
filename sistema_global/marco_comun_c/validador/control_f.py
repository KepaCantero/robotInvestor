"""F — control de riesgo previo a la autorización (CT-G-08, reglas de control F-01..F-11 y de verificación CF-01..CF-07).

Determinista, sin LLM, sin red. F calcula su propia exposición a partir de la cartera que recibe; no consume M.
`controlar` aplica las reglas y devuelve el informe; `validar_informe_f` lo verifica sin fiarse de él: lo
vuelve a calcular con las mismas entradas. Todos los límites son valores de partida [PROPUESTO].
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from datetime import timedelta

from validar_sobre import _dt

VERSION_REGLAS = "F-0.1.0"
POLITICA_DEFECTO = {"riesgo_max_pct": 1.0, "tamano_max_pct": 10.0, "exposicion_max_pct": 100.0,
                    "concentracion_max_pct": 20.0, "perdida_dia_max_pct": 2.0, "max_posiciones": 10,
                    "apalancamiento_max": 1.0, "frescura_max_min": 60.0, "valor_min_eur": 100.0,
                    "vigencia_max_horas": 24.0}
CLAVES_POLITICA = set(POLITICA_DEFECTO)
CARTERAS = {"TRADING", "TACTICA", "LARGO_PLAZO"}
ID = re.compile(r"^[A-Za-z0-9._:/-]{1,64}\Z")
FH = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})\Z")
ERRORES = (KeyError, TypeError, AttributeError, ValueError, IndexError, OverflowError, RecursionError, MemoryError)
ORDEN_SOLICITUD = {"instrumento", "activo_base", "direccion", "cantidad", "precio_entrada", "stop_precio", "apalancamiento", "cartera"}


def hash_contenido(x) -> str:
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _num(x, minimo=None, estricto=False):
    if not isinstance(x, (int, float)) or isinstance(x, bool) or not math.isfinite(x):
        return False
    return minimo is None or (x > minimo if estricto else x >= minimo)


def politica_valida(p) -> bool:
    return (isinstance(p, dict) and set(p) == CLAVES_POLITICA
            and all(_num(p[k], 0, True) for k in CLAVES_POLITICA)
            and isinstance(p["max_posiciones"], int) and not isinstance(p["max_posiciones"], bool)
            and p["apalancamiento_max"] >= 1
            and all(p[k] <= 100 for k in ("riesgo_max_pct", "tamano_max_pct", "exposicion_max_pct", "concentracion_max_pct", "perdida_dia_max_pct"))
            and p["concentracion_max_pct"] <= p["exposicion_max_pct"] and p["tamano_max_pct"] <= p["exposicion_max_pct"]
            and p["max_posiciones"] <= 1000 and p["apalancamiento_max"] <= 100 and p["vigencia_max_horas"] <= 168)


def _forma(sol, cart, pol, ahora) -> str | None:
    """Devuelve el motivo del primer defecto de forma, o None."""
    if not (isinstance(sol, dict) and set(sol) == ORDEN_SOLICITUD):
        return "solicitud con campos distintos de los exigidos"
    if not (isinstance(sol["instrumento"], str) and ID.match(sol["instrumento"]) and isinstance(sol["activo_base"], str) and ID.match(sol["activo_base"])):
        return "instrumento o activo_base inválidos"
    if sol["direccion"] not in ("LARGO", "CORTO") or sol["cartera"] not in CARTERAS:
        return "dirección o cartera inválidas"
    if not (_num(sol["cantidad"], 0, True) and _num(sol["precio_entrada"], 0, True) and _num(sol["stop_precio"], 0, True)
            and _num(sol["apalancamiento"], 1)):
        return "cantidad, precios o apalancamiento no válidos"
    if not politica_valida(pol):
        return "política inválida"
    if not (isinstance(cart, dict) and set(cart) == {"fecha_hora", "capital_eur", "perdida_dia_eur", "posiciones"}
            and isinstance(cart["fecha_hora"], str) and FH.match(cart["fecha_hora"]) and _num(cart["capital_eur"], 0, True)
            and _num(cart["perdida_dia_eur"], 0) and isinstance(cart["posiciones"], list)):
        return "estado de cartera inválido"
    for p in cart["posiciones"]:
        if not (isinstance(p, dict) and set(p) == {"instrumento", "activo_base", "valor_eur"} and isinstance(p["activo_base"], str)
                and ID.match(p["activo_base"]) and isinstance(p["instrumento"], str) and ID.match(p["instrumento"]) and _num(p["valor_eur"], 0)):
            return "posición de cartera inválida"
    if not (isinstance(ahora, str) and FH.match(ahora)):
        return "fecha de cálculo inválida"
    return None


def controlar(sol, cart, pol, ahora) -> dict:
    """Aplica F-01..F-11. Nunca lanza excepciones: cualquier fallo es un VETADO. Devuelve
    {resultado, cantidad_aprobada, controles}."""
    try:
        return _controlar(sol, cart, pol, ahora)
    except ERRORES as e:
        return {"resultado": "VETADO", "cantidad_aprobada": 0.0,
                "controles": [{"regla": "F-01", "resultado": "VETA", "valor": None, "limite": None, "motivo": f"error de cálculo: {type(e).__name__}"}]}


def _c(regla, resultado, valor=None, limite=None, motivo=""):
    return {"regla": regla, "resultado": resultado, "valor": valor, "limite": limite, "motivo": motivo}


def _controlar(sol, cart, pol, ahora):
    mal = _forma(sol, cart, pol, ahora)
    if mal:
        return {"resultado": "VETADO", "cantidad_aprobada": 0.0, "controles": [_c("F-01", "VETA", motivo=mal)]}
    cap_total = cart["capital_eur"]
    ent, stop, q = sol["precio_entrada"], sol["stop_precio"], sol["cantidad"]
    ctl = [_c("F-01", "OK")]
    # F-02 el stop existe y está del lado que pierde
    lado_ok = stop < ent if sol["direccion"] == "LARGO" else stop > ent
    ctl.append(_c("F-02", "OK" if lado_ok else "VETA", stop, ent, "" if lado_ok else "el stop debe estar del lado de la pérdida"))
    # F-05 apalancamiento
    ap_ok = sol["apalancamiento"] <= pol["apalancamiento_max"]
    ctl.append(_c("F-05", "OK" if ap_ok else "VETA", sol["apalancamiento"], pol["apalancamiento_max"]))
    # F-08 pérdida del día
    lim_perd = pol["perdida_dia_max_pct"] / 100 * cap_total
    ctl.append(_c("F-08", "OK" if cart["perdida_dia_eur"] < lim_perd else "VETA", cart["perdida_dia_eur"], lim_perd))
    # F-09 número de posiciones
    npos = len(cart["posiciones"])
    ctl.append(_c("F-09", "OK" if npos < pol["max_posiciones"] else "VETA", npos, pol["max_posiciones"]))
    # F-10 frescura del estado de cartera
    edad = (_dt(ahora) - _dt(cart["fecha_hora"])).total_seconds() / 60
    fresco = 0 <= edad <= pol["frescura_max_min"]
    ctl.append(_c("F-10", "OK" if fresco else "VETA", edad, pol["frescura_max_min"], "" if fresco else "estado de cartera viejo o del futuro"))
    # topes de cantidad (REDUCE si la solicitud los supera)
    expuesto = sum(p["valor_eur"] for p in cart["posiciones"])
    mismo = sum(p["valor_eur"] for p in cart["posiciones"] if p["activo_base"] == sol["activo_base"])
    riesgo_unit = abs(ent - stop)
    topes = [("F-03", pol["riesgo_max_pct"] / 100 * cap_total / riesgo_unit if riesgo_unit > 0 else 0.0),
             ("F-04", pol["tamano_max_pct"] / 100 * cap_total / ent),
             ("F-06", max(0.0, pol["exposicion_max_pct"] / 100 * cap_total - expuesto) / ent),
             ("F-07", max(0.0, pol["concentracion_max_pct"] / 100 * cap_total - mismo) / ent)]
    for regla, tope in topes:
        ctl.append(_c(regla, "OK" if q <= tope else "REDUCE", q, tope))
    veta = any(x["resultado"] == "VETA" for x in ctl)
    aprobada = min([q] + [t for _, t in topes])
    aprobada = math.floor(aprobada * 1e6) / 1e6
    # F-11 una reducción que deja una posición sin sentido se veta
    ctl.append(_c("F-11", "OK" if aprobada * ent >= pol["valor_min_eur"] else "VETA", aprobada * ent, pol["valor_min_eur"]))
    veta = veta or ctl[-1]["resultado"] == "VETA"
    if veta:
        return {"resultado": "VETADO", "cantidad_aprobada": 0.0, "controles": ctl}
    return {"resultado": "REDUCIDO" if aprobada < q else "APROBADO", "cantidad_aprobada": aprobada, "controles": ctl}


def construir_informe(event_id, expediente_id, correlation_id, propuesta, sol, cart, pol, emitido_en, valid_until) -> dict:
    r = controlar(sol, cart, pol, emitido_en)
    return {"event_id": event_id, "correlation_id": correlation_id, "expediente_id": expediente_id, "producer": "F",
            "consumer": "ORQUESTADOR", "tipo_mensaje": "CT-G-08", "version_esquema": "0.1.0", "emitido_en": emitido_en,
            "valid_until": valid_until, "version_reglas": VERSION_REGLAS,
            "propuesta_ref": {"expediente_id": expediente_id, "hash": hash_contenido(propuesta)},
            "entradas": {"solicitud": sol, "cartera": cart, "politica": pol},
            "resultado": r["resultado"], "cantidad_aprobada": r["cantidad_aprobada"], "controles": r["controles"]}


CAMPOS = {"event_id", "correlation_id", "expediente_id", "producer", "consumer", "tipo_mensaje", "version_esquema", "emitido_en",
          "valid_until", "version_reglas", "propuesta_ref", "entradas", "resultado", "cantidad_aprobada", "controles"}


def validar_informe_f(inf, ctx) -> list[dict]:
    """ctx: ahora, expediente_id, correlation_id, propuesta (la registrada en el expediente), cartera_destino,
    politica (la oficial del Orquestador). Nunca lanza excepciones."""
    try:
        return _validar(inf, ctx)
    except ERRORES as e:
        return [{"regla": "CF-01", "mensaje": f"entrada o contexto mal formado: {type(e).__name__}"}]


def _validar(inf, ctx):
    fallos = []

    def f(regla, m):
        fallos.append({"regla": regla, "mensaje": m})

    ahora, prop = _dt(ctx["ahora"]), ctx["propuesta"]
    if not (isinstance(inf, dict) and set(inf) == CAMPOS):
        return [{"regla": "CF-01", "mensaje": "campos distintos de los exigidos"}]
    if not (inf["producer"] == "F" and inf["consumer"] == "ORQUESTADOR" and inf["tipo_mensaje"] == "CT-G-08"
            and inf["version_esquema"] == "0.1.0" and inf["version_reglas"] == VERSION_REGLAS
            and isinstance(inf["event_id"], str) and ID.match(inf["event_id"])
            and inf["resultado"] in ("APROBADO", "REDUCIDO", "VETADO") and _num(inf["cantidad_aprobada"], 0)
            and isinstance(inf["emitido_en"], str) and FH.match(inf["emitido_en"]) and isinstance(inf["valid_until"], str) and FH.match(inf["valid_until"])
            and isinstance(inf["entradas"], dict) and set(inf["entradas"]) == {"solicitud", "cartera", "politica"}
            and isinstance(inf["propuesta_ref"], dict) and set(inf["propuesta_ref"]) == {"expediente_id", "hash"}
            and isinstance(inf["controles"], list)):
        return [{"regla": "CF-01", "mensaje": "forma inválida"}]
    # CF-02 el informe es de esta propuesta
    if (inf["expediente_id"] != ctx["expediente_id"] or inf["correlation_id"] != ctx["correlation_id"]
            or inf["propuesta_ref"] != {"expediente_id": ctx["expediente_id"], "hash": hash_contenido(prop)}):
        f("CF-02", "el informe no corresponde a esta propuesta (expediente, petición o hash)")
    # CF-03 tiempos
    em, vu = _dt(inf["emitido_en"]), _dt(inf["valid_until"])
    if not (em <= ahora <= vu) or vu - em > timedelta(hours=ctx["politica"]["vigencia_max_horas"]):
        f("CF-03", "el informe debe estar emitido, vigente y no durar más que la política")
    cart_f = inf["entradas"]["cartera"].get("fecha_hora") if isinstance(inf["entradas"]["cartera"], dict) else None
    if not (isinstance(cart_f, str) and FH.match(cart_f)) or not (0 <= (ahora - _dt(cart_f)).total_seconds() / 60 <= ctx["politica"]["frescura_max_min"]):
        f("CF-03", "el estado de cartera es viejo respecto a ahora (o del futuro)")
    # CF-07 la política es la oficial, no una más laxa
    if inf["entradas"]["politica"] != ctx["politica"]:
        f("CF-07", "la política usada no es la oficial del Orquestador")
    # CF-05 la solicitud es la propuesta
    sol = inf["entradas"]["solicitud"]
    stops = [c for c in prop["salida"]["condiciones"] if c.get("tipo") == "STOP"]
    if len(stops) != 1:
        f("CF-05", "la propuesta debe tener exactamente un STOP")
    else:
        direccion = "LARGO" if stops[0]["operador"] in ("<", "<=") else "CORTO"
        en = prop["entrada"]
        if not (isinstance(sol, dict) and sol.get("precio_entrada") == en["limite"] and sol.get("stop_precio") == stops[0]["umbral"]
                and sol.get("direccion") == direccion and sol.get("cartera") == ctx["cartera_destino"]
                and sol.get("instrumento") == en["instrumento"] and sol.get("activo_base") == en["activo_base"]
                and sol.get("apalancamiento") == en["apalancamiento"] and sol.get("cantidad") == en["cantidad"]):
            f("CF-05", "la solicitud no coincide con la propuesta (límite, stop, dirección, cartera, instrumento, activo base, apalancamiento y cantidad)")
    # CF-04 se recalcula con las mismas entradas
    r = controlar(sol, inf["entradas"]["cartera"], inf["entradas"]["politica"], inf["emitido_en"])
    if (r["resultado"], r["cantidad_aprobada"], r["controles"]) != (inf["resultado"], inf["cantidad_aprobada"], inf["controles"]):
        f("CF-04", "el resultado no es el que dan las reglas con esas entradas")
    # CF-08 la cartera debe incluir todo lo que el Orquestador ya tiene comprometido en esa cartera
    pos = inf["entradas"]["cartera"].get("posiciones") if isinstance(inf["entradas"]["cartera"], dict) else None
    if isinstance(pos, list):
        vistos = {}
        for p in pos:
            if isinstance(p, dict):
                k = (p.get("instrumento"), p.get("activo_base"))
                vistos[k] = vistos.get(k, 0) + 1
        pedidos = {}
        for c in ctx.get("compromisos", []):
            k = (c[0], c[1])
            pedidos[k] = pedidos.get(k, 0) + 1
        for k, nveces in pedidos.items():
            if vistos.get(k, 0) < nveces:
                f("CF-08", f"la cartera del informe omite una posición o autorización ya comprometida: {k[0]}")
                break
    # CF-06 coherencia
    if inf["resultado"] == "VETADO" and inf["cantidad_aprobada"] != 0:
        f("CF-06", "un veto no aprueba cantidad")
    if isinstance(sol, dict) and _num(sol.get("cantidad")) and inf["cantidad_aprobada"] > sol["cantidad"]:
        f("CF-06", "no se puede aprobar más de lo solicitado")
    return fallos
