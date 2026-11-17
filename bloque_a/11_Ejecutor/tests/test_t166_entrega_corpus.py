"""T-166 · Entrega del corpus del Bloque A (Documento 0 V5.3): «Catálogo V5.0» en los prompts MC y en las funciones del Motor
(D-2 de T-157), FC-EVAL-001 en el ejemplo del Registro de cálculos (D-3), RF-0046 en el ejemplo del Evaluador (D-4) y la
respuesta final de CT-03 en el Anexo B (T-162, T-169).

Criterios de aceptación en `.docs/tickets/T-166/README.md`. Sin red ni modelo: corpus, código y un bloque simulado.
"""
import copy
import difflib
import json
import re
import unicodedata

import goldens_ct as g
import jsonschema
import pytest
from bloque_a.configuracion import DIR_EJECUTOR, buscar_versionado, cargar_config
from bloque_a.herramientas import verificador_ids as vi
from bloque_a.motor import servicio
from bloque_a.prompts import NOMBRES_ALTERNATIVOS, CatalogoPrompts
from conftest import AS_OF, nuevo_bloque

from bloque_a import contratos, respuesta_final

BLOQUE = DIR_EJECUTOR.parent
HISTORICO = BLOQUE / "99_Historico_V5.2"
DOC0_V52 = "Documento 0 - Protocolo maestro del Bloque A - Versión óptima V5.2.md"
DOC0_V53 = "Documento 0 - Protocolo maestro del Bloque A - Versión óptima V5.3.md"
PROMPTS_MC = ["System prompt - MC-01 Fundamentos cuantitativos y estadística - Versión óptima V5.0",
              "System prompt - MC-02 Series temporales, tendencias, regímenes y volatilidad - Versión óptima V5.0",
              "System prompt - MC-03 Econometría, causalidad y macroeconomía cuantitativa - Versión óptima V5.0",
              "System prompt - MC-04 Crecimiento, difusión y prospectiva cuantitativa - Versión óptima V5.0",
              "System prompt - MC-05 Simulación estocástica y escenarios - Versión óptima V5.0"]
EVALUADOR = "02_System_prompts/System prompt - Evaluador de Previsiones y Aprendizaje - Versión óptima V5.0"
FUNCIONES_MOTOR = ("03_Funciones/Funciones, tareas y cometidos – Motor de Cálculo Avanzado para el Analizador de Tendencias de "
                   "Inversión – óptima V5.0")
REGISTRO_CALCULOS = "05_Archivos_operativos/Registro de cálculos del Motor (esquema V2.0)"
F9 = "05_Archivos_operativos/Registro de Fuentes para el Analizador de Tendencias de Inversión - V3.2.md"
# Los ocho archivos que corrige la entrega y la sustitución exacta de cada uno (lo único que puede cambiar)
CORREGIDOS = {**{f"02_System_prompts/{p}": [("Catálogo V4.0", "Catálogo V5.0")] for p in PROMPTS_MC},
              FUNCIONES_MOTOR: [("Catálogo V4.0", "Catálogo V5.0")],
              REGISTRO_CALCULOS: [('"ficha_id":"FX-MC10-003","ficha_version":"1.0","catalog_version":"4.0"',
                                   '"ficha_id":"FC-EVAL-001","ficha_version":"1.0","catalog_version":"5.0"')],
              EVALUADOR: [('"ref_id":"RF-0123"', '"ref_id":"RF-0046"')]}
RE_CATALOGO_V4 = re.compile(r"Cat[aá]logo(?: de cálculos(?: del Motor)?)? V4[.,]0", re.IGNORECASE)


def _leer(rel):
    return (BLOQUE / rel).read_text(encoding="utf-8")


def _vivos():
    """Los .md del corpus vivo del Bloque A: sin `11_Ejecutor/` ni `99_Historico*`."""
    for p in sorted(BLOQUE.rglob("*.md")):
        partes = p.relative_to(BLOQUE).parts
        if partes[0] != "11_Ejecutor" and not partes[0].startswith("99_Historico"):
            yield p


# ---------------------------------------------------------------- CA-1 · D-2: ningún «Catálogo V4.0» vivo
def test_ca1_ningun_md_vivo_del_corpus_cita_el_catalogo_v40():
    citas = [(str(p.relative_to(BLOQUE)), m.group(0)) for p in _vivos() for m in RE_CATALOGO_V4.finditer(p.read_text(encoding="utf-8"))]
    assert citas == []


@pytest.mark.parametrize("prompt", PROMPTS_MC)
def test_ca1_cada_prompt_mc_cita_el_catalogo_vigente_donde_citaba_el_v40(prompt):
    antes = (HISTORICO / "02_System_prompts" / f"{prompt}.md").read_text(encoding="utf-8")
    ahora = _leer(f"02_System_prompts/{prompt}.md")
    vigente = f"Catálogo V{servicio.CATALOG_VERSION}"
    assert antes.count("Catálogo V4.0") >= 1 and ahora.count(vigente) == antes.count("Catálogo V4.0") + antes.count(vigente)
    assert "Catálogo V4.0" not in ahora


