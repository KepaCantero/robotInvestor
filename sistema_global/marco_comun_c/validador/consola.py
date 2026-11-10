"""N mínimo — vista del operador sobre el Orquestador (solo lectura, determinista, sin LLM).

No cambia nada: calcula el panel, la cola de aprobaciones y los avisos pendientes a partir del estado.
Las acciones del operador (autorizar, levantar objeción, acusar aviso) se hacen con los métodos del Orquestador.
Todos los umbrales son [PROPUESTO].

V0.64: el panel acepta un `reloj` y un `diario` opcionales y añade el estado del sistema: kill-switch, autonomía
(carteras degradadas), reloj del sistema y diario, y avisa de la última migración. Sigue siendo solo lectura.
"""
from __future__ import annotations

import copy
from datetime import timedelta, timezone

from k_calidad import ERRORES, estado_sello
from parametros import PARAMETROS
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


def panel(o, ahora, reloj=None, diario=None, lineas_diario_ambar=PARAMETROS["n_lineas_diario_ambar"]):
    """Panel verde/ámbar/rojo con el motivo de cada color. Nunca lanza excepciones: si no puede calcular, ROJO.
    Con `reloj` y `diario` (opcionales) añade sus comprobaciones; sin ellos, las de siempre más kill_switch y autonomia.
    `lineas_diario_ambar` es el tope de líneas del diario sin punto de control a partir del que avisa; por defecto,
    `parametros.PARAMETROS["n_lineas_diario_ambar"]` [PROPUESTO] (V0.67). Un tope que no sea un entero positivo (None,
    texto, bool, NaN o infinito) da ROJO."""
    try:
        return _panel(o, ahora, reloj, diario, lineas_diario_ambar)
    except ERRORES as e:
        return {"nivel": "ROJO", "comprobaciones": [{"que": "panel", "nivel": "ROJO", "motivo": f"no se pudo calcular: {type(e).__name__}"}]}


def _add_seguro(add, que, fn):
    """Las comprobaciones nuevas no pueden salir del panel: lo que falle es ROJO (falla cerrado) y None no añade línea."""
    try:
        r = fn()
    except Exception as ex:   # noqa: BLE001 — un estado ilegible no se pinta de verde
        r = ("ROJO", f"no se pudo leer el estado ({type(ex).__name__})")
    if r is not None:
        add(que, r[0], r[1])


def _kill(o):
    k = o.kill
    if k is None:
        ult = o.rearmes[-1] if o.rearmes else None
        cuando = ult.get("ahora") if isinstance(ult, dict) else None
        return "VERDE", "sin kill-switch activo" + (f"; último rearme {cuando}" if cuando else "")
    if isinstance(k, dict):
        return "ROJO", f"kill-switch activo ({k.get('actor', '?')}): {k.get('motivo', '?')} desde {k.get('ahora', '?')}"
    return "ROJO", f"kill-switch activo con un registro ilegible: {k!r}"


def _autonomia(o):
    if not isinstance(o.degradadas, dict):   # V0.67 (QA de T-79, H-03): None, [] o "" no son «autonomía plena»
        return "ROJO", f"el registro de carteras degradadas es ilegible ({type(o.degradadas).__name__}): revisa el estado"
    if not o.degradadas:
        return "VERDE", "autonomía plena: ninguna cartera degradada"
    partes = []
    for c in sorted(o.degradadas):
        d = o.degradadas[c]
        if isinstance(d, dict):
            partes.append(f"{c} en {o.nivel(c)} ({d.get('motivo', '?')} desde {d.get('ahora', '?')})")
        else:
            partes.append(f"{c} en {o.nivel(c)} (registro ilegible: {d!r})")
    return "AMBAR", f"autonomía reducida: {'; '.join(partes)}"


