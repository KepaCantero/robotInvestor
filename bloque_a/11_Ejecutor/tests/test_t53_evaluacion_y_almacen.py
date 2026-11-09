"""T-53 · Regresiones del Evaluador, HT-01 (datos y bóveda), F4 (R11) y HT-08.

Cada prueba cubre un defecto verificado por la revisión del Bloque A (CA-02, CA-07, CA-08, CA-09, CA-10, CA-13,
CS-03, CS-05, CS-12 y la cesta de RI-TB) y falla sin su corrección.
"""
import datetime as dt
import json
import math
import os
import stat

import numpy as np
import pandas as pd
import pytest
from bloque_a.almacen import Almacen, EscrituraFueraDeReserva, PronosticoCongelado
from bloque_a.contratos import ANALISTAS
from bloque_a.evaluador import (
    BANDAS_VERBALES_POR_DEFECTO,
    PROB_DE_BANDA,
    Evaluador,
    banda_de,
    banda_publicable,
    fijar_bandas,
)
from bloque_a.herramientas import ht01_boveda as hb
from bloque_a.herramientas.ht01_datos import (
    DatosInvalidos,
    DatosNoDisponibles,
    ProveedorCSV,
    ProveedorSintetico,
)
from bloque_a.herramientas.ht08_monitor import SIN_ESTADO, Monitor
from bloque_a.motor import evaluacion as ev
from conftest import RAIZ

ESQUEMA_PAQUETE = RAIZ.parent / "06_Plantillas_entregables" / "Esquema JSON - Paquete de oportunidades - V5.0.json"


class MotorFalso:
    def servir(self, *a, **k):
        return {"calc_id": "CALC-PRUEBA"}


def _alta(a: Almacen, pid: str, **campos) -> None:
    base = {"tipo_entrada": "ALTA", "prg_id": pid, "opp_id": "OPP-1", "clase": "RV", "horizonte": "H3", "prob_interna": 0.65,
            "sentido": "POSITIVO", "en_informe": True, "fecha_emision": "2026-06-05", "referencia_ingenua": {"valor_o_prob": 0.5},
            "estado": "ABIERTO"}
    a.escribir("F4", "AG-10", {**base, **campos})


def _resolver(a: Almacen, pid: str, o: int, fecha: str = "2030-01-10") -> None:
    a.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": pid, "estado": "RESUELTO",
                               "resolucion": {"resultado_binario": o, "comprobacion_fuga": "SUPERADA", "valor_observado": 0.1 if o else -0.1,
                                              "fecha_resuelto": fecha}})


# ------------------------------------------------------------------------------------------------ CA-02 · HT-01
@pytest.mark.parametrize("malo", ["-", "n.d.", '"1.234,5"', "inf", "1e400"])
def test_ht01_cierre_no_numerico_rechaza_la_serie(tmp_path, malo):
    (tmp_path / "XYZ.csv").write_text(f"fecha,cierre\n2026-06-01,100\n2026-06-02,101\n2026-06-03,{malo}\n", encoding="utf-8")
    p = ProveedorCSV(tmp_path)
    p.fijar_as_of("2026-06-05")
    with pytest.raises(DatosInvalidos, match="serie rechazada"):
        p.valor_en("XYZ", "2026-06-05")
    # se trata como dato no disponible (los llamadores que esperan o marcan NO_RESOLUBLE lo capturan)
    with pytest.raises(DatosNoDisponibles):
        p.cierres("XYZ")


def test_ht01_fecha_publicacion_no_interpretable_no_es_visible(tmp_path):
    (tmp_path / "ABC.csv").write_text("fecha,cierre,fecha_publicacion\n2026-06-01,1,\n2026-06-02,2,2026-07-01\n"
                                      "2026-06-03,3,31/06/2026\n2026-06-04,,\n2026-06-05,5,2026-06-05\n", encoding="utf-8")
    p = ProveedorCSV(tmp_path)
    p.fijar_as_of("2026-06-05")
    vis = p.cierres("ABC")
    assert list(vis.index.strftime("%Y-%m-%d")) == ["2026-06-01", "2026-06-05"]
    assert all(np.isfinite(vis.values))
    p.fijar_as_of("2026-12-31")
    assert "2026-06-03" not in set(p.cierres("ABC").index.strftime("%Y-%m-%d"))   # nunca visible
    desc = p._serie_completa("ABC").attrs["filas_descartadas"]
    assert any("2026-06-03" in d and "fecha_publicacion" in d for d in desc) and any("2026-06-04" in d for d in desc)


