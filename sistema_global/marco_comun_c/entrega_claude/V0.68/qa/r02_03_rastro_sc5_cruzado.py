"""QA r02 · sonda 03 (H-02 y H-05 corregidos): el cruce del rastro SC-5 con los expedientes (`_consultas_citadas_ok`).
  1) Recorridos legítimos con consulta (D reutilizando, C, D con encargo, E único y E con O-30) no dan nunca un CONSULTAS falso
     (que con el cruce saltaría el kill-switch en el siguiente punto de decisión), también tras guardar y cargar.
  2) La entrada por E con consulta que se devuelve a D (O-22) no deja nada: ni expediente ni APERTURA (la anotó antes de comparar).
  3) Un falsificador sin clave que rehace la cadena SC-5 entera (los hash son sha256 sin secreto) no puede quitar ni cambiar lo
     citado: APERTURA a otro expediente, quitar el análisis de la consulta, APERTURA duplicada, APERTURA a un expediente sin
     consulta, borrar el expediente DIRECTA.
  4) Formas raras del atributo `consultas` (estado distinto con la cadena vacía, None, lista) salen en integridad() y paran.
(Datos SIMULADOS.)"""
import copy
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import AHORA, ENTRADA, SALIDA, anotar_entrada, autorizar_op, chk, dim, fin, foto, hasta, informe_f, nuevo  # noqa: E402
from pruebas_via_directa_t80 import consulta, descartado_por_operador, enc_directa, sobre_directa  # noqa: E402
import persistencia as pe  # noqa: E402

MOT = "solo hay un candidato en la cartera: lo pidió el operador"


def hasta_ejecutada(o, eid, ahora=AHORA):
    r = o.proponer(eid, ENTRADA, SALIDA, "BROKER", ahora, dim(o, eid))
    assert r["ok"], r
    assert autorizar_op(o, eid, informe_f(o, eid, 42), ahora)["ok"]
    anotar_entrada(o, eid, f"ORD-{eid}", 100.0, ahora)
    r = o.ejecutar(eid, {"orden_id": f"ORD-{eid}", "cantidad": 100.0, "precio": 1.1, "conciliada": True,
                         "proteccion_orden_ids": [f"ORD-{eid}-STOP"]}, "G", ahora)
    assert r["ok"], r


def ida_y_vuelta(o):
    rc = pe.cargar(pe.volcar(o, AHORA))
    return rc["ok"] and rc["orquestador"].integridad() == []


# 1a) D reutilizando con consulta, hasta EJECUTADA
o = nuevo()
descartado_por_operador(o, 1)
assert o.consultar(consulta(), "BROKER", AHORA)["ok"]
r = o.abrir_directa("EXP-DQ-01", "COR-DQ-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001", consulta_id="CON-0001")
assert r["ok"], r
assert o.comparar(["EXP-DQ-01"], "D", AHORA)["ok"]
hasta_ejecutada(o, "EXP-DQ-01")
chk("1a_D_con_consulta_hasta_EJECUTADA_integro", o.integridad() == [] and o.kill is None and ida_y_vuelta(o), o.integridad())
O_BASE = o

# 1b) C con consulta (ANALIZAR, sin análisis) hasta PROPUESTA
o = nuevo()
assert o.consultar(consulta("CON-0002", tipo="ANALIZAR", bloque="C", cartera=None, analisis=(), pregunta="¿Qué tal pinta el yen este trimestre?"),
                   "BROKER", AHORA)["ok"]
r = o.abrir_directa("EXP-DC-05", "COR-EXP-DC-05", "TACTICA", "C", "BROKER", AHORA, encargo=enc_directa("EXP-DC-05", 5), consulta_id="CON-0002")
print("1b) C con consulta:", r["ok"], r["codigo"], r["motivo"][:70])
assert r["ok"]
assert o.entregar_sobre("EXP-DC-05", sobre_directa("EXP-DC-05", 5), AHORA)["ok"]
assert o.comparar(["EXP-DC-05"], "D", AHORA)["ok"]
r = o.proponer("EXP-DC-05", ENTRADA, SALIDA, "BROKER", AHORA, dim(o, "EXP-DC-05"))
chk("1b_C_con_consulta_hasta_PROPUESTA_integro", r["ok"] and o.integridad() == [] and ida_y_vuelta(o), (r, o.integridad()))

