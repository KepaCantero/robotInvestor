"""QA r02 de T-125 (revisor sin contexto): el camino Analista/Buscador → F2 → Evaluador → FUE- → CT-19 en ciclos en vivo con
el cliente simulado, y ataques a la entrada (fechas raras, registro tardío, fuentes falsas, duplicados, determinismo).

Uso, desde `bloque_a/11_Ejecutor`:  QA_TMP=<carpeta temporal> python ../../.docs/tickets/T-125/revisores/r02_01_ataques_ciclo.py
Cada bloque imprime una línea «Bnn · qué · obtenido». No escribe nada fuera de QA_TMP.
"""
import json
import os
import sys
import tempfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path.cwd() / "tests"))
from conftest import AS_OF, RUTA_UNIVERSO_EJEMPLO, cargar_universo, config_pruebas, nuevo_bloque  # noqa: E402
from bloque_a import mock_respuestas  # noqa: E402
from bloque_a.evaluador import motivo_pronostico_fuente_no_registrable  # noqa: E402
from bloque_a.referencias import Referencias  # noqa: E402

UNIVERSO = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
TMP = os.environ.get("QA_TMP")
F9A, F9B = "REF-RF-0001", "REF-RF-0003"
FICHA0, BUSQ0, ANAL0 = mock_respuestas._ficha, mock_respuestas._busqueda, mock_respuestas._analista
C1, C2 = "2026-04-03", AS_OF


def bloque(etiqueta):
    return nuevo_bloque(Path(tempfile.mkdtemp(prefix=f"qa10_t125_{etiqueta}_", dir=TMP)), UNIVERSO, cfg=config_pruebas(modo="vivo"))


def con_ficha(extra):
    """El Analista simulado añade a cada finalista las afirmaciones que devuelve `extra(sym, hoy)`."""
    def ficha(u, msg, ctx, rng, inyectado):
        f = FICHA0(u, msg, ctx, rng, inyectado)
        f["afirmaciones"].extend(extra(f["indicador_seguimiento"]["simbolo"], pd.Timestamp(ctx["fecha_as_of"])))
        return f
    mock_respuestas._ficha = ficha


def restaurar():
    mock_respuestas._ficha, mock_respuestas._busqueda, mock_respuestas._analista = FICHA0, BUSQ0, ANAL0


def pf(ref, sym, obj, umbral, emision, direccion="por_encima", prob=0.8):
    d = {"ref_id": ref, "variable": "cierre", "serie_ht01": sym, "fecha_objetivo": obj, "umbral_o_rango": umbral,
         "direccion": direccion, "fecha_emision": emision}
    if prob is not None:
        d["probabilidad"] = prob
    return d


def af(texto, fuente, bloque_pf):
    return {"afirmacion": texto, "fuente": fuente, "direccion": "favorable", "pronostico_fuente": bloque_pf}


def bd(hoy, k):
    return str((hoy + pd.offsets.BDay(k)).date())


def clm_con_bloque(b):
    return [c for c in b.almacen.estado("F2", clave="clm_id").values() if isinstance(c.get("pronostico_fuente"), dict)]


def rechazos(b):
    return [e["detalle"] for e in b.almacen.leer("HA") if "Pronóstico de fuente no registrable" in str(e.get("detalle"))]


def resumen_fue(b, r):
    return [(f["ref_id"], f["n"], f["aciertos"], f["bss"], f["puntos_historial"], bool(f["calc_id"])) for f in r["evaluacion"]["fiabilidad_fuentes"]]


# ------------------------------------------------------------------ B01 · camino entero, con la cifra del Motor comprobada a mano
def mezcla(sym, hoy):   # 5 aciertos seguros (umbral 1) y 5 fallos seguros (umbral 1e9) por finalista, con prob 0,8
    return [af(f"{F9A} prevé {sym} > {u:g} el {bd(hoy, k)}", F9A, pf(F9A, sym, bd(hoy, k), u, str(hoy.date())))
            for k in (3, 6) for u in (1.0, 1e9)]


def camino(etiqueta):
    con_ficha(mezcla)
    b = bloque(etiqueta)
    r1 = b.ciclo(C1, alcance={"clases": ["RV"]})
    r2 = b.ciclo(C2, alcance={"clases": ["RV"]})
    restaurar()
    return b, r1, r2


