"""T-101 · Diseño V6 del Bloque A (aspirante): núcleo común y kits, GC1 por código, Prospectiva por ciclo, Contradictor de la
selección provisional y sus sustitutas, Sintetizador, Lector de evidencia, Respondedor, registro de cobertura y
contrafactual. Criterios de `.docs/tickets/T-101/README.md`. Con `diseno: v5`, el resto de la batería no cambia (CA-1)."""
import copy
import json
import math
from pathlib import Path

import pandas as pd
import pytest
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config, parametro
from bloque_a.contratos import canal_permitido
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient, _tokens_aprox
from bloque_a.orquestacion import Bloque
from bloque_a.prompts import (
    ANALISTAS_TIPO,
    CatalogoPrompts,
    identidad,
    kit,
    secciones,
)
from conftest import AS_OF, DATOS, config_pruebas

from bloque_a import diseno_v6 as v6
from bloque_a import mock_respuestas as mr

QUITADOS_EN_V6 = {"AG-01", "AG-02", "AG-12", "AG-14", "AG-16", "AG-17", "AG-18", "AG-20"}


def _cfg(**extra):
    return config_pruebas(diseno="v6", **extra)


def _bloque(tmp, cfg, cliente=None, **kw):
    return Bloque(cfg, ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), cliente or MockClient(),
                  Path(tmp) / "estado", Path(tmp) / "ent", **kw)


def _espiar(b, cliente):
    """Orden de las llamadas al modelo y de la validación G3, y los cuerpos de los mensajes CT-06 y CT-13."""
    orden, cuerpos = [], {"CT-06": [], "CT-13": []}
    gen = cliente.generar

    def _gen(**kw):
        orden.append(kw["agente"])
        return gen(**kw)
    cliente.generar = _gen
    val = b._validar_g3

    def _val(*a, **k):
        orden.append("G3")
        return val(*a, **k)
    b._validar_g3 = _val
    crear = b.mensajeria.crear

    def _crear(contrato, emisor, receptor, cuerpo, **k):
        if contrato in cuerpos:
            cuerpos[contrato].append(json.loads(json.dumps(cuerpo, default=str)))
        return crear(contrato, emisor, receptor, cuerpo, **k)
    b.mensajeria.crear = _crear
    return orden, cuerpos


def _cobertura(b):
    return [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "COBERTURA"]


# ================================================================================================ configuración y prompts
def test_diseno_desconocido_falla_cerrado(tmp_path):
    with pytest.raises(ValueError, match="diseno"):
        _bloque(tmp_path, config_pruebas(diseno="v7"))


def test_por_defecto_el_diseno_es_v5():
    assert cargar_config()["diseno"] == "v5"


def test_nucleo_identico_para_los_doce_y_sin_marcadores():
    c = CatalogoPrompts(_cfg())
    nucleos = {json.dumps(c.system(ag, cache=False)[:2]) for ag in ANALISTAS_TIPO}
    assert len(nucleos) == 1 and "{{" not in c.nucleo()


@pytest.mark.parametrize("ag", sorted(ANALISTAS_TIPO))
def test_kit_completo_no_pierde_nada_y_no_inventa(ag):
    """CA-2: con la §10, núcleo (con la identidad sustituida) más kit tienen exactamente las secciones del prompt V5.0, y cada
    sección del kit es texto literal del prompt V5.0."""
    c = CatalogoPrompts(_cfg())
    c.nucleo()
    esp, marco = c.texto(ag), c._cache["_marco"]
    k = kit(esp, marco, "completa")
    _, sk = secciones(k)
    _, se = secciones(esp)
    from bloque_a.prompts import _sin_comentario, _sustituir
    _, sm = secciones(_sustituir(_sin_comentario(marco), identidad(esp)))
    for n, txt in se.items():
        assert sm.get(n, "").strip() == txt.strip() or sk.get(n, "").strip() == txt.strip(), (ag, n)
    for n, txt in sk.items():
        assert txt.strip() == se[n].strip(), (ag, n)
    assert set(se) == set(sm) | set(sk)
    corto = kit(esp, marco, "ninguna")
    assert "10" not in secciones(corto)[1] and "6" in secciones(corto)[1]


def test_kit_con_base_desconocida_falla():
    c = CatalogoPrompts(_cfg())
    c.nucleo()
    with pytest.raises(ValueError):
        kit(c.texto("AG-05"), c._cache["_marco"], "resumida")


def test_dos_puntos_de_cache_para_los_analistas():
    c = CatalogoPrompts(_cfg())
    s = c.system("AG-05")
    assert len(s) == 3 and "cache_control" in s[1] and "cache_control" in s[2] and "cache_control" not in s[0]
    assert len(c.system("AG-10")) == 2
    assert len(CatalogoPrompts(config_pruebas()).system("AG-05")) == 2   # V5: el prompt íntegro


def test_tope_de_tokens_de_los_prompts_por_papel():
    """Idea 7: el system de cada papel de la V6 no pasa de su tope en la configuración."""
    cfg = _cfg()
    c = CatalogoPrompts(cfg)
    tope = parametro(cfg, "v6.tope_tokens_system")
    for ag in ANALISTAS_TIPO:
        assert _tokens_aprox("".join(b["text"] for b in c.system(ag))) <= tope["analista"], ag
    for ag in ("AG-10", "AG-11", "AG-26", "AG-27", "AG-28"):
        assert _tokens_aprox("".join(b["text"] for b in c.system(ag))) <= tope[ag], ag


def test_el_simulador_lee_el_nucleo_de_la_cache_entre_analistas():
    """Idea 2: la caché es por prefijo, no por agente: el segundo analista lee el núcleo que escribió el primero."""
    c, cli = CatalogoPrompts(_cfg()), MockClient()
    msg = [{"role": "user", "content": "# Encargo\n```json\n" + json.dumps({"contexto": {"fecha_as_of": AS_OF}, "mensaje": {
        "clase": "DIV", "fase": "REVISION_VIGENTES", "opciones_vigentes": [], "universo": []}}) + "\n```\n"}]
    u1 = cli.generar(agente="AG-05", modelo="m", system=c.system("AG-05"), mensajes=msg, max_tokens=10).uso
    u2 = cli.generar(agente="AG-03", modelo="m", system=c.system("AG-03"), mensajes=copy.deepcopy(msg), max_tokens=10).uso
    nucleo = _tokens_aprox(c.nucleo() + c.system("AG-05")[1]["text"])
    assert u1.cache_lectura == 0 and u2.cache_lectura == nucleo and u2.cache_escritura > 0


