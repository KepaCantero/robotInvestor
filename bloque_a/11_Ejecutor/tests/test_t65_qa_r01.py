"""T-65 · Correcciones de la QA r01 de T-65 (`.docs/tickets/T-65/qa.md`): H-01, H-02, H-04, H-05, H-07, H-08 y H-11.

Cada prueba falla con el commit b699d4f (ver `.docs/tickets/T-65/pruebas.md`). H-03 (cita del log) se comprueba con el
gate `refs-vivas` desde una copia limpia; H-06, con `.docs/scripts/prueba_refs_vivas.py`.
"""
import shutil
from pathlib import Path

import pandas as pd
import pytest
from bloque_a.almacen import Almacen
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config, max_tokens_de
from bloque_a.evaluador import Evaluador
from bloque_a.herramientas.ht01_datos import (
    DatosInvalidos,
    ProveedorCSV,
    cargar_universo,
)
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
from conftest import AS_OF, DATOS, config_pruebas


def _bloque(tmp_path, cfg=None, datos=DATOS, universo=RUTA_UNIVERSO_EJEMPLO):
    return Bloque(cfg or config_pruebas(), ProveedorCSV(datos), cargar_universo(universo), MockClient(),
                  Path(tmp_path) / "estado", Path(tmp_path) / "ent")


def _div_con_cierre_malo_antiguo(tmp_path, malo: float) -> Path:
    """Los pares DIV del ejemplo con historia desde 2019 y un cierre malo en 2019, fuera de la ventana de 3 años del lote."""
    datos = tmp_path / "datos"
    shutil.copytree(DATOS, datos)
    uni = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
    for s in uni[uni["clase"] == "DIV"]["simbolo"]:
        df = pd.read_csv(datos / f"{s}.csv")
        extra = pd.DataFrame({"fecha": [str(d.date()) for d in pd.bdate_range("2019-01-01", pd.Timestamp(df["fecha"].iloc[0])
                                                                                 - pd.Timedelta(days=1))]})
        for c in df.columns:
            if c != "fecha":
                extra[c] = df[c].iloc[0]
        extra.loc[10, "cierre"] = malo
        pd.concat([extra, df]).to_csv(datos / f"{s}.csv", index=False)
    return datos


def _con_csv(tmp_path, contenido: bytes) -> tuple[Path, Path]:
    datos = tmp_path / "datos"
    shutil.copytree(DATOS, datos)
    (datos / "USDNEW=X.csv").write_bytes(contenido)
    uni = Path(RUTA_UNIVERSO_EJEMPLO).read_text(encoding="utf-8").rstrip("\n") + \
        "\nUSDNEW=X,DIV,Dólar frente a nueva divisa,ESTRATEGIA,GLB,G10,USD,SOLO EJEMPLO,Pares,Par nuevo,Otros cruces,USD/NEW,\n"
    (tmp_path / "u.csv").write_text(uni, encoding="utf-8")
    return datos, tmp_path / "u.csv"


# ---------------------------------------------------------------- H-01 · un cierre malo antiguo no deja al tipo sin precio
@pytest.mark.parametrize("malo", [0.0, -1.0])
def test_r01_h01_cierre_malo_fuera_de_la_ventana_no_vacia_el_tipo(tmp_path, malo):
    b = _bloque(tmp_path, datos=_div_con_cierre_malo_antiguo(tmp_path, malo))
    b.fijar_fecha(AS_OF)
    sen, _ = b.senales_clase("DIV", AS_OF, "RUN-2026-0001")
    assert sen and all("precio" in t and "fecha_dato" in t for t in sen.values())   # b699d4f: los 6 sin precio, en silencio
    r = b.ciclo(AS_OF, alcance={"clases": ["DIV"]})
    assert r["paquete"]["clases"]["DIV"]["opciones"]                                  # b699d4f: 0 opciones, run COMPLETO


def test_r01_h01_valor_en_valida_solo_el_cierre_que_devuelve(tmp_path):
    (tmp_path / "X.csv").write_text("fecha,cierre\n2019-01-02,0\n2026-06-01,100\n2026-06-02,101\n", encoding="utf-8")
    (tmp_path / "Y.csv").write_text("fecha,cierre\n2026-06-01,100\n2026-06-02,-3\n", encoding="utf-8")
    p = ProveedorCSV(tmp_path)
    p.fijar_as_of("2026-06-05")
    assert p.valor_en("X", "2026-06-05")[1] == 101.0                               # b699d4f: DatosInvalidos por el 0 de 2019
    with pytest.raises(DatosInvalidos):
        p.cierres("X")                                                          # la historia entera sí lo incluye
    with pytest.raises(DatosInvalidos):
        p.valor_en("Y", "2026-06-05")                                           # el cierre que devuelve, sí se valida
    assert p.ultima_fecha("X") == pd.Timestamp("2026-06-02")


