"""Los cinco entregables: nombres y carpetas ENT, validación del paquete contra el esquema del Anexo B, G3 APTO en las
dos pasadas, legibilidad HT-07 ≥ 70, anexo XLSX, registros F1–F6 y RC; y entrega de cada ámbito de ejemplo (12 tipos)."""
import json
import re
from pathlib import Path

import jsonschema
import openpyxl
import pytest

from bloque_b.configuracion import TIPOS_ACTIVO, cargar_ambitos, cargar_config
from bloque_b.herramientas import ht07, ht09, ht11
from bloque_b.orquestacion import Coordinador
from bloque_b.sintesis import esquema_paquete

from conftest import AS_OF, peticion_ambito

CARPETAS = {"informe_tecnico": "Informes técnicos Broker", "informe_visual": "Informes visuales Usuario",
            "paquete_json": "Paquetes JSON", "memorando": "Memorandos ejecutivos", "anexo_datos": "Anexos de datos",
            "mapa_eslabones": "Mapas por eslabón"}


def test_seis_entregables_en_sus_carpetas(entrega_redes):
    res = entrega_redes["res"]
    assert set(res["entregables"]) == set(CARPETAS) | {"mapa_eslabones_json", "mapa_eslabones_docx"}
    for k, ruta in res["entregables"].items():
        p = Path(ruta)
        assert p.exists() and p.parent.name == CARPETAS[k.replace("mapa_eslabones_json", "mapa_eslabones").replace("mapa_eslabones_docx", "mapa_eslabones")]
        assert p.name.startswith(f"{AS_OF}_") and res["pet_id"] in p.name
    assert not (entrega_redes["ent"].salida / ".borradores" / res["pet_id"]).exists() or \
        not any((entrega_redes["ent"].salida / ".borradores" / res["pet_id"]).rglob("*.json"))
    assert res["autorizacion_salida"].startswith("AUTS-B-")


