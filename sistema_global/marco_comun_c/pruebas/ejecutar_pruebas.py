"""Ejecuta todos los casos: los válidos deben pasar; cada inválido debe fallar
exactamente con la regla que su nombre indica (inv_Vnn_...)."""
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
from validar_sobre import validar, cargar_json  # noqa: E402

ctx = json.loads((AQUI / "contexto.json").read_text(encoding="utf-8"))
ok = True
for ruta in sorted((AQUI / "validos").glob("*.json")):
    fallos = validar(cargar_json(ruta.read_text(encoding="utf-8")), ctx)
    estado = "OK " if not fallos else "FALLA"
    print(f"{estado} {ruta.name}" + ("" if not fallos else f"  -> {fallos}"))
    ok &= not fallos
for ruta in sorted((AQUI / "invalidos").glob("*.json")):
    esperada = re.search(r"inv_(V\d+)", ruta.name).group(1).replace("V", "V-")
    try:
        fallos = validar(cargar_json(ruta.read_text(encoding="utf-8")), ctx)
        reglas = {x["regla"] for x in fallos}
    except ValueError:          # el cargador estricto rechaza NaN e infinitos
        fallos, reglas = [{"regla": "V-01"}], {"V-01"}
    bien = reglas == {esperada}
    print(f"{'OK ' if bien else 'FALLA'} {ruta.name}  esperada={esperada} obtenida={sorted(reglas)}")
    ok &= bien
print("\nRESULTADO:", "TODAS LAS PRUEBAS PASAN" if ok else "HAY FALLOS")
sys.exit(0 if ok else 1)