def test_canales_de_la_v6_solo_con_la_v6():
    assert not canal_permitido("CT-08", "AG-05", "AG-28") and canal_permitido("CT-08", "AG-05", "AG-28", v6=True)
    assert not canal_permitido("CT-15", "AG-02", "AG-26") and canal_permitido("CT-15", "AG-02", "AG-26", v6=True)


def test_la_bolsa_del_ciclo_sale_de_los_tipos_sin_cambiar_el_total(tmp_path):
    b = _bloque(tmp_path, _cfg())
    asign = {"RV": 18.0, "DIV": 5.0, "COMUN": 24.0}
    out = v6.repartir_presupuesto(b, asign, ["RV", "DIV"])
    assert math.isclose(sum(out.values()), sum(asign.values())) and out[v6.BOLSA_GLOBAL] > 0 and out["RV"] < 18.0


def test_auditor_por_muestreo_sembrado(tmp_path):
    ids = [f"RUN-2026-{i:04d}" for i in range(400)]
    b = _bloque(tmp_path, _cfg())
    frac = sum(v6.auditar_este_run(b, x) for x in ids) / len(ids)
    assert 0.15 < frac < 0.35 and v6.auditar_este_run(b, ids[7]) == v6.auditar_este_run(b, ids[7])
    assert not any(v6.auditar_este_run(_bloque(tmp_path / "a", _cfg(v6={"auditoria_fraccion": 0.0})), x) for x in ids[:50])
    assert all(v6.auditar_este_run(_bloque(tmp_path / "b", _cfg(v6={"auditoria_fraccion": 1.0})), x) for x in ids[:50])


# ================================================================================================ ciclo V6 con los doce perfiles
@pytest.fixture(scope="module")
def dos_disenos(tmp_path_factory):
    """El mismo ciclo C1 con los doce perfiles en la V5 y en la V6."""
    out = {}
    for d in ("v5", "v6"):
        tmp = tmp_path_factory.mktemp(d)
        cli = MockClient()
        b = _bloque(tmp, config_pruebas(diseno=d), cli)
        orden, cuerpos = _espiar(b, cli)
        r = b.ciclo(AS_OF)
        out[d] = {"b": b, "r": r, "cli": cli, "orden": orden, "cuerpos": cuerpos}
    return out


def test_ciclo_v6_entrega_y_valida(dos_disenos):
    r = dos_disenos["v6"]["r"]
    assert r["g3"]["dictamen"] in ("APTO", "APTO_CON_ADVERTENCIAS") and r["g3_entregables"]["dictamen"] != "BLOQUEADO"
    assert r.get("entrega") != "BLOQUEADA" and sum(len(c["opciones"]) for c in r["paquete"]["clases"].values()) > 0


def test_v6_no_llama_a_los_papeles_que_pasan_a_codigo(dos_disenos):
    llamados = {x["agente"] for x in dos_disenos["v6"]["cli"].llamadas}
    assert not llamados & QUITADOS_EN_V6
    assert {"AG-10", "AG-11", "AG-26"} <= llamados


def test_prospectiva_una_vez_por_lote_con_cobertura(dos_disenos):
    """CA-3: una llamada por lote de `max_encargos_por_lote`, no una por tipo, y ninguna finalista sin resultado."""
    d = dos_disenos["v6"]
    cob = _cobertura(d["b"])[0]["prospectiva"]
    n10 = sum(1 for x in d["cli"].llamadas if x["agente"] == "AG-10")
    assert n10 == cob["lotes"] == math.ceil(cob["encargos"] / parametro(d["b"].cfg, "v6.prospectiva.max_encargos_por_lote"))
    assert cob["omitidos"] == [] and n10 < sum(1 for x in dos_disenos["v5"]["cli"].llamadas if x["agente"] == "AG-10")


def test_el_contradictor_solo_ve_la_seleccion_y_todo_lo_entregado_esta_criticado(dos_disenos):
    """CA-4: cada opción nueva entregada de un tipo N2/N3 pasó por el Contradictor; lo criticado estuvo en un top-3."""
    d = dos_disenos["v6"]
    b, r = d["b"], d["r"]
    cob = _cobertura(b)[0]
    criticadas = {x for ronda in cob["critica"]["rondas"] for x in ronda["criticadas"]}
    pedidas = {p["ref"] for m in d["cuerpos"]["CT-13"] for p in m.get("peticiones", [])}
    assert pedidas == criticadas
    for c, cl in r["paquete"]["clases"].items():
        if r["nivel_por_clase"][c] not in ("N2", "N3"):
            continue
        filas = {f["opp_id"]: f for f in cob["clases"][c]["filas"] if f.get("opp_id")}
        for o in cl["opciones"]:
            if o["opp_id"] in filas:
                assert filas[o["opp_id"]]["criticada"], (c, o["opp_id"])
    finalistas = sum(1 for c in cob["clases"].values() for f in c["filas"] if f["fase"] != "GC1" and f["fase"] not in ("GC2", "GC3"))
    assert len(criticadas) <= finalistas


def test_el_sintetizador_escribe_una_vez_despues_de_g3(dos_disenos):
    orden = dos_disenos["v6"]["orden"]
    assert orden.count("AG-26") == 1 and orden.index("AG-26") > orden.index("G3")


def test_gc1_por_codigo_limita_lo_que_ve_el_analista(dos_disenos):
    """CA-6: el Analista recibe como mucho `max_candidatas` con señal, más la exploración, lo que no tiene señal y lo vigente."""
    d = dos_disenos["v6"]
    b = d["b"]
    maxc = parametro(b.cfg, "seleccion.max_candidatas")
    cob = _cobertura(b)[0]["clases"]
    for m in d["cuerpos"]["CT-06"]:
        if m.get("fase") != "CRIBADO_E_INVESTIGACION":
            continue
        g = cob[m["clase"]]["gc1"]
        permitidos = set(g["pasan"]) | set(g["exploracion"]) | set(g["sin_senal_medible"]) | set(g["vigentes"])
        vistos = {u["simbolo"] for u in m["universo"]}
        assert vistos <= permitidos and len(g["pasan"]) <= maxc and all(u.get("gc1") for u in m["universo"])
        assert len(g["exploracion"]) <= parametro(b.cfg, "v6.gc1.exploracion_celdas")


