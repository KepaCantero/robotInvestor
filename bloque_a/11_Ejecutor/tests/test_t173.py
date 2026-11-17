"""T-173 · PB-50 y PB-64 del Plan de pruebas V3.0 (INC-T116-03).

- PB-50 (12.2 del Documento 0): un horizonte H1–H4 cuyo acierto es inferior a la referencia ingenua con significación
  (DM-HLN) pasa solo de «Sí» a «Limitado», con su AJU- en F6 y su CFG- de P-31 en F10; ningún cambio hacia o desde «No».
- PB-64 (12.1; esquema de F4, 5.1): los estados de los H5 por hitos se publican en F6 (EH5-) y en los entregables.
"""
import json
from pathlib import Path

import pandas as pd
import pytest
from bloque_a.almacen import Almacen
from bloque_a.configuracion import CLASES, aplicabilidad, parametro
from bloque_a.evaluador import Evaluador, estado_hito
from conftest import AS_OF, RAIZ, config_pruebas, nuevo_bloque

FECHA = "2026-06-05"
CFG = config_pruebas(evaluacion={"bootstrap_replicas": 50, "simulaciones_ece": 50})
N_MIN = int(parametro(CFG, "evaluacion.min_calibrar"))
ALFA = float(parametro(CFG, "evaluacion.alfa_holm"))
MIN_CONG = int(parametro(CFG, "evaluacion.min_conglomerados_bootstrap"))
# H-06 (cierre de la QA r02): la familia de Holm de la revisión son todas las celdas H1–H4 en «Sí» de la tabla del bloque
FAMILIA = sum(1 for c in CLASES for h in ("H1", "H2", "H3", "H4") if aplicabilidad(CFG, c, h) == "SI")


def _sembrar(a: Almacen, clase: str, h: str, n: int, gana: bool = False, desde: int = 1, contaminado: bool = False,
             o=None, p: float = 0.85, resol=None) -> None:
    """`n` pronósticos resueltos de `clase` × `h`, uno por semana y cada uno con su fecha de resolución (un conglomerado
    PA-03 por PRG): dicen 0,85 y aciertan 1 de cada 3 (pierden contra la referencia de 0,5) o, con `gana`, 9 de cada 10.
    `o(i)` y `resol(i)` sustituyen el resultado y la fecha de resolución."""
    for i in range(n):
        pid = f"PRG-2025-{desde + i:04d}"
        oi = o(i) if o else (int(i % 10 != 0) if gana else int(i % 3 == 0))
        emision = pd.Timestamp("2025-01-06") + pd.Timedelta(days=7 * i)
        fr = resol(i) if resol else str((emision + pd.Timedelta(days=14)).date())
        a.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": pid, "opp_id": "OPP-T173", "clase": clase, "horizonte": h,
                                   "prob_interna": p, "sentido": "POSITIVO", "en_informe": True,
                                   "fecha_emision": str(emision.date()), "fecha_resolucion": fr,
                                   "referencia_ingenua": {"valor_o_prob": 0.5}, "estado": "ABIERTO",
                                   **({"contaminacion_posible": True} if contaminado else {})})
        a.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": pid, "estado": "RESUELTO",
                                   "resolucion": {"resultado_binario": oi, "comprobacion_fuga": "SUPERADA", "valor_observado": 0.01,
                                                  "fecha_resuelto": fr}})


def _uniforme(n: int, k: int):
    """`k` aciertos repartidos de forma regular entre `n`."""
    import numpy as np
    unos = set(np.linspace(0, n - 1, k).round().astype(int).tolist())
    return lambda i: int(i in unos)


def _evaluador(tmp_path, fecha=FECHA):
    a = Almacen(tmp_path / "estado")
    a.reloj.fijar(fecha)
    return a, Evaluador(a, None, None, CFG, None)


