"""T-197 QA r02 · ataques nuevos del revisor sobre las correcciones de la r02 (pytest). Las que fallan son hallazgos.

Se lanza desde `bloque_a/11_Ejecutor` de la copia que se quiere medir:
    ../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-197/revisores/r02_01_ataques.py
"""
import multiprocessing as mp
import os
import sys
from pathlib import Path

import pytest

RAIZ = Path.cwd()
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "tests"))

from bloque_a import orquestacion  # noqa: E402
from bloque_a import planificacion_c1 as plan  # noqa: E402
from bloque_a.almacen import Reloj  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402
from conftest import nuevo_bloque  # noqa: E402

INSTALACION = "2026-05-29"
CT04 = {"configuracion": {"periodicidad": "QUINCENAL", "dia_hora_entrega": "MIE 08:00"}}
ID = "C1-EJEC-2026-05-30T06:00"


class RelojInstalado(Reloj):
    def __init__(self, zona: str = "Europe/Madrid") -> None:
        super().__init__(zona)
        self.fijar(INSTALACION)


@pytest.fixture(scope="session")
def universo():
    return cargar_universo(RUTA_UNIVERSO_EJEMPLO)


def _proceso(tmp, universo_csv, espera_s, q):
    sys.path.insert(0, str(RAIZ))
    sys.path.insert(0, str(RAIZ / "tests"))
    import time

    from bloque_a import orquestacion as orq
    from bloque_a import planificacion_c1 as pl
    from bloque_a.herramientas.ht01_datos import cargar_universo as cu
    from conftest import nuevo_bloque as nb
    orq.Reloj = RelojInstalado
    b = nb(tmp, cu(universo_csv))
    n = []

    def ciclo(as_of=None, disparador=None, **kw):
        n.append(1)
        time.sleep(espera_s)
        return {"run_id": "RUN-P", "estado": "COMPLETO"}

    b.ciclo = ciclo
    q.put((pl.disparar(b, "2026-05-30T06:10")["estado"], len(n)))


def _cuatro(tmp, espera_s):
    ctx = mp.get_context("spawn")
    q = ctx.Queue()
    ps = [ctx.Process(target=_proceso, args=(tmp, RUTA_UNIVERSO_EJEMPLO, espera_s, q)) for _ in range(4)]
    for p in ps:
        p.start()
    res = [q.get(timeout=300) for _ in ps]
    for p in ps:
        p.join(60)
    return res


# ---------------------------------------------------------------- B1 · A4 en cualquier orden de llegada
@pytest.mark.parametrize("ronda", range(4))
@pytest.mark.parametrize("espera_s", [0.0, 3.0])
def test_b1_cuatro_procesos_cualquier_orden_un_solo_c1_y_ningun_falso_huerfano(tmp_path, universo, monkeypatch, ronda, espera_s):
    """Con un C1 instantáneo o lento, en cualquier orden: un EMITIDO; los demás EN_CURSO (llegan con el C1 abierto) o
    DESCARTADO_DUPLICADO (llegan con él cerrado); nunca FALLIDO ni una incidencia de huérfano."""
    monkeypatch.setattr(orquestacion, "Reloj", RelojInstalado)
    nuevo_bloque(tmp_path, universo)
    res = _cuatro(tmp_path, espera_s)
    estados = sorted(e for e, _ in res)
    assert estados.count("EMITIDO") == 1 and set(estados) <= {"EMITIDO", "EN_CURSO", "DESCARTADO_DUPLICADO"}, estados
    assert sum(n for _, n in res) == 1
    b = nuevo_bloque(tmp_path, universo)
    assert not [e for e in b.almacen.leer("HA") if e.get("disparo_huerfano")]
    f5 = b.almacen.estado("F5")[ID]
    assert f5["estado_run"] == "COMPLETO" and not f5.get("cierre_huerfano")
    if espera_s:
        assert estados.count("EN_CURSO") == 3, estados