def test_ca1_el_patron_ve_las_formas_de_citar_el_v40():
    for texto in ("ficha VIGENTE del Catálogo V4.0;", "Catalogo V4,0", "Catálogo de cálculos del Motor V4.0"):
        assert RE_CATALOGO_V4.search(texto), texto
    assert not RE_CATALOGO_V4.search("Mapa de conocimientos V4.0")


# ---------------------------------------------------------------- CA-2 · D-3 y D-4: el verificador da 0 errores
@pytest.fixture(scope="module")
def informe():
    return vi.verificar(BLOQUE)


def test_ca2_el_verificador_no_da_ningun_error_sobre_el_corpus(informe):
    assert sum(c["ERROR"] for c in informe["resumen"].values()) == 0
    codigos = {h["codigo"] for h in informe["hallazgos"]}
    assert not codigos & {"FICHA_CITADA_INEXISTENTE", "REF_INEXISTENTE", "MENCION_OTRA_VERSION"}
    assert [h["id"] for h in informe["hallazgos"] if h["nivel"] == "AVISO"] == ["RF-1"]   # la tarjeta del Auditor (INC-T157-05)
    assert informe["entradas"]["documento_0"]["archivo"].endswith(DOC0_V53)


def test_ca2_el_ejemplo_del_registro_de_calculos_cita_una_ficha_vigente_del_mc10():
    texto = _leer(f"{REGISTRO_CALCULOS}.md")
    bloque = texto[texto.index("## 7. Ejemplo ficticio"):]
    ejemplo = json.loads(bloque[bloque.index("```json") + 7:bloque.index("```", bloque.index("```json") + 7)])
    op, ficha = ejemplo["operacion"], servicio.IMPLEMENTADAS["FC-EVAL-001"]
    assert op["ficha_id"] == "FC-EVAL-001" and op["catalog_version"] == servicio.CATALOG_VERSION
    assert op["ficha_version"] == ficha["version"] and ejemplo["modulos"] == [ficha["modulo"]] == ["MC-10"]
    assert "FX-MC10-003" not in texto


def test_ca2_el_ejemplo_del_evaluador_cita_una_rf_que_existe_en_f9():
    prompt, f9 = _leer(f"{EVALUADOR}.md"), _leer(F9)
    assert '"ref_id":"RF-0046"' in prompt and "RF-0123" not in prompt
    bajas = f9[f9.index("## Registro de bajas"):]
    assert "\n#### RF-0046 · " in f9[:f9.index("## Registro de bajas")] and "RF-0046" not in bajas
    ficha = f9[f9.index("\n#### RF-0046 · "):]
    ficha = ficha[:ficha.index("\n####", 1)]
    assert "TF-05" in ficha and "**Estado:** Aprobada" in ficha


# ---------------------------------------------------------------- CA-3 · la V5.3 es la V5.2 con CT-03
def _sin_anexo_b(texto):
    return (texto[:texto.index("## ANEXO B.")] + texto[texto.index("## ANEXO C."):]).splitlines()


def _anexo_b(texto):
    return texto[texto.index("## ANEXO B."):texto.index("## ANEXO C.")].splitlines()


def test_ca3_en_01_gobernanza_solo_la_v53_y_la_v52_en_el_historico():
    assert sorted(p.name for p in (BLOQUE / "01_Gobernanza").iterdir()) == [DOC0_V53]
    assert sorted(p.name for p in (HISTORICO / "01_Gobernanza").iterdir()) == [DOC0_V52]


def test_ca3_fuera_del_anexo_b_solo_cambian_la_cabecera_y_el_registro_de_cambios():
    v52 = (HISTORICO / "01_Gobernanza" / DOC0_V52).read_text(encoding="utf-8")
    v53 = _leer(f"01_Gobernanza/{DOC0_V53}")
    cambios = [x for x in difflib.ndiff(_sin_anexo_b(v52), _sin_anexo_b(v53)) if x[:1] in "+-"]
    quitadas = [x[2:].split(":**")[0] for x in cambios if x[0] == "-"]
    puestas = [x[2:] for x in cambios if x[0] == "+"]
    assert quitadas == ["## Buscador de Oportunidades de Inversión · Versión óptima V5.2", "**Fecha", "**Sustituye a", "**Actualizado"]
    assert [x.split(":**")[0] for x in puestas[:4]] == ["## Buscador de Oportunidades de Inversión · Versión óptima V5.3", "**Fecha",
                                                       "**Sustituye a", "**Actualizado"]
    assert len(puestas) == 5 and puestas[4].startswith("| óptima V5.3 | 17/11/2026 | Anexo B: CT-03 describe la respuesta final")
    assert "`99_Historico_V5.2`" in puestas[2] and puestas[3].startswith("**Actualizado:** V5.3, 17/11/2026 — Anexo B: la respuesta final")
    assert "T-166" in puestas[4] and '`version_contrato` sigue en "5.1"' in puestas[4]


