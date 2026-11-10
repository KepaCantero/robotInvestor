"""QA r01 de T-90 · utilidades comunes de las sondas (entorno aislado, igual que tests/conftest.py).

Uso: importado por las sondas r01_*.py. Necesita la raíz del ejecutor de B en RI_EJECUTOR_B (por defecto, la del repo
que contiene este archivo), para poder ejecutarse también sobre una copia limpia (git worktree).
"""
import json
import os
import sys
import tempfile
from pathlib import Path

RAIZ = Path(os.environ.get("RI_EJECUTOR_B") or Path(__file__).resolve().parents[4] / "bloque_b" / "11_Ejecutor")
sys.path.insert(0, str(RAIZ))

from bloque_b import mock_respuestas as mr  # noqa: E402
from bloque_b.configuracion import cargar_config  # noqa: E402
from bloque_b.entorno import Entorno  # noqa: E402
from bloque_b.orquestacion import Coordinador  # noqa: E402

AS_OF = "2026-11-03"
PETICION = RAIZ / "ejemplos" / "peticiones" / "peticion_redes_bloque_a.json"
MARCA = "SONDA-T90"


def ejecutar(extra_por_dim, as_of=AS_OF):
    """Ejecuta una petición completa añadiendo a cada dimensión las notas de extra_por_dim[dim]."""
    orig = dict(mr._TAREAS)

    def envolver(f):
        def g(msg, ctx, r):
            out = f(msg, ctx, r)
            for inf in out.get("dim_informes") or []:
                for n in extra_por_dim.get(inf["dim"], []):
                    inf["notas"].append(json.loads(json.dumps(n)))
            return out
        return g

    for k, f in list(mr._TAREAS.items()):
        if k[1] in ("informe_dimensional", "cobertura_dimensiones"):
            mr._TAREAS[k] = envolver(f)
    try:
        d = Path(tempfile.mkdtemp(prefix="t90_qa_"))
        (d / "prompts").mkdir()
        cfg = cargar_config(extra={"rutas": {"prompts": str(d / "prompts")}, "reloj": {"factor_simulado": 0.3}})
        ent = Entorno(cfg, estado=str(d / "estado"), salida=str(d / "salida"), as_of=as_of)
        res = Coordinador(ent).recibir(json.loads(PETICION.read_text(encoding="utf-8")))
    finally:
        mr._TAREAS.clear()
        mr._TAREAS.update(orig)
    out = {"res": res, "ent": ent}
    if res.get("estado_peticion") == "ENTREGADA":
        e = res["entregables"]
        out["paquete"] = json.loads(Path(e["paquete_json"]).read_text(encoding="utf-8"))
        out["tecnico"] = Path(e["informe_tecnico"]).read_text(encoding="utf-8")
        out["visual"] = Path(e["informe_visual"]).read_text(encoding="utf-8")
        out["memo"] = Path(e["memorando"]).read_text(encoding="utf-8")
    out["claims"] = [x for x in ent.alm.leer("F2") if x.get("tipo_entrada") == "CLM"]
    out["g3"] = [x for x in ent.alm.leer("HA") if x.get("tipo_entrada") == "G3V"]
    return out


def nota(texto, fechas=None, **campos):
    n = {"afirmacion": f"{MARCA} {texto}", "etiqueta": "[INTERPRETACIÓN]", "contiene_cifra": False}
    if fechas is not None:
        n["fechas"] = fechas
    n.update(campos)
    return n


def f3(a, b, c):
    return {"fecha_fenomeno": a, "fecha_publicacion": b, "conocible_desde": c}


def marcas_en_f2(o):
    return sorted(c["afirmacion"] for c in o["claims"] if MARCA in c["afirmacion"])


def marcas_en_paquete(o):
    return sorted(n["afirmacion"] for d in o["paquete"]["dimensiones"] for n in d["notas"] if MARCA in n["afirmacion"])
