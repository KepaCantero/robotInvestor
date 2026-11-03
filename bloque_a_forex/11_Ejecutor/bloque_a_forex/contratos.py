"""Contratos CT-01 a CT-25 y CT-06T (sección 6 y Anexo B del Documento 0 del Bloque A Forex V1.1).

V1.1 (03/11/2026): CT-23 consulta al Broker (Coordinador ↔ Broker, en ambos sentidos), CT-24 encargo de seguimiento de
opción (Broker → Coordinador, retorno por el mismo contrato) y CT-25 solicitud y provisión de credenciales (Coordinador ↔
Broker; en origen, el Buscador puede enviar sus solicitudes directamente al Coordinador). Ningún mensaje transporta el valor de
una credencial: solo su alias (`credencial_ref`) y su estado.

- `crear_mensaje` añade los campos comunes (msg_id, contrato, version_contrato, emisor, receptor,
  run_id/query_id, timestamp, presupuesto/consumo, estado…).
- `validar_mensaje` aplica R2 (canales cerrados), R8 (credenciales y datos personales) y los campos
  mínimos del Anexo B.
- `Buzon` da acuse e idempotencia (el mismo msg_id se procesa una sola vez).
- `sanear_contenido_externo` aplica R9: el contenido externo es dato; las instrucciones incrustadas se
  neutralizan y se devuelven como hallazgos para registrarlas como incidencia.
- `ESQUEMAS`: esquemas JSON mínimos de las respuestas de cada agente (validación con jsonschema).
"""
from __future__ import annotations

import copy
import json
import re
import threading
from typing import Any, Dict, List, Optional, Tuple

VERSION_CONTRATO = "FX-1.1"
ESTADOS = ("COMPLETO", "PARCIAL", "SIN_RESULTADO", "RECHAZADO")
# Analistas de segmento (Documento 0 Forex, 4.2): AG-03..AG-08; Analistas transversales: AG-09 (BCM) y AG-21 (PFV)
ANALISTAS = {"AG-03", "AG-04", "AG-05", "AG-06", "AG-07", "AG-08"}
TRANSVERSALES = {"AG-09", "AG-21"}
ANALISTAS_TODOS = ANALISTAS | TRANSVERSALES
TODOS = {f"AG-{i:02d}" for i in range(1, 22)}
AGENTE_SEGMENTO = {"G10N": "AG-03", "G10M": "AG-04", "EMAS": "AG-05", "EMLA": "AG-06", "EMEA": "AG-07", "ESTR": "AG-08"}
SEGMENTO_AGENTE = {v: k for k, v in AGENTE_SEGMENTO.items()}
AGENTE_CAPA = {"BCM": "AG-09", "PFV": "AG-21"}

# Canales: contrato -> lista de (emisores, receptores); «↔» se modela con ambas direcciones.
def _par(a, b):
    return [(set(a), set(b)), (set(b), set(a))]


CANALES: Dict[str, List[Tuple[set, set]]] = {
    "CT-01": [({"BROKER"}, {"AG-01"})],
    "CT-02": [({"AG-01"}, {"BROKER"})],
    "CT-03": _par({"BROKER"}, {"AG-01"}),
    "CT-04": [({"BROKER"}, {"AG-01"})],
    "CT-05": _par({"AG-01"}, {"AG-02"}),
    "CT-06": _par({"AG-02"}, ANALISTAS),
    "CT-06T": _par({"AG-02"}, TRANSVERSALES),
    "CT-07": _par({"AG-02", "AG-10"} | ANALISTAS_TODOS, {"AG-16"}),
    "CT-08": _par({"AG-02", "AG-10", "AG-11"} | ANALISTAS_TODOS, {"AG-14"}),
    "CT-09": _par({"AG-02", "AG-10", "AG-20", "AG-18", "AG-19", "AG-14", "AG-15", "AG-16"} | ANALISTAS_TODOS, {"AG-13"}),
    "CT-10": _par({"AG-18", "AG-19", "AG-20"}, {"AG-13"}),
    "CT-11": _par(ANALISTAS_TODOS | {"AG-16", "AG-14", "AG-15", "AG-10", "AG-11"}, {"AG-12"}),
    "CT-12": _par({"AG-02"}, {"AG-10"}),
    "CT-13": _par({"AG-02"}, {"AG-11"}),
    "CT-14": _par({"AG-02"}, {"AG-18"}),
    "CT-15": _par({"AG-02"}, {"AG-17"}),
    "CT-16": [({"AG-01"}, {"AG-18"})],
    "CT-17": _par({"AG-18"}, {"AG-19"}),
    "CT-18": [({"AG-18"}, TODOS)],
    "CT-19": [({"AG-20"}, {"AG-01", "AG-02", "AG-10", "AG-16", "AG-18"} | ANALISTAS_TODOS)],
    "CT-20": _par({"AG-13"}, {"AG-15"}),
    "CT-21": [({"AG-14", "AG-15", "AG-16"}, {"AG-18"})],
    "CT-22": [({"AG-01"}, {"AG-20"})],
    "CT-23": _par({"AG-01"}, {"BROKER"}),
    "CT-24": _par({"BROKER"}, {"AG-01"}),
    "CT-25": _par({"AG-01"}, {"BROKER"}) + [({"AG-16", "AG-02"}, {"AG-01"})],
}

