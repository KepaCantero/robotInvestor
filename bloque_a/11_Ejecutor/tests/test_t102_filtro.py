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
    "{opp:OPP-2026-0001} depende sobre todo del dólar.",
    "Pocas ideas de {tipo:RV} pasaron los filtros esta semana.",   # r06: sin marcadores de cuenta
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
    t = "La semana pinta tranquila en {tipo:RV}. Hay un 70 % de probabilidad de subida. {opp:OPP-2026-0001} depende del dólar."
    limpio, reglas = v6.limpiar(t, perm, MARCAS)
    assert reglas == ["CIFRA"] and limpio == "La semana pinta tranquila en renta variable. la renta variable de calidad depende del dólar."


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
    ("El dólar sube frente al euro… Conviene comprar AAPL.", "El dólar sube frente al euro..."),   # con marcas, NFKC: «…» es «...»
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
        out["frases_30s"][1] = "Cada idea puede salir mal. Hay un 70 % de probabilidad de subida."   # r06: dos frases
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
        out["regimen_macro"] = "Marca régimen en {tipo:DIV}. Hay un 70 % de probabilidad de subida."
        for f in out["factores_dominantes"]:
            f["factor"] = "Marca factor del clúster. Comprar US0378331005 ya."
        out["preguntas_sugeridas"] = ["¿Marca pregunta sobre el carry? La venta de TSLA es urgente."]
        out["lectura_conjunto"] = f"Marca lectura: {{opp:{opp}}} depende del dólar; " + MALA
        out["limitaciones"] = ["Marca limitación de datos sintéticos. " + MALA]
        out["frases_30s"][0] = "Marca resumen de la semana. " + MALA
        out["frases_30s"][1] = "Hay un 70 % de probabilidad de subida."
        for t in out["tarjetas"]:
            t["por_que_llano"] = "Marca por qué. " + MALA
            t["que_puede_salir_mal_llano"] = "Marca riesgo. Vender MSFT."
            t["ambito_llano"] = "Marca ámbito. {opp:OPP-9999-9999} es otra."
        out["motivos_llanos"] = {"DIV": "Marca motivo de {tipo:DIV}. " + MALA}
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
    # r04 (QA r03, H-29) y r06: los valores, calculados aparte a partir del paquete (no con `v6.marcadores`)
    ops = [o for d in p["clases"].values() for o in d["opciones"]]
    n_tipos = sum(1 for d in p["clases"].values() if d["opciones"])
    assert m["opp:" + capt["opp"]] == next(o["nombre_llano"] for o in ops if o["opp_id"] == capt["opp"])
    assert m["tipo:DIV"] == v6.NOMBRE_CLASE["DIV"].lower() and not any(k.startswith(("n:", "candidatas:", "n_")) for k in m)
    todo = json.dumps([p, red], ensure_ascii=False)
    for x in ("AAPL", "US0378331005", "TSLA", "MSFT", "QQQ", "70 %", "58 %", "{opp:", "{n_", "{candidatas:"):
        assert x not in todo, x
    assert p["regimen_macro"] == f"Marca régimen en {m['tipo:DIV']}."
    assert p["clusteres_exposicion"] and all(c["factor_dominante"] == "Marca factor del clúster." for c in p["clusteres_exposicion"])
    assert p["preguntas_sugeridas"] == ["¿Marca pregunta sobre el carry?"]
    assert p["x_lectura_conjunto"] == f"Marca lectura: {m['opp:' + capt['opp']]} depende del dólar;"
    assert "Sintetizador: Marca limitación de datos sintéticos." in p["limitaciones"]
    # r06: la primera frase (las cuentas) la escribe el código; la del Sintetizador va después
    ideas, tipos = ("idea" if len(ops) == 1 else "ideas"), ("tipo" if n_tipos == 1 else "tipos")   # T-113 (H-49): singular
    assert red["frases_30s"] == [f"Esta semana vemos {len(ops)} {ideas} en {n_tipos} {tipos} de inversión.", "Marca resumen de la semana.",
                                 capt["defecto"]["frases_30s"][2]]
    assert red["tarjetas"] and all(t["por_que_llano"] == "Marca por qué." and t["que_puede_salir_mal_llano"] == "Marca riesgo."
                                   and t["ambito_llano"] == "Marca ámbito." for t in red["tarjetas"])
    div = p["clases"]["DIV"]
    n_div = len(div["opciones"])
    cuenta = (f"De {div['candidatas_analizadas']} ideas de {v6.NOMBRE_CLASE['DIV'].lower()} analizadas, {n_div} "
              f"{'pasó' if n_div == 1 else 'pasaron'} todos los filtros.")
    assert red["motivos_llanos"] == {"DIV": f"{cuenta} Marca motivo de {m['tipo:DIV']}."}
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


