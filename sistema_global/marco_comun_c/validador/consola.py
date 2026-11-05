"""N mínimo — vista del operador sobre el Orquestador (solo lectura, determinista, sin LLM).

No cambia nada: calcula el panel, la cola de aprobaciones y los avisos pendientes a partir del estado.
Las acciones del operador (autorizar, levantar objeción, acusar aviso) se hacen con los métodos del Orquestador.
Todos los umbrales son [PROPUESTO].
"""
from __future__ import annotations

import copy
from datetime import timedelta, timezone

from k_calidad import ERRORES, estado_sello
from validar_sobre import _dt

HORAS_AMBAR_PROPUESTA = 6      # una propuesta que vence en menos de estas horas pasa a ámbar
FRACCION_AMBAR_DIA = 0.8       # el gasto diario pasa a ámbar al llegar a esta fracción del tope
ORDEN = {"VERDE": 0, "AMBAR": 1, "ROJO": 2}


def _peor(niveles):
    return max(niveles, key=ORDEN.__getitem__, default="VERDE")


def _tiempo(o, ahora):
    """Nunca se calcula con un reloj anterior al último que vio el Orquestador."""
    a = _dt(ahora)
    return max(a, _dt(o.ultimo_ahora)) if o.ultimo_ahora else a


def cola_aprobaciones(o, ahora):
    """Lo que espera una decisión del operador, ordenado por urgencia (lo que vence antes, primero).
    Nunca lanza excepciones: si no puede calcularla, devuelve una entrada ERROR vencida."""
    try:
        return _cola(o, ahora)
    except ERRORES:
        return [{"tipo": "ERROR", "ref": None, "vence": None, "vencida": True}]


def _cola(o, ahora):
    a = _tiempo(o, ahora)
    items = []
    for eid, e in o.expedientes.items():
        if e["estado"] == "PROPUESTA":
            lim = min(_dt(e["propuesta"]["entrada"]["ventana_hasta"]), _dt(e["sobre"]["valid_until"]))
            items.append({"tipo": "AUTORIZAR", "ref": eid, "vence": lim.isoformat(), "vencida": a > lim})
        elif e["retenido"] is not None and e["estado"] == "EN_ANALISIS":
            lim = _dt(e["retenido"]["sobre"]["valid_until"])
            items.append({"tipo": "OBJECION_CRITICA", "ref": eid, "vence": lim.isoformat(), "vencida": a > lim})
        elif e["estado"] == "EN_ANALISIS" and e["retenido"] is None:
            en = o.encargos.get(e["encargo_actual"])
            if en is not None and en["estado"] in ("INCOMPLETO", "CADUCADO", "ANULADO"):
                items.append({"tipo": "REEMITIR_O_DESCARTAR", "ref": eid, "vence": None, "vencida": False})
    for pid, p in o.posiciones.items():
        if p["estado"] == "EN_REVISION":
            items.append({"tipo": "REVISAR_POSICION", "ref": pid, "vence": None, "vencida": False})
    return sorted(items, key=lambda x: (x["vence"] is None, _dt(x["vence"]) if x["vence"] else a, x["ref"]))


def avisos_pendientes(o):
    """Copias: la consola no puede modificar los avisos del Orquestador."""
    return sorted((copy.deepcopy(x) for x in o.avisos if x["acuse"] is None), key=lambda x: (x["prioridad"] != "ALTA", x["id"]))


def panel(o, ahora):
    """Panel verde/ámbar/rojo con el motivo de cada color. Nunca lanza excepciones: si no puede calcular, ROJO."""
    try:
        return _panel(o, ahora)
    except ERRORES as e:
        return {"nivel": "ROJO", "comprobaciones": [{"que": "panel", "nivel": "ROJO", "motivo": f"no se pudo calcular: {type(e).__name__}"}]}


def _panel(o, ahora):
    a = _tiempo(o, ahora)
    c = []

    def add(que, nivel, motivo):
        c.append({"que": que, "nivel": nivel, "motivo": motivo})

    # integridad de los historiales
    malos = o.integridad()
    add("integridad", "ROJO" if malos else "VERDE", f"historial o propuesta alterados en {malos}" if malos else "historiales íntegros")
    # datos de K
    vig = [s for s in o.sellos.values() if s["estado"] == "VIGENTE"]
    caducados = [s["sello_id"] for s in vig
                 if estado_sello(s, str(a.astimezone(timezone.utc).date()), s["cartera"], o.cal_def) == "CADUCADO"]
    if not vig:
        add("datos", "ROJO", "no hay ningún sello de K vigente")
    elif len(caducados) == len(vig):
        add("datos", "ROJO", f"todos los sellos vigentes ya caducaron por antigüedad: {sorted(caducados)}")
    elif caducados:
        add("datos", "AMBAR", f"sellos que ya caducaron por antigüedad: {sorted(caducados)}")
    else:
        add("datos", "VERDE", "sellos de K vigentes")
    # presupuesto del día
    fecha = str(a.astimezone(timezone.utc).date())
    gc, gt, rc, rt = o._tope_dia(fecha)
    cmax, tmax = o.cfg["dia_coste_max_eur"], o.cfg["dia_tiempo_max_min"]
    if gc >= cmax or gt >= tmax:
        add("presupuesto", "ROJO", "presupuesto del día agotado")
    elif gc + rc >= FRACCION_AMBAR_DIA * cmax or gt + rt >= FRACCION_AMBAR_DIA * tmax:
        add("presupuesto", "AMBAR", "el gasto más las reservas supera el 80 % del tope del día")
    else:
        add("presupuesto", "VERDE", "presupuesto del día con margen")
    # avisos sin acusar
    pend = avisos_pendientes(o)
    altas = [x["id"] for x in pend if x["prioridad"] == "ALTA"]
    add("avisos", "ROJO" if altas else ("AMBAR" if pend else "VERDE"),
        f"avisos de prioridad alta sin acusar: {altas}" if altas else (f"{len(pend)} aviso(s) sin acusar" if pend else "sin avisos pendientes"))
    # decisiones que esperan al operador
    cola = cola_aprobaciones(o, ahora)
    criticas = [x["ref"] for x in cola if x["tipo"] == "OBJECION_CRITICA"]
    urgentes = [x["ref"] for x in cola if x["vence"] and (x["vencida"] or _dt(x["vence"]) - a < timedelta(hours=HORAS_AMBAR_PROPUESTA))]
    sin_plazo = [x["ref"] for x in cola if x["tipo"] in ("REVISAR_POSICION", "REEMITIR_O_DESCARTAR", "ERROR")]
    if criticas or any(x["tipo"] == "ERROR" for x in cola):
        add("decisiones", "ROJO", f"objeción crítica del Contradictor o error de cálculo: {sorted(criticas) or 'cola no calculable'}")
    elif urgentes:
        add("decisiones", "AMBAR", f"decisiones que vencen pronto o ya vencieron: {sorted(urgentes)}")
    elif sin_plazo:
        add("decisiones", "AMBAR", f"esperan al operador, sin plazo: {sorted(sin_plazo)}")
    else:
        add("decisiones", "VERDE", f"{len(cola)} decisión(es) pendiente(s), sin urgencia" if cola else "sin decisiones pendientes")
    return {"nivel": _peor([x["nivel"] for x in c]), "comprobaciones": c}
