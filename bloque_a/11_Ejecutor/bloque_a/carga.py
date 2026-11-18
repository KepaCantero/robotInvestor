"""Orquestador técnico, modo CARGA (T-178): registro en HA de lo que mide HT-08 y propuesta de tipo 3 por saturación repetida.

Prompt del Orquestador V5.0, 5.3 punto 5: si el cuello de botella está en un agente de instancia única (AG-01, AG-02, AG-18,
AG-19, AG-20), no se abren instancias; se reordena su cola por prioridad, se informa al Coordinador si afecta a plazos de
entrega (vía la entrada de HA, que el Coordinador lee) y se eleva al operador una propuesta de tipo 3 si se repite.
Esquema de HA V2.0: 4.5 (ORD-, CAR-) y 4.8 (P3-). Plan de pruebas V3.0: PB-19.

- La reordenación y el aviso los pone HT-08 en el CAR- (`ht08_monitor.Monitor._saturacion`).
- «Si se repite» (el Anexo A no le da número; [PROPUESTO], INC-T178-01): vuelve a ocurrir, es decir, hay en HA otro CAR- de
  saturación del mismo agente de otro run, posterior a la última entrada de su última propuesta. Una propuesta que no
  está cerrada no se duplica: el CAR- la cita. Solo RECHAZADA o APLICADA la cierran (r02, QA r01 H-02: un estado fuera del
  enum del esquema, o ninguno, la deja abierta: falla cerrado, sin duplicar la cola de tipo 3); después, hace falta
  volver a repetirse.
- r02 (QA r01, H-01): la lectura de HA, la decisión, la P3- y el CAR- van en una sola transacción del almacén (exclusión
  también entre procesos), de modo que dos runs concurrentes no crean dos propuestas.
- r02 (QA r01, H-05): la evidencia de la P3- cita solo los CAR- que ya están en HA (los de las saturaciones anteriores) y
  las cifras de la actual; el CAR- actual cita la P3- (`p3_id`) y se escribe después. Si ese CAR- falla, la P3- sigue
  siendo coherente (no cita nada inexistente) y queda abierta para el run siguiente; el error se relanza.
"""
from __future__ import annotations

from .guias import BATERIA_REGRESION

CLAVE_P3 = "saturacion_instancia_unica"
CERRADAS = ("RECHAZADA", "APLICADA")


def _es_p3_de(e: dict, agente: str) -> bool:
    return e.get("tipo_entrada") == "P3" and e.get("clave") == CLAVE_P3 and e.get("agente_saturado") == agente


def _es_car_de(e: dict, agente: str) -> bool:
    # Los CAR- anteriores a T-178 no llevan `saturado`: entonces solo se escribían por saturación
    return e.get("tipo_entrada") == "CAR" and e.get("agente") == agente and e.get("saturado", True)


def _propuesta(almacen, car: dict, run_id: str | None) -> str | None:
    """P3- que cita el CAR- (la abierta, o una nueva si la saturación se repite), o None si es la primera vez."""
    ag = car["agente"]
    ha = almacen.leer("HA")
    estados = almacen.estado("HA")
    # Las decisiones del operador son entradas nuevas con el mismo id (append-only) que no repiten la clave: se reconocen
    # por el id de la propuesta, que lleva la clave en su vista consolidada
    ids = {pid for pid, v in estados.items() if _es_p3_de(v, ag)}
    propias = [i for i, e in enumerate(ha) if e.get("tipo_entrada") == "P3" and e.get("id") in ids]
    for i in reversed(propias):
        pid = ha[i]["id"]
        if estados.get(pid, {}).get("estado") not in CERRADAS:
            return pid
    corte = propias[-1] + 1 if propias else 0
    previos = [e for e in ha[corte:] if _es_car_de(e, ag) and e.get("run_id") != run_id]
    if not previos:
        return None
    p3_id = almacen.nuevo_id("P3-ORQ")
    evidencia = {"car": [e["id"] for e in previos], "runs": sorted({str(e.get("run_id")) for e in previos}),
                 "run_actual": run_id, "cola": car["cola"], "umbral_cola": car["umbral_cola"],
                 "afecta_plazos": car["afecta_plazos"]}
    almacen.escribir("HA", "AG-18", {
        "tipo_entrada": "P3", "id": p3_id, "origen": "ORQ", "clave": CLAVE_P3, "agente_saturado": ag,
        "objeto": f"Capacidad de {ag}, instancia única con cola (4.5 del Documento 0): saturación repetida",
        "evidencia": evidencia,
        "impacto": (f"{ag} no admite instancias paralelas: con la cola por encima del umbral las órdenes esperan en serie"
                    + (" y pueden retrasar entregas" if car["afecta_plazos"] else "; no está en el camino de la entrega")),
        "pruebas_regresion": list(BATERIA_REGRESION) + ["PB-19"],
        "plan_reversion": "Si el operador la rechaza, todo sigue igual (instancia única con reordenación y aviso); si la aprueba, "
                          "el cambio se hace como tipo 3 (18.1), con sus pruebas de regresión",
        "npr": None, "estado": "PENDING_OPERATOR", "decision_operador": None, "run_id": run_id})
    return p3_id


def registrar_carga(almacen, entradas: list[dict], run_id: str | None) -> list[dict]:
    """Escribe en HA, bajo AG-18, las ORD- y CAR- de `Monitor.evaluar_instancias`. Un CAR- de saturación lleva `p3_id`
    cuando hay propuesta de tipo 3; la P3- se escribe antes que el CAR-, que así nunca cita una propuesta que no existe, y
    la P3- solo cita CAR- ya escritos (H-05)."""
    escritas = []
    for orden in entradas:
        with almacen._transaccion():   # r02 (H-01): leer HA, decidir y escribir, sin otro run en medio
            e = dict(orden)
            e["id"] = almacen.nuevo_id(e["tipo_entrada"])
            if e["tipo_entrada"] == "CAR" and e.get("saturado"):
                p3_id = _propuesta(almacen, e, run_id)
                if p3_id:
                    e["p3_id"] = p3_id
            escritas.append(almacen.escribir("HA", "AG-18", {**e, "run_id": run_id}))
    return escritas


def avisos_plazos(almacen, run_id: str | None = None) -> list[dict]:
    """Lectura del Coordinador (AG-01): los CAR- de HA con aviso de plazos dirigido a él (de un run, o todos)."""
    return [e for e in almacen.leer("HA")
            if e.get("tipo_entrada") == "CAR" and (e.get("aviso_coordinador") or {}).get("destinatario") == "AG-01"
            and (run_id is None or e.get("run_id") == run_id)]
