"""Rotación de la clave de firma del estado guardado y del diario (T-03, sexta parte; V0.49). Determinista, sin red.

Desde V0.45 una clave secreta firma el estado y cada línea del diario. Este módulo la cambia, con el sistema parado y el diario
cerrado en un punto de control (como al migrar):

- `rotar(texto, ahora, motivo, clave_vieja, clave_nueva)` carga el estado con la clave vieja (si es None, el estado debe estar sin
  firmar: así se firma por primera vez), exige que esté íntegro, anota una entrada ROTACION en el registro encadenado de límites
  del Orquestador (identificador de la clave anterior y de la nueva, SHA-256 del texto de partida y motivo) y lo vuelca firmado
  con la clave nueva. Nunca quita la firma.
- `rotar_ficheros(ruta_estado, ruta_diario, ahora, motivo, clave_vieja, clave_nueva)` lo hace con los ficheros: guarda una copia
  del estado anterior, escribe el estado nuevo y luego el diario con un PUNTO firmado con la clave nueva. Si se corta entre los
  dos, volver a llamarla con las mismas claves lo completa.

Antes de rotar: abrir el diario con la clave vieja, hacer `punto()` y dejar de usar ese Diario (si se usa después, se bloquea con
DI-06: el fichero cambió por fuera); generar la nueva con `persistencia.nueva_clave()` y guardarla con `persistencia.escribir_clave()`.
Después: abrir con la nueva. Las copias firmadas con la clave vieja siguen abriéndose con ella (no se pueden invalidar sin el ancla
monótona, Fase 3), pero ninguna se carga con la nueva, y `rotar_ficheros` no vuelve a aceptar una clave retirada: lleva junto al
estado un registro de claves retiradas (`<ruta_estado>.claves-retiradas`, un `clave_id` por línea, 0600) y, además, no deja volver a
una clave que el propio estado registra como retirada (revisión de V0.49, hallazgos 1, 2 y 6).

Códigos (fallan cerrado; además los de la persistencia y el diario al leer, y PE-05 al escribir):
  CL-01 claves imposibles: la nueva falta o no es válida, o es la misma que la vieja.
  CL-02 el estado no está íntegro (integridad() no vacía al cargarlo), o el resultado no se volvería a cargar con la clave nueva o
        pasa del tamaño máximo.
  CL-03 instante ilegible o anterior al reloj del Orquestador, motivo fuera de 15 a 500 caracteres o actor que no es el operador.
  CL-04 el diario no está cerrado en un punto de control del fichero de estado, el estado ya está con la clave nueva sin una
        rotación desde esa clave vieja, la copia del estado anterior existe con otro contenido o el registro de claves retiradas
        no se puede leer. Un diario firmado con otra clave da DI-02 al leerlo.
Dos claves que HMAC trata igual (una más larga de 64 bytes y su SHA-256, o una con ceros al final) cuentan como la misma (CL-01).
"""
from __future__ import annotations

import hashlib
import json
import os

import diario as di
import persistencia as pe
from orquestador import _dt, _motivo_ok

MAXIMO_ANIO = 2100   # como el reloj (V0.47): un instante desde 2100 bloquearía el reloj para siempre (revisión, hallazgo 9)


def _r(ok, codigo, motivo, **extra):
    return {"ok": ok, "codigo": codigo, "motivo": motivo, **extra}


def _no(codigo, motivo):
    return _r(False, codigo, motivo, texto=None, orquestador=None)


def _id(clave):
    return None if clave is None else pe.clave_id(clave)


def _hmac_norm(clave):
    """La clave tal como la usa HMAC-SHA256 (bloque de 64 bytes): dos claves con la misma forma normalizada son la misma."""
    k = bytes(clave)
    if len(k) > 64:
        k = hashlib.sha256(k).digest()
    return k.ljust(64, b"\0")


