"""Almacén de archivos operativos del bloque (F1–F6, F10, F11, RC, HA) en JSONL append-only.

- Cada línea es una entrada con metadatos `_seq`, `_fecha` (fecha as_of en que se conoció), `_ts`,
  `_autor`, `_hash_prev` y `_hash` (cadena de integridad: cualquier modificación o borrado se detecta).
- Matriz de escritura (sección 5.1 del Documento 0): cada archivo tiene su propietario; F4 distingue
  alta (AG-10) y resolución (AG-20, solo campos de resolución); F10 distingue parámetros de servicio
  (AG-01), calibrables (AG-20) y del operador. Una escritura fuera de reserva se rechaza, se registra
  como incidencia en HA y lanza `EscrituraFueraDeReserva`.
- Vista `as_of`: `leer(archivo, as_of)` solo devuelve lo conocible en esa fecha (backtest sin fuga).
"""
from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import threading
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any, Dict, List, Optional
from zoneinfo import ZoneInfo

ARCHIVOS = {
    "F1": "F1_registro_maestro_tendencias.jsonl",
    "F2": "F2_registro_evidencia.jsonl",
    "F3": "F3_registro_oportunidades.jsonl",
    "F4": "F4_registro_pronosticos.jsonl",
    "F5": "F5_historial_analisis.jsonl",
    "F6": "F6_memoria_aprendizaje.jsonl",
    "F10": "F10_configuracion.jsonl",
    "F11": "F11_registro_seguimientos.jsonl",    # V5.1: Registro de seguimientos encargados (CT-24)
    "RC": "RC_registro_calculos.jsonl",
    "HA": "HA_historial_auditorias.jsonl",
}
PROPIETARIOS = {"F1": {"AG-02"}, "F2": {"AG-12"}, "F3": {"AG-02"}, "F4": {"AG-10", "AG-20"}, "F5": {"AG-01"},
                "F6": {"AG-20"}, "F10": {"AG-01", "AG-20", "OPERADOR"}, "F11": {"AG-01"}, "RC": {"AG-13"}, "HA": {"AG-18"}}
CLAVES = {"F1": "tnd_id", "F2": "id", "F3": "opp_id", "F4": "prg_id", "F5": "id", "F6": "id", "F10": "param_id", "F11": "seg_id",
          "RC": "calc_id", "HA": "id"}
# Regímenes del esquema F10 V3.0 (05_Archivos_operativos, «Configuración y parámetros del bloque», tabla de P-01 a P-44).
# T-65 (CS-11 de T-53): se completan con P-34, P-38 y P-44 (SERVICIO) y P-35, P-36, P-39 y P-40 (CALIBRABLE)
PARAMETROS_SERVICIO = {"P-01", "P-02", "P-03", "P-21", "P-29", "P-34", "P-38", "P-44"}
PARAMETROS_CALIBRABLES = {"P-05", "P-06", "P-07", "P-08", "P-09", "P-10", "P-11", "P-12", "P-17", "P-20", "P-22",
                          "P-23", "P-24", "P-25", "P-26", "P-27", "P-30", "P-31", "P-35", "P-36", "P-39", "P-40",
                          "P-42"}   # P-42: degradación automática de H5 (12.2), CALIBRABLE en el esquema F10 V3.0
CAMPOS_RESOLUCION_F4 = {"prg_id", "tipo_entrada", "resolucion", "estado"}


class EscrituraFueraDeReserva(PermissionError):
    pass


class PronosticoCongelado(EscrituraFueraDeReserva):
    """R11: un pronóstico de F4 se congela en su alta y se resuelve una sola vez. Se rechaza una segunda ALTA con un
    `prg_id` existente, una RESOLUCION de un `prg_id` sin alta y una segunda RESOLUCION del mismo pronóstico."""


class Reloj:
    """Reloj controlado: marcas temporales deterministas a partir de la fecha as_of."""

    def __init__(self, zona: str = "Europe/Madrid") -> None:
        self.zona = ZoneInfo(zona)
        self._fecha: dt.date | None = None
        self._seg = 0
        self._lock = threading.Lock()

    def fijar(self, fecha) -> None:
        f = dt.date.fromisoformat(str(fecha)[:10])
        with self._lock:
            if f != self._fecha:
                self._fecha, self._seg = f, 0

    @property
    def fecha(self) -> dt.date:
        if self._fecha is None:
            self.fijar(dt.date.today())
        return self._fecha

    def ahora(self) -> str:
        with self._lock:
            base = dt.datetime.combine(self.fecha, dt.time(6, 0), tzinfo=self.zona)
            t = base + dt.timedelta(seconds=self._seg)
            self._seg += 1
        return t.isoformat(timespec="seconds")


