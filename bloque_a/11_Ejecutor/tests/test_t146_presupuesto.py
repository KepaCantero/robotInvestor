"""T-146 · el presupuesto en UC corta antes de cada petición al modelo.

Antes, `Bloque._invocar` comparaba lo disponible con una estimación (2 500 tokens de salida, el system prompt como lectura de
caché, sin reparación ni continuaciones) y cargaba lo real después; la escritura de caché de los agentes compartidos se cargaba
como lectura hasta `liquidar_primas`; AG-18, AG-19 y AG-20 no pasaban por el presupuesto y las búsquedas web no contaban en UC.
Con el peor caso pasado por el cliente real, la bolsa de divisas acababa en 48,4 UC con un límite de 26,3 (T-145).

Aquí el peor caso pasa por el cliente real (`AnthropicClient`) con un SDK falso que no sale de la máquina: cada petición
declara como uso su peor caso (toda la entrada como escritura de caché con el margen del tokenizador, `max_tokens` de salida y
las búsquedas al máximo), los agentes con búsqueda devuelven `pause_turn` hasta agotar las continuaciones y el primer intento de
cada llamada no es JSON (se paga la reparación)."""
from __future__ import annotations

import copy
import json
import types

import pytest
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, parametro
from bloque_a.consumo import (
    Contabilidad,
    Presupuesto,
    ReservaLlamada,
    busquedas_maximas,
    tokens_de_peticion,
)
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import AnthropicClient, MockClient, Uso, con_guarda
from bloque_a.orquestacion import Bloque
from conftest import AS_OF, DATOS, config_pruebas

from bloque_a import mock_respuestas

FACTOR = 1.35   # el de `presupuesto_uc.reserva.factor_tokens_entrada` (se comprueba abajo)


def _tok(texto: str) -> int:
    return max(1, int(len(texto) / 3.6))


def _texto_de(contenido) -> str:
    if isinstance(contenido, str):
        return contenido
    return "".join(getattr(b, "text", "") or "" for b in contenido)


class SDKPeorCaso:
    """SDK falso: cada petición declara el peor caso. La entrada se cuenta aparte de la reserva: lo que escribió el modelo vuelve
    con sus propios tokens (los que se cobraron como salida) y el resto (system, encargo, errores de la reparación) con el
    margen del tokenizador, como en la QA r01 de T-140 (`r01_02_peor_caso_con_cliente_real.py`)."""

    def __init__(self, cont: int, max_usos: int, semilla: int, reparaciones: int = 1, factor_entrada: float = FACTOR) -> None:
        self.cont, self.max_usos, self.semilla, self.reparaciones, self.factor = cont, max_usos, semilla, reparaciones, factor_entrada
        self.peticiones: list[dict] = []
        self.messages = self

    def create(self, **kw):
        agente = kw["metadata"]["user_id"].removeprefix("bloque-a-")
        msgs = kw["messages"]
        salida = int(kw["max_tokens"])
        sys_txt = "".join(b.get("text", "") for b in kw["system"])
        propio = [m for m in msgs if m["role"] == "user"]
        reenviado = sum(_tok(_texto_de(m["content"])) for m in msgs if m["role"] == "assistant")
        entrada = int((_tok(sys_txt) + _tok(json.dumps(propio, ensure_ascii=False))) * self.factor) + reenviado
        con_web = bool(kw.get("tools"))
        pausas = sum(1 for m in msgs if m["role"] == "assistant" and not isinstance(m["content"], str))
        intento = sum(1 for m in msgs if m["role"] == "user")
        largo = "análisis " * int(salida * 3.6 / 9)          # el texto que ocupa max_tokens (y que se reenvía)
        if con_web and pausas < self.cont:
            stop, texto = "pause_turn", largo
        elif intento <= self.reparaciones:
            stop, texto = "end_turn", largo                   # no es JSON: el ejecutor pide la reparación
        else:
            stop = "end_turn"
            texto = json.dumps(mock_respuestas.responder(agente, msgs[:1], self.semilla), ensure_ascii=False)
        busq = self.max_usos if con_web else 0
        self.peticiones.append({"agente": agente, "entrada": entrada, "salida": salida, "busquedas": busq, "stop": stop})
        uso = types.SimpleNamespace(input_tokens=0, output_tokens=salida, cache_creation_input_tokens=entrada, cache_read_input_tokens=0,
                                    server_tool_use=types.SimpleNamespace(web_search_requests=busq))
        return types.SimpleNamespace(stop_reason=stop, usage=uso, content=[types.SimpleNamespace(type="text", text=texto)])


def _cfg(**extra):
    base = {"modo": "vivo", "perfiles": {"activos": ["DIV"]}}
    from bloque_a.configuracion import fusionar
    return config_pruebas(**fusionar(base, extra))


def _bloque(tmp, cfg, cliente):
    return Bloque(cfg, ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), cliente, tmp / "estado", tmp / "ent")


def _peor_ciclo(tmp, cfg, reparaciones=1, factor_entrada=FACTOR):
    sdk = SDKPeorCaso(int(cfg["llm"]["max_continuaciones_pause_turn"]), int(cfg["busqueda_web"]["max_usos_por_llamada"]),
                      int(cfg["llm"]["semilla_mock"]), reparaciones, factor_entrada)
    b = _bloque(tmp, cfg, AnthropicClient(sdk=sdk, max_continuaciones=int(cfg["llm"]["max_continuaciones_pause_turn"])))
    return b, b.ciclo(AS_OF, nivel_forzado="N2"), sdk


def _limites(cfg, v):
    """El límite de la bolsa y el de la ampliación máxima (`Presupuesto.limite` y `limite_maximo`). T-146 r02 (QA r01, H-07):
    lo asignado de F5 es el que se aplicó (escalado si el reparto pasa del ciclo, H-06), así que el cálculo vale también con
    escala; antes usaba el asignado sin escalar y no habría visto H-03."""
    pu = cfg["presupuesto_uc"]
    return v["asignado"] * (1 + pu["ampliacion_sin_autorizacion"]) + v["ampliado"], v["asignado"] * (1 + pu["ampliacion_max_autorizable"])


def _comprobar_cotas(b, r, cfg):
    """Ninguna bolsa pasa de su límite ni del de la ampliación máxima; la suma no pasa del ciclo con esa ampliación; todo lo que
    se gastó está cargado en alguna bolsa (nada queda fuera del presupuesto)."""
    pres = r["presupuesto"]
    for bolsa, v in pres.items():
        limite, maximo = _limites(cfg, v)
        assert v["consumido"] <= limite + 1e-6, (bolsa, v)
        assert limite <= maximo + 1e-6, (bolsa, v)
    tope = cfg["presupuesto_uc"]["ciclo_semanal_max"] * (1 + cfg["presupuesto_uc"]["ampliacion_max_autorizable"])
    total = sum(v["consumido"] for v in pres.values())
    assert total <= tope
    assert sum(_limites(cfg, v)[1] for v in pres.values()) <= tope + 1e-3   # la suma de los límites máximos (H-07)
    gastado = sum(x["uc"] for x in b.contabilidad.llamadas if x["run_id"] == r["run_id"])
    assert total == pytest.approx(gastado, abs=0.01)   # redondeo de 0,0001 por llamada
    run = b.almacen.estado("F5", clave="id")[r["run_id"]]
    assert "excesos_reserva" not in run                 # ninguna petición costó más de lo que reservó
    return run


