"""T-197 (PB-09) · Cambio de periodicidad por el Broker: el P-01 que escribe el CT-04 guarda la ejecución y la entrega, HT-05
dispara el siguiente C1 en la fecha nueva según el P-01 de F10 (una vez, también entre procesos) y ningún otro parámetro cambia.

Calendario de las pruebas: el bloque se instala el viernes 29-05-2026 (P-01 por defecto, semanal, ejecución SAB 06:00 y
entrega LUN 07:00); el Broker pide QUINCENAL con entrega MIE 08:00 el martes 02-06 (efecto 03-06)."""
import copy
import datetime as dt
import json
import multiprocessing as mp
import os
import threading
import time

import pytest
from bloque_a.almacen import Reloj
from bloque_a.configuracion import parametro
from bloque_a.herramientas import ht05_planificador as ht05
from conftest import DATOS, config_pruebas, nuevo_bloque

from bloque_a import orquestacion
from bloque_a import planificacion_c1 as plan

INSTALACION = "2026-05-29"
CT04 = {"configuracion": {"periodicidad": "QUINCENAL", "dia_hora_entrega": "MIE 08:00"}}
NUEVO_P01 = "QUINCENAL · LUN 07:00 · entrega MIE 08:00"


class RelojInstalado(Reloj):
    """El F10 inicial nace el día de la instalación, no el día en que corre la prueba."""

    def __init__(self, zona: str = "Europe/Madrid") -> None:
        super().__init__(zona)
        self.fijar(INSTALACION)


@pytest.fixture
def bloque(tmp_path, universo, monkeypatch):
    monkeypatch.setattr(orquestacion, "Reloj", RelojInstalado)
    return nuevo_bloque(tmp_path, universo)


def _con_ciclo_simulado(b, fallo=None, espera=None):
    """Sustituye el C1 por uno que anota la llamada (las pruebas del disparo no necesitan el análisis entero)."""
    llamadas = []

    def ciclo(as_of=None, disparador=None, **kw):
        llamadas.append({"as_of": str(as_of), "disparador": copy.deepcopy(disparador)})
        if espera is not None:
            espera.wait(5)
        if fallo is not None:
            raise fallo
        return {"run_id": f"RUN-SIM-{len(llamadas)}", "estado": "COMPLETO"}

    b.ciclo = ciclo
    return llamadas


def _disparos(b):
    return [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "DISPARO"]


def _f10_sin_historial(b, dia):
    return {k: {c: v for c, v in e.items() if not c.startswith("_")} for k, e in b.almacen.estado("F10", "2026-12-31", efectivo_el=dia).items()}


# ------------------------------------------------------------------ CA-1 · el P-01 del CT-04 guarda ejecución y entrega
def test_ca1_ct04_escribe_el_p01_completo_con_fecha_de_efecto(bloque):
    r = bloque.decision(CT04, "2026-06-02")
    assert r["estado"] == "APLICADA" and list(r["aplicado"]) == ["P-01"]
    cfg = [e for e in bloque.almacen.leer("F10") if e.get("tipo_entrada") == "CFG"]
    assert len(cfg) == 1 and cfg[0]["autor"] == "AG-01" and cfg[0]["_autor"] == "AG-01"
    assert cfg[0]["de"] == ht05.P01_INICIAL and cfg[0]["a"] == cfg[0]["valor_vigente"] == NUEVO_P01
    assert cfg[0]["fecha_efecto"] == "2026-06-03" and cfg[0]["origen"] == r["ret_id"]
    assert bloque.f10("2026-06-02")["P-01"] == ht05.P01_INICIAL      # hasta la fecha de efecto rige el anterior
    assert bloque.f10("2026-06-03")["P-01"] == NUEVO_P01
    ret = bloque.almacen.estado("F5")[r["ret_id"]]
    assert ret["estado"] == "APLICADA" and ret["aplicado_en_f10"]["parametros"] == {"P-01": cfg[0]["cfg_id"]}
    avisos = [m for m in bloque.mensajeria.registro if m["contrato"] == "CT-22" and m["receptor"] == "AG-20"]
    assert [m["msg_id"] for m in avisos] == [ret["aviso_ct22"]]


def test_ca1_cambios_parciales_conservan_la_otra_parte_y_recalculan_la_ejecucion(bloque):
    bloque.decision({"configuracion": {"dia_hora_entrega": "MIE 08:30"}}, "2026-06-02")
    assert bloque.f10("2026-06-03")["P-01"] == "SEMANAL · LUN 07:00 · entrega MIE 08:30"     # redondeo hacia abajo
    bloque.decision({"configuracion": {"periodicidad": "DIARIA"}}, "2026-06-03")
    assert bloque.f10("2026-06-04")["P-01"] == "DIARIA · MIE 06:00 · entrega MIE 08:30"      # adelanto diario (2 h)
    bloque.decision({"configuracion": {"periodicidad": "MENSUAL", "dia_hora_entrega": "MIÉ 08:00"}}, "2026-06-04")
    assert bloque.f10("2026-06-05")["P-01"] == "MENSUAL · LUN 07:00 · entrega MIÉ 08:00"


