"""HT-08 · Monitor de colas y consumo: colas por agente, tiempos, consumo frente a presupuesto
y órdenes de apertura de instancias (R25) para los agentes sin estado."""
from __future__ import annotations

import math
import threading
import time
from collections import defaultdict
from typing import Dict, List

SIN_ESTADO = {"AG-03", "AG-04", "AG-05", "AG-06", "AG-07", "AG-08", "AG-09", "AG-10", "AG-11", "AG-12",
              "AG-13", "AG-14", "AG-15", "AG-16", "AG-17"}


class Monitor:
    def __init__(self, umbral_cola: int = 3, instancias_max: int = 8) -> None:
        self.umbral_cola = umbral_cola
        self.instancias_max = instancias_max
        self._lock = threading.Lock()
        self.cola: Dict[str, int] = defaultdict(int)
        self.completados: Dict[str, int] = defaultdict(int)
        self.tiempo_total: Dict[str, float] = defaultdict(float)
        self.instancias: Dict[str, int] = defaultdict(lambda: 1)
        self.ordenes: List[Dict] = []

    def encolar(self, agente: str, n: int = 1) -> None:
        with self._lock:
            self.cola[agente] += n

    def inicio(self, agente: str) -> float:
        return time.perf_counter()

    def fin(self, agente: str, t0: float) -> None:
        with self._lock:
            self.cola[agente] = max(self.cola[agente] - 1, 0)
            self.completados[agente] += 1
            self.tiempo_total[agente] += time.perf_counter() - t0

    def evaluar_instancias(self) -> List[Dict]:
        """Devuelve órdenes ORD- (ABRIR) para agentes sin estado con cola > umbral; para agentes con
        estado solo se registra la saturación (CAR-), nunca se abren instancias (PB-19)."""
        nuevas = []
        with self._lock:
            for ag, q in self.cola.items():
                if q <= self.umbral_cola:
                    continue
                if ag in SIN_ESTADO:
                    antes = self.instancias[ag]
                    c = min(max(math.ceil(q / (self.umbral_cola * 0.75)), antes + 1), self.instancias_max)
                    if c > antes:
                        self.instancias[ag] = c
                        nuevas.append({"tipo_entrada": "ORD", "agente": ag, "accion": "ABRIR", "instancias_antes": antes,
                                       "instancias_despues": c, "metricas_disparo": {"cola": q},
                                       "calculo": "c = ⌈cola/(umbral·0,75)⌉"})
                else:
                    nuevas.append({"tipo_entrada": "CAR", "agente": ag, "cola": q, "instancias": 1,
                                   "nota": "agente con estado: instancia única; se reordena por prioridad"})
            self.ordenes.extend(nuevas)
        return nuevas

    def instantanea(self) -> Dict:
        with self._lock:
            return {ag: {"cola": self.cola[ag], "completados": self.completados[ag],
                         "W_medio_s": round(self.tiempo_total[ag] / self.completados[ag], 4) if self.completados[ag] else None,
                         "instancias": self.instancias[ag]}
                    for ag in sorted(set(self.cola) | set(self.completados))}