def _restituir(a, fecha):
    """Un tipo 3 que devuelve RF × H2 a «Sí»."""
    import copy
    matriz = copy.deepcopy(a.estado("F10")["P-31"]["valor_vigente"])
    matriz["RF"]["H2"] = "SI"
    a.escribir("F10", "AG-20", {"tipo_entrada": "CFG", "cfg_id": f"CFG-T3-{fecha}", "param_id": "P-31", "autor": "AG-20",
                                "de": None, "a": matriz, "valor_vigente": matriz, "regimen": "OPERADOR", "motivo": "tipo 3",
                                "fecha_registro": fecha, "fecha_efecto": fecha, "revierte_a": None})


# ================================================================================================ PB-50
def test_pb50_rf_h2_pierde_con_significacion_y_baja_a_limitado(tmp_path):
    a, e = _evaluador(tmp_path)
    _sembrar(a, "RF", "H2", 35)
    assert aplicabilidad(CFG, "RF", "H2") == "SI"
    celda = e.degradacion_dm(FECHA)["RF|H2"]
    assert celda["n"] == 35 and celda["conglomerados"] == 35 and celda["n_eff"] >= N_MIN
    assert FAMILIA > 1 and celda["celdas_holm"] == FAMILIA and celda["umbral_holm"] == ALFA / FAMILIA
    assert celda["degradar"] and celda["dm_hln"]["p_valor"] <= celda["umbral_holm"] and celda["brier"] > celda["brier_ref"]
    hechos = e.aplicar_degradacion_dm(FECHA)
    assert [(h["tipo_entrada"], h["parametro"], h["celda"], h["de"], h["a"]) for h in hechos] == [
        ("AJU", "P-31", {"clase": "RF", "horizonte": "H2"}, "SI", "LIMITADO")]
    aju = a.estado("F6", clave="id")[hechos[0]["id"]]
    ev_dm = aju["evidencia"]["dm_hln"]
    assert (ev_dm["p_valor"], ev_dm["h"], ev_dm["n_conglomerados"]) == (celda["dm_hln"]["p_valor"], celda["h"], 35)
    assert ev_dm["estadistico"] < 0
    ev = aju["evidencia"]
    assert (ev["alfa"], ev["n"], ev["n_eff"], ev["conglomerados"], ev["umbral_holm"], ev["celdas_holm"]) == (
        ALFA, 35, celda["n_eff"], 35, ALFA / FAMILIA, FAMILIA) and len(ev["prg"]) == 35 and ev["revision"] == "RDM-2026-06"
    cfg = [x for x in a.leer("F10") if x.get("tipo_entrada") == "CFG"]
    p31 = [x for x in cfg if x["param_id"] == "P-31"]
    assert len(p31) == 1 and p31[0]["origen"] == aju["id"] and p31[0]["cfg_id"].startswith("CFG-")
    assert p31[0]["de"]["RF"]["H2"] == "SI" and p31[0]["a"]["RF"]["H2"] == "LIMITADO"
    # solo cambia esa celda (ningún cambio hacia o desde «No»)
    cambios = {(c, h) for c in p31[0]["de"] for h in p31[0]["de"][c] if p31[0]["de"][c][h] != p31[0]["a"][c][h]}
    assert cambios == {("RF", "H2")}
    assert [x["param_id"] for x in cfg] == ["P-31", "P-30"] and a.estado("F10")["P-31"]["valor_vigente"]["RF"]["H2"] == "LIMITADO"
    rdm = a.estado("F6", clave="id")["RDM-2026-06"]                    # registro de la revisión mensual
    assert rdm["ajustes"] == [aju["id"]] and rdm["celdas"]["RF|H2"]["degradar"]


