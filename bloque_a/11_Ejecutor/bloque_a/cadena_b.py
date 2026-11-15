"""T-142 · Cadena de encargos A → B (Fase 6), en el papel del Broker y sin modelo.

El Bloque A no se comunica con el Bloque B (Documento 0 del Bloque A, 2.2 y R4): su paquete de oportunidades lleva, por
opción, un `paquete_para_bloque_B` (Anexo B) que el Broker reenvía si decide continuar. Este módulo hace lo que hace el
Broker con ese encargo, en código determinista:

- `opciones_enviables`: las opciones cuyo siguiente paso sugerido es `ENVIAR_A_BLOQUE_B` (7.8); la decisión es del
  Broker, este filtro es su política en la cadena simulada.
- `construir_peticion`: la petición CT-B-01 (`peticion`, Anexo B.1 del Documento 0 del Bloque B) a partir de una opción
  del paquete. El `paquete_para_bloque_B` va tal cual (validado antes contra el esquema del Bloque A, `entrada_bloque_B`)
  y, como extensión `x_`, con la clave del ámbito del Bloque B. Ningún campo inventado: lo que el Bloque A no da lleva
  el valor que el Anexo B.1 del Bloque B prevé (configuración `cadena_b.peticion`) o va vacío.
- `clave_universo_b`: la correspondencia de ámbitos A → B `[PROPUESTO]` (INC-T142-01), en la configuración
  (`cadena_b.correspondencia_ambitos`, por símbolo del indicador de seguimiento). **Falla cerrado**: sin
  correspondencia no hay petición; el Broker no inventa la clave del universo del Bloque B.
- `ct04_desde_respuesta_b`: la vuelta. El Documento 0 del Bloque A no tiene canal para el resultado del Bloque B; prevé
  que el Broker comunique por CT-04 la decisión `ENVIADA_A_BLOQUE_B` y, si quiere, un `resultado_comunicado` en texto
  (7.7 y Anexo B). Se construye ese CT-04 con los identificadores que devuelve el Bloque B (INC-T142-01).

No importa nada del Bloque B: su respuesta llega como datos (el JSON de su línea de comandos)."""
from __future__ import annotations

import copy
import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

import jsonschema

from .configuracion import buscar_versionado, ruta
from .contratos import contiene_credenciales, secretos_en_texto

ORIGEN_BLOQUE_A = "BLOQUE_A"
SIGUIENTE_PASO_ENVIO = "ENVIAR_A_BLOQUE_B"
DECISION_ENVIADA = "ENVIADA_A_BLOQUE_B"
CLAVE_EXTENSION_B = "x_clave_universo"   # extensión que lee el ejecutor del Bloque B (su README, 3; peticion_redes_bloque_a.json)
# T-147 (QA r01 de T-142, H-03): los valores que el Anexo B.1 del Documento 0 del Bloque B admite en los campos de la
# petición que salen de la configuración (`cadena_b.peticion`): `nivel` «N1|N2|N3|PERS|AUTO», `prioridad`
# «ALTA|NORMAL|BAJA» y el único perfil de invertibilidad que nombra, «MINORISTA_UE_DEFECTO». Son del contrato, no
# números: `tests/test_t147.py` comprueba que coinciden con el bloque ```json de B.1. `idioma_usuario` es una etiqueta de
# idioma como la del ejemplo de B.1 («es-ES»): dos o tres letras y, si acaso, la región en mayúsculas.
ENUMERACIONES_B1: dict[str, tuple[str, ...]] = {"nivel": ("N1", "N2", "N3", "PERS", "AUTO"),
                                                "prioridad": ("ALTA", "NORMAL", "BAJA"),
                                                "perfil_invertibilidad": ("MINORISTA_UE_DEFECTO",)}
