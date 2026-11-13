"""QA r03 de T-106 · Huecos de `Motor._error_de_forma` (H-15): peticiones mal formadas que la r03 no mira.

Cada petición debe acabar en RECHAZADO (sin excepción al llamador) con exactamente una entrada nueva en RC, y el almacén
debe seguir íntegro. Se prueban, sobre una ficha servible (MON-YLD-001) y sobre una que no se sirve (una DOCUMENTADO):
  - `plan` no hashable (lista, dict) o de otro tipo;
  - `parametros` con claves de tipos mezclados (int y str) o no textuales;
  - `perfil`, `clase` o `semilla` con claves mezcladas o tipos raros;
  - `datos` con `valores` de claves mezcladas, `serie` con `inicio`/`fin`/`alias`/`rol` de tipos raros, `fecha_corte` con
    zona horaria frente a un `fin` sin ella;
  - `operacion` como dict con `ficha_id` de texto y claves de más (debe servirse igual que con la operación en texto).
Y, como regresión, que las formas válidas que usan los ciclos (operación en texto o en dict, sin `plan`, `plan` explícito,
`fecha_corte` como fecha, datos con serie) no se rechazan por forma.

Uso: .venv/bin/python -I -B .docs/tickets/T-106/revisores/r03_02_forma.py [RAIZ]
"""
from __future__ import annotations

import datetime as dt
import shutil
import sys
import tempfile
import warnings
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

M = C.preparar(sys.argv[1] if len(sys.argv) > 1 else None)
S = M["servicio"]
warnings.simplefilter("ignore")
TMP = Path(tempfile.mkdtemp(prefix="qa_r03_t106_forma_"))


class ProveedorSeries(C.Proveedor):
    """Proveedor con una serie diaria «X» (para los casos con `serie`)."""
    nombre = "qa_r03"

    def cierres(self, serie, inicio=None, fin=None):
        if serie != "X":
            raise KeyError(serie)
        idx = pd.bdate_range("2020-01-01", "2026-11-10")
        s = pd.Series(range(1, len(idx) + 1), index=idx, dtype=float)
        if inicio is not None:
            s = s[s.index >= pd.Timestamp(inicio)]
        if fin is not None:
            s = s[s.index <= pd.Timestamp(fin)]
        if s.empty:
            raise KeyError(f"{serie} vacía")
        return s


MO = S.Motor(M["Almacen"](TMP / "a"), ProveedorSeries(), M["cargar_config"]())
DAT = S.CASOS_CONTROL["MON-YLD-001"][0]["datos"]
PAR = dict(S.CASOS_CONTROL["MON-YLD-001"][0].get("parametros") or {})
DOC = sorted(f for f in S.FICHAS_CATALOGO if f not in S.IMPLEMENTADAS)[0]   # una ficha del Catálogo sin código


def probar(nombre, pet):
    n = len(MO.almacen.leer("RC"))
    try:
        r = MO.servir(pet, "AG-21")
    except Exception as exc:  # noqa: BLE001
        return C.informe(f"{nombre}: RECHAZADO en RC, sin excepción", False,
                         f"excepción {type(exc).__name__}: {str(exc)[:100]} · entradas nuevas en RC: {len(MO.almacen.leer('RC')) - n}")
    nuevas = len(MO.almacen.leer("RC")) - n
    return C.informe(f"{nombre}: RECHAZADO en RC, sin excepción", r["estado"] == "RECHAZADO" and nuevas == 1,
                     f"{r['estado']} {r.get('motivo', '')} · entradas nuevas en RC: {nuevas}")


