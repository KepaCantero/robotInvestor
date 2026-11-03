#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HT-02 · Verificador de enlaces y contenido (implementación de referencia).

Bloque B · Robot Investor · V2.0 · 03/11/2026 · Subordinado al Documento 0 del
Bloque B, óptima V2.0 (secciones 4.4, 5.2, 13.4, 13.5 y Anexo A). Copia de la
implementación de referencia del Bloque A (óptima V5.0): solo cambia esta
cabecera. Lee las fichas de F7 (ANA-DOC-, MBA-), F8 (DOC-MOT-, MBM-), F9 (MBF-)
y del Fondo metodológico con el mismo formato «#### ID · Q nn (N) — Título».

Lee un archivo de referencias (F7, F8 o F9) con fichas del tipo

    #### ANA-DOC-0001 · Q 85 (A) — Título
    - **URL:** https://…
    - **DOI:** 10.1111/…
    - **Estado del enlace:** OK
    - **Última verificación:** 2026-10-25

comprueba cada URL/DOI (HEAD y GET con tiempo límite y reintentos, resolución
de DOI por https://doi.org/, redirecciones, 4xx/5xx, muro de pago heurístico,
retractaciones heurísticas, hash de contenido normalizado y similitud frente a
la huella anterior, copia en Wayback) y produce un informe JSON + CSV con el
estado (OK, REDIRIGIDO, ROTO, MURO_PAGO, CONTENIDO_CAMBIADO) y la acción
sugerida (REPARAR, DEGRADAR, BORRAR, NINGUNA).

Opciones de escritura sobre el markdown:
  --aplicar                 actualiza «Estado del enlace», «Última verificación»,
                            «Primer fallo», «Hash de contenido», «Huella de
                            contenido» y, si estaba vacía, «Copia archivada».
  --borrar ID --motivo TXT  elimina la ficha y añade la línea al «Registro de
                            bajas» (REF-id, título, motivo, fecha, sustituta).

Campos reconocidos (todos opcionales salvo URL o DOI): URL, DOI, Estado del
enlace, Última verificación, Primer fallo, Hash de contenido, Huella de
contenido, Copia archivada, Último uso, Evidencias.

Similitud de contenido: se guarda SHA-256 del texto normalizado y una huella
SimHash de 64 bits (Charikar, 2002) sobre tríos de palabras; la similitud es
1 − distancia de Hamming/64 y se compara con el umbral del Anexo A (0,8).
Es una aproximación de la similitud textual que no exige guardar el texto.

ROTO exige dos intentos fallidos separados ≥ 24 h (13.4): el primer fallo se
anota en «Primer fallo»; un fallo posterior ≥ 24 h lo confirma; si el primer
fallo tiene ≥ 7 días (dos barridos semanales) y no hay alternativa, se sugiere
BORRAR. Un acierto intermedio borra «Primer fallo».

Solo biblioteca estándar (usa ht07_legibilidad para extraer texto visible).
Estado de madurez (R22): implementada (referencia), pruebas unitarias
superadas; pendiente de integración.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import csv
import datetime as dt
import hashlib
import io
import json
import re
import socket
import ssl
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

try:
    from ht07_legibilidad import extraer_texto_html
except ImportError:  # pragma: no cover - ejecución desde otra ruta
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from ht07_legibilidad import extraer_texto_html

VERSION = "4.0"
USER_AGENT = "RobotInvestor-BloqueA-HT02/4.0 (verificador de referencias; +sin datos personales)"
ESTADOS = ("OK", "REDIRIGIDO", "ROTO", "MURO_PAGO", "CONTENIDO_CAMBIADO")
ACCIONES = ("REPARAR", "DEGRADAR", "BORRAR", "NINGUNA")
PRECEDENCIA = {"ROTO": 5, "MURO_PAGO": 4, "CONTENIDO_CAMBIADO": 3, "REDIRIGIDO": 2, "OK": 1}

RE_FICHA = re.compile(r"^####\s+(?P<id>[^\s·—]+)(?:\s*·\s*Q\s*(?P<q>\d{1,3})\s*\((?P<nivel>[A-D])\))?\s*—\s*(?P<titulo>.+?)\s*$")
RE_CAMPO = re.compile(r"^(?P<pre>\s*[-*]\s+\*\*)(?P<campo>[^*]+?):\*\*(?P<sep>\s*)(?P<valor>.*?)\s*$")
RE_TITULO = re.compile(r"^(#{1,6})\s")

MARCAS_MURO = [
    "subscribe to read", "subscribe to continue", "subscribers only", "subscription required",
    "purchase this article", "buy this article", "buy article", "purchase pdf", "rent this article",
    "access through your institution", "get access", "log in to read", "sign in to read",
    "to continue reading", "already a subscriber", "this content is for subscribers",
    "suscríbete para leer", "suscríbete para seguir leyendo", "contenido exclusivo para suscriptores",
    "solo para suscriptores", "hazte suscriptor", "inicia sesión para leer", "compra este artículo",
    "paywall",
]
MARCAS_RETRACTACION = [
    "this article has been retracted", "retraction notice", "notice of retraction", "retracted article",
    "retraction:", "this paper has been withdrawn", "this article has been withdrawn",
    "artículo retractado", "nota de retractación", "este artículo ha sido retractado",
]
MARCAS_SOFT404 = ["404", "page not found", "página no encontrada", "not found", "no se ha encontrado la página"]


