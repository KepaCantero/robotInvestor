"""QA r02 · sonda 04: fallo cerrado y atomicidad de abrir_directa() y consultar() en los caminos nuevos de la r01, y el parámetro
o_max_analisis_consulta (PAR-0.5.0).
  - Cada rechazo nuevo (análisis + encargo, origen re-encargado, CADUCADA, N3, niveles raros, consulta_id raro, C con encargo
    inválido y consulta) deja el estado igual (salvo avisos y reloj) y sin APERTURA.
  - consultar(): cada rechazo deja el estado igual; con el registro roto da O-13 y kill-switch ANTES de mirar si es duplicada (H-05).
  - El tope está en el borde: 50 pasa la forma (y falla luego por el análisis desconocido), 51 no. Cambiar parametros._VALORES en
    caliente no cambia PARAMETROS (copia congelada).
(Datos SIMULADOS.)"""
import copy
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import AHORA, chk, encargo, fin, foto, hasta, nuevo, sobre_para  # noqa: E402
from pruebas_orquestador import COND_OBS  # noqa: E402
from pruebas_via_directa_t80 import consulta, descartado_por_operador, enc_directa  # noqa: E402
import parametros  # noqa: E402
from parametros import PARAMETROS  # noqa: E402


def rechaza(nombre, o, fn, codigos):
    antes = foto(o)
    n_sc5 = len(o.consultas["entradas"])
    r = fn()
    bien = (not r["ok"]) and r["codigo"] in codigos and foto(o) == antes and len(o.consultas["entradas"]) == n_sc5
    chk(nombre, bien, (r["codigo"], r["motivo"][:90], "estado cambió" if foto(o) != antes else ""))


o = nuevo()
descartado_por_operador(o, 1)
assert o.consultar(consulta(), "BROKER", AHORA)["ok"]
ab = o.abrir_directa
rechaza("D_analisis_y_encargo_O01", o, lambda: ab("EXP-DD-06", "COR-EXP-DD-06", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001",
                                                     encargo=enc_directa("EXP-DD-06", 6, nivel="N2"), consulta_id="CON-0001"), ("O-01",))
rechaza("D_encargo_N3_O06", o, lambda: ab("EXP-DD-06", "COR-EXP-DD-06", "TACTICA", "D", "BROKER", AHORA,
                                             encargo=enc_directa("EXP-DD-06", 6, nivel="N3"), consulta_id="CON-0001"), ("O-06",))
for i, nivel in enumerate((None, "N9", 2, ["N1"], {"n": 1}, "n1", " N1", "")):
    def f(nivel=nivel):
        e = enc_directa("EXP-DD-06", 6)
        e["payload"]["nivel_analisis"] = nivel
        return ab("EXP-DD-06", "COR-EXP-DD-06", "TACTICA", "D", "BROKER", AHORA, encargo=e, consulta_id="CON-0001")
    rechaza(f"D_encargo_nivel_raro_{i}_{type(nivel).__name__}", o, f, ("O-06", "O-01", "O-00"))
