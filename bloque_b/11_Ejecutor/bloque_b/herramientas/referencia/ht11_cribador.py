#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HT-11 · Cribador de universos (implementación de referencia).

Bloque B · Robot Investor · V2.0 · 03/11/2026 · Subordinada al Documento 0 del Bloque B, óptima V2.0
(secciones 2.6, 2.7, 4.4, 8.5, 9.4 pasos 1–2, 9.6 PC1 y Anexo A).

Construye el universo invertible de un tipo de activo a partir de listas y CSV de fuentes gratuitas
(constituyentes de índices, listas de ETF y fondos por categoría, emisiones, listados de mercados, tokens):

  1. **Fusión y deduplicación** de las fuentes por ISIN (o por `id` si no hay ISIN), con registro de las fuentes de
     cada instrumento. Las listas de una columna (`--lista`) restringen o amplían por identificador.
  2. **Punto en el tiempo** (sin sesgo de supervivencia ni de anticipación): para cada instrumento se toma la última
     instantánea con `fecha_dato` ≤ fecha del universo; solo entran los que cotizaban en esa fecha
     (`fecha_alta` ≤ fecha < `fecha_baja`). Los dados de baja después de la fecha siguen en el universo.
  3. **Delimitación del ámbito**: si se indica `ambito`, solo entran las filas cuya columna `ambitos` (lista separada
     por «;») lo contiene.
  4. **Filtros duros de invertibilidad** del playbook (8.5) y del marco 2.7 (PC1): cada exclusión con motivo
     controlado (`NO_INVERTIBLE`, `FUERA_DE_MARCO`, `DATOS_INSUFICIENTES` cuando el filtro no es verificable) y
     detalle. Sancionados y suspendidos se excluyen siempre (no modificable). Las señales que no excluyen (p. ej.,
     denominación mínima > 1 000 € en RF, producto con pérdida superior al desembolso en DER) se devuelven como avisos.
     Un vehículo colectivo (etf, fondo, sicav) fuera del universo FON se excluye con motivo
     `NO_INVERTIBLE` y detalle «se asigna a FON» (2.6, regla 2; coherente con G3B-SEL-09 de HT-09).

La pureza (PC2), los datos (PC3) y las alertas (PC4) se evalúan después (MC-B07 y HT-03).

Columnas comunes: id, isin, nombre, tipo_activo, region_mercado (EEE, UK, CH, US, CA, JP, AU, HK, SG u OTRO),
mercado, divisa, emisor, ambitos, subcluster, sancionado, suspendido, fecha_alta, fecha_baja, fecha_dato y las
columnas de filtro de cada tipo (ver FILTROS). Booleanos: «sí/si/true/1/x» o «no/false/0».

Solo biblioteca estándar. CLI:
  python3 ht11_cribador.py --tipo RV --csv universo.csv [--csv otro.csv] [--lista constituyentes.txt]
                           --fecha 2026-10-30 [--ambito redes_electricas_europa] [--horizonte H3]
                           [--marco marco.json] [--salida universo.json]
Estado de madurez (R26): implementada (referencia), pruebas unitarias superadas; integrada en el ejecutor.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple

VERSION = "2.0"
TIPOS_ACTIVO = ("RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV")
REGIONES_MARCO_DEFECTO = ("EEE", "UK", "CH", "US", "CA", "JP", "AU", "HK", "SG")
DIAS_HORIZONTE = {"H1": 14, "H2": 56, "H3": 365, "H4": 365}
MARCO_DEFECTO = {"perfil": "MINORISTA_UE_DEFECTO", "divisa_base": "EUR", "ucits_requerido": True,
                 "mercados_admitidos": list(REGIONES_MARCO_DEFECTO), "permitir_cfd": False, "permitir_microcap": False,
                 "exclusiones": []}
