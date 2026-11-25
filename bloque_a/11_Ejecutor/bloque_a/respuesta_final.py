"""T-162 · C3: respuesta final por CT-03 cuando termina el análisis escalado de una consulta del Broker (§7.6.3 del Documento 0
óptima V5.1, PB-07 del Plan de pruebas V3.0).

`Bloque.consulta` envía primero la respuesta provisional (CT-03 con el `escalado`: nivel, plazo y RUN-). Al acabar el RUN- ad hoc,
este módulo envía la final: otro CT-03 RETORNO de AG-01 al Broker, con el `query_id` de la consulta y el `run_id` del RUN-, y
las referencias de lo que el RUN- entregó. Reglas:

- Determinista: el texto y las referencias los escribe el código con lo que hay en F1–F5 (sin llamar al modelo).
- Falla cerrado: solo cita identificadores que son la clave de una entrada de F1–F5 a la fecha de la consulta; si el RUN- falló,
  no entregó o no se lanzó, la final lo dice (`estado` SIN_RESULTADO) y no cita ninguna opción.
- Se valida contra `ESQUEMA` y después por la mensajería (canal, R8 y campos mínimos de CT-03) antes de escribir nada.
- Idempotente: la final queda en F5 como una entrada más de su QRY-; si ya está, se devuelve la guardada y no sale otra.
- T-169 (QA r01 de T-162): un fallo de integridad o de control del almacén durante el RUN- para la consulta como antes
  (`para_la_consulta`, H-01); el `msg_id` de la provisional queda en F5 y `enviar` lo exige, y una final que no salió la envían
  la consulta o el ciclo siguientes (`enviar_pendientes`, H-02); cada referencia se filtra por su tipo y el RUN- tiene que ser
  el que lanzó la consulta (H-03).

Lo que el diseño no decía (el campo `respuesta_final`, los resultados, las referencias y la confianza) está en INC-T162-01,
`[PROPUESTO]`; lo de T-169, en INC-T169-01. Desde T-166, el Anexo B del Documento 0 V5.3 (CT-03) describe esta final.
"""
from __future__ import annotations

import copy
from typing import Any

import jsonschema

from .configuracion import NOMBRE_CLASE
from .contratos import ESQUEMAS, DatosSensibles, MensajeInvalido
from .herramientas.ht01_datos import FugaDeInformacion
from .llm import ReplayFaltante

# Vocabulario de confianza del Documento 0 (glosario), de menos a más
CONFIANZAS = ("en disputa", "especulativo", "probable", "establecido")
# Resultado del análisis escalado → estado común del sobre (§6.2.6)
RESULTADOS = {"ENTREGADO": "COMPLETO", "ENTREGADO_PARCIAL": "PARCIAL", "SIN_ENTREGA": "SIN_RESULTADO",
              "FALLIDO": "SIN_RESULTADO", "NO_EJECUTADO": "SIN_RESULTADO"}
ESTADO_F5 = {"COMPLETO": "RESPONDIDA_FINAL", "PARCIAL": "RESPONDIDA_FINAL", "SIN_RESULTADO": "FINAL_SIN_RESULTADO"}
# T-169 (H-01): errores del RUN- escalado que no se absorben en una final FALLIDO, sino que paran la consulta como antes: los
# controles del almacén y de la mensajería (`PermissionError`: EscrituraFueraDeReserva, PronosticoCongelado, CanalNoPrevisto,
# DatosSensibles), un mensaje que no cumple su contrato, una fuga de información (look-ahead) y, r02 (H-02), una respuesta que
# no está grabada en el modo «reproducir» del cliente replay (falla la reproducción, no el análisis)
ERRORES_DE_CONTROL = (PermissionError, MensajeInvalido, FugaDeInformacion, ReplayFaltante)
# T-169 (H-02): rechazos de una final pendiente que no escriben nada (esquema, R8 o campos de la mensajería): se aparta
RECHAZOS_SIN_EFECTO = (DatosSensibles, MensajeInvalido)
PATRON_REF = r"^(?:RUN|OPP|TND|CLM|PRG)-[0-9]{4}-[0-9]{4,}$"
_TXT = {"type": "string", "minLength": 1}
_CONSULTA = ESQUEMAS["CONSULTA"]["properties"]

ESQUEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "CT-03 · respuesta final de una consulta escalada (cuerpo, sin el sobre común)",
    "type": "object", "additionalProperties": False,
    "required": ["clase_consulta", "ruta", "respuesta", "referencias", "confianza", "escalado", "respuesta_final", "limitaciones"],
    "properties": {
        "clase_consulta": _CONSULTA["clase_consulta"],
        "ruta": {"const": "ANALITICA"},
        "respuesta": _TXT,
        "referencias": {"type": "array", "uniqueItems": True, "items": {"type": "string", "pattern": PATRON_REF}},
        "confianza": _CONSULTA["confianza"],
        # El mismo `escalado` que la provisional (Anexo B: `run_id` y `plazo_estimado`)
        "escalado": {"type": "object", "additionalProperties": False, "required": ["nivel", "clases", "plazo_estimado", "run_id"],
                     "properties": {"nivel": {"enum": ["N1", "N2", "N3"]}, "clases": {"type": "array", "items": _TXT},
                                    "plazo_estimado": _TXT, "respuesta_provisional": {"type": "string"},
                                    "run_id": {"type": ["string", "null"]}, "estado_run": _TXT}},
        "respuesta_final": {"type": "object", "additionalProperties": False, "required": ["provisional_msg_id", "resultado_analisis"],
                            "properties": {"provisional_msg_id": {"type": "string", "pattern": "^MSG-"},
                                           "resultado_analisis": {"enum": list(RESULTADOS)}}},
        "limitaciones": {"type": "array", "items": _TXT},
    },
    "allOf": [
        # Sin análisis lanzado no hay nada que citar; fallido o sin entrega, como mucho el RUN-
        {"if": {"properties": {"respuesta_final": {"properties": {"resultado_analisis": {"const": "NO_EJECUTADO"}}}}},
         "then": {"properties": {"referencias": {"maxItems": 0}}}},
        {"if": {"properties": {"respuesta_final": {"properties": {"resultado_analisis": {"enum": ["FALLIDO", "SIN_ENTREGA"]}}}}},
         "then": {"properties": {"referencias": {"maxItems": 1, "items": {"pattern": "^RUN-"}}}}},
    ],
}


class RespuestaFinalInvalida(ValueError):
    pass


def consulta_en_cola(almacen, qry: dict) -> bool:
    """T-196 (PB-08): una consulta escalada cuya petición sigue en la cola del Coordinador (`cola_peticiones`, PET- ENCOLADA
    o EN_CURSO): su análisis aún no ha terminado y la final no puede salir. Si la PET- no llegó a escribirse, no está en cola:
    su análisis no se lanzó, y la final lo dice."""
    pet_id = qry.get("peticion_cola")
    if not pet_id:
        return False
    pet = almacen.estado("F5").get(pet_id) or {}
    return pet.get("tipo_entrada") == "PETICION" and pet.get("estado") in ("ENCOLADA", "EN_CURSO")


def para_la_consulta(almacen, error: BaseException) -> bool:
    """T-169 (H-01): True si el fallo del RUN- escalado tiene que parar la consulta (relanzarse) en vez de dar una final
    FALLIDO: un error de control, o cualquier error con algún fichero del almacén que ya no pasa su comprobación de integridad."""
    return isinstance(error, ERRORES_DE_CONTROL) or not all(almacen.verificar_integridad().values())


