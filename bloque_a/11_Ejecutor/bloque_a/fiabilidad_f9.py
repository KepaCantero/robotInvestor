"""T-198 (PB-46): el Buscador de Fuentes Avanzadas (AG-16) atiende el CT-19 FIABILIDAD_FUENTES del Evaluador.

Documento 0 V5.3, 12.5: el Evaluador mide la fiabilidad de las fuentes de opinión «y la comunica al Buscador, que la incorpora
a su calidad en F9». Hasta T-198 el CT-19 se creaba COMPLETO y nadie lo atendía (QA r01 de T-159, H-02; INC-T159-01): F9 es un
archivo del corpus congelado y el ejecutor no tenía dónde escribir lo que el Buscador recibe.

Lo que hace el ejecutor (determinista, con el cliente simulado o con el real):

- **F9 de la instancia.** El almacén tiene un archivo F9 propio (propietario AG-16, R6), append-only y encadenado como los
  demás, que va encima de las fichas del corpus sin cambiarlas. Cada fuente del CT-19 deja en él una entrada
  `FIABILIDAD_MEDIDA` con el bloque «Fiabilidad medida» de la ficha de fuente (prompt del Buscador V5.0, 4.4):
  pronósticos registrados, resueltos, la métrica del Evaluador (BSS, BSS contraído y puntos del criterio 2, con su `calc_id`),
  la ventana, la fecha del CT-19 y el mensaje que la trajo.
- **Atención comprobada.** Antes de escribir nada se comprueba el mensaje entero: CT-19 de AG-20 a AG-16, `tipo`
  FIABILIDAD_FUENTES, `timestamp` ISO no posterior a `as_of`, y cada fuente igual a su FUE- de F6 (conocible en `as_of`), con
  el `comunicado_ct19` de ese mensaje y un `ref_id` que es una fuente de F9. Si algo no cuadra, no se escribe ninguna
  (`FiabilidadNoAtendible`). La comprobación y las escrituras van bajo el cerrojo del almacén (no hay vuelta atrás: si el
  almacén falla a mitad, lo ya escrito queda y el ciclo siguiente completa el resto sin duplicar).
- **Sin duplicados y con reintento.** Una FUE- ya atendida no se vuelve a escribir; una que quedó sin atender (el ciclo cayó o
  el mensaje no cuadró) sale de nuevo en el CT-19 del ciclo siguiente.
- **FUE- que ya no se puede atender** (r02, H-01). Si la fuente de una FUE- ya no es de F9 (baja R19, borrado de HT-02, versión
  nueva de F9), el ciclo no la mete en el CT-19: deja una sola incidencia de datos en HA con la marca `fue_no_atendible` y no
  vuelve a salir; las demás FUE- se atienden.
- **F9 ilegible** (cierre de la r02, H-08). Si F9 no tiene ninguna ficha cargada, no se marca nada: una incidencia sin marca y
  el reintento en el ciclo siguiente.
- **Identificador.** Cada entrada lleva `id` `FMD-AAAA-nnnn` (fiabilidad medida), del contador del almacén.
- **Al Buscador.** Cuando el Buscador recibe una búsqueda (CT-07), las fuentes de F9 que le ofrece el ejecutor llevan su
  `fiabilidad_medida` si la tienen (prompt, sección 3: «Q, nivel y fiabilidad_medida (si existe)»).

Lo que queda para el modelo real (INC-T198-01): recalcular la Q de la ficha con el criterio 2 (el prompt, 6.3, da su propia
contracción, n / (n + 30) sobre una puntuación por bandas, distinta de la del esquema de F6, k = 20), el nivel, el orden dentro
de la temática y la línea RECALIFICACION de «Novedades». Por eso cada entrada dice `recalificacion_q: PENDIENTE` y la Q del
corpus no cambia.
"""
from __future__ import annotations

import copy
import datetime as dt

from .configuracion import parametro
from .evaluador import RE_FECHA_ISO, fuente_de_opinion_registrada

# Campos de cada fuente del CT-19 al Buscador (los de la FUE- del esquema de F6, 4.5, salvo `calc_id` y `comunicado_ct19`)
CAMPOS_CT19 = ("fue_id", "ref_id", "periodo", "n", "aciertos", "bss", "bss_contraido", "puntos_historial")
# Lo que el Buscador ve de una fuente en su búsqueda (bloque «Fiabilidad medida» de la ficha, prompt 4.4)
CAMPOS_CONTEXTO = ("pronosticos_registrados", "resueltos", "aciertos", "bss", "bss_contraido", "puntos_historial",
                   "ventana_meses", "fecha_ct19")


class FiabilidadNoAtendible(Exception):
    """El CT-19 de fiabilidad no se puede atender: no se escribe nada en F9."""


def _fue_de_f6(almacen, as_of) -> dict[str, dict]:
    return {k: v for k, v in almacen.estado("F6", as_of, clave="id").items() if v.get("tipo_entrada") == "FUE"}