# ================================================================================================== ronda r04 (QA r03 de T-102)
PROHIBIDAS_R04 = [
    # H-20: probabilidades en letra o con números Unicode
    ("CIFRA", "Vemos un setenta por cien de probabilidad de subida."), ("CIFRA", "La probabilidad de subida es de tres entre cuatro."),
    ("CIFRA", "Con una confianza de dos tercios, el BCE recortará."), ("CIFRA", "La probabilidad de subida es de ⅔."),
    ("CIFRA", "Vemos un ⁷⁰ % de subida."), ("CIFRA", "Lo vemos en Ⅶ sobre Ⅹ."), ("CIFRA", "Novecientos de cada mil escenarios acaban en subida."),
    ("CIFRA", "El escenario base pesa la mitad, el alcista un cuarto y el bajista otro cuarto."),
    # H-23: probabilidades compuestas con marcadores
    ("MARCADOR", "La probabilidad de subida es del {n:RV}{n:RV} %."), ("MARCADOR", "Lo vemos en {n:RV} sobre {candidatas:RV}."),
    ("MARCADOR", "La probabilidad de subida es alta en {n_ideas} ideas."),
    # H-21: sufijo con punto o tras coma; un índice seguido del código de un fondo; nombres de fondo
    ("R21", "Recomendamos Apple Inc."), ("R21", "Comprar Microsoft Corp. cuanto antes."), ("R21", "La opción preferida es Tesla, Inc."),
    ("R21", "Comprar Apple inc ya."), ("R21", "Recomendamos el ETF MSCI World IWDA."), ("R21", "Comprar el S&P SPY ya."),
    ("R21", "Recomendamos el Vanguard Global Stock Index Fund."), ("R21", "Recomendamos el Amundi MSCI World UCITS ETF."),
    # H-22: minúsculas tras un vehículo, homoglifos, códigos pegados, una letra tras un vehículo, «$», mezcla de mayúsculas
    ("R21", "Recomendamos el ETF qqq."), ("R21", "Recomendamos el fondo qqq."), ("R21", "Comprar ΝVDΑ ya."), ("R21", "Recomendamos el fondo ЅРY."),
    ("R21", "Comprar renta variable-NVDA."), ("R21", "Comprar acciones.NVDA ya."), ("R21", "Vender el REIT O antes de la subida."),
    ("R21", "Comprar $tsla ya."), ("R21", "Comprar AApl ya."), ("R21", "Comprar AA ya."),
    ("MARCADOR", "Vemos ❴total❵ tipos."),
]
LEGITIMAS_R04 = [
    "Las SICAV pierden atractivo fiscal.", "Las opciones de venta encarecen cuando el mercado tiene miedo.",
    "El crédito AA aguanta mejor que el BBB.", "Los ETFs de renta fija captan flujos.", "Es una tesis para todo el siglo XXI.",
    "La OTAN eleva el gasto en defensa.", "Invertir en el MSCI ACWI es la forma más sencilla de diversificar.",
    "El escenario base supone un dólar más débil.", "Es probable que el BCE recorte este verano.",
]