RE_IDIOMA = re.compile(r"[a-z]{2,3}(?:-[A-Z]{2})?")
RE_SIN_ESPACIOS = re.compile(r"\S+")   # una clave o un símbolo de la tabla de correspondencia: sin espacios
# T-149 (QA r01 de T-147, H-02 de T-142): el Broker solo recibe el paquete en la entrega CT-02, que exige un dictamen G3
# favorable (Documento 0 del Bloque A, 7.3: «BLOQUEADO impide la entrega»; `contratos.py`, CT-02). Un paquete sin uno de
# estos dos estados no se reenvía al Bloque B.
ESTADOS_G3_ENTREGA = ("APTO", "APTO_CON_ADVERTENCIAS")
DATO_PROTEGIDO = "«dato protegido por R8»"
DETALLE_OMITIDO = "detalle omitido: reproducía un dato protegido por R8"


def sin_datos_protegidos(texto: str) -> str:
    """T-149 (QA r01 de T-147, H-01): el texto de un error sin los datos que protege R8 (`contratos.secretos_en_texto`):
    cada uno se sustituye por «dato protegido por R8» y, si aun así queda alguno (uno que el detector solo ve con los
    escapes de JSON sustituidos, o un IBAN con otros espacios), el texto entero se cambia por un aviso. Los mensajes de
    `jsonschema` llevan el valor que no cumple («'…' is not one of …»), y una configuración rara también."""
    for dato in sorted(secretos_en_texto(texto), key=len, reverse=True):
        texto = texto.replace(dato, DATO_PROTEGIDO)
    if secretos_en_texto(texto) or contiene_credenciales(texto):
        return DETALLE_OMITIDO
    return texto


class ErrorCadenaB(ValueError):
    """La petición CT-B-01 no se construye: `codigo` dice por qué (falla cerrado, sin valores inventados)."""

    def __init__(self, codigo: str, detalle: str) -> None:
        detalle = sin_datos_protegidos(detalle)   # T-149 (QA r01 de T-147, H-01): ningún error copia un dato de R8
        super().__init__(f"{codigo}: {detalle}")
        self.codigo = codigo
        self.detalle = detalle


@lru_cache(maxsize=8)
def _validador_entrada(ruta_esquema: str, definicion: str = "entrada_bloque_B") -> jsonschema.Draft202012Validator:
    esquema = json.loads(Path(ruta_esquema).read_text(encoding="utf-8"))
    return jsonschema.Draft202012Validator({"$ref": f"#/$defs/{definicion}", "$defs": esquema["$defs"]})


def _ruta_esquema_paquete(cfg: dict) -> Path:
    p = buscar_versionado(ruta(cfg, "plantillas"), "Esquema JSON - Paquete de oportunidades", ".json")
    if p is None:
        raise ErrorCadenaB("ESQUEMA_NO_DISPONIBLE", "no se encuentra el esquema JSON del paquete de oportunidades")
    return p


def errores_entrada_b(entrada: Any, cfg: dict, definicion: str = "entrada_bloque_B") -> list[str]:
    """Errores del `paquete_para_bloque_B` de una opción frente a `$defs/entrada_bloque_B` del esquema del Bloque A (o,
    con `definicion="opcion/properties/tipos_secundarios"`, de los tipos secundarios de la opción frente a su definición
    en `$defs/opcion`, T-147)."""
    v = _validador_entrada(str(_ruta_esquema_paquete(cfg)), definicion)
    # T-149: sin los datos de R8 antes de recortar (un correo cortado ya no se reconoce y dejaría su parte local)
    return [sin_datos_protegidos(f"{'/'.join(map(str, e.absolute_path)) or '(raíz)'}: {e.message}")[:200]
            for e in v.iter_errors(entrada)][:10]


def _opciones(paquete: dict) -> list[dict]:
    out: list[dict] = []
    for clase in (paquete.get("clases") or {}).values():
        out.extend(o for o in (clase or {}).get("opciones") or [] if isinstance(o, dict))
    return out


def opciones_enviables(paquete: dict) -> list[str]:
    """`opp_id` de las opciones con `siguiente_paso_sugerido = ENVIAR_A_BLOQUE_B`, en el orden del paquete."""
    return [o["opp_id"] for o in _opciones(paquete) if o.get("siguiente_paso_sugerido") == SIGUIENTE_PASO_ENVIO]


