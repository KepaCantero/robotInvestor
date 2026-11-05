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

from control_f import ERRORES
from validar_sobre import _dt

ID = re.compile(r"^[A-Za-z0-9._:/-]{1,64}\Z")
TOL = 1e-6


class ConexionPerdida(Exception):
    pass


def _num(x, minimo=None):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) and (minimo is None or x > minimo)


class BrokerSimulado:
    """Intermediario de pruebas: precios fijos, ejecución completa o parcial, y fallos a demanda."""

    def __init__(self, capital_eur, precios, hora_datos, fraccion_fill=1.0, rechaza_stops=False, caido=False, rechaza_mercado=False):
        self.capital_eur, self.precios, self.hora_datos = capital_eur, dict(precios), hora_datos
        self.fraccion_fill, self.rechaza_stops, self.caido, self.rechaza_mercado = fraccion_fill, rechaza_stops, caido, rechaza_mercado
        self.ordenes, self.pos, self.perdida_dia_eur = {}, {}, 0.0

    def enviar(self, o):
        if self.caido:
            raise ConexionPerdida("sin conexión con el intermediario")
        ok = (isinstance(o, dict) and isinstance(o.get("orden_id"), str) and ID.match(o["orden_id"]) and o.get("tipo") in ("LIMITE", "MERCADO", "STOP")
              and o.get("lado") in ("COMPRA", "VENTA") and isinstance(o.get("instrumento"), str) and isinstance(o.get("activo_base"), str)
              and _num(o.get("cantidad"), 0) and (o["tipo"] == "MERCADO" or _num(o.get("precio"), 0)))
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
            signo = 1 if o["lado"] == "VENTA" else -1   # un stop de venta protege un largo
            tiene = self.pos.get(o["instrumento"], {"cantidad": 0.0})["cantidad"] * signo
            if self.rechaza_stops or tiene + TOL < o["cantidad"]:
                reg["estado"] = "RECHAZADA"
        else:
            sale = o["tipo"] == "MERCADO" or (o["lado"] == "COMPRA" and p <= o["precio"]) or (o["lado"] == "VENTA" and p >= o["precio"])
            if sale:
                q = o["cantidad"] * (self.fraccion_fill if o["tipo"] == "LIMITE" else 1.0)   # solo las entradas pueden ejecutarse a medias
                self._fill(o, q, p)
                reg["ejecutada"], reg["precio_medio"] = q, p
                reg["estado"] = "EJECUTADA" if q >= o["cantidad"] - TOL else "PARCIAL"
        return self._res(reg)

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
                signo = 1 if x["lado"] == "VENTA" else -1
                if self.pos.get(x["instrumento"], {"cantidad": 0.0})["cantidad"] * signo + TOL < x["cantidad"]:
                    r["estado"] = "CANCELADA"

    @staticmethod
    def _res(reg):
        o = reg["orden"]
        return {"orden_id": o["orden_id"], "estado": reg["estado"], "cantidad_ejecutada": reg["ejecutada"], "precio_medio": reg["precio_medio"],
                "tipo": o["tipo"], "lado": o["lado"], "cantidad": o["cantidad"], "precio": o.get("precio")}

    def cancelar(self, orden_id):
        if self.caido:
            raise ConexionPerdida("sin conexión con el intermediario")
        r = self.ordenes.get(orden_id)
        if r is not None and r["estado"] == "ACEPTADA":
            r["estado"] = "CANCELADA"
        return self._res(r) if r else None

    def consultar(self, orden_id):
        if self.caido:
            raise ConexionPerdida("sin conexión con el intermediario")
        r = self.ordenes.get(orden_id)
        return self._res(r) if r else None

    def posiciones(self):
        if self.caido:
            raise ConexionPerdida("sin conexión con el intermediario")
        return [{"instrumento": k, "activo_base": v["activo_base"], "cantidad": v["cantidad"]} for k, v in sorted(self.pos.items())]


def cartera_para_f(broker):
    """El estado de cartera que F necesita, tomado del intermediario y no de quien emite el informe."""
    pos = broker.posiciones()
    return {"fecha_hora": broker.hora_datos, "capital_eur": broker.capital_eur, "perdida_dia_eur": broker.perdida_dia_eur,
            "posiciones": [{"instrumento": p["instrumento"], "activo_base": p["activo_base"],
                            "valor_eur": abs(p["cantidad"]) * broker.precios[p["instrumento"]]} for p in pos]}


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