@pytest.mark.parametrize(("regla", "frase"), PROHIBIDAS_R04)
def test_r04_lo_que_pasaba_en_la_qa_r03_se_quita(perm, regla, frase):
    assert v6.texto_prohibido(frase, perm, MARCAS) == regla


@pytest.mark.parametrize("frase", LEGITIMAS_R04)
def test_r04_frases_legitimas(perm, frase):
    assert v6.texto_prohibido(frase, perm, MARCAS) is None


def test_r04_llaves_de_ancho_completo_son_marcadores(perm):
    """H-28: NFKC convierte «｛tipo:RV｝» en «{tipo:RV}», que se rellena; «｛n_ideas｝», de cuenta, se quita (r06)."""
    assert v6.limpiar("Vemos ｛tipo:RV｝ hoy.", perm, MARCAS) == ("Vemos renta variable hoy.", [])
    assert v6.limpiar("Vemos ｛n_ideas｝ ideas.", perm, MARCAS)[1] == ["MARCADOR"]


def test_r04_un_nombre_llano_con_ticker_no_se_rellena(perm):
    """H-27: el `nombre_llano` lo escribe un Analista; si incumple la regla, el marcador pone «esta idea»."""
    paquete = {"clases": {"RV": {"opciones": [{"opp_id": "OPP-2026-0001", "nombre_llano": "Comprar AAPL"}], "candidatas_analizadas": 3}}}
    assert v6.marcadores(paquete, perm)["opp:OPP-2026-0001"] == "esta idea"


def test_r04_un_glosario_que_no_es_texto_no_rompe_el_ciclo(tmp_path, monkeypatch):
    """H-24: una definición que no es texto se quita y se declara (antes, el ciclo entero caía)."""
    orig = mr._sintetizador

    def sintetizador(msg, ctx, rng):
        out = orig(msg, ctx, rng)
        out["glosario"] = [{"termino": "Carry", "definicion": {"x": 1}}, {"termino": "Riesgo", "definicion": "Lo que puedes perder."}]
        return out
    monkeypatch.setattr(mr, "_sintetizador", sintetizador)
    res = _bloque(tmp_path).ciclo(AS_OF)
    assert any("FORMATO" in x for x in res["paquete"]["limitaciones"])


def test_r04_muchos_espacios_en_tiempo_lineal(perm):
    """H-26: 50.000 espacios o tabuladores seguidos (antes, 11 s)."""
    t0 = time.perf_counter()
    for t in (" " * 50_000 + "x", "\t" * 50_000 + "x", "a." + " " * 50_000 + "b"):
        v6.limpiar(t, perm, MARCAS)
    assert time.perf_counter() - t0 < 2


def test_r04_el_sintetizador_recibe_la_lista_de_siglas(tmp_path):
    """H-25: la instrucción lleva las siglas que puede usar."""
    b = _bloque(tmp_path)
    vistas = []
    orig = b._invocar

    def invocar(agente, contrato, mensaje, esquema, instrucciones, *a, **k):
        if agente == "AG-26":
            vistas.append(instrucciones)
        return orig(agente, contrato, mensaje, esquema, instrucciones, *a, **k)
    b._invocar = invocar
    b.ciclo(AS_OF)
    assert vistas and all("Siglas que puedes usar:" in x and " OTAN" in x for x in vistas)


