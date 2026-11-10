"""r05_01 · QA T-65 r05 · H-24: resolución de un PRG con cada serie parada alrededor de la emisión y del borde de PS2,
por horizonte (H1 a H5), y el nuevo uso de `ps2_antiguedad_maxima_dias` en la resolución.

Uso (desde bloque_a/11_Ejecutor):  ../../.venv/bin/python ../../.docs/tickets/T-65/revisores/r05_01_resolucion_por_horizonte.py [parte…]

Partes:
  M · Matriz: H1–H5 × {proxy, referencia, miembro de la CESTA} × parada {emisión − 1 sesión, emisión, emisión + 1 sesión,
      borde de PS2, borde + 1 día}. Esperado: nunca RESUELTO sin un dato de cada serie posterior a la emisión (ni con
      rentabilidad 0); RESUELTO en el borde exacto; ABIERTO más allá; NO_RESOLUBLE pasado el plazo.
  X · Ventanas desalineadas: H3/H4/H5 con la referencia parada dentro de la tolerancia y el proxy al día. ¿Cuántos sucesos
      cambian frente a medir las dos series hasta la misma fecha?
  T · Datos que llegan tarde: H4 con el proxy sin los últimos 20 días a la primera fecha de resolución; luego llegan.
  F · Festivos en H1 al resolver: cierres de Xetra (24, 25 y 26-12; Viernes Santo y lunes de Pascua), que `ps2_festivos`
      descuenta en PS2 al emitir.
  O · PRG antiguos: ALTA sin `horizonte` válido, H5 con probabilidad, resoluciones ya escritas con el código anterior.
"""
import pathlib
import shutil
import sys
import tempfile
import warnings

import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, str(pathlib.Path.cwd()))
from bloque_a.configuracion import DIR_EJECUTOR, RUTA_UNIVERSO_EJEMPLO, cargar_config, parametro  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque, _sesiones_entre  # noqa: E402

PARTES = set(sys.argv[1:]) or {"M", "X", "T", "F", "O"}
hall, info = 0, 0
BD = pd.offsets.BDay