def test_paquete_valida_contra_el_esquema(entrega_redes):
    p = json.loads(Path(entrega_redes["res"]["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
    esq = esquema_paquete(entrega_redes["ent"].cfg)
    assert esq is not None
    jsonschema.Draft202012Validator(esq).validate(p)
    assert p["pet_id"] == entrega_redes["res"]["pet_id"]
    assert re.fullmatch(r"RUN-B-\d{4}-\d{4}-\d{2}", p["run_ids"][0])
    assert p["auditoria"]["autorizacion_salida"].startswith("AUTS-B-")


def test_g3_apto_en_las_dos_pasadas(entrega_redes):
    ent, res = entrega_redes["ent"], entrega_redes["res"]
    g3 = [e for e in ent.alm.leer("HA") if e.get("tipo_entrada") == "G3V" and e.get("pet_id") == res["pet_id"]]
    pasadas = {e["pasada"]: e["dictamen"] for e in g3}
    assert pasadas["PAQUETE_SINTESIS"] in ("APTO", "APTO_CON_ADVERTENCIAS")
    assert pasadas["FIDELIDAD_ENTREGABLES"] in ("APTO", "APTO_CON_ADVERTENCIAS")
    assert res["estado_g3"] == "APTO"


def test_g3_independiente_sobre_los_archivos(entrega_redes):
    e = entrega_redes["res"]["entregables"]
    leer = lambda k: Path(e[k]).read_text(encoding="utf-8")   # noqa: E731
    r = ht09.validar(json.loads(leer("paquete_json")), informe_visual=leer("informe_visual"), informe_tecnico=leer("informe_tecnico"),
                     memorando=leer("memorando"), anexo=e["anexo_datos"], rutas=e, esquema=esquema_paquete(entrega_redes["ent"].cfg))
    assert r["dictamen"] in ("APTO", "APTO_CON_ADVERTENCIAS"), r["motivo"]


def test_legibilidad_y_accesibilidad_del_informe_visual(entrega_redes):
    html = Path(entrega_redes["res"]["entregables"]["informe_visual"]).read_text(encoding="utf-8")
    leg = ht07.analizar(html, es_html=True)
    assert leg["fernandez_huerta"] >= 70
    assert leg["pct_frases_mas_de_20"] <= 5
    assert '<html lang="es' in html and "<title>" in html and 'name="viewport"' in html
    assert "<script src=" not in html and "http://" not in html            # autocontenido
    assert "En 30 segundos" in ht07.extraer_texto_html(html)
    for c in re.findall(r'meta name="(pet_id|data_cutoff|semaforo)"', html):
        assert c


def test_informe_tecnico_y_memorando(entrega_redes):
    e = entrega_redes["res"]["entregables"]
    tec = Path(e["informe_tecnico"]).read_text(encoding="utf-8")
    memo = Path(e["memorando"]).read_text(encoding="utf-8")
    assert tec.count("\n## ") >= 12
    assert entrega_redes["res"]["rec_id"] in tec
    assert len(memo.split()) < len(tec.split())
    for t in (tec, memo):
        assert "sk-" not in t and "@" not in t


def test_anexo_xlsx(entrega_redes):
    wb = openpyxl.load_workbook(entrega_redes["res"]["entregables"]["anexo_datos"], read_only=True)
    hojas = set(wb.sheetnames)
    for h in ("Leeme", "Puntuaciones", "Cifras", "Fuentes", "Escenarios", "Sensibilidades", "Pronosticos", "Artefactos", "Encargos_C"):
        assert h in hojas
    assert any(h.startswith("Universo_") for h in hojas)


def test_registros_tras_la_entrega(entrega_redes):
    ent, res = entrega_redes["ent"], entrega_redes["res"]
    alm = ent.alm
    assert alm.estado("F1", tipo="PETICION")[res["pet_id"]]["estado"] == "ENTREGADA"
    assert res["rec_id"] in alm.estado("F3")
    assert any(k.startswith("CAND-B-") for k in alm.estado("F3"))
    f4 = alm.estado("F4")
    assert f4 and all(p["estado"] == "ABIERTO" for p in f4.values())
    assert {p.get("tipo") for p in f4.values()} >= {"AMBITO", "RANKING"}
    assert alm.leer("F2") and alm.leer("F6") and alm.leer("RC")
    assert all(alm.verificar_integridad().values())
    calc = [e for e in alm.leer("RC") if e.get("tipo_entrada") == "CALC"]
    assert calc and all(c.get("fecha_corte") for c in calc)


def test_entrega_registrada_en_ct_b_02(entrega_redes):
    ent, res = entrega_redes["ent"], entrega_redes["res"]
    archivo = ent.salida / f"{AS_OF}_entrega_{res['pet_id']}.json"
    d = json.loads(archivo.read_text(encoding="utf-8"))
    assert d["resumen"]["veredicto"] == res["resumen"]["veredicto"]
    assert res["resumen"]["siguiente_paso_sugerido"] in ("ENVIAR_CANDIDATOS_A_C", "PROFUNDIZAR_EN_B", "VIGILAR", "DESCARTAR")


# ------------------------------------------------------------------------------------------------ ámbitos y tipos
def test_universos_de_ejemplo_cubren_los_12_tipos():
    cfg = cargar_config()
    amb = cargar_ambitos(cfg)
    from bloque_b.entorno import cargar_universos
    uni = cargar_universos(cfg)
    cubiertos = set()
    for clave, a in amb.items():
        for t in a["tipos_activo"]:
            u = ht11.construir_universo(t, [{"nombre": t, "filas": uni[t]}], AS_OF, clave, a.get("horizonte", "H3"))
            assert u["tamano_invertible"] >= 3, (clave, t, u["excluidos_por_motivo"])
            assert u["excluidos"], (clave, t)            # cada universo de ejemplo ejercita al menos una exclusión
            cubiertos.add(t)
    assert cubiertos == set(TIPOS_ACTIVO)


def test_universo_punto_en_el_tiempo():
    from bloque_b.entorno import cargar_universos
    uni = cargar_universos(cargar_config())
    pasado = ht11.construir_universo("RV", [{"nombre": "RV", "filas": uni["RV"]}], "2023-06-30", "redes_electricas_europa", "H4")
    hoy = ht11.construir_universo("RV", [{"nombre": "RV", "filas": uni["RV"]}], AS_OF, "redes_electricas_europa", "H4")
    ids = lambda u: {f["id"] for f in u["incluidos"]} | {f["id"] for f in u["excluidos"]}   # noqa: E731
    assert ids(pasado) != ids(hoy) or pasado["fuera_de_fecha"] != hoy["fuera_de_fecha"]


@pytest.mark.parametrize("clave", list(cargar_ambitos(cargar_config())))
def test_cada_ambito_de_ejemplo_se_entrega(hacer_entorno, rapido, clave):
    ent = hacer_entorno(rapido)
    r = Coordinador(ent).recibir(peticion_ambito(clave))
    assert r["estado_peticion"] == "ENTREGADA", r
    assert r["estado_g3"] in ("APTO", "APTO_CON_ADVERTENCIAS")
    p = json.loads(Path(r["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(esquema_paquete(ent.cfg)).validate(p)
    leg = ht07.analizar(Path(r["entregables"]["informe_visual"]).read_text(encoding="utf-8"), es_html=True)
    assert leg["fernandez_huerta"] >= 70


@pytest.mark.parametrize("nivel", ["N1", "N3"])
def test_niveles_n1_y_n3(hacer_entorno, rapido, nivel):
    ent = hacer_entorno(rapido)
    r = Coordinador(ent).recibir(peticion_ambito("redes_electricas_europa", nivel=nivel))
    assert r["estado_peticion"] == "ENTREGADA" and r["estado_g3"] in ("APTO", "APTO_CON_ADVERTENCIAS")
    p = json.loads(Path(r["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
    assert p["estrategia"]["nivel"] == nivel
