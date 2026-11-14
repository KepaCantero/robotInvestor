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
CON_CAMPOS = [f"CT-{n:02d}" for n in (*range(1, 16), 22, 23, 24, 25)]
SIN_CAMPOS = [f"CT-{n}" for n in range(16, 22)]   # CT-22 tiene un campo nombrado en el Anexo B (QA r01, H-02)


def test_ca4_hay_esquema_derivado_para_cada_contrato_con_campos_en_el_anexo_b(a_mano):
    esquemas, ejemplos = a_mano
    assert sorted({clave.split(".")[0] for clave in esquemas}) == CON_CAMPOS
    assert set(esquemas) == set(ejemplos)
    assert all(clave.split(".")[1] in ("ENCARGO", "RETORNO") for clave in esquemas)
    assert g.sin_campos_en_anexo_b(esquemas) == SIN_CAMPOS
    assert _congelado("divergencias_anexo_b.json")["contratos_sin_campos_en_el_anexo_b"] == SIN_CAMPOS


def test_ca4_de_ct16_a_ct22_el_anexo_b_solo_nombra_el_tipo_de_ct22(a_mano):
    """QA r01, H-02: el párrafo «CT-16 a CT-22» remite a los prompts y solo nombra un campo, `tipo` de CT-22, con dos
    valores que «admite además». El esquema derivado dice eso y nada más: el campo, sin lista cerrada."""
    esquemas, ejemplos = a_mano
    parrafo = g.parrafos_anexo_b()["CT-22"]
    assert all(g.parrafos_anexo_b()[ct] == parrafo for ct in SIN_CAMPOS)
    assert re.findall(r"`([^`]+)`", parrafo) == ["tipo", "CONSULTA_RECURRENTE", "DECISION_SEGUIMIENTO"] and "En CT-22, `tipo` admite además" in parrafo
    esquema = esquemas["CT-22.ENCARGO"]
    assert {k: v for k, v in esquema.items() if k not in ("$comment", "$schema")} == {
        "type": "object", "required": ["tipo"], "properties": {"tipo": {"examples": ["CONSULTA_RECURRENTE", "DECISION_SEGUIMIENTO"]}}}
    assert "CT-22.RETORNO" not in esquemas and "lista es abierta" in esquema["$comment"]
    validador = jsonschema.Draft202012Validator(esquema)
    assert validador.is_valid(ejemplos["CT-22.ENCARGO"]) and validador.is_valid({"tipo": "PREGUNTA_REPETIDA"})
    assert not validador.is_valid({"tipo_aviso": "CONSULTA_RECURRENTE"})


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
    assert comprobados > 150


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
    """QA r01, H-05: el Anexo B no dice qué campos lleva un retorno RECHAZADO o SIN_RESULTADO. No se inventa: se declara en
    cada esquema de retorno y en el README de los goldens."""
    esquemas, _ = a_mano
    retornos = [clave for clave in esquemas if clave.endswith(".RETORNO")]
    assert len(retornos) == 15
    for clave in retornos:
        assert "RECHAZADO" in esquemas[clave]["$comment"] and "no sirve para juzgar los otros" in esquemas[clave]["$comment"], clave
        assert "if" not in esquemas[clave], clave
    assert "ACLARACION_REQUERIDA" in esquemas["CT-09.RETORNO"]["$comment"] and "ACLARACION_REQUERIDA" in g.parrafos_anexo_b()["CT-09"]
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
    cambiados["CT-13.RETORNO"]["properties"]["objeciones"]["items"]["properties"]["cns_id"] = {}
    assert g.campos_fuera_de_su_parrafo(cambiados, parrafos) == [("CT-10.ENCARGO", "semilla"), ("CT-13.RETORNO", "cns_id"),
                                                                 ("CT-24.ENCARGO", "alcance"), ("CT-24.ENCARGO", "regiones")]
    doc0 = next((g.BLOQUE / "01_Gobernanza").glob("Documento 0*.md")).read_text(encoding="utf-8")
    anexo = doc0[doc0.index("## ANEXO B."):doc0.index("## ANEXO C.")]
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


def test_ca7_el_tipo_de_ct22_que_el_ejecutor_emite_en_tipo_aviso_esta_congelado(a_mano, flujos, tmp_path):
    """QA r01, H-02: el Anexo B nombra `tipo` de CT-22 con CONSULTA_RECURRENTE y DECISION_SEGUIMIENTO; el ejecutor los emite
    en `tipo_aviso`. La diferencia se mide con los mensajes que crea el ejecutor y está en el golden y en INC-T114-01."""
    esquemas, ejemplos = a_mano
    avisos = [m for m in g.todos_los_mensajes(flujos) if m["contrato"] == "CT-22"]
    assert sorted({(m.get("tipo"), m.get("tipo_aviso")) for m in avisos}, key=str) == [
        ("DECISIONES_BROKER", None), ("PREGUNTA_REPETIDA", None), (None, "CONSULTA_RECURRENTE"), (None, "DECISION_SEGUIMIENTO")]
    congelado = _congelado("divergencias_anexo_b.json")
    en_otro = congelado["valores_que_el_anexo_b_nombra_en_un_campo_y_el_ejecutor_emite_en_otro"]
    assert en_otro["CT-22.ENCARGO"] == [
        {"campo_del_anexo_b": "tipo", "campo_del_ejecutor": "tipo_aviso", "valor": "CONSULTA_RECURRENTE"},
        {"campo_del_anexo_b": "tipo", "campo_del_ejecutor": "tipo_aviso", "valor": "DECISION_SEGUIMIENTO"}]
    assert congelado["mensajes_de_los_flujos_simulados_que_no_cumplen_el_anexo_b"]["CT-22.ENCARGO"] == ["(raíz): 'tipo' is a required property"]
    assert congelado["por_contrato"]["CT-22.ENCARGO"] == {"el_ejecutor_admite_que_falte": ["tipo"]}
    # si el ejecutor los emitiera en `tipo`, como dice el Anexo B, la diferencia desaparecería: el golden cambiaría
    corregidos = [{**{k: v for k, v in m.items() if k != "tipo_aviso"}, "tipo": m["tipo_aviso"]} if "tipo_aviso" in m else m for m in avisos]
    sin = g.divergencias(esquemas, ejemplos, corregidos, tmp_path, FECHA)
    assert "CT-22.ENCARGO" not in sin["valores_que_el_anexo_b_nombra_en_un_campo_y_el_ejecutor_emite_en_otro"]
    assert "CT-22.ENCARGO" not in sin["mensajes_de_los_flujos_simulados_que_no_cumplen_el_anexo_b"]
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
        "01_Gobernanza/Documento 0 - Protocolo maestro del Bloque A - Versión óptima V5.1.md",
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
    assert rechazados == ["CT-11.ENCARGO", "CT-12.ENCARGO", "CT-13.ENCARGO"]
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
    assert f["pregunta_repetida"]["mensajes"]["CT-22.ENCARGO"]["valores_de_listas_abiertas"] == {"tipo": ["PREGUNTA_REPETIDA"]}
    assert f["decision_broker"]["mensajes"]["CT-22.ENCARGO"]["valores_de_listas_abiertas"] == {"tipo": ["DECISIONES_BROKER"]}
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
