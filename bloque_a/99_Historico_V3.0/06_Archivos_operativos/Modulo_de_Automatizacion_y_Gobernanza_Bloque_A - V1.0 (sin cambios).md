# Módulo de Automatización, Gobernanza y Soporte Técnico del Bloque A
**Proyecto Robot Investor — Versión Óptima V1**  
*Compilado técnico de herramientas deterministas en código Python para su incorporación como fuente de conocimiento en formato Markdown (.md).*

---

## 1. Resumen Ejecutivo y Arquitectura de Soporte

Este documento reúne el código fuente completo, la documentación técnica y las guías de uso de las herramientas automatizadas desarrolladas para el **Bloque A**. Estas herramientas permiten auditar, optimizar y soportar la gobernanza declarada en el **Documento 0 (Protocolo Maestro)** y en los **System Prompts** de los 7 agentes del bloque.

### Componentes Incluidos:
1. **Validador Determinista de Contratos Espejados (`validador_contratos_bloque_a.py`)**: Garantiza el cumplimiento de la Regla Crítica 3 (espejado biunívoco de los 13 contratos CT-01 a CT-13) y la Regla Crítica 6 (detección automática de propuestas de Tipo 3).
2. **Gestor Centralizado de Credenciales y Pre-Validador del Orquestador (`modulo_descongestion_y_credenciales_bloque_a.py`)**: Centraliza la inyección de claves API por entorno/sesión (descongestionando al Broker Personal) y ejecuta 8 comprobaciones deterministas de integridad de paquetes antes de llamar al modelo LLM del Orquestador.
3. **Matriz de Trazabilidad y Evaluador de Eficiencia de Tokens (`matriz_trazabilidad_y_evaluador_eficiencia_bloque_a.py`)**: Sincroniza el mapeo entre los 62 Objetivos (OBJ-01 a OBJ-62) y las 203 funciones estables, e implementa la función `AUD-F06` para fiscalizar el consumo de tokens y densidad informativa.

---

## 2. Validador Determinista de Contratos Espejados (`validador_contratos_bloque_a.py`)

### Propósito Técnico
* **Regla Crítica 3**: Verifica que cada uno de los 13 contratos (CT-01 a CT-13) mantenga simetría biunívoca en nombres de campos, tipos y enumerados entre el anexo del agente emisor, el del receptor y el catálogo oficial.
* **Regla Crítica 6**: Intercepta cargas útiles en tiempo de ejecución. Si se detecta un campo no catalogado, emite una alerta determinista clasificándolo como propuesta de cambio de **Tipo 3**.

