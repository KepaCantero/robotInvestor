"""Archivos operativos del Bloque B (F1–F6, F10, F11, RC, HA) en JSONL append-only con cadena de hash.

- Cada entrada lleva `_seq`, `_fecha` (fecha de corte en que se conoció), `_ts`, `_autor`, `_hash_prev` y `_hash`:
  cualquier modificación o borrado se detecta (`verificar_integridad`).
- Matriz de escritura (sección 5.1 del Documento 0): F1 AG-B01 · F2 AG-B15 · F3 AG-B02 (altas y contenido) y AG-B23
  (seguimiento, vigilancia, resultados y `decision_broker`) · F4 AG-B13 (alta) y AG-B23 (resolución) · F5 AG-B23 ·
  F6 AG-B02 · F10 AG-B01 (servicio), AG-B23 (calibrables) y OPERADOR · F11 AG-B01 (V2.1, registro de seguimientos
  encargados) · RC AG-B16 · HA AG-B21. Una escritura fuera de
  reserva se rechaza, se registra como incidencia en HA y lanza `EscrituraFueraDeReserva` (R8).
- Vista en una fecha: `leer(archivo, as_of)` solo devuelve lo conocible en esa fecha (backtest sin anticipación).
- Ninguna clave API se escribe nunca: `escribir` rechaza cualquier entrada con aspecto de credencial (R10).
"""
from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import re
import threading
from pathlib import Path
from typing import Callable, Dict, List, Optional
from zoneinfo import ZoneInfo

ARCHIVOS = {
    "F1": "F1_registro_peticiones_ejecuciones.jsonl", "F2": "F2_registro_evidencia.jsonl",
    "F3": "F3_registro_analisis_candidatos.jsonl", "F4": "F4_registro_pronosticos.jsonl",
    "F5": "F5_memoria_aprendizaje.jsonl", "F6": "F6_biblioteca_mercados.jsonl", "F10": "F10_configuracion.jsonl",
    "F11": "F11_registro_seguimientos.jsonl",
    "RC": "RC_registro_calculos.jsonl", "HA": "HA_historial_auditorias.jsonl",
}
PROPIETARIOS = {"F1": {"AG-B01"}, "F2": {"AG-B15"}, "F3": {"AG-B02", "AG-B23"}, "F4": {"AG-B13", "AG-B23"},
                "F5": {"AG-B23"}, "F6": {"AG-B02"}, "F10": {"AG-B01", "AG-B23", "OPERADOR"}, "F11": {"AG-B01"}, "RC": {"AG-B16"},
                "HA": {"AG-B21"}}
TIPOS_F3_EVAL = {"SEGUIMIENTO", "DECISION_BROKER", "RESULTADO", "ALERTA"}
CAMPOS_RESOLUCION_F4 = {"id", "tipo_entrada", "resolucion", "estado"}
PARAMETROS_SERVICIO = {"consultas_broker", "seguimientos", "politica_autorizacion", "tope_autorizacion_automatica_min", "criterios_nivel_auto", "marco_invertibilidad",
                       "top_n", "idioma_usuario", "objetivos_tiempo"}
PARAMETROS_CALIBRABLES = {"pesos_A", "pesos_E", "pesos_C", "pesos_S", "umbrales", "matriz", "modelo_tiempos", "caducidades",
                          "pureza_min", "umbrales_pv", "pesos_AE", "pesos_PEM", "umbrales_cuello"}
RE_CLAVE = re.compile(r"(sk-ant-[A-Za-z0-9_\-]{8,}|sk-trampa-[A-Za-z0-9\-]{6,}|AKIA[0-9A-Z]{16}|"
                      r"\"(?:api_key|clave|secret|token)\"\s*:\s*\"[^\"]{8,}\")", re.IGNORECASE)


class EscrituraFueraDeReserva(PermissionError):
    pass


class DatoProhibido(ValueError):
    """Entrada con una credencial o clave: se rechaza íntegra (R10)."""