def atendidas(almacen, as_of=None) -> set[str]:
    """`fue_id` de las FUE- que el Buscador ya incorporó a F9."""
    return {e["fue_id"] for e in almacen.leer("F9", as_of)
            if e.get("tipo_entrada") == "FIABILIDAD_MEDIDA" and isinstance(e.get("fue_id"), str)}


def no_atendibles(almacen, as_of=None) -> set[str]:
    """`fue_id` de las FUE- declaradas en HA como no atendibles (su fuente ya no es de F9; r02, H-01)."""
    return {e["fue_no_atendible"] for e in almacen.leer("HA", as_of) if isinstance(e.get("fue_no_atendible"), str)}


def por_comunicar(almacen, as_of) -> list[dict]:
    """FUE- de F6 que el Buscador no ha incorporado todavía a F9: las nuevas del ciclo y las que quedaron sin atender, salvo las
    declaradas no atendibles. En orden de periodo y de identificador, para que en F9 la última de una fuente sea la más
    reciente."""
    hechas = atendidas(almacen, as_of) | no_atendibles(almacen, as_of)
    return sorted((f for f in _fue_de_f6(almacen, as_of).values() if f.get("fue_id") not in hechas),
                  key=lambda f: (str(f.get("periodo")), str(f.get("fue_id"))))


def apartar_no_atendibles(almacen, fues: list[dict], referencias, run_id: str) -> list[dict]:
    """r02 (H-01): separa las FUE- cuya fuente ya no es de F9. Cada una deja UNA incidencia de datos en HA con la marca
    `fue_no_atendible` (que `por_comunicar` excluye después) y no va en el CT-19; devuelve las demás. Se llama bajo el cerrojo
    del almacén, con la lista que acaba de dar `por_comunicar`.
    Cierre de la QA r02 (H-08): si F9 no tiene ninguna ficha cargada (archivo ausente o ruta mal puesta), no se sabe qué fuente
    salió de F9: no se marca ninguna, queda una incidencia de datos sin marca y no hay CT-19 este ciclo (se reintenta en el
    siguiente)."""
    if fues and not (getattr(referencias, "fichas", None) or {}).get("F9"):
        almacen.incidencia_de_datos(f"F9 no se pudo leer (ninguna ficha cargada): {len(fues)} FUE- sin enviar al Buscador; se "
                           "reintentan en el ciclo siguiente", "AG-16", severidad="Operativa", run_id=run_id,
                           tratamiento="sin marca; reintento en el ciclo siguiente")
        return []
    quedan = []
    for f in fues:
        if fuente_de_opinion_registrada(f.get("ref_id"), referencias):
            quedan.append(f)
            continue
        almacen.incidencia_de_datos(f"{f.get('fue_id')}: la fuente {f.get('ref_id')!r} ya no es de F9; su fiabilidad no se puede "
                           "incorporar y no se vuelve a enviar al Buscador", "AG-16", severidad="Operativa", run_id=run_id,
                           fue_no_atendible=f.get("fue_id"), tratamiento="declarada una vez; excluida de los CT-19 siguientes")
    return quedan


def cuerpo_ct19(fues: list[dict]) -> dict:
    return {"tipo": "FIABILIDAD_FUENTES", "fuentes": [{k: f.get(k) for k in CAMPOS_CT19} for f in fues]}


def _fecha_del_mensaje(msg: dict, as_of) -> str:
    """r02 (H-03): la fecha del `timestamp` del mensaje, que tiene que ser ISO 8601 y no posterior a `as_of`."""
    ts = msg.get("timestamp")
    if not isinstance(ts, str) or not RE_FECHA_ISO.fullmatch(ts.strip()):
        raise FiabilidadNoAtendible(f"timestamp del CT-19 que no es una fecha ISO: {ts!r}")
    try:
        fecha = dt.date.fromisoformat(ts.strip()[:10])
    except ValueError as e:   # solo la de fromisoformat: «2026-02-30» cumple el patrón y no es una fecha
        raise FiabilidadNoAtendible(f"timestamp del CT-19 fuera del calendario: {ts!r}") from e
    if as_of is not None and fecha.isoformat() > str(as_of)[:10]:
        raise FiabilidadNoAtendible(f"timestamp del CT-19 posterior a as_of: {ts!r}")
    return fecha.isoformat()


