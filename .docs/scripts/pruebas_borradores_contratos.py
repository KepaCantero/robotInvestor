"""Pruebas de los borradores de esquema de `.docs/diseno/contratos/` (CT-G-08 0.4.0 y CT-G-24 0.1.0, 12-11-2026).

Los ejemplos de CT-G-08 salen de un informe real de F del marco común (0.3.0) al que se añade el tipo de acción; los de CT-G-24,
del propio registro de experimentos (T-99). Uso: .venv/bin/python -m pytest -q .docs/scripts/pruebas_borradores_contratos.py
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

import jsonschema
import pytest

RAIZ = Path(__file__).resolve().parents[2]
CONTRATOS = RAIZ / ".docs" / "diseno" / "contratos"
MARCO = RAIZ / "sistema_global" / "marco_comun_c"
sys.path[:0] = [str(MARCO / "validador"), str(MARCO / "pruebas"), str(Path(__file__).resolve().parent)]
from control_f import POLITICA_DEFECTO, construir_informe  # noqa: E402
from pruebas_control_f import AHORA_F, CART, solicitud  # noqa: E402
from pruebas_control_f_t22 import CTX  # noqa: E402
import registro_experimentos as rx  # noqa: E402

CT08 = json.loads((CONTRATOS / "ct-g-08_0.4.0-borrador.schema.json").read_text(encoding="utf-8"))
CT24 = json.loads((CONTRATOS / "ct-g-24_0.1.0-borrador.schema.json").read_text(encoding="utf-8"))
HASH = "a" * 64


def valida(esquema, x):
    return not list(jsonschema.Draft202012Validator(esquema).iter_errors(x))


def informe(tipo="ABRIR_O_AUMENTAR", **cambios):
    inf = construir_informe("EV-F-0001", "EXP-0001", "COR-0001", {"p": 1}, solicitud(), CART, POLITICA_DEFECTO, AHORA_F,
                            "2026-11-06T12:00:00+00:00", CTX)
    inf["version_esquema"] = "0.4.0"
    inf["payload"]["tipo_accion"] = tipo
    inf["payload"]["deduccion"] = {"posicion_conciliada": {"foto_ref": HASH, "cantidad": 0.0, "direccion": "SIN_POSICION"},
                                   "cantidad_solicitada": 100.0, "sentido_solicitado": "COMPRA",
                                   "criterio": "sin posición conciliada en el instrumento: la compra abre riesgo"}
    for ruta, v in cambios.items():
        d = inf
        *pre, ult = ruta.split("__")
        for k in pre:
            d = d[k]
        d[ult] = v
    return inf


def test_los_borradores_son_los_que_genera_el_script():
    r = subprocess.run([sys.executable, "-I", str(CONTRATOS / "generar_borradores.py"), "--comprobar"], capture_output=True, text=True, check=False)
    assert r.returncode == 0, r.stdout + r.stderr


def test_ct08_los_esquemas_son_validos():
    jsonschema.Draft202012Validator.check_schema(CT08)
    jsonschema.Draft202012Validator.check_schema(CT24)


def test_ct08_un_informe_real_con_tipo_de_accion_valida():
    inf = informe()
    assert inf["resultado_politica"]["resultado"] == "APROBADO" and valida(CT08, inf)


@pytest.mark.parametrize("nombre,mutar", [
    ("sin_tipo", lambda i: i["payload"].pop("tipo_accion")),
    ("tipo_inventado", lambda i: i["payload"].update(tipo_accion="VENDER_TODO")),
    ("sin_deduccion", lambda i: i["payload"].pop("deduccion")),
    ("version_vieja", lambda i: i.update(version_esquema="0.3.0")),
    ("posicion_mal_formada", lambda i: i["payload"]["deduccion"]["posicion_conciliada"].update(direccion="ALGO")),
    ("cantidad_solicitada_cero", lambda i: i["payload"]["deduccion"].update(cantidad_solicitada=0)),
])
def test_ct08_informes_mal_formados(nombre, mutar):
    inf = informe()
    mutar(inf)
    assert not valida(CT08, inf), nombre


def _vetado(inf, regla):
    inf["resultado_politica"]["resultado"] = "VETADO"
    inf["resultado_politica"]["controles"].append({"regla": regla, "resultado": "VETA", "valor": 1, "limite": 0, "motivo": "x"})
    inf["payload"]["cantidad_aprobada"] = 0.0
    return inf


def test_ct08_reducir_aprobado_o_vetado_por_forma_valida():
    assert valida(CT08, informe("REDUCIR_O_CERRAR"))
    assert valida(CT08, _vetado(informe("REDUCIR_O_CERRAR"), "F-24"))   # vender más de lo que se tiene
    assert valida(CT08, _vetado(informe("PROTEGER"), "F-01"))


@pytest.mark.parametrize("regla", ["F-08", "F-16", "F-17", "F-21"])   # pérdida del día, de la semana, frecuencia, ventanas
def test_ct08_reducir_o_proteger_no_se_vetan_por_perdidas_frecuencia_ni_eventos(regla):
    assert not valida(CT08, _vetado(informe("REDUCIR_O_CERRAR"), regla))
    assert not valida(CT08, _vetado(informe("PROTEGER"), regla))


def test_ct08_reducir_no_puede_salir_reducido():
    inf = informe("REDUCIR_O_CERRAR")
    inf["resultado_politica"]["resultado"] = "REDUCIDO"
    assert not valida(CT08, inf)


def test_ct08_abrir_si_se_puede_vetar_por_perdidas():
    assert valida(CT08, _vetado(informe("ABRIR_O_AUMENTAR"), "F-08"))


def test_ct24_todo_lo_que_escribe_el_registro_valida(tmp_path):
    r = rx.Registro(tmp_path / "r.jsonl")
    pre = {"hipotesis": "El recorte del Director no empeora la calidad", "objeto": "RECORTE", "metrica": "exceso frente a la cesta",
           "datos": "backtest simulado", "desde": "2026-03-06", "hasta": "2026-05-29", "semilla": 7,
           "criterio_exito": "rango del 90 % por encima de cero", "max_variantes": 2}
    exp = r.prerregistrar(pre, "claude")["exp_id"]
    for v, ver in (("v1", "peor"), ("v2", "fallido"), ("v3", "mejor")):
        n = r.intento(exp, v)["n"]
        r.resultado(exp, n, ver, {"nota": "prueba"})
    lineas = [json.loads(x) for x in (tmp_path / "r.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len(lineas) == 7 and all(valida(CT24, x) for x in lineas)


@pytest.mark.parametrize("nombre,mutar", [
    ("tipo_desconocido", lambda e: e.update(tipo="BORRADO")),
    ("veredicto_inventado", lambda e: e.update(veredicto="casi") if e["tipo"] == "RESULTADO" else e.update(tipo="X")),
    ("sin_huella", lambda e: e.pop("_hash")),
    ("exp_id_mal_formado", lambda e: e.update(exp_id="EXP-26-1")),
])
def test_ct24_anotaciones_mal_formadas(tmp_path, nombre, mutar):
    r = rx.Registro(tmp_path / "r.jsonl")
    exp = r.prerregistrar({"hipotesis": "Cambiar el modelo del Analizador ahorra coste", "objeto": "MODELO", "metrica": "coste por selección",
                           "datos": "x", "desde": "2026-01-01", "hasta": "2026-02-01", "semilla": 1,
                           "criterio_exito": "coste menor sin peor calidad", "max_variantes": 1}, "claude")["exp_id"]
    r.intento(exp, "v1")
    r.resultado(exp, 1, "peor")
    e = copy.deepcopy(json.loads((tmp_path / "r.jsonl").read_text(encoding="utf-8").splitlines()[-1]))
    mutar(e)
    assert not valida(CT24, e), nombre


def test_ct24_prerregistro_con_max_variantes_cero_no_valida(tmp_path):
    r = rx.Registro(tmp_path / "r.jsonl")
    r.prerregistrar({"hipotesis": "Cambiar el modelo del Analizador ahorra coste", "objeto": "MODELO", "metrica": "coste por selección",
                     "datos": "x", "desde": "2026-01-01", "hasta": "2026-02-01", "semilla": 1,
                     "criterio_exito": "coste menor sin peor calidad", "max_variantes": 1}, "claude")
    e = json.loads((tmp_path / "r.jsonl").read_text(encoding="utf-8"))
    e["contenido"]["max_variantes"] = 0
    assert not valida(CT24, e)