b, r1, r2 = camino("b01")
cb = clm_con_bloque(b)
reg = {e["clm_id"]: e["_fecha"] for e in b.almacen.leer("F2") if e.get("tipo_entrada") == "CLM" and isinstance(e.get("pronostico_fuente"), dict)}
print(f"B01a · ciclo {C1}: {r1['estado']} · CLM con bloque en F2: {len(cb)} · tipos {sorted({c['tipo_afirmacion'] for c in cb})} · "
      f"fechas de registro {sorted(set(reg.values()))} · FUE- en C1: {r1['evaluacion']['fiabilidad_fuentes']}")
fue = r2["evaluacion"]["fiabilidad_fuentes"]
print(f"B01b · ciclo {C2}: {r2['estado']} · FUE-: {resumen_fue(b, r2)}")
if fue:
    f = fue[0]
    ps = b.evaluador.pronosticos_de_fuentes(C2)
    brier = sum((p["prob"] - p["resultado"]) ** 2 for p in ps) / len(ps)
    brier_ref = sum((0.5 - p["resultado"]) ** 2 for p in ps) / len(ps)
    rc = [e for e in b.almacen.leer("RC") if e.get("calc_id") == f["calc_id"]]
    rc_ops = [((e.get("operacion") or {}).get("ficha_id"), e.get("run_id"), e.get("solicitante")) for e in rc]
    ct19 = [m for m in b.mensajeria.registro if m["contrato"] == "CT-19" and m["receptor"] == "AG-16"]
    f6 = b.almacen.estado("F6", clave="id")[f["fue_id"]]
    print(f"B01c · BSS a mano {1 - brier / brier_ref:.6f} frente a FUE- {f['bss']} · calc_id {f['calc_id']} en RC: {rc_ops} · "
          f"CT-19 a AG-16: {[m['msg_id'] for m in ct19]} · anotado {f6['comunicado_ct19']} · run del ciclo {r2['run_id']}")

# ------------------------------------------------------------------ B02 · determinismo: el mismo escenario en dos almacenes
b2, _, r2b = camino("b02")
uno = json.dumps([{k: v for k, v in x.items()} for x in r2["evaluacion"]["fiabilidad_fuentes"]], sort_keys=True, default=str)
dos = json.dumps([{k: v for k, v in x.items()} for x in r2b["evaluacion"]["fiabilidad_fuentes"]], sort_keys=True, default=str)
f2a = json.dumps(sorted((c["clm_id"], c["pronostico_fuente"]) for c in cb), default=str)
f2b = json.dumps(sorted((c["clm_id"], c["pronostico_fuente"]) for c in clm_con_bloque(b2)), default=str)
print(f"B02 · FUE- idénticas: {uno == dos} · bloques de F2 idénticos: {f2a == f2b}")

# ------------------------------------------------------------------ B03 · fechas raras en el alta (función de registro)
refs = Referencias(config_pruebas())
base = pf(F9A, "SPY", "2026-07-01", 1.0, "2026-06-01")
casos = {"objetivo 'tomorrow'": {"fecha_objetivo": "tomorrow"}, "objetivo 'now'": {"fecha_objetivo": "now"},
         "emisión 'today'": {"fecha_emision": "today"}, "emisión 'yesterday'": {"fecha_emision": "yesterday"},
         "objetivo '2026'": {"fecha_objetivo": "2026"}, "objetivo '2026-07'": {"fecha_objetivo": "2026-07"},
         "objetivo 'July 1 2026'": {"fecha_objetivo": "July 1 2026"}, "objetivo '1/7/2026'": {"fecha_objetivo": "1/7/2026"},
         "objetivo '20260701'": {"fecha_objetivo": "20260701"}, "objetivo '2026-07-01T23:00-12:00'": {"fecha_objetivo": "2026-07-01T23:00-12:00"},
         "objetivo '9999-12-31'": {"fecha_objetivo": "9999-12-31"}, "objetivo ''": {"fecha_objetivo": ""},
         "objetivo 'NaT'": {"fecha_objetivo": "NaT"}, "objetivo None": {"fecha_objetivo": None}}