@pytest.mark.parametrize("caso", ["n_insuficiente", "gana", "contaminados"])
def test_pb50_sin_muestra_o_sin_perdida_significativa_no_degrada(tmp_path, caso):
    a, e = _evaluador(tmp_path)
    if caso == "n_insuficiente":
        _sembrar(a, "RF", "H2", N_MIN - 1)
    elif caso == "gana":
        _sembrar(a, "RF", "H2", 35, gana=True)
    else:                                                  # PA-09: los contaminados no cuentan para la degradación
        _sembrar(a, "RF", "H2", 35, contaminado=True)
    celda = e.degradacion_dm(FECHA).get("RF|H2")
    assert celda is None or not celda["degradar"]
    assert e.aplicar_degradacion_dm(FECHA) == [] and "P-31" not in a.estado("F10")


def test_pb50_r02_h01_una_sola_semana_mala_no_degrada(tmp_path):
    """QA r01, H-01 (§4): 30 PRG de RF × H2 resueltos el mismo día son un solo conglomerado PA-03 (n_eff = 1): no degrada."""
    a, e = _evaluador(tmp_path)
    _sembrar(a, "RF", "H2", 30, resol=lambda i: "2026-05-29")
    celda = e.degradacion_dm(FECHA)["RF|H2"]
    assert celda["conglomerados"] == 1 and celda["n_eff"] < N_MIN and celda["dm_hln"] is None and not celda["degradar"]
    assert "muestra insuficiente" in celda["motivo"]
    assert e.aplicar_degradacion_dm(FECHA) == [] and "P-31" not in a.estado("F10")


def test_pb50_r02_h01_historia_buena_mas_una_semana_mala_no_degrada(tmp_path):
    """QA r01, H-01 (§4b y §12): 60 semanas en que el pronóstico gana y una semana mala de 30 PRG. Por PRG, con h = 1, «pierde»
    (p ≈ 0,08); por conglomerado de fecha (61) gana con claridad: no degrada."""
    a, e = _evaluador(tmp_path)
    _sembrar(a, "RF", "H2", 60, gana=True)
    _sembrar(a, "RF", "H2", 30, desde=500, o=lambda i: 0, resol=lambda i: "2026-05-29")
    celda = e.degradacion_dm(FECHA)["RF|H2"]
    assert celda["n"] == 90 and celda["conglomerados"] == 61 and celda["dm_hln"]["n_conglomerados"] == 61
    assert celda["brier"] > celda["brier_ref"]                         # por PRG, el pronóstico pierde…
    assert celda["dm_hln"]["p_valor"] > 0.99 and not celda["degradar"]  # …pero por conglomerado gana
    assert e.aplicar_degradacion_dm(FECHA) == []


def test_pb50_r02_h01_sin_fechas_de_conglomerado_ni_conglomerados_minimos_no_degrada(tmp_path):
    a, e = _evaluador(tmp_path)
    # 35 PRG en MIN_CONG − 1 fechas, con una n mínima que n_eff cumple (min_calibrar = 5): solo faltan conglomerados
    e.cfg = config_pruebas(evaluacion={"min_calibrar": 5})
    _sembrar(a, "RF", "H2", 35, resol=lambda i: str((pd.Timestamp("2025-06-02") + pd.Timedelta(days=7 * (i % (MIN_CONG - 1)))).date()))
    celda = e.degradacion_dm(FECHA)["RF|H2"]
    assert celda["conglomerados"] == MIN_CONG - 1 and celda["n_eff"] >= 5
    assert not celda["degradar"] and celda["dm_hln"] is None and "conglomerados (mínimo" in celda["motivo"]
    a2, e2 = _evaluador(tmp_path / "b")
    _sembrar(a2, "RF", "H2", 35)
    e2._fechas_conglomerado = lambda lst: None                         # sin fechas interpretables: falla cerrado
    c2 = e2.degradacion_dm(FECHA)["RF|H2"]
    assert not c2["degradar"] and "sin fechas" in c2["motivo"]


