"""G — ejecución y conciliación (código de referencia V0.1) y un intermediario SIMULADO para probarlo.

G envía las órdenes de una propuesta AUTORIZADA, protege la posición con un stop, comprueba contra el
intermediario que lo que cree que tiene es lo que tiene, y solo entonces se lo cuenta al Orquestador.
Determinista, sin LLM. Los identificadores de orden son deterministas: reintentar es seguro.
Falla cerrado: ante cualquier duda no se da por abierta una posición; si hay una posición sin protección o
no autorizada, se intenta cerrar y se avisa al operador.
"""
from __future__ import annotations

import copy
import math
import re

from control_f import ERRORES, divisa_cotizada, par_divisas
from manual_g import aplanar_manual, neto_libre, via_norm
from validar_sobre import _dt

ID = re.compile(r"^[A-Za-z0-9._:/-]{1,64}\Z")
TOL = 1e-6


class ConexionPerdida(Exception):
    pass


def _num(x, minimo=None):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) and (minimo is None or x > minimo)


class BrokerSimulado:
    """Intermediario de pruebas: precios fijos, ejecución completa o parcial, y fallos a demanda."""

    def __init__(self, capital_eur, precios, hora_datos, fraccion_fill=1.0, rechaza_stops=False, caido=False, rechaza_mercado=False, fraccion_mercado=1.0,
                 tipos_cambio=None):
        self.capital_eur, self.precios, self.hora_datos = capital_eur, dict(precios), hora_datos
        self.tipos_cambio = dict(tipos_cambio) if tipos_cambio is not None else None   # euros por unidad; None: se deducen de los pares con EUR
        self.cuenta = "SIM-1"
        self.fraccion_fill, self.rechaza_stops, self.caido, self.rechaza_mercado = fraccion_fill, rechaza_stops, caido, rechaza_mercado
        self.fraccion_mercado = fraccion_mercado
        self.ordenes, self.pos, self.perdida_dia_eur = {}, {}, 0.0

    def _expirar(self):
        """Una orden límite con valida_hasta deja de estar viva cuando el reloj del mercado pasa esa hora (GTD)."""
        for r in self.ordenes.values():
            x = r["orden"]
            if x["tipo"] == "LIMITE" and r["estado"] == "ACEPTADA" and x.get("valida_hasta") and _dt(self.hora_datos) > _dt(x["valida_hasta"]):
                r["estado"] = "CANCELADA"

    def avanzar_reloj(self, hora):
        self.hora_datos = hora
        self._expirar()

    def enviar(self, o):
        if self.caido:
            raise ConexionPerdida("sin conexión con el intermediario")
        ok = (isinstance(o, dict) and isinstance(o.get("orden_id"), str) and ID.match(o["orden_id"]) and o.get("tipo") in ("LIMITE", "MERCADO", "STOP")
              and o.get("lado") in ("COMPRA", "VENTA") and isinstance(o.get("instrumento"), str) and isinstance(o.get("activo_base"), str)
              and _num(o.get("cantidad"), 0) and (o["tipo"] == "MERCADO" or _num(o.get("precio"), 0))
              and (o.get("valida_hasta") is None or isinstance(o["valida_hasta"], str))
              and (o.get("via_acceso") is None or isinstance(o["via_acceso"], str))
              and isinstance(o.get("solo_reduccion", False), bool) and not (o.get("solo_reduccion") and o["tipo"] == "LIMITE"))
        if not ok:
            return {"orden_id": o.get("orden_id") if isinstance(o, dict) else None, "estado": "RECHAZADA", "cantidad_ejecutada": 0.0, "precio_medio": None}
        prev = self.ordenes.get(o["orden_id"])
        if prev is not None:   # idempotencia: el mismo id con el mismo contenido devuelve lo ya hecho
            if prev["orden"] == o:
                return self._res(prev)
            return {"orden_id": o["orden_id"], "estado": "RECHAZADA", "cantidad_ejecutada": 0.0, "precio_medio": None}
        reg = {"orden": copy.deepcopy(o), "estado": "ACEPTADA", "ejecutada": 0.0, "precio_medio": None}
        self.ordenes[o["orden_id"]] = reg
        p = self.precios.get(o["instrumento"])
        if p is None or (o["tipo"] == "MERCADO" and self.rechaza_mercado):
            reg["estado"] = "RECHAZADA"
        elif o["tipo"] == "STOP":
            tiene = self._reducible(o)   # un stop de venta protege un largo
            # un stop normal debe tener debajo toda su cantidad; uno de solo reducción, algo que reducir
            if self.rechaza_stops or (tiene <= TOL if o.get("solo_reduccion") else tiene + TOL < o["cantidad"]):
                reg["estado"] = "RECHAZADA"
            elif (o["lado"] == "VENTA" and p <= o["precio"]) or (o["lado"] == "COMPRA" and p >= o["precio"]):   # ya cruzado: salta al instante
                q = min(o["cantidad"], tiene)
                self._fill(o, q, p)
                reg["ejecutada"], reg["precio_medio"], reg["estado"] = q, p, "EJECUTADA"
        else:
            sale = o["tipo"] == "MERCADO" or (o["lado"] == "COMPRA" and p <= o["precio"]) or (o["lado"] == "VENTA" and p >= o["precio"])
            if sale:
                q = o["cantidad"] * (self.fraccion_fill if o["tipo"] == "LIMITE" else self.fraccion_mercado)
                if o.get("solo_reduccion"):   # nunca abre ni da la vuelta a una posición
                    q = min(q, max(self._reducible(o), 0.0))
                if q <= TOL:
                    reg["estado"] = "CANCELADA"
                    return self._res(reg)
                self._fill(o, q, p)
                reg["ejecutada"], reg["precio_medio"] = q, p   # ejecución inmediata: el simulador no tiene reloj; G usará el instante de la llamada
                reg["estado"] = "EJECUTADA" if q >= o["cantidad"] - TOL else "PARCIAL"
        return self._res(reg)

    def _reducible(self, o):
        """Cantidad de la posición que la orden reduciría (positiva si va en contra de la posición)."""
        signo = 1 if o["lado"] == "VENTA" else -1
        return self.pos.get(o["instrumento"], {"cantidad": 0.0})["cantidad"] * signo

    def _fill(self, o, q, p):
        d = q if o["lado"] == "COMPRA" else -q
        cur = self.pos.get(o["instrumento"], {"cantidad": 0.0, "activo_base": o["activo_base"]})
        cur["cantidad"] += d
        if abs(cur["cantidad"]) <= TOL:
            self.pos.pop(o["instrumento"], None)
        else:
            self.pos[o["instrumento"]] = cur
        for r in self.ordenes.values():   # un stop que ya no tiene posición debajo se cancela
            x = r["orden"]
            if x["tipo"] == "STOP" and r["estado"] == "ACEPTADA" and x["instrumento"] == o["instrumento"]:
                tiene = self._reducible(x)
                # uno de solo reducción sigue vivo mientras quede algo que reducir: nunca abre la posición contraria
                if (tiene <= TOL) if x.get("solo_reduccion") else (tiene + TOL < x["cantidad"]):
                    r["estado"] = "CANCELADA"

    def mover_precio(self, instrumento, precio, hora=None):
        """Simula el mercado: cambia el precio y dispara los stops cruzados (se ejecutan al precio nuevo, como un salto)."""
        self.precios[instrumento] = precio
        if hora:
            self.hora_datos = hora   # también es el instante en que se ejecuta lo que el movimiento dispare
        self._expirar()
        for r in self.ordenes.values():
            x = r["orden"]
            if x["tipo"] == "STOP" and r["estado"] == "ACEPTADA" and x["instrumento"] == instrumento \
                    and ((x["lado"] == "VENTA" and precio <= x["precio"]) or (x["lado"] == "COMPRA" and precio >= x["precio"])):
                q = min(x["cantidad"], self._reducible(x)) if x.get("solo_reduccion") else x["cantidad"]
                if q <= TOL:
                    r["estado"] = "CANCELADA"
                    continue
                self._fill(x, q, precio)
                r["ejecutada"], r["precio_medio"], r["estado"], r["ejecutada_en"] = q, precio, "EJECUTADA", self.hora_datos
        for r in self.ordenes.values():   # una orden límite viva se ejecuta si el precio la alcanza
            x = r["orden"]
            if x["tipo"] == "LIMITE" and r["estado"] == "ACEPTADA" and x["instrumento"] == instrumento \
                    and ((x["lado"] == "COMPRA" and precio <= x["precio"]) or (x["lado"] == "VENTA" and precio >= x["precio"])):
                q = x["cantidad"] * self.fraccion_fill
                self._fill(x, q, precio)
                r["ejecutada"], r["precio_medio"], r["ejecutada_en"] = q, precio, self.hora_datos
                r["estado"] = "EJECUTADA" if q >= x["cantidad"] - TOL else "PARCIAL"

    @staticmethod
    def _res(reg):
        o = reg["orden"]
        return {"orden_id": o["orden_id"], "estado": reg["estado"], "cantidad_ejecutada": reg["ejecutada"], "precio_medio": reg["precio_medio"],
                "tipo": o["tipo"], "lado": o["lado"], "cantidad": o["cantidad"], "precio": o.get("precio"), "instrumento": o["instrumento"],
                "ejecutada_en": reg.get("ejecutada_en"), "solo_reduccion": bool(o.get("solo_reduccion")),
                "via_acceso": o.get("via_acceso")}

    def cancelar(self, orden_id):
        if self.caido:
            raise ConexionPerdida("sin conexión con el intermediario")
        r = self.ordenes.get(orden_id)
        if r is not None and r["estado"] in ("ACEPTADA", "PARCIAL"):   # de una parcial se cancela el resto; lo ejecutado queda
            r["estado"] = "CANCELADA"
        return self._res(r) if r else None

    def consultar(self, orden_id):
        if self.caido:
            raise ConexionPerdida("sin conexión con el intermediario")
        self._expirar()
        r = self.ordenes.get(orden_id)
        return self._res(r) if r else None

    def tipos_cambio_eur(self):
        """Euros por unidad de cada divisa: los fijados, o los que se deducen de los precios de pares con el euro."""
        if self.caido:
            raise ConexionPerdida("sin conexión con el intermediario")
        if self.tipos_cambio is not None:
            return dict(self.tipos_cambio)
        t = {}
        for ins, p in self.precios.items():
            par = par_divisas(ins)
            if par and par[0] == "EUR" and p > 0:
                t[par[1]] = 1 / p
            elif par and par[1] == "EUR" and p > 0:
                t[par[0]] = p
        return t

    def posiciones(self):
        if self.caido:
            raise ConexionPerdida("sin conexión con el intermediario")
        return [{"instrumento": k, "activo_base": v["activo_base"], "cantidad": v["cantidad"]} for k, v in sorted(self.pos.items())]


