"""QA r01 de T-113 · H-24 de T-108: dominios de MON e IDX en el borde. Para cada parámetro de `DOMINIOS`, valores dentro, en
el borde y fuera, y tipos raros. Fuera del dominio: ErrorFicha. Dentro: se sirve o ErrorFicha, nunca otra excepción, y en
menos de 20 s. Además, por el Motor: RECHAZADO con entrada en RC.
Uso (desde bloque_a/11_Ejecutor de la copia): python .../r01_05_dominios_mon_idx.py"""
import copy
import os
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, ".")
from bloque_a.almacen import Almacen  # noqa: E402
from bloque_a.configuracion import cargar_config  # noqa: E402
from bloque_a.motor import fichas_mon_idx as f  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402

ErrorFicha = servicio.op.ErrorFicha
RAROS = [None, True, False, "12", "", b"1", float("nan"), float("inf"), -float("inf"), [1], {"a": 1}, (1,), 1 + 0j, np.int64(3), np.float64(3.0),
         10 ** 400, -0.0, 1e-300, 2.5, -1, 0]
fallos = avisos = 0


def probar(ficha, cambio, i=0):
    caso = servicio.CASOS_CONTROL[ficha][i]
    v = copy.deepcopy({k: x for d in caso["datos"] for k, x in (d.get("valores") or {}).items()})
    t0 = time.perf_counter()
    try:
        r, lim = servicio.IMPLEMENTADAS[ficha]["fn"]({"valores": v, "series": {}, "series_rol": {}}, {**dict(caso.get("parametros") or {}), **cambio})
        res = "SERVIDA"
    except ErrorFicha as e:
        res = "ErrorFicha: " + str(e)[:80]
    except BaseException as e:  # noqa: BLE001
        res = f"EXCEPCIÓN {type(e).__name__}: {str(e)[:80]}"
    return res, time.perf_counter() - t0


