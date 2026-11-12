"""Genera los borradores de esquema de los contratos que salen de la tanda 1 (12-11-2026). No toca el marco común: lee su esquema
vigente de CT-G-08 y escribe aquí los borradores, que solo se aplicarán al marco cuando se ratifique la enmienda 5 y se cierre el
diseño de F y de J.

- ct-g-08_0.4.0-borrador.schema.json: CT-G-08 0.3.0 más el tipo de acción que deduce F (cambio 47 de la enmienda 5, decisión 4 de
  la tanda 1; reequilibrio, cambio 78) y cómo lo dedujo. Una acción que reduce, cierra o protege solo se veta por reglas de forma.
- ct-g-24_0.1.0-borrador.schema.json: la anotación del registro de experimentos (decisión 5 de la tanda 1; T-99).

Uso: python3 .docs/diseno/contratos/generar_borradores.py [--comprobar]   (--comprobar: falla si los ficheros no son los que genera)
"""
import copy
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
CT08_VIGENTE = RAIZ / "sistema_global" / "marco_comun_c" / "esquemas" / "ct-g-08_0.3.0.schema.json"
ID = r"^[A-Za-z0-9._:/-]{1,64}\Z"
HASH = r"^[0-9a-f]{64}\Z"
FH = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})\Z"
TIPOS_ACCION = ["ABRIR_O_AUMENTAR", "REDUCIR_O_CERRAR", "PROTEGER", "REEQUILIBRAR"]
# [PROPUESTO] reglas de forma: las únicas que pueden vetar una acción que reduce, cierra o protege (cambio 47):
# F-01 forma o esquema, F-10 cartera sin conciliar o vieja, F-12 sin tipo de cambio, F-23 precio alejado de la referencia del
# intermediario, F-24 (nueva) cantidad mayor que la de la posición conciliada, F-25 (nueva) orden duplicada
REGLAS_FORMA = ["F-01", "F-10", "F-12", "F-23", "F-24", "F-25"]


def ct08() -> dict:
    s = copy.deepcopy(json.loads(CT08_VIGENTE.read_text(encoding="utf-8")))
    s["$id"] = "https://robot-inversor.local/esquemas/ct-g-08/0.4.0-borrador"
    s["title"] = "CT-G-08 · Resultado de control de F, con el tipo de acción (BORRADOR 0.4.0, sin ratificar)"
    s["description"] = ("Borrador de la enmienda 5 (cambios 47 y 78). F deduce el tipo de acción comparando la orden con la posición "
                        "conciliada de G, no con lo que declare quien la pide. Reducir, cerrar o proteger solo se veta por reglas de forma.")
    s["properties"]["version_esquema"] = {"const": "0.4.0"}
    p = s["properties"]["payload"]
    p["properties"]["tipo_accion"] = {"enum": TIPOS_ACCION}
    p["properties"]["deduccion"] = {
        "type": "object", "additionalProperties": False,
        "required": ["posicion_conciliada", "cantidad_solicitada", "sentido_solicitado", "criterio"],
        "properties": {
            "posicion_conciliada": {"type": "object", "additionalProperties": False, "required": ["foto_ref", "cantidad", "direccion"],
                                    "properties": {"foto_ref": {"type": "string", "pattern": HASH},
                                                   "cantidad": {"type": "number", "minimum": 0},
                                                   "direccion": {"enum": ["LARGO", "CORTO", "SIN_POSICION"]}}},
            "cantidad_solicitada": {"type": "number", "exclusiveMinimum": 0},
            "sentido_solicitado": {"enum": ["COMPRA", "VENTA", "STOP"]},
            "criterio": {"type": "string", "pattern": r"\S"}}}
    p["required"] = sorted(set(p["required"]) | {"tipo_accion", "deduccion"})
    # la asimetría: si reduce, cierra o protege, ningún control veta salvo los de forma, y no hay REDUCIDO
    s["allOf"] = [{
        "if": {"properties": {"payload": {"properties": {"tipo_accion": {"enum": ["REDUCIR_O_CERRAR", "PROTEGER"]}}, "required": ["tipo_accion"]}}},
        "then": {"properties": {"resultado_politica": {
            "properties": {"resultado": {"enum": ["APROBADO", "VETADO"]},
                           "controles": {"items": {"if": {"properties": {"resultado": {"const": "VETA"}}, "required": ["resultado"]},
                                                   "then": {"properties": {"regla": {"enum": REGLAS_FORMA}}}}}}}}}}]
    return s


