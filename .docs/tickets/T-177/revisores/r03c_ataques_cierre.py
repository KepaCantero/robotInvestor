"""QA de T-177 · verificación de la ronda de cierre de la r03 (H-14 a H-17): ataques a cada corrección.

Ejecutar desde bloque_a/11_Ejecutor:
  python -m pytest -q -s -p no:cacheprovider ../../.docs/tickets/T-177/revisores/r03c_ataques_cierre.py
Secretos ficticios partidos en dos cadenas. Los casos «HALLAZGO_*» fijan lo observado; al corregirlos se invierten."""
import importlib
import json
import sys
from pathlib import Path

import pytest

EJ = Path(__file__).resolve().parents[4] / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJ / "tests"))
from conftest import AS_OF, config_pruebas, nuevo_bloque, universo  # noqa: E402,F401

from bloque_a.llm import MockClient, ReplayClient, solicitud_con_valor  # noqa: E402

mc4 = importlib.import_module("bloque_a.mantenimiento_c4")
mock_respuestas = importlib.import_module("bloque_a.mock_respuestas")
FICHA = {"servicio": "API de fondos cerrados", "uso_previsto": "Cribado de FON", "impacto_si_falta": "Datos públicos"}
SOL = {"servicio": FICHA["servicio"], "motivo": "Cribado semanal", "impacto_si_falta": "Datos públicos"}
CORTO = "Hunt" + "er2x!"          # secreto corto y no opaco: solo una clave lo delata


def _aparece(tmp, valor):
    return sorted(str(p.relative_to(tmp)) for p in Path(tmp).rglob("*")
                  if p.is_file() and p.name != "secretos.json" and valor in p.read_text(encoding="utf-8", errors="ignore"))


def _c4(tmp, universo, monkeypatch, sol):
    monkeypatch.setattr(mock_respuestas, "_mantenimiento_c4",
                        lambda msg: {"referencias": [], "sintesis": "s", "lagunas": [], "solicitudes_credenciales": sol})
    b = nuevo_bloque(tmp, universo, cliente=ReplayClient(Path(tmp) / "cinta.jsonl", "grabar", MockClient()),
                     cfg=config_pruebas(credenciales={"servicios_bfa": [FICHA]}))
    return b, mc4.mantenimiento_c4(b, AS_OF)


# ---- H-17: campos admitidos que el Coordinador NO copia ------------------------------------------------------------------
NO_COPIADOS = {
    "urgencia_no_enum": [{**SOL, "urgencia": CORTO}],                        # desde_retorno la reduce a NORMAL
    "impacto_junto_a_impacto_si_falta": [{**SOL, "impacto": CORTO}],         # se lee impacto_si_falta; impacto se ignora
    "clave_duplicada_por_normalizacion": [{**SOL, "Servicio": CORTO}],       # se lee «servicio»; «Servicio» se ignora
}


@pytest.mark.parametrize("nombre", sorted(NO_COPIADOS))
def test_r03c_HALLAZGO_H18_campo_admitido_que_no_se_copia(tmp_path, universo, monkeypatch, nombre):
    b, r = _c4(tmp_path, universo, monkeypatch, NO_COPIADOS[nombre])
    donde = _aparece(tmp_path, CORTO)
    print(nombre, r["estado_retorno"], [s["resultado"] for s in r["solicitudes"]], donde)
    assert r["estado_retorno"] == "SIN_RESULTADO" and donde == []   # segunda ronda de cierre (invertida): H-18


# Lo que H-17 sí para (variantes de claves raras y anidadas)
PARADAS = {
    "clave_rara_anidada": [{**SOL, "detalle": {"x": CORTO}}],
    "clave_con_espacio_de_anchura_cero_no_admitida": [{**SOL, "pass​word": CORTO}],
    "lista_en_campo_no_admitido": [{**SOL, "extra": [CORTO]}],
    "booleano_de_mas": [{**SOL, "flag": True, "nota": CORTO}],
}


@pytest.mark.parametrize("nombre", sorted(PARADAS))
def test_r03c_h17_paradas(tmp_path, universo, monkeypatch, nombre):
    b, r = _c4(tmp_path, universo, monkeypatch, PARADAS[nombre])
    assert r["estado_retorno"] == "SIN_RESULTADO" and _aparece(tmp_path, CORTO) == []