def _id_entrada(broker, base, instrumento):
    """Identificador de la orden de entrada. Se reanuda la anterior solo si dejó una posición viva en el intermediario
    (un reintento tras un fallo no duplica ni deja huérfana la posición); si ya se cerró, se empieza una nueva."""
    viva = {p["instrumento"] for p in broker.posiciones()}
    for n in range(1, 6):
        oid = f"{base}-{n}"
        c = broker.consultar(oid)
        if c is None:
            return oid, False
        if c["estado"] == "ACEPTADA" or (c["cantidad_ejecutada"] > 0 and instrumento in viva):
            return oid, c["cantidad_ejecutada"] > 0
    raise ValueError("demasiados intentos de entrada")


def ejecutar(o, expediente_id, broker, ahora):
    """Ejecuta una propuesta AUTORIZADA. No lanza excepciones. Códigos: OK; G-01 (intermediario inalcanzable antes de enviar nada);
    G-02 (sin ejecución); G-03 (protección fallida: se cerró); G-04 (CRÍTICO: queda posición sin proteger);
    G-05 (el Orquestador rechazó lo ejecutado: se cerró); G-06 (no ejecutable: no se envió nada);
    G-08 (fallo con órdenes ya enviadas: estado incierto, hay que conciliar)."""
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
    a = _dt(ahora)
    cf, en = e["control_f"], e["propuesta"]["entrada"]
    if o.ultimo_ahora and a < _dt(o.ultimo_ahora):
        return _r(False, "G-06", "el instante recibido es anterior al último que vio el Orquestador; no se envía nada")
    if a > min(_dt(en["ventana_hasta"]), _dt(e["sobre"]["valid_until"]), _dt(cf["valid_until"])) or o._sello_anulado(e):
        return _r(False, "G-06", "la ventana de entrada, el sobre, el informe de F o el sello ya no valen; no se envía nada")
    id_e, reanuda = _id_entrada(broker, f"ORD-{eid}-E", en["instrumento"])
    if any(p["instrumento"] == en["instrumento"] and p["estado"] != "CERRADA" for p in o.posiciones.values()) \
            or (not reanuda and any(p["instrumento"] == en["instrumento"] for p in broker.posiciones())):
        return _r(False, "G-06", "ya hay una posición sobre ese instrumento; en esta versión solo se admite una por instrumento")
    st = [c for c in e["propuesta"]["salida"]["condiciones"] if c["tipo"] == "STOP"][0]
    largo = st["operador"] in ("<", "<=")
    lado_e, lado_s = ("COMPRA", "VENTA") if largo else ("VENTA", "COMPRA")
    base = {"instrumento": en["instrumento"], "activo_base": en["activo_base"]}
    est["enviado"] = True
    r = broker.enviar({**base, "orden_id": id_e, "tipo": "LIMITE", "lado": lado_e, "cantidad": cf["cantidad_aprobada"], "precio": en["limite"]})
    fq = r["cantidad_ejecutada"] if r["estado"] in ("EJECUTADA", "PARCIAL") else 0.0
    if r["estado"] == "ACEPTADA":
        broker.cancelar(id_e)   # lo que no se ha ejecutado no se deja vivo
        r2 = broker.consultar(id_e)
        if r2["estado"] != "CANCELADA" and r2["cantidad_ejecutada"] <= 0:
            return _incierto(o, eid, ahora, "la orden de entrada no se pudo cancelar")
        fq = r2["cantidad_ejecutada"]
    if fq <= 0:
        return _r(False, "G-02", f"sin ejecución ({r['estado']}); nada que reportar al Orquestador")
    precio = r["precio_medio"]
    id_s = _id_libre(broker, f"ORD-{eid}-S", reutilizable=False)

    def deshacer(codigo, motivo):
        """Cierra lo que el intermediario tenga realmente sobre el instrumento (no lo que G cree). Si no puede: aviso CRÍTICO."""
        try:
            broker.cancelar(id_s)
            neto = {p["instrumento"]: p["cantidad"] for p in broker.posiciones()}.get(en["instrumento"], 0.0)
            if abs(neto) > TOL:
                id_x = _id_libre(broker, f"ORD-{eid}-X", reutilizable=True)
                broker.enviar({**base, "orden_id": id_x, "tipo": "MERCADO", "lado": "VENTA" if neto > 0 else "COMPRA", "cantidad": abs(neto)})
            resto = {p["instrumento"]: p["cantidad"] for p in broker.posiciones()}.get(en["instrumento"], 0.0)
            vivo = broker.consultar(id_s)
        except Exception as ex:   # noqa: BLE001
            return _incierto(o, eid, ahora, f"{type(ex).__name__} al deshacer: {motivo}")
        if abs(resto) <= TOL and (vivo is None or vivo["estado"] != "ACEPTADA"):
            reg = _aviso(o, [{"tipo": "POSICION_CERRADA_POR_G", "ref": eid, "detalle": motivo}], ahora)
            return _r(False, codigo, motivo + " No queda posición ni stop vivos.", cerrada=True, aviso_registrado=reg)
        reg = _aviso(o, [{"tipo": "POSICION_SIN_PROTEGER", "ref": eid, "detalle": motivo + " Y no se pudo cerrar."}], ahora)
        return _r(False, "G-04", "CRÍTICO: " + motivo + " La posición no se pudo cerrar.", cerrada=False, aviso_registrado=reg)

    s = broker.enviar({**base, "orden_id": id_s, "tipo": "STOP", "lado": lado_s, "cantidad": fq, "precio": st["umbral"]})
    if s["estado"] != "ACEPTADA":
        return deshacer("G-03", f"el intermediario no aceptó el stop ({s['estado']}).")
    pos = {p["instrumento"]: p for p in broker.posiciones()}
    p = pos.get(en["instrumento"])
    chk = broker.consultar(id_s)
    if not (p and abs(abs(p["cantidad"]) - fq) <= TOL and (p["cantidad"] > 0) == largo and chk and chk["estado"] == "ACEPTADA"):
        return deshacer("G-03", "el intermediario no confirma la posición y su stop.")
    res = o.ejecutar(eid, {"orden_id": id_e, "cantidad": fq, "precio": precio, "conciliada": True, "proteccion_orden_ids": [id_s]}, "G", ahora)
    if not res["ok"]:
        return deshacer("G-05", f"el Orquestador rechazó la ejecución ({res['codigo']}: {res['motivo'][:80]}).")
    return _r(True, "OK", "ejecutada y conciliada", posicion_id=res.get("posicion_id"), cantidad=fq, precio=precio)


