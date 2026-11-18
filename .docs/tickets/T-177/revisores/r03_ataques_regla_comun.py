"""QA r03 de T-177 · ataques a la regla común `contratos.retorno_con_credencial`, falsos positivos con contenido realista y la
reserva EN_CURSO de la bolsa semanal tras la muerte del proceso.

Ejecutar desde bloque_a/11_Ejecutor:
  python -m pytest -q -s -p no:cacheprovider ../../.docs/tickets/T-177/revisores/r03_ataques_regla_comun.py
Secretos ficticios partidos en dos cadenas. Cada caso imprime lo que pasa; las aserciones fijan lo observado."""
import hashlib
import importlib
import json
import signal
import subprocess
import sys
import time
from dataclasses import replace
from pathlib import Path

import pandas as pd
import pytest

EJ = Path(__file__).resolve().parents[4] / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJ / "tests"))
from conftest import AS_OF, config_pruebas, nuevo_bloque, universo  # noqa: E402,F401

from bloque_a.contratos import retorno_con_credencial  # noqa: E402
from bloque_a.llm import MockClient, ReplayClient, RespuestaLLM, Uso, respuesta_segura, solicitud_con_valor  # noqa: E402

mc4 = importlib.import_module("bloque_a.mantenimiento_c4")
mock_respuestas = importlib.import_module("bloque_a.mock_respuestas")
SECRETO = "QaR03Ficticio" + "55TtUu"
FICHA = {"servicio": "API de fondos cerrados", "uso_previsto": "Cribado de FON", "impacto_si_falta": "Datos públicos"}
SOL = {"servicio": FICHA["servicio"], "motivo": "Cribado semanal", "impacto_si_falta": "Datos públicos"}


def _aparece(tmp, valor):
    return sorted(str(p.relative_to(tmp)) for p in Path(tmp).rglob("*")
                  if p.is_file() and p.name != "secretos.json" and valor in p.read_text(encoding="utf-8", errors="ignore"))


def _ret(sol, **top):
    return {"referencias": [], "sintesis": "s", "lagunas": [], "solicitudes_credenciales": sol, **top}


class TextoBFA(MockClient):
    def __init__(self, texto):
        super().__init__()
        self.texto = texto

    def generar(self, **kw):
        r = super().generar(**kw)
        return replace(r, texto=self.texto) if kw.get("agente") == "AG-16" else r


def _c4(tmp, universo, monkeypatch, retorno=None, texto=None):
    if retorno is not None:
        monkeypatch.setattr(mock_respuestas, "_mantenimiento_c4", lambda msg: retorno)
    base = TextoBFA(texto) if texto is not None else MockClient()
    b = nuevo_bloque(tmp, universo, cliente=ReplayClient(Path(tmp) / "cinta.jsonl", "grabar", base),
                     cfg=config_pruebas(credenciales={"servicios_bfa": [FICHA]}))
    return b, mc4.mantenimiento_c4(b, AS_OF)


# ---- 1. R8: lo que la regla común deja pasar dentro de una solicitud no vacía --------------------------------------------
SOLO_LETRAS = "QaFicticioSoloLetras" + "XyzWvuTsr"
SOLO_CIFRAS = "40417731" + "29554812"
CORTO = "Hunt" + "er2x!"
CON_GUIONES = "QaFic-ticio88" + "-YyWwZz-Kk77"
FUGAS = {
    "value_solo_letras": [{**SOL, "value": SOLO_LETRAS}],
    "value_solo_cifras_texto": [{**SOL, "value": SOLO_CIFRAS}],
    "value_corto": [{**SOL, "value": CORTO}],
    "value_con_guiones": [{**SOL, "value": CON_GUIONES}],
    "pin_numerico": [{**SOL, "pin": int(SOLO_CIFRAS)}],
}


@pytest.mark.parametrize("nombre", sorted(FUGAS))
def test_r03_HALLAZGO_H17_sin_etiqueta_bajo_clave_no_listada(tmp_path, universo, monkeypatch, nombre):
    b, r = _c4(tmp_path, universo, monkeypatch, retorno=_ret(FUGAS[nombre]))
    marca = {"value_solo_letras": SOLO_LETRAS, "value_solo_cifras_texto": SOLO_CIFRAS, "value_corto": CORTO,
             "value_con_guiones": CON_GUIONES, "pin_numerico": SOLO_CIFRAS}[nombre]
    donde = _aparece(tmp_path, marca)
    print(nombre, r["estado_retorno"], [s["resultado"] for s in r["solicitudes"]], donde)
    # HALLAZGO H-17: pasa a la caché y a la cinta (no a F5 ni al CT-25). Al corregir: SIN_RESULTADO y donde == []
    assert r["estado_retorno"] == "SIN_RESULTADO" and donde == []   # cierre (invertida): H-17


