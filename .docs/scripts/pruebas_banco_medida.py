"""Pruebas del banco de medida (T-94, y su registro de experimentos desde T-99). Uso: .venv/bin/python -m pytest -q .docs/scripts/pruebas_banco_medida.py

Las unitarias usan precios construidos a mano; la de integración ejecuta el Bloque A con el cliente simulado."""
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from datetime import UTC

import banco_medida as bm

RAIZ = Path(__file__).resolve().parents[2]


def serie(valores, inicio="2026-01-01"):
    return pd.Series([float(v) for v in valores], index=pd.date_range(inicio, periods=len(valores), freq="D"))


def fin_en(dias):
    return lambda ini, h: pd.Timestamp(ini) + pd.Timedelta(days=dias)


@pytest.fixture
def mundo():
    universo = pd.DataFrame({"simbolo": ["X", "Y", "Z", "W"], "clase": ["C1", "C1", "C1", "C2"]})
    precios = {"X": serie([100, 110, 121]), "Y": serie([100, 100, 100]), "Z": serie([100, 90, 81]), "W": serie([50, 50, 50])}
    return universo, precios


def test_exceso_frente_a_la_cesta(mundo):
    universo, precios = mundo
    sel = [{"fecha_asof": "2026-01-01", "clase": "C1", "simbolo": "X", "direccion": "LARGO", "horizonte": "H"},
           {"fecha_asof": "2026-01-01", "clase": "C1", "simbolo": "Z", "direccion": "CORTO", "horizonte": "H"}]
    r = bm.evaluar(sel, precios, universo, fin_en(2))
    cesta = (0.21 + 0.0 - 0.19) / 3
    assert r[0]["resuelta"] and r[0]["exceso"] == pytest.approx(0.21 - cesta)
    assert r[1]["resuelta"] and r[1]["exceso"] == pytest.approx(-(-0.19 - cesta))


def test_sin_precio_final_queda_sin_resolver(mundo):
    universo, precios = mundo
    sel = [{"fecha_asof": "2026-01-01", "clase": "C1", "simbolo": "X", "direccion": "LARGO", "horizonte": "H"}]
    r = bm.evaluar(sel, precios, universo, fin_en(30))
    assert r[0]["resuelta"] is False and r[0]["exceso"] is None
    inf = bm.construir_informe({"titular": r, "azar": r}, {"llamadas": 0, "tokens_entrada": 0, "tokens_salida": 0,
                                                          "coste_estimado": None}, 200, 1, None, "h")
    assert inf["contendientes"]["titular"]["resueltas"] == 0 and inf["contendientes"]["titular"]["media"] is None


def test_neutral_no_se_puntua(mundo):
    universo, precios = mundo
    sel = [{"fecha_asof": "2026-01-01", "clase": "C1", "simbolo": "X", "direccion": "NEUTRAL", "horizonte": "H"}]
    assert bm.evaluar(sel, precios, universo, fin_en(2))[0]["resuelta"] is False


def test_simbolo_ausente_detiene(mundo):
    universo, precios = mundo
    sel = [{"fecha_asof": "2026-01-01", "clase": "C1", "simbolo": "NO", "direccion": "LARGO", "horizonte": "H"}]
    with pytest.raises(bm.BancoError):
        bm.evaluar(sel, precios, universo, fin_en(2))


def test_cargar_precios_falla_si_falta(tmp_path):
    with pytest.raises(bm.BancoError):
        bm.cargar_precios(tmp_path, ["NO"])


def test_momento_sin_datos_futuros():
    universo = pd.DataFrame({"simbolo": ["A", "B"], "clase": ["C", "C"]})
    base = {"A": serie([100, 101, 102, 103, 104, 105]), "B": serie([100, 100, 100, 100, 100, 100])}
    plantilla = [{"fecha_asof": "2026-01-04", "clase": "C", "simbolo": "?", "direccion": "LARGO", "horizonte": "H"}]
    elegido = bm.momento(plantilla, universo, base, ventana=2)[0]["simbolo"]
    alterado = {"A": base["A"].copy(), "B": base["B"].copy()}
    alterado["B"].iloc[4:] = 1000.0  # después del corte
    assert elegido == "A"
    assert bm.momento(plantilla, universo, alterado, ventana=2)[0]["simbolo"] == "A"


def test_azar_reproducible_y_dentro_de_la_clase(mundo):
    universo, _ = mundo
    plantilla = [{"fecha_asof": "2026-01-01", "clase": "C1", "simbolo": "X", "direccion": "LARGO", "horizonte": "H"},
                 {"fecha_asof": "2026-01-01", "clase": "C1", "simbolo": "Y", "direccion": "CORTO", "horizonte": "H"}]
    a, b = bm.azar(plantilla, universo, 7), bm.azar(plantilla, universo, 7)
    assert a == b
    assert {s["simbolo"] for s in a} <= {"X", "Y", "Z"}
    assert [s["direccion"] for s in a] == ["LARGO", "CORTO"]


def test_veredictos():
    assert bm.veredicto([-0.01, 0.02]) == "todavía no se sabe"
    assert bm.veredicto([0.001, 0.02]) == "mejor"
    assert bm.veredicto([-0.03, -0.001]) == "peor"
    d = bm.diferencia([0.05] * 30, [-0.05] * 30, 500, 3)
    assert d["veredicto"] == "mejor"


def test_informe_reproducible(mundo):
    universo, precios = mundo
    sel = [{"fecha_asof": "2026-01-01", "clase": "C1", "simbolo": s, "direccion": "LARGO", "horizonte": "H"} for s in "XYZ"]
    ev = bm.evaluar(sel, precios, universo, fin_en(2))
    consumo = {"llamadas": 3, "tokens_entrada": 300, "tokens_salida": 30, "coste_estimado": None}
    i1 = bm.construir_informe({"titular": ev, "azar": ev}, consumo, 500, 7, "aviso", "h")
    i2 = bm.construir_informe({"titular": ev, "azar": ev}, consumo, 500, 7, "aviso", "h")
    assert json.dumps(i1, sort_keys=True) == json.dumps(i2, sort_keys=True)
    assert bm.informe_md(i1, "t").startswith("**Aviso:** aviso")


