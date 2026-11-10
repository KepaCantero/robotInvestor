"""r05_02 · QA T-65 r05 · H-24 en un backtest largo con series que se paran, que tienen huecos y que vuelven.

Uso (desde bloque_a/11_Ejecutor):  ../../.venv/bin/python ../../.docs/tickets/T-65/revisores/r05_02_backtest_largo_series_paradas.py [desde hasta]

Ciclos semanales (por defecto del 2025-09-05 al 2026-10-30; RV, MP y DIV; horizontes H1 a H4 por turnos; cliente simulado) con:
  · ACWI (referencia de RV) con un hueco del 2026-01-12 al 2026-02-13 (vuelve a publicarse después);
  · DBC (referencia de MP) parada desde el 2026-06-30;
  · SPY con un hueco del 2026-04-06 al 2026-04-17;
  · un miembro de la cesta de DIV parado desde el 2026-03-13.
Y la resolución final del backtest. Comprueba en F4, frente a los CSV:
  (1) ningún PRG RESUELTO con una serie sin dato posterior a la emisión, más antigua que PS2 de su horizonte en la
      resolución, o con `fecha_dato_proxy` / `fecha_dato_referencia` distintas del último dato real;
  (2) ningún PRG emitido con el proxy o la referencia más antiguos que PS2 de su horizonte;
  (3) ningún NO_RESOLUBLE con todas sus series al día (sería una pérdida espuria);
  (4) ningún ABIERTO vencido más allá del plazo de NO_RESOLUBLE.
"""
import collections
import pathlib
import shutil
import sys
import tempfile
import warnings

import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, str(pathlib.Path.cwd()))
from bloque_a.configuracion import DIR_EJECUTOR, RUTA_UNIVERSO_EJEMPLO, cargar_config, parametro  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.herramientas.ht05_planificador import dias_habiles_entre, fechas_ciclo  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque, _sesiones_entre  # noqa: E402

