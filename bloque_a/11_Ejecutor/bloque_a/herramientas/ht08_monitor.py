"""HT-08 · Monitor de colas y consumo: colas por agente, tiempos, consumo frente a presupuesto
y órdenes de apertura de instancias (R25) para los agentes sin estado."""
from __future__ import annotations

import datetime as dt
import math
import re
import threading
import time
from collections import defaultdict

from ..configuracion import parametro
from ..contratos import ANALISTAS

# Documento 0 V5.1, 4.5: sin estado (varias instancias) los Analistas de tipo de activo (AG-03 a AG-09 y AG-21 a
# AG-25, tomados de `contratos.ANALISTAS` para no duplicar la lista), AG-12 a AG-17 y, con altas serializadas,
# AG-10 y AG-11. Con estado (instancia única con cola): AG-01, AG-02, AG-18, AG-19 y AG-20.
OTROS_SIN_ESTADO: frozenset[str] = frozenset({"AG-10", "AG-11", "AG-12", "AG-13", "AG-14", "AG-15", "AG-16", "AG-17"})
SIN_ESTADO: frozenset[str] = frozenset(ANALISTAS) | OTROS_SIN_ESTADO
# T-178 (PB-19): de los agentes de instancia única, los que están en el camino de la entrega (C1–C3): el Coordinador, el
# Analizador y el Orquestador (G3 síncrona, CT-14). El Auditor es asíncrono y nunca bloquea (R17) y el Evaluador trabaja en
# C4 y C5, en segundo plano (6 del Documento 0): su saturación no retrasa una entrega. [PROPUESTO] en INC-T178-01.
CAMINO_ENTREGA: frozenset[str] = frozenset({"AG-01", "AG-02", "AG-18"})
# Prioridad de una orden: la lista cerrada de CT-01 (Documento 0, Anexo B), en ese orden; C6 va por detrás de C1–C3 (R5, 6).
PRIORIDADES: tuple[str, ...] = ("ALTA", "NORMAL", "BAJA")
TIPOS_C6: frozenset[str] = frozenset({"SEGUIMIENTO"})
# T-178 r02 (QA r01, H-04): tipos de orden admitidos, en lista cerrada: los de CT-01 (`contratos.py`) y el CT-05 de C6
# (`seguimiento.py`). Un tipo mal escrito («seguimiento») pasaría por C1–C3: se rechaza.
TIPOS: frozenset[str] = frozenset({"AD_HOC", "PROFUNDIZACION", "PERIODICO"}) | TIPOS_C6
RE_FECHA = re.compile(r"\d{4}-\d{2}-\d{2}")


def _fecha_objetivo(f, ref: str) -> str | None:
    """T-178 r02 (QA r01, H-03): la fecha objetivo entra en la clave de orden, así que se exige AAAA-MM-DD (una fecha real)
    o un `datetime.date`, que se guarda en ISO. Otro formato, otro tipo o NaN se rechazan: compararían mal como texto."""
    if f is None:
        return None
    if isinstance(f, dt.date):
        return (f.date() if isinstance(f, dt.datetime) else f).isoformat()
    if not (isinstance(f, str) and RE_FECHA.fullmatch(f)):
        raise ValueError(f"HT-08: fecha_objetivo {f!r} de {ref} no es AAAA-MM-DD")
    try:
        dt.date.fromisoformat(f)
    except ValueError:
        raise ValueError(f"HT-08: fecha_objetivo {f!r} de {ref} no es una fecha") from None
    return f


def clave_prioridad(orden: dict) -> tuple:
    """Orden de atención de una cola de instancia única (T-178): C1–C3 antes que C6; ALTA, NORMAL, BAJA; la fecha objetivo
    más temprana (sin fecha, al final); y el orden de llegada, que hace el orden estable y total."""
    fecha = orden.get("fecha_objetivo")
    return (orden.get("tipo") in TIPOS_C6, PRIORIDADES.index(orden["prioridad"]), fecha is None, str(fecha or ""),
            orden["llegada"])


def _positivo(nombre, valor):
    if valor is None:
        valor = parametro(None, f"paralelismo.{nombre}")
    if type(valor) not in (int, float) or not math.isfinite(valor) or valor <= 0:
        raise ValueError(f"{nombre} debe ser un número positivo y finito")
    return valor


