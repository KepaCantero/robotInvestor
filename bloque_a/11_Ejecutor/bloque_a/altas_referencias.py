"""Alta por lotes de fichas revisadas por el custodio (Documento 0 §13.3, Anexo D)."""
from __future__ import annotations

import re
from datetime import date
from urllib.parse import urlsplit

from .contratos import RE_INYECCION, contiene_credenciales
from .herramientas import ht02
from .mantenimiento_fuentes import publicar
from .referencias import _anio, nivel_de_q

PREFIJOS = {"F7": ("ANA-DOC", "TA"), "F8": ("DOC-MOT", "TM"), "F9": ("RF", "TF")}


def clave_orden(ficha):
    fecha = ficha.campo("Fecha de publicación")
    if fecha:
        try:
            return (-(ficha.q or 0), -date.fromisoformat(fecha).toordinal(), ficha.id)
        except ValueError:
            pass
    anio = _anio(ficha)
    return (-(ficha.q or 0), -date(anio, 1, 1).toordinal() if anio else 0, ficha.id)


def incorporar(ruta, archivo, lote, cfg=None):
    original = ruta.read_text(encoding="utf-8")
    lineas = original.splitlines(keepends=True)
    pref, tax = PREFIJOS[archivo]
    ids = {f.id for f in ht02.leer_fichas(lineas)}
    if not isinstance(lote, list) or not lote:
        raise ValueError("Se requiere una lista de altas")
    for a in lote:
        rid, tema, q = a["id"], a["tematica"], a["q"]
        if not re.fullmatch(pref + r"-\d+", rid) or rid in ids:
            raise ValueError("Identificador repetido o ajeno al catálogo")
        if not re.fullmatch(tax + r"-\d{2}", tema) or type(q) is not int or not 0 <= q <= 100:
            raise ValueError("Temática o Q incorrecta")
        titulo, url = a["titulo"], a["url"]
        if any(not isinstance(v, str) or not v.strip() or len(v.splitlines()) != 1 for v in (titulo, url)):
            raise ValueError("Título o enlace incorrecto")
        enlace = urlsplit(url)
        if enlace.scheme not in ("https", "http") or not enlace.hostname or enlace.username or enlace.password or contiene_credenciales(a) or RE_INYECCION.search(titulo):
            raise ValueError("Ficha rechazada por origen o por contenido")
        fecha = date.fromisoformat(a["fecha_publicacion"])
        nivel = nivel_de_q(q, cfg)
        inicio = [i for i, l in enumerate(lineas) if re.match(rf"^## {tema}(?:\s|$)", l)]
        if len(inicio) != 1:
            raise ValueError("Sección temática ausente o ambigua")
        fin = next((i for i in range(inicio[0]+1, len(lineas)) if re.match(r"^#{1,2} ", lineas[i])), len(lineas))
        clave = (-q, -fecha.toordinal(), rid)
        pos = next((f.linea_inicio for f in ht02.leer_fichas(lineas) if inicio[0] < f.linea_inicio < fin and clave < clave_orden(f)), fin)
        campos = [f"#### {rid} · Q {q} ({nivel}) — {titulo}", "", f"- **Temática:** {tema}", f"- **Calidad Q:** {q} ({nivel})",
                  f"- **Fecha de publicación:** {fecha}", f"- **Año:** {fecha.year}", f"- **URL:** {url}", "- **Estado del enlace:** PENDIENTE_VERIFICACION_ALTA"]
        if nivel == "D":
            campos.append("- **Seguimiento:** candidata a baja")
        lineas[pos:pos] = ["\n", *(c+"\n" for c in campos), "\n"]
        ids.add(rid)
    publicar(ruta, original, "".join(lineas))
