"""Servicio del Motor (AG-13) en el ejecutor: despacho CT-09, re-ejecución CT-10 y Registro de cálculos.

Cada servicio escribe en RC su artefacto reproducible: operación y versión de ficha, datos efectivos
(símbolo, rango, huella), parámetros, semilla, fecha de corte, resultado y clave de idempotencia
(hash de todo lo anterior). Una petición idéntica se sirve desde caché. Las fichas del Catálogo no
implementadas se rechazan con `METODO_NO_IMPLEMENTADO` (y la alternativa del núcleo transversal).
"""
from __future__ import annotations

import copy
import functools
import math
import os
import re
import threading
from collections.abc import Callable
from pathlib import Path
from typing import Any, TypeGuard

import numpy as np
import pandas as pd

from ..configuracion import DIR_EJECUTOR, config_por_defecto, parametro, raiz_paquete
from ..herramientas.ht01_datos import DatosNoDisponibles, FugaDeInformacion
from ..herramientas.ht06_indice import clave_hash
from . import evaluacion as ev
from . import (
    fichas_fon_der,
    fichas_mon_idx,
    fichas_p2,
    fichas_reales,
    fichas_riesgo,
    fichas_series,
    fichas_tcv,
    fichas_valoracion,
)
from . import operaciones as op

CATALOG_VERSION = "5.0"
# Índice de fichas documentadas. IMPLEMENTADAS enumera por separado los métodos ejecutables.
FICHAS_CATALOGO = [
    "FX-TREND-001", "FX-BRK-001", "FX-STL-001", "FX-VOL-001", "FX-REGIME-001", "FX-PPA-001", "FX-CARRY-001",
    "FX-COINT-001", "FX-CORR-001", "ST-DESC-001", "ST-INF-001", "FIN-CAGR-001", "BIB-MET-001", "SIM-MC-001",
    "RISK-VAR-001", "ML-CAL-001", "AUD-REX-001", "SCORE-RK-001", "FC-EVAL-001", "FC-CAL-001", "BT-DSR-001",
    "BT-PBO-001", "BT-VAR-001", "SCN-H-001", "VOL-GARCH-001", "REG-HMM-001", "ML-PRED-001", "ML-CLUS-001",
    "RISK-DD-001", "DEC-VOI-001", "DER-OPT-001", "TEM-DIFF-001", "ACC-VAL-001", "ACC-ERP-001", "ACC-FACT-001",
    "ACC-MOM-001", "FIR-PRICE-001", "FIR-CURVE-001", "FIR-CARRY-001", "FIR-SPREAD-001", "FIR-CRED-001",
    "FX-BEER-001", "FX-MOM-001", "CMD-CURVE-001", "CMD-INV-001", "CMD-RETDEC-001", "CMD-REAL-001", "REI-NAV-001",
    "REI-CAP-001", "REI-FFO-001", "REI-LEV-001", "CHR-ONCHAIN-001", "CHR-FUND-001", "CHR-FLOW-001",
    "CHR-TOKEN-001", "PRV-PME-001", "PRV-CF-001", "ALT-DESMOOTH-001", "ALT-HF-001", "ALT-AUC-001",
    "DER-ROLL-001", "DER-SKEW-001", "DER-TERM-001", "DER-VRP-001",
    "FON-DISC-001", "FON-FLOW-001", "FON-LEV-001", "FON-TD-001",
    "IDX-CONC-001", "IDX-ERP-001", "IDX-REB-001", "IDX-REL-001",
    "MON-EXP-001", "MON-FIX-001", "MON-REAL-001", "MON-YLD-001",
    "TCV-BEI-001", "TCV-CDS-001", "TCV-SLOPE-001", "TCV-TP-001", "TCV-VIXTS-001",
]
ALTERNATIVAS = {"REG-HMM-001": "FX-TREND-001", "FX-REGIME-001": "FX-TREND-001", "RISK-VAR-001": "RISK-DD-001",
                "SCN-H-001": "FX-VOL-001", "FIR-SPREAD-001": "ST-DESC-001", "FIR-CARRY-001": "FX-CARRY-001",
                "ML-PRED-001": "ACC-MOM-001", "ACC-VAL-001": "ACC-ERP-001", "REI-NAV-001": "REI-CAP-001",
                "CHR-ONCHAIN-001": "ACC-MOM-001", "ALT-DESMOOTH-001": "RISK-DD-001"}


def _sesiones_anuales(params: dict) -> int:
    return 365 if params.get("clase") == "CRI" else 252


def _por_serie(fn: Callable[[pd.Series, dict], dict]) -> Callable:
    """Aplica una función a cada serie; los fallos por símbolo se anotan como limitaciones."""
    def envoltura(ent: dict, params: dict) -> tuple[dict, list[str]]:
        tabla, lim = {}, []
        for s, serie in ent["series"].items():
            try:
                tabla[s] = fn(serie, params)
            except op.ErrorFicha as e:
                lim.append(f"{s}: {e}")
        if not tabla:
            raise op.ErrorFicha("; ".join(lim) or "sin series")
        return {"tabla": tabla}, lim
    envoltura.__name__ = fn.__name__
    return envoltura


def _f_desc(s, p):
    r = op.rentabilidades(s)
    out = {"rendimientos": op.descriptiva(r.values)}
    if p.get("posicion_ultimo", True):
        ventana = int(p.get("ventana_posicion", 756))
        hist = s.iloc[-ventana:]
        out["posicion_precio"] = op.posicion_historica(float(s.iloc[-1]), hist.values)
    return out


def _f_cagr(s, p):
    out = {f"rent_{k}": op.rentabilidad_periodo(s, n) for k, n in (("1s", 5), ("1m", 21), ("3m", 63), ("6m", 126), ("12m", 252))}
    anios = (s.index[-1] - s.index[0]).days / 365.25
    out["cagr_ventana"] = op.cagr(float(s.iloc[0]), float(s.iloc[-1]), anios) if anios > 0 else None
    return out


def _f_mom(s, p):
    return op.momentum_12_1(s, int(p.get("retrospeccion", 12)), int(p.get("salto", 1)))


def _f_vol(s, p):
    return op.volatilidad(s, int(p.get("ventana", 20)), _sesiones_anuales(p))


def _f_garch(s, p):
    return op.garch11(s, int(p.get("horizonte", 10)), _sesiones_anuales(p))


def _f_trend(s, p):
    sem = s.resample("W-FRI").last().dropna()
    sem = sem.iloc[-int(p.get("ventana_semanas", 26)):]
    return op.mann_kendall(sem.values, float(p.get("nivel", 0.05)), bool(p.get("corregir_autocorrelacion", True)))


def _f_riesgo(s, p):
    return op.escala_riesgo(s, _sesiones_anuales(p), p.get("dias_liquidacion"))


def f_momentum(ent, params):
    res, lim = _por_serie(_f_mom)(ent, params)
    rangos = op.rango_transversal({k: v["momentum"] for k, v in res["tabla"].items()})
    for k, v in rangos.items():
        res["tabla"][k]["percentil_transversal"] = v["percentil"]
        res["tabla"][k]["z_transversal"] = v["z"]
    if len(rangos) < 10:
        lim.append(f"universo de {len(rangos)} miembros (< 10): rango transversal orientativo")
    return res, lim


