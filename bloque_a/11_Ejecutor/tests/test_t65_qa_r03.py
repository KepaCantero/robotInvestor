"""T-65 · Correcciones de la QA r03 de T-65 (`.docs/tickets/T-65/qa.md`, «Ronda r03»): H-16 a H-21.

Las de H-16 a H-18, H-20 y H-21 fallan con el commit 8d74622; las de H-19 cubren partes de H-12 que no tenían prueba y se
comprueban con su mutación (ver `.docs/tickets/T-65/pruebas.md`). H-22 se prueba en `.docs/scripts/prueba_refs_vivas.py`.
"""
import shutil
from pathlib import Path

import pandas as pd
import pytest
from bloque_a.almacen import Almacen
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config
from bloque_a.herramientas.ht01_datos import (
    DatosInvalidos,
    FugaDeInformacion,
    ProveedorCSV,
    cargar_universo,
)
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
from conftest import AS_OF, DATOS, config_pruebas


def _bloque(tmp_path, datos=DATOS, cfg=None):
    return Bloque(cfg or config_pruebas(), ProveedorCSV(datos), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(),
                  Path(tmp_path) / "estado", Path(tmp_path) / "ent")


def _datos(tmp_path) -> Path:
    datos = tmp_path / "datos"
    shutil.copytree(DATOS, datos)
    return datos


def _parar(datos: Path, simbolo: str, desde: str) -> None:
    """El símbolo deja de publicarse: se quitan sus filas posteriores a `desde`."""
    df = pd.read_csv(datos / f"{simbolo}.csv")
    df[df["fecha"] <= desde].to_csv(datos / f"{simbolo}.csv", index=False)


def _cero(datos: Path, simbolo: str, fecha: str) -> None:
    df = pd.read_csv(datos / f"{simbolo}.csv")
    df.loc[df["fecha"] == fecha, "cierre"] = 0
    df.to_csv(datos / f"{simbolo}.csv", index=False)


# ---------------------------------------------------------------- H-16 · referencia obsoleta, al emitir
def test_r03_h16_referencia_parada_deja_fuera_los_tipos_que_la_usan(tmp_path):
    datos = _datos(tmp_path)
    _parar(datos, "ACWI", "2025-06-30")                           # referencia de RV y de IDX, parada hace 11 meses
    b = _bloque(tmp_path, datos=datos)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV", "IDX", "DIV"]})   # 8d74622: RV e IDX COMPLETO con el nivel de 2025-06-30
    assert r["estado"] == "PARCIAL" and r["paquete"]["clases"]["DIV"]["opciones"]
    altas = [x for x in b.almacen.leer("F4") if x.get("tipo_entrada") == "ALTA" and x.get("clase") in ("RV", "IDX")]
    assert not altas                                               # ningún pronóstico con la referencia parada
    lim = " ".join(r["paquete"]["limitaciones"])
    assert "referencia de comparación ACWI" in lim and "2025-06-30" in lim
    assert len([x for x in b.almacen.leer("HA") if x.get("tipo") == "DATOS" and x.get("objeto") == "ACWI"]) == 2


def test_r03_h16_la_frescura_de_la_referencia_sale_de_la_configuracion(tmp_path):
    datos = _datos(tmp_path)
    _parar(datos, "ACWI", "2026-05-22")                           # 14 días antes de AS_OF
    assert cargar_config()["referencias"]["antiguedad_maxima_dias"] == 7
    b = _bloque(tmp_path / "a", datos=datos)
    b.fijar_fecha(AS_OF)
    assert "14 días" in b._referencia_invalida("ACWI", "2023-01-02", AS_OF)
    holgada = _bloque(tmp_path / "b", datos=datos, cfg=config_pruebas(referencias={"antiguedad_maxima_dias": 20}))
    holgada.fijar_fecha(AS_OF)
    assert holgada._referencia_invalida("ACWI", "2023-01-02", AS_OF) is None


# ---------------------------------------------------------------- H-16 · referencia o proxy parados, al resolver
def _prg_relativo(a: Almacen) -> None:
    a.escribir("F4", "AG-10", {
        "tipo_entrada": "ALTA", "prg_id": "PRG-2026-0901", "opp_id": "OPP-1", "clase": "RV", "horizonte": "H2", "estado": "ABIERTO",
        "prob_interna": 0.65, "sentido": "POSITIVO", "umbral": 0.0, "tipo_pronostico": "RELATIVO", "referencia_indice": "ACWI",
        "variable": {"serie_ht01": "SPY"}, "fecha_emision": "2026-04-03", "fecha_resolucion": "2026-05-01",
        "nivel_referencia": {"valor": 1.0, "fecha": "2026-04-03"}, "referencia_ingenua": {"valor_o_prob": 0.5}, "en_informe": True})


