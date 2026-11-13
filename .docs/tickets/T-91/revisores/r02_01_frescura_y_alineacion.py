"""QA r02 de T-91 (revisor nuevo) · 01: resolución con paradas, huecos y festivos en el proxy, la referencia y la CESTA, en
H1 a H4, frente a un oráculo propio que lee los CSV.

  .venv/bin/python -I .docs/tickets/T-91/revisores/r02_01_frescura_y_alineacion.py [--ejecutor RUTA_11_EJECUTOR] [--rapido] [--n=N] [--semilla=S]

Escenarios aleatorios (semilla fija): emisión en cuatro fechas (Navidad 2025, Pascua 2026, abril y junio de 2026), horizonte
H1 a H4, PRG DIRECCIONAL, RELATIVO frente a ACWI o RELATIVO frente a la CESTA de RV. A cada serie (SPY, ACWI, cada miembro)
se le aplica, al azar, una parada, un hueco cerca de la fecha de resolución o un calendario con festivos (los de PS2 o
festivos ajenos a PS2). Se resuelve dos sesiones después de la fecha de resolución.

Comprobaciones:
  1 · ningún RESUELTO usa un dato (proxy, referencia o miembro) sin dato posterior a su base o más viejo que PS2 frente a la
      fecha de resolución (edad con un calendario propio: H1 en sesiones sin los festivos de `ps2_festivos`);
  2 · el código coincide con un oráculo propio de la regla r02 (frescura frente a f1, medir hasta la fecha común sin iterar):
      estado, fechas y exceso;
  3 · INFORMATIVO (H-05 de la r02): cuántos RESUELTOS acaban con las series en fechas distintas tras alinear, y la mayor
      diferencia en días; con un oráculo «iterado» (repetir la alineación hasta que coincidan) cuántos se alinearían.
Con --ejecutor apuntando a 7feb697 (la r01) sirve de control: allí la comprobación 1 debe fallar."""
import random
import shutil
import sys
import tempfile
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "T-88" / "revisores"))
from r01_comun import Marcador, preparar  # noqa: E402

a, resto, ej = preparar(__doc__)
N = next((int(x.split("=")[1]) for x in resto if x.startswith("--n=")), 120 if a.rapido else 400)
SEM = next((int(x.split("=")[1]) for x in resto if x.startswith("--semilla=")), 20261112)

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
EMISIONES = ["2025-12-19", "2026-03-27", "2026-04-17", "2026-06-12"]
OFFSET = {"H1": (5, 12), "H2": (12, 30), "H3": (25, 70), "H4": (50, 110)}
AJENOS = ["2026-01-19", "2026-02-16", "2026-05-25", "2026-06-19", "2026-07-03", "2026-09-07", "2026-04-06", "2026-05-01",
          "2026-05-14", "2026-05-25", "2026-12-28", "2026-01-02"]   # festivos de otras bolsas, fuera de `ps2_festivos`


def cerrado_ps2(d: pd.Timestamp) -> bool:
    e = pd.Timestamp(easter(d.year))
    return (d.weekday() >= 5 or d.strftime("%m-%d") in FEST["fijos"]
            or (FEST["viernes_santo"] and d == e - pd.Timedelta(days=2))
            or (FEST["lunes_de_pascua"] and d == e + pd.Timedelta(days=1)))


def edad(d, f1, hz) -> int:
    d, f1 = pd.Timestamp(d).normalize(), pd.Timestamp(f1).normalize()
    if hz != "H1":
        return (f1 - d).days
    n, x = 0, d
    while x < f1:
        n += 0 if cerrado_ps2(x) else 1
        x += pd.Timedelta(days=1)
    return n


def fresca(d0, d1, f1, hz) -> bool:
    return pd.Timestamp(d1) > pd.Timestamp(d0) and edad(d1, f1, hz) <= int(LIM[hz])


class Espera(Exception):
    pass


