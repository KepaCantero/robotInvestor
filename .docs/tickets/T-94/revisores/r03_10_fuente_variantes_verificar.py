"""QA r03 de T-94 · Experimento por fuente (H-14), variantes y `verificar` (H-15) con lo que cambió en la ronda r03.

Titular falso (se sustituye `titular_a`), datos y registros en un temporal; nunca se escribe en el repositorio.
1. La misma fuente escrita de dos formas: datos por defecto frente a `--datos` con la ruta de los datos de ejemplo de A.
2. Los mismos datos copiados a otra carpeta: ¿experimento nuevo con su variante libre (y adoptable)?
3. La misma variante otra vez (mismos parámetros, misma huella) con un titular que no es determinista (como A con un modelo
   real) o con los datos cambiados en la misma carpeta: ¿cuenta como un intento más dentro del máximo y puede dar un «mejor»
   adoptable después de un «todavía no se sabe»?
4. `experimento.json` con «dentro_del_maximo» cambiado: ¿lo ve `verificar`?
5. Un registro falso: informe.json cambiado a «mejor», informe.md regenerado, un registro nuevo con su cadena bien hecha y
   experimento.json apuntando a él: ¿lo da por bueno `verificar` sin --registro? ¿Y con el registro de verdad?
6. Ejecutar sin registro (`--registro ""`): ¿lo admite? ¿Qué dice después `verificar`?
Uso: .venv/bin/python -B .docs/tickets/T-94/revisores/r03_10_fuente_variantes_verificar.py [<carpeta de banco_medida.py>]"""
import argparse
import json
import random
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
CARPETA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3] / "scripts"
sys.path.insert(0, str(CARPETA))
import banco_medida as bm  # noqa: E402
import registro_experimentos as rx  # noqa: E402

fallos = []


def ok(cond, msg):
    print(("OK   " if cond else "FALLO ") + msg)
    if not cond:
        fallos.append(msg)


TMP = Path(tempfile.mkdtemp(prefix="r03_t94_fuente_"))
datos = TMP / "datos"
datos.mkdir()
fechas = pd.bdate_range("2023-01-02", "2026-06-30")
rng = np.random.default_rng(41)
sims = [f"S{i}" for i in range(10)]
for s in sims:
    pd.DataFrame({"fecha": fechas.strftime("%Y-%m-%d"),
                  "cierre": 100 * np.exp(np.cumsum(rng.normal(0, 0.01, len(fechas))))}).to_csv(datos / f"{s}.csv", index=False)
universo = TMP / "universo.csv"
pd.DataFrame({"simbolo": sims, "clase": ["C"] * 10}).to_csv(universo, index=False)
CORTES = pd.date_range("2024-01-05", periods=60, freq="7D")
PRECIOS = {s: pd.read_csv(datos / f"{s}.csv", index_col="fecha", parse_dates=True)["cierre"] for s in sims}
ESTADO = {"semilla_titular": 0, "habilidad": 0.0}


def titular(desde, hasta, carpeta, cliente, frecuencia, clases, **kw):
    """Titular que, con probabilidad «habilidad», elige el mejor activo de la semana (mira el futuro); si no, al azar.
    «semilla_titular» cambia de una ejecución a otra: no es determinista, como A con un modelo real."""
    r = random.Random(ESTADO["semilla_titular"])
    sel = []
    for c in CORTES:
        ret = {s: bm.rentabilidad(PRECIOS[s], c, c + pd.Timedelta(days=5)) for s in sims}
        s = max(ret, key=ret.get) if r.random() < ESTADO["habilidad"] else r.choice(sims)
        sel.append({"fecha_asof": c.strftime("%Y-%m-%d"), "clase": "C", "simbolo": s, "direccion": "LARGO", "horizonte": "H"})
    return {"selecciones": sel, "consumo": {"llamadas": 1, "tokens_entrada": 1, "tokens_salida": 1, "coste_estimado": None},
            "datos": datos, "universo": universo,   # siempre los del temporal (la fuente se decide antes, con los argumentos)
            "fecha_fin": lambda ini, h: ini + pd.Timedelta(days=5), "advertencias": [], "excluidos_contaminacion": 0}


bm.titular_a = titular


