"""Validador determinista del encargo CT-G-01 0.1.0 (reglas E-01 a E-12) y
comprobación de que un sobre CT-G-02 responde a su encargo (reglas R-01 a R-08).

Sin LLM, sin red, sin reloj propio. Nunca lanza excepciones por un mensaje mal formado.
Todos los límites numéricos son valores de partida [PROPUESTO] y se pasan en el contexto.
"""
from __future__ import annotations

import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

from jsonschema import Draft202012Validator

from validar_sobre import _dt, _numeros_no_finitos, cargar_json

AQUI = Path(__file__).resolve().parent
VERSIONES_CONOCIDAS = {"0.1.0"}
VIGENCIA_MAX = timedelta(days=30)
# Valores de partida por cartera (P-03, P-04, P-11, P-13 del cuestionario) [PROPUESTO]
HORIZONTE_DIAS = {"TRADING": (1, 28), "TACTICA": (14, 183), "LARGO_PLAZO": (1095, 7300)}
ANTIGUEDAD_CORTE_DIAS = {"TRADING": 1, "TACTICA": 1, "LARGO_PLAZO": 5}   # días HÁBILES
CON_POSICION = {"AUMENTAR", "REDUCIR", "CERRAR", "MANTENER"}


def _dias_habiles(desde, hasta):
    """Días hábiles (lunes a viernes) entre dos fechas; festivos no se consideran."""
    n, d = 0, desde
    while d < hasta:
        d += timedelta(days=1)
        if d.weekday() < 5:
            n += 1
    return n


def _norm(t):
    return t.strip().upper()
TAMANO_MAX_PCT = {"TRADING": 10.0, "TACTICA": 10.0, "LARGO_PLAZO": 10.0}
NIVEL_ORDEN = {"N0": 0, "N1": 1, "N2": 2, "N3": 3}
NIVEL_MIN_POR_DECISION = {"ABRIR_POSICION": "N2", "AUMENTAR": "N2"}
NIVEL_MAX_POR_DECISION = {"DESCARTAR": "N1", "EXPLORAR": "N1"}
PRODUCTOR_POR_CARTERA = {"TRADING": "GESTOR_TRADING", "TACTICA": "GESTOR_TACTICA",
                         "LARGO_PLAZO": "GESTOR_LARGO_PLAZO"}


def _esquema():
    ruta = AQUI.parent / "esquemas" / "ct-g-01_0.1.0.schema.json"
    return json.loads(ruta.read_text(encoding="utf-8"))


def validar_encargo(msg, ctx) -> list[dict]:
    """Nunca lanza excepciones: un contexto o mensaje defectuoso se rechaza con E-01."""
    try:
        return _validar_encargo(msg, ctx)
    except (KeyError, TypeError, AttributeError, ValueError, IndexError) as e:
        return [{"regla": "E-01", "ruta": "(interno)", "mensaje": f"entrada o contexto mal formado: {type(e).__name__}: {e}"}]


