"""Pruebas de la adaptación a la V5.0 (Documento 0 óptima V5.0): doce tipos de activo, frontera con el Bloque B,
carga robusta de prompts, universo de ámbitos con indicador de seguimiento, referencias de 8.4, presupuestos del
Anexo A y regla 5 de 2.6 (sin duplicados entre tipos)."""
import unicodedata
from pathlib import Path

import pandas as pd
import pytest

from conftest import AS_OF, RAIZ, config_pruebas, nuevo_bloque
from bloque_a.almacen import Almacen
from bloque_a.agentes import Agentes
from bloque_a.configuracion import CLASES, TABLA_HORIZONTES, buscar_versionado, cargar_config
from bloque_a.consumo import Contabilidad
from bloque_a.contratos import AGENTE_CLASE, ANALISTAS, ESQUEMAS, canal_permitido
from bloque_a.herramientas import ht03
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.prompts import NOMBRES, CatalogoPrompts


def test_doce_tipos_agentes_y_canales():
    assert CLASES == ("RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV")
    assert set(AGENTE_CLASE) == set(CLASES) and set(TABLA_HORIZONTES) == set(CLASES)
    assert {AGENTE_CLASE[c] for c in ("IDX", "FON", "DER", "MON", "TCV")} == {"AG-21", "AG-22", "AG-23", "AG-24", "AG-25"}
    assert set(AGENTE_CLASE.values()) == ANALISTAS and all(a in NOMBRES for a in ANALISTAS)
    assert canal_permitido("CT-06", "AG-02", "AG-25") and canal_permitido("CT-06", "AG-23", "AG-02")
    assert not canal_permitido("CT-03", "AG-21", "BROKER")
    assert TABLA_HORIZONTES["FON"]["H1"] == "NO" and TABLA_HORIZONTES["DER"]["H4"] == "NO" and TABLA_HORIZONTES["MON"]["H4"] == "NO"


def test_configuracion_por_defecto_v5():
    cfg = cargar_config()
    pu = cfg["presupuesto_uc"]
    assert (pu["N0"], pu["N1"], pu["N2"], pu["N3"], pu["ciclo_semanal_max"]) == (1, 5, 18, 50, 240)      # Anexo A
    assert all(f"AG-{i}" in cfg["modelos"] for i in range(21, 26))
    ref = cfg["indices_referencia"]
    assert set(ref) == set(CLASES)                                                                        # 8.4
    assert (ref["IDX"], ref["DER"], ref["MON"], ref["TCV"], ref["FON"]) == ("ACWI", "SUBYACENTE", "XEON.DE", "NINGUNA", "CESTA")


