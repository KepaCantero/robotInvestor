"""QA r02 de T-102 · Ataques propios del revisor de la r02 al filtro R13/R21 frase a frase (commit 9297df9).

Uso (desde la raíz del repositorio; la raíz del código a atacar es opcional, por defecto el repositorio):
  .venv/bin/python -I .docs/tickets/T-102/revisores/r02_ataques_t102.py [<raiz_repo>] [-k <parte del nombre>]
Cada comprobación imprime OK, FALLO u OBS con su detalle. No escribe nada en el repositorio (los ciclos van a /tmp).
"""
from __future__ import annotations

import json
import sys
import tempfile
import time
from pathlib import Path

ARGS = list(sys.argv[1:])
FILTRO = None
if "-k" in ARGS:
    i = ARGS.index("-k")
    FILTRO = ARGS[i + 1]
    del ARGS[i:i + 2]
RAIZ = Path(ARGS[0] if ARGS else ".").resolve()
EJEC = RAIZ / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJEC / "tests"))
sys.path.insert(0, str(EJEC))

from conftest import AS_OF, DATOS, config_pruebas  # noqa: E402

from bloque_a import diseno_v6 as v6  # noqa: E402
from bloque_a import mock_respuestas as mr  # noqa: E402
from bloque_a.configuracion import CLASES, RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402

assert Path(v6.__file__).resolve().is_relative_to(EJEC.resolve()), v6.__file__
UNIVERSO = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
RES: list[tuple[str, str, str]] = []


def informe(nombre, estado, detalle=""):
    RES.append((nombre, estado, detalle))
    print(f"[{estado:5}] {nombre}: {detalle}", flush=True)


def bloque(perfiles=("DIV",)):
    tmp = Path(tempfile.mkdtemp(prefix="r02_t102_"))
    c = config_pruebas(diseno="v6", perfiles={"activos": list(perfiles)}, seleccion={"umbral_senal_gc1": 0.55})
    return Bloque(c, ProveedorCSV(DATOS), UNIVERSO, MockClient(), tmp / "estado", tmp / "ent")


_PERM = None


def perm():
    global _PERM
    if _PERM is None:
        _PERM = v6.permitidos_r21(bloque(tuple(CLASES)))
    return _PERM


def que(t):
    return v6.texto_prohibido(t, perm())


def pasan(casos):
    return [c for c in casos if que(c) is None]


def quitadas(casos):
    return [c for c in casos if que(c) is not None]


# ====================================================================== H-11: listas y saltos que separan el verbo del código
def at_lista_tras_verbo():
    """El verbo en una frase y los instrumentos en la siguiente (lista con viñetas, numerada o con «;»): la división del CA-8
    parte la compra en trozos que, uno a uno, no incumplen nada."""
    casos = ["Comprar estas tres acciones:\n- NVDA\n- AMD\n- AVGO",
             "Comprar:\n1. NVDA\n2. AMD",
             "Las ideas de la semana, para comprar:\n• NVDA\n• AMD",
             "Comprar: 1. NVDA; 2. AMD.",
             "Comprar estas acciones; NVDA, AMD y AVGO.",
             "Vender ahora... META.",
             "Vender ahora… META.",
             "Probabilidad de recorte en marzo:\n70 %",
             "Probabilidad de que el oro suba en H3:\n- escenario base: 60 %"]
    p = pasan(casos)
    resto = v6.limpiar("Comprar: NVDA; AMD; AVGO.", perm())
    informe("lista_tras_verbo", "FALLO" if p else "OK",
            f"pasan {len(p)}/{len(casos)}: {p!r}; además «Comprar: NVDA; AMD; AVGO.» deja {resto[0]!r} ({resto[1]})")