def cartera_para_f(broker, divisas=None):
    """El estado de cartera que F necesita, tomado del intermediario y no de quien emite el informe, valorado en euros
    con los tipos de cambio del propio intermediario. Si falta un tipo de cambio para valorar una posición, falla (fail-closed)."""
    pos = broker.posiciones()
    tipos = broker.tipos_cambio_eur()
    valores = []
    for p in pos:
        d = divisa_cotizada(p["instrumento"], divisas)
        fx = 1.0 if d == "EUR" else tipos.get(d)
        if fx is None:
            raise ValueError(f"sin tipo de cambio para valorar {p['instrumento']} en euros")
        valores.append({"instrumento": p["instrumento"], "activo_base": p["activo_base"],
                        "valor_eur": abs(p["cantidad"]) * broker.precios[p["instrumento"]] * fx})
    return {"fecha_hora": broker.hora_datos, "capital_eur": broker.capital_eur, "perdida_dia_eur": broker.perdida_dia_eur,
            "posiciones": valores, "tipos_cambio_eur": tipos}


def foto_cartera(o, broker, ahora):
    """G toma la foto de cartera del intermediario y la registra en el Orquestador (T-11). Devuelve la foto o None."""
    try:
        f = cartera_para_f(broker, o.cfg.get("divisas_cotizacion"))
    except (ConexionPerdida, ValueError, KeyError):
        return None
    return f if o.registrar_cartera(f, "G", _instante(o, ahora), cuenta=getattr(broker, "cuenta", None))["ok"] else None


def _r(ok, codigo, motivo, **extra):
    return {"ok": ok, "codigo": codigo, "motivo": motivo, **extra}


def _instante(o, ahora):
    """El instante con el que G informa al Orquestador: nunca anterior al último que este vio (si no, el aviso se perdería)."""
    return max(ahora, o.ultimo_ahora, key=_dt) if o.ultimo_ahora else ahora


def _aviso(o, diferencias, ahora):
    """Informa al Orquestador y devuelve si quedó registrado."""
    try:
        return bool(o.reportar_discrepancia(diferencias, "G", _instante(o, ahora))["ok"])
    except Exception:   # noqa: BLE001 - informar nunca debe romper el cierre de emergencia
        return False


def _id_libre(broker, base, reutilizable):
    """Identificador determinista con número de intento. Se reutiliza el de una orden viva o ejecutada (idempotencia);
    si la anterior fue rechazada o cancelada sin ejecutar nada, se pasa al siguiente intento."""
    for n in range(1, 6):
        oid = f"{base}-{n}"
        c = broker.consultar(oid)
        if c is None:
            return oid
        if c["estado"] in ("ACEPTADA", "EJECUTADA", "PARCIAL") and (reutilizable or c["estado"] == "ACEPTADA"):
            return oid
    raise ValueError("demasiados intentos con el mismo identificador")


PENDIENTES = ("ENVIADA", "PARCIAL", "EJECUTADA")   # orden de entrada en curso: aún no conciliada ni cerrada


def _id_nuevo(broker, base, usados=()):
    """Identificador de un intento de entrada nuevo: nunca uno que el intermediario o el Orquestador ya conozcan."""
    for n in range(1, 10):
        oid = f"{base}-{n}"
        if oid not in usados and broker.consultar(oid) is None:
            return oid
    raise ValueError("demasiados intentos de entrada")


def ejecutar(o, expediente_id, broker, ahora):
    """Ejecuta una propuesta AUTORIZADA. No lanza excepciones. Códigos: OK; G-01 (intermediario inalcanzable antes de enviar nada);
    G-02 (sin ejecución); G-03 (protección fallida: se cerró); G-04 (CRÍTICO: queda posición sin proteger);
    G-05 (el Orquestador rechazó lo ejecutado: se cerró); G-06 (no ejecutable: no se envió nada);
    G-08 (fallo con órdenes ya enviadas: estado incierto, hay que conciliar);
    G-11 (la orden de entrada queda viva en el intermediario hasta que venza la ventana; la revisa `revisar_entrada`)."""
    est = {"enviado": False}
    try:
        return _ejecutar(o, expediente_id, broker, ahora, est)
    except ConexionPerdida as e:
        if not est["enviado"]:
            return _r(False, "G-01", f"intermediario inalcanzable antes de enviar nada: {e}. Se puede reintentar.")
        return _incierto(o, expediente_id, ahora, f"conexión perdida: {e}")
    except Exception as e:   # noqa: BLE001 - tras enviar órdenes, cualquier fallo deja el estado incierto
        if not est["enviado"]:
            return _r(False, "G-06", f"error inesperado antes de enviar nada: {type(e).__name__}")
        return _incierto(o, expediente_id, ahora, f"{type(e).__name__}")


def _incierto(o, eid, ahora, causa):
    reg = _aviso(o, [{"tipo": "ESTADO_INCIERTO", "ref": eid, "detalle": f"fallo tras enviar órdenes ({causa}); puede haber posición o stop sin confirmar"}], ahora)
    return _r(False, "G-08", f"fallo con órdenes ya enviadas ({causa}): estado incierto, hay que conciliar con el intermediario.", incierto=True, aviso_registrado=reg)


