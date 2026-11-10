"""QA de Claude, V0.64 (panel con el estado del sistema): sondas propias. Uso: MARCO=<marcoC> python3 -I entrega_claude/V0.67/scripts/r01_panel_v064.py (desde marcoC)"""
import math, os, sys, tempfile
M = os.environ["MARCO"]
sys.path.insert(0, os.path.join(M, "validador")); sys.path.insert(0, os.path.join(M, "pruebas"))
from pruebas_consola_sistema import nuevo_reloj, nuevo_diario, iso, MOTIVO_REARME  # noqa: E402
from pruebas_orquestador import AHORA, nuevo  # noqa: E402
from consola import panel  # noqa: E402
import diario as di  # noqa: E402

def linea(p, que):
    return next((x for x in p["comprobaciones"] if x["que"] == que), None)

res = []
def chk(nombre, cond, detalle=""):
    res.append(cond); print(("OK      " if cond else "HALLAZGO"), nombre, "" if cond else detalle)

o = nuevo()
# 1. contraste justo en el límite: VERDE, como ahora() (que usa >)
f, r = nuevo_reloj()
f.pasa(r.max_sin_contraste_s)
chk("reloj en el límite exacto: VERDE", linea(panel(o, AHORA, reloj=r), "reloj")["nivel"] == "VERDE", linea(panel(o, AHORA, reloj=r), "reloj"))
f.pasa(0.001)
chk("reloj pasado el límite: AMBAR", linea(panel(o, AHORA, reloj=r), "reloj")["nivel"] == "AMBAR")
# 2. monótono NaN: no se confirma el contraste
f, r = nuevo_reloj(); f.nan_mono = True
chk("monótono NaN: no VERDE", linea(panel(o, AHORA, reloj=r), "reloj")["nivel"] != "VERDE")
# 3. reloj bloqueado: ROJO, y sigue ROJO aunque las carteras se degraden
f, r = nuevo_reloj(); f.pasa(10, pared=-3600)
r.ahora()
p = panel(o, AHORA, reloj=r)
chk("reloj bloqueado tras un salto hacia atrás: ROJO", linea(p, "reloj")["nivel"] == "ROJO", linea(p, "reloj"))
# 4. tope de líneas del diario raro: nunca VERDE con un tope que no es un entero positivo
with tempfile.TemporaryDirectory() as t:
    d = nuevo_diario(t)
    for tope in (float("nan"), None, "1000", -1, 0, True, float("inf")):
        l = linea(panel(o, AHORA, diario=d, lineas_diario_ambar=tope), "diario")
        chk(f"tope del diario {tope!r}: no VERDE (falla cerrado)", l["nivel"] != "VERDE", l)
# 5. objeto de reloj o de diario equivocado: ROJO, sin excepción
for malo in ({}, object(), "reloj"):
    p = panel(o, AHORA, reloj=malo)
    chk(f"reloj {type(malo).__name__}: ROJO", linea(p, "reloj")["nivel"] == "ROJO")
    p = panel(o, AHORA, diario=malo)
    chk(f"diario {type(malo).__name__}: ROJO", linea(p, "diario")["nivel"] == "ROJO")
# 6. kill-switch con un registro incompleto: ROJO
o2 = nuevo(); o2.kill = {}
chk("kill-switch {} (registro vacío): ROJO", linea(panel(o2, AHORA), "kill_switch")["nivel"] == "ROJO", linea(panel(o2, AHORA), "kill_switch"))
o3 = nuevo(); o3.kill = False
chk("kill-switch False (no es None ni dict): ROJO", linea(panel(o3, AHORA), "kill_switch")["nivel"] == "ROJO", linea(panel(o3, AHORA), "kill_switch"))
# 7. el panel no muta el estado
import copy, json
o4 = nuevo(); antes = json.dumps(o4.__dict__, default=str, sort_keys=True)
panel(o4, AHORA); chk("el panel no muta el Orquestador", json.dumps(o4.__dict__, default=str, sort_keys=True) == antes)
print("RESULTADO:", "SIN HALLAZGOS" if all(res) else f"{res.count(False)} HALLAZGO(S)")
