"""QA r03 de T-91 (revisor nuevo) · 02: el bucle de alineación y su salvaguarda, y calendarios sin fechas comunes.

  .venv/bin/python -I .docs/tickets/T-91/revisores/r03_02_bucle_y_calendarios.py [--ejecutor RUTA_11_EJECUTOR] [partes]

Partes:
  G · salvaguarda «la fecha común no baja»: con un proveedor que ignora `hasta` (devuelve siempre su último cierre <= f1),
      la resolución debe terminar (alarma de 20 s) y dejar el PRG en espera; también dentro de la CESTA;
  S · con un proveedor correcto la salvaguarda no se dispara nunca (espía de `DatosNoDisponibles` con su texto) en 200
      escenarios del oráculo de r03_01 (se importa su generador): es inalcanzable, así que quitarla es un mutante equivalente
      con datos de HT-01 bien formados;
  C · INFORMATIVO: proxy diario y referencia semanal fechada en sábado (sin ninguna fecha común): con la regla r03 el PRG no se
      resuelve nunca (queda NO_RESOLUBLE pasado el plazo); se imprime qué pasa;
  D · caso fijo para el bucle de la CESTA: el proxy (SPY) para el 29-04; en la CESTA de RV un miembro para el 30-04 y otro no
      tiene el 30-04; H2 con resolución el 01-05. Una sola vuelta dentro de la CESTA la deja en 30-04/29-04 y el proxy, en
      29-04, coincide con su mínimo, así que el bucle de fuera no la corrige. Esperado: RESUELTO con TODOS los miembros en
      29-04 y el exceso igual al del oráculo (todas las series en 29-04).
Por defecto, todas."""
import signal
import sys
import tempfile
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "T-88" / "revisores"))
from r01_comun import Marcador, preparar  # noqa: E402

a, resto, ej = preparar(__doc__)
partes = [x for x in resto if not x.startswith("--")] or ["G", "S", "C", "D"]

import pandas as pd  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import DatosNoDisponibles, ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402
from conftest import DATOS, config_pruebas  # noqa: E402

m = Marcador()


class Alarma(Exception):
    pass


def _al(*_):
    raise Alarma()


signal.signal(signal.SIGALRM, _al)
E0 = "2026-04-17"


def nuevo(datos=DATOS):
    tmp = Path(tempfile.mkdtemp(prefix="qa_t91_r03b_"))
    return Bloque(config_pruebas(), ProveedorCSV(datos), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "estado", tmp / "ent")


def prg(b, ref, hz, f1, clase="RV"):
    b.fijar_fecha(E0)
    ev = b.evaluador
    reg = {"tipo_entrada": "ALTA", "prg_id": "PRG-2026-0901", "opp_id": "OPP-1", "clase": clase, "horizonte": hz,
           "estado": "ABIERTO", "prob_interna": 0.65, "sentido": "POSITIVO", "umbral": 0.0, "tipo_pronostico": "RELATIVO",
           "referencia_indice": ref, "variable": {"serie_ht01": "SPY"}, "fecha_emision": E0, "fecha_resolucion": f1,
           "nivel_referencia": ev._base_conocida("SPY", E0), "referencia_ingenua": {"valor_o_prob": 0.5}, "en_informe": True}
    if ref == "CESTA":
        reg["bases_cesta"] = ev.bases_cesta(clase, E0, hz)
    else:
        bb = ev._base_conocida(ref, E0)
        reg["nivel_referencia_indice"], reg["fecha_nivel_referencia_indice"] = bb["valor"], bb["fecha"]
    b.almacen.escribir("F4", "AG-10", reg)


def resolver(b, asof):
    b.fijar_fecha(asof)
    signal.alarm(20)
    try:
        b.evaluador.resolver(asof, "RUN-2026-0001")
    finally:
        signal.alarm(0)
    return b.almacen.estado("F4")["PRG-2026-0901"]


if "G" in partes:
    for ref in ("ACWI", "CESTA"):
        b = nuevo()
        prg(b, ref, "H2", "2026-05-01")
        orig = b.proveedor.valor_en
        # proveedor defectuoso: ignora la fecha pedida si es anterior a f1 y devuelve su último cierre <= f1; el SPY, además,
        # «pierde» el 1 de mayo para que las series no coincidan en la primera pasada
        def malo(simbolo, fecha, _o=orig):
            f = pd.Timestamp(fecha)
            if f < pd.Timestamp("2026-05-01") and f >= pd.Timestamp("2026-04-20"):
                f = pd.Timestamp("2026-05-01")
            d, v = _o(simbolo, f)
            if simbolo == "SPY" and d == pd.Timestamp("2026-05-01"):
                d, v = _o(simbolo, "2026-04-30")
            return d, v
        b.proveedor.valor_en = malo
        try:
            e = resolver(b, "2026-05-05")
            m.check(f"G · {ref}: con un proveedor que ignora `hasta`, la resolución acaba y espera", e["estado"] == "ABIERTO", e["estado"])
        except Alarma:
            m.check(f"G · {ref}: con un proveedor que ignora `hasta`, la resolución acaba y espera", False, "se cuelga (> 20 s)")

