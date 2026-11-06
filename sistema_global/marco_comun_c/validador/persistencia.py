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

V0.45 (T-03, tercera parte): con una clave secreta (`clave=` en volcar, guardar, cargar y cargar_de; `nueva_clave`,
`escribir_clave` y `leer_clave` con un fichero 0600 como bóveda de la Fase 1) el documento lleva clave_id y una firma
HMAC-SHA256 de su cabecera y de la huella del estado: PE-06 si falta la firma o la clave, si es de otra clave o si no es válida;
PE-07 si la clave no vale (menos de 32 bytes, fichero legible por otros, no hexadecimal). Sin la clave ya no se puede rehacer
nada, tampoco lo que no está encadenado. Sin clave todo sigue como en V0.42.

V0.46 (T-03, cuarta parte): el documento pasa al formato ESTADO-ORQUESTADOR-0.2.0 y lleva en la cabecera el "esquema" del
código que lo escribió (`esquema_actual`: huella de los atributos del Orquestador, la configuración por defecto, los parámetros,
las constantes y las versiones de reglas; la configuración y el calendario del operador no cuentan). Un documento de otro esquema
o del formato 0.1.0 (V0.42 a V0.45) no se carga: PE-08, hay que migrarlo con `migraciones.migrar` o `migraciones.migrar_ficheros`.
La firma cubre toda la cabecera, también el esquema.

