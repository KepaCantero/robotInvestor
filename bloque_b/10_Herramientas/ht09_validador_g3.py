#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HT-09 · Validador determinista G3 del Bloque B (implementación de referencia).

Bloque B · Robot Investor · V2.0 (actualizado V2.1, 03/11/2026) · Subordinada al Documento 0 del Bloque B, óptima V2.1
(secciones 1, 4.4, 7.4 F8–F9, 7.10–7.13, 8.3, 8.6–8.10, 9, 14, 17 y Anexos A, A.2, B y D) y al catálogo G3 del «Plan de
pruebas del Bloque B - V2.0» actualizado V2.1 (sección 3: `G3B-EST/DAT/MET/CON/SEL/TMP/ENT-nn`).

V2.1 añade las 19 comprobaciones del grupo 8 del catálogo (las del prompt del Orquestador): G3B-EST-11…14,
G3B-MET-18…22, G3B-CON-19…21, G3B-SEL-16…18, G3B-TMP-05…06 y G3B-ENT-11…12 (107 en total), con los perfiles
reducidos PAR (`validar_informe_parada`, B.15) y CIC (`validar_informe_seguimiento`, B.14). G3B-CON-10 se amplía al
horizonte principal por tipo de objeto (8.6).

Valida un `paquete_analisis_mercado` (B.9, con `paquete_para_bloque_C` B.10 y `plan_de_seguimiento` B.11) en la pasada
PAQUETE_SINTESIS (F8) y, si se le pasan los entregables, en la pasada FIDELIDAD_ENTREGABLES (F9). Cada comprobación del
catálogo tiene resultado PASA · FALLA · NO_APLICA (con motivo; NO_APLICA nunca cuenta como PASA) y clase fija B
(bloqueante) o W (advertencia). Dictamen: BLOQUEADO si falla alguna B; APTO_CON_ADVERTENCIAS si falla alguna W; APTO
en otro caso.

Comprobaciones que dependen de insumos opcionales (se evalúan solo si se proporcionan): extracto de F2/RC (`f2`) para
G3B-DAT-02/05/10/13; parámetros de F10 (`parametros_f10`) para G3B-EST-04 y G3B-MET-02; rutas de los entregables para
G3B-EST-08; anexo XLSX para G3B-ENT-07; entregables para G3B-ENT-*. Las comprobaciones **manuales** del Orquestador
(no deterministas con estos insumos) se devuelven como NO_APLICA con motivo «manual»: G3B-EST-02, G3B-DAT-09,
G3B-DAT-11, G3B-DAT-14 y G3B-MET-13 (ver `MANUALES`).

Sin consumo de modelo de lenguaje. Solo biblioteca estándar (importa ht03_puntuaciones y ht07_legibilidad del mismo
directorio; `jsonschema` y `openpyxl` son opcionales). Códigos de salida: 0 APTO, 1 APTO_CON_ADVERTENCIAS, 2 BLOQUEADO,
3 error de entrada. Estado de madurez (R26): implementada (referencia), pruebas unitarias superadas; integrada en el
ejecutor `bloque_b`.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from typing import Any, Dict, Iterable, List, Optional, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ht03_puntuaciones as ht03  # noqa: E402
import ht07_legibilidad as ht07  # noqa: E402

VERSION = "2.1"
TIPOS = ht03.TIPOS_ACTIVO
DIMS = ht03.DIMENSIONES

# Catálogo G3 del Plan de pruebas (ID: nombre, clase, pasada). Solo lo amplía el operador (tipo 3).
CATALOGO: Dict[str, tuple] = {
    "G3B-EST-01": ("Esquema `paquete_analisis_mercado`", "B", "F8, F9"),
    "G3B-EST-02": ("Campos comunes de mensaje", "B", "F8"),
    "G3B-EST-03": ("Identificadores", "B", "F8"),
    "G3B-EST-04": ("Versión de metodología", "B", "F8"),
    "G3B-EST-05": ("Datos protegidos", "B", "F8, F9"),
    "G3B-EST-06": ("Instrucciones incrustadas", "B", "F8, F9"),
    "G3B-EST-07": ("Vocabularios controlados", "B", "F8"),
    "G3B-EST-08": ("Nombres y carpetas de entregables", "W", "F9"),
    "G3B-EST-09": ("Esquema `paquete_para_bloque_C`", "B", "F8"),
    "G3B-EST-10": ("Esquema `plan_de_seguimiento`", "B", "F8"),
    "G3B-DAT-01": ("Cifras con origen", "B", "F8"),
    "G3B-DAT-02": ("Afirmaciones trazadas", "B", "F8"),
    "G3B-DAT-03": ("Etiqueta epistémica", "B", "F8, F9"),
    "G3B-DAT-04": ("Clase de cifra", "B", "F8"),
    "G3B-DAT-05": ("Declaración de datos completa", "B", "F8"),
    "G3B-DAT-06": ("Frescura (PA2)", "B", "F8"),
    "G3B-DAT-07": ("Fechas válidas", "B", "F8"),
    "G3B-DAT-08": ("Fecha de corte única", "B", "F9"),
    "G3B-DAT-09": ("Unidades y divisas", "B", "F8"),
    "G3B-DAT-10": ("Evidencia viva", "B", "F8"),
    "G3B-DAT-11": ("Raíces y corroboración (PA1)", "B", "F8"),
    "G3B-DAT-12": ("Herencia del Bloque A (R31)", "B", "F8"),
    "G3B-DAT-13": ("Artefactos presentes", "B", "F8"),
    "G3B-DAT-14": ("Discrepancias (PA6)", "B", "F8"),
    "G3B-MET-01": ("A, E y C reconstruibles", "B", "F8"),
    "G3B-MET-02": ("Pesos vigentes", "B", "F8"),
    "G3B-MET-03": ("Banda marginal", "B", "F8"),
    "G3B-MET-04": ("Tope por saturación narrativa", "B", "F8"),
    "G3B-MET-05": ("Doce dimensiones (PA3, R17)", "B", "F8"),
    "G3B-MET-06": ("Pesos efectivos y desviaciones", "W", "F8"),
    "G3B-MET-07": ("Hipótesis competidoras (PA4)", "B", "F8"),
    "G3B-MET-08": ("Tesis falsable", "B", "F8"),
    "G3B-MET-09": ("Protocolo cuantitativo", "B", "F8"),
    "G3B-MET-10": ("Escenarios", "B", "F8"),
    "G3B-MET-11": ("Referencias ingenuas", "W", "F8"),
    "G3B-MET-12": ("Perfiles coherentes", "W", "F8"),
    "G3B-MET-13": ("Madurez declarada", "B", "F8, F9"),
    "G3B-MET-14": ("Despliegue estructural", "B", "F8"),
    "G3B-MET-15": ("Cambios grandes", "W", "F8"),
    "G3B-MET-16": ("Puertas de continuidad", "W", "F8"),
    "G3B-MET-17": ("Régimen", "W", "F8"),
    "G3B-CON-01": ("Puertas PA1–PA8", "B", "F8"),
    "G3B-CON-02": ("Veredicto coherente", "B", "F8"),
    "G3B-CON-03": ("Contenido del veredicto", "B", "F8"),
    "G3B-CON-04": ("Campos de decisión", "B / W", "F8"),
    "G3B-CON-05": ("Resultado del análisis", "B", "F8"),
    "G3B-CON-06": ("Refutación de la tesis (R18)", "B", "F8"),
    "G3B-CON-07": ("Autocrítica", "B", "F8"),
    "G3B-CON-08": ("Probabilidad certificada (R13)", "B", "F8, F9"),
    "G3B-CON-09": ("Banda sin certificado", "B", "F8, F9"),
    "G3B-CON-10": ("Horizontes aplicables", "B", "F8"),
    "G3B-CON-11": ("Pronósticos congelables", "B", "F8"),
    "G3B-CON-12": ("Mapa de cobertura", "B", "F8"),
    "G3B-CON-13": ("Cuatro evaluaciones", "B", "F8"),
    "G3B-CON-14": ("Preguntas respondidas", "B", "F8"),
    "G3B-CON-15": ("No asesoramiento", "B", "F8, F9"),
    "G3B-CON-16": ("Frontera con los Bloques C", "B", "F8, F9"),
    "G3B-CON-17": ("Historial de aciertos", "W", "F8"),
    "G3B-CON-18": ("Vocabulario de confianza", "W", "F8"),
    "G3B-SEL-01": ("Universo declarado", "B", "F8"),
    "G3B-SEL-02": ("PC1–PC4", "B", "F8"),
    "G3B-SEL-03": ("S reconstruible (PC7)", "B", "F8"),
    "G3B-SEL-04": ("Incertidumbre del ranking (PC6)", "B", "F8"),
    "G3B-SEL-05": ("Veredicto del candidato", "B", "F8"),
    "G3B-SEL-06": ("Top-N sin relleno (R21)", "B", "F8"),
    "G3B-SEL-07": ("Diversidad", "B", "F8"),
    "G3B-SEL-08": ("Apuestas independientes", "W", "F8"),
    "G3B-SEL-09": ("Asignación de tipo", "B", "F8"),
    "G3B-SEL-10": ("Marco de invertibilidad", "B", "F8"),
    "G3B-SEL-11": ("Refutación de candidatos (PC5)", "B", "F8"),
    "G3B-SEL-12": ("Traducción de rasgos", "W", "F8"),
    "G3B-SEL-13": ("Encargos C.x coherentes", "B", "F8"),
    "G3B-SEL-14": ("Supervivencia", "W", "F8"),
    "G3B-SEL-15": ("Pureza (PC2)", "B", "F8"),
    "G3B-TMP-01": ("Tiempo y consumo", "W", "F8"),
    "G3B-TMP-02": ("Autorización registrada (R20)", "B", "F8"),
    "G3B-TMP-03": ("Alcance reducido declarado (R23)", "B", "F8"),
    "G3B-TMP-04": ("Estados degradados", "B", "F8"),
    "G3B-ENT-01": ("Legibilidad del informe visual", "B", "F9"),
    "G3B-ENT-02": ("Fidelidad", "B", "F9"),
    "G3B-ENT-03": ("Coherencia entre entregables", "B", "F9"),
    "G3B-ENT-04": ("Informe visual", "B", "F9"),
    "G3B-ENT-05": ("Informe técnico completo", "B", "F9"),
    "G3B-ENT-06": ("Memorando", "W", "F9"),
    "G3B-ENT-07": ("Anexo de datos", "B", "F9"),
    "G3B-ENT-08": ("Accesibilidad", "W", "F9"),
    "G3B-ENT-09": ("Reservas y limitaciones visibles", "B", "F9"),
    "G3B-ENT-10": ("Jerga explicada", "W", "F9"),
    # V2.1 (grupo 8 del catálogo del Orquestador; Plan de pruebas, sección 3, actualizado V2.1)
    "G3B-EST-11": ("Esquema `mapa_cadena_valor`", "B", "F8, F9"),
    "G3B-EST-12": ("Esquema `informe_parada`", "B", "PAR"),
    "G3B-EST-13": ("Esquema `informe_seguimiento`", "B", "CIC"),
    "G3B-EST-14": ("Consultas al Broker", "B", "F8, PAR, CIC"),
    "G3B-MET-18": ("Puertas de viabilidad (R33)", "B", "F8, PAR"),
    "G3B-MET-19": ("PCB y AE reconstruibles", "B", "F8"),
    "G3B-MET-20": ("Desglose jerárquico", "W", "F8"),
    "G3B-MET-21": ("Lista de comprobación profesional", "B", "F8, F9"),
    "G3B-MET-22": ("Horizonte H5", "B", "F8, F9"),
    "G3B-CON-19": ("Contenido del informe de parada", "B", "PAR"),
    "G3B-CON-20": ("Continuación forzada", "B", "F8, F9"),
    "G3B-CON-21": ("Supuestos aplicados", "B", "F8, F9, PAR, CIC"),
    "G3B-SEL-16": ("`eslabon_id` en todo candidato", "B", "F8, CIC"),
    "G3B-SEL-17": ("Mejores opciones por eslabón", "B", "F8"),
    "G3B-SEL-18": ("Emergentes", "B", "F8, F9"),
    "G3B-TMP-05": ("Tiempo por capa", "B", "F8, PAR"),
    "G3B-TMP-06": ("Ciclo N1-SEG", "B", "CIC"),
    "G3B-ENT-11": ("Entregable 6 completo", "B", "F9"),
    "G3B-ENT-12": ("Tablas por eslabón del informe visual", "B", "F9"),
}
MANUALES = {
    "G3B-EST-02": "manual: campos comunes de los mensajes CT-B integrados (los comprueba el Orquestador en HA)",
    "G3B-DAT-09": "manual: unidades y divisas de cada cifra frente a su DAT-B",
    "G3B-DAT-11": "manual: recuento de raíces independientes frente a F2 (Curador)",
    "G3B-DAT-14": "manual: discrepancias DSC-B materiales frente a F2",
    "G3B-MET-13": "manual: estado de madurez de cada método frente a RC y CC",
}

ENUMS = {
    "tipo_objeto": ht03.TIPOS_OBJETO, "veredicto": ht03.VEREDICTOS_AMBITO,
    "veredicto_candidato": ("PRIORITARIO_PARA_C", "SECUNDARIO"),
    "resultado_del_analisis": ("CONCLUYENTE", "PARCIAL", "NO_CONCLUYENTE", "DETENIDO_EN_PUERTA", "BLOQUEADO"),
    "siguiente_paso_sugerido": ("ENVIAR_CANDIDATOS_A_C", "PROFUNDIZAR_EN_B", "VIGILAR", "DESCARTAR"),
    "relevancia_decisional": ("ALTA", "MEDIA", "BAJA"), "horizonte": ht03.HORIZONTES, "nivel": ("N1", "N2", "N3", "PERS"),
    "profundidad": ("P0", "P1", "P2", "P3"), "etiqueta": ("[HECHO]", "[INTERPRETACIÓN]", "[ESPECULACIÓN]"),
    "clase_cifra": ("determinista", "estimacion_estadistica", "juicio_experto"),
    "estado_hipotesis": ("confirmada", "debilitada", "indeterminada", "invalidada"),
    "estado_regimen": ("definido", "mixto", "incierto", "en_transicion"), "fuerza": ("fuerte", "moderada", "debil"),
    "motivo_exclusion": ht03.MOTIVOS_EXCLUSION, "veredicto_tesis": ("robusta", "fragil", "refutada"),
    "confianza_verbal": ("establecido", "probable", "especulativo", "en disputa"),
}
BANDAS_VERBALES = ("muy probable", "más probable que no", "incierto", "poco probable", "muy poco probable")
# Anexo A.2: formatos de identificadores
RE_IDS = {
    "cns_id": r"CNS-B-\d{4}-\d{4,}", "seg_id": r"SEG-B-\d{4}-\d{4,}", "ciclo_id": r"CIC-B-\d{4}-\d{4,}-\d{2,}",
    "emg_id": r"EMG-B-\d{4}-\d{4,}",
    "pet_id": r"PET-B-\d{4}-\d{4}", "run_id": r"RUN-B-\d{4}-\d{4}(-\d{2})?", "rec_id": r"REC-B-\d{4}-\d{4}",
    "cand_id": r"CAND-B-\d{4}-\d{4,}", "prg_id": r"PRG-B-\d{4}-\d{4,}", "hip_id": r"HIP-B-\d{4}-\d{4,}(-\d+)?",
    "obj_id": r"OBJ-B-\d{4}-\d{4,}", "sig_id": r"SIG-\d{4}-\d{4,}(-\d+)?", "aut_id": r"AUT[CS]?-B-\d{4}-\d{4,}",
    "mkt_id": r"MKT-B-\d{4}-\d{4,}", "rgm_id": r"RGM-B-\d{4}-\d{4,}",
}
LIMITE_TOP = {"N1": (3, 0), "N2": (5, 2), "N3": (10, 5)}
MIN_HIPOTESIS_COMPETIDORAS = {"N1": 1, "N2": 2, "N3": 2, "PERS": 1}
ANTIGUEDAD_MERCADO_DIAS = {"H1": 1, "H2": 3, "H3": 7, "H4": 30, "H5": 90}
CLAVES_MAPA = ("directas", "indirectas", "perdedores_sistematicos", "investigado", "excluido_con_motivo",
               "vigilancia_informativa", "vigilancia_pre_salida")
