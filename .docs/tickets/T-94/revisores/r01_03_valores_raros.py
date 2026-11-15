"""QA r01 de T-94 · Valores límite y tipos raros en datos, selecciones y parámetros. ¿Falla cerrado el banco?

Cada sonda dice qué hace el banco; «FALLO» marca lo que no se detiene con BancoError ni queda fuera de la media
y en cambio produce un número (NaN, inf) o un veredicto sin avisar.
Uso: .venv/bin/python -B .docs/tickets/T-94/revisores/r01_03_valores_raros.py [<carpeta de banco_medida.py>]"""
import json
import math
import sys
import tempfile
from pathlib import Path

import pandas as pd

sys.dont_write_bytecode = True
CARPETA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3] / "scripts"
sys.path.insert(0, str(CARPETA))
import banco_medida as bm

fallos = []


def ok(cond, msg):
    print(("OK   " if cond else "FALLO ") + msg)
    if not cond:
        fallos.append(msg)


def serie(v, inicio="2026-01-01"):
    return pd.Series([float(x) for x in v], index=pd.date_range(inicio, periods=len(v), freq="D"))


U = pd.DataFrame({"simbolo": ["X", "Y", "Z"], "clase": ["C1"] * 3})
SEL = [{"fecha_asof": "2026-01-01", "clase": "C1", "simbolo": "X", "direccion": "LARGO", "horizonte": "H"}]
FIN = lambda ini, h: pd.Timestamp(ini) + pd.Timedelta(days=2)


def probar(nombre, precios, sel=SEL, universo=U):
    try:
        r = bm.evaluar(sel, precios, universo, FIN)
    except bm.BancoError as e:
        return f"BancoError: {e}"
    except Exception as e:  # noqa: BLE001
        return f"{type(e).__name__}: {e}"
    return r


def numero_finito_o_sin_resolver(r):
    if isinstance(r, str):
        return r.startswith("BancoError")
    return all((not f["resuelta"] and f["exceso"] is None) or (f["resuelta"] and math.isfinite(f["exceso"])) for f in r)


base = {"X": serie([100, 110, 121]), "Y": serie([100, 100, 100]), "Z": serie([100, 90, 81])}

# NaN en el precio del propio símbolo al final
p = dict(base, X=serie([100, 110, float("nan")]))
r = probar("nan final", p); print("   NaN final en X →", r)
ok(numero_finito_o_sin_resolver(r), "NaN en el cierre final del símbolo: se detiene o queda sin resolver")

# NaN en un miembro de la cesta: envenena el exceso de toda la clase
p = dict(base, Y=serie([100, 100, float("nan")]))
r = probar("nan cesta", p); print("   NaN final en Y (cesta) →", r)
ok(numero_finito_o_sin_resolver(r), "NaN en un miembro de la cesta: se detiene o queda sin resolver")

# infinito
p = dict(base, Z=serie([100, 90, float("inf")]))
r = probar("inf", p); print("   inf en Z →", r)
ok(numero_finito_o_sin_resolver(r), "inf en un miembro de la cesta: se detiene o queda sin resolver")

# precio final negativo o cero (dato imposible)
p = dict(base, X=serie([100, 110, -5]))
r = probar("negativo", p); print("   cierre final negativo en X →", r)
ok(numero_finito_o_sin_resolver(r) and (isinstance(r, str) or not r[0]["resuelta"]), "cierre final negativo: no se puntúa")

# La propagación al informe: ¿JSON válido?
p = dict(base, Y=serie([100, 100, float("nan")]))
ev = bm.evaluar(SEL * 5, p, U, FIN)
inf = bm.construir_informe({"titular": ev, "azar": ev}, {"llamadas": 0, "tokens_entrada": 0, "tokens_salida": 0,
                                                       "coste_estimado": None}, 100, 1, None, "h")
txt = json.dumps(inf, ensure_ascii=False, sort_keys=True)
print("   informe con NaN:", inf["contendientes"]["titular"], inf["comparaciones"])
ok("NaN" not in txt, "el informe.json no lleva NaN (JSON estricto) ni un veredicto calculado sobre NaN")
try:
    json.loads(txt, parse_constant=lambda c: (_ for _ in ()).throw(ValueError(c)))
    ok(True, "informe.json es JSON estricto")
except ValueError as e:
    ok(False, f"informe.json no es JSON estricto ({e})")

