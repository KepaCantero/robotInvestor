"""Banco de medida (T-94): el diseño actual de un bloque de búsqueda o selección frente a referencias baratas.

Compara, con los mismos datos y las mismas fechas de corte, lo que elige el titular (hoy, el Bloque A en modo backtest)
con dos referencias: azar con semilla y momento (solo código, sin datos posteriores al corte). Mide calidad (exceso frente
a la cesta de la clase, con rango por remuestreo) y coste (llamadas, tokens, caché, uc y coste estimado). Antes de evaluar
sella un prerregistro con su huella. No modifica ningún bloque ni el marco común: solo importa A para ejecutarlo.

Uso (desde la raíz del repositorio):
  .venv/bin/python .docs/scripts/banco_medida.py a --desde 2026-03-06 --hasta 2026-05-29 --salida <carpeta>
      [--cliente mock] [--frecuencia semanal] [--clases DIV,RV] [--datos <carpeta de CSV>] [--universo <csv>]
      [--semilla 7] [--remuestreos 2000] [--ventana 63] [--nivel 0.90] [--min-efectivas 10]
  .venv/bin/python .docs/scripts/banco_medida.py verificar <carpeta> [--registro R]

Qué cuenta como una observación (QA r01 de T-94, H-01 y H-02):
- una apuesta sobre el mismo activo, la misma clase y la misma dirección cuya ventana sigue abierta no se vuelve a contar:
  queda «repetida» y fuera de la media (el Bloque A repite cada semana la misma oportunidad VIGENTE);
- el rango se calcula remuestreando por fecha de corte (todas las selecciones de una fecha juntas), y el número efectivo
  de observaciones es el de fechas distintas;
- por debajo de --min-efectivas fechas por lado no hay veredicto: «todavía no se sabe», con el motivo.

Desde T-99, cada ejecución desde la línea de órdenes se anota en el registro de experimentos (`.docs/scripts/registro_experimentos.py`).
Sin --experimento, el banco reutiliza el experimento ya prerregistrado con la misma hipótesis, objeto y fuente (cliente, datos
y universo); otro periodo, otra semilla u otros parámetros cuentan como otra variante del mismo experimento. Si no lo hay, lo
prerregistra. Con --experimento, ese experimento tiene que tener la misma hipótesis, objeto y fuente. El máximo de variantes no
cambia después de prerregistrar. `--sin-registro` no anota nada (y `verificar` lo dirá). `verificar` comprueba las huellas.

Deja en <carpeta>: prerregistro.json, informe.json, informe.md y la salida del titular (titular/). El informe avisa en su
primera línea si el cliente es simulado o los datos son los de ejemplo: entonces prueba la tubería, no mide a A.
B y C se conectan como un contendiente más (una función que devuelve selecciones); ver `.docs/tickets/T-94/README.md`.
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import hashlib
import io
import json
import math
import os
import random
import shutil
import sys
from collections.abc import Callable, Sequence
from pathlib import Path

import numpy as np
import pandas as pd

VERSION = "0.3.0"   # 0.3.0 (T-94 r02): repeticiones, remuestreo por fechas, mínimo de observaciones y fallo cerrado
RAIZ = Path(__file__).resolve().parents[2]
EJECUTOR_A = RAIZ / "bloque_a" / "11_Ejecutor"
SIGNO = {"LARGO": 1.0, "CORTO": -1.0}
DIRECCIONES = ("LARGO", "CORTO", "NEUTRAL")
# Valores por defecto de los argumentos ([PROPUESTO] técnico en la fila T-94 de la deuda; el banco no es parte del robot).
SEMILLA = 7
REMUESTREOS = 2000
VENTANA_MOMENTO = 63          # sesiones, unos tres meses
NIVEL = 0.90                  # nivel del rango
MIN_EFECTIVAS = 10            # fechas de corte sin solape por lado; el mismo mínimo que A para certificar
                              # (`evaluacion.min_conglomerados_bootstrap` de su configuración)
REMUESTREOS_MIN = 200         # cotas de un experimento (H-19)
NIVEL_MIN, NIVEL_MAX = 0.80, 0.99
MIN_EFECTIVAS_MIN = 5
AVISO_FUGA = "FUGA POR CONOCIMIENTO DEL MODELO"


class BancoError(RuntimeError):
    """Fallo que detiene el banco con su motivo (nunca se rellena un hueco)."""


def _entero(nombre: str, valor, minimo: int = 1) -> int:
    if isinstance(valor, bool) or not isinstance(valor, (int, np.integer)) or valor < minimo:
        raise BancoError(f"«{nombre}» tiene que ser un entero mayor o igual que {minimo} (se recibió {valor!r})")
    return int(valor)


def _nivel(valor) -> float:
    if isinstance(valor, bool) or not isinstance(valor, (int, float)) or not (0 < float(valor) < 1):
        raise BancoError(f"«nivel» tiene que estar entre 0 y 1, sin incluirlos (se recibió {valor!r})")
    return float(valor)


# ---------------------------------------------------------------- datos

def validar_serie(simbolo: str, serie: pd.Series) -> pd.Series:
    """Falla cerrado si la serie no es utilizable: índice de fechas sin zona horaria y cierres finitos y positivos."""
    if not isinstance(serie, pd.Series) or not isinstance(serie.index, pd.DatetimeIndex):
        raise BancoError(f"los precios de {simbolo} no son una serie indexada por fechas")
    if serie.index.tz is not None:
        raise BancoError(f"los precios de {simbolo} tienen zona horaria ({serie.index.tz}); se esperan fechas de sesión sin zona")
    try:
        v = serie.to_numpy(dtype=float)
    except (TypeError, ValueError) as e:
        raise BancoError(f"los precios de {simbolo} no son numéricos: {e}") from e
    malos = ~np.isfinite(v) | (v <= 0)
    if malos.any():
        i = int(np.argmax(malos))
        raise BancoError(f"cierre no válido de {simbolo} el {serie.index[i]:%Y-%m-%d}: {serie.iloc[i]!r} (tiene que ser finito y positivo)")
    return serie


def cargar_precios(carpeta: Path, simbolos: Sequence[str]) -> dict[str, pd.Series]:
    """Cierres por símbolo desde CSV con columnas «fecha» (AAAA-MM-DD) y «cierre». Falla con el motivo si falta un fichero o
    una columna, si una columna está repetida, si no hay filas, si una fecha no es AAAA-MM-DD o está repetida, o si un cierre
    no es finito y positivo (H-03, H-16). Nunca adivina el formato de una fecha: «03/02/2026» se rechaza."""
    out = {}
    for s in sorted(set(simbolos)):
        f = Path(carpeta) / f"{s}.csv"
        if not f.exists():
            raise BancoError(f"no hay datos para {s} en {carpeta}")
        try:
            with open(f, encoding="utf-8", newline="") as fh:
                cabecera = next(csv.reader(fh), [])
            df = pd.read_csv(f, dtype=str, keep_default_na=False)
        except (ValueError, pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeDecodeError) as e:
            raise BancoError(f"no se puede leer {f.name}: {e}") from e
        repetidas = sorted({c for c in cabecera if cabecera.count(c) > 1})
        if repetidas:
            raise BancoError(f"{f.name} tiene columnas repetidas: {repetidas}")
        falta = [c for c in ("fecha", "cierre") if c not in df.columns]
        if falta:
            raise BancoError(f"a {f.name} le faltan las columnas {falta}")
        if df.empty:
            raise BancoError(f"{f.name} no tiene filas")
        texto = df["fecha"].str.strip()
        fechas = pd.to_datetime(texto, errors="coerce", format="%Y-%m-%d")
        malas = fechas.isna() | ~texto.str.fullmatch(r"\d{4}-\d{2}-\d{2}")
        if malas.any():
            raise BancoError(f"fecha que no es AAAA-MM-DD en {f.name}: {df['fecha'][malas].iloc[0]!r}")
        if fechas.duplicated().any():
            raise BancoError(f"fecha repetida en {f.name}: {fechas[fechas.duplicated()].iloc[0]:%Y-%m-%d}")
        cierre = pd.to_numeric(df["cierre"].str.strip(), errors="coerce")   # lo ilegible queda NaN y validar_serie lo rechaza
        serie = pd.Series(cierre.to_numpy(dtype=float), index=pd.DatetimeIndex(fechas)).sort_index()
        out[s] = validar_serie(s, serie)
    return out


def miembros_por_clase(universo: pd.DataFrame) -> dict[str, list[str]]:
    """Símbolos de cada clase, ordenados. Falla si falta una columna o si un símbolo aparece más de una vez (H-17)."""
    if not isinstance(universo, pd.DataFrame) or not {"simbolo", "clase"} <= set(universo.columns):
        raise BancoError("el universo necesita las columnas «simbolo» y «clase»")
    dup = universo["simbolo"][universo["simbolo"].duplicated()]
    if not dup.empty:
        raise BancoError(f"el símbolo {dup.iloc[0]} está duplicado en el universo (aparece más de una vez)")
    return {c: sorted(g) for c, g in universo.groupby("clase")["simbolo"]}


def cierre_hasta(serie: pd.Series, fecha) -> float | None:
    """Último cierre conocido en la fecha (índice <= fecha), o None."""
    previos = serie.loc[: pd.Timestamp(fecha)]
    return None if previos.empty else float(previos.iloc[-1])


def rentabilidad(serie: pd.Series, inicio, fin) -> float | None:
    """Rentabilidad entre el último cierre conocido al inicio y al fin. None si los datos no llegan al fin o algún extremo
    no es finito y positivo."""
    fin = pd.Timestamp(fin)
    if serie.empty or serie.index.max() < fin:
        return None
    a, b = cierre_hasta(serie, inicio), cierre_hasta(serie, fin)
    if a is None or b is None or not (math.isfinite(a) and math.isfinite(b)) or a <= 0 or b <= 0:
        return None
    return b / a - 1.0


# ---------------------------------------------------------------- evaluador

def evaluar(selecciones: list[dict], precios: dict[str, pd.Series], universo: pd.DataFrame,
            fecha_fin: Callable[[pd.Timestamp, str], pd.Timestamp]) -> list[dict]:
    """Exceso de cada selección frente a la cesta de su clase (media del universo de esa clase), con su signo.

    - Una selección queda sin resolver si su símbolo o la cesta no tienen precio al final; nunca se estima.
    - Las selecciones NEUTRAL no se puntúan.
    - Una selección del mismo activo, clase y dirección que otra puntuada cuya ventana sigue abierta en su fecha de corte
      queda «repetida»: es la misma apuesta y no se cuenta dos veces (H-01).
    - Se detiene con el motivo si la clase no está en el universo, si el símbolo no es de esa clase o no tiene datos, si la
      dirección no es LARGO, CORTO ni NEUTRAL, o si una serie no es utilizable (H-03, H-10)."""
    miembros = miembros_por_clase(universo)
    clase_de = dict(zip(universo["simbolo"], universo["clase"]))
    validadas: set[str] = set()

    def serie(sim: str) -> pd.Series:
        if sim not in precios:
            raise BancoError(f"la selección usa {sim}, que no está en los datos")
        if sim not in validadas:
            validar_serie(sim, precios[sim])
            validadas.add(sim)
        return precios[sim]

    def corte(s: dict) -> pd.Timestamp:
        try:
            t = pd.Timestamp(s["fecha_asof"])
        except (KeyError, ValueError, TypeError) as e:
            raise BancoError(f"fecha de corte ilegible en la selección {s!r}") from e
        if t.tz is not None:
            raise BancoError(f"la fecha de corte {s['fecha_asof']!r} tiene zona horaria")
        return t

    inicios = [corte(s) for s in selecciones]
    out: list[dict | None] = [None] * len(selecciones)
    abiertas: dict[tuple, tuple[pd.Timestamp, str]] = {}
    def orden(k: int) -> tuple:   # canónico: no depende del orden de entrada (H-17)
        s = selecciones[k]
        return (inicios[k], str(s.get("clase")), str(s.get("simbolo")), str(s.get("direccion")), str(s.get("horizonte")), k)

    for i in sorted(range(len(selecciones)), key=orden):
        s = selecciones[i]
        clase, sim, direccion = s.get("clase"), s.get("simbolo"), s.get("direccion")
        if direccion not in DIRECCIONES:
            raise BancoError(f"dirección {direccion!r} desconocida en la selección de {sim} ({', '.join(DIRECCIONES)})")
        if clase not in miembros:
            raise BancoError(f"la clase {clase!r} de la selección de {sim} no está en el universo")
        serie(sim)
        if clase_de.get(sim) != clase:
            raise BancoError(f"{sim} no es de la clase {clase} en el universo (es de {clase_de.get(sim)!r})")
        ini = inicios[i]
        try:
            fin = pd.Timestamp(fecha_fin(ini, s["horizonte"]))
        except (KeyError, ValueError, TypeError) as e:
            raise BancoError(f"horizonte {s.get('horizonte')!r} sin fecha de resolución en la selección de {sim}") from e
        if not fin > ini:
            raise BancoError(f"la fecha de resolución de {sim} ({fin:%Y-%m-%d}) no es posterior a la de corte")
        fila = {**s, "fecha_corte": ini.strftime("%Y-%m-%d"), "fecha_fin": fin.strftime("%Y-%m-%d"), "repetida": False}
        clave = (clase, sim, direccion)
        if direccion == "NEUTRAL":
            fila.update(resuelta=False, exceso=None, motivo="NEUTRAL no se puntúa")
        elif clave in abiertas and abiertas[clave][0] > ini:
            fila.update(resuelta=False, exceso=None, repetida=True,
                        motivo=f"repetida: la misma apuesta sigue abierta desde el {abiertas[clave][1]}")
        else:
            abiertas[clave] = (fin, ini.strftime("%Y-%m-%d"))
            r = rentabilidad(serie(sim), ini, fin)
            cesta = [rentabilidad(serie(m), ini, fin) for m in miembros[clase] if m in precios]
            cesta = [x for x in cesta if x is not None]
            if r is None or not cesta:
                fila.update(resuelta=False, exceso=None, motivo="sin precio al final de la ventana")
            else:
                fila.update(resuelta=True, exceso=round(SIGNO[direccion] * (r - float(np.mean(cesta))), 10), cesta_n=len(cesta))
        out[i] = fila
    return [f for f in out if f is not None]


# ---------------------------------------------------------------- estadística

def _limpios(excesos: Sequence, grupos: Sequence | None) -> tuple[np.ndarray, list | None]:
    if grupos is not None and len(grupos) != len(excesos):
        raise BancoError("excesos y grupos de distinta longitud")
    pares = [(e, None if grupos is None else grupos[i]) for i, e in enumerate(excesos) if e is not None]
    x = np.asarray([p[0] for p in pares], dtype=float)
    if not np.isfinite(x).all():
        raise BancoError("hay un exceso no finito: los datos no son utilizables")
    return x, (None if grupos is None else [p[1] for p in pares])


def _efectivas(x: np.ndarray, grupos: list | None) -> int:
    return len(x) if grupos is None else len(set(grupos))


def _medias_remuestreadas(x: np.ndarray, grupos: list | None, n: int, rng: np.random.Generator) -> np.ndarray:
    """Medias de n remuestreos. Sin grupos, de observaciones; con grupos, de grupos enteros (todas sus observaciones)."""
    if grupos is None:
        idx = rng.integers(0, len(x), size=(n, len(x)))
        return x[idx].mean(axis=1)
    claves = sorted(set(grupos), key=str)
    pos = {c: k for k, c in enumerate(claves)}
    sumas = np.zeros(len(claves))
    cuentas = np.zeros(len(claves))
    for v, g in zip(x, grupos):
        sumas[pos[g]] += v
        cuentas[pos[g]] += 1
    idx = rng.integers(0, len(claves), size=(n, len(claves)))
    return sumas[idx].sum(axis=1) / cuentas[idx].sum(axis=1)


def _cuantiles(m: np.ndarray, nivel: float) -> list[float]:
    cola = (1.0 - nivel) / 2.0
    return [round(float(np.quantile(m, cola)), 6), round(float(np.quantile(m, 1.0 - cola)), 6)]


def resumen(excesos: Sequence[float], remuestreos: int, semilla: int, nivel: float = NIVEL,
            grupos: Sequence | None = None) -> dict:
    remuestreos, nivel = _entero("remuestreos", remuestreos), _nivel(nivel)
    x, g = _limpios(excesos, grupos)
    if len(x) == 0:
        return {"n": 0, "efectivas": 0, "media": None, "acierto": None, "rango": None, "nivel": nivel}
    m = _medias_remuestreadas(x, g, remuestreos, np.random.default_rng(semilla))
    return {"n": len(x), "efectivas": _efectivas(x, g), "media": round(float(x.mean()), 6),
            "acierto": round(float((x > 0).mean()), 4), "rango": _cuantiles(m, nivel), "nivel": nivel}


def diferencia(a: Sequence[float], b: Sequence[float], remuestreos: int, semilla: int, nivel: float = NIVEL,
               min_efectivas: int = MIN_EFECTIVAS, grupos_a: Sequence | None = None, grupos_b: Sequence | None = None) -> dict:
    """Diferencia de medias (a menos b) con su rango por remuestreo independiente de cada lado (por grupos si se dan).

    Sin al menos «min_efectivas» observaciones efectivas por lado no hay veredicto (H-02). Como da veredictos, tiene las
    cotas de un experimento (H-19): remuestreos, nivel y mínimo de efectivas no pueden bajar de las de la configuración."""
    remuestreos, nivel = _entero("remuestreos", remuestreos, minimo=REMUESTREOS_MIN), _nivel(nivel)
    if not NIVEL_MIN <= nivel <= NIVEL_MAX:
        raise BancoError(f"«nivel» de un veredicto entre {NIVEL_MIN} y {NIVEL_MAX} (se recibió {nivel})")
    min_efectivas = _entero("min_efectivas", min_efectivas, minimo=MIN_EFECTIVAS_MIN)
    xa, ga = _limpios(a, grupos_a)
    xb, gb = _limpios(b, grupos_b)
    if len(xa) == 0 or len(xb) == 0:
        return {"diferencia": None, "rango": None, "nivel": nivel, "efectivas": [len(xa), len(xb)], "veredicto": "sin datos",
                "motivo": "un lado no tiene ninguna selección resuelta"}
    efectivas = [_efectivas(xa, ga), _efectivas(xb, gb)]
    rng = np.random.default_rng(semilla)
    d = _medias_remuestreadas(xa, ga, remuestreos, rng) - _medias_remuestreadas(xb, gb, remuestreos, rng)
    rango = _cuantiles(d, nivel)
    out = {"diferencia": round(float(xa.mean() - xb.mean()), 6), "rango": rango, "nivel": nivel, "efectivas": efectivas,
           "veredicto": veredicto(rango), "motivo": None}
    if min(efectivas) < min_efectivas:
        out.update(veredicto="todavía no se sabe",
                   motivo=f"pocas observaciones efectivas ({min(efectivas)} de un mínimo de {min_efectivas} por lado)")
    return out


def veredicto(rango: Sequence[float] | None) -> str:
    if not rango:
        return "sin datos"
    lo, hi = rango
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
    """Tantas selecciones como el titular en cada fecha y clase, al azar dentro de la clase y sin repetir activo.

    Copia dirección y horizonte del titular selección a selección, para medir solo la elección del activo. Se detiene si la
    clase no tiene miembros suficientes para igualar al titular (H-06)."""
    miembros = miembros_por_clase(universo)
    out = []
    for (fecha, clase), filas in sorted(_grupos(plantilla).items()):
        pool = miembros.get(clase, [])
        if len(pool) < len(filas):
            raise BancoError(f"azar no puede igualar al titular el {fecha} en {clase}: {len(filas)} selecciones y "
                             f"{len(pool)} miembros en el universo")
        rng = random.Random(f"{semilla}|{fecha}|{clase}")
        for f, sim in zip(filas, rng.sample(pool, k=len(filas))):
            out.append({**f, "simbolo": sim})
    return out


def momento(plantilla: list[dict], universo: pd.DataFrame, precios: dict[str, pd.Series], ventana: int) -> list[dict]:
    """Tantas selecciones como el titular en cada fecha y clase: para LARGO, la de mayor rentabilidad en las últimas
    «ventana» sesiones hasta la fecha de corte; para CORTO, la de menor. Solo usa datos conocidos en la fecha.
    Se detiene si no hay bastantes miembros con historia para igualar al titular (H-06)."""
    ventana = _entero("ventana", ventana)
    miembros = miembros_por_clase(universo)
    out = []
    for (fecha, clase), filas in sorted(_grupos(plantilla).items()):
        corte = pd.Timestamp(fecha)
        puntos = {}
        for m in miembros.get(clase, []):
            serie = precios.get(m)
            if serie is None:
                continue
            hist = validar_serie(m, serie).loc[:corte]
            if len(hist) > ventana:
                puntos[m] = float(hist.iloc[-1] / hist.iloc[-1 - ventana] - 1.0)
        if len(puntos) < len(filas):
            raise BancoError(f"momento no puede igualar al titular el {fecha} en {clase}: {len(filas)} selecciones y "
                             f"{len(puntos)} miembros con más de {ventana} sesiones de historia")
        orden = sorted(puntos, key=lambda k: (-puntos[k], k))
        usados: set = set()
        for f in filas:
            candidatos = orden if f["direccion"] != "CORTO" else list(reversed(orden))
            libre = next(c for c in candidatos if c not in usados)
            usados.add(libre)
            out.append({**f, "simbolo": libre})
    return out


# ---------------------------------------------------------------- titular: Bloque A

def titular_a(desde: str, hasta: str, carpeta: Path, cliente: str, frecuencia: str | None,
              clases: str | None, datos: Path | None = None, universo: Path | None = None) -> dict:
    """Ejecuta A en backtest, espía las llamadas del cliente simulado y devuelve selecciones, consumo y advertencias."""
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

    datos = Path(datos).resolve() if datos else EJECUTOR_A / "ejemplos" / "datos_sinteticos"
    universo_csv = Path(universo).resolve() if universo else EJECUTOR_A / "config" / "universo_ejemplo.csv"
    for p in (datos, universo_csv):
        if not p.exists():
            raise BancoError(f"no existe {p}")
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
    consumo = leer_consumo(carpeta / "salida" / "consumo.csv")
    por_agente: dict[str, int] = {}
    for x in llamadas:
        por_agente[x["agente"]] = por_agente.get(x["agente"], 0) + 1
    consumo["llamadas_por_agente"] = dict(sorted(por_agente.items()))
    advertencias, excluidos = [], None
    fm = carpeta / "salida" / "metricas.json"
    if fm.exists():
        m = json.loads(fm.read_text(encoding="utf-8"))
        advertencias = [str(x) for x in m.get("advertencias") or []]
        excluidos = (m.get("excluidos_contaminacion") or {}).get("total")
    horizontes = config_por_defecto()["horizontes"]
    return {"selecciones": selecciones, "consumo": consumo, "datos": datos, "universo": universo_csv,
            "advertencias": advertencias, "excluidos_contaminacion": excluidos,
            "fecha_fin": lambda ini, h: fecha_resolucion(ini, h, horizontes)}


CAMPOS_ENTEROS = ("llamadas", "tokens_entrada", "tokens_salida", "tokens_cache_escritura", "tokens_cache_lectura")


def _cantidad(fichero: Path, fila: int, campo: str, txt) -> float:
    try:
        v = float(txt)
    except (TypeError, ValueError) as e:
        raise BancoError(f"{Path(fichero).name}, fila {fila}: «{campo}» no es un número ({txt!r})") from e
    if not math.isfinite(v) or v < 0:
        raise BancoError(f"{Path(fichero).name}, fila {fila}: «{campo}» tiene que ser finito y no negativo ({txt!r})")
    return v


def leer_consumo(fichero: Path) -> dict:
    """Suma del consumo.csv de A: llamadas, tokens (también de caché), uc y coste estimado. Un valor no numérico, no finito o
    negativo detiene el banco (H-18). El coste es None si alguna fila no lo trae, y «filas_sin_coste» dice cuántas: un coste
    parcial no se publica como total."""
    consumo: dict = {k: 0 for k in CAMPOS_ENTEROS}
    consumo.update(uc=0.0, coste_estimado=None, filas_sin_coste=0)
    if not Path(fichero).exists():   # sin el fichero no hay coste medido: no se publican ceros (QA r02)
        raise BancoError(f"no hay {Path(fichero).name}: el coste del titular no se puede medir")
    coste, filas = 0.0, 0
    with open(fichero, encoding="utf-8") as fh:
        for n, f in enumerate(csv.DictReader(fh), 2):
            filas += 1
            for k in CAMPOS_ENTEROS:
                consumo[k] += int(_cantidad(fichero, n, k, f.get(k) or 0))
            consumo["uc"] = round(consumo["uc"] + _cantidad(fichero, n, "uc", f.get("uc") or 0), 4)
            if f.get("coste_estimado") in (None, ""):
                consumo["filas_sin_coste"] += 1
            else:
                coste += _cantidad(fichero, n, "coste_estimado", f["coste_estimado"])
    if filas and not consumo["filas_sin_coste"]:
        consumo["coste_estimado"] = round(coste, 4)
    return consumo


# ---------------------------------------------------------------- informe

def huella(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _fecha(fila: dict) -> str:
    """Fecha de corte normalizada (AAAA-MM-DD): la misma fecha escrita de dos formas es la misma fecha (H-17)."""
    return fila.get("fecha_corte") or pd.Timestamp(fila["fecha_asof"]).strftime("%Y-%m-%d")


def fechas_sin_solape(filas: list[dict]) -> set[str]:
    """Fechas de corte cuyas ventanas no se solapan, de la más antigua a la más reciente: se toma una fecha y la siguiente
    que se toma es la primera que empieza cuando ya han terminado todas las ventanas de la anterior (H-13). Una fila sin
    «fecha_fin» tiene una ventana de un día."""
    fin_por_fecha: dict[str, str] = {}
    for f in filas:
        d = _fecha(f)
        fin = f.get("fecha_fin") or d
        fin_por_fecha[d] = max(fin_por_fecha.get(d, fin), fin)
    elegidas, cierre = set(), ""
    for d in sorted(fin_por_fecha):
        if d >= cierre:
            elegidas.add(d)
            cierre = fin_por_fecha[d]   # la siguiente puede empezar el día en que esta termina: no comparten tramo
    return elegidas


def construir_informe(contendientes: dict[str, list[dict]], consumo_titular: dict, remuestreos: int, semilla: int,
                      aviso: str | None, huella_prerregistro: str, nivel: float = NIVEL, min_efectivas: int = MIN_EFECTIVAS,
                      advertencias: Sequence[str] = (), sin_veredicto: str | None = None) -> dict:
    """Informe: calidad por contendiente, comparación del titular con cada referencia y coste.

    Solo entran las fechas de corte de `fechas_sin_solape` (calculadas con el titular y comunes a todos): dos fechas cuyas
    ventanas se solapan comparten mercado y no son observaciones independientes (H-13). Con «sin_veredicto» (por ejemplo,
    fuga por conocimiento del modelo), ninguna comparación da veredicto firme."""
    muestra = fechas_sin_solape(contendientes["titular"])
    res = {}
    excesos = {}
    for nombre, filas in contendientes.items():
        dentro = [f for f in filas if _fecha(f) in muestra]
        puntuadas = [f for f in dentro if f["resuelta"]]
        excesos[nombre] = ([f["exceso"] for f in puntuadas], [_fecha(f) for f in puntuadas])
        res[nombre] = {"selecciones": len(filas), "repetidas": sum(1 for f in filas if f.get("repetida")),
                       "fuera_de_muestra": len(filas) - len(dentro), "resueltas": len(puntuadas),
                       **resumen(excesos[nombre][0], remuestreos, semilla, nivel, excesos[nombre][1])}
    comparaciones = {}
    for n in contendientes:
        if n == "titular":
            continue
        c = diferencia(excesos["titular"][0], excesos[n][0], remuestreos, semilla, nivel, min_efectivas,
                       excesos["titular"][1], excesos[n][1])
        if sin_veredicto and c["veredicto"] in ("mejor", "peor"):
            c.update(veredicto="todavía no se sabe", motivo=sin_veredicto)
        comparaciones[f"titular_vs_{n}"] = c
    resueltas = res["titular"]["resueltas"]
    t = consumo_titular
    coste = t.get("coste_estimado")
    por_sel = {}
    if resueltas:
        por_sel = {"tokens_entrada": round(t.get("tokens_entrada", 0) / resueltas, 1),
                   "tokens_cache_lectura": round(t.get("tokens_cache_lectura", 0) / resueltas, 1),
                   "uc": round(t.get("uc", 0.0) / resueltas, 4),
                   "coste_estimado": None if coste is None else round(coste / resueltas, 4)}
    return {"version_banco": VERSION, "prerregistro": huella_prerregistro, "aviso": aviso,
            "advertencias_titular": list(advertencias), "nivel": nivel, "min_efectivas": min_efectivas,
            "fechas_en_muestra": sorted(muestra),
            "contendientes": res, "comparaciones": comparaciones,
            "coste": {"titular": consumo_titular, "referencias": "cero (solo código)",
                      "por_seleccion_resuelta": por_sel or None}}


def _pct(x) -> str:
    return "—" if x is None else f"{x * 100:+.2f} %"


def _rango(r) -> str:
    return "—" if not r else f"{_pct(r[0])} a {_pct(r[1])}"


def informe_md(inf: dict, titulo: str) -> str:
    pct_nivel = f"{inf['nivel'] * 100:g} %"
    lineas = []
    if inf["aviso"]:
        lineas += [f"**Aviso:** {inf['aviso']}", ""]
    lineas += [f"# {titulo}", "", f"Banco de medida {inf['version_banco']} · prerregistro `{inf['prerregistro'][:16]}…`", ""]
    if inf.get("advertencias_titular"):
        lineas += ["Advertencias del titular:", ""] + [f"- {a}" for a in inf["advertencias_titular"]] + [""]
    lineas += ["## Calidad: exceso frente a la cesta de la clase", "",
               (f"Solo cuentan las fechas de corte cuyas ventanas no se solapan ({len(inf.get('fechas_en_muestra', []))} en la "
                f"muestra), y una apuesta repetida mientras sigue abierta cuenta una vez. El rango del {pct_nivel} remuestrea esas "
                f"fechas; sin {inf['min_efectivas']} por lado no hay veredicto."), "",
               (f"| Contendiente | Selecciones | Repetidas | Fuera de muestra | Resueltas | Fechas efectivas | Exceso medio | "
                f"Rango del {pct_nivel} | Acierto |"),
               "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    orden = ["titular"] + sorted(n for n in inf["contendientes"] if n != "titular")   # el mismo orden antes y después de JSON
    for n in orden:
        r = inf["contendientes"][n]
        acierto = "—" if r["acierto"] is None else f"{r['acierto'] * 100:.0f} %"
        lineas.append(f"| {n} | {r['selecciones']} | {r['repetidas']} | {r.get('fuera_de_muestra', 0)} | {r['resueltas']} | "
                      f"{r['efectivas']} | {_pct(r['media'])} | {_rango(r['rango'])} | {acierto} |")
    lineas += ["", "## El titular frente a cada referencia", "",
               f"| Comparación | Diferencia | Rango del {pct_nivel} | Veredicto | Motivo |", "| --- | --- | --- | --- | --- |"]
    for n, c in sorted(inf["comparaciones"].items()):
        lineas.append(f"| {n} | {_pct(c['diferencia'])} | {_rango(c['rango'])} | {c['veredicto']} | {c.get('motivo') or '—'} |")
    co = inf["coste"]
    t = co["titular"]
    coste = "sin dato" if t.get("coste_estimado") is None else f"{t['coste_estimado']}"
    if t.get("filas_sin_coste"):
        coste += f" ({t['filas_sin_coste']} filas de consumo.csv sin coste: no se suma un coste parcial)"
    lineas += ["", "## Coste", "",
               (f"- Titular: {t['llamadas']} llamadas; tokens: {t['tokens_entrada']} de entrada, {t['tokens_salida']} de salida, "
                f"{t.get('tokens_cache_escritura', 0)} escritos en caché y {t.get('tokens_cache_lectura', 0)} leídos de caché; "
                f"{t.get('uc', 0)} uc; coste estimado {coste}.")]
    ps = co.get("por_seleccion_resuelta")
    if ps:
        cps = "sin dato" if ps["coste_estimado"] is None else f"{ps['coste_estimado']}"
        lineas.append(f"- Por selección resuelta: {ps['tokens_entrada']} tokens de entrada, {ps['tokens_cache_lectura']} leídos de caché, "
                      f"{ps['uc']} uc; coste estimado {cps}.")
    else:
        lineas.append("- Por selección resuelta: sin selecciones resueltas.")
    lineas += ["- Referencias: coste cero (solo código).", ""]
    if t.get("llamadas_por_agente"):
        lineas += ["Llamadas por agente: " + ", ".join(f"{a} {n}" for a, n in t["llamadas_por_agente"].items()) + ".", ""]
    return "\n".join(lineas)


def _escribir_json(ruta: Path, obj) -> None:
    ruta.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def _aviso(cliente: str, datos: Path, universo: Path) -> str | None:
    partes = []
    if cliente == "mock":
        partes.append("cliente simulado: las señales salen de reglas sintéticas, no de un modelo")
    if Path(datos).resolve() == (EJECUTOR_A / "ejemplos" / "datos_sinteticos").resolve():
        partes.append("datos sintéticos de ejemplo")
    if Path(universo).resolve() == (EJECUTOR_A / "config" / "universo_ejemplo.csv").resolve():
        partes.append("universo de ejemplo")
    if not partes:
        return None
    return "; ".join(partes) + ". Esto prueba la tubería del banco, no mide la capacidad de A."


HIPOTESIS_A = ("El Bloque A elige, dentro de cada clase, activos que baten a la cesta de su clase más que el azar y que la "
               "regla de momento")


def _experimento(reg, exp_id: str | None, prerregistro: dict, h: str, max_variantes: int) -> tuple[str, int]:
    """Experimento al que se anota el intento y cuántos experimentos distintos de ese tienen la misma hipótesis.

    Un experimento del banco es una hipótesis con una fuente (cliente, datos y universo): el cliente simulado y el real son
    experimentos distintos, y una prueba con el simulado no gasta las variantes del real. Otro periodo, otra semilla u otros
    parámetros son otra variante del MISMO experimento, que cuenta para su máximo de variantes (H-04, H-14)."""
    fuente = prerregistro["fuente"]
    previos = [x for x in reg.anotaciones() if x["tipo"] == "PRERREGISTRO"]
    misma = [x for x in previos if x["contenido"].get("hipotesis") == prerregistro["hipotesis"]
             and x["contenido"].get("objeto") == "BLOQUE"]
    if exp_id:
        pre = reg.experimento(exp_id)["prerregistro"]["contenido"]
        if pre.get("max_variantes") != max_variantes:
            raise BancoError(f"el experimento {exp_id} se prerregistró con max_variantes {pre.get('max_variantes')}, no "
                             f"{max_variantes}: el máximo no se cambia después (T-99, QA r01 H-08)")
        distinto = [k for k, v in (("hipotesis", prerregistro["hipotesis"]), ("objeto", "BLOQUE"), ("fuente_banco", fuente))
                    if pre.get(k) != v]
        if distinto:
            raise BancoError(f"el experimento {exp_id} no es de este banco: no casan {distinto} con su prerregistro")
    else:
        # Buscar o prerregistrar bajo el mismo cerrojo: dos bancos a la vez no crean dos experimentos (T-99, QA r02 H-19)
        encontrado, _nuevo = reg.buscar_o_prerregistrar(
            lambda c: c.get("hipotesis") == prerregistro["hipotesis"] and c.get("objeto") == "BLOQUE" and c.get("fuente_banco") == fuente,
            {"hipotesis": prerregistro["hipotesis"], "objeto": "BLOQUE", "metrica": prerregistro["metrica"],
             "fuente_banco": fuente, "datos": f"backtest de A con {fuente}; huella del prerregistro del banco {h}",
             "desde": prerregistro["desde"], "hasta": prerregistro["hasta"], "semilla": prerregistro["semilla"],
             "criterio_exito": prerregistro["criterio"] + " (frente al azar y frente al momento a la vez)",
             "max_variantes": max_variantes}, autor="banco_medida")
        exp_id = encontrado["exp_id"]
        prev = encontrado["contenido"].get("max_variantes")
        if prev != max_variantes:
            raise BancoError(f"el experimento {exp_id} de esta hipótesis y fuente se prerregistró con max_variantes {prev}, "
                             f"no {max_variantes}: el máximo no se cambia después (T-99, QA r01 H-08)")
    otros = len({x["exp_id"] for x in misma} - {exp_id})
    return exp_id, otros


def _ruta_publica(ruta) -> str:
    """Cómo se nombra una ruta en el prerregistro y en el registro, que se suben a un repositorio público (T-99, QA r02 H-24):
    relativa a la raíz si está dentro; si no, su nombre y una huella corta de la ruta, sin carpetas de la máquina."""
    p = Path(ruta).resolve()
    try:
        return p.relative_to(RAIZ.resolve()).as_posix()
    except ValueError:
        return f"«externa»/{p.name} ({hashlib.sha256(str(p).encode('utf-8', 'backslashreplace')).hexdigest()[:12]})"


def ejecutar_a(a: argparse.Namespace) -> dict:
    # Cotas de un experimento (H-19): con menos remuestreos, un nivel fuera de [0,80, 0,99] o menos fechas efectivas, el
    # banco daría veredictos firmes sin habilidad. Las funciones de estadística admiten más, para las pruebas.
    semilla = _entero("semilla", getattr(a, "semilla", SEMILLA), minimo=0)
    remuestreos = _entero("remuestreos", getattr(a, "remuestreos", REMUESTREOS), minimo=REMUESTREOS_MIN)
    ventana = _entero("ventana", getattr(a, "ventana", VENTANA_MOMENTO))
    nivel = _nivel(getattr(a, "nivel", NIVEL))
    if not NIVEL_MIN <= nivel <= NIVEL_MAX:
        raise BancoError(f"«nivel» de un experimento entre {NIVEL_MIN} y {NIVEL_MAX} (se recibió {nivel})")
    min_efectivas = _entero("min_efectivas", getattr(a, "min_efectivas", MIN_EFECTIVAS), minimo=MIN_EFECTIVAS_MIN)
    max_variantes = _entero("max_variantes", getattr(a, "max_variantes", 1))
    datos_arg, universo_arg = getattr(a, "datos", None), getattr(a, "universo", None)
    salida = Path(a.salida).resolve()
    salida.mkdir(parents=True, exist_ok=True)
    (salida / "experimento.json").unlink(missing_ok=True)   # nunca el de una ejecución anterior
    datos_txt = _ruta_publica(datos_arg) if datos_arg else "ejemplos/datos_sinteticos de A"
    universo_txt = _ruta_publica(universo_arg) if universo_arg else "config/universo_ejemplo.csv de A"
    prerregistro = {
        "hipotesis": HIPOTESIS_A,
        "titular": "bloque_a (backtest)", "referencias": ["azar", "momento"], "desde": a.desde, "hasta": a.hasta,
        "frecuencia": a.frecuencia, "clases": a.clases, "cliente": a.cliente, "datos": datos_txt, "universo": universo_txt,
        "fuente": f"cliente {a.cliente}, datos {datos_txt}, universo {universo_txt}",
        "semilla": semilla, "remuestreos": remuestreos, "ventana_momento": ventana, "nivel": nivel, "min_efectivas": min_efectivas,
        "metrica": ("exceso con signo frente a la media de la clase entre la fecha de corte y la de resolución del horizonte "
                    "principal, solo en fechas de corte cuyas ventanas no se solapan; una apuesta repetida mientras sigue "
                    "abierta cuenta una vez"),
        "criterio": (f"mejor si el rango del {nivel * 100:g} % de la diferencia de medias, remuestreando fechas de corte sin "
                     f"solape, queda por encima de cero con al menos {min_efectivas} fechas por lado; peor si queda por "
                     "debajo; si no, todavía no se sabe"),
        "version_banco": VERSION}
    h = huella(prerregistro)
    reg = intento = None
    otros_misma = 0
    if getattr(a, "registro", None) == "":   # T-99, QA r01 H-08: un registro vacío no desactiva el registro en silencio
        raise BancoError("--registro vacío (o RI_AGENTE no válido, sin registro por defecto): indica uno, o usa --sin-registro")
    if getattr(a, "registro", None):   # T-99: cada intento cuenta, también los que fallan
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import registro_experimentos as rx
        try:
            reg = rx.Registro(a.registro)
            exp_id, otros_misma = _experimento(reg, getattr(a, "experimento", None), prerregistro, h, max_variantes)
            intento = reg.intento(exp_id, variante=h[:16])
        except rx.RegistroError as e:
            raise BancoError(f"registro de experimentos: {e}") from e
    try:
        _escribir_json(salida / "prerregistro.json", {**prerregistro, "huella": h})   # dentro: si falla, el intento es «fallido»
        kw = {k: v for k, v in (("datos", datos_arg), ("universo", universo_arg)) if v}
        tit = titular_a(a.desde, a.hasta, salida / "titular", a.cliente, a.frecuencia, a.clases, **kw)
        universo = pd.read_csv(tit["universo"], usecols=["simbolo", "clase"])
        precios = cargar_precios(tit["datos"], universo["simbolo"].tolist())
        plantilla = tit["selecciones"]
        contendientes = {
            "titular": evaluar(plantilla, precios, universo, tit["fecha_fin"]),
            "azar": evaluar(azar(plantilla, universo, semilla), precios, universo, tit["fecha_fin"]),
            "momento": evaluar(momento(plantilla, universo, precios, ventana), precios, universo, tit["fecha_fin"]),
        }
        advertencias = list(tit.get("advertencias") or [])
        if tit.get("excluidos_contaminacion"):
            advertencias.append(f"el titular apartó {tit['excluidos_contaminacion']} pronósticos por contaminación")
        if otros_misma:
            advertencias.append(f"hay {otros_misma} experimento(s) más con esta misma hipótesis en el registro (otra fuente): "
                                "mirar todos sus resultados")
        sin_veredicto = None
        if a.cliente != "mock" and any(AVISO_FUGA in x for x in advertencias):
            sin_veredicto = "el periodo empieza antes de la fecha de corte del modelo: puede conocer el resultado"
        aviso = _aviso(a.cliente, tit["datos"], tit["universo"])
        inf = construir_informe(contendientes, tit["consumo"], remuestreos, semilla, aviso, h, nivel, min_efectivas,
                                advertencias, sin_veredicto)
        _escribir_json(salida / "informe.json", inf)
        (salida / "informe.md").write_text(informe_md(inf, titulo_informe(a.desde, a.hasta)), encoding="utf-8")
    except BaseException as e:
        if reg is not None:
            try:
                motivo = f"{type(e).__name__}: {e}"[:300].encode("utf-8", "backslashreplace").decode("utf-8")   # H-20
                reg.resultado(intento["exp_id"], intento["n"], "fallido", {"motivo": motivo})
            except rx.RegistroError as ex:   # no tapa el fallo original: lo encadena
                raise BancoError(f"{type(e).__name__}: {e}; y no se pudo anotar el intento como fallido: {ex}") from e
        raise
    if reg is not None:
        # El intento va aparte (experimento.json), para que el informe de dos ejecuciones iguales sea idéntico byte a byte.
        experimento = {"exp_id": intento["exp_id"], "intento": intento["n"], "dentro_del_maximo": intento["dentro_del_maximo"],
                       # relativa a la carpeta de salida: sin carpetas de la máquina (T-99, QA r03 H-24)
                       "registro": os.path.relpath(Path(a.registro).resolve(), salida)}
        try:
            reg.resultado(intento["exp_id"], intento["n"], veredicto_conjunto(inf["comparaciones"]),
                          {"comparaciones": {k: v["veredicto"] for k, v in inf["comparaciones"].items()}, "aviso": aviso,
                           "huella_prerregistro_banco": h, "huella_informe": huella(inf)})
        except rx.RegistroError as e:
            raise BancoError(f"registro de experimentos: {e}") from e
        _escribir_json(salida / "experimento.json", experimento)
        inf["experimento"] = experimento
    return inf


def titulo_informe(desde: str, hasta: str) -> str:
    return f"Banco de medida del Bloque A ({desde} a {hasta})"


def verificar(carpeta: Path | str, registro: Path | str | None = None) -> list[str]:
    """Comprueba una carpeta de salida del banco y devuelve la lista de problemas (vacía si todo cuadra):
    - prerregistro.json casa con su huella y el informe cita esa huella;
    - informe.md es exactamente el que sale de informe.json;
    - el intento y el resultado del registro (experimento.json) casan con el prerregistro y con el informe.
    Sin experimento.json no se puede comprobar que el informe sea el que dio el banco, y se dice (H-15)."""
    carpeta = Path(carpeta)
    problemas = []
    try:
        pre = json.loads((carpeta / "prerregistro.json").read_text(encoding="utf-8"))
        inf = json.loads((carpeta / "informe.json").read_text(encoding="utf-8"))
        md = (carpeta / "informe.md").read_text(encoding="utf-8")
    except (OSError, ValueError) as e:
        return [f"no se pueden leer los ficheros: {e}"]
    if not isinstance(pre, dict) or not isinstance(inf, dict):
        return ["prerregistro.json o informe.json no tienen la forma de una salida del banco"]
    h = huella({k: v for k, v in pre.items() if k != "huella"})
    if pre.get("huella") != h:
        problemas.append("prerregistro.json no casa con su huella: se reescribió")
    if inf.get("prerregistro") != h:
        problemas.append("el informe cita una huella distinta de la del prerregistro")
    try:
        if md != informe_md(inf, titulo_informe(pre.get("desde"), pre.get("hasta"))):
            problemas.append("informe.md no es el que sale de informe.json")
    except (KeyError, TypeError, ValueError, AttributeError):
        problemas.append("informe.json no tiene la forma de un informe del banco")
    fe = carpeta / "experimento.json"
    if not fe.exists():
        problemas.append("no hay experimento.json: sin el registro no se puede comprobar que el informe sea el que dio el banco")
        return problemas
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import registro_experimentos as rx
    try:
        e = json.loads(fe.read_text(encoding="utf-8"))
        exp = rx.Registro(registro or (carpeta / e["registro"])).experimento(e["exp_id"])
        n = e["intento"]
    except (OSError, ValueError, TypeError, KeyError, rx.RegistroError) as ex:
        return problemas + [f"no se puede leer el experimento del registro: {type(ex).__name__}: {ex}"]
    it = next((x for x in exp["intentos"] if x["n"] == n), None)
    rs = next((x for x in exp["resultados"] if x["n"] == n), None)
    if it is None or it["variante"] != h[:16]:
        problemas.append("el intento del registro no es de este prerregistro")
    if rs is None or rs["detalle"].get("huella_informe") != huella(inf):
        problemas.append("el resultado del registro no casa con el informe")
    return problemas


def veredicto_conjunto(comparaciones: dict) -> str:
    """T-99: «mejor» solo si gana a todas las referencias; «peor» si pierde con alguna; si no, «todavía no se sabe»."""
    vs = [c["veredicto"] for c in comparaciones.values()]
    if vs and all(v == "mejor" for v in vs):
        return "mejor"
    if any(v == "peor" for v in vs):
        return "peor"
    return "todavía no se sabe"


def _arg_entero(minimo: int):
    def f(txt: str) -> int:
        try:
            v = int(txt)
        except ValueError as e:
            raise argparse.ArgumentTypeError(f"{txt!r} no es un entero") from e
        if v < minimo:
            raise argparse.ArgumentTypeError(f"tiene que ser mayor o igual que {minimo}")
        return v
    return f


def _arg_nivel(txt: str) -> float:
    try:
        v = _nivel(float(txt))
    except (ValueError, BancoError) as e:
        raise argparse.ArgumentTypeError(str(e)) from e
    if not NIVEL_MIN <= v <= NIVEL_MAX:
        raise argparse.ArgumentTypeError(f"tiene que estar entre {NIVEL_MIN} y {NIVEL_MAX}")
    return v


def _registro_defecto() -> str | None:
    """El registro del agente (T-99, QA r02 H-17): el mismo que usa registro_experimentos.py por defecto. Con un RI_AGENTE
    no válido no hay registro por defecto, y el banco se detiene al empezar (QA r03)."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import registro_experimentos as rx
    return None if rx.REGISTRO_DEFECTO is None else str(rx.REGISTRO_DEFECTO)


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
    pa.add_argument("--datos", help="carpeta de CSV de precios (por defecto, los datos sintéticos de ejemplo de A)")
    pa.add_argument("--universo", help="CSV del universo (por defecto, el universo de ejemplo de A)")
    pa.add_argument("--semilla", type=_arg_entero(0), default=SEMILLA)
    pa.add_argument("--remuestreos", type=_arg_entero(REMUESTREOS_MIN), default=REMUESTREOS)
    pa.add_argument("--ventana", type=_arg_entero(1), default=VENTANA_MOMENTO)
    pa.add_argument("--nivel", type=_arg_nivel, default=NIVEL)
    pa.add_argument("--min-efectivas", dest="min_efectivas", type=_arg_entero(MIN_EFECTIVAS_MIN), default=MIN_EFECTIVAS)
    # T-99: registro de experimentos (por defecto, el del repositorio); --experimento añade un intento a uno ya prerregistrado
    pa.add_argument("--registro", default=_registro_defecto() or "")
    pa.add_argument("--sin-registro", dest="registro", action="store_const", const=None,
                    help="no anotar en el registro de experimentos (el informe no se podrá verificar)")
    pa.add_argument("--experimento")
    pa.add_argument("--max-variantes", dest="max_variantes", type=_arg_entero(1), default=1)
    pv = sub.add_parser("verificar", help="comprueba las huellas de una carpeta de salida del banco")
    pv.add_argument("carpeta")
    pv.add_argument("--registro")
    a = ap.parse_args(argv)
    if a.bloque == "verificar":
        problemas = verificar(a.carpeta, a.registro)
        for p in problemas:
            print(f"- {p}", file=sys.stderr)
        print("verificado: las huellas casan" if not problemas else f"{len(problemas)} problema(s)")
        return 0 if not problemas else 2
    try:
        inf = ejecutar_a(a)
    except BancoError as e:
        print(f"banco de medida detenido: {e}", file=sys.stderr)
        return 2
    print(json.dumps(inf["comparaciones"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