def _ejecutar(o, eid, broker, ahora, est):
    e = o.expedientes.get(eid)
    if e is None or e["estado"] != "AUTORIZADA" or not e.get("control_f"):
        return _r(False, "G-06", "el expediente no está AUTORIZADA con un informe de F")
    if o.ultimo_ahora and _dt(ahora) < _dt(o.ultimo_ahora):
        return _r(False, "G-06", "el instante recibido es anterior al último que vio el Orquestador; no se envía nada")
    oe = e.get("orden_entrada")
    if oe and oe["estado"] in PENDIENTES:   # hay una entrada en curso: se revisa (y se protege si se ejecutó); nunca se envía otra
        return revisar_entrada(o, eid, broker, ahora)
    en, cf = e["propuesta"]["entrada"], e["control_f"]
    if _dt(ahora) > _limite_entrada(o, e) or o._sello_anulado(e):
        return _r(False, "G-06", "la ventana de entrada, el sobre, el informe de F o el sello ya no valen; no se envía nada")
    if not o.autorizacion_vigente(e):
        return _r(False, "G-06", "la autorización ya no vale (fue automática y la cartera ya no está en L2, o después se bajó el límite de "
                                 "pérdida): vuelve a pasar por F y por el operador; no se envía nada")
    if any(p["instrumento"] == en["instrumento"] and p["estado"] != "CERRADA" for p in o.posiciones.values()) \
            or any(p["instrumento"] == en["instrumento"] for p in broker.posiciones()):
        return _r(False, "G-06", "ya hay una posición sobre ese instrumento; en esta versión solo se admite una por instrumento")
    previos = (oe or {}).get("anteriores", []) + ([oe] if oe else [])
    for x in previos:   # un intento anterior que siga vivo (envío perdido que llegó tarde) se cancela antes de enviar otro
        c = broker.consultar(x["orden_id"])
        if c and c["estado"] in ("ACEPTADA", "PARCIAL"):
            est["enviado"] = True
            broker.cancelar(x["orden_id"])
            c = broker.consultar(x["orden_id"])
            if c and c["estado"] in ("ACEPTADA", "PARCIAL") or (c and c["cantidad_ejecutada"] > 0):
                return _incierto(o, eid, ahora, f"un intento anterior ({x['orden_id']}) seguía vivo o se ejecutó")
    id_e = _id_nuevo(broker, f"ORD-{eid}-E", {x["orden_id"] for x in previos})
    st = [c for c in e["propuesta"]["salida"]["condiciones"] if c["tipo"] == "STOP"][0]
    lado_e = "COMPRA" if st["operador"] in ("<", "<=") else "VENTA"
    # se anota ENVIADA antes de enviar: si el envío se pierde, la revisión la marcará como rechazada; nunca hay una orden viva desconocida
    t = o.orden_entrada(eid, id_e, "ENVIADA", 0.0, "G", _instante(o, ahora))
    if not t["ok"]:
        return _r(False, "G-06", f"el Orquestador no admite la orden de entrada ({t['codigo']}): {t['motivo']}")
    est["enviado"] = True
    r = broker.enviar({"instrumento": en["instrumento"], "activo_base": en["activo_base"], "orden_id": id_e, "tipo": "LIMITE",
                       "lado": lado_e, "cantidad": cf["cantidad_aprobada"], "precio": en["limite"],
                       "valida_hasta": _limite_entrada(o, e).isoformat(),   # caduca también en el intermediario, aunque G no vuelva
                       "via_acceso": en["via_acceso"]})   # por la vía analizada (el adaptador real la traduce a su producto, T-45)
    return _resolver(o, eid, broker, ahora, r, est)


def _limite_entrada(o, e):
    en, cf = e["propuesta"]["entrada"], e["control_f"]
    return min(_dt(en["ventana_hasta"]), _dt(e["sobre"]["valid_until"]), _dt(cf["valid_until"]))


def revisar_entrada(o, expediente_id, broker, ahora, forzar_cancelacion=False):
    """Revisa la orden de entrada en curso. ENVIADA: si se ejecutó (toda o en parte) protege y reporta; si venció, la cartera
    se degradó o se pide cancelar, la cancela. PARCIAL o EJECUTADA aún sin conciliar (p. ej., se perdió la conexión al poner
    el stop): reanuda la protección. No lanza excepciones. Mismos códigos que ejecutar."""
    est = {"enviado": True}
    try:
        e = o.expedientes.get(expediente_id) if isinstance(expediente_id, str) else None
        oe = e.get("orden_entrada") if e else None
        if not (e and e["estado"] == "AUTORIZADA" and oe and oe["estado"] in PENDIENTES):
            return _r(False, "G-06", "no hay una orden de entrada en curso que revisar")
        if o.ultimo_ahora and _dt(ahora) < _dt(o.ultimo_ahora):
            return _r(False, "G-06", "el instante recibido es anterior al último que vio el Orquestador")
        c = broker.consultar(oe["orden_id"])
        if oe["estado"] != "ENVIADA":
            if c is None or c["cantidad_ejecutada"] <= 0:
                return _incierto(o, expediente_id, ahora, "la orden anotada como ejecutada no aparece ejecutada en el intermediario")
            return _proteger(o, expediente_id, broker, ahora, c, oe["cantidad_ejecutada"], est)
        if c is None:   # se anotó pero nunca llegó al intermediario
            o.orden_entrada(expediente_id, oe["orden_id"], "RECHAZADA", 0.0, "G", _instante(o, ahora))
            return _r(False, "G-02", "la orden de entrada no llegó al intermediario; se anota como rechazada")
        return _resolver(o, expediente_id, broker, ahora, c, est, forzar_cancelacion)
    except ConexionPerdida as ex:
        oe = (o.expedientes.get(expediente_id) or {}).get("orden_entrada") if isinstance(expediente_id, str) else None
        if oe and oe["estado"] == "ENVIADA":
            return _r(False, "G-01", f"sin conexión con el intermediario; la orden sigue anotada como enviada y se revisará ({ex})")
        return _incierto(o, expediente_id, ahora, f"conexión perdida con la entrada ya ejecutada: {ex}")
    except Exception as ex:   # noqa: BLE001
        return _incierto(o, expediente_id, ahora, f"{type(ex).__name__} al revisar la entrada")


def cancelar_entrada(o, expediente_id, broker, ahora):
    """Cancela a petición (operador o kill-switch) la orden de entrada viva. Lo que ya se hubiera ejecutado se protege y reporta."""
    return revisar_entrada(o, expediente_id, broker, ahora, forzar_cancelacion=True)


def kill_switch(o, broker, ahora, motivo, actor="OPERADOR"):
    """Kill-switch (§8): el Orquestador bloquea lo nuevo y pasa todo a L1; G cancela todas las órdenes de entrada vivas.
    No toca las órdenes de protección ni liquida posiciones. Lo que ya se hubiera ejecutado se protege y reporta."""
    r = o.activar_kill_switch(motivo, actor, _instante(o, ahora))
    if not r["ok"]:
        return r
    resultados = {}
    for eid in sorted(o.expedientes):
        x = o.expedientes[eid]
        if x["estado"] == "AUTORIZADA" and (x.get("orden_entrada") or {}).get("estado") in PENDIENTES:
            resultados[eid] = revisar_entrada(o, eid, broker, ahora, forzar_cancelacion=True)["codigo"]
    vivas = [k for k, v in resultados.items() if v in ("G-01", "G-08", "G-11")]
    return _r(not vivas, "OK" if not vivas else "G-08", "kill-switch activo; entradas canceladas" if not vivas
              else f"kill-switch activo, pero no se pudieron cancelar: {', '.join(vivas)}", entradas=resultados)


