#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HT-09 · Validador determinista G3 (implementación de referencia).

Bloque A Forex · Robot Investor · Versión óptima V1.0 · 02/11/2026 · actualizado V1.1 (03/11/2026) ·
Subordinado al Documento 0 del Bloque A Forex V1.1 (secciones 2.4–2.6, 4.4, 6.2.9, 7.3 F6, 7.8, 7.11, 8.3, 9, 14 y
Anexos A y B).

Valida un `paquete_oportunidades` Forex (Anexo B) y devuelve el dictamen
APTO / APTO_CON_ADVERTENCIAS / BLOQUEADO con la lista de comprobaciones:

  C01 Campos obligatorios, valores permitidos y prefijos de identificadores con infijo FX (RUN-FX-, OPP-FX-, PRG-FX-,
      TND-FX-, CLM-FX-, EVD-FX-, CALC-FX-)
  C02 Máximo de opciones por segmento y rangos
  C03 Menos de tres con motivo (R14)
  C04 Puntuaciones reconstruibles con HT-03 (RK siempre; dimensiones de la A FX si hay desglose)
  C05 Elegibilidad (9.2), puertas G1–G4 / PS1–PS8 y PS3 de convertibilidad e invertibilidad
  C06 Horizontes compatibles con la tabla 8.3 por segmento («No» de ESTR en H1, «Limitado» con catalizador)
  C07 Probabilidad numérica solo con certificado de horizonte (R13)
  C08 Evidencias y cálculos referenciados no vacíos (R7) y trazas CLM→EVD
  C09 Objeciones: ninguna fuerte sin resolver; respuestas a fuertes y moderadas (R12)
  C10 Coherencia de `relevancia_decisional` y del riesgo 1–5 con el Anexo A (notas 2 y 3)
  C11 `paquete_para_bloque_B` (encargo de 2.5) para cada opción con ENVIAR_A_BLOQUE_B
  C12 Legibilidad del informe visual con HT-07 (Fernández-Huerta corregido ≥ 70)
  C13 Ausencia de credenciales o secretos (R8)
  C14 Coherencia del semáforo y de las apuestas independientes
  C15 Frontera con el Bloque B: ningún instrumento, proveedor, apalancamiento, tamaño ni nivel de entrada (R21)
  C16 Oportunidad duplicada en dos segmentos (regla 4 de 2.6)
  C17 Naturaleza de la inversión y horizonte principal (regla de adecuación de 8.3; V1.1)
  C18 H5 «limitado»: naturaleza ESTRUCTURAL, uno de los tres ámbitos admitidos, banda cualitativa e hitos HIT-FX- (8.3, R13,
      Anexo A; V1.1)
  C19 Supuestos declarados por consultas al Broker sin respuesta (6.2.9, CT-23; V1.1)
  Además, `validar_seguimiento` valida el `informe_seguimiento_opcion` del ciclo C6 (14.4 y Anexo B; códigos S01–S06).
  Comprobaciones específicas de divisas G3-FX-01 a G3-FX-11 (Anexo 1 del Plan de pruebas del Bloque A Forex):
  G3-FX-01 Notación BASE/COTIZADA (ISO 4217 y convención de mercado) y dirección (con la composición y el nombre llano)
  G3-FX-02 Composición de cestas, bloques y estrategias (PS4): pesos por lado que suman 1, ISO 4217, divisa de financiación
  G3-FX-03 Asignación de segmento según las reglas 1–3 de 2.6 (o motivo registrado)
  G3-FX-04 Convertibilidad (PS3) completa y riesgo de régimen (tipo fijo o controles: riesgo ≥ 4)
  G3-FX-05 Carry: cifra anual, signo, carry ajustado por volatilidad, CALC-FX- y coherencia con dirección y diferencial
  G3-FX-06 Referencias ingenuas: paseo aleatorio; forward en rentabilidad total; rentabilidad nula o índice en estrategias (W)
  G3-FX-07 Anticipación en fijaciones: niveles conocibles en la fecha, con fuente, hora y zona
  G3-FX-08 Exposición agregada reconstruible desde las composiciones y contradicciones entre segmentos (misma divisa como
           pata activa de la tesis con direcciones opuestas) justificadas
  G3-FX-09 Diversidad por divisa: una divisa con la misma dirección en ≤ 2 opciones del segmento
  G3-FX-10 Capas transversales: referencia a los informes CT-06T (TRV-FX-) o declaración de su ausencia (W)
  G3-FX-11 Tipo de rentabilidad (PRECIO_CONTADO o RENTABILIDAD_TOTAL) y divisa de medición de cada PRG

Los seis segmentos (G10N, G10M, EMAS, EMLA, EMEA, ESTR) y la tabla de horizontes 8.3 son los del
Documento 0 Forex; PS3 es la convertibilidad e invertibilidad del ámbito.

Sin consumo de modelo de lenguaje. Solo biblioteca estándar (importa
ht03_puntuaciones y ht07_legibilidad del mismo directorio).
Códigos de salida: 0 APTO, 1 APTO_CON_ADVERTENCIAS, 2 BLOQUEADO, 3 error de entrada.

Estado de madurez (R22): implementada (referencia), pruebas unitarias
superadas; pendiente de integración.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ht03_puntuaciones as ht03  # noqa: E402
import ht07_legibilidad as ht07  # noqa: E402

VERSION = "FX-1.1"
SEGMENTOS = ht03.SEGMENTOS          # los seis segmentos de 2.6, en su orden canónico
CLASES = SEGMENTOS                  # alias histórico («Analista de clase», Anexo C)
SEGMENTOS_EMERGENTES = ("EMAS", "EMLA", "EMEA")
HORIZONTES = ("H1", "H2", "H3", "H4", "H5")
# Tabla 8.3 del Documento 0 Forex V1.1: SI, LIMITADO, NO. H5 (décadas, 5–30 años) es «limitado» en los seis segmentos y
# solo se admite para naturaleza ESTRUCTURAL en uno de los tres ámbitos de AMBITOS_H5 (C18).
TABLA_HORIZONTES = {
    "G10N": {"H1": "SI", "H2": "SI", "H3": "SI", "H4": "SI", "H5": "LIMITADO"},
    "G10M": {"H1": "SI", "H2": "SI", "H3": "SI", "H4": "SI", "H5": "LIMITADO"},
    "EMAS": {"H1": "LIMITADO", "H2": "SI", "H3": "SI", "H4": "LIMITADO", "H5": "LIMITADO"},
    "EMLA": {"H1": "LIMITADO", "H2": "SI", "H3": "SI", "H4": "LIMITADO", "H5": "LIMITADO"},
    "EMEA": {"H1": "LIMITADO", "H2": "SI", "H3": "SI", "H4": "LIMITADO", "H5": "LIMITADO"},
    "ESTR": {"H1": "NO", "H2": "SI", "H3": "SI", "H4": "SI", "H5": "LIMITADO"},
}
# Regla de adecuación del horizonte al tipo de inversión (8.3 V1.1): rango admisible del horizonte principal.
# La naturaleza LIQUIDEZ del Bloque A general no se usa en el Bloque A Forex.
RANGO_NATURALEZA = {"TACTICA": ("H1", "H2"), "CICLICA": ("H2", "H3", "H4"), "PRIMA_RIESGO": ("H2", "H3", "H4"),
                    "VALORACION": ("H3", "H4"), "ESTRUCTURAL": ("H4", "H5")}
NATURALEZAS = tuple(RANGO_NATURALEZA)
AMBITOS_H5 = ("EQUILIBRIO_LARGO_PLAZO", "REGIMEN_CAMBIARIO", "SISTEMA_MONETARIO_INTERNACIONAL")
# Anexo A: ≥ 3 hitos HIT-FX- por pronóstico H5; el primero a ≤ 12 meses y ≤ 24 meses entre hitos consecutivos
H5_MIN_HITOS, H5_PRIMER_HITO_MESES, H5_MAX_ENTRE_HITOS_MESES = 3, 12, 24
RE_FECHA_ISO = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")
# Tipos de opción (2.4): granularidad máxima par, cruce, cesta, bloque, estrategia o régimen
TIPOS_OPCION = ("PAR", "CRUCE", "CESTA", "BLOQUE", "ESTRATEGIA", "VOLATILIDAD", "REGIMEN")
TIPOS_CON_PAR = ("PAR", "CRUCE", "VOLATILIDAD")
TIPOS_CESTA = ("CESTA", "BLOQUE", "ESTRATEGIA")
TIPOS_OPCION_AJENOS = {"MERCADO": "tipo del Bloque A general", "SECTOR": "tipo del Bloque A general",
                       "SUBSECTOR": "tipo del Bloque A general", "TEMATICA": "tipo del Bloque A general",
                       "SEGMENTO": "tipo del Bloque A general", "FACTOR": "tipo del Bloque A general",
                       "ESTILO": "tipo del Bloque A general", "INSTRUMENTO_GENERICO": "el Bloque A no propone instrumentos",
                       "INSTRUMENTO": "el Bloque A no propone instrumentos"}
DIRECCIONES_BASE = ("ALCISTA_BASE", "BAJISTA_BASE")
# Dirección (2.4): referida a la base en las opciones con par; en cestas, bloques y estrategias va en `composicion`
# (lado y peso de cada divisa) y en VOLATILIDAD en `vista_volatilidad` (ALZA/BAJA y plazo).
TIPOS_CON_DIRECCION = ("PAR", "CRUCE", "REGIMEN")
TIPOS_RENTABILIDAD = ("PRECIO_CONTADO", "RENTABILIDAD_TOTAL")
TIPO_RENTABILIDAD_VOLATILIDAD = "NIVEL_VOLATILIDAD"   # 2.4: pronósticos sobre el nivel de volatilidad implícita (solo VOLATILIDAD)
# 9.6.6: el USD y el EUR como contrapartida o financiación de un par no son la «pata activa» de la tesis
CONTRAPARTIDAS = ("USD", "EUR")
# Asignación de segmento (2.6): divisa → segmento y prelación de liquidez (de más a menos líquido)
SEGMENTO_DE_DIVISA = {**{d: "G10N" for d in ("USD", "EUR", "JPY", "GBP", "CHF")},
                      **{d: "G10M" for d in ("AUD", "NZD", "CAD", "NOK", "SEK")},
                      **{d: "EMAS" for d in ("CNY", "CNH", "INR", "KRW", "TWD", "IDR", "SGD", "THB", "MYR", "PHP", "VND", "HKD")},
                      **{d: "EMLA" for d in ("BRL", "MXN", "CLP", "COP", "PEN", "ARS", "UYU")},
                      **{d: "EMEA" for d in ("PLN", "HUF", "CZK", "RON", "TRY", "ZAR", "ILS", "EGP", "NGN", "KES", "MAD", "SAR",
                                             "AED", "QAR", "KWD", "BHD", "OMR")}}
LIQUIDEZ_SEGMENTO = ("G10N", "G10M", "EMAS", "EMLA", "EMEA")
# Nombres llanos de las divisas (sin tildes) para comprobar `nombre_llano` frente a la dirección (G3-FX-01)
NOMBRES_LLANOS = {"dolar australiano": "AUD", "dolar neozelandes": "NZD", "dolar canadiense": "CAD", "dolar de hong kong": "HKD",
                  "dolar de singapur": "SGD", "dolar taiwanes": "TWD", "dolar": "USD", "euro": "EUR", "yen": "JPY", "libra": "GBP",
                  "franco suizo": "CHF", "franco": "CHF", "corona noruega": "NOK", "corona sueca": "SEK", "corona checa": "CZK",
                  "won": "KRW", "yuan": "CNY", "renminbi": "CNY", "rupia india": "INR", "rupia indonesia": "IDR", "baht": "THB",
                  "ringgit": "MYR", "peso filipino": "PHP", "peso mexicano": "MXN", "real": "BRL", "peso chileno": "CLP",
                  "peso colombiano": "COP", "sol peruano": "PEN", "peso argentino": "ARS", "zloty": "PLN", "esloti": "PLN",
                  "florin": "HUF", "leu": "RON", "lira turca": "TRY", "lira": "TRY", "rand": "ZAR", "seq": "ILS", "shekel": "ILS",
                  "libra egipcia": "EGP", "naira": "NGN", "riyal saudi": "SAR", "dirham": "AED"}
REGIMENES = ("LIBRE_FLOTACION", "FLOTACION_ADMINISTRADA", "BANDA", "TIPO_FIJO", "CAJA_CONVERSION", "CONTROLES")
# Campos que delatan una decisión del Bloque B (instrumento, proveedor, coste, apalancamiento, tamaño, entrada)
CAMPOS_PROHIBIDOS = ("vehiculos_genericos", "instrumento", "instrumentos", "proveedor", "apalancamiento", "tamano_posicion",
                     "tamaño_posicion", "nivel_entrada", "precio_entrada", "stop_loss", "take_profit", "coste_implementacion")
