"""Contratos CT-B: campos comunes (6.2 y Anexo B), saneamiento de contenido externo (R12), detección de credenciales y
datos personales (R10, R11), extracción y validación mínima de las respuestas JSON de los agentes."""
from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional, Tuple

VERSION_CONTRATO = "2.1"
ESTADOS_RETORNO = ("COMPLETO", "PARCIAL", "SIN_RESULTADO", "RECHAZADO", "EN_PAUSA")

RE_INSTRUCCION = re.compile(
    r"(ignora(?:r)? (?:las |todas las |tus )?instrucciones[^.\n]*|ignore (?:all |the )?(?:previous |prior )?instructions[^.\n]*|"
    r"system prompt[^.\n]*|act[uú]a como[^.\n]*|you are now[^.\n]*|nuevas instrucciones:[^\n]*|"
    r"ejecuta (?:la herramienta|el comando)[^.\n]*|<\s*/?\s*(?:system|tool_use|instrucciones)\s*>)", re.IGNORECASE)
RE_SECRETO = re.compile(r"(sk-ant-[A-Za-z0-9_\-]{8,}|sk-trampa-[A-Za-z0-9\-]{6,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|"
                        r"api[_-]?key\s*[:=]\s*\S{6,}|bearer\s+[A-Za-z0-9\-_.=]{16,}|password\s*[:=]\s*\S+)", re.IGNORECASE)
RE_PERSONAL = re.compile(r"(\b[A-Z]{2}\d{2}(?:\s?\d{4}){4,7}\b|[\w.+-]+@[\w-]+\.[\w.-]+|\b\d{8}[A-HJ-NP-TV-Z]\b|"
                         r"\b[XYZ]\d{7}[A-Z]\b|\+34\s?\d{3}\s?\d{3}\s?\d{3})")
RE_CARTERA = re.compile(r"\b(mi|nuestra) cartera\b|\bmi perfil\b|\bcu[aá]nto (debo|deber[ií]a) (comprar|invertir)\b|"
                        r"\btama[ñn]o de (mi|la) posici[oó]n\b", re.IGNORECASE)


class MensajeRechazado(ValueError):
    """Mensaje con credenciales, claves o datos personales: se rechaza íntegro (6.2.5)."""

    def __init__(self, motivo: str, tipo: str) -> None:
        super().__init__(motivo)
        self.tipo = tipo


def comprobar_sensibles(obj: Any) -> None:
    texto = json.dumps(obj, ensure_ascii=False, default=str)
    if RE_SECRETO.search(texto):
        raise MensajeRechazado("El mensaje contiene una credencial o clave (no se reproduce)", "CREDENCIAL")
    if RE_PERSONAL.search(texto):
        raise MensajeRechazado("El mensaje contiene datos personales", "DATOS_PERSONALES")


def sanear(obj: Any, incidencias: Optional[List[str]] = None) -> Any:
    """Neutraliza instrucciones incrustadas en contenido transportado (R12): se sustituyen por un marcador."""
    if isinstance(obj, str):
        if RE_INSTRUCCION.search(obj):
            if incidencias is not None:
                incidencias.append(obj[:80])
            return RE_INSTRUCCION.sub("[INSTRUCCION_INCRUSTADA_RETIRADA]", obj)
        return obj
    if isinstance(obj, dict):
        return {k: sanear(v, incidencias) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanear(v, incidencias) for v in obj]
    return obj


def mensaje(contrato: str, emisor: str, receptor: str, pet_id: Optional[str], run_id: Optional[str], cuerpo: Dict,
            msg_id: str, timestamp: str, presupuesto: Optional[Dict] = None) -> Dict:
    m = {"msg_id": msg_id, "contrato": contrato, "version_contrato": VERSION_CONTRATO, "emisor": emisor, "receptor": receptor,
         "pet_id": pet_id, "run_id": run_id, "timestamp": timestamp}
    if presupuesto:
        m["presupuesto"] = presupuesto
    m.update(cuerpo)
    return m


def extraer_json(texto: str) -> Optional[Dict]:
    t = texto.strip()
    if t.startswith("```"):
        t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t)
    try:
        d = json.loads(t)
        return d if isinstance(d, dict) else None
    except json.JSONDecodeError:
        pass
    ini, fin = t.find("{"), t.rfind("}")
    if ini >= 0 and fin > ini:
        try:
            d = json.loads(t[ini:fin + 1])
            return d if isinstance(d, dict) else None
        except json.JSONDecodeError:
            return None
    return None


def validar_minimo(d: Dict, esquema: Dict) -> Tuple[bool, List[str]]:
    """Comprobación ligera: claves obligatorias del esquema mínimo y tipos de primer nivel."""
    errores = []
    for k in esquema.get("required", []):
        if k not in d:
            errores.append(f"falta «{k}»")
    for k, sub in (esquema.get("properties") or {}).items():
        if k in d and "type" in sub:
            tipos = sub["type"] if isinstance(sub["type"], list) else [sub["type"]]
            mapa = {"object": dict, "array": list, "string": str, "number": (int, float), "integer": int, "boolean": bool,
                    "null": type(None)}
            if not any(isinstance(d[k], mapa[t]) for t in tipos if t in mapa):
                errores.append(f"«{k}» no es {tipos}")
    return (not errores), errores


def esquema(requeridos: Dict[str, str]) -> Dict:
    return {"type": "object", "required": list(requeridos), "properties": {k: {"type": v} for k, v in requeridos.items()}}


# Campos que solo pueden tomar valores controlados (Anexo D.5)
VOCAB = {
    "etiqueta": ("[HECHO]", "[INTERPRETACIÓN]", "[ESPECULACIÓN]"),
    "clase_cifra": ("determinista", "estimacion_estadistica", "juicio_experto"),
    "estado_hipotesis": ("confirmada", "debilitada", "indeterminada", "invalidada"),
    "estado_regimen": ("definido", "mixto", "incierto", "en_transicion"),
    "fuerza": ("fuerte", "moderada", "debil"),
    "veredicto_tesis": ("robusta", "fragil", "refutada"),
    "confianza": ("alta", "media", "baja"),
    "severidad": ("Crítica", "Material", "Operativa", "Menor"),
}


def controlado(valor: Any, campo: str, defecto: str) -> str:
    v = str(valor or "").strip()
    for x in VOCAB[campo]:
        if v.lower() == x.lower() or v.lower().strip("[]") == x.lower().strip("[]"):
            return x
    if campo == "etiqueta":
        lv = v.lower()
        if "hecho" in lv:
            return "[HECHO]"
        if "interpret" in lv:
            return "[INTERPRETACIÓN]"
        if "especul" in lv:
            return "[ESPECULACIÓN]"
    if campo == "veredicto_tesis" and v.lower() in ("frágil",):
        return "fragil"
    return defecto


def multiplo10(v: Any, defecto: Any = 50) -> Any:
    if v in ("NA", "NE"):
        return v
    try:
        x = float(v)
    except (TypeError, ValueError):
        return defecto
    return int(max(0, min(100, round(x / 10.0) * 10)))
