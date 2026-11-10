"""r01_01 · QA T-65 · H-10 (c), H-15 y H-16 contra datos raros, a través del ciclo completo.

Uso (desde bloque_a/11_Ejecutor):  ../../.venv/bin/python ../../.docs/tickets/T-65/revisores/r01_01_datos_raros.py

Parte A: un símbolo nuevo de DIV con datos raros (los casos de r2_06 de la QA de T-53 y otros nuevos: CSV binario, vacío,
sin columnas, fechas ilegibles, inf, desordenado). Esperado: el ciclo no cae, el símbolo se excluye y se declara, DIV
conserva opciones, estado PARCIAL.
Parte B: historia parcial (casos e y g de r2_01 de la QA de T-53). Esperado: clústeres calculados para el resto.
Parte C: el proxy de una opción VIGENTE pasa a tener datos inválidos la semana siguiente (vigentes, clústeres, GC0).
Parte D: dos proxies medibles (≥ min_semanas_proxy) sin solape: ¿vuelve a rechazarse ML-CLUS-001 para todos?
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

AS_OF = "2026-06-05"
SIG = "2026-06-12"
F = list(pd.bdate_range("2023-01-02", AS_OF))
LINEA = "{s},DIV,Dólar frente a nueva divisa,ESTRATEGIA,GLB,G10,USD,SOLO EJEMPLO,Pares,Par nuevo,Otros cruces,USD/{s},\n"
TMP = pathlib.Path(tempfile.mkdtemp(prefix="r01_01_"))
resumen = []


def preparar(series: dict) -> pathlib.Path:
    tmp = pathlib.Path(tempfile.mkdtemp(dir=TMP))
    datos = tmp / "datos"
    shutil.copytree(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos", datos)
    uni = pathlib.Path(RUTA_UNIVERSO_EJEMPLO).read_text(encoding="utf-8").rstrip("\n") + "\n"
    for s, contenido in series.items():
        (datos / f"{s}.csv").write_bytes(contenido if isinstance(contenido, bytes) else contenido.encode("utf-8"))
        uni += LINEA.format(s=s)
    (tmp / "u.csv").write_text(uni, encoding="utf-8")
    return tmp


def bloque(tmp, datos=None):
    todos = ["RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV"]
    return Bloque(cargar_config(extra={"modo": "backtest", "perfiles": {"activos": todos}}), ProveedorCSV(datos or tmp / "datos"),
                  cargar_universo(tmp / "u.csv"), MockClient(), tmp / "e", tmp / "s")


def csv(filas):
    return "fecha,cierre\n" + "".join(f"{d},{v}\n" for d, v in filas)


def caso(nombre, series: dict, espera_invalido=True):
    tmp = preparar(series)
    try:
        b = bloque(tmp)
        r = b.ciclo(AS_OF, alcance={"clases": ["DIV"]})
    except Exception as e:  # noqa: BLE001
        print(f"[{nombre}] EXCEPCIÓN {type(e).__name__}: {str(e)[:200]}")
        resumen.append((nombre, "HALLAZGO", f"excepción {type(e).__name__}"))
        return
    run = r["run_id"]
    inval = b._datos_invalidos.get(("DIV", run))
    excl = b._sin_historia.get(("DIV", run))
    ops = len(r["paquete"]["clases"]["DIV"]["opciones"])
    lim = [x[:170] for x in r["paquete"]["limitaciones"] if "Divisas" in x or "clúster" in x]
    incs = [x for x in b.almacen.leer("HA") if x.get("tipo") == "DATOS" and x.get("objeto") in series]
    print(f"[{nombre}] invalidos={inval} sin_historia={excl} opciones={ops} estado={r['estado']} incidencias={len(incs)}\n"
          f"      limitaciones={lim}")
    declarado = bool(inval or excl) and r["estado"] == "PARCIAL"
    ok = ops > 0 and (declarado if espera_invalido else True)
    resumen.append((nombre, "OK" if ok else "HALLAZGO", f"ops={ops} estado={r['estado']} inval={inval} excl={excl}"))


print("== Parte A: datos raros de un símbolo nuevo")
caso("control", {}, espera_invalido=False)
caso("cero", {"USDNEW=X": csv((d.date(), "0") for d in F)})
caso("negativo", {"USDNEW=X": csv((d.date(), f"-1.{i % 9}") for i, d in enumerate(F))})
caso("un_cero_en_medio", {"USDNEW=X": csv((d.date(), "0" if i == 400 else f"1.0{i % 9}") for i, d in enumerate(F))})
caso("duplicadas", {"USDNEW=X": csv([(d.date(), f"1.0{i % 9}") for i, d in enumerate(F)] + [(F[-1].date(), "1.5")])})
caso("inf", {"USDNEW=X": csv((d.date(), "inf" if i == 300 else f"1.0{i % 9}") for i, d in enumerate(F))})
caso("binario", {"USDNEW=X": bytes(range(256)) * 20})
caso("vacio_0_bytes", {"USDNEW=X": b""})
caso("sin_columna_cierre", {"USDNEW=X": "fecha,precio\n" + "".join(f"{d.date()},1.0\n" for d in F)})
caso("fecha_ilegible", {"USDNEW=X": csv([(d.date(), f"1.0{i % 9}") for i, d in enumerate(F)] + [("31/31/2024", "1.0")])})
caso("desordenadas", {"USDNEW=X": csv(reversed([(d.date(), f"1.0{i % 9}") for i, d in enumerate(F)]))}, espera_invalido=False)
caso("dos_invalidos_y_uno_corto", {"USDNEW=X": csv((d.date(), "0") for d in F),
                                   "USDNEW2=X": csv([(d.date(), "1.0") for d in F] + [(F[5].date(), "1.1")]),
                                   "USDNEW3=X": csv((d.date(), f"1.0{i % 9}") for i, d in enumerate(pd.bdate_range("2026-05-22", AS_OF)))})

print("\n== Parte B: historia parcial (QA T-53, r2_01 e y g)")
bd = pd.bdate_range
caso("e_hueco_2021_y_vuelve", {"USDNEW=X": csv((d.date(), f"1.0{i % 9}") for i, d in
                                               enumerate(list(bd("2019-01-01", "2021-12-31")) + list(bd("2026-05-22", AS_OF))))},
     espera_invalido=False)
caso("g_dos_cortos", {"USDNEW=X": csv((d.date(), f"1.0{i % 9}") for i, d in enumerate(bd("2026-05-22", AS_OF))),
                      "USDNEW2=X": csv((d.date(), f"1.0{i % 9}") for i, d in enumerate(bd("2026-05-22", AS_OF)))},
     espera_invalido=False)

print("\n== Parte C: el proxy de una opción vigente se vuelve inválido la semana siguiente")
for nombre, corromper in (("dup", lambda t: t + t.splitlines()[-1] + "\n"),
                          ("cero_semana", lambda t: "\n".join(
                              (ln.rsplit(",", 2)[0] + ",0," + ln.rsplit(",", 1)[1]) if ln.startswith("2026-06-1") else ln
                              for ln in t.splitlines()) + "\n"),
                          ("binario", lambda t: bytes(range(256)) * 20)):
    tmp = preparar({})
    b = bloque(tmp)
    r1 = b.ciclo(AS_OF, alcance={"clases": ["DIV"]})
    prox = r1["paquete"]["clases"]["DIV"]["opciones"][0]["indicador_seguimiento"]["simbolo"]
    datos2 = tmp / "datos2"
    shutil.copytree(tmp / "datos", datos2)
    ruta = datos2 / f"{prox}.csv"
    nuevo = corromper(ruta.read_text(encoding="utf-8"))
    ruta.write_bytes(nuevo if isinstance(nuevo, bytes) else nuevo.encode("utf-8"))
    b2 = bloque(tmp, datos2)
    for tipo, kw in (("PERIODICO", {}), ("AD_HOC_N1", {"tipo": "AD_HOC", "nivel_forzado": "N1"})):
        try:
            r2 = b2.ciclo(SIG, alcance={"clases": ["DIV"]}, **kw)
            run = r2["run_id"]
            ops2 = [o["indicador_seguimiento"]["simbolo"] for o in r2["paquete"]["clases"]["DIV"]["opciones"]]
            lim = [x[:150] for x in r2["paquete"]["limitaciones"] if prox in x or "clúster" in x]
            print(f"[C/{nombre}/{tipo}] proxy={prox} estado={r2['estado']} invalidos={b2._datos_invalidos.get(('DIV', run))} "
                  f"opciones={ops2}\n      limitaciones={lim}")
            ok = prox not in ops2 or bool(lim)
            resumen.append((f"C/{nombre}/{tipo}", "OK" if ok else "HALLAZGO", f"estado={r2['estado']} proxy_publicado={prox in ops2}"))
        except Exception as e:  # noqa: BLE001
            print(f"[C/{nombre}/{tipo}] EXCEPCIÓN {type(e).__name__}: {str(e)[:200]}")
            resumen.append((f"C/{nombre}/{tipo}", "HALLAZGO", f"excepción {type(e).__name__}: {str(e)[:80]}"))
        b2 = bloque(tmp, datos2)

print("\n== Parte D: dos proxies medibles sin solape")
viejo = list(bd("2023-04-03", "2024-12-27"))          # ≈ 90 semanas, deja de cotizar
nuevo = list(bd("2025-03-03", AS_OF))                  # ≈ 66 semanas, empieza después
tmp = preparar({"USDOLD=X": csv((d.date(), f"1.0{i % 9}") for i, d in enumerate(viejo)),
                "USDNEW=X": csv((d.date(), f"1.{i % 7}") for i, d in enumerate(nuevo))})
b = bloque(tmp)
b.fijar_fecha(AS_OF)
an = {"DIV": {"finalistas": [{"proxy": p, "_gc3": True} for p in ("EURUSD=X", "USDJPY=X", "USDOLD=X", "USDNEW=X")]}}
cl = b._clusteres(an, AS_OF, "RUN-2026-0001")
print(f"[D] rechazo={cl.get('rechazo')} sin_historia={cl.get('sin_historia')} asignacion={cl['asignacion']}")
resumen.append(("D/sin_solape", "INFO" if cl.get("rechazo") else "OK", f"rechazo={cl.get('rechazo')}"))

print("\n== Parte E: CSV ilegible y ciclo con todos los tipos (¿cae todo el ciclo por un símbolo?)")
for nombre, contenido in (("vacio_0_bytes", b""), ("binario", bytes(range(256)) * 20)):
    tmp = preparar({"USDNEW=X": contenido})
    try:
        r = bloque(tmp).ciclo(AS_OF)
        resumen.append((f"E/{nombre}", "OK", f"estado={r['estado']}"))
        print(f"[E/{nombre}] estado={r['estado']}")
    except Exception as e:  # noqa: BLE001
        print(f"[E/{nombre}] EXCEPCIÓN {type(e).__name__}: {str(e)[:150]}")
        resumen.append((f"E/{nombre}", "HALLAZGO", f"el ciclo de los 12 tipos cae: {type(e).__name__}"))

print("\n== Resumen")
for n, v, d in resumen:
    print(f"  {v:9s} {n:32s} {d}")
print(f"HALLAZGOS: {sum(1 for _, v, _ in resumen if v == 'HALLAZGO')} · INFO: {sum(1 for _, v, _ in resumen if v == 'INFO')}")
