"""T-114 · Fase 3: los contratos CT-01 a CT-25 están congelados en goldens comparados byte a byte.

Criterios de aceptación en `.docs/tickets/T-114/README.md`. La regla de re-congelado, en `tests/goldens/README.md`.
"""
import copy
import importlib.util
import json
import re
import shutil

import goldens_ct as g
import jsonschema
import pytest

from bloque_a import contratos

CONTRATOS = [f"CT-{n:02d}" for n in range(1, 26)]


FECHA = "2026-06-05"   # la `AS_OF` de `conftest.py`


@pytest.fixture(scope="module")
def flujos(tmp_path_factory):
    """Los mensajes de los flujos simulados, una vez para todo el módulo."""
    return g.capturar_flujos(tmp_path_factory.mktemp("flujos"), FECHA)


@pytest.fixture(scope="module")
def generados(flujos):
    return g.generar(flujos=flujos)


@pytest.fixture(scope="module")
def a_mano():
    return g.leer_a_mano()


@pytest.fixture(scope="module")
def bateria():
    return g.leer_bateria()


def _congelado(nombre):
    return json.loads((g.CARPETA / nombre).read_text(encoding="utf-8"))


def _doc0():
    return next((g.BLOQUE / "01_Gobernanza").glob("Documento 0*.md")).read_text(encoding="utf-8")


def _anexo_b():
    doc0 = _doc0()
    return doc0[doc0.index("## ANEXO B."):doc0.index("## ANEXO C.")]


# ---------------------------------------------------------------- CA-1 · los goldens coinciden byte a byte
@pytest.mark.parametrize("nombre", g.GENERADOS)
def test_ca1_cada_golden_coincide_byte_a_byte(generados, nombre):
    assert (g.CARPETA / nombre).read_bytes() == generados[nombre].encode("utf-8"), (
        f"{nombre} difiere del golden; si el cambio de formato es deliberado, lea tests/goldens/README.md")


def test_ca1_no_sobra_ni_falta_ningun_fichero(generados):
    assert set(generados) == set(g.GENERADOS)
    assert g.comparar(generados) == []
    assert {p.name for p in g.CARPETA.iterdir()} == set(g.GENERADOS) | set(g.A_MANO) | set(g.DOCUMENTOS)


def test_ca1_un_fichero_de_mas_o_de_menos_se_detecta(generados, tmp_path):
    copia = tmp_path / "goldens"
    shutil.copytree(g.CARPETA, copia)
    (copia / "otro.json").write_text("{}\n", encoding="utf-8")
    assert g.comparar(generados, copia) == ["otro.json: fichero que no es un golden conocido"]
    (copia / "otro.json").unlink()
    (copia / "tablas_contratos.json").unlink()
    (copia / "README.md").unlink()
    assert g.comparar(generados, copia) == ["tablas_contratos.json: falta el golden", "README.md: falta"]


def test_ca1_los_goldens_tienen_la_forma_canonica():
    for nombre in g.GENERADOS + g.A_MANO:
        crudo = (g.CARPETA / nombre).read_text(encoding="utf-8")
        assert crudo == g.texto(json.loads(crudo)), nombre


# ---------------------------------------------------------------- CA-2 · un golden que no avisa no protege
def _mutar(obj):
    """Cambia la primera hoja que encuentra (un texto, un número, un booleano o un nulo)."""
    if isinstance(obj, dict):
        for k in sorted(obj):
            if isinstance(obj[k], (dict, list)):
                if _mutar(obj[k]):
                    return True
            else:
                obj[k] = "MUTADO"
                return True
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, (dict, list)):
                if _mutar(v):
                    return True
            else:
                obj[i] = "MUTADO"
                return True
    return False


@pytest.mark.parametrize("nombre", g.GENERADOS)
def test_ca2_mutar_un_campo_del_golden_hace_fallar_la_comparacion(generados, tmp_path, nombre):
    copia = tmp_path / "goldens"
    shutil.copytree(g.CARPETA, copia)
    assert g.comparar(generados, copia) == []
    mutado = json.loads((copia / nombre).read_text(encoding="utf-8"))
    assert _mutar(mutado)
    (copia / nombre).write_text(g.texto(mutado), encoding="utf-8")
    problemas = g.comparar(generados, copia)
    assert len(problemas) == 1 and problemas[0].startswith(f"{nombre}: difiere del golden congelado")


def test_ca2_un_solo_byte_de_diferencia_basta(generados, tmp_path):
    copia = tmp_path / "goldens"
    shutil.copytree(g.CARPETA, copia)
    ruta = copia / "tablas_contratos.json"
    ruta.write_bytes(ruta.read_bytes() + b"\n")
    assert [p.split(":")[0] for p in g.comparar(generados, copia)] == ["tablas_contratos.json"]


@pytest.mark.parametrize("tabla, cambio", [
    ("CANALES", lambda t: t.__setitem__("CT-01", [({"BROKER"}, {"AG-02"})])),
    ("CANALES", lambda t: t.pop("CT-22")),
    ("CANALES_V6", lambda t: t.__setitem__("CT-09", [({"AG-26"}, {"AG-13"})])),
    ("CAMPOS_MINIMOS", lambda t: t["CT-09"].remove("fecha_corte")),
    ("CAMPOS_MINIMOS", lambda t: t.__setitem__("CT-04", ["decisiones"])),
    ("CAMPOS_RETORNO", lambda t: t["CT-03"].append("escalado")),
    ("ESTADOS_ESPECIFICOS", lambda t: t.__setitem__("CT-25", ("PROVISTA", "DENEGADA"))),
    ("CAMPO_ESTADO", lambda t: t.__setitem__("CT-24", "estado")),
])
def test_ca2_cambiar_una_tabla_del_codigo_cambia_lo_generado(monkeypatch, tabla, cambio):
    antes = g.texto(g.tablas())
    assert antes == (g.CARPETA / "tablas_contratos.json").read_text(encoding="utf-8")
    mutada = copy.deepcopy(getattr(contratos, tabla))
    cambio(mutada)
    monkeypatch.setattr(contratos, tabla, mutada)
    assert g.texto(g.tablas()) != antes


@pytest.mark.parametrize("constante, valor", [("VERSION_CONTRATO", "5.2"), ("ESTADOS", ("COMPLETO", "PARCIAL", "RECHAZADO"))])
def test_ca2_cambiar_la_version_o_los_estados_cambia_lo_generado(monkeypatch, constante, valor):
    antes = g.texto(g.tablas())
    monkeypatch.setattr(contratos, constante, valor)
    assert g.texto(g.tablas()) != antes


@pytest.mark.parametrize("cambio", [
    lambda e: e["INFORME_CLASE"]["required"].remove("lagunas"),
    lambda e: e["CONSULTA"]["properties"]["ruta"]["enum"].append("N1"),
    lambda e: e["REDACCION"]["properties"]["frases_30s"].__setitem__("maxItems", 4),
    lambda e: e.pop("PLAN_MOTOR"),
    lambda e: e.__setitem__("NUEVO", {"type": "object"}),
])
def test_ca2_cambiar_un_esquema_del_codigo_cambia_lo_generado(monkeypatch, cambio):
    antes = g.texto(g.esquemas_respuestas())
    assert antes == (g.CARPETA / "esquemas_respuestas.json").read_text(encoding="utf-8")
    mutados = copy.deepcopy(contratos.ESQUEMAS)
    cambio(mutados)
    monkeypatch.setattr(contratos, "ESQUEMAS", mutados)
    assert g.texto(g.esquemas_respuestas()) != antes


def test_ca2_un_campo_minimo_nuevo_cambia_los_mensajes_y_las_divergencias(monkeypatch, a_mano, tmp_path):
    esquemas, ejemplos = a_mano
    fecha = "2026-06-05"
    assert g.mensajes_ejemplo(ejemplos, tmp_path / "a", fecha) == _congelado("mensajes_ejemplo.json")
    mutada = copy.deepcopy(contratos.CAMPOS_MINIMOS)
    mutada["CT-10"].append("tolerancia")
    monkeypatch.setattr(contratos, "CAMPOS_MINIMOS", mutada)
    mensajes = g.mensajes_ejemplo(ejemplos, tmp_path / "b", fecha)
    assert mensajes["CT-10.ENCARGO"] == {"rechazo": {"clase": "MensajeInvalido", "motivo": "CT-10: faltan campos mínimos ['tolerancia']"}}
    difieren = g.divergencias(esquemas, ejemplos, [], tmp_path / "c", fecha)
    assert difieren["por_contrato"]["CT-10.ENCARGO"]["el_ejecutor_exige_y_el_anexo_b_no_nombra"] == ["tolerancia"]
    assert "CT-10.ENCARGO" not in _congelado("divergencias_anexo_b.json")["por_contrato"]


# ---------------------------------------------------------------- CA-3 · los 25 contratos y solo ellos
def test_ca3_las_tablas_cubren_ct01_a_ct25():
    tablas = _congelado("tablas_contratos.json")
    assert sorted(tablas["canales"]) == CONTRATOS
    for nombre in ("canales_v6", "campos_minimos", "campos_retorno", "campo_estado", "estados_especificos"):
        assert set(tablas[nombre]) <= set(CONTRATOS), nombre
    assert all(par["emisores"] and par["receptores"] for pares in tablas["canales"].values() for par in pares)
    assert tablas["version_contrato"] == "5.1"


def test_ca3_son_los_contratos_del_documento_0():
    doc0 = next((g.BLOQUE / "01_Gobernanza").glob("Documento 0*.md")).read_text(encoding="utf-8")
    seccion = doc0[doc0.index("### 6.1 Contratos en vigor"):doc0.index("### 6.2 Reglas comunes")]
    assert re.findall(r"^\| (CT-[0-9]{2}) \|", seccion, flags=re.MULTILINE) == CONTRATOS
    assert sorted(contratos.CANALES) == CONTRATOS


# ---------------------------------------------------------------- CA-4 · esquemas derivados del Anexo B
CON_CAMPOS = [f"CT-{n:02d}" for n in (*range(1, 18), 19, 22, 23, 24, 25)]
# T-143: el Anexo B V5.2 da los campos de lo que el ejecutor emite por CT-16, CT-17 y CT-19; CT-18, CT-20 y CT-21 siguen en
# los prompts de sistema
SIN_CAMPOS = ["CT-18", "CT-20", "CT-21"]


def test_ca4_hay_esquema_derivado_para_cada_contrato_con_campos_en_el_anexo_b(a_mano):
    esquemas, ejemplos = a_mano
    assert sorted({clave.split(".")[0] for clave in esquemas}) == CON_CAMPOS
    assert set(esquemas) == set(ejemplos)
    assert all(clave.split(".")[1] in ("ENCARGO", "RETORNO") for clave in esquemas)
    assert g.sin_campos_en_anexo_b(esquemas) == SIN_CAMPOS
    assert _congelado("divergencias_anexo_b.json")["contratos_sin_campos_en_el_anexo_b"] == SIN_CAMPOS


def test_ca4_ct22_lleva_tipo_o_tipo_aviso_y_ct18_ct20_ct21_ningun_campo(a_mano):
    """QA r01, H-02, y T-143: el Anexo B V5.2 dice qué valores lleva `tipo` y cuáles `tipo_aviso` (los dos campos que el
    ejecutor emite), uno de los dos por aviso, sin lista cerrada. CT-18, CT-20 y CT-21 no nombran ningún campo."""
    esquemas, ejemplos = a_mano
    parrafos = g.parrafos_anexo_b()
    parrafo = parrafos["CT-22"]
    assert re.findall(r"`([^`]+)`", parrafo) == ["tipo", "tipo_aviso"]
    assert "`tipo` (DECISIONES_BROKER o PREGUNTA_REPETIDA) o `tipo_aviso` (CONSULTA_RECURRENTE o DECISION_SEGUIMIENTO)" in parrafo
    assert parrafos["CT-20"] == parrafos["CT-21"] and all(not re.findall(r"`([^`]+)`", parrafos[ct]) for ct in SIN_CAMPOS)
    esquema = esquemas["CT-22.ENCARGO"]
    assert {k: v for k, v in esquema.items() if k not in ("$comment", "$schema")} == {
        "type": "object", "required": [], "oneOf": [{"required": ["tipo"]}, {"required": ["tipo_aviso"]}],
        "properties": {"tipo": {"examples": ["DECISIONES_BROKER", "PREGUNTA_REPETIDA"]},
                       "tipo_aviso": {"examples": ["CONSULTA_RECURRENTE", "DECISION_SEGUIMIENTO"]}}}
    assert "CT-22.RETORNO" not in esquemas
    validador = jsonschema.Draft202012Validator(esquema)
    assert validador.is_valid(ejemplos["CT-22.ENCARGO"]) and validador.is_valid({"tipo_aviso": "CONSULTA_RECURRENTE"})
    assert not validador.is_valid({}) and not validador.is_valid({"tipo": "PREGUNTA_REPETIDA", "tipo_aviso": "CONSULTA_RECURRENTE"})


def test_ca4_cada_esquema_es_valido_lleva_la_marca_y_su_ejemplo_lo_cumple(a_mano):
    esquemas, ejemplos = a_mano
    for clave, esquema in esquemas.items():
        jsonschema.Draft202012Validator.check_schema(esquema)
        assert esquema["$comment"].startswith(g.MARCA), clave
        assert esquema["type"] == "object" and "additionalProperties" not in esquema, clave
        assert set(esquema["required"]) <= set(esquema["properties"]), clave
        jsonschema.Draft202012Validator(esquema).validate(ejemplos[clave])


def test_ca4_un_ejemplo_sin_un_campo_obligatorio_o_fuera_de_lista_no_cumple(a_mano):
    esquemas, ejemplos = a_mano
    comprobados = 0
    for clave, esquema in esquemas.items():
        validador = jsonschema.Draft202012Validator(esquema)
        for campo in esquema["required"]:
            recortado = {k: v for k, v in ejemplos[clave].items() if k != campo}
            assert not validador.is_valid(recortado), (clave, campo)
            comprobados += 1
        for campo, prop in esquema["properties"].items():
            if "enum" in prop and campo in ejemplos[clave]:
                assert not validador.is_valid({**ejemplos[clave], campo: "FUERA_DE_LISTA"}), (clave, campo)
                comprobados += 1
    # T-143: con el Anexo B V5.2 hay menos campos obligatorios (186 → 99); el número exacto hace que se note un campo que deja
    # de ser obligatorio o una lista que deja de estar cerrada en un esquema derivado
    assert comprobados == 99


def test_ca4_el_seguimiento_exige_seg_id_y_opp_id_en_ct05(a_mano):
    esquemas, ejemplos = a_mano
    validador = jsonschema.Draft202012Validator(esquemas["CT-05.ENCARGO"])
    seguimiento = {**ejemplos["CT-05.ENCARGO"], "tipo": "SEGUIMIENTO"}
    assert not validador.is_valid(seguimiento)
    assert validador.is_valid({**seguimiento, "seg_id": "SEG-2026-0001", "opp_id": "OPP-2026-0007"})


