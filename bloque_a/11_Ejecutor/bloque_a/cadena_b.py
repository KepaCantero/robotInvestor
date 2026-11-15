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
from functools import lru_cache
from pathlib import Path
from typing import Any

import jsonschema

from .configuracion import buscar_versionado, ruta

ORIGEN_BLOQUE_A = "BLOQUE_A"
SIGUIENTE_PASO_ENVIO = "ENVIAR_A_BLOQUE_B"
DECISION_ENVIADA = "ENVIADA_A_BLOQUE_B"
CLAVE_EXTENSION_B = "x_clave_universo"   # extensión que lee el ejecutor del Bloque B (su README, 3; peticion_redes_bloque_a.json)


class ErrorCadenaB(ValueError):
    """La petición CT-B-01 no se construye: `codigo` dice por qué (falla cerrado, sin valores inventados)."""

    def __init__(self, codigo: str, detalle: str) -> None:
        super().__init__(f"{codigo}: {detalle}")
        self.codigo = codigo
        self.detalle = detalle


@lru_cache(maxsize=4)
def _validador_entrada(ruta_esquema: str) -> jsonschema.Draft202012Validator:
    esquema = json.loads(Path(ruta_esquema).read_text(encoding="utf-8"))
    return jsonschema.Draft202012Validator({"$ref": "#/$defs/entrada_bloque_B", "$defs": esquema["$defs"]})


def _ruta_esquema_paquete(cfg: dict) -> Path:
    p = buscar_versionado(ruta(cfg, "plantillas"), "Esquema JSON - Paquete de oportunidades", ".json")
    if p is None:
        raise ErrorCadenaB("ESQUEMA_NO_DISPONIBLE", "no se encuentra el esquema JSON del paquete de oportunidades")
    return p


def errores_entrada_b(entrada: Any, cfg: dict) -> list[str]:
    """Errores del `paquete_para_bloque_B` de una opción frente a `$defs/entrada_bloque_B` del esquema del Bloque A."""
    v = _validador_entrada(str(_ruta_esquema_paquete(cfg)))
    return [f"{'/'.join(map(str, e.absolute_path)) or '(raíz)'}: {e.message}"[:200] for e in v.iter_errors(entrada)][:10]


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
    if not isinstance(tabla, dict) or not all(isinstance(k, str) and isinstance(v, str) and v.strip() for k, v in tabla.items()):
        raise ErrorCadenaB("CONFIGURACION_CADENA_B", "«cadena_b.correspondencia_ambitos» debe ser una tabla símbolo → clave")
    simbolo = (entrada.get("indicador_seguimiento") or {}).get("simbolo")
    if not isinstance(simbolo, str) or not simbolo:
        raise ErrorCadenaB("SIN_CORRESPONDENCIA_AMBITO",
                           f"{entrada.get('opp_id')}: el indicador de seguimiento no trae símbolo con el que buscar el ámbito del Bloque B")
    clave = tabla.get(simbolo)
    if clave is None:
        raise ErrorCadenaB("SIN_CORRESPONDENCIA_AMBITO",
                           f"{entrada.get('opp_id')}: el ámbito de {simbolo} no tiene correspondencia con un ámbito del Bloque B")
    return clave


def construir_peticion(paquete: dict, opp_id: str, cfg: dict, *, exigir_correspondencia: bool = True) -> dict:
    """Petición CT-B-01 del Broker al Bloque B para la opción `opp_id` del paquete de oportunidades (Anexo B.1 del
    Documento 0 del Bloque B). No muta el paquete. Errores: `ErrorCadenaB` con su código.

    Sin correspondencia de ámbito, falla cerrado (`SIN_CORRESPONDENCIA_AMBITO`). Solo con
    `exigir_correspondencia=False` (la sonda de `cadena_a_b.py --sonda-sin-correspondencia`, para documentar qué hace el
    Bloque B) se construye sin clave: ni `x_clave_universo` ni `objeto.clave_universo`, nunca una clave supuesta."""
    if not isinstance(paquete, dict):
        raise ErrorCadenaB("PAQUETE_INVALIDO", "el paquete de oportunidades no es un objeto JSON")
    if not isinstance(paquete.get("run_id"), str) or not paquete["run_id"]:
        raise ErrorCadenaB("PAQUETE_INVALIDO", "el paquete de oportunidades no trae «run_id»")
    opcion = _una(_opciones(paquete), opp_id, "las opciones del paquete")
    entrada = _una(paquete.get("paquete_para_bloque_B") or [], opp_id, "«paquete_para_bloque_B»")
    errores = errores_entrada_b(entrada, cfg)
    if errores:
        raise ErrorCadenaB("ENTRADA_B_INVALIDA", f"{opp_id}: " + "; ".join(errores))
    clave: str | None
    try:
        clave = clave_universo_b(entrada, cfg)
    except ErrorCadenaB as e:
        if exigir_correspondencia or e.codigo != "SIN_CORRESPONDENCIA_AMBITO":
            raise
        clave = None
    defecto = _seccion(cfg).get("peticion") or {}
    falta = [k for k in ("nivel", "prioridad", "perfil_invertibilidad") if not defecto.get(k)]
    if falta:
        raise ErrorCadenaB("CONFIGURACION_CADENA_B", f"faltan en «cadena_b.peticion»: {', '.join(falta)}")
    if not cfg.get("idioma"):
        raise ErrorCadenaB("CONFIGURACION_CADENA_B", "falta «idioma» en la configuración")
    encargo = copy.deepcopy(entrada)
    objeto: dict[str, Any] = {"descripcion": entrada.get("nombre"), "tipo_objeto_sugerido": None,
                              "ambito": copy.deepcopy(entrada["ambito"])}
    if clave is not None:
        encargo[CLAVE_EXTENSION_B] = clave
        objeto["clave_universo"] = clave
    tipos = [entrada["tipo_activo"]] + [t for t in opcion.get("tipos_secundarios") or [] if t != entrada["tipo_activo"]]
    return {
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
        "idioma_usuario": cfg["idioma"],
    }


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
