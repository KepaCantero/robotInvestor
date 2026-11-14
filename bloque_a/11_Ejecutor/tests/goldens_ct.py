"""T-114 · Fase 3: goldens de los contratos CT-01 a CT-25 del Bloque A.

Genera el texto exacto de cada golden a partir del código (`bloque_a/contratos.py`), de los esquemas derivados del
Anexo B (`goldens/anexo_b_esquemas.json`, escritos a mano), de una batería fija de mensajes válidos e inválidos
(`goldens/bateria_mensajes.json`, escrita a mano) y de los flujos simulados del ejecutor (dos ciclos semanales V5, uno
V6, consultas, petición ad hoc, decisión del Broker, seguimiento encargado, consulta al Broker y credenciales). Las pruebas
(`test_fase3_goldens.py`) comparan ese texto, byte a byte, con los ficheros de `goldens/`.

Uso, desde `bloque_a/11_Ejecutor`:
    python tests/goldens_ct.py                          comprueba; termina con 1 si algo difiere
    python tests/goldens_ct.py --update --motivo "…"    re-congela (solo deliberado) y lo anota en REGISTRO.md

La regla de re-congelado está en `goldens/README.md`.
"""
from __future__ import annotations

import argparse
import contextlib
import copy
import datetime as dt
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

import jsonschema

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent                 # bloque_a/11_Ejecutor
BLOQUE = RAIZ.parent               # bloque_a
for _ruta in (str(RAIZ), str(AQUI)):
    if _ruta not in sys.path:
        sys.path.insert(0, _ruta)

from bloque_a.almacen import Almacen, Reloj

from bloque_a import contratos

CARPETA = AQUI / "goldens"
A_MANO = ("anexo_b_esquemas.json", "anexo_b_ejemplos.json", "bateria_mensajes.json")
GENERADOS = ("tablas_contratos.json", "esquemas_respuestas.json", "mensajes_ejemplo.json", "aceptaciones_rechazos.json",
             "formas_flujos_mock.json", "divergencias_anexo_b.json", "huellas.json")
DOCUMENTOS = ("README.md", "REGISTRO.md")
MARCA = "derivado del Anexo B"
RUN_EJEMPLO = "RUN-2026-0001"
# Campos comunes de todo mensaje (primer párrafo del Anexo B y `Mensajeria.crear`): no cuentan como diferencia
SOBRE = frozenset({"msg_id", "contrato", "version_contrato", "emisor", "receptor", "run_id", "query_id", "timestamp", "tipo_mensaje",
                   "presupuesto", "consumo", "estado", "limitaciones", "autoevaluacion", "consultas_broker",
                   "solicitudes_credenciales", "supuestos_declarados"})


def texto(obj) -> str:
    """Forma canónica de un golden: claves ordenadas, sangría de un espacio, UTF-8 sin escapes y salto final."""
    return json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def _canales(tabla: dict) -> dict:
    return {ct: [{"emisores": sorted(em), "receptores": sorted(rc)} for em, rc in pares] for ct, pares in tabla.items()}


def tablas() -> dict:
    """Las tablas de `contratos.py` que definen qué contratos hay, por dónde viajan y qué campos exigen."""
    return {"version_contrato": contratos.VERSION_CONTRATO, "estados": list(contratos.ESTADOS),
            "campo_estado": dict(contratos.CAMPO_ESTADO),
            "estados_especificos": {k: list(v) for k, v in contratos.ESTADOS_ESPECIFICOS.items()},
            "canales": _canales(contratos.CANALES), "canales_v6": _canales(contratos.CANALES_V6),
            "campos_minimos": {k: list(v) for k, v in contratos.CAMPOS_MINIMOS.items()},
            "campos_retorno": {k: list(v) for k, v in contratos.CAMPOS_RETORNO.items()}}


def esquemas_respuestas() -> dict:
    return json.loads(json.dumps(contratos.ESQUEMAS))


def leer_a_mano(carpeta: Path = CARPETA) -> tuple[dict, dict]:
    esquemas = json.loads((carpeta / A_MANO[0]).read_text(encoding="utf-8"))
    ejemplos = json.loads((carpeta / A_MANO[1]).read_text(encoding="utf-8"))
    return esquemas, ejemplos


def sin_campos_en_anexo_b(esquemas: dict) -> list[str]:
    """Contratos en vigor de los que el Anexo B no nombra ningún campo (los remite a los prompts de sistema)."""
    con = {clave.split(".")[0] for clave in esquemas}
    return sorted(set(contratos.CANALES) - con)


