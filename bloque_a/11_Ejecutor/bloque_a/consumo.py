"""Contabilidad de consumo (tokens, búsquedas, UC, coste) y presupuestos en UC por clase y fase.

T-146: el presupuesto corta antes de cada petición al modelo. `ReservaLlamada` reserva en la bolsa el peor caso de la
petición (la entrada entera con el margen del tokenizador y como escritura de caché, `max_tokens` de salida y las búsquedas
al máximo) antes de enviarla, cobra lo real después y libera el resto; si no cabe, pide la ampliación con la regla del
ejecutor, recorta la salida a lo que cabe o, por debajo de la salida mínima, no la envía y la fase se cierra declarada."""
from __future__ import annotations

import json
import math
import threading
from collections import defaultdict
from collections.abc import Callable
from dataclasses import asdict, fields
from typing import Any

from .configuracion import parametro
from .llm import Uso, _tokens_aprox


class Contabilidad:
    def __init__(self, cfg: dict) -> None:
        self.cfg = cfg
        self._lock = threading.Lock()
        self.llamadas: list[dict] = []
        self.motor: dict[str, float] = defaultdict(float)

    def uc_de(self, uso: Uso) -> float:
        ent_eq = uso.entrada + uso.cache_escritura + float(parametro(self.cfg, "uc.factor_lectura_cache")) * uso.cache_lectura
        uc = (0.5 * ent_eq / float(parametro(self.cfg, "uc.tokens_entrada_por_uc"))
              + 0.5 * uso.salida / float(parametro(self.cfg, "uc.tokens_salida_por_uc")))
        if uso.busquedas_web:   # T-146: cada búsqueda web cuenta en UC (antes no contaba)
            uc += uso.busquedas_web * float(parametro(self.cfg, "uc.uc_por_busqueda_web"))
        return round(uc, 4)

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
        sumados = {k: sum(c[k] for c in ll if not c["cache_hit"])
                   for k in ("entrada", "salida", "cache_escritura", "cache_lectura", "busquedas_web")}   # T-146: con las búsquedas
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

    def __init__(self, asignado: dict[str, float], cfg: dict, tope_total: float | None = None) -> None:
        self.asignado = {k: float(v) for k, v in asignado.items()}
        self.consumido: dict[str, float] = defaultdict(float)
        self.ampliado: dict[str, float] = defaultdict(float)
        self.cfg = cfg
        self._lock = threading.Lock()
        self.cierres: list[dict] = []
        # T-146: lo reservado por las peticiones en curso (su peor caso) y el coste real de las ya hechas de una llamada que aún
        # no se ha cargado; lo retenido de las primas «solo» de los prefijos compartidos hasta `liquidar_primas`; las salidas
        # recortadas para caber; las peticiones que costaron más de lo reservado; y el factor de tokens observado por bolsa
        self.reservado: dict[str, float] = defaultdict(float)
        self.retenido: dict[str, float] = defaultdict(float)
        self.recortes: list[dict] = []
        self.excesos: list[dict] = []
        self.factor_observado: dict[str, float] = {}
        # T-146: con un reparto por encima del ciclo (N3 forzado en el periódico o un override), cada bolsa se escala para que
        # la suma de los límites con la ampliación máxima no pase de `tope_total` con esa misma ampliación
        total = sum(v for v in self.asignado.values() if v > 0)
        self._escala = min(1.0, float(tope_total) / total) if tope_total is not None and total > 0 else 1.0
        # T-88: (bolsa, agente) que ya pagaron la escritura de su prefijo en este run; primas «solo» por bolsa y primas reales
        # pendientes de liquidar, en tokens (enteros: la suma no depende del orden de los hilos)
        self._llamados: set = set()
        # T-88 r02 (QA r01, H-02): por grupo de prefijos (los analistas, que comparten el núcleo V6, o cada agente compartido),
        # los pesos «solo» de cada bolsa y los tokens escritos de verdad; aparte, los tokens que ya cargó cada bolsa
        self._pesos: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self._reales: dict[str, int] = defaultdict(int)
        self._cargadas: dict[str, int] = defaultdict(int)

    def _base(self, clase: str) -> float:
        return self.asignado.get(clase, 0.0) * self._escala

    def _limite(self, clase: str) -> float:
        """Límite actual de la bolsa: la base con el margen sin autorización y lo autorizado (con el cerrojo tomado)."""
        return self._base(clase) * (1 + float(parametro(self.cfg, "presupuesto_uc.ampliacion_sin_autorizacion"))) + self.ampliado[clase]

    def _ocupado(self, clase: str) -> float:
        return self.consumido[clase] + self.reservado[clase] + self.retenido[clase]

    def limite(self, clase: str) -> float:
        with self._lock:
            return self._limite(clase)

    def limite_maximo(self, clase: str) -> float:
        """T-146: el límite de la bolsa con la ampliación máxima autorizable (el tope de `autorizar_hasta_tope`)."""
        return self._base(clase) * (1 + float(parametro(self.cfg, "presupuesto_uc.ampliacion_max_autorizable")))

    def disponible(self, clase: str) -> float:
        with self._lock:
            return self._limite(clase) - self._ocupado(clase)

    def reservar(self, clase: str, uc: float) -> bool:
        """T-146: reserva `uc` si caben en lo que queda (comprobación y reserva bajo el mismo cerrojo)."""
        with self._lock:
            if self._limite(clase) - self._ocupado(clase) + 1e-9 >= uc:
                self.reservado[clase] += uc
                return True
            return False

    def retener_real(self, clase: str, uc: float) -> None:
        """T-146: el coste real de una petición ya hecha, apartado sin comprobar (ya se gastó) hasta que se cargue."""
        with self._lock:
            self.reservado[clase] += uc

    def liberar(self, clase: str, uc: float) -> None:
        with self._lock:
            self.reservado[clase] -= uc
            if abs(self.reservado[clase]) < 1e-9:
                self.reservado[clase] = 0.0

    def anotar(self, lista: str, entrada: dict) -> None:
        with self._lock:
            getattr(self, lista).append(entrada)

    def factor_de(self, clase: str, base: float) -> float:
        with self._lock:
            return max(base, self.factor_observado.get(clase, 0.0))

    def observar_factor(self, clase: str, factor: float) -> None:
        with self._lock:
            self.factor_observado[clase] = max(factor, self.factor_observado.get(clase, 0.0))

    def absorber(self, otro: Presupuesto) -> None:
        """T-146: suma a esta lo consumido y declarado en `otro` (la bolsa con la que corre el informe de aprendizaje, C5,
        antes de que el ciclo reparta su presupuesto)."""
        otro.liquidar_primas()
        with otro._lock:
            consumido, cierres = dict(otro.consumido), list(otro.cierres)
            recortes, excesos = list(otro.recortes), list(otro.excesos)
        with self._lock:
            for bolsa, uc in consumido.items():
                self.consumido[bolsa] += uc
            self.cierres.extend(cierres)
            self.recortes.extend(recortes)
            self.excesos.extend(excesos)

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

    def cargar_con_prima(self, bolsa: str, grupo: str, leido: float, tokens_solo: int, tokens_cargar: int, tokens_reales: int,
                         tokens_retener: int = 0) -> None:
        """T-88: carga la lectura de lo cacheado y `tokens_cargar` de prima (la del analista propio de la bolsa, que siempre la
        escribe ella; ver `Bloque._cargar`). La prima «solo» (`tokens_solo`, lo que escribiría la bolsa si fuera la única) es
        el peso del reparto, y los tokens escritos de verdad quedan pendientes de `liquidar_primas`, por grupo de prefijos.
        T-146: la prima de `tokens_retener` queda retenida en la bolsa (no se puede gastar) hasta la liquidación, que le
        carga como mucho eso: así la bolsa no pasa de su límite al liquidar."""
        with self._lock:
            self.consumido[bolsa] += leido + self._uc_prima(tokens_cargar)
            self.retenido[bolsa] += self._uc_prima(tokens_retener)
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
            self.retenido.clear()   # T-146: lo retenido para las primas ya está cargado

    def puede(self, clase: str, estimado: float) -> bool:
        return self.disponible(clase) >= estimado

    def autorizar_hasta_tope(self, clase: str, estimado: float, fase_admitida: bool) -> tuple[bool, float]:
        """T-92 (auditoría de Astra, A6): el máximo incluye tanto el margen automático como lo ya autorizado, y la
        comprobación y el ajuste comparten el cerrojo. Lectura prudente de «ampliación máxima autorizable» del Anexo A como
        tope del total (base × (1 + 0,50)), no como un 50 % adicional al margen automático (INC-T92-01, [PROPUESTO])."""
        sin_aut = float(parametro(self.cfg, "presupuesto_uc.ampliacion_sin_autorizacion"))
        maximo = float(parametro(self.cfg, "presupuesto_uc.ampliacion_max_autorizable"))
        with self._lock:
            base = self._base(clase)
            actual = base * (1 + sin_aut) + self.ampliado[clase]
            falta = estimado + self._ocupado(clase) - actual   # T-146: también lo reservado y lo retenido
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