out = []
for nombre, cambio in casos.items():
    m = motivo_pronostico_fuente_no_registrable({**base, **cambio}, F9A, "2026-06-05", refs)
    out.append(f"{nombre} → {'REGISTRABLE' if m is None else m[:40]}")
print("B03 · " + " | ".join(out))

# ------------------------------------------------------------------ B04 · palabras relativas: la fecha sale del reloj de la máquina
from bloque_a.evaluador import _fecha_de_calendario  # noqa: E402

lect = {t: str(_fecha_de_calendario(t).date()) for t in ("now", "today", "1/7/2026", "July 1 2026", "2026")}
hoy_maquina = pd.Timestamp.now().date()
m_hoy = motivo_pronostico_fuente_no_registrable({**base, "fecha_emision": "today", "fecha_objetivo": str(hoy_maquina + pd.Timedelta(days=10))},
                                                F9A, str(hoy_maquina + pd.Timedelta(days=3)), refs)
print(f"B04 · lecturas {lect} (máquina: {hoy_maquina}) · emisión «today» con registro a +3 días y objetivo a +10: "
      f"{'REGISTRABLE' if m_hoy is None else m_hoy} (el mismo bloque, leído otro día, da otra fecha de emisión)")

# ------------------------------------------------------------------ B05 · registro tardío y fechas en el borde, en el ciclo
def bordes(sym, hoy):
    d = str(hoy.date())
    return [af(f"{F9A} {sym} objetivo hoy", F9A, pf(F9A, sym, d, 1.0, bd(hoy, -5))),
            af(f"{F9A} {sym} objetivo ayer", F9A, pf(F9A, sym, bd(hoy, -1), 1.0, bd(hoy, -5))),
            af(f"{F9A} {sym} emitido mañana", F9A, pf(F9A, sym, bd(hoy, 5), 1.0, bd(hoy, 1))),
            af(f"{F9A} {sym} objetivo mañana", F9A, pf(F9A, sym, bd(hoy, 1), 1.0, d))]


con_ficha(bordes)
b5 = bloque("b05")
b5.ciclo(C1, alcance={"clases": ["RV"]})
restaurar()
print(f"B05 · objetivo hoy/ayer, emitido mañana, objetivo mañana: con bloque {sorted({c['afirmacion'].split(' objetivo ')[-1] if 'objetivo' in c['afirmacion'] else c['afirmacion'] for c in clm_con_bloque(b5)})} · "
      f"motivos en HA {sorted({d.split('(')[1].split(')')[0] for d in rechazos(b5)})}")

# ------------------------------------------------------------------ B06 · fuentes falsas
def falsas(sym, hoy):
    o, e = bd(hoy, 5), str(hoy.date())
    return [af(f"x1 {sym}", F9A, pf(F9B, sym, o, 1.0, e)),                       # el bloque dice otra fuente de F9
            af(f"x2 {sym}", "REF-ANA-DOC-0061", pf("REF-ANA-DOC-0061", sym, o, 1.0, e)),   # F7
            af(f"x3 {sym}", "REF-RF-9999", pf("REF-RF-9999", sym, o, 1.0, e)),   # no existe
            af(f"x4 {sym}", f"HT-01:{sym}", pf(F9A, sym, o, 1.0, e)),            # dato de mercado con bloque de F9
            af(f"x5 {sym}", F9A, pf(F9A, sym, o, 1.0, e, direccion={"x": 1})),  # dirección no hashable
            af(f"x6 {sym}", F9A, pf(F9A, ["SPY"], o, 1.0, e))]                   # serie no textual


con_ficha(falsas)
b6 = bloque("b06")
r6 = b6.ciclo(C1, alcance={"clases": ["RV"]})
restaurar()
print(f"B06 · ciclo {r6['estado']} · con bloque: {[c['afirmacion'][:2] for c in clm_con_bloque(b6)]} · "
      f"motivos {sorted({d.split('(')[1].split(')')[0][:45] for d in rechazos(b6)})}")

