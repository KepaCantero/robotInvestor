"""T-169 · hallazgos de la QA r01 de T-162 (respuesta final por CT-03, PB-07): H-01 a H-04.

Todo con el cliente simulado (`MockClient`), sin red ni coste. Los escenarios baratos usan un bloque solo con divisas; los que
necesitan opciones entregadas, un ciclo de renta variable y la consulta de PB-07 (una vez por módulo; la vista de F3 y F5 se
retoca sin escribir en el almacén).
"""
import copy
import json

import pytest
from bloque_a.almacen import EscrituraFueraDeReserva, PronosticoCongelado
from bloque_a.configuracion import cargar_config
from bloque_a.contratos import CanalNoPrevisto, DatosSensibles, MensajeInvalido
from bloque_a.herramientas.ht01_datos import FugaDeInformacion
from conftest import AS_OF, nuevo_bloque

from bloque_a import respuesta_final

PB07 = "¿Qué opinas de la renta variable india frente a la indonesia a 6 meses?"
DIV = "Analiza qué conviene hacer ahora"                   # el simulado lo escala a divisas, el único tipo activo
ORO = "¿Qué opinas del oro frente a la plata a 6 meses?"
CORREO = "ana.garcia.t169@ejemplo.com"
DESPUES = "2026-06-12"


def _bloque_div(tmp_path, universo):
    return nuevo_bloque(tmp_path, universo, cfg=cargar_config(extra={"modo": "backtest"}))


def _espiar(b) -> list[dict]:
    vistos: list[dict] = []
    crear = b.mensajeria.crear

    def crear_y_anotar(*args, **kwargs):
        msg = crear(*args, **kwargs)
        vistos.append(copy.deepcopy(msg))
        return msg

    b.mensajeria.crear = crear_y_anotar
    return vistos


def _ct03_retornos(mensajes: list[dict], qry_id: str | None = None) -> list[dict]:
    return [m for m in mensajes if m["contrato"] == "CT-03" and m["tipo_mensaje"] == "RETORNO"
            and (qry_id is None or m.get("query_id") == qry_id)]


def _qry(b, qry_id: str | None = None) -> list[dict]:
    return [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "QRY" and (qry_id is None or e["id"] == qry_id)]


def _finales(b, qry_id: str) -> list[dict]:
    return [e for e in _qry(b, qry_id) if e.get("respuesta_final")]


def _sin_final(monkeypatch, b, texto, **kw):
    """Una consulta cuya final no sale (como si el proceso muriera justo después de la provisional)."""
    real = respuesta_final.enviar
    monkeypatch.setattr(respuesta_final, "enviar", lambda *a, **k: None)
    q = b.consulta(texto, as_of=AS_OF, **kw)
    monkeypatch.setattr(respuesta_final, "enviar", real)
    assert q["respuesta_final"] is None and not _finales(b, q["query_id"])
    return q


def _cuerpo(final: dict) -> dict:
    return {k: v for k, v in final.items() if k not in ("msg_id", "timestamp", "repetido")}


# ================================================================ H-01 · integridad y controles paran la consulta
def test_h01_un_fallo_de_integridad_para_la_consulta_como_en_la_base(tmp_path, universo):
    """La sonda del bloque 4 de `r01_02_procesos_y_base.py`: sello de F2 manipulado con el bloque abierto. La consulta lee F1–F6
    sin notarlo y el primer `escribir` de F2, dentro del RUN-, falla la integridad: se para como en la base (f2b3ad4)."""
    b = _bloque_div(tmp_path, universo)
    ruta = b.almacen._ruta_sellos
    sellos = json.loads(ruta.read_text(encoding="utf-8"))
    sellos["F2"] = [999, "0" * 64]
    ruta.write_text(json.dumps(sellos), encoding="utf-8")
    mensajes = _espiar(b)
    with pytest.raises(ValueError, match="Fallo de integridad en el sello de F2"):
        b.consulta(DIV, as_of=AS_OF)
    assert not _ct03_retornos(mensajes) and not _qry(b)                        # ni provisional ni final ni QRY en F5
    assert not [e for e in b.almacen.leer("HA") if e.get("tipo") == "HERRAMIENTA"]


@pytest.mark.parametrize("error", [EscrituraFueraDeReserva("x"), PronosticoCongelado("x"), CanalNoPrevisto("x"),
                                   DatosSensibles("x"), MensajeInvalido("x"), FugaDeInformacion("x")],
                         ids=lambda e: type(e).__name__)
