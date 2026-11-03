#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HT-09 · Validador determinista G3 (implementación de referencia).

Bloque A · Robot Investor · Versión óptima V5.0 · 02/11/2026 · Subordinado al
Documento 0 óptima V5.0 (secciones 2.4–2.6, 4.4, 7.3 F6, 7.8, 8.3, 9, 14 y
Anexos A y B).

Valida un `paquete_oportunidades` (Anexo B) y devuelve el dictamen
APTO / APTO_CON_ADVERTENCIAS / BLOQUEADO con la lista de comprobaciones:

  C01 Campos obligatorios y valores permitidos
  C02 Máximo de opciones por tipo de activo y rangos
  C03 Menos de tres con motivo (R14)
  C04 Puntuaciones reconstruibles con HT-03 (RK siempre; dimensiones si hay desglose)
  C05 Elegibilidad (9.2) y puertas G1–G4 / PS1–PS8
  C06 Horizontes compatibles con la tabla 8.3
  C07 Probabilidad numérica solo con certificado de horizonte (R13)
  C08 Evidencias y cálculos referenciados no vacíos (R7) y trazas CLM→EVD
  C09 Objeciones: ninguna fuerte sin resolver; respuestas a fuertes y moderadas (R12)
  C10 Coherencia de `relevancia_decisional` con la regla del Anexo A
  C11 `paquete_para_bloque_B` para opciones con ENVIAR_A_BLOQUE_B
  C12 Legibilidad del informe visual con HT-07 (Fernández-Huerta ≥ 70)
  C13 Ausencia de credenciales o secretos (R8)
  C14 Coherencia del semáforo y de las apuestas independientes
  C15 Frontera con el Bloque B: ninguna selección de activo concreto (2.4–2.5, R21)
  C16 Oportunidad duplicada en dos tipos de activo (regla 5 de 2.6)

Los doce tipos de activo (RV, RF, DIV, MP, IDX, FON, DER, INM, CRI, ALT, MON,
TCV) y la tabla de horizontes 8.3 son los de la V5.0; PS3 es la invertibilidad
del ámbito.

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

VERSION = "5.0"
CLASES = ht03.TIPOS_ACTIVO          # los doce tipos de activo de 2.6, en su orden canónico
HORIZONTES = ("H1", "H2", "H3", "H4")
# Tabla 8.3 (V5.0): SI, LIMITADO, NO
TABLA_HORIZONTES = {
    "RV": {"H1": "LIMITADO", "H2": "SI", "H3": "SI", "H4": "SI"},
    "RF": {"H1": "LIMITADO", "H2": "SI", "H3": "SI", "H4": "SI"},
    "DIV": {"H1": "SI", "H2": "SI", "H3": "SI", "H4": "LIMITADO"},
    "MP": {"H1": "SI", "H2": "SI", "H3": "SI", "H4": "SI"},
    "IDX": {"H1": "LIMITADO", "H2": "SI", "H3": "SI", "H4": "SI"},
    "FON": {"H1": "NO", "H2": "LIMITADO", "H3": "SI", "H4": "SI"},
    "DER": {"H1": "SI", "H2": "SI", "H3": "SI", "H4": "NO"},
    "INM": {"H1": "NO", "H2": "LIMITADO", "H3": "SI", "H4": "SI"},
    "CRI": {"H1": "SI", "H2": "SI", "H3": "SI", "H4": "LIMITADO"},
    "ALT": {"H1": "NO", "H2": "NO", "H3": "LIMITADO", "H4": "SI"},
    "MON": {"H1": "LIMITADO", "H2": "SI", "H3": "SI", "H4": "NO"},
    "TCV": {"H1": "SI", "H2": "SI", "H3": "SI", "H4": "LIMITADO"},
}
# Granularidad del ámbito (2.4): nunca un activo concreto
TIPOS_OPCION = ("MERCADO", "SECTOR", "SUBSECTOR", "TEMATICA", "SEGMENTO", "FACTOR", "ESTILO", "ESTRATEGIA")
TIPOS_OPCION_RETIRADOS = {"INSTRUMENTO_GENERICO": "retirado en V5.0 (el Bloque A no propone instrumentos)",
                          "INDUSTRIA": "retirado en V5.0: usar SUBSECTOR"}
