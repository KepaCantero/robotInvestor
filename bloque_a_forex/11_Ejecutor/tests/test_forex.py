"""Pruebas de la adaptación al Bloque A Forex (Documento 0 del Bloque A Forex V1.0): seis segmentos y 21 agentes,
capas transversales CT-06T, notación y dirección (2.4), carry, convertibilidad (PS3), referencias de 8.4, exposición
agregada y contradicciones entre segmentos (9.6.6), regla 4 de 2.6 (sin duplicados entre segmentos), carga robusta de
prompts y archivos de referencia."""
import unicodedata
from pathlib import Path

import pandas as pd
import pytest

from conftest import AS_OF, RAIZ, config_pruebas, nuevo_bloque
from bloque_a_forex import fx
from bloque_a_forex.agentes import Agentes
from bloque_a_forex.almacen import Almacen
from bloque_a_forex.configuracion import SEGMENTOS, TABLA_HORIZONTES, buscar_versionado, cargar_config
from bloque_a_forex.consumo import Contabilidad
from bloque_a_forex.contratos import AGENTE_CAPA, AGENTE_SEGMENTO, ANALISTAS, ESQUEMAS, canal_permitido
from bloque_a_forex.herramientas import ht03
from bloque_a_forex.herramientas.ht01_datos import ProveedorCSV, cargar_universo, simbolos_sinteticos
from bloque_a_forex.llm import MockClient
from bloque_a_forex.prompts import NOMBRES, CatalogoPrompts


def test_seis_segmentos_veintiun_agentes_y_canales():
    assert SEGMENTOS == ("G10N", "G10M", "EMAS", "EMLA", "EMEA", "ESTR")
    assert set(AGENTE_SEGMENTO) == set(SEGMENTOS) and set(TABLA_HORIZONTES) == set(SEGMENTOS)
    assert [AGENTE_SEGMENTO[c] for c in SEGMENTOS] == ["AG-03", "AG-04", "AG-05", "AG-06", "AG-07", "AG-08"]
    assert AGENTE_CAPA == {"BCM": "AG-09", "PFV": "AG-21"} and set(NOMBRES) == {f"AG-{i:02d}" for i in range(1, 22)}
    assert set(AGENTE_SEGMENTO.values()) == ANALISTAS
    assert canal_permitido("CT-06T", "AG-02", "AG-09") and canal_permitido("CT-06T", "AG-21", "AG-02")
    assert not canal_permitido("CT-06T", "AG-03", "AG-09") and not canal_permitido("CT-03", "AG-21", "BROKER")
    assert TABLA_HORIZONTES["ESTR"]["H1"] == "NO"                                                # tabla 8.3
    assert all(TABLA_HORIZONTES[c][h] == "LIMITADO" for c in ("EMAS", "EMLA", "EMEA") for h in ("H1", "H4"))


def test_configuracion_por_defecto_forex():
    cfg = cargar_config()
    pu = cfg["presupuesto_uc"]
    assert (pu["N0"], pu["N1"], pu["N2"], pu["N3"], pu["transversal"], pu["ciclo_semanal_max"]) == (1, 5, 18, 50, 6, 140)  # Anexo A
    assert cfg["divisa_base_usuario"] == "EUR" and cfg["methodology_version"] == "FX-1.1"
    assert list(cfg["segmentos_activos"]) == list(SEGMENTOS)
    assert all(f"AG-{i:02d}" in cfg["modelos"] for i in range(1, 22))
    ref = cfg["indices_referencia"]
    assert set(ref) == set(SEGMENTOS)                                                                  # 8.4
    assert {c: ref[c] for c in SEGMENTOS} == {"G10N": "NINGUNA", "G10M": "NINGUNA", "EMAS": "CESTA", "EMLA": "CESTA",
                                              "EMEA": "CESTA", "ESTR": "NINGUNA"}
    assert ":" in cfg["ht01"]["hora_fijacion"] and "/" in cfg["ht01"]["hora_fijacion"]