def test_h01_un_error_de_control_del_run_se_relanza(tmp_path, universo, monkeypatch, error):
    b = _bloque_div(tmp_path, universo)
    mensajes = _espiar(b)

    def ciclo(*a, **k):
        raise error

    monkeypatch.setattr(b, "ciclo", ciclo)
    with pytest.raises(type(error)):
        b.consulta(DIV, as_of=AS_OF)
    assert not _ct03_retornos(mensajes) and not _qry(b)
    assert not [e for e in b.almacen.leer("HA") if e.get("tipo") == "HERRAMIENTA"]


def test_h01_un_error_corriente_tras_registrar_el_run_sigue_dando_fallido(tmp_path, universo):
    """Un fallo del análisis con el almacén íntegro (la auditoría, tras registrar y entregar el RUN-) sigue dando la final
    FALLIDO, que cita el RUN- registrado (mata M07: sin buscarlo, no habría RUN-)."""
    b = _bloque_div(tmp_path, universo)

    def auditar(*a, **k):
        raise KeyError("fallo interno")

    b._auditar = auditar
    q = b.consulta(DIV, as_of=AS_OF)
    run_id = q["escalado"]["run_id"]
    assert run_id and q["escalado"]["estado_run"] == "FALLIDO"
    assert b.almacen.estado("F5", clave="id")[run_id]["disparador"]["qry_id"] == q["query_id"]
    fin = q["respuesta_final"]
    assert fin["respuesta_final"]["resultado_analisis"] == "FALLIDO" and fin["referencias"] == [run_id] and fin["run_id"] == run_id
    assert any("KeyError" in x for x in fin["limitaciones"]) and "fallo interno" not in json.dumps(fin, ensure_ascii=False)
    assert b.almacen.estado("F5", clave="id")[q["query_id"]]["fallo_analisis"] == "KeyError"


# ================================================================ H-02 · la provisional en F5 y las finales pendientes
def test_h02_la_provisional_queda_en_f5(tmp_path, universo):
    b = _bloque_div(tmp_path, universo)
    q = b.consulta(ORO, as_of=AS_OF, ejecutar_escalado=False)
    qry = _qry(b, q["query_id"])
    assert len(qry) == 3 and qry[1]["provisional_msg_id"] == q["msg_id"] and "fallo_analisis" not in qry[1]
    assert not any("tema_normalizado" in e for e in qry[1:])
    assert q["respuesta_final"]["respuesta_final"]["provisional_msg_id"] == q["msg_id"]


def test_h02_enviar_rechaza_una_provisional_inventada_o_sin_registrar(tmp_path, universo, monkeypatch):
    b = _bloque_div(tmp_path, universo)
    mensajes = _espiar(b)
    q = _sin_final(monkeypatch, b, ORO, ejecutar_escalado=False)
    n_msg, n_f5 = len(mensajes), len(b.almacen.leer("F5"))
    with pytest.raises(respuesta_final.RespuestaFinalInvalida, match="no es la provisional registrada"):
        respuesta_final.enviar(b, q["query_id"], "MSG-2026-999999", AS_OF)
    assert len(mensajes) == n_msg and len(b.almacen.leer("F5")) == n_f5
    fin = respuesta_final.enviar(b, q["query_id"], None, AS_OF)                      # None: la de F5
    assert fin["respuesta_final"]["provisional_msg_id"] == q["msg_id"] and fin["repetido"] is False
    with pytest.raises(respuesta_final.RespuestaFinalInvalida, match="otra provisional"):
        respuesta_final.enviar(b, q["query_id"], "MSG-2026-999999", AS_OF)
    assert respuesta_final.enviar(b, q["query_id"], q["msg_id"], AS_OF)["repetido"] is True
    # una consulta escalada sin la provisional registrada (estado de antes de T-169 o manipulado): no hay final que enlazar
    monkeypatch.setattr(respuesta_final, "registrar_provisional", lambda *a, **k: None)
    q2 = _sin_final(monkeypatch, b, ORO, ejecutar_escalado=False)
    with pytest.raises(respuesta_final.RespuestaFinalInvalida, match="no tiene registrada"):
        respuesta_final.enviar(b, q2["query_id"], q2["msg_id"], AS_OF)
    assert not _finales(b, q2["query_id"]) and q2["query_id"] not in [x for x, _ in respuesta_final.pendientes(b.almacen)]


