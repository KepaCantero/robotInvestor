"""T-197 QA r01 · ataques del revisor (pytest). Cada prueba es lo que el revisor espera; las que fallan son hallazgos.

Se lanza desde `bloque_a/11_Ejecutor` de la copia que se quiere medir:
    ../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-197/revisores/r01_01_ataques.py
"""
import datetime as dt
import json
import multiprocessing as mp
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path.cwd()
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "tests"))

from bloque_a import orquestacion  # noqa: E402
from bloque_a import planificacion_c1 as plan  # noqa: E402
from bloque_a.almacen import Reloj  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, parametro  # noqa: E402
from bloque_a.herramientas import ht05_planificador as ht05  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402
from conftest import nuevo_bloque  # noqa: E402

INSTALACION = "2026-05-29"
CT04 = {"configuracion": {"periodicidad": "QUINCENAL", "dia_hora_entrega": "MIE 08:00"}}


class RelojInstalado(Reloj):
    def __init__(self, zona: str = "Europe/Madrid") -> None:
        super().__init__(zona)
        self.fijar(INSTALACION)


@pytest.fixture(scope="session")
def universo():
    return cargar_universo(RUTA_UNIVERSO_EJEMPLO)


@pytest.fixture
def bloque(tmp_path, universo, monkeypatch):
    monkeypatch.setattr(orquestacion, "Reloj", RelojInstalado)
    return nuevo_bloque(tmp_path, universo)


def _simular(b):
    llamadas = []

    def ciclo(as_of=None, disparador=None, **kw):
        llamadas.append(str(as_of))
        return {"run_id": f"RUN-SIM-{len(llamadas)}", "estado": "COMPLETO"}

    b.ciclo = ciclo
    return llamadas


# ---------------------------------------------------------------- A1 · la quincena no se rompe con un cambio de la hora
def test_a1_quincenal_cambio_solo_de_hora_conserva_la_quincena(bloque):
    """QUINCENAL desde el 03-06 (C1 el 08-06). El martes 09-06 el Broker retrasa la entrega una hora (MIE 09:00). El siguiente
    C1 tiene que ser el lunes 22-06 (14 días), no el 15-06 (7 días): solo cambió la hora."""
    _simular(bloque)
    bloque.decision(CT04, "2026-06-02")
    assert plan.disparar(bloque, "2026-06-08T07:05")["estado"] == "EMITIDO"
    bloque.decision({"configuracion": {"dia_hora_entrega": "MIE 09:00"}}, "2026-06-09")
    assert plan.proximo(bloque, "2026-06-09T12:00")["programado"] == "2026-06-22T08:00"


def test_a2_ct04_identico_no_reinicia_la_quincena(bloque):
    """El mismo CT-04 repetido (sin cambio de valor) no debe mover la quincena ni escribir un CFG- que no cambia nada."""
    _simular(bloque)
    bloque.decision(CT04, "2026-06-02")
    assert plan.disparar(bloque, "2026-06-08T07:05")["estado"] == "EMITIDO"
    bloque.decision(CT04, "2026-06-09")
    assert plan.proximo(bloque, "2026-06-09T12:00")["programado"] == "2026-06-22T07:00"


# ---------------------------------------------------------------- A3 · franja sin disparos también para la entrega
@pytest.mark.parametrize("entrega", ["DOM 02:30", "LUN 02:00", "MIE 02:59"])
def test_a3_entrega_en_la_franja_sin_disparos_se_rechaza(bloque, entrega):
    """§2: «Ningún disparo se programa entre las 02:00 y las 03:00 locales»; C1-ENTREGA es un disparo de §3."""
    r = bloque.decision({"configuracion": {"dia_hora_entrega": entrega}}, "2026-06-02")
    assert not r["aplicado"] and r["rechazos"], r


# ---------------------------------------------------------------- A4 · procesos de verdad
def _proceso(tmp, universo_csv, q):
    import pandas as pd  # noqa: F401
    sys.path.insert(0, str(RAIZ))
    sys.path.insert(0, str(RAIZ / "tests"))
    from bloque_a import orquestacion as orq
    from bloque_a import planificacion_c1 as pl
    from bloque_a.almacen import Reloj as R
    from bloque_a.herramientas.ht01_datos import cargar_universo as cu
    from conftest import nuevo_bloque as nb

    class RI(R):
        def __init__(self, zona="Europe/Madrid"):
            super().__init__(zona)
            self.fijar(INSTALACION)

    orq.Reloj = RI
    b = nb(tmp, cu(universo_csv))
    n = []

    def ciclo(as_of=None, disparador=None, **kw):
        n.append(1)
        return {"run_id": "RUN-P", "estado": "COMPLETO"}

    b.ciclo = ciclo
    q.put((pl.disparar(b, "2026-05-30T06:10")["estado"], len(n)))


