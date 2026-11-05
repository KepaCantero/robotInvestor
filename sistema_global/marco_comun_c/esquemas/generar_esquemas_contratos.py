"""Genera los esquemas JSON de los contratos que el sistema ya emite o recibe (T-25) y el registro de los 16 contratos.

Uso: python3 esquemas/generar_esquemas_contratos.py   (escribe los ficheros en esta carpeta)

Envoltura común (Constitución, «sobre común»): event_id, correlation_id, expediente_id, producer, consumer, tipo_mensaje,
version_esquema, emitido_en, valid_until, data_refs, payload y, si lo hay, resultado_politica. Desde T-47 (REG-0.2.0) todos los
contratos con esquema la usan y el registro admite varias versiones por contrato (VIGENTE o RETIRADA). Los esquemas comprueban la
FORMA; las reglas que cruzan campos o miran el estado del sistema las aplican el Orquestador y los validadores de cada bloque.
"""
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
FH = {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})\Z"}
FECHA = {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}\Z"}
ID = {"type": "string", "pattern": r"^[A-Za-z0-9._:/-]{1,64}\Z"}
ID_O_NULO = {"anyOf": [ID, {"type": "null"}]}
TXT = {"type": "string", "pattern": r"\S"}                      # texto libre con algo más que espacios
REF = {"type": "string", "minLength": 1}                        # referencias tal como las admite CT-G-02 (data_refs, event_id del sobre)
NUM = {"type": "number"}
POS = {"type": "number", "exclusiveMinimum": 0}
NUM0 = {"type": "number", "minimum": 0}
HASH = {"type": "string", "pattern": r"^[0-9a-f]{64}\Z"}
CARTERA = {"enum": ["TRADING", "TACTICA", "LARGO_PLAZO"]}
OPERADOR = {"enum": ["<", "<=", ">", ">=", "=="]}
BOOL = {"type": "boolean"}


def obj(props, required=None, extra=False):
    return {"type": "object", "properties": props, "required": required if required is not None else list(props),
            "additionalProperties": extra}


def envoltura(tipo, version, titulo, de, a, payload, producer, consumer, con_expediente=True, con_vigencia=True, politica=False,
              data_refs=None, sin_vigencia=False):
    props = {
        "event_id": ID,
        "correlation_id": ID if con_expediente else ID_O_NULO,
        "expediente_id": ID if con_expediente else ID_O_NULO,
        "producer": producer, "consumer": consumer,
        "tipo_mensaje": {"const": tipo}, "version_esquema": {"const": version},
        "emitido_en": FH,
        "valid_until": {"type": "null"} if sin_vigencia else FH if con_vigencia else {"anyOf": [FH, {"type": "null"}]},
        "data_refs": data_refs or {"type": "array", "uniqueItems": True, "items": REF},
        "payload": payload,
    }
    if politica:
        props["resultado_politica"] = politica
    req = list(props)
    return {"$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": f"https://robot-inversor.local/esquemas/{tipo.lower()}/{version}",
            "title": f"{tipo} · {titulo}",
            "description": f"Versión {version} (provisional, 0.x). {de} → {a}. Envoltura común de la Constitución.",
            "type": "object", "properties": props, "required": req, "additionalProperties": False}


CONDICION = {**obj({"id": ID, "tipo": {"enum": ["STOP", "OBJETIVO", "INVALIDEZ"]}, "metrica": TXT, "operador": OPERADOR, "umbral": NUM,
                    "unidad": TXT, "fraccion": {"type": "number", "exclusiveMinimum": 0, "exclusiveMaximum": 1}},
                   required=["id", "tipo", "metrica", "operador", "umbral"], extra=True),   # la invalidez se copia del sobre, con lo que traiga
             "if": {"required": ["fraccion"]}, "then": {"properties": {"tipo": {"const": "OBJETIVO"}}}}   # solo un OBJETIVO reduce
REFERENCIA = obj({"benchmark_ref": ID, "rentabilidad_anual_pct": {"type": "number", "minimum": -5, "maximum": 50}})

ESQUEMAS = {}   # (tipo, versión) -> esquema