def test_registro_de_cobertura_de_cada_candidata(dos_disenos):
    """CA-7 (primera parte): cada finalista tiene su fase y su motivo; la muestra de descartes lleva su precio."""
    b = dos_disenos["v6"]["b"]
    cob = _cobertura(b)
    assert len(cob) == 1
    n = parametro(b.cfg, "v6.cobertura.muestra_descartes")
    for d in cob[0]["clases"].values():
        assert all(f["fase"] and f["motivo"] for f in d["filas"])
        assert len(d["muestra_descartes"]) <= n and all("precio" in x for x in d["muestra_descartes"])


def test_v6_hace_menos_llamadas_y_lee_menos_tokens(dos_disenos):
    """CA-8, reformulado tras H-02 de la QA r01 (con el simulador; no dice nada de la calidad): menos llamadas y menos tokens de
    entrada que la V5, contando la caché y sin contarla."""
    c5, c6 = dos_disenos["v5"]["r"]["consumo"], dos_disenos["v6"]["r"]["consumo"]
    tot = lambda c: c["entrada"] + c["cache_escritura"] + c["cache_lectura"]
    assert c6["llamadas"] < c5["llamadas"] and tot(c6) < tot(c5) and c6["entrada"] < c5["entrada"]


def test_v6_declara_sus_limitaciones(dos_disenos):
    lim = " ".join(dos_disenos["v6"]["r"]["paquete"]["limitaciones"])
    assert "Contradictor del mismo proveedor" in lim and "Curación determinista" in lim


def test_consumo_registra_intentos_y_latencia(dos_disenos):
    c = dos_disenos["v6"]["r"]["consumo"]
    assert "reintentos" in c and "latencia_s" in c
    assert all("intento" in x and "latencia_s" in x for x in dos_disenos["v6"]["b"].contabilidad.llamadas)


# ================================================================================================ casos límite y fallo cerrado
def _cfg_div(**extra):
    base = {"perfiles": {"activos": ["DIV"]}, "seleccion": {"umbral_senal_gc1": 0.55}}
    from bloque_a.configuracion import fusionar
    return _cfg(**fusionar(base, extra))


def test_si_cae_la_mejor_entra_otra_y_tambien_se_critica(tmp_path, monkeypatch):
    """CA-4 (sustitución, A-01): la mejor candidata recibe una objeción fuerte que no se resuelve; la que entra pasa la crítica
    en una ronda de sustitución y nada sale sin crítica."""
    orig_c, orig_a = mr._contrarias, mr._analista
    victima = {}

    def contrarias(msg, ctx, rng):
        if "contrarreplicas" in msg:
            return {"resultados": [{"objecion_id": x["objecion_id"], "resuelta": False, "motivo": "no basta"} for x in msg["contrarreplicas"]]}
        out = orig_c(msg, ctx, rng)
        victima.setdefault("ref", msg["peticiones"][0]["ref"])
        for x in out["resultados"]:
            x["objeciones"] = [o for o in x["objeciones"] if o["fuerza"] != "fuerte"]
            if x["ref"] == victima["ref"]:
                x["objeciones"].append({"id": "X", "tipo": "evidencia_insuficiente", "fuerza": "fuerte", "argumento": "No se sostiene.",
                                        "evidencia": "-", "que_la_resolveria": "otra raíz"})
        return out
    monkeypatch.setattr(mr, "_contrarias", contrarias)

    def analista(msg, ctx, rng, iny):   # el acusado responde a todo, pero la contrarréplica no da por resuelta la fuerte
        return orig_a(msg, ctx, rng, iny)
    monkeypatch.setattr(mr, "_analista", analista)
    b = _bloque(tmp_path, _cfg_div())
    r = b.ciclo(AS_OF)
    cob = _cobertura(b)[0]
    rondas = cob["critica"]["rondas"]
    assert rondas[0]["tipo"] == "PROVISIONAL" and len(rondas) >= 2 and rondas[1]["tipo"] == "SUSTITUCION" and rondas[1]["criticadas"]
    proxy = victima["ref"].split(":")[1]
    entregadas = {o["indicador_seguimiento"]["simbolo"] for o in r["paquete"]["clases"]["DIV"]["opciones"]}
    assert proxy not in entregadas
    filas = {f["simbolo"]: f for f in cob["clases"]["DIV"]["filas"]}
    assert all(filas[s]["criticada"] for s in entregadas if s in filas)


def test_una_omision_de_prospectiva_se_reintenta_y_se_declara(tmp_path, monkeypatch):
    """CA-3 (fallo cerrado): un encargo que Prospectiva no devuelve se pide otra vez; si sigue faltando, la finalista queda sin
    pronóstico, no se entrega y se declara (no cuenta como pronóstico negativo)."""
    orig = mr._prospectiva
    quitar = {}

    def prospectiva(msg, ctx, rng):
        out = orig(msg, ctx, rng)
        quitar.setdefault("ref", msg["encargos"][0]["ref"])
        out["resultados"] = [x for x in out["resultados"] if x["ref"] != quitar["ref"]]
        return out
    monkeypatch.setattr(mr, "_prospectiva", prospectiva)
    cli = MockClient()
    b = _bloque(tmp_path, _cfg_div(), cli)
    r = b.ciclo(AS_OF)
    cob = _cobertura(b)[0]
    assert cob["prospectiva"]["omitidos"] == [quitar["ref"]]
    assert sum(1 for x in cli.llamadas if x["agente"] == "AG-10") == cob["prospectiva"]["lotes"] == 2
    proxy = quitar["ref"].split(":")[1]
    assert proxy not in {o["indicador_seguimiento"]["simbolo"] for o in r["paquete"]["clases"]["DIV"]["opciones"]}
    assert any("Prospectiva sin pronóstico" in x and quitar["ref"] in x for x in r["paquete"]["limitaciones"])
    assert next(f for f in cob["clases"]["DIV"]["filas"] if f["simbolo"] == proxy)["fase"] == "PROSPECTIVA"


