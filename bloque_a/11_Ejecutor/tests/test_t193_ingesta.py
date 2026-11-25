from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from bloque_a.herramientas.ht08_monitor import Monitor
from conftest import AS_OF, nuevo_bloque


def test_abrir_por_tiempo_y_cerrar_con_histeresis():
    reloj = [0.0]
    m = Monitor(objetivo_ingesta_s=1, reloj=lambda: reloj[0])
    m.encolar("AG-12")
    t = m.inicio("AG-12")
    reloj[0] = 3.
    m.fin("AG-12", t)
    orden, = m.evaluar_instancias()
    assert orden["accion"] == "ABRIR" and orden["metricas_disparo"]["W"] == 3.
    m.encolar("AG-12")
    t = m.inicio("AG-12")
    reloj[0] += 0.2
    m.fin("AG-12", t)
    reloj[0] += 2
    assert not _ordenes(m.evaluar_instancias())
    reloj[0] += 2
    cierre, = m.evaluar_instancias()
    assert cierre["accion"] == "CERRAR" and cierre["instancias_despues"] == 1


def test_cuarenta_ingestas_concurrentes_sin_duplicados(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    def ingresar(i):
        f = {"proxy": "X", "senales": {"fecha_dato": AS_OF, "precio": 1}, "_piezas": [{"fuente": "HT-01:X",
             "afirmacion": "Dato de prueba", "direccion": "neutra", "origen": "AG-13"}]}
        b._registrar_evidencia_clase({"nivel": "N1", "clase": "RV", "finalistas": [f]}, pd.Timestamp(AS_OF), f"RUN-{i}")
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(ingresar, range(40)))
    assert len(b.almacen.estado("F2", clave="evd_id")) == 1
    assert len(b.almacen.estado("F2", clave="clm_id")) == 1


def test_la_orden_por_ingesta_se_registra_en_el_mismo_ciclo(tmp_path, universo, monkeypatch):
    b = nuevo_bloque(tmp_path, universo)
    reloj = [0.0]
    b.monitor = Monitor(objetivo_ingesta_s=1, reloj=lambda: reloj[0])
    b.agentes.monitor = b.monitor
    curar = b._curar_lote

    duracion = [3.]

    def ingesta_lenta(*args, **kwargs):
        curar(*args, **kwargs)
        reloj[0] += duracion[0]

    monkeypatch.setattr(b, "_curar_lote", ingesta_lenta)
    run = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    orden, = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "ORD" and e["agente"] == "AG-12"]
    assert orden["run_id"] == run["run_id"]
    assert orden["accion"] == "ABRIR" and orden["metricas_disparo"]["W"] == 3
    assert orden["metricas_disparo"]["lambda"] == 1 / 3
    duracion[0] = .5
    siguiente = b.ciclo("2026-06-12", alcance={"clases": ["RV"]})
    car, = [e for e in b.almacen.leer("HA") if e.get("run_id") == siguiente["run_id"]
            and e.get("tipo_entrada") == "CAR" and e["agente"] == "AG-12"]
    assert car["W"] == .5 and car["en_objetivo"] and car["saturado"] is False


def _ventana(monitor, reloj, duracion, intervalo, cantidad=1, agente="AG-12"):
    monitor.encolar(agente, cantidad)
    reloj[0] += intervalo
    for _ in range(cantidad):
        monitor.fin(agente, reloj[0] - duracion)
    return monitor.evaluar_instancias()


def _ordenes(lectura):
    return [e for e in lectura if e["tipo_entrada"] == "ORD"]


