"""Servicio del Motor (AG-13) en el ejecutor: despacho CT-09, re-ejecución CT-10 y Registro de cálculos.

Cada servicio escribe en RC su artefacto reproducible: operación y versión de ficha, datos efectivos
(símbolo, rango, huella), parámetros, semilla, fecha de corte, resultado y clave de idempotencia
(hash de todo lo anterior). Una petición idéntica se sirve desde caché. Las fichas del Catálogo no
implementadas se rechazan con `METODO_NO_IMPLEMENTADO` (y la alternativa que declara la ficha); las fichas del
Catálogo V5.0 retiradas en el Catálogo Forex, con `FUERA_DE_CATALOGO` y la ficha cambiaria más próxima.
"""
from __future__ import annotations

import inspect
import math
import threading
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from ..herramientas.ht01_datos import DatosNoDisponibles, FugaDeInformacion
from ..herramientas.ht06_indice import clave_hash
from . import evaluacion as ev
from . import operaciones as op

CATALOG_VERSION = "FX-1.0"
# Las 60 fichas del índice del Catálogo de cálculos del Motor - Bloque A Forex V1.0 (sección 4)
FICHAS_CATALOGO = [
    "FX-TREND-001", "FX-BRK-001", "FX-STL-001", "FX-VOL-001", "FX-REGIME-001", "FX-COINT-001", "FX-CORR-001",
    "ST-DESC-001", "ST-INF-001", "FIN-CAGR-001", "BIB-MET-001", "SIM-MC-001", "RISK-VAR-001", "ML-CAL-001",
    "AUD-REX-001", "FC-CAL-001", "BT-DSR-001", "BT-PBO-001", "BT-VAR-001", "VOL-GARCH-001", "ML-PRED-001",
    "DEC-VOI-001", "SCORE-RK-001", "FC-EVAL-001", "SCN-H-001", "REG-HMM-001", "ML-CLUS-001", "RISK-DD-001",
    "MON-EXP-001", "FX-CONV-001", "FX-SETL-001", "FX-FWD-001", "FX-TR-001", "FX-CARRY-001", "FX-CIP-001",
    "FX-UIP-001", "FX-PPP-001", "FX-PPA-001", "FX-BEER-001", "FX-FEER-001", "FX-REER-001", "FX-RDIFF-001",
    "FX-TOT-001", "FX-TAYLOR-001", "FX-SURP-001", "FX-POS-001", "FX-BASKET-001", "FX-NDF-001", "FX-MOM-001",
    "FX-FACT-001", "FX-GK-001", "FX-RR-001", "FX-TERM-001", "FX-VRP-001", "FX-RND-001", "FX-TAIL-001",
    "FX-PEG-001", "FX-PASS-001", "FX-RW-001", "FX-BT-001",
]
# Fichas del Catálogo V5.0 del Bloque A general retiradas en el Catálogo Forex (sección 10) y su sustituta
RETIRADAS = {"ACC-MOM-001": "FX-MOM-001", "ACC-FACT-001": "FX-FACT-001", "DER-OPT-001": "FX-GK-001",
             "DER-SKEW-001": "FX-RR-001", "DER-TERM-001": "FX-TERM-001", "DER-VRP-001": "FX-VRP-001",
             "DER-ROLL-001": "FX-FWD-001", "MON-YLD-001": "FX-FWD-001", "MON-REAL-001": "FX-CARRY-001",
             "TEM-DIFF-001": "FX-PASS-001", "ACC-VAL-001": None, "ACC-ERP-001": None, "CMD-CURVE-001": None,
             "REI-CAP-001": None}
# Alternativa implementada que declara cada ficha DOCUMENTADO (o la más próxima del núcleo)
ALTERNATIVAS = {"REG-HMM-001": "FX-TREND-001", "FX-REGIME-001": "FX-TREND-001", "RISK-VAR-001": "RISK-DD-001",
                "SCN-H-001": "FX-VOL-001", "ML-PRED-001": "FX-MOM-001", "FX-FACT-001": "FX-MOM-001",
                "FX-TR-001": "FX-CARRY-001", "FX-NDF-001": "FX-FWD-001", "FX-CIP-001": "FX-FWD-001",
                "FX-RDIFF-001": "FX-CARRY-001", "FX-BEER-001": "FX-PPP-001", "FX-REER-001": "FX-PPP-001",
                "FX-TAIL-001": "RISK-DD-001", "FX-PEG-001": "RISK-DD-001", "FX-BT-001": "FX-RW-001",
                "BT-DSR-001": "FC-EVAL-001", "FX-POS-001": "ST-DESC-001", "FX-BASKET-001": "FIN-CAGR-001",
                "FX-VRP-001": "FX-VOL-001", "FX-TERM-001": "FX-VOL-001"}