class Reloj:
    """Reloj controlado: fecha de corte fijada y marcas temporales deterministas (o el reloj real si no se fija)."""

    def __init__(self, zona: str = "Europe/Madrid") -> None:
        self.zona = ZoneInfo(zona)
        self._fecha: Optional[dt.date] = None
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
            t = dt.datetime.combine(self.fecha, dt.time(7, 0), tzinfo=self.zona) + dt.timedelta(seconds=self._seg)
            self._seg += 1
        return t.isoformat(timespec="seconds")

    def avanzar_horas(self, horas: float) -> None:
        with self._lock:
            self._seg += int(horas * 3600)
            extra_dias = self._seg // 86400
            if extra_dias:
                self._fecha = self._fecha + dt.timedelta(days=extra_dias)
                self._seg %= 86400


def _hash(prev: str, contenido: Dict) -> str:
    h = hashlib.sha256(prev.encode())
    h.update(json.dumps(contenido, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8"))
    return h.hexdigest()


class Almacen:
    def __init__(self, carpeta, reloj: Optional[Reloj] = None) -> None:
        self.carpeta = Path(carpeta)
        self.carpeta.mkdir(parents=True, exist_ok=True)
        self.reloj = reloj or Reloj()
        self._lock = threading.RLock()
        self._entradas: Dict[str, List[Dict]] = {}
        for k, nombre in ARCHIVOS.items():
            p = self.carpeta / nombre
            self._entradas[k] = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] \
                if p.exists() else []
        self._ruta_cont = self.carpeta / "contadores.json"
        self._cont: Dict[str, int] = json.loads(self._ruta_cont.read_text(encoding="utf-8")) if self._ruta_cont.exists() else {}
        (self.carpeta / "puntos_control").mkdir(exist_ok=True)

    # ------------------------------------------------------------------ identificadores (Anexo A.2)
    def nuevo_id(self, prefijo: str, anio: Optional[int] = None) -> str:
        anio = anio or self.reloj.fecha.year
        with self._lock:
            k = f"{prefijo}-{anio}"
            self._cont[k] = self._cont.get(k, 0) + 1
            self._ruta_cont.write_text(json.dumps(self._cont, sort_keys=True), encoding="utf-8")
            return f"{prefijo}-{anio}-{self._cont[k]:04d}"

    def nuevo_run(self, pet_id: str) -> str:
        """RUN-B-AAAA-NNNN-rr: rr = número de ejecución (reanudación o fase) de la petición."""
        base = pet_id.replace("PET-B-", "RUN-B-")
        with self._lock:
            k = f"RUN::{pet_id}"
            self._cont[k] = self._cont.get(k, 0) + 1
            self._ruta_cont.write_text(json.dumps(self._cont, sort_keys=True), encoding="utf-8")
            return f"{base}-{self._cont[k]:02d}"

    @property
    def dir_puntos_control(self) -> Path:
        return self.carpeta / "puntos_control"

    # ------------------------------------------------------------------ escritura
    def _reserva(self, archivo: str, autor: str, e: Dict) -> Optional[str]:
        if archivo not in ARCHIVOS:
            return f"Archivo desconocido {archivo}"
        if autor not in PROPIETARIOS[archivo]:
            return f"{autor} no es propietario de escritura de {archivo} ({sorted(PROPIETARIOS[archivo])})"
        tipo = e.get("tipo_entrada")
        if archivo == "F3" and autor == "AG-B23" and tipo not in TIPOS_F3_EVAL:
            return "AG-B23 solo escribe en F3 campos de seguimiento, vigilancia, resultados y decision_broker"
        if archivo == "F3" and autor == "AG-B02" and tipo in TIPOS_F3_EVAL - {"ALERTA"}:
            return "AG-B02 no escribe campos de seguimiento ni la decisión del Broker en F3 (A.2)"
        if archivo == "F4":
            if autor == "AG-B13" and tipo != "ALTA":
                return "AG-B13 solo da de alta pronósticos (R14)"
            if autor == "AG-B23" and (tipo != "RESOLUCION" or set(e) - CAMPOS_RESOLUCION_F4):
                return "AG-B23 solo escribe campos de resolución en F4"
        if archivo == "F10" and tipo == "CFG":
            p = e.get("parametro")
            if autor == "AG-B01" and p not in PARAMETROS_SERVICIO:
                return f"AG-B01 solo cambia parámetros de servicio (no {p})"
            if autor == "AG-B23" and p not in PARAMETROS_CALIBRABLES:
                return f"AG-B23 solo cambia parámetros calibrables (no {p})"
        return None

    def escribir(self, archivo: str, autor: str, entrada: Dict) -> Dict:
        if RE_CLAVE.search(json.dumps(entrada, ensure_ascii=False, default=str)):
            if archivo != "HA":
                self.incidencia("CREDENCIAL_FUERA_DE_BOVEDA", f"Entrada para {archivo} con aspecto de clave: rechazada "
                                "íntegra y no reproducida", autor, severidad="Crítica")
            raise DatoProhibido("Entrada con una credencial o clave: rechazada (R10)")
        motivo = self._reserva(archivo, autor, entrada)
        if motivo:
            if not (archivo == "HA" and autor == "AG-B21"):
                self.incidencia("ACCESO_FUERA_DE_MATRIZ", f"{archivo}: {motivo}", autor)
            raise EscrituraFueraDeReserva(motivo)
        with self._lock:
            lista = self._entradas[archivo]
            prev = lista[-1]["_hash"] if lista else "0" * 64
            e = copy.deepcopy(entrada)
            e.update({"_seq": len(lista) + 1, "_fecha": str(self.reloj.fecha), "_ts": self.reloj.ahora(),
                      "_autor": autor, "_hash_prev": prev})
            e["_hash"] = _hash(prev, {k: v for k, v in e.items() if k != "_hash"})
            lista.append(e)
            with open(self.carpeta / ARCHIVOS[archivo], "a", encoding="utf-8") as fh:
                fh.write(json.dumps(e, ensure_ascii=False, default=str) + "\n")
            return e

    def incidencia(self, tipo: str, detalle: str, objeto: str = "", severidad: str = "Material", **extra) -> Dict:
        return self.escribir("HA", "AG-B21", {"tipo_entrada": "INC", "id": self.nuevo_id("INC-B"), "tipo": tipo,
                                              "severidad": severidad, "objeto": objeto, "detalle": detalle, **extra})

    # ------------------------------------------------------------------ lectura
    def leer(self, archivo: str, as_of=None, filtro: Optional[Callable[[Dict], bool]] = None) -> List[Dict]:
        lim = str(as_of)[:10] if as_of is not None else None
        with self._lock:
            out = [e for e in self._entradas[archivo] if lim is None or e["_fecha"] <= lim]
        if filtro:
            out = [e for e in out if filtro(e)]
        return copy.deepcopy(out)

    def estado(self, archivo: str, clave: str = "id", as_of=None, tipo: Optional[str] = None) -> Dict[str, Dict]:
        """Vista consolidada por clave (la última entrada prevalece campo a campo; historial conservado)."""
        out: Dict[str, Dict] = {}
        for e in self.leer(archivo, as_of):
            if tipo and e.get("tipo_entrada") != tipo and e.get("tipo_objeto_registro") != tipo:
                continue
            k = e.get(clave)
            if not k:
                continue
            base = out.setdefault(k, {"_historial": []})
            for c, v in e.items():
                if not c.startswith("_"):
                    base[c] = v
            base["_historial"].append({"seq": e["_seq"], "fecha": e["_fecha"], "tipo": e.get("tipo_entrada"), "autor": e["_autor"]})
            base["_ultima_fecha"] = e["_fecha"]
        return out

    def verificar_integridad(self) -> Dict[str, bool]:
        res = {}
        for a, nombre in ARCHIVOS.items():
            p = self.carpeta / nombre
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