# Recomendación de instrumento concreto o de ejecución en un texto de la opción
RE_INSTRUMENTO = re.compile(
    r"(?i)\b(?:compr(?:ar|a|e)|vend(?:er|a|e)|usar|utiliz(?:ar|a|e)|recomend\w*|sugerimos|conviene|se aconseja|operar|"
    r"mediante|v[ií]a|a\s+trav[eé]s\s+de|con)\s+(?:un|una|el|la|los|las|unos|unas)?\s*"
    r"(?:ETF|ETC|ETN|CFDs?|futuros?|forwards?|opci[oó]n(?:es)?\s+(?:call|put|de\s+compra|de\s+venta)|calls?|puts?|swaps?|"
    r"NDFs?|cuenta\s+en\s+divisas|dep[oó]sitos?\s+en\s+divisas)\b")
RE_EJECUCION = re.compile(r"(?i)\b(?:nivel|precio|punto)\s+de\s+entrada\b|\bstop[\s-]?loss\b|\btake[\s-]?profit\b|"
                          r"\bapalancamiento\s+(?:de\s+)?\d|\b\d+\s*[x×]\s+de\s+apalancamiento\b|\btama[nñ]o\s+de\s+(?:la\s+)?posici[oó]n\b")
RE_ISIN = re.compile(r"\b[A-Z]{2}[A-Z0-9]{9}[0-9]\b")
RE_PAR = re.compile(r"^([A-Z]{3})/([A-Z]{3})$")
RE_ISO = re.compile(r"^[A-Z]{3}$")
# Códigos ISO 4217 de divisas en circulación (más XAU y XAG, que el bloque usa solo como referencia de refugio)
ISO_4217 = frozenset("""
AED AFN ALL AMD ANG AOA ARS AUD AWG AZN BAM BBD BDT BGN BHD BIF BMD BND BOB BRL BSD BTN BWP BYN BZD CAD CDF CHF CLP CNY
CNH COP CRC CUP CVE CZK DJF DKK DOP DZD EGP ERN ETB EUR FJD FKP GBP GEL GHS GIP GMD GNF GTQ GYD HKD HNL HTG HUF IDR ILS
INR IQD IRR ISK JMD JOD JPY KES KGS KHR KMF KPW KRW KWD KYD KZT LAK LBP LKR LRD LSL LYD MAD MDL MGA MKD MMK MNT MOP MRU
MUR MVR MWK MXN MYR MZN NAD NGN NIO NOK NPR NZD OMR PAB PEN PGK PHP PKR PLN PYG QAR RON RSD RUB RWF SAR SBD SCR SDG SEK
SGD SHP SLE SOS SRD SSP STN SVC SYP SZL THB TJS TMT TND TOP TRY TTD TWD TZS UAH UGX USD UYU UZS VES VND VUV WST XAF XCD
XOF XPF YER ZAR ZMW ZWG XAU XAG
""".split())
# Convención de mercado para la divisa base: cuanto antes en la lista, más «base». Las divisas que no figuran
# (emergentes) se cotizan contra las de la lista (USD/MXN, EUR/PLN); el JPY es siempre cotizada (ZAR/JPY, MXN/JPY).
PRIORIDAD_BASE = ("XAU", "XAG", "EUR", "GBP", "AUD", "NZD", "USD", "CAD", "CHF", "NOK", "SEK", "DKK")
STOPWORDS = {"de", "del", "la", "el", "los", "las", "y", "e", "en", "a", "al", "con", "por", "para", "sobre", "un", "una",
             "frente", "entre", "su", "sus"}
BANDAS_CUALITATIVAS = ("más probable que no", "incierto", "poco probable")
ENUMS = {
    "tipo": ("PERIODICO", "AD_HOC", "PROFUNDIZACION"),
    "estado_semaforo": ("VERDE", "AMBAR", "GRIS"),
    "relevancia_decisional": ("ALTA", "MEDIA", "BAJA"),
    "reversibilidad": ("alta", "media", "baja"),
    "liquidez": ("alta", "media", "baja"),
    "siguiente_paso_sugerido": ("ENVIAR_A_BLOQUE_B", "PROFUNDIZAR_EN_A", "VIGILAR", "DESCARTAR"),
    "confianza": ("establecido", "probable", "especulativo", "en disputa"),
    "fuerza": ("fuerte", "moderada", "debil", "débil"),
    "signo_carry": ("a favor", "en contra", "neutro", "no aplicable"),
}
RE_EXPOSICION = re.compile(r"^(?:(?:larga|corta)(?: moderada| fuerte)?|neutra)$")
CAMPOS_RAIZ = ["run_id", "fecha", "methodology_version", "tipo", "regimen_macro", "regimen_cambiario", "apuestas_independientes",
               "exposicion_agregada", "segmentos", "seguimiento_vigentes", "historial_aciertos", "paquete_para_bloque_B",
               "preguntas_sugeridas", "limitaciones"]
CAMPOS_SEGMENTO = ["estado_semaforo", "regimen_segmento", "candidatas_analizadas", "opciones", "menos_de_tres_motivo"]
CAMPOS_OPCION_NO_VACIOS = ["opp_id", "rango", "tipo_opcion", "segmento", "nombre", "nombre_llano", "tesis",
                           "mecanismo", "puntuaciones", "horizontes", "valoracion", "riesgos", "riesgo_1a5",
                           "invalidacion", "convertibilidad", "liquidez", "relevancia_decisional", "reversibilidad",
                           "siguiente_paso_sugerido", "que_cambiaria_la_conclusion", "confianza", "evidencias", "calculos"]
# «ambito» e «indicador_seguimiento» se comprueban en C15; «par», «direccion», «composicion» y «divisa_financiacion» en
# G3-FX-01/02 (pueden ser nulos según el tipo de opción); «carry» en G3-FX-05 y «convertibilidad» en G3-FX-04
CAMPOS_OPCION_PRESENTES = ["tnd_ids", "catalizadores", "objeciones", "par", "direccion", "composicion", "divisa_financiacion"]
# Encargo para el Bloque B (2.5 y Anexo B Forex)
CAMPOS_BLOQUE_B = ["segmento", "tipo_opcion", "par", "composicion", "direccion", "divisa_financiacion", "ambito", "tesis",
                   "mecanismo", "horizonte_principal", "horizontes", "pronosticos", "catalizadores", "riesgos", "invalidacion", "indicador_seguimiento",
                   "carry_esperado", "consideraciones_implementacion", "metricas_clave", "preguntas_para_B", "evidencias",
                   "calculos"]
CAMPOS_BLOQUE_B_PUEDEN_VACIOS = ("catalizadores", "par", "direccion", "composicion", "divisa_financiacion")
RE_SECRETO = re.compile(
    r"(?i)(\"(api[_-]?key|apikey|secret|client_secret|password|passwd|contraseña|access[_-]?token|bearer)\"\s*:\s*\"[^\"]+\")"
    r"|(sk-[A-Za-z0-9_-]{20,})|(AKIA[0-9A-Z]{16})|(-----BEGIN [A-Z ]*PRIVATE KEY-----)|(Bearer\s+[A-Za-z0-9._-]{20,})")
# R8 V1.1: el valor de una credencial nunca viaja en un paquete; solo su alias (`credencial_ref`) y su estado
RE_VALOR_CREDENCIAL = re.compile(
    r"(?i)\"(credencial(?:_valor)?|valor_credencial|clave(?:_api)?|api_token|token|secreto)\"\s*:\s*\"[^\"]{6,}\"")


class Registro:
    NOMBRES = {
        "C01": "Campos obligatorios, valores permitidos y prefijos FX", "C02": "Máximo de opciones por segmento, rangos y clústeres (9.6.3)",
        "C03": "Menos de tres con motivo (R14)", "C04": "Puntuaciones reconstruibles con HT-03",
        "C05": "Elegibilidad (9.2), puertas G1–G4 / PS1–PS8 y PS3 de convertibilidad",
        "C06": "Horizontes compatibles con la tabla 8.3 por segmento",
        "C07": "Probabilidad numérica solo con certificado (R13)", "C08": "Evidencias y cálculos referenciados (R7)",
        "C09": "Objeciones resueltas o respondidas (R12)", "C10": "Relevancia decisional y riesgo 1–5 (Anexo A)",
        "C11": "Paquete para el Bloque B", "C12": "Legibilidad del informe visual (HT-07)",
        "C13": "Ausencia de credenciales (R8)", "C14": "Coherencia del semáforo y apuestas independientes",
        "C15": "Frontera con el Bloque B: sin instrumentos concretos ni ejecución (R21)",
        "C16": "Oportunidad duplicada en dos segmentos (2.6)",
        "C17": "Naturaleza de la inversión y horizonte principal (8.3)",
        "C18": "H5 limitado: ámbito estructural, banda cualitativa e hitos (8.3, R13)",
        "C19": "Supuestos declarados de consultas al Broker (6.2.9, CT-23)",
        # Comprobaciones específicas de divisas (Anexo 1 del Plan de pruebas Forex)
        "G3-FX-01": "Notación BASE/COTIZADA y dirección", "G3-FX-02": "Composición de cestas (PS4)",
        "G3-FX-03": "Asignación de segmento (2.6)", "G3-FX-04": "Convertibilidad (PS3) y riesgo de régimen",
        "G3-FX-05": "Carry", "G3-FX-06": "Referencias ingenuas (paseo aleatorio, forward)",
        "G3-FX-07": "Anticipación en fijaciones", "G3-FX-08": "Exposición agregada y contradicciones",
        "G3-FX-09": "Diversidad por divisa", "G3-FX-10": "Capas transversales (CT-06T)",
        "G3-FX-11": "Tipo de rentabilidad y divisa de medición",
    }

    def __init__(self) -> None:
        self.inc: Dict[str, List[Dict]] = {k: [] for k in self.NOMBRES}
        self.extra: Dict[str, Any] = {}

    def bloqueo(self, c: str, ruta: str, detalle: str) -> None:
        self.inc[c].append({"severidad": "BLOQUEO", "ruta": ruta, "detalle": detalle})

    def advertencia(self, c: str, ruta: str, detalle: str) -> None:
        self.inc[c].append({"severidad": "ADVERTENCIA", "ruta": ruta, "detalle": detalle})

    def comprobaciones(self) -> List[Dict]:
        out = []
        for c, nombre in self.NOMBRES.items():
            sev = {i["severidad"] for i in self.inc[c]}
            res = "BLOQUEO" if "BLOQUEO" in sev else ("ADVERTENCIA" if sev else "OK")
            entrada = {"id": c, "nombre": nombre, "resultado": res, "incidencias": self.inc[c]}
            if c in self.extra:
                entrada["datos"] = self.extra[c]
            out.append(entrada)
        return out


def _vacio(v: Any) -> bool:
    return v is None or (isinstance(v, (str, list, dict)) and len(v) == 0) or (isinstance(v, str) and not v.strip()) \
        or (isinstance(v, str) and v.strip() in ("…", "..."))


def es_isin(codigo: str) -> bool:
    """ISIN con dígito de control válido (Luhn sobre la conversión letra→número)."""
    if not RE_ISIN.fullmatch(codigo or "") or not any(ch.isdigit() for ch in codigo[2:11]):
        return False
    digitos = "".join(str(int(ch, 36)) for ch in codigo[:-1])
    total = 0
    for i, ch in enumerate(reversed(digitos)):
        n = int(ch)
        if i % 2 == 0:
            n *= 2
            n = n - 9 if n > 9 else n
        total += n
    return (10 - total % 10) % 10 == int(codigo[-1])


def normalizar_texto(t: Any) -> str:
    """Minúsculas, sin tildes ni signos, sin palabras vacías: clave para detectar duplicados entre segmentos."""
    import unicodedata
    t = unicodedata.normalize("NFKD", str(t or "")).encode("ascii", "ignore").decode("ascii").lower()
    t = re.sub(r"\(.*?\)", " ", t)
    palabras = [w for w in re.split(r"[^a-z0-9]+", t) if w and w not in STOPWORDS]
    return " ".join(palabras)


def clave_ambito(op: Dict) -> Optional[str]:
    amb = op.get("ambito")
    if not isinstance(amb, dict) or _vacio(amb.get("incluye")):
        return None
    return normalizar_texto(amb.get("incluye"))


def clave_exposicion(op: Dict) -> Optional[str]:
    """Clave de exposición (par y dirección, o composición con lados): la misma apuesta cambiaria en dos segmentos."""
    ex = ht03.exposiciones_de(op)
    if not ex:
        if op.get("par") and op.get("direccion"):
            return f"{op['par']}|{op['direccion']}"
        return None
    return " ".join(sorted(f"{e['divisa']}:{e['lado']}" for e in ex))


def lados_par(par: str, direccion: str) -> Optional[Dict[str, str]]:
    m = RE_PAR.match(par or "")
    if not m or direccion not in DIRECCIONES_BASE:
        return None
    base, cot = m.groups()
    if base == cot:
        return None
    return {base: "LARGO", cot: "CORTO"} if direccion == "ALCISTA_BASE" else {base: "CORTO", cot: "LARGO"}