def _canal(ct: str, sentido: str) -> tuple[str, str]:
    """Emisor y receptor del ejemplo: el primer canal del contrato; el retorno vuelve por él si el canal lo permite."""
    emisores, receptores = contratos.CANALES[ct][0]
    em, rc = min(emisores), min(receptores)
    if sentido == "RETORNO" and contratos.canal_permitido(ct, rc, em):
        return rc, em
    return em, rc


def _mensajeria(carpeta: Path, fecha: str):
    reloj = Reloj()
    reloj.fijar(fecha)
    return contratos.Mensajeria(Almacen(carpeta, reloj))


def _crear(mensajeria, clave: str, cuerpo: dict) -> dict:
    """Crea el mensaje de un cuerpo del Anexo B por el canal del contrato. Los campos del sobre que el Anexo B pone en el
    cuerpo (`run_id`, `query_id`, `presupuesto`, `consumo`) se pasan por su sitio, como hace el ejecutor."""
    ct, sentido = clave.split(".")
    em, rc = _canal(ct, sentido)
    run_id = cuerpo.get("run_id") or (None if cuerpo.get("query_id") else RUN_EJEMPLO)
    try:
        msg = mensajeria.crear(ct, em, rc, cuerpo, run_id=run_id, query_id=cuerpo.get("query_id"),
                               presupuesto=cuerpo.get("presupuesto"), consumo=cuerpo.get("consumo"), tipo_mensaje=sentido)
        return {"mensaje": msg}
    except (ValueError, PermissionError) as e:
        return {"rechazo": {"clase": type(e).__name__, "motivo": str(e)}}


def mensajes_ejemplo(ejemplos: dict, carpeta_tmp: Path, fecha: str) -> dict:
    """El mensaje que `Mensajeria.crear` construye con cada ejemplo del Anexo B, o la clase de su rechazo."""
    mensajeria = _mensajeria(Path(carpeta_tmp) / "estado_mensajes", fecha)
    return {clave: _crear(mensajeria, clave, ejemplos[clave]) for clave in sorted(ejemplos)}


# ---------------------------------------------------------------------------------------------------------------------
# Batería de aceptaciones y rechazos (QA r01, H-01 a): las reglas de valor de `Mensajeria.crear` y `validar` viven en el
# código, no en las tablas; aquí se congelan por su efecto. La batería es un fichero de datos escrito a mano.
# ---------------------------------------------------------------------------------------------------------------------
CAMPOS_CASO = frozenset({"que", "espera", "base", "contrato", "tipo_mensaje", "emisor", "receptor", "cuerpo", "pon", "quita",
                         "run_id", "query_id", "estado", "presupuesto", "consumo", "v6", "via", "mensaje_pon", "mensaje_quita"})
RESULTADOS = ("ADMITIDO", "RECHAZADO")


def leer_bateria(carpeta: Path = CARPETA) -> dict:
    return json.loads((carpeta / A_MANO[2]).read_text(encoding="utf-8"))["casos"]


def _caso(caso: dict, ejemplos: dict, carpeta: Path, fecha: str, modulo=contratos) -> tuple[dict, list[dict]]:
    """Resultado de un caso de la batería y la traza que deja. El caso parte de un ejemplo del Anexo B (`base`) o de un
    `cuerpo` propio; `pon` y `quita` lo cambian. Con `via: validar`, el mensaje se crea (tiene que admitirse), se cambia
    con `mensaje_pon` y `mensaje_quita` y se pasa a `Mensajeria.validar`. Un caso mal escrito es un error, no un rechazo.
    `modulo` es el módulo de contratos que se mide (las pruebas pasan copias cambiadas para ver que la batería lo nota)."""
    if set(caso) - CAMPOS_CASO or caso.get("espera") not in RESULTADOS or caso.get("via", "crear") not in ("crear", "validar"):
        raise ValueError(f"caso de la batería mal escrito: {sorted(caso)}")
    if ("base" in caso) == ("cuerpo" in caso):
        raise ValueError("un caso lleva `base` o `cuerpo`, uno de los dos")
    base = caso.get("base")
    cuerpo = copy.deepcopy(ejemplos[base] if base else caso["cuerpo"])
    cuerpo.update(copy.deepcopy(caso.get("pon", {})))
    for campo in caso.get("quita", []):
        del cuerpo[campo]
    ct = caso.get("contrato") or base.split(".")[0]
    sentido = caso.get("tipo_mensaje") or base.split(".")[1]
    if "emisor" in caso or "receptor" in caso:
        em, rc = caso["emisor"], caso["receptor"]
    else:
        em, rc = _canal(ct, sentido)
    run_id = caso["run_id"] if "run_id" in caso else cuerpo.get("run_id") or (None if cuerpo.get("query_id") else RUN_EJEMPLO)
    query_id = caso["query_id"] if "query_id" in caso else cuerpo.get("query_id")
    reloj = Reloj()
    reloj.fijar(fecha)
    mensajeria = modulo.Mensajeria(Almacen(carpeta, reloj), v6=bool(caso.get("v6", False)))

    def crear():
        return mensajeria.crear(ct, em, rc, cuerpo, run_id=run_id, query_id=query_id,
                                presupuesto=caso.get("presupuesto", cuerpo.get("presupuesto")),
                                consumo=caso.get("consumo", cuerpo.get("consumo")), estado=caso.get("estado"), tipo_mensaje=sentido)

    try:
        if caso.get("via", "crear") == "crear":
            return {"resultado": "ADMITIDO", "mensaje": crear()}, list(mensajeria.registro)
        try:
            msg = crear()
        except (ValueError, PermissionError) as e:
            raise ValueError(f"un caso `via: validar` parte de un mensaje que se admite: {e}") from None
        msg.update(copy.deepcopy(caso.get("mensaje_pon", {})))
        for campo in caso.get("mensaje_quita", []):
            del msg[campo]
        mensajeria.validar(msg)
        return {"resultado": "ADMITIDO"}, []
    except (modulo.MensajeInvalido, modulo.CanalNoPrevisto, modulo.DatosSensibles) as e:
        return {"resultado": "RECHAZADO", "clase": type(e).__name__, "motivo": str(e)}, []