def test_referencias_de_comparacion(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    assert b._referencia("G10N") is None and b._referencia("ESTR") is None     # rentabilidad en exceso nula
    assert b._referencia("EMLA") == "CESTA"                                    # cesta equiponderada del segmento


def _escribir(d: Path, nombre: str, texto: str = "x") -> Path:
    p = d / nombre
    p.write_text(texto, encoding="utf-8")
    return p


def test_busqueda_de_archivos_por_prefijo_con_preferencia_forex(tmp_path):
    general = _escribir(tmp_path, "System prompt - Analista de G10 núcleo - Versión óptima V5.0.md", "general")
    assert buscar_versionado(tmp_path, "System prompt - Analista de G10 núcleo") == general
    forex = _escribir(tmp_path, "System prompt - Analista de G10 núcleo - Bloque A Forex - Versión óptima V1.0.md", "fx")
    assert buscar_versionado(tmp_path, "System prompt - Analista de G10 núcleo") == forex          # gana el de Forex
    forex2 = _escribir(tmp_path, "System prompt - Analista de G10 núcleo - Bloque A Forex - Versión óptima V1.1.md", "fx2")
    assert buscar_versionado(tmp_path, "System prompt - Analista de G10 núcleo") == forex2         # y la versión más alta
    nfd = unicodedata.normalize("NFD", "System prompt - Analista de Divisas Emergentes de Latinoamérica - Bloque A Forex - "
                                       "Versión óptima V1.0.md")
    p = _escribir(tmp_path, nfd)
    assert buscar_versionado(tmp_path, "System prompt - Analista de Divisas Emergentes de Latinoamérica") == p
    _escribir(tmp_path, "System prompt - Analista de G10 núcleo ampliado - Bloque A Forex - V9.0.md")   # otro agente
    assert buscar_versionado(tmp_path, "System prompt - Analista de G10 núcleo") == forex2
    assert buscar_versionado(tmp_path, "System prompt - Auditor") is None
    e = _escribir(tmp_path, "Esquema JSON - Paquete de oportunidades - Bloque A Forex - V1.0.json", "{}")
    _escribir(tmp_path, "Esquema JSON - Paquete de oportunidades - V5.0.json", "{}")
    assert buscar_versionado(tmp_path, "Esquema JSON - Paquete de oportunidades", ".json") == e


def test_prompts_reales_y_modo_degradado(tmp_path):
    cat = CatalogoPrompts(config_pruebas())
    for ag in NOMBRES:
        a = cat.archivo(ag)
        assert a.exists() and a.name.startswith(f"System prompt - {NOMBRES[ag]} - ") and "Bloque A Forex" in a.name, ag
    d = tmp_path / "prompts"
    d.mkdir()
    _escribir(d, "Marco común de los Analistas de segmento (plantilla) - Bloque A Forex - V1.0.md", "MARCO COMÚN")
    _escribir(d, "System prompt - Analista de Bancos Centrales y Macro Cambiaria - Bloque A Forex - Versión óptima V1.3.md", "BCM")
    _escribir(d, "System prompt - Analista de G10 núcleo - Versión óptima V5.0.md", "GENERAL")
    cfg2 = config_pruebas(rutas={"prompts": str(d)})
    alm = Almacen(tmp_path / "estado")
    ag = Agentes(cfg2, MockClient(), alm, Contabilidad(cfg2))
    assert ag.prompts.texto("AG-09") == "BCM"                                        # sufijo de versión cualquiera
    sust = ag.verificar_prompts(["AG-03", "AG-09", "AG-21"], "RUN-FX-2026-0001")
    assert set(sust) == {"AG-03", "AG-21"}                                           # V5.0 general y marco común: degradado
    assert "MARCO COMÚN" in ag.prompts.texto("AG-21") and ag.prompts.texto("AG-03") == "GENERAL"
    incs = [e for e in alm.leer("HA") if e.get("tipo_entrada") == "INC" and "AG-21" in e.get("detalle", "")]
    assert len(incs) == 1
    ag.verificar_prompts(["AG-21"], "RUN-FX-2026-0002")                              # una sola incidencia
    assert len([e for e in alm.leer("HA") if e.get("tipo_entrada") == "INC" and "AG-21" in e.get("detalle", "")]) == 1
    with pytest.raises(FileNotFoundError):
        ag.prompts.texto("AG-19")                                                     # no es Analista: sin sustituto


def test_universo_de_ambitos_cambiarios(tmp_path):
    u = cargar_universo(RAIZ / "config" / "universo_ejemplo.csv")
    assert set(u["segmento"]) == set(SEGMENTOS)
    assert {"codigo", "segmento", "tipo", "base", "cotizada", "convertible", "ndf"} <= set(u.columns)
    assert u["convertible"].dtype == bool and u["ndf"].dtype == bool
    assert set(u["tipo"]) == {"PAR", "CRUCE", "CESTA", "ESTRATEGIA", "VOLATILIDAD", "REGIMEN"}
    for f in u[u["tipo"].isin(["PAR", "CRUCE", "REGIMEN"])].itertuples():
        assert len(f.base) == 3 and len(f.cotizada) == 3
    prov = ProveedorCSV(RAIZ / "ejemplos" / "datos_sinteticos")
    sims = simbolos_sinteticos(u)
    assert all(prov.tiene(s) for s in sims)                                            # datos para todo el universo y sus tipos
    assert {"TIPO-USD", "TIPO-EUR", "TIPO-JPY", "TIPO-MXN", "TIPO-EGP"} <= set(sims)
    malo = tmp_path / "m.csv"
    malo.write_text("codigo,segmento,tipo,base,cotizada,convertible,ndf\nX,RV,PAR,EUR,USD,si,no\n", encoding="utf-8")
    with pytest.raises(ValueError, match="segmentos desconocidos"):
        cargar_universo(malo)
    malo.write_text("codigo,segmento,tipo,base,cotizada,convertible,ndf\nX,G10N,ETF,EUR,USD,si,no\n", encoding="utf-8")
    with pytest.raises(ValueError, match="tipo no permitido"):
        cargar_universo(malo)
    malo.write_text("codigo,segmento,tipo,base,cotizada,convertible,ndf\nX,ESTR,CESTA,,USD,si,no\n", encoding="utf-8")
    with pytest.raises(ValueError, match="sin composición"):
        cargar_universo(malo)
    malo.write_text("codigo,segmento,tipo,base,cotizada,convertible,ndf\nX\tG10N,PAR,eur,USD,si,no\n".replace("\t", ","), encoding="utf-8")
    with pytest.raises(ValueError, match="ISO 4217"):
        cargar_universo(malo)


def test_esquema_de_finalista_cambiaria():
    import jsonschema
    fin = ESQUEMAS["INFORME_SEGMENTO"]["properties"]["finalistas"]["items"]
    req = set(fin["required"])
    assert {"par", "composicion", "direccion", "divisa_financiacion", "convertibilidad", "indicador_seguimiento",
            "consideraciones_implementacion", "metricas_clave", "preguntas_para_B"} <= req
    assert "subtipo" not in req and "invertibilidad" not in req and "criterios_seleccion_sugeridos" not in req
    assert set(fin["properties"]["dimensiones"]["properties"]["A"]["properties"]) == set(ht03.PARAMETROS_POR_DEFECTO["pesos"]["A"])
    v = jsonschema.Draft202012Validator(fin)
    for prohibido in ("instrumento", "ejemplos_ilustrativos", "apalancamiento", "nivel_entrada"):
        assert any(e.validator == "not" for e in v.iter_errors({prohibido: "x"}))


def test_utilidades_fx_notacion_exposicion_y_textos():
    comp = fx.composicion_par("USD/JPY", "BAJISTA_BASE")
    assert comp == [{"divisa": "USD", "peso": 1.0, "lado": "CORTO"}, {"divisa": "JPY", "peso": 1.0, "lado": "LARGO"}]
    assert fx.nombre_llano(comp, "PAR", "USD/JPY") == "El yen japonés podría ganar valor frente al dólar de EE. UU."
    assert fx.sube_baja_llano(comp) == "Sube el yen japonés y baja el dólar de EE. UU."
    cesta = fx.composicion_fila({"composicion": "AUD:LARGO:0.5;NZD:LARGO:0.5;JPY:CORTO:1.0"})
    assert fx.exposicion_neta([{"composicion": cesta}, {"composicion": fx.invertir(cesta)}]) == {}
    neta = fx.exposicion_neta([{"composicion": comp}, {"composicion": cesta}])
    assert neta == {"USD": -1.0, "JPY": 0.0} or neta == {"USD": -1.0, "AUD": 0.5, "NZD": 0.5}
    assert fx.categoria_exposicion(0.5) == "larga moderada" and fx.categoria_exposicion(-2) == "corta fuerte"
    assert fx.categoria_exposicion(1) == "larga" and fx.categoria_exposicion(0) == "neutra"
    assert fx.indicador_sube({"tipo_opcion": "CESTA", "composicion": fx.invertir(cesta)}, {"composicion": "AUD:LARGO:0.5;NZD:LARGO:0.5;JPY:CORTO:1.0"}) is False
    assert fx.sin_jerga("Carry G10 y momentum") == "Diferencia de intereses grandes monedas y tendencia"


def test_normalizacion_fx_de_las_finalistas(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    f = {"proxy": "USDJPY", "tipo_opcion": "PAR", "direccion": "BAJISTA_BASE", "composicion": [], "nombre": "x"}
    assert b._normalizar_fx(f) is None
    assert f["par"] == "USD/JPY" and f["divisa_financiacion"] == "USD" and f["_sube"] is False
    assert {c["divisa"]: c["lado"] for c in f["composicion"]} == {"USD": "CORTO", "JPY": "LARGO"}
    assert b._normalizar_fx({"proxy": "USDJPY", "tipo_opcion": "PAR", "direccion": None}) == "dirección sin especificar (PS4)"
    v = {"proxy": "VOL-EURUSD-1M", "vista_volatilidad": {"sentido": "BAJA", "plazo": "1M"}}
    assert b._normalizar_fx(v) is None and v["direccion"] is None and v["composicion"] == [] and v["_sube"] is False
    c = {"proxy": "FX-CARRY-G10", "composicion": [{"divisa": "AUD", "peso": 0.7, "lado": "LARGO"}]}   # pesos mal: se toma el universo
    assert b._normalizar_fx(c) is None and len(c["composicion"]) == 5 and c["divisa_financiacion"] in ("JPY", "CHF")
    inr = {"proxy": "USDINR", "direccion": "BAJISTA_BASE"}
    assert b._normalizar_fx(inr) is None
    assert inr["convertibilidad"]["convertible"] is False and inr["convertibilidad"]["ndf"] is True and b._ps3(inr)
    hkd = {"proxy": "USDHKD", "direccion": "ALCISTA_BASE"}
    assert b._normalizar_fx(hkd) is None and hkd["regimen_cambiario_divisa"] == "CAJA_CONVERSION"


def _evaluada(oid, segmento, nivel=70):
    dims = {k: {d: nivel for d in ht03.PARAMETROS_POR_DEFECTO["pesos"][k]} for k in ("T", "E", "A")}
    dims["M"] = {d: 50 for d in ht03.PARAMETROS_POR_DEFECTO["pesos"]["M"]}
    dims["P"] = {"novedad": 60, "incertidumbre_reducible": 60, "coste_eficiencia": 60}
    return ht03.evaluar_opcion({"opp_id": oid, "segmento": segmento, "dimensiones": dims, "cluster": oid,
                                "puertas": {g: True for g in ht03.PARAMETROS_POR_DEFECTO["puertas_obligatorias"]}})


def _seleccion(b, cand, ev):
    return {c: {"candidatos": cand[c], "evaluadas": ev[c], "n_cand": 4, "seleccion": ht03.seleccionar_top3(ev[c], b.params_ht03, 4)}
            for c in cand}


def test_sin_duplicados_entre_segmentos(tmp_path, universo):
    """Regla 4 de 2.6: la misma exposición (par y dirección) no puede figurar en dos top-3; se queda la de mayor RK."""
    b = nuevo_bloque(tmp_path, universo)
    usdmxn = fx.composicion_par("USD/MXN", "BAJISTA_BASE")
    cand = {"EMLA": [{"opp_id": "OPP-FX-2026-0901", "nombre": "USD/MXN bajista", "tipo_opcion": "PAR", "par": "USD/MXN",
                      "direccion": "BAJISTA_BASE", "composicion": usdmxn},
                     {"opp_id": "OPP-FX-2026-0902", "nombre": "USD/BRL bajista", "tipo_opcion": "PAR", "par": "USD/BRL",
                      "direccion": "BAJISTA_BASE", "composicion": fx.composicion_par("USD/BRL", "BAJISTA_BASE")}],
            "ESTR": [{"opp_id": "OPP-FX-2026-0903", "nombre": "Peso mexicano frente al dólar", "tipo_opcion": "PAR",
                      "par": "USD/MXN", "direccion": "BAJISTA_BASE", "composicion": usdmxn}]}
    ev = {"EMLA": [_evaluada("OPP-FX-2026-0901", "EMLA", 80), _evaluada("OPP-FX-2026-0902", "EMLA", 70)],
          "ESTR": [_evaluada("OPP-FX-2026-0903", "ESTR", 70)]}
    sel = _seleccion(b, cand, ev)
    quitadas = b._deduplicar_entre_segmentos(sel)
    assert [q["opp_id"] for q in quitadas] == ["OPP-FX-2026-0903"]                 # duplicada por exposición
    assert sel["ESTR"]["seleccion"]["top3"] == [] and sel["ESTR"]["seleccion"]["menos_de_tres_motivo"]
    motivos = sel["ESTR"]["evaluadas"][0]["motivos_no_elegible"]
    assert motivos[-1]["codigo"] == "DUPLICADA_EN_OTRO_SEGMENTO" and "OPP-FX-2026-0901" in motivos[-1]["detalle"]


def test_contradicciones_entre_segmentos(tmp_path, universo):
    """9.6.6: una misma divisa como pata activa de la tesis, larga en un segmento y corta en otro, se justifica
    (Analizador) o se resuelve (sale la de menor RK). El USD o el EUR como contrapartida no cuentan."""
    b = nuevo_bloque(tmp_path, universo)

    def preparar(par_a, dir_a, par_b, dir_b, tipo_b="CRUCE"):
        cand = {"G10N": [{"opp_id": "OPP-FX-2026-0801", "tipo_opcion": "PAR", "par": par_a, "composicion": fx.composicion_par(par_a, dir_a)}],
                "G10M": [{"opp_id": "OPP-FX-2026-0802", "tipo_opcion": tipo_b, "par": par_b, "composicion": fx.composicion_par(par_b, dir_b)}]}
        ev = {"G10N": [_evaluada("OPP-FX-2026-0801", "G10N", 80)], "G10M": [_evaluada("OPP-FX-2026-0802", "G10M", 70)]}
        return _seleccion(b, cand, ev)
    # JPY pata activa larga en G10N (USD/JPY bajista) y corta en G10M (CAD/JPY alcista): contradicción real
    sel = preparar("USD/JPY", "BAJISTA_BASE", "CAD/JPY", "ALCISTA_BASE")
    integ = {"contradicciones": []}
    q = b._resolver_contradicciones(sel, integ)
    assert [x["opp_id"] for x in q] == ["OPP-FX-2026-0802"] and q[0]["divisa"] == "JPY" and integ["contradicciones_resueltas"] == q
    assert sel["G10M"]["seleccion"]["top3"] == []
    assert sel["G10M"]["evaluadas"][0]["motivos_no_elegible"][-1]["codigo"] == "CONTRADICCION_ENTRE_SEGMENTOS"
    sel = preparar("USD/JPY", "BAJISTA_BASE", "CAD/JPY", "ALCISTA_BASE")
    just = {"contradicciones": [{"divisa": "JPY", "justificacion_contradiccion": "Plazos distintos: H2 en G10M frente a H4 en G10N."}]}
    assert b._resolver_contradicciones(sel, just) == [] and len(sel["G10M"]["seleccion"]["top3"]) == 1
    # USD como contrapartida en direcciones distintas (USD/JPY bajista y USD/CAD alcista): no es contradicción
    sel = preparar("USD/JPY", "BAJISTA_BASE", "USD/CAD", "ALCISTA_BASE", "PAR")
    assert b._resolver_contradicciones(sel, {"contradicciones": []}) == []
    # EUR como contrapartida (EUR/USD alcista frente a EUR/PLN bajista): tampoco
    sel = preparar("EUR/USD", "ALCISTA_BASE", "EUR/PLN", "BAJISTA_BASE")
    assert b._resolver_contradicciones(sel, {"contradicciones": []}) == []


def test_gc0_tercio_de_pares_e_indice_representativo(tmp_path, universo):
    """Anexo A (1): cambio material si al menos un tercio de los pares vigilados se mueve > 1,5 σ semanales o si lo hace
    el índice representativo, o una opción vigente o finalista."""
    from bloque_a_forex.herramientas.ht01_datos import ProveedorSintetico
    idx = pd.bdate_range("2024-01-01", "2026-06-05")
    rng = __import__("numpy").random.default_rng(4)

    def serie(salto=0.0):
        r = rng.normal(0, 0.004, len(idx))
        r[-5:] = salto / 5                                  # última semana: quieta o con un salto

        return pd.DataFrame({"cierre": 1.0 * __import__("numpy").exp(__import__("numpy").cumsum(r))}, index=idx)
    u = universo[universo["simbolo"].isin(["AUDUSD", "NZDUSD", "USDCAD"])].copy()

    def bloque(saltos, nombre):
        prov = ProveedorSintetico({}, fijos={s: serie(x) for s, x in zip(["AUDUSD", "NZDUSD", "USDCAD"], saltos)})
        bq = Bloque_(tmp_path / nombre, prov, u)
        bq.fijar_fecha(AS_OF)
        return bq
    from bloque_a_forex.orquestacion import Bloque

    def Bloque_(d, prov, uni):
        return Bloque(config_pruebas(), prov, uni, MockClient(), d / "estado", d / "ent")
    quietos = bloque([0.0, 0.0, 0.0], "a").gc0("G10M", AS_OF, [])
    assert not any("pares vigilados" in m or "índice representativo" in m for m in quietos["motivos"])
    uno = bloque([0.08, 0.0, 0.0], "b")
    g = uno.gc0("G10M", AS_OF, [])
    assert any("1 de 3 pares vigilados" in m for m in g["motivos"])                # un tercio
    g = uno.gc0("G10M", AS_OF, [{"opp_id": "OPP-FX-2026-0001", "indicador_seguimiento": {"simbolo": "AUDUSD"}}])
    assert any("opción vigente o finalista sobre AUDUSD" in m for m in g["motivos"])


def test_referencia_ingenua_paseo_aleatorio_y_forward(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    r = b.evaluador.referencia_ingenua("USDMXN", "EMLA", 126, True, AS_OF, carry_indicador_pct=-5.5)
    assert r["valor_o_prob"] == 0.5 and r["calc_id"].startswith("CALC-FX-")
    assert r["cambio_forward"] > 0 and r["prob_forward"] > 0.5        # el forward descuenta la subida de lo que rinde menos
    r2 = b.evaluador.referencia_ingenua("USDMXN", "EMLA", 126, False, AS_OF, carry_indicador_pct=-5.5)
    assert r2["prob_forward"] == pytest.approx(1 - r["prob_forward"], abs=1e-3)
    assert b.evaluador.referencia_ingenua("VOL-EURUSD-1M", "G10N", 20, True, AS_OF)["prob_forward"] is None


def test_archivos_de_referencia_reales_se_localizan_y_se_leen():
    """Evita el fallo silencioso de arrancar sin referencias si cambia el sufijo de versión de F7–F9/FM."""
    from bloque_a_forex.referencias import Referencias
    r = Referencias(cargar_config())
    for k in ("F7", "F8", "F9", "FM"):
        assert r.rutas[k].exists(), f"No se encuentra el archivo de referencias {k}: {r.rutas[k]}"
        assert len(r.fichas[k]) > 0, f"{k} sin fichas legibles"