def test_integracion_bloque_a(tmp_path):
    """CA-1, CA-4, CA-7 y CA-8: el banco completo sobre A con el cliente simulado, dos veces."""
    py = RAIZ / ".venv" / "bin" / "python"
    antes = subprocess.run(["git", "status", "--porcelain", "bloque_a", "bloque_b", "sistema_global/marco_comun_c"],
                           cwd=RAIZ, capture_output=True, text=True, check=True).stdout
    salidas = []
    registro = tmp_path / "registro.jsonl"   # T-99: nunca el registro del repositorio
    for i in range(2):
        out = tmp_path / f"r{i}"
        extra = ["--experimento", "EXP-" + _anio() + "-0001"] if i else []   # la segunda vez, un intento más del mismo
        r = subprocess.run([str(py), str(RAIZ / ".docs/scripts/banco_medida.py"), "a", "--desde", "2026-03-06",
                            "--hasta", "2026-04-24", "--salida", str(out), "--remuestreos", "300", "--registro", str(registro), *extra],
                           cwd=RAIZ, capture_output=True, text=True, check=False)
        assert r.returncode == 0, r.stderr
        for f in ("prerregistro.json", "informe.json", "informe.md"):
            assert (out / f).exists()
        salidas.append((out / "informe.json").read_text(encoding="utf-8"))
        assert (out / "informe.md").read_text(encoding="utf-8").startswith("**Aviso:**")
    assert salidas[0] == salidas[1]
    despues = subprocess.run(["git", "status", "--porcelain", "bloque_a", "bloque_b", "sistema_global/marco_comun_c"],
                             cwd=RAIZ, capture_output=True, text=True, check=True).stdout
    assert antes == despues
    import registro_experimentos as rx
    res = rx.Registro(registro).resumen("EXP-" + _anio() + "-0001")
    assert res["intentos"] == 2 and res["variantes"] == 1 and res["sin_resultado"] == [] and res["fuera_del_maximo"] == []
    assert set(res["veredictos"].values()) <= set(rx.VEREDICTOS) and len(res["veredictos"]) == 2


def _anio():
    from datetime import datetime
    return str(datetime.now(UTC).year)


def test_un_intento_que_falla_tambien_queda_anotado(tmp_path, monkeypatch):
    """T-99: cada intento cuenta, también el que no llega a dar resultado."""
    import argparse

    import registro_experimentos as rx

    def falla(*a, **k):
        raise bm.BancoError("sin datos para esas fechas")
    monkeypatch.setattr(bm, "titular_a", falla)
    ns = argparse.Namespace(desde="2026-03-06", hasta="2026-04-24", salida=str(tmp_path / "s"), cliente="mock", frecuencia=None,
                            clases=None, semilla=7, remuestreos=200, ventana=63, registro=str(tmp_path / "r.jsonl"),
                            experimento=None, max_variantes=1)
    with pytest.raises(bm.BancoError):
        bm.ejecutar_a(ns)
    res = rx.Registro(tmp_path / "r.jsonl").resumen("EXP-" + _anio() + "-0001")
    assert res["intentos"] == 1 and res["veredictos"] == {"1": "fallido"} and not res["adoptable"]


def test_veredicto_conjunto():
    assert bm.veredicto_conjunto({"a": {"veredicto": "mejor"}, "b": {"veredicto": "mejor"}}) == "mejor"
    assert bm.veredicto_conjunto({"a": {"veredicto": "mejor"}, "b": {"veredicto": "peor"}}) == "peor"
    assert bm.veredicto_conjunto({"a": {"veredicto": "mejor"}, "b": {"veredicto": "todavía no se sabe"}}) == "todavía no se sabe"
    assert bm.veredicto_conjunto({"a": {"veredicto": "sin datos"}}) == "todavía no se sabe"


# ---------------------------------------------------------------- ronda r02 (QA r01 NO APTO): una prueba por hallazgo

def _sel(fecha, simbolo, clase="C1", direccion="LARGO", horizonte="H"):
    return {"fecha_asof": fecha, "clase": clase, "simbolo": simbolo, "direccion": direccion, "horizonte": horizonte}


def test_h01_apuesta_repetida_cuenta_una_vez(mundo):
    universo, precios = mundo
    sel = [_sel("2026-01-01", "X"), _sel("2026-01-02", "X"), _sel("2026-01-02", "X", direccion="CORTO"), _sel("2026-01-02", "Y")]
    r = bm.evaluar(sel, precios, universo, lambda ini, h: pd.Timestamp("2026-01-03"))
    assert [f["repetida"] for f in r] == [False, True, False, False]
    assert r[1]["resuelta"] is False and r[1]["exceso"] is None and "2026-01-01" in r[1]["motivo"]
    # cerrada la ventana, la misma apuesta vuelve a contar
    r2 = bm.evaluar([_sel("2026-01-01", "X"), _sel("2026-01-02", "X")], precios, universo, fin_en(1))
    assert [f["repetida"] for f in r2] == [False, False]


def test_h01_remuestreo_por_fechas_y_efectivas():
    # dos fechas con cinco observaciones iguales cada una: por grupos hay 2 observaciones efectivas, no 10
    x = [0.01] * 5 + [0.03] * 5
    g = ["d1"] * 5 + ["d2"] * 5
    r = bm.resumen(x, 2000, 1, grupos=g)
    assert r["n"] == 10 and r["efectivas"] == 2
    # remuestrear grupos enteros: las medias posibles son 0,01, 0,02 y 0,03
    assert r["rango"] == [0.01, 0.03]
    d = bm.diferencia(x, [0.0] * 10, 500, 1, grupos_a=g, grupos_b=g)
    assert d["efectivas"] == [2, 2] and d["veredicto"] == "todavía no se sabe" and "mínimo de 10" in d["motivo"]


def test_h01_simulacion_nula_no_afirma():
    """Sin habilidad, la misma oportunidad repetida cada semana con ventanas solapadas no da veredictos firmes."""
    import random

    import numpy as np
    simbolos = [f"S{i}" for i in range(6)]
    universo = pd.DataFrame({"simbolo": simbolos, "clase": ["C"] * 6})
    fechas = pd.bdate_range("2024-01-01", "2026-12-31")
    cortes = [d.strftime("%Y-%m-%d") for d in pd.date_range("2025-03-07", periods=13, freq="7D")]
    firmes = 0
    for k in range(40):
        rng = np.random.default_rng(500 + k)
        precios = {s: pd.Series(100 * np.exp(np.cumsum(rng.normal(0, 0.01, len(fechas)))), index=fechas) for s in simbolos}
        fijos = random.Random(k).sample(simbolos, 3)
        pl = [_sel(c, s, clase="C") for c in cortes for s in fijos]
        fin = lambda ini, h: ini + pd.DateOffset(months=6)
        inf = bm.construir_informe({"titular": bm.evaluar(pl, precios, universo, fin),
                                    "azar": bm.evaluar(bm.azar(pl, universo, k), precios, universo, fin)},
                                   {"llamadas": 0, "tokens_entrada": 0, "tokens_salida": 0, "coste_estimado": None}, 300, k, None, "h")
        firmes += inf["comparaciones"]["titular_vs_azar"]["veredicto"] in ("mejor", "peor")
        assert inf["contendientes"]["titular"]["resueltas"] == 3
    assert firmes / 40 <= 0.15


