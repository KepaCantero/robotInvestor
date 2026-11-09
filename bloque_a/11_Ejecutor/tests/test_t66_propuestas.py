"""T-66 · Propuestas de T-53 aplicadas al Bloque A (parte de orquestación): PA-01, H-06, PA-05, PA-09, PA-14 y PA-21.

Cada prueba falla sin su cambio (ver `.docs/tickets/T-66/pruebas.md`).
"""
import json
from pathlib import Path

import pytest
from conftest import AS_OF, DATOS, config_pruebas

from bloque_a import mock_respuestas as mr
from bloque_a import sintesis
from bloque_a.configuracion import (
    CLASES,
    RUTA_UNIVERSO_EJEMPLO,
    cargar_config,
    perfiles_activos,
)
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque


def _bloque(tmp_path, cfg=None, cliente=None):
    return Bloque(cfg or config_pruebas(), ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), cliente or MockClient(),
                  Path(tmp_path) / "estado", Path(tmp_path) / "ent")


def _capturar_ct13(b) -> list[dict]:
    """Guarda el cuerpo de cada mensaje CT-13 (el registro de la mensajería solo guarda la cabecera)."""
    cuerpos: list[dict] = []
    crear = b.mensajeria.crear

    def _crear(contrato, emisor, receptor, cuerpo, **kw):
        if contrato == "CT-13":
            cuerpos.append(json.loads(json.dumps(cuerpo, default=str)))
        return crear(contrato, emisor, receptor, cuerpo, **kw)
    b.mensajeria.crear = _crear
    return cuerpos


# ---------------------------------------------------------------- PA-01 · solo el perfil de divisas activo por defecto
def test_pa01_por_defecto_solo_divisas():
    assert perfiles_activos(cargar_config()) == ["DIV"]


@pytest.mark.parametrize("perfiles", [{}, {"activos": []}, {"activos": ["DIV", "XXX"]}])
def test_pa01_sin_perfiles_validos_falla_cerrado(perfiles):
    with pytest.raises(ValueError):
        perfiles_activos({"perfiles": perfiles})


def test_pa01_ciclo_por_defecto_analiza_solo_divisas(tmp_path):
    b = _bloque(tmp_path, cfg=cargar_config(extra={"modo": "backtest"}))
    r = b.ciclo(AS_OF)
    assert list(r["paquete"]["clases"]) == ["DIV"]
    assert b.f10()["P-02"] == ["DIV"]


def test_pa01_tipo_no_activo_responde_no_estimable_y_no_redacta(tmp_path):
    b = _bloque(tmp_path, cfg=cargar_config(extra={"modo": "backtest"}))
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert r["estado"] == "PARCIAL" and r["entrega"] == "SIN_RESULTADO" and r["paquete"]["clases"] == {}
    assert any("NO_ESTIMABLE" in x for x in r["paquete"]["limitaciones"])
    assert not (Path(tmp_path) / "ent").exists() or not list((Path(tmp_path) / "ent").rglob("*.json"))


def test_pa01_alcance_mixto_analiza_lo_activo_y_declara_lo_demas(tmp_path):
    b = _bloque(tmp_path, cfg=cargar_config(extra={"modo": "backtest"}))
    r = b.ciclo(AS_OF, alcance={"clases": ["DIV", "CRI"]})
    assert list(r["paquete"]["clases"]) == ["DIV"]
    assert any("Cripto" in x and "NO_ESTIMABLE" in x for x in r["paquete"]["limitaciones"])


# ---------------------------------------------------------------- H-06 (T-65) · todo pausado: se cierra sin redactar
def test_h06_todo_pausado_no_redacta_ni_falla_en_el_esquema(tmp_path):
    b = _bloque(tmp_path)
    b.consultas.enviar({"tipo": "ACLARACION_ALCANCE", "modo": "BLOQUEANTE", "clases": ["CRI"],
                        "preguntas": [{"texto": "¿Incluimos stablecoins?", "supuesto_declarado": "No", "efecto_si_falso": "ámbito"}]}, AS_OF)
    r = b.ciclo(AS_OF, alcance={"clases": ["CRI"]})
    assert r["entrega"] == "SIN_RESULTADO" and r["g3"]["dictamen"] == "SIN_RESULTADO"   # antes: BLOQUEADA por ESQUEMA_JSON
    assert any("pausado" in x for x in r["paquete"]["limitaciones"])
    run = [x for x in b.almacen.leer("F5") if x.get("tipo_entrada") == "RUN"][-1]
    assert run["entrega"] == "SIN_RESULTADO" and run["estado"] == "PARCIAL"