ESQUEMAS[("CT-G-04", "0.1.0")] = envoltura(
    "CT-G-04", "0.1.0", "Petición de comparación", "Broker/gestor", "D",
    obj({"cartera": CARTERA, "expedientes": {"type": "array", "minItems": 1, "uniqueItems": True, "items": ID},
         "referencia": REFERENCIA, "testigos": {"type": "array", "uniqueItems": True, "items": ID}}),
    producer={"enum": ["BROKER", "GESTOR_TRADING", "GESTOR_TACTICA", "GESTOR_LARGO_PLAZO"]}, consumer={"const": "D"}, con_expediente=False)

ESQUEMAS[("CT-G-05", "0.1.0")] = envoltura(
    "CT-G-05", "0.1.0", "Comparativa", "D", "Broker/gestor",
    obj({"comparacion_id": ID, "cartera": CARTERA, "codigo_d": ID, "decision_global": {"enum": ["INVERTIR", "ABSTENERSE"]},
         "referencia": REFERENCIA,
         "candidatos": {"type": "array", "minItems": 1, "items": obj({
             "expediente_id": ID, "ganador": BOOL, "aspirante": BOOL, "excluido": {"anyOf": [ID, {"type": "null"}]},
             "decision": {"anyOf": [{"enum": ["CLARA", "AJUSTADA"]}, {"type": "null"}]}, "sensible": {"anyOf": [BOOL, {"type": "null"}]},
             "elegido_por_operador": BOOL, "detalle_d": {"anyOf": [{"type": "object"}, {"type": "null"}]}})},
         "testigos": {"type": "array", "uniqueItems": True, "items": ID}, "apartado_mejor": ID_O_NULO, "ganador": ID_O_NULO}),
    producer={"const": "D"}, consumer={"enum": ["BROKER", "GESTOR_TRADING", "GESTOR_TACTICA", "GESTOR_LARGO_PLAZO", "ORQUESTADOR"]},
    con_expediente=False)

ESQUEMAS[("CT-G-06", "0.1.0")] = envoltura(
    "CT-G-06", "0.1.0", "Propuesta de inversión", "Broker/gestor", "E",
    obj({"cartera": CARTERA,
         "entrada": obj({"limite": POS, "ventana_hasta": FH, "instrumento": ID, "activo_base": ID, "via_acceso": TXT,
                         "apalancamiento": {"type": "number", "minimum": 1}, "cantidad": POS, "resto_parcial": {"const": "CANCELAR"}},
                        required=["limite", "ventana_hasta", "instrumento", "activo_base", "via_acceso", "apalancamiento", "cantidad"], extra=True),
         "salida": obj({"condiciones": {"type": "array", "minItems": 1, "items": CONDICION,
                                        "contains": {"properties": {"tipo": {"const": "STOP"}}, "required": ["tipo"]}, "minContains": 1, "maxContains": 1},
                        "fecha": FECHA}),
         "cantidad_e": NUM0, "sobre_ref": obj({"event_id": REF, "hash": HASH}), "comparacion_id": ID}),
    producer={"enum": ["BROKER", "GESTOR_TRADING", "GESTOR_TACTICA", "GESTOR_LARGO_PLAZO"]}, consumer={"const": "E"})

CONTROL = obj({"regla": ID, "resultado": {"enum": ["OK", "REDUCE", "VETA"]}, "valor": {}, "limite": {}}, required=["regla", "resultado"], extra=True)
ESQUEMAS[("CT-G-08", "0.1.0")] = {   # 0.1.0 RETIRADA: envoltura parcial (sin data_refs ni payload); se conserva para leer el histórico
    "$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "https://robot-inversor.local/esquemas/ct-g-08/0.1.0",
    "title": "CT-G-08 · Resultado de control de F",
    "description": "Versión 0.1.0 RETIRADA (T-47). F → Orquestador (G, Broker). Envoltura parcial: sin data_refs ni payload. Solo para leer el histórico.",
    "type": "object",
    "properties": {"event_id": ID, "correlation_id": ID, "expediente_id": ID, "producer": {"const": "F"}, "consumer": {"const": "ORQUESTADOR"},
                   "tipo_mensaje": {"const": "CT-G-08"}, "version_esquema": {"const": "0.1.0"}, "emitido_en": FH, "valid_until": FH,
                   "version_reglas": ID, "propuesta_ref": obj({"expediente_id": ID, "hash": HASH}),
                   "entradas": obj({"solicitud": {"type": "object"}, "cartera": {"type": "object"}, "politica": {"type": "object"}}),
                   "resultado": {"enum": ["APROBADO", "REDUCIDO", "VETADO"]}, "cantidad_aprobada": NUM0,
                   "controles": {"type": "array", "items": CONTROL}},
    "required": ["event_id", "correlation_id", "expediente_id", "producer", "consumer", "tipo_mensaje", "version_esquema", "emitido_en",
                 "valid_until", "version_reglas", "propuesta_ref", "entradas", "resultado", "cantidad_aprobada", "controles"],
    "additionalProperties": False}

