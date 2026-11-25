"""T-201 · cuota de mypy del Bloque A: los cambios que no son solo anotaciones, cada uno con su prueba.

El ticket no cambia ningún comportamiento (la equivalencia de salidas está en `.docs/tickets/T-201/equivalencia.sh`). Estas
pruebas fijan lo que cada cambio no mecánico debe conservar, y la de `ruta` lo único que cambia: el mensaje del error.
"""
import copy
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from bloque_a.almacen import Almacen
from bloque_a.configuracion import cargar_config, raiz_paquete, ruta
from bloque_a.herramientas import ht02, ht03, ht07, ht09
from bloque_a.motor import evaluacion, fichas_p2, operaciones, servicio
from conftest import AS_OF

from bloque_a import seguimiento

REFERENCIA = Path(__file__).resolve().parents[1] / "bloque_a" / "herramientas" / "referencia"
ENVOLTORIOS = [(ht02, "ht02_verificador_enlaces"), (ht03, "ht03_puntuaciones"), (ht07, "ht07_legibilidad"),
               (ht09, "ht09_validador_g3")]


# ------------------------------------------------------------------ envoltorios de HT-02, HT-03, HT-07 y HT-09
@pytest.mark.parametrize(("envoltorio", "nombre"), ENVOLTORIOS, ids=[n for _, n in ENVOLTORIOS])
def test_el_envoltorio_importa_en_ejecucion_el_mismo_modulo_que_antes(envoltorio, nombre):
    """En ejecución el envoltorio sigue importando la copia por `sys.path` (nombre de primer nivel), no por su ruta de
    paquete: un segundo objeto módulo duplicaría las clases (p. ej. `ErrorEntrada`) y un `except` dejaría de casar."""
    assert envoltorio.modulo is sys.modules[nombre]
    assert Path(envoltorio.modulo.__file__).resolve() == REFERENCIA / f"{nombre}.py"


@pytest.mark.parametrize(("envoltorio", "nombre"), ENVOLTORIOS, ids=[n for _, n in ENVOLTORIOS])
def test_la_rama_de_mypy_apunta_al_mismo_fichero(envoltorio, nombre):
    """La rama `TYPE_CHECKING` nombra `bloque_a.herramientas.referencia.<nombre>`: es el mismo fichero que se ejecuta."""
    spec = importlib.util.find_spec(f"bloque_a.herramientas.referencia.{nombre}")
    assert spec is not None and Path(spec.origin).resolve() == Path(envoltorio.modulo.__file__).resolve()
    fuente = Path(envoltorio.__file__).read_text(encoding="utf-8")
    assert f"from .referencia.{nombre} import *" in fuente and f"from {nombre} import *" in fuente


@pytest.mark.parametrize(("envoltorio", "nombre"), ENVOLTORIOS, ids=[n for _, n in ENVOLTORIOS])
def test_el_envoltorio_reexporta_cada_nombre_publico_de_la_referencia(envoltorio, nombre):
    publicos = [n for n in vars(envoltorio.modulo) if not n.startswith("_")]
    assert publicos
    propios = {"comprobar_madurez", "normalizar", "NIVELES"} if envoltorio is ht09 else set()   # T-165: G3-MET-13
    for n in publicos:
        if n not in propios and not isinstance(getattr(envoltorio.modulo, n), type(sys)):
            assert getattr(envoltorio, n) is getattr(envoltorio.modulo, n), n


def test_ht09_y_ht03_comparten_la_clase_de_error_de_la_referencia():
    assert ht09.modulo.ht03 is ht03.modulo
    assert ht03.ErrorEntrada is ht09.modulo.ht03.ErrorEntrada


# ------------------------------------------------------------------ configuracion.ruta
def test_ruta_sin_la_clave_falla_con_el_mismo_tipo_de_error_y_dice_que_clave_falta():
    with pytest.raises(TypeError, match=r"^rutas\.plantillas no está en la configuración o es null$"):
        ruta({"rutas": {}}, "plantillas")
    with pytest.raises(TypeError, match=r"^rutas\.prompts no está en la configuración o es null$"):
        ruta({}, "prompts")


