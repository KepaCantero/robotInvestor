"""QA r01 de T-100 (V0.76): CA-6 con estados y diarios GENUINOS de la V0.75, escritos por el código de la V0.75 (commit d7f2095) y
abiertos con el de la V0.76. Datos SIMULADOS.

Uso (desde la raíz del repositorio):
    .venv/bin/python -I .docs/tickets/T-100/revisores/r01_04_estado_y_diario_v075.py <marco V0.75> <marco V0.76>
El marco de la V0.75 se saca con `git worktree add --detach <dir> d7f2095` (o `git archive`); el script no toca ninguno de los dos.
Cada parte se ejecuta en un proceso aparte, con el código de su versión. Imprime BIEN, FALLA u OBSERVA. Termina con 0.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

V075, V076 = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()

ESCRIBE = r'''
import json, sys
from pathlib import Path
M = Path(sys.argv[1]); d = Path(sys.argv[2])
sys.path.insert(0, str(M / "validador")); sys.path.insert(0, str(M / "pruebas"))
import persistencia as pe, diario as di
from pruebas_orquestador import AHORA, nuevo
o = nuevo()
assert o.iniciar_sombra(100000.0, 100.0, "OPERADOR", AHORA)["ok"]
assert o.movimiento_sombra("APORTE", 50000.0, 100.0, "G", "2026-12-10T10:00:00+00:00")["ok"]
(d / "estado_v075.json").write_text(pe.volcar(o, "2026-12-10T10:00:00+00:00"), encoding="utf-8")
# diario con un movimiento DESPUÉS del punto de control (sin cerrar), y otro cerrado con punto()
for nombre, cerrar in (("abierto", False), ("cerrado", True)):
    o2 = nuevo()
    D = di.crear(o2, str(d / f"e_{nombre}.json"), str(d / f"d_{nombre}.log"), AHORA)["diario"]
    assert D.iniciar_sombra(100000.0, 100.0, "OPERADOR", AHORA)["ok"]
    assert D.movimiento_sombra("APORTE", 50000.0, 100.0, "G", "2026-12-10T10:00:00+00:00")["ok"]
    if cerrar:
        assert D.punto("2026-12-10T10:00:00+00:00")["ok"]
print(json.dumps({"esquema": pe.esquema_actual()}))
'''

LEE = r'''
import json, sys
from pathlib import Path
M = Path(sys.argv[1]); d = Path(sys.argv[2])
sys.path.insert(0, str(M / "validador")); sys.path.insert(0, str(M / "pruebas"))
import persistencia as pe, diario as di
out = {"esquema": pe.esquema_actual()}
c = pe.cargar((d / "estado_v075.json").read_text(encoding="utf-8"))
o = c.get("orquestador")
out["cargar"] = c.get("codigo")
if o is not None:
    out["integridad"] = o.integridad()
    out["movs_sin_ref"] = [x for x in o.sombra["entradas"] if x["tipo"] == "APORTE" and "ref" not in x] != []
    out["nuevo_con_ref"] = o.movimiento_sombra("APORTE", 50000.0, 100.0, "OPERADOR", "2026-12-11T10:00:00+00:00", ref="INT-1")["codigo"]
    out["nuevo_sin_ref"] = o.movimiento_sombra("APORTE", 1.0, 100.0, "OPERADOR", "2026-12-11T10:00:00+00:00")["codigo"]
    out["aportes"] = len([x for x in o.sombra["entradas"] if x["tipo"] == "APORTE"])
    out["kill"] = o.kill is not None
for nombre in ("abierto", "cerrado"):
    r = di.abrir(str(d / f"e_{nombre}.json"), str(d / f"d_{nombre}.log"))
    oo = r.get("diario").orquestador if r.get("diario") is not None else r.get("orquestador")
    out[f"diario_{nombre}"] = {"codigo": r.get("codigo"), "motivo": str(r.get("motivo"))[:160],
                               "kill": oo is not None and oo.kill is not None}
print(json.dumps(out))
'''


def correr(codigo, marco, d):
    r = subprocess.run([sys.executable, "-I", "-c", codigo, str(marco), str(d)], capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        raise SystemExit(f"falla el proceso con {marco}: {r.stderr[-800:]}")
    return json.loads(r.stdout.strip().splitlines()[-1])


def sonda(nombre, estado, detalle=""):
    print(f"{estado:7s} {nombre}  {str(detalle)[:500]}")


with tempfile.TemporaryDirectory() as d:
    w = correr(ESCRIBE, V075, d)
    r = correr(LEE, V076, d)
sonda("C01_el_esquema_de_la_V076_es_el_de_la_V075", "BIEN" if w["esquema"] == r["esquema"] else "FALLA", (w["esquema"][:12], r["esquema"][:12]))
sonda("C02_un_estado_V075_se_carga_sin_migrar_y_conserva_el_movimiento_sin_referencia",
      "BIEN" if r["cargar"] == "OK" and r["integridad"] == [] and r["movs_sin_ref"] else "FALLA", r)
sonda("C03_tras_cargar_se_anota_con_referencia_y_sin_ella_es_O01", "BIEN" if r["nuevo_con_ref"] == "OK" and r["nuevo_sin_ref"] == "O-01"
      and r["aportes"] == 2 and not r["kill"] else "FALLA", r)
sonda("C04_un_diario_V075_cerrado_con_punto_se_abre", "BIEN" if r["diario_cerrado"]["codigo"] == "OK" and not r["diario_cerrado"]["kill"]
      else "FALLA", r["diario_cerrado"])
dab = r["diario_abierto"]
sonda("C05_un_diario_V075_con_un_movimiento_tras_el_punto_no_se_abre_con_la_V076",
      "FALLA" if dab["codigo"] != "OK" else "BIEN", f"{dab}: al reaplicar, movimiento_sombra sin ref da O-01 y no el OK anotado; sin "
      "migración no hay MG-06 que pida cerrar el diario antes de cambiar de código")
