"""Estima el coste en USD de un ciclo del Bloque A con la API real, sin gastar nada (T-129).

Lee el `llamadas.json` que deja `medir_consumo_a.py` (una fila por llamada del cliente simulado) y le aplica una tarifa
(`bloque_a/11_Ejecutor/config/precios_anthropic.yaml` u otra con las mismas claves). Da dos cifras:
- **estimación:** la entrada que mide el simulador (que es la real: prompts de sistema y encargos) y la salida simulada,
  que es más corta que la de un modelo;
- **cota superior:** la misma entrada, toda la salida hasta `max_tokens` en cada llamada y, en los agentes con búsqueda
  web, todas las búsquedas que permite `busqueda_web.max_usos_por_llamada`. Lo que se lee en una búsqueda también se
  cobra como entrada y no se puede saber sin la API: queda fuera de las dos cifras (se dice en la salida).

Uso (desde la raíz):
  .venv/bin/python .docs/scripts/estimar_coste_ciclo_a.py <carpeta de medir_consumo_a> [--precios yaml] [--config yaml]
`--config` es la misma configuración adicional que se pasó a `medir_consumo_a.py` (para leer los agentes con búsqueda).
"""
import argparse
import collections
import json
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[2]
EJECUTOR = RAIZ / "bloque_a" / "11_Ejecutor"


def _config(extra: str | None) -> dict:
    sys.path.insert(0, str(EJECUTOR))
    from bloque_a.configuracion import cargar_config
    return cargar_config(extra)


def _coste(p: dict, entrada: float, salida: float, escr: float, lect: float) -> float:
    return (entrada * p["entrada"] + salida * p["salida"] + escr * p["escritura_cache"] + lect * p["lectura_cache"]) / 1e6


def estimar(llamadas: list[dict], precios: dict, precio_busqueda_mil: float, agentes_busqueda: set[str],
            max_usos: int) -> dict:
    tot = {"estimacion": 0.0, "cota_superior": 0.0, "busquedas_cota": 0}
    por_modelo: dict[str, dict] = collections.defaultdict(lambda: {"llamadas": 0, "estimacion": 0.0, "cota_superior": 0.0})
    for x in llamadas:
        p = precios.get(x["modelo"])
        if p is None or any(p.get(k) is None for k in ("entrada", "salida", "escritura_cache", "lectura_cache")):
            raise SystemExit(f"sin tarifa para {x['modelo']}: añádala al fichero de precios")
        escr, lect = x.get("cache_escr", 0), x.get("cache_lect", 0)
        entrada = max(0, x["sys_tok"] + x["user_tok"] - escr - lect)      # lo que no sale de la caché ni se escribe en ella
        est = _coste(p, entrada, x["out_tok"], escr, lect)
        cota = _coste(p, entrada, x["max_tokens"], escr, lect)
        if x["agente"] in agentes_busqueda:
            tot["busquedas_cota"] += max_usos
            cota += max_usos * precio_busqueda_mil / 1000
        tot["estimacion"] += est
        tot["cota_superior"] += cota
        m = por_modelo[x["modelo"]]
        m["llamadas"] += 1
        m["estimacion"] += est
        m["cota_superior"] += cota
    tot["llamadas"] = len(llamadas)
    tot["por_modelo"] = dict(sorted(por_modelo.items()))
    return tot


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("carpeta")
    ap.add_argument("--precios", default=str(EJECUTOR / "config" / "precios_anthropic.yaml"))
    ap.add_argument("--config", default=None)
    a = ap.parse_args(argv)
    llamadas = json.loads((Path(a.carpeta) / "llamadas.json").read_text(encoding="utf-8"))
    tarifa = yaml.safe_load(Path(a.precios).read_text(encoding="utf-8"))
    cfg = _config(a.config)
    bw = cfg.get("busqueda_web") or {}
    agentes = set(bw.get("agentes") or []) if bw.get("habilitada_en_vivo") else set()
    r = estimar(llamadas, tarifa["precios_por_millon"], float(tarifa["precio_busqueda_web_por_mil"]), agentes,
                int(bw.get("max_usos_por_llamada", 0)))
    print(f"{r['llamadas']} llamadas · estimación {r['estimacion']:.2f} USD · cota superior {r['cota_superior']:.2f} USD "
          f"(con hasta {r['busquedas_cota']} búsquedas web)")
    for m, v in r["por_modelo"].items():
        print(f"  {m:20} llamadas {v['llamadas']:3} · estimación {v['estimacion']:.3f} · cota {v['cota_superior']:.3f}")
    print("No incluye: los tokens de lo que lee cada búsqueda web, reintentos ni reparaciones de JSON.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
