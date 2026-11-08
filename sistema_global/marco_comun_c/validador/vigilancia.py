"""H — vigilancia de posiciones (código de referencia V0.1).

H mira cada posición abierta contra los datos de mercado y contra el intermediario, y cuando una condición de salida
declarada de antemano se cumple, pide a G que cierre. Determinista, sin LLM. H no decide nada nuevo: solo aplica
las condiciones que la propuesta ya fijó. Ante un dato ausente o viejo no cierra: avisa.
Reglas: H-01 stop ejecutado por el intermediario; H-02 condición de salida cumplida; H-03 dato ausente o viejo;
H-04 cierre pendiente (CERRANDO) que se reintenta; H-05 stop cumplido sin que el intermediario lo ejecutara;
H-06 métrica no soportada; H-07 diferencias de conciliación; H-08 reducción en curso (REDUCIENDO) que se retoma;
H-09 instante sospechoso (no se hace nada); H-10 salida preparada para el operador (L0/L1); H-11 orden de entrada viva;
H-12 reducción parcial por una condición OBJETIVO que declara su fracción (una sola vez; si ya no cabe, se informa y se sigue);
H-13 posición con el estado de control alterado (no se envía nada por ella);
H-14 llegó la fecha de revisión de la tesis: la posición pasa a EN_REVISION y la confirma (con fecha nueva) o la cierra el operador;
H-15 se cumplió la condición de reapertura de un expediente en observación (aviso O-31; se puede re-encargar);
H-16 se cumple un escenario de fallo del Contradictor o una invalidez por una métrica que no es el precio: pide revisión y propone,
nunca vende (T-49); H-17 la pérdida no realizada pasa el umbral configurado (y otra vez por cada múltiplo): pide revisión;
H-18 falta el dato de una señal (o llega sin unidad, en otra unidad o no numérico): no se evalúa;
H-19 fallo inesperado al vigilar una posición: se informa (degrada su cartera) y se sigue con las demás.
"""
from __future__ import annotations

import math
from datetime import date, timezone

import math as _m

from orquestador import NIVELES
from ejecucion_g import _aviso, _instante, _stop_retirado_que_cerro, cerrar, conciliar, cotizar, reducir, revisar_entrada
from orquestador import OPERADORES
from validar_sobre import _dt

from parametros import PARAMETROS as _P   # noqa: E402
MAX_EDAD_MIN = _P["h_max_edad_dato_min"]   # [PROPUESTO]
SALTO_MAX_H = _P["h_salto_max_horas"]    # [PROPUESTO] más allá, el instante recibido se considera sospechoso


def _valor_cumplido(c, pm):
    """El valor con el que se declara cumplida la condición de un stop que el intermediario ya ejecutó: el precio real si la
    cumple y, si no (relleno mejor, redondeo, dato ausente), el umbral mismo o el valor más próximo que la cumple."""
    from orquestador import OPERADORES as OP
    u = c["umbral"]
    for v in (pm, u, _m.nextafter(u, -_m.inf), _m.nextafter(u, _m.inf)):
        if _num(v) and OP[c["operador"]](v, u):
            return v
    return u


def _num(x):
    try:   # un entero enorme desborda math.isfinite (revisión T-49, R-01)
        return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)
    except OverflowError:
        return False


def _dato_senal(x, d, metricas):
    """T-49: el valor con el que se evalúa una señal, o (None, motivo). El precio sale del dato fresco de la pasada; otra métrica
    llega como {"valor", "unidad"} y su unidad debe ser la de la señal (revisión, R-03)."""
    if x["metrica"] == "precio":
        return d["precio"], None
    m = metricas.get(x["metrica"])
    if m is None:
        return None, f"sin dato de {x['metrica']}"
    if not (isinstance(m, dict) and set(m) == {"valor", "unidad"}):
        return None, f"el dato de {x['metrica']} debe ser {{valor, unidad}}"
    if m["unidad"] != x["unidad"]:
        return None, f"el dato de {x['metrica']} llega en {str(m['unidad'])[:12]!r} y la señal está en {x['unidad']!r}"
    if not _num(m["valor"]):
        return None, f"el dato de {x['metrica']} no es numérico"
    return m["valor"], None


def _dato_fresco(d, ahora, max_edad_min):
    try:
        if not (isinstance(d, dict) and _num(d.get("precio")) and d["precio"] > 0):
            return False
        edad = (_dt(ahora) - _dt(d["hora"])).total_seconds() / 60
        return 0 <= edad <= max_edad_min
    except Exception:   # noqa: BLE001
        return False


