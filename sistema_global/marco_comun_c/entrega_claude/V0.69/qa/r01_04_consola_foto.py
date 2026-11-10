"""QA r01 de T-72 (V0.69): la comprobación «diario» de la consola con la foto pública.

1. No lee privados del diario: un envoltorio registra cada atributo que la consola pide al objeto `diario`.
2. Fotos raras (tipos, bools, subclases de dict, `get` que lanza, `estado_diario` no invocable o que devuelve otra cosa): nunca
   VERDE salvo la foto buena, y nunca sale una excepción del panel.
3. Foto contradictoria `operativo: False` con el resto «bueno»: ¿VERDE? (la consola no mira `operativo`).
4. Panel completo de HEAD frente al del árbol en escenarios donde no debe cambiar nada (sin reloj ni diario, con reloj, con un
   diario limpio, con muchas líneas, bloqueado): mismos niveles (el texto del bloqueo puede cambiar). Se ejecuta en un proceso
   aparte con cada marco.

Uso (desde sistema_global/marco_comun_c): python3 -I entrega_claude/V0.69/qa/r01_04_consola_foto.py <marco_de_HEAD>
"""
import json
import os
import subprocess
import sys

M = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ESCENARIOS = r'''
import json, os, sys, tempfile
M = sys.argv[1]
sys.path.insert(0, os.path.join(M, "validador")); sys.path.insert(0, os.path.join(M, "pruebas"))
from consola import panel
from pruebas_consola_sistema import nuevo_diario
from pruebas_orquestador import AHORA, nuevo
from pruebas_reloj_t03 import nuevo_reloj
out = {}
def foto(p):
    return {"nivel": p["nivel"], "comprobaciones": [(c["que"], c["nivel"]) for c in p["comprobaciones"]]}
with tempfile.TemporaryDirectory() as t:
    o = nuevo()
    out["sin_nada"] = foto(panel(o, AHORA))
    f, r = nuevo_reloj(); out["reloj"] = foto(panel(o, AHORA, reloj=r))
    f.pasa(90000.0); out["reloj_caducado"] = foto(panel(o, AHORA, reloj=r))
    f, r = nuevo_reloj(contrastar=False); out["reloj_sin_contraste"] = foto(panel(o, AHORA, reloj=r))
    d = nuevo_diario(os.path.join(t, "a")); out["diario_limpio"] = foto(panel(d.orquestador, AHORA, diario=d))
    d.barrer(AHORA); out["diario_3"] = foto(panel(d.orquestador, AHORA, diario=d, lineas_diario_ambar=2))
    out["diario_3_tope3"] = foto(panel(d.orquestador, AHORA, diario=d, lineas_diario_ambar=3))
    out["diario_tope_nan"] = foto(panel(d.orquestador, AHORA, diario=d, lineas_diario_ambar=float("nan")))
    d.orquestador.cotizaciones["X"] = {"ultima": 1.0}; d.barrer(AHORA)
    out["diario_bloqueado"] = foto(panel(d.orquestador, AHORA, diario=d))
    out["diario_texto"] = foto(panel(o, AHORA, diario="x"))
    out["diario_orquestador"] = foto(panel(o, AHORA, diario=o))
    f, r = nuevo_reloj(); d = nuevo_diario(os.path.join(t, "b"))
    out["todo"] = foto(panel(d.orquestador, AHORA, reloj=r, diario=d))
print(json.dumps(out, sort_keys=True))
'''

sys.path.insert(0, os.path.join(M, "validador"))
sys.path.insert(0, os.path.join(M, "pruebas"))
from consola import panel  # noqa: E402
from pruebas_consola_sistema import comp  # noqa: E402
from pruebas_orquestador import AHORA, nuevo  # noqa: E402

res = []


def chk(nombre, cond, detalle=""):
    res.append(bool(cond))
    print(("OK      " if cond else "HALLAZGO"), nombre, "" if cond else detalle)


BUENA = {"operativo": True, "bloqueo": None, "lineas": 2, "sincronizado": True, "motivo_desincronizado": None}


