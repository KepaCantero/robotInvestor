"""T-158 · Guías de mejora del Orquestador (CT-18) en el ejecutor: esquema, emisión, revisión del receptor (R23), registro
COR- y P3- en HA, retirada del ítem y aplicación en el contexto del agente. PB-48 de extremo a extremo con el cliente simulado."""
import copy
import datetime as dt
import json

import pytest
from bloque_a.configuracion import cargar_config
from bloque_a.contratos import DatosSensibles, MensajeInvalido
from bloque_a.herramientas import ht03
from conftest import AS_OF, config_pruebas, nuevo_bloque
from test_fase4_huecos import IBAN

from bloque_a import guias as G
from bloque_a import mock_respuestas

PB48 = "Omitir la segunda pasada en banda marginal para ahorrar"
VALIDO = "En la integración, cita primero el régimen macro y después los factores dominantes"


def item(que=VALIDO, **extra):
    return {"tipo": 2, "origen": ["LEC-2026-0901"], "que_cambia": que, "donde_se_comprueba": "campo lectura_conjunto (CT-05)",
            "como_se_sabe": "revisión del Auditor sin hallazgo de orden durante 4 ciclos", **extra}


def guias_ha(b, tipo=None):
    return [e for e in b.almacen.leer("HA") if e["tipo_entrada"] in ((tipo,) if tipo else ("GUI", "COR", "P3"))]


@pytest.fixture
def b(tmp_path, universo):
    blq = nuevo_bloque(tmp_path, universo)
    blq.fijar_fecha(AS_OF)
    return blq


# ------------------------------------------------------------------------------------------- esquema (va primero)
def test_el_ejemplo_del_prompt_del_orquestador_cumple_el_esquema():
    """Prompt del Orquestador 4.5, con `tipo_ct18` en lugar de `tipo_mensaje` (el sobre del ejecutor ya usa ese campo)."""
    ejemplo = {"tipo_ct18": "GUIA", "guia_id": "GUI-AG05-0004", "version": 4, "sustituye": "GUI-AG05-0003",
               "fecha_aplicacion": "2026-11-16", "acuse_requerido": True,
               "items": [{"item_id": "GUI-AG05-0004-01", "tipo": 2, "origen": ["HAL-2026-0118", "LEC-2026-0031"],
                          "que_cambia": "En cribado DIV, comprobar el diferencial de carry ajustado por volatilidad con datos de "
                                        "HT-01 de ≤ 3 días antes de proponer candidatas H2",
                          "donde_se_comprueba": "campo cribado[].senal del informe de clase (CT-06)",
                          "como_se_sabe": "HT-09 G3-DAT-02 sin fallos en DIV durante 4 ciclos", "caducidad": "2027-02-15"}]}
    cfg = cargar_config()
    assert G.validar_cuerpo(ejemplo, "AG-05", cfg) == []
    assert G.conflicto_del_item(ejemplo["items"][0]) is None              # una guía corriente no es un conflicto
    tal_cual = {k: v for k, v in ejemplo.items() if k != "tipo_ct18"} | {"tipo_mensaje": "GUIA"}
    assert any("tipo_ct18" in e for e in G.validar_cuerpo(tal_cual, "AG-05", cfg))
    assert G.validar_cuerpo(ejemplo, "AG-02", cfg)                         # la guía es de AG-05, no de otro agente


