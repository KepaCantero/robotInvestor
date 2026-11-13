"""QA r03 de T-91 (revisor nuevo) · 01: resolución frente a un oráculo CERRADO de la regla r03, con huecos, festivos,
paradas, días sueltos, calendarios alternos y series semanales en el proxy, la referencia y cada miembro de la CESTA (H1 a H4).

  .venv/bin/python -I .docs/tickets/T-91/revisores/r03_01_oraculo_fecha_comun.py [--ejecutor RUTA_11_EJECUTOR] [--n=N] [--semilla=S]

Oráculo (no itera: fórmula cerrada). Sea g la fecha más reciente <= f1 en la que TODAS las series usadas (proxy y referencia, o
proxy y cada miembro congelado de la CESTA) tienen cierre. El PRG se resuelve si y solo si g existe y, en cada serie,
g > fecha de su base y la edad de g frente a f1 no pasa la antigüedad de PS2 del horizonte (H1 en sesiones sin
`ps2_festivos`, con un calendario propio con dateutil). Entonces fecha_dato = fecha_dato_proxy = fecha_dato_referencia = g y
el exceso es rent_proxy(g) − rent_ref(g) (media de los miembros en la CESTA). Si no, el PRG sigue ABIERTO.

Comprobaciones:
  1 · estado, las tres fechas y el exceso (5e-9: `valor_observado` va redondeado a 8 decimales) coinciden con el oráculo en todos los escenarios;
  2 · todo RESUELTO tiene todas las series (espía de `_rentabilidad_serie`, última medida) en la misma fecha;
  3 · el bucle acaba: cada resolución termina en menos de 30 s (alarma) y con un número de medidas acotado
      (≤ (nº de series) × (nº de fechas distintas de las series en [emisión, f1]) + nº de series).
Con --ejecutor apuntando a d1a5a1b (la r02) sirve de control: allí la comprobación 1 y la 2 deben fallar."""
import random
import shutil
import signal
import sys
import tempfile
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "T-88" / "revisores"))
from r01_comun import Marcador, preparar  # noqa: E402

a, resto, ej = preparar(__doc__)
N = next((int(x.split("=")[1]) for x in resto if x.startswith("--n=")), 500)
SEM = next((int(x.split("=")[1]) for x in resto if x.startswith("--semilla=")), 20261113)

import pandas as pd  # noqa: E402
from dateutil.easter import easter  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402
from conftest import DATOS, config_pruebas  # noqa: E402

CFG = config_pruebas()
LIM = CFG["ps2_antiguedad_maxima_dias"]
FEST = CFG["ps2_festivos"]
RV = sorted(cargar_universo(RUTA_UNIVERSO_EJEMPLO).query("clase == 'RV'")["simbolo"])
EMISIONES = ["2025-12-19", "2026-03-27", "2026-04-17", "2026-06-12", "2026-08-28"]
OFFSET = {"H1": (5, 12), "H2": (12, 30), "H3": (25, 70), "H4": (50, 110)}
AJENOS = pd.to_datetime(["2026-01-19", "2026-02-16", "2026-05-25", "2026-06-19", "2026-07-03", "2026-09-07", "2026-04-06",
                         "2026-05-01", "2026-05-14", "2026-12-28", "2026-01-02", "2026-10-12"])


def cerrado_ps2(d):
    e = pd.Timestamp(easter(d.year))
    return (d.weekday() >= 5 or d.strftime("%m-%d") in FEST["fijos"] or (FEST["viernes_santo"] and d == e - pd.Timedelta(days=2))
            or (FEST["lunes_de_pascua"] and d == e + pd.Timedelta(days=1)))


def edad(d, f1, hz):
    d, f1 = pd.Timestamp(d).normalize(), pd.Timestamp(f1).normalize()
    if hz != "H1":
        return (f1 - d).days
    n, x = 0, d
    while x < f1:
        n += 0 if cerrado_ps2(x) else 1
        x += pd.Timedelta(days=1)
    return n