ESQUEMAS[("CT-G-09", "0.1.0")] = envoltura(
    "CT-G-09", "0.1.0", "Orden con su protección", "Orquestador (tras E/F y la autorización)", "G",
    obj({"cartera": CARTERA, "instrumento": ID, "activo_base": ID, "via_acceso": TXT, "lado": {"enum": ["COMPRA", "VENTA"]},
         "tipo": {"const": "LIMITE"}, "cantidad": POS, "precio_limite": POS, "valida_hasta": FH,
         "proteccion": obj({"tipo": {"const": "STOP"}, "precio": POS, "solo_reduccion": {"const": True}}),
         "control_f_ref": obj({"event_id": ID, "hash": HASH}), "autorizada_por": {"enum": ["OPERADOR", "MATRIZ_AUTONOMIA"]}}),
    producer={"const": "ORQUESTADOR"}, consumer={"const": "G"})

ESQUEMAS[("CT-G-10", "0.1.0")] = envoltura(
    "CT-G-10", "0.1.0", "Alerta o petición de revisión de posición", "H", "Broker/gestor",
    obj({"posicion_id": ID, "cartera": CARTERA, "estado_posicion": {"enum": ["ABIERTA", "EN_REVISION", "REDUCIENDO", "CERRANDO", "CERRADA"]},
         "tipo": {"enum": ["CIERRE_PREPARADO", "REDUCCION_PREPARADA", "REVISION", "OTRA"]}, "texto": TXT}),
    producer={"const": "H"}, consumer={"enum": ["GESTOR_TRADING", "GESTOR_TACTICA", "GESTOR_LARGO_PLAZO", "OPERADOR"]})

ESQUEMAS[("CT-G-14", "0.1.0")] = {   # 0.1.0 RETIRADA: envoltura propia (contrato/version); se conserva para leer el histórico
    "$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "https://robot-inversor.local/esquemas/ct-g-14/0.1.0",
    "title": "CT-G-14 · Registro de ejecución manual",
    "description": "Versión 0.1.0 (provisional, 0.x). Operador → G. Las reglas RM-01 a RM-10 las aplica validador/manual_g.py. "
                   "Versión RETIRADA (T-47): envoltura propia (contrato/version). Solo para leer el histórico.",
    "type": "object",
    "properties": {"contrato": {"const": "CT-G-14"}, "version": {"const": "0.1.0"}, "event_id": ID, "producer": {"const": "OPERADOR"},
                   "emitido_en": FH, "ejecutado_en": FH, "cartera": CARTERA, "instrumento": ID, "activo_base": ID,
                   "lado": {"enum": ["COMPRA", "VENTA"]}, "cantidad": POS, "precio": POS, "ref_intermediario": ID,
                   "motivo": {"type": "string", "minLength": 3, "maxLength": 500, "pattern": r"\S.*\S|\S{3}"},
                   "vinculo": {"oneOf": [obj({"tipo": {"enum": ["EXPEDIENTE", "POSICION"]}, "id": ID}),
                                         obj({"tipo": {"const": "LIBRE"}, "id": {"type": "null"}})]},
                   "proteccion_ref": ID, "comision_eur": NUM0, "via_acceso": TXT},
    "required": ["contrato", "version", "event_id", "producer", "emitido_en", "ejecutado_en", "cartera", "instrumento", "activo_base",
                 "lado", "cantidad", "precio", "ref_intermediario", "motivo", "vinculo"],
    "additionalProperties": False}

