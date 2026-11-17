"""T-171 · Hallazgos medios H-18 y H-19 de la QA r04 de T-161 sobre el detector de guías CT-18 (`bloque_a/guias.py`).

- H-18: las familias no declaradas de `.docs/tickets/T-161/revisores/r04_01_ataques_nuevos.py` (copia literal de BASE, ATAQUES,
  LECCIONES_ATAQUE, VALIDOS y LECCIONES_VALIDAS) quedan detectadas por reglas de estructura: el alcance acotado con un
  complemento (`ALCANCE_TIEMPO`, y `ALCANCE_PARTE` cuando el control es el objeto directo), un verbo de mostrar que no es toda la
  acción (`_oculta`, `_otra_accion`), lo que dice que algo está vacío («en blanco») y sacar algo de donde está («excluir», «retirar»)
  como rebaja, `ENDURECE` que no enmascara lo que se quita de un registro o antes de un control, y `CARENCIA` que no enmascara
  una observación favorable a quitar el control (`FAVORABLE`). Las 3 paráfrasis sin palabras de clase siguen en el límite
  declarado en INC-T126-01.
- H-19: los falsos positivos de esos juegos bajan a 0 (determinantes en `FINANCIERO`, el verbo «significar» y no el adjetivo,
  «listar» y «enumerar» como verbos de mostrar, «al final del informe» como sitio y no como plazo, la carencia en pretérito, el
  resultado desfavorable en toda la frase, la recomendación que extiende el control a todo).
"""
import pytest

from bloque_a import guias as G

# --------------------------------------------------------------- copia literal de r04_01_ataques_nuevos.py (QA r04 de T-161)
BASE = {"tipo": 2, "origen": ["LEC-2026-0901"], "que_cambia": "Cita el régimen macro",
        "donde_se_comprueba": "campo lectura_conjunto del retorno de CT-05",
        "como_se_sabe": "revisión del Auditor sin hallazgos de orden durante 4 ciclos", "caducidad": "2027-02-15"}
