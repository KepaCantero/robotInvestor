"""Orquestador — código de referencia V0.1 (máquina de estados de expedientes y posiciones).

Determinista: sin LLM, sin red, sin reloj propio (el tiempo entra por el parámetro `ahora`).
Falla cerrado: cada operación devuelve {"ok", "codigo", "motivo", ...}; ante cualquier error
rechaza, restaura el estado y no lanza excepciones. Solo el Orquestador cambia estados.
Todos los valores numéricos de la configuración son de partida [PROPUESTO].
"""
from __future__ import annotations

import copy
import functools
import hashlib
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from k_calidad import (Calendario, ERRORES, SinCobertura, estado_sello, hash_serie,  # noqa: E402
                       validar_sello)
from validar_encargo import sobre_responde_a_encargo, validar_encargo  # noqa: E402
from validar_sobre import _dt  # noqa: E402
from manual_g import neto_libre, validar_manual  # noqa: E402
from comparador import MARGEN_AJUSTADO, REFERENCIA_EFECTIVO, _referencia_ok, comparar_candidatos  # noqa: E402
from dimensionado import dimensionar  # noqa: E402
from validar_contradictor import validar_informe  # noqa: E402
from control_f import POLITICA_DEFECTO, controlar, politica_valida, validar_informe_f  # noqa: E402

VERSION_REGLAS = "ORQ-0.1.0"
_FH = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})\Z")
_ID = re.compile(r"^[A-Za-z0-9._:/-]{1,64}\Z")
GESTORES = {"GESTOR_TRADING", "GESTOR_TACTICA", "GESTOR_LARGO_PLAZO"}
EMISORES = {"BROKER"} | GESTORES
DECISORES = EMISORES | {"OPERADOR"}
TERMINALES = {"DESCARTADA", "EJECUTADA"}

# (desde, hasta) -> actores que pueden pedirla
T = {}
for _e in ("DETECTADA", "EN_OBSERVACION", "CADUCADA"):
    T[(_e, "EN_ANALISIS")] = EMISORES
T[("EN_ANALISIS", "EN_ANALISIS")] = EMISORES          # reintento tras encargo incompleto, caducado o anulado
T[("EN_ANALISIS", "VALIDADA")] = {"C"}
T[("VALIDADA", "COMPARADA")] = {"D"}
T[("COMPARADA", "COMPARADA")] = {"D"}   # al llegar candidatos nuevos se vuelve a comparar con todos
T[("COMPARADA", "PROPUESTA")] = EMISORES
T[("PROPUESTA", "AUTORIZADA")] = {"OPERADOR", "MATRIZ_AUTONOMIA"}
T[("AUTORIZADA", "EJECUTADA")] = {"G"}
for _e in ("DETECTADA", "EN_ANALISIS", "VALIDADA", "COMPARADA", "PROPUESTA"):
    T[(_e, "EN_OBSERVACION")] = DECISORES | {"D"}
for _e in ("DETECTADA", "EN_ANALISIS", "VALIDADA", "COMPARADA", "PROPUESTA", "AUTORIZADA", "EN_OBSERVACION", "CADUCADA"):
    T[(_e, "DESCARTADA")] = DECISORES
for _e in ("VALIDADA", "COMPARADA", "PROPUESTA", "AUTORIZADA"):
    T[(_e, "CADUCADA")] = {"ORQUESTADOR"}

TP = {  # posiciones
    ("ABIERTA", "EN_REVISION"): {"H", "ORQUESTADOR"},
    ("EN_REVISION", "ABIERTA"): EMISORES | {"OPERADOR"},
    ("ABIERTA", "REDUCIENDO"): {"F", "G", "ORQUESTADOR", "OPERADOR"},
    ("ABIERTA", "CERRANDO"): {"F", "G", "ORQUESTADOR", "OPERADOR"},
    ("EN_REVISION", "REDUCIENDO"): {"F", "G", "ORQUESTADOR", "OPERADOR"},
    ("EN_REVISION", "CERRANDO"): {"F", "G", "ORQUESTADOR", "OPERADOR"},
    ("REDUCIENDO", "ABIERTA"): {"G"},
    ("REDUCIENDO", "CERRADA"): {"G"},
    ("CERRANDO", "CERRADA"): {"G"},
}
OPERADORES = {"<": lambda v, u: v < u, "<=": lambda v, u: v <= u, ">": lambda v, u: v > u,
              ">=": lambda v, u: v >= u, "==": lambda v, u: v == u}

CONFIG_DEFECTO = {"max_reintentos": 3, "umbral_corte_comun_dias_habiles": 0,
                  "dia_coste_max_eur": 50.0, "dia_tiempo_max_min": 600, "tolerancia_precio_entrada": 0.05,
                  "exige_contradictor_en": [], "matriz_autonomia": {}, "politica_f": POLITICA_DEFECTO,
                  "nivel_autonomia": {}, "tolerancia_conciliacion_rel": 0.0, "instrumentos_permitidos": None,
                  "referencias": {c: dict(REFERENCIA_EFECTIVO) for c in ("TRADING", "TACTICA", "LARGO_PLAZO")}}   # benchmark de cada cartera [PROPUESTO]   # cartera -> L0 (simulado) | L1 (el operador confirma) | L2 (automático con límites); sin dato = L1
NIVELES = {"L0": 0, "L1": 1, "L2": 2}
# Prioridad de cada aviso para el operador [PROPUESTO]
PRIORIDAD_AVISO = {"O-20": "MEDIA", "O-18": "ALTA", "O-03": "ALTA", "O-08": "ALTA", "O-09": "ALTA", "O-13": "ALTA", "O-17": "ALTA"}
ACTORES_PROPUESTA = set(EMISORES)   # quien propone no aprueba ni controla: F, D y H no proponen (Constitución §2, P1)


def _ins(x):
    """Identidad de un instrumento: «EUR/USD» y «EURUSD» son el mismo."""
    return re.sub(r"[^A-Z0-9]", "", x.upper()) if isinstance(x, str) else None


MAX_EDAD_DIMENSIONADO_MIN = 60   # [PROPUESTO] el cálculo de E no puede ser más viejo que esto al proponer


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


class RelojRetrocede(Exception):
    pass


def _valida_config(c):
    """La configuración se valida al construir: una configuración mala no arranca el Orquestador."""
    ok = (politica_valida(c["politica_f"])
          and all(isinstance(x, str) and x in ("N0", "N1", "N2", "N3") for x in c["exige_contradictor_en"])
          and isinstance(c.get("perfiles_activos"), list) and c["perfiles_activos"] and all(isinstance(x, str) for x in c["perfiles_activos"])
          and isinstance(c.get("clases_ratificadas"), dict) and isinstance(c.get("apalancamiento_permitido"), bool)
          and all(_num(c[k]) and c[k] > 0 for k in ("dia_coste_max_eur", "dia_tiempo_max_min", "tolerancia_precio_entrada"))
          and isinstance(c["max_reintentos"], int) and not isinstance(c["max_reintentos"], bool) and c["max_reintentos"] >= 1
          and isinstance(c["umbral_corte_comun_dias_habiles"], int) and not isinstance(c["umbral_corte_comun_dias_habiles"], bool)
          and c["umbral_corte_comun_dias_habiles"] >= 0
          and isinstance(c["exige_contradictor_en"], list) and isinstance(c["matriz_autonomia"], dict)
          and all(isinstance(v, bool) for v in c["matriz_autonomia"].values())
          and isinstance(c["nivel_autonomia"], dict)
          and all(k in ("TRADING", "TACTICA", "LARGO_PLAZO") and v in NIVELES for k, v in c["nivel_autonomia"].items())
          and _num(c["tolerancia_conciliacion_rel"]) and 0 <= c["tolerancia_conciliacion_rel"] <= 0.01
          and isinstance(c["referencias"], dict) and set(c["referencias"]) == {"TRADING", "TACTICA", "LARGO_PLAZO"}
          and all(_referencia_ok(v) for v in c["referencias"].values())
          and (c["instrumentos_permitidos"] is None or isinstance(c["instrumentos_permitidos"], dict)
               and all(k in ("TRADING", "TACTICA", "LARGO_PLAZO") and isinstance(v, list) and all(isinstance(x, str) for x in v)
                       for k, v in c["instrumentos_permitidos"].items())))
    if ok and not c["apalancamiento_permitido"] and c["politica_f"]["apalancamiento_max"] > 1:
        ok = False   # la política de F no puede permitir lo que el sistema prohíbe
    if not ok:
        raise ValueError("configuración del Orquestador inválida")


def _hash(x) -> str:
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _r(ok, codigo, motivo="", **extra):
    return {"ok": ok, "codigo": codigo, "motivo": motivo, **extra}


def _no(codigo, motivo, **extra):
    return _r(False, codigo, motivo, **extra)


def _seguro(fn):
    """Cada operación es atómica: ante un error inesperado restaura el estado y rechaza (O-00)."""
    @functools.wraps(fn)
    def w(self, *a, **k):
        copia = copy.deepcopy(self.__dict__)
        try:
            r = fn(self, *a, **k)
            if not r["ok"]:   # una llamada rechazada no puede adelantar el reloj del Orquestador
                self.ultimo_ahora = copia["ultimo_ahora"]
            return r
        except RelojRetrocede as e:
            self.__dict__.clear(); self.__dict__.update(copia)
            return _no("O-16", str(e))
        except (*ERRORES, SinCobertura) as e:
            self.__dict__.clear(); self.__dict__.update(copia)
            return _no("O-00", f"{fn.__name__}: {type(e).__name__}: {str(e)[:120]}")
    return w


