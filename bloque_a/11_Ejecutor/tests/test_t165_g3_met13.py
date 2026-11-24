"""T-165 · G3-MET-13 «Madurez declarada» (PB-47, R22): comprobación complementaria de HT-09 en el ejecutor.

Desde la r03 (QA r02 NO APTO) el enfoque es estructural (INC-T165-01): la madurez de un método solo la escribe el ejecutor, en una
forma canónica junto a cada ficha («ST-DESC-001 [madurez: IMPLEMENTADO]»), y la prosa del modelo no se interpreta: la raíz
«valid-» en un ámbito que nombra un método bloquea, una ficha que el Motor no sirve no se nombra sin su forma canónica y una forma
canónica que no coincide con el Catálogo bloquea.

Unitarias de `ht09.comprobar_madurez`, `ht09.textos_de`, `ht09.anotar_madurez` y de `sintesis` (ámbito, localización y campos de
madurez de los informes de clase), y de extremo a extremo con el cliente simulado (`MockClient`, sin red ni coste): PB-47 con su
preparación completa, la declaración corregida, el informe técnico y el visual, y el ciclo normal con la madurez canónica.
"""
import json
import re
from pathlib import Path
from types import SimpleNamespace

import pytest
from bloque_a.herramientas import ht09
from bloque_a.motor import servicio
from bloque_a.redaccion import Redaccion
from conftest import AS_OF, config_pruebas, nuevo_bloque
from tiempo_cpu import minimos_intercalados

from bloque_a import mock_respuestas
from bloque_a import sintesis as sint

MADUREZ = {"ML-CLUS-001": "DOCUMENTADO", "ST-DESC-001": "IMPLEMENTADO", "DER-OPT-001": "DOCUMENTADO",
           "VOL-GARCH-001": "IMPLEMENTADO", "FX-PPA-001": "IMPLEMENTADO", "FX-COINT-001": "IMPLEMENTADO",
           "FON-DISC-001": "DOCUMENTADO", "AUD-REX-001": "IMPLEMENTADO", "IDX-CONC-001": "Implementado (referencia)",
           "FC-EVAL-001": "VALIDADO"}
BLOQUE_REAL = SimpleNamespace(motor=SimpleNamespace(raiz=None))


def _sirve(f):
    return ht09.nivel_catalogo(MADUREZ.get(f)) >= 2


def _comp(texto, sev="BLOQUEO", madurez=MADUREZ, sirve=_sirve):
    return ht09.comprobar_madurez([("r", texto, sev)], madurez, sirve, madurez)


def _real(texto, sev="BLOQUEO"):
    return sint._comprobar_met13(BLOQUE_REAL, [("r", texto, sev)])


def _json_real(obj, ruta="paquete"):
    return sint._comprobar_met13(BLOQUE_REAL, [(r, t, "BLOQUEO") for r, t in ht09.textos_de(obj, ruta)])


def _documentado(monkeypatch, ficha="ML-CLUS-001"):
    original = servicio.madurez_catalogo
    monkeypatch.setattr(servicio, "madurez_catalogo", lambda raiz=None: {**original(raiz), ficha: "DOCUMENTADO"})


# ------------------------------------------------------------------ comprobar_madurez: lo que bloquea (reglas A, B y C)
@pytest.mark.parametrize("texto, ficha", [
    ("Los clústeres de exposición se calculan con ML-CLUS-001, un método validado.", "ML-CLUS-001"),   # PB-47 (A y B)
    ("ST-DESC-001 está validado en backtest", "ST-DESC-001"),           # A: nada nombrado está VALIDADO
    ("ST-DESC-001 no está validado", "ST-DESC-001"),                    # A: la negación no se interpreta
    ("ML-CLUS-001 [madurez: DOCUMENTADO; no la sirve el Motor] está implementado", "ML-CLUS-001"),  # A: «implement-» de un DOCUMENTADO
    ("La señal sale de ML-SUPER-001", "ML-SUPER-001"),                  # B: una ficha que no existe y no se sirve
    ("N efectivo ML-CLUS-001: 12", "ML-CLUS-001"),                      # B: nombrada sin servirse ni su forma canónica
    ("ML-CLUS-001: documentado, no se sirve", "ML-CLUS-001"),           # B: la declaración del modelo no cuenta
    ("ST-DESC-001 [madurez: VALIDADO]", "ST-DESC-001"),                 # C: no coincide con el Catálogo
    ("ML-CLUS-001 [madurez: DOCUMENTADO]", "ML-CLUS-001"),              # C: falta «no la sirve el Motor»
    ("FX-PPA-001 VALIDATED", "FX-PPA-001"),
    ("VOL-GARCH-001, revalidado en 2025, sostiene la banda.", "VOL-GARCH-001"),   # la raíz con prefijo
    ("FC-EVAL-001 y ST-DESC-001: validados", "ST-DESC-001"),           # A: una VALIDADO no cubre a la otra
])
def test_bloquea(texto, ficha):
    c = _comp(texto)
    assert c["resultado"] == "BLOQUEO", c
    assert c["id"] == "G3-MET-13" and any(ficha in i["detalle"] and i["severidad"] == "BLOQUEO" and i["ruta"] == "r"
                                          for i in c["incidencias"])


@pytest.mark.parametrize("texto", [
    "El percentil del precio está validado por el método de rangos.",   # A: un sustantivo de método sin ficha
    "Madurez: validado.",                                                # el sustantivo de madurez
    "[madurez: IMPLEMENTADO]",                                           # C: una forma canónica que no sigue a una ficha
    "Resultado validado en el backtest de tres años.",
])
def test_bloquea_sin_ficha(texto):
    assert _comp(texto)["resultado"] == "BLOQUEO", texto


# ------------------------------------------------------------------ comprobar_madurez: lo que no salta
@pytest.mark.parametrize("texto", [
    "Precio en el percentil 96% de sus últimos tres años (ST-DESC-001).",   # servida y sin madurez
    "Precio (ST-DESC-001 [madurez: IMPLEMENTADO]).",                     # la forma canónica correcta no se lee
    "Los clústeres no se calculan: ML-CLUS-001 [madurez: DOCUMENTADO; no la sirve el Motor].",
    "FC-EVAL-001 [madurez: VALIDADO] mide la calibración.",             # una VALIDADO con su forma canónica
    "FC-EVAL-001 está validado.",                                        # solo fichas en VALIDADO y ningún sustantivo de método
    "IDX-CONC-001 implementado",                                         # «Implementado (referencia)»
    "Re-ejecución CT-10 con AUD-REX-001",
    "CALC-2026-0001 de OPP-2026-0003, G3-MET-13 y DEC-2026-001: todo validado",   # no son fichas ni sustantivos de método
    "El umbral fue validado por el operador.",                           # sin método en el ámbito
    "Invalidación: el precio cae bajo el percentil 50 (ST-DESC-001).",    # «invalid-» no es la raíz
    "Hemos comprobado con ST-DESC-001 que el precio está en el percentil 95 %.",   # H-18: los sinónimos no cuentan
    "Riesgo verificado con RISK-DD-001: caída máxima del 22 %.",
    "ST-DESC-001 documentado",                                           # infradeclarar no salta
])
def test_no_salta(texto):
    c = _comp(texto) if "RISK" not in texto else _real(texto)
    assert c["resultado"] == "OK" and not c["incidencias"], c


def test_formato_de_ht09_y_severidad_advertencia_sin_extracto():
    c = _comp("ML-CLUS-001, un método validado. OPP-2026-0007", sev="ADVERTENCIA")
    assert set(c) == {"id", "nombre", "resultado", "incidencias", "datos"} and c["resultado"] == "ADVERTENCIA"
    assert c["nombre"] == ht09.NOMBRE_MET13 and c["datos"]["fichas_citadas"] == ["ML-CLUS-001"]
    assert all(set(i) == {"severidad", "ruta", "detalle"} and "OPP-" not in i["detalle"] for i in c["incidencias"])
    primera = c["incidencias"][0]   # primero la madurez afirmada (regla A), después la ficha no servida (B)
    assert "«validado»" in primera["detalle"] and "«DOCUMENTADO»" in primera["detalle"] and "método validado" not in primera["detalle"]
    assert any("forma canónica «ML-CLUS-001 [madurez: DOCUMENTADO; no la sirve el Motor]»" in i["detalle"] for i in c["incidencias"])


def test_el_extracto_de_un_bloqueo_no_lleva_otra_opcion():
    paquete = {"clases": {"RV": {"opciones": [
        {"opp_id": "OPP-2026-0001", "mecanismo": "Complementa a OPP-2026-0002, y VOL-GARCH-001 está validado."},
        {"opp_id": "OPP-2026-0002", "mecanismo": "Persistencia del impulso."}]}}}
    c = sint.g3_met13(BLOQUE_REAL, paquete, {}, None)
    afectadas = {x for i in c["incidencias"] for x in re.findall(r"OPP-\d{4}-\d{4,}", i["ruta"] + " " + i["detalle"])}
    assert c["resultado"] == "BLOQUEO" and afectadas == {"OPP-2026-0001"}