LIMITES = {  # Anexo A y 8.5
    "RV_capitalizacion_meur": 300, "RV_volumen_meur": 1.0, "RV_flotante_pct": 15, "RV_ejercicios": 3,
    "RF_saldo_corporativo_meur": 300, "RF_saldo_soberano_meur": 1000, "RF_denominacion_aviso_eur": 1000,
    "INM_capitalizacion_meur": 300, "INM_volumen_meur": 0.5, "INM_ltv": 0.60, "INM_nav_meses": 6,
    "FON_patrimonio_etf_meur": 100, "FON_patrimonio_activo_meur": 50, "FON_historial_anos": 1, "FON_historial_indice_anos": 3,
    "DER_interes_abierto": 1000, "MP_interes_abierto": 1000, "CRI_capitalizacion_meur": 500, "CRI_historial_meses": 12,
    "IDX_historial_anos": 3, "ALT_nav_meses": 3, "TCV_volumen_meur": 0.5,
}
# Regla 2 de asignación (2.6): un vehículo colectivo es siempre FON, con el tipo del subyacente en `tipo_subyacente`.
# Mismo criterio que G3B-SEL-09 (HT-09). Los fondos cerrados y ELTIF de ALT (tabla 2.6, fila 10) no se tocan.
VEHICULOS_COLECTIVOS = ("etf", "fondo", "sicav")
CALIF_CORTO_VALIDAS = ("A-1+", "A-1", "A-2", "P-1", "P-2", "F1+", "F1", "F2")


class ErrorEntrada(ValueError):
    pass


class SinDato(Exception):
    """El filtro no es verificable con los datos disponibles."""


