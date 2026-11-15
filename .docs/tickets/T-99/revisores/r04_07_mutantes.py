"""r04_07 · Mutantes del revisor sobre lo nuevo de la 0.4.0 (sello local, git que no responde, turno, «fallido» tardío,
RI_AGENTE, sellar, enlaces simbólicos). Cada mutante cambia `registro_experimentos.py` de un worktree DESECHABLE y se mira si
lo matan (1) las pruebas del implementador y (2) los scripts r04_01, r04_04 y r04_06 del revisor (más hallazgos que sin
mutar). Siempre deja el fichero como estaba. Uso: .venv/bin/python -B r04_07_mutantes.py <worktree desechable>"""
import re
import subprocess
import sys
from pathlib import Path

W = Path(sys.argv[1]).resolve()
assert W != Path("/home/user/robotinvestor"), "los mutantes nunca van en el árbol principal"
F = W / ".docs/scripts/registro_experimentos.py"
PY = str(W / ".venv/bin/python")
DIR = Path(__file__).resolve().parent
ORIGINAL = F.read_bytes()

MUTANTES = [
    ("M01 sello varias por detrás sin estar en git", "if k < len(out) - 1 and not (en_git", "if False and not (en_git"),
    ("M02 sello por delante del registro se admite", "        if not en_cadena:\n", "        if not en_cadena and k <= len(out):\n"),
    ("M03 sin sello siempre se admite", "if ultima is None or len(out) == 1 or (en_git", "if True or (en_git"),
    ("M04 sello muy por detrás con cualquier git", "k < len(out) - 1 and not (en_git is not None and texto.encode(\"utf-8\") == en_git)",
     "k < len(out) - 1 and not (en_git is not None)"),
    ("M05 fallido tardío no cuenta para adoptar", "and not d[\"fallido_tardio\"]", ""),
    ("M06 fallido tardío mira intentos anteriores", "for j in suyos if j[\"n\"] > i[\"n\"])", "for j in suyos if j[\"n\"] < i[\"n\"])"),
    ("M07 el lector no pasa por el turno", "            self._esperar(turno, fcntl.LOCK_EX, \"esperando turno\")\n",
     "            if not compartido:\n                self._esperar(turno, fcntl.LOCK_EX, \"esperando turno\")\n"),
    ("M08 el escritor suelta el turno antes de esperar el cerrojo", "                if compartido:   # el lector pasa por el turno y lo suelta enseguida\n",
     "                if True:\n"),
    ("M09 RI_AGENTE no válido cae en el de claude", "if AGENTE_VALIDO else None", "if AGENTE_VALIDO else RAIZ / \".docs\" / \"experimentos\" / \"registro_claude.jsonl\""),
    ("M10 RI_AGENTE sin validar", "AGENTE_VALIDO = re.fullmatch(r\"[a-z0-9_-]{1,32}\", AGENTE) is not None", "AGENTE_VALIDO = True"),
    ("M11 sellar sin mirar la versión", "            if con_sello:\n", "            if False:\n"),
    ("M12 sellar no deja la marca", "s[\"sellado_a_mano\"] = True", "pass"),
    ("M13 git que no reconoce el repositorio: sin ancla", "        if dir_git.returncode != 0:", "        if dir_git.returncode != 0:\n            return None\n        if False:"),
    ("M14 HEAD ilegible: sin ancla", "        if cabeza.returncode == 1 and not cabeza.stderr.strip():", "        if cabeza.returncode != 0:"),
    ("M15 enlace simbólico sin resolver", "self.ruta = Path(os.path.realpath(ruta))", "self.ruta = Path(ruta)"),
    ("M16 sin fcntl se escribe igual", "            if not compartido:\n                raise RegistroError(\"este sistema",
     "            if False:\n                raise RegistroError(\"este sistema"),
    ("M17 sin comprobar HEAD como prefijo", "        if en_head is not None and not texto.encode(\"utf-8\").startswith(en_head):",
     "        if False:"),
    ("M18 la marca a mano no se arrastra", "if a_mano or getattr(self, \"sello_a_mano\", False):", "if a_mano:"),
]


def cuenta_hallazgos():
    total = 0
    for s in ("r04_01_sello_local.py", "r04_04_fallido_tardio.py", "r04_06_agente_sellar_scripts.py"):
        r = subprocess.run([PY, "-B", str(DIR / s), str(W)], capture_output=True, text=True, timeout=900)
        m = re.search(r"(\d+)/(\d+) como pide el plan", r.stdout)
        total += 1000 if m is None else int(m.group(2)) - int(m.group(1))
    return total


def pruebas_matan():
    r = subprocess.run([PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", str(W / ".docs/scripts/pruebas_registro_experimentos.py")],
                       capture_output=True, text=True, cwd=W, timeout=900)
    return r.returncode != 0


try:
    base = cuenta_hallazgos()
    print(f"sin mutar: {base} hallazgo(s) en los scripts del revisor; pruebas del implementador {'fallan' if pruebas_matan() else 'pasan'}")
    vivos_impl, vivos_todo = [], []
    for nombre, viejo, nuevo in MUTANTES:
        texto = ORIGINAL.decode("utf-8")
        assert texto.count(viejo) == 1, f"{nombre}: el trozo a mutar no aparece una sola vez"
        F.write_text(texto.replace(viejo, nuevo), encoding="utf-8")
        mi = pruebas_matan()
        mr = cuenta_hallazgos() > base
        if not mi:
            vivos_impl.append(nombre)
        if not mi and not mr:
            vivos_todo.append(nombre)
        print(f"[{'MUERTO' if mi or mr else 'VIVO'}] {nombre} · pruebas del implementador: {'lo matan' if mi else 'no'}; "
              f"scripts del revisor: {'lo matan' if mr else 'no'}", flush=True)
        F.write_bytes(ORIGINAL)
    print(f"\nvivos frente a las pruebas del implementador: {len(vivos_impl)} de {len(MUTANTES)} {vivos_impl}")
    print(f"vivos frente a todo: {len(vivos_todo)} de {len(MUTANTES)} {vivos_todo}")
finally:
    F.write_bytes(ORIGINAL)
