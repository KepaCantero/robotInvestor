"""r02_00 · Vuelve a ejecutar un script r01 de T-99 sin tocarlo, sentencia a sentencia: con el registro 0.2.0 varias
manipulaciones de r01 ya fallan cerradas con una excepción que r01 no esperaba y que cortaba el resto del script. Aquí cada
sentencia de primer nivel se ejecuta aparte y, si lanza, se anota «[EXCEPCIÓN]» y se sigue con la siguiente.

Con --sello, `escribir()` de r01_comun rehace también el sello del registro a partir de la última línea escrita: es el
atacante que reescribe el fichero Y su sello (lo que, según el implementador, solo delata el ancla de git). Sin --sello, el
script r01 se comporta como en la ronda r01 (el sello queda el que escribió el registro).

Uso: python3 r02_00_r01_por_sentencias.py <raíz> <script r01> [--sello]
"""
import ast
import json
import sys
import traceback
from pathlib import Path

raiz, script = sys.argv[1], Path(sys.argv[2]).resolve()
rehacer_sello = "--sello" in sys.argv[3:]
sys.argv = [str(script), raiz]
sys.path.insert(0, str(script.parent))
import r01_comun  # noqa: E402

if rehacer_sello:
    _escribir = r01_comun.escribir

    def escribir(reg, ls, final="\n"):
        _escribir(reg, ls, final)
        ultima = next((x for x in reversed(ls) if x.strip()), None)
        try:
            e = json.loads(ultima) if ultima else None
        except ValueError:
            e = None
        if isinstance(e, dict) and "_seq" in e and "_hash" in e:
            reg.sello.write_text(json.dumps({"seq": e["_seq"], "hash": e["_hash"]}) + "\n", encoding="utf-8")
        elif ultima is None:
            reg.sello.write_text(json.dumps({"seq": 0, "hash": "0" * 64}) + "\n", encoding="utf-8")

    r01_comun.escribir = escribir

fuente = script.read_text(encoding="utf-8")
arbol = ast.parse(fuente, str(script))
ns = {"__name__": "__main__", "__file__": str(script)}
for nodo in arbol.body:
    codigo = compile(ast.Module(body=[nodo], type_ignores=[]), str(script), "exec")
    try:
        exec(codigo, ns)   # noqa: S102 - scripts r01 del propio ticket
    except SystemExit:
        raise
    except BaseException as e:   # noqa: BLE001
        ult = traceback.extract_tb(e.__traceback__)[-1]
        print(f"[EXCEPCIÓN] línea {nodo.lineno} de {script.name}: {type(e).__name__}: {str(e)[:160]} "
              f"(en {Path(ult.filename).name}:{ult.lineno})")
