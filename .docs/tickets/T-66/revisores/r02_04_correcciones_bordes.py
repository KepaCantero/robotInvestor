"""T-66 · QA r02 · bordes de las correcciones H-02 a H-05 y H-08 (y la entrada de la contrarréplica).

Uso: PYTHONPATH=<ejecutor de A>:<revisores r01>:<revisores r02> python r02_04_correcciones_bordes.py
"""
import math

import numpy as np

from r01_comun import AS_OF, Gancho, bloque, cfg, comprobar, fin
from bloque_a.configuracion import cargar_config
from bloque_a.motor import evaluacion as ev

DEF = lambda: cargar_config(extra={"modo": "backtest"})  # noqa: E731  configuración por defecto (solo DIV)

# H-02 · el EJECUTOR (no el simulado) cae en los tipos activos cuando el modelo no declara tipo en el escalado
def sin_clases(agente, msg, datos):
    if agente == "AG-01" and isinstance(datos, dict) and isinstance(datos.get("escalado"), dict):
        datos["escalado"].pop("clases", None)
    return datos


b = bloque(c=DEF(), cliente=Gancho(sin_clases))
r = b.consulta("Analiza qué conviene hacer ahora", as_of=AS_OF)
comprobar("H-02 · escalado del modelo sin «clases»: el ejecutor usa los tipos activos", (r.get("escalado") or {}).get("clases") == ["DIV"],
          f"escalado {r.get('escalado', {}).get('clases')}")
vistos = {}


def ver_cuerpo(agente, msg, datos):
    if agente == "AG-01":
        vistos["clases_activas"] = msg.get("clases_activas")
    return datos


b = bloque(c=DEF(), cliente=Gancho(ver_cuerpo))
b.decision({"configuracion": {"clases_activas": ["RV", "DIV"]}}, AS_OF)
r = b.consulta("Analiza qué conviene hacer ahora", as_of=AS_OF)
comprobar("H-02 · tras CT-04 [RV, DIV], AG-01 recibe esos tipos y el escalado va a ellos",
          vistos.get("clases_activas") == ["RV", "DIV"], f"AG-01 recibió {vistos.get('clases_activas')}; escalado {r.get('escalado', {}).get('clases')}")

# H-03 · clases_activas con formas no válidas
for valor in ("DIV", {"DIV": True}, None, [None], [], ["DIV", "XXX"]):
    b = bloque(c=DEF())
    rr = b.decision({"configuracion": {"clases_activas": valor}}, AS_OF)
    comprobar(f"H-03 · clases_activas={valor!r}: rechazado y P-02 intacto",
              "P-02" not in rr.get("aplicado", {}) and b.f10()["P-02"] == ["DIV"], f"aplicado {rr.get('aplicado')}; rechazos {rr.get('rechazos')}")

# H-04 · aprobar_certificados con formas no válidas
for valor in ("CERT-2026-0001", {"CERT-2026-0001": 1}, 7, [None], [["CERT-2026-0001"]]):
    b = bloque()
    try:
        rr = b.decision({"aprobar_certificados": valor}, AS_OF)
        comprobar(f"H-04 · aprobar_certificados={valor!r}: nada aprobado, rechazo declarado",
                  rr.get("certificados_aprobados") == [] and bool(rr.get("rechazos")) and len(rr["rechazos"]) <= 1,
                  f"{len(rr.get('rechazos', []))} rechazos: {rr.get('rechazos')}")
    except Exception as e:  # noqa: BLE001
        comprobar(f"H-04 · aprobar_certificados={valor!r}: no lanza excepción", False, f"{type(e).__name__}: {e}")
b = bloque()
rr = b.decision({"aprobar_certificados": []}, AS_OF)
comprobar("H-04 · aprobar_certificados=[]: sin rechazos ni aprobaciones", rr.get("certificados_aprobados") == [] and not rr.get("rechazos"),
          f"{rr.get('rechazos')}")

