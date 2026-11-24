"""T-198 · PB-46: el Buscador de Fuentes Avanzadas (AG-16) atiende el CT-19 FIABILIDAD_FUENTES del Evaluador.

Hasta T-198 el CT-19 se creaba COMPLETO y nadie lo atendía (QA r01 de T-159, H-02): no había en F9 dónde escribir. Ahora la
fiabilidad medida de cada FUE- queda en F9 de la instancia (almacén, propietario AG-16), comprobada contra F6 y F9 antes de
escribir, sin duplicados, con reintento, y el Buscador la ve en sus búsquedas (CT-07). La recalificación de Q, el nivel y el
orden de F9 siguen siendo del modelo real (INC-T198-01).
"""
import copy
import json
import threading
import types

import pytest
from bloque_a.almacen import ARCHIVOS, Almacen, EscrituraFueraDeReserva, Reloj
from bloque_a.configuracion import cargar_config, parametro
from bloque_a.fiabilidad_f9 import CAMPOS_CT19, FiabilidadNoAtendible
from conftest import AS_OF, config_pruebas, nuevo_bloque
from test_t125_fiabilidad_fuentes import _escribir_clm, _sembrar

from bloque_a import fiabilidad_f9, mock_respuestas

FUENTE_A, FUENTE_B = "REF-RF-0001", "REF-RF-0003"     # fuentes de F9 (corpus)


def _bloque(tmp_path, universo, cfg=None):
    b = nuevo_bloque(tmp_path, universo, cfg=cfg)
    b.fijar_fecha(AS_OF)
    return b


def _f9(b, as_of=None):
    return [e for e in b.almacen.leer("F9", as_of) if e.get("tipo_entrada") == "FIABILIDAD_MEDIDA"]


def _ct19_al_buscador(b):
    return [m for m in b.mensajeria.registro if m["contrato"] == "CT-19" and m["receptor"] == "AG-16"]


def _dos_fuentes(b):
    """El caso del plan: dos fuentes de 25 pronósticos explícitos, una con habilidad y otra sin ella."""
    _sembrar(b, FUENTE_A, 20, 5)
    _sembrar(b, FUENTE_B, 13, 12, inicio_id=101)


def _msg_comunicado(b, fues):
    """Un CT-19 como el del ciclo, con su `comunicado_ct19` anotado en F6, sin atenderlo."""
    msg = b.mensajeria.crear("CT-19", "AG-20", "AG-16", fiabilidad_f9.cuerpo_ct19(fues), run_id="RUN-2026-0001",
                             tipo_mensaje="RETORNO", estado="COMPLETO")
    for f in fues:
        b.almacen.escribir("F6", "AG-20", {"tipo_entrada": "FUE", "id": f["fue_id"], "comunicado_ct19": msg["msg_id"]})
    return msg


# ---------------------------------------------------------------- CA-1 · el CT-19 se atiende y deja la fiabilidad en F9
def test_ca1_las_dos_fuentes_del_plan_quedan_en_f9_con_su_fiabilidad_medida(tmp_path, universo):
    b = _bloque(tmp_path, universo, cfg=config_pruebas())
    _dos_fuentes(b)
    # uno de FUENTE_A registrado y sin vencer: cuenta como registrado, no como resuelto
    _escribir_clm(b, {"tipo_entrada": "CLM", "clm_id": "CLM-2026-0500", "afirmacion": "sin vencer", "tipo_afirmacion": "PRONOSTICO_FUENTE",
                      "evidencias": [], "pronostico_fuente": {"ref_id": FUENTE_A, "variable": "cierre", "serie_ht01": "SPY",
                      "fecha_objetivo": "2026-12-31", "umbral_o_rango": 1.0, "direccion": "por_encima", "probabilidad": 0.7,
                      "fecha_emision": "2026-06-01"}}, "2026-06-01")
    # r02 (H-05): un bloque pronostico_fuente en una afirmación que no es PRONOSTICO_FUENTE no cuenta como registrado
    _escribir_clm(b, {"tipo_entrada": "CLM", "clm_id": "CLM-2026-0501", "afirmacion": "otra", "tipo_afirmacion": "PREVISION",
                      "evidencias": [], "pronostico_fuente": {"ref_id": FUENTE_A, "fecha_objetivo": "2026-12-31"}}, "2026-06-01")
    # r02 (H-04): uno registrado después de as_of no cuenta (sin fuga)
    _escribir_clm(b, {"tipo_entrada": "CLM", "clm_id": "CLM-2026-0502", "afirmacion": "después", "tipo_afirmacion": "PRONOSTICO_FUENTE",
                      "evidencias": [], "pronostico_fuente": {"ref_id": FUENTE_A, "variable": "cierre", "serie_ht01": "SPY",
                      "fecha_objetivo": "2026-12-31", "umbral_o_rango": 2.0, "direccion": "por_encima", "probabilidad": 0.7,
                      "fecha_emision": "2026-06-10"}}, "2026-06-10")
    q_corpus = {r: b.referencias.por_id(r)["q"] for r in (FUENTE_A, FUENTE_B)}
    fue = {f["ref_id"]: f for f in b.evaluador.fiabilidad_fuentes(AS_OF, "RUN-2026-0001")}
    atendidas = b._comunicar_fiabilidad(b.reloj.fecha, "RUN-2026-0001")
    msg = _ct19_al_buscador(b)
    assert len(msg) == 1 and sorted(atendidas) == sorted(f["fue_id"] for f in fue.values())
    f6 = b.almacen.estado("F6", clave="id")
    f9 = {e["ref_id"]: e for e in _f9(b)}
    assert set(f9) == {FUENTE_A, FUENTE_B}
    for ref_id, e in f9.items():
        f = fue[ref_id]
        assert e["_autor"] == "AG-16" and e["fue_id"] == f["fue_id"] and e["recibido_via"] == msg[0]["msg_id"]
        assert f6[f["fue_id"]]["comunicado_ct19"] == msg[0]["msg_id"]
        assert (e["resueltos"], e["aciertos"], e["bss"], e["bss_contraido"], e["puntos_historial"]) == (
            f["n"], f["aciertos"], f["bss"], f["bss_contraido"], f["puntos_historial"])
        assert e["calc_id"] == f["calc_id"] and e["calc_id"] and e["periodo"] == AS_OF[:7]
        assert e["metrica"] == f6[f["fue_id"]]["metodo"] and e["metrica"]                     # r02 (H-05)
        assert e["id"].startswith("FMD-")                                                       # r02 (H-06)
        assert e["pronosticos_registrados"] == (26 if ref_id == FUENTE_A else 25) and e["resueltos"] == 25 and e["ventana_meses"] == parametro(b.cfg, "fiabilidad_fuentes.ventana_meses")
        assert e["fecha_ct19"] == AS_OF and e["run_id"] == "RUN-2026-0001" and e["recalificacion_q"] == "PENDIENTE"
    neutro = parametro(b.cfg, "fiabilidad_fuentes.puntos_neutro")
    assert f9[FUENTE_A]["puntos_historial"] > neutro > f9[FUENTE_B]["puntos_historial"]
    # la Q de las fichas del corpus no cambia: recalcularla es del Buscador con el modelo real (INC-T198-01)
    assert {r: b.referencias.por_id(r)["q"] for r in q_corpus} == q_corpus