def test_referencias_de_comparacion(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    assert b._referencia("DER", "^BXM") == "SPY"                 # rentabilidad del subyacente sin derivado
    assert b._referencia("TCV", "^VIX") is None                  # posición neutra: pronóstico absoluto
    assert b._referencia("MON") == "XEON.DE" and b._referencia("FON") == "CESTA" and b._referencia("IDX") == "ACWI"
    u = universo.copy()
    u.loc[u["simbolo"] == "^PUT", "subyacente"] = ""
    b2 = nuevo_bloque(tmp_path / "b", universo, universo_df=u)
    assert b2._referencia("DER", "^PUT") == "CESTA"              # sin subyacente: cesta del tipo


def _escribir(d: Path, nombre: str, texto: str = "x") -> Path:
    p = d / nombre
    p.write_text(texto, encoding="utf-8")
    return p


def test_busqueda_de_archivos_versionados(tmp_path):
    _escribir(tmp_path, "System prompt - Analista de Índices Bursátiles - Versión óptima V5.0.md", "v4")
    v5 = _escribir(tmp_path, "System prompt - Analista de Índices Bursátiles - Versión óptima V5.0.md", "v5")
    _escribir(tmp_path, "System prompt - Analista de Índices Bursátiles Globales - Versión óptima V9.0.md")   # otro agente
    assert buscar_versionado(tmp_path, "System prompt - Analista de Índices Bursátiles") == v5
    nfd = unicodedata.normalize("NFD", "System prompt - Analista de Fondos y Vehículos de Inversión Colectiva - Versión óptima V5.0.md")
    p = _escribir(tmp_path, nfd)
    assert buscar_versionado(tmp_path, "System prompt - Analista de Fondos y Vehículos de Inversión Colectiva") == p
    # nombre V5.0 y nombre anterior del mismo agente: gana la versión más alta
    viejo = _escribir(tmp_path, "System prompt - Analista de Renta Fija y Crédito - Versión óptima V5.0.md")
    bases = ["System prompt - Analista de Renta Fija", "System prompt - Analista de Renta Fija y Crédito"]
    assert buscar_versionado(tmp_path, bases) == viejo
    nuevo = _escribir(tmp_path, "System prompt - Analista de Renta Fija - Versión óptima V5.0.md")
    assert buscar_versionado(tmp_path, bases) == nuevo
    assert buscar_versionado(tmp_path, "System prompt - Auditor") is None
    _escribir(tmp_path, "Esquema JSON - Paquete de oportunidades - V5.0.json", "{}")
    e5 = _escribir(tmp_path, "Esquema JSON - Paquete de oportunidades - V5.0.json", "{}")
    assert buscar_versionado(tmp_path, "Esquema JSON - Paquete de oportunidades", ".json") == e5


def test_prompts_de_los_analistas_nuevos_y_modo_degradado(tmp_path):
    cfg = config_pruebas()
    cat = CatalogoPrompts(cfg)
    for ag in ("AG-21", "AG-22", "AG-23", "AG-24", "AG-25"):
        assert cat.archivo(ag).name.startswith(f"System prompt - {NOMBRES[ag]} - ")
    d = tmp_path / "prompts"
    d.mkdir()
    _escribir(d, "Marco común de los Analistas de tipo de activo (plantilla) - V5.0.md", "MARCO COMÚN")
    _escribir(d, "System prompt - Analista de Derivados Financieros - Versión óptima V5.0.md", "DERIVADOS")
    cfg2 = config_pruebas(rutas={"prompts": str(d)})
    alm = Almacen(tmp_path / "estado")
    ag = Agentes(cfg2, MockClient(), alm, Contabilidad(cfg2))
    assert ag.prompts.texto("AG-23") == "DERIVADOS"                                  # sufijo de versión cualquiera
    sust = ag.verificar_prompts(["AG-21", "AG-23"], "RUN-2026-0001")
    assert set(sust) == {"AG-21"} and "MARCO COMÚN" in ag.prompts.texto("AG-21")
    incs = [e for e in alm.leer("HA") if e.get("tipo_entrada") == "INC" and "AG-21" in e.get("detalle", "")]
    assert len(incs) == 1 and incs[0]["severidad"] == "Operativa"
    ag.verificar_prompts(["AG-21"], "RUN-2026-0002")                                  # una sola incidencia
    assert len([e for e in alm.leer("HA") if e.get("tipo_entrada") == "INC" and "AG-21" in e.get("detalle", "")]) == 1
    with pytest.raises(FileNotFoundError):
        ag.prompts.texto("AG-19")                                                     # no es Analista: sin sustituto
    cfg3 = config_pruebas(rutas={"prompts": str(d)}, prompts={"marco_comun_si_falta": False})
    with pytest.raises(FileNotFoundError):
        CatalogoPrompts(cfg3).texto("AG-22")


def test_universo_de_ambitos_con_indicador(tmp_path):
    u = cargar_universo(RAIZ / "config" / "universo_ejemplo.csv")
    assert set(u["clase"]) == set(CLASES)
    assert {"subtipo", "ambito_incluye", "ambito_excluye", "indicador", "subyacente"} <= set(u.columns)
    assert not (u["tipo_opcion"].isin(["INSTRUMENTO_GENERICO", "INDUSTRIA"])).any()
    for s in ("^VIX", "T10YIE", "BAMLH0A0HYM2", "CURVA-USD-2S10S-TR", "XEON.DE", "BIL", "^NSEI", "CEFS", "^BXM"):
        assert s in set(u["simbolo"])
    prov = ProveedorCSV(RAIZ / "ejemplos" / "datos_sinteticos")
    assert all(prov.tiene(s) for s in u["simbolo"])                                   # datos sintéticos para todo el universo
    # Compatibilidad V4.x: tipos de opción retirados se reinterpretan; columnas opcionales ausentes se rellenan
    viejo = tmp_path / "u.csv"
    viejo.write_text("simbolo,clase,nombre,tipo_opcion,region,sector,divisa,notas\n"
                     "GLD,MP,Oro,INSTRUMENTO_GENERICO,GLB,Metales,USD,x\nXLI,RV,Industria,INDUSTRIA,NAM,Industria,USD,x\n", encoding="utf-8")
    uv = cargar_universo(viejo)
    assert list(uv["tipo_opcion"]) == ["SEGMENTO", "SUBSECTOR"] and (uv["subyacente"] == "").all()
    malo = tmp_path / "m.csv"
    malo.write_text("simbolo,clase,nombre,tipo_opcion,region,sector,divisa,notas\nX,RV,X,ACCION_CONCRETA,NAM,s,USD,x\n", encoding="utf-8")
    with pytest.raises(ValueError, match="tipo_opcion"):
        cargar_universo(malo)
    malo.write_text("simbolo,clase,nombre,tipo_opcion,region,sector,divisa,notas\nX,ETF,X,SECTOR,NAM,s,USD,x\n", encoding="utf-8")
    with pytest.raises(ValueError, match="desconocidos"):
        cargar_universo(malo)


def test_esquema_de_finalista_sin_vehiculos():
    import jsonschema
    fin = ESQUEMAS["INFORME_CLASE"]["properties"]["finalistas"]["items"]
    req = set(fin["required"])
    assert {"ambito", "indicador_seguimiento", "invertibilidad", "subtipo", "criterios_seleccion_sugeridos", "metricas_clave",
            "preguntas_para_B"} <= req
    assert "proxy_backtest" not in req and "vehiculos_genericos" not in req
    assert fin["properties"]["tipo_opcion"]["enum"] == ["MERCADO", "SECTOR", "SUBSECTOR", "TEMATICA", "SEGMENTO", "FACTOR", "ESTILO", "ESTRATEGIA"]
    v = jsonschema.Draft202012Validator(fin)
    assert any("vehiculos_genericos" in str(e.message) or e.validator == "not" for e in v.iter_errors({"vehiculos_genericos": ["ETF"]}))
    assert ESQUEMAS["INFORME_CLASE"]["properties"]["finalistas"]["items"]["properties"]["dimensiones"]


def _evaluada(oid, clase, rk_dims=70):
    dims = {"T": {k: rk_dims for k in ht03.PARAMETROS_POR_DEFECTO["pesos"]["T"]},
            "E": {k: rk_dims for k in ht03.PARAMETROS_POR_DEFECTO["pesos"]["E"]},
            "M": {k: 50 for k in ht03.PARAMETROS_POR_DEFECTO["pesos"]["M"]},
            "A": {k: rk_dims for k in ht03.PARAMETROS_POR_DEFECTO["pesos"]["A"]},
            "P": {"novedad": 60, "incertidumbre_reducible": 60, "coste_eficiencia": 60}}
    return ht03.evaluar_opcion({"opp_id": oid, "tipo_activo": clase, "dimensiones": dims, "cluster": oid,
                                "puertas": {g: True for g in ht03.PARAMETROS_POR_DEFECTO["puertas_obligatorias"]}})


def test_sin_duplicados_entre_tipos(tmp_path, universo):
    """Regla 5 de 2.6: el mismo ámbito no puede figurar en dos top-3; se queda la opción de mayor RK."""
    b = nuevo_bloque(tmp_path, universo)
    amb = {"incluye": "Bonos del Tesoro de EE. UU. ligados a la inflación", "excluye": "x", "region": "EE. UU."}
    cand = {"RF": [{"opp_id": "OPP-2026-0901", "nombre": "Inflación en EE. UU.", "ambito": amb},
                   {"opp_id": "OPP-2026-0902", "nombre": "Crédito IG", "ambito": {**amb, "incluye": "Crédito IG"}}],
            "TCV": [{"opp_id": "OPP-2026-0903", "nombre": "INFLACIÓN en EE.UU.", "ambito": {**amb, "incluye": "Factor inflación"}}]}
    ev = {"RF": [_evaluada("OPP-2026-0901", "RF", 80), _evaluada("OPP-2026-0902", "RF", 70)],
          "TCV": [_evaluada("OPP-2026-0903", "TCV", 70)]}
    sel = {c: {"candidatos": cand[c], "evaluadas": ev[c], "n_cand": 4, "seleccion": ht03.seleccionar_top3(ev[c], b.params_ht03, 4)}
           for c in cand}
    quitadas = b._deduplicar_entre_tipos(sel)
    assert [q["opp_id"] for q in quitadas] == ["OPP-2026-0903"]                 # duplicada por nombre normalizado
    assert sel["TCV"]["seleccion"]["top3"] == [] and sel["TCV"]["seleccion"]["menos_de_tres_motivo"]
    assert [t["opp_id"] for t in sel["RF"]["seleccion"]["top3"]] == ["OPP-2026-0901", "OPP-2026-0902"]
    motivos = sel["TCV"]["evaluadas"][0]["motivos_no_elegible"]
    assert motivos[-1]["codigo"] == "DUPLICADA_EN_OTRO_TIPO" and "OPP-2026-0901" in motivos[-1]["detalle"]


def test_referencias_reales_se_cargan_con_cualquier_version():
    """Evita el fallo silencioso de arrancar sin referencias si cambia el sufijo de versión de F7–F9/FM."""
    from bloque_a.configuracion import cargar_config
    from bloque_a.referencias import Referencias
    r = Referencias(cargar_config())
    for k in ("F7", "F8", "F9", "FM"):
        assert r.rutas[k].exists(), f"No se encuentra el archivo de referencias {k}: {r.rutas[k]}"
        assert len(r.fichas[k]) >= 100, f"{k} con muy pocas fichas: {len(r.fichas[k])}"