# ================================================================================================== ronda r05 (QA r04 de T-102)
R05_PROHIBIDAS = [
    # H-31: probabilidades en letra que pasaban
    ("CIFRA", "Sube una de cada tres veces."), ("CIFRA", "Ocurre siete veces de cada diez."),
    ("CIFRA", "Hay una cuarta parte de probabilidad de caída."), ("CIFRA", "Las cuotas están tres contra uno."),
    ("CIFRA", "El reparto es sesenta-cuarenta."), ("CIFRA", "- base: la mitad"), ("CIFRA", "- alcista: un cuarto"),
    ("CIFRA", "Hay un cuarto de probabilidad de caída."), ("CIFRA", "Sube una décima al mes."),   # N05
    ("CIFRA", "Hay mil razones para comprar."), ("CIFRA", "Hay la mitad de probabilidad de caída."),   # N06
    ("CIFRA", "Sube punto y medio."), ("CIFRA", "La mitad de las ideas dependen del dólar."),
    ("CIFRA", "Sube mucho, un ‰ al día."), ("CIFRA", "Cae en %."),   # N07
    ("CIFRA", "Puede subir un por ciento."), ("CIFRA", "Puede subir un por cien."),   # N09
    ("MARCADOR", "Hay {n:RV} chances de subida."), ("MARCADOR", "Hay {n:RV} opciones de que suba."),   # r06: cuenta
    ("MARCADOR", "Sube {n:RV} veces de cada {n_ideas}."), ("MARCADOR", "Las cuotas están {n:RV} contra uno."),
    ("MARCADOR", "Sube una de cada {n_ideas} veces."), ("MARCADOR", "Entre {n:RV} a {n_ideas} ideas."),
    # H-32: sufijos de sociedad
    ("R21", "Enel SpA gana cuota."), ("R21", "Compre Enel S.p.A. ya."), ("R21", "Toyota Motor Co. sube."),
    ("R21", "Rio Tinto Limited cae."), ("R21", "Conviene apple inc. a corto."), ("R21", "Siemens Aktiengesellschaft cae."),
    ("R21", "Recomendamos el Amundi Prime Global ETF."),   # N15
    # H-33: un código partido por caracteres invisibles
    ("R21", "Compre N\u200bV\u200bD\u200bA ya."), ("R21", "Compre NVD­A ya."), ("R21", "Compre NV⁠DA ya."),
    ("R21", "Compre N̈VDA ya."),
    ("R21", "La ψ del mercado sube."),   # N20: letras griegas
    ("R21", "Comprar NV ya."),   # N39: códigos de dos letras
    ("R21", "Conviene comprar solo la acción ordinaria."),   # Q11: `_UNITARIA`
    ("R21", "Comprar Unilever plc."),   # un nombre que acaba como un infinitivo no es un verbo si no abre la frase
    ("R21", "Comprar ᏚᏢᎩ cuanto antes."), ("R21", "Comprar ɴᴠᴅᴀ ya."), ("R21", "Comprar 🇳🇻🇩🇦 ya."),   # otros alfabetos
    ("MARCADOR", "La subida es del {n:RV} ٪."), ("CIFRA", "Es el doble de probable que suba."), ("CIFRA", "Sube un ٪."),
    ("MARCADOR", "Vemos 〔n_ideas〕 ideas."), ("MARCADOR", "Vemos [n:RV] ideas."),
]
R05_LEGITIMAS = [
    # H-35: «medio», «mitad» y ordinales que no son cantidades
    "A medio plazo es probable que suba.", "En la segunda mitad del año es probable una pausa.",
    "Oriente Medio añade riesgo al escenario base.", "Con certeza, a medio plazo el dólar pesa.",
    "El cuarto trimestre será probablemente el más débil.", "A mitad de año revisaremos el escenario.",
    "Uno de los riesgos es la inflación.",
    # H-36: palabras comunes y nombres de región tras un vehículo o delante de «ETF»
    "Las acciones de Europa suben con el euro.", "Las opciones sobre Europa encarecen la cobertura.",
    "El fondo Europa del Este cae.", "Cada ETF replica un índice.", "Sobreponderar ETF de RF tiene sentido.",
    "Todos los ETF de RV suben.",
    "Los ETF baratos ganan cuota.",   # N42
    "El EURUSD cae.",   # N38
]


@pytest.mark.parametrize("regla,frase", R05_PROHIBIDAS)
def test_r05_lo_que_pasaba_en_la_qa_r04_se_quita(perm, regla, frase):
    assert v6.frase_prohibida(frase, perm) == regla, frase