def _previas(ahora, motivo, actor, clave_vieja, clave_nueva):
    """Lo que se comprueba antes de cualquier camino (revisión, hallazgos 5 y 8). None o (codigo, motivo)."""
    if not pe._instante_ok(ahora) or _dt(ahora).year >= MAXIMO_ANIO:
        return "CL-03", "instante de la rotación ilegible o fuera de lo plausible"
    if not _motivo_ok(motivo):
        return "CL-03", "la rotación necesita un motivo de 15 a 500 caracteres"
    if not (type(actor) is str and actor == "OPERADOR"):
        return "CL-03", "solo el operador rota la clave"
    if clave_nueva is None or not pe.clave_valida(clave_nueva):
        return "CL-01", "la clave nueva falta o no es válida: la rotación nunca quita la firma"
    if clave_vieja is not None and not pe.clave_valida(clave_vieja):
        return "CL-01", "la clave vieja no es válida"
    if clave_vieja is not None and _hmac_norm(clave_vieja) == _hmac_norm(clave_nueva):
        return "CL-01", "la clave nueva es la misma que la vieja (o equivalente para HMAC)"
    return None


def rotar(texto, ahora, motivo, clave_vieja, clave_nueva, actor="OPERADOR") -> dict:
    """Vuelve a firmar el texto de un estado guardado con otra clave. Nunca lanza. {ok, codigo, motivo, texto, orquestador}."""
    try:
        return _rotar(texto, ahora, motivo, clave_vieja, clave_nueva, actor)
    except Exception as ex:   # noqa: BLE001
        return _no("CL-02", f"no se pudo rotar la clave: {type(ex).__name__}")


def _rotar(texto, ahora, motivo, clave_vieja, clave_nueva, actor):
    if not isinstance(texto, str):
        return _no("PE-01", "el estado debe ser texto")
    err = _previas(ahora, motivo, actor, clave_vieja, clave_nueva)
    if err:
        return _no(*err)
    c = pe.cargar(texto, clave_vieja)
    if not c["ok"]:
        if c["codigo"] == "O-13":
            return _no("CL-02", f"el estado no está íntegro ({c.get('integridad')}): no se rota; ábrelo y resuélvelo antes")
        return {**c, "texto": None, "orquestador": None}
    o = c["orquestador"]
    retiradas = {x.get("clave_antes") for x in o.limites["entradas"] if x.get("tipo") == "ROTACION"}
    if pe.clave_id(clave_nueva) in retiradas:   # hallazgo 6: no se vuelve a una clave retirada
        return _no("CL-01", "la clave nueva ya se retiró en una rotación anterior")
    if o.ultimo_ahora is not None and _dt(ahora) < _dt(o.ultimo_ahora):
        return _no("CL-03", f"el instante de la rotación es anterior al reloj del Orquestador ({o.ultimo_ahora})")
    o._anota_limite({"tipo": "ROTACION", "clave_antes": _id(clave_vieja), "clave_despues": pe.clave_id(clave_nueva),
                     "fichero_antes": hashlib.sha256(texto.encode("utf-8")).hexdigest(), "motivo": motivo},
                    actor, ahora, f"clave de firma {'cambiada' if clave_vieja is not None else 'puesta por primera vez'}: {motivo[:120]}")
    o.ultimo_ahora = ahora
    if o.integridad():
        return _no("CL-02", f"el estado no cuadra tras anotar la rotación: {o.integridad()[:5]}")
    salida = pe.volcar(o, ahora, clave_nueva)
    if len(salida) > pe.MAX_BYTES:
        return _no("CL-02", f"el estado pasaría de {pe.MAX_BYTES} bytes")
    prueba = pe.cargar(salida, clave_nueva)
    if not prueba["ok"]:
        return _no("CL-02", f"el estado con la clave nueva no se volvería a cargar: {prueba['codigo']} {prueba['motivo']}")
    return _r(True, "OK", "clave de firma rotada", texto=salida, orquestador=prueba["orquestador"])


