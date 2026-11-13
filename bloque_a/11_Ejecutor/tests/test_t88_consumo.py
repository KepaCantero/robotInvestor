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



# ================================================================================================== ronda r03 (QA r02 de T-88)
from types import SimpleNamespace

from bloque_a.consumo import Contabilidad
from bloque_a.llm import Uso


def _fake(v6=False):
    cfg = config_pruebas()
    return SimpleNamespace(contabilidad=Contabilidad(cfg), v6=v6), Presupuesto({"RV": 50, "RF": 50, "IDX": 50, "FON": 50, "COMUN": 50}, cfg)


def _r(escrito, leido, intentos=1, entrada=1000, salida=500):
    return SimpleNamespace(uso=Uso(entrada=entrada, salida=salida, cache_escritura=escrito, cache_lectura=leido), cache_hit=False,
                           intentos=intentos, uc=0.0)


def _leido(fake, r):
    u = r.uso
    return fake.contabilidad.uc_de(Uso(entrada=u.entrada, salida=u.salida, cache_lectura=u.cache_escritura + u.cache_lectura))


def test_r03_durante_la_fase_solo_el_analista_propio_carga_su_escritura():
    """P1 y P2: el analista propio carga la prima de su prompt; un agente compartido, no (solo la lectura)."""
    fake, p = _fake()
    propio, compartido = _r(20000, 0), _r(20000, 0)
    Bloque._cargar(fake, p, "RV", "AG-03", propio)
    Bloque._cargar(fake, p, "RF", "AG-14", compartido)
    assert p.consumido["RV"] == pytest.approx(_leido(fake, propio) + p._uc_prima(20000))
    assert p.consumido["RF"] == pytest.approx(_leido(fake, compartido))


def test_r03_el_analista_propio_carga_su_prima_solo_aunque_lea_de_cache():
    """P10: con la caché ya caliente (escritura real 0), el tipo carga igualmente lo que escribiría solo."""
    fake, p = _fake()
    r = _r(0, 20000)
    Bloque._cargar(fake, p, "RV", "AG-03", r)
    assert p.consumido["RV"] == pytest.approx(_leido(fake, r) + p._uc_prima(20000))


def test_r03_la_prima_solo_se_divide_por_los_intentos_y_solo_en_la_primera_llamada():
    """P8 y P9."""
    fake, p = _fake()
    r1 = _r(20000, 20000, intentos=2)   # un intento escribe y el otro lee el mismo prefijo
    Bloque._cargar(fake, p, "RV", "AG-03", r1)
    assert p.consumido["RV"] == pytest.approx(_leido(fake, r1) + p._uc_prima(20000))
    antes = p.consumido["RV"]
    r2 = _r(0, 20000)
    Bloque._cargar(fake, p, "RV", "AG-03", r2)   # segunda llamada del mismo agente en la bolsa: sin prima
    assert p.consumido["RV"] - antes == pytest.approx(_leido(fake, r2))


def test_r03_v5_cada_analista_paga_su_prompt_y_los_compartidos_se_reparten_por_agente():
    """P3 y H-05: en la V5 no se mezclan los prompts de los analistas ni con los compartidos."""
    fake, p = _fake()
    Bloque._cargar(fake, p, "RV", "AG-03", _r(10000, 0))
    Bloque._cargar(fake, p, "RF", "AG-04", _r(20000, 0))
    Bloque._cargar(fake, p, "RV", "AG-14", _r(0, 20000))      # AG-14: RF escribe y RV lee
    Bloque._cargar(fake, p, "RF", "AG-14", _r(20000, 0))
    base = {b: p.consumido[b] - p._uc_prima(t) for b, t in (("RV", 10000), ("RF", 20000))}
    p.liquidar_primas()
    assert p.consumido["RV"] == pytest.approx(base["RV"] + p._uc_prima(10000) + p._uc_prima(10000))
    assert p.consumido["RF"] == pytest.approx(base["RF"] + p._uc_prima(20000) + p._uc_prima(10000))


def test_r03_v6_los_analistas_comparten_grupo_por_el_nucleo():
    """P4: en la V6 el núcleo común lo escribe el primer analista; el grupo de los analistas lo reparte entre los tipos."""
    fake, p = _fake(v6=True)
    Bloque._cargar(fake, p, "IDX", "AG-21", _r(15000, 0))   # escribe núcleo (10.000) y kit (5.000)
    Bloque._cargar(fake, p, "FON", "AG-22", _r(5000, 10000))   # lee el núcleo y escribe su kit
    antes = {b: p.consumido[b] - p._uc_prima(15000) for b in ("IDX", "FON")}
    p.liquidar_primas()
    assert p.consumido["IDX"] == pytest.approx(antes["IDX"] + p._uc_prima(10000))
    assert p.consumido["FON"] == pytest.approx(antes["FON"] + p._uc_prima(10000))