def test_ca1_con_la_configuracion_por_defecto_tal_cual(tmp_path, universo):
    b = _bloque(tmp_path, universo, cfg=cargar_config())
    _sembrar(b, FUENTE_A, 20, 5)
    fue = b.evaluador.fiabilidad_fuentes(AS_OF, "RUN-2026-0001")
    assert len(fue) == 1
    assert b._comunicar_fiabilidad(b.reloj.fecha, "RUN-2026-0001") == [fue[0]["fue_id"]]
    assert [e["ref_id"] for e in _f9(b)] == [FUENTE_A]


def test_ca1_en_un_ciclo_el_buscador_atiende_el_ct19(tmp_path, universo):
    b = _bloque(tmp_path, universo, cfg=config_pruebas())
    _sembrar(b, FUENTE_A, 20, 5)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    fue = r["evaluacion"]["fiabilidad_fuentes"]
    msg = _ct19_al_buscador(b)
    f9 = _f9(b)
    assert len(fue) == 1 and len(msg) == 1 and len(f9) == 1
    assert f9[0]["fue_id"] == fue[0]["fue_id"] and f9[0]["recibido_via"] == msg[0]["msg_id"] and f9[0]["run_id"] == r["run_id"]
    assert not [e for e in b.almacen.leer("HA") if "no atendido por el Buscador" in str(e.get("detalle"))]


# ---------------------------------------------------------------- CA-2 · falla cerrado: si algo no cuadra, nada en F9
def _caso_dos(tmp_path, universo):
    b = _bloque(tmp_path, universo, cfg=config_pruebas())
    _dos_fuentes(b)
    fues = b.evaluador.fiabilidad_fuentes(AS_OF, "RUN-2026-0001")
    return b, fues, _msg_comunicado(b, fues)


def _otro(msg, **cambios):
    m = copy.deepcopy(msg)
    m.update(cambios)
    return m


def _fuente_cambiada(msg, i, **cambios):
    m = copy.deepcopy(msg)
    m["fuentes"][i].update(cambios)
    return m


