"""r05_00 · Vuelve a ejecutar un script de una ronda anterior (r02, r03 o r04) sin tocarlo, sentencia a sentencia, como hacía
`r02_00_r01_por_sentencias.py` con los r01. Con la 0.5.0 varios scripts se cortan por dos cambios deliberados:
- el sello vive dentro de .git (H-37): los `git add <registro>.sello` de los scripts que subían el sello (r02 y r03) ya no casan
  con ningún fichero. Aquí, antes de importar el script, se envuelve `git` de r02_comun y r03_comun para que quite de un
  `git add` las rutas «*.sello» que no existen (lo mismo que hizo a mano la r04 al adaptar r03_01 y r03_02);
- una variante no se repite con un intento abierto (H-40, punto 5): las secuencias que lo hacían lanzan RegistroError.
Cada sentencia de primer nivel se ejecuta aparte y, si lanza, se anota «[EXCEPCIÓN]» y se sigue con la siguiente; los casos
que dependen de una sentencia cortada caen en cascada (se dice en qa.md).

Uso: python3 -B r05_00_por_sentencias.py <raíz> <script de una ronda anterior>
"""
import ast
import sys
import traceback
from pathlib import Path

raiz, script = sys.argv[1], Path(sys.argv[2]).resolve()
sys.argv = [str(script), raiz]
sys.path.insert(0, str(script.parent))
import r02_comun  # noqa: E402
import r03_comun  # noqa: E402


def _envolver(mod):
    original = mod.git

    def git(carpeta, *args, **kw):
        if args and args[0] == "add":
            base = Path(carpeta)
            args = tuple(a for a in args if not (a.endswith(".sello") and not (base / a).exists() and not Path(a).exists()))
            if len(args) == 1:
                return ""
        return original(carpeta, *args, **kw)

    mod.git = git


_envolver(r02_comun)
_envolver(r03_comun)

fuente = script.read_text(encoding="utf-8")
arbol = ast.parse(fuente, str(script))
ns = {"__name__": "__main__", "__file__": str(script)}
for nodo in arbol.body:
    codigo = compile(ast.Module(body=[nodo], type_ignores=[]), str(script), "exec")
    try:
        exec(codigo, ns)   # noqa: S102 - scripts del propio ticket
    except SystemExit:
        raise
    except BaseException as e:   # noqa: BLE001
        ult = traceback.extract_tb(e.__traceback__)[-1]
        print(f"[EXCEPCIÓN] línea {nodo.lineno} de {script.name}: {type(e).__name__}: {str(e)[:160]} "
              f"(en {Path(ult.filename).name}:{ult.lineno})")
