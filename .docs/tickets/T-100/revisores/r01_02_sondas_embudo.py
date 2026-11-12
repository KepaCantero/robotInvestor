"""QA r01 de T-100 (V0.76): sondas del revisor contra el embudo (T-75 H-15): la causa previa de una salida no puede depender de
dónde empiece el periodo, con vetos, observaciones y análisis nuevos en distintos órdenes, y con el periodo empezando justo en el
borde de cada anotación. Datos SIMULADOS.

Uso (desde la raíz del repositorio): .venv/bin/python -I .docs/tickets/T-100/revisores/r01_02_sondas_embudo.py [ruta del marco]
Cada sonda imprime BIEN o FALLA. Termina con 0 siempre: es una sonda.
"""
import sys
from datetime import datetime, timedelta
from pathlib import Path

MARCO = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[4] / "sistema_global" / "marco_comun_c"
sys.path.insert(0, str(MARCO / "validador"))
sys.path.insert(0, str(MARCO / "pruebas"))
from orquestador import Orquestador  # noqa: E402
from pruebas_k import CAL  # noqa: E402
from pruebas_operador_t50 import vetado  # noqa: E402
from pruebas_orquestador import AHORA, CFG, S1, encargo, hasta, registrar_motor, sobre_para  # noqa: E402

T0 = "2026-09-01T09:00:00+00:00"
RES = []


def sonda(nombre, bien, detalle=""):
    bien = bool(bien)
    RES.append((nombre, bien))
    print(f"{'BIEN' if bien else 'FALLA':6s} {nombre}  {str(detalle)[:600]}")


def mas(t, **kw):
    return (datetime.fromisoformat(t) + timedelta(**kw)).isoformat()


def antiguo():
    o = Orquestador(CFG, CAL)
    assert o.degradar("TRADING", "arranque de prueba: el operador deja TRADING en L1", "OPERADOR", T0)["ok"]
    assert o.registrar_sello(S1, AHORA)["ok"]
    registrar_motor(o, S1["sello_id"])
    return o


def con_veto():
    o = antiguo()
    hasta(o, "PROPUESTA", 1)
    assert o.pantalla_aprobacion("EXP-0001", vetado(o), AHORA)["codigo"] == "O-06"
    return o


def reanalizar(o, t_obs, t_reab, t_sobre, sufijo):
    assert o.observar("EXP-0001", [{"tipo": "PRECIO", "instrumento": "EURUSD", "operador": ">=", "umbral": 1.12}], "esperar",
                      "GESTOR_TACTICA", t_obs)["ok"]
    assert o.reabrir("EXP-0001", "cambió el contexto", "OPERADOR", t_reab)["ok"]
    enc = encargo(1)
    enc["event_id"] = f"EV-ENC-01{sufijo}"
    assert o.emitir_encargo("EXP-0001", enc, "GESTOR_TACTICA", t_reab)["ok"]
    s = sobre_para(1, None)
    s["event_id"] = f"EV-SOB-0001-{sufijo}"
    assert o.entregar_sobre("EXP-0001", s, t_sobre)["ok"]


def causas(o, hasta_t):
    """Para cada salida, el conjunto de bloqueo_previo que da el embudo con todos los inicios de periodo posibles anteriores a ella,
    incluidos los bordes exactos de cada anotación y un microsegundo antes y después."""
    hs = sorted({x["ahora"] for x in o.expedientes["EXP-0001"]["historial"]}, key=datetime.fromisoformat)
    inicios = sorted({v for t in hs for v in (mas(t, microseconds=-1), t, mas(t, microseconds=1))} | {mas(hs[0], days=-1)},
                     key=datetime.fromisoformat)
    out = {}
    for d0 in [x for x in inicios if datetime.fromisoformat(x) <= datetime.fromisoformat(hasta_t)]:
        em = o.embudo(d0, hasta_t)
        assert em is not None, d0
        for s in em["salidas"]:
            out.setdefault((s["hasta"], s["ahora"]), set()).add(s["bloqueo_previo"])
    return out


def veto(o):
    return next(x["motivo"] for x in o.expedientes["EXP-0001"]["historial"] if x["desde"] == x["hasta"] == "PROPUESTA" and x["actor"] == "F")


# E1: veto, observación (salida), reapertura y análisis nuevo, descarte (salida)
o = con_veto()
reanalizar(o, mas(AHORA, minutes=1), mas(AHORA, minutes=2), mas(AHORA, minutes=3), "A")
t_desc = mas(AHORA, minutes=10)
assert o.descartar("EXP-0001", "el operador lo descarta tras el nuevo análisis", "OPERADOR", t_desc)["ok"]
c = causas(o, t_desc)
v = veto(o)
obs = c.get(("EN_OBSERVACION", mas(AHORA, minutes=1)))
desc = c.get(("DESCARTADA", t_desc))
sonda("E1_la_observacion_tras_el_veto_lleva_el_veto_con_cualquier_inicio", obs == {v}, obs)
sonda("E1b_el_descarte_tras_el_analisis_nuevo_no_lleva_el_veto_con_cualquier_inicio", desc == {None}, desc)