def test_ca3_dentro_del_anexo_b_solo_cambia_la_lectura_y_se_anade_la_final_de_ct03():
    v52 = _anexo_b((HISTORICO / "01_Gobernanza" / DOC0_V52).read_text(encoding="utf-8"))
    v53 = _anexo_b(_leer(f"01_Gobernanza/{DOC0_V53}"))
    cambios = [x for x in difflib.ndiff(v52, v53) if x[:1] in "+-"]
    assert [x[2:].startswith("**Cómo se lee este anexo (V5.2).** Describe") for x in cambios if x[0] == "-"] == [True]
    puestas = [x[2:] for x in cambios if x[0] == "+"]
    assert len(puestas) == 2 and puestas[0].startswith("**Cómo se lee este anexo (V5.2 y V5.3).**")
    assert puestas[1].startswith("Respuesta final (V5.3). ")
    assert puestas[0].replace("(V5.2 y V5.3)", "(V5.2)") in v52
    # la final va en el párrafo de CT-03, justo después de su texto de la V5.2
    assert puestas[1] in g.parrafos_anexo_b()["CT-03"] and contratos.VERSION_CONTRATO == "5.1"


# ---------------------------------------------------------------- CA-4 · los ocho archivos corregidos y su histórico
@pytest.mark.parametrize("rel", sorted(CORREGIDOS))
def test_ca4_cada_archivo_corregido_es_su_version_anterior_con_solo_la_sustitucion(rel):
    antes = (HISTORICO / f"{rel}.md").read_text(encoding="utf-8")
    ahora = _leer(f"{rel}.md")
    restaurado = ahora
    for viejo, nuevo in CORREGIDOS[rel]:
        assert nuevo in ahora and viejo in antes
        restaurado = restaurado.replace(nuevo, viejo)
    assert restaurado == antes and ahora != antes
    # su .docx (copia de consulta del texto anterior) se va con él al histórico; el .md nuevo no tiene .docx (INC-T166-01)
    assert (HISTORICO / f"{rel}.docx").is_file() and not (BLOQUE / f"{rel}.docx").exists()


def test_ca4_el_historico_solo_tiene_lo_que_sustituye_esta_entrega():
    esperado = sorted([f"01_Gobernanza/{DOC0_V52}"] + [f"{r}.{x}" for r in CORREGIDOS for x in ("md", "docx")])
    hay = sorted(unicodedata.normalize("NFC", str(p.relative_to(HISTORICO))) for p in HISTORICO.rglob("*") if p.is_file())
    assert hay == esperado


# ---------------------------------------------------------------- CA-5 · el Anexo B describe la final como el código
def _codigo():
    return {"esquema": copy.deepcopy(respuesta_final.ESQUEMA), "resultados": dict(respuesta_final.RESULTADOS),
            "estado_f5": dict(respuesta_final.ESTADO_F5), "confianzas": list(respuesta_final.CONFIANZAS),
            "patron": respuesta_final.PATRON_REF, "errores_control": [e.__name__ for e in respuesta_final.ERRORES_DE_CONTROL],
            "rechazos": [e.__name__ for e in respuesta_final.RECHAZOS_SIN_EFECTO]}


def _nombres(texto):
    return re.findall(r"`([^`]+)`", texto)