def ns(salida, registro, **kw):
    d = dict(desde="2024-01-05", hasta="2025-02-21", salida=str(TMP / salida), cliente="mock", frecuencia=None, clases=None,
             semilla=7, remuestreos=500, ventana=63, nivel=0.9, min_efectivas=10, registro=str(registro), experimento=None,
             max_variantes=1)
    d.update(kw)
    return argparse.Namespace(**d)


# 1. La misma fuente escrita de dos formas
reg = TMP / "reg1.jsonl"
ej = bm.EJECUTOR_A / "ejemplos" / "datos_sinteticos"
uj = bm.EJECUTOR_A / "config" / "universo_ejemplo.csv"
a = bm.ejecutar_a(ns("f1", reg))
b = bm.ejecutar_a(ns("f2", reg, datos=str(ej), universo=str(uj)))
print(f"   por defecto: {a['experimento']['exp_id']}; con --datos y --universo de ejemplo explícitos: {b['experimento']['exp_id']} "
      f"(dentro del máximo: {b['experimento']['dentro_del_maximo']})")
ok(a["experimento"]["exp_id"] == b["experimento"]["exp_id"],
   "los datos y el universo de ejemplo, por defecto o con su ruta, son la misma fuente (el mismo experimento)")

# 2. Los mismos datos copiados a otra carpeta
reg = TMP / "reg2.jsonl"
ESTADO.update(semilla_titular=1, habilidad=0.0)
c1 = bm.ejecutar_a(ns("c1", reg, cliente="anthropic", datos=str(datos), universo=str(universo)))
copia = TMP / "datos_copia"
shutil.copytree(datos, copia)
shutil.copy(universo, TMP / "universo_copia.csv")
c2 = bm.ejecutar_a(ns("c2", reg, cliente="anthropic", datos=str(copia), universo=str(TMP / "universo_copia.csv")))
print(f"   datos originales: {c1['experimento']['exp_id']}; la misma copia en otra carpeta: {c2['experimento']['exp_id']} "
      f"(dentro del máximo {c2['experimento']['dentro_del_maximo']}); avisos {[x for x in c2['advertencias_titular'] if 'hipótesis' in x]}")
ok(c1["experimento"]["exp_id"] == c2["experimento"]["exp_id"] or not c2["experimento"]["dentro_del_maximo"],
   "copiar los mismos datos a otra carpeta no abre un experimento nuevo con su variante libre")

# 3. La misma variante otra vez con un titular que no es determinista
reg = TMP / "reg3.jsonl"
R = rx.Registro(reg)
vistos = []
for intento in range(1, 9):
    ESTADO.update(semilla_titular=100 + intento, habilidad=0.20)
    inf = bm.ejecutar_a(ns(f"n{intento}", reg, cliente="anthropic", datos=str(datos), universo=str(universo)))
    e = inf["experimento"]
    vistos.append((e["intento"], e["dentro_del_maximo"], bm.veredicto_conjunto(inf["comparaciones"])))
res = R.resumen(e["exp_id"])
print(f"   8 ejecuciones con los mismos parámetros (titular no determinista, 20 % de habilidad): {vistos}")
print(f"   registro: variantes {res['variantes']}, fuera del máximo {res['fuera_del_maximo']}, adoptables {res['adoptables']}")
primero = vistos[0][2]
ok(not (primero != "mejor" and res["adoptables"]),
   "repetir la misma variante hasta que salga «mejor» no la hace adoptable (o cada repetición cuenta contra el máximo)")
# los datos cambiados en la misma carpeta: misma huella
reg = TMP / "reg3b.jsonl"
ESTADO.update(semilla_titular=7, habilidad=0.0)
d1 = bm.ejecutar_a(ns("d1", reg, cliente="anthropic", datos=str(datos), universo=str(universo)))
pre1 = json.loads((TMP / "d1" / "prerregistro.json").read_text(encoding="utf-8"))["huella"]
for s in sims[:3]:
    f = datos / f"{s}.csv"
    df = pd.read_csv(f, dtype=str)
    df["cierre"] = (df["cierre"].astype(float) * 1.5).map(lambda v: f"{v:.6f}")
    df.to_csv(f, index=False)
