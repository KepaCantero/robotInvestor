import datetime as dt
from types import SimpleNamespace

import pytest
from bloque_b.evaluador import metricas


@pytest.mark.parametrize(("sesiones_entre_cortes", "esperados"), [(1, 3), (10, 30)])
def test_certificado_cuenta_periodos_sin_solapar(sesiones_entre_cortes, esperados):
    registros = {}
    for i in range(30):
        inicio = dt.date(2020, 1, 1) + dt.timedelta(days=i * sesiones_entre_cortes)
        registros[i] = {"tipo": "RANKING", "celda": "SEL-RV×H4", "estado": "RESUELTO",
                        "fecha_emision": inicio.isoformat(), "fecha_resolucion": (inicio + dt.timedelta(days=10)).isoformat(),
                        "resolucion": {"acierto": True, "exceso": 0.02, "ic_rango": 0.7}}
    # Una fila histórica sin fechas no aporta una ventana de evaluación verificable.
    registros[30] = {k: v for k, v in registros[0].items() if k != "fecha_emision"}
    ent = SimpleNamespace(cfg={}, alm=SimpleNamespace(estado=lambda _: registros))
    resultado = metricas(ent)
    assert bool(resultado["certificados"]) == (esperados == 30)
    celda = resultado["celdas"]["RANKING|SEL-RV×H4"]
    assert celda["n"] == 31
    assert celda["certificacion_ranking"]["n_sin_solapamiento"] == esperados