CAMPOS_MINIMOS = {
    "CT-01": ["tipo", "alcance", "horizontes", "prioridad"],
    "CT-02": ["entregables", "resumen", "estado_g3"],
    "CT-03": ["pregunta"],
    "CT-05": ["tipo", "alcance", "nivel_por_segmento", "presupuesto_por_segmento", "memoria", "delta_gc0", "fecha_objetivo"],
    "CT-06": ["segmento", "fase", "nivel", "opciones_vigentes", "lecciones"],
    "CT-06T": ["capa", "nivel", "presupuesto", "segmentos_destino", "foco"],
    "CT-07": ["pregunta", "objetivo", "segmento", "horizonte", "profundidad", "max_fuentes", "fecha_limite_informacion"],
    "CT-08": ["pregunta", "objetivo", "segmento", "horizonte", "profundidad", "max_fuentes", "fecha_limite_informacion"],
    "CT-09": ["operacion", "perfil", "modo", "plan", "datos", "parametros", "semilla", "fecha_corte"],
    "CT-10": ["artefacto_id", "motivo"],
    "CT-11": ["piezas"],
    "CT-12": ["encargos"],
    "CT-13": ["peticiones"],
    "CT-14": ["paquete_sintesis"],
    "CT-15": ["paquete_sintesis"],
    "CT-23": ["cns_id", "sentido", "tipo", "modo", "plazo_respuesta"],
    "CT-24": ["accion", "opp_id"],
    "CT-25": ["crd_id", "servicio", "herramienta", "uso_previsto", "solicitante", "impacto_si_falta"],
}
CAMPOS_RETORNO = {"CT-03": ["clase_consulta", "ruta", "respuesta", "referencias", "confianza"],
                  "CT-23": ["cns_id", "estado"], "CT-24": ["seg_id", "estado"], "CT-25": ["crd_id", "estado"]}

RE_SECRETO = re.compile(
    r"(?i)(\"(api[_-]?key|apikey|secret|client_secret|password|passwd|contraseña|access[_-]?token|bearer)\"\s*:\s*\"[^\"]+\")"
    r"|(sk-[A-Za-z0-9_-]{20,})|(AKIA[0-9A-Z]{16})|(-----BEGIN [A-Z ]*PRIVATE KEY-----)|(Bearer\s+[A-Za-z0-9._-]{20,})"
    r"|(?-i:(\bES\d{22}\b)|(\b\d{8}-?[A-HJ-NP-TV-Z]\b))"
    # R8 V1.1: el valor de una credencial nunca viaja en un mensaje (solo `credencial_ref` y estado)
    r"|(\"(credencial(?:_valor)?|valor_credencial|clave(?:_api)?|api_token|token|secreto)\"\s*:\s*\"[^\"]{6,}\")")

