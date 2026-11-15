"""r05_04 · El cerrojo con los ficheros dentro de .git, el lector sin permiso (H-39) y `pruebas_scripts.sh` (H-38).
1. r04_05 casos 1 y 4 rehechos para la regla nueva (variantes distintas por escritor; el v1 del caso 4 cerrado antes): en un
   repositorio git (cerrojo y turno en .git/ri-registro), tres escritores y tres lectores a la vez; un lector colgado con dos
   escritores detrás.
2. Lector sin permiso (uid 65534, «nobody»): (a) registro fuera de git en una carpeta de solo lectura; (b) registro en un
   repositorio de otro usuario («dubious ownership»); (c) el mismo con safe.directory=* en su configuración global.
3. `sellar` y la marca «sellado a mano» (H-39, puntos 2 y 3).
4. `pruebas_scripts.sh` en un worktree desechable (si se da): una prueba que falla dice qué pasó; la línea base con comentario;
   con espacios delante; sin fichero; quitar una prueba sin bajar la línea base.
Uso: .venv/bin/python -B r05_04_cerrojo_lector_scripts.py <raíz> [<worktree desechable>]"""
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r05_comun import (AHORA, DESPUES, REL, SCRIPTS, borrar, caso, cli, carpeta_local, experimento_completo, fin, git, lanza,  # noqa: E402
                       lineas, pre, recadenar, repo_proyecto, rx, subir, tmpdir, escribir_lineas)

tmps = []
PY = sys.executable


