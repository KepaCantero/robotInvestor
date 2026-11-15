"""QA r01 de T-141 (revisor independiente): contrasta los cruces que deriva `descargar_datos_bce.py` con otra fuente
pública e independiente, los tipos de mediodía de Nueva York de la Reserva Federal (H.10, en FRED: descarga CSV pública
sin clave, `fredgraph.csv`). Si un cruce estuviera invertido, la diferencia sería de órdenes de magnitud.

Uso: <python> -I r01_contraste_fred.py <carpeta_datos_bce> <carpeta_fred>
(`<carpeta_fred>` con fred_DEXJPUS.csv, fred_DEXUSEU.csv, fred_DEXUSUK.csv, fred_DEXUSAL.csv, fred_DEXSZUS.csv y
fred_DEXMXUS.csv, descargados con curl de https://fred.stlouisfed.org/graph/fredgraph.csv?id=<serie>&cosd=2024-01-01).
Termina con 0 si la mediana del desvío relativo de cada cruce es < 0,5 % y el máximo < 3 %."""
import sys
from pathlib import Path

import pandas as pd

PARES = {"EURUSD=X": "DEXUSEU", "USDJPY=X": "DEXJPUS", "GBPUSD=X": "DEXUSUK", "AUDUSD=X": "DEXUSAL",
         "USDCHF=X": "DEXSZUS", "USDMXN=X": "DEXMXUS"}   # FRED: DEXUSxx = dólares por xx; DEXxxUS = xx por dólar
bce, fred = Path(sys.argv[1]), Path(sys.argv[2])
ok = True
for sim, serie in PARES.items():
    a = pd.read_csv(bce / f"{sim}.csv", parse_dates=["fecha"]).set_index("fecha")["cierre"]
    f = pd.read_csv(fred / f"fred_{serie}.csv", parse_dates=["observation_date"]).set_index("observation_date")[serie]
    f = pd.to_numeric(f, errors="coerce").dropna()
    j = pd.concat([a, f], axis=1, join="inner").dropna()
    d = (j.iloc[:, 0] / j.iloc[:, 1] - 1).abs()
    bien = d.median() < 0.005 and d.max() < 0.03
    ok &= bien
    print(f"{'OK ' if bien else 'MAL'} {sim:9} vs {serie}: {len(j)} días comunes · mediana {d.median():.4%} · máx {d.max():.4%}"
          f" ({d.idxmax().date()}) · último BCE {j.iloc[-1, 0]:.4f} / Fed {j.iloc[-1, 1]:.4f}")
sys.exit(0 if ok else 1)