# R9: patrones de instrucciones incrustadas en contenido externo (español e inglés)
PATRONES_INYECCION = [
    r"ignora(?:d)?\s+(?:todas\s+)?(?:las\s+)?instrucciones(?:\s+anteriores)?",
    r"olvida\s+(?:tus|las)\s+(?:instrucciones|reglas)",
    r"ignore\s+(?:all\s+)?(?:previous|prior|above)\s+instructions",
    r"disregard\s+(?:the\s+)?(?:previous|system)\s+(?:instructions|prompt)",
    r"(?:nuevo|new)\s+system\s+prompt",
    r"act[uú]a\s+como\s+si",
    r"(?:asigna|pon|sube)\s+(?:una\s+)?(?:puntuaci[oó]n|nota|[AETRK]{1,2})\s+(?:de\s+|a\s+)?\d{2,3}",
    r"(?:cambia|modifica)\s+(?:el|los)\s+(?:umbral|umbrales|par[aá]metros?)",
    r"(?:env[ií]a|reenv[ií]a|manda)\s+(?:esto|el\s+informe|los\s+datos)\s+a",
    r"you\s+are\s+now",
    r"<\s*/?\s*system\s*>",
]
RE_INYECCION = re.compile("|".join(f"(?:{p})" for p in PATRONES_INYECCION), re.IGNORECASE)
MARCA_RETIRADA = "[INSTRUCCION_INCRUSTADA_RETIRADA]"


class CanalNoPrevisto(PermissionError):
    pass


class DatosSensibles(PermissionError):
    pass


class MensajeInvalido(ValueError):
    pass


def sanear_contenido_externo(texto: str, origen: str = "") -> Tuple[str, List[Dict]]:
    """Neutraliza instrucciones incrustadas (R9). Devuelve el texto saneado y los hallazgos."""
    if not isinstance(texto, str) or not texto:
        return texto, []
    hallazgos = []
    def _sust(m):
        hallazgos.append({"origen": origen, "fragmento": m.group(0)[:80], "tipo": "INSTRUCCION_INCRUSTADA"})
        return MARCA_RETIRADA
    limpio = RE_INYECCION.sub(_sust, texto)
    return limpio, hallazgos


def sanear_estructura(obj: Any, origen: str = "") -> Tuple[Any, List[Dict]]:
    """Aplica `sanear_contenido_externo` a todas las cadenas de una estructura JSON."""
    hallazgos: List[Dict] = []
    def rec(o, ruta):
        if isinstance(o, str):
            t, h = sanear_contenido_externo(o, f"{origen}{ruta}")
            hallazgos.extend(h)
            return t
        if isinstance(o, list):
            return [rec(x, f"{ruta}[{i}]") for i, x in enumerate(o)]
        if isinstance(o, dict):
            return {k: rec(v, f"{ruta}.{k}") for k, v in o.items()}
        return o
    return rec(copy.deepcopy(obj), ""), hallazgos


def contiene_credenciales(obj: Any) -> List[str]:
    volcado = json.dumps(obj, ensure_ascii=False, default=str)
    return [m.group(0)[:6] + "…" for m in RE_SECRETO.finditer(volcado)]


def canal_permitido(contrato: str, emisor: str, receptor: str) -> bool:
    for em, rc in CANALES.get(contrato, []):
        if emisor in em and receptor in rc:
            return True
    return False


