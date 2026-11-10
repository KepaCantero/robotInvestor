"""r03_02 · QA T-65 r03 · referencias de comparación con datos malos en ciclos completos (H-12).

Uso (desde bloque_a/11_Ejecutor):  ../../.venv/bin/python ../../.docs/tickets/T-65/revisores/r03_02_referencias_ciclo.py [parte…]

Partes:
  A · ACWI (referencia de RV y de IDX, y miembro de IDX) con más formas de datos malos. Ciclo de RV, IDX y DIV.
      Esperado: el ciclo no cae; DIV intacto; RV e IDX, o se analizan con una referencia que vale, o quedan fuera
      declarados (limitación «referencia de comparación ACWI» e incidencia DATOS por tipo).
  B · SUBYACENTE (DER → SPY): SPY con un cierre 0 en la ventana y SPY sin archivo. Esperado: los indicadores de DER que lo
      usan se excluyen y se declaran (README de T-65, H-12); nunca se cambia de referencia en silencio.
  C · Vigentes con referencia guardada: ciclo 1 sano; ciclo 2 con la referencia guardada mala.
  D · Seguimiento de pronósticos ya emitidos: ciclo 1 sano el 2026-05-01 (RELATIVO frente a ACWI); ACWI se estropea
      después (cierre 0 en la resolución, o deja de publicarse tras la emisión); ciclo 2 el 2026-05-15.
      Esperado: un pronóstico RELATIVO no se resuelve con una referencia que no tiene dato en la resolución.
"""
import json
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

AS_OF = "2026-06-05"
PARTES = set(sys.argv[1:]) or {"A", "B", "C", "D"}
hall, info = 0, 0


