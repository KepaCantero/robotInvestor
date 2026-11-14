"""QA r01 de T-113 · H-23 y H-27 de T-108 con un oráculo: sendas escalonadas conocidas, su curva OIS exacta, redondeada a
1 pb o 0,1 pb con `precision_cotizacion` = medio último dígito. Se cuenta (a) cuántas se rechazan con «no se puede reproducir»
(H-27: deberían ser 0), (b) cuántas reuniones tienen un error real de `movimientos_en_reunion` o `movimientos_acumulados`
mayor que la cota publicada (H-23: 0) y (c) que una curva que NO es escalonada siga rechazándose con la precisión declarada.
Uso (desde bloque_a/11_Ejecutor de la copia): python .../r01_04_mon_exp_oraculo.py [n_sendas]"""
import math
import sys
from collections import Counter

import numpy as np
import pandas as pd

sys.path.insert(0, ".")
from bloque_a.motor import servicio  # noqa: E402

fn = servicio.IMPLEMENTADAS["MON-EXP-001"]["fn"]
N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
rng = np.random.default_rng(113)
FECHA = pd.Timestamp("2026-11-12")
BASE = 360.0
INC = 0.0025


def curva_exacta(r0, tasas, cortes, dias):
    out = []
    for d in dias:
        lg, prev, r = 0.0, 0, r0
        tramos = list(zip(cortes, tasas))
        for c, rk in tramos:
            if c >= d:
                break
            lg += (c - prev) * math.log1p(r / BASE); prev, r = c, rk
        lg += (d - prev) * math.log1p(r / BASE)
        out.append(math.expm1(lg) * BASE / d)
    return out


motivos: Counter = Counter()
servidas = fuera_r = fuera_a = reuniones = 0
peor_r = peor_a = 0.0
for i in range(N):
    n_reu = int(rng.integers(2, 6))
    cortes = sorted(int(x) for x in rng.choice(np.arange(15, 330), size=n_reu, replace=False))
    if min(np.diff([0] + cortes)) < 20:
        continue
    oficial, dif = 0.02 + float(rng.uniform(-0.01, 0.02)), 0.0008
    r0 = oficial - dif
    mov = rng.choice([-1, -0.5, 0, 0.3, 0.7, 1.0], size=n_reu) * INC
    tasas = list(r0 + np.cumsum(mov))
    # nodos: uno en cada reunión, uno entre reuniones y alguno más (sistema sobredeterminado)
    dias = sorted(set(cortes) | {int((a + b) / 2) for a, b in zip(cortes, cortes[1:] + [cortes[-1] + 40])} | {cortes[-1] + 40, 7}
                  | {int(x) for x in rng.integers(10, cortes[-1] + 40, size=3)})
    exacta = curva_exacta(r0, tasas, cortes, dias)
    dec = int(rng.choice([4, 5]))   # 1 pb o 0,1 pb
    prec = 0.5 * 10 ** (-dec)
    v = {"fecha": str(FECHA.date()), "base_curva": 360, "tipo_oficial": oficial, "diferencial_estable": dif,
         "reuniones": [str((FECHA + pd.Timedelta(days=c)).date()) for c in cortes],
         "curva": [{"dias": d, "tipo": round(t, dec)} for d, t in zip(dias, exacta)], "precision_cotizacion": prec}
    try:
        r, lim = fn({"valores": v, "series": {}, "series_rol": {}}, {})
    except Exception as e:  # noqa: BLE001
        t = str(e)
        motivos["no se puede reproducir" if "no se puede reproducir" in t else "no identificada" if "no identificada" in t
                else "no se puede contrastar" if "contrastar" in t else t[:60]] += 1
        continue
    servidas += 1
    prev = r0
    for s, rk in zip(r["senda"], tasas):
        reuniones += 1
        e_r = abs(s["movimientos_en_reunion"] - (rk - prev) / INC)
        e_a = abs(s["movimientos_acumulados"] - (rk - r0) / INC)
        prev = rk
        cr, ca = s["incertidumbre_probabilidad"], s["incertidumbre_probabilidad_acumulada"]
        if cr < 1 and e_r > cr * (1 + 1e-3) + 1e-9:
            fuera_r += 1
        if ca < 1 and e_a > ca * (1 + 1e-3) + 1e-9:
            fuera_a += 1
        peor_r, peor_a = max(peor_r, e_r / max(cr, 1e-300)), max(peor_a, e_a / max(ca, 1e-300))
print(f"sendas servidas: {servidas}; rechazos: {dict(motivos)}")
print(f"H-27: rechazos «no se puede reproducir» de curvas escalonadas exactas redondeadas: {motivos['no se puede reproducir']} (esperado 0)")
print(f"H-23: reuniones {reuniones}; error real > cota publicada: en la reunión {fuera_r}, acumulada {fuera_a} (esperado 0); "
      f"peor error/cota: {peor_r:.3f} y {peor_a:.3f}")

# (c) una curva lisa (no escalonada) con precisión declarada debe seguir rechazándose
dias = [7, 30, 60, 90, 120, 150, 180, 240, 300, 365]
rech = 0
for pend in (0.004, 0.008, 0.02):
    v = {"fecha": str(FECHA.date()), "base_curva": 360, "tipo_oficial": 0.02, "diferencial_estable": 0.0008,
         "reuniones": [str((FECHA + pd.Timedelta(days=c)).date()) for c in (35, 125, 215, 305)],
         "curva": [{"dias": d, "tipo": round(0.0192 + pend * (d / 365) ** 2, 4)} for d in dias], "precision_cotizacion": 0.00005}
    try:
        r, lim = fn({"valores": v, "series": {}, "series_rol": {}}, {})
        print(f"  curva lisa (pendiente {pend}): SERVIDA; limitaciones: {[x[:70] for x in lim]}")
    except Exception as e:  # noqa: BLE001
        rech += 1; print(f"  curva lisa (pendiente {pend}): rechazada · {str(e)[:110]}")
# (d) precisión declarada disparatada: ¿se sirve cualquier cosa?
for prec in (0.0, 1e-12, 0.01, 1.0, float("nan"), float("inf"), -1e-9, "0.0001", True):
    v2 = {**v, "precision_cotizacion": prec}
    try:
        r, lim = fn({"valores": v2, "series": {}, "series_rol": {}}, {})
        print(f"  precisión {prec!r}: SERVIDA con {len(lim)} limitaciones")
    except Exception as e:  # noqa: BLE001
        print(f"  precisión {prec!r}: rechazada · {type(e).__name__}: {str(e)[:90]}")