# H-05 · casi constantes, escalas grandes y varianza pequeña pero real
fechas = [f"2026-01-{1 + i % 10:02d}" for i in range(200)]
for c in (0.0, 1.0, 1e6, -0.3, 0.1 + 0.2):
    res = ev.n_efectiva(fechas, [c] * 200)
    comprobar(f"H-05 · residuos constantes {c}: ρ = 1, n_eff = 10", res["rho"] == 1.0 and math.isclose(res["n_eff"], 10.0), f"{res}")
ruido = (0.3 + np.random.default_rng(0).normal(0, 1e-15, 200)).tolist()
res = ev.n_efectiva(fechas, ruido)
comprobar("H-05 · constante con ruido de coma flotante (1e-15): ρ = 1", res["rho"] == 1.0, f"{res}")
real = [0.3 + (1e-6 if (i // 20) % 2 else 0.0) for i in range(200)]   # varianza pequeña pero real, toda entre fechas
res = ev.n_efectiva([f"2026-01-{1 + (i // 20):02d}" for i in range(200)], real)
comprobar("H-05 · varianza real pequeña (1e-6) no se toma por nula: pasa por el ANOVA", res["nota"] is None and res["rho"] > 0.9, f"{res}")
for malo in ([float("nan")] * 200, [float("inf")] * 200):
    try:
        ev.n_efectiva(fechas, malo)
        comprobar(f"H-05 · residuos {malo[0]}: falla cerrado", False, "no lanzó")
    except ValueError:
        comprobar(f"H-05 · residuos {malo[0]}: falla cerrado", True)

# H-08 · el rango del Analista sale del esquema
from bloque_a import sintesis as si  # noqa: E402
from bloque_a.contratos import FINALISTA  # noqa: E402
rango = FINALISTA["properties"]["probabilidades_propias"]["additionalProperties"]
lim = (rango["minimum"], rango["maximum"])
casos = {lim[0]: lim[0], lim[1]: lim[1], lim[0] - 1e-9: None, lim[1] + 1e-9: None, True: None, "0.5": None, float("nan"): None}
okh8 = all(si._prob_analista({"probabilidades_propias": {"H2": v}}, "H2") == esp for v, esp in casos.items())
comprobar(f"H-08 · _prob_analista respeta el rango del esquema {lim}", okh8)

# Entrada de la contrarréplica: ¿qué recibe el Contradictor de cada evidencia citada?
cap = {}


def g(agente, msg, datos):
    if agente == "AG-11" and msg.get("contrarreplicas"):
        cap["cr"] = msg["contrarreplicas"]
        return datos
    if agente == "AG-11":
        for x in datos["resultados"]:
            x["objeciones"] = [o for o in x["objeciones"] if o["fuerza"] != "fuerte"] + [
                {"id": "Z", "tipo": "evidencia_insuficiente", "fuerza": "fuerte", "argumento": "QA", "evidencia": "-", "que_la_resolveria": "x"}]
        return datos
    if msg.get("fase") == "RESPUESTA_OBJECIONES":
        return {"respuestas": [{"objecion_id": o["objecion_id"], "respuesta": "Resuelta con la evidencia citada", "resuelta": True,
                                "evidencia_citada": [e for e in o["evidencia_disponible"] if not e.startswith("HT-01")][:2]}
                               for o in msg["objeciones"]]}
    return datos


b = bloque(cliente=Gancho(g))
b.ciclo(AS_OF, alcance={"clases": ["RV"]})
sin_contenido = [(x["ref"], e["id"]) for x in cap.get("cr", []) for e in x["evidencia_citada"] if not e.get("afirmacion")]
todas = [(x["ref"], e["id"]) for x in cap.get("cr", []) for e in x["evidencia_citada"]]
comprobar("contrarréplica: cada evidencia citada llega con su contenido (no solo el id)", not sin_contenido,
          f"{len(sin_contenido)}/{len(todas)} sin contenido, p. ej. {sin_contenido[:3]}")
calc = sorted({e for x in cap.get("cr", []) for _, e in [(x['ref'], y['id']) for y in x['evidencia_citada']] if e.startswith("CALC-")})
print(f"    ids CALC citados (comunes a la clase): {calc}")

fin()