def _resolver(o, eid, broker, ahora, r, est, forzar=False):
    """Decide qué hacer con la orden de entrada según su estado en el intermediario."""
    e = o.expedientes[eid]
    id_e = r["orden_id"]
    vencida = forzar or o.kill is not None or _dt(ahora) > _limite_entrada(o, e) or o._sello_anulado(e) or not o.autorizacion_vigente(e)
    if r["estado"] == "ACEPTADA" and not vencida:
        return _r(False, "G-11", f"orden de entrada viva hasta {_limite_entrada(o, e).isoformat()}", orden_id=id_e, viva=True)
    if r["estado"] in ("ACEPTADA", "PARCIAL"):   # vencida, cancelada a petición, o parcial: se cancela el resto (resto_parcial = CANCELAR)
        broker.cancelar(id_e)
        r2 = broker.consultar(id_e)
        if r2 is None or r2["estado"] in ("ACEPTADA", "PARCIAL"):
            return _incierto(o, eid, ahora, "la orden de entrada no se pudo cancelar")
        r = r2
    fq = r["cantidad_ejecutada"] or 0.0
    if fq <= TOL:
        estado = "RECHAZADA" if r["estado"] == "RECHAZADA" else "CANCELADA"
        o.orden_entrada(eid, id_e, estado, 0.0, "G", _instante(o, ahora))
        return _r(False, "G-02", f"sin ejecución ({r['estado']}{', cancelada' if vencida else ''}); nada que reportar al Orquestador")
    estado = "EJECUTADA" if fq >= e["control_f"]["cantidad_aprobada"] - TOL else "PARCIAL"
    t = o.orden_entrada(eid, id_e, estado, fq, "G", _instante(o, ahora))
    if not t["ok"]:
        return _incierto(o, eid, ahora, f"el Orquestador no anota la ejecución de la entrada ({t['codigo']})")
    return _proteger(o, eid, broker, ahora, r, fq, est)


def _proteger(o, eid, broker, ahora, r, fq, est):
    e = o.expedientes[eid]
    cf, en = e["control_f"], e["propuesta"]["entrada"]
    id_e = r["orden_id"]
    st = [c for c in e["propuesta"]["salida"]["condiciones"] if c["tipo"] == "STOP"][0]
    largo = st["operador"] in ("<", "<=")
    lado_s = "VENTA" if largo else "COMPRA"
    base = {"instrumento": en["instrumento"], "activo_base": en["activo_base"], "via_acceso": en["via_acceso"]}
    precio = r["precio_medio"]
    id_s = _id_libre(broker, f"ORD-{eid}-S", reutilizable=False)

    def deshacer(codigo, motivo):
        """Cierra lo que el intermediario tenga realmente sobre el instrumento (no lo que G cree). Si no puede: aviso CRÍTICO."""
        try:
            broker.cancelar(id_s)
            neto = {p["instrumento"]: p["cantidad"] for p in broker.posiciones()}.get(en["instrumento"], 0.0)
            if abs(neto) > TOL:
                id_x = _id_libre(broker, f"ORD-{eid}-X", reutilizable=False)   # nunca la venta de un intento anterior
                broker.enviar({**base, "orden_id": id_x, "tipo": "MERCADO", "lado": "VENTA" if neto > 0 else "COMPRA", "cantidad": abs(neto),
                               "solo_reduccion": True})
            resto = {p["instrumento"]: p["cantidad"] for p in broker.posiciones()}.get(en["instrumento"], 0.0)
            vivo = broker.consultar(id_s)
        except Exception as ex:   # noqa: BLE001
            return _incierto(o, eid, ahora, f"{type(ex).__name__} al deshacer: {motivo}")
        if abs(resto) <= TOL and (vivo is None or vivo["estado"] != "ACEPTADA"):
            o.orden_entrada(eid, id_e, "DESHECHA", fq, "G", _instante(o, ahora))   # cerrada y comprobada: admite un intento nuevo
            reg = _aviso(o, [{"tipo": "POSICION_CERRADA_POR_G", "ref": eid, "detalle": motivo}], ahora)
            return _r(False, codigo, motivo + " No queda posición ni stop vivos.", cerrada=True, aviso_registrado=reg)
        reg = _aviso(o, [{"tipo": "POSICION_SIN_PROTEGER", "ref": eid, "detalle": motivo + " Y no se pudo cerrar."}], ahora)
        return _r(False, "G-04", "CRÍTICO: " + motivo + " La posición no se pudo cerrar.", cerrada=False, aviso_registrado=reg)

    ent = broker.consultar(id_e)
    if not ent or via_norm(ent.get("via_acceso")) != via_norm(en["via_acceso"]):   # el intermediario ejecutó por otra vía: no es lo analizado
        return deshacer("G-03", "el intermediario no confirma la vía de acceso autorizada.")
    s = broker.enviar({**base, "orden_id": id_s, "tipo": "STOP", "lado": lado_s, "cantidad": fq, "precio": st["umbral"], "solo_reduccion": True})
    if s["estado"] != "ACEPTADA":
        return deshacer("G-03", f"el intermediario no aceptó el stop ({s['estado']}).")
    pos = {p["instrumento"]: p for p in broker.posiciones()}
    p = pos.get(en["instrumento"])
    chk = broker.consultar(id_s)
    if not (p and abs(abs(p["cantidad"]) - fq) <= TOL and (p["cantidad"] > 0) == largo and chk and chk["estado"] == "ACEPTADA"):
        return deshacer("G-03", "el intermediario no confirma la posición y su stop.")
    res = o.ejecutar(eid, {"orden_id": id_e, "cantidad": fq, "precio": precio, "conciliada": True, "proteccion_orden_ids": [id_s],
                           "ejecutada_en": r.get("ejecutada_en")}, "G", _instante(o, ahora))
    if not res["ok"]:
        return deshacer("G-05", f"el Orquestador rechazó la ejecución ({res['codigo']}: {res['motivo'][:80]}).")
    return _r(True, "OK", "ejecutada y conciliada", posicion_id=res.get("posicion_id"), cantidad=fq, precio=precio)


