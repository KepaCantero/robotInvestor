"""HT-01 · Bóveda de credenciales simulada y conectores por alias (R10, 17.2).

El Broker deposita la clave por el canal seguro del ecosistema (aquí: variable de entorno `BLOQUE_B_BOVEDA_<ALIAS>` o un
archivo de bóveda con permisos 600 fuera del directorio de estado, indicado con `--boveda`). Los agentes y el resto del
ejecutor solo conocen el alias (`credencial_ref`); la clave se entrega al conector en la capa de ejecución, nunca se
registra (F1 guarda solo la solicitud CRED-B y su estado) y nunca aparece en mensajes, archivos ni registros.
"""
from __future__ import annotations

import json
import os
import re
import stat
from pathlib import Path
from typing import Callable, Dict, Optional

# Conectores conocidos: los gratuitos sin clave están siempre activos; los que exigen registro o clave gratuita
# necesitan un alias en la bóveda; los de pago están desactivados (Anexo A, R30).
CONECTORES = {
    "precios_csv": {"tipo_acceso": "GRATUITO", "requiere_clave": False, "dimensiones": ["D9", "D10"]},
    "flujos_etf_diarios": {"tipo_acceso": "GRATUITO_CON_REGISTRO", "requiere_clave": True, "dimensiones": ["D10"],
                           "proveedor": "Proveedor de flujos de ETF (ilustrativo)",
                           "degradacion": "D10 en P1 con fuentes semanales públicas"},
    "fundamentales_pago": {"tipo_acceso": "DE_PAGO_FUTURO", "requiere_clave": True, "dimensiones": ["D8"],
                           "proveedor": "Proveedor de fundamentales de pago (desactivado)",
                           "degradacion": "fundamentales de las cuentas publicadas"},
}
_ALIAS = re.compile(r"^[a-z0-9][a-z0-9\-]{2,40}$")


class CredencialNoDisponible(KeyError):
    pass


class Boveda:
    def __init__(self, ruta: Optional[str] = None) -> None:
        self._ruta = Path(ruta) if ruta else None
        self._claves: Dict[str, str] = {}
        if self._ruta and self._ruta.exists():
            modo = stat.S_IMODE(self._ruta.stat().st_mode)
            if modo & 0o077:
                raise PermissionError(f"La bóveda {self._ruta} debe tener permisos 600")
            self._claves = json.loads(self._ruta.read_text(encoding="utf-8"))

    def _clave(self, alias: str) -> Optional[str]:
        if not _ALIAS.match(alias or ""):
            raise ValueError("Alias de credencial no válido")
        return self._claves.get(alias) or os.environ.get("BLOQUE_B_BOVEDA_" + alias.upper().replace("-", "_"))

    def depositar(self, alias: str, clave: str) -> None:
        """Canal seguro del Broker (fuera de los contratos): solo para pruebas y para el operador."""
        if self._ruta is None:
            raise RuntimeError("Bóveda sin archivo: use variables de entorno")
        self._claves[alias] = clave
        self._ruta.write_text(json.dumps(self._claves), encoding="utf-8")
        os.chmod(self._ruta, 0o600)

    def disponible(self, alias: Optional[str]) -> bool:
        return bool(alias) and self._clave(alias) is not None

    def usar(self, alias: str, conector: Callable[[str], object]):
        """Invoca `conector(clave)` en la capa de ejecución; la clave no sale de aquí ni se devuelve."""
        clave = self._clave(alias)
        if clave is None:
            raise CredencialNoDisponible(alias)
        return conector(clave)

    def estado(self) -> Dict[str, Dict]:
        """Solo estados y alias, nunca claves (lo que ve el Coordinador)."""
        out = {}
        for nombre, c in CONECTORES.items():
            alias = f"alias-{nombre.replace('_', '-')}"
            out[nombre] = {"tipo_acceso": c["tipo_acceso"], "requiere_clave": c["requiere_clave"],
                           "credencial_ref": alias if c["requiere_clave"] else None,
                           "estado": ("ACTIVO" if not c["requiere_clave"] else
                                      "DESACTIVADO_PAGO" if c["tipo_acceso"] == "DE_PAGO_FUTURO" else
                                      ("PROVISTA_EN_BOVEDA" if self.disponible(alias) else "SIN_CREDENCIAL"))}
        return out
