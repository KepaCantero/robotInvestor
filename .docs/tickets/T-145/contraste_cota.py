"""T-145 · contraste del supuesto S4 de la cota (`estimar_coste_ciclo_a.cota_ciclo`): con las respuestas del simulado alargadas hasta cerca de max_tokens (método del
revisor, r01_01 escenario 2), ningún encargo pasa del que supone la cota. Uso (desde bloque_a/11_Ejecutor):
python -I <este> <tmp> [--config yaml]"""
import collections
import sys
from pathlib import Path

RAIZ = Path.cwd().parents[1]
src = (RAIZ / ".docs/tickets/T-140/revisores/r01_01_cota_ciclo_real.py").read_text(encoding="utf-8")
corte = src.index("shutil.rmtree(S, ignore_errors=True)")
ns = {"__file__": str(RAIZ / ".docs/tickets/T-140/revisores/r01_01_cota_ciclo_real.py"), "__name__": "r1"}
exec(compile(src[:corte], "r1", "exec"), ns)
import shutil

S = Path(sys.argv[1]); shutil.rmtree(S, ignore_errors=True); S.mkdir(parents=True)
base = ns["ciclo"](S / "e0", "2024-03-29")
ns["INFLAR"]["activo"] = True
largo = ns["ciclo"](S / "e1", "2024-03-29")
est = ns["est"]; cfg = ns["cfg"]; tarifa = ns["tarifa"]
c = est.cota_ciclo(base, cfg, tarifa["precios_por_millon"], 10.0, 1.35)
cota_enc = collections.defaultdict(float)
for x in c["papeles"]:
    for a in x["agentes"]:
        cota_enc[a] = max(cota_enc[a], x["encargo_tok"])
peor = collections.defaultdict(float)
for x in largo:
    peor[x["agente"]] = max(peor[x["agente"]], x["user_tok"])
fallos = [a for a in peor if peor[a] > cota_enc[a]]
for a in sorted(peor):
    print(f"  {a}: encargo alargado {peor[a]:8.0f} · supuesto de la cota {cota_enc[a]:8.0f}")
print(("FALLA " + ", ".join(fallos)) if fallos else "ok: ningún encargo alargado pasa del supuesto S4")
c2 = est.cota_ciclo(largo, cfg, tarifa["precios_por_millon"], 10.0, 1.35)["cota"]
print(f"cota con el ciclo medido {c['cota']:.2f} USD · con el ciclo alargado como medida {c2:.2f} USD")