# ====================================================================== H-12: verbos de R21 que faltan o no admiten artículo
def at_recomendar_y_posiciones():
    casos = ["Recomendamos el ETF IBIT para la exposición a bitcoin.",
             "Recomendamos el ETN VXX como cobertura táctica.",
             "Recomendamos el ETF TBT para apostar por la subida de la TIR.",
             "Recomendamos el fondo Vanguard S&P 500 UCITS ETF (VUSA).",
             "Recomendamos el fondo Invesco CurrencyShares Japanese Yen Trust (FXY).",
             "Nuestra recomendación para el trimestre es NVDA.",
             "Abrir una posición larga en TSLA con stop por debajo de 200 dólares.",
             "Abrir una posición en NVDA.",
             "Abrir posiciones largas en NVDA.",
             "Tomar una posición corta en TSLA.",
             "Abrir un largo en el contrato M6EZ6 de diciembre.",
             "Reducir el peso en INTC.",
             "Elegimos NVDA como opción principal.",
             "La opción preferida es NVDA.",
             "Cubrir la cartera con puts sobre QQQ.",
             "Traspasar el dinero al ETF VWCE es la opción preferida.",
             "Comprar tras los resultados NVDA.",
             "Comprar según el plan NVDA y AMD."]
    p = pasan(casos)
    informe("recomendar_y_posiciones", "FALLO" if p else "OK", f"pasan {len(p)}/{len(casos)}: {p!r}")


# ====================================================================== H-13: horizontes, identificadores y siglas del Documento 0
def at_horizontes_e_identificadores():
    """Frases normales de un informe del Bloque A con un horizonte (H1–H5, que el Sintetizador recibe en `horizontes`) o un
    identificador del paquete (OPP-…) tras un verbo de compra o inversión."""
    casos = ["Comprar duración encaja con el horizonte H3.",
             "Sobreponderar RV europea en H2 y H3.",
             "Invertir en infraestructuras es una tesis H5 con hitos verificables.",
             "Comprar duración en H3 porque la curva se empina.",
             "Comprar exposición a oro en H3 y H4 encaja con el régimen.",
             "Vender dólar frente a yen es una idea H2.",
             "Invertir en RF IG con horizonte principal H3.",
             "Sobreponderar materias primas: banda moderada en H3.",
             "Invertir en metales de transición, como el litio y el níquel, exige horizonte H4.",
             "Comprar RV europea (opción OPP-RV-01).",
             "Vender exposición a oficinas (véase OPP-2026-0012)."]
    q = quitadas(casos)
    informe("horizontes_e_identificadores", "FALLO" if q else "OK", f"quitadas {len(q)}/{len(casos)}: {q!r}")


def at_siglas_del_documento0():
    """Siglas de ámbitos y métricas que el propio Documento 0 usa en la tabla de tipos y en sus estrategias (secciones 2.4 y 8),
    tras «Comprar»: ninguna es un instrumento concreto."""
    siglas = ["ADR", "GDR", "CDS", "CFD", "NFT", "RWA", "ELTIF", "FFO", "AFFO", "CAPE", "LTV", "MVRV", "FX", "DPI", "PME"]
    casos = {s: f"Comprar el segmento con {s} favorable es la lectura del ámbito." for s in siglas}
    casos.update({"CLO": "Comprar CLO AAA europeos.", "MBS": "Comprar MBS de agencia.", "ABS": "Comprar ABS europeos.",
                  "AT1": "Comprar bonos AT1 bancarios.", "CDX": "Comprar protección con el índice CDX IG.",
                  "HICP": "Comprar inflación HICP a diez años.", "SMI": "Comprar el SMI suizo.",
                  "ASX": "Comprar el ASX 200.", "GCC": "Comprar mercados del GCC.", "SOX": "Comprar semiconductores (SOX)."})
    q = sorted(s for s, f in casos.items() if que(f))
    informe("siglas_del_documento0", "OBS" if q else "OK", f"quitadas {len(q)}/{len(casos)}: {q}")