PERFIL_OBJETO = {"SECTOR": "PERF-B-SECT", "TEMATICA": "PERF-B-TEMA", "MERCADO_GEOGRAFICO": "PERF-B-GEO",
                 "SEGMENTO_DE_CLASE": "PERF-B-SEGM", "ESTRATEGIA_FACTOR": "PERF-B-FACT", "CADENA_DE_VALOR": "PERF-B-CADENA"}
TABLA_HORIZONTES = {  # 8.6 · por tipo de activo (H1…H5)
    "RV": ("LIMITADO", "SI", "SI", "SI", "SI"), "IDX": ("LIMITADO", "SI", "SI", "SI", "SI"),
    "RF": ("LIMITADO", "SI", "SI", "SI", "LIMITADO"), "DIV": ("SI", "SI", "SI", "LIMITADO", "LIMITADO"),
    "CRI": ("SI", "SI", "SI", "LIMITADO", "LIMITADO"), "TCV": ("SI", "SI", "SI", "LIMITADO", "LIMITADO"),
    "MP": ("SI", "SI", "SI", "SI", "LIMITADO"), "FON": ("NO", "LIMITADO", "SI", "SI", "SI"),
    "INM": ("NO", "LIMITADO", "SI", "SI", "SI"), "DER": ("SI", "SI", "SI", "NO", "NO"),
    "ALT": ("NO", "NO", "LIMITADO", "SI", "SI"), "MON": ("LIMITADO", "SI", "SI", "NO", "NO"),
}
TABLA_HORIZONTES_OBJETO = {  # 8.6 · por tipo de objeto (H1…H5)
    "SECTOR": ("LIMITADO", "SI", "SI", "SI", "SI"), "TEMATICA": ("NO", "LIMITADO", "SI", "SI", "SI"),
    "MERCADO_GEOGRAFICO": ("LIMITADO", "SI", "SI", "SI", "SI"), "SEGMENTO_DE_CLASE": ("SI", "SI", "SI", "SI", "LIMITADO"),
    "ESTRATEGIA_FACTOR": ("LIMITADO", "SI", "SI", "SI", "LIMITADO"), "CADENA_DE_VALOR": ("NO", "LIMITADO", "SI", "SI", "SI"),
}
RE_ESLABON = r"ESL-\d{2}(\.\d{2}){0,2}(\.[a-z])?"
TIPOS_CONSULTA = ("ACLARACION_ALCANCE", "DATO_O_DOCUMENTO", "PREFERENCIA_O_CRITERIO", "CONFIRMACION_SUPUESTO", "OTRA")
ITEMS_N1 = (1, 4, 15, 16, 17, 18)       # 8.10: ítems marcados (N1)
ESTADOS_LISTA = ("TRATADO", "NO_APLICABLE", "LAGUNA")
AVISO_TABLAS_ESLABON = "Activos que el análisis ha estudiado; no son recomendaciones; tu Broker decide"
OBLIGATORIOS = ("pet_id", "run_ids", "rec_id", "fecha", "data_cutoff", "methodology_version", "origen", "ambito",
                "estrategia", "dimensiones", "despliegue_estructural", "proyecciones", "regimen", "tesis",
                "evaluaciones_separadas", "puntuaciones", "puertas_ambito", "veredicto", "escenarios", "pronosticos",
                "pronosticos_detalle", "riesgos", "riesgo_1a5", "catalizadores", "invalidacion", "refutacion",
                "candidatos_por_tipo", "apuestas_independientes", "paquete_para_bloque_C", "plan_de_seguimiento",
                "mapa_cobertura", "historial_aciertos", "tiempo_consumo", "preguntas_sugeridas", "limitaciones",
                "reservas_auditoria", "mapa_cadena_valor", "capas", "consultas_broker", "lista_profesional")
HOJAS_ANEXO = ("Leeme", "Puntuaciones", "Cifras", "Fuentes", "Escenarios", "Sensibilidades", "Pronosticos", "Artefactos",
               "Eslabones", "Opciones_eslabon", "Emergentes")
RE_SECRETO = re.compile(r"(sk-ant-[A-Za-z0-9_\-]{8,}|sk-[A-Za-z0-9_\-]{16,}|AKIA[0-9A-Z]{16}|api[_-]?key\s*[:=]\s*\S{6,}|"
                        r"bearer\s+[A-Za-z0-9\-_.=]{16,}|contrase(?:ñ|n)a\s*[:=]\s*\S+|password\s*[:=]\s*\S+|"
                        r"-----BEGIN [A-Z ]*PRIVATE KEY-----)", re.IGNORECASE)
RE_PERSONAL = re.compile(r"(\b[A-Z]{2}\d{2}(?:\s?\d{4}){4,7}\b|[\w.+-]+@[\w-]+\.[\w.-]+|\b\d{8}[A-HJ-NP-TV-Z]\b|"
                         r"\b[XYZ]\d{7}[A-Z]\b|\+34\s?\d{3}\s?\d{3}\s?\d{3}|\b(mi|tu) cartera\b(?! de (pedidos|proyectos|clientes))|"
                         r"\b(mi|tu) perfil (de riesgo|inversor)\b)",
                         re.IGNORECASE)
RE_INSTRUCCION = re.compile(r"(ignora (las|todas las|tus) instrucciones|ignore (all|previous) instructions|system prompt|"
                            r"ejecuta (la herramienta|el comando)|act[uú]a como|you are now|nuevas instrucciones:|"
                            r"<\s*/?\s*(system|tool_use)\s*>)", re.IGNORECASE)
RE_ASESORAMIENTO = re.compile(r"(te recomendamos (comprar|vender)|recomendamos (comprar|vender)|deber[ií]as (comprar|vender|invertir)|"
                              r"\bcompre\b|\bvenda\b|entre ya|compra ya|vende ya|tama[ñn]o de (la )?posici[oó]n|"
                              r"asesoramiento personalizado para ti)", re.IGNORECASE)
RE_FRONTERA_C = re.compile(r"(precio objetivo|target price|valor razonable de la acci[oó]n es)", re.IGNORECASE)
RE_ISIN = re.compile(r"\b[A-Z]{2}[A-Z0-9]{9}[0-9]\b")
AVISO_VISUAL = "Esto no es una recomendación personal"
SEMAFORO = {"INVERTIR": "verde", "INVERTIR_ESCALONADO": "verde-claro", "VIGILAR": "ambar", "DESCARTAR": "gris"}
SECCIONES_TECNICO = 16


class ErrorEntrada(ValueError):
    pass


class Registro:
    def __init__(self) -> None:
        self.fallos: Dict[str, List[Dict]] = {}
        self.evaluadas: set = set()
        self.no_aplica: Dict[str, str] = {}

    def ok(self, *codigos: str) -> None:
        for c in codigos:
            if c not in CATALOGO:
                raise KeyError(c)
            self.evaluadas.add(c)

    def falla(self, codigo: str, msg: str, clase: Optional[str] = None) -> None:
        self.ok(codigo)
        cl = clase or CATALOGO[codigo][1]
        self.fallos.setdefault(codigo, []).append({"clase": "B" if cl.startswith("B") else "W", "detalle": msg})

    def na(self, codigo: str, motivo: str) -> None:
        if codigo not in self.evaluadas:
            self.no_aplica[codigo] = motivo

    def resultados(self) -> List[Dict]:
        out = []
        for c, (nombre, clase, pasada) in CATALOGO.items():
            if c in self.fallos:
                cls = "B" if any(f["clase"] == "B" for f in self.fallos[c]) else "W"
                out.append({"id": c, "nombre": nombre, "clase": clase, "pasada": pasada, "resultado": "FALLA",
                            "clase_fallo": cls, "detalles": [f["detalle"] for f in self.fallos[c]]})
            elif c in self.evaluadas:
                out.append({"id": c, "nombre": nombre, "clase": clase, "pasada": pasada, "resultado": "PASA", "detalles": []})
            else:
                motivo = MANUALES.get(c) or self.no_aplica.get(c) or "insumo no proporcionado en esta pasada"
                out.append({"id": c, "nombre": nombre, "clase": clase, "pasada": pasada, "resultado": "NO_APLICA",
                            "detalles": [motivo], "manual": c in MANUALES})
        return out

    def dictamen(self) -> str:
        cls = [f["clase"] for fs in self.fallos.values() for f in fs]
        if "B" in cls:
            return "BLOQUEADO"
        if "W" in cls:
            return "APTO_CON_ADVERTENCIAS"
        return "APTO"


def _vacio(v: Any) -> bool:
    return v is None or v == "" or v == [] or v == {}


def _textos(o: Any) -> Iterable[str]:
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from _textos(v)
    elif isinstance(o, list):
        for v in o:
            yield from _textos(v)


def _fecha(v) -> Optional[dt.date]:
    try:
        return dt.date.fromisoformat(str(v)[:10])
    except (TypeError, ValueError):
        return None


def _ide(clave: str, v: Any) -> bool:
    return bool(re.fullmatch(RE_IDS[clave], str(v or "")))


def candidatos_top(paq: Dict) -> List[Dict]:
    out = []
    for t in TIPOS:
        d = (paq.get("candidatos_por_tipo") or {}).get(t) or {}
        if d.get("aplicable"):
            for c in d.get("top_n") or []:
                out.append({**c, "_tipo": t})
    return out


def opciones_adicionales(paq: Dict) -> Dict[str, Dict]:
    """Opciones de las tablas por eslabón que no están en el top-N de su tipo (9.13), con su eslabón en «_eslabon»."""
    out = {}
    for e in ((paq.get("mapa_cadena_valor") or {}).get("eslabones") or []):
        for o in e.get("opciones") or []:
            if not o.get("en_top_n_tipo"):
                out[o.get("cand_id")] = {**o, "_eslabon": e.get("eslabon_id")}
    return out


# ==============================================================================================================
# EST · Estructura y seguridad
# ==============================================================================================================
def _est(p: Dict, R: Registro, esquema: Optional[Dict], f10: Optional[Dict]) -> None:
    R.ok("G3B-EST-01", "G3B-EST-03", "G3B-EST-07", "G3B-EST-09", "G3B-EST-10")
    for k in OBLIGATORIOS:
        if k not in p:
            R.falla("G3B-EST-01", f"Falta el campo obligatorio «{k}»")
    cpt = p.get("candidatos_por_tipo") or {}
    for t in TIPOS:
        d = cpt.get(t)
        if d is None:
            R.falla("G3B-EST-01", f"candidatos_por_tipo sin la clave {t}")
        elif d.get("aplicable") is False and _vacio(d.get("motivo")):
            R.falla("G3B-EST-01", f"{t} no aplicable sin motivo")
        elif d.get("aplicable") not in (True, False):
            R.falla("G3B-EST-01", f"{t}: «aplicable» debe ser true o false")
    for t in cpt:
        if t not in TIPOS:
            R.falla("G3B-EST-07", f"Tipo de activo desconocido: {t}")
    if esquema is not None:
        try:
            import jsonschema  # type: ignore
            for e in sorted(jsonschema.Draft202012Validator(esquema).iter_errors(p), key=lambda e: list(e.path))[:25]:
                ruta = "/".join(map(str, e.path)) or "(raíz)"
                cod = "G3B-EST-09" if ruta.startswith("paquete_para_bloque_C") else \
                    "G3B-EST-10" if ruta.startswith("plan_de_seguimiento") else "G3B-EST-01"
                R.falla(cod, f"Esquema: {ruta}: {e.message[:200]}")
        except ImportError:
            pass
    # Identificadores (A.2) y duplicados
    for k in ("pet_id", "rec_id"):
        if not _ide(k, p.get(k)):
            R.falla("G3B-EST-03", f"{k} con formato inválido: {p.get(k)!r}")
    for r in p.get("run_ids") or []:
        if not _ide("run_id", r):
            R.falla("G3B-EST-03", f"run_id con formato inválido: {r!r} (RUN-B-AAAA-NNNN-rr)")
    for x in p.get("pronosticos") or []:
        if not _ide("prg_id", x):
            R.falla("G3B-EST-03", f"PRG-B con formato inválido: {x!r}")
    ids_cand = [c.get("cand_id") for c in candidatos_top(p)]
    for c in ids_cand:
        if not _ide("cand_id", c):
            R.falla("G3B-EST-03", f"cand_id con formato inválido: {c!r}")
    if len(ids_cand) != len(set(ids_cand)):
        R.falla("G3B-EST-03", "cand_id duplicado bajo dos objetos")
    for a in (p.get("tiempo_consumo") or {}).get("autorizaciones") or []:
        if not _ide("aut_id", a):
            R.falla("G3B-EST-03", f"Autorización con formato inválido: {a!r}")
    sin_origen = {k: v for k, v in p.items() if k != "origen"}
    for m in re.findall(r"\b(?:OPP|CLM|PRG|CALC)-\d{4}-\d{4}\b", json.dumps(sin_origen, ensure_ascii=False)):
        R.falla("G3B-EST-03", f"Identificador del Bloque A {m} usado fuera de «origen»")
    if f10 and f10.get("methodology_version"):
        R.ok("G3B-EST-04")
        if str(p.get("methodology_version")) != str(f10["methodology_version"]):
            R.falla("G3B-EST-04", f"methodology_version {p.get('methodology_version')} ≠ F10 {f10['methodology_version']}")
    else:
        R.na("G3B-EST-04", "sin extracto de F10 (parametros_f10)")
    # Vocabularios (D.5)
    amb = p.get("ambito") or {}
    v = p.get("veredicto") or {}
    est = p.get("estrategia") or {}
    chequeos = [("tipo_objeto", amb.get("tipo_objeto")), ("veredicto", v.get("valor")),
                ("resultado_del_analisis", v.get("resultado_del_analisis")), ("nivel", est.get("nivel")),
                ("horizonte", est.get("horizonte_dominante"))]
    for enum, val in chequeos:
        if val not in ENUMS[enum]:
            R.falla("G3B-EST-07", f"{enum} fuera de vocabulario: {val!r}")
    for c in candidatos_top(p):
        if c.get("veredicto") not in ENUMS["veredicto_candidato"]:
            R.falla("G3B-EST-07", f"{c.get('cand_id')}: veredicto fuera de vocabulario {c.get('veredicto')!r}")
    for t, d in cpt.items():
        for m in (d or {}).get("excluidos_por_motivo") or {}:
            if m not in ENUMS["motivo_exclusion"]:
                R.falla("G3B-EST-07", f"{t}: motivo de exclusión no controlado {m!r}")
    for h in (p.get("tesis") or {}).get("hipotesis") or []:
        if h.get("estado") not in ENUMS["estado_hipotesis"]:
            R.falla("G3B-EST-07", f"{h.get('hip_id')}: estado de hipótesis fuera de vocabulario {h.get('estado')!r}")
    # Encargos C.x (B.10)
    for bloque, lst in (p.get("paquete_para_bloque_C") or {}).items():
        if not re.fullmatch(r"C\.(?:[1-9]|1[0-2])", str(bloque)):
            R.falla("G3B-EST-09", f"Bloque de destino no válido: {bloque!r}")
            continue
        for e in lst or []:
            t = e.get("tipo_activo")
            if t in ht03.BLOQUE_C and (ht03.BLOQUE_C[t] != bloque or e.get("bloque_destino") != bloque):
                R.falla("G3B-EST-09", f"{e.get('cand_id')}: bloque {bloque}/{e.get('bloque_destino')} no corresponde a {t} (2.6)")
            if "no es una valoración individual" not in str(e.get("aviso", "")):
                R.falla("G3B-EST-09", f"{e.get('cand_id')}: falta el aviso del encargo")
            for k in ("cand_id", "pet_id", "rec_id", "instrumento", "puntuacion", "pureza", "preguntas_para_C", "data_cutoff"):
                if _vacio(e.get(k)):
                    R.falla("G3B-EST-09", f"{e.get('cand_id')}: encargo sin «{k}»")
    # Plan de seguimiento (B.11)
    ps = p.get("plan_de_seguimiento") or {}
    if _vacio(ps):
        R.falla("G3B-EST-10", "Falta el plan de seguimiento")
    else:
        if ps.get("rec_id") != p.get("rec_id") or ps.get("pet_id") != p.get("pet_id"):
            R.falla("G3B-EST-10", "rec_id/pet_id del plan no coinciden con el paquete")
        sen = ps.get("senales") or []
        if not sen and v.get("valor") != "DESCARTAR":
            R.falla("G3B-EST-10", "Plan sin señales")
        for s in sen:
            sid = s.get("sig_id")
            if not _ide("sig_id", sid):
                R.falla("G3B-EST-10", f"Señal con identificador inválido: {sid!r}")
            if not str(s.get("serie", "")).startswith("HT-01:"):
                R.falla("G3B-EST-10", f"{sid}: sin serie HT-01")
            if _vacio(s.get("umbral_fluctuacion")) or s.get("umbral_revision") is None or s.get("umbral_invalidacion") is None:
                R.falla("G3B-EST-10", f"{sid}: sin los tres umbrales")
            if _vacio(s.get("criterio_cambio_estructural")):
                R.falla("G3B-EST-10", f"{sid}: sin criterio de cambio estructural")
            if _vacio(s.get("frecuencia")):
                R.falla("G3B-EST-10", f"{sid}: sin frecuencia")
            if s.get("direccion") not in ("por_encima", "por_debajo"):
                R.falla("G3B-EST-10", f"{sid}: dirección no válida")
            elif s.get("umbral_revision") is not None and s.get("umbral_invalidacion") is not None:
                ok = (s["umbral_invalidacion"] <= s["umbral_revision"]) if s["direccion"] == "por_debajo" else \
                    (s["umbral_invalidacion"] >= s["umbral_revision"])
                if not ok:
                    R.falla("G3B-EST-10", f"{sid}: el umbral de invalidación llega antes que el de revisión")
        if v.get("valor") != "DESCARTAR" and _vacio(ps.get("condiciones_invalidacion_ambito")):
            R.falla("G3B-EST-10", "Sin condiciones de invalidación del ámbito")
        prgs = set(p.get("pronosticos") or [])
        for x in ps.get("pronosticos_a_resolver") or []:
            if x.get("prg_id") not in prgs or not _fecha(x.get("fecha_resolucion")):
                R.falla("G3B-EST-10", f"{x.get('prg_id')}: pronóstico del plan inexistente o sin fecha de resolución")


