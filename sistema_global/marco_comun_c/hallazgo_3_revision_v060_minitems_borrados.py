"""Hallazgo 3 de la revisión V0.60 — _forma_real reclasifica como «de valor» los borrados de elementos
de lista que dejan la lista POR DEBAJO de su minItems (que SÍ rompen la forma del esquema JSON).

La justificación de la reclasificación (Documento 0 §2 punto 3) es «el esquema admite cualquier
longitud sobre su mínimo», pero _forma_real no mira el mínimo: borrar el último elemento de una lista
con minItems 1 (cartera_compatible, incertidumbre del sobre; revisadas, escenarios_fallo, evid_refs
del informe; mercados, fuentes, resultado_reglas del sello) deja el documento NO conforme y la
batería deja de exigir la regla de esquema justo ahí (solo las promesas generales).

El producto está limpio: esta sonda demuestra los seis casos y todos acaban en la regla de esquema.
Mientras la batería no exija la regla también en esos casos (regresión r03_…), este guion FALLA.

Ejecutar desde la raíz de marcoC:  python3 hallazgo_3_revision_v060_minitems_borrados.py
"""
import copy
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "validador"))
sys.path.insert(0, str(RAIZ / "pruebas"))

from validar_sobre import validar, cargar_json
from validar_contradictor import validar_informe
from k_calidad import validar_sello
from pruebas_contradictor import AHORA as AHORA_CTR, informe as informe_ctr, sobre_base
from pruebas_k import CAL


def casos():
    out = []
    sobres = [(p.name, cargar_json(p.read_text(encoding="utf-8")))
              for p in sorted((RAIZ / "pruebas" / "validos").glob("*.json"))]
    CTX = json.loads((RAIZ / "pruebas" / "contexto.json").read_text(encoding="utf-8"))
    for n, s in sobres:
        if len(s["payload"]["identificacion"]["cartera_compatible"]) == 1:
            x = copy.deepcopy(s)
            del x["payload"]["identificacion"]["cartera_compatible"][0]
            out.append(("sobre", f"{n}: cartera_compatible 1->0", x, CTX, "V-01"))
            break
    s0 = sobres[0][1]
    if len(s0["incertidumbre"]) == 1:
        x = copy.deepcopy(s0)
        del x["incertidumbre"][0]
        out.append(("sobre", "incertidumbre 1->0", x, CTX, "V-01"))
    inf = informe_ctr(sobre_base())
    if len(inf["payload"]["cobertura"]["revisadas"]) == 1:
        y = informe_ctr(sobre_base())
        del y["payload"]["cobertura"]["revisadas"][0]
        out.append(("informe", "revisadas 1->0", y,
                    {"ahora": AHORA_CTR, "sobre": copy.deepcopy(sobre_base())}, "C-01"))
    if len(inf["payload"]["escenarios_fallo"]) == 1:
        y2 = informe_ctr(sobre_base())
        del y2["payload"]["escenarios_fallo"][0]
        out.append(("informe", "escenarios_fallo 1->0", y2,
                    {"ahora": AHORA_CTR, "sobre": copy.deepcopy(sobre_base())}, "C-01"))
        y3 = informe_ctr(sobre_base())
        if len(y3["payload"]["escenarios_fallo"][0]["evid_refs"]) == 1:
            del y3["payload"]["escenarios_fallo"][0]["evid_refs"][0]
            out.append(("informe", "evid_refs 1->0", y3,
                        {"ahora": AHORA_CTR, "sobre": copy.deepcopy(sobre_base())}, "C-01"))
    sellos = [(p.name, json.loads(p.read_text(encoding="utf-8")))
              for p in sorted((RAIZ / "pruebas" / "k").glob("valido_*.sello.json"))]
    for n, k in sellos:
        if len(k["mercados"]) == 1:
            x = copy.deepcopy(k)
            del x["mercados"][0]
            out.append(("sello", f"{n}: mercados 1->0", x, {"calendario": CAL}, "S-01"))
            break
    k0 = sellos[0][1]
    if len(k0["resultado_reglas"]) == 15:
        x = copy.deepcopy(k0)
        del x["resultado_reglas"][7]
        out.append(("sello", "resultado_reglas 15->14 (minItems 15)", x, {"calendario": CAL}, "S-01"))
    return out


def la_bateria_exige_la_regla_en_minitems():
    fuente = (RAIZ / "pruebas" / "pruebas_robustez_validadores.py").read_text(encoding="utf-8")
    marca = "minItems" in fuente or "bajo_minItems" in fuente or "minimo" in fuente.lower()
    return marca, "la batería trata los borrados bajo minItems" if marca else \
        "_forma_real reclasifica todo borrado de elemento de lista como «de valor», sin mirar el mínimo"


def main():
    mal = []
    for modulo, nombre, msg, ctx, esperada in casos():
        if modulo == "sobre":
            r = validar(copy.deepcopy(msg), copy.deepcopy(ctx))
        elif modulo == "informe":
            r = validar_informe(copy.deepcopy(msg), copy.deepcopy(ctx))
        else:
            r = validar_sello(copy.deepcopy(msg), copy.deepcopy(ctx))
        reglas = sorted({x.get("regla") for x in r})
        ok = esperada in reglas
        print(("OK   " if ok else "FALLA") + f"  producto: {modulo} {nombre} -> {reglas or 'VÁLIDO'} (esperada {esperada})")
        if not ok:
            mal.append(nombre)
    ok_bat, det_bat = la_bateria_exige_la_regla_en_minitems()
    print(("OK   " if ok_bat else "FALLA") + f"  batería:  {det_bat}")
    if mal or not ok_bat:
        print("\nHALLAZGO 3 (baja): los borrados que dejan una lista bajo su minItems rompen la forma "
              "del esquema y sin embargo la batería no exige en ellos la regla de esquema (solo las "
              "promesas generales). El validador de verdad sí falla cerrado en los seis casos sondeados. "
              "Corrección: en los objetivos MENSAJE, reclasificar como «de forma» el borrado que deja "
              "la lista vacía o bajo su mínimo (o exigir la regla también ahí) + regresión r03_….")
    return 0 if (not mal and ok_bat) else 1


if __name__ == "__main__":
    sys.exit(main())
