"""QA r01 de T-91 (revisor nuevo) · 01: ataques a la resolución de pronósticos (H-26 a H-28).

  .venv/bin/python -I .docs/tickets/T-91/revisores/r01_01_resolucion_ataques.py [--ejecutor RUTA_11_EJECUTOR] [partes]

Partes (todas por defecto):
  A · calendario: `_sesiones_entre` frente a un cálculo propio (dateutil.easter) en 20.000 pares de fechas de 1999 a 2046 con
      tres juegos de festivos, y bordes de PS2 en H1 en Navidad, fin de año y Pascua de 2025 a 2030;
  H · alineación con huecos: una serie parada dentro de la tolerancia y la otra con un hueco justo antes de esa fecha
      (proxy/referencia, H2 y H4; y dos miembros de la CESTA). Esperado (README de T-91 y INC-T91-01): RESUELTO con las dos
      series medidas hasta la misma fecha, o en espera; nunca un dato más viejo que PS2;
  C · CESTA con un miembro parado: dentro de la tolerancia, en la emisión, más allá de la tolerancia y ya viejo al emitir;
  O · PRG antiguos: CESTA sin `bases_cesta` congeladas (debe dar lo mismo que con ellas), nivel de la referencia como número
      suelto con la referencia parada, y nivel del proxy como número suelto;
  B · backtest corto (RV y DIV, 2026-03-06 a 2026-06-26): `pronosticos.csv` con las columnas anteriores en su sitio, las dos
      nuevas al final y coherentes con F4, y el criterio y la regla congelados en cada PRG nuevo (también los hitos)."""
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
PARTES = {x for x in resto if len(x) == 1} or set("AHCOB")

import pandas as pd  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402
from conftest import DATOS, config_pruebas  # noqa: E402

try:
    from bloque_a.calendario import _sesiones_entre
except ImportError:   # 7feb697^
    from bloque_a.orquestacion import _sesiones_entre
m = Marcador()
EMISION = "2026-04-17"
LIM = cargar_config()["ps2_antiguedad_maxima_dias"]


def datos_mod(cambios: dict) -> Path:
    """cambios: simbolo -> función(df) -> df."""
    tmp = Path(tempfile.mkdtemp(prefix="qa_t91_"))
    d = tmp / "datos"
    shutil.copytree(DATOS, d)
    for s, f in cambios.items():
        df = pd.read_csv(d / f"{s}.csv")
        f(df).to_csv(d / f"{s}.csv", index=False)
    return d


def parar(fecha):
    return lambda df: df[df["fecha"] <= fecha]


def hueco(desde, hasta):
    return lambda df: df[(df["fecha"] < desde) | (df["fecha"] > hasta)]


def nuevo(datos=DATOS, cfg=None):
    tmp = Path(tempfile.mkdtemp(prefix="qa_t91_b_"))
    return Bloque(cfg or config_pruebas(), ProveedorCSV(datos), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(),
                  tmp / "estado", tmp / "ent")


def prg(b, hz, resolucion, proxy="SPY", ref="ACWI", clase="RV", extra=None, quitar=()):
    b.fijar_fecha(EMISION)
    e = {"tipo_entrada": "ALTA", "prg_id": "PRG-2026-0901", "opp_id": "OPP-1", "clase": clase, "horizonte": hz,
         "estado": "ABIERTO", "prob_interna": 0.65, "sentido": "POSITIVO", "umbral": 0.0,
         "tipo_pronostico": "RELATIVO" if ref else "DIRECCIONAL", "referencia_indice": ref, "variable": {"serie_ht01": proxy},
         "fecha_emision": EMISION, "fecha_resolucion": resolucion, "nivel_referencia": b.evaluador._base_conocida(proxy, EMISION),
         "referencia_ingenua": {"valor_o_prob": 0.5}, "en_informe": True}
    if ref == "CESTA":
        e["bases_cesta"] = b.evaluador.bases_cesta(clase, EMISION, hz)
    elif ref:
        base = b.evaluador._base_conocida(ref, EMISION)
        e["nivel_referencia_indice"], e["fecha_nivel_referencia_indice"] = base["valor"], base["fecha"]
    e.update(extra or {})
    for k in quitar:
        e.pop(k, None)
    b.almacen.escribir("F4", "AG-10", e)


