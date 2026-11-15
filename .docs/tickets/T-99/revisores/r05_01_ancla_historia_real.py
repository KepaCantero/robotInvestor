"""r05_01 · El ancla de la 0.5.0 con historias reales (H-35 y lo que lo rodea).
1. En un clon nuevo del repositorio del proyecto (la raíz revisada y, si se da, un clon completo de origin): el registro por
   defecto (misma ruta relativa) se crea, se anota, se sube, se sigue anotando y se verifica; tiempo de una lectura.
2. Fusiones DESPUÉS del registro: sin avance rápido que no lo tocan, una octopus con una rama que lo alarga, historias sin
   relación (con y sin registro propio).
3. Cambiar de rama con anotaciones que solo están en la otra (sello por worktree, no por rama).
4. Commits que borran y vuelven a añadir el registro (git rm --cached y add; renombrar y volver), truncado y restaurado.
5. `git gc --aggressive --prune=now` y `git repack -ad`.
Uso: .venv/bin/python -B r05_01_ancla_historia_real.py <raíz> [<clon completo del proyecto>]"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r05_comun import (AHORA, DESPUES, RAIZ, REL, borrar, caso, clon_del_proyecto, cronometro, detecta, experimento_completo,  # noqa: E402
                       fin, git, lanza, lineas, pre, repo_proyecto, rx, subir, tmpdir, escribir_lineas)

tmps = []
origenes = [("raíz revisada", RAIZ)] + ([("clon completo", Path(sys.argv[2]).resolve())] if len(sys.argv) > 2 else [])

# 1. El registro por defecto en la historia real del proyecto
for nombre, origen in origenes:
    c = clon_del_proyecto(origen); tmps.append(c)
    superficial = git(c, "rev-parse", "--is-shallow-repository")
    fusiones = git(c, "rev-list", "--merges", "--count", "HEAD")
    lista = git(c, "rev-list", "--full-history", "--parents", "HEAD", "--", str(REL)).splitlines()
    caso(f"(referencia) {nombre}: superficial={superficial}, {fusiones} fusiones; rev-list lista {len(lista)} commits sin el registro", True)
    reg = rx.Registro(c / REL)
    e = lanza(lambda: reg.prerregistrar(pre(), "qa", ahora=AHORA), rx.RegistroError)
    caso(f"{nombre}: el primer prerregistro del registro por defecto se escribe", e is None, str(e)[:100] if e else "")
    if e:
        continue
    exp = "EXP-2026-0001"
    n = reg.intento(exp, "v1", ahora=DESPUES)["n"]; reg.resultado(exp, n, "peor", ahora=DESPUES)
    subir(c, REL, mensaje="registro")
    n = reg.intento(exp, "v2", ahora=DESPUES)["n"]; reg.resultado(exp, n, "mejor", ahora=DESPUES)
    t = cronometro(); v = reg.verificar(); dt = t()
    caso(f"{nombre}: subido y anotado después: verificar = {v} en {dt:.2f} s", v == 5 and dt < 2.0)
    caso(f"{nombre}: el sello está dentro de .git y el árbol solo tiene el registro",
         reg.sello.is_relative_to(Path(git(c, "rev-parse", "--absolute-git-dir"))) and
         git(c, "status", "--porcelain", "--untracked-files=all").split() == ["M", REL.as_posix()], str(reg.sello.parent.name))
    subir(c, REL, mensaje="registro 2")
    caso(f"{nombre}: tras el segundo commit, verificar = {reg.verificar()}", reg.verificar() == 5)

# 2. Fusiones después del registro
repo = repo_proyecto("r05_t99_fus_"); tmps.append(repo)
reg = rx.Registro(repo / REL)
exp = experimento_completo(reg, "peor"); subir(repo, REL)
for rama, f in (("x", "x.txt"), ("y", "y.txt")):
    git(repo, "checkout", "-q", "-b", rama, "develop")
    (repo / f).write_text(rama, encoding="utf-8"); git(repo, "add", f); git(repo, "commit", "-q", "-m", rama)
git(repo, "checkout", "-q", "-b", "z", "develop")
n = reg.intento(exp, "v2", ahora=DESPUES)["n"]; reg.resultado(exp, n, "mejor", ahora=DESPUES); subir(repo, REL, mensaje="z")
git(repo, "checkout", "-q", "develop")
ok, motivo = detecta(reg)
caso("(observación) en develop, con dos anotaciones que solo están en la rama z: falla cerrado (sello por worktree)", ok, motivo[:90])
git(repo, "merge", "-q", "--no-ff", "--no-edit", "x")
git(repo, "merge", "-q", "--no-edit", "y", "z")   # octopus: y no toca el registro, z lo alarga
caso("octopus (y sin registro nuevo, z que lo alarga) tras una fusión sin avance rápido: se lee",
     not detecta(reg)[0] and reg.verificar() == 5, detecta(reg)[1][:80])
caso("(control) la octopus tiene tres padres", len(git(repo, "rev-list", "--parents", "-n1", "HEAD").split()) == 4)
otro = repo_proyecto("r05_t99_otro_"); tmps.append(otro)
(otro / "nada.txt").write_text("x", encoding="utf-8"); git(otro, "add", "nada.txt"); git(otro, "commit", "-q", "-m", "otro")
git(repo, "fetch", "-q", str(otro), "develop:otro")
git(repo, "merge", "-q", "--no-edit", "--allow-unrelated-histories", "-X", "ours", "otro")
caso("fusión de una historia sin relación y sin registro: se lee", not detecta(reg)[0], detecta(reg)[1][:80])
otro2 = repo_proyecto("r05_t99_otro2_"); tmps.append(otro2)
experimento_completo(rx.Registro(otro2 / REL), "mejor"); subir(otro2, REL)
git(repo, "fetch", "-q", str(otro2), "develop:otro2")
git(repo, "merge", "-q", "--no-edit", "--allow-unrelated-histories", "-s", "ours", "otro2")
ok, motivo = detecta(reg)
caso("fusión «-s ours» de una historia con OTRO registro en la misma ruta: falla cerrado", ok, motivo[:90])

# 3. Borrar y volver a añadir; renombrar y volver; truncar y restaurar
for titulo, pasos in (
    ("git rm --cached y volver a añadir el mismo contenido", [("rm", "--cached", "-q", str(REL)), ("commit", "-q", "-m", "fuera"),
                                                            ("add", str(REL)), ("commit", "-q", "-m", "dentro")]),
    ("renombrar el registro y volver a su nombre", [("mv", str(REL), str(REL) + ".bak"), ("commit", "-q", "-m", "mv"),
                                                    ("mv", str(REL) + ".bak", str(REL)), ("commit", "-q", "-m", "mv2")]),
):
    repo = repo_proyecto("r05_t99_rm_"); tmps.append(repo)
    reg = rx.Registro(repo / REL)
    experimento_completo(reg, "peor"); subir(repo, REL)
    for p in pasos:
        git(repo, *p)
    ok, motivo = detecta(reg)
    caso(f"(límite: falla cerrado para siempre) {titulo}", ok, motivo[:90])

repo = repo_proyecto("r05_t99_trunc_"); tmps.append(repo)
reg = rx.Registro(repo / REL)
exp = experimento_completo(reg, "peor"); subir(repo, REL)
completo = lineas(reg.ruta)
escribir_lineas(reg.ruta, completo[:2]); subir(repo, REL, mensaje="truncado")
escribir_lineas(reg.ruta, completo); subir(repo, REL, mensaje="restaurado")
ok, motivo = detecta(reg)
caso("truncado subido y restaurado en el commit siguiente: se detecta (la historia lo recuerda)", ok, motivo[:90])

# 4. gc y repack
repo = repo_proyecto("r05_t99_gc_"); tmps.append(repo)
reg = rx.Registro(repo / REL)
exp = experimento_completo(reg, "peor"); subir(repo, REL)
n = reg.intento(exp, "v2", ahora=DESPUES)["n"]; reg.resultado(exp, n, "mejor", ahora=DESPUES)
git(repo, "gc", "-q", "--aggressive", "--prune=now"); git(repo, "repack", "-q", "-ad")
caso("tras gc --aggressive --prune=now y repack -ad, con dos anotaciones sin subir: se lee y el sello sigue",
     not detecta(reg)[0] and reg.sello.exists(), detecta(reg)[1][:80])
escribir_lineas(reg.ruta, lineas(reg.ruta)[:3])
caso("tras el gc, quitar lo no subido se sigue detectando", detecta(reg)[0], detecta(reg)[1][:80])

for t in tmps:
    borrar(t)
fin()