base = {"operacion": "MON-YLD-001", "datos": DAT, "parametros": PAR, "fecha_corte": "2026-11-12"}
MALAS = {
    "plan = ['PLAN_MIN'] (lista)": {**base, "plan": ["PLAN_MIN"]},
    "plan = {'PLAN_MIN': 1} (dict)": {**base, "plan": {"PLAN_MIN": 1}},
    "parametros con claves int y str": {**base, "parametros": {**PAR, "x": 1, 1: "x"}},
    "parametros con clave tupla": {**base, "parametros": {**PAR, ("a", "b"): 1}},
    "parametros con clave None y str": {**base, "parametros": {**PAR, "x": 1, None: 1}},
    "perfil = {1: 'a', 'b': 2}": {**base, "perfil": {1: "a", "b": 2}},
    "clase = {1: 'a', 'b': 2}": {**base, "clase": {1: "a", "b": 2}},
    "valores con claves int y str": {**base, "datos": [{"valores": {**DAT[0]["valores"], 7: 1}}]},
    "serie con inicio = {'a': 1}": {**base, "datos": [{"serie": "X", "inicio": {"a": 1}}]},
    "serie con fin = [1]": {**base, "datos": [{"serie": "X", "fin": [1]}]},
    "serie con alias = ['a']": {**base, "datos": [{"serie": "X", "alias": ["a"]}]},
    "serie con rol = {'r': 1}": {**base, "datos": [{"serie": "X", "rol": {"r": 1}}]},
    "fecha_corte con zona horaria y serie sin ella": {**base, "datos": [{"serie": "X", "fin": "2026-11-01"}],
                                                      "fecha_corte": "2026-11-12T00:00:00+01:00"},
    "serie desconocida": {**base, "datos": [{"serie": "NO_EXISTE"}]},
    "fecha_corte = True": {**base, "fecha_corte": True},
    "fecha_corte = 1e30": {**base, "fecha_corte": 1e30},
}
for nombre, pet in MALAS.items():
    probar(f"ficha servible · {nombre}", pet)
for nombre in ("plan = ['PLAN_MIN'] (lista)", "parametros con claves int y str", "perfil = {1: 'a', 'b': 2}"):
    probar(f"ficha no servible ({DOC}) · {nombre}", {**MALAS[nombre], "operacion": DOC})

# integridad del almacén tras todo lo anterior
try:
    ok = MO.almacen.verificar_integridad() if hasattr(MO.almacen, "verificar_integridad") else None
    C.informe("el almacén sigue íntegro tras las peticiones mal formadas", ok is None or bool(ok) is True or ok == [] or
              (isinstance(ok, dict) and not any(ok.values())), str(ok)[:200])
except Exception as exc:  # noqa: BLE001
    C.informe("el almacén sigue íntegro tras las peticiones mal formadas", False, f"{type(exc).__name__}: {exc}"[:200])

# ------------------------------------------------------------------ regresión: formas válidas no se rechazan por forma
VALIDAS = {
    "operación en texto, sin plan": base,
    "operación en dict con claves de más": {**base, "operacion": {"ficha_id": "MON-YLD-001", "version": "1.0", "method_id": "x"}},
    "plan explícito PLAN_MIN": {**base, "plan": "PLAN_MIN"},
    "fecha_corte como date": {**base, "fecha_corte": dt.date(2026, 11, 12)},
    "fecha_corte como Timestamp": {**base, "fecha_corte": pd.Timestamp("2026-11-12")},
    "sin fecha_corte": {k: v for k, v in base.items() if k != "fecha_corte"},
    "parametros = None": {**base, "parametros": None},
    "datos con una serie además de los valores": {**base, "datos": [*DAT, {"serie": "X", "inicio": "2025-01-01", "fin": "2026-11-01"}]},
}
estado0 = None
for nombre, pet in VALIDAS.items():
    try:
        r = MO.servir(pet, "AG-21")
        mal = r["estado"] == "RECHAZADO" and "mal formada" in r.get("detalle", "")
        C.informe(f"forma válida · {nombre}: no se rechaza por forma", not mal, f"{r['estado']} {r.get('detalle', '')[:80]}")
    except Exception as exc:  # noqa: BLE001
        C.informe(f"forma válida · {nombre}: no se rechaza por forma", False, f"excepción {type(exc).__name__}: {exc}"[:120])
planes = sorted(S.parametro(MO.cfg, "uc.motor_por_plan")) if hasattr(S, "parametro") else []
for plan in planes:
    r = MO.servir({**base, "plan": plan}, "AG-21")
    C.informe(f"plan configurado {plan}: se acepta", r["estado"] != "RECHAZADO", r["estado"])

shutil.rmtree(TMP, ignore_errors=True)
sys.exit(C.resumen())