def test_ca4_el_contenido_de_ct23_solo_va_en_entrante(a_mano):
    """QA r01, H-05: «contenido: solo en ENTRANTE» se codifica con condición, como `seg_id` y `opp_id` de CT-05."""
    esquemas, ejemplos = a_mano
    validador = jsonschema.Draft202012Validator(esquemas["CT-23.ENCARGO"])
    saliente = ejemplos["CT-23.ENCARGO"]
    assert saliente["sentido"] == "SALIENTE" and "contenido" not in saliente and validador.is_valid(saliente)
    assert not validador.is_valid({**saliente, "contenido": "Texto."})
    entrante = {**saliente, "sentido": "ENTRANTE"}
    assert not validador.is_valid(entrante)
    assert validador.is_valid({**entrante, "contenido": "El usuario prefiere excluir tabaco."})


def test_ca4_los_retornos_declaran_que_el_anexo_b_no_describe_el_retorno_rechazado(a_mano):
    """QA r01, H-05: el Anexo B V5.1 no decía qué campos lleva un retorno RECHAZADO o SIN_RESULTADO; el V5.2 lo dice (estado
    común y motivo). Los esquemas de retorno describen el retorno con resultado, y así se declara en cada uno y en el README."""
    esquemas, _ = a_mano
    retornos = [clave for clave in esquemas if clave.endswith(".RETORNO")]
    assert len(retornos) == 18   # T-143: más CT-19, (r02) CT-15 y (r03) CT-17
    for clave in retornos:
        assert "RECHAZADO" in esquemas[clave]["$comment"] and "no sirve para juzgar los otros" in esquemas[clave]["$comment"], clave
        assert "if" not in esquemas[clave], clave
    assert "ACLARACION_REQUERIDA" in esquemas["CT-09.RETORNO"]["$comment"] and "ACLARACION_REQUERIDA" in g.parrafos_anexo_b()["CT-09"]
    assert "Un retorno RECHAZADO o SIN_RESULTADO lleva el estado común y el motivo (6.2.6)" in _anexo_b()
    assert "RECHAZADO o SIN_RESULTADO" in (g.CARPETA / "README.md").read_text(encoding="utf-8")


def test_ca4_los_campos_de_cada_esquema_estan_en_el_parrafo_de_su_contrato(a_mano):
    """Nada inventado (QA r01, H-06): cada campo de un esquema derivado, anidados incluidos, aparece tal cual en el párrafo
    del Anexo B que habla de su contrato, no en cualquier parte del Anexo B."""
    esquemas, _ = a_mano
    parrafos = g.parrafos_anexo_b()
    assert sorted(parrafos) == CONTRATOS
    assert parrafos["CT-07"] == parrafos["CT-08"] and "CT-09 Cálculo" in parrafos["CT-09"] and "CT-10" not in parrafos["CT-09"]
    assert g.campos_fuera_de_su_parrafo(esquemas, parrafos) == []


def test_ca4_un_campo_de_otro_contrato_se_detecta(a_mano):
    """La comprobación anterior falla si un campo de CT-09 se pone por error en CT-10, o un campo anidado en otro contrato."""
    esquemas, _ = a_mano
    parrafos = g.parrafos_anexo_b()
    cambiados = copy.deepcopy(esquemas)
    cambiados["CT-10.ENCARGO"]["properties"]["semilla"] = {}
    cambiados["CT-24.ENCARGO"]["properties"]["alcance"] = {"type": "object", "properties": {"regiones": {}}}
    cambiados["CT-13.RETORNO"]["properties"]["resultados"] = {"items": {"properties": {"cns_id": {}}}}
    assert g.campos_fuera_de_su_parrafo(cambiados, parrafos) == [("CT-10.ENCARGO", "semilla"), ("CT-13.RETORNO", "cns_id"),
                                                                 ("CT-24.ENCARGO", "alcance"), ("CT-24.ENCARGO", "regiones")]
    anexo = _anexo_b()
    assert all(f"`{campo}`" in anexo or f'"{campo}"' in anexo for campo in ("semilla", "cns_id", "alcance", "regiones"))   # la prueba de la r01 no los veía


# ---------------------------------------------------------------- CA-5 · los ejemplos publicados cumplen sus esquemas
def _publicado(nombre):
    plantillas = g.BLOQUE / "06_Plantillas_entregables"
    esquema = json.loads(next(plantillas.glob(f"Esquema JSON - {nombre}*.json")).read_text(encoding="utf-8"))
    ejemplo = json.loads(next(plantillas.glob(f"Ejemplo - {nombre}*.json")).read_text(encoding="utf-8"))
    validador = jsonschema.validators.validator_for(esquema)
    validador.check_schema(esquema)
    return validador(esquema), ejemplo


def test_ca5_el_ejemplo_del_paquete_cumple_su_esquema_publicado():
    validador, ejemplo = _publicado("Paquete de oportunidades")
    assert list(validador.iter_errors(ejemplo)) == []


def test_ca5_el_ejemplo_de_seguimiento_cumple_su_esquema_salvo_la_clave_de_aviso():
    """INC-T114-02: el ejemplo publicado lleva `x_aviso_ejemplo` y el esquema V5.1 no admite claves de más en la raíz."""
    validador, ejemplo = _publicado("Informe de seguimiento de opción")
    errores = [(list(e.absolute_path), e.validator, e.message) for e in validador.iter_errors(ejemplo)]
    assert errores == [([], "additionalProperties", "Additional properties are not allowed ('x_aviso_ejemplo' was unexpected)")]
    assert list(validador.iter_errors({k: v for k, v in ejemplo.items() if k != "x_aviso_ejemplo"})) == []


# ---------------------------------------------------------------- CA-6 · re-congelar solo es deliberado
def test_ca6_recongelar_sin_motivo_falla_y_no_escribe(generados, tmp_path, capsys):
    copia = tmp_path / "goldens"
    shutil.copytree(g.CARPETA, copia)
    (copia / "tablas_contratos.json").write_text("{}\n", encoding="utf-8")
    antes = {p.name: p.read_bytes() for p in copia.iterdir()}
    for motivo in ("", "   ", None):
        with pytest.raises(ValueError, match="exige un motivo"):
            g.recongelar(motivo, copia, generados)
    assert {p.name: p.read_bytes() for p in copia.iterdir()} == antes
    assert g.main(["--update"]) == 2 and g.main(["--update", "--motivo", "  "]) == 2
    assert "exige un motivo" in capsys.readouterr().err
    assert g.comparar(generados) == []


def test_ca6_recongelar_con_motivo_escribe_y_registra(generados, tmp_path):
    copia = tmp_path / "goldens"
    shutil.copytree(g.CARPETA, copia)
    registro = (copia / "REGISTRO.md").read_text(encoding="utf-8")
    assert g.recongelar("sin cambios", copia, generados) == []
    assert (copia / "REGISTRO.md").read_text(encoding="utf-8") == registro
    (copia / "huellas.json").write_text("{}\n", encoding="utf-8")
    (copia / "tablas_contratos.json").unlink()
    assert g.recongelar("  prueba de\nre-congelado ", copia, generados, hoy="2026-11-13") == ["huellas.json", "tablas_contratos.json"]
    assert g.comparar(generados, copia) == []
    assert (copia / "REGISTRO.md").read_text(encoding="utf-8") == (
        registro + "- 2026-11-13 · huellas.json, tablas_contratos.json · prueba de re-congelado\n")


def test_ca6_el_registro_y_el_readme_dicen_la_regla():
    leeme = (g.CARPETA / "README.md").read_text(encoding="utf-8")
    assert "Re-congelar solo es deliberado" in leeme and "--update --motivo" in leeme and "el mismo commit" in leeme
    lineas = [x for x in (g.CARPETA / "REGISTRO.md").read_text(encoding="utf-8").splitlines() if x.startswith("- ")]
    assert lineas and all(re.fullmatch(r"- [0-9]{4}-[0-9]{2}-[0-9]{2} · [a-z_., ]+\.json · \S.*", x) for x in lineas)


# ---------------------------------------------------------------- CA-7 · las diferencias con el Anexo B, congeladas
def test_ca7_una_divergencia_nueva_no_coincide_con_el_golden(a_mano, tmp_path):
    esquemas, ejemplos = a_mano
    congelado = _congelado("divergencias_anexo_b.json")
    sin_ciclo = g.divergencias(esquemas, ejemplos, [], tmp_path / "a", "2026-06-05")
    assert sin_ciclo["por_contrato"] == congelado["por_contrato"]
    endurecidos = copy.deepcopy(esquemas)
    endurecidos["CT-10.ENCARGO"]["required"].append("tolerancia")
    endurecidos["CT-10.ENCARGO"]["properties"]["tolerancia"] = {}
    con_ejemplo = {**ejemplos, "CT-10.ENCARGO": {**ejemplos["CT-10.ENCARGO"], "tolerancia": 0}}
    nuevas = g.divergencias(endurecidos, con_ejemplo, [], tmp_path / "b", "2026-06-05")
    assert nuevas["por_contrato"]["CT-10.ENCARGO"] == {"el_ejecutor_admite_que_falte": ["tolerancia"]}
    assert nuevas["por_contrato"] != congelado["por_contrato"]


def test_ca7_un_mensaje_de_un_flujo_fuera_del_anexo_b_aparece(a_mano, tmp_path):
    esquemas, ejemplos = a_mano
    msg = {"contrato": "CT-09", "tipo_mensaje": "ENCARGO", **ejemplos["CT-09.ENCARGO"], "modo": "OTRO"}
    del msg["semilla"]
    difieren = g.divergencias(esquemas, ejemplos, [msg], tmp_path, "2026-06-05")
    assert difieren["mensajes_de_los_flujos_simulados_que_no_cumplen_el_anexo_b"] == {
        "CT-09.ENCARGO": ["(raíz): 'semilla' is a required property", "modo: enum ['SYNC_CALC', 'ASYNC_CALC']"]}
    assert difieren["valores_que_el_anexo_b_nombra_en_un_campo_y_el_ejecutor_emite_en_otro"] == {}


def test_ca7_el_tipo_de_ct22_coincide_con_el_anexo_b_y_vuelve_a_diferir_si_cambia(a_mano, flujos, tmp_path):
    """QA r01, H-02, y T-143: el ejecutor emite DECISIONES_BROKER y PREGUNTA_REPETIDA en `tipo`, y CONSULTA_RECURRENTE y
    DECISION_SEGUIMIENTO en `tipo_aviso`. Hasta la V5.1 el Anexo B ponía los cuatro en `tipo` (la diferencia estaba
    congelada); el V5.2 dice qué campo lleva cada valor y la diferencia desaparece. Si el ejecutor volviera a emitirlos en
    `tipo`, como decía la V5.1, o un aviso llevara los dos campos o ninguno, la diferencia volvería."""
    esquemas, ejemplos = a_mano
    avisos = [m for m in g.todos_los_mensajes(flujos) if m["contrato"] == "CT-22"]
    assert sorted({(m.get("tipo"), m.get("tipo_aviso")) for m in avisos}, key=str) == [
        ("DECISIONES_BROKER", None), ("PREGUNTA_REPETIDA", None), (None, "CONSULTA_RECURRENTE"), (None, "DECISION_SEGUIMIENTO")]
    congelado = _congelado("divergencias_anexo_b.json")
    assert "CT-22.ENCARGO" not in congelado["valores_que_el_anexo_b_nombra_en_un_campo_y_el_ejecutor_emite_en_otro"]
    assert "CT-22.ENCARGO" not in congelado["mensajes_de_los_flujos_simulados_que_no_cumplen_el_anexo_b"]
    assert "CT-22.ENCARGO" not in congelado["por_contrato"]
    medido = g.divergencias(esquemas, ejemplos, avisos, tmp_path / "a", FECHA)
    assert medido["valores_que_el_anexo_b_nombra_en_un_campo_y_el_ejecutor_emite_en_otro"] == {}
    assert medido["mensajes_de_los_flujos_simulados_que_no_cumplen_el_anexo_b"] == {}
    # como decía la V5.1: los cuatro en `tipo`
    en_tipo = [{**{k: v for k, v in m.items() if k != "tipo_aviso"}, "tipo": m["tipo_aviso"]} if "tipo_aviso" in m else m for m in avisos]
    vuelve = g.divergencias(esquemas, ejemplos, en_tipo, tmp_path / "b", FECHA)
    assert vuelve["valores_que_el_anexo_b_nombra_en_un_campo_y_el_ejecutor_emite_en_otro"]["CT-22.ENCARGO"] == [
        {"campo_del_anexo_b": "tipo_aviso", "campo_del_ejecutor": "tipo", "valor": "CONSULTA_RECURRENTE"},
        {"campo_del_anexo_b": "tipo_aviso", "campo_del_ejecutor": "tipo", "valor": "DECISION_SEGUIMIENTO"}]
    # los dos campos o ninguno
    for cambio in (lambda m: {**m, "tipo": "X", "tipo_aviso": "Y"}, lambda m: {k: v for k, v in m.items() if k not in ("tipo", "tipo_aviso")}):
        roto = g.divergencias(esquemas, ejemplos, [cambio(avisos[0])], tmp_path / "c", FECHA)
        assert list(roto["mensajes_de_los_flujos_simulados_que_no_cumplen_el_anexo_b"]["CT-22.ENCARGO"]) == ["(raíz): oneOf [{'required': ['tipo']}, {'required': ['tipo_aviso']}]"]
    incidencias = (g.BLOQUE.parent / "docs" / "incidencias.md").read_text(encoding="utf-8")
    inc = incidencias[incidencias.index("**INC-T114-01"):incidencias.index("**INC-T114-02")]
    assert "`tipo_aviso`" in inc and "CONSULTA_RECURRENTE" in inc and "DECISION_SEGUIMIENTO" in inc and "CT-16 a CT-21" in inc
    assert "CT-16 a CT-22:** el Anexo B no da sus campos" not in inc


def test_ca7_las_divergencias_estan_en_las_incidencias_y_en_la_deuda():
    raiz = g.BLOQUE.parent
    assert "INC-T114-01" in (raiz / "docs" / "incidencias.md").read_text(encoding="utf-8")
    deuda = (raiz / "sistema_global" / "seguimiento" / "Deuda_tecnica_y_pendientes_del_operador.md").read_text(encoding="utf-8")
    assert "| T-114 |" in deuda and "INC-T114-01" in deuda


# ---------------------------------------------------------------- CA-8 · generar dos veces da lo mismo
def test_ca8_dos_generaciones_seguidas_dan_el_mismo_texto(generados):
    """La segunda generación vuelve a ejecutar todos los flujos (no reutiliza los del módulo)."""
    assert g.generar() == generados


def test_ca8_las_formas_no_dependen_del_orden_de_los_mensajes(flujos, a_mano):
    assert sum(len(v) for v in flujos.values()) > 150
    al_reves = {nombre: mensajes[::-1] for nombre, mensajes in flujos.items()}
    assert g.formas(flujos, a_mano[0]) == g.formas(al_reves, a_mano[0]) == _congelado("formas_flujos_mock.json")