def nuevo(prefijo, cambiar_datos=None, cambiar_uni=None, extra=None, tmp=None):
    tmp = tmp or pathlib.Path(tempfile.mkdtemp(prefix=f"r03_02_{prefijo}_"))
    datos = tmp / "datos"
    if not datos.exists():
        shutil.copytree(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos", datos)
    uni = pathlib.Path(RUTA_UNIVERSO_EJEMPLO).read_text(encoding="utf-8")
    if cambiar_uni:
        uni = cambiar_uni(uni)
    (tmp / "u.csv").write_text(uni, encoding="utf-8")
    if cambiar_datos:
        cambiar_datos(datos)
    cfg = {"modo": "backtest", "perfiles": {"activos": ["RV", "DIV", "IDX", "DER"]}}
    cfg.update(extra or {})
    b = Bloque(cargar_config(extra=cfg), ProveedorCSV(datos), cargar_universo(tmp / "u.csv"), MockClient(), tmp / "e", tmp / "s")
    return b, tmp


def editar(ruta, f):
    df = pd.read_csv(ruta)
    df = f(df)
    df.to_csv(ruta, index=False)


def resumen(b, r, tipos):
    lim = " | ".join(r["paquete"].get("limitaciones") or [])
    ops = {c: len((r["paquete"]["clases"].get(c) or {}).get("opciones") or []) for c in tipos}
    incs = [x for x in b.almacen.leer("HA") if x.get("tipo") == "DATOS" and x.get("run_id") == r["run_id"]]
    return ops, lim, incs


def prgs(b, as_of, run_id=None):
    return [p for p in b.almacen.estado("F4", as_of).values() if run_id is None or p.get("run_id") == run_id]


# ------------------------------------------------------------------ A
FORMAS = {
    "inf el día anterior": lambda d: editar(d / "ACWI.csv", lambda df: df.assign(cierre=df["cierre"].where(df["fecha"] != "2026-06-04", float("inf")))),
    "texto en un cierre": lambda d: (d / "ACWI.csv").write_text(_texto(d), encoding="utf-8"),
    "NaN en las 3 últimas sesiones": lambda d: editar(d / "ACWI.csv", lambda df: df.assign(
        cierre=df["cierre"].where(~df["fecha"].isin(["2026-06-03", "2026-06-04", "2026-06-05"])))),
    "Close y Adj Close": lambda d: editar(d / "ACWI.csv", lambda df: df.rename(columns={"fecha": "Date", "cierre": "Close"}).assign(**{"Adj Close": df["cierre"]})),
    "cierre repetido": lambda d: (d / "ACWI.csv").write_text(_repetido(d), encoding="utf-8"),
    "BOM y mayúsculas": lambda d: (d / "ACWI.csv").write_bytes(("﻿" + (d / "ACWI.csv").read_text().upper()).encode("utf-8")),
    "fechas con zona": lambda d: editar(d / "ACWI.csv", lambda df: df.assign(fecha=df["fecha"] + " 00:00:00-04:00")),
    "una sola fila (as_of)": lambda d: editar(d / "ACWI.csv", lambda df: df[df["fecha"] == AS_OF]),
    "solo filas futuras": lambda d: editar(d / "ACWI.csv", lambda df: df[df["fecha"] > AS_OF]),
    "sin publicar hasta 2027": lambda d: editar(d / "ACWI.csv", lambda df: df.assign(fecha_publicacion="2027-01-01")),
    "deja de publicarse en 2025-06": lambda d: editar(d / "ACWI.csv", lambda df: df[df["fecha"] <= "2025-06-30"]),
    "cierre negativo en 2019 (fuera de ventana)": lambda d: editar(d / "ACWI.csv", lambda df: pd.concat(
        [pd.DataFrame([{"fecha": "2019-01-02", "cierre": -5.0}]), df])),
    "inf en 2019 (fuera de ventana)": lambda d: editar(d / "ACWI.csv", lambda df: pd.concat(
        [pd.DataFrame([{"fecha": "2019-01-02", "cierre": float("inf")}]), df])),
}


def _texto(d):
    t = (d / "ACWI.csv").read_text(encoding="utf-8").splitlines()
    i = t[0].split(",").index("cierre")
    out = [t[0]]
    for ln in t[1:]:
        c = ln.split(",")
        if c[0] == "2026-06-03":
            c[i] = "n.d."
        out.append(",".join(c))
    return "\n".join(out) + "\n"


def _repetido(d):
    df = pd.read_csv(d / "ACWI.csv")[["fecha", "cierre"]]
    return "fecha,cierre,cierre\n" + "".join(f"{f},{c},{c * 3}\n" for f, c in zip(df["fecha"], df["cierre"]))


if "A" in PARTES:
    b0, _ = nuevo("A0")
    r0 = b0.ciclo(AS_OF, alcance={"clases": ["RV", "IDX", "DIV"]})
    base = resumen(b0, r0, ["RV", "IDX", "DIV"])[0]
    print(f"A · control sano: {base}")
    for nombre, estropear in FORMAS.items():
        b, _ = nuevo("A", estropear)
        try:
            r = b.ciclo(AS_OF, alcance={"clases": ["RV", "IDX", "DIV"]})
        except Exception as e:  # noqa: BLE001
            hall += 1
            print(f"HALLAZGO  A · {nombre}: el ciclo cae: {type(e).__name__}: {str(e)[:140]}")
            continue
        ops, lim, incs = resumen(b, r, ["RV", "IDX", "DIV"])
        fuera = "referencia de comparación ACWI" in lim
        ok_div = ops["DIV"] == base["DIV"]
        if not ok_div:
            hall += 1
            print(f"HALLAZGO  A · {nombre}: DIV cambia {ops}")
            continue
        if fuera:
            ok = ops["RV"] == 0 and ops["IDX"] == 0 and len([x for x in incs if x.get("objeto") == "ACWI"]) >= 2
            et = "OK" if ok else "HALLAZGO"
            hall += 0 if ok else 1
            print(f"{et:9} A · {nombre}: RV e IDX fuera y declarados · ops={ops} incidencias ACWI={len(incs)}")
        else:
            nivel = {p.get("nivel_referencia_indice") for p in prgs(b, AS_OF, r["run_id"]) if p.get("referencia_indice") == "ACWI"}
            print(f"INFO      A · {nombre}: RV e IDX analizados con ACWI · ops={ops} estado={r['estado']} "
                  f"niveles ACWI usados={sorted(x for x in nivel if x is not None)[:3]}")
            info += 1

# ------------------------------------------------------------------ B
FB = "2026-05-01"   # fecha en la que DER da opciones con el cliente simulado
if "B" in PARTES:
    b0, _ = nuevo("B0")
    r0 = b0.ciclo(FB, alcance={"clases": ["DER", "DIV"]})
    print(f"B · control sano: DER ops={len(r0['paquete']['clases']['DER']['opciones'])} referencias de los PRG de DER="
          f"{sorted({str(p.get('referencia_indice')) for p in prgs(b0, FB, r0['run_id']) if p.get('clase') == 'DER'})}")
    def spy_cero(d):
        editar(d / "SPY.csv", lambda df: df.assign(cierre=df["cierre"].where(df["fecha"] != "2026-04-24", 0.0)))

    for nombre, estropear in (("SPY con un cierre 0 en la ventana", spy_cero), ("SPY sin archivo", lambda d: (d / "SPY.csv").unlink())):
        b, _ = nuevo("B", estropear)
        try:
            r = b.ciclo(FB, alcance={"clases": ["DER", "DIV"]})
        except Exception as e:  # noqa: BLE001
            hall += 1
            print(f"HALLAZGO  B · {nombre}: el ciclo cae: {type(e).__name__}: {str(e)[:140]}")
            continue
        ops, lim, incs = resumen(b, r, ["DER", "DIV"])
        refs = sorted({str(p.get("referencia_indice")) for p in prgs(b, FB, r["run_id"]) if p.get("clase") == "DER"})
        declarado = "SPY" in lim or any("SPY" in str(x.get("descripcion") or x) for x in incs)
        cambia = refs and refs != ["SPY"]
        print(f"{'HALLAZGO' if cambia and not declarado else 'OK':9} B · {nombre}: DER ops={ops['DER']} estado={r['estado']} "
              f"referencias de los PRG de DER={refs} · SPY declarado={declarado} · incidencias={[x.get('objeto') for x in incs]}")
        if cambia and not declarado:
            hall += 1

# ------------------------------------------------------------------ C
if "C" in PARTES:
    # C1 · RV con referencia SPY en el ciclo 1; en el ciclo 2 la configuración pasa a ACWI (sana) y SPY se estropea
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="r03_02_C1_"))
    b1, _ = nuevo("C1", extra={"indices_referencia": {"RV": "SPY"}}, tmp=tmp)
    r1 = b1.ciclo("2026-05-29", alcance={"clases": ["RV"]})
    vig = [v for v in b1.vigentes("2026-05-29", "RV")]
    print(f"C1 · ciclo 1: RV ops={len(r1['paquete']['clases']['RV']['opciones'])} vigentes={len(vig)} "
          f"referencias guardadas={sorted({str(v.get('referencia_indice')) for v in vig})}")
    editar(tmp / "datos" / "SPY.csv", lambda df: df.assign(cierre=df["cierre"].where(df["fecha"] != "2026-06-01", 0.0)))
    b2, _ = nuevo("C1", tmp=tmp)
    try:
        r2 = b2.ciclo(AS_OF, alcance={"clases": ["RV", "DIV"]})
        ops, lim, incs = resumen(b2, r2, ["RV", "DIV"])
        print(f"{'OK' if 'SPY' in lim else 'HALLAZGO':9} C1 · ciclo 2: ops={ops} · SPY declarado={'SPY' in lim} · "
              f"incidencias={[x.get('objeto') for x in incs]}")
        hall += 0 if "SPY" in lim else 1
    except Exception as e:  # noqa: BLE001
        hall += 1
        print(f"HALLAZGO  C1 · ciclo 2 cae: {type(e).__name__}: {str(e)[:140]}")

    # C2 · DER con un subyacente distinto por indicador (^BXM → SPY, ^PUT → VGK, TAIL → ACWI). Ciclo 1 sano el 2026-05-01;
    # ciclo 2 el 2026-05-08 con la referencia guardada de la vigente de DER estropeada (cierre 0 el 2026-05-05). README
    # de T-65 (H-12): «con SUBYACENTE, la referencia propia de un indicador malo excluye y declara solo ese indicador».
    SUBS = {"^BXM": "SPY", "^PUT": "VGK", "TAIL": "ACWI"}

    def subs_distintos(u):
        out = []
        for ln in u.splitlines():
            s0 = ln.split(",", 1)[0]
            out.append(ln[: ln.rfind(",")] + "," + SUBS[s0] if s0 in SUBS and ",DER," in ln else ln)
        return "\n".join(out) + "\n"

    tmp = pathlib.Path(tempfile.mkdtemp(prefix="r03_02_C2_"))
    b1, _ = nuevo("C2", cambiar_uni=subs_distintos, tmp=tmp)
    b1.ciclo("2026-05-01", alcance={"clases": ["DER"]})
    vig = {simbolo: v.get("referencia_indice") for v in b1.vigentes("2026-05-01", "DER")
           for simbolo in [(v.get("indicador_seguimiento") or {}).get("simbolo")]}
    print(f"C2 · ciclo 1 (DER sano): vigentes de DER y su referencia guardada={vig}")
    if not vig:
        info += 1
        print("INFO      C2 · sin vigentes de DER: parte no aplicable")
    else:
        mala = sorted(vig.values())[0]

        def estropea(d):
            editar(d / f"{mala}.csv", lambda df: df.assign(cierre=df["cierre"].where(df["fecha"] != "2026-05-05", 0.0)))
        for con_vigente in (False, True):
            t2 = tmp if con_vigente else pathlib.Path(tempfile.mkdtemp(prefix="r03_02_C2b_"))
            b2, _ = nuevo("C2", cambiar_datos=estropea, cambiar_uni=subs_distintos, tmp=t2)
            try:
                r2 = b2.ciclo("2026-05-08", alcance={"clases": ["DER"]})
            except Exception as e:  # noqa: BLE001
                hall += 1
                print(f"HALLAZGO  C2 · cae: {type(e).__name__}: {str(e)[:140]}")
                continue
            ops, lim, incs = resumen(b2, r2, ["DER"])
            excl = b2._datos_invalidos.get(("DER", r2["run_id"]))
            tipo_fuera = f"referencia de comparación {mala}" in lim
            et = "INFO" if tipo_fuera else "OK"
            info += 1 if tipo_fuera else 0
            print(f"{et:9} C2 · {mala} mala, {'con' if con_vigente else 'sin'} vigente que la guarda: DER ops={ops['DER']} "
                  f"indicadores excluidos={excl} · tipo entero fuera={tipo_fuera} · estado={r2['estado']}")

