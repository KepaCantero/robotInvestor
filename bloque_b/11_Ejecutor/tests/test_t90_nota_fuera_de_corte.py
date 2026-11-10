"""T-90 (QA de T-64, H-01): una nota de un especialista con fechas de fuente posteriores al corte se excluye y se declara."""
import json
from pathlib import Path

from bloque_b import mock_respuestas as mr
from bloque_b.orquestacion import Coordinador
from conftest import peticion_redes


def _informe_con_fuga(msg, ctx, r):
    out = mr._informe_dimensional(msg, ctx, r)
    inf = out["dim_informes"][0]
    inf["notas"].append({"afirmacion": "Un dato que solo se conoció después del corte.", "etiqueta": "[INTERPRETACIÓN]",
                         "contiene_cifra": False, "fechas": {"fecha_fenomeno": "2099-01-01", "fecha_publicacion": "2099-01-02",
                                                             "conocible_desde": "2099-01-02"}})
    return out


def test_nota_posterior_al_corte_se_excluye_y_se_declara(hacer_entorno, rapido, monkeypatch):
    monkeypatch.setitem(mr._TAREAS, ("*", "informe_dimensional"), _informe_con_fuga)
    ent = hacer_entorno(rapido)
    res = Coordinador(ent).recibir(peticion_redes())
    assert res["estado_peticion"] == "ENTREGADA", res
    p = json.loads(Path(res["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
    claims = [e for e in ent.alm.leer("F2") if e.get("tipo_entrada") == "CLM"]
    assert not any("después del corte" in c["afirmacion"] for c in claims)      # no entra en el expediente ni en el informe
    assert not any("después del corte" in n["afirmacion"] for d in p["dimensiones"] for n in d["notas"])
    assert any("1 nota(s)" in x and "excluida(s) por fechas de fuente posteriores al corte" in x for x in p["estados_degradados"]), p["estados_degradados"]


def _informe_con_fechas_raras(msg, ctx, r):
    out = mr._informe_dimensional(msg, ctx, r)
    inf = out["dim_informes"][0]
    for k in range(2):   # dos notas del mismo especialista con fechas incompletas (la instrucción dice «omite lo desconocido»)
        inf["notas"].append({"afirmacion": f"Una nota con fechas incompletas {k}.", "etiqueta": "[INTERPRETACIÓN]", "contiene_cifra": False,
                             "fechas": {"fecha_publicacion": "2025-01-02"}})
    return out


def test_fechas_incompletas_no_se_rotulan_como_fuga_y_se_cuentan(hacer_entorno, rapido, monkeypatch):
    """QA de T-90, H-01 y H-02: motivo propio para fechas incompletas, y cuántas notas se excluyeron."""
    monkeypatch.setitem(mr._TAREAS, ("*", "informe_dimensional"), _informe_con_fechas_raras)
    ent = hacer_entorno(rapido)
    res = Coordinador(ent).recibir(peticion_redes())
    p = json.loads(Path(res["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
    ed = [x for x in p["estados_degradados"] if "excluida(s)" in x]
    assert ed and all("2 nota(s)" in x and "incompletas, ilegibles o incoherentes" in x and "fuga" not in x for x in ed), ed   # una por dimensión