def test_ca1_lee_el_p01_de_dos_partes_anterior_a_t197(bloque):
    bloque.almacen.reloj.fijar("2026-06-01")
    bloque.almacen.escribir("F10", "AG-01", {"tipo_entrada": "CFG", "cfg_id": "CFG-2026-0900", "param_id": "P-01",
                                             "a": "QUINCENAL · MIE 08:00", "valor_vigente": "QUINCENAL · MIE 08:00",
                                             "autor": "AG-01", "fecha_efecto": "2026-06-02"})
    bloque.decision({"configuracion": {"periodicidad": "SEMANAL"}}, "2026-06-02")
    assert bloque.f10("2026-06-03")["P-01"] == "SEMANAL · LUN 07:00 · entrega MIE 08:00"
    assert ht05.leer_p01("QUINCENAL · MIE 08:00") == ("QUINCENAL", None, "MIE 08:00")


def test_ca1_rechaza_lo_que_ht05_no_puede_programar_sin_tocar_f10(bloque):
    antes = bloque.almacen.leer("F10")
    for conf, motivo in [({"dia_hora_entrega": "LUN 03:30"}, "franja sin disparos"),   # ejecución SAB 02:00
                         ({"periodicidad": "DIARIA", "dia_hora_entrega": "LUN 01:00"}, "día anterior"),
                         ({"periodicidad": "PERSONALIZADA"}, "no programable"),
                         ({"dia_hora_entrega": "LUNES 7"}, "HH:MM"),
                         # r02 (H-04): la entrega también es un disparo de HT-05; ninguna entre las 02:00 y las 03:00
                         ({"dia_hora_entrega": "DOM 02:30"}, "la entrega a las 02:30"),
                         ({"dia_hora_entrega": "LUN 02:00"}, "la entrega a las 02:00"),
                         ({"dia_hora_entrega": "MIE 02:59"}, "la entrega a las 02:59")]:
        r = bloque.decision({"configuracion": conf}, "2026-06-02")
        assert not r["aplicado"] and motivo in r["rechazos"][0]["motivo"], (conf, r)
    assert bloque.almacen.leer("F10") == antes


def test_ca1_p01_ilegible_exige_las_dos_partes(bloque):
    bloque.almacen.reloj.fijar("2026-06-01")
    bloque.almacen.escribir("F10", "AG-01", {"tipo_entrada": "CFG", "cfg_id": "CFG-2026-0901", "param_id": "P-01",
                                             "valor_vigente": "CADA LUNA LLENA", "autor": "AG-01", "fecha_efecto": "2026-06-02"})
    r = bloque.decision({"configuracion": {"periodicidad": "SEMANAL"}}, "2026-06-02")
    assert not r["aplicado"] and r["rechazos"]
    r = bloque.decision(CT04, "2026-06-02")
    assert r["aplicado"] and bloque.f10("2026-06-03")["P-01"] == NUEVO_P01


# ------------------------------------------------------------------ CA-2 · HT-05 calcula el siguiente C1 con el P-01 de F10
def test_ca2_proximo_c1_en_la_fecha_nueva(bloque):
    bloque.fijar_fecha("2026-06-02")
    antes = plan.proximo(bloque, "2026-06-02T10:00")
    assert antes["programado"] == "2026-06-06T06:00" and antes["entrega"] == "2026-06-08T07:00"   # semanal vigente
    bloque.decision(CT04, "2026-06-02")
    nuevo = plan.proximo(bloque, "2026-06-02T10:00")
    assert nuevo["programado"] == "2026-06-08T07:00" and nuevo["entrega"] == "2026-06-10T08:00"
    assert nuevo["p01"] == NUEVO_P01 and nuevo["disparo_id"] == "C1-EJEC-2026-06-08T07:00"
    assert plan.proximo(bloque, "2026-06-08T07:00")["programado"] == "2026-06-22T07:00"          # quincenal, no semanal
    assert plan.proximo(bloque, "2026-06-22T07:00")["programado"] == "2026-07-06T07:00"