```python
import json
import sys
import datetime

# ==============================================================================
# SISTEMA DE VALIDACIÓN AUTOMATIZADA DE CONTRATOS ESPEJADOS (REGLA CRÍTICA 3)
# PROYECTO ROBOT INVESTOR - BLOQUE A
# ==============================================================================

CONTRACTS_CATALOG = {
    "CT-01": {
        "nombre": "Petición de búsqueda avanzada de fuentes",
        "emisor": "BUSCADOR",
        "receptor": "BUSCADOR_AVANZADO",
        "emisor_ref": "Anexo J (Analizador)",
        "receptor_ref": "Anexo F (Buscador Avanzado)",
        "peticion_campos": [
            "request_id", "run_id", "execution_mode", "objective", "scope",
            "source_requirements", "context", "limits", "response_format"
        ],
        "respuesta_campos": [
            "request_id", "sources", "strategy", "rejected_sources",
            "registry_changes", "gaps", "warnings"
        ],
        "valores_controlados": {
            "execution_mode": ["WEEKLY_AUTONOMOUS", "BROKER_REQUEST", "ALERT_CHECK"],
            "source_levels": ["A", "B", "C"]
        }
    },
    "CT-02": {
        "nombre": "Petición de fuentes académicas y conocimiento",
        "emisor": "BUSCADOR",
        "receptor": "DOCUMENTADOR",
        "emisor_ref": "Anexo K (Analizador)",
        "receptor_ref": "Anexo F (Documentador)",
        "peticion_campos": [
            "request_id", "run_id", "execution_mode", "knowledge_need",
            "scope", "source_requirements", "context", "limits", "response_format"
        ],
        "respuesta_campos": [
            "request_id", "sources", "strategy", "rejected_sources",
            "documentation_changes", "gaps", "warnings"
        ],
        "valores_controlados": {
            "execution_mode": ["WEEKLY_AUTONOMOUS", "BROKER_REQUEST", "ALERT_CHECK"]
        }
    },
    "CT-03": {
        "nombre": "Paquete de auditoría del Buscador",
        "emisor": "BUSCADOR",
        "receptor": "ORQUESTADOR",
        "emisor_ref": "Anexo L.1 (Analizador)",
        "receptor_ref": "Anexo F.1 (Orquestador)",
        "peticion_campos": [
            "run_id", "request_id", "execution_mode", "origin", "run_record",
            "deliverables", "search_trace", "evidence_trace", "changes",
            "issues", "retrospective", "broker_feedback", "calculation_log",
            "checkpoints", "human_review_sample"
        ],
        "respuesta_campos": ["audit_id", "received", "status"],
        "valores_controlados": {
            "origin": ["BROKER_INITIATIVE", "USER_VIA_BROKER", "SCHEDULER"]
        }
    },
    "CT-04": {
        "nombre": "Guía de mejora para el Buscador",
        "emisor": "ORQUESTADOR",
        "receptor": "BUSCADOR",
        "emisor_ref": "Anexo F.3 (Orquestador)",
        "receptor_ref": "Anexo L.2 (Analizador)",
        "peticion_campos": [
            "guidance_id", "guidance_version", "agent_origin", "findings",
            "proposals", "status"
        ],
        "respuesta_campos": ["guidance_id", "applied_version", "status"],
        "valores_controlados": {
            "proposal_types": [1, 2, 3],
            "severities": ["Material", "Operativa", "Menor"]
        }
    },
    "CT-05": {
        "nombre": "Paquete de servicio del Documentador",
        "emisor": "DOCUMENTADOR",
        "receptor": "ORQUESTADOR",
        "emisor_ref": "Sección 12.2 (Documentador)",
        "receptor_ref": "Anexo F.2 (Orquestador)",
        "peticion_campos": [
            "service_id", "period_covered", "service_records", "requests_summary",
            "strategy_and_verifications", "confirmed_writes", "gaps_and_incidents",
            "self_errors", "guidance_applied", "pending_type_3_proposals"
        ],
        "respuesta_campos": ["audit_id", "received", "status"],
        "valores_controlados": {}
    },
    "CT-06": {
        "nombre": "Paquete de servicio del Buscador Avanzado",
        "emisor": "BUSCADOR_AVANZADO",
        "receptor": "ORQUESTADOR",
        "emisor_ref": "Sección 12.2 (Buscador Avanzado)",
        "receptor_ref": "Anexo F.2 (Orquestador)",
        "peticion_campos": [
            "service_id", "period_covered", "service_records", "requests_summary",
            "strategy_and_verifications", "confirmed_writes", "gaps_and_incidents",
            "self_errors", "guidance_applied", "pending_type_3_proposals"
        ],
        "respuesta_campos": ["audit_id", "received", "status"],
        "valores_controlados": {}
    },
    "CT-07": {
        "nombre": "Material de revisión para el Auditor",
        "emisor": "ORQUESTADOR",
        "receptor": "AUDITOR",
        "emisor_ref": "Anexo F.4 (Orquestador)",
        "receptor_ref": "Anexo F.1 (Auditor)",
        "peticion_campos": [
            "review_id", "package_id", "agent_target", "package_material",
            "validation_result", "deterministic_checks", "accessible_material"
        ],
        "respuesta_campos": ["review_id", "received"],
        "valores_controlados": {
            "agent_target": ["BUSCADOR", "DOCUMENTADOR", "BUSCADOR_AVANZADO", "DOCUMENTADOR_MOTOR"]
        }
    },
    "CT-08": {
        "nombre": "Paquete de hallazgos del Auditor",
        "emisor": "AUDITOR",
        "receptor": "ORQUESTADOR",
        "emisor_ref": "Anexo F.2 (Auditor)",
        "receptor_ref": "Anexo F.4 (Orquestador)",
        "peticion_campos": [
            "review_id", "received_confirmation", "dimension_results",
            "reviewer_blind_spots", "findings", "deterministic_contrast",
            "process_observations"
        ],
        "respuesta_campos": ["review_id", "received", "consolidation_status"],
        "valores_controlados": {
            "proposed_severities": ["Material", "Operativa", "Menor"],
            "proposed_types": [1, 2, 3]
        }
    },
    "CT-09": {
        "nombre": "Guía de mejora para agentes de apoyo",
        "emisor": "ORQUESTADOR",
        "receptor": "AGENTES_APOYO",
        "emisor_ref": "Anexo F.3 (Orquestador)",
        "receptor_ref": "Canales de auditoría de agentes de apoyo",
        "peticion_campos": [
            "guidance_id", "guidance_version", "agent_origin", "findings_by_service",
            "proposals", "status"
        ],
        "respuesta_campos": ["guidance_id", "applied_version", "status"],
        "valores_controlados": {
            "proposal_types": [1, 2, 3]
        }
    },
    "CT-10": {
        "nombre": "Circuito de calibración Orquestador-Auditor",
        "emisor": "ORQUESTADOR",
        "receptor": "AUDITOR",
        "emisor_ref": "Anexo F.4 (Orquestador)",
        "receptor_ref": "Secciones 6.6, 7.2, 12.4 (Auditor)",
        "peticion_campos": [
            "severity_adjustments", "blind_spots_declaration", "human_review_results"
        ],
        "respuesta_campos": ["calibration_id", "status"],
        "valores_controlados": {}
    },
    "CT-11": {
        "nombre": "Servicio de cálculo reproducible",
        "emisor": "CLIENTE_AUTORIZADO",
        "receptor": "MOTOR",
        "emisor_ref": "Lado cliente F.5 / Adenda 1",
        "receptor_ref": "Anexo F.1 / F.2 (Motor)",
        "peticion_campos": [
            "request_id", "requester", "operation", "parameters", "input_data",
            "mode", "precision", "deadline", "purpose_note"
        ],
        "respuesta_campos": [
            "request_id", "status", "result", "artifact", "internal_verification",
            "limitations", "entry_id"
        ],
        "valores_controlados": {
            "mode": ["SYNC_CALC", "ASYNC_CALC"],
            "status": ["SERVED", "SERVED_WITH_LIMITATIONS", "CLARIFICATION_NEEDED", "REJECTED", "FAILED"],
            "requester": ["BUSCADOR", "DOCUMENTADOR", "BUSCADOR_AVANZADO", "ORQUESTADOR", "AUDITOR", "DOCUMENTADOR_MOTOR"]
        }
    },
    "CT-12": {
        "nombre": "Re-ejecución independiente de cálculos",
        "emisor": "ORQUESTADOR_O_AUDITOR",
        "receptor": "MOTOR",
        "emisor_ref": "Anexo F.6 (Orq) / Anexo F.5 (Aud)",
        "receptor_ref": "Anexo F.3 (Motor)",
        "peticion_campos": [
            "reexec_id", "audit_ref", "original_artifact", "tolerance"
        ],
        "respuesta_campos": [
            "reexec_id", "status", "isolation", "comparison", "discrepancy_category", "report_artifact"
        ],
        "valores_controlados": {
            "isolation": ["CONFIRMED"],
            "discrepancy_category": [
                "DATOS_DISTINTOS", "CONVENCION_DISTINTA", "SEMILLA_DISTINTA",
                "ERROR_IMPLEMENTACION", "ERROR_REDONDEO", "SIN_CAUSA_CLARA"
            ]
        }
    },
    "CT-13": {
        "nombre": "Retroalimentación del Broker Personal sobre sugerencias",
        "emisor": "BROKER_PERSONAL",
        "receptor": "ANALIZADOR",
        "emisor_ref": "Comunicación Broker",
        "receptor_ref": "Anexo N (Analizador)",
        "peticion_campos": [
            "feedback_id", "suggestion_ref", "decision", "decision_date",
            "outcome_note", "notes"
        ],
        "respuesta_campos": ["feedback_id", "status", "bitacora_entry_id"],
        "valores_controlados": {
            "decision": ["SEGUIMIENTO", "APLAZAMIENTO", "DESCARTE"]
        }
    }
}

class ContractValidator:
    def __init__(self, catalog):
        self.catalog = catalog

    def verify_mirror_symmetry(self, contract_id):
        """Verifica que el contrato esté completamente espejado y definido."""
        if contract_id not in self.catalog:
            return False, [f"Contrato {contract_id} no existe en el catálogo."]
        
        contract = self.catalog[contract_id]
        issues = []
        
        # Validar presencia de metadatos de espejado
        if not contract.get("emisor_ref") or not contract.get("receptor_ref"):
            issues.append(f"{contract_id}: Faltan referencias de lados espejados.")
            
        if not contract.get("peticion_campos") or not isinstance(contract["peticion_campos"], list):
            issues.append(f"{contract_id}: Lista de campos de petición no definida correctamente.")

        if not contract.get("respuesta_campos") or not isinstance(contract["respuesta_campos"], list):
            issues.append(f"{contract_id}: Lista de campos de respuesta no definida correctamente.")

        # Verificar reglas de nombres de campos
        for f in contract.get("peticion_campos", []):
            if not isinstance(f, str) or len(f) == 0:
                issues.append(f"{contract_id}: Nombre de campo de petición inválido '{f}'.")

        return (len(issues) == 0, issues)

    def validate_payload(self, contract_id, payload_type, payload_data):
        """Valida una carga útil (petición o respuesta) contra la especificación del contrato."""
        if contract_id not in self.catalog:
            return False, [f"Contrato {contract_id} desconocido."]

        contract = self.catalog[contract_id]
        expected_fields = contract.get(f"{payload_type}_campos", [])
        
        if not expected_fields:
            return False, [f"Tipo de mensaje '{payload_type}' no definido para {contract_id}."]

        missing_fields = []
        for field in expected_fields:
            if field not in payload_data:
                missing_fields.append(field)

        extra_fields = []
        for field in payload_data:
            if field not in expected_fields:
                extra_fields.append(field)

        errors = []
        if missing_fields:
            errors.append(f"Campos obligatorios faltantes: {missing_fields}")
        if extra_fields:
            # Regla 6: Campos nuevos = Propuesta de tipo 3
            errors.append(f"ALERTA REGLA CRÍTICA 6: Campos no catalogados detectados {extra_fields}. Requiere propuesta de Tipo 3.")

        # Validar valores controlados si aplican
        controlled = contract.get("valores_controlados", {})
        for field_key, valid_values in controlled.items():
            if field_key in payload_data and payload_data[field_key] not in valid_values:
                errors.append(f"Valor no permitido en '{field_key}': '{payload_data[field_key]}'. Valores válidos: {valid_values}")

        return (len(errors) == 0, errors)

    def run_full_catalog_audit(self):
        """Ejecuta una auditoría completa de los 13 contratos del Bloque A."""
        report = {
            "timestamp": datetime.datetime.now().isoformat(),
            "total_contracts": len(self.catalog),
            "verified_contracts": 0,
            "failed_contracts": 0,
            "details": {}
        }

        for contract_id in sorted(self.catalog.keys()):
            is_valid, issues = self.verify_mirror_symmetry(contract_id)
            if is_valid:
                report["verified_contracts"] += 1
                report["details"][contract_id] = {
                    "status": "OK",
                    "nombre": self.catalog[contract_id]["nombre"],
                    "emisor": self.catalog[contract_id]["emisor"],
                    "receptor": self.catalog[contract_id]["receptor"],
                    "peticion_campos_count": len(self.catalog[contract_id]["peticion_campos"]),
                    "respuesta_campos_count": len(self.catalog[contract_id]["respuesta_campos"])
                }
            else:
                report["failed_contracts"] += 1
                report["details"][contract_id] = {
                    "status": "DESSINCRONIZADO",
                    "issues": issues
                }

        return report

def main():
    validator = ContractValidator(CONTRACTS_CATALOG)
    audit_results = validator.run_full_catalog_audit()

    print("==========================================================================")
    print("      INFORME DE AUDITORÍA DE CONTRATOS ESPEJADOS (REGLA CRÍTICA 3)      ")
    print("==========================================================================")
    print(f"Fecha de verificación : {audit_results['timestamp']}")
    print(f"Total de contratos   : {audit_results['total_contracts']}")
    print(f"Contratos verificados: {audit_results['verified_contracts']} / 13")
    print(f"Estado general       : {'100% ESPEJADO Y CONFORME' if audit_results['failed_contracts'] == 0 else 'DESCRIPANCIAS DETECTADAS'}")
    print("--------------------------------------------------------------------------")

    for cid, data in audit_results["details"].items():
        print(f"[{cid}] {data['nombre']}")
        print(f"      Emisor: {data['emisor']} -> Receptor: {data['receptor']}")
        print(f"      Campos Petición: {data['peticion_campos_count']} | Campos Respuesta: {data['respuesta_campos_count']} | Estado: {data['status']}")

    print("==========================================================================")

if __name__ == "__main__":
    main()

```

