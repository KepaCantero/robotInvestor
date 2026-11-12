"""T-102 · Filtro R13/R21 frase a frase de los textos del Sintetizador (diseño V6): H-23 y H-24 de la QA r03 de T-101.

Banco fijo de frases legítimas (de informes de divisas, índices, materias primas, derivados y tipos) y prohibidas (probabilidades
numéricas, R13; compra o venta de un instrumento concreto, R21), tomado de las QA r02 y r03 de T-101. Un nombre propio suelto sin
código ni sufijo («entrar en Tesla») es un límite declarado y no está en el banco."""
import json
from pathlib import Path

import pytest
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, fusionar
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
from conftest import AS_OF, DATOS, config_pruebas

from bloque_a import diseno_v6 as v6
from bloque_a import mock_respuestas as mr

LEGITIMAS = [
    "Un 5 % del capital ya está en opciones del mismo clúster.",
    "La probabilidad es baja; aun así, un 5 % del capital comparte el factor de riesgo.",
    "Los pronósticos con probabilidad alta acertaron el 62 % de las veces en el historial.",
    "¿Conviene vender USD frente al EUR si el diferencial de tipos se estrecha?",
    "El Analista prefiere no comprar RF larga mientras suba la inflación.",
    "Con el dólar fuerte, puede tener sentido vender EM y esperar.",
    "El ETF de referencia (SPY) sigue al índice; no es una recomendación.",
    "El índice VIX sube; el riesgo de cola de RV aumenta.",
    "Si la curva se empina, el segmento de vender HY pierde atractivo.",
    "Las opciones de renta fija ganan un 3 % en el mes.",
    "Las tres opciones de RV acumulan un 4,2 % desde la última revisión.",
    "Las opciones del mismo clúster comparten una correlación de 0,8.",
    "Dos de las opciones vigentes caen más de un 5 % y siguen por encima de su invalidación.",
    "La venta de opciones de compra sobre el S&P 500 rinde un 1,5 % mensual.",
    "Las opciones sobre el VIX cotizan con una prima del 12 % sobre la media.",
    "Vender volatilidad con opciones de venta cubiertas rinde un 0,9 % al mes.",
    "La probabilidad de un recorte de la Fed hasta el 4,25 % ha subido.",
    "El mercado descuenta con alta probabilidad que el BCE deje el depósito en el 2 %.",
    "Conviene vender MSCI World frente a emergentes según el régimen.",
    "El índice ISM manufacturero sube; se compra DXY en la sesión.",
    "El Analista no ve motivos para vender EURUSD tras el dato de empleo.",
    "Los fondos tienden a comprar GBPUSD cuando sube el diferencial de tipos.",
    "El mercado vende JPY y compra MXN por el carry.",
    "Los operadores vuelven a la compra de WTI tras el recorte de la OPEP.",
    "Los bancos centrales siguen comprando oro; la venta de GNL a Europa crece.",
    "Los inversores venden BRENT y compran oro.",
    "El diferencial BAMLH0A0HYM2 se estrecha 20 pb en el mes.",
    "La pendiente CURVA-USD-2S10S-TR vuelve a positivo.",
]
PROHIBIDAS = [
    ("R13", "Probabilidad del 87 % de que el dólar suba este trimestre."), ("R13", "Hay un 70 % de probabilidad de subida."),
    ("R13", "La probabilidad de subida es de 0,87."), ("R13", "Vemos un 87 por ciento de probabilidades de subida."),
    ("R13", "Un 80 % de posibilidades de que el euro baje."), ("R13", "El escenario base tiene un 65 % de opciones de cumplirse."),
    ("R13", "Probabilidad de subida: 87 %."), ("R13", "Es probable al 80 % que el euro baje."),
    ("R13", "Vemos un 87 % de confianza en la subida."),
    ("R21", "Conviene comprar AAPL cuanto antes."), ("R21", "Compra acciones de Apple (AAPL)."),
    ("R21", "compra acciones de Apple (AAPL) esta semana."), ("R21", "Comprar AAPL es la mejor idea."),
    ("R21", "Recomendamos la compra de AAPL y de MSFT."), ("R21", "Sobreponderar Microsoft Corp frente al índice."),
    ("R21", "Comprar el bono del Tesoro a 10 años con vencimiento 2034."), ("R21", "Comprar US0378331005 ya."),
    ("R21", "Recomendamos invertir en NVDA este trimestre."), ("R21", "Conviene vender las acciones de TSLA."),
    ("R21", "Comprar el ETF QQQ es la mejor forma de exponerse."), ("R21", "Comprar ETF ARKK para la innovación."),
    ("R21", "Tomar posiciones en MSFT y GOOGL."), ("R21", "Vender un poco de META y comprar algo de NFLX."),
    ("R21", "Abrir largos en AMZN ya."), ("R21", "Conviene comprar GLD como cobertura."), ("R21", "Sobreponderar XLK frente al índice."),
]