# ====================================================================== H-14: R13 quita la forma cualitativa que R13 pide
def at_r13_forma_cualitativa():
    """R13 (Documento 0): sin certificado, «la previsión se expresa en bandas cualitativas». «Es probable que X suba un N %»
    es esa forma: banda cualitativa + magnitud del movimiento, sin probabilidad numérica."""
    casos = ["Es probable que los beneficios del sector crezcan un 8 % en 2027.",
             "Es probable que el oro suba un 5 % más.",
             "Es probable que la inflación cierre el año en el 2,4 %.",
             "Es probable que el IPC se modere al 2,1 % en primavera.",
             "Es probable que el paro suba al 6,5 % en 2027.",
             "Es poco probable que el tipo de depósito baje del 1,5 % en este ciclo.",
             "Lo más probable es que el oro consolide tras subir un 25 % en el año.",
             "Es probable que la TIR del Treasury a 10 años oscile entre el 4 % y el 4,6 % en H2.",
             "La probabilidad de un recorte al 4,25 % sube.",
             "La probabilidad de que el tipo baje al 4,25 % sube.",
             "La probabilidad de un tipo terminal del 3 % ha bajado.",
             "La posibilidad de una subida del BOJ al 0,75 % gana peso en la semana."]
    q = quitadas(casos)
    control = que("La probabilidad de un recorte hasta el 4,25 % sube.")
    informe("r13_forma_cualitativa", "FALLO" if q else "OK",
            f"quitadas {len(q)}/{len(casos)} (el ejemplo del README, «hasta el 4,25 %», da {control}): {q!r}")


# ====================================================================== H-15: formas de R13 que pasan
def at_r13_formas_que_pasan():
    casos = ["Con una confianza del 70 %, el diferencial italiano se estrechará en H3.",
             "Confianza: 80 %.",
             "Escenarios para la RV europea: base (55 %), alcista (25 %) y bajista (20 %).",
             "Escenario alcista (30 %): el oro sube a 3.200 dólares.",
             "Las opciones de un empinamiento de la curva son de 3 de cada 4.",
             "Asignamos una probabilidad de 7 sobre 10 a la subida.",
             "Vemos 2/3 de probabilidad de recorte.",
             "Una probabilidad de 70 por 100.",
             "P(subida) = 70 %."]
    p = pasan(casos)
    informe("r13_formas_que_pasan", "FALLO" if p else "OK", f"pasan {len(p)}/{len(casos)}: {p!r}")


# ====================================================================== bajos
def at_series_de_tokens():
    """H-09 de la r01: un token concreto es un instrumento (BTC y ETH salen de la lista), pero su serie del universo no."""
    casos = {"Comprar BTC.": que("Comprar BTC."), "Comprar BTC-USD.": que("Comprar BTC-USD."),
             "Comprar SOL.": que("Comprar SOL."), "Comprar SOL-USD.": que("Comprar SOL-USD.")}
    incoh = casos["Comprar BTC."] != casos["Comprar BTC-USD."] or casos["Comprar SOL."] != casos["Comprar SOL-USD."]
    informe("series_de_tokens", "OBS" if incoh else "OK", repr(casos))


def at_emision_con_abreviatura():
    a = "Recomendamos el bono de Telefónica con vencimiento en 2031."
    b = "Comprar bonos del Tesoro de EE. UU. con vencimiento en 2030."
    c = "Comprar bonos del Tesoro de EEUU con vencimiento en 2030."
    r = {a: que(a), b: que(b), c: que(c)}
    informe("emision_con_abreviatura", "OBS" if r[b] != r[c] else "OK", repr(r))


