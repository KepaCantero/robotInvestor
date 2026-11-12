"""T-102 · Filtro R13/R21 frase a frase de los textos del Sintetizador (diseño V6): H-23 y H-24 de la QA r03 de T-101.

Banco fijo de frases legítimas (de informes de divisas, índices, materias primas, derivados y tipos) y prohibidas (probabilidades
numéricas, R13; compra o venta de un instrumento concreto, R21), tomado de las QA r02 y r03 de T-101. Un nombre propio suelto sin
código ni sufijo («entrar en Tesla») es un límite declarado y no está en el banco."""
import copy
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


# ================================================================================================== ronda r02 (QA r01 de T-102)
# Casos del banco del revisor (`.docs/tickets/T-102/revisores/r01_banco_frases.py`) que fallaban, y otros nuevos.
R13_R02 = [   # H-01: «la probabilidad de que X … es del N %» y formas parecidas
    "La probabilidad de que el S&P 500 suba este mes es del 70 %.", "Las probabilidades de un recorte en marzo son del 60 %.",
    "La probabilidad de que bajen los alquileres es del 40 %.", "El escenario alcista tiene una probabilidad estimada del 65 %.",
    "La probabilidad implícita de un movimiento del 5 % es del 18 %.", "La probabilidad de una corrección del 10 % es del 30 %.",
    "Probabilidad de que el euro caiga: 70 %.", "Probabilidad de subida del crudo: 80 %.",
    "La probabilidad de inversión de la curva este año es del 35 %.", "Con un 80 % de seguridad, la renta variable sube.",
    "La probabilidad de que el tipo de interés baje es del 70 %.", "Estimamos que hay 7 de cada 10 posibilidades de una subida.",
    "Las chances de una corrección son del 30 %.", "Hay un 40 % de riesgo de recesión en Europa este año.",
    "Con una probabilidad de 0,7, el euro se aprecia.", "El modelo da un 80 % de que la curva se desinvierta.",
    "La probabilidad de que la inflación supere el 3 % es del 40 %.", "La probabilidad se sitúa en el 70 %.",
]
R21_R02 = [   # H-02: listas tras «:» o «,», incisos, abreviaturas, verbos nuevos, sufijos de bolsa
    "Comprar: NVDA, AMD y AVGO.", "Para la cobertura, comprar: FXF.", "Conviene comprar, por valoración, META.",
    "Compra, esta semana, acciones de Apple (AAPL).", "Conviene comprar acciones de EE. UU. como AAPL esta semana.",
    "Vender bancos de EE. UU. y en concreto JPM.", "Comprar tecnológicas de EE. UU. (AAPL, MSFT).", "Apostar por NVDA antes de resultados.",
    "Acumular MSFT en las caídas.", "Invertir en XEON.DE para la liquidez en euros.", "Recomendamos vender las acciones de Inditex (ITX.MC).",
    "Conviene comprar ahora mismo AAPL.", "Vender, sin esperar más, TSLA.", "Ponerse largos en SMH antes de resultados.",
    "Conviene liquidar la posición en NFLX.", "Vender las acciones de Nestlé SA.", "Telefónica S.A. mejora márgenes.",
    "Conviene vender las acciones de BHP y comprar RIO.", "Comprar BTC ahora.", "Comprar el ETF EWZ si Brasil recorta tipos.",
    "El ISIN US0378331005 cotiza al alza.", "Conviene comprar la acción de Inditex.",   # ISIN sin verbo; `_UNITARIA` sin código
]
LEGITIMAS_R02 = [   # H-03: siglas que no son instrumentos; H-01: cifras que no son probabilidades
    "Conviene vender EUR/USD si el BCE recorta antes que la Fed.", "El mercado compra USD/JPY por el diferencial de tipos.",
    "Comprar crédito BBB a dos años ofrece un diferencial atractivo frente al Tesoro.", "Sobreponderar LATAM frente a Asia.",
    "Invertir en IA sigue siendo el tema dominante del mercado.", "Conviene no vender volatilidad antes de la reunión del FOMC.",
    "Comprar compañías con PER bajo ha batido al índice este trimestre.", "Invertir en fondos con TER bajo mejora la rentabilidad neta.",
    "La compra de fondos cerrados con descuento sobre el NAV es una idea recurrente.", "Invertir en SOCIMI cotizadas da exposición al alquiler.",
    "Invertir en el EURO STOXX 50 tiene sentido si mejora el PMI europeo.", "Invertir en el MSCI ACWI es la forma más sencilla de diversificar.",
    "Vender straddles sobre el SPX rinde un 1 % al mes con volatilidad baja.", "Comprar el CSI 300 tiene sentido si China estimula.",
    "Conviene comprar gas TTF para el invierno si los inventarios bajan.", "Vender el índice BCOM frente al oro ha funcionado en el ciclo.",
    "Invertir en ILS tiene sentido tras una temporada de huracanes tranquila.", "Invertir en FMM a corto plazo da un 3 % sin riesgo de duración.",
    "La venta de bonos del Tesoro de EE.UU. por bancos centrales extranjeros continúa.", "Conviene vender bonos de EE. UU. a largo si sube la prima.",
    "El VaR al 95 % de confianza de la estrategia es del 2,1 %.", "Los pronósticos acertaron el 58 % de las veces en el historial.",
    "La probabilidad es baja, pero un 5 % del capital comparte el factor de riesgo.", "Es probable que el BCE recorte en junio.",
    "La probabilidad de un aterrizaje suave ha aumentado, según la encuesta.", "El rendimiento del bono a 2 años se sitúa en el 4,1 %.",
    "La correlación entre RV y RF vuelve a ser negativa, en torno a -0,3.", "Vender JPY y comprar AUD es la expresión clásica del carry.",
    "Acumular liquidez en USD rinde más que en EUR este año.", "Vender EURGBP si el BoE recorta antes que el BCE.",
    "Comprar EUR y esperar a ver qué hace el ETF de oro GLD.", "Nada de esto es un consejo para comprar o vender.",
    "Conviene vender HY si el ETF HYG pierde la media de 200 sesiones.",   # el código tras una subordinada no es lo comprado
]


