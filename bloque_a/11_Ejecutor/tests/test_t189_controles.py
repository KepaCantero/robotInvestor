import pytest
from bloque_a.configuracion import parametro
from bloque_a.consumo import Presupuesto
from bloque_a.contratos import DatosSensibles
from conftest import AS_OF, config_pruebas, nuevo_bloque


def test_ct04_rechaza_lista_global_incompatible(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    horizontes = ["H1", "H2", "H3", "H4"]
    resultado = b.decision({"configuracion": {"horizontes": horizontes}}, AS_OF)
    assert b.f10("2026-12-31")["P-03"] == horizontes
    assert {e["parametro"] for e in resultado["rechazos"]} == {
        "horizontes:FON:H1", "horizontes:INM:H1", "horizontes:ALT:H1", "horizontes:ALT:H2",
        "horizontes:MON:H4", "horizontes:DER:H4",
    }
    assert all(e["motivo"] for e in resultado["rechazos"])


@pytest.mark.parametrize("invalido", [[], None, "H1", ["H3", "H3"]])
def test_p03_rechaza_forma_invalida(tmp_path, universo, invalido):
    b = nuevo_bloque(tmp_path, universo)
    antes = b.almacen.leer("F10")
    respuesta = b.decision({"configuracion": {"horizontes": invalido}}, AS_OF)
    assert [r["parametro"] for r in respuesta["rechazos"]] == ["horizontes"]
    assert b.almacen.leer("F10") == antes


def test_seguridad_solo_etiquetas(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    with pytest.raises(DatosSensibles):
        b.decision({"valoracion_informe": {"nota": "ES91 2100 " + "0418 4502 0005 1332",
                                           "api_key": "valor-" + "ficticio"}}, AS_OF)
    inc = b.almacen.leer("HA")[-1]
    assert set(inc["tipos_dato"]) == {"IBAN", "CLAVE_API"}


def test_aut_con_valor_ganado(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["MP"]}, presupuesto_override={"MP": 6.0})
    aut = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "AUT" and e.get("bolsa") == "MP"]
    assert {e["decision"] for e in aut} == {"AUTORIZADA", "DENEGADA"}
    assert r["presupuesto"]["MP"]["consumido"] > 0
    assert any(e["ev"] > 0 and e["cpi"] for e in aut)
    assert all(e["motivo"] for e in aut)
    # INC-T189-01: el EAC se informa. La autorización depende del tope de la bolsa y de la fase.
    assert any(e["eac"] > 1.5 * e["bac"] and e["decision"] == "AUTORIZADA" for e in aut if e["eac"])
    for e in aut:
        assert bool(e["condiciones"]) == (e["decision"] == "AUTORIZADA")
        if e["ev"] and e["ac"]:
            assert e["cpi"] == pytest.approx(e["ev"] / e["ac"])
            assert e["eac"] == pytest.approx(e["ac"] + (e["bac"] - e["ev"]) / e["cpi"])
        else:
            assert e["eac"] is None


def test_valor_ganado_de_fases_realmente_servidas():
    cfg = config_pruebas()
    pres = Presupuesto({"MP": 8}, cfg)
    pres.cargar("MP", 2)
    assert pres.valor_ganado("MP", "prospectiva") == {"bac": 8, "ac": 2, "ev": 0, "cpi": 0, "eac": None}
    for fase in ("cribado", "investigacion", "prospectiva"):
        pres.registrar_fase_servida("MP", fase)
    pesos = parametro(cfg, "presupuesto_uc.reparto_fases")
    ev = 8 * (pesos["cribado"] + pesos["investigacion"])
    assert pres.valor_ganado("MP", "prospectiva") == pytest.approx(
        {"bac": 8, "ac": 2, "ev": ev, "cpi": ev / 2, "eac": 2 + (8 - ev) / (ev / 2)}
    )