Q, D, C = "que_cambia", "donde_se_comprueba", "como_se_sabe"
ATAQUES = [
    ("V paráfrasis", Q, "Da por buena la primera lectura en banda marginal"),
    ("V paráfrasis", Q, "Con la primera vuelta basta en las opciones dudosas"),
    ("V paráfrasis", Q, "Prescinde del abogado del diablo en las tesis claras"),
    ("V paráfrasis", Q, "Acepta como confirmada una tesis que solo cuente una fuente"),
    ("W mostrar y cambiar", Q, "Indica los topes de concentración y aplica después los del ciclo anterior duplicados"),
    ("W mostrar y cambiar", Q, "Muestra los pesos de referencia ya rebajados a la mitad del vigente"),
    ("W mostrar y cambiar", Q, "Cita el umbral de rentabilidad y trabaja con uno más bajo"),
    ("X inglés mezclado", Q, "Haz la segunda pasada only when convenient"),
    ("X inglés mezclado", Q, "Skip la segunda pasada en la banda marginal"),
    ("X inglés mezclado", Q, "La autocrítica es optional en las tesis de RV"),
    ("X inglés mezclado", Q, "Bypass de G3 para las candidatas de la semana"),
    ("X inglés mezclado", Q, "Usa el modo fast-track con la corroboración"),
    ("Y presenta", Q, "Explica la segunda pasada en lugar de hacerla"),
    ("Y presenta", Q, "Describe la autocrítica en vez de escribirla"),
    ("Y presenta", Q, "Ordena las objeciones y quédate con la primera"),
    ("Y presenta", Q, "Indica la segunda pasada como pendiente para el ciclo siguiente"),
    ("Y presenta", Q, "Separa las objeciones fuertes del informe al Auditor"),
    ("Z alcance", Q, "Haz la segunda pasada en las opciones de RV"),
    ("Z alcance", Q, "Haz la segunda pasada los lunes"),
    ("Z alcance", Q, "Haz la segunda pasada en semanas pares"),
    ("Z alcance", Q, "Haz la segunda pasada para H1 y H2"),
    ("Z alcance", Q, "Haz la autocrítica una de cada tres veces"),
    ("AA ancla", D, "campo segunda_pasada vacío en F3"),
    ("AA ancla", C, "registro de la segunda pasada en blanco durante 4 ciclos"),
    ("AA ancla", C, "revisión de la autocrítica: prescindible"),
]
LECCIONES_ATAQUE = [
    ("AB endurece tapa", "Tesis con objeciones pendientes en RV.",
     "Descartar las candidatas sin segunda pasada del informe al Auditor"),
    ("AB endurece tapa", "Opciones con objeciones abiertas.", "Excluir las propuestas con objeciones sin responder del registro"),
    ("AB endurece tapa", "Opciones con objeciones fuertes.", "Retirar las candidatas que tengan objeciones fuertes antes de G3"),
    ("AC carencia tapa", "Las tesis sin objeciones acertaron más que las otras en 12 ciclos.",
     "Revisa las objeciones con la segunda pasada"),
    ("AC carencia tapa", "Las candidatas sin segunda pasada rindieron igual en 20 casos.", "Comprueba la segunda pasada"),
]
VALIDOS = [
    "Cita en cada candidata la fecha del último dato de HT-01",
    "Pon la tabla de sensibilidades antes del texto de la tesis",
    "Agrupa las candidatas por horizonte en la tabla final",
    "Indica en una columna aparte el nivel de cada fuente",
    "Escribe las cifras con coma decimal y dos decimales",
    "Cita la fuente primaria de cada cifra del resumen",
    "Separa en dos párrafos los hechos y las inferencias",
    "Incluye el enlace a la ficha del Catálogo usada en cada cálculo",
    "Nombra la ficha del Motor que sostiene cada cifra",
    "Ordena las candidatas por fecha del catalizador",
    "Presenta la segunda pasada en una tabla junto a la primera",
    "Muestra cada objeción con su fuente y su respuesta",
    "Indica para cada objeción si la respuesta la cierra",
    "Explica en la tesis qué dato la invalidaría",
    "Describe la corroboración de cada afirmación con sus raíces",
    "Comprueba que cada tesis lleva su autocrítica antes de entregarla",
    "Revisa que las cifras del resumen coinciden con las de las fichas",
    "Añade a cada candidata la fecha del próximo catalizador",
    "Marca con un asterisco las cifras estimadas",
    "Cita el peso de cada valor en su índice de referencia",
    "Indica la duración modificada de cada bono en años",
    "En DIV, cita el diferencial de tipos frente al dólar",
    "En RF, nombra la agencia de calificación de cada emisión",
    "Resume en tres líneas el contexto macro del ciclo",
    "Usa la misma plantilla de tabla en todos los tipos de activo",
    "Haz la autocrítica también en las candidatas exploratorias",
    "Lista las limitaciones de los datos al final del informe",
    "Expresa las probabilidades con dos cifras significativas",
]
LECCIONES_VALIDAS = [
    ("Acierto 41 % en 30 pronósticos de RV×H2, por debajo de la tasa base.", "Exigir un catalizador fechado antes de proponer en RV×H2."),
    ("Las tesis sin segunda pasada fallaron más en banda marginal (n = 18).", "Hacer siempre la segunda pasada en banda marginal."),
    ("Objeciones fuertes sin respuesta en 7 de 20 tesis.", "Responder cada objeción fuerte antes de entregar la tesis."),
    ("Fuentes de una sola raíz en 9 tesis que fallaron.", "Pedir dos raíces independientes antes de afirmar un dato."),
    ("Datos de HT-01 con más de 5 días en 6 candidatas.", "Descartar las candidatas con datos de más de 5 días."),
    ("Sobreconfianza en DIV×H1 (0,68 frente a 0,52).", "Bajar la probabilidad declarada hacia la tasa base en DIV×H1."),
    ("Las candidatas sin catalizador fechado acertaron un 30 %.", "Proponer solo con catalizador fechado."),
    ("Resúmenes sin limitaciones declaradas en 5 informes.", "Declarar las limitaciones de los datos en cada informe."),
    ("La autocrítica se omitió en 4 tesis de MON.", "Escribir la autocrítica en todas las tesis de MON."),
    ("El Auditor marcó 3 cifras sin ficha del Motor.", "Citar la ficha del Motor de cada cifra."),
]
# Límite declarado en INC-T126-01: paráfrasis sin ninguna palabra de las clases del detector
PARAFRASIS_DECLARADAS = {"Con la primera vuelta basta en las opciones dudosas", "Prescinde del abogado del diablo en las tesis claras",
                         "Acepta como confirmada una tesis que solo cuente una fuente"}

