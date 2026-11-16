"""T-133 QA r02 · `verificar` con avisos (banco 0.5.0, r02 H-02 y H-03).

Se ejecuta con el banco de un WORKTREE y RI_AGENTE=qa-r02-t133: el registro por defecto cae en <worktree>/.docs/experimentos,
nunca en el del repositorio principal, y se borra al final. Titular falso y datos en un temporal.
1. Carpeta copiada a otra profundidad: código 0, el aviso sale por stderr y no cuenta como problema.
2. La API sin lista de avisos (`verificar(c)`): no rompe y no dice nada del registro citado; con lista, un aviso.
3. Aviso y problema a la vez (copia con informe.md tocado): código 2 y los dos se ven.
4. experimento.json sin la clave «registro» (ya solo informa): ¿problema o aviso?
5. experimento.json que cita un registro fabricado con el mismo exp_id e intento: sin --registro no pasa.
6. Salida de la línea de órdenes con solo avisos: ¿dice «verificado»?
Uso: .venv/bin/python -B r02_03_verificar_avisos.py <carpeta de banco_medida.py de un worktree>"""
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

os.environ["RI_AGENTE"] = "qa-r02-t133"
sys.dont_write_bytecode = True
CARPETA = Path(sys.argv[1]).resolve()
if CARPETA == Path(__file__).resolve().parents[5] / ".docs" / "scripts":
    sys.exit("me niego: pásame el banco de un worktree (el registro por defecto caería en el repositorio principal)")
sys.path.insert(0, str(CARPETA))
import banco_medida as bm
import registro_experimentos as rx

REG = Path(rx.REGISTRO_DEFECTO)
_s = rx.Registro(REG, ancla_git=False).sello
for _f in [REG, *_s.parent.glob(_s.name.rsplit(".", 1)[0] + "*")]:   # restos de una ejecución anterior
    _f.unlink(missing_ok=True)
assert str(REG).startswith(str(CARPETA.parents[1])), REG
fallos = []


def ok(cond, msg):
    print(("OK   " if cond else "FALLO ") + msg, flush=True)
    if not cond:
        fallos.append(msg)


TMP = Path(tempfile.mkdtemp(prefix="r02_t133_verificar_"))
datos = TMP / "datos"
datos.mkdir()
fechas = pd.bdate_range("2024-01-01", "2026-06-30")
rng = np.random.default_rng(13)
sims = [f"S{i}" for i in range(8)]
for s in sims:
    pd.DataFrame({"fecha": fechas.strftime("%Y-%m-%d"),
                  "cierre": 100 * np.exp(np.cumsum(rng.normal(0, 0.01, len(fechas))))}).to_csv(datos / f"{s}.csv", index=False)
universo = TMP / "universo.csv"
pd.DataFrame({"simbolo": sims, "clase": ["C"] * 8}).to_csv(universo, index=False)
bm.rutas_por_defecto = lambda: (datos, universo)
cortes = [d.strftime("%Y-%m-%d") for d in pd.date_range("2025-03-07", periods=13, freq="7D")]
bm.titular_a = lambda *a, **k: {
    "selecciones": [{"fecha_asof": c, "clase": "C", "simbolo": s, "direccion": "LARGO", "horizonte": "H"} for c in cortes
                    for s in ("S1", "S4")],
    "consumo": {"llamadas": 1, "tokens_entrada": 1, "tokens_salida": 1, "coste_estimado": None},
    "datos": datos, "universo": universo, "fecha_fin": lambda ini, h: ini + pd.DateOffset(months=6),
    "advertencias": [], "excluidos_contaminacion": 0}


def cli(*args):
    err, out = io.StringIO(), io.StringIO()
    with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out):
        cod = bm.main(list(map(str, args)))
    return cod, out.getvalue().strip(), [x for x in err.getvalue().splitlines() if x.strip()]


try:
    cod, _, err = cli("a", "--desde", "2025-03-07", "--hasta", "2025-05-30", "--salida", TMP / "s", "--remuestreos", "200")
    ok(cod == 0, f"`a` con el registro por defecto del worktree ({err[-1:] if cod else ''})")
    c = TMP / "s"
    honda = TMP / "evidencia" / "a" / "b" / "s"
    shutil.copytree(c, honda)
    cod, out, err = cli("verificar", honda)
    ok(cod == 0 and any("aviso" in x for x in err) and not any(x.startswith("- ") for x in err),
       f"1. copia a otra profundidad: código {cod}, salida «{out}», stderr {err}")
    ok(bm.verificar(honda) == [], "2. la API sin lista de avisos da [] (el registro citado no se dice)")
    av = []
    ok(bm.verificar(honda, None, av) == [] and len(av) == 1, f"2b. con lista: 0 problemas y 1 aviso ({av})")
    (honda / "informe.md").write_text((honda / "informe.md").read_text(encoding="utf-8") + "x", encoding="utf-8")
    cod, out, err = cli("verificar", honda)
    ok(cod == 2 and any("aviso" in x for x in err) and any(x.startswith("- ") for x in err),
       f"3. aviso y problema a la vez: código {cod}, stderr {err}")
    sin = TMP / "sin_registro"
    shutil.copytree(c, sin)
    e = json.loads((sin / "experimento.json").read_text(encoding="utf-8"))
    del e["registro"]
    (sin / "experimento.json").write_text(json.dumps(e), encoding="utf-8")
    p = bm.verificar(sin)
    print(f"   4. experimento.json sin «registro»: {p}")
    falso = TMP / "falso.jsonl"
    rf = rx.Registro(falso, ancla_git=False)
    pre = rf.prerregistrar({"hipotesis": "hipótesis fabricada", "objeto": "BLOQUE", "metrica": "métrica fabricada",
                            "datos": "datos fabricados", "desde": "2025-01-01", "hasta": "2025-02-01", "semilla": 1,
                            "criterio_exito": "criterio fabricado", "max_variantes": 1}, autor="falso")
    print(f"   5. registro fabricado: {pre['exp_id']}")
    fab = TMP / "fabricada"
    shutil.copytree(c, fab)
    e = json.loads((fab / "experimento.json").read_text(encoding="utf-8"))
    e["registro"] = os.path.relpath(falso, fab)
    (fab / "experimento.json").write_text(json.dumps(e), encoding="utf-8")
    av = []
    ok(bm.verificar(fab, None, av) == [] and av, f"5. la carpeta auténtica que cita un registro fabricado se verifica contra el "
                                                 f"del agente: pasa con aviso ({av})")
finally:
    sello = rx.Registro(REG, ancla_git=False).sello   # en la carpeta git del worktree (o junto al registro)
    for f in [REG, *sello.parent.glob(sello.name.rsplit(".", 1)[0] + "*")]:
        f.unlink(missing_ok=True)
    shutil.rmtree(TMP, ignore_errors=True)
print(f"\n{len(fallos)} fallo(s)")
for f in fallos:
    print(" - " + f)
sys.exit(1 if fallos else 0)