# ---------------------------------------------------------------------------
# Lectura del markdown
# ---------------------------------------------------------------------------
@dataclass
class Ficha:
    id: str
    titulo: str
    q: Optional[int]
    nivel: Optional[str]
    linea_inicio: int  # índice de la cabecera
    linea_fin: int  # índice exclusivo
    campos: Dict[str, str] = field(default_factory=dict)
    lineas_campo: Dict[str, int] = field(default_factory=dict)

    def campo(self, *nombres: str) -> Optional[str]:
        norm = {_norm_clave(k): v for k, v in self.campos.items()}
        for n in nombres:
            v = norm.get(_norm_clave(n))
            if v is not None and _valor_util(v):
                return v
        return None


def _norm_clave(s: str) -> str:
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", s.strip().lower())


def _valor_util(v: str) -> bool:
    return bool(v.strip()) and v.strip().lower() not in ("—", "-", "–", "n/d", "nd", "no disponible", "ninguno", "ninguna", "null")


def leer_fichas(lineas: List[str]) -> List[Ficha]:
    fichas: List[Ficha] = []
    actual: Optional[Ficha] = None
    for i, ln in enumerate(lineas):
        m = RE_FICHA.match(ln.rstrip("\n"))
        if m or RE_TITULO.match(ln):
            if actual:
                actual.linea_fin = i
                fichas.append(actual)
                actual = None
            if m:
                actual = Ficha(id=m.group("id"), titulo=m.group("titulo"),
                               q=int(m.group("q")) if m.group("q") else None,
                               nivel=m.group("nivel"), linea_inicio=i, linea_fin=len(lineas))
            continue
        if actual:
            mc = RE_CAMPO.match(ln.rstrip("\n"))
            if mc:
                actual.campos[mc.group("campo").strip()] = mc.group("valor").strip()
                actual.lineas_campo[_norm_clave(mc.group("campo"))] = i
    if actual:
        actual.linea_fin = len(lineas)
        fichas.append(actual)
    return fichas


def extraer_url(valor: Optional[str]) -> Optional[str]:
    if not valor:
        return None
    m = re.search(r"\((https?://[^)\s]+)\)", valor) or re.search(r"<(https?://[^>\s]+)>", valor) \
        or re.search(r"(https?://[^\s<>)\]]+)", valor)
    return m.group(1).rstrip(".,;") if m else None


def extraer_doi(valor: Optional[str]) -> Optional[str]:
    if not valor:
        return None
    m = re.search(r"(10\.\d{4,9}/[^\s<>\"]+)", valor)
    return m.group(1).rstrip(".,;)") if m else None


def _fecha(valor: Optional[str]) -> Optional[dt.date]:
    if not valor:
        return None
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", valor)
    if m:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.search(r"(\d{2})/(\d{2})/(\d{4})", valor)
    if m:
        return dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    return None


# ---------------------------------------------------------------------------
# Contenido: normalización, hash y SimHash
# ---------------------------------------------------------------------------
def normalizar_contenido(cuerpo: bytes, content_type: str) -> str:
    charset = "utf-8"
    m = re.search(r"charset=([\w-]+)", content_type or "", re.I)
    if m:
        charset = m.group(1)
    try:
        texto = cuerpo.decode(charset, errors="replace")
    except LookupError:
        texto = cuerpo.decode("utf-8", errors="replace")
    if "html" in (content_type or "").lower() or re.search(r"<\s*(html|body|p|div)\b", texto[:3000], re.I):
        texto = extraer_texto_html(texto)
    texto = unicodedata.normalize("NFKC", texto).lower()
    tokens = [t for t in re.findall(r"\w+", texto) if not re.search(r"\d", t)]  # fuera fechas y contadores
    return " ".join(tokens)


def sha256_texto(texto: str) -> str:
    return "sha256:" + hashlib.sha256(texto.encode("utf-8")).hexdigest()


def simhash64(texto: str) -> str:
    palabras = texto.split()
    tejas = [" ".join(palabras[i:i + 3]) for i in range(max(1, len(palabras) - 2))] if palabras else []
    v = [0] * 64
    for t in tejas:
        h = int.from_bytes(hashlib.blake2b(t.encode("utf-8"), digest_size=8).digest(), "big")
        for b in range(64):
            v[b] += 1 if (h >> b) & 1 else -1
    huella = sum(1 << b for b in range(64) if v[b] > 0)
    return f"simhash64:{huella:016x}"


def similitud_simhash(a: str, b: str) -> Optional[float]:
    try:
        x = int(a.split(":", 1)[1], 16)
        y = int(b.split(":", 1)[1], 16)
    except (IndexError, ValueError):
        return None
    return round(1 - bin(x ^ y).count("1") / 64, 4)