Lo que no hace (T-03 sigue abierta para ello): la huella sin clave detecta un fichero roto o tocado a mano, no a quien la rehace;
lo que está encadenado lo detecta integridad(), pero avisos, fotos, cotizaciones, manuales o pantallas no van en ninguna cadena
(desde V0.45, con clave, la firma lo cubre todo). Ni la firma ni las huellas impiden volver a un estado y un diario firmados más
antiguos, ni recortar el final del diario: para eso hace falta un ancla monótona fuera del alcance de quien toca los ficheros
(la bóveda real, Fase 3). La rotación de claves y el reloj real del sistema quedan pendientes.
"""
from __future__ import annotations

import copy
import hashlib
import hmac
import json
import math
import os
import re
import secrets
import stat
import tempfile
from datetime import datetime

from orquestador import CONFIG_DEFECTO, Orquestador

FORMATO = "ESTADO-ORQUESTADOR-0.2.0"     # V0.46: con "esquema" en la cabecera
FORMATO_010 = "ESTADO-ORQUESTADOR-0.1.0"  # V0.42 a V0.45: se lee para migrarlo, no se carga
CLAVES_010 = {"formato", "version_config", "guardado_en", "atributos", "estado", "huella"}
CLAVES = CLAVES_010 | {"esquema"}
CLAVES_FIRMADO = CLAVES | {"clave_id", "firma"}   # V0.45: con una clave secreta, el documento va firmado (HMAC-SHA256)
CLAVES_FIRMADO_010 = CLAVES_010 | {"clave_id", "firma"}
FORMAS = {FORMATO: (CLAVES, CLAVES_FIRMADO), FORMATO_010: (CLAVES_010, CLAVES_FIRMADO_010)}
CLAVE_MIN_BYTES = 32
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


def clave_valida(clave) -> bool:
    """Al menos 32 bytes y no trivial: una clave con menos de 8 valores de byte distintos (por ejemplo, todo ceros) no vale
    (revisión de V0.45, hallazgo 5). Una clave de nueva_clave() siempre los tiene."""
    return isinstance(clave, (bytes, bytearray)) and len(clave) >= CLAVE_MIN_BYTES and len(set(bytes(clave))) >= 8


def clave_id(clave) -> str:
    """Identificador público de una clave (no la revela): permite decir «firmado con otra clave» en lugar de «firma rota»."""
    return hashlib.sha256(b"robot-investor/clave-id/" + bytes(clave)).hexdigest()[:16]


def firmar(clave, mensaje: str) -> str:
    return hmac.new(bytes(clave), mensaje.encode("ascii"), hashlib.sha256).hexdigest()


def _firma_doc(clave, doc) -> str:
    """La firma cubre la cabecera entera y el estado tal como está escrito, en su orden: la huella canónica ordena las claves y
    el Orquestador recorre expedientes, encargos y sellos en orden de inserción (revisión de V0.45, hallazgo 1). Lleva un prefijo
    de dominio distinto del de las líneas del diario."""
    orden = hashlib.sha256(_texto(doc["estado"]).encode("ascii")).hexdigest()
    # toda la cabecera salvo la firma (en 0.1.0 son las mismas claves que en V0.45; en 0.2.0, también el esquema)
    cabecera = _canon({k: doc[k] for k in doc if k not in ("estado", "firma")})
    return firmar(clave, "robot-investor/estado/" + cabecera + "|" + orden)


# V0.46: lo que forma el esquema del código. Un Orquestador se crea con una configuración y un calendario sintéticos (no los del
# operador: así el esquema no depende de ellos y se puede calcular aunque la configuración guardada no valga con este código).
CFG_ESQUEMA = {"perfiles_activos": ["C-DIV"], "clases_ratificadas": {"C-DIV": "Q"}, "apalancamiento_permitido": False}
CAL_ESQUEMA = {"version": "ESQUEMA", "mercados": {}}
# módulos cuyas constantes (nombres en mayúsculas) deciden qué hace el sistema con el estado guardado; persistencia, diario y
# migraciones no: su forma la da el formato del documento (revisión de V0.46, hallazgo 7)
MODULOS_ESQUEMA = ("comparador", "consola", "contratos", "control_f", "dimensionado", "ejecucion_g", "k_calidad", "mandatos",
                   "manual_g", "motor", "orquestador", "parametros", "validar_contradictor", "validar_encargo", "validar_sobre", "vigilancia")
_MAYUSCULAS = re.compile(r"^[A-Z][A-Z0-9_]*\Z")


def _norm(v):
    """Una constante en forma JSON determinista: conjuntos ordenados, tuplas como listas, expresiones regulares por su patrón,
    clases y funciones por su nombre, intervalos en segundos. Las rutas no cuentan (dependen de dónde está instalado)."""
    if v is None or isinstance(v, (str, bool, int)):
        return v
    if isinstance(v, float):
        return v if math.isfinite(v) else repr(v)
    if isinstance(v, (list, tuple)):
        return [_norm(x) for x in v]
    if isinstance(v, (set, frozenset)):
        return sorted((_norm(x) for x in v), key=_canon)
    if isinstance(v, dict) or type(v).__name__ == "mappingproxy":
        return {str(k): _norm(x) for k, x in v.items()}
    if isinstance(v, re.Pattern):
        return {"re": v.pattern, "flags": int(v.flags)}
    if isinstance(v, type):
        return {"clase": v.__name__}
    if type(v).__name__ == "timedelta":
        return {"segundos": v.total_seconds()}
    return {"tipo": type(v).__name__}


def parte_de_codigo() -> dict:
    """V0.46: todo lo que este código decide por sí mismo, sin datos del operador: los atributos de un Orquestador recién creado,
    CONFIG_DEFECTO entera, la parte de la configuración completa que no viene de la configuración ni del calendario (parámetros,
    constantes y versiones de reglas: con ella se rehace la huella de configuración de un estado de este código) y las constantes
    de los módulos de MODULOS_ESQUEMA. Es JSON puro: se puede guardar en el registro de esquemas de las migraciones."""
    import importlib
    f = Orquestador(CFG_ESQUEMA, CAL_ESQUEMA)
    codigo = {k: v for k, v in f._configuracion_completa().items() if k not in ("orquestador", "calendario", "version_config")}
    modulos = {}
    for nombre in MODULOS_ESQUEMA:
        m = importlib.import_module(nombre)
        modulos[nombre] = {k: _norm(v) for k, v in sorted(vars(m).items())
                           if _MAYUSCULAS.match(k) and not isinstance(v, os.PathLike)}
    return json.loads(_canon({"atributos": sorted(vars(f)), "config_defecto": _norm(CONFIG_DEFECTO), "codigo": _norm(codigo),
                              "modulos": modulos}))


def esquema_de_parte(parte) -> str:
    return hashlib.sha256(_canon(parte).encode("ascii")).hexdigest()


def esquema_actual() -> str:
    """V0.46: el esquema de este código (huella de `parte_de_codigo`)."""
    return esquema_de_parte(parte_de_codigo())


def nueva_clave() -> bytes:
    return secrets.token_bytes(CLAVE_MIN_BYTES)


def escribir_clave(ruta, clave) -> dict:
    """Guarda una clave en un fichero nuevo legible solo por su dueño (0600). En la Fase 1 hace de bóveda; nunca pisa uno existente."""
    if not clave_valida(clave):
        return _r(False, "PE-07", f"la clave debe tener al menos {CLAVE_MIN_BYTES} bytes")
    try:
        fd = os.open(ruta, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="ascii") as f:
            f.write(bytes(clave).hex() + "\n")
            f.flush()
            os.fsync(f.fileno())
    except (OSError, ValueError, TypeError) as ex:
        return _r(False, "PE-07", f"no se pudo escribir la clave: {type(ex).__name__}")
    return _r(True, "OK", "clave guardada", clave_id=clave_id(clave))


def leer_clave(ruta) -> dict:
    """Lee una clave escrita con `escribir_clave`. Falla cerrado (PE-07) si no existe, si otros pueden leerla (permisos de grupo u
    otros), si no es hexadecimal o si es corta. Devuelve {ok, codigo, motivo, clave}."""
    # se abre una vez, sin seguir enlaces y sin bloquearse (un FIFO), y se comprueba lo abierto, no la ruta: así lo comprobado y lo
    # leído son lo mismo (revisión de V0.45, hallazgos 5 a 7)
    fd = None
    try:
        fd = os.open(ruta, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            return _r(False, "PE-07", "la clave no es un fichero normal", clave=None)
        if hasattr(os, "geteuid") and st.st_uid != os.geteuid():
            return _r(False, "PE-07", "el fichero de la clave es de otro usuario", clave=None)
        if st.st_mode & 0o077:
            return _r(False, "PE-07", "el fichero de la clave lo pueden leer otros: debe ser 0600", clave=None)
        texto = os.read(fd, 4096).decode("ascii").strip()
        clave = bytes.fromhex(texto)
    except (OSError, ValueError, TypeError, UnicodeDecodeError) as ex:
        return _r(False, "PE-07", f"no se pudo leer la clave: {type(ex).__name__}", clave=None)
    finally:
        if fd is not None:
            os.close(fd)
    if not clave_valida(clave):
        return _r(False, "PE-07", f"la clave debe tener al menos {CLAVE_MIN_BYTES} bytes y no ser trivial", clave=None)
    return _r(True, "OK", "clave leída", clave=clave)


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


def volcar(o, guardado_en, clave=None) -> str:
    """El estado entero del Orquestador como texto JSON canónico. Lanza ValueError si el instante es ilegible, la clave no vale o
    el estado tiene algo que JSON no guarda tal cual (así un error de programación no deja un fichero que luego cargaría distinto).
    Con clave, el documento va firmado (clave_id y firma HMAC-SHA256)."""
    if not _instante_ok(guardado_en):
        raise ValueError("instante de guardado ilegible")
    if clave is not None and not clave_valida(clave):
        raise ValueError(f"la clave debe tener al menos {CLAVE_MIN_BYTES} bytes")
    estado = {k: v for k, v in vars(o).items()}
    if not _solo_json(estado):
        malos = sorted(k for k, v in estado.items() if not _solo_json(v))
        raise ValueError(f"el estado tiene valores que JSON no guarda tal cual: {malos[:5]}")
    doc = {"formato": FORMATO, "esquema": esquema_actual(), "version_config": o.cfg["version_config"], "guardado_en": guardado_en,
           "atributos": sorted(estado), "estado": estado, "huella": _huella(estado)}
    if clave is not None:
        doc["clave_id"] = clave_id(clave)
        doc["firma"] = _firma_doc(clave, doc)
    return _texto(doc)


def fsync_carpeta(carpeta):
    """Tras os.replace, el cambio de nombre solo es duradero cuando la carpeta llega al disco (revisión del diario, hallazgo 11)."""
    fd = os.open(carpeta, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def guardar(o, ruta, guardado_en, clave=None) -> dict:
    """Escribe el estado en `ruta` de forma atómica. Nunca lanza: devuelve {ok, codigo, motivo, ruta, huella}."""
    try:
        texto = volcar(o, guardado_en, clave)
    except (ValueError, TypeError, RecursionError) as ex:
        return _r(False, "PE-07" if "clave" in str(ex) else "PE-01", f"no se puede volcar el estado: {str(ex)[:160]}")
    if len(texto) > MAX_BYTES:   # no se escribe lo que luego no se podría leer (revisión de V0.46, hallazgo 9)
        return _r(False, "PE-05", f"el estado pasa de {MAX_BYTES} bytes: no se guarda")
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
        fsync_carpeta(carpeta)
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


def verificar(texto, clave=None):
    """V0.46: la parte de `cargar` que no depende del código: forma del documento (0.1.0 o 0.2.0), firma con la clave y huella.
    Devuelve (documento, None) o (None, resultado con el código del fallo). Nunca lanza. La usan `cargar` y las migraciones."""
    try:
        doc = json.loads(texto, parse_constant=lambda c: (_ for _ in ()).throw(ValueError(c)))
    except (ValueError, TypeError, RecursionError):
        return None, _r(False, "PE-01", "el texto no es JSON legible (o trae NaN o infinitos)", orquestador=None)
    if clave is not None and not clave_valida(clave):
        return None, _r(False, "PE-07", f"la clave debe tener al menos {CLAVE_MIN_BYTES} bytes", orquestador=None)
    if not (isinstance(doc, dict) and isinstance(doc.get("formato"), str)):
        return None, _r(False, "PE-01", "el documento no tiene la forma de un estado guardado", orquestador=None)
    if doc["formato"] not in FORMAS:
        return None, _r(False, "PE-03", f"formato {doc['formato']!r}; este código lee {FORMATO} (y {FORMATO_010} para migrarlo)", orquestador=None)
    simple, firmada = FORMAS[doc["formato"]]
    if not (set(doc) in (simple, firmada) and isinstance(doc["estado"], dict) and isinstance(doc["atributos"], list)
            and isinstance(doc["huella"], str) and HEX64.match(doc["huella"]) and _instante_ok(doc["guardado_en"])
            and isinstance(doc["version_config"], str)
            and ("esquema" not in doc or (isinstance(doc["esquema"], str) and HEX64.match(doc["esquema"])))):
        return None, _r(False, "PE-01", "el documento no tiene la forma de un estado guardado", orquestador=None)
    # V0.45: la firma va antes que nada más; sin la clave no se puede comprobar, y un documento sin firma no vale si hay clave
    firmado = set(doc) == firmada
    if firmado and clave is None:
        return None, _r(False, "PE-06", "el estado está firmado: hace falta la clave para comprobarlo", orquestador=None)
    if not firmado and clave is not None:
        return None, _r(False, "PE-06", "el estado no está firmado y se esperaba firmado con la clave", orquestador=None)
    if firmado:
        if not (isinstance(doc["clave_id"], str) and isinstance(doc["firma"], str) and HEX64.match(doc["firma"])):
            return None, _r(False, "PE-01", "firma o identificador de clave mal formados", orquestador=None)
        if doc["clave_id"] != clave_id(clave):
            return None, _r(False, "PE-06", "el estado está firmado con otra clave", orquestador=None)
        try:
            buena = hmac.compare_digest(_firma_doc(clave, doc), doc["firma"])
        except (ValueError, TypeError, RecursionError):
            buena = False
        if not buena:
            return None, _r(False, "PE-06", "la firma del estado no es válida: se tocó con la clave o sin ella", orquestador=None)
    try:
        if _huella(doc["estado"]) != doc["huella"]:
            return None, _r(False, "PE-02", "la huella del estado no cuadra: el fichero está roto o se tocó a mano", orquestador=None)
    except (ValueError, TypeError, RecursionError):
        return None, _r(False, "PE-01", "el estado tiene valores que no se pueden poner en forma canónica", orquestador=None)
    return doc, None


def montar(doc):
    """V0.46: monta un Orquestador con el estado de un documento ya verificado, con las comprobaciones que dependen del código
    (versión de configuración, atributos, configuración y calendario aceptados), sin llamar a integridad(). Devuelve (o, None) o
    (None, resultado). Nunca lanza."""
    est = doc["estado"]
    # la versión de configuración es un dato (el operador puede fijar la suya, hallazgo 5): debe ser la de la configuración guardada;
    # que el código haya cambiado lo dicen el esquema (PE-08), los atributos (PE-03), la validación (PE-04) y la huella (CONFIG)
    if not isinstance(est.get("cfg"), dict) or est["cfg"].get("version_config") != doc["version_config"]:
        return None, _r(False, "PE-03", "la versión de configuración del documento no es la de la configuración guardada", orquestador=None)
    if set(CONFIG_DEFECTO) - set(est["cfg"]):
        return None, _r(False, "PE-04", "a la configuración guardada le faltan claves de este código: hace falta una migración", orquestador=None)
    if sorted(est) != doc["atributos"]:
        return None, _r(False, "PE-03", "la lista de atributos no es la del estado guardado", orquestador=None)
    try:
        esperados = _atributos_de_este_codigo(est)
    except Exception as ex:   # noqa: BLE001 — ValueError de _valida_config o un calendario inválido
        return None, _r(False, "PE-04", f"este código no acepta la configuración o el calendario guardados: {str(ex)[:120]}", orquestador=None)
    if set(est) != esperados:
        return None, _r(False, "PE-03", f"atributos distintos de los de este código: sobran {sorted(set(est) - esperados)[:3]}, "
                                        f"faltan {sorted(esperados - set(est))[:3]}", orquestador=None)
    try:
        o = Orquestador(est["cfg"], est["cal_def"])
        for k in sorted(est):
            setattr(o, k, copy.deepcopy(est[k]))
    except Exception as ex:   # noqa: BLE001
        return None, _r(False, "PE-04", f"el estado no se puede montar con este código: {type(ex).__name__}", orquestador=None)
    return o, None


def cargar(texto, clave=None) -> dict:
    """Vuelve a montar un Orquestador desde el texto de `volcar`. Nunca lanza. Devuelve {ok, codigo, motivo, orquestador}:
    orquestador es None si no se pudo montar (PE-01 a PE-08) y el Orquestador montado si se montó (OK, o O-13 con el
    kill-switch activado si integridad() no está vacía)."""
    doc, err = verificar(texto, clave)
    if err:
        return err
    if doc["formato"] != FORMATO:
        return _r(False, "PE-08", f"estado en formato {doc['formato']} (de V0.42 a V0.45): hay que migrarlo (migraciones.migrar)", orquestador=None)
    try:
        actual = esquema_actual()
    except Exception as ex:   # noqa: BLE001 — no debería pasar: el propio código no se puede describir
        return _r(False, "PE-04", f"no se puede calcular el esquema de este código: {type(ex).__name__}", orquestador=None)
    if doc["esquema"] != actual:
        return _r(False, "PE-08", "el estado lo guardó otra versión del código (otro esquema): hay que migrarlo (migraciones.migrar)",
                  orquestador=None, esquema=doc["esquema"], esquema_actual=actual)
    o, err = montar(doc)
    if err:
        return err
    try:
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


def cargar_de(ruta, clave=None) -> dict:
    """Lee el fichero y llama a `cargar`. Nunca lanza: un fichero que no se puede leer es PE-05."""
    try:
        with open(ruta, "rb") as f:
            datos = f.read(MAX_BYTES + 1)
        if len(datos) > MAX_BYTES:
            return _r(False, "PE-05", f"el fichero pasa de {MAX_BYTES} bytes: no se lee", orquestador=None)
        texto = datos.decode("utf-8")
    except (OSError, UnicodeDecodeError, ValueError, TypeError, MemoryError) as ex:   # hallazgos 6 y 7
        return _r(False, "PE-05", f"no se pudo leer el estado: {type(ex).__name__}", orquestador=None)
    return cargar(texto, clave)
