#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HT-03 · Calculadora determinista de puntuaciones, veredictos y rankings (implementación de referencia).

Bloque B · Robot Investor · V2.0 (actualizado V2.1, 03/11/2026) · Subordinada al Documento 0 del Bloque B, óptima V2.1
(secciones 2.6, 7.9, 7.10, 8.3, 8.5, 8.6, 8.7.2–8.7.4, 9.1–9.8, 9.12–9.13 y Anexo A).

Calcula, sin modelo de lenguaje y con aritmética exacta (fracciones):

  * Estrategia (8.3): pesos de la matriz tipo de objeto × dimensión, moduladores por horizonte (8.3.2) y por
    tipo de activo material (8.3.3, media geométrica si hay varios), desviaciones del Director (±5 puntos),
    renormalización a 100 con enteros (mayor resto), profundidad P0–P3 por la regla determinista (peso ≥ 12 → P3;
    7–11 → P2; 4–6 → P1; ≤ 3 → P0), mínimos D9 ≥ P2 y D12 ≥ P1, ajustes por nivel (N1 un escalón menos con
    mínimo P1 y D9/D12 en P2; N3 peso ≥ 9 → P3) y activación de especialistas (8.3.4).
  * Puntuaciones del ámbito (9.1): A y E como media ponderada de componentes 0–100 en múltiplos de 10 (o «NA» /
    «NE»), redondeada al múltiplo de 5; NA redistribuye su peso; NE puntúa 0; máximo dos NA/NE por puntuación;
    tope por saturación narrativa (componente «valoracion_expectativas» de A ≤ 40). RF desde el veredicto de la
    refutación y las objeciones moderadas sin resolver; C = 0,20·A + 0,35·E + 0,25·RF + 0,20·RE con tope
    C ≤ E + 10 (redondeo al entero).
  * Banda marginal (≤ 5 puntos de un umbral del ámbito; ≤ 3 del candidato o del corte del top-N): con segunda
    pasada se usa el menor valor; sin ella, PA7 (ámbito) o PC7 (candidato) limitan.
  * Veredicto del ámbito (9.2–9.3) con PA1–PA8 y orden de cálculo de tres pasos; relevancia decisional y
    siguiente paso (7.9).
  * Selección (9.4–9.7): normalización de métricas (winsorización 2,5/97,5 y percentiles en el universo
    cribado, inversión de métricas inversas, subgrupos), componentes PE, QL, VA, MO, RI, LA y CO por playbook
    (NA redistribuye, NE puntúa 0, más de dos NE excluyen), S redondeado al entero, puertas PC1–PC8, top-N y
    alternativas con las reglas de diversidad y no duplicación, veredictos del candidato y apuestas
    independientes.
  * V2.1: horizonte H5 (moduladores de 8.3.2); AG-B24 en la activación (8.3.4); puntuación del cuello de botella
    PCB = round(100 × severidad × persistencia × relevancia / 125) con indicadores en semáforo (8.7.2, 9.12, Anexo A);
    atractivo del eslabón AE y potencial del emergente PEM (9.12, 8.7.3); puertas de viabilidad PV1–PV3 (7.10);
    mejores opciones por eslabón, hasta cinco y adicionales al top-N sin duplicarlo (9.13).