# CSV con un cierre vacío → NaN que entra sin aviso
with tempfile.TemporaryDirectory() as t:
    Path(t, "Q.csv").write_text("fecha,cierre\n2026-01-01,100\n2026-01-02,\n2026-01-03,105\n", encoding="utf-8")
    try:
        s = bm.cargar_precios(Path(t), ["Q"])["Q"]
        ok(not s.isna().any(), f"cargar_precios rechaza o avisa un cierre vacío (cargó {list(s.values)})")
    except bm.BancoError as e:
        ok(True, f"cargar_precios rechaza un cierre vacío: {e}")
    Path(t, "R.csv").write_text("fecha,cierre\n2026-01-01,100\n2026-01-02,abc\n", encoding="utf-8")
    try:
        bm.cargar_precios(Path(t), ["R"])
        ok(False, "cargar_precios con texto en «cierre» no falla")
    except bm.BancoError as e:
        ok(True, f"cierre no numérico → BancoError: {e}")
    except Exception as e:  # noqa: BLE001
        ok(False, f"cierre no numérico → {type(e).__name__} en vez de BancoError (no «se detiene con el motivo»)")
    Path(t, "T.csv").write_text("date,close\n2026-01-01,100\n", encoding="utf-8")
    try:
        bm.cargar_precios(Path(t), ["T"])
        ok(False, "columnas ajenas no fallan")
    except bm.BancoError:
        ok(True, "columnas ajenas → BancoError")
    except Exception as e:  # noqa: BLE001
        ok(False, f"columnas ajenas → {type(e).__name__} en vez de BancoError")

# Clase de la selección ausente del universo: ¿se detiene o se pierde en silencio?
sel = [dict(SEL[0], clase="NOEXISTE")]
r = probar("clase", base, sel); print("   clase ajena al universo →", r)
ok(isinstance(r, str) and r.startswith("BancoError"), "selección de una clase que no está en el universo: se detiene con motivo")

# Símbolo que no pertenece a la clase de la selección (se compara con la cesta equivocada)
U2 = pd.DataFrame({"simbolo": ["X", "Y", "Z", "W"], "clase": ["C1", "C1", "C1", "C2"]})
p = dict(base, W=serie([50, 50, 50]))
sel = [dict(SEL[0], simbolo="W")]
r = probar("clase cruzada", p, sel, U2); print("   W (C2) seleccionado como C1 →", r if isinstance(r, str) else r[0])
ok(isinstance(r, str), "símbolo de otra clase evaluado contra una cesta que no es la suya: se detiene con motivo")

# Dirección desconocida o en minúsculas
r = probar("minusculas", base, [dict(SEL[0], direccion="largo")]); print("   dirección «largo» →", r[0] if not isinstance(r, str) else r)
ok(isinstance(r, str), "dirección desconocida («largo»): se detiene con motivo en vez de quedar sin resolver en silencio")

# Lista vacía de selecciones
try:
    inf = bm.construir_informe({"titular": [], "azar": []}, {"llamadas": 0, "tokens_entrada": 0, "tokens_salida": 0,
                                                            "coste_estimado": None}, 100, 1, None, "h")
    print("   titular sin selecciones →", inf["comparaciones"])
    ok(inf["comparaciones"]["titular_vs_azar"]["veredicto"] == "sin datos", "titular sin selecciones → «sin datos»")
except Exception as e:  # noqa: BLE001
    ok(False, f"titular sin selecciones → {type(e).__name__}: {e}")

# Parámetros: remuestreos 0 / negativos, ventana 0 / negativa
for rem in (0, -5):
    try:
        bm.resumen([0.1, 0.2], rem, 1)
        ok(False, f"remuestreos={rem} aceptado")
    except bm.BancoError:
        ok(True, f"remuestreos={rem} → BancoError")
    except Exception as e:  # noqa: BLE001
        ok(False, f"remuestreos={rem} → {type(e).__name__} (no valida el argumento)")
plantilla = [{"fecha_asof": "2026-01-03", "clase": "C1", "simbolo": "?", "direccion": "LARGO", "horizonte": "H"}]
for v in (0, -2):
    try:
        out = bm.momento(plantilla, U, base, v)
        ok(False, f"ventana={v} aceptada sin validar (eligió {[o['simbolo'] for o in out]})")
    except bm.BancoError:
        ok(True, f"ventana={v} → BancoError")

# Índice con zona horaria
p = {k: v.tz_localize("UTC") for k, v in base.items()}
r = probar("tz", p); print("   índice con zona horaria →", r if isinstance(r, str) else r[0]["resuelta"])
ok(not isinstance(r, str) or r.startswith("BancoError"), "índice con zona horaria: resuelve o BancoError (no TypeError)")

print(f"\n{len(fallos)} fallo(s)")
for f in fallos:
    print(" -", f)
sys.exit(1 if fallos else 0)