def detectar_muro_pago(texto_bajo: str, codigo: Optional[int], crudo: str) -> Tuple[bool, List[str]]:
    indicios = [m for m in MARCAS_MURO if m in texto_bajo]
    if re.search(r'"isAccessibleForFree"\s*:\s*"?(false|False)', crudo):
        indicios.append("isAccessibleForFree=false")
    if codigo == 402:
        return True, ["HTTP 402"] + indicios
    if codigo in (401, 403) and indicios:
        return True, [f"HTTP {codigo}"] + indicios
    fuerte = "isAccessibleForFree=false" in indicios
    return (fuerte or len(set(indicios)) >= 2), indicios


def detectar_retractacion(texto_bajo: str) -> List[str]:
    return [m for m in MARCAS_RETRACTACION if m in texto_bajo]


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------
@dataclass
class Config:
    timeout: float = 15.0
    reintentos: int = 2
    espera_base: float = 1.0
    max_bytes: int = 2_000_000
    doi_base: str = "https://doi.org/"
    wayback_api: str = "https://archive.org/wayback/available"
    wayback: str = "incidencias"  # siempre | incidencias | nunca
    usar_proxy_entorno: bool = True
    ca_bundle: Optional[str] = None
    umbral_similitud: float = 0.8
    dias_confirmacion_roto: int = 1
    dias_entre_barridos: int = 7
    dias_sin_uso_baja: int = 180
    q_baja: int = 50
    descargar_contenido: bool = True


class _Redirecciones(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        super().__init__()
        self.cadena: List[Dict] = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.cadena.append({"codigo": code, "url": newurl})
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _es_local(url: str) -> bool:
    host = (urllib.parse.urlsplit(url).hostname or "").lower()
    return host in ("localhost", "127.0.0.1", "::1") or host.endswith(".localhost")


def _peticion(url: str, metodo: str, cfg: Config) -> Dict:
    red = _Redirecciones()
    handlers: List = [red]
    if not cfg.usar_proxy_entorno or _es_local(url):
        handlers.append(urllib.request.ProxyHandler({}))
    if url.lower().startswith("https"):
        ctx = ssl.create_default_context(cafile=cfg.ca_bundle) if cfg.ca_bundle else ssl.create_default_context()
        handlers.append(urllib.request.HTTPSHandler(context=ctx))
    opener = urllib.request.build_opener(*handlers)
    req = urllib.request.Request(url, method=metodo, headers={
        "User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml,application/pdf;q=0.9,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8"})
    out = {"metodo": metodo, "codigo": None, "url_final": url, "redirecciones": red.cadena, "error": None,
           "content_type": "", "cuerpo": b""}
    try:
        with opener.open(req, timeout=cfg.timeout) as r:
            out["codigo"] = r.status
            out["url_final"] = r.geturl()
            out["content_type"] = r.headers.get("Content-Type", "")
            if metodo == "GET":
                out["cuerpo"] = r.read(cfg.max_bytes)
    except urllib.error.HTTPError as e:
        out["codigo"] = e.code
        out["url_final"] = e.geturl() or url
        out["content_type"] = e.headers.get("Content-Type", "") if e.headers else ""
        if metodo == "GET":
            try:
                out["cuerpo"] = e.read(cfg.max_bytes)
            except Exception:  # noqa: BLE001
                pass
    except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, ssl.SSLError, ValueError, OSError) as e:
        razon = getattr(e, "reason", e)
        out["error"] = f"{type(e).__name__}: {razon}"
    return out


def _reintentable(r: Dict) -> bool:
    return r["error"] is not None or (r["codigo"] is not None and (r["codigo"] >= 500 or r["codigo"] in (408, 429)))


def _con_reintentos(url: str, metodo: str, cfg: Config) -> Tuple[Dict, int]:
    intentos = 0
    r: Dict = {}
    for k in range(cfg.reintentos + 1):
        intentos += 1
        r = _peticion(url, metodo, cfg)
        if not _reintentable(r):
            break
        if k < cfg.reintentos and cfg.espera_base > 0:
            time.sleep(cfg.espera_base * (2 ** k))
    return r, intentos


