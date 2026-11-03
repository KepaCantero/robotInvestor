"""Utilidades comunes de las pruebas del ejecutor del Bloque B.

Las pruebas NO dependen del contenido de los system prompts (se redactan en paralelo): cada entorno de prueba apunta
`rutas.prompts` a una carpeta temporal vacía, de modo que el catálogo usa el marcador declarado del cliente simulado.
Las pruebas de búsqueda de prompts crean sus propios archivos ficticios.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

DIR_EJECUTOR = Path(__file__).resolve().parents[1]
if str(DIR_EJECUTOR) not in sys.path:
    sys.path.insert(0, str(DIR_EJECUTOR))

from bloque_b.configuracion import cargar_ambitos, cargar_config, fusionar  # noqa: E402
from bloque_b.entorno import Entorno  # noqa: E402
from bloque_b.orquestacion import Coordinador  # noqa: E402

AS_OF = "2026-11-03"
PETICION_REDES = DIR_EJECUTOR / "ejemplos" / "peticiones" / "peticion_redes_bloque_a.json"


def peticion_redes(**cambios):
    p = json.loads(PETICION_REDES.read_text(encoding="utf-8"))
    for k, v in cambios.items():
        p[k] = v
    return p


def peticion_ambito(clave: str, nivel: str = "N2", **cambios):
    a = cargar_ambitos(cargar_config())[clave]
    p = {"origen": "LIBRE", "objeto": {"descripcion": a["nombre"], "clave_universo": clave},
         "tipos_activo_admitidos": a.get("tipos_activo"), "horizontes": [a.get("horizonte", "H3")], "nivel": nivel}
    p.update(cambios)
    return p


@pytest.fixture(scope="session")
def dir_prompts_vacio(tmp_path_factory):
    return tmp_path_factory.mktemp("prompts_vacios")


@pytest.fixture
def hacer_cfg(dir_prompts_vacio):
    def _cfg(**extra):
        base = {"rutas": {"prompts": str(dir_prompts_vacio)}}
        return cargar_config(extra=fusionar(base, extra))
    return _cfg


@pytest.fixture
def hacer_entorno(tmp_path, hacer_cfg):
    """Fábrica de entornos aislados (estado y salida en tmp_path; fecha de corte fija)."""
    contador = {"n": 0}

    def _ent(cfg=None, as_of=AS_OF, nombre=None, **kw):
        contador["n"] += 1
        n = nombre or f"e{contador['n']}"
        return Entorno(cfg or hacer_cfg(), estado=str(tmp_path / n / "estado"), salida=str(tmp_path / n / "salida"),
                       as_of=as_of, **kw)
    return _ent


@pytest.fixture
def rapido(hacer_cfg):
    """Configuración con reloj simulado rápido (sin puerta de tiempo en N2)."""
    return hacer_cfg(reloj={"factor_simulado": 0.3})


@pytest.fixture(scope="session")
def entrega_redes(tmp_path_factory):
    """Una entrega completa (redes eléctricas, N2, sin pausa) compartida por las pruebas de solo lectura."""
    d = tmp_path_factory.mktemp("entrega_redes")
    (d / "prompts").mkdir()
    cfg = cargar_config(extra={"rutas": {"prompts": str(d / "prompts")}, "reloj": {"factor_simulado": 0.3}})
    ent = Entorno(cfg, estado=str(d / "estado"), salida=str(d / "salida"), as_of=AS_OF)
    coord = Coordinador(ent)
    res = coord.recibir(peticion_redes())
    assert res.get("estado_peticion") == "ENTREGADA", res
    return {"ent": ent, "coord": coord, "res": res, "dir": d}


def copia(o):
    return copy.deepcopy(o)
