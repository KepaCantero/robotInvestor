"""T-65 · Correcciones de la QA r02 de T-65 (`.docs/tickets/T-65/qa.md`, «Ronda r02»): H-12, H-13 y H-14.

Cada prueba falla con el commit 052e79a (ver `.docs/tickets/T-65/pruebas.md`). H-15 (refs_vivas) se prueba en
`.docs/scripts/prueba_refs_vivas.py`.
"""
import shutil
from pathlib import Path

import pandas as pd
import pytest
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
from bloque_a.herramientas.ht01_datos import (
    DatosInvalidos,
    ProveedorCSV,
    cargar_universo,
)
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
from conftest import AS_OF, DATOS, config_pruebas

LINEA_NUEVA = "USDNEW=X,DIV,Dólar frente a nueva divisa,ESTRATEGIA,GLB,G10,USD,SOLO EJEMPLO,Pares,Par nuevo,Otros cruces,USD/NEW,\n"
FECHAS = list(pd.bdate_range("2023-01-02", AS_OF))


def _bloque(tmp_path, datos=DATOS, universo=RUTA_UNIVERSO_EJEMPLO):
    return Bloque(config_pruebas(), ProveedorCSV(datos), cargar_universo(universo), MockClient(),
                  Path(tmp_path) / "estado", Path(tmp_path) / "ent")


def _datos(tmp_path) -> Path:
    datos = tmp_path / "datos"
    shutil.copytree(DATOS, datos)
    return datos


def _limitaciones(r) -> str:
    return " ".join(r["paquete"]["limitaciones"])


# ---------------------------------------------------------------- H-12 · índice de referencia con datos malos
def _acwi_cero(datos: Path) -> None:
    df = pd.read_csv(datos / "ACWI.csv")
    df.loc[df["fecha"] == "2026-05-29", "cierre"] = 0
    df.to_csv(datos / "ACWI.csv", index=False)


def _acwi_binario(datos: Path) -> None:
    (datos / "ACWI.csv").write_bytes(bytes(range(256)) * 20)


def _acwi_ausente(datos: Path) -> None:
    (datos / "ACWI.csv").unlink()


@pytest.mark.parametrize("estropear", [_acwi_cero, _acwi_binario, _acwi_ausente], ids=["cero", "binario", "ausente"])
def test_r02_h12_referencia_mala_degrada_solo_los_tipos_que_la_usan(tmp_path, estropear):
    datos = _datos(tmp_path)
    estropear(datos)                                                 # ACWI: referencia de RV y de IDX (indices_referencia)
    b = _bloque(tmp_path, datos=datos)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV", "IDX", "DIV"]})      # 052e79a: el ciclo entero caía
    assert r["estado"] == "PARCIAL"
    assert r["paquete"]["clases"]["DIV"]["opciones"]                 # el tipo que no usa ACWI sigue
    for c in ("RV", "IDX"):
        assert not (r["paquete"]["clases"].get(c) or {}).get("opciones")        # nada calculado con la referencia mala
    lim = _limitaciones(r)
    assert "referencia de comparación ACWI" in lim
    assert "Renta variable" in lim and "Índices bursátiles" in lim
    incs = [x for x in b.almacen.leer("HA") if x.get("tipo") == "DATOS" and x.get("objeto") == "ACWI"]
    assert len(incs) == 2 and {x["run_id"] for x in incs} == {r["run_id"]}  # una por tipo afectado


def test_r02_h12_referencia_sana_no_cambia_nada(tmp_path):
    b = _bloque(tmp_path)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert r["paquete"]["clases"]["RV"]["opciones"]
    assert "referencia de comparación" not in _limitaciones(r)
    assert not [x for x in b.almacen.leer("HA") if x.get("tipo") == "DATOS"]


def test_r02_h12_subyacente_malo_excluye_solo_su_indicador(tmp_path, monkeypatch):
    b = _bloque(tmp_path)
    b.fijar_fecha(AS_OF)
    uni = b.universo[b.universo["clase"] == "DER"]
    fila = uni[uni["subyacente"].astype(str).str.strip() != ""].iloc[0]
    simbolo, sub = fila["simbolo"], str(fila["subyacente"]).strip()
    cierres = b.proveedor.cierres

    def malo(s, *a, **kw):
        if s == sub:
            raise DatosInvalidos(f"HT-01: cierre no positivo simulado de {sub}")
        return cierres(s, *a, **kw)
    monkeypatch.setattr(b.proveedor, "cierres", malo)
    senales, _ = b.senales_clase("DER", AS_OF, "RUN-2026-0001")
    assert simbolo not in senales and simbolo in b._datos_invalidos[("DER", "RUN-2026-0001")]