def resolver(b, fecha):
    b.fijar_fecha(fecha)
    llamadas = []
    orig = b.evaluador._rentabilidad_serie

    def espia(simbolo, f0, f1, base=None):
        r = orig(simbolo, f0, f1, base)
        llamadas.append((simbolo, str(pd.Timestamp(f1).date()), str(r[2].date())))
        return r
    b.evaluador._rentabilidad_serie = espia
    try:
        b.evaluador.resolver(fecha, "RUN-2026-0001")
    finally:
        b.evaluador._rentabilidad_serie = orig
    return b.almacen.estado("F4")["PRG-2026-0901"], llamadas


def ultimas_fechas(llamadas):
    """Fecha del último dato usado por símbolo en la última medición de cada uno."""
    out = {}
    for s, _, d in llamadas:
        out[s] = d
    return out


def edad(ev, d, f1, hz):
    """Antigüedad como la cuenta PS2 (calendario de HEAD también para la base, para comparar)."""
    from bloque_a.configuracion import parametro
    try:
        from bloque_a.calendario import validar_festivos_ps2
    except ImportError:
        from bloque_a.orquestacion import validar_festivos_ps2
    if hz == "H1":
        return _sesiones_entre(d, f1, validar_festivos_ps2(parametro(ev.cfg, "ps2_festivos")))
    return (pd.Timestamp(f1) - pd.Timestamp(d)).days


# ------------------------------------------------------------------------------------------------- A · calendario
if "A" in PARTES:
    from dateutil.easter import easter

    def propio(d0, d1, fest):
        d0, d1 = pd.Timestamp(d0).normalize(), pd.Timestamp(d1).normalize()
        n, d = 0, d0
        while d < d1:
            e = pd.Timestamp(easter(d.year))
            cerrado = (d.weekday() >= 5 or d.strftime("%m-%d") in fest["fijos"]
                       or (fest["viernes_santo"] and d == e - pd.Timedelta(days=2))
                       or (fest["lunes_de_pascua"] and d == e + pd.Timedelta(days=1)))
            n += 0 if cerrado else 1
            d += pd.Timedelta(days=1)
        return n
    juegos = [{"viernes_santo": True, "lunes_de_pascua": False, "fijos": ["01-01", "12-24", "12-25", "12-26", "12-31"]},
              {"viernes_santo": True, "lunes_de_pascua": True, "fijos": ["01-01", "05-01", "12-24", "12-25", "12-26", "12-31"]},
              {"viernes_santo": False, "lunes_de_pascua": True, "fijos": ["02-29", "07-04"]}]
    rnd = random.Random(20261112)
    malos = []
    for k in range(20000):
        fest = juegos[k % 3]
        d0 = pd.Timestamp("1999-01-01") + pd.Timedelta(days=rnd.randrange(0, 47 * 365))
        d1 = d0 + pd.Timedelta(days=rnd.choice([0, 1, 2, 3, 4, 5, 6, 7, 9, 12, 20, 40, 400]) * (1 if k % 17 else -1))
        x, y = _sesiones_entre(d0, d1, fest), propio(d0, d1, fest)
        if x != y:
            malos.append((str(d0.date()), str(d1.date()), x, y))
    m.check("A: _sesiones_entre = cálculo propio en 20.000 pares (1999–2046, 3 juegos)", not malos, f"{len(malos)} distintos: {malos[:5]}")
    b = nuevo(cfg=config_pruebas(ps2_festivos=juegos[1]))
    ev = b.evaluador
    bordes = []
    for anio in range(2025, 2031):
        e = pd.Timestamp(easter(anio))
        casos = [(f"{anio}-12-23", f"{anio}-12-27"), (f"{anio}-12-30", f"{anio + 1}-01-02"),
                 (str((e - pd.Timedelta(days=3)).date()), str((e + pd.Timedelta(days=1)).date())),
                 (str((e - pd.Timedelta(days=3)).date()), str((e + pd.Timedelta(days=2)).date()))]
        for ultimo, res in casos:
            ultimo_habil = pd.Timestamp(ultimo)
            while ultimo_habil.weekday() >= 5:
                ultimo_habil -= pd.Timedelta(days=1)
            esperado = propio(ultimo_habil, res, juegos[1])
            motivo = ev.motivo_no_fresca("2020-01-01", ultimo_habil, res, "H1")
            if (motivo is None) != (esperado <= LIM["H1"]):
                bordes.append((str(ultimo_habil.date()), res, esperado, motivo))
    m.check("A: motivo_no_fresca en H1 sigue al calendario de PS2 en Navidad, fin de año y Pascua 2025–2030", not bordes, str(bordes[:4]))
    # Mismo calendario al emitir (PS2 en _puertas) y al resolver
    from bloque_a import orquestacion
    m.check("A: PS2 al emitir y la resolución usan la misma función", getattr(orquestacion, "_sesiones_entre", None) is _sesiones_entre)