def _senales(o, pid, d, ahora, acciones, no_eval):
    """T-49: escenarios de fallo, invalidez por otras métricas y pérdida no realizada. Solo piden revisión: nada va al
    intermediario. Se evalúan con el dato fresco de la pasada (d) sobre una posición abierta o en revisión."""
    from orquestador import nivel_perdida
    p = o.posiciones[pid]
    if p["estado"] not in ("ABIERTA", "EN_REVISION") or not o.posicion_integra(pid):
        return
    metricas = d.get("metricas") if isinstance(d.get("metricas"), dict) else {}
    for x in p.get("senales") or []:
        if x["clave"] in p["senales_disparadas"]:
            continue
        v, motivo = _dato_senal(x, d, metricas)
        if motivo:
            no_eval.append({"posicion": pid, "senal": x["clave"], "regla": "H-18", "motivo": motivo})
            continue
        if OPERADORES[x["operador"]](v, x["umbral"]):
            r = o.registrar_senal(pid, "SENAL", x["clave"], v, "H", _instante(o, ahora))
            acciones.append({"posicion": pid, "regla": "H-16", "senal": x["clave"], "ok": r["ok"], "codigo": r["codigo"]})
    nv = nivel_perdida(p, d.get("precio"), o.cfg["alerta_perdida_pct"])   # la misma cuenta que el Orquestador (R-07)
    if nv is None:
        no_eval.append({"posicion": pid, "senal": "PERDIDA", "regla": "H-18", "motivo": "no se puede calcular la pérdida"})
    elif nv[1] > p["perdida_alertada"]:
        r = o.registrar_senal(pid, "PERDIDA", None, d["precio"], "H", _instante(o, ahora))
        acciones.append({"posicion": pid, "regla": "H-17", "perdida_pct": round(nv[0], 4), "nivel": nv[1], "ok": r["ok"], "codigo": r["codigo"]})