# ---------------------------------------------------------------- huellas de lo que no se genera
def test_las_huellas_cubren_el_documento_0_los_esquemas_publicados_y_lo_escrito_a_mano(tmp_path):
    huellas = _congelado("huellas.json")
    assert sorted(huellas) == sorted([
        "01_Gobernanza/Documento 0 - Protocolo maestro del Bloque A - Versión óptima V5.3.md",   # T-143; V5.3 desde T-166
        "06_Plantillas_entregables/Esquema JSON - Informe de seguimiento de opción - V5.1.json",
        "06_Plantillas_entregables/Esquema JSON - Paquete de oportunidades - V5.0.json",
        "goldens/anexo_b_ejemplos.json", "goldens/anexo_b_esquemas.json", "goldens/bateria_mensajes.json"])
    copia = tmp_path / "goldens"
    shutil.copytree(g.CARPETA, copia)
    assert g.huellas(copia) == huellas
    ruta = copia / "anexo_b_esquemas.json"
    ruta.write_text(ruta.read_text(encoding="utf-8").replace('"INMEDIATA"', '"URGENTE"'), encoding="utf-8")
    assert g.huellas(copia) != huellas
    shutil.copy(g.CARPETA / "anexo_b_esquemas.json", ruta)
    ruta = copia / "bateria_mensajes.json"
    ruta.write_text(ruta.read_text(encoding="utf-8").replace('"espera": "RECHAZADO"', '"espera": "ADMITIDO"', 1), encoding="utf-8")
    assert g.huellas(copia) != huellas


# ---------------------------------------------------------------- los mensajes de ejemplo, uno a uno
def test_los_mensajes_de_ejemplo_llevan_el_sobre_comun_y_el_cuerpo_intacto(a_mano):
    _, ejemplos = a_mano
    mensajes = _congelado("mensajes_ejemplo.json")
    assert set(mensajes) == set(ejemplos)
    rechazados = sorted(k for k, v in mensajes.items() if "rechazo" in v)
    assert rechazados == []   # T-143: el Anexo B V5.2 describe CT-11, CT-12 y CT-13 como lotes; hasta la V5.1 se rechazaban
    for clave, v in mensajes.items():
        if "rechazo" in v:
            continue
        msg, (ct, sentido) = v["mensaje"], clave.split(".")
        assert msg["contrato"] == ct and msg["tipo_mensaje"] == sentido and msg["version_contrato"] == "5.1"
        assert re.fullmatch(r"MSG-2026-[0-9]{6}", msg["msg_id"]) and msg["timestamp"].startswith("2026-06-05T06:")
        assert contratos.canal_permitido(ct, msg["emisor"], msg["receptor"])
        assert ("presupuesto" in msg) == (sentido == "ENCARGO") and ("consumo" in msg) == (sentido == "RETORNO")
        campo_estado = contratos.CAMPO_ESTADO.get(ct) if sentido == "RETORNO" else None
        for campo, valor in ejemplos[clave].items():
            if campo == "estado" and campo_estado:   # §6.2.6: el estado del objeto pasa a su campo propio
                assert msg[campo_estado] == valor and msg["estado"] == "COMPLETO"
            elif valor is not None or campo in msg:
                assert msg[campo] == valor, (clave, campo)


# ================================================================ QA r01, H-01 a · aceptaciones y rechazos de la mensajería
def test_h01_la_bateria_cubre_los_25_contratos_con_admitidos_y_rechazados(bateria):
    congelado = _congelado("aceptaciones_rechazos.json")
    assert set(congelado["casos"]) == set(bateria) and len(bateria) >= 350
    assert congelado["no_coinciden_con_lo_que_espera_la_bateria"] == []
    assert all(congelado["casos"][n]["resultado"] == caso["espera"] for n, caso in bateria.items())
    por_contrato = {ct: {"ADMITIDO": 0, "RECHAZADO": 0} for ct in CONTRATOS}
    for nombre, caso in bateria.items():
        assert set(caso) <= g.CAMPOS_CASO and caso["que"].strip(), nombre
        if nombre.split("/")[0] in por_contrato:
            por_contrato[nombre.split("/")[0]][caso["espera"]] += 1
    assert all(n["ADMITIDO"] >= 1 and n["RECHAZADO"] >= 1 for n in por_contrato.values()), por_contrato
    assert {v["clase"] for v in congelado["casos"].values() if v["resultado"] == "RECHAZADO"} == {"MensajeInvalido", "CanalNoPrevisto", "DatosSensibles"}
    assert congelado["claves_de_la_traza_de_mensajes"] == ["contrato", "emisor", "msg_id", "receptor", "tipo_mensaje"]


def test_h01_las_reglas_de_valor_estan_en_la_bateria():
    """Una a una, las reglas que la r01 encontró sin congelar: cada una tiene un caso admitido y otro rechazado."""
    casos = _congelado("aceptaciones_rechazos.json")["casos"]

    def motivo(nombre):
        return casos[nombre]["motivo"]

    def admitido(nombre):
        return casos[nombre]["resultado"] == "ADMITIDO"

    # listas de CT-01 (tipo, prioridad, horizontes) y `alcance`
    assert all(admitido(f"CT-01/tipo_{t}") for t in ("ad_hoc", "profundizacion", "periodico"))
    assert motivo("CT-01/tipo_no_admitido_seguimiento") == motivo("CT-01/prioridad_no_admitida_urgente") == "CT-01: tipo o prioridad no admitidos"
    assert all(admitido(f"CT-01/horizonte_h{n}") for n in range(1, 6)) and admitido("CT-01/horizontes_los_cinco")
    assert motivo("CT-01/horizontes_no_validos_h6") == motivo("CT-01/alcance_no_valido_texto") == "CT-01: alcance u horizontes no válidos"
    # la entrega exige G3 aprobado
    assert admitido("CT-02/entrega_apta") and admitido("CT-02/entrega_apta_con_advertencias")
    assert motivo("CT-02/entrega_con_g3_bloqueado") == "CT-02: se requiere una entrega G3 aprobada con rutas y resumen"
    # contratos exentos de `run_id` y `query_id`: los ocho, ni uno más
    exentos = sorted(ct for ct in CONTRATOS if admitido(f"{ct}/sin_run_id_ni_query_id"))
    assert exentos == ["CT-01", "CT-03", "CT-04", "CT-18", "CT-21", "CT-23", "CT-24", "CT-25"]
    assert all(motivo(f"{ct}/sin_run_id_ni_query_id") == "Falta run_id o query_id" for ct in CONTRATOS if ct not in exentos)
    # tipos de mensaje y versión
    assert motivo("sobre/tipo_mensaje_acuse") == motivo("sobre/version_anterior") == "Versión o tipo de mensaje no admitido"
    # estado común del retorno y estado propio de CT-23 a CT-25
    assert motivo("sobre/retorno_estado_fuera_de_lista") == "Estado de retorno no válido 'HECHO'"
    for ct, campo in contratos.CAMPO_ESTADO.items():
        for estado in contratos.ESTADOS_ESPECIFICOS[ct]:
            msg = casos[f"{ct}/retorno_estado_propio_{estado.lower()}"]["mensaje"]
            assert msg[campo] == estado and msg["estado"] == "COMPLETO"
        assert motivo(f"{ct}/retorno_estado_propio_fuera_de_lista") == f"{campo} no válido"
        assert motivo(f"{ct}/retorno_con_los_dos_estados_contradictorios") == f"{ct}: estados de objeto contradictorios"
    # campos reservados del sobre
    for campo in ("msg_id", "contrato", "version_contrato", "emisor", "receptor", "timestamp", "tipo_mensaje", "run_id", "query_id",
                  "presupuesto", "consumo", "estado"):
        assert motivo(f"sobre/cuerpo_cambia_{campo}") == f"No se puede cambiar {campo} desde el cuerpo"
    assert admitido("sobre/cuerpo_repite_emisor") and "emisor" in casos["sobre/cuerpo_repite_emisor"]["mensaje"]
    # `msg_id` externo del Broker
    assert casos["CT-01/msg_id_del_broker"]["mensaje"]["msg_id"] == "MSG-BRK-2026-000123"
    assert motivo("CT-01/msg_id_del_broker_no_valido_con_la_forma_del_bloque") == "msg_id externo no válido (formato MSG-BRK-AAAA-NNNNNN)"
    # datos protegidos: se rechaza sin copiar el dato al motivo
    for nombre in ("sobre/dato_personal_en_el_cuerpo", "sobre/cuenta_bancaria_anidada", "CT-25/retorno_con_dato_protegido"):
        assert casos[nombre]["clase"] == "DatosSensibles" and re.fullmatch(r"Mensaje MSG-2026-000001 con datos protegidos en \['[a-z_]+'\]", motivo(nombre))
    # canales: cerrados, y los del V6 solo con el diseño V6
    assert casos["CT-06/analistas_entre_si"]["clase"] == "CanalNoPrevisto"
    assert admitido("v6/CT-15_analizador_al_sintetizador_con_v6") and not admitido("v6/CT-15_analizador_al_sintetizador_con_v5")


def test_h01_un_caso_mal_escrito_es_un_error_y_no_un_rechazo(a_mano, tmp_path):
    _, ejemplos = a_mano
    base = {"que": "x", "espera": "RECHAZADO", "base": "CT-10.ENCARGO"}
    for malo in ({**base, "campo_nuevo": 1}, {**base, "espera": "QUIZA"}, {**base, "cuerpo": {}}, {"que": "x", "espera": "ADMITIDO"},
                 {**base, "via": "otra"}, {**base, "via": "validar", "pon": {"contrato": "CT-09"}}):
        with pytest.raises(ValueError):
            g.aceptaciones({"malo": malo}, ejemplos, tmp_path, FECHA)
    with pytest.raises(KeyError):
        g.aceptaciones({"malo": {**base, "quita": ["no_esta"]}}, ejemplos, tmp_path, FECHA)
    cambiado = g.aceptaciones({"caso": {**base, "espera": "ADMITIDO", "pon": {"contrato": "CT-09"}}}, ejemplos, tmp_path, FECHA)
    assert cambiado["no_coinciden_con_lo_que_espera_la_bateria"] == ["caso"]


# Cambios de una línea en `contratos.py` que la r01 vio pasar sin que saltara ningún golden (y casi todos, ninguna prueba).
# Cada uno se aplica a una copia del módulo: los casos de la batería que tocan esa regla (los que empiezan por el prefijo;
# no se pasa la batería entera para no alargar la suite) tienen que dar otro resultado. Si el texto original ya no está en
# `contratos.py`, la prueba falla y hay que actualizar el mutante (el código cambió).
MUTANTES_DE_LA_MENSAJERIA = [
    ("M18 · la traza pierde tipo_mensaje", "sobre/encargo", 'for k in ("msg_id", "contrato", "emisor", "receptor", "tipo_mensaje")})', 'for k in ("msg_id", "contrato", "emisor", "receptor")})'),
    ("M20 · el cuerpo puede pisar campos reservados", "sobre/cuerpo_cambia",
     '            if cuerpo[campo] != msg.get(campo):\n                raise MensajeInvalido(f"No se puede cambiar {campo} desde el cuerpo")\n            cuerpo.pop(campo)',
     '            pass'),
    ("M21 · otro formato del msg_id del Broker", "CT-01/msg_id", 'r"MSG-BRK-[0-9]{4}-[0-9]{1,12}"', 'r"MSG-EXT-[0-9]{4}-[0-9]{1,12}"'),
    ("M22 · estados de objeto contradictorios admitidos", "CT-23/retorno_con", 'if campo in cuerpo and cuerpo[campo] != antiguo:', 'if False:'),
    ("M23 · CT-01 admite tipo SEGUIMIENTO", "CT-01/tipo", 'not in ("AD_HOC", "PROFUNDIZACION", "PERIODICO")', 'not in ("AD_HOC", "PROFUNDIZACION", "PERIODICO", "SEGUIMIENTO")'),
    ("M24 · CT-01 admite prioridad URGENTE", "CT-01/prioridad", 'not in ("ALTA", "NORMAL", "BAJA")', 'not in ("ALTA", "NORMAL", "BAJA", "URGENTE")'),
    ("M25 · CT-01 admite el horizonte H6", "CT-01/horizonte", 'h not in ("H1", "H2", "H3", "H4", "H5")', 'h not in ("H1", "H2", "H3", "H4", "H5", "H6")'),
    ("M26 · CT-01 pierde el horizonte H5", "CT-01/horizonte", 'h not in ("H1", "H2", "H3", "H4", "H5")', 'h not in ("H1", "H2", "H3", "H4")'),
    ("M27 · CT-02 admite una entrega con G3 BLOQUEADO", "CT-02/entrega", 'not in ("APTO", "APTO_CON_ADVERTENCIAS")):', 'not in ("APTO", "APTO_CON_ADVERTENCIAS", "BLOQUEADO")):'),
    ("M28 · CT-05 exento de run_id", "CT-05/", '("CT-01", "CT-03", "CT-04", "CT-18", "CT-21", "CT-23", "CT-24", "CT-25")',
     '("CT-01", "CT-03", "CT-04", "CT-05", "CT-18", "CT-21", "CT-23", "CT-24", "CT-25")'),
    ("M29 · CT-23 deja de estar exento de run_id", "CT-23/sin_run", '("CT-01", "CT-03", "CT-04", "CT-18", "CT-21", "CT-23", "CT-24", "CT-25")',
     '("CT-01", "CT-03", "CT-04", "CT-18", "CT-21", "CT-24", "CT-25")'),
    ("M30 · no se comprueban los datos protegidos", "sobre/dato", '        if cred:\n            campos', '        if False:\n            campos'),
    ("M31 · no se comprueba el estado propio de CT-23 a CT-25", "CT-24/retorno_estado", 'if msg.get(campo) not in ESTADOS_ESPECIFICOS[msg["contrato"]]:', 'if False:'),
    ("M32 · no se comprueba el estado del retorno", "sobre/retorno_estado", 'if tipo != "ENCARGO" and msg.get("estado") not in ESTADOS:', 'if False:'),
    ("M33 · no se comprueba la versión", "sobre/version", 'if msg["version_contrato"] != VERSION_CONTRATO or msg.get("tipo_mensaje")', 'if msg.get("tipo_mensaje")'),
    ("M38 · se admite un tercer tipo de mensaje", "sobre/tipo_mensaje", 'msg.get("tipo_mensaje") not in ("ENCARGO", "RETORNO")', 'msg.get("tipo_mensaje") not in ("ENCARGO", "RETORNO", "ACUSE")'),
    ("M39 · CT-01 no retira el msg_id externo del cuerpo", "CT-01/msg_id", 'if contrato == "CT-01" and emisor == "BROKER" else None', 'if contrato == "CT-01" and emisor == "NADIE" else None'),
    ("M40 · CT-01 no comprueba que alcance sea un objeto", "CT-01/alcance", 'if not isinstance(msg["alcance"], dict) or not isinstance', 'if not isinstance'),
    ("un campo reservado menos (run_id)", "sobre/cuerpo_cambia_run_id", '"tipo_mensaje", "run_id", "query_id", "presupuesto", "consumo", "estado"}', '"tipo_mensaje", "query_id", "presupuesto", "consumo", "estado"}'),
    ("la normalización del estado propio se aplica también al encargo", "CT-25/encargo_con_estado", 'if tipo_mensaje == "RETORNO" and contrato in CAMPO_ESTADO:', 'if contrato in CAMPO_ESTADO:'),
    ("CT-02 no exige que entregables sea un objeto", "CT-02/entrega", 'not isinstance(msg.get("entregables"), dict) or not isinstance(msg.get("resumen"), dict)', 'not isinstance(msg.get("resumen"), dict)'),
    ("los canales del V6 se abren siempre", "v6/", '+ (CANALES_V6.get(contrato, []) if v6 else [])', '+ CANALES_V6.get(contrato, [])'),
]