def test_h02_la_siguiente_consulta_envia_la_final_pendiente(tmp_path, universo, monkeypatch):
    b = _bloque_div(tmp_path, universo)
    q1 = _sin_final(monkeypatch, b, ORO, ejecutar_escalado=False)
    assert respuesta_final.pendientes(b.almacen) == [(q1["query_id"], AS_OF)]
    mensajes = _espiar(b)
    q2 = b.consulta(ORO, as_of=AS_OF, ejecutar_escalado=False)
    pendiente, prov2, fin2 = _ct03_retornos(mensajes)
    assert pendiente["query_id"] == q1["query_id"] and pendiente["respuesta_final"]["provisional_msg_id"] == q1["msg_id"]
    assert mensajes.index(pendiente) < mensajes.index(next(m for m in mensajes if m["contrato"] == "CT-03"
                                                           and m["tipo_mensaje"] == "ENCARGO"))   # antes de atender la nueva
    assert (prov2["msg_id"], fin2["query_id"]) == (q2["msg_id"], q2["query_id"])
    assert len(_finales(b, q1["query_id"])) == 1 and len(_finales(b, q2["query_id"])) == 1
    assert respuesta_final.pendientes(b.almacen) == []
    b.consulta(ORO, as_of=AS_OF, ejecutar_escalado=False)                         # una tercera no la repite
    assert len(_ct03_retornos(mensajes, q1["query_id"])) == 1


def test_h02_el_siguiente_ciclo_envia_la_final_pendiente(tmp_path, universo, monkeypatch):
    b = _bloque_div(tmp_path, universo)
    q1 = _sin_final(monkeypatch, b, ORO, ejecutar_escalado=False)
    mensajes = _espiar(b)
    b.ciclo(DESPUES)
    finales = _ct03_retornos(mensajes, q1["query_id"])
    assert len(finales) == 1 and finales[0]["respuesta_final"]["provisional_msg_id"] == q1["msg_id"]
    assert mensajes.index(finales[0]) < mensajes.index(next(m for m in mensajes if m["contrato"] == "CT-05"))
    assert respuesta_final.enviar_pendientes(b, DESPUES) == [] and len(_finales(b, q1["query_id"])) == 1


def test_h02_un_bloque_reabierto_envia_la_final_pendiente(tmp_path, universo, monkeypatch):
    b = _bloque_div(tmp_path, universo)
    q1 = _sin_final(monkeypatch, b, ORO, ejecutar_escalado=False)
    del b
    b2 = _bloque_div(tmp_path, universo)                                           # el mismo almacén, otra instancia
    assert respuesta_final.pendientes(b2.almacen) == [(q1["query_id"], AS_OF)]
    mensajes = _espiar(b2)
    q2 = b2.consulta(ORO, as_of=AS_OF, ejecutar_escalado=False)
    finales = _ct03_retornos(mensajes, q1["query_id"])
    assert len(finales) == 1 and finales[0]["respuesta_final"]["provisional_msg_id"] == q1["msg_id"]
    assert finales[0]["msg_id"] not in (q1["msg_id"], q2["msg_id"]) and all(b2.almacen.verificar_integridad().values())


def test_h02_la_final_recuperada_es_la_que_habria_salido(tmp_path, universo, monkeypatch):
    """La misma consulta (su RUN- falla) en dos almacenes: en uno la final sale en la consulta; en el otro queda pendiente y la
    envía una semana después `enviar_pendientes`, con la fecha de la consulta y la clase del fallo guardada en F5."""
    def falla(*a, **k):
        raise RuntimeError("detalle")

    directa = _bloque_div(tmp_path / "directa", universo)
    monkeypatch.setattr(directa, "ciclo", falla)
    esperada = directa.consulta(DIV, as_of=AS_OF)["respuesta_final"]
    tarde = _bloque_div(tmp_path / "tarde", universo)
    monkeypatch.setattr(tarde, "ciclo", falla)
    q = _sin_final(monkeypatch, tarde, DIV)
    tarde.fijar_fecha(DESPUES)
    enviadas = respuesta_final.enviar_pendientes(tarde, DESPUES)
    assert len(enviadas) == 1 and _cuerpo(enviadas[0]) == _cuerpo(esperada)
    assert any("RuntimeError" in x for x in enviadas[0]["limitaciones"]) and enviadas[0]["estado"] == "SIN_RESULTADO"
    assert enviadas[0]["msg_id"] == esperada["msg_id"] and enviadas[0]["timestamp"] != esperada["timestamp"]
    assert respuesta_final.registrada(tarde.almacen, q["query_id"]) == {k: v for k, v in enviadas[0].items() if k != "repetido"}