def aceptaciones(bateria: dict, ejemplos: dict, carpeta_tmp: Path, fecha: str, modulo=contratos) -> dict:
    """Qué hace `Mensajeria` con cada caso de la batería: el mensaje normalizado si lo admite, o la clase y el motivo del
    rechazo. Cada caso usa un almacén nuevo: su `msg_id` no depende de los demás casos."""
    casos, traza = {}, set()
    for n, nombre in enumerate(sorted(bateria)):
        casos[nombre], registro = _caso(bateria[nombre], ejemplos, Path(carpeta_tmp) / "bateria" / f"{n:04d}", fecha, modulo)
        traza |= {clave for entrada in registro for clave in entrada}
    return {"casos": casos, "claves_de_la_traza_de_mensajes": sorted(traza),
            "no_coinciden_con_lo_que_espera_la_bateria": sorted(n for n in casos if casos[n]["resultado"] != bateria[n]["espera"])}


# ---------------------------------------------------------------------------------------------------------------------
# Flujos simulados (QA r01, H-01 b y c): más flujos que el ciclo semanal, y de cada tipo de mensaje la ruta de cada clave
# con su tipo JSON.
# ---------------------------------------------------------------------------------------------------------------------
TODOS = "todos"
# Nombre del flujo → contratos que se guardan de él. De los flujos que lanzan un ciclo ad hoc por dentro (consulta que
# escala, petición) solo se guardan los contratos que el flujo añade: los del ciclo ya están en los ciclos semanales.
FLUJOS = {
    "ciclo_semanal_v5": TODOS,
    "consulta_n0": ("CT-03",),
    "consulta_que_escala": ("CT-03",),
    "pregunta_repetida": ("CT-03", "CT-22"),
    "peticion_ad_hoc": ("CT-01", "CT-02"),
    "decision_broker": ("CT-04", "CT-22"),
    "seguimiento_encargado": ("CT-05", "CT-06", "CT-22", "CT-24"),
    "consulta_al_broker": ("CT-22", "CT-23"),
    "credenciales": ("CT-25",),
    "informe_de_aprendizaje": ("CT-19",),
    "ciclo_semanal_v6": TODOS,
}
VALOR_DE_PRUEBA = "valor-de-prueba-no-es-una-clave"   # lo que el Broker deposita en la bóveda simulada; nunca va en un mensaje


class _Captura:
    """Anota, flujo a flujo, los mensajes que crea la mensajería de un bloque."""

    def __init__(self) -> None:
        self.flujos: dict[str, list[dict]] = {nombre: [] for nombre in FLUJOS}
        self._abierto: str | None = None

    def espiar(self, bloque) -> None:
        crear = bloque.mensajeria.crear

        def crear_y_anotar(*args, **kwargs):
            msg = crear(*args, **kwargs)
            nombre = self._abierto
            if nombre is not None and (FLUJOS[nombre] == TODOS or msg["contrato"] in FLUJOS[nombre]):
                self.flujos[nombre].append(json.loads(json.dumps(msg, default=str)))
            return msg

        bloque.mensajeria.crear = crear_y_anotar

    @contextlib.contextmanager
    def flujo(self, nombre: str):
        self._abierto = nombre
        try:
            yield
        finally:
            self._abierto = None


def _mas_dias(fecha: str, dias: int) -> str:
    return (dt.date.fromisoformat(fecha) + dt.timedelta(days=dias)).isoformat()


