"""Banco de medida (T-94): el diseño actual de un bloque de búsqueda o selección frente a referencias baratas.

Compara, con los mismos datos y las mismas fechas de corte, lo que elige el titular (hoy, el Bloque A en modo backtest)
con dos referencias: azar con semilla y momento (solo código, sin datos posteriores al corte). Mide calidad (exceso frente
a la cesta de la clase, con rango por remuestreo) y coste (llamadas, tokens y coste estimado). Antes de evaluar sella un
prerregistro con su huella. No modifica ningún bloque ni el marco común: solo importa A para ejecutarlo.

Uso (desde la raíz del repositorio):
  .venv/bin/python .docs/scripts/banco_medida.py a --desde 2026-03-06 --hasta 2026-05-29 --salida <carpeta>
      [--cliente mock] [--frecuencia semanal] [--clases DIV,RV] [--semilla 7] [--remuestreos 2000] [--ventana 63]

Deja en <carpeta>: prerregistro.json, informe.json, informe.md y la salida del titular (titular/). Con el cliente
simulado o los datos de ejemplo, el informe lo avisa en su primera línea: entonces prueba la tubería, no mide a A.
B y C se conectan como un contendiente más (una función que devuelve selecciones); ver `.docs/tickets/T-94/README.md`.
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import hashlib
import io
import json
import os
import random
import shutil
import sys
from collections.abc import Callable, Sequence
from pathlib import Path

import numpy as np
import pandas as pd

VERSION = "0.1.0"
RAIZ = Path(__file__).resolve().parents[2]
EJECUTOR_A = RAIZ / "bloque_a" / "11_Ejecutor"
SIGNO = {"LARGO": 1.0, "CORTO": -1.0}


class BancoError(RuntimeError):
    """Fallo que detiene el banco con su motivo (nunca se rellena un hueco)."""


# ---------------------------------------------------------------- datos

def cargar_precios(carpeta: Path, simbolos: Sequence[str]) -> dict[str, pd.Series]:
    """Cierres por símbolo desde CSV con columnas «fecha» y «cierre». Falla si falta alguno."""
    out = {}
    for s in sorted(set(simbolos)):
        f = Path(carpeta) / f"{s}.csv"
        if not f.exists():
            raise BancoError(f"no hay datos para {s} en {carpeta}")
        df = pd.read_csv(f, usecols=["fecha", "cierre"])
        serie = pd.Series(df["cierre"].astype(float).values, index=pd.to_datetime(df["fecha"])).sort_index()
        out[s] = serie[~serie.index.duplicated(keep="last")]
    return out


def cierre_hasta(serie: pd.Series, fecha) -> float | None:
    """Último cierre conocido en la fecha (índice <= fecha), o None."""
    previos = serie.loc[: pd.Timestamp(fecha)]
    return None if previos.empty else float(previos.iloc[-1])


def rentabilidad(serie: pd.Series, inicio, fin) -> float | None:
    """Rentabilidad entre el último cierre conocido al inicio y al fin. None si los datos no llegan al fin."""
    fin = pd.Timestamp(fin)
    if serie.empty or serie.index.max() < fin:
        return None
    a, b = cierre_hasta(serie, inicio), cierre_hasta(serie, fin)
    if a is None or b is None or a <= 0:
        return None
    return b / a - 1.0


# ---------------------------------------------------------------- evaluador

def evaluar(selecciones: list[dict], precios: dict[str, pd.Series], universo: pd.DataFrame,
            fecha_fin: Callable[[pd.Timestamp, str], pd.Timestamp]) -> list[dict]:
    """Exceso de cada selección frente a la cesta de su clase (media del universo de esa clase), con su signo.

    Una selección queda sin resolver si su símbolo o la cesta no tienen precio al final; nunca se estima.
    Las selecciones NEUTRAL no se puntúan."""
    miembros = universo.groupby("clase")["simbolo"].apply(list).to_dict()
    out = []
    for s in selecciones:
        fila = dict(s)
        ini = pd.Timestamp(s["fecha_asof"])
        fin = fecha_fin(ini, s["horizonte"])
        fila["fecha_fin"] = fin.strftime("%Y-%m-%d")
        if s["simbolo"] not in precios:
            raise BancoError(f"la selección usa {s['simbolo']}, que no está en los datos")
        signo = SIGNO.get(s["direccion"])
        r = rentabilidad(precios[s["simbolo"]], ini, fin)
        cesta = [rentabilidad(precios[m], ini, fin) for m in miembros.get(s["clase"], []) if m in precios]
        cesta = [x for x in cesta if x is not None]
        if signo is None or r is None or not cesta:
            fila.update(resuelta=False, exceso=None)
        else:
            fila.update(resuelta=True, exceso=round(signo * (r - float(np.mean(cesta))), 10))
        out.append(fila)
    return out


# ---------------------------------------------------------------- estadística

def _remuestreo_medias(x: np.ndarray, n: int, rng: np.random.Generator) -> np.ndarray:
    idx = rng.integers(0, len(x), size=(n, len(x)))
    return x[idx].mean(axis=1)


def resumen(excesos: Sequence[float], remuestreos: int, semilla: int) -> dict:
    x = np.asarray([e for e in excesos if e is not None], dtype=float)
    if len(x) == 0:
        return {"n": 0, "media": None, "acierto": None, "rango90": None}
    m = _remuestreo_medias(x, remuestreos, np.random.default_rng(semilla))
    return {"n": len(x), "media": round(float(x.mean()), 6), "acierto": round(float((x > 0).mean()), 4),
            "rango90": [round(float(np.quantile(m, 0.05)), 6), round(float(np.quantile(m, 0.95)), 6)]}


def diferencia(a: Sequence[float], b: Sequence[float], remuestreos: int, semilla: int) -> dict:
    """Diferencia de medias (a menos b) con rango del 90 % por remuestreo independiente."""
    xa = np.asarray([e for e in a if e is not None], dtype=float)
    xb = np.asarray([e for e in b if e is not None], dtype=float)
    if len(xa) == 0 or len(xb) == 0:
        return {"diferencia": None, "rango90": None, "veredicto": "sin datos"}
    rng = np.random.default_rng(semilla)
    d = _remuestreo_medias(xa, remuestreos, rng) - _remuestreo_medias(xb, remuestreos, rng)
    rango = [round(float(np.quantile(d, 0.05)), 6), round(float(np.quantile(d, 0.95)), 6)]
    return {"diferencia": round(float(xa.mean() - xb.mean()), 6), "rango90": rango, "veredicto": veredicto(rango)}


def veredicto(rango90: Sequence[float] | None) -> str:
    if not rango90:
        return "sin datos"
    lo, hi = rango90
    if lo > 0:
        return "mejor"
    if hi < 0:
        return "peor"
    return "todavía no se sabe"


# ---------------------------------------------------------------- referencias

def _grupos(plantilla: list[dict]) -> dict[tuple, list[dict]]:
    g: dict[tuple, list[dict]] = {}
    for s in plantilla:
        g.setdefault((s["fecha_asof"], s["clase"]), []).append(s)
    return g


def azar(plantilla: list[dict], universo: pd.DataFrame, semilla: int) -> list[dict]:
    """Tantas selecciones como el titular en cada fecha y clase, al azar dentro de la clase.

    Copia dirección y horizonte del titular selección a selección, para medir solo la elección del activo."""
    miembros = universo.groupby("clase")["simbolo"].apply(sorted).to_dict()
    out = []
    for (fecha, clase), filas in sorted(_grupos(plantilla).items()):
        pool = miembros.get(clase, [])
        if not pool:
            raise BancoError(f"la clase {clase} no tiene miembros en el universo")
        rng = random.Random(f"{semilla}|{fecha}|{clase}")
        elegidos = rng.sample(pool, k=min(len(filas), len(pool)))
        for f, sim in zip(filas, elegidos):
            out.append({**f, "simbolo": sim})
    return out


def momento(plantilla: list[dict], universo: pd.DataFrame, precios: dict[str, pd.Series], ventana: int) -> list[dict]:
    """Tantas selecciones como el titular en cada fecha y clase: para LARGO, la de mayor rentabilidad en las últimas
    «ventana» sesiones hasta la fecha de corte; para CORTO, la de menor. Solo usa datos conocidos en la fecha."""
    miembros = universo.groupby("clase")["simbolo"].apply(sorted).to_dict()
    out = []
    for (fecha, clase), filas in sorted(_grupos(plantilla).items()):
        corte = pd.Timestamp(fecha)
        puntos = {}
        for m in miembros.get(clase, []):
            serie = precios.get(m)
            if serie is None:
                continue
            hist = serie.loc[:corte]
            if len(hist) > ventana:
                puntos[m] = float(hist.iloc[-1] / hist.iloc[-1 - ventana] - 1.0)
        orden = sorted(puntos, key=lambda k: (-puntos[k], k))
        usados: set = set()
        for f in filas:
            candidatos = orden if f["direccion"] != "CORTO" else list(reversed(orden))
            libre = [c for c in candidatos if c not in usados]
            if not libre:
                continue
            usados.add(libre[0])
            out.append({**f, "simbolo": libre[0]})
    return out


# ---------------------------------------------------------------- titular: Bloque A

def titular_a(desde: str, hasta: str, carpeta: Path, cliente: str, frecuencia: str | None,
              clases: str | None) -> dict:
    """Ejecuta A en backtest, espía las llamadas del cliente simulado y devuelve selecciones y consumo."""
    sys.path.insert(0, str(EJECUTOR_A))
    from bloque_a.configuracion import config_por_defecto
    from bloque_a.herramientas.ht05_planificador import fecha_resolucion

    from bloque_a import cli, llm

    llamadas: list[dict] = []
    original = llm.MockClient.generar

    def espia(self, **kw):
        r = original(self, **kw)
        llamadas.append({"agente": kw["agente"], "modelo": kw["modelo"], "salida": r.uso.salida})
        return r

    datos = EJECUTOR_A / "ejemplos" / "datos_sinteticos"
    universo_csv = EJECUTOR_A / "config" / "universo_ejemplo.csv"
    args = ["--cliente", cliente, "--datos", str(datos), "--universo", str(universo_csv),
            "--estado", str(carpeta / "estado"), "--salida", str(carpeta / "salida"),
            "backtest", "--desde", desde, "--hasta", hasta]
    if frecuencia:
        args += ["--frecuencia", frecuencia]
    if clases:
        args += ["--clases", clases]
    shutil.rmtree(carpeta, ignore_errors=True)
    previo = os.getcwd()
    llm.MockClient.generar = espia
    try:
        os.chdir(EJECUTOR_A)
        with contextlib.redirect_stdout(io.StringIO()):
            codigo = cli.main(args)
    finally:
        llm.MockClient.generar = original
        os.chdir(previo)
    if codigo not in (None, 0):
        raise BancoError(f"el titular A terminó con código {codigo}")
    senales = carpeta / "salida" / "senales.csv"
    if not senales.exists():
        raise BancoError("el titular A no dejó senales.csv")
    with open(senales, encoding="utf-8") as fh:
        filas = list(csv.DictReader(fh))
    selecciones = [{"fecha_asof": f["fecha_asof"], "clase": f["clase"], "simbolo": f["indicador_seguimiento_simbolo"],
                    "direccion": f["direccion"], "horizonte": f["horizonte_principal"]}
                   for f in filas if f.get("indicador_seguimiento_simbolo")]
    consumo = {"llamadas": 0, "tokens_entrada": 0, "tokens_salida": 0, "coste_estimado": None}
    fc = carpeta / "salida" / "consumo.csv"
    if fc.exists():
        with open(fc, encoding="utf-8") as fh:
            for f in csv.DictReader(fh):
                consumo["llamadas"] += int(float(f["llamadas"] or 0))
                consumo["tokens_entrada"] += int(float(f["tokens_entrada"] or 0))
                consumo["tokens_salida"] += int(float(f["tokens_salida"] or 0))
                if f.get("coste_estimado"):
                    consumo["coste_estimado"] = round((consumo["coste_estimado"] or 0) + float(f["coste_estimado"]), 4)
    por_agente: dict[str, int] = {}
    for x in llamadas:
        por_agente[x["agente"]] = por_agente.get(x["agente"], 0) + 1
    consumo["llamadas_por_agente"] = dict(sorted(por_agente.items()))
    horizontes = config_por_defecto()["horizontes"]
    return {"selecciones": selecciones, "consumo": consumo, "datos": datos, "universo": universo_csv,
            "fecha_fin": lambda ini, h: fecha_resolucion(ini, h, horizontes)}


# ---------------------------------------------------------------- informe

def huella(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def construir_informe(contendientes: dict[str, list[dict]], consumo_titular: dict, remuestreos: int, semilla: int,
                      aviso: str | None, huella_prerregistro: str) -> dict:
    res = {}
    excesos = {}
    for nombre, filas in contendientes.items():
        ex = [f["exceso"] for f in filas if f["resuelta"]]
        excesos[nombre] = ex
        res[nombre] = {"selecciones": len(filas), "resueltas": len(ex), **resumen(ex, remuestreos, semilla)}
    comparaciones = {f"titular_vs_{n}": diferencia(excesos["titular"], excesos[n], remuestreos, semilla)
                     for n in contendientes if n != "titular"}
    resueltas = res["titular"]["resueltas"]
    coste = consumo_titular.get("coste_estimado")
    return {"version_banco": VERSION, "prerregistro": huella_prerregistro, "aviso": aviso,
            "contendientes": res, "comparaciones": comparaciones,
            "coste": {"titular": consumo_titular, "referencias": "cero (solo código)",
                      "tokens_entrada_por_seleccion_resuelta": (round(consumo_titular["tokens_entrada"] / resueltas, 1)
                                                                if resueltas else None),
                      "coste_por_seleccion_resuelta": round(coste / resueltas, 4) if coste and resueltas else None}}


def _pct(x) -> str:
    return "—" if x is None else f"{x * 100:+.2f} %"


def informe_md(inf: dict, titulo: str) -> str:
    lineas = []
    if inf["aviso"]:
        lineas += [f"**Aviso:** {inf['aviso']}", ""]
    lineas += [f"# {titulo}", "", f"Banco de medida {inf['version_banco']} · prerregistro `{inf['prerregistro'][:16]}…`", "",
               "## Calidad: exceso frente a la cesta de la clase", "",
               "| Contendiente | Selecciones | Resueltas | Exceso medio | Rango del 90 % | Acierto |", "| --- | --- | --- | --- | --- | --- |"]
    for n, r in inf["contendientes"].items():
        rango = "—" if not r["rango90"] else f"{_pct(r['rango90'][0])} a {_pct(r['rango90'][1])}"
        acierto = "—" if r["acierto"] is None else f"{r['acierto'] * 100:.0f} %"
        lineas.append(f"| {n} | {r['selecciones']} | {r['resueltas']} | {_pct(r['media'])} | {rango} | {acierto} |")
    lineas += ["", "## El titular frente a cada referencia", "", "| Comparación | Diferencia | Rango del 90 % | Veredicto |",
               "| --- | --- | --- | --- |"]
    for n, c in inf["comparaciones"].items():
        rango = "—" if not c["rango90"] else f"{_pct(c['rango90'][0])} a {_pct(c['rango90'][1])}"
        lineas.append(f"| {n} | {_pct(c['diferencia'])} | {rango} | {c['veredicto']} |")
    co = inf["coste"]
    t = co["titular"]
    lineas += ["", "## Coste", "",
               (f"- Titular: {t['llamadas']} llamadas, {t['tokens_entrada']} tokens de entrada y {t['tokens_salida']} de salida; "
                f"coste estimado {t['coste_estimado'] if t['coste_estimado'] is not None else 'sin dato'}."),
               f"- Tokens de entrada por selección resuelta: {co['tokens_entrada_por_seleccion_resuelta']}.",
               "- Referencias: coste cero (solo código).", ""]
    if t.get("llamadas_por_agente"):
        lineas += ["Llamadas por agente: " + ", ".join(f"{a} {n}" for a, n in t["llamadas_por_agente"].items()) + ".", ""]
    return "\n".join(lineas)


def ejecutar_a(a: argparse.Namespace) -> dict:
    salida = Path(a.salida).resolve()
    salida.mkdir(parents=True, exist_ok=True)
    prerregistro = {
        "hipotesis": "El Bloque A elige, dentro de cada clase, activos que baten a la cesta de su clase más que el azar y que la regla de momento",
        "titular": "bloque_a (backtest)", "referencias": ["azar", "momento"], "desde": a.desde, "hasta": a.hasta,
        "frecuencia": a.frecuencia, "clases": a.clases, "cliente": a.cliente, "semilla": a.semilla,
        "remuestreos": a.remuestreos, "ventana_momento": a.ventana,
        "metrica": "exceso con signo frente a la media de la clase entre la fecha de corte y la de resolución del horizonte principal",
        "criterio": "mejor si el rango del 90 % de la diferencia de medias queda por encima de cero; peor si queda por debajo; si no, todavía no se sabe",
        "version_banco": VERSION}
    h = huella(prerregistro)
    (salida / "prerregistro.json").write_text(json.dumps({**prerregistro, "huella": h}, ensure_ascii=False, indent=2,
                                                          sort_keys=True) + "\n", encoding="utf-8")
    tit = titular_a(a.desde, a.hasta, salida / "titular", a.cliente, a.frecuencia, a.clases)
    universo = pd.read_csv(tit["universo"], usecols=["simbolo", "clase"])
    precios = cargar_precios(tit["datos"], universo["simbolo"].tolist())
    plantilla = tit["selecciones"]
    contendientes = {
        "titular": evaluar(plantilla, precios, universo, tit["fecha_fin"]),
        "azar": evaluar(azar(plantilla, universo, a.semilla), precios, universo, tit["fecha_fin"]),
        "momento": evaluar(momento(plantilla, universo, precios, a.ventana), precios, universo, tit["fecha_fin"]),
    }
    aviso = None
    if a.cliente == "mock" or "ejemplos" in str(tit["datos"]):
        aviso = ("cliente simulado y datos sintéticos de ejemplo: esto prueba la tubería del banco, "
                 "no mide la capacidad de A. Con datos de K (T-86) y el cliente real, el mismo banco da la medida de verdad.")
    inf = construir_informe(contendientes, tit["consumo"], a.remuestreos, a.semilla, aviso, h)
    (salida / "informe.json").write_text(json.dumps(inf, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (salida / "informe.md").write_text(informe_md(inf, f"Banco de medida del Bloque A ({a.desde} a {a.hasta})"), encoding="utf-8")
    return inf


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="bloque", required=True)
    pa = sub.add_parser("a", help="Bloque A como titular, en backtest")
    pa.add_argument("--desde", required=True)
    pa.add_argument("--hasta", required=True)
    pa.add_argument("--salida", required=True)
    pa.add_argument("--cliente", default="mock")
    pa.add_argument("--frecuencia", choices=["diaria", "semanal", "quincenal", "mensual"])
    pa.add_argument("--clases")
    pa.add_argument("--semilla", type=int, default=7)
    pa.add_argument("--remuestreos", type=int, default=2000)
    pa.add_argument("--ventana", type=int, default=63)
    a = ap.parse_args(argv)
    try:
        inf = ejecutar_a(a)
    except BancoError as e:
        print(f"banco de medida detenido: {e}", file=sys.stderr)
        return 2
    print(json.dumps(inf["comparaciones"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