def ct24() -> dict:
    texto = {"type": "string", "minLength": 10}
    comun = {"_seq": {"type": "integer", "minimum": 1}, "_hash_prev": {"type": "string", "pattern": HASH},
             "_hash": {"type": "string", "pattern": HASH}, "exp_id": {"type": "string", "pattern": r"^EXP-\d{4}-\d{4}\Z"}}
    fecha = {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}\Z"}
    pre = {"type": "object", "additionalProperties": False,
           "required": ["tipo", "exp_id", "autor", "creado_en", "version_registro", "contenido", "huella_prerregistro", "_seq", "_hash_prev", "_hash"],
           "properties": {**comun, "tipo": {"const": "PRERREGISTRO"}, "autor": {"type": "string", "pattern": r"\S"},
                          "creado_en": {"type": "string", "pattern": FH}, "version_registro": {"type": "string", "pattern": r"^\d+\.\d+\.\d+\Z"},
                          "huella_prerregistro": {"type": "string", "pattern": HASH},
                          "contenido": {"type": "object", "additionalProperties": True,
                                        "required": ["hipotesis", "objeto", "metrica", "datos", "desde", "hasta", "semilla", "criterio_exito", "max_variantes"],
                                        "properties": {"hipotesis": texto, "metrica": texto, "criterio_exito": texto, "datos": {"type": "string"},
                                                       "objeto": {"enum": ["RECORTE", "INSTRUCCION", "MODELO", "ESTRATEGIA", "PARAMETRO", "BLOQUE", "OTRO"]},
                                                       "desde": fecha, "hasta": fecha, "semilla": {"type": "integer"},
                                                       "max_variantes": {"type": "integer", "minimum": 1, "maximum": 1000}}}}}
    intento = {"type": "object", "additionalProperties": False,
               "required": ["tipo", "exp_id", "n", "variante", "inicio", "huella_prerregistro", "dentro_del_maximo", "_seq", "_hash_prev", "_hash"],
               "properties": {**comun, "tipo": {"const": "INTENTO"}, "n": {"type": "integer", "minimum": 1}, "variante": {"type": "string"},
                              "inicio": {"type": "string", "pattern": FH}, "huella_prerregistro": {"type": "string", "pattern": HASH},
                              "dentro_del_maximo": {"type": "boolean"}}}
    resultado = {"type": "object", "additionalProperties": False,
                 "required": ["tipo", "exp_id", "n", "veredicto", "detalle", "registrado_en", "_seq", "_hash_prev", "_hash"],
                 "properties": {**comun, "tipo": {"const": "RESULTADO"}, "n": {"type": "integer", "minimum": 1},
                                "veredicto": {"enum": ["mejor", "peor", "todavía no se sabe", "fallido"]}, "detalle": {"type": "object"},
                                "registrado_en": {"type": "string", "pattern": FH}}}
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "https://robot-inversor.local/esquemas/ct-g-24/0.1.0-borrador",
            "title": "CT-G-24 · Anotación del registro de experimentos (BORRADOR 0.1.0, sin ratificar)",
            "description": ("Decisión 5 de la tanda 1 (D-53 propuesta). Cada línea del registro es una anotación; la cadena de huellas la "
                            "comprueba el registro, no el esquema. La envoltura común de los contratos CT-G se decide con el diseño de J."),
            "oneOf": [pre, intento, resultado]}


SALIDAS = {"ct-g-08_0.4.0-borrador.schema.json": ct08, "ct-g-24_0.1.0-borrador.schema.json": ct24}


def main() -> int:
    mal = []
    for nombre, f in SALIDAS.items():
        texto = json.dumps(f(), ensure_ascii=False, indent=1, sort_keys=True) + "\n"
        ruta = AQUI / nombre
        if "--comprobar" in sys.argv:
            if not ruta.exists() or ruta.read_text(encoding="utf-8") != texto:
                mal.append(nombre)
        else:
            ruta.write_text(texto, encoding="utf-8")
            print("escrito", nombre)
    if mal:
        print("no coinciden con lo que genera el script:", ", ".join(mal))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
