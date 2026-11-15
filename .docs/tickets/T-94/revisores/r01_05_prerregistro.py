"""QA r01 de T-94 · Prerregistro: manipulado, posterior a mirar resultados, y el registro de experimentos (T-99) en lo que toca al banco.

Se sustituye el titular A por uno falso y rápido (monkeypatch de `titular_a`) que lee datos construidos en una carpeta temporal;
nada se escribe en el repositorio (registro y salida en un directorio temporal).
1. Seed shopping: ejecutar el banco con semillas 1..N sin --experimento. ¿Cada ejecución abre un experimento nuevo con un solo
   intento (y por tanto «dentro del máximo»), de modo que el máximo de variantes no limita nada?
2. Fallo después del titular (símbolo ausente en evaluar): ¿queda el intento sin resultado en el registro?
3. Prerregistro manipulado después de la ejecución (hipótesis cambiada y huella recalculada): ¿lo detecta algo?
4. --experimento de un experimento ajeno (otro objeto, otras fechas, otra semilla): ¿se acepta?
Uso: .venv/bin/python -B .docs/tickets/T-94/revisores/r01_05_prerregistro.py [<carpeta de banco_medida.py>]"""
import argparse
import json
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
CARPETA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3] / "scripts"
sys.path.insert(0, str(CARPETA))
import banco_medida as bm
import registro_experimentos as rx

fallos = []


def ok(cond, msg):
    print(("OK   " if cond else "FALLO ") + msg)
    if not cond:
        fallos.append(msg)


tmp = Path(tempfile.mkdtemp(prefix="r01_t94_"))
datos = tmp / "datos"
datos.mkdir()
fechas = pd.bdate_range("2024-01-01", "2026-12-31")
rng = np.random.default_rng(5)
sims = [f"S{i}" for i in range(8)]
for s in sims:
    pd.DataFrame({"fecha": fechas.strftime("%Y-%m-%d"),
                  "cierre": 100 * np.exp(np.cumsum(rng.normal(0.0002, 0.01, len(fechas))))}).to_csv(datos / f"{s}.csv", index=False)
universo = tmp / "universo.csv"
pd.DataFrame({"simbolo": sims, "clase": ["C"] * 8}).to_csv(universo, index=False)
cortes = [d.strftime("%Y-%m-%d") for d in pd.date_range("2025-03-07", periods=13, freq="7D")]


def titular_falso(simbolos):
    def f(desde, hasta, carpeta, cliente, frecuencia, clases):
        sel = [{"fecha_asof": c, "clase": "C", "simbolo": s, "direccion": "LARGO", "horizonte": "H3"} for c in cortes for s in simbolos]
        return {"selecciones": sel, "consumo": {"llamadas": 1, "tokens_entrada": 1, "tokens_salida": 1, "coste_estimado": None},
                "datos": datos, "universo": universo, "fecha_fin": lambda ini, h: ini + pd.DateOffset(months=6)}
    return f


def ns(salida, registro, semilla, experimento=None, **kw):
    d = dict(desde="2025-03-07", hasta="2025-05-30", salida=str(salida), cliente="mock", frecuencia=None, clases=None,
             semilla=semilla, remuestreos=300, ventana=63, registro=str(registro), experimento=experimento, max_variantes=1)
    d.update(kw)
    return argparse.Namespace(**d)


# 1. Seed shopping
bm.titular_a = titular_falso(["S1", "S4"])
reg = tmp / "reg.jsonl"
veredictos = {}
for semilla in range(1, 21):
    inf = bm.ejecutar_a(ns(tmp / f"s{semilla}", reg, semilla))
    veredictos[semilla] = bm.veredicto_conjunto(inf["comparaciones"])
R = rx.Registro(reg)
exps = sorted({x["exp_id"] for x in R.anotaciones() if x["tipo"] == "PRERREGISTRO"})
res = [R.resumen(e) for e in exps]
print(f"   20 semillas → {len(exps)} experimentos; intentos por experimento: {sorted({r['intentos'] for r in res})}; "
      f"fuera del máximo: {sum(len(r['fuera_del_maximo']) for r in res)}; veredictos: {sorted(set(veredictos.values()))}; "
      f"adoptables: {sum(r['adoptable'] for r in res)}")
