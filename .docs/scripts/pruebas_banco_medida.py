"""Pruebas del banco de medida (T-94, y su registro de experimentos desde T-99). Uso: .venv/bin/python -m pytest -q .docs/scripts/pruebas_banco_medida.py

Las unitarias usan precios construidos a mano; la de integración ejecuta el Bloque A con el cliente simulado."""
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
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
    from datetime import datetime, timezone
    return str(datetime.now(timezone.utc).year)


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
