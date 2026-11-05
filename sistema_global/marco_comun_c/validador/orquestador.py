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
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from k_calidad import (Calendario, ERRORES, SinCobertura, estado_sello, hash_serie,  # noqa: E402
                       validar_sello)
from validar_encargo import sobre_responde_a_encargo, validar_encargo  # noqa: E402
from validar_sobre import _dt  # noqa: E402
from manual_g import neto_libre, validar_manual, via_norm  # noqa: E402
from comparador import MARGEN_AJUSTADO, REFERENCIA_EFECTIVO, _referencia_ok, comparar_candidatos  # noqa: E402
from dimensionado import dimensionar  # noqa: E402
from validar_contradictor import validar_informe  # noqa: E402
from control_f import POLITICA_DEFECTO, controlar, divisa_cotizada, par_divisas, politica_valida, tipo_cambio, validar_informe_f  # noqa: E402

VERSION_REGLAS = "ORQ-0.1.0"
_FH = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})\Z")
_ID = re.compile(r"^[A-Za-z0-9._:/-]{1,64}\Z")
GESTORES = {"GESTOR_TRADING", "GESTOR_TACTICA", "GESTOR_LARGO_PLAZO"}
GESTOR_DE = {"TRADING": "GESTOR_TRADING", "TACTICA": "GESTOR_TACTICA", "LARGO_PLAZO": "GESTOR_LARGO_PLAZO"}
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
    ("REDUCIENDO", "EN_REVISION"): {"G"},   # una reducción no confirma la tesis: vuelve al estado del que salió
    ("REDUCIENDO", "CERRADA"): {"G"},
    ("REDUCIENDO", "CERRANDO"): {"F", "G", "ORQUESTADOR", "OPERADOR"},   # cerrar del todo una posición a media reducción
    ("CERRANDO", "CERRADA"): {"G"},
}
OPERADORES = {"<": lambda v, u: v < u, "<=": lambda v, u: v <= u, ">": lambda v, u: v > u,
              ">=": lambda v, u: v >= u, "==": lambda v, u: v == u}

CONFIG_DEFECTO = {"max_reintentos": 3, "umbral_corte_comun_dias_habiles": 0,
                  "dia_coste_max_eur": 50.0, "revision_max_dias": 90, "dia_tiempo_max_min": 600, "tolerancia_precio_entrada": 0.05,
                  "exige_contradictor_en": [], "matriz_autonomia": {}, "politica_f": POLITICA_DEFECTO,
                  "nivel_autonomia": {}, "tolerancia_conciliacion_rel": 0.0, "instrumentos_permitidos": None,
                  "referencias": {c: dict(REFERENCIA_EFECTIVO) for c in ("TRADING", "TACTICA", "LARGO_PLAZO")},   # benchmark de cada cartera [PROPUESTO]
                  # [PROPUESTO] controles sobre el operador (§6) y avisos (§11); los canales reales los fija el operador (D-07, P-08)
                  "aprobacion": {"caduca_min": 15, "canales": ["CONSOLA"], "enfriamiento_min": 30, "enfriamiento_tras_perdida_dia_eur": 0.0,
                                 "horario_utc": ["07:00", "21:00"]},
                  "avisos": {"canal_alta": "CONSOLA", "canal_escalado": "ESCALADO", "reiterar_min": 15, "escalar_tras": 3},
                  "kill_switch": {"periodo_min_l1_horas": 24},
                  "divisas_cotizacion": {},   # instrumento -> divisa en que cotiza, si no es un par de divisas ISO
                  # [PROPUESTO] rangos plausibles de euros por unidad; un tipo fuera de rango o sin rango no se acepta (D-21)
                  "rangos_tipo_cambio_eur": {"USD": [0.6, 1.4], "GBP": [0.9, 1.6], "JPY": [0.003, 0.015], "CHF": [0.7, 1.4], "AUD": [0.4, 0.9],
                                             "CAD": [0.45, 0.95], "SEK": [0.06, 0.13], "NOK": [0.06, 0.13], "DKK": [0.12, 0.15]},
                  "tolerancia_tipo_par_pct": 15.0,   # [PROPUESTO] desvío máximo entre el tipo de la foto y el que implica el límite de un par con el euro
                  "cuenta_intermediario": "SIM-1"}    # la cuenta de la que G toma las fotos (D-21)   # cartera -> L0 (simulado) | L1 (el operador confirma) | L2 (automático con límites); sin dato = L1
NIVELES = {"L0": 0, "L1": 1, "L2": 2}
# Prioridad de cada aviso para el operador [PROPUESTO]
TIPOS_KILL = {"POSICION_DESCONOCIDA", "CANTIDAD", "SENTIDO_O_ACTIVO", "PROTECCION", "PROTECCION_HUERFANA", "ENTRADA_HUERFANA",
              "MANUAL_NO_CUADRA", "POSICION_SIN_PROTEGER", "INTEGRIDAD"}   # lo que G sabe explicar (cierres propios, conexión, estado incierto, dato viejo) no
PRIORIDAD_AVISO = {"O-20": "MEDIA", "O-30": "ALTA", "O-25": "ALTA", "O-26": "ALTA", "O-19": "ALTA", "O-18": "ALTA", "O-03": "ALTA", "O-08": "ALTA", "O-09": "ALTA", "O-13": "ALTA", "O-17": "ALTA"}
ACTORES_PROPUESTA = set(EMISORES)   # quien propone no aprueba ni controla: F, D y H no proponen (Constitución §2, P1)


_via = via_norm   # identidad de una vía de acceso (texto libre del sobre), la misma en CT-G-14 y en R-14


_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}\Z")


def _ins(x):
    """Identidad de un instrumento: «EUR/USD» y «EURUSD» son el mismo."""
    return re.sub(r"[^A-Z0-9]", "", x.upper()) if isinstance(x, str) else None


MAX_EDAD_DIMENSIONADO_MIN = 60   # [PROPUESTO] el cálculo de E no puede ser más viejo que esto al proponer


_HM = re.compile(r"^([01]\d|2[0-3]):[0-5]\d\Z")


def _aprob_ok(a):
    return (isinstance(a, dict) and set(a) == {"caduca_min", "canales", "enfriamiento_min", "enfriamiento_tras_perdida_dia_eur", "horario_utc"}
            and _num(a["caduca_min"]) and 0 < a["caduca_min"] <= 120 and isinstance(a["canales"], list) and a["canales"]
            and all(isinstance(x, str) and x and x.upper() != "CHAT" for x in a["canales"])
            and _num(a["enfriamiento_min"]) and a["enfriamiento_min"] >= 0 and _num(a["enfriamiento_tras_perdida_dia_eur"])
            and a["enfriamiento_tras_perdida_dia_eur"] >= 0 and isinstance(a["horario_utc"], list) and len(a["horario_utc"]) == 2
            and all(isinstance(x, str) and _HM.match(x) for x in a["horario_utc"]) and a["horario_utc"][0] != a["horario_utc"][1])


def _en_horario(a, horario):
    """Horario supervisado [desde, hasta] en UTC; admite cruzar la medianoche (p. ej. 22:00-06:00)."""
    hm = a.astimezone(timezone.utc).strftime("%H:%M")
    d, h = horario
    return d <= hm <= h if d < h else (hm >= d or hm <= h)


def _avisos_ok(a):
    return (isinstance(a, dict) and set(a) == {"canal_alta", "canal_escalado", "reiterar_min", "escalar_tras"}
            and all(isinstance(a[k], str) and a[k] and a[k].upper() != "CHAT" for k in ("canal_alta", "canal_escalado"))
            and a["canal_escalado"] != a["canal_alta"] and _num(a["reiterar_min"]) and a["reiterar_min"] > 0
            and isinstance(a["escalar_tras"], int) and not isinstance(a["escalar_tras"], bool) and a["escalar_tras"] >= 1)


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
          and _aprob_ok(c["aprobacion"]) and _avisos_ok(c["avisos"])
          and isinstance(c["kill_switch"], dict) and set(c["kill_switch"]) == {"periodo_min_l1_horas"} and _num(c["kill_switch"]["periodo_min_l1_horas"])
          and c["kill_switch"]["periodo_min_l1_horas"] >= 0
          and isinstance(c["rangos_tipo_cambio_eur"], dict)
          and all(isinstance(k, str) and re.fullmatch(r"[A-Z]{3}", k) and isinstance(v, list) and len(v) == 2 and all(_num(x) and x > 0 for x in v)
                  and v[0] < v[1] for k, v in c["rangos_tipo_cambio_eur"].items())
          and _num(c["tolerancia_tipo_par_pct"]) and 0 < c["tolerancia_tipo_par_pct"] <= 50
          and isinstance(c["revision_max_dias"], int) and not isinstance(c["revision_max_dias"], bool) and 1 <= c["revision_max_dias"] <= 366
          and isinstance(c["cuenta_intermediario"], str) and _ID.match(c["cuenta_intermediario"])
          and isinstance(c["divisas_cotizacion"], dict)
          and all(isinstance(k, str) and isinstance(v, str) and re.fullmatch(r"[A-Z]{3}", v) for k, v in c["divisas_cotizacion"].items())
          and isinstance(c["referencias"], dict) and set(c["referencias"]) == {"TRADING", "TACTICA", "LARGO_PLAZO"}
          and all(_referencia_ok(v) for v in c["referencias"].values())
          and (c["instrumentos_permitidos"] is None or isinstance(c["instrumentos_permitidos"], dict)
               and all(k in ("TRADING", "TACTICA", "LARGO_PLAZO") and isinstance(v, list) and all(isinstance(x, str) for x in v)
                       for k, v in c["instrumentos_permitidos"].items())))
    if ok and not c["apalancamiento_permitido"] and c["politica_f"]["apalancamiento_max"] > 1:
        ok = False   # la política de F no puede permitir lo que el sistema prohíbe
    if not ok:
        raise ValueError("configuración del Orquestador inválida")