def registrar_provisional(almacen, qry_id: str, msg_id: str, fallo: str | None = None) -> None:
    """T-169 (H-02): deja en F5, en la misma QRY-, el `msg_id` de la provisional ya creada y, si el RUN- falló, la clase del
    error: lo que hace falta para enviar la final después, con el mismo enlace y el mismo texto."""
    almacen.escribir("F5", "AG-01", {"tipo_entrada": "QRY", "id": qry_id, "provisional_msg_id": msg_id,
                                     **({"fallo_analisis": fallo} if fallo else {})})


def registrada(almacen, qry_id: str) -> dict | None:
    """La final ya enviada de esa consulta (tal como se guardó en F5), o None."""
    for e in reversed(almacen.leer("F5")):
        if e.get("tipo_entrada") == "QRY" and e.get("id") == qry_id and e.get("respuesta_final"):
            return copy.deepcopy(e["respuesta_final"])
    return None


def validar(cuerpo: dict, estado: str) -> None:
    """El cuerpo cumple `ESQUEMA` y su estado común es el de su resultado."""
    errores = sorted(jsonschema.Draft202012Validator(ESQUEMA).iter_errors(cuerpo), key=lambda e: list(e.absolute_path))
    if errores:
        e = errores[0]
        raise RespuestaFinalInvalida(f"CT-03 final no cumple su esquema en {'/'.join(map(str, e.absolute_path)) or '(raíz)'}: {e.message}")
    if RESULTADOS[cuerpo["respuesta_final"]["resultado_analisis"]] != estado:
        raise RespuestaFinalInvalida(f"CT-03 final: estado {estado} incoherente con {cuerpo['respuesta_final']['resultado_analisis']}")


def _existentes(almacen, as_of) -> set[str]:
    """Identificadores que son la clave de una entrada (no solo una mención): RUN- de F5, TND- de F1, CLM- de F2, OPP- de F3
    y PRG- dados de alta en F4."""
    ids = {e["id"] for e in almacen.leer("F5", as_of) if e.get("tipo_entrada") == "RUN" and e.get("id")}
    ids |= {e["tnd_id"] for e in almacen.leer("F1", as_of) if e.get("tnd_id")}
    ids |= {e["clm_id"] for e in almacen.leer("F2", as_of) if e.get("tipo_entrada") == "CLM" and e.get("clm_id")}
    ids |= {e["opp_id"] for e in almacen.leer("F3", as_of) if e.get("opp_id")}
    ids |= {e["prg_id"] for e in almacen.leer("F4", as_of) if e.get("tipo_entrada") == "ALTA" and e.get("prg_id")}
    return ids


def _por_tipo(valores, prefijo: str) -> tuple[list[str], list[str]]:
    """T-169 (H-03): (los del tipo del campo, los de otro tipo); lo que no es texto no cuenta."""
    textos = [x for x in valores or [] if isinstance(x, str) and x]
    return [x for x in textos if x.startswith(prefijo)], [x for x in textos if not x.startswith(prefijo)]


def _resultado(escalado: dict, run: dict | None) -> str:
    if escalado.get("estado_run") == "FALLIDO":
        return "FALLIDO"
    if not escalado.get("run_id"):
        return "NO_EJECUTADO"
    if run is None or run.get("entrega", "ENTREGADA") != "ENTREGADA":
        return "SIN_ENTREGA"
    return "ENTREGADO" if run.get("estado") == "COMPLETO" else "ENTREGADO_PARCIAL"


def _menos_confiada(valores) -> str:
    return min(valores, key=CONFIANZAS.index)


