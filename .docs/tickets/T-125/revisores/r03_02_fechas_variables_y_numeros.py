"""QA r03 de T-125 (revisor sin contexto): lo que la r03 cambia (fechas solo ISO, `variable` resoluble, umbral como número,
dirección no textual, `run_id`) atacado por los bordes: ISO válidas que deben seguir leyéndose (también en un ciclo),
formatos que aún se cuelan, variables raras, configuración de `variables_nivel` mal formada o distinta de la de por defecto,
números enormes en el umbral o la probabilidad (en el alta de un ciclo y en un F2 manipulado).

Uso, desde `bloque_a/11_Ejecutor`:  QA_TMP=<carpeta temporal> python ../../.docs/tickets/T-125/revisores/r03_02_fechas_variables_y_numeros.py
Cada bloque imprime «Nnn · qué · obtenido». No escribe nada fuera de QA_TMP.
"""
import copy
import os
import sys
import tempfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path.cwd() / "tests"))
from conftest import AS_OF, RUTA_UNIVERSO_EJEMPLO, cargar_universo, config_pruebas, nuevo_bloque  # noqa: E402
from bloque_a import mock_respuestas  # noqa: E402
from bloque_a.evaluador import _fecha_de_calendario, motivo_pronostico_fuente_no_registrable, variable_resoluble  # noqa: E402
from bloque_a.referencias import Referencias  # noqa: E402

UNIVERSO = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
TMP = os.environ.get("QA_TMP")
F9A = "REF-RF-0001"
FICHA0 = mock_respuestas._ficha
C1, C2 = "2026-04-03", AS_OF
VARS = ["nivel", "cierre", "precio"]


def bloque(etiqueta, cfg=None):
    return nuevo_bloque(Path(tempfile.mkdtemp(prefix=f"qa12_t125_{etiqueta}_", dir=TMP)), UNIVERSO, cfg=cfg or config_pruebas(modo="vivo"))


def con_ficha(extra):
    def ficha(u, msg, ctx, rng, inyectado):
        f = FICHA0(u, msg, ctx, rng, inyectado)
        f["afirmaciones"].extend(extra(f["indicador_seguimiento"]["simbolo"], pd.Timestamp(ctx["fecha_as_of"])))
        return f
    mock_respuestas._ficha = ficha


def restaurar():
    mock_respuestas._ficha = FICHA0


def pf(sym, obj, umbral, emision, direccion="por_encima", prob=0.8, variable="cierre"):
    return {"ref_id": F9A, "variable": variable, "serie_ht01": sym, "fecha_objetivo": obj, "umbral_o_rango": umbral,
            "direccion": direccion, "fecha_emision": emision, "probabilidad": prob}


def af(texto, bloque_pf):
    return {"afirmacion": texto, "fuente": F9A, "direccion": "favorable", "pronostico_fuente": bloque_pf}


def bd(hoy, k):
    return str((hoy + pd.offsets.BDay(k)).date())


def con_bloque(b):
    return [c for c in b.almacen.estado("F2", clave="clm_id").values() if isinstance(c.get("pronostico_fuente"), dict)]


def rechazos(b):
    return sorted({e["detalle"].split("(", 1)[1].split(")")[0][:60] for e in b.almacen.leer("HA")
                   if "Pronóstico de fuente no registrable" in str(e.get("detalle"))})


def lectura(v):
    try:
        return str(_fecha_de_calendario(v).date())
    except Exception as e:  # noqa: BLE001
        return f"{type(e).__name__}"


refs = Referencias(config_pruebas())
base = pf("SPY", "2026-07-01", 1.0, "2026-06-01")


def motivo(cambio, variables=VARS):
    try:
        m = motivo_pronostico_fuente_no_registrable({**base, **cambio}, F9A, "2026-06-05", refs, variables)
        return "REGISTRABLE" if m is None else m[:50]
    except Exception as e:  # noqa: BLE001
        return f"EXCEPCIÓN {type(e).__name__}: {str(e)[:50]}"


# ------------------------------------------------------------------ N01 · ISO válidas: se siguen leyendo
validas = ["2026-07-01", " 2026-07-01 ", "2026-07-01T10:30", "2026-07-01 10:30:15", "2026-07-01T10:30:15.123456",
           "2026-07-01T23:30:00+05:00", "2026-07-01T00:10:00Z", "2026-07-01T10:00+0500", "2026-07-01T23:59:59-12:00"]
print("N01a · " + " | ".join(f"{v!r} → {lectura(v)}" for v in validas))