@pytest.mark.parametrize("cambio, error", [
    (lambda c: c["items"][0].__setitem__("tipo", 3), "items/0/tipo"),
    (lambda c: c["items"][0].__setitem__("tipo", True), "items/0/tipo"),
    (lambda c: c["items"][0].__setitem__("origen", []), "items/0/origen"),
    (lambda c: c["items"][0].__setitem__("origen", ["OTRO-1"]), "items/0/origen/0"),
    (lambda c: c["items"][0].__setitem__("que_cambia", ""), "items/0/que_cambia"),
    (lambda c: c["items"][0].pop("como_se_sabe"), "items/0"),
    (lambda c: c["items"][0].__setitem__("caducidad", "2026-13-01"), "caducidad no válida"),
    (lambda c: c["items"][0].__setitem__("caducidad", "2026-01-01"), "caduca antes"),
    (lambda c: c["items"][0].__setitem__("item_id", "GUI-AG02-0009-01"), "no es un ítem"),
    (lambda c: c.__setitem__("items", []), "items"),
    (lambda c: c.__setitem__("acuse_requerido", False), "acuse_requerido"),
    (lambda c: c.__setitem__("version", 2), "no corresponde a la versión"),
    (lambda c: c.__setitem__("sustituye", "GUI-AG02-0001"), "versión 1"),
    (lambda c: c.__setitem__("fecha_aplicacion", "2026-02-30"), "fecha_aplicacion no válida"),
])
def test_el_esquema_rechaza_cuerpos_mal_formados(cambio, error):
    cuerpo = {"tipo_ct18": "GUIA", "guia_id": "GUI-AG02-0001", "version": 1, "sustituye": None, "fecha_aplicacion": AS_OF,
              "acuse_requerido": True, "items": [{"item_id": "GUI-AG02-0001-01", "caducidad": "2026-12-05", **item()}]}
    cfg = cargar_config()
    assert G.validar_cuerpo(cuerpo, "AG-02", cfg) == []
    cambio(cuerpo)
    errores = G.validar_cuerpo(cuerpo, "AG-02", cfg)
    assert errores and any(error in e for e in errores), errores


# ------------------------------------------------------------------------------------------- emisión
def test_emitir_deja_la_guia_en_ha_con_su_acuse_y_la_envia_por_ct18(b):
    r = b.guias.emitir("AG-02", [item()], as_of=AS_OF)
    assert r["guia_id"] == "GUI-AG02-0001" and r["items"] == ["GUI-AG02-0001-01"] and r["acuse"]["asignado"] == "AG-02"
    msg = [m for m in b.mensajeria.registro if m["contrato"] == "CT-18"]
    assert msg == [{"msg_id": r["msg_id"], "contrato": "CT-18", "emisor": "AG-18", "receptor": "AG-02", "tipo_mensaje": "ENCARGO"}]
    g = b.guias.todas()["GUI-AG02-0001"]
    assert g["estado"] == "ISSUED" and g["acuse"] and g["msg_id"] == r["msg_id"] and g["agente"] == "AG-02"
    meses = b.cfg["guias_orquestador"]["caducidad_por_defecto_meses"]                       # dos trimestres (6.9)
    assert g["items"][0]["caducidad"] == G._mas_meses(dt.date.fromisoformat(AS_OF), meses).isoformat() == "2026-12-05"
    assert G.validar_cuerpo(b.guias.cuerpo(g), "AG-02", b.cfg) == []


def test_la_version_siguiente_sustituye_a_la_vigente(b):
    b.guias.emitir("AG-02", [item()], as_of=AS_OF)
    r = b.guias.emitir("AG-02", [item(), item("En la integración, nombra el régimen de cada tipo en una frase")], as_of=AS_OF)
    assert (r["guia_id"], r["version"], r["sustituye"]) == ("GUI-AG02-0002", 2, "GUI-AG02-0001")
    todas = b.guias.todas()
    assert todas["GUI-AG02-0001"]["estado"] == "SUPERSEDED" and todas["GUI-AG02-0001"]["sustituida_por"] == "GUI-AG02-0002"
    assert list(b.guias.vigentes("AG-02")) == ["GUI-AG02-0002"]
    assert b.guias.emitir("AG-05", [item()], as_of=AS_OF)["guia_id"] == "GUI-AG05-0001"   # versionado por agente