def notacion_convencional(base: str, cot: str) -> bool:
    """True si BASE/COTIZADA sigue la convención de mercado (EUR/USD, USD/JPY, EUR/PLN, USD/MXN, ZAR/JPY)."""
    if cot == "JPY":
        return True
    if base == "JPY":
        return False
    rb = PRIORIDAD_BASE.index(base) if base in PRIORIDAD_BASE else None
    rc = PRIORIDAD_BASE.index(cot) if cot in PRIORIDAD_BASE else None
    if rb is None and rc is None:
        return True                       # dos emergentes: sin convención única
    if rb is None:
        return False                      # emergente como base frente a una divisa de la lista (MXN/USD)
    if rc is None:
        return True
    return rb < rc


def _horizontes_ofrecidos(op: Dict) -> Dict[str, Dict]:
    h = op.get("horizontes") or {}
    if not isinstance(h, dict):
        return {}
    return {k: v for k, v in h.items() if isinstance(v, dict) and any(not _vacio(x) for x in v.values())}


def _es_vigente(op: Dict, vigentes: set) -> bool:
    if isinstance(op.get("vigente"), bool):
        return op["vigente"]
    if str(op.get("estado", "")).upper() == "VIGENTE":
        return True
    return op.get("opp_id") in vigentes


def patas_activas(op: Dict) -> Dict[str, str]:
    """Pata activa de la tesis (9.6.6): la divisa cuyo movimiento se pronostica, con su lado (LARGO/CORTO).
    Si la opción declara `pata_activa` (lista de códigos ISO), se usa. Si no: en PAR, CRUCE y REGIMEN, la divisa que no
    es USD ni EUR (las dos en un cruce sin USD ni EUR; la larga si el par es EUR/USD); en CESTA, BLOQUE y ESTRATEGIA,
    las divisas del lado opuesto al de la divisa de financiación; en VOLATILIDAD, ninguna."""
    comp = {c.get("divisa"): c.get("lado") for c in (op.get("composicion") or []) if isinstance(c, dict)}
    expl = op.get("pata_activa")
    if isinstance(expl, str):
        expl = [expl]
    if isinstance(expl, list) and expl:
        return {d: comp[d] for d in expl if d in comp}
    tipo = op.get("tipo_opcion")
    if tipo == "VOLATILIDAD" or not comp:
        return {}
    if tipo in TIPOS_CON_DIRECCION or len(comp) == 2 and tipo not in TIPOS_CESTA:
        propias = {d: l for d, l in comp.items() if d not in CONTRAPARTIDAS}
        return propias or {d: l for d, l in comp.items() if l == "LARGO"}
    fin = op.get("divisa_financiacion")
    lado_fin = comp.get(fin, "CORTO")
    return {d: l for d, l in comp.items() if l != lado_fin}


def relevancia_esperada_alta(op: Dict, segmento: str, vigente: bool, p: Dict) -> List[str]:
    """Disparadores de relevancia ALTA según la nota 3 del Anexo A del Documento 0 Forex."""
    motivos = []
    r = op.get("riesgo_1a5")
    if isinstance(r, (int, float)) and r >= 4:
        motivos.append(f"riesgo {r}/5 ≥ 4")
    if str(op.get("reversibilidad", "")).lower() == "baja":
        motivos.append("reversibilidad baja (divisa con NDF o controles)")
    if "H4" in _horizontes_ofrecidos(op) and ((isinstance(r, (int, float)) and r >= 3)
                                               or str(op.get("liquidez", "")).lower() == "baja"):
        motivos.append("horizonte H4 con riesgo ≥ 3 o liquidez baja")
    if op.get("horizonte_principal") == "H5":
        motivos.append("horizonte principal H5")
    pu = op.get("puntuaciones") or {}
    E, A = pu.get("E"), pu.get("A")
    if isinstance(E, (int, float)) and isinstance(A, (int, float)) and E < p.get("rel_E", 70) and A >= p.get("rel_A", 75):
        motivos.append(f"E {E} < 70 con A {A} ≥ 75 (atractiva pero incierta)")
    if op.get("tipo_opcion") == "REGIMEN":
        motivos.append("opción de tipo REGIMEN")
    if segmento in SEGMENTOS_EMERGENTES and str(op.get("liquidez", "")).lower() == "baja":
        motivos.append("divisa emergente de liquidez baja")
    return motivos


def riesgo_minimo(op: Dict) -> Optional[str]:
    """Nota 2 del Anexo A: un tipo fijo con riesgo de ruptura o una divisa con controles parte, como mínimo, de 4."""
    conv = op.get("convertibilidad") if isinstance(op.get("convertibilidad"), dict) else {}
    if conv.get("controles_capitales") is True:
        return "divisa con controles de capitales"
    if op.get("regimen_cambiario_divisa") in ("TIPO_FIJO", "CAJA_CONVERSION"):
        return f"tipo fijo ({op.get('regimen_cambiario_divisa')}) con riesgo de ruptura"
    if op.get("tipo_opcion") == "REGIMEN":
        return (f"opción REGIMEN sobre un régimen {op.get('regimen_cambiario_divisa') or 'no declarado'}: ruptura o ajuste de un tipo "
                "fijo, una banda o un control de capitales")
    return None


def _textos_opcion(op: Dict) -> List[str]:
    amb = op.get("ambito") if isinstance(op.get("ambito"), dict) else {}
    return [x for x in [op.get("nombre"), op.get("nombre_llano"), op.get("tesis"), op.get("mecanismo"), op.get("valoracion"),
                        op.get("por_que_llano"), op.get("sube_baja_llano")] + list(amb.values())
            + list(op.get("invalidacion") or []) + list(op.get("que_cambiaria_la_conclusion") or []) if isinstance(x, str)]


def _frontera(R: Registro, ruta: str, textos: List[str], campos: Dict) -> None:
    for c in CAMPOS_PROHIBIDOS:
        if c in campos:
            R.bloqueo("C15", f"{ruta}.{c}", f"Campo «{c}» propio del Bloque B (instrumento, proveedor, coste, apalancamiento, "
                                            "tamaño o entrada): el Bloque A Forex no lo decide (R21)")
    for t in textos:
        m = RE_INSTRUMENTO.search(t)
        if m:
            R.bloqueo("C15", ruta, f"Propone un instrumento concreto («{m.group(0)}»): la granularidad máxima es el par, la cesta "
                                   "o la estrategia; el instrumento lo elige el Bloque B (R21)")
        m = RE_EJECUCION.search(t)
        if m:
            R.bloqueo("C15", ruta, f"Decisión de ejecución («{m.group(0)}»): los niveles del par solo pueden ser condiciones de "
                                   "invalidación, nunca de entrada, y el tamaño o el apalancamiento son del Bloque B (2.5)")
        isins = sorted({x for x in RE_ISIN.findall(t) if es_isin(x)})
        if isins:
            R.bloqueo("C15", ruta, f"Identificador de instrumento concreto (ISIN): {', '.join(isins)}")


def _divisa_de_nombre(texto: str) -> List[str]:
    """Códigos ISO de las divisas nombradas en un texto llano, en orden de aparición (coincidencia más larga primero)."""
    import unicodedata
    t = unicodedata.normalize("NFKD", str(texto or "")).encode("ascii", "ignore").decode("ascii").lower()
    hallados = []
    for nombre in sorted(NOMBRES_LLANOS, key=len, reverse=True):
        for m in re.finditer(r"\b" + re.escape(nombre) + r"\b", t):
            if not any(a <= m.start() < b for a, b, _ in hallados):
                hallados.append((m.start(), m.end(), NOMBRES_LLANOS[nombre]))
    return [c for _, _, c in sorted(hallados)]


def lados_desde_nombre_llano(texto: str) -> Optional[Dict[str, str]]:
    """«El yen podría ganar valor frente al dólar» → {JPY: LARGO, USD: CORTO}. None si no se reconoce el patrón."""
    import unicodedata
    t = unicodedata.normalize("NFKD", str(texto or "")).encode("ascii", "ignore").decode("ascii").lower()
    if "frente a" not in t:
        return None
    antes, despues = t.split("frente a", 1)
    a, b = _divisa_de_nombre(antes), _divisa_de_nombre(despues)
    if len(a) != 1 or len(b) != 1 or a[0] == b[0]:
        return None
    if re.search(r"ganar valor|subir|suba|apreci|fortalec", antes):
        return {a[0]: "LARGO", b[0]: "CORTO"}
    if re.search(r"perder valor|bajar|baje|depreci|debilit", antes):
        return {a[0]: "CORTO", b[0]: "LARGO"}
    return None


def segmento_esperado(op: Dict) -> Optional[str]:
    """Reglas 1–3 de 2.6: divisa menos líquida; tres o más divisas o regla sistemática → ESTR; volatilidad de un par →
    segmento del par. None si no se puede determinar (divisa fuera de la tabla de 2.6)."""
    tipo = op.get("tipo_opcion")
    if tipo == "ESTRATEGIA":
        return "ESTR"
    divisas = sorted({c.get("divisa") for c in (op.get("composicion") or []) if isinstance(c, dict) and c.get("divisa")})
    m = RE_PAR.match(str(op.get("par") or ""))
    if m and tipo in ("PAR", "CRUCE", "VOLATILIDAD", "REGIMEN"):
        divisas = list(m.groups())
    elif tipo == "VOLATILIDAD":
        return "ESTR"                      # estrategia de volatilidad sobre varias divisas
    if len(divisas) >= 3:
        return "ESTR"
    if len(divisas) != 2:
        return None
    segs = [SEGMENTO_DE_DIVISA.get(d) for d in divisas]
    if None in segs:
        return None
    return max(segs, key=lambda s: LIQUIDEZ_SEGMENTO.index(s))


