"""r05_05 · Mutantes del revisor sobre lo nuevo de la 0.5.0 (H-35, «fallido» tardío por `_seq`, no repetir con un intento abierto,
resultado anterior a su inicio, sello y cerrojos dentro de .git, lector sin permiso). Cada mutante cambia
`registro_experimentos.py` de un worktree DESECHABLE y se mira si lo matan (1) las pruebas del implementador
(`pruebas_registro_experimentos.py`) y (2) los scripts r05_01 a r05_04 del revisor (más hallazgos que sin mutar; r05_03 sin el
banco y r05_04 sin `pruebas_scripts.sh`). Siempre deja el fichero como estaba.
Uso: .venv/bin/python -B r05_05_mutantes.py <worktree desechable>"""
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
    ("M01 H-35 revertido: un commit sin el registro siempre es un borrado",
     "                if any(version(p) is not None for p in padres):\n", "                if True:\n"),
    ("M02 un borrado nunca se detecta", "                if any(version(p) is not None for p in padres):\n", "                if False:\n"),
    ("M03 el prefijo solo se mira contra el primer padre", "            for p in padres:\n                anterior", "            for p in padres[:1]:\n                anterior"),
    ("M04 tardío por instantes, no por la cadena",
     'and any(j["_seq"] < res[i["n"]]["_seq"] for j in suyos if j["n"] > i["n"])',
     'and any(_instante(j["inicio"], "i") < _instante(res[i["n"]]["registrado_en"], "r") for j in suyos if j["n"] > i["n"])'),
    ("M05 tardío también contra el propio intento", 'for j in suyos if j["n"] > i["n"])', 'for j in suyos if j["n"] >= i["n"])'),
    ("M06 sin la regla de no repetir con uno abierto", "            if abiertos:   # QA r04", "            if False:   # QA r04"),
    ("M07 la regla mira los abiertos de cualquier variante",
     'abiertos = [x["n"] for x in exp["intentos"] if _nfc(x["variante"]) == _nfc(variante) and x["n"] not in con_resultado]',
     'abiertos = [x["n"] for x in exp["intentos"] if x["n"] not in con_resultado]'),
    ("M08 la regla compara variantes sin NFC",
     'if _nfc(x["variante"]) == _nfc(variante) and x["n"] not in con_resultado]',
     'if x["variante"] == unicodedata.normalize("NFD", variante) and x["n"] not in con_resultado]'),
    ("M09 resultado anterior a su inicio admitido", '            if _instante(ahora, "ahora") < _instante(inicio, "inicio"):', "            if False:"),
    ("M10 sello y cerrojos junto al registro (0.4.0)", "        if self._carpeta_local is None:\n            return", "        if True:\n            return"),
    ("M11 nombre local sin la carpeta", 'self._carpeta_local = (base, rel.replace("/", "__"))', "self._carpeta_local = (base, Path(rel).name)"),
    ("M12 --git-path relativo sin anclar a la raíz", "base = base if base.is_absolute() else raiz / base", "base = base"),
    ("M13 el lector sin permiso falla", "            if compartido:   # H-39", "            if False:   # H-39"),
    ("M14 el sello de un worktree va a la carpeta común de git", '"rev-parse", "--git-path", "ri-registro"',
     '"rev-parse", "--git-common-dir"'),
]
SCRIPTS = [("r05_01_ancla_historia_real.py", []), ("r05_02_sello_en_git.py", []), ("r05_03_tardio_y_abiertos.py", ["--sin-banco"]),
           ("r05_04_cerrojo_lector_scripts.py", [])]


def cuenta_hallazgos():
    total = 0
    for s, extra in SCRIPTS:
        try:
            r = subprocess.run([PY, "-B", str(DIR / s), str(W), *extra], capture_output=True, text=True, timeout=900)
            m = re.search(r"(\d+)/(\d+) como pide el plan", r.stdout)
            total += 1000 if m is None else int(m.group(2)) - int(m.group(1))
        except subprocess.TimeoutExpired:
            total += 1000
    return total


def pruebas_matan():
    try:
        r = subprocess.run([PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", str(W / ".docs/scripts/pruebas_registro_experimentos.py")],
                           capture_output=True, text=True, cwd=W, timeout=900)
    except subprocess.TimeoutExpired:
        return True
    return r.returncode != 0


try:
    base = cuenta_hallazgos()
    print(f"hallazgos de los scripts sin mutar: {base}")
    vivos_p = vivos_s = 0
    for nombre, viejo, nuevo in MUTANTES:
        texto = ORIGINAL.decode("utf-8")
        assert texto.count(viejo) == 1, f"{nombre}: el patrón no está una sola vez"
        F.write_text(texto.replace(viejo, nuevo), encoding="utf-8")
        mp = pruebas_matan()
        h = cuenta_hallazgos()
        ms = h > base
        vivos_p += not mp; vivos_s += not ms
        print(f"[{'muerto' if mp else 'VIVO'} pruebas · {'muerto' if ms else 'VIVO'} scripts ({h})] {nombre}", flush=True)
        F.write_bytes(ORIGINAL)
    print(f"\n{len(MUTANTES)} mutantes: vivos frente a las pruebas {vivos_p}, frente a los scripts {vivos_s}")
finally:
    F.write_bytes(ORIGINAL)
