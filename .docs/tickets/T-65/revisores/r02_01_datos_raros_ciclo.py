"""r02_01 · QA T-65 r02 · H-01 y H-02 (r01) con más formas de datos malos, a través del ciclo completo de los 12 tipos.

Uso (desde bloque_a/11_Ejecutor):  ../../.venv/bin/python ../../.docs/tickets/T-65/revisores/r02_01_datos_raros_ciclo.py [ABCD]

Parte A (proveedor): cada forma de CSV malo, leída con `cierres` (ventana) y `valor_en`. Esperado: o una serie válida, o
`DatosNoDisponibles`/`DatosInvalidos`. Cualquier otra excepción «escapa» del contrato de HT-01.
Parte B (ciclo de 12 tipos): la forma mala en un símbolo de DIV (cuya referencia es CESTA: `Evaluador.tasa_base` vuelve a
leer a todos los miembros). Esperado: el ciclo no cae; el símbolo se excluye y se declara.
Parte C (ciclo de 12 tipos): la forma mala en ACWI, el índice de referencia de RV y de IDX (`indices_referencia`).
Esperado: el ciclo no cae; los demás tipos siguen; RV e IDX se degradan y lo declaran.
Parte D: un cierre ≤ 0 fuera de la ventana del lote pero dentro de otras lecturas (gc0, clústeres, tasa base) y fuera de
todas: no debe vaciar el tipo en silencio.
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
from bloque_a.herramientas.ht01_datos import DatosNoDisponibles, ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402

AS_OF = "2026-06-05"
F = list(pd.bdate_range("2023-01-02", AS_OF))
BASE = "".join(f"{d.date()},1.0{i % 9}\n" for i, d in enumerate(F))
LINEA = "{s},DIV,Dólar frente a nueva divisa,ESTRATEGIA,GLB,G10,USD,SOLO EJEMPLO,Pares,Par nuevo,Otros cruces,USD/{s},\n"
TODOS = ["RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV"]
TMP = pathlib.Path(tempfile.mkdtemp(prefix="r02_01_"))
res: list = []

FORMAS = {
    "columna_cierre_duplicada": ("fecha,cierre,close\n" + "".join(f"{d.date()},1.0,1.0\n" for d in F)).encode(),
    "fechas_con_zona_horaria": ("fecha,cierre\n" + "".join(f"{d.date()}T00:00:00+02:00,1.0{i % 9}\n" for i, d in enumerate(F))).encode(),
    "zonas_mezcladas": ("fecha,cierre\n" + "".join(f"{d.date()}T00:00:00+0{i % 2}:00,1.0\n" for i, d in enumerate(F))).encode(),
    "utf16": ("fecha,cierre\n" + BASE).encode("utf-16"),
    "latin1": ("fecha,cierre,nota\n" + "".join(f"{d.date()},1.0,café\n" for d in F)).encode("latin-1"),
    "truncado": ("fecha,cierre\n" + BASE + "2026-06-0").encode(),
    "solo_cabecera": b"fecha,cierre\n",
    "vacio": b"",
    "binario": bytes(range(256)) * 20,
    "punto_y_coma": ("fecha;cierre\n" + BASE.replace(",", ";")).encode(),
    "fila_con_campos_de_mas": ("fecha,cierre\n" + BASE + "2026-06-05,1.0,9,9\n").encode(),
    "desordenado_y_duplicado": ("fecha,cierre\n" + "".join(reversed(BASE.splitlines(True))) + f"{F[3].date()},1.5\n").encode(),
    "cierre_nan_texto_en_medio": ("fecha,cierre\n" + "".join(f"{d.date()},{'NaN' if i == 200 else '1.0' + str(i % 9)}\n"
                                                               for i, d in enumerate(F))).encode(),
    "cero_en_la_ventana": ("fecha,cierre\n" + "".join(f"{d.date()},{'0' if i == 500 else '1.0' + str(i % 9)}\n"
                                                        for i, d in enumerate(F))).encode(),
    "cierres_booleanos": ("fecha,cierre\n" + "".join(f"{d.date()},True\n" for d in F)).encode(),
}


def parte_a():
    print("== Parte A: contrato de HT-01 ante cada forma")
    for n, b in FORMAS.items():
        d = pathlib.Path(tempfile.mkdtemp(dir=TMP))
        (d / "X.csv").write_bytes(b)
        p = ProveedorCSV(d)
        p.fijar_as_of(AS_OF)
        for lect, f in (("cierres", lambda: p.cierres("X", "2023-05-01", AS_OF)), ("valor_en", lambda: p.valor_en("X", AS_OF))):
            try:
                r = f()
                v = "OK" if n not in ("cierres_booleanos",) else "INFO"
                det = f"serie de {len(r)}" if lect == "cierres" else f"{r}"
            except DatosNoDisponibles as e:
                v, det = "OK", f"{type(e).__name__}: {str(e)[:80]}"
            except Exception as e:  # noqa: BLE001
                v, det = "HALLAZGO", f"escapa {type(e).__name__}: {str(e)[:80]}"
            print(f"  {v:9s} {n:28s} {lect:9s} {det}")
            res.append((f"A/{n}/{lect}", v, det))


def preparar(series: dict, nuevos_div=()) -> pathlib.Path:
    tmp = pathlib.Path(tempfile.mkdtemp(dir=TMP))
    datos = tmp / "datos"
    shutil.copytree(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos", datos)
    uni = pathlib.Path(RUTA_UNIVERSO_EJEMPLO).read_text(encoding="utf-8").rstrip("\n") + "\n"
    for s, contenido in series.items():
        (datos / f"{s}.csv").write_bytes(contenido)
    for s in nuevos_div:
        uni += LINEA.format(s=s)
    (tmp / "u.csv").write_text(uni, encoding="utf-8")
    return tmp


def ciclo(nombre, tmp, simbolo, tipos_afectados):
    b = Bloque(cargar_config(extra={"modo": "backtest", "perfiles": {"activos": TODOS}}), ProveedorCSV(tmp / "datos"),
               cargar_universo(tmp / "u.csv"), MockClient(), tmp / "e", tmp / "s")
    try:
        r = b.ciclo(AS_OF)
    except Exception as e:  # noqa: BLE001
        det = f"el ciclo de los 12 tipos cae: {type(e).__name__}: {str(e)[:110]}"
        print(f"  HALLAZGO  {nombre:40s} {det}")
        res.append((nombre, "HALLAZGO", det))
        return
    run = r["run_id"]
    clases = r["paquete"]["clases"]
    ops = {c: len(clases[c]["opciones"]) for c in clases}
    decl = [c for c in tipos_afectados if simbolo in " ".join(r["paquete"]["limitaciones"]) or
            simbolo in (getattr(b, "_datos_invalidos", {}).get((c, run)) or []) + (b._sin_historia.get((c, run)) or [])]
    incs = [x for x in b.almacen.leer("HA") if x.get("tipo") == "DATOS" and x.get("objeto") == simbolo]
    v = "OK" if r["estado"] == "PARCIAL" and decl else "HALLAZGO"
    det = f"estado={r['estado']} declarado_en={decl} incidencias={len(incs)} opciones={ops}"
    print(f"  {v:9s} {nombre:40s} {det}")
    res.append((nombre, v, det))


def parte_b():
    print("\n== Parte B: la forma mala en un símbolo de DIV (referencia CESTA), ciclo de 12 tipos")
    for n in ("columna_cierre_duplicada", "fechas_con_zona_horaria", "utf16", "truncado", "desordenado_y_duplicado",
              "cero_en_la_ventana", "solo_cabecera"):
        ciclo(f"B/{n}", preparar({"USDNEW=X": FORMAS[n]}, nuevos_div=["USDNEW=X"]), "USDNEW=X", ["DIV"])


def parte_c():
    print("\n== Parte C: la forma mala en ACWI (referencia de RV y de IDX), ciclo de 12 tipos")
    acwi = (DIR_EJECUTOR / "ejemplos" / "datos_sinteticos" / "ACWI.csv").read_text(encoding="utf-8")
    lineas = acwi.splitlines(True)
    cab = lineas[0]
    i_cierre = cab.strip().split(",").index("cierre")

    def con_cierre(pred, valor):
        out = [cab]
        for ln in lineas[1:]:
            c = ln.rstrip("\n").split(",")
            if pred(c[0]):
                c[i_cierre] = valor
            out.append(",".join(c) + "\n")
        return "".join(out).encode()
    variantes = {
        "cero_hace_una_semana": con_cierre(lambda f: f == "2026-05-29", "0"),
        "negativo_hace_dos_anios": con_cierre(lambda f: f == "2024-06-03", "-5"),
        "binario": FORMAS["binario"],
        "columna_cierre_duplicada": (cab.rstrip("\n") + ",close\n" + "".join(
            ln.rstrip("\n") + "," + ln.rstrip("\n").split(",")[i_cierre] + "\n" for ln in lineas[1:])).encode(),
    }
    for n, b in variantes.items():
        ciclo(f"C/ACWI/{n}", preparar({"ACWI": b}), "ACWI", ["RV", "IDX"])


def parte_d():
    print("\n== Parte D: un cierre ≤ 0 antiguo en todos los pares DIV (fuera de la ventana del lote)")
    for anio in ("2019-03-01", "2023-02-01"):
        tmp = preparar({})
        datos = tmp / "datos"
        uni = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
        for s in uni[uni["clase"] == "DIV"]["simbolo"]:
            df = pd.read_csv(datos / f"{s}.csv")
            primero = pd.Timestamp(df["fecha"].iloc[0])
            fechas = pd.bdate_range("2019-01-01", primero - pd.Timedelta(days=1))
            extra = pd.DataFrame({"fecha": [str(d.date()) for d in fechas]})
            for c in df.columns:
                if c != "fecha":
                    extra[c] = df[c].iloc[0]
            df = pd.concat([extra, df], ignore_index=True)
            df.loc[df["fecha"] == anio, "cierre"] = 0.0
            if not (df["fecha"] == anio).any():
                df.loc[df.index[df["fecha"] > anio][0], "cierre"] = 0.0
            df.to_csv(datos / f"{s}.csv", index=False)
        b = Bloque(cargar_config(extra={"modo": "backtest", "perfiles": {"activos": TODOS}}), ProveedorCSV(datos),
                   cargar_universo(tmp / "u.csv"), MockClient(), tmp / "e", tmp / "s")
        try:
            r = b.ciclo(AS_OF, alcance={"clases": ["DIV"]})
        except Exception as e:  # noqa: BLE001
            res.append((f"D/{anio}", "HALLAZGO", f"cae {type(e).__name__}"))
            print(f"  HALLAZGO  D/{anio} cae {type(e).__name__}: {e}")
            continue
        ops = len(r["paquete"]["clases"]["DIV"]["opciones"])
        lim = [x[:120] for x in r["paquete"]["limitaciones"] if "Divisas" in x or "HT-01" in x]
        v = "OK" if ops > 0 or (r["estado"] == "PARCIAL" and lim) else "HALLAZGO"
        det = f"estado={r['estado']} opciones={ops} limitaciones={lim}"
        print(f"  {v:9s} D/{anio} {det}")
        res.append((f"D/{anio}", v, det))


PARTES = sys.argv[1] if len(sys.argv) > 1 else "ABCD"   # p. ej., «C» para repetir solo la parte C (también en HEAD)
for letra, fn in (("A", parte_a), ("B", parte_b), ("C", parte_c), ("D", parte_d)):
    if letra in PARTES:
        fn()
print("\n== Resumen")
for n, v, d in res:
    if v != "OK":
        print(f"  {v:9s} {n:44s} {d[:150]}")
print(f"HALLAZGOS: {sum(1 for _, v, _ in res if v == 'HALLAZGO')} · INFO: {sum(1 for _, v, _ in res if v == 'INFO')} · "
      f"OK: {sum(1 for _, v, _ in res if v == 'OK')}")
