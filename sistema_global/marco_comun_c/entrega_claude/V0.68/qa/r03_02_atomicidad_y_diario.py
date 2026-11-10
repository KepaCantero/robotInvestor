"""QA r03 · sonda 02: atomicidad y fallo cerrado de abrir_directa() y consultar(), y el diario.
  a) un rechazo de abrir_directa por C (y por D con encargo) tras _caducar_encargos: ¿deja el estado igual (encargos incluidos)?
  b) tipos que no se pueden usar como clave (listas, dicts) en cartera/bloque de abrir_directa y de una consulta: rechazo sin estado;
  c) analisis_vigentes() no muta nada, también con un estado roto (devuelve [] o filas, nunca lanza);
  d) el diario reproduce un recorrido con DIRECTA por E devuelto a D con consulta (la APERTURA se retira), el DIRECTA que caduca y
     se reanaliza, y rechazos: el estado reproducido es idéntico.
(Datos SIMULADOS.)"""
import copy
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import AHORA, ENTRADA, SALIDA, chk, dim, enc_directa, encargo, fin, foto, nuevo, sobre_para  # noqa: E402,F401
from pruebas_orquestador import COND_OBS  # noqa: E402
import persistencia as pe  # noqa: E402
import diario as di  # noqa: E402

TARDE = "2026-11-08T13:00:00+00:00"   # pasó el valid_until (12:00) del encargo EN_CURSO de EXP-0001


def con_encargo_en_curso():
    o = nuevo()
    assert o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
    assert o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA)["ok"]
    return o


# a) rechazos de abrir_directa con un encargo vencido de otro expediente
for etiqueta, bloque, mutar in (("C_cartera_del_encargo", "C", lambda e: e["payload"].__setitem__("cartera_destino", "TRADING")),
                                 ("C_mandato", "C", lambda e: e["payload"].__setitem__("mandato_ref", "otro")),
                                 ("D_nivel_N3", "D", lambda e: e["payload"].__setitem__("nivel_analisis", "N3")),
                                 ("C_producer", "C", lambda e: e.__setitem__("expediente_id", "EXP-OTRO"))):
    o = con_encargo_en_curso()
    antes = foto(o)
    e = enc_directa("EXP-DC-09", 9)
    mutar(e)
    r = o.abrir_directa("EXP-DC-09", "COR-EXP-DC-09", "TACTICA", bloque, "BROKER", TARDE, encargo=e)
    cambios = sorted(k for k in antes if antes[k] != foto(o)[k])
    print(f"a) {etiqueta}:", r["ok"], r["codigo"], r["motivo"][:70], "| cambia:", cambios,
          "| encargo de EXP-0001:", o.encargos["EV-ENC-0001"]["estado"])
    chk(f"a_{etiqueta}_rechazo_sin_estado", not r["ok"] and not cambios, cambios)

# b) tipos que no son clave
o = nuevo()
antes = foto(o)
for kw in ({"cartera_destino": ["TACTICA"]}, {"cartera_destino": {"x": 1}}, {"bloque": ["D"]}, {"bloque": {"D": 1}}):
    args = {"expediente_id": "EXP-X", "correlation_id": "COR-X", "cartera_destino": "TACTICA", "bloque": "D", "actor": "BROKER", "ahora": AHORA,
            "analisis": "EV-SOB-0001", **kw}
    r = o.abrir_directa(**args)
    chk(f"b_abrir_directa_{list(kw)[0]}_{type(list(kw.values())[0]).__name__}_rechaza_sin_estado", not r["ok"] and foto(o) == antes, r)
CB = {"consulta_id": "CON-9", "correlation_id": "COR-CON-9", "tipo": "ANALIZAR", "bloque": "C", "cartera": None, "analisis": [],
      "pregunta": "¿cómo está el euro frente al dólar esta semana?"}
for kw in ({"cartera": ["TACTICA"]}, {"tipo": ["ANALIZAR"]}, {"bloque": {"C": 1}}, {"analisis": [["EV-SOB-0001"]]},
           {"analisis": "EV-SOB-0001"}, {"pregunta": None}, {"analisis": [float("nan")]}):
    r = o.consultar({**CB, **kw}, "BROKER", AHORA)
    chk(f"b_consultar_{list(kw)[0]}_{type(list(kw.values())[0]).__name__}_rechaza_sin_estado", not r["ok"] and foto(o) == antes,
        (r, foto(o) == antes))