@pytest.mark.parametrize("receptor, items", [
    ("AG-02", [item(tipo=3)]),
    ("AG-02", [item(origen=[])]),
    ("AG-02", [item(caducidad="2026-01-01")]),
    ("AG-02", []),
    ("AG-02", "no es una lista"),
    ("BROKER", [item()]),
    ("AG-99", [item()]),
    ("AG-02", [item() for _ in range(9)]),                                              # 8 ítems por versión (6.9)
    ("AG-02", [item(origen=[f"HAL-2026-{n:04d}" for n in range(11)])]),                 # 10 hallazgos por versión
])
def test_una_guia_mal_formada_no_se_emite_y_nada_cambia(b, receptor, items):
    antes_ha, antes_msg = b.almacen.leer("HA"), list(b.mensajeria.registro)
    with pytest.raises(MensajeInvalido):
        b.guias.emitir(receptor, items, as_of=AS_OF)
    assert b.almacen.leer("HA") == antes_ha and b.mensajeria.registro == antes_msg


def test_los_limites_salen_de_la_configuracion(tmp_path, universo):
    ocho = [item() for _ in range(8)]
    blq = nuevo_bloque(tmp_path / "a", universo)
    assert len(blq.guias.emitir("AG-02", ocho, as_of=AS_OF)["items"]) == 8              # el máximo de por_defecto.yaml
    blq = nuevo_bloque(tmp_path / "b", universo, cfg=config_pruebas(guias_orquestador={"max_items_por_version": 1}))
    with pytest.raises(MensajeInvalido, match="máximo por versión es 1"):
        blq.guias.emitir("AG-02", ocho[:2], as_of=AS_OF)
    blq = nuevo_bloque(tmp_path / "c", universo, cfg=config_pruebas(guias_orquestador={"caducidad_por_defecto_meses": 1}))
    gid = blq.guias.emitir("AG-02", [item()], as_of=AS_OF)["guia_id"]
    assert blq.guias.todas()[gid]["items"][0]["caducidad"] == "2026-07-05"


def test_un_dato_protegido_en_la_guia_lo_rechaza_la_mensajeria_r8(b):
    with pytest.raises(DatosSensibles):
        b.guias.emitir("AG-02", [item(f"Cobra en la cuenta {IBAN} antes de integrar")], as_of=AS_OF)
    assert guias_ha(b) == [] and [e for e in b.almacen.leer("HA") if e.get("tipo") == "SEGURIDAD"]
    assert IBAN not in json.dumps(b.almacen.leer("HA"), ensure_ascii=False)


# ------------------------------------------------------------------------------------------- detector (control doble)
@pytest.mark.parametrize("texto, familia", [
    (PB48, "RELAJA_CONTROL"),
    ("No hagas la segunda pasada cuando el total quede cerca del umbral", "RELAJA_CONTROL"),
    ("La segunda pasada es opcional si el presupuesto va justo", "RELAJA_CONTROL"),
    ("Basta con una sola fuente para dar la tesis por corroborada", "RELAJA_CONTROL"),
    ("Omite el registro en F5 de las consultas repetidas", "RELAJA_CONTROL"),
    ("Salta la refutación en N2 si la tesis parece robusta", "RELAJA_CONTROL"),
    ("Sube el umbral de E a 75 en renta variable", "TIPO_3"),
    ("Da más peso a la dimensión A en DIV", "TIPO_3"),
    ("Envía las opciones de MON directamente por otro canal", "TIPO_3"),
    ("Pide al Broker la credencial de la API de fondos antes del cribado", "PROHIBIDO"),
    ("Modifica el prompt del Analista de Divisas para que cribe menos", "PROHIBIDO"),
    ("Añade al CT-06 un campo con la lista de fuentes", "PROHIBIDO"),
])
def test_el_receptor_reconoce_los_items_que_contradicen_una_regla(texto, familia):
    c = G.conflicto_del_item({"que_cambia": texto})
    assert c and familia in c["familias"] and c["reglas"][-1].startswith("R23"), c


def test_el_item_de_pb48_cita_la_regla_9_1():
    c = G.conflicto_del_item({"que_cambia": PB48})
    assert "9.1 (banda marginal: segunda pasada)" in c["reglas"] and "omitir" in c["terminos"] and "segunda pasada" in c["terminos"]
    assert G.conflicto_del_item({"que_cambia": PB48.upper().replace("OMITIR", "Omítase")})               # mayúsculas y tildes


