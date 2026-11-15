"""QA r01 de T-94 · Integración con A real (cliente simulado): determinismo, CA-8, coste y aviso.

1. Dos ejecuciones con PYTHONHASHSEED distinto y la misma semilla del banco: informe.json, informe.md y prerregistro.json
   idénticos byte a byte (CA-4).
2. `git status` de bloque_a, bloque_b y sistema_global/marco_comun_c antes y después (CA-8), y que la ejecución no deja nada
   fuera de --salida y del registro indicado.
3. Coste: el banco suma tokens de entrada y salida de consumo.csv; ¿cuánto deja fuera (caché, uc)?
4. Aviso: ¿qué dice si el cliente no es el simulado pero los datos siguen siendo los de ejemplo (que el banco no deja cambiar)?
5. Selecciones del titular: ¿cuántas son oportunidades distintas y cuántas repeticiones VIGENTE con ventanas solapadas?
6. Advertencias que A deja en metricas.json (fuga por conocimiento del modelo, cliente simulado): ¿llegan al informe?
Uso: .venv/bin/python -B .docs/tickets/T-94/revisores/r01_06_integracion_coste_aviso.py [<raíz del repositorio o worktree>]"""
import argparse
import csv
import json
import os
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
RAIZ = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[4]
PY = RAIZ / ".venv" / "bin" / "python"
BANCO = RAIZ / ".docs" / "scripts" / "banco_medida.py"
fallos = []


def ok(cond, msg):
    print(("OK   " if cond else "FALLO ") + msg)
    if not cond:
        fallos.append(msg)


def estado_git():
    return subprocess.run(["git", "status", "--porcelain", "--untracked-files=all", "bloque_a", "bloque_b", "bloque_a_forex",
                           "sistema_global/marco_comun_c", ".docs/experimentos"], cwd=RAIZ, capture_output=True, text=True,
                          check=True).stdout


tmp = Path(tempfile.mkdtemp(prefix="r01_t94_int_"))
antes = estado_git()
salidas = []
for i, hs in enumerate(("1", "987")):
    out = tmp / f"r{i}"
    env = dict(os.environ, PYTHONHASHSEED=hs, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([str(PY), "-B", str(BANCO), "a", "--desde", "2026-03-06", "--hasta", "2026-05-29", "--salida", str(out),
                        "--remuestreos", "500", "--registro", str(tmp / f"reg{i}.jsonl")], cwd=RAIZ, capture_output=True,
                       text=True, env=env, check=False)
    ok(r.returncode == 0, f"ejecución {i} (PYTHONHASHSEED={hs}) termina con 0")
    salidas.append({f: (out / f).read_bytes() for f in ("prerregistro.json", "informe.json", "informe.md")})
    print("   stdout de la ejecución (¿se escapa la salida de A?):", r.stdout.splitlines()[:2], "…")
for f in ("prerregistro.json", "informe.json", "informe.md"):
    ok(salidas[0][f] == salidas[1][f], f"{f} idéntico byte a byte con PYTHONHASHSEED distinto")
ok(antes == estado_git(), "git status de bloques, marco y .docs/experimentos sin cambios tras dos ejecuciones")

out = tmp / "r0"
inf = json.loads((out / "informe.json").read_text(encoding="utf-8"))
with open(out / "titular" / "salida" / "consumo.csv", encoding="utf-8") as fh:
    filas = list(csv.DictReader(fh))
suma = {k: sum(float(f[k] or 0) for f in filas) for k in ("tokens_entrada", "tokens_salida", "tokens_cache_escritura",
                                                          "tokens_cache_lectura", "uc")}
print(f"   consumo.csv: {suma}")
print(f"   informe: {inf['coste']['titular']}")
ok(inf["coste"]["titular"]["tokens_entrada"] == int(suma["tokens_entrada"]), "tokens de entrada sumados bien")
cache = suma["tokens_cache_escritura"] + suma["tokens_cache_lectura"]
ok(cache == 0 or any("cache" in k for k in inf["coste"]["titular"]),
   f"el coste del informe recoge los tokens de caché ({int(cache)} frente a {int(suma['tokens_entrada'])} de entrada) o las uc ({suma['uc']:.1f})")

# 4. Aviso con cliente no simulado: se comprueba con la función, sin llamar a ninguna API
sys.path.insert(0, str(BANCO.parent))
import banco_medida as bm

real = bm.titular_a


def titular_sin_api(desde, hasta, carpeta, cliente, frecuencia, clases):
    return real(desde, hasta, carpeta, "mock", frecuencia, clases)   # mismos datos de ejemplo; el banco cree que es «anthropic»


bm.titular_a = titular_sin_api
ns = argparse.Namespace(desde="2026-03-06", hasta="2026-04-03", salida=str(tmp / "aviso"), cliente="anthropic", frecuencia=None,
                        clases=None, semilla=7, remuestreos=50, ventana=63, registro=None, experimento=None, max_variantes=1)
aviso = bm.ejecutar_a(ns)["aviso"]
print(f"   aviso con --cliente anthropic y datos de ejemplo: {aviso}")
ok(not aviso.startswith("cliente simulado"), "con cliente no simulado el aviso no dice «cliente simulado»")
ok('add_argument("--datos"' in BANCO.read_text(encoding="utf-8"),
   "el banco permite indicar otros datos y universo (los de K, T-86) sin tocar el código")

# 5. Repeticiones VIGENTE
with open(out / "titular" / "salida" / "senales.csv", encoding="utf-8") as fh:
    sen = list(csv.DictReader(fh))
c = Counter(f["vigente_nueva"] for f in sen)
distintas = len({(f["indicador_seguimiento_simbolo"], f["direccion"]) for f in sen})
print(f"   senales.csv: {len(sen)} filas, {dict(c)}, {distintas} oportunidades distintas; horizontes {Counter(f['horizonte_principal'] for f in sen)}")
print(f"   el informe las trata como {inf['contendientes']['titular']['resueltas']} observaciones independientes; "
      f"veredictos {[(k, v['veredicto']) for k, v in inf['comparaciones'].items()]}")
ok(inf["contendientes"]["titular"]["resueltas"] <= distintas or "efectivas" in json.dumps(inf),
   "el informe no cuenta como independientes las repeticiones VIGENTE con ventanas solapadas (o declara un n efectivo)")

# 6. Advertencias de A
with open(out / "titular" / "salida" / "metricas.json", encoding="utf-8") as fh:
    adv = json.load(fh).get("advertencias", [])
fuga = [a for a in adv if "FUGA" in a]
print(f"   advertencias de A: {[a[:60] + '…' for a in adv]}")
ok(not fuga or any("FUGA" in str(v) for v in inf.values()), "la advertencia de fuga por conocimiento del modelo de A llega al informe")

print(f"\n{len(fallos)} fallo(s)")
for f in fallos:
    print(" -", f)
print(f"(temporal: {tmp})")
sys.exit(1 if fallos else 0)
