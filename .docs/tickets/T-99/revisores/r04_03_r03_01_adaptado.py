"""r04_03 · `r03_01_ancla_historial.py` adaptado a la 0.4.0 sin tocar el original: los repositorios temporales llevan el
.gitignore del proyecto y cada commit sube solo el registro (el sello es local). Los casos de stash, checkout y reset ya no
los esconde un sello subido. Lo demás, igual.
"""
"""r03_01 · El ancla del registro 0.3.0 en todo el historial de git (H-13, H-14): reescritura de la historia (reset, amend y
force-push a un remoto), stash y checkout de lo no subido, commits mixtos, historias largas, renombrar, subcarpetas,
worktrees, clones superficiales, git que no responde y nombres con comodines de pathspec.
En cada ataque «declarado» el atacante también rehace el sello, para que solo el ancla pueda detectarlo.
Uso: .venv/bin/python -B r03_01_ancla_historial.py <raíz>"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r04_comun import repo_proyecto  # noqa: E402
from r03_comun import (borrar, caso, cronometro, escribir_lineas, experimento_completo, fin, git, lanza, lineas,  # noqa: E402
                       pre, rehacer_sello, repo_temporal, rx, subir, tmpdir)

REL = Path(".docs/experimentos/registro_claude.jsonl")


def montar(n_experimentos=2, rel=REL):
    """Repositorio con un registro de n experimentos completos, subido (registro y sello) en un commit por experimento."""
    repo = repo_proyecto()
    reg = rx.Registro(repo / rel)
    for i in range(n_experimentos):
        exp = experimento_completo(reg, "peor" if i % 2 else "mejor")
        subir(repo, rel, mensaje=f"experimento {exp}")
    return repo, reg


def truncar(reg, n=2):
    ls = lineas(reg.ruta)
    escribir_lineas(reg.ruta, ls[:-n])
    rehacer_sello(reg)


def detecta(reg):
    e = lanza(reg.verificar, rx.RegistroError)
    return e is not None, (str(e)[:110] if e else f"verificar = {reg.verificar()}")


tmps = []

# 1. Control: truncado subido con un commit (H-13) y commit mixto que toca el registro y otros ficheros
repo, reg = montar(); tmps.append(repo)
truncar(reg)
(repo / "otro.txt").write_text("cambio\n", encoding="utf-8")
git(repo, "add", "-A"); git(repo, "commit", "-q", "-m", "mixto")
ok, d = detecta(reg)
caso("truncado subido en un commit que también toca otros ficheros: se detecta", ok, d)

# 2. reset --hard HEAD~1 de un commit ya subido al remoto: el registro y el sello (los dos con seguimiento) vuelven atrás.
#    Variante v1 «mejor» (subido) y la misma v1 «peor» (subido después): contradictoria, no adoptable.
remoto = tmpdir("r03_t99_remoto_"); tmps.append(remoto)
git(remoto, "init", "-q", "--bare", "-b", "develop")
repo, reg = montar(1); tmps.append(repo)
exp = reg.anotaciones()[0]["exp_id"]
experimento_completo(reg, "peor", "v1", exp=exp); subir(repo, REL, mensaje="repetición")
git(repo, "remote", "add", "origin", str(remoto)); git(repo, "push", "-q", "origin", "develop")
n_antes, adop_antes = reg.verificar(), reg.adoptable(exp)
git(repo, "reset", "-q", "--hard", "HEAD~1")
ok, d = detecta(reg)
en_origen = git(repo, "show", f"origin/develop:{REL}").count("\n") + 1
caso("reset --hard HEAD~1 de un experimento ya subido al remoto: se detecta (o al menos se avisa de que origin tiene más)",
     ok, f"antes {n_antes} anotaciones y adoptable={adop_antes}; tras el reset {d} y adoptable="
         f"{'—' if ok else reg.adoptable(exp)}; origin/develop tiene {en_origen}")

# 3. amend del último commit con el registro truncado y el sello rehecho, y force-push: otro clon lo acepta
repo, reg = montar(); tmps.append(repo)
remoto2 = tmpdir("r03_t99_remoto_"); tmps.append(remoto2)
git(remoto2, "init", "-q", "--bare", "-b", "develop")
git(repo, "remote", "add", "origin", str(remoto2)); git(repo, "push", "-q", "origin", "develop")
clon = tmpdir("r03_t99_clon_"); tmps.append(clon); clon.rmdir()
git(clon.parent, "clone", "-q", str(remoto2), str(clon))
truncar(reg)
git(repo, "add", "-A"); git(repo, "commit", "-q", "--amend", "-m", "experimento (reescrito)")
git(repo, "push", "-q", "--force", "origin", "develop")
ok, d = detecta(reg)
caso("(límite por declarar) amend + force-push del último experimento: el clon que lo hizo lo detecta", ok, d)
git(clon, "fetch", "-q"); git(clon, "reset", "-q", "--hard", "origin/develop")
ok, d = detecta(rx.Registro(clon / REL))
caso("(límite por declarar) …y otro clon que se pone al día con reset lo detecta", ok, d)
r = subprocess.run(["git", "-C", str(clon), "pull", "-q", "--rebase"], capture_output=True, text=True)
caso("(referencia) en ese clon, la versión anterior sigue en el reflog", "HEAD@{1}" in git(clon, "reflog", "-n", "2"),
     git(clon, "reflog", "-n", "2").replace("\n", " | ")[:120])

# 4. stash y checkout de anotaciones aún no subidas (lo que «solo protege el sello»)
for orden in (["stash", "-q"], ["checkout", "-q", "--", ".docs/experimentos"], ["reset", "-q", "--hard"]):
    repo, reg = montar(1); tmps.append(repo)
    exp = reg.anotaciones()[0]["exp_id"]
    experimento_completo(reg, "peor", "v1", exp=exp)   # la misma variante sale «peor» y no se sube: contradictoria
    antes = f"{reg.verificar()} y adoptable={reg.adoptable(exp)}"
    git(repo, *orden)
    ok, d = detecta(reg)
    adop = "—" if ok else reg.adoptable(exp)
    caso(f"git {' '.join(orden[:1])}: los intentos aún no subidos desaparecen y se detecta (el sello debía protegerlos)", ok,
         f"antes {antes}; después {d}; adoptable = {adop}")

# 5. Sin sello y con el registro devuelto a lo de HEAD: se acepta (nuevo en la 0.3.0, H-18)
repo, reg = montar(1); tmps.append(repo)
exp = reg.anotaciones()[0]["exp_id"]
experimento_completo(reg, "peor", "v2", exp=exp)
reg.sello.unlink()
git(repo, "checkout", "-q", "--", str(REL))
ok, d = detecta(reg)
caso("(dentro del límite declarado: tocar el sello) borrar el sello y devolver el registro a HEAD: se detecta", ok, d)

# 6. El registro borrado del árbol de trabajo (sin commit): se detecta
repo, reg = montar(1); tmps.append(repo)
reg.ruta.unlink(); reg.sello.unlink()
ok, d = detecta(reg)
caso("registro y sello borrados del árbol de trabajo (subidos en HEAD): se detecta", ok, d)

# 7. Renombrar: con el truncado en el mismo commit que el git mv
repo, reg = montar(); tmps.append(repo)
nuevo = REL.with_name("registro_claude2.jsonl")
git(repo, "mv", str(REL), str(nuevo)); os.replace(repo / (str(REL) + ".sello"), repo / (str(nuevo) + ".sello"))   # el sello es local: se mueve a mano
reg2 = rx.Registro(repo / nuevo)
truncar(reg2)
git(repo, "add", "-A"); git(repo, "commit", "-q", "-m", "renombrado")
ok, d = detecta(reg)
caso("renombrar y truncar: el registro de siempre falla cerrado («se quitó»)", ok, d)
ok, d = detecta(reg2)
caso("(referencia) …y el registro nuevo empieza su historia en el renombrado (sin --follow)", not ok, d)

# 8. Subcarpeta profunda y worktree enlazado
rel_hondo = Path("a/b/c/d/e/registro.jsonl")
repo, reg = montar(2, rel_hondo); tmps.append(repo)
truncar(reg); git(repo, "commit", "-q", "-am", "truncado")
ok, d = detecta(reg)
caso("subcarpeta profunda: truncado subido se detecta", ok, d)
repo, reg = montar(); tmps.append(repo)
wt = tmpdir("r03_t99_wt_"); tmps.append(wt); wt.rmdir()
git(repo, "worktree", "add", "-q", "--detach", str(wt))
regw = rx.Registro(wt / REL)
caso("worktree enlazado: el registro se lee", lanza(regw.verificar) is None, lanza(regw.verificar) or regw.verificar())
truncar(regw); git(wt, "commit", "-q", "-am", "truncado en el worktree")
ok, d = detecta(regw)
caso("worktree enlazado: truncado subido desde el worktree se detecta", ok, d)
shutil.move(str(repo / ".git"), str(repo / "git_movido"))   # el «.git» del worktree apunta ahora a una carpeta que no existe
ok, d = detecta(regw)
caso("worktree cuyo repositorio principal ya no está («.git» que apunta a nada): falla cerrado", ok, d)

# 9. Clones superficiales
repo, reg = montar(4); tmps.append(repo)
sup = tmpdir("r03_t99_sup_"); tmps.append(sup); sup.rmdir()
git(sup.parent, "clone", "-q", "--depth", "1", f"file://{repo}", str(sup))
regs = rx.Registro(sup / REL)
e = lanza(regs.verificar)
caso("clon superficial (--depth 1): se lee sin falsa alarma", e is None, e or regs.verificar())
truncar(regs); git(sup, "commit", "-q", "-am", "truncado en el clon superficial")
ok, d = detecta(regs)
caso("clon superficial: truncado subido encima del commit frontera se detecta", ok, d)

# 10. Git que no responde aunque el registro está en un repositorio con commits (H-14): truncado con sello rehecho
def roto(nombre, estropear, restaurar=None):
    repo, reg = montar(); tmps.append(repo)
    truncar(reg)
    deshacer = estropear(repo)
    try:
        ok, d = detecta(reg)
    finally:
        if deshacer:
            deshacer()
    caso(f"{nombre}: falla cerrado", ok, d)


def propietario_ajeno(repo):
    subprocess.run(["chown", "-R", "nobody", str(repo)], check=True)
    return None


def head_a_objeto_que_no_existe(repo):
    (repo / ".git" / "refs" / "heads" / "develop").write_text("1" * 40 + "\n", encoding="utf-8")
    for p in (repo / ".git").glob("packed-refs"):
        p.unlink()
    return None


def config_global_rota(repo):
    casa = tmpdir("r03_t99_casa_"); tmps.append(casa)
    (casa / ".gitconfig").write_text("[core\n roto\n", encoding="utf-8")
    viejo = os.environ.get("HOME")
    os.environ["HOME"] = str(casa)
    return lambda: os.environ.__setitem__("HOME", viejo)


def git_vacio(repo):
    shutil.rmtree(repo / ".git"); (repo / ".git").mkdir()
    return None


def git_fichero_a_nada(repo):
    shutil.rmtree(repo / ".git"); (repo / ".git").write_text("gitdir: /no/existe/.git\n", encoding="utf-8")
    return None


roto("repositorio de otro usuario (safe.directory, «dubious ownership»)", propietario_ajeno)
roto("HEAD que apunta a un objeto que no existe", head_a_objeto_que_no_existe)
roto("configuración global de git mal formada (todas las órdenes de git fallan)", config_global_rota)
roto("«.git» vacío", git_vacio)
roto("«.git» fichero que apunta a una carpeta que no existe", git_fichero_a_nada)

# 11. Nombres con comodines de pathspec: «r[1].jsonl» junto a «r1.jsonl»
repo = repo_proyecto(); tmps.append(repo)
rg = rx.Registro(repo / "r[1].jsonl"); r1 = rx.Registro(repo / "r1.jsonl")
experimento_completo(rg); experimento_completo(r1, "mejor"); experimento_completo(r1, "peor")
git(repo, "add", "-A"); git(repo, "commit", "-q", "-m", "dos registros")
experimento_completo(r1, "peor"); git(repo, "add", "-A"); git(repo, "commit", "-q", "-m", "r1 crece")
e = lanza(rg.verificar)
caso("registro «r[1].jsonl» con un «r1.jsonl» al lado: se lee sin falsa alarma", e is None, e or rg.verificar())
experimento_completo(rg, "peor", "v2", exp=rg.anotaciones()[0]["exp_id"])
git(repo, "add", "-A"); git(repo, "commit", "-q", "-m", "r[1] crece")
truncar(rg); git(repo, "add", "-A"); git(repo, "commit", "-q", "-m", "r[1] truncado")
ok, d = detecta(rg)
caso("registro «r[1].jsonl»: truncado subido se detecta", ok, d)

# 12. Historia larga: un commit por experimento (lo que pide la decisión (2): subir el registro al terminar cada uno)
for n in (100, 400):
    repo = repo_proyecto(); tmps.append(repo)
    reg = rx.Registro(repo / REL, ancla_git=False)   # se construye sin ancla (si no, cada escritura relee toda la historia)
    exp = reg.prerregistrar(pre(max_variantes=1000), "qa", ahora="2026-11-12T10:00:00+00:00")["exp_id"]
    subir(repo, REL)
    for i in range(n):
        k = reg.intento(exp, f"v{i}", ahora="2026-11-12T11:00:00+00:00")["n"]
        reg.resultado(exp, k, "peor", ahora="2026-11-12T11:00:00+00:00")
        git(repo, "add", str(REL)); git(repo, "commit", "-q", "-m", f"intento {k}")
    reg = rx.Registro(repo / REL)
    t = cronometro(); reg.verificar(); s = t()
    caso(f"historia de {n} commits del registro: una lectura tarda menos que la espera del cerrojo ({rx.CERROJO_ESPERA_S} s) "
         "con margen (< 1/10)", s < rx.CERROJO_ESPERA_S / 10, f"{s:.2f} s por lectura; el banco lee 4 o 5 veces por ejecución")

for p in tmps:
    subprocess.run(["chown", "-R", "root", str(p)], check=False, capture_output=True)
    borrar(p)
fin()
