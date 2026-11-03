"""HT-01 · Bóveda de credenciales (simulada) del Bloque A Forex V1.1 (R8, CT-25, 4.4 y 7.10 del Documento 0).

- El Broker deposita la clave **directamente** en la bóveda (`depositar`, que simula el procedimiento seguro de la
  herramienta); la respuesta del CT-25 solo transporta el estado y el alias (`credencial_ref`).
- Los agentes y los archivos del bloque solo ven `estado()` (alias, estado y caducidad): nunca el valor.
- `_valor_para_herramienta` es la única vía de lectura del valor y la usa exclusivamente la capa de ejecución de HT-01
  (p. ej., un proveedor de datos de pago). No forma parte de la API de los agentes.

Simulación: el valor se guarda ofuscado (no cifrado) en `boveda.json` con permisos 0600 dentro de la carpeta de estado. En
producción se sustituye por un gestor de secretos real; el contrato (alias + estado) no cambia. Estado de madurez (R22):
implementada como simulación, con pruebas; no validada como almacén seguro.
"""
from __future__ import annotations

import base64
import datetime as dt
import json
import os
import re
import threading
from pathlib import Path
from typing import Dict, Optional

ESTADOS = ("PROVISTA", "AUSENTE", "CADUCADA", "REVOCADA")


def alias_de(servicio: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", str(servicio).lower()).strip("-")[:48] or "servicio"
    return f"vault://ht01/{slug}"


class Boveda:
    def __init__(self, carpeta) -> None:
        self.carpeta = Path(carpeta)
        self.carpeta.mkdir(parents=True, exist_ok=True)
        self.ruta = self.carpeta / "boveda.json"
        self._lock = threading.Lock()
        self._datos: Dict[str, Dict] = json.loads(self.ruta.read_text(encoding="utf-8")) if self.ruta.exists() else {}

    def _guardar(self) -> None:
        self.ruta.write_text(json.dumps(self._datos, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        try:
            os.chmod(self.ruta, 0o600)
        except OSError:   # pragma: no cover - sistemas sin permisos POSIX
            pass

    def estado(self, servicio: str, hoy: Optional[dt.date] = None) -> Dict:
        """Lo único que ven los agentes: alias, estado y caducidad (nunca el valor)."""
        alias = alias_de(servicio)
        e = self._datos.get(alias)
        if not e:
            return {"servicio": servicio, "credencial_ref": None, "estado": "AUSENTE", "caducidad": None}
        estado = e["estado"]
        if estado == "PROVISTA" and e.get("caducidad") and hoy and dt.date.fromisoformat(e["caducidad"]) < hoy:
            estado = "CADUCADA"
        return {"servicio": servicio, "credencial_ref": alias, "estado": estado, "caducidad": e.get("caducidad")}

    def depositar(self, servicio: str, valor: str, caducidad: Optional[str] = None) -> str:
        """Depósito directo por el Broker (procedimiento seguro simulado). Devuelve solo el alias."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Valor de credencial vacío")
        alias = alias_de(servicio)
        with self._lock:
            self._datos[alias] = {"servicio": servicio, "estado": "PROVISTA", "caducidad": caducidad,
                                  "valor_ofuscado": base64.b64encode(valor.encode("utf-8")).decode("ascii")}
            self._guardar()
        return alias

    def revocar(self, servicio: str) -> None:
        alias = alias_de(servicio)
        with self._lock:
            if alias in self._datos:
                self._datos[alias]["estado"] = "REVOCADA"
                self._datos[alias].pop("valor_ofuscado", None)
                self._guardar()

    def _valor_para_herramienta(self, credencial_ref: str) -> Optional[str]:
        """Solo para la capa de ejecución de HT-01; nunca para un agente ni para un archivo del bloque."""
        e = self._datos.get(credencial_ref)
        if not e or e.get("estado") != "PROVISTA" or "valor_ofuscado" not in e:
            return None
        return base64.b64decode(e["valor_ofuscado"]).decode("utf-8")
