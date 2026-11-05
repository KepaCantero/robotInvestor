"""Genera el esquema JSON de CT-G-03 (informe del Contradictor) versión 0.2.0.

Uso: python3 generar_esquema_contradictor.py > ct-g-03_0.2.0.schema.json
0.2.0 (T-48): autoría (modelo, proveedor y diversidad respecto a C) y escenarios en que la tesis falla, con disparador medible;
cada objeción cita los escenarios a los que se refiere. La 0.1.0 queda RETIRADA (su esquema se conserva para el histórico).
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
        "escenarios": {"type": "array", "uniqueItems": True, "items": ID},   # escenarios de fallo a los que se refiere (C-13)
    })},
    "autoria": {**obj({   # C-11: quién hizo el informe y si aporta diversidad respecto a C (identificadores cerrados, no texto libre)
        "modelo": ID, "proveedor": ID,
        "diversidad": {"enum": ["OTRO_PROVEEDOR", "OTRO_MODELO", "MISMO_MODELO"]},
        "motivo_mismo_modelo": TXT,
    }, required=["modelo", "proveedor", "diversidad"]),
        "if": {"properties": {"diversidad": {"const": "MISMO_MODELO"}}},
        "then": {"required": ["motivo_mismo_modelo"]}, "else": {"not": {"required": ["motivo_mismo_modelo"]}}},
    "escenarios_fallo": {"type": "array", "minItems": 1, "maxItems": 20, "items": obj({   # C-12: dónde falla la tesis
        "id": ID,
        "descripcion": TXT,
        "disparador": obj({"metrica": ID, "operador": {"enum": ["<", "<=", ">", ">=", "=="]}, "umbral": {"type": "number"}, "unidad": ID}),
        "consecuencia": {"enum": ["INVALIDA_TESIS", "PERDIDA"]},
        "perdida_pct": {"type": "number", "minimum": -100, "exclusiveMaximum": 0},
        "evid_refs": {"type": "array", "minItems": 1, "uniqueItems": True, "items": ID},
    }, required=["id", "descripcion", "disparador", "consecuencia", "evid_refs"]) | {
        "if": {"properties": {"consecuencia": {"const": "PERDIDA"}}},
        "then": {"required": ["perdida_pct"]}, "else": {"not": {"required": ["perdida_pct"]}}}},
    "veredicto": {"enum": ["SIN_OBJECIONES_RELEVANTES", "OBJECION_MAYOR", "OBJECION_CRITICA"]},
    "cobertura": obj({
        "revisadas": {"type": "array", "minItems": 1, "uniqueItems": True, "items": SECCION},
        "no_revisadas": {"type": "array", "items": obj({"seccion": SECCION, "motivo": TXT})},
    }),
})

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://robot-inversor.local/esquemas/ct-g-03/0.2.0",
    "title": "CT-G-03 · Informe del Contradictor",
    "description": "Versión 0.2.0 (provisional, 0.x; T-48: autoría y escenarios de fallo). La 0.1.0 está retirada. Lo emite el Contradictor y lo recibe el Orquestador.",
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