def test_el_sintetizador_no_puede_cambiar_la_seleccion(tmp_path, monkeypatch):
    """CA-5: aunque el Sintetizador devuelva otra selección o cifras, solo se toman sus textos y HT-09 valida después."""
    orig = mr._sintetizador
    capt = {}

    def sintetizador(msg, ctx, rng):
        out = orig(msg, ctx, rng)
        out.update({"top3": ["OPP-9999-9999"], "clases": {}, "puntuaciones": {"RK": 100}, "apuestas_independientes": 99,
                    "regimen_macro": "Régimen escrito por el Sintetizador de la prueba."})
        return out
    monkeypatch.setattr(mr, "_sintetizador", sintetizador)
    b = _bloque(tmp_path, _cfg_div())
    val = b._validar_g3

    def _val(paquete, *a, **k):
        p, g = val(paquete, *a, **k)
        capt["ids"] = {c: [o["opp_id"] for o in d["opciones"]] for c, d in p["clases"].items()}
        capt["apuestas"] = p["apuestas_independientes"]
        return p, g
    b._validar_g3 = _val
    r = b.ciclo(AS_OF)
    assert {c: [o["opp_id"] for o in d["opciones"]] for c, d in r["paquete"]["clases"].items()} == capt["ids"]
    assert r["paquete"]["apuestas_independientes"] == capt["apuestas"] and "top3" not in r["paquete"]
    assert r["paquete"]["regimen_macro"] == "Régimen escrito por el Sintetizador de la prueba."
    assert r["g3_entregables"]["dictamen"] != "BLOQUEADO"


def test_las_consultas_n0_las_responde_el_respondedor(tmp_path):
    cli = MockClient()
    b = _bloque(tmp_path, _cfg_div(), cli)
    b.ciclo(AS_OF)
    n = len(cli.llamadas)
    b.consulta("¿Por qué no aparece la renta fija esta semana?", as_of=AS_OF)
    nuevos = {x["agente"] for x in cli.llamadas[n:]}
    assert "AG-27" in nuevos and "AG-01" not in nuevos


def test_contradictor_de_otro_proveedor(tmp_path):
    cli, otro = MockClient(), MockClient(semilla=7)
    b = _bloque(tmp_path, _cfg_div(v6={"contradictor": {"proveedor": "otro"}}), cli, cliente_contradictor=otro)
    r = b.ciclo(AS_OF)
    assert any(x["agente"] == "AG-11" for x in otro.llamadas) and not any(x["agente"] == "AG-11" for x in cli.llamadas)
    assert not any("Contradictor del mismo proveedor" in x for x in r["paquete"]["limitaciones"])
    b2 = _bloque(tmp_path / "b", _cfg_div(v6={"contradictor": {"proveedor": "otro"}}))
    r2 = b2.ciclo(AS_OF)
    assert any("segundo proveedor no está configurado" in x for x in r2["paquete"]["limitaciones"])


def test_el_contrafactual_resuelve_la_muestra_al_vencer_su_horizonte(tmp_path):
    """CA-7 (segunda parte, idea 4): la muestra de descartes de un run se compara con las elegidas cuando vence su horizonte."""
    b = _bloque(tmp_path, _cfg_div())
    b.ciclo(AS_OF)
    cob = _cobertura(b)[0]
    assert not [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "CONTRAFACTUAL"]
    vence = v6._fecha_vencimiento(b, cob["fecha"], cob["horizonte_contrafactual"])
    b.ciclo(str((vence + pd.Timedelta(days=3)).date()))
    ctf = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "CONTRAFACTUAL"]
    assert len(ctf) == 1 and ctf[0]["cobertura_id"] == cob["id"] and "DIV" in ctf[0]["clases"]
    d = ctf[0]["clases"]["DIV"]
    assert d["descartes"] + d["elegidas"] > 0 and d["descartes_que_superan"] <= d["descartes"]
    b.ciclo(str((vence + pd.Timedelta(days=10)).date()))   # una sola vez
    assert len([e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "CONTRAFACTUAL" and e["cobertura_id"] == cob["id"]]) == 1


def test_gc1_no_descarta_lo_que_no_tiene_senal(tmp_path):
    b = _bloque(tmp_path, _cfg_div())
    uni = [{"simbolo": "A", "senales": {"senal_compuesta": 0.9}}, {"simbolo": "B", "senales": {"senal_compuesta": None}},
           {"simbolo": "C", "senales": {"senal_compuesta": 0.1}}, {"simbolo": "D", "senales": {}}]
    filtrado, reg = v6.gc1(b, "DIV", uni, [], AS_OF)
    marcas = {u["simbolo"]: u["gc1"] for u in filtrado}
    assert marcas["A"] == "PASA" and marcas["B"] == marcas["D"] == "SIN_SENAL_MEDIBLE" and marcas.get("C") == "EXPLORACION"
    assert reg["descartes"] == []


# ================================================================================================ QA r01 de T-101 (ronda r02)
def _filas(b, clase):
    return _cobertura(b)[-1]["clases"][clase]["filas"]


def _entregadas(r, clase):
    return {o["indicador_seguimiento"]["simbolo"] for o in r["paquete"]["clases"][clase]["opciones"]}


def _hunde(monkeypatch):
    """El Contradictor simulado: objeción fuerte sin resolver para la primera ref que ve; sin fuertes para el resto."""
    orig = mr._contrarias
    estado = {"victimas": set()}

    def contrarias(msg, ctx, rng):
        if "contrarreplicas" in msg:
            return {"resultados": [{"objecion_id": x["objecion_id"], "resuelta": False, "motivo": "no basta"} for x in msg["contrarreplicas"]]}
        out = orig(msg, ctx, rng)
        if not estado["victimas"]:
            estado["victimas"].add(msg["peticiones"][0]["ref"])
        for x in out["resultados"]:
            x["objeciones"] = [o for o in x["objeciones"] if o["fuerza"] != "fuerte"]
            if x["ref"] in estado["victimas"]:
                x["objeciones"].append({"id": "X", "tipo": "evidencia_insuficiente", "fuerza": "fuerte", "argumento": "No se sostiene.",
                                        "evidencia": "-", "que_la_resolveria": "otra raíz"})
        return out
    monkeypatch.setattr(mr, "_contrarias", contrarias)
    return estado


def test_sin_rondas_de_sustitucion_la_que_entra_sin_critica_no_sale(tmp_path, monkeypatch):
    """H-11 (M08, M09, M18 y M27): con `max_rondas_sustitucion: 0`, la que sustituye a la que cae no se puede criticar: no se
    entrega, se declara y el run queda PARCIAL; todo lo entregado está criticado."""
    estado = _hunde(monkeypatch)
    b = _bloque(tmp_path, _cfg_div(v6={"contradictor": {"max_rondas_sustitucion": 0}}))
    r = b.ciclo(AS_OF)
    cob = _cobertura(b)[-1]
    filas = _filas(b, "DIV")
    criticadas = {f["simbolo"] for f in filas if f.get("criticada")}
    assert estado["victimas"] and _entregadas(r, "DIV") <= criticadas
    sin = cob["critica"]["sin_critica"]
    assert sin and all(x["proxy"] not in _entregadas(r, "DIV") for x in sin)
    assert all(next(f for f in filas if f["simbolo"] == x["proxy"] and f["fase"] != "ANALISTA")["fase"] == "CRITICA" for x in sin)
    assert any(x.startswith("Sin crítica del Contradictor") for x in r["paquete"]["limitaciones"]) and r["estado"] == "PARCIAL"


