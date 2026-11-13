"""QA r01 (T-88 y T-91): motor de mutantes. Aplica cada mutante (sustitución exacta, una sola vez) en una COPIA del repo
(worktree), ejecuta primero las pruebas del ticket y, si sobrevive, la suite entera de A (-x), y restaura el archivo.

  .venv/bin/python -I .docs/tickets/T-88/revisores/r01_04_mutantes.py RAIZ_DE_LA_COPIA [--sin-suite] [--solo=M1,M2] [--suite=a.py,b.py]
Con --suite, la segunda etapa son esas pruebas (suites relacionadas) en lugar de la suite entera (más rápido).
Nunca sobre el árbol principal: se niega si RAIZ es la raíz del repo del script."""
import os
import subprocess
import sys
import time
from pathlib import Path

PRINCIPAL = Path(__file__).resolve().parents[4]


def ejecutar(mutantes, pruebas_ticket, detectores=()):
    """mutantes: [(id, descripción, archivo relativo a 11_Ejecutor, viejo, nuevo)]; detectores: [(nombre, [args])] scripts propios
    que se lanzan contra la copia mutada si el mutante sobrevive a la suite."""
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    raiz = Path(args[0]).resolve()
    assert raiz != PRINCIPAL, "nunca sobre el árbol principal"
    ej = raiz / "bloque_a" / "11_Ejecutor"
    solo = next((a.split("=", 1)[1].split(",") for a in sys.argv if a.startswith("--solo=")), None)
    py = str(PRINCIPAL / ".venv" / "bin" / "python")
    env = {**os.environ, "PYTHONPATH": str(ej)}
    resumen = []
    for mid, desc, archivo, viejo, nuevo in mutantes:
        if solo and mid not in solo:
            continue
        ruta = ej / archivo
        original = ruta.read_text(encoding="utf-8")
        n = original.count(viejo)
        if n != 1:
            print(f"ERROR {mid}: el patrón aparece {n} veces", flush=True)
            resumen.append((mid, "ERROR"))
            continue
        ruta.write_text(original.replace(viejo, nuevo), encoding="utf-8")
        t0 = time.time()
        try:
            p = subprocess.run([py, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *pruebas_ticket], cwd=ej, env=env,
                               capture_output=True, text=True)
            estado = "DETECTADO (pruebas del ticket)" if p.returncode else None
            if estado is None and "--sin-suite" not in sys.argv:
                suite = next((a.split("=", 1)[1].split(",") for a in sys.argv if a.startswith("--suite=")), [])
                p = subprocess.run([py, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *suite], cwd=ej, env=env,
                                   capture_output=True, text=True)
                etapa = "suites relacionadas" if suite else "suite entera"
                estado = f"DETECTADO ({etapa})" if p.returncode else None
            if p.returncode:
                fallo = [x for x in p.stdout.splitlines() if x.startswith("FAILED") or x.startswith("ERROR")][:1]
                estado += f" · {fallo[0][:140] if fallo else ''}"
            else:
                estado = ("SOBREVIVE a las pruebas del ticket" if "--sin-suite" in sys.argv
                          else "SOBREVIVE a las suites relacionadas" if any(a.startswith("--suite=") for a in sys.argv)
                          else "SOBREVIVE a la suite")
                for nombre, dargs in detectores:
                    q = subprocess.run([py, "-I", *[str(x).replace("{EJ}", str(ej)) for x in dargs]], capture_output=True, text=True)
                    estado += f" · {nombre}: {'lo detecta' if q.returncode else 'no lo detecta'}"
        finally:
            ruta.write_text(original, encoding="utf-8")
        print(f"{mid:4} {desc}: {estado} ({time.time() - t0:.0f} s)", flush=True)
        resumen.append((mid, estado))
    vivos = [m for m, e in resumen if e.startswith("SOBREVIVE")]
    print(f"== {len(resumen)} mutantes; sobreviven {len(vivos)}: {vivos}")