def capturar_flujos(carpeta_tmp: Path, fecha: str) -> dict[str, list[dict]]:
    """Los mensajes que crean los flujos del ejecutor con `MockClient` y los doce perfiles de las pruebas. Las llamadas son
    las de `test_integracion.py`, `test_v51.py` y `test_t101_v6.py`. La auditoría se activa también en modo backtest para
    que el ciclo emita CT-16 y CT-17."""
    import conftest
    from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
    from bloque_a.herramientas.ht01_datos import cargar_universo

    universo = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
    semana2 = _mas_dias(fecha, 7)
    captura = _Captura()

    # ---- un bloque V5: dos ciclos semanales y, sobre su memoria, lo que el Broker pregunta, pide y decide
    b = conftest.nuevo_bloque(Path(carpeta_tmp) / "v5", universo, cfg=conftest.config_pruebas(auditoria={"en_backtest": True}))
    captura.espiar(b)
    with captura.flujo("ciclo_semanal_v5"):
        b.ciclo(fecha)
    with captura.flujo("consulta_n0"):
        b.consulta("¿Por qué no aparece ninguna opción nueva de renta fija esta semana?", as_of=fecha)
    with captura.flujo("consulta_que_escala"):
        b.consulta("¿Qué opinas del oro frente a la plata a 6 meses?", as_of=fecha)
    with captura.flujo("pregunta_repetida"):
        for _ in range(3):   # a la tercera, aviso CT-22 y una lección de producto
            b.consulta("¿Cuál es el estado de las opciones vigentes?", as_of=fecha)
    with captura.flujo("ciclo_semanal_v5"):
        r2 = b.ciclo(semana2)     # el segundo ciclo ya lleva opciones vigentes y la lección
    opps = [o["opp_id"] for d in r2["paquete"]["clases"].values() for o in d["opciones"]]
    with captura.flujo("peticion_ad_hoc"):
        b.peticion(json.loads((RAIZ / "ejemplos" / "peticiones" / "peticion_ad_hoc.json").read_text(encoding="utf-8")), semana2)
    with captura.flujo("decision_broker"):
        b.decision({"decisiones": [{"opp_id": opps[0], "decision": "DESCARTADA", "motivo": "no encaja"}],
                    "valoracion_informe": {"run_id": r2["run_id"], "utilidad": 4, "comentario": "Claro."},
                    "configuracion": {"horizontes": ["H1", "H3"]}}, semana2)
        b.decision({"resultado_comunicado": {"opp_id": opps[0], "texto": "No se operó."}}, semana2)
    # ---- otro bloque V5: consulta al Broker, credenciales y, tras un ciclo corto que no se guarda, el seguimiento encargado
    b = conftest.nuevo_bloque(Path(carpeta_tmp) / "broker", universo)
    captura.espiar(b)
    with captura.flujo("consulta_al_broker"):
        cns = b.consultas.enviar({"tipo": "ACLARACION_ALCANCE", "modo": "BLOQUEANTE", "clases": ["CRI"],
                                  "preguntas": [{"texto": "¿Incluimos stablecoins?", "supuesto_declarado": "No se incluyen",
                                                 "efecto_si_falso": "Se ampliaría el cribado de CRI"}]}, fecha)["cns_id"]
        b.consultas.responder(cns, [{"indice": 0, "texto": "Sí, inclúyelas"}], as_of=fecha)
        recurrente = {"tipo": "DATO_O_DOCUMENTO", "modo": "NO_BLOQUEANTE", "run_id": "RUN-2026-0099",
                      "preguntas": [{"texto": "¿Tiene el último informe del fondo?", "supuesto_declarado": "Se usa el anterior"}]}
        for _ in range(3):   # tres iguales: aviso CT-22 de consulta recurrente
            b.consultas.enviar(dict(recurrente), fecha)
        b.consultas.entrante("El usuario prefiere excluir tabaco y armas", {"run_id": None}, fecha)
    with captura.flujo("credenciales"):
        crd = b.credenciales.solicitar("API de fondos cerrados", "AG-16", "Cribado FON", "Datos públicos semanales", as_of=fecha)["crd_id"]
        b.credenciales.depositar(crd, VALOR_DE_PRUEBA, _mas_dias(fecha, 365), fecha)
        crd = b.credenciales.solicitar("API de crédito privado", "AG-09", "Cribado ALT", "Sin descuentos de secundario", as_of=fecha)["crd_id"]
        b.credenciales.responder({"crd_id": crd, "estado": "DENEGADA", "credencial_ref": None}, fecha)
        b.credenciales.solicitar("API de opciones", "AG-23", "Volatilidad implícita", "Sin superficie de volatilidad", as_of=fecha)
        b.credenciales.recordatorios(_mas_dias(fecha, 8))
    opps = [o["opp_id"] for d in b.ciclo(fecha, alcance={"clases": ["RV", "MP"]})["paquete"]["clases"].values() for o in d["opciones"]]
    with captura.flujo("seguimiento_encargado"):
        seg = b.seguimientos.procesar({"accion": "ALTA", "opp_id": opps[0], "frecuencia": "SEMANAL", "motivo": "Vigilar sin enviar a B",
                                       "senales_interes": ["Momentum relativo"]}, fecha)["seg_id"]
        b.seguimientos.procesar({"accion": "ALTA", "opp_id": opps[1], "frecuencia": "DIARIA", "fecha_fin": _mas_dias(fecha, 3)}, fecha)
        b.seguimientos.ejecutar(semana2)      # un ciclo C6 del primero; el segundo ha llegado a su fecha de fin
        b.seguimientos.procesar({"accion": "PAUSA", "seg_id": seg}, semana2)
        b.seguimientos.procesar({"accion": "REANUDACION", "seg_id": seg}, semana2)
        b.seguimientos.procesar({"accion": "MODIFICACION", "seg_id": seg, "frecuencia": "MENSUAL"}, semana2)
        b.seguimientos.respuesta_broker(seg, "RECHAZADA", as_of=semana2)
        b.seguimientos.procesar({"accion": "CANCELACION", "seg_id": seg}, semana2)
    with captura.flujo("informe_de_aprendizaje"):
        b.ciclo(_mas_dias(fecha, 35), alcance={"clases": ["RV", "MP"]})   # cinco semanas después ya hay pronósticos resueltos

    # ---- un bloque del diseño V6: un ciclo semanal
    b = conftest.nuevo_bloque(Path(carpeta_tmp) / "v6", universo, cfg=conftest.config_pruebas(diseno="v6", auditoria={"en_backtest": True}))
    captura.espiar(b)
    with captura.flujo("ciclo_semanal_v6"):
        b.ciclo(fecha)
    return captura.flujos