def construir(almacen, qry: dict, provisional_msg_id: str, as_of, fallo: str | None = None) -> tuple[dict, str | None, str, list[str]]:
    """(cuerpo, run_id, estado común, referencias descartadas) de la final de la consulta `qry` (su entrada consolidada de F5)."""
    esc = copy.deepcopy(qry["escalado"])
    run_id = esc.get("run_id")
    entrada_run = (almacen.estado("F5", as_of).get(run_id) if run_id else None) or {}
    es_run = entrada_run.get("tipo_entrada") == "RUN"
    # T-169 (H-03): solo cuenta el RUN- que lanzó esta consulta (su disparador lleva la QRY-)
    lanzado = es_run and (entrada_run.get("disparador") or {}).get("qry_id") == qry.get("id")
    run = entrada_run if lanzado else None
    ajenas: list[str] = []
    resultado = _resultado(esc, run)
    existentes = _existentes(almacen, as_of)
    nivel_tipos = f"nivel {esc['nivel']}; {', '.join(NOMBRE_CLASE.get(c, c) for c in esc['clases'])}"
    limitaciones = [x for x in (run or {}).get("limitaciones", []) if isinstance(x, str) and x.strip()]
    candidatas: list[str] = [run_id] if run_id and run is not None else []
    if resultado in ("ENTREGADO", "ENTREGADO_PARCIAL"):
        f3 = almacen.estado("F3", as_of)
        f4 = almacen.leer("F4", as_of)
        lineas, confianzas = [], []
        for clase, opps in ((run or {}).get("top3_por_clase") or {}).items():
            de_la_clase = []
            for opp in opps:
                o = f3.get(opp)
                if o is None or opp not in existentes:
                    continue
                tnd, otras_tnd = _por_tipo(o.get("tnd_ids") or [o.get("tnd_id")], "TND-")
                clm, otras_clm = _por_tipo(o.get("evidencias"), "CLM-")
                candidatas += [opp, *tnd, *clm]
                ajenas += [*otras_tnd, *otras_clm]
                candidatas += [x["prg_id"] for x in f4 if x.get("tipo_entrada") == "ALTA" and x.get("run_id") == run_id
                               and x.get("opp_id") == opp and str(x.get("prg_id", "")).startswith("PRG-")]
                conf = o.get("confianza") if o.get("confianza") in CONFIANZAS else "especulativo"
                confianzas.append(conf)
                de_la_clase.append(f"{opp} «{o.get('nombre') or opp}» (confianza {conf})")
            if de_la_clase:
                lineas.append(f"{NOMBRE_CLASE.get(clase, clase)}: {', '.join(de_la_clase)}")
        como = "completo" if resultado == "ENTREGADO" else "con alcance parcial"
        if lineas:
            texto = (f"Análisis {run_id} terminado {como} y entregado ({nivel_tipos}). Opciones del top-3: " + "; ".join(lineas)
                     + ". Cada referencia lleva a la opción, su tendencia, sus evidencias y sus pronósticos congelados.")
        else:
            texto = (f"Análisis {run_id} terminado {como} y entregado ({nivel_tipos}), sin ninguna opción en el top-3: ninguna pasó "
                     "las puertas del análisis.")
        if limitaciones:
            texto += " Lleva limitaciones declaradas (ver «limitaciones»)."
        confianza = _menos_confiada(confianzas) if confianzas else _menos_confiada([qry.get("confianza", "especulativo"), "especulativo"])
    else:
        if resultado == "FALLIDO":
            motivo = f"falló ({fallo})" if fallo else "falló"
            limitaciones.append(f"El análisis escalado {motivo}; queda una incidencia en HA")
            texto = f"El análisis escalado ({nivel_tipos}) no terminó: {motivo}."
        elif resultado == "NO_EJECUTADO":
            limitaciones.append("El análisis escalado no se lanzó (consulta sin escalado)")
            texto = f"El análisis escalado ({nivel_tipos}) no se lanzó."
        else:
            por_que = ("el RUN- no lo lanzó esta consulta" if run is None and es_run
                       else "el RUN- no consta en F5" if run is None else "G3 bloqueó la entrega" if run.get("entrega") == "BLOQUEADA"
                       else "ningún tipo de activo del alcance se pudo analizar" if run.get("entrega") == "SIN_RESULTADO"
                       else f"entrega {run.get('entrega')}")
            limitaciones.append(f"El análisis {run_id} terminó sin entrega: {por_que}")
            texto = f"El análisis {run_id} ({nivel_tipos}) terminó sin entrega: {por_que}."
        texto += " No hay resultado que comunicar: la respuesta provisional no se confirma ni se amplía."
        confianza = _menos_confiada([qry.get("confianza", "especulativo"), "especulativo"])
    vistas: list[str] = []
    for x in candidatas:
        if x and x not in vistas:
            vistas.append(x)
    referencias = [x for x in vistas if x in existentes]
    descartadas = [x for x in vistas if x not in existentes] + [x for x in dict.fromkeys(ajenas) if x not in vistas]
    cuerpo = {"clase_consulta": qry["clase_consulta"], "ruta": "ANALITICA", "respuesta": texto, "referencias": referencias,
              "confianza": confianza, "escalado": esc, "limitaciones": limitaciones,
              "respuesta_final": {"provisional_msg_id": provisional_msg_id, "resultado_analisis": resultado}}
    # El sobre enlaza el RUN- solo si consta en F5; si no, queda en el `escalado`, como en la provisional
    return cuerpo, (run_id if run is not None else None), RESULTADOS[resultado], descartadas


