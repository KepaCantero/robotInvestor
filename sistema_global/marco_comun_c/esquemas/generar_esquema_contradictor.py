"""Genera el esquema JSON de CT-G-03 (informe del Contradictor) versión 0.1.0.

Uso: python3 generar_esquema_contradictor.py > ct-g-03_0.1.0.schema.json
Comprueba la FORMA. Las reglas que cruzan campos las aplica validador/validar_contradictor.py.
"""
import json

FECHAHORA = {"type": "string",
             "pattern": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})\Z"}
TXT = {"type": "string", "pattern": r"^[^\s​-‍﻿]([\s\S]*[^\s​-‍﻿])?\Z"}
ID = {"type": "string", "pattern": r"^[A-Za-z0-9._:/-]{1,64}\Z"}
HASH = {"type": "string", "pattern": r"^[0-9a-f]{64}\Z"}
SECCION = {"type": "string", "pattern": r"^[a-z0-9_]{1,40}\Z"}


def obj(props, required=None):
    return {"type": "object", "properties": props,
            "required": required if required is not None else list(props),
            "additionalProperties": False}


payload = obj({
    "sobre_ref": obj({"event_id": ID, "hash": HASH}),
    "nivel_analisis": {"enum": ["N0", "N1", "N2", "N3"]},
    "independencia": obj({"vio_conclusion": {"type": "boolean"}, "vio_confianza": {"type": "boolean"},
                          "contexto_compartido_con_c": {"type": "boolean"}}),
    "objeciones": {"type": "array", "maxItems": 50, "items": obj({
        "id": ID,
        "tipo": {"enum": ["DATO", "LOGICA", "SUPUESTO", "RIESGO_OMITIDO", "ALTERNATIVA"]},
        "gravedad": {"enum": ["MENOR", "MAYOR", "CRITICA"]},
        "texto": TXT,
        "evid_refs": {"type": "array", "uniqueItems": True, "items": ID},
    })},
    "veredicto": {"enum": ["SIN_OBJECIONES_RELEVANTES", "OBJECION_MAYOR", "OBJECION_CRITICA"]},
    "cobertura": obj({
        "revisadas": {"type": "array", "minItems": 1, "uniqueItems": True, "items": SECCION},
        "no_revisadas": {"type": "array", "items": obj({"seccion": SECCION, "motivo": TXT})},
    }),
})

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://robot-inversor.local/esquemas/ct-g-03/0.1.0",
    "title": "CT-G-03 · Informe del Contradictor",
    "description": "Versión 0.1.0 (provisional, 0.x). Lo emite el Contradictor y lo recibe el Orquestador.",
    "type": "object",
    "properties": {
        "event_id": ID, "correlation_id": ID, "expediente_id": ID,
        "producer": {"const": "CONTRADICTOR"}, "consumer": {"const": "ORQUESTADOR"},
        "tipo_mensaje": {"const": "CT-G-03"},
        "version_esquema": {"type": "string", "pattern": r"^\d+\.\d+\.\d+\Z"},
        "emitido_en": FECHAHORA, "valid_until": FECHAHORA,
        "data_refs": {"type": "array", "uniqueItems": True, "items": ID},
        "payload": payload,
    },
    "required": ["event_id", "correlation_id", "expediente_id", "producer", "consumer", "tipo_mensaje",
                 "version_esquema", "emitido_en", "valid_until", "data_refs", "payload"],
    "additionalProperties": False,
}

if __name__ == "__main__":
    print(json.dumps(schema, ensure_ascii=False, indent=2))
