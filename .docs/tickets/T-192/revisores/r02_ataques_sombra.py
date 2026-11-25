"""QA r01 (Claude) de T-192, PB-35: cierre del AJU- EN_SOMBRA con DM-HLN.

Uso, desde bloque_a/11_Ejecutor con la venv del repo:
    python ../../.docs/tickets/T-192/revisores/r02_ataques_sombra.py
Siembra en F5 y F4 trimestres de sombra semanales como la prueba del ticket, pero con ruido (varianza no nula) y con la
configuración por defecto. Cada caso imprime OK o FALLO.
"""
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, ".")
sys.path.insert(0, "tests")
from conftest import config_pruebas, nuevo_bloque  # noqa: E402

from bloque_a.herramientas.ht01_datos import ProveedorCSV  # noqa: E402,F401

UNIVERSO = pd.read_csv("config/universo_ejemplo.csv")
fallos = []


def caso(nombre, cond, detalle=""):
    print(("OK    " if cond else "FALLO ") + nombre + (f" · {detalle}" if detalle else ""), flush=True)
    if not cond:
        fallos.append(nombre)


def sembrar(b, semanas, mejora, semilla=1, opps=4, sentido="POSITIVO", romper=None):
    """Trimestre de sombra: cada semana, `opps` opciones con RK anterior y nuevo; la nueva ordena mejor si mejora > 0."""
    rng = np.random.default_rng(semilla)
    alm = b.almacen
    b.fijar_fecha("2026-01-02")
    alm.escribir("F6", "AG-20", {"tipo_entrada": "AJU", "id": "AJU-Q", "parametro": "P-11", "efecto_desde": "2026-01-02",
                                 "sombra_hasta": "2026-04-02", "estado": "EN_SOMBRA", "delta": 0.05})
    for i, fecha in enumerate(pd.date_range("2026-01-09", periods=semanas, freq="7D")):
        b.fijar_fecha(fecha)
        rid = f"RUN-Q{i}"
        y = rng.normal(size=opps)
        ruido = rng.normal(size=opps)
        anterior = (y * (0.5 - mejora) + ruido).tolist()
        nueva = (y * (0.5 + mejora) + ruido).tolist()
        pares = {f"OPP-{i}-{k}": [anterior[k], nueva[k]] for k in range(opps)}
        alm.escribir("F5", "AG-01", {"tipo_entrada": "RUN", "id": rid, "entrega": "ENTREGADA",
                                     "sombra": {"RV": {"aju_id": "AJU-Q", "rk_pareado": pares, "cambios": 0}}})
        for k in range(opps):
            pid, oid = f"PRG-Q{i}-{k}", f"OPP-{i}-{k}"
            alm.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": pid, "opp_id": oid, "clase": "RV", "run_id": rid,
                                         "fecha_emision": str(fecha.date()), "horizonte": "H1", "sentido": sentido, "estado": "ABIERTO"})
            res = {"valor_observado": float(y[k]) * (1 if sentido == "POSITIVO" else -1), "fecha_dato": str(fecha.date()),
                   "comprobacion_fuga": "SUPERADA"}
            if romper and i == 0 and k == 0:
                res = romper(res)
            alm.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": pid, "estado": "RESUELTO", "resolucion": res})
    b.fijar_fecha("2026-04-03")


def nuevo(cfg=None):
    tmp = Path(tempfile.mkdtemp(prefix="qa192_"))
    return nuevo_bloque(tmp, UNIVERSO, cfg=cfg)


# 1. Configuración por defecto (min_calibrar = 30, meses_sombra = 3): un trimestre semanal (13 lecturas) con una mejora clara
b = nuevo()
sembrar(b, 13, mejora=0.45)
c = b.evaluador.cerrar_sombra("2026-04-03")
caso("con la configuración por defecto un trimestre que mejora claramente se CONFIRMA", c and c["estado"] == "CONFIRMADO",
     f"{c and c['estado']} · {c and c.get('motivo_cierre')} · fechas={c and len(c.get('fechas_pareadas', []))}")

# 2. Con la muestra mínima rebajada, la dirección del DM-HLN: mejora clara → CONFIRMADO; empeora clara → REVERTIDO con p < 0,10
for mejora, esperado in ((0.45, "CONFIRMADO"), (-0.45, "REVERTIDO")):
    b = nuevo(config_pruebas(evaluacion={"min_calibrar": 3}))
    sembrar(b, 13, mejora=mejora)
    c = b.evaluador.cerrar_sombra("2026-04-03")
    caso(f"mejora {mejora:+}: {esperado}", c and c["estado"] == esperado,
         f"{c and c['estado']} · p={c and (c.get('dm_hln') or {}).get('p_unilateral')} · ic {c and c.get('ic_anterior')} → {c and c.get('ic_nueva')}")

# 3. Pronósticos NEGATIVOS: el signo del resultado se invierte y la conclusión no cambia
b = nuevo(config_pruebas(evaluacion={"min_calibrar": 3}))
sembrar(b, 13, mejora=0.45, sentido="NEGATIVO")
c = b.evaluador.cerrar_sombra("2026-04-03")
caso("sentido NEGATIVO: CONFIRMADO igual", c and c["estado"] == "CONFIRMADO", f"{c and c['estado']}")

# 4. Registro conforme al esquema F6 V2.0 (4.x AJU-): resultado_sombra {metrica_nueva, metrica_anterior, dm_hln_p,
#    decisiones_top3_cambiadas, decision}
b = nuevo(config_pruebas(evaluacion={"min_calibrar": 3}))
sembrar(b, 13, mejora=0.45)
c = b.evaluador.cerrar_sombra("2026-04-03")
rs = (c or {}).get("resultado_sombra") or {}
caso("AJU- cerrado con resultado_sombra del esquema F6 V2.0",
     {"metrica_nueva", "metrica_anterior", "dm_hln_p", "decisiones_top3_cambiadas", "decision"} <= set(rs),
     f"claves escritas: {sorted(k for k in (c or {}) if not k.startswith('_'))}")

# 5. Un registro histórico incompleto (resolución sin valor_observado) no tumba el C5
b = nuevo(config_pruebas(evaluacion={"min_calibrar": 3}))
sembrar(b, 13, mejora=0.45, romper=lambda r: {k: v for k, v in r.items() if k != "valor_observado"})
try:
    c = b.evaluador.cerrar_sombra("2026-04-03")
    caso("resolución sin valor_observado: la sombra se cierra sin excepción", c is not None, f"{c and c['estado']}")
except Exception as e:  # noqa: BLE001
    caso("resolución sin valor_observado: la sombra se cierra sin excepción", False, repr(e))

# 6. Antes de sombra_hasta no se cierra; el día exacto sí; dos veces, una sola
b = nuevo(config_pruebas(evaluacion={"min_calibrar": 3}))
sembrar(b, 13, mejora=0.45)
caso("el día anterior a sombra_hasta no se cierra", b.evaluador.cerrar_sombra("2026-04-01") is None)
c1 = b.evaluador.cerrar_sombra("2026-04-02")
c2 = b.evaluador.cerrar_sombra("2026-04-03")
caso("el día de sombra_hasta se cierra y no se repite", c1 is not None and c2 is None)

print(f"\n{len(fallos)} fallo(s): {fallos}")