def _reloj(reloj):
    b = reloj.bloqueo
    if b is not None:
        if isinstance(b, dict):
            return "ROJO", f"el reloj está bloqueado ({b.get('codigo', '?')}: {b.get('motivo', '?')}): hay que rearmarlo"
        return "ROJO", f"el reloj está bloqueado con un registro ilegible: {b!r}"
    e = reloj.estado()
    if not isinstance(e, dict):
        return "ROJO", "el reloj no da su estado"
    if not e.get("contrastado", False):
        return "AMBAR", "el reloj aún no se ha contrastado (o lo rearmaron): contrástalo con una referencia externa"
    s = e.get("segundos_desde_contraste")
    if s is None:
        return "AMBAR", "no se puede confirmar el contraste del reloj: contrástalo otra vez"
    if not s <= reloj.max_sin_contraste_s:   # T-85: un tope NaN o ilegible no deja pasar a VERDE
        return "AMBAR", f"hace {s:.0f} s que no se contrasta el reloj (tope {reloj.max_sin_contraste_s:.0f} s): contrástalo otra vez"
    return "VERDE", f"reloj contrastado hace {s:.0f} s"


def _diario(diario, tope):
    """T-72 (V0.69): lee `Diario.estado_diario()`, la foto pública de solo lectura, y ya no los privados `_roto` y `_n`. Un diario
    que no está al día con el Orquestador (cambió por fuera, o su fichero lo reescribió otro proceso) es ROJO: la operación
    siguiente daría DI-06. V0.67: el tope se valida antes (un NaN, un infinito o un bool daban VERDE: fallaba abierto)."""
    if isinstance(tope, bool) or not isinstance(tope, int) or tope < 1:
        return "ROJO", f"el tope de líneas del diario no es un entero positivo ({tope!r}): revisa la configuración"
    f = getattr(diario, "estado_diario", None)
    e = f() if callable(f) else None
    if not isinstance(e, dict):
        return "ROJO", f"el diario no da su estado ({type(diario).__name__})"
    b = e.get("bloqueo")
    if b is not None:
        det = f"{b.get('codigo', '?')}: {b.get('motivo', '?')}" if isinstance(b, dict) else repr(b)
        return "ROJO", f"el diario está bloqueado ({det}): reábrelo y sigue desde el último punto de control"
    if e.get("sincronizado") is not True:
        return "ROJO", (f"el diario no está al día con el Orquestador ({e.get('motivo_desincronizado') or '?'}): la operación siguiente "
                        "dará DI-06; reábrelo para volver al estado anotado")
    n = e.get("lineas")
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        return "ROJO", f"el diario no da su número de líneas ({n!r})"
    if n > tope:
        return "AMBAR", f"el diario lleva {n} líneas desde el último punto de control (tope {tope}): hazle un punto"
    return "VERDE", f"diario operativo ({n} línea(s) desde el último punto de control)"


def _migracion(o):
    """La línea informativa de la última migración, o None si la última entrada del registro de límites no es una MIGRACION."""
    try:
        ent = o.limites["entradas"]
        ult = ent[-1] if ent else None
    except Exception:   # noqa: BLE001 — unos límites ilegibles ya los ve «integridad» (ROJO); aquí no hay línea
        return None
    if not isinstance(ult, dict) or ult.get("tipo") != "MIGRACION":
        return None
    try:
        cuando = o.limites["historial"][-1]["ahora"]   # pareada con la entrada (lo exige _limites_ok)
    except Exception:   # noqa: BLE001
        cuando = None
    ids = ult.get("migraciones")
    if (not isinstance(cuando, str) or not cuando or not isinstance(ids, list) or not ids
            or not all(isinstance(i, str) and i for i in ids)):
        return "ROJO", "hay una migración anotada pero el registro no la deja leer: revisa el estado"
    return "VERDE", f"migrado a este código el {cuando} ({', '.join(ids)})"


def _panel(o, ahora, reloj=None, diario=None, lineas_diario_ambar=PARAMETROS["n_lineas_diario_ambar"]):
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
    # estado del sistema (V0.64): kill-switch y autonomía siempre; reloj, diario y migración cuando proceda
    _add_seguro(add, "kill_switch", lambda: _kill(o))
    _add_seguro(add, "autonomia", lambda: _autonomia(o))
    if reloj is not None:
        _add_seguro(add, "reloj", lambda: _reloj(reloj))
    if diario is not None:
        _add_seguro(add, "diario", lambda: _diario(diario, lineas_diario_ambar))
    _add_seguro(add, "migracion", lambda: _migracion(o))
    return {"nivel": _peor([x["nivel"] for x in c]), "comprobaciones": c}