def _final_que_difiere(parrafo, c):
    """Lo que difiere entre el párrafo «Respuesta final (V5.3)» de CT-03 y `respuesta_final.py` (`c`, de `_codigo`)."""
    m = re.search(r"Respuesta final \(V5\.3\)\. [^\n]*", parrafo)
    if not m:
        return ["no hay párrafo de la respuesta final"]
    p, esq, difieren = m.group(0), c["esquema"], []

    def frase(rx):
        x = re.search(rx, p)
        if not x:
            difieren.append(f"falta la frase {rx!r}")
        return x

    if x := frase(r"La final lleva ([^.]*), y ningún otro campo\."):
        if set(_nombres(x.group(1))) != set(esq["required"]) or set(esq["properties"]) != set(esq["required"]):
            difieren.append(f"cuerpo: el código exige {sorted(esq['required'])} y nombra {sorted(esq['properties'])}")
        if esq.get("additionalProperties") is not False:
            difieren.append("el código admite otros campos")
        if "`ruta` ANALITICA" not in x.group(1) or esq["properties"]["ruta"] != {"const": "ANALITICA"}:
            difieren.append("la ruta de la final no es ANALITICA")
    rf = esq["properties"]["respuesta_final"]
    if x := frase(r"`respuesta_final` lleva (`provisional_msg_id`) \([^)]*\) y (`resultado_analisis`) \(([^)]*)\)\."):
        if {x.group(1).strip("`"), x.group(2).strip("`")} != set(rf["required"]) or set(rf["properties"]) != set(rf["required"]):
            difieren.append(f"respuesta_final: el código exige {sorted(rf['required'])}")
        valores = [v.strip() for v in x.group(3).split(" | ")]
        if valores != rf["properties"]["resultado_analisis"]["enum"] or valores != list(c["resultados"]):
            difieren.append(f"resultados: {valores} frente a {list(c['resultados'])}")
        if rf["properties"]["provisional_msg_id"].get("pattern") != "^MSG-" or "MSG-" not in x.group(0):
            difieren.append("provisional_msg_id no es un MSG-")
    if x := frase(r"Estado común según el resultado: ([^.]*)\."):
        dicho = {}
        for trozo in x.group(1).split("; "):
            *res, estado = re.split(r", | y ", trozo)
            dicho |= {r: estado for r in res}
        if dicho != c["resultados"]:
            difieren.append(f"estado común: {dicho} frente a {c['resultados']}")
    if x := frase(r"con estado (\w+) \(([^)]*)\) o (\w+)\."):
        dicho = {**{e: x.group(1) for e in x.group(2).split(" o ")}, "SIN_RESULTADO": x.group(3)}
        if dicho != c["estado_f5"]:
            difieren.append(f"estado en F5: {dicho} frente a {c['estado_f5']}")
    if x := frase(r"Las referencias son identificadores ([^:]*), sin repetir:"):
        dichos = re.findall(r"([A-Z]+)-", x.group(1))
        codigo = re.search(r"\(\?:([A-Z|]+)\)", c["patron"]).group(1).split("|")
        if dichos != codigo:
            difieren.append(f"prefijos: {dichos} frente a {codigo}")
        if esq["properties"]["referencias"].get("uniqueItems") is not True:
            difieren.append("el código admite referencias repetidas")
    if x := frase(r"Con (\w+) no hay referencias; con (\w+) o (\w+), como mucho el RUN-\."):
        reglas = {tuple(sorted([r["if"]["properties"]["respuesta_final"]["properties"]["resultado_analisis"].get("const")]
                               if "const" in r["if"]["properties"]["respuesta_final"]["properties"]["resultado_analisis"]
                               else r["if"]["properties"]["respuesta_final"]["properties"]["resultado_analisis"]["enum"])):
                  r["then"]["properties"]["referencias"] for r in esq.get("allOf", [])}
        if reglas.get((x.group(1),)) != {"maxItems": 0}:
            difieren.append(f"sin referencias: el código {reglas}")
        if reglas.get(tuple(sorted([x.group(2), x.group(3)]))) != {"maxItems": 1, "items": {"pattern": "^RUN-"}}:
            difieren.append(f"como mucho el RUN-: el código {reglas}")
    if x := frase(r"\(([a-z ]+(?: < [a-z ]+)+);"):
        if x.group(1).split(" < ") != c["confianzas"]:
            difieren.append(f"confianza: {x.group(1)} frente a {c['confianzas']}")
        if c["esquema"]["properties"]["confianza"] != contratos.ESQUEMAS["CONSULTA"]["properties"]["confianza"]:
            difieren.append("la confianza de la final no es la de la consulta")
        if set(c["confianzas"]) != set(contratos.ESQUEMAS["CONSULTA"]["properties"]["confianza"]["enum"]):
            difieren.append("el vocabulario de confianza no es el de la consulta")
    # r02 (QA r01, H-01): los errores que paran la consulta son `ERRORES_DE_CONTROL`, cada uno con su descripción en la frase
    if set(c["errores_control"]) != set(ERRORES_DE_CONTROL_EN_LA_PROSA):
        difieren.append(f"errores de control: el código {sorted(c['errores_control'])}")
    difieren += [f"no nombra {nombre} («{texto}»)" for nombre, texto in ERRORES_DE_CONTROL_EN_LA_PROSA.items() if texto not in p]
    # r03 (QA r02, H-07): los rechazos que se apartan en vez de parar (`RECHAZOS_SIN_EFECTO`)
    if set(c["rechazos"]) != {"DatosSensibles", "MensajeInvalido"} or "(R8 o un mensaje que no cumple su contrato)" not in p:
        difieren.append(f"rechazos que se apartan: el código {sorted(c['rechazos'])}")
    for fija in FRASES_FIJAS_FINAL:
        if fija not in p:
            difieren.append(f"falta «{fija}»")
    return difieren


