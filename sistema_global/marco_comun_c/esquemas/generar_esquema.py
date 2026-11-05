"""Genera el esquema JSON de CT-G-02 (sobre común de valoración) versión 0.1.0.

Uso: python3 generar_esquema.py > ct-g-02_0.1.0.schema.json
El esquema comprueba la FORMA. Las reglas que cruzan campos (topes de confianza,
probabilidades que suman 1, caducidad, etc.) las aplica validador/validar_sobre.py.
"""
import json

PERFILES = ["C-RV", "C-RF", "C-DIV", "C-MP", "C-IDX", "C-FON",
            "C-DER", "C-INM", "C-CRI", "C-ALT", "C-MON", "C-TCV"]
FACTORES = ["TIPOS", "RV", "USD", "CREDITO", "INFLACION",
            "MATERIAS_PRIMAS", "VOLATILIDAD", "LIQUIDEZ"]
EPISODIOS = ["EP-2008-LEHMAN", "EP-2011-EUROZONA", "EP-2015-SNB",
             "EP-2018-Q4", "EP-2020-COVID", "EP-2022-TIPOS"]
ESTADOS_CIFRA = ["VERIFICADO", "ESTIMADO", "SUPUESTO", "NO_ESTIMABLE"]


def ref(n):
    return {"$ref": f"#/$defs/{n}"}


def obj(props, required=None, extra=False):
    return {"type": "object", "properties": props,
            "required": required if required is not None else list(props),
            "additionalProperties": extra}