class Mensajeria:
    """Crea y valida mensajes; mantiene el registro de msg_id procesados (idempotencia)."""

    def __init__(self, almacen) -> None:
        self.almacen = almacen
        self._lock = threading.Lock()
        self._procesados: Dict[str, Dict] = {}
        self.registro: List[Dict] = []   # traza de mensajes (contrato, emisor, receptor, msg_id)

    def crear(self, contrato: str, emisor: str, receptor: str, cuerpo: Dict, *, run_id: Optional[str] = None,
              query_id: Optional[str] = None, presupuesto: Optional[Dict] = None, consumo: Optional[Dict] = None,
              estado: Optional[str] = None, tipo_mensaje: str = "ENCARGO") -> Dict:
        msg = {"msg_id": self.almacen.nuevo_id("MSG", ancho=6), "contrato": contrato, "version_contrato": VERSION_CONTRATO,
               "emisor": emisor, "receptor": receptor, "timestamp": self.almacen.reloj.ahora(), "tipo_mensaje": tipo_mensaje}
        if run_id:
            msg["run_id"] = run_id
        if query_id:
            msg["query_id"] = query_id
        if tipo_mensaje == "ENCARGO":
            msg["presupuesto"] = presupuesto or {}
        else:
            msg["consumo"] = consumo or {}
            msg["estado"] = estado or "COMPLETO"
            msg.setdefault("limitaciones", [])
            msg.setdefault("autoevaluacion", "")
        msg.update(copy.deepcopy(cuerpo))
        self.validar(msg)
        with self._lock:
            self.registro.append({k: msg.get(k) for k in ("msg_id", "contrato", "emisor", "receptor", "tipo_mensaje")})
        return msg

    def validar(self, msg: Dict) -> None:
        for c in ("msg_id", "contrato", "version_contrato", "emisor", "receptor", "timestamp"):
            if not msg.get(c):
                raise MensajeInvalido(f"Falta el campo común {c}")
        if msg["contrato"] not in CANALES:
            self.almacen.incidencia("CANAL_NO_PREVISTO", f"Contrato inexistente {msg['contrato']}", msg.get("emisor", ""))
            raise CanalNoPrevisto(f"Contrato inexistente {msg['contrato']}")
        if not canal_permitido(msg["contrato"], msg["emisor"], msg["receptor"]):
            self.almacen.incidencia("CANAL_NO_PREVISTO",
                                    f"{msg['emisor']} → {msg['receptor']} por {msg['contrato']} no previsto (R2)", msg["emisor"])
            raise CanalNoPrevisto(f"{msg['emisor']} → {msg['receptor']} por {msg['contrato']} no previsto (R2)")
        cred = contiene_credenciales({k: v for k, v in msg.items() if k not in ("msg_id", "timestamp")})
        if cred:
            campos = [k for k, v in msg.items() if contiene_credenciales(v)]
            self.almacen.incidencia("SEGURIDAD", "Mensaje con credenciales o datos personales rechazado íntegro (R8)",
                                    msg["emisor"], campo_afectado=campos)
            raise DatosSensibles(f"Mensaje {msg['msg_id']} con datos protegidos en {campos}")
        if not msg.get("run_id") and not msg.get("query_id") and msg["contrato"] not in ("CT-01", "CT-03", "CT-04", "CT-18", "CT-21",
                                                                                          "CT-23", "CT-24", "CT-25"):
            raise MensajeInvalido("Falta run_id o query_id")
        tipo = msg.get("tipo_mensaje", "ENCARGO")
        req = CAMPOS_MINIMOS.get(msg["contrato"], []) if tipo == "ENCARGO" else CAMPOS_RETORNO.get(msg["contrato"], [])
        falta = [c for c in req if c not in msg]
        if falta:
            raise MensajeInvalido(f"{msg['contrato']}: faltan campos mínimos {falta}")
        if tipo != "ENCARGO" and msg.get("estado") not in ESTADOS:
            raise MensajeInvalido(f"Estado de retorno no válido {msg.get('estado')!r}")

    def procesar_una_vez(self, msg: Dict, funcion) -> Tuple[Dict, bool]:
        """Idempotencia: devuelve (respuesta, repetido). El mismo msg_id no se reprocesa."""
        with self._lock:
            if msg["msg_id"] in self._procesados:
                return copy.deepcopy(self._procesados[msg["msg_id"]]), True
        r = funcion(msg)
        with self._lock:
            self._procesados[msg["msg_id"]] = copy.deepcopy(r)
        return r, False

    def acuse(self, msg: Dict, asignado: str, **extra) -> Dict:
        return {"acuse_de": msg["msg_id"], "asignado": asignado, "timestamp": self.almacen.reloj.ahora(), **extra}


# ============================================================================================
# Esquemas JSON mínimos de las respuestas de los agentes
# ============================================================================================
DIM = {"anyOf": [{"type": "integer", "minimum": 0, "maximum": 100, "multipleOf": 10}, {"enum": ["NA", "NE"]}]}
DIMS = {"type": "object", "additionalProperties": DIM}
TIPOS_OPCION = ["PAR", "CRUCE", "CESTA", "BLOQUE", "ESTRATEGIA", "VOLATILIDAD", "REGIMEN"]   # 2.4 Forex
TXT = {"type": "string", "minLength": 1}
LISTA_TXT = {"type": "array", "items": {"type": "string"}}
LISTA_TXT_MIN1 = {"type": "array", "minItems": 1, "items": TXT}
ISO = {"type": "string", "pattern": "^[A-Z]{3}$"}
AMBITO = {"type": "object", "required": ["incluye", "excluye"], "properties": {"incluye": TXT, "excluye": TXT}}
# En el ejecutor el indicador de seguimiento necesita un código HT-01 del universo (para medir y resolver F4)
INDICADOR = {"type": "object", "required": ["nombre", "simbolo"],
             "properties": {"nombre": TXT, "simbolo": TXT, "fuente": {"type": "string"}, "tipo": {"type": "string"}}}