def iso_con_hora(sym, hoy):
    return [af(f"{F9A} {sym} con hora", pf(sym, bd(hoy, 3) + "T16:00", 1.0, str(hoy.date()))),
            af(f"{F9A} {sym} con zona", pf(sym, bd(hoy, 4) + "T16:00:00+02:00", 1.0, str(hoy.date()) + "T08:00Z")),
            af(f"{F9A} {sym} con Z", pf(sym, bd(hoy, 5) + "T00:00:00Z", 1e9, str(hoy.date())))]


con_ficha(iso_con_hora)
b1 = bloque("n01")
b1.ciclo(C1, alcance={"clases": ["RV"]})
restaurar()
b1.fijar_fecha(C2)
ps1 = b1.evaluador.pronosticos_de_fuentes(C2)
print(f"N01b · ciclo con objetivos ISO con hora, zona y Z: en F2 {len(con_bloque(b1))} · rechazos {rechazos(b1)} · "
      f"cuentan {len(ps1)} · resultados {sorted({(p['fecha_objetivo'], p['resultado']) for p in ps1})[:3]}…")

# ------------------------------------------------------------------ N02 · formatos que aún se cuelan
raras = {"cifras de ancho completo": "２０２６-０７-０１", "cifras árabes orientales": "٢٠٢٦-٠٧-٠١",
         "cifras devanagari": "२०२६-०७-०१", "zona sin hora": "2026-07-01-05:00", "zona +14": "2026-07-01T10:00+14:00",
         "año 9999": "9999-12-31", "año 0001": "0001-01-01", "espacio Unicode delante": " 2026-07-01"}
print("N02a · " + " | ".join(f"{k} {v!r} → {lectura(v)} / alta {motivo({'fecha_objetivo': v})}" for k, v in raras.items()))


def cifras_raras(sym, hoy):
    o = bd(hoy, 3)
    ancho = o.translate(str.maketrans("0123456789", "０１２３４５６７８９"))
    return [af(f"{F9A} {sym} ancho completo", pf(sym, ancho, 1.0, str(hoy.date())))]


con_ficha(cifras_raras)
b2 = bloque("n02")
b2.ciclo(C1, alcance={"clases": ["RV"]})
restaurar()
b2.fijar_fecha(C2)
print(f"N02b · ciclo con fecha objetivo en cifras de ancho completo: guardadas en F2 "
      f"{sorted({c['pronostico_fuente']['fecha_objetivo'] for c in con_bloque(b2)})} · cuentan {len(b2.evaluador.pronosticos_de_fuentes(C2))}")

# ------------------------------------------------------------------ N03 · variables
var = ["cierre", "CIERRE", " precio\n", "Nivel", "cierre​", "cierre_ajustado", "rentabilidad", "close", "nivel ", "c", "", None, 1, ["cierre"]]
print("N03a · " + " | ".join(f"{v!r} → {variable_resoluble(v, VARS)}" for v in var))
print(f"N03b · variables_nivel mal formada: texto «cierre» y variable «c» → {motivo({'variable': 'c'}, 'cierre')} · "
      f"None → {motivo({}, None)} (None usa la de por defecto) · [] → {motivo({}, [])} · número 5 → {motivo({}, 5)}")

# configuración propia: solo «cierre»; ¿la respeta el alta del ciclo (orquestacion) y el Evaluador?
cfg = copy.deepcopy(config_pruebas(modo="vivo"))
cfg["fiabilidad_fuentes"]["variables_nivel"] = ["cierre"]


def dos_variables(sym, hoy):
    return [af(f"{F9A} {sym} cierre", pf(sym, bd(hoy, 3), 1.0, str(hoy.date()))),
            af(f"{F9A} {sym} precio", pf(sym, bd(hoy, 4), 1.0, str(hoy.date()), variable="precio"))]


con_ficha(dos_variables)
b3 = bloque("n03", cfg)
b3.ciclo(C1, alcance={"clases": ["RV"]})
restaurar()
print(f"N03c · configuración con variables_nivel [cierre]: variables en F2 {sorted({c['pronostico_fuente']['variable'] for c in con_bloque(b3)})} · "
      f"rechazos {rechazos(b3)}")
# la configuración se estrecha después del registro: ¿el Evaluador deja de contar los «precio» ya guardados?
con_ficha(dos_variables)
b3b = bloque("n03b")
b3b.ciclo(C1, alcance={"clases": ["RV"]})
restaurar()
b3b.fijar_fecha(C2)
antes = len(b3b.evaluador.pronosticos_de_fuentes(C2))
b3b.evaluador.cfg = cfg
despues = len(b3b.evaluador.pronosticos_de_fuentes(C2))
print(f"N03d · registrados con [nivel, cierre, precio]: cuentan {antes}; evaluados con [cierre]: {despues}")