def _composicion(R: Registro, ruta: str, op: Dict, tipo: str) -> Dict[str, float]:
    """G3-FX-01 (notación y dirección) y G3-FX-02 (composición de cestas, PS4). Devuelve la exposición neta por divisa."""
    par, direc, comp, fin = op.get("par"), op.get("direccion"), op.get("composicion"), op.get("divisa_financiacion")
    neta: Dict[str, float] = {}
    if tipo in TIPOS_CON_DIRECCION:
        if direc not in DIRECCIONES_BASE:
            R.bloqueo("G3-FX-01", f"{ruta}.direccion", f"Una opción {tipo} con par exige `direccion` ALCISTA_BASE o BAJISTA_BASE "
                                                        f"referida a la base ({direc!r}); PS4 si falta")
    elif direc is not None:
        R.bloqueo("G3-FX-01", f"{ruta}.direccion", f"En una opción {tipo} la dirección no va en `direccion` sino en "
                                                    + ("`vista_volatilidad`" if tipo == "VOLATILIDAD" else "`composicion` (LARGO/CORTO y peso)")
                                                    + " (2.4); debe ser null")
    if tipo == "VOLATILIDAD":
        vv = op.get("vista_volatilidad")
        if not isinstance(vv, dict) or vv.get("sentido") not in ("ALZA", "BAJA") or _vacio(vv.get("plazo")):
            R.bloqueo("G3-FX-01", f"{ruta}.vista_volatilidad", "Una opción VOLATILIDAD expresa su vista con `vista_volatilidad` "
                                                                "{sentido: ALZA|BAJA, plazo} (2.4)")
    if par is not None:
        m = RE_PAR.match(str(par))
        if not m:
            R.bloqueo("G3-FX-01", f"{ruta}.par", f"Notación {par!r} no es BASE/COTIZADA con códigos ISO 4217 (p. ej., EUR/USD)")
        else:
            base, cot = m.groups()
            for d in (base, cot):
                if d not in ISO_4217:
                    R.bloqueo("G3-FX-01", f"{ruta}.par", f"{d} no es un código ISO 4217 en circulación")
            if base == cot:
                R.bloqueo("G3-FX-01", f"{ruta}.par", "La base y la cotizada coinciden")
            elif not notacion_convencional(base, cot):
                R.bloqueo("G3-FX-01", f"{ruta}.par", f"{par} no sigue la convención de mercado (prelación EUR, GBP, AUD, NZD, USD, "
                                                     f"CAD, CHF, NOK, SEK, JPY; ¿{cot}/{base}?)")
    elif tipo in TIPOS_CON_PAR:
        R.bloqueo("G3-FX-01", f"{ruta}.par", f"Una opción {tipo} exige «par» en notación BASE/COTIZADA")
    if tipo == "CRUCE" and isinstance(par, str) and "USD" in par.split("/"):
        R.advertencia("G3-FX-01", f"{ruta}.tipo_opcion", f"{par} incluye el USD: no es un cruce (usar PAR)")
    if tipo == "PAR" and isinstance(par, str) and RE_PAR.match(par) and "USD" not in par.split("/"):
        R.advertencia("G3-FX-01", f"{ruta}.tipo_opcion", f"{par} no incluye el USD: es un cruce (usar CRUCE)")
    # Composición
    if comp is not None and not isinstance(comp, list):
        R.bloqueo("C01", f"{ruta}.composicion", "Debe ser una lista [{divisa, peso, lado}]")
        comp = []
    comp = comp or []
    for j, c in enumerate(comp):
        rc = f"{ruta}.composicion[{j}]"
        if not isinstance(c, dict):
            R.bloqueo("G3-FX-02", rc, "Elemento no válido")
            continue
        if not RE_ISO.match(str(c.get("divisa", ""))) or c.get("divisa") not in ISO_4217:
            R.bloqueo("G3-FX-02", rc, f"Divisa {c.get('divisa')!r} no es un código ISO 4217")
        if c.get("lado") not in ht03.LADOS:
            R.bloqueo("G3-FX-02", rc, f"Lado {c.get('lado')!r} no es LARGO ni CORTO")
        pe = c.get("peso")
        if isinstance(pe, bool) or not isinstance(pe, (int, float)) or not 0 < pe <= 1:
            R.bloqueo("G3-FX-02", rc, "PS4: peso ausente o fuera de (0, 1]: exposición no cuantificada")
        elif c.get("lado") in ht03.LADOS and isinstance(c.get("divisa"), str):
            neta[c["divisa"]] = neta.get(c["divisa"], 0.0) + (pe if c["lado"] == "LARGO" else -pe)
    if tipo in TIPOS_CESTA:
        if len(comp) < 2:
            R.bloqueo("G3-FX-02", f"{ruta}.composicion", f"PS4: {tipo} sin composición (divisas, pesos y lados)")
        for lado in ht03.LADOS:
            suma = sum(c.get("peso", 0) for c in comp if isinstance(c, dict) and c.get("lado") == lado
                       and isinstance(c.get("peso"), (int, float)) and not isinstance(c.get("peso"), bool))
            if comp and abs(suma - 1) > 0.011:
                R.bloqueo("G3-FX-02", f"{ruta}.composicion", f"Los pesos del lado {lado} suman {suma:.2f} (deben sumar 1)")
        if _vacio(fin):
            R.bloqueo("G3-FX-02", f"{ruta}.divisa_financiacion", f"PS4: {tipo} sin divisa de financiación")
        elif not any(isinstance(c, dict) and c.get("divisa") == fin and c.get("lado") == "CORTO" for c in comp):
            R.advertencia("G3-FX-02", f"{ruta}.divisa_financiacion", f"{fin} no figura como lado CORTO de la composición")
    lp = lados_par(str(par or ""), str(direc or ""))
    if lp:
        if comp:
            de_comp = {c.get("divisa"): c.get("lado") for c in comp if isinstance(c, dict)}
            if any(de_comp.get(d) not in (None, l) for d, l in lp.items()):
                R.bloqueo("G3-FX-01", f"{ruta}.composicion", f"Dirección incoherente con la composición: {par} {direc} exige {lp}")
        else:
            for d, l in lp.items():
                neta[d] = neta.get(d, 0.0) + (1.0 if l == "LARGO" else -1.0)
        vendida = next(d for d, l in lp.items() if l == "CORTO")
        if _vacio(fin):
            R.bloqueo("G3-FX-01", f"{ruta}.divisa_financiacion", "PS4: dirección sin divisa de financiación")
        elif fin != vendida:
            R.bloqueo("G3-FX-01", f"{ruta}.divisa_financiacion", f"{fin} no es la divisa que se vende en {par} {direc} (debería ser {vendida})")
        ll = lados_desde_nombre_llano(op.get("nombre_llano"))
        if ll and all(d in lp for d in ll) and ll != lp:
            R.bloqueo("G3-FX-01", f"{ruta}.nombre_llano", f"«{op.get('nombre_llano')}» contradice la dirección {par} {direc}")
    if fin is not None and not _vacio(fin) and fin not in ISO_4217:
        R.bloqueo("G3-FX-02", f"{ruta}.divisa_financiacion", f"{fin!r} no es un código ISO 4217")
    if tipo == "REGIMEN" and op.get("regimen_cambiario_divisa") not in REGIMENES:
        R.bloqueo("G3-FX-04", f"{ruta}.regimen_cambiario_divisa", f"Una opción REGIMEN declara el régimen ({'/'.join(REGIMENES)})")
    return neta


def _carry(R: Registro, ruta: str, op: Dict, tipo: str) -> None:
    """G3-FX-05: carry anual, signo, carry ajustado por volatilidad y CALC-; signo coherente con la dirección y el diferencial."""
    ca = op.get("carry")
    if not isinstance(ca, dict):
        R.bloqueo("G3-FX-05", f"{ruta}.carry", "Opción sin bloque de carry {anual_pct, signo, ajustado_vol, calc_id}")
        return
    v, sg, aj, calc = ca.get("anual_pct"), ca.get("signo"), ca.get("ajustado_vol"), ca.get("calc_id")
    if sg not in ENUMS["signo_carry"]:
        R.bloqueo("G3-FX-05", f"{ruta}.carry.signo", f"Signo {sg!r} no permitido ({'/'.join(ENUMS['signo_carry'])})")
        return
    if sg == "no aplicable":
        if tipo != "VOLATILIDAD":
            R.bloqueo("G3-FX-05", f"{ruta}.carry", "Carry «no aplicable» solo en opciones de VOLATILIDAD")
        return
    num = isinstance(v, (int, float)) and not isinstance(v, bool)
    if not num:
        R.bloqueo("G3-FX-05", f"{ruta}.carry.anual_pct", "Opción sin carry anual")
        return
    if not isinstance(aj, (int, float)) or isinstance(aj, bool):
        R.bloqueo("G3-FX-05", f"{ruta}.carry.ajustado_vol", "Opción sin carry ajustado por volatilidad")
    elif (aj > 0) != (v > 0) and abs(v) > 1e-9 and abs(aj) > 1e-9:
        R.bloqueo("G3-FX-05", f"{ruta}.carry.ajustado_vol", "El carry ajustado por volatilidad tiene signo distinto del carry anual")
    if _vacio(calc) or not str(calc).startswith("CALC-FX-"):
        R.bloqueo("G3-FX-05", f"{ruta}.carry.calc_id", "Cifra de carry sin cálculo CALC-FX- (R7)")
    esperado = "a favor" if v > 0.25 else ("en contra" if v < -0.25 else "neutro")
    if sg != esperado and not (sg == "neutro" and abs(v) <= 0.5) and not (esperado == "neutro" and sg in ("a favor", "en contra")
                                                                         and (sg == "a favor") == (v > 0)):
        R.bloqueo("G3-FX-05", f"{ruta}.carry", f"Signo «{sg}» incoherente con un carry de {v:+.2f} % anual")
    dif = ca.get("diferencial_tipos_pct")
    direc = op.get("direccion")
    if isinstance(dif, (int, float)) and not isinstance(dif, bool) and direc in DIRECCIONES_BASE and abs(dif) > 0.05:
        esperado_v = dif if direc == "ALCISTA_BASE" else -dif
        if (esperado_v > 0) != (v > 0):
            R.bloqueo("G3-FX-05", f"{ruta}.carry", f"Carry {v:+.2f} % incoherente con la dirección {direc} y el diferencial de tipos "
                                                   f"base − cotizada {dif:+.2f} %")


def _meses_entre(a: str, b: str) -> Optional[float]:
    ma, mb = RE_FECHA_ISO.match(str(a or "")), RE_FECHA_ISO.match(str(b or ""))
    if not ma or not mb:
        return None
    ya, xa, da = (int(x) for x in ma.groups())
    yb, xb, db = (int(x) for x in mb.groups())
    return (yb - ya) * 12 + (xb - xa) + (db - da) / 30.0


def _horizonte_principal(R: "Registro", ro: str, op: Dict, seg: str) -> None:
    """C17 · Regla de adecuación del horizonte al tipo de inversión (Documento 0 Forex V1.1, 8.3)."""
    nat, hp = op.get("naturaleza_inversion"), op.get("horizonte_principal")
    if _vacio(nat):
        R.bloqueo("C17", f"{ro}.naturaleza_inversion", "Naturaleza de la inversión ausente (8.3)")
    elif nat == "LIQUIDEZ":
        R.bloqueo("C17", f"{ro}.naturaleza_inversion", "LIQUIDEZ es una naturaleza del Bloque A general; no se usa en el Bloque A Forex")
    elif nat not in NATURALEZAS:
        R.bloqueo("C17", f"{ro}.naturaleza_inversion", f"Valor no permitido {nat!r} ({'/'.join(NATURALEZAS)})")
    if _vacio(hp):
        R.bloqueo("C17", f"{ro}.horizonte_principal", "Horizonte principal ausente (8.3)")
        return
    if hp not in HORIZONTES:
        R.bloqueo("C17", f"{ro}.horizonte_principal", f"Horizonte principal desconocido {hp!r}")
        return
    if hp not in _horizontes_ofrecidos(op):
        R.bloqueo("C17", f"{ro}.horizonte_principal", f"{hp} no figura entre los horizontes ofrecidos por la opción")
    regla = TABLA_HORIZONTES.get(seg, {}).get(hp)
    if regla == "NO":
        R.bloqueo("C17", f"{ro}.horizonte_principal", f"{hp} en celda «No» de {seg} (tabla 8.3)")
    elif regla == "LIMITADO" and hp != "H5" and not op.get("catalizadores"):
        R.advertencia("C17", f"{ro}.horizonte_principal", f"{hp} «limitado» en {seg} sin catalizador identificado")
    if nat in RANGO_NATURALEZA and hp not in RANGO_NATURALEZA[nat]:
        rango = f"{RANGO_NATURALEZA[nat][0]}–{RANGO_NATURALEZA[nat][-1]}"
        if hp == "H5":
            R.bloqueo("C17", f"{ro}.horizonte_principal", f"H5 como horizonte principal exige naturaleza ESTRUCTURAL ({nat})")
        elif _vacio(op.get("justificacion_horizonte")):
            R.bloqueo("C17", f"{ro}.horizonte_principal", f"{hp} fuera del rango de la naturaleza {nat} ({rango}) sin "
                                                          "`justificacion_horizonte`")
        else:
            R.advertencia("C17", f"{ro}.horizonte_principal", f"{hp} fuera del rango de la naturaleza {nat} ({rango}), con "
                                                              "justificación: dictamina el Orquestador (CT-14)")


def _h5(R: "Registro", rh: str, hv: Dict, op: Dict, fecha_paquete: Optional[str]) -> None:
    """C18 · H5 «limitado»: solo ESTRUCTURAL, en uno de los tres ámbitos, sin probabilidad numérica y con hitos (Anexo A)."""
    if op.get("naturaleza_inversion") != "ESTRUCTURAL":
        R.bloqueo("C18", rh, f"H5 solo para naturaleza ESTRUCTURAL (declarada {op.get('naturaleza_inversion')!r}); nunca para "
                             "tesis tácticas o cíclicas sobre un par")
    amb = hv.get("ambito_h5") or op.get("ambito_h5")
    if amb not in AMBITOS_H5:
        R.bloqueo("C18", rh, f"H5 fuera de los tres ámbitos admitidos ({'/'.join(AMBITOS_H5)}): {amb!r}")
    if hv.get("prob") is not None:
        R.bloqueo("C18", rh, "H5 con probabilidad numérica: en H5 la probabilidad es siempre cualitativa y no certificable (R13)")
    if _vacio(hv.get("banda")):
        R.bloqueo("C18", rh, "H5 sin banda verbal")
    hitos = hv.get("hitos")
    if not isinstance(hitos, list) or len(hitos) < H5_MIN_HITOS:
        R.bloqueo("C18", f"{rh}.hitos", f"H5 con {len(hitos) if isinstance(hitos, list) else 0} hitos; mínimo {H5_MIN_HITOS} (Anexo A)")
        return
    fechas = []
    for i, x in enumerate(hitos):
        rx = f"{rh}.hitos[{i}]"
        if not isinstance(x, dict):
            R.bloqueo("C18", rx, "El hito debe ser un objeto {hit_id, fecha, indicador, criterio}")
            continue
        for c in ("fecha", "indicador", "criterio"):
            if _vacio(x.get(c)):
                R.bloqueo("C18", f"{rx}.{c}", "Campo del hito ausente o vacío")
        hid = x.get("hit_id")
        if not _vacio(hid) and not re.match(r"^HIT-FX-\d{4}-\d{4,}$", str(hid)):
            R.bloqueo("C18", f"{rx}.hit_id", f"{hid} no sigue el formato HIT-FX-AAAA-NNNN")
        if RE_FECHA_ISO.match(str(x.get("fecha") or "")):
            fechas.append(str(x["fecha"]))
        elif not _vacio(x.get("fecha")):
            R.bloqueo("C18", f"{rx}.fecha", f"Fecha no ISO {x.get('fecha')!r}")
    fechas.sort()
    if fechas and fecha_paquete and RE_FECHA_ISO.match(str(fecha_paquete)):
        m = _meses_entre(str(fecha_paquete), fechas[0])
        if m is not None and m > H5_PRIMER_HITO_MESES:
            R.bloqueo("C18", f"{rh}.hitos", f"Primer hito a {m:.0f} meses (> {H5_PRIMER_HITO_MESES}, Anexo A)")
        if m is not None and m < 0:
            R.bloqueo("C18", f"{rh}.hitos", "Primer hito anterior a la fecha del paquete")
    for a, b in zip(fechas, fechas[1:]):
        m = _meses_entre(a, b)
        if m is not None and m > H5_MAX_ENTRE_HITOS_MESES:
            R.bloqueo("C18", f"{rh}.hitos", f"{m:.0f} meses entre los hitos {a} y {b} (> {H5_MAX_ENTRE_HITOS_MESES}, Anexo A)")


