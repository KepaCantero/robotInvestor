"""Migraciones del estado guardado entre versiones del código (T-03, cuarta parte; V0.46). Determinista, sin red.

Un estado guardado (persistencia, V0.42) solo lo puede cargar el código que lo guardó: una clave nueva en la configuración, un
atributo nuevo del Orquestador o un parámetro, una constante o una versión de reglas distintos lo dejan inservible (PE-03, PE-04
o CONFIG con kill-switch). Desde V0.46 cada documento lleva el esquema del código que lo escribió (`persistencia.esquema_actual`)
y un estado de otro esquema no se carga (PE-08): se migra aquí, de forma explícita y solo por el operador.

- `esquemas_codigo.json` (junto a este módulo) guarda, para cada esquema conocido, su parte de código (`persistencia.
  parte_de_codigo`): con ella se rehace la huella de configuración de un estado de ese código y se comprueba que nadie la tocó
  antes de migrarlo. Se añade el del código actual con `python3 validador/migraciones.py --registrar-esquema "V0.xx"`.
- `MIGRACIONES` es el registro fijo de migraciones: cada una parte de un formato y un esquema y llega a otro esquema, con una
  función pura sobre una copia del estado (el diccionario JSON) y la lista de rutas del estado que puede cambiar ("cfg.x.y",
  "expedientes"…). Las funciones escriben valores literales: no leen CONFIG_DEFECTO, que cambia con el código. De cada formato y
  esquema sale como mucho una migración, así que el camino es único.
- `migrar(texto, ahora, motivo, clave)` verifica el documento (forma, firma, huella), comprueba la huella de configuración con el
  código que lo guardó, aplica el camino, exige que todo lo que cambia esté declarado (y nunca el registro de límites, el
  kill-switch, los rearmes, el reloj ni el límite de pérdida), monta el estado con el código actual, anota una entrada MIGRACION
  en el registro encadenado de límites (huella de configuración nueva) y devuelve el texto en el formato actual. Nunca lanza.
- `migrar_ficheros(ruta_estado, ruta_diario, ahora, motivo, clave)` hace lo mismo con los ficheros: solo con el diario cerrado (una
  sola línea PUNTO), guarda una copia del estado anterior, escribe el estado nuevo y luego el diario con un PUNTO nuevo; si se corta
  entre los dos, volver a llamarla lo completa (también con un código más nuevo).

Códigos (fallan cerrado; además los de la persistencia y el diario al leer):
  MG-01 no hay camino de migración (o el registro de migraciones o de esquemas está mal formado o no tiene el esquema de origen).
  MG-02 el estado no está íntegro antes o después de migrar (también su huella de configuración con el código que lo guardó), o
        el resultado no se volvería a cargar o pasa del tamaño máximo.
  MG-03 una migración falla (lanza o no devuelve un estado que JSON guarde tal cual).
  MG-04 la migración cambia, quita o añade algo del estado que no declara, o algo que no se puede cambiar.
  MG-05 instante ilegible o anterior al reloj del Orquestador, motivo fuera de 15 a 500 caracteres o actor que no es el operador.
  MG-06 el diario no está cerrado en un punto de control del fichero de estado (hay que abrirlo con el código anterior y hacer
        punto()), o no corresponde al estado.

Cada vez que cambie el esquema del código (por ejemplo, al integrar piezas nuevas) se registra el esquema nuevo y una migración
que llegue a él: pruebas_migraciones_t03.py falla mientras el esquema del código no esté registrado y alcanzable.
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import math
from datetime import timezone

import diario as di
from control_f import divisa_cotizada, tipo_cambio
import persistencia as pe
from orquestador import CONFIG_DEFECTO, LIMITE_PERDIDA, Orquestador, _canon, _dt, _hash, _motivo_ok

RUTA_ESQUEMAS = Path(__file__).resolve().parent / "esquemas_codigo.json"
# esquema del código de V0.36 a V0.49 (los documentos 0.1.0 no lo llevan: se entiende este)
ESQUEMA_V0_45 = "04a549790220df9cc4d040ec55e7d9e1968635c3b450aa65495c6aaa5fc68527"
# esquema de V0.50 (T-18: L3, umbral_l2_eur, CFG-0.9.0)
ESQUEMA_V0_50 = "5879fc70d7018821d33e470a71392630f8c5d28b2afad73811ba39ab10712f65"
# esquema de V0.51 (T-18: promocion_nivel, CFG-0.10.0)
ESQUEMA_V0_51 = "a52f1c6e72bfcd9590e93258b119547734d5af3b28a01f80fb691eed290d1985"
# esquema de V0.53 (integración de las piezas de GLM V0.37-V0.41: libres_tope_dia_eur, libres, cortacircuitos; CFG-0.11.0)
ESQUEMA_V0_53 = "0a18459ec3066ff9ddd17b2e06bda9c41abf40a110191e014aad136cb807eaa2"
# esquema de V0.67 (integración del kit 2 de GLM, V0.60-V0.66, más el tope de líneas del diario del panel en parametros.py)
ESQUEMA_V0_67 = "f3943b0d923b81f423256f435e1db04f352c8ebf6d0962fd2dc5f37b5853086e"
# lo que una migración nunca puede cambiar, aunque lo declare (revisión de V0.46, hallazgos 5 y 10)
PROHIBIDAS = ("limites", "kill", "rearmes", "ultimo_ahora", "huella_config", f"cfg.politica_f.{LIMITE_PERDIDA}",
              "cfg.nivel_autonomia")   # V0.51 (revisión, duda 2): ninguna migración sube ni baja el nivel de nadie


@dataclass(frozen=True)
class Migracion:
    id: str
    formato_desde: str
    esquema_desde: str
    esquema_hasta: str
    aplicar: Callable[[dict], dict]
    cambia: frozenset = frozenset()   # rutas del estado que puede cambiar ("cfg.politica_f", "expedientes"…)
    descripcion: str = ""


def _sin_cambios(estado):
    return estado


def _v050(estado):
    """V0.45 → V0.50 (T-18): la configuración guardada recibe umbral_l2_eur con el valor de partida de V0.50 (literal) y, si
    llevaba la versión por defecto de V0.45, pasa a CFG-0.9.0. Nada más cambia: el nivel de cada cartera sigue siendo el que era."""
    cfg = estado["cfg"]
    cfg["umbral_l2_eur"] = {"TRADING": 5000.0, "TACTICA": 5000.0, "LARGO_PLAZO": 5000.0}
    if cfg.get("version_config") == "CFG-0.7.0":
        cfg["version_config"] = "CFG-0.9.0"
    return estado


def _v051(estado):
    """V0.50 → V0.51 (T-18): la configuración guardada recibe promocion_nivel con el valor de partida de V0.51 (literal) y, si
    llevaba la versión por defecto de V0.50, pasa a CFG-0.10.0; el estado recibe ultimas_degradaciones vacío. El nivel de cada
    cartera no cambia."""
    cfg = estado["cfg"]
    cfg["promocion_nivel"] = {"periodo_min_dias": 30}
    estado["ultimas_degradaciones"] = {}   # no se sabe cuándo se pidió degradar antes: vacío (los O-19 de L2 y L3 están en los avisos)
    if cfg.get("version_config") == "CFG-0.9.0":
        cfg["version_config"] = "CFG-0.10.0"
    return estado


def _v053(estado):
    """V0.51 → V0.53 (integración de GLM): la configuración guardada recibe libres_tope_dia_eur (T-33) con su valor de partida
    (literal) y, si llevaba la versión por defecto de V0.51/V0.52, pasa a CFG-0.11.0. El estado recibe la lista de días con
    cortacircuito (T-40) vacía (antes no saltaba) y la de LIBRES (T-33) reconstruida desde los registros manuales LIBRE que ya
    guardaba (revisión de la integración, h03: si no, las de hoy dejarían de contar en F-14 y en su tope). Su importe se valora
    como lo hace el Orquestador, con la última foto de G (None si no se puede: cuenta como el importe máximo del día en F-14), y
    como instante de registro se toma su emisión, que nunca es posterior (F-14 la cuenta en más contextos, no en menos)."""
    cfg = estado["cfg"]
    cfg["libres_tope_dia_eur"] = {"TRADING": 2000.0, "TACTICA": 2000.0, "LARGO_PLAZO": 2000.0}
    estado["cortacircuitos"] = []
    libres = []
    for m in estado.get("manuales", []):
        if not (isinstance(m, dict) and isinstance(m.get("vinculo"), dict) and m["vinculo"].get("tipo") == "LIBRE"):
            continue
        fx = tipo_cambio(divisa_cotizada(m["instrumento"], cfg.get("divisas_cotizacion") or {}), estado.get("ultima_foto"))
        try:
            importe = m["cantidad"] * m["precio"] * fx if fx is not None else None
        except (TypeError, OverflowError):
            importe = None
        if importe is not None and not (math.isfinite(importe) and importe > 0):
            importe = None
        libres.append({"cartera": m["cartera"], "dia": _dt(m["ejecutado_en"]).astimezone(timezone.utc).date().isoformat(),
                       "importe_eur": importe, "registrado_en": m["emitido_en"], "event_id": m["event_id"]})
    estado["libres"] = libres
    if cfg.get("version_config") == "CFG-0.10.0":
        cfg["version_config"] = "CFG-0.11.0"
    return estado


MIGRACIONES = (
    Migracion("MIG-001", pe.FORMATO_010, ESQUEMA_V0_45, ESQUEMA_V0_45, _sin_cambios, frozenset(),
              "formato 0.1.0 (V0.42 a V0.45) a 0.2.0: la cabecera lleva el esquema; el estado no cambia"),
    Migracion("MIG-002", pe.FORMATO, ESQUEMA_V0_45, ESQUEMA_V0_50, _v050, frozenset({"cfg.umbral_l2_eur"}),
              "V0.45 a V0.50 (T-18): umbral_l2_eur con su valor de partida y CFG-0.9.0; L3 nuevo, sin cambiar el nivel de nadie"),
    Migracion("MIG-003", pe.FORMATO, ESQUEMA_V0_50, ESQUEMA_V0_51, _v051, frozenset({"cfg.promocion_nivel"}),
              "V0.50 a V0.51 (T-18): promocion_nivel con su valor de partida y CFG-0.10.0; el nivel de cada cartera no cambia"),
    Migracion("MIG-004", pe.FORMATO, ESQUEMA_V0_51, ESQUEMA_V0_53, _v053, frozenset({"cfg.libres_tope_dia_eur", "libres"}),
              "V0.51 a V0.53 (integración de GLM): libres_tope_dia_eur con su valor de partida, listas vacías de LIBRES y "
              "cortacircuitos, y CFG-0.11.0"),
    Migracion("MIG-005", pe.FORMATO, ESQUEMA_V0_53, ESQUEMA_V0_67, _sin_cambios, frozenset(),
              "V0.53 a V0.67 (integración del kit 2 de GLM): solo cambia el código (n_lineas_diario_ambar en parametros.py); "
              "el estado guardado no cambia"),
)


def cargar_esquemas(ruta=RUTA_ESQUEMAS):
    """{esquema: {"version", "parte"}} del fichero de registro; {} si no se puede leer (y entonces nada se migra: MG-01)."""
    try:
        with open(ruta, encoding="ascii") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError, UnicodeDecodeError):
        return {}


ESQUEMAS = cargar_esquemas()


def _r(ok, codigo, motivo, **extra):
    return {"ok": ok, "codigo": codigo, "motivo": motivo, **extra}


def _no(codigo, motivo):
    return _r(False, codigo, motivo, texto=None, orquestador=None, migraciones=[])


def esquema_de(doc):
    """El esquema que declara un documento verificado (0.1.0: el de V0.36 a V0.46)."""
    return doc.get("esquema") if doc["formato"] == pe.FORMATO else ESQUEMA_V0_45


def _registro_ok(registro):
    return (isinstance(registro, (tuple, list)) and all(
        isinstance(m, Migracion) and all(isinstance(x, str) for x in (m.id, m.formato_desde, m.esquema_desde, m.esquema_hasta))
        and callable(m.aplicar) and isinstance(m.cambia, frozenset) and all(isinstance(c, str) and c for c in m.cambia) for m in registro)
        and len({m.id for m in registro}) == len(registro))


def camino(formato, esquema, actual, registro=MIGRACIONES):
    """Lista de migraciones desde (formato, esquema) hasta el formato actual y `actual`, o None si no hay camino (ninguna
    migración aplicable, más de una, un ciclo o un registro mal formado)."""
    if not _registro_ok(registro):
        return None
    pasos = []
    for _ in range(len(registro) + 1):
        if formato == pe.FORMATO and esquema == actual:
            return pasos
        aplicables = [m for m in registro if m.formato_desde == formato and m.esquema_desde == esquema]
        if len(aplicables) != 1:
            return None
        pasos.append(aplicables[0])
        formato, esquema = pe.FORMATO, aplicables[0].esquema_hasta
    return None


def _diferencias(antes, despues, ruta=""):
    """[(ruta, tipo)] con tipo "cambia", "quita" o "nueva", bajando por los diccionarios (las listas se comparan enteras)."""
    out = []
    for k, v in antes.items():
        r = f"{ruta}.{k}" if ruta else k
        if k not in despues:
            out.append((r, "quita"))
        elif isinstance(v, dict) and isinstance(despues[k], dict):
            out += _diferencias(v, despues[k], r)
        elif type(v) is not type(despues[k]) or _canon(v) != _canon(despues[k]):
            out.append((r, "cambia"))
    out += [(f"{ruta}.{k}" if ruta else k, "nueva") for k in despues if k not in antes]
    return out


def _bajo(ruta, prefijos):
    return any(ruta == c or ruta.startswith(c + ".") for c in prefijos)


def migrar(texto, ahora, motivo, clave=None, actor="OPERADOR", registro=MIGRACIONES, esquemas=None) -> dict:
    """Migra el texto de un estado guardado al formato y esquema de este código. Nunca lanza. Devuelve {ok, codigo, motivo,
    texto, orquestador, migraciones}: si no hay nada que migrar, ok con migraciones [] y el texto de entrada."""
    try:
        return _migrar(texto, ahora, motivo, clave, actor, registro, ESQUEMAS if esquemas is None else esquemas)
    except Exception as ex:   # noqa: BLE001 — anidamientos extremos, registros raros… (revisión de V0.46, hallazgos 2 y 6)
        return _no("MG-02", f"no se pudo comprobar o migrar el estado: {type(ex).__name__}")


def _migrar(texto, ahora, motivo, clave, actor, registro, esquemas):
    if not isinstance(texto, str):
        return _no("PE-01", "el estado a migrar debe ser texto")
    if not pe._instante_ok(ahora) or _dt(ahora).year >= 2100:   # V0.49 (revisión, hallazgo 9): como el reloj, nada desde 2100
        return _no("MG-05", "instante de la migración ilegible o fuera de lo plausible")
    if not _motivo_ok(motivo):
        return _no("MG-05", "la migración necesita un motivo de 15 a 500 caracteres")
    if actor != "OPERADOR":   # hallazgo 11: solo el operador cambia la huella de la configuración
        return _no("MG-05", "solo el operador migra el estado")
    doc, err = pe.verificar(texto, clave)
    if err:
        return {**err, "texto": None, "migraciones": []}
    est0 = doc["estado"]
    actual = pe.esquema_actual()
    pasos = camino(doc["formato"], esquema_de(doc), actual, registro)
    if pasos is None:
        return _no("MG-01", f"no hay camino de migración desde {doc['formato']} con el esquema {str(esquema_de(doc))[:12]}… hasta el de "
                            f"este código ({actual[:12]}…), o el registro de migraciones está mal formado")
    if not pasos:
        return _r(True, "OK", "el estado ya es de este código: nada que migrar", texto=texto, orquestador=None, migraciones=[])
    # la huella de configuración, rehecha con el código que guardó el estado (hallazgo 1): una configuración tocada no se blanquea
    origen = esquemas.get(esquema_de(doc)) if isinstance(esquemas, dict) else None
    parte = origen.get("parte") if isinstance(origen, dict) else None
    if not (isinstance(parte, dict) and pe.esquema_de_parte(parte) == esquema_de(doc) and isinstance(parte.get("codigo"), dict)):
        return _no("MG-01", "el esquema de origen no está en el registro de esquemas: no se puede comprobar su configuración")
    cfg0 = est0.get("cfg")
    if not isinstance(cfg0, dict):
        return _no("MG-02", "el estado no tiene configuración")
    completa0 = {"version_config": cfg0.get("version_config"), "orquestador": cfg0, "calendario": est0.get("cal_def"), **parte["codigo"]}
    if _hash(_canon(completa0)) != est0.get("huella_config"):
        return _no("MG-02", "la configuración guardada no es la de su huella con el código que la guardó: se tocó; ábrelo con ese código")
    est = copy.deepcopy(est0)
    for m in pasos:
        try:
            est = m.aplicar(copy.deepcopy(est))
        except Exception as ex:   # noqa: BLE001
            return _no("MG-03", f"{m.id} falla: {type(ex).__name__}")
        if not (isinstance(est, dict) and pe._solo_json(est)):
            return _no("MG-03", f"{m.id} no devuelve un estado que JSON guarde tal cual")
    ids = [m.id for m in pasos]
    cambia = frozenset().union(*(m.cambia for m in pasos)) | {"cfg.version_config"}
    cfg1 = est.get("cfg")
    if not isinstance(cfg1, dict):
        return _no("MG-04", "la migración deja el estado sin configuración")
    # todo lo que cambia tiene que estar declarado (hallazgos 4, 5 y 10); sin declararlo solo se puede añadir un atributo nuevo del
    # Orquestador o una clave nueva de la configuración con el valor de este código; lo prohibido no cambia nunca
    fresco = vars(Orquestador(pe.CFG_ESQUEMA, pe.CAL_ESQUEMA))   # sin datos del operador
    indebidos = []
    for ruta, tipo in _diferencias(est0, est):
        if _bajo(ruta, PROHIBIDAS):
            indebidos.append(ruta)
        elif _bajo(ruta, cambia):
            continue
        elif tipo == "nueva" and "." not in ruta and _canon(est[ruta]) == _canon(fresco.get(ruta)):
            continue
        elif tipo == "nueva" and ruta.count(".") == 1 and ruta.startswith("cfg.") and ruta[4:] in CONFIG_DEFECTO \
                and _canon(cfg1[ruta[4:]]) == _canon(CONFIG_DEFECTO[ruta[4:]]):
            continue
        else:
            indebidos.append(ruta)
    if indebidos:
        return _no("MG-04", f"la migración cambiaría lo que no declara o no se puede cambiar: {indebidos[:5]}")
    nuevo = {"formato": pe.FORMATO, "esquema": actual, "version_config": cfg1.get("version_config"), "guardado_en": ahora,
             "atributos": sorted(est), "estado": est}
    o, err = pe.montar(nuevo)
    if err:
        return {**err, "motivo": f"el estado migrado no se monta con este código: {err['motivo']}", "texto": None, "migraciones": []}
    rotos = o.integridad()
    # antes de anotar: solo puede fallar la huella de la configuración (la del código anterior, ya comprobada); lo encadenado y el
    # registro de límites tienen que cuadrar
    if set(rotos) - {"CONFIG"} or not o._limites_ok():
        return _no("MG-02", f"el estado no está íntegro: {(sorted(set(rotos) - {'CONFIG'}) or ['registro de límites'])[:5]}; "
                            "ábrelo con el código que lo guardó")
    if o.ultimo_ahora is not None and _dt(ahora) < _dt(o.ultimo_ahora):
        return _no("MG-05", f"el instante de la migración es anterior al reloj del Orquestador ({o.ultimo_ahora})")
    antes = o.huella_config
    o.huella_config = _hash(_canon(o._configuracion_completa()))
    o._anota_limite({"tipo": "MIGRACION", LIMITE_PERDIDA: o.cfg["politica_f"][LIMITE_PERDIDA], "huella_config": o.huella_config,
                     "huella_antes": antes, "esquema_antes": esquema_de(doc), "esquema_despues": actual, "migraciones": ids,
                     "fichero_antes": hashlib.sha256(texto.encode("utf-8")).hexdigest(), "motivo": motivo},
                    actor, ahora, f"estado migrado a este código ({', '.join(ids)}): {motivo[:120]}")
    o.ultimo_ahora = ahora
    rotos = o.integridad()
    if rotos:
        return _no("MG-02", f"el estado migrado no cuadra: {rotos[:5]}")
    salida = pe.volcar(o, ahora, clave)
    if len(salida) > pe.MAX_BYTES:   # hallazgo 9: no se deja un estado que luego no se podría leer
        return _no("MG-02", f"el estado migrado pasaría de {pe.MAX_BYTES} bytes")
    prueba = pe.cargar(salida, clave)
    if not prueba["ok"]:
        return _no("MG-02", f"el estado migrado no se volvería a cargar: {prueba['codigo']} {prueba['motivo']}")
    return _r(True, "OK", f"estado migrado ({', '.join(ids)})", texto=salida, orquestador=prueba["orquestador"], migraciones=ids)


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
    huella = json.loads(texto)["huella"]
    linea = di._linea({"n": 1, "tipo": "PUNTO", "estado": huella, "fichero": hashlib.sha256(texto.encode("utf-8")).hexdigest()}, di.CERO, clave)
    return json.dumps(linea, ensure_ascii=True, separators=(",", ":")) + "\n"


def _ultima_migracion(texto):
    """La última entrada del registro de límites si es una MIGRACION (del texto ya verificado por migrar o cargar)."""
    try:
        ent = json.loads(texto)["estado"]["limites"]["entradas"]
        return ent[-1] if ent and isinstance(ent[-1], dict) and ent[-1].get("tipo") == "MIGRACION" else None
    except (ValueError, KeyError, TypeError, IndexError):
        return None


def migrar_ficheros(ruta_estado, ruta_diario, ahora, motivo, clave=None, actor="OPERADOR", registro=MIGRACIONES, esquemas=None) -> dict:
    """Migra el fichero de estado y deja el diario en un punto de control del estado migrado. Nunca lanza. Devuelve {ok, codigo,
    motivo, migraciones, completada, copia}: completada=True si solo terminó una migración que se había cortado a medias; copia es
    la ruta donde quedó el estado anterior."""
    try:
        return _migrar_ficheros(ruta_estado, ruta_diario, ahora, motivo, clave, actor, registro, esquemas)
    except Exception as ex:   # noqa: BLE001
        return _r(False, "MG-02", f"no se pudo migrar: {type(ex).__name__}", migraciones=[], completada=False, copia=None)


def _migrar_ficheros(ruta_estado, ruta_diario, ahora, motivo, clave, actor, registro, esquemas):
    def no(codigo, m, **x):
        return _r(False, codigo, m, **{"migraciones": [], "completada": False, "copia": None, **x})
    texto, err = _leer_estado(ruta_estado)
    if err:
        return no(err["codigo"], err["motivo"])
    lineas, _, _, err = di._leer(ruta_diario, clave)
    if err:
        return no(err["codigo"], err["motivo"])
    if not lineas:
        return no("DI-02", "el diario no tiene ninguna línea completa")
    sha = hashlib.sha256(texto.encode("utf-8")).hexdigest()
    r = migrar(texto, ahora, motivo, clave, actor, registro, esquemas)
    if not r["ok"]:
        return no(r["codigo"], r["motivo"])
    cerrado = len(lineas) == 1 and lineas[0]["tipo"] == "PUNTO"
    previa = _ultima_migracion(texto)
    # el diario sigue en el PUNTO del fichero del que se migró la última vez (una migración cortada entre el estado y el diario)
    cortada = cerrado and previa is not None and previa.get("fichero_antes") == lineas[0]["fichero"] != sha
    if r["migraciones"]:
        if not cerrado:
            return no("MG-06", "el diario tiene operaciones después de su punto de control: ábrelo con el código que lo escribió y "
                               "haz punto() antes de migrar")
        propio = lineas[0]["fichero"] == sha and lineas[0]["estado"] == json.loads(texto)["huella"]
        if not (propio or cortada):   # hallazgo 8: también si una migración anterior se cortó y llega un código más nuevo
            return no("MG-06", "el punto de control del diario no es el del fichero de estado")
        copia = f"{ruta_estado}.antes-{sha[:16]}"   # hallazgo 9: el estado anterior no se pierde
        try:
            di._escribir_atomico(copia, texto)
            di._escribir_atomico(ruta_estado, r["texto"])
            di._escribir_atomico(ruta_diario, _punto(r["texto"], clave))
        except (OSError, ValueError, TypeError) as ex:
            return no("PE-05", f"no se pudo escribir la migración: {type(ex).__name__}; vuelve a llamar a migrar_ficheros", copia=copia)
        return _r(True, "OK", r["motivo"], migraciones=r["migraciones"], completada=False, copia=copia)
    # el estado ya es de este código: nada que hacer si el diario es suyo; si se cortó una migración, se completa el diario
    if any(e["tipo"] == "PUNTO" and e["fichero"] == sha for e in lineas):
        return _r(True, "OK", "el estado ya es de este código: nada que migrar", migraciones=[], completada=False, copia=None)
    if not cortada:
        return no("MG-06", "el diario no tiene un punto de control del fichero de estado ni de aquel del que se migró")
    try:
        di._escribir_atomico(ruta_diario, _punto(texto, clave))
    except (OSError, ValueError, TypeError) as ex:
        return no("PE-05", f"no se pudo escribir el diario: {type(ex).__name__}")
    return _r(True, "OK", "migración cortada completada: diario en el punto de control del estado migrado",
              migraciones=list(previa.get("migraciones", [])), completada=True, copia=None)


def registrar_esquema_actual(version, ruta=RUTA_ESQUEMAS) -> str:
    """Añade al registro de esquemas el del código actual (al cambiar el código, junto con su migración). Devuelve el esquema."""
    d = cargar_esquemas(ruta)
    parte = pe.parte_de_codigo()
    e = pe.esquema_de_parte(parte)
    d.setdefault(e, {"version": version, "parte": parte})
    with open(ruta, "w", encoding="ascii") as f:
        f.write(json.dumps(d, ensure_ascii=True, sort_keys=True, indent=1) + "\n")
    return e


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--registrar-esquema":
        print(registrar_esquema_actual(sys.argv[2]))
    else:
        print("uso: python3 validador/migraciones.py --registrar-esquema V0.xx")