# ---------------------------------------------------------------- PA-05 · Contradictor con evidencia, contrarréplica y veredicto por regla
def test_pa05_el_contradictor_no_recibe_el_razonamiento_del_analista(tmp_path):
    b = _bloque(tmp_path)
    cuerpos = _capturar_ct13(b)
    b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    ct13 = [m for m in cuerpos if m.get("peticiones")]
    assert ct13
    for m in ct13:
        for p in m["peticiones"]:
            assert not {"tesis", "mecanismo", "premortem", "dimensiones"} & set(p)
            assert p["evidencias"] and "afirmaciones_verificables" in p


def _forzar_fuerte(monkeypatch, cita: int, confirma: bool | None):
    """AG-11 pone una objeción fuerte a todas; el Analista la da por resuelta citando `cita` evidencias; AG-11 confirma o no."""
    orig_contr, orig_an = mr._contrarias, mr._analista

    def contrarias(msg, ctx, rng):
        if "contrarreplicas" in msg:
            if confirma is None:
                return orig_contr(msg, ctx, rng)
            return {"resultados": [{"objecion_id": x["objecion_id"], "resuelta": confirma, "motivo": "forzado"} for x in msg["contrarreplicas"]]}
        out = orig_contr(msg, ctx, rng)
        for x in out["resultados"]:
            x["objeciones"] = [o for o in x["objeciones"] if o["fuerza"] != "fuerte"] + [
                {"id": f"OBJ-{x['ref']}-09", "tipo": "evidencia_insuficiente", "fuerza": "fuerte", "argumento": "Forzada",
                 "evidencia": "-", "que_la_resolveria": "Dos fuentes independientes"}]
        return out

    def analista(msg, ctx, rng, iny):
        if msg.get("fase") == "RESPUESTA_OBJECIONES":
            return {"respuestas": [{"objecion_id": o["objecion_id"], "respuesta": "Resuelta, según el Analista", "resuelta": True,
                                    "evidencia_citada": list(o.get("evidencia_disponible") or [])[:cita]} for o in msg["objeciones"]]}
        return orig_an(msg, ctx, rng, iny)
    monkeypatch.setattr(mr, "_contrarias", contrarias)
    monkeypatch.setattr(mr, "_analista", analista)


def _fuertes(b):
    f3 = b.almacen.estado("F3").values()
    return [o for x in f3 for o in (x.get("objeciones_internas") or []) if o["fuerza"] == "fuerte"]


def test_pa05_el_analista_no_resuelve_solo_una_objecion_fuerte_sin_evidencia(tmp_path, monkeypatch):
    _forzar_fuerte(monkeypatch, cita=0, confirma=True)
    b = _bloque(tmp_path)
    cuerpos = _capturar_ct13(b)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert _fuertes(b) and not any(o["resuelta"] for o in _fuertes(b))      # antes: «resuelta» del propio Analista
    assert not r["paquete"]["clases"]["RV"]["opciones"]
    assert not [m for m in cuerpos if m.get("contrarreplicas")]


def test_pa05_sin_confirmacion_del_contradictor_sigue_abierta(tmp_path, monkeypatch):
    _forzar_fuerte(monkeypatch, cita=2, confirma=False)
    b = _bloque(tmp_path)
    cuerpos = _capturar_ct13(b)
    b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert _fuertes(b) and not any(o["resuelta"] for o in _fuertes(b))
    assert [m for m in cuerpos if m.get("contrarreplicas")]


def test_pa05_con_evidencia_y_confirmacion_queda_resuelta_y_la_tesis_es_fragil(tmp_path, monkeypatch):
    _forzar_fuerte(monkeypatch, cita=2, confirma=True)
    b = _bloque(tmp_path)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert _fuertes(b) and all(o["resuelta"] and o["evidencia_citada"] for o in _fuertes(b))
    ops = r["paquete"]["clases"]["RV"]["opciones"]
    assert ops and all(o["confianza"] == "especulativo" for o in ops)            # tesis frágil → especulativo
    f3 = [x for x in b.almacen.estado("F3").values() if x.get("estado") == "PUBLICADA" or x.get("rango_top3")]
    assert f3 and all(x["veredicto_refutacion"] == "tesis frágil" for x in f3)


@pytest.mark.parametrize("objs, esperado", [
    ([{"fuerza": "fuerte", "resuelta": False}], "tesis refutada"),
    ([{"fuerza": "fuerte", "resuelta": True}], "tesis frágil"),
    ([{"fuerza": "moderada", "resuelta": True}, {"fuerza": "moderada", "resuelta": True}], "tesis frágil"),
    ([{"fuerza": "moderada", "resuelta": True}, {"fuerza": "debil", "resuelta": False}], "tesis robusta"),
    ([], "tesis robusta"),
])
def test_pa05_veredicto_por_regla(tmp_path, objs, esperado):
    b = _bloque(tmp_path)
    assert b._veredicto_refutacion({"_objeciones": objs}) == esperado