def test_h02_la_pendiente_se_construye_con_la_fecha_de_su_consulta(tmp_path, universo, monkeypatch):
    """Lo que cambia en F5 después de la consulta (aquí, el RUN- marcado bloqueado una semana después) no entra en la final
    pendiente: se construye con la fecha de la QRY-, no con la del día en que sale (mata N08)."""
    b = _bloque_div(tmp_path, universo)
    q = _sin_final(monkeypatch, b, DIV)
    run_id = q["escalado"]["run_id"]
    qry = b.almacen.estado("F5", AS_OF, clave="id")[q["query_id"]]
    esperado, _, _, _ = respuesta_final.construir(b.almacen, qry, q["msg_id"], AS_OF)
    assert esperado["respuesta_final"]["resultado_analisis"].startswith("ENTREGADO")
    b.fijar_fecha(DESPUES)
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "RUN", "id": run_id, "entrega": "BLOQUEADA"})
    enviadas = respuesta_final.enviar_pendientes(b, DESPUES)
    assert len(enviadas) == 1 and {k: enviadas[0][k] for k in esperado} == esperado

def _construir_rechazado(monkeypatch, qry_id, error=None):
    """`construir` que, solo para `qry_id`, añade un correo (R8) o lanza `error`."""
    real = respuesta_final.construir

    def construir(almacen, qry, *a, **k):
        cuerpo, run_id, estado, desc = real(almacen, qry, *a, **k)
        if qry.get("id") == qry_id:
            if error is not None:
                raise error
            cuerpo = {**cuerpo, "limitaciones": [*cuerpo["limitaciones"], f"Contacto {CORREO}"]}
        return cuerpo, run_id, estado, desc

    monkeypatch.setattr(respuesta_final, "construir", construir)


def test_h02_una_pendiente_que_la_mensajeria_rechaza_se_aparta_una_vez(tmp_path, universo, monkeypatch):
    b = _bloque_div(tmp_path, universo)
    q1 = _sin_final(monkeypatch, b, ORO, ejecutar_escalado=False)
    _construir_rechazado(monkeypatch, q1["query_id"])
    mensajes = _espiar(b)
    q2 = b.consulta(ORO, as_of=AS_OF, ejecutar_escalado=False)                     # no se para: atiende la nueva
    assert not _ct03_retornos(mensajes, q1["query_id"]) and len(_ct03_retornos(mensajes, q2["query_id"])) == 2
    marca = [e for e in _qry(b, q1["query_id"]) if e.get("final_no_enviable")]
    assert len(marca) == 1 and marca[0]["final_no_enviable"] == {"error": "DatosSensibles"} and not _finales(b, q1["query_id"])
    inc = [e for e in b.almacen.leer("HA") if q1["query_id"] in e.get("detalle", "")]
    assert len(inc) == 1 and inc[0]["escalado_operador"] is True and "apartada" in inc[0]["detalle"]
    ha = json.dumps(b.almacen.leer("HA"), ensure_ascii=False)
    assert CORREO not in ha and any(e.get("tipo") == "SEGURIDAD" for e in b.almacen.leer("HA"))
    n_ha = len(b.almacen.leer("HA"))
    b.consulta(ORO, as_of=AS_OF, ejecutar_escalado=False)                         # no se reintenta sola
    assert len(b.almacen.leer("HA")) == n_ha and respuesta_final.pendientes(b.almacen) == []
    monkeypatch.undo()                                                             # corregido el estado, el operador la reenvía
    fin = respuesta_final.enviar(b, q1["query_id"], None, AS_OF)
    assert fin["repetido"] is False and fin["respuesta_final"]["provisional_msg_id"] == q1["msg_id"]


