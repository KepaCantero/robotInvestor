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
