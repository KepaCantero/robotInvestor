"""QA r01 de T-187: comprobaciones de los hallazgos H-01 a H-03 (para la ronda de cierre).

Uso, desde la raíz del repositorio: python3 -I .docs/tickets/T-187/revisores/r01_04_comprobaciones_cierre.py
Sale con 1 si alguna falla. Hoy (86f0385) fallan las tres.
- H-01: PB-51 no puede salir «Superada» mientras una cláusula del criterio (tamaños de los 21 papeles sin orientación)
  quede sin comprobar y el resultado esperado («ninguna afirmación técnica errónea») no se cumpla: cobertura PARCIAL y
  «No comprueba» con las dos cosas.
- H-02: cada prompt con 10 afirmaciones técnicas verificables juzgadas (o todas sus candidatas técnicas, declarado).
- H-03: lo que comentario.json atribuye a los revisores está en sus notas: cada «discutible» lleva «discutib» en la nota
  de su lote, y ningún matiz de una dudosa afirma una búsqueda que la nota no recoge.
"""
import collections
import json
import sys
from pathlib import Path

TICKET = Path(__file__).resolve().parents[1]
RAIZ = TICKET.parents[2]
fallos = []

mapa = json.loads((RAIZ / "bloque_a/11_Ejecutor/tests/mapa_plan_pruebas.json").read_text(encoding="utf-8"))["PB-51"]
nc = mapa["no_comprueba"]
if mapa["cobertura"] != "PARCIAL" or "ninguna afirmación técnica errónea" not in nc or "INC-T187-03" not in nc:
    fallos.append(f"H-01: cobertura {mapa['cobertura']}; «No comprueba» sin el resultado esperado incumplido")

m = {a["id"]: a for a in json.loads((TICKET / "muestra_afirmaciones.json").read_text(encoding="utf-8"))["afirmaciones"]}
notas = {}
for f in sorted((TICKET / "veredictos").glob("lote_*.json")):
    for v in json.loads(f.read_text(encoding="utf-8"))["veredictos"]:
        notas[v["id"]] = v
verif = collections.Counter(m[i]["prompt"] for i, v in notas.items() if i in m and v["veredicto"] != "NO_VERIFICABLE")
cortos = sorted((n, p) for p in {a["prompt"] for a in m.values()} if (n := verif.get(p, 0)) < 10)
if cortos and "afirmaciones técnicas por prompt" not in nc:
    fallos.append(f"H-02: {len(cortos)} prompts con menos de 10 verificables (mínimo {cortos[0]}), sin declarar")

com = json.loads((TICKET / "veredictos/comentario.json").read_text(encoding="utf-8"))
sin_apoyo = [i for i in com["discutibles"] if "discutib" not in notas[i]["nota"].lower()]
inventado = [i for i, t in com["dudosas"].items() if "no confirm" in t.lower() and "no confirm" not in notas[i]["nota"].lower()]
if sin_apoyo or inventado:
    fallos.append(f"H-03: discutibles sin apoyo en las notas {sin_apoyo}; matiz que la nota no dice {inventado}")

print("\n".join(fallos) or "las tres comprobaciones pasan")
sys.exit(1 if fallos else 0)