# r02 (QA r01, H-01): cómo nombra la frase cada error de `respuesta_final.ERRORES_DE_CONTROL` (PermissionError cubre los controles
# del almacén, EscrituraFueraDeReserva y PronosticoCongelado, y los de la mensajería, CanalNoPrevisto y DatosSensibles)
ERRORES_DE_CONTROL_EN_LA_PROSA = {"PermissionError": "los controles del almacén y de la mensajería",
                                  "MensajeInvalido": "un mensaje que no cumple su contrato",
                                  "FugaDeInformacion": "una fuga de información de HT-01",
                                  "ReplayFaltante": "una respuesta sin grabar en el modo de reproducción"}


# Frases que no son listas y que describen reglas del código medidas abajo con el propio código
FRASES_FIJAS_FINAL = [
    # r02 (QA r01, H-04): la primera frase entera y tres más
    ("Respuesta final (V5.3). Cuando termina el análisis escalado de una consulta de ruta ANALITICA (o falla, no entrega o no se "
     "lanzó), el Coordinador envía otro CT-03 RETORNO al Broker, la respuesta final; la provisional no cambia."),
    "`escalado` (el mismo que la provisional)",
    "`provisional_msg_id` (el `msg_id` de la provisional, MSG-, que queda registrado en F5)",
    "La confianza es, con opciones, la más baja de las suyas en F3 (",
    "En el retorno CT-03, `respuesta_final` es opcional: solo la lleva la final, no la respuesta en N0 ni la provisional.",
    ("El resultado sale de F5: FALLIDO si el `estado_run` del `escalado` es FALLIDO; NO_EJECUTADO si el `escalado` no tiene "
     "`run_id`; SIN_ENTREGA si el RUN- no consta en F5, no lo lanzó esta consulta o su `entrega` en F5 no es ENTREGADA (sin "
     "`entrega`, cuenta como entregada); si no, ENTREGADO con el RUN- COMPLETO y ENTREGADO_PARCIAL en los demás casos."),
    # r02 (QA r01, H-02): sin RUN- el sobre no lleva `run_id` (`Mensajeria.crear`); nulo solo en la copia de F5
    ("En el sobre, `query_id` es el de la consulta y `run_id` el del RUN- solo si consta en F5 y lo lanzó esta consulta (si no, "
     "el sobre no lleva `run_id`, y la copia de la final en F5 lo deja nulo)."),
    ("el RUN- y, por cada opción de su top-3 y en su orden, la OPP-, sus TND-, sus CLM- (evidencias) y los PRG- que ese RUN- "
     "congeló para ella; solo se cita un identificador que es la clave de una entrada de F1 a F5 a la fecha de la consulta."),
    "una confianza fuera de ese vocabulario cuenta como especulativo); sin opciones o sin resultado, la más baja entre la de la provisional y especulativo.",
    "El texto de `respuesta` lo escribe el código con lo que hay en F3 y F5, sin llamar al modelo; sin resultado, dice que la respuesta provisional no se confirma ni se amplía.",
    # r02 (QA r01, H-03): un rechazo de la mensajería sí escribe su incidencia en HA
    ("La final se valida con su esquema (`respuesta_final.ESQUEMA` de `bloque_a/respuesta_final.py`) y por la mensajería antes de "
     "escribir la final en F5 (un rechazo de la mensajería deja su incidencia en HA, como con cualquier mensaje), sale una sola "
     "vez y queda en F5 en la misma QRY-"),
    # r02 (QA r01, H-01): qué para la consulta y qué da FALLIDO
    # r03 (QA r02, H-07): los rechazos del esquema y de la mensajería (`RECHAZOS_SIN_EFECTO`) se apartan, no paran
    ("Una final que no salió la envían la consulta o el ciclo siguientes, con la fecha de su consulta; si no se puede enviar, se "
     "aparta una vez con una incidencia escalada al operador, también si la rechazan su esquema o la mensajería (R8 o un mensaje "
     "que no cumple su contrato), salvo un fallo de integridad o cualquier otro error de control, que para la consulta o el "
     "ciclo."),
    ("Un fallo de integridad del almacén o un error de control durante el análisis (los controles del almacén y de la mensajería, "
     "un mensaje que no cumple su contrato, una fuga de información de HT-01 o una respuesta sin grabar en el modo de "
     "reproducción: `respuesta_final.ERRORES_DE_CONTROL`) para la consulta: no hay provisional ni final; cualquier otro error da "
     "la final FALLIDO."),
]


def test_ca5_el_anexo_b_describe_la_respuesta_final_como_respuesta_final_py():
    assert _final_que_difiere(g.parrafos_anexo_b()["CT-03"], _codigo()) == []