def test_ca2_un_ct19_que_no_cuadra_no_escribe_nada_en_f9(tmp_path, universo):
    b, fues, msg = _caso_dos(tmp_path, universo)
    fuera_de_f9 = "REF-FM-0001" if b.referencias.por_id("REF-FM-0001") else "REF-0001"
    malos = {
        "otro emisor": _otro(msg, emisor="AG-02"), "otro receptor": _otro(msg, receptor="AG-18"),
        "otro contrato": _otro(msg, contrato="CT-21"), "otro tipo": _otro(msg, tipo="PROPUESTA_TIPO_3"),
        "sin msg_id": _otro(msg, msg_id=""), "sin fuentes": _otro(msg, fuentes=[]), "fuentes no lista": _otro(msg, fuentes={}),
        "no es objeto": None,
        # la primera fuente cuadra; la segunda no: tampoco se escribe la primera
        "puntos distintos de F6": _fuente_cambiada(msg, 1, puntos_historial=19.0),
        "n distinto de F6": _fuente_cambiada(msg, 1, n=99),
        "fue_id que no está en F6": _fuente_cambiada(msg, 1, fue_id="FUE-2026-9999"),
        "ref_id distinto de F6": _fuente_cambiada(msg, 1, ref_id=FUENTE_A),
        "campo de más": _fuente_cambiada(msg, 1, q=95),
        "fue_id repetido": _otro(msg, fuentes=[msg["fuentes"][0], msg["fuentes"][0]]),
        "fuente sin un campo": _otro(msg, fuentes=[msg["fuentes"][0], {k: v for k, v in msg["fuentes"][1].items() if k != "bss"}]),
        "F6 anota otro CT-19": _otro(msg, msg_id="MSG-2026-999999"),
    }
    for motivo, m in malos.items():
        with pytest.raises(FiabilidadNoAtendible):
            fiabilidad_f9.atender_ct19(b, m, b.reloj.fecha, "RUN-2026-0001")
        assert _f9(b) == [], motivo
    # una FUE- cuya fuente no es de F9 (escrita a mano: el Evaluador ya no la contaría)
    b.almacen.escribir("F6", "AG-20", {"tipo_entrada": "FUE", "id": fues[1]["fue_id"], "ref_id": fuera_de_f9})
    with pytest.raises(FiabilidadNoAtendible, match="no es una fuente de F9"):
        fiabilidad_f9.atender_ct19(b, _fuente_cambiada(msg, 1, ref_id=fuera_de_f9), b.reloj.fecha, "RUN-2026-0001")
    assert _f9(b) == []


def test_ca2_un_ct19_sin_msg_id_no_se_atiende_aunque_f6_no_anote_ninguno(tmp_path, universo):
    """Una FUE- recién escrita tiene `comunicado_ct19` None: un mensaje sin msg_id no puede pasar por el suyo."""
    b = _bloque(tmp_path, universo, cfg=config_pruebas())
    _sembrar(b, FUENTE_A, 20, 5)
    fues = b.evaluador.fiabilidad_fuentes(AS_OF, "RUN-2026-0001")
    msg = {"contrato": "CT-19", "emisor": "AG-20", "receptor": "AG-16", "msg_id": None, **fiabilidad_f9.cuerpo_ct19(fues)}
    with pytest.raises(FiabilidadNoAtendible, match="msg_id"):
        fiabilidad_f9.atender_ct19(b, msg, b.reloj.fecha, "RUN-2026-0001")
    assert _f9(b) == []


def test_ca2_el_ct19_bueno_si_se_atiende(tmp_path, universo):
    b, fues, msg = _caso_dos(tmp_path, universo)
    assert sorted(fiabilidad_f9.atender_ct19(b, msg, b.reloj.fecha, "RUN-2026-0001")) == sorted(f["fue_id"] for f in fues)
    assert len(_f9(b)) == 2


def test_ca2_en_el_ciclo_queda_una_incidencia_y_se_reintenta_en_el_siguiente(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo, cfg=config_pruebas())
    _sembrar(b, FUENTE_A, 20, 5)
    b.evaluador.fiabilidad_fuentes(AS_OF, "RUN-2026-0001")
    original = fiabilidad_f9.comprobar_ct19

    def no_cuadra(msg, f6, referencias, as_of=None):
        raise FiabilidadNoAtendible("prueba")
    monkeypatch.setattr(fiabilidad_f9, "comprobar_ct19", no_cuadra)
    assert b._comunicar_fiabilidad(b.reloj.fecha, "RUN-2026-0001") == []
    assert _f9(b) == []
    inc = [e for e in b.almacen.leer("HA") if "no atendido por el Buscador" in str(e.get("detalle"))]
    assert len(inc) == 1 and inc[0]["objeto"] == "AG-16" and inc[0]["run_id"] == "RUN-2026-0001"
    monkeypatch.setattr(fiabilidad_f9, "comprobar_ct19", original)
    assert len(b._comunicar_fiabilidad(b.reloj.fecha, "RUN-2026-0002")) == 1
    msgs = _ct19_al_buscador(b)
    assert len(msgs) == 2 and _f9(b)[0]["recibido_via"] == msgs[1]["msg_id"] and _f9(b)[0]["run_id"] == "RUN-2026-0002"


def test_ca2_un_error_del_almacen_no_se_traga(tmp_path, universo, monkeypatch):
    """Solo se captura `FiabilidadNoAtendible`: un fallo de escritura del almacén sale del ciclo (falla cerrado)."""
    b = _bloque(tmp_path, universo, cfg=config_pruebas())
    _sembrar(b, FUENTE_A, 20, 5)
    b.evaluador.fiabilidad_fuentes(AS_OF, "RUN-2026-0001")
    escribir = b.almacen.escribir

    def roto(archivo, autor, entrada):
        if archivo == "F9":
            raise OSError("disco")
        return escribir(archivo, autor, entrada)
    monkeypatch.setattr(b.almacen, "escribir", roto)
    with pytest.raises(OSError):
        b._comunicar_fiabilidad(b.reloj.fecha, "RUN-2026-0001")


