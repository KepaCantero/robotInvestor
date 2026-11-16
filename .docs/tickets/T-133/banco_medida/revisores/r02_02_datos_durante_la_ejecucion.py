"""T-133 QA r02 · La comprobación de que los datos no cambian durante la ejecución (banco 0.5.0, r02 H-01).

`ejecutar_a` calcula las huellas antes de ejecutar A y vuelve a calcularlas con lo que devuelve el titular. Ataques, con un
titular falso que toca los ficheros mientras «se ejecuta» (todo en un temporal, `--sin-registro` salvo donde se dice):
1. cambia un cierre y lo deja cambiado → ¿se detiene?
2. cambia un cierre y lo restaura antes de volver (A habría leído otros datos) → ¿se ve?
3. cambia la clase de un símbolo en el universo → ¿se detiene?
4. cambia solo el «nombre» de una fila del universo (A lo lee) → ¿se ve?
5. cambia un CSV que no es de un símbolo del universo (un índice de referencia de A) → ¿se ve?
6. el titular devuelve otra carpeta con el mismo contenido → ¿pasa? (debe: es el mismo dato)
7. con registro: el intento que se detiene queda «fallido» y la misma variante se puede volver a intentar.
8. universo con símbolos que parecen números («0700»), mezclados con otros (8) o todos (8b) → ¿lo acepta el banco como A?
Uso: .venv/bin/python -B r02_02_datos_durante_la_ejecucion.py <carpeta de banco_medida.py>"""
import argparse
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
CARPETA = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(CARPETA))
import banco_medida as bm
import registro_experimentos as rx

fallos, notas = [], []


def ok(cond, msg):
    print(("OK   " if cond else "FALLO ") + msg, flush=True)
    if not cond:
        fallos.append(msg)


def nota(msg):
    print("NOTA  " + msg, flush=True)
    notas.append(msg)


TMP = Path(tempfile.mkdtemp(prefix="r02_t133_durante_"))
datos = TMP / "datos"
datos.mkdir()
fechas = pd.bdate_range("2024-01-01", "2026-06-30")
rng = np.random.default_rng(9)
sims = [f"S{i}" for i in range(8)]
for s in sims + ["REF"]:
    pd.DataFrame({"fecha": fechas.strftime("%Y-%m-%d"),
                  "cierre": 100 * np.exp(np.cumsum(rng.normal(0, 0.01, len(fechas))))}).to_csv(datos / f"{s}.csv", index=False)
universo = TMP / "universo.csv"
pd.DataFrame({"simbolo": sims, "clase": ["C"] * 8, "nombre": [f"n{s}" for s in sims]}).to_csv(universo, index=False)
bm.rutas_por_defecto = lambda: (datos, universo)
cortes = [d.strftime("%Y-%m-%d") for d in pd.date_range("2025-03-07", periods=13, freq="7D")]


def titular(tocar=None, devuelve=None, elige=("S1", "S4")):
    def f(desde, hasta, carpeta, cliente, frecuencia, clases, **kw):
        restaura = tocar() if tocar else None
        if restaura:
            restaura()
        d, u = devuelve or (datos, universo)
        return {"selecciones": [{"fecha_asof": c, "clase": "C", "simbolo": s, "direccion": "LARGO", "horizonte": "H"}
                                for c in cortes for s in elige],
                "consumo": {"llamadas": 1, "tokens_entrada": 1, "tokens_salida": 1, "coste_estimado": None},
                "datos": d, "universo": u, "fecha_fin": lambda ini, h: ini + pd.DateOffset(months=6),
                "advertencias": [], "excluidos_contaminacion": 0}
    return f


def ns(salida, registro=None, **kw):
    d = {"desde": "2025-03-07", "hasta": "2025-05-30", "salida": str(TMP / salida), "cliente": "mock", "frecuencia": None,
         "clases": None, "semilla": 7, "remuestreos": 200, "ventana": 63, "registro": registro, "experimento": None,
         "max_variantes": 1}
    d.update(kw)
    return argparse.Namespace(**d)


def corre(nombre, tit, **kw):
    bm.titular_a = tit
    try:
        return bm.ejecutar_a(ns(nombre, **kw)), None
    except bm.BancoError as e:
        return None, str(e)


def editar(fichero, cambia):
    original = fichero.read_bytes()
    texto = original.decode("utf-8").splitlines()
    fichero.write_text("\n".join(cambia(texto)) + "\n", encoding="utf-8")
    return lambda: fichero.write_bytes(original)


def otro_cierre(t):
    t[20] = t[20].rsplit(",", 1)[0] + ",77.0"
    return t


inf, err = corre("base", titular())
ok(err is None, f"sin tocar nada, el banco termina ({err})")

r = {}


def caso1():
    r["1"] = editar(datos / "S1.csv", otro_cierre)