CAMPOS_RETIRADOS = ("vehiculos_genericos",)   # «vehículos de implementación» (V4.x) sustituidos por ámbito e invertibilidad
RE_ISIN = re.compile(r"\b[A-Z]{2}[A-Z0-9]{9}[0-9]\b")
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
}
CAMPOS_RAIZ = ["run_id", "fecha", "methodology_version", "tipo", "regimen_macro", "apuestas_independientes", "clases",
               "seguimiento_vigentes", "historial_aciertos", "paquete_para_bloque_B", "preguntas_sugeridas", "limitaciones"]
CAMPOS_CLASE = ["estado_semaforo", "regimen_clase", "candidatas_analizadas", "opciones", "menos_de_tres_motivo"]
CAMPOS_OPCION_NO_VACIOS = ["opp_id", "rango", "tipo_opcion", "tipo_activo", "subtipo", "nombre", "nombre_llano", "tesis",
                           "mecanismo", "puntuaciones", "horizontes", "valoracion", "riesgos", "riesgo_1a5", "invalidacion",
                           "invertibilidad", "liquidez", "relevancia_decisional", "reversibilidad",
                           "siguiente_paso_sugerido", "que_cambiaria_la_conclusion", "confianza", "evidencias", "calculos"]
# «ambito» e «indicador_seguimiento» se comprueban en C15 (su ausencia indica selección de activo concreto)
CAMPOS_OPCION_PRESENTES = ["tnd_ids", "catalizadores", "objeciones"]
# Encargo para el Bloque B (2.5 y Anexo B V5.0)
CAMPOS_BLOQUE_B = ["tipo_activo", "subtipo", "ambito", "tesis", "mecanismo", "horizontes", "pronosticos", "catalizadores",
                   "riesgos", "invalidacion", "indicador_seguimiento", "criterios_seleccion_sugeridos", "metricas_clave",
                   "preguntas_para_B", "evidencias", "calculos"]
CAMPOS_BLOQUE_B_PUEDEN_VACIOS = ("catalizadores",)
RE_SECRETO = re.compile(
    r"(?i)(\"(api[_-]?key|apikey|secret|client_secret|password|passwd|contraseña|access[_-]?token|bearer)\"\s*:\s*\"[^\"]+\")"
    r"|(sk-[A-Za-z0-9_-]{20,})|(AKIA[0-9A-Z]{16})|(-----BEGIN [A-Z ]*PRIVATE KEY-----)|(Bearer\s+[A-Za-z0-9._-]{20,})")