def test_ht01_fecha_publicacion_invalida_en_serie_sin_normalizar():
    """Defensa en profundidad: también en `serie()` (series fijas que no pasan por la normalización del CSV)."""
    idx = pd.bdate_range("2026-06-01", "2026-06-05")
    df = pd.DataFrame({"cierre": [1.0, 2.0, 3.0, 4.0, 5.0],
                       "fecha_publicacion": ["", "2026-06-02", "31/06/2026", "2026-07-01", None]}, index=idx)
    p = ProveedorSintetico({}, fijos={"M": df})
    p.fijar_as_of("2026-06-05")
    assert list(p.cierres("M").values) == [1.0, 2.0, 5.0]


# ------------------------------------------------------------------------------------------------ CA-02 · resolver
def _evaluador_nan(tmp_path):
    idx = pd.bdate_range("2026-01-01", "2026-08-31")
    cierre = 100 + np.arange(len(idx)) * 0.1
    cierre[idx >= pd.Timestamp("2026-07-30")] = np.nan          # cierre de resolución no numérico
    p = ProveedorSintetico({}, fijos={"XYZ": pd.DataFrame({"cierre": cierre}, index=idx)})
    a = Almacen(tmp_path)
    a.reloj.fijar("2026-06-05")
    _alta(a, "PRG-2026-0001", horizonte="H2", tipo_pronostico="DIRECCIONAL", variable={"serie_ht01": "XYZ"},
          referencia_indice=None, nivel_referencia={"valor": 117.0, "fecha": "2026-06-05"}, umbral=0.0,
          fecha_resolucion="2026-07-31")
    return Evaluador(a, p, MotorFalso(), {"evaluacion": {}}, pd.DataFrame({"simbolo": ["XYZ"], "clase": ["RV"]})), a, p


def test_resolver_valor_no_finito_es_dato_no_disponible(tmp_path):
    e, a, p = _evaluador_nan(tmp_path)
    # poco después del vencimiento: queda pendiente (nunca NO_OCURRIDO)
    p.fijar_as_of("2026-08-03")
    a.reloj.fijar("2026-08-03")
    assert e.resolver("2026-08-03") == []
    assert a.estado("F4")["PRG-2026-0001"]["estado"] == "ABIERTO"
    # tras los días hábiles sin dato válido: NO_RESOLUBLE, sin resultado ni NaN en F4
    p.fijar_as_of("2026-08-20")
    a.reloj.fijar("2026-08-20")
    r = e.resolver("2026-08-20")
    assert [x["estado"] for x in r] == ["NO_RESOLUBLE"]
    f4 = a.estado("F4")["PRG-2026-0001"]
    assert f4["estado"] == "NO_RESOLUBLE" and "resultado" not in f4["resolucion"]
    assert "NaN" not in (tmp_path / "F4_registro_pronosticos.jsonl").read_text(encoding="utf-8")


