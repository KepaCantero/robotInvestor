"""T-165 QA r01 · falsos positivos en ciclos simulados normales (sin siembra) y comparación de los entregables con la versión
anterior a T-165.

Ejecuta, con el cliente simulado y sin red ni gasto, ciclos de varios tipos y fechas (diseño V5 con los doce tipos, varias
semanas seguidas y fechas de 2024 a 2026; diseño V6; configuración por defecto, solo DIV) y deja en `--salida`:
- `resumen.json`: por ciclo, los G3V- (fase, dictamen efectivo, resultado de G3-MET-13), las fichas que cita cada entregable y
  las palabras de madurez que contiene;
- los entregables (técnico, visual y JSON) con un nombre estable por escenario y ciclo, para compararlos con `diff -r` (el
  técnico cita la ruta de trabajo de sus hermanos: se normaliza con
  `sed -E 's#[^`]*/_trabajo_[^/]+/#T/#g'` antes de comparar).

Se lanza desde `bloque_a/11_Ejecutor` de la copia que se quiere medir (importa el paquete de esa carpeta):
    ../../.venv/bin/python <ruta>/r01_03_ciclos_normales.py --salida /ruta/salida
Para comparar con la versión anterior a T-165, se ejecuta también desde una exportación de HEAD con `ht09.py`, `sintesis.py` y
`redaccion.py` de HEAD~1 y sin la expresión de T-165 en `orquestacion.py` (ver qa.md), y se comparan las dos salidas con
`diff -r` (el `resumen.json` difiere por G3-MET-13, que no existe antes).
"""
import argparse
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

import pandas as pd

RAIZ = Path.cwd()
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "tests"))
from conftest import config_pruebas, nuevo_bloque  # noqa: E402

from bloque_a import sintesis as sint  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402

assert Path(sint.__file__).resolve().is_relative_to(RAIZ.resolve()), f"importa otra copia: {sint.__file__}"
RE_FICHA = re.compile(r"(?<![\w-])([A-Z]+(?:-[A-Z][A-Z0-9]*)+-\d{3})(?!\w|-\w)")
RE_PALABRA = re.compile(r"(?<!\w)(validad\w*|valid[oó]\w*|implementad\w*|documentad\w*|verificad\w*)", re.IGNORECASE)

ESCENARIOS = {
    "v5_12tipos_2026": (lambda: config_pruebas(), ["2026-06-05", "2026-06-12"]),
    "v5_12tipos_2025": (lambda: config_pruebas(), ["2025-01-10", "2025-01-17", "2025-01-24"]),
    "v5_12tipos_2024": (lambda: config_pruebas(), ["2024-03-01"]),
    "v6_12tipos": (lambda: config_pruebas(diseno="v6", auditoria={"en_backtest": True}), ["2026-06-05", "2025-01-10"]),
    "por_defecto_div": (lambda: cargar_config(extra={"modo": "backtest"}), ["2024-02-02", "2024-02-09"]),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", required=True)
    ap.add_argument("--escenarios", nargs="*", default=sorted(ESCENARIOS))
    a = ap.parse_args()
    salida = Path(a.salida)
    shutil.rmtree(salida, ignore_errors=True)
    salida.mkdir(parents=True)
    universo = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
    resumen, problemas = {}, []
    for esc in a.escenarios:
        cfg_f, fechas = ESCENARIOS[esc]
        with tempfile.TemporaryDirectory(dir=salida, prefix="_trabajo_") as tmp:   # se borra al terminar
            b = nuevo_bloque(Path(tmp), universo, cfg=cfg_f())
            for i, fecha in enumerate(fechas):
                r = b.ciclo(fecha)
                g3 = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "G3V" and e["run_id"] == r["run_id"]]
                filas = []
                for e in g3:
                    met = next((c for c in e["comprobaciones"] if c["id"] == "G3-MET-13"), None)
                    filas.append([e.get("fase"), e["dictamen_efectivo"], met["resultado"] if met else None,
                                  (met or {}).get("detalle", [])[:3]])
                    if met and met["resultado"] != "OK":
                        problemas.append((esc, fecha, e.get("fase"), met["detalle"][:3]))
                ent = {}
                for k, v in (r.get("entregables") or {}).items():
                    t = Path(v).read_text(encoding="utf-8")
                    ext = Path(v).suffix
                    (salida / f"{esc}_{i}_{k}{ext}").write_text(t, encoding="utf-8")
                    ent[k] = {"bloqueado": "_bloqueados" in v, "fichas": sorted(set(RE_FICHA.findall(t))),
                              "palabras": sorted({m.lower() for m in RE_PALABRA.findall(t)})}
                n_op = sum(len(d["opciones"]) for d in r["paquete"]["clases"].values())
                resumen[f"{esc}_{i}"] = {"fecha": fecha, "run_id": r["run_id"], "g3": filas, "opciones": n_op,
                                         "entrega": r.get("entrega"), "entregables": ent}
                print(esc, fecha, r["run_id"], "opciones", n_op, [(f[0], f[1], f[2]) for f in filas], flush=True)
    (salida / "resumen.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
    print("G3-MET-13 distinto de OK:", problemas or "ninguno")
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main())