def comprobar_url(url: str, cfg: Config) -> Dict:
    """HEAD y, si procede, GET. Devuelve la observación cruda de la URL."""
    head, n1 = _con_reintentos(url, "HEAD", cfg)
    obs = {"url": url, "head_codigo": head["codigo"], "intentos": n1, "error": head["error"]}
    necesita_get = cfg.descargar_contenido or head["codigo"] is None or head["codigo"] >= 400
    final = head
    if necesita_get:
        get, n2 = _con_reintentos(url, "GET", cfg)
        obs["intentos"] += n2
        obs["error"] = get["error"]
        final = get if (get["codigo"] is not None or head["codigo"] is None) else head
    obs.update({"codigo_http": final["codigo"], "url_final": final["url_final"],
                "redirecciones": final["redirecciones"], "content_type": final["content_type"]})
    cuerpo = final.get("cuerpo") or b""
    obs["bytes"] = len(cuerpo)
    texto_norm = normalizar_contenido(cuerpo, final["content_type"]) if cuerpo else ""
    crudo = cuerpo[:300_000].decode("utf-8", errors="replace") if cuerpo else ""
    bajo = (unicodedata.normalize("NFKC", crudo).lower() if crudo else "")
    obs["muro_pago"], obs["indicios_muro_pago"] = detectar_muro_pago(bajo, final["codigo"], crudo)
    obs["retractacion"] = detectar_retractacion(bajo)
    titulo = re.search(r"<title[^>]*>(.*?)</title>", crudo, re.I | re.S)
    obs["titulo_pagina"] = re.sub(r"\s+", " ", titulo.group(1)).strip()[:200] if titulo else None
    if texto_norm and final["codigo"] is not None and final["codigo"] < 400:
        obs["hash"] = sha256_texto(texto_norm)
        obs["huella"] = simhash64(texto_norm)
    else:
        obs["hash"] = obs["huella"] = None
    return obs


def consultar_wayback(url: str, cfg: Config, fecha: Optional[dt.date] = None) -> Optional[Dict]:
    q = {"url": url}
    if fecha:
        q["timestamp"] = fecha.strftime("%Y%m%d")
    api = cfg.wayback_api + ("&" if "?" in cfg.wayback_api else "?") + urllib.parse.urlencode(q)
    r, _ = _con_reintentos(api, "GET", Config(**{**cfg.__dict__, "reintentos": min(cfg.reintentos, 1)}))
    if r["codigo"] != 200 or not r["cuerpo"]:
        return None
    try:
        datos = json.loads(r["cuerpo"].decode("utf-8", errors="replace"))
        snap = (datos.get("archived_snapshots") or {}).get("closest") or {}
    except (ValueError, AttributeError):
        return None
    if snap.get("available") and snap.get("url"):
        return {"url": snap["url"], "timestamp": snap.get("timestamp"), "status": snap.get("status")}
    return None


# ---------------------------------------------------------------------------
# Clasificación y acción sugerida
# ---------------------------------------------------------------------------
def _url_equivalente(a: str, b: str) -> bool:
    def n(u):
        s = urllib.parse.urlsplit(u)
        host = (s.hostname or "").lower()
        host = host[4:] if host.startswith("www.") else host
        return host, s.path.rstrip("/") or "/", s.query
    return n(a) == n(b)


def clasificar(obs: Dict, ficha: Ficha, cfg: Config) -> Tuple[str, List[str]]:
    notas: List[str] = []
    codigo = obs.get("codigo_http")
    if codigo is None:
        notas.append(f"Sin respuesta tras {obs.get('intentos')} intentos: {obs.get('error')}")
        return "ROTO", notas
    if obs.get("muro_pago"):
        notas.append("Indicios de muro de pago: " + ", ".join(obs.get("indicios_muro_pago") or []))
        return "MURO_PAGO", notas
    if codigo >= 400:
        notas.append(f"HTTP {codigo}")
        return "ROTO", notas
    orig_path = urllib.parse.urlsplit(obs["url"]).path
    fin_path = urllib.parse.urlsplit(obs["url_final"]).path
    if obs["redirecciones"] and orig_path not in ("", "/") and fin_path in ("", "/"):
        notas.append("Redirección a la portada del sitio (soft-404)")
        return "ROTO", notas
    t = (obs.get("titulo_pagina") or "").lower()
    if any(m in t for m in MARCAS_SOFT404):
        notas.append(f"Título de página de error: «{obs.get('titulo_pagina')}» (soft-404)")
        return "ROTO", notas
    estado = "OK"
    if obs["redirecciones"] and not _url_equivalente(obs["url"], obs["url_final"]):
        estado = "REDIRIGIDO"
        notas.append(f"Redirige a {obs['url_final']}")
    hash_prev = ficha.campo("Hash de contenido")
    huella_prev = ficha.campo("Huella de contenido")
    obs["similitud"] = None
    if obs.get("hash") and hash_prev:
        if hash_prev.strip() == obs["hash"]:
            obs["similitud"] = 1.0
        else:
            sim = similitud_simhash(huella_prev, obs["huella"]) if huella_prev else None
            obs["similitud"] = sim
            if sim is None or sim < cfg.umbral_similitud:
                notas.append("Contenido cambiado: " + (f"similitud {sim} < {cfg.umbral_similitud}" if sim is not None
                                                       else "hash distinto y sin huella previa para medir similitud"))
                estado = "CONTENIDO_CAMBIADO"
            else:
                notas.append(f"Cambios menores de contenido (similitud {sim})")
    return estado, notas