def _leer_estado(ruta):
    try:
        with open(ruta, "rb") as f:
            datos = f.read(pe.MAX_BYTES + 1)
        if len(datos) > pe.MAX_BYTES:
            return None, _r(False, "PE-05", "el fichero de estado pasa del tamaño máximo")
        return datos.decode("utf-8"), None
    except (OSError, UnicodeDecodeError, ValueError, TypeError, MemoryError) as ex:
        return None, _r(False, "PE-05", f"no se pudo leer el estado: {type(ex).__name__}")


def _punto(texto, clave):
    linea = di._linea({"n": 1, "tipo": "PUNTO", "estado": json.loads(texto)["huella"],
                       "fichero": hashlib.sha256(texto.encode("utf-8")).hexdigest()}, di.CERO, clave)
    return json.dumps(linea, ensure_ascii=True, separators=(",", ":")) + "\n"


def _ultima_rotacion(doc):
    """La última entrada del registro de límites de un documento ya verificado, si es una ROTACION."""
    try:
        ent = doc["estado"]["limites"]["entradas"]
        return ent[-1] if ent and isinstance(ent[-1], dict) and ent[-1].get("tipo") == "ROTACION" else None
    except (KeyError, TypeError, IndexError):
        return None


def _leer_retiradas(ruta):
    """Conjunto de clave_id retirados, o None si el registro existe y no se puede leer."""
    if not os.path.lexists(ruta):
        return set()
    try:
        with open(ruta, encoding="ascii") as f:
            ids = {x.strip() for x in f.read().splitlines() if x.strip()}
        return ids if all(pe.HEX64.match(x.ljust(64, "0")) and len(x) == 16 for x in ids) else None
    except (OSError, UnicodeDecodeError, ValueError):
        return None


def _retirar(ruta, retiradas, clave_vieja):
    if clave_vieja is None or pe.clave_id(clave_vieja) in retiradas:
        return
    di._escribir_atomico(ruta, "".join(x + "\n" for x in sorted(retiradas | {pe.clave_id(clave_vieja)})))


def rotar_ficheros(ruta_estado, ruta_diario, ahora, motivo, clave_vieja, clave_nueva, actor="OPERADOR", ruta_retiradas=None) -> dict:
    """Rota la clave del fichero de estado y deja el diario en un punto de control firmado con la nueva. Nunca lanza.
    {ok, codigo, motivo, completada, copia}: completada=True si solo terminó una rotación que se había cortado."""
    try:
        return _rotar_ficheros(ruta_estado, ruta_diario, ahora, motivo, clave_vieja, clave_nueva, actor, ruta_retiradas)
    except Exception as ex:   # noqa: BLE001
        return _r(False, "CL-02", f"no se pudo rotar: {type(ex).__name__}", completada=False, copia=None)


