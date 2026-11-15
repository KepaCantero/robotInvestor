"""QA r01 de T-129 · ¿la «cota superior» del estimador es una cota? Sensibilidad a lo que el simulador no puede saber.

Sobre el `llamadas.json` de `medir_consumo_a.py` (el mismo de la tabla del README) se recalcula la cota cambiando una cosa:
 a. las lecturas de caché del simulador pasan a escrituras (llamadas en paralelo con el mismo prefijo: en la API, la entrada
    de caché solo existe cuando la primera respuesta empieza; el simulador, con su cerrojo, lee al instante);
 b. los tokens del simulador (3,6 caracteres por token) × 1,35 (el margen que la documentación da al tokenizador de la
    familia 4.7 y posteriores frente a los anteriores; no es una medida: el recuento real pide count_tokens con clave);
 c. los agentes con búsqueda con pause_turn hasta max_continuaciones (1 + 3 peticiones, cada una con su entrada, su salida
    hasta max_tokens y max_usos búsquedas);
 d. el umbral de 100 000 tokens de Haiku 5.5: ¿alguna llamada lo pasa?
Uso (desde la raíz de la copia): python -I r01_02_sensibilidad_cota.py <carpeta de medir_consumo_a> [--config yaml]
"""
import importlib.util
import json
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location("est", RAIZ / ".docs" / "scripts" / "estimar_coste_ciclo_a.py")
est = importlib.util.module_from_spec(spec)
spec.loader.exec_module(est)

carpeta = Path(sys.argv[1])
extra = sys.argv[sys.argv.index("--config") + 1] if "--config" in sys.argv else None
llamadas = json.loads((carpeta / "llamadas.json").read_text(encoding="utf-8"))
tarifa = yaml.safe_load((RAIZ / "bloque_a" / "11_Ejecutor" / "config" / "precios_anthropic.yaml").read_text(encoding="utf-8"))
cfg = est._config(extra)
bw = cfg["busqueda_web"]
agentes = set(bw["agentes"]) if bw.get("habilitada_en_vivo") else set()
mu = int(bw["max_usos_por_llamada"])
cont = int(cfg["llm"]["max_continuaciones_pause_turn"])
P, PB = tarifa["precios_por_millon"], float(tarifa["precio_busqueda_web_por_mil"])


def cota(ll):
    return est.estimar(ll, P, PB, agentes, mu)


base = cota(llamadas)
print(f"base: {base['llamadas']} llamadas · estimación {base['estimacion']:.2f} · cota {base['cota_superior']:.2f}")
lect = sum(x["cache_lect"] for x in llamadas)
escr = sum(x["cache_escr"] for x in llamadas)
print(f"   tokens: lectura de caché {lect} · escritura {escr} · entrada sin caché "
      f"{sum(max(0, x['sys_tok'] + x['user_tok'] - x['cache_lect'] - x['cache_escr']) for x in llamadas)}")

a = [dict(x, cache_escr=x["cache_escr"] + x["cache_lect"], cache_lect=0) for x in llamadas]
print(f"a. sin lecturas de caché: cota {cota(a)['cota_superior']:.2f}")

f = 1.35
b = [dict(x, **{k: int(x[k] * f) for k in ("sys_tok", "user_tok", "out_tok", "cache_escr", "cache_lect")}) for x in llamadas]
print(f"b. tokens × {f}: cota {cota(b)['cota_superior']:.2f}")

c = []
for x in llamadas:
    c.append(x)
    if x["agente"] in agentes:
        # cada continuación reenvía la entrada (que ya está en caché: lectura) y puede llegar a max_tokens y max_usos
        for _ in range(cont):
            c.append(dict(x, cache_lect=x["sys_tok"] + x["user_tok"], cache_escr=0))
rc = cota(c)
print(f"c. pause_turn hasta {cont} continuaciones en {sum(1 for x in llamadas if x['agente'] in agentes)} llamadas con "
      f"búsqueda: cota {rc['cota_superior']:.2f} ({rc['busquedas_cota']} búsquedas)")

ab = cota([dict(y, cache_escr=y["cache_escr"] + y["cache_lect"], cache_lect=0) for y in b])
print(f"a+b: cota {ab['cota_superior']:.2f}")
hk = [x for x in llamadas if x["modelo"] == "claude-haiku-5-5"]
mx = max((x["sys_tok"] + x["user_tok"] for x in hk), default=0)
print(f"d. Haiku 5.5: {len(hk)} llamadas, prompt máximo {mx} tokens (umbral 100 000): "
      f"{'lo pasa' if mx > 100_000 else 'no lo pasa'}")