@pytest.mark.parametrize(("texto", "tipo"), [
    ("4111 1111 " + "1111 1111", "TARJETA"),
    ("correo" + "@example.com", "CORREO"),
    ("1234" + "5678Z", "IDENTIFICACION_PERSONAL"),
    ("DE89 3704 " + "0044 0532 0130 00", "IBAN"),
    ("ES91 2100 " + "0418 4502 0005 1332", "IBAN"),
    ("sk-ant-" + "api03-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", "CLAVE_API"),
])
def test_tipo_sin_valor_en_almacen(tmp_path, universo, texto, tipo):
    b = nuevo_bloque(tmp_path, universo)
    with pytest.raises(DatosSensibles) as error:
        b.decision({"valoracion_informe": {"comentario": texto}}, AS_OF)
    assert texto not in str(error.value)
    assert b.almacen.leer("HA")[-1]["tipos_dato"] == [tipo]
    assert not any(texto.encode() in p.read_bytes() for p in tmp_path.rglob("*") if p.is_file())


@pytest.mark.parametrize("anidado", [False, True])
def test_nombre_sensible_se_enmascara(tmp_path, universo, anidado):
    b = nuevo_bloque(tmp_path, universo)
    clave = "sk-ant-" + "api03-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    cuerpo = {clave: "texto"}
    cuerpo = {"valoracion_informe": cuerpo} if anidado else {"valoracion_informe": {}, **cuerpo}
    with pytest.raises(DatosSensibles) as error:
        b.decision(cuerpo, AS_OF)
    assert clave not in str(error.value)
    inc = b.almacen.leer("HA")[-1]
    assert inc["campo_afectado"] == (["valoracion_informe"] if anidado else ["campo_protegido"])
    assert inc["tipos_dato"] == ["CLAVE_API"]
    assert not any(clave.encode() in p.read_bytes() for p in tmp_path.rglob("*") if p.is_file())


def test_vias_de_consultas_y_credenciales(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    correo = "buzon" + "@example.org"
    with pytest.raises(DatosSensibles):
        b.consultas.enviar({"tipo": "DATO_O_DOCUMENTO", "preguntas": [{"texto": correo, "supuesto_declarado": "Actual"}]}, AS_OF)
    assert b.almacen.leer("HA")[-1]["tipos_dato"] == ["CORREO"]
    valor = "dato-" + "ficticio"
    b.credenciales.desde_retorno({"valor": valor}, "AG-16", AS_OF)
    assert b.almacen.leer("HA")[-1]["tipos_dato"] == ["CREDENCIAL"]
    opaco = "a123456789" * 4
    b.credenciales.desde_retorno({"solicitudes_credenciales": [{"motivo": opaco}]}, "AG-16", AS_OF)
    assert b.almacen.leer("HA")[-1]["tipos_dato"] == ["CREDENCIAL"]
    solicitud = b.credenciales.solicitar("servicio de prueba", "AG-16", "prueba", "sin datos", as_of=AS_OF)
    b.credenciales.responder({"crd_id": solicitud["crd_id"], "estado": "PROVISTA", "valor": valor}, AS_OF)
    assert b.almacen.leer("HA")[-1]["tipos_dato"] == ["CREDENCIAL"]
    assert not any(v.encode() in p.read_bytes() for p in tmp_path.rglob("*") if p.is_file() for v in (correo, opaco, valor))


def test_ct04_compone_el_calendario_y_los_horizontes_en_el_mismo_dia(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    primero = b.decision({"configuracion": {"dia_hora_entrega": "MIE 08:00", "horizontes": ["H1", "H3"]}}, AS_OF)
    assert set(primero["aplicado"]) == {"P-01", "P-03"}
    assert {e["parametro"] for e in primero["rechazos"]} == {"horizontes:FON:H1", "horizontes:INM:H1", "horizontes:ALT:H1"}
    segundo = b.decision({"configuracion": {"periodicidad": "QUINCENAL", "horizontes": ["H1", "H3"]}}, AS_OF)
    assert set(segundo["aplicado"]) == {"P-01"}
    vigente = b.f10("2026-06-06")
    assert vigente["P-01"] == "QUINCENAL · LUN 07:00 · entrega MIE 08:00"
    assert vigente["P-03"] == ["H1", "H3"]
    cambios = [e for e in b.almacen.leer("F10") if e.get("tipo_entrada") == "CFG"]
    assert [e["param_id"] for e in cambios].count("P-03") == 1
    assert len([e for e in cambios if e["param_id"] == "P-01"]) == 2