def enviar(bloque, qry_id: str, provisional_msg_id: str | None, as_of, fallo: str | None = None) -> dict:
    """Envía (una sola vez) la final de la consulta `qry_id`. Devuelve el mensaje sin el sobre común, con su `msg_id`, su
    `timestamp`, su `run_id`, su `estado` y `repetido` (True si ya se había enviado: entonces no sale otro).

    T-169 (H-02): la provisional a la que responde es la que F5 tiene registrada para esa QRY- (`registrar_provisional`); sin
    ella no hay final, y un `provisional_msg_id` dado que no es ese se rechaza (None: el de F5). La clase del fallo del RUN-,
    si no se da, también sale de F5."""
    almacen = bloque.almacen
    with almacen._transaccion():   # comprobar y escribir de una vez, también entre procesos
        previa = registrada(almacen, qry_id)
        if previa is not None:
            if provisional_msg_id is not None and previa["respuesta_final"]["provisional_msg_id"] != provisional_msg_id:
                raise RespuestaFinalInvalida(f"{qry_id}: la final ya enviada responde a otra provisional")
            return {**previa, "repetido": True}
        qry = almacen.estado("F5", as_of).get(qry_id)
        if not qry or qry.get("tipo_entrada") != "QRY" or qry.get("ruta") != "ANALITICA" or not isinstance(qry.get("escalado"), dict):
            raise RespuestaFinalInvalida(f"{qry_id} no es una consulta escalada de F5: no lleva respuesta final")
        registrado = qry.get("provisional_msg_id")
        if not isinstance(registrado, str) or not registrado.startswith("MSG-"):
            raise RespuestaFinalInvalida(f"{qry_id}: F5 no tiene registrada la respuesta provisional; no hay final que enlazar")
        if consulta_en_cola(almacen, qry):   # T-196: la final sale al atender su petición, no antes
            raise RespuestaFinalInvalida(f"{qry_id}: su análisis sigue en la cola ({qry['peticion_cola']}); la final sale al atenderlo")
        if provisional_msg_id is not None and provisional_msg_id != registrado:
            raise RespuestaFinalInvalida(f"{qry_id}: {provisional_msg_id} no es la provisional registrada en F5")
        fallo = fallo or qry.get("fallo_analisis")
        cuerpo, run_id, estado, descartadas = construir(almacen, qry, registrado, as_of, fallo)
        validar(cuerpo, estado)
        msg = bloque.mensajeria.crear("CT-03", "AG-01", "BROKER", cuerpo, query_id=qry_id, run_id=run_id,
                                      tipo_mensaje="RETORNO", estado=estado)
        final = {"msg_id": msg["msg_id"], "timestamp": msg["timestamp"], "run_id": run_id, "estado": estado, **cuerpo}
        almacen.escribir("F5", "AG-01", {"tipo_entrada": "QRY", "id": qry_id, "estado": ESTADO_F5[estado], "respuesta_final": final,
                                         "referencias_descartadas_final": descartadas})
    return {**copy.deepcopy(final), "repetido": False}


