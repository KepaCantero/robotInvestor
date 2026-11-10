"""Hallazgo 4 de la revisión V0.60 — la promesa «toda mutación de valor del sello que respeta la forma
da al menos S-12» es falsa para el campo `estado`, excluido del hash por diseño.

Documento 0 §2 punto 3 y §3 (fila S-12), y LEEME («el sello da S-12 en toda mutación de valor que
respeta la forma»): falso. hash_del_sello excluye `hash_sello` y `estado` («cambia en la vida del
sello»), de modo que VIGENTE->CADUCADO (dentro del enum del esquema, respeta la forma) deja el sello
VÁLIDO y sin S-12. El veneno de la batería (None, "", "x", [], {}, True, 0, -1, 1e308, NaN, ±inf,
"1.1") nunca produce un valor dentro del enum ["VIGENTE","CADUCADO","ANULADO"], así que la
comprobación `sello_valor_que_respeta_la_forma_da_S12` no puede verlo con la semilla actual.

La conducta del producto es defendible y está por capas (el consumidor lo ve: E-16); lo que está mal
es la documentación, que no declara la excepción como hace con las demás. Este guion fija el
comportamiento REAL (pasa si el producto se comporta como se describió al revisor y la documentación
declara la excepción; falla si alguien aprieta el validador sin revisar el documento o al revés).

Ejecutar desde la raíz de marcoC:  python3 hallazgo_4_revision_v060_sello_estado_sin_S12.py
"""
import copy
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "validador"))
sys.path.insert(0, str(RAIZ / "pruebas"))

from validar_sobre import cargar_json
from k_calidad import validar_sello, hash_del_sello
from validar_encargo import validar_encargo
from pruebas_k import CAL
from pruebas_encargo import CTX as CTX_ENC, encargo_div


def main():
    sellos = [(p.name, json.loads(p.read_text(encoding="utf-8")))
              for p in sorted((RAIZ / "pruebas" / "k").glob("valido_*.sello.json"))]
    n, k0 = sellos[0]
    x = copy.deepcopy(k0)
    x["estado"] = "CADUCADO" if x["estado"] == "VIGENTE" else "VIGENTE"
    r = validar_sello(x, {"calendario": CAL})
    reglas = sorted({y.get("regla") for y in r})
    ok_a = (r == [] and "S-12" not in reglas)
    print(("OK   " if ok_a else "FALLA") +
          f"  sello con `estado` alterado dentro del enum -> {reglas or 'VÁLIDO'} (sin S-12: el hash lo excluye)")

    enc = encargo_div()
    enc["payload"]["sello_corte_ref"] = x["sello_id"]
    CT = copy.deepcopy(CTX_ENC)
    CT["sellos"] = dict(CTX_ENC["sellos"])
    CT["sellos"][x["sello_id"]] = x
    r2 = validar_encargo(enc, CT)
    reglas2 = sorted({z.get("regla") for z in r2})
    ok_b = "E-16" in reglas2
    print(("OK   " if ok_b else "FALLA") + f"  consumidor: el encargo lo rechaza con E-16 -> {reglas2}")

    doc = (RAIZ / "entrega_glm" / "V0.60" / "Documento_0.md").read_text(encoding="utf-8")
    declara_excepcion = "estado" in doc and ("excluido" in doc or "excluye" in doc)
    print(("OK   " if declara_excepcion else "FALLA") +
          "  documento: el Documento 0 declara la excepción de `estado` en la promesa S-12")

    if not (ok_a and ok_b):
        print("\nEl comportamiento del producto cambió respecto a lo revisado: revisar la cadena "
              "sello -> encargo antes de aceptar el cambio.")
    elif not declara_excepcion:
        print("\nHALLAZGO 4 (baja): el Documento 0 (§2 punto 3 y §3, fila S-12) y el LEEME prometen "
              "«al menos S-12» para TODA mutación de valor que respeta la forma; falso para `estado` "
              "(excluido del hash por diseño; el consumidor lo ve con E-16). Corrección: declarar la "
              "excepción en §2/§3 y en el LEEME, igual que las demás excepciones por diseño, y fijar "
              "el comportamiento con este caso (estado alterado -> sin S-12, E-16 en el encargo).")
    return 0 if (ok_a and ok_b) else 1


if __name__ == "__main__":
    sys.exit(main())