def _validar_encargo(msg, ctx) -> list[dict]:
    """ctx: ahora (ISO con zona), fecha_corte_vigente (la de K), perfiles_activos,
    apalancamiento_permitido, y opcionales: horizonte_dias, antiguedad_corte_dias,
    tamano_max_pct, presupuesto_minimo {nivel: {coste_eur, tiempo_min}}, coste_max_eur."""
    fallos: list[dict] = []

    def f(regla, ruta, m):
        fallos.append({"regla": regla, "ruta": ruta, "mensaje": m})

    try:
        ahora = _dt(ctx["ahora"])
        corte_vigente = date.fromisoformat(ctx["fecha_corte_vigente"])
        activos = list(ctx["perfiles_activos"])
    except (KeyError, ValueError, TypeError) as e:
        f("E-01", "contexto", f"contexto de validación inválido: {e}")
        return fallos

    ver = msg.get("version_esquema") if isinstance(msg, dict) else None
    if not isinstance(ver, str) or ver not in VERSIONES_CONOCIDAS:
        f("E-01", "version_esquema", f"versión desconocida: {ver!r}")
        return fallos
    for ruta in _numeros_no_finitos(msg):
        f("E-01", ruta, "número no finito (NaN o infinito)")
    if fallos:
        return fallos
    for e in sorted(Draft202012Validator(_esquema()).iter_errors(msg),
                    key=lambda e: [str(x) for x in e.absolute_path]):
        f("E-01", ".".join(str(x) for x in e.absolute_path) or "(raíz)", e.message[:200])
    if fallos:
        return fallos

    p = msg["payload"]
    cand, man, pre = p["candidato"], p["mandato"], p["presupuesto"]
    cartera, nivel, decision = p["cartera_destino"], p["nivel_analisis"], p["decision_informada"]

    # E-02 destinatario: perfil activo y coincidente con el candidato
    if msg["consumer"] != cand["perfil"]:
        f("E-02", "consumer", "el destinatario no coincide con el perfil del candidato")
    if cand["perfil"] not in activos:
        f("E-02", "payload.candidato.perfil", f"{cand['perfil']} está NO_CONSTRUIDO")

    # E-03 vigencia
    emitido = None
    try:
        emitido, vence = _dt(msg["emitido_en"]), _dt(msg["valid_until"])
        if vence <= emitido:
            f("E-03", "valid_until", "valid_until no es posterior a emitido_en")
        if vence - emitido > VIGENCIA_MAX:
            f("E-03", "valid_until", f"vigencia superior a {VIGENCIA_MAX.days} días")
        if vence <= ahora:
            f("E-03", "valid_until", "el encargo está caducado")
        if emitido > ahora:
            f("E-03", "emitido_en", "emitido en el futuro")
    except ValueError as e:
        f("E-03", "emitido_en", f"fecha-hora inválida: {e}")

    # E-04 fecha de corte: la vigente de K y no demasiado antigua
    try:
        fc = date.fromisoformat(p["fecha_corte"])
        if fc != corte_vigente:
            f("E-04", "payload.fecha_corte", "no es la fecha de corte vigente emitida por K")
        if fc > ahora.date():
            f("E-04", "payload.fecha_corte", "posterior a hoy")
        tope = ctx.get("antiguedad_corte_dias", ANTIGUEDAD_CORTE_DIAS)[cartera]
        if _dias_habiles(fc, ahora.date()) > tope:
            f("E-04", "payload.fecha_corte", f"más antigua de {tope} día(s) hábil(es) para {cartera}")
    except (ValueError, KeyError):
        f("E-04", "payload.fecha_corte", "fecha no interpretable")

    # E-05 horizonte coherente y dentro del rango de la cartera
    h = man["horizonte_dias"]
    lo, hi = ctx.get("horizonte_dias", HORIZONTE_DIAS)[cartera]
    if h["min"] > h["max"]:
        f("E-05", "payload.mandato.horizonte_dias", "min mayor que max")
    elif h["min"] < lo or h["max"] > hi:
        f("E-05", "payload.mandato.horizonte_dias", f"fuera del rango {lo}–{hi} días de {cartera}")

    # E-06 apalancamiento
    if man["apalancamiento_max"] != 0 and ctx.get("apalancamiento_permitido") is not True:
        f("E-06", "payload.mandato.apalancamiento_max", "apalancamiento no habilitado: debe ser 0")

    # E-07 tamaño máximo respecto al tope nominal de la cartera
    tope_t = ctx.get("tamano_max_pct", TAMANO_MAX_PCT)[cartera]
    if man["tamano_max_pct_cartera"] > tope_t:
        f("E-07", "payload.mandato.tamano_max_pct_cartera", f"supera el límite nominal de {tope_t} %")

    # E-08 presupuesto y plazo
    try:
        entrega = _dt(pre["entrega_antes_de"])
        if emitido is not None and entrega <= emitido:
            f("E-08", "payload.presupuesto.entrega_antes_de", "anterior a la emisión")
        if entrega > _dt(msg["valid_until"]):
            f("E-08", "payload.presupuesto.entrega_antes_de", "posterior a la vigencia del encargo")
    except ValueError:
        f("E-08", "payload.presupuesto.entrega_antes_de", "fecha-hora inválida")
    minimo = ctx.get("presupuesto_minimo", {}).get(nivel)
    if minimo and (pre["coste_max_eur"] < minimo["coste_eur"] or pre["tiempo_max_min"] < minimo["tiempo_min"]):
        f("E-08", "payload.presupuesto", f"por debajo del mínimo exigido para {nivel}")
    if "coste_max_eur" in ctx and pre["coste_max_eur"] > ctx["coste_max_eur"]:
        f("E-08", "payload.presupuesto.coste_max_eur", "supera el tope por encargo")

    # E-09 nivel acorde con la decisión que informa
    if decision in NIVEL_MIN_POR_DECISION and NIVEL_ORDEN[nivel] < NIVEL_ORDEN[NIVEL_MIN_POR_DECISION[decision]]:
        f("E-09", "payload.nivel_analisis", f"{decision} exige al menos {NIVEL_MIN_POR_DECISION[decision]}")
    if decision in NIVEL_MAX_POR_DECISION and NIVEL_ORDEN[nivel] > NIVEL_ORDEN[NIVEL_MAX_POR_DECISION[decision]]:
        f("E-09", "payload.nivel_analisis", f"{decision} no justifica más de {NIVEL_MAX_POR_DECISION[decision]}")

    # E-10 el instrumento está permitido por el mandato
    permitidos = {_norm(x) for x in man["instrumentos_permitidos"]}
    if _norm(cand["instrumento"]) not in permitidos:
        f("E-10", "payload.candidato.instrumento", "no figura entre los instrumentos permitidos del mandato")
    if _norm(cand["instrumento"]) in {_norm(x) for x in man.get("exclusiones", [])}:
        f("E-10", "payload.candidato.instrumento", "figura en las exclusiones del mandato")

    # E-11 emisor coherente con la cartera
    if msg["producer"] != "BROKER" and msg["producer"] != PRODUCTOR_POR_CARTERA[cartera]:
        f("E-11", "producer", f"un gestor solo puede encargar para su propia cartera ({cartera})")

    # E-12 trazabilidad: el paquete de B y el sello de corte figuran en data_refs
    for ref, nombre in ((cand["paquete_b_ref"], "paquete_b_ref"), (p["sello_corte_ref"], "sello_corte_ref")):
        if ref not in msg["data_refs"]:
            f("E-12", "data_refs", f"falta {nombre} ({ref}) en data_refs")
    # E-12b: las dos referencias deben ser distintas y estar ambas
    if cand["paquete_b_ref"] == p["sello_corte_ref"]:
        f("E-12", "payload", "paquete_b_ref y sello_corte_ref no pueden ser la misma referencia")

    # E-13 decisiones sobre una posición existente llevan posicion_id; las demás no
    if decision in CON_POSICION and "posicion_id" not in p:
        f("E-13", "payload.posicion_id", f"{decision} exige posicion_id")
    if decision not in CON_POSICION and "posicion_id" in p:
        f("E-13", "payload.posicion_id", f"{decision} no admite posicion_id")

    # E-14 solo se emiten encargos aprobados por la política
    if msg["resultado_politica"]["resultado"] != "APROBADO":
        f("E-14", "resultado_politica.resultado", "el encargo no está APROBADO por la política")

    # E-15 el tiempo máximo de trabajo cabe en la ventana hasta la entrega
    if emitido is not None and "entrega" in locals() and entrega > emitido:
        if (entrega - emitido).total_seconds() / 60 < pre["tiempo_max_min"]:
            f("E-15", "payload.presupuesto", "tiempo_max_min no cabe entre la emisión y la entrega")
    return fallos


