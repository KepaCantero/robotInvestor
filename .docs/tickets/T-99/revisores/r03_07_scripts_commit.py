"""r03_07 · Los cambios de commit_limpio.sh y commit.sh (H-12, H-18): la comprobación «registro con su sello» se extrae tal cual
de commit_limpio.sh y se ejecuta en una carpeta temporal con varias listas de rutas; commit.sh se lee.
Uso: .venv/bin/python -B r03_07_scripts_commit.py <raíz>"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r03_comun import DESPUES, RAIZ, borrar, caso, experimento_completo, fin, rx, tmpdir  # noqa: E402

limpio = (RAIZ / ".docs" / "scripts" / "commit_limpio.sh").read_text(encoding="utf-8").splitlines()
i = next(k for k, x in enumerate(limpio) if "H-18" in x)
bloque = []
for x in limpio[i + 1:]:
    bloque.append(x)
    if x == "done":
        break
fragmento = "\n".join(bloque)

d = tmpdir(); rel = ".docs/experimentos/registro_claude.jsonl"
reg = rx.Registro(d / rel)
exp = experimento_completo(reg)
viejo = reg.sello.read_bytes()
experimento_completo(reg, "peor", "v2", exp=exp)   # dos anotaciones más: el sello viejo queda dos por detrás


def comprobar(*rutas):
    guion = 'fallo(){ echo "FALLO: $*"; exit 1; }\nrutas=(' + " ".join(f"'{r}'" for r in rutas) + ")\n" + fragmento + "\necho PASA"
    p = subprocess.run(["bash", "-c", guion], cwd=d, capture_output=True, text=True)
    return p.stdout.strip()


caso("commit_limpio: el registro sin su sello se rechaza", comprobar(rel).startswith("FALLO"), comprobar(rel))
caso("commit_limpio: registro y sello juntos pasan", comprobar(rel, rel + ".sello") == "PASA")
caso("commit_limpio: el sello sin su registro se rechaza (en un clon, sello por delante del registro: bloqueado)",
     comprobar(rel + ".sello").startswith("FALLO"), comprobar(rel + ".sello"))
actual = reg.sello.read_bytes(); reg.sello.write_bytes(viejo)
caso("commit_limpio: registro y sello que no casan (sello dos por detrás) se rechazan antes del commit",
     comprobar(rel, rel + ".sello").startswith("FALLO"), comprobar(rel, rel + ".sello") + f" · verificar: {type(e).__name__ if (e := __import__('r03_comun').lanza(reg.verificar)) else 'íntegro'}")
reg.sello.write_bytes(actual)
tmp = Path(str(reg.sello) + ".tmp"); tmp.write_text("{}\n", encoding="utf-8")
caso("commit_limpio: un «.sello.tmp» que se cuela en las rutas se rechaza", comprobar(rel, rel + ".sello", rel + ".sello.tmp").startswith("FALLO"),
     comprobar(rel, rel + ".sello", rel + ".sello.tmp"))

commit = (RAIZ / ".docs" / "scripts" / "commit.sh").read_text(encoding="utf-8")
caso("commit.sh también comprueba que el registro se sube con su sello (con rutas explícitas no lo hace «git add -A»)",
     "sello" in commit, "commit.sh no menciona el sello")
caso("commit.sh ejecuta las pruebas de .docs/scripts (H-12)", "pruebas_*.py" in commit)
caso("las pruebas de .docs/scripts tienen un número mínimo, como los bloques (H-12, r02: quitar pruebas no se ve)",
     any(k in commit + "\n".join(limpio) for k in ("--minimo", "minimo_pruebas", "passed")), "solo el código de salida de pytest")
borrar(d)
fin()