# ---------------------------------------------------------------- CA-3 · sin duplicados, también entre procesos
def test_ca3_atender_dos_veces_no_duplica_y_el_ciclo_siguiente_no_reenvia(tmp_path, universo):
    b, _, msg = _caso_dos(tmp_path, universo)
    assert len(fiabilidad_f9.atender_ct19(b, msg, b.reloj.fecha, "RUN-2026-0001")) == 2
    assert fiabilidad_f9.atender_ct19(b, msg, b.reloj.fecha, "RUN-2026-0001") == []
    assert len(_f9(b)) == 2
    assert b._comunicar_fiabilidad(b.reloj.fecha, "RUN-2026-0002") == [] and len(_ct19_al_buscador(b)) == 1


def test_ca3_dos_instancias_a_la_vez_dejan_una_entrada_por_fuente(tmp_path, universo, monkeypatch):
    b, fues, msg = _caso_dos(tmp_path, universo)
    carpeta = b.almacen.carpeta
    barrera = threading.Barrier(4)
    # cierre de la QA r02 (H-10): otra barrera, con plazo, dentro de la sección crítica (tras leer lo atendido). Sin el cerrojo
    # los cuatro leen antes de que nadie escriba; con él, el plazo vence y siguen uno detrás de otro
    dentro, leer = threading.Barrier(4, timeout=3), fiabilidad_f9.atendidas

    def atendidas_lento(almacen, as_of=None):
        r = leer(almacen, as_of)
        try:
            dentro.wait()
        except threading.BrokenBarrierError:
            pass
        return r
    monkeypatch.setattr(fiabilidad_f9, "atendidas", atendidas_lento)
    resultados, errores = [], []

    def atender():
        alm = Almacen(carpeta, Reloj())
        alm.reloj.fijar(AS_OF)
        otro = types.SimpleNamespace(almacen=alm, cfg=b.cfg, referencias=b.referencias)
        barrera.wait()
        try:
            resultados.append(fiabilidad_f9.atender_ct19(otro, msg, AS_OF, "RUN-2026-0001"))
        except Exception as e:  # noqa: BLE001 — la prueba recoge cualquier fallo para afirmarlo
            errores.append(e)
    hilos = [threading.Thread(target=atender) for _ in range(4)]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    assert errores == []
    assert sorted(len(r) for r in resultados) == [0, 0, 0, 2]
    final = Almacen(carpeta, Reloj())
    assert sorted(e["fue_id"] for e in final.leer("F9")) == sorted(f["fue_id"] for f in fues)
    assert all(final.verificar_integridad().values())


# ---------------------------------------------------------------- CA-4 · lo comunicado y sin atender sale otra vez
def test_ca4_una_fue_comunicada_antes_de_t198_se_atiende_en_el_ciclo_siguiente(tmp_path, universo):
    """Un almacén de antes de T-198: la FUE- tiene `comunicado_ct19` de un CT-19 que nadie atendió."""
    b, fues, msg = _caso_dos(tmp_path, universo)
    assert fiabilidad_f9.por_comunicar(b.almacen, AS_OF) == sorted(
        (b.almacen.estado("F6", clave="id")[f["fue_id"]] for f in fues), key=lambda f: (f["periodo"], f["fue_id"]))
    assert len(b._comunicar_fiabilidad(b.reloj.fecha, "RUN-2026-0002")) == 2
    nuevo = _ct19_al_buscador(b)[-1]["msg_id"]
    assert nuevo != msg["msg_id"]
    assert {e["recibido_via"] for e in _f9(b)} == {nuevo}
    f6 = b.almacen.estado("F6", clave="id")
    assert all(f6[f["fue_id"]]["comunicado_ct19"] == nuevo for f in fues)
    assert fiabilidad_f9.por_comunicar(b.almacen, AS_OF) == []


def test_ca4_la_mas_reciente_de_una_fuente_queda_la_ultima(tmp_path, universo):
    b = _bloque(tmp_path, universo, cfg=config_pruebas())
    for i, periodo in enumerate(("2026-06", "2026-05")):   # escritas en orden inverso
        fue_id = f"FUE-2026-000{i + 1}"
        b.almacen.escribir("F6", "AG-20", {"tipo_entrada": "FUE", "id": fue_id, "fue_id": fue_id, "ref_id": FUENTE_A,
                                           "periodo": periodo, "n": 10 + i, "aciertos": 5, "bss": 0.1, "bss_contraido": 0.05,
                                           "puntos_historial": 10.5 + i, "calc_id": "CALC-2026-0001", "comunicado_ct19": None})
    assert len(b._comunicar_fiabilidad(b.reloj.fecha, "RUN-2026-0001")) == 2
    assert fiabilidad_f9.fiabilidad_medida(b.almacen, AS_OF)[FUENTE_A]["puntos_historial"] == 10.5   # la de 2026-06