def sobre_responde_a_encargo(encargo, sobre, ctx_encargo, ctx_sobre) -> list[dict]:
    """Comprueba que un sobre CT-G-02 responde al encargo CT-G-01 que lo originó.
    Valida ambos antes de cruzarlos (R-00) y nunca lanza excepciones."""
    from validar_sobre import validar
    previos = [{"regla": "R-00", "ruta": "encargo", "mensaje": f"{x['regla']}: {x['mensaje']}"} for x in validar_encargo(encargo, ctx_encargo)]
    previos += [{"regla": "R-00", "ruta": "sobre", "mensaje": f"{x['regla']}: {x['mensaje']}"} for x in validar(sobre, ctx_sobre)]
    if previos:
        return previos
    try:
        return _cruzar(encargo, sobre)
    except (KeyError, TypeError, AttributeError, ValueError, IndexError) as e:
        return [{"regla": "R-00", "ruta": "(interno)", "mensaje": f"{type(e).__name__}: {e}"}]


def _cruzar(encargo: dict, sobre: dict) -> list[dict]:
    fallos: list[dict] = []

    def f(regla, ruta, m):
        fallos.append({"regla": regla, "ruta": ruta, "mensaje": m})

    pe, ps = encargo["payload"], sobre["payload"]
    ident = ps["identificacion"]
    if sobre["correlation_id"] != encargo["correlation_id"]:
        f("R-01", "correlation_id", "el sobre pertenece a otra petición")
    if sobre["expediente_id"] != encargo["expediente_id"]:
        f("R-02", "expediente_id", "el sobre pertenece a otro candidato")
    if ident["perfil"] != pe["candidato"]["perfil"] or sobre["producer"] != encargo["consumer"]:
        f("R-03", "payload.identificacion.perfil", "no lo emite el perfil al que se encargó")
    if ident["fecha_corte"] != pe["fecha_corte"]:
        f("R-04", "payload.identificacion.fecha_corte", "fecha de corte distinta de la del encargo")
    if ident["nivel_analisis"] != pe["nivel_analisis"]:
        f("R-05", "payload.identificacion.nivel_analisis", "nivel distinto del pedido")
    if pe["cartera_destino"] not in ident["cartera_compatible"]:
        f("R-06", "payload.identificacion.cartera_compatible", "no es compatible con la cartera de destino")
    try:
        if _dt(sobre["emitido_en"]) > _dt(pe["presupuesto"]["entrega_antes_de"]):
            f("R-07", "emitido_en", "entregado fuera de plazo")
    except ValueError:
        f("R-07", "emitido_en", "fecha-hora inválida")
    cap = ps.get("capital", {}).get("apalancamiento")
    if cap and isinstance(cap.get("valor"), (int, float)) and cap["valor"] > pe["mandato"]["apalancamiento_max"]:
        f("R-08", "payload.capital.apalancamiento", "supera el apalancamiento máximo del mandato")
    if _norm(ident["instrumento"]) != _norm(pe["candidato"]["instrumento"]):
        f("R-09", "payload.identificacion.instrumento", "instrumento distinto del encargado")
    try:
        if _dt(sobre["emitido_en"]) < _dt(encargo["emitido_en"]):
            f("R-10", "emitido_en", "el sobre es anterior al encargo")
    except ValueError:
        f("R-10", "emitido_en", "fecha-hora inválida")
    return fallos


def main(argv):
    if len(argv) < 3:
        print("uso: validar_encargo.py encargo.json contexto.json")
        return 2
    try:
        msg = cargar_json(Path(argv[1]).read_text(encoding="utf-8"))
        ctx = cargar_json(Path(argv[2]).read_text(encoding="utf-8"))
    except ValueError as e:
        print(f"E-01  (archivo): {e}\nRECHAZADO (1 incumplimiento)")
        return 1
    fallos = validar_encargo(msg, ctx)
    for x in fallos:
        print(f"{x['regla']}  {x['ruta']}: {x['mensaje']}")
    print("VÁLIDO" if not fallos else f"RECHAZADO ({len(fallos)} incumplimientos)")
    return 0 if not fallos else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
