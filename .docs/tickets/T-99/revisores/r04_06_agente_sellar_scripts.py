"""r04_06 · RI_AGENTE estricto (H-17), la orden «sellar» solo para la 0.1.0 (H-30), la comprobación de rutas locales de
commit_limpio.sh (H-18, H-25, H-31), commit.sh y la línea base de las pruebas de .docs/scripts (H-12).
La línea base se ataca en una COPIA desechable de la raíz (argumento 2, opcional: un worktree que se puede ensuciar); sin él,
esos casos se saltan. Uso: .venv/bin/python -B r04_06_agente_sellar_scripts.py <raíz> [<worktree desechable>]"""
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r04_comun import (AHORA, DESPUES, PY, RAIZ, REL, SCRIPTS, borrar, caso, cli, detecta, experimento_completo, fin,  # noqa: E402
                       git, lanza, lineas, pre, recadenar, repo_proyecto, rx, subir, tmpdir)

tmps = []
EXPS = RAIZ / ".docs" / "experimentos"

# 1. RI_AGENTE: un valor no válido no elige registro, y no crea nada
for valor in ("Astra", "astra ", "", "ástra", "a" * 33, "../astra", "astra/x"):
    rc, out = cli("ver", env={"RI_AGENTE": valor})
    caso(f"RI_AGENTE={valor!r}: la orden se detiene con un motivo y no crea nada", rc == 2 and "RI_AGENTE" in out and not EXPS.exists(),
         f"rc={rc}; {out[:90]}")
rc, out = cli("--registro", str(tmpdir("r04_t99_") / "x.jsonl"), "ver", env={"RI_AGENTE": "Astra"})
caso("RI_AGENTE no válido con --registro explícito: funciona (el registro lo da la orden)", rc == 0, out[:80])
for valor, nombre in ((None, "registro_claude.jsonl"), ("astra", "registro_astra.jsonl"), ("claude-nube", "registro_claude-nube.jsonl")):
    env = {k: v for k, v in os.environ.items() if k != "RI_AGENTE"}
    if valor is not None:
        env["RI_AGENTE"] = valor
    r = subprocess.run([PY, "-I", "-c", f"import sys; sys.path.insert(0, {str(SCRIPTS)!r}); import registro_experimentos as rx; "
                        "print(rx.REGISTRO_DEFECTO.name)"], capture_output=True, text=True, env=env)
    caso(f"RI_AGENTE={valor!r} → {nombre}", r.stdout.strip() == nombre, r.stdout.strip() or r.stderr.strip()[-80:])
env = {k: v for k, v in os.environ.items() if k != "RI_AGENTE"}
env["RI_AGENTE"] = "Astra"
r = subprocess.run([PY, "-B", str(SCRIPTS / "banco_medida.py"), "a", "--desde", "2024-01-05", "--hasta", "2024-03-29",
                    "--salida", str(tmpdir("r04_t99_banco_") / "s")], capture_output=True, text=True, env=env)
caso("banco con RI_AGENTE no válido y sin --registro: se detiene al empezar, sin traza y sin crear nada",
     r.returncode == 2 and "Traceback" not in r.stderr and not EXPS.exists(), r.stderr.strip()[-110:])
claude_md = (RAIZ / "CLAUDE.md").read_text(encoding="utf-8")
caso("(documentación) CLAUDE.md, por donde entra Claude, dice que dos sesiones de Claude usan RI_AGENTE distintos",
     "RI_AGENTE" in claude_md, "CLAUDE.md no menciona RI_AGENTE (sí AGENTS.md, punto 9, y .docs/README.md)")
gi = (RAIZ / ".gitignore").read_text(encoding="utf-8")
caso("(documentación) el comentario del .gitignore dice que el sello es local",
     "el sello sí se sube" not in gi, [x for x in gi.splitlines() if "T-99" in x][0])

# 2. sellar: solo la 0.1.0; deja la marca; ¿y qué pasa con la marca en un clon? ¿y con un registro mixto 0.1.0 + 0.4.0?
d = tmpdir("r04_t99_"); tmps.append(d)
reg = rx.Registro(d / "r.jsonl")
experimento_completo(reg, "peor")
viejas = [json.loads(x) for x in lineas(reg.ruta)]
viejas[0]["version_registro"] = "0.1.0"
(d / "v010.jsonl").write_text("".join(x + "\n" for x in recadenar(viejas)), encoding="utf-8")
rc, out = cli("--registro", str(d / "v010.jsonl"), "verificar")
caso("registro de la 0.1.0 sin sello: verificar pide «sellar»", rc == 2 and "sellar" in out, out[:100])
rc, out = cli("--registro", str(d / "v010.jsonl"), "sellar")
rc2, out2 = cli("--registro", str(d / "v010.jsonl"), "verificar")
caso("sellar lo sella y verificar dice «sellado a mano»", rc == 0 and rc2 == 0 and "sellado a mano" in out2, f"{out} | {out2}")
# Mixto: prerregistro de la 0.1.0 y un intento y resultado escritos por la 0.4.0 (los intentos no llevan versión)
r010 = rx.Registro(d / "v010.jsonl")
exp = viejas[0]["exp_id"]
r010.intento(exp, "v1", ahora=DESPUES); r010.resultado(exp, 2, "peor", ahora=DESPUES)
completo = lineas(r010.ruta)
r010.sello.unlink()
(d / "v010.jsonl").write_text("".join(x + "\n" for x in completo[:3]), encoding="utf-8")   # quita el «peor» de la 0.4.0
rc, out = cli("--registro", str(d / "v010.jsonl"), "sellar")
caso("(límite declarado: tocar el sello) registro 0.1.0 continuado con la 0.4.0, sin sello y sin lo último: sellar se niega",
     rc != 0, f"rc={rc}; {out[:100]} (solo mira la versión de los PRERREGISTRO)")