def _seguridad(textos: Dict[str, str], R: Registro) -> None:
    R.ok("G3B-EST-05", "G3B-EST-06", "G3B-CON-15", "G3B-CON-16")
    for nombre, t in textos.items():
        if not t:
            continue
        if RE_SECRETO.search(t):
            R.falla("G3B-EST-05", f"{nombre}: posible credencial o clave (no se reproduce) (R10)")
        m = RE_PERSONAL.search(t)
        if m:
            R.falla("G3B-EST-05", f"{nombre}: posible dato personal o referencia a cartera/perfil (R11)")
        m = RE_INSTRUCCION.search(t)
        if m:
            R.falla("G3B-EST-06", f"{nombre}: instrucción incrustada «{m.group(0)}» (R12)")
        for m in RE_ASESORAMIENTO.finditer(t):
            if not re.search(r"\b(no|ni|sin|nunca)\b[^.]{0,40}$", t[max(0, m.start() - 60):m.start()], re.I):
                R.falla("G3B-CON-15", f"{nombre}: lenguaje de orden o asesoramiento «{m.group(0)}» (R4)")
        for m in RE_FRONTERA_C.finditer(t):
            if not re.search(r"\b(no|ni|sin|nunca)\b[^.]{0,40}$", t[max(0, m.start() - 60):m.start()], re.I):
                R.falla("G3B-CON-16", f"{nombre}: «{m.group(0)}»: valoración individual propia de un Bloque C.x (R7)")


# ==============================================================================================================
# DAT · Datos y trazabilidad
# ==============================================================================================================
def _dat(p: Dict, R: Registro, f2: Optional[Dict]) -> None:
    R.ok("G3B-DAT-01", "G3B-DAT-03", "G3B-DAT-04", "G3B-DAT-06", "G3B-DAT-07", "G3B-DAT-12")
    for pr in (p.get("tesis") or {}).get("premisas") or []:
        if not pr.get("evidencia"):
            R.falla("G3B-DAT-01", f"Premisa sin evidencia: {str(pr.get('premisa'))[:60]!r}")
        for x in pr.get("evidencia") or []:
            if not re.fullmatch(r"(CLM|EVD|DAT|CALC)-B-\d{4}-\d{4,}", str(x)):
                R.falla("G3B-DAT-01", f"Evidencia con identificador no válido: {x!r}")
    for c in candidatos_top(p):
        if not re.fullmatch(r"(DAT|CALC)-B-\d{4}-\d{4,}", str((c.get("pureza") or {}).get("fuente") or "")):
            R.falla("G3B-DAT-01", f"{c.get('cand_id')}: pureza sin DAT-B ni CALC-B")
    for lst in (p.get("paquete_para_bloque_C") or {}).values():
        for e in lst or []:
            for m in e.get("metricas_clave") or []:
                if not re.fullmatch(r"(DAT|CALC)-B-\d{4}-\d{4,}", str(m.get("fuente", ""))):
                    R.falla("G3B-DAT-01", f"{e.get('cand_id')}: métrica {m.get('metrica')} sin DAT-B ni CALC-B")
    for d in p.get("dimensiones") or []:
        for n in d.get("notas") or []:
            if n.get("etiqueta") not in ENUMS["etiqueta"]:
                R.falla("G3B-DAT-03", f"{d.get('dim')}: afirmación sin etiqueta válida: {str(n.get('afirmacion'))[:60]!r}")
            if n.get("etiqueta") == "[HECHO]" and re.search(r"\bconsenso\b", str(n.get("afirmacion")), re.I):
                R.falla("G3B-DAT-03", f"{d.get('dim')}: cifra de consenso etiquetada [HECHO]")
            if n.get("etiqueta") == "[HECHO]" and not (n.get("evidencias") or n.get("calculos") or n.get("datos")):
                R.falla("G3B-DAT-01", f"{d.get('dim')}: [HECHO] sin evidencia ni cálculo: {str(n.get('afirmacion'))[:60]!r}")
            tiene_cifra = n.get("contiene_cifra") or bool(re.search(r"\d+(?:[.,]\d+)?\s?(%|M€|€|puntos)", str(n.get("afirmacion"))))
            if tiene_cifra and n.get("clase_cifra") not in ENUMS["clase_cifra"]:
                R.falla("G3B-DAT-04", f"{d.get('dim')}: cifra sin clase: {str(n.get('afirmacion'))[:60]!r}")
    corte, fecha = _fecha(p.get("data_cutoff")), _fecha(p.get("fecha"))
    if corte is None or fecha is None:
        R.falla("G3B-DAT-07", "fecha o data_cutoff no ISO 8601")
    else:
        if corte > fecha:
            R.falla("G3B-DAT-07", f"data_cutoff {corte} posterior a la fecha {fecha}")
        for c in candidatos_top(p):
            fd = _fecha(c.get("fecha_dato"))
            if c.get("fecha_dato") and fd is None:
                R.falla("G3B-DAT-07", f"{c.get('cand_id')}: fecha_dato no ISO")
            elif fd and fd > corte:
                R.falla("G3B-DAT-07", f"{c.get('cand_id')}: fecha_dato {fd} posterior a data_cutoff")
        hz = (p.get("estrategia") or {}).get("horizonte_dominante", "H3")
        for dd in p.get("fechas_datos_criticos") or []:
            f = _fecha(dd.get("fecha"))
            if f is None:
                R.falla("G3B-DAT-07", f"Fecha no válida en {dd.get('dato')}")
                continue
            if f > corte:
                R.falla("G3B-DAT-07", f"{dd.get('dato')}: fecha {f} posterior a data_cutoff")
            lim = ANTIGUEDAD_MERCADO_DIAS.get(hz, 7) if dd.get("clase", "mercado") == "mercado" else \
                (183 if dd.get("clase") == "fundamental" else None)
            if lim is not None and (corte - f).days > lim and not dd.get("justificacion"):
                R.falla("G3B-DAT-06", f"{dd.get('dato')}: {(corte - f).days} días (> {lim}) sin justificación (PA2)")
    o = p.get("origen") or {}
    if o.get("tipo") == "BLOQUE_A" and ("confirmado" not in o or "refutado" not in o):
        R.falla("G3B-DAT-12", "Origen BLOQUE_A sin «confirmado» y «refutado» (R31)")
    for d in p.get("dimensiones") or []:
        for n in d.get("notas") or []:
            if n.get("origen_heredado") in ("PENDIENTE", "SIN_VERIFICAR") and n.get("etiqueta") == "[HECHO]":
                R.falla("G3B-DAT-12", f"{d.get('dim')}: afirmación heredada sin verificar etiquetada [HECHO]")
    if not f2:
        for c in ("G3B-DAT-02", "G3B-DAT-05", "G3B-DAT-10", "G3B-DAT-13"):
            R.na(c, "sin extracto de F2/RC (f2)")
        return
    R.ok("G3B-DAT-02", "G3B-DAT-05", "G3B-DAT-10", "G3B-DAT-13")
    texto = json.dumps(p, ensure_ascii=False)
    conocidos = set(f2.get("ids") or [])
    citados = set(re.findall(r"\b(?:CLM|EVD|DAT|CALC)-B-\d{4}-\d{4,}\b", texto))
    faltan = sorted(x for x in citados - conocidos if not x.startswith("CALC-"))
    if faltan:
        R.falla("G3B-DAT-02", f"Identificadores citados inexistentes en F2: {faltan[:10]}")
    for clm, evds in (f2.get("trazas") or {}).items():
        if clm in citados and not evds:
            R.falla("G3B-DAT-02", f"{clm} sin EVD-B")
    for dat, info in (f2.get("dat") or {}).items():
        if dat in citados and info.get("apta_cifra_critica") is False:
            R.falla("G3B-DAT-05", f"{dat} con declaración incompleta (apta_cifra_critica = false) sostiene una cifra")
    for evd, estado in (f2.get("evd_estados") or {}).items():
        if estado in ("REFUTADA", "FUENTE_RETIRADA") and evd in citados:
            R.falla("G3B-DAT-10", f"{evd} en estado {estado} sin revisión registrada")
    estados_calc = f2.get("calc_estados") or {}
    for calc in sorted(x for x in citados if x.startswith("CALC-")):
        e = estados_calc.get(calc)
        if e is None:
            R.falla("G3B-DAT-13", f"{calc} inexistente en RC")
        elif e in ("RECHAZADO", "FALLIDO", "ACLARACION_NECESARIA"):
            R.falla("G3B-DAT-13", f"{calc} en estado {e}")


# ==============================================================================================================
# MET · Método
# ==============================================================================================================
def _met(p: Dict, R: Registro, f10: Optional[Dict]) -> Dict:
    R.ok("G3B-MET-01", "G3B-MET-03", "G3B-MET-04", "G3B-MET-05", "G3B-MET-06", "G3B-MET-07", "G3B-MET-08",
         "G3B-MET-09", "G3B-MET-10", "G3B-MET-11", "G3B-MET-12", "G3B-MET-14", "G3B-MET-16", "G3B-MET-17")
    est = p.get("estrategia") or {}
    nivel = est.get("nivel", "N2")
    pesos, prof = est.get("pesos_efectivos") or {}, est.get("profundidad") or {}
    if set(pesos) != set(DIMS) or abs(sum(float(x) for x in pesos.values()) - 100) > 0.5:
        R.falla("G3B-MET-06", "Pesos efectivos incompletos o que no suman 100")
    for dv in est.get("desviaciones") or []:
        if abs(int(dv.get("puntos", 0))) > 5 and _vacio(dv.get("motivo")):
            R.falla("G3B-MET-06", f"Desviación de {dv.get('dim')} > ±5 sin motivo sustantivo")
    if f10 and f10.get("pesos"):
        R.ok("G3B-MET-02")
        for k in ("A", "E"):
            ref = (f10["pesos"] or {}).get(k)
            if ref and ref != ht03.PARAMETROS_POR_DEFECTO["pesos"][k]:
                R.falla("G3B-MET-02", f"Pesos de {k} de F10 distintos de los usados por HT-03")
    else:
        R.na("G3B-MET-02", "sin extracto de F10 (parametros_f10)")
    # Doce dimensiones
    dims = {d.get("dim"): d for d in p.get("dimensiones") or []}
    excl = {e.get("dim"): e for e in est.get("exclusiones") or []}
    if prof.get("D9") in ("P0", "P1"):
        R.falla("G3B-MET-05", "D9 por debajo de P2")
    if prof.get("D12") == "P0":
        R.falla("G3B-MET-05", "D12 por debajo de P1")
    orden = ENUMS["profundidad"]
    for d in DIMS:
        if d in excl:
            if _vacio(excl[d].get("motivo")):
                R.falla("G3B-MET-05", f"{d} excluida sin motivo")
            continue
        if d not in dims:
            R.falla("G3B-MET-05", f"{d} ni tratada ni excluida con motivo (PA3)")
            continue
        if _vacio(dims[d].get("notas")):
            R.falla("G3B-MET-05", f"{d} sin notas")
        tratada = dims[d].get("profundidad_tratada")
        if prof.get(d) == "P3" and tratada in ("P0", "P1"):
            R.falla("G3B-MET-05", f"{d} P3 tratada en {tratada}")
        if tratada in orden and prof.get(d) in orden and orden.index(tratada) < orden.index(prof[d]):
            R.falla("G3B-MET-06", f"{d} tratada en {tratada}, por debajo de {prof[d]}")
    # A, E y C
    pu = p.get("puntuaciones") or {}
    des = pu.get("desglose") or {}
    punt: Dict = {}
    try:
        rA = ht03.calcular_A(des.get("A") or {}, bool(pu.get("saturacion_narrativa")))
        rE = ht03.calcular_E(des.get("E") or {})
    except ht03.ErrorEntrada as e:
        R.falla("G3B-MET-01", f"Desglose de A o E no válido: {e}")
        rA = rE = None
    segunda = bool(pu.get("segunda_pasada"))
    if rA and rE:
        if not rA["calculable"] or not rE["calculable"]:
            R.falla("G3B-MET-01", "A o E no calculables (más de dos NA/NE)")
        else:
            for k, r in (("A", rA), ("E", rE)):
                if pu.get(k) != r["total"] and not (segunda and (pu.get(k) or 101) < r["total"]):
                    R.falla("G3B-MET-01", f"{k} = {pu.get(k)} no se reconstruye con HT-03 ({r['total']})")
            ref = p.get("refutacion") or {}
            vt = ref.get("veredicto_tesis")
            if vt in ENUMS["veredicto_tesis"]:
                mod = sum(1 for o in ref.get("objeciones") or [] if o.get("objeto") == "TESIS" and
                          o.get("fuerza") == "moderada" and not o.get("resuelta"))
                rf = ht03.calcular_RF(vt, mod)
                if pu.get("RF") != rf and not (nivel == "N1" and (pu.get("RF") or 101) < rf):
                    R.falla("G3B-MET-01", f"RF = {pu.get('RF')} no coincide con la refutación ({rf})")
            try:
                rc = ht03.calcular_C(rA["total"], rE["total"], int(pu.get("RF", 0)), pu.get("RE"))
                if pu.get("C") != rc["C"] and not (segunda and (pu.get("C") or 101) < rc["C"]):
                    R.falla("G3B-MET-01", f"C = {pu.get('C')} no se reconstruye ({rc['C']})")
            except (ht03.ErrorEntrada, TypeError, ValueError) as e:
                R.falla("G3B-MET-01", f"C no calculable: {e}")
            if pu.get("C") is not None and pu.get("E") is not None and pu["C"] > pu["E"] + 10:
                R.falla("G3B-MET-01", f"C = {pu['C']} supera el tope E + 10")
            punt = {"A": pu.get("A"), "E": pu.get("E"), "C": pu.get("C")}
    if pu.get("saturacion_narrativa") and isinstance((des.get("A") or {}).get("valoracion_expectativas"), (int, float)) \
            and des["A"]["valoracion_expectativas"] > 40:
        R.falla("G3B-MET-04", "Saturación narrativa con «valoración frente a expectativas» > 40")
    u = ht03.PARAMETROS_POR_DEFECTO["umbrales_ambito"]
    umb = {"A": [u["INVERTIR"]["A"], u["INVERTIR_ESCALONADO"]["A"], u["VIGILAR"]["A"]], "E": [u["INVERTIR"]["E"]],
           "C": [u["INVERTIR"]["C"], u["INVERTIR_ESCALONADO"]["C"]]}
    en_banda = [k for k in ("A", "E", "C") if ht03.en_banda_marginal(pu.get(k), umb[k], 5)]
    if en_banda and not segunda and (p.get("puertas_ambito") or {}).get("PA7") == "OK":
        R.falla("G3B-MET-03", f"{', '.join(en_banda)} en banda marginal sin segunda pasada y con PA7 «OK»")
    # Hipótesis y tesis
    t = p.get("tesis") or {}
    hips = t.get("hipotesis") or []
    comp = [h for h in hips if not str(h.get("hip_id", "")).endswith("-0")]
    minimo = MIN_HIPOTESIS_COMPETIDORAS.get(nivel, 2)
    if len(comp) < minimo:
        R.falla("G3B-MET-07", f"{len(comp)} hipótesis competidoras; {nivel} exige {minimo}")
    for h in hips:
        if not _ide("hip_id", h.get("hip_id")):
            R.falla("G3B-MET-07", f"hip_id inválido {h.get('hip_id')!r}")
        if _vacio(h.get("discriminante")):
            R.falla("G3B-MET-07", f"{h.get('hip_id')}: sin discriminante")
        if h.get("estado") not in ENUMS["estado_hipotesis"]:
            R.falla("G3B-MET-07", f"{h.get('hip_id')}: no cerrada")
        if not str(h.get("hip_id", "")).endswith("-0") and (_vacio(h.get("indicador_anticipado")) or _vacio(h.get("invalidacion"))):
            R.falla("G3B-MET-07", f"{h.get('hip_id')}: sin indicador anticipado o invalidación")
    if _vacio(t.get("enunciado")) and not re.search(r"no hay tesis defendible", json.dumps(p, ensure_ascii=False), re.I):
        R.falla("G3B-MET-08", "Sin tesis y sin declaración de «no hay tesis defendible»")
    for pr in t.get("premisas") or []:
        for k in ("evidencia", "comprobacion", "horizonte", "invalidacion"):
            if _vacio(pr.get(k)):
                R.falla("G3B-MET-08", f"Premisa sin «{k}»: {str(pr.get('premisa'))[:50]!r}")
    if not _vacio(t.get("enunciado")) and not t.get("premisas"):
        R.falla("G3B-MET-08", "Tesis sin premisas")
    pr = p.get("proyecciones") or {}
    if pr.get("activada"):
        if _vacio(pr.get("etapas")) or _vacio(pr.get("premisas")) or _vacio(p.get("sensibilidades")):
            R.falla("G3B-MET-09", "Máquina de proyecciones activada sin etapas, premisas o sensibilidades")
    elif _vacio(pr.get("motivo_exclusion")):
        R.falla("G3B-MET-09", "Máquina de proyecciones excluida sin motivo")
    esc = p.get("escenarios") or []
    if len(esc) < 3:
        R.falla("G3B-MET-10", "Menos de tres escenarios")
    for e in esc:
        if _vacio(e.get("regimen")):
            R.falla("G3B-MET-10", f"Escenario {e.get('nombre')} sin régimen de referencia")
        if e.get("probabilidad") is not None and _vacio(e.get("base_probabilidad")):
            R.falla("G3B-MET-10", f"Escenario {e.get('nombre')} con probabilidad sin base calibrable declarada")
    for x in p.get("pronosticos_detalle") or []:
        if _vacio(x.get("referencia_ingenua")):
            R.falla("G3B-MET-11", f"{x.get('prg_id')} sin referencia ingenua")
    perf = PERFIL_OBJETO.get((p.get("ambito") or {}).get("tipo_objeto"))
    if perf and perf not in (est.get("perfil_motor") or []):
        R.falla("G3B-MET-12", f"Perfil {perf} ausente para el tipo de objeto")
    for pb in est.get("playbooks") or []:
        t2 = pb.replace("SEL-", "")
        if not ((p.get("candidatos_por_tipo") or {}).get(t2) or {}).get("aplicable"):
            R.falla("G3B-MET-12", f"Playbook {pb} sin tipo de activo aplicable")
    de = p.get("despliegue_estructural") or {}
    for k in ("mapa_cadena", "actores", "vigilancia_tecnologica", "cuellos_botella", "efectos_segundo_orden"):
        if k not in de:
            R.falla("G3B-MET-14", f"Despliegue estructural sin «{k}»")
    if "D4" not in excl and not de.get("mapa_cadena"):
        R.falla("G3B-MET-14", "Mapa de la cadena vacío sin exclusión motivada de D4")
    cambio = pu.get("cambio_frente_previo")
    if cambio:
        R.ok("G3B-MET-15")
        if any(abs(float(cambio.get(k, 0))) >= 15 for k in ("A", "E", "C")) and _vacio(cambio.get("justificacion")):
            R.falla("G3B-MET-15", "Cambio ≥ 15 puntos frente al análisis previo sin justificación")
    else:
        R.na("G3B-MET-15", "sin REC-B previo del mismo ámbito")
    pc = p.get("puertas_continuidad")
    if not pc:
        R.falla("G3B-MET-16", "Falta el registro de las puertas de continuidad GC0–GC3")
    else:
        for g in ("GC0", "GC2", "GC3"):
            if _vacio(pc.get(g)):
                R.falla("G3B-MET-16", f"Falta la decisión {g}")
        if _vacio(pc.get("GC1")):
            R.falla("G3B-MET-16", "Falta GC1 por dimensión")
    reg = p.get("regimen") or {}
    if reg.get("estado_confianza") not in ENUMS["estado_regimen"]:
        R.falla("G3B-MET-17", "Régimen sin estado de confianza válido")
    for rel in reg.get("relaciones") or []:
        if rel.get("naturaleza") not in ("historica_observada", "causal_demostrada"):
            R.falla("G3B-MET-17", "Relación del régimen sin naturaleza declarada")
    return punt


