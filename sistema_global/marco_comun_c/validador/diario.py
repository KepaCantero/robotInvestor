"""Diario de operaciones del Orquestador (T-03, segunda parte; V0.43). Determinista, sin red.

Con la persistencia de V0.42 el estado se guarda cuando alguien llama a `guardar`; lo que pase entre dos guardados se pierde con
un corte. El diario lo evita con la técnica de siempre (registro previo a la escritura): cada llamada a un método que cambia el
estado del Orquestador (los que llevan @_seguro) se anota en un fichero de solo añadir ANTES de aplicarse, y su resultado
DESPUÉS. Al arrancar se carga el último estado guardado y se vuelven a aplicar, en orden, las operaciones posteriores: como el
Orquestador es determinista, se llega exactamente al mismo estado.

`Diario` envuelve al Orquestador y se usa en su lugar (G, H, la consola y las pruebas lo reciben como `o`): los atributos y los
métodos que solo leen pasan tal cual; los que cambian el estado se anotan. Líneas del diario (JSON solo ASCII, una por línea,
encadenadas por hash):
  {"n", "tipo": "PUNTO", "estado": huella del estado, "fichero": sha-256 del fichero de estado, "prev", "hash"} — punto de control
  {"n", "tipo": "OP", "metodo", "args", "kwargs", "prev", "hash"}               — antes de aplicar
  {"n", "tipo": "RES", "op": n de su OP, "resultado": sha-256 del resultado, "prev", "hash"} — después de aplicar

Códigos (fallan cerrado):
  DI-01 la operación lleva argumentos que el diario no guarda tal cual (tuplas, conjuntos, NaN, objetos): no se aplica.
  DI-02 el diario está roto: una línea ilegible que no es la última, la cadena de hashes no cuadra o el orden no es el esperado.
  DI-03 el diario no tiene un punto de control para ese fichero de estado (son de historias o instalaciones distintas).
  DI-04 al volver a aplicar, una operación no da el resultado anotado: el código o los datos cambiaron; kill-switch y O-13.
  DI-05 no se puede escribir en el diario: la operación no se aplica (la línea a medias se quita) y el diario deja de aceptar
  operaciones hasta reabrirlo.
Una operación que lanza una excepción no recogida por @_seguro se anota con la marca de la excepción (O-00) y se reproduce igual.
Lo privado del Orquestador no se expone a través del diario (salvo PRIVADOS_DE_LECTURA) y los datos se devuelven copiados: el estado
solo cambia con los métodos anotados. Pasado un cuarto de MAX_BYTES, el diario hace solo un punto de control.
Más los de la persistencia (PE-01 a PE-05, O-13) al cargar el estado.

Una última línea a medias (corte durante la escritura) no es un fallo: se ignora y se informa (linea_incompleta). Una OP sin su
RES al final es una operación que quizá llegó a aplicarse antes del corte: se aplica (desde el estado guardado no estaba
aplicada) y se anota su RES.

`punto(ahora)` hace un punto de control: anota PUNTO con la huella del estado, guarda el estado (escritura atómica) y deja el
diario con solo esa línea (también atómico). Un corte en medio es recuperable: si el estado nuevo no llegó a guardarse, el diario
aún tiene el punto anterior y las operaciones; si llegó a guardarse, su PUNTO ya está en el diario.

Límites: un solo proceso escribe el diario; las huellas no tienen clave (como en V0.42); el reloj sigue llegando como argumento.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import tempfile

import persistencia as pe

CERO = "0" * 64
# métodos privados que solo leen y que G, la consola y contratos usan (revisión, hallazgo 3); el resto de lo privado no se expone
PRIVADOS_DE_LECTURA = frozenset({"_sello_anulado", "_testigos", "_tope_dia"})


def _limite_diario():
    """Pasado este tamaño, el diario hace solo un punto de control tras la operación (revisión, hallazgo 12)."""
    return pe.MAX_BYTES // 4


def _codificar(x):
    """El JSON exacto de unos argumentos, o None si el diario no los puede guardar tal cual (tuplas, conjuntos, NaN, objetos,
    enteros enormes, anidamiento excesivo: revisión, hallazgos 6 y 7)."""
    try:
        if not pe._solo_json(x):
            return None
        return json.dumps(x, ensure_ascii=True, separators=(",", ":"), allow_nan=False)
    except (ValueError, TypeError, RecursionError):
        return None


def _sha_fichero(ruta):
    with open(ruta, "rb") as f:
        return hashlib.sha256(f.read(pe.MAX_BYTES + 1)).hexdigest()


def _h(x) -> str:
    return hashlib.sha256(pe._canon(x).encode("ascii")).hexdigest()


def _resultado(r) -> str:
    """Huella del resultado de una operación. Si trae algo que JSON no guarda, se usa su repr (determinista para los tipos del
    Orquestador); así un resultado distinto al volver a aplicar se nota igual."""
    try:
        return _h(r)
    except (TypeError, ValueError):
        return hashlib.sha256(repr(r).encode("utf-8", "backslashreplace")).hexdigest()


def _r(ok, codigo, motivo, **extra):
    return {"ok": ok, "codigo": codigo, "motivo": motivo, **extra}


def _linea(entrada, prev):
    e = {**entrada, "prev": prev}
    e["hash"] = _h(e)
    return e


def mutantes(o) -> frozenset:
    """Los métodos que cambian el estado: los públicos envueltos por @_seguro (functools.wraps deja __wrapped__). Un
    staticmethod también es invocable y puede tener __wrapped__ desde Python 3.10: no cuenta (revisión, hallazgo 4)."""
    return frozenset(n for n, f in vars(type(o)).items() if not n.startswith("_") and not isinstance(f, (staticmethod, classmethod))
                     and callable(f) and hasattr(f, "__wrapped__"))


def _escribir_atomico(ruta, texto):
    carpeta = os.path.dirname(os.path.abspath(ruta)) or "."
    fd, tmp = tempfile.mkstemp(prefix=".diario-", suffix=".tmp", dir=carpeta)
    try:
        with os.fdopen(fd, "w", encoding="ascii") as f:
            f.write(texto)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, ruta)
        tmp = None
        pe.fsync_carpeta(carpeta)
    finally:
        if tmp and os.path.exists(tmp):
            os.unlink(tmp)


def _aplicar(o, metodo, args, kwargs):
    """Aplica una operación. Si lanza (algo que @_seguro no recoge, como argumentos que el método no acepta), el resultado es la
    marca de la excepción: al reabrir se reproduce igual y el diario sigue sirviendo (revisión, hallazgo 5)."""
    try:
        return getattr(o, metodo)(*args, **kwargs)
    except Exception as ex:   # noqa: BLE001
        return {"ok": False, "codigo": "O-00", "motivo": f"excepción al aplicar {metodo}: {type(ex).__name__}", "excepcion": type(ex).__name__}


class Diario:
    """Un Orquestador con diario. Se obtiene con `crear` o `abrir`, nunca construyéndolo a mano."""

    def __init__(self, o, ruta_estado, ruta_diario, ultimo, n):
        object.__setattr__(self, "_o", o)
        object.__setattr__(self, "_ruta_estado", ruta_estado)
        object.__setattr__(self, "_ruta_diario", ruta_diario)
        object.__setattr__(self, "_ultimo", ultimo)     # hash de la última línea
        object.__setattr__(self, "_n", n)               # número de la última línea
        object.__setattr__(self, "_mutantes", mutantes(o))
        object.__setattr__(self, "_roto", None)         # motivo si una escritura falló: no se aceptan más operaciones

    # --------------------------------------------------------------- lo que pasa, y cómo
    def __getattr__(self, nombre):
        """Métodos que cambian el estado: anotados. Métodos que leen: tal cual. Datos: una copia (cambiarla no toca el estado, que
        solo cambia con sus métodos y queda en el diario). Lo privado no se expone, salvo unos pocos métodos de lectura."""
        if nombre.startswith("__") or nombre in ("_o", "_ruta_estado", "_ruta_diario", "_ultimo", "_n", "_mutantes", "_roto"):
            raise AttributeError(nombre)   # sin esto, copy/pickle de un Diario a medio construir entran en recursión (hallazgo 8)
        if nombre.startswith("_") and nombre not in PRIVADOS_DE_LECTURA:
            raise AttributeError(f"{nombre}: lo privado del Orquestador no se usa a través del diario (no quedaría anotado)")
        a = getattr(self._o, nombre)
        if nombre in self._mutantes:
            def anotada(*args, **kwargs):
                return self._operar(nombre, list(args), dict(kwargs))
            anotada.__name__ = nombre
            return anotada
        if callable(a):
            return a
        return copy.deepcopy(a)

    def __deepcopy__(self, memo):
        """Una copia no lleva diario: es una copia del Orquestador (que nadie anota)."""
        return copy.deepcopy(self._o, memo)

    def __copy__(self):
        return copy.deepcopy(self._o)

    def __setattr__(self, nombre, valor):
        raise AttributeError("el estado del Orquestador solo cambia con sus métodos: así queda en el diario")

    @property
    def orquestador(self):
        """El Orquestador envuelto, para leerlo (cambiarlo por aquí no queda en el diario)."""
        return self._o

    # --------------------------------------------------------------- escritura
    def _anotar(self, entrada):
        """Añade una línea y la lleva al disco. Si algo falla, intenta dejar el fichero como estaba (revisión, hallazgo 2): así una
        operación que responde «no se aplica» tampoco se aplicará al reabrir. Lanza OSError si no lo consigue."""
        e = _linea({"n": self._n + 1, **entrada}, self._ultimo)
        texto = json.dumps(e, ensure_ascii=True, separators=(",", ":"), allow_nan=False) + "\n"
        tam = os.path.getsize(self._ruta_diario)
        try:
            with open(self._ruta_diario, "a", encoding="ascii") as f:
                f.write(texto)
                f.flush()
                os.fsync(f.fileno())
        except BaseException:
            try:
                with open(self._ruta_diario, "r+b") as f:
                    f.truncate(tam)
                    f.flush()
                    os.fsync(f.fileno())
            except OSError:
                pass
            raise
        object.__setattr__(self, "_ultimo", e["hash"])
        object.__setattr__(self, "_n", e["n"])
        return e["n"]

    def _operar(self, metodo, args, kwargs):
        if self._roto:
            return _r(False, "DI-05", f"el diario no acepta operaciones tras un fallo de escritura ({self._roto}): reábrelo")
        ca, ck = _codificar(args), _codificar(kwargs)
        if ca is None or ck is None:
            return _r(False, "DI-01", f"{metodo}: argumentos que el diario no guarda tal cual; no se aplica")
        args, kwargs = json.loads(ca), json.loads(ck)   # se aplica exactamente lo anotado, como al reabrir
        try:
            n = self._anotar({"tipo": "OP", "metodo": metodo, "args": args, "kwargs": kwargs})
        except BaseException as ex:   # noqa: BLE001
            object.__setattr__(self, "_roto", type(ex).__name__)
            if not isinstance(ex, Exception):
                raise
            return _r(False, "DI-05", f"no se pudo anotar la operación en el diario: no se aplica ({type(ex).__name__}); reábrelo")
        r = _aplicar(self._o, metodo, args, kwargs)
        try:
            self._anotar({"tipo": "RES", "op": n, "resultado": _resultado(r)})
        except BaseException as ex:   # noqa: BLE001 — aplicada pero sin RES: al reabrir se vuelve a aplicar desde el estado guardado
            object.__setattr__(self, "_roto", type(ex).__name__)
            if not isinstance(ex, Exception):
                raise
            return r
        if os.path.getsize(self._ruta_diario) > _limite_diario() and self._o.ultimo_ahora:
            self.punto(self._o.ultimo_ahora)   # el diario no crece sin límite (hallazgo 12); si falla, queda bloqueado
        return r

    def punto(self, ahora) -> dict:
        """Punto de control: PUNTO en el diario, estado guardado y diario reducido a ese PUNTO. Nunca lanza."""
        if self._roto:
            return _r(False, "DI-05", "el diario no acepta operaciones tras un fallo de escritura: reábrelo")
        try:
            texto = pe.volcar(self._o, ahora)
        except (ValueError, TypeError) as ex:
            return _r(False, "PE-01", f"no se puede volcar el estado: {str(ex)[:120]}")
        huella = json.loads(texto)["huella"]
        prueba = pe.cargar(texto)   # nunca se guarda (ni se reduce el diario) un estado que no se volvería a cargar (hallazgo 1)
        if not prueba["ok"]:
            return _r(False, prueba["codigo"], f"el estado no se volvería a cargar: {prueba['motivo']}; no se hace el punto")
        fichero = hashlib.sha256(texto.encode("ascii")).hexdigest()
        try:
            self._anotar({"tipo": "PUNTO", "estado": huella, "fichero": fichero})
            _escribir_atomico(self._ruta_estado, texto)
            nuevo = _linea({"n": 1, "tipo": "PUNTO", "estado": huella, "fichero": fichero}, CERO)
            _escribir_atomico(self._ruta_diario, json.dumps(nuevo, ensure_ascii=True, separators=(",", ":")) + "\n")
        except (OSError, ValueError, TypeError) as ex:
            object.__setattr__(self, "_roto", type(ex).__name__)
            return _r(False, "DI-05", f"no se pudo hacer el punto de control: {type(ex).__name__}; reábrelo")
        object.__setattr__(self, "_ultimo", nuevo["hash"])
        object.__setattr__(self, "_n", 1)
        return _r(True, "OK", "punto de control hecho", huella=huella)


def crear(o, ruta_estado, ruta_diario, ahora) -> dict:
    """Empieza un diario nuevo para `o`: guarda su estado y deja el diario con su PUNTO. No pisa ficheros existentes."""
    try:
        if os.path.exists(ruta_estado) or os.path.exists(ruta_diario):
            return _r(False, "DI-03", "ya hay un estado o un diario: ábrelos con abrir(), no se pisan", diario=None)
        texto = pe.volcar(o, ahora)
        huella = json.loads(texto)["huella"]
        prueba = pe.cargar(texto)
        if not prueba["ok"]:
            return _r(False, prueba["codigo"], f"el estado no se volvería a cargar: {prueba['motivo']}", diario=None)
        primera = _linea({"n": 1, "tipo": "PUNTO", "estado": huella, "fichero": hashlib.sha256(texto.encode("ascii")).hexdigest()}, CERO)
        _escribir_atomico(ruta_estado, texto)
        _escribir_atomico(ruta_diario, json.dumps(primera, ensure_ascii=True, separators=(",", ":")) + "\n")
    except (OSError, ValueError, TypeError) as ex:
        return _r(False, "DI-05", f"no se pudo crear el diario: {type(ex).__name__}", diario=None)
    return _r(True, "OK", "diario creado", diario=Diario(o, ruta_estado, ruta_diario, primera["hash"], 1))


def _leer(ruta_diario):
    """Las líneas del diario comprobadas (cadena y numeración). Devuelve (lineas, cortada, reescribir, error): cortada si se
    descartó una última línea a medias; reescribir si el fichero no acaba en salto de línea (hay que dejarlo limpio antes de
    seguir añadiendo)."""
    try:
        with open(ruta_diario, "rb") as f:
            datos = f.read(pe.MAX_BYTES + 1)
    except (OSError, ValueError, TypeError) as ex:
        return None, False, False, _r(False, "PE-05", f"no se pudo leer el diario: {type(ex).__name__}", diario=None)
    if len(datos) > pe.MAX_BYTES:
        return None, False, False, _r(False, "PE-05", "el diario pasa del tamaño máximo", diario=None)
    crudas = datos.split(b"\n")
    incompleta = crudas[-1] != b""   # sin salto final: la última se cortó al escribirla
    if not incompleta:
        crudas = crudas[:-1]
    lineas, prev = [], None
    for i, c in enumerate(crudas):
        ultima = i == len(crudas) - 1
        try:
            e = json.loads(c.decode("ascii"), parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
            ok = (isinstance(e, dict) and isinstance(e.get("hash"), str) and isinstance(e.get("prev"), str) and isinstance(e.get("n"), int)
                  and not isinstance(e.get("n"), bool) and e.get("tipo") in ("PUNTO", "OP", "RES")
                  and _h({k: v for k, v in e.items() if k != "hash"}) == e["hash"])
        except (ValueError, UnicodeDecodeError, TypeError, RecursionError):
            ok = False
        if not ok:
            if ultima and incompleta:
                return lineas, True, True, None
            return None, False, False, _r(False, "DI-02", f"línea {i + 1} del diario ilegible o con su hash roto", diario=None)
        if (prev is None and (e["prev"] != CERO or e["n"] != 1)) or (prev is not None and (e["prev"] != prev["hash"] or e["n"] != prev["n"] + 1)):
            return None, False, False, _r(False, "DI-02", f"la cadena del diario se rompe en la línea {i + 1}", diario=None)
        if not _forma_ok(e):
            return None, False, False, _r(False, "DI-02", f"línea {i + 1} del diario con otra forma", diario=None)
        lineas.append(e)
        prev = e
    if not lineas:
        return None, False, False, _r(False, "DI-02", "el diario está vacío", diario=None)
    return lineas, False, incompleta, None


def _forma_ok(e):
    t = e["tipo"]
    if t == "PUNTO":
        return (set(e) == {"n", "tipo", "estado", "fichero", "prev", "hash"} and all(isinstance(e[k], str) and pe.HEX64.match(e[k]) is not None
                                                                                   for k in ("estado", "fichero")))
    if t == "OP":
        return (set(e) == {"n", "tipo", "metodo", "args", "kwargs", "prev", "hash"} and isinstance(e["metodo"], str)
                and isinstance(e["args"], list) and isinstance(e["kwargs"], dict))
    return (set(e) == {"n", "tipo", "op", "resultado", "prev", "hash"} and isinstance(e["op"], int) and not isinstance(e["op"], bool)
            and isinstance(e["resultado"], str) and pe.HEX64.match(e["resultado"]) is not None)


def abrir(ruta_estado, ruta_diario) -> dict:
    """Carga el último estado guardado y vuelve a aplicar lo que el diario tiene después de su punto de control. Nunca lanza.
    Devuelve {ok, codigo, motivo, diario, aplicadas, linea_incompleta}."""
    r = pe.cargar_de(ruta_estado)
    if not r["ok"]:
        return _r(False, r["codigo"], f"estado: {r['motivo']}", diario=None, orquestador=r.get("orquestador"))
    o = r["orquestador"]
    try:
        fichero = _sha_fichero(ruta_estado)
    except (OSError, ValueError, TypeError) as ex:
        return _r(False, "PE-05", f"no se pudo releer el estado: {type(ex).__name__}", diario=None)
    lineas, incompleta, reescribir, err = _leer(ruta_diario)
    if err:
        return err
    # el punto de control es el de ESE fichero (no basta la huella del estado: dos instalaciones pueden tener el mismo, hallazgo 9)
    desde = max((i for i, e in enumerate(lineas) if e["tipo"] == "PUNTO" and e["fichero"] == fichero), default=None)
    if desde is None:
        return _r(False, "DI-03", "el diario no tiene un punto de control para el estado guardado", diario=None)
    validos = mutantes(o)
    resto, aplicadas = lineas[desde + 1:], 0
    i = 0
    while i < len(resto):
        e = resto[i]
        if e["tipo"] == "PUNTO":   # un punto cuyo estado no llegó a guardarse: el estado reaplicado debe ser el suyo (hallazgo 10)
            try:
                ahora_huella = json.loads(pe.volcar(o, "2000-01-01T00:00:00+00:00"))["huella"]
            except (ValueError, TypeError) as ex:
                return _r(False, "DI-04", f"línea {e['n']}: el estado reaplicado no se puede volcar ({type(ex).__name__})", diario=None)
            if ahora_huella != e["estado"]:
                return _r(False, "DI-04", f"línea {e['n']}: el estado reaplicado no es el del punto de control anotado", diario=None)
            i += 1
            continue
        if e["tipo"] != "OP" or e["metodo"] not in validos:
            return _r(False, "DI-02", f"línea {e['n']}: se esperaba una operación conocida", diario=None)
        res = _aplicar(o, e["metodo"], e["args"], e["kwargs"])
        aplicadas += 1
        sig = resto[i + 1] if i + 1 < len(resto) else None
        if sig is not None and sig["tipo"] == "RES":
            if sig["op"] != e["n"]:
                return _r(False, "DI-02", f"línea {sig['n']}: resultado de otra operación", diario=None)
            if sig["resultado"] != _resultado(res):
                motivo = f"diario: la operación {e['n']} ({e['metodo']}) no da el resultado anotado al volver a aplicarla"
                try:
                    o._activar_kill(motivo, "ORQUESTADOR", o.ultimo_ahora)
                    o._aviso("O-13", motivo, o.ultimo_ahora)
                except Exception:   # noqa: BLE001
                    pass
                return _r(False, "DI-04", motivo, diario=None, orquestador=o)
            i += 2
            continue
        if sig is not None:   # una OP sin su RES solo puede ser la última
            return _r(False, "DI-02", f"línea {e['n']}: operación sin resultado que no es la última", diario=None)
        d = Diario(o, ruta_estado, ruta_diario, lineas[-1]["hash"], lineas[-1]["n"])
        try:
            if reescribir:   # se quita la línea cortada (o se cierra la última) antes de seguir escribiendo
                _reescribir(ruta_diario, lineas)
            d._anotar({"tipo": "RES", "op": e["n"], "resultado": _resultado(res)})
        except (OSError, ValueError, TypeError) as ex:
            return _r(False, "DI-05", f"no se pudo completar el diario: {type(ex).__name__}", diario=None)
        return _r(True, "OK", "estado cargado y diario aplicado", diario=d, aplicadas=aplicadas, linea_incompleta=incompleta)
    d = Diario(o, ruta_estado, ruta_diario, lineas[-1]["hash"], lineas[-1]["n"])
    if reescribir:
        try:
            _reescribir(ruta_diario, lineas)
        except (OSError, ValueError, TypeError) as ex:
            return _r(False, "DI-05", f"no se pudo quitar la línea cortada: {type(ex).__name__}", diario=None)
    return _r(True, "OK", "estado cargado y diario aplicado", diario=d, aplicadas=aplicadas, linea_incompleta=incompleta)


def _reescribir(ruta_diario, lineas):
    _escribir_atomico(ruta_diario, "".join(json.dumps(e, ensure_ascii=True, separators=(",", ":")) + "\n" for e in lineas))
