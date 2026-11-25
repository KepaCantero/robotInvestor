"""Alta por lotes de fichas revisadas por el custodio (Documento 0 §13.3, Anexo D)."""
from __future__ import annotations

import re
from datetime import date
from urllib.parse import urlsplit

from .contratos import RE_INYECCION, contiene_credenciales
from .herramientas import ht02
from .mantenimiento_fuentes import bajas_registradas, publicar, puntuar_referencia
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


def incorporar(ruta, archivo, lote, cfg=None, *, fecha_corte=None, registro_f9=None):
    original = ruta.read_text(encoding="utf-8")
    lineas = original.splitlines(keepends=True)
    pref, tax = PREFIJOS[archivo]
    ids = {f.id for f in ht02.leer_fichas(lineas)}
    bajas = {rid for rid, _ in bajas_registradas(lineas, ruta)}
    if archivo == "F9" and registro_f9 is not None and registro_f9.is_file():
        bajas.update(rid for rid, _ in bajas_registradas(registro_f9.read_text(encoding="utf-8").splitlines(), registro_f9))
    corte = fecha_corte if fecha_corte is not None else date.today()
    if not isinstance(lote, list) or not lote:
        raise ValueError("Se requiere una lista de altas")
    for a in lote:
        if not isinstance(a, dict):
            raise TypeError("Cada alta debe ser una ficha")
        rid, tema = a.get("id"), a.get("tematica")
        if not isinstance(rid, str) or not isinstance(tema, str):
            raise TypeError("La ficha necesita un identificador y una temática")
        if rid in bajas:
            raise ValueError(f"Identificador dado de baja: {rid}")
        q = puntuar_referencia(a.get("puntos"), archivo, cfg)
        if "q" in a and (type(a["q"]) is not int or a["q"] != q):
            raise ValueError("La Q declarada debe ser entera y coincidir con la suma de los siete criterios")
        if not re.fullmatch(pref + r"-\d+", rid) or rid in ids:
            raise ValueError("Identificador repetido o ajeno al catálogo")
        if not re.fullmatch(tax + r"-\d{2}", tema):
            raise ValueError("Temática o Q incorrecta")
        titulo, url = a.get("titulo"), a.get("url")
        if any(not isinstance(v, str) or not v.strip() or v.splitlines() != [v] for v in (titulo, url)):
            raise ValueError("Título o enlace incorrecto")
        if not re.fullmatch(r"""https?://[^\s<>()\[\]"'`]+""", url):
            raise ValueError("El enlace debe ser una URL HTTP(S) sin espacios ni marcado")
        enlace = urlsplit(url)
        if not enlace.hostname or enlace.username or enlace.password or contiene_credenciales(a) or RE_INYECCION.search(titulo):
            raise ValueError("Ficha rechazada por origen o por contenido")
        tipologia = a.get("tipologia")
        if tipologia not in ("primaria", "secundaria", "terciaria"):
            raise ValueError("La tipología debe ser primaria, secundaria o terciaria")
        fecha = date.fromisoformat(a["fecha_publicacion"])
        if fecha > corte:
            raise ValueError("Publicación posterior a la fecha de la instancia")
        nivel = nivel_de_q(q, cfg)
        unica = a.get("unica_fuente_de")
        if "unica_fuente_de" in a and (nivel != "D" or not isinstance(unica, str) or not unica.strip()
                or unica.splitlines() != [unica] or RE_INYECCION.search(unica)):
            raise ValueError("La excepción de fuente única requiere una ficha D y un dato necesario en una línea")
        inicio = [i for i, l in enumerate(lineas) if re.match(rf"^## {tema}(?:\s|$)", l)]
        if len(inicio) != 1:
            raise ValueError("Sección temática ausente o ambigua")
        fin = next((i for i in range(inicio[0]+1, len(lineas)) if re.match(r"^#{1,2} ", lineas[i])), len(lineas))
        clave = (-q, -fecha.toordinal(), rid)
        pos = next((f.linea_inicio for f in ht02.leer_fichas(lineas) if inicio[0] < f.linea_inicio < fin and clave < clave_orden(f)), fin)
        campos = [f"#### {rid} · Q {q} ({nivel}) — {titulo}", "", f"- **Temática:** {tema}", f"- **Calidad Q:** {q} ({nivel}) — {a['puntos']}",
                  f"- **Tipología:** {tipologia}",
                  f"- **Fecha de publicación:** {fecha}", f"- **Año:** {fecha.year}", f"- **URL:** {url}", "- **Estado del enlace:** PENDIENTE_BARRIDO"]
        if nivel == "D":
            seguimiento = f"única fuente de un dato necesario: {unica.strip()}" if unica else "candidata a baja"
            campos.append(f"- **Seguimiento:** {seguimiento}")
        lineas[pos:pos] = ["\n", *(c+"\n" for c in campos), "\n"]
        ids.add(rid)
    publicar(ruta, original, "".join(lineas))