def nuevo(prep=None):
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="r05_01_"))
    datos = tmp / "datos"
    shutil.copytree(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos", datos)
    if prep:
        prep(datos)
    cfg = {"modo": "backtest", "perfiles": {"activos": ["RV", "DIV", "IDX"]}}
    return Bloque(cargar_config(extra=cfg), ProveedorCSV(datos), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(),
                  tmp / "e", tmp / "s"), datos


def parar(simbolo, hasta, quitar=()):
    def f(datos):
        df = pd.read_csv(datos / f"{simbolo}.csv")
        df = df[df["fecha"] <= hasta] if hasta else df
        df = df[~df["fecha"].isin(list(quitar))]
        df.to_csv(datos / f"{simbolo}.csv", index=False)
    return f


def prg(b, prg_id, clase, hz, proxy, ref, f0, f1, tipo="RELATIVO", prob=0.65):
    b.fijar_fecha(f0)
    alta = {"tipo_entrada": "ALTA", "prg_id": prg_id, "opp_id": "OPP-1", "clase": clase, "horizonte": hz, "estado": "ABIERTO",
            "prob_interna": prob, "sentido": "POSITIVO", "umbral": 0.0, "tipo_pronostico": tipo, "referencia_indice": ref,
            "variable": {"serie_ht01": proxy}, "fecha_emision": f0, "fecha_resolucion": f1,
            "nivel_referencia": {"valor": 1.0, "fecha": f0}, "referencia_ingenua": {"valor_o_prob": 0.5}, "en_informe": True}
    if hz is None:
        alta.pop("horizonte")
    b.almacen.escribir("F4", "AG-10", alta)


def resolver(b, prg_id, as_of):
    b.fijar_fecha(as_of)
    b.evaluador.resolver(as_of, "RUN-2026-0099")
    e = b.almacen.estado("F4", as_of)[prg_id]
    return e.get("estado"), e.get("resolucion") or {}


def ts(x):
    return pd.Timestamp(x).normalize()


# Fechas: emisión en viernes; resolución con la fecha que guarda HT-05 (H5: hito ficticio a 4 años, dentro de los datos)
EMI = {"H1": "2026-04-17", "H2": "2026-03-27", "H3": "2025-11-28", "H4": "2025-06-27", "H5": "2022-06-24"}
RES = {"H1": "2026-04-24", "H2": "2026-04-24", "H3": "2026-05-28", "H4": "2026-06-27", "H5": "2026-06-24"}

# ------------------------------------------------------------------ M
if "M" in PARTES:
    b0, _ = nuevo()
    lim = parametro(b0.cfg, "ps2_antiguedad_maxima_dias")
    b0.fijar_fecha("2026-06-05")
    miembro = b0.evaluador.simbolos_clase("DIV")[0]
    for hz in ("H1", "H2", "H3", "H4", "H5"):
        f0, f1 = ts(EMI[hz]), ts(RES[hz])
        if hz == "H1":
            borde = f1 - BD(lim["H1"])
        else:
            borde = f1 - pd.Timedelta(days=lim[hz])
            borde = borde if borde.weekday() < 5 else borde + BD(1)   # primer día hábil que cumple
        paradas = [("emisión − 1 sesión", f0 - BD(1)), ("emisión", f0), ("emisión + 1 sesión", f0 + BD(1)),
                   ("borde de PS2", borde), ("borde − 1 sesión (fuera)", borde - BD(1))]
        for quien, clase, proxy, ref, sym in (("proxy", "RV", "SPY", "ACWI", "SPY"), ("referencia", "RV", "SPY", "ACWI", "ACWI"),
                                              ("miembro de la CESTA", "DIV", b0.evaluador.simbolos_clase("DIV")[1], "CESTA", miembro)):
            for nombre, hasta in paradas:
                b, _ = nuevo(parar(sym, str(hasta.date())))
                prg(b, "PRG-2026-0901", clase, hz, proxy, ref, str(f0.date()), str(f1.date()))
                as_of = f1 + BD(1)
                est, res = resolver(b, "PRG-2026-0901", as_of)
                d_sym = hasta
                dentro = d_sym > f0 and ((len(pd.bdate_range(d_sym, f1)) - 1) <= lim["H1"] if hz == "H1" else (f1 - d_sym).days <= lim[hz])
                rr, rp = res.get("rent_referencia"), res.get("rent_proxy")
                cero = est == "RESUELTO" and (rr == 0.0 or rp == 0.0)
                if quien == "miembro de la CESTA":
                    # la cesta se resuelve sin el miembro que no sirve: nunca con su 0
                    b.fijar_fecha(as_of)
                    otros = [s for s in b.evaluador.simbolos_clase("DIV") if s != miembro]
                    import numpy as np
                    vals = []
                    for s in otros:
                        try:
                            vals.append(b.evaluador.rentabilidad(s, "DIV", f0, f1, hz)[0])
                        except Exception:
                            pass
                    con = None
                    try:
                        con = b.evaluador.rentabilidad("CESTA", "DIV", f0, f1, hz)[0]
                    except Exception:
                        pass
                    sin = float(np.mean(vals)) if vals else None
                    if dentro:
                        ok = con is not None and (sin is None or abs(con - sin) > 1e-12 or len(vals) == 0)
                    else:
                        ok = con is not None and sin is not None and abs(con - sin) < 1e-12
                    et = "OK" if ok else "HALLAZGO"
                    hall += 0 if ok else 1
                    print(f"{et:9} M · {hz} · {quien} parado en {nombre} ({hasta.date()}): cuenta={dentro} cesta={con} sin él={sin} estado={est}")
                    continue
                if cero or (est == "RESUELTO" and not dentro):
                    et = "HALLAZGO"
                    hall += 1
                elif est != "RESUELTO" and dentro:
                    et = "HALLAZGO"
                    hall += 1
                else:
                    et = "OK"
                print(f"{et:9} M · {hz} · {quien} parado en {nombre} ({hasta.date()}): dentro={dentro} estado={est} "
                      f"rp={rp} rr={rr} f_proxy={res.get('fecha_dato_proxy')} f_ref={res.get('fecha_dato_referencia')}")
                if est == "ABIERTO" and hz == "H1":
                    est2, _ = resolver(b, "PRG-2026-0901", f1 + BD(int(parametro(b.cfg, "evaluacion.dias_habiles_no_resoluble"))))
                    if est2 != "NO_RESOLUBLE":
                        hall += 1
                        print(f"HALLAZGO    pasado el plazo sigue {est2}")

# ------------------------------------------------------------------ X
if "X" in PARTES:
    b, datos = nuevo()
    acwi = pd.read_csv(datos / "ACWI.csv", parse_dates=["fecha"]).set_index("fecha")["cierre"]
    spy = pd.read_csv(datos / "SPY.csv", parse_dates=["fecha"]).set_index("fecha")["cierre"]
    lim = parametro(b.cfg, "ps2_antiguedad_maxima_dias")
    from bloque_a.herramientas.ht05_planificador import fecha_resolucion
    for hz, tol, etiqueta in (("H1", None, "PS2 (1 sesión)"), ("H2", 3, "PS2 (3 días)"), ("H2", 7, "r03/r04 (7 días)"),
                              ("H3", 7, "PS2 = r04 (7 días)"), ("H4", 7, "r03/r04 (7 días)"), ("H4", 30, "PS2 (30 días)")):
        cambios, n = 0, 0
        for f0 in pd.date_range("2024-01-05", "2025-10-31", freq="W-FRI"):
            f1 = fecha_resolucion(f0, hz, b.cfg["horizontes"])
            if f1 > pd.Timestamp("2026-10-30"):
                continue
            d1b = (f1 - BD(1)) if tol is None else f1 - pd.Timedelta(days=tol)
            d1b = acwi[acwi.index >= d1b].index.min()   # referencia parada justo dentro de la tolerancia
            d0 = acwi[acwi.index <= f0].index.max()
            p0, p1 = spy[spy.index <= f0].iloc[-1], spy[spy.index <= f1].iloc[-1]
            r0, r1 = acwi[acwi.index <= f0].iloc[-1], acwi.loc[d1b]
            desalineado = (p1 / p0 - 1) - (r1 / r0 - 1) > 0
            p1a = spy[spy.index <= d1b].iloc[-1]
            alineado = (p1a / p0 - 1) - (r1 / r0 - 1) > 0
            n += 1
            cambios += int(desalineado != alineado)
            _ = d0
        print(f"INFO      X · {hz}, tolerancia {etiqueta}: con ACWI parada en el borde y SPY al día, {cambios} de {n} sucesos "
              f"cambian frente a medir las dos series hasta la misma fecha (resolución de PRG RELATIVO)")
        info += 1
    # de punta a punta: H4 con ACWI parada 29 días antes
    f0, f1 = "2025-06-27", "2026-06-27"
    b, _ = nuevo(parar("ACWI", "2026-05-29"))
    prg(b, "PRG-2026-0902", "RV", "H4", "SPY", "ACWI", f0, f1)
    est, res = resolver(b, "PRG-2026-0902", "2026-07-03")
    print(f"INFO      X · H4, ACWI parada 2026-05-29 (29 días antes de {f1}): estado={est} f_proxy={res.get('fecha_dato_proxy')} "
          f"f_ref={res.get('fecha_dato_referencia')} exceso={res.get('valor_observado')}")
    info += 1

# ------------------------------------------------------------------ T
if "T" in PARTES:
    f0, f1 = "2025-06-27", "2026-06-27"
    for retraso in (5, 20, 35):
        hasta = str((ts(f1) - pd.Timedelta(days=retraso)).date())
        b, datos = nuevo(parar("SPY", hasta))
        prg(b, "PRG-2026-0903", "RV", "H4", "SPY", "ACWI", f0, f1)
        est, res = resolver(b, "PRG-2026-0903", "2026-07-03")
        print(f"INFO      T · H4, SPY con los últimos {retraso} días sin llegar a la primera resolución: estado={est} "
              f"f_proxy={res.get('fecha_dato_proxy')} rp={res.get('rent_proxy')} (con 7 días comunes: {'ABIERTO' if retraso > 7 else 'RESUELTO'})")
        info += 1

# ------------------------------------------------------------------ F
if "F" in PARTES:
    b0, _ = nuevo()
    fest = b0._festivos_ps2
    CASOS = [
        ("Navidad (Xetra cierra 24, 25 y 26-12)", "2025-12-19", "2025-12-26", ["2025-12-24", "2025-12-25", "2025-12-26"]),
        ("Pascua (Xetra cierra Viernes Santo y lunes)", "2026-03-30", "2026-04-06", ["2026-04-03", "2026-04-06"]),
        ("Viernes Santo solo (NYSE)", "2026-03-27", "2026-04-03", ["2026-04-03"]),
    ]
    for nombre, f0, f1, quitar in CASOS:
        for quien in ("SPY", "ACWI", "ambas"):
            syms = ["SPY", "ACWI"] if quien == "ambas" else [quien]

            def prep(datos, syms=syms, quitar=quitar):
                for s in syms:
                    parar(s, None, quitar)(datos)
            b, datos = nuevo(prep)
            prg(b, "PRG-2026-0904", "RV", "H1", "SPY", "ACWI", f0, f1)
            ultimo = max(d for d in pd.bdate_range(ts(f0), ts(f1)) if str(d.date()) not in quitar)
            ses_ps2 = _sesiones_entre(ultimo, f1, fest)
            est, res = resolver(b, "PRG-2026-0904", ts(f1) + BD(1))
            est2 = est
            if est == "ABIERTO":
                est2, _ = resolver(b, "PRG-2026-0904", ts(f1) + BD(int(parametro(b.cfg, "evaluacion.dias_habiles_no_resoluble"))))
            mal = est2 != "RESUELTO" and ses_ps2 <= 1
            hall += 1 if mal else 0
            print(f"{'HALLAZGO' if mal else 'OK':9} F · H1 · {nombre} · {quien} sin esos días: último dato {ultimo.date()}, "
                  f"sesiones según PS2 (con ps2_festivos)={ses_ps2} · estado={est} → {est2}")

# ------------------------------------------------------------------ O
if "O" in PARTES:
    for nombre, hz in (("ALTA sin horizonte", None), ("horizonte desconocido H6", "H6"), ("horizonte en minúsculas", "h2")):
        b, _ = nuevo()
        prg(b, "PRG-2026-0905", "RV", hz, "SPY", "ACWI", "2026-03-27", "2026-04-24")
        try:
            est, res = resolver(b, "PRG-2026-0905", "2026-04-27")
            print(f"INFO      O · {nombre}: estado={est}")
        except Exception as e:  # noqa: BLE001
            print(f"INFO      O · {nombre}: la resolución lanza {type(e).__name__}: {e}")
        info += 1
    # H5 con probabilidad numérica (no debería emitirse, R13): ¿qué tolerancia usa?
    b, _ = nuevo(parar("ACWI", "2026-04-01"))
    prg(b, "PRG-2026-0906", "RV", "H5", "SPY", "ACWI", "2022-06-24", "2026-06-24")
    est, res = resolver(b, "PRG-2026-0906", "2026-06-26")
    print(f"INFO      O · H5 con probabilidad y ACWI parada 84 días antes: estado={est} f_ref={res.get('fecha_dato_referencia')}")
    info += 1

print(f"HALLAZGOS: {hall} · INFO: {info}")
