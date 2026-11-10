"""T-83, corrección de la QA r01: cada hallazgo (H-01 a H-06) evaluado contra `parametros_doc.py` de un commit (por defecto
HEAD) y contra el del árbol de trabajo. Con HEAD cada hallazgo debe salir FALLA y con el árbol, OK: es la prueba de que la
regresión correspondiente de `pruebas_parametros_doc_t83.py` falla sin la corrección (la batería entera no arranca con el
módulo de HEAD, porque usa la API nueva: subtablas, valor documentado, desfasados()).

Uso (desde la raíz del repo): .venv/bin/python -I .docs/tickets/T-83/r02_contra_head.py [commit]
"""
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
VALIDADOR = REPO / "sistema_global" / "marco_comun_c" / "validador"
COMMIT = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
sys.path.insert(0, str(VALIDADOR))
from control_f import POLITICA_DEFECTO  # noqa: E402
from orquestador import CONFIG_DEFECTO  # noqa: E402
from parametros import PARAMETROS, como_dict  # noqa: E402

TABLAS = {"PARAMETROS": PARAMETROS, "CONFIG_DEFECTO": CONFIG_DEFECTO, "POLITICA_DEFECTO": POLITICA_DEFECTO}


def copia():
    return {t: json.loads(json.dumps(como_dict(v) if t == "PARAMETROS" else v, default=list)) for t, v in TABLAS.items()}


def cargar(ruta, nombre):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def evaluar(m):
    def prueba(fn):
        try:
            return bool(fn())
        except Exception:   # noqa: BLE001  con la API antigua, lo que lanza no está corregido
            return False

    def h01():
        r = m.doc("apalancamiento_max", "POLITICA_DEFECTO")
        return r["estado"] == "RATIFICADO" and "Constitución D-16" in r["fuente"] and r["pregunta"] is None

    def h02():
        sub = m.DOC["CONFIG_DEFECTO.aprobacion"]
        otra = copia()
        otra["CONFIG_DEFECTO"]["aprobacion"]["x_t83_tope_eur"] = 1.0
        return (set(sub) == set(CONFIG_DEFECTO["aprobacion"]) and all(v["pregunta"] for v in sub.values())
                and m.DOC["CONFIG_DEFECTO.mandatos"]["instrumentos_permitidos"]["pregunta"]
                and ("CONFIG_DEFECTO.aprobacion", "x_t83_tope_eur", "SIN_DOCUMENTAR") in m.faltan(otra))

    def h03():
        return "no se prohíbe" in m.doc("horario_utc", "CONFIG_DEFECTO.aprobacion")["justificacion"]

    def h04():
        return ("como máximo" in m.doc("revision_max_dias")["pregunta"] and m.doc("rangos_tipo_cambio_eur")["pregunta"].startswith("¿Te vale")
                and "marcador" in m.doc("rentabilidad_anual_pct", "CONFIG_DEFECTO.referencias")["justificacion"])

    def h05():
        otra = copia()
        otra["PARAMETROS"]["k_min_observaciones"] = 40
        return m.desfasados() == [] and ("PARAMETROS", "k_min_observaciones") in m.desfasados(otra)

    def h06():
        otra = {t: dict(v) for t, v in TABLAS.items()}
        del otra["POLITICA_DEFECTO"]["valor_min_eur"]
        try:
            m.preguntas_pendientes(otra)
        except ValueError:
            pass
        else:
            return False
        try:
            m.preguntas_pendientes({})
        except ValueError:
            return True
        return False

    return {n: prueba(f) for n, f in (("H-01", h01), ("H-02", h02), ("H-03", h03), ("H-04", h04), ("H-05", h05), ("H-06", h06))}


with tempfile.TemporaryDirectory() as td:
    viejo = Path(td) / "parametros_doc_viejo.py"
    viejo.write_bytes(subprocess.run(["git", "-C", str(REPO), "show", f"{COMMIT}:sistema_global/marco_comun_c/validador/parametros_doc.py"],
                                     capture_output=True, check=True).stdout)
    resultados = {COMMIT: evaluar(cargar(viejo, "parametros_doc_viejo")),
                  "árbol": evaluar(cargar(VALIDADOR / "parametros_doc.py", "parametros_doc_arbol"))}
bien = True
for h in ("H-01", "H-02", "H-03", "H-04", "H-05", "H-06"):
    antes, ahora = resultados[COMMIT][h], resultados["árbol"][h]
    bien &= (not antes) and ahora
    print(f"{h}: {COMMIT} {'OK   ' if antes else 'FALLA'} · árbol {'OK   ' if ahora else 'FALLA'}")
print("RESULTADO r02 CONTRA", COMMIT + ":", "CADA HALLAZGO FALLA ANTES Y PASA AHORA" if bien else "HAY DIFERENCIAS")
sys.exit(0 if bien else 1)
