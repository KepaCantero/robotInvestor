"""SC-3 — registro del Motor numérico (código de referencia V0.33, T-26 parte 1).

La Constitución (§9.3 y tabla de servicios) pide que las cifras las calcule el Motor y que cada agente cite el ID del
artefacto; cada módulo declara su modelo y sus límites de validez, y el cálculo es reproducible (hash, semilla, fecha de
corte). Este módulo no calcula: define qué es un modelo declarado y un artefacto registrado, y comprueba (V-26) que las
cifras de un sobre citan artefactos que existen, con su modelo y sin datos posteriores al corte del sobre.
Determinista, sin LLM y sin reloj.
"""
from __future__ import annotations

import hashlib
import json
import re

VERSION_SC3 = "SC3-0.1.0"
_ID = re.compile(r"^[A-Za-z0-9._:/-]{1,64}\Z")
_VER = re.compile(r"^\d+\.\d+\.\d+\Z")
_HASH = re.compile(r"^[0-9a-f]{64}\Z")
_SELLO = re.compile(r"^K-\d{8}-\d{3}\Z")
CLAVES_MODELO = {"modelo_ref", "version", "descripcion", "limites_validez"}
CLAVES_ARTEFACTO = {"artefacto_id", "modelo_ref", "version_modelo", "sello_ref", "semilla", "entradas_hash", "resultado_hash"}


def _texto(x, n=300):
    return isinstance(x, str) and x.strip() == x and 0 < len(x) <= n


def huella(x) -> str:
    return hashlib.sha256(json.dumps(x, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()


def modelo_fallo(m):
    """Motivo por el que un modelo declarado no vale, o None. Un modelo declara qué es y dónde deja de valer."""
    if not (isinstance(m, dict) and set(m) == CLAVES_MODELO):
        return f"un modelo declara exactamente {sorted(CLAVES_MODELO)}"
    if not (isinstance(m["modelo_ref"], str) and _ID.match(m["modelo_ref"])):
        return "modelo_ref mal formado"
    if not (isinstance(m["version"], str) and _VER.match(m["version"])):
        return "versión del modelo mal formada (x.y.z)"
    if not _texto(m["descripcion"]):
        return "descripción vacía o demasiado larga"
    if not _texto(m["limites_validez"], 500):
        return "límites de validez vacíos: un modelo sin límites declarados no se registra"
    return None


def artefacto_fallo(a):
    """Motivo por el que un artefacto no vale (forma), o None. La coherencia con modelos y sellos la comprueba el registro."""
    if not (isinstance(a, dict) and set(a) == CLAVES_ARTEFACTO):
        return f"un artefacto declara exactamente {sorted(CLAVES_ARTEFACTO)}"
    if not all(isinstance(a[k], str) and _ID.match(a[k]) for k in ("artefacto_id", "modelo_ref")):
        return "artefacto_id o modelo_ref mal formados"
    if not (isinstance(a["version_modelo"], str) and _VER.match(a["version_modelo"])):
        return "version_modelo mal formada"
    if not (isinstance(a["sello_ref"], str) and _SELLO.match(a["sello_ref"])):
        return "sello_ref no es un sello de K (fecha de corte del cálculo)"
    s = a["semilla"]
    if s is not None and not (isinstance(s, int) and not isinstance(s, bool) and 0 <= s < 2 ** 63):
        return "semilla: null (cálculo sin azar) o un entero no negativo"
    if not all(isinstance(a[k], str) and _HASH.match(a[k]) for k in ("entradas_hash", "resultado_hash")):
        return "entradas_hash y resultado_hash son sha256 en hexadecimal"
    return None


def _cifras(x, ruta="payload"):
    """Las Cifras del sobre (objetos con estado y valor) con su ruta."""
    if isinstance(x, dict):
        if "estado" in x and "valor" in x:
            yield ruta, x
        for k, v in x.items():
            yield from _cifras(v, f"{ruta}.{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from _cifras(v, f"{ruta}[{i}]")


def vista_ok(vista):
    """La vista del registro que recibe el validador: {artefacto_id: {modelo_ref, fecha_corte, sello_ref}}."""
    return isinstance(vista, dict) and all(
        isinstance(k, str) and isinstance(v, dict) and {"modelo_ref", "fecha_corte", "sello_ref"} <= set(v)
        and all(isinstance(v[c], str) for c in ("modelo_ref", "fecha_corte", "sello_ref")) for k, v in vista.items())


def fallos_sobre(sobre, vista, fecha_corte, cifras=None, sello=None):
    """V-26: (ruta, mensaje) por cada cita del sobre que el registro SC-3 no respalda. `vista` = {artefacto_id: {modelo_ref,
    fecha_corte, sello_ref}}; `fecha_corte` = la del sobre; `sello` = el sello de K del encargo (si se conoce, el artefacto
    debe ser de ese sello: revisión T-26, G1). Toda cifra VERIFICADO o ESTIMADO cita un artefacto registrado (G2). No lanza:
    una entrada mal formada sale como una sola cita no respaldada."""
    try:
        return _fallos_sobre(sobre, vista, fecha_corte, cifras, sello)
    except (KeyError, TypeError, AttributeError, ValueError) as e:
        return [("(interno)", f"sobre o registro del Motor mal formados: {type(e).__name__}")]


def _fallos_sobre(sobre, vista, fecha_corte, cifras, sello):
    p = sobre["payload"]
    out = []

    def respaldo(aid):
        art = vista.get(aid)
        if art is None:
            return f"{aid} no está registrado en el Motor (SC-3)"
        if sello is not None and art["sello_ref"] != sello:
            return f"{aid} se calculó con el sello {art['sello_ref']}, no con el del encargo ({sello})"
        if art["fecha_corte"] > fecha_corte:
            return f"{aid} se calculó con datos de {art['fecha_corte']}, posteriores al corte del sobre ({fecha_corte})"
        return None
    citados = (p.get("referencias") or {}).get("artefactos_motor") or []
    for i, aid in enumerate(citados):
        m = respaldo(aid)
        if m:
            out.append((f"payload.referencias.artefactos_motor[{i}]", m))
    for ruta, c in (cifras if cifras is not None else _cifras(p)):
        if c.get("estado") not in ("VERIFICADO", "ESTIMADO"):
            continue
        aid = c.get("motor_id")
        m = respaldo(aid) if isinstance(aid, str) else "la cifra no cita ningún artefacto del Motor"
        if m:
            if aid not in citados:   # las citadas ya se informaron arriba
                out.append((ruta, m))
        elif vista[aid]["modelo_ref"] != c.get("modelo_ref"):
            out.append((ruta, f"la cifra cita el modelo {c.get('modelo_ref')!r} y el artefacto {aid} es de {vista[aid]['modelo_ref']!r}"))
    return out