# r02 (QA r01, H-03): los tres límites del valor de la clave
def test_ruta_con_la_clave_a_null_da_el_mensaje_nuevo():
    with pytest.raises(TypeError, match=r"^rutas\.x no está en la configuración o es null$"):
        ruta({"rutas": {"x": None}}, "x")


def test_ruta_con_la_clave_vacia_devuelve_la_raiz_del_paquete_como_antes():
    cfg = {"rutas": {"x": ""}}
    assert ruta(cfg, "x") == raiz_paquete(cfg)


def test_ruta_con_la_clave_a_cero_da_el_error_de_path_como_antes():
    with pytest.raises(TypeError) as e:
        ruta({"rutas": {"x": 0}}, "x")
    assert "not 'int'" in str(e.value) and "no está en la configuración" not in str(e.value)


def test_ruta_con_la_clave_no_cambia():
    cfg = cargar_config()
    assert ruta(cfg, "plantillas").is_dir()
    assert ruta({"rutas": {"x": "/tmp"}}, "x") == Path("/tmp")


# ------------------------------------------------------------------ seguimiento
class _B:
    def __init__(self, carpeta):
        self.almacen = Almacen(Path(carpeta))
        self.cfg = cargar_config()


def test_un_ct24_sin_seg_id_sigue_siendo_un_encargo_desconocido(tmp_path):
    s = seguimiento.Seguimientos(_B(tmp_path))
    with pytest.raises(KeyError, match="Encargo desconocido None"):
        s._cambio({"accion": "PAUSA"}, "PAUSA", pd.Timestamp(AS_OF))


@pytest.mark.parametrize(("clase", "agente"), [("RV", "AG-03"), ("RF", "AG-04"), ("TCV", "AG-25"), (None, None),
                                               ("XYZ", None), ("", None)])
def test_b_agente_da_el_analista_de_su_clase_o_falla(clase, agente):
    # T-205: una clase desconocida, vacía o None ya no va al AG-03 por defecto: falla de forma explícita
    if agente is None:
        with pytest.raises(seguimiento.ClaseNoAdmitida):
            seguimiento.b_agente(clase)
    else:
        assert seguimiento.b_agente(clase) == agente


@pytest.mark.parametrize(("hito", "estado"), [
    ({"estado": "ABIERTO"}, "PENDIENTE"),
    ({"estado": "RESUELTO", "resolucion": {"resultado_binario": 1}}, "CUMPLIDO"),
    ({"estado": "RESUELTO", "resolucion": {"resultado_binario": 0}}, "FALLADO"),
    ({"estado": "RESUELTO"}, "FALLADO"),
    ({"estado": "RESUELTO", "resolucion": None}, "FALLADO"),
    ({"estado": "ANULADO"}, "PENDIENTE"),
    ({}, "PENDIENTE"),
    ({"estado": None, "resolucion": {"resultado_binario": 1}}, "PENDIENTE"),
])
def test_estado_hito_da_lo_mismo_que_la_comprension_de_antes(hito, estado):
    antes = {"ABIERTO": "PENDIENTE", "RESUELTO": "CUMPLIDO" if (hito.get("resolucion") or {}).get("resultado_binario")
             else "FALLADO"}.get(hito.get("estado"), "PENDIENTE")
    assert seguimiento._estado_hito(hito) == antes == estado


def test_estado_hito_lee_el_resultado_aunque_el_hito_siga_abierto():
    """Como antes: el resultado binario se lee siempre; una resolución que no es un diccionario sigue fallando."""
    with pytest.raises(AttributeError):
        seguimiento._estado_hito({"estado": "ABIERTO", "resolucion": "no es un diccionario"})