def comprobar_ct19(msg: dict, f6: dict[str, dict], referencias, as_of=None) -> list[dict]:
    """Comprueba el CT-19 entero frente a F6 y F9 y devuelve sus fuentes; `FiabilidadNoAtendible` al primer fallo."""
    if not isinstance(msg, dict):
        raise FiabilidadNoAtendible("el mensaje no es un objeto")
    if (msg.get("contrato"), msg.get("emisor"), msg.get("receptor")) != ("CT-19", "AG-20", "AG-16"):
        raise FiabilidadNoAtendible("no es un CT-19 del Evaluador al Buscador")
    if msg.get("tipo") != "FIABILIDAD_FUENTES":
        raise FiabilidadNoAtendible(f"CT-19 de tipo {msg.get('tipo')!r}, no FIABILIDAD_FUENTES")
    msg_id, fuentes = msg.get("msg_id"), msg.get("fuentes")
    if not isinstance(msg_id, str) or not msg_id:
        raise FiabilidadNoAtendible("CT-19 sin msg_id")
    if not isinstance(fuentes, list) or not fuentes:
        raise FiabilidadNoAtendible("CT-19 sin fuentes")
    _fecha_del_mensaje(msg, as_of)
    vistos: set[str] = set()
    for f in fuentes:
        if not isinstance(f, dict) or set(f) != set(CAMPOS_CT19):
            raise FiabilidadNoAtendible("una fuente del CT-19 no trae exactamente los campos de la FUE-")
        fue_id = f["fue_id"]
        if not isinstance(fue_id, str) or fue_id in vistos:
            raise FiabilidadNoAtendible(f"fue_id ausente o repetido en el CT-19: {fue_id!r}")
        vistos.add(fue_id)
        fue = f6.get(fue_id)
        if fue is None:
            raise FiabilidadNoAtendible(f"{fue_id} no está en F6")
        distintos = [k for k in CAMPOS_CT19 if fue.get(k) != f[k]]
        if distintos:
            raise FiabilidadNoAtendible(f"{fue_id}: el CT-19 no coincide con F6 en {distintos}")
        if fue.get("comunicado_ct19") != msg_id:
            raise FiabilidadNoAtendible(f"{fue_id}: F6 no anota este CT-19 ({msg_id})")
        if not fuente_de_opinion_registrada(f["ref_id"], referencias):
            raise FiabilidadNoAtendible(f"{fue_id}: {f['ref_id']!r} no es una fuente de F9")
    return fuentes


def _registrados(almacen, as_of) -> dict[str, int]:
    """Pronósticos registrados en F2 por fuente (afirmaciones PRONOSTICO_FUENTE con su bloque), resueltos o no."""
    cuenta: dict[str, int] = {}
    for clm in almacen.estado("F2", as_of, clave="clm_id").values():
        pf = clm.get("pronostico_fuente")
        if clm.get("tipo_afirmacion") == "PRONOSTICO_FUENTE" and isinstance(pf, dict) and isinstance(pf.get("ref_id"), str):
            cuenta[pf["ref_id"]] = cuenta.get(pf["ref_id"], 0) + 1
    return cuenta


def atender_ct19(bloque, msg: dict, as_of, run_id: str) -> list[str]:
    """El Buscador incorpora a F9 la fiabilidad que trae el CT-19. Devuelve los `fue_id` escritos (los ya atendidos se
    saltan). Comprueba todo antes de escribir, y comprueba y escribe bajo el cerrojo del almacén: si el almacén falla a mitad,
    lo ya escrito queda y el ciclo siguiente completa el resto sin duplicar."""
    almacen = bloque.almacen
    ventana = int(parametro(bloque.cfg, "fiabilidad_fuentes.ventana_meses"))
    with almacen._transaccion():
        f6 = _fue_de_f6(almacen, as_of)
        fuentes = comprobar_ct19(msg, f6, bloque.referencias, as_of)
        hechas = atendidas(almacen, as_of)
        nuevas = [f for f in fuentes if f["fue_id"] not in hechas]
        if not nuevas:
            return []
        registrados = _registrados(almacen, as_of)
        fecha = str(msg.get("timestamp") or "")[:10] or str(as_of)[:10]
        escritas = []
        for f in nuevas:
            fue = f6[f["fue_id"]]
            almacen.escribir("F9", "AG-16", {
                "tipo_entrada": "FIABILIDAD_MEDIDA", "id": almacen.nuevo_id("FMD"), "ref_id": f["ref_id"], "fue_id": f["fue_id"],
                "periodo": f["periodo"], "pronosticos_registrados": registrados.get(f["ref_id"], 0), "resueltos": f["n"],
                "aciertos": f["aciertos"], "bss": f["bss"], "bss_contraido": f["bss_contraido"],
                "puntos_historial": f["puntos_historial"], "calc_id": fue.get("calc_id"), "metrica": fue.get("metodo"),
                "ventana_meses": ventana, "fecha_ct19": fecha, "recibido_via": msg["msg_id"], "run_id": run_id,
                "recalificacion_q": "PENDIENTE"})
            escritas.append(f["fue_id"])
        return escritas


def fiabilidad_medida(almacen, as_of) -> dict[str, dict]:
    """La última fiabilidad medida de cada fuente en F9 de la instancia, conocible en `as_of`."""
    return {ref: {k: e.get(k) for k in CAMPOS_CONTEXTO}
            for ref, e in almacen.estado("F9", as_of, clave="ref_id").items() if e.get("tipo_entrada") == "FIABILIDAD_MEDIDA"}


def anotar_candidatas(almacen, as_of, referencias: list[dict]) -> None:
    """Añade `fiabilidad_medida` a las fuentes de F9 ofrecidas al Buscador que la tienen; a las demás no les añade nada."""
    medida = fiabilidad_medida(almacen, as_of)
    if not medida:
        return
    for r in referencias:
        if r.get("archivo") == "F9" and r.get("ref_id") in medida:
            r["fiabilidad_medida"] = copy.deepcopy(medida[r["ref_id"]])
