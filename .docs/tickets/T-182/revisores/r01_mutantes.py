"""QA r01 de T-182 (Claude). Mutantes propios contra las pruebas del ticket, cada uno en una copia temporal.

`.venv/bin/python .docs/tickets/T-182/revisores/r01_mutantes.py [pruebas…]`. Sin argumentos usa la prueba del ticket.
Imprime MUERTO o VIVO por mutante; un VIVO que cambia el comportamiento es hallazgo. Código 1 si queda alguno vivo.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

raiz = Path(__file__).resolve().parents[4]
ej = Path("bloque_a/11_Ejecutor")
pruebas = sys.argv[1:] or ["tests/test_t182_procedencia.py"]
MF, ORQ = "bloque_a/mantenimiento_fuentes.py", "bloque_a/orquestacion.py"
RED, SIN, REF = "bloque_a/redaccion.py", "bloque_a/sintesis.py", "bloque_a/referencias.py"
mutaciones = [
    (RED, 'if any(sint.control_est06(res, nombre, Path(ruta).read_text(encoding="utf-8")) for nombre, ruta in rutas.items()) and "G3-EST-06" not in bloq:', 'if False:'),
    (SIN, 'control_est06(res, "paquete", paquete)\n', 'None\n'),
    (ORQ, 'pieza.update(afirmacion="Pieza en cuarentena", extracto="", direccion="neutra")', 'pass'),
    (ORQ, 'pieza.pop("pronostico_fuente", None)', 'pass'),
    (ORQ, 'if ref.get("ref_id") in retiradas:', 'if False:'),
    (ORQ, 'if evd.get("estado_verificacion") == "FUENTE_RETIRADA" or fuente in self.referencias.retiradas_f9(as_of):', 'if False:'),
    (ORQ, 'retirar_por_manipulacion(self, fuente, as_of, run_id)\n                    continue', 'retirar_por_manipulacion(self, fuente, as_of, run_id)'),
    (MF, 'if not ref or ref["archivo"] != "F9" or ', 'if not ref or '),
    (MF, 'if refs.registro_bajas_f9 and refs.registro_bajas_f9.exists():', 'if False:'),
    (REF, 'and "REF-" + r["ref_id"] not in retiradas]', ']'),
    (REF, 'if dia <= str(as_of)[:10]}', '}'),
]


def correr(carpeta):
    return subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *pruebas], cwd=carpeta / ej,
                          text=True, capture_output=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})


vivos = []
with tempfile.TemporaryDirectory() as tmp:
    copia = Path(tmp)
    shutil.copytree(raiz / "bloque_a", copia / "bloque_a", ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    base = correr(copia)
    if base.returncode:
        raise SystemExit("La base no pasa:\n" + base.stdout[-2000:])
    for ruta, antes, despues in mutaciones:
        archivo = copia / ej / ruta
        original = archivo.read_text(encoding="utf-8")
        assert original.count(antes) == 1, (ruta, antes)
        archivo.write_text(original.replace(antes, despues), encoding="utf-8")
        r = correr(copia)
        archivo.write_text(original, encoding="utf-8")
        muerto = r.returncode == 1 and " failed" in r.stdout
        print(("MUERTO " if muerto else "VIVO   ") + f"{ruta}: {antes[:90]}", flush=True)
        if not muerto:
            vivos.append(antes)
print(f"\n{len(vivos)} vivos de {len(mutaciones)}")
sys.exit(1 if vivos else 0)
