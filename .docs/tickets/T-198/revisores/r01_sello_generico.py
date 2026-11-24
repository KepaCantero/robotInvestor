"""QA r01 (T-198): ¿la migración «archivo sin sello y sin fichero → se sella vacío» vale solo para F9 o para cualquier archivo?
Borra HA (o F4, F6) junto con su clave en sellos_integridad.json y abre el almacén. Antes de T-198 debe fallar cerrado.
Uso: python r01_sello_generico.py <ruta de 11_Ejecutor>"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from bloque_a.almacen import ARCHIVOS, Almacen  # noqa: E402

fallos = 0
for archivo, autor, entrada in (("HA", "AG-18", {"tipo_entrada": "INC", "id": "INC-2026-0001"}),
                                ("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": "PRG-2026-0001"}),
                                ("F6", "AG-20", {"tipo_entrada": "FUE", "id": "FUE-2026-0001"})):
    with tempfile.TemporaryDirectory() as d:
        c = Path(d) / "estado"
        Almacen(c).escribir(archivo, autor, entrada)
        (c / ARCHIVOS[archivo]).unlink()
        s = json.loads((c / "sellos_integridad.json").read_text(encoding="utf-8"))
        s.pop(archivo)
        (c / "sellos_integridad.json").write_text(json.dumps(s), encoding="utf-8")
        try:
            alm = Almacen(c)
            print(f"{archivo}: ABRE con {len(alm.leer(archivo))} entradas (la historia desaparece sin aviso)")
            fallos += 1
        except Exception as e:  # noqa: BLE001
            print(f"{archivo}: falla cerrado ({type(e).__name__}: {e})")
sys.exit(1 if fallos else 0)