class Monitor:
    def __init__(self, umbral_cola: int = 3, instancias_max: int = 8, *, objetivo_ingesta_s=None, reloj=None,
                 factor_tiempo=None, rho_objetivo=None, rho_cierre=None, lecturas_cierre=None) -> None:
        self.factor_tiempo = _positivo("factor_tiempo", factor_tiempo)
        self.rho_objetivo = _positivo("rho_objetivo", rho_objetivo)
        self.rho_cierre = _positivo("rho_cierre", rho_cierre)
        self.lecturas_cierre = _positivo("lecturas_cierre", lecturas_cierre)
        if not 0 < self.rho_cierre < self.rho_objetivo <= 1:
            raise ValueError("Se exige 0 < rho_cierre < rho_objetivo <= 1")
        if type(self.lecturas_cierre) is not int:
            raise ValueError("lecturas_cierre debe ser un entero")
        self.umbral_cola = umbral_cola
        self.instancias_max = instancias_max
        self._lock = threading.Lock()
        self.cola: dict[str, int] = defaultdict(int)
        self.completados: dict[str, int] = defaultdict(int)
        self.tiempo_total: dict[str, float] = defaultdict(float)
        self.instancias: dict[str, int] = defaultdict(lambda: 1)
        self.ordenes: list[dict] = []
        self.pendientes: dict[str, list[dict]] = defaultdict(list)   # T-178: órdenes conocidas de cada cola
        if objetivo_ingesta_s is not None and (isinstance(objetivo_ingesta_s, bool) or not isinstance(objetivo_ingesta_s, (int, float))
                                              or not math.isfinite(objetivo_ingesta_s) or objetivo_ingesta_s <= 0):
            raise ValueError("El objetivo de ingesta debe ser positivo y finito")
        self.objetivo_ingesta_s = objetivo_ingesta_s
        self._reloj = reloj or time.perf_counter
        self._ultima_lectura = self._reloj()
        self._lecturas_vacias: dict[str, int] = defaultdict(int)
        self._llegadas: dict[str, int] = defaultdict(int)
        self._previos: dict[str, tuple[int, float]] = {}
        self._llegada = 0

    def encolar(self, agente: str, n: int = 1, ordenes: list[dict] | None = None) -> None:
        """Suma `n` a la cola del agente o, con `ordenes`, las registra (`ref`, `prioridad`, `tipo`, `fecha_objetivo`) y
        suma cuántas son. Falla cerrado antes de tocar nada: una orden sin `ref`, con una `ref` repetida o con una
        prioridad fuera de ALTA | NORMAL | BAJA se rechaza (sin prioridad, NORMAL, como en `Bloque.ciclo`)."""
        nuevas = []
        if ordenes is not None:
            vistas = set()
            for o in ordenes:
                ref, prioridad = o.get("ref"), o.get("prioridad", "NORMAL")
                if not ref or not isinstance(ref, str):
                    raise ValueError(f"HT-08: orden sin referencia en la cola de {agente}")
                if prioridad not in PRIORIDADES:
                    raise ValueError(f"HT-08: prioridad {prioridad!r} de {ref} fuera de {'|'.join(PRIORIDADES)}")
                tipo = o.get("tipo")
                if tipo is not None and tipo not in TIPOS:
                    raise ValueError(f"HT-08: tipo {tipo!r} de {ref} fuera de {'|'.join(sorted(TIPOS))}")
                fecha = _fecha_objetivo(o.get("fecha_objetivo"), ref)
                if ref in vistas:
                    raise ValueError(f"HT-08: {ref} repetida en la cola de {agente}")
                vistas.add(ref)
                nuevas.append({"ref": ref, "prioridad": prioridad, "tipo": tipo, "fecha_objetivo": fecha})
            n = len(nuevas)
        with self._lock:
            if repetidas := {p["ref"] for p in self.pendientes[agente]} & {o["ref"] for o in nuevas}:
                raise ValueError(f"HT-08: {', '.join(sorted(repetidas))} ya en la cola de {agente}")
            for o in nuevas:
                self._llegada += 1
                self.pendientes[agente].append({**o, "llegada": self._llegada})
            self.cola[agente] += n
            self._llegadas[agente] += n

    def retirar(self, agente: str, ref: str) -> None:
        """Saca de la cola una orden atendida (T-178). Una referencia que no está en la cola se rechaza."""
        with self._lock:
            pend = self.pendientes[agente]
            i = next((k for k, p in enumerate(pend) if p["ref"] == ref), None)
            if i is None:
                raise KeyError(f"HT-08: {ref} no está en la cola de {agente}")
            del pend[i]
            self.cola[agente] = max(self.cola[agente] - 1, 0)

    def inicio(self, agente: str) -> float:
        return self._reloj()

    def fin(self, agente: str, t0: float) -> None:
        # T-178 r02 (QA r01, H-06): una orden con detalle solo sale de la cola con `retirar`; `fin` (la ruta de
        # `Agentes.llamar`) no baja el contador por debajo del detalle, para que el CAR- no se contradiga
        with self._lock:
            self.cola[agente] = max(self.cola[agente] - 1, len(self.pendientes[agente]))
            self.completados[agente] += 1
            self.tiempo_total[agente] += self._reloj() - t0

    def evaluar_instancias(self) -> list[dict]:
        """Devuelve órdenes ORD- (ABRIR) para agentes sin estado con cola > umbral. Un agente con estado (instancia única)
        nunca recibe ORD- (PB-19): su cola se reordena por prioridad y queda un CAR- de la saturación con la cola
        reordenada y, si está en el camino de la entrega, el aviso al Coordinador sobre plazos (T-178; prompt del
        Orquestador V5.0, 5.3 punto 5). La propuesta de tipo 3 si se repite la decide `carga.registrar_carga`, que lee HA."""
        nuevas = []
        with self._lock:
            ahora = self._reloj()
            ventana = ahora - self._ultima_lectura
            for ag, q in self.cola.items():
                if ag not in SIN_ESTADO:
                    if q > self.umbral_cola:
                        nuevas.append(self._saturacion(ag, q))
                    continue
                prev_n, prev_s = self._previos.get(ag, (0, 0.0))
                n = self.completados[ag] - prev_n
                ocupado = self.tiempo_total[ag] - prev_s
                media = ocupado / n if n else None
                antes = self.instancias[ag]
                lenta = ag == "AG-12" and self.objetivo_ingesta_s is not None and media is not None and media > self.factor_tiempo * self.objetivo_ingesta_s
                rho = ocupado / (ventana * antes) if ventana > 0 else None
                tasa = self._llegadas[ag] / ventana if ventana > 0 else None
                metricas = {"cola": q, "W": media, "rho": rho, "lambda": tasa, "mu": 1 / media if media else None}
                if lenta or q > self.umbral_cola:
                    self._lecturas_vacias[ag] = 0
                    if tasa is not None and media:
                        c = math.ceil(tasa * media / self.rho_objetivo)
                        calculo = f"c = ⌈λ/(μ·{self.rho_objetivo})⌉"
                    else:
                        c = antes + 1
                        calculo = "primera apertura por cola sin tasa observada"
                    destino = min(max(c, antes + 1), self.instancias_max)
                    if destino > antes:
                        nuevas.append({"tipo_entrada": "ORD", "agente": ag, "accion": "ABRIR", "instancias_antes": antes,
                                       "instancias_despues": destino, "metricas_disparo": metricas, "calculo": calculo})
                        self.instancias[ag] = destino
                elif antes > 1:
                    libre = q == 0 and rho is not None and rho < self.rho_cierre
                    self._lecturas_vacias[ag] = self._lecturas_vacias[ag] + 1 if libre else 0
                    if self._lecturas_vacias[ag] >= self.lecturas_cierre:
                        self.instancias[ag] -= 1
                        self._lecturas_vacias[ag] = 0
                        nuevas.append({"tipo_entrada": "ORD", "agente": ag, "accion": "CERRAR", "instancias_antes": antes,
                                       "instancias_despues": antes - 1, "metricas_disparo": metricas,
                                       "calculo": f"{self.lecturas_cierre} lecturas con cola 0 y ρ < {self.rho_cierre}"})
                if ag == "AG-12" and antes > 1 and media is not None and self.objetivo_ingesta_s is not None:
                    nuevas.append({"tipo_entrada": "CAR", "agente": ag, "saturado": False, "W": media,
                                   "objetivo": self.objetivo_ingesta_s, "rho": rho, "instancias": self.instancias[ag],
                                   "en_objetivo": media <= self.objetivo_ingesta_s})
                self._previos[ag] = self.completados[ag], self.tiempo_total[ag]
                self._llegadas[ag] = 0
            self._ultima_lectura = ahora
            self.ordenes.extend(nuevas)
        return nuevas

    def _saturacion(self, ag: str, q: int) -> dict:
        """CAR- de un agente de instancia única saturado (se llama con el cerrojo tomado). Reordena su cola en el monitor.
        Solo contadores: los tiempos dependen del reloj y harían HA irreproducible."""
        antes = self.pendientes[ag]
        orden = sorted(antes, key=clave_prioridad)
        self.pendientes[ag] = orden
        cola = [{"posicion": i, "ref": p["ref"], "prioridad": p["prioridad"], "tipo": p["tipo"],
                 "fecha_objetivo": p["fecha_objetivo"]} for i, p in enumerate(orden, start=1)]
        car = {"tipo_entrada": "CAR", "agente": ag, "cola": q, "instancias": 1, "encargos_completados": self.completados[ag],
               "saturado": True, "umbral_cola": self.umbral_cola, "reordenada": True,
               "orden_cambiado": [p["ref"] for p in orden] != [p["ref"] for p in antes], "cola_reordenada": cola,
               "sin_detalle": max(q - len(orden), 0), "afecta_plazos": ag in CAMINO_ENTREGA,
               "nota": "agente con estado: instancia única; no se abren instancias y se reordena por prioridad"}
        if car["afecta_plazos"]:
            car["aviso_coordinador"] = {
                "destinatario": "AG-01", "en_espera_sobre_umbral": q - self.umbral_cola,
                "motivo": (f"{ag} es instancia única con cola (4.5 del Documento 0): {q} órdenes en cola con el umbral en "
                           f"{self.umbral_cola}; se atienden en serie y por prioridad, y las que esperan pueden retrasar su plazo"),
                "ordenes": [{"posicion": c["posicion"], "ref": c["ref"], "fecha_objetivo": c["fecha_objetivo"]} for c in cola]}
        return car

    def instantanea(self) -> dict:
        with self._lock:
            return {ag: {"cola": self.cola[ag], "completados": self.completados[ag],
                         "W_medio_s": round(self.tiempo_total[ag] / self.completados[ag], 4) if self.completados[ag] else None,
                         "instancias": self.instancias[ag]}
                    for ag in sorted(set(self.cola) | set(self.completados))}