def test_la_revision_c6_lleva_el_estado_de_cada_hito(tmp_path):
    """`_revision` pone en cada pronóstico abierto el estado de sus hitos con `_estado_hito`."""
    from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
    from bloque_a.herramientas.ht01_datos import cargar_universo
    from conftest import nuevo_bloque
    b = nuevo_bloque(tmp_path, cargar_universo(RUTA_UNIVERSO_EJEMPLO))
    b.fijar_fecha(AS_OF)
    b.almacen.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": "PRG-2026-0001", "opp_id": "OPP-2026-0001",
                                       "estado": "ABIERTO", "horizonte": "H2", "hit_ids": ["HIT-2026-0001", "HIT-2026-0002"]})
    b.almacen.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": "HIT-2026-0001", "es_hito": True, "estado": "RESUELTO",
                                       "fecha_resolucion": "2026-05-29", "resolucion": {"resultado_binario": 1}})
    b.almacen.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": "HIT-2026-0002", "es_hito": True, "estado": "ABIERTO",
                                       "fecha_resolucion": "2026-07-03"})
    opp = {"opp_id": "OPP-2026-0001", "clase": "DIV", "indicador_seguimiento": {"simbolo": "EURUSD=X"}}
    rev = b.seguimientos._revision({"fecha_alta": "2026-05-29"}, opp, pd.Timestamp(AS_OF))
    [p] = rev["pronosticos_abiertos"]
    assert p["hitos"] == [{"hit_id": "HIT-2026-0001", "fecha": "2026-05-29", "estado": "CUMPLIDO"},
                          {"hit_id": "HIT-2026-0002", "fecha": "2026-07-03", "estado": "PENDIENTE"}]


# ------------------------------------------------------------------ motor
def test_acierto_direccional_con_lista_y_con_array():
    for o in ([1, 0, 1, 1], np.array([1, 0, 1, 1])):
        r = evaluacion.acierto_direccional(o)
        assert (r["n"], r["aciertos"], r["tasa"]) == (4, 3, 0.75)
    assert evaluacion.acierto_direccional([])["n"] == 0
    # r02 (QA r01, H-02): con flotantes, los aciertos se cuentan sobre el array truncado a enteros, no sobre la entrada
    r = evaluacion.acierto_direccional([1.7, 1.7, 0.2])
    assert (r["n"], r["aciertos"]) == (3, 2)


def test_diferencial_rentabilidades_con_historia_usa_el_diferencial_escalado():
    hist = [0.01, 0.02, 0.03, 0.04, 0.05]
    r = operaciones.diferencial_rentabilidades(0.06, 0.02, hist)
    assert r["diferencial"] == pytest.approx(4.0) and r["unidad"] == "pp"
    esperado = operaciones.posicion_historica(r["diferencial"], np.array(hist) * 100)   # el mismo valor que sale en `diferencial`
    assert {k: r[f"{k}_historico"] for k in esperado} == esperado
    pb = operaciones.diferencial_rentabilidades(0.06, 0.02, hist, en_pb=True)
    assert pb["diferencial"] == pytest.approx(400.0) and pb["unidad"] == "pb" and pb["n_historico"] == 5
    assert "z_historico" not in operaciones.diferencial_rentabilidades(0.06, 0.02, hist[:4])


def test_motor_sin_ficha_y_cache_hit_como_antes(tmp_path):
    class _P:
        as_of = None
        nombre = "pruebas"
    m = servicio.Motor(Almacen(tmp_path), _P(), cargar_config())
    for pet in ({"operacion": None, "datos": []}, {"operacion": {"ficha_id": None}, "datos": []}, {"datos": []}):
        r = m.servir(pet, "AG-02")
        assert (r["estado"], r["motivo"]) == ("RECHAZADO", "DATOS_INCOHERENTES") and r.get("alternativa") is None
    caso = fichas_p2.CASOS_CONTROL["FIR-CRED-001"][1]
    valores = {k: v for d in caso["datos"] for k, v in d["valores"].items()}
    pet = {"operacion": "FIR-CRED-001", "datos": [{"valores": valores}], "parametros": dict(caso["parametros"]), "fecha_corte": None}
    r1 = m.servir(copy.deepcopy(pet), "AG-21")
    r2 = m.servir(copy.deepcopy(pet), "AG-21")
    hit = m.almacen.leer("RC")[-1]
    assert not r1["cache_hit"] and r2["cache_hit"] and hit["tipo_entrada"] == "CACHE_HIT"
    assert r2["calc_id_cache"] == hit["calc_id"] and hit["calc_original"] == r1["calc_id"]