def f_corr(ent, params):
    rend = pd.DataFrame({k: op.rentabilidades(s) for k, s in ent["series"].items()})
    return op.correlaciones(rend, float(params.get("cola_cuantil", 0.05))), []


def f_clus(ent, params):
    sem = pd.DataFrame({k: s.resample("W-FRI").last() for k, s in ent["series"].items()}).pct_change()
    sem = sem.iloc[-int(params.get("ventana_semanas", 104)):]
    lim = []
    if len(sem.dropna()) < 52:
        lim.append("menos de 1 año de rendimientos semanales comunes: clústeres orientativos")
    return op.clusteres(sem, float(params.get("umbral_rho", 0.7))), lim


def f_carry(ent, params):
    v = ent["valores"]
    spot = next(iter(ent["series"].values())) if ent["series"] else None
    if spot is not None:
        s0, s1 = float(spot.iloc[0]), float(spot.iloc[-1])
        anios = (spot.index[-1] - spot.index[0]).days / 365.25
    else:
        s0, s1, anios = float(v["spot_ini"]), float(v["spot_fin"]), float(v["anios"])
    return op.carry_divisas(float(v["tipo_base"]), float(v["tipo_cotizada"]), s0, s1, anios), []


def f_roll(ent, params):
    v = dict(ent["valores"])
    for rol in ("f_proximo", "f_siguiente"):
        if rol not in v and rol in ent["series_rol"]:
            v[rol] = float(ent["series_rol"][rol].iloc[-1])
    return op.roll_yield(float(v["f_proximo"]), float(v["f_siguiente"]), float(v["dias_entre"]), v.get("tipo_libre")), []


def f_fc_eval(ent, params):
    v = ent["valores"]
    m = ev.evaluar_celda(v["p"], v["o"], v.get("p_ref", [0.5] * len(v["p"])), float(params.get("tasa_base", 0.5)),
                         int(params.get("replicas", 2000)), int(params.get("simulaciones", 2000)),
                         float(params.get("nivel", 0.90)), int(params.get("semilla_bootstrap", 12345)), int(params.get("h", 1)))
    lim = [] if m["n"] >= 30 else [f"n = {m['n']} < 30: solo detecta ventajas grandes; «no significativo» no equivale a «sin ventaja»"]
    return m, lim


def f_fc_cal(ent, params):
    v = ent["valores"]
    c = ev.ece(v["p"], v["o"])
    c["ece_nulo"] = ev.ece_nulo(v["p"], int(params.get("simulaciones", 2000)), int(params.get("semilla_bootstrap", 54321)))
    lim = [] if len(v["p"]) >= 50 else ["menos de 50 pares (p, o): calibración orientativa"]
    return c, lim


def f_score(ent, params):
    from ..herramientas.ht03 import PARAMETROS_POR_DEFECTO
    v = ent["valores"]
    pesos = (params.get("pesos") or PARAMETROS_POR_DEFECTO["pesos"])
    dims = v["dimensiones"]
    tope = 40 if v.get("saturacion_narrativa") else None
    tot = {}
    for k in ("T", "E", "M", "A"):
        if k == "T" and dims.get("T") == "NA":
            tot["T"] = None
            continue
        tot[k] = op.puntuacion_total(dims[k], pesos[k], tope if k == "A" else None)
    prk = params.get("pesos_rk") or PARAMETROS_POR_DEFECTO["pesos_rk"]
    tot["RK"] = op.clave_rk(tot["A"], tot["E"], tot["T"], (prk["A"], prk["E"], prk["T"]))
    return tot, []


IMPLEMENTADAS: dict[str, dict[str, Any]] = {
    "ST-DESC-001": {"fn": _por_serie(_f_desc), "modulo": "MC-01", "version": "1.1", "cifra": "DETERMINISTA", "ri": "RI-NA", "tol": 1e-10},
    "FIN-CAGR-001": {"fn": _por_serie(_f_cagr), "modulo": "MC-01", "version": "1.1", "cifra": "DETERMINISTA", "ri": "RI-NA", "tol": 1e-10},
    "ACC-MOM-001": {"fn": f_momentum, "modulo": "MC-09", "version": "1.0", "cifra": "ESTADISTICA", "ri": "RI-CM", "tol": 1e-10},
    "FX-VOL-001": {"fn": _por_serie(_f_vol), "modulo": "MC-02", "version": "1.1", "cifra": "ESTADISTICA", "ri": "RI-EWMA", "tol": 1e-8},
    "VOL-GARCH-001": {"fn": _por_serie(_f_garch), "modulo": "MC-02", "version": "1.0", "cifra": "ESTADISTICA", "ri": "RI-EWMA", "tol": 1e-6},
    "FX-TREND-001": {"fn": _por_serie(_f_trend), "modulo": "MC-02", "version": "1.1", "cifra": "ESTADISTICA", "ri": "RI-PA", "tol": 1e-6},
    "RISK-DD-001": {"fn": _por_serie(_f_riesgo), "modulo": "MC-07", "version": "1.0", "cifra": "ESTADISTICA", "ri": "RI-NA", "tol": 1e-8},
    "FX-CORR-001": {"fn": f_corr, "modulo": "MC-03", "version": "1.1", "cifra": "ESTADISTICA", "ri": "correlación de ventana larga", "tol": 1e-8},
    "ML-CLUS-001": {"fn": f_clus, "modulo": "MC-06", "version": "1.0", "cifra": "ESTADISTICA", "ri": "agrupación por clase", "tol": 1e-8},
    "FX-CARRY-001": {"fn": f_carry, "modulo": "MC-03", "version": "1.1", "cifra": "DETERMINISTA", "ri": "RI-PA", "tol": 1e-8},
    "CMD-CURVE-001": {"fn": f_roll, "modulo": "MC-09", "version": "1.0", "cifra": "DETERMINISTA", "ri": "pendiente media histórica", "tol": 1e-10},
    "FC-EVAL-001": {"fn": f_fc_eval, "modulo": "MC-10", "version": "1.0", "cifra": "ESTADISTICA", "ri": "referencia de la celda", "tol": 1e-8},
    "FC-CAL-001": {"fn": f_fc_cal, "modulo": "MC-10", "version": "1.0", "cifra": "ESTADISTICA", "ri": "RI-CLI", "tol": 1e-8},
    "SCORE-RK-001": {"fn": f_score, "modulo": "MC-01", "version": "1.0", "cifra": "DETERMINISTA", "ri": "RI-NA", "tol": 0.0},
}


# T-65 (CS-08 de T-53): fichas con código en el ejecutor que no se sirven aunque el Catálogo las diera por IMPLEMENTADO
# (código provisional, sin la prueba que exige la promoción). T-112 rehízo las tres que había (ACC-ERP-001, FX-MOM-001 y
# REI-CAP-001) en `fichas_valoracion` y `fichas_reales`, con sus casos de control: el conjunto queda vacío y se conserva
# para la próxima ficha que tenga código antes de su promoción.
DOCUMENTADAS_CON_CODIGO: frozenset[str] = frozenset()


