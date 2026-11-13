"""T-92: regresiones de la revisión de Claude sobre la auditoría de Astra (rama astra/bloque-a-integridad-y-evidencia).

Cada prueba cubre un defecto de la rama, o una regla de develop (T-65) que la rama deshacía y que T-92 conserva.
Sin red ni claves: datos y SDK simulados.
"""
import json
from types import SimpleNamespace

import pandas as pd
import pytest
from bloque_a.almacen import Almacen
from bloque_a.consumo import Presupuesto
from bloque_a.contratos import MensajeInvalido, Mensajeria
from bloque_a.herramientas.ht01_datos import DatosNoDisponibles
from bloque_a.llm import AnthropicClient, contenido_sensible
from conftest import AS_OF, nuevo_bloque
from test_t87_datos import _csv, _evaluador


# ---------------------------------------------------------------------------------------------- R8 sin falsos positivos
@pytest.mark.parametrize("texto", [
    "Fuente: https://johnhcochrane.com/research-all/the-risk-and-return-of-venture-capital",
    "el risk-adjusted-return-of-the-portfolio mejora", "disk-encryption-at-rest-for-the-database",
    "task-force-on-climate-related-financial-disclosures",
    "https://news.example.com/sk-hynix-posts-record-quarterly-profit-2025", "ver informe sk-hynix-posts-record-quarterly-profit",
    "Fuente: sk-hynix_annual_report_2023.pdf", "ver sk-innovation_to_merge_with_enmove"])
def test_r8_no_confunde_palabras_con_sk_con_una_clave(texto):
    assert not contenido_sensible(texto)


SK = "s" + "k-"   # partido para que el escáner de secretos del repositorio no tome por real una clave ficticia


@pytest.mark.parametrize("texto", [f"clave {SK}ant-api03-{'A' * 24}", f'"{SK}proj-{"B" * 26}"', f"token={SK}{'C7' * 12}",
                                   f"OPENAI_KEY_{SK}Ab3{'x9' * 10}"])
def test_r8_sigue_detectando_claves_reales(texto):
    assert contenido_sensible(texto)


def test_r8_una_url_de_fuentes_llega_al_modelo():
    llamadas = []

    class SDK:
        messages = None

        def create(self, **kw):
            llamadas.append(kw)
            return SimpleNamespace(stop_reason="end_turn", usage=SimpleNamespace(input_tokens=5, output_tokens=5),
                                   content=[SimpleNamespace(type="text", text="ver the-risk-and-return-of-venture-capital")])
    sdk = SDK()
    sdk.messages = sdk
    r = AnthropicClient(sdk=sdk).generar(agente="AG-03", modelo="m", system=[{"type": "text", "text": "s"}],
                                         mensajes=[{"role": "user", "content": "https://x.org/the-risk-and-return-of-venture-capital"}],
                                         max_tokens=10)
    assert llamadas and r.stop_reason == "end_turn" and "risk" in r.texto


# ---------------------------------------------------------------------------------------------- sellos de integridad
def _con_tres(tmp):
    a = Almacen(tmp)
    for k in ("uno", "dos", "tres"):
        a.escribir("F5", "AG-01", {"id": k})
    return next(tmp.glob("F5*"))


def test_almacen_sellado_sin_fichero_de_sellos_falla_cerrado(tmp_path):
    f5 = _con_tres(tmp_path)
    lineas = f5.read_text(encoding="utf-8").splitlines()
    f5.write_text("\n".join(lineas[:-1]) + "\n", encoding="utf-8")
    (tmp_path / "sellos_integridad.json").unlink()
    with pytest.raises(ValueError, match="sellos"):
        Almacen(tmp_path)


def test_almacen_anterior_a_los_sellos_se_sella_al_abrir(tmp_path):
    _con_tres(tmp_path)
    (tmp_path / "sellos_integridad.json").unlink()
    (tmp_path / "formato_almacen.json").unlink()
    a = Almacen(tmp_path)
    assert list(a.estado("F5")) == ["uno", "dos", "tres"]
    assert (tmp_path / "sellos_integridad.json").exists() and (tmp_path / "formato_almacen.json").exists()
    assert Almacen(tmp_path).verificar_integridad("F5")["F5"]