class Oraculo:
    """Regla r02 leída de INC-T91-01, sobre los CSV: `iterar` repite la alineación hasta que todas las series coincidan."""

    def __init__(self, series: dict[str, pd.Series], hz, f1, iterar=False):
        self.s, self.hz, self.f1, self.iterar = series, hz, pd.Timestamp(f1), iterar
        self.usadas: dict[str, pd.Timestamp] = {}

    def ult(self, sim, t):
        x = self.s[sim]
        x = x[x.index <= pd.Timestamp(t)]
        if x.empty:
            raise Espera(sim)
        return x.index[-1], float(x.iloc[-1])

    def una(self, sim, base, t):
        d1, v1 = self.ult(sim, t)
        if not fresca(base["fecha"], d1, self.f1, self.hz):
            raise Espera(sim)
        self.usadas[sim] = d1
        return v1 / base["valor"] - 1, d1

    def cesta(self, bases, t):
        patas = {m: self.una(m, b, t) for m, b in sorted(bases.items())}
        corte = min(d for _, d in patas.values())
        while any(d != corte for _, d in patas.values()):
            patas = {m: self.una(m, b, corte) for m, b in sorted(bases.items())}
            nuevo = min(d for _, d in patas.values())
            if not self.iterar or nuevo == corte:
                break
            corte = nuevo
        return sum(r for r, _ in patas.values()) / len(patas), min(d for _, d in patas.values())

    def medir(self, ref, bases_ref, base_p, t):
        rp, d1 = self.una("SPY", base_p, t)
        if ref is None:
            return rp, None, d1, None
        rr, d1b = self.cesta(bases_ref, t) if ref == "CESTA" else self.una(ref, bases_ref, t)
        return rp, rr, d1, d1b

    def resolver(self, ref, bases_ref, base_p):
        rp, rr, d1, d1b = self.medir(ref, bases_ref, base_p, self.f1)
        if ref is not None and d1 != d1b:
            corte = min(d1, d1b)
            while True:
                rp, rr, d1, d1b = self.medir(ref, bases_ref, base_p, corte)
                if not self.iterar or d1 == d1b or min(d1, d1b) == corte:
                    break
                corte = min(d1, d1b)
        return rp, rr, d1, d1b


def modificar(df: pd.DataFrame, rng: random.Random, f1: pd.Timestamp, hz: str, e: pd.Timestamp) -> tuple[pd.DataFrame, str]:
    f = pd.to_datetime(df["fecha"])
    desc = []
    margen = int(LIM[hz]) + (3 if hz == "H1" else 0)
    if rng.random() < 0.3:
        fechas_f = [d for d in pd.date_range(e - pd.Timedelta(days=20), f1 + pd.Timedelta(days=5)) if cerrado_ps2(d) and d.weekday() < 5]
        df, f = df[~f.isin(fechas_f)], f[~f.isin(fechas_f)]
        desc.append("festivos PS2")
    if rng.random() < 0.25:
        aj = pd.to_datetime(AJENOS)
        df, f = df[~f.isin(aj)], f[~f.isin(aj)]
        desc.append("festivos ajenos")
    if rng.random() < 0.35:
        p = f1 - pd.Timedelta(days=rng.randint(0, margen + 4))
        p = max(p, e)
        df, f = df[f <= p], f[f <= p]
        desc.append(f"parada {p.date()}")
    if rng.random() < 0.45:
        ini = f1 - pd.Timedelta(days=rng.randint(0, margen + 8))
        ini = max(ini, e + pd.Timedelta(days=1))
        fin = ini + pd.Timedelta(days=rng.randint(0, 9))
        df, f = df[(f < ini) | (f > fin)], f[(f < ini) | (f > fin)]
        desc.append(f"hueco {ini.date()}..{fin.date()}")
    return df, ", ".join(desc)


def escenario(k: int, rng: random.Random):
    e = pd.Timestamp(rng.choice(EMISIONES))
    hz = rng.choice(["H1", "H2", "H3", "H4"])
    f1 = e + pd.Timedelta(days=rng.randint(*OFFSET[hz]))
    while f1.weekday() >= 5 and rng.random() < 0.7:
        f1 += pd.Timedelta(days=1)
    ref = rng.choice([None, "ACWI", "ACWI", "CESTA", "CESTA"])
    tmp = Path(tempfile.mkdtemp(prefix="qa_t91_r02_"))
    d = tmp / "datos"
    d.mkdir()
    simbolos = ["SPY"] + (["ACWI"] if ref == "ACWI" else RV if ref == "CESTA" else [])
    desc = {}
    for x in DATOS.iterdir():
        if x.stem in simbolos and rng.random() < 0.8:
            df, dd = modificar(pd.read_csv(x), rng, f1, hz, e)
            df.to_csv(d / x.name, index=False)
            if dd:
                desc[x.stem] = dd
        else:
            shutil.copyfile(x, d / x.name)
    return tmp, d, str(e.date()), hz, str(f1.date()), ref, desc


