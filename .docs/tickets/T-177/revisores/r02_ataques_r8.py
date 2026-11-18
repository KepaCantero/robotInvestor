"""QA r02 de T-177 (revisor independiente, otro que el de la r01). Familias de ataque a R8 que no están en r01_ataques_r8.py.

Ejecutar desde bloque_a/11_Ejecutor:  python -m pytest -q -s -p no:cacheprovider ../../.docs/tickets/T-177/revisores/r02_ataques_r8.py
Los secretos son ficticios y van partidos en dos cadenas. Cada caso imprime dónde aparece el secreto (lista vacía = en ningún
archivo). Los casos «HALLAZGO_*» pasan mientras el fallo siga presente; al corregirlo se invierte la aserción (`== []`)."""
import base64
import importlib
import json
import sys
from dataclasses import replace
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "bloque_a" / "11_Ejecutor" / "tests"))
from conftest import AS_OF, config_pruebas, nuevo_bloque, universo  # noqa: E402,F401

from bloque_a.llm import MockClient, ReplayClient  # noqa: E402
from bloque_a.mantenimiento_c4 import mantenimiento_c4  # noqa: E402

mock_respuestas = importlib.import_module("bloque_a.mock_respuestas")
SECRETO = "QaR02Ficticio" + "88YyWw"      # 19 caracteres, letras y cifras: no es una credencial real
FICHA = {"servicio": "API de fondos cerrados", "uso_previsto": "Cribado de FON", "impacto_si_falta": "Datos públicos"}
BASE = {"servicio": FICHA["servicio"], "motivo": "m", "impacto_si_falta": "i"}


def _bloque(tmp, universo, cliente=None):
    return nuevo_bloque(tmp, universo, cliente=cliente,
                        cfg=config_pruebas(credenciales={"servicios_bfa": [FICHA]}))


def _aparece(tmp, valor):
    return sorted(str(p.relative_to(tmp)) for p in Path(tmp).rglob("*")
                  if p.is_file() and p.name != "secretos.json" and valor in p.read_text(encoding="utf-8", errors="ignore"))


def _ret(sol, top=None):
    r = {"referencias": [], "sintesis": "s", "lagunas": [], "solicitudes_credenciales": sol}
    r.update(top or {})
    return r


class TextoBFA(MockClient):
    """Cliente simulado cuyo AG-16 devuelve un texto crudo dado (para escapes JSON y respuestas que no son un dict)."""
    def __init__(self, texto):
        super().__init__()
        self.texto = texto

    def generar(self, **kw):
        r = super().generar(**kw)
        return replace(r, texto=self.texto) if kw.get("agente") == "AG-16" else r


def _c4(tmp, universo, monkeypatch, retorno=None, texto=None, grabar=True):
    """Una C4 con el retorno (dict) o el texto crudo dado, grabando la cinta (modo sombra) y con la caché activa."""
    if retorno is not None:
        monkeypatch.setattr(mock_respuestas, "_mantenimiento_c4", lambda msg: retorno)
    base = TextoBFA(texto) if texto is not None else MockClient()
    cliente = ReplayClient(Path(tmp) / "cinta.jsonl", "grabar", base) if grabar else base
    b = _bloque(tmp, universo, cliente=cliente)
    return b, mantenimiento_c4(b, AS_OF)


# ---- 1. Claves de valor en otros idiomas o con caracteres raros (fuera de CAMPOS_VALOR_CREDENCIAL) ----------------------
CLAVES_OTRAS = ["value", "wert", "senha", "chiave", "mot_de_passe", "key", "secret_value", "valor_api", "パスワード", "clé",
                "v\uff41lor"]   # la última, con una «a» de ancho completo
CLAVES_NORMALIZADAS = ["Valor\u200b", "VALOR", "Api-Key", "access.token", "Contraseña"]   # la normalización las reconoce


@pytest.mark.parametrize("clave", CLAVES_NORMALIZADAS)
def test_r02_claves_raras_que_si_se_bloquean(tmp_path, universo, monkeypatch, clave):
    b, r = _c4(tmp_path, universo, monkeypatch, retorno=_ret([{**BASE, clave: SECRETO}]))
    assert r["estado_retorno"] == "SIN_RESULTADO" and _aparece(tmp_path, SECRETO) == []


@pytest.mark.parametrize("clave", CLAVES_OTRAS)
def test_r02_HALLAZGO_H08_clave_de_valor_fuera_de_la_lista(tmp_path, universo, monkeypatch, clave):
    b, r = _c4(tmp_path, universo, monkeypatch, retorno=_ret([{**BASE, clave: SECRETO}]))
    donde = _aparece(tmp_path, SECRETO)
    print(repr(clave), r["estado_retorno"], r["rechazo"], [s["resultado"] for s in r["solicitudes"]], donde)
    assert donde == []        # r03 (invertida): H-08 corregido


