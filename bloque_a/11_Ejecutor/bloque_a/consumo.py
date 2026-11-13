"""Contabilidad de consumo (tokens, búsquedas, UC, coste) y presupuestos en UC por clase y fase."""
from __future__ import annotations

import threading
from collections import defaultdict
from dataclasses import asdict
from typing import Any

from .configuracion import parametro
from .llm import Uso


class Contabilidad:
    def __init__(self, cfg: dict) -> None:
        self.cfg = cfg
        self._lock = threading.Lock()
        self.llamadas: list[dict] = []
        self.motor: dict[str, float] = defaultdict(float)

    def uc_de(self, uso: Uso) -> float:
        ent_eq = uso.entrada + uso.cache_escritura + float(parametro(self.cfg, "uc.factor_lectura_cache")) * uso.cache_lectura
        return round(0.5 * ent_eq / float(parametro(self.cfg, "uc.tokens_entrada_por_uc"))
                     + 0.5 * uso.salida / float(parametro(self.cfg, "uc.tokens_salida_por_uc")), 4)

    def coste_de(self, modelo: str, uso: Uso) -> float | None:
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

    def registrar(self, run_id: str | None, agente: str, modelo: str, uso: Uso, clase: str | None = None,
                  fase: str | None = None, cache_hit: bool = False, intento: int = 1, latencia_s: float = 0.0) -> float:
        uc = 0.0 if cache_hit else self.uc_de(uso)
        with self._lock:
            # T-101 (idea 6): el intento (1 = primera; 2 o más = reparación) y la latencia de cada llamada
            self.llamadas.append({"run_id": run_id, "agente": agente, "modelo": modelo, "clase": clase, "fase": fase,
                                  "cache_hit": cache_hit, "uc": uc, "intento": int(intento), "latencia_s": round(float(latencia_s), 4),
                                  **asdict(uso)})
        return uc

    def cargar_motor(self, run_id: str | None, uc: float) -> None:
        with self._lock:
            self.motor[run_id or "-"] += uc

    def resumen(self, run_id: str | None = None) -> dict:
        with self._lock:
            ll = [c for c in self.llamadas if run_id is None or c["run_id"] == run_id]
            motor = sum(v for k, v in self.motor.items() if run_id is None or k == run_id)
        tot: dict[str, Any] = {"llamadas": len(ll), "entrada": 0, "salida": 0, "cache_escritura": 0, "cache_lectura": 0, "busquedas_web": 0}
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
        tot["reintentos"] = sum(1 for c in ll if c.get("intento", 1) > 1)
        tot["latencia_s"] = round(sum(c.get("latencia_s", 0.0) for c in ll), 4)
        # T-113 (H-15 de T-107): la UC del total se calcula con los tokens sumados, no sumando cifras ya redondeadas; si no,
        # depende de qué llamada escribió un prefijo compartido (orden de los hilos) en la cuarta cifra
        sumados = {k: sum(c[k] for c in ll if not c["cache_hit"]) for k in ("entrada", "salida", "cache_escritura", "cache_lectura")}
        tot["uc_llm"] = self.uc_de(Uso(**sumados)) if ll else 0.0
        tot["uc_motor"] = round(motor, 4)
        tot["uc"] = round(tot["uc_llm"] + motor, 4)
        tot["coste_estimado"] = round(coste, 4) if coste_ok and ll else None
        por_agente: dict[str, dict] = defaultdict(lambda: {"llamadas": 0, "uc": 0.0, "entrada": 0, "salida": 0})
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
    """Presupuesto en UC de un RUN por clase (y una bolsa común para las fases transversales)."""

    def __init__(self, asignado: dict[str, float], cfg: dict) -> None:
        self.asignado = {k: float(v) for k, v in asignado.items()}
        self.consumido: dict[str, float] = defaultdict(float)
        self.ampliado: dict[str, float] = defaultdict(float)
        self.cfg = cfg
        self._lock = threading.Lock()
        self.cierres: list[dict] = []
        # T-88: (bolsa, agente) que ya pagaron la escritura de su prefijo en este run; primas «solo» por bolsa y primas reales
        # pendientes de liquidar, en tokens (enteros: la suma no depende del orden de los hilos)
        self._llamados: set = set()
        # T-88 r02 (QA r01, H-02): por grupo de prefijos (los analistas, que comparten el núcleo V6, o cada agente compartido),
        # los pesos «solo» de cada bolsa y los tokens escritos de verdad; aparte, los tokens que ya cargó cada bolsa
        self._pesos: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self._reales: dict[str, int] = defaultdict(int)
        self._cargadas: dict[str, int] = defaultdict(int)

    def disponible(self, clase: str) -> float:
        with self._lock:
            return self.asignado.get(clase, 0.0) * (1 + float(parametro(self.cfg, "presupuesto_uc.ampliacion_sin_autorizacion"))) \
                + self.ampliado[clase] - self.consumido[clase]

    def cargar(self, clase: str, uc: float) -> None:
        with self._lock:
            self.consumido[clase] += uc

    def primera_llamada(self, bolsa: str, agente: str) -> bool:
        """True la primera vez que se pregunta por (bolsa, agente) en este presupuesto (un run)."""
        with self._lock:
            nuevo = (bolsa, agente) not in self._llamados
            self._llamados.add((bolsa, agente))
            return nuevo

    def _uc_prima(self, tokens: float) -> float:
        """UC de más que cuesta escribir `tokens` en la caché en lugar de leerlos (la parte de entrada de `Contabilidad.uc_de`)."""
        return 0.5 * tokens * (1 - float(parametro(self.cfg, "uc.factor_lectura_cache"))) / float(parametro(self.cfg, "uc.tokens_entrada_por_uc"))

    def cargar_con_prima(self, bolsa: str, grupo: str, leido: float, tokens_solo: int, tokens_cargar: int, tokens_reales: int) -> None:
        """T-88: carga la lectura de lo cacheado y `tokens_cargar` de prima (la del analista propio de la bolsa, que siempre la
        escribe ella; ver `Bloque._cargar`). La prima «solo» (`tokens_solo`, lo que escribiría la bolsa si fuera la única) es
        el peso del reparto, y los tokens escritos de verdad quedan pendientes de `liquidar_primas`, por grupo de prefijos."""
        with self._lock:
            self.consumido[bolsa] += leido + self._uc_prima(tokens_cargar)
            self._pesos[grupo][bolsa] += int(tokens_solo)
            self._reales[grupo] += int(tokens_reales)
            self._cargadas[bolsa] += int(tokens_cargar)

    def liquidar_primas(self) -> None:
        """T-88: en cada grupo de prefijos, reparte los tokens escritos de verdad en proporción a los pesos «solo», y quita lo
        que ya se cargó durante la fase. El total cargado vuelve a ser el real y el reparto no depende del orden de los hilos.
        Un grupo sin pesos va a la bolsa común."""
        with self._lock:
            for grupo in sorted(self._reales):
                pesos, reales = self._pesos.get(grupo, {}), self._reales[grupo]
                total = sum(pesos.values())
                if not total:
                    self.consumido["COMUN"] += self._uc_prima(reales)
                    continue
                for bolsa in sorted(pesos):
                    self.consumido[bolsa] += self._uc_prima(reales * pesos[bolsa] / total)
            for bolsa in sorted(self._cargadas):
                self.consumido[bolsa] -= self._uc_prima(self._cargadas[bolsa])
            self._pesos.clear()
            self._reales.clear()
            self._cargadas.clear()

    def puede(self, clase: str, estimado: float) -> bool:
        return self.disponible(clase) >= estimado

    def autorizar_hasta_tope(self, clase: str, estimado: float, fase_admitida: bool) -> tuple[bool, float]:
        """T-92 (auditoría de Astra, A6): el máximo incluye tanto el margen automático como lo ya autorizado, y la
        comprobación y el ajuste comparten el cerrojo. Lectura prudente de «ampliación máxima autorizable» del Anexo A como
        tope del total (base × (1 + 0,50)), no como un 50 % adicional al margen automático (INC-T92-01, [PROPUESTO])."""
        sin_aut = float(parametro(self.cfg, "presupuesto_uc.ampliacion_sin_autorizacion"))
        maximo = float(parametro(self.cfg, "presupuesto_uc.ampliacion_max_autorizable"))
        with self._lock:
            base = self.asignado.get(clase, 0.0)
            actual = base * (1 + sin_aut) + self.ampliado[clase]
            falta = estimado + self.consumido[clase] - actual
            concede = fase_admitida and falta > 0 and actual + falta <= base * (1 + maximo) + 1e-9
            if concede:
                self.ampliado[clase] += falta
            return concede, falta

    def ampliar(self, clase: str, uc: float) -> None:
        with self._lock:
            self.ampliado[clase] += uc

    def cierre_parcial(self, clase: str, fase: str, motivo: str) -> None:
        with self._lock:
            self.cierres.append({"clase": clase, "fase": fase, "motivo": motivo})

    def resumen(self) -> dict:
        self.liquidar_primas()
        with self._lock:
            return {k: {"asignado": self.asignado.get(k, 0.0), "ampliado": round(self.ampliado[k], 4),
                        "consumido": round(self.consumido[k], 4)} for k in sorted(set(self.asignado) | set(self.consumido))}