def test_lo_que_el_contradictor_no_devuelve_se_reintenta_se_declara_y_no_sale(tmp_path, monkeypatch):
    """H-03, H-04 y M06: una ref que el Contradictor no devuelve se pide otra vez y, si sigue sin volver, no se entrega, se
    declara con su motivo y el run queda PARCIAL."""
    cli = MockClient()
    b = _bloque(tmp_path, _cfg_div(), cli)
    ver = {"llamadas": []}
    orig = mr._contrarias

    def contrarias(msg, ctx, rng):
        out = orig(msg, ctx, rng)
        if "contrarreplicas" in msg:
            return out
        ver.setdefault("ref", msg["peticiones"][0]["ref"])
        ver["llamadas"].append([p["ref"] for p in msg["peticiones"]])
        out["resultados"] = [x for x in out["resultados"] if x["ref"] != ver["ref"]]
        return out
    monkeypatch.setattr(mr, "_contrarias", contrarias)
    r = b.ciclo(AS_OF)
    cob = _cobertura(b)[-1]
    proxy = ver["ref"].split(":")[1]
    assert ver["ref"] in cob["critica"]["sin_respuesta"] and [ver["ref"]] in ver["llamadas"]   # el reintento, solo con lo que faltó
    assert proxy not in _entregadas(r, "DIV") and r["estado"] == "PARCIAL"
    assert any("no devolvió la crítica" in x and ver["ref"] in x for x in r["paquete"]["limitaciones"])
    fila = next(f for f in _filas(b, "DIV") if f["simbolo"] == proxy and f["fase"] != "ANALISTA")
    assert fila["fase"] == "CRITICA" and "no la devolvió" in fila["motivo"]


def test_el_reintento_no_sale_de_la_cache(tmp_path, monkeypatch):
    """H-04: si Prospectiva no devuelve nada la primera vez, el reintento es otro encargo y llega al modelo."""
    orig = mr._prospectiva

    def prospectiva(msg, ctx, rng):
        out = orig(msg, ctx, rng)
        if "reintento_de_cobertura" not in msg:
            out["resultados"] = []
        return out
    monkeypatch.setattr(mr, "_prospectiva", prospectiva)
    cli = MockClient()
    b = _bloque(tmp_path, _cfg_div(v6={"prospectiva": {"max_encargos_por_lote": 50}}), cli)
    b.ciclo(AS_OF)
    cob = _cobertura(b)[-1]["prospectiva"]
    assert cob["omitidos"] == [] and sum(1 for x in cli.llamadas if x["agente"] == "AG-10") == 2


def test_prospectiva_no_acepta_refs_no_pedidas(tmp_path, monkeypatch):
    """M25: un resultado para una ref que no estaba en el lote no se toma."""
    orig = mr._prospectiva
    uni = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
    simbolos = list(uni.loc[uni["clase"] == "DIV", "simbolo"])

    def prospectiva(msg, ctx, rng):
        out = orig(msg, ctx, rng)
        pedidas = {e["ref"] for e in msg["encargos"]}
        for sym in simbolos:
            if f"DIV:{sym}" not in pedidas:
                out["resultados"].append({"ref": f"DIV:{sym}", "escenarios": {}, "hitos": [], "indicadores_adelantados": [], "invalidacion": [],
                                          "pronosticos": [{"horizonte": "H2", "vista": "alcista", "prob_interna": 0.6, "escenario_asociado": "BASE",
                                                           "metodo": "ACC-MOM-001", "afirmacion": "PRONOSTICO FALSO"}]})
        return out
    monkeypatch.setattr(mr, "_prospectiva", prospectiva)
    b = _bloque(tmp_path, _cfg_div(v6={"prospectiva": {"max_encargos_por_lote": 1}}))
    r = b.ciclo(AS_OF)
    assert "PRONOSTICO FALSO" not in json.dumps(r["paquete"], ensure_ascii=False)
    assert [e for e in b.almacen.leer("F4") if e.get("tipo_entrada") == "ALTA"]
    assert "PRONOSTICO FALSO" not in json.dumps(b.almacen.leer("F4"), ensure_ascii=False)   # tampoco se congela en F4


def test_el_identificador_opp_no_se_gasta_en_cada_ronda(tmp_path, monkeypatch):
    """M14: las rondas de crítica no piden identificadores OPP- nuevos: los creados son las finalistas."""
    _hunde(monkeypatch)
    b = _bloque(tmp_path, _cfg_div())
    b.ciclo(AS_OF)
    assert len(_cobertura(b)[-1]["critica"]["rondas"]) >= 2
    usados = int(b.almacen.nuevo_id("OPP").rsplit("-", 1)[1]) - 1
    assert usados == len({f["opp_id"] for f in _filas(b, "DIV") if f.get("opp_id")})


def test_gc1_respeta_max_candidatas_y_marca_nan_e_infinito(tmp_path):
    """M01 y H-06."""
    b = _bloque(tmp_path, _cfg_div())
    maxc = parametro(b.cfg, "seleccion.max_candidatas")
    uni = [{"simbolo": f"S{i:02d}", "senales": {"senal_compuesta": 0.9 - i / 1000}} for i in range(maxc + 4)]
    uni += [{"simbolo": "NAN", "senales": {"senal_compuesta": float("nan")}}, {"simbolo": "INF", "senales": {"senal_compuesta": float("inf")}},
            {"simbolo": "TOP", "senales": {"senal_compuesta": 0.95}}]
    filtrado, reg = v6.gc1(b, "DIV", uni, [], AS_OF)
    marcas = {u["simbolo"]: u["gc1"] for u in filtrado}
    assert len(reg["pasan"]) == maxc and marcas["TOP"] == "PASA"
    assert marcas["NAN"] == marcas["INF"] == "SIN_SENAL_MEDIBLE"
    assert all(d["simbolo"] != "TOP" for d in reg["descartes"])


def test_gc1_cuenta_los_falsos_negativos():
    """M23."""
    out = {"gc1": {"exploracion": ["X", "Y"]}, "finalistas": [{"proxy": "X"}, {"proxy": "Z"}]}
    v6.gc1_falsos_negativos(out)
    assert out["gc1"]["falsos_negativos"] == ["X"]