# E2: veto y descarte directo, sin análisis nuevo: el veto es la causa con cualquier inicio
o = con_veto()
t_desc = mas(AHORA, minutes=10)
assert o.descartar("EXP-0001", "el operador lo descarta tras el veto", "OPERADOR", t_desc)["ok"]
c = causas(o, t_desc)
sonda("E2_sin_analisis_nuevo_el_veto_es_la_causa_con_cualquier_inicio", c.get(("DESCARTADA", t_desc)) == {veto(o)}, c)

# E3: veto, análisis nuevo en el mismo instante que el inicio del periodo (borde exacto), y caducidad por barrido
o = con_veto()
t3 = mas(AHORA, minutes=3)
reanalizar(o, mas(AHORA, minutes=1), mas(AHORA, minutes=2), t3, "B")
em_borde = o.embudo(t3, mas(AHORA, days=30))   # (t3, …]: el análisis nuevo queda fuera del periodo, por el borde
o.barrer(mas(AHORA, days=30))
c = causas(o, mas(AHORA, days=30))
cad = {k: v for k, v in c.items() if k[0] == "CADUCADA"}
sonda("E3_la_caducidad_tras_el_analisis_nuevo_no_lleva_el_veto_tampoco_con_el_borde", all(v_ == {None} for v_ in cad.values()) and cad,
      (cad, em_borde and em_borde["salidas"]))

# E4: dos ciclos: veto, análisis nuevo, observación y otro análisis; descarte. Nunca reaparece el veto viejo
o = con_veto()
reanalizar(o, mas(AHORA, minutes=1), mas(AHORA, minutes=2), mas(AHORA, minutes=3), "C")
reanalizar(o, mas(AHORA, minutes=4), mas(AHORA, minutes=5), mas(AHORA, minutes=6), "D")
t_desc = mas(AHORA, minutes=10)
assert o.descartar("EXP-0001", "descartado tras dos análisis", "OPERADOR", t_desc)["ok"]
c = causas(o, t_desc)
sonda("E4_dos_reanalisis_el_veto_viejo_no_reaparece", c.get(("DESCARTADA", t_desc)) == {None} and c.get(("EN_OBSERVACION", mas(AHORA, minutes=4))) == {None}
      and c.get(("EN_OBSERVACION", mas(AHORA, minutes=1))) == {veto(o)}, c)

# E5: el «hasta» corta entre anotaciones: la fila de la oportunidad lleva el veto solo si el análisis nuevo cae después de hasta
o = con_veto()
reanalizar(o, mas(AHORA, minutes=1), mas(AHORA, minutes=2), mas(AHORA, minutes=3), "E")
ini = mas(AHORA, days=-30)
filas = {h: next(x for x in o.embudo(ini, h)["oportunidades"] if x["expediente_id"] == "EXP-0001")["bloqueo"]
         for h in (AHORA, mas(AHORA, minutes=1), mas(AHORA, minutes=2), mas(AHORA, minutes=3))}
sonda("E5_el_bloqueo_de_la_fila_sigue_el_hasta", filas[AHORA] == veto(o) and filas[mas(AHORA, minutes=1)] == veto(o)
      and filas[mas(AHORA, minutes=2)] is None and filas[mas(AHORA, minutes=3)] is None, filas)

# E6: veto, observación, reapertura y encargo nuevo (EN_ANALISIS) y, antes del sobre, el operador lo descarta: el encargo nuevo ya
# es un análisis nuevo (el embudo borra el veto al llegar a VALIDADA o a EN_ANALISIS)
o = con_veto()
assert o.observar("EXP-0001", [{"tipo": "PRECIO", "instrumento": "EURUSD", "operador": ">=", "umbral": 1.12}], "esperar",
                  "GESTOR_TACTICA", mas(AHORA, minutes=1))["ok"]
assert o.reabrir("EXP-0001", "cambió el contexto", "OPERADOR", mas(AHORA, minutes=2))["ok"]
enc = encargo(1)
enc["event_id"] = "EV-ENC-01F"
assert o.emitir_encargo("EXP-0001", enc, "GESTOR_TACTICA", mas(AHORA, minutes=2))["ok"]
t_desc = mas(AHORA, minutes=10)
rd = o.descartar("EXP-0001", "descartado con el encargo nuevo en curso", "OPERADOR", t_desc)
c = causas(o, t_desc)
estado_previo = [x["desde"] for x in o.expedientes["EXP-0001"]["historial"] if x["hasta"] == "DESCARTADA"]
sonda("E6_descartado_en_analisis_tras_el_encargo_nuevo_no_lleva_el_veto", rd["ok"] and c.get(("DESCARTADA", t_desc)) == {None},
      (rd["codigo"], estado_previo, c))

print()
print(f"{sum(b for _, b in RES)} BIEN, {sum(not b for _, b in RES)} FALLA: {[n for n, b in RES if not b]}")