# ------------------------------------------------------------------------------------------------ CA-07 · Holm
def test_holm_escalonado_se_detiene_en_el_primer_fallo():
    assert ev.holm_rechazos({"RV|H3": 0.06, "RF|H3": 0.07}, 0.10) == {"RV|H3": False, "RF|H3": False}
    u = ev.holm({"A": 0.01, "B": 0.06, "C": 0.07}, 0.10)
    assert u["A"] == pytest.approx(0.10 / 3) and u["B"] == pytest.approx(0.05) and u["C"] == 0.0
    assert ev.holm_rechazos({"A": 0.01, "B": 0.06, "C": 0.07}, 0.10) == {"A": True, "B": False, "C": False}
    # sin fallos, todas se rechazan con los umbrales nominales
    assert ev.holm_rechazos({"A": 0.01, "B": 0.04, "C": 0.09}, 0.10) == {"A": True, "B": True, "C": True}
    # una celda detrás de la parada no se certifica aunque su p esté por debajo de α
    crit = ev.criterio_certificado({"n": 200, "bss": {"ic": [0.1, 0.2]}, "calibracion": {"ece": 0.01}, "ece_nulo": {"q90": 0.05},
                                    "dm_hln": {"p_unilateral": 0.07}}, 100, 0.15, u["C"])
    assert not crit["certificable"] and any("Holm" in m for m in crit["motivos"])


# ------------------------------------------------------------------------------------------------ CA-08 · hitos H5
def test_hitos_h5_no_cuentan_en_h4_ni_en_el_historial(tmp_path):
    a = Almacen(tmp_path)
    a.reloj.fijar("2030-01-10")
    hits = []
    for i in range(3):
        hid = f"HIT-2026-000{i + 1}"
        hits.append(hid)
        _alta(a, hid, prg_padre="PRG-2026-0009", es_hito=True, horizonte="H4", fecha_resolucion=f"202{7 + i}-06-05")
        _resolver(a, hid, 1)
    _alta(a, "PRG-2026-0009", horizonte="H5", prob_interna=None, hit_ids=hits, fecha_resolucion="2036-06-05")
    _alta(a, "PRG-2026-0010", horizonte="H4")
    _resolver(a, "PRG-2026-0010", 0)
    e = Evaluador(a, None, None, {"evaluacion": {}}, None)
    assert [p["prg_id"] for p in e.resueltos("2030-01-10")] == ["PRG-2026-0010"]
    assert {k: v["n"] for k, v in e.metricas("2030-01-10").items()} == {"RV|H4": 1}
    assert e.historial_aciertos("2030-01-10", semanas=600)["global"]["n"] == 1
    assert e.revisar_certificados("2030-01-10")["insuficientes"] == {"RV|H4": "n = 1 < 100"}
    # los hitos se evalúan aparte: tasa de hitos cumplidos por tipo × H5
    h5 = e.estado_h5("2030-01-10")
    assert h5["celdas"]["RV"]["n"] == 3 and h5["celdas"]["RV"]["tasa_cumplidos"] == 1.0
    assert h5["pronosticos"]["PRG-2026-0009"]["hitos_cumplidos"] == 3


# ------------------------------------------------------------------------------------------------ CA-09 · F4 (R11)
def test_f4_congelacion_rechaza_realta_y_resoluciones_invalidas(tmp_path):
    a = Almacen(tmp_path)
    a.reloj.fijar("2026-06-05")
    _alta(a, "PRG-2026-0001", prob_interna=0.6)
    with pytest.raises(PronosticoCongelado, match="segunda ALTA"):
        _alta(a, "PRG-2026-0001", prob_interna=0.9, sentido="NEGATIVO")
    with pytest.raises(PronosticoCongelado, match="no está dado de alta"):
        _resolver(a, "PRG-2099-9999", 1)
    _resolver(a, "PRG-2026-0001", 1)
    with pytest.raises(PronosticoCongelado, match="ya está resuelto"):
        _resolver(a, "PRG-2026-0001", 0)
    assert issubclass(PronosticoCongelado, EscrituraFueraDeReserva)
    e = a.estado("F4")
    assert set(e) == {"PRG-2026-0001"} and e["PRG-2026-0001"]["prob_interna"] == 0.6
    assert e["PRG-2026-0001"]["resolucion"]["resultado_binario"] == 1 and len(e["PRG-2026-0001"]["resoluciones"]) == 1
    assert sum(1 for x in a.leer("HA") if x.get("tipo") == "ESCRITURA") == 3
    assert a.verificar_integridad("F4") == {"F4": True}
    # el índice se reconstruye al reabrir el almacén desde disco
    b = Almacen(tmp_path)
    with pytest.raises(PronosticoCongelado):
        _alta(b, "PRG-2026-0001")
    with pytest.raises(PronosticoCongelado):
        _resolver(b, "PRG-2026-0001", 0)


