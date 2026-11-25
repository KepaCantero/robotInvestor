"""QA r01 de T-201 (revisor): entradas hostiles, base frente a T-201.

Uso: python r01_ataques.py <11_Ejecutor de la base> <11_Ejecutor de T-201> <carpeta_tmp>
Lanza `r01_sonda.py` con cada árbol (procesos separados: los dos paquetes se llaman `bloque_a`) y compara caso a caso.
Lo único que puede diferir es lo declarado en INC-T201-01: el mensaje del TypeError de `ruta` cuando falta la clave (None).
Termina con 1 si hay cualquier otra diferencia.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

BASE, NUEVO, TMP = (Path(a).resolve() for a in sys.argv[1:4])
SONDA = Path(__file__).with_name("r01_sonda.py")


def sondear(ej: Path, nombre: str) -> dict:
    tmp = TMP / nombre
    tmp.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1", BLOQUE_A_RAIZ=str(ej.parent))
    r = subprocess.run([str(Path(sys.executable)), str(SONDA), str(ej), str(tmp)], capture_output=True, text=True, env=env,
                       cwd=str(tmp), check=False)
    if r.returncode:
        print(r.stderr[-3000:])
        raise SystemExit(f"la sonda falló en {nombre}")
    return json.loads(r.stdout)


a, b = sondear(BASE, "base"), sondear(NUEVO, "nuevo")
assert set(a) == set(b), set(a) ^ set(b)
declarados, otros = [], []
for k in sorted(a):
    if a[k] == b[k]:
        continue
    decl = (k.startswith("ruta_") and a[k].get("exc") == b[k].get("exc") == "TypeError" and "no está en la configuración" in b[k]["msg"])
    (declarados if decl else otros).append(k)
    print(("DECLARADO " if decl else "DIFERENCIA ") + k + f"\n   base : {a[k]}\n   T-201: {b[k]}")
excs = sum(1 for v in a.values() if "exc" in v)
print(f"casos: {len(a)} (con excepción en la base: {excs}); iguales: {len(a) - len(declarados) - len(otros)}; "
      f"diferencias declaradas: {len(declarados)}; otras diferencias: {len(otros)}")
print("VEREDICTO:", "EQUIVALENTE salvo lo declarado" if not otros else "DISTINTO")
sys.exit(1 if otros else 0)