def _contratos_cambiado(carpeta, viejo, nuevo):
    """Una copia de `contratos.py` con un cambio de texto, cargada como módulo aparte. El paquete no se toca."""
    fuente = (g.RAIZ / "bloque_a" / "contratos.py").read_text(encoding="utf-8")
    assert fuente.count(viejo) == 1, f"el mutante ya no se puede aplicar a contratos.py: actualícelo ({viejo[:60]!r})"
    ruta = carpeta / "contratos_cambiado_t114.py"
    ruta.write_text(fuente.replace(viejo, nuevo), encoding="utf-8")
    spec = importlib.util.spec_from_file_location("contratos_cambiado_t114", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def test_h01_la_copia_sin_cambios_de_contratos_da_el_golden(a_mano, bateria, tmp_path):
    """El control de la prueba de mutantes: la misma copia en memoria, sin cambiar nada, da exactamente el golden."""
    modulo = _contratos_cambiado(tmp_path, "VERSION_CONTRATO = \"5.1\"", "VERSION_CONTRATO = \"5.1\"")
    assert modulo is not contratos and modulo.Mensajeria is not contratos.Mensajeria
    assert g.aceptaciones(bateria, a_mano[1], tmp_path, FECHA, modulo) == _congelado("aceptaciones_rechazos.json")


@pytest.mark.parametrize("prefijo, viejo, nuevo", [m[1:] for m in MUTANTES_DE_LA_MENSAJERIA], ids=[m[0] for m in MUTANTES_DE_LA_MENSAJERIA])
def test_h01_un_cambio_en_las_reglas_de_la_mensajeria_cambia_el_golden(a_mano, bateria, tmp_path, prefijo, viejo, nuevo):
    modulo = _contratos_cambiado(tmp_path, viejo, nuevo)
    casos = {n: caso for n, caso in bateria.items() if n.startswith(prefijo)}
    assert casos, prefijo
    medido = g.aceptaciones(casos, a_mano[1], tmp_path, FECHA, modulo)
    congelado = _congelado("aceptaciones_rechazos.json")
    distintos = sorted(n for n in casos if medido["casos"][n] != congelado["casos"][n])
    assert distintos or medido["claves_de_la_traza_de_mensajes"] != congelado["claves_de_la_traza_de_mensajes"]


# ================================================================ QA r01, H-01 b y c · más flujos y rutas anidadas con su tipo
OBSERVADOS = [f"CT-{n:02d}" for n in (1, 2, 3, 4, 5, 6, 8, 11, 12, 13, 15, 16, 17, 19, 22, 23, 24, 25)]


def test_h01_los_flujos_cubren_los_contratos_que_el_ejecutor_emite(flujos):
    congelado = _congelado("formas_flujos_mock.json")
    assert sorted(congelado["flujos"]) == sorted(g.FLUJOS) == sorted(flujos)
    assert all(flujos[nombre] for nombre in g.FLUJOS), {n: len(v) for n, v in flujos.items()}
    assert congelado["contratos_vistos_en_algun_flujo"] == OBSERVADOS
    assert congelado["contratos_que_ningun_flujo_emite"] == ["CT-07", "CT-09", "CT-10", "CT-14", "CT-18", "CT-20", "CT-21"]
    for nombre, guardados in g.FLUJOS.items():
        vistos = {clave.split(".")[0] for clave in congelado["flujos"][nombre]["mensajes"]}
        assert vistos == set(guardados) if guardados != g.TODOS else len(vistos) >= 7, nombre
    f = congelado["flujos"]
    assert f["consulta_n0"]["mensajes"]["CT-03.RETORNO"]["valores_de_listas_cerradas"]["ruta"] == ["N0"]
    assert f["consulta_que_escala"]["mensajes"]["CT-03.RETORNO"]["valores_de_listas_cerradas"]["ruta"] == ["ANALITICA"]
    assert f["consulta_que_escala"]["mensajes"]["CT-03.RETORNO"]["rutas_siempre"]["escalado.run_id"] == "string"
    assert f["pregunta_repetida"]["mensajes"]["CT-22.ENCARGO"]["valores_de_listas_abiertas"] == {"tipo": ["PREGUNTA_REPETIDA"], "tipo_aviso": []}
    assert f["decision_broker"]["mensajes"]["CT-22.ENCARGO"]["valores_de_listas_abiertas"] == {"tipo": ["DECISIONES_BROKER"], "tipo_aviso": []}
    assert f["consulta_al_broker"]["mensajes"]["CT-22.ENCARGO"]["valores_de_listas_abiertas"] == {"tipo": [], "tipo_aviso": ["CONSULTA_RECURRENTE"]}
    assert f["consulta_al_broker"]["mensajes"]["CT-23.RETORNO"]["valores_de_listas_cerradas"] == {"estado_consulta": ["RESPONDIDA"]}
    assert f["seguimiento_encargado"]["mensajes"]["CT-05.ENCARGO"]["valores_de_listas_cerradas"]["tipo"] == ["SEGUIMIENTO"]
    assert f["seguimiento_encargado"]["mensajes"]["CT-24.ENCARGO"]["valores_de_listas_cerradas"]["accion"] == [
        "ALTA", "CANCELACION", "MODIFICACION", "PAUSA", "REANUDACION"]
    assert f["consulta_al_broker"]["mensajes"]["CT-23.ENCARGO"]["valores_de_listas_cerradas"]["sentido"] == ["ENTRANTE", "SALIENTE"]
    assert set(f["ciclo_semanal_v6"]["mensajes"]["CT-15.ENCARGO"]["receptores"]) == {"AG-26"}
    assert set(f["ciclo_semanal_v5"]["mensajes"]["CT-15.ENCARGO"]["receptores"]) == {"AG-17"}
    assert f["ciclo_semanal_v5"]["mensajes"]["CT-06.ENCARGO"]["rutas_a_veces"]["lecciones[]"] == "string"   # el segundo ciclo ya lleva lecciones


def test_h01_las_rutas_llevan_claves_anidadas_tipos_y_combinaciones():
    mensajes = [{"a": 1, "b": {"c": [{"d": "x", "RV": None}, {"d": "y", "e": 1.5}], "RV": {"OPP-2026-0007": True}}, "f": []},
                {"a": "1", "b": {"c": []}, "g": None}]
    siempre, a_veces = g.rutas(mensajes)
    assert siempre == {"a": "integer|string", "b": "object", "b.c": "array", "b.c[].d": "string", "b.<clase>.<id>": "boolean"}
    assert a_veces == {"b.c[]": "object", "b.<clase>": "object", "b.c[].<clase>": "null", "b.c[].e": "number", "f": "array", "g": "null"}
    forma = g.formas({"flujo": [{"contrato": "CT-99", "tipo_mensaje": "ENCARGO", "emisor": "X", "receptor": "Y", **m} for m in mensajes]})
    assert forma["flujos"]["flujo"]["mensajes"]["CT-99.ENCARGO"]["combinaciones_de_claves_a_veces"] == ["f", "g"]


def _cambiar(flujos, contrato, cambio, tipo_mensaje=None):
    """Una copia de los flujos con `cambio(msg)` aplicado a los mensajes de un contrato. Devuelve la copia y cuántos cambió."""
    copia, n = copy.deepcopy(flujos), 0
    for mensajes in copia.values():
        for msg in mensajes:
            if msg["contrato"] == contrato and tipo_mensaje in (None, msg["tipo_mensaje"]) and cambio(msg) is not False:
                n += 1
    return copia, n


def _renombrar(viejo, nuevo):
    def cambio(msg):
        if viejo not in msg:
            return False
        msg[nuevo] = msg.pop(viejo)
    return cambio


def _sin_proximo_ciclo_al_finalizar(msg):
    if msg.get("estado_seguimiento") != "FINALIZADO":
        return False
    del msg["proximo_ciclo"]


def _sin_herramienta(msg):
    return msg.pop("herramienta", False)


# Los cambios de formato de lo que el ejecutor emite que la r01 vio pasar (E02 a E11), hechos sobre los mensajes capturados
CAMBIOS_DE_EMISION = [
    ("E02 · lecciones de CT-06 pasa de identificadores a objetos", "CT-06", None,
     lambda m: m.__setitem__("lecciones", [{"id": x} for x in m["lecciones"]]) if m["lecciones"] else False),
    ("E03 · clave nueva dentro de cada encargo de CT-12", "CT-12", None, lambda m: [e.__setitem__("extra_qa", 1) for e in m["encargos"]]),
    ("E04 · clave nueva dentro de resumen de CT-02", "CT-02", None, lambda m: m["resumen"].__setitem__("extra_qa", 1)),
    ("E05 · top3_por_clase de CT-02 pasa de listas a un número", "CT-02", None,
     lambda m: m["resumen"].__setitem__("top3_por_clase", {c: len(v) for c, v in m["resumen"]["top3_por_clase"].items()})),
    ("E06 · urgencia de CT-03 renombrada", "CT-03", "ENCARGO", _renombrar("urgencia", "prisa")),
    ("E07 · paquete_auditoria de CT-16 renombrado", "CT-16", None, _renombrar("paquete_auditoria", "paquete")),
    ("E08 · ret_id de CT-22 renombrado", "CT-22", None, _renombrar("ret_id", "ret")),
    ("E09 · CT-24 FINALIZADO sin proximo_ciclo", "CT-24", "RETORNO", _sin_proximo_ciclo_al_finalizar),
    ("E10 · solicitud CT-25 sin herramienta", "CT-25", "ENCARGO", _sin_herramienta),
    ("E11 · respuestas de CT-23 renombrada", "CT-23", "RETORNO", _renombrar("respuestas", "contestaciones")),
    ("un valor que cambia de tipo dentro de una lista (CT-13)", "CT-13", None, lambda m: m["peticiones"][0].__setitem__("opp_id", 7) if m["peticiones"] else False),
    ("un campo anidado que desaparece (CT-05, memoria)", "CT-05", None, lambda m: m["memoria"].pop("opp_vigentes", False)),
    ("el informe de CT-19 pasa de texto a objeto", "CT-19", None, lambda m: m.__setitem__("informe", {"resumen": m["informe"]})),
    ("un receptor distinto (CT-17)", "CT-17", None, lambda m: m.__setitem__("receptor", "AG-20")),
]


@pytest.mark.parametrize("contrato, tipo_mensaje, cambio", [c[1:] for c in CAMBIOS_DE_EMISION], ids=[c[0] for c in CAMBIOS_DE_EMISION])
def test_h01_un_cambio_en_lo_que_el_ejecutor_emite_cambia_las_formas(flujos, a_mano, contrato, tipo_mensaje, cambio):
    cambiados, n = _cambiar(flujos, contrato, cambio, tipo_mensaje)
    assert n >= 1, "el cambio no se aplicó a ningún mensaje capturado"
    assert g.formas(cambiados, a_mano[0]) != _congelado("formas_flujos_mock.json")


def test_h01_el_readme_declara_el_alcance_y_los_limites():
    leeme = (g.CARPETA / "README.md").read_text(encoding="utf-8")
    assert all(f"`{nombre}`" in leeme for nombre in g.GENERADOS + g.A_MANO + ("REGISTRO.md",))
    assert "## Límites" in leeme and "## Qué ve cada golden" in leeme
    limites = leeme[leeme.index("## Límites"):]
    for ct in _congelado("formas_flujos_mock.json")["contratos_que_ningun_flujo_emite"]:
        assert ct in limites, ct
    assert all(flujo in leeme for flujo in g.FLUJOS)


def test_un_fichero_a_mano_roto_se_dice_sin_traza(monkeypatch, capsys):
    """Si un esquema, un ejemplo o un caso de la batería está roto, el comprobador termina con 1 y dice por qué."""
    def roto(*args, **kwargs):
        raise ValueError("caso de la batería mal escrito: ['Xv6']\nmás detalle")
    monkeypatch.setattr(g, "generar", roto)
    assert g.main([]) == 1
    salida = capsys.readouterr()
    assert salida.err == "ERROR · no se pueden generar los goldens: ValueError: caso de la batería mal escrito: ['Xv6']\n"
    assert salida.out == "goldens de contratos: no se pueden generar\n"


# ================================================================ T-143 · el Anexo B V5.2 describe lo que hace el ejecutor
# Los retornos internos los valida el esquema de respuesta del agente (`ESQUEMAS`); el Anexo B V5.2 lo dice con una frase fija
# por esquema: «con `CLAVE`, que exige …; admite además …». Aquí, qué esquemas valida el ejecutor en cada contrato
# (`_invocar` de `orquestacion.py` y `diseno_v6.py`).
ESQUEMAS_DE_RESPUESTA = {"CT-05": ["INTEGRACION"], "CT-06": ["INFORME_CLASE", "REVISION_VIGENTES", "RESPUESTA_OBJECIONES"],
                         "CT-07": ["BUSQUEDA"], "CT-08": ["BUSQUEDA"], "CT-11": ["CURACION"], "CT-12": ["PROSPECTIVA"],
                         "CT-13": ["REFUTACION", "CONTRARREPLICA"], "CT-14": ["DICTAMEN_G3"], "CT-15": ["REDACCION", "SINTESIS"],
                         "CT-17": ["AUDITORIA"]}   # T-143 r03 (QA r02, H-09): el Auditor responde con AUDITORIA
# T-143 r03 (QA r02, H-08): la ficha de cada finalista (y exploratoria) de CT-06; sus anidados se describen con «En `FINALISTA`, …»
FICHA = "FINALISTA"
# T-143 r03 (QA r02, H-11 b): frases de los retornos internos que no son una lista de campos y que fija el Anexo B V5.2 (lo que
# corrigieron H-02 de la r01 y H-07 de la r02)
FRASES_FIJAS = {
    # r04 (QA r03, H-12 y H-13): el V6 y sus interruptores
    "CT-05": [("En el diseño V6 (con `v6.sintetizador`, el valor por defecto) no hay orden INTEGRACION ni su retorno: el código "
               "calcula antes de G3 el régimen de cada tipo y los cambios frente al run anterior, y el Sintetizador escribe después "
               "la integración con `SINTESIS` (CT-15)."),
              "Con `v6.sintetizador` desactivado, el V6 emite la orden INTEGRACION como el V5."],
    "CT-11": [("El ejecutor pide la curación solo en los niveles N2 y N3; en el diseño V6, solo con `v6.curacion_llm`, que viene "
               "desactivado: entonces no se emite el CT-11 y la curación es determinista.")],
    "CT-17": ["De cada hallazgo, el ejecutor toma además, si lo trae, `objeto` (si no, el run auditado), que el esquema no exige."],
    "CT-07": ["sin `afirmacion`, la pieza toma la síntesis, y sin `direccion`, neutra.",
              "En backtest solo cuentan las referencias registradas que se le ofrecieron.",
              "Solo usa las tres primeras referencias de la respuesta."],
    "CT-06": ["En la fase SEGUIMIENTO no hay informe del Analista: la revisión la calcula el ejecutor (7.11)."],
    "CT-14": ["No hay dictamen APTO: si el validador HT-09 da «apto», la entrega sigue sin dictamen del Orquestador (6.1).",
              ("En el diseño V6, salvo con `v6.dictamen_g3_llm`, que viene desactivado, el CT-14 se emite pero no se pide dictamen a "
               "AG-18: lo da la regla, apto con advertencias si no hay bloqueos y bloqueado si los hay.")],
    "CT-15": ["respuesta: los textos del informe, no sus rutas.",
              "Los tres entregables y sus rutas los escribe el ejecutor, que mide su legibilidad al validarlos (G3).",
              # ronda de cierre (QA r04, H-16 c): el Sintetizador del V6 y su integración
              ("En el diseño V6 (con `v6.sintetizador`, el valor por defecto; si no, responde el Redactor con `REDACCION`), el "
               "Sintetizador responde con `SINTESIS`"),
              "Los campos de integración de `SINTESIS` son la integración del V6."],
}
# Lo que la prosa no puede volver a decir de esos retornos (texto de la V5.1 o lo contrario de la frase fija)
FRASES_PROHIBIDAS = {"CT-14": ["dictamen APTO,", "dictamina APTO", "(APTO |"], "CT-15": ["rutas de los tres entregables", "métricas de legibilidad"],
                     "CT-05": ["la integración la calcula el código"]}   # r04 (QA r03, H-12): la frase de la r03
# T-143 r02: campos del retorno que el Anexo B nombra fuera del esquema de respuesta (el retorno parcial de CT-05, que el
# ejecutor no lee)
EXTRAS_DEL_RETORNO = {"CT-05": {"SOLICITUD_PRESUPUESTO", "consultas_broker", "solicitudes_credenciales"}}
# T-143 r02 (QA r01, H-03 y H-05): los campos anidados se describen con «En `CLAVE`, cada elemento de `ruta` lleva …; admite
# además …» (o «`ruta` lleva …» si es un objeto); `a[].b` es el campo `b` de cada elemento de `a`
RE_ANIDADO = re.compile(r"En ((?:`[A-Z_0-9]+`(?:, | y )?)+), (?:cada elemento de )?`([a-z_\[\].0-9]+)` lleva ([^;.]*)"
                        r"(?:; admite además ([^;.]*))?\.")
# Los campos comunes que la frase fija no nombra («salvo `estado` y `autoevaluacion`, que son comunes»)
COMUNES_DE_LA_RESPUESTA = frozenset({"estado", "autoevaluacion"})
RE_VALORES = re.compile(r"`([^`]+)` \(([^)]*)\)")


def _nombres(texto):
    return set(re.findall(r"`([^`]+)`", texto or ""))


def _en(esquema, ruta):
    """El esquema de `ruta` («a[].b») dentro de un esquema de respuesta; si es una lista, el de sus elementos."""
    for parte in ruta.split("."):
        esquema = esquema["properties"][parte.removesuffix("[]")]
        if parte.endswith("[]") or "items" in esquema:
            esquema = esquema.get("items", esquema)
    return esquema


def _valores_que_difieren(texto, esquema, donde, obligatorios=True):
    """Los valores que la prosa da entre paréntesis tras un campo frente al `enum` del código, y los campos con `enum` que la
    prosa nombra sin dar sus valores."""
    difieren, dados = [], {c: {v.strip() for v in vs.split(" | ")} for c, vs in RE_VALORES.findall(texto or "")}
    for campo in _nombres(texto):
        prop = esquema.get("properties", {}).get(campo, {})
        enum = prop.get("enum") or (prop.get("items") or {}).get("enum")   # r03 (H-08): también una lista de valores cerrados
        if enum is None:
            continue
        if campo in dados and dados[campo] != set(enum):
            difieren.append((*donde, f"`{campo}` admite {sorted(enum)}; el Anexo B dice {sorted(dados[campo])}"))
        elif campo not in dados and obligatorios:
            difieren.append((*donde, f"`{campo}` tiene lista cerrada {sorted(enum)} y el Anexo B no da sus valores"))
    return difieren


def _con_anidados(esquema, ruta="", ficha=None):
    """(ruta, esquema) de cada campo anidado con campos propios (objeto o lista de objetos). La ficha de los finalistas no se
    recorre aquí: sus anidados se comparan aparte, con la clave `FINALISTA`."""
    for campo, prop in esquema.get("properties", {}).items():
        if not ruta and campo in COMUNES_DE_LA_RESPUESTA:
            continue
        sub = prop.get("items", prop)
        if isinstance(sub, dict) and ("required" in sub or "properties" in sub):
            r = f"{ruta}{campo}"
            yield r, sub
            if ficha is None or sub != ficha:
                yield from _con_anidados(sub, r + "[].", ficha)


def _anidado_que_difiere(ct, clave, ruta, sub, lleva, ademas):
    """Lo que difiere entre una frase «… lleva …; admite además …» y el esquema del código de ese campo."""
    difieren = []
    if _nombres(lleva) != set(sub.get("required", [])):
        difieren.append((ct, clave, f"`{ruta}` lleva {sorted(sub.get('required', []))}; el Anexo B dice {sorted(_nombres(lleva))}"))
    opcionales = set(sub.get("properties", {})) - set(sub.get("required", []))
    if _nombres(ademas) != opcionales:
        difieren.append((ct, clave, f"`{ruta}` admite además {sorted(opcionales)}; el Anexo B dice {sorted(_nombres(ademas))}"))
    return difieren + _valores_que_difieren(f"{lleva} {ademas or ''}", sub, (ct, clave))


def _esquemas_de_respuesta_que_difieren(esquemas_respuesta, parrafos, derivados):
    """(contrato, esquema, qué difiere) donde el Anexo B V5.2 y `ESQUEMAS` no dicen lo mismo de un retorno interno: los campos
    de primer nivel, los anidados y los valores de las listas cerradas."""
    difieren = []
    ficha = esquemas_respuesta["INFORME_CLASE"]["properties"]["finalistas"]["items"]
    for ct, claves in ESQUEMAS_DE_RESPUESTA.items():
        nombrados, p = set(), parrafos[ct]
        difieren += [(ct, "frase fija", f"falta «{f}»") for f in FRASES_FIJAS.get(ct, []) if f not in p]
        difieren += [(ct, "frase prohibida", f"dice «{f}»") for f in FRASES_PROHIBIDAS.get(ct, []) if f in p]
        anidados = {}
        for m in RE_ANIDADO.finditer(p):
            for clave in re.findall(r"`([A-Z_0-9]+)`", m.group(1)):
                anidados[(clave, m.group(2))] = m.groups()[2:]
        if any(sub == ficha for clave in claves for _, sub in _con_anidados(esquemas_respuesta[clave], ficha=ficha)):
            for ruta, sub in _con_anidados(ficha, ficha=ficha):
                if (FICHA, ruta) not in anidados:
                    difieren.append((ct, FICHA, f"el Anexo B no describe `{ruta}`"))
                    continue
                difieren += _anidado_que_difiere(ct, FICHA, ruta, sub, *anidados.pop((FICHA, ruta)))
        for clave in claves:
            codigo = esquemas_respuesta[clave]
            m = re.search(rf"con `{clave}`, que exige ([^;.]*)(?:; admite además ([^;.]*))?\.", p)
            if not m:
                difieren.append((ct, clave, "el párrafo no lo describe"))
                continue
            exige = set(codigo.get("required", [])) - COMUNES_DE_LA_RESPUESTA
            admite = set(codigo.get("properties", {})) - set(codigo.get("required", [])) - COMUNES_DE_LA_RESPUESTA
            if _nombres(m.group(1)) != exige:
                difieren.append((ct, clave, f"exige {sorted(exige)}; el Anexo B dice {sorted(_nombres(m.group(1)))}"))
            if _nombres(m.group(2)) != admite:
                difieren.append((ct, clave, f"admite además {sorted(admite)}; el Anexo B dice {sorted(_nombres(m.group(2)))}"))
            difieren += _valores_que_difieren(f"{m.group(1)} {m.group(2) or ''}", codigo, (ct, clave))
            nombrados |= exige | admite
            for ruta, sub in _con_anidados(codigo, ficha=ficha):
                if (clave, ruta) not in anidados:
                    difieren.append((ct, clave, f"el Anexo B no describe `{ruta}`"))
                    continue
                lleva, ademas = anidados.pop((clave, ruta))
                if lleva.startswith("lo mismo que cada elemento de "):
                    otro = re.search(r"`([^`]+)`", lleva).group(1)
                    iguales = [k for k in claves if otro in esquemas_respuesta[k].get("properties", {})
                               and _en(esquemas_respuesta[k], otro) == sub]
                    if not iguales:
                        difieren.append((ct, clave, f"`{ruta}` no lleva lo mismo que `{otro}`"))
                    continue
                difieren += _anidado_que_difiere(ct, clave, ruta, sub, lleva, ademas)
        difieren += [(ct, clave, f"el Anexo B describe `{ruta}`, que el esquema no tiene") for clave, ruta in anidados]
        derivado = derivados[f"{ct}.RETORNO"]
        if set(derivado["properties"]) != nombrados | EXTRAS_DEL_RETORNO.get(ct, set()) or derivado["required"]:
            difieren.append((ct, "derivado", f"el esquema derivado nombra {sorted(derivado['properties'])} y exige {derivado['required']}"))
    return difieren


def test_t143_los_retornos_internos_son_los_esquemas_de_respuesta_del_codigo(a_mano):
    """CA-4 de T-143: de cada retorno interno, el Anexo B V5.2 nombra exactamente los campos de primer nivel que exige y que
    admite el esquema de respuesta del agente (`ESQUEMAS`, sin los campos comunes), y el esquema derivado no exige ninguno
    (la mensajería no ve estos retornos)."""
    parrafos = g.parrafos_anexo_b()
    assert _esquemas_de_respuesta_que_difieren(contratos.ESQUEMAS, parrafos, a_mano[0]) == []
    assert all(f"`{clave}`" in parrafos[ct] for ct, claves in ESQUEMAS_DE_RESPUESTA.items() for clave in claves)


@pytest.mark.parametrize("cambio", [
    lambda e: e["INFORME_CLASE"]["required"].append("senales_para_otras_clases"),
    lambda e: e["BUSQUEDA"]["required"].remove("lagunas"),
    lambda e: e["DICTAMEN_G3"]["properties"].pop("advertencias"),
    lambda e: e["CURACION"]["properties"].__setitem__("evd_id", {}),
    lambda e: e["REVISION_VIGENTES"]["properties"].pop("exploratorias"),
], ids=["campo exigido nuevo", "campo exigido que deja de serlo", "campo admitido quitado", "campo admitido nuevo", "otro esquema de CT-06"])
def test_t143_un_cambio_en_los_esquemas_de_respuesta_se_nota(a_mano, cambio):
    mutados = copy.deepcopy(contratos.ESQUEMAS)
    cambio(mutados)
    assert _esquemas_de_respuesta_que_difieren(mutados, g.parrafos_anexo_b(), a_mano[0]) != []


def test_t143_el_estado_propio_de_ct23_a_ct25_es_el_del_codigo(a_mano):
    """El campo y los valores del estado propio (6.2.6) del Anexo B V5.2 son los de `CAMPO_ESTADO` y `ESTADOS_ESPECIFICOS`:
    en el bloque JSON del retorno y en el esquema derivado, que ya no pone el estado del objeto en `estado`."""
    esquemas, _ = a_mano
    parrafos = g.parrafos_anexo_b()
    assert sorted(contratos.CAMPO_ESTADO) == ["CT-23", "CT-24", "CT-25"]
    for ct, campo in contratos.CAMPO_ESTADO.items():
        valores = list(contratos.ESTADOS_ESPECIFICOS[ct])
        assert f'"{campo}":"{"|".join(valores)}"' in parrafos[ct], ct
        assert esquemas[f"{ct}.RETORNO"]["properties"][campo] == {"enum": valores} and campo in esquemas[f"{ct}.RETORNO"]["required"]
        assert "estado" not in esquemas[f"{ct}.RETORNO"]["properties"] and '"estado":' not in parrafos[ct]


def _motor(tmp_path):
    from bloque_a.almacen import Almacen
    from bloque_a.configuracion import cargar_config
    from bloque_a.motor import servicio

    class Proveedor:
        as_of = None
        nombre = "pruebas"

    return servicio, servicio.Motor(Almacen(tmp_path), Proveedor(), cargar_config())


def test_t143_las_claves_de_los_retornos_del_motor_son_las_del_anexo_b(a_mano, tmp_path):
    """CT-09 y CT-10 no pasan por la mensajería: el Anexo B V5.2 da las claves de lo que devuelve el Motor, y aquí se miden
    con el Motor de verdad (un cálculo servido, el mismo servido desde la caché, un rechazo y la re-ejecución)."""
    esquemas, _ = a_mano
    servicio, motor = _motor(tmp_path)
    ficha = next(f for f in sorted(servicio.CASOS_CONTROL) if servicio.servible(f) and f != "VOL-GARCH-001")
    caso = servicio.CASOS_CONTROL[ficha][0]
    peticion = {"operacion": ficha, "datos": caso.get("datos") or [], "parametros": dict(caso.get("parametros") or {}),
                "fecha_corte": "2029-12-31"}
    servido = motor.servir(peticion, "AG-21")
    cache = motor.servir(peticion, "AG-21")
    rechazo = motor.servir({**peticion, "operacion": "NO-EXISTE-001"}, "AG-21")
    reejecucion = motor.reejecutar(servido["calc_id"], "auditoría de prueba")
    assert servido["estado"] in ("SERVED", "SERVED_WITH_LIMITATIONS") and cache["cache_hit"] is True and rechazo["estado"] == "RECHAZADO"
    ct09 = esquemas["CT-09.RETORNO"]
    assert set(servido) | set(cache) | set(rechazo) == set(ct09["properties"]) | {"estado"} and ct09["required"] == []
    assert servido["clase_cifra"] in ct09["properties"]["clase_cifra"]["enum"]
    assert {servicio.IMPLEMENTADAS[f]["cifra"] for f in servicio.IMPLEMENTADAS} == set(ct09["properties"]["clase_cifra"]["enum"])
    ct10 = esquemas["CT-10.RETORNO"]
    assert set(reejecucion) == set(ct10["properties"]) and ct10["required"] == []
    assert reejecucion["coincide"] in ct10["properties"]["coincide"]["enum"]
    parrafo = g.parrafos_anexo_b()["CT-09"]
    assert "(SERVED o SERVED_WITH_LIMITATIONS)" in parrafo and "`estado` RECHAZADO" in parrafo


# Cambios de lo que el ejecutor emite que el Anexo B V5.2 no describe: cada uno vuelve a dar una diferencia (en la V5.1 eran
# diferencias congeladas). Se aplican a los mensajes capturados de los flujos.
VUELVEN_A_DIFERIR = [
    ("CT-11 · una pieza sin indice", "CT-11", lambda m: m["piezas"][0].pop("indice") if m["piezas"] else False),
    ("CT-12 · un encargo sin tipo_pronostico", "CT-12", lambda m: m["encargos"][0].pop("tipo_pronostico") if m["encargos"] else False),
    ("CT-13 · una petición sin evidencias", "CT-13", lambda m: m["peticiones"][0].pop("evidencias") if m["peticiones"] else False),
    ("CT-06 · una fase que el Anexo B no nombra", "CT-06", lambda m: m.__setitem__("fase", "OTRA_FASE")),
    ("CT-03 · escalado sin plazo_estimado", "CT-03", lambda m: m["escalado"].pop("plazo_estimado") if isinstance(m.get("escalado"), dict) else False),
    ("CT-23 · el estado de la consulta en estado", "CT-23", lambda m: m.__setitem__("estado", m.pop("estado_consulta")) if "estado_consulta" in m else False),
    ("CT-24 · el estado del seguimiento en estado", "CT-24", lambda m: m.__setitem__("estado", m.pop("estado_seguimiento")) if "estado_seguimiento" in m else False),
    ("CT-16 · paquete_auditoria sin entregables", "CT-16", lambda m: m["paquete_auditoria"].pop("entregables")),
]


@pytest.mark.parametrize("contrato, cambio", [c[1:] for c in VUELVEN_A_DIFERIR], ids=[c[0] for c in VUELVEN_A_DIFERIR])
def test_t143_lo_que_el_anexo_b_ya_describe_vuelve_a_diferir_si_el_ejecutor_cambia(flujos, a_mano, tmp_path, contrato, cambio):
    esquemas, ejemplos = a_mano
    cambiados, n = _cambiar(flujos, contrato, cambio)
    assert n >= 1, "el cambio no se aplicó a ningún mensaje capturado"
    medido = g.divergencias(esquemas, ejemplos, [m for m in g.todos_los_mensajes(cambiados) if m["contrato"] == contrato], tmp_path, FECHA)
    difieren = medido["mensajes_de_los_flujos_simulados_que_no_cumplen_el_anexo_b"] or medido["valores_que_el_anexo_b_nombra_en_un_campo_y_el_ejecutor_emite_en_otro"]
    assert difieren and all(clave.startswith(contrato) for clave in difieren)


@pytest.mark.parametrize("clave, campo", [("CT-24.ENCARGO", "opp_id"), ("CT-25.ENCARGO", "urgencia"), ("CT-01.ENCARGO", "fecha_objetivo"),
                                          ("CT-23.RETORNO", "respuestas"), ("CT-03.RETORNO", "escalado")])
def test_t143_un_campo_que_el_anexo_b_vuelve_a_exigir_y_el_ejecutor_no_da_una_diferencia(a_mano, tmp_path, clave, campo):
    """Los campos que la V5.2 marca «opcional» porque el ejecutor no los exige: si el Anexo B volviera a exigirlos sin cambiar
    el código, la diferencia volvería (en la V5.1 estaba congelada)."""
    esquemas, ejemplos = a_mano
    assert campo not in esquemas[clave]["required"] and campo in ejemplos[clave]
    exigidos = copy.deepcopy(esquemas)
    exigidos[clave]["required"].append(campo)
    medido = g.divergencias(exigidos, ejemplos, [], tmp_path, FECHA)
    assert medido["por_contrato"] == {clave: {"el_ejecutor_admite_que_falte": [campo]}}


def test_t143_las_divergencias_que_quedan():
    """CA-3 de T-143: contra el Anexo B V5.2 no queda ninguna diferencia medida; solo los contratos de los que el Anexo B no
    da campos (CT-18, CT-20 y CT-21, en los prompts de sistema)."""
    assert _congelado("divergencias_anexo_b.json") == {
        "contratos_sin_campos_en_el_anexo_b": SIN_CAMPOS, "mensajes_de_los_flujos_simulados_que_no_cumplen_el_anexo_b": {},
        "por_contrato": {}, "valores_que_el_anexo_b_nombra_en_un_campo_y_el_ejecutor_emite_en_otro": {}}


def test_t143_la_v52_es_la_v51_con_el_anexo_b_corregido():
    """CA-1 y CA-2 de T-143: la V5.1 (`.md` y `.docx`) está en `99_Historico_V5.1`, y fuera del Anexo B la V5.2 solo cambia
    la cabecera de versión y añade una fila al registro de cambios (Anexo F). Desde T-166 la V5.2 está en `99_Historico_V5.2` y
    en `01_Gobernanza` está la V5.3 (`test_t166_entrega_corpus.py` compara la V5.3 con la V5.2)."""
    v52_md = g.BLOQUE / "99_Historico_V5.2" / "01_Gobernanza" / "Documento 0 - Protocolo maestro del Bloque A - Versión óptima V5.2.md"
    historico = g.BLOQUE / "99_Historico_V5.1" / "01_Gobernanza"
    assert sorted(p.name for p in historico.iterdir()) == [f"Documento 0 - Protocolo maestro del Bloque A - Versión óptima V5.1.{x}" for x in ("docx", "md")]

    def sin_anexo_b(texto):
        return (texto[:texto.index("## ANEXO B.")] + texto[texto.index("## ANEXO C."):]).splitlines()

    v51 = sin_anexo_b((historico / "Documento 0 - Protocolo maestro del Bloque A - Versión óptima V5.1.md").read_text(encoding="utf-8"))
    v52_texto = v52_md.read_text(encoding="utf-8")
    v52 = sin_anexo_b(v52_texto)
    import difflib
    cambios = [x for x in difflib.ndiff(v51, v52) if x[:1] in "+-"]
    quitadas = [x[2:] for x in cambios if x[0] == "-"]
    puestas = [x[2:] for x in cambios if x[0] == "+"]
    assert [x.split(":**")[0] for x in quitadas] == ["## Buscador de Oportunidades de Inversión · Versión óptima V5.1", "**Fecha", "**Sustituye a", "**Actualizado"]
    assert [x.split(":**")[0] for x in puestas[:4]] == ["## Buscador de Oportunidades de Inversión · Versión óptima V5.2", "**Fecha", "**Sustituye a", "**Actualizado"]
    assert len(puestas) == 5 and puestas[4].startswith("| óptima V5.2 | 15/11/2026 | Anexo B corregido")
    assert "`99_Historico_V5.1`" in puestas[2] and "INC-T114-01" in puestas[4]
    assert '`version_contrato` ("5.1")' in v52_texto and '`version_contrato` ("5.1")' in _anexo_b() and contratos.VERSION_CONTRATO == "5.1"


# ================================================================ T-143 r02 (QA r01, H-01 a H-05) · lo que la prosa del Anexo B dice
@pytest.mark.parametrize("donde, cambio", [
    ("código", lambda e, p: e["REFUTACION"]["properties"]["resultados"]["items"]["properties"]["veredicto_global"]["enum"].append("tesis dudosa")),
    ("código", lambda e, p: e["REFUTACION"]["properties"]["resultados"]["items"]["properties"]["objeciones"]["items"]["required"].append("evidencia")),
    ("código", lambda e, p: e["CURACION"]["properties"]["piezas"]["items"]["properties"]["nivel_confianza"]["enum"].pop()),
    ("código", lambda e, p: e["RESPUESTA_OBJECIONES"]["properties"]["respuestas"]["items"]["required"].append("evidencia_citada")),
    ("código", lambda e, p: e["INFORME_CLASE"]["properties"]["cribado"]["items"]["required"].append("senal")),
    ("código", lambda e, p: e["REDACCION"]["properties"].__setitem__("rutas", {"type": "object", "required": ["informe_tecnico"]})),
    ("prosa", lambda e, p: p.__setitem__("CT-13", p["CT-13"].replace("`fuerza` (fuerte | moderada | debil), `argumento`", "`fuerza` (fuerte | moderada | debil), `argumento`, `evidencia`"))),
    ("prosa", lambda e, p: p.__setitem__("CT-14", p["CT-14"].replace("`dictamen` (APTO_CON_ADVERTENCIAS | BLOQUEADO)", "`dictamen` (APTO | APTO_CON_ADVERTENCIAS | BLOQUEADO)"))),
    ("prosa", lambda e, p: p.__setitem__("CT-06", p["CT-06"].replace("`premortem`, ", ""))),
    ("prosa", lambda e, p: p.__setitem__("CT-12", p["CT-12"].replace("`vista` (alcista | bajista | lateral | relativa_favorable | relativa_desfavorable)", "`vista`"))),
    ("prosa", lambda e, p: p.__setitem__("CT-15", p["CT-15"].replace("El Redactor responde con `REDACCION`", "El Redactor responde con rutas"))),
    # r03 (QA r02, H-08, H-09 y H-11 b)
    ("código", lambda e, p: e["AUDITORIA"]["required"].append("conclusion")),
    ("código", lambda e, p: e["AUDITORIA"]["properties"]["hallazgos"]["items"]["properties"]["severidad"]["enum"].append("Leve")),
    ("código", lambda e, p: e["INFORME_CLASE"]["properties"]["finalistas"]["items"]["properties"]["tipo_opcion"]["enum"].append("PAIS")),
    ("código", lambda e, p: e["INFORME_CLASE"]["properties"]["finalistas"]["items"]["properties"]["regiones"]["items"]["enum"].pop()),
    ("código", lambda e, p: e["INFORME_CLASE"]["properties"]["finalistas"]["items"]["properties"]["ambito"]["required"].append("pais")),
    ("código", lambda e, p: e["INFORME_CLASE"]["properties"]["finalistas"]["items"]["properties"]["afirmaciones"]["items"]["properties"]["direccion"]["enum"].pop()),
    ("prosa", lambda e, p: p.__setitem__("CT-06", p["CT-06"].replace("`nombre`, `nombre_llano`, `tipo_opcion` (MERCADO | SECTOR | SUBSECTOR | TEMATICA | SEGMENTO | FACTOR | ESTILO | ESTRATEGIA)", "`nombre`, `nombre_llano`, `tipo_opcion` (MERCADO | PAIS)"))),
    ("prosa", lambda e, p: p.__setitem__("CT-06", p["CT-06"].replace(", `horizontes_aplicables` (H1 | H2 | H3 | H4 | H5),", ", `horizontes_aplicables`,"))),
    ("prosa", lambda e, p: p.__setitem__("CT-06", p["CT-06"].replace(" En `FINALISTA`, `tendencia` lleva `nombre_canonico`.", ""))),
    ("prosa", lambda e, p: p.__setitem__("CT-17", p["CT-17"].replace("con `AUDITORIA`, que exige `hallazgos` y `resumen`", "con su esquema"))),
    ("prosa", lambda e, p: p.__setitem__("CT-15", p["CT-15"].replace("Los tres entregables y sus rutas los escribe el ejecutor, que mide su legibilidad al validarlos (G3).", "El Redactor devuelve además las rutas de los tres entregables y sus métricas de legibilidad."))),
    ("prosa", lambda e, p: p.__setitem__("CT-14", p["CT-14"].replace("No hay dictamen APTO: si el validador HT-09 da «apto», la entrega sigue sin dictamen del Orquestador (6.1).", "Si el validador HT-09 da «apto», el Orquestador dictamina APTO."))),
    ("prosa", lambda e, p: p.__setitem__("CT-06", p["CT-06"].replace("En la fase SEGUIMIENTO no hay informe del Analista: la revisión la calcula el ejecutor (7.11).", "En la fase SEGUIMIENTO el Analista responde con `INFORME_CLASE`."))),
], ids=["C02 veredicto nuevo en el código", "evidencia exigida en cada objeción", "un nivel de confianza menos",
        "evidencia_citada exigida", "cribado con señal", "REDACCION con rutas", "D06 la prosa vuelve a poner evidencia",
        "D09 la prosa admite APTO", "la ficha sin premortem", "vista sin sus valores", "CT-15 sin REDACCION",
        "C12 AUDITORIA exige un campo más", "una severidad nueva", "C13 tipo_opcion nuevo", "una región menos",
        "ambito exige un campo más", "una dirección menos en las afirmaciones de la ficha", "P03 tipo_opcion con otros valores",
        "horizontes_aplicables sin valores", "la ficha sin tendencia", "CT-17 sin AUDITORIA", "D20 CT-15 rutas y legibilidad",
        "D21 CT-14 dictamen APTO", "P06 CT-06 informe en SEGUIMIENTO"])
def test_t143_r02_un_cambio_en_los_valores_o_en_los_anidados_se_nota(a_mano, donde, cambio):
    """QA r01 de T-143, H-02, H-03 y H-05: la comparación con `ESQUEMAS` llega a los campos anidados que la prosa describe y a
    los valores de sus listas cerradas, en los dos sentidos (el código cambia o la prosa cambia)."""
    mutados, parrafos = copy.deepcopy(contratos.ESQUEMAS), g.parrafos_anexo_b()
    antes = dict(parrafos)
    cambio(mutados, parrafos)
    assert donde == "código" or parrafos != antes, "el texto del mutante ya no está en el Anexo B: actualícelo"
    assert _esquemas_de_respuesta_que_difieren(mutados, parrafos, a_mano[0]) != []


def _enumerados(esquema, ruta=""):
    for campo, prop in esquema.get("properties", {}).items():
        if "enum" in prop:
            yield campo, prop["enum"]
        sub = prop.get("items", prop)
        if isinstance(sub, dict) and sub is not prop or "properties" in prop:
            yield from _enumerados(sub, f"{ruta}{campo}.")


def _listas_de_la_prosa_que_difieren(esquemas, parrafos):
    """(esquema derivado, campo, qué difiere) donde los valores que el Anexo B da a una lista cerrada (en su bloque JSON,
    «"campo":"A|B"», o en la prosa, «`campo` (A | B)») no son los del esquema derivado."""
    difieren = []
    for clave, esquema in esquemas.items():
        p = parrafos[clave.split(".")[0]]
        for campo, enum in _enumerados(esquema):
            vistos = [set(v.split("|")) for v in re.findall(rf'"{campo}":"([^"]*)"', p)]
            vistos += [{x.strip() for x in v.split(" | ")} for v in re.findall(rf"`{campo}` \(([^)]*)\)", p)]
            if not vistos:
                difieren.append((clave, campo, "el Anexo B no da sus valores"))
            difieren += [(clave, campo, f"el Anexo B dice {sorted(v)}; el derivado, {sorted(enum)}") for v in vistos if v != set(enum)]
    return difieren


def test_t143_r02_las_listas_de_la_prosa_son_las_del_esquema_derivado(a_mano):
    """QA r01 de T-143, H-05 (D05, D10): cada lista cerrada de un esquema derivado tiene sus valores en el párrafo de su
    contrato, y son los mismos."""
    assert _listas_de_la_prosa_que_difieren(a_mano[0], g.parrafos_anexo_b()) == []


@pytest.mark.parametrize("ct, viejo, nuevo", [
    ("CT-06", "SEGUIMIENTO | CRIBADO_E_INVESTIGACION | REVISION_VIGENTES | RESPUESTA_OBJECIONES)", "SEGUIMIENTO | CRIBADO_E_INVESTIGACION | RESPUESTA_OBJECIONES)"),
    ("CT-09", "`clase_cifra` (DETERMINISTA | ESTADISTICA)", "`clase_cifra` (DETERMINISTA | ESTADISTICA | MIXTA)"),
    ("CT-10", "`coincide` (SI | DENTRO_TOLERANCIA | NO)", "`coincide` (SI | NO)"),
    ("CT-24", '"estado_seguimiento":"ACTIVO|PAUSADO|CANCELADO|FINALIZADO"', '"estado_seguimiento":"ACTIVO|PAUSADO|CANCELADO"'),
], ids=["D05 sin REVISION_VIGENTES", "D10 clase_cifra MIXTA", "coincide sin DENTRO_TOLERANCIA", "CT-24 sin FINALIZADO"])
def test_t143_r02_una_lista_de_la_prosa_cambiada_se_nota(a_mano, ct, viejo, nuevo):
    parrafos = g.parrafos_anexo_b()
    assert parrafos[ct].count(viejo) == 1, "el texto del mutante ya no está en el Anexo B: actualícelo"
    parrafos[ct] = parrafos[ct].replace(viejo, nuevo)
    assert _listas_de_la_prosa_que_difieren(a_mano[0], parrafos) != []


# Cómo marca el Anexo B que un campo puede faltar. T-143 r03 (QA r02, H-11 a): la marca acompaña al campo, no basta con que
# esté en la misma frase («y no solo `accion`», «salvo error» no marcan nada)
_LISTA = r"((?:`[^`]+`(?:,\s|\sy\s)?)+)"   # una lista de campos: `a`, `b` y `c`
RE_SON_OPCIONALES = re.compile(r"[Ss]on opcionales(?: [^`:.;]*:)?\s+" + _LISTA)                      # «Son opcionales `a` y `b`»
RE_LISTA_OPCIONAL = re.compile(_LISTA + r"\s+(?:son opcionales|es opcional|van si aplica|(?:van )?solo con)")   # «`a` es opcional»
RE_OPCIONAL_ENTRE_PARENTESIS = re.compile(r"`([^`]+)` \((?:opcional|si aplica)\)")                    # «`a` (si aplica)»
RE_OPCIONAL_EN_EL_JSON = re.compile(r'"([^"]+)":"(?:opcional|solo en)')                               # «"a":"opcional…"»
RE_NO_ENVIA = re.compile(r"no envía `([^`]+)`")                                                       # «el Broker no envía `a`»
# Frases que dicen que la mensajería no exige ninguno de los campos que nombran
FRASES_SIN_EXIGENCIA = ("la mensajería no lo exige", "la mensajería no los exige", "la mensajería no exige sus campos", "uno de dos campos")
# Retornos que no pasan por la mensajería: su derivado no exige nada y los describe la frase fija (pruebas de arriba)
SIN_MENSAJERIA = {f"{ct}.RETORNO" for ct in [*ESQUEMAS_DE_RESPUESTA, "CT-09", "CT-10"]}


def _marcados_como_opcionales(parrafo):
    marcados = set()
    for rx in (RE_SON_OPCIONALES, RE_LISTA_OPCIONAL):
        for m in rx.finditer(parrafo):
            marcados |= _nombres(m.group(1))
    for rx in (RE_OPCIONAL_ENTRE_PARENTESIS, RE_OPCIONAL_EN_EL_JSON, RE_NO_ENVIA):
        marcados |= set(rx.findall(parrafo))
    for frase in (f for linea in parrafo.splitlines() for f in linea.split(". ")):
        if any(x in frase for x in FRASES_SIN_EXIGENCIA):
            marcados |= _nombres(frase)
    return marcados


def _opcionales_sin_marca(esquemas, parrafos):
    """(esquema derivado, campo) de cada campo de primer nivel que el derivado no exige y que el párrafo no marca como
    opcional: por la regla del propio Anexo B («los demás campos nombrados los lleva el mensaje»), la prosa lo estaría
    exigiendo. Desde la r03 también los del sobre que el derivado nombra (`query_id` de CT-03, `run_id` de CT-23)."""
    faltan = []
    for clave, esquema in esquemas.items():
        if clave in SIN_MENSAJERIA:
            continue
        marcados = _marcados_como_opcionales(parrafos[clave.split(".")[0]])
        faltan += [(clave, campo) for campo in sorted(set(esquema["properties"]) - set(esquema["required"])) if campo not in marcados]
    return faltan


def test_t143_r02_lo_que_el_derivado_no_exige_la_prosa_lo_marca_opcional(a_mano):
    """QA r01 de T-143, H-03 y H-05 (D03, D04): la prosa no vuelve a exigir lo que el ejecutor no exige."""
    assert _opcionales_sin_marca(a_mano[0], g.parrafos_anexo_b()) == []


@pytest.mark.parametrize("ct, viejo", [
    ("CT-01", "Son opcionales `nivel_forzado`, `fecha_objetivo` y `referencia_previa`, y dentro de `alcance` todo es opcional (sin `clases`, el ciclo usa los tipos activos). "),
    ("CT-25", "`herramienta` y `urgencia` son opcionales (un recordatorio no los repite)"),
    ("CT-04", "Son opcionales los cinco bloques, que se envían por separado: "),
    ("CT-24", "En el encargo son opcionales `seg_id`, `opp_id`, `frecuencia`, `calendario_personalizado`, `motivo`, `senales_interes` y `fecha_fin`: solo `accion` es obligatorio, y cada acción lleva lo que necesita."),
    # r03 (QA r02, H-11 a): P01, P02, P07 y P08 de r02_03, que la marca suelta dejaba pasar
    ("CT-24", "son opcionales `seg_id`, `opp_id`, `frecuencia`, `calendario_personalizado`, `motivo`, `senales_interes` y `fecha_fin`: solo `accion` es obligatorio"),
    ("CT-25", "`credencial_ref` y `caducidad` son opcionales (una respuesta DENEGADA no lleva caducidad)."),
    ("CT-05", "y `insumos_integracion` solo con INTEGRACION"),
    ("CT-03", "En la consulta, el Broker no envía `query_id`: lo asigna el bloque al recibirla (QRY-). "),
], ids=["D03 CT-01", "D04 CT-25", "CT-04", "CT-24", "P01 CT-24 obligatorios y no solo accion", "P02 CT-25 salvo error",
        "P07 CT-05 insumos_integracion siempre", "P08 CT-03 el Broker envía query_id"])
def test_t143_r02_quitar_una_marca_de_opcional_se_nota(a_mano, request, ct, viejo):
    nuevos = {"D04 CT-25": "`herramienta` es opcional",
              "P01 CT-24 obligatorios y no solo accion": "son obligatorios `seg_id`, `opp_id`, `frecuencia`, "
              "`calendario_personalizado`, `motivo`, `senales_interes` y `fecha_fin`, y no solo `accion`",
              "P02 CT-25 salvo error": "`credencial_ref` y `caducidad` los lleva toda respuesta, salvo error.",
              "P07 CT-05 insumos_integracion siempre": "y `insumos_integracion` en todas las órdenes",
              "P08 CT-03 el Broker envía query_id": "En la consulta, el Broker envía `query_id` (QRY-). "}
    parrafos = g.parrafos_anexo_b()
    assert parrafos[ct].count(viejo) == 1, "el texto del mutante ya no está en el Anexo B: actualícelo"
    parrafos[ct] = parrafos[ct].replace(viejo, nuevos.get(request.node.callspec.id, ""))
    assert _opcionales_sin_marca(a_mano[0], parrafos) != []


def _fases_fuera_de_la_regla(mensajes):
    """CT-06 que no siguen la regla del Anexo B: CRIBADO_E_INVESTIGACION en N2 y N3, REVISION_VIGENTES en los demás niveles,
    RESPUESTA_OBJECIONES con las objeciones del CT-13 y SEGUIMIENTO en el ciclo C6 (con `seg_id`)."""
    malos = []
    for m in mensajes:
        fase, nivel = m.get("fase"), m.get("nivel")
        if fase == "RESPUESTA_OBJECIONES":
            ok = "objeciones" in m
        elif fase == "SEGUIMIENTO":
            ok = "seg_id" in m
        else:
            ok = fase == ("CRIBADO_E_INVESTIGACION" if nivel in ("N2", "N3") else "REVISION_VIGENTES")
        if not ok:
            malos.append((fase, nivel))
    return malos


def test_t143_r02_cada_fase_de_ct06_se_emite_cuando_dice_el_anexo_b(flujos):
    """QA r01 de T-143, H-05 (C07): el Anexo B dice cuándo emite el ciclo cada fase; los flujos simulados lo cumplen y emiten
    las cuatro. Si el ejecutor emitiera otra fase en un nivel (por ejemplo PROFUNDIZACION en N1), la prueba fallaría."""
    assert "El ciclo emite CRIBADO_E_INVESTIGACION en los niveles N2 y N3, REVISION_VIGENTES en los demás, RESPUESTA_OBJECIONES " \
           "cuando el Analista responde a las objeciones del CT-13 y SEGUIMIENTO en el ciclo C6." in g.parrafos_anexo_b()["CT-06"]
    ct06 = [m for m in g.todos_los_mensajes(flujos) if m["contrato"] == "CT-06" and m["tipo_mensaje"] == "ENCARGO"]
    assert {m["fase"] for m in ct06} == {"CRIBADO_E_INVESTIGACION", "REVISION_VIGENTES", "RESPUESTA_OBJECIONES", "SEGUIMIENTO"}
    assert _fases_fuera_de_la_regla(ct06) == []
    cambiados, n = _cambiar(flujos, "CT-06", lambda m: m.__setitem__("fase", "PROFUNDIZACION") if m["fase"] == "REVISION_VIGENTES" else False)
    assert n >= 1 and _fases_fuera_de_la_regla([m for m in g.todos_los_mensajes(cambiados) if m["contrato"] == "CT-06"]) != []


def test_t143_r02_ct04_con_solo_aprobar_certificados_no_se_rechaza(tmp_path):
    """QA r01 de T-143, H-01: el Anexo B nombra el quinto bloque de CT-04 (`aprobar_certificados`, PA-10) y dice que se rechaza
    un CT-04 sin ninguno de los cinco; `Bloque.decision` hace eso."""
    import conftest
    parrafo = g.parrafos_anexo_b()["CT-04"]
    assert "`aprobar_certificados`" in parrafo and "un CT-04 sin ninguno de los cinco se rechaza" in parrafo
    b = conftest.nuevo_bloque(tmp_path / "ct04", conftest.cargar_universo(conftest.RUTA_UNIVERSO_EJEMPLO))
    r = b.decision({"aprobar_certificados": ["CERT-2099-9999"]}, conftest.AS_OF)
    assert r["estado"] in ("REGISTRADA", "APLICADA", "APLICADA_PARCIALMENTE")
    with pytest.raises(ValueError, match="CT-04 vacío"):
        b.decision({}, conftest.AS_OF)


def test_t143_r02_ct03_sin_ejecutar_el_analisis_no_lleva_estado_run(tmp_path, a_mano):
    """QA r01 de T-143, H-03 (a): con `consulta --sin-escalado` el `escalado` no lleva `estado_run` y su `run_id` es nulo; el
    Anexo B y el esquema derivado lo admiten."""
    import conftest
    b = conftest.nuevo_bloque(tmp_path / "ct03", conftest.cargar_universo(conftest.RUTA_UNIVERSO_EJEMPLO))
    r = b.consulta("¿Qué opinas del oro frente a la plata a 6 meses?", as_of=conftest.AS_OF, ejecutar_escalado=False)
    esc = r["escalado"]
    assert isinstance(esc, dict) and "estado_run" not in esc and esc["run_id"] is None
    retorno = {k: r[k] for k in ("query_id", "clase_consulta", "ruta", "respuesta", "referencias", "confianza", "escalado")}
    assert list(jsonschema.Draft202012Validator(a_mano[0]["CT-03.RETORNO"]).iter_errors(retorno)) == []
    assert "`estado_run` solo si se ejecutó el análisis" in g.parrafos_anexo_b()["CT-03"]


def test_t143_r02_ct09_sin_fecha_corte_el_motor_sirve_y_el_anexo_b_lo_dice(tmp_path):
    """QA r01 de T-143, H-04: la `fecha_corte` la exige la mensajería, no el Motor, que sirve sin ella con la fecha del
    proveedor (o sin corte). El Anexo B dice eso, no «obligatoria siempre»."""
    servicio, motor = _motor(tmp_path)
    ficha = next(f for f in sorted(servicio.CASOS_CONTROL) if servicio.servible(f) and f != "VOL-GARCH-001")
    caso = servicio.CASOS_CONTROL[ficha][0]
    r = motor.servir({"operacion": ficha, "datos": caso.get("datos") or [], "parametros": dict(caso.get("parametros") or {})}, "AG-21")
    assert str(r["estado"]).startswith("SERVED")
    assert "fecha_corte" in contratos.CAMPOS_MINIMOS["CT-09"]
    parrafo = g.parrafos_anexo_b()["CT-09"]
    assert "obligatoria siempre" not in parrafo and "la exige la mensajería" in parrafo


# ================================================================ T-143 r03 (QA r02, H-07) · la `memoria` de cada orden CT-05
@pytest.fixture(scope="module")
def ordenes_integracion(tmp_path_factory):
    """Las órdenes CT-05 que el ejecutor pasa a `_invocar` (la de INTEGRACION no pasa por la mensajería), en un ciclo V5 y en
    uno V6, con dos tipos de activo para que sea corto."""
    import conftest
    vistas = {}
    # r04 (QA r03, H-12 y H-13): también el V6 sin Sintetizador; el espía anota (esquema, orden) de CT-05 y (contrato, esquema)
    # de todas las invocaciones
    configs = {"v5": None, "v6": {"diseno": "v6"}, "v6_sin_sintetizador": {"diseno": "v6", "v6": {"sintetizador": False}}}
    for diseno, extra in configs.items():
        cfg = conftest.config_pruebas(**extra) if extra else None
        b = conftest.nuevo_bloque(tmp_path_factory.mktemp(diseno), conftest.cargar_universo(conftest.RUTA_UNIVERSO_EJEMPLO), cfg=cfg)
        vistas[diseno], vistas[diseno + "_invocaciones"], invocar = [], set(), b._invocar

        def espia(agente, contrato, msg, esquema, *args, _vistas=vistas[diseno], _todas=vistas[diseno + "_invocaciones"],
                  _invocar=invocar, **kwargs):
            _todas.add((contrato, esquema))
            if contrato == "CT-05":
                _vistas.append((esquema, copy.deepcopy(msg)))
            return _invocar(agente, contrato, msg, esquema, *args, **kwargs)

        b._invocar = espia
        b.ciclo(FECHA, alcance={"clases": ["RV", "MP"]})
    return vistas


def _memorias_que_difieren(parrafo, ordenes):
    """Lo que difiere entre lo que el Anexo B dice que lleva `memoria` (y `delta_gc0`) en cada tipo de orden CT-05 y las órdenes
    que emite el ejecutor."""
    reglas = {"ciclo": r"En la orden del ciclo \(PERIODICO, AD_HOC o PROFUNDIZACION\), `memoria` lleva ([^(]*)\(",
              "SEGUIMIENTO": r"En SEGUIMIENTO, `memoria` lleva ([^,]*), y `delta_gc0` va vacío",
              "INTEGRACION": r"En INTEGRACION, `memoria` lleva (.*?), y `delta_gc0`, solo los motivos de GC0 de cada tipo de activo"}
    dichas, difieren = {}, []
    for tipo, rx in reglas.items():
        m = re.search(rx, parrafo)
        if not m:
            difieren.append((tipo, "el Anexo B no lo dice"))
        dichas[tipo] = _nombres(m.group(1)) if m else set()
    for orden in ordenes:
        tipo = orden["tipo"] if orden["tipo"] in ("SEGUIMIENTO", "INTEGRACION") else "ciclo"
        if set(orden["memoria"]) != dichas[tipo]:
            difieren.append((orden["tipo"], f"`memoria` lleva {sorted(orden['memoria'])}; el Anexo B dice {sorted(dichas[tipo])}"))
        delta = orden["delta_gc0"]
        if tipo == "SEGUIMIENTO" and delta != {}:
            difieren.append((orden["tipo"], f"`delta_gc0` no va vacío: {delta}"))
        if tipo == "INTEGRACION" and not all(isinstance(v, list) for v in delta.values()):
            difieren.append((orden["tipo"], "`delta_gc0` no lleva solo los motivos de cada tipo de activo"))
    return difieren


def _ordenes_ct05(flujos, ordenes_integracion):
    del_ciclo = [m for m in g.todos_los_mensajes(flujos) if m["contrato"] == "CT-05" and m["tipo_mensaje"] == "ENCARGO"]
    return del_ciclo + [msg for esquema, msg in ordenes_integracion["v5"] if esquema == "INTEGRACION"]


def test_t143_r03_la_memoria_de_cada_orden_ct05_es_la_del_anexo_b(flujos, ordenes_integracion):
    """QA r02 de T-143, H-07 (C18, C19, D23): la `memoria` de la orden del ciclo, de SEGUIMIENTO y de INTEGRACION, y su
    `delta_gc0`, son los que dice el Anexo B; en el diseño V6 no hay orden INTEGRACION, como dice el Anexo B."""
    ordenes = _ordenes_ct05(flujos, ordenes_integracion)
    assert {o["tipo"] for o in ordenes} >= {"PERIODICO", "AD_HOC", "SEGUIMIENTO", "INTEGRACION"}
    assert _memorias_que_difieren(g.parrafos_anexo_b()["CT-05"], ordenes) == []
    assert "INTEGRACION" not in [e for e, _ in ordenes_integracion["v6"]] and "INTEGRACION" in [e for e, _ in ordenes_integracion["v5"]]
    assert "En el diseño V6 (con `v6.sintetizador`, el valor por defecto) no hay orden INTEGRACION" in g.parrafos_anexo_b()["CT-05"]


@pytest.mark.parametrize("cambio", [
    lambda p, o: (p.replace("`opp_vigentes`, `tnd_activas`, `lec_aplicables` y `certificados`", "`opp_vigentes`"), o),
    lambda p, o: (p.replace("`memoria` lleva `senales_interes`", "`memoria` lleva `opp_vigentes`"), o),
    lambda p, o: (p, [{**x, "memoria": {"senales": x["memoria"]["senales_interes"]}} if x["tipo"] == "SEGUIMIENTO" else x for x in o]),
    lambda p, o: (p, [{**x, "memoria": {"run_previo": None, "top3_anterior": None}} if x["tipo"] == "INTEGRACION" else x for x in o]),
    lambda p, o: (p, [{**x, "delta_gc0": {"RV": {}}} if x["tipo"] == "SEGUIMIENTO" else x for x in o]),
], ids=["D23 la prosa cambia la memoria del ciclo", "la prosa da a SEGUIMIENTO otra memoria", "C18 SEGUIMIENTO con otra clave",
        "C19 INTEGRACION con otra clave", "SEGUIMIENTO con delta_gc0"])
def test_t143_r03_un_cambio_en_la_memoria_se_nota(flujos, ordenes_integracion, cambio):
    parrafo, ordenes = g.parrafos_anexo_b()["CT-05"], _ordenes_ct05(flujos, ordenes_integracion)
    nuevo, cambiadas = cambio(parrafo, ordenes)
    assert nuevo != parrafo or cambiadas != ordenes, "el mutante no cambia nada: actualícelo"
    assert _memorias_que_difieren(nuevo, cambiadas) != []


# ================================================================ T-143 r04 (QA r03, H-12 a H-15)
def test_t143_r04_lo_que_cambia_en_el_v6_es_lo_que_dice_el_anexo_b(ordenes_integracion):
    """QA r03 de T-143, H-12 y H-13: con el V6 por defecto no hay orden INTEGRACION ni curación por el Curador, y CT-15 va con
    `SINTESIS`; con `v6.sintetizador` desactivado, el V6 emite la orden INTEGRACION y CT-15 va con `REDACCION`; el V5 pide la
    curación (los dos tipos del ciclo corto van en N2)."""
    v5, v6, v6_sin = (ordenes_integracion[k + "_invocaciones"] for k in ("v5", "v6", "v6_sin_sintetizador"))
    assert {("CT-05", "INTEGRACION"), ("CT-11", "CURACION"), ("CT-15", "REDACCION")} <= v5
    # El ciclo simulado sale APTO en HT-09 y no llega a CT-14: el dictamen del V6 lo mide `test_t143_r04b_dictamen_g3_del_v6`
    assert ("CT-15", "SINTESIS") in v6 and not {("CT-05", "INTEGRACION"), ("CT-11", "CURACION")} & v6
    assert {("CT-05", "INTEGRACION"), ("CT-15", "REDACCION")} <= v6_sin and ("CT-15", "SINTESIS") not in v6_sin
    p = g.parrafos_anexo_b()
    assert all(f in p[ct] for ct in ("CT-05", "CT-11", "CT-14", "CT-15") for f in FRASES_FIJAS[ct])


def _piezas_de_busqueda(tmp_path, referencias):
    """Las piezas que `_peticion_conocimiento` forma con una respuesta de `BUSQUEDA` dada (cliente sustituido), en backtest, con
    dos REF- ofrecidas (REF-2026-0001 y REF-2026-0002)."""
    import types

    import conftest
    import pandas as pd
    b = conftest.nuevo_bloque(tmp_path, conftest.cargar_universo(conftest.RUTA_UNIVERSO_EJEMPLO))
    assert b.modo == "backtest"
    b.referencias.para_clase = lambda *a, **k: {"referencias": [{"ref_id": f"REF-2026-000{i}", "anio": 2025} for i in (1, 2, 3)]}
    b._invocar = lambda *a, **k: types.SimpleNamespace(datos={"referencias": referencias, "sintesis": "La síntesis.", "lagunas": []})
    out = b._peticion_conocimiento("RV", {"proxy": "EJEMPLO", "horizontes_aplicables": ["H3"]}, {"tipo": "CT-08", "pregunta": "¿?"},
                                   None, pd.Timestamp(FECHA), "RUN-2026-0001", None)
    return out["piezas"]


def test_t143_r04_lo_que_el_ejecutor_lee_de_cada_referencia_es_lo_que_dice_el_anexo_b(tmp_path):
    """QA r03 de T-143, H-10, H-14 y H-15 (C28, D30, D31): sin `afirmacion`, la pieza toma la síntesis; sin `direccion`, neutra;
    `extracto` o, si no, `motivo`; en backtest, solo las REF- ofrecidas; solo las tres primeras referencias."""
    piezas = _piezas_de_busqueda(tmp_path, [
        {"ref_id": "REF-1999-0009", "afirmacion": "No ofrecida."},                                     # backtest: fuera
        {"ref_id": "REF-2026-0001"},                                                                   # sin afirmación ni dirección
        {"ref_id": "REF-2026-0002", "afirmacion": "Con todo.", "direccion": "favorable", "motivo": "Por el motivo."},
        {"ref_id": "REF-2026-0003", "afirmacion": "La cuarta."}])                                      # cuarta: fuera
    assert [(x["fuente"], x["afirmacion"], x["direccion"], x["extracto"]) for x in piezas] == [
        ("REF-2026-0001", "La síntesis.", "neutra", ""), ("REF-2026-0002", "Con todo.", "favorable", "Por el motivo.")]
    p = g.parrafos_anexo_b()["CT-07"]
    assert "`afirmacion`, `direccion`, `extracto` (o, si no hay, `motivo`) y `pronostico_fuente`" in p
    assert all(f in p for f in FRASES_FIJAS["CT-07"])


@pytest.mark.parametrize("viejo, nuevo", [("y sin `direccion`, neutra.", "y sin `direccion`, favorable."),
                                          ("En backtest solo cuentan las referencias registradas que se le ofrecieron.", ""),
                                          ("Solo usa las tres primeras referencias de la respuesta.", ""),
                                          ("toma además, si lo trae, `objeto`", "toma además, si lo trae, `objeto_auditado`")],
                         ids=["D30 otra dirección por defecto", "D31 sin la regla de backtest", "sin las tres primeras", "otra clave del hallazgo"])
def test_t143_r04_un_cambio_en_esas_frases_se_nota(a_mano, viejo, nuevo):
    parrafos = g.parrafos_anexo_b()
    ct = next(c for c in ("CT-07", "CT-17") if viejo in parrafos[c])
    parrafos[ct] = parrafos[ct].replace(viejo, nuevo)
    assert _esquemas_de_respuesta_que_difieren(contratos.ESQUEMAS, parrafos, a_mano[0]) != []


def test_t143_r04_de_cada_hallazgo_el_ejecutor_toma_objeto(tmp_path):
    """QA r03 de T-143, H-14 (C29): `_auditar` toma de cada hallazgo de `AUDITORIA` su `objeto` y, si no lo trae, el run."""
    import types

    import conftest
    import pandas as pd
    b = conftest.nuevo_bloque(tmp_path, conftest.cargar_universo(conftest.RUTA_UNIVERSO_EJEMPLO),
                              cfg=conftest.config_pruebas(auditoria={"en_backtest": True}))
    b._invocar = lambda *a, **k: types.SimpleNamespace(datos={"resumen": "Dos hallazgos.", "hallazgos": [
        {"regla": "R13", "descripcion": "Con objeto.", "severidad": "Menor", "objeto": "OPP-2026-0007"},
        {"regla": "R1", "descripcion": "Sin objeto.", "severidad": "Menor"}]})
    resultado = {"paquete": {"clases": {}, "limitaciones": []}, "g3_entregables": {},
                 "entregables": {"informe_tecnico": "a", "informe_visual": "b", "paquete_json": "c"}}
    b._auditar(resultado, "PERIODICO", {"RV": "N2"}, pd.Timestamp(FECHA), "RUN-2026-0001")
    hal = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "HAL"]
    assert [(e["regla_o_punto"], e["objeto"]) for e in hal] == [("R13", "OPP-2026-0007"), ("R1", "RUN-2026-0001")]
    assert FRASES_FIJAS["CT-17"][0] in g.parrafos_anexo_b()["CT-17"]