# ---------------------------------------------------------------- CA-1 · el peor caso, solo divisas (configuración por defecto)
def test_ca1_peor_caso_divisas_ninguna_bolsa_pasa_de_su_limite(tmp_path):
    cfg = _cfg()
    b, r, sdk = _peor_ciclo(tmp_path, cfg)
    run = _comprobar_cotas(b, r, cfg)
    # T-145 medía 48,4 UC en DIV con un límite de 26,3: ahora el límite manda
    assert r["presupuesto"]["DIV"]["consumido"] <= _limites(cfg, r["presupuesto"]["DIV"])[0] + 1e-6
    # el ciclo termina, PARCIAL y con lo recortado declarado en el paquete y en F5
    assert r["estado"] == "PARCIAL" and run["cierres_parciales"]
    assert any(x.startswith("Presupuesto agotado en DIV") for x in r["paquete"]["limitaciones"])
    assert all("UC en el peor caso" in c["motivo"] for c in run["cierres_parciales"])
    # se pagaron reparaciones y continuaciones: cada una salió solo después de reservar la suya
    assert any(p["stop"] == "pause_turn" for p in sdk.peticiones) and len(sdk.peticiones) > len(b.contabilidad.llamadas) // 2


def test_ca1_las_ampliaciones_nunca_pasan_de_la_maxima(tmp_path):
    cfg = _cfg()
    b, r, _ = _peor_ciclo(tmp_path, cfg)
    for v in r["presupuesto"].values():
        assert v["ampliado"] <= v["asignado"] * (cfg["presupuesto_uc"]["ampliacion_max_autorizable"]
                                                 - cfg["presupuesto_uc"]["ampliacion_sin_autorizacion"]) + 1e-6
    auts = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "AUT" and e["run_id"] == r["run_id"]]
    assert auts and {e["decision"] for e in auts} <= {"AUTORIZADA", "DENEGADA"}


# ---------------------------------------------------------------- CA-2 · los doce tipos, con hilos
def test_ca2_peor_caso_doce_tipos_con_hilos(tmp_path):
    cfg = _cfg(perfiles={"activos": ["RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV"]},
               paralelismo={"hilos_analistas": 6})
    b, r, _ = _peor_ciclo(tmp_path, cfg)
    _comprobar_cotas(b, r, cfg)
    assert r["estado"] == "PARCIAL" and r["entregables"]   # termina y entrega con lo recortado declarado


def test_ca2_determinista_con_hilos_cerca_del_limite(tmp_path):
    """T-88: con varios hilos y las bolsas al límite, el presupuesto, los cierres y los recortes no dependen del orden."""
    cfg = _cfg(perfiles={"activos": ["RV", "RF", "DIV", "MP"]}, paralelismo={"hilos_analistas": 4})
    vistos = set()
    for k in range(2):
        b, r, _ = _peor_ciclo(tmp_path / str(k), copy.deepcopy(cfg))
        run = b.almacen.estado("F5", clave="id")[r["run_id"]]
        vistos.add(json.dumps([run["presupuesto"], run["cierres_parciales"], run.get("recortes_salida")], sort_keys=True))
    assert len(vistos) == 1


def test_ca2_v6_peor_caso_ninguna_bolsa_pasa_de_su_limite(tmp_path):
    cfg = _cfg(diseno="v6", perfiles={"activos": ["DIV", "RV"]})
    b, r, _ = _peor_ciclo(tmp_path, cfg)
    _comprobar_cotas(b, r, cfg)


# ---------------------------------------------------------------- CA-3 · AG-18, AG-19 y AG-20 dentro del presupuesto
def _res_eval_con_resueltos():
    return {"resueltos": 3, "metricas": {"DIV|H2": {"n": 3, "brier": 0.2, "brier_ref": 0.25, "acierto": {"tasa": 0.66},
                                                    "calibracion_global": None}},
            "certificados": {"emitidos": [], "insuficientes": []}, "lecciones_nuevas": []}


def test_ca3_ag18_ag19_y_ag20_cargan_en_la_bolsa_comun(tmp_path, monkeypatch):
    cfg = _cfg(auditoria={"en_vivo": True})
    b = _bloque(tmp_path, cfg, MockClient())
    monkeypatch.setattr(b.evaluador, "ciclo", lambda as_of, run_id: _res_eval_con_resueltos())
    r = b.ciclo(AS_OF)
    ll = [x for x in b.contabilidad.llamadas if x["run_id"] == r["run_id"]]
    agentes = {x["agente"] for x in ll}
    assert {"AG-20", "AG-19"} <= agentes
    # todo lo gastado está en las bolsas: también AG-20 (antes del reparto) y AG-19 (después del registro)
    assert sum(v["consumido"] for v in r["presupuesto"].values()) == pytest.approx(sum(x["uc"] for x in ll), abs=0.01)
    assert r["presupuesto"]["COMUN"]["consumido"] >= sum(x["uc"] for x in ll if x["agente"] in ("AG-18", "AG-19", "AG-20")) - 0.01


def test_ca3_sin_sitio_ag20_no_sale_y_se_declara(tmp_path, monkeypatch):
    cfg = _cfg()
    b = _bloque(tmp_path, cfg, MockClient())
    monkeypatch.setattr(b.evaluador, "ciclo", lambda as_of, run_id: _res_eval_con_resueltos())
    r = b.ciclo(AS_OF, presupuesto_override={"COMUN": 0.01})
    assert "AG-20" not in {x["agente"] for x in b.contabilidad.llamadas}
    assert any(c["clase"] == "COMUN" and "AG-20" in c["motivo"] for c in b.almacen.estado("F5", clave="id")[r["run_id"]]["cierres_parciales"])


def test_ca3_los_controles_admiten_ampliacion(tmp_path):
    """R16: el dictamen G3 y la auditoría pueden pedir la ampliación (con su AUT- en HA); otra fase transversal, no."""
    b = _bloque(tmp_path, _cfg(), MockClient())
    b.fijar_fecha(AS_OF)
    p = Presupuesto({"COMUN": 10.0}, b.cfg)
    p.cargar("COMUN", 12.0)
    assert b._solicitar_ampliacion(p, "COMUN", 1.0, "RUN-2026-0001", "CT-17", control=True)
    assert not b._solicitar_ampliacion(p, "COMUN", 0.5, "RUN-2026-0001", "integracion")
    aut = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "AUT"]
    assert [e["decision"] for e in aut] == ["AUTORIZADA", "DENEGADA"] and "R16" in aut[0]["valor_informacion"]


# ---------------------------------------------------------------- CA-4 · las búsquedas cuentan en UC
def test_ca4_las_busquedas_cuentan_en_uc():
    cfg = _cfg()
    c = Contabilidad(cfg)
    ub = float(parametro(cfg, "uc.uc_por_busqueda_web"))
    assert ub > 0 and c.uc_de(Uso(busquedas_web=3)) == pytest.approx(3 * ub)
    c.registrar("RUN-1", "AG-14", "m", Uso(entrada=8000, busquedas_web=2))
    assert c.resumen("RUN-1")["uc_llm"] == pytest.approx(0.5 + 2 * ub)
    herr = [{"type": "web_search_20260318", "name": "web_search", "max_uses": 5}]
    assert busquedas_maximas(herr) == 5 and busquedas_maximas(None) == 0
    p = Presupuesto({"DIV": 100.0}, cfg)
    g = ReservaLlamada(p, "DIV", c, "AG-14")
    assert g.reservar([{"text": "x" * 360}], [], herr, 1500) == 1500
    con, sin = p.reservado["DIV"], None
    g.cerrar()
    g2 = ReservaLlamada(p, "DIV", c, "AG-14")
    g2.reservar([{"text": "x" * 360}], [], None, 1500)
    sin = p.reservado["DIV"]
    assert con - sin == pytest.approx(5 * ub, abs=0.01)


