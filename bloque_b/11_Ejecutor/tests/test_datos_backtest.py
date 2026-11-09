"""HT-01 sin anticipación (guardia as_of, proveedor CSV y sintético), selección invariante a datos futuros, backtest en
sus dos modos y `generar-sinteticos`."""
import csv
import json

import numpy as np
import pandas as pd
import pytest

from bloque_b.backtest import backtest, fechas_corte, seleccion_rapida
from bloque_b.entorno import proveedor_sintetico
from bloque_b.herramientas.ht01_datos import DatosNoDisponibles, FugaDeInformacion, ProveedorCSV, ProveedorDatos
from bloque_b.orquestacion import Coordinador

from conftest import peticion_redes


def test_guardia_as_of(hacer_cfg):
    p = proveedor_sintetico(hacer_cfg())
    with pytest.raises(RuntimeError):
        p.serie("SXNP")                               # sin fecha de corte no hay datos
    p.fijar_as_of("2024-06-28")
    s = p.cierres("SXNP")
    assert s.index.max() <= pd.Timestamp("2024-06-28")
    with pytest.raises(FugaDeInformacion):
        p.serie("SXNP", fin="2024-07-31")
    with pytest.raises(DatosNoDisponibles):
        p.cierres("NO-EXISTE")
    assert all(r["fin"] <= r["as_of"] for r in p.registro_peticiones)


