"""HT-01 · Bóveda de credenciales (simulada) — Documento 0 óptima V5.1, 4.4, 7.10 y R8.

Las claves de los servicios externos las deposita el Broker por CT-25 directamente en la bóveda (nunca en un
mensaje, un archivo del bloque ni el contexto de un agente). Los agentes y el Coordinador solo ven el alias
(`credencial_ref`) y el estado (`PROVISTA`, `AUSENTE`, `CADUCADA`, `REVOCADA`).

Simulación del ejecutor: la bóveda vive en `<estado>/boveda/`: `indice.json` (alias → servicio, estado,
caducidad; sin valores) y `secretos.json` (alias → valor, permisos 0600). Ningún método público devuelve el
valor salvo `valor_para_herramienta`, que solo debe usar la capa de herramientas (p. ej., un proveedor de
datos de pago) y que nunca se registra. En producción se sustituye por un gestor de secretos.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import threading
from pathlib import Path
from typing import Dict, List, Optional

ESTADOS = ("PROVISTA", "AUSENTE", "CADUCADA", "REVOCADA")


def alias_de(servicio: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", servicio.lower()).strip("-")[:40] or "servicio"
    return f"boveda://ht01/{s}"


class Boveda:
    def __init__(self, carpeta) -> None:
        self.carpeta = Path(carpeta)
        self.carpeta.mkdir(parents=True, exist_ok=True)
        self._indice = self.carpeta / "indice.json"
        self._secretos = self.carpeta / "secretos.json"
        self._lock = threading.Lock()

    def _leer(self, p: Path) -> Dict:
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}

    def _escribir(self, p: Path, datos: Dict, privado: bool = False) -> None:
        p.write_text(json.dumps(datos, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
        if privado:
            try:
                os.chmod(p, 0o600)
            except OSError:  # pragma: no cover - sistemas sin permisos POSIX
                pass

    # ---------------------------------------------------------------- vista sin valores (agentes, Coordinador)
    def estado(self, alias: str, hoy: Optional[dt.date] = None) -> Dict:
        e = dict(self._leer(self._indice).get(alias) or {"alias": alias, "estado": "AUSENTE"})
        if e.get("estado") == "PROVISTA" and e.get("caducidad") and hoy and dt.date.fromisoformat(e["caducidad"]) < hoy:
            e["estado"] = "CADUCADA"
        return e

    def estado_servicio(self, servicio: str, hoy: Optional[dt.date] = None) -> Dict:
        return self.estado(alias_de(servicio), hoy)

    def listar(self, hoy: Optional[dt.date] = None) -> List[Dict]:
        return [self.estado(a, hoy) for a in sorted(self._leer(self._indice))]

    # ---------------------------------------------------------------- operaciones del Broker (fuera de banda)
    def depositar(self, servicio: str, valor: str, caducidad: Optional[str] = None, alias: Optional[str] = None) -> Dict:
        """El Broker deposita la clave por el procedimiento seguro de la herramienta. Devuelve solo alias y estado."""
        if not valor or not isinstance(valor, str):
            raise ValueError("Valor de credencial vacío")
        alias = alias or alias_de(servicio)
        with self._lock:
            idx, sec = self._leer(self._indice), self._leer(self._secretos)
            sec[alias] = valor
            idx[alias] = {"alias": alias, "servicio": servicio, "estado": "PROVISTA", "caducidad": caducidad,
                          "actualizado": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
            self._escribir(self._secretos, sec, privado=True)
            self._escribir(self._indice, idx)
        return {"credencial_ref": alias, "estado": "PROVISTA", "caducidad": caducidad}

    def revocar(self, alias: str) -> Dict:
        with self._lock:
            idx, sec = self._leer(self._indice), self._leer(self._secretos)
            sec.pop(alias, None)
            if alias in idx:
                idx[alias]["estado"] = "REVOCADA"
            self._escribir(self._secretos, sec, privado=True)
            self._escribir(self._indice, idx)
        return self.estado(alias)

    # ---------------------------------------------------------------- capa de herramientas (nunca a un agente)
    def valor_para_herramienta(self, alias: str, hoy: Optional[dt.date] = None) -> Optional[str]:
        if self.estado(alias, hoy).get("estado") != "PROVISTA":
            return None
        return self._leer(self._secretos).get(alias)
