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
from validar_encargo import NIVEL_MIN_POR_DECISION, NIVEL_ORDEN, sobre_responde_a_encargo, validar_encargo  # noqa: E402
from validar_sobre import _dt, bloqueos  # noqa: E402
from manual_g import aplanar_manual, neto_libre, validar_manual, via_norm  # noqa: E402
from comparador import MARGEN_AJUSTADO, REFERENCIA_EFECTIVO, _referencia_ok, comparar_candidatos  # noqa: E402
from dimensionado import dimensionar  # noqa: E402
from validar_contradictor import diversidad, validar_informe  # noqa: E402
from parametros import PARAMETROS, VERSION_PARAMETROS, como_dict  # noqa: E402
from k_calidad import VERSION_REGLAS as VERSION_REGLAS_K  # noqa: E402
from k_calidad import eventos_entre, hash_del_sello  # noqa: E402
from control_f import VERSION_REGLAS as VERSION_REGLAS_F  # noqa: E402
import mandatos as sc1  # noqa: E402  T-51: SC-1, el mandato de cada cartera
import motor as sc3  # noqa: E402  T-26: SC-3, registro del Motor numérico
from control_f import POLITICA_DEFECTO, aplanar_informe, controlar, controles_de_contexto, divisa_cotizada, par_divisas, politica_valida, tipo_cambio, validar_informe_f  # noqa: E402

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
                  "version_config": "CFG-0.11.0",   # 0.11.0 (V0.53): integra 0.8.0 de GLM (T-33, libres_tope_dia_eur) con 0.10.0. 0.10.0 (T-18): promocion_nivel. 0.9.0 (T-18): L3 y umbral_l2_eur. 0.8.0 (T-33, GLM): libres_tope_dia_eur. 0.2.0 (T-48): Contradictor exigido en N2 y N3; autoria_c. 0.3.0 (T-49): alerta_perdida_pct. 0.4.0 (T-50): anulaciones_veto_mes. 0.5.0 (T-51): mandatos (SC-1) en lugar de instrumentos_permitidos. 0.6.0 (T-26/T-42): tolerancia_tipo_k_rel. 0.7.0 (T-22): politica_f con importes en euros y controles de la §8
                  "dia_coste_max_eur": 50.0, "revision_max_dias": 90, "observacion_max_dias": 30, "max_reaperturas": 2, "dia_tiempo_max_min": 600, "tolerancia_precio_entrada": 0.05,
                  "alerta_perdida_pct": -5.0,   # T-49: H pide revisar al perder esto (y cada múltiplo) [PROPUESTO]
                  "anulaciones_veto_mes": 2,
                  "tolerancia_tipo_k_rel": 0.03,   # T-42: desviación máxima entre el tipo de cambio de G y el último cierre de K [PROPUESTO, D-29]   # T-50 (§6.2): anulaciones de veto de F que el operador puede hacer en un mes natural (UTC) [PROPUESTO]
                  "exige_contradictor_en": ["N2", "N3"], "contradictor_desactivado_motivo": None, "autoria_c": {}, "autoria_contradictor": None,
                  "matriz_autonomia": {},   # T-48: Contradictor exigido por defecto donde se compara y propone [PROPUESTO]
                  "politica_f": POLITICA_DEFECTO,
                  "nivel_autonomia": {}, "tolerancia_conciliacion_rel": 0.0,   # cartera -> L0 | L1 | L2 (automático hasta umbral_l2_eur) | L3 (sin umbral, en horario); sin dato = L1
                  # T-18 (§6): lo que la matriz autoriza sola en L2 no pasa de este importe por orden, en euros; por encima, el operador
                  # (en L3, dentro del horario supervisado, sin umbral: solo el mandato y F) [PROPUESTO, P-01, D-33]
                  "umbral_l2_eur": {"TRADING": 5000.0, "TACTICA": 5000.0, "LARGO_PLAZO": 5000.0},
                  # T-18 (§6, V0.51): subir de nivel exige este periodo en el nivel actual sin incidentes [PROPUESTO, P-02, D-34]
                  "promocion_nivel": {"periodo_min_dias": 30},
                  "libres_tope_dia_eur": {c: 2000.0 for c in ("TRADING", "TACTICA", "LARGO_PLAZO")},   # T-33 (§6): tope diario por cartera de las operaciones LIBRES declaradas (CT-G-14) [PROPUESTO, D-32]
                  "mandatos": sc1.MANDATOS_DEFECTO,   # T-51: SC-1, fuente única del mandato de cada cartera [PROPUESTO, P-03, D-28]
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
                  "cuenta_intermediario": "SIM-1"}    # la cuenta de la que G toma las fotos (D-21)
NIVELES = {"L0": 0, "L1": 1, "L2": 2, "L3": 3}   # V0.50 (T-18): L3 autónomo, solo en horario supervisado (fuera, como L2)
# Prioridad de cada aviso para el operador [PROPUESTO]
TIPOS_KILL = {"POSICION_DESCONOCIDA", "CANTIDAD", "SENTIDO_O_ACTIVO", "PROTECCION", "PROTECCION_HUERFANA", "ENTRADA_HUERFANA",
              "MANUAL_NO_CUADRA", "POSICION_SIN_PROTEGER", "INTEGRIDAD"}   # lo que G sabe explicar (cierres propios, conexión, estado incierto, dato viejo) no
# T-50: vetos de F que el operador puede anular (con motivo y dentro del límite mensual) [PROPUESTO, D-27]. No se anulan los de
# forma o cálculo (F-01), lado del stop (F-02), apalancamiento (F-05), pérdida del día (F-08), cartera vieja (F-10) ni tipo de cambio (F-12),
# y la anulación nunca pasa de los topes de cantidad de F (F-03, F-04, F-06 y F-07)
VETOS_ANULABLES = ("F-09", "F-11")
TOPES_F = ("F-03", "F-04", "F-06", "F-07", "F-13", "F-14", "F-15")   # T-22: también los importes en euros acotan una anulación
LIMITE_PERDIDA = "perdida_dia_max_pct"   # T-50 (§6.3): el límite de pérdida de la política de F que el operador puede ajustar
MOTIVO_MIN = 15   # caracteres mínimos del motivo de una anulación de veto o de un cambio de límite


def _migracion_que_cambia(x):
    """V0.46: una entrada MIGRACION del registro de límites que cambió la huella de la configuración completa (otro código)."""
    return x["tipo"] == "MIGRACION" and x.get("huella_antes") != x.get("huella_config")


def _saturada(x):
    """V0.53 (revisión de la integración, h04): una suma de pérdidas que desborda se satura al mayor flotante finito. Sigue por
    encima de cualquier límite (el cortacircuito y F-16 actúan igual) y el estado sigue siendo guardable (PE-01 rechaza infinitos)."""
    return x if math.isfinite(x) else sys.float_info.max


def _motivo_ok(m):
    return isinstance(m, str) and len(m.strip()) >= MOTIVO_MIN and len(m) <= 500


def _mes(t):
    return t.astimezone(timezone.utc).strftime("%Y-%m")


def _dia(t):
    return t.astimezone(timezone.utc).date().isoformat()


# V0.51 (T-18): avisos que, en el periodo de promoción, impiden subir de nivel (además de O-19, ALCANZADO y el kill-switch)
INCIDENTES_PROMOCION = ("O-03", "O-18", "O-25", "O-37")   # V0.53: también el tope de LIBRES superado (T-33)
PRIORIDAD_AVISO = {"O-39": "ALTA", "O-36": "MEDIA", "O-35": "ALTA", "O-34": "ALTA", "O-33": "MEDIA", "O-32": "MEDIA", "O-31": "MEDIA", "O-20": "MEDIA", "O-30": "ALTA", "O-25": "ALTA", "O-26": "ALTA", "O-19": "ALTA", "O-18": "ALTA", "O-03": "ALTA", "O-08": "ALTA", "O-09": "ALTA", "O-13": "ALTA", "O-17": "ALTA", "O-37": "ALTA", "O-38": "ALTA"}   # O-37 (T-33): tope diario de las LIBRES superado, o LIBRES sin poder valorar; O-38 (T-40): cortacircuito global por pérdida
ACTORES_PROPUESTA = set(EMISORES)   # quien propone no aprueba ni controla: F, D y H no proponen (Constitución §2, P1)


_via = via_norm   # identidad de una vía de acceso (texto libre del sobre), la misma en CT-G-14 y en R-14


_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}\Z")


def _ins(x):
    """Identidad de un instrumento: «EUR/USD» y «EURUSD» son el mismo (T-51: la misma función que SC-1, con NFKC)."""
    return sc1.norm(x)


MAX_EDAD_DIMENSIONADO_MIN = PARAMETROS["e_max_edad_dimensionado_min"]   # [PROPUESTO] el cálculo de E no puede ser más viejo que esto al proponer


_HM = re.compile(r"^([01]\d|2[0-3]):[0-5]\d\Z")


def _aprob_ok(a):
    return (isinstance(a, dict) and set(a) == {"caduca_min", "canales", "enfriamiento_min", "enfriamiento_tras_perdida_dia_eur", "horario_utc"}
            and _num(a["caduca_min"]) and 0 < a["caduca_min"] <= 120 and isinstance(a["canales"], list) and a["canales"]
            and all(isinstance(x, str) and x and x.upper() != "CHAT" for x in a["canales"])
            and _num(a["enfriamiento_min"]) and a["enfriamiento_min"] >= 0 and _num(a["enfriamiento_tras_perdida_dia_eur"])
            and a["enfriamiento_tras_perdida_dia_eur"] >= 0 and isinstance(a["horario_utc"], list) and len(a["horario_utc"]) == 2
            and all(isinstance(x, str) and _HM.match(x) for x in a["horario_utc"]) and a["horario_utc"][0] != a["horario_utc"][1])


def _en_horario(a, horario):
    """Horario supervisado [desde, hasta) en UTC, al segundo; admite cruzar la medianoche (p. ej. 22:00-06:00). V0.50 (revisión,
    hallazgo 4): el extremo final ya no cuenta (antes, todo su minuto)."""
    u = a.astimezone(timezone.utc)
    t = u.hour * 3600 + u.minute * 60 + u.second + u.microsecond / 1e6
    d, h = (int(x[:2]) * 3600 + int(x[3:]) * 60 for x in horario)
    return d <= t < h if d < h else (t >= d or t < h)


def _avisos_ok(a):
    return (isinstance(a, dict) and set(a) == {"canal_alta", "canal_escalado", "reiterar_min", "escalar_tras"}
            and all(isinstance(a[k], str) and a[k] and a[k].upper() != "CHAT" for k in ("canal_alta", "canal_escalado"))
            and a["canal_escalado"] != a["canal_alta"] and _num(a["reiterar_min"]) and a["reiterar_min"] > 0
            and isinstance(a["escalar_tras"], int) and not isinstance(a["escalar_tras"], bool) and a["escalar_tras"] >= 1)


def _autoria_ok(v):
    return isinstance(v, dict) and set(v) == {"modelo", "proveedor"} and all(isinstance(x, str) and _ID.match(x) for x in v.values())


def _num(x):
    try:   # un entero enorme (JSON sin límite) desborda math.isfinite: no es un número utilizable (revisión T-49, R-01)
        return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)
    except OverflowError:
        return False


METRICAS_PRECIO = ("precio", "precio_cierre")   # T-49: métricas de precio; su unidad es la divisa de cotización del instrumento
_METRICA = re.compile(r"^[a-z][a-z0-9_]{0,63}\Z")   # grafía canónica de una métrica: H compara exactamente, sin normalizar
ALERTA_PERDIDA_RANGO = (-50.0, -0.5)   # T-49: límites de alerta_perdida_pct (revisión, R-06)


def senal_mal_formada(metrica, unidad, divisa):
    """T-49: una señal (escenario de fallo o invalidez) que H no podría evaluar bien: métrica sin grafía canónica, o métrica de
    precio en una unidad que no es la divisa de cotización (un % o otra divisa nunca se cumpliría o se cumpliría ya)."""
    if not (isinstance(metrica, str) and _METRICA.match(metrica)):
        return f"métrica {metrica!r} sin grafía canónica (minúsculas, cifras y _)"
    if metrica in METRICAS_PRECIO and unidad != divisa:
        return f"la métrica {metrica} va en la divisa de cotización del instrumento ({divisa}), no en {unidad!r}"
    if unidad is not None and not (isinstance(unidad, str) and _ID.match(unidad)):
        return "unidad mal formada"
    return None


def _senales_de(e):
    """T-49: lo que H vigila además de las condiciones de salida: los escenarios de fallo del Contradictor y las invalidez de la
    propuesta cuya métrica no es el precio. Ninguna vende: piden revisión."""
    out = []
    for x in (e.get("contradictor") or {}).get("escenarios_fallo", []):
        out.append({"clave": "CONTRADICTOR:" + x["id"], "id": x["id"], "origen": "CONTRADICTOR", "texto": str(x["descripcion"]), "metrica": x["disparador"]["metrica"],
                    "operador": x["disparador"]["operador"], "umbral": x["disparador"]["umbral"], "unidad": x["disparador"]["unidad"]})
    for c in e["propuesta"]["salida"]["condiciones"]:
        if c["tipo"] == "INVALIDEZ" and c["metrica"] != "precio":
            out.append({"clave": "INVALIDEZ:" + c["id"], "id": c["id"], "origen": "INVALIDEZ",   # la clave separa los dos espacios de ids (R-02)
                        "texto": str(c.get("descripcion") or f"{c['metrica']} {c['operador']} {c['umbral']}"),
                        "metrica": c["metrica"], "operador": c["operador"], "umbral": c["umbral"], "unidad": c.get("unidad")})
    return out


def perdida_pct(p, precio):
    """Pérdida (negativa) o ganancia no realizada de una posición, en % del precio de entrada, según su dirección."""
    r = (precio - p["precio_entrada"]) / p["precio_entrada"] * 100.0
    return r if p["direccion"] == "LARGO" else -r


def nivel_perdida(p, precio, umbral):
    """T-49: (pérdida en %, nivel) con el precio actual: el nivel es cuántas veces se ha perdido el umbral (0 si no llega).
    H y el Orquestador usan esta misma cuenta (revisión, R-07). None si no se puede calcular con esos datos."""
    if not (_num(precio) and precio > 0 and _num(p.get("precio_entrada")) and p["precio_entrada"] > 0 and _num(umbral) and umbral < 0):
        return None
    pp = perdida_pct(p, precio)
    q = pp / umbral
    if not (math.isfinite(pp) and math.isfinite(q)):
        return None
    return pp, (int(math.floor(q + 1e-9)) if pp < 0 else 0)


def _motivo_bloqueo(bl):
    return f"exclusión dura BLOQUEADO ({', '.join(bl)}): el candidato no compite"


def _es_bloqueo(a):
    """La anotación con la que el Orquestador descarta un candidato bloqueado (T-27)."""
    return a["actor"] == "ORQUESTADOR" and a["hasta"] == "DESCARTADA" and isinstance(a["motivo"], str) and a["motivo"].startswith("exclusión dura BLOQUEADO")


class RelojRetrocede(Exception):
    pass


NIVELES_CONTRADICTOR = ("N2", "N3")   # T-48: donde la Constitución lo quiere siempre (comparación y propuesta)
CONFIG_OBLIGATORIA = {"perfiles_activos", "clases_ratificadas", "apalancamiento_permitido"}   # sin valor por defecto: las fija el operador


def _valida_config(c):
    """La configuración se valida al construir: una configuración mala no arranca el Orquestador."""
    if set(c) - set(CONFIG_DEFECTO) - CONFIG_OBLIGATORIA:   # una errata no se ignora en silencio (T-25)
        raise ValueError(f"configuración del Orquestador inválida: claves desconocidas {sorted(set(c) - set(CONFIG_DEFECTO) - CONFIG_OBLIGATORIA)[:3]}")
    if CONFIG_OBLIGATORIA - set(c):
        raise ValueError(f"configuración del Orquestador inválida: faltan {sorted(CONFIG_OBLIGATORIA - set(c))}")
    ok = (politica_valida(c["politica_f"])
          and _num(c["alerta_perdida_pct"]) and ALERTA_PERDIDA_RANGO[0] <= c["alerta_perdida_pct"] <= ALERTA_PERDIDA_RANGO[1]
          and isinstance(c["exige_contradictor_en"], list)
          and all(isinstance(x, str) and x in ("N0", "N1", "N2", "N3") for x in c["exige_contradictor_en"])
          and isinstance(c.get("perfiles_activos"), list) and c["perfiles_activos"] and all(isinstance(x, str) for x in c["perfiles_activos"])
          and isinstance(c.get("clases_ratificadas"), dict) and isinstance(c.get("apalancamiento_permitido"), bool)
          and all(_num(c[k]) and c[k] > 0 for k in ("dia_coste_max_eur", "dia_tiempo_max_min", "tolerancia_precio_entrada"))
          and isinstance(c["max_reintentos"], int) and not isinstance(c["max_reintentos"], bool) and c["max_reintentos"] >= 1
          and isinstance(c["umbral_corte_comun_dias_habiles"], int) and not isinstance(c["umbral_corte_comun_dias_habiles"], bool)
          and c["umbral_corte_comun_dias_habiles"] >= 0
          and isinstance(c["exige_contradictor_en"], list) and isinstance(c["matriz_autonomia"], dict)
          and isinstance(c["autoria_c"], dict) and all(k in c["perfiles_activos"] and _autoria_ok(v) for k, v in c["autoria_c"].items())
          and (c["autoria_contradictor"] is None or _autoria_ok(c["autoria_contradictor"]))
          # quitar N2 o N3 de exige_contradictor_en (T-48) solo con motivo escrito en la configuración; con todos, sin motivo
          and ((set(NIVELES_CONTRADICTOR) <= set(c["exige_contradictor_en"])) == (c["contradictor_desactivado_motivo"] is None))
          and (c["contradictor_desactivado_motivo"] is None or (isinstance(c["contradictor_desactivado_motivo"], str)
                                                                and 3 <= len(c["contradictor_desactivado_motivo"].strip()) <= 200))
          and all(isinstance(v, bool) for v in c["matriz_autonomia"].values())
          and isinstance(c["umbral_l2_eur"], dict) and set(c["umbral_l2_eur"]) == {"TRADING", "TACTICA", "LARGO_PLAZO"}
          and all(_num(v) and v >= 0 for v in c["umbral_l2_eur"].values())
          and isinstance(c["promocion_nivel"], dict) and set(c["promocion_nivel"]) == {"periodo_min_dias"}
          and _num(c["promocion_nivel"]["periodo_min_dias"]) and 1 <= c["promocion_nivel"]["periodo_min_dias"] <= 365
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
          and isinstance(c["version_config"], str) and re.fullmatch(r"CFG-\d+\.\d+\.\d+", c["version_config"]) is not None
          and isinstance(c["revision_max_dias"], int) and not isinstance(c["revision_max_dias"], bool) and 1 <= c["revision_max_dias"] <= 366
          and isinstance(c["observacion_max_dias"], int) and not isinstance(c["observacion_max_dias"], bool) and 1 <= c["observacion_max_dias"] <= 366
          and isinstance(c["max_reaperturas"], int) and not isinstance(c["max_reaperturas"], bool) and 0 <= c["max_reaperturas"] <= 20
          and _num(c["tolerancia_tipo_k_rel"]) and 0 < c["tolerancia_tipo_k_rel"] <= 0.5
          and isinstance(c["anulaciones_veto_mes"], int) and not isinstance(c["anulaciones_veto_mes"], bool) and 0 <= c["anulaciones_veto_mes"] <= 10
          and isinstance(c["libres_tope_dia_eur"], dict) and set(c["libres_tope_dia_eur"]) == set(sc1.CARTERAS)   # T-33: exactamente las tres carteras
          and all(_num(v) and v >= 0 for v in c["libres_tope_dia_eur"].values())   # un tope es un número finito >= 0 (0.0 prohíbe las LIBRES valoradas)
          and isinstance(c["cuenta_intermediario"], str) and _ID.match(c["cuenta_intermediario"])
          and isinstance(c["divisas_cotizacion"], dict)
          and all(isinstance(k, str) and isinstance(v, str) and re.fullmatch(r"[A-Z]{3}", v) for k, v in c["divisas_cotizacion"].items())
          and isinstance(c["referencias"], dict) and set(c["referencias"]) == {"TRADING", "TACTICA", "LARGO_PLAZO"}
          and all(_referencia_ok(v) for v in c["referencias"].values())
          and isinstance(c["mandatos"], dict) and set(c["mandatos"]) == set(sc1.CARTERAS)
          and all(sc1.mandato_ok(k, v, c["apalancamiento_permitido"] is True) is None
                  and v["benchmark_ref"] == c["referencias"][k]["benchmark_ref"] for k, v in c["mandatos"].items()))
    if ok and not c["apalancamiento_permitido"] and c["politica_f"]["apalancamiento_max"] > 1:
        ok = False   # la política de F no puede permitir lo que el sistema prohíbe
    if not ok:
        raise ValueError("configuración del Orquestador inválida")


TOL_Q = 1e-6   # tolerancia de cantidades (la misma que G)
# Lo que define el control de una posición: va en la cadena de su historial (cada anotación lleva su hash)
CAMPOS_POS = ("posicion_id", "expediente_id", "estado", "cantidad", "cantidad_inicial", "cartera", "direccion", "instrumento", "activo_base",
              "stop_precio", "condiciones_salida", "via_acceso", "fecha_revision", "protecciones", "protecciones_anteriores", "reduccion", "reducciones", "condiciones_consumidas",
              "precio_entrada", "senales", "senales_disparadas", "perdida_alertada",   # T-49: lo que H vigila además de las salidas
              "propuestas")   # T-49 (revisión, R-04): las propuestas y alertas a la posición también van en la cadena


def _estado_pos(p):
    return {k: p.get(k) for k in CAMPOS_POS}