ESQUEMAS[("CT-G-16", "0.1.0")] = envoltura(
    "CT-G-16", "0.1.0", "Aviso al operador", "Orquestador", "Operador",
    obj({"aviso_id": ID, "codigo": {"type": "string", "pattern": r"^O-\d{2}\Z"}, "prioridad": {"enum": ["ALTA", "MEDIA"]},
         "motivo": TXT, "ref": {"anyOf": [{"type": "string"}, {"type": "null"}]},
         "carteras": {"anyOf": [{"type": "array", "uniqueItems": True, "items": CARTERA}, {"type": "null"}]},
         "canal": {"type": "string", "minLength": 1}, "acuse": {"anyOf": [obj({"actor": ID, "ahora": FH}), {"type": "null"}]},
         "reiteraciones": {"type": "integer", "minimum": 0}, "escalado": BOOL}),
    producer={"const": "ORQUESTADOR"}, consumer={"const": "OPERADOR"}, con_expediente=False, con_vigencia=False)

ESQUEMAS[("CT-G-08", "0.2.0")] = envoltura(
    "CT-G-08", "0.2.0", "Resultado de control de F", "F", "Orquestador (G, Broker)",
    obj({"propuesta_ref": obj({"expediente_id": ID, "hash": HASH}),
         "entradas": obj({"solicitud": {"type": "object"}, "cartera": {"type": "object"}, "politica": {"type": "object"}}),
         "cantidad_aprobada": NUM0}),
    producer={"const": "F"}, consumer={"const": "ORQUESTADOR"},
    data_refs={"type": "array", "maxItems": 0},   # F no usa evidencia externa: lo que usa va en payload.entradas
    politica=obj({"version_politica": ID, "resultado": {"enum": ["APROBADO", "REDUCIDO", "VETADO"]}, "motivo": TXT,
                  "controles": {"type": "array", "items": CONTROL}}))

ESQUEMAS[("CT-G-14", "0.2.0")] = {
    **envoltura(
        "CT-G-14", "0.2.0", "Registro de ejecución manual", "Operador", "G",
        obj({"ejecutado_en": FH, "cartera": CARTERA, "instrumento": ID, "activo_base": ID,
             "lado": {"enum": ["COMPRA", "VENTA"]}, "cantidad": POS, "precio": POS, "ref_intermediario": ID,
             "motivo": {"type": "string", "maxLength": 500, "pattern": r"\S[\s\S]*\S[\s\S]*\S"},   # = manual_g.motivo_ok
             "vinculo": {"oneOf": [obj({"tipo": {"enum": ["EXPEDIENTE", "POSICION"]}, "id": ID}),
                                   obj({"tipo": {"const": "LIBRE"}, "id": {"type": "null"}})]},
             "proteccion_ref": ID, "comision_eur": NUM0, "via_acceso": TXT},
            required=["ejecutado_en", "cartera", "instrumento", "activo_base", "lado", "cantidad", "precio", "ref_intermediario", "motivo", "vinculo"]),
        producer={"const": "OPERADOR"}, consumer={"const": "G"}, con_expediente=False, sin_vigencia=True,
        data_refs={"type": "array", "minItems": 1, "maxItems": 2, "uniqueItems": True, "items": ID}),
    # una operación LIBRE no identifica caso; una vinculada, sí (RM-11 comprueba además que es el del vínculo)
    "if": {"properties": {"payload": {"properties": {"vinculo": {"properties": {"tipo": {"const": "LIBRE"}}}}}}},
    "then": {"properties": {"expediente_id": {"type": "null"}, "correlation_id": {"type": "null"}}},
    "else": {"properties": {"expediente_id": ID, "correlation_id": ID}}}
ESQUEMAS[("CT-G-14", "0.2.0")]["description"] += " Las reglas RM-01 a RM-11 las aplica validador/manual_g.py; data_refs = las órdenes del payload."

# Versiones retiradas: su esquema se conserva para leer el histórico (contratos.validar(..., historico=True)); ningún consumidor las acepta
RETIRADAS = {"CT-G-02": [("0.1.0", "ct-g-02_0.1.0.schema.json", "COMPLETA")], "CT-G-08": [("0.1.0", "ct-g-08_0.1.0.schema.json", "PARCIAL")], "CT-G-14": [("0.1.0", "ct-g-14_0.1.0.schema.json", "PROPIA")]}

