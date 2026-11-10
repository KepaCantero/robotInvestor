"""Hallazgo 2 de la revisión V0.60 — claves del contexto que el Orquestador pasa siempre y la batería
no muta: `sc3` y `sello_encargo` (sobre), `autoria_c`/`autoria_contradictor` (informe).

El Documento 0 (§1) promete «mutando tanto el mensaje como cada clave de su contexto» y §2 punto 4
dice que validar_sobre «solo lee» ahora, fecha_corte_encargo, perfiles, clases y la bandera. Falso:
con el contexto que el Orquestador pasa SIEMPRE (orquestador.py, llamada de validar_sobre) también
lee `sc3` y `sello_encargo` (camino V-26), y `validar_informe` lee `autoria_c` y
`autoria_contradictor` cuando están configuradas. La batería no muta esas claves (CLAVES_CTX_SOBRE
tiene 5 claves; el fixture contexto.json no lleva sc3).

El producto está limpio: esta sonda demuestra que sc3/sello_encargo corruptos dan V-01. FALLA la
cobertura y la exactitud de la documentación hasta que la batería los incluya (regresión r02_…).

Ejecutar desde la raíz de marcoC:  python3 hallazgo_2_revision_v060_contexto_sc3_sello.py
"""
import copy
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "validador"))
sys.path.insert(0, str(RAIZ / "pruebas"))

from validar_sobre import validar, cargar_json
from pruebas_contradictor import AHORA as AHORA_CTR, informe as informe_ctr, sobre_base


def sondas_producto():
    sobres = [(p.name, cargar_json(p.read_text(encoding="utf-8")))
              for p in sorted((RAIZ / "pruebas" / "validos").glob("*.json"))]
    CTX = json.loads((RAIZ / "pruebas" / "contexto.json").read_text(encoding="utf-8"))
    s0 = sobres[0][1]
    out = []
    c = copy.deepcopy(CTX)
    c["sc3"] = "x"
    out.append(("sc3 corrompido -> V-01", "V-01" in {x["regla"] for x in validar(copy.deepcopy(s0), c)}))
    c2 = copy.deepcopy(CTX)
    c2["sc3"] = {"historial": [], "estado": "VIGENTE", "entradas": []}
    c2["sello_encargo"] = ["no", "es", "texto"]
    out.append(("sello_encargo corrompido (con sc3) -> V-01",
                "V-01" in {x["regla"] for x in validar(copy.deepcopy(s0), c2)}))
    return out


def la_bateria_cubre_las_claves():
    fuente = (RAIZ / "pruebas" / "pruebas_robustez_validadores.py").read_text(encoding="utf-8")
    return ("sc3" in fuente) and ("sello_encargo" in fuente), \
        "la batería menciona sc3/sello_encargo entre las claves mutadas" if "sc3" in fuente else \
        "CLAVES_CTX_SOBRE y la cabecera de la batería no incluyen sc3 ni sello_encargo"


def main():
    todo_ok = True
    for nombre, ok in sondas_producto():
        print(("OK   " if ok else "FALLA") + f"  producto: {nombre}")
        todo_ok &= ok
    ok_bat, det_bat = la_bateria_cubre_las_claves()
    print(("OK   " if ok_bat else "FALLA") + f"  batería:  {det_bat}")
    todo_ok &= ok_bat
    if not ok_bat:
        print("\nHALLAZGO 2 (media): el Documento 0 §2.4 («solo lee») es incompleto y §1 («cada clave "
              "de su contexto») no se cumple para las claves que el Orquestador pasa siempre. "
              "Corrección: mutar sc3 y sello_encargo en la batería (ADMITE: V-01/V-26), mutar "
              "autoria_c/autoria_contradictor del informe con un fixture que las traiga, y corregir "
              "el §2.4 del Documento 0.")
    return 0 if todo_ok else 1


if __name__ == "__main__":
    sys.exit(main())
