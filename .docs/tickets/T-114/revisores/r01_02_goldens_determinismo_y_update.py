"""QA r01 de T-114 · Determinismo de la generación, `--update` sin motivo y mutación de cada golden y de los ficheros a mano.

Uso:  python r01_02_goldens_determinismo_y_update.py <copia_desechable_del_repo>
Trabaja solo en la copia desechable. Imprime una línea por comprobación (OK / FALLO) y termina con 1 si alguna falla.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

PY = "/home/user/robotinvestor/.venv/bin/python"
copia = Path(sys.argv[1]).resolve()
assert "qa_f3_mut" in str(copia), "solo en la copia desechable"
EJ = copia / "bloque_a" / "11_Ejecutor"
G = EJ / "tests" / "goldens"
fallos = 0


def huellas() -> dict:
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(G.iterdir())}


def correr(args: list[str], env: dict | None = None) -> tuple[int, str]:
    r = subprocess.run([PY, *args], cwd=EJ, capture_output=True, text=True, env={**os.environ, **(env or {})})
    return r.returncode, (r.stdout + r.stderr).strip()


def anotar(nombre: str, bien: bool, detalle: str = "") -> None:
    global fallos
    fallos += not bien
    print(f"{'OK   ' if bien else 'FALLO'} · {nombre}{' · ' + detalle if detalle else ''}", flush=True)


GEN = ("import sys, json, hashlib; sys.path[:0]=['tests','.']; import goldens_ct as g; t=g.generar(); "
       "print(json.dumps({k: hashlib.sha256(v.encode()).hexdigest() for k, v in sorted(t.items())}))")
base = huellas()
# 1 · determinismo: cuatro procesos con PYTHONHASHSEED distinto y otro directorio temporal
salidas = []
for semilla in ("0", "1", "12345", "random"):
    rc, out = correr(["-c", GEN], {"PYTHONHASHSEED": semilla, "TMPDIR": str(copia)})
    salidas.append(out.splitlines()[-1] if rc == 0 else f"rc={rc}")
anotar("generar() da el mismo texto con PYTHONHASHSEED 0, 1, 12345 y aleatorio", len(set(salidas)) == 1 and salidas[0].startswith("{"))
if salidas[0].startswith("{"):
    gen = json.loads(salidas[0])
    anotar("lo generado coincide con lo congelado", all(base[k] == v for k, v in gen.items()), f"{len(gen)} goldens")
# 2 · otra zona horaria y otra configuración regional
rc, out = correr(["tests/goldens_ct.py"], {"TZ": "Pacific/Kiritimati", "LC_ALL": "C", "LANG": "C"})
anotar("comprueba igual con TZ=Pacific/Kiritimati y LC_ALL=C", rc == 0, out.splitlines()[-1][:120])
# 3 · --update sin motivo: código 2 y ningún byte cambiado, aunque haya un golden roto
ruta = G / "tablas_contratos.json"
original = ruta.read_bytes()
ruta.write_text("{}\n", encoding="utf-8")
antes = huellas()
for args in (["--update"], ["--update", "--motivo", ""], ["--update", "--motivo", "   "], ["--update", "--motivo", "\t\n"]):
    rc, out = correr(["tests/goldens_ct.py", *args])
    anotar(f"{' '.join(repr(a) for a in args)} → código 2 y nada escrito", rc == 2 and huellas() == antes, f"rc={rc}")
rc, out = correr(["tests/goldens_ct.py"])
anotar("sin opciones, con un golden roto → código 1 y lo nombra", rc == 1 and "tablas_contratos.json" in out, out.splitlines()[0][:140])
anotar("sin opciones no escribe nada", huellas() == antes)
# 4 · --update con motivo: regenera y añade UNA línea a REGISTRO.md
reg = (G / "REGISTRO.md").read_text(encoding="utf-8")
rc, out = correr(["tests/goldens_ct.py", "--update", "--motivo", "QA r01: prueba | con\nsalto"])
nuevo = (G / "REGISTRO.md").read_text(encoding="utf-8")
anotar("--update con motivo regenera el golden roto", rc == 0 and ruta.read_bytes() == original, out.splitlines()[-1][:120])
anotar("…y añade una sola línea al registro", nuevo.startswith(reg) and nuevo[len(reg):].count("\n") == 1, repr(nuevo[len(reg):])[:140])
rc, out = correr(["tests/goldens_ct.py", "--update", "--motivo", "QA r01: sin cambios"])
anotar("--update con motivo y sin diferencias no toca el registro", rc == 0 and (G / "REGISTRO.md").read_text(encoding="utf-8") == nuevo)
(G / "REGISTRO.md").write_text(reg, encoding="utf-8")
anotar("la carpeta vuelve a su estado", huellas() == base)
# 5 · mutación de un valor en cada fichero (generados y a mano): el comprobador lo dice
for nombre in sorted(p.name for p in G.glob("*.json")):
    r = G / nombre
    crudo = r.read_text(encoding="utf-8")
    # cambia el último valor de texto del fichero (una hoja profunda, no la primera)
    i = crudo.rstrip().rfind('"', 0, crudo.rstrip().rfind('"'))
    mutado = crudo[:i + 1] + "X" + crudo[i + 1:]
    r.write_text(mutado, encoding="utf-8")
    rc, out = correr(["tests/goldens_ct.py"])
    anotar(f"mutar la última hoja de {nombre} → código 1", rc == 1, "; ".join(x[:110] for x in out.splitlines()[:2]))
    r.write_text(crudo, encoding="utf-8")
# 6 · espacios finales o BOM en un golden
crudo = ruta.read_bytes()
ruta.write_bytes(b"\xef\xbb\xbf" + crudo)
rc, out = correr(["tests/goldens_ct.py"])
anotar("un BOM delante de un golden → código 1", rc == 1)
ruta.write_bytes(crudo)
# 7 · un fichero de más y un README borrado
(G / "sobra.json").write_text("{}\n", encoding="utf-8")
rc, out = correr(["tests/goldens_ct.py"])
anotar("un fichero de más → código 1", rc == 1 and "sobra.json" in out)
(G / "sobra.json").unlink()
anotar("fin: carpeta intacta", huellas() == base)
raise SystemExit(1 if fallos else 0)
