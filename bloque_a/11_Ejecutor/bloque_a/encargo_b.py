"""Preparación local de CT-B-01 a partir de una entrega validada y una decisión del Broker."""
from __future__ import annotations

import json
from copy import deepcopy

import jsonschema

from .configuracion import DIR_EJECUTOR, buscar_versionado
from .contratos import contiene_credenciales


def preparar_encargo_b(paquete: dict, decision: dict, universos: dict) -> dict:
    """La decisión fija la pareja de ámbitos que el Broker comprobó. No hay envío ni coincidencia aproximada."""
    ruta = buscar_versionado(DIR_EJECUTOR.parent / "06_Plantillas_entregables", "Esquema JSON - Paquete de oportunidades", ".json")
    if ruta is None:
        raise ValueError("Falta el esquema oficial del paquete de A")
    jsonschema.Draft202012Validator(json.loads(ruta.read_text(encoding="utf-8"))).validate(paquete)
    if not isinstance(decision, dict) or not isinstance(universos, dict):
        raise TypeError("La decisión y el catálogo de universos deben ser objetos")
    if paquete.get("estado_g3") not in ("APTO", "APTO_CON_ADVERTENCIAS"):
        raise ValueError("G3 no autoriza este paquete")
    if decision.get("decision") != "ENVIADA_A_BLOQUE_B" or decision.get("run_id") != paquete["run_id"]:
        raise ValueError("Falta la decisión explícita del Broker sobre esta entrega")
    ordenes = [o for o in paquete["paquete_para_bloque_B"] if o["opp_id"] == decision.get("opp_id")]
    if len(ordenes) != 1:
        raise ValueError("Se requiere un único encargo de A para la OPP indicada")
    orden = ordenes[0]
    clave = decision.get("clave_universo")
    destino = universos.get(clave) if isinstance(clave, str) else None
    if destino is None:
        raise ValueError("El universo confirmado no existe en el catálogo de B")
    if not isinstance(destino, dict):
        raise TypeError("Se requiere una ficha de universo")
    ambito_b = {k: destino[k] for k in ("incluye", "excluye", "region")}
    if orden["ambito"] != decision.get("ambito_a") or ambito_b != decision.get("ambito_b"):
        raise ValueError("Los ámbitos actuales difieren de la correspondencia confirmada por el Broker")
    if orden["tipo_activo"] not in destino["tipos_activo"]:
        raise ValueError("El universo confirmado no estudia el tipo de activo del encargo")
    if orden.get("x_clave_universo", clave) != clave:
        raise ValueError("El encargo ya identifica otro universo")
    encargo = deepcopy(orden)
    encargo["x_clave_universo"] = clave
    peticion = {"origen": "BLOQUE_A", "pet_ref_broker": f"{paquete['run_id']}:{orden['opp_id']}",
                "objeto": {"descripcion": orden["nombre"], "ambito": deepcopy(orden["ambito"]),
                           "tipo_objeto_sugerido": destino["tipo_objeto"], "clave_universo": clave},
                "tipos_activo_admitidos": [orden["tipo_activo"]], "horizontes": list(orden["horizontes"]),
                "paquete_para_bloque_B": encargo}
    if contiene_credenciales(peticion):
        raise ValueError("El borrador contiene datos protegidos")
    return peticion