def _condiciones_reapertura_ok(conds, hoy):
    """T-46: condiciones comprobables. PRECIO {instrumento, operador, umbral}; FECHA {fecha futura}; SELLO_NUEVO {}."""
    if len(conds) > 10:
        return "como mucho 10"
    for c in conds:
        if not isinstance(c, dict) or c.get("tipo") not in ("PRECIO", "FECHA", "SELLO_NUEVO"):
            return "cada una debe ser PRECIO, FECHA o SELLO_NUEVO"
        if c["tipo"] == "PRECIO" and not (set(c) == {"tipo", "instrumento", "operador", "umbral"} and isinstance(c["instrumento"], str)
                                          and _ID.match(c["instrumento"]) and c["operador"] in OPERADORES and _num(c["umbral"]) and c["umbral"] > 0):
            return "PRECIO exige instrumento, operador y umbral positivo"
        if c["tipo"] == "FECHA":
            try:
                f = date.fromisoformat(c["fecha"]) if set(c) == {"tipo", "fecha"} and isinstance(c["fecha"], str) and _FECHA.match(c["fecha"]) else None
            except ValueError:
                f = None
            if f is None or f <= hoy:
                return "FECHA exige una fecha futura AAAA-MM-DD"
        if c["tipo"] == "SELLO_NUEVO" and set(c) != {"tipo"}:
            return "SELLO_NUEVO no lleva más campos"
    return None


def _identidad(e):
    d = {k: e.get(k) for k in ("expediente_id", "correlation_id", "via_entrada", "cartera_destino")}
    if e.get("via_entrada") == "DIRECTA":   # T-80: por dónde entró, qué análisis reutiliza y de qué consulta viene, encadenados
        d.update({k: e.get(k) for k in CAMPOS_DIRECTA})
    return d


VIVOS = ("VALIDADA", "COMPARADA", "PROPUESTA", "AUTORIZADA")   # candidato con análisis, en juego
# T-80 (D-28, §2 y §4.1 regla 6): vía DIRECTA. El Broker entra por C, D o E y el expediente nace en el estado de ese bloque;
# F y G nunca son punto de entrada. Una consulta no abre expediente: deja su rastro en SC-5
BLOQUES_DIRECTA = {"C": "EN_ANALISIS", "D": "VALIDADA", "E": "COMPARADA"}
REUTILIZABLE_DESDE = ("EN_OBSERVACION", "DESCARTADA")   # en juego, invertido, en reanálisis o caducado (§4.1, regla 4): no
MOTIVO_REUTILIZA = "análisis vigente reutilizado"   # la anotación que da a un expediente DIRECTA el sobre validado de otro
# §2: lo que falte al entrar por D se encarga a C con un análisis «de nivel bajo». [PROPUESTO] (QA de T-80, H-04): el más bajo con el
# que se puede invertir (N2), porque entrar por D es para decidir y con N1 el expediente nunca llegaría a una orden
NIVEL_BAJO = NIVEL_MIN_POR_DECISION["ABRIR_POSICION"]
TIPOS_CONSULTA = ("COMPARAR", "ANALIZAR", "PROYECTAR")   # §2: comparar, analizar o proyectar sin intención de invertir
BLOQUES_CONSULTA = ("A", "B", "C", "D", "E", "K")   # empieza y termina en un bloque de análisis o de datos, nunca en F ni G
CAMPOS_CONSULTA = ("consulta_id", "correlation_id", "tipo", "bloque", "cartera", "analisis", "pregunta")
CAMPOS_DIRECTA = ("bloque_entrada", "analisis_ref", "consulta_ref")   # solo los lleva un expediente DIRECTA (y van en su identidad)