COMPOSICION = {"type": "array", "items": {"type": "object", "required": ["divisa", "peso", "lado"],
                                          "properties": {"divisa": ISO, "peso": {"type": "number", "exclusiveMinimum": 0, "maximum": 1},
                                                         "lado": {"enum": ["LARGO", "CORTO"]}}}}
CONVERTIBILIDAD = {"type": "object", "required": ["convertible", "ndf", "controles_capitales", "profundidad", "nota"],
                   "properties": {"convertible": {"type": "boolean"}, "ndf": {"type": "boolean"}, "controles_capitales": {"type": "boolean"},
                                  "impiden_exposicion": {"type": "boolean"}, "exposicion_alternativa": {"type": "boolean"},
                                  "profundidad": {"enum": ["muy alta", "alta", "media", "baja"]}, "nota": TXT}}
DIMS_A_FX = {"type": "object", "properties": {k: DIM for k in ("asimetria", "valoracion", "carry", "catalizadores",
                                                               "momento_posicionamiento", "convertibilidad")},
             "additionalProperties": False}

# Ficha de una finalista (CT-06, informe de segmento): un ámbito cambiario, nunca un instrumento (2.4–2.5, R21)
FINALISTA = {
    "type": "object",
    "required": ["nombre", "nombre_llano", "tipo_opcion", "par", "composicion", "direccion", "divisa_financiacion", "ambito",
                 "indicador_seguimiento", "convertibilidad", "tesis", "mecanismo", "valoracion", "catalizadores", "riesgos",
                 "invalidacion", "horizontes_aplicables", "dimensiones", "premortem", "afirmaciones", "lo_que_no_sabemos",
                 "consideraciones_implementacion", "metricas_clave", "preguntas_para_B"],
    "properties": {
        "nombre": TXT, "nombre_llano": {"type": "string", "minLength": 3, "maxLength": 70},
        "sube_baja_llano": {"type": "string", "maxLength": 160},
        "tipo_opcion": {"enum": TIPOS_OPCION},
        "par": {"anyOf": [{"type": "string", "pattern": "^[A-Z]{3}/[A-Z]{3}$"}, {"type": "null"}]},
        "composicion": COMPOSICION,
        "direccion": {"enum": ["ALCISTA_BASE", "BAJISTA_BASE", None]},
        "vista_volatilidad": {"type": "object", "required": ["sentido", "plazo"],
                              "properties": {"sentido": {"enum": ["ALZA", "BAJA"]}, "plazo": TXT}},
        "divisa_financiacion": {"anyOf": [ISO, {"type": "null"}]},
        "regimen_cambiario_divisa": {"enum": ["LIBRE_FLOTACION", "FLOTACION_ADMINISTRADA", "BANDA", "TIPO_FIJO", "CAJA_CONVERSION", "CONTROLES"]},
        "motivo_asignacion_segmento": TXT,
        "ambito": AMBITO, "indicador_seguimiento": INDICADOR, "convertibilidad": CONVERTIBILIDAD,
        "tesis": TXT, "mecanismo": TXT, "valoracion": TXT,
        "catalizadores": {"type": "array", "items": {"type": "object", "required": ["evento", "fecha"],
                                                     "properties": {"evento": TXT, "fecha": {"type": "string",
                                                     "pattern": r"^[0-9]{4}-[0-9]{2}(-[0-9]{2})?$|^[0-9]{4}-T[1-4]$|^[0-9]{4}-S[12]$"}}}},
        "riesgos": {"type": "array", "minItems": 1, "items": TXT},
        "invalidacion": {"type": "array", "minItems": 1, "items": TXT},
        "invalidacion_cuantitativa": {"type": "array", "items": {"type": "object", "required": ["simbolo", "umbral", "direccion"],
                                      "properties": {"simbolo": TXT, "umbral": {"type": "number"},
                                                     "direccion": {"enum": ["por_debajo", "por_encima"]}}}},
        "horizontes_aplicables": {"type": "array", "minItems": 1, "items": {"enum": ["H1", "H2", "H3", "H4", "H5"]}},
        "naturaleza_inversion": {"enum": ["TACTICA", "CICLICA", "PRIMA_RIESGO", "VALORACION", "ESTRUCTURAL"]},
        "ambito_h5": {"enum": ["EQUILIBRIO_LARGO_PLAZO", "REGIMEN_CAMBIARIO", "SISTEMA_MONETARIO_INTERNACIONAL"]},
        "justificacion_horizonte": {"type": ["string", "null"]},
        "dimensiones": {"type": "object", "required": ["T", "E", "M", "A", "P"],
                        "properties": {"T": {"anyOf": [DIMS, {"const": "NA"}]}, "E": DIMS, "M": DIMS, "A": DIMS_A_FX, "P": DIMS}},
        "segunda_pasada": {"type": "object"},
        "saturacion_narrativa": {"type": "boolean"},
        "premortem": TXT,
        "afirmaciones": {"type": "array", "minItems": 1, "items": {"type": "object", "required": ["afirmacion", "fuente", "direccion"],
                         "properties": {"afirmacion": TXT, "fuente": TXT,
                                        "direccion": {"enum": ["favorable", "contraria", "neutra", "ambigua"]}}}},
        "lo_que_no_sabemos": {"type": "array", "minItems": 1, "items": TXT},
        "liquidez": {"enum": ["alta", "media", "baja"]},
        "consideraciones_implementacion": LISTA_TXT_MIN1, "metricas_clave": LISTA_TXT_MIN1, "preguntas_para_B": LISTA_TXT_MIN1,
        "discrepancia_material": {"type": "boolean"},
        "tendencia": {"type": "object", "required": ["nombre_canonico"]},
        "peticiones_conocimiento": {"type": "array"},
    },
    # Frontera con el Bloque B (R21): el Bloque A Forex no elige instrumento, proveedor, coste, apalancamiento, tamaño ni entrada
    "not": {"anyOf": [{"required": [k]} for k in ("instrumento", "vehiculos_genericos", "apalancamiento", "tamano_posicion",
                                                  "nivel_entrada", "proveedor", "ejemplos_ilustrativos")]},
}
REVISION = {"type": "array", "items": {"type": "object", "required": ["opp_id", "invalidacion_activada", "recomendacion"],
            "properties": {"opp_id": TXT, "invalidacion_activada": {"type": "boolean"},
                           "recomendacion": {"enum": ["MANTENER", "REVISAR", "CERRAR"]}}}}