def test_proveedor_csv_y_fecha_de_publicacion(tmp_path):
    fechas = pd.bdate_range("2024-01-01", "2024-03-29")
    with open(tmp_path / "MACRO.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["fecha", "cierre", "fecha_publicacion"])
        for i, f in enumerate(fechas):
            w.writerow([f.date(), 100 + i, (f + pd.Timedelta(days=30)).date()])
    p = ProveedorCSV(tmp_path)
    p.fijar_as_of("2024-03-29")
    s = p.cierres("MACRO")
    assert s.index.max() <= pd.Timestamp("2024-02-29")          # lo publicado después de as_of no se ve


def test_sinteticos_con_altas_y_bajas(hacer_cfg):
    """Los universos de ejemplo incluyen instrumentos dados de baja y de alta: sus series empiezan y terminan en esas fechas."""
    p = proveedor_sintetico(hacer_cfg())
    assert p._bajas and p._altas
    p.fijar_as_of("2026-10-30")
    s, f = next(iter(p._bajas.items()))
    assert p.cierres(s).index.max() < f
    s, f = next(iter(p._altas.items()))
    assert p.cierres(s).index.min() >= f


class ProveedorAlterado(ProveedorDatos):
    """Igual que la base hasta `corte`; después, series alteradas al azar (para probar que nada mira el futuro)."""

    def __init__(self, base, corte):
        super().__init__()
        self.base, self.corte = base, pd.Timestamp(corte)

    def simbolos(self):
        return self.base.simbolos()

    def _serie_completa(self, simbolo):
        df = self.base._serie_completa(simbolo).copy()
        m = df.index > self.corte
        rng = np.random.default_rng(abs(hash(simbolo)) % 2 ** 32)
        df.loc[m, "cierre"] = df.loc[m, "cierre"].values * rng.uniform(0.2, 5.0, m.sum())
        return df


def test_seleccion_invariante_a_datos_futuros(hacer_entorno, hacer_cfg):
    corte = "2024-06-28"
    cfg = hacer_cfg()
    base = proveedor_sintetico(cfg)
    e1 = hacer_entorno(cfg, as_of=corte, proveedor=base)
    e2 = hacer_entorno(cfg, as_of=corte, proveedor=ProveedorAlterado(proveedor_sintetico(cfg), corte))
    for t in ("RV", "FON"):
        a = seleccion_rapida(e1, "redes_electricas_europa", t, "N2", "H4")
        b = seleccion_rapida(e2, "redes_electricas_europa", t, "N2", "H4")
        assert [(x["cand_id"], x["S"], x["en_top_n"]) for x in a] == [(x["cand_id"], x["S"], x["en_top_n"]) for x in b]


def test_analisis_completo_invariante_a_datos_futuros(hacer_entorno, hacer_cfg):
    corte = "2025-03-31"
    cfg = hacer_cfg(reloj={"factor_simulado": 0.3})
    r1 = Coordinador(hacer_entorno(cfg, as_of=corte, proveedor=proveedor_sintetico(cfg))).recibir(peticion_redes())
    r2 = Coordinador(hacer_entorno(cfg, as_of=corte, proveedor=ProveedorAlterado(proveedor_sintetico(cfg), corte))).recibir(peticion_redes())
    assert r1["resumen"] == r2["resumen"]


def test_fechas_de_corte():
    assert fechas_corte("2025-01-01", "2025-03-31") == ["2025-01-31", "2025-02-28", "2025-03-31"]
    assert all(pd.Timestamp(f).weekday() == 4 for f in fechas_corte("2025-01-01", "2025-02-28", "semanal"))


def test_backtest_solo_seleccion(hacer_entorno, tmp_path):
    ent = hacer_entorno()
    sal = tmp_path / "bt1"
    res = backtest(ent, Coordinador(ent), peticion_redes(), "2024-01-01", "2024-12-31", "mensual", True, str(sal))
    assert res["modo"] == "solo_seleccion" and res["fechas"] == 12
    for t in ("RV", "FON", "RF"):
        m = res["metricas_rankings"][t]
        assert m["n_rankings"] == 12 and m["ic_rango_medio"] is not None
        assert m["certificacion_ranking"]["n_sin_solapamiento"] == 1
        assert m["certificable"] is False
    filas = list(csv.DictReader(open(sal / "rankings.csv", encoding="utf-8")))
    assert {"fecha_asof", "cand_id", "S", "en_top_n", "rent_fwd", "rent_fwd_universo", "rent_fwd_referencia_ambito"} <= set(filas[0])
    assert all(f["fecha_fin_horizonte"] > f["fecha_asof"] for f in filas)
    for n in ("series_ranking.csv", "pronosticos.csv", "consumo.csv", "metricas.json"):
        assert (sal / n).exists()


def test_backtest_completo(hacer_entorno, tmp_path):
    ent = hacer_entorno()                 # reloj normal: la política POL-BT-1 autoriza las pausas
    sal = tmp_path / "bt2"
    res = backtest(ent, Coordinador(ent), peticion_redes(), "2025-01-01", "2025-02-28", "mensual", False, str(sal))
    assert res["modo"] == "completo" and res["fechas"] == 2
    assert not res["advertencias"]
    assert ent.f10()["politica_autorizacion"][0]["regla_id"] == "POL-BT-1"
    pron = list(csv.DictReader(open(sal / "pronosticos.csv", encoding="utf-8")))
    assert pron and {p["estado"] for p in pron} <= {"RESUELTO", "ABIERTO", "NO_RESOLUBLE"}
    assert any(p["estado"] == "RESUELTO" for p in pron)
    assert (sal / "entregables_ultima_fecha").is_dir() and len(list((sal / "entregables_ultima_fecha").iterdir())) == 8   # seis entregables (V2.1); el 6.º con .md, .json y .docx
    filas = list(csv.DictReader(open(sal / "rankings.csv", encoding="utf-8")))
    assert {f["fecha_asof"] for f in filas} == {"2025-01-31", "2025-02-28"}
    # cada análisis se ejecutó en modo backtest (sin búsqueda web) y sus datos son de su fecha
    assert ent.inv.modo == "backtest"
    calc = [e for e in ent.alm.leer("RC") if e.get("tipo_entrada") == "CALC" and e.get("fecha_corte")]
    assert all(str(c["fecha_corte"])[:10] <= c["_fecha"] for c in calc)


def test_generar_sinteticos(tmp_path, hacer_cfg):
    p = proveedor_sintetico(hacer_cfg())
    rutas = p.escribir_csv(tmp_path / "datos")
    assert len(rutas) > 100
    csvp = ProveedorCSV(tmp_path / "datos")
    csvp.fijar_as_of("2026-10-30")
    p.fijar_as_of("2026-10-30")
    a, b = csvp.cierres("SXNP"), p.cierres("SXNP")
    assert len(a) == len(b) and abs(float(a.iloc[-1]) - float(b.iloc[-1])) < 1e-6


@pytest.mark.parametrize("archivo_vacio", [False, True], ids=["archivo-ausente", "sin-observaciones"])
def test_una_serie_sin_precios_no_trunca_los_otros_rankings(hacer_entorno, hacer_cfg, tmp_path, archivo_vacio):
    datos = tmp_path / "datos"
    proveedor_sintetico(hacer_cfg()).escribir_csv(datos)
    simbolo = "RV-ABBN"
    archivo = datos / f"{simbolo}.csv"
    if archivo_vacio:
        archivo.write_text("fecha,cierre\n", encoding="utf-8")
    else:
        archivo.unlink()
    ent = hacer_entorno(proveedor=ProveedorCSV(datos))
    sal = tmp_path / "evaluacion"
    res = backtest(ent, Coordinador(ent), peticion_redes(), "2025-01-01", "2025-01-31", solo_seleccion=True, salida=sal)
    assert res["fin_datos"] == "2026-10-30"
    assert res["metricas_rankings"]["RV"]["n_rankings"] == 1
    assert any(simbolo in aviso for aviso in res["advertencias"])
    with (sal / "rankings.csv").open(encoding="utf-8") as fh:
        filas = {f["simbolo"]: f for f in csv.DictReader(fh)}
    assert filas[simbolo]["evaluable"] == "False"
    assert filas[simbolo]["rent_fwd"] == ""
    assert filas["RV-ENR"]["evaluable"] == "True"
    assert float(filas["RV-ENR"]["rent_fwd"]) == pytest.approx(
        ent.motor.rentabilidad("RV-ENR", "2025-01-31", filas["RV-ENR"]["fecha_fin_horizonte"]))
