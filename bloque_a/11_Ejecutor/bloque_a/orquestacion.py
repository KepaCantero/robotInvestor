"""Orquestación de los ciclos del Bloque A en el ejecutor.

C1 (periódico) y C2 (ad hoc): fases F0–F8 (sección 7.3 del Documento 0 óptima V5.0) con puertas de continuidad
GC0–GC3, presupuestos en UC por tipo de activo y fase, Analistas de los doce tipos de activo en paralelo (R25),
selección determinista con HT-03 y sin duplicados entre tipos (regla 5 de 2.6),
validación G3 con HT-09 (y dictamen del Orquestador si no es APTO), redacción, congelación de pronósticos
(F4) y registro (F1, F3, F5). F9 (auditoría) y C5 (evaluación) nunca bloquean la entrega.
Frontera con el Bloque B (2.4–2.5, R21): cada opción es un ámbito con su indicador de seguimiento (un símbolo del
universo, que sirve para medir y resolver los pronósticos) y su encargo para el Bloque B; nunca un activo concreto.
C3 (consultas): ruta N0 desde la memoria del bloque o escalado a C2. CT-04: decisiones y configuración.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from . import sintesis as sint
from .agentes import Agentes
from .almacen import Almacen, Reloj
from .anonimizacion import Anonimizador
from .configuracion import (
    ANTIGUEDAD_PS2,
    CLASES,
    HORIZONTES,
    NOMBRE_CLASE,
    aplicabilidad,
)
from .consumo import Contabilidad, Presupuesto
from .contratos import (
    AGENTE_CLASE,
    ESQUEMAS,
    Mensajeria,
    contiene_credenciales,
    sanear_contenido_externo,
    sanear_estructura,
)
from .evaluador import PROB_DE_BANDA, Evaluador, banda_de, banda_publicable
from .herramientas import ht03, ht09
from .herramientas.ht01_datos import DatosNoDisponibles
from .herramientas.ht05_planificador import fecha_resolucion
from .herramientas.ht06_indice import (
    RE_ID,
    CacheResultados,
    Indice,
    clave_hash,
    normalizar,
)
from .herramientas.ht08_monitor import Monitor
from .interfaz_broker import ConsultasBroker, Credenciales
from .llm import LLMClient, Uso
from .motor import Motor
from .redaccion import Redaccion
from .referencias import Referencias
from .seguimiento import Seguimientos

INSTR = {
    "CRIBADO_E_INVESTIGACION": (
        "Fases F1 (cribado) y F2 (investigación dirigida) de tu tipo de activo. Aplica tu estrategia al universo de "
        "ÁMBITOS recibido: cada candidata es un ámbito (mercado, sector, subsector, temática, segmento, factor, estilo o "
        "estrategia; nunca un activo concreto) y DEBE llevar «indicador_seguimiento» con «simbolo» igual a un símbolo del "
        "universo (sirve para medir y resolver pronósticos, no es una recomendación). Usa las señales y cálculos CALC- "
        "entregados, revisa las condiciones de invalidación de las opciones vigentes, devuelve como máximo {max_cand} "
        "candidatas en «cribado» (con paso_gc1 y motivo) y como máximo {max_fin} finalistas con ficha completa: "
        "tipo_opcion, subtipo, «ambito» (incluye, excluye, región), «invertibilidad» del ámbito (universo negociable "
        "suficiente y accesible), encargo para el Bloque B («criterios_seleccion_sugeridos», «metricas_clave», "
        "«preguntas_para_B»), nombres concretos solo en «ejemplos_ilustrativos», "
        "dimensiones T/E/M/A/P (múltiplos de 10, «NA»/«NE»; A: asimetria, valoracion, catalizadores, momento, "
        "invertibilidad), «segunda_pasada» de las dimensiones decisivas si un total "
        "queda a ≤ 5 puntos de un umbral, horizontes aplicables según la tabla de tu clase, afirmaciones con su fuente "
        "(HT-01:<símbolo>, CALC-… o REF-… de las referencias disponibles), invalidación cualitativa y cuantitativa "
        "(símbolo, umbral de precio, dirección), pre-mortem y lo que no sabes. Si necesitas conocimiento, usa "
        "«peticiones_conocimiento» [{{tipo: CT-07|CT-08, pregunta, para: símbolo del indicador}}] (máximo {max_pet})."),
    "REVISION_VIGENTES": (
        "Nivel N1 · arrastre verificado (GC0 sin cambio material). Solo revisa las opciones vigentes (condiciones de "
        "invalidación y datos) y, con la rotación exploratoria, como máximo 2 «exploratorias» del universo indicado. "
        "No investigues candidatas nuevas."),
    "RESPUESTA_OBJECIONES": (
        "Responde a cada objeción fuerte o moderada del Analista de hipótesis contrarias con evidencia o declárala sin "
        "resolver («resuelta»: false). Una objeción fuerte sin resolver excluye la opción del top-3."),
}


def simbolo_seguimiento(x: dict) -> str | None:
    """Símbolo HT-01 del indicador de seguimiento de una ficha o de un registro de F3. Compatibilidad: los
    registros y respuestas V4.x usaban «proxy_backtest»."""
    ind = x.get("indicador_seguimiento")
    if isinstance(ind, dict) and ind.get("simbolo"):
        return ind["simbolo"]
    return x.get("simbolo_seguimiento") or x.get("proxy_backtest")


def _semana(fecha) -> str:
    f = pd.Timestamp(fecha)
    return f"Semana {f.isocalendar()[1]} de {f.isocalendar()[0]}"


def _sesiones_entre(desde, hasta, festivos: dict) -> int:
    """Sesiones hábiles en [desde, hasta) sin los cierres habituales de mercado (`ps2_festivos`, [PROPUESTO]): Viernes
    Santo y fechas fijas MM-DD. Así el dato de la última sesión real vale en H1 tras un puente o un festivo."""
    d0, d1 = pd.Timestamp(desde).normalize(), pd.Timestamp(hasta).normalize()
    if d1 <= d0:
        return 0
    cierres = [d for d in pd.date_range(d0, d1) if d.strftime("%m-%d") in set(festivos.get("fijos") or [])]
    if festivos.get("viernes_santo"):
        from pandas.tseries.holiday import GoodFriday
        cierres += list(GoodFriday.dates(d0, d1))
    return int(np.busday_count(d0.date(), d1.date(), holidays=[d.date() for d in cierres]))


class Bloque:
    def __init__(self, cfg: dict, proveedor, universo: pd.DataFrame, cliente: LLMClient, carpeta_estado,
                 carpeta_entregables=None, anonimizar: bool | None = None) -> None:
        # Copia propia: la tabla de horizontes vigente (P-31, F10) se escribe en ella en cada ciclo y no debe pasar a
        # otras instancias que compartan el dict del llamador (T-53, QA r02 H-12)
        self.cfg = copy.deepcopy(cfg)
        cfg = self.cfg
        self.modo = cfg.get("modo", "vivo")
        self.proveedor = proveedor
        self._sin_historia: dict[tuple[str, str], list[str]] = {}   # (clase, run_id) → símbolos sin dato a la fecha as_of
        self._fichas_rechazadas: dict[tuple[str, str], list[str]] = {}   # (clase, run_id) → fichas del lote rechazadas
        self.universo = universo.copy()
        self.reloj = Reloj(cfg.get("zona_horaria", "Europe/Madrid"))
        self.almacen = Almacen(carpeta_estado, self.reloj)
        self.carpeta_entregables = Path(carpeta_entregables or (cfg.get("rutas") or {}).get("entregables", "./entregables"))
        self.contabilidad = Contabilidad(cfg)
        self.monitor = Monitor(int((cfg.get("paralelismo") or {}).get("umbral_cola", 3)))
        self.cache = CacheResultados(Path(carpeta_estado) / "cache_resultados.jsonl")
        self.cliente = cliente
        self.agentes = Agentes(cfg, cliente, self.almacen, self.contabilidad, self.monitor, self.cache)
        self.motor = Motor(self.almacen, proveedor, cfg, self.contabilidad)
        self.evaluador = Evaluador(self.almacen, proveedor, self.motor, cfg, self.universo)
        self.mensajeria = Mensajeria(self.almacen)
        self.referencias = Referencias(cfg)
        self.redaccion = Redaccion(cfg)
        anon = (cfg.get("backtest") or {}).get("anonimizar", False) if anonimizar is None else anonimizar
        self.anon = Anonimizador(self.universo) if anon else None
        self.params_ht03 = ht03.fusionar_parametros(cfg.get("_parametros_ht03"))
        self._incidencias_universo_registradas = False
        self._inicializar_f10()
        # V5.1: comunicación fluida con el Broker (CT-23), credenciales en la bóveda de HT-01 (CT-25) y
        # seguimientos encargados de opción (CT-24, ciclo C6, F11)
        self.consultas = ConsultasBroker(self)
        self.credenciales = Credenciales(self, Path(carpeta_estado) / "boveda")
        self.seguimientos = Seguimientos(self)

    # ====================================================================================
    # Utilidades
    # ====================================================================================
    def fijar_fecha(self, as_of) -> pd.Timestamp:
        f = pd.Timestamp(as_of).normalize()
        self.proveedor.fijar_as_of(f)
        self.reloj.fijar(f.date())
        return f

    def _inicializar_f10(self) -> None:
        if self.almacen.leer("F10"):
            return
        a = self.cfg
        params = [("P-01", "Periodicidad del ciclo C1", "SEMANAL · SAB 06:00 · entrega LUN 07:00", "SERVICIO"),
                  ("P-02", "Clases de activo activas", list(CLASES), "SERVICIO"),
                  ("P-03", "Horizontes de interés", list(HORIZONTES), "SERVICIO"),
                  ("P-09", "Umbrales de elegibilidad", self.params_ht03["umbrales"], "CALIBRABLE"),
                  ("P-11", "Pesos de RK", self.params_ht03["pesos_rk"], "CALIBRABLE"),
                  ("P-17", "Presupuesto de referencia (UC)", a.get("presupuesto_uc"), "CALIBRABLE"),
                  ("P-29", "Idioma", a.get("idioma", "es-ES"), "SERVICIO"),
                  ("P-30", "Versión de metodología", a.get("methodology_version", "4.0"), "CALIBRABLE"),
                  ("P-32", "Índices de referencia por clase", a.get("indices_referencia"), "OPERADOR")]
        for pid, nombre, valor, reg in params:
            self.almacen.escribir("F10", "OPERADOR", {"tipo_entrada": "PARAMETRO", "param_id": pid, "nombre": nombre,
                                                      "valor_inicial": valor, "valor_vigente": valor, "regimen": reg})

    def f10(self, as_of=None) -> dict[str, Any]:
        return {k: v.get("valor_vigente") for k, v in self.almacen.estado("F10", as_of).items()}

    def _contexto(self, as_of, run_id, clase=None, extra=None) -> dict:
        f10 = self.f10(as_of)
        ctx = {"fecha_as_of": str(pd.Timestamp(as_of).date()), "modo": self.modo, "run_id": run_id,
               "methodology_version": f10.get("P-30", "4.0"), "anonimizado": bool(self.anon),
               "lecciones": self.evaluador.lecciones_vigentes(as_of, clase),
               "f10": {"umbrales": f10.get("P-09"), "pesos_rk": f10.get("P-11"), "horizontes_interes": f10.get("P-03")}}
        if extra:
            ctx.update(extra)
        return ctx

    def _vista(self, obj):
        return self.anon.entrada(obj) if self.anon else obj

    def _real(self, obj):
        return self.anon.salida(obj) if self.anon else obj

    def _invocar(self, agente, contrato, mensaje, esquema, instrucciones, as_of, run_id, clase=None, fase=None,
                 presupuesto: Presupuesto | None = None, bolsa=None, permitir_web=False, max_uc_estimado=None):
        """Llamada a un agente con control de presupuesto (estimación previa) y anonimización."""
        bolsa = bolsa or clase or "COMUN"
        if presupuesto is not None:
            est = max_uc_estimado if max_uc_estimado is not None else self._estimar_uc(agente, mensaje)
            if not presupuesto.puede(bolsa, est):
                if not self._solicitar_ampliacion(presupuesto, bolsa, est, run_id, fase):
                    presupuesto.cierre_parcial(bolsa, fase or contrato, f"presupuesto insuficiente para {agente} ({est:.2f} UC estimadas)")
                    return None
        ctx = self._contexto(as_of, run_id, clase)
        r = self.agentes.invocar(agente, contrato, self._vista(mensaje), esquema, instrucciones, self._vista(ctx), run_id,
                                 clase, fase, permitir_web)
        if presupuesto is not None:
            presupuesto.cargar(bolsa, r.uc)
        if r.datos is not None:
            r.datos = self._real(r.datos)
        return r

    def _estimar_uc(self, agente: str, mensaje: dict) -> float:
        n_user = len(json.dumps(mensaje, ensure_ascii=False, default=str)) / 3.6 + 1500
        n_sys = len(self.agentes.prompts.texto(agente)) / 3.6
        return self.contabilidad.uc_de(Uso(entrada=int(n_user), cache_lectura=int(n_sys), salida=2500))

    def _solicitar_ampliacion(self, presupuesto: Presupuesto, bolsa: str, est: float, run_id: str, fase: str | None) -> bool:
        """Ampliación > 25 % (10.3): el Orquestador decide en el ciclo periódico con la regla de valor de la
        información; tope total configurable (por defecto +50 %)."""
        pu = self.cfg.get("presupuesto_uc") or {}
        asignado = presupuesto.asignado.get(bolsa, 0.0)
        tope = asignado * float(pu.get("ampliacion_max_autorizable", 0.5))
        falta = est - presupuesto.disponible(bolsa)
        ya = presupuesto.ampliado[bolsa]
        autoriza = falta > 0 and ya + falta <= tope + 1e-9 and fase in ("prospectiva", "refutacion", "respuesta_objeciones")
        self.almacen.escribir("HA", "AG-18", {"tipo_entrada": "AUT", "id": self.almacen.nuevo_id("AUT"), "run_id": run_id,
                                              "solicitante": "AG-02", "bolsa": bolsa, "presupuesto_base": asignado,
                                              "ampliacion_uc": round(falta, 4), "valor_informacion": f"fase {fase}: puede cambiar el top-3",
                                              "decision": "AUTORIZADA" if autoriza else "DENEGADA",
                                              "motivo": "dentro del tope de ampliación" if autoriza else "supera el tope o la fase no cambia la decisión"})
        if autoriza:
            presupuesto.ampliar(bolsa, falta)
        return autoriza

    def _registrar_r9(self, hallazgos: list[dict], run_id: str | None) -> None:
        for h in hallazgos:
            self.almacen.incidencia("MANIPULACION", f"Instrucción incrustada neutralizada en {h['origen']} (R9)", h["origen"],
                                    tratamiento="instrucción retirada; contenido tratado como dato; fuente degradada",
                                    fragmento=h["fragmento"], run_id=run_id)

    def _universo_clase(self, clase: str, run_id: str | None) -> list[dict]:
        filas, hallazgos = [], []
        for _, f in self.universo[self.universo["clase"] == clase].iterrows():
            if not self.proveedor.tiene(f["simbolo"]):
                continue
            d = f.to_dict()
            d["notas"], h = sanear_contenido_externo(d["notas"], f"universo:{f['simbolo']}")
            hallazgos += h
            filas.append(d)
        if hallazgos and not self._incidencias_universo_registradas:
            self._registrar_r9(hallazgos, run_id)
        return filas

    # ====================================================================================
    # Señales deterministas por clase (Motor, PLAN_MIN)
    # ====================================================================================
    def senales_clase(self, clase: str, as_of, run_id: str) -> tuple[dict[str, dict], list[str]]:
        ini = str((pd.Timestamp(as_of) - pd.DateOffset(years=3, days=30)).date())
        simbolos, sin_historia = [], []
        for f in self._universo_clase(clase, run_id):
            # Un símbolo sin datos en la ventana del lote (empieza a cotizar después de as_of o dejó de cotizar antes
            # de la ventana) no puede tumbar las fichas del tipo entero: se excluye y se declara (R14, R16, PS2).
            try:
                self.proveedor.cierres(f["simbolo"], ini, as_of)
                simbolos.append(f["simbolo"])
            except DatosNoDisponibles:
                sin_historia.append(f["simbolo"])
        self._sin_historia[(clase, run_id)] = sin_historia
        self._fichas_rechazadas[(clase, run_id)] = []
        datos = [{"serie": s, "inicio": ini} for s in simbolos]
        tabla: dict[str, dict] = {s: {} for s in simbolos}
        calcs: list[str] = []
        for ficha, params in (("ACC-MOM-001", {}), ("FX-VOL-001", {"ventana": 20}), ("FX-TREND-001", {"ventana_semanas": 26}),
                              ("RISK-DD-001", {}), ("ST-DESC-001", {"posicion_ultimo": True}), ("FIN-CAGR-001", {})):
            r = self.motor.servir({"operacion": ficha, "plan": "PLAN_MIN", "clase": clase, "datos": datos, "parametros": params,
                                   "perfil": ["TRANSVERSAL"], "fecha_corte": str(pd.Timestamp(as_of).date())}, "AG-02", run_id)
            if r["estado"] == "RECHAZADO":   # nunca en silencio: se declara como laguna del tipo
                self._fichas_rechazadas[(clase, run_id)].append(ficha)
                continue
            calcs.append(r["calc_id"])
            for s, v in (r["resultado"].get("tabla") or {}).items():
                t = tabla[s]
                t.setdefault("calc_ids", []).append(r["calc_id"])
                if ficha == "ACC-MOM-001":
                    t.update({"momentum_12_1": v["momentum"], "pct_momentum_clase": v.get("percentil_transversal"),
                              "z_momentum_clase": v.get("z_transversal"), "senal_tsmom": v["senal_tsmom"]})
                elif ficha == "FX-VOL-001":
                    t.update({"vol_20d": v["volatilidad_anual"], "vol_ewma": v["ewma_anual"]})
                elif ficha == "FX-TREND-001":
                    t.update({"tendencia_26s": v["direccion"], "p_tendencia": v["p_valor"], "pendiente_sen_semanal": v["pendiente_sen"]})
                elif ficha == "RISK-DD-001":
                    t.update({"riesgo_1a5": v["riesgo_1a5"], "mdd": v["mdd"], "drawdown_actual": v["drawdown_actual"],
                              "vol_anual_3a": v["volatilidad_anual"]})
                elif ficha == "ST-DESC-001":
                    pos = v.get("posicion_precio") or {}
                    t.update({"z_precio_3a": pos.get("z"), "pct_precio_3a": pos.get("percentil")})
                elif ficha == "FIN-CAGR-001":
                    t.update({k: v.get(k) for k in ("rent_1s", "rent_1m", "rent_3m", "rent_12m")})
        for s, t in tabla.items():
            try:
                fd, precio = self.proveedor.valor_en(s, as_of)
                t["precio"] = round(precio, 6)
                t["fecha_dato"] = str(fd.date())
            except DatosNoDisponibles:
                pass
            # Señal compuesta (GC1, Anexo A): familias momento, tendencia y valoración relativa
            fam = []
            if t.get("pct_momentum_clase") is not None:
                fam.append(t["pct_momentum_clase"])
            if t.get("tendencia_26s"):
                fam.append({"creciente": 1.0, "sin tendencia": 0.5, "decreciente": 0.0}[t["tendencia_26s"]])
            if t.get("pct_precio_3a") is not None:
                fam.append(1 - t["pct_precio_3a"] * 0.5)
            t["senal_compuesta"] = round(sum(fam) / len(fam), 4) if fam else None
            t["familias_concordantes"] = sum(1 for x in fam if x >= 0.6)
            if self.anon and "precio" in t:
                self.anon.factores[s] = 100.0 / t["precio"] if t["precio"] else 1.0
                t["precio"] = 100.0
        return {s: t for s, t in tabla.items() if t}, calcs

    # ====================================================================================
    # F0 · GC0 (determinista)
    # ====================================================================================
    def vigentes(self, as_of, clase: str | None = None) -> list[dict]:
        return [o for o in self.almacen.estado("F3", as_of).values()
                if o.get("estado") in ("PROPUESTA", "VIGENTE") and (clase is None or o.get("clase") == clase)]

    def _referencia(self, clase: str, simbolo: str | None = None) -> str | None:
        """Referencia de comparación del tipo de activo (8.4): símbolo, «CESTA», «SUBYACENTE» (columna «subyacente»
        del universo para el indicador; si falta, CESTA) o «NINGUNA»/vacío (pronóstico absoluto: posición neutra)."""
        ref = (self.cfg.get("indices_referencia") or {}).get(clase, "CESTA")
        if ref is None or str(ref).strip().upper() in ("", "NINGUNA", "NONE"):
            return None
        if str(ref).upper() == "SUBYACENTE":
            fila = self.universo[self.universo["simbolo"] == simbolo] if simbolo else self.universo.iloc[0:0]
            sub = str(fila["subyacente"].iloc[0]).strip() if len(fila) and "subyacente" in fila else ""
            return sub if sub and self.proveedor.tiene(sub) else "CESTA"
        return ref

    def gc0(self, clase: str, as_of, vigentes: list[dict]) -> dict:
        g = self.cfg.get("gc0") or {}
        motivos, invalidadas = [], []
        previos = [r for r in self.almacen.leer("F5", as_of) if r.get("tipo_entrada") == "RUN" and clase in (r.get("nivel_por_clase") or {})]
        if not previos:
            motivos.append("sin ciclo anterior de la clase (memoria vacía)")
        ref = self._referencia(clase)
        try:
            sims = [ref] if ref not in (None, "CESTA") else [s for s in self.evaluador.simbolos_clase(clase)]
            semanas = int(g.get("ventana_sigma_semanas", 104))
            serie = pd.concat([self.proveedor.cierres(s, pd.Timestamp(as_of) - pd.Timedelta(weeks=semanas + 2), as_of).pct_change()
                               for s in sims], axis=1).mean(axis=1).dropna()
            sem = (1 + serie).resample("W-FRI").prod().dropna() - 1
            if len(sem) > 10:
                sigma = float(sem.iloc[:-1].std(ddof=1))
                ult = float(sem.iloc[-1])
                if abs(ult) > float(g.get("sigma_semanal", 1.5)) * sigma:
                    motivos.append(f"movimiento semanal de la clase {ult:+.2%} > {g.get('sigma_semanal', 1.5)} σ ({sigma:.2%})")
        except (DatosNoDisponibles, ValueError):
            motivos.append("datos de la referencia de la clase no disponibles (modo degradado)")
        for v in vigentes:
            for inv in v.get("invalidacion_cuantitativa") or []:
                try:
                    _, precio = self.proveedor.valor_en(inv["simbolo"], as_of)
                except DatosNoDisponibles:
                    continue
                u = float(inv["umbral"])
                cruzada = precio < u if inv["direccion"] == "por_debajo" else precio > u
                if cruzada:
                    invalidadas.append(v["opp_id"])
                    motivos.append(f"condición de invalidación cumplida en {v['opp_id']}")
                elif abs(precio - u) / precio < float(g.get("invalidacion_cercana", 0.10)):
                    motivos.append(f"condición de invalidación a < {g.get('invalidacion_cercana', 0.1):.0%} en {v['opp_id']}")
        for ev in g.get("eventos_calendario") or []:
            f = pd.Timestamp(ev["fecha"])
            if clase in ev.get("clases", []) and pd.Timestamp(as_of) - pd.Timedelta(days=7) < f <= pd.Timestamp(as_of) + pd.Timedelta(days=7):
                motivos.append(f"evento de calendario: {ev.get('evento')}")
        ultimo = previos[-1]["_fecha"] if previos else None
        nuevas = [l for l in self.evaluador.lecciones_vigentes(as_of, clase) if ultimo and l["fecha"] > ultimo]
        if nuevas:
            motivos.append(f"{len(nuevas)} lección(es) nueva(s) aplicable(s)")
        prometedoras = [o for o in self.almacen.estado("F3", as_of).values()
                        if o.get("clase") == clase and o.get("estado") == "CANDIDATA" and o.get("exploratoria_prometedora")]
        if prometedoras:
            motivos.append("candidata exploratoria prometedora del ciclo anterior")
        return {"cambio_material": bool(motivos), "motivos": motivos, "invalidadas": invalidadas,
                "arrastre_verificado": not motivos}

    # ====================================================================================
    # Ciclo C1 / C2
    # ====================================================================================
    def ciclo(self, as_of=None, tipo: str = "PERIODICO", alcance: dict | None = None, nivel_forzado: str | None = None,
              horizontes: list[str] | None = None, disparador: dict | None = None, prioridad: str = "NORMAL",
              presupuesto_override: dict[str, float] | None = None) -> dict:
        as_of = self.fijar_fecha(as_of or pd.Timestamp.today())
        run_id = self.almacen.nuevo_id("RUN")
        limitaciones: list[str] = []
        # C5 primero (no bloquea): resolución, métricas, certificados, lecciones
        try:
            res_eval = self.evaluador.ciclo(as_of, run_id)
        except Exception as e:  # pragma: no cover - modo degradado
            res_eval = {"error": str(e)}
            self.almacen.incidencia("HERRAMIENTA", f"Evaluador no disponible: {e}", "AG-20", severidad="Operativa")
        self._informe_aprendizaje(res_eval, as_of, run_id)

        f10 = self.f10(as_of)
        # La aplicabilidad de horizontes vigente es la de F10 (P-31) si el Evaluador la degradó (12.2); si no, la tabla 8.3
        self.cfg["_tabla_horizontes"] = self.evaluador._matriz_aplicabilidad(as_of)
        activas = list(f10.get("P-02") or CLASES)
        clases = [c for c in ((alcance or {}).get("clases") or activas) if c in activas]
        # V5.1 (7.9): las consultas CT-23 vencidas siguen con su supuesto declarado; una BLOQUEANTE sin respuesta pausa
        # en este punto de control (F0) los tipos de activo afectados, y el resto del análisis sigue
        self.consultas.vencer(as_of)
        pausadas = self.consultas.clases_pausadas(as_of, clases)
        if pausadas:   # también si queda pausado todo el alcance: entonces el run no analiza nada y lo declara
            clases = [c for c in clases if c not in pausadas]
            limitaciones += [f"{NOMBRE_CLASE[c]}: pausado en F0 a la espera de la respuesta del Broker a {k} (consulta BLOQUEANTE, R26)"
                             for c, k in sorted(pausadas.items())]
        hz_interes = horizontes or list(f10.get("P-03") or HORIZONTES)
        vigentes = {c: self.vigentes(as_of, c) for c in clases}
        gc0 = {c: self.gc0(c, as_of, vigentes[c]) for c in clases}
        if tipo == "PERIODICO" and not nivel_forzado:
            nivel = {c: "N2" if gc0[c]["cambio_material"] else "N1" for c in clases}
        else:
            nivel = {c: nivel_forzado or ("N3" if tipo == "PROFUNDIZACION" else "N2") for c in clases}
        pu = self.cfg.get("presupuesto_uc") or {}
        asign = {c: float(pu.get(nivel[c], 20)) for c in clases}
        if tipo != "PERIODICO" and any(nivel[c] == "N3" for c in clases):
            asign = {c: float(pu.get("N3", 50)) / max(len(clases), 1) for c in clases}
        asign["COMUN"] = max(float(pu.get("ciclo_semanal_max", 160)) - sum(asign.values()), 0.1 * float(pu.get("ciclo_semanal_max", 160)))
        if presupuesto_override:
            asign.update(presupuesto_override)
        presupuesto = Presupuesto(asign, self.cfg)
        memoria = {"opp_vigentes": [v["opp_id"] for c in clases for v in vigentes[c]],
                   "tnd_activas": [t["tnd_id"] for t in self.almacen.estado("F1", as_of).values() if t.get("estado") not in ("archivada", "invalidada")][:50],
                   "lec_aplicables": [l["id"] for l in self.evaluador.lecciones_vigentes(as_of)],
                   "certificados": [c["id"] for c in self.evaluador.certificados_vigentes(as_of)]}
        self.mensajeria.crear("CT-05", "AG-01", "AG-02", {"tipo": tipo, "alcance": alcance or {"clases": clases},
                                                          "nivel_por_clase": nivel, "presupuesto_por_clase": asign, "memoria": memoria,
                                                          "delta_gc0": gc0, "fecha_objetivo": str(as_of.date()), "horizontes": hz_interes},
                              run_id=run_id, presupuesto={"uc": sum(asign.values())})

        # F1–F4 por clase (paralelo, R25); las escrituras se hacen después en orden determinista
        hilos = int((self.cfg.get("paralelismo") or {}).get("hilos_analistas", 4))
        # Señales del Motor en orden determinista (los identificadores CALC- no dependen del paralelismo)
        pre = {}
        for c in clases:
            try:
                pre[c] = self.senales_clase(c, as_of, run_id)
            except Exception as e:  # modo degradado (PS2)
                pre[c] = e
        # Prompts de los Analistas cargados en el hilo principal (incidencia única si alguno trabaja con el marco común)
        self.agentes.verificar_prompts([AGENTE_CLASE[c] for c in clases], run_id)
        tareas = {c: (c, nivel[c], vigentes[c], gc0[c], as_of, run_id, presupuesto, hz_interes, alcance or {}, pre[c]) for c in clases}
        with ThreadPoolExecutor(max_workers=max(1, hilos)) as ex:
            futuros = {c: ex.submit(self._analizar_clase, *args) for c, args in tareas.items()}
            analisis = {c: futuros[c].result() for c in clases}
        for orden in self.monitor.evaluar_instancias():
            self.almacen.escribir("HA", "AG-18", {**orden, "id": self.almacen.nuevo_id(orden["tipo_entrada"]), "run_id": run_id})

        # Registro de evidencia (F2) y asignación de identificadores en orden determinista
        for c in clases:
            self._registrar_evidencia_clase(analisis[c], as_of, run_id)
        # Clústeres de exposición entre todas las finalistas (ML-CLUS-001)
        clusteres = self._clusteres(analisis, as_of, run_id)
        # F5 · Selección por clase con HT-03
        seleccion = {c: self._seleccionar(c, analisis[c], clusteres, as_of, run_id, hz_interes) for c in clases}
        # Regla 5 de 2.6: una misma oportunidad no puede aparecer en dos top-3 distintos
        self._deduplicar_entre_tipos(seleccion)
        # Integración del Analizador (CT-05 retorno): régimen, factores, preguntas
        integ = self._integrar(seleccion, analisis, gc0, nivel, as_of, run_id, presupuesto)
        historial = self.evaluador.historial_aciertos(as_of)
        paquete, extras = sint.construir(self, run_id, tipo, as_of, clases, nivel, gc0, analisis, seleccion, clusteres, integ,
                                         historial, presupuesto)
        if clusteres.get("rechazo"):
            limitaciones = limitaciones + [(f"clústeres de exposición no calculados ({clusteres['rechazo']}): la concentración entre "
                                            "opciones no se ha podido medir en este ciclo")]
        if limitaciones:
            paquete["limitaciones"] = limitaciones + [x for x in paquete["limitaciones"] if not x.startswith("Ninguna limitación")]
        # F6 · G3 (HT-09) + dictamen del Orquestador si no es APTO
        paquete, g3 = self._validar_g3(paquete, extras, as_of, run_id)
        estado_run = "COMPLETO"
        if presupuesto.cierres or pausadas or clusteres.get("rechazo") or any(a.get("estado") == "PARCIAL" for a in analisis.values()):
            estado_run = "PARCIAL"   # un tipo pausado por una consulta BLOQUEANTE deja el run incompleto (7.9)
        resultado = {"run_id": run_id, "as_of": str(as_of.date()), "tipo": tipo, "nivel_por_clase": nivel, "gc0": gc0,
                     "g3": g3, "estado": estado_run, "paquete": paquete, "entregables": None, "evaluacion": res_eval}
        if g3["dictamen"] == "BLOQUEADO":
            resultado["estado"] = "PARCIAL"
            resultado["entrega"] = "BLOQUEADA"
            self._registrar_run(resultado, analisis, seleccion, presupuesto, gc0, disparador, alcance, hz_interes, prioridad, [], [])
            return resultado
        # F7 · Redacción, HT-07 y segunda pasada de HT-09
        entreg, g3b, red = self._redactar(paquete, extras, as_of, run_id, presupuesto, estado_run)
        resultado["entregables"] = entreg
        resultado["g3_entregables"] = g3b
        if g3b["dictamen"] == "BLOQUEADO":
            resultado["estado"] = "PARCIAL"
            resultado["entrega"] = "BLOQUEADA"
            self._registrar_run(resultado, analisis, seleccion, presupuesto, gc0, disparador, alcance, hz_interes, prioridad, [], [])
            return resultado
        # F8 · Congelación (F4), estados (F1, F3), historial (F5) y entrega CT-02
        prg = self._congelar(extras, as_of, run_id)
        self._escribir_f1_f3(analisis, seleccion, extras, as_of, run_id)
        self._registrar_run(resultado, analisis, seleccion, presupuesto, gc0, disparador, alcance, hz_interes, prioridad, prg, entreg)
        self.mensajeria.crear("CT-02", "AG-01", "BROKER", {"entregables": entreg, "resumen": {
            "top3_por_clase": {c: [o["opp_id"] for o in paquete["clases"][c]["opciones"]] for c in paquete["clases"]},
            "cambios_vs_anterior": integ.get("cambios_vs_anterior", ""), "apuestas_independientes": paquete["apuestas_independientes"]},
            "estado_g3": g3b["dictamen"]}, run_id=run_id, tipo_mensaje="RETORNO", estado=resultado["estado"])
        resultado["prg_congelados"] = prg
        # F9 · Auditoría asíncrona (nunca bloquea)
        self._auditar(resultado, tipo, nivel, as_of, run_id)
        resultado["consumo"] = self.contabilidad.resumen(run_id)
        resultado["presupuesto"] = presupuesto.resumen()
        return resultado

    # ------------------------------------------------------------------------------------
    def _informe_aprendizaje(self, res_eval: dict, as_of, run_id: str) -> None:
        if not res_eval or not res_eval.get("resueltos") or not (self.cfg.get("evaluacion") or {}).get("llm_informe_aprendizaje", True):
            return
        resumen = {k: {"n": m["n"], "brier": m.get("brier"), "brier_ref": m.get("brier_ref"),
                       "acierto": (m.get("acierto") or {}).get("tasa"), "calibracion_global": m.get("calibracion_global")}
                   for k, m in (res_eval.get("metricas") or {}).items()}
        msg = {"tarea": "C5_INFORME_APRENDIZAJE", "resueltos_hoy": res_eval["resueltos"], "metricas_por_celda": resumen,
               "certificados": {"emitidos": [c["id"] for c in res_eval["certificados"]["emitidos"]],
                                "insuficientes": res_eval["certificados"]["insuficientes"]},
               "lecciones_deterministas": [l["observacion"] for l in res_eval.get("lecciones_nuevas", [])]}
        r = self._invocar("AG-20", "C5", msg, "APRENDIZAJE",
                          "Redacta el informe de aprendizaje (CT-19) a partir de las métricas: resumen y, solo si los datos lo "
                          "sostienen, lecciones con ámbito, observación factual con cifras, recomendación y fuerza.", as_of, run_id)
        if not r or not r.datos:
            return
        n_tot = sum(m["n"] for m in resumen.values())
        for l in r.datos.get("lecciones", [])[:3]:
            fuerza = l.get("fuerza", "anecdotica")
            if fuerza == "estadistica" and n_tot < 30:
                fuerza = "anecdotica"
            self.evaluador._nueva_leccion(as_of, l.get("ambito") or {}, l.get("tipo", "PREDICTIVA"), l["observacion"],
                                          l["recomendacion"], fuerza, [run_id], n_tot, origen="AG-20")
        self.mensajeria.crear("CT-19", "AG-20", "AG-02", {"informe": r.datos.get("resumen", "")}, run_id=run_id,
                              tipo_mensaje="RETORNO", estado="COMPLETO")

    # ====================================================================================
    # F1–F4 por clase
    # ====================================================================================
    def _analizar_clase(self, clase, nivel, vigentes, gc0, as_of, run_id, presupuesto: Presupuesto, hz_interes, alcance, pre=None) -> dict:
        agente = AGENTE_CLASE[clase]
        sc = self.cfg.get("seleccion") or {}
        out = {"clase": clase, "nivel": nivel, "estado": "COMPLETO", "finalistas": [], "cribado": [], "descartadas": [],
               "revision_vigentes": [], "regimen": "", "lagunas": [], "calc_ids": [], "piezas": [], "hallazgos_r9": [],
               "exploratorias": [], "peticiones": []}
        try:
            if isinstance(pre, Exception):
                raise pre
            senales, calcs = pre if pre is not None else self.senales_clase(clase, as_of, run_id)
        except Exception as e:  # modo degradado (PS2)
            out.update({"estado": "PARCIAL", "lagunas": [f"datos de mercado no disponibles: {e}"]})
            return out
        out["senales"], out["calc_ids"] = senales, calcs
        excluidos = self._sin_historia.get((clase, run_id)) or []
        if excluidos:
            out["estado"] = "PARCIAL"
            out["lagunas"].append(f"sin datos HT-01 en la ventana de 3 años hasta {pd.Timestamp(as_of).date()} para "
                                  f"{', '.join(excluidos)}: excluidos del cribado de este ciclo (PS2)")
        rechazadas = self._fichas_rechazadas.get((clase, run_id)) or []
        if rechazadas:
            out["estado"] = "PARCIAL"
            out["lagunas"].append(f"fichas del Motor rechazadas en este ciclo: {', '.join(rechazadas)} (sus señales faltan)")
        if not senales:
            out.update({"estado": "PARCIAL", "lagunas": ["sin datos HT-01 para el universo de la clase (PS2)"]})
            return out
        universo = []
        for f in self._universo_clase(clase, run_id):
            if f["simbolo"] in senales:
                universo.append({"simbolo": f["simbolo"], "nombre": f["nombre"], "tipo_opcion": f["tipo_opcion"], "region": f["region"],
                                 "sector": f["sector"], "divisa": f["divisa"], "notas": f["notas"],
                                 "subtipo": f.get("subtipo", ""), "ambito_incluye": f.get("ambito_incluye", ""),
                                 "ambito_excluye": f.get("ambito_excluye", ""), "indicador": f.get("indicador", ""),
                                 "senales": {k: (round(v, 6) if isinstance(v, float) else v) for k, v in senales[f["simbolo"]].items() if k != "calc_ids"}})
        refs = self.referencias.para_clase(clase, as_of, self.modo)
        out["hallazgos_r9"] += refs["hallazgos_r9"]
        vig_msg = []
        for v in vigentes:
            vig_msg.append({"opp_id": v["opp_id"], "nombre": v.get("nombre"), "ambito": v.get("ambito"),
                            "indicador_seguimiento": v.get("indicador_seguimiento") or {"simbolo": simbolo_seguimiento(v)},
                            "tesis": v.get("tesis"), "invalidacion": v.get("invalidacion"),
                            "invalidacion_cuantitativa": self._umbrales_vista(v.get("invalidacion_cuantitativa") or []),
                            "invalidacion_activada": v["opp_id"] in gc0["invalidadas"]})
        fase = "CRIBADO_E_INVESTIGACION" if nivel in ("N2", "N3") else "REVISION_VIGENTES"
        rot = []
        if fase == "REVISION_VIGENTES":
            vistos = {simbolo_seguimiento(v) for v in vigentes}
            rot = sorted([u["simbolo"] for u in universo if u["simbolo"] not in vistos],
                         key=lambda s: hashlib.sha256(f"{as_of.date()}{s}".encode()).hexdigest())[:2]
            if not vigentes and not rot:
                out["regimen"] = "Sin cambios materiales; sin opciones vigentes que revisar."
                return out
        msg = {"clase": clase, "tipo_activo": clase, "fase": fase, "nivel": nivel, "presupuesto": {"uc": presupuesto.asignado.get(clase)},
               "opciones_vigentes": vig_msg, "lecciones": [l["id"] for l in self.evaluador.lecciones_vigentes(as_of, clase)],
               "delta_gc0": {k: gc0[k] for k in ("cambio_material", "motivos")},
               "foco": {k: alcance.get(k) for k in ("regiones", "tematicas", "activos_concretos", "pregunta") if alcance.get(k)} or None,
               "universo": universo if fase == "CRIBADO_E_INVESTIGACION" else [u for u in universo if u["simbolo"] in rot or u["simbolo"] in {simbolo_seguimiento(v) for v in vigentes}],
               "rotacion_exploratoria": rot, "calculos_disponibles": calcs, "referencias_disponibles": refs["referencias"],
               "horizontes_aplicables_clase": {h: aplicabilidad(self.cfg, clase, h) for h in HORIZONTES},
               "horizontes_interes": hz_interes, "max_candidatas": sc.get("max_candidatas", 8), "max_finalistas": sc.get("max_finalistas", 5),
               "umbral_senal_gc1": sc.get("umbral_senal_gc1", 0.75), "fecha_limite_informacion": str(as_of.date()) if self.modo == "backtest" else None}
        instr = INSTR[fase].format(max_cand=sc.get("max_candidatas", 8), max_fin=sc.get("max_finalistas", 5),
                                   max_pet=sc.get("peticiones_conocimiento_por_clase", 1))
        pr = self.cfg.get("presupuesto_uc", {}).get("reparto_fases", {})
        self.mensajeria.crear("CT-06", "AG-02", agente, msg, run_id=run_id, presupuesto={"uc": presupuesto.asignado.get(clase)})
        r = self._invocar(agente, "CT-06", msg, "INFORME_CLASE" if fase == "CRIBADO_E_INVESTIGACION" else "REVISION_VIGENTES",
                          instr, as_of, run_id, clase, "cribado", presupuesto)
        if r is None or r.datos is None:
            out["estado"] = "PARCIAL"
            out["lagunas"].append("informe de clase no disponible (presupuesto o salida no conforme): alcance reducido declarado")
            out["revision_vigentes"] = [{"opp_id": v["opp_id"], "invalidacion_activada": v["opp_id"] in gc0["invalidadas"],
                                         "recomendacion": "CERRAR" if v["opp_id"] in gc0["invalidadas"] else "MANTENER"} for v in vigentes]
            return out
        d = r.datos
        out["regimen"] = (d.get("regimen_clase") or {}).get("diagnostico", "")
        out["revision_vigentes"] = d.get("revision_vigentes", [])
        for rv in out["revision_vigentes"]:   # la invalidación determinista prevalece (R23)
            if rv.get("opp_id") in gc0["invalidadas"]:
                rv["invalidacion_activada"], rv["recomendacion"] = True, "CERRAR"
        out["cribado"] = d.get("cribado", [])
        out["descartadas"] = d.get("descartadas_relevantes", [])
        out["lagunas"] += d.get("lagunas", [])
        estado_agente = d.get("estado", "COMPLETO") if d.get("estado") in ("COMPLETO", "PARCIAL") else "COMPLETO"
        out["estado"] = "PARCIAL" if out["estado"] == "PARCIAL" else estado_agente   # una laguna previa no se borra
        simbolos_clase = set(senales)
        fins = d.get("finalistas", []) if fase == "CRIBADO_E_INVESTIGACION" else []
        for f in d.get("exploratorias", []) if fase == "REVISION_VIGENTES" else []:
            if simbolo_seguimiento(f) in simbolos_clase:
                out["exploratorias"].append(f)
        vistos = set()
        for f in fins:
            sym = simbolo_seguimiento(f)
            if sym not in simbolos_clase:
                out["descartadas"].append({"nombre": f.get("nombre"), "motivo": f"indicador de seguimiento «{sym}» fuera del universo del tipo de activo (PS3)"})
                continue
            if sym in vistos:
                continue
            vistos.add(sym)
            f = copy.deepcopy(f)
            f["clase"], f["tipo_activo"], f["proxy"] = clase, clase, sym
            ind = dict(f.get("indicador_seguimiento") or {})
            ind.update({"simbolo": sym, "nombre": ind.get("nombre") or f.get("nombre") or sym})
            f["indicador_seguimiento"] = ind
            f["invalidacion_cuantitativa"] = self._umbrales_reales(f.get("invalidacion_cuantitativa") or [])
            f["horizontes_aplicables"] = [h for h in f.get("horizontes_aplicables", []) if aplicabilidad(self.cfg, clase, h) != "NO"]
            f["senales"] = senales.get(sym, {})
            out["finalistas"].append(f)
        # CT-07 / CT-08: peticiones de conocimiento (máximo configurado, valor de la información)
        maxp = int(sc.get("peticiones_conocimiento_por_clase", 1))
        for f in out["finalistas"]:
            for pet in (f.get("peticiones_conocimiento") or []):
                if len(out["peticiones"]) >= maxp:
                    break
                out["peticiones"].append(self._peticion_conocimiento(clase, f, pet, refs["referencias"], as_of, run_id, presupuesto))
        # Piezas de evidencia (CT-11): afirmaciones del Analista + dato HT-01/CALC de la señal (fuente primaria)
        for i, f in enumerate(out["finalistas"]):
            s = f["senales"]
            f["_piezas"] = []
            for a in f.get("afirmaciones", []):
                f["_piezas"].append({"afirmacion": a["afirmacion"], "fuente": a["fuente"], "direccion": a["direccion"],
                                     "extracto": a.get("extracto") or a["afirmacion"][:160], "origen": agente})
            if s.get("momentum_12_1") is not None:
                f["_piezas"].append({"afirmacion": f"Momentum 12-1 de {f['proxy']}: {s['momentum_12_1']:+.2%} (percentil {s.get('pct_momentum_clase', 0):.0%} de la clase) a {as_of.date()}",
                                     "fuente": f"HT-01:{f['proxy']}", "calc": s.get("calc_ids", [None])[0],
                                     "direccion": "favorable" if s["momentum_12_1"] > 0 else "contraria", "extracto": "serie de cierres HT-01",
                                     "origen": "AG-13", "tipo_afirmacion": "DATO"})
            for pr_ in out["peticiones"]:
                if pr_ and pr_.get("para") == f["proxy"]:
                    f["_piezas"] += pr_.get("piezas", [])
        # GC2 (E provisional ≥ 50, mecanismo y exposición con datos) y GC3 (top por RK provisional)
        for f in out["finalistas"]:
            ev = ht03.evaluar_opcion({"opp_id": "PROV", "clase": clase, "dimensiones": f["dimensiones"],
                                      "segunda_pasada": f.get("segunda_pasada") or {}, "saturacion_narrativa": f.get("saturacion_narrativa", False),
                                      "puertas": {}}, self.params_ht03)
            f["_prov"] = ev["puntuaciones"]
            f["_gc2"] = (not ev["errores"]) and ev["puntuaciones"].get("E", 0) >= self.params_ht03["umbrales"]["GC2_E"] \
                and bool(f.get("mecanismo")) and bool(f["senales"])
        pasan = sorted([f for f in out["finalistas"] if f["_gc2"]], key=lambda f: (-f["_prov"].get("RK", 0), f["proxy"]))
        for k, f in enumerate(pasan):
            f["_gc3"] = k < int(sc.get("max_finalistas", 5))
        for f in out["finalistas"]:
            f.setdefault("_gc3", False)
        finales = [f for f in out["finalistas"] if f["_gc3"]]
        # F3 · Prospectiva (CT-12) y F4 · Refutación (CT-13), por lotes de la clase
        if finales:
            self._prospectiva(clase, finales, as_of, run_id, presupuesto, hz_interes)
            if nivel in ("N2", "N3"):
                self._refutacion(clase, finales, nivel, as_of, run_id, presupuesto)
        return out

    def _umbrales_vista(self, inv: list[dict]) -> list[dict]:
        if not self.anon:
            return inv
        return [{**i, "umbral": round(float(i["umbral"]) * self.anon.factores.get(i["simbolo"], 1.0), 6)} for i in inv]

    def _umbrales_reales(self, inv: list[dict]) -> list[dict]:
        out = []
        for i in inv:
            try:
                u = float(i["umbral"])
            except (KeyError, TypeError, ValueError):
                continue
            if self.anon:
                u = u / self.anon.factores.get(i["simbolo"], 1.0)
            out.append({"simbolo": i["simbolo"], "umbral": round(u, 6), "direccion": i.get("direccion", "por_debajo")})
        return out

    def _peticion_conocimiento(self, clase, f, pet, refs, as_of, run_id, presupuesto) -> dict | None:
        tipo = pet.get("tipo", "CT-08")
        agente = "AG-16" if tipo == "CT-07" else "AG-14"
        arch = ("F9",) if agente == "AG-16" else ("F7",)
        cand = self.referencias.para_clase(clase, as_of, self.modo, max_n=8, archivos=arch)
        msg = {"pregunta": pet.get("pregunta", ""), "objetivo": pet.get("objetivo", "confirmar"), "clase": clase,
               "horizonte": (f.get("horizontes_aplicables") or ["H3"])[0], "profundidad": "minima", "max_fuentes": 3,
               "fecha_limite_informacion": str(as_of.date()), "referencias_candidatas": cand["referencias"],
               "para": f["proxy"]}
        self.mensajeria.crear(tipo, AGENTE_CLASE[clase], agente, msg, run_id=run_id, presupuesto={"uc": 1})
        r = self._invocar(agente, tipo, msg, "BUSQUEDA",
                          "Selecciona entre las referencias candidatas (o, en modo vivo, busca) las que confirman o refutan la "
                          "pregunta; devuelve REF- con una afirmación y su dirección, síntesis, contradicciones y lagunas.",
                          as_of, run_id, clase, "investigacion", presupuesto, permitir_web=True)
        if not r or not r.datos:
            return {"para": f["proxy"], "piezas": [], "estado": "SIN_RESULTADO"}
        datos, hall = sanear_estructura(r.datos, f"{agente}:{run_id}")
        piezas = []
        for ref in datos.get("referencias", [])[:3]:
            if not self.referencias.por_id(str(ref.get("ref_id", ""))) and self.modo == "backtest":
                continue   # en backtest solo referencias registradas y anteriores a as_of
            piezas.append({"afirmacion": ref.get("afirmacion") or datos.get("sintesis", "")[:200], "fuente": ref["ref_id"],
                           "direccion": ref.get("direccion", "neutra"), "extracto": (ref.get("extracto") or ref.get("motivo") or "")[:160],
                           "origen": agente, "incidencia": bool(hall)})
        return {"para": f["proxy"], "piezas": piezas, "hallazgos_r9": hall, "estado": "COMPLETO"}

    def _prospectiva(self, clase, finales, as_of, run_id, presupuesto, hz_interes) -> None:
        certs = {(c["celda"]["clase"], c["celda"]["horizonte"]) for c in self.evaluador.certificados_vigentes(as_of)}
        encargos = []
        for f in finales:
            ref = self._referencia(clase, f["proxy"])
            tipo_p = "DIRECCIONAL" if ref is None or ref == f["proxy"] else "RELATIVO"
            hs = [h for h in f.get("horizontes_aplicables", []) if h in hz_interes]
            f["_tipo_pronostico"], f["_referencia"] = tipo_p, (None if tipo_p == "DIRECCIONAL" else ref)
            encargos.append({"ref": f["proxy"], "opp_id": f.get("opp_id"), "tesis": f["tesis"], "proxy": f["proxy"],
                             "referencia_indice": f["_referencia"], "tipo_pronostico": tipo_p, "horizontes": hs,
                             "datos": {k: v for k, v in f["senales"].items() if k != "calc_ids"},
                             "catalizadores_conocidos": f.get("catalizadores", []), "invalidacion_propuesta": f.get("invalidacion", []),
                             "certificado_r13": {h: (clase, h) in certs for h in hs}})
        msg = {"encargos": encargos, "fecha_limite_informacion": str(as_of.date())}
        self.mensajeria.crear("CT-12", "AG-02", "AG-10", msg, run_id=run_id, presupuesto={"uc": presupuesto.asignado.get(clase)})
        r = self._invocar("AG-10", "CT-12", msg, "PROSPECTIVA",
                          "Para cada encargo, construye escenarios por horizonte y propone un pronóstico verificable por horizonte "
                          "pedido: vista (alcista/bajista para DIRECCIONAL; relativa_favorable/relativa_desfavorable para "
                          "RELATIVO frente a la referencia), probabilidad interna (0,05–0,95), afirmación inequívoca y escenario.",
                          as_of, run_id, clase, "prospectiva", presupuesto)
        res = {x["ref"]: x for x in (r.datos or {}).get("resultados", [])} if r and r.datos else {}
        for f in finales:
            f["_prospectiva"] = res.get(f["proxy"])

    def _refutacion(self, clase, finales, nivel, as_of, run_id, presupuesto) -> None:
        peticiones = [{"ref": f["proxy"], "opp_id": f.get("opp_id"), "tesis": f["tesis"], "mecanismo": f.get("mecanismo"),
                       "evidencias_clave": [p["afirmacion"] for p in f["_piezas"]][:6], "calculos": f["senales"].get("calc_ids", []),
                       "prospectiva": (f.get("_prospectiva") or {}).get("pronosticos", []), "premortem": f.get("premortem"),
                       "dimensiones": f["dimensiones"]} for f in finales]
        msg = {"peticiones": peticiones, "nivel": nivel}
        self.mensajeria.crear("CT-13", "AG-02", "AG-11", msg, run_id=run_id, presupuesto={"uc": presupuesto.asignado.get(clase)})
        r = self._invocar("AG-11", "CT-13", msg, "REFUTACION",
                          "Refuta de forma independiente cada tesis: objeciones graduadas (fuerte, moderada, débil) con id "
                          "OBJ-<ref>-nn, tipo, argumento, evidencia y qué la resolvería; veredicto global por tesis.",
                          as_of, run_id, clase, "refutacion", presupuesto)
        if not r or not r.datos:
            for f in finales:
                f["_refutacion"] = None
            return
        res = {x["ref"]: x for x in r.datos.get("resultados", [])}
        pendientes = []
        for f in finales:
            x = res.get(f["proxy"])
            f["_refutacion"] = x
            f["_objeciones"] = []
            for o in (x or {}).get("objeciones", []):
                f["_objeciones"].append({"objecion_id": o["id"], "tipo": o.get("tipo"), "fuerza": o["fuerza"], "resumen": o["argumento"],
                                         "que_la_resolveria": o.get("que_la_resolveria"), "respuesta": None, "resuelta": False})
                if o["fuerza"] in ("fuerte", "moderada"):
                    pendientes.append({"ref": f["proxy"], "objecion_id": o["id"], "fuerza": o["fuerza"], "argumento": o["argumento"],
                                       "que_la_resolveria": o.get("que_la_resolveria"), "dimensiones_E": f["dimensiones"].get("E")})
        if pendientes:
            agente = AGENTE_CLASE[clase]
            msg2 = {"clase": clase, "fase": "RESPUESTA_OBJECIONES", "nivel": nivel, "opciones_vigentes": [], "lecciones": [],
                    "objeciones": pendientes}
            self.mensajeria.crear("CT-06", "AG-02", agente, msg2, run_id=run_id, presupuesto={"uc": presupuesto.asignado.get(clase)})
            r2 = self._invocar(agente, "CT-06", msg2, "RESPUESTA_OBJECIONES", INSTR["RESPUESTA_OBJECIONES"], as_of, run_id, clase,
                               "respuesta_objeciones", presupuesto)
            resp = {x["objecion_id"]: x for x in (r2.datos or {}).get("respuestas", [])} if r2 and r2.datos else {}
            for f in finales:
                for o in f.get("_objeciones", []):
                    x = resp.get(o["objecion_id"])
                    if x and (x.get("respuesta") or "").strip():
                        o["respuesta"] = x["respuesta"]
                        o["resuelta"] = bool(x.get("resuelta")) if o["fuerza"] == "fuerte" else True

    # ====================================================================================
    # Evidencia (F2), clústeres y selección
    # ====================================================================================
    def _registrar_evidencia_clase(self, an: dict, as_of, run_id: str) -> None:
        clase = an["clase"]
        self._registrar_r9(an.get("hallazgos_r9", []), run_id)
        for p in an.get("peticiones", []):
            if p:
                self._registrar_r9(p.get("hallazgos_r9", []), run_id)
        finales = [f for f in an["finalistas"]]
        if not finales:
            return
        # Curación LLM (N2/N3): tipo de afirmación, confianza y alertas; la deduplicación y las raíces son deterministas
        clasif = {}
        if an["nivel"] in ("N2", "N3"):
            piezas = [{"indice": i, **{k: p.get(k) for k in ("afirmacion", "fuente", "direccion", "extracto")}}
                      for i, p in enumerate(pz for f in finales for pz in f["_piezas"])]
            if piezas:
                msg = {"piezas": piezas, "clase": clase}
                self.mensajeria.crear("CT-11", AGENTE_CLASE[clase], "AG-12", msg, run_id=run_id, presupuesto={"uc": 1})
                r = self._invocar("AG-12", "CT-11", msg, "CURACION",
                                  "Clasifica cada pieza (tipo de afirmación, nivel de confianza) y señala alertas (cuarentena, "
                                  "posible coordinación, fecha dudosa). La deduplicación por hash y el recuento de raíces los hace el ejecutor.",
                                  as_of, run_id, clase, "investigacion")
                if r and r.datos:
                    clasif = {x["indice"]: x for x in r.datos.get("piezas", [])}
        i = 0
        clm_por_texto = {normalizar(c.get("afirmacion", "")): c for c in self.almacen.estado("F2", as_of, clave="clm_id").values()
                         if c.get("tipo_entrada") == "CLM"}
        evd_por_hash = {e.get("hash_contenido"): e for e in self.almacen.estado("F2", as_of, clave="evd_id").values()
                        if e.get("tipo_entrada") == "EVD"}
        for f in finales:
            f["_evidencias"], f["_raices"], f["_manipulacion"] = [], {}, False
            for p in f["_piezas"]:
                cl = clasif.get(i, {})
                i += 1
                fuente = p["fuente"]
                ref = self.referencias.por_id(fuente) if fuente.startswith("REF-") else None
                if fuente.startswith("HT-01:") or fuente.startswith("CALC-"):
                    nivel_f, tipo_f, raiz = "A", "PRIMARIA", fuente if fuente.startswith("HT-01:") else f"HT-01:{f['proxy']}"
                elif ref:
                    nivel_f, tipo_f, raiz = ref["nivel"] or "C", "PRIMARIA" if "primaria" in (ref.get("tipologia") or "").lower() else "SECUNDARIA", fuente
                else:
                    nivel_f, tipo_f, raiz = "C", "SECUNDARIA", fuente   # «C provisional»
                h = clave_hash(normalizar(p.get("extracto", "")), fuente)[:32]
                clave_clm = normalizar(p["afirmacion"])
                clm = clm_por_texto.get(clave_clm)
                if clm is None:
                    clm = {"tipo_entrada": "CLM", "clm_id": self.almacen.nuevo_id("CLM"), "afirmacion": p["afirmacion"],
                           "tipo_afirmacion": cl.get("tipo_afirmacion") or p.get("tipo_afirmacion") or "ANALISIS", "clase": clase,
                           "evidencias": [], "raices_independientes": 0, "ps1_cumple": False,
                           "nivel_confianza": cl.get("nivel_confianza", "probable"),
                           "utilizada_por": [{"objeto": f["proxy"], "papel": "tesis"}], "historial": [{"fecha": str(as_of.date()), "cambio": "alta", "run_id": run_id}]}
                    clm_por_texto[clave_clm] = clm
                dup = evd_por_hash.get(h)
                if dup is None:
                    evd = {"tipo_entrada": "EVD", "evd_id": self.almacen.nuevo_id("EVD"), "clm_ids": [clm["clm_id"]],
                           "direccion": p["direccion"].upper(), "ref_id": fuente, "nivel_fuente": nivel_f, "tipo_fuente": tipo_f,
                           "grado_independencia": "RAIZ", "raiz_evd_id": None, "url_canonica": None, "identificador_documental": fuente,
                           "extracto": p.get("extracto", "")[:200], "hash_contenido": h, "estado_verificacion": "VERIFICADA" if nivel_f == "A" else "PENDIENTE",
                           "limitaciones": "dato de mercado HT-01" if fuente.startswith(("HT-01", "CALC")) else "fuente registrada; extracto mínimo",
                           "fecha_publicacion": str(as_of.date()), "fecha_recuperacion": self.reloj.ahora(), "conocible_desde": str(as_of.date()),
                           "alertas": cl.get("alertas", []), "_raiz": raiz}
                    if p.get("incidencia"):
                        evd["incidencia_manipulacion"] = {"tipo": "INSTRUCCION_INCRUSTADA", "detalle": "neutralizada por el ejecutor"}
                        f["_manipulacion"] = True
                    self.almacen.escribir("F2", "AG-12", evd)
                    evd_por_hash[h] = evd
                else:
                    evd = dup
                if evd["evd_id"] not in clm["evidencias"]:
                    clm["evidencias"].append(evd["evd_id"])
                # PS1 exige corroborar las afirmaciones centrales del Analista (9.3): la pieza de momentum que añade el
                # ejecutor es contexto y su «dirección» no depende de la tesis, así que no cuenta como raíz.
                if evd["direccion"] == "FAVORABLE" and p.get("origen") != "AG-13":
                    f["_raices"][evd.get("_raiz", fuente)] = (evd["nivel_fuente"], evd["tipo_fuente"])
                if clm["clm_id"] not in f["_evidencias"]:
                    f["_evidencias"].append(clm["clm_id"])
            raices = f["_raices"]
            f["_ps1"] = sum(1 for n, _ in raices.values() if n in ("A", "B")) >= 2 or any(n == "A" and t == "PRIMARIA" for n, t in raices.values())
            for cid in f["_evidencias"]:
                clm = next(c for c in clm_por_texto.values() if c["clm_id"] == cid)
                clm["raices_independientes"] = len(raices)
                clm["ps1_cumple"] = f["_ps1"]
        escritos = set()
        for f in finales:
            for cid in f["_evidencias"]:
                if cid in escritos:
                    continue
                clm = next(c for c in clm_por_texto.values() if c["clm_id"] == cid)
                self.almacen.escribir("F2", "AG-12", {k: v for k, v in clm.items() if not k.startswith("_")})
                escritos.add(cid)

    def _clusteres(self, analisis: dict, as_of, run_id: str) -> dict:
        proxies = sorted({f["proxy"] for an in analisis.values() for f in an["finalistas"] if f.get("_gc3")}
                         | {simbolo_seguimiento(v) for c in analisis for v in self.vigentes(as_of, c) if simbolo_seguimiento(v)})
        if not proxies:
            return {"asignacion": {}, "calc_id": None, "n_efectivo": 0}
        ini = str((pd.Timestamp(as_of) - pd.DateOffset(years=2, days=14)).date())
        r = self.motor.servir({"operacion": "ML-CLUS-001", "plan": "PLAN_MIN", "datos": [{"serie": p, "inicio": ini} for p in proxies],
                               "parametros": {"umbral_rho": float((self.cfg.get("clusteres") or {}).get("umbral_rho", 0.7)),
                                              "ventana_semanas": int((self.cfg.get("clusteres") or {}).get("ventana_semanas", 104))}, "fecha_corte": str(pd.Timestamp(as_of).date())},
                              "AG-02", run_id)
        if r["estado"] == "RECHAZADO":   # sin clústeres no se mide la concentración: se declara, no se calla (T-53, QA H-01)
            return {"asignacion": {p: i + 1 for i, p in enumerate(proxies)}, "calc_id": None, "n_efectivo": len(proxies),
                    "rechazo": str(r.get("detalle") or r.get("motivo_rechazo") or "ML-CLUS-001 rechazado")}
        return {"asignacion": r["resultado"]["asignacion"], "calc_id": r["calc_id"], "n_efectivo": r["resultado"]["n_efectivo"]}

    def _opp_id(self, clase: str, proxy: str, tipo_opcion: str, as_of) -> tuple[str, dict | None]:
        for o in self.almacen.estado("F3", as_of).values():
            if o.get("clase") == clase and simbolo_seguimiento(o) == proxy and o.get("tipo_opcion") == tipo_opcion \
                    and o.get("estado") not in ("CERRADA", "DESCARTADA"):
                return o["opp_id"], o
        return self.almacen.nuevo_id("OPP"), None

    def _puertas(self, f: dict, nivel: str, as_of, horizontes_ok: list[str]) -> dict[str, bool]:
        fecha_dato = f["senales"].get("fecha_dato")
        lim = {**ANTIGUEDAD_PS2, **(self.cfg.get("ps2_antiguedad_maxima_dias") or {})}   # Anexo A (PS2)
        if fecha_dato:
            edad = (pd.Timestamp(as_of) - pd.Timestamp(fecha_dato)).days
            # H1 cuenta sesiones hábiles (el dato del viernes vale el lunes); el resto, días naturales (Anexo A)
            sesiones = _sesiones_entre(fecha_dato, as_of, self.cfg.get("ps2_festivos") or {})
        else:
            edad = sesiones = 999   # sin fecha del dato no se supera PS2 (falla cerrado)
        ps2 = bool(horizontes_ok) and all((sesiones if h == "H1" else edad) <= lim[h] for h in horizontes_ok)
        refut = f.get("_refutacion")
        fuertes_abiertas = sum(1 for o in f.get("_objeciones", []) if o["fuerza"] == "fuerte" and not o["resuelta"])
        moderadas_sin = sum(1 for o in f.get("_objeciones", []) if o["fuerza"] == "moderada" and not o.get("respuesta"))
        ps5 = (refut is not None) if nivel in ("N2", "N3") else bool(f.get("premortem"))
        return {"G1": bool(f.get("_ps1")), "G2": ps5 and fuertes_abiertas == 0 and moderadas_sin == 0, "G3": True,
                "G4": bool(f.get("lo_que_no_sabemos")) and bool(f.get("invalidacion")) and bool(horizontes_ok),
                "PS1": bool(f.get("_ps1")), "PS2": ps2,
                # PS3 (V5.0): invertibilidad del ámbito e indicador de seguimiento medible
                "PS3": (f.get("invertibilidad") or {}).get("universo_suficiente") is True and bool(f.get("indicador_seguimiento"))
                and bool(f["senales"].get("fecha_dato")),
                "PS4": bool(f["senales"].get("riesgo_1a5")), "PS5": ps5, "PS6": not f.get("discrepancia_material", False),
                "PS7": not f.get("_manipulacion", False), "PS8": True}

    def _horizontes(self, f: dict, clase: str, hz_interes: list[str]) -> dict[str, dict]:
        """Pronósticos por horizonte a partir de la prospectiva, filtrados por la tabla 8.3 y F10."""
        out = {}
        pros = f.get("_prospectiva") or {}
        for p in pros.get("pronosticos", []):
            h = p["horizonte"]
            ap = aplicabilidad(self.cfg, clase, h)
            if h not in hz_interes or h not in f.get("horizontes_aplicables", []) or ap == "NO" or h in out:
                continue
            if ap == "LIMITADO" and not f.get("catalizadores"):
                continue
            vista = p["vista"]
            if f["_tipo_pronostico"] == "RELATIVO":
                vista = {"alcista": "relativa_favorable", "bajista": "relativa_desfavorable"}.get(vista, vista)
            else:
                vista = {"relativa_favorable": "alcista", "relativa_desfavorable": "bajista"}.get(vista, vista)
            if vista == "lateral":
                continue
            prob = min(max(round(float(p["prob_interna"]) * 20) / 20, 0.05), 0.95)
            out[h] = {"vista": vista, "prob_interna": prob, "afirmacion": p["afirmacion"],
                      "escenario": p.get("escenario_asociado", "BASE"), "metodo": p.get("metodo") or "PROSPECTIVA-AG10"}
        return out

    def _seleccionar(self, clase: str, an: dict, clusteres: dict, as_of, run_id: str, hz_interes: list[str]) -> dict:
        nivel = an["nivel"]
        candidatos, entradas_ht03 = [], []
        cerradas = []
        vig = {v["opp_id"]: v for v in self.vigentes(as_of, clase)}
        rev = {r.get("opp_id"): r for r in an.get("revision_vigentes", [])}
        nuevos_proxies = {f["proxy"] for f in an["finalistas"] if f.get("_gc3")}
        for oid, v in vig.items():
            r = rev.get(oid, {})
            if r.get("invalidacion_activada") or r.get("recomendacion") == "CERRAR":
                cerradas.append({"opp_id": oid, "motivo_cierre": "INVALIDACION" if r.get("invalidacion_activada") else "SUSTITUCION",
                                 "comentario": "Condición de invalidación cumplida" if r.get("invalidacion_activada") else "Cierre recomendado por el Analista de clase"})
        # Finalistas nuevas o reevaluadas
        for f in an["finalistas"]:
            if not f.get("_gc3"):
                continue
            oid, previa = self._opp_id(clase, f["proxy"], f["tipo_opcion"], as_of)
            if oid in [c["opp_id"] for c in cerradas]:
                oid, previa = self.almacen.nuevo_id("OPP"), None
            f["opp_id"], f["_previa"] = oid, previa
            f["_vigente"] = oid in vig
            f["_hz"] = self._horizontes(f, clase, hz_interes)
            candidatos.append(f)
        # Vigentes mantenidas sin reevaluación (arrastre verificado o N2 sin repetir la ficha)
        for oid, v in vig.items():
            if oid in [c["opp_id"] for c in cerradas] or simbolo_seguimiento(v) in nuevos_proxies:
                continue
            f = self._desde_f3(v, an, as_of)
            if f is None:
                cerradas.append({"opp_id": oid, "motivo_cierre": "SUSTITUCION", "comentario": "Sin datos para reconfirmar (PS2)"})
                continue
            candidatos.append(f)
        # Objeciones → dimensión E «objeciones_respondidas» (determinista)
        for f in candidatos:
            objs = [o for o in f.get("_objeciones", []) if o["fuerza"] in ("fuerte", "moderada")]
            if objs and not f.get("_arrastre"):
                ok = sum(1 for o in objs if o.get("respuesta") and (o["fuerza"] != "fuerte" or o["resuelta"]))
                f["dimensiones"] = copy.deepcopy(f["dimensiones"])
                f["dimensiones"]["E"]["objeciones_respondidas"] = int(round(10 * ok / len(objs))) * 10
            if not f.get("_ps1") and isinstance(f["dimensiones"].get("E"), dict):
                f["dimensiones"]["E"]["calidad_raices"] = min(f["dimensiones"]["E"].get("calidad_raices", 0) if isinstance(f["dimensiones"]["E"].get("calidad_raices"), int) else 0, 50)
        for f in candidatos:
            f["_cluster"] = f"CL-{clusteres['asignacion'].get(f['proxy'], 99)}"
            f["_puertas"] = self._puertas(f, nivel if not f.get("_arrastre") else "N1", as_of, list(f["_hz"]))
            entradas_ht03.append({"opp_id": f["opp_id"], "clase": clase, "cluster": f["_cluster"], "vigente": f["_vigente"],
                                  "riesgo_cola": f["senales"].get("riesgo_1a5"), "saturacion_narrativa": bool(f.get("saturacion_narrativa")),
                                  "dimensiones": f["dimensiones"], "segunda_pasada": f.get("segunda_pasada") or {},
                                  "anterior": (f.get("_previa") or {}).get("puntuaciones_totales") or {}, "puertas": f["_puertas"],
                                  "objeciones_fuertes_abiertas": sum(1 for o in f.get("_objeciones", []) if o["fuerza"] == "fuerte" and not o["resuelta"])})
        evaluadas = [ht03.evaluar_opcion(e, self.params_ht03) for e in entradas_ht03]
        n_cand = len(an.get("cribado", [])) or len(an["finalistas"]) or len(candidatos)
        sel = ht03.seleccionar_top3(evaluadas, self.params_ht03, max(n_cand, len(evaluadas)))
        sombra = None
        aju = self.evaluador.ajuste_en_sombra(as_of)
        if aju and evaluadas:
            ps = ht03.fusionar_parametros({"pesos_rk": aju["a"]})
            ev_s = [ht03.evaluar_opcion(e, ps) for e in entradas_ht03]
            sel_s = ht03.seleccionar_top3(ev_s, ps, max(n_cand, len(ev_s)))
            sombra = {"aju_id": aju["id"], "top3_sombra": [t["opp_id"] for t in sel_s["top3"]],
                      "cambios": len({t["opp_id"] for t in sel_s["top3"]} ^ {t["opp_id"] for t in sel["top3"]})}
        for f, e in zip(candidatos, evaluadas):
            f["_ht03"] = e
        return {"candidatos": candidatos, "evaluadas": evaluadas, "seleccion": sel, "cerradas": cerradas, "sombra": sombra,
                "entradas_ht03": entradas_ht03, "n_cand": max(n_cand, len(evaluadas))}

    def _deduplicar_entre_tipos(self, seleccion: dict[str, dict], max_pasadas: int = 4) -> list[dict]:
        """Regla 5 de 2.6 (y C16 de HT-09): si dos top-3 de tipos distintos comparten nombre o ámbito normalizados, se
        conserva la opción de mayor RK (a igual RK, la del tipo anterior en la tabla 2.6) y la otra deja de ser elegible
        en su tipo con el motivo DUPLICADA_EN_OTRO_TIPO; ese tipo vuelve a seleccionar su top-3 con HT-03."""
        quitadas: list[dict] = []
        for _ in range(max_pasadas):
            sel = [(c, t) for c in seleccion for t in seleccion[c]["seleccion"]["top3"]]
            sel.sort(key=lambda x: (-x[1]["RK"], CLASES.index(x[0]) if x[0] in CLASES else 99, x[1]["opp_id"]))
            vistos: dict[str, tuple[str, str]] = {}
            excluir: dict[str, dict[str, str]] = {}
            for c, t in sel:
                f = next(x for x in seleccion[c]["candidatos"] if x["opp_id"] == t["opp_id"])
                claves = {"nombre:" + ht09.normalizar_texto(f.get("nombre"))}
                ka = ht09.clave_ambito(f)
                if ka:
                    claves.add("ambito:" + ka)
                previo = next((vistos[k] for k in sorted(claves) if k in vistos and vistos[k][0] != c), None)
                if previo:
                    excluir.setdefault(c, {})[t["opp_id"]] = f"Duplicada de {previo[1]} ({previo[0]}): regla 5 de 2.6"
                else:
                    for k in claves:
                        vistos.setdefault(k, (c, t["opp_id"]))
            if not excluir:
                break
            for c, ids in excluir.items():
                s = seleccion[c]
                for e in s["evaluadas"]:
                    if e["opp_id"] in ids:
                        e["elegible"] = False
                        e["motivos_no_elegible"].append({"codigo": "DUPLICADA_EN_OTRO_TIPO", "detalle": ids[e["opp_id"]]})
                        quitadas.append({"clase": c, "opp_id": e["opp_id"], "motivo": ids[e["opp_id"]]})
                s["seleccion"] = ht03.seleccionar_top3(s["evaluadas"], self.params_ht03, s.get("n_cand") or len(s["evaluadas"]))
        return quitadas

    def _desde_f3(self, v: dict, an: dict, as_of) -> dict | None:
        """Reconstruye una opción vigente desde F3 para el arrastre verificado: datos frescos (PS2), mismas
        dimensiones (reconfirmación con HT-03) y pronósticos abiertos; los vencidos se reemiten (versión nueva)."""
        sym = simbolo_seguimiento(v)
        sen = (an.get("senales") or {}).get(sym)
        if not sen:
            try:
                fd, precio = self.proveedor.valor_en(sym, as_of)
                sen = {"fecha_dato": str(fd.date()), "precio": precio, "riesgo_1a5": v.get("riesgo_1a5")}
            except DatosNoDisponibles:
                return None
        f = {k: copy.deepcopy(v.get(k)) for k in ("nombre", "nombre_llano", "tipo_opcion", "subtipo", "tesis", "mecanismo", "valoracion",
                                                   "catalizadores", "riesgos", "invalidacion", "invalidacion_cuantitativa",
                                                   "horizontes_aplicables", "ambito", "indicador_seguimiento", "invertibilidad",
                                                   "ejemplos_ilustrativos", "criterios_seleccion_sugeridos", "metricas_clave",
                                                   "preguntas_para_B", "dimensiones", "segunda_pasada",
                                                   "saturacion_narrativa", "premortem", "lo_que_no_sabemos", "regiones", "liquidez")}
        f = {k: x for k, x in f.items() if x is not None}
        f.setdefault("indicador_seguimiento", {"nombre": v.get("nombre") or sym, "simbolo": sym})
        f.setdefault("invertibilidad", {"universo_suficiente": True, "nota": "Registro anterior a V5.0: invertibilidad no declarada"})
        f.update({"clase": v["clase"], "tipo_activo": v["clase"], "proxy": sym, "opp_id": v["opp_id"], "_previa": v, "_vigente": True, "_arrastre": True,
                  "senales": sen, "_ps1": v.get("ps1", True), "_evidencias": v.get("evidencias", []),
                  "_objeciones": v.get("objeciones_internas", []), "_refutacion": {"arrastre": True},
                  "_tipo_pronostico": v.get("tipo_pronostico", "RELATIVO"), "_referencia": v.get("referencia_indice"),
                  "tnd_id": v.get("tnd_id"), "afirmaciones": [], "_gc3": True})
        if not f.get("premortem"):
            f["premortem"] = "Arrastre verificado: pre-mortem del ciclo de alta vigente."
        hz = {}
        abiertos = {p["prg_id"]: p for p in self.almacen.estado("F4", as_of).values() if p.get("opp_id") == v["opp_id"]}
        for h, d in (v.get("horizontes_prg") or {}).items():
            p = abiertos.get(d.get("prg_id"))
            if p is None:
                continue
            prob = p["prob_interna"] if p.get("prob_interna") is not None else PROB_DE_BANDA.get(p.get("banda_verbal"))
            if prob is None:     # sin probabilidad ni banda reconocible no se inventa un 0,5: el horizonte no se arrastra
                continue
            base = {"vista": d["vista"], "prob_interna": prob, "afirmacion": p["afirmacion"],
                    "escenario": p.get("escenario_asociado", "BASE"), "metodo": p.get("metodo")}
            if p.get("estado") == "ABIERTO":
                hz[h] = {**base, "prg_existente": p["prg_id"]}
            else:
                hz[h] = {**base, "metodo": "ARRASTRE", "version_de": p["prg_id"]}
        f["_hz"] = hz
        return f

    # ====================================================================================
    # Integración, G3, redacción, congelación y registro
    # ====================================================================================
    def _integrar(self, seleccion, analisis, gc0, nivel, as_of, run_id, presupuesto) -> dict:
        resumen = {}
        for c, s in seleccion.items():
            por_id = {f["opp_id"]: f for f in s["candidatos"]}
            resumen[c] = {"nivel": nivel[c], "regimen": analisis[c].get("regimen"),
                          "top3": [{"opp_id": t["opp_id"], "nombre": por_id[t["opp_id"]].get("nombre"), "proxy": por_id[t["opp_id"]]["proxy"],
                                    "cluster": t.get("cluster"), "RK": t["RK"]} for t in s["seleccion"]["top3"]],
                          "cerradas": s["cerradas"], "lagunas": analisis[c].get("lagunas", [])[:3]}
        anterior = [r for r in self.almacen.leer("F5", as_of) if r.get("tipo_entrada") == "RUN"]
        msg = {"tipo": "INTEGRACION", "alcance": {"clases": list(seleccion)}, "nivel_por_clase": nivel,
               "presupuesto_por_clase": presupuesto.asignado, "memoria": {"run_anterior": anterior[-1]["id"] if anterior else None,
               "top3_anterior": anterior[-1].get("top3_por_clase") if anterior else None},
               "delta_gc0": {c: g["motivos"] for c, g in gc0.items()}, "fecha_objetivo": str(pd.Timestamp(as_of).date()),
               "insumos_integracion": resumen}
        r = self._invocar("AG-02", "CT-05", msg, "INTEGRACION",
                          "Integra los informes de clase: régimen macro común, factores dominantes (qué opciones dependen del mismo "
                          "factor), lectura del conjunto, cambios frente al ciclo anterior, preguntas sugeridas para el Broker y "
                          "limitaciones. No cambies la selección: la ha hecho HT-03.", as_of, run_id, None, "integracion", presupuesto, bolsa="COMUN")
        if r and r.datos:
            return r.datos
        return {"regimen_macro": "Régimen no integrado por el Analizador (salida no disponible); ver regímenes por clase.",
                "factores_dominantes": [], "lectura_conjunto": "Integración no disponible: alcance reducido declarado.",
                "preguntas_sugeridas": [], "limitaciones": ["integración del Analizador no disponible"], "cambios_vs_anterior": ""}

    def _validar_g3(self, paquete: dict, extras: dict, as_of, run_id: str) -> tuple[dict, dict]:
        intento = 0
        while True:
            intento += 1
            res = sint.ht09_validar(self, paquete, extras, None)
            dictamen = res["dictamen"]
            advert = [c for c in res["comprobaciones"] if c["resultado"] == "ADVERTENCIA"
                      and not (c["id"] == "C12" and all("no se ha facilitado" in i["detalle"] for i in c["incidencias"]))]
            bloq = [c for c in res["comprobaciones"] if c["resultado"] == "BLOQUEO"]
            efectivo = "BLOQUEADO" if bloq else ("APTO_CON_ADVERTENCIAS" if advert else "APTO")
            g3v = {"tipo_entrada": "G3V", "id": f"G3V-{run_id[4:]}-{intento:02d}", "run_id": run_id, "tipo_control": "SINCRONO_DETERMINISTA",
                   "fase": "F6", "dictamen_ht09": dictamen, "dictamen_efectivo": efectivo,
                   "comprobaciones": [{"id": c["id"], "resultado": c["resultado"], "n_incidencias": len(c["incidencias"]),
                                       "detalle": [i["detalle"] for i in c["incidencias"]][:5]} for c in res["comprobaciones"]]}
            if efectivo == "APTO":
                self.almacen.escribir("HA", "AG-18", g3v)
                return paquete, {"dictamen": "APTO", "advertencias": [], "intentos": intento, "g3v_id": g3v["id"]}
            # CT-14: el Orquestador dictamina con prioridad máxima
            msg = {"run_id": run_id, "paquete_sintesis": {"resumen": {c: [o["opp_id"] for o in paquete["clases"][c]["opciones"]] for c in paquete["clases"]}},
                   "resultado_ht09": {"dictamen": efectivo, "bloqueos": [{"id": c["id"], "incidencias": c["incidencias"][:5]} for c in bloq],
                                      "advertencias": [{"id": c["id"], "incidencias": c["incidencias"][:5]} for c in advert]}}
            self.mensajeria.crear("CT-14", "AG-02", "AG-18", msg, run_id=run_id, presupuesto={"uc": 1})
            r = self._invocar("AG-18", "CT-14", msg, "DICTAMEN_G3",
                              "Dictamina la validación G3: APTO_CON_ADVERTENCIAS solo si no hay bloqueos; si los hay, BLOQUEADO con "
                              "condiciones para quedar APTO. Nunca APTO por defecto.", as_of, run_id)
            dict_orq = (r.datos or {}).get("dictamen") if r and r.datos else None
            if bloq:
                dict_orq = "BLOQUEADO"     # el Orquestador no puede convertir un bloqueo en apto (R16, R17)
            g3v["excepcion"] = {"recibida": True, "dictamen_orquestador": dict_orq or ("BLOQUEADO" if bloq else "APTO_CON_ADVERTENCIAS"),
                                "motivo": (r.datos or {}).get("motivo") if r and r.datos else "salida del Orquestador no disponible; regla restrictiva"}
            self.almacen.escribir("HA", "AG-18", g3v)
            if not bloq:
                return paquete, {"dictamen": "APTO_CON_ADVERTENCIAS", "advertencias": [c["id"] for c in advert], "intentos": intento,
                                 "g3v_id": g3v["id"]}
            if intento >= 2:
                return paquete, {"dictamen": "BLOQUEADO", "bloqueos": [c["id"] for c in bloq], "intentos": intento, "g3v_id": g3v["id"]}
            # Corrección: se retiran las opciones con bloqueo y se reconstruye el paquete
            afectadas = set()
            for c in bloq:
                for inc in c["incidencias"]:
                    afectadas |= set(re.findall(r"OPP-\d{4}-\d{4,}", inc["ruta"] + " " + inc["detalle"]))
            if not afectadas:
                return paquete, {"dictamen": "BLOQUEADO", "bloqueos": [c["id"] for c in bloq], "intentos": intento, "g3v_id": g3v["id"]}
            paquete, extras = sint.retirar_opciones(self, paquete, extras, afectadas)

    def _redactar(self, paquete, extras, as_of, run_id, presupuesto, estado_run) -> tuple[dict, dict, dict]:
        msg = sint.mensaje_redactor(paquete)
        self.mensajeria.crear("CT-15", "AG-02", "AG-17", {"paquete_sintesis": msg}, run_id=run_id, presupuesto={"uc": 2})
        instr = ("Redacta los textos del informe visual para un usuario sin conocimientos financieros: tres frases de «la semana "
                 "en 30 segundos», por cada opción «por qué» y «qué podría salir mal» (≤ 20 palabras, sin jerga o explicada entre "
                 "paréntesis), motivos llanos de las clases sin tres opciones, un glosario de hasta 5 términos y una frase honesta "
                 "sobre el historial de aciertos. Índice Fernández-Huerta ≥ 70. Las cifras ya vienen calculadas: no inventes otras.")
        r = self._invocar("AG-17", "CT-15", {"paquete_sintesis": msg}, "REDACCION", instr, as_of, run_id, None, "redaccion", presupuesto, bolsa="COMUN")
        red = (r.datos if r and r.datos else None) or self.redaccion.textos_por_defecto(paquete)
        entreg, g3b = self.redaccion.generar(self, paquete, extras, red, as_of, run_id, estado_run)
        if g3b["dictamen"] == "BLOQUEADO" and any(c == "C12" for c in g3b.get("bloqueos", [])):
            # Una reescritura con la lista de frases largas (PB-39)
            msg2 = {"paquete_sintesis": msg, "reescritura": {"fernandez_huerta": g3b.get("legibilidad"), "frases_largas": g3b.get("frases_largas", [])}}
            r2 = self._invocar("AG-17", "CT-15", msg2, "REDACCION", instr + " Reescribe: el índice no alcanza 70.", as_of, run_id,
                               None, "redaccion", presupuesto, bolsa="COMUN")
            if r2 and r2.datos:
                entreg, g3b = self.redaccion.generar(self, paquete, extras, r2.datos, as_of, run_id, estado_run)
        return entreg, g3b, red

    def _congelar(self, extras: dict, as_of, run_id: str) -> list[str]:
        """F8: alta en F4 (AG-10) de los pronósticos de las opciones del informe y de las finalistas no seleccionadas."""
        ids = []
        for prg in extras["prg_borradores"]:
            if prg.get("prg_existente"):
                continue
            self.almacen.escribir("F4", "AG-10", prg)
            ids.append(prg["prg_id"])
        return ids

    def _escribir_f1_f3(self, analisis, seleccion, extras, as_of, run_id) -> None:
        sel_ids = {o["opp_id"]: o for c in extras["paquete_clases"] for o in extras["paquete_clases"][c]}
        prg_por_opp: dict[str, dict] = {}
        for p in extras["prg_borradores"]:
            if p.get("es_hito"):
                continue
            prg_por_opp.setdefault(p["opp_id"], {})[p["horizonte"]] = {"prg_id": p.get("prg_existente") or p["prg_id"], "vista": p["vista"]}
        for c in seleccion:
            for f in seleccion[c]["candidatos"]:
                previa = f.get("_previa")
                tnd_id = f.get("tnd_id")
                if f.get("tendencia") and (not tnd_id or f.get("_tnd_nuevo")) and not f.get("_arrastre"):
                    tnd_id = self._tendencia(f, c, as_of, run_id)
                en_sel = f["opp_id"] in sel_ids
                estado = ("VIGENTE" if f.get("_vigente") else "PROPUESTA") if en_sel else (
                    "EN_OBSERVACION" if f["_ht03"]["elegible"] or not f.get("_vigente") else "CERRADA")
                e = {"tipo_entrada": "ALTA" if previa is None else "ACTUALIZACION", "opp_id": f["opp_id"], "version": (previa or {}).get("version", 0) + 1,
                     "nombre": f.get("nombre"), "nombre_llano": f.get("nombre_llano"), "clase": c, "tipo_activo": c,
                     "tipo_opcion": f.get("tipo_opcion"), "subtipo": f.get("subtipo"), "ambito": f.get("ambito"),
                     "indicador_seguimiento": f.get("indicador_seguimiento"), "simbolo_seguimiento": f["proxy"],
                     "invertibilidad": f.get("invertibilidad"), "ejemplos_ilustrativos": f.get("ejemplos_ilustrativos"),
                     "criterios_seleccion_sugeridos": f.get("criterios_seleccion_sugeridos"), "metricas_clave": f.get("metricas_clave"),
                     "preguntas_para_B": f.get("preguntas_para_B"), "regiones": f.get("regiones"), "tnd_id": tnd_id, "tnd_ids": [tnd_id] if tnd_id else [],
                     "tesis": f.get("tesis"), "mecanismo": f.get("mecanismo"), "valoracion": f.get("valoracion"),
                     "catalizadores": f.get("catalizadores"), "riesgos": f.get("riesgos"), "riesgo_1a5": f["senales"].get("riesgo_1a5"),
                     "invalidacion": f.get("invalidacion"), "invalidacion_cuantitativa": f.get("invalidacion_cuantitativa"),
                     "que_no_sabemos": f.get("lo_que_no_sabemos"), "lo_que_no_sabemos": f.get("lo_que_no_sabemos"),
                     "horizontes_aplicables": f.get("horizontes_aplicables"), "liquidez": f.get("liquidez", "alta"),
                     "dimensiones": f["dimensiones"], "segunda_pasada": f.get("segunda_pasada"), "saturacion_narrativa": f.get("saturacion_narrativa", False),
                     "puntuaciones_totales": f["_ht03"]["puntuaciones"], "puertas": f["_puertas"], "elegible": f["_ht03"]["elegible"],
                     "motivos_no_elegible": [m["detalle"] for m in f["_ht03"]["motivos_no_elegible"]],
                     "objeciones_internas": f.get("_objeciones", []), "premortem": f.get("premortem"), "cluster_id": f.get("_cluster"),
                     "ps1": f.get("_ps1"), "evidencias": f.get("_evidencias", []), "tipo_pronostico": f.get("_tipo_pronostico"),
                     "referencia_indice": f.get("_referencia"), "horizontes_prg": prg_por_opp.get(f["opp_id"], {}),
                     "naturaleza_inversion": f.get("_naturaleza"), "horizonte_principal": f.get("_hp"),
                     "estado": estado, "de": (previa or {}).get("estado"), "rango_top3": (sel_ids.get(f["opp_id"]) or {}).get("rango"),
                     "run_ids": ((previa or {}).get("run_ids") or []) + [run_id], "confianza": (sel_ids.get(f["opp_id"]) or {}).get("confianza")}
                self.almacen.escribir("F3", "AG-02", e)
            for cz in seleccion[c]["cerradas"]:
                self.almacen.escribir("F3", "AG-02", {"tipo_entrada": "ACTUALIZACION", "opp_id": cz["opp_id"], "estado": "CERRADA",
                                                      "cierre": {"fecha": str(pd.Timestamp(as_of).date()), "motivo": cz["motivo_cierre"],
                                                                 "comentario": cz["comentario"]}, "run_ids_cierre": [run_id]})
            for f in analisis[c].get("exploratorias", []):
                sym = simbolo_seguimiento(f)
                oid, previa = self._opp_id(c, sym, f.get("tipo_opcion", "MERCADO"), as_of)
                if previa is None:
                    self.almacen.escribir("F3", "AG-02", {"tipo_entrada": "ALTA", "opp_id": oid, "clase": c, "tipo_activo": c, "nombre": f.get("nombre"),
                                                          "tipo_opcion": f.get("tipo_opcion"), "ambito": f.get("ambito"),
                                                          "indicador_seguimiento": f.get("indicador_seguimiento") or {"simbolo": sym},
                                                          "simbolo_seguimiento": sym,
                                                          "tesis": f.get("tesis"), "estado": "CANDIDATA", "exploratoria_prometedora": True,
                                                          "run_ids": [run_id]})

    def _tendencia(self, f: dict, clase: str, as_of, run_id: str) -> str:
        t = f["tendencia"]
        nombre = normalizar(t.get("nombre_canonico", ""))
        for x in self.almacen.estado("F1", as_of).values():
            if normalizar(x.get("nombre_canonico", "")) == nombre:
                self.almacen.escribir("F1", "AG-02", {"tipo_entrada": "DETECCION", "tnd_id": x["tnd_id"], "fecha_ultima_revision": str(pd.Timestamp(as_of).date()),
                                                      "referencias_ejecuciones": (x.get("referencias_ejecuciones") or []) + [run_id]})
                return x["tnd_id"]
        tid = f.get("tnd_id") or self.almacen.nuevo_id("TND")
        f["_tnd_nuevo"] = False
        self.almacen.escribir("F1", "AG-02", {
            "tipo_entrada": "ALTA", "tnd_id": tid, "version": 1, "nombre_canonico": t.get("nombre_canonico"),
            "categoria": t.get("categoria", "SECTORIAL"), "clase_principal": clase, "regiones": f.get("regiones"),
            "mecanismo": f.get("mecanismo"), "hipotesis_principal": f.get("tesis"), "fase_madurez": t.get("fase_madurez", "EMERGENTE"),
            "estado": "en investigación", "narrativa_saturada": bool(f.get("saturacion_narrativa")),
            "condiciones_invalidacion": f.get("invalidacion"), "horizontes_relevantes": f.get("horizontes_aplicables"),
            "referencias_evidencia": f.get("_evidencias", []), "referencias_ejecuciones": [run_id],
            "fecha_primera_deteccion": str(pd.Timestamp(as_of).date()), "fecha_ultima_revision": str(pd.Timestamp(as_of).date()),
            "fecha_proxima_revision": str((pd.Timestamp(as_of) + pd.Timedelta(days=90)).date()),
            "historial_estados": [{"fecha": str(pd.Timestamp(as_of).date()), "run_id": run_id, "de": "(detección)", "a": "en investigación",
                                   "justificacion": "nivel N2/N3 asignado"}]})
        return tid

    def _registrar_run(self, resultado, analisis, seleccion, presupuesto, gc0, disparador, alcance, hz, prioridad, prg, entreg) -> None:
        paquete = resultado["paquete"]
        run_id = resultado["run_id"]
        anterior = [r for r in self.almacen.leer("F5") if r.get("tipo_entrada") == "RUN" and r.get("entrega") != "BLOQUEADA"]
        top_ant = anterior[-1].get("top3_por_clase", {}) if anterior else {}
        top = {c: [o["opp_id"] for o in paquete["clases"][c]["opciones"]] for c in paquete["clases"]}
        cambios = {"entradas": sorted({x for v in top.values() for x in v} - {x for v in top_ant.values() for x in v}),
                   "salidas": sorted({x for v in top_ant.values() for x in v} - {x for v in top.values() for x in v})}
        cambios["mantenidas"] = sorted({x for v in top.values() for x in v} & {x for v in top_ant.values() for x in v})
        dec = []
        for c, an in analisis.items():
            for cb in an.get("cribado", []):
                dec.append({"clase": c, "objeto": cb.get("candidata"), "puerta": "GC1", "resultado": bool(cb.get("paso_gc1")), "motivo": cb.get("motivo")})
            for f in an["finalistas"]:
                dec.append({"clase": c, "objeto": f["proxy"], "puerta": "GC2", "resultado": f["_gc2"], "motivo": f"E provisional {f['_prov'].get('E')}"})
                if f["_gc2"]:
                    dec.append({"clase": c, "objeto": f["proxy"], "puerta": "GC3", "resultado": f["_gc3"], "motivo": f"RK provisional {f['_prov'].get('RK')}"})
        cons = self.contabilidad.resumen(run_id)
        self.almacen.escribir("F5", "AG-01", {
            "tipo_entrada": "RUN", "id": run_id, "tipo": resultado["tipo"], "disparador": disparador or {"origen": "HT-05"},
            "fecha_inicio": resultado["as_of"], "fecha_entrega": self.reloj.ahora(), "fecha_objetivo": resultado["as_of"],
            "alcance": alcance or {"clases": list(resultado["nivel_por_clase"])}, "horizontes": hz, "prioridad": prioridad,
            "nivel_por_clase": resultado["nivel_por_clase"], "gc0_por_clase": gc0, "decisiones_puertas": dec,
            "presupuesto": presupuesto.resumen(), "cierres_parciales": presupuesto.cierres, "consumo": {k: cons[k] for k in ("llamadas", "uc", "uc_llm", "uc_motor", "entrada", "salida", "cache_escritura", "cache_lectura")},
            "participantes": [{"agente": a, "encargos": d["llamadas"]} for a, d in cons["por_agente"].items()],
            "methodology_version": paquete.get("methodology_version"), "top3_por_clase": top, "cambios_vs_anterior": cambios,
            "apuestas_independientes": paquete.get("apuestas_independientes"), "prg_congelados": prg, "entregables": entreg,
            "g3": resultado.get("g3_entregables") or resultado.get("g3"), "estado": resultado["estado"],
            "entrega": resultado.get("entrega", "ENTREGADA"), "limitaciones": paquete.get("limitaciones", []),
            "sombra": {c: s["sombra"] for c, s in seleccion.items() if s.get("sombra")}})
        sombras = {c: s["sombra"] for c, s in seleccion.items() if s.get("sombra")}
        if sombras:
            self.almacen.escribir("F6", "AG-20", {"tipo_entrada": "SOMBRA", "id": f"SOM-{run_id}", "run_id": run_id, "comparacion": sombras,
                                                  "decisiones_top3_cambiadas": sum(s["cambios"] for s in sombras.values())})

    def _auditar(self, resultado: dict, tipo: str, nivel: dict, as_of, run_id: str) -> None:
        au = self.cfg.get("auditoria") or {}
        activa = au.get("en_backtest" if self.modo == "backtest" else "en_vivo", True)
        if not activa:
            return
        if tipo == "AD_HOC" and not any(v == "N3" for v in nivel.values()):
            h = int(hashlib.sha256(run_id.encode()).hexdigest(), 16) % 100
            if h >= int(100 * float(au.get("muestreo_ad_hoc", 0.3))):
                return
        paquete = resultado["paquete"]
        self.mensajeria.crear("CT-16", "AG-01", "AG-18", {"paquete_auditoria": {"run_id": run_id, "entregables": resultado["entregables"]}},
                              run_id=run_id, presupuesto={"uc": 2})
        msg = {"run_id": run_id, "tipo": tipo, "nivel_por_clase": nivel, "g3": resultado.get("g3_entregables"),
               "opciones": [{"opp_id": o["opp_id"], "clase": c, "nombre": o["nombre"], "tesis": o["tesis"], "puntuaciones": o["puntuaciones"],
                             "objeciones": o["objeciones"], "riesgo_1a5": o["riesgo_1a5"], "relevancia_decisional": o["relevancia_decisional"]}
                            for c, d in paquete["clases"].items() for o in d["opciones"]],
               "limitaciones": paquete.get("limitaciones", [])}
        self.mensajeria.crear("CT-17", "AG-18", "AG-19", msg, run_id=run_id, presupuesto={"uc": 2})
        r = self._invocar("AG-19", "CT-17", msg, "AUDITORIA",
                          "Revisión experta asíncrona del informe: rigor, sesgos, coherencia entre clases y cumplimiento de las reglas "
                          "R1–R25. Propón hallazgos con regla, descripción, severidad y objeto. No editas la entrega.", as_of, run_id)
        aud_id = self.almacen.nuevo_id("AUD")
        hal = []
        for h in ((r.datos or {}).get("hallazgos", []) if r and r.datos else []):
            hid = self.almacen.nuevo_id("HAL")
            self.almacen.escribir("HA", "AG-18", {"tipo_entrada": "HAL", "id": hid, "audit_id": aud_id, "objeto": h.get("objeto", run_id),
                                                  "regla_o_punto": h["regla"], "descripcion": h["descripcion"], "origen": "AUDITOR",
                                                  "severidad": h["severidad"], "estado": "ABIERTO"})
            hal.append(hid)
        self.almacen.escribir("HA", "AG-18", {"tipo_entrada": "AUD", "id": aud_id, "objeto": run_id, "muestreo": {"motivo": "OBLIGATORIO" if tipo == "PERIODICO" else "ALEATORIO"},
                                              "hallazgos": hal, "resumen": (r.datos or {}).get("resumen") if r and r.datos else "auditor no disponible",
                                              "estados_finales": {"proceso": "COMPLETED" if r and r.datos else "COMPLETED_WITH_LIMITATIONS"}})

    # ====================================================================================
    # C2 · Petición ad hoc (CT-01)
    # ====================================================================================
    def peticion(self, ct01: dict, as_of=None) -> dict:
        as_of = self.fijar_fecha(as_of or pd.Timestamp.today())
        msg = self.mensajeria.crear("CT-01", "BROKER", "AG-01", ct01)
        def _proc(m):
            alcance = m.get("alcance") or {}
            tipo = m.get("tipo", "AD_HOC")
            if tipo == "PERIODICO":
                tipo = "AD_HOC"
            return self.ciclo(as_of, tipo=tipo, alcance=alcance, nivel_forzado=m.get("nivel_forzado"),
                              horizontes=m.get("horizontes"), disparador={"origen": "CT-01", "msg_id": m["msg_id"]},
                              prioridad=m.get("prioridad", "NORMAL"))
        res, repetido = self.mensajeria.procesar_una_vez(msg, _proc)
        res = dict(res)
        res["acuse"] = self.mensajeria.acuse(msg, res["run_id"], nivel=res["nivel_por_clase"], repetido=repetido)
        return res

    # ====================================================================================
    # C3 · Consulta (CT-03)
    # ====================================================================================
    def consulta(self, texto: str, contexto: dict | None = None, as_of=None, urgencia: str = "NORMAL",
                 ejecutar_escalado: bool = True) -> dict:
        as_of = self.fijar_fecha(as_of or pd.Timestamp.today())
        msg = self.mensajeria.crear("CT-03", "BROKER", "AG-01", {"pregunta": texto, "contexto": contexto or {}, "urgencia": urgencia})
        qry_id = self.almacen.nuevo_id("QRY")
        indice = Indice(self.almacen, as_of)
        hits = indice.buscar(texto + " " + " ".join(str(v) for v in (contexto or {}).values() if v))
        runs = [r for r in self.almacen.leer("F5", as_of) if r.get("tipo_entrada") == "RUN"]
        ultimo = runs[-1] if runs else None
        opps = self.almacen.estado("F3", as_of)
        memoria = {"ultimo_run": {"run_id": ultimo["id"], "fecha": ultimo["_fecha"], "top3_por_clase": {
                        c: [{"opp_id": o, "nombre": (opps.get(o) or {}).get("nombre"), "estado": (opps.get(o) or {}).get("estado")} for o in lst]
                        for c, lst in ultimo.get("top3_por_clase", {}).items()},
                        "gc0_por_clase": {c: g.get("motivos") for c, g in (ultimo.get("gc0_por_clase") or {}).items()}} if ultimo else None,
                   "resultados_indice": [{"archivo": h["archivo"], "id": next(iter(RE_ID.findall(json.dumps(h["entrada"], default=str))), None),
                                          "extracto": {k: h["entrada"].get(k) for k in ("nombre", "tesis", "estado", "motivos_no_elegible",
                                                                                        "puntuaciones_totales", "afirmacion", "resultado", "cierre",
                                                                                        "clase", "top3_por_clase") if h["entrada"].get(k) is not None}}
                                         for h in hits]}
        cuerpo = {"query_id": qry_id, "pregunta": texto, "contexto": contexto or {}, "urgencia": urgencia, "memoria_bloque": memoria}
        pres = Presupuesto({"N0": float((self.cfg.get("presupuesto_uc") or {}).get("N0", 1))}, self.cfg)
        r = self._invocar("AG-01", "CT-03", cuerpo, "CONSULTA",
                          "Clasifica la consulta (ACLARACION, DATO, METODO, CONTRASTE, PROFUNDIZACION, ESTADO). Si es respondible con la "
                          "memoria del bloque (ruta N0), responde de forma breve y trazable citando solo identificadores presentes en "
                          "«memoria_bloque». Si exige análisis (ruta ANALITICA), da una respuesta provisional con lo que se sabe y propón "
                          "el escalado {nivel, clases, pregunta}. Nunca respondas con conocimiento propio no trazado.",
                          as_of, qry_id, None, "consulta", pres, bolsa="N0", max_uc_estimado=0.0)
        d = (r.datos if r and r.datos else None) or {"clase_consulta": "ACLARACION", "ruta": "ANALITICA",
                                                     "respuesta": "No puedo responder ahora con la memoria del bloque; se escala.",
                                                     "referencias": [], "confianza": "especulativo", "tema_normalizado": normalizar(texto)[:60]}
        conocidos = set()
        for a in ("F1", "F2", "F3", "F4", "F5", "F6", "RC"):
            for e in self.almacen.leer(a, as_of):
                conocidos |= set(RE_ID.findall(json.dumps({k: v for k, v in e.items() if not k.startswith("_")}, default=str)))
        refs = [x for x in d.get("referencias", []) if x in conocidos]
        descartadas = [x for x in d.get("referencias", []) if x not in conocidos]
        if d["ruta"] == "N0" and not refs:
            d["ruta"] = "ANALITICA"
            d["respuesta"] = "La memoria del bloque no contiene una respuesta trazable; se escala a análisis. " + d["respuesta"]
        d["referencias"] = refs
        escalado = None
        if d["ruta"] == "ANALITICA":
            esc = d.get("escalado") or {}
            clases = [c for c in (esc.get("clases") or (contexto or {}).get("clases") or []) if c in CLASES] or ["RV"]
            nivel = esc.get("nivel") if esc.get("nivel") in ("N1", "N2", "N3") else ("N3" if d["clase_consulta"] == "PROFUNDIZACION" else "N2")
            escalado = {"nivel": nivel, "clases": clases, "plazo_estimado": "mismo día (ejecución síncrona del ejecutor)",
                        "respuesta_provisional": d["respuesta"], "run_id": None}
            if ejecutar_escalado:
                res = self.ciclo(as_of, tipo="AD_HOC", alcance={"clases": clases, "pregunta": esc.get("pregunta") or texto},
                                 nivel_forzado=nivel, disparador={"origen": "CT-03", "msg_id": msg["msg_id"], "qry_id": qry_id})
                escalado["run_id"] = res["run_id"]
                escalado["estado_run"] = res["estado"]
        tema = normalizar(d.get("tema_normalizado") or texto)[:80].strip()
        hace4 = str((pd.Timestamp(as_of) - pd.Timedelta(weeks=4)).date())
        previas = [q for q in self.almacen.leer("F5", as_of) if q.get("tipo_entrada") == "QRY" and q.get("tema_normalizado") == tema and q["_fecha"] >= hace4]
        repeticion = None
        cons = self.contabilidad.resumen(qry_id)
        entrada = {"tipo_entrada": "QRY", "id": qry_id, "fecha_recepcion": msg["timestamp"], "fecha_respuesta": self.reloj.ahora(),
                   "pregunta": texto, "contexto": contexto or {}, "urgencia": urgencia, "clase_consulta": d["clase_consulta"],
                   "ruta": d["ruta"], "respuesta": d["respuesta"], "referencias": refs, "referencias_descartadas": descartadas,
                   "confianza": d["confianza"], "escalado": escalado, "tiempo_respuesta_s": 0, "tema_normalizado": tema,
                   "consumo_uc": cons["uc"], "estado": "RESPONDIDA_N0" if d["ruta"] == "N0" else "RESPONDIDA_ANALITICA"}
        if len(previas) + 1 >= 3:
            aviso = self.mensajeria.crear("CT-22", "AG-01", "AG-20", {"tipo": "PREGUNTA_REPETIDA", "tema": tema,
                                                                      "qry_ids": [q["id"] for q in previas] + [qry_id]}, query_id=qry_id)
            lec = self.evaluador.leccion_producto(as_of, tema, [q["id"] for q in previas] + [qry_id])
            repeticion = {"veces_4_semanas": len(previas) + 1, "aviso_ct22_msg_id": aviso["msg_id"], "lec_id": (lec or {}).get("id")}
            entrada["repeticion"] = repeticion
        self.almacen.escribir("F5", "AG-01", entrada)
        respuesta = self.mensajeria.crear("CT-03", "AG-01", "BROKER", {k: entrada[k] for k in ("clase_consulta", "ruta", "respuesta", "referencias", "confianza", "escalado")},
                                          query_id=qry_id, tipo_mensaje="RETORNO", estado="COMPLETO")
        return {"query_id": qry_id, **{k: entrada[k] for k in ("clase_consulta", "ruta", "respuesta", "referencias", "confianza", "escalado")},
                "repeticion": repeticion, "consumo": cons, "msg_id": respuesta["msg_id"]}

    # ====================================================================================
    # CT-04 · Decisiones y configuración
    # ====================================================================================
    def decision(self, ct04: dict, as_of=None) -> dict:
        as_of = self.fijar_fecha(as_of or pd.Timestamp.today())
        if not any(k in ct04 for k in ("decisiones", "valoracion_informe", "configuracion", "resultado_comunicado")):
            raise ValueError("CT-04 vacío: se espera decisiones, valoracion_informe, configuracion o resultado_comunicado")
        msg = self.mensajeria.crear("CT-04", "BROKER", "AG-01", ct04)
        ret_id = self.almacen.nuevo_id("RET")
        opps = self.almacen.estado("F3", as_of)
        for d in ct04.get("decisiones") or []:
            if d.get("opp_id") in opps:
                self.almacen.escribir("F3", "AG-02", {"tipo_entrada": "DECISION_BROKER", "opp_id": d["opp_id"],
                                                      "decision_broker": {"fecha": str(as_of.date()), "decision": d["decision"],
                                                                          "motivo": d.get("motivo"), "ret_id": ret_id}})
        aplicado, rechazos = {}, []
        conf = ct04.get("configuracion") or {}
        mapa = {"periodicidad": "P-01", "dia_hora_entrega": "P-01", "clases_activas": "P-02", "horizontes": "P-03", "idioma_usuario": "P-29"}
        f10 = self.f10(as_of)
        for k, v in conf.items():
            if k not in mapa:
                rechazos.append({"parametro": k, "motivo": "no es un parámetro de servicio (régimen CALIBRABLE u OPERADOR)"})
                continue
            if k == "clases_activas":
                malas = [c for c in v if c not in CLASES]
                if malas:
                    rechazos.append({"parametro": k, "motivo": f"clases desconocidas {malas}"})
                    continue
            if k == "horizontes":
                no = [h for h in v if h not in HORIZONTES]
                if no:
                    rechazos.append({"parametro": k, "motivo": f"horizontes desconocidos {no}"})
                    continue
                activas = conf.get("clases_activas") or f10.get("P-02") or list(CLASES)
                for h in v:
                    for c in activas:
                        if aplicabilidad(self.cfg, c, h) == "NO":
                            rechazos.append({"parametro": f"horizontes:{c}:{h}", "motivo": f"{h} es «No» para {c} en la tabla 8.3 (no se activa para esa clase)"})
            pid = mapa[k]
            valor = v if pid != "P-01" else f"{conf.get('periodicidad', 'SEMANAL')} · {conf.get('dia_hora_entrega', 'SAB 06:00')}"
            if pid in aplicado:
                continue
            cfg_id = self.almacen.nuevo_id("CFG")
            self.almacen.escribir("F10", "AG-01", {"tipo_entrada": "CFG", "cfg_id": cfg_id, "param_id": pid, "de": f10.get(pid), "a": valor,
                                                   "valor_vigente": valor, "autor": "AG-01", "origen": ret_id,
                                                   "fecha_efecto": str((as_of + pd.Timedelta(days=1)).date())})
            aplicado[pid] = cfg_id
        aviso = self.mensajeria.crear("CT-22", "AG-01", "AG-20", {"tipo": "DECISIONES_BROKER", "ret_id": ret_id,
                                                                  "decisiones": ct04.get("decisiones") or [],
                                                                  "resultado_comunicado": ct04.get("resultado_comunicado")}, query_id=ret_id)
        estado = "APLICADA" if not rechazos else ("APLICADA_PARCIALMENTE" if aplicado or ct04.get("decisiones") else "REGISTRADA")
        self.almacen.escribir("F5", "AG-01", {"tipo_entrada": "RET", "id": ret_id, "msg_id": msg["msg_id"], "fecha": str(as_of.date()),
                                              "decisiones": ct04.get("decisiones"), "valoracion_informe": ct04.get("valoracion_informe"),
                                              "configuracion": conf or None, "resultado_comunicado": ct04.get("resultado_comunicado"),
                                              "aplicado_en_f10": {"parametros": aplicado, "rechazos": rechazos}, "aviso_ct22": aviso["msg_id"],
                                              "estado": estado})
        return {"ret_id": ret_id, "estado": estado, "aplicado": aplicado, "rechazos": rechazos}

    # ====================================================================================
    def estado(self) -> dict:
        runs = [r for r in self.almacen.leer("F5") if r.get("tipo_entrada") == "RUN"]
        f4 = self.almacen.estado("F4")
        return {"ultimos_runs": [{"run_id": r["id"], "fecha": r["_fecha"], "tipo": r["tipo"], "estado": r["estado"],
                                  "uc": (r.get("consumo") or {}).get("uc"), "g3": (r.get("g3") or {}).get("dictamen")} for r in runs[-10:]],
                "colas": self.monitor.instantanea(),
                "consumo_sesion": {k: v for k, v in self.contabilidad.resumen().items() if k != "por_agente"},
                "pronosticos": {"abiertos": sum(1 for p in f4.values() if p.get("estado") == "ABIERTO"),
                                "resueltos": sum(1 for p in f4.values() if p.get("estado") == "RESUELTO")},
                "certificados_vigentes": [c["id"] for c in self.evaluador.certificados_vigentes()],
                "integridad_archivos": self.almacen.verificar_integridad()}
