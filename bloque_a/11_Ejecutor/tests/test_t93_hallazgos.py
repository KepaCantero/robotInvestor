"""T-93: regresiones de los hallazgos H-32 a H-39 de la QA r04 de T-92 (`.docs/tickets/T-92/qa.md`, «Ronda r04»).

Sin red ni claves: datos y SDK simulados. Las claves de prueba se arman en tiempo de ejecución para que el escáner de secretos
del repositorio no las tome por reales.
"""
import datetime as dt
import json
import urllib.parse

import pytest
from bloque_a.almacen import Almacen
from bloque_a.contratos import contiene_credenciales
from bloque_a.llm import LLMClient, ReplayClient, RespuestaLLM, Uso, contenido_sensible
from conftest import config_pruebas, nuevo_bloque

SK = "s" + "k-"
CLAVE = f"{SK}ant-api03-{'msUpBNeqXSNZ0e2m' * 2}"
CONSULTA = {"tipo": "OTRA", "modo": "BLOQUEANTE", "clases": ["RV"], "preguntas": [{"texto": "¿RV?", "supuesto_declarado": "esperar"}]}


# ---------------------------------------------------------------------------------------------- H-32: escapes delante de la clave
@pytest.mark.parametrize("nombre,texto", [
    ("json_u00ab", json.dumps({"nota": "la clave «" + CLAVE + "»"})),
    ("json_u201c", json.dumps({"nota": "“" + CLAVE + "”"})),
    ("json_nbsp", json.dumps({"nota": "clave: " + CLAVE})),
    ("json_raya", json.dumps({"nota": "—" + CLAVE})),
    ("json_emoji", json.dumps({"nota": "🔑" + CLAVE})),
    ("json_b", json.dumps({"nota": "\b" + CLAVE})),
    ("json_f", json.dumps({"nota": "\f" + CLAVE})),
    ("url_key", "https://x.example/cb?next=" + urllib.parse.quote("https://api.example/v1?key=" + CLAVE, safe="")),
    ("url_espacio", "q=" + urllib.parse.quote("mi clave " + CLAVE)),
    ("repr_xa0", repr("clave: " + CLAVE)),
])
def test_h32_ningun_escape_delante_oculta_la_clave(nombre, texto):
    assert contenido_sensible(texto), nombre


def test_h32_la_grabadora_no_escribe_la_clave_en_la_cinta(tmp_path):
    texto = json.dumps({"nota": "la clave «" + CLAVE + "»"})

    class Base(LLMClient):
        nombre = "base"

        def generar(self, **kw):
            return RespuestaLLM(texto, Uso(), "m", "end_turn")
    cinta = tmp_path / "cinta.jsonl"
    r = ReplayClient(cinta, "grabar", Base()).generar(agente="AG-02", modelo="m", system=[],
                                                      mensajes=[{"role": "user", "content": "x"}], max_tokens=10)
    assert r.stop_reason == "contenido_sensible"
    assert not cinta.exists() or CLAVE not in cinta.read_text(encoding="utf-8")


def test_h32_contenido_sensible_recorre_los_conjuntos():
    assert contenido_sensible({"s": {" " + CLAVE}}) and contenido_sensible({" " + CLAVE}) and contenido_sensible(frozenset({CLAVE}))
    assert contiene_credenciales({"s": {" " + CLAVE}})


# ---------------------------------------------------------------------------------------------- H-33: prensa financiera
@pytest.mark.parametrize("texto", [
    "https://www.reuters.com/technology/sk-hynix-q2-profit-jumps-on-ai-chip-demand-2024-07-25/",
    "https://www.reuters.com/technology/sk-hynix-posts-record-q3-profit-2024-10-24/",
    "https://www.reuters.com/business/sk-telecom-5g-subscribers-rise-2024-01-10/",
    "https://www.example.com/news/sk-hynix-hbm3e-supply-deal-with-nvidia",
    "https://www.example.com/ir/sk-biopharm-fy2023-annual-report",
    "Descarga: sk-hynix_20240725_earnings_release.pdf",
    "https://www.marketscreener.com/quote/stock/SK-TELECOM-CO-LTD-6496057/news/",
    "https://www.marketscreener.com/quote/stock/SK-INNOVATION-CO-LTD-6494946/",
    "SK-HYNIX-QUARTERLY-RESULTS-2024",
    "https://www.example.com/sk-hynix-1q24-earnings-call-transcript",
    "https://www.example.com/sk-hynix-000660-stock-analysis",
    "sk-HynixEarnings-2024-summary",
])
def test_h33_urls_de_prensa_financiera_no_son_claves(texto):
    assert not contenido_sensible(texto)


def test_h33_una_fecha_de_8_cifras_que_no_existe_no_es_texto():
    assert contenido_sensible(f"ver {SK}hynix_20241345_earnings_release_final") and contenido_sensible(f"ver {SK}hynix_20240230_earnings_release_x")