def test_sin_catalogo_legible_toda_mencion_bloquea():
    c = ht09.comprobar_madurez([("r", "Percentil (ST-DESC-001).", "BLOQUEO")], {}, lambda f: False, servicio.FICHAS_CATALOGO)
    assert c["resultado"] == "BLOQUEO"


def test_una_mencion_repetida_en_la_misma_ruta_se_anota_una_vez():
    c = ht09.comprobar_madurez([("r", "ST-DESC-001 validado.", "BLOQUEO")] * 3, MADUREZ, _sirve, MADUREZ)
    assert len(c["incidencias"]) == 1


def test_aud_rex_001_se_sirve_por_ct10():
    assert sint._sirve(BLOQUE_REAL)("AUD-REX-001") and not servicio.servible("AUD-REX-001")
    assert _real("Re-ejecución CT-10 con AUD-REX-001.")["resultado"] == "OK"


# ------------------------------------------------------------------ fichas con otra grafía (H-04, H-21) y coste (H-10, H-22)
@pytest.mark.parametrize("escrita", ["ST_DESC_001", "st_desc_001", "ST.DESC.001", "ST-DESC-0001", "st desc 001", "ST‑DESC‑001",
                                     "vol_garch_001", "VOL-GARCH"])
def test_una_ficha_con_otra_grafia_se_reconoce(escrita):
    fx = ht09.fichas_de(servicio.FICHAS_CATALOGO)
    (m,) = fx.buscar(ht09.normalizar(f"La señal sale de {escrita}."))
    assert m[2] in ("ST-DESC-001", "VOL-GARCH-001")
    assert _real(f"{escrita} está validado.")["resultado"] == "BLOQUEO"


@pytest.mark.parametrize("no_ficha", ["OPP-2026-0001", "CALC-2026-0001", "G3-MET-13", "Catálogo V5.0", "PB-47", "2026.001"])
def test_lo_que_no_es_una_ficha(no_ficha):
    assert ht09.fichas_de(servicio.FICHAS_CATALOGO).buscar(ht09.normalizar(f"Ver {no_ficha} validado.")) == []


def test_una_ficha_desconocida_con_cuatro_cifras_o_prefijo_conocido_es_una_ficha_inventada():
    for t in ("ST-DESC-1001 calcula el percentil.", "ML-SUPER-001 agrupa.", "ml_super_001 agrupa.", "ML.SUPER.001 agrupa."):
        c = _real(t)
        assert c["resultado"] == "BLOQUEO" and "sin ficha en el Catálogo" in c["incidencias"][0]["detalle"], t


@pytest.mark.parametrize("ficha_ambigua", ["CARRY-001", "MOM-001", "VAR-001"])
def test_una_parcial_ambigua_falla_cerrado(ficha_ambigua):
    """«CARRY-001» puede ser FX-CARRY-001 o FIR-CARRY-001: no se reconoce con seguridad y la regla B la bloquea."""
    c = _real(f"La señal sale de {ficha_ambigua}.")
    assert c["resultado"] == "BLOQUEO" and "no se puede reconocer con seguridad" in c["incidencias"][0]["detalle"]


def test_coste_lineal_en_una_frase_larga_y_en_muchas_fichas_por_parrafo():
    """Tiempo de CPU del proceso (como T-168): 8 veces más texto, como mucho 12 veces más tiempo (×1,5 de lo lineal, el
    margen relativo que tenía el tope de 6 con ×4). Un coste lineal + cuadrático (b·n + a·n²) falla en cuanto el término
    cuadrático, al tamaño largo, pasa de 0,62 veces el lineal (con ×4 y tope 6 era 0,8).
    T-199 r02 (QA r01, H-01): la mínima de tres medidas intercaladas de cada tamaño, sin el recolector (`tiempo_cpu`); con una
    sola medida de ×4 y tope 6, la razón llegaba a 5,97 con la máquina cargada (lineal: 4)."""
    _real("ST-DESC-001")
    for unidad in ("no está validado, ", "ST-DESC-001 implementado. ", "VOL GARCH 001 y ST-DESC-001; "):
        corto, largo = minimos_intercalados(lambda u=unidad: _real(u * 1000), lambda u=unidad: _real(u * 8000))
        assert largo < 12 * max(corto, 0.02), (unidad, corto, largo)


# ------------------------------------------------------------------ HTML (H-11)
@pytest.mark.parametrize("html", ['<span title="VOL-GARCH-001 validado">Volatilidad del 18 %</span>',
                                  "<p>VOL-GARCH-001 está <b>vali</b>dado</p>", "<p>VOL-GARCH-001 está vali&shy;dado</p>",
                                  "<p>VOL-GARCH-001<br>validado</p>", "<p>VOL-GARCH-001 est&#225; &#118;alidado</p>",
                                  "<h3>ST-DESC-001</h3><p>Percentil del precio.</p><p>Está validado.</p>",
                                  "<table><tr><th></th><th>ST-DESC-001</th></tr><tr><td>Madurez</td><td>validado</td></tr></table>"])
def test_html(html):
    assert _real(ht09.texto_html(html))["resultado"] == "BLOQUEO"


def test_html_sin_madurez_no_salta_y_con_ella_en_cualquier_parte_bloquea():
    assert _comp(ht09.texto_html("<p>Percentil (ST-DESC-001)</p><p>El plan lo aprobó el operador &amp; el Broker</p>"))["resultado"] == "OK"
    # falso positivo aceptado (falla cerrado): «validado por el operador» en un visual que nombra una ficha
    t = ht09.texto_html("<p>Percentil (ST-DESC-001)</p><p>El plan fue validado por el operador &amp; el Broker</p>")
    assert _comp(t)["resultado"] == "BLOQUEO"


# ------------------------------------------------------------------ el ámbito: el registro o el documento (H-02, H-08, H-17, H-23)
@pytest.mark.parametrize("texto", [
    "La volatilidad sale de VOL-GARCH-001.\n\nEstá validado.",                                       # otro párrafo
    "## ST-DESC-001\n\nMide la posición del precio en su rango.\n\nEstá validado en la muestra.",     # dos párrafos tras el título
    "| | ST-DESC-001 | VOL-GARCH-001 |\n|---|---|---|\n| Estado | validado | validado |",             # tabla transpuesta
    "| ST-DESC-001 | implementado |\n\nEste resultado está validado.",                               # después de una tabla
    "ST-DESC-001 está validado: no hay dudas.",                                                    # H-14
    "ST-DESC-001 completó con éxito la validación fuera de muestra.",                              # H-15
    "ST-DESC-001, indicador de tendencia validado en backtest.",                                    # H-13
    "Hoy, más que nunca, ST-DESC-001 está validado.", "ST-DESC-001 se validaba cada trimestre.",     # H-26
])
def test_en_el_mismo_texto_la_palabra_cuenta_en_todo_el(texto):
    assert _real(texto)["resultado"] == "BLOQUEO", texto


def test_h17_otro_campo_de_la_misma_opcion_bloquea_esa_opcion_y_no_las_demas():
    paquete = {"clases": {"RV": {"opciones": [
        {"opp_id": "OPP-2026-0001", "valoracion": "Precio en el percentil 96 % (ST-DESC-001).", "mecanismo": "Está validado."},
        {"opp_id": "OPP-2026-0002", "valoracion": "Precio en el percentil 50 % (ST-DESC-001).", "mecanismo": "Impulso."}]}},
        "limitaciones": ["ninguna"]}
    c = sint.g3_met13(BLOQUE_REAL, paquete, {}, None)
    assert [i["ruta"] for i in c["incidencias"]] == ["paquete.clases.RV.opciones[OPP-2026-0001].mecanismo"]
    # fuera de una opción, el ámbito es el paquete: una palabra en las limitaciones y una ficha en otro campo del paquete
    paquete["clases"]["RV"]["opciones"][0]["mecanismo"] = "Impulso."
    paquete["limitaciones"] = ["Todo validado."]
    paquete["clusteres_exposicion"] = [{"factor_dominante": "Correlación semanal (ML-CLUS-001)", "opp_ids": []}]
    c = sint.g3_met13(BLOQUE_REAL, paquete, {}, None)
    assert [(i["ruta"], i["severidad"]) for i in c["incidencias"]] == [("paquete.limitaciones[0]", "BLOQUEO")]


