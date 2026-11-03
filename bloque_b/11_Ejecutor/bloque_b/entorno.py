"""Entorno de ejecución: configuración, almacén, reloj, proveedor de datos (HT-01), bóveda, cliente LLM, prompts,
invocador, Motor, universos, ámbitos y referencias. Lo comparten todos los subcomandos."""
from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Dict, List, Optional

from .agentes import Invocador
from .almacen import Almacen, Reloj
from .configuracion import TIPOS_ACTIVO, cargar_ambitos, cargar_config, ruta
from .herramientas import ht11
from .herramientas.boveda import Boveda
from .herramientas.ht01_datos import ProveedorCSV, ProveedorDatos, ProveedorSintetico
from .llm import crear_cliente
from .motor import Motor
from .prompts import CatalogoPrompts
from .referencias import Referencias


def cargar_universos(cfg: Dict) -> Dict[str, List[Dict]]:
    base = ruta(cfg, "universos")
    out = {}
    for t in TIPOS_ACTIVO:
        p = base / f"universo_{t}.csv"
        out[t] = ht11.leer_csv(p) if p.exists() else []
    return out


def series_de_ejemplo(cfg: Dict, universos: Dict[str, List[Dict]], ambitos: Dict) -> Dict[str, Dict]:
    """Símbolo → {grupo, alta, baja} de todas las series que usan los universos y los ámbitos de ejemplo."""
    out: Dict[str, Dict] = {}
    for t, filas in universos.items():
        for f in filas:
            if f.get("simbolo"):
                amb = (f.get("ambitos") or "x").split(";")[0]
                out[f["simbolo"]] = {"grupo": f"{t}:{amb}", "alta": f.get("fecha_alta") or None, "baja": f.get("fecha_baja") or None}
    for clave, a in ambitos.items():
        t = (a.get("tipos_activo") or ["RV"])[0]
        for k in ("indicador", "referencia"):
            s = (a.get(k) or {}).get("simbolo")
            if s and s not in out:
                out[s] = {"grupo": f"{t}:{clave}" if k == "indicador" else f"{t}:referencia", "alta": None, "baja": None}
    return out


def proveedor_sintetico(cfg: Dict, universos=None, ambitos=None, semilla: Optional[int] = None) -> ProveedorSintetico:
    if semilla is None:
        semilla = int((cfg.get("datos_sinteticos") or {}).get("semilla", 14))
    universos = universos if universos is not None else cargar_universos(cfg)
    ambitos = ambitos if ambitos is not None else cargar_ambitos(cfg)
    s = series_de_ejemplo(cfg, universos, ambitos)
    return ProveedorSintetico({k: v["grupo"] for k, v in s.items()}, semilla=semilla, inicio="2021-01-04", fin="2026-10-30",
                              bajas={k: v["baja"] for k, v in s.items() if v["baja"]},
                              altas={k: v["alta"] for k, v in s.items() if v["alta"] and v["alta"] > "2021-01-04"})


class Entorno:
    def __init__(self, cfg: Optional[Dict] = None, estado: str = "./estado_bloque_b", salida: str = "./entregables",
                 datos: Optional[str] = None, cliente: str = "mock", replay: Optional[str] = None,
                 replay_modo: str = "reproducir", as_of: Optional[str] = None, modo: Optional[str] = None,
                 boveda: Optional[str] = None, proveedor: Optional[ProveedorDatos] = None) -> None:
        self.cfg = cfg or cargar_config()
        self.modo = modo or self.cfg.get("modo", "vivo")
        self.reloj = Reloj(self.cfg.get("zona_horaria", "Europe/Madrid"))
        self.reloj.fijar(as_of or dt.date.today().isoformat())
        self.alm = Almacen(estado, self.reloj)
        self.salida = Path(salida)
        self.ambitos = cargar_ambitos(self.cfg)
        self.universos = cargar_universos(self.cfg)
        if proveedor is not None:
            self.prov = proveedor
        elif datos:
            self.prov = ProveedorCSV(datos)
        else:
            self.prov = proveedor_sintetico(self.cfg, self.universos, self.ambitos)
        self.prov.fijar_as_of(self.reloj.fecha)
        self.boveda = Boveda(boveda)
        self.tipo_cliente = cliente
        self.cliente = crear_cliente(cliente, self.cfg, replay, replay_modo)
        self.prompts = CatalogoPrompts(self.cfg, cliente)
        self.inv = Invocador(self.cfg, self.cliente, self.prompts, self.alm, self.modo)
        self.motor = Motor(self.prov, self.alm, self.cfg)
        self.refs = Referencias(self.cfg)
        tipo_reloj = (self.cfg.get("reloj") or {}).get("tipo", "auto")
        self.reloj_simulado = tipo_reloj == "simulado" or (tipo_reloj == "auto" and cliente != "anthropic")
        self._inicializar_f10()

    def fijar_as_of(self, fecha) -> None:
        self.reloj.fijar(fecha)
        self.prov.fijar_as_of(self.reloj.fecha)

    @property
    def as_of(self) -> str:
        return self.reloj.fecha.isoformat()

    def _inicializar_f10(self) -> None:
        if not self.alm.leer("F10"):
            self.alm.escribir("F10", "OPERADOR", {"tipo_entrada": "INICIAL", "id": "CFG-B-INICIAL",
                                                  "methodology_version": self.cfg.get("methodology_version", "2.0"),
                                                  "politica_autorizacion": self.cfg.get("politica_autorizacion") or [],
                                                  "tope_autorizacion_automatica_min": (self.cfg.get("puerta_tiempo") or {}).get("tope_automatico_min", 240),
                                                  "marco_invertibilidad": self.cfg.get("marco_invertibilidad"),
                                                  "top_n": self.cfg.get("top_n"), "conectores": self.boveda.estado()})

    def f10(self) -> Dict:
        """Vista vigente de F10 (la última entrada de cada parámetro prevalece)."""
        out: Dict = {}
        for e in self.alm.leer("F10"):
            if e.get("tipo_entrada") == "INICIAL":
                out.update({k: v for k, v in e.items() if not k.startswith("_") and k not in ("tipo_entrada", "id")})
            elif e.get("tipo_entrada") == "CFG":
                out[e["parametro"]] = e["valor"]
        return out
