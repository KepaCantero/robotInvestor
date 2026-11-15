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
                            clases=None, semilla=7, remuestreos=10, ventana=63, registro=str(tmp_path / "r.jsonl"),
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
    d = bm.diferencia(x, [0.0] * 10, 500, 1, grupos_a=g, grupos_b=g, min_efectivas=3)
    assert d["efectivas"] == [2, 2] and d["veredicto"] == "todavía no se sabe" and "mínimo de 3" in d["motivo"]


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
    assert bm.diferencia([0.05], [-0.05], 300, 1, min_efectivas=1)["veredicto"] == "mejor"


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
    with pytest.raises(bm.BancoError, match="fecha ilegible"):
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
                 "tokens_cache_lectura": 5000, "uc": 2.0, "coste_estimado": 0.0}
    ev = [{"resuelta": True, "exceso": 0.01, "fecha_asof": "2026-01-01"}, {"resuelta": True, "exceso": 0.02, "fecha_asof": "2026-01-02"}]
    inf = bm.construir_informe({"titular": ev, "azar": ev}, c, 50, 1, None, "h")
    assert inf["coste"]["por_seleccion_resuelta"] == {"tokens_entrada": 75.0, "tokens_cache_lectura": 2500.0, "uc": 1.0,
                                                      "coste_estimado": 0.0}
    md = bm.informe_md(inf, "t")
    assert "5000 leídos de caché" in md and "coste estimado 0.0." in md and "Por selección resuelta" in md


def test_h08_fuga_sin_veredicto_y_advertencias():
    ev = [{"resuelta": True, "exceso": 0.05, "fecha_asof": f"2026-01-{d:02d}"} for d in range(1, 21)]
    ref = [{"resuelta": True, "exceso": -0.05, "fecha_asof": f"2026-01-{d:02d}"} for d in range(1, 21)]
    consumo = {"llamadas": 0, "tokens_entrada": 0, "tokens_salida": 0, "coste_estimado": None}
    assert bm.construir_informe({"titular": ev, "azar": ref}, consumo, 100, 1, None, "h")["comparaciones"]["titular_vs_azar"]["veredicto"] == "mejor"
    inf = bm.construir_informe({"titular": ev, "azar": ref}, consumo, 100, 1, None, "h",
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
             "semilla": semilla, "remuestreos": 100, "ventana": 63, "registro": str(tmp_path / "reg.jsonl"), "experimento": None, "max_variantes": 1}
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
    # otro periodo es otro experimento, y el informe avisa de que ya hay otro con la misma hipótesis
    inf = bm.ejecutar_a(_ns(tmp_path, "p2", desde="2025-03-14"))
    assert inf["experimento"]["exp_id"] != res["exp_id"]
    bm.ejecutar_a(_ns(tmp_path, "p3", desde="2025-03-21"))
    inf = json.loads((tmp_path / "p3" / "informe.json").read_text(encoding="utf-8"))
    assert any("experimentos con esta misma hipótesis" in a for a in inf["advertencias_titular"])


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