Entrada y salida JSON (CLI: `python3 ht03_puntuaciones.py entrada.json [--salida salida.json]`). Solo biblioteca
estándar. Estado de madurez (R26): implementada (referencia), pruebas unitarias superadas; integrada en el
ejecutor `bloque_b` como copia literal.
"""
from __future__ import annotations

import argparse
import copy
import json
import math
import sys
from fractions import Fraction
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

VERSION = "2.1"

DIMENSIONES = tuple(f"D{i}" for i in range(1, 13))
TIPOS_OBJETO = ("SECTOR", "TEMATICA", "MERCADO_GEOGRAFICO", "SEGMENTO_DE_CLASE", "ESTRATEGIA_FACTOR", "CADENA_DE_VALOR")
TIPOS_ACTIVO = ("RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV")
BLOQUE_C = {t: f"C.{i}" for i, t in enumerate(TIPOS_ACTIVO, start=1)}
HORIZONTES = ("H1", "H2", "H3", "H4", "H5")
NIVELES = ("N0", "N1", "N2", "N3", "PERS")
VEREDICTOS_AMBITO = ("INVERTIR", "INVERTIR_ESCALONADO", "VIGILAR", "DESCARTAR")
VEREDICTOS_CANDIDATO = ("PRIORITARIO_PARA_C", "SECUNDARIO", "EXCLUIDO")
MOTIVOS_EXCLUSION = ("NO_INVERTIBLE", "PUREZA_INSUFICIENTE", "DATOS_INSUFICIENTES", "ALERTA_CRITICA", "S_INSUFICIENTE",
                     "REFUTADO", "DUPLICADO", "FUERA_DE_MARCO")
COMPONENTES_S = ("PE", "QL", "VA", "MO", "RI", "LA", "CO")
PUERTAS_AMBITO = tuple(f"PA{i}" for i in range(1, 9))
PUERTAS_CANDIDATO = tuple(f"PC{i}" for i in range(1, 9))

# --------------------------------------------------------------------------------------------------------------
# Matriz de estrategia (8.3.1): peso inicial por tipo de objeto (columnas suman 100)
# --------------------------------------------------------------------------------------------------------------
MATRIZ = {
    "SECTOR":             dict(zip(DIMENSIONES, (5, 10, 9, 13, 7, 7, 9, 12, 12, 5, 4, 7))),
    "TEMATICA":           dict(zip(DIMENSIONES, (8, 13, 6, 12, 13, 8, 5, 7, 11, 7, 4, 6))),
    "MERCADO_GEOGRAFICO": dict(zip(DIMENSIONES, (5, 8, 4, 6, 3, 13, 17, 9, 13, 9, 5, 8))),
    "SEGMENTO_DE_CLASE":  dict(zip(DIMENSIONES, (7, 9, 10, 6, 3, 7, 13, 8, 14, 11, 4, 8))),
    "ESTRATEGIA_FACTOR":  dict(zip(DIMENSIONES, (9, 3, 2, 3, 2, 4, 15, 8, 17, 15, 4, 18))),
    "CADENA_DE_VALOR":    dict(zip(DIMENSIONES, (6, 10, 14, 17, 10, 9, 5, 10, 9, 3, 3, 4))),
}
# 8.3.2 · moduladores por horizonte dominante
MOD_HORIZONTE = {  # H1, H2, H3, H4, H5 (8.3.2)
    "D1": (1.0, 1.0, 1.0, 1.0, 1.0), "D2": (0.3, 0.6, 1.0, 1.3, 1.5), "D3": (0.6, 0.8, 1.0, 1.2, 1.2),
    "D4": (0.3, 0.6, 1.0, 1.3, 1.4), "D5": (0.2, 0.5, 1.0, 1.4, 1.7), "D6": (1.0, 1.0, 1.0, 1.1, 1.1),
    "D7": (1.3, 1.3, 1.0, 0.9, 0.7), "D8": (0.6, 1.0, 1.0, 1.1, 1.0), "D9": (0.8, 1.0, 1.1, 1.2, 1.0),
    "D10": (2.2, 1.6, 1.0, 0.6, 0.3), "D11": (0.3, 0.5, 1.0, 1.3, 1.6), "D12": (1.8, 1.4, 1.0, 1.0, 1.0),
}
# 8.3.3 · moduladores por tipo de activo material
MOD_TIPO = {
    "RV": {"D8": 1.2, "D9": 1.1}, "RF": {"D7": 1.3, "D8": 1.2, "D5": 0.5},
    "DIV": {"D7": 1.5, "D6": 1.2, "D4": 0.3, "D5": 0.3}, "MP": {"D3": 1.5, "D2": 1.2, "D6": 1.2, "D8": 0.7},
    "IDX": {"D7": 1.2, "D9": 1.2, "D4": 0.7}, "FON": {"D10": 1.3, "D9": 1.1},
    "DER": {"D10": 1.4, "D12": 1.3, "D9": 1.2}, "INM": {"D7": 1.3, "D3": 1.2, "D6": 1.1},
    "CRI": {"D5": 1.3, "D10": 1.4, "D6": 1.3, "D8": 0.7}, "ALT": {"D8": 1.2, "D9": 1.2, "D10": 0.7},
    "MON": {"D7": 1.8, "D9": 1.2, "D4": 0.3, "D5": 0.3}, "TCV": {"D7": 1.6, "D12": 1.2, "D4": 0.3, "D5": 0.3},
}
# 8.3.4 · activación de especialistas: L líder · A activado · C condicional · — no activado
ESPECIALISTAS = {
    "AG-B03": ("D1", "D4"), "AG-B04": ("D2",), "AG-B05": ("D3",), "AG-B06": ("D5",), "AG-B07": ("D6",),
    "AG-B08": ("D7",), "AG-B09": ("D8", "D9"), "AG-B10": ("D10",), "AG-B11": ("D11", "D12"),
}
ACTIVACION = {  # columnas: SECTOR, TEMATICA, MERCADO_GEOGRAFICO, SEGMENTO_DE_CLASE, ESTRATEGIA_FACTOR, CADENA_DE_VALOR
    "AG-B03": ("L", "L", "C", "A", "C", "L"), "AG-B04": ("A", "L", "A", "A", "—", "A"),
    "AG-B05": ("A", "A", "C", "A", "—", "L"), "AG-B06": ("A", "L", "—", "C", "—", "A"),
    "AG-B07": ("A", "A", "L", "A", "C", "A"), "AG-B08": ("A", "C", "L", "L", "L", "C"),
    "AG-B09": ("L", "A", "L", "L", "L", "A"), "AG-B10": ("C", "A", "A", "A", "L", "C"),
    "AG-B11": ("A", "A", "A", "A", "A", "C"),
}
# AG-B24 · especialista transversal (no es dueño de una dimensión: alimenta D4 —actores emergentes— y D5; 8.3.4)
ACTIVACION_EMG = ("A", "A", "C", "C", "C", "A")
# AG-B05 es líder en SEGMENTO_DE_CLASE cuando el segmento es de MP, INM o RF por emisión (8.3.4)
LIDER_AG_B05_SEGMENTO = ("MP", "INM", "RF")

# --------------------------------------------------------------------------------------------------------------
# Puntuaciones del ámbito (9.1) y umbrales (Anexo A)
# --------------------------------------------------------------------------------------------------------------
PARAMETROS_POR_DEFECTO: Dict[str, Any] = {
    "pesos": {
        "A": {"asimetria": 25, "valoracion_expectativas": 20, "calidad_crecimiento": 15, "ventaja_estructural": 10,
              "catalizadores": 10, "momento_flujos": 10, "riesgos": 10},
        "E": {"calidad_raices": 25, "cobertura_dimensional": 15, "calidad_metodologica": 15, "trazabilidad": 15,
              "actualidad": 10, "discrepancias_resueltas": 10, "hipotesis_cerradas": 10},
        "C": {"A": Fraction(20, 100), "E": Fraction(35, 100), "RF": Fraction(25, 100), "RE": Fraction(20, 100)},
    },
    "tope_C_sobre_E": 10,
    "tope_saturacion_valoracion": 40,
    "umbrales_ambito": {"INVERTIR": {"A": 65, "E": 60, "C": 65}, "INVERTIR_ESCALONADO": {"A": 60, "E": 60, "C": 55},
                        "VIGILAR": {"A": 50}},
    "gc2": {"A": 50, "E": 50},
    "banda_marginal_ambito": 5,
    "banda_marginal_candidato": 3,
    "umbrales_candidato": {"PRIORITARIO_PARA_C": 65, "ic90_inferior_prioritario": 55, "SECUNDARIO": 50},
    "top_n": {"N1": (3, 0), "N2": (5, 2), "N3": (10, 5)},
    "gc3_multiplo": 2,
    "diversidad": {"solapamiento_duplicado": 0.80, "max_emisiones_por_emisor_RF": 2, "max_frac_subcluster": 0.40,
                   "correlacion_duplicado": 0.90},
    "max_ne_candidato": 2,
    "desviacion_max_director": 5,
    # V2.1 · puertas de viabilidad (7.10, Anexo A)
    "pv1": {"materialidad_min_meur": 2000, "materialidad_min_instrumentos": 3, "max_debilidades": 1},
    "pv3": {"AE_min": 60, "PCB_min": 30, "rojos_min": 2, "S_min": 50},
    # V2.1 · cuellos de botella, eslabones y emergentes (8.7.2, 8.7.3, 9.12, 9.13, Anexo A)
    "pesos_AE": {"crecimiento": 20, "margen_roic": 20, "poder_negociacion": 15, "cuello": 20, "expectativas_inv": 15,
                 "sustitucion_inv": 10},
    "pesos_PEM": {"tecnologia": 20, "traccion": 25, "equipo": 15, "financiacion": 15, "posicion_cadena": 15,
                  "via_exposicion": 10},
    "eslabon_atractivo_AE": 60,
    "cuello_material": {"PCB": 30, "rojos": 2},
    "mejores_por_eslabon": {"N1": 3, "N2": 5, "N3": 5, "PERS": 5},
    # (ámbar, rojo) por indicador; «sentido» = por_encima | por_debajo (8.7.2, Anexo A)
    "umbrales_cuello": {
        "utilizacion": (0.85, 0.90, "por_encima"), "plazo_entrega_ratio": (1.5, 2.0, "por_encima"),
        "book_to_bill": (1.1, 1.2, "por_encima"), "hhi_proveedores": (1500, 2500, "por_encima"),
        "cuota_primer_pais": (0.40, 0.60, "por_encima"), "margen_sobre_adyacentes_pp": (5, 10, "por_encima"),
        "spot_contrato": (1.15, 1.30, "por_encima"), "capacidad_vs_deficit": (1.0, 1.0001, "por_encima"),
        "permisos_meses": (12, 24, "por_encima"), "inventarios_percentil": (25, 10, "por_debajo"),
        "insumo_sin_sustituto": (1, 1, "por_encima")},
}

# --------------------------------------------------------------------------------------------------------------
# Playbooks (8.5): pesos de S (None = NA), mínimo de pureza PC2 y métricas por componente
# (métrica, peso interno, inversa). Las métricas de precio las calcula el Motor (MC-B01/MC-B07) con HT-01.
# --------------------------------------------------------------------------------------------------------------
PLAYBOOKS: Dict[str, Dict[str, Any]] = {
    "RV": {"perfil": "SEL-RV", "pesos": {"PE": 20, "QL": 20, "VA": 20, "MO": 15, "RI": 15, "LA": 10, "CO": None},
           "pureza_min": 0.25, "metricas": {
               "PE": [("pureza", 1, False)],
               "QL": [("roic", 2, False), ("margen_operativo_rel", 1, False), ("deuda_neta_ebitda", 1, True), ("piotroski", 1, False)],
               "VA": [("per_relativo", 1, True), ("fcf_yield", 1, False), ("brecha_crecimiento_implicito", 1, True)],
               "MO": [("revisiones_bpa_3m", 1, False), ("momento_12_1", 1, False)],
               "RI": [("volatilidad_1a", 1, True), ("beta", 1, True), ("concentracion_clientes", 1, True)],
               "LA": [("volumen_medio_meur", 1, False)], "CO": []},
           "alertas_criticas": ("dimision_auditor", "investigacion_fraude", "impago_reestructuracion"),
           "referencia_ranking": "media equiponderada del universo cribado"},
    "RF": {"perfil": "SEL-RF", "pesos": {"PE": 15, "QL": 25, "VA": 25, "MO": 5, "RI": 15, "LA": 15, "CO": None},
           "pureza_min": 0.25, "metricas": {
               "PE": [("pureza", 1, False)],
               "QL": [("calificacion_num", 2, False), ("deuda_ebitda", 1, True), ("cobertura_intereses", 1, False)],
               "VA": [("diferencial_vs_curva_pb", 1, False), ("z_diferencial", 1, False), ("rentabilidad_esperada_neta", 1, False)],
               "MO": [("cambio_diferencial_3m_pb", 1, True)],
               "RI": [("duracion", 1, True), ("subordinacion", 1, True)],
               "LA": [("saldo_vivo_meur", 1, False), ("horquilla_pb", 1, True), ("denominacion_min_eur", 1, True)], "CO": []},
           "alertas_criticas": ("impago", "diferimiento_cupones", "procedimiento_concursal", "calificacion_retirada"),
           "referencia_ranking": "rentabilidad total media equiponderada del universo cribado, ajustada por duración"},
    "DIV": {"perfil": "SEL-DIV", "pesos": {"PE": 10, "QL": 15, "VA": 25, "MO": 15, "RI": 15, "LA": 10, "CO": 10},
            "pureza_min": None, "metricas": {
                "PE": [("pureza", 1, False)],
                "QL": [("cuenta_corriente_pib", 1, False), ("reservas_meses_importacion", 1, False), ("inflacion", 1, True)],
                "VA": [("infravaloracion_ppa", 1, False), ("carry_ajustado_vol", 1, False)],
                "MO": [("momento_3m", 1, False), ("momento_12m", 1, False)],
                "RI": [("volatilidad_1a", 1, True)], "LA": [("horquilla_pb", 1, True)], "CO": [("coste_instrumento_pct", 1, True)]},
            "alertas_criticas": ("controles_capital", "regimen_cambiario_en_revision", "sanciones"),
            "referencia_ranking": "media equiponderada de los pares cribados"},
    "MP": {"perfil": "SEL-MP", "pesos": {"PE": 20, "QL": 10, "VA": 20, "MO": 15, "RI": 10, "LA": 15, "CO": 10},
           "pureza_min": 0.80, "metricas": {
               "PE": [("pureza", 1, False)], "QL": [("calidad_emisor", 1, False)],
               "VA": [("roll_yield", 1, False), ("percentil_coste_marginal", 1, True)],
               "MO": [("momento_12_1", 1, False)], "RI": [("volatilidad_1a", 1, True)],
               "LA": [("volumen_medio_meur", 1, False)], "CO": [("ter", 1, True), ("coste_roll_pct", 1, True)]},
           "alertas_criticas": ("suspension_creaciones", "problema_custodio", "liquidacion_fisica_no_apta"),
           "referencia_ranking": "media equiponderada de los instrumentos cribados"},
    "IDX": {"perfil": "SEL-IDX", "pesos": {"PE": 25, "QL": 15, "VA": 20, "MO": 15, "RI": 10, "LA": 10, "CO": 5},
            "pureza_min": 0.60, "metricas": {
                "PE": [("pureza", 1, False)], "QL": [("concentracion_top10", 1, True), ("rotacion_anual", 1, True)],
                "VA": [("per_adelantado_rel", 1, True), ("prima_riesgo_implicita", 1, False)],
                "MO": [("momento_12_1", 1, False)], "RI": [("volatilidad_1a", 1, True), ("caida_maxima_1a", 1, True)],
                "LA": [("activos_vehiculos_meur", 1, False)], "CO": [("ter_minimo", 1, True)]},
            "alertas_criticas": ("revision_metodologia_material",),
            "referencia_ranking": "media de los índices alternativos cribados"},
    "FON": {"perfil": "SEL-FON", "pesos": {"PE": 25, "QL": 20, "VA": 10, "MO": 5, "RI": 10, "LA": 15, "CO": 15},
            "pureza_min": 0.50, "metricas": {
                "PE": [("pureza", 1, False)],
                "QL": [("diferencia_seguimiento_pct", 1, True), ("error_seguimiento_pct", 1, True)],
                "VA": [("valoracion_cartera_rel", 1, True)], "MO": [("flujos_netos_6m_pct", 1, False)],
                "RI": [("concentracion_top10", 1, True), ("replica_sintetica", 1, True)],
                "LA": [("volumen_medio_meur", 1, False), ("patrimonio_meur", 1, False)], "CO": [("ter", 1, True)]},
            "alertas_criticas": ("suspension_reembolsos", "anuncio_cierre_fusion"),
            "referencia_ranking": "media equiponderada de los vehículos cribados (rentabilidad neta)"},
    "DER": {"perfil": "SEL-DER", "pesos": {"PE": 20, "QL": None, "VA": 25, "MO": 5, "RI": 20, "LA": 20, "CO": 10},
            "pureza_min": 0.60, "metricas": {
                "PE": [("pureza", 1, False)], "QL": [],
                "VA": [("vol_implicita_menos_realizada", 1, True), ("base_vs_teorico_pct", 1, True)],
                "MO": [("momento_3m", 1, False)], "RI": [("apalancamiento", 1, True), ("perdida_maxima_pct", 1, True)],
                "LA": [("interes_abierto", 1, False), ("volumen_contratos", 1, False)],
                "CO": [("coste_roll_pct", 1, True), ("horquilla_pb", 1, True)]},
            "alertas_criticas": ("subyacente_suspendido", "emisor_en_dificultades"),
            "referencia_ranking": "estrategia equiponderada sobre los instrumentos cribados"},
    "INM": {"perfil": "SEL-INM", "pesos": {"PE": 15, "QL": 20, "VA": 25, "MO": 10, "RI": 15, "LA": 10, "CO": 5},
            "pureza_min": 0.50, "metricas": {
                "PE": [("pureza", 1, False)],
                "QL": [("ocupacion", 1, False), ("duracion_contratos_anos", 1, False), ("coste_deuda", 1, True)],
                "VA": [("descuento_nav", 1, False), ("rentabilidad_affo", 1, False)],
                "MO": [("momento_12_1", 1, False)], "RI": [("ltv", 1, True), ("vencimientos_24m_pct", 1, True)],
                "LA": [("volumen_medio_meur", 1, False)], "CO": [("gastos_gav", 1, True)]},
            "alertas_criticas": ("incumplimiento_covenants", "ampliacion_forzosa", "salvedades_valoraciones"),
            "referencia_ranking": "media equiponderada del universo cribado"},
    "CRI": {"perfil": "SEL-CRI", "pesos": {"PE": 15, "QL": 20, "VA": 20, "MO": 15, "RI": 15, "LA": 10, "CO": 5},
            "pureza_min": 0.50, "metricas": {
                "PE": [("pureza", 1, False)],
                "QL": [("comisiones_anuales_musd", 1, False), ("direcciones_activas_miles", 1, False), ("desarrolladores", 1, False)],
                "VA": [("cap_sobre_comisiones", 1, True), ("mvrv", 1, True)],
                "MO": [("momento_3m", 1, False)],
                "RI": [("volatilidad_1a", 1, True), ("desbloqueos_90d_pct", 1, True), ("concentracion_tenedores", 1, True)],
                "LA": [("volumen_medio_meur", 1, False)], "CO": [("coste_custodia_pct", 1, True)]},
            "alertas_criticas": ("hackeo_no_resuelto", "investigacion_penal_fundadores", "exclusion_mica"),
            "referencia_ranking": "media equiponderada del universo cribado"},
    "ALT": {"perfil": "SEL-ALT", "pesos": {"PE": 15, "QL": 20, "VA": 20, "MO": 5, "RI": 15, "LA": 10, "CO": 15},
            "pureza_min": 0.50, "metricas": {
                "PE": [("pureza", 1, False)], "QL": [("pme", 1, False), ("dpi", 1, False)],
                "VA": [("descuento_nav", 1, False)], "MO": [("momento_12_1", 1, False)],
                "RI": [("apalancamiento", 1, True)], "LA": [("volumen_medio_meur", 1, False)],
                "CO": [("comisiones_totales_pct", 1, True)]},
            "alertas_criticas": ("suspension_reembolsos", "nav_no_publicado", "valoraciones_sin_auditar"),
            "referencia_ranking": "media equiponderada del universo cribado"},
    "MON": {"perfil": "SEL-MON", "pesos": {"PE": 5, "QL": 25, "VA": 30, "MO": None, "RI": 10, "LA": 15, "CO": 15},
            "pureza_min": None, "metricas": {
                "PE": [("pureza", 1, False)], "QL": [("calificacion_corto_num", 1, False), ("vmp_dias", 1, True)],
                "VA": [("rentabilidad_neta_vs_estr_pb", 1, False)], "MO": [],
                "RI": [("riesgo_reinversion", 1, True)], "LA": [("patrimonio_meur", 1, False)], "CO": [("ter", 1, True)]},
            "alertas_criticas": ("suspension_reembolsos", "calificacion_bajo_minimo"),
            "referencia_ranking": "media de los instrumentos cribados"},
    "TCV": {"perfil": "SEL-TCV", "pesos": {"PE": 25, "QL": None, "VA": 25, "MO": 5, "RI": 15, "LA": 15, "CO": 15},
            "pureza_min": 0.70, "metricas": {
                "PE": [("pureza", 1, False)], "QL": [],
                "VA": [("carry_rolldown_pct", 1, False), ("desviacion_valor_razonable", 1, False)],
                "MO": [("momento_3m", 1, False)],
                "RI": [("volatilidad_1a", 1, True), ("deterioro_roll_pct", 1, True)],
                "LA": [("volumen_medio_meur", 1, False)], "CO": [("ter", 1, True), ("coste_roll_pct", 1, True)]},
            "alertas_criticas": ("riesgo_liquidacion_anticipada",),
            "referencia_ranking": "media de los instrumentos cribados"},
}


class ErrorEntrada(ValueError):
    """Entrada no conforme."""


# ==============================================================================================================
# Utilidades aritméticas
# ==============================================================================================================
def _frac(x) -> Fraction:
    if isinstance(x, Fraction):
        return x
    if isinstance(x, float):
        return Fraction(str(x))
    return Fraction(x)


def redondear(valor, paso: int = 1) -> int:
    """Redondeo al múltiplo de `paso` más próximo; los empates exactos se resuelven hacia abajo (prudencia)."""
    v = _frac(valor) / paso
    piso = math.floor(v)
    resto = v - piso
    return int((piso + (1 if resto > Fraction(1, 2) else 0)) * paso)


def _num(f) -> float:
    return float(round(float(f), 4))


def fusionar_parametros(extra: Optional[Dict]) -> Dict:
    p = copy.deepcopy(PARAMETROS_POR_DEFECTO)

    def fus(a, b):
        for k, v in (b or {}).items():
            if isinstance(v, dict) and isinstance(a.get(k), dict):
                fus(a[k], v)
            else:
                a[k] = v
    fus(p, extra or {})
    return p


# ==============================================================================================================
# Estrategia (8.3)
# ==============================================================================================================
def _mayor_resto(valores: Dict[str, Fraction], total: int = 100) -> Dict[str, int]:
    s = sum(valores.values())
    if s <= 0:
        raise ErrorEntrada("Pesos nulos tras modular")
    escal = {k: v * total / s for k, v in valores.items()}
    base = {k: math.floor(v) for k, v in escal.items()}
    faltan = total - sum(base.values())
    orden = sorted(escal, key=lambda k: (-(escal[k] - base[k]), DIMENSIONES.index(k) if k in DIMENSIONES else 0))
    for k in orden[:faltan]:
        base[k] += 1
    return base


def profundidad_por_peso(peso: float) -> str:
    """Regla determinista de 8.3.1: ≥ 12 → P3 · 7–11 → P2 · 4–6 → P1 · ≤ 3 → P0."""
    if peso >= 12:
        return "P3"
    if peso >= 7:
        return "P2"
    if peso >= 4:
        return "P1"
    return "P0"


_ORDEN_P = ("P0", "P1", "P2", "P3")


def _max_p(a: str, b: str) -> str:
    return a if _ORDEN_P.index(a) >= _ORDEN_P.index(b) else b


def estrategia(tipo_objeto: str, horizonte: str, tipos_materiales: Sequence[str] = (), nivel: str = "N2",
               desviaciones: Optional[Dict[str, int]] = None, segmento_tipo: Optional[str] = None,
               params: Optional[Dict] = None) -> Dict:
    """Pesos efectivos, profundidad y activación de especialistas (8.3). `tipos_materiales` son los tipos de activo
    con peso material en la tesis (8.3.3); `desviaciones` (dimensión → puntos) son las del Director (±5)."""
    p = fusionar_parametros(params)
    if tipo_objeto not in MATRIZ:
        raise ErrorEntrada(f"tipo_objeto desconocido: {tipo_objeto}")
    if horizonte not in HORIZONTES:
        raise ErrorEntrada(f"horizonte desconocido: {horizonte}")
    ih = HORIZONTES.index(horizonte)
    base = {d: _frac(MATRIZ[tipo_objeto][d]) * _frac(MOD_HORIZONTE[d][ih]) for d in DIMENSIONES}
    tipos_materiales = [t for t in tipos_materiales if t in MOD_TIPO]
    if tipos_materiales:
        for d in DIMENSIONES:
            fac = [MOD_TIPO[t].get(d, 1.0) for t in tipos_materiales]
            g = math.prod(fac) ** (1.0 / len(fac))   # media geométrica (8.3.3)
            base[d] = base[d] * _frac(round(g, 6))
    pesos = _mayor_resto(base)
    avisos: List[str] = []
    desv_aplicadas: List[Dict] = []
    if desviaciones:
        lim = p["desviacion_max_director"]
        ajust = {d: Fraction(pesos[d]) for d in DIMENSIONES}
        for d, v in desviaciones.items():
            if d not in ajust:
                raise ErrorEntrada(f"Desviación sobre dimensión desconocida {d}")
            v2 = max(-lim, min(lim, int(v)))
            if v2 != int(v):
                avisos.append(f"Desviación de {d} ({v}) recortada a ±{lim}: una desviación mayor exige motivo sustantivo (8.3.4)")
            ajust[d] = max(Fraction(0), ajust[d] + v2)
            desv_aplicadas.append({"dim": d, "puntos": v2})
        pesos = _mayor_resto(ajust)
    prof = {d: profundidad_por_peso(pesos[d]) for d in DIMENSIONES}
    # Mínimos de 8.3.1
    prof["D9"] = _max_p(prof["D9"], "P2")
    prof["D12"] = _max_p(prof["D12"], "P1")
    if nivel == "N1":
        # 8.3.4 y A.2: un escalón menos (mínimo P1); D9 y D12 se mantienen en P2 solo si su profundidad modulada ya
        # era P2 o superior (D9 lo es siempre por el mínimo de 8.3.1)
        previa = dict(prof)
        for d in DIMENSIONES:
            i = _ORDEN_P.index(prof[d])
            prof[d] = _ORDEN_P[max(1, i - 1)]
        for d in ("D9", "D12"):
            if _ORDEN_P.index(previa[d]) >= 2:
                prof[d] = _max_p(prof[d], "P2")
    elif nivel == "N3":
        for d in DIMENSIONES:
            if pesos[d] >= 9:
                prof[d] = "P3"
    col = TIPOS_OBJETO.index(tipo_objeto)
    activacion: Dict[str, Dict] = {}
    for ag, dims in ESPECIALISTAS.items():
        codigo = ACTIVACION[ag][col]
        if ag == "AG-B05" and tipo_objeto == "SEGMENTO_DE_CLASE" and segmento_tipo in LIDER_AG_B05_SEGMENTO:
            codigo = "L"
        peso_max = max(pesos[d] for d in dims)
        if codigo == "C":
            activo = peso_max > 4 or nivel == "N3"
            motivo = ("peso modulado > 4" if peso_max > 4 else "N3: condicionales activados") if activo else "peso modulado ≤ 4"
        elif codigo == "—":
            activo, motivo = False, "no se activa por defecto (la dimensión la cubre el Director)"
        else:
            activo, motivo = True, "líder" if codigo == "L" else "activado"
        if nivel == "N1" and codigo != "L":
            activo, motivo = False, "N1: solo se activan los líderes"
        activacion[ag] = {"codigo": codigo, "activo": activo, "motivo": motivo, "dimensiones": list(dims)}
    # AG-B24 (8.3.4, condición propia): C → D4 o D5 con peso ≥ 7 tras modular, o N3; en N1 solo en las celdas A
    # (limitado al eslabón crítico). Transversal: no se le asignan dimensiones propias.
    cod = ACTIVACION_EMG[col]
    if cod == "A":
        act, mot = True, "activado (celda A)"
    else:
        peso = max(pesos["D4"], pesos["D5"])
        act = peso >= 7 or nivel == "N3"
        mot = (f"D4/D5 con peso {peso} ≥ 7" if peso >= 7 else "N3: condicionales activados") if act else \
            f"D4/D5 con peso {peso} < 7 (sin disparador)"
    if nivel == "N1" and cod != "A":
        act, mot = False, "N1: AG-B24 solo en las celdas A"
    elif nivel == "N1":
        mot += "; N1: limitado al eslabón crítico"
    activacion["AG-B24"] = {"codigo": cod, "activo": act, "motivo": mot, "dimensiones": [], "transversal": True,
                            "alimenta": ["D4", "D5"]}
    lideres = sorted({d for ag, a in activacion.items() if a["codigo"] == "L" and a["activo"] for d in a["dimensiones"]})
    capa2 = [d for d in DIMENSIONES if d in set(lideres) | {"D2", "D4", "D8", "D9"} and prof[d] != "P0"]
    exclusiones_admisibles = [d for d in DIMENSIONES if prof[d] == "P0"]
    return {"herramienta": "HT-03", "version": VERSION, "tipo_objeto": tipo_objeto, "horizonte_dominante": horizonte,
            "nivel": nivel, "tipos_materiales": list(tipos_materiales), "pesos_efectivos": pesos,
            "profundidad": prof, "activacion": activacion, "exclusiones_admisibles": exclusiones_admisibles,
            "dimensiones_capa2": capa2, "dimensiones_capa3": [d for d in DIMENSIONES if d not in capa2],
            "desviaciones": desv_aplicadas, "avisos": avisos}


# ==============================================================================================================
# Puntuaciones del ámbito (9.1)
# ==============================================================================================================
def calcular_puntuacion(nombre: str, comps: Dict[str, Any], pesos: Dict[str, Any], max_na_ne: int = 2,
                        paso: int = 5, multiplos_de_10: bool = True) -> Dict:
    """Media ponderada de componentes; NA redistribuye, NE puntúa 0; máximo `max_na_ne` NA/NE."""
    faltan = [k for k in pesos if k not in comps]
    if faltan:
        raise ErrorEntrada(f"{nombre}: faltan componentes {faltan}")
    extra = [k for k in comps if k not in pesos]
    if extra:
        raise ErrorEntrada(f"{nombre}: componentes desconocidos {extra}")
    na = [k for k, v in comps.items() if v == "NA"]
    ne = [k for k, v in comps.items() if v == "NE"]
    for k, v in comps.items():
        if v in ("NA", "NE"):
            continue
        if not isinstance(v, (int, float)) or isinstance(v, bool) or v < 0 or v > 100:
            raise ErrorEntrada(f"{nombre}.{k}: valor {v!r} fuera de 0–100")
        if multiplos_de_10 and (int(v) != v or int(v) % 10):
            raise ErrorEntrada(f"{nombre}.{k}: {v} no es múltiplo de 10")
    if len(na) + len(ne) > max_na_ne:
        return {"nombre": nombre, "calculable": False, "total": None, "motivo": f"más de {max_na_ne} NA/NE",
                "na": na, "ne": ne}
    activos = {k: _frac(w) for k, w in pesos.items() if k not in na}
    suma_w = sum(activos.values())
    if suma_w == 0:
        return {"nombre": nombre, "calculable": False, "total": None, "motivo": "pesos nulos", "na": na, "ne": ne}
    exacto = sum(w * (0 if comps[k] == "NE" else _frac(comps[k])) for k, w in activos.items()) / suma_w
    return {"nombre": nombre, "calculable": True, "total": redondear(exacto, paso), "exacto": _num(exacto),
            "pesos_efectivos": {k: _num(w * 100 / suma_w) for k, w in activos.items()}, "na": na, "ne": ne}


def calcular_A(comps: Dict[str, Any], saturacion_narrativa: bool = False, params: Optional[Dict] = None) -> Dict:
    p = fusionar_parametros(params)
    c = dict(comps)
    aplicado = False
    if saturacion_narrativa and isinstance(c.get("valoracion_expectativas"), (int, float)):
        tope = p["tope_saturacion_valoracion"]
        if c["valoracion_expectativas"] > tope:
            c["valoracion_expectativas"] = tope
            aplicado = True
    r = calcular_puntuacion("A", c, p["pesos"]["A"])
    r["tope_saturacion_aplicado"] = aplicado
    r["componentes"] = c
    return r


def calcular_E(comps: Dict[str, Any], params: Optional[Dict] = None) -> Dict:
    p = fusionar_parametros(params)
    r = calcular_puntuacion("E", comps, p["pesos"]["E"])
    r["componentes"] = dict(comps)
    return r


def calcular_RF(veredicto_tesis: Optional[str], moderadas_sin_resolver: int = 0) -> int:
    """RF (9.1): robusta 100 · frágil 50 · refutada 0; −10 por objeción moderada sin resolver; mínimo 0."""
    base = {"robusta": 100, "fragil": 50, "frágil": 50, "refutada": 0}.get((veredicto_tesis or "").lower())
    if base is None:
        raise ErrorEntrada(f"veredicto_tesis desconocido: {veredicto_tesis!r}")
    return max(0, base - 10 * int(moderadas_sin_resolver))


def calcular_C(A: int, E: int, RF: int, RE: Optional[int], params: Optional[Dict] = None) -> Dict:
    """C (9.1). RE puede ser None («NA»: en N1 sin simulación PLAN_MIN, A.2): su peso se redistribuye."""
    p = fusionar_parametros(params)
    w = dict(p["pesos"]["C"])
    vals = {"A": A, "E": E, "RF": RF, "RE": RE}
    if RE is None or RE == "NA":
        del w["RE"]
        del vals["RE"]
    for n, v in vals.items():
        if v is None or v < 0 or v > 100:
            raise ErrorEntrada(f"C: {n} fuera de 0–100 ({v})")
    exacto = sum(w[k] * _frac(vals[k]) for k in w) / sum(w.values())
    valor = redondear(exacto, 1)
    tope = E + p["tope_C_sobre_E"]
    aplicado = valor > tope
    if aplicado:
        valor = tope
    lectura = "alta" if valor >= 70 else ("media" if valor >= 50 else "baja")
    return {"C": valor, "exacto": _num(exacto), "tope": tope, "tope_aplicado": aplicado, "lectura": lectura,
            "formula": "C = 0,20·A + 0,35·E + 0,25·RF + 0,20·RE; C ≤ E + 10"}


def en_banda_marginal(valor: Optional[float], umbrales: Iterable[float], margen: float) -> List[float]:
    if valor is None:
        return []
    return [u for u in umbrales if abs(valor - u) <= margen]


# ==============================================================================================================
# Veredicto del ámbito (9.2–9.3) y relevancia (7.9)
# ==============================================================================================================
def veredicto_ambito_provisional(A: int, E: int, C: int, puertas: Dict[str, str], flags: Optional[Dict] = None,
                                 params: Optional[Dict] = None) -> Dict:
    """Paso 1 del orden de cálculo: veredicto con A, E, C y PA1–PA8 (sin la condición de candidatos).
    `puertas`: PA1…PA8 → «OK» o «BLOQUEA». `flags`: tesis_refutada, integridad (PA8 por integridad),
    catalizadores_escalonados, valoracion_parcialmente_descontada, dispersion_alta."""
    p = fusionar_parametros(params)
    flags = flags or {}
    u = p["umbrales_ambito"]
    bloquean = [g for g in PUERTAS_AMBITO if puertas.get(g, "OK") != "OK"]
    motivos: List[str] = []
    if flags.get("tesis_refutada"):
        return {"veredicto": "DESCARTAR", "motivo": "tesis refutada (PA5)", "puertas_bloqueantes": bloquean,
                "motivo_descarte": "sin tesis defendible"}
    if flags.get("integridad"):
        return {"veredicto": "DESCARTAR", "motivo": "PA8 por integridad", "puertas_bloqueantes": bloquean,
                "motivo_descarte": "integridad"}
    if A < u["VIGILAR"]["A"]:
        return {"veredicto": "DESCARTAR", "motivo": f"A < {u['VIGILAR']['A']}", "puertas_bloqueantes": bloquean,
                "motivo_descarte": flags.get("motivo_descarte") or "ya descontado o sin tesis defendible"}
    cumple_inv = A >= u["INVERTIR"]["A"] and E >= u["INVERTIR"]["E"] and C >= u["INVERTIR"]["C"]
    cumple_esc = A >= u["INVERTIR_ESCALONADO"]["A"] and E >= u["INVERTIR_ESCALONADO"]["E"] and \
        C >= u["INVERTIR_ESCALONADO"]["C"]
    escalonar = any(flags.get(k) for k in ("catalizadores_escalonados", "valoracion_parcialmente_descontada",
                                           "dispersion_alta"))
    if bloquean:
        motivos.append("puertas " + ", ".join(bloquean) + " limitan a VIGILAR")
        v = "VIGILAR"
    elif cumple_inv and not escalonar:
        v = "INVERTIR"
    elif cumple_esc and (escalonar or 55 <= C <= 64 or cumple_inv):
        v = "INVERTIR_ESCALONADO"
        motivos.append("condiciones de escalonamiento" if escalonar or cumple_inv else "C entre 55 y 64")
    else:
        v = "VIGILAR"
        motivos.append("no se cumplen los umbrales de INVERTIR ni de INVERTIR_ESCALONADO")
    return {"veredicto": v, "motivo": "; ".join(motivos) or "umbrales y puertas superados", "puertas_bloqueantes": bloquean,
            "motivo_descarte": None}


def relevancia_decisional(veredicto: str, A: int, E: int, riesgo_1a5: int, horizonte: str,
                          iliquidez: bool = False, tipos_prioritarios: Sequence[str] = (),
                          disparador_cercano: bool = False) -> Tuple[str, List[str]]:
    """Regla de 7.9."""
    motivos = []
    inv = veredicto in ("INVERTIR", "INVERTIR_ESCALONADO")
    if inv and riesgo_1a5 >= 4:
        motivos.append("INVERTIR con riesgo ≥ 4/5")
    if horizonte in ("H4", "H5") and iliquidez:
        motivos.append(f"{horizonte} con iliquidez")
    alto = sorted(set(tipos_prioritarios) & {"CRI", "ALT", "DER"})
    if alto:
        motivos.append("tipos " + ", ".join(alto) + " entre los prioritarios")
    if E < 70 and A >= 75:
        motivos.append("E < 70 con A ≥ 75")
    if motivos:
        return "ALTA", motivos
    if inv or (veredicto == "VIGILAR" and disparador_cercano):
        return "MEDIA", ["INVERTIR/ESCALONADO" if inv else "VIGILAR con disparador cercano"]
    return "BAJA", ["VIGILAR sin disparador cercano" if veredicto == "VIGILAR" else "DESCARTAR"]


def siguiente_paso(veredicto: str, prioritarios: int, resultado: str = "CONCLUYENTE", relevancia: str = "MEDIA",
                   E: int = 100) -> str:
    """Regla del bloque (7.9; concreción declarada en HT-03): ENVIAR_CANDIDATOS_A_C si el veredicto es INVERTIR o
    INVERTIR_ESCALONADO con prioritarios; PROFUNDIZAR_EN_B si es VIGILAR con resultado PARCIAL/NO_CONCLUYENTE o con
    relevancia ALTA y E < 70; VIGILAR o DESCARTAR en el resto."""
    if veredicto in ("INVERTIR", "INVERTIR_ESCALONADO") and prioritarios > 0:
        return "ENVIAR_CANDIDATOS_A_C"
    if veredicto == "DESCARTAR":
        return "DESCARTAR"
    if resultado in ("PARCIAL", "NO_CONCLUYENTE") or (relevancia == "ALTA" and E < 70):
        return "PROFUNDIZAR_EN_B"
    return "VIGILAR"


# ==============================================================================================================
# Selección (9.4–9.7)
# ==============================================================================================================
def _percentil(valores: List[float], q: float) -> float:
    s = sorted(valores)
    if not s:
        raise ErrorEntrada("percentil de lista vacía")
    k = (len(s) - 1) * q
    f, c = math.floor(k), math.ceil(k)
    return s[f] if f == c else s[f] + (s[c] - s[f]) * (k - f)


def percentiles_winsorizados(valores: Dict[str, Optional[float]], inversa: bool = False,
                             limites: Tuple[float, float] = (0.025, 0.975)) -> Dict[str, Optional[float]]:
    """Winsoriza en (2,5 %, 97,5 %) y convierte en percentil 0–100 (rango medio con empates) dentro del grupo."""
    validos = {k: float(v) for k, v in valores.items() if v is not None and not (isinstance(v, float) and math.isnan(v))}
    out: Dict[str, Optional[float]] = {k: None for k in valores}
    n = len(validos)
    if n == 0:
        return out
    if n == 1:
        out[next(iter(validos))] = 50.0
        return out
    lo, hi = _percentil(list(validos.values()), limites[0]), _percentil(list(validos.values()), limites[1])
    w = {k: min(max(v, lo), hi) for k, v in validos.items()}
    if inversa:
        w = {k: -v for k, v in w.items()}
    orden = sorted(w.items(), key=lambda kv: kv[1])
    i = 0
    while i < n:
        j = i
        while j + 1 < n and orden[j + 1][1] == orden[i][1]:
            j += 1
        rango_medio = (i + j) / 2.0
        for t in range(i, j + 1):
            out[orden[t][0]] = round(100.0 * rango_medio / (n - 1), 4)
        i = j + 1
    return out


def normalizar_universo(filas: List[Dict], tipo_activo: str, grupo: Optional[str] = None,
                        metricas_playbook: Optional[Dict] = None) -> Dict[str, Dict[str, Any]]:
    """Componentes 0–100 de cada candidato (9.5, punto 1). `filas`: dicts con `cand_id` y métricas (None = falta).
    Devuelve cand_id → {componente: valor 0–100 | "NA" | "NE"}; la normalización se hace dentro de cada valor de
    `grupo` (subgrupo del universo heterogéneo) si se indica."""
    pb = PLAYBOOKS[tipo_activo]
    metricas = metricas_playbook or pb["metricas"]
    grupos: Dict[str, List[Dict]] = {}
    for f in filas:
        grupos.setdefault(str(f.get(grupo)) if grupo else "_", []).append(f)
    out: Dict[str, Dict[str, Any]] = {f["cand_id"]: {} for f in filas}
    for comp in COMPONENTES_S:
        if pb["pesos"].get(comp) is None:
            for f in filas:
                out[f["cand_id"]][comp] = "NA"
            continue
        lista = metricas.get(comp) or []
        for _, gfilas in grupos.items():
            pct_por_metrica = {}
            for (m, peso, inv) in lista:
                pct_por_metrica[m] = (peso, percentiles_winsorizados({f["cand_id"]: f.get(m) for f in gfilas}, inv))
            for f in gfilas:
                num, den = 0.0, 0.0
                for m, (peso, pct) in pct_por_metrica.items():
                    v = pct.get(f["cand_id"])
                    if v is not None:
                        num += peso * v
                        den += peso
                out[f["cand_id"]][comp] = round(num / den, 4) if den > 0 else "NE"
    return out


def calcular_S(componentes: Dict[str, Any], tipo_activo: str, pesos: Optional[Dict[str, Any]] = None,
               max_ne: int = 2) -> Dict:
    """S = Σ peso × componente (9.5, punto 2) con NA redistribuido y NE = 0; redondeo al entero.
    Más de `max_ne` componentes NE → excluido (DATOS_INSUFICIENTES)."""
    pesos = pesos or PLAYBOOKS[tipo_activo]["pesos"]
    ne = [k for k in COMPONENTES_S if componentes.get(k) == "NE"]
    na = [k for k in COMPONENTES_S if pesos.get(k) is None or componentes.get(k) == "NA"]
    if len(ne) > max_ne:
        return {"S": None, "calculable": False, "motivo": "DATOS_INSUFICIENTES", "ne": ne, "na": na}
    activos = {k: _frac(pesos[k]) for k in COMPONENTES_S if k not in na}
    sw = sum(activos.values())
    if sw == 0:
        return {"S": None, "calculable": False, "motivo": "DATOS_INSUFICIENTES", "ne": ne, "na": na}
    exacto = Fraction(0)
    for k, w in activos.items():
        v = componentes.get(k)
        if v in (None, "NE"):
            v = 0
        if not isinstance(v, (int, float, Fraction)) or v < 0 or v > 100:
            raise ErrorEntrada(f"Componente {k} fuera de 0–100: {v!r}")
        exacto += w * _frac(v)
    exacto /= sw
    return {"S": redondear(exacto, 1), "exacto": _num(exacto), "calculable": True, "ne": ne, "na": na,
            "pesos_efectivos": {k: _num(w * 100 / sw) for k, w in activos.items()}}


def puertas_candidato(c: Dict, tipo_activo: str, params: Optional[Dict] = None) -> Dict[str, str]:
    """PC1–PC4 (y PC5–PC8 si los datos están). Campos de `c`: invertible (bool), pureza (0–1), datos_ok (bool),
    ne (int), alertas (lista de {senal, critica}), objecion_fuerte_sin_resolver, refutado, ic90_S, frontera,
    reconstruible, banda_sin_segunda_pasada, duplicado."""
    p = fusionar_parametros(params)
    pb = PLAYBOOKS[tipo_activo]
    g: Dict[str, str] = {}
    g["PC1"] = "OK" if c.get("invertible", True) else "NO_INVERTIBLE"
    pmin = c.get("pureza_min", pb["pureza_min"])
    pur = c.get("pureza")
    if c.get("pureza_ok") is not None:
        g["PC2"] = "OK" if c["pureza_ok"] else "PUREZA_INSUFICIENTE"
    elif pmin is None:
        g["PC2"] = "OK"
    else:
        g["PC2"] = "OK" if (pur is not None and pur >= pmin) else "PUREZA_INSUFICIENTE"
    g["PC3"] = "OK" if (c.get("datos_ok", True) and int(c.get("ne", 0)) <= p["max_ne_candidato"]) else "DATOS_INSUFICIENTES"
    criticas = [a for a in c.get("alertas") or [] if a.get("critica") or a.get("estado") == "critica"
                or a.get("senal") in pb["alertas_criticas"]]
    g["PC4"] = "ALERTA_CRITICA" if criticas else "OK"
    if c.get("refutado"):
        g["PC5"] = "REFUTADO"
    elif c.get("objecion_fuerte_sin_resolver"):
        g["PC5"] = "LIMITA"
    else:
        g["PC5"] = "OK"
    ic = c.get("ic90_S")
    g["PC6"] = "OK" if (ic is None or ic[0] >= p["umbrales_candidato"]["ic90_inferior_prioritario"]) and not c.get("frontera") \
        else "LIMITA"
    g["PC7"] = "OK" if c.get("reconstruible", True) and not c.get("banda_sin_segunda_pasada") else "LIMITA"
    g["PC8"] = "LIMITA" if c.get("duplicado") else "OK"
    return g


def _aplicar_segunda_pasada(c: Dict, umbrales: List[int], corte: Optional[float], margen: int) -> Dict:
    S = c.get("S")
    if S is None:
        return c
    refs = list(umbrales) + ([corte] if corte is not None else [])
    if en_banda_marginal(S, refs, margen):
        s2 = c.get("S_segunda_pasada")
        if s2 is not None:
            c["S"] = min(S, int(s2))
            c["segunda_pasada"] = True
        else:
            c["banda_sin_segunda_pasada"] = True
    return c


def seleccionar(candidatos: List[Dict], tipo_activo: str, nivel: str = "N2", veredicto_ambito: str = "INVERTIR",
                params: Optional[Dict] = None, top_n: Optional[int] = None, n_alternativas: Optional[int] = None,
                ambito_es_subcluster: bool = False, candidatos_aun_con_vigilar: bool = False,
                correlaciones: Optional[Dict[str, float]] = None,
                solapamientos: Optional[Dict[str, float]] = None) -> Dict:
    """Ranking, top-N, alternativas, diversidad y veredictos de un tipo de activo (9.4–9.7).

    Cada candidato: cand_id, S (o componentes para calcularlo), ic90_S, ic90_rango, pureza, invertible,
    alertas, emisor, subcluster, indice_replicado, objecion_fuerte_sin_resolver, refutado, S_segunda_pasada.
    `correlaciones` y `solapamientos`: clave «idA|idB» (orden indiferente) → valor."""
    p = fusionar_parametros(params)
    if tipo_activo not in PLAYBOOKS:
        raise ErrorEntrada(f"tipo de activo desconocido {tipo_activo}")
    n_def, alt_def = p["top_n"].get(nivel, p["top_n"]["N2"])
    N = int(top_n if top_n is not None else n_def)
    NA = int(n_alternativas if n_alternativas is not None else alt_def)
    uc = p["umbrales_candidato"]
    margen = p["banda_marginal_candidato"]
    dv = p["diversidad"]
    correlaciones = {"|".join(sorted(k.split("|"))): v for k, v in (correlaciones or {}).items()}
    solapamientos = {"|".join(sorted(k.split("|"))): v for k, v in (solapamientos or {}).items()}

    evaluados: List[Dict] = []
    excluidos: List[Dict] = []
    for c0 in candidatos:
        c = copy.deepcopy(c0)
        if c.get("S") is None and c.get("componentes"):
            rs = calcular_S(c["componentes"], tipo_activo, max_ne=p["max_ne_candidato"])
            c["S"] = rs["S"]
            c["ne"] = len(rs["ne"])
        elif c.get("componentes"):
            c["ne"] = sum(1 for v in c["componentes"].values() if v == "NE")
        g = puertas_candidato(c, tipo_activo, p)
        c["puertas"] = g
        motivo = next((g[k] for k in ("PC1", "PC2", "PC3", "PC4") if g[k] != "OK"), None)
        if motivo is None and g["PC5"] == "REFUTADO":
            motivo = "REFUTADO"
        if motivo is None and c.get("S") is None:
            motivo = "DATOS_INSUFICIENTES"
        if motivo is None and c["S"] < uc["SECUNDARIO"]:
            motivo = "S_INSUFICIENTE"
        if motivo:
            c.update({"veredicto": "EXCLUIDO", "motivo_exclusion": motivo})
            excluidos.append(c)
        else:
            evaluados.append(c)

    def clave(c):
        ic = c.get("ic90_S") or [c["S"], c["S"]]
        return (-c["S"], -ic[0], -(c.get("pureza") or 0), str(c["cand_id"]))

    evaluados.sort(key=clave)
    corte = evaluados[N - 1]["S"] if len(evaluados) >= N and N > 0 else None
    for c in evaluados:
        _aplicar_segunda_pasada(c, [uc["PRIORITARIO_PARA_C"], uc["SECUNDARIO"]], corte, margen)
        c["puertas"] = puertas_candidato(c, tipo_activo, p)
    excl2 = [c for c in evaluados if c["S"] < uc["SECUNDARIO"]]
    for c in excl2:
        c.update({"veredicto": "EXCLUIDO", "motivo_exclusion": "S_INSUFICIENTE"})
    excluidos.extend(excl2)
    evaluados = [c for c in evaluados if c["S"] >= uc["SECUNDARIO"]]
    evaluados.sort(key=clave)
    for i, c in enumerate(evaluados, start=1):
        c["rango"] = i
        icr = c.get("ic90_rango")
        # FRONTERA (9.5, punto 4): el IC 90 % del rango cruza el corte del top-N
        c["frontera"] = bool(c.get("frontera")) or bool(icr and N and icr[0] <= N < icr[1])

    # Diversidad y no duplicación (9.7)
    top: List[Dict] = []
    alternativas: List[Dict] = []
    sustituciones: List[Dict] = []

    def _dup_con(c, otro) -> Optional[str]:
        if c.get("indice_replicado") and c.get("indice_replicado") == otro.get("indice_replicado"):
            return "mismo índice replicado"
        k = "|".join(sorted([str(c["cand_id"]), str(otro["cand_id"])]))
        if solapamientos.get(k, 0) > dv["solapamiento_duplicado"]:
            return f"solapamiento de cartera {solapamientos[k]:.0%} > {dv['solapamiento_duplicado']:.0%}"
        if correlaciones.get(k, 0) > dv["correlacion_duplicado"] and \
                (c.get("tesis_captura") or "_") == (otro.get("tesis_captura") or "_"):
            return f"correlación {correlaciones[k]:.2f} > {dv['correlacion_duplicado']} con la misma tesis de captura"
        return None

    max_sub = max(1, math.floor(dv["max_frac_subcluster"] * N)) if N else 0
    for c in evaluados:
        if len(top) >= N:
            alternativas.append(c)
            continue
        motivo = None
        for o in top:
            m = _dup_con(c, o)
            if m:
                motivo = (m, o)
                break
        if motivo is None and tipo_activo == "RF" and c.get("emisor"):
            if sum(1 for o in top if o.get("emisor") == c["emisor"]) >= dv["max_emisiones_por_emisor_RF"]:
                motivo = (f"más de {dv['max_emisiones_por_emisor_RF']} emisiones del emisor {c['emisor']}", None)
        if motivo is None and c.get("subcluster") and not ambito_es_subcluster:
            if sum(1 for o in top if o.get("subcluster") == c["subcluster"]) >= max_sub:
                motivo = (f"subclúster {c['subcluster']} alcanzaría más del {dv['max_frac_subcluster']:.0%} del top-N", None)
        if motivo:
            c["duplicado"] = motivo[1] is not None
            c["motivo_diversidad"] = motivo[0]
            sustituciones.append({"desplazado": c["cand_id"], "S": c["S"], "motivo": motivo[0],
                                  "frente_a": motivo[1]["cand_id"] if motivo[1] else None})
            alternativas.append(c)
        else:
            top.append(c)
    n_alt_publicadas = max(NA, 0)

    ambito_ok = veredicto_ambito in ("INVERTIR", "INVERTIR_ESCALONADO") or candidatos_aun_con_vigilar
    for c in top + alternativas:
        c["puertas"] = puertas_candidato(c, tipo_activo, p)
    for c in top:
        g = c["puertas"]
        limit = [k for k in ("PC5", "PC6", "PC7", "PC8") if g[k] != "OK"]
        if c["S"] >= uc["PRIORITARIO_PARA_C"] and not limit and ambito_ok:
            c["veredicto"] = "PRIORITARIO_PARA_C"
        else:
            c["veredicto"] = "SECUNDARIO"
            razones = []
            if c["S"] < uc["PRIORITARIO_PARA_C"]:
                razones.append(f"S < {uc['PRIORITARIO_PARA_C']}")
            razones += [f"{k} limita" for k in limit]
            if not ambito_ok:
                razones.append(f"ámbito en {veredicto_ambito}")
            c["motivo_secundario"] = razones
    for i, c in enumerate(alternativas):
        c["veredicto"] = "SECUNDARIO"
        c["alternativa"] = i < n_alt_publicadas
        c.setdefault("motivo_secundario", ["alternativa" if i < n_alt_publicadas else "fuera del top-N"])
    prioritarios = [c for c in top if c["veredicto"] == "PRIORITARIO_PARA_C"]
    menos = None
    if not prioritarios:
        menos = (f"Ningún candidato {tipo_activo} es prioritario: {len(candidatos)} analizados, {len(excluidos)} "
                 f"excluidos por puertas o S, {len(top)} en el top-N como SECUNDARIO.")
    elif len(top) < N:
        menos = f"Solo {len(top)} candidatos superan las puertas (top-N previsto {N}); no se rellena (R21)."
    por_motivo: Dict[str, int] = {}
    for c in excluidos:
        por_motivo[c["motivo_exclusion"]] = por_motivo.get(c["motivo_exclusion"], 0) + 1
    return {"tipo_activo": tipo_activo, "playbook": PLAYBOOKS[tipo_activo]["perfil"], "top_n_previsto": N,
            "top_n": top, "alternativas": alternativas[:n_alt_publicadas], "resto_secundarios": alternativas[n_alt_publicadas:],
            "excluidos": excluidos, "excluidos_por_motivo": por_motivo, "sustituciones_diversidad": sustituciones,
            "menos_de_N_motivo": menos, "prioritarios": [c["cand_id"] for c in prioritarios]}


def lista_corta_gc3(candidatos: List[Dict], top_n: int, multiplo: int = 2) -> Tuple[List[Dict], List[Dict]]:
    """GC3: finalistas = los 2 × top-N mejores por S provisional que superan PC1–PC4."""
    aptos = [c for c in candidatos if c.get("S") is not None and all(
        (c.get("puertas") or {}).get(k, "OK") == "OK" for k in ("PC1", "PC2", "PC3", "PC4"))]
    aptos.sort(key=lambda c: (-c["S"], str(c["cand_id"])))
    k = multiplo * top_n
    return aptos[:k], aptos[k:]


def apuestas_independientes(candidatos: List[Dict], correlaciones: Optional[Dict[str, float]] = None,
                            umbral: float = 0.9) -> Dict:
    """Número de apuestas independientes (9.7, regla 5): une candidatos que comparten emisor o subyacente
    («exposicion_compartida») o con correlación > umbral; devuelve grupos y su número."""
    ids = [c["cand_id"] for c in candidatos]
    padre = {i: i for i in ids}

    def raiz(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    def unir(a, b):
        ra, rb = raiz(a), raiz(b)
        if ra != rb:
            padre[rb] = ra
    clave_exp: Dict[str, str] = {}
    for c in candidatos:
        for k in [c.get("emisor"), c.get("subyacente"), c.get("exposicion_compartida")]:
            if k:
                if k in clave_exp:
                    unir(clave_exp[k], c["cand_id"])
                else:
                    clave_exp[k] = c["cand_id"]
    for k, v in (correlaciones or {}).items():
        a, b = k.split("|")
        if a in padre and b in padre and v > umbral:
            unir(a, b)
    grupos: Dict[str, List[str]] = {}
    for i in ids:
        grupos.setdefault(raiz(i), []).append(i)
    return {"apuestas_independientes": len(grupos), "grupos": sorted(grupos.values())}


# ==============================================================================================================
# V2.1 · Cuellos de botella (8.7.2, 9.12), atractivo del eslabón (AE), potencial del emergente (PEM)
# ==============================================================================================================
VIAS_EXPOSICION = ("COTIZADA_DIRECTA", "MATRIZ_COTIZADA", "ETF_O_FONDO", "FUTURA_SALIDA_A_BOLSA", "NO_INVERTIBLE_HOY")
VIAS_INVERTIBLES = ("COTIZADA_DIRECTA", "MATRIZ_COTIZADA", "ETF_O_FONDO")
TIPOS_EMERGENTE = ("STARTUP", "SCALE_UP", "SPIN_OFF_UNIVERSITARIO", "SPIN_OFF_CORPORATIVO", "SALIDA_A_BOLSA_RECIENTE")
NIVELES_ESLABON = ("macro", "sub", "actividad", "insumo")
ESTADOS_SEMAFORO = ("VERDE", "AMBAR", "ROJO")


def estado_indicador_cuello(indicador: str, valor: Any, params: Optional[Dict] = None) -> str:
    """Semáforo de un indicador de cuello con los umbrales (ámbar, rojo) del Anexo A. `insumo_sin_sustituto` es
    booleano (ROJO si True). `capacidad_vs_deficit` = tiempo de nueva capacidad / plazo hasta el déficit
    (ÁMBAR si lo iguala, ROJO si lo supera)."""
    p = fusionar_parametros(params)
    u = p["umbrales_cuello"].get(indicador)
    if u is None:
        raise ErrorEntrada(f"Indicador de cuello desconocido: {indicador}")
    if valor is None:
        return "VERDE"
    if indicador == "insumo_sin_sustituto":
        return "ROJO" if bool(valor) else "VERDE"
    v = float(valor)
    ambar, rojo, sentido = u
    if indicador == "capacidad_vs_deficit":
        return "ROJO" if v > 1.0 else ("AMBAR" if v == 1.0 else "VERDE")
    if sentido == "por_encima":
        return "ROJO" if v > rojo else ("AMBAR" if v >= ambar else "VERDE")
    return "ROJO" if v < rojo else ("AMBAR" if v < ambar else "VERDE")


def severidad_cuello(estados: Sequence[str], insumo_sin_sustituto_utilizacion_95: bool = False) -> int:
    """Severidad 1–5 (9.12): 1 ninguno en rojo · 2 uno en rojo o ≥ 3 en ámbar · 3 dos en rojo · 4 tres o cuatro en
    rojo · 5 cinco o más en rojo, o insumo sin sustituto con utilización > 95 %."""
    rojos = sum(1 for e in estados if e == "ROJO")
    ambar = sum(1 for e in estados if e == "AMBAR")
    if rojos >= 5 or insumo_sin_sustituto_utilizacion_95:
        return 5
    if rojos >= 3:
        return 4
    if rojos == 2:
        return 3
    if rojos == 1 or ambar >= 3:
        return 2
    return 1


def persistencia_cuello(meses_hasta_cierre: Optional[float]) -> int:
    """Persistencia 1–5 (9.12): < 6 meses · 6–12 · 1–2 años · 2–4 años · > 4 años."""
    if meses_hasta_cierre is None:
        raise ErrorEntrada("persistencia: falta el tiempo hasta cerrar el déficit")
    m = float(meses_hasta_cierre)
    return 1 if m < 6 else 2 if m < 12 else 3 if m < 24 else 4 if m <= 48 else 5


def calcular_PCB(severidad: int, persistencia: int, relevancia: int) -> int:
    """PCB = round(100 × severidad × persistencia × relevancia / 125), factores en 1–5 (8.7.2, 9.12)."""
    for n, v in (("severidad", severidad), ("persistencia", persistencia), ("relevancia", relevancia)):
        if not isinstance(v, int) or isinstance(v, bool) or not 1 <= v <= 5:
            raise ErrorEntrada(f"PCB: {n} = {v!r} fuera de 1–5")
    return redondear(Fraction(100 * severidad * persistencia * relevancia, 125), 1)


def evaluar_cuello(indicadores: Sequence[Dict], persistencia_meses: Optional[float], relevancia_valor: int,
                   params: Optional[Dict] = None) -> Dict:
    """Ficha VC-BOT-001 (cálculo determinista con los insumos del Motor): `indicadores` = [{indicador, valor} o
    {indicador, estado}]. Devuelve estados, severidad, persistencia, relevancia, PCB, material y es_cuello."""
    p = fusionar_parametros(params)
    est = []
    util = None
    sin_sust = False
    for x in indicadores or []:
        e = x.get("estado")
        if e not in ESTADOS_SEMAFORO:
            e = estado_indicador_cuello(x["indicador"], x.get("valor"), p)
        est.append({"indicador": x["indicador"], "valor": x.get("valor"), "estado": e})
        if x["indicador"] == "utilizacion" and x.get("valor") is not None:
            util = float(x["valor"])
        if x["indicador"] == "insumo_sin_sustituto" and e == "ROJO":
            sin_sust = True
    estados = [x["estado"] for x in est]
    sev = severidad_cuello(estados, sin_sust and util is not None and util > 0.95)
    per = persistencia_cuello(persistencia_meses) if persistencia_meses is not None else 1
    rel = int(relevancia_valor or 1)
    pcb = calcular_PCB(sev, per, rel)
    rojos = estados.count("ROJO")
    cm = p["cuello_material"]
    return {"herramienta": "HT-03", "ficha": "VC-BOT-001", "indicadores": est, "rojos": rojos,
            "ambar": estados.count("AMBAR"), "severidad": sev, "persistencia": per, "relevancia_valor": rel, "PCB": pcb,
            "material": pcb >= cm["PCB"] and rojos >= cm["rojos"], "es_cuello": sev >= 2}


def calcular_AE(componentes: Dict[str, Any], PCB: Optional[int] = None, params: Optional[Dict] = None) -> Dict:
    """AE 0–100 (9.12): crecimiento 20 · margen y ROIC relativos 20 · poder de negociación y barreras 15 · cuello
    favorable 20 · expectativas descontadas (inversa) 15 · sustitución (inversa) 10. Si no se da el componente
    «cuello», se deriva del PCB escalado al múltiplo de 10. Redondeo al entero (9.1)."""
    p = fusionar_parametros(params)
    c = dict(componentes)
    if c.get("cuello") is None:
        c["cuello"] = redondear(Fraction(int(PCB or 0)), 10) if PCB is not None else "NA"
    r = calcular_puntuacion("AE", c, p["pesos_AE"], paso=1)
    r["componentes"] = c
    r["atractivo"] = bool(r["calculable"] and r["total"] >= p["eslabon_atractivo_AE"])
    return r


def calcular_PEM(criterios: Dict[str, Any], params: Optional[Dict] = None) -> Dict:
    """PEM 0–100 (8.7.3): tecnología 20 · tracción 25 · equipo 15 · financiación 15 · posición en la cadena 15 · vía
    de exposición 10. Ordena la subtabla de emergentes; no es una recomendación ni sustituye a S."""
    p = fusionar_parametros(params)
    r = calcular_puntuacion("PEM", dict(criterios), p["pesos_PEM"], paso=1)
    r["componentes"] = dict(criterios)
    return r


# ==============================================================================================================
# V2.1 · Puertas de viabilidad PV1–PV3 (7.10, Anexo A)
# ==============================================================================================================
def evaluar_pv1(insumos: Dict, params: Optional[Dict] = None) -> Dict:
    """PV1 (fin de la capa 1). Insumos: tipos_con_invertible (nº de tipos con ≥ 1 instrumento que supera PC1 en el
    universo preliminar), instrumentos_invertibles, capitalizacion_agregada_meur (o None), alerta_integridad,
    biblioteca_descartar_sin_cambio, ya_descontado, sin_mecanismo. No se supera con un criterio eliminatorio o con
    dos o más de debilidad."""
    p = fusionar_parametros(params)["pv1"]
    elim, deb = [], []
    if int(insumos.get("tipos_con_invertible") or 0) == 0:
        elim.append({"criterio": "SIN_INVERTIBILIDAD", "clase": "ELIMINATORIO",
                     "detalle": "Ningún tipo de activo con instrumentos que superen PC1 en el universo preliminar"})
    if insumos.get("alerta_integridad"):
        elim.append({"criterio": "ALERTA_GRAVE", "clase": "ELIMINATORIO",
                     "detalle": "Alerta grave de integridad en la premisa central"})
    if insumos.get("biblioteca_descartar_sin_cambio"):
        elim.append({"criterio": "BIBLIOTECA_DESCARTAR", "clase": "ELIMINATORIO",
                     "detalle": "Ficha F6 vigente con DESCARTAR y sin cambio material (GC0)"})
    cap = insumos.get("capitalizacion_agregada_meur")
    n = int(insumos.get("instrumentos_invertibles") or 0)
    if (cap is not None and float(cap) < p["materialidad_min_meur"]) or n < p["materialidad_min_instrumentos"]:
        deb.append({"criterio": "MATERIALIDAD", "clase": "DEBILIDAD",
                    "detalle": (f"Capitalización agregada {cap} M€ y {n} instrumentos invertibles" if cap is not None
                                else f"Capitalización agregada no disponible y {n} instrumentos invertibles")
                               + f" frente a los mínimos ({p['materialidad_min_meur']} M€; {p['materialidad_min_instrumentos']} instrumentos)"})
    if insumos.get("ya_descontado"):
        deb.append({"criterio": "YA_DESCONTADO", "clase": "DEBILIDAD",
                    "detalle": "Valoración en el percentil alto de su historia con saturación narrativa probable y sin tesis diferencial"})
    if insumos.get("sin_mecanismo"):
        deb.append({"criterio": "SIN_MECANISMO", "clase": "DEBILIDAD", "detalle": "Tesis básica sin mecanismo plausible"})
    superada = not elim and len(deb) <= p["max_debilidades"]
    return {"puerta": "PV1", "resultado": "SUPERADA" if superada else "NO_SUPERADA",
            "motivos": elim + deb if not superada else [], "debilidades": deb, "eliminatorios": elim, "insumos": dict(insumos)}


def evaluar_pv2(A: Optional[int], E: Optional[int], tesis_viva: bool, fuentes_para_cerrar_E: bool = False,
                params: Optional[Dict] = None) -> Dict:
    """PV2 (fin de la capa 2; integra GC2): A provisional ≥ 50 y E provisional ≥ 50 y tesis viva tras una
    autorrefutación. Si solo falla E y hay fuentes que podrían cerrarla, se propone consulta CONFIRMACION_SUPUESTO."""
    p = fusionar_parametros(params)["gc2"]
    motivos = []
    if A is None or A < p["A"]:
        motivos.append({"criterio": "A_PROVISIONAL", "clase": "UMBRAL", "detalle": f"A provisional {A} < {p['A']}"})
    if E is None or E < p["E"]:
        motivos.append({"criterio": "E_PROVISIONAL", "clase": "UMBRAL", "detalle": f"E provisional {E} < {p['E']}"})
    if not tesis_viva:
        motivos.append({"criterio": "TESIS_REFUTADA", "clase": "UMBRAL", "detalle": "La tesis no sobrevive a la autorrefutación del Director"})
    solo_E = len(motivos) == 1 and motivos[0]["criterio"] == "E_PROVISIONAL"
    return {"puerta": "PV2", "resultado": "NO_SUPERADA" if motivos else "SUPERADA", "motivos": motivos,
            "proponer_consulta": bool(solo_E and fuentes_para_cerrar_E), "A": A, "E": E, "tesis_viva": bool(tesis_viva)}


def eslabon_cualifica(e: Dict, params: Optional[Dict] = None) -> Dict:
    """Eslabón atractivo (AE ≥ umbral) o con cuello material (PCB ≥ umbral y ≥ 2 indicadores en rojo)."""
    p = fusionar_parametros(params)
    ae = (e.get("atractivo") or {}).get("AE") if isinstance(e.get("atractivo"), dict) else e.get("AE")
    cb = e.get("cuello_botella") or {}
    pcb = cb.get("PCB") if cb else e.get("PCB")
    rojos = sum(1 for x in cb.get("indicadores") or [] if x.get("estado") == "ROJO") if cb else int(e.get("rojos") or 0)
    material = bool(cb.get("material")) if "material" in cb else (pcb is not None and pcb >= p["cuello_material"]["PCB"]
                                                                   and rojos >= p["cuello_material"]["rojos"])
    atractivo = ae is not None and ae >= p["eslabon_atractivo_AE"]
    unico = e.get("eslabon_id") == "ESL-00"     # sin cadena: el ámbito es el eslabón único y siempre cuenta (7.10, PV3)
    return {"atractivo": atractivo, "cuello_material": material, "cualifica": atractivo or material or unico, "AE": ae, "PCB": pcb}


def _apto_pc1_4(c: Dict) -> bool:
    g = c.get("puertas") or {}
    return all(g.get(k, "OK") == "OK" for k in ("PC1", "PC2", "PC3", "PC4"))


def evaluar_pv3(eslabones: Sequence[Dict], candidatos: Sequence[Dict], params: Optional[Dict] = None) -> Dict:
    """PV3 (fin de la capa 3): ≥ 1 eslabón atractivo o con cuello material con ≥ 1 opción que supere PC1–PC4 y con
    S provisional ≥ 50. `candidatos`: [{cand_id, eslabon_id, S, puertas}]. Sin cadena: eslabón único ESL-00."""
    p = fusionar_parametros(params)
    smin = p["pv3"]["S_min"]
    detalle = []
    ok = False
    for e in eslabones or []:
        q = eslabon_cualifica(e, p)
        ops = [c for c in candidatos if c.get("eslabon_id") == e.get("eslabon_id") and c.get("S") is not None
               and c["S"] >= smin and _apto_pc1_4(c)]
        cumple = q["cualifica"] and bool(ops)
        ok = ok or cumple
        detalle.append({"eslabon_id": e.get("eslabon_id"), **q, "opciones_aptas": len(ops), "cumple": cumple})
    return {"puerta": "PV3", "resultado": "SUPERADA" if ok else "NO_SUPERADA", "eslabones": detalle,
            "motivos": [] if ok else [{"criterio": "SIN_ESLABON_CON_OPCIONES", "clase": "UMBRAL",
                                        "detalle": "Ningún eslabón atractivo o con cuello material tiene una opción invertible con S ≥ 50"}]}


def mejores_por_eslabon(eslabones: Sequence[Dict], candidatos_por_tipo: Dict[str, List[Dict]], nivel: str = "N2",
                        veredicto_ambito: str = "INVERTIR", candidatos_aun_con_vigilar: bool = False,
                        eslabon_critico: Optional[str] = None, params: Optional[Dict] = None) -> Dict:
    """Mejores opciones por eslabón (9.13): para cada eslabón que cualifica, hasta 5 opciones (N1: 3 y solo el eslabón
    crítico) entre todos los tipos, por S y, a igualdad, por pureza al eslabón. Solo opciones con PC1–PC4 y S ≥ 50.
    Un candidato del top-N figura por referencia (`en_top_n_tipo`) con su veredicto; los añadidos por cobertura del
    eslabón reciben el veredicto de 9.6 (PRIORITARIO_PARA_C si S ≥ 65, PC5–PC8 superadas y ámbito INVERTIR o
    INVERTIR_ESCALONADO). `candidatos_por_tipo[t]`: candidatos ya evaluados por `seleccionar` (con veredicto y
    en_top_n) o crudos (cand_id, S, puertas, eslabon_id, pureza_eslabon)."""
    p = fusionar_parametros(params)
    n_max = p["mejores_por_eslabon"].get(nivel, 5)
    uc = p["umbrales_candidato"]
    ambito_ok = veredicto_ambito in ("INVERTIR", "INVERTIR_ESCALONADO") or candidatos_aun_con_vigilar
    tablas: Dict[str, Dict] = {}
    usados = set()
    for e in eslabones or []:
        eid = e.get("eslabon_id")
        q = eslabon_cualifica(e, p)
        if nivel == "N1" and eslabon_critico and eid != eslabon_critico:
            continue
        if not q["cualifica"]:
            continue
        pool = []
        for t, cs in (candidatos_por_tipo or {}).items():
            for c in cs:
                if c.get("eslabon_id") != eid or c.get("S") is None or c["S"] < uc["SECUNDARIO"] or not _apto_pc1_4(c):
                    continue
                if c.get("veredicto") == "EXCLUIDO" or (c.get("puertas") or {}).get("PC5") == "REFUTADO":
                    continue
                pool.append((t, c))
        pool.sort(key=lambda x: (-x[1]["S"], -(x[1].get("pureza_eslabon") or 0), str(x[1]["cand_id"])))
        opciones = []
        for t, c in pool[:n_max]:
            g = c.get("puertas") or {}
            en_top = bool(c.get("en_top_n"))
            if en_top and c.get("veredicto") in ("PRIORITARIO_PARA_C", "SECUNDARIO"):
                ver, mot = c["veredicto"], c.get("motivo_secundario") or []
            else:
                lim = [k for k in ("PC5", "PC6", "PC7", "PC8") if g.get(k, "OK") != "OK"]
                if c["S"] >= uc["PRIORITARIO_PARA_C"] and not lim and ambito_ok:
                    ver, mot = "PRIORITARIO_PARA_C", []
                else:
                    ver = "SECUNDARIO"
                    mot = ([f"S < {uc['PRIORITARIO_PARA_C']}"] if c["S"] < uc["PRIORITARIO_PARA_C"] else []) + \
                        [f"{k} limita" for k in lim] + ([] if ambito_ok else [f"ámbito en {veredicto_ambito}"])
            opciones.append({"rango": len(opciones) + 1, "cand_id": c["cand_id"], "tipo_activo": t, "S": c["S"],
                             "ic90_S": c.get("ic90_S"), "pureza_eslabon": c.get("pureza_eslabon"), "veredicto": ver,
                             "motivo_secundario": mot, "en_top_n_tipo": en_top})
            usados.add(c["cand_id"])
        tablas[eid] = {"eslabon_id": eid, **q, "opciones": opciones,
                       "sin_opciones_motivo": None if opciones else "Ninguna opción supera PC1–PC4 con S ≥ 50 en este eslabón (R21)"}
    adicionales = sorted({o["cand_id"] for tb in tablas.values() for o in tb["opciones"] if not o["en_top_n_tipo"]})
    return {"herramienta": "HT-03", "regla": "9.13", "max_por_eslabon": n_max, "tablas": tablas,
            "adicionales_al_top_n": adicionales,
            "prioritarios_adicionales": sorted({o["cand_id"] for tb in tablas.values() for o in tb["opciones"]
                                                if not o["en_top_n_tipo"] and o["veredicto"] == "PRIORITARIO_PARA_C"})}


# ==============================================================================================================
# Cálculo completo (entrada JSON)
# ==============================================================================================================
def procesar(entrada: Dict) -> Dict:
    """Entrada: {"parametros"?, "nivel", "horizonte", "riesgo_1a5", "iliquidez"?, "A": {...}, "E": {...},
    "saturacion_narrativa"?, "refutacion": {"veredicto_tesis", "moderadas_sin_resolver"}, "RE",
    "puertas_ambito": {PA1..PA7}, "flags"?, "segunda_pasada"?: {"A","E","C"}, "candidatos_aun_con_vigilar"?,
    "disparador_cercano"?, "resultado_del_analisis"?, "eslabones"? (V2.1: desglose con AE y cuello), "eslabon_critico"?,
    "candidatos_por_tipo": {tipo: {"candidatos": [...], "top_n"?, "n_alternativas"?, ...}}}.
    Aplica el orden de cálculo de 9.3."""
    p = fusionar_parametros(entrada.get("parametros"))
    nivel = entrada.get("nivel", "N2")
    rA = calcular_A(entrada["A"], entrada.get("saturacion_narrativa", False), p)
    rE = calcular_E(entrada["E"], p)
    if not rA["calculable"] or not rE["calculable"]:
        return {"herramienta": "HT-03", "version": VERSION, "error": "A o E no calculables", "A": rA, "E": rE}
    ref = entrada.get("refutacion") or {}
    if nivel == "N1" and not ref.get("veredicto_tesis"):
        ref = {"veredicto_tesis": "fragil", "moderadas_sin_resolver": 0}
    RF = calcular_RF(ref.get("veredicto_tesis"), ref.get("moderadas_sin_resolver", 0))
    RE = entrada.get("RE", 50)
    RE = None if RE in (None, "NA") else int(RE)
    A, E = rA["total"], rE["total"]
    rC = calcular_C(A, E, RF, RE, p)
    C = rC["C"]
    segunda = entrada.get("segunda_pasada") or {}
    margen = p["banda_marginal_ambito"]
    u = p["umbrales_ambito"]
    umb = {"A": [u["INVERTIR"]["A"], u["INVERTIR_ESCALONADO"]["A"], u["VIGILAR"]["A"]],
           "E": [u["INVERTIR"]["E"]], "C": [u["INVERTIR"]["C"], u["INVERTIR_ESCALONADO"]["C"]]}
    banda: Dict[str, List[int]] = {}
    sin_segunda = []
    valores = {"A": A, "E": E, "C": C}
    for k in ("A", "E", "C"):
        b = en_banda_marginal(valores[k], umb[k], margen)
        if b:
            banda[k] = b
            if k in segunda and segunda[k] is not None:
                valores[k] = min(valores[k], int(segunda[k]))
            else:
                sin_segunda.append(k)
    A, E, C = valores["A"], valores["E"], valores["C"]
    if C > E + p["tope_C_sobre_E"]:
        C = E + p["tope_C_sobre_E"]
    puertas = {g: entrada.get("puertas_ambito", {}).get(g, "OK") for g in PUERTAS_AMBITO}
    if sin_segunda:
        puertas["PA7"] = "BLOQUEA"
    flags = dict(entrada.get("flags") or {})
    if ref.get("veredicto_tesis") == "refutada":
        flags["tesis_refutada"] = True
        puertas["PA5"] = "BLOQUEA"
    # PA8 por universo: ningún tipo con candidato que supere PC1–PC4
    tipos = entrada.get("candidatos_por_tipo") or {}
    alguno = False
    for t, d in tipos.items():
        for c in d.get("candidatos", []):
            g = puertas_candidato(c, t, p)
            if all(g[k] == "OK" for k in ("PC1", "PC2", "PC3", "PC4")):
                alguno = True
                break
    if tipos and not alguno:
        puertas["PA8"] = "BLOQUEA"
    prov = veredicto_ambito_provisional(A, E, C, puertas, flags, p)
    sel: Dict[str, Dict] = {}
    for t, d in tipos.items():
        sel[t] = seleccionar(d.get("candidatos", []), t, nivel, prov["veredicto"], p, d.get("top_n"),
                             d.get("n_alternativas"), d.get("ambito_es_subcluster", False),
                             entrada.get("candidatos_aun_con_vigilar", False), d.get("correlaciones"),
                             d.get("solapamientos"))
    # Mejores opciones por eslabón (9.13): adicionales al top-N y sin duplicarlo
    mpe = None
    if entrada.get("eslabones"):
        pool = {}
        for t, s_ in sel.items():
            top_ids = {c["cand_id"] for c in s_["top_n"]}
            pool[t] = [dict(c, en_top_n=c["cand_id"] in top_ids) for c in s_["top_n"] + s_["alternativas"] + s_["resto_secundarios"]]
        mpe = mejores_por_eslabon(entrada["eslabones"], pool, nivel, prov["veredicto"],
                                  entrada.get("candidatos_aun_con_vigilar", False), entrada.get("eslabon_critico"), p)
    prioritarios_tipos = [t for t, s in sel.items() if s["prioritarios"]]
    if mpe:
        for tb in mpe["tablas"].values():
            for o in tb["opciones"]:
                if o["veredicto"] == "PRIORITARIO_PARA_C" and o["tipo_activo"] not in prioritarios_tipos:
                    prioritarios_tipos.append(o["tipo_activo"])
    final = prov["veredicto"]
    motivo_final = prov["motivo"]
    if final in ("INVERTIR", "INVERTIR_ESCALONADO") and tipos and not prioritarios_tipos:
        final = "VIGILAR"
        motivo_final = "sin vehículo de captura adecuado"
        for s in sel.values():
            for c in s["top_n"]:
                if c["veredicto"] == "PRIORITARIO_PARA_C":
                    c["veredicto"] = "SECUNDARIO"
    elif final == "VIGILAR" and not entrada.get("candidatos_aun_con_vigilar"):
        for s in sel.values():
            for c in s["top_n"]:
                if c["veredicto"] == "PRIORITARIO_PARA_C":
                    c["veredicto"] = "SECUNDARIO"
    if mpe and final not in ("INVERTIR", "INVERTIR_ESCALONADO") and not entrada.get("candidatos_aun_con_vigilar"):
        for tb in mpe["tablas"].values():
            for o in tb["opciones"]:
                if o["veredicto"] == "PRIORITARIO_PARA_C":
                    o["veredicto"] = "SECUNDARIO"
                    o["motivo_secundario"] = list(o.get("motivo_secundario") or []) + [f"ámbito en {final}"]
        mpe["prioritarios_adicionales"] = []
    n_prior = sum(len(s["prioritarios"]) for s in sel.values()) if final in ("INVERTIR", "INVERTIR_ESCALONADO") else 0
    if mpe and final in ("INVERTIR", "INVERTIR_ESCALONADO"):
        n_prior += len(mpe["prioritarios_adicionales"])
    rel, mot_rel = relevancia_decisional(final, A, E, int(entrada.get("riesgo_1a5", 3)), entrada.get("horizonte", "H3"),
                                         bool(entrada.get("iliquidez")), prioritarios_tipos if n_prior else [],
                                         bool(entrada.get("disparador_cercano")))
    resultado = entrada.get("resultado_del_analisis", "CONCLUYENTE")
    paso = siguiente_paso(final, n_prior, resultado, rel, E)
    todos_top = [c for s in sel.values() for c in s["top_n"] if c["veredicto"] in ("PRIORITARIO_PARA_C", "SECUNDARIO")]
    ap = apuestas_independientes([c for c in todos_top if c["veredicto"] == "PRIORITARIO_PARA_C"] or todos_top)
    return {"herramienta": "HT-03", "version": VERSION,
            "puntuaciones": {"A": A, "E": E, "C": C, "RF": RF, "RE": RE,
                             "desglose": {"A": rA["componentes"], "E": rE["componentes"]},
                             "segunda_pasada": bool(banda) and not sin_segunda and bool(segunda),
                             "banda_marginal": banda, "sin_segunda_pasada": sin_segunda,
                             "lectura_C": "alta" if C >= 70 else ("media" if C >= 50 else "baja"),
                             "tope_saturacion_aplicado": rA["tope_saturacion_aplicado"], "C_detalle": rC},
            "puertas_ambito": puertas, "veredicto_provisional": prov,
            "veredicto": {"valor": final, "motivo": motivo_final, "motivo_descarte": prov.get("motivo_descarte"),
                          "relevancia_decisional": rel, "motivos_relevancia": mot_rel, "siguiente_paso_sugerido": paso},
            "seleccion": sel, "mejores_por_eslabon": mpe,
            "apuestas_independientes": ap["apuestas_independientes"], "grupos_apuestas": ap["grupos"]}


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="HT-03 · Puntuaciones, veredictos y rankings del Bloque B")
    ap.add_argument("entrada", help="JSON de entrada ('-' para stdin)")
    ap.add_argument("--salida", help="Archivo de salida JSON (por defecto, stdout)")
    ap.add_argument("--estrategia", action="store_true",
                    help="La entrada es {tipo_objeto, horizonte, tipos_materiales, nivel, desviaciones}")
    a = ap.parse_args(argv)
    try:
        datos = json.load(sys.stdin if a.entrada == "-" else open(a.entrada, encoding="utf-8"))
        if a.estrategia:
            res = estrategia(datos["tipo_objeto"], datos["horizonte"], datos.get("tipos_materiales", ()),
                             datos.get("nivel", "N2"), datos.get("desviaciones"), datos.get("segmento_tipo"),
                             datos.get("parametros"))
        else:
            res = procesar(datos)
    except (ErrorEntrada, KeyError, json.JSONDecodeError) as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 3
    txt = json.dumps(res, ensure_ascii=False, indent=2, default=str)
    if a.salida:
        with open(a.salida, "w", encoding="utf-8") as fh:
            fh.write(txt)
    else:
        print(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