REGISTRO = [
    ("CT-G-01", "Encargo de análisis", "Broker/gestor → C", "ESQUEMA", "0.1.0", "ct-g-01_0.1.0.schema.json", "COMPLETA"),
    ("CT-G-02", "Sobre común de valoración", "C → verificación, D, Broker", "ESQUEMA", "0.2.0", "ct-g-02_0.2.0.schema.json", "COMPLETA"),
    ("CT-G-03", "Informe del Contradictor", "Contradictor → D, Broker", "ESQUEMA", "0.1.0", "ct-g-03_0.1.0.schema.json", "COMPLETA"),
    ("CT-G-04", "Petición de comparación", "Broker/gestor → D", "ESQUEMA", "0.1.0", "ct-g-04_0.1.0.schema.json", "COMPLETA"),
    ("CT-G-05", "Comparativa", "D → Broker/gestor", "ESQUEMA", "0.1.0", "ct-g-05_0.1.0.schema.json", "COMPLETA"),
    ("CT-G-06", "Propuesta de inversión", "Broker/gestor → E", "ESQUEMA", "0.1.0", "ct-g-06_0.1.0.schema.json", "COMPLETA"),
    ("CT-G-07", "Plan de cartera por libro", "E → F", "PENDIENTE", None, None, "E solo dimensiona una propuesta; el plan por libro es de Fase 2"),
    ("CT-G-08", "Resultado de control", "F → G, Broker", "ESQUEMA", "0.2.0", "ct-g-08_0.2.0.schema.json", "COMPLETA"),
    ("CT-G-09", "Orden con su protección", "E/F → G", "ESQUEMA", "0.1.0", "ct-g-09_0.1.0.schema.json", "COMPLETA"),
    ("CT-G-10", "Alerta o petición de revisión de posición", "H → Broker/gestor", "ESQUEMA", "0.1.0", "ct-g-10_0.1.0.schema.json", "COMPLETA"),
    ("CT-G-11", "Consulta al Broker o al operador", "Cualquiera → Broker", "PENDIENTE", None, None, "sin bloque que la emita en Fase 1"),
    ("CT-G-12", "Seguimiento de encargo", "Bloque → Orquestador", "PENDIENTE", None, None, "hoy el gasto se registra con registrar_gasto, sin mensaje"),
    ("CT-G-13", "Propuesta de cambio y veredicto de validación", "I → J → operador", "PENDIENTE", None, None, "bloques I y J no construidos"),
    ("CT-G-14", "Registro de ejecución manual", "Operador → G", "ESQUEMA", "0.2.0", "ct-g-14_0.2.0.schema.json", "COMPLETA"),
    ("CT-G-15", "Estrategia validada y universo admitido", "J → E, F", "PENDIENTE", None, None, "bloque J no construido"),
    ("CT-G-16", "Aviso al operador", "Orquestador → operador", "ESQUEMA", "0.1.0", "ct-g-16_0.1.0.schema.json", "COMPLETA"),
]


def main():
    for (tipo, version), esq in ESQUEMAS.items():
        (AQUI / f"{tipo.lower()}_{version}.schema.json").write_text(json.dumps(esq, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    reg = []
    for t, n, d, e, v, f, x in REGISTRO:
        c = {"tipo": t, "nombre": n, "de_a": d, "estado": e, "version": v, "esquema": f, "envoltura" if e == "ESQUEMA" else "motivo": x}
        if e == "ESQUEMA":
            c["versiones"] = [{"version": v, "esquema": f, "envoltura": x, "estado": "VIGENTE"}] + \
                             [{"version": rv, "esquema": rf, "envoltura": rx, "estado": "RETIRADA"} for rv, rf, rx in RETIRADAS.get(t, [])]
        reg.append(c)
    (AQUI / "registro_contratos.json").write_text(json.dumps({"version_registro": "REG-0.2.0", "contratos": reg}, ensure_ascii=False, indent=2) + "\n",
                                                  encoding="utf-8")
    print(f"{len(ESQUEMAS)} esquemas y el registro de {len(REGISTRO)} contratos")


if __name__ == "__main__":
    main()