def conciliar(o, broker, ahora):
    """Compara lo que el Orquestador cree con lo que dice el intermediario e informa de las discrepancias.
    Por instrumento, la cantidad esperada (con signo) es la de las posiciones abiertas más las operaciones LIBRES
    declaradas por el operador (CT-G-14). Una diferencia nula con operaciones declaradas, o dentro de la tolerancia
    configurada, es una diferencia EXPLICADA: se devuelve y no dispara nada. Lo demás es discrepancia y se avisa."""
    dif, expl = [], []
    try:
        tol = o.cfg.get("tolerancia_conciliacion_rel", 0.0)
        manuales = getattr(o, "manuales", [])
        reales = {p["instrumento"]: p for p in broker.posiciones()}
        abiertas = {}
        for pid, p in o.posiciones.items():
            todos = _stops_de(broker, pid, p)
            if p["estado"] == "CERRADA":
                for prot in todos:   # un stop vivo de una posición cerrada abriría una posición contraria
                    c = broker.consultar(prot)
                    if c and c["estado"] == "ACEPTADA":
                        dif.append({"tipo": "PROTECCION_HUERFANA", "ref": pid, "detalle": f"la orden {prot} sigue viva con la posición cerrada"})
                continue
            saltado = [c for c in (broker.consultar(x) for x in todos) if c and c["estado"] == "EJECUTADA"]
            if saltado and abs(_neto(broker, p["instrumento"])) <= TOL:   # el stop propio ya cerró la posición; H lo confirmará (H-01)
                expl.append({"tipo": "STOP_EJECUTADO", "ref": pid, "detalle": f"el stop {saltado[0]['orden_id']} cerró la posición; falta que H lo confirme"})
                continue
            abiertas.setdefault(p["instrumento"], []).append((pid, p))
            lado_s = "VENTA" if p["direccion"] == "LARGO" else "COMPRA"
            if p["estado"] == "REDUCIENDO":   # a media reducción basta un stop vivo que cubra lo que hay de verdad
                real_abs = abs(_neto(broker, p["instrumento"]))
                buenos = [x for x in todos if (c := broker.consultar(x)) and c["estado"] == "ACEPTADA" and c["tipo"] == "STOP" and c["lado"] == lado_s
                          and c["precio"] == p["stop_precio"] and via_norm(c.get("via_acceso")) == via_norm(p.get("via_acceso")) and c["cantidad"] + TOL >= real_abs and (c["solo_reduccion"] or abs(c["cantidad"] - real_abs) <= TOL)]
                if not buenos:
                    dif.append({"tipo": "PROTECCION", "ref": pid, "detalle": "a media reducción no hay un stop vivo que cubra la posición real"})
                fijos = False
            else:
                fijos = True
            for prot in (p["protecciones"] if fijos else []):
                c = broker.consultar(prot)
                if not c or c["estado"] != "ACEPTADA":
                    dif.append({"tipo": "PROTECCION", "ref": pid, "detalle": f"la orden de protección {prot} no está viva ({c['estado'] if c else 'inexistente'})"})
                elif not (c["tipo"] == "STOP" and c["lado"] == lado_s and abs(c["cantidad"] - p["cantidad"]) <= TOL and c["precio"] == p["stop_precio"]
                          and via_norm(c.get("via_acceso")) == via_norm(p.get("via_acceso"))):
                    dif.append({"tipo": "PROTECCION", "ref": pid, "detalle": f"el stop {prot} no coincide con la posición (tipo, lado, cantidad o precio)"})
            for prot in (x for x in todos if x not in p["protecciones"] and fijos):   # stops retirados que siguen vivos
                c = broker.consultar(prot)
                if c and c["estado"] == "ACEPTADA":
                    dif.append({"tipo": "PROTECCION_HUERFANA", "ref": pid, "detalle": f"el stop retirado {prot} sigue vivo"})
        for pid, p in o.posiciones.items():   # una venta de reducción o una orden de cierre viva podría ejecutarse sin control
            ns = [r["n"] for r in p.get("reducciones", [])] + ([p["reduccion"]["n"]] if p.get("reduccion") else [])
            for x in [y for n in ns for y in _ids_reduccion(broker, pid, n, "M")] + _ids_cierre(broker, pid):
                c = broker.consultar(x)
                if c and c["estado"] in ("ACEPTADA", "PARCIAL"):
                    dif.append({"tipo": "ORDEN_VIVA", "ref": pid, "detalle": f"la orden {x} de G sigue viva en el intermediario"})
        for eid, e in o.expedientes.items():   # una orden de entrada viva que el Orquestador ya no espera abriría una posición sin control
            oe = e.get("orden_entrada")
            if not oe:
                continue
            esperada = oe["orden_id"] if (oe["estado"] == "ENVIADA" and e["estado"] == "AUTORIZADA") else None
            for x in oe.get("anteriores", []) + [oe]:
                if x["orden_id"] == esperada:
                    continue
                c = broker.consultar(x["orden_id"])
                if c and c["estado"] in ("ACEPTADA", "PARCIAL"):
                    dif.append({"tipo": "ENTRADA_HUERFANA", "ref": eid, "detalle": f"la orden de entrada {x['orden_id']} sigue viva y el Orquestador no la espera"})
        libres = {r["instrumento"] for r in manuales if r["vinculo"]["tipo"] == "LIBRE"}
        for ins in sorted(set(reales) | set(abiertas) | libres):
            ps = abiertas.get(ins, [])
            libre = 0.0 if ps else neto_libre(manuales, ins)   # una LIBRE nunca explica la cantidad de una posición del sistema
            esperado = sum(p["cantidad"] if p["direccion"] == "LARGO" else -p["cantidad"] for _, p in ps) + libre
            r = reales.get(ins)
            real = r["cantidad"] if r else 0.0
            d = real - esperado
            ref = ps[0][0] if len(ps) == 1 else ins
            if abs(d) <= TOL:
                if abs(libre) > TOL:
                    expl.append({"tipo": "MANUAL_DECLARADA", "ref": ins, "detalle": f"{libre:+} declarado por el operador (CT-G-14)"})
            elif not ps and abs(libre) <= TOL and _entrada_en_curso(o, ins, real):
                expl.append({"tipo": "ENTRADA_EN_CURSO", "ref": ins, "detalle": f"{real} de una orden de entrada ejecutada que G aún no ha protegido y reportado"})
            elif len(ps) == 1 and abs(libre) <= TOL and (x := _en_curso(broker, ps[0][0], ps[0][1], real)):
                expl.append({"tipo": x, "ref": ref, "detalle": f"el intermediario tiene {real}: lo que dejan las órdenes de G ya ejecutadas"})
            elif ps and real * esperado < 0:
                dif.append({"tipo": "SENTIDO_O_ACTIVO", "ref": ref, "detalle": "el sentido no coincide con el intermediario"})
            elif ps and abs(d) <= tol * abs(esperado):
                expl.append({"tipo": "REDONDEO", "ref": ref, "detalle": f"diferencia {d:+.6g} dentro de la tolerancia relativa {tol}"})
            elif not ps and abs(libre) <= TOL:
                dif.append({"tipo": "POSICION_DESCONOCIDA", "ref": ins, "detalle": f"el intermediario tiene {real} que el Orquestador no conoce ni el operador declaró"})
            elif not ps:
                dif.append({"tipo": "MANUAL_NO_CUADRA", "ref": ins, "detalle": f"el operador declaró {libre:+} y el intermediario tiene {real}"})
            else:
                dif.append({"tipo": "CANTIDAD", "ref": ref, "detalle": f"Orquestador {esperado}, intermediario {real}"})
            for pid, p in ps:
                if r is not None and r["activo_base"] != p["activo_base"]:
                    dif.append({"tipo": "SENTIDO_O_ACTIVO", "ref": pid, "detalle": "el activo base no coincide con el intermediario"})
            if not ps and r is not None and abs(libre) > TOL:
                bases = {x["activo_base"] for x in manuales if x["vinculo"]["tipo"] == "LIBRE" and x["instrumento"] == ins}
                if bases != {r["activo_base"]}:
                    dif.append({"tipo": "SENTIDO_O_ACTIVO", "ref": ins, "detalle": "el activo base declarado no coincide con el intermediario"})
        if hasattr(o, "registrar_conciliacion"):
            o.registrar_conciliacion(not dif, "G", _instante(o, ahora))
        if dif:
            _aviso(o, dif, ahora)
            if getattr(o, "kill", None) is not None:   # el kill-switch automático: G cancela en el acto las entradas vivas
                for eid in sorted(o.expedientes):
                    x = o.expedientes[eid]
                    if x["estado"] == "AUTORIZADA" and (x.get("orden_entrada") or {}).get("estado") == "ENVIADA":
                        revisar_entrada(o, eid, broker, ahora, forzar_cancelacion=True)
        return {"ok": not dif, "diferencias": dif, "explicadas": expl}
    except ConexionPerdida as e:   # T-29: no poder conciliar también se informa (degrada todo; lo ya encontrado, con su gravedad)
        todo = dif + [{"tipo": "SIN_CONEXION", "ref": None, "detalle": str(e)[:120]}]
        _aviso(o, todo, ahora)
        return {"ok": False, "diferencias": todo, "explicadas": []}
    except Exception as e:   # noqa: BLE001
        todo = dif + [{"tipo": "ERROR", "ref": None, "detalle": type(e).__name__}]
        _aviso(o, todo, ahora)
        return {"ok": False, "diferencias": todo, "explicadas": []}


def _ids_cierre(broker, pid):
    ids = []
    for k in range(1, MAX_INTENTOS):
        oid = f"ORD-{pid}-C-{k}"
        if broker.consultar(oid) is None:
            break
        ids.append(oid)
    return ids