# ==============================================================================================================
# CON · Conclusiones
# ==============================================================================================================
def _con(p: Dict, R: Registro, punt: Dict, certificados: Optional[List[Dict]], preguntas: Optional[List[str]]) -> None:
    R.ok(*[f"G3B-CON-{i:02d}" for i in range(1, 19) if i not in (15, 16)])
    v = p.get("veredicto") or {}
    pa = p.get("puertas_ambito") or {}
    est = p.get("estrategia") or {}
    nivel = est.get("nivel", "N2")
    if set(pa) != set(ht03.PUERTAS_AMBITO) or any(x not in ("OK", "BLOQUEA") for x in pa.values()):
        R.falla("G3B-CON-01", "PA1–PA8 incompletas o con valores no permitidos")
    real = v.get("valor")
    bloq = [g for g, x in pa.items() if x == "BLOQUEA"]
    if bloq and real in ("INVERTIR", "INVERTIR_ESCALONADO"):
        R.falla("G3B-CON-01", f"Veredicto {real} por encima del máximo con {', '.join(bloq)} bloqueadas")
    prior = [c for c in candidatos_top(p) if c.get("veredicto") == "PRIORITARIO_PARA_C"]
    if punt and None not in punt.values():
        flags = dict(p.get("x_flags_veredicto") or {})
        if (p.get("refutacion") or {}).get("veredicto_tesis") == "refutada":
            flags["tesis_refutada"] = True
        prov = ht03.veredicto_ambito_provisional(punt["A"], punt["E"], punt["C"], pa, flags)
        esperado = prov["veredicto"]
        if esperado in ("INVERTIR", "INVERTIR_ESCALONADO") and not prior:
            esperado = "VIGILAR"
        if real != esperado:
            R.falla("G3B-CON-02", f"Veredicto {real} ≠ HT-03 ({esperado}: {prov['motivo']})")
    if real in ("INVERTIR", "INVERTIR_ESCALONADO") and not prior:
        R.falla("G3B-CON-02", f"{real} sin ningún PRIORITARIO_PARA_C")
    if real == "INVERTIR" and _vacio(v.get("condiciones_entrada")):
        R.falla("G3B-CON-03", "INVERTIR sin condiciones de entrada")
    if real == "INVERTIR_ESCALONADO" and (_vacio(v.get("tramos")) or any(_vacio(t.get("condicion")) for t in v.get("tramos") or [])):
        R.falla("G3B-CON-03", "INVERTIR_ESCALONADO sin tramos con disparador")
    if real == "VIGILAR" and (_vacio(v.get("disparadores")) or any(_vacio(d.get("fecha_esperada")) for d in v.get("disparadores") or [])):
        R.falla("G3B-CON-03", "VIGILAR sin disparadores fechados")
    if real == "DESCARTAR" and (_vacio(v.get("motivo_descarte")) or _vacio(v.get("que_cambiaria_la_conclusion"))):
        R.falla("G3B-CON-03", "DESCARTAR sin motivo o sin «qué tendría que cambiar»")
    if v.get("siguiente_paso_sugerido") not in ENUMS["siguiente_paso_sugerido"] or _vacio(v.get("que_cambiaria_la_conclusion")):
        R.falla("G3B-CON-04", "siguiente_paso_sugerido o que_cambiaria_la_conclusion ausentes o fuera de vocabulario", "B")
    if v.get("relevancia_decisional") not in ENUMS["relevancia_decisional"]:
        R.falla("G3B-CON-04", "relevancia_decisional fuera de vocabulario", "B")
    pu = p.get("puntuaciones") or {}
    tipos_prior = sorted({c["_tipo"] for c in prior})
    try:
        rel, mot = ht03.relevancia_decisional(real, int(pu.get("A", 0)), int(pu.get("E", 0)), int(p.get("riesgo_1a5") or 3),
                                              est.get("horizonte_dominante", "H3"), bool(p.get("x_iliquidez")), tipos_prior,
                                              bool(v.get("x_disparador_cercano")))
        if v.get("relevancia_decisional") != rel:
            R.falla("G3B-CON-04", f"relevancia_decisional {v.get('relevancia_decisional')} ≠ regla de 7.9 ({rel})", "W")
    except (TypeError, ValueError):
        R.falla("G3B-CON-04", "No se puede recalcular la relevancia decisional", "W")
    if v.get("siguiente_paso_sugerido") == "ENVIAR_CANDIDATOS_A_C" and not prior:
        R.falla("G3B-CON-04", "ENVIAR_CANDIDATOS_A_C sin prioritarios", "B")
    res = v.get("resultado_del_analisis")
    if res == "NO_CONCLUYENTE" and real != "VIGILAR":
        R.falla("G3B-CON-05", "NO_CONCLUYENTE con veredicto distinto de VIGILAR")
    if res == "PARCIAL" and _vacio(est.get("recortes_declarados")) and _vacio(p.get("limitaciones")):
        R.falla("G3B-CON-05", "PARCIAL sin alcance reducido declarado")
    ref = p.get("refutacion") or {}
    if nivel in ("N2", "N3") and (ref.get("realizada_por") != "AG-B14" or ref.get("veredicto_tesis") not in ENUMS["veredicto_tesis"]):
        R.falla("G3B-CON-06", "N2/N3 sin refutación de AG-B14 sobre la tesis (CT-B-17)")
    for o in ref.get("objeciones") or []:
        if o.get("objeto") == "TESIS" and o.get("fuerza") == "fuerte" and not o.get("resuelta") and \
                real in ("INVERTIR", "INVERTIR_ESCALONADO"):
            R.falla("G3B-CON-06", f"{o.get('obj_id')}: objeción fuerte sin resolver sobre la tesis con {real} (R18)")
    if real != "DESCARTAR" and _vacio(p.get("invalidacion")):
        R.falla("G3B-CON-07", "Sin condiciones de invalidación")
    if _vacio(p.get("riesgos")) or any(_vacio(r.get("senal_temprana")) for r in p.get("riesgos") or []):
        R.falla("G3B-CON-07", "Riesgos sin señal temprana")
    if _vacio(p.get("limitaciones")) and _vacio((p.get("tesis") or {}).get("lo_que_no_sabemos")):
        R.falla("G3B-CON-07", "Falta «qué podría salir mal y qué no sabemos»")
    if real in ("INVERTIR", "INVERTIR_ESCALONADO") and _vacio((p.get("tesis") or {}).get("steelman_contrario")):
        R.falla("G3B-CON-07", "Sin steelman de la tesis contraria")
    cert = certificados or []
    for x in p.get("pronosticos_detalle") or []:
        if x.get("probabilidad_publicada") is not None and not any(c.get("celda") == x.get("celda") for c in cert):
            R.falla("G3B-CON-08", f"{x.get('prg_id')}: probabilidad publicada sin certificado de {x.get('celda')}")
        if x.get("probabilidad_publicada") is None and x.get("banda") not in BANDAS_VERBALES:
            R.falla("G3B-CON-09", f"{x.get('prg_id')}: sin certificado y sin banda verbal")
    for e in p.get("escenarios") or []:
        if e.get("probabilidad") is not None and not cert and _vacio(e.get("base_probabilidad")):
            R.falla("G3B-CON-08", f"Escenario {e.get('nombre')} con probabilidad sin certificado ni base")
    if not [c for c in cert if c.get("tipo") == "ranking"] and \
            "sin ventaja demostrada" not in str((p.get("historial_aciertos") or {}).get("certificacion", "")):
        R.falla("G3B-CON-09", "Sin certificado de ranking y sin la leyenda «sin ventaja demostrada todavía»")
    hz = est.get("horizonte_dominante")
    for t in TIPOS:
        d = (p.get("candidatos_por_tipo") or {}).get(t) or {}
        if d.get("aplicable") and hz in ht03.HORIZONTES:
            ap = TABLA_HORIZONTES[t][ht03.HORIZONTES.index(hz)] if t in TABLA_HORIZONTES else "SI"
            if ap == "NO":
                R.falla("G3B-CON-10", f"Horizonte {hz} no aplicable a {t} (8.6)")
            elif ap == "LIMITADO" and _vacio(d.get("x_justificacion_horizonte")) and _vacio(p.get("catalizadores")):
                R.falla("G3B-CON-10", f"Horizonte {hz} «Limitado» para {t} sin catalizador ni datos declarados")
    if hz == "H1" and not any("tiempo real" in s.lower() or "H1" in s for s in p.get("limitaciones") or []):
        R.falla("G3B-CON-10", "H1 sin advertencia de baja fiabilidad sin datos en tiempo real")
    detalle = {x.get("prg_id"): x for x in p.get("pronosticos_detalle") or []}
    for prg in p.get("pronosticos") or []:
        x = detalle.get(prg)
        if not x:
            R.falla("G3B-CON-11", f"{prg} sin detalle congelable")
            continue
        for k in ("afirmacion", "fecha_resolucion", "criterio", "referencia", "referencia_ingenua"):
            if _vacio(x.get(k)):
                R.falla("G3B-CON-11", f"{prg}: sin «{k}»")
        if x.get("tipo") == "RANKING" and (_vacio(x.get("universo_ref")) or _vacio(x.get("tratamiento_bajas"))):
            R.falla("G3B-CON-11", f"{prg}: ranking sin universo_ref o tratamiento_bajas")
    m = p.get("mapa_cobertura") or {}
    for k in CLAVES_MAPA:
        if k not in m:
            R.falla("G3B-CON-12", f"mapa_cobertura sin «{k}»")
    if _vacio(m.get("investigado")):
        R.falla("G3B-CON-12", "No distingue «sin oportunidades» de «insuficientemente estudiado» (investigado vacío)")
    for e in m.get("excluido_con_motivo") or []:
        if isinstance(e, dict) and _vacio(e.get("motivo")):
            R.falla("G3B-CON-12", f"Omisión sin motivo: {e.get('objeto')}")
    for k in ("mercado", "calidad_ambito", "atractivo_bursatil", "accesibilidad"):
        if _vacio((p.get("evaluaciones_separadas") or {}).get(k)):
            R.falla("G3B-CON-13", f"Falta la evaluación «{k}»")
    resp = p.get("respuestas_preguntas") or []
    for r in resp:
        if _vacio(r.get("respuesta")):
            R.falla("G3B-CON-14", f"Pregunta sin respuesta: {str(r.get('pregunta'))[:60]!r}")
    for q in preguntas or []:
        if not any(q.strip().lower() == str(r.get("pregunta", "")).strip().lower() for r in resp):
            R.falla("G3B-CON-14", f"Pregunta de la petición sin respuesta explícita: {q[:60]!r}")
    h = p.get("historial_aciertos") or {}
    if _vacio(h) or _vacio(h.get("certificacion")) or (_vacio(h.get("ambitos")) and _vacio(h.get("rankings"))):
        R.falla("G3B-CON-17", "Historial de aciertos sin tamaño muestral o sin estado de certificación")
    cv = v.get("confianza_verbal")
    if cv is not None and cv not in ENUMS["confianza_verbal"]:
        R.falla("G3B-CON-18", f"Confianza fuera de vocabulario: {cv!r}")