def sugerir_accion(estado: str, obs: Dict, ficha: Ficha, fecha: dt.date, cfg: Config,
                   alternativa: Optional[Dict]) -> Tuple[str, str, Dict]:
    """Devuelve (acción, motivo, campos de control) según 13.4–13.5."""
    ctl: Dict = {"confirmado": None, "primer_fallo": None}
    primer = _fecha(ficha.campo("Primer fallo"))
    if obs.get("retractacion"):
        return "BORRAR", "Contenido retractado o retirado (" + ", ".join(obs["retractacion"]) + "); confirmar y avisar al Curador si sustenta EVD", ctl
    accion, motivo = "NINGUNA", "Sin incidencias"
    if estado == "ROTO":
        primer_efectivo = primer or fecha
        ctl["primer_fallo"] = primer_efectivo
        dias = (fecha - primer_efectivo).days
        ctl["confirmado"] = dias >= cfg.dias_confirmacion_roto
        if alternativa:
            accion, motivo = "REPARAR", f"Enlace roto; alternativa disponible: {alternativa['tipo']} {alternativa['url']}"
        elif not ctl["confirmado"]:
            accion, motivo = "NINGUNA", "Primer fallo: reintentar tras ≥ 24 h para confirmar (13.4)"
        elif dias >= cfg.dias_entre_barridos:
            accion, motivo = "BORRAR", f"Enlace roto sin alternativa tras dos barridos (primer fallo {primer_efectivo.isoformat()})"
        else:
            accion, motivo = "DEGRADAR", "Roto confirmado sin alternativa; se borrará si persiste en el siguiente barrido"
    elif estado == "MURO_PAGO":
        if alternativa:
            accion, motivo = "REPARAR", f"Muro de pago; copia de acceso abierto: {alternativa['url']}"
        else:
            accion, motivo = "DEGRADAR", "Muro de pago sin copia abierta: bajar el criterio de accesibilidad (13.3)"
    elif estado == "CONTENIDO_CAMBIADO":
        accion = "DEGRADAR"
        motivo = "Contenido cambiado por encima del umbral: revisar coincidencia con los metadatos"
        if alternativa:
            motivo += f"; versión archivada: {alternativa['url']}"
    elif estado == "REDIRIGIDO":
        permanente = any(r["codigo"] in (301, 308) for r in obs.get("redirecciones") or [])
        if permanente:
            accion, motivo = "REPARAR", f"Redirección permanente: actualizar la URL a {obs['url_final']}"
        else:
            accion, motivo = "NINGUNA", "Redirección temporal"
    # Baja por calidad (Q < 50 y sin uso en 180 días)
    ultimo_uso = _fecha(ficha.campo("Último uso"))
    if accion in ("NINGUNA", "DEGRADAR") and ficha.q is not None and ficha.q < cfg.q_baja and ultimo_uso \
            and (fecha - ultimo_uso).days >= cfg.dias_sin_uso_baja:
        accion, motivo = "BORRAR", f"Q {ficha.q} < {cfg.q_baja} y sin uso en {(fecha - ultimo_uso).days} días"
    return accion, motivo, ctl


def verificar_ficha(ficha: Ficha, cfg: Config, fecha: dt.date) -> Dict:
    url = extraer_url(ficha.campo("URL", "URL de acceso", "Enlace", "DOI / URL", "DOI / ISBN / URL", "Canal oficial (URL raíz)"))
    doi = extraer_doi(ficha.campo("DOI", "DOI o identificador persistente", "DOI / URL", "DOI / ISBN / URL"))
    res: Dict = {"id": ficha.id, "titulo": ficha.titulo, "q": ficha.q, "nivel": ficha.nivel, "url": url, "doi": doi,
                 "estado_anterior": ficha.campo("Estado del enlace"),
                 "ultima_verificacion_anterior": ficha.campo("Última verificación"),
                 "fecha_verificacion": fecha.isoformat()}
    if not url and not doi:
        res.update({"estado": "ROTO", "accion": "REPARAR", "motivo": "La ficha no tiene URL ni DOI",
                    "notas": [], "codigo_http": None, "confirmado": True, "primer_fallo": None})
        return res
    obs_doi = None
    if doi:
        obs_doi = comprobar_url(cfg.doi_base + urllib.parse.quote(doi, safe="/:;()._-"), cfg)
        res["doi_resuelto"] = bool(obs_doi["redirecciones"]) or (obs_doi["codigo_http"] is not None and obs_doi["codigo_http"] < 400)
        res["doi_destino"] = obs_doi["url_final"]
        res["doi_codigo_http"] = obs_doi["codigo_http"]
    obs = comprobar_url(url, cfg) if url else obs_doi
    estado, notas = clasificar(obs, ficha, cfg)
    if not url and estado == "REDIRIGIDO":  # la redirección es inherente a la resolución del DOI
        estado = "OK"
        notas = [n for n in notas if not n.startswith("Redirige a")] + [f"DOI resuelto a {obs['url_final']}"]
    alternativa = None
    if estado in ("ROTO", "MURO_PAGO") and obs_doi is not None and url:
        e_doi, _ = clasificar(dict(obs_doi), Ficha(ficha.id, ficha.titulo, None, None, 0, 0), cfg)
        if e_doi in ("OK", "REDIRIGIDO") and estado == "ROTO":
            alternativa = {"tipo": "DOI", "url": obs_doi["url_final"]}
    copia = None
    if cfg.wayback == "siempre" or (cfg.wayback == "incidencias" and estado in ("ROTO", "MURO_PAGO", "CONTENIDO_CAMBIADO")):
        objetivo = url or obs["url_final"]
        copia = consultar_wayback(objetivo, cfg, _fecha(ficha.campo("Última verificación")) if estado == "CONTENIDO_CAMBIADO" else None)
        if copia and not alternativa:
            alternativa = {"tipo": "Wayback", "url": copia["url"]}
    accion, motivo, ctl = sugerir_accion(estado, obs, ficha, fecha, cfg, alternativa)
    res.update({
        "estado": estado, "accion": accion, "motivo": motivo, "notas": notas,
        "codigo_http": obs.get("codigo_http"), "head_codigo": obs.get("head_codigo"), "intentos": obs.get("intentos"),
        "url_final": obs.get("url_final"), "redirecciones": obs.get("redirecciones"),
        "muro_pago": obs.get("muro_pago"), "indicios_muro_pago": obs.get("indicios_muro_pago"),
        "retractacion": obs.get("retractacion"), "similitud": obs.get("similitud"),
        "hash": obs.get("hash"), "huella": obs.get("huella"),
        "copia_archivada": copia, "confirmado": ctl["confirmado"],
        "primer_fallo": ctl["primer_fallo"].isoformat() if ctl["primer_fallo"] else None,
    })
    if accion == "BORRAR" and ficha.campo("Evidencias", "EVD"):
        res["aviso_curador"] = f"La referencia sustenta {ficha.campo('Evidencias', 'EVD')}: avisar al Curador (CT-11, fuente_retirada)"
    return res