# ------------------------------------------------------------------ B07 · duplicados
def dup(sym, hoy):
    o, e = bd(hoy, 5), str(hoy.date())
    return [af(f"{F9A} dice A de {sym}", F9A, pf(F9A, sym, o, 1.0, e)),
            af(f"{F9A} dice B de {sym}", F9A, pf(F9A, sym, o, 1.0, e)),            # el mismo bloque, otro texto
            af(f"{F9A} dice C de {sym}", F9A, pf(F9A, sym, o, 1, e)),              # el mismo con umbral entero
            af(f"{F9A} dice D de {sym}", F9A, pf(F9A, sym, o + "T00:00:00", 1.0, e))]   # la misma fecha con hora


con_ficha(dup)
b7 = bloque("b07")
b7.ciclo(C1, alcance={"clases": ["RV"]})
restaurar()
b7.fijar_fecha(C2)   # el proveedor, con datos hasta el corte de la evaluación
ps7 = b7.evaluador.pronosticos_de_fuentes(C2)
por_serie: dict = {}
for p in ps7:
    por_serie.setdefault(p["fecha_objetivo"], []).append(p["clm_id"])
print(f"B07 · CLM con bloque {len(clm_con_bloque(b7))} · pronósticos que cuentan {len(ps7)} para "
      f"{len({c['pronostico_fuente']['serie_ht01'] for c in clm_con_bloque(b7)})} series (lo esperado: uno por serie)")

# ------------------------------------------------------------------ B08 · el mismo pronóstico citado en dos ciclos con textos distintos
def ciclo_a(sym, hoy):
    return [af(f"{F9A} (ciclo 1) sobre {sym}", F9A, pf(F9A, sym, "2026-06-01", 1.0, "2026-04-03"))]


def ciclo_b(sym, hoy):
    return [af(f"{F9A} (ciclo 2, otra cita) sobre {sym}", F9A, pf(F9A, sym, "2026-06-01", 1.0, "2026-04-03"))]


b8 = bloque("b08")
con_ficha(ciclo_a)
b8.ciclo(C1, alcance={"clases": ["RV"]})
con_ficha(ciclo_b)
b8.ciclo("2026-04-10", alcance={"clases": ["RV"]})
restaurar()
b8.fijar_fecha(C2)
n8 = len(clm_con_bloque(b8))
c8 = len(b8.evaluador.pronosticos_de_fuentes(C2))
print(f"B08 · CLM con bloque {n8} · cuentan {c8} (una por serie: {len({c['pronostico_fuente']['serie_ht01'] for c in clm_con_bloque(b8)})})")

# ------------------------------------------------------------------ B09 · el Buscador en backtest y en vivo
def analista(msg, ctx, rng, inyectado):
    r = ANAL0(msg, ctx, rng, inyectado)
    for f in r.get("finalistas", []):
        f["peticiones_conocimiento"] = [{"tipo": "CT-07", "pregunta": "¿Qué prevén las fuentes?", "objetivo": "confirmar"}]
    return r


def busqueda(msg, ctx, rng):
    hoy = pd.Timestamp(ctx["fecha_as_of"])
    refs_ = [{"ref_id": r["ref_id"], "afirmacion": f"{r['ref_id']} prevé {msg['para']} > 1", "direccion": "favorable",
              "pronostico_fuente": pf(r["ref_id"], msg["para"], bd(hoy, 5), 1.0, str(hoy.date()))}
             for r in (msg.get("referencias_candidatas") or [])[:2]]
    return {"referencias": refs_, "sintesis": "x", "contradicciones": [], "lagunas": []}


for modo in ("backtest", "vivo"):
    mock_respuestas._analista, mock_respuestas._busqueda = analista, busqueda
    b9 = nuevo_bloque(Path(tempfile.mkdtemp(prefix=f"qa10_t125_b09{modo}_", dir=TMP)), UNIVERSO, cfg=config_pruebas(modo=modo))
    b9.ciclo(C1, alcance={"clases": ["RV"]})
    restaurar()
    print(f"B09 · Buscador en {modo}: CLM con bloque {len(clm_con_bloque(b9))} · ref_id {sorted({c['pronostico_fuente']['ref_id'] for c in clm_con_bloque(b9)})} · "
          f"rechazos {len(rechazos(b9))}")