# ====================================================================== división, idempotencia y espacios
def at_idempotencia_y_espacios():
    pr = perm()
    problemas = []
    textos = ["El dólar sube.\r\nEl euro baja.", "El dólar sube.  El euro baja.\t", "  El oro sube. ", "Línea 1\n\n\nLínea 2",
              "El dólar sube. El euro baja.", "Comprar AAPL. El oro sube.", "El oro sube. Comprar AAPL.\nEl dólar cae.",
              "Comprar AAPL.\r\nEl oro sube.\r\n", "Dato del 2 %. Hay un 70 % de probabilidad.  El euro sube."]
    for t in textos:
        a, ra = v6.limpiar(t, pr)
        b, rb = v6.limpiar(a, pr)
        if rb or a != b:
            problemas.append(("no idempotente", t, a, b))
        if not ra and a != t:
            problemas.append(("un texto limpio cambia", t, a))
    # espacios Unicode entre la cifra y el signo, o entre el verbo y el código
    for t in ["Hay un 70 % de probabilidad de subida.", "Hay un 70 % de probabilidad de subida.", "Comprar AAPL."]:
        if que(t) is None:
            problemas.append(("espacio Unicode", t))
    informe("idempotencia_y_espacios", "FALLO" if problemas else "OK", repr(problemas))


