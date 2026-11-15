"""r05_02 · El sello, el cerrojo y el turno dentro de la carpeta de git (H-37, 0.5.0).
1. Dónde van en un repositorio normal, en un worktree enlazado y en un submódulo; nada en el árbol de trabajo.
2. `git stash -u` con el registro nunca subido, y `git stash --all` con anotaciones sin subir: se detecta y `stash pop` funciona.
3. `git clean -fdX` (no toca nada del registro) y `git clean -fdx` con el registro sin subir (se pierde; se detecta).
4. Un clon nuevo (sin sello) y `git worktree remove` + `prune`.
5. Un registro de la 0.4.0 con su sello JUNTO al fichero (antes de la r05): ¿se lee con la 0.5.0? ¿hay salida?
6. Dos registros del mismo repositorio cuyos nombres colisionan al aplanar la ruta («a/b.jsonl» y «a__b.jsonl»).
7. Un registro fuera de git cuya carpeta pasa a ser un repositorio (`git init`).
Uso: .venv/bin/python -B r05_02_sello_en_git.py <raíz>"""
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r05_comun import (DESPUES, ENTORNO_GIT, REL, borrar, caso, carpeta_local, cli, detecta, experimento_completo, fin, git,  # noqa: E402
                       lanza, lineas, pre, repo_proyecto, rx, subir, tmpdir, escribir_lineas)

tmps = []


def arbol_limpio(repo, permitido=()):
    """Ficheros sin seguimiento o ignorados del árbol, sin contar los permitidos."""
    out = git(repo, "status", "--porcelain", "--ignored", "--untracked-files=all").splitlines()
    return [x for x in out if not any(x.endswith(p) for p in permitido)]


# 1. Ubicación
repo = repo_proyecto("r05_t99_loc_"); tmps.append(repo)
reg = rx.Registro(repo / REL)
exp = experimento_completo(reg, "peor")
caso("repositorio normal: sello en .git/ri-registro", reg.sello.parent == carpeta_local(repo) and reg.sello.exists(),
     str(reg.sello.relative_to(repo)))
caso("repositorio normal: en el árbol solo está el registro", arbol_limpio(repo, (REL.as_posix(),)) == [], str(arbol_limpio(repo))[:80])
subir(repo, REL)
wt = tmpdir("r05_t99_wt_"); wt.rmdir(); tmps.append(wt)
git(repo, "worktree", "add", "-q", "--detach", str(wt))
regw = rx.Registro(wt / REL)
n = regw.intento(exp, "v2", ahora=DESPUES)["n"]; regw.resultado(exp, n, "mejor", ahora=DESPUES)
caso("worktree enlazado: sello propio en .git/worktrees/<n>/ri-registro",
     "worktrees" in regw.sello.parts and regw.sello.exists() and regw.sello != reg.sello, "/".join(regw.sello.parts[-4:]))
caso("worktree enlazado: el registro principal no se ve afectado", reg.verificar() == 3 and regw.verificar() == 5)
caso("worktree enlazado: en su árbol solo está el registro", arbol_limpio(wt, (REL.as_posix(),)) == [], str(arbol_limpio(wt))[:80])
git(repo, "worktree", "remove", "--force", str(wt)); git(repo, "worktree", "prune")
caso("worktree quitado y podado: su carpeta de git (con su sello) desaparece", not regw.sello.exists())

sub_origen = repo_proyecto("r05_t99_suborig_"); tmps.append(sub_origen)
experimento_completo(rx.Registro(sub_origen / REL), "peor"); subir(sub_origen, REL)
sup = repo_proyecto("r05_t99_sup_"); tmps.append(sup)
r = subprocess.run(["git", "-C", str(sup), "-c", "protocol.file.allow=always", "submodule", "add", "-q", str(sub_origen), "sub"],
                   capture_output=True, text=True, env=ENTORNO_GIT)
if r.returncode == 0:
    regs = rx.Registro(sup / "sub" / REL)
    e = lanza(lambda: regs.intento("EXP-2026-0001", "v2", ahora=DESPUES), rx.RegistroError)
    caso("submódulo: se anota en el registro del submódulo", e is None, str(e)[:90] if e else "")
    caso("submódulo: sello en .git/modules/sub/ri-registro del superproyecto", "modules" in regs.sello.parts and regs.sello.exists(),
         "/".join(regs.sello.parts[-5:]))
    caso("submódulo: en su árbol solo está el registro", arbol_limpio(sup / "sub", (REL.as_posix(),)) == [])
else:
    caso("(no comprobado) submódulo: git submodule add falló", True, r.stderr.strip()[:80])

# 2. stash
repo = repo_proyecto("r05_t99_stash_"); tmps.append(repo)
reg = rx.Registro(repo / REL)
exp = experimento_completo(reg, "mejor")   # nunca subido
git(repo, "stash", "-q", "-u")
ok, motivo = detecta(reg)
caso("stash -u con el registro nunca subido: leer falla cerrado", ok and not reg.ruta.exists(), motivo[:80])
e = lanza(lambda: reg.prerregistrar(pre(), "qa"), rx.RegistroError)
caso("stash -u: prerregistrar en el registro ausente falla cerrado (no empieza uno nuevo)", e is not None and not reg.ruta.exists(),
     str(e)[:80] if e else "")