def test_ca2_calendarios_de_ht05():
    inicio = dt.date(2026, 6, 3)
    sig = ht05.siguiente_ejecucion
    assert sig(dt.datetime(2026, 6, 5, 9), "DIARIA", "LUN 05:00", inicio) == dt.datetime(2026, 6, 8, 5)        # sin fin de semana
    assert sig(dt.datetime(2026, 6, 3), "MENSUAL", "SAB 06:00", inicio) == dt.datetime(2026, 6, 6, 6)
    assert sig(dt.datetime(2026, 6, 6, 6), "MENSUAL", "SAB 06:00", inicio) == dt.datetime(2026, 7, 4, 6)
    assert sig(dt.datetime(2026, 6, 1), "SEMANAL", "SAB 06:00", inicio) == dt.datetime(2026, 6, 6, 6)          # no antes del inicio
    # la quincenal se ancla en su primera ejecución, no en la paridad de la semana ISO (2026 tiene 53 semanas)
    fin = dt.date(2026, 12, 21)
    assert sig(dt.datetime(2026, 12, 21, 7), "QUINCENAL", "LUN 07:00", fin) == dt.datetime(2027, 1, 4, 7)
    assert sig(dt.datetime(2027, 1, 4, 7), "QUINCENAL", "LUN 07:00", fin) == dt.datetime(2027, 1, 18, 7)   # ISO: semana 1 → 2
    assert ht05.ultima_ejecucion(dt.datetime(2026, 6, 2, 23), "SEMANAL", "SAB 06:00", inicio) is None
    assert ht05.entrega_de(dt.datetime(2026, 6, 8, 7), "QUINCENAL", "MIE 08:00") == dt.datetime(2026, 6, 10, 8)
    assert ht05.entrega_de(dt.datetime(2026, 6, 8, 5), "DIARIA", "LUN 07:00") == dt.datetime(2026, 6, 8, 7)


def test_ca2_los_numeros_salen_de_la_configuracion():
    cfg = parametro(None, "planificador")
    # el adelanto por defecto es el del P-01 inicial (SAB 06:00 → LUN 07:00, 49 h; especificación de HT-05, §4)
    per, ejec, ent = ht05.leer_p01(ht05.P01_INICIAL)
    assert ht05.ejecucion_para_entrega(per, ent, cfg) == ejec
    otro = dict(cfg, adelanto_ejecucion_h=dict(cfg["adelanto_ejecucion_h"], QUINCENAL=25))
    assert ht05.ejecucion_para_entrega("QUINCENAL", "MIE 08:00", otro) == "MAR 07:00"
    with pytest.raises(ht05.P01Invalido):
        ht05.ejecucion_para_entrega("SEMANAL", "LUN 08:30", dict(cfg, franja_sin_disparos_h=[7, 8]))


# ------------------------------------------------------------------ CA-3 · el siguiente C1 se dispara en la fecha nueva
def test_ca3_el_c1_se_dispara_en_la_fecha_nueva_y_no_en_la_antigua(bloque):
    llamadas = _con_ciclo_simulado(bloque)
    r = plan.disparar(bloque, "2026-05-30T06:10")                   # C1 semanal de antes del cambio
    assert r["estado"] == "EMITIDO" and r["disparo"]["disparo_id"] == "C1-EJEC-2026-05-30T06:00"
    bloque.decision(CT04, "2026-06-02")
    assert plan.disparar(bloque, "2026-06-06T06:10")["estado"] == "DESCARTADO_DUPLICADO"   # el sábado ya no hay C1
    assert plan.disparar(bloque, "2026-06-08T06:59")["estado"] == "DESCARTADO_DUPLICADO"
    r = plan.disparar(bloque, "2026-06-08T07:05")
    assert r["estado"] == "EMITIDO" and r["run_id"] == "RUN-SIM-2" and r["proximo"]["programado"] == "2026-06-22T07:00"
    assert [c["as_of"][:16] for c in llamadas] == ["2026-05-30 06:10", "2026-06-08 07:05"]
    d = llamadas[1]["disparador"]
    assert d["origen"] == "HT-05" and d["disparo_id"] == "C1-EJEC-2026-06-08T07:00" and d["p01"] == NUEVO_P01
    assert d["cfg_id"] == bloque.almacen.estado("F10")["P-01"]["cfg_id"]
    assert plan.disparar(bloque, "2026-06-15T07:05")["estado"] == "DESCARTADO_DUPLICADO"   # semana sin C1 (quincenal)
    assert len(llamadas) == 2
    f5 = bloque.almacen.estado("F5")["C1-EJEC-2026-06-08T07:00"]
    assert (f5["estado"], f5["run_id"], f5["estado_run"], f5["p01"], f5["entrega"]) == (
        "EMITIDO", "RUN-SIM-2", "COMPLETO", NUEVO_P01, "2026-06-10T08:00")


def test_ca3_ciclo_real_disparado_lleva_su_p01_en_el_run(tmp_path, universo, monkeypatch):
    """Integración: el C1 que dispara HT-05 es un ciclo real del bloque (cliente simulado) y su RUN- de F5 lleva el P-01."""
    monkeypatch.setattr(orquestacion, "Reloj", RelojInstalado)
    b = nuevo_bloque(tmp_path, universo, cfg=config_pruebas(perfiles={"activos": ["DIV"]}))
    b.decision(CT04, "2026-06-02")
    r = plan.disparar(b, "2026-06-08T07:05")
    assert r["estado"] == "EMITIDO" and r["run_id"].startswith("RUN-")
    run = b.almacen.estado("F5")[r["run_id"]]
    assert run["tipo_entrada"] == "RUN" and run["tipo"] == "PERIODICO" and run["fecha_inicio"] == "2026-06-08"
    assert run["disparador"]["disparo_id"] == "C1-EJEC-2026-06-08T07:00" and run["disparador"]["p01"] == NUEVO_P01
    assert b.almacen.estado("F5")["C1-EJEC-2026-06-08T07:00"]["run_id"] == r["run_id"]