# ---------------------------------------------------------------- H-13 · formas raras de CSV, dato inválido del símbolo
CSV_RAROS = {
    "yahoo_close_y_adj_close": "Date,Open,High,Low,Close,Adj Close,Volume\n" + "".join(
        f"{d.date()},1,1,1,1.0{i % 9},1.0{i % 9},100\n" for i, d in enumerate(FECHAS)),
    "fechas_con_zona": "fecha,cierre\n" + "".join(f"{d.date()} 00:00:00-04:00,1.0{i % 9}\n" for i, d in enumerate(FECHAS)),
    "publicacion_con_zona": "fecha,cierre,fecha_publicacion\n" + "".join(
        f"{d.date()},1.0{i % 9},{d.date()}T18:00:00+02:00\n" for i, d in enumerate(FECHAS)),
}


@pytest.mark.parametrize("caso", sorted(CSV_RAROS))
def test_r02_h13_csv_raro_es_dato_invalido_del_simbolo(tmp_path, caso):
    datos = _datos(tmp_path)
    (datos / "USDNEW=X.csv").write_text(CSV_RAROS[caso], encoding="utf-8")
    p = ProveedorCSV(datos)
    p.fijar_as_of(AS_OF)
    with pytest.raises(DatosInvalidos):                               # 052e79a: AttributeError o TypeError
        p.cierres("USDNEW=X")
    (tmp_path / "u.csv").write_text(Path(RUTA_UNIVERSO_EJEMPLO).read_text(encoding="utf-8").rstrip("\n") + "\n" + LINEA_NUEVA,
                                    encoding="utf-8")
    b = _bloque(tmp_path, datos=datos, universo=tmp_path / "u.csv")
    r = b.ciclo(AS_OF, alcance={"clases": ["DIV", "RV"]})             # 052e79a: caía el ciclo (tasa base de la CESTA)
    assert r["paquete"]["clases"]["DIV"]["opciones"] and r["paquete"]["clases"]["RV"]["opciones"]
    assert b._datos_invalidos[("DIV", r["run_id"])] == ["USDNEW=X"]
    assert "datos HT-01 inválidos" in _limitaciones(r)


def test_r02_h13_cualquier_error_de_la_normalizacion_es_dato_invalido(tmp_path, monkeypatch):
    from bloque_a.herramientas import ht01_datos
    (tmp_path / "X.csv").write_text("fecha,cierre\n2026-06-01,1\n", encoding="utf-8")

    def rompe(df, origen):
        raise AttributeError("forma inesperada")
    monkeypatch.setattr(ht01_datos, "_normalizar_df_sin_envolver", rompe)
    p = ProveedorCSV(tmp_path)
    p.fijar_as_of(AS_OF)
    with pytest.raises(DatosInvalidos, match="AttributeError"):
        p.cierres("X")


# ---------------------------------------------------------------- H-14 · un cierre booleano no es un precio
@pytest.mark.parametrize("valor", ["True", "False"])
def test_r02_h14_cierre_booleano_se_rechaza(tmp_path, valor):
    (tmp_path / "B.csv").write_text("fecha,cierre\n" + "".join(f"{d.date()},{valor}\n" for d in FECHAS[-10:]),
                                    encoding="utf-8")
    p = ProveedorCSV(tmp_path)
    p.fijar_as_of(AS_OF)
    with pytest.raises(DatosInvalidos, match="booleanos"):           # 052e79a: precio constante de 1 (o 0)
        p.cierres("B")


# ---------------------------------------------------------------- H-13 · cada forma rara declara su motivo propio
@pytest.mark.parametrize("contenido, motivo", [
    ("Date,Close,Adj Close\n2026-06-01,1,1\n", "columnas ambiguas"),
    ("fecha,cierre\n2026-06-01 00:00:00-04:00,1\n", "zona horaria"),
    ("fecha,cierre\n2026-06-01,1\n2026-06-01,2\n", "fechas duplicadas"),
    ("fecha,cierre\nno-es-una-fecha,1\n", "fechas no interpretables"),
])
def test_r02_h13_motivo_explicito_de_cada_forma_rara(tmp_path, contenido, motivo):
    """El envoltorio genérico ya evita que caiga el ciclo; además, cada forma conocida se declara con su motivo (no con
    «datos no normalizables»), que es lo que lee quien revisa la incidencia."""
    (tmp_path / "X.csv").write_text(contenido, encoding="utf-8")
    p = ProveedorCSV(tmp_path)
    p.fijar_as_of(AS_OF)
    with pytest.raises(DatosInvalidos, match=motivo) as e:
        p.cierres("X")
    assert "no normalizables" not in str(e.value)                    # el motivo propio, no el del envoltorio