d2 = bm.ejecutar_a(ns("d2", reg, cliente="anthropic", datos=str(datos), universo=str(universo)))
pre2 = json.loads((TMP / "d2" / "prerregistro.json").read_text(encoding="utf-8"))["huella"]
print(f"   datos cambiados en la misma carpeta: huellas del prerregistro iguales {pre1 == pre2}; segundo intento dentro del "
      f"máximo {d2['experimento']['dentro_del_maximo']}")
ok(pre1 != pre2 or not d2["experimento"]["dentro_del_maximo"],
   "con otros datos en la misma carpeta, el prerregistro no es el mismo (la huella no recoge el contenido de los datos)")

# 4. experimento.json con dentro_del_maximo cambiado
reg = TMP / "reg4.jsonl"
ESTADO.update(semilla_titular=3, habilidad=0.0)
bm.ejecutar_a(ns("v1", reg, semilla=1))
bm.ejecutar_a(ns("v2", reg, semilla=2))                     # segunda variante: fuera del máximo
v = TMP / "v2"
e = json.loads((v / "experimento.json").read_text(encoding="utf-8"))
print(f"   v2: dentro del máximo {e['dentro_del_maximo']}; verificar antes: {bm.verificar(v)}")
e["dentro_del_maximo"] = True
(v / "experimento.json").write_text(json.dumps(e), encoding="utf-8")
p = bm.verificar(v)
print(f"   experimento.json con dentro_del_maximo = true: verificar → {p}")
ok(p != [], "experimento.json que dice «dentro del máximo» cuando el registro dice que no: verificar lo ve")

# 5. Registro falso
reg = TMP / "reg5.jsonl"
ESTADO.update(semilla_titular=5, habilidad=0.0)
bm.ejecutar_a(ns("w", reg))
w = TMP / "w"
pre = json.loads((w / "prerregistro.json").read_text(encoding="utf-8"))
inf = json.loads((w / "informe.json").read_text(encoding="utf-8"))
antes = {k: c["veredicto"] for k, c in inf["comparaciones"].items()}
for c in inf["comparaciones"].values():
    c.update(veredicto="mejor", motivo=None)
bm._escribir_json(w / "informe.json", inf)
(w / "informe.md").write_text(bm.informe_md(inf, bm.titulo_informe(pre["desde"], pre["hasta"])), encoding="utf-8")
falso = TMP / "otro_sitio" / "registro.jsonl"
F = rx.Registro(falso)
exp_falso = F.prerregistrar({"hipotesis": pre["hipotesis"], "objeto": "BLOQUE", "metrica": pre["metrica"], "fuente_banco": pre["fuente"],
                            "datos": "x" * 12, "desde": pre["desde"], "hasta": pre["hasta"], "semilla": pre["semilla"],
                            "criterio_exito": pre["criterio"], "max_variantes": 1}, autor="banco_medida")["exp_id"]
it = F.intento(exp_falso, variante=pre["huella"][:16])
F.resultado(exp_falso, it["n"], "mejor", {"huella_informe": bm.huella(inf)})
(w / "experimento.json").write_text(json.dumps({"exp_id": exp_falso, "intento": it["n"], "dentro_del_maximo": True,
                                                "registro": str(falso)}), encoding="utf-8")
p_sin, p_con = bm.verificar(w), bm.verificar(w, reg)
print(f"   veredictos {antes} → «mejor», md regenerado y registro falso en otra carpeta: verificar sin --registro {p_sin}; "
      f"con el registro de verdad {p_con}")
ok(p_sin != [], "verificar sin --registro no da por buena una carpeta que apunta a un registro fabricado fuera del repositorio")
ok(p_con != [], "verificar con el registro de verdad ve la manipulación")

# 6. Sin registro
ESTADO.update(semilla_titular=6, habilidad=0.0)
try:
    inf = bm.ejecutar_a(ns("sin", ""))
    p = bm.verificar(TMP / "sin")
    print(f"   --registro \"\": ejecuta sin anotar el intento; experimento en el informe: {'experimento' in inf}; verificar → {p}")
    ok(p != [], "una ejecución sin registro no pasa `verificar`")
except bm.BancoError as e:
    ok(True, f"--registro vacío → BancoError: {e}")

print(f"\n{len(fallos)} fallo(s)")
for f in fallos:
    print(" -", f)
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(1 if fallos else 0)