def test_r03c_h17_nominal_y_variantes_legitimas_pasan(tmp_path, universo, monkeypatch):
    b, r = _c4(tmp_path, universo, monkeypatch, [{**SOL, "urgencia": "ALTA"}])
    assert r["estado_retorno"] == "COMPLETO" and r["solicitudes"][0]["resultado"] == "SOLICITADA"


# ---- H-14: variantes del texto ilegible ----------------------------------------------------------------------------------
@pytest.mark.parametrize("clave", ["solicitudes\\u005Fcredenciales", "solicitudes\\u005fcredenci\\u0061les",
                                   "solicitudes\\/credenciales", "Solicitudes Credenciales"])
def test_r03c_h14_ilegible_variantes(clave):
    assert solicitud_con_valor('{"' + clave + '": [{"servicio": "x"}] ,,, }')


def test_r03c_h14_sin_falso_positivo_en_ilegible_corriente():
    assert not solicitud_con_valor('{"sintesis": "texto con \\u00e9 y sin el campo" ,,, }')


# ---- H-15: identificadores públicos ---------------------------------------------------------------------------------------
def test_r03c_h15_limites():
    dir40 = "0x" + "c0ffee12" * 5
    casos = {
        "dir_0x_con_coma": ({"token": dir40 + ",", "solicitudes_credenciales": []}, False),
        "dir_0x_mayusculas": ({"token": dir40.upper().replace("0X", "0x"), "solicitudes_credenciales": []}, False),
        "dir_0x_41": ({"token": dir40 + "a", "solicitudes_credenciales": []}, True),
        "dir_0x_en_url": ({"token": "https://etherscan.io/token/" + dir40, "solicitudes_credenciales": []}, True),
        "lei_minusculas": ({"clave": "5493001kjtiigc8y1r12", "solicitudes_credenciales": []}, True),
        "lei_y_secreto": ({"clave": "5493001KJTIIGC8Y1R12 QaR03Fict" + "icio55TtUu", "solicitudes_credenciales": []}, True),
    }
    res = {n: solicitud_con_valor(json.dumps(d)) for n, (d, _) in casos.items()}
    print(res)
    assert all(res[n] is esp for n, (_, esp) in casos.items())


# ---- H-16: reservas manipuladas -------------------------------------------------------------------------------------------
@pytest.mark.parametrize("pid", [None, "123", -5, True, 2 ** 22 + 54321])
def test_r03c_h16_pid_manipulado(tmp_path, universo, pid):
    b = nuevo_bloque(tmp_path, universo, cfg=config_pruebas(credenciales={"servicios_bfa": [FICHA]}))
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "C4_CREDENCIALES", "id": "C4-2026-9990", "agente": "AG-16",
                                        "fecha": AS_OF, "estado_retorno": "EN_CURSO", "uc": 3.0, "pid": pid})
    r = mc4.mantenimiento_c4(b, AS_OF)
    avisos = [e for e in b.almacen.leer("HA") if e.get("reserva_huerfana")]
    print(repr(pid), r["estado_retorno"], r["reservas_en_curso"], len(avisos))
    assert r["estado_retorno"] == "SIN_PRESUPUESTO" and r["reservas_en_curso"] == ["C4-2026-9990"]
    assert len(avisos) == (1 if pid == 2 ** 22 + 54321 else 0)   # sin pid válido no se sabe: no se avisa (None)


def test_r03c_h16_aviso_una_vez_entre_dias_y_fuera_de_ventana(tmp_path, universo):
    import pandas as pd
    b = nuevo_bloque(tmp_path, universo, cfg=config_pruebas(credenciales={"servicios_bfa": [FICHA]}))
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "C4_CREDENCIALES", "id": "C4-2026-9991", "agente": "AG-16",
                                        "fecha": AS_OF, "estado_retorno": "EN_CURSO", "uc": 3.0, "pid": 2 ** 22 + 54322})
    d = [str((pd.Timestamp(AS_OF) + pd.Timedelta(days=k)).date()) for k in (0, 3, 6, 7)]
    rs = [mc4.mantenimiento_c4(b, x) for x in d]
    avisos = [e for e in b.almacen.leer("HA") if e.get("reserva_huerfana")]
    print([r["estado_retorno"] for r in rs], len(avisos), avisos[0]["detalle"] if avisos else None)
    assert [r["estado_retorno"] for r in rs[:3]] == ["SIN_PRESUPUESTO"] * 3 and rs[3]["estado_retorno"] == "COMPLETO"
    assert len(avisos) == 1 and d[3] in avisos[0]["detalle"]