@pytest.mark.parametrize("frase", R05_LEGITIMAS)
def test_r05_frases_legitimas(perm, frase):
    assert v6.frase_prohibida(frase, perm) is None, frase


def test_r05_n37_una_serie_del_universo_no_es_un_instrumento():
    perm = {"codigos": frozenset(), "series": frozenset({"VIXCLS"})}
    assert v6.frase_prohibida("El VIXCLS sube.", perm) is None
    assert v6.frase_prohibida("El VIXCLS sube.", {"codigos": frozenset(), "series": frozenset()}) == "R21"


def test_r05_h31_una_lista_de_probabilidades_en_letra_no_llega(perm):
    t = "Probabilidades por escenario:\n- base: la mitad\n- alcista: un cuarto\n- bajista: el resto"
    limpio, reglas = v6.limpiar(t, perm, MARCAS)
    assert reglas.count("CIFRA") == 2 and "mitad" not in limpio and "cuarto" not in limpio


def test_r05_h37_sufijo_en_tiempo_lineal(perm):
    t0 = time.perf_counter()
    for n in (20000, 40000):
        v6.frase_prohibida("A." * n, perm)
        v6.frase_prohibida("Abc " * n + "Inc", perm)
    assert time.perf_counter() - t0 < 2.0


def test_r05_h39_las_siglas_con_cifras_no_se_ofrecen(tmp_path):
    b = _bloque(tmp_path)
    vistas = []
    orig = b._invocar

    def invocar(agente, contrato, mensaje, esquema, instrucciones, *a, **k):
        if agente == "AG-26":
            vistas.append(instrucciones)
        return orig(agente, contrato, mensaje, esquema, instrucciones, *a, **k)
    b._invocar = invocar
    b.ciclo(AS_OF)
    assert vistas and not any(s_ in x for x in vistas for s_ in ("G7", "G10", "G20"))


class _Redaccion:
    def textos_por_defecto(self, paquete):
        return {"frases_30s": ["frase por defecto", "segunda por defecto", "tercera por defecto"], "tarjetas": [], "motivos_llanos": {}, "glosario": [],
                "frase_historial": "historial por defecto"}


def test_r05_marcadores_glosario_e_historial_frente_al_paquete():
    """N36, Q29 y Q36 (r05) y las cuentas que escribe el código (r06), comparadas con el paquete."""
    from types import SimpleNamespace
    paquete = {"clases": {"RV": {"opciones": [{"opp_id": "OPP-1", "nombre_llano": "la renta variable"}], "candidatas_analizadas": 9},
                          "RF": {"opciones": [], "candidatas_analizadas": 3}},
               "apuestas_independientes": 7, "limitaciones": []}
    d = {"frases_30s": ["Una frase del Sintetizador.", "Hay ideas en {n_tipos} tipos."], "tarjetas": [],
         "motivos_llanos": {"RF": "Preferimos no rellenar el hueco.", "RV": "Solo {n:RV} pasaron."},
         "glosario": [{"termino": "{tipo:RV}", "definicion": "Activos de empresas cotizadas."},
                      {"termino": "Compre AAPL", "definicion": "Una definición."}],
         "frase_historial": "Compre AAPL ya."}
    perm = {"codigos": frozenset(), "series": frozenset()}
    red = v6._redaccion_segura(SimpleNamespace(redaccion=_Redaccion()), paquete, d, perm)
    assert red["frases_30s"] == ["frase por defecto", "Una frase del Sintetizador.", "tercera por defecto"]   # la de cuenta, a su defecto
    assert red["motivos_llanos"] == {"RF": f"De 3 ideas de {v6.NOMBRE_CLASE['RF'].lower()} analizadas, 0 pasaron todos los filtros. "
                                           "Preferimos no rellenar el hueco."}
    assert red["glosario"] == [{"termino": v6.NOMBRE_CLASE["RV"].lower(), "definicion": "Activos de empresas cotizadas."}]
    assert red["frase_historial"] == "historial por defecto"
    assert v6._cuenta_motivo(paquete, "RV") == f"De 9 ideas de {v6.NOMBRE_CLASE['RV'].lower()} analizadas, 1 pasó todos los filtros."