def vigilar(o, broker, datos, ahora, max_edad_min=MAX_EDAD_MIN):
    """datos: {instrumento: {"precio": número, "hora": ISO con zona, "metricas": {métrica: {"valor": número, "unidad": texto}}}}
    ("metricas" es opcional: solo lo usan las señales de T-49). Devuelve las acciones y avisos de esta pasada.
    max_edad_min solo puede ser más estricto que el parámetro (T-25): otro valor se ignora."""
    if not (_num(max_edad_min) and 0 < max_edad_min <= MAX_EDAD_MIN):
        max_edad_min = MAX_EDAD_MIN
    try:
        if o.ultimo_ahora and (_dt(ahora) - _dt(o.ultimo_ahora)).total_seconds() > SALTO_MAX_H * 3600:
            return {"acciones": [{"posicion": None, "regla": "H-09", "ok": False, "codigo": "H-09"}], "no_evaluadas": [], "conciliacion_ok": False,
                    "motivo": "el instante recibido salta demasiado respecto al último que vio el Orquestador; no se hace nada"}
        ahora = _instante(o, ahora)
    except Exception:   # noqa: BLE001
        return {"acciones": [{"posicion": None, "regla": "H-09", "ok": False, "codigo": "H-09"}], "no_evaluadas": [], "conciliacion_ok": False,
                "motivo": "instante ilegible"}
    acciones, no_eval, hechos = [], [], set()
    # Órdenes de entrada vivas: si se ejecutaron se protegen y se reportan; si vencieron se cancelan (H-11)
    for eid in sorted(o.expedientes):
        x = o.expedientes[eid]
        if x["estado"] == "AUTORIZADA" and (x.get("orden_entrada") or {}).get("estado") in ("ENVIADA", "PARCIAL", "EJECUTADA"):
            r = revisar_entrada(o, eid, broker, ahora)
            acciones.append({"expediente": eid, "posicion": None, "regla": "H-11", "ok": r["ok"], "codigo": r["codigo"]})
    # Primera pasada: hechos consumados (cierres pendientes y stops que el intermediario ya ejecutó).
    for pid in sorted(o.posiciones):
        p = o.posiciones[pid]
        if p["estado"] == "CERRADA":
            continue
        if not o.posicion_integra(pid):   # fail-closed: con un estado alterado no se envía nada por esta posición
            reg = _aviso(o, [{"tipo": "INTEGRIDAD", "ref": pid, "detalle": "el estado de control de la posición no cuadra con su historial"}], ahora)
            acciones.append({"posicion": pid, "regla": "H-13", "ok": False, "codigo": "H-13", "aviso_registrado": reg})
            hechos.add(pid)
            continue
        if p["estado"] == "CERRANDO":
            r = cerrar(o, pid, broker, ahora)
            acciones.append({"posicion": pid, "regla": "H-04", "ok": r["ok"], "codigo": r["codigo"]})
            hechos.add(pid)
            continue
        if p["estado"] == "REDUCIENDO":   # se retoma; si un stop la cerró entera, G la termina como cierre
            r = reducir(o, pid, broker, ahora)
            acciones.append({"posicion": pid, "regla": "H-08", "ok": r["ok"], "codigo": r["codigo"]})
            if r["ok"] or o.posiciones[pid]["estado"] != "REDUCIENDO":
                hechos.add(pid)
            continue   # si sigue REDUCIENDO, la segunda pasada vigila sus condiciones de cierre
        try:
            ejec = [c for x in p["protecciones"] if (c := broker.consultar(x)) and c["estado"] in ("EJECUTADA", "PARCIAL")]
            if not ejec:   # V0.53 (revisión de GLM g01; integración h02): un stop retirado por una parcial a mano que aún saltó y
                # cerró él solo lo que quedaba (ejecutado por esa cantidad, instrumento a cero) se confirma como un stop propio
                ret = _stop_retirado_que_cerro(broker, p)
                ejec = [broker.consultar(ret)] if ret else []
        except Exception:   # noqa: BLE001
            ejec = []
        if ejec:   # el intermediario ya ejecutó el stop: solo falta confirmar el cierre
            stop = next(c for c in o.posiciones[pid]["condiciones_salida"]["condiciones"] if c["tipo"] == "STOP")
            cond = {"id": stop["id"], "valor_observado": _valor_cumplido(stop, ejec[0]["precio_medio"]), "stop_ejecutado_orden_id": ejec[0]["orden_id"]}
            r = cerrar(o, pid, broker, ahora, condicion=cond)
            acciones.append({"posicion": pid, "regla": "H-01", "ok": r["ok"], "codigo": r["codigo"]})
            hechos.add(pid)
    # Conciliar antes de cualquier decisión: una diferencia degrada la cartera y el cierre automático ya no se hace
    conc = conciliar(o, broker, ahora)

    def _una(pid):
        p = o.posiciones[pid]
        if p["estado"] == "CERRADA" or pid in hechos:
            return
        if p["estado"] == "ABIERTA" and p.get("fecha_revision") and date.fromisoformat(p["fecha_revision"]) <= _dt(ahora).astimezone(timezone.utc).date():
            r = o.posicion_transicion(pid, "EN_REVISION", "H", _instante(o, ahora), motivo=f"llegó la fecha de revisión {p['fecha_revision']}")
            if r["ok"]:
                o.proponer_sobre_posicion(pid, f"REVISIÓN: llegó la fecha de revisión {p['fecha_revision']}; confirme la tesis con una fecha nueva o cierre",
                                          "H", _instante(o, ahora))
            acciones.append({"posicion": pid, "regla": "H-14", "ok": r["ok"], "codigo": r["codigo"]})   # sigue vigilando sus condiciones
        d = datos.get(p["instrumento"]) if isinstance(datos, dict) else None
        if not _dato_fresco(d, ahora, max_edad_min):
            o.degradar(p["cartera"], f"sin precio fresco de {p['instrumento']}", "H", _instante(o, ahora))
            reg = _aviso(o, [{"tipo": "DATO_VIEJO", "ref": pid, "detalle": f"sin precio fresco de {p['instrumento']}; no se vigila la posición"}], ahora)
            acciones.append({"posicion": pid, "regla": "H-03", "ok": False, "codigo": "H-03", "aviso_registrado": reg})
            return
        n_acc = len(acciones)
        for c in p["condiciones_salida"]["condiciones"]:
            if c["metrica"] != "precio":
                if c["tipo"] != "INVALIDEZ":   # una invalidez con otra métrica es una señal (H-16): pide revisión, no vende
                    no_eval.append({"posicion": pid, "condicion": c["id"], "regla": "H-06"})
                continue
            if c["id"] in p.get("condiciones_consumidas", []):   # una toma parcial ya hecha no se repite
                continue
            parcial = c.get("fraccion") is not None
            if parcial and (p["estado"] == "REDUCIENDO" or c["fraccion"] * p["cantidad_inicial"] >= p["cantidad"] - 1e-6):
                if p["estado"] != "REDUCIENDO":   # la toma parcial ya no cabe (se redujo antes): no bloquea las demás condiciones
                    no_eval.append({"posicion": pid, "condicion": c["id"], "regla": "H-12", "motivo": "la toma parcial ya no cabe en lo que queda"})
                continue
            if OPERADORES[c["operador"]](d["precio"], c["umbral"]):
                if parcial:   # T-43: antes de preparar o hacer una toma parcial, si no cabe se propone al operador una sola vez
                    cotizar(o, broker, p["instrumento"], ahora)
                    v = o.cantidad_reduccion(pid, _instante(o, ahora), condicion_id=c["id"])
                    if not v["ok"]:
                        pref = f"REDUCCIÓN NO VIABLE: {c['id']} "   # revisión de V0.52, hallazgo 1: una vez, aunque cambie el motivo
                        if not v.get("transitorio") and not any(x["texto"].startswith(pref) for x in p["propuestas"]):   # sin precio: otra pasada
                            o.proponer_sobre_posicion(pid, f"{pref}(fracción {c['fraccion']}) cumplida, pero {v['motivo']}; decida el operador", "H", _instante(o, ahora))
                        no_eval.append({"posicion": pid, "condicion": c["id"], "regla": "H-12", "motivo": v["motivo"]})
                        continue
                if NIVELES[o.nivel(p["cartera"])] < 2:   # L0/L1: H prepara la salida y la confirma el operador
                    txt = (f"REDUCCIÓN PREPARADA: {c['id']} ({c['tipo']}, fracción {c['fraccion']}, {v['cantidad']} con el paso) cumplida; confirme la reducción" if parcial
                           else f"CIERRE PREPARADO: {c['id']} ({c['tipo']}) cumplida; confirme el cierre")
                    if not any(x["texto"] == txt for x in p["propuestas"]):
                        o.proponer_sobre_posicion(pid, txt, "H", _instante(o, ahora))
                    acciones.append({"posicion": pid, "regla": "H-10", "condicion": c["id"], "ok": False, "codigo": "H-10"})
                    break
                if parcial:
                    r = reducir(o, pid, broker, ahora, condicion={"id": c["id"], "valor_observado": d["precio"]})
                    acciones.append({"posicion": pid, "regla": "H-12", "condicion": c["id"], "ok": r["ok"], "codigo": r["codigo"]})
                    break
                r = cerrar(o, pid, broker, ahora, condicion={"id": c["id"], "valor_observado": d["precio"]})
                acciones.append({"posicion": pid, "regla": "H-05" if c["tipo"] == "STOP" else "H-02", "condicion": c["id"],
                                 "ok": r["ok"], "codigo": r["codigo"]})
                break
        if not any(x.get("posicion") == pid and x["regla"] in ("H-02", "H-05", "H-10", "H-12") for x in acciones[n_acc:]):
            _senales(o, pid, d, ahora, acciones, no_eval)   # si esta pasada ya actuó por una salida declarada, no se añade ruido
    for pid in sorted(o.posiciones):   # un fallo inesperado en una posición se informa y no deja sin vigilar a las demás (R-01)
        try:
            _una(pid)
        except Exception as ex:   # noqa: BLE001
            reg = _aviso(o, [{"tipo": "VIGILANCIA_FALLIDA", "ref": pid, "detalle": f"{type(ex).__name__}: no se vigiló la posición en esta pasada"}], ahora)
            acciones.append({"posicion": pid, "regla": "H-19", "ok": False, "codigo": "H-19", "aviso_registrado": reg})
    rr = o.revisar_reaperturas(datos if isinstance(datos, dict) else {}, "H", ahora, max_edad_min)   # T-46: con la misma frescura que H
    for eid in rr.get("cumplidas", []):
        acciones.append({"expediente": eid, "posicion": None, "regla": "H-15", "ok": True, "codigo": "H-15"})
    if not conc["ok"]:
        acciones.append({"posicion": None, "regla": "H-07", "ok": False, "codigo": "H-07", "diferencias": [d["tipo"] for d in conc["diferencias"]]})
    return {"acciones": acciones, "no_evaluadas": no_eval, "conciliacion_ok": conc["ok"]}