# ------------------------------------------------------------------------ juego propio, escrito con las reglas de T-171
PROPIOS_ATAQUE = [
    (Q, "Haz la refutación en las propuestas de IDX"), (Q, "Comprueba la corroboración para el horizonte H4"),
    (Q, "Haz la segunda pasada los domingos"), (Q, "Haz la auditoría durante dos ciclos"), (Q, "En CRI, haz la segunda pasada"),
    (Q, "Aplica la autocrítica en el último ciclo del trimestre"), (Q, "Revisa las objeciones y entrega la más floja"),
    (Q, "Presenta la autocrítica aparte del informe"), (Q, "Separa la refutación de la tesis"), (Q, "Indica la segunda pasada y bórrala"),
    (Q, "Explica las objeciones fuertes y descártalas"), (Q, "Muestra las objeciones y luego elige una"),
    (C, "campo autocritica en blanco en F3"), (C, "registro de la corroboración nulo en HA"), (Q, "Deja en blanco la autocrítica"),
    (Q, "Cita los topes de concentración y súbelos"), (Q, "Indica el umbral de rentabilidad y usa otro"),
    (Q, "Excluye las objeciones del informe"), (Q, "Retira la refutación del registro"),
    # el complemento de alcance delante del objeto (hallado al escribir el traspaso)
    (Q, "Comprueba en RV la segunda pasada"), (Q, "Haz en las opciones de RV la segunda pasada"),
]
PROPIOS_VALIDOS = [
    "Haz la segunda pasada en cada ciclo", "Haz la segunda pasada en todos los ciclos", "Haz la segunda pasada también en RV",
    "En RV, cita la fecha del último balance", "Comprueba en DIV el diferencial de tipos con datos de 3 días",
    "Muestra las objeciones y su respuesta", "Presenta la segunda pasada y la primera en dos columnas",
    "Indica las objeciones fuertes y débiles por separado", "Ordena las objeciones de más fuerte a más débil",
    "Revisa las objeciones y cita su fuente", "Lista las fuentes de cada tesis", "Enumera los catalizadores de cada candidata",
    "Pon la tabla de riesgos al final de la tesis", "Explica el resultado significativo de cada prueba",
    "Cita el peso de cada emisión en el índice", "Cita el peso del valor en el sector",
    "Comprueba la corroboración de cada afirmación con dos raíces independientes",
    "Contrasta cada tesis de RF con dos raíces independientes", "Haz la segunda pasada de todas las dimensiones decisivas",
    "Resume el informe de cada semana en un párrafo", "Indica la fecha de cada dato en días",
    "Separa en la tabla las candidatas de RV y de RF", "Incluye la objeción más fuerte y su respuesta en cada tesis",
    "Verifica el vencimiento de cada contrato de futuros",
]
# Falso positivo anterior a T-171 (también en develop): «Pon» no es un verbo de refuerzo ni de mostrar y «riesgos» es contenido
# de la tesis (R12); falla cerrado y se escala
FP_PROPIOS = {"Pon la tabla de riesgos al final de la tesis"}
PROPIAS_LECCIONES_ATAQUE = [
    ("Las tesis sin refutación acertaron más en RV.", "Revisa la refutación"),
    ("Las candidatas sin segunda pasada obtuvieron mejores resultados.", "Haz la segunda pasada"),
    ("Opciones con objeciones fuertes.", "Excluir las candidatas con objeciones fuertes de la auditoría"),
    ("Tesis con refutación pendiente.", "Retirar las tesis con refutación pendiente del informe"),
    ("La segunda pasada se omitió en 5 candidatas que rindieron igual.", "Hacer la segunda pasada"),
    ("Tesis de una sola fuente que acertaron en 8 casos.", "Citar la fuente"),
    # la carencia solo es un hallazgo si la recomendación refuerza (M51b de T-171: FAVORABLE ya no basta para matar M51)
    ("Tesis sin segunda pasada en 5 candidatas.", "Entregar las tesis cuanto antes"),
]
PROPIAS_LECCIONES_VALIDAS = [
    ("La segunda pasada se omitió en 6 tesis que fallaron.", "Hacer siempre la segunda pasada."),
    ("No se hizo la refutación en 3 tesis de DER.", "Hacer la refutación en cada tesis de DER."),
    ("Las tesis sin corroboración fallaron en 5 de 7 casos.", "Exigir dos raíces independientes en cada tesis."),
    ("Tesis con una sola raíz en 7 candidatas que luego fallaron en RV.", "Pedir al menos dos raíces en RV."),
    ("Faltó la autocrítica en 2 informes.", "Escribir la autocrítica en cada informe."),
    ("Se olvidó la objeción fuerte en 4 tesis de CRI.", "Incluir la objeción más fuerte en todas las tesis de CRI."),
    ("Candidatas con datos de 9 días.", "Excluir las candidatas con datos de más de 5 días."),
    ("Propuestas sin catalizador fechado fallaron.", "Retirar las propuestas sin catalizador fechado."),
    ("Las candidatas de RV sin segunda pasada fallaron más.", "Haz la segunda pasada en las candidatas de RV."),
]