def test_r01_h01_un_precio_invalido_excluye_y_declara_el_simbolo(tmp_path, monkeypatch):
    b = _bloque(tmp_path)
    b.fijar_fecha(AS_OF)
    valor_en = b.proveedor.valor_en

    def malo(simbolo, fecha):
        if simbolo == "EURUSD=X":
            raise DatosInvalidos("HT-01: cierre no positivo simulado")
        return valor_en(simbolo, fecha)
    monkeypatch.setattr(b.proveedor, "valor_en", malo)
    sen, _ = b.senales_clase("DIV", AS_OF, "RUN-2026-0001")
    assert "EURUSD=X" not in sen and sen                                         # b699d4f: se quedaba sin precio, en silencio
    assert b._datos_invalidos[("DIV", "RUN-2026-0001")] == ["EURUSD=X"]
    assert [x for x in b.almacen.leer("HA") if x.get("tipo") == "DATOS" and x.get("objeto") == "EURUSD=X"]


# ---------------------------------------------------------------- H-02 · un CSV ilegible no tumba el ciclo
@pytest.mark.parametrize("contenido", [b"", bytes(range(256)) * 20, "fecha,cierre\n2026-06-01,1\n".encode("utf-16")])
def test_r01_h02_csv_ilegible_falla_cerrado_por_simbolo(tmp_path, contenido):
    datos, uni = _con_csv(tmp_path, contenido)
    p = ProveedorCSV(datos)
    p.fijar_as_of(AS_OF)
    with pytest.raises(DatosInvalidos):
        p.cierres("USDNEW=X")                                                    # b699d4f: EmptyDataError o ParserError
    b = _bloque(tmp_path, datos=datos, universo=uni)
    r = b.ciclo(AS_OF, alcance={"clases": ["DIV", "RV"]})                        # b699d4f: el ciclo entero caía
    assert r["estado"] == "PARCIAL" and r["paquete"]["clases"]["DIV"]["opciones"]
    assert b._datos_invalidos[("DIV", r["run_id"])] == ["USDNEW=X"]


# ---------------------------------------------------------------- H-04 · «MM-DD» estricto
@pytest.mark.parametrize("fijo", [" 1-25", "12-25 ", "١٢-٢٥", "12/25", "1-125"])
def test_r01_h04_festivo_fijo_con_formato_no_estricto_se_rechaza(tmp_path, fijo):
    cfg = config_pruebas()
    cfg["ps2_festivos"] = {"viernes_santo": True, "lunes_de_pascua": False, "fijos": ["12-25", fijo]}
    with pytest.raises(ValueError, match="MM-DD"):                              # b699d4f: se aceptaba y no casaba nunca
        _bloque(tmp_path, cfg=cfg)


# ---------------------------------------------------------------- H-05 · literales de respaldo que quedaban
def test_r01_h05_frecuencias_y_presupuestos_sin_respaldo_en_el_codigo(tmp_path):
    cfg = config_pruebas(seguimiento={"frecuencias": {"SEMANAL": 6}}, max_tokens={"por_defecto": 1234},
                         uc={"motor_por_plan": {"PLAN_MIN": 0.07}}, presupuesto_uc={"fraccion_minima_comun": 0.2})
    b = _bloque(tmp_path, cfg=cfg)
    assert b.seguimientos._dias({"frecuencia": "SEMANAL"}) == 6
    assert b.seguimientos._dias({"frecuencia": "PERSONALIZADA", "calendario_personalizado": {}}) == 6   # b699d4f: 7
    with pytest.raises(KeyError):
        b.seguimientos._dias({"frecuencia": "CADA_SIGLO"})                       # b699d4f: 7 en silencio
    assert "AG-01" not in cfg["max_tokens"] and max_tokens_de(cfg, "AG-01") == 1234   # b699d4f: 8000 si faltaba
    b.fijar_fecha(AS_OF)
    r = b.motor.servir({"operacion": "ST-DESC-001", "plan": "PLAN_MIN", "datos": [{"serie": "SPY"}]}, "AG-02", "RUN-2026-0001")
    rc = next(x for x in b.almacen.leer("RC") if x.get("calc_id") == r["calc_id"])
    assert rc["consumo_uc"] == pytest.approx(0.07)


def test_r01_h05_textos_con_los_dias_de_la_configuracion(tmp_path):
    b = _bloque(tmp_path, cfg=config_pruebas(evaluacion={"dias_habiles_no_resoluble": 7}))
    r = b.ciclo(AS_OF, alcance={"clases": ["DIV"]})
    altas = [x for x in b.almacen.leer("F4") if x.get("tipo_entrada") == "ALTA" and x.get("run_id") == r["run_id"]]
    assert altas and all("NO_RESOLUBLE tras 7 días hábiles" in x["regla_fallback"] for x in altas)   # b699d4f: «10» fijo