# ---------------------------------------------------------------- PA-09 · contaminación por conocimiento del modelo
class ClienteConMemoria(MockClient):
    """Simulado que se declara como un modelo real (con conocimiento previo del periodo)."""
    conocimiento_previo = True


def test_pa09_backtest_con_modelo_real_antes_del_corte_marca_y_anonimiza(tmp_path):
    b = _bloque(tmp_path, cliente=ClienteConMemoria())
    assert b.anon is not None                                                   # anonimizar: auto
    b.ciclo(AS_OF, alcance={"clases": ["DIV"]})
    altas = [p for p in b.almacen.leer("F4") if p.get("tipo_entrada") == "ALTA"]
    assert altas and all(p["contaminacion_posible"] is True for p in altas)


def test_pa09_simulado_y_fechas_posteriores_al_corte_no_se_marcan(tmp_path):
    b = _bloque(tmp_path)
    assert b.anon is None and b.contaminacion_posible(AS_OF) is False
    b2 = _bloque(Path(tmp_path) / "b", cliente=ClienteConMemoria())
    assert b2.contaminacion_posible("2026-07-15") is False and b2.contaminacion_posible("2026-06-30") is True
    b3 = _bloque(Path(tmp_path) / "c", cfg=config_pruebas(modo="vivo"), cliente=ClienteConMemoria())
    assert b3.contaminacion_posible(AS_OF) is False                             # en vivo no hay periodo pasado que recordar


def test_pa09_sin_fecha_de_corte_falla_cerrado(tmp_path):
    b = _bloque(tmp_path, cfg=config_pruebas(backtest={"fecha_corte_modelo": None}), cliente=ClienteConMemoria())
    assert b.contaminacion_posible("2030-01-01") is True


# ---------------------------------------------------------------- PA-14 · ablación determinista
def test_pa14_cada_run_registra_la_ablacion_por_tipo(tmp_path):
    b = _bloque(tmp_path)
    b.ciclo(AS_OF, alcance={"clases": ["RV", "DIV"]})
    run = [x for x in b.almacen.leer("F5") if x.get("tipo_entrada") == "RUN"][-1]
    for c in ("RV", "DIV"):
        a = run["ablacion"][c]
        assert set(a) == {"top3", "sin_objeciones", "referencia_simple"}
        assert a["referencia_simple"]["criterio"] == "señal compuesta" and len(a["referencia_simple"]["simbolos"]) <= 3


def test_pa14_una_objecion_fuerte_que_excluye_se_ve_en_la_ablacion(tmp_path, monkeypatch):
    _forzar_fuerte(monkeypatch, cita=0, confirma=True)
    b = _bloque(tmp_path)
    b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    run = [x for x in b.almacen.leer("F5") if x.get("tipo_entrada") == "RUN"][-1]
    a = run["ablacion"]["RV"]
    assert a["top3"] == [] and a["sin_objeciones"]["top3"] and a["sin_objeciones"]["cambia_decision"] is True


# ---------------------------------------------------------------- PA-21 · probabilidad propia del Analista
def test_pa21_la_probabilidad_del_analista_llega_a_f4(tmp_path):
    b = _bloque(tmp_path)
    b.ciclo(AS_OF, alcance={"clases": ["DIV"]})
    altas = [p for p in b.almacen.leer("F4") if p.get("tipo_entrada") == "ALTA" and not p.get("es_hito") and p["horizonte"] != "H5"]
    assert altas and all(isinstance(p["prob_analista"], float) for p in altas)


@pytest.mark.parametrize("valor, esperado", [(0.7, 0.7), (0.99, None), (0.01, None), ("0.6", None), (True, None), (None, None)])
def test_pa21_valores_fuera_de_rango_no_se_registran(valor, esperado):
    assert sintesis._prob_analista({"probabilidades_propias": {"H2": valor}}, "H2") == esperado


def test_pa21_el_esquema_finalista_admite_la_probabilidad_propia():
    from bloque_a.contratos import FINALISTA
    assert FINALISTA["properties"]["probabilidades_propias"]["additionalProperties"]["maximum"] == 0.95


def test_config_de_pruebas_activa_los_doce_perfiles():
    assert perfiles_activos(config_pruebas()) == list(CLASES)
    assert json.dumps(cargar_config()["contrarias"]) == json.dumps({"moderadas_para_fragil": 2})