# ------------------------------------------------------------------ CA-4 · ningún otro parámetro cambia
def test_ca4_ningun_otro_parametro_cambia(bloque):
    _con_ciclo_simulado(bloque)
    cfg_antes = copy.deepcopy(bloque.cfg)
    antes = _f10_sin_historial(bloque, "2026-06-03")
    bloque.decision(CT04, "2026-06-02")
    despues = _f10_sin_historial(bloque, "2026-06-03")
    assert set(antes) == set(despues)
    assert {k for k in antes if antes[k] != despues[k]} == {"P-01"}
    assert despues["P-30"]["valor_vigente"] == antes["P-30"]["valor_vigente"]            # methodology_version sin cambio
    assert [e["param_id"] for e in bloque.almacen.leer("F10") if e.get("tipo_entrada") == "CFG"] == ["P-01"]
    n_f10 = len(bloque.almacen.leer("F10"))
    plan.disparar(bloque, "2026-06-08T07:05")
    assert len(bloque.almacen.leer("F10")) == n_f10 and bloque.cfg == cfg_antes      # disparar no escribe en F10


# ------------------------------------------------------------------ CA-5 · disparos perdidos, idempotencia y fallo cerrado
def test_ca5_disparo_perdido_se_recupera_una_vez_o_queda_perdido(bloque):
    llamadas = _con_ciclo_simulado(bloque)
    r = plan.disparar(bloque, "2026-06-01T08:00")                   # entrega LUN 07:00 pasada, dentro de 24 h
    assert r["estado"] == "RECUPERADO" and len(llamadas) == 1
    r = plan.disparar(bloque, "2026-06-09T07:01")                   # el C1 del 06-06 nunca se lanzó: más de 24 h tarde
    assert r["estado"] == "PERDIDO" and r["run_id"] is None and len(llamadas) == 1
    assert bloque.almacen.estado("F5")["C1-EJEC-2026-06-06T06:00"]["estado"] == "PERDIDO"
    assert plan.disparar(bloque, "2026-06-09T08:00")["estado"] == "DESCARTADO_DUPLICADO"
    assert len(llamadas) == 1


def test_ca5_limite_de_24_horas(bloque):
    llamadas = _con_ciclo_simulado(bloque)
    assert plan.disparar(bloque, "2026-06-02T07:00")["estado"] == "RECUPERADO" and len(llamadas) == 1


def test_ca5_sin_ejecutar_no_escribe(bloque):
    llamadas = _con_ciclo_simulado(bloque)
    r = plan.disparar(bloque, "2026-05-30T06:10", ejecutar=False)
    assert r["estado"] == "PENDIENTE" and not llamadas and not _disparos(bloque)
    assert plan.disparar(bloque, "2026-05-29T05:00")["estado"] == "SIN_DISPARO"          # antes de la instalación, nada


def test_ca5_ciclo_cortado_queda_fallido_y_no_se_repite(bloque):
    llamadas = _con_ciclo_simulado(bloque, fallo=RuntimeError("corte"))
    with pytest.raises(RuntimeError):
        plan.disparar(bloque, "2026-05-30T06:10")
    f5 = bloque.almacen.estado("F5")["C1-EJEC-2026-05-30T06:00"]
    assert f5["estado_run"] == "FALLIDO" and f5["run_id"] is None
    assert plan.disparar(bloque, "2026-05-30T07:10")["estado"] == "DESCARTADO_DUPLICADO" and len(llamadas) == 1


def test_ca5_p01_ilegible_falla_cerrado_sin_escribir(bloque):
    llamadas = _con_ciclo_simulado(bloque)
    bloque.almacen.reloj.fijar("2026-06-01")
    bloque.almacen.escribir("F10", "AG-01", {"tipo_entrada": "CFG", "cfg_id": "CFG-2026-0902", "param_id": "P-01",
                                             "valor_vigente": "SEMANAL · SAB 6", "autor": "AG-01", "fecha_efecto": "2026-06-02"})
    n_f5 = len(bloque.almacen.leer("F5"))
    with pytest.raises(ht05.P01Invalido):
        plan.disparar(bloque, "2026-06-06T06:10")
    assert len(bloque.almacen.leer("F5")) == n_f5 and not llamadas
    for malo in ["PATATA · SAB 06:00 · entrega LUN 07:00", "SEMANAL · SAB 06:00 · LUN 07:00", "SEMANAL", "QUINCENAL · MIE 8:00"]:
        with pytest.raises(ht05.P01Invalido):
            ht05.leer_p01(malo)
    with pytest.raises(ht05.P01Invalido):
        ht05.componer_p01("SEMANAL", None, "LUN 07:00")                                     # nunca «None» en F10