def test_el_tecnico_es_un_ambito_y_la_ruta_es_la_linea_del_parrafo(monkeypatch):
    """X07 (QA r02): la ruta de una incidencia del técnico es la línea en que empieza su párrafo; el ámbito es todo el técnico."""
    res = {"dictamen": "APTO", "motivo": "", "resumen": {"ok": 0, "advertencias": 0, "bloqueos": 0},
           "comprobaciones": [{"id": "G3-MET-13", "nombre": ht09.NOMBRE_MET13, "resultado": "OK", "incidencias": [], "datos": {}}]}
    assert sint.g3_met13_tecnico(BLOQUE_REAL, res, "# T\n\nLa volatilidad sale de VOL-GARCH-001.\nEs un resultado validado.\n")
    assert [i["ruta"] for i in res["comprobaciones"][0]["incidencias"]] == ["informe_tecnico, línea 3"]
    assert res["dictamen"] == "BLOQUEADO"
    res["comprobaciones"][0].update(resultado="OK", incidencias=[])
    assert sint.g3_met13_tecnico(BLOQUE_REAL, res, "VOL-GARCH-001 en la tabla.\n\nOtro.\n\n## 7\n\nEstá validado.\n")
    assert [i["ruta"] for i in res["comprobaciones"][0]["incidencias"]] == ["informe_tecnico, línea 7"]


def test_ambito_de():
    assert ht09.ambito_de("paquete.clases.RV.opciones[OPP-2026-0001].horizontes.H1.metodo") == \
        "paquete.clases.RV.opciones[OPP-2026-0001]"
    assert ht09.ambito_de("informes_clase.RV.no_entregada[SPY].tesis") == "informes_clase.RV.no_entregada[SPY]"
    assert ht09.ambito_de("paquete.limitaciones[3]") == "paquete"
    assert ht09.ambito_de("informe_tecnico, línea 12") == "informe_tecnico" and ht09.ambito_de("r") == "r"


# ------------------------------------------------------------------ JSON: las claves cuentan y los campos de madurez son del ejecutor
def test_textos_de_lleva_el_opp_en_la_ruta_y_la_clave_en_el_texto():
    obj = {"clases": {"RV": {"opciones": [{"opp_id": "OPP-2026-0004", "mecanismo": "x", "calculos": ["CALC-1"]}]}}}
    t = dict(ht09.textos_de(obj, "paquete"))
    assert t["paquete.clases.RV.opciones[OPP-2026-0004].mecanismo"] == "clases · RV · opciones · mecanismo: x"
    assert t["paquete.clases.RV.opciones[OPP-2026-0004].calculos[0]"] == "clases · RV · opciones · calculos: CALC-1"


@pytest.mark.parametrize("obj", [
    {"metodo": "VOL-GARCH-001", "validado": True}, {"ficha": "ST-DESC-001", "validado": "sí"},
    {"ficha": "ST-DESC-001", "is_validated": 1}, {"ficha": "ST-DESC-001", "validated": "yes"},
    {"ficha": "ST-DESC-001", "nivel_madurez": "3"}, {"metodo": "VOL-GARCH-001", "nivel_madurez": 3},
    {"ficha": "ST-DESC-001", "madurez": {"nivel": "VALIDADO"}}, {"calculo": {"ficha": "ST-DESC-001"}, "madurez": "validado"},
    {"metodos": [{"id": "ST-DESC-001"}], "estado": "validado"}, {"VOL-GARCH-001": {"estado": "validado"}},
    {"estado_madurez_metodos": {"VOL-GARCH-001": "validado"}}, {"estado_madurez_metodos": ["VOL-GARCH-001", "validado"]},
    {"estado_madurez_metodos": "ST-DESC-001: implementado"},                      # el valor del modelo no vale: solo el canónico
    {"estado_madurez_metodos": "ST-DESC-001 [madurez: VALIDADO]"},               # canónico de forma, falso
    {"metodo_principal": "ST-DESC-001", "justificacion": "Resultado validado."},  # H-17 en un registro
    {"ficha": "ST-DESC-001", "validacion": "superada"},
])
def test_json_bloquea(obj):
    assert _json_real(obj)["resultado"] == "BLOQUEO", obj


@pytest.mark.parametrize("obj", [
    {"estado_madurez_metodos": "ST-DESC-001 [madurez: IMPLEMENTADO]; RISK-DD-001 [madurez: IMPLEMENTADO]"},
    {"estado_madurez_metodos": ht09.SIN_FICHAS},
    {"metodo": "ST-DESC-001", "invalidacion": ["cierre bajo la media"]},
])
def test_json_canonico_no_salta(obj):
    assert _json_real(obj)["resultado"] == "OK", obj


def test_canonizar_madurez_escribe_el_campo_de_madurez_de_los_informes_de_clase(monkeypatch):
    monkeypatch.setattr(servicio, "madurez_catalogo", lambda raiz=None: dict(MADUREZ))
    seleccion = {"RV": {"candidatos": [
        {"opp_id": "OPP-2026-0001", "valoracion": "Percentil (ST-DESC-001).", "estado_madurez_metodos": "FON-DISC-001: documentado, no validado"},
        {"opp_id": "OPP-2026-0002", "valoracion": "Sin cálculo.", "x": {"madurez": True}}]}}
    sint.canonizar_madurez(BLOQUE_REAL, seleccion)
    a, b = seleccion["RV"]["candidatos"]
    assert a["estado_madurez_metodos"] == "ST-DESC-001 [madurez: IMPLEMENTADO]" and b["x"]["madurez"] == ht09.SIN_FICHAS
    c = sint.g3_met13(BLOQUE_REAL, {"clases": {}}, {"seleccion": seleccion}, None)
    assert c["resultado"] == "OK", c


# ------------------------------------------------------------------ la forma canónica que escribe el ejecutor
def test_anotar_madurez():
    t = "Percentil (ST-DESC-001); clústeres de ML-CLUS-001; ya anotada ST-DESC-001 [madurez: IMPLEMENTADO]; OPP-2026-0001."
    a = ht09.anotar_madurez(t, MADUREZ, _sirve, MADUREZ)
    assert a == ("Percentil (ST-DESC-001 [madurez: IMPLEMENTADO]); clústeres de ML-CLUS-001 [madurez: DOCUMENTADO; no la sirve "
                 "el Motor]; ya anotada ST-DESC-001 [madurez: IMPLEMENTADO]; OPP-2026-0001.")
    assert ht09.anotar_madurez(a, MADUREZ, _sirve, MADUREZ) == a                       # idempotente
    assert _comp(a)["resultado"] == "OK"                                                # y G3-MET-13 la da por buena
    assert ht09.resumen_madurez(["ST-DESC-001", "ML-CLUS-001"], MADUREZ, _sirve) == \
        "ML-CLUS-001 [madurez: DOCUMENTADO; no la sirve el Motor]; ST-DESC-001 [madurez: IMPLEMENTADO]"


def test_anotar_json_no_toca_un_identificador_ni_las_claves():
    js = {"metodo": "ST-DESC-001", "ST-DESC-001": "Percentil (ST-DESC-001).", "n": 3}
    assert sint.anotar_json(BLOQUE_REAL, js) == {"metodo": "ST-DESC-001", "ST-DESC-001": "Percentil (ST-DESC-001 [madurez: "
                                                 "IMPLEMENTADO]).", "n": 3}


def test_los_textos_del_ejecutor_no_dicen_validacion():
    """La retirada de F6 y el respaldo de la integración V6 no usan la raíz «valid-» (bloquearían el paquete en su ámbito)."""
    import inspect

    from bloque_a import diseno_v6
    assert "validación G3" not in inspect.getsource(sint.retirar_opciones)
    assert "paquete validado" not in inspect.getsource(diseno_v6.integracion_determinista)


# ------------------------------------------------------------------ sintesis.g3_met13: dónde se localiza
def test_g3_met13_localiza_en_la_opcion_y_advierte_de_lo_que_no_se_entrega(monkeypatch):
    monkeypatch.setattr(servicio, "madurez_catalogo", lambda raiz=None: dict(MADUREZ))
    bloque = SimpleNamespace(motor=SimpleNamespace(raiz=None))
    frase = "Calculado con ML-CLUS-001, un método validado."
    paquete = {"clases": {"RV": {"opciones": [{"opp_id": "OPP-2026-0001", "mecanismo": "Persistencia del impulso."}]}},
               "limitaciones": ["ninguna"]}
    extras = {"seleccion": {"RV": {"candidatos": [{"opp_id": "OPP-2026-0001", "proxy": "AAA", "mecanismo": frase},
                                                  {"opp_id": "OPP-2026-0002", "proxy": "BBB", "valoracion": frase}]}},
              "analisis": {"RV": {"regimen": "Régimen alcista; ST-DESC-001 está validado.", "lagunas": []}}}
    c = sint.g3_met13(bloque, paquete, extras, None)
    por_ruta = {i["ruta"]: i["severidad"] for i in c["incidencias"]}
    assert por_ruta == {"informes_clase.RV[OPP-2026-0001].mecanismo": "BLOQUEO",
                        "informes_clase.RV.no_entregada[BBB].valoracion": "ADVERTENCIA",
                        "informes_clase.RV.regimen": "ADVERTENCIA"}
    assert c["resultado"] == "BLOQUEO"
    # Sin la candidata que es opción, solo quedan advertencias (lo que no llega a la entrega)
    extras["seleccion"]["RV"]["candidatos"].pop(0)
    assert sint.g3_met13(bloque, paquete, extras, None)["resultado"] == "ADVERTENCIA"
    # Y un paquete que lo dice fuera de una opción bloquea sin OPP- (todo el run)
    paquete["limitaciones"] = [frase]
    c = sint.g3_met13(bloque, paquete, {}, None)
    assert {(i["ruta"], i["severidad"]) for i in c["incidencias"]} == {("paquete.limitaciones[0]", "BLOQUEO")}