# ------------------------------------------------------------------------------------------------- H · huecos
if "H" in PARTES:
    casos = [
        # (nombre, hz, resolución, fecha de resolución real, cambios, ref, clase, proxy)
        ("H2 ref parada 04-29, proxy con hueco 04-21..04-29", "H2", "2026-05-01", "2026-05-04",
         {"ACWI": parar("2026-04-29"), "SPY": hueco("2026-04-21", "2026-04-29")}, "ACWI", "RV", "SPY"),
        ("H2 proxy parado 04-29, ref con hueco 04-22..04-29", "H2", "2026-05-01", "2026-05-04",
         {"SPY": parar("2026-04-29"), "ACWI": hueco("2026-04-22", "2026-04-29")}, "ACWI", "RV", "SPY"),
        ("H4 ref parada 20 días antes, proxy con hueco de 25 días antes", "H4", "2026-07-17", "2026-07-20",
         {"ACWI": parar("2026-06-26"), "SPY": hueco("2026-06-01", "2026-06-26")}, "ACWI", "RV", "SPY"),
    ]
    for nombre, hz, fr, hoy, cambios, ref, clase, proxy in casos:
        b = nuevo(datos_mod(cambios))
        prg(b, hz, fr, proxy=proxy, ref=ref, clase=clase)
        e, ll = resolver(b, hoy)
        r = e.get("resolucion") or {}
        if e["estado"] != "RESUELTO":
            m.check(f"H {nombre}: espera (aceptable)", True, e["estado"])
            continue
        dp, dr = r.get("fecha_dato_proxy"), r.get("fecha_dato_referencia")
        print(f"   {nombre}: RESUELTO · proxy hasta {dp} · referencia hasta {dr} · edad PS2 proxy {edad(b.evaluador, dp, fr, hz)} "
              f"(máx. {LIM[hz]})")
        m.check(f"H {nombre}: proxy y referencia medidos hasta la misma fecha", dp == dr, f"{dp} vs {dr}")
        m.check(f"H {nombre}: ningún dato usado más viejo que PS2", max(edad(b.evaluador, dp, fr, hz), edad(b.evaluador, dr, fr, hz)) <= LIM[hz],
                f"edades {edad(b.evaluador, dp, fr, hz)} / {edad(b.evaluador, dr, fr, hz)}")
    # CESTA: un miembro parado dentro de la tolerancia y otro con un hueco justo antes
    b0 = nuevo()
    b0.fijar_fecha("2026-06-05")
    mi = b0.evaluador.simbolos_clase("DIV")
    b = nuevo(datos_mod({mi[0]: parar("2026-04-29"), mi[1]: hueco("2026-04-22", "2026-04-29")}))
    prg(b, "H2", "2026-05-01", proxy=mi[2], ref="CESTA", clase="DIV")
    e, ll = resolver(b, "2026-05-04")
    r = e.get("resolucion") or {}
    fechas = ultimas_fechas(ll)
    if e["estado"] == "RESUELTO":
        miembros = {s: fechas.get(s) for s in mi if s in (e.get("bases_cesta") or {})}
        print(f"   CESTA con un miembro parado y otro con hueco: RESUELTO · fechas por miembro {miembros} · proxy {r.get('fecha_dato_proxy')}"
              f" · referencia {r.get('fecha_dato_referencia')}")
        m.check("H CESTA: todos los miembros medidos hasta la misma fecha", len(set(miembros.values())) == 1, str(miembros))
        m.check("H CESTA: proxy y CESTA hasta la misma fecha", r.get("fecha_dato_proxy") == r.get("fecha_dato_referencia"))
        edades = {s: edad(b.evaluador, d, "2026-05-01", "H2") for s, d in miembros.items()}
        m.check("H CESTA: ningún miembro medido con un dato más viejo que PS2", max(edades.values()) <= LIM["H2"],
                f"edades {edades} (máx. {LIM['H2']})")
    else:
        m.check("H CESTA: espera (aceptable)", True, e["estado"])