# ==============================================================================================================
# Lectura
# ==============================================================================================================
def leer_csv(ruta) -> List[Dict[str, str]]:
    with open(ruta, encoding="utf-8-sig", newline="") as fh:
        filas = [{(k or "").strip(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(fh)]
    for f in filas:
        if not f.get("id") and not f.get("isin"):
            raise ErrorEntrada(f"{ruta}: fila sin id ni isin")
    return filas


def leer_lista(ruta) -> List[str]:
    out = []
    for ln in Path(ruta).read_text(encoding="utf-8").splitlines():
        ln = ln.split("#", 1)[0].strip()
        if ln:
            out.append(ln.split(",")[0].strip())
    return out


def _bool(v: Any) -> Optional[bool]:
    if v is None:
        return None
    if isinstance(v, bool):
        return v
    s = str(v).strip().lower()
    if s in ("", "nd", "n/d", "na"):
        return None
    if s in ("si", "sí", "true", "1", "x", "yes", "s"):
        return True
    if s in ("no", "false", "0", "n"):
        return False
    raise ErrorEntrada(f"Booleano no reconocido: {v!r}")


def _num(v: Any) -> Optional[float]:
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace(",", ".")
    if s in ("", "nd", "n/d", "na"):
        return None
    return float(s)


def _fecha(v: Any) -> Optional[dt.date]:
    if v in (None, ""):
        return None
    return dt.date.fromisoformat(str(v)[:10])


def _req_num(f: Dict, campo: str) -> float:
    v = _num(f.get(campo))
    if v is None:
        raise SinDato(campo)
    return v


def _req_bool(f: Dict, campo: str) -> bool:
    v = _bool(f.get(campo))
    if v is None:
        raise SinDato(campo)
    return v


# ==============================================================================================================
# Filtros duros por playbook (8.5)
# Cada filtro devuelve (pasa, detalle, avisos)
# ==============================================================================================================
Resultado = Tuple[bool, str, List[str]]


def _f_rv(f, marco, fecha, horizonte) -> Resultado:
    cap = _req_num(f, "capitalizacion_meur")
    if cap < LIMITES["RV_capitalizacion_meur"] and not marco.get("permitir_microcap"):
        return False, f"capitalización {cap:g} M€ < 300 M€", []
    vol = _req_num(f, "volumen_medio_meur")
    if vol < LIMITES["RV_volumen_meur"]:
        return False, f"volumen medio {vol:g} M€/día < 1 M€", []
    flo = _req_num(f, "flotante_pct")
    if flo < LIMITES["RV_flotante_pct"]:
        return False, f"capital flotante {flo:g} % < 15 %", []
    ej = _req_num(f, "ejercicios_auditados")
    reciente = _bool(f.get("salida_bolsa_reciente")) or False
    if ej < LIMITES["RV_ejercicios"] and not (reciente and ej >= 2):
        return False, f"{ej:g} ejercicios auditados (< 3)", []
    op = (f.get("opinion_auditoria") or "").lower()
    if op in ("denegada", "salvedades_materiales", "adversa"):
        return False, f"opinión de auditoría {op}", []
    return True, "", []


def _f_rf(f, marco, fecha, horizonte) -> Resultado:
    if not _req_bool(f, "precio_observable"):
        return False, "sin precios observables en mercado regulado o SMN", []
    tipo_em = (f.get("tipo_emisor") or "corporativo").lower()
    saldo = _req_num(f, "saldo_vivo_meur")
    minimo = LIMITES["RF_saldo_soberano_meur"] if tipo_em.startswith("soberano") else LIMITES["RF_saldo_corporativo_meur"]
    if saldo < minimo:
        return False, f"saldo vivo {saldo:g} M€ < {minimo} M€", []
    if not _req_bool(f, "folleto"):
        return False, "sin folleto disponible", []
    if _bool(f.get("impago")):
        return False, "en impago", []
    venc = _fecha(f.get("vencimiento"))
    if venc is None:
        raise SinDato("vencimiento")
    if (venc - fecha).days < DIAS_HORIZONTE.get(horizonte, 365):
        return False, f"vencimiento {venc} incompatible con el horizonte {horizonte}", []
    if not (f.get("calificacion") or _bool(f.get("metricas_credito"))):
        return False, "sin calificación ni métricas de crédito calculables", []
    avisos = []
    den = _num(f.get("denominacion_min_eur"))
    if den is not None and den > LIMITES["RF_denominacion_aviso_eur"]:
        avisos.append(f"denominación mínima {den:g} € > 1 000 € (penaliza LA)")
    return True, "", avisos


def _f_div(f, marco, fecha, horizonte) -> Resultado:
    if _req_bool(f, "controles_capital"):
        return False, "divisa con controles de capital materiales", []
    if not f.get("instrumento_acceso"):
        raise SinDato("instrumento_acceso")
    if not _req_bool(f, "instrumento_en_marco"):
        return False, "sin instrumento de acceso del marco (futuro regulado, ETC/ETN del EEE o monetario UCITS)", []
    return True, "", []


def _f_mp(f, marco, fecha, horizonte) -> Resultado:
    ti = (f.get("tipo_instrumento") or "").lower()
    if ti == "futuro":
        if not _req_bool(f, "mercado_regulado"):
            return False, "futuro fuera de mercado regulado", []
        oi = _req_num(f, "interes_abierto")
        if oi < LIMITES["MP_interes_abierto"]:
            return False, f"interés abierto {oi:g} < {LIMITES['MP_interes_abierto']}", []
    elif ti in ("etc", "etn"):
        if (f.get("region_mercado") or "") != "EEE":
            return False, "ETC/ETN no cotizado en el EEE", []
        if not _req_bool(f, "colateral_auditado"):
            return False, "sin colateral o respaldo físico auditado", []
        if not f.get("emisor"):
            raise SinDato("emisor")
    else:
        raise SinDato("tipo_instrumento")
    return True, "", []


def _f_idx(f, marco, fecha, horizonte) -> Resultado:
    if not _req_bool(f, "metodologia_publica"):
        return False, "metodología no pública", []
    if not _req_bool(f, "replicable_ucits_o_futuro"):
        return False, "ningún ETF UCITS ni futuro listado lo replica", []
    h = _req_num(f, "historial_anos")
    if h < LIMITES["IDX_historial_anos"] and not _bool(f.get("reconstruccion_documentada")):
        return False, f"historial {h:g} años < 3 sin reconstrucción documentada", []
    return True, "", []


def _f_fon(f, marco, fecha, horizonte) -> Resultado:
    cerrado = _bool(f.get("cerrado_cotizado")) or False
    if not cerrado:
        if marco.get("ucits_requerido", True) and not _req_bool(f, "ucits"):
            return False, "no UCITS (solo informativo)", []
        if not _req_bool(f, "kid"):
            return False, "sin KID PRIIPs", []
    pasivo = (f.get("gestion") or "pasiva").lower().startswith("pas")
    pat = _req_num(f, "patrimonio_meur")
    minimo = LIMITES["FON_patrimonio_etf_meur"] if pasivo else LIMITES["FON_patrimonio_activo_meur"]
    if pat < minimo:
        return False, f"patrimonio {pat:g} M€ < {minimo} M€", []
    h = _req_num(f, "historial_anos")
    hi = _num(f.get("historial_indice_anos")) or 0
    if h < LIMITES["FON_historial_anos"] and hi < LIMITES["FON_historial_indice_anos"]:
        return False, f"historial {h:g} años < 1 (e índice < 3)", []
    if not _req_bool(f, "clase_eur_o_cubierta"):
        return False, "sin clase en EUR ni cobertura disponible", []
    if _bool(f.get("en_liquidacion")):
        return False, "en liquidación o fusión", []
    return True, "", []


def _f_der(f, marco, fecha, horizonte) -> Resultado:
    ti = (f.get("tipo_instrumento") or "").lower()
    if "binaria" in ti:
        return False, "opciones binarias excluidas siempre", []
    if ti == "cfd" and not marco.get("permitir_cfd"):
        return False, "CFD excluido salvo marco expreso", []
    if not _req_bool(f, "mercado_regulado"):
        return False, "no listado en mercado regulado", []
    if not _req_bool(f, "kid"):
        return False, "sin KID PRIIPs", []
    oi = _req_num(f, "interes_abierto")
    if oi < LIMITES["DER_interes_abierto"]:
        return False, f"interés abierto {oi:g} < {LIMITES['DER_interes_abierto']} contratos", []
    avisos = ["pérdida potencial superior al desembolso"] if _bool(f.get("perdida_superior_desembolso")) else []
    return True, "", avisos


def _f_inm(f, marco, fecha, horizonte) -> Resultado:
    cap = _req_num(f, "capitalizacion_meur")
    if cap < LIMITES["INM_capitalizacion_meur"]:
        return False, f"capitalización {cap:g} M€ < 300 M€", []
    vol = _req_num(f, "volumen_medio_meur")
    if vol < LIMITES["INM_volumen_meur"]:
        return False, f"volumen {vol:g} M€/día < 0,5 M€", []
    nav = _req_num(f, "nav_frecuencia_meses")
    if nav > LIMITES["INM_nav_meses"]:
        return False, f"NAV publicado cada {nav:g} meses (> semestral)", []
    if not _req_bool(f, "cuentas_auditadas"):
        return False, "sin cuentas auditadas", []
    ltv = _req_num(f, "ltv")
    if ltv > LIMITES["INM_ltv"]:
        return False, f"LTV {ltv:.0%} > 60 %", []
    return True, "", []


def _f_cri(f, marco, fecha, horizonte) -> Resultado:
    if _bool(f.get("stablecoin")):
        return False, "stablecoin: solo infraestructura, no candidato de rentabilidad", []
    if not _req_bool(f, "acceso_mica_o_etp"):
        return False, "sin proveedor MiCA ni ETP del EEE", []
    cap = _req_num(f, "capitalizacion_meur")
    if cap < LIMITES["CRI_capitalizacion_meur"]:
        return False, f"capitalización {cap:g} M€ < 500 M€", []
    hm = _req_num(f, "historial_meses")
    if hm < LIMITES["CRI_historial_meses"]:
        return False, f"historial {hm:g} meses < 12", []
    if _bool(f.get("lavado_detectado")):
        return False, "volumen con lavado detectable", []
    if _bool(f.get("advertencia_regulatoria")):
        return False, "advertencia regulatoria específica vigente", []
    if _bool(f.get("es_protocolo")) and not _req_bool(f, "codigo_auditado"):
        return False, "protocolo sin código auditado", []
    return True, "", []


def _f_alt(f, marco, fecha, horizonte) -> Resultado:
    if not _req_bool(f, "cotizado_o_eltif"):
        return False, "ni cotizado en el marco ni ELTIF minorista (vigilancia informativa)", []
    nav = _req_num(f, "nav_frecuencia_meses")
    if nav > LIMITES["ALT_nav_meses"]:
        return False, f"NAV cada {nav:g} meses (> trimestral)", []
    if not _req_bool(f, "nav_auditado"):
        return False, "NAV sin auditoría anual", []
    if not f.get("mecanismo_liquidez"):
        raise SinDato("mecanismo_liquidez")
    if not _req_bool(f, "gestor_regulado"):
        return False, "gestor no regulado", []
    return True, "", []


def _f_mon(f, marco, fecha, horizonte) -> Resultado:
    ti = (f.get("tipo_instrumento") or "").lower()
    tipo_em = (f.get("tipo_emisor") or "").lower()
    if ti in ("fondo", "etf"):
        if not _req_bool(f, "mmf_reglamento"):
            return False, "fondo no acogido al reglamento europeo de fondos monetarios", []
        if not _req_bool(f, "kid"):
            return False, "sin KID", []
    else:
        if not tipo_em.startswith("soberano"):
            cal = (f.get("calificacion_corto") or "").upper()
            if not cal:
                raise SinDato("calificacion_corto")
            if cal not in CALIF_CORTO_VALIDAS:
                return False, f"calificación a corto {cal} por debajo de A-2", []
        plazo = _num(f.get("plazo_dias"))
        if plazo is not None and plazo > max(DIAS_HORIZONTE.get(horizonte, 365) * 1.5, 30):
            return False, f"plazo {plazo:g} días incompatible con el horizonte {horizonte}", []
    return True, "", []


def _f_tcv(f, marco, fecha, horizonte) -> Resultado:
    regulado = _bool(f.get("mercado_regulado")) or False
    ucits = (_bool(f.get("ucits")) or False) and (_bool(f.get("kid")) or False)
    if not (regulado or ucits):
        return False, "ni futuro en mercado regulado ni vehículo UCITS con KID", []
    vol = _num(f.get("volumen_medio_meur"))
    oi = _num(f.get("interes_abierto"))
    if vol is None and oi is None:
        raise SinDato("volumen_medio_meur|interes_abierto")
    if not ((vol or 0) >= LIMITES["TCV_volumen_meur"] or (oi or 0) >= LIMITES["DER_interes_abierto"]):
        return False, "liquidez insuficiente", []
    avisos = []
    if _bool(f.get("apalancado_o_inverso")):
        if horizonte not in ("H1", "H2"):
            return False, "producto apalancado o inverso de volatilidad solo para H1–H2", []
        avisos.append("producto apalancado o inverso: deterioro estructural por roll (advertencia explícita)")
    return True, "", avisos


FILTROS: Dict[str, Callable] = {"RV": _f_rv, "RF": _f_rf, "DIV": _f_div, "MP": _f_mp, "IDX": _f_idx, "FON": _f_fon,
                                "DER": _f_der, "INM": _f_inm, "CRI": _f_cri, "ALT": _f_alt, "MON": _f_mon, "TCV": _f_tcv}


# ==============================================================================================================
# Construcción del universo
# ==============================================================================================================
def _clave(f: Dict) -> str:
    return (f.get("isin") or "").upper() or f.get("id")


def fusionar_fuentes(fuentes: Sequence[Dict]) -> Dict[str, List[Dict]]:
    """`fuentes`: [{"nombre", "filas"}]. Devuelve clave → instantáneas (con `_fuentes`)."""
    out: Dict[str, List[Dict]] = {}
    origen: Dict[str, set] = {}
    for fu in fuentes:
        for fila in fu["filas"]:
            k = _clave(fila)
            out.setdefault(k, []).append(dict(fila))
            origen.setdefault(k, set()).add(fu["nombre"])
    for k, lst in out.items():
        for f in lst:
            f["_fuentes"] = sorted(origen[k])
    return out


def instantanea(snaps: List[Dict], fecha: dt.date) -> Optional[Dict]:
    """Última instantánea con fecha_dato ≤ fecha (sin fecha_dato: siempre visible)."""
    vis = [s for s in snaps if _fecha(s.get("fecha_dato")) is None or _fecha(s.get("fecha_dato")) <= fecha]
    if not vis:
        return None
    return max(vis, key=lambda s: _fecha(s.get("fecha_dato")) or dt.date.min)


def construir_universo(tipo_activo: str, fuentes: Sequence[Dict], fecha, ambito: Optional[str] = None,
                       horizonte: str = "H3", marco: Optional[Dict] = None, lista_restriccion: Optional[Iterable[str]] = None,
                       sancionados: Optional[Iterable[str]] = None) -> Dict:
    if tipo_activo not in FILTROS:
        raise ErrorEntrada(f"tipo de activo desconocido {tipo_activo}")
    fecha = _fecha(fecha) if not isinstance(fecha, dt.date) else fecha
    m = dict(MARCO_DEFECTO)
    m.update(marco or {})
    regiones = set(m.get("mercados_admitidos") or REGIONES_MARCO_DEFECTO)
    excl_broker = set(m.get("exclusiones") or [])
    sanc = set(sancionados or [])
    restr = set(lista_restriccion) if lista_restriccion else None
    snaps = fusionar_fuentes(fuentes)
    incluidos, excluidos, avisos = [], [], []
    bruto = 0
    fuera_de_fecha = 0
    for k, lst in sorted(snaps.items()):
        f = instantanea(lst, fecha)
        if f is None:
            fuera_de_fecha += 1
            continue
        if (f.get("tipo_activo") or tipo_activo) != tipo_activo:
            continue
        alta, baja = _fecha(f.get("fecha_alta")), _fecha(f.get("fecha_baja"))
        if (alta and alta > fecha) or (baja and baja <= fecha):
            fuera_de_fecha += 1
            continue
        if ambito and ambito not in [a.strip() for a in (f.get("ambitos") or "").split(";")]:
            continue
        if restr is not None and f.get("id") not in restr and (f.get("isin") or "") not in restr:
            continue
        bruto += 1
        ident = f.get("id") or f.get("isin")
        base = {"id": ident, "isin": f.get("isin") or None, "nombre": f.get("nombre"), "fuentes": f["_fuentes"],
                "fecha_dato": f.get("fecha_dato") or None}
        if ident in sanc or (f.get("isin") and f["isin"] in sanc) or _bool(f.get("sancionado")) or _bool(f.get("suspendido")):
            excluidos.append({**base, "motivo": "NO_INVERTIBLE", "detalle": "sancionado o suspendido (exclusión no modificable)"})
            continue
        if ident in excl_broker:
            excluidos.append({**base, "motivo": "FUERA_DE_MARCO", "detalle": "excluido por el marco de la petición"})
            continue
        reg = f.get("region_mercado") or ""
        if reg not in regiones:
            excluidos.append({**base, "motivo": "FUERA_DE_MARCO", "detalle": f"mercado {reg or '¿?'} fuera del marco"})
            continue
        if tipo_activo != "FON" and (f.get("tipo_instrumento") or "").strip().lower() in VEHICULOS_COLECTIVOS:
            excluidos.append({**base, "motivo": "NO_INVERTIBLE", "detalle": "vehículo colectivo: se asigna a FON con su "
                              f"tipo_subyacente {tipo_activo} (2.6, regla 2), no a {tipo_activo}"})
            continue
        try:
            ok, det, av = FILTROS[tipo_activo](f, m, fecha, horizonte)
        except SinDato as e:
            excluidos.append({**base, "motivo": "DATOS_INSUFICIENTES", "detalle": f"filtro no verificable: falta {e}"})
            continue
        if not ok:
            excluidos.append({**base, "motivo": "NO_INVERTIBLE", "detalle": det})
            continue
        fila = {k2: v for k2, v in f.items() if not k2.startswith("_")}
        fila["_fuentes"] = f["_fuentes"]
        fila["avisos_invertibilidad"] = av
        incluidos.append(fila)
        avisos += [f"{ident}: {a}" for a in av]
    recuento: Dict[str, int] = {}
    for e in excluidos:
        recuento[e["motivo"]] = recuento.get(e["motivo"], 0) + 1
    return {"herramienta": "HT-11", "version": VERSION, "tipo_activo": tipo_activo, "fecha_universo": fecha.isoformat(),
            "ambito": ambito, "horizonte": horizonte, "marco": m,
            "fuentes": sorted({n for fu in fuentes for n in [fu["nombre"]]}),
            "tamano_bruto": bruto, "tamano_invertible": len(incluidos), "fuera_de_fecha": fuera_de_fecha,
            "incluidos": incluidos, "excluidos": excluidos, "excluidos_por_motivo": recuento, "avisos": avisos,
            "nota_supervivencia": "universo en punto del tiempo: instantáneas con fecha_dato ≤ fecha y cotización vigente en la fecha"}


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="HT-11 · Cribador de universos del Bloque B")
    ap.add_argument("--tipo", required=True, choices=TIPOS_ACTIVO)
    ap.add_argument("--csv", action="append", default=[], help="CSV de una fuente (repetible)")
    ap.add_argument("--lista", action="append", default=[], help="Lista de identificadores que restringe el universo")
    ap.add_argument("--fecha", required=True, help="Fecha del universo (AAAA-MM-DD)")
    ap.add_argument("--ambito")
    ap.add_argument("--horizonte", default="H3", choices=("H1", "H2", "H3", "H4"))
    ap.add_argument("--marco", help="JSON con el marco de invertibilidad")
    ap.add_argument("--sancionados", help="Lista de identificadores sancionados")
    ap.add_argument("--salida")
    a = ap.parse_args(argv)
    try:
        fuentes = [{"nombre": Path(p).name, "filas": leer_csv(p)} for p in a.csv]
        restr = [i for l in a.lista for i in leer_lista(l)] or None
        marco = json.load(open(a.marco, encoding="utf-8")) if a.marco else None
        sanc = leer_lista(a.sancionados) if a.sancionados else None
        res = construir_universo(a.tipo, fuentes, a.fecha, a.ambito, a.horizonte, marco, restr, sanc)
    except (ErrorEntrada, ValueError, OSError) as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 3
    txt = json.dumps(res, ensure_ascii=False, indent=2)
    if a.salida:
        Path(a.salida).write_text(txt, encoding="utf-8")
    else:
        print(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