# ---------------------------------------------------------------- CA-5 · la reserva petición a petición
def _guarda(asignado, cfg=None, **kw):
    cfg = cfg or _cfg()
    p = Presupuesto({"DIV": asignado}, cfg)
    return p, ReservaLlamada(p, "DIV", Contabilidad(cfg), "AG-05", **kw), cfg


def test_ca5_reserva_el_peor_caso_y_cobra_lo_real():
    p, g, cfg = _guarda(10.0)
    system, msgs = [{"text": "s" * 36000}], [{"role": "user", "content": "u" * 3600}]
    tokens = tokens_de_peticion(system, msgs, None)
    peor = Contabilidad(cfg).uc_de(Uso(entrada=int(-(-tokens * FACTOR // 1)), salida=3000))
    assert float(parametro(cfg, "presupuesto_uc.reserva.factor_tokens_entrada")) == FACTOR
    assert g.reservar(system, msgs, None, 3000) == 3000 and p.reservado["DIV"] == pytest.approx(peor)
    g.pagar_resto(Uso(entrada=100, salida=100))            # lo real, mucho menos: queda apartado hasta cerrar
    real = Contabilidad(cfg).uc_de(Uso(entrada=100, salida=100))
    assert p.reservado["DIV"] == pytest.approx(real)
    g.cerrar()
    assert p.reservado["DIV"] == 0 and p.consumido["DIV"] == 0   # lo carga después `Bloque._cargar`


def test_ca5_si_no_cabe_recorta_la_salida_y_por_debajo_del_minimo_no_sale():
    p, g, cfg = _guarda(2.0)                                # límite 2,5 UC
    system = [{"text": "s" * 3600}]                          # 1 000 tokens de entrada
    mt = g.reservar(system, [], None, 12000)                # 12 000 de salida serían 4 UC
    assert mt is not None and 2500 <= mt < 12000
    assert p.reservado["DIV"] <= p.limite("DIV") + 1e-9 and p.recortes and p.recortes[0]["max_tokens_enviado"] == mt
    g.cerrar()
    p.cargar("DIV", p.limite("DIV") - 0.5)                  # queda 0,5 UC: menos de la salida mínima
    g2 = ReservaLlamada(p, "DIV", Contabilidad(cfg), "AG-05")
    assert g2.reservar(system, [], None, 12000) is None and "UC en el peor caso" in g2.negada
    assert p.reservado["DIV"] == 0


def test_ca5_pide_la_ampliacion_antes_de_recortar():
    pedidas = []

    def ampliar(est):
        pedidas.append(est)
        p.ampliar("DIV", est)
        return True
    p, g, _ = _guarda(2.0, ampliar=ampliar)
    assert g.reservar([{"text": "s" * 3600}], [], None, 12000) == 12000 and pedidas and not p.recortes


def test_ca5_cada_continuacion_reserva_la_suya_y_la_que_no_cabe_no_sale():
    """El cliente real con `pause_turn`: la primera petición la reserva `Agentes`, cada continuación la suya dentro del cliente."""
    cfg = _cfg()
    sdk = SDKPeorCaso(cont=3, max_usos=5, semilla=1)
    cli = AnthropicClient(sdk=sdk, max_continuaciones=3)
    herr = [{"type": "web_search_20260318", "name": "web_search", "max_uses": 5}]
    system, msgs = [{"type": "text", "text": "s" * 3600}], [{"role": "user", "content": "hola"}]
    p, g, _ = _guarda(4.0, cfg)                              # límite 5 UC: caben la primera y quizá una continuación
    mt = g.reservar(system, msgs, herr, 3000)
    with con_guarda(g):
        r = cli.generar(agente="AG-16", modelo="m", system=system, mensajes=msgs, max_tokens=mt, herramientas=herr)
    g.pagar_resto(r.uso)
    assert r.stop_reason == "presupuesto_agotado" and 1 <= len(sdk.peticiones) < 4
    assert g.peticiones == len(sdk.peticiones)               # ninguna salió sin su reserva
    assert p.reservado["DIV"] <= p.limite("DIV") + 1e-9      # lo apartado (real) cabe en el límite
    g.cerrar()


def test_ca5_el_factor_observado_sube_si_la_entrada_mide_mas():
    p, g, cfg = _guarda(100.0)
    system = [{"text": "s" * 36000}]                          # 10 000 tokens estimados
    g.reservar(system, [], None, 100)
    g.pagar_resto(Uso(entrada=20000, salida=10))              # el doble de lo estimado: más que el margen
    assert p.factor_de("DIV", FACTOR) == pytest.approx(2.0, rel=1e-3) and p.excesos
    antes = p.reservado["DIV"]
    g.reservar(system, [], None, 100)
    assert p.reservado["DIV"] - antes == pytest.approx(Contabilidad(cfg).uc_de(Uso(entrada=20000, salida=100)), abs=0.01)
    g.cerrar()


def test_ca5_la_reserva_cuenta_en_la_ampliacion():
    """`autorizar_hasta_tope` cuenta lo reservado y lo retenido como ocupado: no se autoriza dos veces lo mismo."""
    p, _, _ = _guarda(10.0)
    p.reservar("DIV", 12.0)
    concede, falta = p.autorizar_hasta_tope("DIV", 1.0, True)
    assert concede and falta == pytest.approx(0.5)


# ---------------------------------------------------------------- CA-6 · la liquidación de las primas no pasa de lo retenido
def test_ca6_la_escritura_fuera_del_prefijo_se_carga_ya_y_la_prima_queda_retenida():
    cfg = _cfg()
    fake = types.SimpleNamespace(contabilidad=Contabilidad(cfg), v6=False)
    p = Presupuesto({"RV": 50, "RF": 50, "COMUN": 50}, cfg)
    r = types.SimpleNamespace(uso=Uso(entrada=0, salida=0, cache_escritura=50000, cache_lectura=0), cache_hit=False, intentos=1, uc=0.0)
    Bloque._cargar(fake, p, "RF", "AG-14", r, prefijo=20000)   # el prefijo es 20 000; el resto se escribió aparte
    lectura = fake.contabilidad.uc_de(Uso(entrada=30000, cache_lectura=20000))
    assert p.consumido["RF"] == pytest.approx(lectura) and p.retenido["RF"] == pytest.approx(p._uc_prima(20000))
    antes = p.consumido["RF"] + p.retenido["RF"]
    p.liquidar_primas()
    assert p.consumido["RF"] <= antes + 1e-9 and not p.retenido


def test_ca6_la_suma_de_limites_no_pasa_del_ciclo():
    cfg = _cfg()
    pu = cfg["presupuesto_uc"]
    asign = {c: float(pu["N3"]) for c in ("RV", "RF", "DIV", "MP", "IDX", "FON")}
    asign["COMUN"] = 24.0
    p = Presupuesto(asign, cfg, tope_total=float(pu["ciclo_semanal_max"]))
    assert sum(p.limite_maximo(b) for b in asign) == pytest.approx(pu["ciclo_semanal_max"] * (1 + pu["ampliacion_max_autorizable"]))
    sin_tope = Presupuesto(asign, cfg)
    assert sin_tope.limite("RV") == pytest.approx(pu["N3"] * (1 + pu["ampliacion_sin_autorizacion"]))


# ---------------------------------------------------------------- CA-7 · con el simulado, los ciclos de siempre
def test_ca7_con_el_simulado_un_ciclo_n2_no_recorta_ni_cierra(tmp_path):
    cfg = _cfg()
    b = _bloque(tmp_path, cfg, MockClient())
    r = b.ciclo(AS_OF, nivel_forzado="N2")
    run = b.almacen.estado("F5", clave="id")[r["run_id"]]
    assert r["estado"] == "COMPLETO" and not run["cierres_parciales"] and "recortes_salida" not in run
    assert not [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "AUT"]
    assert sum(v["consumido"] for v in r["presupuesto"].values()) == pytest.approx(
        sum(x["uc"] for x in b.contabilidad.llamadas if x["run_id"] == r["run_id"]), abs=0.01)


def test_ca7_con_el_simulado_un_ciclo_n1_recorta_la_salida_del_analista_y_sigue_completo(tmp_path):
    """En N1 (5 UC y +25 %) el peor caso del Analista apenas cabe (en el backtest de ejemplo, 6,31 UC frente a 6,25 en las
    semanas N1). Con una salida máxima mayor no cabe: se deniega la ampliación (la fase de cribado no la admite) y sale con la
    salida que cabe. El ciclo sigue COMPLETO."""
    cfg = _cfg(max_tokens={"AG-05": 15000})
    b = _bloque(tmp_path, cfg, MockClient())
    r = b.ciclo(AS_OF, nivel_forzado="N1")
    run = b.almacen.estado("F5", clave="id")[r["run_id"]]
    assert r["estado"] == "COMPLETO" and not run["cierres_parciales"]
    rec = run["recortes_salida"]
    assert [x["agente"] for x in rec] == ["AG-05"] and 2500 <= rec[0]["max_tokens_enviado"] < rec[0]["max_tokens"]
    assert r["presupuesto"]["DIV"]["consumido"] <= _limites(cfg, r["presupuesto"]["DIV"])[0]


def _agentes(tmp, cliente, cfg):
    from bloque_a.agentes import Agentes
    from bloque_a.almacen import Almacen
    return Agentes(cfg, cliente, Almacen(tmp / "estado"), Contabilidad(cfg), cache=None)


C08 = {"agente": "AG-16", "contrato": "CT-08", "mensaje": {"pregunta": "¿qué dice el banco central?"}, "esquema_clave": "BUSQUEDA",
       "instrucciones": "Busca", "contexto": {"fecha_as_of": "2026-06-05", "modo": "vivo"}, "permitir_web": True}


def test_ca5_agentes_la_continuacion_que_no_cabe_deja_la_llamada_parcial_sin_reparar(tmp_path):
    cfg = _cfg()
    sdk = SDKPeorCaso(cont=3, max_usos=5, semilla=1)
    a = _agentes(tmp_path, AnthropicClient(sdk=sdk, max_continuaciones=3), cfg)
    p = Presupuesto({"DIV": 6.0}, cfg)
    g = ReservaLlamada(p, "DIV", a.contabilidad, "AG-16")
    r = a.invocar(**C08, guarda=g)
    g.cerrar()
    assert r.estado == "PARCIAL" and any("presupuesto_agotado" in e for e in r.errores)
    assert all(x["stop"] == "pause_turn" for x in sdk.peticiones)   # no se pidió la reparación
    assert g.peticiones == len(sdk.peticiones) and g.negada


def test_ca5_agentes_sin_sitio_para_la_primera_no_sale_ninguna(tmp_path):
    cfg = _cfg()
    sdk = SDKPeorCaso(cont=3, max_usos=5, semilla=1)
    a = _agentes(tmp_path, AnthropicClient(sdk=sdk, max_continuaciones=3), cfg)
    p = Presupuesto({"DIV": 0.1}, cfg)
    g = ReservaLlamada(p, "DIV", a.contabilidad, "AG-16")
    r = a.invocar(**C08, guarda=g)
    assert r.estado == "SIN_PRESUPUESTO" and not sdk.peticiones and not a.contabilidad.llamadas


def test_ca3_el_dictamen_g3_de_ag18_carga_en_la_bolsa_comun(tmp_path):
    """Con los 12 tipos y los datos de ejemplo del 29-03-2024, G3 da advertencias y dictamina el Orquestador (AG-18)."""
    cfg = _cfg(perfiles={"activos": ["RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV"]})
    b = _bloque(tmp_path, cfg, MockClient())
    r = b.ciclo("2024-03-29")
    ll = [x for x in b.contabilidad.llamadas if x["run_id"] == r["run_id"]]
    assert "AG-18" in {x["agente"] for x in ll}
    assert sum(v["consumido"] for v in r["presupuesto"].values()) == pytest.approx(sum(x["uc"] for x in ll), abs=0.01)


# ================================================================ r02 · hallazgos de la QA r01
class SDKCacheYBusquedas(SDKPeorCaso):
    """El peor caso de `SDKPeorCaso` con una caché de prompts como la de la API (el primero que envía un system prompt lo
    escribe y los demás lo leen; quién llega antes depende del orden de los hilos) y lo que lee cada búsqueda (`lectura`
    tokens), que la API cobra como entrada de la misma petición (QA r01, `r01_02_ciclo_sdk_hostil.py --cache --lectura`)."""

    def __init__(self, *a, lectura: int = 0, **kw) -> None:
        super().__init__(*a, **kw)
        self.lectura, self.vistos = lectura, set()
        import threading
        self.cerrojo = threading.Lock()

    def create(self, **kw):
        r = super().create(**kw)
        u = r.usage
        sistema = int(_tok("".join(b.get("text", "") for b in kw["system"])) * self.factor)
        clave = json.dumps([kw["model"], kw.get("tools"), kw["system"]], sort_keys=True, default=str)
        with self.cerrojo:
            leido = clave in self.vistos
            self.vistos.add(clave)
        # el punto de caché está al final del system prompt: lo de después (encargo, reparación, continuación) es entrada
        resto = u.cache_creation_input_tokens - sistema
        u.cache_read_input_tokens, u.cache_creation_input_tokens = (sistema, 0) if leido else (0, sistema)
        u.input_tokens = resto + u.server_tool_use.web_search_requests * self.lectura
        return r


def _ciclo_en_orden(tmp, cfg, orden, lectura=0):
    """Un ciclo con los hilos de los tipos uno detrás de otro en `orden` (cada uno espera al anterior): quién escribe antes el
    prefijo compartido de AG-10, AG-12 o AG-14 queda fijado por el orden, sin depender de los tiempos de la máquina."""
    import threading
    sdk = SDKCacheYBusquedas(int(cfg["llm"]["max_continuaciones_pause_turn"]), int(cfg["busqueda_web"]["max_usos_por_llamada"]),
                             int(cfg["llm"]["semilla_mock"]), lectura=lectura)
    b = _bloque(tmp, cfg, AnthropicClient(sdk=sdk, max_continuaciones=int(cfg["llm"]["max_continuaciones_pause_turn"])))
    hechos = {c: threading.Event() for c in orden}
    original = b._analizar_clase_en_ambito

    def en_orden(clase, *args):
        i = orden.index(clase)
        if i:
            assert hechos[orden[i - 1]].wait(600)
        try:
            return original(clase, *args)
        finally:
            hechos[clase].set()
    b._analizar_clase_en_ambito = en_orden
    r = b.ciclo(AS_OF, nivel_forzado="N2")
    run = b.almacen.estado("F5", clave="id")[r["run_id"]]
    from collections import Counter
    llamadas = dict(sorted(Counter(x["agente"] for x in b.contabilidad.llamadas).items()))
    return b, r, sdk, json.dumps([run["presupuesto"], run["cierres_parciales"], run.get("recortes_salida"),
                                  run.get("excesos_reserva"), llamadas], sort_keys=True)


CUATRO = ["RV", "RF", "DIV", "MP"]


def test_r02_h02_con_cache_compartida_el_orden_de_los_hilos_no_cambia_f5(tmp_path):
    """H-02 (alta): con una caché de prompts compartida, lo que se apartaba entre peticiones dependía de si otro hilo había
    escrito antes el prefijo (lo leído cuesta una décima parte), y con eso se decidía si cabían la reparación y las
    continuaciones: F5 cambiaba con el orden de los hilos (T-88). Ahora lo apartado cuenta lo leído como escrito."""
    cfg = _cfg(perfiles={"activos": CUATRO}, paralelismo={"hilos_analistas": 4})
    firmas, lecturas = set(), 0
    for k, orden in enumerate((CUATRO, CUATRO[::-1])):
        b, r, _sdk, firma = _ciclo_en_orden(tmp_path / str(k), copy.deepcopy(cfg), orden)
        firmas.add(firma)
        lecturas += sum(x["cache_lectura"] for x in b.contabilidad.llamadas)
        _comprobar_cotas(b, r, cfg)
    assert lecturas > 0          # el SDK sí devuelve lectura de caché (el de CA-2 no: H-07)
    assert len(firmas) == 1


def test_r02_h02_lo_apartado_cuenta_lo_leido_como_escrito():
    p, g, cfg = _guarda(100.0)
    g.reservar([{"text": "s" * 36000}], [], None, 100)
    g.pagar_resto(Uso(entrada=10, salida=10, cache_lectura=9000))
    assert p.reservado["DIV"] == pytest.approx(Contabilidad(cfg).uc_de(Uso(entrada=10, salida=10, cache_escritura=9000)))
    g.cerrar()


def test_r02_h01_lo_que_leen_las_busquedas_no_sube_el_factor_de_la_bolsa():
    """H-01 (alta): la entrada de una petición con búsquedas trae lo que leyeron (no es error del tokenizador). Antes subía
    el factor observado de la bolsa (a unos 4,7 con 5 × 6 000 tokens) y doblaba las reservas siguientes."""
    herr = [{"type": "web_search_20260318", "name": "web_search", "max_uses": 5}]
    system, msgs = [{"text": "s" * 21600}], [{"role": "user", "content": "u" * 7200}]
    p, g, cfg = _guarda(100.0)
    bruto = tokens_de_peticion(system, msgs, herr)
    g.reservar(system, msgs, herr, 3000)
    g.pagar_resto(Uso(cache_escritura=bruto, entrada=5 * 6000, salida=3000, busquedas_web=5))
    g.cerrar()
    assert not p.factor_observado and p.excesos and p.excesos[0]["busquedas_web"] == 5   # queda anotado, con sus búsquedas
    limpia = ReservaLlamada(Presupuesto({"DIV": 100.0}, cfg), "DIV", Contabilidad(cfg), "AG-10")
    limpia.reservar(system, msgs, None, 3000)
    despues = ReservaLlamada(p, "DIV", Contabilidad(cfg), "AG-10")
    despues.reservar(system, msgs, None, 3000)
    assert despues.peor_total == pytest.approx(limpia.peor_total)
    # sin búsquedas, el margen que no basta sí sube el factor (CA-5)
    g2 = ReservaLlamada(p, "DIV", Contabilidad(cfg), "AG-10")
    g2.reservar(system, msgs, None, 3000)
    g2.pagar_resto(Uso(cache_escritura=2 * bruto, salida=3000))
    assert p.factor_observado["DIV"] > FACTOR


def test_r02_h01_en_un_ciclo_la_lectura_de_las_busquedas_no_cierra_fases(tmp_path, monkeypatch):
    """En el ciclo con búsquedas (modo vivo), lo que leen no cambia las llamadas que caben: la Prospectiva y los demás hacen
    las mismas llamadas que sin lectura (antes, con 3 000 tokens por búsqueda, la Prospectiva de los 12 tipos pasaba de 18 a
    14 llamadas) y ninguna bolsa observa un factor."""
    vistos = []
    monkeypatch.setattr(Presupuesto, "observar_factor", lambda self, clase, factor: vistos.append((clase, factor)))
    cfg = _cfg(perfiles={"activos": CUATRO}, paralelismo={"hilos_analistas": 4})
    llamadas = []
    for k, lectura in enumerate((0, 3000)):
        b, _r, sdk, _ = _ciclo_en_orden(tmp_path / str(k), copy.deepcopy(cfg), CUATRO, lectura)
        assert any(p["busquedas"] for p in sdk.peticiones)
        from collections import Counter
        llamadas.append(Counter(x["agente"] for x in b.contabilidad.llamadas))
    assert llamadas[0] == llamadas[1] and not vistos


def test_r02_h04_la_lectura_por_busqueda_se_reserva_si_se_configura():
    """H-04 (media): `presupuesto_uc.reserva.tokens_lectura_por_busqueda` (`[PROPUESTO]`, por defecto 0: sin dato medido)
    se reserva por cada búsqueda posible; un valor negativo falla cerrado."""
    herr = [{"type": "web_search_20260318", "name": "web_search", "max_uses": 5}]
    system = [{"text": "s" * 3600}]
    cfg0 = _cfg()
    assert parametro(cfg0, "presupuesto_uc.reserva.tokens_lectura_por_busqueda") == 0
    cfg = _cfg(presupuesto_uc={"reserva": {"tokens_lectura_por_busqueda": 4000}})
    reservas = []
    for c in (cfg0, cfg):
        g = ReservaLlamada(Presupuesto({"DIV": 100.0}, c), "DIV", Contabilidad(c), "AG-14")
        g.reservar(system, [], herr, 1000)
        reservas.append(g.peor_total)
    assert reservas[1] - reservas[0] == pytest.approx(Contabilidad(cfg).uc_de(Uso(entrada=5 * 4000)), abs=1e-3)
    sin_busqueda = ReservaLlamada(Presupuesto({"DIV": 100.0}, cfg), "DIV", Contabilidad(cfg), "AG-10")
    sin_busqueda.reservar(system, [], None, 1000)
    assert sin_busqueda.peor_total < reservas[0]
    negativo = _cfg(presupuesto_uc={"reserva": {"tokens_lectura_por_busqueda": -1}})
    with pytest.raises(ValueError, match="tokens_lectura_por_busqueda"):
        ReservaLlamada(Presupuesto({"DIV": 1.0}, negativo), "DIV", Contabilidad(negativo), "AG-14")


class SDKSoloAprendizaje:
    """Para AG-20 con el cliente real: el primer intento ocupa `max_tokens` y no es JSON; la reparación es la del simulado."""

    def __init__(self):
        self.messages, self.n = self, 0

    def create(self, **kw):
        self.n += 1
        msgs, salida = kw["messages"], int(kw["max_tokens"])
        entrada = int(tokens_de_peticion(kw["system"], msgs, kw.get("tools")) * FACTOR)
        texto = ("análisis " * int(salida * 3.6 / 9) if len([m for m in msgs if m["role"] == "user"]) == 1
                 else json.dumps(mock_respuestas.responder("AG-20", msgs[:1], 1), ensure_ascii=False))
        uso = types.SimpleNamespace(input_tokens=0, output_tokens=salida, cache_creation_input_tokens=entrada,
                                    cache_read_input_tokens=0, server_tool_use=None)
        return types.SimpleNamespace(stop_reason="end_turn", usage=uso, content=[types.SimpleNamespace(type="text", text=texto)])


DOCE = ["RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV"]


def test_r02_h03_y_h06_con_un_reparto_por_encima_del_ciclo_ag20_cabe_en_comun_escalada(tmp_path, monkeypatch):
    """H-03 (media): con N2 = 100 y los 12 tipos el reparto pasa del ciclo y las bolsas se escalan (COMÚN, de 24 a unas 4,7
    UC). AG-20 corre antes del reparto: antes lo hacía contra una COMÚN sin escalar (30 UC de límite) y COMÚN acababa en
    9,8 UC con un límite de 5,9. Ahora su bolsa es la base de COMÚN en el peor reparto posible, ya escalada.
    H-06 (baja): F5 da lo asignado escalado y la escala, y CT-05 lo asignado escalado."""
    cfg = _cfg(perfiles={"activos": DOCE}, presupuesto_uc={"N2": 100}, llm={"cache_resultados": False})
    b = _bloque(tmp_path, cfg, MockClient())
    sdk = SDKSoloAprendizaje()
    b.agentes.clientes["AG-20"] = AnthropicClient(sdk=sdk)
    monkeypatch.setattr(b.evaluador, "ciclo", lambda as_of, run_id: _res_eval_con_resueltos())
    ct05 = []
    crear = b.mensajeria.crear

    def espia(contrato, *a, **k):
        if contrato == "CT-05":
            ct05.append(a[2])
        return crear(contrato, *a, **k)
    monkeypatch.setattr(b.mensajeria, "crear", espia)
    r = b.ciclo("2024-03-29")
    assert sdk.n >= 1                                          # AG-20 salió con el cliente real
    pu = cfg["presupuesto_uc"]
    escala = pu["ciclo_semanal_max"] / (12 * 100 + pu["fraccion_minima_comun"] * pu["ciclo_semanal_max"])
    base_comun = pu["fraccion_minima_comun"] * pu["ciclo_semanal_max"] * escala
    ag20 = sum(x["uc"] for x in b.contabilidad.llamadas if x["agente"] == "AG-20")
    com = r["presupuesto"]["COMUN"]
    assert 0 < ag20 and com["consumido"] <= base_comun * (1 + pu["ampliacion_sin_autorizacion"]) + com["ampliado"] + 1e-6
    run = _comprobar_cotas(b, r, cfg)
    assert run["escala_presupuesto"] == pytest.approx(escala, abs=1e-6)
    assert com["asignado"] == pytest.approx(base_comun, abs=1e-5)
    assert sum(ct05[0]["presupuesto_por_clase"].values()) == pytest.approx(pu["ciclo_semanal_max"], abs=1e-3)
    assert ct05[0]["presupuesto_por_clase"]["COMUN"] == pytest.approx(com["asignado"])


def test_r02_h03_con_el_reparto_normal_la_bolsa_de_c5_no_cambia(tmp_path):
    """Sin escala (el reparto de siempre), AG-20 corre contra lo de antes: lo que COMÚN tiene como mínimo o su override."""
    cfg = _cfg()
    b = _bloque(tmp_path, cfg, MockClient())
    pu = cfg["presupuesto_uc"]
    minimo = pu["fraccion_minima_comun"] * pu["ciclo_semanal_max"]
    assert b._comun_minimo_c5(AS_OF, "PERIODICO", None, None, None, pu["ciclo_semanal_max"]) == pytest.approx(minimo)
    assert b._comun_minimo_c5(AS_OF, "PERIODICO", None, None, {"COMUN": 3.0}, pu["ciclo_semanal_max"]) == pytest.approx(3.0)
    # N3 forzado en un periódico con los 12 tipos: 12 × 50 + 24 pasa de 240 y la bolsa de C5 baja con la escala
    doce = _bloque(tmp_path / "doce", _cfg(perfiles={"activos": DOCE}), MockClient())
    assert doce._comun_minimo_c5(AS_OF, "PERIODICO", None, "N3", None, pu["ciclo_semanal_max"]) == pytest.approx(
        minimo * pu["ciclo_semanal_max"] / (12 * pu["N3"] + minimo))


def test_r02_h05_un_json_muy_anidado_deja_la_llamada_parcial_y_lo_pagado_en_la_bolsa(tmp_path):
    """H-05 (baja): una reparación con un JSON demasiado anidado lanzaba `RecursionError` desde `extraer_json`: lo pagado no
    llegaba a la bolsa y el ciclo caía. Ahora es un JSON no válido (falla cerrado)."""
    from bloque_a.agentes import extraer_json
    with pytest.raises(ValueError, match="anidado"):
        extraer_json("[" * 200000 + "]" * 200000)
    cfg = _cfg(llm={"cache_resultados": False})

    class SDK:
        def __init__(self):
            self.messages, self.textos = self, ["no es json", "[" * 200000 + "]" * 200000]

        def create(self, **kw):
            uso = types.SimpleNamespace(input_tokens=0, output_tokens=100, cache_read_input_tokens=0, server_tool_use=None,
                                        cache_creation_input_tokens=int(tokens_de_peticion(kw["system"], kw["messages"], None) * FACTOR))
            return types.SimpleNamespace(stop_reason="end_turn", usage=uso,
                                         content=[types.SimpleNamespace(type="text", text=self.textos.pop(0))])
    b = _bloque(tmp_path, cfg, AnthropicClient(sdk=SDK()))
    p = Presupuesto({"DIV": 18.0}, cfg)
    r = b._invocar("AG-12", "CT-11", {"piezas": []}, "CURACION", "Clasifica.", AS_OF, "RUN-QA", "DIV", "investigacion", p)
    p.liquidar_primas()
    assert r.estado == "PARCIAL" and any("JSON no válido" in e for e in r.errores)
    assert p.consumido["DIV"] == pytest.approx(sum(x["uc"] for x in b.contabilidad.llamadas), abs=1e-3)
    assert p.reservado["DIV"] == 0


def test_r02_h05_si_la_llamada_se_cae_lo_pagado_queda_en_la_bolsa(tmp_path, monkeypatch):
    """Cualquier otra excepción a mitad de llamada (después de pagar una petición) deja lo pagado cargado en la bolsa: el
    ciclo puede seguir en modo degradado y lo gastado sigue en el presupuesto."""
    import bloque_a.agentes as ag
    cfg = _cfg(llm={"cache_resultados": False})
    sdk = SDKPeorCaso(0, 0, 1, reparaciones=0)
    b = _bloque(tmp_path, cfg, AnthropicClient(sdk=sdk))

    def falla(texto):
        raise RuntimeError("fallo a mitad de llamada")
    monkeypatch.setattr(ag, "extraer_json", falla)
    p = Presupuesto({"DIV": 18.0}, cfg)
    with pytest.raises(RuntimeError):
        b._invocar("AG-12", "CT-11", {"piezas": []}, "CURACION", "Clasifica.", AS_OF, "RUN-QA", "DIV", "investigacion", p)
    assert len(sdk.peticiones) == 1 and p.reservado["DIV"] == 0
    assert p.consumido["DIV"] == pytest.approx(sum(x["uc"] for x in b.contabilidad.llamadas), abs=1e-3) and p.consumido["DIV"] > 0


def test_r02_h08_lo_real_se_carga_antes_de_soltar_lo_apartado(tmp_path, monkeypatch):
    """H-08 (baja, latente): `_invocar` soltaba lo apartado antes de cargar lo real; si dos hilos compartieran una bolsa, otro
    podría reservar en ese hueco. Ahora, al soltarlo, lo real ya está cargado."""
    cfg = _cfg(llm={"cache_resultados": False})
    b = _bloque(tmp_path, cfg, MockClient())
    p = Presupuesto({"DIV": 18.0}, cfg)
    vistos = []
    cerrar = ReservaLlamada.cerrar

    def espia(self):
        vistos.append((self.p.consumido[self.bolsa], self.apartado))
        cerrar(self)
    monkeypatch.setattr(ReservaLlamada, "cerrar", espia)
    r = b._invocar("AG-12", "CT-11", {"piezas": []}, "CURACION", "Clasifica.", AS_OF, "RUN-QA", "DIV", "investigacion", p)
    assert r.estado == "COMPLETO" and vistos and vistos[0][1] > 0
    assert vistos[0][0] > 0                                    # lo real ya estaba en la bolsa al soltar lo apartado


def test_r02_h10_cada_continuacion_se_paga_por_separado():
    """H-10 (baja): las continuaciones de `pause_turn` se pagan una a una frente a su reserva (el cliente real llama a `pagar`
    tras cada petición): ninguna cuesta más de lo suyo y no hay excesos, aunque el total de la llamada pase de una reserva."""
    cfg = _cfg()
    sdk = SDKPeorCaso(cont=3, max_usos=5, semilla=1)
    cli = AnthropicClient(sdk=sdk, max_continuaciones=3)
    herr = [{"type": "web_search_20260318", "name": "web_search", "max_uses": 5}]
    system, msgs = [{"type": "text", "text": "s" * 3600}], [{"role": "user", "content": "hola"}]
    p, g, _ = _guarda(100.0, cfg)
    mt = g.reservar(system, msgs, herr, 3000)
    with con_guarda(g):
        r = cli.generar(agente="AG-16", modelo="m", system=system, mensajes=msgs, max_tokens=mt, herramientas=herr)
    g.pagar_resto(r.uso)
    assert len(sdk.peticiones) == 4 and g.peticiones == 4
    assert Contabilidad(cfg).uc_de(r.uso) > g.peor_total / g.peticiones     # el total pasa de una reserva media
    assert not p.excesos and p.reservado["DIV"] == pytest.approx(g.apartado)
    g.cerrar()


def test_r02_h10_pagar_resto_suelta_las_reservas_que_no_salieron():
    p, g, _ = _guarda(100.0)
    g.reservar([{"text": "s" * 3600}], [], None, 1000)
    g.reservar([{"text": "s" * 3600}], [], None, 1000)        # una segunda que no llegó a salir
    g.pagar_resto(Uso(entrada=100, salida=10))
    assert p.reservado["DIV"] == pytest.approx(g.apartado)


def test_r02_h10_cargar_usa_el_prefijo_de_la_primera_peticion(tmp_path):
    """Con continuaciones, lo cacheado de la llamada suma el prefijo de cada petición: la prima retenida de un agente
    compartido es la del prefijo de la primera (`ReservaLlamada.prefijo`), no la suma dividida por los intentos."""
    cfg = _cfg(llm={"cache_resultados": False})

    class SDK:
        def __init__(self):
            self.messages, self.n = self, 0

        def create(self, **kw):
            self.n += 1
            uso = types.SimpleNamespace(input_tokens=500, output_tokens=200, cache_creation_input_tokens=20000 if self.n == 1 else 0,
                                        cache_read_input_tokens=0 if self.n == 1 else 20000,
                                        server_tool_use=types.SimpleNamespace(web_search_requests=1))
            texto = "x" if self.n == 1 else json.dumps(mock_respuestas.responder("AG-16", kw["messages"][:1], 1), ensure_ascii=False)
            return types.SimpleNamespace(stop_reason="pause_turn" if self.n == 1 else "end_turn", usage=uso,
                                         content=[types.SimpleNamespace(type="text", text=texto)])
    b = _bloque(tmp_path, cfg, AnthropicClient(sdk=SDK(), max_continuaciones=3))
    p = Presupuesto({"DIV": 18.0}, cfg)
    r = b._invocar("AG-16", "CT-08", C08["mensaje"], "BUSQUEDA", "Busca", AS_OF, "RUN-QA", "DIV", "investigacion", p,
                   permitir_web=True)
    assert r.estado == "COMPLETO" and r.intentos == 1
    assert p.retenido["DIV"] == pytest.approx(p._uc_prima(20000))


# ================================================================ T-151 · bajos de la QA r02 de T-146 (H-11, H-12, V01, V04, V05)
WEB = [{"type": "web_search_20260318", "name": "web_search", "max_uses": 5}]


def test_t151_h11_la_continuacion_de_una_generacion_que_busco_no_observa():
    """H-11 (baja): la continuación de `pause_turn` sin búsquedas nuevas reenvía lo leído antes (en la API, bloques con
    `encrypted_content` que la medida de 3,6 caracteres por token no ve enteros): su entrada no es error del tokenizador y
    no sube el factor de la bolsa. Antes subía (6,57 en el R9 del revisor)."""
    system, msgs = [{"text": "s" * 21600}], [{"role": "user", "content": "u" * 7200}]
    p, g, _ = _guarda(100.0)
    bruto = tokens_de_peticion(system, msgs, WEB)
    g.reservar(system, msgs, WEB, 3000)
    g.pagar(Uso(cache_escritura=bruto, entrada=5 * 3000, salida=3000, busquedas_web=5))       # la que busca
    g.reservar(system, msgs, WEB, 3000)
    g.pagar(Uso(cache_escritura=bruto + 5 * 3000 * 3, salida=3000, busquedas_web=0))          # la continuación: reenvía lo leído
    g.pagar_resto(Uso(cache_escritura=2 * bruto + 5 * 3000 * 4, salida=6000, busquedas_web=5))
    g.cerrar()
    assert not p.factor_observado


def test_t151_h11_con_el_cliente_real_la_ultima_continuacion_no_observa():
    """El R9 del revisor por el cliente real: tres vueltas que buscan y una última sin búsquedas que reenvía 15 lecturas de
    3 000 tokens que la medida no ve."""
    class SDK:
        def __init__(self):
            self.messages, self.n = self, 0

        def create(self, **kw):
            self.n += 1
            medida = tokens_de_peticion(kw["system"], kw["messages"], kw.get("tools"))
            vuelta = 1 + sum(1 for m in kw["messages"] if m["role"] == "assistant")
            nuevas = 0 if vuelta == 4 else 5
            uso = types.SimpleNamespace(input_tokens=0, output_tokens=int(kw["max_tokens"]), cache_read_input_tokens=0,
                                        cache_creation_input_tokens=int(medida) + 5 * 3000 * (vuelta - 1) + nuevas * 3000,
                                        server_tool_use=types.SimpleNamespace(web_search_requests=nuevas))
            return types.SimpleNamespace(stop_reason="end_turn" if vuelta == 4 else "pause_turn", usage=uso,
                                         content=[types.SimpleNamespace(type="text", text="ok")])
    system, msgs = [{"type": "text", "text": "s" * 21600}], [{"role": "user", "content": "u" * 7200}]
    p, g, _ = _guarda(100.0)
    cli = AnthropicClient(sdk=SDK(), max_continuaciones=3)
    mt = g.reservar(system, msgs, WEB, 3000)
    with con_guarda(g):
        r = cli.generar(agente="AG-14", modelo="m", system=system, mensajes=msgs, max_tokens=mt, herramientas=WEB)
    g.pagar_resto(r.uso)
    g.cerrar()
    assert cli.sdk.n == 4 and not p.factor_observado


def test_t151_h11_la_reparacion_tras_buscar_si_observa():
    """Límite de la regla: la reparación empieza otra generación (solo reenvía el texto de la respuesta, no los bloques de
    búsqueda), y una petición sin búsquedas de una llamada posterior también: las dos aprenden el tokenizador peor."""
    system, msgs = [{"text": "s" * 21600}], [{"role": "user", "content": "u" * 7200}]
    for siguiente in ("reparación", "otra llamada"):
        p, g, cfg = _guarda(100.0)
        g.reservar(system, msgs, WEB, 3000)
        g.pagar_resto(Uso(cache_escritura=tokens_de_peticion(system, msgs, WEB), entrada=5 * 3000, salida=3000, busquedas_web=5))
        if siguiente == "otra llamada":
            g.cerrar()
            g = ReservaLlamada(p, "DIV", Contabilidad(cfg), "AG-05")
        g.reservar(system, msgs, None, 3000)
        g.pagar_resto(Uso(cache_escritura=int(tokens_de_peticion(system, msgs, None) * 1.8), salida=3000))
        g.cerrar()
        assert p.factor_observado.get("DIV", 0) >= 1.79, siguiente


def test_t151_h12_sin_tipos_lo_de_ag20_esta_en_f5(tmp_path, monkeypatch):
    """H-12 (baja): con un alcance sin ningún tipo que analizar (un tipo no activo), AG-20 corre contra su bolsa de C5 y el
    ciclo sale por `_run_sin_analisis`, que no escribía el presupuesto en el RUN de F5: lo gastado no estaba en ninguna
    bolsa (CA-3 de T-146). Ahora sí, en la COMÚN, con los cierres."""
    cfg = _cfg(llm={"cache_resultados": False})
    b = _bloque(tmp_path / "a", cfg, MockClient())
    monkeypatch.setattr(b.evaluador, "ciclo", lambda as_of, run_id: _res_eval_con_resueltos())
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})              # RV no está activo: nada que analizar
    run = b.almacen.estado("F5", clave="id")[r["run_id"]]
    gastado = sum(x["uc"] for x in b.contabilidad.llamadas if x["run_id"] == r["run_id"])
    assert r["estado"] == "PARCIAL" and r["entrega"] == "SIN_RESULTADO"
    assert {x["agente"] for x in b.contabilidad.llamadas} == {"AG-20"} and gastado > 0
    assert set(run["presupuesto"]) == {"COMUN"} and run["presupuesto"]["COMUN"]["consumido"] == pytest.approx(gastado, abs=1e-3)
    assert r["presupuesto"] == run["presupuesto"] and run["cierres_parciales"] == []
    limite, _ = _limites(cfg, run["presupuesto"]["COMUN"])
    assert run["presupuesto"]["COMUN"]["consumido"] <= limite
    # sin sitio para AG-20: no sale y el cierre queda en el RUN sin análisis
    b2 = _bloque(tmp_path / "b", cfg, MockClient())
    monkeypatch.setattr(b2.evaluador, "ciclo", lambda as_of, run_id: _res_eval_con_resueltos())
    r2 = b2.ciclo(AS_OF, alcance={"clases": ["RV"]}, presupuesto_override={"COMUN": 0.01})
    run2 = b2.almacen.estado("F5", clave="id")[r2["run_id"]]
    assert not b2.contabilidad.llamadas and run2["presupuesto"]["COMUN"]["consumido"] == 0
    assert any(c["clase"] == "COMUN" and "AG-20" in c["motivo"] for c in run2["cierres_parciales"])


def test_t151_v01_el_exceso_no_depende_de_si_el_prefijo_se_leyo():
    """Mutante V01 de la QA r02: el exceso se compara con lo real contado como escrito (como lo apartado, H-02). Si se
    comparara con lo real con la lectura barata, `excesos_reserva` dependería de qué hilo escribió antes el prefijo
    compartido (el orden de los hilos)."""
    system = [{"text": "s" * 36000}]
    excesos = []
    for campo in ("cache_escritura", "cache_lectura"):
        p, g, _ = _guarda(100.0)
        g.reservar(system, [], None, 100)
        g.pagar_resto(Uso(salida=10, **{campo: 2 * tokens_de_peticion(system, [], None)}))
        g.cerrar()
        excesos.append(p.excesos)
    assert excesos[0] and excesos[0] == excesos[1]


def test_t151_v04_un_keyboardinterrupt_deja_lo_pagado_en_la_bolsa(tmp_path):
    """Mutante V04 de la QA r02: `_invocar` captura `BaseException`, no solo `Exception`: un `KeyboardInterrupt` (que el
    cliente no captura) en la reparación, tras una petición pagada, deja lo pagado cargado en la bolsa y nada reservado, y
    sube."""
    cfg = _cfg(llm={"cache_resultados": False})

    class SDK:
        def __init__(self):
            self.messages, self.n = self, 0

        def create(self, **kw):
            self.n += 1
            if self.n == 2:
                raise KeyboardInterrupt
            uso = types.SimpleNamespace(input_tokens=0, output_tokens=100, cache_read_input_tokens=0, server_tool_use=None,
                                        cache_creation_input_tokens=int(tokens_de_peticion(kw["system"], kw["messages"], None) * FACTOR))
            return types.SimpleNamespace(stop_reason="end_turn", usage=uso, content=[types.SimpleNamespace(type="text", text="no es json")])
    sdk = SDK()
    b = _bloque(tmp_path, cfg, AnthropicClient(sdk=sdk))
    p = Presupuesto({"DIV": 18.0}, cfg)
    with pytest.raises(KeyboardInterrupt):
        b._invocar("AG-12", "CT-11", {"piezas": []}, "CURACION", "Clasifica.", AS_OF, "RUN-QA", "DIV", "investigacion", p)
    p.liquidar_primas()
    gastado = sum(x["uc"] for x in b.contabilidad.llamadas)
    assert sdk.n == 2 and gastado > 0 and p.reservado["DIV"] == 0
    assert p.consumido["DIV"] == pytest.approx(gastado, abs=1e-3)


def test_t151_v05_r8_sin_comprobar_por_lo_anidado_bloquea(tmp_path, monkeypatch):
    """Mutante V05 de la QA r02: si la comprobación de credenciales (R8) no se puede hacer (`RecursionError`, por lo
    anidado), la respuesta se bloquea (falla cerrado) y la llamada no queda COMPLETA."""
    import bloque_a.agentes as ag
    cfg = _cfg(llm={"cache_resultados": False})
    b = _bloque(tmp_path, cfg, MockClient())

    def no_se_puede(datos):
        raise RecursionError("demasiado anidado")
    monkeypatch.setattr(ag, "contiene_credenciales", no_se_puede)
    r = b._invocar("AG-12", "CT-11", {"piezas": []}, "CURACION", "Clasifica.", AS_OF, "RUN-QA", "DIV", "investigacion",
                   Presupuesto({"DIV": 18.0}, cfg))
    assert r.estado == "PARCIAL" and r.datos is None and "respuesta bloqueada por R8" in r.errores
