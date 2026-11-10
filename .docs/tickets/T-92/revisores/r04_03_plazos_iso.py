"""QA r04 de T-92 (revisor nuevo): plazo de CT-23 solo ISO 8601, fin de día con cambios de hora y medianoche inexistente (H-30).

Uso: python -I r04_03_plazos_iso.py <ruta a bloque_a/11_Ejecutor>
Imprime OK/FALLO por caso (INFO no cuenta).
"""
import datetime as dt, sys, tempfile
from pathlib import Path
EJ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(EJ)); sys.path.insert(0, str(EJ / "tests"))
import bloque_a
assert Path(bloque_a.__file__).resolve().is_relative_to(EJ), bloque_a.__file__
import pandas as pd
from conftest import config_pruebas, nuevo_bloque
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
from bloque_a.herramientas.ht01_datos import cargar_universo

fallos = 0
def informe(nombre, ok, detalle=""):
    global fallos
    fallos += 0 if ok else 1
    print(("OK    " if ok else "FALLO ") + nombre + (f" — {detalle}" if detalle else ""))
def info(nombre, detalle=""):
    print("INFO  " + nombre + (f" — {detalle}" if detalle else ""))

universo = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
CONSULTA = {"tipo": "OTRA", "modo": "BLOQUEANTE", "clases": ["RV"], "preguntas": [{"texto": "¿RV?", "supuesto_declarado": "esperar"}]}

def guardado(plazo, envio="2026-03-02", cfg=None):
    with tempfile.TemporaryDirectory() as d:
        b = nuevo_bloque(d, universo, cfg=cfg)
        try:
            return b.consultas.enviar({**CONSULTA, "plazo_respuesta": plazo}, envio)["plazo_respuesta"]
        except Exception as x:
            return "ValueError" if isinstance(x, ValueError) else f"{type(x).__name__}"

def borde(plazo, dentro, fuera, envio="2026-03-02", cfg=None):
    with tempfile.TemporaryDirectory() as d:
        b = nuevo_bloque(d, universo, cfg=cfg)
        c = b.consultas.enviar({**CONSULTA, "plazo_respuesta": plazo}, envio)
        return b.consultas.vencer(dentro), b.consultas.vencer(fuera), c["cns_id"], c["plazo_respuesta"]

print("--- 1. Solo ISO 8601")
for forma in ["2026", "2026-06", "8 June 2026", "June 8, 2026", "2026-6-8", "2026/06/08", "08/06/2026", "2026-06-08T09",
              "mañana", "", "2026-13-01", "2026-02-30", "2026-06-08T25:00", "2026-W24-1", "2026-159"]:
    r = guardado(forma)
    esperado_vacio = forma == ""   # vacío = sin plazo: el del modo
    ok = (r == "ValueError") if not esperado_vacio else not r.endswith("Error")
    informe(f"1a «{forma}» se rechaza" if not esperado_vacio else "1a «» usa el plazo del modo", ok, r)
for forma, prefijo in [("2026-06-08", "2026-06-08T23:59:59.999999+02:00"), ("20260608", "2026-06-08T23:59:59.999999+02:00"),
                       (" 2026-06-08 ", "2026-06-08T23:59:59.999999+02:00"), ("2026-06-08T09:00", "2026-06-08T09:00:00+02:00"),
                       ("2026-06-08 09:00:00", "2026-06-08T09:00:00+02:00"), ("2026-06-08T07:00Z", "2026-06-08T09:00:00+02:00"),
                       ("2026-06-08T09:00:00+0200", "2026-06-08T09:00:00+02:00"),
                       ("2026-06-08T09:00:00.123456789+02:00", "2026-06-08T09:00:00.123456")]:
    r = guardado(forma)
    informe(f"1b «{forma}» se acepta → {r}", r.startswith(prefijo))

print("--- 2. Fin del día en Madrid (cambios de hora) y en una zona con medianoche inexistente")
for plazo, dentro, fuera in [("2026-03-29", "2026-03-29T21:59:59.999Z", "2026-03-29T22:00Z"),
                             ("2026-10-25", "2026-10-25T22:59:59.999Z", "2026-10-25T23:00Z"),
                             ("20260329", "2026-03-29T21:59:59.999Z", "2026-03-29T22:00Z")]:
    d_, f_, k, g = borde(plazo, dentro, fuera)
    informe(f"2a «{plazo}»: abierta hasta {dentro}, vencida a {fuera}", d_ == [] and f_ == [k], f"{d_}/{f_} ({g})")