def _supuestos(R: "Registro", paquete: Dict) -> None:
    """C19 · Toda conclusión que dependa de una consulta CT-23 sin respuesta lleva su supuesto declarado (6.2.9)."""
    sup = paquete.get("supuestos_declarados")
    if sup is None:
        sup = []
    if not isinstance(sup, list):
        R.bloqueo("C19", "supuestos_declarados", "Debe ser una lista [{supuesto, cns_id, efecto_si_falso}]")
        return
    declarados = set()
    for i, s in enumerate(sup):
        rs = f"supuestos_declarados[{i}]"
        if not isinstance(s, dict):
            R.bloqueo("C19", rs, "Cada supuesto debe ser un objeto {supuesto, cns_id, efecto_si_falso}")
            continue
        for c in ("supuesto", "efecto_si_falso"):
            if _vacio(s.get(c)):
                R.bloqueo("C19", f"{rs}.{c}", "Campo ausente o vacío")
        cid = s.get("cns_id")
        if not _vacio(cid):
            if not re.match(r"^CNS-FX-\d{4}-\d{4,}$", str(cid)):
                R.bloqueo("C19", f"{rs}.cns_id", f"{cid} no sigue el formato CNS-FX-AAAA-NNNN")
            declarados.add(str(cid))
    pendientes = paquete.get("consultas_broker_sin_respuesta") or []
    for cid in pendientes:
        if str(cid) not in declarados:
            R.bloqueo("C19", "supuestos_declarados", f"La consulta {cid} sigue sin respuesta y no tiene supuesto declarado (6.2.9)")


# ============================================================================================
# Informe de seguimiento de opción (ciclo C6, 14.4 y Anexo B del Documento 0 Forex V1.1)
# ============================================================================================
SEMAFOROS_SEGUIMIENTO = ("VERDE", "AMBAR", "ROJO")
RECOMENDACIONES_SEGUIMIENTO = ("MANTENER_VIGILANCIA", "PROPONER_ENVIO_A_B", "CERRAR", "PROPONER_CANCELACION")
CAMPOS_SEGUIMIENTO = ["seg_id", "opp_id", "run_id", "ciclo", "fecha", "segmento", "horizonte_principal", "sin_novedad",
                      "semaforo", "que_ha_cambiado", "senales_interes", "invalidacion", "catalizadores", "puntuaciones",
                      "pronosticos_abiertos", "recomendacion", "motivo", "sugerir_profundizacion_N3",
                      "paquete_para_bloque_B", "supuestos_declarados", "limitaciones"]
NOMBRES_SEGUIMIENTO = {"S01": "Campos, prefijos y vocabularios del informe de seguimiento",
                       "S02": "Recomendación coherente (7.11.4)", "S03": "Puntuaciones recalculadas con HT-03",
                       "S04": "Pronósticos abiertos e hitos H5", "S05": "Ausencia de credenciales (R8)",
                       "S06": "Supuestos declarados (6.2.9)"}


def validar_seguimiento(informe: Dict, max_palabras: int = 300, texto: Optional[str] = None) -> Dict:
    """Valida un `informe_seguimiento_opcion` (JSON) y, si se da, la longitud del informe breve (≤ 300 palabras)."""
    R = Registro()
    R.NOMBRES = dict(NOMBRES_SEGUIMIENTO)
    R.inc = {k: [] for k in R.NOMBRES}
    for c in CAMPOS_SEGUIMIENTO:
        if c not in informe:
            R.bloqueo("S01", c, "Campo obligatorio ausente")
    pref = {"seg_id": r"^SEG-FX-\d{4}-\d{4,}$", "opp_id": r"^OPP-FX-\d{4}-\d{4,}$", "run_id": r"^RUN-FX-\d{4}-\d{4,}$"}
    for c, rx in pref.items():
        if informe.get(c) is not None and not re.match(rx, str(informe.get(c))):
            R.bloqueo("S01", c, f"{informe.get(c)!r} no sigue el formato {rx}")
    if informe.get("segmento") is not None and informe.get("segmento") not in SEGMENTOS:
        R.bloqueo("S01", "segmento", f"Segmento desconocido {informe.get('segmento')!r}")
    if informe.get("horizonte_principal") is not None and informe.get("horizonte_principal") not in HORIZONTES:
        R.bloqueo("S01", "horizonte_principal", f"Horizonte desconocido {informe.get('horizonte_principal')!r}")
    if informe.get("semaforo") not in SEMAFOROS_SEGUIMIENTO:
        R.bloqueo("S01", "semaforo", f"Valor no permitido {informe.get('semaforo')!r} ({'/'.join(SEMAFOROS_SEGUIMIENTO)})")
    rec = informe.get("recomendacion")
    if rec not in RECOMENDACIONES_SEGUIMIENTO:
        R.bloqueo("S01", "recomendacion", f"Valor no permitido {rec!r} ({'/'.join(RECOMENDACIONES_SEGUIMIENTO)})")
    if not isinstance(informe.get("ciclo"), int) or informe.get("ciclo", 0) < 1:
        R.bloqueo("S01", "ciclo", "Número de ciclo entero ≥ 1")
    if _vacio(informe.get("motivo")):
        R.bloqueo("S02", "motivo", "Recomendación sin motivo")
    pu = informe.get("puntuaciones") if isinstance(informe.get("puntuaciones"), dict) else {}
    if rec == "PROPONER_ENVIO_A_B":
        if pu.get("elegible") is not True:
            R.bloqueo("S02", "recomendacion", "PROPONER_ENVIO_A_B exige que la opción vuelva a ser elegible (9.2) con HT-03")
        if not isinstance(informe.get("paquete_para_bloque_B"), dict) or not informe["paquete_para_bloque_B"]:
            R.bloqueo("S02", "paquete_para_bloque_B", "PROPONER_ENVIO_A_B sin paquete_para_bloque_B actualizado")
        if informe.get("objeciones_fuertes_abiertas"):
            R.bloqueo("S02", "recomendacion", "PROPONER_ENVIO_A_B con objeciones fuertes abiertas")
    if rec == "CERRAR" and not any(isinstance(x, dict) and x.get("activada") for x in (informe.get("invalidacion") or [])) \
            and _vacio(informe.get("motivo_cierre")):
        R.advertencia("S02", "recomendacion", "CERRAR sin invalidación activada ni `motivo_cierre` (objetivo alcanzado u horizonte vencido)")
    if informe.get("sin_novedad") is True and informe.get("semaforo") == "ROJO":
        R.advertencia("S02", "semaforo", "Ciclo «sin novedad» con semáforo ROJO")
    if informe.get("semaforo") == "ROJO" and rec == "PROPONER_ENVIO_A_B":
        R.bloqueo("S02", "semaforo", "Semáforo ROJO incompatible con PROPONER_ENVIO_A_B")
    if pu:
        if pu.get("fuente") not in (None, "HT-03"):
            R.bloqueo("S03", "puntuaciones.fuente", "Las puntuaciones del seguimiento se recalculan con HT-03")
        for k in ("E", "A", "RK"):
            v = pu.get(k)
            if not isinstance(v, (int, float)) or isinstance(v, bool) or not 0 <= v <= 100:
                R.bloqueo("S03", f"puntuaciones.{k}", f"Puntuación {k} no válida {v!r}")
    else:
        R.bloqueo("S03", "puntuaciones", "Sin puntuaciones actualizadas")
    for i, p in enumerate(informe.get("pronosticos_abiertos") or []):
        rp = f"pronosticos_abiertos[{i}]"
        if not isinstance(p, dict) or not str(p.get("prg_id", "")).startswith("PRG-FX-"):
            R.bloqueo("S04", rp, "Pronóstico sin identificador PRG-FX-")
            continue
        if p.get("horizonte") == "H5" and not p.get("hitos"):
            R.bloqueo("S04", f"{rp}.hitos", "Pronóstico H5 sin hitos HIT-FX-")
        if p.get("nuevo") is True:
            R.bloqueo("S04", rp, "Un ciclo de seguimiento no congela pronósticos nuevos (7.11.3)")
    volcado = json.dumps(informe, ensure_ascii=False)
    for m in list(RE_SECRETO.finditer(volcado)) + list(RE_VALOR_CREDENCIAL.finditer(volcado)):
        R.bloqueo("S05", "(informe)", f"Posible credencial o secreto: «{m.group(0)[:24]}…»")
    sub = Registro()
    _supuestos(sub, informe)
    for x in sub.inc["C19"]:
        R.inc["S06"].append(x)
    if texto is not None:
        n = len(re.findall(r"\w+", texto))
        R.extra["S01"] = {"palabras_informe": n}
        if n > max_palabras and informe.get("sin_novedad") is not True:
            R.advertencia("S01", "(informe breve)", f"{n} palabras > {max_palabras} (14.4)")
        elif informe.get("sin_novedad") is True and n > max_palabras:
            R.bloqueo("S01", "(informe breve)", f"Informe «sin novedad» de {n} palabras")
    comps = R.comprobaciones()
    bloqueos = [c for c in comps if c["resultado"] == "BLOQUEO"]
    advert = [c for c in comps if c["resultado"] == "ADVERTENCIA"]
    dictamen = "BLOQUEADO" if bloqueos else ("APTO_CON_ADVERTENCIAS" if advert else "APTO")
    return {"herramienta": "HT-09", "version": VERSION, "objeto": "informe_seguimiento_opcion", "seg_id": informe.get("seg_id"),
            "run_id": informe.get("run_id"), "dictamen": dictamen,
            "motivo": ("; ".join(f"{c['id']} {c['nombre']}" for c in (bloqueos or advert)) or "Todas las comprobaciones superadas"),
            "comprobaciones": comps}


