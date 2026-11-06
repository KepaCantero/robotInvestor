"""Persistencia del estado del Orquestador (T-03, primera parte; V0.42). Determinista, sin red.

Hasta V0.41 todo el estado vivía en memoria: un reinicio lo perdía y, con él, los historiales encadenados, el reloj (que nunca
retrocede), el kill-switch y los registros de K, SC-3, F y G. Este módulo lo guarda en un documento JSON y lo vuelve a cargar:

- `volcar(o, guardado_en)` da el texto JSON (solo ASCII, en el orden de inserción del estado): {"formato", "version_config", "guardado_en", "atributos", "estado", "huella"}.
  "estado" son TODOS los atributos del Orquestador (nada se elige a mano: un atributo nuevo se guarda solo) y "huella" es el
  SHA-256 de su forma canónica.
- `guardar(o, ruta, guardado_en)` lo escribe de forma atómica (fichero temporal en la misma carpeta, fsync y os.replace): un corte
  a medias deja el fichero anterior entero o el nuevo entero, nunca uno roto.
- `cargar(texto)` / `cargar_de(ruta)` lo vuelven a montar sin fiarse de él, en este orden y fallando cerrado:
  PE-01 texto ilegible o con otra forma; PE-02 la huella no cuadra (fichero corrupto o editado sin rehacer la huella);
  PE-03 formato o atributos distintos de los de este código, o versión del documento distinta de la de su configuración (hace
  falta una migración; no se adivina); PE-04 la configuración guardada (completa: sin rellenar con los valores por defecto) o el
  calendario no los acepta este código, o el estado no se puede comprobar; PE-05 no se puede leer o escribir (o pasa de MAX_BYTES). Si todo eso pasa, se monta el Orquestador y se le pasa integridad():
  si algo no cuadra (historiales, posiciones, configuración, motor o sellos), se devuelve montado pero con el kill-switch activado
  (O-13), para que el operador vea qué pasó; nunca se sigue operando con un estado que no cuadra.

Lo que no hace (T-03 sigue abierta para ello): la huella sin clave detecta un fichero roto o tocado a mano, no a quien la rehace;
lo que está encadenado lo detecta integridad(), pero avisos, fotos, cotizaciones, manuales o pantallas no van en ninguna cadena.
Una firma con clave (HMAC con la clave en la bóveda, Fase 3), el reloj real del sistema y las migraciones entre versiones quedan
pendientes.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import os
import re
import tempfile
from datetime import datetime

from orquestador import CONFIG_DEFECTO, Orquestador

FORMATO = "ESTADO-ORQUESTADOR-0.1.0"
CLAVES = {"formato", "version_config", "guardado_en", "atributos", "estado", "huella"}
FH = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?(Z|[+-][0-9]{2}:[0-9]{2})\Z")
MAX_BYTES = 256 * 1024 * 1024   # un estado más grande no se lee: PE-05 (revisión, hallazgo 7)
HEX64 = re.compile(r"^[0-9a-f]{64}\Z")


def _canon(x) -> str:
    """Forma canónica para la huella: claves ordenadas, solo ASCII (un surrogado suelto se escapa y vuelve igual), sin espacios,
    sin NaN ni infinitos (allow_nan=False los rechaza)."""
    return json.dumps(x, sort_keys=True, ensure_ascii=True, separators=(",", ":"), allow_nan=False)


def _texto(x) -> str:
    """El texto del fichero: como el canónico pero conservando el orden de inserción de los diccionarios, porque el Orquestador
    recorre expedientes, encargos y sellos en ese orden (y numera avisos según él): cargar debe devolverlo igual (hallazgo 1)."""
    return json.dumps(x, ensure_ascii=True, separators=(",", ":"), allow_nan=False)


def _instante_ok(x) -> bool:
    if not (isinstance(x, str) and FH.match(x)):
        return False
    try:
        datetime.fromisoformat(x.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def _huella(estado) -> str:
    return hashlib.sha256(_canon(estado).encode("utf-8")).hexdigest()


def _r(ok, codigo, motivo, **extra):
    return {"ok": ok, "codigo": codigo, "motivo": motivo, **extra}


def _solo_json(x) -> bool:
    """El estado solo puede tener lo que JSON guarda sin cambiarlo: textos, enteros, reales finitos, booleanos, None, listas y
    diccionarios con claves de texto. Una tupla o un conjunto volverían como lista y cambiarían comparaciones: se rechaza."""
    if x is None or isinstance(x, (str, bool, int)):
        return True
    if isinstance(x, float):
        return math.isfinite(x)
    if isinstance(x, list):
        return all(_solo_json(v) for v in x)
    if isinstance(x, dict):
        return all(isinstance(k, str) and _solo_json(v) for k, v in x.items())
    return False


def volcar(o, guardado_en) -> str:
    """El estado entero del Orquestador como texto JSON canónico. Lanza ValueError si el instante es ilegible o el estado tiene
    algo que JSON no guarda tal cual (así un error de programación no deja un fichero que luego cargaría distinto)."""
    if not _instante_ok(guardado_en):
        raise ValueError("instante de guardado ilegible")
    estado = {k: v for k, v in vars(o).items()}
    if not _solo_json(estado):
        malos = sorted(k for k, v in estado.items() if not _solo_json(v))
        raise ValueError(f"el estado tiene valores que JSON no guarda tal cual: {malos[:5]}")
    doc = {"formato": FORMATO, "version_config": o.cfg["version_config"], "guardado_en": guardado_en,
           "atributos": sorted(estado), "estado": estado, "huella": _huella(estado)}
    return _texto(doc)


def guardar(o, ruta, guardado_en) -> dict:
    """Escribe el estado en `ruta` de forma atómica. Nunca lanza: devuelve {ok, codigo, motivo, ruta, huella}."""
    try:
        texto = volcar(o, guardado_en)
    except (ValueError, TypeError, RecursionError) as ex:
        return _r(False, "PE-01", f"no se puede volcar el estado: {str(ex)[:160]}")
    tmp = None
    try:
        carpeta = os.path.dirname(os.path.abspath(ruta)) or "."
        fd, tmp = tempfile.mkstemp(prefix=".estado-", suffix=".tmp", dir=carpeta)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(texto)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, ruta)
        tmp = None
    except (OSError, ValueError, TypeError) as ex:   # ruta None o con un carácter nulo también (hallazgo 6)
        return _r(False, "PE-05", f"no se pudo escribir el estado: {type(ex).__name__}")
    finally:
        try:
            if tmp and os.path.exists(tmp):
                os.unlink(tmp)
        except OSError:
            pass
    return _r(True, "OK", "estado guardado", ruta=ruta, huella=json.loads(texto)["huella"])


def _atributos_de_este_codigo(estado):
    """Los atributos que tiene un Orquestador recién creado con la configuración y el calendario guardados."""
    return set(vars(Orquestador(estado["cfg"], estado["cal_def"])))


def cargar(texto) -> dict:
    """Vuelve a montar un Orquestador desde el texto de `volcar`. Nunca lanza. Devuelve {ok, codigo, motivo, orquestador}:
    orquestador es None si no se pudo montar (PE-01 a PE-04) y el Orquestador montado si se montó (OK, o O-13 con el
    kill-switch activado si integridad() no está vacía)."""
    try:
        doc = json.loads(texto, parse_constant=lambda c: (_ for _ in ()).throw(ValueError(c)))
    except (ValueError, TypeError, RecursionError):
        return _r(False, "PE-01", "el texto no es JSON legible (o trae NaN o infinitos)", orquestador=None)
    if not (isinstance(doc, dict) and set(doc) == CLAVES and isinstance(doc["estado"], dict) and isinstance(doc["atributos"], list)
            and isinstance(doc["huella"], str) and HEX64.match(doc["huella"]) and _instante_ok(doc["guardado_en"])
            and isinstance(doc["formato"], str) and isinstance(doc["version_config"], str)):
        return _r(False, "PE-01", "el documento no tiene la forma de un estado guardado", orquestador=None)
    try:
        if _huella(doc["estado"]) != doc["huella"]:
            return _r(False, "PE-02", "la huella del estado no cuadra: el fichero está roto o se tocó a mano", orquestador=None)
    except (ValueError, TypeError, RecursionError):
        return _r(False, "PE-01", "el estado tiene valores que no se pueden poner en forma canónica", orquestador=None)
    est = doc["estado"]
    if doc["formato"] != FORMATO:
        return _r(False, "PE-03", f"formato {doc['formato']!r}; este código lee {FORMATO}: hace falta una migración", orquestador=None)
    # la versión de configuración es un dato (el operador puede fijar la suya, hallazgo 5): debe ser la de la configuración guardada;
    # que el código haya cambiado lo dicen los atributos (PE-03), la validación (PE-04) y la huella de la configuración (CONFIG)
    if not isinstance(est.get("cfg"), dict) or est["cfg"].get("version_config") != doc["version_config"]:
        return _r(False, "PE-03", "la versión de configuración del documento no es la de la configuración guardada", orquestador=None)
    if set(CONFIG_DEFECTO) - set(est["cfg"]):
        return _r(False, "PE-04", "a la configuración guardada le faltan claves de este código: hace falta una migración", orquestador=None)
    if sorted(est) != doc["atributos"]:
        return _r(False, "PE-03", "la lista de atributos no es la del estado guardado", orquestador=None)
    try:
        esperados = _atributos_de_este_codigo(est)
    except Exception as ex:   # noqa: BLE001 — ValueError de _valida_config o un calendario inválido
        return _r(False, "PE-04", f"este código no acepta la configuración o el calendario guardados: {str(ex)[:120]}", orquestador=None)
    if set(est) != esperados:
        return _r(False, "PE-03", f"atributos distintos de los de este código: sobran {sorted(set(est) - esperados)[:3]}, "
                                  f"faltan {sorted(esperados - set(est))[:3]}", orquestador=None)
    try:
        o = Orquestador(est["cfg"], est["cal_def"])
        for k in sorted(est):
            setattr(o, k, copy.deepcopy(est[k]))
        rotos = o.integridad()
        if rotos:
            # siempre deja rastro: aviso O-13 nuevo (ALTA, sin acusar) aunque el kill-switch ya estuviera activo (hallazgo 4)
            cuando = o.ultimo_ahora if _instante_ok(o.ultimo_ahora) else doc["guardado_en"]
            motivo = f"estado cargado sin integridad: {', '.join(rotos[:5])}"
            o._activar_kill(motivo, "ORQUESTADOR", cuando)
            o._aviso("O-13", motivo, cuando)
    except Exception as ex:   # noqa: BLE001 — un estado que ni siquiera se puede comprobar (o avisar) no se usa (hallazgo 2)
        return _r(False, "PE-04", f"el estado no se puede comprobar con este código: {type(ex).__name__}", orquestador=None)
    if rotos:
        return _r(False, "O-13", f"el estado cargado no cuadra ({', '.join(rotos[:5])}): kill-switch activado", orquestador=o, integridad=rotos)
    return _r(True, "OK", "estado cargado", orquestador=o, guardado_en=doc["guardado_en"])


def cargar_de(ruta) -> dict:
    """Lee el fichero y llama a `cargar`. Nunca lanza: un fichero que no se puede leer es PE-05."""
    try:
        with open(ruta, "rb") as f:
            datos = f.read(MAX_BYTES + 1)
        if len(datos) > MAX_BYTES:
            return _r(False, "PE-05", f"el fichero pasa de {MAX_BYTES} bytes: no se lee", orquestador=None)
        texto = datos.decode("utf-8")
    except (OSError, UnicodeDecodeError, ValueError, TypeError, MemoryError) as ex:   # hallazgos 6 y 7
        return _r(False, "PE-05", f"no se pudo leer el estado: {type(ex).__name__}", orquestador=None)
    return cargar(texto)
