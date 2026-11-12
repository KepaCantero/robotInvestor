"""T-102 · Textos del Sintetizador (diseño V6) con marcadores y una regla estricta (ronda r03, decisión del operador del
12-11-2026). El Sintetizador escribe con marcadores ({opp:…}, {tipo:…}, {n:…}, {candidatas:…}, {n_ideas}, {n_tipos} y
{n_apuestas}) que rellena el código. Su texto libre no lleva ninguna cifra ni ningún código de un instrumento concreto, y una
frase que incumple la regla se quita (falla cerrado) y se declara.

Los bancos recogen las frases de las QA r01 y r02 de T-102 que antes pasaban (listas, «recomendamos el ETF X», «la opción
preferida es X», probabilidades en letra o con cifra) y frases legítimas escritas como pide el prompt (sin cifras)."""
import copy
import json
import time
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
    "El dólar se fortalece frente a las divisas emergentes.",
    "La probabilidad es baja, pero varias ideas comparten el mismo factor de riesgo.",
    "Es probable que el BCE recorte tipos este verano.",
    "El mercado asigna alta probabilidad a una pausa de la Fed.",
    "Conviene vender EUR/USD si el BCE recorta antes que la Fed.",
    "El mercado compra USD/JPY por el diferencial de tipos.",
    "Vender JPY y comprar AUD es la expresión clásica del carry.",
    "Comprar crédito BBB a corto plazo ofrece un diferencial atractivo frente al Tesoro.",
    "Sobreponderar LATAM frente a Asia gana peso con el dólar débil.",
    "Invertir en IA sigue siendo el tema dominante del mercado.",
    "Conviene no vender volatilidad antes de la reunión del FOMC.",
    "Invertir en el MSCI ACWI es la forma más sencilla de diversificar.",
    "Comprar el EURO STOXX tiene sentido si mejora el PMI europeo.",
    "La venta de bonos del Tesoro de EE. UU. por bancos centrales extranjeros continúa.",
    "Los diferenciales de CDS y de CLO se estrechan en el mes.",
    "Los activos tokenizados (RWA) ganan atractivo con la regulación.",
    "El índice VIX sube; el riesgo de cola de RV aumenta.",
    "Las opciones del mismo clúster comparten el impulso de precios.",
    "Nada de esto es un consejo para comprar o vender.",
    "¿Qué haría cambiar el semáforo de RV?",
    "Esta semana vemos {n_ideas} ideas en {n_tipos} tipos de inversión.",
    "{opp:OPP-2026-0001} depende sobre todo del dólar.",
    "Miramos {candidatas:RV} ideas de {tipo:RV} y solo {n:RV} pasaron los filtros.",
    "En realidad son {n_apuestas} apuestas distintas.",
]
PROHIBIDAS = [
    # CIFRA: cualquier cifra, también las probabilidades que antes pasaban (QA r02, H-15) y los horizontes (H-13)
    ("CIFRA", "La probabilidad de que el S&P 500 suba este mes es del 70 %."), ("CIFRA", "Hay un 70 % de probabilidad de subida."),
    ("CIFRA", "La probabilidad de subida es de 0,87."), ("CIFRA", "Con una confianza del 70 % la RV sube."),
    ("CIFRA", "Confianza: 80 %."), ("CIFRA", "P(subida) = 70 %."), ("CIFRA", "Lo vemos en 7 sobre 10."), ("CIFRA", "Un escenario de 2/3."),
    ("CIFRA", "Vemos un setenta por ciento de probabilidades de subida."), ("CIFRA", "Siete de cada diez veces sube."),
    ("CIFRA", "La probabilidad de subida es de dos tercios."), ("CIFRA", "El oro sube un 3 % en el mes."),
    ("CIFRA", "Comprar US0378331005 ya."), ("CIFRA", "Comprar el bono del Tesoro con vencimiento en 2034."),
    ("CIFRA", "La idea es para el horizonte H3."), ("CIFRA", "La opción OPP-2026-0001 depende del dólar."),
    # R21: un código de un instrumento, con o sin verbo (QA r02, H-11 y H-12)
    ("R21", "Conviene comprar AAPL cuanto antes."), ("R21", "Recomendamos el ETF IBIT."), ("R21", "La opción preferida es NVDA."),
    ("R21", "Abrir una posición larga en TSLA."), ("R21", "Reducir el peso en INTC."), ("R21", "Comprar: NVDA, AMD y AVGO."),
    ("R21", "Comprar:\n- NVDA\n- AMD"), ("R21", "El fondo QQQ sigue al índice."), ("R21", "Invertir en XEON.DE para la liquidez."),
    ("R21", "Comprar BTC-USD ahora."), ("R21", "Sobreponderar Microsoft Corp frente al índice."),
    ("R21", "Telefónica S.A. mejora márgenes."), ("R21", "Conviene comprar la acción de Inditex."),
    # MARCADOR: desconocido o mal formado
    ("MARCADOR", "{opp:OPP-9999-9999} depende del dólar."), ("MARCADOR", "Vemos {total} ideas."), ("MARCADOR", "Vemos {n_ideas ideas."),
]