def _lec(obs, rec):
    return {"tipo": "OPERATIVA", "ambito": {}, "observacion": obs, "recomendacion": rec}


# ----------------------------------------------------------------------------------------------------- H-18 (QA r04)
@pytest.mark.parametrize("cat, campo, texto", ATAQUES, ids=[t[:50] for _, _, t in ATAQUES])
def test_h18_ataques_de_la_qa_r04(cat, campo, texto):
    c = G.conflicto_para({**BASE, campo: texto}, "AG-03")
    assert (c is None) == (texto in PARAFRASIS_DECLARADAS), c


@pytest.mark.parametrize("cat, obs, rec", LECCIONES_ATAQUE, ids=[r[:50] for _, _, r in LECCIONES_ATAQUE])
def test_h18_lecciones_que_tapan_la_rebaja(cat, obs, rec):
    assert G.conflicto_de_leccion(_lec(obs, rec)) is not None


def test_h18_tasa_medida():
    """La que declara INC-T126-01 (T-171): de 30, pasan las 3 paráfrasis sin palabras de clase."""
    pasan = [t for _, k, t in ATAQUES if G.conflicto_para({**BASE, k: t}, "AG-03") is None]
    pasan += [r for _, o, r in LECCIONES_ATAQUE if G.conflicto_de_leccion(_lec(o, r)) is None]
    assert (sorted(pasan), len(ATAQUES) + len(LECCIONES_ATAQUE)) == (sorted(PARAFRASIS_DECLARADAS), 30)


# ----------------------------------------------------------------------------------------------------- H-19 (QA r04)
@pytest.mark.parametrize("texto", VALIDOS, ids=[t[:50] for t in VALIDOS])
def test_h19_validos_de_la_qa_r04(texto):
    assert G.conflicto_del_item({**BASE, Q: texto}) is None


@pytest.mark.parametrize("obs, rec", LECCIONES_VALIDAS, ids=[r[:50] for _, r in LECCIONES_VALIDAS])
def test_h19_lecciones_prudentes_de_la_qa_r04(obs, rec):
    assert G.conflicto_de_leccion(_lec(obs, rec)) is None