def test_h02_pocas_observaciones_no_dan_veredicto():
    for n in (1, 2, 9):
        d = bm.diferencia([0.05] * n, [-0.05] * n, 300, 1)
        assert d["veredicto"] == "todavía no se sabe" and d["motivo"].startswith("pocas observaciones")
    assert bm.diferencia([0.05] * 10, [-0.05] * 10, 300, 1)["veredicto"] == "mejor"
    assert bm.diferencia([0.05] * 5, [-0.05] * 5, 300, 1, min_efectivas=5)["veredicto"] == "mejor"
    # las cotas de un veredicto (H-19)
    for kw in ({"min_efectivas": 4}, {"nivel": 0.01}, {"nivel": 0.995}):
        with pytest.raises(bm.BancoError):
            bm.diferencia([0.05] * 10, [-0.05] * 10, 300, 1, **kw)
    with pytest.raises(bm.BancoError):
        bm.diferencia([0.05] * 10, [-0.05] * 10, 1, 1)


@pytest.mark.parametrize("cierre", ["", " ", "nan", "inf", "-inf", "-5", "0", "abc"])
def test_h03_cierres_imposibles_detienen(tmp_path, cierre):
    (tmp_path / "X.csv").write_text(f"fecha,cierre\n2026-01-01,100\n2026-01-02,{cierre}\n", encoding="utf-8")
    with pytest.raises(bm.BancoError, match="cierre no válido de X el 2026-01-02"):
        bm.cargar_precios(tmp_path, ["X"])


def test_h03_columnas_y_fechas(tmp_path):
    (tmp_path / "X.csv").write_text("dia,precio\n2026-01-01,100\n", encoding="utf-8")
    with pytest.raises(bm.BancoError, match="faltan las columnas"):
        bm.cargar_precios(tmp_path, ["X"])
    (tmp_path / "Y.csv").write_text("fecha,cierre\nayer,100\n", encoding="utf-8")
    with pytest.raises(bm.BancoError, match="no es AAAA-MM-DD"):
        bm.cargar_precios(tmp_path, ["Y"])
    (tmp_path / "Z.csv").write_text("fecha,cierre,volumen\n2026-01-02,101\n2026-01-01,100\n", encoding="utf-8")
    assert list(bm.cargar_precios(tmp_path, ["Z"])["Z"]) == [100.0, 101.0]


@pytest.mark.parametrize("malo", [float("nan"), float("inf"), -1.0])
def test_h03_series_imposibles_en_evaluar_y_momento(mundo, malo):
    universo, precios = mundo
    p = dict(precios)
    p["Y"] = p["Y"].copy()
    p["Y"].iloc[2] = malo   # miembro de la cesta
    with pytest.raises(bm.BancoError, match="cierre no válido de Y"):
        bm.evaluar([_sel("2026-01-01", "X")], p, universo, fin_en(2))
    with pytest.raises(bm.BancoError, match="cierre no válido de Y"):
        bm.momento([_sel("2026-01-03", "?")], universo, p, ventana=1)
    assert bm.rentabilidad(pd.Series([100.0, malo], index=pd.date_range("2026-01-01", periods=2)), "2026-01-01", "2026-01-02") is None


def test_h03_informe_en_json_estricto(tmp_path):
    with pytest.raises(ValueError):
        bm._escribir_json(tmp_path / "x.json", {"a": float("nan")})
    with pytest.raises(bm.BancoError, match="no finito"):
        bm.resumen([0.1, float("inf")], 10, 1)


def test_h10_clase_direccion_y_simbolo(mundo):
    universo, precios = mundo
    casos = [(_sel("2026-01-01", "X", clase="OTRA"), "no está en el universo"),
             (_sel("2026-01-01", "X", direccion="largo"), "dirección"),
             (_sel("2026-01-01", "W", clase="C1"), "no es de la clase C1")]
    for s, motivo in casos:
        with pytest.raises(bm.BancoError, match=motivo):
            bm.evaluar([s], precios, universo, fin_en(2))
    tz = {k: v.tz_localize("UTC") for k, v in precios.items()}
    with pytest.raises(bm.BancoError, match="zona horaria"):
        bm.evaluar([_sel("2026-01-01", "X")], tz, universo, fin_en(2))


@pytest.mark.parametrize("kw", [{"remuestreos": 0}, {"remuestreos": -3}, {"nivel": 0}, {"nivel": 1.0}, {"nivel": 90}])
def test_h10_parametros_de_la_estadistica(kw):
    args = {"remuestreos": 10, "nivel": 0.9, **kw}
    with pytest.raises(bm.BancoError):
        bm.resumen([0.1, 0.2], args["remuestreos"], 1, nivel=args["nivel"])
    with pytest.raises(bm.BancoError):
        bm.momento([], pd.DataFrame({"simbolo": [], "clase": []}), {}, ventana=0)


@pytest.mark.parametrize("arg", [["--remuestreos", "0"], ["--ventana", "0"], ["--nivel", "1.5"], ["--min-efectivas", "0"]])
def test_h10_argumentos_de_la_linea_de_ordenes(arg):
    with pytest.raises(SystemExit):
        bm.main(["a", "--desde", "2026-03-06", "--hasta", "2026-04-24", "--salida", "x", *arg])


def test_h06_referencias_iguales_al_titular_o_se_detienen():
    universo = pd.DataFrame({"simbolo": ["A", "B", "C"], "clase": ["K"] * 3})
    precios = {"A": serie(range(100, 110)), "B": serie(range(100, 110)), "C": serie([100, 101])}
    pl = [_sel("2026-01-10", "?", clase="K"), _sel("2026-01-10", "?", clase="K"), _sel("2026-01-10", "?", clase="K")]
    with pytest.raises(bm.BancoError, match="momento no puede igualar"):
        bm.momento(pl, universo, precios, ventana=3)
    assert len(bm.momento(pl[:2], universo, precios, ventana=3)) == 2
    with pytest.raises(bm.BancoError, match="azar no puede igualar"):
        bm.azar(pl + pl[:1], universo, 7)


