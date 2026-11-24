"""QA r01 (Claude): mutantes propios de T-189 y T-191. Uso: python r01_mutantes.py T-189|T-191 (desde la raíz del worktree, con la venv).
Cada mutante vive en una copia temporal de bloque_a; «VIVO» = ninguna prueba del ticket lo mata."""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

raiz = Path(__file__).resolve().parents[4]
ej = Path("bloque_a/11_Ejecutor")
MUT = {
    "T-189": (["tests/test_t189_controles.py", "tests/test_fase4_huecos.py::test_pb10_la_configuracion_rechazada_en_parte_no_toca_nada_mas",
               "tests/test_fase4_huecos.py::test_pb17_ampliacion_autorizada_y_denegada_dejan_su_aut_en_ha",
               "tests/test_fase4_huecos.py::test_pb17_en_un_ciclo_la_ampliacion_denegada_cierra_con_alcance_reducido",
               "tests/test_fase4_huecos.py::test_pb21_un_ct04_con_una_clave_y_un_iban_se_rechaza_y_no_queda_en_ningun_archivo"], [
        ("EV incluye la fase en curso", "bloque_a/consumo.py", "terminadas = self.fases_servidas[bolsa] - {fase}", "terminadas = self.fases_servidas[bolsa]"),
        ("EV sin BAC", "bloque_a/consumo.py", "ev = bac * sum(", "ev = sum("),
        ("EV sin pesos (todas las fases)", "bloque_a/consumo.py", "if nombre in terminadas)", "if True)"),
        ("BAC = 1", "bloque_a/consumo.py", "bac = self._base(bolsa)", "bac = 1.0"),
        ("nunca registra fases servidas", "bloque_a/orquestacion.py", "presupuesto.registrar_fase_servida(bolsa, fase)", "pass"),
        ("horizontes vacíos admitidos", "bloque_a/orquestacion.py", "if not isinstance(v, list) or not v:\n                    rechazos.append({\"parametro\": k, \"motivo\": \"se necesita una lista de horizontes\"})\n                    continue\n                no =",
         "if False:\n                    continue\n                no ="),
        ("clave como nombre de campo sin ocultar", "bloque_a/contratos.py", "campo_afectado=[k if not contiene_credenciales(k) else \"campo_protegido\" for k in campos]", "campo_afectado=campos"),
        ("tarjeta como clave", "bloque_a/contratos.py", 'tipos.add("TARJETA")', 'tipos.add("CLAVE_API")'),
        ("DNI como clave", "bloque_a/contratos.py", 'tipos.add("IDENTIFICACION_PERSONAL")', 'tipos.add("CLAVE_API")'),
        ("correo como clave", "bloque_a/contratos.py", 'tipos.add("CORREO")', 'tipos.add("CLAVE_API")'),
    ]),
    "T-191": (["tests/test_t191_degradado.py", "tests/test_t159_extremo_a_extremo.py::test_pb52_con_ht09_caido_nunca_hay_apto_por_defecto_ni_entrega"], [
        ("sin incidencia HERRAMIENTA", "bloque_a/sintesis.py", "            bloque.almacen.incidencia(\"HERRAMIENTA\", detalle, run_id, fase=fase, msg_id=aviso[\"msg_id\"])\n", ""),
        ("captura cualquier excepción", "bloque_a/sintesis.py", "except (RuntimeError, OSError, ValueError, KeyError, TypeError):", "except Exception:"),
        ("fase mal atribuida", "bloque_a/sintesis.py", 'fase = "F7" if visual is not None else "F6"', 'fase = "F6"'),
        ("sin limitación en el paquete", "bloque_a/orquestacion.py", '                paquete.setdefault("limitaciones", []).append(res["motivo"])\n', ""),
        ("G3V F6 sin dictamen NO_DISPONIBLE", "bloque_a/orquestacion.py", 'g3v.update(tipo_control="G3_MANUAL", dictamen_ht09="NO_DISPONIBLE")', 'g3v.update(tipo_control="G3_MANUAL")'),
        ("G3V F7 con el dictamen de la herramienta", "bloque_a/redaccion.py", '"dictamen_ht09": "NO_DISPONIBLE" if res.get("modo") else res["dictamen"]', '"dictamen_ht09": res["dictamen"]'),
        ("G3V F7 sin etiqueta", "bloque_a/redaccion.py", '"tipo_control": res.get("modo", "SINCRONO_DETERMINISTA")', '"tipo_control": "SINCRONO_DETERMINISTA"'),
        ("CT-14 sin la fase", "bloque_a/sintesis.py", '"resultado_ht09": {"dictamen": "NO_DISPONIBLE", "fase": fase}', '"resultado_ht09": {"dictamen": "NO_DISPONIBLE"}'),
    ]),
}
pruebas, mutaciones = MUT[sys.argv[1]]


def correr(carpeta):
    return subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *pruebas], cwd=carpeta / ej, text=True,
                          capture_output=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})


with tempfile.TemporaryDirectory() as tmp:
    copia = Path(tmp)
    shutil.copytree(raiz / "bloque_a", copia / "bloque_a", ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    base = correr(copia)
    if base.returncode:
        raise SystemExit(base.stdout[-2000:] + base.stderr[-2000:])
    for nombre, ruta, antes, despues in mutaciones:
        archivo = copia / ej / ruta
        original = archivo.read_text()
        if original.count(antes) != 1:
            print("NO APLICA", nombre, original.count(antes)); continue
        archivo.write_text(original.replace(antes, despues))
        res = correr(copia)
        archivo.write_text(original)
        print(("MUERTO " if res.returncode == 1 and " failed" in res.stdout else "VIVO   ") + nombre, flush=True)