def _volcar(o: Any) -> Any:
    """Para medir una petición con bloques del SDK (la continuación tras `pause_turn` reenvía el contenido devuelto)."""
    if hasattr(o, "model_dump"):
        return o.model_dump()
    if hasattr(o, "__dict__"):
        return vars(o)
    return str(o)


def tokens_de_peticion(system: list[dict], mensajes: list[dict], herramientas: list[dict] | None) -> int:
    """Tokens de entrada de una petición con la aproximación del ejecutor (3,6 caracteres por token, `llm._tokens_aprox`):
    los bloques del system prompt, los mensajes y la definición de las herramientas."""
    texto = "".join(str(b.get("text", "")) for b in system or [])
    texto += json.dumps(mensajes, ensure_ascii=False, default=_volcar)
    if herramientas:
        texto += json.dumps(herramientas, ensure_ascii=False, default=_volcar)
    return _tokens_aprox(texto)


def busquedas_maximas(herramientas: list[dict] | None) -> int:
    """Las búsquedas web que puede hacer una petición como mucho (`max_uses` de la herramienta de búsqueda)."""
    return sum(int(h.get("max_uses", 0) or 0) for h in herramientas or []
               if "web_search" in str(h.get("type", "")) or h.get("name") == "web_search")


class ReservaLlamada:
    """T-146: el presupuesto de una llamada a un agente, petición a petición (la primera, cada reparación y cada continuación).

    `reservar` aparta en la bolsa el peor caso de la petición antes de enviarla: la entrada medida con el margen del
    tokenizador (`presupuesto_uc.reserva.factor_tokens_entrada`, o el mayor observado en la bolsa) y toda como escritura de
    caché (no hay garantía de lectura), `max_tokens` de salida y las búsquedas al máximo, convertido a UC con
    `Contabilidad.uc_de`. Si no cabe, pide la ampliación con la regla del ejecutor (`ampliar`); si se deniega, recorta la
    salida a lo que cabe (nunca por debajo de `presupuesto_uc.reserva.salida_minima_tokens`) y, si ni eso cabe, la petición
    no sale (`negada` lleva el motivo). `pagar` cambia la reserva de una petición por su coste real, que queda apartado
    hasta que `cerrar` lo suelta y `Bloque._cargar` lo carga. Una llamada corre en un solo hilo."""

    def __init__(self, presupuesto: Presupuesto, bolsa: str, contabilidad: Contabilidad, agente: str,
                 ampliar: Callable[[float], bool] | None = None) -> None:
        self.p = presupuesto
        self.bolsa = bolsa
        self.cont = contabilidad
        self.agente = agente
        self.ampliar = ampliar
        cfg = presupuesto.cfg
        self.factor = float(parametro(cfg, "presupuesto_uc.reserva.factor_tokens_entrada"))
        self.salida_minima = int(parametro(cfg, "presupuesto_uc.reserva.salida_minima_tokens"))
        self.tokens_salida_por_uc = float(parametro(cfg, "uc.tokens_salida_por_uc"))
        self._abiertas: list[tuple[float, int]] = []   # (peor caso en UC, tokens de entrada estimados sin margen)
        self._pagado = Uso()                           # lo pagado petición a petición en la generación en curso
        self._apartado = 0.0                           # coste real de las peticiones hechas, apartado hasta `cerrar`
        self.peticiones = 0
        self.prefijo: int | None = None                # lo cacheado (leído o escrito) en la primera petición
        self.negada: str | None = None
        self.peor_total = 0.0                          # suma de lo reservado (para las pruebas y el análisis)

    def _peor(self, tokens: int, salida: int, busquedas: int) -> float:
        return self.cont.uc_de(Uso(entrada=tokens, salida=salida, busquedas_web=busquedas))

    def reservar(self, system: list[dict], mensajes: list[dict], herramientas: list[dict] | None, max_tokens: int) -> int | None:
        """Reserva la siguiente petición. Devuelve el `max_tokens` con el que puede salir o None si no cabe."""
        bruto = tokens_de_peticion(system, mensajes, herramientas)
        tokens = math.ceil(bruto * self.p.factor_de(self.bolsa, self.factor))
        busq = busquedas_maximas(herramientas)
        completo = self._peor(tokens, int(max_tokens), busq)
        concedido = self.p.reservar(self.bolsa, completo) or (
            self.ampliar is not None and self.ampliar(completo) and self.p.reservar(self.bolsa, completo))
        if concedido:
            return self._abrir(completo, bruto, int(max_tokens))
        # Degradar: la salida que cabe en lo que queda (con una diezmilésima de UC de holgura por el redondeo de uc_de)
        libre = self.p.disponible(self.bolsa) - self._peor(tokens, 0, busq) - 1e-4
        mt = min(int(max_tokens), math.floor(libre * 2 * self.tokens_salida_por_uc)) if libre > 0 else 0
        if mt >= self.salida_minima:
            w = self._peor(tokens, mt, busq)
            if self.p.reservar(self.bolsa, w):
                self.p.anotar("recortes", {"clase": self.bolsa, "agente": self.agente, "peticion": self.peticiones + 1,
                                           "max_tokens": int(max_tokens), "max_tokens_enviado": mt,
                                           "peor_caso_uc": round(completo, 4), "reservado_uc": round(w, 4)})
                return self._abrir(w, bruto, mt)
        quien = self.agente if self.peticiones == 0 else f"otra petición de {self.agente} (reparación o continuación)"
        self.negada = f"presupuesto insuficiente para {quien} ({completo:.2f} UC en el peor caso)"
        return None

    def _abrir(self, w: float, bruto: int, mt: int) -> int:
        self._abiertas.append((w, bruto))
        self.peticiones += 1
        self.peor_total += w
        return mt

    def pagar(self, uso: Uso) -> None:
        """La petición más antigua sin pagar ha terminado con `uso`: suelta su reserva y aparta su coste real."""
        w, bruto = self._abiertas.pop(0) if self._abiertas else (0.0, 0)
        self.p.liberar(self.bolsa, w)
        real = self.cont.uc_de(uso)
        self.p.retener_real(self.bolsa, real)
        self._apartado += real
        self._pagado.sumar(uso)
        entrada = uso.entrada + uso.cache_escritura + uso.cache_lectura
        if self.prefijo is None:
            self.prefijo = uso.cache_lectura + uso.cache_escritura
        if bruto and entrada > bruto * self.p.factor_de(self.bolsa, self.factor):
            self.p.observar_factor(self.bolsa, entrada / bruto)   # el margen no bastó: las siguientes peticiones usan lo visto
        if real > w + 1e-4:
            self.p.anotar("excesos", {"clase": self.bolsa, "agente": self.agente, "reservado_uc": round(w, 4), "real_uc": round(real, 4)})

    def pagar_resto(self, uso_total: Uso) -> None:
        """Al volver del cliente: lo que la generación costó y no se pagó petición a petición se paga como una petición, y
        las reservas que no llegaron a salir se sueltan."""
        resto = Uso(**{f.name: max(0, getattr(uso_total, f.name) - getattr(self._pagado, f.name)) for f in fields(Uso)})
        if self._abiertas or any(asdict(resto).values()):
            self.pagar(resto)
        for w, _ in self._abiertas:
            self.p.liberar(self.bolsa, w)
        self._abiertas.clear()
        self._pagado = Uso()

    def cerrar(self) -> None:
        """Suelta lo reservado y lo apartado de esta llamada (después se carga lo real con `Bloque._cargar`)."""
        for w, _ in self._abiertas:
            self.p.liberar(self.bolsa, w)
        self._abiertas.clear()
        if self._apartado:
            self.p.liberar(self.bolsa, self._apartado)
            self._apartado = 0.0
