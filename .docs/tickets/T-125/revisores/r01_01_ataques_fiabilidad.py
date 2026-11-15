"""QA r01 de T-125 (revisor sin contexto): ataques a `Evaluador.pronosticos_de_fuentes` / `fiabilidad_fuentes` y al CT-19.

Uso, desde `bloque_a/11_Ejecutor`:  python ../../.docs/tickets/T-125/revisores/r01_01_ataques_fiabilidad.py
Imprime una línea por ataque con lo obtenido. No cambia nada del repositorio (todo en un directorio temporal).
"""
import json
import os
import sys
import tempfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path.cwd() / "tests"))
from conftest import AS_OF, RUTA_UNIVERSO_EJEMPLO, cargar_universo, config_pruebas, nuevo_bloque  # noqa: E402


UNIVERSO = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
SERIE = "SPY"
TMP = Path(tempfile.mkdtemp(prefix="qa7_t125_", dir=os.environ.get("QA_TMP")))
_n = [0]


def bloque():
    _n[0] += 1
    b = nuevo_bloque(TMP / f"b{_n[0]}", UNIVERSO)
    b.fijar_fecha(AS_OF)
    return b


def clm(b, i, ref_id, objetivo, umbral, direccion="por_encima", prob=0.7, emision=None, texto=None, **extra):
    pf = {"ref_id": ref_id, "variable": "cierre", "serie_ht01": SERIE, "fecha_objetivo": objetivo, "umbral_o_rango": umbral,
          "direccion": direccion, "probabilidad": prob,
          "fecha_emision": emision or str((pd.Timestamp(objetivo) - pd.Timedelta(days=30)).date()), **extra}
    if prob is None:
        pf.pop("probabilidad")
    b.almacen.escribir("F2", "AG-12", {"tipo_entrada": "CLM", "clm_id": f"CLM-2025-{i:04d}", "afirmacion": texto or f"{ref_id} {i}",
                                       "tipo_afirmacion": "PRONOSTICO_FUENTE", "pronostico_fuente": pf})


def sembrar(b, ref_id, aciertos, fallos, desde="2025-01-06", inicio=1, prob=0.7):
    for i, f in enumerate(pd.bdate_range(desde, periods=aciertos + fallos)):
        _, v = b.proveedor.valor_en(SERIE, f)
        clm(b, inicio + i, ref_id, str(f.date()), v - 1 if i < aciertos else v + 1, prob=prob)


def linea(nombre, obtenido, esperado_por_revisor):
    print(f"[{nombre}] obtenido: {obtenido} | lo que pediría el revisor: {esperado_por_revisor}")


# A1 · registro tardío: la pieza entra en F2 cuando su fecha objetivo ya pasó (el resultado era conocido al registrarla)
b = bloque()
sembrar(b, "REF-0001", 5, 0)                                  # escritas con el reloj en AS_OF (2026-06-05), objetivos en 2025
ps = b.evaluador.pronosticos_de_fuentes(AS_OF)
linea("A1 registro posterior a la fecha objetivo", f"{len(ps)} de 5 cuentan",
      "no deberían contar (F2: «conocible_desde ... es el filtro anti-fuga»; Doc. 0 12.2: sin fuga)")

# A2 · ref_id arbitrario: el ejecutor no comprueba que sea una fuente (RF-/REF-) conocida
b = bloque()
for k, ref in enumerate(["cualquier cosa", "OPP-2026-0001", "REF-9999"]):
    sembrar(b, ref, 5, 0, inicio=1 + 100 * k)
fue = b.evaluador.fiabilidad_fuentes(AS_OF)
linea("A2 ref_id sin validar", sorted(f["ref_id"] for f in fue), "ninguna FUE- (fuentes inexistentes o que no son fuentes)")