# ================================================================ T-143 ronda de cierre (QA r04, H-16)


@pytest.mark.parametrize("resultado, esperado", [("ADVERTENCIA", "APTO_CON_ADVERTENCIAS"), ("BLOQUEO", "BLOQUEADO")])
@pytest.mark.parametrize("diseno, extra", [("V5", {}), ("V6", {"diseno": "v6"}),
                                           ("V6 con dictamen_g3_llm", {"diseno": "v6", "v6": {"dictamen_g3_llm": True}})],
                         ids=["V5", "V6", "V6 con dictamen_g3_llm"])
def test_t143_r04b_dictamen_g3_del_v6(tmp_path, monkeypatch, diseno, extra, resultado, esperado):
    """QA r04 de T-143, H-16 a (E01): con HT-09 en ADVERTENCIA o BLOQUEO, `_validar_g3` emite el CT-14 en el V5, en el V6 y en el
    V6 con `v6.dictamen_g3_llm`; pide `DICTAMEN_G3` a AG-18 salvo en el V6 por defecto, donde el dictamen lo da la regla (apto
    con advertencias sin bloqueos, bloqueado con ellos), como dice el Anexo B."""
    import types

    import conftest
    import pandas as pd

    from bloque_a import orquestacion
    b = conftest.nuevo_bloque(tmp_path, conftest.cargar_universo(conftest.RUTA_UNIVERSO_EJEMPLO),
                              cfg=conftest.config_pruebas(**extra) if extra else None)
    creados, invocados = [], []
    crear = b.mensajeria.crear
    monkeypatch.setattr(b.mensajeria, "crear", lambda ct, *a, **k: (creados.append(ct), crear(ct, *a, **k))[1])
    monkeypatch.setattr(b, "_invocar", lambda ag, ct, msg, esq, *a, **k: (
        invocados.append((ag, ct, esq)), types.SimpleNamespace(datos={"dictamen": "APTO_CON_ADVERTENCIAS", "motivo": "m"}))[1])
    comp = [{"id": "C05", "resultado": resultado, "incidencias": [{"ruta": "x", "detalle": "d"}]}]
    monkeypatch.setattr(orquestacion.sint, "ht09_validar", lambda *a, **k: {"dictamen": resultado, "comprobaciones": comp})
    _, res = b._validar_g3({"clases": {}, "limitaciones": []}, {}, pd.Timestamp(FECHA), "RUN-2026-0001")
    assert "CT-14" in creados
    assert (("AG-18", "CT-14", "DICTAMEN_G3") in invocados) == (diseno != "V6")
    assert res["dictamen"] == esperado
    assert FRASES_FIJAS["CT-14"][1] in g.parrafos_anexo_b()["CT-14"]