# ---------------------------------------------------------------- CA-5 · el Buscador la ve en sus búsquedas (CT-07)
def test_ca5_anotar_candidatas_solo_las_de_f9_con_fiabilidad_y_sin_fuga(tmp_path, universo):
    b, _, msg = _caso_dos(tmp_path, universo)
    fiabilidad_f9.atender_ct19(b, msg, b.reloj.fecha, "RUN-2026-0001")
    cands = [{"ref_id": FUENTE_A, "archivo": "F9"}, {"ref_id": "REF-RF-0004", "archivo": "F9"}, {"ref_id": FUENTE_B, "archivo": "F7"}]
    fiabilidad_f9.anotar_candidatas(b.almacen, AS_OF, cands)
    assert set(cands[0]["fiabilidad_medida"]) == set(fiabilidad_f9.CAMPOS_CONTEXTO)
    assert cands[0]["fiabilidad_medida"]["resueltos"] == 25 and cands[0]["fiabilidad_medida"]["fecha_ct19"] == AS_OF
    assert "fiabilidad_medida" not in cands[1] and "fiabilidad_medida" not in cands[2]
    antes = [{"ref_id": FUENTE_A, "archivo": "F9"}]
    fiabilidad_f9.anotar_candidatas(b.almacen, "2026-06-04", antes)   # lo escrito el 5 no se conoce el 4
    assert antes == [{"ref_id": FUENTE_A, "archivo": "F9"}]


def test_ca5_en_un_ciclo_la_busqueda_del_buscador_lleva_la_fiabilidad_medida(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo, cfg=config_pruebas())
    cand = b.referencias.para_clase("RV", AS_OF, b.modo, max_n=8, archivos=("F9",))["referencias"]
    medida = cand[0]["ref_id"]
    _sembrar(b, medida, 20, 5)
    original = mock_respuestas._analista
    vistas = []

    def analista(msg, ctx, rng, inyectado):
        r = original(msg, ctx, rng, inyectado)
        for f in r.get("finalistas", []):
            f["peticiones_conocimiento"] = [{"tipo": "CT-07", "pregunta": "¿Qué dicen las fuentes?", "objetivo": "confirmar"}]
        return r

    def busqueda(msg, ctx, rng):
        vistas.append(copy.deepcopy(msg.get("referencias_candidatas") or []))
        return {"referencias": [], "sintesis": "Sin piezas.", "contradicciones": [], "lagunas": []}
    monkeypatch.setattr(mock_respuestas, "_analista", analista)
    monkeypatch.setattr(mock_respuestas, "_busqueda", busqueda)
    b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert vistas
    for refs in vistas:
        con = [r for r in refs if "fiabilidad_medida" in r]
        assert [r["ref_id"] for r in con] == [medida]
        assert con[0]["fiabilidad_medida"]["resueltos"] == 25 and con[0]["fiabilidad_medida"]["puntos_historial"] > 10


# ---------------------------------------------------------------- CA-6 · F9 de la instancia en el almacén
def test_ca6_solo_ag16_escribe_f9_y_solo_fiabilidad_medida(tmp_path):
    alm = Almacen(tmp_path / "estado")
    with pytest.raises(EscrituraFueraDeReserva):
        alm.escribir("F9", "AG-20", {"tipo_entrada": "FIABILIDAD_MEDIDA", "ref_id": FUENTE_A})
    with pytest.raises(EscrituraFueraDeReserva):
        alm.escribir("F9", "AG-16", {"tipo_entrada": "RECALIFICACION", "ref_id": FUENTE_A})
    with pytest.raises(EscrituraFueraDeReserva):
        alm.escribir("F6", "AG-16", {"tipo_entrada": "FUE", "id": "FUE-2026-0001"})
    assert alm.leer("F9") == []
    alm.escribir("F9", "AG-16", {"tipo_entrada": "FIABILIDAD_MEDIDA", "ref_id": FUENTE_A})
    assert [e["ref_id"] for e in alm.leer("F9")] == [FUENTE_A]


def _quitar_sello(carpeta, archivo):
    ruta = carpeta / "sellos_integridad.json"
    sellos = json.loads(ruta.read_text(encoding="utf-8"))
    sellos.pop(archivo)
    ruta.write_text(json.dumps(sellos), encoding="utf-8")


def test_ca6_un_almacen_sellado_antes_de_t198_abre_y_sella_f9_vacio(tmp_path):
    carpeta = tmp_path / "estado"
    Almacen(carpeta).escribir("F6", "AG-20", {"tipo_entrada": "FUE", "id": "FUE-2026-0001"})
    _quitar_sello(carpeta, "F9")                              # como lo dejó la versión anterior
    alm = Almacen(carpeta)
    assert json.loads((carpeta / "sellos_integridad.json").read_text(encoding="utf-8"))["F9"] == [0, "0" * 64]
    assert all(alm.verificar_integridad().values()) and len(alm.leer("F6")) == 1
    alm.escribir("F9", "AG-16", {"tipo_entrada": "FIABILIDAD_MEDIDA", "ref_id": FUENTE_A})
    assert len(Almacen(carpeta).leer("F9")) == 1