def test_ca5_instante_con_zona_y_dias_antes_del_inicio(bloque):
    llamadas = _con_ciclo_simulado(bloque)
    with pytest.raises(ValueError, match="sin zona"):
        plan.disparar(bloque, "2026-05-30T06:10+02:00")
    assert not llamadas and not _disparos(bloque)
    assert not ht05.es_dia_de_ejecucion(dt.date(2026, 5, 30), "SEMANAL", "SAB 06:00", dt.date(2026, 6, 3))
    assert ht05.es_dia_de_ejecucion(dt.date(2026, 6, 6), "SEMANAL", "SAB 06:00", dt.date(2026, 6, 3))


def test_ca5_dos_procesos_a_la_vez_disparan_un_solo_c1(tmp_path, universo, monkeypatch):
    monkeypatch.setattr(orquestacion, "Reloj", RelojInstalado)
    bloques = [nuevo_bloque(tmp_path, universo) for _ in range(4)]
    espera = threading.Event()
    original = plan._disparo_registrado

    def lento(b, disparo_id):   # abre la ventana entre la lectura y la escritura: sin la transacción, los cuatro disparan
        r = original(b, disparo_id)
        time.sleep(0.2)
        return r

    monkeypatch.setattr(plan, "_disparo_registrado", lento)
    llamadas = [_con_ciclo_simulado(b, espera=espera) for b in bloques]
    salidas: list = []
    hilos = [threading.Thread(target=lambda b=b: salidas.append(plan.disparar(b, "2026-05-30T06:10"))) for b in bloques]
    for h in hilos:
        h.start()
    limite = time.monotonic() + 15
    while len(salidas) < 3 and time.monotonic() < limite:   # el que dispara sigue dentro del ciclo hasta `espera`
        time.sleep(0.05)
    espera.set()
    for h in hilos:
        h.join(10)
    # r02 (H-02): mientras el ciclo corre, su proceso vive: los otros tres ven el disparo EN_CURSO
    assert sorted(s["estado"] for s in salidas) == ["EMITIDO"] + ["EN_CURSO"] * 3
    assert plan.disparar(bloques[1], "2026-05-30T06:20")["estado"] == "DESCARTADO_DUPLICADO"   # ya cerrado
    assert sum(len(x) for x in llamadas) == 1 and len([e for e in _disparos(bloques[0]) if "programado" in e]) == 1


# ------------------------------------------------------------------ r02 (QA r01) · H-01: la quincena no se reinicia
def test_r02_h01_cambio_solo_de_hora_conserva_la_quincena(bloque):
    _con_ciclo_simulado(bloque)
    bloque.decision(CT04, "2026-06-02")
    assert plan.disparar(bloque, "2026-06-08T07:05")["estado"] == "EMITIDO"
    bloque.decision({"configuracion": {"dia_hora_entrega": "MIE 09:00"}}, "2026-06-09")
    cfg = [e for e in bloque.almacen.leer("F10") if e.get("tipo_entrada") == "CFG"]
    assert [e["semana_ancla_quincenal"] for e in cfg] == ["2026-06-08", "2026-06-08"]        # el ancla se copia
    assert plan.proximo(bloque, "2026-06-09T12:00")["programado"] == "2026-06-22T08:00"     # 14 días, no 7


def test_r02_h01_ct04_identico_no_escribe_cfg_ni_reinicia_la_quincena(bloque):
    _con_ciclo_simulado(bloque)
    bloque.decision(CT04, "2026-06-02")
    assert plan.disparar(bloque, "2026-06-08T07:05")["estado"] == "EMITIDO"
    n = len(bloque.almacen.leer("F10"))
    r = bloque.decision(CT04, "2026-06-09")
    assert r["estado"] == "APLICADA" and r["aplicado"] == {} and r["sin_cambio"] == ["P-01"]
    assert len(bloque.almacen.leer("F10")) == n
    assert bloque.almacen.estado("F5")[r["ret_id"]]["aplicado_en_f10"]["sin_cambio"] == ["P-01"]
    assert plan.proximo(bloque, "2026-06-09T12:00")["programado"] == "2026-06-22T07:00"


def test_r02_h01_cambio_de_dia_de_entrega_sigue_en_la_misma_quincena(bloque):
    _con_ciclo_simulado(bloque)
    bloque.decision(CT04, "2026-06-02")
    assert plan.disparar(bloque, "2026-06-08T07:05")["estado"] == "EMITIDO"
    bloque.decision({"configuracion": {"dia_hora_entrega": "JUE 08:00"}}, "2026-06-09")        # ejecución MAR 07:00
    assert plan.proximo(bloque, "2026-06-09T12:00")["programado"] == "2026-06-23T07:00"