def verificar_archivo(lineas: List[str], cfg: Config, fecha: dt.date, ids: Optional[Sequence[str]] = None,
                      hilos: int = 4) -> List[Dict]:
    fichas = [f for f in leer_fichas(lineas) if not ids or f.id in ids]
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, hilos)) as ex:
        return list(ex.map(lambda f: verificar_ficha(f, cfg, fecha), fichas))


# ---------------------------------------------------------------------------
# Escritura en el markdown
# ---------------------------------------------------------------------------
def _fijar_campo(lineas: List[str], ficha: Ficha, nombre: str, valor: str) -> None:
    clave = _norm_clave(nombre)
    if clave in ficha.lineas_campo:
        i = ficha.lineas_campo[clave]
        m = RE_CAMPO.match(lineas[i].rstrip("\n"))
        fin = "\n" if lineas[i].endswith("\n") else ""
        lineas[i] = f"{m.group('pre')}{m.group('campo')}:** {valor}{fin}"
        return
    ultima = max(ficha.lineas_campo.values()) if ficha.lineas_campo else ficha.linea_inicio
    prefijo = "- **"
    lineas.insert(ultima + 1, f"{prefijo}{nombre}:** {valor}\n")


def aplicar_resultados(lineas: List[str], resultados: List[Dict]) -> List[str]:
    por_id = {r["id"]: r for r in resultados}
    # Procesar de abajo arriba para no desplazar índices
    for ficha in sorted(leer_fichas(lineas), key=lambda f: -f.linea_inicio):
        r = por_id.get(ficha.id)
        if not r:
            continue
        cambios: List[Tuple[str, str]] = [("Estado del enlace", r["estado"]),
                                          ("Última verificación", r["fecha_verificacion"])]
        if r["estado"] == "ROTO":
            if r.get("primer_fallo"):
                cambios.append(("Primer fallo", r["primer_fallo"]))
        elif ficha.campo("Primer fallo"):
            cambios.append(("Primer fallo", "—"))
        if r.get("hash") and r["estado"] in ("OK", "REDIRIGIDO"):
            cambios.append(("Hash de contenido", r["hash"]))
            cambios.append(("Huella de contenido", r["huella"]))
        elif r.get("hash") and r["estado"] == "MURO_PAGO" and not ficha.campo("Hash de contenido"):
            cambios.append(("Hash de contenido", r["hash"]))
            cambios.append(("Huella de contenido", r["huella"]))
        if r.get("copia_archivada") and not ficha.campo("Copia archivada"):
            cambios.append(("Copia archivada", r["copia_archivada"]["url"]))
        # Aplicar en orden inverso a la posición de inserción para mantener el orden visual
        for nombre, valor in cambios:
            _fijar_campo(lineas, ficha, nombre, valor)
            ficha = next(f for f in leer_fichas(lineas) if f.id == ficha.id and f.linea_inicio == ficha.linea_inicio)
    return lineas