# c) analisis_vigentes no muta
o = nuevo()
assert o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
assert o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA)["ok"]
assert o.entregar_sobre("EXP-0001", sobre_para(1, None), AHORA)["ok"]
antes = copy.deepcopy(o.__dict__)
reg = o.analisis_vigentes(AHORA)
reg2 = o.analisis_vigentes("no-es-una-fecha")
reg3 = o.analisis_vigentes(AHORA, cartera=["TACTICA"])
chk("c_analisis_vigentes_no_muta", o.__dict__ == antes)
chk("c_analisis_vigentes_ilegible_da_lista_vacia", reg2 == [] and isinstance(reg3, list), (reg2, reg3))
o.expedientes["EXP-0001"]["sobre"]["valid_until"] = None   # estado roto: no lanza
chk("c_analisis_vigentes_con_estado_roto_no_lanza", isinstance(o.analisis_vigentes(AHORA), list))

# d) diario
CE = {**ENTRADA, "ventana_hasta": "2026-11-06T09:30:00+00:00"}
T1, T2 = "2026-11-06T09:40:00+00:00", "2026-11-06T09:50:00+00:00"
with tempfile.TemporaryDirectory() as tmp:
    o = nuevo()
    rd = di.crear(o, Path(tmp) / "e.json", Path(tmp) / "d.jsonl", AHORA)
    D = rd["diario"]
    for n in (1, 2):
        assert D.detectar(f"EXP-000{n}", f"COR-000{n}", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
        assert D.emitir_encargo(f"EXP-000{n}", encargo(n), "GESTOR_TACTICA", AHORA)["ok"]
        assert D.entregar_sobre(f"EXP-000{n}", sobre_para(n, None), AHORA)["ok"]
    assert D.observar("EXP-0001", COND_OBS, "el operador lo aparta", "OPERADOR", AHORA)["ok"]
    rs = [D.consultar({**CB, "analisis": ["EV-SOB-0001"], "cartera": "TACTICA"}, "BROKER", AHORA)]
    rs.append(D.abrir_directa("EXP-DE-01", "COR-DE-01", "TACTICA", "E", "BROKER", AHORA, analisis="EV-SOB-0001",
                              motivo="candidato único: el resto no encaja con la tesis", consulta_id="CON-9"))   # O-22: EXP-0002 vivo
    sc5 = len(D._o.consultas["entradas"])
    assert D.descartar("EXP-0002", "el operador descarta al rival", "OPERADOR", AHORA)["ok"]
    rs.append(D.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001", consulta_id="CON-9"))
    rs.append(D.comparar(["EXP-DD-01"], "D", AHORA))
    rs.append(D.proponer("EXP-DD-01", CE, SALIDA, "BROKER", AHORA, dim(D, "EXP-DD-01", entrada=CE)))
    rs.append(D.barrer(T1))
    e3 = encargo(1, producer="BROKER")
    e3["expediente_id"], e3["correlation_id"], e3["event_id"] = "EXP-DD-01", "COR-DD-01", "EV-ENC-DD-01-B"
    rs.append(D.emitir_encargo("EXP-DD-01", e3, "BROKER", T2))
    s2 = sobre_para(1, None)
    s2["expediente_id"], s2["correlation_id"], s2["event_id"] = "EXP-DD-01", "COR-DD-01", "EV-SOB-DD-01-B"
    rs.append(D.entregar_sobre("EXP-DD-01", s2, T2))
    rs.append(D.abrir_directa("EXP-DD-02", "COR-DD-02", "TACTICA", "D", "BROKER", T2, analisis="EV-SOB-0001", consulta_id="CON-9"))
    rs.append(D.abrir_directa("EXP-DD-03", "COR-DD-03", "TACTICA", ["D"], "BROKER", T2, analisis="EV-SOB-0001"))
    print("d) diario:", [(r["ok"], r["codigo"]) for r in rs])
    chk("d_E_devuelto_a_D_retira_la_apertura", rs[1]["codigo"] == "O-22" and sc5 == 1 and "EXP-DE-01" not in D._o.expedientes, (rs[1], sc5))
    chk("d_integridad_vacia", D._o.integridad() == [], D._o.integridad())
    ra = di.abrir(Path(tmp) / "e.json", Path(tmp) / "d.jsonl")
    chk("d_diario_reproduce_igual", ra.get("ok") and pe.volcar(ra["diario"]._o, T2) == pe.volcar(D._o, T2), ra.get("motivo"))
    rc = pe.cargar(pe.volcar(D._o, T2))
    chk("d_guardar_y_cargar_integro", rc["ok"] and rc["orquestador"].integridad() == [], rc.get("motivo"))
sys.exit(fin())