@pytest.mark.parametrize("frase", R13_R02)
def test_r02_h01_una_probabilidad_numerica_se_quita(perm, frase):
    assert v6.texto_prohibido(frase, perm) == "R13"


@pytest.mark.parametrize("frase", R21_R02)
def test_r02_h02_la_compra_en_toda_la_frase_se_caza(perm, frase):
    assert v6.texto_prohibido(frase, perm) == "R21"


@pytest.mark.parametrize("frase", LEGITIMAS_R02)
def test_r02_h03_siglas_y_cifras_legitimas_se_conservan(perm, frase):
    assert v6.texto_prohibido(frase, perm) is None


@pytest.mark.parametrize(("texto", "esperado"), [
    ("Comprar acciones de Banco Santander S.A. ya. El dólar cae.", "El dólar cae."),
    ("La renta variable de EE. UU. sube un 2 %. Conviene comprar AAPL. El dólar cae frente al EUR.",
     "La renta variable de EE. UU. sube un 2 %. El dólar cae frente al EUR."),
    ("El dólar sube frente al euro\nConviene comprar AAPL", "El dólar sube frente al euro"),
    ("El dólar sube frente al euro… Conviene comprar AAPL.", "El dólar sube frente al euro…"),
    ("El dólar sube. Hay un 70 % de probabilidad de subida; el euro baja.", "El dólar sube. el euro baja."),
    ("Comprar US0378331005. El dólar sube.", "El dólar sube."),
    ("La venta de TSLA se acelera. El dólar sube.", "El dólar sube."),
])
def test_r02_h04_se_divide_sin_partir_abreviaturas(perm, texto, esperado):
    assert v6.limpiar(texto, perm)[0] == esperado


def test_r02_h04_un_texto_sin_nada_prohibido_sale_igual(perm):
    t = "  El dólar sube.\n\nEl euro baja.  La RV de EE. UU. cae un 1,5 %.\n"
    assert v6.limpiar(t, perm) == (t, [])


def test_r02_h07_textos_largos_en_tiempo_lineal(perm):
    import time
    casos = ["Apple Microsoft Alphabet Amazon " * 2000, "acciones de " * 2500, "Comprar " + "AAPL " * 3000]
    t0 = time.perf_counter()
    for t in casos:
        v6.texto_prohibido(t, perm)
    assert time.perf_counter() - t0 < 2


