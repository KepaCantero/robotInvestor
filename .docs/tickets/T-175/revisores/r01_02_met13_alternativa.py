"""QA r01 de T-175 (revisor): ¿puede el texto del modelo de una alternativa descartada tirar la entrega entera?

Uso (desde bloque_a/11_Ejecutor de la copia que se quiera medir; sirve también en develop 80751da, anterior a T-175):
    ../../.venv/bin/python <ruta>/r01_02_met13_alternativa.py [alternativa|opcion] ["texto añadido"] [obedece]

Simula un Contradictor (AG-11) que escribe «validada» en el argumento de su objeción fuerte y un modelo que NO obedece la
reescritura R22 (lo mismo que una reescritura que no cabe en la bolsa, que no se pide). «alternativa»: solo en la candidata que,
en el ciclo de referencia, queda fuera del top-3 con la objeción fuerte sin resolver; «opcion»: solo en la primera del top-3.
"""
import copy
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "tests")
from conftest import AS_OF, RUTA_UNIVERSO_EJEMPLO, cargar_universo, nuevo_bloque  # noqa: E402

from bloque_a import mock_respuestas  # noqa: E402

modo = sys.argv[1] if len(sys.argv) > 1 else "alternativa"
TEXTO = " " + (sys.argv[2] if len(sys.argv) > 2 else "La señal no está validada fuera de muestra.")
OBEDECE = len(sys.argv) > 3 and sys.argv[3] == "obedece"   # el modelo sí corrige la raíz «valid-» al reescribir
U = cargar_universo(RUTA_UNIVERSO_EJEMPLO)

b0 = nuevo_bloque(tempfile.mkdtemp(), U)
ref = b0.ciclo(AS_OF, alcance={"clases": ["RV"]})
top = [o["opp_id"] for o in ref["paquete"]["clases"]["RV"]["opciones"]]
f3 = b0.almacen.leer("F3", AS_OF)
if modo == "alternativa":
    (e,) = [x for x in f3 if x["clase"] == "RV" and x["opp_id"] not in top
            and any(o["fuerza"] == "fuerte" and not o["resuelta"] for o in x.get("objeciones_internas") or [])]
else:
    e = next(x for x in f3 if x["opp_id"] == top[0])
objetivo = next(o["objecion_id"] for o in e["objeciones_internas"]) .rsplit("-", 1)[0][4:]   # OBJ-<proxy>-nn → proxy
print(f"referencia: {ref.get('entrega') or 'ENTREGADA'} · top-3 {top} · objetivo {modo}: {e['opp_id']} ({objetivo})")

original = mock_respuestas.responder
if not OBEDECE:
    mock_respuestas._obedece_r22 = lambda msg, d: d      # un modelo que no corrige la raíz al reescribir


PRIMERA: dict = {}


def responder(agente, mensajes, semilla):
    enc = mock_respuestas.extraer_encargo(mensajes[0]["content"])["mensaje"]
    es_reescritura = isinstance(enc, dict) and isinstance(enc.get("reescritura"), dict) and enc["reescritura"].get("r22")
    if agente == "AG-11" and es_reescritura and "refutacion" in PRIMERA and not OBEDECE:
        return copy.deepcopy(PRIMERA["refutacion"])   # el modelo repite su respuesta: la raíz persiste tras la reescritura
    d = original(agente, mensajes, semilla)
    if agente == "AG-11" and isinstance(d, dict) and isinstance(d.get("resultados"), list):
        for x in d["resultados"]:
            if isinstance(x, dict) and x.get("ref") == objetivo:
                for o in x.get("objeciones", []):
                    o["argumento"] += TEXTO
            if modo == "alternativa" and isinstance(x, dict) and str(x.get("objecion_id", "")).startswith(f"OBJ-{objetivo}-"):
                x["resuelta"] = False   # la contrarréplica no convence: la fuerte sigue abierta, como en la referencia
        if not es_reescritura and isinstance(enc, dict) and enc.get("peticiones"):
            PRIMERA["refutacion"] = copy.deepcopy(d)
    return d


mock_respuestas.responder = responder
b = nuevo_bloque(tempfile.mkdtemp(), U)
r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
md = Path(r["entregables"]["informe_tecnico"]).read_text(encoding="utf-8")
sel = [o["opp_id"] for o in r["paquete"]["clases"]["RV"]["opciones"]]
print(f"con {TEXTO.strip()!r}: {r.get('entrega') or 'ENTREGADA'} · bloqueos {(r.get('g3_entregables') or {}).get('bloqueos')} · top-3 {sel}"
      f" · «validada» en el técnico: {md.count('validada')} · 4.N.4: {'Alternativas descartadas' in md}")
for g in [x for x in b.almacen.leer("HA", AS_OF) if x.get("tipo_entrada") == "G3V"]:
    m = [c for c in g["comprobaciones"] if c["id"] == "G3-MET-13"]
    print(f"   {g['id']}: {g['dictamen_efectivo']} · G3-MET-13 {[(c['resultado'], c.get('n_incidencias', len(c.get('detalle') or []))) for c in m]}")
for x in b.almacen.leer("F3", AS_OF):
    if x.get("opp_id") == e["opp_id"] or objetivo in str(x.get("objeciones_internas")):
        print("   F3:", x["opp_id"], x.get("estado"), "elegible", x.get("elegible"),
              [(o["objecion_id"], o["fuerza"], o["resuelta"], o["resumen"][-45:]) for o in x.get("objeciones_internas") or []])