def pendientes(almacen, as_of=None) -> list[tuple[str, str]]:
    """T-169 (H-02): (QRY-, su fecha) de cada consulta escalada con la provisional registrada en F5 y sin final enviada ni
    apartada, en el orden de F5. T-196: sin las que tienen su análisis en la cola (`consulta_en_cola`)."""
    salida = []
    for qry_id, q in almacen.estado("F5", as_of).items():
        if (q.get("tipo_entrada") == "QRY" and q.get("ruta") == "ANALITICA" and isinstance(q.get("escalado"), dict)
                and q.get("provisional_msg_id") and not q.get("respuesta_final") and not q.get("final_no_enviable")
                and not consulta_en_cola(almacen, q)):
            # T-196: la de una consulta encolada, con la fecha en que se atendió (la de su RUN-), no la de la consulta
            salida.append((qry_id, q["_ultima_fecha"] if q.get("peticion_cola") else q["_historial"][0]["fecha"]))
    return salida


def _apartar(almacen, qry_id: str, error: str) -> None:
    """T-169 (cierre, H-01 de la r02): primero la incidencia y después la marca. Si falla la incidencia, la pendiente sigue y se
    reintenta; si falla la marca, como mucho se repite la incidencia. Nunca queda apartada sin escalar."""
    almacen.incidencia("OTRO", f"La respuesta final pendiente de {qry_id} no se puede enviar ({error}); queda apartada; "
                       "puede haberse creado el mensaje; revisar antes de reenviar",
                       "AG-01", severidad="Operativa", escalado_operador=True,
                       tratamiento="apartada; el operador la reenvía con respuesta_final.enviar tras corregir el estado")
    almacen.escribir("F5", "AG-01", {"tipo_entrada": "QRY", "id": qry_id, "final_no_enviable": {"error": error}})


def enviar_pendientes(bloque, as_of=None) -> list[dict]:
    """T-169 (H-02): envía las finales pendientes (`pendientes`), cada una con la fecha de su consulta: la misma final que
    habría salido entonces. Una que no se puede enviar se aparta una vez (entrada `final_no_enviable` en F5 e incidencia en HA
    con `escalado_operador`) y no para el resto; el operador la reenvía con `enviar` tras corregir el estado.

    T-169 r02: solo para (se propaga) lo que para una consulta (`para_la_consulta`: integridad o control), salvo los rechazos sin
    efecto con el almacén íntegro, que se apartan (H-01); el envío y el apartado van bajo la transacción del almacén y se vuelve a
    mirar dentro si ya tiene final o está apartada, así que se aparta una sola vez aunque la vean varios hilos o procesos (H-03)."""
    almacen = bloque.almacen
    cola = getattr(bloque, "cola", None)
    if cola is not None:   # T-196 r02 (H-03): avisa de las peticiones huérfanas, cuya final no puede salir sola
        cola.huerfanas()
    enviadas = []
    for qry_id, fecha in pendientes(almacen, as_of):
        with almacen._transaccion():
            ahora = almacen.estado("F5").get(qry_id) or {}
            if ahora.get("final_no_enviable"):
                continue
            try:
                enviadas.append(enviar(bloque, qry_id, None, fecha))
            except (RespuestaFinalInvalida, *RECHAZOS_SIN_EFECTO) as e:
                if not all(almacen.verificar_integridad().values()):
                    raise
                _apartar(almacen, qry_id, type(e).__name__)
            except Exception as e:
                if para_la_consulta(almacen, e):
                    raise
                _apartar(almacen, qry_id, type(e).__name__)
    return enviadas