@pytest.mark.parametrize("parado", ["ACWI", "SPY"])
def test_r03_h16_no_se_resuelve_con_una_serie_parada(tmp_path, parado):
    datos = _datos(tmp_path)
    _parar(datos, parado, "2026-04-10")                            # deja de publicarse tras la emisión
    b = _bloque(tmp_path, datos=datos)
    b.fijar_fecha("2026-04-03")                                  # el PRG se congela en su fecha de emisión
    _prg_relativo(b.almacen)
    b.fijar_fecha("2026-05-04")
    assert b.evaluador.resolver("2026-05-04", "RUN-2026-0001") == []     # 8d74622: RESUELTO con una rentabilidad 0
    assert b.almacen.estado("F4")["PRG-2026-0901"]["estado"] == "ABIERTO"
    b.fijar_fecha(AS_OF)                                          # pasado el plazo de días hábiles: NO_RESOLUBLE
    b.evaluador.resolver(AS_OF, "RUN-2026-0002")
    assert b.almacen.estado("F4")["PRG-2026-0901"]["estado"] == "NO_RESOLUBLE"


def test_r03_h16_con_las_dos_series_al_dia_se_resuelve(tmp_path):
    b = _bloque(tmp_path)
    b.fijar_fecha("2026-04-03")                                  # el PRG se congela en su fecha de emisión
    _prg_relativo(b.almacen)
    b.fijar_fecha("2026-05-04")
    b.evaluador.resolver("2026-05-04", "RUN-2026-0001")
    assert b.almacen.estado("F4")["PRG-2026-0901"]["estado"] == "RESUELTO"


def test_r03_h16_un_miembro_parado_de_la_cesta_no_cuenta(tmp_path):
    datos = _datos(tmp_path)
    b = _bloque(tmp_path, datos=datos)
    b.fijar_fecha(AS_OF)
    ev = b.evaluador
    todos = ev.simbolos_clase("DIV")
    r_todos, _ = ev.rentabilidad("CESTA", "DIV", "2026-04-03", "2026-05-01", "H2")
    _parar(datos, todos[0], "2026-04-10")
    b2 = _bloque(tmp_path / "b", datos=datos)
    b2.fijar_fecha(AS_OF)
    r_sin, _ = b2.evaluador.rentabilidad("CESTA", "DIV", "2026-04-03", "2026-05-01", "H2")
    otros = [b2.evaluador.rentabilidad(s, "DIV", "2026-04-03", "2026-05-01", "H2")[0] for s in todos[1:]]
    assert r_sin == pytest.approx(sum(otros) / len(otros)) and r_sin != pytest.approx(r_todos)   # 8d74622: entraba con 0


# ---------------------------------------------------------------- H-17 · subyacente declarado sin datos
def test_r03_h17_subyacente_sin_archivo_se_declara_y_no_se_cambia_por_la_cesta(tmp_path):
    datos = _datos(tmp_path)
    uni = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
    der = uni[uni["clase"] == "DER"]
    sub = str(der["subyacente"].dropna().astype(str).str.strip().replace("", pd.NA).dropna().iloc[0])
    con_sub = list(der[der["subyacente"].astype(str).str.strip() == sub]["simbolo"])
    (datos / f"{sub}.csv").unlink()
    b = _bloque(tmp_path, datos=datos)
    b.fijar_fecha(AS_OF)
    assert b._referencia("DER", con_sub[0]) == sub                 # 8d74622: «CESTA», en silencio
    senales, _ = b.senales_clase("DER", AS_OF, "RUN-2026-0001")
    assert not set(con_sub) & set(senales)
    assert set(con_sub) <= set(b._datos_invalidos[("DER", "RUN-2026-0001")])


def test_r03_h17_columna_vacia_sigue_siendo_la_cesta(tmp_path):
    b = _bloque(tmp_path)
    vacios = b.universo[(b.universo["clase"] == "DER") & (b.universo["subyacente"].isna()
                                                         | (b.universo["subyacente"].astype(str).str.strip() == ""))]
    sin_fila = "NO-ESTA-EN-EL-UNIVERSO"
    assert b._referencia("DER", sin_fila) == "CESTA"
    for s in vacios["simbolo"]:
        assert b._referencia("DER", s) == "CESTA"


# ---------------------------------------------------------------- H-18 · con SUBYACENTE, la vigente se valida con su indicador
def test_r03_h18_vigente_con_subyacente_malo_excluye_solo_su_indicador(tmp_path, monkeypatch):
    datos = _datos(tmp_path)
    _cero(datos, "ACWI", "2026-05-29")
    b = _bloque(tmp_path, datos=datos)
    b.fijar_fecha(AS_OF)
    der = [s for s in b.universo[b.universo["clase"] == "DER"]["simbolo"] if b.proveedor.tiene(s)]
    vigente = {"opp_id": "OPP-2026-0001", "clase": "DER", "estado": "VIGENTE", "indicador_seguimiento": {"simbolo": der[0]},
               "referencia_indice": "ACWI"}
    monkeypatch.setattr(b, "vigentes", lambda as_of, clase=None: [vigente] if clase == "DER" else [])
    senales, _ = b.senales_clase("DER", AS_OF, "RUN-2026-0001")       # 8d74622: DatosInvalidos, DER entero fuera
    assert der[0] not in senales and senales
    assert b._datos_invalidos[("DER", "RUN-2026-0001")] == [der[0]]