def _una(items: list[dict], opp_id: str, donde: str) -> dict:
    hallados = [x for x in items if isinstance(x, dict) and x.get("opp_id") == opp_id]
    if not hallados:
        raise ErrorCadenaB("OPCION_DESCONOCIDA", f"{opp_id} no está en {donde}")
    if len(hallados) > 1:
        raise ErrorCadenaB("OPCION_DUPLICADA", f"{opp_id} figura {len(hallados)} veces en {donde}")
    return hallados[0]


def _seccion(cfg: dict) -> dict:
    sec = cfg.get("cadena_b")
    if not isinstance(sec, dict):
        raise ErrorCadenaB("CONFIGURACION_CADENA_B", "falta la sección «cadena_b» en la configuración")
    return sec


def clave_universo_b(entrada: dict, cfg: dict) -> str:
    """Clave del ámbito del Bloque B que corresponde al ámbito de la opción (por el símbolo de su indicador de
    seguimiento). Sin tabla, sin símbolo o sin fila para el símbolo: `ErrorCadenaB` (falla cerrado)."""
    tabla = _seccion(cfg).get("correspondencia_ambitos")
    # T-147 (QA r01 de T-142, H-03): ni el símbolo ni la clave llevan espacios (« liquidez_eur » no es la clave del Bloque B)
    if not isinstance(tabla, dict) or not tabla or not all(
            isinstance(k, str) and isinstance(v, str) and RE_SIN_ESPACIOS.fullmatch(k) and RE_SIN_ESPACIOS.fullmatch(v)
            for k, v in tabla.items()):
        raise ErrorCadenaB("CONFIGURACION_CADENA_B", "«cadena_b.correspondencia_ambitos» debe ser una tabla símbolo → clave, "
                                                     "sin espacios")
    simbolo = (entrada.get("indicador_seguimiento") or {}).get("simbolo")
    if not isinstance(simbolo, str) or not simbolo:
        raise ErrorCadenaB("SIN_CORRESPONDENCIA_AMBITO",
                           f"{entrada.get('opp_id')}: el indicador de seguimiento no trae símbolo con el que buscar el ámbito del Bloque B")
    clave = tabla.get(simbolo)
    if clave is None:
        raise ErrorCadenaB("SIN_CORRESPONDENCIA_AMBITO",
                           f"{entrada.get('opp_id')}: el ámbito de {simbolo} no tiene correspondencia con un ámbito del Bloque B")
    return clave


def _valores_de_la_peticion(cfg: dict) -> tuple[dict[str, str], str]:
    """Los valores de `cadena_b.peticion` y el idioma, validados contra el Anexo B.1 del Bloque B (T-147, QA r01 de T-142,
    H-03): un valor ausente, de otro tipo o fuera de su enumeración falla cerrado (`CONFIGURACION_CADENA_B`)."""
    defecto = _seccion(cfg).get("peticion")
    if defecto is None:
        defecto = {}
    if not isinstance(defecto, dict):
        raise ErrorCadenaB("CONFIGURACION_CADENA_B", "«cadena_b.peticion» debe ser una tabla")
    falta = [k for k in ENUMERACIONES_B1 if not defecto.get(k)]
    if falta:
        raise ErrorCadenaB("CONFIGURACION_CADENA_B", f"faltan en «cadena_b.peticion»: {', '.join(falta)}")
    fuera = [f"{k} = {defecto[k]!r} (B.1: {'|'.join(v)})" for k, v in ENUMERACIONES_B1.items() if defecto[k] not in v]
    if fuera:
        raise ErrorCadenaB("CONFIGURACION_CADENA_B", f"«cadena_b.peticion» fuera del Anexo B.1 del Bloque B: {'; '.join(fuera)}")
    idioma = cfg.get("idioma")
    if not idioma:
        raise ErrorCadenaB("CONFIGURACION_CADENA_B", "falta «idioma» en la configuración")
    if not isinstance(idioma, str) or not RE_IDIOMA.fullmatch(idioma):
        raise ErrorCadenaB("CONFIGURACION_CADENA_B", f"«idioma» = {idioma!r} no es una etiqueta de idioma como la de B.1 (es-ES)")
    return {k: defecto[k] for k in ENUMERACIONES_B1}, idioma