def test_h02_un_error_de_control_en_una_pendiente_para_la_consulta_y_no_aparta(tmp_path, universo, monkeypatch):
    """r02 (H-01 de la QA r01 de T-169): un error corriente se aparta (`test_t169_r02.py`); uno de control para, como en H-01."""
    b = _bloque_div(tmp_path, universo)
    q1 = _sin_final(monkeypatch, b, ORO, ejecutar_escalado=False)
    _construir_rechazado(monkeypatch, q1["query_id"], EscrituraFueraDeReserva("x"))
    with pytest.raises(EscrituraFueraDeReserva):
        b.consulta(ORO, as_of=AS_OF, ejecutar_escalado=False)
    assert respuesta_final.pendientes(b.almacen) == [(q1["query_id"], AS_OF)]
    # nada apartado, y la consulta nueva no llegó a empezar: en F5 solo la provisional y su registro, de la primera
    assert not [e for e in _qry(b, q1["query_id"]) if e.get("final_no_enviable")] and len(_qry(b)) == 2


# ================================================================ H-03 y H-04 · sobre un RUN- con opciones entregadas
@pytest.fixture(scope="module")
def dos_runs(tmp_path_factory, universo):
    """Un ciclo de RV (RUN-1) y la consulta de PB-07, que escala a RV (RUN-2): las mismas opciones salen en los dos."""
    b = nuevo_bloque(tmp_path_factory.mktemp("t169"), universo)
    r1 = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    q = b.consulta(PB07, as_of=AS_OF)
    return b, r1, q


def _construir_con(b, q, monkeypatch, f5=None, f3=None):
    """`construir` con la vista consolidada de F5 o de F3 retocada; no escribe nada en el almacén."""
    qry = b.almacen.estado("F5", AS_OF, clave="id")[q["query_id"]]
    real = b.almacen.estado

    def estado(archivo, as_of=None, clave=None, **k):
        out = real(archivo, as_of, clave, **k)
        if archivo == "F5" and f5:
            f5(out)
        if archivo == "F3" and f3:
            f3(out)
        return out

    monkeypatch.setattr(b.almacen, "estado", estado)
    try:
        return respuesta_final.construir(b.almacen, qry, q["msg_id"], AS_OF)
    finally:
        monkeypatch.setattr(b.almacen, "estado", real)


def _top(b, q):
    return [o for lst in b.almacen.estado("F5", clave="id")[q["escalado"]["run_id"]]["top3_por_clase"].values() for o in lst]


@pytest.mark.parametrize("ajeno", ["RUN-2026-0001", "HIT-2026-0001", "PRG-2026-0001"])   # existen, pero no son CLM-
def test_h03_un_id_de_otro_tipo_en_las_evidencias_no_se_cita(dos_runs, monkeypatch, ajeno):
    b, r1, q = dos_runs
    top = _top(b, q)
    assert r1["run_id"] == "RUN-2026-0001"

    def f3(out):
        out[top[0]]["evidencias"] = [*out[top[0]]["evidencias"], ajeno]

    cuerpo, _, estado, descartadas = _construir_con(b, q, monkeypatch, f3=f3)
    respuesta_final.validar(cuerpo, estado)                                         # un HIT- ya no tumba la final
    assert ajeno not in cuerpo["referencias"] and ajeno in descartadas
    assert [r for r in cuerpo["referencias"] if r.startswith("RUN-")] == [q["escalado"]["run_id"]]


def test_h03_un_id_de_otro_tipo_en_las_tendencias_no_se_cita(dos_runs, monkeypatch):
    b, _, q = dos_runs
    top = _top(b, q)
    clm = b.almacen.estado("F3")[top[1]]["evidencias"][0]                          # un CLM- que existe, de otra opción

    def f3(out):
        out[top[0]]["tnd_ids"] = [*out[top[0]]["tnd_ids"], clm, "PRG-2026-0001"]
        out[top[0]]["evidencias"] = []
        out[top[1]]["evidencias"] = []

    cuerpo, _, estado, descartadas = _construir_con(b, q, monkeypatch, f3=f3)
    respuesta_final.validar(cuerpo, estado)
    assert clm not in cuerpo["referencias"] and "PRG-2026-0001" not in cuerpo["referencias"]
    assert {clm, "PRG-2026-0001"} <= set(descartadas)