def test_r02_h10_cada_campo_por_el_camino_real(tmp_path, monkeypatch):
    """Una frase legítima y una prohibida en cada uno de los textos del Sintetizador: sale la legítima, lo que se queda vacío
    toma su defecto y todo se declara (H-05 y H-10). El ISIN, «la venta de» y el «;» van en campos distintos."""
    orig = mr._sintetizador
    MALA = "Conviene comprar AAPL cuanto antes."
    capt: dict = {}

    def sintetizador(msg, ctx, rng):
        out = orig(msg, ctx, rng)
        out["regimen_macro"] = "Marca régimen con el dólar fuerte. Hay un 70 % de probabilidad de subida."
        for f in out["factores_dominantes"]:
            f["factor"] = "Marca factor del clúster. Comprar US0378331005 ya."
        out["preguntas_sugeridas"] = ["¿Marca pregunta sobre el carry? La venta de TSLA es urgente."]
        out["lectura_conjunto"] = "Marca lectura: el Analista no ve motivos para vender EURUSD tras el dato; " + MALA
        out["limitaciones"] = ["Marca limitación de datos sintéticos. " + MALA]
        out["frases_30s"][0] = "Marca treinta. " + MALA
        out["frases_30s"][1] = "Hay un 70 % de probabilidad de subida."
        for t in out["tarjetas"]:
            t["por_que_llano"] = "Marca por qué. " + MALA
            t["que_puede_salir_mal_llano"] = "Marca riesgo. Vender MSFT."
            t["ambito_llano"] = "Marca ámbito. Comprar NVDA."
        out["motivos_llanos"] = {"RV": "Marca motivo. " + MALA}
        out["glosario"] = [{"termino": "Carry", "definicion": "Marca glosario."}, {"termino": "ETF", "definicion": "Comprar QQQ es un ejemplo."}]
        out["frase_historial"] = "Marca historial. " + MALA
        return out
    monkeypatch.setattr(mr, "_sintetizador", sintetizador)
    b = _bloque(tmp_path)
    orig_gen = b.redaccion.generar

    def generar(bloque, paquete, extras, r, *a, **k):
        capt["red"], capt["defecto"] = copy.deepcopy(r), bloque.redaccion.textos_por_defecto(paquete)
        return orig_gen(bloque, paquete, extras, r, *a, **k)
    b.redaccion.generar = generar
    res = b.ciclo(AS_OF)
    p, red = res["paquete"], capt["red"]
    todo = json.dumps([p, red], ensure_ascii=False)
    for x in ("AAPL", "US0378331005", "TSLA", "MSFT", "NVDA", "QQQ", "70 %"):
        assert x not in todo, x
    assert p["regimen_macro"] == "Marca régimen con el dólar fuerte."
    assert p["clusteres_exposicion"] and all(c["factor_dominante"] == "Marca factor del clúster." for c in p["clusteres_exposicion"])
    assert p["preguntas_sugeridas"] == ["¿Marca pregunta sobre el carry?"]
    assert p["x_lectura_conjunto"] == "Marca lectura: el Analista no ve motivos para vender EURUSD tras el dato;"
    assert "Sintetizador: Marca limitación de datos sintéticos." in p["limitaciones"]
    assert red["frases_30s"][0] == "Marca treinta." and red["frases_30s"][1] == capt["defecto"]["frases_30s"][1]
    assert red["tarjetas"] and all(t["por_que_llano"] == "Marca por qué." and t["que_puede_salir_mal_llano"] == "Marca riesgo."
                                   and t["ambito_llano"] == "Marca ámbito." for t in red["tarjetas"])
    assert red["motivos_llanos"] == {"RV": "Marca motivo."}
    assert [g["termino"] for g in red["glosario"]] == ["Carry"]
    assert red["frase_historial"] == "Marca historial."
    n_tarj = len(red["tarjetas"])
    llanas = [x for x in p["limitaciones"] if x.startswith("Frases llanas del Sintetizador quitadas")]
    assert llanas == [f"Frases llanas del Sintetizador quitadas por R13, R21: {2 + 3 * n_tarj + 3}; el resto de sus textos se conserva"]
    integ = next(x for x in p["limitaciones"] if x.startswith("Frases del Sintetizador quitadas"))
    for campo in ("regimen_macro (R13)", "factores_dominantes (R21)", "preguntas_sugeridas (R21)", "lectura_conjunto (R21)", "limitaciones (R21)"):
        assert campo in integ


def test_r02_h06_la_reescritura_declara_solo_lo_que_se_entrega(tmp_path, monkeypatch):
    larga = ("Las consideraciones macroeconómicas internacionalizadas multidimensionalmente condicionan extraordinariamente "
             "la interpretación probabilísticamente fundamentada de correlaciones intertemporales heterogéneas")
    orig = mr._sintetizador
    n = {"k": 0}

    def sintetizador(msg, ctx, rng):
        n["k"] += 1
        out = orig(msg, ctx, rng)
        if n["k"] == 1:
            out["frases_30s"] = [larga + ". Comprar AAPL.", larga + ".", larga + "."]
            for t in out["tarjetas"]:
                t["por_que_llano"] = larga[:150] + "."
            out["frase_historial"] = larga + "."
        return out
    monkeypatch.setattr(mr, "_sintetizador", sintetizador)
    res = _bloque(tmp_path).ciclo(AS_OF)
    assert n["k"] == 2
    assert not [x for x in res["paquete"]["limitaciones"] if x.startswith("Frases llanas del Sintetizador quitadas")]
    assert res["paquete"]["limitaciones"]