def todos_los_mensajes(flujos: dict[str, list[dict]]) -> list[dict]:
    return [msg for nombre in sorted(flujos) for msg in flujos[nombre]]


TIPOS_JSON = {dict: "object", list: "array", str: "string", bool: "boolean", int: "integer", float: "number", type(None): "null"}
RE_CLAVE_ID = re.compile(r"[A-Z][A-Z0-9]*(-[A-Z0-9]+)*-[0-9]{4}-[0-9]+")


def _clave(clave: str) -> str:
    """Las claves que son datos y no formato (el código de un tipo de activo, un identificador) se escriben genéricas."""
    if clave in contratos.AGENTE_CLASE:
        return "<clase>"
    return "<id>" if RE_CLAVE_ID.fullmatch(clave) else clave


def rutas(mensajes: list[dict]) -> tuple[dict[str, str], dict[str, str]]:
    """La ruta de cada clave (anidadas incluidas; `x[]` es un elemento de la lista `x`) con sus tipos JSON, en dos grupos:
    las que están en todos los objetos que podrían llevarlas y las que solo en algunos. Una lista «siempre» tiene elementos
    si ninguna de las vistas está vacía."""
    contenedores: dict[str, int] = {}
    vistas: dict[str, list] = {}

    def anotar(padre: str, ruta: str, valor, cuenta: bool) -> None:
        dato = vistas.setdefault(ruta, [padre, 0, set()])
        dato[1] += cuenta
        dato[2].add(TIPOS_JSON[type(valor)])
        recorrer(valor, ruta)

    def recorrer(valor, ruta: str) -> None:
        if isinstance(valor, dict):
            contenedores[ruta] = contenedores.get(ruta, 0) + 1
            for clave, v in valor.items():
                anotar(ruta, f"{ruta}.{_clave(clave)}" if ruta else _clave(clave), v, True)
        elif isinstance(valor, list):
            contenedores[ruta] = contenedores.get(ruta, 0) + 1
            for n, v in enumerate(valor):
                anotar(ruta, ruta + "[]", v, n == 0)

    for msg in mensajes:
        recorrer(msg, "")
    siempre, a_veces = {}, {}
    for ruta in sorted(vistas):
        padre, n, tipos = vistas[ruta]
        (siempre if n == contenedores[padre] else a_veces)[ruta] = "|".join(sorted(tipos))
    return siempre, a_veces


def _nombrados(esquema: dict, palabra: str) -> list[str]:
    return sorted(c for c, p in esquema.get("properties", {}).items() if palabra in p)