# Con la etiqueta (clave de CAMPOS_VALOR_CREDENCIAL) los mismos valores se paran
@pytest.mark.parametrize("valor", [SOLO_LETRAS, SOLO_CIFRAS, CORTO, CON_GUIONES])
def test_r03_mismos_valores_con_etiqueta_bloqueados(tmp_path, universo, monkeypatch, valor):
    b, r = _c4(tmp_path, universo, monkeypatch, retorno=_ret([{**SOL, "secreto": valor}]))
    assert r["estado_retorno"] == "SIN_RESULTADO" and _aparece(tmp_path, valor) == []


# Variantes estructurales contra la regla común: todas deben pararse
ESTRUCTURALES = {
    "secreto_como_clave": _ret([{**SOL, SECRETO: "x"}]),
    "dos_claves_una_vacia": {"solicitudes_credenciales": [], "Solicitudes-Credenciales": [{**SOL, "nota": SECRETO}]},
    "solicitudes_anidadas_en_texto": _ret([SOL], sintesis=json.dumps({"x": {"solicitudes_credenciales": [{"valor": "abc"}]}})),
    "texto_json_doble": _ret(json.dumps(json.dumps([{**SOL, "value": SECRETO}]))),
    "base64_de_la_solicitud": _ret([{**SOL, "anexo": __import__("base64").b64encode(
        json.dumps({"valor": SECRETO}).encode()).decode()}]),
    "valor_en_raiz_ambigua_opaca": _ret([], valor="usar " + SECRETO),
    "lista_de_un_texto_con_espacios": _ret("   "),
}


@pytest.mark.parametrize("nombre", sorted(ESTRUCTURALES))
def test_r03_estructurales_bloqueadas(tmp_path, universo, monkeypatch, nombre):
    b, r = _c4(tmp_path, universo, monkeypatch, retorno=ESTRUCTURALES[nombre])
    donde = _aparece(tmp_path, SECRETO)
    print(nombre, r["estado_retorno"], donde)
    if nombre == "lista_de_un_texto_con_espacios":
        assert r["solicitudes"] == []
    else:
        assert r["estado_retorno"] == "SIN_RESULTADO" and donde == []


def test_r03_HALLAZGO_H14_texto_ilegible_con_clave_escapada():
    """No se puede leer como JSON y la clave va con \\u005f: el prefiltro textual mira el texto crudo."""
    texto = '{"solicitudes\\u005fcredenciales": [{"servicio": "x", "value": "' + SECRETO + '"}] ,,, }'
    print("ilegible + escape:", solicitud_con_valor(texto))
    assert solicitud_con_valor(texto) is True           # cierre (invertida): H-14


def test_r03_anidamiento_profundo_falla_cerrado():
    hondo = "[" * 5000 + "]" * 5000
    assert solicitud_con_valor('{"solicitudes_credenciales": [' + hondo + ']}')
    s = json.dumps({"solicitudes_credenciales": [SOL], "sintesis": hondo})
    assert solicitud_con_valor(s)


# ---- 2. Falsos positivos con contenido realista -------------------------------------------------------------------------
SHA = hashlib.sha256(b"informe anual").hexdigest()
DIR_0X = "0x" + hashlib.sha1(b"contrato ficticio").hexdigest()
LEI = "5493001KJTIIGC8Y1R12"
FALSOS = {
    # informes con la lista vacía (todos los de Analista): no deben bloquearse
    # HALLAZGO H-15 (pasan a False al corregir): una dirección 0x (pública, T-147) o un LEI válido bajo una clave ambigua
    "cri_token_direccion_0x": ({"activos": [{"token": DIR_0X, "nombre": "USDC"}], "solicitudes_credenciales": []}, False),
    "clave_con_lei": ({"emisores": [{"clave": LEI}], "solicitudes_credenciales": []}, False),   # cierre (invertidas): H-15
    "valor_texto_largo": ({"indicadores": [{"valor": "4,25 % (serie BAMLH0A0HYM2, 2024-03-01)"}],
                           "solicitudes_credenciales": []}, False),
    "sha_en_referencias_lista_vacia": ({"referencias": [{"huella": SHA}], "solicitudes_credenciales": []}, False),
    # informes que piden una credencial: coste declarado de la extensión
    "sha_en_referencias_con_solicitud": ({"referencias": [{"huella": SHA}], "solicitudes_credenciales": [SOL]}, True),
    "lei_en_finalista_con_solicitud": ({"finalistas": [{"lei": LEI}], "solicitudes_credenciales": [SOL]}, True),
    "url_con_id_largo_con_solicitud": ({"fuentes": ["https://docs.ejemplo.org/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2/x"],
                                        "solicitudes_credenciales": [SOL]}, True),
    "opp_y_calc_con_solicitud": ({"finalistas": [{"opp_id": "OPP-2024-03-01-RV-001", "calc": "CALC-2024-0001"}],
                                  "solicitudes_credenciales": [SOL]}, False),
}