MUTANTES_CODIGO = {
    "un resultado más": lambda c: (c["resultados"].__setitem__("CANCELADO", "SIN_RESULTADO"),
                                   c["esquema"]["properties"]["respuesta_final"]["properties"]["resultado_analisis"]["enum"].append("CANCELADO")),
    "otro estado común": lambda c: c["resultados"].__setitem__("ENTREGADO_PARCIAL", "COMPLETO"),
    "otro estado en F5": lambda c: c["estado_f5"].__setitem__("PARCIAL", "RESPONDIDA_PARCIAL"),
    "otro orden de confianza": lambda c: c.__setitem__("confianzas", ["especulativo", "en disputa", "probable", "establecido"]),
    "un prefijo más": lambda c: c.__setitem__("patron", c["patron"].replace("PRG", "PRG|HIT")),
    "un campo más en el cuerpo": lambda c: (c["esquema"]["required"].append("documentos"), c["esquema"]["properties"].__setitem__("documentos", {})),
    "un campo opcional en el cuerpo": lambda c: c["esquema"]["properties"].__setitem__("notas", {}),
    "otros campos admitidos": lambda c: c["esquema"].pop("additionalProperties"),
    "un campo más en respuesta_final": lambda c: c["esquema"]["properties"]["respuesta_final"]["required"].append("run_id"),
    "referencias repetidas": lambda c: c["esquema"]["properties"]["referencias"].pop("uniqueItems"),
    "sin lanzar se cita el RUN-": lambda c: c["esquema"]["allOf"][0]["then"]["properties"]["referencias"].__setitem__("maxItems", 1),
    "fallido sin referencias": lambda c: c["esquema"]["allOf"][1]["then"]["properties"].__setitem__("referencias", {"maxItems": 0}),
    # r02 (QA r01, H-01): una fuga de información ya no para la consulta
    "la fuga de información no para": lambda c: c["errores_control"].remove("FugaDeInformacion"),
    "otro error de control": lambda c: c["errores_control"].append("TimeoutError"),
    # r03 (QA r02, H-07)
    "un rechazo más se aparta": lambda c: c["rechazos"].append("CanalNoPrevisto"),
}


@pytest.mark.parametrize("mutante", sorted(MUTANTES_CODIGO))
def test_ca5_un_cambio_en_respuesta_final_py_se_nota(mutante):
    c = _codigo()
    MUTANTES_CODIGO[mutante](c)
    assert _final_que_difiere(g.parrafos_anexo_b()["CT-03"], c) != []


MUTANTES_PROSA = [
    ("| FALLIDO | NO_EJECUTADO)", "| FALLIDO)"),
    ("ENTREGADO_PARCIAL, PARCIAL;", "ENTREGADO_PARCIAL, COMPLETO;"),
    ("RUN-, OPP-, TND-, CLM- y PRG-", "RUN-, OPP-, TND- y CLM-"),
    ("en disputa < especulativo < probable < establecido", "especulativo < en disputa < probable < establecido"),
    ("`limitaciones` y `respuesta_final`, y ningún otro campo", "y `respuesta_final`, y ningún otro campo"),
    ("Con NO_EJECUTADO no hay referencias; con FALLIDO o SIN_ENTREGA,", "Con FALLIDO no hay referencias; con NO_EJECUTADO o SIN_ENTREGA,"),
    ("RESPONDIDA_FINAL (COMPLETO o PARCIAL)", "RESPONDIDA_FINAL (COMPLETO)"),
    ("(sin `entrega`, cuenta como entregada)", "(sin `entrega`, no cuenta como entregada)"),
    ("sale una sola vez", "sale cada vez que se pide"),
    ("solo si consta en F5 y lo lanzó esta consulta (si no, el sobre no lleva `run_id`", "siempre (si no, el sobre no lleva `run_id`"),
    # r02 (QA r01, H-04): los seis mutantes vivos de `revisores/r01_02_mutantes_prosa.py`
    ("con opciones, la más baja de las suyas en F3", "con opciones, la más alta de las suyas en F3"),
    ("que queda registrado en F5)", "que queda registrado en F3)"),
    ("`escalado` (el mismo que la provisional)", "`escalado` (distinto del de la provisional)"),
    ("de una consulta de ruta ANALITICA", "de una consulta de ruta N0"),
    ("(o falla, no entrega o no se lanzó)", "(solo si entrega)"),
    ("`provisional_msg_id` (el `msg_id` de la provisional, MSG-,", "`provisional_msg_id` (el `query_id` de la consulta, MSG-,"),
    # r02 (QA r01, H-01 a H-03): las frases corregidas
    ("una fuga de información de HT-01 o ", ""),
    ("; cualquier otro error da la final FALLIDO.", "."),
    (", salvo un fallo de integridad o cualquier otro error de control, que para la consulta o el ciclo.", "."),
    # r03 (QA r02, H-07)
    ("también si la rechazan su esquema o la mensajería (R8 o un mensaje que no cumple su contrato), ", ""),
    ("el sobre no lleva `run_id`, y la copia de la final en F5 lo deja nulo", "nulo"),
    ("antes de escribir la final en F5 (un rechazo de la mensajería deja su incidencia en HA, como con cualquier mensaje)", "antes de escribir nada"),
]


