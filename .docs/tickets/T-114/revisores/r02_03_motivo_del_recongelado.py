"""QA r02 de T-114 · ¿Es cierto el motivo del último re-congelado de `formas_flujos_mock.json` (línea del 14-11 de
`goldens/REGISTRO.md`: «en el ciclo V6 simulado, los Analistas de RF (AG-04) y de TCV (AG-25) dejan de emitir CT-08, porque el
encargo CT-06 les comunica ahora el umbral de su tipo (0,65) [...]; no cambia ningún formato»)?

En una copia desechable (ruta con «qa_f3_mut»), se deshace SOLO el cambio de T-117 r02 que el motivo cita (el umbral de GC1
que el encargo CT-06 comunica: el del tipo de activo en V6 → el general), se generan las formas con la copia y se comparan con
el golden congelado. Si el motivo es cierto, la única diferencia son los emisores de CT-08 del ciclo V6 (vuelven AG-04 y AG-25)
y nada de rutas, tipos ni combinaciones. Restaura la copia al acabar.

Uso:  python r02_03_motivo_del_recongelado.py <copia_desechable>
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PY = "/home/user/robotinvestor/.venv/bin/python"
VIEJO = ('"umbral_senal_gc1": (v6.umbral_gc1(self, clase) if v6.activo(self, "gc1.por_codigo")\n'
         '                                    else parametro(self.cfg, "seleccion.umbral_senal_gc1")),')
NUEVO = '"umbral_senal_gc1": parametro(self.cfg, "seleccion.umbral_senal_gc1"),'
GENERAR = """
import json, sys, tempfile
from pathlib import Path
sys.path[:0] = ['tests', '.']
import goldens_ct as g
esquemas, _ = g.leer_a_mano()
with tempfile.TemporaryDirectory() as tmp:
    flujos = g.capturar_flujos(Path(tmp), '2026-06-05')
print(json.dumps(g.formas(flujos, esquemas), ensure_ascii=False, sort_keys=True))
"""


def diferencias(a, b, ruta=""):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                yield f"{ruta}/{k}: solo en lo generado sin el cambio de T-117 → {json.dumps(b[k], ensure_ascii=False)[:160]}"
            elif k not in b:
                yield f"{ruta}/{k}: solo en el golden → {json.dumps(a[k], ensure_ascii=False)[:160]}"
            else:
                yield from diferencias(a[k], b[k], f"{ruta}/{k}")
    elif a != b:
        yield f"{ruta}: golden {json.dumps(a, ensure_ascii=False)[:160]} · sin el cambio {json.dumps(b, ensure_ascii=False)[:160]}"


def main() -> int:
    copia = Path(sys.argv[1]).resolve()
    assert "qa_f3_mut" in str(copia), "solo en una copia desechable"
    ej = copia / "bloque_a" / "11_Ejecutor"
    ruta = ej / "bloque_a" / "orquestacion.py"
    original = ruta.read_text(encoding="utf-8")
    assert original.count(VIEJO) == 1, "el cambio de T-117 r02 no está como se esperaba"
    try:
        ruta.write_text(original.replace(VIEJO, NUEVO), encoding="utf-8")
        r = subprocess.run([PY, "-c", GENERAR], cwd=ej, capture_output=True, text=True)
    finally:
        ruta.write_text(original, encoding="utf-8")
    if r.returncode:
        print("no se pudo generar:", r.stderr[-800:])
        return 0
    sin_cambio = json.loads(r.stdout.strip().splitlines()[-1])
    golden = json.loads((ej / "tests" / "goldens" / "formas_flujos_mock.json").read_text(encoding="utf-8"))
    difs = list(diferencias(golden, sin_cambio))
    print(f"diferencias entre el golden y lo generado sin el cambio de T-117 r02: {len(difs)}")
    for d in difs:
        print("  " + d)
    solo_emisores = all("/ciclo_semanal_v6/mensajes/CT-08.ENCARGO/emisores" in d for d in difs)
    print("el motivo es cierto (solo cambian los emisores de CT-08 del ciclo V6): " + str(bool(difs) and solo_emisores))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