class Espia:
    def __init__(self, foto):
        object.__setattr__(self, "pedidos", [])
        object.__setattr__(self, "foto", foto)

    def __getattribute__(self, nombre):
        if nombre not in ("pedidos", "foto", "__class__", "__dict__"):
            object.__getattribute__(self, "pedidos").append(nombre)
        if nombre == "estado_diario":
            return lambda: object.__getattribute__(self, "foto")
        if nombre.startswith("_") and not nombre.startswith("__"):
            return "PRIVADO LEÍDO"
        return object.__getattribute__(self, nombre)


esp = Espia(dict(BUENA))
k = comp(nuevo(), "diario", diario=esp)
chk("con la foto buena, VERDE", k["nivel"] == "VERDE", k)
chk("la consola solo pide estado_diario (ningún privado)", [p for p in esp.pedidos if not p.startswith("__")] == ["estado_diario"], esp.pedidos)


class DictRaro(dict):
    def get(self, *a):
        raise RuntimeError("get roto")


class Igual(dict):
    """Un dict cuyo `sincronizado` es un objeto que dice ser igual a todo."""


class Todo:
    def __eq__(self, o):
        return True

    def __bool__(self):
        return True


raras = {
    "None": None, "lista": [BUENA], "texto": "VERDE", "dict vacío": {},
    "get que lanza": DictRaro(BUENA),
    "bloqueo False": {**BUENA, "bloqueo": False}, "bloqueo {}": {**BUENA, "bloqueo": {}}, "bloqueo 0": {**BUENA, "bloqueo": 0},
    "bloqueo texto": {**BUENA, "bloqueo": "DI-06"},
    "sincronizado 1": {**BUENA, "sincronizado": 1}, "sincronizado 'True'": {**BUENA, "sincronizado": "True"},
    "sincronizado objeto ==todo": {**BUENA, "sincronizado": Todo()}, "sin sincronizado": {k: v for k, v in BUENA.items() if k != "sincronizado"},
    "lineas True": {**BUENA, "lineas": True}, "lineas 2.0": {**BUENA, "lineas": 2.0}, "lineas 0": {**BUENA, "lineas": 0},
    "lineas -1": {**BUENA, "lineas": -1}, "lineas '2'": {**BUENA, "lineas": "2"}, "lineas NaN": {**BUENA, "lineas": float("nan")},
    "sin lineas": {k: v for k, v in BUENA.items() if k != "lineas"},
}
for etq, foto in raras.items():
    try:
        p = panel(nuevo(), AHORA, diario=Espia(foto))
        c = next(x for x in p["comprobaciones"] if x["que"] == "diario")
        chk(f"foto rara «{etq}»: no VERDE", c["nivel"] != "VERDE", c)
    except Exception as ex:   # noqa: BLE001
        chk(f"foto rara «{etq}»: el panel no lanza", False, repr(ex))


class NoInvocable:
    estado_diario = dict(BUENA)


class PropiedadQueLanza:
    @property
    def estado_diario(self):
        raise RuntimeError("x")


for etq, obj in (("estado_diario no invocable", NoInvocable()), ("estado_diario propiedad que lanza", PropiedadQueLanza())):
    k = comp(nuevo(), "diario", diario=obj)
    chk(f"{etq}: ROJO", k["nivel"] == "ROJO", k)

# 3. foto contradictoria
k = comp(nuevo(), "diario", diario=Espia({**BUENA, "operativo": False}))
print(("INFO    " if k["nivel"] == "VERDE" else "OK      "),
      f"foto con operativo=False y el resto bueno: {k['nivel']} (la consola no mira `operativo`; el Diario real no la da)")

# 4. HEAD frente al árbol
head = os.path.abspath(sys.argv[1])
py = sys.executable
salidas = {}
for nombre, marco in (("HEAD", head), ("árbol", M)):
    s = subprocess.run([py, "-I", "-c", ESCENARIOS, marco], capture_output=True, text=True, cwd=marco)
    assert s.returncode == 0, s.stderr[-2000:]
    salidas[nombre] = json.loads(s.stdout.strip().splitlines()[-1])
for esc in sorted(salidas["HEAD"]):
    chk(f"panel igual que en HEAD: {esc}", salidas["HEAD"][esc] == salidas["árbol"][esc], (salidas["HEAD"][esc], salidas["árbol"][esc]))

print(f"\n{len(res)} comprobaciones, {res.count(False)} hallazgos")
print("RESULTADO r01_04:", "SIN HALLAZGOS" if all(res) else "HAY HALLAZGOS")
sys.exit(0 if all(res) else 1)
