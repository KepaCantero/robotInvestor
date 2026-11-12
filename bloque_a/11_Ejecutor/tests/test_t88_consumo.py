"""T-88: el consumo por tipo de F5 es el mismo en dos ejecuciones iguales con varios hilos (QA de T-65, H-10).

La causa era la caché de prompts: la escritura de un prefijo compartido (un agente que trabaja para varios tipos, como AG-10,
AG-11, AG-12 o AG-14, o el núcleo común de los analistas V6) la pagaba el tipo cuyo hilo llegaba primero."""
import json
from pathlib import Path

import pytest
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
from bloque_a.consumo import Presupuesto
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
from conftest import AS_OF, DATOS, config_pruebas

PERFILES = ["RV", "RF", "DIV", "MP", "IDX", "FON"]


def _consumo(tmp: Path, diseno: str) -> tuple[dict, float]:
    b = Bloque(config_pruebas(diseno=diseno, perfiles={"activos": PERFILES}, paralelismo={"hilos_analistas": 6}), ProveedorCSV(DATOS),
               cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "estado", tmp / "ent")
    b.ciclo(AS_OF)
    f5 = [e for e in b.almacen.leer("F5") if "presupuesto" in e][-1]["presupuesto"]
    return f5, sum(x["uc"] for x in b.contabilidad.llamadas)


@pytest.mark.parametrize("diseno", ["v5", "v6"])
def test_dos_ejecuciones_iguales_dan_el_mismo_consumo_por_tipo(tmp_path, diseno):
    vistos = [json.dumps(_consumo(tmp_path / str(k), diseno)[0], sort_keys=True) for k in range(3)]
    assert len(set(vistos)) == 1, vistos


def test_v6_el_total_cargado_es_el_coste_real(tmp_path):
    """En la V6 todas las llamadas pasan antes del registro de F5: lo cargado a las bolsas es exactamente lo gastado."""
    f5, real = _consumo(tmp_path, "v6")
    assert sum(x["consumido"] for x in f5.values()) == pytest.approx(real, abs=0.01)   # redondeo de 0,0001 por llamada


def test_la_liquidacion_reparte_por_grupo_y_conserva_el_total():
    p = Presupuesto({"RV": 10, "RF": 10, "COMUN": 5}, config_pruebas())
    assert p.primera_llamada("RV", "AG-14") and not p.primera_llamada("RV", "AG-14") and p.primera_llamada("RF", "AG-14")
    prima = p._uc_prima(20000)
    assert prima > 0
    # AG-14, compartido: RF llegó primero y escribió 20.000 tokens; RV los leyó. Durante la fase ninguno carga prima
    p.cargar_con_prima("RV", "AG-14", 0.5, 20000, 0, 0)
    p.cargar_con_prima("RF", "AG-14", 0.5, 20000, 0, 20000)
    # el analista propio de RV (AG-03) escribe su prompt: se carga ya (QA r01 de T-88, H-01)
    p.cargar_con_prima("RV", "ANALISTAS", 0.2, 10000, 10000, 10000)
    assert p.consumido["RV"] == pytest.approx(0.7 + p._uc_prima(10000)) and p.consumido["RF"] == pytest.approx(0.5)
    p.liquidar_primas()
    # AG-14 a medias; el prompt de RV, entero para RV y nada para RF (H-02: los grupos no se mezclan)
    assert p.consumido["RV"] == pytest.approx(0.7 + prima / 2 + p._uc_prima(10000))
    assert p.consumido["RF"] == pytest.approx(0.5 + prima / 2)
    p.liquidar_primas()   # una segunda liquidación no cambia nada
    assert p.consumido["RF"] == pytest.approx(0.5 + prima / 2)


def test_sin_pesos_lo_real_va_a_la_bolsa_comun():
    p = Presupuesto({"RV": 10, "COMUN": 5}, config_pruebas())
    p.cargar_con_prima("RV", "AG-14", 0.5, 0, 0, 3000)
    p.liquidar_primas()
    assert p.consumido["RV"] == pytest.approx(0.5) and p.consumido["COMUN"] == pytest.approx(p._uc_prima(3000))
