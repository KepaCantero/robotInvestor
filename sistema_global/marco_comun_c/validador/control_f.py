"""F — control de riesgo previo a la autorización (CT-G-08 0.3.0 con la envoltura común, reglas de control F-01..F-23 y de verificación CF-01..CF-09).

Determinista, sin LLM, sin red. F calcula su propia exposición a partir de la cartera que recibe; no consume M.
`controlar` aplica las reglas y devuelve el informe; `validar_informe_f` lo verifica sin fiarse de él: lo
vuelve a calcular con las mismas entradas. Todos los límites son valores de partida [PROPUESTO].

T-22 (V0.36): los controles de la §8 que faltaban. F recibe, además de la solicitud, la cartera y la política, un `contexto`
que construye el Orquestador con sus propios registros (no lo escribe quien propone; CF-09 exige que sea el suyo):
mandato efectivo, fecha de revisión, exclusiones duras y evidencia del sobre, eventos de K en la ventana, nivel de autonomía
y kill-switch, actividad reciente (importe autorizado hoy, autorizaciones en la última hora, pérdida de la semana) y la última
cotización que G tomó del intermediario. Reglas nuevas: F-13 a F-15 importes máximos en euros por orden, por día y por activo
(REDUCE); F-16 pérdida máxima del día y de la semana en euros; F-17 órdenes por hora; F-18 mandato; F-19 exclusiones duras;
F-20 evidencia mínima; F-21 ventanas de eventos y fin de semana; F-22 autonomía; F-23 precio del intermediario (frescura y
deriva respecto al límite). Sin contexto (uso interno de E para dimensionar) solo se aplican las reglas que no dependen de él;
un informe CT-G-08 siempre lo lleva.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from datetime import timedelta, timezone

from datetime import date

from mandatos import norm
from validar_sobre import _dt

VERSION_REGLAS = "F-0.3.0"   # 0.2.0: conversión a euros con los tipos de cambio de la cartera (T-10). 0.3.0: controles de la §8 (T-22)
POLITICA_DEFECTO = {"riesgo_max_pct": 1.0, "tamano_max_pct": 10.0, "exposicion_max_pct": 100.0,
                    "concentracion_max_pct": 20.0, "perdida_dia_max_pct": 2.0, "max_posiciones": 10,
                    "apalancamiento_max": 1.0, "frescura_max_min": 60.0, "valor_min_eur": 100.0,
                    "vigencia_max_horas": 24.0,
                    # T-22: límites nominales en euros y controles previos de la §8 [PROPUESTO, D-11 y D-31]
                    "importe_max_orden_eur": 20000.0, "importe_max_dia_eur": 50000.0, "importe_max_activo_eur": 30000.0,
                    "perdida_dia_max_eur": 2500.0, "perdida_semana_max_eur": 5000.0, "ordenes_max_hora": 10,
                    "evidencia_verificada_min": 0.05, "corte_max_dias": 3, "ventana_eventos_dias": 1,
                    "viernes_corte_utc_h": 20, "deriva_precio_max_pct": 2.0, "precio_frescura_max_min": 15.0}
CLAVES_POLITICA = set(POLITICA_DEFECTO)
ENTEROS_POLITICA = ("max_posiciones", "ordenes_max_hora", "corte_max_dias", "ventana_eventos_dias", "viernes_corte_utc_h")
TIPOS_EVENTO_RESTRINGIDOS = ("BANCO_CENTRAL", "RESULTADOS")   # §8.7 [PROPUESTO]: no se abre en su ventana
CLAVES_CONTEXTO = {"mandato", "fecha_revision", "exclusiones_duras", "evidencia", "eventos", "autonomia", "actividad", "precio_intermediario"}
CLAVES_MANDATO = {"version", "instrumentos_permitidos", "exclusiones", "apalancamiento_max", "horizonte_max_dias"}
CARTERAS = {"TRADING", "TACTICA", "LARGO_PLAZO"}
ID = re.compile(r"^[A-Za-z0-9._:/-]{1,64}\Z")
FH = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})\Z")
ERRORES = (KeyError, TypeError, AttributeError, ValueError, IndexError, OverflowError, ZeroDivisionError, RecursionError, MemoryError)
ORDEN_SOLICITUD = {"instrumento", "activo_base", "divisa_cotizacion", "direccion", "cantidad", "precio_entrada", "stop_precio", "apalancamiento", "cartera"}
DIVISA = re.compile(r"^[A-Z]{3}\Z")


DIVISAS_ISO = {"EUR", "USD", "GBP", "JPY", "CHF", "AUD", "CAD", "NZD", "SEK", "NOK", "DKK", "PLN", "CZK", "HUF", "TRY", "MXN",
               "ZAR", "SGD", "HKD", "CNH", "CNY", "KRW", "INR", "BRL"}


def par_divisas(instrumento):
    """(base, cotizada) si el instrumento es un par de dos divisas ISO conocidas (admite «EUR/USD»); si no, None."""
    if not isinstance(instrumento, str):
        return None
    ins = re.sub(r"[/\-_. ]", "", instrumento.upper())
    if re.fullmatch(r"[A-Z]{6}", ins) and ins[:3] in DIVISAS_ISO and ins[3:] in DIVISAS_ISO and ins[:3] != ins[3:]:
        return ins[:3], ins[3:]
    return None


def divisa_cotizada(instrumento, tabla=None):
    """Divisa en la que cotiza el precio del instrumento: la de la tabla de configuración o, en un par de divisas ISO, la
    segunda. None si no se sabe (no se propone ni se valora: F veta)."""
    if isinstance(tabla, dict) and instrumento in tabla:
        return tabla[instrumento]
    p = par_divisas(instrumento)
    return p[1] if p else None


def tipo_cambio(divisa, cart):
    """Euros por una unidad de `divisa`, según la cartera que aporta G. None si falta."""
    if divisa == "EUR":
        return 1.0
    t = cart.get("tipos_cambio_eur", {}).get(divisa) if isinstance(cart, dict) and isinstance(cart.get("tipos_cambio_eur"), dict) else None
    return t if _num(t, 0, True) else None


def hash_contenido(x) -> str:
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _num(x, minimo=None, estricto=False):
    if not isinstance(x, (int, float)) or isinstance(x, bool) or not math.isfinite(x):
        return False
    return minimo is None or (x > minimo if estricto else x >= minimo)


def politica_valida(p) -> bool:
    return (isinstance(p, dict) and set(p) == CLAVES_POLITICA
            and all(_num(p[k], 0, True) for k in CLAVES_POLITICA)
            and all(isinstance(p[k], int) and not isinstance(p[k], bool) for k in ENTEROS_POLITICA)
            and p["apalancamiento_max"] >= 1
            and p["evidencia_verificada_min"] <= 1 and p["viernes_corte_utc_h"] <= 24 and p["ventana_eventos_dias"] <= 30
            and p["importe_max_orden_eur"] <= p["importe_max_dia_eur"] and p["perdida_dia_max_eur"] <= p["perdida_semana_max_eur"]
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
    if not (isinstance(sol["divisa_cotizacion"], str) and DIVISA.match(sol["divisa_cotizacion"])):
        return "divisa de cotización inválida"
    if not (isinstance(cart, dict) and set(cart) == {"fecha_hora", "capital_eur", "perdida_dia_eur", "posiciones", "tipos_cambio_eur"}
            and isinstance(cart["tipos_cambio_eur"], dict)
            and all(isinstance(k, str) and DIVISA.match(k) and _num(v, 0, True) for k, v in cart["tipos_cambio_eur"].items())
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


FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}\Z")
NIVELES = ("L0", "L1", "L2", "L3")   # V0.50 (T-18): L3, autónomo en horario supervisado


def _txt_id(x):
    return isinstance(x, str) and ID.match(x) is not None


def _fecha(x):
    if not (isinstance(x, str) and FECHA.match(x)):
        return None
    try:
        return date.fromisoformat(x)
    except ValueError:
        return None


def _forma_contexto(c) -> str | None:
    """Motivo del primer defecto de forma del contexto de F (T-22), o None."""
    if not (isinstance(c, dict) and set(c) == CLAVES_CONTEXTO):
        return "contexto con campos distintos de los exigidos"
    m = c["mandato"]
    if not (isinstance(m, dict) and set(m) == CLAVES_MANDATO and isinstance(m["version"], str) and m["version"]
            and (m["instrumentos_permitidos"] is None or (isinstance(m["instrumentos_permitidos"], list) and all(isinstance(x, str) for x in m["instrumentos_permitidos"])))
            and isinstance(m["exclusiones"], list) and all(isinstance(x, str) for x in m["exclusiones"])
            and _num(m["apalancamiento_max"], 1) and isinstance(m["horizonte_max_dias"], int) and not isinstance(m["horizonte_max_dias"], bool)
            and m["horizonte_max_dias"] >= 1):
        return "mandato del contexto inválido"
    if _fecha(c["fecha_revision"]) is None:
        return "fecha de revisión del contexto inválida"
    ex = c["exclusiones_duras"]
    if not (isinstance(ex, dict) and set(ex) == {"sanciones", "invertibilidad", "acceso"} and all(isinstance(v, str) for v in ex.values())):
        return "exclusiones duras del contexto inválidas"
    ev = c["evidencia"]
    if not (isinstance(ev, dict) and set(ev) == {"proporcion_verificado", "fecha_corte", "valid_until"} and _num(ev["proporcion_verificado"], 0)
            and ev["proporcion_verificado"] <= 1 and _fecha(ev["fecha_corte"]) is not None and isinstance(ev["valid_until"], str) and FH.match(ev["valid_until"])):
        return "evidencia del contexto inválida"
    if c["eventos"] is not None and not (isinstance(c["eventos"], list) and all(
            isinstance(x, dict) and set(x) == {"fecha", "tipo"} and _fecha(x["fecha"]) is not None and isinstance(x["tipo"], str) for x in c["eventos"])):
        return "eventos del contexto inválidos"
    au = c["autonomia"]
    if not (isinstance(au, dict) and set(au) == {"nivel", "kill_switch"} and isinstance(au["nivel"], str) and isinstance(au["kill_switch"], bool)):
        return "autonomía del contexto inválida"
    ac = c["actividad"]
    if not (isinstance(ac, dict) and set(ac) == {"importe_dia_eur", "ordenes_ultima_hora", "perdida_semana_eur"}
            and _num(ac["importe_dia_eur"], 0) and _num(ac["perdida_semana_eur"], 0) and isinstance(ac["ordenes_ultima_hora"], int)
            and not isinstance(ac["ordenes_ultima_hora"], bool) and ac["ordenes_ultima_hora"] >= 0):
        return "actividad del contexto inválida"
    pi = c["precio_intermediario"]
    if pi is not None and not (isinstance(pi, dict) and set(pi) == {"valor", "fecha_hora"} and _num(pi["valor"], 0, True)
                               and isinstance(pi["fecha_hora"], str) and FH.match(pi["fecha_hora"])):
        return "precio del intermediario del contexto inválido"
    return None


def controlar(sol, cart, pol, ahora, contexto=None) -> dict:
    """Aplica F-01..F-23 (sin contexto, solo las que no dependen de él: es el uso de E). Nunca lanza excepciones: cualquier
    fallo es un VETADO. Devuelve {resultado, cantidad_aprobada, controles}."""
    try:
        return _controlar(sol, cart, pol, ahora, contexto)
    except ERRORES as e:
        return {"resultado": "VETADO", "cantidad_aprobada": 0.0,
                "controles": [{"regla": "F-01", "resultado": "VETA", "valor": None, "limite": None, "motivo": f"error de cálculo: {type(e).__name__}"}]}


def _c(regla, resultado, valor=None, limite=None, motivo=""):
    return {"regla": regla, "resultado": resultado, "valor": valor, "limite": limite, "motivo": motivo}


def _controlar(sol, cart, pol, ahora, ctx=None):
    mal = _forma(sol, cart, pol, ahora) or (_forma_contexto(ctx) if ctx is not None else None)
    if mal:
        return {"resultado": "VETADO", "cantidad_aprobada": 0.0, "controles": [_c("F-01", "VETA", motivo=mal)]}
    cap_total = cart["capital_eur"]
    ent, stop, q = sol["precio_entrada"], sol["stop_precio"], sol["cantidad"]
    fx = tipo_cambio(sol["divisa_cotizacion"], cart)
    if fx is None:   # F-12: sin tipo de cambio no se puede valorar en euros
        return {"resultado": "VETADO", "cantidad_aprobada": 0.0,
                "controles": [_c("F-01", "OK"), _c("F-12", "VETA", sol["divisa_cotizacion"], None, "sin tipo de cambio a euros para la divisa de cotización")]}
    ctl = [_c("F-01", "OK"), _c("F-12", "OK", fx)]
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
    # F-16 (T-22) pérdida del día en euros, además del porcentaje de F-08
    ctl.append(_c("F-16", "OK" if cart["perdida_dia_eur"] < pol["perdida_dia_max_eur"] else "VETA", cart["perdida_dia_eur"], pol["perdida_dia_max_eur"],
                  "" if cart["perdida_dia_eur"] < pol["perdida_dia_max_eur"] else "pérdida del día en euros"))
    if ctx is not None:
        ctl += _controles_contexto(sol, pol, ahora, ctx)
    # topes de cantidad (REDUCE si la solicitud los supera)
    expuesto = sum(p["valor_eur"] for p in cart["posiciones"])
    mismo = sum(p["valor_eur"] for p in cart["posiciones"] if norm(p["activo_base"]) == norm(sol["activo_base"]))   # T-22: misma identidad, sea cual sea la grafía
    riesgo_unit = abs(ent - stop) * fx   # en euros por unidad
    ent_eur = ent * fx                    # valor en euros de una unidad
    topes = [("F-03", pol["riesgo_max_pct"] / 100 * cap_total / riesgo_unit if riesgo_unit > 0 else 0.0),
             ("F-04", pol["tamano_max_pct"] / 100 * cap_total / ent_eur),
             ("F-06", max(0.0, pol["exposicion_max_pct"] / 100 * cap_total - expuesto) / ent_eur),
             ("F-07", max(0.0, pol["concentracion_max_pct"] / 100 * cap_total - mismo) / ent_eur),
             ("F-13", pol["importe_max_orden_eur"] / ent_eur),   # T-22: importes nominales en euros
             ("F-15", max(0.0, pol["importe_max_activo_eur"] - mismo) / ent_eur)]
    if ctx is not None:
        topes.append(("F-14", max(0.0, pol["importe_max_dia_eur"] - ctx["actividad"]["importe_dia_eur"]) / ent_eur))
    for regla, tope in topes:
        ctl.append(_c(regla, "OK" if q <= tope else "REDUCE", q, tope))
    veta = any(x["resultado"] == "VETA" for x in ctl)
    aprobada = min([q] + [t for _, t in topes])
    aprobada = math.floor(aprobada * 1e6) / 1e6
    # F-11 una reducción que deja una posición sin sentido se veta
    ctl.append(_c("F-11", "OK" if aprobada * ent_eur >= pol["valor_min_eur"] else "VETA", aprobada * ent_eur, pol["valor_min_eur"]))
    veta = veta or ctl[-1]["resultado"] == "VETA"
    if veta:
        return {"resultado": "VETADO", "cantidad_aprobada": 0.0, "controles": ctl}
    return {"resultado": "REDUCIDO" if aprobada < q else "APROBADO", "cantidad_aprobada": aprobada, "controles": ctl}


def controles_de_contexto(sol, pol, ahora, ctx):
    """F-16 (semana) a F-23 sobre una solicitud, sin las reglas de cantidad: lo que el Orquestador vuelve a comprobar al enviar la
    orden (T-22, revisión H4). Nunca lanza: un contexto mal formado da un único VETA de F-01."""
    try:
        mal = _forma_contexto(ctx)
        return [_c("F-01", "VETA", motivo=mal)] if mal else _controles_contexto(sol, pol, ahora, ctx)
    except ERRORES as e:
        return [_c("F-01", "VETA", motivo=f"error de cálculo: {type(e).__name__}")]


def _controles_contexto(sol, pol, ahora, ctx):
    """F-16 (semana) a F-23: lo que F comprueba con el contexto del Orquestador (T-22). Solo OK o VETA."""
    out = []
    a = _dt(ahora)
    hoy = a.astimezone(timezone.utc).date()

    def chk(regla, ok, valor, limite, motivo):
        out.append(_c(regla, "OK" if ok else "VETA", valor, limite, "" if ok else motivo))
    ac = ctx["actividad"]
    chk("F-16", ac["perdida_semana_eur"] < pol["perdida_semana_max_eur"], ac["perdida_semana_eur"], pol["perdida_semana_max_eur"],
        "pérdida de la semana en euros")
    chk("F-17", ac["ordenes_ultima_hora"] < pol["ordenes_max_hora"], ac["ordenes_ultima_hora"], pol["ordenes_max_hora"],
        "demasiadas órdenes en la última hora")
    m = ctx["mandato"]
    i = norm(sol["instrumento"])
    dias = (_fecha(ctx["fecha_revision"]) - hoy).days
    motivo_m = ("el instrumento no está entre los permitidos del mandato" if m["instrumentos_permitidos"] is not None and i not in {norm(x) for x in m["instrumentos_permitidos"]}
                else "el instrumento está excluido por el mandato" if i in {norm(x) for x in m["exclusiones"]}
                else "apalancamiento mayor que el del mandato" if sol["apalancamiento"] > m["apalancamiento_max"]
                else "la revisión queda más allá del horizonte del mandato" if not 0 < dias <= m["horizonte_max_dias"]
                else "")
    chk("F-18", not motivo_m, dias, m["horizonte_max_dias"], motivo_m)
    malas = sorted(k for k, v in ctx["exclusiones_duras"].items() if v != "OK")
    chk("F-19", not malas, ",".join(malas) or None, None, "exclusión dura no superada: " + ",".join(malas))
    ev = ctx["evidencia"]
    edad_corte = (hoy - _fecha(ev["fecha_corte"])).days
    motivo_e = ("proporción de cifras verificadas por debajo del mínimo" if ev["proporcion_verificado"] < pol["evidencia_verificada_min"]
                else "fecha de corte vieja o futura" if not 0 <= edad_corte <= pol["corte_max_dias"]
                else "el sobre ya no está vigente" if not a < _dt(ev["valid_until"])
                else "")
    chk("F-20", not motivo_e, ev["proporcion_verificado"], pol["evidencia_verificada_min"], motivo_e)
    hasta = hoy + timedelta(days=pol["ventana_eventos_dias"])
    if ctx["eventos"] is None:
        chk("F-21", False, None, None, "el calendario de eventos no se puede leer")
    else:
        cerca = sorted({x["tipo"] for x in ctx["eventos"] if x["tipo"] in TIPOS_EVENTO_RESTRINGIDOS and hoy <= _fecha(x["fecha"]) <= hasta})
        u = a.astimezone(timezone.utc)
        finde = u.weekday() >= 5 or (u.weekday() == 4 and u.hour >= pol["viernes_corte_utc_h"])
        chk("F-21", not cerca and not finde, ",".join(cerca) or None, pol["ventana_eventos_dias"],
            ("evento en la ventana de restricción: " + ",".join(cerca)) if cerca else "fin de semana: riesgo de hueco")
    au = ctx["autonomia"]
    chk("F-22", au["nivel"] in NIVELES and not au["kill_switch"], au["nivel"], None,
        "kill-switch activo" if au["kill_switch"] else "nivel de autonomía desconocido")
    pi = ctx["precio_intermediario"]
    if pi is None:
        chk("F-23", False, None, None, "sin precio del intermediario para el instrumento")
    else:
        edad = (a - _dt(pi["fecha_hora"])).total_seconds() / 60
        deriva = abs(sol["precio_entrada"] / pi["valor"] - 1) * 100
        chk("F-23", 0 <= edad <= pol["precio_frescura_max_min"] and deriva <= pol["deriva_precio_max_pct"], deriva, pol["deriva_precio_max_pct"],
            "precio del intermediario viejo o del futuro" if not 0 <= edad <= pol["precio_frescura_max_min"]
            else "el límite se aleja del precio del intermediario")
    return out


VERSION_ESQUEMA = "0.3.0"   # T-47: envoltura común (data_refs, payload, resultado_politica). T-22: payload.entradas.contexto; la 0.2.0 está retirada


def motivo_de(resultado, controles) -> str:
    """Motivo del resultado, deducido de los controles (determinista: CF-04 lo recalcula)."""
    if resultado == "VETADO":
        c = next((x for x in controles if x.get("resultado") == "VETA"), None)
        return f"veta {c['regla']}" + (f": {c['motivo']}" if c and c.get("motivo") else "") if c else "veta"
    if resultado == "REDUCIDO":
        return "reduce " + ", ".join(x["regla"] for x in controles if x.get("resultado") == "REDUCE")
    return "todos los controles en OK"


def construir_informe(event_id, expediente_id, correlation_id, propuesta, sol, cart, pol, emitido_en, valid_until, contexto=None) -> dict:
    """CT-G-08 0.3.0 con la envoltura común. `contexto` es el que entrega el Orquestador (contexto_f); sin él el informe no vale (CF-01)."""
    r = controlar(sol, cart, pol, emitido_en, contexto) if contexto is not None else \
        {"resultado": "VETADO", "cantidad_aprobada": 0.0, "controles": [_c("F-01", "VETA", motivo="falta el contexto del Orquestador")]}
    return {"event_id": event_id, "correlation_id": correlation_id, "expediente_id": expediente_id, "producer": "F",
            "consumer": "ORQUESTADOR", "tipo_mensaje": "CT-G-08", "version_esquema": VERSION_ESQUEMA, "emitido_en": emitido_en,
            "valid_until": valid_until, "data_refs": [],
            "payload": {"propuesta_ref": {"expediente_id": expediente_id, "hash": hash_contenido(propuesta)},
                        "entradas": {"solicitud": sol, "cartera": cart, "politica": pol, "contexto": contexto},
                        "cantidad_aprobada": r["cantidad_aprobada"]},
            "resultado_politica": {"version_politica": VERSION_REGLAS, "resultado": r["resultado"],
                                   "motivo": motivo_de(r["resultado"], r["controles"]), "controles": r["controles"]}}


ENVOLTURA = {"event_id", "correlation_id", "expediente_id", "producer", "consumer", "tipo_mensaje", "version_esquema", "emitido_en",
             "valid_until", "data_refs", "payload", "resultado_politica"}
CAMPOS_PAYLOAD = {"propuesta_ref", "entradas", "cantidad_aprobada"}
CAMPOS_POLITICA = {"version_politica", "resultado", "motivo", "controles"}
# forma interna plana (la que usan el Orquestador y G); no es un mensaje
CAMPOS = {"event_id", "correlation_id", "expediente_id", "producer", "consumer", "tipo_mensaje", "version_esquema", "emitido_en",
          "valid_until", "version_reglas", "propuesta_ref", "entradas", "resultado", "cantidad_aprobada", "controles", "motivo"}


def aplanar_informe(inf):
    """Del mensaje CT-G-08 0.2.0 a la forma interna plana. None si no tiene exactamente la forma de la envoltura (no lanza)."""
    try:
        if not (isinstance(inf, dict) and set(inf) == ENVOLTURA and inf["version_esquema"] == VERSION_ESQUEMA
                and inf["tipo_mensaje"] == "CT-G-08" and inf["data_refs"] == []
                and isinstance(inf["payload"], dict) and set(inf["payload"]) == CAMPOS_PAYLOAD
                and isinstance(inf["resultado_politica"], dict) and set(inf["resultado_politica"]) == CAMPOS_POLITICA):
            return None
        pl, rp = inf["payload"], inf["resultado_politica"]
        return {**{k: inf[k] for k in ("event_id", "correlation_id", "expediente_id", "producer", "consumer", "tipo_mensaje",
                                       "version_esquema", "emitido_en", "valid_until")},
                "version_reglas": rp["version_politica"], "propuesta_ref": pl["propuesta_ref"], "entradas": pl["entradas"],
                "resultado": rp["resultado"], "cantidad_aprobada": pl["cantidad_aprobada"], "controles": rp["controles"], "motivo": rp["motivo"]}
    except ERRORES:
        return None


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
    if isinstance(inf, dict) and inf.get("version_esquema") != VERSION_ESQUEMA:
        return [{"regla": "CF-01", "mensaje": f"versión de CT-G-08 no admitida: {str(inf.get('version_esquema'))[:20]} (vigente {VERSION_ESQUEMA})"}]
    inf = aplanar_informe(inf)
    if inf is None:
        return [{"regla": "CF-01", "mensaje": "campos distintos de los exigidos (envoltura, payload, resultado_politica o data_refs)"}]
    if not (inf["producer"] == "F" and inf["consumer"] == "ORQUESTADOR" and inf["tipo_mensaje"] == "CT-G-08"
            and inf["version_esquema"] == VERSION_ESQUEMA and inf["version_reglas"] == VERSION_REGLAS
            and isinstance(inf["event_id"], str) and ID.match(inf["event_id"])
            and inf["resultado"] in ("APROBADO", "REDUCIDO", "VETADO") and _num(inf["cantidad_aprobada"], 0)
            and isinstance(inf["emitido_en"], str) and FH.match(inf["emitido_en"]) and isinstance(inf["valid_until"], str) and FH.match(inf["valid_until"])
            and isinstance(inf["entradas"], dict) and set(inf["entradas"]) == {"solicitud", "cartera", "politica", "contexto"}
            and isinstance(inf["entradas"]["contexto"], dict)
            and isinstance(inf["propuesta_ref"], dict) and set(inf["propuesta_ref"]) == {"expediente_id", "hash"}
            and isinstance(inf["controles"], list) and isinstance(inf["motivo"], str)):
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
                and sol.get("apalancamiento") == en["apalancamiento"] and sol.get("cantidad") == en["cantidad"]
                and sol.get("divisa_cotizacion") == ctx.get("divisa_cotizacion")):
            f("CF-05", "la solicitud no coincide con la propuesta (límite, stop, dirección, cartera, instrumento, activo base, divisa de cotización, apalancamiento y cantidad)")
    # CF-04 se recalcula con las mismas entradas
    r = controlar(sol, inf["entradas"]["cartera"], inf["entradas"]["politica"], inf["emitido_en"], inf["entradas"]["contexto"])
    if (r["resultado"], r["cantidad_aprobada"], r["controles"], motivo_de(r["resultado"], r["controles"])) \
            != (inf["resultado"], inf["cantidad_aprobada"], inf["controles"], inf["motivo"]):
        f("CF-04", "el resultado (o su motivo) no es el que dan las reglas con esas entradas")
    # CF-09 (T-22) el contexto es el que da el Orquestador con sus registros, no uno escrito por quien emite el informe
    if inf["entradas"]["contexto"] != ctx.get("contexto"):
        f("CF-09", "el contexto del informe no es el del Orquestador (mandato, evidencia, eventos, autonomía, actividad o precio)")
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