def _sesiones_anuales(params: Dict) -> int:
    return 252


def _por_serie(fn: Callable[[pd.Series, Dict], Dict]) -> Callable:
    """Aplica una función a cada serie; los fallos por símbolo se anotan como limitaciones."""
    def envoltura(ent: Dict, params: Dict) -> Tuple[Dict, List[str]]:
        tabla, lim = {}, []
        for s, serie in ent["series"].items():
            try:
                tabla[s] = fn(serie, {**params, "_simbolo": s})
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
    sym = p.get("_simbolo")
    return op.escala_riesgo(s, _sesiones_anuales(p), liquidez_limitada=sym in (p.get("liquidez_limitada") or []),
                            suelo_regimen=sym in (p.get("suelo_regimen") or []),
                            sentido=-1 if sym in (p.get("sentido_bajista") or []) else 1,
                            dias_liquidacion=p.get("dias_liquidacion"))


def f_fx_mom(ent, params):
    """FX-MOM-001 v2.0: 12-1, señal TSMOM (signo de 12 meses) y rango transversal dentro del universo declarado."""
    res, lim = _por_serie(_f_mom)(ent, params)
    rangos = op.rango_transversal({k: v["momentum"] for k, v in res["tabla"].items()})
    for k, v in rangos.items():
        res["tabla"][k]["percentil_transversal"] = v["percentil"]
        res["tabla"][k]["z_transversal"] = v["z"]
        vol = res["tabla"][k].get("volatilidad_anual")
        res["tabla"][k]["senal_tsmom_escalada"] = (res["tabla"][k]["senal_tsmom"] * 0.10 / vol) if vol else None
    if len(rangos) < 10:
        lim.append(f"universo de {len(rangos)} miembros (< 10): rango transversal orientativo")
    lim.append("rentabilidad de contado (sin carry): la versión en rentabilidad total de FX-TR-001 está DOCUMENTADO")
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
    """FX-CARRY-001 v2.0: núcleo v1.1 (diferencial y descomposición realizada) y carry de la exposición con signo,
    carry ajustado por volatilidad (realizada si no se aporta implícita, declarado) y equilibrio."""
    v = ent["valores"]
    spot = next(iter(ent["series"].values())) if ent["series"] else None
    if spot is not None:
        s0, s1 = float(spot.iloc[0]), float(spot.iloc[-1])
        anios = max((spot.index[-1] - spot.index[0]).days / 365.25, 0.0)
    else:
        s0, s1, anios = float(v["spot_ini"]), float(v["spot_fin"]), float(v["anios"])
    out = op.carry_divisas(float(v["tipo_base"]), float(v["tipo_cotizada"]), s0, s1, anios)
    lim = []
    vol = v.get("vol_anual")
    if vol is None and spot is not None and len(spot) >= 64:
        vol = float(op.rentabilidades(spot.iloc[-64:], log=True).std(ddof=1) * np.sqrt(252))
        lim.append("volatilidad realizada de 3 meses (sin implícita aportada)")
    out.update(op.carry_exposicion(float(v["tipo_base"]), float(v["tipo_cotizada"]),
                                   str(params.get("direccion") or "ALCISTA_BASE"), vol,
                                   v.get("inflacion_base"), v.get("inflacion_cotizada")))
    if vol is None:
        lim.append("sin volatilidad: carry ajustado no disponible")
    return out, lim


def f_fwd(ent, params):
    v = dict(ent["valores"])
    if "spot" not in v and ent["series"]:
        v["spot"] = float(next(iter(ent["series"].values())).iloc[-1])
    out = op.forward_teorico(float(v["spot"]), float(v["tipo_base"]), float(v["tipo_cotizada"]),
                             float(params.get("plazo_dias", v.get("plazo_dias", 91))),
                             int(params.get("base_dias_base", 360)), int(params.get("base_dias_cotizada", 360)),
                             float(params.get("escala_pip", 1e-4)))
    lim = ["forward teórico por paridad cubierta: sin base cruzada (FX-CIP-001 DOCUMENTADO)"]
    if v.get("forward") is not None:
        out["forward_cotizado"] = float(v["forward"])
        out["diferencia_pips"] = (float(v["forward"]) - out["forward"]) / float(params.get("escala_pip", 1e-4))
    return out, lim