# T-106 (Motor Fase 1): las 21 fichas V5.0 de IDX, FON, DER, MON y TCV, cada familia en su módulo, con sus casos de control
# (§20 del Catálogo). Las advertencias fijas de una ficha («Supuestos y limitaciones») van en `resultado["advertencias"]`, no
# como limitaciones del cálculo: así el estado SERVED_WITH_LIMITATIONS solo señala problemas de los datos.
def _advertencias_aparte(fn: Callable, advertencias: set) -> Callable:
    def envoltura(ent: dict, params: dict) -> tuple[dict, list[str]]:
        r, lim = fn(ent, params)
        adv = [x for x in lim if x in advertencias]
        if adv:
            r = {**r, "advertencias": list(r.get("advertencias") or []) + adv}
        return r, [x for x in lim if x not in advertencias]
    envoltura.__name__, envoltura.__module__ = fn.__name__, fn.__module__
    return envoltura


CASOS_CONTROL: dict[str, list[dict[str, Any]]] = {}
# T-112 (Motor Fase 2): las fichas P0 y P1 del Catálogo, en cuatro módulos más; las que llevan azar declaran su `semilla`
MODULOS_FASE1 = (fichas_mon_idx, fichas_fon_der, fichas_tcv)
MODULOS_FASE2 = (fichas_series, fichas_riesgo, fichas_valoracion, fichas_reales)
# T-119: las diez fichas P2 (ampliación), las últimas que el Catálogo daba por DOCUMENTADO; ninguna usa azar
MODULOS_P2 = (fichas_p2,)
ACEPTA_SEMILLA: set[str] = set()
for _mod in MODULOS_FASE1 + MODULOS_FASE2 + MODULOS_P2:
    _adv = getattr(_mod, "ADVERTENCIAS", {})
    for _f, _meta in _mod.FICHAS.items():
        IMPLEMENTADAS[_f] = {**_meta, "fn": _advertencias_aparte(_meta["fn"], set(_adv[_f])) if _f in _adv else _meta["fn"]}
        if "semilla" in (getattr(_mod, "PARAMETROS_POR_DEFECTO", {}).get(_f) or {}):
            ACEPTA_SEMILLA.add(_f)
    CASOS_CONTROL.update(_mod.CASOS_CONTROL)

RUTA_CATALOGO = ("04_Motor_conocimiento_y_catalogo", "Catálogo de cálculos del Motor - V5.0.md")
_FILA_CATALOGO = re.compile(r"^\| ([A-Z]+(?:-[A-Z0-9]+)+-\d{3}) \|.*\| (P\d) \| ([^|]+?) \|\s*$", re.MULTILINE)
FASE1 = frozenset(f for m in MODULOS_FASE1 for f in m.CASOS_CONTROL)   # las fichas de T-106
FASE2 = frozenset(f for m in MODULOS_FASE2 for f in m.CASOS_CONTROL)   # las de T-112
P2 = frozenset(f for m in MODULOS_P2 for f in m.CASOS_CONTROL)         # las de T-119
ESTRICTAS = FASE1 | FASE2 | P2   # resultado estricto: el Motor rechaza cualquier cifra no finita
# T-112: BIB-MET-001 solo la piden por CT-09 el Orquestador técnico (paquetes CT-21) y el Evaluador («Supuestos y
# limitaciones» de la ficha); los agentes de conocimiento no son sus clientes
SOLICITANTES_FICHA = {"BIB-MET-001": frozenset({"AG-18", "AG-20"})}
# T-112: AUD-REX-001 no es un cálculo del CT-09, sino la re-ejecución CT-10 (`Motor.reejecutar`); sus casos de control
# re-ejecutan un cálculo de la Fase 1 (CASO_AUD_REX) y artefactos alterados a propósito
SERVICIOS_CT10 = frozenset({"AUD-REX-001"})
CASO_AUD_REX = "IDX-CONC-001"
# QA r01 de T-112, H-08 (QX08): un cálculo cuyos parámetros cambian el resultado, para que la re-ejecución sin los parámetros
# del artefacto no coincida (ficha y número de caso de control de la Fase 1)
CASO_AUD_REX_PARAMETROS = ("FON-DISC-001", 3)


# T-118 (QA r02 de T-112, H-13): una petición con más niveles de anidamiento que estos se rechaza por su forma, antes de
# copiarla o escribirla (un JSON así se puede leer, pero agota la pila al copiarlo). Los casos de control llegan a 9 niveles
# contando la petición [PROPUESTO INC-T118-01, técnico].
PROFUNDIDAD_MAXIMA = 32
_CONTENEDORES = (dict, list, tuple, set, frozenset)


def _demasiado_anidado(x: Any, tope: int = PROFUNDIDAD_MAXIMA) -> bool:
    """¿Hay un contenedor a `tope` niveles o más por debajo de `x`? Recorrido con pila propia: no agota la de Python."""
    pila = [(x, 0)]
    while pila:
        v, nivel = pila.pop()
        if not isinstance(v, _CONTENEDORES):
            continue
        if nivel >= tope:
            return True
        hijos = list(v.keys()) + list(v.values()) if isinstance(v, dict) else v
        pila.extend((h, nivel + 1) for h in hijos if isinstance(h, _CONTENEDORES))
    return False


def _distintas(a: Any, b: Any) -> bool:
    """T-118 (H-13): dos semillas son distintas si no se puede afirmar que son iguales (un array no da un booleano)."""
    try:
        return bool(a != b)
    except (TypeError, ValueError):
        return True


class _ConfiguracionLeida(dict):
    """T-118 (QA r02 de T-112, H-11): la configuración del Motor tal como la recibe una ficha, que apunta en `leidas` las
    secciones (claves de primer nivel) que la ficha consulta, para guardarlas en el artefacto."""

    def __init__(self, cfg: dict | None) -> None:
        super().__init__(cfg or {})
        self.leidas: set[str] = set()

    def __bool__(self) -> bool:   # `parametro` hace `cfg or {}`: una configuración vacía también se registra
        return True

    def __contains__(self, clave: object) -> bool:
        self.leidas.add(str(clave))
        return super().__contains__(clave)

    def __getitem__(self, clave: Any) -> Any:
        self.leidas.add(str(clave))
        return super().__getitem__(clave)

    def get(self, clave: Any, defecto: Any = None) -> Any:
        self.leidas.add(str(clave))
        return super().get(clave, defecto)


def _configuracion_usada(cfg: dict, secciones: Any) -> dict[str, dict[str, Any]]:
    """H-11: de cada sección de la configuración que la ficha ha leído, su `valor` en la configuración del Motor (sin la
    clave si no la trae) y la huella de la misma sección en `config/por_defecto.yaml` (`por_defecto`), que es de donde
    `parametro` toma lo que la del Motor no traiga."""
    out: dict[str, dict[str, Any]] = {}
    for k in sorted(map(str, secciones)):
        out[k] = {"por_defecto": clave_hash(config_por_defecto().get(k))[:16]}
        if k in cfg:
            out[k]["valor"] = copy.deepcopy(dict.get(cfg, k))
    return out


def _raiz(raiz: str | os.PathLike | None = None) -> Path:
    return Path(raiz or os.environ.get("BLOQUE_A_RAIZ") or DIR_EJECUTOR.parent)