ESTADO_RET = {"enum": list(ESTADOS)}
SENALES_SEGMENTO = {"type": "object", "additionalProperties": {"type": "string"}}

ESQUEMAS: Dict[str, Dict] = {
    "INFORME_SEGMENTO": {
        "type": "object",
        "required": ["segmento", "estado", "regimen_segmento", "revision_vigentes", "cribado", "finalistas", "lagunas", "autoevaluacion"],
        "properties": {"segmento": TXT, "estado": ESTADO_RET,
                       "regimen_segmento": {"type": "object", "required": ["diagnostico"]},
                       "revision_vigentes": REVISION,
                       "cribado": {"type": "array", "items": {"type": "object", "required": ["candidata", "paso_gc1", "motivo"]}},
                       "finalistas": {"type": "array", "maxItems": 5, "items": FINALISTA},
                       "descartadas_relevantes": {"type": "array"}, "lagunas": LISTA_TXT, "autoevaluacion": {"type": "string"}},
    },
    "REVISION_VIGENTES": {
        "type": "object", "required": ["segmento", "estado", "regimen_segmento", "revision_vigentes", "autoevaluacion"],
        "properties": {"segmento": TXT, "estado": ESTADO_RET, "regimen_segmento": {"type": "object", "required": ["diagnostico"]},
                       "revision_vigentes": REVISION, "exploratorias": {"type": "array", "maxItems": 2, "items": FINALISTA}},
    },
    "RESPUESTA_OBJECIONES": {
        "type": "object", "required": ["respuestas"],
        "properties": {"respuestas": {"type": "array", "items": {"type": "object", "required": ["objecion_id", "respuesta", "resuelta"],
                       "properties": {"objecion_id": TXT, "respuesta": {"type": "string"}, "resuelta": {"type": "boolean"}}}}},
    },
    "INFORME_BCM": {
        "type": "object",
        "required": ["regimen_global", "bancos_centrales", "diferenciales", "calendario", "riesgos_intervencion", "senales_por_segmento", "lagunas"],
        "properties": {"regimen_global": {"type": "object", "required": ["dolar", "riesgo", "diagnostico"],
                                          "properties": {"dolar": {"enum": ["fuerte", "neutro", "debil"]},
                                                         "riesgo": {"enum": ["apetito", "neutro", "aversion"]}, "diagnostico": TXT}},
                       "bancos_centrales": {"type": "array", "items": {"type": "object",
                           "required": ["banco", "tipo_actual", "senda_descontada", "sesgo", "proxima_reunion", "sorpresa_reciente"]}},
                       "diferenciales": {"type": "array"}, "calendario": {"type": "array"}, "riesgos_intervencion": LISTA_TXT,
                       "senales_por_segmento": SENALES_SEGMENTO, "lagunas": LISTA_TXT},
    },
    "INFORME_PFV": {
        "type": "object",
        "required": ["posicionamiento", "flujos", "volatilidad", "crowding_estrategias", "base_cruzada", "senales_por_segmento", "lagunas"],
        "properties": {"posicionamiento": {"type": "array", "items": {"type": "object",
                           "required": ["divisa", "neto_cftc", "percentil_historico", "cambio_semanal"]}},
                       "flujos": LISTA_TXT, "volatilidad": {"type": "array", "items": {"type": "object",
                           "required": ["par", "iv_1m", "rv_1m", "rr_25d", "percentil"]}},
                       "regimen_volatilidad": {"enum": ["baja", "media", "alta"]},
                       "crowding_estrategias": {"type": "array"}, "base_cruzada": {"type": "array"},
                       "senales_por_segmento": SENALES_SEGMENTO, "lagunas": LISTA_TXT},
    },
    "PROSPECTIVA": {
        "type": "object", "required": ["resultados", "autoevaluacion"],
        "properties": {"resultados": {"type": "array", "items": {"type": "object", "required": ["ref", "pronosticos", "escenarios"],
            "properties": {"ref": TXT, "escenarios": {"type": "object"}, "hitos": {"type": "array"},
                           "indicadores_adelantados": {"type": "array"}, "invalidacion": {"type": "array"},
                           "pronosticos": {"type": "array", "items": {"type": "object",
                               "required": ["horizonte", "vista", "prob_interna", "afirmacion", "escenario_asociado"],
                               "properties": {"horizonte": {"enum": ["H1", "H2", "H3", "H4"]},
                                              "vista": {"enum": ["alcista", "bajista", "lateral", "relativa_favorable", "relativa_desfavorable"]},
                                              "prob_interna": {"type": "number", "minimum": 0.05, "maximum": 0.95},
                                              "afirmacion": TXT, "escenario_asociado": {"enum": ["BASE", "FAVORABLE", "ADVERSO"]},
                                              "metodo": {"type": "string"}}}}}}}},
    },
    "REFUTACION": {
        "type": "object", "required": ["resultados", "autoevaluacion"],
        "properties": {"resultados": {"type": "array", "items": {"type": "object", "required": ["ref", "objeciones", "veredicto_global"],
            "properties": {"ref": TXT, "veredicto_global": {"enum": ["tesis robusta", "tesis frágil", "tesis refutada"]},
                           "objeciones": {"type": "array", "items": {"type": "object",
                               "required": ["id", "tipo", "fuerza", "argumento", "que_la_resolveria"],
                               "properties": {"fuerza": {"enum": ["fuerte", "moderada", "debil"]}}}}}}}},
    },
    "CURACION": {
        "type": "object", "required": ["piezas"],
        "properties": {"piezas": {"type": "array", "items": {"type": "object", "required": ["indice", "tipo_afirmacion", "nivel_confianza"],
            "properties": {"indice": {"type": "integer"},
                           "tipo_afirmacion": {"enum": ["HECHO", "DATO", "ANALISIS", "OPINION", "PREVISION", "RUMOR", "PRONOSTICO_FUENTE"]},
                           "nivel_confianza": {"enum": ["establecido", "probable", "especulativo", "en disputa"]},
                           "alertas": LISTA_TXT}}}},
    },
    "INTEGRACION": {
        "type": "object", "required": ["regimen_macro", "factores_dominantes", "lectura_conjunto", "preguntas_sugeridas", "limitaciones"],
        "properties": {"regimen_macro": {"type": "string", "minLength": 10}, "factores_dominantes": {"type": "array"},
                       "contradicciones": {"type": "array", "items": {"type": "object", "required": ["divisa", "justificacion_contradiccion"]}},
                       "lectura_divisa_base": {"type": "string", "maxLength": 200},
                       "lectura_conjunto": TXT, "preguntas_sugeridas": LISTA_TXT, "limitaciones": LISTA_TXT,
                       "cambios_vs_anterior": {"type": "string"}},
    },
    "REDACCION": {
        "type": "object", "required": ["frases_30s", "tarjetas", "motivos_llanos", "glosario", "frase_historial"],
        "properties": {"frases_30s": {"type": "array", "minItems": 3, "maxItems": 3, "items": TXT},
                       "tarjetas": {"type": "array", "items": {"type": "object", "required": ["opp_id", "por_que_llano", "que_puede_salir_mal_llano"],
                                    "properties": {"por_que_llano": {"type": "string", "maxLength": 160},
                                                   "que_puede_salir_mal_llano": {"type": "string", "maxLength": 200},
                                                   "sube_baja_llano": {"type": "string", "maxLength": 160}}}},
                       "motivos_llanos": {"type": "object"},
                       "glosario": {"type": "array", "maxItems": 5, "items": {"type": "object", "required": ["termino", "definicion"]}},
                       "frase_historial": TXT},
    },
    "CONSULTA": {
        "type": "object", "required": ["clase_consulta", "ruta", "respuesta", "referencias", "confianza", "tema_normalizado"],
        "properties": {"clase_consulta": {"enum": ["ACLARACION", "DATO", "METODO", "CONTRASTE", "PROFUNDIZACION", "ESTADO"]},
                       "ruta": {"enum": ["N0", "ANALITICA"]}, "respuesta": TXT, "referencias": LISTA_TXT,
                       "confianza": {"enum": ["establecido", "probable", "especulativo", "en disputa"]},
                       "tema_normalizado": TXT, "escalado": {"type": ["object", "null"]}},
    },
    "DICTAMEN_G3": {
        "type": "object", "required": ["dictamen", "motivo"],
        "properties": {"dictamen": {"enum": ["APTO_CON_ADVERTENCIAS", "BLOQUEADO"]}, "motivo": TXT,
                       "condiciones_para_apto": LISTA_TXT, "advertencias": LISTA_TXT},
    },
    "AUDITORIA": {
        "type": "object", "required": ["hallazgos", "resumen"],
        "properties": {"hallazgos": {"type": "array", "items": {"type": "object", "required": ["regla", "descripcion", "severidad"],
                       "properties": {"severidad": {"enum": ["Crítica", "Material", "Operativa", "Menor"]}}}}, "resumen": TXT},
    },
    "APRENDIZAJE": {
        "type": "object", "required": ["resumen", "lecciones"],
        "properties": {"resumen": TXT, "lecciones": {"type": "array", "items": {"type": "object",
                       "required": ["tipo", "observacion", "recomendacion", "fuerza"],
                       "properties": {"fuerza": {"enum": ["anecdotica", "recurrente", "estadistica"]}}}}},
    },
    "BUSQUEDA": {
        "type": "object", "required": ["referencias", "sintesis", "lagunas"],
        "properties": {"referencias": {"type": "array", "items": {"type": "object", "required": ["ref_id"]}},
                       "sintesis": {"type": "string"}, "contradicciones": {"type": "array"}, "lagunas": LISTA_TXT},
    },
    "PLAN_MOTOR": {
        "type": "object", "required": ["ficha_id", "parametros", "justificacion"],
        "properties": {"ficha_id": TXT, "parametros": {"type": "object"}, "justificacion": TXT},
    },
}