def test_r02_h01_de_otra_periodicidad_a_quincenal_ancla_de_nuevo(bloque):
    bloque.decision(CT04, "2026-06-02")
    bloque.decision({"configuracion": {"periodicidad": "SEMANAL"}}, "2026-06-09")
    assert bloque.almacen.leer("F10")[-1]["semana_ancla_quincenal"] is None
    bloque.decision({"configuracion": {"periodicidad": "QUINCENAL"}}, "2026-06-16")           # efecto 17-06
    assert bloque.almacen.leer("F10")[-1]["semana_ancla_quincenal"] == "2026-06-22"
    assert plan.proximo(bloque, "2026-06-16T12:00")["programado"] == "2026-06-22T07:00"


# ------------------------------------------------------------------ r02 · H-02: disparo huérfano
def _muere(estado, universo_csv):
    """Proceso aparte cuyo C1 muere a mitad (OOM, kill -9): el `finally` no corre."""
    from bloque_a.herramientas.ht01_datos import cargar_universo
    from conftest import nuevo_bloque as nb

    from bloque_a import orquestacion as orq
    from bloque_a import planificacion_c1 as pl
    orq.Reloj = RelojInstalado
    b = nb(estado, cargar_universo(universo_csv))
    b.ciclo = lambda *a, **k: os._exit(9)
    pl.disparar(b, "2026-05-30T06:10")


def test_r02_h02_proceso_muerto_deja_el_disparo_fallido_con_incidencia_y_sin_repetir(tmp_path, universo, monkeypatch):
    from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
    monkeypatch.setattr(orquestacion, "Reloj", RelojInstalado)
    nuevo_bloque(tmp_path, universo)
    p = mp.get_context("spawn").Process(target=_muere, args=(tmp_path, RUTA_UNIVERSO_EJEMPLO))
    p.start()
    p.join(300)
    assert p.exitcode == 9
    b = nuevo_bloque(tmp_path, universo)
    llamadas = _con_ciclo_simulado(b)
    reserva = b.almacen.estado("F5")["C1-EJEC-2026-05-30T06:00"]
    assert reserva["pid"] != os.getpid() and "estado_run" not in reserva
    r = plan.disparar(b, "2026-05-30T07:10")
    assert r["estado"] == "FALLIDO" and r["motivo"] == "proceso terminado" and not llamadas
    f5 = b.almacen.estado("F5")["C1-EJEC-2026-05-30T06:00"]
    # cierre (H-08): se lee como un ciclo cortado, con `estado_run` arriba y el motivo
    assert f5["estado_run"] == "FALLIDO" and f5["motivo_cierre"] == "proceso terminado" and f5["run_id"] is None
    inc = [e for e in b.almacen.leer("HA") if e.get("disparo_huerfano") == "C1-EJEC-2026-05-30T06:00"]
    assert len(inc) == 1 and inc[0]["severidad"] == "Operativa"
    r = plan.disparar(b, "2026-05-30T08:10")                    # una sola vez: ni otra incidencia ni otro C1
    assert r["estado"] == "DESCARTADO_DUPLICADO" and r["estado_run"] == "FALLIDO" and not llamadas
    assert len([e for e in b.almacen.leer("HA") if e.get("disparo_huerfano")]) == 1


def test_r02_h02_proceso_vivo_da_en_curso_sin_escribir(bloque):
    vistos = []

    def ciclo(as_of=None, disparador=None, **kw):   # mientras el C1 corre, otro sondeo del mismo proceso (vivo)
        n = (len(bloque.almacen.leer("F5")), len(bloque.almacen.leer("HA")))
        vistos.append((plan.disparar(bloque, "2026-05-30T06:30")["estado"], n,
                       (len(bloque.almacen.leer("F5")), len(bloque.almacen.leer("HA")))))
        return {"run_id": "RUN-SIM-1", "estado": "COMPLETO"}

    bloque.ciclo = ciclo
    assert plan.disparar(bloque, "2026-05-30T06:10")["estado"] == "EMITIDO"
    assert vistos[0][0] == "EN_CURSO" and vistos[0][1] == vistos[0][2]
    reserva = bloque.almacen.estado("F5")["C1-EJEC-2026-05-30T06:00"]
    assert reserva["pid"] == os.getpid() and reserva["boot_id"] and isinstance(reserva["arranque_proceso"], int)
    assert reserva["estado_run"] == "COMPLETO" and "C1-EJEC-2026-05-30T06:00" not in plan._ABIERTOS


# ------------------------------------------------------------------ ronda de cierre de la QA r02 · H-07: pid reutilizado
def _reserva_ajena(b, **identidad):
    b.almacen.reloj.fijar("2026-05-30")
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "DISPARO", "id": "C1-EJEC-2026-05-30T06:00", "ciclo": "C1", "origen": "HT-05",
                                       "fecha_disparo": "2026-05-30T06:10", "programado": "2026-05-30T06:00",
                                       "entrega": "2026-06-01T07:00", "p01": ht05.P01_INICIAL, "cfg_id": None,
                                       "estado": "EMITIDO", "run_id": None, **identidad})


