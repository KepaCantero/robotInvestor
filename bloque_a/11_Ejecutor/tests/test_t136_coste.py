"""T-136 · Hallazgos de la QA r01 de T-129: la cota superior del coste (H-01), el suelo (H-02) y dos mutantes vivos del
cliente real (H-03: `output_config` con otra cosa que el formato y una versión vieja de la búsqueda web)."""
import importlib.util
from pathlib import Path

import pytest
import yaml
from bloque_a.configuracion import cargar_config
from bloque_a.llm import AnthropicClient
from conftest import config_pruebas, nuevo_bloque
from test_t129_modo_sombra import PRECIOS, SDKQueAnota

RAIZ = Path(__file__).resolve().parents[1]
BUSQUEDA_WEB_MAS_RECIENTE = "web_search_20260318"   # documentación de Anthropic, 15-11-2026


def _estimador():
    ruta = RAIZ.parents[1] / ".docs" / "scripts" / "estimar_coste_ciclo_a.py"
    spec = importlib.util.spec_from_file_location("estimar_coste_ciclo_a", ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.parametrize("estructurada", [False, True])
def test_h03_output_config_solo_lleva_el_formato(tmp_path, universo, estructurada):
    sdk = SDKQueAnota()
    cfg = config_pruebas(modo="vivo")
    b = nuevo_bloque(tmp_path, universo, cliente=AnthropicClient(sdk=sdk, salida_estructurada=estructurada), cfg=cfg)
    b.ciclo("2026-06-05", alcance={"clases": ["RV"]}, nivel_forzado="N2")
    con = [k for k in sdk.peticiones if "output_config" in k]
    if estructurada:
        assert con and all(set(k["output_config"]) == {"format"} and k["output_config"]["format"]["type"] == "json_schema"
                           for k in con)
    else:
        assert con == []


def test_h03_la_busqueda_web_es_la_version_de_la_configuracion_y_la_mas_reciente(tmp_path, universo):
    assert cargar_config()["busqueda_web"]["tipo_herramienta"] == BUSQUEDA_WEB_MAS_RECIENTE
    sdk = SDKQueAnota()
    b = nuevo_bloque(tmp_path, universo, cliente=AnthropicClient(sdk=sdk), cfg=config_pruebas(modo="vivo"))
    b.ciclo("2026-06-05", alcance={"clases": ["RV"]}, nivel_forzado="N2")
    tipos = {h["type"] for k in sdk.peticiones for h in k.get("tools") or []}
    assert tipos == {BUSQUEDA_WEB_MAS_RECIENTE}


def test_h01_la_cota_cubre_sin_cache_margen_de_tokens_y_continuaciones():
    est = _estimador()
    precios = {"m": {"entrada": 2.0, "salida": 10.0, "escritura_cache": 4.0, "lectura_cache": 0.1}}
    llamada = {"agente": "AG-16", "modelo": "m", "sys_tok": 800_000, "user_tok": 200_000, "out_tok": 0, "max_tokens": 100_000,
               "cache_escr": 0, "cache_lect": 800_000}
    r = est.estimar([llamada], precios, 10.0, {"AG-16"}, 5, factor_tokens=1.35, continuaciones=3)
    # suelo: 0,2 M sin caché (0,4) + 0,8 M de lectura (0,08)
    assert r["estimacion"] == pytest.approx(0.48)
    # cota: 4 vueltas × 1,35 M como escritura (4 × 5,4) + 0,1 M de salida (1) + 20 búsquedas (0,2)
    # T-137 (QA r01 de T-136, H-01): cada continuación es una petición que reenvía lo ya generado y paga su max_tokens:
    # Σ_v (1,35 M + v · 0,1 M) × 4 + 4 × 0,1 M × 10 + 20 búsquedas
    assert r["cota_superior"] == pytest.approx(sum((1.35 + 0.1 * v) * 4.0 for v in range(4)) + 4 * 1.0 + 0.2)
    assert r["busquedas_cota"] == 20
    sin = est.estimar([llamada], precios, 10.0, set(), 5, factor_tokens=1.35, continuaciones=3)
    assert sin["cota_superior"] == pytest.approx(1.35 * 4.0 + 1.0) and sin["busquedas_cota"] == 0


def test_h01_la_tarifa_trae_el_margen_de_tokens():
    assert yaml.safe_load(PRECIOS.read_text(encoding="utf-8"))["factor_tokens_cota"] == 1.35