# ====================================================================== rendimiento con salidas degeneradas (≈ 30.000 caracteres)
def at_rendimiento_30k():
    n = 30000
    casos = {
        "comprar_oro_coma": ("Comprar oro, " * (n // 13)),
        "verbos_sin_corte_y_codigo_final": ("comprar " * (n // 8)) + "AAPL",
        "verbo_y_muchos_codigos_permitidos": "Comprar " + ("USD EUR JPY " * (n // 12)),
        "probabilidad_y_cifras": ("probabilidad del tipo en el 2 % " * (n // 32)),
        "tope_hasta": ("recorte de la de la de la " * (n // 26)) + "hasta el 2 %",
        "nivel_funcion_larga": "probable " + ("tipo " + "de la " * 4000) + "2 %",
        "mayusculas_y_sufijo": ("Apple Microsoft " * (n // 16)) + "Inc",
        "indices": "Comprar " + ("MSCI World S&P 500 " * (n // 19)),
        "abreviaturas": ("EE. UU. S.A. p. ej. etc. " * (n // 25)),
        "saltos": ("Comprar oro\n" * (n // 12)),
        "puntos": ("Comprar oro. " * (n // 13)),
        "y_verbo": ("comprar oro y vender plata y " * (n // 29)) + "AAPL",
        "bonos_vencimiento": ("bonos " * (n // 6)) + "vencimiento en 2030",
        "isin_falsos": ("ES0000012M8 " * (n // 12)),
    }
    pr = perm()
    tiempos = {}
    for k, t in casos.items():
        t0 = time.perf_counter()
        v6.limpiar(t, pr)
        tiempos[k] = round(time.perf_counter() - t0, 3)
    total = sum(tiempos.values())
    lentos = {k: s for k, s in tiempos.items() if s > 1}
    informe("rendimiento_30k", "FALLO" if total > 2 else "OK", f"total {total:.2f} s; lentos (> 1 s) {lentos}; todos {tiempos}")


def at_rendimiento_escala():
    """Cómo crece el tiempo con la longitud en el caso más lento (para ver si es cuadrático)."""
    pr = perm()
    out = {}
    for n in (5000, 10000, 20000, 30000):
        t = "Comprar oro, " * (n // 13)
        t0 = time.perf_counter()
        v6.limpiar(t, pr)
        out[n] = round(time.perf_counter() - t0, 3)
    informe("rendimiento_escala", "OBS", repr(out))


# ====================================================================== camino real: el ciclo V6 con el Sintetizador simulado
def ciclo_con_sintetizador(cambiar, perfiles=("DIV",)):
    orig = mr._sintetizador

    def g(msg, ctx, rng):
        out = orig(msg, ctx, rng)
        cambiar(out)
        return out
    mr._sintetizador = g
    try:
        b = bloque(perfiles)
        reds = []
        gen = b.redaccion.generar

        def generar(bl, paquete, extras, red, *a, **k):
            reds.append(json.loads(json.dumps(red, ensure_ascii=False)))
            return gen(bl, paquete, extras, red, *a, **k)
        b.redaccion.generar = generar
        r = b.ciclo(AS_OF)
    finally:
        mr._sintetizador = orig
    return b, r, reds


def entregables_texto(r) -> str:
    e = r.get("entregables") or {}
    return " ".join(Path(p).read_text(encoding="utf-8") for p in e.values() if isinstance(p, str) and Path(p).exists())


def at_camino_real_lista_y_recomendar():
    """Por el camino real: cada texto del Sintetizador lleva una compra en lista (H-11) o una recomendación (H-12). ¿Llega algún
    código al paquete o a los entregables?"""
    marcas = {"NVDA": "Comprar estas acciones:\n- NVDA\n- AMD", "IBIT": "Recomendamos el ETF IBIT.",
              "TSLA": "Tomar una posición corta en TSLA.", "VXX": "Recomendamos el ETN VXX como cobertura.",
              "70 %": "Probabilidad de recorte en marzo:\n70 %"}
    texto = " ".join(marcas.values())

    def cambiar(out):
        out["regimen_macro"] = "El dólar sigue fuerte. " + marcas["NVDA"]
        out["lectura_conjunto"] = "Las ideas comparten el factor dólar. " + marcas["IBIT"]
        out["frases_30s"][0] = "El dólar manda esta semana. " + marcas["TSLA"]
        for t in out["tarjetas"]:
            t["por_que_llano"] = "El dólar sube desde hace meses. " + marcas["VXX"]
            t["que_puede_salir_mal_llano"] = "Si el dólar cae, la idea cae. " + marcas["70 %"]
        out["frase_historial"] = "Hay pocos casos todavía. " + marcas["IBIT"]
    _b, r, reds = ciclo_con_sintetizador(cambiar)
    p = r.get("paquete") or {}
    todo = json.dumps([p, reds[-1] if reds else {}], ensure_ascii=False)
    ent = entregables_texto(r)
    fugas = {k: (k in todo, k in ent) for k in marcas}
    hay = [k for k, (a, b) in fugas.items() if a or b]
    lim = [x for x in p.get("limitaciones", []) if "quitadas" in x]
    informe("camino_real_lista_y_recomendar", "FALLO" if hay else "OK",
            f"llegan (paquete o redacción, entregables): {fugas}; limitaciones={lim}; texto inyectado={texto!r}")


def at_camino_real_horizonte_en_tarjeta():
    """Una tarjeta normal con su horizonte («... con horizonte principal H3») pierde el texto y toma el de por defecto."""
    def cambiar(out):
        for t in out["tarjetas"]:
            t["por_que_llano"] = "Invertir en esta zona encaja con el horizonte H3."
    _b, r, reds = ciclo_con_sintetizador(cambiar)
    red = reds[-1] if reds else {}
    tarj = [t["por_que_llano"] for t in red.get("tarjetas", [])]
    perdidas = sum(1 for x in tarj if "H3" not in x)
    informe("camino_real_horizonte_en_tarjeta", "FALLO" if perdidas else "OK",
            f"tarjetas que pierden su texto: {perdidas}/{len(tarj)}; quedan {sorted(set(tarj))!r}")


PRUEBAS = [v for k, v in sorted(globals().items()) if k.startswith("at_") and callable(v)]


def main() -> int:
    for f in PRUEBAS:
        if FILTRO and FILTRO not in f.__name__:
            continue
        try:
            f()
        except Exception as e:  # noqa: BLE001
            informe(f.__name__[3:], "ERROR", f"{type(e).__name__}: {e}")
    print(f"\nResumen: {sum(1 for r in RES if r[1] == 'OK')} OK, {sum(1 for r in RES if r[1] == 'FALLO')} FALLO, "
          f"{sum(1 for r in RES if r[1] == 'OBS')} OBS, {sum(1 for r in RES if r[1] == 'ERROR')} ERROR")
    return 0


if __name__ == "__main__":
    sys.exit(main())
