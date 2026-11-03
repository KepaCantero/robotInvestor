"""Catálogo de los 24 agentes, búsqueda robusta de prompts por nombre y modos degradados (sin depender del contenido)."""
import unicodedata

import pytest

from bloque_b.configuracion import DIR_EJECUTOR, buscar_versionado, cargar_config, raiz_paquete, ruta
from bloque_b.prompts import AGENTES, BLOQUE_EJECUTOR, ESPECIALISTAS, NOMBRES, CatalogoPrompts


def _cfg(carpeta, **prompts):
    return cargar_config(extra={"rutas": {"prompts": str(carpeta)}, "prompts": prompts})


def test_hay_24_agentes_con_ids_correlativos():
    assert list(AGENTES) == [f"AG-B{i:02d}" for i in range(1, 25)]
    assert len(set(NOMBRES.values())) == 24
    assert ESPECIALISTAS == tuple(f"AG-B{i:02d}" for i in range(3, 12)) + ("AG-B24",)


def test_busqueda_por_nombre_version_mas_alta_nfd_y_mayusculas(tmp_path):
    n = NOMBRES["AG-B02"]
    (tmp_path / f"System prompt - {n} - Bloque B - Versión óptima V1.3.md").write_text("antigua", encoding="utf-8")
    nfd = unicodedata.normalize("NFD", f"system PROMPT - {n} - Bloque B - Versión óptima V2.0.md")
    (tmp_path / nfd).write_text("vigente", encoding="utf-8")
    (tmp_path / f"System prompt - {n} - notas.txt").write_text("no es md", encoding="utf-8")
    cat = CatalogoPrompts(_cfg(tmp_path))
    assert cat.texto("AG-B02") == "vigente"
    assert cat.estado()["AG-B02"]["estado"] == "CARGADO"


def test_no_confunde_prefijos(tmp_path):
    # «Documentador para el Motor» no debe casar con un archivo de «Documentador para el Director»
    (tmp_path / "System prompt - Documentador para el Director - Bloque B - Versión óptima V2.0.md").write_text("dir", encoding="utf-8")
    assert buscar_versionado(tmp_path, "System prompt - Documentador para el Motor") is None
    assert buscar_versionado(tmp_path, "System prompt - Documentador para el Director").name.startswith("System prompt - Documentador para el Director")


def test_alias_ag_b18(tmp_path):
    (tmp_path / "System prompt - Documentador para el Analizador de Mercados - Bloque B - Versión óptima V2.0.md").write_text("alias", encoding="utf-8")
    assert CatalogoPrompts(_cfg(tmp_path)).texto("AG-B18") == "alias"


def test_marco_comun_para_especialistas(tmp_path):
    (tmp_path / "Marco común de los Analistas de dimensión (plantilla) - Bloque B - Versión óptima V2.0.md").write_text("MARCO", encoding="utf-8")
    cat = CatalogoPrompts(_cfg(tmp_path), cliente="anthropic")
    assert "MARCO" in cat.texto("AG-B05") and "modo degradado" in cat.texto("AG-B05")
    assert cat.estado()["AG-B05"]["estado"] == "DEGRADADO"
    with pytest.raises(FileNotFoundError):     # no especialista y cliente real: error explícito
        cat.texto("AG-B22")


def test_marcador_con_cliente_simulado(tmp_path):
    cat = CatalogoPrompts(_cfg(tmp_path), cliente="mock")
    assert "Marcador" in cat.texto("AG-B22")
    assert "AG-B22" in cat.sustituidos
    with pytest.raises(FileNotFoundError):
        CatalogoPrompts(_cfg(tmp_path, marcador_si_falta_con_mock=False), cliente="mock").texto("AG-B22")
    with pytest.raises(KeyError):
        cat.texto("AG-B99")


def test_system_lleva_prompt_integro_e_interfaz_con_cache(tmp_path):
    texto = "PROMPT ÍNTEGRO\n" * 3
    (tmp_path / f"System prompt - {NOMBRES['AG-B12']} - Bloque B - Versión óptima V2.0.md").write_text(texto, encoding="utf-8")
    bloques = CatalogoPrompts(_cfg(tmp_path)).system("AG-B12", "1h")
    assert bloques[0]["text"] == texto
    assert bloques[1]["text"] == BLOQUE_EJECUTOR
    assert bloques[1]["cache_control"] == {"type": "ephemeral", "ttl": "1h"}


def test_rutas_del_paquete():
    cfg = cargar_config()
    assert raiz_paquete(cfg) == DIR_EJECUTOR.parent
    assert ruta(cfg, "universos") == DIR_EJECUTOR / "config" / "universos"


def test_prompts_reales_si_existen_casan_con_su_agente():
    """Solo comprueba nombres de archivo (no contenido). Se omite si la carpeta aún no tiene prompts."""
    cfg = cargar_config()
    cat = CatalogoPrompts(cfg)
    est = cat.estado()
    encontrados = {a: e for a, e in est.items() if e["archivo"]}
    if not encontrados:
        pytest.skip("02_System_prompts sin prompts todavía")
    for a, e in encontrados.items():
        assert any(unicodedata.normalize("NFC", e["archivo"]).casefold().startswith(f"system prompt - {n}".casefold())
                   for n in AGENTES[a]), (a, e["archivo"])


def test_los_24_agentes_son_invocables_con_el_cliente_simulado(hacer_entorno):
    ent = hacer_entorno()
    for ag in AGENTES:
        r = ent.inv.llamar(ag, "CT-B-PRUEBA", "prueba", {"pet_id": "PET-B-2026-0001"}, "Responde.", {}, {"fecha_as_of": ent.as_of})
        assert isinstance(r, dict) and not r.get("_no_conforme"), ag
    assert len(ent.inv.registro) == 24
    assert {r["agente"] for r in ent.inv.registro} == set(AGENTES)
    assert ent.inv.uc_total > 0


def test_respuesta_no_conforme_degrada_con_incidencia(hacer_entorno):
    from bloque_b.llm import MockClient
    ent = hacer_entorno()
    ent.inv.cliente = MockClient(fallos={"AG-B04": 2})
    r = ent.inv.llamar("AG-B04", "CT-B-10", "dimension", {"dim": "D2"}, "x", {"campo_obligatorio": "string"}, {})
    assert r == {"estado": "PARCIAL", "_no_conforme": True}
    assert any(e.get("tipo") == "RESPUESTA_NO_CONFORME" for e in ent.alm.leer("HA"))
    # un único fallo se repara con el reintento
    ent.inv.cliente = MockClient(fallos={"AG-B04": 1})
    r = ent.inv.llamar("AG-B04", "CT-B-10", "dimension", {"dim": "D2"}, "x", {}, {})
    assert not r.get("_no_conforme")