r = subprocess.run(["git", "-C", str(repo), "stash", "pop", "-q"], capture_output=True, text=True, env=ENTORNO_GIT)
caso("stash pop funciona (nada del registro se recreó en el árbol)", r.returncode == 0 and reg.verificar() == 3, r.stderr.strip()[:80])
subir(repo, REL)
n = reg.intento(exp, "v1", ahora=DESPUES)["n"]; reg.resultado(exp, n, "peor", ahora=DESPUES)   # repetición «peor», sin subir
git(repo, "stash", "-q", "--all")
ok, motivo = detecta(reg)
caso("stash --all con una repetición «peor» sin subir: se detecta", ok, motivo[:80])
caso("stash --all: adoptable no se puede leer (falla cerrado)", lanza(lambda: reg.adoptable(exp), rx.RegistroError) is not None)
r = subprocess.run(["git", "-C", str(repo), "stash", "pop", "-q"], capture_output=True, text=True, env=ENTORNO_GIT)
caso("stash --all y pop: vuelve todo y se lee", r.returncode == 0 and reg.verificar() == 5, r.stderr.strip()[:80])

# 3. clean
git(repo, "clean", "-q", "-fdX")
caso("clean -fdX: el sello sigue y el registro se lee", reg.sello.exists() and reg.verificar() == 5)
repo = repo_proyecto("r05_t99_clean_"); tmps.append(repo)
reg = rx.Registro(repo / REL)
experimento_completo(reg, "mejor")
git(repo, "clean", "-q", "-fdx")
ok, motivo = detecta(reg)
caso("clean -fdx con el registro sin subir: el registro se pierde y se detecta (el sello queda)", ok and reg.sello.exists(), motivo[:80])

# 4. Clon nuevo
repo = repo_proyecto("r05_t99_clon_"); tmps.append(repo)
reg = rx.Registro(repo / REL)
exp = experimento_completo(reg, "mejor"); subir(repo, REL)
clon = tmpdir("r05_t99_clon2_"); clon.rmdir(); tmps.append(clon)
git(clon.parent, "clone", "-q", str(repo), str(clon))
regc = rx.Registro(clon / REL)
caso("clon nuevo: sin sello y se lee", not regc.sello.exists() and regc.verificar() == 3)
n = regc.intento(exp, "v2", ahora=DESPUES)["n"]
caso("clon nuevo: la primera escritura crea el sello en su .git", regc.sello.exists() and regc.sello.parent == carpeta_local(clon))

# 5. Un registro de la 0.4.0 con el sello junto al fichero
repo = repo_proyecto("r05_t99_v040_"); tmps.append(repo)
reg = rx.Registro(repo / REL)
exp = experimento_completo(reg, "peor"); subir(repo, REL)
n = reg.intento(exp, "v2", ahora=DESPUES)["n"]; reg.resultado(exp, n, "mejor", ahora=DESPUES)   # sin subir
viejo = reg.ruta.with_name(reg.ruta.name + ".sello")
shutil.move(str(reg.sello), str(viejo))   # donde lo dejaba la 0.4.0
ok, motivo = detecta(rx.Registro(repo / REL))
caso("(observación) registro de la 0.4.0 con su sello junto al fichero: la 0.5.0 no lo encuentra y falla cerrado", ok, motivo[:90])
rc, out = cli("--registro", str(repo / REL), "sellar")
caso("(observación) y «sellar» no da salida (se niega: versión con sello)", rc != 0, out[:90])

# 6. Colisión de nombres al aplanar la ruta
repo = repo_proyecto("r05_t99_col_"); tmps.append(repo)
a = rx.Registro(repo / "a" / "b.jsonl"); b = rx.Registro(repo / "a__b.jsonl")
caso("(observación) «a/b.jsonl» y «a__b.jsonl» comparten sello", a.sello == b.sello, a.sello.name)
experimento_completo(a, "peor")
eb = lanza(lambda: experimento_completo(b, "peor"), rx.RegistroError) or lanza(b.verificar, rx.RegistroError)
ea = lanza(a.verificar, rx.RegistroError)
caso("dos registros cuyos nombres colisionan no se pisan el sello", ea is None and eb is None,
     f"a: {str(ea)[:60] if ea else 'íntegro'} · b: {str(eb)[:60] if eb else 'íntegro'}")

# 7. Fuera de git y después git init
d = tmpdir("r05_t99_init_"); tmps.append(d)
reg = rx.Registro(d / "reg.jsonl")
exp = experimento_completo(reg, "peor")
caso("(control) fuera de git, sello junto al registro", reg.sello == d / "reg.jsonl.sello")
git(d, "init", "-q")
reg2 = rx.Registro(d / "reg.jsonl")
ok, motivo = detecta(reg2)
caso("(observación) tras git init en la carpeta: el sello se busca en .git y falla cerrado", ok, motivo[:80])
git(d, "add", "reg.jsonl"); git(d, "-c", "commit.gpgsign=false", "commit", "-q", "-m", "r")
caso("(observación) salida: subir el registro tal como está", not detecta(rx.Registro(d / "reg.jsonl"))[0])

for t in tmps:
    borrar(t)
fin()