for ficha, dom in f.DOMINIOS.items():
    for clave, (tipo, lo, hi) in dom.items():
        lista = tipo.startswith("lista")
        entero = tipo in ("entero", "lista_entera")
        dentro = [lo if tipo != "real_positivo" else lo + 1e-9, hi, (lo + hi) // 2 if entero else (lo + hi) / 2]
        fuera = [lo - 1 if tipo != "real_positivo" else lo, hi + 1, hi + 1e-9 if not entero else hi + 0.5, -hi - 5]
        for x in dentro:
            res, dt = probar(ficha, {clave: [x] if lista else x})
            mal = res.startswith("EXCEPCIÓN") or dt > 20
            fallos += mal
            print(f"{'FALLO' if mal else 'ok   '} {ficha} {clave}={x!r} (dentro) -> {res[:100]} [{dt:.2f} s]")
        for x in fuera:
            res, dt = probar(ficha, {clave: [x] if lista else x})
            mal = not res.startswith("ErrorFicha") or "parámetro" not in res and "momentum" not in res
            fallos += mal
            print(f"{'FALLO' if mal else 'ok   '} {ficha} {clave}={x!r} (fuera) -> {res[:100]}")
        for x in RAROS:
            if lista and isinstance(x, (list, tuple)):
                continue
            res, dt = probar(ficha, {clave: [x] if lista else x})
            admite = isinstance(x, (int, float, np.floating)) and not isinstance(x, bool) and x == x and abs(x) != float("inf") and (
                lo < x <= hi if tipo == "real_positivo" else lo <= x <= hi) and (not entero or x == int(x))
            if res.startswith("EXCEPCIÓN") or (not admite and not res.startswith("ErrorFicha")):
                fallos += 1
                print(f"FALLO {ficha} {clave}={x!r} (raro) -> {res[:110]}")
            elif admite and res.startswith("ErrorFicha") and "parámetro" in res:
                avisos += 1
                print(f"aviso {ficha} {clave}={x!r} está en el dominio y se rechaza -> {res[:110]}")
        if lista:
            tope = f._MAX_LISTA.get(clave, 12)
            medio = (lo + hi) // 2
            for nombre, x, debe_rechazar in (("vacía", [], True), ("tope", [lo + i for i in range(tope)], False),
                                             ("tope+1", [lo + i for i in range(tope + 1)], True), ("repetidos", [medio, medio], False),
                                             ("anidada", [[medio]], True), ("texto", "abc", True), ("tupla", (medio,), False),
                                             ("None", None, True), ("dict", {medio: 1}, True), ("generador", range(1, 3), True),
                                             ("con None", [medio, None], True), ("con NaN", [medio, float("nan")], True)):
                res, dt = probar(ficha, {clave: x})
                mal = res.startswith("EXCEPCIÓN") or (debe_rechazar and not res.startswith("ErrorFicha"))
                fallos += mal
                print(f"{'FALLO' if mal else 'ok   '} {ficha} {clave} lista {nombre} -> {res[:100]}")

print("== IDX-REL: salto y retro")
for cambio in ({"momentum_salto_meses": 11, "momentum_retro_meses": 12}, {"momentum_salto_meses": 12, "momentum_retro_meses": 12},
               {"momentum_salto_meses": 0, "momentum_retro_meses": 2}, {"momentum_salto_meses": 1, "momentum_retro_meses": 2},
               {"momentum_salto_meses": 2, "momentum_retro_meses": 2}, {"momentum_salto_meses": 119, "momentum_retro_meses": 120},
               {"momentum_corto_meses": 120}, {"momentum_salto_meses": 1.0, "momentum_retro_meses": 12.0}):
    res, dt = probar("IDX-REL-001", cambio)
    print(("FALLO" if res.startswith("EXCEPCIÓN") else "ok   "), cambio, "->", res[:110]); fallos += res.startswith("EXCEPCIÓN")

print("== los parámetros por defecto y los casos de control están dentro del dominio")
for ficha in f.DOMINIOS:
    try:
        f._dominio(ficha, dict(f.PARAMETROS_POR_DEFECTO[ficha])); print("ok   ", ficha, "por defecto")
    except Exception as e:  # noqa: BLE001
        fallos += 1; print("FALLO", ficha, e)

print("== por el Motor: fuera de dominio es RECHAZADO con entrada en RC")


class _P:
    as_of = None
    nombre = "pruebas"


m = servicio.Motor(Almacen(Path(tempfile.mkdtemp(prefix="qa_t113_dom_", dir=os.environ.get("QA_TMP")))), _P(), cargar_config())
for ficha, cambio in (("IDX-REL-001", {"momentum_retro_meses": -20}), ("MON-EXP-001", {"diferencial_estable_dias": 0}),
                      ("IDX-CONC-001", {"media_amplitud": 0}), ("IDX-REB-001", {"sesiones_estimacion": -1}),
                      ("MON-YLD-001", {"plazos_meses": []}), ("MON-FIX-001", {"escenarios_pb": [1001]})):
    caso = servicio.CASOS_CONTROL[ficha][0]
    n0 = len(m.almacen.leer("RC"))
    try:
        r = m.servir({"operacion": ficha, "datos": copy.deepcopy(caso["datos"]), "parametros": {**dict(caso.get("parametros") or {}), **cambio},
                      "fecha_corte": "2026-11-12"}, "AG-03")
        mal = r["estado"] != "RECHAZADO" or len(m.almacen.leer("RC")) != n0 + 1
        print(("FALLO" if mal else "ok   "), ficha, cambio, "->", r["estado"], r.get("motivo"), str(r.get("detalle") or r.get("descripcion") or "")[:80])
    except BaseException as e:  # noqa: BLE001
        mal = True; print("FALLO", ficha, cambio, "EXCEPCIÓN", type(e).__name__, str(e)[:80])
    fallos += mal
    # y el caso de control sin tocar se sigue sirviendo por el Motor
    r = m.servir({"operacion": ficha, "datos": copy.deepcopy(caso["datos"]), "parametros": dict(caso.get("parametros") or {}), "fecha_corte": "2026-11-12"}, "AG-03")
    if r["estado"] == "RECHAZADO":
        fallos += 1; print("FALLO", ficha, "el caso de control se rechaza por el Motor:", r.get("motivo"))
print("FALLOS:", fallos, "· avisos:", avisos)