# ---------------------------------------------------------------------------------------------- reconciliación de CT-01
def test_reserva_fallida_se_reconcilia_y_se_puede_reintentar(tmp_path):
    ms = Mensajeria(Almacen(tmp_path))
    m = ms.crear("CT-03", "BROKER", "AG-01", {"pregunta": "saldo"})
    with pytest.raises(RuntimeError):
        ms.procesar_una_vez(m, lambda _: (_ for _ in ()).throw(RuntimeError("secreto-que-no-debe-guardarse")))
    estado = ms.estado_reserva(m["msg_id"])
    assert estado == {"msg_id": m["msg_id"], "estado": "FALLIDO", "error": "RuntimeError"}
    assert "secreto" not in (tmp_path / "acuses.sqlite3").read_bytes().decode("latin-1")
    with pytest.raises(MensajeInvalido, match="interrumpido"):
        ms.procesar_una_vez(m, lambda _: pytest.fail("no se repite sin reconciliar"))
    with pytest.raises(MensajeInvalido, match="motivo"):
        ms.reconciliar(m["msg_id"], "  ")
    assert ms.reconciliar(m["msg_id"], "F5 revisado: sin efectos")["estado"] == "LIBERADA"
    inc = [e for e in ms.almacen.leer("HA") if "liberada por el operador" in str(e.get("detalle"))]
    assert len(inc) == 1
    assert ms.procesar_una_vez(m, lambda _: {"ok": 1}) == ({"ok": 1}, False)
    with pytest.raises(MensajeInvalido, match="COMPLETADO"):
        ms.reconciliar(m["msg_id"], "otra vez")
    assert ms.estado_reserva("MSG-2099-000001")["estado"] == "DESCONOCIDO"


def test_cinta_de_acuses_anterior_gana_la_columna_de_error(tmp_path):
    import sqlite3
    db = sqlite3.connect(tmp_path / "acuses.sqlite3")
    db.execute("CREATE TABLE acuses (id TEXT PRIMARY KEY, huella TEXT NOT NULL, respuesta TEXT)")
    db.execute("INSERT INTO acuses VALUES ('MSG-2026-000001', 'h', NULL)")
    db.commit()
    db.close()
    ms = Mensajeria(Almacen(tmp_path))
    assert ms.estado_reserva("MSG-2026-000001")["estado"] == "EN_CURSO"


# ---------------------------------------------------------------------------------------------- se conserva T-65
def test_fichas_documentadas_con_codigo_siguen_sin_cifras_citables(tmp_path, universo, monkeypatch):
    """T-112: las tres fichas se promovieron con sus casos de control; la regla se comprueba con el conjunto puesto a mano."""
    from bloque_a.motor import servicio
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    for ficha in ("ACC-ERP-001", "FX-MOM-001", "REI-CAP-001"):
        assert servicio.servible(ficha)
        monkeypatch.setattr(servicio, "DOCUMENTADAS_CON_CODIGO", frozenset({ficha}))
        r = b.motor.servir({"operacion": ficha}, "AG-02")
        assert r["estado"] == "RECHAZADO" and r["motivo"] == "METODO_NO_IMPLEMENTADO", (ficha, r)