TOL_Q = 1e-6   # tolerancia de cantidades (la misma que G)
# Lo que define el control de una posición: va en la cadena de su historial (cada anotación lleva su hash)
CAMPOS_POS = ("posicion_id", "expediente_id", "estado", "cantidad", "cantidad_inicial", "cartera", "direccion", "instrumento", "activo_base",
              "stop_precio", "condiciones_salida", "via_acceso", "fecha_revision", "protecciones", "protecciones_anteriores", "reduccion", "reducciones", "condiciones_consumidas")


def _estado_pos(p):
    return {k: p.get(k) for k in CAMPOS_POS}


def _identidad(e):
    return {k: e.get(k) for k in ("expediente_id", "correlation_id", "via_entrada", "cartera_destino")}


VIVOS = ("VALIDADA", "COMPARADA", "PROPUESTA", "AUTORIZADA")   # candidato con análisis, en juego


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
        self.pantallas = {}            # expediente -> pantalla de aprobación con las cifras de F (§6)
        self.kill = None               # kill-switch activo: {"motivo", "actor", "ahora"}
        self.rearmes = []              # rehabilitaciones tras el kill-switch
        self.ultima_conciliacion = None   # {"ahora", "limpia"}: la anota G cada vez que concilia
        self.fotos = {}                   # hash -> foto de cartera tomada por G del intermediario (T-11), para auditoría
        self.ultima_foto = None           # la única que vale: la más reciente
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
            self._aviso("O-19", f"cartera {cartera} degradada a L1: {motivo[:120]}", ahora, cartera, carteras={cartera})

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
        if _dt(ahora) < _dt(self.degradadas[cartera]["ahora"]):
            return _no("O-16", "el restablecimiento no puede ser anterior a la degradación")
        pend = [x for x in self.avisos if x["acuse"] is None and x["codigo"] in ("O-18", "O-19", "O-26")
                and (x["codigo"] == "O-26" or x.get("carteras") is None or cartera in x["carteras"])]
        if pend:   # T-29: solo los avisos que afectan a esta cartera (y los que no se pueden atribuir)
            return _no("O-06", f"hay avisos de discrepancia, degradación o kill-switch sin acusar que afectan a {cartera}: {pend[0]['id']}")
        if self.kill is not None:
            return _no("O-26", "el kill-switch está activo: primero hay que rearmarlo")
        if self.rearmes and (_dt(ahora) - _dt(self.rearmes[-1]["ahora"])).total_seconds() < self.cfg["kill_switch"]["periodo_min_l1_horas"] * 3600:
            return _no("O-26", "tras el kill-switch la cartera sigue en L1 durante el periodo mínimo")
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

    def _aviso(self, codigo, motivo, ahora, ref=None, carteras=None):
        if any(x["acuse"] is None and x["codigo"] == codigo and x["ref"] == ref and x["motivo"] == motivo for x in self.avisos):
            return   # ya hay uno igual sin acusar: no se multiplica
        prio = PRIORIDAD_AVISO.get(codigo, "MEDIA")
        self.avisos.append({"id": f"AV-{len(self.avisos) + 1:05d}", "codigo": codigo, "prioridad": prio,
                            "motivo": motivo, "ref": ref, "ahora": ahora, "acuse": None,
                            "canal": self.cfg["avisos"]["canal_alta"] if prio == "ALTA" else "CONSOLA", "reiteraciones": [], "escalado": False,
                            "carteras": sorted(carteras) if carteras is not None else None})

    def _carteras_de(self, ref):
        """Carteras a las que pertenece la referencia de una discrepancia o un aviso: una posición, un expediente, una cartera o un
        instrumento (posiciones abiertas, autorizaciones y operaciones libres en él). Vacío si no se puede atribuir."""
        if not isinstance(ref, str):
            return set()
        coincide = [ref in ("TRADING", "TACTICA", "LARGO_PLAZO"), ref in self.posiciones, ref in self.expedientes]
        if sum(coincide) > 1:   # una referencia ambigua (un id que es a la vez otra cosa) no se atribuye: degrada todas
            return set()
        if coincide[0]:
            return {ref}
        if coincide[1]:
            p = self.posiciones[ref]
            return {p["cartera"]} if self._posicion_ok(p) and p["cartera"] in GESTOR_DE else set()   # alterada: no se fía de su cartera
        if coincide[2]:
            x = self.expedientes[ref]
            return {x["cartera_destino"]} if self._todo_ok(x) and x["cartera_destino"] in GESTOR_DE else set()
        ins = _ins(ref)
        cs = {p["cartera"] for p in self.posiciones.values() if p["estado"] != "CERRADA" and _ins(p["instrumento"]) == ins}
        cs |= {x["cartera_destino"] for x in self.expedientes.values()
               if x["estado"] in ("AUTORIZADA", "EJECUTADA") and x.get("propuesta") and _ins(x["propuesta"]["entrada"]["instrumento"]) == ins}
        cs |= {r["cartera"] for r in self.manuales if r["vinculo"]["tipo"] == "LIBRE" and _ins(r["instrumento"]) == ins}
        return cs if cs <= set(GESTOR_DE) else set()

    @_seguro
    def reportar_discrepancia(self, diferencias, actor, ahora):
        """G informa de que lo que el intermediario tiene no coincide con lo que el Orquestador cree."""
        self._ahora(ahora)
        if actor != "G":
            return _no("O-05", "solo G reporta discrepancias de conciliación")
        if not (isinstance(diferencias, list) and diferencias and all(isinstance(d, dict) and isinstance(d.get("tipo"), str) for d in diferencias)):
            return _no("O-01", "una discrepancia exige una lista no vacía de diferencias con tipo")
        for d in diferencias:   # T-29: la atribución se fija al avisar (no cambia si luego se reclasifica algo)
            cs = self._carteras_de(d.get("ref"))
            self._aviso("O-18", f"conciliación: {d['tipo']} {d.get('ref')}: {str(d.get('detalle'))[:120]}", ahora,
                        d.get("ref") if isinstance(d.get("ref"), str) else None, carteras=cs or set(GESTOR_DE))
        afectadas = set()   # T-29: cada diferencia degrada la cartera de su posición, expediente o instrumento; si no se puede atribuir, todas
        for d in diferencias:
            cs = self._carteras_de(d.get("ref"))
            afectadas |= cs if cs else {"TRADING", "TACTICA", "LARGO_PLAZO"}
        for c in sorted(afectadas):
            self._degradar(c, f"discrepancia de conciliación ({', '.join(sorted({d['tipo'] for d in diferencias}))[:80]})", ahora)
        graves = sorted({d["tipo"] for d in diferencias} & TIPOS_KILL)
        if graves:   # §11: una discrepancia sin explicar (o una posición sin proteger) dispara el kill-switch
            self._activar_kill(f"discrepancia sin explicar con el intermediario ({', '.join(graves)})", "ORQUESTADOR", ahora)
        return _r(True, "OK", f"{len(diferencias)} diferencia(s) registrada(s)")

    # ------------------------------------------------------------ kill-switch (§8 y §11)
    def _activar_kill(self, motivo, actor, ahora):
        if self.kill is None:
            self.kill = {"motivo": motivo[:200], "actor": actor, "ahora": ahora}
            self._aviso("O-26", f"KILL-SWITCH activado por {actor}: {motivo[:120]}", ahora)
        for c in ("TRADING", "TACTICA", "LARGO_PLAZO"):
            self._degradar(c, f"kill-switch: {motivo[:80]}", ahora)

    @_seguro
    def activar_kill_switch(self, motivo, actor, ahora):
        """Interruptor manual del operador o automático (Orquestador, vigilante). Bloquea autorizaciones y órdenes de entrada
        nuevas y pasa todo a L1; G cancela las entradas vivas. No cancela protecciones ni liquida posiciones."""
        self._ahora(ahora)
        if actor not in ("OPERADOR", "ORQUESTADOR", "VIGILANTE"):
            return _no("O-05", "solo el operador, el Orquestador o el vigilante activan el kill-switch")
        if not (isinstance(motivo, str) and motivo.strip()):
            return _no("O-15", "el kill-switch exige motivo")
        if self.kill is not None:
            return _r(True, "O-02", "el kill-switch ya está activo", duplicado=True)
        self._activar_kill(motivo, actor, ahora)
        return _r(True, "OK", "kill-switch activo: G debe cancelar las órdenes de entrada vivas")

    @_seguro
    def registrar_conciliacion(self, limpia, actor, ahora):
        """G anota el resultado de cada conciliación (limpia o no): el rearme exige una limpia posterior al kill-switch."""
        self._ahora(ahora)
        if actor != "G" or not isinstance(limpia, bool):
            return _no("O-05", "solo G anota conciliaciones, con un resultado booleano")
        self.ultima_conciliacion = {"ahora": ahora, "limpia": limpia}
        return _r(True, "OK", "conciliación anotada")

    @_seguro
    def registrar_cartera(self, foto, actor, ahora, cuenta=None):
        """G registra la foto de cartera que ha tomado del intermediario. E y F solo valen con una foto registrada (T-11)."""
        a = self._ahora(ahora)
        if actor != "G":
            return _no("O-05", "solo G registra el estado de cartera del intermediario")
        ok = (isinstance(foto, dict) and set(foto) == {"fecha_hora", "capital_eur", "perdida_dia_eur", "posiciones", "tipos_cambio_eur"}
              and isinstance(foto["fecha_hora"], str) and _FH.match(foto["fecha_hora"]) and _num(foto["capital_eur"]) and foto["capital_eur"] > 0
              and _num(foto["perdida_dia_eur"]) and foto["perdida_dia_eur"] >= 0 and isinstance(foto["posiciones"], list)
              and isinstance(foto["tipos_cambio_eur"], dict)
              and all(isinstance(k, str) and re.fullmatch(r"[A-Z]{3}", k) and _num(v) and v > 0 for k, v in foto["tipos_cambio_eur"].items()))
        ok = ok and all(isinstance(p, dict) and set(p) == {"instrumento", "activo_base", "valor_eur"} and isinstance(p["instrumento"], str)
                        and isinstance(p["activo_base"], str) and _num(p["valor_eur"]) and p["valor_eur"] >= 0 for p in foto["posiciones"])
        if not ok:
            return _no("O-01", "foto de cartera mal formada")
        if cuenta != self.cfg["cuenta_intermediario"]:
            return _no("O-29", "la foto no es de la cuenta del intermediario configurada")
        rangos = self.cfg["rangos_tipo_cambio_eur"]
        fuera = sorted(k for k, v in foto["tipos_cambio_eur"].items() if k not in rangos or not rangos[k][0] <= v <= rangos[k][1])
        if fuera:
            return _no("O-29", f"tipo de cambio sin rango de referencia o fuera de él: {', '.join(fuera)}")
        t = _dt(foto["fecha_hora"])
        if t > a or (a - t).total_seconds() > self.cfg["politica_f"]["frescura_max_min"] * 60:
            return _no("O-10", "la foto de cartera es del futuro o más vieja que la frescura que admite F")
        if self.ultima_foto and t < _dt(self.ultima_foto["fecha_hora"]):
            return _no("O-10", "la foto es anterior a la última registrada")
        h = _hash(foto)
        self.fotos[h] = {"ahora": ahora, "fecha_hora": foto["fecha_hora"]}
        self.ultima_foto = copy.deepcopy(foto)
        if len(self.fotos) > 200:   # solo hacen falta las recientes
            for k in sorted(self.fotos, key=lambda k: _dt(self.fotos[k]["ahora"]))[:len(self.fotos) - 200]:
                del self.fotos[k]
        return _r(True, "OK", "foto de cartera registrada", hash=h)

    def cartera_f(self):
        """La única cartera que E y F pueden usar: la última foto de G más las autorizaciones que aún no están en el
        intermediario (sin orden o con la orden de entrada viva), valoradas en euros con los tipos de esa foto."""
        if self.ultima_foto is None:
            return None
        c = copy.deepcopy(self.ultima_foto)
        for k in sorted(self.expedientes):
            e = self.expedientes[k]
            oe = e.get("orden_entrada")
            if e["estado"] == "AUTORIZADA" and (oe is None or oe["estado"] in ("ENVIADA", "RECHAZADA", "CANCELADA", "DESHECHA")):
                en = e["propuesta"]["entrada"]
                fx = tipo_cambio(self.divisa(en["instrumento"]), c)
                if fx is None:
                    return None
                c["posiciones"].append({"instrumento": en["instrumento"], "activo_base": en["activo_base"],
                                        "valor_eur": e["control_f"]["cantidad_aprobada"] * en["limite"] * fx})
        return c

    def _foto_de_g(self, cart, instrumento=None, limite=None):
        cf = self.cartera_f()
        if cf is None or not isinstance(cart, dict) or _hash(cart) != _hash(cf):
            return _no("O-29", "la cartera no es la vigente: la última foto de G del intermediario más las autorizaciones pendientes")
        par = par_divisas(instrumento) if instrumento else None
        if par and par[0] == "EUR" and _num(limite) and limite > 0:   # en un par con el euro, el tipo de la foto debe cuadrar con el precio
            fx = tipo_cambio(par[1], cart)
            if fx is None or abs(fx * limite - 1) * 100 > self.cfg["tolerancia_tipo_par_pct"]:
                return _no("O-29", f"el tipo de cambio de {par[1]} no cuadra con el precio del par")
        return None

    def divisa(self, instrumento):
        return divisa_cotizada(instrumento, self.cfg["divisas_cotizacion"])

    LISTA_REHABILITACION = ("causa_corregida", "conciliacion_limpia", "datos_frescos", "protecciones_verificadas")

    @_seguro
    def rearmar_kill_switch(self, lista, actor, ahora):
        """Rehabilitación manual con la lista del §11. Las carteras siguen en L1 un periodo mínimo antes de poder restablecerse."""
        self._ahora(ahora)
        if actor != "OPERADOR":
            return _no("O-05", "solo el operador rearma tras el kill-switch")
        if self.kill is None:
            return _no("O-12", "el kill-switch no está activo")
        if not (isinstance(lista, dict) and set(lista) == set(self.LISTA_REHABILITACION) and all(v is True for v in lista.values())):
            return _no("O-06", "la lista de rehabilitación debe venir completa y con todo comprobado: " + ", ".join(self.LISTA_REHABILITACION))
        if any(x["acuse"] is None and x["prioridad"] == "ALTA" for x in self.avisos):
            return _no("O-06", "hay avisos de prioridad alta sin acusar")
        vivas = sorted(k for k, x in self.expedientes.items() if self._entrada_viva(x))
        if vivas:
            return _no("O-06", f"quedan órdenes de entrada vivas sin cancelar: {', '.join(vivas)}")
        uc = self.ultima_conciliacion
        if not (uc and uc["limpia"] and _dt(uc["ahora"]) >= _dt(self.kill["ahora"])):
            return _no("O-06", "falta una conciliación limpia con el intermediario posterior al kill-switch")
        self.rearmes.append({"kill": self.kill, "lista": dict(lista), "ahora": ahora})
        self.kill = None
        return _r(True, "OK", f"rearmado; las carteras siguen en L1 al menos {self.cfg['kill_switch']['periodo_min_l1_horas']} h")

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
        if _dt(ahora) < _dt(av["ahora"]):
            return _no("O-16", "el acuse no puede ser anterior al aviso")
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

    def _posicion_ok(self, p):
        """Historial íntegro y el estado de control de la posición (cantidad, stops, reducción) es el anotado en la cadena."""
        return self._historial_ok(p) and p["historial"][-1].get("datos") == _hash(_estado_pos(p))

    def posicion_integra(self, posicion_id):
        """Para G y H antes de enviar nada al intermediario por una posición (también al retomar un cierre o una reducción)."""
        p = self.posiciones.get(posicion_id)
        return p is not None and self._posicion_ok(p)

    def _anota_pos(self, p, desde, hasta, actor, ahora, motivo, ref=None):
        p["estado"] = hasta
        self._anota(p, desde, hasta, actor, ahora, motivo, ref, datos=_hash(_estado_pos(p)))

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
        if not s or "documento" not in s:   # sin sobre solo si nunca se validó
            return not any(h["hasta"] == "VALIDADA" for h in e["historial"])
        ult = [h for h in e["historial"] if h["hasta"] == "VALIDADA"]
        return bool(ult) and ult[-1]["datos"] == self._huella_sobre(e) and s["hash"] == _hash(s["documento"])

    @staticmethod
    def _huella_sobre(e):
        """Lo que se anota al validar: el sobre (con su vigencia, que puede acortar el Contradictor) y el informe del Contradictor."""
        return _hash({"sobre": {k: v for k, v in e["sobre"].items() if k != "documento"}, "contradictor": e.get("contradictor")})

    def _comparacion_ok(self, e):
        """El resultado de D (y la elección del operador) es el que se anotó en la cadena del historial."""
        c = e.get("comparacion")
        if not c:
            return True
        ult = [h for h in e["historial"] if h["hasta"] == "COMPARADA"]
        return bool(ult) and ult[-1]["datos"] == _hash(c)

    def _orden_ok(self, e):
        """El estado de la orden de entrada es el anotado en la cadena del historial."""
        oe = e.get("orden_entrada")
        if not oe:
            return True
        ult = [h for h in e["historial"] if h["hasta"] in ("AUTORIZADA", "EJECUTADA")]
        return bool(ult) and ult[-1]["datos"] == _hash(oe)

    @staticmethod
    def autorizada_por(e):
        """Quién autorizó de verdad (la transición a AUTORIZADA desde otro estado, no las anotaciones de la orden)."""
        return next((x["actor"] for x in reversed(e["historial"]) if x["hasta"] == "AUTORIZADA" and x["desde"] != "AUTORIZADA"), None)

    def autorizacion_vigente(self, e):
        """Una autorización automática deja de valer si la cartera bajó de nivel."""
        return not (self.autorizada_por(e) == "MATRIZ_AUTONOMIA" and NIVELES[self.nivel(e["cartera_destino"])] < 2)

    @staticmethod
    def _entrada_viva(e):
        """Hay una orden de entrada enviada al intermediario que G aún no ha resuelto: no se caduca ni se descarta a ciegas."""
        oe = e.get("orden_entrada")
        return bool(oe) and oe["estado"] == "ENVIADA" and e["estado"] == "AUTORIZADA"

    def _aprobacion_ok(self, e):
        """Lo autorizado (cantidad de F y, si autorizó el operador, su aprobación) es lo anotado al autorizar."""
        cf = e.get("control_f")
        if not cf:
            return True
        ult = [h for h in e["historial"] if h["hasta"] == "AUTORIZADA" and h["desde"] != "AUTORIZADA"]
        return bool(ult) and ult[-1]["datos"] == _hash(cf) and (ult[-1]["actor"] != "OPERADOR" or cf.get("aprobacion") is not None)

    def _todo_ok(self, e):
        return (self._historial_ok(e) and self._identidad_ok(e) and self._propuesta_ok(e) and self._sobre_ok(e) and self._comparacion_ok(e)
                and self._orden_ok(e) and self._aprobacion_ok(e))

    @staticmethod
    def _identidad_ok(e):
        """La cartera, la petición y el encargo vigente del expediente son los anotados (T-36: sin ellos se le saca de una comparación)."""
        h = e["historial"]
        if h[0]["datos"] != _hash(_identidad(e)):
            return False
        enc = [x["ref"] for x in h if x["hasta"] == "EN_ANALISIS" and x["motivo"] == "encargo emitido"]
        return e.get("encargo_actual") == (enc[-1] if enc else None)

    def _rota(self):
        """Primer expediente cuya integridad no cuadra (cualquier cartera), o None."""
        return next((k for k, x in sorted(self.expedientes.items()) if not self._todo_ok(x)), None)

    def integridad(self):
        """Lista de expedientes (EXP:) y posiciones (POS:) cuyo historial, sobre, comparación o propuesta no cuadra."""
        return sorted(["EXP:" + k for k, v in self.expedientes.items() if not self._todo_ok(v)]
                      + ["POS:" + k for k, v in self.posiciones.items() if not self._posicion_ok(v)])

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
        if not self._todo_ok(e):   # incidente de seguridad (§11): el registro se alteró fuera del Orquestador
            self._activar_kill(f"integridad rota en {eid}", "ORQUESTADOR", self.ultimo_ahora or "1970-01-01T00:00:00+00:00")
            return None, _no("O-13", "el historial, la propuesta, el sobre, la comparación, la orden o la aprobación del expediente no son íntegros")
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
        if v["hash"] != h:   # posible inyección o suplantación: incidente de seguridad (§11)
            self._aviso("O-03", f"event_id {eid} repetido con otro contenido", ahora, expediente_id)
            self._activar_kill(f"event_id {eid} repetido con otro contenido", "ORQUESTADOR", ahora)
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
                if en and en["sello_ref"] == viejo and x["estado"] in ("VALIDADA", "COMPARADA", "PROPUESTA", "AUTORIZADA") and not self._entrada_viva(x):
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
        if expediente_id in GESTOR_DE or expediente_id.startswith("POS-") or expediente_id in self.posiciones:
            return _no("O-01", "el identificador del expediente no puede ser el nombre de una cartera ni el de una posición")
        e = {"expediente_id": expediente_id, "correlation_id": correlation_id, "via_entrada": via_entrada,
             "cartera_destino": cartera_destino, "estado": "DETECTADA", "historial": [], "encargo_actual": None,
             "sobre": None, "contradictor": None, "retenido": None, "sin_avance": 0, "propuesta": None, "posicion_id": None, "reapertura": None}
        self._anota(e, None, "DETECTADA", actor, ahora, "detectada", datos=_hash(_identidad(e)))
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
        self._anota(e, e["estado"], "VALIDADA", "C", ahora, "sobre aceptado", sid, datos=self._huella_sobre(e))
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
                    datos=self._huella_sobre(e))
        return _r(True, "OK", "objeción levantada; expediente validado")

    def _candidato_vivo(self, x, cartera, a):
        """Candidato que debe entrar en cualquier comparación de la cartera: VALIDADA o COMPARADA, con sobre vigente y sello válido."""
        return (x["cartera_destino"] == cartera and x["estado"] in ("VALIDADA", "COMPARADA") and x.get("sobre")
                and a <= _dt(x["sobre"]["valid_until"]) and not self._sello_anulado(x))

    @staticmethod
    def _salida_no_operador(x):
        """T-36: la anotación con la que el candidato salió del juego (desde VALIDADA, COMPARADA, PROPUESTA o AUTORIZADA) tras su
        última validación, si no la decidió el operador y él no la ha ratificado después. Lo que pase luego (reabrir, observar
        otra vez, descartar) no la borra. Una caducidad del Orquestador no es una salida decidida por nadie."""
        h = x["historial"]
        iv = max((i for i, a in enumerate(h) if a["hasta"] == "VALIDADA" and a["desde"] != "VALIDADA"), default=None)
        if iv is None:
            return None
        salida = None
        for a in h[iv + 1:]:
            if salida is None:
                if a["desde"] in VIVOS and a["hasta"] not in VIVOS + ("EJECUTADA",):
                    if a["actor"] == "OPERADOR" or (a["actor"] == "ORQUESTADOR" and a["hasta"] == "CADUCADA"):
                        return None
                    salida = a
            elif a["actor"] == "OPERADOR" and (a["hasta"] in ("EN_OBSERVACION", "DESCARTADA") or a["ref"] == "RATIFICA_APARTADO"):
                return None   # el operador lo hizo suyo
        return salida

    def _sellos_validos(self, x):
        refs = [r for r in x["sobre"]["documento"].get("data_refs", []) if isinstance(r, str) and r.startswith("K-")]
        return bool(refs) and all(self.sellos.get(r, {}).get("estado") not in (None, "ANULADO") for r in refs)

    def _testigos(self, cartera, a, excluir):
        """Candidatos de la cartera sacados del juego por alguien distinto del operador (observar, descartar, reabrir…) cuyo sobre
        validado sigue vigente. Se deducen del historial encadenado; la integridad de todos se comprueba antes (comparar, proponer)."""
        out = []
        for k, x in sorted(self.expedientes.items()):
            if k in excluir or x["cartera_destino"] != cartera or x["estado"] in VIVOS + ("EJECUTADA",) or not x.get("sobre"):
                continue
            if self._salida_no_operador(x) and a <= _dt(x["sobre"]["valid_until"]) and self._sellos_validos(x):
                out.append(x)
        return out

    def _testigos_nuevos(self, e, a):
        """Testigos que no estaban cuando se comparó: la comparación ya no vale (proponer y autorizar)."""
        c = e.get("comparacion") or {}
        return sorted(x["expediente_id"] for x in self._testigos(e["cartera_destino"], a, {e["expediente_id"]})
                      if x["expediente_id"] not in c.get("testigos", [])
                      and (x.get("comparacion") or {}).get("id") != c.get("id"))   # ya se comparó con él en esa misma comparación

    def _comprobar_testigos(self, e, a):
        rota = self._rota()
        if rota:
            self._activar_kill(f"integridad rota en {rota}", "ORQUESTADOR", self.ultimo_ahora or "1970-01-01T00:00:00+00:00")
            return _no("O-13", f"el expediente {rota} no es íntegro")
        nuevos = self._testigos_nuevos(e, a)
        if nuevos:
            return _no("O-22", f"después de comparar se apartó a {', '.join(nuevos[:5])}: compare de nuevo")
        return None

    @_seguro
    def ratificar_apartado(self, expediente_id, motivo, actor, ahora):
        """El operador hace suyo el apartado de un candidato (p. ej. el que F vetó y su gestor descartó): deja de ser testigo."""
        self._ahora(ahora)
        e, err = self._exp(expediente_id)
        if err:
            return err
        if actor != "OPERADOR":
            return _no("O-05", "solo el operador ratifica un apartado")
        if not (isinstance(motivo, str) and motivo.strip()):
            return _no("O-15", "ratificar un apartado exige motivo")
        if e["estado"] in VIVOS + ("EJECUTADA",) or not self._salida_no_operador(e):
            return _no("O-04", "no hay ningún apartado pendiente de ratificar en este expediente")
        self._anota(e, e["estado"], e["estado"], "OPERADOR", ahora, f"apartado ratificado: {motivo.strip()[:160]}", "RATIFICA_APARTADO")
        return _r(True, "OK", "apartado ratificado")

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
        # T-36: ¿habría ganado alguno de los apartados? Se compara también con ellos; si es así, D no da ganador y elige el operador
        rota = self._rota()   # T-36: cualquier expediente alterado (también uno sacado de la cartera) detiene la comparación
        if rota:
            self._activar_kill(f"integridad rota en {rota}", "ORQUESTADOR", self.ultimo_ahora or "1970-01-01T00:00:00+00:00")
            return _no("O-13", f"el expediente {rota} no es íntegro: no se compara")
        testigos = self._testigos(cartera, a, set(expediente_ids))
        apartado_mejor = None
        if testigos and d["decision_global"] == "INVERTIR":
            t = comparar_candidatos([{"expediente_id": x["expediente_id"], "sobre": copy.deepcopy(x["sobre"]["documento"])} for x in exps + testigos],
                                    ahora, ref)
            tids = {x["expediente_id"] for x in testigos}
            if not t["ok"]:
                return _no("O-01", f"D no pudo comparar con los candidatos apartados: {t['motivo']}")
            mejores = [t["ganador_global"]] if t["ganador_global"] else t["aspirantes"]
            apartado_mejor = next((x for x in mejores if x in tids), None)
        elif testigos and d["decision_global"] == "ABSTENERSE":
            t = comparar_candidatos([{"expediente_id": x["expediente_id"], "sobre": copy.deepcopy(x["sobre"]["documento"])} for x in testigos], ahora, ref)
            if t["ok"] and t["decision_global"] == "INVERTIR":   # D se abstiene, pero un apartado sí superaba la referencia
                apartado_mejor = t["ganador_global"] or t["aspirantes"][0]
        cid = "CMP-" + _hash([sorted(expediente_ids), ahora, len(self.ultima_comparacion)])[:12]
        filas = {r["expediente_id"]: r for g in d["grupos"].values() for r in g["ranking"]}
        excl = {x["expediente_id"]: x["motivo"] for x in d.get("excluidos", [])}
        en_juego = set([d["ganador_global"]] if d["ganador_global"] else d["aspirantes"])   # lo que D habría dejado elegir
        for e in exps:
            eid = e["expediente_id"]
            grupo = next((g for g in d.get("grupos", {}).values() if any(r["expediente_id"] == eid for r in g["ranking"])), None)
            fila = filas.get(eid)
            e["comparacion"] = {"id": cid, "codigo_d": d["codigo"], "decision_global": d["decision_global"], "referencia": d["referencia"],
                                "decision": grupo["decision"] if grupo else None, "sensible": grupo["sensible"] if grupo else None,
                                "ganador": d["ganador_global"] == eid and apartado_mejor is None,
                                "aspirante": eid in en_juego and (d["ganador_global"] is None or apartado_mejor is not None),
                                "excluido": excl.get(eid), "elegido_por_operador": None,
                                "testigos": [x["expediente_id"] for x in testigos], "apartado_mejor": apartado_mejor,
                                "detalle_d": {k: fila[k] for k in ("puntuacion", "exceso_sobre_referencia_pct", "horizonte_dias", "peor_escenario_pct",
                                                                   "confianza_normalizada", "factor_evidencia", "dominado_por")} if fila else None}
            self._anota(e, e["estado"], "COMPARADA", actor, ahora, "comparada con " + ",".join(expediente_ids), cid, datos=_hash(e["comparacion"]))
        ganador = next((x["expediente_id"] for x in exps if x["comparacion"]["ganador"]), None)
        self.ultima_comparacion[cartera] = cid
        if apartado_mejor:
            quien = self.expedientes[apartado_mejor]["historial"][-1]["actor"]
            self._aviso("O-30", f"{cartera}: el candidato {apartado_mejor}, apartado por {quien}, habría ganado la comparación; decide el operador",
                        ahora, apartado_mejor)
            return _r(True, "O-30", "un candidato apartado habría ganado: D no da ganador y elige el operador",
                      ganador=None, apartado_mejor=apartado_mejor, codigo_d=d["codigo"], decision_global=d["decision_global"])
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
            return _no("O-22", "solo se elige entre los aspirantes de una decisión ajustada (empatados, primeros con otra ponderación o cuando un apartado habría ganado)")
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
        if _via(ce.get("via_acceso")) is None:
            return _no("O-01", "condiciones_entrada: falta via_acceso (por qué vía se opera: contado, futuro, ETF...)")
        try:
            fr = date.fromisoformat(cs["fecha"]) if isinstance(cs, dict) and isinstance(cs.get("fecha"), str) and _FECHA.match(cs["fecha"]) else None
        except ValueError:
            fr = None
        if fr is None:
            return _no("O-01", "condiciones_salida: falta la fecha de revisión (AAAA-MM-DD)")
        if fr <= a.astimezone(timezone.utc).date():
            return _no("O-10", "la fecha de revisión ya ha llegado: la tesis se revisa antes de proponer")
        if self.divisa(ce["instrumento"]) is None:
            return _no("O-01", "no se conoce la divisa de cotización del instrumento: configúrela en divisas_cotizacion")
        par = par_divisas(ce["instrumento"]) if ce["instrumento"] not in self.cfg["divisas_cotizacion"] else None
        if par and ce["activo_base"] != par[0]:
            return _no("O-01", "en un par de divisas el activo base es la primera divisa")
        if ce.get("resto_parcial", "CANCELAR") != "CANCELAR":
            return _no("O-01", "condiciones_entrada.resto_parcial: solo se admite CANCELAR (mantener vivo el resto exige redimensionar el stop, T-12)")
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
        for c_ in conds:   # T-12: un OBJETIVO puede declarar la fracción de la posición inicial que se reduce al cumplirse
            if "fraccion" in c_ and not (c_["tipo"] == "OBJETIVO" and _num(c_["fraccion"]) and 0 < c_["fraccion"] < 1):
                return _no("O-01", "condiciones_salida: solo un OBJETIVO declara fracción, y debe estar entre 0 y 1 (sin incluirlos)")
        if sum(c_.get("fraccion", 0) for c_ in conds) >= 1:
            return _no("O-01", "condiciones_salida: las fracciones declaradas suman la posición entera; para eso está un OBJETIVO sin fracción")
        stops = [c for c in conds if c.get("tipo") == "STOP"]
        if len(stops) != 1 or stops[0]["metrica"] != "precio":
            return _no("O-01", "condiciones_salida: debe haber exactamente un STOP y su métrica debe ser el precio")
        c = e.get("comparacion") or {}
        if not (c.get("ganador") or c.get("elegido_por_operador")):
            return _no("O-22", "solo se propone el ganador de D o el candidato que eligió el operador")
        err = self._comprobar_testigos(e, a)
        if err:
            return err
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
        if _via(ce["via_acceso"]) != _via(ident["via_acceso"]):
            return _no("O-21", "la vía de acceso no es la analizada en el sobre (un futuro analizado no se opera como contado)")
        if date.fromisoformat(cs["fecha"]) > date.fromisoformat(es["fecha_revision"]):
            return _no("O-21", "la fecha de revisión pasa de la del sobre")
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
        err = self._foto_de_g(dim["cartera"], ce["instrumento"], ce["limite"])
        if err:
            return None, err
        esperado = {"instrumento": ce["instrumento"], "activo_base": ce["activo_base"], "divisa_cotizacion": self.divisa(ce["instrumento"]),
                    "direccion": "LARGO" if stop["operador"] in ("<", "<=") else "CORTO",
                    "precio_entrada": ce["limite"], "stop_precio": stop["umbral"], "apalancamiento": ce["apalancamiento"], "cartera": e["cartera_destino"]}
        if sol != esperado:
            return None, _no("O-23", "la solicitud de E no es la propuesta (instrumento, dirección, límite, stop, apalancamiento o cartera)")
        r = dimensionar(copy.deepcopy(sol), copy.deepcopy(dim["cartera"]), self.cfg["politica_f"], dim["ahora"], dim["riesgo_objetivo_pct"], dim["paso"])
        if not r["ok"]:
            return None, _no("O-23", f"E no da una cantidad viable ({r['codigo']}): {r['motivo'][:80]}")
        if ce["cantidad"] > r["cantidad"] * (1 + 1e-12):
            return None, _no("O-23", f"la cantidad propuesta supera la que calcula E ({r['cantidad']})")
        return r["cantidad"], None

    def _comprobar_autorizacion(self, e, expediente_id, actor, control_f, a, ahora):
        err = self._transicion_ok(e, "AUTORIZADA", actor)
        if err:
            return err
        if self.kill is not None:
            return _no("O-26", "kill-switch activo: no se autoriza nada nuevo")
        if actor == "MATRIZ_AUTONOMIA" and not self.cfg["matriz_autonomia"].get(e["cartera_destino"], False):
            return _no("O-05", "la matriz de autonomía no autoriza esta cartera sin el operador")
        if actor == "MATRIZ_AUTONOMIA" and NIVELES[self.nivel(e["cartera_destino"])] < 2:
            return _no("O-05", f"la cartera está en {self.nivel(e['cartera_destino'])}: autoriza el operador")
        if actor == "MATRIZ_AUTONOMIA" and not self._sello_vigente_para(e, a):   # T-29: sin datos vigentes no hay decisión automática
            self._degradar(e["cartera_destino"], "la matriz iba a autorizar con un sello que ya no está vigente", ahora)
            return _no("O-10", "el sello del análisis ya no está vigente para la cartera: autoriza el operador")
        if not isinstance(control_f, dict) or not isinstance(control_f.get("event_id"), str):
            return _no("O-01", "falta el informe de control de F (CT-G-08)")
        err = self._comprobar_testigos(e, a)   # T-36: nadie apartó a un rival después de comparar
        if err:
            return err
        if a > _dt(e["propuesta"]["entrada"]["ventana_hasta"]) or a > _dt(e["sobre"]["valid_until"]):
            return _no("O-10", "la propuesta caducó")
        if date.fromisoformat(e["propuesta"]["salida"]["fecha"]) <= a.astimezone(timezone.utc).date():
            return _no("O-10", "llegó la fecha de revisión de la tesis: se revisa antes de autorizar")
        if self._sello_anulado(e):
            return _no("O-06", "el sello del análisis ya no es válido")
        fallos = validar_informe_f(control_f, {"ahora": ahora, "expediente_id": expediente_id, "correlation_id": e["correlation_id"],
                                               "divisa_cotizacion": self.divisa(e["propuesta"]["entrada"]["instrumento"]),
                                               "propuesta": e["propuesta"], "cartera_destino": e["cartera_destino"], "politica": self.cfg["politica_f"],
                                               "compromisos": self._compromisos(expediente_id, e["cartera_destino"])})
        if fallos:
            return _no("O-01", f"informe de F no válido: {fallos[0]['regla']}: {fallos[0]['mensaje'][:80]}", reglas=sorted({x['regla'] for x in fallos}))
        err = self._foto_de_g(control_f["entradas"]["cartera"], e["propuesta"]["entrada"]["instrumento"], e["propuesta"]["entrada"]["limite"])
        if err:
            return err
        cap_e = (e["propuesta"].get("dimensionado") or {}).get("cartera", {}).get("capital_eur")
        if cap_e != control_f["entradas"]["cartera"].get("capital_eur"):
            return _no("O-23", "F controló con un capital distinto del que usó E para dimensionar")
        return None

    @_seguro
    def pantalla_aprobacion(self, expediente_id, control_f, ahora, actor="OPERADOR"):
        """Pantalla de la cola de aprobaciones (§6): solo cifras calculadas por F, sin texto de un LLM. El operador la aprueba
        citando su hash y tecleando el importe. Vale una sola vez y caduca; con pérdida del día o fuera de horario, hay enfriamiento."""
        a = self._ahora(ahora)
        if actor != "OPERADOR":
            return _no("O-05", "solo el operador pide la pantalla de aprobación")
        e, err = self._exp(expediente_id)
        if err:
            return err
        err = self._comprobar_autorizacion(e, expediente_id, "OPERADOR", control_f, a, ahora)
        if err:
            return err
        if control_f["event_id"] in self.eventos:
            self._duplicado(control_f["event_id"], _hash(control_f), expediente_id, ahora)
            return _no("O-03", "el informe de F ya se usó")
        if control_f["resultado"] == "VETADO":   # el veto queda registrado: ese informe no se puede volver a usar
            self.eventos[control_f["event_id"]] = {"hash": _hash(control_f), "expediente_id": expediente_id}
            return _no("O-06", "F vetó la propuesta: no hay nada que aprobar")
        en = e["propuesta"]["entrada"]
        st = [c for c in e["propuesta"]["salida"]["condiciones"] if c["tipo"] == "STOP"][0]
        q = control_f["cantidad_aprobada"]
        fx = tipo_cambio(control_f["entradas"]["solicitud"]["divisa_cotizacion"], control_f["entradas"]["cartera"])
        cfg = self.cfg["aprobacion"]
        perdida = control_f["entradas"]["cartera"].get("perdida_dia_eur", 0.0)
        fuera = not _en_horario(a, cfg["horario_utc"])
        motivos_espera = (["pérdida en el día"] if perdida > cfg["enfriamiento_tras_perdida_dia_eur"] else []) + (["fuera de horario"] if fuera else [])
        espera = timedelta(minutes=cfg["enfriamiento_min"]) if motivos_espera else timedelta(0)
        p = {"expediente_id": expediente_id, "informe_f": control_f["event_id"], "informe_f_hash": _hash(control_f), "resultado_f": control_f["resultado"],
             "instrumento": en["instrumento"], "via_acceso": en["via_acceso"], "direccion": "LARGO" if st["operador"] in ("<", "<=") else "CORTO",
             "fecha_revision": e["propuesta"]["salida"]["fecha"], "cantidad": q, "precio_limite": en["limite"], "stop": st["umbral"],
             "importe": round(q * en["limite"] * fx, 2), "riesgo": round(q * abs(en["limite"] - st["umbral"]) * fx, 2), "unidad_importe": "EUR",
             "divisa_cotizacion": control_f["entradas"]["solicitud"]["divisa_cotizacion"], "tipo_cambio_eur": fx,
             "apalancamiento": en["apalancamiento"], "cartera": e["cartera_destino"], "valid_until_f": control_f["valid_until"],
             "generada_en": ahora, "caduca_en": (a + espera + timedelta(minutes=cfg["caduca_min"])).isoformat(),
             "enfriamiento_hasta": (a + espera).isoformat(), "motivos_enfriamiento": motivos_espera}
        p["hash"] = _hash(p)
        self.pantallas[expediente_id] = {**p, "usada": False}
        return _r(True, "OK", "pantalla de aprobación lista", pantalla=copy.deepcopy(p))

    def _comprobar_aprobacion(self, expediente_id, control_f, aprobacion, a):
        p = self.pantallas.get(expediente_id)
        if not (isinstance(aprobacion, dict) and set(aprobacion) == {"pantalla_hash", "importe_tecleado", "canal", "segundo_factor"}):
            return _no("O-27", "la autorización del operador exige su aprobación: pantalla_hash, importe_tecleado, canal y segundo_factor")
        if p is None or _hash({k: v for k, v in p.items() if k not in ("hash", "usada")}) != p["hash"] or aprobacion["pantalla_hash"] != p["hash"]:
            return _no("O-27", "la aprobación no corresponde a la pantalla con las cifras de F")
        if p["usada"]:
            return _no("O-03", "esa aprobación ya se usó")
        if p["informe_f"] != control_f["event_id"] or p["informe_f_hash"] != _hash(control_f):
            return _no("O-27", "la pantalla aprobada es de otro informe de F (o de otro contenido con el mismo identificador)")
        if a > _dt(p["caduca_en"]):
            return _no("O-10", "la aprobación caducó: no se actúa")
        if a < _dt(p["enfriamiento_hasta"]):
            return _no("O-28", f"enfriamiento hasta {p['enfriamiento_hasta']} ({', '.join(p['motivos_enfriamiento'])})")
        cfg = self.cfg["aprobacion"]
        if not _en_horario(a, cfg["horario_utc"]) and (a - _dt(p["generada_en"])).total_seconds() < cfg["enfriamiento_min"] * 60:
            return _no("O-28", "la aprobación cae fuera de horario: espere el enfriamiento desde que se generó la pantalla")
        imp = aprobacion["importe_tecleado"]
        if not (_num(imp) and abs(imp - p["importe"]) < 0.005):
            return _no("O-27", "el importe tecleado no coincide con el de la pantalla")
        if aprobacion["canal"] not in self.cfg["aprobacion"]["canales"] or aprobacion["segundo_factor"] is not True:
            return _no("O-05", "una acción que aumenta riesgo exige un canal de aprobación admitido (no el chat) y segundo factor")
        return None

    @_seguro
    def autorizar(self, expediente_id, actor, control_f, ahora, aprobacion=None):
        a = self._ahora(ahora)
        e, err = self._exp(expediente_id)
        if err:
            return err
        err = self._comprobar_autorizacion(e, expediente_id, actor, control_f, a, ahora)
        if err:
            return err
        ih = _hash(control_f)
        dup = self._duplicado(control_f["event_id"], ih, expediente_id, ahora)
        if dup:
            return _no("O-03", "el informe de F ya se usó")
        if actor == "OPERADOR" and control_f["resultado"] != "VETADO":
            err = self._comprobar_aprobacion(expediente_id, control_f, aprobacion, a)
            if err:
                return err
            self.pantallas[expediente_id]["usada"] = True
        self.eventos[control_f["event_id"]] = {"hash": ih, "expediente_id": expediente_id}
        if control_f["resultado"] == "VETADO":
            return _no("O-06", "F vetó la propuesta")
        e["control_f"] = {"resultado": control_f["resultado"], "cantidad_aprobada": control_f["cantidad_aprobada"], "event_id": control_f["event_id"],
                          "emitido_en": control_f["emitido_en"], "valid_until": control_f["valid_until"], "entradas": copy.deepcopy(control_f["entradas"]),
                          "aprobacion": ({k: v for k, v in self.pantallas[expediente_id].items() if k != "usada"} if actor == "OPERADOR" else None)}
        self._anota(e, e["estado"], "AUTORIZADA", actor, ahora, f"control F: {control_f['resultado']} ({control_f['cantidad_aprobada']})", control_f["event_id"],
                    datos=_hash(e["control_f"]))
        return _r(True, "OK", "autorizada")

    TRANS_ORDEN = {None: {"ENVIADA"}, "ENVIADA": {"PARCIAL", "EJECUTADA", "RECHAZADA", "CANCELADA"},
                   "PARCIAL": {"DESHECHA"}, "EJECUTADA": {"DESHECHA"}}

    @_seguro
    def orden_entrada(self, expediente_id, orden_id, estado, cantidad_ejecutada, actor, ahora):
        """G anota el estado de la orden de entrada (Constitución §4.2): ENVIADA, y luego PARCIAL, EJECUTADA, RECHAZADA o
        CANCELADA. CONCILIADA la pone el Orquestador al aceptar la ejecución. Una orden enviada no cuenta como ejecutada."""
        self._ahora(ahora)
        e, err = self._exp(expediente_id)
        if err:
            return err
        if actor != "G":
            return _no("O-05", "solo G anota el estado de las órdenes")
        if e["estado"] != "AUTORIZADA":
            return _no("O-04", "solo un expediente AUTORIZADA tiene orden de entrada")
        if not (isinstance(orden_id, str) and _ID.match(orden_id) and _num(cantidad_ejecutada) and cantidad_ejecutada >= 0):
            return _no("O-01", "orden_id y cantidad_ejecutada (>= 0) obligatorios")
        oe = e.get("orden_entrada")
        actual = oe["estado"] if oe else None
        anteriores = (oe or {}).get("anteriores", [])
        if oe and oe["orden_id"] != orden_id:
            # intento nuevo: tras uno que no ejecutó nada, o tras uno que G cerró y comprobó (DESHECHA)
            if estado == "ENVIADA" and actual in ("RECHAZADA", "CANCELADA", "DESHECHA"):
                anteriores = anteriores + [{k: oe[k] for k in ("orden_id", "estado", "cantidad_ejecutada")}]
                oe, actual = None, None
            else:
                return _no("O-03", "ya hay otra orden de entrada para este expediente")
        if actual == estado and oe and oe["cantidad_ejecutada"] == cantidad_ejecutada:
            return _r(True, "O-02", "estado ya anotado", duplicado=True)
        if estado not in self.TRANS_ORDEN.get(actual, set()):
            return _no("O-04", f"transición de orden no permitida: {actual} -> {estado}")
        if estado == "DESHECHA" and cantidad_ejecutada != oe["cantidad_ejecutada"]:
            return _no("O-01", "DESHECHA debe llevar la cantidad que se ejecutó y se cerró")
        if (estado in ("ENVIADA", "RECHAZADA", "CANCELADA") and cantidad_ejecutada != 0) or (estado in ("PARCIAL", "EJECUTADA") and cantidad_ejecutada <= 0) \
                or cantidad_ejecutada > e["control_f"]["cantidad_aprobada"] * (1 + 1e-12):
            return _no("O-01", "cantidad ejecutada incoherente con el estado o mayor que la aprobada por F")
        if estado == "ENVIADA" and (orden_id in self.ordenes_usadas or any(x["orden_id"] == orden_id for x in anteriores)):
            return _no("O-03", "orden ya usada")
        if estado == "DESHECHA":
            self.ordenes_usadas.append(orden_id)
        hist = (oe or {}).get("historial", [])
        if estado == "ENVIADA" and self.kill is not None:
            return _no("O-26", "kill-switch activo: no se envían órdenes de entrada")
        aut = next((x["ahora"] for x in reversed(e["historial"]) if x["hasta"] == "AUTORIZADA" and x["desde"] != "AUTORIZADA"), None)
        if estado == "ENVIADA" and aut and any(_dt(r["kill"]["ahora"]) >= _dt(aut) for r in self.rearmes):
            return _no("O-26", "la autorización es anterior a un kill-switch: hay que volver a aprobar")
        if estado == "ENVIADA" and not self.autorizacion_vigente(e):
            return _no("O-05", f"la autorización fue automática y la cartera está ahora en {self.nivel(e['cartera_destino'])}: la confirma el operador")
        e["orden_entrada"] = {"orden_id": orden_id, "estado": estado, "cantidad_ejecutada": cantidad_ejecutada, "anteriores": anteriores,
                              "historial": hist + [{"estado": estado, "ahora": ahora, "cantidad_ejecutada": cantidad_ejecutada}]}
        self._anota(e, "AUTORIZADA", "AUTORIZADA", actor, ahora, f"orden de entrada {estado}", orden_id, datos=_hash(e["orden_entrada"]))
        return _r(True, "OK", f"orden {estado}")

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
        t = a   # la vigencia se mide en el instante en que el intermediario ejecutó, si G lo aporta
        if orden.get("ejecutada_en") is not None:
            if not (isinstance(orden["ejecutada_en"], str) and _FH.match(orden["ejecutada_en"])):
                return _no("O-01", "ejecutada_en con formato inválido")
            t = _dt(orden["ejecutada_en"])
            if t > a:
                return _no("O-01", "ejecutada_en posterior al instante actual")
        if t > _dt(e["propuesta"]["entrada"]["ventana_hasta"]) or t > _dt(e["sobre"]["valid_until"]):
            return _no("O-10", "la ventana de entrada o el sobre vencieron antes de ejecutar")
        if date.fromisoformat(e["propuesta"]["salida"]["fecha"]) <= t.astimezone(timezone.utc).date():
            return _no("O-10", "llegó la fecha de revisión de la tesis antes de ejecutar: se revisa antes de abrir")
        quien = self.autorizada_por(e)
        if not manual and quien == "MATRIZ_AUTONOMIA" and NIVELES[self.nivel(e["cartera_destino"])] < 2:
            return _no("O-05", f"la autorización fue automática y la cartera está ahora en {self.nivel(e['cartera_destino'])}: la confirma el operador")
        if not manual and quien == "MATRIZ_AUTONOMIA" and not self._sello_vigente_para(e, t):
            self._degradar(e["cartera_destino"], "una autorización automática iba a ejecutarse con un sello que ya no está vigente", ahora)
            return _no("O-10", "la autorización fue automática y el sello del análisis ya no está vigente: la confirma el operador")
        if self._sello_anulado(e):
            return _no("O-06", "el sello del análisis ya no es válido")
        cf = e["control_f"]
        if t > _dt(cf["valid_until"]):
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
        oe = e.get("orden_entrada")
        if not manual:
            if not (oe and oe["orden_id"] == orden["orden_id"] and oe["estado"] in ("PARCIAL", "EJECUTADA")
                    and abs(oe["cantidad_ejecutada"] - orden["cantidad"]) <= 1e-9):
                return _no("O-06", "la ejecución no corresponde a la orden de entrada anotada (estado y cantidad)")
            ultimo_envio = next((h["ahora"] for h in reversed(oe["historial"]) if h["estado"] == "ENVIADA"), None)
            if ultimo_envio and t < _dt(ultimo_envio):
                return _no("O-01", "ejecutada_en anterior al envío de la orden")
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
                                "origen": "MANUAL" if manual else "G", "ejecutada_en": orden.get("ejecutada_en") or ahora,
                                "cantidad_inicial": orden["cantidad"], "protecciones_anteriores": [], "reduccion": None, "reducciones": [],
                                "condiciones_consumidas": [], "via_acceso": e["propuesta"]["entrada"]["via_acceso"],
                                "fecha_revision": e["propuesta"]["salida"]["fecha"]}
        self.ordenes_usadas += [orden["orden_id"], *prot]
        self._anota_pos(self.posiciones[pid], None, "ABIERTA", actor if manual else "G", ahora,
                    "ejecución manual declarada (CT-G-14)" if manual else "orden conciliada", orden["orden_id"])
        e["posicion_id"] = pid
        if oe and not manual:
            oe["estado"] = "CONCILIADA"
            oe["historial"].append({"estado": "CONCILIADA", "ahora": ahora, "cantidad_ejecutada": orden["cantidad"]})
        self._anota(e, e["estado"], "EJECUTADA", actor, ahora, "ejecutada", orden["orden_id"], datos=_hash(oe) if oe else None)
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
        if (e is not None and not self._todo_ok(e)) or (p is not None and not self._posicion_ok(p)):
            self._activar_kill(f"integridad rota en {ref}", "ORQUESTADOR", self.ultimo_ahora or "1970-01-01T00:00:00+00:00")
            return _no("O-13", "el expediente o la posición vinculados no son íntegros (historial, sobre, propuesta, orden, aprobación o estado)")
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
        if v["tipo"] == "EXPEDIENTE" and self._entrada_viva(e):
            return _no("O-25", "hay una orden de entrada de G viva para este expediente: cancélela antes de ejecutar a mano")
        if v["tipo"] == "EXPEDIENTE":
            orden = {"orden_id": registro["ref_intermediario"], "cantidad": registro["cantidad"], "precio": registro["precio"], "conciliada": True,
                     "proteccion_orden_ids": [registro["proteccion_ref"]]}
            r = self._ejecutar(e, orden, "OPERADOR", ahora, a, manual=True)
            if not r["ok"]:
                return r
        elif v["tipo"] == "POSICION":
            if p.get("reduccion"):   # una reducción a medias termina con el cierre total
                p["reducciones"].append({**p["reduccion"], "restante": 0, "interrumpida": "cierre manual"})
                p["reduccion"] = None
            self._anota_pos(p, p["estado"], "CERRANDO", "OPERADOR", ahora, f"cierre manual declarado (CT-G-14): {registro['motivo'][:120]}")
            p["cantidad"] = 0
            self.ordenes_usadas.append(registro["ref_intermediario"])
            self._anota_pos(p, "CERRANDO", "CERRADA", "OPERADOR", ahora, "cierre manual declarado (CT-G-14)", registro["ref_intermediario"])
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
        if actor in GESTORES and actor != GESTOR_DE[e["cartera_destino"]]:
            return _no("O-05", "un gestor solo aparta expedientes de su cartera")
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
        if actor in GESTORES and actor != GESTOR_DE[e["cartera_destino"]]:
            return _no("O-05", "un gestor solo aparta expedientes de su cartera")
        if not (isinstance(motivo, str) and motivo.strip()):
            return _no("O-15", "el descarte exige motivo")
        if self._entrada_viva(e):
            return _no("O-25", "hay una orden de entrada viva en el intermediario: G debe cancelarla antes de descartar")
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
                if (a > min(limites) or self._sello_anulado(e)) and self._entrada_viva(e):
                    self._aviso("O-25", f"expediente {eid}: venció con la orden de entrada aún viva; G debe cancelarla", ahora, eid)
                    cambios.append(("aviso_entrada_viva", eid, "AUTORIZADA"))
                elif a > min(limites) or self._sello_anulado(e):
                    self._anota(e, e["estado"], "CADUCADA", "ORQUESTADOR", ahora, "venció valid_until o la ventana de entrada")
                    self._aviso("O-10", f"expediente {eid} caducó sin decidirse", ahora, eid)
                    cambios.append(("expediente", eid, "CADUCADA"))
        cfg_av = self.cfg["avisos"]
        for av in self.avisos:   # CT-G-16: un aviso de prioridad alta sin acuse se reitera y, tras varias veces, escala
            if av["prioridad"] == "ALTA" and av["acuse"] is None:
                debidas = int((a - _dt(av["ahora"])).total_seconds() // (cfg_av["reiterar_min"] * 60))   # las que tocaban, aunque el barrido llegue tarde
                if debidas > len(av["reiteraciones"]):
                    av["reiteraciones"].append(ahora)
                    av["reiteraciones_debidas"] = debidas
                    cambios.append(("aviso_reiterado", av["id"], debidas))
                if max(debidas, len(av["reiteraciones"])) >= cfg_av["escalar_tras"] and not av["escalado"]:
                    av["escalado"], av["canal"] = True, cfg_av["canal_escalado"]
                    cambios.append(("aviso_escalado", av["id"], cfg_av["canal_escalado"]))
        for sid, s in self.sellos.items():
            if s["estado"] == "VIGENTE" and estado_sello(s, str(a.astimezone(timezone.utc).date()), s["cartera"], self.cal_def) == "CADUCADO":
                s["estado"] = "CADUCADO"
                self._aviso("O-10", f"el sello {sid} caducó por antigüedad", ahora, sid)
                cambios.append(("sello", sid, "CADUCADO"))
        for c, sid, eid in self._datos_viejos(a):   # T-29: candidatos en juego sobre datos que ya no valen para su cartera
            if c not in self.degradadas and NIVELES[self.nivel(c)] > 1:
                self._degradar(c, f"el sello {sid} de {eid} ya no está vigente para {c}", ahora)
                cambios.append(("degradada", c, sid))
        return _r(True, "OK", f"{len(cambios)} cambio(s)", cambios=cambios)

    def _sello_vigente_para(self, e, a):
        """El sello del análisis del expediente sigue VIGENTE para su cartera hoy (K: antigüedad por cartera)."""
        en = self.encargos.get(e["encargo_actual"])
        s = self.sellos.get(en["sello_ref"]) if en else None
        if s is None or s["estado"] == "ANULADO":
            return False
        s = {**s, "estado": "VIGENTE"}   # CADUCADO lo marcó barrer para la cartera del sello; aquí manda la antigüedad para esta cartera
        return estado_sello(s, str(a.astimezone(timezone.utc).date()), e["cartera_destino"], self.cal_def) == "VIGENTE"

    def _datos_viejos(self, a):
        """(cartera, sello, expediente) de los candidatos en juego cuyo sello ya no está vigente para su cartera."""
        out = []
        for eid, x in sorted(self.expedientes.items()):
            if x["estado"] in VIVOS and not self._sello_vigente_para(x, a):   # también con la orden de entrada viva
                en = self.encargos.get(x["encargo_actual"])
                out.append((x["cartera_destino"], en["sello_ref"] if en else None, eid))
        return out

    # ------------------------------------------------------------ posiciones
    def _pos(self, pid):
        p = self.posiciones.get(pid)
        if p is None:
            return None, _no("O-12", f"posición inexistente: {pid!r}")
        if not self._posicion_ok(p):
            return None, _no("O-13", "el historial de la posición o su estado de control (cantidad, stops, reducción) no es íntegro")
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
    def posicion_transicion(self, posicion_id, hasta, actor, ahora, condicion=None, restante=None, orden=None, motivo=None,
                            cantidad=None, protecciones=None, fecha_revision=None):
        """Transiciones de una posición. Reducir (T-12): el operador con cantidad y motivo; automático solo por una condición
        OBJETIVO que declare su fracción, una vez, y desde L2. Al terminar la reducción G aporta el stop redimensionado."""
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
        if cantidad is not None and hasta != "REDUCIENDO":
            return _no("O-01", "la cantidad solo se indica al pedir una reducción")
        if protecciones is not None and not (p["estado"] == "REDUCIENDO" and hasta in ("ABIERTA", "EN_REVISION")):
            return _no("O-01", "los stops solo se sustituyen al terminar una reducción")
        ref, decl = None, None
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
                parcial = c.get("fraccion") is not None
                if hasta == "CERRANDO" and parcial:
                    return _no("O-06", "esa condición declara una reducción parcial, no un cierre")
                if hasta == "REDUCIENDO" and not parcial:
                    return _no("O-06", "una reducción automática exige una condición que declare la fracción que se reduce")
                if c["id"] in p["condiciones_consumidas"]:
                    return _no("O-06", "esa condición ya redujo la posición una vez")
                ref, decl = c["id"], c
        if hasta == "REDUCIENDO":
            if decl is not None:
                q = decl["fraccion"] * p["cantidad_inicial"]
                if cantidad is not None and not (_num(cantidad) and abs(cantidad - q) <= 1e-9 * max(1.0, q)):
                    return _no("O-06", "la cantidad no es la que fija la fracción declarada")
            else:
                q = cantidad
            if not (_num(q) and q > TOL_Q):
                return _no("O-06", "la reducción exige una cantidad positiva y mayor que la tolerancia de cantidades")
            if q >= p["cantidad"] - TOL_Q:
                return _no("O-06", "la reducción dejaría la posición a cero o al revés: use el cierre (CERRANDO)")
        if fecha_revision is not None and not (hasta == "ABIERTA" and p["estado"] == "EN_REVISION"):
            return _no("O-01", "la fecha de revisión solo se renueva al confirmar la tesis (EN_REVISION -> ABIERTA)")
        nueva_fr = None
        if hasta == "ABIERTA" and p["estado"] == "EN_REVISION":
            if actor in GESTORES and actor != GESTOR_DE[p["cartera"]]:
                return _no("O-05", "un gestor solo confirma la tesis de las posiciones de su cartera")
            if not (isinstance(motivo, str) and motivo.strip()):
                return _no("O-15", "confirmar la tesis exige motivo")
            hoy = _dt(ahora).astimezone(timezone.utc).date()
            vencida = p.get("fecha_revision") is not None and date.fromisoformat(p["fecha_revision"]) <= hoy
            if fecha_revision is not None:
                try:
                    nueva_fr = date.fromisoformat(fecha_revision) if isinstance(fecha_revision, str) and _FECHA.match(fecha_revision) else None
                except ValueError:
                    nueva_fr = None
                if nueva_fr is None:
                    return _no("O-01", "fecha_revision con formato inválido (AAAA-MM-DD)")
                if nueva_fr <= hoy:
                    return _no("O-10", "la nueva fecha de revisión debe ser futura")
                if nueva_fr > hoy + timedelta(days=self.cfg["revision_max_dias"]):
                    return _no("O-06", f"la nueva fecha de revisión no puede estar a más de {self.cfg['revision_max_dias']} días")
            elif vencida:
                return _no("O-15", "la fecha de revisión ya llegó: confirmar la tesis exige fijar la siguiente")
        nuevas = None
        if p["estado"] == "REDUCIENDO" and hasta in ("ABIERTA", "EN_REVISION") and hasta != p["reduccion"]["vuelve_a"]:
            return _no("O-04", f"la reducción salió de {p['reduccion']['vuelve_a']} y vuelve a ese estado")
        if p["estado"] in ("REDUCIENDO", "CERRANDO") and hasta in ("ABIERTA", "EN_REVISION", "CERRADA"):
            ok = (isinstance(orden, dict) and orden.get("conciliada") is True and isinstance(orden.get("orden_id"), str)
                  and _num(restante) and 0 <= restante <= p["cantidad"])
            if not ok:
                return _no("O-06", "se exige orden conciliada y cantidad restante")
            if (hasta == "CERRADA") != (restante == 0):
                return _no("O-06", "CERRADA exige restante 0; ABIERTA, restante mayor que 0")
            if p["estado"] == "CERRANDO" and restante != 0:
                return _no("O-06", "CERRANDO solo termina en CERRADA")
            if hasta != "CERRADA":   # fin de una reducción: lo que queda y su stop
                if restante > p["reduccion"]["objetivo_restante"] + TOL_Q:
                    return _no("O-06", "la reducción no ha llegado a la cantidad pedida: sigue REDUCIENDO")
                if not (isinstance(protecciones, list) and protecciones and len(set(protecciones)) == len(protecciones)
                        and all(isinstance(x, str) and _ID.match(x) for x in protecciones)):
                    return _no("O-06", "al terminar una reducción G debe aportar el stop redimensionado a lo que queda")
                previas = set(p["protecciones"]) | set(p["protecciones_anteriores"])
                if any(x in p["protecciones_anteriores"] or (x not in previas and x in self.ordenes_usadas) or x == orden["orden_id"]
                       for x in protecciones):
                    return _no("O-03", "ese stop ya se usó o es una orden retirada")
                nuevas = list(protecciones)
            propia = hasta == "CERRADA" and orden["orden_id"] in p["protecciones"]   # el cierre puede ser el propio stop que saltó
            if orden["orden_id"] in self.ordenes_usadas and not propia:
                return _no("O-03", "orden ya usada")
            if not propia:
                self.ordenes_usadas.append(orden["orden_id"])
            p["cantidad"] = restante
            ref = orden["orden_id"]
        # --- a partir de aquí todo es válido: se aplica
        if nueva_fr is not None:
            p["fecha_revision"] = p["condiciones_salida"]["fecha"] = nueva_fr.isoformat()
        if hasta == "REDUCIENDO":
            p["reduccion"] = {"n": len(p["reducciones"]) + 1, "cantidad": q, "desde": p["cantidad"], "objetivo_restante": p["cantidad"] - q,
                              "condicion": decl["id"] if decl else None, "actor": actor, "motivo": motivo, "pedida_en": ahora,
                              "vuelve_a": p["estado"]}
        elif p["estado"] == "REDUCIENDO":
            fin = {**p["reduccion"], "restante": p["cantidad"] if hasta != "CERRANDO" else None, "orden_id": ref, "terminada_en": ahora}
            if hasta in ("CERRANDO", "CERRADA"):
                fin["interrumpida"] = "cierre"
            elif fin["condicion"]:
                p["condiciones_consumidas"].append(fin["condicion"])
            p["reducciones"].append(fin)
            p["reduccion"] = None
            if nuevas is not None:
                p["protecciones_anteriores"] += [x for x in p["protecciones"] if x not in nuevas]
                self.ordenes_usadas += [x for x in nuevas if x not in self.ordenes_usadas]
                p["protecciones"] = nuevas
        self._anota_pos(p, p["estado"], hasta, actor, ahora, motivo or "transición de posición", ref)
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
        if any(x["acuse"] is None and x["codigo"] in ("O-18", "O-19") and (x["ref"] in (posicion_id, p["cartera"]) or p["cartera"] in (x.get("carteras") or []))
               for x in self.avisos) or p["cartera"] in self.degradadas:
            return _no("O-06", "la cartera de la posición está degradada o tiene avisos sin acusar: resuélvalo antes de reclasificar")
        antes = p["cartera"]
        p["cartera"] = nueva_cartera
        self._anota_pos(p, p["estado"], p["estado"], actor, ahora, f"reclasificada {antes} -> {nueva_cartera}: {motivo}")
        return _r(True, "OK", "reclasificada")