# ==============================================================================================================
# SEL · Selección de candidatos
# ==============================================================================================================
def _sel(p: Dict, R: Registro) -> None:
    R.ok(*[f"G3B-SEL-{i:02d}" for i in range(1, 16)])
    est = p.get("estrategia") or {}
    nivel = est.get("nivel", "N2")
    veredicto = (p.get("veredicto") or {}).get("valor")
    u = ht03.PARAMETROS_POR_DEFECTO["umbrales_candidato"]
    con_vig = bool(p.get("x_candidatos_aun_con_vigilar"))
    obj_fuertes = {o.get("objeto") for o in (p.get("refutacion") or {}).get("objeciones") or []
                   if o.get("fuerza") == "fuerte" and not o.get("resuelta")}
    obj_resp = {o.get("objeto") for o in (p.get("refutacion") or {}).get("objeciones") or []
                if o.get("fuerza") in ("fuerte", "moderada") and _vacio(o.get("respuesta"))
                and o.get("estado_contraste") != "incertidumbre_abierta"}
    for t in TIPOS:
        d = (p.get("candidatos_por_tipo") or {}).get(t) or {}
        if not d.get("aplicable"):
            continue
        uni = d.get("universo") or {}
        if any(_vacio(uni.get(k)) and uni.get(k) != 0 for k in ("tamano", "fuentes", "fecha")) or "excluidos_por_motivo" not in d:
            R.falla("G3B-SEL-01", f"{t}: universo incompleto o sin excluidos_por_motivo")
        if "punto" not in str(uni.get("metodo", "")).lower() and not uni.get("x_sesgo_supervivencia_comprobado"):
            R.falla("G3B-SEL-14", f"{t}: universo sin comprobación de sesgo de supervivencia declarada")
        top = d.get("top_n") or []
        lim = LIMITE_TOP.get(nivel)
        if lim and len(top) > lim[0]:
            R.falla("G3B-SEL-06", f"{t}: {len(top)} en el top-N (máximo {lim[0]})")
        if lim and len(top) < lim[0] and _vacio(d.get("menos_de_N_motivo")):
            R.falla("G3B-SEL-06", f"{t}: menos de N sin menos_de_N_motivo (R21)")
        if _vacio(d.get("traduccion_rasgos_metricas")):
            R.falla("G3B-SEL-12", f"{t}: rasgos de la tesis sin traducción a métricas")
        pmin = ht03.PLAYBOOKS[t]["pureza_min"]
        indices, emisores, subcl = {}, {}, {}
        sustituidos = {s.get("desplazado") for s in d.get("sustituciones_diversidad") or []}
        for c in top:
            cid = c.get("cand_id")
            pc = c.get("puertas") or {}
            if any(pc.get(g, "OK") != "OK" for g in ("PC1", "PC2", "PC3", "PC4")) or \
                    any(a.get("estado") == "critica" for a in c.get("alertas") or []):
                R.falla("G3B-SEL-02", f"{cid}: en el top-N sin PC1–PC4 superadas")
            des = c.get("desglose") or {}
            try:
                comp = {k: ("NA" if (des.get(k) is None and ht03.PLAYBOOKS[t]["pesos"].get(k) is None) else
                            ("NE" if des.get(k) is None else des.get(k))) for k in ht03.COMPONENTES_S}
                rs = ht03.calcular_S(comp, t)
                if not rs["calculable"]:
                    R.falla("G3B-SEL-03", f"{cid}: S no calculable (> 2 NE)")
                elif rs["S"] != c.get("S") and not (c.get("segunda_pasada") and (c.get("S") or 101) < rs["S"]):
                    R.falla("G3B-SEL-03", f"{cid}: S = {c.get('S')} no se reconstruye ({rs['S']})")
            except ht03.ErrorEntrada as e:
                R.falla("G3B-SEL-03", f"{cid}: desglose no válido ({e})")
            S, ic = c.get("S"), c.get("ic90_S")
            if not ic or len(ic) != 2 or S is None or not ic[0] <= S <= ic[1] or not c.get("ic90_rango"):
                R.falla("G3B-SEL-04", f"{cid}: falta ic90_S/ic90_rango o el IC no contiene S")
            ver = c.get("veredicto")
            if ver == "PRIORITARIO_PARA_C":
                if ic and ic[0] < u["ic90_inferior_prioritario"] or c.get("frontera"):
                    R.falla("G3B-SEL-04", f"{cid}: PRIORITARIO con IC inferior < 55 o FRONTERA (PC6)")
                prob = []
                if S is None or S < u["PRIORITARIO_PARA_C"]:
                    prob.append("S < 65")
                if any(pc.get(g, "OK") != "OK" for g in ("PC5", "PC6", "PC7", "PC8")):
                    prob.append("PC5–PC8 limitan")
                if veredicto not in ("INVERTIR", "INVERTIR_ESCALONADO") and not con_vig:
                    prob.append(f"ámbito {veredicto}")
                if prob:
                    R.falla("G3B-SEL-05", f"{cid}: PRIORITARIO_PARA_C indebido ({'; '.join(prob)})")
                if cid in obj_fuertes:
                    R.falla("G3B-SEL-11", f"{cid}: PRIORITARIO con objeción fuerte sin resolver (PC5)")
            elif ver == "SECUNDARIO" and S is not None and S < u["SECUNDARIO"]:
                R.falla("G3B-SEL-05", f"{cid}: SECUNDARIO con S < 50")
            if nivel in ("N2", "N3") and cid in obj_resp:
                R.falla("G3B-SEL-11", f"{cid}: objeción fuerte o moderada sin respuesta")
            pur = c.get("pureza") or {}
            if _vacio(pur.get("fuente")) or _vacio(pur.get("metodo")):
                R.falla("G3B-SEL-15", f"{cid}: pureza sin fuente o método")
            if pmin is not None and (pur.get("valor") is None or pur["valor"] < pmin):
                R.falla("G3B-SEL-15", f"{cid}: pureza {pur.get('valor')} < mínimo {pmin}")
            ti = c.get("tipo_instrumento")
            if ti in ("etf", "fondo") and t != "FON":
                R.falla("G3B-SEL-09", f"{cid}: vehículo colectivo fuera de FON")
            if t == "FON" and _vacio(c.get("tipo_subyacente")):
                R.falla("G3B-SEL-09", f"{cid}: FON sin tipo_subyacente")
            if ti in ("etc", "etn") and t in ("FON", "RV"):
                R.falla("G3B-SEL-09", f"{cid}: ETC/ETN fuera del tipo de su subyacente")
            if t == "IDX" and ti != "indice":
                R.falla("G3B-SEL-09", f"{cid}: candidato IDX que no es un índice (el vehículo de réplica es FON)")
            if ti in ("opcion_binaria", "cfd") or "binaria" in str(c.get("nombre", "")).lower():
                R.falla("G3B-SEL-10", f"{cid}: instrumento excluido por el marco (binaria o CFD)")
            if pc.get("PC1") not in (None, "OK"):
                R.falla("G3B-SEL-10", f"{cid}: fuera del marco de invertibilidad (PC1)")
            ir = c.get("indice_replicado")
            if ir:
                if ir in indices and cid not in sustituidos:
                    R.falla("G3B-SEL-07", f"{cid} y {indices[ir]} replican el mismo índice")
                indices[ir] = cid
            if t == "RF" and c.get("emisor"):
                emisores[c["emisor"]] = emisores.get(c["emisor"], 0) + 1
            if c.get("subcluster"):
                subcl[c["subcluster"]] = subcl.get(c["subcluster"], 0) + 1
        for e, n in emisores.items():
            if n > 2:
                R.falla("G3B-SEL-07", f"RF: {n} emisiones de {e} en el top-N")
        if top and not d.get("ambito_es_subcluster"):
            n_prev = (lim or (len(top), 0))[0]
            for s, n in subcl.items():
                if n > max(1, int(0.4 * n_prev)):
                    R.falla("G3B-SEL-07", f"{t}: subclúster {s} con {n} (> 40 % del top-N)")
    # Encargos C.x
    enc = {}
    for lst in (p.get("paquete_para_bloque_C") or {}).values():
        for e in lst or []:
            enc[e.get("cand_id")] = e
    tops = {c.get("cand_id"): c for c in candidatos_top(p)}
    adic = opciones_adicionales(p)      # V2.1: mejores opciones por eslabón añadidas por cobertura (9.13)
    for cid, c in tops.items():
        if c.get("veredicto") in ("PRIORITARIO_PARA_C", "SECUNDARIO") and cid not in enc:
            R.falla("G3B-SEL-13", f"{cid}: candidato del top-N sin encargo")
    pv3_no = ((p.get("capas") or {}).get("puertas_viabilidad") or {}).get("PV3") == "NO_SUPERADA"
    for cid, o in adic.items():
        if pv3_no:      # PV3 no superada: opciones indicativas sin encargo C.x (7.10, 14.6)
            continue
        if o.get("veredicto") in ("PRIORITARIO_PARA_C", "SECUNDARIO") and cid not in enc:
            R.falla("G3B-SEL-13", f"{cid}: opción por eslabón sin encargo (9.4, paso 10)")
    for cid, e in enc.items():
        c = tops.get(cid)
        if c is None and cid in adic:
            o = adic[cid]
            pu = e.get("puntuacion") or {}
            if pu.get("S") != o.get("S") or e.get("origen_seleccion") != "MEJORES_POR_ESLABON" or e.get("eslabon_id") != o.get("_eslabon"):
                R.falla("G3B-SEL-13", f"{cid}: encargo de una opción por eslabón incoherente (S, origen o eslabón)")
            continue
        if c is None:
            R.falla("G3B-SEL-13", f"{cid}: encargo de un candidato que no está en el top-N ni en las tablas por eslabón")
            continue
        pu = e.get("puntuacion") or {}
        if pu.get("S") != c.get("S") or pu.get("ic90_S") != c.get("ic90_S") or pu.get("rango") != c.get("rango"):
            R.falla("G3B-SEL-13", f"{cid}: S, IC o rango del encargo distintos del candidato")
        if (e.get("pureza") or {}).get("valor") != (c.get("pureza") or {}).get("valor"):
            R.falla("G3B-SEL-13", f"{cid}: pureza del encargo distinta")
        if len(e.get("senales_alerta") or []) != len(c.get("alertas") or []):
            R.falla("G3B-SEL-13", f"{cid}: alertas del encargo distintas")
        if e.get("pet_id") != p.get("pet_id") or e.get("rec_id") != p.get("rec_id") or e.get("data_cutoff") != p.get("data_cutoff"):
            R.falla("G3B-SEL-13", f"{cid}: pet_id, rec_id o data_cutoff del encargo distintos")
    # Apuestas independientes
    n = p.get("apuestas_independientes")
    top_v = [c for c in tops.values() if c.get("veredicto") in ("PRIORITARIO_PARA_C", "SECUNDARIO")] + \
        [o for o in adic.values() if o.get("veredicto") in ("PRIORITARIO_PARA_C", "SECUNDARIO")]
    if not isinstance(n, int) or n < 0:
        R.falla("G3B-SEL-08", f"apuestas_independientes no válido: {n!r}")
    else:
        emisores_glob: Dict[str, List[str]] = {}
        for c in top_v:
            if c.get("emisor"):
                emisores_glob.setdefault(c["emisor"], []).append(c.get("cand_id"))
        for em, ids in emisores_glob.items():
            if len(ids) > 1 and not all((tops.get(i) or adic.get(i) or {}).get("exposicion_compartida") for i in ids):
                R.falla("G3B-SEL-08", f"Exposición compartida sin marcar: {em} ({', '.join(ids)})")
        distintas = len(top_v) - sum(len(ids) - 1 for ids in emisores_glob.values() if len(ids) > 1)
        if n > max(distintas, 0):
            R.falla("G3B-SEL-08", f"{n} apuestas independientes > {distintas} exposiciones distintas")
        if any(c.get("veredicto") == "PRIORITARIO_PARA_C" for c in top_v) and n < 1:
            R.falla("G3B-SEL-08", "Hay prioritarios y 0 apuestas independientes")


# ==============================================================================================================
# TMP · Tiempo
# ==============================================================================================================
def _tmp(p: Dict, R: Registro) -> None:
    R.ok("G3B-TMP-01", "G3B-TMP-02", "G3B-TMP-03", "G3B-TMP-04")
    tc = p.get("tiempo_consumo") or {}
    est = p.get("estrategia") or {}
    for k in ("minutos", "uc", "estimado_p80_min", "por_fase_min"):
        if _vacio(tc.get(k)) and tc.get(k) != 0:
            R.falla("G3B-TMP-01", f"tiempo_consumo sin «{k}»")
    p80 = tc.get("estimado_p80_min")
    real = tc.get("minutos")
    aut = tc.get("autorizaciones") or []
    autorizado = tc.get("minutos_autorizados") or 30
    margen = max(0.1 * autorizado, 5)
    n3_expreso = est.get("nivel") == "N3" and tc.get("n3_expreso")
    if not aut and not n3_expreso:
        if isinstance(p80, (int, float)) and p80 > 30:
            R.falla("G3B-TMP-02", f"p80 {p80} min > 30 sin AUT-B registrada (R20)")
        if isinstance(real, (int, float)) and real > autorizado + margen:
            R.falla("G3B-TMP-02", f"Tiempo real {real} min > autorizado {autorizado} + margen sin AUT-B")
    rec = tc.get("opcion_autorizada") or est.get("x_opcion_autorizada")
    if rec in ("VERSION_30_MIN", "DIVIDIR_EN_FASES") and _vacio(est.get("recortes_declarados")):
        R.falla("G3B-TMP-03", f"Opción {rec} sin alcance reducido declarado (R23)")
    if (p.get("veredicto") or {}).get("resultado_del_analisis") == "PARCIAL" and _vacio(est.get("recortes_declarados")) \
            and _vacio(p.get("limitaciones")):
        R.falla("G3B-TMP-03", "Resultado PARCIAL sin alcance reducido declarado")
    deg = p.get("estados_degradados") or []
    if deg and _vacio(p.get("limitaciones")):
        R.falla("G3B-TMP-04", "Estados degradados sin limitación declarada")


# ==============================================================================================================
# ENT · Entregables (segunda pasada)
# ==============================================================================================================
def _meta(html: str, nombre: str) -> Optional[str]:
    m = re.search(rf'<meta\s+name="{re.escape(nombre)}"\s+content="([^"]*)"', html)
    return m.group(1) if m else None