def validar(paquete: Dict, certificados: Optional[List[Dict]] = None, informe_visual: Optional[str] = None,
            desgloses: Optional[Dict[str, Dict]] = None, parametros: Optional[Dict] = None,
            trazas: Optional[Dict[str, List[str]]] = None, artefactos: Optional[List[str]] = None,
            umbral_fh: float = 70.0) -> Dict:
    R = Registro()
    p = ht03.fusionar_parametros(parametros)
    u = p["umbrales"]
    maxn = p.get("max_opciones_por_segmento", 3)
    certificados = certificados or []
    desgloses = desgloses or {}
    if trazas is None and isinstance(paquete.get("trazas"), dict):
        trazas = paquete["trazas"]

    # C13 credenciales
    volcado = json.dumps(paquete, ensure_ascii=False)
    for m in RE_SECRETO.finditer(volcado):
        R.bloqueo("C13", "(paquete)", f"Posible credencial o secreto: «{m.group(0)[:24]}…»")
    for m in RE_VALOR_CREDENCIAL.finditer(volcado):
        R.bloqueo("C13", "(paquete)", f"Valor de credencial en el paquete («{m.group(1)}»): solo se admite el alias "
                                      "`credencial_ref` de la bóveda de HT-01 (R8, CT-25)")
    # C19 supuestos declarados (6.2.9)
    _supuestos(R, paquete)

    # C01 raíz
    for c in CAMPOS_RAIZ:
        if c not in paquete:
            R.bloqueo("C01", c, "Campo obligatorio ausente")
    for c in ("run_id", "fecha", "methodology_version", "regimen_macro"):
        if c in paquete and _vacio(paquete[c]):
            R.bloqueo("C01", c, "Campo obligatorio vacío")
    if paquete.get("tipo") is not None and paquete.get("tipo") not in ENUMS["tipo"]:
        R.bloqueo("C01", "tipo", f"Valor no permitido {paquete.get('tipo')!r}")
    if paquete.get("run_id") and not re.match(r"^RUN-FX-\d{4}-\d{4,}$", str(paquete["run_id"])):
        R.bloqueo("C01", "run_id", "No sigue el formato RUN-FX-AAAA-NNNN (prefijos del Anexo C Forex)")
    if paquete.get("methodology_version") and not str(paquete["methodology_version"]).startswith("FX-"):
        R.advertencia("C01", "methodology_version", f"Versión de metodología {paquete['methodology_version']} distinta de FX-x.y")
    rc_ = paquete.get("regimen_cambiario")
    if "regimen_cambiario" in paquete:
        opciones_rc = {"dolar": ("fuerte", "neutro", "debil"), "riesgo": ("apetito", "neutro", "aversion"),
                       "volatilidad": ("baja", "media", "alta")}
        if not isinstance(rc_, dict):
            R.bloqueo("C01", "regimen_cambiario", "Debe ser un objeto {dolar, riesgo, volatilidad}")
        else:
            for k, vals in opciones_rc.items():
                if rc_.get(k) not in vals:
                    R.bloqueo("C01", f"regimen_cambiario.{k}", f"Valor {rc_.get(k)!r} no permitido ({'/'.join(vals)})")
    db = paquete.get("divisa_base_usuario")
    if db is not None and db not in ISO_4217:
        R.bloqueo("C01", "divisa_base_usuario", f"{db!r} no es un código ISO 4217")
    segmentos = paquete.get("segmentos") if isinstance(paquete.get("segmentos"), dict) else {}
    vigentes = {s.get("opp_id") for s in (paquete.get("seguimiento_vigentes") or []) if isinstance(s, dict)
                and str(s.get("estado", "")).upper() == "VIGENTE"}
    bloque_b = {b.get("opp_id"): b for b in (paquete.get("paquete_para_bloque_B") or []) if isinstance(b, dict)}
    total_opciones = 0
    ids_vistos: set = set()
    recalculadas: Dict[str, Dict] = {}
    claves_dup: Dict[str, List[tuple]] = {}   # C16: clave normalizada → [(segmento, opp_id)]
    seg_de_opp: Dict[str, str] = {}
    neta_global: Dict[str, float] = {}
    lados_por_divisa: Dict[str, Dict[str, set]] = {}   # pata activa → {LARGO: {(segmento, opp)}, CORTO: {…}} (9.6.6)

    for seg, datos in segmentos.items():
        rs = f"segmentos.{seg}"
        if seg not in SEGMENTOS:
            R.bloqueo("C01", rs, f"Segmento desconocido (válidos: {', '.join(SEGMENTOS)})")
            continue
        if not isinstance(datos, dict):
            R.bloqueo("C01", rs, "El segmento debe ser un objeto")
            continue
        for c in CAMPOS_SEGMENTO:
            if c not in datos:
                R.bloqueo("C01", f"{rs}.{c}", "Campo obligatorio ausente")
        if datos.get("estado_semaforo") is not None and datos.get("estado_semaforo") not in ENUMS["estado_semaforo"]:
            R.bloqueo("C01", f"{rs}.estado_semaforo", f"Valor no permitido {datos.get('estado_semaforo')!r}")
        opciones = datos.get("opciones") if isinstance(datos.get("opciones"), list) else []
        n = len(opciones)
        total_opciones += n
        # C02
        if n > maxn:
            R.bloqueo("C02", rs, f"{n} opciones (máximo {maxn})")
        rangos = [o.get("rango") for o in opciones if isinstance(o, dict)]
        if sorted(r for r in rangos if isinstance(r, int)) != list(range(1, n + 1)):
            R.bloqueo("C02", rs, f"Rangos {rangos} no son 1..{n} sin repeticiones")
        # C03
        if n < maxn and _vacio(datos.get("menos_de_tres_motivo")):
            R.bloqueo("C03", rs, f"{n} opción(es) sin «menos_de_tres_motivo»")
        cand = datos.get("candidatas_analizadas")
        if isinstance(cand, int) and cand < n:
            R.bloqueo("C01", f"{rs}.candidatas_analizadas", f"{cand} candidatas analizadas < {n} opciones")
        # C14 semáforo
        sem = datos.get("estado_semaforo")
        if sem == "VERDE" and n == 0:
            R.advertencia("C14", rs, "Semáforo VERDE sin opciones")
        if sem == "GRIS" and n > 0:
            R.advertencia("C14", rs, "Semáforo GRIS con opciones propuestas")
        # C02 / G3-FX-09 diversidad del segmento (9.6.3)
        clusters = [o.get("cluster") or o.get("cluster_id") for o in opciones if isinstance(o, dict)]
        for cl in sorted({c for c in clusters if c}):
            if clusters.count(cl) > p["max_por_cluster"]:
                R.bloqueo("C02", rs, f"{clusters.count(cl)} opciones del clúster «{cl}» (máximo {p['max_por_cluster']}, 9.6.3)")
        cuenta: Dict[tuple, int] = {}
        for o in opciones:
            if isinstance(o, dict):
                for e in ht03.exposiciones_de(o):
                    cuenta[(e["divisa"], e["lado"])] = cuenta.get((e["divisa"], e["lado"]), 0) + 1
        for (d, l), k in sorted(cuenta.items()):
            if k > p["max_divisa_misma_direccion"]:
                R.bloqueo("G3-FX-09", rs, f"{d} {l} en {k} opciones del segmento (máximo {p['max_divisa_misma_direccion']}, 9.6.3)")

        for i, op in enumerate(opciones):
            ro = f"{rs}.opciones[{i}]"
            if not isinstance(op, dict):
                R.bloqueo("C01", ro, "La opción debe ser un objeto")
                continue
            oid = op.get("opp_id") or f"#{i}"
            ro = f"{rs}.{oid}"
            if oid in ids_vistos:
                R.bloqueo("C01", ro, "opp_id duplicado en el paquete")
                if seg_de_opp.get(oid) and seg_de_opp[oid] != seg:
                    R.bloqueo("C16", ro, f"La misma oportunidad {oid} figura en {seg_de_opp[oid]} y en {seg}")
            ids_vistos.add(oid)
            seg_de_opp.setdefault(oid, seg)
            if op.get("segmento") is not None and op.get("segmento") != seg:
                R.bloqueo("C01", f"{ro}.segmento", f"segmento {op.get('segmento')!r} distinto del segmento {seg} en el que figura")
            if op.get("opp_id") and not re.match(r"^OPP-FX-\d{4}-\d{4,}$", str(op["opp_id"])):
                R.bloqueo("C01", ro, "opp_id no sigue el formato OPP-FX-AAAA-NNNN (Anexo C Forex)")
            for t in op.get("tnd_ids") or []:
                if isinstance(t, str) and not t.startswith("TND-FX-"):
                    R.bloqueo("C01", f"{ro}.tnd_ids", f"{t} no sigue el formato TND-FX-")
            for c in CAMPOS_OPCION_NO_VACIOS:
                if c not in op:
                    R.bloqueo("C01", f"{ro}.{c}", "Campo obligatorio ausente")
                elif _vacio(op[c]) and not isinstance(op[c], (int, float)):
                    R.bloqueo("C01", f"{ro}.{c}", "Campo obligatorio vacío")
            for c in CAMPOS_OPCION_PRESENTES:
                if c not in op:
                    R.bloqueo("C01", f"{ro}.{c}", "Campo obligatorio ausente (puede ser nulo o lista vacía)")
            for c in ("relevancia_decisional", "reversibilidad", "liquidez", "siguiente_paso_sugerido", "confianza"):
                if c in op and not _vacio(op[c]) and op[c] not in ENUMS[c]:
                    R.bloqueo("C01", f"{ro}.{c}", f"Valor no permitido {op[c]!r}")
            r15 = op.get("riesgo_1a5")
            if "riesgo_1a5" in op and (isinstance(r15, bool) or not isinstance(r15, int) or not 1 <= r15 <= 5):
                R.bloqueo("C01", f"{ro}.riesgo_1a5", f"Debe ser entero 1–5 ({r15!r})")
            if isinstance(op.get("catalizadores"), list) and not op["catalizadores"]:
                R.advertencia("C01", f"{ro}.catalizadores", "Sin catalizadores identificados")

            # C15 frontera con el Bloque B (2.4–2.5, R21)
            to = op.get("tipo_opcion")
            if not _vacio(to) and to not in TIPOS_OPCION:
                extra = f" ({TIPOS_OPCION_AJENOS[to]})" if to in TIPOS_OPCION_AJENOS else ""
                R.bloqueo("C15", f"{ro}.tipo_opcion", f"tipo_opcion {to!r} fuera de los tipos cambiarios "
                                                      f"{'/'.join(TIPOS_OPCION)}{extra}")
            amb = op.get("ambito")
            if not isinstance(amb, dict):
                R.bloqueo("C15", f"{ro}.ambito", "Sin delimitación del ámbito (incluye/excluye)")
            else:
                for k in ("incluye", "excluye"):
                    if _vacio(amb.get(k)):
                        R.bloqueo("C15", f"{ro}.ambito.{k}", "Delimitación del ámbito incompleta")
            ind = op.get("indicador_seguimiento")
            if not isinstance(ind, dict) or _vacio(ind.get("nombre")):
                R.bloqueo("C15", f"{ro}.indicador_seguimiento", "Sin indicador de seguimiento medible (PS3)")
            _frontera(R, ro, _textos_opcion(op), op)
            if "ejemplos_ilustrativos" in op:
                R.bloqueo("C15", f"{ro}.ejemplos_ilustrativos", "Campo del Bloque A general: en divisas la granularidad máxima es "
                                                                "el par o la cesta; no se citan productos")
            # G3-FX-01/02 notación, dirección y composición; G3-FX-05 carry; G3-FX-03 asignación de segmento
            neta = _composicion(R, ro, op, str(to or ""))
            _carry(R, ro, op, str(to or ""))
            esperado_seg = segmento_esperado(op)
            if esperado_seg and esperado_seg != seg:
                if _vacio(op.get("motivo_asignacion_segmento")):
                    R.bloqueo("G3-FX-03", f"{ro}.segmento", f"Las reglas 1–3 de 2.6 asignan {esperado_seg}, no {seg}, y no hay "
                                                             "`motivo_asignacion_segmento`")
                else:
                    R.advertencia("G3-FX-03", f"{ro}.segmento", f"Asignada a {seg} (las reglas darían {esperado_seg}) con motivo registrado")
            for d, v in neta.items():
                neta_global[d] = neta_global.get(d, 0.0) + v
            for d, l in patas_activas(op).items():
                if l in ("LARGO", "CORTO"):
                    lados_por_divisa.setdefault(d, {"LARGO": set(), "CORTO": set()})[l].add((seg, oid))
            # C16 claves de duplicado
            kn = normalizar_texto(op.get("nombre"))
            if kn:
                claves_dup.setdefault("nombre:" + kn, []).append((seg, oid))
            ka = clave_ambito(op)
            if ka:
                claves_dup.setdefault("ambito:" + ka, []).append((seg, oid))
            ke = clave_exposicion(op)
            if ke and op.get("tipo_opcion") != "VOLATILIDAD":
                claves_dup.setdefault("exposicion:" + ke, []).append((seg, oid))

            pu = op.get("puntuaciones") if isinstance(op.get("puntuaciones"), dict) else {}
            # C04 puntuaciones
            T, E, M, A, RK = (pu.get(k) for k in ("T", "E", "M", "A", "RK"))
            T_na = bool((isinstance(T, str) and T.upper() == "NA") or (T is None and op.get("tactica")))
            for k in ("E", "A", "M", "RK") + (() if T_na else ("T",)):
                v = pu.get(k)
                if isinstance(v, bool) or not isinstance(v, (int, float)) or not 0 <= v <= 100:
                    R.bloqueo("C04", f"{ro}.puntuaciones.{k}", f"Valor no válido {v!r}")
                elif k != "RK" and v % 5 != 0:
                    R.bloqueo("C04", f"{ro}.puntuaciones.{k}", f"{v} no es múltiplo de 5 (redondeo de HT-03)")
            if all(isinstance(x, (int, float)) for x in (E, A, RK)) and (T_na or isinstance(T, (int, float))):
                rk_calc, _ = ht03.calcular_rk(None if T_na else int(T), int(E), int(A), p["pesos_rk"])
                if rk_calc != RK:
                    R.bloqueo("C04", f"{ro}.puntuaciones.RK", f"RK declarado {RK} ≠ reconstruido {rk_calc}")
            entrada_ht03 = desgloses.get(oid) or (op.get("desglose") if isinstance(op.get("desglose"), dict) else None)
            if entrada_ht03:
                if "dimensiones" not in entrada_ht03:
                    entrada_ht03 = {"dimensiones": entrada_ht03}
                op_ht03 = {"opp_id": oid, "segmento": seg, **entrada_ht03}
                ev = ht03.evaluar_opcion(op_ht03, p)
                recalculadas[oid] = ev["puntuaciones"]
                if ev["errores"]:
                    R.bloqueo("C04", ro, "Desglose no calculable con HT-03: " + "; ".join(ev["errores"]))
                for k in ("T", "E", "M", "A", "RK"):
                    if k in ev["puntuaciones"] and k in pu and ev["puntuaciones"][k] != pu[k] \
                            and not (k == "T" and T_na and ev["puntuaciones"][k] == "NA"):
                        R.bloqueo("C04", f"{ro}.puntuaciones.{k}", f"Declarado {pu[k]} ≠ HT-03 {ev['puntuaciones'][k]}")
                for bm in ev["banda_marginal"]:
                    if not bm.get("resuelta"):
                        R.bloqueo("C05", ro, f"PS8: {bm['puntuacion']} en banda marginal sin segunda pasada independiente")
            else:
                R.advertencia("C04", ro, "Sin desglose de dimensiones: solo se ha reconstruido RK (aportar --desgloses)")

            # C05 elegibilidad y puertas
            if isinstance(E, (int, float)) and E < u["E"]:
                R.bloqueo("C05", ro, f"E={E} < {u['E']}")
            if T_na:
                if isinstance(A, (int, float)) and A < u["A_si_T_NA"]:
                    R.bloqueo("C05", ro, f"A={A} < {u['A_si_T_NA']} con T NA")
            else:
                if isinstance(A, (int, float)) and A < u["A"]:
                    R.bloqueo("C05", ro, f"A={A} < {u['A']}")
                if isinstance(T, (int, float)) and T < u["T"]:
                    R.bloqueo("C05", ro, f"T={T} < {u['T']}")
            for k, umbral in (("E", u["E"]), ("A", u["A_si_T_NA"] if T_na else u["A"]), ("T", None if T_na else u["T"])):
                v = pu.get(k)
                if umbral is not None and isinstance(v, (int, float)) and 0 <= v - umbral <= p["banda_marginal"] and not entrada_ht03:
                    R.advertencia("C05", ro, f"{k}={v} en banda marginal (≤ {p['banda_marginal']} sobre {umbral}): verificar segunda pasada (PS8)")
            puertas = op.get("puertas")
            if isinstance(puertas, dict):
                for g in p["puertas_obligatorias"]:
                    if g not in puertas:
                        R.bloqueo("C05", ro, f"Puerta {g} sin resultado")
                    elif puertas[g] is not True:
                        R.bloqueo("C05", ro, f"Puerta {g} no superada")
            else:
                R.advertencia("C05", ro, "El paquete no incluye el estado de las puertas G1–G4/PS1–PS8 de la opción")
            conv = op.get("convertibilidad")
            if isinstance(conv, dict):
                for k in ("convertible", "ndf", "controles_capitales"):
                    if not isinstance(conv.get(k), bool):
                        R.bloqueo("G3-FX-04", f"{ro}.convertibilidad.{k}", "Bloque `convertibilidad` incompleto: debe ser booleano")
                if conv.get("profundidad") not in ("muy alta", "alta", "media", "baja"):
                    R.bloqueo("G3-FX-04", f"{ro}.convertibilidad.profundidad", "Bloque `convertibilidad` incompleto: profundidad")
                if conv.get("convertible") is False and not (conv.get("ndf") is True or conv.get("exposicion_alternativa") is True):
                    R.bloqueo("G3-FX-04", f"{ro}.convertibilidad", "PS3: divisa no convertible sin exposición alternativa (NDF, futuros "
                                                             "o productos cotizados) para un inversor minorista europeo")
                if conv.get("impiden_exposicion") is True:
                    R.bloqueo("G3-FX-04", f"{ro}.convertibilidad", "PS3: controles de capitales que impiden la exposición o la repatriación")
                if _vacio(conv.get("nota")):
                    R.advertencia("G3-FX-04", f"{ro}.convertibilidad.nota", "PS3 sin nota que justifique la convertibilidad e invertibilidad")
            else:
                R.bloqueo("G3-FX-04", f"{ro}.convertibilidad", "Debe ser un objeto {convertible, ndf, controles_capitales, profundidad, nota}")

            # C17 naturaleza de la inversión y horizonte principal (8.3 V1.1)
            _horizonte_principal(R, ro, op, seg)
            # C06 / C07 horizontes
            ofrecidos = _horizontes_ofrecidos(op)
            if not ofrecidos:
                R.bloqueo("C06", ro, "Ningún horizonte con contenido")
            for h, hv in ofrecidos.items():
                rh = f"{ro}.horizontes.{h}"
                if h not in HORIZONTES:
                    R.bloqueo("C06", rh, "Horizonte desconocido")
                    continue
                regla = TABLA_HORIZONTES[seg][h]
                if regla == "NO":
                    R.bloqueo("C06", rh, f"{h} no aplicable a {seg} (tabla 8.3: «No»)")
                elif regla == "LIMITADO" and h == "H5":
                    pass   # H5: la limitación es el ámbito estructural y los hitos (C18), no un catalizador
                elif regla == "LIMITADO":
                    if not op.get("catalizadores"):
                        R.bloqueo("C06", rh, f"{h} «limitado» en {seg}: exige un catalizador identificado (8.3)")
                    elif str(op.get("liquidez", "")).lower() == "baja":
                        R.bloqueo("C06", rh, f"{h} «limitado» en {seg}: exige liquidez suficiente (liquidez baja declarada)")
                    else:
                        R.advertencia("C06", rh, f"{h} «limitado» en {seg}: confirmar liquidez suficiente y catalizador fechado")
                pid = hv.get("prg_id")
                if _vacio(pid) or not str(pid).startswith("PRG-"):
                    R.bloqueo("C06", rh, "Horizonte sin pronóstico PRG- congelado (9.6.7, R11)")
                elif not str(pid).startswith("PRG-FX-"):
                    R.bloqueo("C01", rh, f"{pid} no sigue el formato PRG-FX- (Anexo C Forex)")
                if h == "H1" and _vacio(hv.get("advertencia")):
                    R.advertencia("C06", rh, "H1 debe presentarse con la advertencia de menor fiabilidad (8.3)")
                prob = hv.get("prob")
                if h == "H5":
                    _h5(R, rh, hv, op, paquete.get("fecha"))
                if prob is not None and h == "H5":
                    pass   # C18 ya bloquea: en H5 la probabilidad es siempre cualitativa
                elif prob is not None:
                    if isinstance(prob, bool) or not isinstance(prob, (int, float)) or not 0 <= prob <= 1:
                        R.bloqueo("C07", rh, f"Probabilidad no válida {prob!r} (0–1)")
                    cert = [c for c in certificados if (c.get("segmento") or c.get("clase")) == seg and c.get("horizonte") == h
                            and c.get("vigente", True) and (not c.get("metodo") or not hv.get("metodo")
                                                             or c.get("metodo") == hv.get("metodo"))]
                    if not cert:
                        R.bloqueo("C07", rh, f"Probabilidad numérica sin certificado vigente para {seg}×{h} (R13)")
                else:
                    banda = str(hv.get("banda") or "").strip().lower()
                    if banda not in BANDAS_CUALITATIVAS:
                        R.advertencia("C07", rh, f"Banda «{hv.get('banda')}» fuera del vocabulario {BANDAS_CUALITATIVAS}")
                # G3-FX-11 tipo de rentabilidad y divisa de medición; G3-FX-06 referencias ingenuas (8.4)
                tr = hv.get("tipo_rentabilidad")
                validos_tr = TIPOS_RENTABILIDAD + ((TIPO_RENTABILIDAD_VOLATILIDAD,) if to == "VOLATILIDAD" else ())
                if tr not in validos_tr:
                    R.bloqueo("G3-FX-11", rh, f"PRG sin `tipo_rentabilidad` válido ({'/'.join(validos_tr)}): {tr!r}")
                dm = hv.get("divisa_medicion")
                if _vacio(dm) or dm not in ISO_4217:
                    R.bloqueo("G3-FX-11", rh, f"PRG sin divisa de medición ISO 4217 ({dm!r})")
                ref = str(hv.get("referencia") or "").lower()
                if seg == "ESTR" and to in TIPOS_CESTA:
                    if not any(k in ref for k in ("rentabilidad nula", "índice de la estrategia", "indice de la estrategia")):
                        R.advertencia("G3-FX-06", rh, "PRG de estrategia sin rentabilidad nula o índice de la estrategia como referencia (8.4)")
                elif "paseo aleatorio" not in ref:
                    R.advertencia("G3-FX-06", rh, "PRG sin el paseo aleatorio como referencia ingenua (Meese-Rogoff, 8.4)")
                if tr == "RENTABILIDAD_TOTAL" and "forward" not in ref and not (seg == "ESTR" and to in TIPOS_CESTA):
                    R.advertencia("G3-FX-06", rh, "PRG de rentabilidad total sin el forward como referencia (8.4)")

            # C08 evidencias y cálculos
            ev_list = op.get("evidencias") if isinstance(op.get("evidencias"), list) else []
            ca_list = op.get("calculos") if isinstance(op.get("calculos"), list) else []
            if not ev_list or any(_vacio(x) for x in ev_list):
                R.bloqueo("C08", f"{ro}.evidencias", "Sin evidencias referenciadas (R7)")
            if not ca_list or any(_vacio(x) for x in ca_list):
                R.bloqueo("C08", f"{ro}.calculos", "Sin cálculos referenciados (R7)")
            for x in ev_list:
                if isinstance(x, str) and not re.match(r"^(CLM|EVD)-FX-", x):
                    R.bloqueo("C01", f"{ro}.evidencias", f"Identificador «{x}» no es CLM-FX-/EVD-FX- (Anexo C Forex)")
                if trazas is not None and isinstance(x, str) and x.startswith("CLM-") and not trazas.get(x):
                    R.bloqueo("C08", f"{ro}.evidencias", f"{x} sin EVD vinculada en F2")
            for x in ca_list:
                if isinstance(x, str) and not re.match(r"^CALC-FX-", x):
                    R.bloqueo("C01", f"{ro}.calculos", f"Identificador «{x}» no es CALC-FX- (Anexo C Forex)")
                if artefactos is not None and x not in artefactos:
                    R.bloqueo("C08", f"{ro}.calculos", f"{x} sin artefacto en el Registro de cálculos")
            if trazas is None:
                R.extra.setdefault("C08", {"trazas_clm_evd": "no comprobadas (sin extracto de F2)"})

            # C09 objeciones
            objs = op.get("objeciones") if isinstance(op.get("objeciones"), list) else []
            if not objs:
                R.advertencia("C09", ro, "Sin objeciones registradas (aceptable solo en N1 con pre-mortem)")
            for j, ob in enumerate(objs):
                if not isinstance(ob, dict):
                    continue
                fz = str(ob.get("fuerza", "")).lower()
                if fz and fz not in ENUMS["fuerza"]:
                    R.advertencia("C09", f"{ro}.objeciones[{j}]", f"Fuerza «{fz}» no reconocida")
                resuelta = ob.get("resuelta")
                sin_resp = _vacio(ob.get("respuesta"))
                if fz == "fuerte" and (resuelta is False or (resuelta is None and sin_resp)):
                    R.bloqueo("C09", f"{ro}.objeciones[{j}]", "Objeción fuerte sin resolver")
                elif fz == "moderada" and sin_resp:
                    R.bloqueo("C09", f"{ro}.objeciones[{j}]", "Objeción moderada sin respuesta del Analista (G2)")

            # C10 relevancia decisional y riesgo mínimo
            vig = _es_vigente(op, vigentes)
            disparadores = relevancia_esperada_alta(op, seg, vig, p)
            rel = op.get("relevancia_decisional")
            if disparadores and rel != "ALTA":
                R.bloqueo("C10", ro, f"Relevancia «{rel}» pero la regla exige ALTA: {', '.join(disparadores)}")
            elif not disparadores and rel == "ALTA":
                R.advertencia("C10", ro, "ALTA sin disparador del Anexo A (sobrestimación conservadora)")
            elif rel == "BAJA" and not vig:
                R.advertencia("C10", ro, "BAJA en una opción nueva (BAJA se reserva a vigentes sin cambio material)")
            motivo_r = riesgo_minimo(op)
            if motivo_r and isinstance(r15, int) and r15 < 4:
                R.bloqueo("G3-FX-04", f"{ro}.riesgo_1a5", f"Riesgo {r15}/5 por debajo del mínimo 4 ({motivo_r}; nota 2 del Anexo A)")

            # C11 paquete para el Bloque B
            b = bloque_b.get(oid)
            if op.get("siguiente_paso_sugerido") == "ENVIAR_A_BLOQUE_B" and not b:
                R.bloqueo("C11", ro, "ENVIAR_A_BLOQUE_B sin encargo en paquete_para_bloque_B")
            if b:
                rb = f"paquete_para_bloque_B.{oid}"
                for c in CAMPOS_BLOQUE_B:
                    if c not in b:
                        R.bloqueo("C11", f"{rb}.{c}", "Campo ausente")
                    elif c not in CAMPOS_BLOQUE_B_PUEDEN_VACIOS and _vacio(b[c]):
                        R.bloqueo("C11", f"{rb}.{c}", "Campo vacío")
                if b.get("segmento") and b["segmento"] != seg:
                    R.bloqueo("C11", f"{rb}.segmento", f"{b['segmento']} distinto del segmento de la opción ({seg})")
                if b.get("horizonte_principal") and op.get("horizonte_principal") and b["horizonte_principal"] != op["horizonte_principal"]:
                    R.bloqueo("C11", f"{rb}.horizonte_principal", f"{b['horizonte_principal']} distinto del horizonte principal de la "
                                                                  f"opción ({op['horizonte_principal']})")
                for c in ("par", "direccion", "divisa_financiacion", "tipo_opcion", "vista_volatilidad"):
                    if c in b and b.get(c) != op.get(c):
                        R.bloqueo("C11", f"{rb}.{c}", f"{b.get(c)!r} distinto del de la opción ({op.get(c)!r})")
                hb = b.get("horizontes") if isinstance(b.get("horizontes"), list) else []
                for h in hb:
                    if h not in ofrecidos:
                        R.advertencia("C11", f"{rb}.horizontes", f"{h} no figura entre los horizontes de la opción")
                prg_op = {str(v.get("prg_id")) for v in ofrecidos.values()}
                for x in (b.get("pronosticos") if isinstance(b.get("pronosticos"), list) else []):
                    if x not in prg_op:
                        R.advertencia("C11", f"{rb}.pronosticos", f"{x} no es un pronóstico de la opción")
                for c in ("ambito", "indicador_seguimiento", "composicion"):
                    if isinstance(b.get(c), (dict, list)) and isinstance(op.get(c), (dict, list)) and b[c] != op[c]:
                        R.advertencia("C11", f"{rb}.{c}", "Distinto del de la opción: el encargo debe transportar el mismo ámbito")
                ce, co = b.get("carry_esperado"), op.get("carry")
                if isinstance(ce, dict) and isinstance(co, dict) and (ce.get("signo") != co.get("signo")
                                                                      or ce.get("anual_pct") != co.get("anual_pct")):
                    R.advertencia("C11", f"{rb}.carry_esperado", "Carry esperado distinto del de la opción")
                # Las preguntas para el Bloque B pueden mencionar instrumentos (son preguntas, no propuestas); las
                # consideraciones de implementación son información y no pueden recomendar un instrumento (2.5)
                # G3-FX-07 anticipación en fijaciones: niveles conocibles en la fecha, con fuente, hora y zona
                lim = str(paquete.get("fecha_datos_mercado") or paquete.get("fecha") or "9999-12-31")
                for k, nv in (b.get("niveles_referencia") or {}).items() if isinstance(b.get("niveles_referencia"), dict) else []:
                    rn = f"{rb}.niveles_referencia.{k}"
                    if not isinstance(nv, dict):
                        continue
                    for campo in ("fecha_dato", "conocible_desde"):
                        if isinstance(nv.get(campo), str) and nv[campo][:10] > lim:
                            R.bloqueo("G3-FX-07", rn, f"{campo} {nv[campo]} posterior a la congelación ({lim}): anticipación")
                    if _vacio(nv.get("fuente")) or _vacio(nv.get("hora_fijacion")) or not re.search(r"\b\d{1,2}:\d{2}\b", str(nv.get("hora_fijacion") or "")) \
                            or "/" not in str(nv.get("hora_fijacion") or ""):
                        R.bloqueo("G3-FX-07", rn, "Fijación sin fuente, hora y zona (p. ej., «16:00 Europe/London»)")
                _frontera(R, rb, [x for x in (b.get("consideraciones_implementacion") or []) if isinstance(x, str)]
                          + [x for x in (b.get("tesis"), b.get("nombre")) if isinstance(x, str)], b)

    # C16 oportunidad duplicada en dos segmentos (regla 4 de 2.6): nombre, ámbito o exposición
    for clave, lst in claves_dup.items():
        segs = sorted({t for t, _ in lst})
        ids = sorted({o for _, o in lst})
        if len(ids) < 2:
            continue
        criterio = {"nombre": "nombre", "ambito": "ámbito", "exposicion": "exposición (par y dirección o composición)"}[clave.split(":", 1)[0]]
        if len(segs) > 1:
            R.bloqueo("C16", f"segmentos.{'/'.join(segs)}",
                      f"Oportunidad duplicada en dos segmentos por {criterio} «{clave.split(':', 1)[1]}»: {', '.join(ids)}")
        else:
            R.advertencia("C16", f"segmentos.{segs[0]}", f"Dos opciones del mismo segmento con {criterio} idéntico: {', '.join(ids)}")
    for oid in bloque_b:
        if oid not in ids_vistos:
            R.bloqueo("C11", f"paquete_para_bloque_B.{oid}", "Entrada para una opción que no está en el paquete")

    # G3-FX-10 capas transversales: referencia a los informes CT-06T (TRV-FX-) del ciclo o declaración de su ausencia
    it = paquete.get("informes_transversales")
    ids_trv = [v for k, v in (it.items() if isinstance(it, dict) else []) if k in ("BCM", "PFV") and isinstance(v, str)]
    if not (len(ids_trv) == 2 and all(v.startswith("TRV-FX-") for v in ids_trv)) and _vacio((it or {}).get("nota") if isinstance(it, dict) else None):
        R.advertencia("G3-FX-10", "informes_transversales", "Sin referencia a los informes CT-06T del ciclo (TRV-FX- de AG-09 y AG-21) "
                                                            "ni declaración de su ausencia o reutilización")

    # C14 apuestas independientes
    ai = paquete.get("apuestas_independientes")
    if ai is not None:
        if not isinstance(ai, int) or ai < 0:
            R.bloqueo("C01", "apuestas_independientes", f"Valor no válido {ai!r}")
        elif ai > total_opciones:
            R.advertencia("C14", "apuestas_independientes", f"{ai} apuestas independientes > {total_opciones} opciones")
        elif total_opciones > 0 and ai == 0:
            R.advertencia("C14", "apuestas_independientes", "0 apuestas independientes con opciones propuestas")

    # G3-FX-08 exposición agregada por divisa (14.1, 9.6.6) y contradicciones entre segmentos
    expo = paquete.get("exposicion_agregada")
    if not isinstance(expo, dict) or not expo:
        if total_opciones:
            R.bloqueo("G3-FX-08", "exposicion_agregada", "Exposición agregada por divisa ausente (14.1; reconstruible desde las composiciones)")
    if "exposicion_agregada" in paquete:
        if not isinstance(expo, dict):
            R.bloqueo("C01", "exposicion_agregada", "Debe ser un objeto {DIVISA: larga|corta [moderada|fuerte]|neutra}")
            expo = {}
        for d, v in expo.items():
            if d not in ISO_4217:
                R.bloqueo("G3-FX-08", f"exposicion_agregada.{d}", f"{d} no es un código ISO 4217")
            if not isinstance(v, str) or not RE_EXPOSICION.match(v):
                R.bloqueo("G3-FX-08", f"exposicion_agregada.{d}", f"Valor {v!r} no permitido (larga|corta [moderada|fuerte] o neutra)")
                continue
            neta = neta_global.get(d, 0.0)
            signo = 1 if neta > 1e-9 else (-1 if neta < -1e-9 else 0)
            declarado = 1 if v.startswith("larga") else (-1 if v.startswith("corta") else 0)
            if signo and declarado and signo != declarado:
                R.bloqueo("G3-FX-08", f"exposicion_agregada.{d}", f"Declarada «{v}» pero las opciones suman una exposición neta "
                                                             f"{'larga' if signo > 0 else 'corta'} ({neta:+.2f})")
            elif signo != declarado:
                R.advertencia("G3-FX-08", f"exposicion_agregada.{d}", f"Declarada «{v}» con exposición neta de las opciones {neta:+.2f}")
        for d, v in sorted(neta_global.items()):
            if abs(v) >= 1 - 1e-9 and d not in expo:
                R.advertencia("G3-FX-08", "exposicion_agregada", f"{d} con exposición neta {v:+.2f} no declarada")
        R.extra["G3-FX-08"] = {"exposicion_neta_calculada": {d: round(v, 4) for d, v in sorted(neta_global.items()) if abs(v) > 1e-9}}
    justificadas = {str(c.get("divisa")) for c in (paquete.get("contradicciones_entre_segmentos") or [])
                    if isinstance(c, dict) and not _vacio(c.get("justificacion_contradiccion"))}
    for d, lados in sorted(lados_por_divisa.items()):
        segs_l = {sg for sg, _ in lados["LARGO"]}
        segs_c = {sg for sg, _ in lados["CORTO"]}
        if d not in justificadas and any(a != b for a in segs_l for b in segs_c):
            R.bloqueo("G3-FX-08", f"divisa.{d}", f"{d} como pata activa larga en {sorted(segs_l)} y corta en {sorted(segs_c)} "
                                                 f"({', '.join(sorted(o for _, o in lados['LARGO'] | lados['CORTO']))}) sin "
                                                 "`justificacion_contradiccion` en «contradicciones_entre_segmentos» ni resolución (9.6.6)")

    # C12 legibilidad
    if informe_visual:
        try:
            with open(informe_visual, encoding="utf-8", errors="replace") as fh:
                contenido = fh.read()
            leg = ht07.analizar(contenido, es_html=informe_visual.lower().endswith((".html", ".htm")) or None,
                                umbral_fh=umbral_fh)
            R.extra["C12"] = {k: leg[k] for k in ("fernandez_huerta", "interpretacion", "palabras", "frases",
                                                  "longitud_media_frase", "pct_frases_mas_de_20", "jerga_sin_explicar")}
            if leg["fernandez_huerta"] is None or leg["fernandez_huerta"] < umbral_fh:
                R.bloqueo("C12", informe_visual, f"Fernández-Huerta {leg['fernandez_huerta']} < {umbral_fh}")
            if leg["frases_largas"]:
                R.advertencia("C12", informe_visual, f"{len(leg['frases_largas'])} frase(s) de más de 20 palabras")
            if leg["jerga_sin_explicar"]:
                R.advertencia("C12", informe_visual, "Jerga sin explicar la primera vez: " + ", ".join(leg["jerga_sin_explicar"][:10]))
        except OSError as e:
            R.bloqueo("C12", informe_visual, f"No se puede leer el informe visual: {e}")
    else:
        R.advertencia("C12", "(informe visual)", "Legibilidad no comprobada: no se ha facilitado la ruta del informe")

    comps = R.comprobaciones()
    bloqueos = [c for c in comps if c["resultado"] == "BLOQUEO"]
    advert = [c for c in comps if c["resultado"] == "ADVERTENCIA"]
    dictamen = "BLOQUEADO" if bloqueos else ("APTO_CON_ADVERTENCIAS" if advert else "APTO")
    motivo = ("; ".join(f"{c['id']} {c['nombre']}" for c in bloqueos) if bloqueos else
              ("; ".join(f"{c['id']} {c['nombre']}" for c in advert) if advert else "Todas las comprobaciones superadas"))
    return {"herramienta": "HT-09", "version": VERSION, "run_id": paquete.get("run_id"), "dictamen": dictamen,
            "motivo": motivo,
            "resumen": {"ok": len(comps) - len(bloqueos) - len(advert), "advertencias": len(advert), "bloqueos": len(bloqueos),
                        "opciones": total_opciones},
            "comprobaciones": comps, "puntuaciones_recalculadas": recalculadas}