cfg = config_pruebas(); cfg["zona_horaria"] = "America/Santiago"
# En Chile la hora de verano 2026 empieza el domingo 6-9: las 00:00 pasan a 01:00 (las 00:00 del 6-9 no existen)
d_, f_, k, g = borde("2026-09-05", "2026-09-06T03:59:59.999Z", "2026-09-06T04:00Z", envio="2026-09-01", cfg=cfg)
informe("2b Santiago, plazo «2026-09-05»: no lanza; abierta hasta las 23:59:59,999 del 5-9 (-04) y vencida a las 00:00 (-04)",
        d_ == [] and f_ == [k], f"{d_}/{f_}; guardado {g}")
r = guardado("2026-09-06T00:30", envio="2026-09-01", cfg=cfg)
informe("2c Santiago, hora inexistente «2026-09-06T00:30»: pasa a la primera hora válida (01:00 -03)", r.startswith("2026-09-06T01:00"), r)
r = guardado("2026-09-06", envio="2026-09-01", cfg=cfg)
informe("2d Santiago, plazo «2026-09-06» (día de 23 h): vence a las 23:59:59,999999 -03 del 6-9", r.startswith("2026-09-06T23:59:59.999999-03:00"), r)
# fin del horario de verano: las 23:00-24:00 del 4-4 se repiten
r = guardado("2026-04-04T23:30", envio="2026-04-01", cfg=cfg)
info("2e Santiago, hora ambigua «2026-04-04T23:30» (se repite)", f"guardado {r} (ambiguous=True: la primera, con horario de verano)")
r = guardado("2026-04-04", envio="2026-04-01", cfg=cfg)
informe("2f Santiago, plazo «2026-04-04» (día de 25 h): vence a las 23:59:59,999999 -04 (la segunda vuelta)",
        r.startswith("2026-04-04T23:59:59.999999-04:00"), r)

print("--- 3. Tipos que no son texto (no pasan por la regla ISO)")
for forma in [20260608, 2026.5, True, dt.date(2026, 6, 8), dt.datetime(2026, 6, 8), pd.Timestamp("2026-06-08")]:
    info(f"3  plazo {forma!r} ({type(forma).__name__})", guardado(forma))
with tempfile.TemporaryDirectory() as d:
    b = nuevo_bloque(d, universo)
    try:
        c = b.consultas.enviar({**CONSULTA, "plazo_respuesta": 20260608}, "2026-06-05")
        venc = b.consultas.vencer("2026-06-05T09:00")
        informe("3b un plazo numérico 20260608 no deja vencida al instante una consulta BLOQUEANTE", c["cns_id"] not in venc,
                f"guardado {c['plazo_respuesta']}; vencidas al enviar: {venc}")
    except (ValueError, TypeError) as x:
        informe("3b un plazo numérico 20260608 no deja vencida al instante una consulta BLOQUEANTE", True, f"rechazado: {type(x).__name__}")

print("--- 4. Consultas ya guardadas por develop con un plazo que no es ISO (develop guardaba el texto tal cual)")
for antiguo in ["2026-6-8", "8/6/2026", "2026-06-08 09:00:00.000000+0200 CEST"]:
    with tempfile.TemporaryDirectory() as d:
        b = nuevo_bloque(d, universo)
        b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "CNS", "id": "CNS-2026-0099", "cns_id": "CNS-2026-0099",
                                           "sentido": "SALIENTE", "tipo": "OTRA", "modo": "BLOQUEANTE", "clases": ["RV"],
                                           "preguntas": [{"texto": "¿RV?", "supuesto_declarado": "esperar"}],
                                           "plazo_respuesta": antiguo, "estado": "ENVIADA"})
        try:
            v = b.consultas.vencer("2027-01-10T09:00")   # el registro lleva la fecha del reloj (hoy)
            res = f"vencidas {v}"
        except Exception as x:
            res = f"{type(x).__name__}: {str(x)[:70]}"
        informe(f"4  F5 con plazo antiguo «{antiguo}»: vencer() (que el ciclo llama en F0) no se rompe", not res.startswith(("ValueError", "TypeError")), res)
print("fallos:", fallos)