def test_ca6_f9_sin_sello_o_borrado_falla_cerrado(tmp_path):
    carpeta = tmp_path / "estado"
    Almacen(carpeta).escribir("F9", "AG-16", {"tipo_entrada": "FIABILIDAD_MEDIDA", "ref_id": FUENTE_A})
    _quitar_sello(carpeta, "F9")                              # el archivo existe y su sello no
    with pytest.raises(ValueError, match="F9"):
        Almacen(carpeta)
    otra = tmp_path / "otra"
    Almacen(otra).escribir("F9", "AG-16", {"tipo_entrada": "FIABILIDAD_MEDIDA", "ref_id": FUENTE_A})
    (otra / ARCHIVOS["F9"]).unlink()                          # borrado con su sello en su sitio
    with pytest.raises(ValueError, match="F9"):
        Almacen(otra)


# ---------------------------------------------------------------- CA-7 · regresión
def test_ca7_sin_fue_no_hay_ct19_ni_f9_ni_anotacion(tmp_path, universo):
    b = _bloque(tmp_path, universo, cfg=config_pruebas())
    assert b._comunicar_fiabilidad(b.reloj.fecha, "RUN-2026-0001") == []
    assert _ct19_al_buscador(b) == [] and not (b.almacen.carpeta / ARCHIVOS["F9"]).exists()
    cands = [{"ref_id": FUENTE_A, "archivo": "F9"}]
    fiabilidad_f9.anotar_candidatas(b.almacen, AS_OF, cands)
    assert cands == [{"ref_id": FUENTE_A, "archivo": "F9"}]


def test_ca7_el_ct19_al_buscador_conserva_sus_campos(tmp_path, universo):
    """El cuerpo es el de T-125 (`tipo` y `fuentes` con los campos de la FUE-): el contrato no cambia."""
    b = _bloque(tmp_path, universo, cfg=config_pruebas())
    _sembrar(b, FUENTE_A, 20, 5)
    fue = b.evaluador.fiabilidad_fuentes(AS_OF, "RUN-2026-0001")[0]
    cuerpo = fiabilidad_f9.cuerpo_ct19([fue])
    assert cuerpo == {"tipo": "FIABILIDAD_FUENTES", "fuentes": [{k: fue[k] for k in
                      ("fue_id", "ref_id", "periodo", "n", "aciertos", "bss", "bss_contraido", "puntos_historial")}]}
    assert CAMPOS_CT19 == ("fue_id", "ref_id", "periodo", "n", "aciertos", "bss", "bss_contraido", "puntos_historial")


def test_ca7_ningun_texto_de_f9_dice_valid(tmp_path, universo):
    """R8 y G3-MET-13: lo que escribe el ejecutor no llama «validado» a nada."""
    b, _, msg = _caso_dos(tmp_path, universo)
    fiabilidad_f9.atender_ct19(b, msg, b.reloj.fecha, "RUN-2026-0001")
    texto = json.dumps(_f9(b), ensure_ascii=False).lower()
    assert "valid" not in texto


# ---------------------------------------------------------------- Ronda r02 (QA r01 NO APTO)
def _inc_no_atendido(b):
    return [e for e in b.almacen.leer("HA") if "no atendido por el Buscador" in str(e.get("detalle"))]


def test_r02_h01_una_fue_cuya_fuente_salio_de_f9_no_bloquea_a_las_demas(tmp_path, universo, monkeypatch):
    """La de `revisores/r01_ataques.py`: dos FUE- y la fuente B deja de estar en F9 (baja R19, borrado de HT-02, otra versión de
    F9). A se atiende; B se declara una vez y no vuelve a salir en el CT-19."""
    b = _bloque(tmp_path, universo, cfg=config_pruebas())
    _dos_fuentes(b)
    fues = {f["ref_id"]: f for f in b.evaluador.fiabilidad_fuentes(AS_OF, "RUN-2026-0001")}
    original = b.referencias.por_id
    monkeypatch.setattr(b.referencias, "por_id", lambda r: None if r == FUENTE_B else original(r))
    for i in range(3):
        b._comunicar_fiabilidad(b.reloj.fecha, f"RUN-2026-000{i + 2}")
    assert [e["ref_id"] for e in _f9(b)] == [FUENTE_A]
    marcas = [e for e in b.almacen.leer("HA") if e.get("fue_no_atendible")]
    assert [e["fue_no_atendible"] for e in marcas] == [fues[FUENTE_B]["fue_id"]] and marcas[0]["tipo"] == "DATOS"
    assert marcas[0]["run_id"] == "RUN-2026-0002" and _inc_no_atendido(b) == []
    ct19 = _ct19_al_buscador(b)
    assert len(ct19) == 1                                   # los ciclos 3 y 4 no reenvían nada
    assert fiabilidad_f9.por_comunicar(b.almacen, AS_OF) == []