# ------------------------------------------------------------------ B10 · F2 manipulado: una pieza con dirección no hashable
b10 = bloque("b10")
b10.fijar_fecha(C2)
for i, d in enumerate(pd.bdate_range("2025-01-06", periods=6)):
    b10.reloj.fijar("2024-12-01")
    _, v = b10.proveedor.valor_en("SPY", d)
    b10.almacen.escribir("F2", "AG-12", {"tipo_entrada": "CLM", "clm_id": f"CLM-2024-{i:04d}", "afirmacion": f"m{i}", "tipo_afirmacion": "PRONOSTICO_FUENTE",
                                         "pronostico_fuente": pf(F9A, "SPY", str(d.date()), v - 1, "2024-12-01")})
b10.almacen.escribir("F2", "AG-12", {"tipo_entrada": "CLM", "clm_id": "CLM-2024-0999", "afirmacion": "raro", "tipo_afirmacion": "PRONOSTICO_FUENTE",
                                     "pronostico_fuente": pf(F9B, "SPY", "2025-02-03", 1.0, "2024-12-01", direccion=["por_encima"])})
b10.reloj.fijar(C2)
try:
    salida = b10.evaluador.fiabilidad_fuentes(C2)
    print(f"B10 · F2 con un bloque de dirección no hashable (otra fuente): FUE- {[x['ref_id'] for x in salida]}")
except Exception as e:  # noqa: BLE001
    print(f"B10 · F2 con un bloque de dirección no hashable (otra fuente): EXCEPCIÓN {type(e).__name__}: {e} — se pierde la FUE- de {F9A}")

# ------------------------------------------------------------------ B11 · «now» y «1/7/2026» en un ciclo: ¿entran en F2?
def relativas(sym, hoy):
    return [af(f"{F9A} prevé {sym} > 1 «now»", F9A, pf(F9A, sym, "now", 1.0, str(hoy.date()))),
            af(f"{F9A} prevé {sym} > 1 el 1/7/2026", F9A, pf(F9A, sym, "1/7/2026", 1.0, str(hoy.date()))),
            af(f"{F9A} prevé {sym} > 1 el July 1 2026", F9A, pf(F9A, sym, "July 1 2026", 1.0, str(hoy.date())))]


con_ficha(relativas)
b11 = bloque("b11")
b11.ciclo(C1, alcance={"clases": ["RV"]})
restaurar()
print(f"B11 · ciclo {C1}: fechas objetivo guardadas en F2 {sorted({c['pronostico_fuente']['fecha_objetivo'] for c in clm_con_bloque(b11)})} · "
      f"rechazos {sorted({d.split('(')[1].split(')')[0][:50] for d in rechazos(b11)})}")

# ------------------------------------------------------------------ B12 · el campo `variable` no se mira
sin_variable = {k: v for k, v in base.items() if k != "variable"}
print(f"B12a · alta sin `variable`: {motivo_pronostico_fuente_no_registrable(sin_variable, F9A, '2026-06-05', refs) or 'REGISTRABLE'} · "
      f"con variable «rentabilidad_12m»: {motivo_pronostico_fuente_no_registrable({**base, 'variable': 'rentabilidad_12m'}, F9A, '2026-06-05', refs) or 'REGISTRABLE'}")
b12 = bloque("b12")
b12.fijar_fecha(C2)
for i, d in enumerate(pd.bdate_range("2025-01-06", periods=5)):
    b12.reloj.fijar("2024-12-01")
    # «la rentabilidad a 12 meses de SPY superará el 5 %», con probabilidad 0,9
    b12.almacen.escribir("F2", "AG-12", {"tipo_entrada": "CLM", "clm_id": f"CLM-2024-{i:04d}", "afirmacion": f"r{i}", "tipo_afirmacion": "PRONOSTICO_FUENTE",
                                         "pronostico_fuente": {**pf(F9A, "SPY", str(d.date()), 0.05, "2024-12-01", prob=0.9), "variable": "rentabilidad_12m"}})
b12.reloj.fijar(C2)
ps12 = b12.evaluador.pronosticos_de_fuentes(C2)
print(f"B12b · cinco pronósticos de «rentabilidad_12m > 0,05»: resueltos {len(ps12)} con valor {sorted({round(p['valor'], 2) for p in ps12})[:3]}… "
      f"(el cierre, no la rentabilidad) · resultados {[p['resultado'] for p in ps12]} · FUE- {[(f['n'], f['aciertos'], f['puntos_historial']) for f in b12.evaluador.fiabilidad_fuentes(C2)]}")