@pytest.mark.parametrize("viejo, nuevo", MUTANTES_PROSA, ids=[m[0][:40] for m in MUTANTES_PROSA])
def test_ca5_un_cambio_en_la_prosa_se_nota(viejo, nuevo):
    p = g.parrafos_anexo_b()["CT-03"]
    assert p.count(viejo) == 1, "el texto del mutante ya no está en el Anexo B: actualícelo"
    assert _final_que_difiere(p.replace(viejo, nuevo), _codigo()) != []


# Lo que dicen las frases fijas, medido con las funciones del código
@pytest.mark.parametrize("escalado, run, resultado", [
    ({"run_id": "RUN-2026-0001", "estado_run": "FALLIDO"}, None, "FALLIDO"),
    ({"run_id": None}, None, "NO_EJECUTADO"),
    ({"run_id": "RUN-2026-0001"}, None, "SIN_ENTREGA"),
    ({"run_id": "RUN-2026-0001"}, {"entrega": "BLOQUEADA", "estado": "COMPLETO"}, "SIN_ENTREGA"),
    ({"run_id": "RUN-2026-0001"}, {"estado": "COMPLETO"}, "ENTREGADO"),
    ({"run_id": "RUN-2026-0001"}, {"entrega": "ENTREGADA", "estado": "PARCIAL"}, "ENTREGADO_PARCIAL"),
], ids=["fallido", "sin lanzar", "sin RUN- en F5", "bloqueado", "sin entrega cuenta como entregada", "parcial"])
def test_ca5_el_resultado_sale_de_f5_como_dice_el_anexo_b(escalado, run, resultado):
    assert respuesta_final._resultado(escalado, run) == resultado


def test_ca5_los_errores_de_control_son_los_que_paran_la_consulta():
    """r02 (QA r01, H-01): `PermissionError` cubre los controles del almacén y de la mensajería que nombra la frase."""
    from bloque_a.almacen import EscrituraFueraDeReserva, PronosticoCongelado
    from bloque_a.contratos import CanalNoPrevisto, DatosSensibles
    assert all(issubclass(e, PermissionError) for e in (EscrituraFueraDeReserva, PronosticoCongelado, CanalNoPrevisto, DatosSensibles))
    assert not respuesta_final.para_la_consulta(_AlmacenIntegro(), KeyError("x"))           # cualquier otro error: FALLIDO
    assert all(respuesta_final.para_la_consulta(_AlmacenIntegro(), e("x")) for e in respuesta_final.ERRORES_DE_CONTROL)


def _pendiente(tmp_path, universo, monkeypatch):
    """Una final pendiente: la consulta deja la provisional registrada y la final sin enviar."""
    b = nuevo_bloque(tmp_path, universo, cfg=cargar_config(extra={"modo": "backtest"}))
    real = respuesta_final.enviar
    monkeypatch.setattr(respuesta_final, "enviar", lambda *a, **k: None)
    q = b.consulta("Analiza qué conviene hacer ahora", as_of=AS_OF, ejecutar_escalado=False)
    monkeypatch.setattr(respuesta_final, "enviar", real)
    assert [x for x, _ in respuesta_final.pendientes(b.almacen)] == [q["query_id"]]
    return b, q["query_id"]


@pytest.mark.parametrize("error", ["DatosSensibles", "MensajeInvalido"])
def test_ca5_los_rechazos_de_la_mensajeria_son_de_control_y_no_paran_se_apartan(tmp_path, universo, monkeypatch, error):
    """r03 (QA r02, H-07; prueba de `revisores/r02_01`): una final pendiente que la mensajería rechaza por R8 o por un mensaje que
    no cumple su contrato se aparta con su incidencia escalada, y la consulta siguiente sigue, como dice el Anexo B."""
    from bloque_a import contratos as c
    exc = getattr(c, error)("x")
    assert isinstance(exc, respuesta_final.ERRORES_DE_CONTROL)
    b, qry = _pendiente(tmp_path, universo, monkeypatch)
    crear = b.mensajeria.crear

    def crear_o_fallar(contrato, emisor, receptor, cuerpo, **k):
        if contrato == "CT-03" and "respuesta_final" in cuerpo and k.get("query_id") == qry:   # solo la pendiente
            raise exc
        return crear(contrato, emisor, receptor, cuerpo, **k)
    monkeypatch.setattr(b.mensajeria, "crear", crear_o_fallar)
    b.consulta("Analiza qué conviene hacer ahora", as_of="2026-06-12", ejecutar_escalado=False)
    f5 = b.almacen.estado("F5")[qry]
    assert f5.get("final_no_enviable") == {"error": error} and not f5.get("respuesta_final")
    assert any(e.get("escalado_operador") and qry in str(e.get("descripcion", e)) for e in b.almacen.leer("HA"))