def formas(flujos: dict[str, list[dict]], esquemas: dict | None = None) -> dict:
    """Por flujo, contrato y tipo de mensaje: quién emite, quién recibe, la ruta de cada clave con su tipo JSON, las
    combinaciones de claves de primer nivel que no van siempre (una por forma de mensaje vista) y los valores vistos en los
    campos para los que el Anexo B nombra valores (lista cerrada, `enum`; lista abierta, `examples`). Además, qué contratos se
    han visto en algún flujo y cuáles no."""
    esquemas = esquemas or {}
    salida: dict = {}
    for nombre in sorted(flujos):
        grupos: dict[str, list[dict]] = {}
        for msg in flujos[nombre]:
            grupos.setdefault(f"{msg['contrato']}.{msg['tipo_mensaje']}", []).append(msg)
        tipos = {}
        for clave in sorted(grupos):
            mensajes = grupos[clave]
            siempre, a_veces = rutas(mensajes)
            opcionales = {_clave(c) for m in mensajes for c in m} - set(siempre)
            tipos[clave] = {"emisores": sorted({m["emisor"] for m in mensajes}), "receptores": sorted({m["receptor"] for m in mensajes}),
                            "rutas_siempre": siempre, "rutas_a_veces": a_veces,
                            "combinaciones_de_claves_a_veces": sorted({" ".join(sorted(opcionales & {_clave(c) for c in m})) for m in mensajes})}
            for titulo, palabra in (("valores_de_listas_cerradas", "enum"), ("valores_de_listas_abiertas", "examples")):
                campos = _nombrados(esquemas.get(clave, {}), palabra)
                if campos:
                    tipos[clave][titulo] = {c: sorted({str(m[c]) for m in mensajes if c in m}) for c in campos}
        guardados = FLUJOS.get(nombre, TODOS)
        salida[nombre] = {"contratos_que_se_guardan": guardados if guardados == TODOS else list(guardados), "mensajes": tipos}
    vistos = {msg["contrato"] for msg in todos_los_mensajes(flujos)}
    return {"flujos": salida, "contratos_vistos_en_algun_flujo": sorted(vistos),
            "contratos_que_ningun_flujo_emite": sorted(set(contratos.CANALES) - vistos)}


def _errores(esquema: dict, instancia: dict) -> list[str]:
    validador = jsonschema.Draft202012Validator(esquema)
    return sorted({f"{'/'.join(str(p) for p in e.absolute_path) or '(raíz)'}: {e.validator} {e.validator_value!r}"
                   if e.validator != "required" else f"{'/'.join(str(p) for p in e.absolute_path) or '(raíz)'}: {e.message}"
                   for e in validador.iter_errors(instancia)})


def _en_otro_campo(esquema: dict, msg: dict) -> set[tuple[str, str, str]]:
    """(campo del Anexo B, campo del ejecutor, valor) cuando un valor que el Anexo B nombra para un campo viaja en otro."""
    hallados = set()
    for campo, prop in esquema.get("properties", {}).items():
        valores = {v for v in [*prop.get("enum", []), *prop.get("examples", [])] if isinstance(v, str)}
        hallados |= {(campo, otro, v) for otro, v in msg.items() if otro != campo and isinstance(v, str) and v in valores}
    return hallados


def divergencias(esquemas: dict, ejemplos: dict, capturados: list[dict], carpeta_tmp: Path, fecha: str) -> dict:
    """Dónde difieren el Anexo B (esquemas derivados) y el ejecutor, medido con el propio ejecutor. Se congela: una
    diferencia nueva hace fallar la suite.

    - `el_ejecutor_rechaza_el_ejemplo_del_anexo_b`: el ejemplo cumple el esquema derivado y `Mensajeria.crear` no lo admite;
    - `el_ejecutor_admite_que_falte`: campos obligatorios en el Anexo B sin los cuales `Mensajeria.crear` admite el mensaje;
    - `el_ejecutor_exige_y_el_anexo_b_no_nombra`: campos mínimos del ejecutor que el Anexo B no nombra;
    - los mensajes de los flujos simulados que no cumplen el esquema derivado, con el motivo;
    - los valores que el Anexo B nombra para un campo y el ejecutor emite en otro (por ejemplo, `tipo` de CT-22)."""
    mensajeria = _mensajeria(Path(carpeta_tmp) / "estado_divergencias", fecha)
    campos: dict[str, dict] = {}
    for clave in sorted(esquemas):
        ct, sentido = clave.split(".")
        tabla = contratos.CAMPOS_MINIMOS if sentido == "ENCARGO" else contratos.CAMPOS_RETORNO
        d: dict = {}
        sobra = sorted(set(tabla.get(ct, [])) - set(esquemas[clave].get("properties", {})) - SOBRE)
        if sobra:
            d["el_ejecutor_exige_y_el_anexo_b_no_nombra"] = sobra
        entero = _crear(mensajeria, clave, ejemplos[clave])
        if "rechazo" in entero:
            d["el_ejecutor_rechaza_el_ejemplo_del_anexo_b"] = entero["rechazo"]
        else:
            falta = [c for c in sorted(set(esquemas[clave].get("required", [])) - SOBRE)
                     if "mensaje" in _crear(mensajeria, clave, {k: v for k, v in ejemplos[clave].items() if k != c})]
            if falta:
                d["el_ejecutor_admite_que_falte"] = falta
        if d:
            campos[clave] = d
    no_cumplen: dict[str, set[str]] = {}
    otro_campo: dict[str, set[tuple[str, str, str]]] = {}
    for msg in capturados:
        clave = f"{msg['contrato']}.{msg['tipo_mensaje']}"
        if clave in esquemas:
            no_cumplen.setdefault(clave, set()).update(_errores(esquemas[clave], msg))
            otro_campo.setdefault(clave, set()).update(_en_otro_campo(esquemas[clave], msg))
    return {"por_contrato": campos,
            "mensajes_de_los_flujos_simulados_que_no_cumplen_el_anexo_b": {k: sorted(v) for k, v in sorted(no_cumplen.items()) if v},
            "valores_que_el_anexo_b_nombra_en_un_campo_y_el_ejecutor_emite_en_otro": {
                k: [{"campo_del_anexo_b": a, "campo_del_ejecutor": b, "valor": v} for a, b, v in sorted(hallados)]
                for k, hallados in sorted(otro_campo.items()) if hallados},
            "contratos_sin_campos_en_el_anexo_b": sin_campos_en_anexo_b(esquemas)}