def _en_curso(broker, pid, p, real):
    """Una reducción o un cierre a medias no son discrepancia si lo que tiene el intermediario es exactamente la cantidad
    anotada menos lo que han ejecutado las órdenes de G para esa reducción o ese cierre (nunca una venta ajena)."""
    signo = 1 if p["direccion"] == "LARGO" else -1
    if real * signo <= TOL:
        return None
    if p["estado"] == "REDUCIENDO":
        esperado = p["cantidad"] - _vendido(broker, pid, p["reduccion"]["n"])
        return "REDUCCION_EN_CURSO" if abs(real * signo - esperado) <= TOL else None
    if p["estado"] == "CERRANDO":
        ult = p["reducciones"][-1] if p.get("reducciones") else None
        previo = _vendido(broker, pid, ult["n"]) if ult and ult.get("interrumpida") == "cierre" else 0.0
        cerrado = sum(broker.consultar(x)["cantidad_ejecutada"] for x in _ids_cierre(broker, pid))
        return "CIERRE_EN_CURSO" if abs(real * signo - (p["cantidad"] - previo - cerrado)) <= TOL else None
    return None


def _entrada_en_curso(o, ins, real):
    """Cantidad que el intermediario tiene por una entrada en curso (ejecutada, aún sin conciliar): G la protegerá en su revisión."""
    for e in o.expedientes.values():
        oe = e.get("orden_entrada")
        # solo mientras G aún no la ha visto ejecutada; si ya la anotó y no la protegió, es su fallo y debe verse como discrepancia
        if e["estado"] == "AUTORIZADA" and oe and oe["estado"] == "ENVIADA" and e["propuesta"]["entrada"]["instrumento"] == ins:
            st = [c for c in e["propuesta"]["salida"]["condiciones"] if c["tipo"] == "STOP"][0]
            signo = 1 if st["operador"] in ("<", "<=") else -1
            return real * signo > 0 and abs(real) <= e["control_f"]["cantidad_aprobada"] * (1 + 1e-12)
    return False


def _cierre_previo(broker, base):
    """Última orden de cierre a mercado ya ejecutada (total o parcial) en un intento anterior."""
    ult = None
    for n in range(1, MAX_INTENTOS):
        c = broker.consultar(f"{base}-{n}")
        if c is None:
            break
        if c["cantidad_ejecutada"] > 0:
            ult = c["orden_id"]
    return ult


MAX_INTENTOS = 50   # órdenes de cierre o de reducción por posición (las parciales repetidas consumen identificadores)


def _id_cierre(broker, base, lado, cantidad):
    """Identificador de la siguiente orden de cierre. Se reutiliza el de una orden idéntica que sigue sin ejecutarse
    (reintento tras un fallo); si ya se ejecutó algo o cambió lo que hay que cerrar, se pasa al siguiente intento."""
    for n in range(1, MAX_INTENTOS):
        oid = f"{base}-{n}"
        c = broker.consultar(oid)
        if c is None or (c["estado"] == "ACEPTADA" and c["lado"] == lado and abs(c["cantidad"] - cantidad) <= TOL):
            return oid
    raise ValueError("demasiados intentos de cierre")


def cerrar(o, posicion_id, broker, ahora, actor="G", condicion=None, motivo=None):
    """Cierra una posición abierta: pasa a CERRANDO (el Orquestador valida quién y por qué), cierra la posición neta real
    en el intermediario, retira el stop, comprueba que no queda nada y solo entonces pasa a CERRADA.
    Si algo falla, la posición queda en CERRANDO y a la vista; repetir la llamada es seguro."""
    p = o.posiciones.get(posicion_id) if isinstance(posicion_id, str) else None
    if p is None or p["estado"] not in ("ABIERTA", "EN_REVISION", "CERRANDO", "REDUCIENDO"):
        return _r(False, "G-06", "la posición no existe o no se puede cerrar en su estado")
    if not o.posicion_integra(posicion_id):   # también al retomar un cierre: nada se envía con un estado alterado
        return _r(False, "G-06", "O-13: el estado de control de la posición no es íntegro; no se envía nada")
    if o.ultimo_ahora and _dt(ahora) < _dt(o.ultimo_ahora):
        return _r(False, "G-06", "el instante recibido es anterior al último que vio el Orquestador; no se envía nada")
    plano = False
    if p["estado"] == "REDUCIENDO":   # plano en el intermediario (un stop saltó): se termina directamente como cierre
        try:
            plano = abs(_neto(broker, p["instrumento"])) <= TOL
        except Exception as ex:   # noqa: BLE001
            return _r(False, "G-01", f"sin conexión con el intermediario ({type(ex).__name__})")
    if not plano and p["estado"] != "CERRANDO":
        t = o.posicion_transicion(posicion_id, "CERRANDO", actor, ahora, condicion=condicion, motivo=motivo)
        if not t["ok"]:
            return _r(False, "G-06", f"el Orquestador no admite el cierre ({t['codigo']}): {t['motivo']}")
    est = {"enviado": False}
    try:
        return _cerrar(o, p, posicion_id, broker, ahora, est)
    except ConexionPerdida as ex:
        if not est["enviado"]:
            return _r(False, "G-01", f"sin conexión con el intermediario; la posición sigue CERRANDO y se puede reintentar ({ex})")
        return _incierto(o, posicion_id, ahora, "ConexionPerdida al cerrar")
    except Exception as ex:   # noqa: BLE001
        return _incierto(o, posicion_id, ahora, f"{type(ex).__name__} al cerrar") if est["enviado"] else _incompleto(o, posicion_id, ahora, f"{type(ex).__name__} al preparar el cierre")


def _incompleto(o, pid, ahora, causa):
    reg = _aviso(o, [{"tipo": "CIERRE_INCOMPLETO", "ref": pid, "detalle": causa}], ahora)
    return _r(False, "G-09", f"cierre no completado ({causa}); la posición sigue CERRANDO.", aviso_registrado=reg)


def _neto(broker, ins):
    return {x["instrumento"]: x["cantidad"] for x in broker.posiciones()}.get(ins, 0.0)


def _minimo_vivo(p):
    """Lo mínimo que el intermediario puede tener de la posición sin que sea una diferencia: lo que deja una reducción en curso
    o interrumpida por el cierre; si no, la cantidad anotada."""
    if p.get("reduccion"):
        return p["reduccion"]["objetivo_restante"]
    ult = p["reducciones"][-1] if p.get("reducciones") else None
    if p["estado"] == "CERRANDO" and ult and ult.get("interrumpida") == "cierre":
        return ult["objetivo_restante"]
    return p["cantidad"]


def _cerrar(o, p, pid, broker, ahora, est):
    """Lleva a cero la posición neta REAL del intermediario sobre el instrumento, sea cual sea su sentido o cantidad
    (si un stop saltó a mitad del cierre, la orden a mercado puede haber abierto la posición contraria: también se cierra)."""
    ins = p["instrumento"]
    base = f"ORD-{pid}-C"
    neto = _neto(broker, ins)
    minimo = _minimo_vivo(p)   # a media reducción (o en un cierre que la interrumpió) vale lo ya reducido
    if abs(neto) > TOL and ((neto > 0) != (p["direccion"] == "LARGO") or abs(neto) > p["cantidad"] + TOL or abs(neto) < minimo - TOL):
        _aviso(o, [{"tipo": "DIFERENCIA_AL_CERRAR", "ref": pid, "detalle": f"el Orquestador tiene {p['cantidad']} y el intermediario {neto}; se cierra lo que hay"}], ahora)
    for _ in range(4):
        if abs(neto) <= TOL:
            break
        lado, cant = ("VENTA" if neto > 0 else "COMPRA"), abs(neto)
        id_c = _id_cierre(broker, base, lado, cant)
        est["enviado"] = True
        r = broker.enviar({"orden_id": id_c, "instrumento": ins, "activo_base": p["activo_base"], "tipo": "MERCADO", "lado": lado, "cantidad": cant,
                           "solo_reduccion": True, "via_acceso": p.get("via_acceso")})   # si el stop salta entre medias, no abre la posición contraria
        if r["estado"] in ("ACEPTADA", "PARCIAL"):   # el resto de una parcial no se deja vivo
            broker.cancelar(id_c)
        neto = _neto(broker, ins)
    if abs(neto) > TOL:
        return _incompleto(o, pid, ahora, f"tras varios intentos el intermediario aún tiene {neto} sobre {ins}")
    stops = _stops_de(broker, pid, p)   # los vigentes y los que una reducción a medias dejó en el intermediario
    orden_id = _cierre_previo(broker, base)
    if orden_id is None:
        ejec = [x for x in stops if (c := broker.consultar(x)) and c["estado"] in ("EJECUTADA", "PARCIAL")]
        if not ejec:
            return _incompleto(o, pid, ahora, "la posición ya no está en el intermediario y ninguna orden la explica")
        orden_id = ejec[0]
    est["enviado"] = True
    for _ in range(3):
        for x in stops:
            broker.cancelar(x)
        vivos = [x for x in stops if (c := broker.consultar(x)) and c["estado"] == "ACEPTADA"]
        if not vivos:
            break
    if vivos:
        return _incompleto(o, pid, ahora, f"no se pudo retirar el stop {vivos[0]}")
    t = o.posicion_transicion(pid, "CERRADA", "G", ahora, restante=0, orden={"orden_id": orden_id, "conciliada": True})
    if not t["ok"]:
        return _incompleto(o, pid, ahora, f"el Orquestador rechazó el cierre ({t['codigo']})")
    return _r(True, "OK", "posición cerrada y conciliada", orden_id=orden_id)