# ------------------------------------------------------------------------------------------------- C · CESTA con un miembro parado
if "C" in PARTES:
    b0 = nuevo()
    b0.fijar_fecha("2026-06-05")
    mi = b0.evaluador.simbolos_clase("DIV")
    proxy = mi[-1]
    for nombre, parada, hoy, esperado in [
        ("dentro de la tolerancia (2 días en H2)", "2026-04-29", "2026-05-04", "RESUELTO"),
        ("en la emisión", EMISION, "2026-05-04", "ABIERTO"),
        ("en la emisión, pasado el plazo", EMISION, "2026-06-05", "NO_RESOLUBLE"),
        ("más allá de la tolerancia (6 días en H2)", "2026-04-24", "2026-05-04", "ABIERTO"),
    ]:
        b = nuevo(datos_mod({mi[0]: parar(parada)}))
        prg(b, "H2", "2026-05-01", proxy=proxy, ref="CESTA", clase="DIV")
        e, ll = resolver(b, hoy)
        ok = e["estado"] == esperado
        det = e["estado"]
        if e["estado"] == "RESUELTO":
            f = ultimas_fechas(ll)
            usados = {s: f.get(s) for s in e["bases_cesta"]}
            ok = ok and set(usados.values()) == {parada} and e["resolucion"]["fecha_dato_proxy"] == parada
            det += f" · fechas {sorted(set(usados.values()))} · proxy {e['resolucion']['fecha_dato_proxy']}"
        m.check(f"C miembro parado {nombre}: {esperado}", ok, det)
    # Ya viejo al emitir: queda fuera de las bases (H1, 1 sesión)
    b = nuevo(datos_mod({mi[0]: parar("2026-04-14")}))
    prg(b, "H1", "2026-04-24", proxy=proxy, ref="CESTA", clase="DIV")
    e, ll = resolver(b, "2026-04-27")
    m.check("C miembro ya viejo al emitir: fuera de las bases congeladas y el PRG se resuelve",
            mi[0] not in e["bases_cesta"] and e["estado"] == "RESUELTO", f"{e['estado']} · bases {sorted(e['bases_cesta'])}")

# ------------------------------------------------------------------------------------------------- O · PRG antiguos
if "O" in PARTES:
    b0 = nuevo()
    b0.fijar_fecha("2026-06-05")
    mi = b0.evaluador.simbolos_clase("DIV")
    res = {}
    for nombre, quitar in (("con bases", ()), ("sin bases", ("bases_cesta",))):
        b = nuevo(datos_mod({mi[0]: parar("2026-04-29")}))
        prg(b, "H2", "2026-05-01", proxy=mi[-1], ref="CESTA", clase="DIV", quitar=quitar)
        e, _ = resolver(b, "2026-05-04")
        res[nombre] = (e["estado"], (e.get("resolucion") or {}).get("valor_observado"), (e.get("resolucion") or {}).get("fecha_dato_referencia"))
    m.check("O CESTA sin bases congeladas da lo mismo que con ellas", res["con bases"] == res["sin bases"], str(res))
    # Nivel de la referencia como número suelto, sin fecha, y referencia parada dentro de la tolerancia
    b = nuevo(datos_mod({"ACWI": parar("2026-04-29")}))
    base_ref = b.evaluador._base_conocida("ACWI", EMISION) if b.fijar_fecha(EMISION) is not None else None
    prg(b, "H2", "2026-05-01", extra={"nivel_referencia_indice": base_ref["valor"]}, quitar=("fecha_nivel_referencia_indice",))
    try:
        e, _ = resolver(b, "2026-05-04")
        r = e.get("resolucion") or {}
        m.check("O referencia con nivel suelto: RESUELTO y alineado", e["estado"] == "RESUELTO" and r.get("fecha_dato_proxy") == r.get("fecha_dato_referencia") == "2026-04-29",
                f"{e['estado']} {r.get('fecha_dato_proxy')} {r.get('fecha_dato_referencia')}")
    except Exception as ex:   # noqa: BLE001
        m.check("O referencia con nivel suelto: no rompe la resolución", False, f"{type(ex).__name__}: {ex}")
    # Nivel del proxy como número suelto (registros anteriores a T-92)
    b = nuevo()
    b.fijar_fecha(EMISION)
    v = b.evaluador._base_conocida("SPY", EMISION)["valor"]
    prg(b, "H2", "2026-05-01", extra={"nivel_referencia": v})
    try:
        e, _ = resolver(b, "2026-05-04")
        m.check("O proxy con nivel suelto: no rompe la resolución", True, e["estado"])
    except Exception as ex:   # noqa: BLE001
        m.check("O proxy con nivel suelto: no rompe la resolución (¿anterior a T-91?)", False, f"{type(ex).__name__}: {str(ex)[:80]}")