def modificar(df, rng, f1, hz, e, papel):
    f = pd.to_datetime(df["fecha"])
    quitar = pd.Series(False, index=df.index)
    desc = []
    margen = int(LIM[hz]) + (3 if hz == "H1" else 0)
    ventana = (f > e) & (f <= f1 + pd.Timedelta(days=5))
    if rng.random() < 0.3:
        quitar |= f.map(lambda d: cerrado_ps2(d)) & ventana
        desc.append("festivos PS2")
    if rng.random() < 0.2:
        quitar |= f.isin(AJENOS)
        desc.append("festivos ajenos")
    if rng.random() < 0.3:
        p = max(f1 - pd.Timedelta(days=rng.randint(0, margen + 4)), e)
        quitar |= f > p
        desc.append(f"parada {p.date()}")
    if rng.random() < 0.35:
        ini = max(f1 - pd.Timedelta(days=rng.randint(0, margen + 8)), e + pd.Timedelta(days=1))
        fin = ini + pd.Timedelta(days=rng.randint(0, 9))
        quitar |= (f >= ini) & (f <= fin)
        desc.append(f"hueco {ini.date()}..{fin.date()}")
    if rng.random() < 0.25:   # días sueltos al azar cerca de f1
        cerca = ventana & (f >= f1 - pd.Timedelta(days=margen + 10))
        quitar |= cerca & pd.Series([rng.random() < 0.4 for _ in range(len(df))], index=df.index)
        desc.append("días sueltos")
    if rng.random() < 0.12:   # calendario alterno: proxy solo días pares, referencia solo impares, cerca de f1
        cerca = ventana & (f >= f1 - pd.Timedelta(days=margen + 10))
        par = f.dt.day % 2 == 0
        quitar |= cerca & (~par if papel == "proxy" else par)
        desc.append("alterno")
    if rng.random() < 0.08 and papel != "proxy":   # semanal (solo viernes) desde la emisión
        quitar |= ventana & (f.dt.weekday != 4)
        desc.append("semanal")
    return df[~quitar], ", ".join(desc)


def escenario(rng):
    e = pd.Timestamp(rng.choice(EMISIONES))
    hz = rng.choice(["H1", "H2", "H3", "H4"])
    f1 = e + pd.Timedelta(days=rng.randint(*OFFSET[hz]))
    while f1.weekday() >= 5 and rng.random() < 0.7:
        f1 += pd.Timedelta(days=1)
    ref = rng.choice([None, "ACWI", "ACWI", "CESTA", "CESTA"])
    tmp = Path(tempfile.mkdtemp(prefix="qa_t91_r03_"))
    d = tmp / "datos"
    d.mkdir()
    simbolos = ["SPY"] + (["ACWI"] if ref == "ACWI" else RV if ref == "CESTA" else [])
    desc = {}
    for x in DATOS.iterdir():
        if x.stem in simbolos and rng.random() < 0.85:
            df, dd = modificar(pd.read_csv(x), rng, f1, hz, e, "proxy" if x.stem == "SPY" else "ref")
            df.to_csv(d / x.name, index=False)
            if dd:
                desc[x.stem] = dd
        else:
            shutil.copyfile(x, d / x.name)
    return tmp, d, str(e.date()), hz, str(f1.date()), ref, desc


class Alarma(Exception):
    pass


def _alarma(*_):
    raise Alarma()


signal.signal(signal.SIGALRM, _alarma)


def ejecutar(tmp, d, e, hz, f1, ref):
    b = Bloque(config_pruebas(), ProveedorCSV(d), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "estado", tmp / "ent")
    b.fijar_fecha(e)
    ev = b.evaluador
    try:
        nivel = ev._base_conocida("SPY", e)
    except Exception:
        return None
    reg = {"tipo_entrada": "ALTA", "prg_id": "PRG-2026-0901", "opp_id": "OPP-1", "clase": "RV", "horizonte": hz,
           "estado": "ABIERTO", "prob_interna": 0.65, "sentido": "POSITIVO", "umbral": 0.0,
           "tipo_pronostico": "RELATIVO" if ref else "DIRECCIONAL", "referencia_indice": ref, "variable": {"serie_ht01": "SPY"},
           "fecha_emision": e, "fecha_resolucion": f1, "nivel_referencia": nivel,
           "referencia_ingenua": {"valor_o_prob": 0.5}, "en_informe": True}
    if ref == "CESTA":
        reg["bases_cesta"] = ev.bases_cesta("RV", e, hz)
        if not reg["bases_cesta"]:
            return None
    elif ref:
        base = ev._base_conocida(ref, e)
        reg["nivel_referencia_indice"], reg["fecha_nivel_referencia_indice"] = base["valor"], base["fecha"]
    b.almacen.escribir("F4", "AG-10", reg)
    asof = pd.Timestamp(f1) + pd.offsets.BDay(2)
    b.fijar_fecha(str(asof.date()))
    usadas, n_medidas = {}, [0]
    orig = ev._rentabilidad_serie

    def espia(simbolo, f0, f1_, base=None):
        n_medidas[0] += 1
        r = orig(simbolo, f0, f1_, base)
        usadas[simbolo] = r[2]
        return r
    ev._rentabilidad_serie = espia
    signal.alarm(30)
    try:
        ev.resolver(str(asof.date()), "RUN-2026-0001")
    finally:
        signal.alarm(0)
    return reg, b.almacen.estado("F4")["PRG-2026-0901"], usadas, n_medidas[0]