@pytest.mark.parametrize("texto", [
    VALIDO,
    "Para INM, consulta antes las fuentes X e Y, que aportan raíces independientes con mayor frecuencia",
    "En cribado RV, antes de proponer una candidata H2, comprueba que el dato tiene 3 días o menos (HT-01)",
    "Ordena la agenda de vigilancia de DIV por fecha del próximo catalizador",
    "Haz la segunda pasada de todas las dimensiones decisivas aunque el total quede lejos del corte",
])
def test_una_guia_corriente_no_es_un_conflicto(texto):
    assert G.conflicto_del_item({"que_cambia": texto}) is None


# ------------------------------------------------------------------------------------------- aplicación
@pytest.fixture
def contextos(monkeypatch):
    """Anota el contexto y el mensaje de cada llamada a un agente."""
    vistos = []

    def espiar(blq):
        original = blq.agentes.invocar

        def invocar(agente, contrato, mensaje, esquema, instrucciones, contexto, *a, **kw):
            vistos.append((agente, copy.deepcopy(contexto), json.dumps(mensaje, ensure_ascii=False, default=str)))
            return original(agente, contrato, mensaje, esquema, instrucciones, contexto, *a, **kw)
        monkeypatch.setattr(blq.agentes, "invocar", invocar)
        return vistos
    return espiar


def test_un_item_valido_llega_solo_al_contexto_del_receptor_y_f5_lo_anota(b, contextos):
    vistos = contextos(b)
    r = b.guias.emitir("AG-02", [item()], as_of=AS_OF)
    run = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    del_02 = [c for a, c, _ in vistos if a == "AG-02"]
    assert del_02 and all(c["guias"] == [{"guia_id": r["guia_id"], "item_id": r["items"][0], "tipo": 2, "que_cambia": VALIDO,
                                          "donde_se_comprueba": item()["donde_se_comprueba"],
                                          "como_se_sabe": item()["como_se_sabe"]}] for c in del_02)
    assert all("guias" not in c for a, c, _ in vistos if a != "AG-02")
    f5 = b.almacen.estado("F5")[run["run_id"]]
    assert f5["guias_aplicadas"] == {"AG-02": [r["guia_id"]]}
    assert guias_ha(b, "COR") == [] and guias_ha(b, "P3") == []


def test_una_guia_futura_o_caducada_no_se_aplica(b):
    b.guias.emitir("AG-02", [item()], as_of=AS_OF, fecha_aplicacion="2026-06-12")
    assert b.guias.para("AG-02", AS_OF, "RUN-X") == []
    assert b.guias.para("AG-02", "2026-06-12", "RUN-Y")                                  # el día de su aplicación, sí
    b.guias.emitir("AG-05", [item(caducidad="2026-06-10")], as_of=AS_OF)
    assert b.guias.para("AG-05", "2026-06-10", "RUN-Z")                                  # el día de su caducidad, aún sí
    b.fijar_fecha("2026-06-11")
    assert b.guias.para("AG-05", "2026-06-11", "RUN-W") == []
    assert b.guias.todas()["GUI-AG05-0001"]["estado"] == "RETIRADA"


def test_una_guia_de_ha_que_no_cumple_el_esquema_no_se_aplica(b):
    b.almacen.escribir("HA", "AG-18", {"tipo_entrada": "GUI", "id": "GUI-AG02-0001", "guia_id": "GUI-AG02-0001", "agente": "AG-02",
                                       "version": 1, "sustituye": None, "fecha_aplicacion": AS_OF, "estado": "ISSUED",
                                       "items": [{"item_id": "GUI-AG02-0001-01", "caducidad": "2026-12-05", **item(tipo=3)}]})
    assert b.guias.para("AG-02", AS_OF, "RUN-X") == []
    assert b.guias.todas()["GUI-AG02-0001"]["estado"] == "RETIRADA"
    assert [e for e in b.almacen.leer("HA") if e.get("tipo") == "HERRAMIENTA" and "GUI-AG02-0001" in e["detalle"]]