def test_h11_borde_del_cero_y_nivel_frente_a_un_oraculo():
    assert bm.veredicto([0.0, 0.1]) == "todavía no se sabe" and bm.veredicto([-0.1, 0.0]) == "todavía no se sabe"
    import numpy as np
    x = np.random.default_rng(1).normal(0.01, 0.05, size=200)
    se = x.std(ddof=1) / np.sqrt(len(x))
    for nivel, z in ((0.90, 1.6449), (0.80, 1.2816)):
        lo, hi = bm.resumen(list(x), 4000, 7, nivel=nivel)["rango"]
        assert abs(lo - (x.mean() - z * se)) < 0.15 * se and abs(hi - (x.mean() + z * se)) < 0.15 * se


def test_h11_momento_corto_elige_la_peor():
    universo = pd.DataFrame({"simbolo": ["A", "B", "C"], "clase": ["K"] * 3})
    precios = {"A": serie([100, 110, 120]), "B": serie([100, 100, 100]), "C": serie([100, 90, 80])}
    out = bm.momento([_sel("2026-01-03", "?", clase="K", direccion="CORTO"), _sel("2026-01-03", "?", clase="K")], universo, precios, 2)
    assert [s["simbolo"] for s in out] == ["C", "A"]


def test_h11_azar_con_semilla_por_fecha_y_clase(mundo):
    import random
    universo, _ = mundo
    fechas = [f"2026-01-{d:02d}" for d in range(1, 13)]
    out = bm.azar([_sel(f, "X") for f in fechas], universo, 7)
    esperado = [random.Random(f"7|{f}|C1").sample(["X", "Y", "Z"], k=1)[0] for f in fechas]
    assert [s["simbolo"] for s in out] == esperado


def test_h07_coste_con_cache_uc_y_coste_cero(tmp_path):
    f = tmp_path / "consumo.csv"
    f.write_text("run_id,llamadas,tokens_entrada,tokens_salida,tokens_cache_escritura,tokens_cache_lectura,uc,coste_estimado\n"
                 "R1,2,100,10,500,4000,1.5,0\nR2,1,50,5,0,1000,0.5,0\n", encoding="utf-8")
    c = bm.leer_consumo(f)
    assert c == {"llamadas": 3, "tokens_entrada": 150, "tokens_salida": 15, "tokens_cache_escritura": 500,
                 "tokens_cache_lectura": 5000, "uc": 2.0, "coste_estimado": 0.0, "filas_sin_coste": 0}
    ev = [{"resuelta": True, "exceso": 0.01, "fecha_asof": "2026-01-01"}, {"resuelta": True, "exceso": 0.02, "fecha_asof": "2026-01-02"}]
    inf = bm.construir_informe({"titular": ev, "azar": ev}, c, 200, 1, None, "h")
    assert inf["coste"]["por_seleccion_resuelta"] == {"tokens_entrada": 75.0, "tokens_cache_lectura": 2500.0, "uc": 1.0,
                                                      "coste_estimado": 0.0}
    md = bm.informe_md(inf, "t")
    assert "5000 leídos de caché" in md and "coste estimado 0.0." in md and "Por selección resuelta" in md


def test_h08_fuga_sin_veredicto_y_advertencias():
    ev = [{"resuelta": True, "exceso": 0.05, "fecha_asof": f"2026-01-{d:02d}"} for d in range(1, 21)]
    ref = [{"resuelta": True, "exceso": -0.05, "fecha_asof": f"2026-01-{d:02d}"} for d in range(1, 21)]
    consumo = {"llamadas": 0, "tokens_entrada": 0, "tokens_salida": 0, "coste_estimado": None}
    assert bm.construir_informe({"titular": ev, "azar": ref}, consumo, 200, 1, None, "h")["comparaciones"]["titular_vs_azar"]["veredicto"] == "mejor"
    inf = bm.construir_informe({"titular": ev, "azar": ref}, consumo, 200, 1, None, "h",
                               advertencias=[bm.AVISO_FUGA + ": el periodo empieza antes"], sin_veredicto="fuga")
    c = inf["comparaciones"]["titular_vs_azar"]
    assert c["veredicto"] == "todavía no se sabe" and c["motivo"] == "fuga"
    assert inf["advertencias_titular"][0].startswith(bm.AVISO_FUGA) and bm.AVISO_FUGA in bm.informe_md(inf, "t")


def test_h09_aviso_por_partes():
    ej_datos, ej_univ = bm.EJECUTOR_A / "ejemplos" / "datos_sinteticos", bm.EJECUTOR_A / "config" / "universo_ejemplo.csv"
    assert bm._aviso("mock", ej_datos, ej_univ).startswith("cliente simulado")
    a = bm._aviso("anthropic", ej_datos, ej_univ)
    assert not a.startswith("cliente simulado") and "datos sintéticos de ejemplo" in a
    assert bm._aviso("anthropic", RAIZ, RAIZ / "x.csv") is None


def _titular_falso(datos, universo, simbolos=("S1", "S4"), falla_evaluar=False):
    cortes = [d.strftime("%Y-%m-%d") for d in pd.date_range("2025-03-07", periods=13, freq="7D")]

    def f(desde, hasta, carpeta, cliente, frecuencia, clases, **kw):
        sel = [_sel(c, s, clase="C") for c in cortes for s in simbolos]
        if falla_evaluar:
            sel.append(_sel(cortes[0], "NOESTA", clase="C"))
        return {"selecciones": sel, "consumo": {"llamadas": 1, "tokens_entrada": 1, "tokens_salida": 1, "coste_estimado": None},
                "datos": datos, "universo": universo, "fecha_fin": lambda ini, h: ini + pd.DateOffset(months=6),
                "advertencias": [], "excluidos_contaminacion": 0}
    return f


@pytest.fixture
def datos_falsos(tmp_path):
    import numpy as np
    datos = tmp_path / "datos"
    datos.mkdir()
    fechas = pd.bdate_range("2024-01-01", "2026-06-30")
    rng = np.random.default_rng(3)
    sims = [f"S{i}" for i in range(8)]
    for s in sims:
        pd.DataFrame({"fecha": fechas.strftime("%Y-%m-%d"),
                      "cierre": 100 * np.exp(np.cumsum(rng.normal(0, 0.01, len(fechas))))}).to_csv(datos / f"{s}.csv", index=False)
    universo = tmp_path / "universo.csv"
    pd.DataFrame({"simbolo": sims, "clase": ["C"] * 8}).to_csv(universo, index=False)
    return datos, universo