def test_el_analista_sabe_que_gc1_ya_se_aplico(tmp_path):
    """H-05: la instrucción explica las marcas de GC1."""
    cli = MockClient()
    vistos = []
    gen = cli.generar

    def _gen(**kw):
        if kw["agente"] == "AG-05":
            vistos.append(kw["mensajes"][0]["content"])
        return gen(**kw)
    cli.generar = _gen
    _bloque(tmp_path, _cfg_div(), cli).ciclo(AS_OF)
    assert any("ya ha aplicado GC1" in t and "EXPLORACION" in t for t in vistos)


@pytest.mark.parametrize("extra", [{"gc1": {"exploracion_celdas": -1}}, {"prospectiva": {"max_encargos_por_lote": 0}},
                                   {"auditoria_fraccion": 1.5}, {"contradictor": {"proveedor": "tercero"}},
                                   {"cobertura": {"horizonte_contrafactual": "H9"}}, {"analista": {"base_conocimientos": "media"}},
                                   {"sintetizador_limites": {"regimen": 0}}, {"contradictor": {"max_rondas_sustitucion": True}}])
def test_la_seccion_v6_se_valida_al_crear_el_bloque(tmp_path, extra):
    """H-07."""
    with pytest.raises(ValueError, match="v6"):
        _bloque(tmp_path, _cfg_div(v6=extra))


def test_el_override_de_presupuesto_no_cuenta_dos_veces_la_bolsa_del_ciclo(tmp_path):
    """H-07: con `presupuesto_override`, el total es el del override (más la bolsa común)."""
    r = _bloque(tmp_path, _cfg_div()).ciclo(AS_OF, presupuesto_override={"DIV": 10.0})
    pres = r["presupuesto"]
    assert math.isclose(sum(v["asignado"] for v in pres.values()), 10.0 + pres["COMUN"]["asignado"])


def test_el_sintetizador_no_cuela_probabilidades_ni_compras(tmp_path, monkeypatch):
    """H-09: un texto con una probabilidad numérica (R13) o con la compra de un instrumento (R21) no se toma y se declara."""
    orig = mr._sintetizador

    def sintetizador(msg, ctx, rng):
        out = orig(msg, ctx, rng)
        out["regimen_macro"] = "Probabilidad del 87 % de que el dólar suba este trimestre."
        out["lectura_conjunto"] = "Conviene comprar AAPL cuanto antes."
        out["frases_30s"][0] = "Hay una probabilidad del 90 % de ganar."
        return out
    monkeypatch.setattr(mr, "_sintetizador", sintetizador)
    r = _bloque(tmp_path, _cfg_div()).ciclo(AS_OF)
    texto = json.dumps(r["paquete"], ensure_ascii=False)
    assert "87 %" not in texto and "AAPL" not in texto
    lim = " ".join(r["paquete"]["limitaciones"])
    assert "Frases del Sintetizador quitadas (cifras" in lim and "Frases llanas del Sintetizador quitadas" in lim   # T-102 r03


def test_la_cobertura_tiene_fila_para_todo_lo_que_vio_el_analista_y_para_las_vigentes(tmp_path):
    """H-01: cada ámbito que recibe el Analista y cada vigente mantenida en el top-3 tienen su fila."""
    cli = MockClient()
    b = _bloque(tmp_path, _cfg_div(), cli)
    _, cuerpos = _espiar(b, cli)
    b.ciclo(AS_OF)
    vistos = {u["simbolo"] for m in cuerpos["CT-06"] if m.get("fase") == "CRIBADO_E_INVESTIGACION" for u in m["universo"]}
    assert vistos and vistos <= {f["simbolo"] for f in _filas(b, "DIV")}
    r2 = b.ciclo(str((pd.Timestamp(AS_OF) + pd.Timedelta(days=7)).date()))
    top2 = {o["opp_id"] for o in r2["paquete"]["clases"]["DIV"]["opciones"]}
    assert top2 <= {f.get("opp_id") for f in _filas(b, "DIV") if f["fase"] == "SELECCION_FINAL"}


def test_el_contrafactual_espera_si_no_hay_precios_y_no_resuelve_antes_de_vencer(tmp_path, monkeypatch):
    """H-10 y M12: la víspera del vencimiento no resuelve; sin ningún precio al vencer, espera al ciclo siguiente."""
    b = _bloque(tmp_path, _cfg_div())
    b.ciclo(AS_OF)
    cob = _cobertura(b)[0]
    vence = v6._fecha_vencimiento(b, cob["fecha"], cob["horizonte_contrafactual"])
    b.fijar_fecha(vence)   # como en el ciclo: la fecha del bloque fija la guardia de fuga
    assert v6.resolver_contrafactual(b, vence - pd.Timedelta(days=1), "RUN-X") == []   # con los datos ya disponibles: aún no vence
    orig = v6._precio
    monkeypatch.setattr(v6, "_precio", lambda bl, sim, fecha: None if pd.Timestamp(fecha) == vence else orig(bl, sim, fecha))
    assert v6.resolver_contrafactual(b, vence, "RUN-X") == []
    monkeypatch.setattr(v6, "_precio", orig)
    assert len(v6.resolver_contrafactual(b, vence, "RUN-Y")) == 1


def test_la_v6_no_llama_al_evaluador_aunque_haya_resueltos(tmp_path):
    """M24: con pronósticos resueltos, la V6 no llama a AG-20 (las lecciones deterministas siguen)."""
    cli = MockClient()
    b = _bloque(tmp_path, _cfg_div(), cli)
    b.ciclo(AS_OF)
    b.ciclo(str((pd.Timestamp(AS_OF) + pd.Timedelta(days=60)).date()))
    assert [e for e in b.almacen.leer("F4") if e.get("tipo_entrada") == "RESOLUCION"]
    assert not any(x["agente"] == "AG-20" for x in cli.llamadas)


@pytest.mark.parametrize(("fraccion", "llamadas"), [(0.0, 0), (1.0, 1)])
def test_el_auditor_por_muestreo_en_el_ciclo_vivo(tmp_path, fraccion, llamadas):
    """M26."""
    cli = MockClient()
    b = _bloque(tmp_path, _cfg_div(modo="vivo", v6={"auditoria_fraccion": fraccion}), cli)
    b.ciclo(AS_OF)
    assert sum(1 for x in cli.llamadas if x["agente"] == "AG-19") == llamadas


