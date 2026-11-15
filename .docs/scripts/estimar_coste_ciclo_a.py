"""Estima el coste en USD de un ciclo del Bloque A con la API real, sin gastar nada (T-129).

Lee el `llamadas.json` que deja `medir_consumo_a.py` (una fila por llamada del cliente simulado) y le aplica una tarifa
(`bloque_a/11_Ejecutor/config/precios_anthropic.yaml` u otra con las mismas claves). Da dos cifras:
- **suelo:** la entrada que mide el simulador (prompts de sistema y encargos, con su caché) y la salida simulada, que es
  mucho más corta que la de un modelo y no lleva el razonamiento adaptativo, que se cobra como salida. No es un valor
  central: el coste real queda por encima (T-133, H-02);
- **cota superior** (T-133, H-01): la entrada multiplicada por `factor_tokens_cota` y pagada entera como escritura de
  caché (las llamadas en paralelo pueden no leer la caché de otra), toda la salida hasta `max_tokens` (que incluye el
  razonamiento) y, en los agentes con búsqueda web, cada continuación de `pause_turn` (`llm.max_continuaciones_pause_turn`)
  reenvía la entrada y puede hacer otras `busqueda_web.max_usos_por_llamada` búsquedas. Lo que se lee en una búsqueda se
  cobra como entrada y no se puede saber sin la API: queda fuera (se dice en la salida).

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
            max_usos: int, factor_tokens: float = 1.0, continuaciones: int = 0) -> dict:
    tot = {"estimacion": 0.0, "cota_superior": 0.0, "busquedas_cota": 0}
    por_modelo: dict[str, dict] = collections.defaultdict(lambda: {"llamadas": 0, "estimacion": 0.0, "cota_superior": 0.0})
    for x in llamadas:
        p = precios.get(x["modelo"])
        if p is None or any(p.get(k) is None for k in ("entrada", "salida", "escritura_cache", "lectura_cache")):
            raise SystemExit(f"sin tarifa para {x['modelo']}: añádala al fichero de precios")
        escr, lect = x.get("cache_escr", 0), x.get("cache_lect", 0)
        entrada = max(0, x["sys_tok"] + x["user_tok"] - escr - lect)      # lo que no sale de la caché ni se escribe en ella
        est = _coste(p, entrada, x["out_tok"], escr, lect)
        entrada_cota = (x["sys_tok"] + x["user_tok"]) * factor_tokens     # toda como escritura de caché, sin lecturas
        vueltas = 1 + (continuaciones if x["agente"] in agentes_busqueda else 0)
        cota = vueltas * _coste(p, 0, 0, entrada_cota, 0) + _coste(p, 0, x["max_tokens"], 0, 0)
        if x["agente"] in agentes_busqueda:
            tot["busquedas_cota"] += max_usos * vueltas
            cota += max_usos * vueltas * precio_busqueda_mil / 1000
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
                int(bw.get("max_usos_por_llamada", 0)), float(tarifa.get("factor_tokens_cota", 1.0)),
                int((cfg.get("llm") or {}).get("max_continuaciones_pause_turn", 0)))
    print(f"{r['llamadas']} llamadas · suelo {r['estimacion']:.2f} USD · cota superior {r['cota_superior']:.2f} USD "
          f"(con hasta {r['busquedas_cota']} búsquedas web)")
    for m, v in r["por_modelo"].items():
        print(f"  {m:20} llamadas {v['llamadas']:3} · suelo {v['estimacion']:.3f} · cota {v['cota_superior']:.3f}")
    print("No incluye: los tokens de lo que lee cada búsqueda web, reintentos ni reparaciones de JSON. El suelo no cuenta el "
          "razonamiento adaptativo, que se cobra como salida; la cota sí (cabe en max_tokens).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