# ------------------------------------------------------------------------------------------------ CA-10 · bóveda
def test_boveda_caducada_se_rechaza_tambien_sin_fecha(tmp_path):
    b = hb.Boveda(tmp_path)
    r = b.depositar("API X", "VALOR-SECRETO-1", caducidad="2020-01-01")
    assert b.valor_para_herramienta(r["credencial_ref"]) is None                       # sin fecha: fecha real
    assert b.valor_para_herramienta(r["credencial_ref"], dt.date(2026, 11, 9)) is None
    assert b.estado(r["credencial_ref"])["estado"] == "CADUCADA"
    assert b.valor_para_herramienta(r["credencial_ref"], dt.date(2019, 12, 31)) == "VALOR-SECRETO-1"
    ok = b.depositar("API Y", "VALOR-SECRETO-2", caducidad="2999-12-31")
    assert b.valor_para_herramienta(ok["credencial_ref"]) == "VALOR-SECRETO-2"


@pytest.mark.parametrize("cad", ["31/12/2026", "2026-02-30", "20261231", "mañana", 20261231])
def test_boveda_caducidad_no_iso_se_rechaza_antes_de_escribir(tmp_path, cad):
    b = hb.Boveda(tmp_path)
    b.depositar("API previa", "VALOR-0", caducidad="2999-01-01")
    antes = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    with pytest.raises(ValueError):
        b.depositar("API Y", "VALOR-SECRETO-2", caducidad=cad)
    assert {p.name: p.read_bytes() for p in tmp_path.iterdir()} == antes            # nada escrito
    assert [e["estado"] for e in b.listar(dt.date(2026, 11, 9))] == ["PROVISTA"]
    assert b.estado(hb.alias_de("API Y"), dt.date(2026, 11, 9))["estado"] == "AUSENTE"


def test_boveda_indice_con_caducidad_ilegible_no_rompe_y_falla_cerrado(tmp_path):
    b = hb.Boveda(tmp_path)
    r = b.depositar("API X", "V", caducidad="2999-01-01")
    idx = json.loads((tmp_path / "indice.json").read_text(encoding="utf-8"))
    idx[r["credencial_ref"]]["caducidad"] = "31/12/2026"                               # índice heredado
    (tmp_path / "indice.json").write_text(json.dumps(idx), encoding="utf-8")
    assert [e["estado"] for e in b.listar(dt.date(2026, 11, 9))] == ["CADUCADA"]
    assert b.valor_para_herramienta(r["credencial_ref"], dt.date(2026, 11, 9)) is None


def test_boveda_secretos_con_0600_desde_el_principio_y_error_de_chmod_propagado(tmp_path, monkeypatch):
    modos = []
    real = os.chmod

    def espia(p, m):
        modos.append(stat.S_IMODE(os.stat(p).st_mode))
        real(p, m)

    monkeypatch.setattr(os, "chmod", espia)
    hb.Boveda(tmp_path / "a").depositar("API Z", "VALOR-SECRETO-3")
    assert modos and all(m == 0o600 for m in modos)                                   # nunca legible por otros
    assert stat.S_IMODE(os.stat(tmp_path / "a" / "secretos.json").st_mode) == 0o600

    def falla(p, m):
        raise OSError("chmod no permitido")

    monkeypatch.setattr(os, "chmod", falla)
    with pytest.raises(OSError, match="chmod"):
        hb.Boveda(tmp_path / "b").depositar("API Z", "VALOR-SECRETO-4")
    assert not (tmp_path / "b" / "secretos.json").exists()
    assert not [p for p in (tmp_path / "b").iterdir() if "secretos" in p.name]        # sin temporales huérfanos