def _ns(tmp_path, salida, semilla=7, **kw):
    import argparse
    d = {"desde": "2025-03-07", "hasta": "2025-05-30", "salida": str(tmp_path / salida), "cliente": "mock", "frecuencia": None, "clases": None,
             "semilla": semilla, "remuestreos": 200, "ventana": 63, "registro": str(tmp_path / "reg.jsonl"), "experimento": None, "max_variantes": 1}
    d.update(kw)
    return argparse.Namespace(**d)


def test_h04_otra_semilla_es_otra_variante_del_mismo_experimento(tmp_path, monkeypatch, datos_falsos):
    import registro_experimentos as rx
    monkeypatch.setattr(bm, "titular_a", _titular_falso(*datos_falsos))
    for s in (1, 2, 3):
        bm.ejecutar_a(_ns(tmp_path, f"s{s}", semilla=s))
    reg = rx.Registro(tmp_path / "reg.jsonl")
    exps = {x["exp_id"] for x in reg.anotaciones() if x["tipo"] == "PRERREGISTRO"}
    assert len(exps) == 1
    res = reg.resumen(exps.pop())
    assert res["intentos"] == 3 and res["fuera_del_maximo"] == [2, 3] and res["sin_resultado"] == []
    # otro periodo es otra variante del MISMO experimento (H-14): adelantar --desde un día no abre uno nuevo
    inf = bm.ejecutar_a(_ns(tmp_path, "p2", desde="2025-03-08"))
    assert inf["experimento"]["exp_id"] == res["exp_id"] and not inf["experimento"]["dentro_del_maximo"]
    assert not reg.adoptable(res["exp_id"]) or reg.resumen(res["exp_id"])["adoptables"] == [1]


def test_h04_experimento_ajeno_rechazado_sin_anotar(tmp_path, monkeypatch, datos_falsos):
    import registro_experimentos as rx
    monkeypatch.setattr(bm, "titular_a", _titular_falso(*datos_falsos))
    reg = rx.Registro(tmp_path / "reg.jsonl")
    ajeno = reg.prerregistrar({"hipotesis": "Otra hipótesis distinta del banco", "objeto": "RECORTE", "metrica": "otra métrica larga",
                               "datos": "otros", "desde": "2020-01-01", "hasta": "2020-02-01", "semilla": 99,
                               "criterio_exito": "otro criterio largo", "max_variantes": 1}, autor="x")["exp_id"]
    with pytest.raises(bm.BancoError, match="no es de este banco"):
        bm.ejecutar_a(_ns(tmp_path, "a", experimento=ajeno))
    assert reg.resumen(ajeno)["intentos"] == 0


def test_h04_verificar_detecta_reescrituras(tmp_path, monkeypatch, datos_falsos):
    monkeypatch.setattr(bm, "titular_a", _titular_falso(*datos_falsos))
    bm.ejecutar_a(_ns(tmp_path, "v"))
    carpeta = tmp_path / "v"
    assert bm.verificar(carpeta) == [] and bm.main(["verificar", str(carpeta)]) == 0
    pre = json.loads((carpeta / "prerregistro.json").read_text(encoding="utf-8"))
    informe = (carpeta / "informe.json").read_text(encoding="utf-8")
    # reescribir el prerregistro y recalcular su huella, y citarla en el informe: el registro lo delata
    pre["min_efectivas"] = 1
    pre["huella"] = bm.huella({k: v for k, v in pre.items() if k != "huella"})
    (carpeta / "prerregistro.json").write_text(json.dumps(pre), encoding="utf-8")
    inf = json.loads(informe)
    inf["prerregistro"] = pre["huella"]
    (carpeta / "informe.json").write_text(json.dumps(inf), encoding="utf-8")
    problemas = bm.verificar(carpeta)
    assert "el intento del registro no es de este prerregistro" in problemas
    assert "el resultado del registro no casa con el informe" in problemas
    # sin recalcular la huella, el propio prerregistro lo delata
    pre["huella"] = "0" * 64
    (carpeta / "prerregistro.json").write_text(json.dumps(pre), encoding="utf-8")
    assert any("se reescribió" in p for p in bm.verificar(carpeta)) and bm.main(["verificar", str(carpeta)]) == 2


def test_h05_fallo_despues_del_titular_queda_anotado(tmp_path, monkeypatch, datos_falsos):
    import registro_experimentos as rx
    monkeypatch.setattr(bm, "titular_a", _titular_falso(*datos_falsos, falla_evaluar=True))
    with pytest.raises(bm.BancoError, match="NOESTA"):
        bm.ejecutar_a(_ns(tmp_path, "f"))
    reg = rx.Registro(tmp_path / "reg.jsonl")
    exp = next(x["exp_id"] for x in reg.anotaciones() if x["tipo"] == "PRERREGISTRO")
    res = reg.resumen(exp)
    assert res["sin_resultado"] == [] and res["veredictos"] == {"1": "fallido"}

    def revienta(*a, **k):
        raise KeyError("columna")
    monkeypatch.setattr(bm, "evaluar", revienta)
    monkeypatch.setattr(bm, "titular_a", _titular_falso(*datos_falsos))
    with pytest.raises(KeyError):
        bm.ejecutar_a(_ns(tmp_path, "g"))
    assert rx.Registro(tmp_path / "reg.jsonl").resumen(exp)["veredictos"]["2"] == "fallido"


def test_h11_informe_cita_la_huella_del_prerregistro(tmp_path, monkeypatch, datos_falsos):
    monkeypatch.setattr(bm, "titular_a", _titular_falso(*datos_falsos))
    inf = bm.ejecutar_a(_ns(tmp_path, "h", registro=None))
    pre = json.loads((tmp_path / "h" / "prerregistro.json").read_text(encoding="utf-8"))
    assert inf["prerregistro"] == pre["huella"] == bm.huella({k: v for k, v in pre.items() if k != "huella"})
    assert not (tmp_path / "h" / "experimento.json").exists()


# ---------------------------------------------------------------- ronda r03 (QA r02 NO APTO): una prueba por hallazgo