# ---- 2. La clave `solicitudes_credenciales` escrita con escapes \\uXXXX (JSON válido): la primera barrera no la ve --------
def test_r02_HALLAZGO_H09_clave_con_escape_unicode_llega_a_la_cinta(tmp_path, universo, monkeypatch):
    texto = ('{"referencias": [], "sintesis": "s", "lagunas": [], "solicitudes\\u005fcredenciales": [{"servicio": "'
             + FICHA["servicio"] + '", "motivo": "m", "impacto_si_falta": "i", "valor": "' + SECRETO + '"}]}')
    assert json.loads(texto)["solicitudes_credenciales"][0]["valor"] == SECRETO
    b, r = _c4(tmp_path, universo, monkeypatch, texto=texto)
    donde = _aparece(tmp_path, SECRETO)
    print("escape \\u005f:", r["estado_retorno"], r["rechazo"], donde)
    assert r["estado_retorno"] == "SIN_RESULTADO"
    assert donde == []                                   # r03 (invertida): H-09 corregido, la cinta no guarda el valor


# ---- 3. JSON dentro de un string ----------------------------------------------------------------------------------------
EN_STRING = {
    "lista_como_texto": _ret(json.dumps([{**BASE, "valor": SECRETO}])),
    "sintesis_con_json": _ret([BASE], top={"sintesis": json.dumps({"valor": SECRETO})}),
}


@pytest.mark.parametrize("nombre", sorted(EN_STRING))
def test_r02_HALLAZGO_H08_json_dentro_de_un_texto(tmp_path, universo, monkeypatch, nombre):
    b, r = _c4(tmp_path, universo, monkeypatch, retorno=EN_STRING[nombre])
    donde = _aparece(tmp_path, SECRETO)
    print(nombre, r["estado_retorno"], r["rechazo"], donde)
    assert donde == []        # r03 (invertida): H-08


# ---- 4. El secreto en un sitio de la solicitud que el Coordinador no copia (y el ficha-opaca no mira) --------------------
FUERA_DE_FORMA = {
    "motivo_como_dict": [{**BASE, "motivo": {"texto": "usar " + SECRETO}}],
    "en_urgencia": [{**BASE, "urgencia": SECRETO}],
    "en_lagunas": None,
}


@pytest.mark.parametrize("nombre", sorted(FUERA_DE_FORMA))
def test_r02_HALLAZGO_H08_fuera_de_los_campos_libres(tmp_path, universo, monkeypatch, nombre):
    ret = _ret(FUERA_DE_FORMA[nombre]) if FUERA_DE_FORMA[nombre] else _ret([BASE], top={"lagunas": ["usar " + SECRETO]})
    b, r = _c4(tmp_path, universo, monkeypatch, retorno=ret)
    donde = _aparece(tmp_path, SECRETO)
    print(nombre, r["estado_retorno"], r["rechazo"], donde)
    assert donde == []        # r03 (invertida): H-08


# ---- 5. Codificados y partidos -----------------------------------------------------------------------------------------
B64_BARRAS = "QaR0/2Fict+icio8" + "/8YyWw+Zz9k/Lm3n"   # base64 con «/» y «+» cada pocos caracteres: tramos < 16
HEX = (SECRETO.encode().hex())


def test_r02_codificados_en_el_motivo(tmp_path, universo, monkeypatch):
    """base64 «limpio» y hex: RE_FICHA_OPACA los rechaza. base64 con «/» y «+» en tramos cortos: límite del detector."""
    res = {}
    for nombre, cod in (("b64", base64.b64encode(SECRETO.encode()).decode().rstrip("=")), ("hex", HEX),
                        ("b64_barras", B64_BARRAS)):
        d = tmp_path / nombre
        b, r = _c4(d, universo, monkeypatch, retorno=_ret([{**BASE, "motivo": "usar " + cod}]))
        res[nombre] = (r["rechazo"], r["estado_retorno"], _aparece(d, cod))
    print(res)
    assert res["b64"][2] == [] and res["hex"][2] == []
    assert res["b64_barras"][2] == []                    # r03 (invertida): H-10 corregido


def test_r02_partido_en_dos_campos(tmp_path, universo, monkeypatch):
    """Un secreto partido en dos campos de < 16: ningún detector puede verlo (límite inherente, no hallazgo)."""
    a, z = SECRETO[:9], SECRETO[9:]
    b, r = _c4(tmp_path, universo, monkeypatch, retorno=_ret([{**BASE, "motivo": "usar " + a, "impacto_si_falta": z}]))
    print("partido:", r["rechazo"], [s["resultado"] for s in r["solicitudes"]], _aparece(tmp_path, a), _aparece(tmp_path, z))