# ------------------------------------------------------------------------------------------------ CA-13 · ECE = 0
def _almacen_certificado(tmp_path):
    a = Almacen(tmp_path)
    a.reloj.fijar("2027-06-04")
    for i in range(100):
        pid = f"PRG-2026-{i + 1:04d}"
        _alta(a, pid, prob_interna=0.75, fecha_emision=str((pd.Timestamp("2026-01-02") + pd.Timedelta(days=i)).date()))
        _resolver(a, pid, 1 if i % 4 else 0, "2027-06-04")
    a.escribir("F6", "AG-20", {"tipo_entrada": "CERT", "id": "CERT-2027-0001", "estado": "VIGENTE",
                               "celda": {"clase": "RV", "horizonte": "H3", "metodo": None}})
    return a


def test_ece_cero_no_revoca_un_certificado(tmp_path):
    a = _almacen_certificado(tmp_path)
    cfg = {"evaluacion": {"bootstrap_replicas": 50, "simulaciones_ece": 50}}
    e = Evaluador(a, None, None, cfg, None)
    m = ev.evaluar_celda([0.75] * 100, [1 if i % 4 else 0 for i in range(100)], [0.5] * 100, 0.5, 50, 50)
    assert m["calibracion"]["ece"] == 0.0 and m["bss"]["valor"] > 0
    assert e.revisar_certificados("2027-06-04")["revocados"] == []


def test_umbral_de_revocacion_ece_sale_de_la_configuracion(tmp_path):
    a = _almacen_certificado(tmp_path)
    cfg = {"evaluacion": {"bootstrap_replicas": 50, "simulaciones_ece": 50, "ece_revocacion": 0.0}}
    assert Evaluador(a, None, None, cfg, None).revisar_certificados("2027-06-04")["revocados"] == ["CERT-2027-0001"]


# ------------------------------------------------------------------------------------------------ CS-03 · HT-08
def test_monitor_abre_instancias_de_los_analistas_nuevos():
    assert ANALISTAS <= SIN_ESTADO and {"AG-21", "AG-22", "AG-23", "AG-24", "AG-25"} <= SIN_ESTADO
    assert not {"AG-01", "AG-02", "AG-18", "AG-19", "AG-20"} & SIN_ESTADO
    m = Monitor(umbral_cola=3, instancias_max=8)
    m.encolar("AG-21", 10)
    m.encolar("AG-20", 10)
    ordenes = {o["agente"]: o for o in m.evaluar_instancias()}
    assert ordenes["AG-21"]["tipo_entrada"] == "ORD" and ordenes["AG-21"]["accion"] == "ABRIR"
    assert ordenes["AG-21"]["instancias_despues"] > 1
    assert ordenes["AG-20"]["tipo_entrada"] == "CAR"


# ------------------------------------------------------------------------------------------------ CS-05 · bandas
def test_cinco_bandas_publicables_iguales_al_esquema():
    esquema = json.loads(ESQUEMA_PAQUETE.read_text(encoding="utf-8"))
    enum = esquema["$defs"]["vista_horizonte"]["properties"]["banda"]["enum"]
    casos = {0.85: "muy probable", 0.65: "más probable que no", 0.50: "incierto", 0.35: "poco probable",
             0.15: "muy poco probable"}
    assert {p: banda_publicable(p) for p in casos} == casos
    assert sorted(casos.values()) == sorted(enum)
    # huecos entre bandas: la más cercana a 50 % (prompt de Prospectiva, 6.5)
    assert banda_publicable(0.77) == "más probable que no" and banda_publicable(0.57) == "incierto"
    assert banda_publicable(0.42) == "incierto" and banda_publicable(0.22) == "poco probable"
    assert banda_publicable(0.97) == "muy probable" and banda_publicable(0.03) == "muy poco probable"
    # límites (intervalos cerrados del Anexo A)
    assert [banda_de(p) for p in (0.80, 0.75, 0.60, 0.55, 0.45, 0.40, 0.25, 0.20)] == [
        "MUY_PROBABLE", "MAS_PROBABLE_QUE_NO", "MAS_PROBABLE_QUE_NO", "INCIERTO", "INCIERTO", "POCO_PROBABLE",
        "POCO_PROBABLE", "MUY_POCO_PROBABLE"]
    assert PROB_DE_BANDA == {"MUY_PROBABLE": 0.85, "MAS_PROBABLE_QUE_NO": 0.65, "INCIERTO": 0.50, "POCO_PROBABLE": 0.35,
                             "MUY_POCO_PROBABLE": 0.15}
    for p in (float("nan"), None, -0.1, 1.2):
        with pytest.raises(ValueError):
            banda_publicable(p)