def _cfg(**extra):
    return config_pruebas(**fusionar({"diseno": "v6", "perfiles": {"activos": ["DIV"]}, "seleccion": {"umbral_senal_gc1": 0.55}}, extra))


def _bloque(tmp, cli=None):
    return Bloque(_cfg(), ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), cli or MockClient(), Path(tmp) / "estado", Path(tmp) / "ent")


@pytest.fixture(scope="module")
def perm(tmp_path_factory):
    return v6.permitidos_r21(_bloque(tmp_path_factory.mktemp("perm")))


MARCAS = {"opp:OPP-2026-0001": "la renta variable de calidad", "tipo:RV": "renta variable", "n:RV": "2", "candidatas:RV": "9",
          "n_ideas": "5", "n_tipos": "3", "n_apuestas": "4"}


@pytest.mark.parametrize("frase", LEGITIMAS)
def test_una_frase_legitima_no_se_quita(perm, frase):
    assert v6.texto_prohibido(frase, perm, MARCAS) is None


@pytest.mark.parametrize(("regla", "frase"), PROHIBIDAS)
def test_una_frase_prohibida_se_quita_con_su_regla(perm, regla, frase):
    assert v6.texto_prohibido(frase, perm, MARCAS) == regla


def test_los_marcadores_se_rellenan_despues_de_filtrar(perm):
    """Las cifras que pone el código no se filtran; las del Sintetizador, sí."""
    t = "Esta semana vemos {n_ideas} ideas. Hay un 70 % de probabilidad de subida. {opp:OPP-2026-0001} depende del dólar."
    limpio, reglas = v6.limpiar(t, perm, MARCAS)
    assert reglas == ["CIFRA"] and limpio == "Esta semana vemos 5 ideas. la renta variable de calidad depende del dólar."


def test_sin_marcas_basta_con_que_esten_bien_formados(perm):
    assert v6.texto_prohibido("{opp:OPP-1234-5678} depende del dólar.", perm) is None
    assert v6.texto_prohibido("{opp:OPP-1234-5678} depende del dólar.", perm, MARCAS) == "MARCADOR"


def test_una_lista_con_saltos_de_linea_no_esconde_la_compra(perm):
    """QA r02, H-11: cada línea es una frase y se juzga sola; un código suelto basta."""
    assert v6.limpiar("Comprar:\n- NVDA\n- AMD\nEl dólar sube.", perm, MARCAS) == ("Comprar:\nEl dólar sube.", ["R21", "R21"])


def test_sin_codigos_permitidos_un_par_es_sospechoso():
    """Los códigos permitidos vienen de la configuración y del universo: sin ellos, el filtro es estricto (falla cerrado)."""
    assert v6.texto_prohibido("Conviene vender EURUSD.", {"codigos": frozenset(), "series": frozenset()}) == "R21"


@pytest.mark.parametrize(("texto", "esperado"), [
    ("Comprar acciones de Banco Santander S.A. ya. El dólar cae.", "El dólar cae."),
    ("La renta variable de EE. UU. sube. Conviene comprar AAPL. El dólar cae frente al EUR.",
     "La renta variable de EE. UU. sube. El dólar cae frente al EUR."),
    ("El dólar sube frente al euro… Conviene comprar AAPL.", "El dólar sube frente al euro…"),
])
def test_se_divide_sin_partir_abreviaturas(perm, texto, esperado):
    assert v6.limpiar(texto, perm, MARCAS)[0] == esperado


def test_un_texto_limpio_sale_igual(perm):
    t = "  El dólar sube.\n\nEl euro baja.  La RV de EE. UU. cae.\n"
    assert v6.limpiar(t, perm, MARCAS) == (t, [])


def test_textos_largos_en_tiempo_lineal(perm):
    casos = ["Apple Microsoft Alphabet Amazon " * 2000, "acciones de " * 2500, "Comprar oro, " * 2500, "{n_ideas} " * 5000]
    t0 = time.perf_counter()
    for t in casos:
        v6.texto_prohibido(t, perm, MARCAS)
    assert time.perf_counter() - t0 < 2


def test_una_tarjeta_mala_no_tira_las_demas(tmp_path, monkeypatch):
    """Una tarjeta con una frase prohibida toma su texto por defecto; las demás y las frases de 30 s se conservan."""
    orig = mr._sintetizador
    capt = {}

    def sintetizador(msg, ctx, rng):
        out = orig(msg, ctx, rng)
        out["tarjetas"][0]["por_que_llano"] = "Conviene comprar AAPL cuanto antes."
        out["frases_30s"][2] = "Cada idea puede salir mal. Hay un 70 % de probabilidad de subida."
        capt["buenas"] = [t["por_que_llano"] for t in out["tarjetas"][1:]]
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
    assert red["frases_30s"][2] == "Cada idea puede salir mal."
    assert not v6._MARCADOR.search(json.dumps(red, ensure_ascii=False))   # los marcadores del simulador quedan rellenados
    assert any("Frases llanas del Sintetizador quitadas" in x for x in res["paquete"]["limitaciones"])
    assert res["g3_entregables"]["dictamen"] != "BLOQUEADO"