def parrafos_anexo_b() -> dict[str, str]:
    """El texto del Anexo B que habla de cada contrato: el párrafo (y su bloque JSON) que empieza por «**CT-NN». Un párrafo
    de varios contratos («CT-07 / CT-08», «CT-16 a CT-22») vale para todos ellos."""
    doc0 = next((BLOQUE / "01_Gobernanza").glob("Documento 0*.md")).read_text(encoding="utf-8")
    anexo = doc0[doc0.index("## ANEXO B."):doc0.index("## ANEXO C.")]
    salida: dict[str, str] = {}
    for trozo in re.split(r"(?m)^(?=\*\*)", anexo):
        cabecera = re.match(r"\*\*(CT-[0-9]{2})(?: (a|/) (CT-[0-9]{2}))?", trozo)
        if not cabecera:
            continue
        primero, union, ultimo = cabecera.groups()
        numeros = range(int(primero[3:]), int(ultimo[3:]) + 1) if union == "a" else [int(x[3:]) for x in (primero, ultimo) if x]
        for n in numeros:
            salida[f"CT-{n:02d}"] = salida.get(f"CT-{n:02d}", "") + trozo
    return salida


def campos_fuera_de_su_parrafo(esquemas: dict, parrafos: dict[str, str]) -> list[tuple[str, str]]:
    """(esquema, campo) de cada campo de un esquema derivado, anidados incluidos, que el párrafo de su contrato no nombra."""
    def nombres(esquema: dict):
        for campo, prop in esquema.get("properties", {}).items():
            yield campo
            yield from nombres(prop)
            yield from nombres(prop.get("items", {}))

    return [(clave, campo) for clave in sorted(esquemas) for campo in sorted(set(nombres(esquemas[clave])))
            if f"`{campo}`" not in parrafos.get(clave.split(".")[0], "") and f'"{campo}"' not in parrafos.get(clave.split(".")[0], "")]


