"""QA r02 de T-177 · H-03 (concurrencia entre procesos de verdad) y H-07 (tope semanal de 3 UC del BFA).

Ejecutar desde bloque_a/11_Ejecutor:
  python -m pytest -q -s -p no:cacheprovider ../../.docs/tickets/T-177/revisores/r02_concurrencia_presupuesto.py"""
import importlib
import json
import subprocess
import sys
import threading
from pathlib import Path

import pandas as pd
import pytest

EJ = Path(__file__).resolve().parents[4] / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJ / "tests"))
from conftest import AS_OF, config_pruebas, nuevo_bloque, universo  # noqa: E402,F401

mc4 = importlib.import_module("bloque_a.mantenimiento_c4")
FICHA = {"servicio": "API de fondos cerrados", "uso_previsto": "Cribado de FON", "impacto_si_falta": "Datos públicos"}


def _cfg(tmp, n=1):
    servicios = [{**FICHA, "servicio": f"API de fondos cerrados {i}"} for i in range(n)]
    p = Path(tmp) / "c4.yaml"
    p.write_text(json.dumps({"credenciales": {"servicios_bfa": servicios}}), encoding="utf-8")   # JSON es YAML válido
    return p


def _cli(tmp, as_of, cfg):
    return subprocess.Popen([sys.executable, "-m", "bloque_a.cli", "--cliente", "mock", "--config", str(cfg), "--datos",
                             "ejemplos/datos_sinteticos", "--estado", str(Path(tmp) / "estado"), "--salida",
                             str(Path(tmp) / "salida"), "--as-of", as_of, "credencial", "c4"],
                            cwd=EJ, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def _f5(tmp):
    filas = [json.loads(x) for x in (Path(tmp) / "estado" / "F5_historial_analisis.jsonl").read_text().splitlines() if x]
    return filas


@pytest.mark.parametrize("ronda", range(4))
def test_r02_h03_cuatro_procesos_a_la_vez(tmp_path, ronda):
    """Cuatro `bloque-a credencial c4` lanzados a la vez sobre el mismo estado, con tres servicios: tres CRD- y tres CT-25."""
    cfg = _cfg(tmp_path, 3)
    procs = [_cli(tmp_path, "2024-03-01", cfg) for _ in range(4)]
    salidas = [p.communicate(timeout=300) for p in procs]
    assert all(p.returncode == 0 for p in procs), [s[1][-500:] for s in salidas]
    crd = {}
    for f in _f5(tmp_path):
        if f.get("tipo_entrada") == "CRD":
            crd.setdefault(f["id"], f)
    ct25 = {c.get("msg_id") for c in crd.values()}   # cada CRD- guarda el msg_id de su CT-25
    from bloque_a.almacen import Almacen
    integ = Almacen(tmp_path / "estado").verificar_integridad("F5")
    print(f"ronda {ronda}: CRD distintas {len(crd)}, CT-25 distintos {len(ct25)}, integridad F5 {integ}",
          sorted(json.loads(s[0])["estado_retorno"] for s in salidas))
    assert len(crd) == 3 and len(ct25) == 3 and all(integ.values())


def test_r02_h07_tope_semanal_y_borde(tmp_path, universo):
    """Varias C4 con servicios distintos (sin acierto de caché) la misma semana: el gasto de la semana no pasa de 3 UC;
    a los 7 días exactos la C4 del día 0 ya no cuenta (ventana (as_of-7, as_of])."""
    tope = 3.0
    hechas = []
    b = None
    for i in range(40):
        cfg = config_pruebas(credenciales={"servicios_bfa": [{**FICHA, "servicio": f"API {i}"}]})
        b = nuevo_bloque(tmp_path, universo, cfg=cfg)
        r = mc4.mantenimiento_c4(b, AS_OF)
        hechas.append((r["estado_retorno"], r["uc"]))
        if r["estado_retorno"] == "SIN_PRESUPUESTO":
            break
    gastado = mc4.uc_c4_semana(b, AS_OF)
    print("C4 del día:", hechas[:3], "…", hechas[-2:], "gastado", gastado)
    assert hechas[-1][0] == "SIN_PRESUPUESTO" and gastado <= tope + 1e-9
    d6 = str((pd.Timestamp(AS_OF) + pd.Timedelta(days=6)).date())
    d7 = str((pd.Timestamp(AS_OF) + pd.Timedelta(days=7)).date())
    assert mc4.mantenimiento_c4(b, d6)["estado_retorno"] == "SIN_PRESUPUESTO"
    r7 = mc4.mantenimiento_c4(b, d7)
    print("día +7:", r7["estado_retorno"], r7["uc_semana_disponible"])
    assert r7["estado_retorno"] != "SIN_PRESUPUESTO" and r7["uc_semana_disponible"] == tope


def test_r02_h07_carrera_del_presupuesto(tmp_path, universo, monkeypatch):
    """Dos C4 a la vez leen el gasto de la semana antes de que ninguna escriba su C4-: ¿pueden gastar entre las dos más
    de la bolsa semanal?"""
    cfg = config_pruebas(credenciales={"servicios_bfa": [FICHA]},
                         mantenimiento_c4={"presupuesto_uc_semana": {"BFA": 3}})
    b0 = nuevo_bloque(tmp_path, universo, cfg=cfg)
    r0 = mc4.mantenimiento_c4(b0, AS_OF)
    coste = r0["uc"]
    assert coste > 0
    # bolsa de modo que quede sitio para una llamada y no para dos
    bolsa = 3.0
    restante_objetivo = 2.5   # cabe la reserva del peor caso de una llamada (≈1,9 UC con el simulado)
    # se llena la semana con C4- ficticias hasta dejar `restante_objetivo` (escritas como las escribe el código)
    b0.almacen.escribir("F5", "AG-01", {"tipo_entrada": "C4_CREDENCIALES", "id": b0.almacen.nuevo_id("C4"), "agente": "AG-16",
                                        "fecha": AS_OF, "uc": round(bolsa - coste - restante_objetivo, 6)})
    # r03 (adaptada por la implementación): `uc_c4_semana` se lee ahora dentro de la transacción y la C4 reserva lo que queda,
    # así que una barrera entre las dos lecturas no se puede cumplir (la segunda espera a la transacción). Se ensancha la
    # ventana con una espera, que es lo que la barrera buscaba
    import time
    orig = mc4.uc_c4_semana

    def lento(bloque, as_of):
        v = orig(bloque, as_of)
        time.sleep(0.5)
        return v
    monkeypatch.setattr(mc4, "uc_c4_semana", lento)
    res = []
    bs = [nuevo_bloque(tmp_path, universo, cfg=config_pruebas(
        credenciales={"servicios_bfa": [{**FICHA, "servicio": f"API carrera {i}"}]})) for i in range(2)]
    hilos = [threading.Thread(target=lambda b=b: res.append(mc4.mantenimiento_c4(b, AS_OF))) for b in bs]
    [h.start() for h in hilos]
    [h.join(120) for h in hilos]
    gastado = orig(bs[0], AS_OF)
    print("carrera:", [(r["estado_retorno"], r["uc"]) for r in res], "gastado en la semana", round(gastado, 4), "bolsa", bolsa)
    # r03: entre las dos no se pasa de la bolsa, y solo una llama (la otra ve la reserva y queda SIN_PRESUPUESTO)
    assert len(res) == 2 and gastado <= bolsa + 1e-9
    assert sorted(r["estado_retorno"] for r in res) == ["COMPLETO", "SIN_PRESUPUESTO"]
