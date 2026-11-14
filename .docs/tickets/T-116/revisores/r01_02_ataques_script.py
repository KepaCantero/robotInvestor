"""QA r01 de T-116 · Ataques a `.docs/scripts/evidencias_plan_a.py` en una copia desechable del repositorio.

Mapa roto, prueba citada que no existe, que falla, que se salta o que es xfail, plan con una PB de más (bien y mal escrita),
fila que cambia de cobertura. Uso:  python r01_02_ataques_script.py <copia_desechable>
Cada caso restaura lo que toca. Imprime el código de salida y la última línea; «!!» marca lo que no falla cerrado.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PY = "/home/user/robotinvestor/.venv/bin/python"
copia = Path(sys.argv[1]).resolve()
assert "qa_f3_mut" in str(copia), "solo en la copia desechable"
SCRIPT = copia / ".docs/scripts/evidencias_plan_a.py"
MAPA = copia / "bloque_a/11_Ejecutor/tests/mapa_plan_pruebas.json"
PLAN = copia / "bloque_a/09_Pruebas/Plan de pruebas del Bloque A - V3.0.md"
HUECOS = copia / "bloque_a/11_Ejecutor/tests/test_fase4_huecos.py"
DOC = copia / "docs/evidencias_pruebas_bloque_a.md"


def correr(*args) -> tuple[int, str, str]:
    r = subprocess.run([PY, str(SCRIPT), *args], cwd=copia, capture_output=True, text=True)
    sal = (r.stdout + r.stderr).strip().splitlines()
    return r.returncode, (sal[-1][:170] if sal else ""), r.stdout + r.stderr


def caso(nombre: str, ruta: Path, cambio, args=(), espera_fallo=True, tambien=None):
    original = ruta.read_bytes()
    doc = DOC.read_bytes()
    try:
        ruta.write_text(cambio(original.decode("utf-8")), encoding="utf-8")
        rc, ult, todo = correr(*args)
        extra = f" · {tambien(todo)}" if tambien else ""
        aviso = "  !! no falla cerrado" if espera_fallo and rc == 0 else ""
        print(f"rc={rc} · {nombre} · {' '.join(args) or '(sin opciones)'} · {ult}{extra}{aviso}", flush=True)
    finally:
        ruta.write_bytes(original)
        DOC.write_bytes(doc)


def mapa(f):
    def cambio(texto):
        m = json.loads(texto)
        f(m)
        return json.dumps(m, ensure_ascii=False, indent=1)
    return cambio


rc, ult, _ = correr()
print(f"rc={rc} · base · {ult}")
caso("mapa: JSON truncado", MAPA, lambda t: t[:len(t) // 2])
caso("mapa: fichero vacío", MAPA, lambda t: "")
caso("mapa: una lista en vez de un objeto", MAPA, lambda t: "[]")
caso("mapa: prueba citada que no existe", MAPA, mapa(lambda m: m["PB-22"]["pruebas"].append("11_Ejecutor/tests/test_unitarias.py::test_no_existe")))
caso("mapa: prueba citada con parámetro", MAPA, mapa(lambda m: m["PB-22"]["pruebas"].append("11_Ejecutor/tests/test_t117_gc1.py::test_cada_tipo_usa_su_umbral[RF-0.65]")))
caso("mapa: se cita un fichero entero, sin prueba", MAPA, mapa(lambda m: m["PB-22"]["pruebas"].append("11_Ejecutor/tests/test_unitarias.py")))
caso("mapa: falta PB-40", MAPA, mapa(lambda m: m.pop("PB-40")))
caso("mapa: PB-99 de más", MAPA, mapa(lambda m: m.__setitem__("PB-99", dict(m["PB-01"]))))
caso("mapa: `pruebas` es un texto y no una lista", MAPA, mapa(lambda m: m["PB-22"].__setitem__("pruebas", m["PB-22"]["pruebas"][0])))
caso("mapa: `comprueba` es null", MAPA, mapa(lambda m: m["PB-22"].__setitem__("comprueba", None)))
caso("mapa: PARCIAL sin decir qué falta", MAPA, mapa(lambda m: m["PB-02"].__setitem__("no_comprueba", "")))
caso("mapa: una PARCIAL pasa a AUTOMATICA sin tocar nada más (PB-17)", MAPA, mapa(lambda m: m["PB-17"].__setitem__("cobertura", "AUTOMATICA")), espera_fallo=False)
caso("mapa: PENDIENTE_API pasa a AUTOMATICA citando una prueba cualquiera (PB-04)", MAPA,
     mapa(lambda m: m["PB-04"].update(cobertura="AUTOMATICA", pruebas=["11_Ejecutor/tests/test_unitarias.py::test_almacen_reserva_integridad_y_as_of"],
                                      comprueba="x", no_comprueba="")), espera_fallo=False)
caso("plan: una PB-68 de más, bien escrita", PLAN, lambda t: t + "\n### PB-68 · Nueva prueba\n\n| Campo | Contenido |\n|---|---|\n| Tipo | INT |\n| Criterio de aprobación | x |\n")
caso("plan: una PB-68 de más con guion en vez de «·»", PLAN, lambda t: t + "\n### PB-68 - Nueva prueba\n\n| Campo | Contenido |\n|---|---|\n| Criterio de aprobación | x |\n")
caso("plan: una PB-100 de más (tres cifras)", PLAN, lambda t: t + "\n### PB-100 · Nueva prueba\n\n| Campo | Contenido |\n|---|---|\n| Criterio de aprobación | x |\n")
caso("plan: PB-22 sin criterio de aprobación", PLAN, lambda t: t.replace("| Criterio de aprobación | Tres INC- tipo CANAL_NO_PREVISTO; cero efectos en archivos |\n", ""))
caso("plan: PB-22 renombrada a PB-2X", PLAN, lambda t: t.replace("### PB-22 · Canal no previsto", "### PB-2X · Canal no previsto"))

FIRMA = "def test_pb22_tres_mensajes_por_canales_no_previstos_tres_incidencias_y_ningun_efecto(tmp_path):\n"
ve = lambda todo: "; ".join(x.strip()[:95] for x in todo.splitlines() if "test_pb22" in x or x.startswith("PB-22"))  # noqa: E731
caso("prueba citada que FALLA", HUECOS, lambda t: t.replace(FIRMA, FIRMA + "    assert False, 'QA'\n"), ("--pb", "PB-22"), tambien=ve)
caso("prueba citada SALTADA (skip)", HUECOS, lambda t: t.replace(FIRMA, "@pytest.mark.skip(reason='QA')\n" + FIRMA), ("--pb", "PB-22"), tambien=ve)
caso("prueba citada xfail que falla", HUECOS, lambda t: t.replace(FIRMA, "@pytest.mark.xfail\n" + FIRMA + "    assert False\n"), ("--pb", "PB-22"), tambien=ve)
caso("prueba citada xfail que pasa (XPASS)", HUECOS, lambda t: t.replace(FIRMA, "@pytest.mark.xfail\n" + FIRMA), ("--pb", "PB-22"), tambien=ve)
caso("prueba citada con error en la fixture", HUECOS, lambda t: t.replace(FIRMA, FIRMA.replace("(tmp_path)", "(tmp_path, no_hay_fixture)")), ("--pb", "PB-22"), tambien=ve)
caso("fichero de pruebas con error de sintaxis", HUECOS, lambda t: t + "\ndef roto(:\n", ("--pb", "PB-22"))
caso("prueba citada vaciada (solo `pass`)", HUECOS, lambda t: t.replace(FIRMA, FIRMA + "    return\n"), ("--pb", "PB-22"), espera_fallo=False, tambien=ve)
rc, ult, _ = correr("--pb", "PB-04")
print(f"rc={rc} · --pb de una fila sin pruebas (PB-04) · {ult}")
rc, ult, _ = correr("--pb", "PB-99")
print(f"rc={rc} · --pb de una fila que no existe · {ult}")
rc, ult, _ = correr("--pb", "PB-22", "--ejecutar")
print(f"rc={rc} · --pb y --ejecutar a la vez · {ult} · ¿se escribió el documento? {'sí' if DOC.read_bytes() != (copia / 'docs/evidencias_pruebas_bloque_a.md').read_bytes() else 'no cambia'}")