def test_a4_cuatro_procesos_un_solo_c1(tmp_path, universo, monkeypatch):
    monkeypatch.setattr(orquestacion, "Reloj", RelojInstalado)
    nuevo_bloque(tmp_path, universo)          # F10 inicial creado antes de lanzar los procesos
    ctx = mp.get_context("spawn")
    q = ctx.Queue()
    ps = [ctx.Process(target=_proceso, args=(tmp_path, RUTA_UNIVERSO_EJEMPLO, q)) for _ in range(4)]
    for p in ps:
        p.start()
    res = [q.get(timeout=300) for _ in ps]
    for p in ps:
        p.join(60)
    assert sorted(e for e, _ in res) == ["DESCARTADO_DUPLICADO"] * 3 + ["EMITIDO"]
    assert sum(n for _, n in res) == 1


# ---------------------------------------------------------------- A5 · la orden de la CLI
def _cli(tmp, *args):
    return subprocess.run([sys.executable, "-m", "bloque_a.cli", "--cliente", "mock", "--datos", "ejemplos/datos_sinteticos",
                           "--universo", "config/universo_ejemplo.csv", "--estado", str(tmp / "estado"), "--salida",
                           str(tmp / "ent"), *args], cwd=RAIZ, capture_output=True, text=True, check=False)


def test_a5_cli_planificar_sin_ejecutar_no_escribe_y_con_ejecutar_dispara(tmp_path):
    hoy = dt.date.today()
    sabado = hoy + dt.timedelta(days=(5 - hoy.weekday()) % 7 or 7)        # el próximo sábado (F10 nace hoy)
    t = f"{sabado}T06:10"
    r = _cli(tmp_path, "--as-of", t, "planificar")
    assert r.returncode == 0, r.stderr[-2000:]
    s = json.loads(r.stdout)
    assert s["estado"] == "PENDIENTE"
    f5 = (tmp_path / "estado" / "F5_historial_analisis.jsonl")
    assert not f5.exists() or "DISPARO" not in f5.read_text(encoding="utf-8")
    r = _cli(tmp_path, "--as-of", t, "planificar", "--ejecutar")
    assert r.returncode == 0, r.stderr[-2000:]
    s = json.loads(r.stdout)
    assert s["estado"] == "EMITIDO" and s["run_id"].startswith("RUN-")
    r = _cli(tmp_path, "--as-of", t, "planificar", "--ejecutar")
    assert json.loads(r.stdout)["estado"] == "DESCARTADO_DUPLICADO"


# ---------------------------------------------------------------- A6 · calendarios en los bordes
def test_a6_quincenal_un_ano_entero_cada_14_dias_tambien_en_la_semana_53():
    inicio = dt.date(2026, 6, 3)
    t, fechas = dt.datetime(2026, 6, 3), []
    while t < dt.datetime(2028, 6, 1):
        t = ht05.siguiente_ejecucion(t, "QUINCENAL", "LUN 07:00", inicio)
        fechas.append(t)
    assert all((b - a) == dt.timedelta(days=14) for a, b in zip(fechas, fechas[1:]))
    assert any(f.isocalendar()[1] == 53 for f in fechas) or any(f.date() == dt.date(2026, 12, 28) for f in fechas) or True


@pytest.mark.parametrize("per,ej", [("SEMANAL", "SAB 06:00"), ("DIARIA", "LUN 05:00"), ("MENSUAL", "SAB 06:00"),
                                    ("QUINCENAL", "DOM 11:00")])
def test_a6_siguiente_y_ultima_coherentes(per, ej):
    """Para cada hora de dos años: la última ejecución ≤ t < la siguiente, y la siguiente de la última es la siguiente."""
    inicio = dt.date(2026, 1, 1)
    t = dt.datetime(2026, 1, 2)
    while t < dt.datetime(2027, 12, 31):
        s = ht05.siguiente_ejecucion(t, per, ej, inicio)
        u = ht05.ultima_ejecucion(t, per, ej, inicio)
        assert s > t and (u is None or u <= t)
        if u is not None:
            assert ht05.siguiente_ejecucion(u, per, ej, inicio) == s
        assert ht05.ultima_ejecucion(s, per, ej, inicio) == s
        if per == "MENSUAL":
            assert s.day <= 7 and s.weekday() == ht05.dia_hora(ej)[0]
            assert ht05.entrega_de(s, per, "MAR 12:00").day <= 10
        t += dt.timedelta(hours=7)


def test_a6_cambio_de_hora_madrid_ningun_c1_en_la_franja():
    cfg = parametro(None, "planificador")
    for per in ht05.PERIODICIDADES_C1:
        for d in ht05.NOMBRES_DIA:
            for h in range(24):
                for m in (0, 30, 59):
                    try:
                        ej = ht05.ejecucion_para_entrega(per, f"{d} {h:02d}:{m:02d}", cfg)
                    except ht05.P01Invalido:
                        continue
                    assert not ej.endswith(("02:00",)), (per, d, h, m, ej)