for i, cid in enumerate((1, ["CON-0001"], {"CON-0001": 1}, b"CON-0001", "CON-0001 ", "", float("nan"))):
    rechaza(f"consulta_id_raro_{i}_{type(cid).__name__}", o,
            lambda cid=cid: ab("EXP-DD-06", "COR-DD-06", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001", consulta_id=cid), ("O-12", "O-01", "O-00"))
mal = enc_directa("EXP-DC-07", 7)
mal["payload"]["presupuesto"]["coste_max_eur"] = -1
rechaza("C_con_encargo_invalido_y_consulta_no_deja_APERTURA", o,
        lambda: ab("EXP-DC-07", "COR-EXP-DC-07", "TACTICA", "C", "BROKER", AHORA, encargo=mal, consulta_id="CON-0001"), ("O-01", "O-00"))
rechaza("C_con_consulta_de_otra_cartera", o,
        lambda: ab("EXP-DC-07", "COR-EXP-DC-07", "TRADING", "C", "BROKER", AHORA, encargo=enc_directa("EXP-DC-07", 7), consulta_id="CON-0001"), ("O-12",))

# origen re-encargado y CADUCADA
o2 = nuevo()
assert o2.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
assert o2.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA)["ok"]
assert o2.entregar_sobre("EXP-0001", sobre_para(1, None), AHORA)["ok"]
assert o2.observar("EXP-0001", COND_OBS, "el operador lo aparta", "OPERADOR", AHORA)["ok"]
assert o2.reabrir("EXP-0001", "el operador pide otro análisis", "OPERADOR", AHORA)["ok"]
e2 = encargo(1)
e2["event_id"] = "EV-ENC-0001-B"
assert o2.emitir_encargo("EXP-0001", e2, "GESTOR_TACTICA", AHORA)["ok"]
assert o2.observar("EXP-0001", COND_OBS, "el operador lo aparta otra vez", "OPERADOR", AHORA)["ok"]
rechaza("origen_re_encargado_O06", o2, lambda: o2.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001"), ("O-06",))
rechaza("origen_re_encargado_por_E_O06", o2, lambda: o2.abrir_directa("EXP-DE-01", "COR-DE-01", "TACTICA", "E", "BROKER", AHORA, analisis="EV-SOB-0001",
                                                                       motivo="solo hay un candidato en la cartera: lo pidió el operador"), ("O-06",))
o3 = nuevo()
hasta(o3, "PROPUESTA", 1)
A2 = "2026-11-08T13:00:00+00:00"
assert o3.barrer(A2)["ok"]
rechaza("CADUCADA_O06", o3, lambda: o3.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", A2, analisis="EV-SOB-0001"), ("O-06",))

# consultar(): rechazos sin estado
for nombre, c, cods in (("tipo", consulta("CON-X", tipo="INVERTIR"), ("O-01",)), ("bloque_F", consulta("CON-X", bloque="F"), ("O-01",)),
                        ("analisis_no_lista", {**consulta("CON-X"), "analisis": "EV-SOB-0001"}, ("O-01",)),
                        ("analisis_desconocido", consulta("CON-X", analisis=("EV-SOB-9999",)), ("O-12",)),
                        ("repetido_otro_contenido", consulta("CON-0001", analisis=()), ("O-03",)),
                        ("pregunta_corta", consulta("CON-X", pregunta="¿y?"), ("O-15",))):
    rechaza(f"consultar_{nombre}", o, lambda c=c: o.consultar(c, "BROKER", AHORA), cods)

# el borde del tope
P = PARAMETROS["o_max_analisis_consulta"]
r50 = o.consultar(consulta("CON-X", tipo="ANALIZAR", bloque="C", cartera=None, analisis=[f"EV-NO-{i}" for i in range(P)]), "BROKER", AHORA)
r51 = o.consultar(consulta("CON-X", tipo="ANALIZAR", bloque="C", cartera=None, analisis=[f"EV-NO-{i}" for i in range(P + 1)]), "BROKER", AHORA)
print("tope", P, "| con", P, ":", r50["codigo"], "| con", P + 1, ":", r51["codigo"], r51["motivo"][:80])
chk("tope_en_el_borde", P == 50 and r50["codigo"] == "O-12" and r51["codigo"] == "O-01" and str(P) in r51["motivo"], (r50, r51))
try:
    PARAMETROS["o_max_analisis_consulta"] = 10 ** 6
    escrito = True
except TypeError:
    escrito = False
chk("PARAMETROS_no_se_escribe", not escrito)

# cambiar el tope en caliente: PARAMETROS es una copia congelada (no una vista de parametros._VALORES), así que no cambia
viejo = parametros._VALORES["o_max_analisis_consulta"]
try:
    parametros._VALORES["o_max_analisis_consulta"] = 10 ** 6
    r = o.consultar(consulta("CON-Y", tipo="ANALIZAR", bloque="C", cartera=None, analisis=[f"EV-NO-{i}" for i in range(P + 1)]), "BROKER", AHORA)
    chk("tope_cambiado_en_caliente_no_se_usa", PARAMETROS["o_max_analisis_consulta"] == 50 and r["codigo"] == "O-01", r)
finally:
    parametros._VALORES["o_max_analisis_consulta"] = viejo

# H-05: con el rastro tocado, consultar da O-13 y kill antes de mirar si la consulta está repetida
o5 = copy.deepcopy(o)
o5.consultas["entradas"][0]["consulta"]["pregunta"] = "otra pregunta escrita a mano"
r = o5.consultar(copy.deepcopy(o5.consultas["entradas"][0]["consulta"]), "BROKER", AHORA)
chk("H05_consulta_tocada_repetida_da_O13_y_kill", r["codigo"] == "O-13" and o5.kill is not None, r)
sys.exit(fin())
