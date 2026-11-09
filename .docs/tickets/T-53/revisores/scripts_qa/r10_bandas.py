"""r10 · CS-05: cinco bandas. Bordes, huecos, valores extremos y no válidos; coherencia con el esquema y con lo ya escrito
en F4 por la tabla antigua; estado global compartido entre dos Evaluadores con configuraciones distintas."""
import json, math, pathlib
from bloque_a import evaluador as ev
from bloque_a.evaluador import banda_de, banda_publicable, Evaluador, fijar_bandas, PROB_DE_BANDA
from bloque_a.almacen import Almacen
import tempfile
def vieja(p):
    if p >= 0.80: return "MUY_PROBABLE"
    if p >= 0.60: return "MAS_PROBABLE_QUE_NO"
    if p > 0.40: return "INCIERTO"
    if p >= 0.25: return "POCO_PROBABLE"
    return "MUY_POCO_PROBABLE"
ps = [0.0, 0.03, 0.05, 0.20, 0.21, 0.22, 0.24, 0.25, 0.40, 0.42, 0.44, 0.45, 0.50, 0.55, 0.57, 0.5999, 0.60, 0.75, 0.77, 0.7999, 0.80, 0.95, 0.97, 1.0]
cambios = [(p, vieja(p), banda_de(p)) for p in ps if vieja(p) != banda_de(p)]
print("tabla:", [(p, banda_de(p)) for p in ps])
print("distintos de la tabla antigua de F4:", cambios)
esq = json.loads(pathlib.Path("/home/claude/repo/bloque_a/06_Plantillas_entregables/Esquema JSON - Paquete de oportunidades - V5.0.json").read_text())
enum = esq["$defs"]["vista_horizonte"]["properties"]["banda"]["enum"]
print("publicables ⊆ enum del esquema:", {banda_publicable(p) for p in ps} <= set(enum), "| cubre las 5:", {banda_publicable(p) for p in ps} == set(enum))
for x in (float("nan"), -0.01, 1.01, None, "0.6"):
    try:
        print(f"banda_de({x!r}) =", banda_de(x))
    except Exception as e:
        print(f"banda_de({x!r}) -> {type(e).__name__}: {e}")
print("PROB_DE_BANDA:", PROB_DE_BANDA)
# estado global: un Evaluador con otra tabla cambia la de todo el proceso
otra = [dict(b) for b in ev.BANDAS_VERBALES_POR_DEFECTO]
otra[1] = dict(otra[1], min=0.56, max=0.79, prob_interna=0.70)
otra[0] = dict(otra[0], min=0.80)
a = Almacen(tempfile.mkdtemp(dir="."))
antes = banda_de(0.58)
Evaluador(a, None, None, {"evaluacion": {}, "bandas_verbales": otra}, None)
print("banda_de(0.58) antes/después de crear un 2.º Evaluador con otra tabla:", antes, "->", banda_de(0.58), "| PROB_DE_BANDA[MAS_PROBABLE_QUE_NO]:", PROB_DE_BANDA["MAS_PROBABLE_QUE_NO"])
fijar_bandas()