# A3 · el mismo pronóstico de la fuente en dos afirmaciones (texto distinto): ¿cuenta dos veces?
b = bloque()
f = pd.bdate_range("2025-01-06", periods=5)
for i, d in enumerate(f):
    _, v = b.proveedor.valor_en(SERIE, d)
    for rep in range(2):
        clm(b, 1 + 2 * i + rep, "REF-0001", str(d.date()), v - 1, texto=f"REF-0001 dice {i} (mención {rep})",
            emision="2024-12-01")
fue = b.evaluador.fiabilidad_fuentes(AS_OF)
linea("A3 mismo pronóstico en dos CLM", f"n = {[x['n'] for x in fue]}", "n = 5 (contar raíces, no menciones; R10)")

# A4 · una vez al mes con dos ciclos del mismo mes, y una segunda fuente que llega a n_min a mitad de mes
b = bloque()
sembrar(b, "REF-0001", 5, 0)
r1 = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
sembrar(b, "REF-0002", 5, 0, inicio=500)
r2 = b.ciclo("2026-06-12", alcance={"clases": ["RV"]})
fues = [e for e in b.almacen.estado("F6", clave="id").values() if e.get("tipo_entrada") == "FUE"]
ct19 = [m for m in b.mensajeria.registro if m["contrato"] == "CT-19" and m["receptor"] == "AG-16"]
linea("A4 dos ciclos en junio", f"FUE- = {[(e['ref_id'], e['periodo'], bool(e.get('comunicado_ct19'))) for e in fues]}, CT-19 = {len(ct19)}",
      "una FUE- por fuente y mes (INC-T125-01): REF-0002 también")
r3 = b.ciclo("2026-07-03", alcance={"clases": ["RV"]})
fues = [e for e in b.almacen.estado("F6", clave="id").values() if e.get("tipo_entrada") == "FUE"]
linea("A4b julio", f"FUE- = {[(e['ref_id'], e['periodo']) for e in fues]}", "una por fuente en julio")

# A5 · probabilidades raras
b = bloque()
_, v = b.proveedor.valor_en(SERIE, "2025-06-02")
raras = [0, 1, 0.0, 1.0, 1e-9, 1 - 1e-9, float("nan"), float("inf"), -0.2, "0.7", 70, None, [0.7], 0.5]
for i, p in enumerate(raras):
    clm(b, 700 + i, f"REF-P{i:02d}", "2025-06-02", v - 1, prob=p)
ps = {p["ref_id"]: p["prob"] for p in b.evaluador.pronosticos_de_fuentes(AS_OF)}
linea("A5 probabilidades", {repr(raras[int(k[-2:])]): ps[k] for k in sorted(ps)},
      "0 < p < 1 o sin declarar (→ prob_sin_declarar); el resto fuera")

# A6 · fechas
b = bloque()
_, v = b.proveedor.valor_en(SERIE, "2025-06-02")
casos = {"con hora": ("2025-06-02T23:59:00", "2025-05-01"), "con zona": ("2025-06-02T10:00:00+05:00", "2025-05-01"),
         "inexistente 30-feb": ("2025-02-30", "2025-01-01"), "objetivo = as_of": (AS_OF, "2026-05-01"),
         "objetivo = emisión": ("2025-06-02", "2025-06-02"), "objetivo > as_of por un día": ("2026-06-06", "2026-05-01"),
         "borde de la ventana (24 meses justos)": ("2024-06-05", "2024-05-01"),
         "un día fuera de la ventana": ("2024-06-04", "2024-05-01"), "fecha como número": (20250602, "2025-05-01"),
         "emisión futura respecto a as_of": ("2025-06-02", "2027-01-01")}
res6 = {}
for i, (k, (obj, emi)) in enumerate(casos.items()):
    b = bloque()
    clm(b, 800 + i, f"REF-F{i:02d}", obj, v - 1, emision=emi)
    try:
        res6[k] = bool(b.evaluador.pronosticos_de_fuentes(AS_OF))
    except Exception as e:  # noqa: BLE001
        res6[k] = f"EXCEPCIÓN {type(e).__name__}: {e}"
