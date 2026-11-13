"""QA r02 de T-91 · 03: casos fijos en los que, tras alinear, proxy y referencia (o la CESTA) siguen acabando en fechas
distintas (H-05 de la r02). Reproducción corta de lo que r02_01 encuentra al azar.

  .venv/bin/python -I .docs/tickets/T-91/revisores/r02_03_desalineacion.py [--ejecutor RUTA_11_EJECUTOR]

Casos (PRG RV, SPY; emisión y resolución indicadas; se resuelve dos sesiones después):
  1 · H2, ACWI parada el 2026-04-29 y SPY sin el dato de ese día (el de `test_r02_h02_b`): SPY 04-28 · ACWI 04-29;
  2 · H3, resolución el 2026-05-14 (Ascensión: SPY sin dato ese día, como una bolsa europea) y ACWI sin el dato del 05-13;
  3 · H2, emisión 2025-12-19 y resolución 2026-01-02: SPY con los festivos de PS2 (sin 31-12 ni 01-01) y ACWI parada el 01-01;
  4 · H4 frente a la CESTA, resolución 2026-07-17: XLI parada el 07-11, XLK sin datos del 07-03 al 07-11, XLE sin datos del
      06-23 al 07-02.
Esperado según el criterio congelado en cada PRG («si las series acaban en fechas distintas, todas se miden hasta la más
antigua») y el objetivo de H-27 (el suceso sobre la misma ventana): las series usadas acaban en la misma fecha. Se informa
también de la fecha que daría repetir la alineación hasta que coincidan."""
import shutil
import sys
import tempfile
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "T-88" / "revisores"))
from r01_comun import Marcador, preparar  # noqa: E402

a, resto, ej = preparar(__doc__)
import pandas as pd  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402
from conftest import DATOS, config_pruebas  # noqa: E402

FEST = ["2025-12-24", "2025-12-25", "2025-12-26", "2025-12-31", "2026-01-01"]


def sin(fechas):
    return lambda df: df[~df["fecha"].isin(fechas)]


def hueco(desde, hasta):
    return lambda df: df[(df["fecha"] < desde) | (df["fecha"] > hasta)]


def parar(f):
    return lambda df: df[df["fecha"] <= f]


CASOS = [
    ("1 H2 hueco de un día en la fecha común", "2026-04-17", "H2", "2026-05-01", "ACWI",
     {"ACWI": [parar("2026-04-29")], "SPY": [sin(["2026-04-29"])]}),
    ("2 H3 Ascensión en el proxy y un dato que falta en la referencia", "2026-04-17", "H3", "2026-05-14", "ACWI",
     {"SPY": [sin(["2026-05-14"])], "ACWI": [sin(["2026-05-13"])]}),
    ("3 H2 fin de año: festivos de PS2 en el proxy y referencia parada el 1 de enero", "2025-12-19", "H2", "2026-01-02", "ACWI",
     {"SPY": [sin(FEST)], "ACWI": [parar("2026-01-01")]}),
    ("4 H4 CESTA con un miembro parado y dos con huecos", "2026-04-17", "H4", "2026-07-17", "CESTA",
     {"XLI": [parar("2026-07-11")], "XLK": [hueco("2026-07-03", "2026-07-11")], "XLE": [hueco("2026-06-23", "2026-07-02")]}),
]

m = Marcador()
for nombre, e, hz, f1, ref, cambios in CASOS:
    tmp = Path(tempfile.mkdtemp(prefix="qa_t91_r02_03_"))
    d = tmp / "datos"
    shutil.copytree(DATOS, d)
    for s, fs in cambios.items():
        df = pd.read_csv(d / f"{s}.csv")
        for f in fs:
            df = f(df)
        df.to_csv(d / f"{s}.csv", index=False)
    b = Bloque(config_pruebas(), ProveedorCSV(d), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "estado", tmp / "ent")
    b.fijar_fecha(e)
    ev = b.evaluador
    reg = {"tipo_entrada": "ALTA", "prg_id": "PRG-2026-0901", "opp_id": "OPP-1", "clase": "RV", "horizonte": hz,
           "estado": "ABIERTO", "prob_interna": 0.65, "sentido": "POSITIVO", "umbral": 0.0, "tipo_pronostico": "RELATIVO",
           "referencia_indice": ref, "variable": {"serie_ht01": "SPY"}, "fecha_emision": e, "fecha_resolucion": f1,
           "nivel_referencia": ev._base_conocida("SPY", e), "referencia_ingenua": {"valor_o_prob": 0.5}, "en_informe": True}
    if ref == "CESTA":
        reg["bases_cesta"] = ev.bases_cesta("RV", e, hz)
    else:
        base = ev._base_conocida(ref, e)
        reg["nivel_referencia_indice"], reg["fecha_nivel_referencia_indice"] = base["valor"], base["fecha"]
    b.almacen.escribir("F4", "AG-10", reg)
    asof = str((pd.Timestamp(f1) + pd.offsets.BDay(2)).date())
    b.fijar_fecha(asof)
    usadas = {}
    orig = ev._rentabilidad_serie

    def espia(simbolo, f0, f1_, base=None, _o=orig, _u=usadas):
        r = _o(simbolo, f0, f1_, base)
        _u[simbolo] = str(r[2].date())
        return r
    ev._rentabilidad_serie = espia
    ev.resolver(asof, "RUN-2026-0001")
    est = b.almacen.estado("F4")["PRG-2026-0901"]
    fechas = sorted(set(usadas.values()))
    # alineación repetida: todas las series hasta la más antigua de las usadas, hasta que coincidan
    comun = min(fechas)
    for _ in range(5):
        nuevas = {s: str(ev.proveedor.valor_en(s, comun)[0].date()) for s in usadas}
        if min(nuevas.values()) == comun:
            break
        comun = min(nuevas.values())
    print(f"   {nombre}: {est['estado']} · fechas usadas {usadas}" + (f" · fecha_dato {est['resolucion'].get('fecha_dato')}"
                                                                      if est["estado"] == "RESUELTO" else "")
          + f" · repitiendo la alineación, todas hasta {comun}")
    m.check(f"{nombre}: RESUELTO con todas las series en la misma fecha, o en espera",
            est["estado"] != "RESUELTO" or len(fechas) == 1, f"{len(fechas)} fechas distintas: {fechas}")
    shutil.rmtree(tmp, ignore_errors=True)
sys.exit(m.fin())