# ---------------------------------------------------------------- H-19 · partes de H-12 sin prueba
def test_r03_h19_la_referencia_guardada_en_una_vigente_se_valida(tmp_path, monkeypatch):
    datos = _datos(tmp_path)
    _cero(datos, "AGG", "2026-05-29")
    b = _bloque(tmp_path, datos=datos)
    b.fijar_fecha(AS_OF)
    vigente = {"opp_id": "OPP-2026-0001", "clase": "RV", "estado": "VIGENTE", "indicador_seguimiento": {"simbolo": "SPY"},
               "referencia_indice": "AGG"}                         # una referencia de un ciclo anterior, distinta de ACWI
    monkeypatch.setattr(b, "vigentes", lambda as_of, clase=None: [vigente] if clase == "RV" else [])
    with pytest.raises(DatosInvalidos, match="AGG"):
        b.senales_clase("RV", AS_OF, "RUN-2026-0001")
    assert [x for x in b.almacen.leer("HA") if x.get("tipo") == "DATOS" and x.get("objeto") == "AGG"]


def test_r03_h19_una_fuga_de_informacion_en_la_referencia_corta(tmp_path, monkeypatch):
    b = _bloque(tmp_path)
    b.fijar_fecha(AS_OF)
    cierres = b.proveedor.cierres

    def fuga(simbolo, *a, **kw):
        if simbolo == "ACWI":
            raise FugaDeInformacion("fuga simulada en la referencia")
        return cierres(simbolo, *a, **kw)
    monkeypatch.setattr(b.proveedor, "cierres", fuga)
    with pytest.raises(FugaDeInformacion):                         # no se absorbe como «referencia inválida»
        b.senales_clase("RV", AS_OF, "RUN-2026-0001")


# ---------------------------------------------------------------- H-20 · cabeceras repetidas
@pytest.mark.parametrize("cabecera", ["fecha,cierre,cierre", "fecha,Close,Close", "fecha,fecha,cierre"])
def test_r03_h20_cabecera_repetida_es_dato_invalido(tmp_path, cabecera):
    n = cabecera.count(",") + 1
    (tmp_path / "X.csv").write_text(cabecera + "\n" + "".join(f"2026-06-0{i}," + ",".join(["1"] * (n - 1)) + "\n"
                                                              for i in range(1, 4)), encoding="utf-8")
    p = ProveedorCSV(tmp_path)
    p.fijar_as_of(AS_OF)
    with pytest.raises(DatosInvalidos, match="repetidas"):         # 8d74622: se usaba la primera columna en silencio
        p.cierres("X")


# ---------------------------------------------------------------- H-21 · solo se valida lo que se usa
def test_r03_h21_un_dato_malo_posterior_a_as_of_no_excluye_el_simbolo(tmp_path):
    (tmp_path / "X.csv").write_text("fecha,cierre\n2026-06-01,100\n2026-06-02,101\n2026-07-01,inf\n2026-07-02,n.d.\n",
                                    encoding="utf-8")
    p = ProveedorCSV(tmp_path)
    p.fijar_as_of("2026-06-05")
    assert list(p.cierres("X")) == [100.0, 101.0]                  # 8d74622: DatosInvalidos por filas futuras
    p.fijar_as_of("2026-07-05")
    with pytest.raises(DatosInvalidos, match="no numéricos o no finitos"):
        p.cierres("X")


def test_r03_h21_un_dato_malo_fuera_de_la_ventana_no_importa(tmp_path):
    (tmp_path / "X.csv").write_text("fecha,cierre\n2019-01-02,inf\n2019-01-03,1\n2019-01-03,2\n2026-06-01,100\n2026-06-02,101\n",
                                    encoding="utf-8")
    p = ProveedorCSV(tmp_path)
    p.fijar_as_of("2026-06-05")
    assert list(p.cierres("X", "2023-01-01")) == [100.0, 101.0]   # 8d74622: DatosInvalidos por la fila de 2019
    assert p.valor_en("X", "2026-06-05")[1] == 101.0
    with pytest.raises(DatosInvalidos):
        p.cierres("X")                                             # la historia entera sí los incluye


def test_r03_h21_una_fecha_repetida_en_el_rango_sigue_siendo_invalida(tmp_path):
    (tmp_path / "X.csv").write_text("fecha,cierre\n2026-06-01,100\n2026-06-02,101\n2026-06-02,102\n", encoding="utf-8")
    p = ProveedorCSV(tmp_path)
    p.fijar_as_of("2026-06-05")
    with pytest.raises(DatosInvalidos, match="fechas duplicadas"):
        p.valor_en("X", "2026-06-05")
    with pytest.raises(DatosInvalidos, match="fechas duplicadas"):
        p.cierres("X", "2026-06-01")