linea("A6 fechas (True = cuenta)", res6, "con hora sí; con zona, contar o descartar sin excepción; objetivo>as_of, 30-feb y fuera de ventana no")

# A6b · una sola pieza con la fecha objetivo con zona horaria (texto del modelo) dentro de un ciclo completo
b = bloque()
sembrar(b, "REF-0001", 5, 0)
clm(b, 900, "REF-0009", "2025-06-02T10:00:00+05:00", v - 1)
try:
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    fues = [e for e in b.almacen.leer("F6") if e.get("tipo_entrada") == "FUE"]
    incs = [e.get("detalle") for e in b.almacen.leer("HA") if e.get("tipo") == "HERRAMIENTA"]
    linea("A6b-detalle", f"res_eval del run: {sorted(r.get('evaluacion') or {})}; incidencias HERRAMIENTA: {incs}",
          "la evaluación completa (certificados, lecciones…) y ninguna incidencia")
    sembrar(b, "REF-0001", 5, 0, inicio=950, desde="2025-03-03")
    r = b.ciclo("2026-07-03", alcance={"clases": ["RV"]})
    incs = [e.get("detalle") for e in b.almacen.leer("HA") if e.get("tipo") == "HERRAMIENTA"]
    linea("A6c un mes después", f"FUE- {len([e for e in b.almacen.leer('F6') if e.get('tipo_entrada') == 'FUE'])}, incidencias HERRAMIENTA {len(incs)}",
          "la pieza mala sigue en F2 (append-only) y la ventana es de 24 meses: ¿se repite cada ciclo?")
    linea("A6b ciclo con una pieza con zona horaria", f"ciclo {r.get('estado')}, entrega {r.get('entrega')}, FUE- {len(fues)}, "
          f"limitaciones del evaluador: {[x for x in r['paquete'].get('limitaciones', []) if 'valuador' in x or 'C5' in x]}",
          "la pieza mala se omite y la FUE- de REF-0001 sale")
except Exception as e:  # noqa: BLE001
    linea("A6b ciclo con una pieza con zona horaria", f"EXCEPCIÓN {type(e).__name__}: {e}", "la pieza mala se omite; el ciclo sigue")

# A7 · determinismo: el mismo escenario en dos bloques da las mismas FUE- (salvo nada)
res = []
for _ in range(2):
    b = bloque()
    sembrar(b, "REF-0001", 18, 7)
    sembrar(b, "REF-0002", 12, 13, inicio=300)
    res.append(json.dumps([{k: f[k] for k in ("fue_id", "ref_id", "n", "aciertos", "bss", "bss_contraido", "puntos_historial", "pronosticos")}
                           for f in b.evaluador.fiabilidad_fuentes(AS_OF)], sort_keys=True))
linea("A7 determinismo", res[0] == res[1], "True")

# A8 · extremos: siempre 0,99 y siempre falla (puntos acotados a 0); referencia exacta (BSS 0, puntos neutros)
b = bloque()
sembrar(b, "REF-MALA", 0, 25, prob=0.99)
sembrar(b, "REF-NEUTRA", 12, 13, inicio=200, prob=0.5)
fue = {f["ref_id"]: (f["bss"], f["bss_contraido"], f["puntos_historial"]) for f in b.evaluador.fiabilidad_fuentes(AS_OF)}
linea("A8 extremos", fue, "MALA con puntos 0 (acotados) y NEUTRA con BSS 0 y puntos 10")

# A9 · prob_sin_declarar frente a la banda «más probable que no» (0,65 en bandas_verbales)
cfg = config_pruebas()
bandas = {x["texto"]: x["prob_interna"] for x in cfg["bandas_verbales"]}
linea("A9 prob sin declarar", (cfg["fiabilidad_fuentes"]["prob_sin_declarar"], bandas.get("más probable que no")),
      "la misma cifra, si el comentario dice «más probable que no»")
print("temporal:", TMP)