# 1c) D con encargo N2 y consulta
o = nuevo()
assert o.consultar(consulta("CON-0003", tipo="PROYECTAR", bloque="D", cartera="TACTICA", analisis=(),
                            pregunta="¿Cómo quedaría la cartera con un poco de EURUSD?"), "BROKER", AHORA)["ok"]
r = o.abrir_directa("EXP-DD-05", "COR-EXP-DD-05", "TACTICA", "D", "BROKER", AHORA, encargo=enc_directa("EXP-DD-05", 5, nivel="N2"),
                    consulta_id="CON-0003")
chk("1c_D_con_encargo_y_consulta_integro", r["ok"] and o.integridad() == [] and o.consultas["entradas"][-1]["tipo"] == "APERTURA", r)

# 1d) E con consulta, candidato único; después observar, reabrir y volver a encargar (el análisis citado sigue siendo el de la consulta)
o = nuevo()
descartado_por_operador(o, 1)
assert o.consultar(consulta(), "BROKER", AHORA)["ok"]
r = o.abrir_directa("EXP-DE-01", "COR-DE-01", "TACTICA", "E", "BROKER", AHORA, analisis="EV-SOB-0001", motivo=MOT, consulta_id="CON-0001")
chk("1d_E_con_consulta_nace_COMPARADA_integro", r["ok"] and o.expedientes["EXP-DE-01"]["estado"] == "COMPARADA" and o.integridad() == [], r)
assert o.observar("EXP-DE-01", [{"tipo": "FECHA", "fecha": "2026-11-20"}], "el operador lo deja para luego", "OPERADOR", AHORA)["ok"]
assert o.reabrir("EXP-DE-01", "el operador quiere un análisis nuevo", "OPERADOR", AHORA)["ok"]
e6 = enc_directa("EXP-DE-01", 1)
e6["correlation_id"] = "COR-DE-01"
r = o.emitir_encargo("EXP-DE-01", e6, "BROKER", AHORA)
s6 = sobre_directa("EXP-DE-01", 1)
s6["correlation_id"] = "COR-DE-01"
r2 = o.entregar_sobre("EXP-DE-01", s6, AHORA) if r["ok"] else r
chk("1d_reanalisis_del_DIRECTA_con_consulta_sigue_integro", r["ok"] and r2["ok"] and o.integridad() == [] and ida_y_vuelta(o), (r, r2, o.integridad()))

# 1e) E con consulta y un testigo que habría ganado (O-30, ok): la APERTURA queda y es íntegro
o = nuevo()
descartado_por_operador(o, 1)
hasta(o, "VALIDADA", 3)
assert o.observar("EXP-0003", [{"tipo": "FECHA", "fecha": "2026-11-20"}], "el gestor lo aparta", "GESTOR_TACTICA", AHORA)["ok"]
assert o.consultar(consulta(), "BROKER", AHORA)["ok"]
r = o.abrir_directa("EXP-DE-01", "COR-DE-01", "TACTICA", "E", "BROKER", AHORA, analisis="EV-SOB-0001", motivo=MOT, consulta_id="CON-0001")
print("1e) E con testigo:", r["ok"], r["codigo"])
chk("1e_E_con_consulta_y_O30_integro", o.integridad() == [] and (not r["ok"] or o.consultas["entradas"][-1]["tipo"] == "APERTURA"), r)