cifra_ids = {"type": "string", "minLength": 1}
FECHA = {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}$"}
FECHAHORA = {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$"}
TXT = {"type": "string", "pattern": r"\S"}
defs = {
    "Cifra": obj({
        "valor": {"type": ["number", "null"]},
        "unidad": {"type": "string", "minLength": 1},
        "estado": {"enum": ESTADOS_CIFRA},
        "modelo_ref": cifra_ids,
        "motor_id": cifra_ids,
    }, required=["valor", "unidad", "estado"]),
    "Texto": {"type": "string", "pattern": r"\S"},
    "Condicion": obj({
        "id": {"type": "string", "minLength": 1},
        "descripcion": {"type": "string", "minLength": 1},
        "metrica": {"type": "string", "minLength": 1},
        "operador": {"enum": ["<", "<=", ">", ">=", "=="]},
        "umbral": {"type": "number"},
        "unidad": {"type": "string", "minLength": 1},
    }),
    "Escenario": obj({
        "nombre": {"type": "string", "minLength": 1},
        "probabilidad": {"type": "number", "minimum": 0, "maximum": 1},
        "rentabilidad_neta_pct": {"type": "number"},
        "horizonte_dias": {"type": "integer", "minimum": 1},
    }),
    "EstadoExclusion": {"enum": ["OK", "BLOQUEADO", "DESCONOCIDO"]},
}

identificacion = obj({
    "perfil": {"enum": PERFILES},
    "clase_comparabilidad": {"enum": ["Q", "S", "K"]},
    "instrumento": ref("Texto"),
    "via_acceso": ref("Texto"),
    "direccion": {"enum": ["LARGO", "CORTO", "NEUTRAL"]},
    "cartera_compatible": {"type": "array", "minItems": 1, "uniqueItems": True,
                           "items": {"enum": ["TRADING", "TACTICA", "LARGO_PLAZO"]}},
    "nivel_analisis": {"enum": ["N0", "N1", "N2", "N3"]},
    "fecha_corte": FECHA,
    "divisa_base": {"const": "EUR"},
})

payload_props = {
    "identificacion": identificacion,
    "tesis": obj({
        "resumen": ref("Texto"),
        "supuestos": {"type": "array", "items": ref("Texto")},
        "condiciones_invalidez": {"type": "array", "items": ref("Condicion")},
    }),
    "entrada_salida": obj({
        "entrada": ref("Texto"),
        "stop": ref("Cifra"),
        "objetivo": ref("Cifra"),
        "fecha_revision": FECHA,
    }),
    "liquidez": obj({
        "tiempo_salida": ref("Cifra"),
        "coste_salida": ref("Cifra"),
        "tamano_max_sin_impacto": ref("Cifra"),
    }),
    "costes": obj({
        "entrada": ref("Cifra"),
        "mantenimiento_anual": ref("Cifra"),
        "salida": ref("Cifra"),
        "impacto_fiscal": ref("Cifra"),
    }),
    "capital": obj({
        "capital_necesario": ref("Cifra"),
        "margen": ref("Cifra"),
        "apalancamiento": ref("Cifra"),
    }),
    "estres_historico": obj({
        "conjunto_version": {"type": "string", "minLength": 1},
        "episodios": {"type": "array", "items": obj({
            "episodio_id": {"enum": EPISODIOS},
            "perdida": ref("Cifra"),
        })},
    }),
    "factores": obj({
        "conjunto_version": {"type": "string", "minLength": 1},
        "ventana_dias": {"type": "integer", "minimum": 1},
        "calidad_ajuste": ref("Cifra"),
        "exposiciones": {"type": "array", "items": obj({
            "factor": {"enum": FACTORES},
            "beta": ref("Cifra"),
        })},
    }),
    "evidencia": obj({
        "frescura_horas": {"type": "number", "minimum": 0},
        "proporcion": obj({
            "VERIFICADO": {"type": "number", "minimum": 0, "maximum": 1},
            "ESTIMADO": {"type": "number", "minimum": 0, "maximum": 1},
            "SUPUESTO": {"type": "number", "minimum": 0, "maximum": 1},
        }),
    }),
    "exclusiones_duras": obj({
        "sanciones": ref("EstadoExclusion"),
        "invertibilidad": ref("EstadoExclusion"),
        "acceso": ref("EstadoExclusion"),
    }),
    "referencias": obj({
        "cuerpo_especializado_ref": {"type": "string", "minLength": 1},
        "artefactos_motor": {"type": "array", "items": {"type": "string", "minLength": 1}},
    }),
    "capa2": obj({
        "estado": {"enum": ["ESTIMADO", "SUPUESTO", "NO_ESTIMABLE"]},
        "metodo": {"type": "string", "minLength": 1},
        "base_datos": {"type": "string", "minLength": 1},
        "escenarios": {"type": "array", "items": ref("Escenario")},
    }, required=["estado"]),
    "capa3": obj({
        "tope_confianza": {"type": "number", "minimum": 0, "maximum": 1},
        "confianza": {"type": "number", "minimum": 0, "maximum": 1},
        "doble_analisis": obj({
            "realizado": {"type": "boolean"},
            "discrepa": {"type": "boolean"},
        }),
    }),
    # Extensión del perfil: libre en 0.x, pero debe declarar su propio esquema.
    "cuerpo_especializado": obj({
        "esquema_ref": {"type": "string", "minLength": 1},
        "version": {"type": "string", "minLength": 1},
        "contenido": {"type": "object"},
    }, required=["esquema_ref", "version", "contenido"]),
}

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://robot-inversor.local/esquemas/ct-g-02/0.1.0",
    "title": "CT-G-02 · Sobre común de valoración",
    "description": "Versión 0.1.0 (provisional, 0.x). Congelación en 1.0.0 tras C-DIV y C-RV.",
    "type": "object",
    "properties": {
        "event_id": {"type": "string", "minLength": 1},
        "correlation_id": {"type": "string", "minLength": 1},
        "expediente_id": {"type": "string", "minLength": 1},
        "producer": {"enum": PERFILES},
        "consumer": {"enum": ["D", "BROKER", "VERIFICACION"]},
        "tipo_mensaje": {"const": "CT-G-02"},
        "version_esquema": {"type": "string", "pattern": r"^\d+\.\d+\.\d+$"},
        "emitido_en": FECHAHORA,
        "valid_until": FECHAHORA,
        "data_refs": {"type": "array", "minItems": 1, "uniqueItems": True, "items": {"type": "string", "minLength": 1}},
        "payload": {
            "type": "object",
            "properties": payload_props,
            "required": ["identificacion", "exclusiones_duras", "evidencia"],
            "additionalProperties": False,
        },
        "incertidumbre": {"type": "array", "minItems": 1, "items": ref("Texto")},
        "resultado_politica": obj({
            "controles": {"type": "array", "items": {"type": "string"}},
            "resultado": {"enum": ["APROBADO", "RECHAZADO", "PENDIENTE"]},
            "motivo": {"type": "string"},
            "version_politica": {"type": "string", "minLength": 1},
        }, required=["resultado", "version_politica"]),
    },
    "required": ["event_id", "correlation_id", "expediente_id", "producer", "consumer",
                 "tipo_mensaje", "version_esquema", "emitido_en", "valid_until",
                 "data_refs", "payload", "incertidumbre", "resultado_politica"],
    "additionalProperties": False,
    "$defs": defs,
}

if __name__ == "__main__":
    print(json.dumps(schema, ensure_ascii=False, indent=2))