def test_h03_un_run_que_no_lanzo_la_consulta_no_se_cita(tmp_path, universo, monkeypatch):
    """La sonda s10 de `r01_01_sondas.py`: una QRY- cuyo `escalado` apunta al RUN- que lanzó otra consulta."""
    b = _bloque_div(tmp_path, universo)
    q1 = b.consulta(DIV, as_of=AS_OF)
    run1 = q1["escalado"]["run_id"]
    q2 = _sin_final(monkeypatch, b, ORO, ejecutar_escalado=False)
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "QRY", "id": q2["query_id"],
                                       "escalado": {**q2["escalado"], "run_id": run1, "estado_run": "COMPLETO"}})
    fin = respuesta_final.enviar(b, q2["query_id"], None, AS_OF)
    assert fin["respuesta_final"]["resultado_analisis"] == "SIN_ENTREGA" and fin["estado"] == "SIN_RESULTADO"
    assert fin["referencias"] == [] and fin["run_id"] is None and "no lo lanzó esta consulta" in fin["respuesta"]
    assert "OPP-" not in json.dumps(fin)


def test_h04_la_confianza_es_la_mas_baja_de_las_citadas(dos_runs, monkeypatch):
    """Mata M01 (la más alta en vez de la más baja): en el escenario nominal las tres opciones tienen la misma."""
    b, _, q = dos_runs
    top = _top(b, q)
    for valores, esperada in ((["establecido", "probable", "establecido"], "probable"),
                              (["probable", "establecido", "en disputa"], "en disputa"),
                              (["establecido", "establecido", "especulativo"], "especulativo")):
        def f3(out, _v=valores):
            for o, v in zip(top, _v):
                out[o]["confianza"] = v

        cuerpo, _, _, _ = _construir_con(b, q, monkeypatch, f3=f3)
        assert cuerpo["confianza"] == esperada, valores


@pytest.mark.parametrize("valor", ["alta", None, 3])
def test_h04_una_confianza_no_valida_cuenta_como_especulativo(dos_runs, monkeypatch, valor):
    """Mata M16 (una confianza no válida en F3 contaría como «establecido»)."""
    b, _, q = dos_runs
    top = _top(b, q)

    def f3(out):
        for o in top:
            out[o]["confianza"] = "establecido"
        out[top[-1]]["confianza"] = valor

    cuerpo, _, _, _ = _construir_con(b, q, monkeypatch, f3=f3)
    assert cuerpo["confianza"] == "especulativo" and f"{top[-1]} " in cuerpo["respuesta"]
    assert "(confianza especulativo)" in cuerpo["respuesta"].split(top[-1])[1]


def test_h04_los_prg_son_solo_los_de_su_run(dos_runs):
    """Mata M02 (PRG- de cualquier RUN- de la opción): el RUN- anterior dejó PRG- de las mismas opciones, que no se citan."""
    b, r1, q = dos_runs
    run2 = q["escalado"]["run_id"]
    top = _top(b, q)
    altas = [e for e in b.almacen.leer("F4") if e.get("tipo_entrada") == "ALTA" and str(e.get("prg_id")).startswith("PRG-")]
    del_anterior = {e["prg_id"] for e in altas if e.get("run_id") == r1["run_id"] and e.get("opp_id") in top}
    assert del_anterior                                                            # la prueba tiene sentido
    citados = {r for r in q["respuesta_final"]["referencias"] if r.startswith("PRG-")}
    assert citados == {e["prg_id"] for e in altas if e.get("run_id") == run2 and e.get("opp_id") in top}
    assert not citados & del_anterior


def test_h04_un_run_parcial_da_entregado_parcial(dos_runs, monkeypatch):
    """Mata M11 (ENTREGADO_PARCIAL con estado COMPLETO) y M12 (un RUN- PARCIAL se da por completo)."""
    b, _, q = dos_runs
    run2 = q["escalado"]["run_id"]

    def f5(out):
        out[run2]["estado"] = "PARCIAL"

    cuerpo, run_id, estado, _ = _construir_con(b, q, monkeypatch, f5=f5)
    assert cuerpo["respuesta_final"]["resultado_analisis"] == "ENTREGADO_PARCIAL" and estado == "PARCIAL" and run_id == run2
    assert "con alcance parcial" in cuerpo["respuesta"] and "terminado completo" not in cuerpo["respuesta"]
    respuesta_final.validar(cuerpo, estado)
    with pytest.raises(respuesta_final.RespuestaFinalInvalida):
        respuesta_final.validar(cuerpo, "COMPLETO")
