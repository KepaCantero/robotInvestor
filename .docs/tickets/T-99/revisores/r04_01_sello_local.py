"""r04_01 · El sello local de la 0.4.0 (H-25, H-26, H-18, H-31): qué cierra y qué abre que el sello no vaya en git.
Órdenes de rutina que devuelven el registro atrás (stash, checkout, reset, stash -a, clean -X), clones nuevos, pulls con líneas
de otra máquina, el sello varias anotaciones por detrás sin pull, borrar el sello y dos worktrees del mismo repositorio.
Todos los repositorios son temporales y llevan el .gitignore del proyecto. Uso: .venv/bin/python -B r04_01_sello_local.py <raíz>"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r04_comun import (REL, borrar, caso, detecta, escribir_lineas, experimento_completo, fin, git, lanza, lineas,  # noqa: E402
                       pre, remoto_y_clon, repo_proyecto, rx, sello, subir)

tmps = []


def montar():
    """v1 «mejor» subido (3 anotaciones) y la misma v1 «peor» sin subir (5): contradictoria, adoptable=False."""
    repo = repo_proyecto()
    tmps.append(repo)
    reg = rx.Registro(repo / REL)
    exp = experimento_completo(reg, "mejor", "v1")
    subir(repo)
    experimento_completo(reg, "peor", "v1", exp=exp)
    return repo, reg, exp


# 1. El sello no se sube: git status no lo ve, y git add lo rechaza
repo, reg, exp = montar()
estado = git(repo, "status", "--short", "--ignored")
ignorados = [x for x in estado.splitlines() if x.startswith("!!")]
visibles = [x for x in estado.splitlines() if not x.startswith("!!")]
caso("sello, cerrojo y turno quedan ignorados; git status solo ve el registro", visibles == [f"M {REL}"] and
     any(".sello" in x for x in ignorados) and any(".turno" in x for x in ignorados) and any(".lock" in x for x in ignorados),
     f"visibles {visibles}; ignorados {ignorados}")
p = lanza(lambda: git(repo, "add", str(REL) + ".sello"))
caso("git add del sello se rechaza (está en .gitignore)", p is not None, str(p)[:80])

# 2. H-25: stash, checkout y reset --hard de lo no subido se detectan, y adoptable no cambia
for orden in (["stash", "-q"], ["checkout", "--", str(REL)], ["reset", "-q", "--hard"], ["stash", "-q", "-u"]):
    repo, reg, exp = montar()
    antes = reg.adoptable(exp)
    git(repo, *orden)
    ok, d = detecta(reg)
    caso(f"H-25: git {' '.join(orden)} que quita la repetición «peor» sin subir: se detecta", ok and antes is False, d)

# 3. stash --all (también lo ignorado): se lleva registro y sello a la vez, como hacía la 0.3.0 con el sello en git
repo, reg, exp = montar()
git(repo, "stash", "-q", "--all")
ok, d = detecta(reg)
caso("(límite declarado: tocar el sello) git stash --all se lleva el sello con el registro", ok,
     f"{d}; adoptable={'—' if ok else reg.adoptable(exp)}")
p = lanza(lambda: git(repo, "stash", "pop", "-q"))
caso("(observación) …y git stash pop falla porque la lectura volvió a crear «.lock» y «.turno»", p is not None, str(p)[:160])
repo, reg, exp = montar()
git(repo, "stash", "-q", "--all")
git(repo, "stash", "pop", "-q")
ok, d = detecta(reg)
caso("…sin leer entre medias, stash pop lo deja como estaba", not ok and reg.verificar() == 5, d)

# 4. git clean -X (solo lo ignorado) borra el sello: con algo sin subir, falla cerrado, y no hay orden para salir
repo, reg, exp = montar()
git(repo, "clean", "-q", "-f", "-d", "-X")
ok, d = detecta(reg)
caso("git clean -fdX borra el sello y hay intentos sin subir: falla cerrado", ok and not reg.sello.exists(), d)
e = lanza(reg.sellar, rx.RegistroError)
caso("…sellar no lo arregla (es de la 0.4.0): sigue cerrado", e is not None, str(e)[:100])
git(repo, "checkout", "--", str(REL))
ok, d = detecta(reg)
caso("(límite declarado: tocar el sello) …y un checkout después lo deja leer sin la repetición «peor»", ok,
     f"{d}; adoptable={'—' if ok else reg.adoptable(exp)}")

# 5. Borrar el sello a mano y checkout: límite declarado (tocar el sello)
repo, reg, exp = montar()
reg.sello.unlink()
git(repo, "checkout", "--", str(REL))
ok, d = detecta(reg)
caso("(límite declarado: tocar el sello) rm del sello + checkout", ok, f"{d}; adoptable={'—' if ok else reg.adoptable(exp)}")

# 6. H-26 (a): reset --hard HEAD~1 de un commit ya subido, en la máquina que lo escribió: el sello va por delante
repo, reg, exp = montar()
subir(repo, mensaje="repetición")
remoto, clon = remoto_y_clon(repo)
tmps += [remoto, clon]
git(repo, "reset", "-q", "--hard", "HEAD~1")
ok, d = detecta(reg)
caso("H-26 (a): reset --hard HEAD~1 de un commit subido, en la máquina que anotó: se detecta", ok, d)

# 7. H-26 (b): otro clon que no anotó nada y se pone al día con un push forzado: límite declarado
reg_c = rx.Registro(clon / REL)
caso("clon nuevo sin sello, idéntico a HEAD: se lee", reg_c.verificar() == 5 and not reg_c.sello.exists())
git(repo, "push", "-q", "--force", "origin", "develop")   # el remoto pierde la repetición «peor»
git(clon, "fetch", "-q")
git(clon, "reset", "-q", "--hard", "origin/develop")
ok, d = detecta(reg_c)
caso("(límite declarado: push forzado) clon que solo leía y hace reset a origin tras el push forzado", ok, d)

# 8. Pull con líneas de otra máquina: el sello local queda varias anotaciones por detrás y se admite; luego se pone al día
repo = repo_proyecto(); tmps.append(repo)
reg = rx.Registro(repo / REL)
exp = experimento_completo(reg, "peor", "v1"); subir(repo)
remoto, clon = remoto_y_clon(repo); tmps += [remoto, clon]
reg_c = rx.Registro(clon / REL)
for v in ("v2", "v3"):
    experimento_completo(reg_c, "peor", v, exp=reg_c.prerregistrar(pre(), "qa", ahora="2026-11-12T10:00:00+00:00")["exp_id"])
    subir(clon)
git(clon, "push", "-q", "origin", "develop")
git(repo, "pull", "-q", "--ff-only", "origin", "develop")
ok, d = detecta(reg)
caso("pull que trae 8 anotaciones de otra máquina (sello 3 en local): se admite", not ok, f"{d}; sello {sello(reg)['seq']}")
experimento_completo(reg, "peor", "v9", exp=exp)
caso("…y la siguiente escritura pone el sello al día", sello(reg)["seq"] == len(lineas(reg.ruta)) == 11,
     f"sello {sello(reg)['seq']}, {len(lineas(reg.ruta))} líneas")

# 9. Pull con líneas de otra máquina y una anotación local sin subir: la fusión rompe la cadena (decisión 3, falla cerrado)
repo = repo_proyecto(); tmps.append(repo)
reg = rx.Registro(repo / REL)
exp = experimento_completo(reg, "peor", "v1"); subir(repo)
remoto, clon = remoto_y_clon(repo); tmps += [remoto, clon]
reg_c = rx.Registro(clon / REL)
experimento_completo(reg_c, "peor", "v2", exp=exp); subir(clon); git(clon, "push", "-q", "origin", "develop")
experimento_completo(reg, "mejor", "v3", exp=exp)    # sin subir
p = lanza(lambda: git(repo, "pull", "-q", "--no-rebase", "origin", "develop"))
ok, d = detecta(reg)
caso("(decisión 3) pull con una anotación local sin subir: el pull se niega o la lectura falla cerrado",
     p is not None or ok, f"pull: {'se niega' if p else 'hecho'}; {d}")

# 10. Sello que se queda atrás dos anotaciones sin pull (dos os.replace que fallan seguidos): falla cerrado
repo = repo_proyecto(); tmps.append(repo)
reg = rx.Registro(repo / REL)
exp = reg.prerregistrar(pre(), "qa", ahora="2026-11-12T10:00:00+00:00")["exp_id"]
original = os.replace
fallos = []


def no_mueve(a, b):
    if str(b).endswith(".sello"):
        fallos.append(1)
        raise OSError("disco lleno (simulado)")
    return original(a, b)


os.replace = no_mueve
try:
    e1 = lanza(lambda: reg.intento(exp, "v1", ahora="2026-11-12T11:00:00+00:00"), rx.RegistroError)
    e2 = lanza(lambda: reg.resultado(exp, 1, "peor", ahora="2026-11-12T11:00:00+00:00"), rx.RegistroError)
finally:
    os.replace = original
ok, d = detecta(reg)
caso("dos sellos que no se pudieron poner al día: las dos escrituras lo dicen y la lectura falla cerrado",
     e1 is not None and e2 is not None and ok, d)
tmp_sobra = reg.sello.with_name(reg.sello.name + ".tmp")
ignorado = git(repo, "check-ignore", str(tmp_sobra.relative_to(repo)), check=False)
caso("…y el «.sello.tmp» que queda está ignorado por git (H-31)", tmp_sobra.exists() and bool(ignorado), ignorado)

# 11. Dos worktrees del mismo repositorio: cada uno su sello; si los dos anotan, la fusión falla cerrado
repo = repo_proyecto(); tmps.append(repo)
reg = rx.Registro(repo / REL)
exp = experimento_completo(reg, "peor", "v1"); subir(repo)
wt = repo.parent / (repo.name + "_wt")
git(repo, "worktree", "add", "-q", "-b", "otra", str(wt)); tmps.append(wt)
reg_w = rx.Registro(wt / REL)
caso("worktree enlazado: se lee sin sello (idéntico a HEAD)", reg_w.verificar() == 3)
experimento_completo(reg_w, "mejor", "v2", exp=exp); subir(wt)
experimento_completo(reg, "peor", "v3", exp=exp); subir(repo)
p = lanza(lambda: git(repo, "merge", "-q", "--no-edit", "otra"))
ok, d = detecta(reg)
caso("(decisión 3) fusionar dos worktrees que anotaron: conflicto o cadena rota, falla cerrado", p is not None or ok,
     f"merge: {'conflicto' if p else 'hecho'}; {d}")

# 12. Restaurar una versión anterior del registro desde git (checkout HEAD~1 -- registro): se detecta (sello y ancla)
repo, reg, exp = montar()
subir(repo, mensaje="repetición")
git(repo, "checkout", "HEAD~1", "--", str(REL))
ok, d = detecta(reg)
caso("checkout HEAD~1 -- registro (versión vieja en el árbol): se detecta", ok, d)

for t in tmps:
    borrar(t)
fin()
