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
    assert orden["accion"] == "ABRIR" and orden["metricas_disparo"]["W_medio_s"] == 3.
    m.encolar("AG-12")
    t = m.inicio("AG-12")
    reloj[0] += 0.2
    m.fin("AG-12", t)
    reloj[0] += 2
    assert not m.evaluar_instancias()
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
