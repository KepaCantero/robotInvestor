"""r04_01 · QA T-65 r04 · H-16 en el borde: frescura de la referencia y del proxy al emitir y al resolver.

Uso (desde bloque_a/11_Ejecutor):  ../../.venv/bin/python ../../.docs/tickets/T-65/revisores/r04_01_frescura_borde.py [parte…]

Partes:
  R · Resolución de un PRG RELATIVO ya emitido (escrito en F4 como en `tests/test_t65_qa_r03.py`) con una serie que deja
      de publicarse en distintos días alrededor de la emisión, para H1 (5 sesiones = 7 días naturales) y H2 (28 días).
      Esperado (H-16): «nunca resuelve con 0»; una serie sin ningún dato posterior a la emisión no se resuelve.
  E · Emisión: ACWI parada a 7 y a 8 días de la fecha as_of (borde de `referencias.antiguedad_maxima_dias`).
  C · CESTA (DIV): un miembro parado justo en la emisión de un PRG H1.
"""
import pathlib
import shutil
import sys
import tempfile
import warnings

import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, str(pathlib.Path.cwd()))
from bloque_a.configuracion import DIR_EJECUTOR, RUTA_UNIVERSO_EJEMPLO, cargar_config  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402

PARTES = set(sys.argv[1:]) or {"R", "E", "C"}
hall, info = 0, 0


