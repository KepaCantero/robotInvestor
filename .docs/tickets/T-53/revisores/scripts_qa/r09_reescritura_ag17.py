"""r09 · CA-03 con la reescritura de AG-17 (PB-39): el primer intento se bloquea por C12 (legibilidad) y el segundo pasa.
¿Dónde acaban los dos intentos, en modo backtest y en modo vivo? ¿Queda algo en _borradores? ¿Se entrega el bueno?
Variante: los dos intentos bloqueados."""
import pathlib, tempfile, json
from bloque_a import sintesis as sint
from bloque_a.configuracion import cargar_config, RUTA_UNIVERSO_EJEMPLO, DIR_EJECUTOR
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
orig = sint.ht09_validar
def con_c12(veces):
    n = {"i": 0}
    def f(bloque, paquete, extras, iv):
        r = orig(bloque, paquete, extras, iv)
        if iv is not None:
            n["i"] += 1
            if n["i"] <= veces:
                r = dict(r, dictamen="BLOQUEADO", comprobaciones=r["comprobaciones"] + [{"id": "C12", "resultado": "BLOQUEO", "detalle": ["FH 50 < 70 (simulado)"], "incidencias": [{"detalle": "FH 50 < 70 (simulado)"}]}])
        return r
    return f
for modo in ("backtest", "vivo"):
    for veces in (1, 2):
        sint.ht09_validar = con_c12(veces)
        tmp = pathlib.Path(tempfile.mkdtemp(dir="."))
        b = Bloque(cargar_config(extra={"modo": modo}), ProveedorCSV(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos"),
                   cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "e", tmp / "s")
        r = b.ciclo("2026-06-05", alcance={"clases": ["RV"]})
        arch = sorted(str(p.relative_to(tmp / "s")) for p in (tmp / "s").rglob("*") if p.is_file())
        dirs = sorted(str(p.relative_to(tmp / "s")) for p in (tmp / "s").rglob("*") if p.is_dir())
        print(f"[{modo}, bloqueos C12={veces}] entrega={r.get('entrega', 'ENTREGADA')} g3b={r.get('g3_entregables', {}).get('dictamen')}")
        print("    archivos:", arch)
        print("    _borradores restantes:", [d for d in dirs if "_borradores" in d])
        if r.get("entregables"):
            print("    rutas devueltas existen:", all(pathlib.Path(p).exists() for p in r["entregables"].values()))
sint.ht09_validar = orig