def _hash(prev: str, contenido: dict) -> str:
    h = hashlib.sha256(prev.encode())
    h.update(json.dumps(contenido, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8"))
    return h.hexdigest()


class Almacen:
    def __init__(self, carpeta, reloj: Reloj | None = None) -> None:
        self.carpeta = Path(carpeta)
        self.carpeta.mkdir(parents=True, exist_ok=True)
        self.reloj = reloj or Reloj()
        self._lock = threading.RLock()
        self._entradas: dict[str, list[dict]] = {}
        for k, nombre in ARCHIVOS.items():
            p = self.carpeta / nombre
            self._entradas[k] = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] \
                if p.exists() else []
        # Índice de F4 (prg_id → tipos de entrada ya escritos) para la comprobación de congelación (R11)
        self._f4_tipos: dict[str, set] = {}
        for e in self._entradas["F4"]:
            if e.get("prg_id"):
                self._f4_tipos.setdefault(e["prg_id"], set()).add(e.get("tipo_entrada"))
        self._ruta_contadores = self.carpeta / "contadores.json"
        self._contadores: dict[str, int] = json.loads(self._ruta_contadores.read_text(encoding="utf-8")) \
            if self._ruta_contadores.exists() else {}

    # ----------------------------------------------------------------------------------------
    # Identificadores
    # ----------------------------------------------------------------------------------------
    def nuevo_id(self, prefijo: str, anio: int | None = None, ancho: int = 4) -> str:
        anio = anio or self.reloj.fecha.year
        with self._lock:
            k = f"{prefijo}-{anio}"
            self._contadores[k] = self._contadores.get(k, 0) + 1
            self._ruta_contadores.write_text(json.dumps(self._contadores, sort_keys=True), encoding="utf-8")
            return f"{prefijo}-{anio}-{self._contadores[k]:0{ancho}d}"

    # ----------------------------------------------------------------------------------------
    # Escritura
    # ----------------------------------------------------------------------------------------
    def _comprobar_reserva(self, archivo: str, autor: str, entrada: dict) -> str | None:
        if archivo not in ARCHIVOS:
            return f"Archivo desconocido {archivo}"
        if autor not in PROPIETARIOS[archivo]:
            return f"{autor} no es propietario de escritura de {archivo} (propietarios: {sorted(PROPIETARIOS[archivo])})"
        tipo = entrada.get("tipo_entrada")
        if archivo == "F4":
            if autor == "AG-10" and tipo != "ALTA":
                return "AG-10 solo da de alta pronósticos en F4 (R11)"
            if autor == "AG-20":
                if tipo != "RESOLUCION":
                    return "AG-20 solo escribe campos de resolución en F4"
                extra = set(entrada) - CAMPOS_RESOLUCION_F4
                if extra:
                    return f"AG-20 intenta escribir campos de alta en F4: {sorted(extra)}"
        if archivo == "F10" and tipo == "CFG":
            pid = entrada.get("param_id")
            if autor == "AG-01" and pid not in PARAMETROS_SERVICIO:
                return f"AG-01 solo modifica parámetros de servicio (no {pid})"
            if autor == "AG-20" and pid not in PARAMETROS_CALIBRABLES:
                return f"AG-20 solo modifica parámetros calibrables (no {pid})"
        return None

    def _comprobar_congelacion_f4(self, entrada: dict) -> str | None:
        """R11 (validar antes de mutar): ALTA solo de un `prg_id` nuevo; RESOLUCION solo de un `prg_id` dado de alta
        y todavía sin resolver. Se llama con el cerrojo tomado (la comprobación y la escritura son atómicas)."""
        tipo, pid = entrada.get("tipo_entrada"), entrada.get("prg_id")
        if not pid:
            return f"F4: {tipo} sin prg_id"
        previas = self._f4_tipos.get(pid, set())
        if tipo == "ALTA":
            if previas:
                return f"R11: {pid} ya está dado de alta y congelado en F4 (no se admite una segunda ALTA)"
        elif tipo == "RESOLUCION":
            if "ALTA" not in previas:
                return f"R11: RESOLUCION de {pid}, que no está dado de alta en F4"
            if "RESOLUCION" in previas:
                return f"R11: {pid} ya está resuelto en F4 (no se admite una segunda RESOLUCION)"
        return None

    def escribir(self, archivo: str, autor: str, entrada: dict) -> dict:
        motivo = self._comprobar_reserva(archivo, autor, entrada)
        if motivo:
            if archivo != "HA" or autor != "AG-18":
                self._incidencia_interna("ACCESO_FUERA_DE_MATRIZ", f"{archivo}: {motivo}", autor)
            raise EscrituraFueraDeReserva(motivo)
        with self._lock:
            if archivo == "F4":
                motivo = self._comprobar_congelacion_f4(entrada)
                if motivo:
                    self._incidencia_interna("ESCRITURA", motivo, autor)
                    raise PronosticoCongelado(motivo)
            lista = self._entradas[archivo]
            prev = lista[-1]["_hash"] if lista else "0" * 64
            e = copy.deepcopy(entrada)
            e["_seq"] = len(lista) + 1
            e["_fecha"] = str(self.reloj.fecha)
            e["_ts"] = self.reloj.ahora()
            e["_autor"] = autor
            e["_hash_prev"] = prev
            e["_hash"] = _hash(prev, {k: v for k, v in e.items() if k != "_hash"})
            lista.append(e)
            if archivo == "F4" and e.get("prg_id"):
                self._f4_tipos.setdefault(e["prg_id"], set()).add(e.get("tipo_entrada"))
            with open(self.carpeta / ARCHIVOS[archivo], "a", encoding="utf-8") as fh:
                fh.write(json.dumps(e, ensure_ascii=False, default=str) + "\n")
            return e

    def _incidencia_interna(self, tipo: str, detalle: str, agente: str) -> None:
        self.escribir("HA", "AG-18", {"tipo_entrada": "INC", "id": self.nuevo_id("INC"), "tipo": tipo,
                                      "severidad": "Material", "objeto": agente, "detalle": detalle,
                                      "tratamiento": "rechazada y registrada", "escalado_operador": True})

    def incidencia(self, tipo: str, detalle: str, objeto: str = "", severidad: str = "Material", **extra) -> dict:
        return self.escribir("HA", "AG-18", {"tipo_entrada": "INC", "id": self.nuevo_id("INC"), "tipo": tipo,
                                             "severidad": severidad, "objeto": objeto, "detalle": detalle,
                                             "tratamiento": extra.pop("tratamiento", "registrada"), **extra})

    # ----------------------------------------------------------------------------------------
    # Lectura
    # ----------------------------------------------------------------------------------------
    def leer(self, archivo: str, as_of=None, filtro: Callable[[dict], bool] | None = None) -> list[dict]:
        lim = str(as_of)[:10] if as_of is not None else None
        with self._lock:
            out = [e for e in self._entradas[archivo] if lim is None or e["_fecha"] <= lim]
        if filtro:
            out = [e for e in out if filtro(e)]
        return copy.deepcopy(out)

    def estado(self, archivo: str, as_of=None, clave: str | None = None) -> dict[str, dict]:
        """Vista consolidada por clave: la última entrada de cada objeto prevalece campo a campo;
        se conserva el historial de entradas (append-only)."""
        clave = clave or CLAVES[archivo]
        out: dict[str, dict] = {}
        for e in self.leer(archivo, as_of):
            k = e.get(clave)
            if not k:
                continue
            if k not in out:
                out[k] = {"_historial": []}
            base = out[k]
            for c, v in e.items():
                if c.startswith("_"):
                    continue
                if c == "resolucion" and archivo == "F4":
                    base.setdefault("resoluciones", []).append(v)
                base[c] = v
            base["_historial"].append({"seq": e["_seq"], "fecha": e["_fecha"], "tipo": e.get("tipo_entrada"),
                                       "autor": e["_autor"]})
            base["_ultima_fecha"] = e["_fecha"]
        return out

    def verificar_integridad(self, archivo: str | None = None) -> dict[str, bool]:
        res = {}
        for a in ([archivo] if archivo else ARCHIVOS):
            p = self.carpeta / ARCHIVOS[a]
            lineas = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []
            prev, ok = "0" * 64, True
            for i, e in enumerate(lineas):
                if e.get("_hash_prev") != prev or e.get("_seq") != i + 1 or \
                        _hash(prev, {k: v for k, v in e.items() if k != "_hash"}) != e.get("_hash"):
                    ok = False
                    break
                prev = e["_hash"]
            res[a] = ok
        return res