def rebasar_contenido(lineas: List[str], fid: str, resultado: Dict) -> List[str]:
    """Acepta el contenido actual como referencia (tras revisión del agente)."""
    ficha = next((f for f in leer_fichas(lineas) if f.id == fid), None)
    if not ficha or not resultado.get("hash"):
        raise ValueError(f"No se puede rebasar {fid}: ficha inexistente o sin contenido descargado")
    _fijar_campo(lineas, ficha, "Hash de contenido", resultado["hash"])
    ficha = next(f for f in leer_fichas(lineas) if f.id == fid)
    _fijar_campo(lineas, ficha, "Huella de contenido", resultado["huella"])
    return lineas


def borrar_ficha(lineas: List[str], fid: str, motivo: str, fecha: dt.date, sustituta: Optional[str] = None) -> Tuple[List[str], Dict]:
    if not motivo or not motivo.strip():
        raise ValueError("El borrado exige --motivo (13.5)")
    ficha = next((f for f in leer_fichas(lineas) if f.id == fid), None)
    if not ficha:
        raise ValueError(f"No existe la ficha {fid}")
    info = {"id": fid, "titulo": ficha.titulo, "motivo": motivo.strip(), "fecha": fecha.isoformat(),
            "sustituta": sustituta or "—", "evidencias": ficha.campo("Evidencias", "EVD")}
    nuevas = lineas[:ficha.linea_inicio] + lineas[ficha.linea_fin:]
    # compactar líneas en blanco duplicadas en el punto de corte
    k = ficha.linea_inicio
    while 0 < k < len(nuevas) and not nuevas[k].strip() and not nuevas[k - 1].strip():
        del nuevas[k]
    celda = lambda s: str(s).replace("|", "\\|").replace("\n", " ")  # noqa: E731
    fila = f"| {celda(fid)} | {celda(ficha.titulo)} | {celda(info['motivo'])} | {info['fecha']} | {celda(info['sustituta'])} |\n"
    idx_sec = next((i for i, ln in enumerate(nuevas) if RE_TITULO.match(ln) and "registro de bajas" in _norm_clave(ln)), None)
    if idx_sec is None:
        if nuevas and nuevas[-1].strip():
            nuevas.append("\n")
        if nuevas and not nuevas[-1].endswith("\n"):
            nuevas[-1] += "\n"
        nuevas += ["## Registro de bajas\n", "\n", "| REF-id | Título | Motivo | Fecha | Sustituta |\n",
                   "|---|---|---|---|---|\n", fila]
    else:
        nivel = len(RE_TITULO.match(nuevas[idx_sec]).group(1))
        fin_sec = next((i for i in range(idx_sec + 1, len(nuevas))
                        if RE_TITULO.match(nuevas[i]) and len(RE_TITULO.match(nuevas[i]).group(1)) <= nivel), len(nuevas))
        filas_tabla = [i for i in range(idx_sec + 1, fin_sec) if nuevas[i].lstrip().startswith("|")]
        if filas_tabla:
            ultima = filas_tabla[-1]
            if not nuevas[ultima].endswith("\n"):
                nuevas[ultima] += "\n"
            nuevas.insert(ultima + 1, fila)
        else:
            nuevas[idx_sec + 1:idx_sec + 1] = ["\n", "| REF-id | Título | Motivo | Fecha | Sustituta |\n",
                                               "|---|---|---|---|---|\n", fila]
    if info["evidencias"]:
        info["aviso_curador"] = "La referencia sustentaba evidencia en F2: avisar al Curador (CT-11, tipo fuente_retirada)"
    return nuevas, info


# ---------------------------------------------------------------------------
# Informes
# ---------------------------------------------------------------------------
COLUMNAS_CSV = ["id", "titulo", "q", "nivel", "url", "doi", "estado_anterior", "estado", "codigo_http", "url_final",
                "muro_pago", "similitud", "retractacion", "copia_archivada", "confirmado", "primer_fallo",
                "accion", "motivo", "fecha_verificacion"]


def a_csv(resultados: List[Dict]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=COLUMNAS_CSV, extrasaction="ignore", lineterminator="\n")
    w.writeheader()
    for r in resultados:
        fila = dict(r)
        fila["copia_archivada"] = (r.get("copia_archivada") or {}).get("url") if r.get("copia_archivada") else ""
        fila["retractacion"] = "; ".join(r.get("retractacion") or [])
        w.writerow(fila)
    return buf.getvalue()


