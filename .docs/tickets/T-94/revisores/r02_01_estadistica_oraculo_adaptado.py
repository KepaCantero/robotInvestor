"""QA r02 de T-94 · Adaptación de r01_01 (la clave «rango90» pasó a «rango», con el nivel aparte en «nivel»; nada más cambia).
Adaptación: cambia solo el nombre de la clave; las comprobaciones son las de r01.

1. Para muestras conocidas, compara `resumen()["rango"]` y `diferencia()["rango"]` con un remuestreo propio
   (otro generador, 20.000 remuestreos) y con la aproximación normal media ± 1,645·sd/√n.
2. Cobertura: con datos iid de media conocida, el rango del 90 % debe contener la media verdadera ~90 % de las veces.
3. Veredicto en el borde: rango que toca el cero exactamente.

Uso: .venv/bin/python -B .docs/tickets/T-94/revisores/r02_01_estadistica_oraculo_adaptado.py [<carpeta de banco_medida.py>]
Sale con 0 si todo cuadra; imprime cada comprobación."""
import sys
from pathlib import Path

import numpy as np

sys.dont_write_bytecode = True
CARPETA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3] / "scripts"
sys.path.insert(0, str(CARPETA))
import banco_medida as bm

fallos = []


def ok(cond, msg):
    print(("OK   " if cond else "FALLO ") + msg)
    if not cond:
        fallos.append(msg)


def oraculo_rango(x, B=20000, seed=12345):
    rng = np.random.default_rng(seed)
    x = np.asarray(x, float)
    medias = np.array([rng.choice(x, size=len(x), replace=True).mean() for _ in range(B)])
    return np.percentile(medias, 5), np.percentile(medias, 95)


# 1. Comparación con oráculo
rng = np.random.default_rng(1)
x = rng.normal(0.01, 0.05, size=60)
r = bm.resumen(list(x), 2000, 7)
lo, hi = oraculo_rango(x)
se = x.std(ddof=1) / np.sqrt(len(x))
print(f"   banco {r['rango']}  oráculo [{lo:.6f}, {hi:.6f}]  normal [{x.mean()-1.645*se:.6f}, {x.mean()+1.645*se:.6f}]")
ok(abs(r["rango"][0] - lo) < 0.25 * se and abs(r["rango"][1] - hi) < 0.25 * se, "resumen: rango90 = oráculo (tolerancia 0,25 errores típicos)")
ok(abs(r["media"] - x.mean()) < 1e-6, "resumen: media exacta")
ok(abs(r["acierto"] - (x > 0).mean()) < 1e-4, "resumen: tasa de acierto exacta")

y = rng.normal(-0.005, 0.04, size=45)
d = bm.diferencia(list(x), list(y), 2000, 7)
rng2 = np.random.default_rng(99)
dd = np.array([rng2.choice(x, len(x)).mean() - rng2.choice(y, len(y)).mean() for _ in range(20000)])
olo, ohi = np.percentile(dd, 5), np.percentile(dd, 95)
sed = np.sqrt(x.var(ddof=1) / len(x) + y.var(ddof=1) / len(y))
print(f"   banco {d['rango']}  oráculo [{olo:.6f}, {ohi:.6f}]")
ok(abs(d["rango"][0] - olo) < 0.25 * sed and abs(d["rango"][1] - ohi) < 0.25 * sed, "diferencia: rango90 = oráculo")
ok(abs(d["diferencia"] - (x.mean() - y.mean())) < 1e-6, "diferencia: diferencia de medias exacta")

# 2. Cobertura con datos iid (lo que el remuestreo sí garantiza)
dentro = 0
N = 400
for k in range(N):
    z = np.random.default_rng(1000 + k).normal(0.0, 1.0, size=40)
    lo_, hi_ = bm.resumen(list(z), 1000, k)["rango"]
    dentro += lo_ <= 0.0 <= hi_
cob = dentro / N
print(f"   cobertura iid n=40: {cob:.3f}")
ok(0.84 <= cob <= 0.95, "cobertura del rango del 90 % con datos iid entre 84 % y 95 %")

# 3. Bordes del veredicto
ok(bm.veredicto([0.0, 0.1]) == "todavía no se sabe", "rango [0, +] incluye el cero → todavía no se sabe")
ok(bm.veredicto([-0.1, 0.0]) == "todavía no se sabe", "rango [-, 0] incluye el cero → todavía no se sabe")
ok(bm.veredicto(None) == "sin datos", "sin rango → sin datos")
# Una sola observación: el rango es un punto; ¿qué veredicto da?
d1 = bm.diferencia([0.01], [-0.01], 2000, 7)
print(f"   n=1 frente a n=1: {d1}")
ok(d1["veredicto"] == "todavía no se sabe", "con una selección por lado no se afirma «mejor» (rango degenerado)")
d2 = bm.diferencia([0.02, 0.03], [-0.01, -0.02], 2000, 7)
print(f"   n=2 frente a n=2: {d2}")
ok(d2["veredicto"] == "todavía no se sabe", "con dos selecciones por lado no se afirma «mejor»")

print(f"\n{len(fallos)} fallo(s)")
sys.exit(1 if fallos else 0)
