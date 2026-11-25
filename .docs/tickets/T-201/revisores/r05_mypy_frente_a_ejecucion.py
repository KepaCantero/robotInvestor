"""QA r01 de T-201 (revisor): ¿comprueba mypy el mismo módulo que se ejecuta? ¿Oculta errores de los llamadores?

Uso: python r05_mypy_frente_a_ejecucion.py <11_Ejecutor> <carpeta_tmp>
1. Escribe en <carpeta_tmp> un fichero que lee cada nombre público (sin contar módulos) de los envoltorios ht02, ht03,
   ht07 y ht09 tal como existen en ejecución, y lo pasa por mypy con las opciones del gate (--ignore-missing-imports):
   ninguno puede dar «Module has no attribute». Es el mismo fichero en las dos ramas, así que el «*» exporta lo mismo.
2. Escribe en <carpeta_tmp> un llamador con una llamada mal hecha a cada envoltorio (aridad y tipos) y comprueba que mypy
   la señala: con T-201 los llamadores se comprueban contra la firma real, no contra Any.
No escribe nada en el árbol.
"""
import subprocess
import sys
import types
from pathlib import Path

EJ, TMP = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(EJ))
TMP.mkdir(parents=True, exist_ok=True)

import importlib  # noqa: E402

ENV = ["ht02", "ht03", "ht07", "ht09"]
fallo = False
accesos = ["from bloque_a.herramientas import ht02, ht03, ht07, ht09"]
for m in ENV:
    vivo = importlib.import_module(f"bloque_a.herramientas.{m}")
    publicos = sorted(n for n, v in vars(vivo).items() if not n.startswith("_") and not isinstance(v, types.ModuleType))
    accesos += [f"{m}.{n}" for n in publicos]
    print(f"{m}: {len(publicos)} nombres públicos en ejecución (sin contar módulos)")
todos = TMP / "llamador_todos.py"
todos.write_text("\n".join(accesos) + "\n", encoding="utf-8")


def mypy(fichero: Path) -> list[str]:
    r = subprocess.run([sys.executable, "-m", "mypy", "--ignore-missing-imports", "--no-error-summary", "--cache-dir",
                        str(TMP / ".mc"), str(fichero)], capture_output=True, text=True, cwd=str(EJ),
                       env={"MYPYPATH": str(EJ), "PATH": "/usr/bin:/bin"}, check=False)
    return [x for x in r.stdout.splitlines() if fichero.name in x and "error" in x]


faltan_en_mypy = mypy(todos)
print(f"nombres de ejecución que mypy no ve ({len(faltan_en_mypy)}):")
print("\n".join("  " + x.split("error: ")[1] for x in faltan_en_mypy[:20]))
fallo |= bool(faltan_en_mypy)

malas = TMP / "llamador_malo.py"
malas.write_text(
    "from bloque_a.herramientas import ht02, ht03, ht07, ht09\n"
    "ht03.evaluar_opcion(1, 2, 3)\n"
    "ht09.validar_seguimiento(informe=5, texto_breve=7)\n"
    "ht07.analizar(42)\n"
    "x: int = ht02.leer_fichas(['a'])\n"
    "ht09.no_existe()\n", encoding="utf-8")
lineas = mypy(malas)
print("\n".join(lineas))
# con T-201 cada línea tiene que dar un error de firma (no «Module has no attribute»), salvo la 6, que sí es attr-defined
vistas = {int(x.split(":")[1]) for x in lineas if "attr-defined" not in x} | {int(x.split(":")[1]) for x in lineas if "no_existe" in x}
faltan = sorted({2, 3, 4, 5, 6} - vistas)
print("llamadas mal hechas que mypy no ve:", faltan or "ninguna")
fallo |= bool(faltan)
sys.exit(1 if fallo else 0)