# La marca «sellado a mano» vive en el sello, que es local: un clon no la tiene
repo = repo_proyecto(); tmps.append(repo)
(repo / REL).parent.mkdir(parents=True)
(repo / REL).write_text("".join(x + "\n" for x in recadenar(viejas)), encoding="utf-8")
rx.Registro(repo / REL).sellar(); subir(repo)
rx.Registro(repo / REL).sello.unlink()   # como en un clon nuevo
rc, out = cli("--registro", str(repo / REL), "verificar")
caso("(baja) la marca «sellado a mano» se ve también en un clon (el sello no se sube)", "sellado a mano" in out, out[:100])

# 3. commit_limpio.sh: la comprobación de rutas locales, extraída tal cual y ejecutada con varias listas de rutas
limpio = (SCRIPTS / "commit_limpio.sh").read_text(encoding="utf-8").splitlines()
i = next(k for k, x in enumerate(limpio) if "H-25" in x)
bloque = []
for x in limpio[i + 2:]:
    bloque.append(x)
    if x == "done":
        break
fragmento = "\n".join(bloque)
rel = str(REL)


def comprobar(*rutas):
    guion = 'fallo(){ echo "FALLO: $*"; exit 1; }\nrutas=(' + " ".join(f"'{r}'" for r in rutas) + ")\n" + fragmento + "\necho PASA"
    return subprocess.run(["bash", "-c", guion], capture_output=True, text=True).stdout.strip()


caso("commit_limpio: el registro solo pasa", comprobar(rel) == "PASA")
for suf in (".sello", ".sello.tmp", ".lock", ".turno"):
    caso(f"commit_limpio: «{suf}» en las rutas se rechaza", comprobar(rel, rel + suf).startswith("FALLO"), comprobar(rel, rel + suf))
caso("commit_limpio: un «.sello» con «./» delante también se rechaza", comprobar("./" + rel + ".sello").startswith("FALLO"))
caso("(referencia) commit_limpio usa update-index, que se salta el .gitignore: por eso hace falta la comprobación",
     any("update-index --add" in x for x in limpio))
commit = (SCRIPTS / "commit.sh").read_text(encoding="utf-8")
caso("commit.sh pasa las pruebas de .docs/scripts con su línea base (pruebas_scripts.sh)", "pruebas_scripts.sh" in commit)
repo = repo_proyecto(); tmps.append(repo)
reg = rx.Registro(repo / REL); experimento_completo(reg)
p = subprocess.run(["bash", "-c", "set -euo pipefail; git add -- \"$1\" \"$2\"; echo SIGUE", "x", str(REL), str(REL) + ".sello"],
                   cwd=repo, capture_output=True, text=True)
caso("commit.sh con el sello en las rutas: «git add» lo rechaza (ignorado) y set -e corta antes del commit",
     p.returncode != 0 and "SIGUE" not in p.stdout,
     f"{p.stderr.strip()[:60]}; queda en el índice (sin commit): {git(repo, 'diff', '--cached', '--name-only')}")

# 4. La línea base de las pruebas de .docs/scripts, atacada en el worktree desechable
if len(sys.argv) > 2:
    W = Path(sys.argv[2]).resolve()
    base_f = W / ".docs/scripts/linea_base_pruebas.txt"
    pruebas_f = W / ".docs/scripts/pruebas_registro_experimentos.py"
    base0, pruebas0 = base_f.read_bytes(), pruebas_f.read_bytes()

    def lanzar():
        r = subprocess.run(["bash", str(W / ".docs/scripts/pruebas_scripts.sh")], capture_output=True, text=True, cwd=W)
        return r.returncode, (r.stdout + r.stderr).strip().splitlines()[-1:] or [""]

    try:
        rc, out = lanzar()
        caso("(control) línea base intacta: pasa", rc == 0, out[0])
        texto = pruebas0.decode("utf-8")
        primera = texto.index("\ndef test_")
        pruebas_f.write_text(texto[:primera] + "\ndef _quitada" + texto[primera + len("\ndef test"):], encoding="utf-8")
        rc, out = lanzar()
        caso("quitar una prueba (sin tocar la línea base): falla", rc != 0, out[0])
        base_f.write_text("193\n", encoding="utf-8")
        rc, out = lanzar()
        caso("(observación) quitar una prueba y bajar la línea base en el mismo cambio: pasa (como las cuotas de los bloques)",
             rc == 0, out[0])
        pruebas_f.write_bytes(pruebas0)
        base_f.write_text("194  # línea base de T-99, 15-11-2026\n", encoding="utf-8")
        rc, out = lanzar()
        caso("(baja) un comentario con cifras en la línea base no la cambia (tr -dc '0-9' las junta)", rc == 0,
             f"rc={rc}; {out[0]}")
        base_f.write_bytes(base0)
        pruebas_f.write_text(texto.replace("\ndef test_", "\ndef test_falla_a_proposito():\n    assert False\n\n\ndef test_", 1),
                             encoding="utf-8")
        rc, out = lanzar()
        caso("una prueba que falla: falla cerrado", rc != 0, f"rc={rc}; última línea: {out[0]!r}")
        caso("(baja) …y dice por qué (el resumen de pytest o el motivo)", "failed" in out[0] or "fallan" in out[0], repr(out[0]))
    finally:
        base_f.write_bytes(base0)
        pruebas_f.write_bytes(pruebas0)
else:
    print("[SIN COMPROBAR] línea base: hace falta un worktree desechable como segundo argumento")

for t in tmps:
    borrar(t)
fin()
