"""Contratos CT-01 a CT-25 (sección 6 y Anexo B del Documento 0 óptima V5.1; CT-23 a CT-25 añadidos en V5.1).

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

import contextlib
import copy
import hashlib
import json
import re
import sqlite3
import threading
from contextlib import closing
from datetime import date
from typing import Any

VERSION_CONTRATO = "5.1"
ESTADOS = ("COMPLETO", "PARCIAL", "SIN_RESULTADO", "RECHAZADO")
# §6.2.6: normalizar el cuerpo del Anexo B antiguo al crear el sobre.
CAMPO_ESTADO = {"CT-23": "estado_consulta", "CT-24": "estado_seguimiento", "CT-25": "estado_credencial"}
ESTADOS_ESPECIFICOS = {"CT-23": ("RESPONDIDA", "PARCIAL", "VENCIDA", "RECIBIDA"),
                       "CT-24": ("ACTIVO", "PAUSADO", "CANCELADO", "FINALIZADO"),
                       "CT-25": ("PROVISTA", "DENEGADA", "APLAZADA")}
# Analistas de tipo de activo (Documento 0 óptima V5.0, 4.2): AG-03..AG-09 y AG-21..AG-25
ANALISTAS = {"AG-03", "AG-04", "AG-05", "AG-06", "AG-07", "AG-08", "AG-09", "AG-21", "AG-22", "AG-23", "AG-24", "AG-25"}
TODOS = {f"AG-{i:02d}" for i in range(1, 26)}
AGENTE_CLASE = {"RV": "AG-03", "RF": "AG-04", "DIV": "AG-05", "MP": "AG-06", "IDX": "AG-21", "FON": "AG-22", "DER": "AG-23",
                "INM": "AG-07", "CRI": "AG-08", "ALT": "AG-09", "MON": "AG-24", "TCV": "AG-25"}
CLASE_AGENTE = {v: k for k, v in AGENTE_CLASE.items()}

# Canales: contrato -> lista de (emisores, receptores); «↔» se modela con ambas direcciones.
def _par(a, b):
    return [(set(a), set(b)), (set(b), set(a))]


CANALES: dict[str, list[tuple[set, set]]] = {
    "CT-01": [({"BROKER"}, {"AG-01"})],
    "CT-02": [({"AG-01"}, {"BROKER"})],
    "CT-03": _par({"BROKER"}, {"AG-01"}),
    "CT-04": [({"BROKER"}, {"AG-01"})],
    "CT-05": _par({"AG-01"}, {"AG-02"}),
    "CT-06": _par({"AG-02"}, ANALISTAS),
    "CT-07": _par({"AG-02", "AG-10"} | ANALISTAS, {"AG-16"}),
    "CT-08": _par({"AG-02", "AG-10", "AG-11"} | ANALISTAS, {"AG-14"}),
    "CT-09": _par({"AG-02", "AG-10", "AG-20", "AG-18", "AG-19", "AG-14", "AG-15", "AG-16"} | ANALISTAS, {"AG-13"}),
    "CT-10": _par({"AG-18", "AG-19", "AG-20"}, {"AG-13"}),
    "CT-11": _par(ANALISTAS | {"AG-16", "AG-14", "AG-15", "AG-10", "AG-11"}, {"AG-12"}),
    "CT-12": _par({"AG-02"}, {"AG-10"}),
    "CT-13": _par({"AG-02"}, {"AG-11"}),
    "CT-14": _par({"AG-02"}, {"AG-18"}),
    "CT-15": _par({"AG-02"}, {"AG-17"}),
    "CT-16": [({"AG-01"}, {"AG-18"})],
    "CT-17": _par({"AG-18"}, {"AG-19"}),
    "CT-18": [({"AG-18"}, TODOS)],
    "CT-19": [({"AG-20"}, {"AG-01", "AG-02", "AG-10", "AG-16", "AG-18"} | ANALISTAS)],
    "CT-20": _par({"AG-13"}, {"AG-15"}),
    "CT-21": [({"AG-14", "AG-15", "AG-16"}, {"AG-18"})],
    "CT-22": [({"AG-01"}, {"AG-20"})],
    # V5.1: consulta al Broker (en ambos sentidos), encargo de seguimiento de opción y credenciales
    "CT-23": _par({"AG-01"}, {"BROKER"}),
    "CT-24": _par({"BROKER"}, {"AG-01"}),
    "CT-25": _par({"AG-01"}, {"BROKER"}),
}

CAMPOS_MINIMOS = {
    "CT-01": ["tipo", "alcance", "horizontes", "prioridad"],
    "CT-02": ["entregables", "resumen", "estado_g3"],
    "CT-03": ["pregunta"],
    "CT-05": ["tipo", "alcance", "nivel_por_clase", "presupuesto_por_clase", "memoria", "delta_gc0", "fecha_objetivo"],
    "CT-06": ["clase", "fase", "nivel", "opciones_vigentes", "lecciones"],
    "CT-07": ["pregunta", "objetivo", "clase", "horizonte", "profundidad", "max_fuentes", "fecha_limite_informacion"],
    "CT-08": ["pregunta", "objetivo", "clase", "horizonte", "profundidad", "max_fuentes", "fecha_limite_informacion"],
    "CT-09": ["operacion", "perfil", "modo", "plan", "datos", "parametros", "semilla", "fecha_corte"],
    "CT-10": ["artefacto_id", "motivo"],
    "CT-11": ["piezas"],
    "CT-12": ["encargos"],
    "CT-13": ["peticiones"],
    "CT-14": ["paquete_sintesis"],
    "CT-15": ["paquete_sintesis"],
    "CT-23": ["cns_id", "sentido", "tipo", "modo"],
    "CT-24": ["accion"],
    "CT-25": ["crd_id", "servicio", "uso_previsto", "solicitante", "impacto_si_falta"],
}
CAMPOS_RETORNO = {"CT-03": ["clase_consulta", "ruta", "respuesta", "referencias", "confianza"],
                  "CT-23": ["cns_id", "estado"], "CT-24": ["seg_id", "estado"], "CT-25": ["crd_id", "estado"]}

RE_SECRETO = re.compile(
    r"(?i)(\"(api[_-]?key|apikey|secret|client_secret|password|passwd|contraseña|access[_-]?token|bearer)\"\s*:\s*\"[^\"]+\")"
    r"|(AKIA[0-9A-Z]{16})|(-----BEGIN [A-Z ]*PRIVATE KEY-----)|(Bearer\s+[A-Za-z0-9._-]{20,})"
    # T-120: el IBAN español se escribe casi siempre en grupos de cuatro; también se detecta con un espacio, un punto o un
    # guion entre grupos (antes, solo todo junto). T-122 (QA r01 de T-120, H-01): con cualquier espacio Unicode (el duro de
    # un IBAN copiado de una web o un PDF), hasta dos separadores seguidos y en cualquier agrupación (la impresa
    # «ES91 2100 0418 45 0200051332») y también en minúsculas: ES, dos cifras de control y 20 cifras
    r"|(?-i:(\b[Ee][Ss]\d{2}(?:[\s.\-]{0,2}\d){20}\b)|(\b\d{8}-?[A-HJ-NP-TV-Z]\b))")

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


def sanear_contenido_externo(texto: str, origen: str = "") -> tuple[str, list[dict]]:
    """Neutraliza instrucciones incrustadas (R9). Devuelve el texto saneado y los hallazgos."""
    if not isinstance(texto, str) or not texto:
        return texto, []
    hallazgos = []
    def _sust(m):
        hallazgos.append({"origen": origen, "fragmento": m.group(0)[:80], "tipo": "INSTRUCCION_INCRUSTADA"})
        return MARCA_RETIRADA
    limpio = RE_INYECCION.sub(_sust, texto)
    return limpio, hallazgos


def sanear_estructura(obj: Any, origen: str = "") -> tuple[Any, list[dict]]:
    """Aplica `sanear_contenido_externo` a todas las cadenas de una estructura JSON."""
    hallazgos: list[dict] = []
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


# T-92 (QA r01, H-07; QA r02, H-17; QA r03, H-25, H-26 y H-28): las claves «sk-» se buscan en dos pasos. El candidato es
# lineal: «sk-» (en mayúsculas o minúsculas) que no está dentro de una palabra (sin letra ni cifra pegada delante; «/», «-»,
# «.», «_» o un espacio sí valen) y 20 caracteres o más de [A-Za-z0-9_-]. Después `_es_clave_sk` lo descarta solo si tiene
# forma de texto corriente: tramos separados por «-» o «_» que son palabras (minúsculas, con mayúscula inicial o siglas) de
# hasta 15 letras o números de hasta 4 cifras («risk-…» queda fuera por el límite; «sk-hynix-posts-record-…»,
# «sk-hynix_annual_report_2023» o «SK-Hynix-Q3-results» son texto). Todo lo demás cuenta como clave.
RE_CANDIDATO_SK = re.compile(r"(?i)(?<![A-Za-z0-9])sk-([A-Za-z0-9_-]{20,})")
PREFIJOS_SK = ("ant-", "proj-", "svcacct-", "admin-", "lf-")
# tramos de texto: palabras, siglas, años y códigos de periodo de los informes («Q4», «FY2023», «3Q24», «2024Q4», «H1»).
# T-93 (QA r04 de T-92, H-33): también como van en las URL de prensa financiera: códigos de periodo en minúsculas («q2»,
# «fy2023», «1q24», «2024q4»), productos («5g», «hbm3e», «ddr5»), códigos de cotización de 5 a 7 cifras («000660»), siglas
# de hasta 15 letras («QUARTERLY») y CamelCase («HynixEarnings»). Las fechas de 8 cifras se aceptan si son una fecha válida.
RE_TRAMO_TEXTO = re.compile(r"[a-z]{1,15}|[A-Z][a-z]{0,14}|[A-Z]{1,15}|[0-9]{1,4}|[A-Z]{1,3}[0-9]{1,4}|[0-9][A-Z][0-9]{1,2}"
                            r"|[0-9]{4}[A-Z][0-9]{1,2}"
                            r"|[a-z]{1,2}[0-9]{1,4}|[0-9][a-z][0-9]{0,2}|[0-9]{4}[a-z][0-9]{1,2}|[a-z]{2,4}[0-9][a-z]?|[0-9]{5,7}"
                            r"|(?:[A-Z][a-z]{1,14}){2,4}")
RE_FECHA_8 = re.compile(r"(19|20)[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])")


def _tramo_texto(t: str) -> bool:
    if RE_TRAMO_TEXTO.fullmatch(t):
        return len(t) <= 30
    if RE_FECHA_8.fullmatch(t):   # T-93 (H-33): una fecha AAAAMMDD que existe
        try:
            date(int(t[:4]), int(t[4:6]), int(t[6:]))
            return True
        except ValueError:
            return False
    return False


def _es_clave_sk(cola: str) -> bool:
    """`cola` es lo que sigue a «sk-». Clave salvo que tenga forma de texto corriente (ver arriba)."""
    if cola.lower().startswith(PREFIJOS_SK):
        return True
    tramos = [t for t in re.split(r"[-_]", cola) if t]
    if len(tramos) >= 3 and all(t.isdigit() for t in tramos):
        # T-103 (QA r01 de T-93, H-41; QA r01 de T-103, H-50): una cola de tres o más tramos de solo cifras (20 caracteres o
        # más) no es texto corriente: los titulares de prensa llevan siempre un tramo de letras
        return True
    return len(tramos) < 2 or not all(_tramo_texto(t) for t in tramos)


# T-93 (H-32): escapes que, delante de una clave, la pegarían a una cifra o una letra y la ocultarían. T-103 (QA r01 de T-93,
# H-40): el tramo de barras se toma entero (un escape doble, como el de un JSON dentro de otro JSON, o una barra literal de
# una ruta), porque consumir solo la barra escapada dejaba la «n» pegada a la clave. También los escapes largos de `ascii()`,
# los octales, el «%uXXXX» de JavaScript y los «%25…» de una URL codificada dos veces
# T-103 r02 (QA r01, H-47): el tramo de barras empieza donde empieza (sin barra delante) y se toma de una vez (posesivo); sin
# eso, un texto con miles de barras seguidas costaba un tiempo cuadrático
RE_ESCAPES = re.compile(r"(?<!\\)\\++(?:u[0-9a-fA-F]{4}|U[0-9a-fA-F]{8}|x[0-9a-fA-F]{2}|[0-7]{1,3}|[ntrbf/\"])"
                        r"|%(?:25)*(?:u[0-9A-Fa-f]{4}|[0-9A-Fa-f]{2})")


# T-123 · R8: IBAN de otros países y números de tarjeta. Un patrón solo daría falsos positivos con cualquier serie de cifras,
# así que el candidato se valida con su dígito de control: el IBAN con el módulo 97 (ISO 13616) y la longitud de su país, y
# la tarjeta con el algoritmo de Luhn, la longitud y el prefijo de su red. Longitudes del registro de IBAN de SWIFT (ISO
# 13616) para los países de la zona SEPA y algunos más; un país que no está en la tabla no se reconoce (límite declarado
# en INC-T123-01). El IBAN español tiene además su patrón propio en `RE_SECRETO`, sin el control (más estricto).
LONGITUD_IBAN = {"AD": 24, "AE": 23, "AT": 20, "BE": 16, "BG": 22, "BR": 29, "CH": 21, "CY": 28, "CZ": 24, "DE": 22, "DK": 18,
                 "EE": 20, "ES": 24, "FI": 18, "FR": 27, "GB": 22, "GI": 23, "GR": 27, "HR": 21, "HU": 28, "IE": 22, "IL": 23,
                 "IS": 26, "IT": 27, "LI": 21, "LT": 20, "LU": 20, "LV": 21, "MC": 27, "MT": 31, "NL": 18, "NO": 15, "PL": 28,
                 "PT": 25, "RO": 24, "SA": 24, "SE": 24, "SI": 19, "SK": 24, "SM": 27, "TR": 26, "VA": 22}
# T-123 r02 (QA r01, H-01): el candidato es una serie de grupos separados por hasta tres espacios, puntos o guiones, y
# dentro de ella se prueban las ventanas de grupos consecutivos; así una caducidad, un CVV, una cifra o un código que van
# al lado («… 1111 12/27», «Ref AB12 DE89 …») no esconden el dato, como pasaba cuando el control miraba la serie entera.
RE_GRUPOS_IBAN = re.compile(r"[A-Za-z0-9]+(?:[\s.\-]{1,3}[A-Za-z0-9]+)*")
RE_SEPARADOR = re.compile(r"[\s.\-]+")
# H-02: sin letra, cifra ni «_» pegados antes o después (un tramo de cifras entre las letras de una huella SHA-256, de un
# UUID o de un identificador no es una tarjeta) y sin una cifra y un punto o una coma delante (la parte decimal de un
# número tampoco). T-130 (QA r02 de T-123): una coma o un punto sin cifra delante sí valen («Visa,4111…», una fila CSV,
# H-05), y entre grupos va un solo espacio, espacio duro o guion: con dos espacios o un salto de línea son las columnas
# de una tabla, no una tarjeta (H-07, regresión de la r02).
RE_GRUPOS_TARJETA = re.compile(r"(?<![0-9A-Za-z_])(?<![0-9][.,])([0-9]+(?:[ \u00a0\u202f\-][0-9]+)*)(?![0-9A-Za-z_])")
# T-136 (QA r01 de T-130, H-01 y H-03): estructura del BBAN de cada país en el registro ISO 13616 de SWIFT, tramo a tramo:
# «n» cifras, «a» letras, «c» letras o cifras. Sustituye al tope común de cuatro letras de T-130, que dejaba fuera IBAN reales
# de Rumanía o Letonia. Así una mención de un ISIN o de un índice seguida de palabras, o una huella truncada, no encaja por
# casualidad: además de la longitud y el módulo 97 (1 de cada 97), tiene que cumplir la forma de su país.
ESTRUCTURA_BBAN = {
    "AD": "4n4n12c", "AE": "3n16n", "AT": "5n11n", "BE": "3n7n2n", "BG": "4a4n2n8c", "BR": "8n5n10n1a1c", "CH": "5n12c",
    "CY": "3n5n16c", "CZ": "4n6n10n", "DE": "8n10n", "DK": "4n9n1n", "EE": "2n2n11n1n", "ES": "4n4n1n1n10n", "FI": "3n11n",
    "FR": "5n5n11c2n", "GB": "4a6n8n", "GI": "4a15c", "GR": "3n4n16c", "HR": "7n10n", "HU": "3n4n1n15n1n", "IE": "4a6n8n",
    "IL": "3n3n13n", "IS": "4n2n6n10n", "IT": "1a5n5n12c", "LI": "5n12c", "LT": "5n11n", "LU": "3n13c", "LV": "4a13c",
    "MC": "5n5n11c2n", "MT": "4a5n18c", "NL": "4a10n", "NO": "4n6n1n", "PL": "8n16n", "PT": "4n4n11n2n", "RO": "4a16c",
    "SA": "2n18c", "SE": "3n16n1n", "SI": "5n8n2n", "SK": "4n6n10n", "SM": "1a5n5n12c", "TR": "5n1n16c", "VA": "3n15n"}
_CLASE_BBAN = {"n": "[0-9]", "a": "[A-Z]", "c": "[A-Z0-9]"}
RE_BBAN = {pais: re.compile("".join(f"{_CLASE_BBAN[k]}{{{n}}}" for n, k in re.findall(r"(\d+)([nac])", e)))
           for pais, e in ESTRUCTURA_BBAN.items()}
# países cuyo BBAN es solo de cifras (los 21 de la tabla; T-130 los listaba a mano y le faltaba VA, H-03)
BBAN_NUMERICO = frozenset(p for p, e in ESTRUCTURA_BBAN.items() if set(re.findall(r"[nac]", e)) == {"n"})
LETRAS_GRUPO_MAX = 4      # un grupo de solo letras más largo es una palabra, no un tramo de un IBAN impreso


def _iban_valido(compacto: str) -> bool:
    """Módulo 97 de ISO 13616: los cuatro primeros caracteres al final, cada letra como 10–35, y el resto da 1."""
    reordenado = compacto[4:] + compacto[:4]
    if not reordenado.isalnum() or not reordenado.isascii():
        return False
    return int("".join(str(int(c, 36)) for c in reordenado)) % 97 == 1


def _bban_plausible(compacto: str, grupos: list[str]) -> bool:
    """El BBAN cumple la estructura de su país (ISO 13616) y, si el IBAN venía en grupos, ninguno es una palabra de más de
    cuatro letras ni, salvo el último, una sola cifra suelta (T-136, H-05: lo que dejan los decimales de una
    cifra con punto tras un ISIN)."""
    patron = RE_BBAN.get(compacto[:2])
    if patron is None or not patron.fullmatch(compacto[4:]):
        return False
    if any(g.isalpha() and len(g) > LETRAS_GRUPO_MAX for g in grupos):
        return False
    return not any(len(g) == 1 and g.isdigit() for g in grupos[:-1])   # una letra suelta sí: el CIN italiano («IT60 X 05428…»)


def _misma_caja(iban: str) -> bool:
    """T-136: las letras de un IBAN van todas en la misma caja que su código de país (o todo en mayúsculas o todo en
    minúsculas): las palabras de una frase en minúsculas tras un ISIN o un índice en mayúsculas no forman un IBAN."""
    pais, letras = iban[:2], [c for c in iban[4:] if c.isalpha()]
    if not letras:
        return True
    if pais.isupper():
        return all(c.isupper() for c in letras)
    if pais.islower():
        return all(c.islower() for c in letras)
    return all(c.isupper() for c in letras) or all(c.islower() for c in letras)


def ibanes_en_texto(texto: str) -> list[str]:
    """IBAN con su longitud de país, un BBAN plausible para su país y su dígito de control correctos: grupos consecutivos de
    una serie que empiezan por dos letras y dos cifras y acaban en un límite de grupo (detrás puede venir una palabra o una
    cifra suelta) o en letras pegadas al último grupo («… 3000EUR»). Coste lineal: cada ventana se corta en la longitud del
    país (T-130, H-08: la r02 copiaba la lista en cada vuelta)."""
    hallados = []
    for m in RE_GRUPOS_IBAN.finditer(texto):
        originales = [g for g in RE_SEPARADOR.split(m.group(0)) if g]
        grupos = [g.upper() for g in originales]
        for i, inicio in enumerate(grupos):
            largo = LONGITUD_IBAN.get(inicio[:2])
            if not largo or not inicio[2:4].isdigit() or not inicio[:2].isalpha():
                continue
            compacto, usados, tal_cual = "", [], ""
            for j in range(i, len(grupos)):
                compacto += grupos[j]
                tal_cual += originales[j]
                usados.append(grupos[j])
                if len(compacto) >= largo:
                    break
            sobra = compacto[largo:]
            if len(compacto) < largo or (sobra and not sobra.isalpha()):   # H-09: «…3000EUR» sí; una cifra pegada, no
                continue
            compacto = compacto[:largo]
            if not _misma_caja(tal_cual[:largo]):
                continue
            if _bban_plausible(compacto, usados[1:] if not sobra else usados[1:-1]) and _iban_valido(compacto):
                hallados.append(compacto)
    return hallados


def _luhn(cifras: str) -> bool:
    total = 0
    for i, c in enumerate(reversed(cifras)):
        d = int(c) * (2 if i % 2 else 1)
        total += d - 9 if d > 9 else d
    return total % 10 == 0


def _red_de_tarjeta(cifras: str) -> bool:
    """Prefijo y longitud de las redes de pago corrientes (Visa, Mastercard, American Express, Discover, JCB, UnionPay)."""
    n = len(cifras)
    if cifras[0] == "4":
        return n in (13, 16, 19)
    if 51 <= int(cifras[:2]) <= 55 or 2221 <= int(cifras[:4]) <= 2720:
        return n == 16
    if cifras[:2] in ("34", "37"):
        return n == 15
    if cifras[:4] == "6011" or cifras[:2] == "65" or 3528 <= int(cifras[:4]) <= 3589 or cifras[:2] == "62":
        return 16 <= n <= 19
    return False


def _forma_de_caducidad(g: str) -> bool:
    """Cuatro cifras con forma de caducidad MMAA: mes 01–12 (calendario, no un umbral) y un año cualquiera de dos cifras.
    T-145 (QA r01 de T-140, H-02): un año de cuatro cifras («2027») ya no cuenta como fecha junto a una tarjeta."""
    return g.isdigit() and len(g) == 4 and 1 <= int(g[:2]) <= 12


def _tarjetas_de_la_serie(grupos: list[str]) -> list[str] | None:
    """T-145 (QA r01 de T-140, H-02 y H-03): reparte una serie de grupos de cuatro cifras en tarjetas de cuatro grupos (de
    una red y con Luhn), cada una seguida, si acaso, de su caducidad MMAA. Lo que sobra solo puede ir detrás de una tarjeta
    y con esa forma: las tablas ponen la fecha delante. Un PIN de cuatro cifras tras la caducidad no se admite (marcaría
    las filas con una fecha en medio; INC-T123-01). Devuelve las tarjetas o None si la serie no se reparte así.
    Programación dinámica desde el final (lineal en la longitud de la serie)."""
    n = len(grupos)
    resto: list[list[str] | None] = [None] * (n + 1)
    resto[n] = []
    for i in range(n - 4, -1, -1):
        c = "".join(grupos[i:i + 4])
        if not (_red_de_tarjeta(c) and _luhn(c)):
            continue
        siguientes = [i + 4] + ([i + 5] if i + 4 < n and _forma_de_caducidad(grupos[i + 4]) else [])   # con su caducidad
        for j in siguientes:
            detras = resto[j]
            if detras is not None:
                resto[i] = [c] + detras
                break
    return resto[0]


GRUPOS_FILA_DE_TABLA = 5   # una tarjeta impresa en grupos de cuatro tiene cuatro (16 cifras); con cinco o más es una tabla


def tarjetas_en_texto(texto: str) -> list[str]:
    """Números de tarjeta: 13 a 19 cifras seguidas o en grupos de al menos cuatro (el último puede ser más corto), de una red
    conocida y con el dígito de control de Luhn. Se prueban las ventanas de grupos consecutivos de cada serie. Se devuelven
    enmascarados (solo las cuatro últimas cifras). Un importe con espacio de miles o una lista de números cortos no empiezan
    por un grupo de cuatro ni siguen con ellos, y no se miran (T-123 r02, H-04)."""
    hallados = []
    for m in RE_GRUPOS_TARJETA.finditer(texto):
        grupos = [g for g in re.split(r"[ \u00a0\u202f\-]", m.group(1)) if g]
        if len(grupos) >= GRUPOS_FILA_DE_TABLA and all(len(g) == 4 for g in grupos):
            # T-136 (QA r01 de T-130, H-02), T-140 (QA r01 de T-136, H-02) y T-145 (QA r01 de T-140, H-02 y H-03): cinco o
            # más números de cuatro cifras seguidos son una fila de tabla, salvo que la serie entera se reparta en tarjetas
            # válidas, cada una con, detrás y si acaso, su caducidad MMAA: una tarjeta con su caducidad, dos
            # tarjetas seguidas o cada una con su caducidad se detectan; un año o una fecha delante ya no valen
            tarjetas = _tarjetas_de_la_serie(grupos)
            hallados += ["tarjeta …" + c[-4:] for c in tarjetas or []]
            continue
        for i in range(len(grupos)):
            cifras = ""
            for j in range(i, len(grupos)):
                if len(grupos[j]) < 4 and j == i:
                    break
                cifras += grupos[j]
                if len(cifras) > 19:
                    break
                if len(cifras) >= 13 and _red_de_tarjeta(cifras) and _luhn(cifras):
                    hallados.append("tarjeta …" + cifras[-4:])
                if len(grupos[j]) < 4:
                    break
    return list(dict.fromkeys(hallados))


def secretos_en_texto(texto) -> list[str]:
    """Indicios de secretos en un texto: los patrones de `RE_SECRETO` y las claves «sk-». También se mira el texto con los
    escapes de JSON («\\n», «\\t», «\\r», «\\/») sustituidos, porque la respuesta de un agente es JSON escrito como
    texto (T-92, QA r03, H-25), y desde T-93 (H-32) también «\\uXXXX», «\\b», «\\f», «\\"», «\\\\», los «\\xNN» de `repr`
    y los «%XX» de una URL. Acepta `bytes` (H-26)."""
    if isinstance(texto, (bytes, bytearray)):
        texto = bytes(texto).decode("utf-8", errors="replace")
    hallados: list[str] = []
    for t in {texto, RE_ESCAPES.sub(" ", texto)}:
        hallados += [m.group(0) for m in RE_SECRETO.finditer(t)]
        hallados += [m.group(0) for m in RE_CANDIDATO_SK.finditer(t) if _es_clave_sk(m.group(1))]
        hallados += ibanes_en_texto(t) + tarjetas_en_texto(t)   # T-123
    return list(dict.fromkeys(hallados))


def _textos(obj: Any):
    if isinstance(obj, (str, bytes, bytearray)):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from _textos(k)
            yield from _textos(v)
    elif isinstance(obj, (list, tuple, set, frozenset)):   # T-103 (H-44): también `frozenset`, como `contenido_sensible`
        for v in obj:
            yield from _textos(v)


def contiene_credenciales(obj: Any) -> list[str]:
    """T-92 (QA r02, H-18): se busca en el volcado JSON (para los pares «"password": "…"») y en cada texto tal cual (en el
    volcado un salto de línea delante de la clave sale escapado como «\\n» y ocultaría la clave)."""
    volcado = json.dumps(obj, ensure_ascii=False, default=str)
    hallados = secretos_en_texto(volcado)
    for t in _textos(obj):
        hallados += secretos_en_texto(t)
    return list(dict.fromkeys(h[:6] + "…" for h in hallados))


# T-101 · Canales del diseño V6: solo se abren con `diseno: v6` (en la V5 siguen cerrados, R2). El Lector de evidencia
# (AG-28) atiende CT-07 y CT-08 en el ciclo y el Sintetizador (AG-26), CT-15. El Respondedor (AG-27) contesta la CT-03 que
# el Coordinador recibe del Broker: no abre canal propio.
CANALES_V6: dict[str, list[tuple[set, set]]] = {
    "CT-07": _par(ANALISTAS, {"AG-28"}),
    "CT-08": _par(ANALISTAS, {"AG-28"}),
    "CT-15": _par({"AG-02"}, {"AG-26"}),
}


def canal_permitido(contrato: str, emisor: str, receptor: str, v6: bool = False) -> bool:
    for em, rc in CANALES.get(contrato, []) + (CANALES_V6.get(contrato, []) if v6 else []):
        if emisor in em and receptor in rc:
            return True
    return False


class Mensajeria:
    """Crea y valida mensajes; mantiene el registro de msg_id procesados (idempotencia)."""

    def __init__(self, almacen, v6: bool = False) -> None:
        self.almacen = almacen
        self.v6 = v6   # T-101: abre los canales del diseño V6
        self._lock = threading.Lock()
        self._procesar = threading.Lock()
        self.registro: list[dict] = []   # traza de mensajes (contrato, emisor, receptor, msg_id)
        self._local = threading.local()

    @contextlib.contextmanager
    def ambito(self, nombre: str):
        """T-65 (CA-15 de T-53): los mensajes creados dentro de un ámbito (el análisis de un tipo de activo en su hilo) llevan
        un contador propio, `MSG-<ámbito>-AAAA-nnnnnn`. Así sus `msg_id` no dependen del orden en que se intercalan los hilos."""
        previo = getattr(self._local, "ambito", None)
        self._local.ambito = str(nombre)
        try:
            yield
        finally:
            self._local.ambito = previo

    def crear(self, contrato: str, emisor: str, receptor: str, cuerpo: dict, *, run_id: str | None = None,
              query_id: str | None = None, presupuesto: dict | None = None, consumo: dict | None = None,
              estado: str | None = None, tipo_mensaje: str = "ENCARGO") -> dict:
        cuerpo = copy.deepcopy(cuerpo)
        # En CT-01 el Broker puede aportar su identificador estable de reintento.
        externo = cuerpo.pop("msg_id", None) if contrato == "CT-01" and emisor == "BROKER" else None
        # T-92 (QA r01, H-08): el identificador del Broker tiene su propio espacio (MSG-BRK-…), distinto del que numera el
        # bloque (MSG-AAAA-… o MSG-<ámbito>-AAAA-…), para que nunca coincidan
        if externo is not None and (not isinstance(externo, str) or not re.fullmatch(r"MSG-BRK-[0-9]{4}-[0-9]{1,12}", externo)):
            raise MensajeInvalido("msg_id externo no válido (formato MSG-BRK-AAAA-NNNNNN)")
        if tipo_mensaje == "RETORNO" and contrato in CAMPO_ESTADO:
            campo = CAMPO_ESTADO[contrato]
            if "estado" in cuerpo:
                antiguo = cuerpo.pop("estado")
                if campo in cuerpo and antiguo == (estado or "COMPLETO"):
                    antiguo = cuerpo[campo]
                if campo in cuerpo and cuerpo[campo] != antiguo:
                    raise MensajeInvalido(f"{contrato}: estados de objeto contradictorios")
                cuerpo[campo] = antiguo
        amb = getattr(self._local, "ambito", None)
        msg = {"msg_id": externo or self.almacen.nuevo_id(f"MSG-{amb}" if amb else "MSG", ancho=6), "contrato": contrato, "version_contrato": VERSION_CONTRATO,
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
        reservados = {"msg_id", "contrato", "version_contrato", "emisor", "receptor", "timestamp",
                      "tipo_mensaje", "run_id", "query_id", "presupuesto", "consumo", "estado"}
        for campo in reservados & cuerpo.keys():
            if cuerpo[campo] != msg.get(campo):
                raise MensajeInvalido(f"No se puede cambiar {campo} desde el cuerpo")
            cuerpo.pop(campo)
        msg.update(cuerpo)
        self.validar(msg)
        with self._lock:
            self.registro.append({k: msg.get(k) for k in ("msg_id", "contrato", "emisor", "receptor", "tipo_mensaje")})
        return msg

    def validar(self, msg: dict) -> None:
        for c in ("msg_id", "contrato", "version_contrato", "emisor", "receptor", "timestamp"):
            if not msg.get(c):
                raise MensajeInvalido(f"Falta el campo común {c}")
        if msg["version_contrato"] != VERSION_CONTRATO or msg.get("tipo_mensaje") not in ("ENCARGO", "RETORNO"):
            raise MensajeInvalido("Versión o tipo de mensaje no admitido")
        if msg["contrato"] not in CANALES:
            self.almacen.incidencia("CANAL_NO_PREVISTO", f"Contrato inexistente {msg['contrato']}", msg.get("emisor", ""),
                                    tratamiento="rechazada y registrada", escalado_operador=True)   # R2: se escala (PB-22, INC-T116-03)
            raise CanalNoPrevisto(f"Contrato inexistente {msg['contrato']}")
        if not canal_permitido(msg["contrato"], msg["emisor"], msg["receptor"], self.v6):
            self.almacen.incidencia("CANAL_NO_PREVISTO",
                                    f"{msg['emisor']} → {msg['receptor']} por {msg['contrato']} no previsto (R2)", msg["emisor"],
                                    tratamiento="rechazada y registrada", escalado_operador=True)
            raise CanalNoPrevisto(f"{msg['emisor']} → {msg['receptor']} por {msg['contrato']} no previsto (R2)")
        cred = contiene_credenciales({k: v for k, v in msg.items() if k not in ("msg_id", "timestamp")})
        if cred:
            campos = [k for k, v in msg.items() if contiene_credenciales(v)]
            self.almacen.incidencia("SEGURIDAD", "Mensaje con credenciales o datos personales rechazado íntegro (R8)",
                                    msg["emisor"], campo_afectado=campos)
            raise DatosSensibles(f"Mensaje {msg['msg_id']} con datos protegidos en {campos}")
        if not msg.get("run_id") and not msg.get("query_id") and msg["contrato"] not in ("CT-01", "CT-03", "CT-04", "CT-18", "CT-21", "CT-23", "CT-24", "CT-25"):
            raise MensajeInvalido("Falta run_id o query_id")
        tipo = msg.get("tipo_mensaje", "ENCARGO")
        req = CAMPOS_MINIMOS.get(msg["contrato"], []) if tipo == "ENCARGO" else CAMPOS_RETORNO.get(msg["contrato"], [])
        if tipo == "RETORNO" and msg["contrato"] in CAMPO_ESTADO:
            campo = CAMPO_ESTADO[msg["contrato"]]
            if msg.get(campo) not in ESTADOS_ESPECIFICOS[msg["contrato"]]:
                raise MensajeInvalido(f"{campo} no válido")
        falta = [c for c in req if c not in msg]
        if falta:
            raise MensajeInvalido(f"{msg['contrato']}: faltan campos mínimos {falta}")
        if tipo == "ENCARGO" and msg["contrato"] == "CT-01":
            if msg["tipo"] not in ("AD_HOC", "PROFUNDIZACION", "PERIODICO") or msg["prioridad"] not in ("ALTA", "NORMAL", "BAJA"):
                raise MensajeInvalido("CT-01: tipo o prioridad no admitidos")
            if not isinstance(msg["alcance"], dict) or not isinstance(msg["horizontes"], list) or any(
                    h not in ("H1", "H2", "H3", "H4", "H5") for h in msg["horizontes"]):
                raise MensajeInvalido("CT-01: alcance u horizontes no válidos")
        if tipo == "RETORNO" and msg["contrato"] == "CT-02" and (
                not isinstance(msg.get("entregables"), dict) or not isinstance(msg.get("resumen"), dict)
                or msg.get("estado_g3") not in ("APTO", "APTO_CON_ADVERTENCIAS")):
            raise MensajeInvalido("CT-02: se requiere una entrega G3 aprobada con rutas y resumen")
        if tipo != "ENCARGO" and msg.get("estado") not in ESTADOS:
            raise MensajeInvalido(f"Estado de retorno no válido {msg.get('estado')!r}")

    def procesar_una_vez(self, msg: dict, funcion) -> tuple[dict, bool]:
        """Idempotencia: devuelve (respuesta, repetido). El mismo msg_id no se reprocesa."""
        self.validar(msg)
        identidad = {k: v for k, v in msg.items() if k not in ("timestamp", "msg_id")}
        huella = hashlib.sha256(json.dumps(identidad, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        # Reservar ANTES de los efectos del ciclo. Una reserva huérfana exige revisión:
        # no se puede saber si ya produjo efectos antes de la caída.
        with self._procesar, closing(self._acuses()) as db:
            with db:
                insertado = db.execute("INSERT OR IGNORE INTO acuses (id, huella) VALUES (?, ?)", (msg["msg_id"], huella))
                if not insertado.rowcount:
                    anterior, respuesta, error = db.execute("SELECT huella, respuesta, error FROM acuses WHERE id=?",
                                                            (msg["msg_id"],)).fetchone()
                    if anterior != huella:
                        raise MensajeInvalido("msg_id reutilizado con contenido distinto")
                    if respuesta is None:
                        estado = f"fallido ({error}) o interrumpido" if error else "en curso o interrumpido"
                        raise MensajeInvalido(f"Mensaje {estado}: revise F5 y, si no dejó efectos que repetir, libere la "
                                              "reserva con `bloque-a reconciliar-mensaje` antes de reintentar")
                    return json.loads(respuesta), True
            try:
                r = funcion(msg)
            except BaseException as e:
                # T-92: el fallo queda anotado (sin el texto, que podría llevar datos sensibles); la reserva sigue bloqueada
                # porque pudo haber efectos, pero ya se distingue de una caída y se puede reconciliar
                with db:
                    db.execute("UPDATE acuses SET error=? WHERE id=?", (type(e).__name__, msg["msg_id"]))
                raise
            # T-92 (QA r01, H-13): la respuesta es la misma la primera vez y al repetirla (la forma guardada)
            guardada = json.dumps(r, default=str)
            with db:
                db.execute("UPDATE acuses SET respuesta=? WHERE id=?", (guardada, msg["msg_id"]))
            return json.loads(guardada), False

    def _acuses(self):
        db = sqlite3.connect(self.almacen.carpeta / "acuses.sqlite3")
        db.execute("CREATE TABLE IF NOT EXISTS acuses (id TEXT PRIMARY KEY, huella TEXT NOT NULL, respuesta TEXT)")
        if "error" not in {fila[1] for fila in db.execute("PRAGMA table_info(acuses)")}:
            db.execute("ALTER TABLE acuses ADD COLUMN error TEXT")
        return db

    def estado_reserva(self, msg_id: str) -> dict:
        """T-92: COMPLETADO, FALLIDO (con la clase del error), EN_CURSO (o interrumpido) o DESCONOCIDO."""
        with self._procesar, closing(self._acuses()) as db:
            fila = db.execute("SELECT respuesta, error FROM acuses WHERE id=?", (msg_id,)).fetchone()
        if fila is None:
            return {"msg_id": msg_id, "estado": "DESCONOCIDO"}
        respuesta, error = fila
        estado = "COMPLETADO" if respuesta is not None else ("FALLIDO" if error else "EN_CURSO")
        return {"msg_id": msg_id, "estado": estado, "error": error}

    def reconciliar(self, msg_id: str, motivo: str) -> dict:
        """T-92 (revisión de la auditoría de Astra): libera la reserva de un mensaje fallido o interrumpido para que el Broker
        pueda reintentarlo con el mismo msg_id. Solo la usa el operador tras revisar F5; queda una incidencia en HA. Un mensaje
        COMPLETADO no se libera (su respuesta se recupera tal cual)."""
        if not isinstance(motivo, str) or not motivo.strip():
            raise MensajeInvalido("La reconciliación exige un motivo")
        estado = self.estado_reserva(msg_id)
        if estado["estado"] not in ("FALLIDO", "EN_CURSO"):
            raise MensajeInvalido(f"No hay una reserva fallida o interrumpida que reconciliar ({estado['estado']})")
        # T-92 (QA r01, H-12): primero el rastro en HA; si HA falla, la reserva no se libera
        self.almacen.incidencia("OTRO", f"Reserva de {msg_id} liberada por el operador ({estado['estado']}): {motivo.strip()}",
                                "AG-01", severidad="Operativa", tratamiento="reconciliación manual de CT-01")
        with self._procesar, closing(self._acuses()) as db, db:
            db.execute("DELETE FROM acuses WHERE id=? AND respuesta IS NULL", (msg_id,))
        return {**estado, "estado": "LIBERADA"}

    def acuse(self, msg: dict, asignado: str, **extra) -> dict:
        return {"acuse_de": msg["msg_id"], "asignado": asignado, "timestamp": self.almacen.reloj.ahora(), **extra}


# ============================================================================================
# Esquemas JSON mínimos de las respuestas de los agentes
# ============================================================================================
DIM = {"anyOf": [{"type": "integer", "minimum": 0, "maximum": 100, "multipleOf": 10}, {"enum": ["NA", "NE"]}]}
DIMS = {"type": "object", "additionalProperties": DIM}
TIPOS_OPCION = ["MERCADO", "SECTOR", "SUBSECTOR", "TEMATICA", "SEGMENTO", "FACTOR", "ESTILO", "ESTRATEGIA"]   # 2.4 V5.0
REGIONES = ["NAM", "LAT", "EUR", "AFR", "ORM", "CHN", "ASE", "JPN", "OCE", "GLB"]
TXT = {"type": "string", "minLength": 1}
LISTA_TXT = {"type": "array", "items": {"type": "string"}}

LISTA_TXT_MIN1 = {"type": "array", "minItems": 1, "items": TXT}
AMBITO = {"type": "object", "required": ["incluye", "excluye", "region"],
          "properties": {"incluye": TXT, "excluye": TXT, "region": TXT}}
# En el ejecutor el indicador de seguimiento necesita un símbolo HT-01 del universo (para medir y resolver F4)
INDICADOR = {"type": "object", "required": ["nombre", "simbolo"],
             "properties": {"nombre": TXT, "simbolo": TXT, "fuente": {"type": "string"}, "tipo": {"type": "string"}}}
INVERTIBILIDAD = {"type": "object", "required": ["universo_suficiente", "nota"],
                  "properties": {"universo_suficiente": {"type": "boolean"}, "nota": TXT}}

# Ficha de una finalista (CT-06, informe de tipo de activo): un ÁMBITO, nunca un activo concreto (2.4–2.5, R21)
FINALISTA = {
    "type": "object",
    "required": ["nombre", "nombre_llano", "tipo_opcion", "subtipo", "ambito", "indicador_seguimiento", "invertibilidad",
                 "tesis", "mecanismo", "valoracion", "catalizadores", "riesgos", "invalidacion", "horizontes_aplicables",
                 "dimensiones", "premortem", "afirmaciones", "lo_que_no_sabemos", "regiones",
                 "criterios_seleccion_sugeridos", "metricas_clave", "preguntas_para_B"],
    "properties": {
        "nombre": TXT, "nombre_llano": {"type": "string", "minLength": 3, "maxLength": 70},
        "tipo_opcion": {"enum": TIPOS_OPCION}, "subtipo": TXT, "ambito": AMBITO, "indicador_seguimiento": INDICADOR,
        "invertibilidad": INVERTIBILIDAD, "ejemplos_ilustrativos": {"type": "array", "maxItems": 8, "items": TXT},
        "tipos_secundarios": {"type": "array", "items": {"type": "string"}},
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
        "naturaleza_inversion": {"enum": ["TACTICA", "LIQUIDEZ", "CICLICA", "PRIMA_RIESGO", "VALORACION", "ESTRUCTURAL"]},
        # V5.1 (8.3): el Analista declara el horizonte principal y, si sale del rango de su naturaleza, lo justifica
        "horizonte_principal": {"enum": ["H1", "H2", "H3", "H4", "H5"]},
        "justificacion_horizonte": {"type": ["string", "null"]},
        # PA-21 (T-66): probabilidad propia del Analista por horizonte (opcional; segunda opinión que mide el Evaluador)
        "probabilidades_propias": {"type": "object", "additionalProperties": {"type": "number", "minimum": 0.05, "maximum": 0.95}},
        "dimensiones": {"type": "object", "required": ["T", "E", "M", "A", "P"],
                        "properties": {"T": {"anyOf": [DIMS, {"const": "NA"}]}, "E": DIMS, "M": DIMS, "A": DIMS, "P": DIMS}},
        "segunda_pasada": {"type": "object"},
        "saturacion_narrativa": {"type": "boolean"},
        "premortem": TXT,
        "afirmaciones": {"type": "array", "minItems": 1, "items": {"type": "object", "required": ["afirmacion", "fuente", "direccion"],
                         "properties": {"afirmacion": TXT, "fuente": TXT,
                                        "direccion": {"enum": ["favorable", "contraria", "neutra", "ambigua"]}}}},
        "lo_que_no_sabemos": {"type": "array", "minItems": 1, "items": TXT},
        "regiones": {"type": "array", "minItems": 1, "items": {"enum": REGIONES}},
        "liquidez": {"enum": ["alta", "media", "baja"]},
        "criterios_seleccion_sugeridos": LISTA_TXT_MIN1, "metricas_clave": LISTA_TXT_MIN1, "preguntas_para_B": LISTA_TXT_MIN1,
        "discrepancia_material": {"type": "boolean"},
        "tendencia": {"type": "object", "required": ["nombre_canonico"]},
        "peticiones_conocimiento": {"type": "array"},
    },
    # V5.0: se retiran los vehículos de implementación y la accesibilidad del vehículo (los sustituyen el ámbito,
    # el indicador de seguimiento, la invertibilidad y el encargo para el Bloque B)
    "not": {"anyOf": [{"required": ["vehiculos_genericos"]}, {"required": ["accesibilidad_minorista_ue"]}]},
}
REVISION = {"type": "array", "items": {"type": "object", "required": ["opp_id", "invalidacion_activada", "recomendacion"],
            "properties": {"opp_id": TXT, "invalidacion_activada": {"type": "boolean"},
                           "recomendacion": {"enum": ["MANTENER", "REVISAR", "CERRAR"]}}}}
ESTADO_RET = {"enum": list(ESTADOS)}

ESQUEMAS: dict[str, dict] = {
    "INFORME_CLASE": {
        "type": "object",
        "required": ["clase", "estado", "regimen_clase", "revision_vigentes", "cribado", "finalistas", "lagunas", "autoevaluacion"],
        "properties": {"clase": TXT, "estado": ESTADO_RET,
                       "regimen_clase": {"type": "object", "required": ["diagnostico"]},
                       "revision_vigentes": REVISION,
                       "cribado": {"type": "array", "items": {"type": "object", "required": ["candidata", "paso_gc1", "motivo"]}},
                       "finalistas": {"type": "array", "maxItems": 5, "items": FINALISTA},
                       "descartadas_relevantes": {"type": "array"}, "lagunas": LISTA_TXT, "autoevaluacion": {"type": "string"}},
    },
    "REVISION_VIGENTES": {
        "type": "object", "required": ["clase", "estado", "regimen_clase", "revision_vigentes", "autoevaluacion"],
        "properties": {"clase": TXT, "estado": ESTADO_RET, "regimen_clase": {"type": "object", "required": ["diagnostico"]},
                       "revision_vigentes": REVISION, "exploratorias": {"type": "array", "maxItems": 2, "items": FINALISTA}},
    },
    "RESPUESTA_OBJECIONES": {
        "type": "object", "required": ["respuestas"],
        "properties": {"respuestas": {"type": "array", "items": {"type": "object", "required": ["objecion_id", "respuesta", "resuelta"],
                       "properties": {"objecion_id": TXT, "respuesta": {"type": "string"}, "resuelta": {"type": "boolean"},
                                      "evidencia_citada": {"type": "array", "items": {"type": "string"}}}}}},
    },
    "CONTRARREPLICA": {   # PA-05 (T-66): el Contradictor confirma o no la resolución de cada objeción fuerte
        "type": "object", "required": ["resultados"],
        "properties": {"resultados": {"type": "array", "items": {"type": "object", "required": ["objecion_id", "resuelta"],
                       "properties": {"objecion_id": TXT, "resuelta": {"type": "boolean"}, "motivo": {"type": "string"}}}}},
    },
    "PROSPECTIVA": {
        "type": "object", "required": ["resultados", "autoevaluacion"],
        "properties": {"resultados": {"type": "array", "items": {"type": "object", "required": ["ref", "pronosticos", "escenarios"],
            "properties": {"ref": TXT, "escenarios": {"type": "object"}, "hitos": {"type": "array"},
                           "indicadores_adelantados": {"type": "array"}, "invalidacion": {"type": "array"},
                           "pronosticos": {"type": "array", "items": {"type": "object",
                               "required": ["horizonte", "vista", "prob_interna", "afirmacion", "escenario_asociado"],
                               "properties": {"horizonte": {"enum": ["H1", "H2", "H3", "H4", "H5"]},
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
                       "lectura_conjunto": TXT, "preguntas_sugeridas": LISTA_TXT, "limitaciones": LISTA_TXT,
                       "cambios_vs_anterior": {"type": "string"}},
    },
    "REDACCION": {
        "type": "object", "required": ["frases_30s", "tarjetas", "motivos_llanos", "glosario", "frase_historial"],
        "properties": {"frases_30s": {"type": "array", "minItems": 3, "maxItems": 3, "items": TXT},
                       "tarjetas": {"type": "array", "items": {"type": "object", "required": ["opp_id", "por_que_llano", "que_puede_salir_mal_llano"],
                                    "properties": {"por_que_llano": {"type": "string", "maxLength": 160},
                                                   "que_puede_salir_mal_llano": {"type": "string", "maxLength": 200},
                                                   "ambito_llano": {"type": "string", "maxLength": 160}}}},
                       "motivos_llanos": {"type": "object"},
                       "glosario": {"type": "array", "maxItems": 5, "items": {"type": "object", "required": ["termino", "definicion"]}},
                       "frase_historial": TXT},
    },
    # T-101 (V6): el Sintetizador devuelve los textos del Redactor y, opcionalmente, los de la integración
    "SINTESIS": {
        "type": "object", "required": ["frases_30s", "tarjetas", "motivos_llanos", "glosario", "frase_historial"],
        # T-102 r06: el Sintetizador escribe dos frases de 30 s; la primera, con las cuentas, la escribe el código. T-113
        # (H-50 de T-110): se admiten de una a tres; `_redaccion_segura` toma las dos primeras o completa y lo declara
        "properties": {"frases_30s": {"type": "array", "minItems": 1, "maxItems": 3, "items": TXT},
                       "tarjetas": {"type": "array", "items": {"type": "object", "required": ["opp_id", "por_que_llano", "que_puede_salir_mal_llano"],
                                    "properties": {"por_que_llano": {"type": "string", "maxLength": 160},
                                                   "que_puede_salir_mal_llano": {"type": "string", "maxLength": 200},
                                                   "ambito_llano": {"type": "string", "maxLength": 160}}}},
                       "motivos_llanos": {"type": "object"},
                       "glosario": {"type": "array", "maxItems": 5, "items": {"type": "object", "required": ["termino", "definicion"]}},
                       "frase_historial": TXT, "regimen_macro": {"type": "string"}, "factores_dominantes": {"type": "array"},
                       "lectura_conjunto": {"type": "string"}, "preguntas_sugeridas": {"type": "array"}, "limitaciones": {"type": "array"}},
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
