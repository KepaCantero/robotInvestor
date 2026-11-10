"""T-66 · QA r02 · opciones vigentes ARRASTRADAS desde F3 (N1 o finalistas no repetidas): ¿conservan la regla de PA-05?

A · F3 escrito por el código anterior a T-66 (fuerte «resuelta» solo por el Analista, sin evidencia ni contrarréplica, id
    del modelo) y arrastrado por el código corregido: ¿se vuelve a publicar con la fuerte resuelta?
B · Solo código corregido: alta con una fuerte resuelta en contrarréplica (tesis frágil → especulativo); a la semana
    siguiente se arrastra: ¿sigue frágil y especulativa?

Cada paso se ejecuta en un proceso aparte con su `bloque_a` (r02_02_paso_arrastre.py).
Uso: NUEVO=<ejecutor de A corregido> PRE=<ejecutor de A anterior a T-66 (p. ej. worktree de da3f6cb)> R01=<revisores r01>
     python r02_02_arrastre.py
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
NUEVO, PRE, R01 = os.environ["NUEVO"], os.environ.get("PRE"), os.environ["R01"]
sys.path[:0] = [NUEVO, R01]
from r01_comun import comprobar, fin  # noqa: E402


def paso(ejecutor, carpeta, as_of, modo):
    out = carpeta / f"{as_of}_{modo}.json"
    env = {**os.environ, "PYTHONPATH": f"{ejecutor}:{R01}:{AQUI}", "PYTHONDONTWRITEBYTECODE": "1"}
    p = subprocess.run([sys.executable, str(AQUI / "r02_02_paso_arrastre.py"), str(carpeta), as_of, modo, str(out)],
                       env=env, capture_output=True, text=True, timeout=1500)
    if p.returncode:
        raise RuntimeError(p.stderr[-2000:])
    d = json.loads(out.read_text(encoding="utf-8"))
    assert Path(d["bloque_a"]).is_relative_to(Path(ejecutor)), d["bloque_a"]
    return d


def vigentes(d):
    return {k: v for k, v in d["f3"].items() if v["estado"] in ("PROPUESTA", "VIGENTE")}


# A · objeciones antiguas
if PRE:
    c = Path(tempfile.mkdtemp(prefix="r02_arrA_"))
    d1 = paso(PRE, c, "2026-06-05", "alta_sin_evidencia")
    d2 = paso(NUEVO, c, "2026-06-12", "arrastre")
    antiguas = {k: v["fuertes"] for k, v in vigentes(d1).items()}
    print(f"    ciclo 1 (anterior a T-66): {d1['estado']}, publicadas {[p['opp_id'] for p in d1['publicadas']]}; fuertes {antiguas}")
    pub2 = {p["opp_id"]: [o for o in p["objeciones"] if o["fuerza"] == "fuerte"] for p in d2["publicadas"]}
    malas = [(k, o["objecion_id"]) for k, objs in pub2.items() for o in objs if o.get("resuelta")
             and not any(x.get("evidencia_citada") and x.get("contrarreplica") for x in d2["f3"][k]["fuertes"]
                         if x["objecion_id"] == o["objecion_id"])]
    comprobar("arrastre de un F3 anterior a T-66: ninguna fuerte resuelta sin evidencia ni contrarréplica se vuelve a publicar",
              not malas, f"ciclo 2 (corregido): {d2['estado']}, integridad {all(d2['integridad'].values())}; publicadas con la fuerte "
              f"resuelta sin evidencia ni contrarréplica {malas}")
else:
    print("[INFO] PRE no definido: se omite el escenario A")

# B · el veredicto por regla en el arrastre
c = Path(tempfile.mkdtemp(prefix="r02_arrB_"))
d1 = paso(NUEVO, c, "2026-06-05", "alta_con_evidencia")
d2 = paso(NUEVO, c, "2026-06-12", "arrastre")
conf1 = {p["opp_id"]: p["confianza"] for p in d1["publicadas"]}
conf2 = {p["opp_id"]: p["confianza"] for p in d2["publicadas"]}
ver1 = {k: v["veredicto_refutacion"] for k, v in vigentes(d1).items()}
ver2 = {k: v["veredicto_refutacion"] for k, v in vigentes(d2).items()}
print(f"    ciclo 1: confianza {conf1}, veredicto {ver1}")
print(f"    ciclo 2 (arrastre): confianza {conf2}, veredicto {ver2}")
fragiles = [k for k, v in ver1.items() if v == "tesis frágil" and k in conf2]
comprobar("arrastre: una tesis frágil sigue siendo especulativa", bool(fragiles) and all(conf2[k] == "especulativo" for k in fragiles),
          f"frágiles en el alta {fragiles}; confianza tras el arrastre {[conf2[k] for k in fragiles]}")
comprobar("arrastre: el veredicto por regla se conserva en F3", bool(fragiles) and all(ver2.get(k) == "tesis frágil" for k in fragiles),
          f"veredicto en F3 tras el arrastre {[ver2.get(k) for k in fragiles]}")

fin()