def test_tope_de_ampliacion_sale_de_la_configuracion(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    cfg = json.loads(json.dumps(b.cfg))
    cfg["presupuesto_uc"]["ampliacion_max_autorizable"] = 0.30
    p = Presupuesto({"RV": 10}, cfg)
    p.cargar("RV", 12.5)
    assert p.autorizar_hasta_tope("RV", 1.0, True) == (False, 1.0)   # 13,5 > 10 × 1,30
    assert p.autorizar_hasta_tope("RV", 0.5, True) == (True, 0.5)    # 13,0 ≤ 13,0


# ---------------------------------------------------------------------------------------------- D02 con la frescura de T-65
def test_cesta_con_un_miembro_parado_no_se_resuelve_quitandolo(tmp_path):
    """El miembro Y deja de publicar tras la emisión: quitarlo de la CESTA sería usar información posterior (supervivencia)."""
    e = _evaluador(tmp_path)
    _csv(tmp_path, "X", "fecha,cierre\n2026-06-05,100\n2026-07-31,120\n")
    _csv(tmp_path, "Y", "fecha,cierre\n2026-06-05,100\n2026-06-08,50\n")
    e.proveedor.fijar_as_of("2026-08-03")
    bases = e.bases_cesta("RV", "2026-06-05")
    assert set(bases) == {"X", "Y"}
    with pytest.raises(DatosNoDisponibles):
        e.rentabilidad("CESTA", "RV", "2026-06-05", "2026-07-31", "H3", base=bases)


def test_base_posterior_a_la_emision_se_rechaza(tmp_path):
    e = _evaluador(tmp_path)
    _csv(tmp_path, "X", "fecha,cierre\n2026-06-05,100\n2026-07-31,120\n")
    e.proveedor.fijar_as_of("2026-08-03")
    with pytest.raises(DatosNoDisponibles, match="posterior"):
        e.rentabilidad("X", "RV", "2026-06-05", "2026-07-31", "H3", base={"valor": 100, "fecha": "2026-06-06"})
    for mala in (True, float("nan"), 0, "100"):
        with pytest.raises(DatosNoDisponibles):
            e.rentabilidad("X", "RV", "2026-06-05", "2026-07-31", "H3", base={"valor": mala, "fecha": "2026-06-05"})
    r, d = e.rentabilidad("X", "RV", "2026-06-05", "2026-07-31", "H3", base={"valor": 100, "fecha": "2026-06-05"})
    assert r == pytest.approx(0.2) and d == pd.Timestamp("2026-07-31")


def test_miembro_ya_parado_al_emitir_no_entra_en_la_cesta(tmp_path):
    """Lo contrario de D02: que un miembro ya no publicaba se sabía al emitir (PS2 de T-65), así que no entra en la CESTA."""
    e = _evaluador(tmp_path)
    _csv(tmp_path, "X", "fecha,cierre\n2026-06-05,100\n2026-07-31,120\n")
    _csv(tmp_path, "Y", "fecha,cierre\n2026-04-01,100\n")
    e.proveedor.fijar_as_of("2026-08-03")
    assert set(e.bases_cesta("RV", "2026-06-05", "H3")) == {"X"}
    assert set(e.bases_cesta("RV", "2026-06-05")) == {"X", "Y"}
    r, _ = e.rentabilidad("CESTA", "RV", "2026-06-05", "2026-07-31", "H3")
    assert r == pytest.approx(0.2)



# ---------------------------------------------------------------------------------------------- QA r01 de T-92
def test_r01_h06_cierre_no_positivo_o_repetido_al_emitir_no_entra_en_la_base(tmp_path):
    e = _evaluador(tmp_path)
    _csv(tmp_path, "X", "fecha,cierre\n2026-06-05,100\n2026-07-31,110\n")
    _csv(tmp_path, "Y", "fecha,cierre\n2026-06-04,100\n2026-06-05,-50\n2026-07-31,60\n")
    e.proveedor.fijar_as_of("2026-06-05")
    assert set(e.bases_cesta("RV", "2026-06-05", "H3")) == {"X"}
    with pytest.raises(DatosNoDisponibles):
        e._base_conocida("Y", "2026-06-05")
    _csv(tmp_path, "Y", "fecha,cierre\n2026-06-05,100\n2026-06-05,101\n2026-07-31,60\n")
    with pytest.raises(DatosNoDisponibles):
        e._base_conocida("Y", "2026-06-05")
    e.proveedor.fijar_as_of("2026-08-03")
    with pytest.raises(DatosNoDisponibles):
        e.rentabilidad("X", "RV", "2026-06-05", "2026-07-31", "H3", base={"valor": -100.0, "fecha": "2026-06-05"})


@pytest.mark.parametrize("fecha", ["no-es-fecha", 12345678901234567890, ["2026-06-05"]])
def test_r01_h14_fecha_ilegible_de_la_base_no_tumba_la_resolucion(tmp_path, fecha):
    e = _evaluador(tmp_path)
    _csv(tmp_path, "X", "fecha,cierre\n2026-06-05,100\n2026-07-31,110\n")
    e.proveedor.fijar_as_of("2026-08-03")
    with pytest.raises(DatosNoDisponibles):
        e.rentabilidad("X", "RV", "2026-06-05", "2026-07-31", "H3", base={"valor": 100.0, "fecha": fecha})


def test_r01_h08_msg_id_del_broker_en_su_propio_espacio(tmp_path):
    ms = Mensajeria(Almacen(tmp_path))
    interno = ms.crear("CT-03", "BROKER", "AG-01", {"pregunta": "x"})
    cuerpo = {"tipo": "AD_HOC", "alcance": {"clases": ["DIV"]}, "nivel_solicitado": "N1", "horizontes": ["H3"], "prioridad": "NORMAL"}
    with pytest.raises(MensajeInvalido, match="MSG-BRK"):
        ms.crear("CT-01", "BROKER", "AG-01", {**cuerpo, "msg_id": interno["msg_id"]})
    m = ms.crear("CT-01", "BROKER", "AG-01", {**cuerpo, "msg_id": "MSG-BRK-2026-000001"})
    assert m["msg_id"] == "MSG-BRK-2026-000001" and not interno["msg_id"].startswith("MSG-BRK-")


def test_r01_h13_la_respuesta_repetida_es_igual_a_la_primera(tmp_path):
    import datetime as dt
    ms = Mensajeria(Almacen(tmp_path))
    m = ms.crear("CT-03", "BROKER", "AG-01", {"pregunta": "x"})
    primera, rep1 = ms.procesar_una_vez(m, lambda _: {"cuando": dt.date(2026, 6, 5), "par": (1, 2)})
    segunda, rep2 = ms.procesar_una_vez(m, lambda _: pytest.fail("no se repite"))
    assert primera == segunda and (rep1, rep2) == (False, True)


def test_r01_h12_si_ha_falla_la_reserva_no_se_libera(tmp_path, monkeypatch):
    ms = Mensajeria(Almacen(tmp_path))
    m = ms.crear("CT-03", "BROKER", "AG-01", {"pregunta": "x"})
    with pytest.raises(RuntimeError):
        ms.procesar_una_vez(m, lambda _: (_ for _ in ()).throw(RuntimeError("x")))
    monkeypatch.setattr(ms.almacen, "incidencia", lambda *a, **k: (_ for _ in ()).throw(OSError("HA sin espacio")))
    with pytest.raises(OSError):
        ms.reconciliar(m["msg_id"], "F5 revisado")
    assert ms.estado_reserva(m["msg_id"])["estado"] == "FALLIDO"


def test_r01_h10_escritura_cortada_antes_del_sello_se_aparta_al_abrir(tmp_path):
    f5 = _con_tres(tmp_path)
    sellos = json.loads((tmp_path / "sellos_integridad.json").read_text())
    sello_dos = None
    lineas = f5.read_text(encoding="utf-8").splitlines()
    sello_dos = [2, json.loads(lineas[1])["_hash"]]
    sellos["F5"] = sello_dos                       # el proceso murió tras escribir el tercero y antes de sellarlo
    (tmp_path / "sellos_integridad.json").write_text(json.dumps(sellos))
    a = Almacen(tmp_path)
    assert list(a.estado("F5")) == ["uno", "dos"]
    aparte = f5.with_name(f5.name + ".no_confirmado.jsonl")
    assert json.loads(aparte.read_text(encoding="utf-8").splitlines()[0])["id"] == "tres"
    assert any("sin confirmar" in str(e.get("detalle")) for e in a.leer("HA"))
    assert Almacen(tmp_path).verificar_integridad()["F5"]
    # menos registros que el sello sigue siendo un fallo de integridad (truncado)
    f5.write_text(lineas[0] + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="sello"):
        Almacen(tmp_path)


def test_r01_h10_ctrl_c_durante_el_sello_no_deja_el_almacen_sin_abrir(tmp_path):
    from unittest.mock import patch
    a = Almacen(tmp_path)
    a.escribir("F5", "AG-01", {"id": "uno"})
    with patch.object(a, "_guardar_json", side_effect=KeyboardInterrupt), pytest.raises(KeyboardInterrupt):
        a.escribir("F5", "AG-01", {"id": "dos"})
    assert list(Almacen(tmp_path).estado("F5")) == ["uno"]


def test_r01_h15_un_plazo_con_solo_fecha_vence_al_terminar_el_dia(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    c = b.consultas.enviar({"tipo": "OTRA", "modo": "BLOQUEANTE", "clases": ["RV"],
                            "preguntas": [{"texto": "¿RV?", "supuesto_declarado": "esperar"}],
                            "plazo_respuesta": "2026-06-08"}, AS_OF)
    assert not b.consultas.vencer("2026-06-08T21:00Z")         # 23:00 en Madrid: aún dentro del día
    assert b.consultas.vencer("2026-06-08T22:00Z") == [c["cns_id"]]


def test_r01_h09_el_umbral_de_la_observacion_sale_de_la_configuracion(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    s = {"senal_compuesta": 0.55, "tendencia_26s": "alcista"}
    assert b._observacion_ht01("X", s)["direccion"] == "favorable"
    b.cfg["senales"]["umbral_favorable"] = 0.6
    assert b._observacion_ht01("X", s)["direccion"] == "contraria"


def test_t65_h05_el_tope_no_tiene_literales_de_respaldo(monkeypatch):
    """Lo que la rama de Astra traía (`cfg.get(..., 0.25)`): sin el parámetro, develop falla cerrado en lugar de inventarlo."""
    from bloque_a import configuracion
    monkeypatch.setattr(configuracion, "config_por_defecto", dict)
    p = Presupuesto({"RV": 10}, {"presupuesto_uc": {}})
    with pytest.raises(KeyError, match="ampliacion"):
        p.autorizar_hasta_tope("RV", 1.0, True)


# ---------------------------------------------------------------------------------------------- QA r02 de T-92
def _claves_realistas(n=2000, semilla=7):
    import random
    rnd = random.Random(semilla)
    alfa = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-"
    for i in range(n):
        cola = "".join(rnd.choice(alfa) for _ in range(rnd.randint(40, 120)))
        yield [f"{SK}ant-api03-{cola}", f"{SK}proj-{cola}", f"{SK}svcacct-{cola}", f"{SK}{cola}"][i % 4]


def test_r02_h17_r8_detecta_todas_las_claves_con_forma_real():
    from bloque_a.contratos import contiene_credenciales
    fallan = [k for k in _claves_realistas() if not contenido_sensible(f"clave: {k}") or not contiene_credenciales({"x": k})]
    assert not fallan, fallan[:3]


def test_r02_h17_r8_sin_retroceso_cuadratico():
    import time
    for texto in ("_" + SK) * 32768, ("a-" * 70000), (SK + "a-" * 70000), ("x" + SK) * 30000:
        t0 = time.perf_counter()
        contenido_sensible(texto)
        assert time.perf_counter() - t0 < 2.0


def test_r02_h18_una_clave_en_su_propia_linea_se_detecta():
    from bloque_a.contratos import contiene_credenciales
    clave = f"{SK}ant-api03-{'Ab9_' * 10}"
    assert contiene_credenciales({"pregunta": "mi clave es:\n" + clave})
    assert contiene_credenciales({"pregunta": "\t" + clave})


def test_r02_h19_mas_de_un_registro_sobre_el_sello_es_fallo_de_integridad(tmp_path):
    f5 = _con_tres(tmp_path)
    lineas = f5.read_text(encoding="utf-8").splitlines()
    sellos = json.loads((tmp_path / "sellos_integridad.json").read_text())
    sellos["F5"] = [1, json.loads(lineas[0])["_hash"]]          # un sello viejo: dos registros por encima
    (tmp_path / "sellos_integridad.json").write_text(json.dumps(sellos))
    with pytest.raises(ValueError, match="sello"):
        Almacen(tmp_path)
    assert f5.read_text(encoding="utf-8").splitlines() == lineas   # no se ha perdido nada confirmado


def test_r02_h19_una_instancia_viva_no_recupera(tmp_path):
    f5 = _con_tres(tmp_path)
    a = Almacen(tmp_path)
    lineas = f5.read_text(encoding="utf-8").splitlines()
    sellos = json.loads((tmp_path / "sellos_integridad.json").read_text())
    sellos["F5"] = [2, json.loads(lineas[1])["_hash"]]
    (tmp_path / "sellos_integridad.json").write_text(json.dumps(sellos))
    assert a.verificar_integridad("F5") == {"F5": False}
    with pytest.raises(ValueError):
        a.escribir("F5", "AG-01", {"id": "cuatro"})
    assert len(f5.read_text(encoding="utf-8").splitlines()) == 3


def test_r02_h20_no_se_reescribe_nada_si_otro_fichero_no_valida(tmp_path):
    f5 = _con_tres(tmp_path)
    a = Almacen(tmp_path)
    a.escribir("F6", "AG-20", {"tipo_entrada": "RES", "id": "RES-1"})
    lineas = f5.read_text(encoding="utf-8").splitlines()
    sellos = json.loads((tmp_path / "sellos_integridad.json").read_text())
    sellos["F5"] = [2, json.loads(lineas[1])["_hash"]]          # F5 recuperable…
    sellos["F6"] = [7, "0" * 64]                                 # …pero F6 no valida
    (tmp_path / "sellos_integridad.json").write_text(json.dumps(sellos))
    with pytest.raises(ValueError):
        Almacen(tmp_path)
    assert f5.read_text(encoding="utf-8").splitlines() == lineas
    assert not f5.with_name(f5.name + ".no_confirmado.jsonl").exists()


def test_r02_h21_ctrl_c_tras_guardar_el_sello_conserva_el_registro(tmp_path):
    from unittest.mock import patch
    a = Almacen(tmp_path)
    a.escribir("F5", "AG-01", {"id": "uno"})
    original = Almacen._guardar_json

    def guarda_y_corta(ruta, datos):
        original(ruta, datos)
        if ruta.name == "sellos_integridad.json":
            raise KeyboardInterrupt
    with patch.object(Almacen, "_guardar_json", staticmethod(guarda_y_corta)), pytest.raises(KeyboardInterrupt):
        a.escribir("F5", "AG-01", {"id": "dos"})
    assert list(Almacen(tmp_path).estado("F5")) == ["uno", "dos"]


@pytest.mark.parametrize("plazo,dentro,fuera", [
    ("2026-03-29", "2026-03-29T21:59Z", "2026-03-29T22:00Z"),    # cambio a verano en Madrid: el día termina a las 22:00 UTC
    ("2026-10-25", "2026-10-25T22:59Z", "2026-10-25T23:00Z"),    # cambio a invierno: termina a las 23:00 UTC
    ("20260608", "2026-06-08T21:59Z", "2026-06-08T22:00Z")])
def test_r02_h22_plazo_con_solo_fecha_y_cambios_de_hora(tmp_path, universo, plazo, dentro, fuera):
    b = nuevo_bloque(tmp_path, universo)
    c = b.consultas.enviar({"tipo": "OTRA", "modo": "BLOQUEANTE", "clases": ["RV"],
                            "preguntas": [{"texto": "¿RV?", "supuesto_declarado": "esperar"}],
                            "plazo_respuesta": plazo}, "2026-03-02")
    assert not b.consultas.vencer(dentro)
    assert b.consultas.vencer(fuera) == [c["cns_id"]]


@pytest.mark.parametrize("malo", [float("nan"), True, -0.1, 1.5, "0.5", None])
def test_r02_h23_umbral_favorable_invalido_falla_cerrado(tmp_path, universo, malo):
    b = nuevo_bloque(tmp_path, universo)
    b.cfg["senales"]["umbral_favorable"] = malo
    with pytest.raises((ValueError, KeyError)):
        b._observacion_ht01("X", {"senal_compuesta": 0.55})



# ---------------------------------------------------------------------------------------------- QA r03 de T-92
@pytest.mark.parametrize("delante", ["/", "-", ".", "key-", "\\n", "\\t", "\n", "_"])
def test_r03_h25_clave_detras_de_separadores_y_escapes(delante):
    import uuid
    for clave in (f"{SK}ant-api03-{'Ab9_' * 10}", f"{SK}proj-{uuid.uuid4().hex}{'Zz-' * 4}"):
        texto = '{"respuesta": "ver ' + delante + clave + '"}'
        assert contenido_sensible(texto), (delante, clave[:12])


def test_r03_h26_formatos_genericos():
    import secrets as sec
    import uuid
    from bloque_a.contratos import contiene_credenciales
    casos = [f"{SK}{uuid.uuid4()}", f"{SK}lf-{uuid.uuid4()}", f"{SK}{sec.token_hex(8)}-{sec.token_hex(8)}",
             f"{SK}{'abc_def_' * 3}{sec.token_hex(4)}", f"SK-{sec.token_urlsafe(24)}"]
    casos += [f"{SK}{sec.token_urlsafe(16)}" for _ in range(500)]
    fallan = [c for c in casos if not contenido_sensible(c)]
    assert not fallan, fallan[:3]
    assert contenido_sensible(casos[0].encode()) and contiene_credenciales({"b": casos[0].encode()})


@pytest.mark.parametrize("texto", ["ticker sk-innovation-2024Q4-results-presentation", "ver sk-biopharm_FY2023_annual_report_EN.pdf",
                                   "sk-hynix_3Q24_earnings_release_final", "SK-Hynix-Q3-results-beat-estimates"])
def test_r03_h28_nombres_de_informes_no_son_claves(texto):
    assert not contenido_sensible(texto)


def test_r03_h27_registros_sin_sello_en_varios_ficheros_fallan_cerrado(tmp_path):
    a = Almacen(tmp_path)
    for k in ("uno", "dos"):
        a.escribir("F5", "AG-01", {"id": k})
        a.escribir("F6", "AG-20", {"tipo_entrada": "RES", "id": k})
    viejo = json.loads((tmp_path / "sellos_integridad.json").read_text())
    for archivo in ("F5", "F6"):
        ruta = next(tmp_path.glob(archivo + "_*"))
        viejo[archivo] = [1, json.loads(ruta.read_text(encoding="utf-8").splitlines()[0])["_hash"]]
    (tmp_path / "sellos_integridad.json").write_text(json.dumps(viejo))
    antes = {p.name: p.read_bytes() for p in tmp_path.glob("F[56]_*")}
    with pytest.raises(ValueError, match="más de un fichero"):
        Almacen(tmp_path)
    assert {p.name: p.read_bytes() for p in tmp_path.glob("F[56]_*")} == antes


def test_r03_h29_ultima_linea_a_medio_escribir_se_aparta_al_abrir(tmp_path):
    f5 = _con_tres(tmp_path)
    with open(f5, "a", encoding="utf-8") as fh:
        fh.write('{"_seq": 4, "id": "cuat')                      # el proceso murió a mitad de la línea
    a = Almacen(tmp_path)
    assert list(a.estado("F5")) == ["uno", "dos", "tres"]
    assert "cuat" in f5.with_name(f5.name + ".no_confirmado.jsonl").read_text(encoding="utf-8")
    assert any("sin confirmar" in str(e.get("detalle")) for e in a.leer("HA"))
    a.escribir("F5", "AG-01", {"id": "cuatro"})
    assert list(Almacen(tmp_path).estado("F5")) == ["uno", "dos", "tres", "cuatro"]


@pytest.mark.parametrize("plazo", ["2026", "2026-06", "8 June 2026", "2026-6-8", "mañana"])
def test_r03_h30_plazo_que_no_es_iso_se_rechaza(tmp_path, universo, plazo):
    b = nuevo_bloque(tmp_path, universo)
    with pytest.raises(ValueError):
        b.consultas.enviar({"tipo": "OTRA", "modo": "BLOQUEANTE", "clases": ["RV"],
                            "preguntas": [{"texto": "¿RV?", "supuesto_declarado": "esperar"}],
                            "plazo_respuesta": plazo}, AS_OF)