_, err = corre("c1", titular(caso1))
ok(err is not None and "prerregistro" in err, f"1. un cierre cambiado durante la ejecución detiene el banco ({err})")
r["1"]()

_, err = corre("c2", titular(lambda: editar(datos / "S1.csv", otro_cierre)))
if err is None:
    nota("2. un cierre cambiado y restaurado antes de que acabe el titular no se ve (A habría leído otros datos): la "
         "comprobación es de antes y después, no de lo que A leyó")


def caso3():
    r["3"] = editar(universo, lambda t: t[:-1] + [t[-1].replace(",C,", ",D,")])


_, err = corre("c3", titular(caso3))
ok(err is not None, f"3. un símbolo que cambia de clase durante la ejecución detiene el banco ({err})")
r["3"]()


def caso4():
    r["4"] = editar(universo, lambda t: t[:-1] + [t[-1].rsplit(",", 1)[0] + ",otro nombre"])


_, err = corre("c4", titular(caso4))
if err is None:
    nota("4. el «nombre» de una fila del universo cambiado durante la ejecución no se ve (A lo lee: va a las fichas y al prompt)")
r["4"]()


def caso5():
    r["5"] = editar(datos / "REF.csv", otro_cierre)


_, err = corre("c5", titular(caso5))
if err is None:
    nota("5. un CSV que no es de un símbolo del universo (un índice de referencia de A) cambiado durante la ejecución no se ve")
r["5"]()

copia = TMP / "copia"
shutil.copytree(datos, copia)
u_copia = TMP / "u_copia.csv"
shutil.copy(universo, u_copia)
_, err = corre("c6", titular(devuelve=(copia, u_copia)))
ok(err is None, f"6. el titular devuelve una copia con el mismo contenido: pasa ({err})")
(copia / "S4.csv").write_text((copia / "S4.csv").read_text(encoding="utf-8").replace("\n2025-04-01,", "\n2025-04-01,9", 1),
                              encoding="utf-8")
_, err = corre("c6b", titular(devuelve=(copia, u_copia)))
ok(err is not None, f"6b. el titular devuelve otra carpeta con un cierre distinto: se detiene ({err})")

reg = TMP / "reg.jsonl"
_, err = corre("c7", titular(caso1), registro=str(reg))
r["1"]()
inf2, err2 = corre("c7b", titular(), registro=str(reg))
R = rx.Registro(reg)
exp = R.experimento(inf2["experimento"]["exp_id"]) if inf2 else None
print(f"   7. intento detenido: {err is not None}; reintento: {inf2 and inf2['experimento']}; resultados "
      f"{[x['veredicto'] for x in exp['resultados']] if exp else None}")
ok(exp is not None and exp["resultados"][0]["veredicto"] == "fallido",
   "7. el intento detenido queda «fallido» en el registro y la misma variante se vuelve a intentar")

u_num = TMP / "u_num.csv"
pd.DataFrame({"simbolo": ["0700", "0005"] + sims[2:], "clase": ["C"] * 8}).to_csv(u_num, index=False)
dn = TMP / "d_num"
shutil.copytree(datos, dn)
(dn / "S0.csv").rename(dn / "0700.csv")
(dn / "S1.csv").rename(dn / "0005.csv")
bm.rutas_por_defecto = lambda: (dn, u_num)
_, err = corre("c8", titular(devuelve=(dn, u_num), elige=("0005", "S4")))
ok(err is None, f"8. un universo con «0700» y «0005» (A los lee como texto): el banco termina ({err})")
if err:
    nota(f"8. un universo con símbolos que parecen números («0700», que A lee como texto) detiene el banco: {err}")
u_jp = TMP / "u_jp.csv"   # 8b. todos los símbolos parecen números (acciones de Japón o Hong Kong)
u_jp.write_text("simbolo,clase\n" + "".join(f"{s},C\n" for s in ("0700", "0005", "7203", "6758", "9984", "8306", "6861", "4063")),
                encoding="utf-8")
dj = TMP / "d_jp"
dj.mkdir()
for s, n in zip(("0700", "0005", "7203", "6758", "9984", "8306", "6861", "4063"), sims):
    shutil.copy(datos / f"{n}.csv", dj / f"{s}.csv")
bm.rutas_por_defecto = lambda: (dj, u_jp)
_, err = corre("c8b", titular(devuelve=(dj, u_jp), elige=("0005", "7203")))
ok(err is None, f"8b. un universo en el que todos los símbolos parecen números («0700», «7203»…): el banco termina ({err})")
shutil.rmtree(TMP, ignore_errors=True)
print(f"\n{len(fallos)} fallo(s), {len(notas)} nota(s)")
for f in fallos:
    print(" - " + f)
sys.exit(1 if fallos else 0)