# ================================================================================================ QA r02 de T-101 (ronda r03)
# T-102 r03: con marcadores, el texto libre del Sintetizador no lleva cifras ni tickers; las frases legítimas son las escritas
# así, y lo que antes era R13 se quita ahora por llevar una cifra (CIFRA)
LEGITIMOS_R21 = ["Varias opciones del mismo clúster comparten el factor de riesgo.",
                 "La probabilidad es baja; aun así, el capital se concentra en el mismo factor.",
                 "Los pronósticos con probabilidad alta acertaron a menudo en el historial.",
                 "¿Conviene vender USD frente al EUR si el diferencial de tipos se estrecha?",
                 "El Analista prefiere no comprar RF larga mientras suba la inflación.",
                 "Con el dólar fuerte, puede tener sentido vender EM y esperar.",
                 "El fondo de referencia de {opp:OPP-2026-0001} sigue al índice; no es una recomendación.",
                 "Si la curva se empina, el segmento de vender HY pierde atractivo."]
PROHIBIDOS_R13_R21 = [("CIFRA", "Probabilidad del 87 % de que el dólar suba este trimestre."), ("CIFRA", "Hay un 70 % de probabilidad de subida."),
                      ("CIFRA", "La probabilidad de subida es de 0,87."), ("CIFRA", "Vemos un 87 por ciento de probabilidades de subida."),
                      ("CIFRA", "Un 80 % de posibilidades de que el euro baje."), ("CIFRA", "El escenario base tiene un 65 % de opciones de cumplirse."),
                      ("R21", "Conviene comprar AAPL cuanto antes."), ("R21", "Compra acciones de Apple (AAPL)."),
                      ("R21", "Recomendamos la compra de AAPL y de MSFT."), ("R21", "Sobreponderar Microsoft Corp frente al índice."),
                      ("CIFRA", "Comprar el bono del Tesoro a 10 años con vencimiento 2034."), ("CIFRA", "Comprar US0378331005 ya."),
                      ("R21", "El ETF de referencia (SPY) sigue al índice.")]


def test_el_filtro_r13_r21_caza_los_casos_con_patron_y_respeta_los_legitimos(tmp_path):
    """H-12: con los códigos permitidos de la configuración y del universo, ningún texto legítimo se tira y los prohibidos con
    patrón se cazan (un nombre propio sin patrón, como «entrar en Tesla», es un límite declarado)."""
    perm = v6.permitidos_r21(_bloque(tmp_path, _cfg_div()))
    assert [t for t in LEGITIMOS_R21 if v6.texto_prohibido(t, perm)] == []
    assert [(r, t) for r, t in PROHIBIDOS_R13_R21 if v6.texto_prohibido(t, perm) != r] == []


def test_el_ejemplo_de_la_qa_r01_no_llega_al_paquete(tmp_path, monkeypatch):
    """H-12: «compra acciones de Apple (AAPL)» en la lectura del conjunto y en una frase llana no llega al paquete ni a los entregables."""
    orig = mr._sintetizador
    txt = "Para esta semana, compra acciones de Apple (AAPL) antes de resultados."

    def sintetizador(msg, ctx, rng):
        out = orig(msg, ctx, rng)
        out["lectura_conjunto"], out["frases_30s"][1] = txt, txt
        return out
    monkeypatch.setattr(mr, "_sintetizador", sintetizador)
    r = _bloque(tmp_path, _cfg_div()).ciclo(AS_OF)
    assert "AAPL" not in json.dumps([r["paquete"], r["entregables"]], ensure_ascii=False, default=str)


def test_cobertura_en_un_ciclo_ligero_con_rotacion_y_sin_filas_contradictorias(tmp_path):
    """H-13, H-14 y H-15: en un ciclo N1, la rotación exploratoria tiene fila; ninguna opción tiene a la vez fila de «no
    propuesta» y de selección; las vigentes del top-3 llevan símbolo y precio en `elegidas`."""
    b = _bloque(tmp_path, _cfg_div())
    b.ciclo(AS_OF)
    r2 = b.ciclo(str((pd.Timestamp(AS_OF) + pd.Timedelta(days=7)).date()))
    assert r2["nivel_por_clase"]["DIV"] == "N1"
    d = _cobertura(b)[-1]["clases"]["DIV"]
    rot = [f for f in d["filas"] if f["fase"] in ("ROTACION", "EXPLORATORIA_F3")]
    assert rot and len(rot) <= parametro(b.cfg, "seleccion.rotacion_exploratoria_celdas")
    seleccion = {f["simbolo"] for f in d["filas"] if f["fase"] == "SELECCION_FINAL"}
    assert not seleccion & {f["simbolo"] for f in d["filas"] if f["fase"] == "ANALISTA"}
    assert not seleccion & {x["simbolo"] for x in d["muestra_descartes"]}
    assert d["elegidas"] and all(x["simbolo"] and x["precio"] for x in d["elegidas"])


def test_el_embudo_cuenta_el_gc1_del_codigo(tmp_path):
    """H-16: con GC1 por código, el embudo del paquete y las decisiones de F5 dicen lo que dejó pasar el código (con el umbral de la
    configuración, 0,75, distinto del 0,55 con el que el Analista simulado marca `paso_gc1`)."""
    b = _bloque(tmp_path, _cfg_div(seleccion={"umbral_senal_gc1": 0.75}))
    r = b.ciclo(AS_OF)
    g = _cobertura(b)[-1]["clases"]["DIV"]["gc1"]
    emb = r["paquete"]["clases"]["DIV"]["embudo"]
    assert emb["pasan_gc1"] == len(g["pasan"]) and emb["cribadas"] == g["universo"]
    run = [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "RUN"][-1]
    gc1 = [x for x in run.get("decisiones_puertas", []) if x["puerta"] == "GC1"]
    assert {x["objeto"] for x in gc1 if x["resultado"]} == set(g["pasan"])