def _ids_reduccion(broker, pid, n, tipo):
    """Órdenes que G envió al intermediario para la reducción n (tipo M: a mercado; S: stops redimensionados)."""
    ids = []
    for k in range(1, MAX_INTENTOS):
        oid = f"ORD-{pid}-R{n}-{tipo}-{k}"
        if broker.consultar(oid) is None:
            break
        ids.append(oid)
    return ids


def _stops_de(broker, pid, p):
    """Stops de la posición: los vigentes y los de cualquier reducción (terminada o a medias)."""
    ns = [r["n"] for r in p.get("reducciones", [])] + ([p["reduccion"]["n"]] if p.get("reduccion") else [])
    return list(p["protecciones"]) + [x for n in ns for x in _ids_reduccion(broker, pid, n, "S") if x not in p["protecciones"]]


def _id_stop(broker, base, lado, cantidad, precio):
    """Stop redimensionado: se reutiliza el que ya esté vivo con lo pedido (reintento); si no, el primer identificador libre."""
    for k in range(1, 10):
        oid = f"{base}-{k}"
        c = broker.consultar(oid)
        if c is None or (c["estado"] == "ACEPTADA" and c["lado"] == lado and abs(c["cantidad"] - cantidad) <= TOL and c["precio"] == precio):
            return oid
    raise ValueError("demasiados intentos de stop")


def reducir(o, posicion_id, broker, ahora, cantidad=None, actor="G", condicion=None, motivo=None):
    """Reduce una posición (T-12). Pasa a REDUCIENDO (el Orquestador valida quién, cuánto y por qué), vende a mercado
    con órdenes de solo reducción hasta la cantidad pedida, pone un stop nuevo del tamaño de lo que queda, retira el
    anterior y solo entonces vuelve a su estado (ABIERTA, o EN_REVISION si la tesis estaba en revisión). El stop anterior es de solo reducción: mientras tanto cubre la posición
    entera y no puede abrir la contraria. Repetir la llamada retoma la reducción en curso.
    Códigos: OK; G-01 sin conexión antes de enviar; G-06 no admitida; G-08 estado incierto; G-12 reducción no completada
    (sigue REDUCIENDO y a la vista); si el intermediario ya está plano, se termina como un cierre."""
    p = o.posiciones.get(posicion_id) if isinstance(posicion_id, str) else None
    if p is None or p["estado"] not in ("ABIERTA", "EN_REVISION", "REDUCIENDO"):
        return _r(False, "G-06", "la posición no existe o no se puede reducir en su estado")
    if o.ultimo_ahora and _dt(ahora) < _dt(o.ultimo_ahora):
        return _r(False, "G-06", "el instante recibido es anterior al último que vio el Orquestador; no se envía nada")
    if not o.posicion_integra(posicion_id):   # también al retomar: nada se envía con un estado alterado
        return _r(False, "G-06", "O-13: el estado de control de la posición no es íntegro; no se envía nada")
    if p["estado"] == "REDUCIENDO":
        if cantidad is not None and not (_num(cantidad) and abs(cantidad - p["reduccion"]["cantidad"]) <= TOL):
            return _r(False, "G-06", "ya hay una reducción en curso de otra cantidad: se termina esa antes")
    else:
        t = o.posicion_transicion(posicion_id, "REDUCIENDO", actor, ahora, condicion=condicion, motivo=motivo, cantidad=cantidad)
        if not t["ok"]:
            return _r(False, "G-06", f"el Orquestador no admite la reducción ({t['codigo']}): {t['motivo']}")
    est = {"enviado": False}
    try:
        return _reducir(o, p, posicion_id, broker, ahora, est)
    except ConexionPerdida as ex:
        if not est["enviado"]:
            return _r(False, "G-01", f"sin conexión con el intermediario; la posición sigue REDUCIENDO y se puede reintentar ({ex})")
        return _incierto(o, posicion_id, ahora, "ConexionPerdida al reducir")
    except Exception as ex:   # noqa: BLE001
        if est["enviado"]:
            return _incierto(o, posicion_id, ahora, f"{type(ex).__name__} al reducir")
        return _red_incompleta(o, posicion_id, ahora, f"{type(ex).__name__} al preparar la reducción")


def _vendido(broker, pid, n):
    """Lo que han ejecutado las ventas (o compras, en un corto) de la reducción n."""
    return sum(broker.consultar(x)["cantidad_ejecutada"] for x in _ids_reduccion(broker, pid, n, "M"))


def _red_incompleta(o, pid, ahora, causa):
    reg = _aviso(o, [{"tipo": "REDUCCION_INCOMPLETA", "ref": pid, "detalle": causa}], ahora)
    return _r(False, "G-12", f"reducción no completada ({causa}); la posición sigue REDUCIENDO con su stop anterior.", aviso_registrado=reg)