def resumen(resultados: List[Dict]) -> Dict:
    por_estado = {e: 0 for e in ESTADOS}
    por_accion = {a: 0 for a in ACCIONES}
    for r in resultados:
        por_estado[r["estado"]] = por_estado.get(r["estado"], 0) + 1
        por_accion[r["accion"]] = por_accion.get(r["accion"], 0) + 1
    n = len(resultados)
    con_enlace = [r for r in resultados if r.get("url") or r.get("doi")]
    incidencia_red = bool(con_enlace) and all(r.get("codigo_http") is None and r.get("doi_codigo_http") is None
                                              for r in con_enlace)
    return {"referencias": n, "por_estado": por_estado, "por_accion": por_accion,
            "salud_enlaces_pct_ok": round(100 * por_estado["OK"] / n, 1) if n else None,
            "incidencia_red": incidencia_red}


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="HT-02 · Verificador de enlaces y contenido de archivos de referencias")
    ap.add_argument("archivo", help="Archivo markdown de referencias (F7, F8 o F9)")
    ap.add_argument("--salida-json", help="Informe JSON (por defecto, stdout)")
    ap.add_argument("--salida-csv", help="Informe CSV")
    ap.add_argument("--ids", nargs="*", help="Verificar solo estas fichas")
    ap.add_argument("--aplicar", action="store_true", help="Actualizar en el markdown los campos de estado y fecha")
    ap.add_argument("--borrar", metavar="ID", help="Eliminar la ficha ID y registrar la baja")
    ap.add_argument("--motivo", help="Motivo de la baja (obligatorio con --borrar)")
    ap.add_argument("--sustituta", help="REF-id sustituta (opcional, con --borrar)")
    ap.add_argument("--rebasar", metavar="ID", help="Aceptar el contenido actual de ID como nueva referencia de hash")
    ap.add_argument("--fecha", help="Fecha de verificación AAAA-MM-DD (por defecto, hoy)")
    ap.add_argument("--timeout", type=float, default=15.0)
    ap.add_argument("--reintentos", type=int, default=2)
    ap.add_argument("--espera", type=float, default=1.0, help="Espera base entre reintentos (s, exponencial)")
    ap.add_argument("--hilos", type=int, default=4)
    ap.add_argument("--umbral-similitud", type=float, default=0.8)
    ap.add_argument("--wayback", choices=["siempre", "incidencias", "nunca"], default="incidencias")
    ap.add_argument("--wayback-api", default="https://archive.org/wayback/available")
    ap.add_argument("--doi-base", default="https://doi.org/")
    ap.add_argument("--sin-contenido", action="store_true", help="No descargar el cuerpo (sin hash ni muro de pago)")
    ap.add_argument("--sin-proxy", action="store_true", help="Ignorar los proxies del entorno")
    ap.add_argument("--ca-bundle", help="Fichero de certificados raíz para TLS")
    a = ap.parse_args(argv)
    fecha = dt.date.fromisoformat(a.fecha) if a.fecha else dt.date.today()
    try:
        with open(a.archivo, encoding="utf-8") as fh:
            lineas = fh.readlines()
    except OSError as e:
        print(json.dumps({"herramienta": "HT-02", "error": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 3
    if a.borrar:
        try:
            nuevas, info = borrar_ficha(lineas, a.borrar, a.motivo or "", fecha, a.sustituta)
        except ValueError as e:
            print(json.dumps({"herramienta": "HT-02", "error": str(e)}, ensure_ascii=False), file=sys.stderr)
            return 2
        with open(a.archivo, "w", encoding="utf-8") as fh:
            fh.writelines(nuevas)
        print(json.dumps({"herramienta": "HT-02", "baja": info}, ensure_ascii=False, indent=2))
        return 0
    cfg = Config(timeout=a.timeout, reintentos=a.reintentos, espera_base=a.espera, doi_base=a.doi_base,
                 wayback_api=a.wayback_api, wayback=a.wayback, usar_proxy_entorno=not a.sin_proxy,
                 ca_bundle=a.ca_bundle, umbral_similitud=a.umbral_similitud, descargar_contenido=not a.sin_contenido)
    ids = a.ids or ([a.rebasar] if a.rebasar else None)
    resultados = verificar_archivo(lineas, cfg, fecha, ids, a.hilos)
    informe = {"herramienta": "HT-02", "version": VERSION, "archivo": a.archivo, "fecha": fecha.isoformat(),
               "resumen": resumen(resultados), "resultados": resultados}
    if a.rebasar:
        r = next((x for x in resultados if x["id"] == a.rebasar), None)
        try:
            lineas = rebasar_contenido(lineas, a.rebasar, r or {})
        except ValueError as e:
            print(json.dumps({"herramienta": "HT-02", "error": str(e)}, ensure_ascii=False), file=sys.stderr)
            return 2
    if a.aplicar and informe["resumen"]["incidencia_red"]:
        informe["aviso"] = ("Ninguna comprobación obtuvo respuesta HTTP: posible incidencia de red o de proxy. "
                            "No se aplica ningún cambio al archivo; repetir cuando haya conectividad.")
        a.aplicar = False
    if a.aplicar:
        lineas = aplicar_resultados(lineas, resultados)
    if a.aplicar or a.rebasar:
        with open(a.archivo, "w", encoding="utf-8") as fh:
            fh.writelines(lineas)
        informe["markdown_actualizado"] = True
    texto = json.dumps(informe, ensure_ascii=False, indent=2)
    if a.salida_json:
        with open(a.salida_json, "w", encoding="utf-8") as fh:
            fh.write(texto + "\n")
    else:
        print(texto)
    if a.salida_csv:
        with open(a.salida_csv, "w", encoding="utf-8", newline="") as fh:
            fh.write(a_csv(resultados))
    return 0


if __name__ == "__main__":
    sys.exit(main())
