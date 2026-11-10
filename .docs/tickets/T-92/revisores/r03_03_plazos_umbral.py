"""QA r03 de T-92 (revisor nuevo): CT-23 con plazo de solo fecha y cambios de hora (H-22) y `senales.umbral_favorable` (H-23).

Uso: python -I r03_03_plazos_umbral.py <ruta a bloque_a/11_Ejecutor>
Imprime OK/FALLO por caso (INFO no cuenta).
"""
import datetime as dt, decimal, sys, tempfile
from pathlib import Path
EJ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(EJ)); sys.path.insert(0, str(EJ / "tests"))
import bloque_a
assert Path(bloque_a.__file__).resolve().is_relative_to(EJ), bloque_a.__file__
import numpy as np
import pandas as pd
from conftest import config_pruebas, nuevo_bloque
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
from bloque_a.herramientas.ht01_datos import cargar_universo

fallos = 0
def informe(nombre, ok, detalle=""):
    global fallos
    fallos += 0 if ok else 1
    print(("OK    " if ok else "FALLO ") + nombre + (f" — {detalle}" if detalle else ""))

universo = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
CONSULTA = {"tipo": "OTRA", "modo": "BLOQUEANTE", "clases": ["RV"], "preguntas": [{"texto": "¿RV?", "supuesto_declarado": "esperar"}]}

def plazo_guardado(plazo, envio="2026-03-02", cfg=None):
    with tempfile.TemporaryDirectory() as d:
        b = nuevo_bloque(d, universo, cfg=cfg)
        try:
            return b.consultas.enviar({**CONSULTA, "plazo_respuesta": plazo}, envio)["plazo_respuesta"]
        except Exception as x:
            return f"{type(x).__name__}: {x}"

def borde(plazo, dentro, fuera, envio="2026-03-02"):
    with tempfile.TemporaryDirectory() as d:
        b = nuevo_bloque(d, universo)
        c = b.consultas.enviar({**CONSULTA, "plazo_respuesta": plazo}, envio)
        return b.consultas.vencer(dentro), b.consultas.vencer(fuera), c["cns_id"]

# 1. Bordes del día en Madrid, con la consulta enviada antes del plazo (días normales y de cambio de hora)
for plazo, dentro, fuera in [("2026-06-08", "2026-06-08T21:59:59.999Z", "2026-06-08T22:00Z"),
                             ("2026-03-29", "2026-03-29T21:59:59.999Z", "2026-03-29T22:00Z"),   # 23 h
                             ("2026-10-25", "2026-10-25T22:59:59.999Z", "2026-10-25T23:00Z"),   # 25 h
                             ("2026-03-28", "2026-03-28T22:59:59.999Z", "2026-03-28T23:00Z"),   # víspera del cambio
                             ("2026-12-31", "2026-12-31T22:59:59.999Z", "2026-12-31T23:00Z")]:  # cambio de año
    d_, f_, k = borde(plazo, dentro, fuera)
    informe(f"1  plazo «{plazo}»: abierto hasta {dentro} y vencido a {fuera}", d_ == [] and f_ == [k], f"{d_} / {f_}")

# 1b. La explicación del ticket para r02_04 caso 3: enviada el 5-6, el 29-3 la consulta aún no existe
with tempfile.TemporaryDirectory() as d:
    b = nuevo_bloque(d, universo)
    c = b.consultas.enviar({**CONSULTA, "plazo_respuesta": "2026-03-29"}, "2026-06-05")
    antes = b.consultas.vencer("2026-03-29T22:00Z")
    despues = b.consultas.vencer("2026-06-05T12:00Z")
    informe("1b explicación de r02_04 caso 3: con envío el 5-6, vencer el 29-3 no la ve y el 5-6 sí la vence",
            antes == [] and despues == [c["cns_id"]], f"29-3: {antes}; 5-6: {despues}")

# 2. Formas de escribir la fecha
print("--- 2. Formas del plazo (INFO: lo guardado)")
for forma in ["2026-06-08", "2026-6-8", "20260608", "2026/06/08", " 2026-06-08 ", "2026-06-08T00:00", "2026-06-08 00:00",
              "2026-06-08T00:00Z", "8 June 2026", "June 8, 2026", "2026-06", "2026", dt.date(2026, 6, 8), pd.Timestamp("2026-06-08")]:
    print(f"INFO  2  {forma!r:30} → {plazo_guardado(forma)}")
informe("2a «2026-06-08», «2026-6-8», «20260608» y «2026/06/08» valen todo el día",
        len({plazo_guardado(f) for f in ["2026-06-08", "2026-6-8", "20260608", "2026/06/08"]}) == 1
        and plazo_guardado("2026-06-08").startswith("2026-06-08T23:59:59.999999"))
informe("2b una hora explícita «2026-06-08T00:00» no se alarga", plazo_guardado("2026-06-08T00:00").startswith("2026-06-08T00:00"))

# 3. Zona del reloj con el cambio de hora a medianoche (configurable: `zona_horaria`)
cfg = config_pruebas(); cfg["zona_horaria"] = "America/Santiago"
r = plazo_guardado("2026-09-05", envio="2026-09-01", cfg=cfg)
print(f"INFO  3  zona America/Santiago, plazo «2026-09-05» (las 00:00 del 6-9 no existen): {r}")

# 4. umbral_favorable: lo válido se acepta, lo inválido falla cerrado, el borde es «favorable»
with tempfile.TemporaryDirectory() as d:
    b = nuevo_bloque(d, universo)
    s = {"senal_compuesta": 0.5, "tendencia_26s": "alcista"}
    for bueno, esperado in [(0.5, "favorable"), (0, "favorable"), (1, "contraria"), (0.0, "favorable"), (1.0, "contraria"),
                            (np.float64(0.5), "favorable"), (0.5000001, "contraria")]:
        b.cfg["senales"]["umbral_favorable"] = bueno
        try:
            r = b._observacion_ht01("X", s)["direccion"]
        except Exception as x:
            r = type(x).__name__
        informe(f"4  umbral {bueno!r} con señal 0,5 → {esperado}", r == esperado, r)
    for malo in (float("nan"), float("inf"), -float("inf"), True, False, -0.01, 1.01, "0.5", None, [0.5],
                 decimal.Decimal("0.5"), np.int64(1)):
        b.cfg["senales"]["umbral_favorable"] = malo
        try:
            r = b._observacion_ht01("X", s)["direccion"]; ok, det = False, f"acepta y da {r}"
        except (ValueError, TypeError, KeyError) as x:
            ok, det = True, type(x).__name__
        informe(f"4b umbral {malo!r} falla cerrado", ok, det)
print("fallos:", fallos)
