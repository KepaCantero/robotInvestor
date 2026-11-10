"""T-66 · QA r02 · un paso de ciclo para las pruebas de arrastre (lo lanza r02_02_arrastre.py en un proceso aparte,
con el `bloque_a` que toque en PYTHONPATH: el anterior a T-66 o el corregido).

Uso: python r02_02_paso_arrastre.py <carpeta> <as_of> <modo> <salida.json>
  modo «alta_sin_evidencia»: AG-11 añade una fuerte a cada opción y el Analista la da por resuelta SIN evidencia ni contrarréplica
  modo «alta_con_evidencia»: AG-11 añade una fuerte; el Analista cita 2 evidencias; la contrarréplica (simulado) confirma
  modo «arrastre»: el Analista no propone finalistas nuevas: las vigentes se arrastran desde F3
"""
import json
import sys
from pathlib import Path

from r01_comun import DATOS, Gancho, cfg
import bloque_a
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.orquestacion import Bloque

carpeta, as_of, modo, salida = Path(sys.argv[1]), sys.argv[2], sys.argv[3], Path(sys.argv[4])
CLASE = "RV"


def g(agente, msg, datos):
    if modo.startswith("alta") and agente == "AG-11" and not msg.get("contrarreplicas"):
        for x in datos["resultados"]:
            x["objeciones"] = [o for o in x["objeciones"] if o["fuerza"] != "fuerte"] + [
                {"id": f"OBJ-{x['ref']}-09", "tipo": "evidencia_insuficiente", "fuerza": "fuerte", "argumento": "Forzada por QA",
                 "evidencia": "-", "que_la_resolveria": "Dos fuentes independientes"}]
        return datos
    if modo.startswith("alta") and msg.get("fase") == "RESPUESTA_OBJECIONES":
        con = modo == "alta_con_evidencia"
        return {"respuestas": [{"objecion_id": o["objecion_id"], "respuesta": "Resuelta con los datos de la serie HT-01", "resuelta": True,
                                **({"evidencia_citada": list(o.get("evidencia_disponible") or [])[:2]} if con else {})}
                               for o in msg["objeciones"]]}
    if modo == "arrastre" and isinstance(datos, dict) and "finalistas" in datos:
        datos["finalistas"] = []
    return datos


b = Bloque(cfg(), ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), Gancho(g), carpeta / "estado", carpeta / "ent")
r = b.ciclo(as_of, alcance={"clases": [CLASE]})
f3 = b.almacen.estado("F3")
out = {"bloque_a": bloque_a.__file__, "estado": r["estado"], "entrega": r.get("entrega"), "g3": r.get("g3"),
       "g3_entregables": r.get("g3_entregables"), "limitaciones": (r.get("paquete") or {}).get("limitaciones"),
       "publicadas": [{"opp_id": o["opp_id"], "confianza": o.get("confianza"),
                       "objeciones": o.get("objeciones")} for o in r["paquete"]["clases"][CLASE]["opciones"]],
       "f3": {k: {"estado": v.get("estado"), "veredicto_refutacion": v.get("veredicto_refutacion"), "version": v.get("version"),
                  "confianza": v.get("confianza"), "run_ids": v.get("run_ids"),
                  "fuertes": [{kk: o.get(kk) for kk in ("objecion_id", "resuelta", "evidencia_citada", "contrarreplica", "respuesta")}
                              for o in v.get("objeciones_internas") or [] if o.get("fuerza") == "fuerte"]}
              for k, v in f3.items()},
       "integridad": b.almacen.verificar_integridad() if hasattr(b.almacen, "verificar_integridad") else None}
salida.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
print(json.dumps({"bloque_a": out["bloque_a"], "estado": out["estado"], "publicadas": [(p["opp_id"], p["confianza"]) for p in out["publicadas"]]}))
