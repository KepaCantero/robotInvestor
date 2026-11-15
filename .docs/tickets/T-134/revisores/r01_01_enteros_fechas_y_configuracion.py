"""QA r01 de T-134 (revisor sin contexto): lo que corrige T-134 atacado por los bordes, por el mismo camino de H-14 (el bloque
`pronostico_fuente` de una pieza que devuelve el Analista, que el esquema de la respuesta no declara):

 E1 · el alta (`motivo_pronostico_fuente_no_registrable`) con enteros enormes (400 y 4 000 cifras, también negativos, el
      límite de `int`→`str` de Python es 4 300), NaN e infinitos de JSON, listas anidadas y tipos raros en cada campo;
 E2 · fechas «ISO» raras: hora 24, segundo 60, mes 13, 29 de febrero, zona +24:00 o +99:99, zona solo con horas, fracción
      de 13 cifras, años 0000, 0001, 1677, 2262 y 9999, espacios Unicode;
 E3 · un ciclo con todas esas piezas a la vez: ¿acaba COMPLETO y cada rechazo queda en HA?;
 E4 · `pronosticos_de_fuentes` con un F2 que ya trae esos bloques (alta antigua o manipulada);
 E5 · `variables_nivel` mal formada en la configuración: ¿falla al crear el Bloque y no a mitad de ciclo?
Uso, desde `bloque_a/11_Ejecutor`:  QA_TMP=<carpeta temporal> python ../../.docs/tickets/T-134/revisores/r01_01_enteros_fechas_y_configuracion.py
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
from bloque_a.evaluador import _fecha_de_calendario, motivo_pronostico_fuente_no_registrable  # noqa: E402
from bloque_a.referencias import Referencias  # noqa: E402

UNIVERSO = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
TMP = os.environ.get("QA_TMP")
F9A = "REF-RF-0001"
FICHA0 = mock_respuestas._ficha
C1, C2 = "2026-04-03", AS_OF
OK, FALLOS = 0, []
ENORME, GIGANTE = 10 ** 400, 10 ** 4000


def comprobar(cond, msg):
    global OK
    OK += bool(cond)
    if not cond:
        FALLOS.append(msg)
    print(f"  {'ok   ' if cond else 'FALLA'} {msg}")


def pf(sym, obj, umbral, emision, direccion="por_encima", prob=0.8, variable="cierre"):
    return {"ref_id": F9A, "variable": variable, "serie_ht01": sym, "fecha_objetivo": obj, "umbral_o_rango": umbral,
            "direccion": direccion, "fecha_emision": emision, "probabilidad": prob}


refs = Referencias(config_pruebas())
BASE = pf("SPY", "2026-07-01", 1.0, "2026-06-01")


def motivo(cambio):
    try:
        m = motivo_pronostico_fuente_no_registrable({**BASE, **cambio}, F9A, "2026-06-05", refs, ["nivel", "cierre", "precio"])
        return "REGISTRABLE" if m is None else "rechazado"
    except Exception as e:  # noqa: BLE001
        return f"EXCEPCIÓN {type(e).__name__}"


anidada = []
x = anidada
for _ in range(400):
    x.append([])
    x = x[0]

print("E1 · alta con números y tipos raros")
CAMBIOS = {
    "umbral 400 cifras": {"umbral_o_rango": ENORME}, "umbral −400 cifras": {"umbral_o_rango": -ENORME},
    "umbral 4 000 cifras": {"umbral_o_rango": GIGANTE}, "rango [−10^400, 10^400]": {"direccion": "fuera", "umbral_o_rango": [-ENORME, ENORME]},
    "rango [1, 10^4000]": {"direccion": "dentro", "umbral_o_rango": [1, GIGANTE]},
    "rango [10^300, 10^301] (representable)": {"direccion": "dentro", "umbral_o_rango": [10 ** 300, 10 ** 301]},
    "probabilidad 10^400": {"probabilidad": ENORME}, "probabilidad −10^4000": {"probabilidad": -GIGANTE},
    "probabilidad 1e-400 (0.0)": {"probabilidad": float("1e-400")}, "umbral NaN": {"umbral_o_rango": float("nan")},
    "umbral −inf": {"umbral_o_rango": float("-inf")}, "rango [NaN, 1]": {"direccion": "dentro", "umbral_o_rango": [float("nan"), 1]},
    "probabilidad NaN": {"probabilidad": float("nan")}, "umbral lista anidada": {"umbral_o_rango": [[1], [2]]},
    "umbral dict": {"umbral_o_rango": {"a": 1}}, "rango de 3": {"direccion": "dentro", "umbral_o_rango": [1, 2, 3]},
    "variable 4 000 cifras": {"variable": GIGANTE}, "dirección 10^400": {"direccion": ENORME},
    "ref_id 10^400": {"ref_id": ENORME}, "serie 10^400": {"serie_ht01": ENORME},
    "fecha objetivo 10^400": {"fecha_objetivo": ENORME}, "fecha emisión 1e308": {"fecha_emision": 1e308},
    "variable anidada 400 niveles": {"variable": anidada}, "dirección anidada 400 niveles": {"direccion": anidada},
}
esperado_registrable = {"rango [10^300, 10^301] (representable)"}
for k, c in CAMBIOS.items():
    r = motivo(c)
    comprobar(r == ("REGISTRABLE" if k in esperado_registrable else "rechazado"), f"{k:40} → {r}")

print("E2 · fechas raras")
FECHAS = {
    "2026-07-01T24:00": None, "2026-07-01T23:59:60": None, "2026-13-01": None, "2026-02-29": None, "2028-02-29": "2028-02-29",
    "2026-07-01T10:00+24:00": None, "2026-07-01T10:00+99:99": None, "2026-07-01T10:00+05": None,
    "2026-07-01T10:00:00.1234567890123": "2026-07-01", "0000-01-01": None, "0001-01-01": "0001-01-01",
    "1677-09-21": "1677-09-21", "2262-04-12": "2262-04-12", "9999-12-31T23:59:59+14:00": "9999-12-31",
    "0001-01-01T00:00-14:00": "0001-01-01", "　2026-07-01　": "2026-07-01", "2026-07-01\x00": None,
    "2026-07-01T10:00:00,5": None, "+2026-07-01": None, "2026-W27-3": None, "2026-182": None,
}
for v, esperado in FECHAS.items():
    try:
        leida = str(_fecha_de_calendario(v).date())
    except (ValueError, TypeError, OverflowError) as e:
        leida = None if True else e
    except Exception as e:  # noqa: BLE001 — una excepción que `_campos_pronostico_fuente` no captura tumbaría el alta
        leida = f"EXCEPCIÓN {type(e).__name__}"
    alta_obj, alta_emi = motivo({"fecha_objetivo": v}), motivo({"fecha_emision": v})
    sin_excepcion = not str(leida).startswith("EXCEPCIÓN") and "EXCEPCIÓN" not in alta_obj + alta_emi
    comprobar(sin_excepcion and (leida == esperado or (esperado is None and leida is None)),
              f"{v!r:40} → {leida} (esperado {esperado}) · alta objetivo {alta_obj} · emisión {alta_emi}")

print("E3 · un ciclo con todas las piezas raras a la vez")


def bd(hoy, k):
    return str((hoy + pd.offsets.BDay(k)).date())


def raras(sym, hoy):
    o, e = bd(hoy, 3), str(hoy.date())
    out = [{"afirmacion": f"{F9A} {sym} sana", "fuente": F9A, "direccion": "favorable", "pronostico_fuente": pf(sym, o, 1.0, e)}]
    for i, (k, c) in enumerate(CAMBIOS.items()):
        out.append({"afirmacion": f"{F9A} {sym} rara {i}", "fuente": F9A, "direccion": "favorable",
                    "pronostico_fuente": {**pf(sym, o, 1.0, e), **c}})
    for j, v in enumerate(FECHAS):
        out.append({"afirmacion": f"{F9A} {sym} fecha {j}", "fuente": F9A, "direccion": "favorable",
                    "pronostico_fuente": pf(sym, v, 1.0, e)})
    return out


def ficha(u, msg, ctx, rng, inyectado):
    f = FICHA0(u, msg, ctx, rng, inyectado)
    f["afirmaciones"].extend(raras(f["indicador_seguimiento"]["simbolo"], pd.Timestamp(ctx["fecha_as_of"])))
    return f


mock_respuestas._ficha = ficha
try:
    b = nuevo_bloque(Path(tempfile.mkdtemp(prefix="qa14_t134_e3_", dir=TMP)), UNIVERSO, cfg=config_pruebas(modo="vivo"))
    try:
        r = b.ciclo(C1, alcance={"clases": ["RV"]})
        estado = r.get("estado")
    except Exception as e:  # noqa: BLE001
        estado = f"EXCEPCIÓN {type(e).__name__}: {str(e)[:80]}"
finally:
    mock_respuestas._ficha = FICHA0
# con tantas piezas, la Curación (AG-12) puede quedarse sin presupuesto: PARCIAL declarado (R16), no una caída
lim = [x for x in (r.get("paquete") or {}).get("limitaciones", [])] if not str(estado).startswith("EXCEPCIÓN") else []
solo_presupuesto = estado == "PARCIAL" and any(x.startswith("Presupuesto agotado") for x in lim)
comprobar(estado == "COMPLETO" or solo_presupuesto,
          f"ciclo con {len(CAMBIOS) + len(FECHAS)} bloques raros por finalista → {estado}"
          f"{' (presupuesto de AG-12 agotado, declarado)' if solo_presupuesto else ''}")
if estado in ("COMPLETO", "PARCIAL"):
    f2 = [c for c in b.almacen.estado("F2", clave="clm_id").values() if isinstance(c.get("pronostico_fuente"), dict)]
    rech = [e for e in b.almacen.leer("HA") if "Pronóstico de fuente no registrable" in str(e.get("detalle"))]
    registradas = sorted({c["afirmacion"].split(" ", 2)[-1] for c in f2})
    print(f"     en F2 con bloque: {len(f2)} ({registradas[:8]}…) · rechazos en HA: {len(rech)}")
    comprobar(all(json.loads(json.dumps(c["pronostico_fuente"])) == c["pronostico_fuente"] for c in f2),
              "lo registrado en F2 se relee igual (JSON)")
    raros_en_f2 = [c for c in f2 if "rara" in c["afirmacion"] and not c["afirmacion"].endswith(
        str(list(CAMBIOS).index("rango [10^300, 10^301] (representable)")))]
    comprobar(not raros_en_f2, f"ningún bloque con un número no representable o un tipo raro entra en F2 ({len(raros_en_f2)})")
    b.fijar_fecha(C2)
    try:
        n = len(b.evaluador.pronosticos_de_fuentes(C2))
        comprobar(True, f"pronosticos_de_fuentes tras el ciclo: {n} resueltos, sin excepción")
    except Exception as e:  # noqa: BLE001
        comprobar(False, f"pronosticos_de_fuentes tras el ciclo: EXCEPCIÓN {type(e).__name__}")

print("E4 · F2 que ya trae los bloques raros (alta antigua o manipulada), junto a uno sano")
b4 = nuevo_bloque(Path(tempfile.mkdtemp(prefix="qa14_t134_e4_", dir=TMP)), UNIVERSO, cfg=config_pruebas(modo="vivo"))
b4.fijar_fecha("2025-01-02")
sano = pf("SPY", "2025-03-03", 1.0, "2025-01-01")
bloques = [sano] + [{**sano, **c} for c in CAMBIOS.values()] + [pf("SPY", v, 1.0, "2025-01-01") for v in FECHAS] \
    + [pf("SPY", "2025-03-03", 1.0, v) for v in FECHAS]
for i, blq in enumerate(bloques):
    b4.almacen.escribir("F2", "AG-12", {"tipo_entrada": "CLM", "clm_id": f"CLM-2025-{9000 + i}", "afirmacion": f"e4 {i}",
                                        "tipo_afirmacion": "PRONOSTICO_FUENTE", "clase": "RV", "evidencias": [],
                                        "pronostico_fuente": blq})
b4.fijar_fecha(AS_OF)
try:
    res = b4.evaluador.pronosticos_de_fuentes(AS_OF)
    ids = [p["clm_id"] for p in res]
    comprobar("CLM-2025-9000" in ids, f"sin excepción; resueltos {len(ids)}; el sano cuenta ({'CLM-2025-9000' in ids})")
except Exception as e:  # noqa: BLE001
    comprobar(False, f"EXCEPCIÓN {type(e).__name__}: {str(e)[:80]}")
try:
    fue = b4.evaluador.fiabilidad_fuentes(AS_OF, "RUN-QA")
    comprobar(True, f"fiabilidad_fuentes sin excepción ({len(fue)} FUE-)")
except Exception as e:  # noqa: BLE001
    comprobar(False, f"fiabilidad_fuentes: EXCEPCIÓN {type(e).__name__}: {str(e)[:80]}")

print("E5 · variables_nivel mal formada en la configuración: falla al crear el Bloque")
for valor in ["cierre", 5, [], [""], ["  "], ["cierre", 5], [["cierre"]], {"cierre": 1}, True]:
    cfg = config_pruebas(modo="vivo", fiabilidad_fuentes={"variables_nivel": valor})
    try:
        nuevo_bloque(Path(tempfile.mkdtemp(prefix="qa14_t134_e5_", dir=TMP)), UNIVERSO, cfg=cfg)
        res = "creado"
    except ValueError as e:
        res = "ValueError" if "variables_nivel" in str(e) else f"ValueError ajeno: {e}"
    except Exception as e:  # noqa: BLE001
        res = f"{type(e).__name__}"
    comprobar(res == "ValueError", f"variables_nivel = {valor!r:16} → {res}")
cfg = config_pruebas(modo="vivo", fiabilidad_fuentes={"variables_nivel": [" Cierre "]})
mock_respuestas._ficha = lambda u, msg, ctx, rng, iny: {**FICHA0(u, msg, ctx, rng, iny)} | {
    "afirmaciones": FICHA0(u, msg, ctx, rng, iny)["afirmaciones"] + raras(FICHA0(u, msg, ctx, rng, iny)["indicador_seguimiento"]["simbolo"],
                                                                         pd.Timestamp(ctx["fecha_as_of"]))[:1]}
try:
    b5 = nuevo_bloque(Path(tempfile.mkdtemp(prefix="qa14_t134_e5b_", dir=TMP)), UNIVERSO, cfg=cfg)
    b5.ciclo(C1, alcance={"clases": ["RV"]})
    f2 = [c for c in b5.almacen.estado("F2", clave="clm_id").values() if isinstance(c.get("pronostico_fuente"), dict)]
    comprobar(bool(f2), f"variables_nivel [' Cierre '] (espacios y mayúscula) admite «cierre»: {len(f2)} en F2")
finally:
    mock_respuestas._ficha = FICHA0

print(f"\nr01_01 T-134: {OK} ok, {len(FALLOS)} fallos")
for f in FALLOS:
    print("  -", f)