def test_si_la_revision_falla_no_se_aplica_ninguna_guia(b, monkeypatch):
    b.guias.emitir("AG-02", [item()], as_of=AS_OF)

    def roto(_):
        raise RuntimeError("detector roto")
    monkeypatch.setattr(G, "conflicto_del_item", roto)
    assert b.guias.para("AG-02", AS_OF, "RUN-X") == []
    assert [e for e in b.almacen.leer("HA") if e.get("tipo") == "HERRAMIENTA" and "no se aplica ninguna" in e["detalle"]]


def test_sin_guias_el_ciclo_no_escribe_ni_envia_nada_de_ct18(b, contextos):
    vistos = contextos(b)
    run = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert guias_ha(b) == [] and not [m for m in b.mensajeria.registro if m["contrato"] == "CT-18"]
    assert all("guias" not in c for _, c, _ in vistos) and "guias_aplicadas" not in b.almacen.estado("F5")[run["run_id"]]


# ------------------------------------------------------------------------------------------- PB-48 de extremo a extremo
@pytest.fixture
def ciclo_pb48_guia(tmp_path, universo, monkeypatch, contextos):
    """El caso del plan con la guía CT-18 de verdad: guía de tipo 2 vigente para el Analizador (AG-02) que sugiere omitir la
    segunda pasada en banda marginal y el Analista simulado que la hace para todas las dimensiones (como en T-126 r02)."""
    original = mock_respuestas._ficha

    def ficha(u, msg, ctx, rng, inyectado):
        f = original(u, msg, ctx, rng, inyectado)
        f["segunda_pasada"] = {k: dict(v) for k, v in f["dimensiones"].items() if isinstance(v, dict)}
        return f
    monkeypatch.setattr(mock_respuestas, "_ficha", ficha)
    evaluadas = []
    evaluar = ht03.evaluar_opcion

    def anotar(op, *args, **kwargs):
        r = evaluar(op, *args, **kwargs)
        evaluadas.append((op, r))
        return r
    monkeypatch.setattr(ht03, "evaluar_opcion", anotar)

    def preparar(items):
        blq = nuevo_bloque(tmp_path, universo)
        blq.fijar_fecha(AS_OF)
        vistos = contextos(blq)
        # paso 1: el Analizador recibe la guía (T-161: el emisor ya la rechaza; PB-48 supone que su filtro falló)
        emitida = blq.guias.emitir("AG-02", items, as_of=AS_OF, simular_fallo_del_emisor=True)
        run = blq.ciclo(AS_OF, alcance={"clases": ["RV"]})                               # paso 2: una selección con banda marginal
        return blq, emitida, run, vistos, [(op, res) for op, res in evaluadas if op.get("opp_id") != "PROV"]
    return preparar


def test_pb48_la_guia_que_omite_la_segunda_pasada_se_registra_se_escala_y_se_retira(ciclo_pb48_guia):
    b, emitida, run, vistos, evaluadas = ciclo_pb48_guia([item(PB48, origen=["LEC-2026-0901"])])
    # La regla más restrictiva manda: la segunda pasada se hace y queda registrada en F3
    marginales = [(op, res) for op, res in evaluadas if res["banda_marginal"]]
    assert marginales
    for op, res in marginales:
        assert op["segunda_pasada"] and "PS8_BANDA_MARGINAL" not in [m["codigo"] for m in res["motivos_no_elegible"]]
    f3 = b.almacen.estado("F3")
    registradas = [op["opp_id"] for op, _ in marginales if op["opp_id"] in f3]
    assert registradas and all(f3[o].get("segunda_pasada") for o in registradas)
    # COR- y P3- en HA
    (cor,), (p3,) = guias_ha(b, "COR"), guias_ha(b, "P3")
    assert cor["entrada_corregida"] == emitida["guia_id"] and cor["item_id"] == emitida["items"][0]
    assert cor["detectado_por"] == "AG-02" and cor["run_id"] == run["run_id"] and cor["p3_id"] == p3["id"]
    assert "9.1 (banda marginal: segunda pasada)" in cor["conflicto"]["reglas"] and "R23" in cor["motivo"]
    assert set(cor["comunicado_a"]) == {"AG-02", "AG-18", "OPERADOR"}
    assert p3["id"].startswith("P3-ORQ-") and p3["origen"] == "ORQ" and p3["estado"] == "PENDING_OPERATOR"
    assert p3["reclasificado_a"] == 3 and p3["tipo_declarado"] == 2 and p3["evidencia"]["cor_id"] == cor["id"]
    assert "PB-48" in p3["pruebas_regresion"] and p3["_autor"] == cor["_autor"] == "AG-18"
    assert p3["id"] in b.almacen.estado("HA") and b.almacen.estado("HA")[p3["id"]]["estado"] == "PENDING_OPERATOR"   # cola de tipo 3
    # El Orquestador lo retira de la guía (era su único ítem): RETIRADA, sin versión nueva
    g = b.guias.todas()[emitida["guia_id"]]
    assert g["estado"] == "RETIRADA" and p3["id"] in g["motivo"] and b.guias.vigentes("AG-02") == {}
    # Su texto no llega a ningún agente ni a HT-03
    assert vistos and all(PB48 not in json.dumps(c, ensure_ascii=False) + m for _, c, m in vistos)
    assert all(PB48 not in repr(op) for op, _ in evaluadas)
    assert "guias_aplicadas" not in b.almacen.estado("F5")[run["run_id"]]