@functools.lru_cache(maxsize=8)
def _madurez(ruta: str, _mtime_ns: int) -> tuple[tuple[str, str], ...]:
    try:
        texto = Path(ruta).read_text(encoding="utf-8")
    except (OSError, ValueError):   # QA r01 de T-106, H-05: también bytes que no son UTF-8 (falla cerrado)
        return ()
    # H-06: solo la tabla del índice de fichas (§4), no cualquier fila del documento que se le parezca
    i, j = texto.find("\n## 4."), texto.find("\n## 5.")
    if i < 0 or j < i:
        return ()
    out: dict[str, str] = {}
    for m in _FILA_CATALOGO.finditer(texto[i:j]):
        out.setdefault(m.group(1), m.group(3).strip())
    return tuple(out.items())


def madurez_catalogo(raiz: str | os.PathLike | None = None) -> dict[str, str]:
    """T-106: la madurez de cada ficha según la tabla del índice del Catálogo (§4). Manda el Catálogo (T-65, CS-08): una ficha
    se sirve solo si tiene código y el Catálogo la da por IMPLEMENTADO o VALIDADO. Sin Catálogo legible, ninguna (falla
    cerrado). La lectura se cachea por ruta y fecha de modificación (H-06)."""
    ruta = _raiz(raiz).joinpath(*RUTA_CATALOGO)
    try:
        mtime = ruta.stat().st_mtime_ns
    except OSError:
        return {}
    return dict(_madurez(str(ruta), mtime))


def citable_segun_catalogo(ficha: str, raiz: str | os.PathLike | None = None) -> bool:
    estado = madurez_catalogo(raiz).get(ficha, "")
    return estado.startswith("IMPLEMENTADO") or estado.startswith("VALIDADO")


def servible(ficha: object, raiz: str | os.PathLike | None = None) -> TypeGuard[str]:
    """La ficha tiene código, el Catálogo la da por IMPLEMENTADO (o VALIDADO) y su dependencia opcional está instalada.
    `raiz` es la del paquete (`rutas.raiz_paquete` de la configuración; H-04)."""
    return (isinstance(ficha, str) and ficha in IMPLEMENTADAS and ficha not in DOCUMENTADAS_CON_CODIGO
            and citable_segun_catalogo(ficha, raiz) and (ficha != "VOL-GARCH-001" or garch_disponible()))


def _no_finito(x: Any) -> bool:
    if isinstance(x, dict):
        return any(_no_finito(v) for v in x.values())
    if isinstance(x, (list, tuple)):
        return any(_no_finito(v) for v in x)
    if isinstance(x, (float, np.floating)):
        return not math.isfinite(float(x))
    return False


def garch_disponible() -> bool:
    try:
        import arch  # noqa: F401
        return True
    except ImportError:
        return False


def _limpio(x: Any) -> Any:
    """Convierte a tipos JSON (sin NaN)."""
    if isinstance(x, dict):
        return {str(k): _limpio(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_limpio(v) for v in x]
    if isinstance(x, (np.floating, float)):
        return None if (math.isnan(float(x)) or math.isinf(float(x))) else float(x)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, np.bool_):
        return bool(x)
    return x