def test_g3_met13_visual_ilegible_falla_cerrado(monkeypatch, tmp_path):
    bloque = SimpleNamespace(motor=SimpleNamespace(raiz=None))
    c = sint.g3_met13(bloque, {"clases": {}}, {}, str(tmp_path / "no_existe.html"))
    assert c["resultado"] == "BLOQUEO" and c["incidencias"][0]["ruta"] == "informe_visual"


def test_recalcular_dictamen_y_motivo_como_la_referencia():
    res = {"dictamen": "APTO", "motivo": "Todas las comprobaciones superadas", "resumen": {"ok": 1, "advertencias": 0, "bloqueos": 0},
           "comprobaciones": [{"id": "C01", "nombre": "Campos", "resultado": "OK", "incidencias": []},
                              {"id": "G3-MET-13", "nombre": ht09.NOMBRE_MET13, "resultado": "ADVERTENCIA", "incidencias": [{}]}]}
    sint._recalcular(res)
    assert res["dictamen"] == "APTO_CON_ADVERTENCIAS" and res["motivo"] == f"G3-MET-13 {ht09.NOMBRE_MET13}"
    res["comprobaciones"][1]["resultado"] = "BLOQUEO"
    sint._recalcular(res)
    assert res["dictamen"] == "BLOQUEADO" and res["resumen"] == {"ok": 1, "advertencias": 0, "bloqueos": 1}


# ------------------------------------------------------------------ de extremo a extremo (cliente simulado)
FRASE = "Los clústeres de exposición se calculan con ML-CLUS-001, un método validado."


def _g3v(b, run_id, fase="F6"):
    return [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "G3V" and e["run_id"] == run_id and e.get("fase") == fase]


def _met13(g3v):
    return next(c for c in g3v["comprobaciones"] if c["id"] == "G3-MET-13")


def _sembrar(monkeypatch, frase):
    original = mock_respuestas._ficha
    sembradas = []

    def ficha(u, msg, ctx, rng, inyectado):
        f = original(u, msg, ctx, rng, inyectado)
        f["mecanismo"] = f"{f['mecanismo']} {frase}"
        sembradas.append(u["simbolo"])
        return f
    monkeypatch.setattr(mock_respuestas, "_ficha", ficha)
    return sembradas


def test_pb47_informe_de_clase_que_llama_validado_a_un_metodo_documentado_bloquea_g3(tmp_path, universo, monkeypatch):
    """PB-47 con su preparación completa: ML-CLUS-001 en DOCUMENTADO y un informe de clase que lo llama «validado». HT-09
    (G3-MET-13) bloquea; las opciones que lo afirman se retiran (CT-14) y el entregable final no lo presenta como validado ni
    usa el método."""
    _documentado(monkeypatch)
    sembradas = _sembrar(monkeypatch, FRASE)
    monkeypatch.setattr(mock_respuestas, "_obedece_r22", lambda msg, d: d)   # r05: el Analista mantiene «validado» al reescribir
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV", "RF"]})
    assert sembradas
    f6 = _g3v(b, r["run_id"])
    assert f6[0]["dictamen_efectivo"] == "BLOQUEADO" and _met13(f6[0])["resultado"] == "BLOQUEO"
    assert any("«validado» para ML-CLUS-001" in d and "«DOCUMENTADO»" in d for d in _met13(f6[0])["detalle"])
    ct14 = [m for m in b.mensajeria.registro if m["contrato"] == "CT-14"]           # al Orquestador, que no lo da por bueno
    assert ct14 and ct14[0]["emisor"] == "AG-02" and ct14[0]["receptor"] == "AG-18"
    assert f6[0]["excepcion"]["dictamen_orquestador"] == "BLOQUEADO"
    assert len(f6) == 2 and f6[1]["dictamen_efectivo"] != "BLOQUEADO"              # la corrección: se retiran las afectadas
    assert all(not d["opciones"] for d in r["paquete"]["clases"].values())       # todas lo afirmaban
    assert any("Opciones retiradas por bloqueo G3" in x for x in r["paquete"]["limitaciones"])
    entregados = {k: Path(v).read_text(encoding="utf-8") for k, v in (r.get("entregables") or {}).items()}
    assert entregados and not [k for k, t in entregados.items() if "validado" in t.lower()]
    js = json.loads(entregados["paquete_json"])
    servidos = {e["calc_id"]: e for e in b.almacen.leer("RC") if e.get("estado") in ("SERVED", "SERVED_WITH_LIMITATIONS")}
    citados = {c for d in js["clases"].values() for o in d["opciones"] for c in o["calculos"]}
    assert all(servidos[c]["operacion"]["ficha_id"] != "ML-CLUS-001" for c in citados)


def test_pb47_corregida_la_declaracion_con_la_forma_canonica_la_entrega_pasa(tmp_path, universo, monkeypatch):
    """«BLOQUEADO hasta corregir la declaración»: el mismo informe de clase, con la ficha en su forma canónica (la madurez del
    Catálogo y que el Motor no la sirve), pasa G3 y se entrega. Desde la r03 la declaración en prosa («documentado y no se
    sirve») no basta: la única declaración que se acepta es la canónica (INC-T165-01)."""
    _documentado(monkeypatch)
    _sembrar(monkeypatch, "Los clústeres de exposición usarían ML-CLUS-001 [madurez: DOCUMENTADO; no la sirve el Motor].")
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV", "RF"]})
    f6, f7 = _g3v(b, r["run_id"]), _g3v(b, r["run_id"], "F7")
    assert len(f6) == 1 and f6[0]["dictamen_efectivo"] == "APTO" and _met13(f6[0])["resultado"] == "OK"
    assert f7 and f7[0]["dictamen_efectivo"] == "APTO" and _met13(f7[0])["resultado"] == "OK"
    assert r["entregables"] and r.get("entrega") != "BLOQUEADA"
    assert all(d["opciones"] for d in r["paquete"]["clases"].values())
    tecnico = Path(r["entregables"]["informe_tecnico"]).read_text(encoding="utf-8")
    assert "ML-CLUS-001 [madurez: DOCUMENTADO; no la sirve el Motor]" in tecnico and "N efectivo ML-CLUS-001" not in tecnico
    # la declaración en prosa del modelo ya no basta
    assert _pb47_prosa(monkeypatch) == "BLOQUEO"


def _pb47_prosa(monkeypatch):
    return _real("Los clústeres de exposición usarían ML-CLUS-001, que está documentado y no se sirve.")["resultado"]


def test_un_metodo_no_servido_solo_en_el_tecnico_bloquea_la_entrega_en_f7(tmp_path, universo, monkeypatch):
    original = Redaccion.tecnico

    def tecnico(self, *a, **k):
        return original(self, *a, **k) + "\nLa volatilidad sale de ML-SUPER-001.\n"
    monkeypatch.setattr(Redaccion, "tecnico", tecnico)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert r.get("entrega") == "BLOQUEADA" and "G3-MET-13" in r["g3_entregables"]["bloqueos"]
    (f7,) = _g3v(b, r["run_id"], "F7")
    assert f7["dictamen_efectivo"] == "BLOQUEADO" and f7["dictamen_ht09"] == "BLOQUEADO"
    assert _met13(f7)["resultado"] == "BLOQUEO" and any("ML-SUPER-001" in d for d in _met13(f7)["detalle"])
    assert all("_bloqueados" in v for v in r["entregables"].values())
    assert not [e for e in b.almacen.leer("F4") if e.get("tipo_entrada") == "ALTA"]   # nada se congela


def test_una_ficha_no_servida_que_el_modelo_pone_en_el_tecnico_se_lee_antes_de_anotar(tmp_path, universo, monkeypatch):
    """La forma canónica la pone el ejecutor después de G3-MET-13: una ficha conocida que el Motor no sirve, escrita solo en el
    técnico sin su forma canónica, bloquea aunque el técnico entregado (anotado) la lleve."""
    _documentado(monkeypatch, "DER-OPT-001")
    original = Redaccion.tecnico

    def tecnico(self, *a, **k):
        return original(self, *a, **k) + "\nLa prima sale de DER-OPT-001.\n"
    monkeypatch.setattr(Redaccion, "tecnico", tecnico)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert r.get("entrega") == "BLOQUEADA" and "G3-MET-13" in r["g3_entregables"]["bloqueos"]