def _reducir(o, p, pid, broker, ahora, est):
    red = p["reduccion"]
    ins, largo = p["instrumento"], p["direccion"] == "LARGO"
    signo, lado = (1, "VENTA") if largo else (-1, "COMPRA")
    objetivo = red["objetivo_restante"]
    base_m, base_s = f"ORD-{pid}-R{red['n']}-M", f"ORD-{pid}-R{red['n']}-S"
    neto = _neto(broker, ins) * signo   # cantidad en el sentido de la posición
    esperado = p["cantidad"] - _vendido(broker, pid, red["n"])
    if abs(neto) > TOL and abs(neto - esperado) > TOL:   # algo ajeno a esta reducción movió la posición: no se vende a ciegas
        _aviso(o, [{"tipo": "DIFERENCIA_AL_REDUCIR", "ref": pid, "detalle": f"el intermediario tiene {neto * signo} y lo esperado es {esperado * signo}"}], ahora)
        return _red_incompleta(o, pid, ahora, f"el intermediario tiene {neto * signo} y, con lo vendido por la reducción, debería tener {esperado * signo}")
    for _ in range(4):
        if neto - objetivo <= TOL or neto <= TOL:
            break
        falta = neto - objetivo
        oid = _id_cierre(broker, base_m, lado, falta)
        est["enviado"] = True
        r = broker.enviar({"orden_id": oid, "instrumento": ins, "activo_base": p["activo_base"], "tipo": "MERCADO", "lado": lado,
                           "cantidad": falta, "solo_reduccion": True, "via_acceso": p.get("via_acceso")})
        if r["estado"] in ("ACEPTADA", "PARCIAL"):   # el resto de una parcial no se deja vivo: podría ejecutarse después
            broker.cancelar(oid)
        neto = _neto(broker, ins) * signo
    if abs(neto) <= TOL:   # un stop la cerró entera mientras tanto: se termina como cierre
        return cerrar(o, pid, broker, ahora)
    if neto < 0:
        return _red_incompleta(o, pid, ahora, f"el intermediario tiene la posición en sentido contrario ({neto * signo})")
    if neto - objetivo > TOL:   # no se llegó: el stop anterior (solo reducción) sigue cubriendo todo
        return _red_incompleta(o, pid, ahora, f"tras varios intentos quedan {neto} y el objetivo es {objetivo}")
    if neto < objetivo - TOL:
        _aviso(o, [{"tipo": "DIFERENCIA_AL_REDUCIR", "ref": pid, "detalle": f"se pidió dejar {objetivo} y el intermediario tiene {neto}; se protege lo que hay"}], ahora)
    # stop nuevo del tamaño de lo que queda, ANTES de retirar el anterior; si la posición cambia entre medias, otra vuelta
    for _ in range(3):
        sid = _id_stop(broker, base_s, lado, neto, p["stop_precio"])
        est["enviado"] = True
        s = broker.enviar({"orden_id": sid, "instrumento": ins, "activo_base": p["activo_base"], "tipo": "STOP", "lado": lado,
                           "cantidad": neto, "precio": p["stop_precio"], "solo_reduccion": True, "via_acceso": p.get("via_acceso")})
        if s["estado"] == "EJECUTADA" and abs(_neto(broker, ins)) <= TOL:   # el precio ya había cruzado el stop
            return cerrar(o, pid, broker, ahora)
        if s["estado"] != "ACEPTADA":
            return _red_incompleta(o, pid, ahora, f"el intermediario no aceptó el stop redimensionado ({s['estado']})")
        sobran = [x for x in _stops_de(broker, pid, p) if x != sid]
        for _ in range(3):
            for x in sobran:
                broker.cancelar(x)
            vivos = [x for x in sobran if (c := broker.consultar(x)) and c["estado"] == "ACEPTADA"]
            if not vivos:
                break
        if vivos:
            return _red_incompleta(o, pid, ahora, f"no se pudo retirar el stop {vivos[0]} (es de solo reducción: no abre la posición contraria)")
        ahora_neto = _neto(broker, ins) * signo
        if abs(ahora_neto) <= TOL:
            return cerrar(o, pid, broker, ahora)
        if abs(ahora_neto - neto) <= TOL:
            break
        neto = ahora_neto
    else:
        return _red_incompleta(o, pid, ahora, "la posición cambió mientras se redimensionaba el stop")
    chk = broker.consultar(sid)
    if not (chk and chk["estado"] == "ACEPTADA" and abs(chk["cantidad"] - neto) <= TOL and chk["precio"] == p["stop_precio"]):
        return _red_incompleta(o, pid, ahora, "el intermediario no confirma el stop redimensionado")
    orden_id = _cierre_previo(broker, base_m)
    if orden_id is None:
        ejec = [x for x in _stops_de(broker, pid, p) if (c := broker.consultar(x)) and c["estado"] in ("EJECUTADA", "PARCIAL")]
        if not ejec:
            return _red_incompleta(o, pid, ahora, "ninguna orden del intermediario explica la reducción")
        orden_id = ejec[0]
    t = o.posicion_transicion(pid, red["vuelve_a"], "G", _instante(o, ahora), restante=neto, orden={"orden_id": orden_id, "conciliada": True},
                              protecciones=[sid])
    if not t["ok"]:
        return _red_incompleta(o, pid, ahora, f"el Orquestador rechazó la reducción ({t['codigo']}: {t['motivo'][:80]})")
    return _r(True, "OK", "posición reducida, stop redimensionado y conciliado", orden_id=orden_id, restante=neto, stop_id=sid)


def _cuadra(x, y):
    return _num(x) and _num(y) and abs(x - y) <= 1e-6 * max(1.0, abs(y))


def declarar_manual(o, registro, broker, ahora):
    """Entrada de CT-G-14: antes de registrar lo que el operador declara, G lo contrasta con el intermediario.
    Códigos: OK y los del Orquestador; G-01 sin conexión; G-10 lo declarado no cuadra con el intermediario."""
    if not isinstance(registro, dict):
        return _r(False, "G-10", "el registro no es un objeto")
    plano = aplanar_manual(registro)   # T-47: CT-G-14 0.2.0
    # antes de consultar o tocar el intermediario, el Orquestador dice (sin efectos) si lo rechazaría; si es así, decide él
    # con sus efectos de diseño (duplicado, integridad) y G no cancela ni consulta nada
    if plano is None or o.comprobar_manual(registro, _instante(o, ahora)) is not None:
        return o.registrar_manual(registro, _instante(o, ahora))
    try:
        v = plano.get("vinculo") if isinstance(plano.get("vinculo"), dict) else {}
        c = broker.consultar(plano.get("ref_intermediario")) if isinstance(plano.get("ref_intermediario"), str) else None
        if not (c and c["estado"] in ("EJECUTADA", "PARCIAL") and c.get("instrumento") == plano.get("instrumento")
                and c["lado"] == plano.get("lado") and _cuadra(c["cantidad_ejecutada"], plano.get("cantidad"))
                and _cuadra(c["precio_medio"], plano.get("precio"))
                and (v.get("tipo") == "LIBRE" or via_norm(c.get("via_acceso")) == via_norm(plano.get("via_acceso")))):
            return _r(False, "G-10", "el intermediario no tiene esa orden ejecutada con ese instrumento, sentido, cantidad, precio y vía de acceso")
        if v.get("tipo") == "EXPEDIENTE":
            e = o.expedientes.get(v.get("id"))
            s = broker.consultar(plano.get("proteccion_ref")) if isinstance(plano.get("proteccion_ref"), str) else None
            stop = next((x for x in e["propuesta"]["salida"]["condiciones"] if x["tipo"] == "STOP"), None) if e and e.get("propuesta") else None
            lado_s = "VENTA" if plano.get("lado") == "COMPRA" else "COMPRA"
            if not (s and stop and s["estado"] == "ACEPTADA" and s["tipo"] == "STOP" and s["lado"] == lado_s and s.get("instrumento") == plano.get("instrumento")
                    and via_norm(s.get("via_acceso")) == via_norm(plano.get("via_acceso"))
                    and _cuadra(s["cantidad"], plano.get("cantidad")) and s["precio"] == stop["umbral"]):
                return _r(False, "G-10", "la orden de protección no está viva en el intermediario o no es el stop de la propuesta")
        elif v.get("tipo") == "POSICION":
            p = o.posiciones.get(v.get("id"))
            if p is None:
                return _r(False, "G-10", "la posición no existe")
            if not o.posicion_integra(v["id"]):
                return _r(False, "G-10", "O-13: el estado de control de la posición no es íntegro")
            stops = _stops_de(broker, v["id"], p)
            for prot in stops:
                s = broker.consultar(prot)
                if s and s["estado"] in ("EJECUTADA", "PARCIAL") and prot in p["protecciones"]:
                    return _r(False, "G-10", "el stop ya se ejecutó: el cierre lo concilia H (H-01), no un registro manual")
            # antes de tocar ningún stop: si el intermediario aún tiene cantidad, no es un cierre total y la posición sigue protegida
            if abs(_neto(broker, p["instrumento"])) > TOL:
                return _r(False, "G-10", "el intermediario aún tiene cantidad en ese instrumento: el cierre no es total")
            for prot in stops:
                s = broker.consultar(prot)
                for _ in range(3):
                    if not (s and s["estado"] == "ACEPTADA"):
                        break
                    s = broker.cancelar(prot)
                if s and s["estado"] == "ACEPTADA":
                    return _r(False, "G-10", f"no se pudo cancelar el stop {prot}: la posición no se da por cerrada")
        r = o.registrar_manual(registro, _instante(o, ahora))
        return r
    except ConexionPerdida as ex:
        return _r(False, "G-01", f"sin conexión con el intermediario: no se registra nada ({ex})")
    except Exception as ex:   # noqa: BLE001
        return _r(False, "G-10", f"no se pudo contrastar con el intermediario ({type(ex).__name__})")