# ------------------------------------------------------------------ N04 · números enormes (un entero de 400 cifras es JSON válido)
GRANDE = 10 ** 400
print(f"N04a · alta: umbral 10^400 → {motivo({'umbral_o_rango': GRANDE})} · rango [0, 10^400] → "
      f"{motivo({'umbral_o_rango': [0, GRANDE], 'direccion': 'dentro'})} · probabilidad 10^400 → {motivo({'probabilidad': GRANDE})} · "
      f"umbral 1e400 (inf) → {motivo({'umbral_o_rango': float('inf')})} · umbral True → {motivo({'umbral_o_rango': True})}")


def enorme(sym, hoy):
    return [af(f"{F9A} {sym} sano", pf(sym, bd(hoy, 3), 1.0, str(hoy.date()))),
            af(f"{F9A} {sym} enorme", pf(sym, bd(hoy, 4), GRANDE, str(hoy.date())))]


con_ficha(enorme)
b4 = bloque("n04")
try:
    r4 = b4.ciclo(C1, alcance={"clases": ["RV"]})
    estado4 = r4["estado"]
except Exception as e:  # noqa: BLE001
    estado4 = f"EXCEPCIÓN {type(e).__name__}: {str(e)[:60]}"
restaurar()
inc4 = [e["detalle"][:90] for e in b4.almacen.leer("HA") if "int too large" in str(e.get("detalle")) or "Overflow" in str(e.get("detalle"))]
print(f"N04b · ciclo con un umbral de 400 cifras (y uno sano) en cada finalista: {estado4} · en F2 con bloque {len(con_bloque(b4))} · "
      f"rechazos {rechazos(b4)} · incidencias por desbordamiento {inc4[:2]}")

# F2 manipulado: seis pronósticos sanos y uno con umbral de 400 cifras
b5 = bloque("n05")
b5.fijar_fecha(C2)
for i, d in enumerate(pd.bdate_range("2025-01-06", periods=6)):
    b5.reloj.fijar("2024-12-01")
    _, v = b5.proveedor.valor_en("SPY", d)
    b5.almacen.escribir("F2", "AG-12", {"tipo_entrada": "CLM", "clm_id": f"CLM-2024-{i:04d}", "afirmacion": f"m{i}",
                                        "tipo_afirmacion": "PRONOSTICO_FUENTE", "pronostico_fuente": pf("SPY", str(d.date()), v - 1, "2024-12-01")})
b5.almacen.escribir("F2", "AG-12", {"tipo_entrada": "CLM", "clm_id": "CLM-2024-0999", "afirmacion": "enorme", "tipo_afirmacion": "PRONOSTICO_FUENTE",
                                    "pronostico_fuente": pf("SPY", "2025-02-03", GRANDE, "2024-12-01")})
b5.reloj.fijar(C2)
try:
    print(f"N04c · F2 con un umbral de 400 cifras junto a 6 sanos: FUE- {[x['ref_id'] for x in b5.evaluador.fiabilidad_fuentes(C2)]}")
except Exception as e:  # noqa: BLE001
    print(f"N04c · F2 con un umbral de 400 cifras junto a 6 sanos: EXCEPCIÓN {type(e).__name__}: {e} — se pierde la FUE- de la fuente sana")

# ------------------------------------------------------------------ N05 · deduplicación por número
b6 = bloque("n06")
b6.fijar_fecha(C2)
d = pd.Timestamp("2025-01-06")
_, v = b6.proveedor.valor_en("SPY", d)
casos6 = [("CLM-2024-0001", [round(v) - 1, round(v) + 1]), ("CLM-2024-0002", [float(round(v) - 1), float(round(v) + 1)]),
          ("CLM-2024-0003", [0, 1e9]), ("CLM-2024-0004", [-0.0, 1e9]), ("CLM-2024-0005", [0.0, 1e9])]
for cid, u in casos6:
    b6.reloj.fijar("2024-12-01")
    b6.almacen.escribir("F2", "AG-12", {"tipo_entrada": "CLM", "clm_id": cid, "afirmacion": cid, "tipo_afirmacion": "PRONOSTICO_FUENTE",
                                        "pronostico_fuente": pf("SPY", str(d.date()), u, "2024-12-01", direccion="dentro")})
b6.reloj.fijar(C2)
print(f"N05 · rangos [a, b] enteros y decimales, y [0, 1e9] / [-0.0, 1e9] / [0.0, 1e9]: cuentan "
      f"{[p['clm_id'] for p in b6.evaluador.pronosticos_de_fuentes(C2)]} (lo esperado: dos)")
