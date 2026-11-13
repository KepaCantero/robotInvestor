"""QA r03 de T-106 · Regresión: el ciclo del Bloque A y las demás fichas del Motor, antes y después de la r03.

1. Ciclo simulado (`--cliente mock … backtest --desde 2024-01-05 --hasta 2024-03-29`) con el ejecutor de cada raíz
   (PYTHONPATH a su `11_Ejecutor`): `senales.csv`, `pronosticos.csv` y `metricas.json` idénticos; en RC, las mismas
   entradas del CT-09 (tipo, ficha, estado, motivo y resultado), sin ninguna «petición mal formada».
2. Cada ficha con casos de control (las 21 y las anteriores que los tengan), por el Motor con los datos de cada caso:
   mismo estado y misma cifra antes y después, salvo las diferencias que la r03 introduce a propósito (MON-EXP:
   `incertidumbre_probabilidad` nueva y la limitación por redondeo; DER-VRP: `nivel_es` fuera de 0,90–0,99), que se
   listan aparte.

Uso: .venv/bin/python -I -B .docs/tickets/T-106/revisores/r03_04_regresion.py RAIZ_ANTES RAIZ_DESPUES
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

ANTES, DESPUES = (Path(a).resolve() for a in sys.argv[1:3])
PY = sys.executable
TMP = Path(tempfile.mkdtemp(prefix="qa_r03_t106_reg_"))


def entorno(raiz: Path) -> dict:
    e = {k: v for k, v in os.environ.items() if k not in ("BLOQUE_A_RAIZ", "PYTHONPATH")}
    e.update({"PYTHONPATH": str(raiz / "bloque_a" / "11_Ejecutor"), "PYTHONDONTWRITEBYTECODE": "1"})
    return e


def ciclo(raiz: Path, nombre: str) -> Path:
    ejec = raiz / "bloque_a" / "11_Ejecutor"
    salida = TMP / nombre
    cmd = [PY, "-B", "-c", "import sys; from bloque_a.cli import main; sys.exit(main())", "--cliente", "mock",
           "--datos", "ejemplos/datos_sinteticos", "--universo", "config/universo_ejemplo.csv", "--salida", str(salida),
           "backtest", "--desde", "2024-01-05", "--hasta", "2024-03-29"]
    r = subprocess.run(cmd, cwd=ejec, env=entorno(raiz), capture_output=True, text=True, timeout=3000)
    if r.returncode != 0:
        print(r.stdout[-2000:], r.stderr[-2000:])
    C.informe(f"ciclo simulado con el ejecutor de {nombre}", r.returncode == 0, (r.stderr.strip().splitlines() or [""])[-1][:120])
    return salida


def rc_ct09(salida: Path) -> list[dict]:
    filas = []
    for ruta in sorted(salida.rglob("*.jsonl")):
        for linea in ruta.read_text(encoding="utf-8").splitlines():
            try:
                e = json.loads(linea)
            except ValueError:
                continue
            if isinstance(e, dict) and e.get("contrato") == "CT-09":
                filas.append({"archivo": ruta.name, "tipo": e.get("tipo_entrada"), "ficha": (e.get("operacion") or {}).get("ficha_id"),
                              "estado": e.get("estado"), "motivo": e.get("motivo_rechazo"),
                              "resultado": json.dumps(e.get("resultado"), sort_keys=True),
                              "limitaciones": e.get("limitaciones"), "detalle": e.get("detalle")})
    return filas


sa, sd = ciclo(ANTES, "antes"), ciclo(DESPUES, "despues")
for nombre in ("senales.csv", "pronosticos.csv", "metricas.json"):
    a, d = sorted(sa.rglob(nombre)), sorted(sd.rglob(nombre))
    iguales = bool(a) and len(a) == len(d) and all(x.read_bytes() == y.read_bytes() for x, y in zip(a, d))
    C.informe(f"ciclo: {nombre} idéntico antes y después", iguales, f"{len(a)} / {len(d)} archivos")
ra, rd = rc_ct09(sa), rc_ct09(sd)
C.informe("ciclo: hay entradas CT-09 en RC (si no, la comparación no dice nada)", len(ra) > 0, f"{len(ra)}")
C.informe("ciclo: las entradas CT-09 de RC coinciden (tipo, ficha, estado, motivo, resultado, limitaciones)", ra == rd,
          f"{len(ra)} frente a {len(rd)}; primera diferencia: "
          + next((f"{x} ≠ {y}" for x, y in zip(ra, rd) if x != y), "longitudes")[:200] if ra != rd else f"{len(ra)} entradas")
mal = [x for x in rd if "mal formada" in str(x.get("detalle"))]
C.informe("ciclo: ninguna petición del ciclo se rechaza por forma", not mal, str(mal[:2])[:200])

# ------------------------------------------------------------------ 2. fichas con casos de control, antes y después
CODIGO = r'''
import json, sys, tempfile, copy
from pathlib import Path
from bloque_a.motor import servicio as S
from bloque_a.almacen import Almacen
from bloque_a.configuracion import cargar_config
class P:
    as_of = None; nombre = "qa"
    def cierres(self, *a, **k): raise KeyError("sin series")
    def huella(self, *a, **k): return "qa"
m = S.Motor(Almacen(Path(tempfile.mkdtemp())), P(), cargar_config())
out = {}
casos = S.CASOS_CONTROL
for ficha in sorted(casos):
    for i, c in enumerate(casos[ficha]):
        for extra in ({}, {"nivel_es": 0.5}, {"nivel_es": 0.999}):
            if extra and ficha != "DER-VRP-001":
                continue
            pet = {"operacion": ficha, "datos": copy.deepcopy(c.get("datos") or []), "fecha_corte": "2026-11-12",
                   "parametros": {**(c.get("parametros") or {}), **extra}}
            try:
                r = m.servir(pet, "AG-21")
                out[f"{ficha}#{i}{extra}"] = [r["estado"], r.get("resultado"), r.get("limitaciones"), r.get("motivo")]
            except Exception as e:
                out[f"{ficha}#{i}{extra}"] = ["EXCEPCION", repr(e)[:200], None, None]
print(json.dumps(out, sort_keys=True, default=str))
'''


def fichas(raiz: Path) -> dict:
    r = subprocess.run([PY, "-B", "-c", CODIGO], cwd=raiz / "bloque_a" / "11_Ejecutor", env=entorno(raiz), capture_output=True,
                       text=True, timeout=1800)
    if r.returncode != 0:
        print(r.stderr[-1500:])
        return {}
    return json.loads(r.stdout.strip().splitlines()[-1])


fa, fd = fichas(ANTES), fichas(DESPUES)
C.informe("casos de control por el Motor en las dos raíces", bool(fa) and set(fa) == set(fd), f"{len(fa)} / {len(fd)} peticiones")


def sin_r03(x):
    """Quita lo que la r03 añade a propósito en MON-EXP (incertidumbre_probabilidad y su unidad)."""
    if isinstance(x, dict):
        return {k: sin_r03(v) for k, v in x.items() if k != "incertidumbre_probabilidad"}
    if isinstance(x, list):
        return [sin_r03(v) for v in x]
    return x


distintas, a_proposito = [], []
for k in sorted(set(fa) & set(fd)):
    a, d = fa[k], fd[k]
    if a == d:
        continue
    if k.startswith("MON-EXP-001") and a[0] == d[0] and sin_r03(a[1]) == sin_r03(d[1]) or \
       k.startswith("MON-EXP-001") and sin_r03(a[1]) == sin_r03(d[1]) and d[0] == "SERVED_WITH_LIMITATIONS":
        a_proposito.append(f"{k}: {a[0]} → {d[0]} (solo incertidumbre_probabilidad y su limitación)")
    elif k.startswith("DER-VRP-001") and "nivel_es" in k and d[0] == "RECHAZADO":
        a_proposito.append(f"{k}: {a[0]} → RECHAZADO (H-20)")
    else:
        distintas.append(f"{k}: {a[0]} → {d[0]}")
C.informe("fichas con casos de control: mismo estado y misma cifra antes y después, salvo lo que la r03 cambia a propósito",
          not distintas, "; ".join(distintas[:6]))
print("      (informativo) cambios a propósito: " + "; ".join(a_proposito))
excep = [k for k, v in fd.items() if v[0] == "EXCEPCION"]
C.informe("ninguna excepción al llamador", not excep, "; ".join(excep[:4]))
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(C.resumen())