def _ent(p: Dict, R: Registro, html: Optional[str], tecnico: Optional[str], memo: Optional[str],
         anexo: Optional[str], rutas: Optional[Dict[str, str]]) -> None:
    pu = p.get("puntuaciones") or {}
    v = (p.get("veredicto") or {}).get("valor")
    prior = [c for c in candidatos_top(p) if c.get("veredicto") == "PRIORITARIO_PARA_C"]
    if html is not None:
        R.ok("G3B-ENT-01", "G3B-ENT-04", "G3B-ENT-08", "G3B-ENT-10", "G3B-DAT-08")
        r = ht07.analizar(html, es_html=True)
        if r["fernandez_huerta"] is None or r["fernandez_huerta"] < 70:
            R.falla("G3B-ENT-01", f"Fernández-Huerta {r['fernandez_huerta']} < 70")
        if r["pct_frases_mas_de_20"] > 5:
            R.falla("G3B-ENT-01", f"{r['pct_frases_mas_de_20']} % de frases de más de 20 palabras (> 5 %)")
        if r["jerga_sin_explicar"]:
            R.falla("G3B-ENT-10", f"Jerga sin explicar: {r['jerga_sin_explicar'][:8]}")
        visible = ht07.extraer_texto_html(html)
        # V2.1 (14.2): los nombres de las opciones solo pueden aparecer en las tablas simplificadas por eslabón
        fuera_tablas = ht07.extraer_texto_html(re.sub(r'<section[^>]*aria-labelledby="t-eslabones".*?</section>', "", html, flags=re.S))
        if AVISO_VISUAL not in visible:
            R.falla("G3B-ENT-04", "Falta el aviso de no recomendación personal")
        if "En 30 segundos" not in visible:
            R.falla("G3B-ENT-04", "Falta «En 30 segundos»")
        sem = _meta(html, "semaforo")
        if sem is None or 'class="luz' not in html:
            R.falla("G3B-ENT-04", "Falta el semáforo")
        elif sem != SEMAFORO.get(v):
            R.falla("G3B-ENT-04", f"Semáforo {sem} ≠ veredicto {v}")
        nombres = sorted({str(c.get("nombre") or "") for c in candidatos_top(p)} |
                         {str(o.get("nombre") or "") for e in ((p.get("mapa_cadena_valor") or {}).get("eslabones") or [])
                          for o in e.get("opciones") or []}, key=len, reverse=True)
        sin_nombres = visible
        for n_ in nombres:
            if len(n_) > 2:
                sin_nombres = sin_nombres.replace(n_, " ")
        for c in candidatos_top(p):
            for k in ("isin", "ticker"):
                val = c.get(k)
                if val and len(str(val)) >= 3 and re.search(rf"\b{re.escape(str(val))}\b", sin_nombres):
                    R.falla("G3B-ENT-04", f"Muestra el identificador {val} de un candidato (lista de valores)")
            nombre = str(c.get("nombre") or "")
            if len(nombre) > 6 and nombre in fuera_tablas:
                R.falla("G3B-ENT-04", f"Muestra el nombre del candidato «{nombre}» fuera de las tablas por eslabón (14.2)")
        if RE_ISIN.search(visible):
            R.falla("G3B-ENT-04", "Contiene un ISIN")
        if re.search(r"<img(?![^>]*\balt=)", html) or re.search(r"<svg(?![^>]*\b(role|aria-label|aria-hidden)=)", html):
            R.falla("G3B-ENT-08", "Gráfico o imagen sin texto alternativo")
        if _meta(html, "data_cutoff") != p.get("data_cutoff"):
            R.falla("G3B-DAT-08", "Informe visual con data_cutoff distinto o ausente")
    else:
        for c in ("G3B-ENT-01", "G3B-ENT-04", "G3B-ENT-08", "G3B-ENT-10"):
            R.na(c, "informe visual no proporcionado (pasada PAQUETE_SINTESIS)")
    textos = [(n, t) for n, t in (("informe técnico", tecnico), ("memorando", memo)) if t is not None]
    if textos:
        R.ok("G3B-ENT-02", "G3B-ENT-03", "G3B-DAT-08", "G3B-ENT-09")
        numeros_paquete = set(re.findall(r"-?\d+(?:[.,]\d+)?", json.dumps(p, ensure_ascii=False)))
        for nombre, t in textos:
            if v and v not in t:
                R.falla("G3B-ENT-03", f"{nombre}: no recoge el veredicto {v}")
            for k in ("A", "E", "C"):
                if pu.get(k) is not None and not re.search(rf"\b{k}\b\D{{0,25}}\b{pu[k]}\b", t):
                    R.falla("G3B-ENT-03", f"{nombre}: no recoge {k} = {pu[k]}")
            if p.get("data_cutoff") not in t:
                R.falla("G3B-DAT-08", f"{nombre}: no declara la fecha de corte {p.get('data_cutoff')}")
            for d in re.findall(r"data_cutoff\D{0,20}(\d{4}-\d{2}-\d{2})", t):
                if d != p.get("data_cutoff"):
                    R.falla("G3B-DAT-08", f"{nombre}: data_cutoff {d} distinto")
            for c in prior:
                if c.get("cand_id") not in t:
                    R.falla("G3B-ENT-03", f"{nombre}: no cita el prioritario {c.get('cand_id')}")
                elif not re.search(rf"{re.escape(c['cand_id'])}[^\n]{{0,240}}\b{c.get('S')}\b", t):
                    R.falla("G3B-ENT-02", f"{nombre}: S de {c.get('cand_id')} distinto del paquete")
            for m in re.finditer(r"\bS = (\d+)", t):
                if m.group(1) not in numeros_paquete:
                    R.falla("G3B-ENT-02", f"{nombre}: cifra S = {m.group(1)} inexistente en el paquete")
            portada = t[:4000]
            for r in p.get("reservas_auditoria") or []:
                if str(r)[:40] not in portada:
                    R.falla("G3B-ENT-09", f"{nombre}: reserva de auditoría ausente de la portada")
            for e in p.get("estados_degradados") or []:
                if str(e)[:40] not in portada and nombre == "informe técnico":
                    R.falla("G3B-ENT-09", f"{nombre}: estado degradado ausente de la portada")
    else:
        for c in ("G3B-ENT-02", "G3B-ENT-03", "G3B-ENT-09"):
            R.na(c, "entregables no proporcionados (pasada PAQUETE_SINTESIS)")
        if html is None:
            R.na("G3B-DAT-08", "entregables no proporcionados")
    if tecnico is not None:
        R.ok("G3B-ENT-05")
        for i in range(1, SECCIONES_TECNICO + 1):
            if not re.search(rf"^## {i}\. ", tecnico, re.M):
                R.falla("G3B-ENT-05", f"Falta la sección {i} de 14.1")
    else:
        R.na("G3B-ENT-05", "informe técnico no proporcionado")
    if memo is not None:
        R.ok("G3B-ENT-06")
        palabras = len(memo.split())
        if palabras > 1100:
            R.falla("G3B-ENT-06", f"Memorando de {palabras} palabras (> 2 páginas)")
        for k in ("Veredicto", "Tesis", "Riesgos", "Tiempo"):
            if k.lower() not in memo.lower():
                R.falla("G3B-ENT-06", f"Memorando sin «{k}»")
    else:
        R.na("G3B-ENT-06", "memorando no proporcionado")
    if anexo is not None:
        R.ok("G3B-ENT-07")
        try:
            from openpyxl import load_workbook  # type: ignore
            wb = load_workbook(anexo, read_only=True)
            hojas = set(wb.sheetnames)
            for h in HOJAS_ANEXO:
                if h not in hojas:
                    R.falla("G3B-ENT-07", f"Anexo sin la hoja {h}")
            for t in TIPOS:
                if ((p.get("candidatos_por_tipo") or {}).get(t) or {}).get("aplicable") and f"Universo_{t}" not in hojas:
                    R.falla("G3B-ENT-07", f"Anexo sin la hoja Universo_{t}")
                elif f"Universo_{t}" in hojas:
                    ws = wb[f"Universo_{t}"]
                    filas = list(ws.iter_rows(values_only=True))
                    cab = list(filas[0]) if filas else []
                    if "S" in cab and "cand_id" in cab:
                        ix, iS = cab.index("cand_id"), cab.index("S")
                        Sanexo = {f[ix]: f[iS] for f in filas[1:] if f[ix]}
                        for c in candidatos_top(p):
                            if c["_tipo"] == t and str(Sanexo.get(c["cand_id"])) != str(c.get("S")):
                                R.falla("G3B-ENT-07", f"S de {c['cand_id']} no coincide con el anexo")
        except ImportError:
            R.falla("G3B-ENT-07", "openpyxl no disponible para leer el anexo", "W")
        except Exception as e:  # noqa: BLE001
            R.falla("G3B-ENT-07", f"Anexo ilegible: {e}")
    else:
        R.na("G3B-ENT-07", "anexo no proporcionado")
    if rutas:
        R.ok("G3B-EST-08")
        carpetas = {"informe_tecnico": ("Informes técnicos Broker", "informe-tecnico"),
                    "informe_visual": ("Informes visuales Usuario", "informe-visual"),
                    "paquete_json": ("Paquetes JSON", "paquete-json"), "memorando": ("Memorandos ejecutivos", "memorando"),
                    "anexo_datos": ("Anexos de datos", "anexo-datos")}
        for k, ruta in rutas.items():
            if k not in carpetas:
                continue
            carpeta, tipo = carpetas[k]
            nombre = os.path.basename(ruta)
            if not re.match(rf"\d{{4}}-\d{{2}}-\d{{2}}_{tipo}_{re.escape(str(p.get('pet_id')))}(_fase\d)?\.", nombre) or \
                    os.path.basename(os.path.dirname(ruta)) != carpeta:
                R.falla("G3B-EST-08", f"{k}: ruta {ruta} fuera de la convención ENT")
    else:
        R.na("G3B-EST-08", "rutas de entregables no proporcionadas")


# ==============================================================================================================
# ==============================================================================================================
# V2.1 · Cadena de valor por eslabón, capas, horizontes, consultas y lista profesional (catálogo del Orquestador,
# grupo 8: EST-11…14, MET-18…22, CON-19…21, SEL-16…18, TMP-05…06, ENT-11…12)
# ==============================================================================================================
LIMITE_CONSULTAS = {"N1": (1, 1), "N2": (3, 1), "N3": (6, 2), "PERS": (3, 1), "N1-SEG": (1, 1)}


def _pv_resultado(pv: Dict, g: str) -> Optional[str]:
    x = pv.get(g)
    return x.get("resultado") if isinstance(x, dict) else x