def construir_peticion(paquete: dict, opp_id: str, cfg: dict, *, exigir_correspondencia: bool = True) -> dict:
    """Petición CT-B-01 del Broker al Bloque B para la opción `opp_id` del paquete de oportunidades (Anexo B.1 del
    Documento 0 del Bloque B). No muta el paquete. Errores: `ErrorCadenaB` con su código.

    Sin correspondencia de ámbito, falla cerrado (`SIN_CORRESPONDENCIA_AMBITO`). Solo con
    `exigir_correspondencia=False` (la sonda de `cadena_a_b.py --sonda-sin-correspondencia`, para documentar qué hace el
    Bloque B) se construye sin clave: ni `x_clave_universo` ni `objeto.clave_universo`, nunca una clave supuesta (T-147,
    QA r01 de T-142, H-04: tampoco la que el paquete de A trajera ya en su encargo).

    T-147 (QA r01 de T-142, H-01): los `tipos_secundarios` de la opción, que entran en la petición, se validan contra su
    definición en `$defs/opcion` del esquema del Bloque A (lista de tipos de los doce, sin repetir); si no cumplen,
    `ENTRADA_B_INVALIDA`. T-149: un paquete sin `estado_g3` APTO o APTO_CON_ADVERTENCIAS (el de un ciclo con G3
    BLOQUEADO) no se reenvía (`ENTREGA_BLOQUEADA_G3`), y ningún error copia en su detalle un dato protegido por R8
    (`sin_datos_protegidos`). La opción entera no se valida: el paquete en memoria del ciclo lleva campos internos. H-02: la petición construida pasa el
    mismo filtro R8 que los mensajes del bloque (`contratos.contiene_credenciales`); si lleva credenciales o datos
    personales, no se devuelve (`DATOS_PROTEGIDOS`, sin reproducir el dato) y el Broker no la envía."""
    if not isinstance(paquete, dict):
        raise ErrorCadenaB("PAQUETE_INVALIDO", "el paquete de oportunidades no es un objeto JSON")
    if not isinstance(paquete.get("run_id"), str) or not paquete["run_id"]:
        raise ErrorCadenaB("PAQUETE_INVALIDO", "el paquete de oportunidades no trae «run_id»")
    if paquete.get("estado_g3") not in ESTADOS_G3_ENTREGA:   # T-149: sin entrega CT-02 no hay encargo
        raise ErrorCadenaB("ENTREGA_BLOQUEADA_G3", "el paquete no trae un dictamen G3 que permita la entrega "
                                                   f"({' o '.join(ESTADOS_G3_ENTREGA)}; 7.3: «BLOQUEADO impide la entrega»): "
                                                   "el Broker no lo ha recibido y no lo reenvía al Bloque B")
    opcion = _una(_opciones(paquete), opp_id, "las opciones del paquete")
    entrada = _una(paquete.get("paquete_para_bloque_B") or [], opp_id, "«paquete_para_bloque_B»")
    errores = errores_entrada_b(entrada, cfg)
    if errores:
        raise ErrorCadenaB("ENTRADA_B_INVALIDA", f"{opp_id}: " + "; ".join(errores))
    if "tipos_secundarios" in opcion:   # T-147 (H-01): lo único de la opción que entra en la petición
        errores = errores_entrada_b(opcion["tipos_secundarios"], cfg, "opcion/properties/tipos_secundarios")
        if errores:
            raise ErrorCadenaB("ENTRADA_B_INVALIDA", f"{opp_id}: tipos_secundarios de la opción: " + "; ".join(errores))
    clave: str | None
    try:
        clave = clave_universo_b(entrada, cfg)
    except ErrorCadenaB as e:
        if exigir_correspondencia or e.codigo != "SIN_CORRESPONDENCIA_AMBITO":
            raise
        clave = None
    defecto, idioma = _valores_de_la_peticion(cfg)
    encargo = copy.deepcopy(entrada)
    encargo.pop(CLAVE_EXTENSION_B, None)   # T-147 (H-04): la clave solo la pone la tabla
    objeto: dict[str, Any] = {"descripcion": entrada.get("nombre"), "tipo_objeto_sugerido": None,
                              "ambito": copy.deepcopy(entrada["ambito"])}
    if clave is not None:
        encargo[CLAVE_EXTENSION_B] = clave
        objeto["clave_universo"] = clave
    tipos = [entrada["tipo_activo"]] + [t for t in opcion.get("tipos_secundarios") or [] if t != entrada["tipo_activo"]]
    peticion = {
        "pet_ref_broker": f"{paquete['run_id']}/{opp_id}",
        "origen": ORIGEN_BLOQUE_A,
        "paquete_para_bloque_B": encargo,
        "objeto": objeto,
        "tipos_activo_admitidos": tipos,
        "horizontes": list(entrada["horizontes"]),
        "preguntas": [],
        "nivel": defecto["nivel"],
        "limite": {"minutos": None, "uc": None},
        "prioridad": defecto["prioridad"],
        "fecha_objetivo": None,
        "marco_invertibilidad": {"perfil": defecto["perfil_invertibilidad"]},
        "top_n": None,
        "alto_impacto": False,
        "referencia_previa": None,
        "idioma_usuario": idioma,
    }
    # T-147 (QA r01 de T-142, H-02): R8 del Documento 0 del Bloque A («ningún mensaje, paquete, archivo ni contexto»
    # lleva credenciales ni datos personales). Solo se nombran los campos, nunca el dato
    if contiene_credenciales(peticion):
        campos = [k for k, v in peticion.items() if contiene_credenciales(v)]
        raise ErrorCadenaB("DATOS_PROTEGIDOS", f"{opp_id}: la petición lleva credenciales o datos personales en {campos} "
                                               f"(R8): el Broker no la envía")
    return peticion