def _rotar_ficheros(ruta_estado, ruta_diario, ahora, motivo, clave_vieja, clave_nueva, actor, ruta_retiradas):
    def no(codigo, m, **x):
        return _r(False, codigo, m, **{"completada": False, "copia": None, **x})
    err = _previas(ahora, motivo, actor, clave_vieja, clave_nueva)
    if err:
        return no(*err)
    if not isinstance(ruta_estado, str):
        return no("PE-05", "ruta de estado no válida")
    ruta_ret = ruta_retiradas if ruta_retiradas is not None else f"{ruta_estado}.claves-retiradas"
    retiradas = _leer_retiradas(ruta_ret)
    if retiradas is None:
        return no("CL-04", "el registro de claves retiradas no se puede leer: no se rota")
    if pe.clave_id(clave_nueva) in retiradas:
        return no("CL-01", "la clave nueva ya se retiró")
    texto, err = _leer_estado(ruta_estado)
    if err:
        return no(err["codigo"], err["motivo"])
    sha = hashlib.sha256(texto.encode("utf-8")).hexdigest()
    doc, _ = pe.verificar(texto, clave_nueva)   # no depende del código: sirve aunque luego llegue otro (hallazgo 7)
    if doc is not None:
        # ya está firmado con la nueva: solo vale si su última entrada es una rotación desde esta clave vieja
        rot = _ultima_rotacion(doc)
        if not (rot and rot.get("clave_antes") == _id(clave_vieja) and rot.get("clave_despues") == pe.clave_id(clave_nueva)):
            return no("CL-04", "el estado ya está con la clave nueva, pero no por una rotación desde esa clave vieja")
        nuevas, _, _, err_n = di._leer(ruta_diario, clave_nueva)
        if err_n is None and any(e["tipo"] == "PUNTO" and e["fichero"] == sha for e in nuevas):
            _retirar(ruta_ret, retiradas, clave_vieja)
            return _r(True, "OK", "el estado y el diario ya están con la clave nueva: nada que hacer", completada=False, copia=None)
        viejas, _, _, err_v = di._leer(ruta_diario, clave_vieja)
        if not (err_v is None and len(viejas) == 1 and viejas[0]["tipo"] == "PUNTO" and viejas[0]["fichero"] == rot.get("fichero_antes")):
            return no("CL-04", "el estado ya está con la clave nueva, pero el diario no es suyo ni del estado del que se rotó")
        try:
            di._escribir_atomico(ruta_diario, _punto(texto, clave_nueva))
            _retirar(ruta_ret, retiradas, clave_vieja)
        except (OSError, ValueError, TypeError) as ex:
            return no("PE-05", f"no se pudo escribir el diario: {type(ex).__name__}")
        return _r(True, "OK", "rotación cortada completada: diario en el punto de control con la clave nueva", completada=True, copia=None)
    if clave_vieja is not None and pe.clave_id(clave_vieja) in retiradas:   # hallazgos 1 y 2: lo firmado con una clave retirada
        return no("CL-01", "la clave vieja ya se retiró: lo firmado con ella no se vuelve a firmar")
    lineas, _, _, err = di._leer(ruta_diario, clave_vieja)
    if err:
        return no(err["codigo"], err["motivo"])
    if not lineas:
        return no("DI-02", "el diario no tiene ninguna línea completa")
    if not (len(lineas) == 1 and lineas[0]["tipo"] == "PUNTO"):
        return no("CL-04", "el diario tiene operaciones después de su punto de control: ábrelo y haz punto() antes de rotar")
    try:
        huella = json.loads(texto)["huella"]
    except (ValueError, KeyError, TypeError):
        huella = None
    if lineas[0]["fichero"] != sha or lineas[0]["estado"] != huella:
        return no("CL-04", "el punto de control del diario no es el del fichero de estado")
    copia = f"{ruta_estado}.antes-{sha[:16]}"
    if os.path.lexists(copia):
        try:
            with open(copia, encoding="utf-8") as f:
                igual = f.read() == texto
        except (OSError, UnicodeDecodeError):
            igual = False
        if not igual:   # hallazgo 2: nunca se pisa una copia distinta
            return no("CL-04", "ya existe una copia del estado anterior con otro contenido: no se pisa")
    r = rotar(texto, ahora, motivo, clave_vieja, clave_nueva, actor)
    if not r["ok"]:
        return no(r["codigo"], r["motivo"])
    try:
        di._escribir_atomico(copia, texto)
        di._escribir_atomico(ruta_estado, r["texto"])
        di._escribir_atomico(ruta_diario, _punto(r["texto"], clave_nueva))
        _retirar(ruta_ret, retiradas, clave_vieja)
    except (OSError, ValueError, TypeError) as ex:
        return no("PE-05", f"no se pudo escribir la rotación: {type(ex).__name__}; vuelve a llamar a rotar_ficheros", copia=copia)
    return _r(True, "OK", "clave de firma rotada en el estado y en el diario", completada=False, copia=copia)