# ---------------------------------------------------------------- H-07 · dos proxies medibles sin solape
def test_r01_h07_dos_proxies_sin_solape_no_tumban_los_clusteres(tmp_path):
    datos = tmp_path / "datos"
    shutil.copytree(DATOS, datos)
    viejo = pd.bdate_range("2023-06-05", "2024-12-31")                         # ≈ 82 semanas en la ventana de 156
    nuevo = pd.bdate_range("2025-01-06", AS_OF)                                # ≈ 74 semanas, sin solape con el viejo
    for s, fechas in (("USDOLD=X", viejo), ("USDNEW=X", nuevo)):
        (datos / f"{s}.csv").write_text("fecha,cierre\n" + "".join(f"{d.date()},{1 + 0.01 * (i % 7)}\n"
                                                                    for i, d in enumerate(fechas)), encoding="utf-8")
    b = _bloque(tmp_path, datos=datos)
    b.fijar_fecha(AS_OF)
    proxies = ["EURUSD=X", "USDJPY=X", "USDOLD=X", "USDNEW=X"]
    cl = b._clusteres({"DIV": {"finalistas": [{"proxy": p, "_gc3": True} for p in proxies]}}, AS_OF, "RUN-2026-0001")
    assert "rechazo" not in cl and cl["calc_id"]                                 # b699d4f: ML-CLUS-001 rechazado para todos
    assert cl["sin_historia"] == ["USDNEW=X"]       # tras EURUSD, USDJPY y USDOLD (más semanas), ya no tiene solape
    assert len(set(cl["asignacion"].values())) >= 2


# ---------------------------------------------------------------- H-08 · pruebas de efecto de CS-10
def test_r01_h08_pregunta_repetida_con_las_veces_de_la_configuracion(tmp_path):
    b = _bloque(tmp_path, cfg=config_pruebas(pregunta_repetida={"veces": 2, "semanas": 4}))
    primera = b.consulta("¿Cuál es el estado de las opciones vigentes?", as_of=AS_OF)
    segunda = b.consulta("¿Cuál es el estado de las opciones vigentes?", as_of=AS_OF)
    assert not primera["repeticion"]
    assert segunda["repeticion"] and segunda["repeticion"]["veces_4_semanas"] == 2   # con el 3 del código: sin repetición


def test_r01_h08_recalibracion_de_rk_con_el_paso_y_las_bandas_de_la_configuracion(tmp_path):
    from test_t66_evaluacion import _celda_recalibrable
    a = Almacen(tmp_path / "a")
    a.reloj.fijar("2026-01-02")
    _celda_recalibrable(a, contaminados=0)
    rr = {"paso": 0.03, "banda_trimestral": 0.05, "banda_total": 0.15, "dif_ic_min": 0.10, "meses_sombra": 3}
    aju = Evaluador(a, None, None, config_pruebas(evaluacion={"recalibracion_rk": rr}), None).recalibrar("2026-01-02")
    assert aju["tipo_entrada"] == "AJU" and aju["delta"] == pytest.approx(0.03)  # con el 0,05 del código: 0,05
    assert aju["banda"] == {"trimestral": 0.05, "total": 0.15}
    b = Almacen(tmp_path / "b")
    b.reloj.fijar("2026-01-02")
    _celda_recalibrable(b, contaminados=0)
    estrecha = {**rr, "banda_total": 0.02}
    p3 = Evaluador(b, None, None, config_pruebas(evaluacion={"recalibracion_rk": estrecha}), None).recalibrar("2026-01-02")
    assert p3["tipo_entrada"] == "P3" and p3["motivo"] == "fuera de banda"


@pytest.mark.parametrize("minimo, esperado", [(2, True), (3, False)])
def test_r01_h08_ps1_con_el_minimo_de_raices_de_la_configuracion(tmp_path, minimo, esperado):
    b = _bloque(tmp_path, cfg=config_pruebas(ps1={"raices_min": minimo}))
    raices = {"r1": ("A", "SECUNDARIA"), "r2": ("B", "SECUNDARIA"), "r3": ("C", "SECUNDARIA")}
    assert b._ps1(raices) is esperado                                            # con el 2 del código, siempre True
    assert b._ps1({"r1": ("A", "PRIMARIA")}) is True


# ---------------------------------------------------------------- H-11 · coma decimal en el texto de la tasa base
def test_r01_h11_limitacion_de_la_tasa_base_con_coma_decimal(tmp_path):
    b = _bloque(tmp_path, cfg=config_pruebas(tasa_base={"min_ventanas": 10_000}))
    b.fijar_fecha(AS_OF)
    ri = b.evaluador.tasa_base("SPY", "ACWI", "RV", 5, True, AS_OF, "RUN-2026-0001")
    rc = next(x for x in b.almacen.leer("RC") if x.get("calc_id") == ri["calc_id"])
    assert rc["limitaciones"][0] == "menos de 10000 ventanas: tasa base 0,5 por defecto"   # b699d4f: «0.5»
    assert cargar_config()["tasa_base"]["sin_historia"] == 0.5