def test_r02_h01_con_todas_las_fuentes_fuera_de_f9_no_hay_ct19(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo, cfg=config_pruebas())
    _sembrar(b, FUENTE_A, 20, 5)
    b.evaluador.fiabilidad_fuentes(AS_OF, "RUN-2026-0001")
    monkeypatch.setattr(b.referencias, "por_id", lambda r: None)
    assert b._comunicar_fiabilidad(b.reloj.fecha, "RUN-2026-0002") == []
    assert _ct19_al_buscador(b) == [] and _f9(b) == []
    assert len([e for e in b.almacen.leer("HA") if e.get("fue_no_atendible")]) == 1


def test_r02_h02_solo_f9_se_sella_vacio_los_demas_borrados_fallan_cerrado(tmp_path):
    """El script `revisores/r01_sello_generico.py` hecho prueba: HA, F4 o F6 borrados con su sello quitado no abren."""
    for archivo, autor, entrada in (("HA", "AG-18", {"tipo_entrada": "INC", "id": "INC-2026-0001"}),
                                    ("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": "PRG-2026-0001"}),
                                    ("F6", "AG-20", {"tipo_entrada": "FUE", "id": "FUE-2026-0001"})):
        carpeta = tmp_path / archivo
        Almacen(carpeta).escribir(archivo, autor, entrada)
        (carpeta / ARCHIVOS[archivo]).unlink()
        _quitar_sello(carpeta, archivo)
        with pytest.raises(ValueError, match=archivo):
            Almacen(carpeta)


@pytest.mark.parametrize("ts", ["2099-01-01T06:00:00+01:00", "2026-06-06T06:00:00+02:00", "ayer", "2026-02-30T06:00:00", "2026-06-04 y algo más", None, 20260605])
def test_r02_h03_un_timestamp_posterior_a_as_of_o_que_no_es_fecha_no_se_atiende(tmp_path, universo, ts):
    b, _, msg = _caso_dos(tmp_path, universo)
    with pytest.raises(FiabilidadNoAtendible, match="timestamp"):
        fiabilidad_f9.atender_ct19(b, _otro(msg, timestamp=ts), b.reloj.fecha, "RUN-2026-0001")
    assert _f9(b) == []


def test_r02_h03_un_timestamp_de_as_of_o_anterior_si(tmp_path, universo):
    b, _, msg = _caso_dos(tmp_path, universo)
    assert len(fiabilidad_f9.atender_ct19(b, _otro(msg, timestamp="2026-06-04T23:59:59+02:00"), b.reloj.fecha, "RUN-2026-0001")) == 2
    assert {e["fecha_ct19"] for e in _f9(b)} == {"2026-06-04"}


def test_r02_h04_una_fue_escrita_despues_de_as_of_no_se_atiende_en_as_of(tmp_path, universo):
    b = _bloque(tmp_path, universo, cfg=config_pruebas())
    b.reloj.fijar("2026-06-10")
    fue = {"tipo_entrada": "FUE", "id": "FUE-2026-0001", "fue_id": "FUE-2026-0001", "ref_id": FUENTE_A, "periodo": "2026-06",
           "n": 10, "aciertos": 6, "bss": 0.1, "bss_contraido": 0.03, "puntos_historial": 10.3, "calc_id": "CALC-2026-0001",
           "metodo": "m", "comunicado_ct19": None}
    b.almacen.escribir("F6", "AG-20", fue)                 # conocida el 10
    b.reloj.fijar(AS_OF)
    msg = _msg_comunicado(b, [fue])                         # mensaje y anotación del 5
    with pytest.raises(FiabilidadNoAtendible):
        fiabilidad_f9.atender_ct19(b, msg, AS_OF, "RUN-2026-0001")
    assert _f9(b) == []
    assert fiabilidad_f9.atender_ct19(b, msg, "2026-06-10", "RUN-2026-0001") == ["FUE-2026-0001"]   # el 10 sí


def test_r02_h04_en_un_ciclo_el_ct07_no_ve_fiabilidad_posterior_a_as_of(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo, cfg=config_pruebas())
    medida = b.referencias.para_clase("RV", AS_OF, b.modo, max_n=8, archivos=("F9",))["referencias"][0]["ref_id"]
    b.reloj.fijar("2026-06-12")
    b.almacen.escribir("F9", "AG-16", {"tipo_entrada": "FIABILIDAD_MEDIDA", "id": "FMD-2026-0001", "ref_id": medida,
                                       "resueltos": 25, "puntos_historial": 11.0, "fecha_ct19": "2026-06-12"})
    b.reloj.fijar(AS_OF)
    original, vistas = mock_respuestas._analista, []

    def analista(msg, ctx, rng, inyectado):
        r = original(msg, ctx, rng, inyectado)
        for f in r.get("finalistas", []):
            f["peticiones_conocimiento"] = [{"tipo": "CT-07", "pregunta": "¿Qué dicen las fuentes?", "objetivo": "confirmar"}]
        return r

    def busqueda(msg, ctx, rng):
        vistas.append(copy.deepcopy(msg.get("referencias_candidatas") or []))
        return {"referencias": [], "sintesis": "Sin piezas.", "contradicciones": [], "lagunas": []}
    monkeypatch.setattr(mock_respuestas, "_analista", analista)
    monkeypatch.setattr(mock_respuestas, "_busqueda", busqueda)
    b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert vistas and any(r["ref_id"] == medida for refs in vistas for r in refs)
    assert not [r for refs in vistas for r in refs if "fiabilidad_medida" in r]