def test_pb48_con_otro_item_valido_la_version_siguiente_conserva_solo_el_valido(ciclo_pb48_guia):
    b, emitida, run, vistos, _ = ciclo_pb48_guia([item(PB48), item()])
    todas = b.guias.todas()
    assert todas[emitida["guia_id"]]["estado"] == "SUPERSEDED"
    (nueva_id,) = b.guias.vigentes("AG-02")
    nueva = todas[nueva_id]
    assert nueva["sustituye"] == emitida["guia_id"] and [i["que_cambia"] for i in nueva["items"]] == [VALIDO]
    assert "P3-ORQ-" in nueva["motivo"]
    ct18 = [m for m in b.mensajeria.registro if m["contrato"] == "CT-18"]
    assert [m["msg_id"] for m in ct18] == [emitida["msg_id"], nueva["msg_id"]] and {m["receptor"] for m in ct18} == {"AG-02"}
    del_02 = [c for a, c, _ in vistos if a == "AG-02"]
    assert del_02 and all([i["que_cambia"] for i in c["guias"]] == [VALIDO] for c in del_02)
    assert b.almacen.estado("F5")[run["run_id"]]["guias_aplicadas"] == {"AG-02": [nueva_id]}
    assert len(guias_ha(b, "COR")) == len(guias_ha(b, "P3")) == 1


def test_pb48_una_guia_ya_vigente_se_revisa_tambien_en_el_siguiente_run(b):
    """Una guía que quedó ISSUED sin revisar (p. ej., de antes de T-158) se revisa en el F0 del run siguiente."""
    b.almacen.escribir("HA", "AG-18", {"tipo_entrada": "GUI", "id": "GUI-AG02-0001", "guia_id": "GUI-AG02-0001", "agente": "AG-02",
                                       "version": 1, "sustituye": None, "fecha_aplicacion": AS_OF, "estado": "ISSUED",
                                       "items": [{"item_id": "GUI-AG02-0001-01", "caducidad": "2026-12-05", **item(PB48)}]})
    run = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    (cor,) = guias_ha(b, "COR")
    assert cor["run_id"] == run["run_id"] and b.guias.todas()["GUI-AG02-0001"]["estado"] == "RETIRADA"


def test_determinismo_misma_entrada_mismas_entradas_de_ha(tmp_path, universo):
    def huella(sub):
        blq = nuevo_bloque(tmp_path / sub, universo)
        blq.fijar_fecha(AS_OF)
        blq.guias.emitir("AG-02", [item(PB48), item()], as_of=AS_OF, simular_fallo_del_emisor=True)   # T-161 (H-05)
        blq.guias.cargar(AS_OF, "RUN-2026-0001")
        return [{k: v for k, v in e.items() if k not in ("_ts", "_hash", "_hash_prev")} for e in guias_ha(blq)]
    assert huella("a") == huella("b")