def test_bandas_desde_configuracion_y_validadas():
    try:
        otra = [dict(b) for b in BANDAS_VERBALES_POR_DEFECTO]
        otra[1].update(min=0.58)                                          # Más probable que no 58–75 %
        Evaluador(None, None, None, {"bandas_verbales": otra}, None)
        assert banda_publicable(0.58) == "más probable que no"
        for mala in ([{**b, "texto": "probable"} if b["codigo"] == "INCIERTO" else b for b in BANDAS_VERBALES_POR_DEFECTO],
                     [b for b in BANDAS_VERBALES_POR_DEFECTO if b["codigo"] != "INCIERTO"],
                     [{**b, "min": 0.50} if b["codigo"] == "MAS_PROBABLE_QUE_NO" else b for b in BANDAS_VERBALES_POR_DEFECTO]):
            with pytest.raises(ValueError):
                fijar_bandas(mala)
    finally:
        fijar_bandas()
    assert banda_publicable(0.58) == "incierto"


# ------------------------------------------------------------------------------------------------ CS-12 · degradación H5
def _h5_con_hitos(a: Almacen, clase: str, padre: str, cumplidos: int, fallados: int, anio: int = 2026) -> None:
    ids = []
    for i, o in enumerate([1] * cumplidos + [0] * fallados):
        hid = f"HIT-{anio}-{clase}{i + 1:04d}"
        ids.append(hid)
        _alta(a, hid, clase=clase, prg_padre=padre, es_hito=True, horizonte="H4", fecha_resolucion="2027-06-04")
        _resolver(a, hid, o, "2027-06-04")
    _alta(a, padre, clase=clase, horizonte="H5", prob_interna=None, hit_ids=ids, fecha_resolucion="2036-06-05")


def test_degradacion_h5_se_aplica_en_f6_y_f10(tmp_path):
    a = Almacen(tmp_path)
    a.reloj.fijar("2027-06-04")
    _h5_con_hitos(a, "RV", "PRG-2026-0901", 5, 15)            # 25 % con 20 hitos: degrada (RV×H5 «Sí»)
    _h5_con_hitos(a, "MP", "PRG-2026-0902", 5, 14)            # 19 hitos: muestra insuficiente
    _h5_con_hitos(a, "RF", "PRG-2026-0903", 4, 16)            # RF×H5 ya «Limitado»: hacia «No» exige tipo 3
    e = Evaluador(a, None, None, {"evaluacion": {}, "methodology_version": "5.1"}, None)
    est = e.estado_h5("2027-06-04")["celdas"]
    assert est["RV"]["degradar"] and not est["MP"]["degradar"] and est["RF"]["degradar"]
    hechos = e.aplicar_degradacion_h5("2027-06-04")
    por = {(h["tipo_entrada"], h["celda"]["clase"]): h for h in hechos}
    assert set(por) == {("AJU", "RV"), ("P3", "RF")}
    aju = por[("AJU", "RV")]
    assert (aju["parametro"], aju["de"], aju["a"]) == ("P-31", "SI", "LIMITADO")
    assert aju["methodology_version"] == {"de": "5.1", "a": "5.2"} and aju["evidencia"]["n_hitos"] == 20
    lec = a.estado("F6", clave="id")[aju["evidencia"]["lec_id"]]
    assert lec["tipo_entrada"] == "LEC" and lec["ambito"] == {"clase": "RV", "horizonte": "H5"} and len(lec["evidencia"]) == 20
    f10 = a.estado("F10")
    assert f10["P-31"]["valor_vigente"]["RV"]["H5"] == "LIMITADO" and f10["P-31"]["_historial"][-1]["autor"] == "AG-20"
    assert f10["P-31"]["valor_vigente"]["RF"]["H5"] == "LIMITADO"           # la P3 no toca F10
    assert f10["P-30"]["valor_vigente"] == "5.2" and f10["P-31"]["origen"] == aju["id"]
    p3 = por[("P3", "RF")]
    assert (p3["de"], p3["a"], p3["motivo"], p3["estado"]) == ("LIMITADO", "NO", "cambio hacia o desde «No»", "ENVIADA")
    # como mucho un escalón por celda y trimestre, y nada mientras haya una P3 pendiente de la celda
    assert e.aplicar_degradacion_h5("2027-06-25") == []
    # el trimestre siguiente, RV «Limitado» → «No» solo como propuesta de tipo 3
    a.reloj.fijar("2027-07-02")
    sig = e.aplicar_degradacion_h5("2027-07-02")
    assert [(h["tipo_entrada"], h["celda"]["clase"], h["a"]) for h in sig] == [("P3", "RV", "NO")]
    assert a.estado("F10")["P-31"]["valor_vigente"]["RV"]["H5"] == "LIMITADO"
    assert a.estado("F10")["P-30"]["valor_vigente"] == "5.2"