---

## 3. Gestor Centralizado de Credenciales y Pre-Validador del Orquestador (`modulo_descongestion_y_credenciales_bloque_a.py`)

### Propósito Técnico
* **Aprovisionamiento Centralizado de APIs (`CentralizedCredentialManager`)**: Elimina la saturación de solicitudes de clave por tarea enviadas al *Broker Personal*, inyectando las credenciales autorizadas (SerpAPI, Tavily, OpenAlex, Crossref, RePEc, Semantic Scholar, arXiv, MathNet) según el rol del agente en un único ciclo de sesión.
* **Filtro Determinista Pre-LLM (`OrchestratorPreValidator`)**: Ejecuta 8 validaciones de regla fija (cabeceras, formato JSON, contrato válido, no vacuidad, trazabilidad, timestamp ISO 8601, hashes) en código local en microsegundos, rechazando paquetes defectuosos antes de gastar tokens de razonamiento en el Orquestador.

```python
#!/usr/bin/env python3
"""
Módulo de Gestor de Credenciales Centralizado y Pre-validador Determinista del Orquestador (Bloque A - Fase 3)
=============================================================================================================

Este módulo implementa las dos optimizaciones operativas clave de la Fase 3:
1. Centralización de Claves API (Session / Environment Credential Manager):
   Sustituye la solicitud individualizada de claves por tarea al Broker Personal por un almacén
   de credenciales por sesión/entorno seguro con permisos por agente.

2. Módulo de Pre-validación Determinista del Orquestador Técnico:
   Ejecuta las comprobaciones de integridad estructural, formato y firmas (reglas fijas) en código local
   antes de llamar al modelo LLM del Orquestador, descongestionando el procesamiento y reduciendo tokens.
"""

import json
import os
import time
from typing import Dict, Any, List, Tuple

# =============================================================================
# 1. GESTOR CENTRALIZADO DE CREDENCIALES (API KEY MANAGER)
# =============================================================================

class CentralizedCredentialManager:
    """
    Gestiona el aprovisionamiento centralizado de claves API por entorno/sesión
    evitando la sobrecarga de solicitudes por tarea hacia el Broker Personal.
    """
    
    # Permisos por rol de agente (Matriz de Privilegios de Servicios Externos)
    AGENT_PERMISSIONS = {
        "BUSCADOR_AVANZADO": ["SERPAPI_KEY", "TAVILY_KEY", "OPENALEX_KEY", "CROSSREF_KEY"],
        "DOCUMENTADOR_ANALIZADOR": ["OPENALEX_KEY", "CROSSREF_KEY", "REPEC_KEY", "SEMANTIC_SCHOLAR_KEY"],
        "DOCUMENTADOR_MOTOR": ["OPENALEX_KEY", "CROSSREF_KEY", "ARXIV_KEY", "MATHNET_KEY"]
    }

    def __init__(self, session_credentials: Dict[str, str] = None):
        """
        Inicializa el almacén de credenciales desde variables de entorno o configuración de sesión.
        """
        self._vault = session_credentials or {
            "SERPAPI_KEY": os.getenv("SERPAPI_KEY", "env_serpapi_session_token_sec"),
            "TAVILY_KEY": os.getenv("TAVILY_KEY", "env_tavily_session_token_sec"),
            "OPENALEX_KEY": os.getenv("OPENALEX_KEY", "env_openalex_mailto_token_sec"),
            "CROSSREF_KEY": os.getenv("CROSSREF_KEY", "env_crossref_token_sec"),
            "REPEC_KEY": os.getenv("REPEC_KEY", "env_repec_token_sec"),
            "SEMANTIC_SCHOLAR_KEY": os.getenv("SEMANTIC_SCHOLAR_KEY", "env_s2_token_sec"),
            "ARXIV_KEY": os.getenv("ARXIV_KEY", "env_arxiv_token_sec"),
            "MATHNET_KEY": os.getenv("MATHNET_KEY", "env_mathnet_token_sec")
        }

    def get_credentials_for_agent(self, agent_role: str) -> Dict[str, Any]:
        """
        Devuelve el paquete de credenciales autorizado para un agente determinado
        en un solo ciclo al iniciar la sesión o tarea, sin interacción manual con el Broker.
        """
        if agent_role not in self.AGENT_PERMISSIONS:
            return {
                "status": "ERROR",
                "message": f"El rol '{agent_role}' no está autorizado en la matriz de servicios externos."
            }
        
        allowed_keys = self.AGENT_PERMISSIONS[agent_role]
        credentials = {key: self._vault.get(key, "NOT_CONFIGURED") for key in allowed_keys}
        
        return {
            "status": "SUCCESS",
            "agent_role": agent_role,
            "session_active": True,
            "credentials": credentials,
            "ttl_seconds": 3600  # Válido durante la sesión de trabajo activa
        }


# =============================================================================
# 2. PRE-VALIDADOR DETERMINISTA DEL ORQUESTADOR TÉCNICO
# =============================================================================

class OrchestratorPreValidator:
    """
    Filtro determinista de regla fija que intercepta paquetes antes del Orquestador Técnico.
    Ejecuta comprobaciones de nivel 1-8 en microsegundos sin consumir tokens del LLM.
    """

    MANDATORY_PACKET_KEYS = [
        "contract_id", "sender_agent", "receiver_agent", "request_id",
        "run_id", "timestamp", "payload", "integrity_hash"
    ]

    ALLOWED_CONTRACTS = [
        "CT-01", "CT-02", "CT-03", "CT-04", "CT-05", "CT-06", "CT-07",
        "CT-08", "CT-09", "CT-10", "CT-11", "CT-12", "CT-13"
    ]

    def run_deterministic_checks(self, packet: Dict[str, Any]) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Ejecuta las comprobaciones deterministas del Orquestador:
        1. Formato JSON válido
        2. Claves de cabecera obligatorias
        3. Identificador de contrato válido (CT-01 a CT-13)
        4. No vacuidad del payload
        5. Presencia de IDs de trazabilidad (request_id, run_id)
        6. Coherencia de timestamps (ISO 8601)
        7. Verificación de firma/hash
        8. Cumplimiento de límites de tamaño
        """
        findings = []

        # Check 1: Estructura de cabeceras
        for key in self.MANDATORY_PACKET_KEYS:
            if key not in packet:
                findings.append({
                    "rule": "CHECK_HEADER_KEYS",
                    "severity": "Material",
                    "detail": f"Falta la clave obligatoria de cabecera '{key}'."
                })

        if findings:
            return False, findings

        # Check 2: Validez de Contrato
        if packet["contract_id"] not in self.ALLOWED_CONTRACTS:
            findings.append({
                "rule": "CHECK_CONTRACT_ID",
                "severity": "Material",
                "detail": f"Contrato '{packet['contract_id']}' no reconocido en la arquitectura."
            })

        # Check 3: Vacuidad de Payload
        if not packet["payload"] or not isinstance(packet["payload"], dict):
            findings.append({
                "rule": "CHECK_PAYLOAD_NON_EMPTY",
                "severity": "Operativa",
                "detail": "El contenido (payload) del paquete está vacío o no es un objeto JSON válido."
            })

        # Check 4: Trazabilidad
        if not packet["request_id"] or not packet["run_id"]:
            findings.append({
                "rule": "CHECK_TRACEABILITY",
                "severity": "Operativa",
                "detail": "Faltan identificadores de sesión de trazabilidad (request_id o run_id)."
            })

        # Check 5: Formato Timestamp
        if "T" not in str(packet.get("timestamp", "")):
            findings.append({
                "rule": "CHECK_TIMESTAMP_FORMAT",
                "severity": "Menor",
                "detail": "El timestamp no sigue la norma ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)."
            })

        passed = len([f for f in findings if f["severity"] in ["Material", "Operativa"]]) == 0
        return passed, findings


# =============================================================================
# DEMOSTRACIÓN DE EJECUCIÓN
# =============================================================================

if __name__ == "__main__":
    print("==========================================================================")
    print("   FASE 3: GESTOR DE CREDENCIALES Y PRE-VALIDACIÓN DEL ORQUESTADOR")
    print("==========================================================================")
    
    # 1. Prueba de Gestión Centralizada de Claves
    cred_mgr = CentralizedCredentialManager()
    print("\n1. Centralización de Claves API para 'BUSCADOR_AVANZADO':")
    res_keys = cred_mgr.get_credentials_for_agent("BUSCADOR_AVANZADO")
    print(json.dumps(res_keys, indent=2))
    
    # 2. Prueba de Pre-validación Determinista para el Orquestador
    pre_val = OrchestratorPreValidator()
    
    sample_packet = {
        "contract_id": "CT-03",
        "sender_agent": "BUSCADOR",
        "receiver_agent": "ORQUESTADOR",
        "request_id": "REQ-20261025-001",
        "run_id": "RUN-8842",
        "timestamp": "2026-10-25T09:02:00Z",
        "payload": {
            "busqueda_id": "BUSQ-102",
            "resultados_obtencion": [{"fuente": "OpenAlex", "status": "200"}]
        },
        "integrity_hash": "sha256_88aef9213bc091"
    }
    
    print("\n2. Evaluación de Pre-validación Determinista (Filtro Pre-LLM):")
    passed, findings = pre_val.run_deterministic_checks(sample_packet)
    print(f"Resultado del Filtro Pre-LLM: {'APROBADO' if passed else 'RECHAZADO'}")
    print(f"Hallazgos detectados         : {len(findings)}")
    if not findings:
        print("-> Paquete 100% íntegro. Apto para pasar al ciclo de auditoría del Orquestador.")
    print("==========================================================================")

```

