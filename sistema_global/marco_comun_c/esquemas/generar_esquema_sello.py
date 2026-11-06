"""Genera el esquema JSON del sello de corte de K, versión 0.2.0.

0.2.0 (T-26, parte 2): cada fuente disponible lleva instrumento, último cierre y procedencia (proveedor, licencia,
obtenido_en, referencia); el sello lleva el calendario de eventos; Q-01 a Q-15. La 0.1.0 se conserva para el histórico.

Uso: python3 generar_esquema_sello.py > k-sello_0.2.0.schema.json
Comprueba la FORMA. La coherencia entre campos la aplica validador/k_calidad.py (reglas S-xx).
"""
import json

REGLAS = [f"Q-{i:02d}" for i in range(1, 16)]
TIPOS_EVENTO = ["BANCO_CENTRAL", "DATO_MACRO", "RESULTADOS", "DIVIDENDO", "SPLIT", "VENCIMIENTO", "FESTIVO_EXTRA", "OTRO"]
TXT = {"type": "string", "minLength": 1, "maxLength": 200, "pattern": r"\S"}
FECHA = {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}\Z"}
FECHAHORA = {"type": "string",
             "pattern": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})\Z"}
ID = {"type": "string", "pattern": r"^[A-Za-z0-9._:/-]{1,64}\Z"}
SELLO_ID = {"type": "string", "pattern": r"^K-\d{8}-\d{3}\Z"}
HASH = {"type": "string", "pattern": r"^[0-9a-f]{64}\Z"}
RESULTADO = {"enum": ["OK", "ADVERTENCIA", "BLOQUEO"]}


def obj(props, required=None):
    return {"type": "object", "properties": props,
            "required": required if required is not None else list(props),
            "additionalProperties": False}


fuente = {
    "type": "object",
    "properties": {
        "fuente_id": ID,
        "estado": {"enum": ["DISPONIBLE", "NO_DISPONIBLE"]},
        "version_conjunto": ID,
        "ultima_observacion": FECHA,
        "antiguedad_dias_habiles": {"type": "integer", "minimum": 0},
        "hash": HASH,
        "instrumento": ID,
        "ultimo_cierre": {"type": "number", "exclusiveMinimum": 0},
        "procedencia": obj({"proveedor": ID, "licencia": ID, "obtenido_en": FECHAHORA, "referencia": TXT}),
    },
    "required": ["fuente_id", "estado"],
    "additionalProperties": False,
    "allOf": [
        {"if": {"properties": {"estado": {"const": "DISPONIBLE"}}},
         "then": {"required": ["version_conjunto", "ultima_observacion",
                               "antiguedad_dias_habiles", "hash", "instrumento", "ultimo_cierre", "procedencia"]}},
        {"if": {"properties": {"estado": {"const": "NO_DISPONIBLE"}}},
         "then": {"not": {"anyOf": [{"required": ["ultima_observacion"]},
                                    {"required": ["antiguedad_dias_habiles"]},
                                    {"required": ["hash"]}, {"required": ["procedencia"]},
                                    {"required": ["ultimo_cierre"]}]}}},
    ],
}

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://robot-inversor.local/esquemas/k-sello/0.2.0",
    "title": "K · Sello de fecha de corte",
    "description": "Versión 0.2.0 (provisional, 0.x). Registro inmutable; una corrección es un sello nuevo. Procedencia, licencia y calendario de eventos (T-26).",
    "type": "object",
    "properties": {
        "sello_id": SELLO_ID,
        "hash_sello": HASH,
        "version_esquema": {"const": "0.2.0"},
        "fecha_corte": FECHA,
        "fecha_solicitada": FECHA,
        "emitido_en": FECHAHORA,
        "cartera": {"enum": ["TRADING", "TACTICA", "LARGO_PLAZO"]},
        "mercados": {"type": "array", "minItems": 1, "items": obj({
            "mercado": ID, "version_calendario": ID})},
        "fuentes": {"type": "array", "minItems": 1, "items": fuente},
        "version_ajustes": ID,
        "version_reglas": ID,
        "resultado_reglas": {"type": "array", "minItems": 15, "maxItems": 15, "items": obj({
            "regla": {"enum": REGLAS}, "resultado": RESULTADO,
            "detalle": {"type": "string", "pattern": r"\S"}}, required=["regla", "resultado"])},
        "resultado_global": RESULTADO,
        "eventos": {"type": "array", "items": obj({"fecha": FECHA, "tipo": {"enum": TIPOS_EVENTO},
                                                     "instrumentos": {"type": "array", "minItems": 1, "uniqueItems": True, "items": ID},
                                                     "descripcion": TXT, "anunciado_en": FECHAHORA})},
        "estado": {"enum": ["VIGENTE", "CADUCADO", "ANULADO"]},
        "reemplaza_a": SELLO_ID,
    },
    "required": ["sello_id", "hash_sello", "version_esquema", "fecha_corte", "fecha_solicitada", "emitido_en",
                 "cartera", "mercados", "fuentes", "version_ajustes", "version_reglas",
                 "resultado_reglas", "resultado_global", "eventos", "estado"],
    "additionalProperties": False,
}

if __name__ == "__main__":
    print(json.dumps(schema, ensure_ascii=False, indent=2))