def test_cada_campo_por_el_camino_real(tmp_path, monkeypatch):
    """Una frase legítima con un marcador y una prohibida en cada texto del Sintetizador: sale la legítima rellenada, lo que se
    queda vacío toma su defecto y todo se declara."""
    orig = mr._sintetizador
    MALA = "Conviene comprar AAPL cuanto antes."
    capt: dict = {}

    def sintetizador(msg, ctx, rng):
        out = orig(msg, ctx, rng)
        opp = next(o["opp_id"] for c in msg["paquete_sintesis"]["clases"].values() for o in c["opciones"])
        capt["opp"] = opp
        out["regimen_macro"] = "Marca régimen en {n_tipos} tipos. Hay un 70 % de probabilidad de subida."
        for f in out["factores_dominantes"]:
            f["factor"] = "Marca factor del clúster. Comprar US0378331005 ya."
        out["preguntas_sugeridas"] = ["¿Marca pregunta sobre el carry? La venta de TSLA es urgente."]
        out["lectura_conjunto"] = f"Marca lectura: {{opp:{opp}}} depende del dólar; " + MALA
        out["limitaciones"] = ["Marca limitación de datos sintéticos. " + MALA]
        out["frases_30s"][0] = "Marca treinta con {n_ideas} ideas. " + MALA
        out["frases_30s"][1] = "Hay un 70 % de probabilidad de subida."
        for t in out["tarjetas"]:
            t["por_que_llano"] = "Marca por qué. " + MALA
            t["que_puede_salir_mal_llano"] = "Marca riesgo. Vender MSFT."
            t["ambito_llano"] = "Marca ámbito. {opp:OPP-9999-9999} es otra."
        out["motivos_llanos"] = {"DIV": "Marca motivo con {candidatas:DIV} ideas. " + MALA}
        out["glosario"] = [{"termino": "Carry", "definicion": "Marca glosario."}, {"termino": "ETF", "definicion": "Comprar QQQ es un ejemplo."}]
        out["frase_historial"] = "Marca historial. Acertamos el 58 % de las veces."
        return out
    monkeypatch.setattr(mr, "_sintetizador", sintetizador)
    b = _bloque(tmp_path)
    orig_gen = b.redaccion.generar

    def generar(bloque, paquete, extras, r, *a, **k):
        capt["red"], capt["defecto"], capt["marcas"] = copy.deepcopy(r), bloque.redaccion.textos_por_defecto(paquete), v6.marcadores(paquete)
        return orig_gen(bloque, paquete, extras, r, *a, **k)
    b.redaccion.generar = generar
    res = b.ciclo(AS_OF)
    p, red, m = res["paquete"], capt["red"], capt["marcas"]
    todo = json.dumps([p, red], ensure_ascii=False)
    for x in ("AAPL", "US0378331005", "TSLA", "MSFT", "QQQ", "70 %", "58 %", "{opp:", "{n_", "{candidatas:"):
        assert x not in todo, x
    assert p["regimen_macro"] == f"Marca régimen en {m['n_tipos']} tipos."
    assert p["clusteres_exposicion"] and all(c["factor_dominante"] == "Marca factor del clúster." for c in p["clusteres_exposicion"])
    assert p["preguntas_sugeridas"] == ["¿Marca pregunta sobre el carry?"]
    assert p["x_lectura_conjunto"] == f"Marca lectura: {m['opp:' + capt['opp']]} depende del dólar;"
    assert "Sintetizador: Marca limitación de datos sintéticos." in p["limitaciones"]
    assert red["frases_30s"][0] == f"Marca treinta con {m['n_ideas']} ideas." and red["frases_30s"][1] == capt["defecto"]["frases_30s"][1]
    assert red["tarjetas"] and all(t["por_que_llano"] == "Marca por qué." and t["que_puede_salir_mal_llano"] == "Marca riesgo."
                                   and t["ambito_llano"] == "Marca ámbito." for t in red["tarjetas"])
    assert red["motivos_llanos"] == {"DIV": f"Marca motivo con {m['candidatas:DIV']} ideas."}
    assert [g["termino"] for g in red["glosario"]] == ["Carry"]
    assert red["frase_historial"] == "Marca historial."
    n_tarj = len(red["tarjetas"])
    llanas = [x for x in p["limitaciones"] if x.startswith("Frases llanas del Sintetizador quitadas")]
    assert llanas == [f"Frases llanas del Sintetizador quitadas (CIFRA, MARCADOR, R21): {2 + 3 * n_tarj + 3}; el resto de sus textos se conserva"]
    integ = next(x for x in p["limitaciones"] if x.startswith("Frases del Sintetizador quitadas"))
    for campo in ("regimen_macro (CIFRA)", "factores_dominantes (CIFRA)", "preguntas_sugeridas (R21)", "lectura_conjunto (R21)", "limitaciones (R21)"):
        assert campo in integ


def test_la_reescritura_declara_solo_lo_que_se_entrega(tmp_path, monkeypatch):
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