def test_h13_solo_fechas_sin_solape():
    filas = [{"fecha_asof": d, "fecha_fin": f, "resuelta": True, "exceso": 0.01}
             for d, f in (("2026-01-01", "2026-01-10"), ("2026-01-05", "2026-01-14"), ("2026-01-10", "2026-01-19"),
                          ("2026-01-12", "2026-01-21"), ("2026-01-19", "2026-01-28"))]
    assert bm.fechas_sin_solape(filas) == {"2026-01-01", "2026-01-10", "2026-01-19"}
    # la ventana más larga de una fecha manda
    filas.insert(2, {"fecha_asof": "2026-01-10", "fecha_fin": "2026-01-25", "resuelta": True, "exceso": 0.0})
    assert bm.fechas_sin_solape(filas) == {"2026-01-01", "2026-01-10"}
    inf = bm.construir_informe({"titular": filas, "azar": filas}, {"llamadas": 0, "tokens_entrada": 0, "tokens_salida": 0,
                                                                  "coste_estimado": None}, 200, 1, None, "h")
    t = inf["contendientes"]["titular"]
    assert t["fuera_de_muestra"] == 3 and t["resueltas"] == 3 and t["efectivas"] == 2
    assert inf["fechas_en_muestra"] == ["2026-01-01", "2026-01-10"]


def test_h13_ventanas_solapadas_sobre_activos_distintos_no_suman_fechas():
    """Un titular que elige cada semana un activo distinto con ventanas de 26 semanas: en un año caben dos fechas."""
    import numpy as np
    sims = [f"S{i}" for i in range(30)]
    universo = pd.DataFrame({"simbolo": sims, "clase": ["C"] * 30})
    fechas = pd.date_range("2024-01-05", periods=150, freq="7D")
    rng = np.random.default_rng(1)
    precios = {s: pd.Series(100 * np.exp(np.cumsum(rng.normal(0, 0.02, len(fechas)))), index=fechas) for s in sims}
    cortes = list(fechas[:52])
    pl = [_sel(c.strftime("%Y-%m-%d"), sims[i % 30], clase="C") for i, c in enumerate(cortes)]
    fin = lambda ini, h: ini + pd.Timedelta(weeks=26)
    ev = bm.evaluar(pl, precios, universo, fin)
    assert sum(f["resuelta"] for f in ev) == 52
    inf = bm.construir_informe({"titular": ev, "azar": bm.evaluar(bm.azar(pl, universo, 3), precios, universo, fin)},
                               {"llamadas": 0, "tokens_entrada": 0, "tokens_salida": 0, "coste_estimado": None}, 200, 1, None, "h")
    assert inf["contendientes"]["titular"]["efectivas"] == 2
    assert inf["comparaciones"]["titular_vs_azar"]["veredicto"] == "todavía no se sabe"


def test_h14_simulado_y_real_son_experimentos_distintos(tmp_path, monkeypatch, datos_falsos):
    import registro_experimentos as rx
    monkeypatch.setattr(bm, "titular_a", _titular_falso(*datos_falsos))
    a = bm.ejecutar_a(_ns(tmp_path, "m"))
    b = bm.ejecutar_a(_ns(tmp_path, "r", cliente="anthropic"))
    assert a["experimento"]["exp_id"] != b["experimento"]["exp_id"]
    assert a["experimento"]["dentro_del_maximo"] and b["experimento"]["dentro_del_maximo"]
    assert any("1 experimento(s) más con esta misma hipótesis" in x for x in b["advertencias_titular"])
    assert not any("misma hipótesis" in x for x in a["advertencias_titular"])
    reg = rx.Registro(tmp_path / "reg.jsonl")
    with pytest.raises(bm.BancoError, match="no casan"):
        bm.ejecutar_a(_ns(tmp_path, "x", cliente="anthropic", experimento=a["experimento"]["exp_id"]))
    assert reg.resumen(a["experimento"]["exp_id"])["intentos"] == 1


def test_h15_verificar_sin_registro_md_y_experimento_danado(tmp_path, monkeypatch, datos_falsos):
    monkeypatch.setattr(bm, "titular_a", _titular_falso(*datos_falsos))
    bm.ejecutar_a(_ns(tmp_path, "v"))
    c = tmp_path / "v"
    assert bm.verificar(c) == []
    md = (c / "informe.md").read_text(encoding="utf-8")
    (c / "informe.md").write_text(md.replace("todavía no se sabe", "mejor"), encoding="utf-8")
    assert "informe.md no es el que sale de informe.json" in bm.verificar(c)
    (c / "informe.md").write_text(md, encoding="utf-8")
    exp = (c / "experimento.json").read_text(encoding="utf-8")
    (c / "experimento.json").write_text("{roto", encoding="utf-8")
    assert any("no se puede leer el experimento" in p for p in bm.verificar(c))
    (c / "experimento.json").unlink()
    inf = json.loads((c / "informe.json").read_text(encoding="utf-8"))
    for comp in inf["comparaciones"].values():
        comp["veredicto"] = "mejor"
    (c / "informe.json").write_text(json.dumps(inf), encoding="utf-8")
    problemas = bm.verificar(c)
    assert any("no hay experimento.json" in p for p in problemas) and bm.main(["verificar", str(c)]) == 2
    (c / "experimento.json").write_text(exp, encoding="utf-8")
    assert "el resultado del registro no casa con el informe" in bm.verificar(c)


@pytest.mark.parametrize("contenido,motivo", [
    ("fecha,cierre\n03/02/2026,100\n", "no es AAAA-MM-DD"),
    ("fecha,cierre\n2026-01-01,100\n2026/01/02,101\n", "no es AAAA-MM-DD"),
    ("fecha,cierre\n2026-01-01,100\n2026-01-01,101\n", "fecha repetida"),
    ("fecha,cierre,cierre\n2026-01-01,100,101\n", "columnas repetidas"),
    ("fecha,cierre\n", "no tiene filas"),
    ("", "no se puede leer"),
])
def test_h16_csv_raros(tmp_path, contenido, motivo):
    (tmp_path / "X.csv").write_text(contenido, encoding="utf-8")
    with pytest.raises(bm.BancoError, match=motivo):
        bm.cargar_precios(tmp_path, ["X"])