def hijo(codigo, uid=None):
    pre_ = "" if uid is None else f"import os; os.setgid({uid}); os.setuid({uid})\n"
    return subprocess.Popen([PY, "-I", "-c", pre_ + f"import sys; sys.path.insert(0, {str(SCRIPTS)!r})\n" + codigo],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


# 1. Escritores y lectores con los cerrojos en .git
repo = repo_proyecto("r05_t99_lock_"); tmps.append(repo)
ruta = repo / REL
exp = rx.Registro(ruta).prerregistrar(pre(max_variantes=1000), "qa", ahora=AHORA)["exp_id"]
subir(repo, REL)
escritor = """
import registro_experimentos as rx
r = rx.Registro({ruta!r}); malos = 0
for k in range(30):
    try:
        i = r.intento({exp!r}, "{w}-%d" % k)
        if k % 2: r.resultado({exp!r}, i["n"], "peor")
    except rx.RegistroError as e:
        malos += 1; print("ERR", e)
print("FIN", malos)
"""
lector = f"""
import time, registro_experimentos as rx
r = rx.Registro({str(ruta)!r}); buenas = malas = 0; t = time.monotonic()
while time.monotonic() - t < 8:
    try:
        r.verificar(); buenas += 1
    except rx.RegistroError as e:
        malas += 1; print("ERR", e)
print("FIN", buenas, malas)
"""
ps = [hijo(escritor.format(ruta=str(ruta), exp=exp, w=w)) for w in "abc"] + [hijo(lector) for _ in range(3)]
salidas = [p.communicate(timeout=300)[0].strip().splitlines()[-1] for p in ps]
reg = rx.Registro(ruta)
e = lanza(reg.verificar, rx.RegistroError)
ns = [x["n"] for x in reg.anotaciones() if x["tipo"] == "INTENTO"] if e is None else []
caso("en git: 3 escritores × 30 (con resultados) y 3 lectores: 90 intentos correlativos, sin errores",
     e is None and ns == list(range(1, 91)) and all(s.split()[-1] == "0" for s in salidas), f"salidas {salidas}")
caso("en git: cerrojo y turno dentro de .git/ri-registro, nada en el árbol",
     (carpeta_local(repo) / ".docs__experimentos__registro_claude.jsonl.lock").exists()
     and not any(p.name.endswith((".lock", ".turno", ".sello")) for p in ruta.parent.iterdir()))
lock = reg._local(".lock")
p = hijo(f"import fcntl, time\nf = open({str(lock)!r}, 'a'); fcntl.flock(f, fcntl.LOCK_SH); print('cogido', flush=True); time.sleep(600)")
p.stdout.readline()
plantilla = ("import time, registro_experimentos as rx\nt = time.monotonic()\ntry:\n    rx.Registro({ruta!r}).intento({exp!r}, {v!r})\n"
             "    print('ESCRIBIÓ', round(time.monotonic() - t, 1))\nexcept rx.RegistroError as e:\n    print('FALLA', round(time.monotonic() - t, 1), e)")
a = hijo(plantilla.format(ruta=str(ruta), exp=exp, v="A"))
time.sleep(1)
b = hijo(plantilla.format(ruta=str(ruta), exp=exp, v="B"))
time.sleep(5)
p.kill(); p.wait()
sa, sb = a.communicate(timeout=120)[0].strip(), b.communicate(timeout=120)[0].strip()
caso("en git: lector colgado 6 s; los dos escritores que esperaban entran al morir", sa.startswith("ESCRIBIÓ") and sb.startswith("ESCRIBIÓ"),
     f"A: {sa[:40]}; B: {sb[:40]}")

# 2. Lector sin permiso
if os.geteuid() == 0:
    mod = tmpdir("r05_t99_mod_"); tmps.append(mod); os.chmod(mod, 0o755)
    (mod / "registro_experimentos.py").write_bytes((SCRIPTS / "registro_experimentos.py").read_bytes())
    os.chmod(mod / "registro_experimentos.py", 0o644)
    hogar = tmpdir("r05_t99_home_"); tmps.append(hogar); os.chown(hogar, 65534, 65534)

    def como_nobody(ruta, ancla=True, entorno=None):
        codigo = (f"import os, sys; os.setgid(65534); os.setuid(65534); sys.path.insert(0, {str(mod)!r})\n"
                  f"import registro_experimentos as rx\ntry:\n    print('LEE', rx.Registro({str(ruta)!r}, ancla_git={ancla}).verificar())\n"
                  "except Exception as e:\n    print('FALLA', type(e).__name__, e)")
        env = {"PATH": os.environ.get("PATH", ""), "HOME": str(hogar), **(entorno or {})}
        r = subprocess.run([PY, "-I", "-c", codigo], capture_output=True, text=True, env=env)
        return (r.stdout + r.stderr).strip()

    d = tmpdir("r05_t99_ro_"); tmps.append(d)
    experimento_completo(rx.Registro(d / "r.jsonl"))
    for f in (".lock", ".turno"):
        (d / ("r.jsonl" + f)).unlink(missing_ok=True)
    os.chmod(d, 0o755)
    for f in d.iterdir():
        os.chmod(f, 0o644)
    out = como_nobody(d / "r.jsonl")
    caso("(a) nobody, registro fuera de git en una carpeta de solo lectura: lo verifica", out.startswith("LEE 3"), out[:100])
    repo = repo_proyecto("r05_t99_ro_git_"); tmps.append(repo)
    experimento_completo(rx.Registro(repo / REL)); subir(repo, REL)
    for raiz, dirs, files in os.walk(repo):
        os.chmod(raiz, 0o755)
        for f in files:
            os.chmod(Path(raiz) / f, 0o644)
    out = como_nobody(repo / REL)
    caso("(b) (observación) nobody, registro en un repositorio de otro usuario: falla cerrado (git no lo reconoce)",
         out.startswith("FALLA"), out[:110])
    (hogar / ".gitconfig").write_text("[safe]\n\tdirectory = *\n", encoding="utf-8"); os.chown(hogar / ".gitconfig", 65534, 65534)
    out = como_nobody(repo / REL)
    caso("(c) nobody con safe.directory=*: verifica el registro de otro usuario sin poder escribir en .git", out.startswith("LEE 3"), out[:110])
else:
    print("[SIN COMPROBAR] lector sin permiso: hace falta ser root para cambiar de usuario")

# 3. sellar y la marca
d = tmpdir("r05_t99_sellar_"); tmps.append(d)
contenido = {k: v for k, v in sorted(pre().items())}
h = rx.huella(contenido)
objs = [{"tipo": "PRERREGISTRO", "exp_id": "EXP-2026-0001", "autor": "qa", "creado_en": AHORA, "version_registro": "0.1.0",
         "contenido": contenido, "huella_prerregistro": h}]
for k in range(1, 4):
    objs.append({"tipo": "INTENTO", "exp_id": "EXP-2026-0001", "n": k, "variante": f"v{k}", "inicio": DESPUES,
                 "huella_prerregistro": h, "dentro_del_maximo": k <= 2})
escribir_lineas(d / "r.jsonl", recadenar(objs)[:2])   # truncado, sin sello: lo de después lo «escribió» una versión con sello
rc, out = cli("--registro", str(d / "r.jsonl"), "sellar")
caso("(H-39 punto 3, sin cambio) registro 0.1.0 continuado, truncado y sin sello: sellar se niega", rc != 0, out[:90])
rc, out = cli("--registro", str(d / "r.jsonl"), "verificar")
caso("(H-39 punto 2) verificar dice «sellado a mano»", "sellado a mano" in out, out[:90])

# 4. pruebas_scripts.sh en un worktree desechable
if len(sys.argv) > 2:
    W = Path(sys.argv[2]).resolve()
    assert W != Path("/home/user/robotinvestor"), "nunca en el árbol principal"
    base = W / ".docs/scripts/linea_base_pruebas.txt"
    prueba = W / ".docs/scripts/pruebas_registro_experimentos.py"
    orig_base, orig_prueba = base.read_bytes(), prueba.read_bytes()

    def lanzar():
        r = subprocess.run(["bash", str(W / ".docs/scripts/pruebas_scripts.sh")], capture_output=True, text=True, cwd=W, timeout=900)
        return r.returncode, (r.stdout + r.stderr)

    try:
        prueba.write_bytes(orig_prueba + b"\n\ndef test_r05_falla_a_proposito():\n    assert 1 == 2\n")
        rc, out = lanzar()
        caso("pruebas_scripts.sh con una prueba que falla: código distinto de 0 y dice cuál", rc != 0 and "test_r05_falla_a_proposito" in out
             and "fallan" in out, f"rc={rc}; {out.strip().splitlines()[-1][:80]}")
        prueba.write_bytes(orig_prueba)
        base.write_text("203  # T-99, 15-11-2026\n", encoding="utf-8")
        rc, out = lanzar()
        caso("línea base con un comentario detrás: se lee 203 y pasa", rc == 0, out.strip().splitlines()[-1][:80])
        base.write_text("  203\n", encoding="utf-8")
        rc, out = lanzar()
        caso("(observación) línea base con espacios delante: falla cerrado («no hay línea base»)", rc != 0 and "no hay línea base" in out,
             out.strip().splitlines()[-1][:80])
        base.unlink()
        rc, out = lanzar()
        caso("sin fichero de línea base: falla cerrado con un motivo", rc != 0 and "ERROR" in out, out.strip().splitlines()[-1][:90])
        base.write_bytes(orig_base)
        texto = orig_prueba.decode("utf-8")
        i = texto.rindex("\ndef test_")   # la última prueba, hasta el final del fichero
        prueba.write_text(texto[:i] + "\n", encoding="utf-8")
        rc, out = lanzar()
        caso("quitar una prueba sin bajar la línea base: falla", rc != 0 and "por debajo de la línea base" in out, out.strip().splitlines()[-1][:90])
    finally:
        base.write_bytes(orig_base); prueba.write_bytes(orig_prueba)
    caso("(control) el worktree desechable queda como estaba", git(W, "status", "--porcelain", "--untracked-files=no") == "")
else:
    print("[SIN COMPROBAR] pruebas_scripts.sh: hace falta un worktree desechable")

for t in tmps:
    borrar(t)
fin()