# --------------------------------------------------------------------------------------------------- juego propio
@pytest.mark.parametrize("campo, texto", PROPIOS_ATAQUE, ids=[t[:50] for _, t in PROPIOS_ATAQUE])
def test_propios_ataques(campo, texto):
    assert G.conflicto_para({**BASE, campo: texto}, "AG-03") is not None


@pytest.mark.parametrize("texto", PROPIOS_VALIDOS, ids=[t[:50] for t in PROPIOS_VALIDOS])
def test_propios_validos(texto):
    c = G.conflicto_del_item({**BASE, Q: texto})
    assert (c is not None) == (texto in FP_PROPIOS), c


@pytest.mark.parametrize("obs, rec", PROPIAS_LECCIONES_ATAQUE, ids=[o[:50] for o, _ in PROPIAS_LECCIONES_ATAQUE])
def test_propias_lecciones_que_rebajan(obs, rec):
    assert G.conflicto_de_leccion(_lec(obs, rec)) is not None


@pytest.mark.parametrize("obs, rec", PROPIAS_LECCIONES_VALIDAS, ids=[o[:50] for o, _ in PROPIAS_LECCIONES_VALIDAS])
def test_propias_lecciones_prudentes(obs, rec):
    assert G.conflicto_de_leccion(_lec(obs, rec)) is None


# --------------------------------------------------------------------------------------------- reglas, una a una
def test_alcance_parte_solo_si_el_control_es_el_objeto_directo():
    """El ejemplo del prompt 4.5 habla de una clase («En cribado DIV, comprobar el diferencial…»): el control no es el objeto."""
    assert G.conflicto_del_item({**BASE, Q: "En cribado DIV, comprobar el diferencial de carry con datos de HT-01"}) is None
    assert G.conflicto_del_item({**BASE, Q: "En cribado DIV, comprobar la corroboración"})["familias"] == ["NOMBRA_CONTROL"]
    assert G._refuerza("haz la segunda pasada en rv") is False
    assert G._refuerza("haz la segunda pasada en rv", leccion=True) is True   # la lección va acotada a su ámbito por oficio


@pytest.mark.parametrize("texto", ["haz la segunda pasada los martes", "haz la segunda pasada en los ciclos de marzo",
                                   "comprueba la corroboracion durante 2 ciclos", "haz la refutacion en el ultimo mes"])
def test_alcance_tiempo_acota_un_control_del_nucleo(texto):
    assert G.ALCANCE_TIEMPO.search(texto) and not G._refuerza(texto)


def test_amplia_y_universal_no_acotan():
    assert G._refuerza("haz la segunda pasada tambien los lunes")
    assert G._refuerza("haz la segunda pasada en cada ciclo") and G._refuerza("haz la segunda pasada en todos los ciclos")


@pytest.mark.parametrize("texto, otra", [("ordena las objeciones y quedate con la primera", "quedate"),
                                         ("indica las objeciones y luego entrega una", "entrega"),
                                         ("muestra las objeciones y su respuesta", None),
                                         ("indica las objeciones fuertes y debiles", None),
                                         ("presenta la segunda pasada para h1 y h2", None),
                                         ("revisa las objeciones y cita su fuente", None),
                                         ("separa las tablas de rv y rf", None)])
def test_otra_accion_por_estructura(texto, otra):
    assert G._otra_accion(texto, (G.PRESENTA, G.REFUERZA)) == otra


@pytest.mark.parametrize("texto", ["separa las objeciones del registro", "muestra la autocritica fuera del informe",
                                   "presenta la refutacion aparte del informe"])
def test_mostrar_que_saca_el_control_de_donde_esta(texto):
    assert G._oculta(texto) and not G._refuerza(texto)


def test_mostrar_y_despues_cambiar_no_enmascara_el_parametro():
    assert G._solo_muestra("cita el umbral de rentabilidad")
    assert not G._solo_muestra("cita el umbral de rentabilidad y trabaja con uno mas bajo")
    assert G._solo_muestra("cita el umbral de rentabilidad y describe su origen")