def nuevo(prep=None, extra=None):
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="r04_01_"))
    datos = tmp / "datos"
    shutil.copytree(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos", datos)
    if prep:
        prep(datos)
    cfg = {"modo": "backtest", "perfiles": {"activos": ["RV", "DIV", "IDX"]}}
    cfg.update(extra or {})
    return Bloque(cargar_config(extra=cfg), ProveedorCSV(datos), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(),
                  tmp / "e", tmp / "s")


def parar(simbolo, hasta):
    def f(datos):
        df = pd.read_csv(datos / f"{simbolo}.csv")
        df[df["fecha"] <= hasta].to_csv(datos / f"{simbolo}.csv", index=False)
    return f


def prg(b, prg_id, clase, hz, proxy, ref, f0, f1):
    b.fijar_fecha(f0)
    b.almacen.escribir("F4", "AG-10", {
        "tipo_entrada": "ALTA", "prg_id": prg_id, "opp_id": "OPP-1", "clase": clase, "horizonte": hz, "estado": "ABIERTO",
        "prob_interna": 0.65, "sentido": "POSITIVO", "umbral": 0.0, "tipo_pronostico": "RELATIVO", "referencia_indice": ref,
        "variable": {"serie_ht01": proxy}, "fecha_emision": f0, "fecha_resolucion": f1,
        "nivel_referencia": {"valor": 1.0, "fecha": f0}, "referencia_ingenua": {"valor_o_prob": 0.5}, "en_informe": True})


def resolver(b, prg_id, as_of):
    b.fijar_fecha(as_of)
    b.evaluador.resolver(as_of, "RUN-2026-0099")
    e = b.almacen.estado("F4", as_of)[prg_id]
    return e.get("estado"), e.get("resolucion") or {}


# ------------------------------------------------------------------ R
if "R" in PARTES:
    # H1: emitido el viernes 2026-04-17, se resuelve el viernes 2026-04-24 (5 sesiones = 7 días naturales)
    CASOS = [
        ("H1", "ACWI", "2026-04-17", "2026-04-17", "2026-04-24", "ACWI parada justo en la emisión"),
        ("H1", "SPY", "2026-04-17", "2026-04-17", "2026-04-24", "proxy parado justo en la emisión"),
        ("H1", "ACWI", "2026-04-16", "2026-04-17", "2026-04-24", "ACWI parada el día antes de la emisión"),
        ("H1", "ACWI", "2026-04-20", "2026-04-17", "2026-04-24", "ACWI parada 1 sesión después de la emisión"),
        ("H2", "ACWI", "2026-03-27", "2026-03-27", "2026-04-24", "H2 · ACWI parada justo en la emisión"),
        ("H2", "ACWI", "2026-04-17", "2026-03-27", "2026-04-24", "H2 · ACWI parada 7 días antes de la resolución"),
        ("H2", "ACWI", "2026-04-16", "2026-03-27", "2026-04-24", "H2 · ACWI parada 8 días antes de la resolución"),
    ]
    for hz, sym, hasta, f0, f1, nombre in CASOS:
        b = nuevo(parar(sym, hasta))
        prg(b, "PRG-2026-0901", "RV", hz, "SPY", "ACWI", f0, f1)
        est, res = resolver(b, "PRG-2026-0901", "2026-04-27")
        rr, rp = res.get("rent_referencia"), res.get("rent_proxy")
        cero = est == "RESUELTO" and (rr == 0.0 or rp == 0.0)
        sin_dato_tras_emision = pd.Timestamp(hasta) <= pd.Timestamp(f0)
        if cero or (est == "RESUELTO" and sin_dato_tras_emision):
            hall += 1
            et = "HALLAZGO"
        elif est == "RESUELTO":
            info += 1
            et = "INFO"
        else:
            et = "OK"
        print(f"{et:9} R · {nombre}: estado={est} rent_proxy={rp} rent_referencia={rr} fecha_dato={res.get('fecha_dato')}")

# ------------------------------------------------------------------ C
if "C" in PARTES:
    b0 = nuevo()
    b0.fijar_fecha("2026-06-05")
    miembros = b0.evaluador.simbolos_clase("DIV")
    f0, f1 = "2026-04-17", "2026-04-24"
    b = nuevo(parar(miembros[0], f0))
    b.fijar_fecha("2026-06-05")
    r_cesta, _ = b.evaluador.rentabilidad("CESTA", "DIV", f0, f1)
    otros = [b.evaluador.rentabilidad(s, "DIV", f0, f1)[0] for s in miembros[1:]]
    r_m0, d_m0 = b.evaluador.rentabilidad(miembros[0], "DIV", f0, f1)
    entra = abs(r_cesta - sum(otros) / len(otros)) > 1e-12
    hall += 1 if entra else 0
    print(f"{'HALLAZGO' if entra else 'OK':9} C · H1, {miembros[0]} parado justo en la emisión: su rentabilidad={r_m0} (dato del {d_m0.date()}); "
          f"cesta={r_cesta:.6f} · media sin él={sum(otros) / len(otros):.6f} · cuenta con 0={entra}")

# ------------------------------------------------------------------ E
if "E" in PARTES:
    AS_OF = "2026-06-05"
    for hasta, esperado_fuera in (("2026-05-29", False), ("2026-05-28", True)):
        b = nuevo(parar("ACWI", hasta))
        r = b.ciclo(AS_OF, alcance={"clases": ["RV", "DIV"]})
        lim = " | ".join(r["paquete"].get("limitaciones") or [])
        fuera = "referencia de comparación ACWI" in lim
        prgs = [p for p in b.almacen.estado("F4", AS_OF).values() if p.get("run_id") == r["run_id"] and p.get("referencia_indice") == "ACWI"]
        ok = fuera == esperado_fuera
        hall += 0 if ok else 1
        niveles = sorted({(p.get("horizonte"), (p.get("nivel_referencia_indice") or {}).get("fecha") if isinstance(p.get("nivel_referencia_indice"), dict) else p.get("nivel_referencia_indice")) for p in prgs})
        print(f"{'OK' if ok else 'HALLAZGO':9} E · ACWI con último cierre {hasta} ({(pd.Timestamp(AS_OF) - pd.Timestamp(hasta)).days} días): "
              f"RV fuera={fuera} estado={r['estado']} PRG frente a ACWI={len(prgs)} {niveles[:4]}")

print(f"HALLAZGOS: {hall} · INFO: {info}")