def test_h17_orden_canonico_fechas_normalizadas_horizonte_y_universo():
    universo = pd.DataFrame({"simbolo": ["X", "Y"], "clase": ["C1", "C1"]})
    precios = {"X": serie(range(100, 120)), "Y": serie([100] * 20)}
    fin = lambda ini, h: ini + pd.Timedelta(days={"H1": 2, "H2": 5}[h])
    a = [_sel("2026-01-01", "X", horizonte="H2"), _sel("2026-01-01", "X", horizonte="H1")]
    ra, rb = bm.evaluar(a, precios, universo, fin), bm.evaluar(list(reversed(a)), precios, universo, fin)
    contada = lambda r: [f["horizonte"] for f in r if not f["repetida"]]
    assert contada(ra) == contada(rb) == ["H1"]
    r = bm.evaluar([_sel("2026-01-01", "X"), {**_sel("2026-01-01 00:00:00", "Y")}], precios, universo, fin_en(2))
    assert {f["fecha_corte"] for f in r} == {"2026-01-01"}
    inf = bm.construir_informe({"titular": r, "azar": r}, {"llamadas": 0, "tokens_entrada": 0, "tokens_salida": 0,
                                                          "coste_estimado": None}, 200, 1, None, "h")
    assert inf["contendientes"]["titular"]["efectivas"] == 1
    a_mano = [{"fecha_asof": d, "resuelta": True, "exceso": 0.01} for d in ("2026-01-01", "2026-01-01 00:00:00", "2026-01-02")]
    inf = bm.construir_informe({"titular": a_mano, "azar": a_mano}, {"llamadas": 0, "tokens_entrada": 0, "tokens_salida": 0,
                                                                    "coste_estimado": None}, 200, 1, None, "h")
    assert inf["contendientes"]["titular"]["efectivas"] == 2 and inf["fechas_en_muestra"] == ["2026-01-01", "2026-01-02"]
    with pytest.raises(bm.BancoError, match="sin fecha de resolución"):
        bm.evaluar([_sel("2026-01-01", "X", horizonte="H9")], precios, universo, fin)
    with pytest.raises(bm.BancoError, match="no es posterior"):
        bm.evaluar([_sel("2026-01-01", "X")], precios, universo, fin_en(0))
    doble = pd.DataFrame({"simbolo": ["X", "X", "Y"], "clase": ["C1", "C1", "C1"]})
    for f in (lambda: bm.evaluar([_sel("2026-01-01", "X")], precios, doble, fin_en(2)), lambda: bm.azar(a, doble, 1),
              lambda: bm.momento(a, doble, precios, 2)):
        with pytest.raises(bm.BancoError, match="duplicado"):
            f()
    with pytest.raises(bm.BancoError, match="no hay consumo.csv"):
        bm.leer_consumo(Path("/no/existe/consumo.csv"))


@pytest.mark.parametrize("valor", ["nan", "inf", "-3", "abc"])
def test_h18_consumo_imposible_detiene(tmp_path, valor):
    f = tmp_path / "consumo.csv"
    f.write_text(f"llamadas,tokens_entrada,tokens_salida,uc,coste_estimado\n1,{valor},1,0.1,0.2\n", encoding="utf-8")
    with pytest.raises(bm.BancoError, match="tokens_entrada"):
        bm.leer_consumo(f)


def test_h18_coste_parcial_semilla_y_registro_roto(tmp_path, monkeypatch, datos_falsos):
    f = tmp_path / "consumo.csv"
    f.write_text("llamadas,tokens_entrada,tokens_salida,coste_estimado\n1,10,1,0.5\n1,10,1,\n", encoding="utf-8")
    c = bm.leer_consumo(f)
    assert c["coste_estimado"] is None and c["filas_sin_coste"] == 1
    inf = bm.construir_informe({"titular": [], "azar": []}, c, 200, 1, None, "h")
    assert "1 filas de consumo.csv sin coste" in bm.informe_md(inf, "t")
    monkeypatch.setattr(bm, "titular_a", _titular_falso(*datos_falsos))
    with pytest.raises(bm.BancoError, match="semilla"):
        bm.ejecutar_a(_ns(tmp_path, "s", semilla=-1))
    (tmp_path / "roto.jsonl").write_text("no es json\n", encoding="utf-8")
    with pytest.raises(bm.BancoError, match="registro de experimentos"):
        bm.ejecutar_a(_ns(tmp_path, "r", registro=str(tmp_path / "roto.jsonl")))


@pytest.mark.parametrize("kw", [{"remuestreos": 1}, {"remuestreos": 199}, {"nivel": 0.5}, {"nivel": 0.995}, {"min_efectivas": 1},
                                {"min_efectivas": 4}])
def test_h19_cotas_de_un_experimento(tmp_path, monkeypatch, datos_falsos, kw):
    import registro_experimentos as rx
    monkeypatch.setattr(bm, "titular_a", _titular_falso(*datos_falsos))
    with pytest.raises(bm.BancoError):
        bm.ejecutar_a(_ns(tmp_path, "c", **kw))
    assert rx.Registro(tmp_path / "reg.jsonl").anotaciones() == []


@pytest.mark.parametrize("arg", [["--remuestreos", "1"], ["--nivel", "0.01"], ["--min-efectivas", "1"], ["--semilla", "-1"]])
def test_h19_cotas_en_la_linea_de_ordenes(arg):
    with pytest.raises(SystemExit):
        bm.main(["a", "--desde", "2026-03-06", "--hasta", "2026-04-24", "--salida", "x", *arg])


def test_h20_la_repetida_no_alarga_la_ventana_y_el_orden_de_entrada_da_igual():
    universo = pd.DataFrame({"simbolo": ["X", "Y"], "clase": ["C1", "C1"]})
    precios = {"X": serie(range(100, 120)), "Y": serie([100] * 20)}
    sel = [_sel("2026-01-01", "X"), _sel("2026-01-02", "X"), _sel("2026-01-03", "X")]
    for orden in (sel, list(reversed(sel))):
        r = sorted(bm.evaluar(orden, precios, universo, fin_en(2)), key=lambda f: f["fecha_asof"])
        assert [f["repetida"] for f in r] == [False, True, False]


def test_h20_minimo_mira_el_lado_con_menos_fechas():
    a = [0.05] * 12
    d = bm.diferencia(a, [-0.05] * 3, 200, 1, grupos_a=[str(i) for i in range(12)], grupos_b=["0", "1", "2"])
    assert d["efectivas"] == [12, 3] and d["veredicto"] == "todavía no se sabe"


def _titular_con_fuga(datos, universo):
    base = _titular_falso(datos, universo, simbolos=("S1",))

    def f(*a, **k):
        t = base(*a, **k)
        cortes = [d.strftime("%Y-%m-%d") for d in pd.date_range("2018-01-05", periods=400, freq="7D")]
        t["selecciones"] = [_sel(c, "S1", clase="C") for c in cortes]
        t["fecha_fin"] = lambda ini, h: ini + pd.Timedelta(days=7)
        t["advertencias"] = [bm.AVISO_FUGA + ": el periodo empieza antes de la fecha de corte configurada"]
        return t
    return f


