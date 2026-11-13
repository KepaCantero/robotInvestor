"""T-114 · Fase 3: los contratos CT-01 a CT-25 están congelados en goldens comparados byte a byte.

Criterios de aceptación en `.docs/tickets/T-114/README.md`. La regla de re-congelado, en `tests/goldens/README.md`.
"""
import copy
import json
import re
import shutil

import goldens_ct as g
import jsonschema
import pytest

from bloque_a import contratos

CONTRATOS = [f"CT-{n:02d}" for n in range(1, 26)]


@pytest.fixture(scope="module")
def generados():
    return g.generar()


@pytest.fixture(scope="module")
def a_mano():
    return g.leer_a_mano()


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
CON_CAMPOS = [f"CT-{n:02d}" for n in (*range(1, 16), 23, 24, 25)]


def test_ca4_hay_esquema_derivado_para_cada_contrato_con_campos_en_el_anexo_b(a_mano):
    esquemas, ejemplos = a_mano
    assert sorted({clave.split(".")[0] for clave in esquemas}) == CON_CAMPOS
    assert set(esquemas) == set(ejemplos)
    assert all(clave.split(".")[1] in ("ENCARGO", "RETORNO") for clave in esquemas)
    assert g.sin_campos_en_anexo_b(esquemas) == [f"CT-{n}" for n in range(16, 23)]
    assert _congelado("divergencias_anexo_b.json")["contratos_sin_campos_en_el_anexo_b"] == [f"CT-{n}" for n in range(16, 23)]


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


def test_ca4_los_campos_de_cada_esquema_estan_en_el_anexo_b(a_mano):
    """Nada inventado: cada campo de primer nivel de un esquema derivado aparece, tal cual, en el Anexo B."""
    esquemas, _ = a_mano
    doc0 = next((g.BLOQUE / "01_Gobernanza").glob("Documento 0*.md")).read_text(encoding="utf-8")
    anexo = doc0[doc0.index("## ANEXO B."):doc0.index("## ANEXO C.")]
    for clave, esquema in esquemas.items():
        for campo in esquema["properties"]:
            assert f"`{campo}`" in anexo or f'"{campo}"' in anexo, (clave, campo)


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


def test_ca7_un_mensaje_del_ciclo_fuera_del_anexo_b_aparece(a_mano, tmp_path):
    esquemas, ejemplos = a_mano
    msg = {"contrato": "CT-09", "tipo_mensaje": "ENCARGO", **ejemplos["CT-09.ENCARGO"], "modo": "OTRO"}
    del msg["semilla"]
    difieren = g.divergencias(esquemas, ejemplos, [msg], tmp_path, "2026-06-05")
    assert difieren["mensajes_del_ciclo_simulado_que_no_cumplen_el_anexo_b"] == {
        "CT-09.ENCARGO": ["(raíz): 'semilla' is a required property", "modo: enum ['SYNC_CALC', 'ASYNC_CALC']"]}


def test_ca7_las_divergencias_estan_en_las_incidencias_y_en_la_deuda():
    raiz = g.BLOQUE.parent
    assert "INC-T114-01" in (raiz / "docs" / "incidencias.md").read_text(encoding="utf-8")
    deuda = (raiz / "sistema_global" / "seguimiento" / "Deuda_tecnica_y_pendientes_del_operador.md").read_text(encoding="utf-8")
    assert "| T-114 |" in deuda and "INC-T114-01" in deuda


# ---------------------------------------------------------------- CA-8 · generar dos veces da lo mismo
def test_ca8_dos_generaciones_seguidas_dan_el_mismo_texto(generados):
    assert g.generar() == generados


def test_ca8_las_formas_no_dependen_del_orden_de_los_mensajes(tmp_path, a_mano):
    capturados = g.capturar_ciclo(tmp_path, "2026-06-05")
    assert len(capturados) > 50 and {m["contrato"] for m in capturados} >= {"CT-02", "CT-05", "CT-06", "CT-11", "CT-15"}
    assert g.formas(capturados, a_mano[0]) == g.formas(capturados[::-1], a_mano[0]) == _congelado("formas_ciclo_mock.json")


# ---------------------------------------------------------------- huellas de lo que no se genera
def test_las_huellas_cubren_el_documento_0_los_esquemas_publicados_y_lo_escrito_a_mano(tmp_path):
    huellas = _congelado("huellas.json")
    assert sorted(huellas) == sorted([
        "01_Gobernanza/Documento 0 - Protocolo maestro del Bloque A - Versión óptima V5.1.md",
        "06_Plantillas_entregables/Esquema JSON - Informe de seguimiento de opción - V5.1.json",
        "06_Plantillas_entregables/Esquema JSON - Paquete de oportunidades - V5.0.json",
        "goldens/anexo_b_ejemplos.json", "goldens/anexo_b_esquemas.json"])
    copia = tmp_path / "goldens"
    shutil.copytree(g.CARPETA, copia)
    assert g.huellas(copia) == huellas
    ruta = copia / "anexo_b_esquemas.json"
    ruta.write_text(ruta.read_text(encoding="utf-8").replace('"INMEDIATA"', '"URGENTE"'), encoding="utf-8")
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