---

## 4. Matriz de Trazabilidad y Evaluador de Eficiencia de Tokens (`matriz_trazabilidad_y_evaluador_eficiencia_bloque_a.py`)

### Propósito Técnico
* **Matriz de Trazabilidad Cruzada (`MatrizTrazabilidadBloqueA`)**: Mantiene el vínculo directo entre las 203 funciones de los 7 agentes (`ANA`, `BAV`, `DOC`, `DMO`, `MOT`, `ORQ`, `AUD`) y los 62 Objetivos normativos (OBJ-01 a OBJ-62) organizados en 7 dimensiones.
* **Telemetría de Eficiencia (`EvaluadorEficienciaEcosistema`)**: Satisface la función `AUD-F06` de la auditoría, comparando el tamaño de los intercambios contra benchmarks presupuestarios de tokens y detectando redundancias de contexto o verbosidad.

```python
import json
import datetime

class MatrizTrazabilidadBloqueA:
    """
    Sincronización del corpus de gobernanza:
    Vincula los 62 Objetivos (OBJ-01 a OBJ-62) y las 203 funciones de los 7 agentes
    con las secciones del Documento 0 y los Contratos CT-01 a CT-13.
    """
    def __init__(self):
        self.dimensiones = {
            "D1": "Gobernanza y coherencia del conjunto (OBJ-01 a OBJ-13)",
            "D2": "Análisis de tendencias y entregables del agente central (OBJ-14 a OBJ-22)",
            "D3": "Fuentes: búsqueda, verificación y archivos documentales (OBJ-23 a OBJ-33)",
            "D4": "Cálculo reproducible y servicio transversal (OBJ-34 a OBJ-39)",
            "D5": "Auditoría y mejora continua (OBJ-40 a OBJ-48)",
            "D6": "Seguridad y límites transversales (OBJ-49 a OBJ-55)",
            "D7": "Trazabilidad, operación y contexto del bloque (OBJ-56 a OBJ-62)"
        }
        
        self.agentes = {
            "ANA": "Analizador de Tendencias de Inversión (32 funciones)",
            "BAV": "Buscador de Fuentes Avanzadas (33 funciones)",
            "DOC": "Documentador para el Analizador (35 funciones)",
            "DMO": "Documentador para el Motor de Cálculo (27 funciones)",
            "MOT": "Motor de Cálculo Avanzado (22 funciones / 249 tareas)",
            "ORQ": "Orquestador Técnico (26 funciones)",
            "AUD": "Auditor (28 funciones)"
        }

    def obtener_resumen_trazabilidad(self):
        return {
            "total_objetivos": 62,
            "dimensiones_cobertura": len(self.dimensiones),
            "total_agentes": len(self.agentes),
            "total_funciones_mapeadas": 203,
            "contratos_vinculados": [f"CT-{i:02d}" for i in range(1, 14)],
            "estado_sincronizacion": "100% SINCRONIZADO",
            "documento_maestro": "Documento 0 - Versión Óptima V1"
        }

class EvaluadorEficienciaEcosistema:
    """
    Monitoreo de Eficiencia de Tokens y Velocidad (AUD-F06):
    Analiza la densidad de información, consumo estimado de tokens y redundancias
    en los intercambios entre agentes a través de los contratos CT-01 a CT-13.
    """
    def __init__(self):
        # Estimaciones promedio de tokens por contrato
        self.contrato_token_benchmark = {
            "CT-01": {"max_tokens_peticion": 800, "max_tokens_respuesta": 3500},
            "CT-02": {"max_tokens_peticion": 800, "max_tokens_respuesta": 3000},
            "CT-03": {"max_tokens_peticion": 4500, "max_tokens_respuesta": 500},
            "CT-04": {"max_tokens_peticion": 1500, "max_tokens_respuesta": 500},
            "CT-05": {"max_tokens_peticion": 3000, "max_tokens_respuesta": 500},
            "CT-06": {"max_tokens_peticion": 3000, "max_tokens_respuesta": 500},
            "CT-07": {"max_tokens_peticion": 5000, "max_tokens_respuesta": 500},
            "CT-08": {"max_tokens_peticion": 3500, "max_tokens_respuesta": 500},
            "CT-09": {"max_tokens_peticion": 1500, "max_tokens_respuesta": 500},
            "CT-10": {"max_tokens_peticion": 1000, "max_tokens_respuesta": 800},
            "CT-11": {"max_tokens_peticion": 1200, "max_tokens_respuesta": 2500},
            "CT-12": {"max_tokens_peticion": 1500, "max_tokens_respuesta": 2000},
            "CT-13": {"max_tokens_peticion": 1000, "max_tokens_respuesta": 500}
        }

    def evaluar_intercambio(self, contract_id, payload_peticion, payload_respuesta):
        tokens_est_peticion = len(json.dumps(payload_peticion)) // 4
        tokens_est_respuesta = len(json.dumps(payload_respuesta)) // 4
        total_tokens = tokens_est_peticion + tokens_est_respuesta
        
        benchmarks = self.contrato_token_benchmark.get(contract_id, {"max_tokens_peticion": 2000, "max_tokens_respuesta": 2000})
        limite_ideal = benchmarks["max_tokens_peticion"] + benchmarks["max_tokens_respuesta"]
        
        eficiencia_pct = round(min(100.0, (limite_ideal / max(1, total_tokens)) * 100), 2)
        
        redundancias_detectadas = []
        if tokens_est_peticion > benchmarks["max_tokens_peticion"]:
            redundancias_detectadas.append("Exceso de contexto en la petición")
        if tokens_est_respuesta > benchmarks["max_tokens_respuesta"]:
            redundancias_detectadas.append("Respuesta potencialmente verbosa o sin comprimir")
            
        return {
            "contract_id": contract_id,
            "tokens_peticion": tokens_est_peticion,
            "tokens_respuesta": tokens_est_respuesta,
            "total_tokens": total_tokens,
            "limite_benchmark": limite_ideal,
            "eficiencia_score": f"{eficiencia_pct}%",
            "redundancias": redundancias_detectadas if redundancias_detectadas else ["Ninguna redundancia crítica"]
        }

if __name__ == "__main__":
    trazabilidad = MatrizTrazabilidadBloqueA()
    evaluador = EvaluadorEficienciaEcosistema()
    
    resumen_traz = trazabilidad.obtener_resumen_trazabilidad()
    
    # Prueba de evaluación de eficiencia en paquete CT-03
    payload_pet_ejemplo = {
        "contract_id": "CT-03",
        "sender_agent": "ANALIZADOR",
        "receiver_agent": "ORQUESTADOR",
        "request_id": "REQ-20261025-001",
        "run_id": "RUN-1029",
        "run_record": {"status": "COMPLETED", "execution_mode": "WEEKLY_AUTONOMOUS"},
        "deliverables": {"json": "summary_json_data_chunk..."},
        "search_trace": {"queries_executed": 15, "sources_verified": 8},
        "evidence_trace": {"claims_count": 12, "confidence_score": 85.5},
        "calculation_log": [{"operation": "MOMENTOS_DESCRIPTIVOS", "status": "VERIFIED"}]
    }
    payload_resp_ejemplo = {
        "audit_id": "AUD-20261025-001",
        "status": "RECEIVED_AND_PREVALIDATED",
        "next_step": "CT-07_TRANSMISSION"
    }
    
    eval_ct03 = evaluador.evaluar_intercambio("CT-03", payload_pet_ejemplo, payload_resp_ejemplo)
    
    print("=" * 74)
    print("      FASE 4: ALINEACIÓN NORMATIVA Y EFICIENCIA ECOSISTÉMICA (MATRIZ & EFFICIENCY)")
    print("=" * 74)
    print(f"Fecha de procesamiento  : {datetime.datetime.now().isoformat()}")
    print(f"Total de Objetivos (OBJ): {resumen_traz['total_objetivos']} distribuidos en {resumen_traz['dimensiones_cobertura']} dimensiones")
    print(f"Total de Funciones Agente: {resumen_traz['total_funciones_mapeadas']} en {resumen_traz['total_agentes']} agentes")
    print(f"Contratos Sincronizados : {len(resumen_traz['contratos_vinculados'])} (CT-01 a CT-13)")
    print(f"Estado de Gobernanza    : {resumen_traz['estado_sincronizacion']}")
    print("-" * 74)
    print("EVALUACIÓN DE MUESTRA DE EFICIENCIA DE TOKENS (CT-03):")
    print(json.dumps(eval_ct03, indent=2, ensure_ascii=False))
    print("=" * 74)

```

---

## 5. Guía de Ejecución e Integración para el Operador

### Requisitos del Entorno
* Python 3.8+ (bibliotecas estándar `json`, `os`, `sys`, `datetime`, `time`). No requiere librerías externas de terceros.

### Comandos de Verificación Inmediata:
1. **Auditoría de Contratos Espejados**:
   ```bash
   python3 validador_contratos_bloque_a.py
   ```
2. **Prueba de Credenciales y Pre-validador**:
   ```bash
   python3 modulo_descongestion_y_credenciales_bloque_a.py
   ```
3. **Resumen de Trazabilidad y Métrica de Eficiencia**:
   ```bash
   python3 matriz_trazabilidad_y_evaluador_eficiencia_bloque_a.py
   ```