def conciliar(o, broker, ahora):
    """Compara lo que el Orquestador cree con lo que dice el intermediario (cantidad, sentido, activo y stop) e informa de las diferencias."""
    try:
        dif = []
        reales = {p["instrumento"]: p for p in broker.posiciones()}
        conocidas = set()
        for pid, p in o.posiciones.items():
            if p["estado"] == "CERRADA":
                for prot in p["protecciones"]:   # un stop vivo de una posición cerrada abriría una posición contraria
                    c = broker.consultar(prot)
                    if c and c["estado"] == "ACEPTADA":
                        dif.append({"tipo": "PROTECCION_HUERFANA", "ref": pid, "detalle": f"la orden {prot} sigue viva con la posición cerrada"})
                continue
            conocidas.add(p["instrumento"])
            r = reales.get(p["instrumento"])
            if r is None or abs(abs(r["cantidad"]) - p["cantidad"]) > TOL:
                dif.append({"tipo": "CANTIDAD", "ref": pid, "detalle": f"Orquestador {p['cantidad']}, intermediario {abs(r['cantidad']) if r else 0}"})
            elif (r["cantidad"] > 0) != (p["direccion"] == "LARGO") or r["activo_base"] != p["activo_base"]:
                dif.append({"tipo": "SENTIDO_O_ACTIVO", "ref": pid, "detalle": "el sentido o el activo base no coinciden con el intermediario"})
            lado_s = "VENTA" if p["direccion"] == "LARGO" else "COMPRA"
            for prot in p["protecciones"]:
                c = broker.consultar(prot)
                if not c or c["estado"] != "ACEPTADA":
                    dif.append({"tipo": "PROTECCION", "ref": pid, "detalle": f"la orden de protección {prot} no está viva ({c['estado'] if c else 'inexistente'})"})
                elif not (c["tipo"] == "STOP" and c["lado"] == lado_s and abs(c["cantidad"] - p["cantidad"]) <= TOL and c["precio"] == p["stop_precio"]):
                    dif.append({"tipo": "PROTECCION", "ref": pid, "detalle": f"el stop {prot} no coincide con la posición (tipo, lado, cantidad o precio)"})
        for ins in sorted(set(reales) - conocidas):
            dif.append({"tipo": "POSICION_DESCONOCIDA", "ref": ins, "detalle": "el intermediario tiene una posición que el Orquestador no conoce"})
        if dif:
            _aviso(o, dif, ahora)
        return {"ok": not dif, "diferencias": dif}
    except ConexionPerdida as e:
        return {"ok": False, "diferencias": [{"tipo": "SIN_CONEXION", "ref": None, "detalle": str(e)}]}
    except Exception as e:   # noqa: BLE001
        return {"ok": False, "diferencias": [{"tipo": "ERROR", "ref": None, "detalle": type(e).__name__}]}