class _TrasLaCuracion(Exception):
    """Corta `_registrar_evidencia_clase` en la primera invocación: lo que viene después de la curación no se mide aquí."""


@pytest.mark.parametrize("nivel", ["N1", "N2"])
@pytest.mark.parametrize("diseno, extra", [("V5", {}), ("V6", {"diseno": "v6"}),
                                           ("V6 con curacion_llm", {"diseno": "v6", "v6": {"curacion_llm": True}})],
                         ids=["V5", "V6", "V6 con curacion_llm"])
def test_t143_r04b_curacion_por_nivel_y_diseno(tmp_path, monkeypatch, diseno, extra, nivel):
    """QA r04 de T-143, H-16 b (E02, E03): `_registrar_evidencia_clase` emite el CT-11 solo en N2 (no en N1), y en el V6 solo
    con `v6.curacion_llm`, como dice el Anexo B."""
    import conftest
    import pandas as pd
    b = conftest.nuevo_bloque(tmp_path, conftest.cargar_universo(conftest.RUTA_UNIVERSO_EJEMPLO),
                              cfg=conftest.config_pruebas(**extra) if extra else None)
    creados = []
    crear = b.mensajeria.crear
    monkeypatch.setattr(b.mensajeria, "crear", lambda ct, *a, **k: (creados.append(ct), crear(ct, *a, **k))[1])

    def invocar(ag, ct, *a, **k):
        raise _TrasLaCuracion(ct)
    monkeypatch.setattr(b, "_invocar", invocar)
    monkeypatch.setattr(b, "_filtrar_evidencia", lambda *a, **k: None)
    an = {"clase": "RV", "nivel": nivel, "finalistas": [{"proxy": "EJEMPLO", "_piezas": [
        {"afirmacion": "a", "fuente": "REF-2026-0001", "direccion": "neutra", "extracto": "e"}]}]}
    try:
        b._registrar_evidencia_clase(an, pd.Timestamp(FECHA), "RUN-2026-0001")
    except _TrasLaCuracion:
        pass
    assert ("CT-11" in creados) == (nivel == "N2" and diseno != "V6")
    assert FRASES_FIJAS["CT-11"][0] in g.parrafos_anexo_b()["CT-11"]
