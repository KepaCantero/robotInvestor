# -*- coding: utf-8 -*-
"""Hallazgo 1 (revisión independiente V0.66) — la foto de las «acciones» pierde «ok» y «posicion».

`_acciones` (pruebas/doradas.py) proyecta cada acción de H a {condicion, codigo, regla}: pierde «ok»,
«posicion», «senal», «perdida_pct», «nivel» y «aviso_registrado». Los ESPERADO de los recorridos dorados
tampoco los miran (jornada: vigilar_objetivo solo mira regla/condicion/codigo; el ok de H-10 no lo mira
nadie), así que un cambio en el «ok» o en la «posicion» informados de una acción no lo ve NI la batería
dorada NI la de la jornada. Aquí se demuestra con dos mutaciones sobre una COPIA del árbol (el árbol real
no se toca): flip de ok en H-10 y posicion fantasma en H-10; en ambas, `pruebas_doradas.py` y
`pruebas_jornada.py` siguen en verde con la foto entregada byte a byte igual.

Uso: python3 hallazgo_1_revision_v066_acciones_ok_posicion.py   (desde la carpeta marcoC o desde scripts/)
Imprime FALLA si el defecto existe (las mutaciones pasan inadvertidas) y OK si está corregido
(p. ej. con la proyección {condicion, codigo, ok, posicion, regla} la batería dorada cae).
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def _raiz():
    """La raíz de marcoC: argv[1], esta carpeta si lo es, o el ascendente que tenga LEEME.md y pruebas/doradas.py."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).resolve()
    for candidato in [AQUI, *AQUI.parents]:
        if (candidato / "LEEME.md").is_file() and (candidato / "pruebas" / "doradas.py").is_file():
            return candidato
    raise SystemExit("No encuentro la raíz de marcoC (pásala como argv[1])")


RAIZ = _raiz()
IGNORA = shutil.ignore_patterns("__pycache__", "*.pyc", ".venv", ".git", "*.zip")

H10 = 'acciones.append({"posicion": pid, "regla": "H-10", "condicion": c["id"], "ok": False, "codigo": "H-10"})'
MUTA_OK = 'acciones.append({"posicion": pid, "regla": "H-10", "condicion": c["id"], "ok": True, "codigo": "H-10"})'
# H-01 no lo mira el guarda interno de vigilar (solo H-02/H-05/H-10/H-12), así que tocar su «posicion» no
# tiene efectos laterales dentro del módulo: si la foto no cambia, es que la proyección se la llevó.
H01 = 'acciones.append({"posicion": pid, "regla": "H-01", "ok": r["ok"], "codigo": r["codigo"]})'
MUTA_POS = 'acciones.append({"posicion": "POS-FANTASMA", "regla": "H-01", "ok": r["ok"], "codigo": r["codigo"]})'


def corre(copia, bateria):
    r = subprocess.run([sys.executable, str(copia / "pruebas" / bateria)],
                       capture_output=True, text=True, cwd=str(copia))
    ult = [l for l in r.stdout.splitlines() if l.strip()]
    return r.returncode, (ult[-1] if ult else "(sin salida)")


def sonda(ruta_relativa, viejo, nuevo, baterias):
    """Muta un módulo en una COPIA del árbol y corre las baterías que se le dan."""
    with tempfile.TemporaryDirectory() as tmp:
        copia = Path(tmp) / "marcoC"
        shutil.copytree(RAIZ, copia, ignore=IGNORA, symlinks=True)
        mod = copia / ruta_relativa
        texto = mod.read_text(encoding="utf-8")
        if texto.count(viejo) != 1:
            return f"NO APLICABLE (la línea aparece {texto.count(viejo)} veces en {ruta_relativa})"
        mod.write_text(texto.replace(viejo, nuevo, 1), encoding="utf-8")
        resultados = [(b, corre(copia, b)) for b in baterias]
        vista = "INADVERTIDA" if all(rc == 0 for _, (rc, _) in resultados) else "CAZADA"
        partes = [f"{b} {'PASA' if rc == 0 else 'cae'}" for b, (rc, _) in resultados]
        return f"{vista}: {'; '.join(partes)}"


def foto_entregada_sin_ok():
    """Evidencia estática: la acción H-10 de la foto entregada no lleva ni ok ni posicion."""
    foto = (RAIZ / "pruebas" / "doradas" / "jornada.json").read_text(encoding="utf-8")
    trozo = foto.split('"regla": "H-10"')[0][-300:]
    return '"codigo": "H-10"' in trozo and '"ok"' not in trozo and '"posicion"' not in trozo


def main():
    print("Hallazgo 1 (V0.66): la proyección de acciones pierde ok/posicion; mutaciones sobre copia:")
    r1 = sonda("validador/vigilancia.py", H10, MUTA_OK, ["pruebas_doradas.py", "pruebas_jornada.py"])
    print(f"  S1 flip ok H-10 False->True (jornada):    {r1}")
    r2 = sonda("validador/vigilancia.py", H01, MUTA_POS, ["pruebas_doradas.py", "pruebas_semana.py"])
    print(f"  S2 posicion de H-01 a POS-FANTASMA (semana): {r2}")
    e = foto_entregada_sin_ok()
    print(f"  Evidencia estática: la acción H-10 de jornada.json va sin ok/posicion: {'sí' if e else 'no'}")
    inadvertidas = ("INADVERTIDA" in r1 or "NO APLICABLE" in r1) and ("INADVERTIDA" in r2 or "NO APLICABLE" in r2)
    print("HALLAZGO 1:", "FALLA (las mutaciones pasan inadvertidas)" if inadvertidas
          else "OK (al menos una mutación es cazada; revisar el detalle)")
    return 1 if inadvertidas else 0


if __name__ == "__main__":
    sys.exit(main())