@pytest.mark.parametrize("frase", ["El escenario base pesa {n:RV}.", "La confianza llega a {n:RV}.", "Hay {n:RV} de seguridad.",
                                   "Con certeza en {n:RV} casos."])
def test_r05_n03_n04_palabra_de_probabilidad_con_un_marcador_numerico(perm, frase):
    assert v6.frase_prohibida(frase, perm) == "MARCADOR"   # r06: un marcador de cuenta ya no vale en el texto libre


def test_r05_n38_q18_un_par_de_divisas_sin_barra_no_es_un_instrumento():
    perm = {"codigos": frozenset({"EUR", "USD"}), "series": frozenset()}
    assert v6.frase_prohibida("El EURUSD cae.", perm) is None and v6.frase_prohibida("El EURXYZ cae.", perm) == "R21"


# ================================================================================================== ronda r06 (QA r05 de T-102)
R06_LEGITIMAS = [
    # H-40: giros con «medio», «mitad», «doble» y ordinales que no son cantidades
    "A corto y medio plazo, el dólar pesa.", "Es un medio de cobertura barato.", "El doble mandato de la Fed pesa.",
    "En mitad de la tormenta, el oro sube.", "Oriente Próximo y Medio añade riesgo.", "Es el quinto mes consecutivo de subidas.",
    "En la segunda mitad, el BCE para.", "Hacia la mitad del año el dólar cae.", "Hacia la mitad de sesión el dólar cae.",
    # H-41: frases corrientes con un vehículo o con «la acción de» / «el bono de»
    "Un ETF es un fondo que cotiza en bolsa.", "Los ETF suben con el mercado.", "El fondo va bien este año.",
    "La acción de los bancos centrales pesa.", "El bono de referencia sube.",
    "Ningún ETF replica todo el mercado.", "- Sobreponderar ETF de RF tiene sentido.", "Las acciones de Europa suben.",
    "La pingüinera crece con la ñ de España.",   # las marcas del español se conservan al limpiar
]
R06_PROHIBIDAS = [
    # H-42: dos marcadores de cuenta ya no componen nada: un marcador de cuenta en el texto libre se quita
    ("MARCADOR", "Sube {n:RV},{n:RF} este año."), ("MARCADOR", "base: {n:RV} de {n_ideas}"), ("MARCADOR", "{n:RV} a uno"),
    ("MARCADOR", "una por cada {n_ideas}"), ("MARCADOR", "{n:RV}x"), ("MARCADOR", "Probabilidad de subida:\n{n:TCV}.{n:RF}"),
    # H-43: cantidades en letra fuera de la lista anterior
    ("CIFRA", "Hay una milésima de diferencia."), ("CIFRA", "Es la centésima parte."), ("CIFRA", "Un onceavo del total."),
    ("CIFRA", "Hay una docena de ideas."), ("CIFRA", "Hay una decena de ideas."), ("CIFRA", "Un centenar de ideas."),
    ("CIFRA", "Un millar de bancos."), ("CIFRA", "Medio centenar de bancos."), ("CIFRA", "Es un fifty-fifty."),
    ("CIFRA", "Van uno a uno."), ("CIFRA", "Seventy percent de probabilidad."), ("CIFRA", "Sube una décima al mes."),
    # H-48: una frase por mutante vivo de la QA r05
    ("CIFRA", "Hay un millón de razones."), ("CIFRA", "Hay un tercio de ideas."), ("CIFRA", "Van uno contra uno."),
    ("CIFRA", "Es la tercera parte del total."), ("CIFRA", "Hay doscientas razones."), ("CIFRA", "Hay veintitrés ideas."),
    ("CIFRA", "Hay dieciséis ideas."), ("CIFRA", "La política de tipos cero quedó atrás."), ("CIFRA", "Sube medio punto."),
    ("CIFRA", "Sube un cuarto de punto."), ("CIFRA", "Es el doble de probable."),
    # H-44: sufijos de sociedad y de fondo, también al empezar la frase o la línea, y tickers con mayúscula inicial
    ("R21", "Pfizer Inc. sube."), ("R21", "Danaher Corp. cae."), ("R21", "- Schlumberger Ltd. sube."),
    ("R21", "Comprar el ETF Nvda."), ("R21", "Comprar el ETF Arkk."), ("R21", "Comprar el REIT Realty."),
    ("R21", "Comprar Unilever Plc."), ("R21", "Comprar Amundi Sicav."), ("R21", "Comprar Merlin Socimi."),
    ("R21", "Comprar Henkel KGaA."), ("R21", "Comprar Nokia Oyj."), ("R21", "Comprar Vale Ltda."), ("R21", "Comprar Maybank Bhd."),
    ("R21", "Comprar Sony Group."), ("R21", "Comprar Alibaba Holding."), ("R21", "Comprar tesla inc ya."),
    ("R21", "Comprar nvidia corporation."), ("R21", "Comprar Global Gold ETC."), ("R21", "Comprar el fondo vwrl."),
    ("R21", "Rio Tinto Spa sube."), ("R21", "Comprar el ETF Ab ya."), ("R21", "Comprar toyota co. ya."),
    # H-46: escrituras de mala fe
    ("R21", "Compre N̲V̲D̲A ya."), ("R21", "Compre ṄVDA ya."), ("R21", "Compre \U0001f17d\U0001f185\U0001f173\U0001f170 ya."),
    ("R21", "Compre N V D A ya."), ("R21", "Compre N_V_D_A ya."), ("R21", "Compre N⠀V⠀D⠀A ya."),
]