def f_ppp(ent, params):
    r = ent["series_rol"]
    if not {"spot", "precios_base", "precios_cotizada"} <= set(r):
        raise op.ErrorFicha("FX-PPP-001: faltan las series «spot», «precios_base» y «precios_cotizada»")
    return op.ppa_relativa(r["spot"], r["precios_base"], r["precios_cotizada"]), [
        "versión sencilla: PPA relativa con base en la media de largo plazo y AR(1) por MCO (sin corrección de Andrews "
        "ni ajuste de Balassa-Samuelson)"]


def f_rw(ent, params):
    v = ent["valores"]
    m = op.evaluar_frente_rw(v["p"], v["o"], v.get("p_fwd"))
    lim = ["versión sencilla: Brier y BSS frente a RI-PA y RI-FWD; Clark-West, fluctuación y bootstrap DOCUMENTADO"]
    if m["n"] < 30:
        lim.append(f"n = {m['n']} < 30: solo detecta ventajas grandes")
    return m, lim


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


IMPLEMENTADAS: Dict[str, Dict[str, Any]] = {
    "ST-DESC-001": {"fn": _por_serie(_f_desc), "modulo": "MC-01", "version": "1.1", "cifra": "DETERMINISTA", "ri": "RI-NA", "tol": 1e-10},
    "FIN-CAGR-001": {"fn": _por_serie(_f_cagr), "modulo": "MC-01", "version": "1.1", "cifra": "DETERMINISTA", "ri": "RI-NA", "tol": 1e-10},
    "FX-MOM-001": {"fn": f_fx_mom, "modulo": "MC-09", "version": "2.0", "cifra": "ESTADISTICA", "ri": "RI-PA", "tol": 1e-10},
    "FX-VOL-001": {"fn": _por_serie(_f_vol), "modulo": "MC-02", "version": "1.1", "cifra": "ESTADISTICA", "ri": "RI-EWMA", "tol": 1e-8},
    "VOL-GARCH-001": {"fn": _por_serie(_f_garch), "modulo": "MC-02", "version": "1.0", "cifra": "ESTADISTICA", "ri": "RI-EWMA", "tol": 1e-6},
    "FX-TREND-001": {"fn": _por_serie(_f_trend), "modulo": "MC-02", "version": "1.1", "cifra": "ESTADISTICA", "ri": "RI-PA", "tol": 1e-6},
    "RISK-DD-001": {"fn": _por_serie(_f_riesgo), "modulo": "MC-07", "version": "2.0", "cifra": "ESTADISTICA", "ri": "RI-NA", "tol": 1e-8},
    "FX-CORR-001": {"fn": f_corr, "modulo": "MC-03", "version": "1.1", "cifra": "ESTADISTICA", "ri": "correlación de ventana larga", "tol": 1e-8},
    "ML-CLUS-001": {"fn": f_clus, "modulo": "MC-06", "version": "1.0", "cifra": "ESTADISTICA", "ri": "agrupación por segmento", "tol": 1e-8},
    "FX-CARRY-001": {"fn": f_carry, "modulo": "MC-03", "version": "2.0", "cifra": "DETERMINISTA", "ri": "RI-PA", "tol": 1e-8},
    "FX-FWD-001": {"fn": f_fwd, "modulo": "MC-01", "version": "1.0", "cifra": "DETERMINISTA", "ri": "RI-NA", "tol": 1e-10},
    "FX-PPP-001": {"fn": f_ppp, "modulo": "MC-03", "version": "1.0", "cifra": "ESTADISTICA", "ri": "RI-PA", "tol": 1e-8},
    "FX-RW-001": {"fn": f_rw, "modulo": "MC-10", "version": "1.0", "cifra": "ESTADISTICA", "ri": "RI-PA y RI-FWD", "tol": 1e-8},
    "FC-EVAL-001": {"fn": f_fc_eval, "modulo": "MC-10", "version": "1.0", "cifra": "ESTADISTICA", "ri": "referencia de la celda", "tol": 1e-8},
    "FC-CAL-001": {"fn": f_fc_cal, "modulo": "MC-10", "version": "1.0", "cifra": "ESTADISTICA", "ri": "RI-CLI", "tol": 1e-8},
    "SCORE-RK-001": {"fn": f_score, "modulo": "MC-01", "version": "2.0", "cifra": "DETERMINISTA", "ri": "RI-NA", "tol": 0.0},
}


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
    def __init__(self, almacen, proveedor, cfg: Dict, contabilidad=None) -> None:
        self.almacen = almacen
        self.proveedor = proveedor
        self.cfg = cfg
        self.contabilidad = contabilidad
        self._cache: Dict[str, Dict] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------------------------
    def _resolver_datos(self, datos: List[Dict], fecha_corte) -> Tuple[Dict, List[Dict]]:
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
                                  "fecha_dato": str(s.index[-1].date()), "n": int(len(s)),
                                  "huella": self.proveedor.huella(d["serie"], d.get("inicio"), fin),
                                  "fuente": f"HT-01:{self.proveedor.nombre}"})
            elif "valores" in d:
                ent["valores"].update(d["valores"])
                efectivos.append({"valor": "en línea", "claves": sorted(d["valores"]), "huella": clave_hash(d["valores"])[:16]})
        return ent, efectivos

    def servir(self, peticion: Dict, solicitante: str, run_id: Optional[str] = None, msg_id: Optional[str] = None) -> Dict:
        ficha = (peticion.get("operacion") or {}).get("ficha_id") if isinstance(peticion.get("operacion"), dict) \
            else peticion.get("operacion")
        params = dict(peticion.get("parametros") or {})
        if peticion.get("segmento"):
            params.setdefault("segmento", peticion["segmento"])
        fecha_corte = peticion.get("fecha_corte") or (str(self.proveedor.as_of.date()) if self.proveedor.as_of is not None else None)
        plan = peticion.get("plan", "PLAN_MIN")
        base = {"calc_id": None, "contrato": "CT-09", "msg_id": msg_id, "run_id": run_id, "solicitante": solicitante,
                "operacion": {"method_id": ficha, "ficha_id": ficha, "ficha_version": None, "catalog_version": CATALOG_VERSION,
                              "op_sin_ficha": False},
                "perfil": peticion.get("perfil") or ["TRANSVERSAL"], "segmento": peticion.get("segmento"),
                "horizonte": peticion.get("horizonte"), "modo": peticion.get("modo", "SYNC_CALC"), "plan": plan,
                "prioridad": peticion.get("prioridad", "MATERIAL"), "parametros": params,
                "semilla": peticion.get("semilla"), "as_of": fecha_corte, "fecha_limite_informacion": fecha_corte,
                "madurez_metodo": "IMPLEMENTADO", "cache_hit": False}
        uc = float((self.cfg.get("uc") or {}).get("motor_por_plan", {}).get(plan, 0.02))
        # 1) Ficha
        if ficha in RETIRADAS:
            alt = RETIRADAS[ficha] or "ST-DESC-001"
            return self._rechazo(base, "FUERA_DE_CATALOGO", f"Ficha {ficha} retirada en el Catálogo Forex (sección 10); "
                                 f"ficha cambiaria más próxima: {alt}", alternativa=alt, uc=uc)
        if ficha not in IMPLEMENTADAS or (ficha == "VOL-GARCH-001" and not garch_disponible()):
            motivo = "METODO_NO_IMPLEMENTADO" if ficha in FICHAS_CATALOGO else "OPERACION_SIN_FICHA"
            return self._rechazo(base, motivo, f"Ficha {ficha} no implementada en el ejecutor del Bloque A Forex V1.0"
                                 + (f"; alternativa: {ALTERNATIVAS[ficha]}" if ficha in ALTERNATIVAS else ""),
                                 alternativa=ALTERNATIVAS.get(ficha), uc=uc)
        meta = IMPLEMENTADAS[ficha]
        base["operacion"]["ficha_version"] = meta["version"]
        base["modulos"] = [meta["modulo"]]
        # 2) Datos (guardia anti-fuga)
        try:
            ent, efectivos = self._resolver_datos(peticion.get("datos") or [], fecha_corte)
        except FugaDeInformacion as e:
            return self._rechazo(base, "FUGA_DE_INFORMACION", str(e), uc=uc)
        except (DatosNoDisponibles, KeyError) as e:
            return self._rechazo(base, "DATOS_NO_DISPONIBLES", str(e), uc=uc)
        clave = clave_hash(ficha, meta["version"], efectivos, params, peticion.get("semilla"), base["perfil"])
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
        resultado, resultado2 = _limpio(resultado), _limpio(resultado2)
        identico = resultado == resultado2
        calc_id = self.almacen.nuevo_id("CALC")
        estado = "SERVED_WITH_LIMITATIONS" if limitaciones else "SERVED"
        entrada = {**base, "tipo_entrada": "SERVICIO", "calc_id": calc_id, "estado": estado, "datos": efectivos,
                   "resultado": {"forma": "TABLA", "payload": resultado}, "clase_cifra": meta["cifra"],
                   "incertidumbre": {"tipo": "IC" if meta["cifra"] == "ESTADISTICA" else None},
                   "referencia_ingenua": {"tipo": meta["ri"]},
                   "artefacto": {"code_ref": f"bloque_a_forex.motor.operaciones · {meta['fn'].__name__}",
                                 "inputs_effective": efectivos, "transformations": "rendimientos simples salvo ficha",
                                 "rounding_policy": "sin redondeo intermedio; JSON float64"},
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

    def _rechazo(self, base: Dict, motivo: str, detalle: str, alternativa: Optional[str] = None, uc: float = 0.0) -> Dict:
        calc_id = self.almacen.nuevo_id("CALC")
        e = {**base, "tipo_entrada": "RECHAZO", "calc_id": calc_id, "estado": "REJECTED", "motivo_rechazo": motivo,
             "detalle": detalle, "alternativa": alternativa, "madurez_metodo": "DOCUMENTADO" if motivo == "METODO_NO_IMPLEMENTADO" else base.get("madurez_metodo"),
             "consumo_uc": 0.0, "limitaciones": [detalle], "incidencias": []}
        self.almacen.escribir("RC", "AG-13", e)
        return {"estado": "RECHAZADO", "motivo": motivo, "detalle": detalle, "calc_id": calc_id, "alternativa": alternativa}

    # ------------------------------------------------------------------------------------
    def reejecutar(self, calc_id: str, motivo: str, solicitante: str = "AG-18") -> Dict:
        """CT-10 (MC-08): recalcula con las entradas del artefacto y compara con la tolerancia de la ficha."""
        orig = self.almacen.estado("RC").get(calc_id)
        if not orig or orig.get("tipo_entrada") != "SERVICIO":
            raise KeyError(f"{calc_id} no es un servicio del Registro de cálculos")
        ficha = orig["operacion"]["ficha_id"]
        datos = []
        for d in orig["datos"]:
            if "serie_ht01" in d:
                datos.append({"serie": d["serie_ht01"], "inicio": d["inicio"], "fin": d["fecha_dato"], "rol": d["rol"]})
        if any("valor" in d for d in orig["datos"]):
            raise NotImplementedError("Re-ejecución de datos en línea: aporte los valores originales")
        ent, efectivos = self._resolver_datos(datos, orig["as_of"])
        nuevo, _ = IMPLEMENTADAS[ficha]["fn"](ent, orig["parametros"])
        nuevo = _limpio(nuevo)
        tol = IMPLEMENTADAS[ficha]["tol"]
        difs = _comparar(orig["resultado"]["payload"], nuevo, tol)
        mismas = [a.get("huella") for a in orig["datos"]] == [b.get("huella") for b in efectivos]
        coincide = "SI" if not difs and mismas else ("DENTRO_TOLERANCIA" if not difs else "NO")
        e = {"tipo_entrada": "REEJECUCION", "calc_id": self.almacen.nuevo_id("CALC"), "contrato": "CT-10",
             "solicitante": solicitante, "operacion": orig["operacion"], "estado": "SERVED", "as_of": orig["as_of"],
             "reejecucion": {"calc_original": calc_id, "motivo": motivo, "aislamiento": "CONFIRMADO", "tolerancia": tol,
                             "coincide": coincide, "diferencias": difs[:20],
                             "categoria": None if coincide != "NO" else ("DATOS_DISTINTOS" if not mismas else "NO_DETERMINISMO"),
                             "diagnostico": "coincidencia exacta" if coincide == "SI" else "ver diferencias"},
             "datos": efectivos, "consumo_uc": 0.0, "madurez_metodo": "IMPLEMENTADO"}
        self.almacen.escribir("RC", "AG-13", e)
        return {"coincide": coincide, "diferencias": difs, "calc_id": e["calc_id"]}


def _comparar(a: Any, b: Any, tol: float, ruta: str = "") -> List[str]:
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
