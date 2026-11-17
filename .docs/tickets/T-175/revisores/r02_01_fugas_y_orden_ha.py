"""QA r02 de T-175 (revisor): (1) textos del modelo en 4.N.4 o en la sección 6 que se escapen de la sustitución de G3-MET-13;
(2) si poner delante las ADVERTENCIAS de las alternativas tapa un BLOQUEO en los cinco detalles que guarda el G3V de F7 en HA.

    cd bloque_a/11_Ejecutor && ../../.venv/bin/python ../../.docs/tickets/T-175/revisores/r02_01_fugas_y_orden_ha.py
Una línea por caso: OK o FUGA/TAPA. Informe, no prueba (sale con 0).
"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, "tests")
from conftest import AS_OF, RUTA_UNIVERSO_EJEMPLO, cargar_universo, nuevo_bloque  # noqa: E402

from bloque_a import sintesis as sint  # noqa: E402
from bloque_a.herramientas import ht09  # noqa: E402

b = nuevo_bloque(tempfile.mkdtemp(), cargar_universo(RUTA_UNIVERSO_EJEMPLO))
r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
paquete = r["paquete"]

TEXTOS = ["La señal no está validada.", "Falta RISK-XYZ-999.", "ST-DESC-001 [madurez: VALIDADO]", "[madurez: IMPLEMENTADO] sin ficha",
          "No está implementado el método.", "Sin VALIDACIÓN externa.", "RISK-XYZ-\n999 partido", "RISK-XYZ|-999 con barra",
          "invalidación de la tesis", "Revalidar con datos", "convalidado por el comité", "Rk válido", "válido con tilde",
          "VOL-GARCH-001 sin arch", "AUD-REX-001", "ST‑DESC‑001 con guiones no ASCII", "ST-DESC-001"]
CAMPOS = ("nombre", "resumen", "respuesta", "que_la_resolveria")


def candidata(campo, t):
    o = {"objecion_id": "OBJ-ZZZ-01", "fuerza": "fuerte", "resumen": "Una sola raíz", "respuesta": "Respuesta suficiente aquí",
         "resuelta": False, "que_la_resolveria": "Una segunda raíz"}
    f = {"opp_id": "OPP-2026-0999", "proxy": "ZZZ", "nombre": "Ámbito ZZZ", "_objeciones": [o],
         "_ht03": {"elegible": False, "puntuaciones": {"RK": 50},
                   "motivos_no_elegible": [{"codigo": "OBJECION_FUERTE", "detalle": "1 objeción(es) fuerte(s) sin resolver"}]}}
    (f if campo == "nombre" else o)[campo] = t
    return f


for campo in CAMPOS:
    for t in TEXTOS:
        extras = {"seleccion": {"RV": {"candidatos": [candidata(campo, t)]}}, "gc0": r["gc0"]}
        extras["alternativas_descartadas"] = sint.alternativas_descartadas(paquete, extras, b)
        md = b.redaccion.tecnico(paquete, extras, {"dictamen": "APTO"}, {}, "COMPLETO", {})
        # solo lo de la alternativa: el párrafo de 4.1.4 y las filas «(alternativa descartada)», con una ficha IMPLEMENTADA al lado
        trozo = "\n".join(x for x in md.splitlines() if "OPP-2026-0999" in x) + "\nMétodo ST-DESC-001."
        comp = sint._comprobar_met13(b, [("informe_tecnico, línea 1", trozo, "BLOQUEO")])
        bloquea = any(i["severidad"] == "BLOQUEO" for i in comp["incidencias"])
        ret = extras["alternativas_descartadas"]["RV"][0]["retirados"]
        print(f"{'FUGA' if bloquea else 'OK  '} {campo:18} {t!r:42} retirados={ret}")

# (2) orden en HA: un BLOQUEO previo de G3-MET-13 (p. ej. del visual) y seis alternativas con texto retirado
res = {"dictamen": "BLOQUEADO", "resumen": {}, "comprobaciones": [{"id": ht09.ID_MET13, "nombre": ht09.NOMBRE_MET13, "resultado": "BLOQUEO", "datos": {"fichas_citadas": []},
       "incidencias": [{"severidad": "BLOQUEO", "ruta": "informe_visual", "detalle": "G3-MET-13 (R22): «validado» en el visual"}]}]}
alts = {"RV": [{"opp_id": f"OPP-2026-09{i:02d}", "retirados": ["nombre"]} for i in range(6)]}
sint.advertir_alternativas_retiradas(res, alts)
c = res["comprobaciones"][0]
cinco = [i["detalle"] for i in c["incidencias"]][:5]   # lo que escribe redaccion.generar en el G3V de F7
print(("TAPA" if not any("visual" in d for d in cinco) else "OK  ") + f" BLOQUEO previo en los 5 detalles de HA · resultado {c['resultado']}"
      f" · dictamen {res['dictamen']}")
# lo mismo con el BLOQUEO del técnico, que `g3_met13_tecnico` añade al final, después de las advertencias
res2 = {"dictamen": "APTO", "resumen": {}, "comprobaciones": [{"id": ht09.ID_MET13, "nombre": ht09.NOMBRE_MET13, "resultado": "OK", "datos": {"fichas_citadas": []}, "incidencias": []}]}
sint.advertir_alternativas_retiradas(res2, alts)
sint.g3_met13_tecnico(b, res2, "El método ST-DESC-001 está validado.")
cinco = [i["detalle"] for i in res2["comprobaciones"][0]["incidencias"]][:5]
print(("TAPA" if not any("BLOQUEO" in str(i.get("severidad")) for i in res2["comprobaciones"][0]["incidencias"][:5]) else "OK  ")
      + f" BLOQUEO del técnico en los 5 detalles de HA · dictamen {res2['dictamen']}")