def ct04_desde_respuesta_b(opp_id: str, respuesta_b: dict) -> dict:
    """CT-04 del Broker al Bloque A tras enviar la opción al Bloque B (7.7 y Anexo B del Documento 0 del Bloque A): la
    decisión `ENVIADA_A_BLOQUE_B` y, como `resultado_comunicado`, un texto con lo que devolvió el Bloque B (sus
    identificadores y su estado, tal cual; lo que no venga no se escribe)."""
    if not isinstance(respuesta_b, dict) or not respuesta_b.get("pet_id"):
        raise ErrorCadenaB("RESPUESTA_B_INVALIDA", f"{opp_id}: la respuesta del Bloque B no trae «pet_id»")
    resumen = respuesta_b.get("resumen")
    if not isinstance(resumen, dict):
        resumen = {}
    partes = [f"Bloque B {respuesta_b['pet_id']}"]
    for etiqueta, valor in (("admisión", respuesta_b.get("admision") or (respuesta_b.get("acuse_inmediato") or {}).get("admision")),
                            ("motivo", respuesta_b.get("motivo")),
                            ("estado", respuesta_b.get("estado_peticion")),
                            ("registro", respuesta_b.get("rec_id")),
                            ("veredicto", resumen.get("veredicto")),
                            ("resultado", resumen.get("resultado_del_analisis"))):
        if valor:
            partes.append(f"{etiqueta} {valor}")
    return {"decisiones": [{"opp_id": opp_id, "decision": DECISION_ENVIADA, "motivo": f"Petición CT-B-01 {respuesta_b['pet_id']}"}],
            "resultado_comunicado": {"opp_id": opp_id, "texto": "; ".join(partes)}}