# ---- 6. Listas de dicts y respuestas que no son dict -----------------------------------------------------------------
NO_DICT = {
    "lista_de_retornos": json.dumps([_ret([{**BASE, "valor": SECRETO}])]),
    "lista_anidada": json.dumps(_ret([[{**BASE, "valor": SECRETO}]])),
    "texto_sin_llaves": "solicitudes_credenciales: servicio API, valor " + SECRETO,
    "prosa_y_json": "Aquí va {nota} y luego " + json.dumps(_ret([{**BASE, "valor": SECRETO}])),
    "fence": "```json\n" + json.dumps(_ret([{**BASE, "Valor": SECRETO}])) + "\n```",
}


@pytest.mark.parametrize("nombre", sorted(NO_DICT))
def test_r02_no_dict_y_listas_bloqueados(tmp_path, universo, monkeypatch, nombre):
    b, r = _c4(tmp_path, universo, monkeypatch, texto=NO_DICT[nombre])
    donde = _aparece(tmp_path, SECRETO)
    print(nombre, r["estado_retorno"], donde)
    assert r["solicitudes"] == [] and donde == []


# ---- 7. Desviación: `valor` numérico ----------------------------------------------------------------------------------
def test_r02_HALLAZGO_H11_valor_numerico_incoherente(tmp_path, universo, monkeypatch):
    """La primera y la segunda barrera dejan pasar un `valor` numérico (desviación declarada), pero el Coordinador lo trata
    como valor de credencial (SEGURIDAD, rechazo íntegro): el número que el Coordinador considera un valor queda en la caché."""
    num = int("40417" + "73129")
    b, r = _c4(tmp_path, universo, monkeypatch, retorno=_ret([{**BASE, "valor": num}]))
    donde = _aparece(tmp_path, str(num))
    print("numérico:", r["estado_retorno"], r["rechazo"], donde)
    assert r["estado_retorno"] == "SIN_RESULTADO" and donde == []   # r03 (invertida): H-11, no llega a la caché


# ---- 8. Escape \\u en la clave de valor (con la clave de solicitudes normal): la primera barrera lee el JSON y lo para --
def test_r02_escape_en_la_clave_de_valor(tmp_path, universo, monkeypatch):
    texto = ('{"referencias": [], "sintesis": "s", "lagunas": [], "solicitudes_credenciales": [{"servicio": "'
             + FICHA["servicio"] + '", "motivo": "m", "impacto_si_falta": "i", "v\\u0061lor": "' + SECRETO + '"}]}')
    b, r = _c4(tmp_path, universo, monkeypatch, texto=texto)
    assert _aparece(tmp_path, SECRETO) == [] and r["estado_retorno"] == "SIN_RESULTADO"


# ---- 9. Falso positivo: el formato canónico de retorno de los Analistas (Marco común V5.0, l. 33 y 44) -----------------
def test_r02_HALLAZGO_H12_informe_de_analista_canonico_descartado():
    """Todo informe de Analista lleva `solicitudes_credenciales: []` y `regimen_clase.indicadores[].valor` de texto («…»): la
    primera barrera lo trata como sensible y el informe entero se pierde. Con `valor` numérico pasa."""
    from bloque_a.llm import RespuestaLLM, Uso, respuesta_segura
    inf = {"clase": "RF", "estado": "COMPLETO", "regimen_clase": {"diagnostico": "Curva positiva", "indicadores": [
        {"nombre": "Tipo a 10 años", "valor": "4,25 %", "fecha": "2024-03-01", "fuente": "HT-01"}]},
        "finalistas": [], "consultas_broker": [], "solicitudes_credenciales": [], "lagunas": [], "autoevaluacion": "ok"}
    texto = respuesta_segura(RespuestaLLM(json.dumps(inf, ensure_ascii=False), Uso(), "m"))
    inf["regimen_clase"]["indicadores"][0]["valor"] = 4.25
    numero = respuesta_segura(RespuestaLLM(json.dumps(inf, ensure_ascii=False), Uso(), "m"))
    print("valor de texto:", texto.stop_reason, "· numérico:", numero.stop_reason)
    assert texto.stop_reason is None and numero.stop_reason is None   # r03 (invertida): H-12 corregido


def test_r02_HALLAZGO_H13_ficha_opaca_con_guiones():
    """RE_FICHA_OPACA toma «-» como parte de la ficha: un símbolo del universo de ejemplo o el nombre de una serie en el
    motivo de una solicitud descarta la respuesta entera."""
    from bloque_a.llm import solicitud_con_valor
    for motivo in ("Serie CURVA-USD-2S10S-TR del universo", "Índice ICE-BofA-US-HY-2024"):
        assert not solicitud_con_valor(json.dumps(_ret([{**BASE, "motivo": motivo}])))   # r03 (invertida): H-13