def test_pb50_r02_h01_n_suficiente_pero_n_eff_insuficiente_no_degrada(tmp_path):
    """60 PRG en 12 fechas, con el mismo resultado dentro de cada fecha (residuos muy correlados): n = 60 ≥ 30 pero
    n_eff < 30 (efecto de diseño de Kish, PA-03): no degrada aunque las 12 medias pierdan."""
    a, e = _evaluador(tmp_path)
    _sembrar(a, "RF", "H2", 60, o=lambda i: int((i // 5) % 3 == 0),
             resol=lambda i: str((pd.Timestamp("2025-06-02") + pd.Timedelta(days=7 * (i // 5))).date()))
    celda = e.degradacion_dm(FECHA)["RF|H2"]
    assert celda["n"] == 60 and celda["conglomerados"] == 12 and celda["n_eff"] < N_MIN
    assert not celda["degradar"] and celda["dm_hln"] is None and "n_eff" in celda["motivo"]
    assert e.aplicar_degradacion_dm(FECHA) == []


def test_pb50_con_p_por_encima_de_alfa_no_degrada(tmp_path):
    a, e = _evaluador(tmp_path)
    _sembrar(a, "RF", "H2", 35)
    p = e.degradacion_dm(FECHA)["RF|H2"]["dm_hln"]["p_valor"]
    e.cfg = config_pruebas(evaluacion={"alfa_holm": p / 2})            # α por debajo de la p observada
    assert not e.degradacion_dm(FECHA)["RF|H2"]["degradar"] and e.aplicar_degradacion_dm(FECHA) == []


def test_pb50_r02_h03_holm_entre_las_celdas_de_la_misma_revision(tmp_path):
    """QA r01, H-03 y cierre de la QA r02, H-06 (decisión por delegación del operador del 17-11-2026, opción b): Holm con la
    familia fija de todas las celdas H1–H4 en «Sí» del bloque, tengan muestra o no. RF × H2 con p entre α/2 y α, que con la
    familia de las celdas evaluables (r02) degradaba sola, ya no degrada: su umbral es α/FAMILIA."""
    a, e = _evaluador(tmp_path)
    _sembrar(a, "RF", "H2", 40, p=0.6, o=_uniforme(40, 17))
    sola = e.degradacion_dm(FECHA)["RF|H2"]
    assert ALFA / 2 < sola["dm_hln"]["p_valor"] <= ALFA
    assert sola["celdas_holm"] == FAMILIA and sola["umbral_holm"] == ALFA / FAMILIA and not sola["degradar"]
    assert "Holm" in sola["motivo"] and e.aplicar_degradacion_dm(FECHA) == [] and "P-31" not in a.estado("F10")
    # una segunda celda que no pierde no cambia la familia (sigue siendo la misma) ni el umbral de la primera
    _sembrar(a, "RF", "H3", 40, desde=301, p=0.6, o=lambda i: int(i % 2 == 0))
    rev = e.degradacion_dm(FECHA)
    assert rev["RF|H2"]["celdas_holm"] == rev["RF|H3"]["celdas_holm"] == FAMILIA
    assert rev["RF|H2"]["umbral_holm"] == ALFA / FAMILIA and not rev["RF|H2"]["degradar"] and not rev["RF|H3"]["degradar"]


def test_pb50_cierre_h06_la_familia_es_fija_y_cuenta_las_celdas_sin_muestra(tmp_path):
    """H-06: la familia no depende de qué celdas tienen muestra. Con la misma celda perdiendo, el umbral es α/FAMILIA con
    una sola celda evaluable; al degradar una celda en «Sí» la familia de la revisión siguiente tiene una menos."""
    a, e = _evaluador(tmp_path, "2026-04-06")
    _sembrar(a, "RF", "H2", 35)
    rev = e.degradacion_dm("2026-04-06")
    assert len(rev) == 1 and rev["RF|H2"]["celdas_holm"] == FAMILIA            # una evaluable, familia entera
    assert len(e.aplicar_degradacion_dm("2026-04-06")) == 1
    a.reloj.fijar("2026-05-04")
    assert e.degradacion_dm("2026-05-04")["RF|H2"]["umbral_holm"] is None      # ya «Limitado»: fuera de la familia
    _sembrar(a, "RF", "H3", 35, desde=101)
    assert e.degradacion_dm("2026-05-04")["RF|H3"]["celdas_holm"] == FAMILIA - 1


@pytest.mark.parametrize(("clase", "h", "valor"), [("RF", "H1", "LIMITADO"), ("MON", "H4", "NO")])
def test_pb50_ningun_cambio_hacia_o_desde_no(tmp_path, clase, h, valor):
    """«Limitado» → «No» no es automático por DM (12.2) y una celda «No» no se mueve: ni AJU-, ni CFG-, ni P3. La celda pierde
    con significación, pero no entra en la familia de Holm de la revisión (no puede bajar)."""
    a, e = _evaluador(tmp_path)
    assert aplicabilidad(CFG, clase, h) == valor
    _sembrar(a, clase, h, 35)
    celda = e.degradacion_dm(FECHA)[f"{clase}|{h}"]
    assert celda["dm_hln"]["p_valor"] <= ALFA and not celda["degradar"] and f"«{valor}»" in celda["motivo"]
    assert e.aplicar_degradacion_dm(FECHA) == []
    assert not [x for x in a.leer("F6") if x.get("parametro") == "P-31"] and "P-31" not in a.estado("F10")


def test_pb50_r02_h03_solo_en_la_revision_mensual(tmp_path):
    """QA r01, H-03: la degradación DM es la revisión mensual (PB-50, paso 2): el primer C5 del mes la hace y deja RDM-; el
    resto de C5 del mes no evalúa nada, aunque la celda haya vuelto a «Sí»."""
    a, e = _evaluador(tmp_path)
    _sembrar(a, "RF", "H2", 35)
    assert len(e.aplicar_degradacion_dm(FECHA)) == 1 and "RDM-2026-06" in a.estado("F6", clave="id")
    a.reloj.fijar("2026-06-12")
    assert e.aplicar_degradacion_dm("2026-06-12") == []
    assert [x["id"] for x in a.leer("F6") if x.get("tipo_entrada") == "REVISION_DM"] == ["RDM-2026-06"]
    a2, e2 = _evaluador(tmp_path / "b")                                # sin nada que degradar también deja su registro
    _sembrar(a2, "RF", "H2", 35, gana=True)
    assert e2.aplicar_degradacion_dm(FECHA) == [] and a2.estado("F6", clave="id")["RDM-2026-06"]["ajustes"] == []


def test_pb50_un_escalon_por_trimestre_y_nunca_sube(tmp_path):
    a, e = _evaluador(tmp_path, "2026-04-06")
    _sembrar(a, "RF", "H2", 35)
    _sembrar(a, "RF", "H3", 35, desde=101)
    assert len(e.aplicar_degradacion_dm("2026-04-06")) == 2
    a.reloj.fijar("2026-05-04")
    assert e.aplicar_degradacion_dm("2026-05-04") == []                # mes nuevo, mismo trimestre, ya «Limitado»: nada
    a.reloj.fijar("2026-07-03")
    assert e.aplicar_degradacion_dm("2026-07-03") == []                # trimestre nuevo, ya «Limitado»: no pasa a «No»
    assert a.estado("F10")["P-31"]["valor_vigente"]["RF"]["H2"] == "LIMITADO"


def test_pb50_restituida_a_si_no_vuelve_a_bajar_en_el_mismo_trimestre(tmp_path):
    """Esquema F10, regla 7: como mucho un escalón por celda y trimestre, aunque un tipo 3 la haya devuelto a «Sí»."""
    a, e = _evaluador(tmp_path, "2026-04-06")
    _sembrar(a, "RF", "H2", 35)
    assert len(e.aplicar_degradacion_dm("2026-04-06")) == 1
    a.reloj.fijar("2026-05-04")
    _restituir(a, "2026-05-04")
    assert e.aplicar_degradacion_dm("2026-05-04") == []                # revisión de mayo, mismo trimestre: no baja otra vez
    a.reloj.fijar("2026-07-03")
    assert len(e.aplicar_degradacion_dm("2026-07-03")) == 1            # trimestre nuevo: sí


def test_pb50_r02_h02_un_fallo_en_f10_anula_el_ajuste_y_el_reintento_degrada(tmp_path):
    """QA r01, H-02 (§10): si la escritura de F10 falla, F6 no afirma un ajuste que no se aplicó (AJU- ANULADO, sin la
    revisión RDM- del mes) y el C5 siguiente del mismo mes y trimestre sí degrada."""
    a, e = _evaluador(tmp_path)
    _sembrar(a, "RF", "H2", 35)
    orig = a.escribir

    def roto(archivo, autor, entrada):
        if archivo == "F10":
            raise OSError("disco lleno (simulado)")
        return orig(archivo, autor, entrada)
    a.escribir = roto
    with pytest.raises(OSError):
        e.aplicar_degradacion_dm(FECHA)
    a.escribir = orig
    aju = [x for x in a.estado("F6", clave="id").values() if x.get("tipo_entrada") == "AJU"]
    assert [(x["estado"], x["aplicado_en_produccion"], x["cfg_p31_revertido"]) for x in aju] == [("ANULADO", False, None)]
    assert "P-31" not in a.estado("F10") and "RDM-2026-06" not in a.estado("F6", clave="id")
    a.reloj.fijar("2026-06-12")
    hechos = e.aplicar_degradacion_dm("2026-06-12")
    assert len(hechos) == 1 and a.estado("F10")["P-31"]["valor_vigente"]["RF"]["H2"] == "LIMITADO"


def test_pb50_r02_h02_si_falla_el_cfg_de_p30_se_revierte_el_de_p31(tmp_path):
    a, e = _evaluador(tmp_path)
    _sembrar(a, "RF", "H2", 35)
    orig = a.escribir

    def roto(archivo, autor, entrada):
        if archivo == "F10" and entrada.get("param_id") == "P-30":
            raise OSError("disco lleno (simulado)")
        return orig(archivo, autor, entrada)
    a.escribir = roto
    with pytest.raises(OSError):
        e.aplicar_degradacion_dm(FECHA)
    a.escribir = orig
    cfg31 = [x for x in a.leer("F10") if x.get("param_id") == "P-31"]
    assert len(cfg31) == 2 and cfg31[1]["revierte_a"] == cfg31[0]["cfg_id"]
    mv = cfg31[1]["methodology_version"]                               # H-05: la reversión no anuncia un cambio de versión
    assert mv["a"] == mv["de"] == cfg31[0]["methodology_version"]["de"] and "P-30" not in a.estado("F10")
    assert a.estado("F10")["P-31"]["valor_vigente"]["RF"]["H2"] == "SI"   # la celda queda como estaba
    aju = next(x for x in a.estado("F6", clave="id").values() if x.get("tipo_entrada") == "AJU")
    assert (aju["estado"], aju["aplicado_en_produccion"], aju["cfg_p31_revertido"]) == ("ANULADO", False, True)


def test_pb50_h5_no_entra_en_la_degradacion_por_dm(tmp_path):
    a, e = _evaluador(tmp_path)
    _sembrar(a, "RV", "H5", 35)
    assert "RV|H5" not in e.degradacion_dm(FECHA) and e.aplicar_degradacion_dm(FECHA) == []


def test_pb50_el_c5_degrada_y_el_ciclo_lee_limitado_sin_bloqueo_de_g3(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.reloj.fijar("2026-06-01")
    _sembrar(b.almacen, "RF", "H2", 35)
    r = b.ciclo(AS_OF, alcance={"clases": ["RF"]})
    dm = r["evaluacion"]["degradacion_dm"]
    assert [(x["celda"], x["de"], x["a"]) for x in dm] == [({"clase": "RF", "horizonte": "H2"}, "SI", "LIMITADO")]
    assert aplicabilidad(b.cfg, "RF", "H2") == "LIMITADO"              # la tabla vigente de este ciclo y del siguiente
    assert r["g3"]["dictamen"] in ("APTO", "APTO_CON_ADVERTENCIAS")    # G3 (HT-09, aplicabilidad) no bloquea
    r2 = b.ciclo("2026-06-12", alcance={"clases": ["RF"]})
    assert r2["evaluacion"]["degradacion_dm"] == [] and aplicabilidad(b.cfg, "RF", "H2") == "LIMITADO"
    assert r2["g3"]["dictamen"] in ("APTO", "APTO_CON_ADVERTENCIAS")


def test_pb50_un_fallo_de_la_degradacion_dm_no_tumba_el_c5(tmp_path, monkeypatch):
    a, e = _evaluador(tmp_path)
    monkeypatch.setattr(e, "aplicar_degradacion_dm", lambda *_a, **_k: (_ for _ in ()).throw(RuntimeError("roto")))
    res = e.ciclo(FECHA)
    assert res["degradacion_dm"] == []
    assert any("DM-HLN" in str(x.get("descripcion") or x) for x in a.leer("HA"))


# ================================================================================================ PB-64
def _hito(a, hid, padre, clase, o, fecha, necesario=False):
    a.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": hid, "opp_id": "OPP-H5", "clase": clase, "horizonte": "H4",
                               "prob_interna": 0.65, "sentido": "POSITIVO", "en_informe": True, "es_hito": True, "prg_padre": padre,
                               "necesario": necesario, "fecha_emision": "2025-06-05", "fecha_resolucion": fecha,
                               "referencia_ingenua": {"valor_o_prob": 0.5}, "estado": "ABIERTO"})
    if o is not None:
        a.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": hid, "estado": "RESUELTO",
                                   "resolucion": {"resultado_binario": o, "comprobacion_fuga": "SUPERADA", "fecha_resuelto": fecha}})


def _sembrar_h5(a, clase="RV"):
    """Tres H5 abiertos, uno por estado, con un hito pendiente cada uno, y uno ya resuelto (no se publica)."""
    casos = {"PRG-2025-0801": ([1, 1, None], None), "PRG-2025-0802": ([0, 0, None], None), "PRG-2025-0803": ([1, 0, None], 1),
             "PRG-2025-0804": ([1, 1, 1], None)}
    for padre, (res, nec) in casos.items():
        ids = []
        for i, o in enumerate(res):
            hid = f"HIT-2025-{padre[-3:]}{i}"
            _hito(a, hid, padre, clase, o, f"2026-0{i + 3}-02" if o is not None else "2027-03-02", necesario=(i == nec))
            ids.append(hid)
        a.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": padre, "opp_id": "OPP-H5", "clase": clase, "horizonte": "H5",
                                   "prob_interna": None, "hit_ids": ids, "fecha_emision": "2025-06-05",
                                   "fecha_resolucion": "2045-06-05", "estado": "ABIERTO"})
    a.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": "PRG-2025-0804", "estado": "NO_RESOLUBLE"})


def test_estado_hito_publicable():
    assert estado_hito(None) == "PENDIENTE" and estado_hito({"estado": "ABIERTO"}) == "PENDIENTE"
    assert estado_hito({"estado": "NO_RESOLUBLE"}) == "NO_RESOLUBLE"
    assert estado_hito({"estado": "RESUELTO", "resolucion": {"resultado_binario": 1}}) == "CUMPLIDO"
    assert estado_hito({"estado": "RESUELTO", "resolucion": {"resultado_binario": 0}}) == "FALLADO"


def test_pb64_c5_publica_los_estados_h5_en_f6(tmp_path):
    a, e = _evaluador(tmp_path)
    _sembrar_h5(a)
    res = e.ciclo(FECHA)
    ent = res["estados_h5"]
    assert ent["id"] == f"EH5-{FECHA}" and ent["id"] in a.estado("F6", clave="id")
    pron = a.estado("F6", clave="id")[ent["id"]]["pronosticos"]
    assert {k: v["estado"] for k, v in pron.items()} == {
        "PRG-2025-0801": "EN_CURSO_CONFORME", "PRG-2025-0802": "DESVIADO", "PRG-2025-0803": "INVALIDADO"}   # solo los abiertos
    assert pron["PRG-2025-0802"]["hitos"] == {"HIT-2025-8020": "FALLADO", "HIT-2025-8021": "FALLADO", "HIT-2025-8022": "PENDIENTE"}
    celda = ent["celdas"]["RV"]
    assert celda["prg_por_estado"] == {"EN_CURSO_CONFORME": 1, "DESVIADO": 1, "INVALIDADO": 1}
    # la tasa de la celda es la del estado_h5 (P-42): 6 de 9 hitos resueltos cumplidos, también los del H5 ya resuelto
    assert (celda["n_hitos"], celda["tasa_cumplidos"]) == (9, round(6 / 9, 4))
    assert ent["umbral"] == e.estado_h5(FECHA)["umbral"] and e.estados_h5_vigentes(FECHA)["eh5_id"] == ent["id"]


def test_pb64_sin_h5_no_publica_nada(tmp_path):
    a, e = _evaluador(tmp_path)
    assert e.ciclo(FECHA)["estados_h5"] is None and e.estados_h5_vigentes(FECHA) is None
    assert not [x for x in a.leer("F6") if x.get("tipo_entrada") == "EH5"]


def test_pb64_paquete_y_tecnico_publican_los_estados_h5(tmp_path, universo):
    import jsonschema
    b = nuevo_bloque(tmp_path, universo)
    b.reloj.fijar("2026-06-01")
    _sembrar_h5(b.almacen)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert r["g3"]["dictamen"] in ("APTO", "APTO_CON_ADVERTENCIAS") and r["entregables"]
    js = json.loads(Path(r["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
    f6 = b.almacen.estado("F6", clave="id")[f"EH5-{AS_OF}"]
    assert js["x_estados_h5"]["eh5_id"] == f6["id"]
    assert js["x_estados_h5"]["pronosticos"] == f6["pronosticos"] and js["x_estados_h5"]["celdas"] == f6["celdas"]
    esquema = json.loads((RAIZ.parent / "06_Plantillas_entregables" / "Esquema JSON - Paquete de oportunidades - V5.0.json")
                         .read_text(encoding="utf-8"))
    assert not [e.message for e in jsonschema.Draft202012Validator(esquema).iter_errors(js)]
    hitos = [x for d in js["clases"].values() for o in d["opciones"] for v in o["horizontes"].values() for x in v.get("hitos") or []]
    assert hitos and all(x["estado"] in ("PENDIENTE", "CUMPLIDO", "FALLADO", "NO_RESOLUBLE") for x in hitos)
    tecnico = Path(r["entregables"]["informe_tecnico"]).read_text(encoding="utf-8")
    assert f"**Pronósticos H5 por hitos** (`{f6['id']}`" in tecnico
    for pid, est in (("PRG-2025-0801", "EN_CURSO_CONFORME"), ("PRG-2025-0802", "DESVIADO"), ("PRG-2025-0803", "INVALIDADO")):
        assert f"| `{pid}` | RV | {est} |" in tecnico
    assert "| RV×H5 | 9 | 0.6667 | 1 | 1 | 1 |" in tecnico
    assert hitos and f"`{hitos[0]['hit_id']}` · {hitos[0]['fecha']}" in tecnico and f"estado: {hitos[0]['estado']}" in tecnico