def _cargar(ruta: Optional[str]):
    if not ruta:
        return None
    with open(ruta, encoding="utf-8") as fh:
        return json.load(fh)


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="HT-09 · Validador determinista G3 del paquete_oportunidades Forex")
    ap.add_argument("paquete", help="JSON del paquete_oportunidades (o paquete_sintesis)")
    ap.add_argument("--certificados", help="JSON: lista de certificados de horizonte [{segmento, horizonte, vigente, metodo?}]")
    ap.add_argument("--informe-visual", help="Ruta del informe visual (HTML o texto) para HT-07")
    ap.add_argument("--desgloses", help="JSON {opp_id: entrada HT-03 (dimensiones, segunda_pasada, saturacion_narrativa)}")
    ap.add_argument("--parametros", help="JSON con parámetros vigentes de F10 (formato de HT-03)")
    ap.add_argument("--trazas", help="JSON {CLM-…: [EVD-…]} extraído de F2")
    ap.add_argument("--artefactos", help="JSON: lista de CALC- presentes en el Registro de cálculos")
    ap.add_argument("--umbral-fh", type=float, default=70.0)
    ap.add_argument("--salida", help="JSON de salida (por defecto, stdout)")
    ap.add_argument("--seguimiento", action="store_true",
                    help="El JSON es un informe_seguimiento_opcion (ciclo C6); --informe-visual da el informe breve")
    a = ap.parse_args(argv)
    if a.seguimiento:
        try:
            inf = _cargar(a.paquete)
            txt = open(a.informe_visual, encoding="utf-8").read() if a.informe_visual else None
            res = validar_seguimiento(inf, texto=txt)
        except (OSError, json.JSONDecodeError, AttributeError, TypeError) as e:
            print(json.dumps({"herramienta": "HT-09", "dictamen": "BLOQUEADO", "error": str(e)}, ensure_ascii=False), file=sys.stderr)
            return 3
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return {"APTO": 0, "APTO_CON_ADVERTENCIAS": 1, "BLOQUEADO": 2}[res["dictamen"]]
    try:
        paquete = _cargar(a.paquete)
        certs = _cargar(a.certificados) or []
        if isinstance(certs, dict):
            certs = certs.get("certificados", [])
        res = validar(paquete, certs, a.informe_visual, _cargar(a.desgloses), _cargar(a.parametros),
                      _cargar(a.trazas), _cargar(a.artefactos), a.umbral_fh)
    except (OSError, json.JSONDecodeError, AttributeError, TypeError) as e:
        print(json.dumps({"herramienta": "HT-09", "dictamen": "BLOQUEADO", "error": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 3
    texto = json.dumps(res, ensure_ascii=False, indent=2)
    if a.salida:
        with open(a.salida, "w", encoding="utf-8") as fh:
            fh.write(texto + "\n")
    else:
        print(texto)
    return {"APTO": 0, "APTO_CON_ADVERTENCIAS": 1, "BLOQUEADO": 2}[res["dictamen"]]


if __name__ == "__main__":
    sys.exit(main())
