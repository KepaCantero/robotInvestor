"""Utilidades comunes de los scripts de ataque r01 (QA r01 de T-99). No escriben nunca en el registro del repositorio.

Uso: python3 -I r01_NN_….py <raíz del repositorio o del worktree>   (por defecto, la raíz que contiene este fichero)
"""
import json
import sys
import tempfile
from pathlib import Path

RAIZ = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / ".docs" / "scripts"))
import registro_experimentos as rx  # noqa: E402

REGISTRO_REPO = RAIZ / ".docs" / "experimentos" / "registro.jsonl"
AHORA = "2026-11-12T10:00:00+00:00"
DESPUES = "2026-11-12T11:00:00+00:00"
ANTES = "2026-11-12T09:00:00+00:00"
_resultados = []


def pre(**cambios):
    d = {"hipotesis": "Quitar la segunda pasada no empeora la calidad", "objeto": "RECORTE",
         "metrica": "exceso frente a la cesta de la clase", "datos": "backtest simulado",
         "desde": "2026-03-06", "hasta": "2026-05-29", "semilla": 7,
         "criterio_exito": "rango del 90 % por encima de cero", "max_variantes": 2}
    d.update(cambios)
    return d


def registro_temporal():
    d = Path(tempfile.mkdtemp(prefix="r01_t99_"))
    return rx.Registro(d / "registro.jsonl")


def caso(nombre, esperado_ok, detalle=""):
    """esperado_ok=True: el registro se comporta como pide el plan; False: hallazgo."""
    _resultados.append((nombre, esperado_ok))
    print(f"[{'OK' if esperado_ok else 'HALLAZGO'}] {nombre}" + (f" · {detalle}" if detalle else ""))


def lanza(f, *exc):
    try:
        f()
    except exc or (Exception,) as e:
        return e
    return None


def lineas(reg):
    return reg.ruta.read_text(encoding="utf-8").splitlines()


def escribir(reg, ls, final="\n"):
    reg.ruta.write_text("\n".join(ls) + final, encoding="utf-8")


def recadenar(objs):
    """Recalcula toda la cadena: lo que puede hacer cualquiera, porque no hay secreto ni ancla externa."""
    prev, out = "0" * 64, []
    for i, e in enumerate(objs, 1):
        e = {k: v for k, v in e.items() if k != "_hash"}
        e["_seq"], e["_hash_prev"] = i, prev
        e["_hash"] = rx.huella(e)
        prev = e["_hash"]
        out.append(json.dumps(e, ensure_ascii=False, sort_keys=True))
    return out


def fin():
    assert not REGISTRO_REPO.exists(), "un script de ataque escribió en el registro del repositorio"
    ok = sum(1 for _, x in _resultados if x)
    print(f"\n{ok}/{len(_resultados)} como pide el plan; {len(_resultados) - ok} hallazgo(s)")