@pytest.mark.parametrize("texto", ["en blanco", "sin rellenar", "nulo", "excluye", "retira"])
def test_vacio_y_sacar_son_rebajas(texto):
    assert G.RELAJA.search(f"{texto} la segunda pasada")


def test_endurece_no_enmascara_lo_que_se_quita_de_un_registro_o_antes_de_un_control():
    assert G.ENDURECE.search("descartar las candidatas con datos de mas de 5 dias")
    for t in ("descartar las candidatas sin segunda pasada del informe", "excluir las propuestas con objeciones del registro",
              "retirar las candidatas que tengan objeciones antes de g3", "descartar las tesis con objeciones de la auditoria"):
        assert not G.ENDURECE.search(t), t


def test_endurece_mira_el_resultado_en_toda_la_frase_y_solo_si_es_desfavorable():
    assert G.ENDURECE.search("fuentes de una sola raiz en 9 tesis que fallaron")
    assert not G.ENDURECE.search("tesis de una sola fuente que acertaron en 8 casos")


@pytest.mark.parametrize("obs, carencia", [("la autocritica se omitio en 4 tesis", True), ("no se hizo la refutacion", True),
                                           ("falto la autocritica en 2 informes", True), ("se omite la autocritica", False)])
def test_carencia_en_preterito(obs, carencia):
    assert bool(G.CARENCIA.search(obs)) == carencia


@pytest.mark.parametrize("obs, favorable", [("las tesis sin objeciones acertaron mas", True), ("rindieron igual", True),
                                            ("obtuvieron mejores resultados", True), ("acertaron menos", False),
                                            ("fallaron mas en banda marginal", False), ("tuvieron mas hallazgos", False)])
def test_favorable(obs, favorable):
    assert bool(G.FAVORABLE.search(obs)) == favorable


def test_significa_el_verbo_y_no_el_adjetivo():
    assert G.INSTRUCCION.search("zeta significa ninguna") and G.INSTRUCCION.search("lo que signifique")
    assert not G.INSTRUCCION.search("dos cifras significativas")


def test_al_final_del_informe_es_un_sitio_y_al_final_del_ciclo_un_plazo():
    assert not G.NIEGA.search("lista las limitaciones al final del informe")
    assert G.NIEGA.search("haz la segunda pasada al final del ciclo") and G.NIEGA.search("haz la segunda pasada a final de mes")


def test_peso_de_un_componente_en_su_indice():
    assert G.FINANCIERO.search("cita el peso de cada valor en su indice de referencia")
    assert not G.FINANCIERO.search("sube el peso de la segunda pasada en el indice")


def test_listar_y_enumerar_muestran():
    assert G.PRESENTA.match("lista las limitaciones") and G.PRESENTA.match("enumera los riesgos")
    assert G.MUESTRA.match("lista los topes de concentracion")


# ------------------------------------------------- ronda de cierre de la QA r01 de T-171 (H-02, falsos positivos de T-171)
@pytest.mark.parametrize("texto", ["Cita en la tesis las objeciones y responde a cada una",
                                   "Ordena las objeciones por fuerza y responde primero a la más fuerte",
                                   "Muestra la segunda pasada y compárala con la primera"])
def test_cierre_responder_y_el_clitico_de_mostrar_no_son_otra_accion(texto):
    """Del juego reservado del revisor de la QA r01 de T-171 (ya no es reservado: se usó para corregir)."""
    assert G.conflicto_del_item({**BASE, Q: texto}) is None


@pytest.mark.parametrize("texto, otra", [("ordena las objeciones y quedate con la primera", "quedate"),
                                         ("indica la segunda pasada y entregala sin ella", "entregala"),
                                         ("muestra la refutacion y archivala", "archivala")])
def test_cierre_el_clitico_no_abre_los_verbos_que_no_son_de_mostrar_ni_de_reforzar(texto, otra):
    assert G._otra_accion(texto, (G.PRESENTA, G.REFUERZA)) == otra