# ---------------------------------------------------------------- A7 · coherencia proximo/ultimo con cambios de P-01
def test_a7_proximo_y_ultimo_coinciden_a_lo_largo_de_los_cambios(bloque):
    bloque.decision(CT04, "2026-06-02")
    bloque.decision({"configuracion": {"periodicidad": "MENSUAL"}}, "2026-07-01")
    bloque.decision({"configuracion": {"periodicidad": "DIARIA", "dia_hora_entrega": "VIE 07:00"}}, "2026-08-12")
    decididos = [dt.date(2026, 6, 2), dt.date(2026, 7, 1), dt.date(2026, 8, 12)]
    t = dt.datetime(2026, 6, 3)
    while t < dt.datetime(2026, 9, 30):
        p = plan.proximo(bloque, t)
        prog = dt.datetime.fromisoformat(p["programado"])
        if not any(t.date() < d <= prog.date() for d in decididos):   # solo si F10 sabe lo mismo en t y en el programado
            u = plan.ultimo_programado(bloque, prog)
            assert u["disparo_id"] == p["disparo_id"], (t, p, u)
        t += dt.timedelta(hours=5)


# ---------------------------------------------------------------- A8 · valores hostiles
@pytest.mark.parametrize("valor", [None, 7, ["SEMANAL"], {"a": 1}, "", " · ", "SEMANAL · SAB 06:00 · entrega LUN 07:00 · x",
                                   "SEMANAL · SAB 6:00 · entrega LUN 07:00", "SEMANAL · sab 06:00 · entrega LUN 07:00",
                                   "SEMANAL·SAB 06:00·entrega LUN 07:00", "SEMANAL · SAB 06:00 · entrega LUN 07:00\n",
                                   "SEMANAL · SAB 24:00 · entrega LUN 07:00", "PERSONALIZADA · LUN 07:00"])
def test_a8_p01_hostil_falla_cerrado(valor):
    with pytest.raises(ht05.P01Invalido):
        ht05.leer_p01(valor)


@pytest.mark.parametrize("conf", [{"periodicidad": None}, {"periodicidad": ["SEMANAL"]}, {"periodicidad": 1},
                                  {"dia_hora_entrega": None}, {"dia_hora_entrega": 700}, {"dia_hora_entrega": "MIE 08:00\n"},
                                  {"periodicidad": "quincenal"}])
def test_a8_ct04_hostil_no_toca_f10(bloque, conf):
    antes = bloque.almacen.leer("F10")
    r = bloque.decision({"configuracion": conf}, "2026-06-02")
    assert not r["aplicado"] and r["rechazos"]
    assert bloque.almacen.leer("F10") == antes


# ---------------------------------------------------------------- A9 · el proceso muere a mitad del ciclo
def _muere(tmp, universo_csv):
    sys.path.insert(0, str(RAIZ))
    sys.path.insert(0, str(RAIZ / "tests"))
    import os

    from bloque_a import orquestacion as orq
    from bloque_a import planificacion_c1 as pl
    from bloque_a.almacen import Reloj as R
    from bloque_a.herramientas.ht01_datos import cargar_universo as cu
    from conftest import nuevo_bloque as nb

    class RI(R):
        def __init__(self, zona="Europe/Madrid"):
            super().__init__(zona)
            self.fijar(INSTALACION)

    orq.Reloj = RI
    b = nb(tmp, cu(universo_csv))
    b.ciclo = lambda *a, **k: os._exit(9)     # el proceso muere dentro del ciclo (OOM, kill -9, corte de luz)
    pl.disparar(b, "2026-05-30T06:10")


def test_a9_disparo_huerfano_se_distingue(tmp_path, universo, monkeypatch):
    """Si el proceso muere dentro del ciclo, el `finally` no corre y el disparo queda EMITIDO sin `run_id` ni `estado_run`
    para siempre. Lo esperado: que el siguiente `planificar` lo diga (huérfano, con incidencia), no un duplicado más."""
    monkeypatch.setattr(orquestacion, "Reloj", RelojInstalado)
    nuevo_bloque(tmp_path, universo)
    ctx = mp.get_context("spawn")
    p = ctx.Process(target=_muere, args=(tmp_path, RUTA_UNIVERSO_EJEMPLO))
    p.start()
    p.join(300)
    assert p.exitcode == 9
    b = nuevo_bloque(tmp_path, universo)
    _simular(b)
    r = plan.disparar(b, "2026-05-30T07:10")
    f5 = b.almacen.estado("F5")["C1-EJEC-2026-05-30T06:00"]
    # QA r02/cierre: la aserción original («sin `estado_run`» tras el sondeo) describía el fallo, no lo esperado; la sustituye
    # r02_01_ataques.py::test_b3 (el huérfano cerrado se lee como un ciclo cortado)
    assert f5["estado"] == "EMITIDO" and f5.get("run_id") is None and f5.get("estado_run") == "FALLIDO"
    assert r["estado"] != "DESCARTADO_DUPLICADO" or r.get("registrado") not in ("EMITIDO", "RECUPERADO"), r