def test_cierre_h07_pid_propio_que_este_proceso_no_abrio_cuenta_como_muerto(bloque):
    _reserva_ajena(bloque, pid=os.getpid(), **plan.identidad_proceso(os.getpid()))   # otro arranque con nuestro pid
    llamadas = _con_ciclo_simulado(bloque)
    r = plan.disparar(bloque, "2026-05-30T07:10")
    assert r["estado"] == "FALLIDO" and not llamadas
    assert bloque.almacen.estado("F5")["C1-EJEC-2026-05-30T06:00"]["estado_run"] == "FALLIDO"


def test_cierre_h07_pid_vivo_de_otro_proceso_con_otra_hora_de_arranque_cuenta_como_muerto(bloque):
    import subprocess
    ajeno = subprocess.Popen(["sleep", "60"])
    try:
        ident = plan.identidad_proceso(ajeno.pid)
        assert ident["arranque_proceso"] is not None
        _reserva_ajena(bloque, pid=ajeno.pid, **dict(ident, arranque_proceso=ident["arranque_proceso"] - 1))
        llamadas = _con_ciclo_simulado(bloque)
        assert plan.disparar(bloque, "2026-05-30T07:10")["estado"] == "FALLIDO" and not llamadas
    finally:
        ajeno.kill()
        ajeno.wait()


def test_cierre_h07_pid_vivo_del_mismo_arranque_sigue_en_curso(bloque):
    import subprocess
    ajeno = subprocess.Popen(["sleep", "60"])
    try:
        _reserva_ajena(bloque, pid=ajeno.pid, **plan.identidad_proceso(ajeno.pid))
        llamadas = _con_ciclo_simulado(bloque)
        n = len(bloque.almacen.leer("F5"))
        assert plan.disparar(bloque, "2026-05-30T07:10")["estado"] == "EN_CURSO" and not llamadas
        assert len(bloque.almacen.leer("F5")) == n
        otro_arranque = dict(plan.identidad_proceso(ajeno.pid), boot_id="00000000-0000-0000-0000-000000000000")
        _reserva_ajena(bloque, pid=ajeno.pid, **otro_arranque)                         # otro boot_id: muerto
        assert plan.disparar(bloque, "2026-05-30T07:20")["estado"] == "FALLIDO"
    finally:
        ajeno.kill()
        ajeno.wait()


# ------------------------------------------------------------------ r02 · H-03: la orden de la CLI
def test_r02_h03_orden_planificar_de_la_cli(tmp_path, monkeypatch, capsys):
    from bloque_a import cli
    monkeypatch.setattr(orquestacion, "Reloj", RelojInstalado)
    base = ["--cliente", "mock", "--datos", str(DATOS), "--estado", str(tmp_path / "estado"), "--salida", str(tmp_path / "ent"),
            "--as-of", "2026-05-30T06:10", "planificar"]

    def orden(*extra):
        assert cli.main(base + list(extra)) == 0
        return json.loads(capsys.readouterr().out)

    r = orden()
    assert r["estado"] == "PENDIENTE" and r["disparo"]["disparo_id"] == "C1-EJEC-2026-05-30T06:00"
    f5 = tmp_path / "estado" / "F5_historial_analisis.jsonl"
    assert not f5.exists() or '"DISPARO"' not in f5.read_text(encoding="utf-8")
    r = orden("--ejecutar")
    assert r["estado"] == "EMITIDO" and r["run_id"].startswith("RUN-") and r["estado_run"]
    assert '"DISPARO"' in f5.read_text(encoding="utf-8")
    assert orden("--ejecutar")["estado"] == "DESCARTADO_DUPLICADO"


# ------------------------------------------------------------------ r02 · H-06: cláusulas sin prueba (mutantes del revisor)
def test_r02_h06_r3_cambio_que_rige_el_dia_del_c1_antiguo(bloque):
    bloque.decision(CT04, "2026-06-05")                          # efecto el sábado 06-06, el día del C1 semanal antiguo
    assert plan.proximo(bloque, "2026-06-05T12:00")["programado"] == "2026-06-08T07:00"


def test_r02_h06_r6_a_la_hora_exacta_de_la_entrega_es_recuperado(bloque):
    _con_ciclo_simulado(bloque)
    assert plan.disparar(bloque, "2026-06-01T07:00")["estado"] == "RECUPERADO"


def test_r02_h06_r7_mensual_el_dia_7():
    inicio = dt.date(2026, 11, 1)
    assert ht05.siguiente_ejecucion(dt.datetime(2026, 11, 1), "MENSUAL", "SAB 06:00", inicio) == dt.datetime(2026, 11, 7, 6)


def test_r02_h06_r8_disparo_a_su_minuto_exacto(bloque):
    _con_ciclo_simulado(bloque)
    r = plan.disparar(bloque, "2026-05-30T06:00")
    assert r["estado"] == "EMITIDO" and r["disparo"]["disparo_id"] == "C1-EJEC-2026-05-30T06:00"


def test_r02_h06_r9_la_entrega_diaria_es_la_del_mismo_dia():
    assert ht05.entrega_de(dt.datetime(2026, 6, 9, 5), "DIARIA", "LUN 07:00") == dt.datetime(2026, 6, 9, 7)


