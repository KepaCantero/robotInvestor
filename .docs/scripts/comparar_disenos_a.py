"""Compara el Bloque A V5 (referencia) y V6 (aspirante, T-101) en el mismo ciclo con el cliente simulado, sin coste.

Uso (desde la raíz del repositorio):
  .venv/bin/python .docs/scripts/comparar_disenos_a.py <carpeta> [--as-of 2026-06-05] [--perfiles RV,RF,...] [--semanas N]
                                                          [--config extra.yaml]
Ejecuta `--semanas` ciclos C1 semanales (por defecto 1) desde `--as-of` con los datos sintéticos de ejemplo, una vez con
`diseno: v5` y otra con `diseno: v6`, y deja en <carpeta>:
- `comparacion.json`: por diseño, llamadas y tokens (entrada, escritura y lectura de caché, salida) por agente, opciones
  entregadas por tipo, y la coincidencia de la selección entre los dos diseños;
- `comparacion.md`: el resumen en tablas.

Solo mide flujo y consumo: la salida del simulador no es representativa y NO dice nada de la calidad (decisión 1 de la
tanda 1; la calidad se mide en el modo sombra con la API real). La carpeta se reemplaza.
"""
from __future__ import annotations

import argparse
import collections
import json
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
EJECUTOR = RAIZ / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJECUTOR))

import pandas as pd
import yaml
from bloque_a.configuracion import (
    CLASES,
    RUTA_UNIVERSO_EJEMPLO,
    cargar_config,
    fusionar,
)
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque

DATOS = EJECUTOR / "ejemplos" / "datos_sinteticos"


def ejecutar(diseno: str, carpeta: Path, as_of: str, perfiles: list[str], semanas: int, extra: dict) -> dict:
    cfg = cargar_config(extra=fusionar({"modo": "backtest", "diseno": diseno, "perfiles": {"activos": perfiles},
                                        "evaluacion": {"bootstrap_replicas": 300, "simulaciones_ece": 300}}, extra))
    cli = MockClient()
    b = Bloque(cfg, ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), cli, carpeta / "estado", carpeta / "ent")
    runs = []
    for k in range(semanas):
        fecha = str((pd.Timestamp(as_of) + pd.Timedelta(days=7 * k)).date())
        r = b.ciclo(fecha)
        runs.append({"as_of": fecha, "estado": r["estado"], "g3": r["g3"]["dictamen"],
                     "opciones": {c: [o["indicador_seguimiento"]["simbolo"] for o in d["opciones"]] for c, d in r["paquete"]["clases"].items()}})
    por_agente: dict = collections.defaultdict(lambda: {"llamadas": 0, "entrada": 0, "cache_escritura": 0, "cache_lectura": 0, "salida": 0})
    for x in b.contabilidad.llamadas:
        a = por_agente[x["agente"]]
        a["llamadas"] += 1
        for k in ("entrada", "cache_escritura", "cache_lectura", "salida"):
            a[k] += x[k]
    tot = {k: sum(a[k] for a in por_agente.values()) for k in ("llamadas", "entrada", "cache_escritura", "cache_lectura", "salida")}
    tot["entrada_total"] = tot["entrada"] + tot["cache_escritura"] + tot["cache_lectura"]
    return {"diseno": diseno, "runs": runs, "total": tot, "por_agente": dict(sorted(por_agente.items()))}


def coincidencia(a: dict, b: dict) -> dict:
    out = {}
    for ra, rb in zip(a["runs"], b["runs"]):
        por_tipo = {}
        for c in sorted(set(ra["opciones"]) | set(rb["opciones"])):
            x, y = set(ra["opciones"].get(c, [])), set(rb["opciones"].get(c, []))
            por_tipo[c] = {"v5": len(x), "v6": len(y), "comunes": len(x & y)}
        out[ra["as_of"]] = por_tipo
    return out


def _n(x: int) -> str:
    return f"{x:,}".replace(",", ".")


def _r(x: float) -> str:
    return f"{x:.2f}".replace(".", ",")


def informe_md(res: dict) -> str:
    v5, v6 = res["v5"]["total"], res["v6"]["total"]
    filas = ["| Métrica | V5 | V6 | V6 / V5 |", "| --- | --- | --- | --- |"]
    for k, nombre in (("llamadas", "Llamadas"), ("entrada_total", "Tokens de entrada (con caché)"), ("cache_lectura", "Leídos de caché"),
                      ("cache_escritura", "Escritos en caché"), ("entrada", "Entrada sin caché"), ("salida", "Salida (simulada)")):
        filas.append(f"| {nombre} | {_n(v5[k])} | {_n(v6[k])} | {_r(v6[k] / v5[k])} |" if v5[k] else f"| {nombre} | 0 | {_n(v6[k])} | — |")
    ag = ["| Agente | V5 llamadas | V6 llamadas |", "| --- | --- | --- |"]
    for a in sorted(set(res["v5"]["por_agente"]) | set(res["v6"]["por_agente"])):
        ag.append(f"| {a} | {res['v5']['por_agente'].get(a, {}).get('llamadas', 0)} | {res['v6']['por_agente'].get(a, {}).get('llamadas', 0)} |")
    sel = ["| Fecha | Tipo | V5 | V6 | En común |", "| --- | --- | --- | --- | --- |"]
    for f, tipos in res["coincidencia"].items():
        for c, d in tipos.items():
            sel.append(f"| {f} | {c} | {d['v5']} | {d['v6']} | {d['comunes']} |")
    return ("# Bloque A: V5 frente a V6 con el simulador\n\n"
            f"Perfiles: {', '.join(res['perfiles'])} · desde {res['as_of']} · {res['semanas']} ciclo(s) C1. **Solo flujo y consumo**: "
            "la salida del simulador no es representativa y no dice nada de la calidad.\n\n## Consumo\n\n" + "\n".join(filas)
            + "\n\n## Llamadas por agente\n\n" + "\n".join(ag) + "\n\n## Opciones entregadas\n\n" + "\n".join(sel) + "\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("carpeta")
    ap.add_argument("--as-of", default="2026-06-05")
    ap.add_argument("--perfiles", default=",".join(CLASES))
    ap.add_argument("--semanas", type=int, default=1)
    ap.add_argument("--config")
    a = ap.parse_args(argv)
    carpeta = Path(a.carpeta)
    shutil.rmtree(carpeta, ignore_errors=True)
    extra = yaml.safe_load(Path(a.config).read_text(encoding="utf-8")) if a.config else {}
    perfiles = [x for x in a.perfiles.split(",") if x]
    res = {"as_of": a.as_of, "perfiles": perfiles, "semanas": a.semanas}
    for d in ("v5", "v6"):
        res[d] = ejecutar(d, carpeta / d, a.as_of, perfiles, a.semanas, extra or {})
    res["coincidencia"] = coincidencia(res["v5"], res["v6"])
    (carpeta / "comparacion.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    md = informe_md(res)
    (carpeta / "comparacion.md").write_text(md, encoding="utf-8")
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