@pytest.fixture
def datos_largos(tmp_path):
    import numpy as np
    datos = tmp_path / "largos"
    datos.mkdir()
    fechas = pd.bdate_range("2017-06-01", "2026-06-30")
    for s, deriva in (("S0", -0.004), ("S1", 0.004), ("S2", -0.004)):   # S1 gana siempre: veredicto firme sin fuga
        pd.DataFrame({"fecha": fechas.strftime("%Y-%m-%d"),
                      "cierre": 100 * np.exp(np.cumsum(np.full(len(fechas), deriva)))}).to_csv(datos / f"{s}.csv", index=False)
    universo = tmp_path / "u_largo.csv"
    pd.DataFrame({"simbolo": ["S0", "S1", "S2"], "clase": ["C"] * 3}).to_csv(universo, index=False)
    return datos, universo


def test_h20_fuga_con_cliente_real_quita_el_veredicto_y_con_el_simulado_no(tmp_path, monkeypatch, datos_largos):
    monkeypatch.setattr(bm, "titular_a", _titular_con_fuga(*datos_largos))
    mock = bm.ejecutar_a(_ns(tmp_path, "m", registro=None))
    real = bm.ejecutar_a(_ns(tmp_path, "r", registro=None, cliente="anthropic"))
    firmes = [k for k, c in mock["comparaciones"].items() if c["veredicto"] in ("mejor", "peor")]
    assert firmes   # con el simulado, la fuga no quita el veredicto
    for k in firmes:
        c = real["comparaciones"][k]
        assert c["veredicto"] == "todavía no se sabe" and "fecha de corte del modelo" in c["motivo"]


def test_h20_fuga_tambien_quita_un_peor():
    ev = [{"resuelta": True, "exceso": -0.05, "fecha_asof": f"2026-01-{d:02d}"} for d in range(1, 21)]
    ref = [{"resuelta": True, "exceso": 0.05, "fecha_asof": f"2026-01-{d:02d}"} for d in range(1, 21)]
    consumo = {"llamadas": 0, "tokens_entrada": 0, "tokens_salida": 0, "coste_estimado": None}
    assert bm.construir_informe({"titular": ev, "azar": ref}, consumo, 200, 1, None, "h")["comparaciones"]["titular_vs_azar"]["veredicto"] == "peor"
    inf = bm.construir_informe({"titular": ev, "azar": ref}, consumo, 200, 1, None, "h", sin_veredicto="fuga")
    assert inf["comparaciones"]["titular_vs_azar"]["veredicto"] == "todavía no se sabe"


def test_h20_no_queda_el_experimento_de_una_ejecucion_anterior(tmp_path, monkeypatch, datos_falsos):
    monkeypatch.setattr(bm, "titular_a", _titular_falso(*datos_falsos))
    bm.ejecutar_a(_ns(tmp_path, "e"))
    assert (tmp_path / "e" / "experimento.json").exists()
    bm.ejecutar_a(_ns(tmp_path, "e", registro=None))
    assert not (tmp_path / "e" / "experimento.json").exists()


# ---------------------------------------------------------------- T-99 r02 (QA r01, H-08): la interfaz del banco con el registro

def test_t99_h08_registro_vacio_y_sin_registro(tmp_path, monkeypatch, datos_falsos):
    monkeypatch.setattr(bm, "titular_a", _titular_falso(*datos_falsos))
    with pytest.raises(bm.BancoError, match="--sin-registro"):
        bm.ejecutar_a(_ns(tmp_path, "v", registro=""))
    inf = bm.ejecutar_a(_ns(tmp_path, "s", registro=None))   # --sin-registro deja registro=None: no se anota, y se dice
    assert "experimento" not in inf and any("no hay experimento.json" in p for p in bm.verificar(tmp_path / "s"))


def test_t99_h08_max_variantes_no_cambia_despues(tmp_path, monkeypatch, datos_falsos):
    monkeypatch.setattr(bm, "titular_a", _titular_falso(*datos_falsos))
    exp = bm.ejecutar_a(_ns(tmp_path, "a"))["experimento"]["exp_id"]
    with pytest.raises(bm.BancoError, match="max_variantes 1"):
        bm.ejecutar_a(_ns(tmp_path, "b", max_variantes=5))
    with pytest.raises(bm.BancoError, match="max_variantes 1"):
        bm.ejecutar_a(_ns(tmp_path, "c", max_variantes=5, experimento=exp))


def test_t99_h08_fallo_al_escribir_el_prerregistro_queda_fallido(tmp_path, monkeypatch, datos_falsos):
    import registro_experimentos as rx
    monkeypatch.setattr(bm, "titular_a", _titular_falso(*datos_falsos))
    real = bm._escribir_json

    def falla(ruta, obj):
        if Path(ruta).name == "prerregistro.json":
            raise OSError("disco lleno")
        real(ruta, obj)
    monkeypatch.setattr(bm, "_escribir_json", falla)
    with pytest.raises(OSError):
        bm.ejecutar_a(_ns(tmp_path, "p"))
    reg = rx.Registro(tmp_path / "reg.jsonl")
    exp = next(x["exp_id"] for x in reg.anotaciones() if x["tipo"] == "PRERREGISTRO")
    assert reg.resumen(exp)["veredictos"] == {"1": "fallido"} and reg.resumen(exp)["sin_resultado"] == []


def test_t99_h08_registro_roto_a_mitad_sale_como_bancoerror(tmp_path, monkeypatch, datos_falsos):
    import registro_experimentos as rx
    monkeypatch.setattr(bm, "titular_a", _titular_falso(*datos_falsos))

    def roto(self, *a, **k):
        raise rx.RegistroError("cadena rota en la anotación 3")
    monkeypatch.setattr(rx.Registro, "resultado", roto)
    with pytest.raises(bm.BancoError, match="registro de experimentos"):
        bm.ejecutar_a(_ns(tmp_path, "r"))
    monkeypatch.setattr(bm, "evaluar", lambda *a, **k: (_ for _ in ()).throw(ValueError("fallo original")))
    with pytest.raises(bm.BancoError, match="fallo original.*no se pudo anotar"):
        bm.ejecutar_a(_ns(tmp_path, "s", semilla=8))   # otra variante: la anterior quedó con su intento abierto


def test_t99_h24_rutas_publicas_sin_carpetas_de_la_maquina(tmp_path):
    fuera = bm._ruta_publica(tmp_path / "datos")
    assert fuera.startswith("«externa»/datos (") and str(tmp_path) not in fuera
    assert bm._ruta_publica(RAIZ / "bloque_a" / "11_Ejecutor") == "bloque_a/11_Ejecutor"