def _v21(p: Dict, R: Registro, f1: Optional[Dict] = None) -> None:
    R.ok("G3B-EST-11", "G3B-EST-14", "G3B-MET-18", "G3B-MET-19", "G3B-MET-20", "G3B-MET-21", "G3B-MET-22", "G3B-CON-20",
         "G3B-CON-21", "G3B-SEL-16", "G3B-SEL-17", "G3B-SEL-18", "G3B-TMP-05")
    est = p.get("estrategia") or {}
    v = p.get("veredicto") or {}
    nivel = est.get("nivel", "N2")
    m = p.get("mapa_cadena_valor") or {}
    esl = m.get("eslabones") or []
    # EST-11 · esquema del mapa (B.16)
    if not esl:
        R.falla("G3B-EST-11", "mapa_cadena_valor sin eslabones (sin cadena: eslabón único ESL-00)")
    ids = [e.get("eslabon_id") for e in esl]
    if len(ids) != len(set(ids)):
        R.falla("G3B-EST-11", "eslabon_id duplicado en el mapa")
    por_id = {e.get("eslabon_id"): e for e in esl}
    for e in esl:
        eid = e.get("eslabon_id")
        if not re.fullmatch(RE_ESLABON, str(eid or "")):
            R.falla("G3B-EST-11", f"eslabon_id no válido: {eid!r}")
        if e.get("nivel") not in ht03.NIVELES_ESLABON:
            R.falla("G3B-EST-11", f"{eid}: nivel {e.get('nivel')!r} fuera de macro|sub|actividad|insumo")
        if e.get("padre") and e["padre"] not in ids:
            R.falla("G3B-EST-11", f"{eid}: padre {e['padre']} inexistente")
        for k in ("nombre", "descripcion", "metricas", "cuello_botella", "atractivo"):
            if _vacio(e.get(k)):
                R.falla("G3B-EST-11", f"{eid}: falta «{k}»")
        cb = e.get("cuello_botella") or {}
        for k in ("severidad", "persistencia", "relevancia_valor", "PCB", "material", "indicadores", "senal_resolucion"):
            if k not in cb:
                R.falla("G3B-EST-11", f"{eid}: cuello_botella sin «{k}»")
        at = e.get("atractivo") or {}
        ae = at.get("AE")
        if ae is None or not (isinstance(ae, (int, float)) and 0 <= ae <= 100) or "desglose" not in at:
            R.falla("G3B-EST-11", f"{eid}: atractivo sin AE válido y desglose")
        if not e.get("opciones") and _vacio(e.get("sin_opciones_motivo")) and ht03.eslabon_cualifica(e)["cualifica"]:
            R.falla("G3B-EST-11", f"{eid}: eslabón que cualifica sin opciones y sin sin_opciones_motivo")
        # MET-19 · PCB y AE reconstruibles
        try:
            ev = ht03.evaluar_cuello([{"indicador": x.get("indicador"), "estado": x.get("estado"), "valor": x.get("valor")}
                                      for x in cb.get("indicadores") or []], None, int(cb.get("relevancia_valor") or 1))
            if cb.get("indicadores") and ev["severidad"] != cb.get("severidad"):
                R.falla("G3B-MET-19", f"{eid}: severidad {cb.get('severidad')} no corresponde a los indicadores en semáforo ({ev['severidad']})")
            pcb = ht03.calcular_PCB(int(cb.get("severidad")), int(cb.get("persistencia")), int(cb.get("relevancia_valor")))
            if pcb != cb.get("PCB"):
                R.falla("G3B-MET-19", f"{eid}: PCB {cb.get('PCB')} ≠ {pcb} recalculado")
            rojos = sum(1 for x in cb.get("indicadores") or [] if x.get("estado") == "ROJO")
            if bool(cb.get("material")) != (pcb >= 30 and rojos >= 2):
                R.falla("G3B-MET-19", f"{eid}: «material» incoherente con PCB {pcb} y {rojos} indicadores en rojo")
            if any(_vacio(x.get("fuente")) for x in cb.get("indicadores") or []):
                R.falla("G3B-MET-19", f"{eid}: indicador de cuello sin fuente")
        except (TypeError, ValueError, ht03.ErrorEntrada) as ex:
            R.falla("G3B-MET-19", f"{eid}: PCB no reconstruible ({ex})")
        des = at.get("desglose")
        if des and ae is not None:
            try:
                r = ht03.calcular_AE({k: des.get(k) for k in ht03.PARAMETROS_POR_DEFECTO["pesos_AE"]}, cb.get("PCB"))
                if r["total"] != ae:
                    R.falla("G3B-MET-19", f"{eid}: AE {ae} ≠ {r['total']} recalculado")
            except ht03.ErrorEntrada as ex:
                R.falla("G3B-MET-19", f"{eid}: AE no reconstruible ({ex})")
        # MET-20 · desglose jerárquico (W): conciliación con el padre
        if e.get("padre") in por_id:
            t_h = ((e.get("metricas") or {}).get("tamano") or {}).get("valor") if isinstance((e.get("metricas") or {}).get("tamano"), dict) else None
            t_p = ((por_id[e["padre"]].get("metricas") or {}).get("tamano") or {}).get("valor") \
                if isinstance((por_id[e["padre"]].get("metricas") or {}).get("tamano"), dict) else None
            if isinstance(t_h, (int, float)) and isinstance(t_p, (int, float)) and t_h > t_p and _vacio(e.get("x_diferencia_declarada")):
                R.falla("G3B-MET-20", f"{eid}: tamaño mayor que el de su padre {e['padre']} sin diferencia declarada")
        for a in (e.get("metricas") or {}).get("actores") or []:
            if a.get("cuota") is None:
                R.falla("G3B-MET-20", f"{eid}: actor {a.get('nombre')} sin cuota")
        # SEL-18 · emergentes
        vig = json.dumps(p.get("mapa_cobertura") or {}, ensure_ascii=False)
        for g in e.get("emergentes") or []:
            gid = g.get("emg_id") or g.get("nombre")
            if g.get("tipo") not in ht03.TIPOS_EMERGENTE or g.get("via_exposicion") not in ht03.VIAS_EXPOSICION:
                R.falla("G3B-SEL-18", f"{gid}: tipo o vía de exposición fuera del vocabulario")
            if g.get("etiqueta") not in ENUMS["etiqueta"]:
                R.falla("G3B-SEL-18", f"{gid}: sin etiqueta epistémica")
            if "S" in g:
                R.falla("G3B-SEL-18", f"{gid}: emergente presentado con S")
            try:
                if not g.get("criterios") or ht03.calcular_PEM(g["criterios"])["total"] != g.get("PEM"):
                    R.falla("G3B-SEL-18", f"{gid}: PEM no reconstruible con HT-03")
            except ht03.ErrorEntrada as ex:
                R.falla("G3B-SEL-18", f"{gid}: PEM no reconstruible ({ex})")
            if g.get("via_exposicion") in ht03.VIAS_INVERTIBLES:
                ie = g.get("instrumento_exposicion") or {}
                pendiente = str(ie.get("motivo") or "").lower().startswith("selección pendiente")
                if _vacio(ie.get("nombre")) or (ie.get("cand_id") is None and not ie.get("fuera_de_filtros") and not pendiente):
                    R.falla("G3B-SEL-18", f"{gid}: emergente invertible que no pasó al universo del Seleccionador sin marca «fuera de filtros»")
            elif g.get("nombre") and g["nombre"] not in vig:
                R.falla("G3B-SEL-18", f"{gid}: vía {g.get('via_exposicion')} ausente de la vigilancia del mapa de cobertura")
    if "omisiones" not in m:
        R.falla("G3B-MET-20", "Mapa sin «omisiones» (eslabones omitidos con motivo)")
    # SEL-16 · eslabon_id en todo candidato
    for c in candidatos_top(p):
        if c.get("eslabon_id") not in ids:
            R.falla("G3B-SEL-16", f"{c.get('cand_id')}: eslabon_id {c.get('eslabon_id')!r} ausente o fuera del mapa")
        for x in c.get("eslabones_secundarios") or []:
            if x not in ids:
                R.falla("G3B-SEL-16", f"{c.get('cand_id')}: eslabón secundario {x} fuera del mapa")
    for lst in (p.get("paquete_para_bloque_C") or {}).values():
        for x in lst or []:
            if x.get("eslabon_id") not in ids:
                R.falla("G3B-SEL-16", f"{x.get('cand_id')}: encargo C.x sin eslabon_id del mapa")
    # SEL-17 · mejores opciones por eslabón (9.13)
    n_max = 3 if nivel == "N1" else 5
    tops = {c.get("cand_id"): c for c in candidatos_top(p)}
    vistos: Dict[str, str] = {}
    inv = v.get("valor") in ("INVERTIR", "INVERTIR_ESCALONADO") or p.get("x_candidatos_aun_con_vigilar")
    for e in esl:
        ops = e.get("opciones") or []
        if len(ops) > n_max:
            R.falla("G3B-SEL-17", f"{e.get('eslabon_id')}: {len(ops)} opciones (máximo {n_max})")
        if nivel == "N1" and ops and m.get("eslabon_critico") and e.get("eslabon_id") != m["eslabon_critico"]:
            R.falla("G3B-SEL-17", f"{e.get('eslabon_id')}: en N1 solo el eslabón crítico lleva opciones")
        orden = [(-(o.get("S") or 0), -(o.get("pureza_eslabon") or 0)) for o in ops]
        if orden != sorted(orden):
            R.falla("G3B-SEL-17", f"{e.get('eslabon_id')}: opciones no ordenadas por S y pureza al eslabón")
        for o in ops:
            cid = o.get("cand_id")
            if cid in vistos:
                R.falla("G3B-SEL-17", f"{cid} figura en dos tablas ({vistos[cid]} y {e.get('eslabon_id')})")
            vistos[cid] = e.get("eslabon_id")
            if not isinstance(o.get("S"), (int, float)) or o["S"] < 50:
                R.falla("G3B-SEL-17", f"{cid}: opción con S < 50")
            if o.get("veredicto") not in ("PRIORITARIO_PARA_C", "SECUNDARIO"):
                R.falla("G3B-SEL-17", f"{cid}: veredicto {o.get('veredicto')!r} no válido en una tabla por eslabón")
            if o.get("veredicto") == "PRIORITARIO_PARA_C" and (o["S"] < 65 or not inv):
                R.falla("G3B-SEL-17", f"{cid}: PRIORITARIO_PARA_C indebido en la tabla por eslabón")
            if bool(o.get("en_top_n_tipo")) != (cid in tops):
                R.falla("G3B-SEL-17", f"{cid}: marca en_top_n_tipo incoherente con el top-N (¿CAND-B duplicado?)")
            if cid in tops and (tops[cid].get("S") != o.get("S") or tops[cid].get("veredicto") != o.get("veredicto")):
                R.falla("G3B-SEL-17", f"{cid}: la tabla por eslabón no reproduce S o veredicto del top-N")
            if cid in tops and tops[cid].get("eslabon_id") != e.get("eslabon_id"):
                R.falla("G3B-SEL-17", f"{cid}: opción fuera de la tabla de su eslabón principal")
    if nivel in ("N2", "N3"):
        refutados = {o.get("objeto") for o in (p.get("refutacion") or {}).get("objeciones") or []} | \
            set(((p.get("refutacion") or {}).get("veredicto_candidatos") or {}))
        for cid, o in opciones_adicionales(p).items():
            if o.get("veredicto") == "PRIORITARIO_PARA_C" and cid not in refutados:
                R.falla("G3B-SEL-17", f"{cid}: opción añadida por cobertura sin refutación (N2/N3)")
    # MET-18 · puertas de viabilidad (R33)
    cap = p.get("capas") or {}
    pv = cap.get("puertas_viabilidad") or {}
    forz = cap.get("continuacion_forzada") or {}
    pf = forz.get("puerta") if isinstance(forz, dict) else None
    for g in ("PV1", "PV2"):
        r_ = _pv_resultado(pv, g)
        if r_ not in ("SUPERADA", "NO_SUPERADA", "FORZADA"):
            R.falla("G3B-MET-18", f"{g} sin resultado registrado")
        elif r_ in ("NO_SUPERADA", "FORZADA") and pf != g:
            R.falla("G3B-MET-18", f"{g} no superada y entrega completa sin continuación forzada registrada (R33)")
    if _pv_resultado(pv, "PV3") not in ("SUPERADA", "NO_SUPERADA", "FORZADA", "NO_EVALUADA"):
        R.falla("G3B-MET-18", "PV3 sin resultado registrado")
    pv2d = ((cap.get("detalle") or {}).get("PV2") or {})
    if _pv_resultado(pv, "PV2") == "SUPERADA" and isinstance(pv2d.get("A"), (int, float)) and isinstance(pv2d.get("E"), (int, float)):
        if not ht03.evaluar_pv2(pv2d["A"], pv2d["E"], pv2d.get("tesis_viva", True))["resultado"] == "SUPERADA":
            R.falla("G3B-MET-18", f"PV2 SUPERADA con A {pv2d['A']} y E {pv2d['E']} provisionales bajo umbral")
    if _pv_resultado(pv, "PV3") == "NO_SUPERADA":
        if v.get("valor") not in ("VIGILAR", "DESCARTAR"):
            R.falla("G3B-MET-18", "PV3 no superada con veredicto distinto de VIGILAR o DESCARTAR")
        if any(c.get("veredicto") == "PRIORITARIO_PARA_C" for c in tops.values()) or any((p.get("paquete_para_bloque_C") or {}).values()):
            R.falla("G3B-MET-18", "PV3 no superada con candidatos prioritarios o encargos C.x (selección incompleta)")
        if v.get("resultado_del_analisis") != "PARCIAL":
            R.falla("G3B-MET-18", "PV3 no superada sin resultado PARCIAL")
    # TMP-05 · tiempo por capa
    tc = p.get("tiempo_consumo") or {}
    if _vacio(cap.get("minutos_por_capa")) or _vacio(tc.get("por_capa_min")):
        R.falla("G3B-TMP-05", "Sin tiempo real por capa")
    if tc.get("opcion_autorizada") == "HASTA_PV2" and _pv_resultado(pv, "PV2") == "SUPERADA" and len(tc.get("autorizaciones") or []) < 2:
        R.falla("G3B-TMP-05", "PV2 superada con autorización HASTA_PV2 sin nueva CT-B-05 para las capas 3 y 4")
    # CON-20 · continuación forzada declarada
    if pf:
        frase = f"continuación forzada por el broker tras {pf.lower()} no superada"
        if not any(frase in str(x).lower() for x in p.get("limitaciones") or []):
            R.falla("G3B-CON-20", f"Falta la declaración «continuación forzada por el Broker tras {pf} no superada»")
    # MET-21 · lista de comprobación profesional (8.10)
    lp = p.get("lista_profesional") or []
    items = {x.get("item"): x for x in lp if isinstance(x, dict)}
    exig = range(1, 23) if nivel in ("N2", "N3", "PERS") else ITEMS_N1
    for i in exig:
        x = items.get(i)
        if not x:
            R.falla("G3B-MET-21", f"Ítem {i} de la lista profesional ausente")
        elif x.get("estado") not in ESTADOS_LISTA:
            R.falla("G3B-MET-21", f"Ítem {i}: estado {x.get('estado')!r} no válido")
        elif _vacio(x.get("referencia")):
            R.falla("G3B-MET-21", f"Ítem {i}: sin referencia o motivo")
    # MET-22 · H5 (R13, 8.6) y CON-10 ampliada: horizonte principal aplicable al tipo de objeto
    hz = est.get("horizonte_dominante")
    obj = (p.get("ambito") or {}).get("tipo_objeto")
    if hz in ht03.HORIZONTES and obj in TABLA_HORIZONTES_OBJETO and TABLA_HORIZONTES_OBJETO[obj][ht03.HORIZONTES.index(hz)] == "NO":
        R.falla("G3B-CON-10", f"Horizonte principal {hz} no aplicable al tipo de objeto {obj} (8.6)")
    for h2 in est.get("horizontes_secundarios") or []:
        if h2 not in ht03.HORIZONTES or h2 == hz:
            R.falla("G3B-CON-10", f"Horizonte secundario no válido: {h2!r}")
    h5 = [x for x in p.get("pronosticos_detalle") or [] if x.get("horizonte") == "H5" or x.get("tipo") == "HITO_H5"]
    if hz == "H5" or h5:
        if any(x.get("probabilidad_publicada") is not None for x in h5):
            R.falla("G3B-MET-22", "Probabilidad numérica publicada en H5 (R13: siempre cualitativa)")
        if hz == "H5" and any(e.get("probabilidad") is not None for e in p.get("escenarios") or []):
            R.falla("G3B-MET-22", "Escenario H5 con probabilidad numérica")
        hitos = [x for x in h5 if x.get("tipo") == "HITO_H5"]
        f0 = _fecha(p.get("fecha"))
        if hz == "H5" and len(hitos) < 3:
            R.falla("G3B-MET-22", f"Tesis H5 con {len(hitos)} hitos intermedios (mínimo 3, Anexo A)")
        for x in hitos:
            fr = _fecha(x.get("fecha_resolucion"))
            if not (f0 and fr and 365 <= (fr - f0).days <= 5 * 366) or _vacio(x.get("criterio")):
                R.falla("G3B-MET-22", f"{x.get('prg_id')}: hito sin criterio o con fecha fuera de 1–5 años")
        if hz == "H5" and (est.get("profundidad") or {}).get("D9") in ("P0", "P1"):
            R.falla("G3B-MET-22", "H5 con D9 por debajo de P2")
    # EST-14 · consultas al Broker (R34, B.12, Anexo A) y CON-21 · supuestos aplicados
    cons = p.get("consultas_broker") or []
    lim, lim_b = LIMITE_CONSULTAS.get(nivel, (3, 1))
    if len(cons) > lim or sum(1 for q in cons if q.get("modo") == "BLOQUEANTE") > lim_b:
        R.falla("G3B-EST-14", f"Consultas por encima del límite del nivel {nivel} ({lim}, bloqueantes {lim_b})")
    supuestos = {str(x.get("cns_id")) for x in p.get("supuestos_aplicados") or []}
    textos_lim = " ".join(str(x) for x in p.get("limitaciones") or [])
    for q in cons:
        cid = q.get("cns_id")
        if not _ide("cns_id", cid) or (f1 is not None and cid not in f1):
            R.falla("G3B-EST-14", f"Consulta {cid!r} no válida o inexistente en F1")
        if q.get("tipo") not in TIPOS_CONSULTA or q.get("modo") not in ("BLOQUEANTE", "NO_BLOQUEANTE") or _vacio(q.get("supuesto")):
            R.falla("G3B-EST-14", f"{cid}: tipo, modo o supuesto declarado no válidos (R34)")
        if RE_SECRETO.search(json.dumps(q, ensure_ascii=False)) or RE_PERSONAL.search(json.dumps(q, ensure_ascii=False)):
            R.falla("G3B-EST-14", f"{cid}: consulta con credenciales, datos personales, cartera o perfil")
        if q.get("resolucion") not in ("RESPONDIDA", "SUPUESTO_APLICADO", "RESPUESTA_TARDIA"):
            R.falla("G3B-CON-21", f"{cid}: consulta sin cerrar en la entrega ({q.get('resolucion')!r})")
        if q.get("resolucion") in ("SUPUESTO_APLICADO", "RESPUESTA_TARDIA") and (str(cid) not in supuestos or str(cid) not in textos_lim):
            R.falla("G3B-CON-21", f"{cid}: supuesto aplicado sin declarar en «supuestos_aplicados» y en las limitaciones")


def _ent_v21(p: Dict, R: Registro, html: Optional[str], mapa_md: Optional[str], textos: Dict[str, Optional[str]]) -> None:
    esl = (p.get("mapa_cadena_valor") or {}).get("eslabones") or []
    pf = ((p.get("capas") or {}).get("continuacion_forzada") or {}).get("puerta")
    for nombre, t in textos.items():      # CON-20 y CON-21 en los entregables (F9)
        if t is None:
            continue
        if pf and "continuación forzada" not in t.lower():
            R.falla("G3B-CON-20", f"El {nombre} no declara la continuación forzada tras {pf}")
        for x in p.get("supuestos_aplicados") or []:
            if str(x.get("cns_id")) not in t:
                R.falla("G3B-CON-21", f"El {nombre} no declara el supuesto aplicado {x.get('cns_id')}")
    if mapa_md is not None:
        R.ok("G3B-ENT-11", "G3B-DAT-08")
        if p.get("data_cutoff") and str(p["data_cutoff"]) not in mapa_md:
            R.falla("G3B-DAT-08", "El mapa por eslabón no declara la fecha de corte del paquete")
        for k in ("Árbol", "Síntesis"):
            if k.lower() not in mapa_md.lower():
                R.falla("G3B-ENT-11", f"Mapa por eslabón sin la sección «{k}»")
        aes = [(e.get("atractivo") or {}).get("AE") for e in esl]
        if aes != sorted(aes, reverse=True):
            R.falla("G3B-ENT-11", "Eslabones del mapa no ordenados por AE descendente")
        for e in esl:
            if e.get("eslabon_id") not in mapa_md:
                R.falla("G3B-ENT-11", f"{e.get('eslabon_id')} ausente del mapa por eslabón")
            ae = (e.get("atractivo") or {}).get("AE")
            if ae is not None and f"AE = {ae}" not in mapa_md:
                R.falla("G3B-ENT-11", f"{e.get('eslabon_id')}: AE {ae} no coincide con el paquete")
            for o in e.get("opciones") or []:
                if o.get("cand_id") not in mapa_md:
                    R.falla("G3B-ENT-11", f"{o.get('cand_id')} ausente de la tabla de {e.get('eslabon_id')}")
            for g in e.get("emergentes") or []:
                if g.get("nombre") and g["nombre"] not in mapa_md:
                    R.falla("G3B-ENT-11", f"Emergente {g['nombre']} ausente de la subtabla de {e.get('eslabon_id')}")
        if _pv_resultado((p.get("capas") or {}).get("puertas_viabilidad") or {}, "PV3") == "NO_SUPERADA" and "PV3 no superada" not in mapa_md:
            R.falla("G3B-ENT-11", "PV3 no superada sin la explicación de por qué ningún eslabón ofrece opciones")
        if RE_FRONTERA_C.search(mapa_md):
            R.falla("G3B-ENT-11", "El mapa por eslabón cita un precio objetivo (frontera con C)")
    else:
        R.na("G3B-ENT-11", "mapa por eslabón no proporcionado")
    if html is not None:
        R.ok("G3B-ENT-12")
        cual = [e for e in esl if e.get("opciones") and ht03.eslabon_cualifica(e)["cualifica"]]
        nombres_mapa = {str(o.get("nombre")) for e in esl for o in e.get("opciones") or []}
        if cual:
            if 'id="t-eslabones"' not in html:
                R.falla("G3B-ENT-12", "El informe visual no incluye las tablas simplificadas por eslabón (14.2)")
            if AVISO_TABLAS_ESLABON.lower() not in ht07.extraer_texto_html(html).lower():
                R.falla("G3B-ENT-12", "Tablas por eslabón sin el rótulo «Activos que el análisis ha estudiado; no son recomendaciones; tu Broker decide»")
        for blo in re.findall(r'<table class="eslabon".*?</table>', html, flags=re.S):
            if blo.count('<tr class="opcion"') > 3:
                R.falla("G3B-ENT-12", "Tabla por eslabón con más de tres opciones (top-3)")
            sin_nombres = re.sub(r'(<tr class="opcion"><td[^>]*>).*?(</td>)', r"\1\2", blo)     # el nombre del activo puede llevar cifras
            if re.search(r"\bS\s*=|\bAE\s*=|precio objetivo|\d+\s?(M€|€|%)", sin_nombres):
                R.falla("G3B-ENT-12", "Tabla por eslabón del informe visual con S, precios o tamaños")
            for n_ in re.findall(r'<tr class="opcion"><td[^>]*>(.*?)</td>', blo):
                if nombres_mapa and html_unescape(n_) not in nombres_mapa:
                    R.falla("G3B-ENT-12", f"Opción «{n_}» del informe visual que no figura en el entregable 6")
    else:
        R.na("G3B-ENT-12", "informe visual no proporcionado")


def html_unescape(t: str) -> str:
    import html as _h
    return _h.unescape(re.sub(r"<[^>]+>", "", t)).strip()


# ==============================================================================================================
# Perfiles reducidos PAR (informe de parada, B.15) y CIC (informe de seguimiento, B.14)
# ==============================================================================================================
CRITERIOS_PARADA = ("SIN_INVERTIBILIDAD", "ALERTA_GRAVE", "BIBLIOTECA_DESCARTAR", "MATERIALIDAD", "YA_DESCONTADO",
                    "SIN_MECANISMO", "A_PROVISIONAL", "E_PROVISIONAL", "TESIS_REFUTADA")