def test_degradacion_h5_umbral_desde_configuracion(tmp_path):
    a = Almacen(tmp_path)
    a.reloj.fijar("2027-06-04")
    _h5_con_hitos(a, "RV", "PRG-2026-0901", 5, 14)
    cfg = {"evaluacion": {"degradacion_h5_min_hitos": 19, "degradacion_h5_tasa_min": 0.30}}
    assert Evaluador(a, None, None, cfg, None).estado_h5("2027-06-04")["celdas"]["RV"]["degradar"]
    cfg = {"evaluacion": {"degradacion_h5_min_hitos": 19, "degradacion_h5_tasa_min": 0.25}}
    assert not Evaluador(a, None, None, cfg, None).estado_h5("2027-06-04")["celdas"]["RV"]["degradar"]


# ------------------------------------------------------------------------------------------------ CA-06 · cesta de RI-TB
def test_tasa_base_cesta_ignora_miembros_sin_datos_y_falla_cerrado_si_no_queda_ninguno(tmp_path):
    nuevo = pd.DataFrame({"cierre": np.linspace(1.0, 1.1, 44)}, index=pd.bdate_range("2026-09-01", "2026-10-30"))
    p = ProveedorSintetico({"EURUSD=X": "DIV", "GBPUSD=X": "DIV"}, fijos={"USDNEW=X": nuevo})
    p.fijar_as_of("2026-06-05")
    uni = pd.DataFrame({"simbolo": ["EURUSD=X", "GBPUSD=X", "USDNEW=X"], "clase": ["DIV", "DIV", "DIV"]})
    a = Almacen(tmp_path)
    a.reloj.fijar("2026-06-05")
    e = Evaluador(a, p, None, {"evaluacion": {}}, uni)
    r = e.tasa_base("EURUSD=X", "CESTA", "DIV", 20, True, "2026-06-05")
    assert 0.0 < r["valor_o_prob"] < 1.0 and r["n_ventanas"] > 5
    rc = a.estado("RC")[r["calc_id"]]
    assert any("USDNEW=X" in x for x in rc["limitaciones"])
    solo_nuevo = pd.DataFrame({"simbolo": ["USDNEW=X"], "clase": ["DIV"]})
    e2 = Evaluador(a, p, None, {"evaluacion": {}}, solo_nuevo)
    with pytest.raises(DatosNoDisponibles, match="Cesta DIV sin datos"):
        e2.tasa_base("EURUSD=X", "CESTA", "DIV", 20, True, "2026-06-05")
    assert math.isfinite(r["valor_o_prob"])