def test_un_visual_que_presenta_un_metodo_como_validado_bloquea_en_f7(tmp_path, universo, monkeypatch):
    original = Redaccion.visual

    def visual(self, *a, **k):
        return original(self, *a, **k).replace("</body>", "<p>El percentil sale de ST-DESC-001, un método validado.</p></body>")
    monkeypatch.setattr(Redaccion, "visual", visual)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    (f7,) = _g3v(b, r["run_id"], "F7")
    assert f7["dictamen_efectivo"] == "BLOQUEADO" and _met13(f7)["resultado"] == "BLOQUEO"
    assert r.get("entrega") == "BLOQUEADA" and all("_bloqueados" in v for v in r["entregables"].values())


def test_el_ciclo_simulado_normal_sigue_apto_y_lleva_la_madurez_canonica(tmp_path, universo, monkeypatch):
    """Sin falsos positivos: el ciclo normal (doce tipos) da G3 APTO en F6 y F7 con G3-MET-13 OK, y no es vacuo: la
    comprobación lee menciones de fichas servidas. Los tres entregables llevan la madurez canónica junto a cada ficha, el técnico
    su declaración R22 y el JSON `x_madurez_metodos`, todo escrito por el ejecutor desde el Catálogo."""
    vistos = []
    original = ht09.comprobar_madurez

    def espia(*a, **k):
        c = original(*a, **k)
        vistos.append(c)
        return c
    monkeypatch.setattr(ht09, "comprobar_madurez", espia)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF)
    f6, f7 = _g3v(b, r["run_id"]), _g3v(b, r["run_id"], "F7")
    assert [e["dictamen_efectivo"] for e in f6 + f7] == ["APTO", "APTO"]
    assert all(_met13(e)["resultado"] == "OK" for e in f6 + f7)
    assert r["entregables"] and r.get("entrega") != "BLOQUEADA"
    citadas = {f for c in vistos for f in c["datos"]["fichas_citadas"]}
    assert {"ST-DESC-001", "RISK-DD-001", "ML-CLUS-001"} <= citadas and all(c["resultado"] == "OK" for c in vistos)
    tecnico = Path(r["entregables"]["informe_tecnico"]).read_text(encoding="utf-8")
    assert "N efectivo ML-CLUS-001 [madurez: IMPLEMENTADO]" in tecnico and "(ST-DESC-001 [madurez: IMPLEMENTADO])" in tecnico
    assert "- Madurez de los métodos citados (R22; la escribe el ejecutor desde el Catálogo): ML-CLUS-001 [madurez: IMPLEMENTADO]" in tecnico
    assert not re.search(r"[A-Z]+-[A-Z]+-\d{3}(?! \[madurez: )", tecnico)                # ninguna ficha sin su madurez
    js = json.loads(Path(r["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
    assert js["x_madurez_metodos"]["ST-DESC-001"] == "IMPLEMENTADO" and "valid" not in json.dumps(js).replace("invalid", "")


def test_la_limitacion_sin_historia_y_la_de_los_clusteres_no_nombran_ml_clus_sin_su_forma_canonica(tmp_path, universo, monkeypatch):
    _documentado(monkeypatch)
    from bloque_a.orquestacion import Bloque
    original = Bloque._clusteres

    def con_una_corta(self, analisis, as_of, run_id):
        out = original(self, analisis, as_of, run_id)
        assert out.get("rechazo")      # ML-CLUS-001 en DOCUMENTADO
        out["sin_historia"] = sorted(out["asignacion"])[:1]
        return out
    monkeypatch.setattr(Bloque, "_clusteres", con_una_corta)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    lim = r["paquete"]["limitaciones"]
    assert any("el resto tampoco se agrupa (el Motor no sirvió los clústeres)" in x for x in lim)
    assert "clústeres de exposición no calculados (el Motor no sirve ML-CLUS-001 [madurez: DOCUMENTADO; no la sirve el Motor])" \
        ": la concentración entre opciones no se ha podido medir en este ciclo" in lim
    assert r["entregables"] and r.get("entrega") != "BLOQUEADA"


# ------------------------------------------------------------------ r02, H-06: textos del ejecutor que citan una ficha
def test_v6_con_ml_clus_documentado_se_entrega(tmp_path, universo, monkeypatch):
    _documentado(monkeypatch)
    b = nuevo_bloque(tmp_path, universo, cfg=config_pruebas(diseno="v6", auditoria={"en_backtest": True}))
    r = b.ciclo(AS_OF, alcance={"clases": ["RV", "RF"]})
    assert r["entregables"] and r.get("entrega") != "BLOQUEADA"
    js = json.loads(Path(r["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
    assert js["clusteres_exposicion"] and all("ML-CLUS-001" not in e["factor_dominante"] for e in js["clusteres_exposicion"])
    assert all(_met13(e)["resultado"] == "OK" for e in _g3v(b, r["run_id"]) + _g3v(b, r["run_id"], "F7"))


def test_el_riesgo_sin_calculo_del_motor_no_cita_risk_dd(tmp_path, universo, monkeypatch):
    """Con RISK-DD-001 en DOCUMENTADO ninguna opción pasa PS4 (exige el riesgo 1–5), así que el rótulo no llega a escribirse sin el
    cálculo; el ciclo se entrega sin bloqueo de G3-MET-13 (la laguna nombra la ficha con su forma canónica). El rótulo es
    condicional igualmente."""
    from bloque_a.redaccion import _fuente_riesgo
    assert _fuente_riesgo({"riesgo_sin_motor": {"OPP-2026-0001"}}, {"opp_id": "OPP-2026-0001"}) == \
        "valor neutro: sin cálculo del Motor en este ciclo"
    assert _fuente_riesgo({"riesgo_sin_motor": set()}, {"opp_id": "OPP-2026-0001"}) == "RISK-DD-001"
    _documentado(monkeypatch, "RISK-DD-001")
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert r["entregables"] and r.get("entrega") != "BLOQUEADA"
    assert all(_met13(e)["resultado"] == "OK" for e in _g3v(b, r["run_id"]) + _g3v(b, r["run_id"], "F7"))
    tecnico = Path(r["entregables"]["informe_tecnico"]).read_text(encoding="utf-8")
    assert "/5** (RISK-DD-001" not in tecnico and "RISK-DD-001 [madurez: DOCUMENTADO; no la sirve el Motor]" in tecnico


def test_el_campo_de_madurez_que_pide_el_prompt_lo_reescribe_el_ejecutor_y_no_retira_la_opcion(tmp_path, universo, monkeypatch):
    """El Analista escribe `estado_madurez_metodos` como le pide su prompt («…: implementado, no validado»): el ejecutor lo
    reescribe en forma canónica al construir el paquete, así que ni bloquea ni llega lo que dijo el modelo."""
    original = mock_respuestas._ficha
    vistas = []

    def ficha(u, msg, ctx, rng, inyectado):
        f = original(u, msg, ctx, rng, inyectado)
        f["estado_madurez_metodos"] = "ST-DESC-001: implementado, no validado"
        vistas.append(f)
        return f
    monkeypatch.setattr(mock_respuestas, "_ficha", ficha)
    leidas = []
    g3_original = sint.g3_met13

    def espia(bloque, paquete, extras, visual):
        leidas.extend(f.get("estado_madurez_metodos") for s in (extras.get("seleccion") or {}).values()
                      for f in s.get("candidatos", []))
        return g3_original(bloque, paquete, extras, visual)
    monkeypatch.setattr(sint, "g3_met13", espia)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert vistas and r["paquete"]["clases"]["RV"]["opciones"] and r.get("entrega") != "BLOQUEADA"
    assert all(_met13(e)["resultado"] == "OK" for e in _g3v(b, r["run_id"]) + _g3v(b, r["run_id"], "F7"))
    assert leidas and set(leidas) == {"ACC-MOM-001 [madurez: IMPLEMENTADO]; ST-DESC-001 [madurez: IMPLEMENTADO]"}   # las que cita la candidata


# ================================================================== r04 (QA r03: H-28 a H-32)
def _llamadas(monkeypatch):
    from bloque_a.orquestacion import Bloque
    vistas = []
    original = Bloque._invocar

    def espia(self, agente, contrato, mensaje, esquema, instrucciones, *a, **k):
        vistas.append((agente, bool(isinstance(mensaje, dict) and mensaje.get("reescritura")), instrucciones))
        return original(self, agente, contrato, mensaje, esquema, instrucciones, *a, **k)
    monkeypatch.setattr(Bloque, "_invocar", espia)
    return vistas


def test_h28_la_regla_r22_va_en_las_instrucciones_de_los_que_redactan():
    from bloque_a.orquestacion import INSTR

    from bloque_a import diseno_v6
    regla = ht09.REGLA_R22_REDACCION
    assert all(v.endswith(regla) for v in INSTR.values()) and set(INSTR) >= {"CRIBADO_E_INVESTIGACION", "RESPUESTA_OBJECIONES"}
    assert diseno_v6.INSTR_SINTESIS.endswith(regla) and diseno_v6.INSTR_PROSPECTIVA.endswith(regla)
    for t in (diseno_v6.INSTR_SINTESIS.replace(regla, ""), diseno_v6._SIN_SINTESIS):   # el texto del ejecutor, sin la raíz
        assert not ht09.tiene_raiz_valid(t), t
    assert "ya revisado por G3" in diseno_v6.INSTR_SINTESIS and "calculadas y revisadas" in diseno_v6.INSTR_SINTESIS
    for f in ("orquestacion.py", "diseno_v6.py"):   # la integración, el Redactor y la Prospectiva V5 también la llevan
        assert (Path(sint.__file__).parent / f).read_text(encoding="utf-8").count("ht09.REGLA_R22_REDACCION") >= 2


def test_h28_la_declaracion_r22_del_analizador_se_reescribe_y_el_ciclo_entrega(tmp_path, universo, monkeypatch):
    """El simulado escribe en la integración la declaración R22 que pide el prompt del Analizador, con la raíz: el ejecutor pide
    una reescritura con su regla y el ciclo entrega sin perder opciones; en el paquete queda la reescrita."""
    vistas = _llamadas(monkeypatch)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV", "RF"]})
    integ = [x for x in vistas if x[0] == "AG-02" and "Integra" in x[2]]
    assert [x[1] for x in integ] == [False, True] and integ[1][2].endswith(f"Reescribe: {ht09.REGLA_R22_REDACCION}")
    assert r["entregables"] and r.get("entrega") != "BLOQUEADA" and all(d["opciones"] for d in r["paquete"]["clases"].values())
    assert all(_met13(e)["resultado"] == "OK" for e in _g3v(b, r["run_id"]) + _g3v(b, r["run_id"], "F7"))
    assert "Métodos usados (R22): su madurez la escribe el ejecutor junto a cada ficha." in r["paquete"]["limitaciones"]
    assert not any(ht09.tiene_raiz_valid(x) for x in r["paquete"]["limitaciones"])
    rc = b.almacen.leer("RC")    # el Motor tampoco escribe la raíz en RC
    assert rc and not any(ht09.tiene_raiz_valid(e.get("limitaciones")) for e in rc)


def test_h28_si_la_raiz_persiste_tras_la_reescritura_el_run_se_bloquea(tmp_path, universo, monkeypatch):
    original = mock_respuestas._integracion

    def integ(msg, ctx, rng):
        return {**original(msg, ctx, rng), "lectura_conjunto": "Métodos usados (R22): implementados y aún no validados."}
    monkeypatch.setattr(mock_respuestas, "_integracion", integ)
    monkeypatch.setattr(mock_respuestas, "_obedece_r22", lambda msg, d: d)   # un modelo que no sigue la regla
    vistas = _llamadas(monkeypatch)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert [x[1] for x in vistas if x[0] == "AG-02" and "Integra" in x[2]] == [False, True]   # una sola reescritura (config)
    f6 = _g3v(b, r["run_id"])
    assert f6[0]["dictamen_efectivo"] == "BLOQUEADO" and _met13(f6[0])["resultado"] == "BLOQUEO" and r.get("entrega") == "BLOQUEADA"


@pytest.mark.parametrize("diseno", ["v5", "v6"])
def test_h28_el_redactor_y_el_sintetizador_se_reescriben(diseno, tmp_path, universo, monkeypatch):
    """El Redactor (V5) o el Sintetizador (V6) repiten la instrucción antigua («sobre el paquete ya validado»): una reescritura y
    el ciclo entrega. El texto entra en el visual, que es un solo ámbito."""
    nombre = "_redactor" if diseno == "v5" else "_sintetizador"
    original = getattr(mock_respuestas, nombre)

    def redactor(msg, ctx, rng):
        d = original(msg, ctx, rng)
        if not msg.get("reescritura"):
            d["frase_historial"] = "Sobre el paquete ya validado, con pocos casos la diferencia puede ser suerte."
        return d
    monkeypatch.setattr(mock_respuestas, nombre, redactor)
    vistas = _llamadas(monkeypatch)
    cfg = config_pruebas(diseno="v6", auditoria={"en_backtest": True}) if diseno == "v6" else None
    b = nuevo_bloque(tmp_path, universo, cfg=cfg) if cfg else nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    agente = "AG-17" if diseno == "v5" else "AG-26"
    assert [x[1] for x in vistas if x[0] == agente] == [False, True]
    assert r["entregables"] and r.get("entrega") != "BLOQUEADA"
    assert all(_met13(e)["resultado"] == "OK" for e in _g3v(b, r["run_id"]) + _g3v(b, r["run_id"], "F7"))


def test_h35_una_laguna_del_analista_con_la_raiz_llega_con_la_palabra_cambiada():
    assert sint._laguna_r22("datos HT-01 sin huecos") == "datos HT-01 sin huecos"
    assert sint._laguna_r22("Validación pendiente de la batería mínima") == \
        "comprobar pendiente de la batería mínima (redacción ajustada por R22)"
    assert sint._laguna_r22("No se pudo validar el dato de flujos") == "No se pudo comprobar el dato de flujos (redacción ajustada por R22)"
    # si la raíz persiste en otra grafía (homoglifo), se omite y se dice
    assert sint._laguna_r22("v\u0430lidación pendiente").startswith("laguna del Analista omitida")


def test_h29_una_carpeta_de_salida_con_la_raiz_no_bloquea(tmp_path, universo):
    b = nuevo_bloque(tmp_path / "validaciones", universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert r["entregables"] and r.get("entrega") != "BLOQUEADA" and "validaciones" in r["entregables"]["informe_tecnico"]
    assert all(_met13(e)["resultado"] == "OK" for e in _g3v(b, r["run_id"], "F7"))


@pytest.mark.parametrize("texto", ["ST-DESC-001 es un método válido fuera de muestra.", "La estrategia de ST-DESC-001 es válida.",
                                   "ST-DESC-001: MÉTODO VÁLIDO.", "La metodología de selección está validada.",
                                   "Señal compuesta validada fuera de la muestra.", "Nuestro sistema de selección está validado."])
def test_h30_h32_la_tilde_y_los_sustantivos_que_faltaban(texto):
    assert _real(texto)["resultado"] == "BLOQUEO", texto


def test_h30_inválido_no_es_la_raiz():
    assert _real("Dato inválido del proveedor en ST-DESC-001: se excluye.")["resultado"] == "OK"


def test_h31_un_campo_con_maxlength_no_se_anota_y_el_esquema_sigue_valido(tmp_path, universo, monkeypatch):
    original = mock_respuestas._ficha

    def ficha(u, msg, ctx, rng, inyectado):
        return {**original(u, msg, ctx, rng, inyectado), "nombre_llano": "Bolsa tecnológica barata según ST-DESC-001 y su rango"}
    monkeypatch.setattr(mock_respuestas, "_ficha", ficha)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert r["entregables"] and r.get("entrega") != "BLOQUEADA"
    js = json.loads(Path(r["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
    o = js["clases"]["RV"]["opciones"][0]
    assert o["nombre_llano"] == "Bolsa tecnológica barata según ST-DESC-001 y su rango" and "[madurez:" in o["valoracion"]
    assert js["x_madurez_metodos"]["ST-DESC-001"] == "IMPLEMENTADO"
    assert {"nombre_llano", "por_que_llano", "que_puede_salir_mal_llano"} <= sint.claves_con_longitud_maxima(
        json.loads(b.redaccion.esquema_json.read_text(encoding="utf-8")))


def test_lo_que_el_modelo_dijo_de_la_madurez_queda_en_ha(tmp_path, universo, monkeypatch):
    original = mock_respuestas._ficha

    def ficha(u, msg, ctx, rng, inyectado):
        return {**original(u, msg, ctx, rng, inyectado), "estado_madurez_metodos": "ST-DESC-001: implementado, no validado"}
    monkeypatch.setattr(mock_respuestas, "_ficha", ficha)
    vistas = _llamadas(monkeypatch)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    (inc,) = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "INC" and "campo(s) de madurez" in e.get("detalle", "")]
    # H-38: el campo de madurez, que reescribe el ejecutor, no dispara la reescritura del informe de clase
    assert not [x for x in vistas if x[0] == "AG-03" and x[1]]
    assert inc["objeto"] == r["run_id"] and inc["madurez_del_modelo"]
    assert any("no validado" in c["texto"] for x in inc["madurez_del_modelo"] for c in x["campos"])



# ================================================================== r05 (QA r04: H-33 a H-37)
REDACTAN = {"AG-02", "AG-10", "AG-11", "AG-17", "AG-26"}


@pytest.mark.parametrize("diseno", ["v5", "v6"])
def test_h33_todas_las_instrucciones_cuyo_texto_llega_al_paquete_llevan_la_regla(diseno, tmp_path, universo, monkeypatch):
    """Recorre las llamadas de un ciclo: las de los Analistas (CT-06 y su respuesta a objeciones), la Prospectiva (CT-12), el
    Contradictor (CT-13, refutación y contrarréplica), la integración (AG-02), el Redactor (AG-17) y el Sintetizador (AG-26)."""
    from bloque_a.contratos import AGENTE_CLASE
    vistas = _llamadas(monkeypatch)
    cfg = config_pruebas(diseno="v6", auditoria={"en_backtest": True}) if diseno == "v6" else None
    b = nuevo_bloque(tmp_path, universo, cfg=cfg) if cfg else nuevo_bloque(tmp_path, universo)
    b.ciclo(AS_OF, alcance={"clases": ["RV", "RF"]})
    redactan = REDACTAN | set(AGENTE_CLASE.values())
    llamadas = [(a, i) for a, _, i in vistas if a in redactan]
    assert {a for a, _ in llamadas} >= {"AG-11", "AG-10"} | {AGENTE_CLASE["RV"]}
    assert all(ht09.REGLA_R22_REDACCION in i for _, i in llamadas), [a for a, i in llamadas if ht09.REGLA_R22_REDACCION not in i]


def _opciones(r):
    return sum(len(d["opciones"]) for d in r["paquete"]["clases"].values())


def test_h33_la_objecion_del_contradictor_con_la_raiz_se_reescribe_y_no_retira_la_opcion(tmp_path, universo, monkeypatch):
    n0 = _opciones(nuevo_bloque(tmp_path / "base", universo).ciclo(AS_OF, alcance={"clases": ["RV"]}))
    original = mock_respuestas._contrarias

    def contrarias(msg, ctx, rng):
        d = original(msg, ctx, rng)
        for x in d.get("resultados", []):
            for o in x.get("objeciones", []):
                o["que_la_resolveria"] = "Una validación fuera de muestra del impulso"
        return d
    monkeypatch.setattr(mock_respuestas, "_contrarias", contrarias)
    vistas = _llamadas(monkeypatch)
    b = nuevo_bloque(tmp_path / "fp", universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert [x[1] for x in vistas if x[0] == "AG-11" and "Refuta" in x[2]] == [False, True]
    assert _opciones(r) == n0 and r.get("entrega") != "BLOQUEADA"
    assert all(_met13(e)["resultado"] == "OK" for e in _g3v(b, r["run_id"]) + _g3v(b, r["run_id"], "F7"))


def test_h34_el_ejemplo_de_fondos_del_corpus_se_reescribe_y_no_retira_opciones(tmp_path, universo, monkeypatch):
    n0 = _opciones(nuevo_bloque(tmp_path / "base", universo).ciclo(AS_OF, alcance={"clases": ["RV"]}))
    original = mock_respuestas._ficha

    def ficha(u, msg, ctx, rng, inyectado):
        f = original(u, msg, ctx, rng, inyectado)
        f["valoracion"] += " Las recompras y ventas de activos cerca del NAV validan las valoraciones."
        return f
    monkeypatch.setattr(mock_respuestas, "_ficha", ficha)
    vistas = _llamadas(monkeypatch)
    b = nuevo_bloque(tmp_path / "fp", universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    cribado = [x[1] for x in vistas if x[0] == "AG-03" and "Fases F1" in x[2]]
    assert cribado == [False, True]
    assert _opciones(r) == n0 and r.get("entrega") != "BLOQUEADA"
    js = json.loads(Path(r["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
    assert all("comprobar las valoraciones" in o["valoracion"] for o in js["clases"]["RV"]["opciones"])


def test_h34_si_la_raiz_persiste_en_el_informe_de_clase_la_opcion_se_retira(tmp_path, universo, monkeypatch):
    original = mock_respuestas._ficha

    def ficha(u, msg, ctx, rng, inyectado):
        f = original(u, msg, ctx, rng, inyectado)
        f["valoracion"] += " Método validado."
        return f
    monkeypatch.setattr(mock_respuestas, "_ficha", ficha)
    monkeypatch.setattr(mock_respuestas, "_obedece_r22", lambda msg, d: d)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert _g3v(b, r["run_id"])[0]["dictamen_efectivo"] == "BLOQUEADO" and not r["paquete"]["clases"]["RV"]["opciones"]


@pytest.mark.parametrize("laguna, clave", [("Validación pendiente de la batería mínima del perfil FX; decláralo así (R22).",
                                            "batería mínima"),
                                           ("No se pudo validar el dato de flujos: falta la serie de posicionamiento.",
                                            "posicionamiento")])
def test_h35_la_carencia_llega_al_broker(laguna, clave, tmp_path, universo, monkeypatch):
    original = mock_respuestas._analista

    def analista(msg, ctx, rng, inyectado):
        d = original(msg, ctx, rng, inyectado)
        if msg.get("fase") == "CRIBADO_E_INVESTIGACION":
            d["estado"], d["lagunas"] = "PARCIAL", [laguna]
        return d
    monkeypatch.setattr(mock_respuestas, "_analista", analista)
    monkeypatch.setattr(mock_respuestas, "_obedece_r22", lambda msg, d: d)   # la ajusta el ejecutor, no la reescritura
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    lim = [x for x in r["paquete"]["limitaciones"] if "alcance reducido" in x]
    assert any(clave in x and "(redacción ajustada por R22)" in x for x in lim), lim
    assert r.get("entrega") != "BLOQUEADA"


def test_h36_h37_la_reescritura_repite_la_instruccion_y_lleva_las_frases(tmp_path, universo, monkeypatch):
    from bloque_a.orquestacion import Bloque
    mensajes = []
    original = Bloque._invocar

    def espia(self, agente, contrato, mensaje, esquema, instrucciones, *a, **k):
        if agente == "AG-02" and isinstance(mensaje, dict) and mensaje.get("reescritura"):
            mensajes.append((mensaje["reescritura"], instrucciones))
        return original(self, agente, contrato, mensaje, esquema, instrucciones, *a, **k)
    monkeypatch.setattr(Bloque, "_invocar", espia)
    b = nuevo_bloque(tmp_path, universo)
    b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    ((rees, instr),) = mensajes
    assert "No cambies la selección: la ha hecho HT-03" in instr and instr.endswith(f"Reescribe: {ht09.REGLA_R22_REDACCION}")
    assert rees["r22"] == ht09.REGLA_R22_REDACCION
    assert {"ruta": "limitaciones[1]", "texto": "Métodos usados (R22): implementados y aún no validados."} in rees["frases"]


def test_h37_frases_con_raiz_tiene_tope():
    d = {"a": ["validado"] * 30, "validez": "x", "b": "nada"}
    f = ht09.frases_con_raiz(d, 10)
    assert len(f) == 10 and f[0] == ("a[0]", "validado")
    assert ht09.frases_con_raiz({"b": "nada", "c": {"validez": 1}}, 10) == [("c.validez", "validez")]


@pytest.mark.parametrize("n", [0, 2])
def test_la_reescritura_sigue_la_configuracion_con_un_modelo_que_no_obedece(n, tmp_path, universo, monkeypatch):
    """Como `r04_01::test_reescritura_sigue_la_configuracion` del revisor, con el simulado sin obedecer la reescritura (desde la
    r05 la obedece por defecto): 1 + n llamadas a la integración y bloqueo."""
    original = mock_respuestas._integracion
    monkeypatch.setattr(mock_respuestas, "_integracion",
                        lambda msg, ctx, rng: {**original(msg, ctx, rng), "lectura_conjunto": "Aún no validado."})
    monkeypatch.setattr(mock_respuestas, "_obedece_r22", lambda msg, d: d)
    vistas = _llamadas(monkeypatch)
    b = nuevo_bloque(tmp_path, universo, cfg=config_pruebas(redaccion={"reescrituras_r22": n}))
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert [x[1] for x in vistas if x[0] == "AG-02" and "Integra" in x[2]] == [False] + [True] * n
    assert r.get("entrega") == "BLOQUEADA" or not r.get("entregables")


def test_el_simulado_obedece_la_reescritura():
    assert mock_respuestas._obedece_r22({"reescritura": {"r22": "x"}}, {"a": ["Validado", "inválido"], "b": 1}) == \
        {"a": ["comprobar", "inválido"], "b": 1}
    assert mock_respuestas._obedece_r22({}, {"a": "validado"}) == {"a": "validado"}


def test_h34_la_reescritura_del_informe_de_clase_y_de_la_refutacion_paga_de_la_bolsa_del_tipo(tmp_path, universo, monkeypatch):
    from bloque_a.orquestacion import Bloque
    bolsas = []
    original = Bloque._invocar

    def espia(self, agente, contrato, mensaje, esquema, instrucciones, *a, **k):
        if isinstance(mensaje, dict) and mensaje.get("reescritura") and agente in ("AG-03", "AG-11"):
            bolsas.append((agente, k.get("bolsa") or a[2] or "COMUN"))   # r06: la de la propia llamada (bolsa, o la de su clase)
        return original(self, agente, contrato, mensaje, esquema, instrucciones, *a, **k)
    monkeypatch.setattr(Bloque, "_invocar", espia)
    original_f, original_c = mock_respuestas._ficha, mock_respuestas._contrarias

    def ficha(u, msg, ctx, rng, inyectado):
        f = original_f(u, msg, ctx, rng, inyectado)
        f["valoracion"] += " Las recompras validan las valoraciones."
        return f

    def contrarias(msg, ctx, rng):
        d = original_c(msg, ctx, rng)
        for x in d.get("resultados", []):
            for o in x.get("objeciones", []):
                o["que_la_resolveria"] = "Una validación fuera de muestra"
        return d
    monkeypatch.setattr(mock_respuestas, "_ficha", ficha)
    monkeypatch.setattr(mock_respuestas, "_contrarias", contrarias)
    nuevo_bloque(tmp_path, universo).ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert ("AG-03", "RV") in bolsas and ("AG-11", "RV") in bolsas and all(b == "RV" for _, b in bolsas)


# ================================================================== r06 (QA r05: H-38 a H-40): la reescritura en `_invocar`
SIEMBRA = " Validado en backtest."


def _sembrar_en_todos(monkeypatch):
    """La raíz en la primera respuesta de cada agente cuyo texto llega al entregable: en cada texto libre (cadenas con espacios
    y de más de 25 caracteres, para no tocar valores cerrados de los esquemas). Las reescrituras no se siembran: el simulado
    obedece."""
    original = mock_respuestas.responder
    sembrados = set()

    def siembra(x):
        if isinstance(x, str):
            return x + SIEMBRA if " " in x and len(x) > 25 else x
        if isinstance(x, dict):
            return {k: siembra(v) for k, v in x.items()}
        if isinstance(x, list):
            return [siembra(v) for v in x]
        return x

    def responder(agente, mensajes, semilla):
        d = original(agente, mensajes, semilla)
        msg = mock_respuestas.extraer_encargo(mensajes[0]["content"])["mensaje"]
        if agente in ht09.AGENTES_SIN_TEXTO_ENTREGADO or (isinstance(msg, dict) and msg.get("reescritura", {}).get("r22")):
            return d
        sembrados.add(agente)
        return siembra(d)
    monkeypatch.setattr(mock_respuestas, "responder", responder)
    return sembrados


@pytest.mark.parametrize("diseno", ["v5", "v6"])
def test_h40_con_la_raiz_en_la_primera_respuesta_de_cada_agente_que_redacta_el_ciclo_entrega_sin_perder_opciones(
        diseno, tmp_path, universo, monkeypatch):
    cfg = config_pruebas(diseno="v6", auditoria={"en_backtest": True}) if diseno == "v6" else None

    def ciclo(carpeta):
        b = nuevo_bloque(carpeta, universo, cfg=cfg) if cfg else nuevo_bloque(carpeta, universo)
        return b, b.ciclo(AS_OF, alcance={"clases": ["RV", "RF"]})
    _, r0 = ciclo(tmp_path / "base")
    n0 = _opciones(r0)
    sembrados = _sembrar_en_todos(monkeypatch)
    vistas = _llamadas(monkeypatch)
    b, r = ciclo(tmp_path / "fp")
    from bloque_a.contratos import AGENTE_CLASE
    assert {"AG-10", "AG-11", AGENTE_CLASE["RV"]} <= sembrados and ({"AG-02", "AG-17"} if diseno == "v5" else {"AG-26"}) <= sembrados
    reescritos = {a for a, rees, _ in vistas if rees}
    assert sembrados <= reescritos | {"AG-01", "AG-27"}, sembrados - reescritos   # cada agente sembrado se reescribe
    # sin perder opciones por G3: un solo G3V- de F6, sin retiradas; el número puede variar (las respuestas sembradas cambian el
    # azar reproducible del simulado aguas abajo), pero no baja
    assert n0 and _opciones(r) >= n0 and r["entregables"] and r.get("entrega") != "BLOQUEADA"
    assert len(_g3v(b, r["run_id"])) == 1 and not any("retiradas por bloqueo G3" in x for x in r["paquete"]["limitaciones"])
    assert all(_met13(e)["resultado"] == "OK" for e in _g3v(b, r["run_id"]) + _g3v(b, r["run_id"], "F7"))
    incs = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "INC" and "reescrita por la raíz" in e.get("detalle", "")]
    assert incs and any(SIEMBRA.strip() in f["texto"] for e in incs for f in e["frases_r22"])   # H-39: queda en HA


def test_h40_todo_agente_que_no_esta_en_la_exclusion_pasa_por_la_reescritura(tmp_path, universo, monkeypatch):
    """`_invocar` reescribe a cualquier agente que no esté en `AGENTES_SIN_TEXTO_ENTREGADO`, también uno nuevo; a los de la
    exclusión, no. Se comprueba con una llamada directa a `_invocar` y una respuesta con la raíz."""
    from bloque_a.orquestacion import Bloque
    b = nuevo_bloque(tmp_path, universo)
    llamadas = []

    def una(self, agente, contrato, mensaje, esquema, instrucciones, *a, **k):
        llamadas.append((agente, bool(mensaje.get("reescritura")), a[2], k.get("bolsa") if k else None))
        texto = "Comprobado." if mensaje.get("reescritura") else "Validado."
        return SimpleNamespace(datos={"t": texto})
    monkeypatch.setattr(Bloque, "_invocar_una", una)
    for agente in ("AG-99", "AG-03", "AG-10", "AG-11", "AG-02", "AG-17", "AG-26", "AG-01", *sorted(ht09.AGENTES_SIN_TEXTO_ENTREGADO)):
        llamadas.clear()
        r = b._invocar(agente, "CT-XX", {"x": 1}, "ESQ", "instr", AS_OF, "RUN-1", "RV", "fase", None)
        excluido = agente in ht09.AGENTES_SIN_TEXTO_ENTREGADO
        assert [x[1] for x in llamadas] == ([False] if excluido else [False, True]), agente
        assert r.datos["t"] == ("Validado." if excluido else "Comprobado.")
        assert all(x[2] == "RV" for x in llamadas)   # la clase (y con ella la bolsa) de la propia llamada


def test_h40_no_quedan_llamadas_sueltas_a_reescribir_r22():
    for f in ("orquestacion.py", "diseno_v6.py"):
        t = (Path(sint.__file__).parent / f).read_text(encoding="utf-8")
        assert t.count("reescribir_r22(") == (2 if f == "orquestacion.py" else 0), f   # la definición y la de `_invocar`


def test_h38_los_campos_de_madurez_no_disparan_la_reescritura(tmp_path, universo, monkeypatch):
    original = mock_respuestas._ficha

    def ficha(u, msg, ctx, rng, inyectado):
        return {**original(u, msg, ctx, rng, inyectado), "estado_madurez_metodos": "ST-DESC-001: implementado, no validado"}
    monkeypatch.setattr(mock_respuestas, "_ficha", ficha)
    vistas = _llamadas(monkeypatch)
    nuevo_bloque(tmp_path, universo).ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert not [x for x in vistas if x[0] == "AG-03" and x[1]]


def test_h39_la_regla_tambien_pide_no_calificar_la_fiabilidad():
    assert "Tampoco califiques con otra palabra la madurez o la fiabilidad de un método" in ht09.REGLA_R22_REDACCION


# ================================================================== cierre de la QA r06: la reescritura que no cabe en la bolsa
@pytest.mark.parametrize("disponible, reescribe", [(1.5, False), (50.0, True)])   # 1,5: justo la primera llamada
def test_cierre_r06_la_reescritura_que_no_cabe_en_la_bolsa_no_se_pide(disponible, reescribe, tmp_path, universo, monkeypatch):
    """Una bolsa justa para la primera llamada (peor caso 1,5 UC) y no para la reescritura (ese peor caso más las frases): no
    se pide, no hay cierre parcial de la fase, la respuesta con la raíz se queda (G3-MET-13 decidirá) y HA lo dice. Con bolsa
    de sobra, se reescribe."""
    from bloque_a.orquestacion import Bloque
    b = nuevo_bloque(tmp_path, universo)
    llamadas = []

    def una(self, agente, contrato, mensaje, esquema, instrucciones, *a, **k):
        llamadas.append(bool(mensaje.get("reescritura")))
        return SimpleNamespace(datos={"t": "Comprobado." if mensaje.get("reescritura") else "Validado."}, peor_caso_uc=1.5)
    monkeypatch.setattr(Bloque, "_invocar_una", una)
    cierres = []
    presupuesto = SimpleNamespace(puede=lambda bolsa, est: est <= disponible,
                                  cierre_parcial=lambda *a: cierres.append(a))
    r = b._invocar("AG-02", "CT-05", {"x": 1}, "INTEGRACION", "instr", AS_OF, "RUN-1", None, "integracion", presupuesto)
    assert llamadas == ([False, True] if reescribe else [False]) and not cierres
    assert r.datos["t"] == ("Comprobado." if reescribe else "Validado.")
    incs = [e["detalle"] for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "INC" and "G3-MET-13 (R22)" in e.get("detalle", "")]
    assert any(("reescrita por la raíz" if reescribe else "sin reescribir: su peor caso") in d for d in incs), incs
    assert reescribe or any("no cabe en la bolsa COMUN; decide G3-MET-13" in d for d in incs)