# ------------------------------------------------------------------------------------------------- B · backtest y pronosticos.csv
if "B" in PARTES:
    import csv

    from bloque_a.backtest import COLUMNAS_PRONOSTICOS, ejecutar_backtest
    sal = Path(tempfile.mkdtemp(prefix="qa_t91_bt_")) / "salida"
    cfg = config_pruebas(perfiles={"activos": ["RV", "DIV"]})
    ejecutar_backtest(cfg, "2026-03-06", "2026-06-26", str(DATOS), str(RUTA_UNIVERSO_EJEMPLO), str(sal))
    filas = list(csv.DictReader(open(sal / "pronosticos.csv", encoding="utf-8")))
    cab = next(csv.reader(open(sal / "pronosticos.csv", encoding="utf-8")))
    print(f"   backtest: {len(filas)} PRG · estados {pd.Series([f['estado'] for f in filas]).value_counts().to_dict()} · salida {sal}")
    try:
        from bloque_a.sintesis import CRITERIO_RESOLUCION, REGLA_FALLBACK
    except ImportError:
        CRITERIO_RESOLUCION = REGLA_FALLBACK = None
    anteriores = ["prg_id", "opp_id", "run_id", "fecha_emision", "clase", "simbolo", "horizonte", "fecha_resolucion", "tipo_pronostico",
                  "direccion", "referencia", "umbral", "banda_verbal", "prob_interna", "prob_publicada", "prob_referencia_ingenua",
                  "nivel_referencia", "nivel_referencia_indice", "en_informe", "estado", "fecha_resuelto", "rent_proxy",
                  "rent_referencia", "valor_observado", "resultado_binario", "brier", "log_score", "brier_ref", "comprobacion_fuga",
                  "version_de"]
    m.check("B: las 30 columnas anteriores siguen en su sitio", cab[:30] == anteriores)
    m.check("B: las dos nuevas, al final", cab[30:] == ["fecha_dato_proxy", "fecha_dato_referencia"] and cab == COLUMNAS_PRONOSTICOS, str(cab[30:]))
    res = [f for f in filas if f["estado"] == "RESUELTO"]
    m.check("B: cada RESUELTO lleva fecha_dato_proxy", all(f["fecha_dato_proxy"] for f in res) and bool(res), f"{len(res)} resueltos")
    rel = [f for f in res if f["tipo_pronostico"] == "RELATIVO"]
    m.check("B: cada RELATIVO resuelto lleva las dos fechas, iguales", all(f["fecha_dato_referencia"] and f["fecha_dato_referencia"] == f["fecha_dato_proxy"] for f in rel),
            f"{len(rel)} relativos")
    m.check("B: los no resueltos dejan las dos fechas vacías", all(not f["fecha_dato_proxy"] and not f["fecha_dato_referencia"] for f in filas if f["estado"] != "RESUELTO"))
    if CRITERIO_RESOLUCION:
        import json
        f4 = [json.loads(x) for x in open(sal / "estado" / "F4_registro_pronosticos.jsonl", encoding="utf-8")]
        altas = [e for e in f4 if e.get("tipo_entrada") == "ALTA"]
        prefijo = CRITERIO_RESOLUCION.split("{fin}")[0]
        sufijo_regla = REGLA_FALLBACK.format(dias_nr=int(cfg["evaluacion"]["dias_habiles_no_resoluble"]))
        malos = [e["prg_id"] for e in altas if not str(e.get("criterio_resolucion", "")).startswith(prefijo)
                 or "la más antigua" not in e.get("criterio_resolucion", "")
                 or (not e.get("es_hito") and e.get("regla_fallback") != sufijo_regla)]
        hitos = [e for e in altas if e.get("es_hito")]
        m.check("B: criterio y regla congelados con la regla nueva en cada PRG nuevo (hitos incluidos)", bool(altas) and not malos,
                f"{len(altas)} altas ({len(hitos)} hitos); malos {malos[:5]}")
        m.check("B: los hitos congelan también la regla de respaldo nueva", all(e.get("regla_fallback") == sufijo_regla for e in hitos),
                str({e.get("regla_fallback") for e in hitos}))
sys.exit(m.fin())