# ------------------------------------------------------------------ D
if "D" in PARTES:
    EMI = "2026-05-01"
    VUELTA = "2026-06-05"   # H2 emitido el 2026-05-01 se resuelve el 2026-05-29

    def estropeos():
        yield "ACWI con cierre 0 en la resolución H2 (2026-05-29)", lambda d: editar(
            d / "ACWI.csv", lambda df: df.assign(cierre=df["cierre"].where(df["fecha"] != "2026-05-29", 0.0)))
        yield "ACWI deja de publicarse tras la emisión", lambda d: editar(d / "ACWI.csv", lambda df: df[df["fecha"] <= EMI])
        yield "ACWI sin archivo tras la emisión", lambda d: (d / "ACWI.csv").unlink()
        yield "proxy deja de publicarse tras la emisión (ACWI sana)", None

    for nombre, estropear in estropeos():
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="r03_02_D_"))
        b1, _ = nuevo("D", tmp=tmp)
        r1 = b1.ciclo(EMI, alcance={"clases": ["RV"]})
        h1 = [p for p in prgs(b1, EMI, r1["run_id"]) if p.get("horizonte") == "H2" and p.get("tipo_pronostico") == "RELATIVO"]
        if not h1:
            print(f"INFO      D · {nombre}: el ciclo 1 no emitió PRG H2 RELATIVO; parte no aplicable")
            info += 1
            continue
        if estropear is None:
            px = sorted({p["variable"]["serie_ht01"] for p in h1})
            for s in px:
                editar(tmp / "datos" / f"{s}.csv", lambda df: df[df["fecha"] <= EMI])
        else:
            estropear(tmp / "datos")
        b2, _ = nuevo("D", tmp=tmp)
        try:
            b2.ciclo(VUELTA, alcance={"clases": ["RV", "DIV"]})
        except Exception as e:  # noqa: BLE001
            hall += 1
            print(f"HALLAZGO  D · {nombre}: el ciclo 2 cae: {type(e).__name__}: {str(e)[:140]}")
            continue
        est = b2.almacen.estado("F4", VUELTA)
        mal = []
        for p in h1:
            e = est.get(p["prg_id"]) or {}
            res = e.get("resolucion") or {}
            if e.get("estado") == "RESUELTO":
                mal.append((p["prg_id"], p["variable"]["serie_ht01"], res.get("fecha_dato"), res.get("rent_proxy"), res.get("rent_referencia"),
                            res.get("resultado")))
        estados = sorted({str((est.get(p["prg_id"]) or {}).get("estado")) for p in h1})
        if mal:
            hall += 1
            print(f"HALLAZGO  D · {nombre}: {len(mal)} de {len(h1)} PRG H2 RELATIVO RESUELTOS sin dato de una de las dos series en "
                  f"la resolución; p. ej. {json.dumps(mal[0], ensure_ascii=False, default=str)}")
        else:
            print(f"OK        D · {nombre}: PRG H2 RELATIVO en estado {estados} (no se resuelven sin dato)")

print(f"HALLAZGOS: {hall} · INFO: {info}")