def test_h33_el_recall_de_las_claves_reales_no_baja():
    import secrets as sec
    import uuid
    casos = [f"{SK}{uuid.uuid4()}", f"{SK}{str(uuid.uuid4()).upper()}", f"{SK}lf-{uuid.uuid4()}", f"{SK}proj-{sec.token_urlsafe(32)}",
             f"{SK}svcacct-{sec.token_urlsafe(32)}", f"{SK}admin-{sec.token_urlsafe(32)}", f"{SK}{sec.token_hex(24)}"]
    casos += [f"{SK}{sec.token_urlsafe(n)}" for n in (16, 24, 32) for _ in range(300)]
    casos += [f"{SK}{sec.token_hex(4)}-{sec.token_hex(4)}-{sec.token_hex(4)}-{sec.token_hex(6)}" for _ in range(300)]
    fallan = [c for c in casos if not contenido_sensible("clave: " + c)]
    assert not fallan, fallan[:3]


# ---------------------------------------------------------------------------------------------- H-34 y H-35: almacén
def _con_tres(tmp):
    a = Almacen(tmp)
    for k in ("uno", "dos", "tres"):
        a.escribir("F5", "AG-01", {"id": k, "nota": "año «ñ» — fin"})
    return next(tmp.glob("F5*"))


def test_h34_almacen_anterior_a_los_sellos_con_la_ultima_linea_cortada(tmp_path):
    f5 = _con_tres(tmp_path)
    (tmp_path / "sellos_integridad.json").unlink()
    (tmp_path / "formato_almacen.json").unlink()
    with open(f5, "a", encoding="utf-8") as fh:
        fh.write('{"_seq": 4, "id": "cuat')
    a = Almacen(tmp_path)
    assert list(a.estado("F5")) == ["uno", "dos", "tres"]
    assert "cuat" in f5.with_name(f5.name + ".no_confirmado.jsonl").read_text(encoding="utf-8")
    a.escribir("F5", "AG-01", {"id": "nuevo"})
    assert list(Almacen(tmp_path).estado("F5")) == ["uno", "dos", "tres", "nuevo"]


def test_h35_un_corte_a_mitad_de_un_caracter_utf8_se_aparta(tmp_path):
    f5 = _con_tres(tmp_path)
    linea = json.dumps({"_seq": 4, "id": "cuatro", "nota": "año «ñ» — fin"}, ensure_ascii=False).encode()
    i = linea.index("ñ".encode()) + 1   # el proceso murió justo entre los dos bytes de «ñ», antes del sello
    with open(f5, "ab") as fh:
        fh.write(linea[:i])
    a = Almacen(tmp_path)
    assert list(a.estado("F5")) == ["uno", "dos", "tres"]
    assert f5.with_name(f5.name + ".no_confirmado.jsonl").exists()
    a.escribir("F5", "AG-01", {"id": "cuatro bis"})
    assert list(Almacen(tmp_path).estado("F5")) == ["uno", "dos", "tres", "cuatro bis"]


# ---------------------------------------------------------------------------------------------- H-37 y H-38: plazos de CT-23
@pytest.mark.parametrize("plazo", [20260608, 2026.5, True, False])
def test_h37_un_plazo_numerico_o_booleano_se_rechaza(tmp_path, universo, plazo):
    b = nuevo_bloque(tmp_path, universo)
    with pytest.raises(ValueError):
        b.consultas.enviar({**CONSULTA, "plazo_respuesta": plazo}, "2026-06-05")


def test_h37_un_date_vence_al_terminar_el_dia_como_su_texto(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    c = b.consultas.enviar({**CONSULTA, "plazo_respuesta": dt.date(2026, 6, 8)}, "2026-06-05")
    assert c["plazo_respuesta"].startswith("2026-06-08T23:59:59.999999+02:00")
    assert not b.consultas.vencer("2026-06-08T21:00Z") and b.consultas.vencer("2026-06-08T22:00Z") == [c["cns_id"]]


@pytest.mark.parametrize("plazo", ["2026-6-8", "8/6/2026", "2026-06-08 09:00:00.000000+0200 CEST"])
def test_h38_un_plazo_antiguo_que_no_se_lee_vence_con_incidencia(tmp_path, universo, plazo):
    b = nuevo_bloque(tmp_path, universo)
    c = b.consultas.enviar(dict(CONSULTA), "2026-06-05")
    guardada = b.almacen.estado("F5", clave="cns_id")[c["cns_id"]]
    b.almacen.escribir("F5", "AG-01", {**{k: v for k, v in guardada.items() if not k.startswith("_")}, "plazo_respuesta": plazo})
    assert b.consultas.vencer("2026-06-06T09:00") == [c["cns_id"]]
    assert any(c["cns_id"] in str(e.get("detalle")) for e in b.almacen.leer("HA"))


# ---------------------------------------------------------------------------------------------- H-39 (c): medianoche inexistente
def test_h39_plazo_en_un_dia_sin_medianoche(tmp_path, universo):
    cfg = config_pruebas()
    cfg["zona_horaria"] = "America/Santiago"   # el 6-9-2026 las 00:00 pasan a la 01:00
    b = nuevo_bloque(tmp_path, universo, cfg=cfg)
    c = b.consultas.enviar({**CONSULTA, "plazo_respuesta": "2026-09-05"}, "2026-09-01")
    assert not b.consultas.vencer("2026-09-06T03:59:59.999Z")
    assert b.consultas.vencer("2026-09-06T04:00Z") == [c["cns_id"]]
