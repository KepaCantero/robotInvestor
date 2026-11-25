"""QA r01 de T-181 (Claude). Mutantes propios contra las pruebas del ticket, cada uno en una copia temporal.

`.venv/bin/python .docs/tickets/T-181/revisores/r01_mutantes.py [pruebas…]`. Sin argumentos usa la prueba del ticket.
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
pruebas = sys.argv[1:] or ["tests/test_t181_fuentes.py"]
MF, ORQ, CLI = "bloque_a/mantenimiento_fuentes.py", "bloque_a/orquestacion.py", "bloque_a/cli.py"
mutaciones = [
    (MF, 'if mes < fecha[:7] and ', 'if '),                                         # CT-21 antes de cerrar el mes
    (MF, 'if op.get("estado") != "VIGENTE":', 'if False:'),                         # revisa opciones no vigentes
    (MF, 'set(op.get("evidencias_ps1", [])) - retiradas', 'set(op.get("evidencias_ps1", []))'),  # la raíz retirada cuenta
    (MF, 'if contiene_credenciales(motivo) or any(c in motivo for c in ("<", ">")):', 'if False:'),  # R8 en el motivo
    (MF, ' or len(motivo.splitlines()) != 1:', ':'),                                # motivo multilínea
    (MF, ' and not ficha.campo("Copia archivada")', ''),                            # borra con copia archivada
    (MF, 'if informe["resumen"]["incidencia_red"]:', 'if False:'),                  # aplica con la red caída
    (MF, 'if rev.get("accion") == "RETRACTADA" and r.get("retractacion"):', 'if rev.get("accion") == "RETRACTADA":'),
    (MF, ' or rev.get("url") != url:', ':'),                                        # repara con otra URL
    (MF, ' or copia.get("retractacion"):', ':'),                                    # repara con una copia retractada
    (MF, 'if ficha.q is None or q >= ficha.q:', 'if ficha.q is None or q > ficha.q:'),
    ('bloque_a/referencias.py', 'if q >= parametro(cfg, f"referencias.niveles_q.{nivel}"):', 'if q > parametro(cfg, f"referencias.niveles_q.{nivel}"):'),
    (MF, 'if e.get("estado_verificacion") != "FUENTE_RETIRADA":', 'if True:'),           # marca la EVD en cada pasada
    (MF, 'afectadas == op.get("revision_bajas", {}).get("evidencias_retiradas")', 'False'),  # F3 en cada pasada
    (MF, 'if not destino or (r.get("doi") and not isinstance(r.get("doi_codigo_http"), int)):', 'if not destino:'),
    (ORQ, 'if any(rid == fuente.removeprefix("REF-") and dia <= str(as_of)[:10]', 'if False and any(rid == fuente.removeprefix("REF-") and dia <= str(as_of)[:10]'),
    (ORQ, 'f["_evidencias_ps1"] = list(respaldos)', 'f["_evidencias_ps1"] = []'),
    (CLI, 'if dia <= datos["fecha"]}', '}'),
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