def oraculo(series, bases, hz, f1):
    f1 = pd.Timestamp(f1)
    comunes = None
    for s in series.values():
        idx = set(s.index[s.index <= f1])
        comunes = idx if comunes is None else comunes & idx
    if not comunes:
        return ("ABIERTO",)
    g = max(comunes)
    for sim, b0 in bases.items():
        if not (g > pd.Timestamp(b0["fecha"]) and edad(g, f1, hz) <= int(LIM[hz])):
            return ("ABIERTO",)
    rent = {sim: float(series[sim][g]) / b0["valor"] - 1 for sim, b0 in bases.items()}
    rp = rent.pop("SPY")
    rr = (sum(rent.values()) / len(rent)) if rent else 0.0
    return ("RESUELTO", g, rp - rr)


m = Marcador()
rng = random.Random(SEM)
distintos, desalineados, colgados, cota = [], [], [], []
n_res = n_esp = 0
por_hz = {h: [0, 0] for h in ("H1", "H2", "H3", "H4")}
max_medidas = 0
for k in range(N):
    tmp, d, e, hz, f1, ref, desc = escenario(rng)
    etiqueta = f"#{k} {hz} e={e} f1={f1} ref={ref} {desc}"
    try:
        try:
            out = ejecutar(tmp, d, e, hz, f1, ref)
        except Alarma:
            colgados.append(etiqueta)
            continue
        if out is None:
            continue
        reg, est, usadas, n_med = out
        syms = ["SPY"] + (["ACWI"] if ref == "ACWI" else sorted(reg["bases_cesta"]) if ref == "CESTA" else [])
        series = {s: pd.read_csv(d / f"{s}.csv", parse_dates=["fecha"]).set_index("fecha")["cierre"] for s in syms}
        bases = {"SPY": reg["nivel_referencia"]}
        if ref == "ACWI":
            bases["ACWI"] = {"valor": reg["nivel_referencia_indice"], "fecha": reg["fecha_nivel_referencia_indice"]}
        elif ref == "CESTA":
            bases.update(reg["bases_cesta"])
        esperado = oraculo(series, bases, hz, f1)
        fechas_ventana = set()
        for s in series.values():
            fechas_ventana |= set(s.index[(s.index > pd.Timestamp(e)) & (s.index <= pd.Timestamp(f1))])
        tope = len(series) * (len(fechas_ventana) + 1) + len(series)
        max_medidas = max(max_medidas, n_med)
        if n_med > tope:
            cota.append(f"{etiqueta}: {n_med} medidas > {tope}")
        if est["estado"] == "RESUELTO":
            n_res += 1
            por_hz[hz][0] += 1
            r = est["resolucion"]
            fr = r.get("fecha_dato_referencia")
            obtenido = ("RESUELTO", pd.Timestamp(r["fecha_dato"]), r["valor_observado"], pd.Timestamp(r["fecha_dato_proxy"]),
                        pd.Timestamp(fr) if fr else None)
            vistas = {s: usadas.get(s) for s in syms}
            if len(set(vistas.values())) > 1:
                desalineados.append(f"{etiqueta}: {({s: str(v.date()) for s, v in vistas.items() if v is not None})}")
        else:
            n_esp += 1
            por_hz[hz][1] += 1
            obtenido = (est["estado"],)
        if esperado[0] == "RESUELTO":
            ok = (obtenido[0] == "RESUELTO" and obtenido[1] == esperado[1] and obtenido[3] == esperado[1]
                  and (ref is None or obtenido[4] == esperado[1]) and abs(obtenido[2] - esperado[2]) <= 5.1e-9)
        else:
            ok = obtenido[0] == "ABIERTO"
        if not ok:
            distintos.append(f"{etiqueta}: código {obtenido} · oráculo {esperado}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

print(f"   {N} escenarios: {n_res} RESUELTOS, {n_esp} en espera; por horizonte (resueltos, espera): {por_hz}; "
      f"máximo de medidas en una resolución: {max_medidas}")
m.check("1 · estado, fechas y exceso iguales que el oráculo cerrado (fecha común más reciente)", not distintos,
        f"{len(distintos)}: {distintos[:4]}")
m.check("2 · todo RESUELTO con todas las series en la misma fecha", not desalineados, f"{len(desalineados)}: {desalineados[:4]}")
m.check("3a · ninguna resolución se cuelga (alarma de 30 s)", not colgados, f"{len(colgados)}: {colgados[:3]}")
m.check("3b · número de medidas acotado", not cota, f"{len(cota)}: {cota[:3]}")
sys.exit(m.fin())
