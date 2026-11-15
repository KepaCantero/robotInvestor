"""T-116 · Ronda r05: cláusulas del Plan de pruebas que la QA r04 (`.docs/tickets/T-116/qa.md`) encontró sin afirmar (H-10) y
la marca de escalado al operador (H-12).

- PB-31: la banda verbal publicada de cada horizonte es la de su probabilidad interna, y la de 0,65 es «más probable que no»
  con «sin ventaja demostrada todavía», en el JSON, en el técnico y en el visual (M31 de `r04_01`).
- PB-37: el Evaluador resuelve los dos pronósticos, el original corregido en su fecha y la corrección en la suya (M37a, M37b).
- PB-22 / H-12: las incidencias marcadas `escalado_operador` se ven en el estado que consulta el operador.
"""
import json
import re
from pathlib import Path

import pytest
from bloque_a.contratos import CanalNoPrevisto
from bloque_a.evaluador import banda_publicable
from conftest import AS_OF, nuevo_bloque

ETIQUETA = "sin ventaja demostrada todavía"


# ---------------------------------------------------------------- PB-31 · la banda sigue a la probabilidad interna
@pytest.fixture(scope="module")
def ciclo_rv(tmp_path_factory, universo):
    b = nuevo_bloque(tmp_path_factory.mktemp("pb31"), universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    return b, r


def test_pb31_la_banda_de_cada_horizonte_publicado_es_la_de_su_probabilidad_interna(ciclo_rv):
    b, r = ciclo_rv
    assert not b.evaluador.certificados_vigentes(AS_OF)
    js = json.loads(Path(r["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
    f4 = b.almacen.estado("F4", AS_OF)
    vistas = [(h, v) for d in js["clases"].values() for o in d["opciones"] for h, v in o["horizontes"].items() if h != "H5"]
    assert vistas
    for h, v in vistas:
        p = f4[v["prg_id"]]["prob_interna"]
        assert v["banda"] == b.evaluador.banda_publicable(p) and v["prob"] is None and v["etiqueta"] == ETIQUETA, (h, v, p)
        assert f4[v["prg_id"]]["banda_verbal"] == b.evaluador.banda_de(p) and f4[v["prg_id"]]["prob_publicada"] is None
    bandas = {v["banda"] for _, v in vistas}
    assert "más probable que no" in bandas and len(bandas) >= 2                        # no todas «incierto»


def test_pb31_el_caso_del_plan_065_es_mas_probable_que_no_en_los_tres_entregables(ciclo_rv):
    """Preparación del plan: PRG H3 (o el horizonte que lo tenga) con probabilidad interna 0,65 y sin certificado."""
    b, r = ciclo_rv
    assert banda_publicable(0.65) == "más probable que no"
    js = json.loads(Path(r["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
    tecnico = Path(r["entregables"]["informe_tecnico"]).read_text(encoding="utf-8")
    visual = re.sub(r"<!--.*?-->", "", Path(r["entregables"]["informe_visual"]).read_text(encoding="utf-8"), flags=re.DOTALL)
    f4 = b.almacen.estado("F4", AS_OF)
    casos = [(o, h, v) for d in js["clases"].values() for o in d["opciones"] for h, v in o["horizontes"].items()
             if h != "H5" and f4[v["prg_id"]]["prob_interna"] == 0.65]
    assert casos
    for o, h, v in casos:
        assert v["banda"] == "más probable que no" and v["prob"] is None and v["etiqueta"] == ETIQUETA     # JSON
        assert re.search(rf"\| {h} \| {re.escape(v['vista'])} \| más probable que no \| {ETIQUETA} \|", tecnico), (o["opp_id"], h)   # técnico
    principales = [(o, o["horizontes"][o["horizonte_principal"]]) for o in (c[0] for c in casos)]
    for o, v in principales:
        if f4[v["prg_id"]]["prob_interna"] == 0.65:
            assert f"Más probable que no · {ETIQUETA}" in visual                         # visual (horizonte principal)
    assert any(f4[v["prg_id"]]["prob_interna"] == 0.65 for _, v in principales)


# ---------------------------------------------------------------- PB-37 · el Evaluador resuelve el original y su corrección
def _alta(b, pid, nivel, fecha_resolucion, **extra):
    b.almacen.escribir("F4", "AG-10", {
        "tipo_entrada": "ALTA", "prg_id": pid, "opp_id": "OPP-1", "clase": "RV", "horizonte": "H2", "estado": "ABIERTO",
        "prob_interna": 0.65, "sentido": "POSITIVO", "umbral": 0.0, "tipo_pronostico": "RELATIVO", "referencia_indice": "ACWI",
        "variable": {"serie_ht01": "SPY"}, "fecha_emision": "2026-04-03", "fecha_resolucion": fecha_resolucion,
        "nivel_referencia": {"valor": nivel, "fecha": "2026-04-03"}, "referencia_ingenua": {"valor_o_prob": 0.5}, "en_informe": True, **extra})


def test_pb37_adelantar_el_reloj_a_los_dos_vencimientos_resuelve_el_original_y_la_correccion(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha("2026-04-03")
    _, real = b.proveedor.valor_en("SPY", "2026-04-03")
    _alta(b, "PRG-2026-0901", round(real * 1.1, 4), "2026-05-01")                            # nivel de referencia mal transcrito
    f4 = tmp_path / "estado" / "F4_registro_pronosticos.jsonl"
    original = f4.read_bytes()
    _alta(b, "PRG-2026-0902", real, "2026-05-08", version_de="PRG-2026-0901")               # Prospectiva corrige: PRG nuevo
    b.fijar_fecha("2026-05-04")                                                            # primer vencimiento
    r1 = b.evaluador.resolver("2026-05-04", "RUN-2026-0001")
    assert [(x["prg_id"], x["estado"]) for x in r1] == [("PRG-2026-0901", "RESUELTO")]
    est = b.almacen.estado("F4")
    assert est["PRG-2026-0901"]["estado"] == "RESUELTO" and est["PRG-2026-0901"]["resolucion"]["fecha_dato_proxy"] <= "2026-05-01"
    assert est["PRG-2026-0902"]["estado"] == "ABIERTO"
    b.fijar_fecha("2026-05-11")                                                            # segundo vencimiento
    r2 = b.evaluador.resolver("2026-05-11", "RUN-2026-0002")
    assert [(x["prg_id"], x["estado"]) for x in r2] == [("PRG-2026-0902", "RESUELTO")]
    est = b.almacen.estado("F4")
    assert est["PRG-2026-0901"]["estado"] == est["PRG-2026-0902"]["estado"] == "RESUELTO"   # ambos RESUELTO
    assert est["PRG-2026-0901"]["nivel_referencia"]["valor"] == round(real * 1.1, 4)       # el original sin cambios
    assert f4.read_bytes().startswith(original) and b.almacen.verificar_integridad("F4")["F4"]   # hash de la entrada intacto
    assert {p["prg_id"] for p in b.evaluador.resueltos("2026-05-11")} == {"PRG-2026-0901", "PRG-2026-0902"}   # ambos en métricas
    assert sum(v["n"] for v in b.evaluador.metricas("2026-05-11").values()) == 2


# ---------------------------------------------------------------- H-12 · lo escalado se ve en el estado del operador
def test_h12_las_incidencias_escaladas_se_ven_en_el_estado_del_operador(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    assert b.estado()["incidencias_escaladas"] == []
    for contrato, emisor, receptor in [("CT-17", "AG-19", "AG-02"), ("CT-02", "AG-17", "BROKER")]:
        with pytest.raises(CanalNoPrevisto):
            b.mensajeria.crear(contrato, emisor, receptor, {}, run_id="RUN-2026-0001",
                               tipo_mensaje="RETORNO" if contrato == "CT-02" else "ENCARGO")
    b.almacen.incidencia("DATOS", "una incidencia que no se escala", "AG-20", severidad="Menor")
    esc = b.estado()["incidencias_escaladas"]
    assert [(e["tipo"], e["objeto"]) for e in esc] == [("CANAL_NO_PREVISTO", "AG-19"), ("CANAL_NO_PREVISTO", "AG-17")]
    assert all(e["id"].startswith("INC-") and e["fecha"] == AS_OF and "no previsto" in e["detalle"] for e in esc)


def test_h12_la_orden_estado_las_muestra(tmp_path, universo, capsys):
    from bloque_a.cli import main as cli_main
    from conftest import DATOS
    sal = tmp_path / "sal"
    b = nuevo_bloque(sal, universo)
    b.fijar_fecha(AS_OF)
    with pytest.raises(CanalNoPrevisto):
        b.mensajeria.crear("CT-17", "AG-19", "AG-02", {}, run_id="RUN-2026-0001")
    capsys.readouterr()
    assert cli_main(["--datos", str(DATOS), "--estado", str(sal / "estado"), "--salida", str(sal), "estado"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert [e["tipo"] for e in out["incidencias_escaladas"]] == ["CANAL_NO_PREVISTO"]