def test_coeficientes_y_recuperacion_medidos_por_ventana():
    reloj = [0.]
    m = Monitor(objetivo_ingesta_s=1, reloj=lambda: reloj[0])
    assert _ventana(m, reloj, 2., 2.) == []
    apertura, = _ordenes(_ventana(m, reloj, 3., 10., 10))
    assert apertura["instancias_despues"] == 4
    assert apertura["metricas_disparo"] == {"W": 3., "rho": 3., "cola": 0, "lambda": 1., "mu": 1/3}
    for duracion, esperado in [(1.5, False), (0.5, True)]:
        car, = _ventana(m, reloj, duracion, 1.)
        assert car["tipo_entrada"] == "CAR" and car["saturado"] is False
        assert car["en_objetivo"] is esperado and car["W"] == duracion and car["objetivo"] == 1
    reloj[0] += 1
    orden, = _ordenes(m.evaluar_instancias())
    assert orden["accion"] == "CERRAR" and orden["instancias_despues"] == 3
    assert m.instancias["AG-12"] == orden["instancias_despues"]
    assert orden["calculo"] and orden["metricas_disparo"]["lambda"] == 0


def test_cierre_consecutivo_solo_con_cola_vacia_y_baja_utilizacion():
    reloj = [0.]
    m = Monitor(objetivo_ingesta_s=1, reloj=lambda: reloj[0])
    assert _ordenes(_ventana(m, reloj, 2.0001, 3.))[0]["accion"] == "ABRIR"
    for _ in range(2):
        assert not _ordenes(m.evaluar_instancias())  # ventana cero
    m.encolar("AG-12")
    for _ in range(2):
        reloj[0] += 5
        assert not _ordenes(m.evaluar_instancias())
    m.fin("AG-12", reloj[0])
    reloj[0] += 2
    assert not _ordenes(m.evaluar_instancias())
    assert not _ordenes(_ventana(m, reloj, 1.5, 2.))
    reloj[0] += 1
    assert not _ordenes(m.evaluar_instancias())
    reloj[0] += 1
    assert _ordenes(m.evaluar_instancias())[0]["instancias_despues"] == 1
    reloj[0] += 2
    assert not m.evaluar_instancias()


def test_umbrales_configurados_y_limite_de_instancias():
    reloj = [0.]
    m = Monitor(objetivo_ingesta_s=1, reloj=lambda: reloj[0], factor_tiempo=3, rho_objetivo=.5,
                rho_cierre=.05, lecturas_cierre=3, instancias_max=6)
    assert not _ventana(m, reloj, 2.5, 3.)
    assert not _ventana(m, reloj, 3., 3.)
    apertura, = _ordenes(_ventana(m, reloj, 3.1, 10., 10))
    assert apertura["instancias_despues"] == 6
    assert not _ordenes(_ventana(m, reloj, 15., 10., 10))  # cap
    for _ in range(3):
        assert not _ordenes(_ventana(m, reloj, 0.6, 1.))
    for _ in range(2):
        reloj[0] += 1
        assert not _ordenes(m.evaluar_instancias())
    reloj[0] += 1
    assert _ordenes(m.evaluar_instancias())[0]["instancias_despues"] == 5
    otro = Monitor(objetivo_ingesta_s=1, reloj=lambda: reloj[0], rho_objetivo=.5)
    assert _ordenes(_ventana(otro, reloj, 3, 10, 10))[0]["instancias_despues"] == 6
    assert not _ventana(otro, reloj, 40, 40, agente="AG-03")


def test_configuracion_objetivo_invalida(tmp_path, universo):
    import pytest
    from conftest import config_pruebas
    for valor in [0, -1, float("nan"), float("inf"), True, "5", [1]]:
        with pytest.raises(ValueError):
            Monitor(objetivo_ingesta_s=valor)
    with pytest.raises(ValueError):
        nuevo_bloque(tmp_path, universo, cfg=config_pruebas(paralelismo={"objetivo_ingesta_s": "5"}))
    for cambios in [{"factor_tiempo": 0}, {"rho_objetivo": 2}, {"rho_cierre": float("nan")}, {"lecturas_cierre": 1.5}]:
        with pytest.raises(ValueError):
            Monitor(**cambios)