@pytest.mark.parametrize("frase", R06_LEGITIMAS)
def test_r06_frases_legitimas(perm, frase):
    assert v6.frase_prohibida(frase, perm) is None, frase


@pytest.mark.parametrize("regla,frase", R06_PROHIBIDAS)
def test_r06_lo_que_pasaba_en_la_qa_r05_se_quita(perm, regla, frase):
    assert v6.texto_prohibido(frase, perm, MARCAS) == regla, frase


def test_r06_el_sintetizador_escribe_dos_frases_de_30s():
    from bloque_a.contratos import ESQUEMAS
    f = ESQUEMAS["SINTESIS"]["properties"]["frases_30s"]
    # T-113 (H-50): de una a tres; `_redaccion_segura` toma las dos primeras o completa y lo declara
    assert (f["minItems"], f["maxItems"]) == (1, 3) and ESQUEMAS["REDACCION"]["properties"]["frases_30s"]["minItems"] == 3   # la V5 no cambia


def test_r06_h45_marcador_y_muchos_espacios_en_tiempo_lineal(perm):
    t0 = time.perf_counter()
    for n in (16000, 32000):
        v6.frase_prohibida("{tipo:RV}" + " " * n + "{tipo:RV}", perm)
    assert time.perf_counter() - t0 < 1.0


def test_r06_n39_q19_un_codigo_de_dos_letras_es_un_instrumento(perm):
    assert v6.frase_prohibida("Compra MU para el trimestre.", perm) == "R21"


def test_r06_q02_lo_que_rellena_el_codigo_no_se_filtra(perm):
    """El valor de un marcador sale del paquete y se pone después de filtrar: no se le aplica la regla."""
    assert v6.limpiar("Miramos {tipo:RV} hoy.", perm, {"tipo:RV": "renta de dos velocidades"}) == ("Miramos renta de dos velocidades hoy.", [])
