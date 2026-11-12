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


def test_la_prima_solo_es_prudente_y_la_liquidacion_conserva_el_total():
    p = Presupuesto({"RV": 10, "RF": 10, "COMUN": 5}, config_pruebas())
    assert p.primera_llamada("RV", "AG-14") and not p.primera_llamada("RV", "AG-14") and p.primera_llamada("RF", "AG-14")
    # RF llegó primero y escribió 20.000 tokens de caché; RV los leyó. Cada uno carga su prima «solo» (los 20.000)
    prima = p._uc_prima(20000)
    assert prima > 0
    p.cargar_con_prima("RV", 0.5, 20000, 0)
    p.cargar_con_prima("RF", 0.5, 20000, 20000)
    assert p.consumido["RV"] == pytest.approx(0.5 + prima) and p.consumido["RF"] == pytest.approx(0.5 + prima)   # prudente
    p.liquidar_primas()
    assert p.consumido["RV"] == pytest.approx(0.5 + prima / 2) and p.consumido["RF"] == pytest.approx(0.5 + prima / 2)
    assert p.consumido["RV"] + p.consumido["RF"] == pytest.approx(1.0 + prima)   # el total real
    p.liquidar_primas()   # una segunda liquidación no cambia nada
    assert p.consumido["RV"] == pytest.approx(0.5 + prima / 2)


def test_sin_primas_solo_lo_real_va_a_la_bolsa_comun():
    p = Presupuesto({"RV": 10, "COMUN": 5}, config_pruebas())
    p.cargar_con_prima("RV", 0.5, 0, 3000)
    p.liquidar_primas()
    assert p.consumido["RV"] == pytest.approx(0.5) and p.consumido["COMUN"] == pytest.approx(p._uc_prima(3000))
