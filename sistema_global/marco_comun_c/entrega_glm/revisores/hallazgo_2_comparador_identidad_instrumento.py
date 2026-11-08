"""Hallazgo 2 — comparador.py: la deduplicación por instrumento no usa la identidad de SC-1 (norm).

La cabecera de D dice que «dos análisis del mismo instrumento, sentido y clase no son alternativas:
se queda el mejor», y desde T-51 la identidad única de un instrumento es `mandatos.norm` (NFKC y solo
letras y cifras), la que usan F-07/F-15, RM-08 y el Orquestador. D deduplica con `inst.strip().upper()`,
así que dos sobres del mismo instrumento con distinta grafía («EURUSD» y «EUR/USD») se ordenan como
alternativas en vez de excluirse uno por DUPLICADO.

Uso: python3 hallazgo_2_comparador_identidad_instrumento.py   (desde la carpeta marcoC)
Imprime FALLA si el defecto existe y OK si está corregido (dedup con norm).
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]   # V0.53: movido a entrega_glm/revisores/
sys.path.insert(0, str(RAIZ / "validador"))
sys.path.insert(0, str(RAIZ / "pruebas"))

import copy

from comparador import comparar_candidatos
from mandatos import norm
from pruebas_comparador import cand
from pruebas_orquestador import AHORA

mal = []
for a, b in (("EURUSD", "EUR/USD"), ("EURUSD", "EUR-USD"), ("EURUSD", "EUR USD"), ("EURUSD", "ＥＵＲＵＳＤ")):
    assert norm(a) == norm(b)          # la identidad de SC-1 dice: el mismo instrumento
    ca = cand(1, instrumento=a)
    cb = cand(2, instrumento=b, esperado=(3.0, 0.5, -4.0))
    r = comparar_candidatos([copy.deepcopy(ca), copy.deepcopy(cb)], AHORA)
    if not r.get("ok"):
        mal.append(f"{a} vs {b}: {r.get('codigo')}")
        continue
    en_ranking = sorted(d["expediente_id"] for g in r["grupos"].values() for d in g["ranking"])
    dup = [e for e in r["excluidos"] if e["motivo"] == "DUPLICADO"]
    if len(en_ranking) == 2 and not dup:
        mal.append(f"{a} vs {b}: los dos en el ranking ({en_ranking}) y ningún DUPLICADO")
    elif len(en_ranking) == 2:
        mal.append(f"{a} vs {b}: los dos en el ranking")

# testigo de que la misma pareja con la misma grafía SÍ se deduplica (el guard existe y funciona)
r = comparar_candidatos([cand(1, instrumento="EURUSD"), cand(2, instrumento="EURUSD", esperado=(3.0, 0.5, -4.0))], AHORA)
if not any(e["motivo"] == "DUPLICADO" for e in r.get("excluidos", [])):
    mal.append("testigo roto: con la misma grafía tampoco deduplica")

print("FALLA " + ("; ".join(mal)) if mal else "OK")
sys.exit(1 if mal else 0)