class _AlmacenIntegro:
    def verificar_integridad(self):
        return {"F5": True}


@pytest.mark.parametrize("provisional, final", [("establecido", "especulativo"), ("probable", "especulativo"),
                                                ("especulativo", "especulativo"), ("en disputa", "en disputa")])
def test_ca5_sin_resultado_la_confianza_es_la_mas_baja_entre_la_provisional_y_especulativo(tmp_path, universo, monkeypatch,
                                                                                           provisional, final):
    """r02 (QA r01, H-05; prueba de `revisores/r01_01`): «sin opciones o sin resultado, la más baja entre la de la provisional
    y especulativo», con el ejecutor simulado y una consulta sin escalado (NO_EJECUTADO)."""
    b = nuevo_bloque(tmp_path, universo, cfg=cargar_config(extra={"modo": "backtest"}))
    real = respuesta_final.construir

    def construir(alm, qry, msg, as_of, fallo=None):
        return real(alm, {**qry, "confianza": provisional}, msg, as_of, fallo)
    monkeypatch.setattr(respuesta_final, "construir", construir)
    q = b.consulta("Analiza qué conviene hacer ahora", as_of=AS_OF, ejecutar_escalado=False)
    assert q["respuesta_final"]["respuesta_final"]["resultado_analisis"] == "NO_EJECUTADO"
    assert q["respuesta_final"]["confianza"] == final


def test_ca5_la_confianza_es_la_mas_baja_como_dice_el_anexo_b():
    assert respuesta_final._menos_confiada(["establecido", "probable", "en disputa"]) == "en disputa"
    assert respuesta_final._menos_confiada(["probable", "especulativo"]) == "especulativo"


# ---------------------------------------------------------------- CA-6 · el esquema derivado admite la final
def test_ca6_el_derivado_de_ct03_admite_y_valida_la_respuesta_final():
    esquemas = json.loads((g.CARPETA / "anexo_b_esquemas.json").read_text(encoding="utf-8"))
    derivado = esquemas["CT-03.RETORNO"]
    rf = derivado["properties"]["respuesta_final"]
    assert "respuesta_final" not in derivado["required"] and "V5.3" in derivado["$comment"]
    assert rf["required"] == respuesta_final.ESQUEMA["properties"]["respuesta_final"]["required"]
    assert rf["properties"]["resultado_analisis"]["enum"] == list(respuesta_final.RESULTADOS)
    ejemplo = json.loads((g.CARPETA / "anexo_b_ejemplos.json").read_text(encoding="utf-8"))["CT-03.RETORNO"]
    jsonschema.validate(ejemplo, derivado)                                                    # la respuesta N0, sin final
    final = {**ejemplo, "ruta": "ANALITICA", "referencias": ["RUN-2026-0001"],
             "escalado": {"run_id": "RUN-2026-0001", "plazo_estimado": "…", "nivel": "N1", "clases": ["RV"], "respuesta_provisional": "…"},
             "respuesta_final": {"provisional_msg_id": "MSG-2026-0001", "resultado_analisis": "SIN_ENTREGA"}}
    jsonschema.validate(final, derivado)
    for roto in ({"provisional_msg_id": "MSG-2026-0001"}, {"provisional_msg_id": "MSG-1", "resultado_analisis": "TERMINADO"}):
        assert list(jsonschema.Draft202012Validator(derivado).iter_errors({**final, "respuesta_final": roto}))
    assert all("V5.3" in e["$comment"] and "V5.2" not in e["$comment"] for e in esquemas.values())


# ---------------------------------------------------------------- CA-7 · el ejecutor sigue encontrando los prompts
def test_ca7_el_ejecutor_carga_el_prompt_corregido_del_evaluador():
    c = CatalogoPrompts(cargar_config())
    p = c.archivo("AG-20")
    assert p.parent == BLOQUE / "02_System_prompts" and unicodedata.normalize("NFC", p.stem) == EVALUADOR.split("/")[1]
    assert '"ref_id":"RF-0046"' in c.texto("AG-20")


def test_ca7_los_prompts_mc_se_encuentran_por_nombre_en_02_y_no_en_el_historico():
    """El ejecutor no envía los prompts MC (el Motor es determinista: no hay agente MC en `NOMBRES_ALTERNATIVOS`); si algún día
    los busca por nombre, `buscar_versionado` da el de `02_System_prompts`, ya corregido."""
    assert not any(n.startswith("MC-") for nombres in NOMBRES_ALTERNATIVOS.values() for n in nombres)
    for prompt in PROMPTS_MC:
        base = prompt.split(" - Versión óptima")[0]
        p = buscar_versionado(BLOQUE / "02_System_prompts", base, ".md")
        assert p is not None and p.parent == BLOQUE / "02_System_prompts"
        assert "Catálogo V5.0" in p.read_text(encoding="utf-8")