mismas = len({r["hipotesis"] for r in res}) == 1
ok(len(exps) == 1 or sum(len(r["fuera_del_maximo"]) for r in res) >= 19,
   "repetir el banco con otra semilla y la misma hipótesis cuenta como variante del MISMO experimento (o queda fuera del máximo)")
print(f"   (las {len(exps)} hipótesis son idénticas: {mismas}; el registro no las enlaza)")

# 2. Fallo después del titular
bm.titular_a = titular_falso(["S1", "NOESTA"])
reg2 = tmp / "reg2.jsonl"
try:
    bm.ejecutar_a(ns(tmp / "f", reg2, 7))
    ok(False, "un símbolo ausente en los datos no detiene el banco")
except bm.BancoError as e:
    print(f"   se detiene: {e}")
r2 = rx.Registro(reg2).resumen(sorted({x['exp_id'] for x in rx.Registro(reg2).anotaciones()})[0])
print(f"   resumen del registro tras el fallo: intentos {r2['intentos']}, sin resultado {r2['sin_resultado']}, veredictos {r2['veredictos']}")
ok(r2["sin_resultado"] == [] and r2["veredictos"] == {"1": "fallido"},
   "un fallo después del titular (símbolo ausente) también deja el intento como «fallido» (T-99: cada intento cuenta)")

# 3. Prerregistro manipulado después
bm.titular_a = titular_falso(["S1", "S4"])
out = tmp / "m"
inf = bm.ejecutar_a(ns(out, tmp / "reg3.jsonl", 7))
p = json.loads((out / "prerregistro.json").read_text(encoding="utf-8"))
p.pop("huella")
p["hipotesis"] = "Otra hipótesis escrita después de ver el informe, que ahora encaja con el resultado"
p["huella"] = bm.huella(p)
(out / "prerregistro.json").write_text(json.dumps(p, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
inf_j = json.loads((out / "informe.json").read_text(encoding="utf-8"))
inf_j["prerregistro"] = p["huella"]
(out / "informe.json").write_text(json.dumps(inf_j, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
verificador = any(hasattr(bm, n) for n in ("verificar", "verificar_prerregistro", "comprobar"))
ok(verificador, "el banco ofrece una comprobación que detecte un prerregistro reescrito junto con su informe")
pre_reg = [x for x in rx.Registro(tmp / "reg3.jsonl").anotaciones() if x["tipo"] == "PRERREGISTRO"][0]
print(f"   el registro sí guarda la huella original dentro de «datos»: {inf['prerregistro'][:16] in pre_reg['contenido']['datos']}")

# 4. --experimento ajeno
reg4 = tmp / "reg4.jsonl"
R4 = rx.Registro(reg4)
ajeno = R4.prerregistrar({"hipotesis": "Recortar el prompt del agente AG-05 no empeora", "objeto": "RECORTE",
                          "metrica": "Brier en H2 frente a la tasa base", "datos": "otros datos", "desde": "2020-01-01",
                          "hasta": "2020-12-31", "semilla": 99, "criterio_exito": "rango del 90 % por encima de cero",
                          "max_variantes": 1}, autor="otro")["exp_id"]
try:
    bm.ejecutar_a(ns(tmp / "aj", reg4, 7, experimento=ajeno))
    print(f"   intento del banco aceptado en {ajeno} (objeto RECORTE, fechas 2020, semilla 99): {R4.resumen(ajeno)['veredictos']}")
    ok(False, "el banco acepta anotar su resultado en un experimento prerregistrado con otro objeto, otras fechas y otra semilla")
except (bm.BancoError, rx.RegistroError) as e:
    ok(True, f"--experimento ajeno rechazado: {e}")

print(f"\n{len(fallos)} fallo(s)")
for f in fallos:
    print(" -", f)
print(f"(temporal: {tmp})")
sys.exit(1 if fallos else 0)