def test_r02_h05_dos_bloques_a_la_vez_un_solo_ct19_y_ninguna_incidencia(tmp_path, universo, monkeypatch):
    """Dos procesos (dos `Bloque` sobre la misma carpeta) en `_comunicar_fiabilidad` a la vez. Una barrera con plazo dentro de
    `por_comunicar` hace que, sin el cerrojo del ciclo, los dos lean lo pendiente antes de que ninguno escriba."""
    b1 = _bloque(tmp_path, universo, cfg=config_pruebas())
    _dos_fuentes(b1)
    fues = b1.evaluador.fiabilidad_fuentes(AS_OF, "RUN-2026-0001")
    b2 = _bloque(tmp_path, universo, cfg=config_pruebas())
    barrera, original = threading.Barrier(2, timeout=3), fiabilidad_f9.por_comunicar

    def lento(almacen, as_of):
        r = original(almacen, as_of)
        try:
            barrera.wait()
        except threading.BrokenBarrierError:
            pass
        return r
    monkeypatch.setattr(fiabilidad_f9, "por_comunicar", lento)
    errores = []

    def correr(b, run):
        try:
            b._comunicar_fiabilidad(b.reloj.fecha, run)
        except Exception as e:  # noqa: BLE001 — la prueba recoge cualquier fallo para afirmarlo
            errores.append(e)
    hilos = [threading.Thread(target=correr, args=(b, f"RUN-2026-000{i + 2}")) for i, b in enumerate((b1, b2))]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    final = Almacen(b1.almacen.carpeta, Reloj())
    assert errores == []
    assert len(_ct19_al_buscador(b1)) + len(_ct19_al_buscador(b2)) == 1
    assert sorted(e["fue_id"] for e in final.leer("F9")) == sorted(f["fue_id"] for f in fues)
    assert not [e for e in final.leer("HA") if "no atendido por el Buscador" in str(e.get("detalle"))]


def test_r02_h06_si_el_almacen_falla_a_mitad_el_ciclo_siguiente_completa_sin_duplicar(tmp_path, universo, monkeypatch):
    """La de `revisores/r01_ataques.py`: no hay vuelta atrás (cerrojo, no transacción); lo escrito queda y se completa."""
    b = _bloque(tmp_path, universo, cfg=config_pruebas())
    _dos_fuentes(b)
    b.evaluador.fiabilidad_fuentes(AS_OF, "RUN-2026-0001")
    escribir, n = b.almacen.escribir, {"f9": 0}

    def roto(archivo, autor, entrada):
        if archivo == "F9":
            n["f9"] += 1
            if n["f9"] == 2:
                raise OSError("disco lleno")
        return escribir(archivo, autor, entrada)
    monkeypatch.setattr(b.almacen, "escribir", roto)
    with pytest.raises(OSError):
        b._comunicar_fiabilidad(b.reloj.fecha, "RUN-2026-0001")
    assert len(_f9(b)) == 1
    monkeypatch.setattr(b.almacen, "escribir", escribir)
    assert len(b._comunicar_fiabilidad(b.reloj.fecha, "RUN-2026-0002")) == 1
    assert sorted(e["ref_id"] for e in _f9(b)) == sorted([FUENTE_A, FUENTE_B])
    assert all(b.almacen.verificar_integridad().values())


# ---------------------------------------------------------------- Ronda de cierre de la QA r02
def test_r02_f9_ilegible_un_ciclo_no_quema_las_fue(tmp_path, universo, monkeypatch):
    """La de `revisores/r02_ataques.py` (H-08): un ciclo con F9 sin fichas cargadas no marca nada ni envía CT-19; deja una
    incidencia sin marca y, cuando F9 vuelve, las dos FUE- se atienden."""
    b = _bloque(tmp_path, universo, cfg=config_pruebas())
    _dos_fuentes(b)
    b.evaluador.fiabilidad_fuentes(AS_OF, "RUN-2026-0001")
    fichas = b.referencias.fichas
    monkeypatch.setattr(b.referencias, "fichas", {k: ([] if k == "F9" else v) for k, v in fichas.items()})
    assert b._comunicar_fiabilidad(b.reloj.fecha, "RUN-2026-0002") == []
    assert _ct19_al_buscador(b) == [] and fiabilidad_f9.no_atendibles(b.almacen) == set()
    inc = [e for e in b.almacen.leer("HA") if "F9 no se pudo leer" in str(e.get("detalle"))]
    assert len(inc) == 1 and "fue_no_atendible" not in inc[0] and inc[0]["run_id"] == "RUN-2026-0002"
    monkeypatch.setattr(b.referencias, "fichas", fichas)
    assert len(b._comunicar_fiabilidad(b.reloj.fecha, "RUN-2026-0003")) == 2
    assert sorted(e["ref_id"] for e in _f9(b)) == [FUENTE_A, FUENTE_B]
    assert fiabilidad_f9.no_atendibles(b.almacen) == set()
