"""Genera el esquema JSON de CT-G-01 (encargo de análisis en profundidad) versión 0.2.0.

0.2.0 (T-51): el mandato ya no viaja en el encargo; se cita en SC-1 por versión y huella (`mandato_ref`) y el encargo solo
puede estrecharlo (`restricciones`). Sale `prioridad`, que la Constitución no pide y nada usaba. La 0.1.0 queda RETIRADA
(su esquema se conserva para leer el histórico).

Uso: python3 generar_esquema_encargo.py > ct-g-01_0.2.0.schema.json
Comprueba la FORMA. Las reglas que cruzan campos las aplica validador/validar_encargo.py.
"""
import json

PERFILES = ["C-RV", "C-RF", "C-DIV", "C-MP", "C-IDX", "C-FON",
            "C-DER", "C-INM", "C-CRI", "C-ALT", "C-MON", "C-TCV"]
CARTERAS = ["TRADING", "TACTICA", "LARGO_PLAZO"]
DECISIONES = ["ABRIR_POSICION", "AUMENTAR", "REDUCIR", "CERRAR", "MANTENER", "DESCARTAR", "EXPLORAR"]

FECHA = {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}\Z"}
FECHAHORA = {"type": "string",
             "pattern": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})\Z"}
TXT = {"type": "string", "pattern": r"^[^\s\u200b-\u200d\ufeff](.*[^\s\u200b-\u200d\ufeff])?\Z"}
ID = {"type": "string", "pattern": r"^\S+\Z"}


def obj(props, required=None):
    return {"type": "object", "properties": props,
            "required": required if required is not None else list(props),
            "additionalProperties": False}


payload = obj({
    "pregunta": TXT,
    "decision_informada": {"enum": DECISIONES},
    "cartera_destino": {"enum": CARTERAS},
    "posicion_id": ID,
    "candidato": obj({
        "perfil": {"enum": PERFILES},
        "instrumento": TXT,
        "via_acceso": TXT,
        "paquete_b_ref": ID,
    }),
    "nivel_analisis": {"enum": ["N0", "N1", "N2", "N3"]},
    "fecha_corte": FECHA,
    "sello_corte_ref": ID,
    "mandato_ref": obj({
        "version": {"type": "string", "pattern": r"^MAN-\d+\.\d+\.\d+\Z"},
        "huella": {"type": "string", "pattern": r"^[0-9a-f]{64}\Z"},
    }),
    "restricciones": {**obj({
        "horizonte_dias": obj({"min": {"type": "integer", "minimum": 1},
                               "max": {"type": "integer", "minimum": 1}}),
        "tamano_max_pct_cartera": {"type": "number", "exclusiveMinimum": 0, "maximum": 100},
        "exclusiones": {"type": "array", "minItems": 1, "uniqueItems": True, "items": TXT},
    }, required=[]), "minProperties": 1},
    "presupuesto": obj({
        "coste_max_eur": {"type": "number", "exclusiveMinimum": 0, "maximum": 1000},
        "tiempo_max_min": {"type": "number", "exclusiveMinimum": 0, "maximum": 1440},
        "entrega_antes_de": FECHAHORA,
    }),
}, required=["pregunta", "decision_informada", "cartera_destino", "candidato", "nivel_analisis",
             "fecha_corte", "sello_corte_ref", "mandato_ref", "presupuesto"])

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://robot-inversor.local/esquemas/ct-g-01/0.2.0",
    "title": "CT-G-01 · Encargo de análisis en profundidad",
    "description": "Versión 0.2.0 (provisional, 0.x). Lo emite el Broker o el gestor de cartera y lo recibe C. El mandato se lee de SC-1 (mandato_ref).",
    "type": "object",
    "properties": {
        "event_id": ID,
        "correlation_id": ID,
        "expediente_id": ID,
        "producer": {"enum": ["BROKER", "GESTOR_TRADING", "GESTOR_TACTICA", "GESTOR_LARGO_PLAZO"]},
        "consumer": {"enum": PERFILES},
        "tipo_mensaje": {"const": "CT-G-01"},
        "version_esquema": {"const": "0.2.0"},
        "emitido_en": FECHAHORA,
        "valid_until": FECHAHORA,
        "data_refs": {"type": "array", "minItems": 1, "uniqueItems": True, "items": ID},
        "payload": payload,
        "resultado_politica": obj({
            "controles": {"type": "array", "items": {"type": "string"}},
            "resultado": {"enum": ["APROBADO", "RECHAZADO", "PENDIENTE"]},
            "motivo": {"type": "string"},
            "version_politica": ID,
        }, required=["resultado", "version_politica"]),
    },
    "required": ["event_id", "correlation_id", "expediente_id", "producer", "consumer",
                 "tipo_mensaje", "version_esquema", "emitido_en", "valid_until",
                 "data_refs", "payload", "resultado_politica"],
    "additionalProperties": False,
}

if __name__ == "__main__":
    print(json.dumps(schema, ensure_ascii=False, indent=2))