class Motor:
    def __init__(self, almacen, proveedor, cfg: dict, contabilidad=None) -> None:
        self.almacen = almacen
        self.proveedor = proveedor
        self.cfg = cfg
        self.contabilidad = contabilidad
        self.raiz = raiz_paquete(cfg)   # QA r01 de T-106, H-04: el Catálogo se lee de la raíz configurada
        self._cache: dict[str, dict] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------------------------
    def _contexto(self, ent: dict, fecha_corte, cfg: dict | None = None) -> dict:
        """QA r01 de T-112 (H-04 y H-07): la ficha recibe la configuración del Motor (no la de por defecto) y la fecha de corte
        de la petición, para leer sus umbrales y no usar datos posteriores. T-118 (H-11): `cfg` es esa configuración con el
        registro de lo que se lee de ella (`_ConfiguracionLeida`) o, en una re-ejecución, la del artefacto."""
        ent["configuracion"] = self.cfg if cfg is None else cfg
        ent["fecha_corte"] = fecha_corte
        return ent

    def _resolver_datos(self, datos: list[dict], fecha_corte) -> tuple[dict, list[dict]]:
        ent = {"series": {}, "series_rol": {}, "valores": {}}
        efectivos = []
        for d in datos:
            if "serie" in d:
                fin = d.get("fin") or fecha_corte
                if fecha_corte is not None and pd.Timestamp(fin) > pd.Timestamp(fecha_corte):
                    raise FugaDeInformacion(f"dato {d['serie']} hasta {fin} posterior a la fecha de corte {fecha_corte}")
                s = self.proveedor.cierres(d["serie"], d.get("inicio"), fin)
                clave = d.get("alias") or d["serie"]
                if d.get("rol") and d["rol"] != "serie":
                    ent["series_rol"][d["rol"]] = s
                else:
                    ent["series"][clave] = s
                efectivos.append({"serie_ht01": d["serie"], "rol": d.get("rol", "serie"), "inicio": str(s.index[0].date()),
                                  "fecha_dato": str(s.index[-1].date()), "n": len(s),
                                  "huella": self.proveedor.huella(d["serie"], d.get("inicio"), fin),
                                  "fuente": f"HT-01:{self.proveedor.nombre}"})
            elif "valores" in d:
                ent["valores"].update(d["valores"])
                # T-112 (AUD-REX-001): el artefacto guarda los valores en línea para poder re-ejecutarlo (CT-10); su huella los
                # comprueba al reconstruir
                efectivos.append({"valor": copy.deepcopy(d["valores"]), "claves": sorted(d["valores"]),
                                  "huella": clave_hash(d["valores"])[:16]})
        return ent, efectivos

    def _error_de_forma(self, peticion: Any) -> str | None:
        """QA r02 de T-106, H-15: la forma de la petición se comprueba antes de nada; una petición mal formada se rechaza
        (DATOS_INCOHERENTES, paso 1 del Motor: esquema) y queda en RC, en vez de lanzar una excepción al llamador."""
        if not isinstance(peticion, dict):
            return "la petición no es un objeto"
        if _demasiado_anidado(peticion):   # T-118 (H-13): antes de copiar, serializar o escribir nada de ella
            return f"anidamiento excesivo (más de {PROFUNDIDAD_MAXIMA} niveles)"
        op_ = peticion.get("operacion")
        ficha = op_.get("ficha_id") if isinstance(op_, dict) else op_
        if not isinstance(ficha, str):
            return "la operación no es un identificador de ficha"
        if peticion.get("parametros") is not None and not isinstance(peticion["parametros"], dict):
            return "«parametros» no es un objeto"
        planes = parametro(self.cfg, "uc.motor_por_plan")
        if not isinstance(peticion.get("plan", "PLAN_MIN"), str):   # T-113 (H-22 de T-108): una lista no es hashable
            return "«plan» no es un texto"
        try:   # T-113 (H-22): lo que entra en la clave de la caché y en el RC tiene que poder serializarse
            clave_hash(peticion.get("parametros"), peticion.get("perfil"), peticion.get("clase"), peticion.get("semilla"))
        except (TypeError, ValueError, RecursionError) as exc:
            return f"«parametros», «perfil», «clase» o «semilla» no serializables ({type(exc).__name__})"
        # T-118 (H-13): `clase` y `perfil` se evalúan como condición más abajo; un array de numpy no tiene valor de verdad
        if peticion.get("clase") is not None and not isinstance(peticion["clase"], str):
            return "«clase» no es un texto"
        if peticion.get("perfil") is not None and not isinstance(peticion["perfil"], (str, list, tuple)):
            return "«perfil» no es un texto ni una lista"
        if peticion.get("plan", "PLAN_MIN") not in planes:
            return f"plan desconocido ({str(peticion.get('plan'))[:40]}); admitidos: {sorted(planes)}"
        if peticion.get("fecha_corte") is not None:
            try:
                if pd.isna(pd.Timestamp(peticion["fecha_corte"])):
                    return "«fecha_corte» vacía"
            except (TypeError, ValueError, OverflowError):
                return f"«fecha_corte» ilegible ({str(peticion['fecha_corte'])[:40]})"
        datos = peticion.get("datos")
        if datos is not None and not (isinstance(datos, list) and all(isinstance(d, dict) for d in datos)):
            return "«datos» no es una lista de objetos"
        for d in datos or []:
            if "serie" in d and not isinstance(d["serie"], str):
                return "una «serie» de «datos» no es un identificador"
            if "valores" in d and not isinstance(d["valores"], dict):
                return "unos «valores» de «datos» no son un objeto"
        return None

    def servir(self, peticion: dict, solicitante: str, run_id: str | None = None, msg_id: str | None = None) -> dict:
        forma = self._error_de_forma(peticion)
        if forma:
            op_ = peticion.get("operacion") if isinstance(peticion, dict) else None
            f_ = op_.get("ficha_id") if isinstance(op_, dict) else op_
            f_ = f_ if isinstance(f_, str) else None
            base_ = {"calc_id": None, "contrato": "CT-09", "msg_id": msg_id, "run_id": run_id, "solicitante": solicitante,
                     "operacion": {"method_id": f_, "ficha_id": f_, "ficha_version": None, "catalog_version": CATALOG_VERSION,
                                   "op_sin_ficha": f_ not in FICHAS_CATALOGO},
                     "madurez_metodo": "IMPLEMENTADO" if f_ in IMPLEMENTADAS else "DESCONOCIDA", "cache_hit": False}
            return self._rechazo(base_, "DATOS_INCOHERENTES", f"petición mal formada: {forma}")
        ficha = (peticion.get("operacion") or {}).get("ficha_id") if isinstance(peticion.get("operacion"), dict) \
            else peticion.get("operacion")
        params = dict(peticion.get("parametros") or {})
        if peticion.get("clase"):
            params.setdefault("clase", peticion["clase"])
        semilla_p, semilla_pet = params.get("semilla"), peticion.get("semilla")
        # sin conjunto: puede no ser hashable; T-118 (H-13): ni comparable (un array de numpy), y entonces son dos
        dos_semillas = semilla_p is not None and semilla_pet is not None and _distintas(semilla_p, semilla_pet)
        if ficha in ACEPTA_SEMILLA and peticion.get("semilla") is not None:   # T-112: la semilla de la petición llega a la ficha
            params.setdefault("semilla", peticion["semilla"])
        fecha_corte = peticion.get("fecha_corte") or (str(self.proveedor.as_of.date()) if self.proveedor.as_of is not None else None)
        plan = peticion.get("plan", "PLAN_MIN")
        base = {"calc_id": None, "contrato": "CT-09", "msg_id": msg_id, "run_id": run_id, "solicitante": solicitante,
                "operacion": {"method_id": ficha, "ficha_id": ficha, "ficha_version": None, "catalog_version": CATALOG_VERSION,
                              "op_sin_ficha": ficha not in FICHAS_CATALOGO},
                "perfil": peticion.get("perfil") or ["TRANSVERSAL"], "clase": peticion.get("clase"),
                "horizonte": peticion.get("horizonte"), "modo": peticion.get("modo", "SYNC_CALC"), "plan": plan,
                "prioridad": peticion.get("prioridad", "MATERIAL"), "parametros": params,
                "semilla": params.get("semilla", peticion.get("semilla")), "as_of": fecha_corte, "fecha_limite_informacion": fecha_corte,
                "madurez_metodo": "IMPLEMENTADO", "cache_hit": False}
        uc = float(parametro(self.cfg, f"uc.motor_por_plan.{plan}"))   # QA r01 de T-65, H-05: sin respaldo 0,02
        if dos_semillas:   # QA r01 de T-112, H-05: el artefacto registra la semilla que se usa; dos distintas no se adivinan
            return self._rechazo(base, "DATOS_INCOHERENTES", "dos semillas distintas en la petición (`semilla` y `parametros.semilla`)", uc=uc)
        # 1) Ficha
        if not servible(ficha, self.raiz):
            motivo = "METODO_NO_IMPLEMENTADO" if ficha in FICHAS_CATALOGO else "OPERACION_SIN_FICHA"
            alt = ALTERNATIVAS.get(ficha)
            alt = alt if alt and servible(alt, self.raiz) else None   # nunca se ofrece como alternativa una ficha que tampoco se sirve
            if ficha == "VOL-GARCH-001" and citable_segun_catalogo(ficha, self.raiz) and not garch_disponible():
                detalle = "Ficha VOL-GARCH-001: falta la dependencia opcional `arch` en el entorno"   # H-12
            elif ficha in SERVICIOS_CT10:   # T-112
                detalle = f"Ficha {ficha}: es la re-ejecución independiente y se pide por CT-10, no por CT-09"
            elif ficha in DOCUMENTADAS_CON_CODIGO:
                detalle = f"Ficha {ficha} con código provisional, sin la promoción de sus casos de control: no entrega cifras citables"
            elif ficha in IMPLEMENTADAS:
                madurez = madurez_catalogo(self.raiz).get(ficha) or "sin Catálogo legible"
                detalle = f"Ficha {ficha} con código pero «{madurez}» en el Catálogo: no entrega cifras citables"
            else:
                detalle = f"Ficha {ficha} no implementada en el ejecutor"
            return self._rechazo(base, motivo, detalle + (f"; alternativa: {alt}" if alt else ""), alternativa=alt, uc=uc)
        if ficha in SOLICITANTES_FICHA and not (isinstance(solicitante, str) and solicitante in SOLICITANTES_FICHA[ficha]):   # H-06
            return self._rechazo(base, "CANAL_NO_AUTORIZADO", f"{ficha} solo la piden {', '.join(sorted(SOLICITANTES_FICHA[ficha]))} "
                                 f"(«Supuestos y limitaciones» de la ficha); {solicitante} no es cliente de esta ficha", uc=uc)
        meta = IMPLEMENTADAS[ficha]
        base["operacion"]["ficha_version"] = meta["version"]
        base["modulos"] = [meta["modulo"]]
        # 2) Datos (guardia anti-fuga)
        try:
            ent, efectivos = self._resolver_datos(peticion.get("datos") or [], fecha_corte)
            lectura = _ConfiguracionLeida(self.cfg)   # T-118 (H-11): lo que la ficha lea de la configuración va al artefacto
            self._contexto(ent, fecha_corte, lectura)
        except FugaDeInformacion as e:
            return self._rechazo(base, "FUGA_DE_INFORMACION", str(e), uc=uc)
        except (DatosNoDisponibles, KeyError) as e:
            return self._rechazo(base, "DATOS_NO_DISPONIBLES", str(e), uc=uc)
        except (TypeError, ValueError, OverflowError, RecursionError, MemoryError) as e:
            # H-15: fechas de una serie ilegibles. T-118 (H-13): tampoco escapa la copia de unos valores que agote la pila
            return self._rechazo(base, "DATOS_INCOHERENTES", f"datos mal formados ({type(e).__name__}: {str(e)[:200]})", uc=uc)
        # QA r02 de T-112 (grupo V): la fecha de corte entra en la clave; si no, una petición con un corte anterior se serviría
        # desde la caché de otra con un corte posterior (H-07)
        clave = clave_hash(ficha, meta["version"], efectivos, params, base["semilla"], base["perfil"], fecha_corte)
        base["clave_idempotencia"] = clave
        with self._lock:
            previo = self._cache.get(clave)
        if previo:
            e = self.almacen.escribir("RC", "AG-13", {**base, "tipo_entrada": "CACHE_HIT", "calc_id": self.almacen.nuevo_id("CALC"),
                                                      "calc_original": previo["calc_id"], "cache_hit": True,
                                                      "estado": previo["estado"], "datos": efectivos, "consumo_uc": 0.0})
            r = dict(previo)
            r["cache_hit"] = True
            r["calc_id_cache"] = e["calc_id"]
            return r
        # 3) Cálculo con doble pasada (determinismo) y segunda vía donde la ficha la tiene
        try:
            resultado, limitaciones = meta["fn"](ent, params)
            resultado2, _ = meta["fn"](ent, params)
        except op.ErrorFicha as e:
            return self._rechazo(base, "DATOS_INSUFICIENTES", str(e), uc=uc)
        except NotImplementedError as e:
            return self._rechazo(base, "METODO_NO_IMPLEMENTADO", str(e), uc=uc)
        except (ValueError, TypeError, ArithmeticError, KeyError, IndexError, AttributeError, np.linalg.LinAlgError, MemoryError,
                RecursionError) as e:
            # QA r01 de T-106, H-02: una entrada que la ficha no valida no tumba el CT-09; se rechaza y queda en RC. QA r01 de
            # T-112, H-01: tampoco una que agota la memoria o la pila (las fichas tienen además topes de tamaño)
            return self._rechazo(base, "DATOS_INSUFICIENTES", f"{ficha}: entrada no válida ({type(e).__name__}: {str(e)[:200]})", uc=uc)
        if ficha in ESTRICTAS and (_no_finito(resultado) or _no_finito(resultado2)):
            return self._rechazo(base, "DATOS_INSUFICIENTES", f"{ficha}: el cálculo da cifras no finitas con estos datos", uc=uc)
        resultado, resultado2 = _limpio(resultado), _limpio(resultado2)
        identico = resultado == resultado2
        calc_id = self.almacen.nuevo_id("CALC")
        estado = "SERVED_WITH_LIMITATIONS" if limitaciones else "SERVED"
        entrada = {**base, "tipo_entrada": "SERVICIO", "calc_id": calc_id, "estado": estado, "datos": efectivos,
                   "resultado": {"forma": "TABLA", "payload": resultado}, "clase_cifra": meta["cifra"],
                   "incertidumbre": {"tipo": "IC" if meta["cifra"] == "ESTADISTICA" else None},
                   "referencia_ingenua": {"tipo": meta["ri"]},
                   "artefacto": {"code_ref": f"{meta['fn'].__module__} · {meta['fn'].__name__}",
                                 "inputs_effective": efectivos, "transformations": "rendimientos simples salvo ficha",
                                 "rounding_policy": "sin redondeo intermedio; JSON float64",
                                 # T-118 (H-11): la re-ejecución (CT-10) usa esta configuración, no la vigente
                                 "configuracion_usada": _configuracion_usada(self.cfg, lectura.leidas)},
                   "verificacion_interna": {"identity_checks": "doble pasada idéntica" if identico else "DIFERENCIA ENTRE PASADAS",
                                            "second_path": "según ficha (campo segunda_via_* en el resultado)"},
                   "consumo_uc": uc, "limitaciones": limitaciones or ["ninguna conocida (ficha implementada, no validada)"],
                   "incidencias": [] if identico else ["no determinismo detectado"]}
        self.almacen.escribir("RC", "AG-13", entrada)
        if self.contabilidad:
            self.contabilidad.cargar_motor(run_id, uc)
        out = {"estado": estado, "calc_id": calc_id, "artefacto_id": calc_id, "resultado": resultado,
               "clase_cifra": meta["cifra"], "limitaciones": limitaciones, "referencia_ingenua": meta["ri"],
               "informe_calidad_datos": efectivos, "cache_hit": False}
        with self._lock:
            self._cache[clave] = out
        return out

    def _rechazo(self, base: dict, motivo: str, detalle: str, alternativa: str | None = None, uc: float = 0.0) -> dict:
        calc_id = self.almacen.nuevo_id("CALC")
        e = {**base, "tipo_entrada": "RECHAZO", "calc_id": calc_id, "estado": "REJECTED", "motivo_rechazo": motivo,
             "detalle": detalle, "alternativa": alternativa, "madurez_metodo": "DOCUMENTADO" if motivo == "METODO_NO_IMPLEMENTADO" else ("DESCONOCIDA" if motivo == "OPERACION_SIN_FICHA" else base.get("madurez_metodo")),
             "consumo_uc": 0.0, "limitaciones": [detalle], "incidencias": []}
        self.almacen.escribir("RC", "AG-13", e)
        return {"estado": "RECHAZADO", "motivo": motivo, "detalle": detalle, "calc_id": calc_id, "alternativa": alternativa}

    # ------------------------------------------------------------------------------------
    def _casos_aud_rex(self) -> list[dict]:
        """T-112: casos de control de AUD-REX-001 (CT-10), en un Registro de cálculos aparte para no ensuciar el del run.
        Re-ejecuta un cálculo servido (SI, con doble pasada) y artefactos alterados a propósito: datos distintos, una
        diferencia dentro de la tolerancia, una fuera de ella y un CT-10 sin motivo."""
        import tempfile

        from ..almacen import Almacen
        res = []
        with tempfile.TemporaryDirectory() as tmp:
            m = Motor(Almacen(Path(tmp)), self.proveedor, self.cfg)
            base = CASO_AUD_REX
            caso = CASOS_CONTROL[base][0]
            r = m.servir({"operacion": base, "datos": copy.deepcopy(caso.get("datos") or []),
                          "parametros": dict(caso.get("parametros") or {}), "fecha_corte": None}, "AG-13")
            if r.get("estado") not in ("SERVED", "SERVED_WITH_LIMITATIONS"):
                return [{"nombre": "cálculo base servido", "superado": False, "detalle": str(r)[:300]}]
            orig = m.almacen.estado("RC")[r["calc_id"]]
            tol = IMPLEMENTADAS[base]["tol"]

            def alterado(cambio) -> str:
                e = copy.deepcopy(orig)
                cambio(e)
                e["calc_id"] = m.almacen.nuevo_id("CALC")
                m.almacen.escribir("RC", "AG-13", e)
                return e["calc_id"]

            def primer_numero(x: Any) -> tuple[Any, Any] | None:
                for k, v in (x.items() if isinstance(x, dict) else enumerate(x) if isinstance(x, list) else []):
                    if isinstance(v, float) and v != 0 and math.isfinite(v):
                        return x, k
                    hallado = primer_numero(v)
                    if hallado:
                        return hallado
                return None

            def escala(f: float):
                def cambio(e):
                    sitio = primer_numero(e["resultado"]["payload"])
                    if sitio is None:
                        raise AssertionError("el resultado base no tiene cifras con las que probar")
                    contenedor, clave = sitio
                    contenedor[clave] = contenedor[clave] * (1 + f)
                return cambio

            def otro_dato(e):
                d = next(x for x in e["datos"] if isinstance(x.get("valor"), dict))
                d["valor"]["_alterado_t112"] = 1

            pruebas = [("re-ejecución de un cálculo servido: coincide SI", lambda: r["calc_id"], ("SI", None)),
                       ("datos en línea alterados: NO y DATOS_DISTINTOS", lambda: alterado(otro_dato), ("NO", "DATOS_DISTINTOS")),
                       ("diferencia por debajo de la tolerancia: DENTRO_TOLERANCIA", lambda: alterado(escala(tol / 10)),
                        ("DENTRO_TOLERANCIA", None)),
                       ("diferencia por encima de la tolerancia: NO", lambda: alterado(escala(tol * 1e3)), ("NO", "ERROR_ORIGINAL"))]
            for nombre, calc, esperado in pruebas:
                try:
                    out = m.reejecutar(calc(), "casos de control de AUD-REX-001")
                    ok = (out["coincide"], out["categoria"]) == esperado
                    res.append({"nombre": nombre, "superado": ok, "detalle": None if ok else f"{out['coincide']}/{out['categoria']}"})
                except Exception as exc:  # noqa: BLE001 — un caso que falla por cualquier motivo no se supera
                    res.append({"nombre": nombre, "superado": False, "detalle": f"{type(exc).__name__}: {exc}"[:300]})
            f_p, i_p = CASO_AUD_REX_PARAMETROS
            caso_p = CASOS_CONTROL[f_p][i_p]
            try:
                rp = m.servir({"operacion": f_p, "datos": copy.deepcopy(caso_p.get("datos") or []),
                               "parametros": dict(caso_p.get("parametros") or {}), "fecha_corte": None}, "AG-13")
                out = m.reejecutar(rp["calc_id"], "casos de control de AUD-REX-001")
                ok = out["coincide"] == "SI"
                res.append({"nombre": "re-ejecución con los parámetros del artefacto (no los de por defecto): SI", "superado": ok,
                            "detalle": None if ok else f"{out['coincide']}/{out['categoria']}"})
            except Exception as exc:  # noqa: BLE001 — un caso que falla por cualquier motivo no se supera
                res.append({"nombre": "re-ejecución con los parámetros del artefacto (no los de por defecto): SI", "superado": False,
                            "detalle": f"{type(exc).__name__}: {exc}"[:300]})
            try:
                m.reejecutar(r["calc_id"], " ")
                res.append({"nombre": "CT-10 sin motivo: imposible", "superado": False, "detalle": "se re-ejecutó sin motivo"})
            except ValueError:
                res.append({"nombre": "CT-10 sin motivo: imposible", "superado": True, "detalle": None})
        return res

    def verificar_casos_control(self, fichas: list[str] | None = None, run_id: str | None = None) -> dict[str, dict]:
        """T-106 (§20.2 del Catálogo: «Paso a IMPLEMENTADO: casos de control superados en el entorno de ejecución y registrados
        en el Registro de cálculos»). Ejecuta los casos de control de cada ficha (dos pasadas, que deben coincidir) y escribe
        una entrada CASOS_CONTROL en RC por ficha. No depende de la madurez del Catálogo: es lo que permite promoverla."""
        out: dict[str, dict] = {}
        for ficha in sorted(fichas or (set(CASOS_CONTROL) | SERVICIOS_CT10)):
            meta, casos = IMPLEMENTADAS.get(ficha), CASOS_CONTROL.get(ficha) or []
            res = self._casos_aud_rex() if ficha in SERVICIOS_CT10 else []
            for caso in casos:
                try:
                    ent, _ = self._resolver_datos(caso.get("datos") or [], None)
                    self._contexto(ent, caso.get("fecha_corte"))
                    params = dict(caso.get("parametros") or {})
                    r1, _ = meta["fn"](ent, dict(params)) if meta else ({}, [])
                    r2, _ = meta["fn"](ent, dict(params)) if meta else ({}, [])
                    ok, detalle = bool(meta) and bool(caso["comprobar"](r1)) and _limpio(r1) == _limpio(r2), None
                except Exception as exc:  # noqa: BLE001 — un caso que falla por cualquier motivo no se supera (falla cerrado)
                    ok, detalle = False, f"{type(exc).__name__}: {exc}"[:300]
                res.append({"nombre": caso.get("nombre"), "superado": ok, "detalle": detalle})
            superados = bool(res) and all(x["superado"] for x in res)
            reg = {"tipo_entrada": "CASOS_CONTROL", "calc_id": self.almacen.nuevo_id("CALC"), "contrato": "CT-10", "run_id": run_id,
                 "solicitante": "AG-13", "estado": "SERVED" if superados else "REJECTED",
                 "operacion": {"method_id": ficha, "ficha_id": ficha, "ficha_version": (meta or {}).get("version"),
                               "catalog_version": CATALOG_VERSION, "op_sin_ficha": ficha not in FICHAS_CATALOGO},
                 "casos_control": res, "superados": superados, "madurez_catalogo": madurez_catalogo(self.raiz).get(ficha),
                 "consumo_uc": 0.0}
            self.almacen.escribir("RC", "AG-13", reg)
            out[ficha] = {"superados": superados, "casos": res, "calc_id": reg["calc_id"]}
        return out

    # ------------------------------------------------------------------------------------
    def reejecutar(self, calc_id: str, motivo: str, solicitante: str = "AG-18") -> dict:
        """CT-10 (AUD-REX-001, MC-08): recalcula en aislamiento con las entradas del artefacto y compara con la tolerancia de
        la ficha. T-112: sin motivo o sin artefacto completo es IMPOSIBLE (no se reconstruye por inferencia); los valores en
        línea se toman del artefacto y se comprueba su huella; doble pasada del recálculo; `coincide` es SI si no hay
        diferencia, DENTRO_TOLERANCIA si la hay pero no supera la tolerancia (esquema del RC V2.0) y NO en otro caso."""
        if not isinstance(motivo, str) or not motivo.strip():
            raise ValueError("CT-10 sin motivo: re-ejecución imposible")
        orig = self.almacen.estado("RC").get(calc_id)
        if not orig or orig.get("tipo_entrada") != "SERVICIO":
            raise KeyError(f"{calc_id} no es un servicio del Registro de cálculos")
        ficha = orig["operacion"]["ficha_id"]
        if ficha not in IMPLEMENTADAS:
            raise KeyError(f"{calc_id}: la ficha {ficha} ya no tiene manejador: re-ejecución imposible")
        datos, huellas_en_linea = [], []
        for d in orig["datos"]:
            if "serie_ht01" in d:
                datos.append({"serie": d["serie_ht01"], "inicio": d["inicio"], "fin": d["fecha_dato"], "rol": d["rol"]})
            elif "valor" in d:
                if not isinstance(d["valor"], dict):   # artefactos anteriores a T-112: solo «en línea», sin los valores
                    raise NotImplementedError("Artefacto sin los valores en línea: re-ejecución imposible")
                datos.append({"valores": copy.deepcopy(d["valor"])})
                huellas_en_linea.append(clave_hash(d["valor"])[:16] == d.get("huella"))
        ent, efectivos = self._resolver_datos(datos, orig["as_of"])
        # T-118 (H-11): la ficha se re-ejecuta con las secciones de la configuración que guardó el artefacto (las «entradas
        # del artefacto» incluyen los números de configuración que la ficha usó); lo que el artefacto no guarde, de la vigente
        artefacto = orig.get("artefacto") if isinstance(orig.get("artefacto"), dict) else {}
        registrada = artefacto.get("configuracion_usada") if isinstance(artefacto.get("configuracion_usada"), dict) else None
        cfg_artefacto = dict(self.cfg)
        for k, reg in (registrada or {}).items():
            if isinstance(reg, dict) and "valor" in reg:
                cfg_artefacto[k] = copy.deepcopy(reg["valor"])
            else:
                cfg_artefacto.pop(k, None)
        lectura = _ConfiguracionLeida(cfg_artefacto)
        fallo = None
        try:
            nuevo, _ = IMPLEMENTADAS[ficha]["fn"](self._contexto(copy.deepcopy(ent), orig["as_of"], lectura),
                                                  copy.deepcopy(orig["parametros"]))
            nuevo2, _ = IMPLEMENTADAS[ficha]["fn"](self._contexto(copy.deepcopy(ent), orig["as_of"], lectura),
                                                   copy.deepcopy(orig["parametros"]))
            nuevo, nuevo2 = _limpio(nuevo), _limpio(nuevo2)
        except (op.ErrorFicha, NotImplementedError, ValueError, TypeError, ArithmeticError, KeyError, IndexError,
                AttributeError, np.linalg.LinAlgError, MemoryError, RecursionError) as exc:
            # T-118 (H-14): la ficha rechaza las entradas del artefacto (p. ej. un tamaño servido antes de una cota): la
            # re-ejecución queda registrada como fallida, no se escapa como excepción
            fallo = f"{type(exc).__name__}: {str(exc)[:300]}"
            nuevo = nuevo2 = None
        tol = IMPLEMENTADAS[ficha]["tol"]
        difs = [] if fallo else _comparar(orig["resultado"]["payload"], nuevo, tol)
        exacto = not fallo and orig["resultado"]["payload"] == nuevo
        mismas = all(huellas_en_linea) and [a.get("huella") for a in orig["datos"]] == [b.get("huella") for b in efectivos]
        version = IMPLEMENTADAS[ficha]["version"] == orig["operacion"].get("ficha_version")
        # H-11: secciones que la re-ejecución ha leído y el artefacto no guarda, y secciones guardadas que ya no son las vigentes
        sin_registro = sorted(lectura.leidas - set(registrada or {}))
        vigente = _configuracion_usada(self.cfg, registrada or {})
        cambiadas = sorted(k for k, reg in (registrada or {}).items() if clave_hash(reg) != clave_hash(vigente[k]))
        cfg_nota = None
        if fallo:
            coincide, categoria = "NO", "ERROR_REEJECUCION"
        elif nuevo != nuevo2:
            coincide, categoria = "NO", "NO_DETERMINISMO"
        elif not mismas:
            coincide, categoria = "NO", "DATOS_DISTINTOS"
        elif difs and (sin_registro or cambiadas):
            # H-11: no se puede culpar al original si la configuración con que se calculó no consta o ya no es la vigente
            coincide, categoria = "NO", "CONVENCION_DISTINTA"
            cfg_nota = ("la configuración con que se calculó no es la vigente o no consta en el artefacto (secciones "
                        f"{', '.join(sorted(set(sin_registro) | set(cambiadas)))})")
        elif difs:
            # recálculo determinista con los mismos datos: si la versión de la ficha es la misma, el que difiere es el original
            coincide, categoria = "NO", ("ERROR_ORIGINAL" if version else "CONVENCION_DISTINTA")
        else:
            coincide, categoria = ("SI" if exacto else "DENTRO_TOLERANCIA"), None
        if fallo:
            diagnostico = f"ERROR_REEJECUCION: la ficha no admite las entradas del artefacto ({fallo})"
        elif cfg_nota:
            diagnostico = f"{categoria}: {cfg_nota}"
        else:
            diagnostico = {"SI": "coincidencia exacta", "DENTRO_TOLERANCIA": "diferencias dentro de la tolerancia de la ficha"}.get(
                coincide, f"{categoria}: ver diferencias")
        e = {"tipo_entrada": "REEJECUCION", "calc_id": self.almacen.nuevo_id("CALC"), "contrato": "CT-10",
             "solicitante": solicitante, "operacion": orig["operacion"], "estado": "SERVED", "as_of": orig["as_of"],
             "reejecucion": {"calc_original": calc_id, "motivo": motivo, "aislamiento": "CONFIRMADO", "tolerancia": tol,
                             "coincide": coincide, "diferencias": difs[:20], "categoria": categoria,
                             "diagnostico": diagnostico,
                             "doble_pasada": not fallo and nuevo == nuevo2, "version_ficha": IMPLEMENTADAS[ficha]["version"],
                             "configuracion": {"origen": "artefacto" if registrada is not None else "vigente (el artefacto no la guarda)",
                                               "distinta_de_la_vigente": cambiadas, "sin_registro": sin_registro}},
             "datos": efectivos, "consumo_uc": 0.0, "madurez_metodo": "IMPLEMENTADO"}
        self.almacen.escribir("RC", "AG-13", e)
        return {"coincide": coincide, "categoria": categoria, "diferencias": difs, "calc_id": e["calc_id"],
                "diagnostico": diagnostico}


def _comparar(a: Any, b: Any, tol: float, ruta: str = "") -> list[str]:
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in set(a) | set(b):
            out += _comparar(a.get(k), b.get(k), tol, f"{ruta}.{k}")
        return out
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return [f"{ruta}: longitudes distintas"]
        out = []
        for i, (x, y) in enumerate(zip(a, b)):
            out += _comparar(x, y, tol, f"{ruta}[{i}]")
        return out
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        den = max(abs(a), abs(b), 1e-12)
        return [] if abs(a - b) / den <= max(tol, 1e-12) else [f"{ruta}: {a} ≠ {b}"]
    return [] if a == b else [f"{ruta}: {a!r} ≠ {b!r}"]