# ---------------------------------------------------------------- B2 · el pid de la reserva lo reutiliza otro proceso
def test_b2_pid_reutilizado_no_deja_el_disparo_en_curso_para_siempre(tmp_path, universo, monkeypatch):
    """Tras un reinicio del contenedor los pid se repiten: el `planificar` del cron puede tener el mismo pid que el proceso
    muerto que dejó la reserva abierta. Aquí, la reserva la dejó otro proceso (otro arranque) con nuestro pid. Esperado:
    FALLIDO (huérfano), no EN_CURSO para siempre."""
    monkeypatch.setattr(orquestacion, "Reloj", RelojInstalado)
    b = nuevo_bloque(tmp_path, universo)
    b.almacen.reloj.fijar("2026-05-30")
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "DISPARO", "id": ID, "ciclo": "C1", "origen": "HT-05",
                                       "fecha_disparo": "2026-05-30T06:10", "programado": "2026-05-30T06:00",
                                       "entrega": "2026-06-01T07:00", "p01": "SEMANAL · SAB 06:00 · entrega LUN 07:00",
                                       "cfg_id": None, "estado": "EMITIDO", "run_id": None, "pid": os.getpid()})
    b2 = nuevo_bloque(tmp_path, universo)       # otro arranque: no abrió ese C1
    b2.ciclo = lambda *a, **k: {"run_id": "RUN-X", "estado": "COMPLETO"}
    r = plan.disparar(b2, "2026-05-30T07:10")
    assert r["estado"] != "EN_CURSO", r


# ---------------------------------------------------------------- B3 · el cierre del huérfano en el mismo campo que el corte
def _muere(tmp, universo_csv):
    sys.path.insert(0, str(RAIZ))
    sys.path.insert(0, str(RAIZ / "tests"))
    from bloque_a import orquestacion as orq
    from bloque_a import planificacion_c1 as pl
    from bloque_a.herramientas.ht01_datos import cargar_universo as cu
    from conftest import nuevo_bloque as nb
    orq.Reloj = RelojInstalado
    b = nb(tmp, cu(universo_csv))
    b.ciclo = lambda *a, **k: os._exit(9)
    pl.disparar(b, "2026-05-30T06:10")


def test_b3_huerfano_cerrado_con_estado_run_como_el_ciclo_cortado(tmp_path, universo, monkeypatch):
    """Sustituye la última aserción de r01 A9 (que pedía, mal, que no hubiera `estado_run` después del sondeo): el disparo
    huérfano cerrado y el ciclo cortado se leen igual en F5, con `estado_run` FALLIDO."""
    monkeypatch.setattr(orquestacion, "Reloj", RelojInstalado)
    nuevo_bloque(tmp_path, universo)
    p = mp.get_context("spawn").Process(target=_muere, args=(tmp_path, RUTA_UNIVERSO_EJEMPLO))
    p.start()
    p.join(300)
    assert p.exitcode == 9
    b = nuevo_bloque(tmp_path, universo)
    b.ciclo = lambda *a, **k: pytest.fail("no se repite")
    assert plan.disparar(b, "2026-05-30T07:10")["estado"] == "FALLIDO"
    assert b.almacen.estado("F5")[ID].get("estado_run") == "FALLIDO"


# ---------------------------------------------------------------- B4 · sin cambio junto a un cambio real
def test_b4_sin_cambio_de_p01_con_otro_parametro(tmp_path, universo, monkeypatch):
    monkeypatch.setattr(orquestacion, "Reloj", RelojInstalado)
    b = nuevo_bloque(tmp_path, universo)
    b.decision(CT04, "2026-06-02")
    r = b.decision({"configuracion": {**CT04["configuracion"], "clases_activas": ["DIV", "RV"]}}, "2026-06-09")
    assert list(r["aplicado"]) == ["P-02"] and r["sin_cambio"] == ["P-01"] and not r["rechazos"]
    cfg = [e for e in b.almacen.leer("F10") if e.get("tipo_entrada") == "CFG" and e["param_id"] == "P-01"]
    assert len(cfg) == 1


def test_b5_quincenal_anterior_a_r02_conserva_su_ancla(tmp_path, universo, monkeypatch):
    """Un CFG- quincenal escrito antes de la r02 (sin `semana_ancla_quincenal`) y un cambio de hora después: la quincena
    sigue la de su primera ejecución (08-06), no se reinicia."""
    monkeypatch.setattr(orquestacion, "Reloj", RelojInstalado)
    b = nuevo_bloque(tmp_path, universo)
    b.almacen.reloj.fijar("2026-06-02")
    b.almacen.escribir("F10", "AG-01", {"tipo_entrada": "CFG", "cfg_id": "CFG-2026-0950", "param_id": "P-01",
                                        "valor_vigente": "QUINCENAL · LUN 07:00 · entrega MIE 08:00", "autor": "AG-01",
                                        "fecha_efecto": "2026-06-03"})
    b.decision({"configuracion": {"dia_hora_entrega": "MIE 09:00"}}, "2026-06-09")
    assert plan.proximo(b, "2026-06-09T12:00")["programado"] == "2026-06-22T08:00"