def ejecutar(tmp, d, e, hz, f1, ref):
    b = Bloque(config_pruebas(), ProveedorCSV(d), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "estado", tmp / "ent")
    b.fijar_fecha(e)
    ev = b.evaluador
    reg = {"tipo_entrada": "ALTA", "prg_id": "PRG-2026-0901", "opp_id": "OPP-1", "clase": "RV", "horizonte": hz,
           "estado": "ABIERTO", "prob_interna": 0.65, "sentido": "POSITIVO", "umbral": 0.0,
           "tipo_pronostico": "RELATIVO" if ref else "DIRECCIONAL", "referencia_indice": ref, "variable": {"serie_ht01": "SPY"},
           "fecha_emision": e, "fecha_resolucion": f1, "nivel_referencia": ev._base_conocida("SPY", e),
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
    usadas = {}
    orig = ev._rentabilidad_serie

    def espia(simbolo, f0, f1_, base=None):
        r = orig(simbolo, f0, f1_, base)
        usadas[simbolo] = r[2]
        return r
    ev._rentabilidad_serie = espia
    ev.resolver(str(asof.date()), "RUN-2026-0001")
    return reg, b.almacen.estado("F4")["PRG-2026-0901"], usadas


m = Marcador()
rng = random.Random(SEM)
n_res = n_esp = 0
viejos, distintos_oraculo, desalineados, alineables = [], [], [], 0
max_dif = (0, None)
por_hz = {h: [0, 0] for h in ("H1", "H2", "H3", "H4")}
for k in range(N):
    tmp, d, e, hz, f1, ref, desc = escenario(k, rng)
    try:
        out = ejecutar(tmp, d, e, hz, f1, ref)
        if out is None:
            continue
        reg, est, usadas = out
        series = {s: pd.read_csv(d / f"{s}.csv", parse_dates=["fecha"]).set_index("fecha")["cierre"]
                  for s in ["SPY"] + (["ACWI"] if ref == "ACWI" else RV if ref == "CESTA" else [])}
        bases_ref = (reg.get("bases_cesta") if ref == "CESTA" else
                     {"valor": reg["nivel_referencia_indice"], "fecha": reg["fecha_nivel_referencia_indice"]} if ref else None)
        o = Oraculo(series, hz, f1)
        try:
            rp, rr, d1, d1b = o.resolver(ref, bases_ref, reg["nivel_referencia"])
            esperado = ("RESUELTO", d1, d1b, rp - (rr or 0.0))
        except Espera:
            esperado = ("ABIERTO",)
        etiqueta = f"#{k} {hz} e={e} f1={f1} ref={ref} {desc}"
        if est["estado"] == "RESUELTO":
            n_res += 1
            por_hz[hz][0] += 1
            r = est["resolucion"]
            # 1 · frescura de cada dato usado en la medida final (espía: última medida de cada símbolo)
            bases = {"SPY": reg["nivel_referencia"]}
            if ref == "ACWI":
                bases["ACWI"] = bases_ref
            elif ref == "CESTA":
                bases.update(bases_ref)
            for s, b0 in bases.items():
                if s in usadas and not fresca(b0["fecha"], usadas[s], f1, hz):
                    viejos.append(f"{etiqueta}: {s} hasta {usadas[s].date()} (edad {edad(usadas[s], f1, hz)}, máx {LIM[hz]})")
            fechas = {s: usadas[s] for s in bases if s in usadas}
            if len(set(fechas.values())) > 1:
                dif = (max(fechas.values()) - min(fechas.values())).days
                desalineados.append(f"{etiqueta}: {({s: str(v.date()) for s, v in fechas.items()})}")
                if dif > max_dif[0]:
                    max_dif = (dif, etiqueta)
                try:
                    oi = Oraculo(series, hz, f1, iterar=True)
                    oi.resolver(ref, bases_ref, reg["nivel_referencia"])
                    alineables += int(len(set(oi.usadas.values())) == 1)
                except Espera:
                    pass
            obtenido = ("RESUELTO", pd.Timestamp(r["fecha_dato_proxy"]),
                        pd.Timestamp(r["fecha_dato_referencia"]) if r.get("fecha_dato_referencia") else None, r["valor_observado"])
        else:
            n_esp += 1
            por_hz[hz][1] += 1
            obtenido = (est["estado"],)
        igual = (obtenido[0] == esperado[0] and (len(obtenido) == 1 or (
            obtenido[1] == esperado[1] and obtenido[2] == esperado[2] and abs(obtenido[3] - esperado[3]) < 1e-8)))
        if not igual:
            distintos_oraculo.append(f"{etiqueta}: código {obtenido} · oráculo {esperado}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

print(f"   {N} escenarios: {n_res} RESUELTOS, {n_esp} en espera; por horizonte (resueltos, espera): {por_hz}")
m.check("1 · ningún RESUELTO con un dato sin posterior a la base o más viejo que PS2", not viejos,
        f"{len(viejos)}: {viejos[:4]}")
m.check("2 · el código coincide con el oráculo de la regla r02 (estado, fechas y exceso)", not distintos_oraculo,
        f"{len(distintos_oraculo)}: {distintos_oraculo[:4]}")
print(f"   3 · INFORMATIVO: RESUELTOS con series en fechas distintas tras alinear: {len(desalineados)} de {n_res}; "
      f"mayor diferencia {max_dif[0]} días ({max_dif[1]}); con la alineación iterada quedarían alineados {alineables}")
for x in desalineados[:6]:
    print("     ", x)
sys.exit(m.fin())