def _cfg(**extra):
    return config_pruebas(**fusionar({"diseno": "v6", "perfiles": {"activos": ["DIV"]}, "seleccion": {"umbral_senal_gc1": 0.55}}, extra))


def _bloque(tmp, cli=None):
    return Bloque(_cfg(), ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), cli or MockClient(), Path(tmp) / "estado", Path(tmp) / "ent")


@pytest.fixture(scope="module")
def perm(tmp_path_factory):
    return v6.permitidos_r21(_bloque(tmp_path_factory.mktemp("perm")))


@pytest.mark.parametrize("frase", LEGITIMAS)
def test_una_frase_legitima_no_se_quita(perm, frase):
    """H-23: «opciones», porcentajes que no son probabilidades, pares sin barra, siglas y series del universo."""
    assert v6.texto_prohibido(frase, perm) is None


@pytest.mark.parametrize(("regla", "frase"), PROHIBIDAS)
def test_una_frase_prohibida_se_caza_con_su_regla(perm, regla, frase):
    """H-24: compras con artículo o con un sustantivo entre medias, «invertir en», tickers de fondo del universo, probabilidades."""
    assert v6.texto_prohibido(frase, perm) == regla


def test_se_quita_la_frase_y_se_conserva_el_resto(perm):
    t = "El dólar se fortalece. Conviene comprar AAPL cuanto antes. Las opciones de renta fija ganan un 3 % en el mes."
    limpio, reglas = v6.limpiar(t, perm)
    assert reglas == ["R21"] and "AAPL" not in limpio and limpio.startswith("El dólar se fortalece.") and "renta fija" in limpio


def test_sin_codigos_permitidos_un_par_de_divisas_es_sospechoso():
    """Los códigos permitidos vienen de la configuración y del universo: sin ellos, el filtro es estricto (falla cerrado)."""
    assert v6.texto_prohibido("Conviene vender EURUSD.", {"codigos": frozenset(), "series": frozenset()}) == "R21"


def test_una_tarjeta_mala_no_tira_las_demas(tmp_path, monkeypatch):
    """H-23: una sola tarjeta con una frase prohibida toma su texto por defecto; las demás y las frases de 30 s se conservan."""
    orig = mr._sintetizador
    capt = {}

    def sintetizador(msg, ctx, rng):
        out = orig(msg, ctx, rng)
        out["tarjetas"][0]["por_que_llano"] = "Conviene comprar AAPL cuanto antes."
        out["frases_30s"][2] = "Cada idea puede salir mal. Hay un 70 % de probabilidad de subida."
        capt["buenas"] = [t["por_que_llano"] for t in out["tarjetas"][1:]]
        capt["frase0"] = out["frases_30s"][0]
        return out
    monkeypatch.setattr(mr, "_sintetizador", sintetizador)
    b = _bloque(tmp_path)
    red = {}
    orig_gen = b.redaccion.generar

    def generar(bloque, paquete, extras, r, *a, **k):
        red.update(r)
        return orig_gen(bloque, paquete, extras, r, *a, **k)
    b.redaccion.generar = generar
    res = b.ciclo(AS_OF)
    assert len(red["tarjetas"]) >= 2, "la prueba necesita al menos dos tarjetas"
    assert "AAPL" not in json.dumps(red, ensure_ascii=False) and red["tarjetas"][0]["por_que_llano"]
    assert [t["por_que_llano"] for t in red["tarjetas"][1:]] == capt["buenas"]
    assert red["frases_30s"][0] == capt["frase0"] and red["frases_30s"][2] == "Cada idea puede salir mal."
    assert any("Frases llanas del Sintetizador quitadas" in x for x in res["paquete"]["limitaciones"])
    assert res["g3_entregables"]["dictamen"] != "BLOQUEADO"


def test_en_la_integracion_se_quita_solo_la_frase(tmp_path, monkeypatch):
    orig = mr._sintetizador

    def sintetizador(msg, ctx, rng):
        out = orig(msg, ctx, rng)
        out["lectura_conjunto"] = "Las opciones dependen del dólar. Conviene vender las acciones de TSLA. El riesgo es la reversión."
        return out
    monkeypatch.setattr(mr, "_sintetizador", sintetizador)
    r = _bloque(tmp_path).ciclo(AS_OF)
    assert r["paquete"]["x_lectura_conjunto"] == "Las opciones dependen del dólar. El riesgo es la reversión."
    assert any("Frases del Sintetizador quitadas" in x for x in r["paquete"]["limitaciones"])