class Orquestador:
    def __init__(self, config, calendario):
        cfg = copy.deepcopy({**CONFIG_DEFECTO, **config})
        _valida_config(cfg)
        self.cfg = cfg
        self.ultimo_ahora, self.ordenes_usadas = None, []
        self.cal_def = calendario
        Calendario(calendario)   # falla pronto si no es válido
        self.sellos, self.eventos, self.encargos = {}, {}, {}
        self.expedientes, self.posiciones, self.gasto_dia, self.avisos = {}, {}, {}, []
        self.ultima_comparacion = {}   # cartera -> id de la comparación vigente
        self.manuales = []     # registros CT-G-14 aceptados (lo que el operador hizo fuera del sistema)
        self.degradadas = {}   # cartera -> motivo: bajada automática a L1 hasta que el operador la restablezca

    # ------------------------------------------------------------ niveles de autonomía
    def nivel(self, cartera):
        """Nivel efectivo: el configurado, o L1 si la cartera está degradada (nunca sube solo)."""
        base = self.cfg["nivel_autonomia"].get(cartera, "L1")
        return "L1" if cartera in self.degradadas and NIVELES[base] > 1 else base

    def _degradar(self, cartera, motivo, ahora):
        if cartera in ("TRADING", "TACTICA", "LARGO_PLAZO") and cartera not in self.degradadas and NIVELES[self.nivel(cartera)] > 1:
            self.degradadas[cartera] = {"motivo": motivo[:160], "ahora": ahora}
            self._aviso("O-19", f"cartera {cartera} degradada a L1: {motivo[:120]}", ahora, cartera)

    @_seguro
    def degradar(self, cartera, motivo, actor, ahora):
        """G o H bajan una cartera a L1 (dato viejo, intermediario caído, estado incierto)."""
        self._ahora(ahora)
        if actor not in ("G", "H", "ORQUESTADOR", "OPERADOR"):
            return _no("O-05", "solo G, H, el Orquestador o el operador degradan una cartera")
        if cartera not in ("TRADING", "TACTICA", "LARGO_PLAZO") or not (isinstance(motivo, str) and motivo.strip()):
            return _no("O-15", "cartera válida y motivo obligatorios")
        self._degradar(cartera, motivo, ahora)
        return _r(True, "OK", f"{cartera} en {self.nivel(cartera)}")

    @_seguro
    def restablecer_nivel(self, cartera, actor, ahora):
        """Solo el operador devuelve una cartera a su nivel configurado, y solo con las discrepancias y degradaciones acusadas."""
        self._ahora(ahora)
        if actor != "OPERADOR":
            return _no("O-05", "solo el operador restablece el nivel de autonomía")
        if cartera not in self.degradadas:
            return _no("O-12", "la cartera no está degradada")
        if any(x["acuse"] is None and x["codigo"] in ("O-18", "O-19") for x in self.avisos):
            return _no("O-06", "hay avisos de discrepancia o degradación sin acusar")
        del self.degradadas[cartera]
        return _r(True, "OK", f"{cartera} vuelve a {self.nivel(cartera)}")

    # ------------------------------------------------------------ utilidades
    def _ahora(self, ahora):
        if not isinstance(ahora, str) or not _FH.match(ahora):
            raise ValueError("ahora con formato inválido")
        a = _dt(ahora)
        if self.ultimo_ahora is not None and a < _dt(self.ultimo_ahora):
            raise RelojRetrocede(f"el reloj retrocede: {ahora} < {self.ultimo_ahora}")
        self.ultimo_ahora = ahora
        return a

    def _aviso(self, codigo, motivo, ahora, ref=None):
        if any(x["acuse"] is None and x["codigo"] == codigo and x["ref"] == ref and x["motivo"] == motivo for x in self.avisos):
            return   # ya hay uno igual sin acusar: no se multiplica
        self.avisos.append({"id": f"AV-{len(self.avisos) + 1:05d}", "codigo": codigo, "prioridad": PRIORIDAD_AVISO.get(codigo, "MEDIA"),
                            "motivo": motivo, "ref": ref, "ahora": ahora, "acuse": None})

    @_seguro
    def reportar_discrepancia(self, diferencias, actor, ahora):
        """G informa de que lo que el intermediario tiene no coincide con lo que el Orquestador cree."""
        self._ahora(ahora)
        if actor != "G":
            return _no("O-05", "solo G reporta discrepancias de conciliación")
        if not (isinstance(diferencias, list) and diferencias and all(isinstance(d, dict) and isinstance(d.get("tipo"), str) for d in diferencias)):
            return _no("O-01", "una discrepancia exige una lista no vacía de diferencias con tipo")
        for d in diferencias:
            self._aviso("O-18", f"conciliación: {d['tipo']} {d.get('ref')}: {str(d.get('detalle'))[:120]}", ahora, d.get("ref") if isinstance(d.get("ref"), str) else None)
        for c in ("TRADING", "TACTICA", "LARGO_PLAZO"):   # una diferencia con el intermediario no se atribuye a una cartera: se baja todo
            self._degradar(c, "discrepancia de conciliación", ahora)
        return _r(True, "OK", f"{len(diferencias)} diferencia(s) registrada(s)")

    @_seguro
    def acusar_aviso(self, aviso_id, actor, ahora):
        """El operador confirma que ha visto un aviso. No lo borra: queda constancia."""
        if actor != "OPERADOR":
            return _no("O-05", "solo el operador acusa recibo de un aviso")
        av = next((x for x in self.avisos if x["id"] == aviso_id), None) if isinstance(aviso_id, str) else None
        if av is None:
            return _no("O-12", f"aviso inexistente: {aviso_id!r}")
        self._ahora(ahora)
        if av["acuse"] is not None:
            return _r(True, "O-02", "aviso ya acusado", duplicado=True)
        av["acuse"] = {"actor": actor, "ahora": ahora}
        return _r(True, "OK", "aviso acusado")

    def _historial_ok(self, ent):
        if not ent["historial"]:
            return False
        prev, ant = "0" * 64, None
        for i, h in enumerate(ent["historial"]):
            cuerpo = {k: v for k, v in h.items() if k != "hash"}
            if h["n"] != i or h["hash_prev"] != prev or h["hash"] != _hash(cuerpo) or h["desde"] != ant:
                return False
            prev, ant = h["hash"], h["hasta"]
        return ent["estado"] == ant

    def cabezas(self):
        """Hash de cabeza de cada historial, para anclarlo fuera del Orquestador (registro de solo añadir)."""
        return {**{"EXP:" + k: v["historial"][-1]["hash"] for k, v in self.expedientes.items()},
                **{"POS:" + k: v["historial"][-1]["hash"] for k, v in self.posiciones.items()}}

    def _propuesta_ok(self, e):
        if not e["propuesta"]:
            return True
        ult = [h for h in e["historial"] if h["hasta"] == "PROPUESTA"]
        return bool(ult) and ult[-1]["datos"] == _hash(e["propuesta"])

    def _sobre_ok(self, e):
        """El sobre guardado es el que se anotó al validarlo (su hash está en la cadena del historial)."""
        s = e.get("sobre")
        if not s or "documento" not in s:
            return True
        ult = [h for h in e["historial"] if h["hasta"] == "VALIDADA"]
        return bool(ult) and ult[-1]["datos"] == s["hash"] == _hash(s["documento"])

    def _comparacion_ok(self, e):
        """El resultado de D (y la elección del operador) es el que se anotó en la cadena del historial."""
        c = e.get("comparacion")
        if not c:
            return True
        ult = [h for h in e["historial"] if h["hasta"] == "COMPARADA"]
        return bool(ult) and ult[-1]["datos"] == _hash(c)

    def _todo_ok(self, e):
        return self._historial_ok(e) and self._propuesta_ok(e) and self._sobre_ok(e) and self._comparacion_ok(e)

    def integridad(self):
        """Lista de expedientes (EXP:) y posiciones (POS:) cuyo historial, sobre, comparación o propuesta no cuadra."""
        return sorted(["EXP:" + k for k, v in self.expedientes.items() if not self._todo_ok(v)]
                      + ["POS:" + k for k, v in self.posiciones.items() if not self._historial_ok(v)])

    def _anota(self, ent, desde, hasta, actor, ahora, motivo, ref=None, datos=None):
        prev = ent["historial"][-1]["hash"] if ent["historial"] else "0" * 64
        h = {"n": len(ent["historial"]), "desde": desde, "hasta": hasta, "actor": actor, "ahora": ahora,
             "motivo": motivo, "ref": ref, "datos": datos, "version_reglas": VERSION_REGLAS, "hash_prev": prev}
        h["hash"] = _hash(h)
        ent["historial"].append(h)
        ent["estado"] = hasta

    def _exp(self, eid):
        e = self.expedientes.get(eid)
        if e is None:
            return None, _no("O-12", f"expediente inexistente: {eid!r}")
        if not self._historial_ok(e):
            return None, _no("O-13", "el historial del expediente no es íntegro")
        if not self._propuesta_ok(e):
            return None, _no("O-13", "la propuesta no coincide con la registrada en el historial")
        if not (self._sobre_ok(e) and self._comparacion_ok(e)):
            return None, _no("O-13", "el sobre o la comparación guardados no coinciden con los anotados en el historial")
        return e, None

    def _compromisos(self, excluir, cartera):
        """Posiciones abiertas y autorizaciones sin ejecutar de esa cartera: la cartera que F recibe debe incluirlas."""
        out = [[x["propuesta"]["entrada"]["instrumento"], x["propuesta"]["entrada"]["activo_base"]]
               for k, x in self.expedientes.items() if k != excluir and x["estado"] == "AUTORIZADA" and x["cartera_destino"] == cartera]
        out += [[p["instrumento"], p["activo_base"]] for p in self.posiciones.values() if p["cartera"] == cartera and p["estado"] != "CERRADA"]
        return out

    def _sello_anulado(self, e):
        en = self.encargos.get(e["encargo_actual"])
        return en is None or self.sellos.get(en["sello_ref"], {}).get("estado") == "ANULADO"

    def _caducar_encargos(self, a, ahora):
        for eid, en in self.encargos.items():
            if en["estado"] == "EN_CURSO" and a > _dt(en["valid_until"]):
                en["estado"] = "CADUCADO"
                self._aviso("O-10", f"encargo {eid} caducó (valid_until)", ahora, en["expediente_id"])

    def _transicion_ok(self, e, hasta, actor):
        if not isinstance(actor, str) or not isinstance(hasta, str):
            return _no("O-01", "actor y estado deben ser texto")
        if e["estado"] in TERMINALES:
            return _no("O-14", f"{e['estado']} es un estado terminal")
        quien = T.get((e["estado"], hasta))
        if quien is None:
            return _no("O-04", f"transición no permitida: {e['estado']} -> {hasta}")
        if actor not in quien:
            return _no("O-05", f"{actor!r} no puede pedir {e['estado']} -> {hasta}")
        return None

    def _duplicado(self, eid, h, expediente_id, ahora):
        """Idempotencia: devuelve el resultado si el mensaje ya se vio, o None si es nuevo."""
        v = self.eventos.get(eid)
        if v is None:
            return None
        if v["hash"] != h:
            self._aviso("O-03", f"event_id {eid} repetido con otro contenido", ahora, expediente_id)
            return _no("O-03", "mismo event_id con contenido distinto")
        if v["expediente_id"] != expediente_id:
            return _no("O-12", "ese mensaje pertenece a otro expediente")
        return _r(True, "O-02", "mensaje duplicado: se ignora", duplicado=True)

    def _ctx_encargo(self, ahora_iso, fecha_vigente=None):
        vigentes = [s["fecha_corte"] for s in self.sellos.values() if s["estado"] == "VIGENTE"]
        if fecha_vigente is None:
            if not vigentes:
                return None
            fecha_vigente = max(vigentes)
        return {"ahora": ahora_iso, "fecha_corte_vigente": fecha_vigente,
                "perfiles_activos": self.cfg["perfiles_activos"],
                "apalancamiento_permitido": self.cfg["apalancamiento_permitido"],
                "sellos": copy.deepcopy(self.sellos), "calendario": self.cal_def}

    def _tope_dia(self, fecha):
        g = self.gasto_dia.get(fecha, {"coste": 0.0, "tiempo": 0.0})
        reservas_c = reservas_t = 0.0
        for en in self.encargos.values():
            if en["estado"] == "EN_CURSO":   # una reserva viva cuenta aunque se emitiera otro día
                reservas_c += max(0.0, en["coste_max"] - en["coste"])
                reservas_t += max(0.0, en["tiempo_max"] - en["tiempo"])
        return g["coste"], g["tiempo"], reservas_c, reservas_t

    # ------------------------------------------------------------ sellos de K
    @_seguro
    def registrar_sello(self, sello, ahora):
        a = self._ahora(ahora)
        fallos = validar_sello(sello, {"calendario": self.cal_def})
        if fallos:
            return _no("O-01", f"sello no válido: {fallos[0]['regla']}: {fallos[0]['mensaje'][:80]}")
        if sello["estado"] != "VIGENTE":
            return _no("O-01", "solo se registran sellos VIGENTES")
        if _dt(sello["emitido_en"]) > a:
            return _no("O-01", "sello emitido en el futuro")
        sid = sello["sello_id"]
        if sid in self.sellos:
            if self.sellos[sid]["hash_sello"] == sello["hash_sello"]:
                return _r(True, "O-02", "sello ya registrado", duplicado=True)
            return _no("O-03", "mismo sello_id con contenido distinto")
        viejo = sello.get("reemplaza_a")
        if viejo is not None and viejo not in self.sellos:
            return _no("O-12", "reemplaza un sello desconocido")
        self.sellos[sid] = copy.deepcopy(sello)
        if viejo is not None:
            self.sellos[viejo]["estado"] = "ANULADO"
            for eid, en in self.encargos.items():
                if en["sello_ref"] == viejo and en["estado"] in ("EN_CURSO", "ENTREGADO"):
                    en["estado"] = "ANULADO"
                    self._aviso("O-06", f"encargo {eid} anulado: su sello {viejo} fue reemplazado", ahora, en["expediente_id"])
            for xid, x in self.expedientes.items():
                en = self.encargos.get(x["encargo_actual"])
                if en and en["sello_ref"] == viejo and x["estado"] in ("VALIDADA", "COMPARADA", "PROPUESTA", "AUTORIZADA"):
                    self._anota(x, x["estado"], "CADUCADA", "ORQUESTADOR", ahora, f"su sello {viejo} fue reemplazado")
                    self._aviso("O-06", f"expediente {xid} caducado: su sello {viejo} fue reemplazado", ahora, xid)
        return _r(True, "OK", "sello registrado")

    # ------------------------------------------------------------ expedientes
    @_seguro
    def detectar(self, expediente_id, correlation_id, via_entrada, cartera_destino, actor, ahora):
        self._ahora(ahora)
        if actor not in EMISORES:
            return _no("O-05", f"{actor!r} no puede abrir expedientes")
        if not (isinstance(expediente_id, str) and _ID.match(expediente_id) and isinstance(correlation_id, str) and _ID.match(correlation_id)):
            return _no("O-01", "identificadores inválidos")
        if via_entrada not in ("DISCRECIONAL", "SISTEMATICA") or cartera_destino not in ("TRADING", "TACTICA", "LARGO_PLAZO"):
            return _no("O-01", "via_entrada o cartera_destino inválidos")
        if actor in GESTORES and actor != {"TRADING": "GESTOR_TRADING", "TACTICA": "GESTOR_TACTICA", "LARGO_PLAZO": "GESTOR_LARGO_PLAZO"}[cartera_destino]:
            return _no("O-05", "un gestor solo abre expedientes de su cartera")
        if expediente_id in self.expedientes:
            return _no("O-03", "expediente ya existe")
        e = {"expediente_id": expediente_id, "correlation_id": correlation_id, "via_entrada": via_entrada,
             "cartera_destino": cartera_destino, "estado": "DETECTADA", "historial": [], "encargo_actual": None,
             "sobre": None, "contradictor": None, "retenido": None, "sin_avance": 0, "propuesta": None, "posicion_id": None, "reapertura": None}
        self._anota(e, None, "DETECTADA", actor, ahora, "detectada")
        self.expedientes[expediente_id] = e
        return _r(True, "OK", "expediente creado")

    @_seguro
    def emitir_encargo(self, expediente_id, encargo, actor, ahora):
        a = self._ahora(ahora)
        e, err = self._exp(expediente_id)
        if err:
            return err
        if e["retenido"] is not None:
            return _no("O-17", "hay una objeción crítica pendiente: el operador debe levantarla o descartar el expediente")
        if not isinstance(encargo, dict) or not isinstance(encargo.get("event_id"), str):
            return _no("O-01", "encargo mal formado")
        eid, h = encargo["event_id"], _hash(encargo)
        dup = self._duplicado(eid, h, expediente_id, ahora)
        if dup:
            return dup
        self._caducar_encargos(a, ahora)
        err = self._transicion_ok(e, "EN_ANALISIS", actor)
        if err:
            return err
        if encargo.get("expediente_id") != expediente_id or encargo.get("correlation_id") != e["correlation_id"]:
            return _no("O-12", "el encargo no pertenece a este expediente o petición")
        if actor != "BROKER" and encargo.get("producer") != actor:
            return _no("O-05", "el emisor del encargo no es quien lo pide")
        if encargo["payload"].get("cartera_destino") != e["cartera_destino"] if isinstance(encargo.get("payload"), dict) else True:
            return _no("O-12", "la cartera del encargo no es la del expediente")
        mand = encargo["payload"].get("mandato")
        if not (isinstance(mand, dict) and mand.get("benchmark_ref") == self.cfg["referencias"][e["cartera_destino"]]["benchmark_ref"]):
            return _no("O-24", "el mandato del encargo no cita la referencia configurada para la cartera")
        ctx = self._ctx_encargo(ahora)
        if ctx is None:
            return _no("O-06", "no hay ningún sello de K registrado")
        fallos = validar_encargo(encargo, ctx)
        if fallos:
            return _no("O-01", f"encargo no válido: {fallos[0]['regla']}: {fallos[0]['mensaje'][:80]}", reglas=sorted({x['regla'] for x in fallos}))
        # reintento: el encargo anterior debe estar cerrado sin éxito
        previo = self.encargos.get(e["encargo_actual"]) if e["encargo_actual"] else None
        if e["estado"] == "EN_ANALISIS" and previo and previo["estado"] in ("EN_CURSO", "ENTREGADO"):
            return _no("O-06", "ya hay un encargo en curso o entregado para este expediente")
        if e["sin_avance"] >= self.cfg["max_reintentos"]:
            self._aviso("O-09", f"{expediente_id}: {e['sin_avance']} encargos sin avance", ahora, expediente_id)
            return _no("O-09", "máximo de reintentos sin avance; se avisa al operador")
        p = encargo["payload"]["presupuesto"]
        fecha = str(a.astimezone(timezone.utc).date())
        gc, gt, rc, rt = self._tope_dia(fecha)
        if gc + rc + p["coste_max_eur"] > self.cfg["dia_coste_max_eur"] or gt + rt + p["tiempo_max_min"] > self.cfg["dia_tiempo_max_min"]:
            return _no("O-08", "presupuesto diario agotado o comprometido: no se aceptan encargos nuevos")
        self.eventos[eid] = {"hash": h, "expediente_id": expediente_id}
        self.encargos[eid] = {"event_id": eid, "expediente_id": expediente_id, "estado": "EN_CURSO",
                              "sello_ref": encargo["payload"]["sello_corte_ref"], "msg": copy.deepcopy(encargo),
                              "valid_until": encargo["valid_until"], "entrega_antes_de": p["entrega_antes_de"],
                              "coste_max": p["coste_max_eur"], "tiempo_max": p["tiempo_max_min"], "coste": 0.0, "tiempo": 0.0,
                              "fecha_emision": fecha, "ahora_emision": ahora, "fecha_corte": encargo["payload"]["fecha_corte"],
                              "fecha_vigente_emision": ctx["fecha_corte_vigente"], "nivel": encargo["payload"]["nivel_analisis"]}
        e["encargo_actual"] = eid
        e["sin_avance"] += 1
        self._anota(e, e["estado"], "EN_ANALISIS", actor, ahora, "encargo emitido", eid)
        return _r(True, "OK", "encargo aceptado", encargo=eid)

    @_seguro
    def registrar_gasto(self, event_id_encargo, coste_eur, tiempo_min, ahora):
        """Los gastos son hechos: se registran siempre (si son válidos) y pueden activar alertas."""
        a = self._ahora(ahora)
        en = self.encargos.get(event_id_encargo)
        if en is None:
            return _no("O-12", "encargo inexistente")
        if not (_num(coste_eur) and _num(tiempo_min) and coste_eur >= 0 and tiempo_min >= 0):
            return _no("O-01", "coste o tiempo inválidos")
        en["coste"] += coste_eur
        en["tiempo"] += tiempo_min
        fecha = str(a.astimezone(timezone.utc).date())
        g = self.gasto_dia.setdefault(fecha, {"coste": 0.0, "tiempo": 0.0})
        g["coste"] += coste_eur
        g["tiempo"] += tiempo_min
        alertas = []
        if en["estado"] == "EN_CURSO" and (en["coste"] > en["coste_max"] or en["tiempo"] > en["tiempo_max"]):
            en["estado"] = "INCOMPLETO"
            alertas.append("O-07")
            self._aviso("O-07", f"encargo {event_id_encargo} superó su presupuesto", ahora, en["expediente_id"])
        if g["coste"] >= self.cfg["dia_coste_max_eur"] or g["tiempo"] >= self.cfg["dia_tiempo_max_min"]:
            alertas.append("O-08")
            self._aviso("O-08", f"presupuesto diario agotado el {fecha}", ahora)
        return _r(True, "OK", "gasto registrado", alertas=alertas)

    @_seguro
    def entregar_sobre(self, expediente_id, sobre, ahora, informe=None):
        a = self._ahora(ahora)
        e, err = self._exp(expediente_id)
        if err:
            return err
        if not isinstance(sobre, dict) or not isinstance(sobre.get("event_id"), str):
            return _no("O-01", "sobre mal formado")
        if e["retenido"] is not None:
            return _no("O-17", "hay una objeción crítica pendiente: el operador debe levantarla o descartar el expediente")
        sid, h = sobre["event_id"], _hash(sobre)
        dup = self._duplicado(sid, h, expediente_id, ahora)
        if dup:
            return dup
        self._caducar_encargos(a, ahora)
        err = self._transicion_ok(e, "VALIDADA", "C")
        if err:
            return err
        en = self.encargos.get(e["encargo_actual"])
        if en is not None and en["estado"] == "CADUCADO":
            return _no("O-10", "el encargo caducó antes de la entrega")
        if en is None or en["estado"] == "ANULADO":
            return _no("O-06", f"el encargo actual no admite entrega ({en['estado'] if en else 'inexistente'})")
        if en["estado"] == "INCOMPLETO":
            return _no("O-07", "encargo incompleto por presupuesto: no se valida; reemitir o descartar")
        if en["estado"] != "EN_CURSO":
            return _no("O-06", f"el encargo está {en['estado']}")
        if self.sellos.get(en["sello_ref"], {}).get("estado") != "VIGENTE":
            en["estado"] = "ANULADO"
            return _no("O-06", "el sello del encargo ya no está vigente")
        ctx_enc = self._ctx_encargo(en["ahora_emision"], en["fecha_vigente_emision"])
        ctx_sob = {"ahora": ahora, "fecha_corte_encargo": en["fecha_corte"], "perfiles_activos": self.cfg["perfiles_activos"],
                   "clases_ratificadas": self.cfg["clases_ratificadas"], "apalancamiento_permitido": self.cfg["apalancamiento_permitido"]}
        # el sobre se valida con su propio reloj; el encargo, con el de su emisión
        fallos = sobre_responde_a_encargo(en["msg"], sobre, ctx_enc, ctx_sob)
        if fallos:
            return _no("O-01", f"el sobre no responde al encargo: {fallos[0]['regla']}: {fallos[0]['mensaje'][:80]}", reglas=sorted({x['regla'] for x in fallos}))
        contr = None
        if en["nivel"] in self.cfg["exige_contradictor_en"] or informe is not None:
            if informe is None:
                return _no("O-06", f"el nivel {en['nivel']} exige el informe del Contradictor (CT-G-03)")
            if not isinstance(informe, dict) or not isinstance(informe.get("event_id"), str):
                return _no("O-01", "informe del Contradictor mal formado")
            ih = _hash(informe)
            dup = self._duplicado(informe["event_id"], ih, expediente_id, ahora)
            if dup:
                return _no("O-03", "el informe ya se usó")
            fallos = validar_informe(informe, {"ahora": ahora, "sobre": sobre})
            if fallos:
                return _no("O-01", f"informe del Contradictor no válido: {fallos[0]['regla']}: {fallos[0]['mensaje'][:80]}", reglas=sorted({x['regla'] for x in fallos}))
            self.eventos[informe["event_id"]] = {"hash": ih, "expediente_id": expediente_id}
            contr = {"event_id": informe["event_id"], "veredicto": informe["payload"]["veredicto"], "hash": ih,
                     "valid_until": informe["valid_until"]}
        self.eventos[sid] = {"hash": h, "expediente_id": expediente_id}
        en["estado"] = "ENTREGADO"
        ident = sobre["payload"]["identificacion"]
        info = {"event_id": sid, "fecha_corte": ident["fecha_corte"], "valid_until": sobre["valid_until"],
                "perfil": ident["perfil"], "nivel": ident["nivel_analisis"], "contradictor_ref": contr["event_id"] if contr else None,
                "hash": h, "documento": copy.deepcopy(sobre)}   # el sobre entero: D y la propuesta se contrastan con él
        if contr:   # el sobre vale solo mientras valga el informe del Contradictor
            info["valid_until"] = min(info["valid_until"], contr["valid_until"], key=_dt)
        if contr and contr["veredicto"] == "OBJECION_CRITICA":
            e["retenido"] = {"sobre": info, "contradictor": contr}
            self._anota(e, e["estado"], "EN_ANALISIS", "ORQUESTADOR", ahora, "sobre retenido por objeción crítica del Contradictor", sid)
            self._aviso("O-17", f"{expediente_id}: objeción crítica del Contradictor; solo el operador puede levantarla", ahora, expediente_id)
            return _no("O-17", "objeción crítica: el expediente queda detenido hasta que el operador la levante o lo descarte")
        if contr and contr["veredicto"] == "OBJECION_MAYOR":
            self._aviso("O-17", f"{expediente_id}: objeción mayor del Contradictor", ahora, expediente_id)
        e["sobre"], e["contradictor"] = info, contr
        e["sin_avance"] = 0
        self._anota(e, e["estado"], "VALIDADA", "C", ahora, "sobre aceptado", sid, datos=h)
        return _r(True, "OK", "sobre aceptado")

    @_seguro
    def levantar_objecion(self, expediente_id, motivo, actor, ahora):
        """Solo el operador, con motivo escrito, levanta una objeción crítica del Contradictor."""
        a = self._ahora(ahora)
        e, err = self._exp(expediente_id)
        if err:
            return err
        if actor != "OPERADOR":
            return _no("O-05", "solo el operador levanta una objeción crítica")
        if not (isinstance(motivo, str) and motivo.strip()):
            return _no("O-15", "levantar una objeción crítica exige motivo escrito")
        r = e["retenido"]
        if r is None or e["estado"] != "EN_ANALISIS":
            return _no("O-04", "no hay ninguna objeción crítica pendiente en este expediente")
        if a > _dt(r["sobre"]["valid_until"]) or self._sello_anulado(e):
            return _no("O-10", "el sobre retenido caducó o su sello ya no es válido")
        e["sobre"], e["contradictor"], e["retenido"] = r["sobre"], r["contradictor"], None
        e["sin_avance"] = 0
        self._anota(e, "EN_ANALISIS", "VALIDADA", "OPERADOR", ahora, f"objeción crítica levantada: {motivo.strip()}", r["contradictor"]["event_id"],
                    datos=e["sobre"].get("hash"))
        return _r(True, "OK", "objeción levantada; expediente validado")

    def _candidato_vivo(self, x, cartera, a):
        """Candidato que debe entrar en cualquier comparación de la cartera: VALIDADA o COMPARADA, con sobre vigente y sello válido."""
        return (x["cartera_destino"] == cartera and x["estado"] in ("VALIDADA", "COMPARADA") and x.get("sobre")
                and a <= _dt(x["sobre"]["valid_until"]) and not self._sello_anulado(x))

    @_seguro
    def comparar(self, expediente_ids, actor, ahora):
        a = self._ahora(ahora)
        if not isinstance(expediente_ids, list) or not expediente_ids or len(set(map(str, expediente_ids))) != len(expediente_ids):
            return _no("O-01", "se necesita al menos un expediente y sin repetidos")
        exps = []
        for eid in expediente_ids:
            e, err = self._exp(eid)
            if err:
                return err
            err = self._transicion_ok(e, "COMPARADA", actor)
            if err:
                return err
            if a > _dt(e["sobre"]["valid_until"]):
                return _no("O-10", f"el sobre de {eid} caducó")
            if self._sello_anulado(e):
                return _no("O-06", f"el sello de {eid} ya no es válido")
            exps.append(e)
        if len({x["cartera_destino"] for x in exps}) != 1:
            return _no("O-06", "los expedientes comparados deben ser de la misma cartera")
        cartera = exps[0]["cartera_destino"]
        faltan = sorted(k for k, x in self.expedientes.items() if k not in expediente_ids and self._candidato_vivo(x, cartera, a))
        if faltan:   # T-34: quien llama no elige contra quién se compara
            return _no("O-24", f"hay que comparar con todos los candidatos vigentes de la cartera; faltan {', '.join(faltan[:5])}", faltan=faltan)
        ref = self.cfg["referencias"][cartera]
        otra = [x["expediente_id"] for x in exps if self.encargos[x["encargo_actual"]]["msg"]["payload"]["mandato"]["benchmark_ref"] != ref["benchmark_ref"]]
        if otra:
            return _no("O-24", f"el mandato del encargo cita otra referencia que la configurada para la cartera: {', '.join(otra)}")
        from datetime import date
        cortes = sorted(date.fromisoformat(x["sobre"]["fecha_corte"]) for x in exps)
        cal = Calendario(self.cal_def)
        dif = max(cal.dias_habiles(m["mercado"], cortes[0], cortes[-1])
                  for x in exps for m in self.sellos[self.encargos[x["encargo_actual"]]["sello_ref"]]["mercados"])
        if dif > self.cfg["umbral_corte_comun_dias_habiles"]:
            viejos = [x["expediente_id"] for x in exps if date.fromisoformat(x["sobre"]["fecha_corte"]) == cortes[0]]
            return _no("O-11", f"fechas de corte distintas ({dif} d.h.): hay que actualizar datos", actualizar=viejos)
        if any(_hash(x["sobre"]["documento"]) != x["sobre"]["hash"] for x in exps):
            return _no("O-13", "un sobre guardado no cuadra con su hash")
        d = comparar_candidatos([{"expediente_id": x["expediente_id"], "sobre": copy.deepcopy(x["sobre"]["documento"])} for x in exps], ahora, ref)
        if not d["ok"]:
            return _no("O-01", f"D no pudo comparar: {d['motivo']}")
        cid = "CMP-" + _hash([sorted(expediente_ids), ahora, len(self.ultima_comparacion)])[:12]
        filas = {r["expediente_id"]: r for g in d["grupos"].values() for r in g["ranking"]}
        excl = {x["expediente_id"]: x["motivo"] for x in d.get("excluidos", [])}
        for e in exps:
            eid = e["expediente_id"]
            grupo = next((g for g in d.get("grupos", {}).values() if any(r["expediente_id"] == eid for r in g["ranking"])), None)
            fila = filas.get(eid)
            e["comparacion"] = {"id": cid, "codigo_d": d["codigo"], "decision_global": d["decision_global"], "referencia": d["referencia"],
                                "decision": grupo["decision"] if grupo else None, "sensible": grupo["sensible"] if grupo else None,
                                "ganador": d["ganador_global"] == eid, "aspirante": eid in d["aspirantes"] and d["ganador_global"] is None,
                                "excluido": excl.get(eid), "elegido_por_operador": None,
                                "detalle_d": {k: fila[k] for k in ("puntuacion", "exceso_sobre_referencia_pct", "horizonte_dias", "peor_escenario_pct",
                                                                   "confianza_normalizada", "factor_evidencia", "dominado_por")} if fila else None}
            self._anota(e, e["estado"], "COMPARADA", actor, ahora, "comparada con " + ",".join(expediente_ids), cid, datos=_hash(e["comparacion"]))
        ganador = next((x["expediente_id"] for x in exps if x["comparacion"]["ganador"]), None)
        self.ultima_comparacion[cartera] = cid
        return _r(True, "OK", "comparación registrada" if d["decision_global"] == "INVERTIR" else "D se abstiene: ningún candidato supera la referencia",
                  ganador=ganador, codigo_d=d["codigo"], decision_global=d["decision_global"])

    @_seguro
    def elegir(self, expediente_id, actor, motivo, ahora):
        """El operador elige entre los aspirantes cuando D no da un ganador claro (empatados o primeros con otra ponderación)."""
        self._ahora(ahora)
        e, err = self._exp(expediente_id)
        if err:
            return err
        if actor != "OPERADOR":
            return _no("O-05", "solo el operador elige cuando D no da un ganador claro")
        if not (isinstance(motivo, str) and motivo.strip()):
            return _no("O-15", "elegir exige motivo")
        c = e.get("comparacion")
        if e["estado"] != "COMPARADA" or c is None:
            return _no("O-04", "solo se elige un expediente COMPARADA")
        if c["ganador"]:
            return _r(True, "O-02", "ya es el ganador de D", duplicado=True)
        if c["excluido"] is not None:
            return _no("O-22", f"D lo excluyó: {c['excluido']}")
        if c["id"] != self.ultima_comparacion.get(e["cartera_destino"]):
            return _no("O-22", "esa comparación ya no es la vigente de la cartera: compare de nuevo")
        if not c["aspirante"]:
            return _no("O-22", "solo se elige entre los aspirantes de una decisión ajustada (empatados o primeros con otra ponderación)")
        if any(x.get("comparacion", {}).get("id") == c["id"] and (x["comparacion"]["ganador"] or x["comparacion"]["elegido_por_operador"])
               for x in self.expedientes.values()):
            return _no("O-22", "en esa comparación ya hay un candidato elegido")
        c["elegido_por_operador"] = {"motivo": motivo[:200], "ahora": ahora}
        self._anota(e, "COMPARADA", "COMPARADA", actor, ahora, f"elegido por el operador: {motivo[:120]}", c["id"], datos=_hash(c))
        return _r(True, "OK", "elegido")

    @_seguro
    def proponer(self, expediente_id, condiciones_entrada, condiciones_salida, actor, ahora, dimensionado=None):
        a = self._ahora(ahora)
        e, err = self._exp(expediente_id)
        if err:
            return err
        err = self._transicion_ok(e, "PROPUESTA", actor)
        if err:
            return err
        if actor not in ACTORES_PROPUESTA:
            return _no("O-05", f"{actor!r} no puede proponer")
        if a > _dt(e["sobre"]["valid_until"]) or self._sello_anulado(e):
            return _no("O-10", "el sobre caducó o su sello ya no es válido")
        ce, cs = condiciones_entrada, condiciones_salida
        if not (isinstance(ce, dict) and _num(ce.get("limite")) and isinstance(ce.get("ventana_hasta"), str) and _FH.match(ce["ventana_hasta"])):
            return _no("O-01", "condiciones_entrada: faltan límite numérico y ventana_hasta")
        if not (isinstance(ce.get("instrumento"), str) and _ID.match(ce["instrumento"]) and isinstance(ce.get("activo_base"), str) and _ID.match(ce["activo_base"])
                and _num(ce.get("cantidad")) and ce["cantidad"] > 0 and _num(ce.get("apalancamiento")) and ce["apalancamiento"] >= 1 and ce["limite"] > 0):
            return _no("O-01", "condiciones_entrada: faltan instrumento, activo_base, cantidad positiva, apalancamiento (>= 1) y límite positivo")
        if ce["apalancamiento"] > 1 and not self.cfg["apalancamiento_permitido"]:
            return _no("O-06", "el apalancamiento no está permitido")
        if _dt(ce["ventana_hasta"]) <= a:
            return _no("O-10", "la ventana de entrada ya venció")
        conds = cs.get("condiciones") if isinstance(cs, dict) else None
        if not (isinstance(conds, list) and conds and all(isinstance(c, dict) and isinstance(c.get("id"), str) and _ID.match(c["id"])
                and isinstance(c.get("metrica"), str) and c.get("operador") in OPERADORES and _num(c.get("umbral")) for c in conds)):
            return _no("O-01", "condiciones_salida: deben ser numéricas (id, métrica, operador, umbral)")
        if len({c["id"] for c in conds}) != len(conds):
            return _no("O-01", "condiciones_salida: ids repetidos")
        if not all(c.get("tipo") in ("STOP", "OBJETIVO", "INVALIDEZ") for c in conds):
            return _no("O-01", "condiciones_salida: cada condición debe ser STOP, OBJETIVO o INVALIDEZ")
        stops = [c for c in conds if c.get("tipo") == "STOP"]
        if len(stops) != 1 or stops[0]["metrica"] != "precio":
            return _no("O-01", "condiciones_salida: debe haber exactamente un STOP y su métrica debe ser el precio")
        c = e.get("comparacion") or {}
        if not (c.get("ganador") or c.get("elegido_por_operador")):
            return _no("O-22", "solo se propone el ganador de D o el candidato que eligió el operador")
        if c.get("id") != self.ultima_comparacion.get(e["cartera_destino"]) or any(
                x["estado"] == "VALIDADA" and self._candidato_vivo(x, e["cartera_destino"], a) for x in self.expedientes.values()):
            return _no("O-22", "hay candidatos nuevos o una comparación más reciente en la cartera: compare de nuevo con todos")
        err = self._coincide_con_sobre(e, ce, cs, stops[0])
        if err:
            return err
        q_e, err = self._cantidad_de_e(e, ce, stops[0], dimensionado, a)
        if err:
            return err
        e["propuesta"] = {"entrada": copy.deepcopy(ce), "salida": copy.deepcopy(cs), "cantidad_e": q_e, "dimensionado": copy.deepcopy(dimensionado)}
        self._anota(e, e["estado"], "PROPUESTA", actor, ahora, "propuesta", datos=_hash(e["propuesta"]))
        return _r(True, "OK", "propuesta registrada")

    def _coincide_con_sobre(self, e, ce, cs, stop):
        """O-21: la propuesta lleva a la orden lo que se analizó, no otra cosa."""
        if _hash(e["sobre"]["documento"]) != e["sobre"]["hash"]:
            return _no("O-13", "el sobre guardado no cuadra con su hash")
        p = e["sobre"]["documento"]["payload"]
        ident, es = p["identificacion"], p["entrada_salida"]
        largo = stop["operador"] in ("<", "<=")
        if not _ins(ident["instrumento"]) or _ins(ce["instrumento"]) != _ins(ident["instrumento"]):
            return _no("O-21", "el instrumento no es el analizado en el sobre")
        if ce["activo_base"] != ident["divisa_base"]:
            return _no("O-21", "el activo base no es la divisa base del sobre (F mide la concentración con él)")
        if ("LARGO" if largo else "CORTO") != ident["direccion"]:
            return _no("O-21", "la dirección no es la del sobre")
        lim = ce["limite"]
        if not (stop["umbral"] < lim if largo else stop["umbral"] > lim):
            return _no("O-21", "el stop no está del lado de la pérdida respecto al límite de entrada")
        sv = es["stop"]["valor"]
        if not (_num(sv) and isinstance(es["stop"].get("unidad"), str) and re.fullmatch(r"[A-Z]{3}", es["stop"]["unidad"])):
            return _no("O-21", "el sobre no da un stop de precio (valor numérico en una divisa): no hay con qué ligar la propuesta")
        if stop["umbral"] < sv if largo else stop["umbral"] > sv:
            return _no("O-21", "el stop es más holgado que el analizado (solo se admite igual o más prudente)")
        ov = es["objetivo"]["valor"]
        objs = [x for x in cs["condiciones"] if x.get("tipo") == "OBJETIVO"]
        for o_ in objs:
            if o_["metrica"] != "precio" or not (o_["umbral"] > lim if largo else o_["umbral"] < lim):
                return _no("O-21", "el objetivo debe ser un precio del lado de la ganancia")
            if _num(ov) and (o_["umbral"] > ov if largo else o_["umbral"] < ov):
                return _no("O-21", "el objetivo es más ambicioso que el analizado")
        declaradas = {(x["metrica"], x["operador"], x["umbral"], x.get("unidad")) for x in cs["condiciones"] if x["tipo"] == "INVALIDEZ"}
        for inv in p["tesis"].get("condiciones_invalidez", []):
            if (inv["metrica"], inv["operador"], inv["umbral"], inv.get("unidad")) not in declaradas:
                return _no("O-21", f"falta la condición de invalidez {inv['id']} del sobre en las condiciones de salida")
        apal = p["capital"]["apalancamiento"]["valor"]
        if _num(apal) and ce["apalancamiento"] > apal:
            return _no("O-21", "el apalancamiento supera el analizado")
        if _dt(ce["ventana_hasta"]) > _dt(e["sobre"]["valid_until"]):
            return _no("O-21", "la ventana de entrada pasa de la vigencia del sobre")
        if e["cartera_destino"] not in ident["cartera_compatible"]:
            return _no("O-21", "la cartera de destino no es compatible según el sobre")
        return None

    def _cantidad_de_e(self, e, ce, stop, dim, a):
        """O-23: la cantidad sale de E. El Orquestador repite el cálculo con las mismas entradas y la propuesta no puede pasarse."""
        if not (isinstance(dim, dict) and set(dim) == {"solicitud", "cartera", "riesgo_objetivo_pct", "paso", "ahora"}
                and isinstance(dim["ahora"], str) and _FH.match(dim["ahora"])):
            return None, _no("O-23", "falta el cálculo de E (solicitud, cartera, riesgo_objetivo_pct, paso, ahora)")
        try:
            t_e = _dt(dim["ahora"])
        except ValueError:
            return None, _no("O-23", "instante del cálculo de E ilegible")
        if not (t_e <= a and (a - t_e).total_seconds() <= MAX_EDAD_DIMENSIONADO_MIN * 60):
            return None, _no("O-23", f"el cálculo de E es posterior al instante o tiene más de {MAX_EDAD_DIMENSIONADO_MIN} min")
        sol = dim["solicitud"]
        esperado = {"instrumento": ce["instrumento"], "activo_base": ce["activo_base"], "direccion": "LARGO" if stop["operador"] in ("<", "<=") else "CORTO",
                    "precio_entrada": ce["limite"], "stop_precio": stop["umbral"], "apalancamiento": ce["apalancamiento"], "cartera": e["cartera_destino"]}
        if sol != esperado:
            return None, _no("O-23", "la solicitud de E no es la propuesta (instrumento, dirección, límite, stop, apalancamiento o cartera)")
        r = dimensionar(copy.deepcopy(sol), copy.deepcopy(dim["cartera"]), self.cfg["politica_f"], dim["ahora"], dim["riesgo_objetivo_pct"], dim["paso"])
        if not r["ok"]:
            return None, _no("O-23", f"E no da una cantidad viable ({r['codigo']}): {r['motivo'][:80]}")
        if ce["cantidad"] > r["cantidad"] * (1 + 1e-12):
            return None, _no("O-23", f"la cantidad propuesta supera la que calcula E ({r['cantidad']})")
        return r["cantidad"], None

    @_seguro
    def autorizar(self, expediente_id, actor, control_f, ahora):
        a = self._ahora(ahora)
        e, err = self._exp(expediente_id)
        if err:
            return err
        err = self._transicion_ok(e, "AUTORIZADA", actor)
        if err:
            return err
        if actor == "MATRIZ_AUTONOMIA" and not self.cfg["matriz_autonomia"].get(e["cartera_destino"], False):
            return _no("O-05", "la matriz de autonomía no autoriza esta cartera sin el operador")
        if actor == "MATRIZ_AUTONOMIA" and NIVELES[self.nivel(e["cartera_destino"])] < 2:
            return _no("O-05", f"la cartera está en {self.nivel(e['cartera_destino'])}: autoriza el operador")
        if not isinstance(control_f, dict) or not isinstance(control_f.get("event_id"), str):
            return _no("O-01", "falta el informe de control de F (CT-G-08)")
        ih = _hash(control_f)
        dup = self._duplicado(control_f["event_id"], ih, expediente_id, ahora)
        if dup:
            return _no("O-03", "el informe de F ya se usó")
        if a > _dt(e["propuesta"]["entrada"]["ventana_hasta"]) or a > _dt(e["sobre"]["valid_until"]):
            return _no("O-10", "la propuesta caducó")
        if self._sello_anulado(e):
            return _no("O-06", "el sello del análisis ya no es válido")
        fallos = validar_informe_f(control_f, {"ahora": ahora, "expediente_id": expediente_id, "correlation_id": e["correlation_id"],
                                               "propuesta": e["propuesta"], "cartera_destino": e["cartera_destino"], "politica": self.cfg["politica_f"],
                                               "compromisos": self._compromisos(expediente_id, e["cartera_destino"])})
        if fallos:
            return _no("O-01", f"informe de F no válido: {fallos[0]['regla']}: {fallos[0]['mensaje'][:80]}", reglas=sorted({x['regla'] for x in fallos}))
        cap_e = (e["propuesta"].get("dimensionado") or {}).get("cartera", {}).get("capital_eur")
        if cap_e != control_f["entradas"]["cartera"].get("capital_eur"):
            return _no("O-23", "F controló con un capital distinto del que usó E para dimensionar")
        self.eventos[control_f["event_id"]] = {"hash": ih, "expediente_id": expediente_id}
        if control_f["resultado"] == "VETADO":
            return _no("O-06", "F vetó la propuesta")
        e["control_f"] = {"resultado": control_f["resultado"], "cantidad_aprobada": control_f["cantidad_aprobada"], "event_id": control_f["event_id"],
                          "emitido_en": control_f["emitido_en"], "valid_until": control_f["valid_until"], "entradas": copy.deepcopy(control_f["entradas"])}
        self._anota(e, e["estado"], "AUTORIZADA", actor, ahora, f"control F: {control_f['resultado']} ({control_f['cantidad_aprobada']})", control_f["event_id"])
        return _r(True, "OK", "autorizada")

    @_seguro
    def ejecutar(self, expediente_id, orden, actor, ahora):
        a = self._ahora(ahora)
        e, err = self._exp(expediente_id)
        if err:
            return err
        err = self._transicion_ok(e, "EJECUTADA", actor)
        if err:
            return err
        return self._ejecutar(e, orden, actor, ahora, a)

    def _ejecutar(self, e, orden, actor, ahora, a, manual=False):
        ok = (isinstance(orden, dict) and isinstance(orden.get("orden_id"), str) and _ID.match(orden["orden_id"])
              and _num(orden.get("cantidad")) and orden["cantidad"] > 0 and _num(orden.get("precio")) and orden["precio"] > 0
              and orden.get("conciliada") is True)
        if not ok:
            return _no("O-06", "sin confirmación verificable del intermediario: no cuenta como ejecutada")
        prot = orden.get("proteccion_orden_ids")
        if not (isinstance(prot, list) and prot and all(isinstance(x, str) and _ID.match(x) for x in prot)):
            return _no("O-06", "la orden no lleva órdenes de protección asociadas")
        if a > _dt(e["propuesta"]["entrada"]["ventana_hasta"]) or a > _dt(e["sobre"]["valid_until"]):
            return _no("O-10", "la ventana de entrada o el sobre vencieron antes de ejecutar")
        quien = next((x["actor"] for x in reversed(e["historial"]) if x["hasta"] == "AUTORIZADA"), None)
        if not manual and quien == "MATRIZ_AUTONOMIA" and NIVELES[self.nivel(e["cartera_destino"])] < 2:
            return _no("O-05", f"la autorización fue automática y la cartera está ahora en {self.nivel(e['cartera_destino'])}: la confirma el operador")
        if self._sello_anulado(e):
            return _no("O-06", "el sello del análisis ya no es válido")
        cf = e["control_f"]
        if a > _dt(cf["valid_until"]):
            return _no("O-10", "el informe de F venció antes de ejecutar")
        if orden["cantidad"] > cf["cantidad_aprobada"]:
            return _no("O-06", "la orden supera la cantidad que F aprobó")
        real = controlar({**cf["entradas"]["solicitud"], "cantidad": orden["cantidad"], "precio_entrada": orden["precio"]},
                         cf["entradas"]["cartera"], cf["entradas"]["politica"], cf["emitido_en"])
        if real["resultado"] != "APROBADO":
            return _no("O-06", "con el precio y la cantidad reales F no aprobaría la orden (stop, riesgo o tamaño)")
        lim = e["propuesta"]["entrada"]["limite"]
        if abs(orden["precio"] - lim) > self.cfg["tolerancia_precio_entrada"] * abs(lim):
            return _no("O-06", "el precio de ejecución se aleja del límite autorizado")
        if orden["orden_id"] in self.ordenes_usadas or any(x in self.ordenes_usadas for x in prot):
            return _no("O-03", "orden ya usada en otro expediente o posición")
        ins = e["propuesta"]["entrada"]["instrumento"]
        if any(q["estado"] != "CERRADA" and q["instrumento"] == ins for q in self.posiciones.values()):
            return _no("O-06", "ya hay una posición abierta en ese instrumento (una por instrumento, T-13)")
        if abs(neto_libre(self.manuales, ins)) > 1e-6:
            return _no("O-06", "hay operaciones libres declaradas abiertas en ese instrumento: no se mezclan con una posición del sistema")
        pid = "POS-" + e["expediente_id"]
        if pid in self.posiciones:
            return _no("O-03", "la posición ya existe")
        self.posiciones[pid] = {"posicion_id": pid, "expediente_id": e["expediente_id"], "cartera": e["cartera_destino"],
                                "cantidad": orden["cantidad"], "estado": "ABIERTA", "historial": [],
                                "nivel": self.nivel(e["cartera_destino"]), "direccion": "LARGO" if [c for c in e["propuesta"]["salida"]["condiciones"] if c["tipo"] == "STOP"][0]["operador"] in ("<", "<=") else "CORTO",
                                "stop_precio": [c for c in e["propuesta"]["salida"]["condiciones"] if c["tipo"] == "STOP"][0]["umbral"],
                                "instrumento": e["propuesta"]["entrada"]["instrumento"], "activo_base": e["propuesta"]["entrada"]["activo_base"],
                                "condiciones_salida": copy.deepcopy(e["propuesta"]["salida"]), "protecciones": list(prot), "propuestas": [],
                                "origen": "MANUAL" if manual else "G"}
        self.ordenes_usadas += [orden["orden_id"], *prot]
        self._anota(self.posiciones[pid], None, "ABIERTA", actor if manual else "G", ahora,
                    "ejecución manual declarada (CT-G-14)" if manual else "orden conciliada", orden["orden_id"])
        e["posicion_id"] = pid
        self._anota(e, e["estado"], "EJECUTADA", actor, ahora, "ejecutada", orden["orden_id"])
        return _r(True, "OK", "ejecutada", posicion_id=pid)

    @_seguro
    def registrar_manual(self, registro, ahora):
        """CT-G-14: el operador declara lo que hizo fuera del sistema. Vinculado a un expediente AUTORIZADA abre su posición;
        vinculado a una posición la cierra; LIBRE solo queda registrado y la conciliación lo cuenta como explicado."""
        a = self._ahora(ahora)
        if not isinstance(registro, dict) or not isinstance(registro.get("event_id"), str):
            return _no("O-01", "registro CT-G-14 sin event_id")
        v = registro.get("vinculo") if isinstance(registro.get("vinculo"), dict) else {}
        ref = v.get("id") if isinstance(v.get("id"), str) else None
        h = _hash(registro)
        dup = self._duplicado(registro["event_id"], h, ref, ahora)
        if dup:
            return dup
        e = self.expedientes.get(ref) if v.get("tipo") == "EXPEDIENTE" else None
        p = self.posiciones.get(ref) if v.get("tipo") == "POSICION" else None
        if (e is not None and not (self._historial_ok(e) and self._propuesta_ok(e))) or (p is not None and not self._historial_ok(p)):
            return _no("O-13", "el historial del vínculo no es íntegro")
        ins = registro.get("instrumento")
        ocupado = any(q["estado"] != "CERRADA" and q["instrumento"] == ins for q in self.posiciones.values()) \
            or any(x["estado"] == "AUTORIZADA" and x.get("propuesta", {}).get("entrada", {}).get("instrumento") == ins for x in self.expedientes.values())
        desde = None
        if e is not None:
            desde = next((x["ahora"] for x in reversed(e["historial"]) if x["hasta"] == "AUTORIZADA"), None)
        elif p is not None:
            desde = p["historial"][0]["ahora"]
        fallos = validar_manual(registro, {"ahora": ahora, "expediente": e, "posicion": p, "tolerancia_precio": self.cfg["tolerancia_precio_entrada"],
                                           "instrumentos_permitidos": self.cfg["instrumentos_permitidos"],
                                           "instrumento_ocupado": ocupado, "no_antes_de": desde})
        if fallos:
            return _no("O-01", f"registro CT-G-14 no válido: {fallos[0]['regla']}: {fallos[0]['mensaje'][:80]}", reglas=sorted({x['regla'] for x in fallos}))
        if registro["ref_intermediario"] in self.ordenes_usadas or registro.get("proteccion_ref") in self.ordenes_usadas \
                or registro["ref_intermediario"] == registro.get("proteccion_ref"):
            return _no("O-03", "esa orden del intermediario ya está registrada")
        if v["tipo"] == "EXPEDIENTE":
            orden = {"orden_id": registro["ref_intermediario"], "cantidad": registro["cantidad"], "precio": registro["precio"], "conciliada": True,
                     "proteccion_orden_ids": [registro["proteccion_ref"]]}
            r = self._ejecutar(e, orden, "OPERADOR", ahora, a, manual=True)
            if not r["ok"]:
                return r
        elif v["tipo"] == "POSICION":
            self._anota(p, p["estado"], "CERRANDO", "OPERADOR", ahora, f"cierre manual declarado (CT-G-14): {registro['motivo'][:120]}")
            p["cantidad"] = 0
            self.ordenes_usadas.append(registro["ref_intermediario"])
            self._anota(p, "CERRANDO", "CERRADA", "OPERADOR", ahora, "cierre manual declarado (CT-G-14)", registro["ref_intermediario"])
        else:   # LIBRE: fuera del control de F; queda a la vista del operador
            self.ordenes_usadas.append(registro["ref_intermediario"])
            self._aviso("O-20", f"operación libre declarada fuera del sistema (sin control de F ni stop): {registro['lado']} {registro['cantidad']} {ins}",
                        ahora, registro["event_id"])
        self.eventos[registro["event_id"]] = {"hash": h, "expediente_id": ref}
        self.manuales.append(copy.deepcopy(registro))
        return _r(True, "OK", f"registro manual aceptado ({v['tipo']})", posicion_id=(e or {}).get("posicion_id") or (p or {}).get("posicion_id"))

    @_seguro
    def observar(self, expediente_id, condiciones_reapertura, motivo, actor, ahora):
        self._ahora(ahora)
        e, err = self._exp(expediente_id)
        if err:
            return err
        err = self._transicion_ok(e, "EN_OBSERVACION", actor)
        if err:
            return err
        if e["retenido"] is not None:
            return _no("O-17", "hay una objeción crítica pendiente: no se puede aparcar el expediente")
        if not (isinstance(motivo, str) and motivo.strip() and isinstance(condiciones_reapertura, list) and condiciones_reapertura
                and all(isinstance(c, str) and c.strip() for c in condiciones_reapertura)):
            return _no("O-15", "se exigen motivo y condiciones de reapertura")
        e["reapertura"] = list(condiciones_reapertura)
        self._anota(e, e["estado"], "EN_OBSERVACION", actor, ahora, motivo)
        return _r(True, "OK", "en observación")

    @_seguro
    def descartar(self, expediente_id, motivo, actor, ahora):
        self._ahora(ahora)
        e, err = self._exp(expediente_id)
        if err:
            return err
        err = self._transicion_ok(e, "DESCARTADA", actor)
        if err:
            return err
        if not (isinstance(motivo, str) and motivo.strip()):
            return _no("O-15", "el descarte exige motivo")
        self._anota(e, e["estado"], "DESCARTADA", actor, ahora, motivo)
        return _r(True, "OK", "descartada")

    @_seguro
    def barrer(self, ahora):
        """Caduca lo vencido. Solo la ejecuta el Orquestador."""
        a = self._ahora(ahora)
        cambios = []
        self._caducar_encargos(a, ahora)
        for eid, en in self.encargos.items():
            if en["estado"] == "EN_CURSO" and a > _dt(en["entrega_antes_de"]):
                self._aviso("O-10", f"encargo {eid}: pasó la hora de entrega sin sobre", ahora, en["expediente_id"])
                cambios.append(("aviso_entrega", eid, "EN_CURSO"))
        for eid, e in self.expedientes.items():
            if e["estado"] in ("VALIDADA", "COMPARADA", "PROPUESTA", "AUTORIZADA"):
                limites = [_dt(e["sobre"]["valid_until"])]
                if e["propuesta"]:
                    limites.append(_dt(e["propuesta"]["entrada"]["ventana_hasta"]))
                if a > min(limites) or self._sello_anulado(e):
                    self._anota(e, e["estado"], "CADUCADA", "ORQUESTADOR", ahora, "venció valid_until o la ventana de entrada")
                    self._aviso("O-10", f"expediente {eid} caducó sin decidirse", ahora, eid)
                    cambios.append(("expediente", eid, "CADUCADA"))
        for sid, s in self.sellos.items():
            if s["estado"] == "VIGENTE" and estado_sello(s, str(a.astimezone(timezone.utc).date()), s["cartera"], self.cal_def) == "CADUCADO":
                s["estado"] = "CADUCADO"
                self._aviso("O-10", f"el sello {sid} caducó por antigüedad", ahora, sid)
                cambios.append(("sello", sid, "CADUCADO"))
        return _r(True, "OK", f"{len(cambios)} cambio(s)", cambios=cambios)

    # ------------------------------------------------------------ posiciones
    def _pos(self, pid):
        p = self.posiciones.get(pid)
        if p is None:
            return None, _no("O-12", f"posición inexistente: {pid!r}")
        if not self._historial_ok(p):
            return None, _no("O-13", "el historial de la posición no es íntegro")
        return p, None

    @_seguro
    def proponer_sobre_posicion(self, posicion_id, texto, actor, ahora):
        """H (o quien sea) propone; una invalidez cualitativa nunca vende."""
        self._ahora(ahora)
        p, err = self._pos(posicion_id)
        if err:
            return err
        if not (isinstance(texto, str) and texto.strip()):
            return _no("O-15", "la propuesta exige texto")
        p["propuestas"].append({"actor": actor, "texto": texto, "ahora": ahora})
        return _r(True, "OK", "propuesta registrada; no cambia el estado de la posición")

    @_seguro
    def posicion_transicion(self, posicion_id, hasta, actor, ahora, condicion=None, restante=None, orden=None, motivo=None):
        self._ahora(ahora)
        p, err = self._pos(posicion_id)
        if err:
            return err
        if p["estado"] == "CERRADA":
            return _no("O-14", "CERRADA es un estado terminal")
        if not isinstance(actor, str) or not isinstance(hasta, str):
            return _no("O-01", "actor y estado deben ser texto")
        quien = TP.get((p["estado"], hasta))
        if quien is None:
            return _no("O-04", f"transición no permitida: {p['estado']} -> {hasta}")
        if actor not in quien:
            return _no("O-05", f"{actor!r} no puede pedir {p['estado']} -> {hasta}")
        ref = None
        if hasta in ("REDUCIENDO", "CERRANDO"):
            if actor == "OPERADOR":
                if not (isinstance(motivo, str) and motivo.strip()):
                    return _no("O-15", "la decisión manual del operador exige motivo")
            else:   # automático: solo por una condición numérica declarada de antemano
                stop_ids = {c["id"] for c in p["condiciones_salida"]["condiciones"] if c["tipo"] == "STOP"}
                hecho = (hasta == "CERRANDO" and isinstance(condicion, dict) and condicion.get("id") in stop_ids
                         and condicion.get("stop_ejecutado_orden_id") in p["protecciones"])   # el stop propio ya saltó en el intermediario
                if not hecho and NIVELES[self.nivel(p["cartera"])] < 2:
                    return _no("O-05", f"la cartera está en {self.nivel(p['cartera'])}: el cierre automático solo desde L2; lo confirma el operador")
                declaradas = {c["id"]: c for c in p["condiciones_salida"]["condiciones"]}
                if not (isinstance(condicion, dict) and condicion.get("id") in declaradas and _num(condicion.get("valor_observado"))):
                    return _no("O-06", "una reducción o cierre automático exige una condición numérica declarada y su valor observado")
                c = declaradas[condicion["id"]]
                if not OPERADORES[c["operador"]](condicion["valor_observado"], c["umbral"]):
                    return _no("O-06", "la condición declarada no se cumple con el valor observado")
                ref = c["id"]
        if hasta == "ABIERTA" and p["estado"] == "EN_REVISION":
            if not (isinstance(motivo, str) and motivo.strip()):
                return _no("O-15", "confirmar la tesis exige motivo")
        if p["estado"] in ("REDUCIENDO", "CERRANDO"):
            ok = (isinstance(orden, dict) and orden.get("conciliada") is True and isinstance(orden.get("orden_id"), str)
                  and _num(restante) and 0 <= restante <= p["cantidad"])
            if not ok:
                return _no("O-06", "se exige orden conciliada y cantidad restante")
            if (hasta == "CERRADA") != (restante == 0):
                return _no("O-06", "CERRADA exige restante 0; ABIERTA, restante mayor que 0")
            if p["estado"] == "CERRANDO" and restante != 0:
                return _no("O-06", "CERRANDO solo termina en CERRADA")
            propia = hasta == "CERRADA" and orden["orden_id"] in p["protecciones"]   # el cierre puede ser el propio stop que saltó
            if orden["orden_id"] in self.ordenes_usadas and not propia:
                return _no("O-03", "orden ya usada")
            if not propia:
                self.ordenes_usadas.append(orden["orden_id"])
            p["cantidad"] = restante
            ref = orden["orden_id"]
        self._anota(p, p["estado"], hasta, actor, ahora, motivo or "transición de posición", ref)
        return _r(True, "OK", f"posición {hasta}")

    @_seguro
    def reclasificar(self, posicion_id, nueva_cartera, actor, motivo, ahora):
        self._ahora(ahora)
        p, err = self._pos(posicion_id)
        if err:
            return err
        if actor != "OPERADOR":
            return _no("O-05", "reclasificar una posición exige la aprobación del operador")
        if nueva_cartera not in ("TRADING", "TACTICA", "LARGO_PLAZO") or not (isinstance(motivo, str) and motivo.strip()):
            return _no("O-15", "cartera destino y motivo obligatorios")
        antes = p["cartera"]
        p["cartera"] = nueva_cartera
        self._anota(p, p["estado"], p["estado"], actor, ahora, f"reclasificada {antes} -> {nueva_cartera}: {motivo}")
        return _r(True, "OK", "reclasificada")