class Registro:
    NOMBRES = {
        "C01": "Campos obligatorios y valores permitidos", "C02": "Máximo de opciones por tipo de activo y rangos",
        "C03": "Menos de tres con motivo (R14)", "C04": "Puntuaciones reconstruibles con HT-03",
        "C05": "Elegibilidad (9.2) y puertas G1–G4 / PS1–PS8", "C06": "Horizontes compatibles con la tabla 8.3",
        "C07": "Probabilidad numérica solo con certificado (R13)", "C08": "Evidencias y cálculos referenciados (R7)",
        "C09": "Objeciones resueltas o respondidas (R12)", "C10": "Relevancia decisional (Anexo A)",
        "C11": "Paquete para el Bloque B", "C12": "Legibilidad del informe visual (HT-07)",
        "C13": "Ausencia de credenciales (R8)", "C14": "Coherencia del semáforo y apuestas independientes",
        "C15": "Frontera con el Bloque B: sin selección de activo concreto (R21)",
        "C16": "Oportunidad duplicada en dos tipos de activo (2.6)",
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
    """Minúsculas, sin tildes ni signos, sin palabras vacías: clave para detectar duplicados entre tipos."""
    import unicodedata
    t = unicodedata.normalize("NFKD", str(t or "")).encode("ascii", "ignore").decode("ascii").lower()
    t = re.sub(r"\(.*?\)", " ", t)
    palabras = [w for w in re.split(r"[^a-z0-9]+", t) if w and w not in STOPWORDS]
    return " ".join(palabras)


def clave_ambito(op: Dict) -> Optional[str]:
    amb = op.get("ambito")
    if not isinstance(amb, dict) or _vacio(amb.get("incluye")):
        return None
    return normalizar_texto(amb.get("incluye")) + " | " + normalizar_texto(amb.get("region"))


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


def relevancia_esperada_alta(op: Dict, clase: str, vigente: bool, p: Dict) -> List[str]:
    """Disparadores de relevancia ALTA según el Anexo A."""
    motivos = []
    r = op.get("riesgo_1a5")
    if isinstance(r, (int, float)) and r >= 4:
        motivos.append(f"riesgo {r}/5 ≥ 4")
    if str(op.get("reversibilidad", "")).lower() == "baja":
        motivos.append("reversibilidad baja")
    if "H4" in _horizontes_ofrecidos(op) and str(op.get("liquidez", "")).lower() == "baja":
        motivos.append("horizonte H4 con iliquidez")
    pu = op.get("puntuaciones") or {}
    E, A = pu.get("E"), pu.get("A")
    if isinstance(E, (int, float)) and isinstance(A, (int, float)) and E < p.get("rel_E", 70) and A >= p.get("rel_A", 75):
        motivos.append(f"E {E} < 70 con A {A} ≥ 75 (atractiva pero incierta)")
    if clase in ("CRI", "ALT") and not vigente:
        motivos.append(f"opción nueva en clase {clase}")
    return motivos


def validar(paquete: Dict, certificados: Optional[List[Dict]] = None, informe_visual: Optional[str] = None,
            desgloses: Optional[Dict[str, Dict]] = None, parametros: Optional[Dict] = None,
            trazas: Optional[Dict[str, List[str]]] = None, artefactos: Optional[List[str]] = None,
            umbral_fh: float = 70.0) -> Dict:
    R = Registro()
    p = ht03.fusionar_parametros(parametros)
    u = p["umbrales"]
    certificados = certificados or []
    desgloses = desgloses or {}
    if trazas is None and isinstance(paquete.get("trazas"), dict):
        trazas = paquete["trazas"]

    # C13 credenciales
    volcado = json.dumps(paquete, ensure_ascii=False)
    for m in RE_SECRETO.finditer(volcado):
        R.bloqueo("C13", "(paquete)", f"Posible credencial o secreto: «{m.group(0)[:24]}…»")

    # C01 raíz
    for c in CAMPOS_RAIZ:
        if c not in paquete:
            R.bloqueo("C01", c, "Campo obligatorio ausente")
    for c in ("run_id", "fecha", "methodology_version", "regimen_macro"):
        if c in paquete and _vacio(paquete[c]):
            R.bloqueo("C01", c, "Campo obligatorio vacío")
    if paquete.get("tipo") is not None and paquete.get("tipo") not in ENUMS["tipo"]:
        R.bloqueo("C01", "tipo", f"Valor no permitido {paquete.get('tipo')!r}")
    if paquete.get("run_id") and not str(paquete["run_id"]).startswith("RUN-"):
        R.advertencia("C01", "run_id", "No sigue el formato RUN-")
    if paquete.get("methodology_version") and str(paquete["methodology_version"]).split(".")[0] not in ("4", "5"):
        R.advertencia("C01", "methodology_version", f"Versión de metodología {paquete['methodology_version']} distinta de 4.x/5.x")
    clases = paquete.get("clases") if isinstance(paquete.get("clases"), dict) else {}
    vigentes = {s.get("opp_id") for s in (paquete.get("seguimiento_vigentes") or []) if isinstance(s, dict)
                and str(s.get("estado", "")).upper() == "VIGENTE"}
    bloque_b = {b.get("opp_id"): b for b in (paquete.get("paquete_para_bloque_B") or []) if isinstance(b, dict)}
    total_opciones = 0
    ids_vistos: set = set()
    recalculadas: Dict[str, Dict] = {}
    claves_dup: Dict[str, List[tuple]] = {}   # C16: clave normalizada → [(tipo, opp_id, criterio)]
    tipo_de_opp: Dict[str, str] = {}

    for clase, datos in clases.items():
        rc = f"clases.{clase}"
        if clase not in CLASES:
            R.bloqueo("C01", rc, f"Tipo de activo desconocido (válidos: {', '.join(CLASES)})")
            continue
        if not isinstance(datos, dict):
            R.bloqueo("C01", rc, "La clase debe ser un objeto")
            continue
        for c in CAMPOS_CLASE:
            if c not in datos:
                R.bloqueo("C01", f"{rc}.{c}", "Campo obligatorio ausente")
        if datos.get("estado_semaforo") is not None and datos.get("estado_semaforo") not in ENUMS["estado_semaforo"]:
            R.bloqueo("C01", f"{rc}.estado_semaforo", f"Valor no permitido {datos.get('estado_semaforo')!r}")
        opciones = datos.get("opciones") if isinstance(datos.get("opciones"), list) else []
        n = len(opciones)
        total_opciones += n
        # C02
        if n > p["max_opciones_por_clase"]:
            R.bloqueo("C02", rc, f"{n} opciones (máximo {p['max_opciones_por_clase']})")
        rangos = [o.get("rango") for o in opciones if isinstance(o, dict)]
        if sorted(r for r in rangos if isinstance(r, int)) != list(range(1, n + 1)):
            R.bloqueo("C02", rc, f"Rangos {rangos} no son 1..{n} sin repeticiones")
        # C03
        if n < p["max_opciones_por_clase"] and _vacio(datos.get("menos_de_tres_motivo")):
            R.bloqueo("C03", rc, f"{n} opción(es) sin «menos_de_tres_motivo»")
        cand = datos.get("candidatas_analizadas")
        if isinstance(cand, int) and cand < n:
            R.bloqueo("C01", f"{rc}.candidatas_analizadas", f"{cand} candidatas analizadas < {n} opciones")
        # C14 semáforo
        sem = datos.get("estado_semaforo")
        if sem == "VERDE" and n == 0:
            R.advertencia("C14", rc, "Semáforo VERDE sin opciones")
        if sem == "GRIS" and n > 0:
            R.advertencia("C14", rc, "Semáforo GRIS con opciones propuestas")
        clusters = [o.get("cluster") for o in opciones if isinstance(o, dict) and o.get("cluster")]
        if len(clusters) == 3 and len(set(clusters)) == 1:
            R.advertencia("C05", rc, f"Las tres opciones comparten clúster «{clusters[0]}»: comprobar excepción de diversidad (9.6.3)")

        for i, op in enumerate(opciones):
            ro = f"{rc}.opciones[{i}]"
            if not isinstance(op, dict):
                R.bloqueo("C01", ro, "La opción debe ser un objeto")
                continue
            oid = op.get("opp_id") or f"#{i}"
            ro = f"{rc}.{oid}"
            if oid in ids_vistos:
                R.bloqueo("C01", ro, "opp_id duplicado en el paquete")
                if tipo_de_opp.get(oid) and tipo_de_opp[oid] != clase:
                    R.bloqueo("C16", ro, f"La misma oportunidad {oid} figura en {tipo_de_opp[oid]} y en {clase}")
            ids_vistos.add(oid)
            tipo_de_opp.setdefault(oid, clase)
            if op.get("tipo_activo") is not None and op.get("tipo_activo") != clase:
                R.bloqueo("C01", f"{ro}.tipo_activo", f"tipo_activo {op.get('tipo_activo')!r} distinto del tipo {clase} en el que figura")

            # C15 frontera con el Bloque B (2.4–2.5, R21)
            to = op.get("tipo_opcion")
            if not _vacio(to) and to not in TIPOS_OPCION:
                extra = f" ({TIPOS_OPCION_RETIRADOS[to]})" if to in TIPOS_OPCION_RETIRADOS else ""
                R.bloqueo("C15", f"{ro}.tipo_opcion", f"tipo_opcion {to!r} fuera de la granularidad permitida "
                                                      f"{'/'.join(TIPOS_OPCION)}{extra}: posible selección de activo concreto")
            amb = op.get("ambito")
            if not isinstance(amb, dict):
                R.bloqueo("C15", f"{ro}.ambito", "Sin delimitación del ámbito (incluye/excluye/región): posible selección de activo concreto")
            else:
                for k in ("incluye", "excluye", "region"):
                    if _vacio(amb.get(k)):
                        R.bloqueo("C15", f"{ro}.ambito.{k}", "Delimitación del ámbito incompleta")
            ind = op.get("indicador_seguimiento")
            if not isinstance(ind, dict) or _vacio(ind.get("nombre")):
                R.bloqueo("C15", f"{ro}.indicador_seguimiento", "Sin indicador de seguimiento del ámbito (PS3): posible selección de activo concreto")
            for c in CAMPOS_RETIRADOS:
                if c in op:
                    R.bloqueo("C15", f"{ro}.{c}", "Campo retirado en V5.0 (vehículos de implementación): la elección de instrumentos es del Bloque B")
            textos = [op.get("nombre"), op.get("nombre_llano"), op.get("tesis")] + (list(amb.values()) if isinstance(amb, dict) else [])
            isins = sorted({m for t in textos if isinstance(t, str) for m in RE_ISIN.findall(t) if es_isin(m)})
            if isins:
                R.bloqueo("C15", ro, f"Identificador de instrumento concreto (ISIN) en la opción: {', '.join(isins)}; "
                                     "los nombres concretos solo caben en «ejemplos_ilustrativos»")
            if "ejemplos_ilustrativos" in op and not isinstance(op["ejemplos_ilustrativos"], list):
                R.bloqueo("C01", f"{ro}.ejemplos_ilustrativos", "Debe ser una lista de textos")
            # C16 claves de duplicado
            kn = normalizar_texto(op.get("nombre"))
            if kn:
                claves_dup.setdefault("nombre:" + kn, []).append((clase, oid))
            ka = clave_ambito(op)
            if ka:
                claves_dup.setdefault("ambito:" + ka, []).append((clase, oid))
            if op.get("opp_id") and not str(op["opp_id"]).startswith("OPP-"):
                R.advertencia("C01", ro, "opp_id no sigue el formato OPP-")
            for c in CAMPOS_OPCION_NO_VACIOS:
                if c not in op:
                    R.bloqueo("C01", f"{ro}.{c}", "Campo obligatorio ausente")
                elif _vacio(op[c]) and not isinstance(op[c], (int, float)):
                    R.bloqueo("C01", f"{ro}.{c}", "Campo obligatorio vacío")
            for c in CAMPOS_OPCION_PRESENTES:
                if c not in op:
                    R.bloqueo("C01", f"{ro}.{c}", "Campo obligatorio ausente (puede ser lista vacía)")
            for c in ("relevancia_decisional", "reversibilidad", "liquidez", "siguiente_paso_sugerido", "confianza"):
                if c in op and not _vacio(op[c]) and op[c] not in ENUMS[c]:
                    R.bloqueo("C01", f"{ro}.{c}", f"Valor no permitido {op[c]!r}")
            r15 = op.get("riesgo_1a5")
            if "riesgo_1a5" in op and (isinstance(r15, bool) or not isinstance(r15, int) or not 1 <= r15 <= 5):
                R.bloqueo("C01", f"{ro}.riesgo_1a5", f"Debe ser entero 1–5 ({r15!r})")
            if isinstance(op.get("catalizadores"), list) and not op["catalizadores"]:
                R.advertencia("C01", f"{ro}.catalizadores", "Sin catalizadores identificados")

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
            entrada_ht03 = desgloses.get(oid) or (pu.get("desglose") if isinstance(pu.get("desglose"), dict) else None)
            if entrada_ht03:
                if "dimensiones" not in entrada_ht03:
                    entrada_ht03 = {"dimensiones": entrada_ht03}
                op_ht03 = {"opp_id": oid, "clase": clase, **entrada_ht03}
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
            inv = op.get("invertibilidad")
            if isinstance(inv, dict):
                if inv.get("universo_suficiente") is not True:
                    R.bloqueo("C05", f"{ro}.invertibilidad", "PS3: el ámbito no tiene un universo negociable suficiente y accesible")
                if _vacio(inv.get("nota")):
                    R.advertencia("C05", f"{ro}.invertibilidad.nota", "PS3 sin nota que justifique la invertibilidad del ámbito")
            elif "invertibilidad" in op:
                R.bloqueo("C01", f"{ro}.invertibilidad", "Debe ser un objeto {universo_suficiente, nota}")

            # C06 / C07 horizontes
            ofrecidos = _horizontes_ofrecidos(op)
            if not ofrecidos:
                R.bloqueo("C06", ro, "Ningún horizonte con contenido")
            for h, hv in ofrecidos.items():
                rh = f"{ro}.horizontes.{h}"
                if h not in HORIZONTES:
                    R.bloqueo("C06", rh, "Horizonte desconocido")
                    continue
                regla = TABLA_HORIZONTES[clase][h]
                if regla == "NO":
                    R.bloqueo("C06", rh, f"{h} no aplicable a {clase} (tabla 8.3)")
                elif regla == "LIMITADO":
                    if not op.get("catalizadores"):
                        R.bloqueo("C06", rh, f"{h} «limitado» en {clase}: exige catalizador identificado")
                    else:
                        R.advertencia("C06", rh, f"{h} «limitado» en {clase}: confirmar datos de frecuencia y liquidez suficientes")
                if _vacio(hv.get("prg_id")) or not str(hv.get("prg_id")).startswith("PRG-"):
                    R.bloqueo("C06", rh, "Horizonte sin pronóstico PRG- congelado (9.6.7, R11)")
                if h == "H1" and _vacio(hv.get("advertencia")):
                    R.advertencia("C06", rh, "H1 debe presentarse con la advertencia de menor fiabilidad (8.3)")
                prob = hv.get("prob")
                if prob is not None:
                    if isinstance(prob, bool) or not isinstance(prob, (int, float)) or not 0 <= prob <= 1:
                        R.bloqueo("C07", rh, f"Probabilidad no válida {prob!r} (0–1)")
                    cert = [c for c in certificados if c.get("clase") == clase and c.get("horizonte") == h
                            and c.get("vigente", True) and (not c.get("metodo") or not hv.get("metodo")
                                                             or c.get("metodo") == hv.get("metodo"))]
                    if not cert:
                        R.bloqueo("C07", rh, f"Probabilidad numérica sin certificado vigente para {clase}×{h}")
                else:
                    banda = str(hv.get("banda") or "").strip().lower()
                    if banda not in BANDAS_CUALITATIVAS:
                        R.advertencia("C07", rh, f"Banda «{hv.get('banda')}» fuera del vocabulario {BANDAS_CUALITATIVAS}")

            # C08 evidencias y cálculos
            ev_list = op.get("evidencias") if isinstance(op.get("evidencias"), list) else []
            ca_list = op.get("calculos") if isinstance(op.get("calculos"), list) else []
            if not ev_list or any(_vacio(x) for x in ev_list):
                R.bloqueo("C08", f"{ro}.evidencias", "Sin evidencias referenciadas (R7)")
            if not ca_list or any(_vacio(x) for x in ca_list):
                R.bloqueo("C08", f"{ro}.calculos", "Sin cálculos referenciados (R7)")
            for x in ev_list:
                if isinstance(x, str) and not re.match(r"^(CLM|EVD)-", x):
                    R.advertencia("C08", f"{ro}.evidencias", f"Identificador «{x}» no es CLM-/EVD-")
                if trazas is not None and isinstance(x, str) and x.startswith("CLM-") and not trazas.get(x):
                    R.bloqueo("C08", f"{ro}.evidencias", f"{x} sin EVD vinculada en F2")
            for x in ca_list:
                if isinstance(x, str) and not re.match(r"^CALC-", x):
                    R.advertencia("C08", f"{ro}.calculos", f"Identificador «{x}» no es CALC-")
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

            # C10 relevancia decisional
            vig = _es_vigente(op, vigentes)
            disparadores = relevancia_esperada_alta(op, clase, vig, p)
            rel = op.get("relevancia_decisional")
            if disparadores and rel != "ALTA":
                R.bloqueo("C10", ro, f"Relevancia «{rel}» pero la regla exige ALTA: {', '.join(disparadores)}")
            elif not disparadores and rel == "ALTA":
                R.advertencia("C10", ro, "ALTA sin disparador del Anexo A (sobrestimación conservadora)")
            elif rel == "BAJA" and not vig:
                R.advertencia("C10", ro, "BAJA en una opción nueva (BAJA se reserva a seguimiento o ajuste menor)")

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
                if b.get("tipo_activo") and b["tipo_activo"] != clase:
                    R.bloqueo("C11", f"{rb}.tipo_activo", f"{b['tipo_activo']} distinto del tipo de la opción ({clase})")
                hb = b.get("horizontes") if isinstance(b.get("horizontes"), list) else []
                for h in hb:
                    if h not in ofrecidos:
                        R.advertencia("C11", f"{rb}.horizontes", f"{h} no figura entre los horizontes de la opción")
                prg_op = {str(v.get("prg_id")) for v in ofrecidos.values()}
                for x in (b.get("pronosticos") if isinstance(b.get("pronosticos"), list) else []):
                    if x not in prg_op:
                        R.advertencia("C11", f"{rb}.pronosticos", f"{x} no es un pronóstico de la opción")
                for c in ("ambito", "indicador_seguimiento"):
                    if isinstance(b.get(c), dict) and isinstance(op.get(c), dict) and b[c] != op[c]:
                        R.advertencia("C11", f"{rb}.{c}", "Distinto del de la opción: el encargo debe transportar el mismo ámbito")
                for c in CAMPOS_RETIRADOS:
                    if c in b:
                        R.bloqueo("C15", f"{rb}.{c}", "Campo retirado en V5.0: el Bloque A no propone vehículos ni instrumentos")
    # C16 oportunidad duplicada en dos tipos (regla 5 de 2.6): nombre o ámbito normalizados
    for clave, lst in claves_dup.items():
        tipos = sorted({t for t, _ in lst})
        ids = sorted({o for _, o in lst})
        if len(ids) < 2:
            continue
        criterio = "nombre" if clave.startswith("nombre:") else "ámbito"
        if len(tipos) > 1:
            R.bloqueo("C16", f"clases.{'/'.join(tipos)}",
                      f"Oportunidad duplicada en dos tipos de activo por {criterio} normalizado «{clave.split(':', 1)[1]}»: {', '.join(ids)}")
        else:
            R.advertencia("C16", f"clases.{tipos[0]}", f"Dos opciones del mismo tipo con {criterio} normalizado idéntico: {', '.join(ids)}")
    for oid in bloque_b:
        if oid not in ids_vistos:
            R.bloqueo("C11", f"paquete_para_bloque_B.{oid}", "Entrada para una opción que no está en el paquete")

    # C14 apuestas independientes
    ai = paquete.get("apuestas_independientes")
    if ai is not None:
        if not isinstance(ai, int) or ai < 0:
            R.bloqueo("C01", "apuestas_independientes", f"Valor no válido {ai!r}")
        elif ai > total_opciones:
            R.advertencia("C14", "apuestas_independientes", f"{ai} apuestas independientes > {total_opciones} opciones")
        elif total_opciones > 0 and ai == 0:
            R.advertencia("C14", "apuestas_independientes", "0 apuestas independientes con opciones propuestas")

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
    ap = argparse.ArgumentParser(description="HT-09 · Validador determinista G3 del paquete_oportunidades")
    ap.add_argument("paquete", help="JSON del paquete_oportunidades (o paquete_sintesis)")
    ap.add_argument("--certificados", help="JSON: lista de certificados de horizonte [{clase, horizonte, vigente, metodo?}]")
    ap.add_argument("--informe-visual", help="Ruta del informe visual (HTML o texto) para HT-07")
    ap.add_argument("--desgloses", help="JSON {opp_id: entrada HT-03 (dimensiones, segunda_pasada, saturacion_narrativa)}")
    ap.add_argument("--parametros", help="JSON con parámetros vigentes de F10 (formato de HT-03)")
    ap.add_argument("--trazas", help="JSON {CLM-…: [EVD-…]} extraído de F2")
    ap.add_argument("--artefactos", help="JSON: lista de CALC- presentes en el Registro de cálculos")
    ap.add_argument("--umbral-fh", type=float, default=70.0)
    ap.add_argument("--salida", help="JSON de salida (por defecto, stdout)")
    a = ap.parse_args(argv)
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