def test_r03_se_liquida_al_acabar_la_fase_en_paralelo_y_al_resumir(tmp_path, monkeypatch):
    """P7: dos liquidaciones por ciclo como mínimo (tras la fase en paralelo y en `resumen`)."""
    import inspect
    llamadas = []
    orig = Presupuesto.liquidar_primas
    monkeypatch.setattr(Presupuesto, "liquidar_primas", lambda self: (llamadas.append(inspect.stack()[1].function), orig(self))[1])
    _consumo(tmp_path, "v5")
    assert "resumen" in llamadas and any(x != "resumen" for x in llamadas), llamadas   # también tras la fase en paralelo


# ================================================================================================== ronda r04 (QA r03 de T-88)
CLAVES_CONSUMO = {"llamadas", "uc", "uc_llm", "uc_motor", "entrada", "salida", "cache_escritura", "cache_lectura"}


@pytest.mark.parametrize("diseno", ["v5", "v6"])
def test_r04_h10_el_run_de_f5_lleva_el_consumo(tmp_path, diseno):
    """H-10: el Documento 0 manda registrar en F5 el presupuesto y el consumo real del run."""
    b = Bloque(config_pruebas(diseno=diseno, perfiles={"activos": PERFILES}, paralelismo={"hilos_analistas": 6}), ProveedorCSV(DATOS),
               cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp_path / "estado", tmp_path / "ent")
    b.ciclo(AS_OF)
    run = [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "RUN"][-1]
    assert {"presupuesto", "cierres_parciales", "consumo", "participantes"} <= set(run)
    assert set(run["consumo"]) == CLAVES_CONSUMO and run["consumo"]["uc"] > 0 and run["consumo"]["llamadas"] > 0
    assert all(u["uc"] is not None for u in b.estado()["ultimos_runs"])


def test_r04_h13_en_la_v5_cada_tipo_paga_las_reescrituras_de_su_analista():
    """H-13 (mutante R1): si la caché de AG-03 se pierde y reescribe su prompt, lo paga RV entero; RF solo paga lo suyo."""
    fake, p = _fake()
    Bloque._cargar(fake, p, "RV", "AG-03", _r(10000, 0))
    Bloque._cargar(fake, p, "RF", "AG-04", _r(20000, 0))
    Bloque._cargar(fake, p, "RV", "AG-03", _r(10000, 0))   # segunda llamada: la caché se perdió y vuelve a escribir
    base = {"RV": p.consumido["RV"] - p._uc_prima(10000), "RF": p.consumido["RF"] - p._uc_prima(20000)}
    p.liquidar_primas()
    assert p.consumido["RV"] == pytest.approx(base["RV"] + p._uc_prima(20000))
    assert p.consumido["RF"] == pytest.approx(base["RF"] + p._uc_prima(20000))


class _AlReves(list):
    """Lista que guarda cada cierre delante: el orden de llegada queda al revés del ordenado."""

    def append(self, x):
        self.insert(0, x)


def test_r04_h13_los_cierres_parciales_salen_ordenados_por_tipo_fase_y_motivo(tmp_path, monkeypatch):
    """H-13 (mutantes R4 y R5): F5 no depende del orden en que los hilos cierran fases."""
    init = Presupuesto.__init__
    llegada = [{"clase": "RV", "fase": "F1", "motivo": "a"}, {"clase": "RV", "fase": "F2", "motivo": "b"},
               {"clase": "RV", "fase": "F2", "motivo": "a"}, {"clase": "IDX", "fase": "F1", "motivo": "a"}]

    def con_cierres(self, *a, **k):
        init(self, *a, **k)
        self.cierres = _AlReves()
        for c in llegada:
            self.cierres.append(dict(c))
    monkeypatch.setattr(Presupuesto, "__init__", con_cierres)
    b = Bloque(config_pruebas(perfiles={"activos": PERFILES}), ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO),
               MockClient(), tmp_path / "estado", tmp_path / "ent")
    b.ciclo(AS_OF)
    cierres = [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "RUN"][-1]["cierres_parciales"]
    clave = [(c["clase"], c["fase"], c["motivo"]) for c in cierres]
    assert clave == sorted(clave) and {("RV", "F2", "a"), ("IDX", "F1", "a")} <= set(clave)