PERFIL_PAR = ("G3B-EST-05", "G3B-EST-06", "G3B-EST-12", "G3B-EST-14", "G3B-MET-18", "G3B-CON-15", "G3B-CON-16", "G3B-CON-19",
              "G3B-CON-21", "G3B-DAT-08", "G3B-TMP-05")
PERFIL_CIC = ("G3B-EST-05", "G3B-EST-06", "G3B-EST-13", "G3B-CON-15", "G3B-CON-16", "G3B-CON-21", "G3B-SEL-16", "G3B-DAT-08",
              "G3B-TMP-06")


def _resultado_parcial(R: Registro, codigos: Sequence[str], perfil: str) -> Dict:
    res = [c for c in R.resultados() if c["id"] in codigos]
    return {"herramienta": "HT-09", "version": VERSION, "perfil": perfil, "dictamen": R.dictamen(), "comprobaciones": res,
            "resumen": {r: sum(1 for c in res if c["resultado"] == r) for r in ("PASA", "FALLA", "NO_APLICA")},
            "motivo": "; ".join(f"{c['id']}: {c['detalles'][0]}" for c in res
                                if c["resultado"] == "FALLA" and c.get("clase_fallo") == "B")[:2000] or None}


def _comunes_reducidos(R: Registro, inf: Dict, markdown: Optional[str], nombre: str) -> None:
    texto = json.dumps(inf, ensure_ascii=False) + (markdown or "")
    _seguridad({nombre: texto}, R)
    R.ok("G3B-CON-15", "G3B-CON-16")
    if RE_ASESORAMIENTO.search(texto):
        R.falla("G3B-CON-15", f"Lenguaje de asesoramiento en el {nombre}")
    if RE_FRONTERA_C.search(texto):
        R.falla("G3B-CON-16", f"El {nombre} cita un precio objetivo (frontera con C)")
    R.ok("G3B-CON-21")
    for x in inf.get("supuestos_aplicados") or []:
        if markdown is not None and str(x.get("cns_id")) not in markdown:
            R.falla("G3B-CON-21", f"Supuesto aplicado {x.get('cns_id')} no declarado en el Markdown del {nombre}")
    if markdown is not None:
        R.ok("G3B-DAT-08")
        if str(inf.get("data_cutoff")) not in markdown:
            R.falla("G3B-DAT-08", f"El Markdown del {nombre} no declara data_cutoff {inf.get('data_cutoff')}")


def validar_informe_parada(inf: Dict, markdown: Optional[str] = None, f1: Optional[Dict] = None) -> Dict:
    """Perfil PAR (7.11, 14.7, B.15): EST-12 esquema, CON-19 contenido, MET-18 puerta y criterios, TMP-05 tiempo por
    capa, EST-14 consultas, CON-21 supuestos, DAT-08 fecha de corte, seguridad y frontera."""
    R = Registro()
    R.ok("G3B-EST-12", "G3B-CON-19", "G3B-MET-18", "G3B-TMP-05", "G3B-EST-14")
    for k in ("pet_id", "run_id", "rec_id", "fecha", "data_cutoff", "ambito", "capa", "puerta", "motivos", "que_lo_cambiaria",
              "sugerencia", "veredicto_registrado", "resultado_del_analisis", "lo_que_ya_se_sabe", "tiempo_consumo",
              "forzar_continuacion", "aviso"):
        if k not in inf:
            R.falla("G3B-EST-12", f"Falta «{k}»")
    if _vacio((inf.get("tiempo_consumo") or {}).get("por_capa_min")):
        R.falla("G3B-TMP-05", "Informe de parada sin tiempo por capa")
    if inf.get("puerta") not in ("PV1", "PV2") or inf.get("capa") not in (1, 2) or \
            {"PV1": 1, "PV2": 2}.get(inf.get("puerta")) != inf.get("capa"):
        R.falla("G3B-MET-18", "Puerta o capa no válidas o incoherentes (PV1 en la capa 1; PV2 en la capa 2)")
    crit = [mo.get("criterio") for mo in inf.get("motivos") or []]
    if inf.get("puerta") == "PV1" and crit:
        ins = {"tipos_con_invertible": 0 if "SIN_INVERTIBILIDAD" in crit else 1, "instrumentos_invertibles": 0 if "MATERIALIDAD" in crit else 99,
               "alerta_integridad": "ALERTA_GRAVE" in crit, "biblioteca_descartar_sin_cambio": "BIBLIOTECA_DESCARTAR" in crit,
               "ya_descontado": "YA_DESCONTADO" in crit, "sin_mecanismo": "SIN_MECANISMO" in crit}
        if ht03.evaluar_pv1(ins)["resultado"] != "NO_SUPERADA":
            R.falla("G3B-MET-18", "Los criterios declarados no bastan para no superar PV1 (un eliminatorio o dos de debilidad)")
    for mo in inf.get("motivos") or []:
        if mo.get("criterio") not in CRITERIOS_PARADA or mo.get("clase") not in ("ELIMINATORIO", "DEBILIDAD", "UMBRAL"):
            R.falla("G3B-EST-12", f"Motivo fuera del vocabulario: {mo.get('criterio')!r}")
        if mo.get("etiqueta") not in ENUMS["etiqueta"] or _vacio(mo.get("evidencia")):
            R.falla("G3B-CON-19", f"Motivo {mo.get('criterio')} sin evidencia o sin etiqueta epistémica")
    puntos = inf.get("por_que_no_merece_seguir") or []
    if not (3 <= len(puntos) <= 6):
        R.falla("G3B-CON-19", f"«Por qué no merece seguir» con {len(puntos)} puntos (tres a seis, 7.11)")
    sug = inf.get("sugerencia")
    if sug not in ("DESCARTAR", "PONER_EN_SEGUIMIENTO"):
        R.falla("G3B-EST-12", f"Sugerencia no válida: {sug!r}")
    if inf.get("veredicto_registrado") != {"DESCARTAR": "DESCARTAR", "PONER_EN_SEGUIMIENTO": "VIGILAR"}.get(sug):
        R.falla("G3B-CON-19", "Veredicto registrado incoherente con la sugerencia (7.11)")
    if sug == "PONER_EN_SEGUIMIENTO" and (_vacio((inf.get("seguimiento_propuesto") or {}).get("frecuencia"))
                                          or _vacio((inf.get("seguimiento_propuesto") or {}).get("senales_de_interes"))):
        R.falla("G3B-CON-19", "Sugerencia de seguimiento sin frecuencia ni señales propuestas")
    if inf.get("resultado_del_analisis") != "DETENIDO_EN_PUERTA":
        R.falla("G3B-CON-19", "resultado_del_analisis distinto de DETENIDO_EN_PUERTA")
    if any(k in inf for k in ("candidatos_por_tipo", "paquete_para_bloque_C", "pronosticos")):
        R.falla("G3B-CON-19", "Un informe de parada no genera candidatos, encargos C.x ni pronósticos (7.11)")
    if not inf.get("que_lo_cambiaria"):
        R.falla("G3B-EST-12", "Sin «qué lo cambiaría»")
    for x in inf.get("supuestos_aplicados") or []:
        if f1 is not None and x.get("cns_id") not in f1:
            R.falla("G3B-EST-14", f"Consulta {x.get('cns_id')} inexistente en F1")
    _comunes_reducidos(R, inf, markdown, "informe de parada")
    if markdown is not None:
        for mo in inf.get("motivos") or []:
            if mo.get("criterio") not in markdown:
                R.falla("G3B-CON-19", f"Motivo {mo.get('criterio')} ausente del Markdown")
        if sug and sug not in markdown:
            R.falla("G3B-CON-19", "Sugerencia ausente del Markdown")
    return _resultado_parcial(R, PERFIL_PAR, "PAR")


def validar_informe_seguimiento(inf: Dict, markdown: Optional[str] = None, seg_activo: Optional[bool] = None) -> Dict:
    """Perfil CIC (7.13, 14.8, B.14): EST-13 esquema, TMP-06 ciclo N1-SEG, SEL-16, CON-21, DAT-08, seguridad y frontera."""
    R = Registro()
    R.ok("G3B-EST-13", "G3B-TMP-06", "G3B-SEL-16")
    for k in ("seg_id", "ciclo_id", "run_id", "fecha", "data_cutoff", "objeto", "semaforo", "resumen", "que_ha_cambiado",
              "senales", "disparadores", "candidatos", "actualizacion_F6", "recomendacion", "motivo", "proximo_ciclo",
              "tiempo_consumo", "nota"):
        if k not in inf:
            R.falla("G3B-EST-13", f"Falta «{k}»")
    if not _ide("seg_id", inf.get("seg_id")) or not _ide("ciclo_id", inf.get("ciclo_id")):
        R.falla("G3B-EST-13", "Identificadores SEG-B o CIC-B no válidos")
    if seg_activo is False:
        R.falla("G3B-EST-13", "SEG-B sin estado ACTIVO en F11")
        R.falla("G3B-TMP-06", "Ciclo sin seguimiento activo (R35)")
    if inf.get("semaforo") not in ("VERDE", "AMBAR", "ROJO"):
        R.falla("G3B-EST-13", f"Semáforo no válido: {inf.get('semaforo')!r}")
    rec = inf.get("recomendacion")
    if rec not in ("MANTENER_VIGILANCIA", "REACTIVAR_ANALISIS_PROFUNDO", "PROPONER_PASAR_A_C", "CANCELAR_SEGUIMIENTO"):
        R.falla("G3B-EST-13", f"Recomendación no válida: {rec!r}")
    if "no ha iniciado" not in str(inf.get("nota", "")).lower():
        R.falla("G3B-EST-13", "Falta la nota «el bloque no ha iniciado ningún análisis profundo» (R35)")
    if rec == "REACTIVAR_ANALISIS_PROFUNDO" and any(_vacio((inf.get("peticion_sugerida") or {}).get(k)) for k in ("nivel", "alcance", "estimacion_min_p80")):
        R.falla("G3B-TMP-06", "Reactivar el análisis sin petición sugerida (nivel, alcance y estimación)")
    if rec == "PROPONER_PASAR_A_C" and _vacio(inf.get("candidatos_propuestos_para_C")):
        R.falla("G3B-EST-13", "Proponer pasar a C sin candidatos")
    tc = inf.get("tiempo_consumo") or {}
    if isinstance(tc.get("estimado_p80_min"), (int, float)) and tc["estimado_p80_min"] > 30 and _vacio(tc.get("autorizaciones")):
        R.falla("G3B-TMP-06", "Ciclo con estimación > 30 min sin AUT-B (PT30)")
    if any(_vacio(x.get("motivo_delta")) for x in inf.get("rondas_delta") or []):
        R.falla("G3B-TMP-06", "Ronda delta encargada sin valor informativo declarado")
    for x in inf.get("senales") or []:
        if x.get("estado") not in ("NORMAL", "PROXIMO", "ALCANZADO"):
            R.falla("G3B-EST-13", f"Señal {x.get('sig_id')}: estado no válido")
    for x in inf.get("disparadores") or []:
        if x.get("estado") not in ("NO_ALCANZADO", "PROXIMO", "ALCANZADO") or x.get("origen") not in ("BROKER", "PLAN"):
            R.falla("G3B-EST-13", f"Disparador «{x.get('descripcion')}»: estado u origen no válidos")
    for c in inf.get("candidatos") or []:
        if not re.fullmatch(RE_ESLABON, str(c.get("eslabon_id") or "")):
            R.falla("G3B-SEL-16", f"Candidato vigente {c.get('cand_id')} sin eslabon_id")
    f0, fp = _fecha(inf.get("fecha")), _fecha(inf.get("proximo_ciclo"))
    if rec != "CANCELAR_SEGUIMIENTO" and not (f0 and fp and fp > f0):
        R.falla("G3B-EST-13", "Próximo ciclo ausente o no posterior a la fecha del ciclo")
    _comunes_reducidos(R, inf, markdown, "informe de seguimiento")
    if markdown is not None:
        for k in ("seg_id", "ciclo_id", "semaforo", "recomendacion"):
            if str(inf.get(k)) not in markdown:
                R.falla("G3B-EST-13", f"El Markdown no declara {k} = {inf.get(k)}")
    return _resultado_parcial(R, PERFIL_CIC, "CIC")


def validar(paquete: Dict, certificados: Optional[List[Dict]] = None, informe_visual: Optional[str] = None,
            informe_tecnico: Optional[str] = None, memorando: Optional[str] = None, f2: Optional[Dict] = None,
            esquema: Optional[Dict] = None, anexo: Optional[str] = None, rutas: Optional[Dict[str, str]] = None,
            parametros_f10: Optional[Dict] = None, preguntas: Optional[List[str]] = None,
            mapa_eslabones: Optional[str] = None, f1: Optional[Dict] = None) -> Dict:
    if not isinstance(paquete, dict):
        raise ErrorEntrada("El paquete debe ser un objeto JSON")
    R = Registro()
    _est(paquete, R, esquema, parametros_f10)
    _dat(paquete, R, f2)
    punt = _met(paquete, R, parametros_f10)
    _con(paquete, R, punt, certificados, preguntas)
    _sel(paquete, R)
    _tmp(paquete, R)
    _v21(paquete, R, f1)
    textos = {"paquete": "\n".join(_textos({k: v for k, v in paquete.items() if k != "origen"})),
              "informe visual": informe_visual or "", "informe técnico": informe_tecnico or "", "memorando": memorando or "",
              "mapa por eslabón": mapa_eslabones or ""}
    _seguridad(textos, R)
    _ent(paquete, R, informe_visual, informe_tecnico, memorando, anexo, rutas)
    _ent_v21(paquete, R, informe_visual, mapa_eslabones, {"informe técnico": informe_tecnico, "memorando": memorando})
    for c in ("G3B-EST-12", "G3B-EST-13", "G3B-CON-19", "G3B-TMP-06"):
        R.na(c, "perfil PAR o CIC: se valida con validar_informe_parada / validar_informe_seguimiento")
    res = R.resultados()
    segunda = any(x is not None for x in (informe_visual, informe_tecnico, memorando, anexo, mapa_eslabones))
    d = R.dictamen()
    return {"herramienta": "HT-09", "version": VERSION, "dictamen": d, "pet_id": paquete.get("pet_id"),
            "pasada": "FIDELIDAD_ENTREGABLES" if segunda else "PAQUETE_SINTESIS", "comprobaciones": res,
            "resumen": {r: sum(1 for c in res if c["resultado"] == r) for r in ("PASA", "FALLA", "NO_APLICA")},
            "motivo": "; ".join(f"{c['id']}: {c['detalles'][0]}" for c in res
                                if c["resultado"] == "FALLA" and c.get("clase_fallo") == "B")[:2000] or None}


def _leer(ruta: Optional[str]) -> Optional[str]:
    if not ruta:
        return None
    with open(ruta, encoding="utf-8") as fh:
        return fh.read()


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="HT-09 · Validador determinista G3 del Bloque B (catálogo G3B)")
    ap.add_argument("paquete", help="paquete_analisis_mercado (JSON)")
    ap.add_argument("--certificados", help="JSON con la lista de certificados vigentes")
    ap.add_argument("--visual", help="Informe visual (HTML)")
    ap.add_argument("--tecnico", help="Informe técnico (Markdown)")
    ap.add_argument("--memorando", help="Memorando ejecutivo (Markdown)")
    ap.add_argument("--anexo", help="Anexo de datos (XLSX)")
    ap.add_argument("--f2", help="JSON {ids, trazas, dat, evd_estados, calc_estados} con el extracto de F2 y RC")
    ap.add_argument("--f10", help="JSON con parámetros de F10 (methodology_version, pesos)")
    ap.add_argument("--esquema", help="Esquema JSON del paquete (requiere jsonschema)")
    ap.add_argument("--salida")
    a = ap.parse_args(argv)
    try:
        paq = json.loads(_leer(a.paquete))
        res = validar(paq, json.loads(_leer(a.certificados)) if a.certificados else None, _leer(a.visual),
                      _leer(a.tecnico), _leer(a.memorando), json.loads(_leer(a.f2)) if a.f2 else None,
                      json.loads(_leer(a.esquema)) if a.esquema else None, a.anexo, None,
                      json.loads(_leer(a.f10)) if a.f10 else None)
    except (ErrorEntrada, json.JSONDecodeError, OSError) as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 3
    txt = json.dumps(res, ensure_ascii=False, indent=2)
    if a.salida:
        with open(a.salida, "w", encoding="utf-8") as fh:
            fh.write(txt)
    else:
        print(txt)
    return {"APTO": 0, "APTO_CON_ADVERTENCIAS": 1, "BLOQUEADO": 2}[res["dictamen"]]


if __name__ == "__main__":
    sys.exit(main())