# 2) E con consulta devuelto a D (otro candidato vigente): no deja nada
o = nuevo()
descartado_por_operador(o, 1)
hasta(o, "VALIDADA", 3)
assert o.consultar(consulta(), "BROKER", AHORA)["ok"]
antes = foto(o)
r = o.abrir_directa("EXP-DE-01", "COR-DE-01", "TACTICA", "E", "BROKER", AHORA, analisis="EV-SOB-0001", motivo=MOT, consulta_id="CON-0001")
chk("2_E_con_consulta_devuelto_a_D_no_deja_nada", r["codigo"] == "O-22" and foto(o) == antes and o.integridad() == [], r)
r = o.abrir_directa("EXP-DE-01", "COR-DE-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001", consulta_id="CON-0001")
chk("2_despues_entra_por_D_con_la_misma_consulta", r["ok"] and o.integridad() == [], r)


# 3) falsificador que rehace la cadena SC-5
def rehacer(o, entradas):
    o.consultas = {"historial": [], "estado": "VIGENTE", "entradas": []}
    for x in entradas:
        o._anota_sc5(x, AHORA)


def forja(nombre, cambio):
    o = copy.deepcopy(O_BASE)
    ent = copy.deepcopy(O_BASE.consultas["entradas"])
    ent = cambio(o, ent)
    rehacer(o, ent)
    integ = o.integridad()
    r = o.consultar(consulta("CON-0009", tipo="ANALIZAR", bloque="C", cartera=None, analisis=(), pregunta="pregunta de la sonda r02"), "BROKER", AHORA)
    chk(f"3_{nombre}_se_detecta_y_para", "CONSULTAS" in integ and r["codigo"] == "O-13" and o.kill is not None, (integ, r["codigo"]))


def ap_a_otro(o, ent):
    ent[-1]["expediente_id"] = "EXP-0001"
    return ent


def quitar_analisis(o, ent):
    ent[0]["consulta"]["analisis"] = []
    return ent


def ap_duplicada(o, ent):
    return ent + [copy.deepcopy(ent[-1])]


def ap_a_no_citante(o, ent):
    return ent + [{"tipo": "APERTURA", "consulta_id": "CON-0001", "expediente_id": "EXP-0001", "bloque": "D"}]


def borrar_expediente(o, ent):
    del o.expedientes["EXP-DQ-01"]
    return ent


for nombre, f in (("APERTURA_a_otro_expediente", ap_a_otro), ("quitar_el_analisis_de_la_consulta", quitar_analisis),
                  ("APERTURA_a_un_expediente_sin_consulta", ap_a_no_citante),
                  ("borrar_el_expediente_DIRECTA", borrar_expediente)):
    forja(nombre, f)

# informativo (no es un hallazgo): añadir lo que nadie cita con la cadena rehecha no lo ve el cruce; lo cubre el ancla externa de
# la cabeza SC5 (T-02), igual que añadir una CONSULTA falsa. Una APERTURA repetida no cambia nada de lo que citan los expedientes
o = copy.deepcopy(O_BASE)
rehacer(o, ap_duplicada(o, copy.deepcopy(O_BASE.consultas["entradas"])))
print("INFO  3_APERTURA_duplicada_con_la_cadena_rehecha: integridad() =", o.integridad(), "(solo la ve el ancla externa de la cabeza SC5)")

# 4) formas raras del atributo
for nombre, valor in (("estado_raro_vacio", {"historial": [], "estado": "OTRO", "entradas": []}), ("None", None), ("lista", []),
                      ("entradas_sin_historial", {"historial": [], "estado": "VIGENTE", "entradas": [{"tipo": "CONSULTA"}]})):
    o = nuevo()
    o.consultas = copy.deepcopy(valor)
    integ = o.integridad()
    r = o.consultar(consulta("CON-0009", tipo="ANALIZAR", bloque="C", cartera=None, analisis=(), pregunta="pregunta de la sonda r02"), "BROKER", AHORA)
    chk(f"4_consultas_{nombre}_sale_en_integridad_y_para", "CONSULTAS" in integ and r["codigo"] == "O-13", (integ, r["codigo"], r["motivo"][:60]))
sys.exit(fin())
