"""Contabilidad de consumo (tokens, búsquedas, UC, coste) y presupuestos en UC por segmento y fase."""
from __future__ import annotations

import threading
from collections import defaultdict
from dataclasses import asdict
from typing import Dict, List, Optional

from .llm import Uso


class Contabilidad:
    def __init__(self, cfg: Dict) -> None:
        self.cfg = cfg
        self._lock = threading.Lock()
        self.llamadas: List[Dict] = []
        self.motor: Dict[str, float] = defaultdict(float)

    def uc_de(self, uso: Uso) -> float:
        u = self.cfg.get("uc") or {}
        ent_eq = uso.entrada + uso.cache_escritura + float(u.get("factor_lectura_cache", 0.1)) * uso.cache_lectura
        return round(0.5 * ent_eq / float(u.get("tokens_entrada_por_uc", 8000))
                     + 0.5 * uso.salida / float(u.get("tokens_salida_por_uc", 1500)), 4)

    def coste_de(self, modelo: str, uso: Uso) -> Optional[float]:
        precios = (self.cfg.get("precios_por_millon") or {}).get(modelo) or {}
        claves = ("entrada", "salida", "escritura_cache", "lectura_cache")
        if any(precios.get(k) is None for k in claves):
            return None
        c = (uso.entrada * precios["entrada"] + uso.salida * precios["salida"]
             + uso.cache_escritura * precios["escritura_cache"] + uso.cache_lectura * precios["lectura_cache"]) / 1e6
        pw = self.cfg.get("precio_busqueda_web_por_mil")
        if uso.busquedas_web:
            if pw is None:
                return None
            c += uso.busquedas_web * pw / 1000
        return round(c, 6)

    def registrar(self, run_id: Optional[str], agente: str, modelo: str, uso: Uso, segmento: Optional[str] = None,
                  fase: Optional[str] = None, cache_hit: bool = False) -> float:
        uc = 0.0 if cache_hit else self.uc_de(uso)
        with self._lock:
            self.llamadas.append({"run_id": run_id, "agente": agente, "modelo": modelo, "segmento": segmento, "fase": fase,
                                  "cache_hit": cache_hit, "uc": uc, **asdict(uso)})
        return uc

    def cargar_motor(self, run_id: Optional[str], uc: float) -> None:
        with self._lock:
            self.motor[run_id or "-"] += uc

    def resumen(self, run_id: Optional[str] = None) -> Dict:
        with self._lock:
            ll = [c for c in self.llamadas if run_id is None or c["run_id"] == run_id]
            motor = sum(v for k, v in self.motor.items() if run_id is None or k == run_id)
        tot = {"llamadas": len(ll), "entrada": 0, "salida": 0, "cache_escritura": 0, "cache_lectura": 0, "busquedas_web": 0}
        coste, coste_ok = 0.0, True
        for c in ll:
            for k in ("entrada", "salida", "cache_escritura", "cache_lectura", "busquedas_web"):
                tot[k] += c[k]
            if not c["cache_hit"]:
                cc = self.coste_de(c["modelo"], Uso(**{k: c[k] for k in ("entrada", "salida", "cache_escritura", "cache_lectura", "busquedas_web")}))
                if cc is None:
                    coste_ok = False
                else:
                    coste += cc
        tot["uc_llm"] = round(sum(c["uc"] for c in ll), 4)
        tot["uc_motor"] = round(motor, 4)
        tot["uc"] = round(tot["uc_llm"] + motor, 4)
        tot["coste_estimado"] = round(coste, 4) if coste_ok and ll else None
        por_agente: Dict[str, Dict] = defaultdict(lambda: {"llamadas": 0, "uc": 0.0, "entrada": 0, "salida": 0})
        for c in ll:
            a = por_agente[c["agente"]]
            a["llamadas"] += 1
            a["uc"] = round(a["uc"] + c["uc"], 4)
            a["entrada"] += c["entrada"] + c["cache_escritura"] + c["cache_lectura"]
            a["salida"] += c["salida"]
        tot["por_agente"] = dict(por_agente)
        return tot


class PresupuestoAgotado(RuntimeError):
    pass


class Presupuesto:
    """Presupuesto en UC de un RUN por segmento (y una bolsa común para las fases transversales)."""

    def __init__(self, asignado: Dict[str, float], cfg: Dict) -> None:
        self.asignado = {k: float(v) for k, v in asignado.items()}
        self.consumido: Dict[str, float] = defaultdict(float)
        self.ampliado: Dict[str, float] = defaultdict(float)
        self.cfg = cfg
        self._lock = threading.Lock()
        self.cierres: List[Dict] = []

    def disponible(self, segmento: str) -> float:
        with self._lock:
            return self.asignado.get(segmento, 0.0) * (1 + float((self.cfg.get("presupuesto_uc") or {}).get("ampliacion_sin_autorizacion", 0.25))) \
                + self.ampliado[segmento] - self.consumido[segmento]

    def cargar(self, segmento: str, uc: float) -> None:
        with self._lock:
            self.consumido[segmento] += uc

    def puede(self, segmento: str, estimado: float) -> bool:
        return self.disponible(segmento) >= estimado

    def ampliar(self, segmento: str, uc: float) -> None:
        with self._lock:
            self.ampliado[segmento] += uc

    def cierre_parcial(self, segmento: str, fase: str, motivo: str) -> None:
        with self._lock:
            self.cierres.append({"segmento": segmento, "fase": fase, "motivo": motivo})

    def resumen(self) -> Dict:
        with self._lock:
            return {k: {"asignado": self.asignado.get(k, 0.0), "ampliado": round(self.ampliado[k], 4),
                        "consumido": round(self.consumido[k], 4)} for k in sorted(set(self.asignado) | set(self.consumido))}