def test_r02_h06_r10_lo_que_f10_aun_no_sabe_no_cuenta(bloque):
    bloque.decision(CT04, "2026-06-02")                          # QUINCENAL desde el 03-06
    bloque.almacen.reloj.fijar("2026-06-05")                     # cambio conocido el 05-06, con efecto (retroactivo) 03-06
    bloque.almacen.escribir("F10", "AG-01", {"tipo_entrada": "CFG", "cfg_id": "CFG-2026-0903", "param_id": "P-01",
                                             "valor_vigente": ht05.P01_INICIAL, "autor": "AG-01", "fecha_efecto": "2026-06-03"})
    assert plan.proximo(bloque, "2026-06-02T10:00")["programado"] == "2026-06-08T07:00"


def test_r02_h06_r11_los_segundos_no_cuentan(bloque):
    _con_ciclo_simulado(bloque)
    assert plan.disparar(bloque, "2026-06-02T07:00:30")["estado"] == "RECUPERADO"   # entrega + 24 h + 30 s


def test_r02_h06_r14_diaria_a_medianoche_admitida():
    cfg = dict(parametro(None, "planificador"), franja_sin_disparos_h=[3, 4])       # para que la entrega 02:00 valga (H-04)
    assert ht05.ejecucion_para_entrega("DIARIA", "LUN 02:00", cfg) == "LUN 00:00"


def test_r02_h06_r15_el_planificador_deduce_la_ejecucion_del_p01_de_dos_partes(bloque):
    bloque.almacen.reloj.fijar("2026-06-01")
    bloque.almacen.escribir("F10", "AG-01", {"tipo_entrada": "CFG", "cfg_id": "CFG-2026-0904", "param_id": "P-01",
                                             "valor_vigente": "QUINCENAL · MIE 08:00", "autor": "AG-01", "fecha_efecto": "2026-06-02"})
    assert plan.proximo(bloque, "2026-06-02T10:00")["programado"] == "2026-06-08T07:00"


def test_r02_h06_r16_el_disparo_lleva_la_fecha_del_dia_del_disparo(bloque):
    _con_ciclo_simulado(bloque)
    plan.disparar(bloque, "2026-05-30T06:10")
    assert {e["_fecha"] for e in _disparos(bloque)} == {"2026-05-30"}


# ------------------------------------------------------------------ segunda ronda de cierre de la QA r02 · H-09 y H-10
def test_cierre2_h09_arranque_proceso_es_la_hora_de_arranque_del_proceso():
    import subprocess
    with open("/proc/stat", encoding="utf-8") as f:
        btime = next(int(linea.split()[1]) for linea in f if linea.startswith("btime "))
    antes = time.time()
    hijo = subprocess.Popen(["sleep", "60"])
    try:
        arranque = plan.identidad_proceso(hijo.pid)["arranque_proceso"]
        assert abs(btime + arranque / os.sysconf("SC_CLK_TCK") - antes) < 2
        primera = plan.identidad_proceso(os.getpid())
        reserva = bytearray(64 * 1024 * 1024)   # el tamaño del proceso cambia; su hora de arranque, no
        assert plan.identidad_proceso(os.getpid()) == primera and len(reserva)
    finally:
        hijo.kill()
        hijo.wait()


def _sin_poder_saberlo(bloque, identidad, monkeypatch=None):
    """Reserva abierta de un proceso vivo ajeno (un `sleep`) de la que no se puede comprobar la identidad: falla cerrado con
    DESCARTADO_DUPLICADO, sin escribir en F5 ni en HA y sin C1 (ni un C1 doble ni un huérfano falso)."""
    import subprocess
    ajeno = subprocess.Popen(["sleep", "60"])
    try:
        _reserva_ajena(bloque, pid=ajeno.pid, **identidad(ajeno.pid))
        if monkeypatch is not None:
            monkeypatch.setattr(plan, "RUTA_BOOT_ID", "/no/existe/boot_id")   # la identidad actual ya no se puede leer
        llamadas = _con_ciclo_simulado(bloque)
        n = (len(bloque.almacen.leer("F5")), len(bloque.almacen.leer("HA")))
        r = plan.disparar(bloque, "2026-05-30T07:10")
        assert r["estado"] == "DESCARTADO_DUPLICADO" and not llamadas, r
        assert (len(bloque.almacen.leer("F5")), len(bloque.almacen.leer("HA"))) == n
    finally:
        ajeno.kill()
        ajeno.wait()


def test_cierre2_h10_boot_id_ilegible_no_se_puede_saber(bloque, monkeypatch):
    _sin_poder_saberlo(bloque, plan.identidad_proceso, monkeypatch)       # reserva completa; el boot_id de ahora, ilegible


def test_cierre2_h10_reserva_sin_identidad_no_se_puede_saber(bloque):
    _sin_poder_saberlo(bloque, lambda pid: {})                             # reserva anterior al cierre: solo el pid
