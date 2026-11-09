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
import stat
import tempfile
import threading
from pathlib import Path
from typing import Dict, List, Optional, Union

ESTADOS = ("PROVISTA", "AUSENTE", "CADUCADA", "REVOCADA")


def validar_caducidad(caducidad: None | str | dt.date) -> str | None:
    """Caducidad en ISO 8601 (AAAA-MM-DD) o None (sin caducidad). Cualquier otro formato (p. ej., `31/12/2026`) se
    rechaza con ValueError antes de escribir nada en la bóveda."""
    if caducidad is None:
        return None
    if isinstance(caducidad, dt.datetime):
        raise ValueError(f"Caducidad de credencial con hora ({caducidad!r}): se espera una fecha AAAA-MM-DD")
    if isinstance(caducidad, dt.date):
        return caducidad.isoformat()
    if not isinstance(caducidad, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", caducidad.strip()):
        raise ValueError(f"Caducidad de credencial no ISO 8601 (AAAA-MM-DD): {caducidad!r}")
    try:
        return dt.date.fromisoformat(caducidad.strip()).isoformat()
    except ValueError as e:
        raise ValueError(f"Caducidad de credencial no válida: {caducidad!r}") from e


def _fecha_hoy(hoy: dt.date | None) -> dt.date:
    """Fecha con la que se comprueba la caducidad. Sin `hoy` se usa la fecha real del sistema: la caducidad de una
    credencial es un hecho del mundo real y nunca se deja de comprobar (falla cerrado)."""
    if hoy is None:
        return dt.date.today()
    if isinstance(hoy, dt.datetime):
        return hoy.date()
    if not isinstance(hoy, dt.date):
        raise TypeError(f"hoy debe ser una fecha, no {type(hoy).__name__}")
    return hoy


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

    def _leer(self, p: Path) -> dict:
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}

    def _escribir(self, p: Path, datos: dict, privado: bool = False) -> None:
        """Escritura atómica: archivo temporal en la misma carpeta (creado por `mkstemp` con modo 0o600 desde el primer
        byte), fsync y `os.replace`. Con `privado`, se fija y se comprueba 0o600 antes de sustituir el archivo; cualquier
        fallo (incluido el de chmod) se propaga y el archivo anterior queda intacto."""
        texto = json.dumps(datos, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8")
        fd, tmp = tempfile.mkstemp(prefix=f".{p.name}.", suffix=".tmp", dir=str(p.parent))
        try:
            with os.fdopen(fd, "wb") as fh:
                fh.write(texto)
                fh.flush()
                os.fsync(fh.fileno())
            if privado:
                os.chmod(tmp, 0o600)
                modo = stat.S_IMODE(os.stat(tmp).st_mode)
                if modo != 0o600:
                    raise PermissionError(f"HT-01 bóveda: no se pudo fijar 0o600 en {p.name} (modo {oct(modo)})")
            os.replace(tmp, p)
        except BaseException:
            try:
                os.unlink(tmp)
            except FileNotFoundError:
                pass
            raise

    # ---------------------------------------------------------------- vista sin valores (agentes, Coordinador)
    def estado(self, alias: str, hoy: dt.date | None = None) -> dict:
        """Estado sin valor. La caducidad se comprueba siempre (sin `hoy`, con la fecha real); una caducidad ilegible
        (p. ej., de un índice anterior a la validación) se trata como CADUCADA, nunca como vigente."""
        e = dict(self._leer(self._indice).get(alias) or {"alias": alias, "estado": "AUSENTE"})
        if e.get("estado") == "PROVISTA" and e.get("caducidad"):
            try:
                cad = dt.date.fromisoformat(str(validar_caducidad(e["caducidad"])))
            except ValueError:
                e["estado"], e["caducidad_invalida"] = "CADUCADA", True
            else:
                if cad < _fecha_hoy(hoy):
                    e["estado"] = "CADUCADA"
        return e

    def estado_servicio(self, servicio: str, hoy: dt.date | None = None) -> dict:
        return self.estado(alias_de(servicio), hoy)

    def listar(self, hoy: dt.date | None = None) -> list[dict]:
        return [self.estado(a, hoy) for a in sorted(self._leer(self._indice))]

    # ---------------------------------------------------------------- operaciones del Broker (fuera de banda)
    def depositar(self, servicio: str, valor: str, caducidad: str | None = None, alias: str | None = None) -> dict:
        """El Broker deposita la clave por el procedimiento seguro de la herramienta. Devuelve solo alias y estado."""
        # Validar antes de mutar: nada se escribe si un dato no es válido
        if not valor or not isinstance(valor, str):
            raise ValueError("Valor de credencial vacío")
        if not servicio or not isinstance(servicio, str):
            raise ValueError("Servicio de la credencial vacío")
        caducidad = validar_caducidad(caducidad)
        alias = alias or alias_de(servicio)
        with self._lock:
            idx, sec = self._leer(self._indice), self._leer(self._secretos)
            sec[alias] = valor
            idx[alias] = {"alias": alias, "servicio": servicio, "estado": "PROVISTA", "caducidad": caducidad,
                          "actualizado": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
            self._escribir(self._secretos, sec, privado=True)
            self._escribir(self._indice, idx)
        return {"credencial_ref": alias, "estado": "PROVISTA", "caducidad": caducidad}

    def revocar(self, alias: str) -> dict:
        with self._lock:
            idx, sec = self._leer(self._indice), self._leer(self._secretos)
            sec.pop(alias, None)
            if alias in idx:
                idx[alias]["estado"] = "REVOCADA"
            self._escribir(self._secretos, sec, privado=True)
            self._escribir(self._indice, idx)
        return self.estado(alias)

    # ---------------------------------------------------------------- capa de herramientas (nunca a un agente)
    def valor_para_herramienta(self, alias: str, hoy: dt.date | None = None) -> str | None:
        """Valor solo para la capa de herramientas. La caducidad se comprueba siempre: con `hoy` (la herramienta debe
        pasar la fecha de su reloj) o, si falta, con la fecha real del sistema; una credencial caducada, revocada,
        ausente o con caducidad ilegible se rechaza (None)."""
        if self.estado(alias, hoy).get("estado") != "PROVISTA":
            return None
        return self._leer(self._secretos).get(alias)