@pytest.mark.parametrize("nombre", sorted(FALSOS))
def test_r03_falsos_positivos(nombre):
    d, esperado = FALSOS[nombre]
    r = respuesta_segura(RespuestaLLM(json.dumps(d, ensure_ascii=False), Uso(), "m"))
    bloqueado = r.stop_reason == "contenido_sensible"
    print(nombre, "bloqueado" if bloqueado else "pasa")
    assert bloqueado is esperado


# ---- 3. Reserva EN_CURSO tras la muerte del proceso ---------------------------------------------------------------------
def test_r03_HALLAZGO_H16_proceso_muerto_reserva_huerfana(tmp_path):
    """Un `credencial c4` matado (SIGKILL) durante la llamada al BFA deja la C4- EN_CURSO con toda la bolsa reservada."""
    lento = tmp_path / "lento.py"
    lento.write_text(
        "import sys, time\nsys.path.insert(0, %r)\nfrom bloque_a import cli, mock_respuestas\n"
        "o = mock_respuestas._mantenimiento_c4\n"
        "def f(msg):\n    time.sleep(60)\n    return o(msg)\n"
        "mock_respuestas._mantenimiento_c4 = f\nsys.exit(cli.main(sys.argv[1:]))\n" % str(EJ), encoding="utf-8")
    cfg = tmp_path / "c4.yaml"
    cfg.write_text(json.dumps({"credenciales": {"servicios_bfa": [FICHA]}}), encoding="utf-8")
    comun = ["--cliente", "mock", "--config", str(cfg), "--datos", "ejemplos/datos_sinteticos", "--estado",
             str(tmp_path / "estado"), "--salida", str(tmp_path / "salida")]
    p = subprocess.Popen([sys.executable, str(lento), *comun, "--as-of", "2024-03-01", "credencial", "c4"], cwd=EJ)
    f5 = tmp_path / "estado" / "F5_historial_analisis.jsonl"
    for _ in range(120):
        if f5.exists() and "EN_CURSO" in f5.read_text():
            break
        time.sleep(0.5)
    p.send_signal(signal.SIGKILL)
    p.wait()

    def c4(fecha):
        out = subprocess.run([sys.executable, "-m", "bloque_a.cli", *comun, "--as-of", fecha, "credencial", "c4"],
                             cwd=EJ, capture_output=True, text=True, check=True).stdout
        return json.loads(out[out.find("{"):])
    filas = [json.loads(x) for x in f5.read_text().splitlines() if x]
    huerfana = [x for x in filas if x.get("estado_retorno") == "EN_CURSO"]
    r1 = c4("2024-03-01")
    r6 = c4(str((pd.Timestamp("2024-03-01") + pd.Timedelta(days=6)).date()))
    r7 = c4(str((pd.Timestamp("2024-03-01") + pd.Timedelta(days=7)).date()))
    print("huérfana:", [(x["id"], x["uc"], sorted(x)) for x in huerfana])
    print("mismo día:", r1["estado_retorno"], sorted(r1), "· +6:", r6["estado_retorno"], "· +7:", r7["estado_retorno"])
    ha = (tmp_path / "estado" / "HA_historial_auditorias.jsonl")
    avisos = [x for x in (ha.read_text().splitlines() if ha.exists() else []) if "C4-" in x or "EN_CURSO" in x]
    avisos = [x for x in avisos if "EN_CURSO" in x or "huérfana" in x]
    print("avisos en HA sobre la reserva:", len(avisos))   # HALLAZGO H-16: ninguno (al corregir: >= 1)
    assert len(avisos) == 1                              # cierre (invertida): H-16, un solo aviso aunque haya dos C4
    assert r1["reservas_en_curso"] == [huerfana[0]["id"]] and "pid" in huerfana[0]
    assert len(huerfana) == 1 and r1["estado_retorno"] == "SIN_PRESUPUESTO" and r6["estado_retorno"] == "SIN_PRESUPUESTO"
    assert r7["estado_retorno"] == "COMPLETO"