def _canon(x):
    """Forma canónica para la huella: un entero y el mismo valor real cuentan igual (50 y 50.0)."""
    if isinstance(x, dict):
        return {str(k): _canon(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_canon(v) for v in x]
    if isinstance(x, (set, frozenset)):
        raise TypeError("un conjunto no es serializable de forma estable")
    if isinstance(x, int) and not isinstance(x, bool):
        return float(x)
    return x


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
        self.cal_def = copy.deepcopy(calendario)   # V0.44 (revisión, hallazgo 4): el Orquestador no comparte el calendario con quien lo crea
        Calendario(calendario)   # falla pronto si no es válido
        # T-25: la configuración entera (la del Orquestador, la política de F, los parámetros de K, D, H y CT-G-14 y las versiones
        # de reglas) tiene una huella; cada anotación del historial la lleva, así que se sabe con qué se decidió cada cosa
        try:
            self.huella_config = _hash(_canon(self._configuracion_completa()))
        except (TypeError, ValueError) as ex:
            raise ValueError(f"configuración del Orquestador inválida: {type(ex).__name__}") from ex
        # T-50: registro encadenado del límite de pérdida: su valor inicial, cada vez que se alcanza y cada cambio del operador
        self.limites = {"historial": [], "estado": "VIGENTE", "entradas": []}
        self._anota_limite({"tipo": "INICIO", LIMITE_PERDIDA: cfg["politica_f"][LIMITE_PERDIDA], "huella_config": self.huella_config},
                           "ORQUESTADOR", None, "límite de pérdida inicial")
        self.sellos, self.eventos, self.encargos = {}, {}, {}
        self.modelos, self.artefactos = {}, {}   # T-26: registro del Motor SC-3 (modelos declarados y artefactos de cálculo)
        self.sc3 = {"historial": [], "estado": "VIGENTE", "entradas": []}   # T-26 (R-M1): cadena de solo añadir del registro
        self.expedientes, self.posiciones, self.gasto_dia, self.avisos = {}, {}, {}, []
        self.ultima_comparacion = {}   # cartera -> id de la comparación vigente
        self.pantallas = {}            # expediente -> pantalla de aprobación con las cifras de F (§6)
        self.kill = None               # kill-switch activo: {"motivo", "actor", "ahora"}
        self.rearmes = []              # rehabilitaciones tras el kill-switch
        self.ultima_conciliacion = None   # {"ahora", "limpia"}: la anota G cada vez que concilia
        self.fotos = {}                   # hash -> foto de cartera tomada por G del intermediario (T-11), para auditoría
        self.cotizaciones = {}            # T-22: instrumento normalizado -> últimas cotizaciones del intermediario que registró G
        self.perdidas_dia = {}            # T-22: fecha UTC -> mayor pérdida del día que dieron las fotos de G (pérdida de la semana de F-16)
        self.ultima_foto = None           # la única que vale: la más reciente
        self.manuales = []     # registros CT-G-14 aceptados (lo que el operador hizo fuera del sistema)
        self.libres = []       # T-33: las LIBRES declaradas, una fila por registro, para su tope diario y para F-14
        self.cortacircuitos = []   # T-40: los días UTC en que el cortacircuito global por pérdida saltó, una fila por día
        self.degradadas = {}   # cartera -> motivo: bajada automática a L1 hasta que el operador la restablezca
        self.consultas = {"historial": [], "estado": "VIGENTE", "entradas": []}   # T-80: rastro SC-5 de las consultas, solo añadir
        self.ultimas_degradaciones = {}   # V0.51: cartera -> último instante en que se pidió degradarla (también en L0 o L1)

    # ------------------------------------------------------------ niveles de autonomía
    def nivel(self, cartera):
        """Nivel efectivo: el configurado, o L1 si la cartera está degradada (nunca sube solo)."""
        base = self.cfg["nivel_autonomia"].get(cartera, "L1")
        return "L1" if cartera in self.degradadas and NIVELES[base] > 1 else base

    def nivel_en(self, cartera, a):
        """V0.50 (T-18, §6): el nivel que rige en el instante a (datetime): L3 solo dentro del horario supervisado (el de la
        aprobación, P-12); fuera, L2. Degradada, L1 como siempre."""
        n = self.nivel(cartera)
        return "L2" if n == "L3" and not _en_horario(a, self.cfg["aprobacion"]["horario_utc"]) else n

    def _importe_eur(self, e, cantidad, entradas):
        """Importe en euros de la entrada (cantidad × límite × tipo de cambio de la cartera con la que F decidió), o None."""
        try:
            fx = tipo_cambio(entradas["solicitud"]["divisa_cotizacion"], entradas["cartera"])
            v = cantidad * e["propuesta"]["entrada"]["limite"] * fx
        except (KeyError, TypeError, ValueError):
            return None
        return v if _num(v) and v >= 0 else None

    def _matriz_permite(self, e, cantidad, entradas, a):
        """V0.50 (T-18): la matriz de autonomía decide sola en L3 dentro del horario supervisado (mandato y F) y en L2 solo hasta el
        umbral de la cartera (umbral_l2_eur). None si puede; si no, el error (O-05: lo aprueba el operador)."""
        c = e["cartera_destino"]
        n = self.nivel_en(c, a)
        if NIVELES[n] >= 3:
            return None
        if NIVELES[n] < 2:
            return _no("O-05", f"la cartera está en {n}: autoriza el operador")
        imp = self._importe_eur(e, cantidad, entradas)
        if imp is None:
            return _no("O-05", "no se puede valorar la entrada en euros: autoriza el operador")
        if imp > self.cfg["umbral_l2_eur"][c] * (1 + 1e-12):
            fuera = " (L3 fuera del horario supervisado: rige L2)" if self.nivel(c) == "L3" else ""
            return _no("O-05", f"la entrada ({round(imp, 2)} EUR) pasa del umbral de L2 de {c} ({self.cfg['umbral_l2_eur'][c]} EUR){fuera}: "
                               "autoriza el operador")
        return None

    def fin_horario_l3(self, e):
        """V0.50 (revisión, hallazgo 1): si la entrada la autorizó la matriz en L3 por encima del umbral de L2, el instante en que
        acaba el horario supervisado que empezó con la autorización (la orden no debe vivir más allá: fuera rige L2). None si no."""
        if self.autorizada_por(e) != "MATRIZ_AUTONOMIA" or self.nivel(e["cartera_destino"]) != "L3" or not e.get("control_f"):
            return None
        imp = self._importe_eur(e, e["control_f"]["cantidad_aprobada"], e["control_f"]["entradas"])
        if imp is not None and imp <= self.cfg["umbral_l2_eur"][e["cartera_destino"]] * (1 + 1e-12):
            return None
        aut = next((x["ahora"] for x in reversed(e["historial"]) if x["hasta"] == "AUTORIZADA" and x["desde"] != "AUTORIZADA"), None)
        if aut is None:
            return None
        a = _dt(aut).astimezone(timezone.utc)
        hh, mm = (int(x) for x in self.cfg["aprobacion"]["horario_utc"][1].split(":"))
        fin = a.replace(hour=hh, minute=mm, second=0, microsecond=0)
        return fin if fin > a else fin + timedelta(days=1)

    def _degradar(self, cartera, motivo, ahora):
        if cartera in ("TRADING", "TACTICA", "LARGO_PLAZO") and isinstance(ahora, str):   # V0.51: queda aunque no baje (L0, L1)
            prev = self.ultimas_degradaciones.get(cartera)
            if prev is None or _dt(ahora) > _dt(prev):
                self.ultimas_degradaciones[cartera] = ahora
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

    def _perdida_semana_eur(self, hasta):
        """T-40: la pérdida de la semana que mira F-16, con el criterio de _actividad: la suma plana, por día de los siete que
        acaban en `hasta` (fecha UTC, incluido), de la mayor pérdida del día que dieron las fotos de G. Suma plana de flotantes
        (no fsum): un conjunto que desborda da infinito y el cortacircuito salta con él, sin lanzar (r01)."""
        return _saturada(sum((v for d, v in self.perdidas_dia.items() if timedelta(0) <= hasta - date.fromisoformat(d) < timedelta(days=7)), 0.0))

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
        malos = self._contraste_tipos_k(foto["tipos_cambio_eur"])   # T-42: segunda fuente, K
        if malos:
            return _no("O-29", "tipo de cambio que no cuadra con el último cierre de K: " + "; ".join(malos))
        t = _dt(foto["fecha_hora"])
        if t > a or (a - t).total_seconds() > self.cfg["politica_f"]["frescura_max_min"] * 60:
            return _no("O-10", "la foto de cartera es del futuro o más vieja que la frescura que admite F")
        if self.ultima_foto and t < _dt(self.ultima_foto["fecha_hora"]):
            return _no("O-10", "la foto es anterior a la última registrada")
        h = _hash(foto)
        self.fotos[h] = {"ahora": ahora, "fecha_hora": foto["fecha_hora"]}
        d = t.astimezone(timezone.utc).date().isoformat()   # T-22: la mayor pérdida de cada día, para la de la semana (no se poda con las fotos)
        self.perdidas_dia[d] = max(self.perdidas_dia.get(d, 0.0), foto["perdida_dia_eur"])
        for k in [k for k in self.perdidas_dia if date.fromisoformat(k) < t.astimezone(timezone.utc).date() - timedelta(days=14)]:
            del self.perdidas_dia[k]
        self.ultima_foto = copy.deepcopy(foto)
        self._anota_alcance(foto, h, ahora)   # T-50: el día en que se alcanza el límite de pérdida no se puede subir
        if len(self.fotos) > 200:   # solo hacen falta las recientes
            for k in sorted(self.fotos, key=lambda k: _dt(self.fotos[k]["ahora"]))[:len(self.fotos) - 200]:
                del self.fotos[k]
        # T-40 (§8 y §11): el cortacircuito global por pérdida salta solo, con el mismo umbral en el que F-16 empieza a vetar.
        # La foto es buena y el registro se acepta igual; el kill-switch de siempre hace el resto (G cancela las entradas vivas).
        pol = self.cfg["politica_f"]
        semana_eur = self._perdida_semana_eur(t.astimezone(timezone.utc).date())
        salta = foto["perdida_dia_eur"] >= pol["perdida_dia_max_eur"] or semana_eur >= pol["perdida_semana_max_eur"]
        ya_hoy = any(x["dia"] == d for x in self.cortacircuitos)   # el aviso y la anotación, una vez por día UTC de la foto
        activa = salta and self.kill is None
        if activa:   # si ya estaba activo por otra causa, no se pisa el motivo; tras un rearme vuelve a saltar
            self._activar_kill((f"cortacircuito global: pérdida del día {foto['perdida_dia_eur']:.2f} EUR (límite {pol['perdida_dia_max_eur']:.2f} EUR)" if foto["perdida_dia_eur"] >= pol["perdida_dia_max_eur"] else
                                f"cortacircuito global: pérdida de la semana {semana_eur:.2f} EUR (límite {pol['perdida_semana_max_eur']:.2f} EUR)"), "ORQUESTADOR", ahora)
        if salta and (activa or not ya_hoy):   # V0.53 (revisión de GLM, g03): cada vez que activa el kill-switch deja fila y aviso
            self.cortacircuitos.append({"dia": d, "perdida_dia_eur": foto["perdida_dia_eur"], "perdida_semana_eur": semana_eur, "ahora": ahora})
            self._aviso("O-38", (f"cortacircuito global por pérdida: día {foto['perdida_dia_eur']:.2f} EUR (límite {pol['perdida_dia_max_eur']:.2f} EUR), "
                                 f"semana {semana_eur:.2f} EUR (límite {pol['perdida_semana_max_eur']:.2f} EUR)"), ahora, "CORTACIRCUITO")
        return _r(True, "OK", "foto de cartera registrada", hash=h, cortacircuito=salta)

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

    @_seguro
    def registrar_cotizacion(self, cotizacion, actor, ahora):
        """T-22 (§8, segunda fuente): G registra el precio que da el intermediario para un instrumento. F lo usa para la deriva
        del límite respecto al mercado y su frescura. Solo G; nunca del futuro ni anterior a la última de ese instrumento."""
        a = self._ahora(ahora)
        if actor != "G":
            return _no("O-05", "solo G registra cotizaciones del intermediario")
        if not (isinstance(cotizacion, dict) and set(cotizacion) == {"instrumento", "valor", "fecha_hora"} and isinstance(cotizacion["instrumento"], str)
                and sc1.norm(cotizacion["instrumento"]) and _num(cotizacion["valor"]) and cotizacion["valor"] > 0
                and isinstance(cotizacion["fecha_hora"], str) and _FH.match(cotizacion["fecha_hora"])):
            return _no("O-01", "cotización mal formada: instrumento, valor y fecha_hora")
        t = _dt(cotizacion["fecha_hora"])
        if t > a:
            return _no("O-10", "la cotización es del futuro")
        k = sc1.norm(cotizacion["instrumento"])
        hist = self.cotizaciones.get(k, [])
        if hist and t < _dt(hist[-1]["fecha_hora"]):
            return _no("O-10", "la cotización es anterior a la última registrada de ese instrumento")
        self.cotizaciones[k] = (hist + [{"valor": cotizacion["valor"], "fecha_hora": cotizacion["fecha_hora"], "registrada_en": ahora}])[-50:]
        return _r(True, "OK", "cotización registrada")

    def _cotizacion_en(self, instrumento, a):
        """La última cotización de G para el instrumento que ya estaba registrada en el instante `a` (así el contexto de un informe se
        puede rehacer después: una cotización que llega más tarde no lo cambia)."""
        return next(({"valor": x["valor"], "fecha_hora": x["fecha_hora"]} for x in reversed(self.cotizaciones.get(sc1.norm(instrumento), []))
                     if _dt(x["registrada_en"]) <= a), None)

    def _contexto_de_informe(self, expediente_id, control_f):
        """El contexto que el Orquestador habría dado a F en el instante de emisión del informe (CF-09). None si no se puede."""
        try:
            return self.contexto_f(expediente_id, control_f["emitido_en"])
        except Exception:   # noqa: BLE001
            return None

    def _actividad(self, excluido, a):
        """Lo que F necesita de la actividad reciente (T-22), sacado de los historiales: el importe autorizado hoy (UTC) por los demás
        expedientes; las órdenes de la última hora: los envíos de órdenes de entrada (reintentos incluidos, también los del propio
        expediente) más las autorizaciones de los demás que aún no se han enviado; y la pérdida de la semana: la suma, por día de los
        últimos siete, de la mayor pérdida del día que dieron las fotos de G."""
        hoy = a.astimezone(timezone.utc).date()
        importe, ordenes = 0.0, 0
        for k in sorted(self.expedientes):
            e = self.expedientes[k]
            if not e.get("control_f"):
                continue
            for x in e["historial"]:
                t = _dt(x["ahora"])
                if t > a:
                    continue
                if x["hasta"] == "AUTORIZADA" and x["desde"] == "AUTORIZADA" and x["motivo"] == "orden de entrada ENVIADA" and a - t <= timedelta(hours=1):
                    ordenes += 1
            if k == excluido:
                continue
            cf = e["control_f"]
            en = e["propuesta"]["entrada"]
            fx = tipo_cambio(cf["entradas"]["solicitud"]["divisa_cotizacion"], cf["entradas"]["cartera"]) or 0.0
            for x in e["historial"]:
                if x["hasta"] == "AUTORIZADA" and x["desde"] != "AUTORIZADA":
                    t = _dt(x["ahora"])
                    if t.astimezone(timezone.utc).date() == hoy and t <= a:
                        importe += cf["cantidad_aprobada"] * en["limite"] * fx
                    if timedelta(0) <= a - t <= timedelta(hours=1) and not any(
                            y["motivo"] == "orden de entrada ENVIADA" and _dt(y["ahora"]) >= t for y in e["historial"]):
                        ordenes += 1   # autorizada y aún sin enviar: su orden saldrá
        semana = _saturada(sum((v for d, v in self.perdidas_dia.items() if timedelta(0) <= hoy - date.fromisoformat(d) < timedelta(days=7)), 0.0))   # V0.53: saturada (finita); suma plana (no fsum): un desbordamiento da infinito y F-16 lo cierra, sin lanzar (r01)
        # T-33: las LIBRES declaradas cuentan en el importe del día de F (límites de la cuenta, no de la cartera), las de este día
        # UTC y solo las ya registradas en el instante `a`: así el contexto de un informe emitido antes sigue siendo el mismo (CF-09).
        # Una LIBRE sin importe no se puede valorar: cuenta como el importe máximo del día (sin valor no se sigue operando ese día).
        # Suma plana de flotantes (no fsum): un importe desbordado da infinito y F-14 lo cierra, sin lanzar (defecto_02).
        for x in self.libres:
            if x["dia"] == hoy.isoformat() and _dt(x["registrado_en"]) <= a:
                importe += x["importe_eur"] if x["importe_eur"] is not None else self.cfg["politica_f"]["importe_max_dia_eur"]
        return {"importe_dia_eur": importe, "ordenes_ultima_hora": ordenes, "perdida_semana_eur": semana}

    def _f_al_enviar(self, e, expediente_id, ahora):
        """T-22 (revisión H4): al enviar la orden de entrada, F vuelve a comprobar lo que depende del momento (fin de semana, eventos,
        precio del intermediario, evidencia vigente, mandato, pérdidas y órdenes por hora) con el contexto de ese instante."""
        cf = e["control_f"]
        ctx = self.contexto_f(expediente_id, ahora)
        sol = {**cf["entradas"]["solicitud"], "cantidad": cf["cantidad_aprobada"]}
        vetos = [c for c in controles_de_contexto(sol, cf["entradas"]["politica"], ahora, ctx) if c["resultado"] == "VETA"]
        if vetos:
            return _no("O-06", f"F no aprobaría el envío ahora: {vetos[0]['regla']}: {vetos[0]['motivo'][:80]}", reglas=sorted({c['regla'] for c in vetos}))
        return None

    def contexto_f(self, expediente_id, ahora):
        """T-22: lo que F necesita además de la solicitud, la cartera y la política para los controles previos de la §8, sacado de
        los registros del Orquestador y no de quien propone. None si el expediente no tiene propuesta o el instante es ilegible.
        El informe de F debe llevar exactamente este contexto, calculado al instante de su emisión (CF-09)."""
        e = self.expedientes.get(expediente_id)
        if not isinstance(e, dict) or not e.get("propuesta"):
            return None
        try:
            a = _dt(ahora)
        except Exception:   # noqa: BLE001
            return None
        m = self._mandato_efectivo(e)
        en = e["propuesta"]["entrada"]
        p = e["sobre"]["documento"]["payload"]
        hoy = a.astimezone(timezone.utc).date()
        sello_e = self.sellos.get((self.encargos.get(e.get("encargo_actual")) or {}).get("sello_ref")) or {}
        ev = eventos_entre(sello_e, hoy.isoformat(), (hoy + timedelta(days=self.cfg["politica_f"]["ventana_eventos_dias"])).isoformat(), en["instrumento"])
        cot = self._cotizacion_en(en["instrumento"], a)
        return {"mandato": {"version": m["version"], "instrumentos_permitidos": copy.deepcopy(m["instrumentos_permitidos"]),
                            "exclusiones": list(m["exclusiones"]), "apalancamiento_max": m["apalancamiento_max"],
                            "horizonte_max_dias": m["horizonte_dias"]["max"]},
                "fecha_revision": e["propuesta"]["salida"]["fecha"],
                "exclusiones_duras": copy.deepcopy(p["exclusiones_duras"]),
                "evidencia": {"proporcion_verificado": p["evidencia"]["proporcion"]["VERIFICADO"],
                              "fecha_corte": p["identificacion"]["fecha_corte"], "valid_until": e["sobre"]["valid_until"]},
                "eventos": None if ev is None else [{"fecha": x["fecha"], "tipo": x["tipo"]} for x in ev],
                # el nivel configurado (la degradación la vigilan la matriz y G; F-22 solo exige un nivel conocido y sin kill-switch)
                "autonomia": {"nivel": self.cfg["nivel_autonomia"].get(e["cartera_destino"], "L1"), "kill_switch": self.kill is not None},
                "actividad": self._actividad(expediente_id, a),
                "precio_intermediario": cot}

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
        if self.kill["actor"] == "ORQUESTADOR" and self.kill["motivo"].startswith("cortacircuito") and self.ultima_foto is not None:   # T-40: no se rearma con la pérdida aún en el límite; el kill VINO del cortacircuito (actor ORQUESTADOR y su prefijo), no uno manual con un motivo parecido (r02)
            pol = self.cfg["politica_f"]
            uf = self.ultima_foto
            if uf["perdida_dia_eur"] >= pol["perdida_dia_max_eur"] or self._perdida_semana_eur(_dt(uf["fecha_hora"]).astimezone(timezone.utc).date()) >= pol["perdida_semana_max_eur"]:
                return _no("O-35", "la pérdida sigue en el límite: no se rearma hasta que baje o cambie el día")
        integ = self.integridad()   # T-52 (V0.53): no se rearma con historiales, posiciones, configuración, Motor o sellos que no cuadran
        if integ:
            return _no("O-13", f"la integridad no se supera ({', '.join(integ)}): no se rearma hasta corregirlo")
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
                **{"POS:" + k: v["historial"][-1]["hash"] for k, v in self.posiciones.items()},
                "LIM": self.limites["historial"][-1]["hash"],
                **({"SC3": self.sc3["historial"][-1]["hash"]} if self.sc3["historial"] else {}),
                **({"SC5": self.consultas["historial"][-1]["hash"]} if self.consultas["historial"] else {})}

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

    def autorizacion_vigente(self, e, a=None):
        """Una autorización automática deja de valer si la cartera bajó de nivel (V0.50: también si se degradó después de autorizar,
        aunque luego se restableciera, y, con el instante a, si la matriz ya no podría decidirla: L3 fuera de horario por encima
        del umbral de L2); cualquier autorización deja de valer si después se bajó el límite de pérdida del día (T-50, revisión
        R-M3: F la aprobó con la política anterior). G no envía la entrada y H la cancela si está viva."""
        aut = next((x["ahora"] for x in reversed(e["historial"]) if x["hasta"] == "AUTORIZADA" and x["desde"] != "AUTORIZADA"), None)
        if self.autorizada_por(e) == "MATRIZ_AUTONOMIA":
            c = e["cartera_destino"]
            if NIVELES[self.nivel(c)] < 2:
                return False
            # revisión de V0.50, hallazgo 2: una degradación posterior (aviso O-19 de la cartera) la anula aunque se restablezca
            if aut and any(x["codigo"] == "O-19" and c in (x.get("carteras") or []) and _dt(x["ahora"]) >= _dt(aut) for x in self.avisos):
                return False
            # V0.51: y también si el operador bajó después el nivel de la cartera (aunque luego lo volviera a subir)
            if aut and any(x["tipo"] == "NIVEL" and x["cartera"] == c and NIVELES[x["nivel"]] < NIVELES[x["antes"]] and _dt(h["ahora"]) >= _dt(aut)
                           for h, x in zip(self.limites["historial"], self.limites["entradas"])):
                return False
            if a is not None and e.get("control_f") and self._matriz_permite(e, e["control_f"]["cantidad_aprobada"], e["control_f"]["entradas"], a):
                return False
        # V0.46: una migración a un código que cambia la configuración completa también la deja sin valor (se decidió con otro)
        return aut is None or not any(((x["tipo"] == "CAMBIO" and x[LIMITE_PERDIDA] < x["antes"]) or _migracion_que_cambia(x)) and _dt(h["ahora"]) >= _dt(aut)
                                      for h, x in zip(self.limites["historial"], self.limites["entradas"]))

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
                and self._orden_ok(e) and self._aprobacion_ok(e) and self._reapertura_ok(e) and self._exclusion_ok(e))

    @staticmethod
    def _exclusion_ok(e):
        """T-27: la exclusión guardada es la anotada por el Orquestador al descartar (hash del sobre, su id y los bloqueos)."""
        b = [a for a in e["historial"] if _es_bloqueo(a)]
        ex = e.get("exclusion")
        if not b:
            return ex is None
        a = b[-1]
        return (isinstance(ex, dict) and set(ex) == {"event_id", "hash", "bloqueos"} and a["datos"] == ex["hash"] and a["ref"] == ex["event_id"]
                and a["motivo"] == _motivo_bloqueo(ex["bloqueos"]))

    @staticmethod
    def _identidad_ok(e):
        """La cartera, la petición y el encargo vigente del expediente son los anotados (T-36: sin ellos se le saca de una comparación)."""
        h = e["historial"]
        if h[0]["datos"] != _hash(_identidad(e)):
            return False
        if e.get("via_entrada") != "DIRECTA" and any(k in e for k in CAMPOS_DIRECTA):   # QA de T-80, H-07: fuera de la identidad
            return False
        enc = [x["ref"] for x in h if (x["hasta"] == "EN_ANALISIS" and x["motivo"] == "encargo emitido")
               or (e.get("via_entrada") == "DIRECTA" and x["desde"] == x["hasta"] == "VALIDADA" and x["actor"] == "ORQUESTADOR" and isinstance(x["motivo"], str)
                   and x["motivo"].startswith(MOTIVO_REUTILIZA))]
        return e.get("encargo_actual") == (enc[-1] if enc else None)

    def _rota(self):
        """Primer expediente cuya integridad no cuadra (cualquier cartera), o None."""
        if not self.config_integra():
            return "CONFIG"
        if not self.motor_ok():   # T-26: el registro del Motor alterado es como un expediente roto
            return "MOTOR"
        if not self.sellos_ok():   # T-26 (R-M2): un sello de K retocado (p. ej. sin su advertencia)
            return "SELLOS"
        if not self.consultas_ok():   # T-80: el rastro de las consultas (SC-5) retocado
            return "CONSULTAS"
        return next((k for k, x in sorted(self.expedientes.items()) if not self._todo_ok(x)), None)

    def integridad(self):
        """Lista de expedientes (EXP:) y posiciones (POS:) cuyo historial, sobre, comparación o propuesta no cuadra."""
        return sorted(["EXP:" + k for k, v in self.expedientes.items() if not self._todo_ok(v)]
                      + ["POS:" + k for k, v in self.posiciones.items() if not self._posicion_ok(v)]
                      + ([] if self.config_integra() else ["CONFIG"]) + ([] if self.motor_ok() else ["MOTOR"])
                      + ([] if self.sellos_ok() else ["SELLOS"]) + ([] if self.consultas_ok() else ["CONSULTAS"]))

    def _configuracion_completa(self):
        """Todo lo que decide: la configuración del Orquestador (con la política de F), los parámetros versionados de K, D, H, E y
        CT-G-14, el calendario, las constantes de política del Orquestador y las versiones de reglas."""
        return {"version_config": self.cfg["version_config"], "orquestador": self.cfg, "version_parametros": VERSION_PARAMETROS,
                "parametros": como_dict(PARAMETROS), "calendario": self.cal_def,
                "constantes": {"prioridad_aviso": PRIORIDAD_AVISO, "tipos_kill": sorted(TIPOS_KILL), "vetos_anulables": list(VETOS_ANULABLES),
                               "topes_f": list(TOPES_F), "limite_perdida": LIMITE_PERDIDA, "motivo_min": MOTIVO_MIN,
                               "incidentes_promocion": list(INCIDENTES_PROMOCION)},
                "reglas": {"orquestador": VERSION_REGLAS, "f": VERSION_REGLAS_F, "k": VERSION_REGLAS_K}}

    def config_integra(self):
        """La configuración en uso es la de la huella (nadie la cambió en caliente) y la huella es la del último cambio anotado
        en el registro de límites (T-50: solo `ajustar_limite_perdida` la cambia)."""
        try:
            return _hash(_canon(self._configuracion_completa())) == self.huella_config and self._limites_ok()
        except (TypeError, ValueError, KeyError, IndexError, AttributeError):   # un registro mal formado tampoco es íntegro (R-m4)
            return False

    # ------------------------------------------------------------ T-50: controles sobre el operador (§6)
    def _anota_limite(self, entrada, actor, ahora, motivo):
        L = self.limites
        L["entradas"].append(entrada)
        self._anota(L, "VIGENTE" if L["historial"] else None, "VIGENTE", actor, ahora, motivo, entrada["tipo"], datos=_hash(entrada))

    def _limites_ok(self):
        L = self.limites
        if not (self._historial_ok(L) and len(L["historial"]) == len(L["entradas"])
                and all(h["datos"] == _hash(x) and h["ref"] == x["tipo"] for h, x in zip(L["historial"], L["entradas"]))):
            return False
        ult = [x for x in L["entradas"] if x["tipo"] in ("INICIO", "CAMBIO", "MIGRACION", "NIVEL")]   # V0.46 y V0.51: también fijan la huella
        return (bool(ult) and L["entradas"][0]["tipo"] == "INICIO" and ult[-1]["huella_config"] == self.huella_config
                and self.cfg["politica_f"][LIMITE_PERDIDA] == ult[-1][LIMITE_PERDIDA])

    def _limite_en(self, t):
        """Valor del límite de pérdida del día vigente en el instante t (el INICIO vale desde siempre)."""
        v = None
        for h, x in zip(self.limites["historial"], self.limites["entradas"]):
            if x["tipo"] == "INICIO" or (x["tipo"] == "CAMBIO" and _dt(h["ahora"]) <= t):
                v = x[LIMITE_PERDIDA]
        return v

    def _limite_min(self, t0, t1):
        """El límite de pérdida más bajo que rigió entre t0 y t1: con él se juzga si una foto alcanzó el límite (revisión, R-M2)."""
        vs = [self._limite_en(t0)] + [x[LIMITE_PERDIDA] for h, x in zip(self.limites["historial"], self.limites["entradas"])
                                      if x["tipo"] == "CAMBIO" and t0 < _dt(h["ahora"]) <= t1]
        return min(vs)

    def _alcanzado_reciente(self, a):
        """§6.3: el límite de pérdida se alcanzó en las últimas 24 horas (cubre el «mismo día» en cualquier zona horaria): una entrada
        ALCANZADO o la última foto, juzgada con el límite más bajo que rigió desde que se tomó."""
        if any(x["tipo"] == "ALCANZADO" and timedelta(0) <= a - _dt(x["fecha_hora"]) < timedelta(hours=24) for x in self.limites["entradas"]):
            return True
        f = self.ultima_foto
        if not f or a - _dt(f["fecha_hora"]) >= timedelta(hours=24):
            return False
        return f["perdida_dia_eur"] >= self._limite_min(_dt(f["fecha_hora"]), a) / 100 * f["capital_eur"]

    def _anota_alcance(self, foto, h, ahora, fecha_hora=None, limite_pct=None):
        """La pérdida del día de la foto está en el límite o más allá (el más bajo que rigió desde la foto; o el que se acaba de
        fijar al bajarlo): se anota una vez por día (UTC de la foto) y se avisa."""
        t = _dt(foto["fecha_hora"])
        pct = limite_pct if limite_pct is not None else self._limite_min(t, _dt(ahora))
        lim = pct / 100 * foto["capital_eur"]
        cuando = fecha_hora or foto["fecha_hora"]
        dia = _dia(_dt(cuando))
        if foto["perdida_dia_eur"] < lim or any(x["tipo"] == "ALCANZADO" and x["dia"] == dia and x["limite_pct"] <= pct for x in self.limites["entradas"]):
            return
        self._anota_limite({"tipo": "ALCANZADO", "dia": dia, "fecha_hora": cuando, "perdida_dia_eur": foto["perdida_dia_eur"],
                            "limite_pct": pct, "limite_eur": lim, "foto": h}, "ORQUESTADOR", ahora,
                           f"límite de pérdida del día alcanzado ({foto['perdida_dia_eur']:.2f} EUR, límite {lim:.2f} EUR)")
        self._aviso("O-35", f"límite de pérdida del día alcanzado el {dia}: no se puede subir en 24 horas", ahora, "LIMITE_PERDIDA")

    def version_politica(self):
        """Versión de la política de F: POL-0 la inicial y una más por cada cambio anotado."""
        return f"POL-{sum(1 for x in self.limites['entradas'] if x['tipo'] == 'CAMBIO')}"

    def _subida_pendiente(self):
        """La última solicitud de subida del límite, si no la siguió ningún cambio."""
        for x in reversed(self.limites["entradas"]):
            if x["tipo"] == "CAMBIO" or _migracion_que_cambia(x):   # V0.46: una migración a otro código anula la solicitud pendiente
                return None
            if x["tipo"] == "SOLICITUD":
                return x
        return None

    @_seguro
    def ajustar_limite_perdida(self, nuevo_pct, actor, motivo, ahora, aprobacion=None):
        """§6.3: el operador ajusta el límite de pérdida del día de la política de F; cada cambio crea una versión nueva de la
        política (POL-n) y de la huella de configuración. Bajarlo vale siempre (si la pérdida ya pasa del nuevo límite, queda
        anotado como alcanzado). Subirlo se hace en dos pasos con la misma llamada: la primera la solicita y la segunda, pasado el
        enfriamiento (§6.1) y antes de que caduque, la aplica. Para subir hace falta canal admitido y segundo factor, sin kill-switch,
        con una foto de cartera reciente, sin haber alcanzado el límite en las últimas 24 horas y sin pasar del límite inicial
        (más arriba exige la validación de J, §8.3, que aún no existe). Todo queda en el registro encadenado de límites."""
        a = self._ahora(ahora)
        if actor != "OPERADOR":
            return _no("O-05", "solo el operador ajusta un límite de pérdida")
        if not _motivo_ok(motivo):
            return _no("O-15", f"un cambio de límite exige motivo (al menos {MOTIVO_MIN} caracteres)")
        if not self.config_integra():
            return _no("O-13", "la configuración o el registro de límites no son íntegros")
        actual = self.cfg["politica_f"][LIMITE_PERDIDA]
        pol = {**self.cfg["politica_f"], LIMITE_PERDIDA: nuevo_pct}
        if not (_num(nuevo_pct) and nuevo_pct > 0 and politica_valida(pol)):
            return _no("O-01", "el límite de pérdida debe ser un número mayor que 0 y no mayor que 100")
        if nuevo_pct == actual:
            return _no("O-02", "el límite ya tiene ese valor")
        sube = nuevo_pct > actual
        canal = None
        if sube:
            if self.kill is not None:
                return _no("O-26", "kill-switch activo: no se sube ningún límite")
            if not (isinstance(aprobacion, dict) and set(aprobacion) == {"canal", "segundo_factor"}
                    and aprobacion["canal"] in self.cfg["aprobacion"]["canales"] and aprobacion["segundo_factor"] is True):
                return _no("O-05", "subir un límite de pérdida exige un canal de aprobación admitido (no el chat) y segundo factor")
            if nuevo_pct > self.limites["entradas"][0][LIMITE_PERDIDA]:
                return _no("O-35", "por encima del límite inicial hace falta la validación de J (§8.3): no se sube desde aquí")
            f = self.ultima_foto
            if not f or not timedelta(0) <= a - _dt(f["fecha_hora"]) <= timedelta(minutes=self.cfg["politica_f"]["frescura_max_min"]):
                return _no("O-35", "sin una foto de cartera reciente no se sabe si el límite se alcanzó: no se sube")
            if self._alcanzado_reciente(a):
                return _no("O-35", "el límite de pérdida se alcanzó en las últimas 24 horas: no se puede subir (Constitución §6)")
            canal = aprobacion["canal"]
            pend = self._subida_pendiente()
            cad = timedelta(minutes=self.cfg["aprobacion"]["caduca_min"])
            if not (pend and pend[LIMITE_PERDIDA] == nuevo_pct and pend["motivo"] == motivo and a <= _dt(pend["hasta"]) + cad):
                hasta = a + timedelta(minutes=self.cfg["aprobacion"]["enfriamiento_min"])
                self._anota_limite({"tipo": "SOLICITUD", "antes": actual, LIMITE_PERDIDA: nuevo_pct, "motivo": motivo, "canal": canal,
                                    "hasta": hasta.isoformat()}, "OPERADOR", ahora, f"solicitud de subir el límite de pérdida a {nuevo_pct} %")
                return _r(True, "O-28", f"subida solicitada: confírmela con la misma llamada desde {hasta.isoformat()} "
                                        f"y hasta {(hasta + cad).isoformat()}", aplicado=False, confirmar_desde=hasta.isoformat())
            if a < _dt(pend["hasta"]):
                return _no("O-28", f"enfriamiento hasta {pend['hasta']}: la subida aún no se puede confirmar")
        self.cfg["politica_f"] = pol
        self.huella_config = _hash(_canon(self._configuracion_completa()))
        n = sum(1 for x in self.limites["entradas"] if x["tipo"] == "CAMBIO") + 1
        self._anota_limite({"tipo": "CAMBIO", "antes": actual, LIMITE_PERDIDA: nuevo_pct, "huella_config": self.huella_config,
                            "motivo": motivo, "canal": canal, "version_politica": f"POL-{n}"}, "OPERADOR", ahora,
                           f"límite de pérdida del día {'subido' if sube else 'bajado'} de {actual} % a {nuevo_pct} %: {motivo[:120]}")
        f = self.ultima_foto
        if not sube and f and a - _dt(f["fecha_hora"]) < timedelta(hours=24):   # bajarlo por debajo de la pérdida es alcanzarlo (R-M1)
            self._anota_alcance(f, _hash(f), ahora, fecha_hora=ahora, limite_pct=nuevo_pct)
        self._aviso("O-35", f"límite de pérdida del día {'subido' if sube else 'bajado'} de {actual} % a {nuevo_pct} % (POL-{n})", ahora, "LIMITE_PERDIDA")
        return _r(True, "OK", f"límite de pérdida del día: {actual} % -> {nuevo_pct} % (POL-{n}); los informes de F anteriores ya no valen"
                  + ("; las autorizaciones anteriores tampoco" if not sube else ""), aplicado=True, version_politica=f"POL-{n}")

    def _nivel_pendiente(self, cartera):
        """V0.51: la solicitud de subir el nivel de la cartera aún sin confirmar (la última, si no la siguió un cambio de nivel de esa
        cartera ni una migración a otro código), o None."""
        for x in reversed(self.limites["entradas"]):
            if (x["tipo"] == "NIVEL" and x.get("cartera") == cartera) or _migracion_que_cambia(x):
                return None
            if x["tipo"] == "SOLICITUD_NIVEL" and x.get("cartera") == cartera:
                return x
        return None

    def _primer_instante(self):
        """El instante más antiguo que el Orquestador tiene anotado (historiales de límites, Motor, expedientes y posiciones, y
        avisos), o None. El INICIO del registro de límites no lleva instante (se crea antes de la primera llamada), así que el
        tiempo en el nivel de partida se cuenta desde aquí: nunca es anterior al arranque real, de modo que el periodo medido no
        puede salir más largo que el verdadero (falla cerrado)."""
        ts = [h["ahora"] for ent in (self.limites, self.sc3, *self.expedientes.values(), *self.posiciones.values())
              for h in ent["historial"] if h["ahora"] is not None]
        ts += [x["ahora"] for x in self.avisos if x["ahora"] is not None]
        return min((_dt(t) for t in ts), default=None)

    def _desde_ultimo_nivel(self, cartera):
        """Instante desde el que la cartera está en su nivel: el del último cambio de nivel de esa cartera o, si no lo hubo, el
        primer instante anotado del sistema (_primer_instante). None si no hay ninguno: sin historial no se promociona."""
        t = None
        for h, x in zip(self.limites["historial"], self.limites["entradas"]):
            if x["tipo"] == "NIVEL" and x.get("cartera") == cartera:
                t = _dt(h["ahora"])
        return t if t is not None else self._primer_instante()

    def criterios_promocion(self, cartera, a):
        """V0.51 (§6, P-02 [PROPUESTO]): lo que impide subir de nivel la cartera en el instante a. Lista vacía si nada.
        - Llevar promocion_nivel.periodo_min_dias en el nivel actual (desde su último cambio de nivel o el primer instante anotado).
        - En la ventana de esos mismos días antes de a (revisión de V0.51, hallazgo 5: un incidente antiguo no bloquea para siempre):
          ninguna degradación de la cartera, tampoco en L0 o L1 (ultimas_degradaciones; hallazgo 1), ni aviso O-19 suyo; ningún
          kill-switch activado ni rearmado; el límite de pérdida del día no alcanzado ningún día de la ventana (por día, porque se
          anota una vez al día; hallazgo 3); ningún aviso de INCIDENTES_PROMOCION (O-03, O-18, O-25) de la cartera o sin atribuir.
        - Ningún aviso de esos sin acusar, sea de cuando sea (hallazgo 4: una discrepancia abierta no se repite en avisos nuevos).
        - Datos que lo prueben (hallazgo 2): una foto de cartera reciente y una conciliación limpia dentro de la ventana, la última.
        - Ahora: integridad superada, sin kill-switch y la cartera sin degradar."""
        desde = self._desde_ultimo_nivel(cartera)
        dias = self.cfg["promocion_nivel"]["periodo_min_dias"]
        if desde is None or a - desde < timedelta(days=dias):
            return [f"periodo mínimo de {dias} días en el nivel actual (desde {desde.isoformat() if desde else '¿?'})"]
        v = a - timedelta(days=dias)   # inicio de la ventana que tiene que estar limpia
        falta = []
        if self.integridad():
            falta.append(f"integridad no superada: {', '.join(self.integridad())}")
        if cartera in self.degradadas:
            falta.append("la cartera está degradada")
        ud = self.ultimas_degradaciones.get(cartera)
        if ud is not None and _dt(ud) >= v:
            falta.append(f"la cartera se degradó en el periodo ({ud})")
        if self.kill is not None or any(_dt(r["kill"]["ahora"]) >= v or _dt(r["ahora"]) >= v for r in self.rearmes):
            falta.append("hubo kill-switch en el periodo")
        for x in self.avisos:
            suya = x.get("carteras") is None or cartera in x["carteras"]
            if x["codigo"] == "O-19" and cartera in (x.get("carteras") or []) and (_dt(x["ahora"]) >= v or x["acuse"] is None):
                falta.append(f"degradación {'sin acusar' if x['acuse'] is None else 'en el periodo'} ({x['id']})")
            elif x["codigo"] in INCIDENTES_PROMOCION and suya and (_dt(x["ahora"]) >= v or x["acuse"] is None):
                falta.append(f"incidente {x['codigo']} {'sin acusar' if x['acuse'] is None else 'en el periodo'} ({x['id']})")
        if any(x["tipo"] == "ALCANZADO" and x["dia"] >= v.date().isoformat() for x in self.limites["entradas"]):
            falta.append("el límite de pérdida del día se alcanzó en el periodo")
        f = self.ultima_foto
        if not f or not timedelta(0) <= a - _dt(f["fecha_hora"]) <= timedelta(minutes=self.cfg["politica_f"]["frescura_max_min"]):
            falta.append("sin una foto de cartera reciente")
        uc = self.ultima_conciliacion
        if not (uc and uc["limpia"] and v <= _dt(uc["ahora"]) <= a):
            falta.append("sin una conciliación limpia en el periodo (la última)")
        return falta

    @_seguro
    def cambiar_nivel(self, cartera, nivel, actor, motivo, ahora, aprobacion=None):
        """V0.51 (T-18, §6): el operador cambia el nivel de autonomía de una cartera sin reiniciar. Bajar vale siempre y es inmediato.
        Subir es de un nivel en uno, en dos llamadas iguales como el límite de pérdida (la primera solicita; la segunda, pasado el
        enfriamiento y antes de que caduque, aplica), con canal admitido, segundo factor, sin kill-switch y cumpliendo los criterios
        de promoción (criterios_promocion; O-39). Cada cambio es una entrada NIVEL del registro de límites con la huella nueva de la
        configuración: no es un incidente. Aviso O-39."""
        a = self._ahora(ahora)
        if actor != "OPERADOR":
            return _no("O-05", "solo el operador cambia el nivel de autonomía")
        if cartera not in ("TRADING", "TACTICA", "LARGO_PLAZO"):
            return _no("O-01", "cartera desconocida")
        if not (isinstance(nivel, str) and nivel in NIVELES):
            return _no("O-01", f"nivel desconocido (válidos: {', '.join(NIVELES)})")
        if not _motivo_ok(motivo):
            return _no("O-15", f"un cambio de nivel exige motivo (al menos {MOTIVO_MIN} caracteres)")
        rota = self._config_rota()   # revisión de V0.51, hallazgo 6: kill-switch y aviso, como en el resto (todo pasa a L1)
        if rota:
            return rota
        actual = self.cfg["nivel_autonomia"].get(cartera, "L1")
        if nivel == actual:
            return _no("O-02", f"la cartera ya está configurada en {nivel}")
        sube = NIVELES[nivel] > NIVELES[actual]
        canal = None
        if sube:
            if NIVELES[nivel] != NIVELES[actual] + 1:
                return _no("O-39", "se sube de un nivel en uno: cada nivel exige su periodo mínimo")
            if self.kill is not None:
                return _no("O-26", "kill-switch activo: no se sube ningún nivel")
            if not (isinstance(aprobacion, dict) and set(aprobacion) == {"canal", "segundo_factor"}
                    and aprobacion["canal"] in self.cfg["aprobacion"]["canales"] and aprobacion["segundo_factor"] is True):
                return _no("O-05", "subir un nivel exige un canal de aprobación admitido (no el chat) y segundo factor")
            falta = self.criterios_promocion(cartera, a)
            if falta:
                return _no("O-39", f"no se cumplen los criterios para subir {cartera} a {nivel}: {'; '.join(falta[:4])}", criterios=falta)
            canal = aprobacion["canal"]
            pend = self._nivel_pendiente(cartera)
            cad = timedelta(minutes=self.cfg["aprobacion"]["caduca_min"])
            if not (pend and pend["nivel"] == nivel and pend["antes"] == actual and pend["motivo"] == motivo and pend["canal"] == canal
                    and a <= _dt(pend["hasta"]) + cad):
                hasta = a + timedelta(minutes=self.cfg["aprobacion"]["enfriamiento_min"])
                self._anota_limite({"tipo": "SOLICITUD_NIVEL", "cartera": cartera, "antes": actual, "nivel": nivel, "motivo": motivo,
                                    "canal": canal, "hasta": hasta.isoformat()}, "OPERADOR", ahora, f"solicitud de subir {cartera} a {nivel}")
                return _r(True, "O-28", f"subida solicitada: confírmela con la misma llamada desde {hasta.isoformat()} "
                                        f"y hasta {(hasta + cad).isoformat()}", aplicado=False, confirmar_desde=hasta.isoformat())
            if a < _dt(pend["hasta"]):
                return _no("O-28", f"enfriamiento hasta {pend['hasta']}: la subida aún no se puede confirmar")
        self.cfg["nivel_autonomia"] = {**self.cfg["nivel_autonomia"], cartera: nivel}
        self.huella_config = _hash(_canon(self._configuracion_completa()))
        self._anota_limite({"tipo": "NIVEL", "cartera": cartera, "antes": actual, "nivel": nivel, LIMITE_PERDIDA: self.cfg["politica_f"][LIMITE_PERDIDA],
                            "huella_config": self.huella_config, "motivo": motivo, "canal": canal}, "OPERADOR", ahora,
                           f"nivel de {cartera} {'subido' if sube else 'bajado'} de {actual} a {nivel}: {motivo[:120]}")
        self._aviso("O-39", f"nivel de autonomía de {cartera} {'subido' if sube else 'bajado'} de {actual} a {nivel}", ahora, cartera, carteras={cartera})
        return _r(True, "OK", f"{cartera}: {actual} -> {nivel}", aplicado=True)

    def anulaciones_mes(self, ahora):
        """Anulaciones de veto autorizadas en el mes natural (UTC) de ese instante, contadas en las cadenas de los expedientes."""
        m = _mes(_dt(ahora))
        return sum(1 for e in self.expedientes.values() for h in e["historial"]
                   if h["hasta"] == "AUTORIZADA" and h["desde"] != "AUTORIZADA" and isinstance(h["motivo"], str)
                   and h["motivo"].startswith("ANULACIÓN DE VETO") and _mes(_dt(h["ahora"])) == m)

    def _comprobar_anulacion(self, cf, anular_veto, a):
        """§6.2 y §8: la anulación de un veto de F. Devuelve (cantidad, vetos, error). La cantidad es la que F habría aprobado sin el
        veto: la solicitada recortada por sus topes; nunca más."""
        if not (isinstance(anular_veto, dict) and set(anular_veto) == {"motivo"} and _motivo_ok(anular_veto["motivo"])):
            return None, None, _no("O-15", f"anular un veto exige motivo (al menos {MOTIVO_MIN} caracteres)")
        vetos = sorted({c["regla"] for c in cf["controles"] if c["resultado"] == "VETA"})
        no = [v for v in vetos if v not in VETOS_ANULABLES]
        if not vetos or no:
            return None, None, _no("O-34", f"veto no anulable ({', '.join(no) or 'sin veto'}): solo se anulan {', '.join(VETOS_ANULABLES)}")
        if self.anulaciones_mes(a.isoformat()) >= self.cfg["anulaciones_veto_mes"]:
            return None, None, _no("O-34", f"límite mensual de anulaciones de veto agotado ({self.cfg['anulaciones_veto_mes']})")
        topes = [c["limite"] for c in cf["controles"] if c["regla"] in TOPES_F]
        q = cf["entradas"]["solicitud"]["cantidad"]
        if len(topes) != len(TOPES_F) or not all(_num(t) for t in topes + [q]):
            return None, None, _no("O-34", "el informe de F no trae sus topes de cantidad: no hay con qué acotar la anulación")
        q = math.floor(min([q] + topes) * 1e6) / 1e6
        if q <= 0:
            return None, None, _no("O-34", "los topes de F no dejan cantidad que autorizar")
        return q, vetos, None

    def _config_rota(self):
        """T-51 (H5): una configuración alterada en caliente (mandatos incluidos) detiene la operación y activa el kill-switch."""
        if self.config_integra():
            return None
        self._activar_kill("configuración alterada en caliente", "ORQUESTADOR", self.ultimo_ahora or "1970-01-01T00:00:00+00:00")
        return _no("O-13", "la configuración (o un mandato de SC-1) no es la de su huella: no se sigue")

    def _mandato_efectivo(self, e):
        """El mandato de SC-1 de la cartera del expediente, estrechado por las restricciones de su encargo vigente."""
        en = self.encargos.get(e.get("encargo_actual")) or {}
        return sc1.efectivo(self.cfg["mandatos"][e["cartera_destino"]], ((en.get("msg") or {}).get("payload") or {}).get("restricciones"))

    def mandato(self, cartera):
        """SC-1 (T-51): el mandato vigente de una cartera y la referencia (versión y huella) que debe citar el encargo."""
        m = self.cfg["mandatos"].get(cartera) if isinstance(cartera, str) else None
        if m is None:
            return None
        return {"cartera": cartera, "version_sc1": sc1.VERSION_SC1, "mandato": copy.deepcopy(m), "referencia": sc1.referencia(m)}

    def configuracion(self):
        """La configuración en vigor y su huella (la misma que llevan las anotaciones)."""
        return {"huella": self.huella_config, "integra": self.config_integra(), **copy.deepcopy(self._configuracion_completa())}

    def _anota(self, ent, desde, hasta, actor, ahora, motivo, ref=None, datos=None):
        prev = ent["historial"][-1]["hash"] if ent["historial"] else "0" * 64
        h = {"n": len(ent["historial"]), "desde": desde, "hasta": hasta, "actor": actor, "ahora": ahora,
             "motivo": motivo, "ref": ref, "datos": datos, "version_reglas": VERSION_REGLAS, "config": self.huella_config, "hash_prev": prev}
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
                "sellos": copy.deepcopy(self.sellos), "calendario": self.cal_def, "mandatos": copy.deepcopy(self.cfg["mandatos"])}

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
        adv = self.advertencias_k(sid)
        if adv:   # T-26 (hallazgo 13): las advertencias de K llegan al Orquestador y al operador
            self._aviso("O-36", f"sello {sid} con advertencias de K: " + "; ".join(f"{x['regla']} {x.get('detalle', '')}"[:120] for x in adv), ahora, sid)
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

    def _advertencias_de(self, e):
        """Las advertencias de K del sello con el que se analizó el expediente (encargo vigente)."""
        en = self.encargos.get(e.get("encargo_actual")) or {}
        return self.advertencias_k(en.get("sello_ref"))

    def _contraste_tipos_k(self, tipos):
        """T-42: cada tipo de cambio de G (EUR por unidad de divisa) frente al último cierre de K. Para cada divisa se busca,
        del más reciente al más antiguo (por fecha de corte y emisión, como instantes), el primer sello aún vigente (estado_sello)
        con una fuente DISPONIBLE de su par con el euro (en cualquier grafía: par_divisas). Una desviación mayor que la tolerancia,
        o una cuenta no finita, es discrepancia. Sin sello que cubra la divisa no hay contraste (quedan los rangos de referencia)."""
        hoy = (self.ultimo_ahora and _dt(self.ultimo_ahora) or datetime.now(timezone.utc)).astimezone(timezone.utc).date().isoformat()
        vig = []
        for x in self.sellos.values():
            try:
                if x.get("estado") == "VIGENTE" and estado_sello(x, hoy, x["cartera"], self.cal_def) == "VIGENTE":
                    vig.append(x)
            except (KeyError, TypeError, ValueError):
                continue
        vig.sort(key=lambda x: (x["fecha_corte"], _dt(x["emitido_en"]), x["sello_id"]), reverse=True)
        tol = self.cfg["tolerancia_tipo_k_rel"]
        out = []
        for div, v in sorted(tipos.items()):
            for s_ in vig:
                refs = []
                for fu in s_.get("fuentes", []):
                    ins, ci = fu.get("instrumento"), fu.get("ultimo_cierre")
                    par = par_divisas(ins) if isinstance(ins, str) else None
                    if fu.get("estado") != "DISPONIBLE" or not par or not _num(ci) or ci <= 0:
                        continue
                    if par == ("EUR", div):
                        refs.append((ins, abs(v * ci - 1)))   # EUR por divisa = 1/cierre: v / (1/ci) - 1
                    elif par == (div, "EUR"):
                        refs.append((ins, abs(v / ci - 1)))
                if not refs:
                    continue
                for ins, dev in refs:
                    if not math.isfinite(dev) or dev > tol:
                        out.append(f"{div} {v}: desviación {dev:.2%} del último cierre de K ({ins}, sello {s_['sello_id']}, tolerancia {tol:.0%})"
                                   if math.isfinite(dev) else f"{div} {v}: no se puede contrastar con K ({ins}, sello {s_['sello_id']})")
                break
        return out

    def advertencias_k(self, sello_id):
        """T-26 (hallazgo 13): las reglas de K que no dieron OK en ese sello (p. ej. Q-10, dato crítico de una sola fuente)."""
        s = self.sellos.get(sello_id) if isinstance(sello_id, str) else None
        return [copy.deepcopy(x) for x in (s or {}).get("resultado_reglas", []) if isinstance(x, dict) and x.get("resultado") != "OK"]

    # ------------------------------------------------------------ T-26: Motor numérico SC-3
    @_seguro
    def registrar_modelo(self, modelo, actor, ahora):
        """Un módulo del Motor declara su modelo y sus límites de validez (una entrada por modelo y versión)."""
        self._ahora(ahora)
        if actor != "MOTOR":
            return _no("O-05", "solo el Motor (SC-3) declara modelos")
        mal = sc3.modelo_fallo(modelo)
        if mal:
            return _no("O-01", f"modelo no válido: {mal}")
        k = f"{modelo['modelo_ref']}@{modelo['version']}"
        if k in self.modelos:
            if self.modelos[k]["hash"] == sc3.huella(modelo):
                return _r(True, "O-02", "modelo ya declarado", duplicado=True)
            return _no("O-03", "mismo modelo y versión con otra declaración")
        self.modelos[k] = {"modelo": copy.deepcopy(modelo), "hash": sc3.huella(modelo), "ahora": ahora}
        self._anota_sc3({"tipo": "MODELO", "clave": k, "hash": sc3.huella(modelo)}, ahora)
        return _r(True, "OK", "modelo declarado")

    @_seguro
    def registrar_artefacto(self, artefacto, actor, ahora):
        """El Motor registra un cálculo reproducible: modelo declarado, sello de K (fecha de corte), semilla y hashes."""
        self._ahora(ahora)
        if actor != "MOTOR":
            return _no("O-05", "solo el Motor (SC-3) registra artefactos")
        mal = sc3.artefacto_fallo(artefacto)
        if mal:
            return _no("O-01", f"artefacto no válido: {mal}")
        aid = artefacto["artefacto_id"]
        if aid in self.artefactos:
            if self.artefactos[aid]["hash"] == sc3.huella(artefacto):
                return _r(True, "O-02", "artefacto ya registrado", duplicado=True)
            return _no("O-03", "mismo artefacto_id con otro contenido")
        mod = self.modelos.get(f"{artefacto['modelo_ref']}@{artefacto['version_modelo']}")
        if mod is None or mod["hash"] != sc3.huella(mod["modelo"]):
            return _no("O-12", "el artefacto es de un modelo no declarado (o alterado) en el Motor")
        sel = self.sellos.get(artefacto["sello_ref"])
        if sel is None or sel["estado"] != "VIGENTE":
            return _no("O-12", "el artefacto cita un sello de K no registrado o no vigente")
        self.artefactos[aid] = {"artefacto": copy.deepcopy(artefacto), "hash": sc3.huella(artefacto),
                                "fecha_corte": sel["fecha_corte"], "ahora": ahora}
        self._anota_sc3({"tipo": "ARTEFACTO", "clave": aid, "hash": sc3.huella(artefacto), "fecha_corte": sel["fecha_corte"]}, ahora)
        return _r(True, "OK", "artefacto registrado")

    def _anota_sc3(self, entrada, ahora):
        L = self.sc3
        L["entradas"].append(entrada)
        self._anota(L, "VIGENTE" if L["historial"] else None, "VIGENTE", "MOTOR", ahora, f"{entrada['tipo']} {entrada['clave']}",
                    entrada["tipo"], datos=_hash(entrada))

    def motor_ok(self):
        """El registro SC-3 es íntegro: su cadena cuadra, los índices de modelos y artefactos son exactamente los de la cadena
        (nada borrado ni añadido por fuera, R-M1), ninguna entrada cambió y los artefactos que cita un sobre aceptado siguen ahí."""
        try:
            L = self.sc3
            if L == {"historial": [], "estado": "VIGENTE", "entradas": []} and not self.modelos and not self.artefactos:
                return True   # T-03 (revisión del diario, hallazgo 1): un Orquestador recién creado, sin nada registrado, es íntegro
            if not (self._historial_ok(L) and len(L["historial"]) == len(L["entradas"])
                    and all(h["datos"] == _hash(x) for h, x in zip(L["historial"], L["entradas"]))):
                return False
            mods = {x["clave"]: x for x in L["entradas"] if x["tipo"] == "MODELO"}
            arts = {x["clave"]: x for x in L["entradas"] if x["tipo"] == "ARTEFACTO"}
            if set(mods) != set(self.modelos) or set(arts) != set(self.artefactos):
                return False
            if not all(v["hash"] == sc3.huella(v["modelo"]) == mods[k]["hash"] for k, v in self.modelos.items()):
                return False
            for k, v in self.artefactos.items():
                a_ = v["artefacto"]
                if not (v["hash"] == sc3.huella(a_) == arts[k]["hash"] and v["fecha_corte"] == arts[k]["fecha_corte"]
                        and f"{a_['modelo_ref']}@{a_['version_modelo']}" in self.modelos
                        and self.sellos.get(a_["sello_ref"], {}).get("fecha_corte") == v["fecha_corte"]):
                    return False
            for e in self.expedientes.values():   # lo que un sobre aceptado cita sigue registrado
                for aid in (((e.get("sobre") or {}).get("documento") or {}).get("payload", {}).get("referencias") or {}).get("artefactos_motor") or []:
                    if aid not in self.artefactos:
                        return False
            return True
        except (KeyError, TypeError, AttributeError, ValueError):
            return False

    def sellos_ok(self):
        """T-26 (R-M2): cada sello guardado sigue teniendo el hash con el que K lo emitió (sus advertencias incluidas)."""
        try:
            return all(hash_del_sello(s_) == s_["hash_sello"] for s_ in self.sellos.values())
        except (KeyError, TypeError, AttributeError, ValueError):
            return False

    def _anota_sc5(self, entrada, ahora):
        """T-80: rastro de solo añadir de las consultas (y de los expedientes DIRECTA que salen de ellas), encadenado."""
        L = self.consultas
        L["entradas"].append(entrada)
        self._anota(L, "VIGENTE" if L["historial"] else None, "VIGENTE", "ORQUESTADOR", ahora,
                    f"{entrada['tipo']} {entrada['consulta_id']}", entrada["tipo"], datos=_hash(entrada))

    def consultas_ok(self):
        """T-80: el rastro SC-5 es íntegro: su cadena cuadra y ninguna entrada cambió (vacío, recién creado, también lo es)."""
        try:
            L = self.consultas
            if L == {"historial": [], "estado": "VIGENTE", "entradas": []}:
                return self._consultas_citadas_ok()
            if not (self._historial_ok(L) and len(L["historial"]) == len(L["entradas"])
                    and all(h["datos"] == _hash(x) for h, x in zip(L["historial"], L["entradas"]))):
                return False
            return self._consultas_citadas_ok()
        except (KeyError, TypeError, AttributeError, ValueError):
            return False

    def _consultas_citadas_ok(self):
        """QA de T-80, H-02: lo que los expedientes encadenan del rastro sigue en él. Todo expediente DIRECTA que sale de una consulta
        tiene en SC-5 esa consulta (con su análisis) y su APERTURA: vaciar o recortar el rastro por el final se ve si recorta algo
        citado. Lo que nadie cita solo lo protege el ancla externa de la cabeza SC5 (T-02)."""
        ent = self.consultas["entradas"]
        cons = {x["consulta_id"]: x for x in ent if x.get("tipo") == "CONSULTA"}
        aperturas = {(x["consulta_id"], x["expediente_id"]) for x in ent if x.get("tipo") == "APERTURA"}
        for k, e in self.expedientes.items():
            c = e.get("consulta_ref") if e.get("via_entrada") == "DIRECTA" else None
            if c is None:
                continue
            if c not in cons or (c, k) not in aperturas:
                return False
            if e.get("analisis_ref") is not None and e["analisis_ref"] not in cons[c]["consulta"]["analisis"]:
                return False
        return all(x["consulta_id"] in cons and (self.expedientes.get(x["expediente_id"]) or {}).get("consulta_ref") == x["consulta_id"]
                   for x in ent if x.get("tipo") == "APERTURA")

    def _consulta(self, consulta_id):
        L = self.consultas.get("entradas") if isinstance(self.consultas, dict) else None
        return next((x["consulta"] for x in L or [] if x.get("tipo") == "CONSULTA" and x["consulta"]["consulta_id"] == consulta_id), None)

    def _vista_sc3(self):
        return {k: {"modelo_ref": v["artefacto"]["modelo_ref"], "fecha_corte": v["fecha_corte"], "sello_ref": v["artefacto"]["sello_ref"]}
                for k, v in self.artefactos.items()}

    # ------------------------------------------------------------ expedientes
    @_seguro
    def detectar(self, expediente_id, correlation_id, via_entrada, cartera_destino, actor, ahora):
        self._ahora(ahora)
        if actor not in EMISORES:
            return _no("O-05", f"{actor!r} no puede abrir expedientes")
        if not (isinstance(expediente_id, str) and _ID.match(expediente_id) and isinstance(correlation_id, str) and _ID.match(correlation_id)):
            return _no("O-01", "identificadores inválidos")
        if via_entrada == "DIRECTA":   # T-80: la vía DIRECTA no nace DETECTADA, sino en el estado del bloque de entrada
            return _no("O-01", "la vía DIRECTA nace en el estado del bloque de entrada (C, D o E): ábrala con abrir_directa() (D-28)")
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

    # ------------------------------------------------------------ T-80: vía DIRECTA y modo CONSULTA (D-28)
    def _analisis_vigente(self, sid, a):
        """El expediente que validó el sobre sid (el registro de análisis son los sobres validados), si sigue vigente con su sello."""
        if not (isinstance(sid, str) and _ID.match(sid)):
            return None, _no("O-01", "análisis: se espera el event_id de un sobre validado")
        ev = self.eventos.get(sid)
        x = self.expedientes.get(ev.get("expediente_id")) if isinstance(ev, dict) else None
        if x is None or (x.get("sobre") or {}).get("event_id") != sid:
            return None, _no("O-12", f"{sid} no está en el registro de análisis (no es el sobre validado de ningún expediente)")
        if a > _dt(x["sobre"]["valid_until"]):
            return None, _no("O-10", f"el análisis {sid} ya no está vigente")
        if self._sello_anulado(x) or not self._sellos_validos(x):
            return None, _no("O-06", f"el sello de K del análisis {sid} ya no es válido")
        return x, None

    def _origen_reutilizable(self, sid, cartera, a):
        """El expediente de origen del análisis sid si se puede reutilizar en un expediente DIRECTA nuevo de la cartera. Ningún
        expediente que tenga ese sobre puede estar en juego, invertido o en reanálisis, ni apartado por alguien distinto del
        operador sin ratificar (T-36: no se vuelve a meter por la vía DIRECTA), ni con una exclusión dura (T-27)."""
        x, err = self._analisis_vigente(sid, a)
        if err:
            return None, err
        if x["cartera_destino"] != cartera:
            return None, _no("O-12", f"el análisis {sid} es de la cartera {x['cartera_destino']}, no de {cartera}")
        # QA de T-80, H-01: el encargo actual del origen tiene que ser aquel al que respondió el sobre (nivel, sello, mandato y
        # presupuesto salen de él). Si se volvió a encargar después de validarlo, el sobre ya no es el de su encargo: no se reutiliza
        h = x["historial"]
        iv = max((i for i, z in enumerate(h) if z["hasta"] == "VALIDADA" and z["desde"] != "VALIDADA"), default=None)
        if iv is None or any(z["hasta"] == "EN_ANALISIS" and z["motivo"] == "encargo emitido" for z in h[iv + 1:]):
            return None, _no("O-06", f"{x['expediente_id']} se volvió a encargar después de validar el análisis {sid}: ya no es el de su encargo")
        for k, y in sorted(self.expedientes.items()):
            if (y.get("sobre") or {}).get("event_id") != sid:
                continue
            if y["estado"] in VIVOS:
                return None, _no("O-06", f"el análisis {sid} ya está en juego en {k} ({y['estado']}): compárelo allí")
            if y["estado"] == "EJECUTADA":
                return None, _no("O-06", f"con el análisis {sid} ya se invirtió en {k}")
            # QA de T-80, H-09 y H-12: lo que caducó después de validarse no vuelve sin análisis nuevo (§4.1, regla 4), aunque
            # después se descarte
            iv_y = max((i for i, z in enumerate(y["historial"]) if z["hasta"] == "VALIDADA" and z["desde"] != "VALIDADA"), default=-1)
            if y["estado"] == "CADUCADA" or any(z["hasta"] == "CADUCADA" for z in y["historial"][iv_y + 1:]):
                return None, _no("O-06", f"{k}, que tiene el análisis {sid}, caducó: una propuesta caducada vuelve con un análisis nuevo (§4.1, regla 4)")
            if y["estado"] not in REUTILIZABLE_DESDE:
                return None, _no("O-06", f"{k}, que tiene el análisis {sid}, se está analizando de nuevo ({y['estado']})")
            if y.get("exclusion") is not None:
                return None, _no("O-06", f"{k}, que tiene el análisis {sid}, quedó excluido (BLOQUEADO)")
            s = self._salida_no_operador(y)
            if s:
                return None, _no("O-06", f"{s['actor']} apartó {k}, que tiene el análisis {sid}: el operador debe ratificarlo o reabrirlo (T-36)")
        if self.encargos[x["encargo_actual"]]["msg"]["payload"].get("mandato_ref") != sc1.referencia(self.cfg["mandatos"][cartera]):
            return None, _no("O-24", f"el análisis {sid} se encargó con otro mandato de SC-1: no vale para el vigente")
        return x, None

    def analisis_vigentes(self, ahora, cartera=None):
        """Registro de análisis vigentes (solo lee, no mueve el reloj): un sobre validado por fila, con su expediente de origen,
        quién más lo tiene y si se puede reutilizar en un expediente DIRECTA (y, si no, por qué). Ilegible: lista vacía."""
        try:
            a = _dt(ahora)
            out = []
            for sid in sorted({(x.get("sobre") or {}).get("event_id") for x in self.expedientes.values()} - {None}):
                x, err = self._analisis_vigente(sid, a)
                if err or (cartera is not None and x["cartera_destino"] != cartera):
                    continue
                _, no = self._origen_reutilizable(sid, x["cartera_destino"], a)
                ident = x["sobre"]["documento"]["payload"]["identificacion"]
                out.append({"analisis": sid, "expediente_id": x["expediente_id"], "cartera": x["cartera_destino"], "perfil": x["sobre"]["perfil"],
                            "instrumento": ident.get("instrumento"), "nivel": x["sobre"]["nivel"], "fecha_corte": x["sobre"]["fecha_corte"],
                            "valid_until": x["sobre"]["valid_until"],
                            "en": sorted(k for k, y in self.expedientes.items() if (y.get("sobre") or {}).get("event_id") == sid),
                            "reutilizable": no is None, "motivo": None if no is None else no["motivo"]})
            return out
        except Exception:   # noqa: BLE001 — una consulta de solo lectura no rompe nada: falla cerrado con la lista vacía
            return []

    @_seguro
    def abrir_directa(self, expediente_id, correlation_id, cartera_destino, bloque, actor, ahora, encargo=None, analisis=None,
                      motivo=None, consulta_id=None):
        """T-80 (D-28): el Broker abre un expediente con vía DIRECTA, que nace en el estado del bloque de entrada (§4.1, regla 6):
        - C: EN_ANALISIS, con un encargo CT-G-01 completo (si no, se rechaza: §2);
        - D: VALIDADA, reutilizando el análisis vigente `analisis` del registro; si no lo hay, con `encargo` se encarga a C un
          análisis de nivel bajo para lo que falta (nace EN_ANALISIS) y, sin él, se rechaza;
        - E: COMPARADA, con un candidato único (`analisis`) y el motivo de no comparar con más: el Orquestador registra la
          comparación frente al benchmark de la cartera (P5). Si hay otros candidatos vigentes en la cartera, se devuelve a D.
        F y G nunca son punto de entrada. El presupuesto por encargo y por día es el mismo. Con consulta_id, el expediente sale
        de esa consulta (sus análisis) y SC-5 lo anota."""
        a = self._ahora(ahora)
        if actor != "BROKER":
            return _no("O-05", f"{actor!r} no puede abrir expedientes por la vía DIRECTA: el Broker entra por C, D o E (§2)")
        if not (isinstance(expediente_id, str) and _ID.match(expediente_id) and isinstance(correlation_id, str) and _ID.match(correlation_id)):
            return _no("O-01", "identificadores inválidos")
        if cartera_destino not in GESTOR_DE:
            return _no("O-01", "cartera_destino inválida")
        if bloque in ("F", "G"):
            return _no("O-01", "F y G nunca son punto de entrada (§2): se entra por C, D o E")
        if bloque not in BLOQUES_DIRECTA:
            return _no("O-01", "bloque de entrada inválido: C, D o E")
        if expediente_id in self.expedientes:
            return _no("O-03", "expediente ya existe")
        if expediente_id in GESTOR_DE or expediente_id.startswith("POS-") or expediente_id in self.posiciones:
            return _no("O-01", "el identificador del expediente no puede ser el nombre de una cartera ni el de una posición")
        if bloque == "C" and (analisis is not None or motivo is not None):
            return _no("O-01", "por C no se reutiliza un análisis ni se da motivo: se encarga uno nuevo")
        if bloque == "E" and encargo is not None:
            return _no("O-01", "por E no se encarga nada: se entra con un análisis validado")
        if bloque in ("D", "E") and analisis is None and (bloque == "E" or encargo is None):
            return _no("O-06", f"entrar por {bloque} exige un análisis vigente del registro" + (" o un encargo de nivel bajo para C" if bloque == "D" else ""))
        if bloque == "D" and motivo is not None:
            return _no("O-01", "el motivo de no comparar es de la entrada por E")
        if bloque == "D" and analisis is not None and encargo is not None:   # QA de T-80, H-06: nada se ignora en silencio
            return _no("O-01", "por D se entra con un análisis vigente o, si no lo hay, con un encargo de nivel bajo: no con los dos")
        if bloque == "E" and not _motivo_ok(motivo):
            return _no("O-15", f"entrar por E con un candidato único exige el motivo de no comparar con más ({MOTIVO_MIN} a 500 caracteres)")
        err = self._config_rota()   # T-51 (H5)
        if err:
            return err
        rota = self._rota()   # como en comparar: con un registro alterado no se reutiliza nada
        if rota:
            self._activar_kill(f"integridad rota en {rota}", "ORQUESTADOR", self.ultimo_ahora or "1970-01-01T00:00:00+00:00")
            return _no("O-13", f"el registro {rota} no es íntegro: no se abre el expediente")
        cons = None
        if consulta_id is not None:
            cons = self._consulta(consulta_id) if isinstance(consulta_id, str) else None
            if cons is None:
                return _no("O-12", f"no hay ninguna consulta {consulta_id!r} en SC-5")
            if cons["cartera"] not in (None, cartera_destino):
                return _no("O-12", f"la consulta {consulta_id} es de la cartera {cons['cartera']}")
            if analisis is not None and analisis not in cons["analisis"]:
                return _no("O-12", f"el análisis {analisis} no es de la consulta {consulta_id}")
        origen, no = (None, None)
        if analisis is not None:
            origen, no = self._origen_reutilizable(analisis, cartera_destino, a)
            if no:
                return {**no, "encargar": NIVEL_BAJO} if bloque == "D" else no
        e = {"expediente_id": expediente_id, "correlation_id": correlation_id, "via_entrada": "DIRECTA", "cartera_destino": cartera_destino,
             "bloque_entrada": bloque, "analisis_ref": analisis if origen is not None else None, "consulta_ref": consulta_id,
             "estado": "DETECTADA", "historial": [], "encargo_actual": None, "sobre": None, "contradictor": None, "retenido": None,
             "sin_avance": 0, "propuesta": None, "posicion_id": None, "reapertura": None}   # el estado se fija al anotar el nacimiento
        if origen is None:   # C, o D sin análisis reutilizable: nace EN_ANALISIS con el encargo
            if bloque == "D":
                p = encargo.get("payload") if isinstance(encargo, dict) else None
                if not (isinstance(p, dict) and NIVEL_ORDEN.get(p.get("nivel_analisis"), 99) <= NIVEL_ORDEN[NIVEL_BAJO]):
                    return _no("O-06", f"lo que falta al entrar por D se encarga a C con un análisis de nivel bajo ({NIVEL_BAJO} o menos)")
            r = self._emitir(e, expediente_id, encargo, actor, ahora, a, nace=True)
            if not r["ok"] or r.get("duplicado"):
                return r if not r.get("duplicado") else _no("O-12", "ese encargo ya se usó")
        else:
            self._anota(e, None, "VALIDADA", actor, ahora, f"nace por {bloque} (vía DIRECTA)", origen["expediente_id"], datos=_hash(_identidad(e)))
            e["encargo_actual"] = origen["encargo_actual"]
            e["sobre"], e["contradictor"] = copy.deepcopy(origen["sobre"]), copy.deepcopy(origen.get("contradictor"))
            self._anota(e, "VALIDADA", "VALIDADA", "ORQUESTADOR", ahora, f"{MOTIVO_REUTILIZA} de {origen['expediente_id']}",
                        origen["encargo_actual"], datos=self._huella_sobre(e))
            self.expedientes[expediente_id] = e
            if cons is not None:   # antes de comparar: el rastro tiene que citar ya la apertura (consultas_ok, H-02)
                self._anota_sc5({"tipo": "APERTURA", "consulta_id": consulta_id, "expediente_id": expediente_id, "bloque": bloque}, ahora)
            if bloque == "E":
                r = self._comparar([expediente_id], "D", ahora, a, motivo_unico=motivo)
                if not r["ok"]:
                    del self.expedientes[expediente_id]
                    if cons is not None:   # la apertura no llegó a hacerse: se quita del rastro (nadie la ha visto)
                        self.consultas["historial"].pop()
                        self.consultas["entradas"].pop()
                    if r.get("faltan"):   # §2: «se devuelve a D»: hay más candidatos vigentes en la cartera y D compara con todos
                        return _no("O-22", f"hay otros candidatos vigentes en la cartera ({', '.join(r['faltan'][:5])}): se devuelve a D; "
                                           "entre por D y compare con todos", devolver_a="D", faltan=r["faltan"])
                    return r
        if cons is not None and origen is None:
            self._anota_sc5({"tipo": "APERTURA", "consulta_id": consulta_id, "expediente_id": expediente_id, "bloque": bloque}, ahora)
        extra = {k: v for k, v in (r.items() if bloque == "E" or origen is None else ()) if k not in ("ok", "codigo", "motivo")}
        return _r(True, "OK" if bloque != "E" else r["codigo"], f"expediente abierto por {bloque} (vía DIRECTA): nace {e['estado']}"
                  + (f"; {r['motivo']}" if bloque == "E" else ""), nace_en=e["estado"], reutiliza=origen["expediente_id"] if origen else None, **extra)

    @_seguro
    def consultar(self, consulta, actor, ahora):
        """T-80 (D-28): una consulta (comparar, analizar o proyectar sin intención de invertir) no abre expediente ni camino a una
        orden: queda en el rastro SC-5 con los análisis vigentes que cita. Una COMPARAR la hace D con esos análisis frente al
        benchmark de la cartera (fecha de corte común, regla 3) y su resultado queda en el rastro; no mueve ningún expediente.
        Si después se decide invertir, abrir_directa(..., consulta_id=) abre el expediente reutilizando sus análisis."""
        a = self._ahora(ahora)
        if actor != "BROKER":
            return _no("O-05", f"{actor!r} no hace consultas: las hace el Broker")
        if not (isinstance(consulta, dict) and set(consulta) == set(CAMPOS_CONSULTA)):
            return _no("O-01", f"consulta mal formada: campos {', '.join(CAMPOS_CONSULTA)}")
        c = consulta
        if not all(isinstance(c[k], str) and _ID.match(c[k]) for k in ("consulta_id", "correlation_id")):
            return _no("O-01", "identificadores de la consulta inválidos")
        err = self._config_rota()
        if err:
            return err
        rota = self._rota()   # QA de T-80, H-05: antes de leer el rastro
        if rota:
            self._activar_kill(f"integridad rota en {rota}", "ORQUESTADOR", self.ultimo_ahora or "1970-01-01T00:00:00+00:00")
            return _no("O-13", f"el registro {rota} no es íntegro: no se consulta")
        previa = self._consulta(c["consulta_id"])
        if previa is not None:
            if _hash(previa) == _hash(c):
                return _r(True, "O-02", "consulta ya registrada: se ignora", duplicado=True)
            return _no("O-03", "ese consulta_id ya se usó con otro contenido")
        if c["tipo"] not in TIPOS_CONSULTA or c["bloque"] not in BLOQUES_CONSULTA:
            return _no("O-01", f"tipo ({', '.join(TIPOS_CONSULTA)}) o bloque ({', '.join(BLOQUES_CONSULTA)}; nunca F ni G) inválidos")
        if c["cartera"] is not None and c["cartera"] not in GESTOR_DE:
            return _no("O-01", "cartera inválida")
        an = c["analisis"]
        if not (isinstance(an, list) and len(an) <= PARAMETROS["o_max_analisis_consulta"] and all(isinstance(x, str) for x in an) and len(set(an)) == len(an)):
            return _no("O-01", f"analisis: lista de event_id de sobres, sin repetidos y como mucho {PARAMETROS['o_max_analisis_consulta']}")
        if not _motivo_ok(c["pregunta"]):
            return _no("O-15", f"una consulta exige su pregunta ({MOTIVO_MIN} a 500 caracteres)")
        if c["tipo"] == "COMPARAR" and (c["bloque"] != "D" or c["cartera"] is None or not an):
            return _no("O-01", "comparar es de D: con la cartera (su benchmark) y al menos un análisis")
        xs = []
        for sid in an:
            x, err = self._analisis_vigente(sid, a)
            if err:
                return err
            if c["cartera"] is not None and x["cartera_destino"] != c["cartera"]:
                return _no("O-12", f"el análisis {sid} es de la cartera {x['cartera_destino']}, no de {c['cartera']}")
            xs.append(x)
        resultado = None
        if c["tipo"] == "COMPARAR":
            dif, _ = self._dif_cortes(xs)
            if dif > self.cfg["umbral_corte_comun_dias_habiles"]:
                return _no("O-11", f"fechas de corte distintas ({dif} d.h.): hay que actualizar datos")
            d = comparar_candidatos([self._candidato_d(x, sid) for sid, x in zip(an, xs)],
                                    ahora, self.cfg["referencias"][c["cartera"]])
            if not d["ok"]:
                return _no("O-01", f"D no pudo comparar: {d['motivo']}")
            resultado = {"codigo_d": d["codigo"], "decision_global": d["decision_global"], "referencia": d["referencia"],
                         "ganador": d["ganador_global"], "aspirantes": sorted(d.get("aspirantes") or []),
                         "excluidos": {x["expediente_id"]: x["motivo"] for x in d.get("excluidos", [])}}
        self._anota_sc5({"tipo": "CONSULTA", "consulta_id": c["consulta_id"], "consulta": copy.deepcopy(c), "actor": actor, "resultado": resultado}, ahora)
        return _r(True, "OK", "consulta registrada en SC-5: no abre expediente", consulta_id=c["consulta_id"], resultado=copy.deepcopy(resultado))

    @_seguro
    def emitir_encargo(self, expediente_id, encargo, actor, ahora):
        a = self._ahora(ahora)
        e, err = self._exp(expediente_id)
        if err:
            return err
        return self._emitir(e, expediente_id, encargo, actor, ahora, a)

    def _emitir(self, e, expediente_id, encargo, actor, ahora, a, nace=False):
        """El encargo a C de un expediente que existe o, con nace (T-80, vía DIRECTA por C), del que nace con él: entonces
        el expediente solo se guarda si el encargo se acepta, y nace EN_ANALISIS (su primera anotación lleva la identidad)."""
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
        pendiente = None
        if e["estado"] == "EN_OBSERVACION":   # T-46: solo con la condición cumplida (o el operador), dentro de plazo y del límite
            r = e["reapertura"]
            if a.astimezone(timezone.utc).date() > date.fromisoformat(r["vence"]):
                return _no("O-10", f"la observación venció el {r['vence']}")
            pendiente = None if r["cumplida"] is not None else self._primera_cumplida(e, None, a)   # fecha o datos nuevos: aquí mismo,
            if r["cumplida"] is None and pendiente is None:                                       # pero se anota solo si el encargo se acepta
                return _no("O-06", "no se ha cumplido ninguna condición de reapertura: el operador puede reabrir con motivo")
            hechas = self._reaperturas_hechas(e)
            if hechas >= self.cfg["max_reaperturas"] and (r["cumplida"] or {}).get("por") != "OPERADOR":
                return _no("O-06", f"el expediente ya se reabrió {hechas} veces: solo el operador puede reabrirlo otra vez")
        if encargo.get("expediente_id") != expediente_id or encargo.get("correlation_id") != e["correlation_id"]:
            return _no("O-12", "el encargo no pertenece a este expediente o petición")
        if actor != "BROKER" and encargo.get("producer") != actor:
            return _no("O-05", "el emisor del encargo no es quien lo pide")
        if encargo["payload"].get("cartera_destino") != e["cartera_destino"] if isinstance(encargo.get("payload"), dict) else True:
            return _no("O-12", "la cartera del encargo no es la del expediente")
        err = self._config_rota()   # T-51 (H5): con la configuración alterada no se encarga nada
        if err:
            return err
        if encargo["payload"].get("mandato_ref") != sc1.referencia(self.cfg["mandatos"][e["cartera_destino"]]):   # T-51
            return _no("O-24", "el encargo no cita el mandato vigente de SC-1 para la cartera (versión y huella): pídalo con mandato()")
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
        if e["estado"] == "EN_OBSERVACION":
            if pendiente is not None:   # la condición que se cumplió al reabrir queda anotada antes del encargo
                self._marcar_cumplida(expediente_id, e, pendiente, "ORQUESTADOR", ahora)
            if previo and previo["estado"] == "EN_CURSO":   # el encargo que quedó en curso al observar ya no se espera
                previo["estado"] = "ANULADO"
            e["propuesta"], e["comparacion"] = None, None   # un análisis nuevo: la propuesta y la comparación anteriores ya no valen
        e["encargo_actual"] = eid
        e["sin_avance"] += 1
        if nace:
            self._anota(e, None, "EN_ANALISIS", actor, ahora, "encargo emitido", eid, datos=_hash(_identidad(e)))
            self.expedientes[expediente_id] = e
        else:
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
        g0 = self.gasto_dia.get(str(a.astimezone(timezone.utc).date()), {"coste": 0.0, "tiempo": 0.0})
        if not all(math.isfinite(x) for x in (en["coste"] + coste_eur, en["tiempo"] + tiempo_min, g0["coste"] + coste_eur, g0["tiempo"] + tiempo_min)):
            return _no("O-01", "el gasto acumulado dejaría de ser un número finito")   # V0.44 (revisión, hallazgo 8)
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
        err = self._config_rota()   # T-51 (H5)
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
        rota = "MOTOR" if not self.motor_ok() else ("SELLOS" if not self.sellos_ok() else None)
        if rota:   # T-26 (R-M3): como en el resto de puntos de decisión, kill-switch
            self._activar_kill(f"integridad rota en {rota}", "ORQUESTADOR", self.ultimo_ahora or "1970-01-01T00:00:00+00:00")
            return _no("O-13", f"el registro {rota} está alterado: no se aceptan sobres")
        ctx_enc = self._ctx_encargo(en["ahora_emision"], en["fecha_vigente_emision"])
        ctx_sob = {"ahora": ahora, "fecha_corte_encargo": en["fecha_corte"], "perfiles_activos": self.cfg["perfiles_activos"],
                   "clases_ratificadas": self.cfg["clases_ratificadas"], "apalancamiento_permitido": self.cfg["apalancamiento_permitido"],
                   "sc3": self._vista_sc3(), "sello_encargo": en["sello_ref"]}   # T-26: V-26, las cifras citan artefactos del Motor
        # el sobre se valida con su propio reloj; el encargo, con el de su emisión
        fallos = sobre_responde_a_encargo(en["msg"], sobre, ctx_enc, ctx_sob)
        if fallos:
            return _no("O-01", f"el sobre no responde al encargo: {fallos[0]['regla']}: {fallos[0]['mensaje'][:80]}", reglas=sorted({x['regla'] for x in fallos}))
        bl = bloqueos(sobre)
        if bl:   # T-27: un candidato bloqueado se informa, no compite: no pasa por VALIDADA (ni compite ni queda de testigo)
            self.eventos[sid] = {"hash": h, "expediente_id": expediente_id}
            en["estado"] = "ENTREGADO"
            e["exclusion"] = {"event_id": sid, "hash": h, "bloqueos": bl}
            e["sin_avance"] = 0
            # transición interna del Orquestador (no está en T: nadie más puede pedirla)
            self._anota(e, e["estado"], "DESCARTADA", "ORQUESTADOR", ahora, _motivo_bloqueo(bl), sid, datos=h)
            self._aviso("O-32", f"{expediente_id}: candidato descartado por exclusión dura BLOQUEADO ({', '.join(bl)})", ahora, expediente_id,
                        carteras={e["cartera_destino"]})
            return _r(True, "O-32", f"sobre recibido como informe: exclusión dura BLOQUEADO ({', '.join(bl)}); expediente descartado")
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
            autoria_c = self.cfg["autoria_c"].get(sobre["payload"]["identificacion"]["perfil"])
            fallos = validar_informe(informe, {"ahora": ahora, "sobre": sobre, "autoria_c": autoria_c,
                                               "autoria_contradictor": self.cfg["autoria_contradictor"]})
            if fallos:
                return _no("O-01", f"informe del Contradictor no válido: {fallos[0]['regla']}: {fallos[0]['mensaje'][:80]}", reglas=sorted({x['regla'] for x in fallos}))
            div_c = self.divisa(sobre["payload"]["identificacion"]["instrumento"])
            for x in informe["payload"]["escenarios_fallo"]:   # T-49: H tiene que poder evaluar cada disparador (revisión, R-03)
                mal = senal_mal_formada(x["disparador"]["metrica"], x["disparador"]["unidad"], div_c)
                if mal:
                    return _no("O-01", f"informe del Contradictor: el escenario {x['id']} no se puede vigilar: {mal}")
            self.eventos[informe["event_id"]] = {"hash": ih, "expediente_id": expediente_id}
            contr = {"event_id": informe["event_id"], "veredicto": informe["payload"]["veredicto"], "hash": ih,
                     "valid_until": informe["valid_until"]}
            div = diversidad(informe["payload"]["autoria"], autoria_c) or informe["payload"]["autoria"]["diversidad"]
            contr["autoria"] = copy.deepcopy(informe["payload"]["autoria"])   # entra en la huella del sobre: queda auditado
            contr["escenarios_fallo"] = copy.deepcopy(informe["payload"]["escenarios_fallo"])   # T-49: viajan a la posición para que H los vigile
            contr["diversidad"] = div if autoria_c is not None else "NO_COMPROBABLE"
            if autoria_c is None or div == "MISMO_MODELO":   # T-48: sin diversidad de modelo, o sin poder comprobarla, el operador lo sabe
                self._aviso("O-33", f"{expediente_id}: " + ("el Contradictor es del mismo modelo que C" if autoria_c is not None and div == "MISMO_MODELO"
                                                            else "no se puede comprobar la diversidad del Contradictor: falta la autoría de C en la configuración"),
                            ahora, expediente_id, carteras={e["cartera_destino"]})
        self.eventos[sid] = {"hash": h, "expediente_id": expediente_id}
        en["estado"] = "ENTREGADO"
        ident = sobre["payload"]["identificacion"]
        info = {"event_id": sid, "fecha_corte": ident["fecha_corte"], "valid_until": sobre["valid_until"],
                "perfil": ident["perfil"], "nivel": ident["nivel_analisis"], "contradictor_ref": contr["event_id"] if contr else None,
                "hash": h, "documento": copy.deepcopy(sobre)}   # el sobre entero: D y la propuesta se contrastan con él
        if contr:   # el sobre vale solo mientras valga el informe del Contradictor
            info["valid_until"] = min(info["valid_until"], contr["valid_until"], key=_dt)
        # T-27: y solo mientras se pueda entrar como se analizó (después no hay propuesta posible: no compite ni es testigo)
        info["valid_until"] = min(info["valid_until"], sobre["payload"]["entrada_salida"]["entrada"]["ventana_hasta"], key=_dt) \
            if "entrada_salida" in sobre["payload"] else info["valid_until"]
        if contr and contr["veredicto"] == "OBJECION_CRITICA":
            e["retenido"] = {"sobre": info, "contradictor": contr}
            self._anota(e, e["estado"], "EN_ANALISIS", "ORQUESTADOR", ahora, "sobre retenido por objeción crítica del Contradictor", sid)
            self._aviso("O-17", f"{expediente_id}: objeción crítica del Contradictor; solo el operador puede levantarla", ahora, expediente_id)
            return _no("O-17", "objeción crítica: el expediente queda detenido hasta que el operador la levante o lo descarte")
        if contr and contr["veredicto"] == "OBJECION_MAYOR":
            self._aviso("O-17", f"{expediente_id}: objeción mayor del Contradictor", ahora, expediente_id)
        e["sobre"], e["contradictor"] = info, contr
        e["sin_avance"] = 0
        sin_contr = contr is None and en["nivel"] in NIVELES_CONTRADICTOR
        # T-48 (revisión): apartarse del valor por defecto exige motivo en la configuración y queda en el historial de cada expediente
        self._anota(e, e["estado"], "VALIDADA", "C", ahora,
                    "sobre aceptado" + (f" sin Contradictor (desactivado: {self.cfg['contradictor_desactivado_motivo']})" if sin_contr else ""),
                    sid, datos=self._huella_sobre(e))
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
            elif a["actor"] == "OPERADOR" and (a["ref"] == "RATIFICA_APARTADO" or (a["hasta"] in ("EN_OBSERVACION", "DESCARTADA") and a["desde"] != a["hasta"])):
                return None   # el operador lo hizo suyo
            elif _es_bloqueo(a):
                return None   # T-27: su análisis nuevo lo bloqueó (exclusión dura): ya no es un candidato que pudiera ganar
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
        self._anota(e, e["estado"], e["estado"], "OPERADOR", ahora, f"apartado ratificado: {motivo.strip()[:160]}", "RATIFICA_APARTADO",
                    datos=_hash(e["reapertura"]) if e["estado"] == "EN_OBSERVACION" else None)
        return _r(True, "OK", "apartado ratificado")

    @_seguro
    def comparar(self, expediente_ids, actor, ahora):
        a = self._ahora(ahora)
        return self._comparar(expediente_ids, actor, ahora, a)

    def _dif_cortes(self, exps):
        """Días hábiles entre la fecha de corte más vieja y la más nueva de unos expedientes, en los mercados de sus sellos."""
        cortes = sorted(date.fromisoformat(x["sobre"]["fecha_corte"]) for x in exps)
        cal = Calendario(self.cal_def)
        dif = max(cal.dias_habiles(m["mercado"], cortes[0], cortes[-1])
                  for x in exps for m in self.sellos[self.encargos[x["encargo_actual"]]["sello_ref"]]["mercados"])
        return dif, cortes

    @staticmethod
    def _candidato_d(x, cid=None):
        """Lo que D recibe de un candidato: su id (el del expediente, o cid) y una copia de su sobre a nombre de ese id. D comprueba
        que el sobre sea del candidato; un expediente DIRECTA que reutiliza el análisis de otro (T-80) lo lleva con el id del
        expediente que lo validó, y la reutilización ya la comprobó y encadenó el Orquestador."""
        doc = copy.deepcopy(x["sobre"]["documento"])
        cid = x["expediente_id"] if cid is None else cid
        if (x.get("via_entrada") == "DIRECTA" and x.get("analisis_ref") is not None) or cid != x["expediente_id"]:
            doc["expediente_id"] = cid
        return {"expediente_id": cid, "sobre": doc}

    def _comparar(self, expediente_ids, actor, ahora, a, motivo_unico=None):
        """La comparación de D. Con motivo_unico (T-80, vía DIRECTA por E con un candidato único), la comparación es la que hay
        frente al benchmark de la cartera (P5) y lleva el motivo de no comparar con más (§4.1, regla 6)."""
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
        err = self._config_rota()   # T-51 (H5): antes que O-24, una configuración alterada es un incidente
        if err:
            return err
        vigente = sc1.referencia(self.cfg["mandatos"][cartera])   # T-51: D mide contra el benchmark del mandato vigente de SC-1
        otra = [x["expediente_id"] for x in exps if self.encargos[x["encargo_actual"]]["msg"]["payload"].get("mandato_ref") != vigente]
        if otra:
            return _no("O-24", f"el encargo no cita el mandato vigente de SC-1 para la cartera: {', '.join(otra)}")
        dif, cortes = self._dif_cortes(exps)
        if dif > self.cfg["umbral_corte_comun_dias_habiles"]:
            viejos = [x["expediente_id"] for x in exps if date.fromisoformat(x["sobre"]["fecha_corte"]) == cortes[0]]
            return _no("O-11", f"fechas de corte distintas ({dif} d.h.): hay que actualizar datos", actualizar=viejos)
        if any(_hash(x["sobre"]["documento"]) != x["sobre"]["hash"] for x in exps):
            return _no("O-13", "un sobre guardado no cuadra con su hash")
        d = comparar_candidatos([self._candidato_d(x) for x in exps], ahora, ref)
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
            t = comparar_candidatos([self._candidato_d(x) for x in exps + testigos],
                                    ahora, ref)
            tids = {x["expediente_id"] for x in testigos}
            if not t["ok"]:
                return _no("O-01", f"D no pudo comparar con los candidatos apartados: {t['motivo']}")
            mejores = [t["ganador_global"]] if t["ganador_global"] else t["aspirantes"]
            apartado_mejor = next((x for x in mejores if x in tids), None)
        elif testigos and d["decision_global"] == "ABSTENERSE":
            t = comparar_candidatos([self._candidato_d(x) for x in testigos], ahora, ref)
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
                                                                   "confianza_normalizada", "factor_evidencia", "dominado_por",
                                                                   # T-17: lo que D verificó y cambió respecto a lo declarado
                                                                   "riesgo_pct", "exceso_anual_pct", "riesgo_anual_pct",
                                                                   "coste_descontado_pct", "confianza_verificada", "ajustes")} if fila else None}
            if motivo_unico is not None:
                e["comparacion"]["motivo_no_comparar"] = motivo_unico.strip()
            self._anota(e, e["estado"], "COMPARADA", actor, ahora,
                        "comparada con " + ",".join(expediente_ids) if motivo_unico is None
                        else "candidato único comparado con el benchmark de la cartera (vía DIRECTA por E)", cid, datos=_hash(e["comparacion"]))
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
        dec = ((self.encargos.get(e.get("encargo_actual")) or {}).get("msg") or {}).get("payload", {}).get("decision_informada")
        if dec not in ("ABRIR_POSICION", "AUMENTAR"):   # T-26 (revisión): un encargo EXPLORAR o DESCARTAR no lleva a una orden
            return _no("O-06", f"el encargo informa la decisión {dec!r}: no se propone una entrada con él")
        ap_m = self._mandato_efectivo(e)["apalancamiento_max"]
        if ce["apalancamiento"] > ap_m:   # T-51 (H3): el mandato de SC-1 manda, diga lo que diga el sobre
            return _no("O-06", f"el apalancamiento supera el máximo del mandato de la cartera ({ap_m})")
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
        if not all(isinstance(c.get(k, ""), str) for c in conds for k in ("descripcion", "unidad")):   # T-49 (revisión, R-05)
            return _no("O-01", "condiciones_salida: la descripción y la unidad de una condición son texto")
        for c_ in conds:   # T-49: H tiene que poder evaluar cada invalidez (revisión, R-03)
            mal = c_["tipo"] == "INVALIDEZ" and senal_mal_formada(c_["metrica"], c_.get("unidad"), self.divisa(ce["instrumento"]))
            if mal:
                return _no("O-21", f"condiciones_salida: la invalidez {c_['id']} no se puede vigilar: {mal}")
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
        sl = es["entrada"]["limite"]["valor"]   # T-27: la entrada del sobre es numérica (V-24)
        if not _num(sl):
            return _no("O-21", "el sobre no da un límite de entrada numérico: no hay con qué ligar la propuesta")
        if lim > sl if largo else lim < sl:
            return _no("O-21", f"el límite de entrada es peor que el analizado ({sl}): no se compra más caro ni se vende más barato")
        if _dt(ce["ventana_hasta"]) > _dt(es["entrada"]["ventana_hasta"]):
            return _no("O-21", "la ventana de entrada pasa de la analizada en el sobre")
        sv = es["stop"]["valor"]
        if not (_num(sv) and isinstance(es["stop"].get("unidad"), str) and re.fullmatch(r"[A-Z]{3}", es["stop"]["unidad"])):
            return _no("O-21", "el sobre no da un stop de precio (valor numérico en una divisa): no hay con qué ligar la propuesta")
        div = self.divisa(ce["instrumento"])   # T-27: los precios del sobre y de la propuesta van en la divisa de cotización
        if es["stop"]["unidad"] != div or es["entrada"]["limite"]["unidad"] != div or (_num(es["objetivo"]["valor"]) and es["objetivo"]["unidad"] != div):
            return _no("O-21", f"los precios del sobre (stop, límite, objetivo) no están en la divisa de cotización del instrumento ({div})")
        if any(x.get("metrica") == "precio" and x.get("tipo") in ("STOP", "OBJETIVO") and x.get("unidad") != div for x in cs["condiciones"]):
            return _no("O-21", f"el stop y el objetivo de la propuesta van en la divisa de cotización ({div})")
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
        # T-51 (H2): el tamaño máximo del mandato de SC-1 (estrechado por el encargo) también limita, además de la política de F
        tam = self._mandato_efectivo(e)["tamano_max_pct_cartera"]
        fx = tipo_cambio(self.divisa(ce["instrumento"]), dim["cartera"])
        if not (_num(fx) and fx > 0) or ce["cantidad"] * ce["limite"] * fx > tam / 100 * dim["cartera"]["capital_eur"] * (1 + 1e-9):
            return None, _no("O-23", f"la propuesta pasa del tamaño máximo del mandato ({tam} % de la cartera)")
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
        if actor == "MATRIZ_AUTONOMIA" and self._advertencias_de(e):   # T-26 (hallazgo 13): con advertencias de K decide el operador
            return _no("O-36", "el análisis usa un sello de K con advertencias (p. ej. dato de una sola fuente): autoriza el operador")
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
                                               "compromisos": self._compromisos(expediente_id, e["cartera_destino"]),
                                               "contexto": self._contexto_de_informe(expediente_id, control_f)})
        if fallos:
            return _no("O-01", f"informe de F no válido: {fallos[0]['regla']}: {fallos[0]['mensaje'][:80]}", reglas=sorted({x['regla'] for x in fallos}))
        cf = aplanar_informe(control_f)   # T-47: CT-G-08 0.2.0 llega envuelto; dentro se usa la forma plana
        em = _dt(cf["emitido_en"])   # T-22 (revisión H2): F debe haber visto todo lo autorizado antes, y el día del informe es el de autorizar
        if em.astimezone(timezone.utc).date() != a.astimezone(timezone.utc).date():
            return _no("O-10", "el informe de F es de otro día (UTC): el importe del día no sería el suyo; pide otro informe")
        posterior = next((k for k, x in self.expedientes.items() if k != expediente_id for h in x["historial"]
                          if h["hasta"] == "AUTORIZADA" and h["desde"] != "AUTORIZADA" and em < _dt(h["ahora"]) <= a), None)
        if posterior:
            return _no("O-10", f"después de emitirse el informe de F se autorizó {posterior}: F no lo contó; pide otro informe")
        libre_post = next((x for x in self.libres if em < _dt(x["registrado_en"]) <= a), None)   # T-33: la LIBRE declarada en la ventana informe→autorizar tampoco la vio F (F-14)
        if libre_post:
            return _no("O-10", f"después de emitirse el informe de F se declaró la LIBRE {libre_post['event_id']}: F no la contó; pide otro informe")
        err = self._foto_de_g(cf["entradas"]["cartera"], e["propuesta"]["entrada"]["instrumento"], e["propuesta"]["entrada"]["limite"])
        if err:
            return err
        cap_e = (e["propuesta"].get("dimensionado") or {}).get("cartera", {}).get("capital_eur")
        if cap_e != cf["entradas"]["cartera"].get("capital_eur"):
            return _no("O-23", "F controló con un capital distinto del que usó E para dimensionar")
        return None

    @_seguro
    def pantalla_aprobacion(self, expediente_id, control_f, ahora, actor="OPERADOR", anular_veto=None):
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
        cf = aplanar_informe(control_f)   # el hash se toma del mensaje completo; las cifras, de su forma plana
        if control_f["event_id"] in self.eventos:
            self._duplicado(control_f["event_id"], _hash(control_f), expediente_id, ahora)
            return _no("O-03", "el informe de F ya se usó")
        anulacion = None
        if anular_veto is not None and cf["resultado"] != "VETADO":
            return _no("O-01", "no hay veto que anular: F no vetó la propuesta")
        if cf["resultado"] == "VETADO" and anular_veto is not None:   # T-50: el operador pide anular el veto, con motivo y límite mensual
            q, vetos, err = self._comprobar_anulacion(cf, anular_veto, a)
            if err:
                return err
            anulacion = {"motivo": anular_veto["motivo"], "vetos": vetos}
        elif cf["resultado"] == "VETADO":   # el veto queda registrado: ese informe no se puede volver a usar
            self.eventos[control_f["event_id"]] = {"hash": _hash(control_f), "expediente_id": expediente_id}
            return _no("O-06", "F vetó la propuesta: no hay nada que aprobar")
        else:
            q = cf["cantidad_aprobada"]
        en = e["propuesta"]["entrada"]
        st = [c for c in e["propuesta"]["salida"]["condiciones"] if c["tipo"] == "STOP"][0]
        fx = tipo_cambio(cf["entradas"]["solicitud"]["divisa_cotizacion"], cf["entradas"]["cartera"])
        cfg = self.cfg["aprobacion"]
        perdida = cf["entradas"]["cartera"].get("perdida_dia_eur", 0.0)
        fuera = not _en_horario(a, cfg["horario_utc"])
        sello_e = self.sellos.get((self.encargos.get(e.get("encargo_actual")) or {}).get("sello_ref")) or {}
        ev_k = eventos_entre(sello_e, a.astimezone(timezone.utc).date().isoformat(), e["propuesta"]["salida"]["fecha"], en["instrumento"])
        if ev_k is None:   # T-26 (R-M2): un calendario ilegible no se presenta como «sin eventos»
            return _no("O-01", "el calendario de eventos del sello no se puede leer: no se presenta la pantalla")
        motivos_espera = ((["pérdida en el día"] if perdida > cfg["enfriamiento_tras_perdida_dia_eur"] else []) + (["fuera de horario"] if fuera else [])
                          + (["anulación de veto"] if anulacion else []))   # T-50: anular un veto siempre espera
        espera = timedelta(minutes=cfg["enfriamiento_min"]) if motivos_espera else timedelta(0)
        p = {"expediente_id": expediente_id, "informe_f": control_f["event_id"], "informe_f_hash": _hash(control_f), "resultado_f": cf["resultado"],
             "instrumento": en["instrumento"], "via_acceso": en["via_acceso"], "direccion": "LARGO" if st["operador"] in ("<", "<=") else "CORTO",
             "fecha_revision": e["propuesta"]["salida"]["fecha"], "cantidad": q, "precio_limite": en["limite"], "stop": st["umbral"],
             "importe": round(q * en["limite"] * fx, 2), "riesgo": round(q * abs(en["limite"] - st["umbral"]) * fx, 2), "unidad_importe": "EUR",
             "divisa_cotizacion": cf["entradas"]["solicitud"]["divisa_cotizacion"], "tipo_cambio_eur": fx,
             "apalancamiento": en["apalancamiento"], "cartera": e["cartera_destino"], "valid_until_f": cf["valid_until"],
             "generada_en": ahora, "caduca_en": (a + espera + timedelta(minutes=cfg["caduca_min"])).isoformat(),
             "enfriamiento_hasta": (a + espera).isoformat(), "motivos_enfriamiento": motivos_espera, "anulacion": anulacion,
             "advertencias_k": self._advertencias_de(e),   # T-26: el operador ve (y acepta) las advertencias de K
             "eventos_k": ev_k}   # T-26: calendario
        # V0.40: las cifras de la §8 con las que F decidió, sacadas del propio informe y no del estado actual. El informe ya pasó
        # validar_informe_f (CF-01..CF-09) en _comprobar_autorizacion: CF-07 fija la política oficial y CF-09 el contexto exacto del
        # Orquestador al instante de emisión, cuya forma ya validó _forma_contexto (precio {valor, fecha_hora} con valor > 0, actividad
        # con sus tres cifras, eventos lista o None). Con anulación de veto, q es la cantidad anulada y el importe ya la usa.
        ctx_f = cf["entradas"]["contexto"]
        pol_f = cf["entradas"]["politica"]
        pi = ctx_f.get("precio_intermediario")
        p["precio_intermediario"] = pi.get("valor") if isinstance(pi, dict) else None
        p["precio_intermediario_en"] = pi.get("fecha_hora") if isinstance(pi, dict) else None
        p["deriva_pct"] = (round(abs(en["limite"] / p["precio_intermediario"] - 1) * 100, 4)
                           if _num(p["precio_intermediario"]) and p["precio_intermediario"] > 0 else None)   # la deriva de F-23
        p["importe_dia_eur"] = round(ctx_f["actividad"]["importe_dia_eur"] + p["importe"], 2)   # lo que quedaría autorizado hoy
        p["limite_dia_eur"] = pol_f["importe_max_dia_eur"]   # F-14
        p["perdida_semana_eur"] = ctx_f["actividad"]["perdida_semana_eur"]   # F-16
        p["limite_semana_eur"] = pol_f["perdida_semana_max_eur"]
        p["ordenes_ultima_hora"] = ctx_f["actividad"]["ordenes_ultima_hora"]   # F-17
        p["limite_ordenes_hora"] = pol_f["ordenes_max_hora"]
        p["eventos_f"] = copy.deepcopy(ctx_f.get("eventos"))   # F-21: los eventos que vio F, tal cual (pueden ser None)
        p["hash"] = _hash(p)
        self.pantallas[expediente_id] = {**p, "usada": False}
        return _r(True, "OK", "pantalla de aprobación lista", pantalla=copy.deepcopy(p))

    def _comprobar_aprobacion(self, expediente_id, control_f, aprobacion, a):
        p = self.pantallas.get(expediente_id)
        base = {"pantalla_hash", "importe_tecleado", "canal", "segundo_factor"}
        if not (isinstance(aprobacion, dict) and set(aprobacion) in (base, base | {"acepta_advertencias_k"})):
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
        if bool(p.get("advertencias_k")) != (aprobacion.get("acepta_advertencias_k") is True) or (
                "acepta_advertencias_k" in aprobacion and aprobacion["acepta_advertencias_k"] is not True):
            return _no("O-36", "la pantalla muestra advertencias de K: la aprobación debe aceptarlas expresamente (acepta_advertencias_k)"
                       if p.get("advertencias_k") else "no hay advertencias de K que aceptar en esta pantalla")
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
        cf = aplanar_informe(control_f)
        ih = _hash(control_f)
        dup = self._duplicado(control_f["event_id"], ih, expediente_id, ahora)
        if dup:
            return _no("O-03", "el informe de F ya se usó")
        anul, cantidad = None, cf["cantidad_aprobada"]
        if actor == "MATRIZ_AUTONOMIA" and cf["resultado"] != "VETADO":   # T-18: tamaño y horario, antes de cambiar nada
            err = self._matriz_permite(e, cantidad, cf["entradas"], a)
            if err:
                return err
        pant = self.pantallas.get(expediente_id) or {}
        if actor == "OPERADOR" and cf["resultado"] == "VETADO" and pant.get("anulacion") and aprobacion is not None:
            # T-50: anulación del veto por el operador: la pantalla de anulación, con su motivo, y el límite mensual de nuevo
            err = self._comprobar_aprobacion(expediente_id, control_f, aprobacion, a)
            if err:
                return err
            q, _, err = self._comprobar_anulacion(cf, {"motivo": pant["anulacion"]["motivo"]}, a)
            if err:
                return err
            if abs(q - pant["cantidad"]) > 1e-9:
                return _no("O-27", "la cantidad de la anulación ya no es la de la pantalla")
            self.pantallas[expediente_id]["usada"] = True
            anul, cantidad = copy.deepcopy(pant["anulacion"]), pant["cantidad"]
        elif actor == "OPERADOR" and cf["resultado"] != "VETADO":
            err = self._comprobar_aprobacion(expediente_id, control_f, aprobacion, a)
            if err:
                return err
            if pant.get("anulacion"):
                return _no("O-27", "esa pantalla es de una anulación de veto, no de este informe")
            self.pantallas[expediente_id]["usada"] = True
        self.eventos[control_f["event_id"]] = {"hash": ih, "expediente_id": expediente_id}
        if cf["resultado"] == "VETADO" and anul is None:
            return _no("O-06", "F vetó la propuesta")
        e["control_f"] = {"resultado": cf["resultado"], "cantidad_aprobada": cantidad, "event_id": cf["event_id"], "anulacion": anul,
                          "emitido_en": cf["emitido_en"], "valid_until": cf["valid_until"], "entradas": copy.deepcopy(cf["entradas"]),
                          "aprobacion": ({k: v for k, v in self.pantallas[expediente_id].items() if k != "usada"} if actor == "OPERADOR" else None)}
        motivo = (f"ANULACIÓN DE VETO ({', '.join(anul['vetos'])}; {cantidad}): {anul['motivo'][:150]}" if anul
                  else f"control F: {cf['resultado']} ({cf['cantidad_aprobada']})")
        self._anota(e, e["estado"], "AUTORIZADA", actor, ahora, motivo, cf["event_id"], datos=_hash(e["control_f"]))
        if anul:
            self._aviso("O-34", f"{expediente_id}: el operador anuló el veto de F ({', '.join(anul['vetos'])}); "
                        f"{self.anulaciones_mes(ahora)} de {self.cfg['anulaciones_veto_mes']} este mes", ahora, expediente_id, carteras={e["cartera_destino"]})
        return _r(True, "OK", "autorizada con el veto de F anulado por el operador" if anul else "autorizada")

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
        if estado == "ENVIADA":   # T-26 (R-M3): antes de enviar nada, todo íntegro (configuración, Motor, sellos y expedientes)
            rota = self._rota()
            if rota:
                self._activar_kill(f"integridad rota en {rota}", "ORQUESTADOR", self.ultimo_ahora or "1970-01-01T00:00:00+00:00")
                return _no("O-13", f"{rota} no es íntegro: no se envía la orden")
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
            return _no("O-05", "la autorización ya no vale (automática con la cartera por debajo de L2 o degradada después, o anterior a una bajada del límite de pérdida): "
                               "vuelve a pasar por F y por el operador")
        if estado == "ENVIADA" and self.autorizada_por(e) == "MATRIZ_AUTONOMIA":   # T-18: el umbral y el horario también al enviar
            err = self._matriz_permite(e, e["control_f"]["cantidad_aprobada"], e["control_f"]["entradas"], _dt(ahora))
            if err:
                return _no("O-05", f"al enviar: {err['motivo']}")
        if estado == "ENVIADA":
            err = self._f_al_enviar(e, expediente_id, ahora)
            if err:
                return err
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
                         cf["entradas"]["cartera"], cf["entradas"]["politica"], cf["emitido_en"], cf["entradas"]["contexto"])
        anul = cf.get("anulacion")
        vetan = {c["regla"] for c in real["controles"] if c["resultado"] == "VETA"}
        ok_anulado = (anul is not None and real["resultado"] == "VETADO" and vetan and vetan <= set(anul["vetos"])
                      and all(c["resultado"] in ("OK", "VETA") for c in real["controles"]))   # T-50 (R-G1): solo vuelven a vetar los anulados
        if real["resultado"] != "APROBADO" and not ok_anulado:
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
                                "nivel": self.nivel_en(e["cartera_destino"], t), "direccion": "LARGO" if [c for c in e["propuesta"]["salida"]["condiciones"] if c["tipo"] == "STOP"][0]["operador"] in ("<", "<=") else "CORTO",
                                "stop_precio": [c for c in e["propuesta"]["salida"]["condiciones"] if c["tipo"] == "STOP"][0]["umbral"],
                                "instrumento": e["propuesta"]["entrada"]["instrumento"], "activo_base": e["propuesta"]["entrada"]["activo_base"],
                                "condiciones_salida": copy.deepcopy(e["propuesta"]["salida"]), "protecciones": list(prot), "propuestas": [],
                                "origen": "MANUAL" if manual else "G", "ejecutada_en": orden.get("ejecutada_en") or ahora,
                                "cantidad_inicial": orden["cantidad"], "protecciones_anteriores": [], "reduccion": None, "reducciones": [],
                                "condiciones_consumidas": [], "via_acceso": e["propuesta"]["entrada"]["via_acceso"],
                                "fecha_revision": e["propuesta"]["salida"]["fecha"], "precio_entrada": orden["precio"],
                                "senales": _senales_de(e), "senales_disparadas": [], "perdida_alertada": 0}
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
        vinculado a una posición la cierra; LIBRE solo queda registrado y la conciliación lo cuenta como explicado. Una LIBRE
        cuenta además para su tope diario por cartera (T-33): se acepta igual y, si el tope se supera o hay importes sin
        valorar, avisa O-37 y degrada la cartera."""
        a = self._ahora(ahora)
        if not isinstance(registro, dict) or not isinstance(registro.get("event_id"), str):
            return _no("O-01", "registro CT-G-14 sin event_id")
        err = self._config_rota()   # T-51 (H5): las exclusiones y listas del mandato deben ser las de su huella
        if err:
            return err
        plano = aplanar_manual(registro)   # T-47: CT-G-14 0.2.0 llega envuelto; dentro se usa la forma plana
        if plano is None:
            fallos = validar_manual(registro, {"ahora": ahora})
            return _no("O-01", f"registro CT-G-14 no válido: {fallos[0]['regla']}: {fallos[0]['mensaje'][:80]}", reglas=sorted({x['regla'] for x in fallos}))
        v = plano["vinculo"] if isinstance(plano["vinculo"], dict) else {}
        ref = v.get("id") if isinstance(v.get("id"), str) else None
        h = _hash(registro)   # del mensaje completo: la misma operación con otra envoltura es otro contenido
        dup = self._duplicado(registro["event_id"], h, ref, ahora)
        if dup:
            return dup
        e = self.expedientes.get(ref) if v.get("tipo") == "EXPEDIENTE" else None
        p = self.posiciones.get(ref) if v.get("tipo") == "POSICION" else None
        if (e is not None and not self._todo_ok(e)) or (p is not None and not self._posicion_ok(p)):
            self._activar_kill(f"integridad rota en {ref}", "ORQUESTADOR", self.ultimo_ahora or "1970-01-01T00:00:00+00:00")
            return _no("O-13", "el expediente o la posición vinculados no son íntegros (historial, sobre, propuesta, orden, aprobación o estado)")
        err = self._reglas_manual(registro, plano, e, p, ahora)
        if err:
            return err
        ins = plano.get("instrumento")
        tope_libres = None   # T-33: solo una LIBRE devuelve tope_libres_superado
        if v["tipo"] == "EXPEDIENTE":
            orden = {"orden_id": plano["ref_intermediario"], "cantidad": plano["cantidad"], "precio": plano["precio"], "conciliada": True,
                     "proteccion_orden_ids": [plano["proteccion_ref"]]}
            r = self._ejecutar(e, orden, "OPERADOR", ahora, a, manual=True)
            if not r["ok"]:
                return r
        elif v["tipo"] == "POSICION":
            parcial = p["estado"] != "REDUCIENDO" and plano["cantidad"] < p["cantidad"] - TOL_Q   # T-44: reducción parcial declarada a mano
            if parcial:
                # Patrón de T-12: el stop nuevo (proteccion_ref) ya está colocado por el operador; aquí solo se sustituyen los viejos.
                # El registro declara la VENTA (como el cierre total declara la suya entera): cantidad es lo vendido y
                # restante es lo que queda, que es la cantidad nueva de la posición.
                p["protecciones_anteriores"] += [x for x in p["protecciones"] if x not in p["protecciones_anteriores"]]   # sin repetidos
                p["protecciones"] = [plano["proteccion_ref"]]
                self.ordenes_usadas += [x for x in (plano["proteccion_ref"], plano["ref_intermediario"]) if x not in self.ordenes_usadas]
                p["reducciones"].append({"n": len(p["reducciones"]) + 1, "cantidad": plano["cantidad"], "desde": p["cantidad"],
                                         "restante": p["cantidad"] - plano["cantidad"], "manual": True, "orden_id": plano["ref_intermediario"],
                                         "terminada_en": ahora, "motivo": plano["motivo"]})
                p["cantidad"] -= plano["cantidad"]   # se resta lo vendido
                self._anota_pos(p, p["estado"], p["estado"], "OPERADOR", ahora,
                                f"reducción parcial manual declarada (CT-G-14): {plano['motivo'][:120]}", plano["ref_intermediario"])
            else:
                if p.get("reduccion"):   # una reducción a medias termina con el cierre total
                    p["reducciones"].append({**p["reduccion"], "restante": 0, "interrumpida": "cierre manual"})
                    p["reduccion"] = None
                self._anota_pos(p, p["estado"], "CERRANDO", "OPERADOR", ahora, f"cierre manual declarado (CT-G-14): {plano['motivo'][:120]}")
                p["cantidad"] = 0
                self.ordenes_usadas.append(plano["ref_intermediario"])
                self._anota_pos(p, "CERRANDO", "CERRADA", "OPERADOR", ahora, "cierre manual declarado (CT-G-14)", plano["ref_intermediario"])
        else:   # LIBRE: fuera del control de F; queda a la vista del operador
            self.ordenes_usadas.append(plano["ref_intermediario"])
            self._aviso("O-20", f"operación libre declarada fuera del sistema (sin control de F ni stop): {plano['lado']} {plano['cantidad']} {ins}",
                        ahora, plano["event_id"])
            tope_libres = self._registrar_libre(plano, ins, ahora)   # T-33: el tope no rechaza (la operación ya ocurrió); avisa y degrada
        self.eventos[plano["event_id"]] = {"hash": h, "expediente_id": ref}
        self.manuales.append(copy.deepcopy(plano))
        r = _r(True, "OK", f"registro manual aceptado ({v['tipo']})", posicion_id=(e or {}).get("posicion_id") or (p or {}).get("posicion_id"))
        if tope_libres is not None:   # T-33: solo en una LIBRE
            r["tope_libres_superado"] = tope_libres
        return r

    def _registrar_libre(self, plano, ins, ahora):
        """T-33: el importe en euros de una LIBRE declarada y su tope diario por cartera. Se llama con el registro ya aceptado:
        el tope no lo rechaza (la operación ya ocurrió; rechazarla sería una discrepancia sin explicar), solo emite el aviso O-37
        y degrada la cartera. Devuelve True si el tope del día quedó superado (o hay importes sin valorar) y False si no."""
        fx = tipo_cambio(self.divisa(ins), self.ultima_foto)   # euros por unidad; 1.0 si la divisa es EUR
        try:
            importe = plano["cantidad"] * plano["precio"] * fx if fx is not None else None   # defecto_01: dos enteros enormes pasan RM-01 y el producto desborda
        except OverflowError:
            importe = None
        if importe is not None and not math.isfinite(importe):   # un producto desbordado no se puede valorar (falla cerrado)
            importe = None
        if importe == 0.0 and fx not in (None, 0) and plano["cantidad"] != 0 and plano["precio"] != 0:
            importe = None   # un producto que subdesborda a 0.0 tampoco se puede valorar: el valor verdadero es positivo y no cabe en un float (revisión, hallazgo 2)
        dia = _dt(plano["ejecutado_en"]).astimezone(timezone.utc).date().isoformat()   # el día UTC en que se ejecutó
        self.libres.append({"cartera": plano["cartera"], "dia": dia, "importe_eur": importe, "registrado_en": ahora,
                            "event_id": plano["event_id"]})
        grupo = [x for x in self.libres if x["cartera"] == plano["cartera"] and x["dia"] == dia]
        tope = self.cfg["libres_tope_dia_eur"][plano["cartera"]]
        sin_valor = any(x["importe_eur"] is None for x in grupo)
        suma = 0.0   # defecto_02: suma plana; math.fsum lanzaría OverflowError con dos importes de 1e308 y el registro debe aceptarse igual
        for x in grupo:
            if x["importe_eur"] is not None:
                suma += x["importe_eur"]
        if not sin_valor and suma <= tope:
            return False
        motivo = (f"operaciones libres de {plano['cartera']} el {dia}: {suma} EUR por encima del tope {tope} EUR" if not sin_valor
                  else f"operaciones libres de {plano['cartera']} el {dia}: sin poder valorarlas en euros")
        self._aviso("O-37", motivo, ahora, plano["event_id"], carteras={plano["cartera"]})
        self._degradar(plano["cartera"], motivo, ahora)
        return True

    def _reglas_manual(self, registro, plano, e, p, ahora):
        """Las reglas de CT-G-14 que no tocan nada (RM-01 a RM-11, O-03 orden ya usada, O-25 entrada viva)."""
        v = plano["vinculo"]
        ins = plano.get("instrumento")
        ocupado = any(q["estado"] != "CERRADA" and q["instrumento"] == ins for q in self.posiciones.values()) \
            or any(x["estado"] == "AUTORIZADA" and x.get("propuesta", {}).get("entrada", {}).get("instrumento") == ins for x in self.expedientes.values())
        desde = None
        if e is not None:
            desde = next((x["ahora"] for x in reversed(e["historial"]) if x["hasta"] == "AUTORIZADA"), None)
        elif p is not None:
            desde = p["historial"][0]["ahora"]
        fallos = validar_manual(registro, {"ahora": ahora, "expediente": e, "posicion": p, "tolerancia_precio": self.cfg["tolerancia_precio_entrada"],
                                           "instrumentos_permitidos": {k: v["instrumentos_permitidos"] for k, v in self.cfg["mandatos"].items()
                                                                       if v["instrumentos_permitidos"] is not None},   # T-51: del mandato de SC-1
                                           "instrumentos_excluidos": {k: v["exclusiones"] for k, v in self.cfg["mandatos"].items()},
                                           "instrumento_ocupado": ocupado, "no_antes_de": desde, "identidad": self._identidad_manual(e, p),
                                           "valor_min_restante_eur": self._valor_min_restante(p["instrumento"]) if p is not None else None})   # T-44
        if fallos:
            return _no("O-01", f"registro CT-G-14 no válido: {fallos[0]['regla']}: {fallos[0]['mensaje'][:80]}", reglas=sorted({x['regla'] for x in fallos}))
        if plano["ref_intermediario"] in self.ordenes_usadas or plano.get("proteccion_ref") in self.ordenes_usadas \
                or plano["ref_intermediario"] == plano.get("proteccion_ref"):
            return _no("O-03", "esa orden del intermediario ya está registrada")
        if v["tipo"] == "EXPEDIENTE" and self._entrada_viva(e):
            return _no("O-25", "hay una orden de entrada de G viva para este expediente: cancélela antes de ejecutar a mano")
        return None

    def comprobar_manual(self, registro, ahora):
        """Comprobación previa de un CT-G-14, SIN EFECTOS (no anota, no mueve el reloj, no activa nada): G la llama antes de consultar
        o tocar el intermediario. None si registrar_manual no lo rechazaría por forma, reglas, duplicado o integridad; si no, el
        motivo. Ante la duda (duplicado, integridad) también devuelve un rechazo: G delega entonces en registrar_manual."""
        try:
            if not (isinstance(ahora, str) and _FH.match(ahora)) or (self.ultimo_ahora is not None and _dt(ahora) < _dt(self.ultimo_ahora)):
                return _no("O-00", "instante inválido o anterior al último")
            if not isinstance(registro, dict) or not isinstance(registro.get("event_id"), str):
                return _no("O-01", "registro CT-G-14 sin event_id")
            if not self.config_integra():   # T-51 (H5); sin efectos: registrar_manual activará el kill-switch
                return _no("O-13", "la configuración (o un mandato de SC-1) no es la de su huella")
            plano = aplanar_manual(registro)
            if plano is None:
                fallos = validar_manual(registro, {"ahora": ahora})
                return _no("O-01", f"registro CT-G-14 no válido: {fallos[0]['regla']}", reglas=sorted({x['regla'] for x in fallos}))
            if registro["event_id"] in self.eventos:
                return _no("O-03", "event_id ya registrado")
            v = plano["vinculo"] if isinstance(plano["vinculo"], dict) else {}
            ref = v.get("id") if isinstance(v.get("id"), str) else None
            e = self.expedientes.get(ref) if v.get("tipo") == "EXPEDIENTE" else None
            p = self.posiciones.get(ref) if v.get("tipo") == "POSICION" else None
            if (e is not None and not self._todo_ok(e)) or (p is not None and not self._posicion_ok(p)):
                return _no("O-13", "el expediente o la posición vinculados no son íntegros")
            if not isinstance(plano["vinculo"], dict):
                fallos = validar_manual(registro, {"ahora": ahora})
                return _no("O-01", "registro CT-G-14 no válido", reglas=sorted({x['regla'] for x in fallos}))
            return self._reglas_manual(registro, plano, e, p, ahora)
        except Exception as ex:   # noqa: BLE001 - una comprobación previa nunca lanza: ante la duda, rechaza
            return _no("O-00", f"no se pudo comprobar el registro ({type(ex).__name__})")

    def _identidad_manual(self, e, p):
        """(expediente_id, correlation_id) que debe llevar la envoltura de un CT-G-14 vinculado (RM-11); None si no hay vínculo."""
        if e is not None:
            return (e["expediente_id"], e["correlation_id"])
        if p is not None and p.get("expediente_id") in self.expedientes:
            return (p["expediente_id"], self.expedientes[p["expediente_id"]]["correlation_id"])
        return None

    def _valor_min_restante(self, ins):
        """T-44: el valor mínimo que debe quedar tras una reducción parcial declarada a mano: el valor_min_eur de la
        política de F convertido a la divisa de cotización del instrumento con el último tipo de cambio conocido
        (la misma fuente que T-33 usa para valorar las LIBRES). None si no se puede convertir: manual_g rechaza
        entonces la reducción parcial con RM-12 (falla cerrado: sin poder valorar el resto, ciérrala entera)."""
        pol = self.cfg.get("politica_f")
        vm = pol.get("valor_min_eur") if isinstance(pol, dict) else None
        if not (_num(vm) and vm >= 0):
            return None
        fx = tipo_cambio(self.divisa(ins), self.ultima_foto)   # euros por unidad de la divisa de cotización
        if not (_num(fx) and fx > 0):
            return None
        try:
            v = vm / fx
        except (OverflowError, ZeroDivisionError, ValueError):
            return None
        return v if _num(v) and v >= 0 else None

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
        if not (isinstance(motivo, str) and motivo.strip() and isinstance(condiciones_reapertura, list) and condiciones_reapertura):
            return _no("O-15", "se exigen motivo y condiciones de reapertura")
        hoy = _dt(ahora).astimezone(timezone.utc).date()
        err = _condiciones_reapertura_ok(condiciones_reapertura, hoy)
        if err:
            return _no("O-01", f"condiciones de reapertura: {err}")
        vence = hoy + timedelta(days=self.cfg["observacion_max_dias"])
        if any(c["tipo"] == "FECHA" and date.fromisoformat(c["fecha"]) > vence for c in condiciones_reapertura):
            return _no("O-01", f"condiciones de reapertura: una FECHA posterior al vencimiento de la observación ({vence}) no podría cumplirse")
        en = self.encargos.get(e["encargo_actual"]) if e["encargo_actual"] else None
        cortes = [x for x in ((e.get("sobre") or {}).get("fecha_corte"), en["fecha_corte"] if en else None) if x]
        e["reapertura"] = {"condiciones": copy.deepcopy(condiciones_reapertura), "desde": ahora, "actor": actor, "motivo": motivo[:200],
                           "vence": vence.isoformat(), "cumplida": None,
                           "corte_previo": max(cortes) if cortes else None}   # el corte más reciente con que se analizó o se encargó
        self._anota(e, e["estado"], "EN_OBSERVACION", actor, ahora, motivo, datos=_hash(e["reapertura"]))
        return _r(True, "OK", "en observación", vence=e["reapertura"]["vence"])

    def _reapertura_ok(self, e):
        """En observación, las condiciones (y si se cumplieron) son las anotadas en la cadena."""
        if e["estado"] != "EN_OBSERVACION":
            return True
        ult = [h for h in e["historial"] if h["hasta"] == "EN_OBSERVACION"]
        return bool(ult) and isinstance(e.get("reapertura"), dict) and ult[-1]["datos"] == _hash(e["reapertura"])

    def _cumple(self, e, cond, datos, a, max_edad_min=PARAMETROS["h_max_edad_dato_min"]):
        """Valor con el que se cumple la condición, o None. PRECIO: dato fresco (15 min) del instrumento; FECHA: llegó;
        SELLO_NUEVO: hay un sello vigente con corte posterior al del análisis (o al día de la observación)."""
        if cond["tipo"] == "FECHA":
            return cond["fecha"] if a.astimezone(timezone.utc).date() >= date.fromisoformat(cond["fecha"]) else None
        if cond["tipo"] == "SELLO_NUEVO":
            base = e["reapertura"]["corte_previo"] or str(_dt(e["reapertura"]["desde"]).astimezone(timezone.utc).date())
            hoy = str(a.astimezone(timezone.utc).date())
            nuevos = sorted(s["fecha_corte"] for s in self.sellos.values() if s["estado"] != "ANULADO" and s["fecha_corte"] > base
                            and estado_sello({**s, "estado": "VIGENTE"}, hoy, e["cartera_destino"], self.cal_def) == "VIGENTE")
            return nuevos[-1] if nuevos else None   # vigente hoy para la cartera del expediente (antigüedad de K por cartera)
        d = next((v for k, v in datos.items() if _ins(k) == _ins(cond["instrumento"])), None) if isinstance(datos, dict) else None
        try:
            fresco = (isinstance(d, dict) and _num(d.get("precio")) and d["precio"] > 0
                      and 0 <= (a - _dt(d["hora"])).total_seconds() <= max_edad_min * 60)
        except Exception:   # noqa: BLE001
            fresco = False
        return d["precio"] if fresco and OPERADORES[cond["operador"]](d["precio"], cond["umbral"]) else None

    def _primera_cumplida(self, e, datos, a, max_edad_min=PARAMETROS["h_max_edad_dato_min"]):
        """(índice, valor) de la primera condición que se cumple, sin tocar nada; None si ninguna o si la observación venció."""
        if a.astimezone(timezone.utc).date() > date.fromisoformat(e["reapertura"]["vence"]):
            return None
        for i, c in enumerate(e["reapertura"]["condiciones"]):
            v = self._cumple(e, c, datos, a, max_edad_min)
            if v is not None:
                return i, v
        return None

    def _reaperturas_hechas(self, e):
        """Reaperturas que cuentan para el límite: las que no autorizó el operador con reabrir."""
        n, por_operador = 0, False
        for h in e["historial"]:
            if h["hasta"] == "EN_OBSERVACION" and h["desde"] != "EN_OBSERVACION":
                por_operador = False
            elif h["desde"] == h["hasta"] == "EN_OBSERVACION" and h["ref"] == "REABRE":
                por_operador = True
            elif h["desde"] == "EN_OBSERVACION" and h["hasta"] == "EN_ANALISIS" and not por_operador:
                n += 1
        return n

    def _marcar_cumplida(self, eid, e, iv, actor, ahora):
        i, v = iv
        c = e["reapertura"]["condiciones"][i]
        e["reapertura"]["cumplida"] = {"condicion": i, "valor": v, "ahora": ahora, "por": actor}
        self._anota(e, "EN_OBSERVACION", "EN_OBSERVACION", actor, ahora, f"condición de reapertura {i} cumplida ({c['tipo']})",
                    datos=_hash(e["reapertura"]))
        if self._reaperturas_hechas(e) >= self.cfg["max_reaperturas"]:
            txt = f"{eid}: se cumplió su condición de reapertura ({c['tipo']}: {v}), pero ya llegó al límite de reaperturas: solo el operador puede reabrirlo"
        else:
            txt = f"{eid}: se cumplió su condición de reapertura ({c['tipo']}: {v}); se puede re-encargar hasta {e['reapertura']['vence']}"
        self._aviso("O-31", txt, ahora, eid, carteras={e["cartera_destino"]})

    def _revisar_reapertura(self, eid, e, datos, actor, a, ahora, max_edad_min=PARAMETROS["h_max_edad_dato_min"]):
        """Marca cumplida la primera condición que se cumpla (dentro de plazo) y avisa. Devuelve True si cambió algo."""
        if e["reapertura"]["cumplida"] is not None:
            return False
        iv = self._primera_cumplida(e, datos, a, max_edad_min)
        if iv is None:
            return False
        self._marcar_cumplida(eid, e, iv, actor, ahora)
        return True

    @_seguro
    def revisar_reaperturas(self, datos, actor, ahora, max_edad_min=PARAMETROS["h_max_edad_dato_min"]):
        """H (en cada pasada, con sus precios) o el Orquestador comprueban las condiciones de los expedientes en observación."""
        a = self._ahora(ahora)
        if actor not in ("H", "ORQUESTADOR"):
            return _no("O-05", "solo H o el Orquestador vigilan las condiciones de reapertura")
        if not (_num(max_edad_min) and 0 < max_edad_min <= PARAMETROS["h_max_edad_dato_min"]):
            return _no("O-01", f"la frescura solo puede ser más estricta que {PARAMETROS['h_max_edad_dato_min']} min")
        cumplidas = []
        for eid, e in sorted(self.expedientes.items()):
            if e["estado"] == "EN_OBSERVACION":
                if not self._todo_ok(e):
                    continue   # alterado: no se marca nada (lo ve integridad y cualquier operación sobre él)
                if self._revisar_reapertura(eid, e, datos, actor, a, ahora, max_edad_min):
                    cumplidas.append(eid)
        return _r(True, "OK", f"{len(cumplidas)} reapertura(s) cumplida(s)", cumplidas=cumplidas)

    @_seguro
    def reabrir(self, expediente_id, motivo, actor, ahora):
        """El operador permite reabrir un expediente en observación aunque su condición no se haya cumplido (o pasado el límite)."""
        self._ahora(ahora)
        e, err = self._exp(expediente_id)
        if err:
            return err
        if actor != "OPERADOR":
            return _no("O-05", "solo el operador reabre sin que se cumpla la condición")
        if not (isinstance(motivo, str) and motivo.strip()):
            return _no("O-15", "reabrir exige motivo")
        if e["estado"] != "EN_OBSERVACION":
            return _no("O-04", "solo se reabre un expediente en observación")
        if _dt(ahora).astimezone(timezone.utc).date() > date.fromisoformat(e["reapertura"]["vence"]):
            return _no("O-10", f"la observación venció el {e['reapertura']['vence']}")
        e["reapertura"]["cumplida"] = {"condicion": None, "valor": None, "ahora": ahora, "por": "OPERADOR", "motivo": motivo[:200]}
        self._anota(e, "EN_OBSERVACION", "EN_OBSERVACION", "OPERADOR", ahora, f"reapertura autorizada por el operador: {motivo[:120]}",
                    "REABRE", datos=_hash(e["reapertura"]))
        return _r(True, "OK", "reapertura autorizada")

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
        for eid, e in sorted(self.expedientes.items()):   # T-46: observaciones
            if e["estado"] != "EN_OBSERVACION" or not isinstance(e.get("reapertura"), dict) or not self._todo_ok(e):
                continue
            if a.astimezone(timezone.utc).date() > date.fromisoformat(e["reapertura"]["vence"]):
                self._anota(e, "EN_OBSERVACION", "DESCARTADA", "ORQUESTADOR", ahora, f"la observación venció el {e['reapertura']['vence']}")
                self._aviso("O-31", f"{eid}: la observación venció sin reabrirse; queda descartado", ahora, eid, carteras={e["cartera_destino"]})
                cambios.append(("expediente", eid, "DESCARTADA"))
            elif self._revisar_reapertura(eid, e, None, "ORQUESTADOR", a, ahora):
                cambios.append(("reapertura", eid, "CUMPLIDA"))
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
    def registrar_senal(self, posicion_id, tipo, ref, valor, actor, ahora):
        """T-49: H registra una señal cumplida sobre una posición: un escenario de fallo o una invalidez por otra métrica (H-16)
        o una pérdida no realizada que pasa el umbral (H-17). Nunca vende: pide revisión (ABIERTA -> EN_REVISION) y deja la
        propuesta. Cada señal se registra una vez; la pérdida, una vez por cada múltiplo del umbral."""
        self._ahora(ahora)
        p, err = self._pos(posicion_id)
        if err:
            return err
        if actor not in ("H", "ORQUESTADOR"):
            return _no("O-05", "solo H registra señales de vigilancia")
        if p["estado"] not in ("ABIERTA", "EN_REVISION"):
            return _no("O-04", f"la posición está {p['estado']}: las señales solo se registran en una posición abierta o en revisión")
        if not self._posicion_ok(p):
            return _no("O-13", "la posición no es íntegra")
        if not _num(valor):
            return _no("O-01", "valor no numérico")
        if tipo == "SENAL":
            s_ = next((x for x in p["senales"] if x["clave"] == ref), None)   # por clave (origen:id): los ids pueden coincidir (R-02)
            if s_ is None:
                return _no("O-01", "señal desconocida en esta posición")
            if ref in p["senales_disparadas"]:
                return _no("O-02", "esa señal ya se registró")
            if not OPERADORES[s_["operador"]](valor, s_["umbral"]):
                return _no("O-01", "la señal no se cumple con ese valor")
            pref = "ESCENARIO DE FALLO" if s_["origen"] == "CONTRADICTOR" else "INVALIDEZ"
            texto = f"{pref}: {s_['id']} se cumple ({s_['metrica']} {valor} {s_['operador']} {s_['umbral']}): {s_['texto'][:160]}; revise la tesis"
            p["senales_disparadas"].append(ref)
        elif tipo == "PERDIDA":   # valor: el precio actual; la pérdida la calcula el Orquestador con su precio de entrada (R-07)
            um = self.cfg["alerta_perdida_pct"]
            nv = nivel_perdida(p, valor, um)
            if nv is None:
                return _no("O-01", "no se puede calcular la pérdida con ese precio")
            pp, k = nv
            if k <= p["perdida_alertada"]:
                return _no("O-02", "esa pérdida no llega a un nivel nuevo (o ya se alertó)")
            texto = f"ALERTA DE PÉRDIDA: {pp:.2f} % no realizada al precio {valor} (umbral {um} %, nivel {k}); revise la tesis o cierre"
            p["perdida_alertada"] = k
        else:
            return _no("O-01", "tipo de señal desconocido (SENAL o PERDIDA)")
        p["propuestas"].append({"actor": "H", "texto": texto, "ahora": ahora})
        desde = p["estado"]
        self._anota_pos(p, desde, "EN_REVISION", "H", ahora, texto[:200], ref if tipo == "SENAL" else "PERDIDA")
        return _r(True, "OK", texto)

    @_seguro
    def proponer_sobre_posicion(self, posicion_id, texto, actor, ahora):
        """H (o quien sea) propone; una invalidez cualitativa nunca vende."""
        self._ahora(ahora)
        p, err = self._pos(posicion_id)
        if err:
            return err
        if not (isinstance(texto, str) and texto.strip()):
            return _no("O-15", "la propuesta exige texto")
        if not (isinstance(actor, str) and _ID.match(actor)):
            return _no("O-05", "actor mal formado")
        p["propuestas"].append({"actor": actor, "texto": texto, "ahora": ahora})
        self._anota_pos(p, p["estado"], p["estado"], actor, ahora, "propuesta: " + texto[:180])   # en la cadena (T-49, R-04)
        return _r(True, "OK", "propuesta registrada; no cambia el estado de la posición")

    def _paso_pos(self, p):
        """V0.52 (T-43): el paso de cantidad del instrumento de la posición: el que usó E al dimensionar su propuesta. None si no se sabe."""
        e = self.expedientes.get(p.get("expediente_id"))
        paso = (((e or {}).get("propuesta") or {}).get("dimensionado") or {}).get("paso")
        return paso if _num(paso) and paso > 0 else None

    def _cantidad_reduccion(self, p, q, a, automatica):
        """V0.52 (T-43): la cantidad de una reducción y su validez, o (None, error O-06). La de una toma parcial automática (fracción
        de la cantidad inicial) se redondea hacia abajo al paso del instrumento; la que pide el operador tiene que ser ya un múltiplo
        del paso (se le dice cuál cabe). Lo que queda tiene que valer al menos el mínimo de F (politica_f.valor_min_eur) con la
        última cotización fresca de G y el tipo de cambio de la última foto; si no, se cierra entera. Sin paso, cotización fresca o
        tipo de cambio no se reduce (falla cerrado)."""
        if not (_num(q) and q > TOL_Q):
            return None, _no("O-06", "la reducción exige una cantidad positiva y mayor que la tolerancia de cantidades")
        paso = self._paso_pos(p)
        if paso is None:
            return None, _no("O-06", "no se conoce el paso de cantidad del instrumento de la posición: redúzcala a mano o ciérrela")
        if automatica:
            q = round(math.floor(q / paso * (1 + 1e-12)) * paso, 12)   # como E: hacia abajo y ajustada a la rejilla del paso
        else:   # revisión de V0.52, hallazgo 2: tolerancia relativa al paso (no a la cantidad) y la cantidad se ajusta a la rejilla
            k = round(q / paso)
            if abs(q / paso - k) > 1e-6:
                abajo = round(math.floor(q / paso) * paso, 12)
                return None, _no("O-06", f"la cantidad tiene que ser un múltiplo del paso del instrumento ({paso}); la más próxima por debajo es {abajo}")
            q = round(k * paso, 12)
        if not q > TOL_Q:
            return None, _no("O-06", f"la reducción no llega a un paso del instrumento ({paso})")
        if q >= p["cantidad"] - TOL_Q:
            return None, _no("O-06", "la reducción dejaría la posición a cero o al revés: use el cierre (CERRANDO)")
        cot = self._cotizacion_en(p["instrumento"], a)
        frescura = timedelta(minutes=self.cfg["politica_f"]["precio_frescura_max_min"])   # la del precio (F-23), no la de la foto (hallazgo 5)
        if not (cot and timedelta(0) <= a - _dt(cot["fecha_hora"]) <= frescura):
            return None, _no("O-06", "sin una cotización reciente de G no se sabe si lo que queda vale el mínimo: G cotiza antes de reducir", transitorio=True)
        fx = tipo_cambio(self.divisa(p["instrumento"]), self.ultima_foto) if self.ultima_foto else None
        if not (_num(fx) and fx > 0):
            return None, _no("O-06", "sin el tipo de cambio de la última foto de G no se puede valorar lo que queda", transitorio=True)
        resto_eur = (p["cantidad"] - q) * cot["valor"] * fx
        minimo = self.cfg["politica_f"]["valor_min_eur"]
        if resto_eur < minimo:
            return None, _no("O-06", f"lo que queda valdría {resto_eur:.2f} EUR, menos que el mínimo de F ({minimo} EUR): ciérrela entera")
        return q, None

    def cantidad_reduccion(self, posicion_id, ahora, cantidad=None, condicion_id=None):
        """V0.52 (T-43), sin efectos: la cantidad con la que se reduciría ahora la posición (la del operador, o la de la toma parcial
        de la condición OBJETIVO con fracción), o el motivo por el que no se puede. H la consulta antes de una toma parcial."""
        p = self.posiciones.get(posicion_id) if isinstance(posicion_id, str) else None
        if p is None or p["estado"] not in ("ABIERTA", "EN_REVISION"):
            return _no("O-12", "la posición no existe o no se puede reducir en su estado")
        if not (isinstance(ahora, str) and _FH.match(ahora)):   # revisión de V0.52, hallazgo 6: responde, no lanza
            return _no("O-01", "instante ilegible")
        a = _dt(ahora)
        if condicion_id is not None:
            c = next((x for x in p["condiciones_salida"]["condiciones"] if x["id"] == condicion_id and x.get("fraccion") is not None), None)
            if c is None:
                return _no("O-06", "esa condición no declara una toma parcial")
            if c["id"] in p["condiciones_consumidas"]:
                return _no("O-06", "esa condición ya redujo la posición una vez")
            q, err = self._cantidad_reduccion(p, c["fraccion"] * p["cantidad_inicial"], a, automatica=True)
        else:
            q, err = self._cantidad_reduccion(p, cantidad, a, automatica=False)
        return err or _r(True, "OK", f"se reduciría {q}", cantidad=q, restante=p["cantidad"] - q)

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
                         and condicion.get("stop_ejecutado_orden_id") in p["protecciones"] + p.get("protecciones_anteriores", []))   # el stop propio ya saltó en el intermediario (V0.53: también uno retirado por una parcial a mano que aún saltó)
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
                q, err = self._cantidad_reduccion(p, decl["fraccion"] * p["cantidad_inicial"], _dt(ahora), automatica=True)
                if err:
                    return err
                if cantidad is not None and not (_num(cantidad) and abs(cantidad - q) <= 1e-9 * max(1.0, q)):
                    return _no("O-06", f"la cantidad no es la que fija la fracción declarada, redondeada al paso ({q})")
            else:
                q, err = self._cantidad_reduccion(p, cantidad, _dt(ahora), automatica=False)
                if err:
                    return err
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
            propia = hasta == "CERRADA" and orden["orden_id"] in p["protecciones"] + p["protecciones_anteriores"]   # el cierre puede ser el propio stop que saltó (V0.53: o uno retirado que aún saltó)
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
            p["reduccion"] = {"n": len(p["reducciones"]) + 1, "cantidad": q, "desde": p["cantidad"], "objetivo_restante": round(p["cantidad"] - q, 12),
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