if "S" in partes:
    import random
    sys.argv = [sys.argv[0], "--ejecutor", str(ej), "--n=0"]
    import importlib.util
    spec = importlib.util.spec_from_file_location("r03_01", Path(__file__).resolve().parent / "r03_01_oraculo_fecha_comun.py")
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except SystemExit:
        pass
    import bloque_a.evaluador as evm
    disparos = []
    orig_init = DatosNoDisponibles.__init__

    def espia_init(self, *args, **kw):
        if args and "no se alinean" in str(args[0]):
            disparos.append(str(args[0]))
        orig_init(self, *args, **kw)
    DatosNoDisponibles.__init__ = espia_init
    rng = random.Random(7)
    n = 0
    for _ in range(200):
        tmp, d, e, hz, f1, ref, desc = mod.escenario(rng)
        try:
            if mod.ejecutar(tmp, d, e, hz, f1, ref) is not None:
                n += 1
        finally:
            import shutil
            shutil.rmtree(tmp, ignore_errors=True)
    DatosNoDisponibles.__init__ = orig_init
    m.check(f"S · con datos bien formados la salvaguarda no se dispara ({n} resoluciones)", not disparos, f"{len(disparos)}: {disparos[:3]}")

if "C" in partes:
    tmp = Path(tempfile.mkdtemp(prefix="qa_t91_r03c_"))
    datos = tmp / "datos"
    datos.mkdir()
    for x in DATOS.iterdir():
        df = pd.read_csv(x)
        if x.stem == "ACWI":
            f = pd.to_datetime(df["fecha"])
            antes = df[f <= pd.Timestamp(E0)]
            desp = df[(f > pd.Timestamp(E0)) & (f.dt.weekday == 4)].copy()   # semanal: el viernes, fechado el sábado
            desp["fecha"] = (pd.to_datetime(desp["fecha"]) + pd.Timedelta(days=1)).dt.strftime("%Y-%m-%d")
            df = pd.concat([antes, desp])
        df.to_csv(datos / x.name, index=False)
    for hz, f1 in (("H3", "2026-05-15"), ("H4", "2026-06-01")):
        b = nuevo(datos)
        prg(b, "ACWI", hz, f1)
        estados = []
        for asof in pd.bdate_range(pd.Timestamp(f1) + pd.Timedelta(days=1), periods=25):
            estados.append(resolver(b, str(asof.date()))["estado"])
            if estados[-1] != "ABIERTO":
                break
        print(f"   C · {hz} f1={f1}, ACWI semanal fechada en sábado: {estados[-1]} tras {len(estados)} sesiones "
              f"(regla r03: sin fecha común no se resuelve nunca)")
if "D" in partes:
    tmp = Path(tempfile.mkdtemp(prefix="qa_t91_r03d_"))
    datos = tmp / "datos"
    datos.mkdir()
    rv = sorted(cargar_universo(RUTA_UNIVERSO_EJEMPLO).query("clase == 'RV'")["simbolo"])
    rv = [x for x in rv if x != "SPY"]
    para_30, sin_30 = rv[0], rv[1]
    for x in DATOS.iterdir():
        df = pd.read_csv(x)
        f = pd.to_datetime(df["fecha"])
        if x.stem == "SPY":
            df = df[f <= pd.Timestamp("2026-04-29")]
        elif x.stem == para_30:
            df = df[f <= pd.Timestamp("2026-04-30")]
        elif x.stem == sin_30:
            df = df[f != pd.Timestamp("2026-04-30")]
        df.to_csv(datos / x.name, index=False)
    b = nuevo(datos)
    prg(b, "CESTA", "H2", "2026-05-01")
    usadas = {}
    orig = b.evaluador._rentabilidad_serie

    def espia(simbolo, f0, f1_, base=None, _o=orig):
        r = _o(simbolo, f0, f1_, base)
        usadas[simbolo] = (r[2], r[0])
        return r
    b.evaluador._rentabilidad_serie = espia
    e = resolver(b, "2026-05-05")
    reg = b.almacen.estado("F4")["PRG-2026-0901"]
    fechas = {s: str(v[0].date()) for s, v in usadas.items()}
    bases = reg["bases_cesta"]
    g = pd.Timestamp("2026-04-29")
    serie = {s: pd.read_csv(datos / f"{s}.csv", parse_dates=["fecha"]).set_index("fecha")["cierre"] for s in ["SPY", *bases]}
    rp = float(serie["SPY"][g]) / reg["nivel_referencia"]["valor"] - 1
    rr = sum(float(serie[s][g]) / b0["valor"] - 1 for s, b0 in bases.items()) / len(bases)
    ok = e["estado"] == "RESUELTO" and set(fechas.values()) == {"2026-04-29"} and abs(e["resolucion"]["valor_observado"] - (rp - rr)) <= 5.1e-9
    m.check("D · CESTA con dos huecos encadenados: todas las series en 29-04 y exceso del oráculo", ok,
            f"estado={e['estado']} fechas={fechas} valor={e.get('resolucion', {}).get('valor_observado')} oráculo={rp - rr:.8f}")
sys.exit(m.fin())