DESDE, HASTA = (sys.argv[1:3] if len(sys.argv) >= 3 else ("2025-09-05", "2026-10-30"))
CLASES = ["RV", "MP", "DIV"]
hall = 0
tmp = pathlib.Path(tempfile.mkdtemp(prefix="r05_02_"))
datos = tmp / "datos"
shutil.copytree(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos", datos)


def editar(sym, filtro):
    df = pd.read_csv(datos / f"{sym}.csv")
    df[filtro(pd.to_datetime(df["fecha"]))].to_csv(datos / f"{sym}.csv", index=False)


cfg = cargar_config(extra={"modo": "backtest", "perfiles": {"activos": CLASES},
                           "evaluacion": {"bootstrap_replicas": 200, "simulaciones_ece": 200}})
b0 = Bloque(cfg, ProveedorCSV(datos), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "x" / "e", tmp / "x" / "s")
b0.fijar_fecha("2026-03-13")
miembro = b0.evaluador.simbolos_clase("DIV")[0]
editar("ACWI", lambda f: ~((f >= "2026-01-12") & (f <= "2026-02-13")))
editar("DBC", lambda f: f <= "2026-06-30")
editar("SPY", lambda f: ~((f >= "2026-04-06") & (f <= "2026-04-17")))
editar(miembro, lambda f: f <= "2026-03-13")
print(f"Miembro de DIV parado: {miembro}")

b = Bloque(cfg, ProveedorCSV(datos), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "e", tmp / "s")
fechas = fechas_ciclo(DESDE, HASTA, "semanal", int(parametro(cfg, "backtest.dia_semana")))
# el cliente simulado no elige H1 ni H4 por sí solo: se alternan los horizontes pedidos por ciclo
TURNOS = [["H1"], ["H2", "H3"], ["H4"]]
for i, f in enumerate(fechas):
    b.ciclo(f, alcance={"clases": CLASES}, horizontes=TURNOS[i % len(TURNOS)])
fin = fechas[-1]
b.fijar_fecha(fin)
b.evaluador.resolver(fin, "RESOLUCION-FINAL")

lim = parametro(cfg, "ps2_antiguedad_maxima_dias")
plazo = int(parametro(cfg, "evaluacion.dias_habiles_no_resoluble"))
fest = b._festivos_ps2
series = {}


def s(sym):
    if sym not in series:
        series[sym] = pd.read_csv(datos / f"{sym}.csv", parse_dates=["fecha"]).set_index("fecha")["cierre"]
    return series[sym]


def ultimo(sym, f):
    x = s(sym)
    x = x[x.index <= pd.Timestamp(f)]
    return x.index.max() if len(x) else None


def sirve(sym, f0, f1, hz):
    d0, d1 = ultimo(sym, f0), ultimo(sym, f1)
    if d0 is None or d1 is None or d1 <= d0:
        return False, d1
    edad = dias_habiles_entre(d1, f1) if hz == "H1" else (pd.Timestamp(f1) - d1).days
    return edad <= lim[hz], d1


f4 = b.almacen.estado("F4", fin)
prgs = [p for p in f4.values() if p.get("prob_interna") is not None and not p.get("es_hito")]
estados = collections.Counter((p["horizonte"], p.get("estado")) for p in prgs)
print(f"Ciclos: {len(fechas)} · PRG: {len(prgs)} · estados por horizonte: {dict(sorted(estados.items()))}")
malos_res, malos_emi, espurios, colgados = [], [], [], []
for p in prgs:
    hz, f0, f1 = p["horizonte"], pd.Timestamp(p["fecha_emision"]), pd.Timestamp(p["fecha_resolucion"])
    proxy, ref = p["variable"]["serie_ht01"], p.get("referencia_indice")
    syms = [proxy] + ([ref] if p.get("tipo_pronostico") == "RELATIVO" and ref and ref != "CESTA" else [])
    # (2) emisión
    for sym in syms:
        d = ultimo(sym, f0)
        edad = _sesiones_entre(d, f0, fest) if hz == "H1" else (f0 - d).days
        if edad > lim[hz]:
            malos_emi.append((p["prg_id"], hz, sym, str(f0.date()), str(d.date())))
    r = p.get("resolucion") or {}
    if p.get("estado") == "RESUELTO":
        for sym, campo in zip(syms, ("fecha_dato_proxy", "fecha_dato_referencia")):
            ok, d1 = sirve(sym, f0, f1, hz)
            if not ok or (d1 is not None and r.get(campo) != str(d1.date())):
                malos_res.append((p["prg_id"], hz, sym, str(f0.date()), str(f1.date()), r.get(campo), str(d1.date()) if d1 is not None else None))
        if r.get("rent_proxy") == 0.0 or r.get("rent_referencia") == 0.0:
            malos_res.append((p["prg_id"], hz, "rent 0", r.get("rent_proxy"), r.get("rent_referencia")))
    elif p.get("estado") == "NO_RESOLUBLE":
        todas = all(sirve(sym, f0, f1, hz)[0] for sym in syms)
        if todas and ref != "CESTA":
            espurios.append((p["prg_id"], hz, syms, str(f0.date()), str(f1.date())))
    elif p.get("estado") == "ABIERTO" and f1 <= fin and dias_habiles_entre(f1, fin) >= plazo:
        colgados.append((p["prg_id"], hz, str(f1.date())))

for nombre, lst in (("RESUELTOS con una serie que no sirve o fecha guardada distinta", malos_res),
                    ("emitidos con una serie más antigua que PS2", malos_emi),
                    ("NO_RESOLUBLE con todas sus series al día", espurios),
                    ("ABIERTO vencidos más allá del plazo", colgados)):
    if lst:
        hall += 1
        print(f"HALLAZGO  {len(lst)} PRG {nombre}: {lst[:4]}")
    else:
        print(f"OK        0 PRG {nombre}")
print(f"HALLAZGOS: {hall}")
