"""r04_08 · El ancla en un repositorio con fusiones ANTERIORES al registro (como el del proyecto). `git rev-list --full-history
--parents HEAD -- <ruta>` reescribe los padres, y en ese modo git incluye SIEMPRE las fusiones, toquen o no la ruta. Una fusión
de antes de que existiera el registro sale en la lista con la ruta ausente, y `_comprobar_ancla` lo toma por «el registro se
quitó del repositorio»: el primer prerregistro del registro por defecto no se puede escribir.
También se lee (solo «ver», que no crea nada) el registro por defecto de la raíz revisada.
Uso: .venv/bin/python -B r04_08_fusion_previa.py <raíz>"""
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r04_comun import AHORA, REL, RAIZ, borrar, caso, cli, experimento_completo, fin, git, lanza, pre, repo_proyecto, rx  # noqa: E402

tmps = []

# 1. Repositorio con historia completa y una fusión (sin avance rápido) de antes del registro
repo = repo_proyecto(); tmps.append(repo)
git(repo, "checkout", "-q", "-b", "tema")
(repo / "a.txt").write_text("tema\n", encoding="utf-8"); git(repo, "add", "a.txt"); git(repo, "commit", "-q", "-m", "tema")
git(repo, "checkout", "-q", "develop")
(repo / "b.txt").write_text("develop\n", encoding="utf-8"); git(repo, "add", "b.txt"); git(repo, "commit", "-q", "-m", "develop")
git(repo, "merge", "-q", "--no-ff", "--no-edit", "tema")
lista = git(repo, "rev-list", "--full-history", "--parents", "HEAD", "--", str(REL))
caso("(referencia) rev-list --full-history --parents lista la fusión aunque no toque el registro", bool(lista), lista[:60])
reg = rx.Registro(repo / REL)
e = lanza(lambda: reg.prerregistrar(pre(), "qa", ahora=AHORA), rx.RegistroError)
caso("primer prerregistro en un repositorio con una fusión anterior al registro: se escribe", e is None, str(e)[:110] if e else "")

# 2. Lo mismo con el registro creado y subido ANTES de la fusión (el caso que cubren las pruebas): se lee
repo = repo_proyecto(); tmps.append(repo)
reg = rx.Registro(repo / REL)
experimento_completo(reg); git(repo, "add", str(REL)); git(repo, "commit", "-q", "-m", "registro")
git(repo, "checkout", "-q", "-b", "tema")
(repo / "a.txt").write_text("tema\n", encoding="utf-8"); git(repo, "add", "a.txt"); git(repo, "commit", "-q", "-m", "tema")
git(repo, "checkout", "-q", "develop")
(repo / "b.txt").write_text("d\n", encoding="utf-8"); git(repo, "add", "b.txt"); git(repo, "commit", "-q", "-m", "develop")
git(repo, "merge", "-q", "--no-ff", "--no-edit", "tema")
e = lanza(reg.verificar, rx.RegistroError)
caso("(control) registro subido antes de una fusión que no lo toca: se lee", e is None, str(e)[:100] if e else "")

# 3. El registro por defecto de la raíz revisada (solo lectura: «ver» con el fichero ausente no crea nada)
superficial = git(RAIZ, "rev-parse", "--is-shallow-repository")
rc, out = cli("ver", env={"RI_AGENTE": "claude"})
caso(f"el registro por defecto de la raíz revisada (clon superficial: {superficial}) se puede usar", rc == 0, out[:120])
caso("(control) «ver» no creó «.docs/experimentos»", not (RAIZ / ".docs" / "experimentos").exists())

for t in tmps:
    borrar(t)
fin()