def test_un_finalista_que_gc1_no_envio_no_vale(tmp_path, monkeypatch):
    """H-17: si el Analista devuelve como finalista un ámbito que GC1 no le envió, se descarta (PS3)."""
    orig = mr._analista
    uni = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
    div = list(uni.loc[uni["clase"] == "DIV", "simbolo"])
    capt = {}

    def analista(msg, ctx, rng, iny):
        out = orig(msg, ctx, rng, iny)
        if msg.get("fase") == "CRIBADO_E_INVESTIGACION" and out.get("finalistas"):
            enviados = {u["simbolo"] for u in msg["universo"]}
            fuera = [s for s in div if s not in enviados]
            if fuera:
                capt["fuera"] = fuera[0]
                f = copy.deepcopy(out["finalistas"][0])
                f["indicador_seguimiento"]["simbolo"], f["nombre"] = fuera[0], f"Ámbito {fuera[0]}"
                out["finalistas"].append(f)
        return out
    monkeypatch.setattr(mr, "_analista", analista)
    b = _bloque(tmp_path, _cfg_div(seleccion={"umbral_senal_gc1": 0.9}))
    r = b.ciclo(AS_OF)
    assert capt.get("fuera") and capt["fuera"] not in _entregadas(r, "DIV")
    assert capt["fuera"] not in {f["simbolo"] for f in _filas(b, "DIV") if f.get("opp_id")}


def test_el_override_de_la_bolsa_del_ciclo_se_respeta_y_vacia_deja_el_run_parcial(tmp_path):
    """H-18: un `presupuesto_override` de V6_GLOBAL se respeta tal cual; con la bolsa vacía, el ciclo queda PARCIAL y declara el cierre."""
    r = _bloque(tmp_path, _cfg_div()).ciclo(AS_OF, presupuesto_override={v6.BOLSA_GLOBAL: 0.001})
    assert math.isclose(r["presupuesto"][v6.BOLSA_GLOBAL]["asignado"], 0.001)
    assert r["estado"] == "PARCIAL" and any("Presupuesto agotado" in x for x in r["paquete"]["limitaciones"])


def test_gc1_con_senal_desconocida_falla_y_gc1_nulo_no_rompe(tmp_path):
    """H-19."""
    with pytest.raises(ValueError, match="senal_por_perfil"):
        _bloque(tmp_path, _cfg_div(v6={"gc1": {"senal_por_perfil": {"DIV": "no_existe"}}}))
    with pytest.raises(ValueError, match="senal_por_perfil"):
        _bloque(tmp_path / "b", _cfg_div(v6={"gc1": {"senal_por_perfil": {"XXX": "senal_compuesta"}}}))
    assert _bloque(tmp_path / "c", _cfg_div(v6={"gc1": {"senal_por_perfil": {"DIV": "momentum_12_1"}}})).v6


def test_el_contrafactual_sin_precios_se_cierra_no_resoluble_al_acabar_la_espera(tmp_path, monkeypatch):
    """H-20: sin precios al vencer se espera `dias_max_espera_precio` días; después se cierra como NO_RESOLUBLE, una vez."""
    b = _bloque(tmp_path, _cfg_div())
    b.ciclo(AS_OF)
    cob = _cobertura(b)[0]
    vence = v6._fecha_vencimiento(b, cob["fecha"], cob["horizonte_contrafactual"])
    espera = parametro(b.cfg, "v6.cobertura.dias_max_espera_precio")
    monkeypatch.setattr(v6, "_precio", lambda bl, sim, fecha: None if pd.Timestamp(fecha) >= vence else 1.0)
    for dias, n in ((0, 0), (espera, 0), (espera + 1, 1), (espera + 9, 0)):
        b.fijar_fecha(vence + pd.Timedelta(days=dias))
        ctf = v6.resolver_contrafactual(b, vence + pd.Timedelta(days=dias), f"RUN-{dias}")
        assert len(ctf) == n, dias
        if n:
            assert ctf[0]["estado"] == "NO_RESOLUBLE" and all(c["estado"] in ("SIN_DATOS", "SIN_MUESTRA") for c in ctf[0]["clases"].values())


def test_el_reintento_del_contradictor_no_sale_de_la_cache(tmp_path, monkeypatch):
    """H-22 (N06): si el Contradictor no devuelve nada la primera vez, el reintento llega al modelo y la opción se critica."""
    orig = mr._contrarias

    def contrarias(msg, ctx, rng):
        out = orig(msg, ctx, rng)
        if "contrarreplicas" not in msg and "reintento_de_cobertura" not in msg:
            out["resultados"] = []
        return out
    monkeypatch.setattr(mr, "_contrarias", contrarias)
    b = _bloque(tmp_path, _cfg_div(v6={"prospectiva": {"max_encargos_por_lote": 50}}))
    b.ciclo(AS_OF)
    assert _cobertura(b)[-1]["critica"]["sin_respuesta"] == []


def test_la_vigente_cerrada_tiene_su_fila(tmp_path, monkeypatch):
    """H-22 (N13): una vigente que el Analista recomienda cerrar tiene su fila CIERRE."""
    b = _bloque(tmp_path, _cfg_div())
    b.ciclo(AS_OF)
    orig = mr._analista

    def analista(msg, ctx, rng, iny):
        out = orig(msg, ctx, rng, iny)
        for rv in out.get("revision_vigentes", []):
            rv["recomendacion"] = "CERRAR"
        return out
    monkeypatch.setattr(mr, "_analista", analista)
    b.ciclo(str((pd.Timestamp(AS_OF) + pd.Timedelta(days=7)).date()))
    assert [f for f in _filas(b, "DIV") if f["fase"] == "CIERRE"]


def test_el_sintetizador_respeta_el_tope_de_preguntas_y_el_presupuesto_del_mensaje(tmp_path, monkeypatch):
    """H-22 (N18 y N22): como mucho `sintetizador_limites.preguntas` preguntas; el mensaje CT-15 declara la bolsa común."""
    orig = mr._sintetizador

    def sintetizador(msg, ctx, rng):
        out = orig(msg, ctx, rng)
        out["preguntas_sugeridas"] = [f"¿Pregunta de prueba {chr(97 + i)}?" for i in range(20)]   # sin cifras (T-102 r03)
        return out
    monkeypatch.setattr(mr, "_sintetizador", sintetizador)
    cli = MockClient()
    b = _bloque(tmp_path, _cfg_div(), cli)
    crear, ct15 = b.mensajeria.crear, []

    def _crear(contrato, emisor, receptor, cuerpo, **k):
        if contrato == "CT-15":
            ct15.append(k.get("presupuesto"))
        return crear(contrato, emisor, receptor, cuerpo, **k)
    b.mensajeria.crear = _crear
    r = b.ciclo(AS_OF)
    assert len(r["paquete"]["preguntas_sugeridas"]) == parametro(b.cfg, "v6.sintetizador_limites")["preguntas"]
    assert ct15 and ct15[0]["uc"] == r["presupuesto"]["COMUN"]["asignado"]
