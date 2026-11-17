"""QA r01 de T-175 (revisor): regresión de los ciclos mock V5 y V6 (doce clases). Escribe en <destino> el JSON, el visual y el
técnico de cada diseño con las rutas temporales normalizadas, para compararlos con `diff -r` entre dos copias.

    cd bloque_a/11_Ejecutor && ../../.venv/bin/python <ruta>/r01_03_regresion.py <destino>
"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "tests")
from conftest import AS_OF, RUTA_UNIVERSO_EJEMPLO, cargar_universo, config_pruebas, nuevo_bloque  # noqa: E402

destino = Path(sys.argv[1])
destino.mkdir(parents=True, exist_ok=True)
for diseno in ("v5", "v6"):
    tmp = tempfile.mkdtemp()
    cfg = config_pruebas(diseno=diseno) if diseno == "v6" else None
    r = nuevo_bloque(tmp, cargar_universo(RUTA_UNIVERSO_EJEMPLO), cfg=cfg).ciclo(AS_OF)
    for k in ("paquete_json", "informe_visual", "informe_tecnico"):
        t = Path(r["entregables"][k]).read_text(encoding="utf-8").replace(tmp, "<TMP>")
        (destino / f"{diseno}_{k}").write_text(t, encoding="utf-8")
    print(diseno, r.get("entrega") or "ENTREGADA", r["g3"].get("dictamen"))