def _sha(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def huellas(carpeta: Path = CARPETA) -> dict:
    """Huellas de lo que no se genera: el Documento 0, los esquemas publicados y los tres ficheros escritos a mano."""
    doc0 = sorted((BLOQUE / "01_Gobernanza").glob("Documento 0*.md"))
    publicados = sorted((BLOQUE / "06_Plantillas_entregables").glob("Esquema JSON*.json"))
    salida = {f"{r.parent.name}/{r.name}": _sha(r) for r in doc0 + publicados}
    salida.update({f"goldens/{n}": _sha(carpeta / n) for n in A_MANO})
    return salida


def generar(carpeta: Path = CARPETA, fecha: str | None = None, flujos: dict[str, list[dict]] | None = None) -> dict[str, str]:
    """Nombre de cada golden generado → su texto. No escribe nada en `carpeta`. Si se pasan `flujos` (los mensajes ya
    capturados con `capturar_flujos`), no se vuelven a ejecutar."""
    if fecha is None:
        import conftest
        fecha = conftest.AS_OF
    esquemas, ejemplos = leer_a_mano(carpeta)
    bateria = leer_bateria(carpeta)
    with tempfile.TemporaryDirectory() as tmp:
        if flujos is None:
            flujos = capturar_flujos(Path(tmp) / "flujos", fecha)
        mensajes = mensajes_ejemplo(ejemplos, Path(tmp), fecha)
        admitidos = aceptaciones(bateria, ejemplos, Path(tmp), fecha)
        difieren = divergencias(esquemas, ejemplos, todos_los_mensajes(flujos), Path(tmp), fecha)
    return {"tablas_contratos.json": texto(tablas()), "esquemas_respuestas.json": texto(esquemas_respuestas()),
            "mensajes_ejemplo.json": texto(mensajes), "aceptaciones_rechazos.json": texto(admitidos),
            "formas_flujos_mock.json": texto(formas(flujos, esquemas)),
            "divergencias_anexo_b.json": texto(difieren), "huellas.json": texto(huellas(carpeta))}


def comparar(generados: dict[str, str], carpeta: Path = CARPETA) -> list[str]:
    """Diferencias entre lo generado y lo congelado; lista vacía si coincide todo, byte a byte."""
    problemas = []
    for nombre in sorted(generados):
        ruta = carpeta / nombre
        if not ruta.is_file():
            problemas.append(f"{nombre}: falta el golden")
        elif ruta.read_bytes() != generados[nombre].encode("utf-8"):
            problemas.append(f"{nombre}: difiere del golden congelado{_primera_diferencia(ruta, generados[nombre])}")
    esperados = set(generados) | set(A_MANO) | set(DOCUMENTOS)
    presentes = {p.name for p in carpeta.iterdir()} if carpeta.is_dir() else set()
    problemas += [f"{n}: fichero que no es un golden conocido" for n in sorted(presentes - esperados)]
    problemas += [f"{n}: falta" for n in sorted(esperados - presentes - set(generados))]
    return problemas


def _primera_diferencia(ruta: Path, nuevo: str) -> str:
    viejas = ruta.read_text(encoding="utf-8", errors="replace").splitlines()
    nuevas = nuevo.splitlines()
    for n, (a, b) in enumerate(zip(viejas, nuevas), start=1):
        if a != b:
            return f" (línea {n}: congelado «{a.strip()}», generado «{b.strip()}»)"
    return f" (congelado {len(viejas)} líneas, generado {len(nuevas)})"


def recongelar(motivo: str, carpeta: Path = CARPETA, generados: dict[str, str] | None = None, hoy: str | None = None) -> list[str]:
    """Re-congelado deliberado: exige motivo, escribe los goldens que cambian y lo anota en REGISTRO.md."""
    if not isinstance(motivo, str) or not motivo.strip():
        raise ValueError("el re-congelado exige un motivo (--motivo)")
    generados = generar(carpeta) if generados is None else generados
    cambiados = [n for n in sorted(generados)
                 if not (carpeta / n).is_file() or (carpeta / n).read_bytes() != generados[n].encode("utf-8")]
    for nombre in cambiados:
        (carpeta / nombre).write_bytes(generados[nombre].encode("utf-8"))
    if cambiados:
        linea = f"- {hoy or dt.date.today().isoformat()} · {', '.join(cambiados)} · {' '.join(motivo.split())}\n"
        with (carpeta / "REGISTRO.md").open("a", encoding="utf-8") as fh:
            fh.write(linea)
    return cambiados


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Goldens de los contratos CT del Bloque A (T-114).")
    ap.add_argument("--update", action="store_true", help="re-congela; exige --motivo")
    ap.add_argument("--motivo", default="", help="por qué cambia el formato (va a REGISTRO.md)")
    args = ap.parse_args(argv)
    if args.update:
        if not args.motivo.strip():
            print("ERROR: el re-congelado exige un motivo: --update --motivo \"…\"", file=sys.stderr)
            return 2
        cambiados = recongelar(args.motivo)
        print("re-congelados: " + (", ".join(cambiados) if cambiados else "ninguno (ya coincidían)"))
        return 0
    try:
        generados = generar()
    except (ValueError, KeyError, TypeError, jsonschema.exceptions.SchemaError, jsonschema.exceptions.UnknownType) as e:   # un fichero escrito a mano roto (esquema, ejemplo o caso de la batería): se dice y se falla
        print(f"ERROR · no se pueden generar los goldens: {type(e).__name__}: {str(e).splitlines()[0]}", file=sys.stderr)
        print("goldens de contratos: no se pueden generar")
        return 1
    problemas = comparar(generados)
    for p in problemas:
        print("DIFERENCIA · " + p, file=sys.stderr)
    print("goldens de contratos: " + ("coinciden" if not problemas else f"{len(problemas)} diferencias"))
    return 1 if problemas else 0


if __name__ == "__main__":
    raise SystemExit(main())
