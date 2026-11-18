"""T-187 · pruebas de `revision_prompts_pb51.py` con casos sintéticos (y una de regresión sobre el corpus real).

Uso, desde la raíz:  .venv/bin/python -m pytest -q .docs/scripts/pruebas_revision_prompts_pb51.py
`PB51_MODULO` apunta a otra copia del script (lo usa `mutantes_revision_prompts_pb51.py`). Las recoge
`.docs/scripts/pruebas_scripts.sh`. Los datos guardados (informe, muestra y veredictos) están en `.docs/tickets/T-187/`.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
DATOS = RAIZ / ".docs" / "tickets" / "T-187"
EJECUTOR = RAIZ / "bloque_a" / "11_Ejecutor"
_spec = importlib.util.spec_from_file_location("rp", os.environ.get("PB51_MODULO", AQUI / "revision_prompts_pb51.py"))
assert _spec and _spec.loader
rp = importlib.util.module_from_spec(_spec)
sys.modules["rp"] = rp                      # las dataclass lo buscan ahí
_spec.loader.exec_module(rp)

TITULOS = ["Identidad y misión (quién eres)", "Posición en el bloque", "Reglas críticas que te aplican",
           "Entradas y salidas", "Procedimiento operativo paso a paso", "Metodología y criterios de decisión propios",
           "Eficiencia: presupuesto", "Autocrítica y control de calidad", "Aprendizaje: cómo usas F6",
           "**Base de conocimientos** (precisa)", "Formatos de salida y ejemplo breve", "Límites, seguridad y modos degradados"]
D0 = "# Documento 0\n\n## ANEXO F. Otro\n\n1. No es esto\n\n## ANEXO G. ESTRUCTURA COMÚN\n\nTodo prompt:\n\n" + \
    "\n".join(f"{i}. {t}" for i, t in enumerate(TITULOS, 1)) + "\n\n## ANEXO H. Siguiente\n\n1. Tampoco\n"
ANEXO = rp.leer_anexo_g(D0)

SEC10 = """### 10.1 Paridades

- **Paridad cubierta (CIP)**: `F/S = (1 + i·τ)/(1 + i*·τ)`. La divisa de tipo alto cotiza con descuento.
- **Enigma de la PPA** (Rogoff, 1996, «The Purchasing Power Parity Puzzle»): vida media de 3–5 años.
- Umbral de alerta: déficit corriente > 4 % del PIB y reservas de al menos 3 meses.

#### 10.1.1 Detalle

- Un elemento del detalle con Meese y Rogoff (1983) y un `doi.org/<DOI>` que no es fórmula.

### 10.2 Trampas frecuentes

1. Presentar el forward como previsión.
2. Mezclar convenciones.

### 10.2 bis Otra cosa

Párrafo con Rentabilidad = diferencial + contado
que sigue en otra línea. Hay un error frecuente aquí.

| Columna | Valor |
| --- | --- |
| **Fila**: definida | `a = b` |

### 10.3 Referencias canónicas

Meese y Rogoff (1983, «Empirical Exchange Rate Models») · Hansen y Hodrick (1980) · Rogoff (1996) · Hull («Options, Futures»)

- Tversky, A. y Kahneman, D. (1974). «Judgment under Uncertainty». *Science*; (1983). «Extensional versus Intuitive Reasoning».
- Si necesitas otra referencia, pídela al Documentador (CT-08).

### 10.4 Inventario de competencias

- **Paridades**: CIP y UIP (10.1) con `x = y` y > 5 umbrales.
"""


def prompt(secciones: dict[int, str] | None = None, titulos: dict[int, str] | None = None, cuerpo10: str = SEC10) -> str:
    out = ["# System prompt de prueba", ""]
    for n in (secciones or {i: "" for i in range(1, 13)}):
        t = (titulos or {}).get(n, TITULOS[n - 1].replace("**", "").split(" (")[0])
        cuerpo = (secciones or {}).get(n) or (cuerpo10 if n == 10 else
                                             "- **Término**: definición con `a + b` y un umbral ≥ 2." if n == 6 else "Texto.")
        out += [f"## {n}. {t}", "", cuerpo, ""]
    return "\n".join(out)


# ---------------------------------------------------------------- Anexo G y secciones
def test_anexo_g_lee_las_doce_secciones_y_para_en_el_titulo_siguiente():
    assert [n for n, _ in ANEXO] == list(range(1, 13))
    assert ANEXO[9][1] == "Base de conocimientos (precisa)"


@pytest.mark.parametrize("d0", ["# Sin anexo\n1. Algo\n", "## ANEXO G. X\n\n1. Uno\n3. Tres\n", "## ANEXO G. X\n\nNada\n"])
def test_anexo_g_ausente_o_mal_numerado_falla(d0):
    with pytest.raises(ValueError):
        rp.leer_anexo_g(d0)


def test_estructura_completa_y_titulos_coherentes():
    e = rp.revisar_estructura(rp.secciones(prompt()), ANEXO)
    assert e["completa"] and e["faltan"] == [] and all(t["coincide"] for t in e["titulos"].values())


def test_titulos_en_mayusculas_y_plurales_coinciden():
    e = rp.revisar_estructura(rp.secciones(prompt(titulos={1: "IDENTIDAD Y MISIÓN", 11: "Formato y estilo"})), ANEXO)
    assert e["titulos"][1]["coincide"] and e["titulos"][11]["coincide"]


def test_titulo_sin_palabra_comun_es_variante_pero_no_rompe_la_estructura():
    e = rp.revisar_estructura(rp.secciones(prompt(titulos={6: "Estrategia de análisis del tipo de activo"})), ANEXO)
    assert e["completa"] and not e["titulos"][6]["coincide"]


def test_falta_una_seccion():
    secs = {i: "" for i in range(1, 13) if i != 10}
    e = rp.revisar_estructura(rp.secciones(prompt(secs)), ANEXO)
    assert e["faltan"] == [10] and not e["completa"]


def test_seccion_repetida_sobrante_o_desordenada():
    t = prompt() + "\n## 13. Extra\n\nx\n## 4. Otra vez\n"
    e = rp.revisar_estructura(rp.secciones(t), ANEXO)
    assert e["sobran"] == [13] and e["repetidas"] == [4] and not e["en_orden"] and not e["completa"]


def test_desordenada_sin_faltar_sobrar_ni_repetir_no_es_completa():
    """Las 12 secciones, una vez cada una, pero la 4 y la 5 cambiadas de sitio."""
    t = prompt()
    a, b = t.index("## 4."), t.index("## 5.")
    c = t.index("## 6.")
    t = t[:a] + t[b:c] + t[a:b] + t[c:]
    e = rp.revisar_estructura(rp.secciones(t), ANEXO)
    assert not e["faltan"] and not e["sobran"] and not e["repetidas"] and not e["en_orden"] and not e["completa"]


def test_titulos_dentro_de_un_bloque_de_codigo_no_son_secciones():
    t = prompt().replace("## 12.", "```\n## 99. Falso\n```\n## 12.")
    assert 99 not in [s.numero for s in rp.secciones(t)]


def test_la_seccion_acaba_en_un_titulo_de_nivel_1():
    t = prompt() + "\n# ANEXO A\n\n- **No cuenta**: `x = y`\n"
    s12 = next(s for s in rp.secciones(t) if s.numero == 12)
    assert not any("No cuenta" in x for x in s12.lineas)


# ---------------------------------------------------------------- subáreas y elementos
def _sec10(cuerpo=SEC10):
    return next(s for s in rp.secciones(prompt(cuerpo10=cuerpo)) if s.numero == 10)


def test_subareas_suman_los_niveles_4_y_separan_bis():
    claves = [s.clave for s in rp.subareas(_sec10())]
    assert claves == ["10.1", "10.2", "10.2 bis", "10.3", "10.4"]
    assert any("Meese" in e.texto for e in rp.subareas(_sec10())[0].elementos)


def test_preambulo_antes_de_la_primera_subarea():
    claves = [s.clave for s in rp.subareas(_sec10("Este es tu conocimiento con `a = b`.\n\n" + SEC10))]
    assert claves[0] == "10.0"


def test_elementos_vinetas_parrafos_tablas_y_codigo():
    lineas = ["- uno", "  sigue", "- dos", "", "párrafo", "continúa", "", "| a | b |", "| --- | --- |", "| c | d |",
              "```", "x = 1", "```"]
    es = rp.elementos(lineas, 100)
    assert [e.texto for e in es] == ["uno\n  sigue", "dos", "párrafo\ncontinúa", "| a | b |", "| c | d |", "```\nx = 1\n```"]
    assert [e.linea for e in es] == [100, 102, 104, 107, 109, 110] and es[3].tabla and not es[0].tabla


# ---------------------------------------------------------------- clasificadores
@pytest.mark.parametrize("t,esperado", [
    ("**CIP**: `F = S`", True), ("**Enigma** (Rogoff, 1996, «X (Y)»): vida", True), ("**Puntos** = F − S", True),
    ("Texto con **negrita**: no al principio", False), ("**Solo negrita** sin más", False)])
def test_definicion(t, esperado):
    assert rp.es_definicion(t) is esperado


@pytest.mark.parametrize("t,n", [
    ("`F/S = (1 + i)`", 1), ("`ln(S_t)`", 1), ("`√T`", 1), ("`doi.org/<DOI>`", 0), ("`web.archive.org/save/<URL>`", 0),
    ("`https://x.org/a`", 0), ("`fondo_entry_NNN`", 0), ("Rentabilidad = diferencial + contado", 1),
    ("`a = b` y `c ≈ d` y x = y", 3), ("a=b sin espacios", 0)])
def test_formulas(t, n):
    assert rp.n_formulas(t) == n


@pytest.mark.parametrize("t,n", [
    ("déficit > 4 % y ≤ 2", 2), ("al menos 3 meses", 1), ("más de la mitad", 0), ("`<URL>`", 0), ("x ≥ −1,5", 1),
    ("como mínimo el 20 %", 1), ("entre 3 y 5 años", 0)])
def test_umbrales(t, n):
    assert rp.n_umbrales(t) == n


def test_citas_formas_a_b_y_c():
    t = ("Meese y Rogoff (1983, «Models») y Mark (1995). También (Balassa, 1964; Samuelson, 1964, «Theoretical») y "
         "Hamilton, *Time Series Analysis*, Princeton, 1994. Y Hoyt (1933). «One Hundred Years».")
    cs = {(c.autores, c.anio): c.titulo for c in rp.citas(t)}
    assert cs == {("Meese y Rogoff", "1983"): True, ("Mark", "1995"): False, ("Balassa", "1964"): False,
                  ("Samuelson", "1964"): True, ("Hamilton", "1994"): True, ("Hoyt", "1933"): True}


def test_citas_con_particulas_et_al_y_falsos_positivos():
    t = ("programa lineal de Rockafellar y Uryasev (2000); López de Prado (2018, «Advances»); Scheffer et al. (2009); "
         "véase el Anexo (2020) y (abril de 2022) y (EUR, USD).")
    cs = {c.autores: c.anio for c in rp.citas(t)}
    assert cs == {"Rockafellar y Uryasev": "2000", "López de Prado": "2018", "Scheffer et al.": "2009"}


def test_citas_sin_doble_cuenta_de_la_forma_a():
    assert len(rp.citas("Rogoff (1996, «The Puzzle»)")) == 1


def test_trampas_por_titulo_y_por_texto():
    sub_t = rp.Subarea("10.2", "Trampas frecuentes")
    sub_o = rp.Subarea("10.3", "Otra")
    assert rp.es_trampa("cualquier cosa", sub_t) and rp.es_trampa("un error típico", sub_o)
    assert not rp.es_trampa("nada", sub_o)


def test_recuento_por_subarea_con_inventario_excluido():
    f = {x["subarea"]: x for x in rp.recuento_seccion10(_sec10())}
    assert (f["10.1"]["definiciones"], f["10.1"]["formulas"], f["10.1"]["umbrales"], f["10.1"]["referencias"]) == (2, 1, 2, 2)
    assert f["10.2"]["trampas"] == 2 and f["10.2 bis"]["trampas"] == 1
    assert f["10.2 bis"]["formulas"] == 2 and f["10.2 bis"]["definiciones"] == 0
    assert f["10.3"]["es_referencias"] and f["10.3"]["referencias"] == 6
    assert f["10.4"]["excluida"] and f["10.4"]["definiciones"] == f["10.4"]["formulas"] == f["10.4"]["umbrales"] == 0


def test_recuento_sin_seccion_10():
    assert rp.recuento_seccion10(None) == []


# ---------------------------------------------------------------- referencias
def test_entradas_de_la_lista_y_autores_heredados():
    es = rp.entradas_lista("Tversky, A. y Kahneman, D. (1974). «A». *Science*; (1983). «B». · Hull («C») · Si necesitas otra (CT-08)")
    assert [(x["autor"], x["anio"], x["titulo"]) for x in es] == [(True, True, True), (True, True, True), (True, False, True)]
    assert es[1]["clave"] == ("tversky", "1983")


def test_entrada_de_tabla_por_celdas():
    es = rp.entradas_lista("| IDX | Campbell y Shiller (1998), «Valuation ratios» |")
    assert len(es) == 1 and es[0]["autor"] and es[0]["titulo"]


def test_entrada_con_iniciales_e_institucion():
    assert rp.entradas_lista("J.P. Morgan/Reuters (1996), *RiskMetrics*")[0]["autor"]
    assert not rp.entradas_lista("Anexo (2020) «X»")[0]["autor"]


def test_referencias_estricto_y_amplio():
    t = prompt() + "\nMás: Hansen y Hodrick (1980, «Forward Exchange Rates») en otra sección.\n"
    r = rp.revisar_referencias(_sec10(), t)
    e = {x["entrada"].split(" (")[0]: x for x in r["entradas"]}
    assert e["Meese y Rogoff"]["titulo_en_la_entrada"]
    assert not e["Hansen y Hodrick"]["titulo_en_la_entrada"] and e["Hansen y Hodrick"]["titulo_en_el_prompt"]
    assert e["Rogoff"]["titulo_en_el_prompt"]          # (Rogoff, 1996, «…») en 10.1
    assert not e["Hull"]["autor_anio"]
    assert r["tiene_lista"] and len(r["entradas"]) == 6


def test_sin_lista_de_referencias():
    r = rp.revisar_referencias(_sec10(SEC10.split("### 10.3")[0]), "nada")
    assert not r["tiene_lista"] and r["entradas"] == []


# ---------------------------------------------------------------- identificadores
@pytest.mark.parametrize("d,ok", [("10.1000/182", True), ("10.1016/j.jfineco.2010.01.001", True), ("10.12/x", False),
                                  ("10.1000/", False), ("11.1000/x", False), ("10.abcd/x", False)])
def test_estructura_del_doi(d, ok):
    assert rp.doi_valido(d) is ok


def test_identificadores_en_texto():
    t = ("Ver 10.2 y 10.15 (secciones), doi: 10.1000/182. y https://doi.org/10.1016/j.jfineco.2010.01.001, "
         "API por DOI: mejor versión, doi: 12/x, ISBN 978-0-306-40615-7, ISBN 0-306-40615-3, ISSN 0378-5955, ISSN 0378-5954")
    ids = rp.identificadores(t)
    assert [(x["doi"], x["estructura_valida"]) for x in ids["doi"]] == [
        ("10.1000/182", True), ("10.1016/j.jfineco.2010.01.001", True), ("12/x", False)]
    assert [x["control_valido"] for x in ids["isbn"]] == [True, False]
    assert [x["control_valido"] for x in ids["issn"]] == [True, False]


@pytest.mark.parametrize("s,ok", [("0-306-40615-2", True), ("080442957X", True), ("9780306406157", True),
                                  ("9780306406158", False), ("12345", False)])
def test_isbn(s, ok):
    assert rp.isbn_valido(s) is ok


# ---------------------------------------------------------------- frases y muestra
def test_frases_con_abreviaturas_codigo_e_iniciales():
    t = ("En EE. UU. el ISM > 42. Según Bailey et al. Hay más. Usa `a. B` sin cortar. Mt. Gox quebró. "
         "La fórmula (véase p. ej. MC-01. Otra) sigue. Fin.")
    fs = rp.frases(t)
    assert fs == ["En EE. UU. el ISM > 42.", "Según Bailey et al. Hay más.", "Usa `a. B` sin cortar.", "Mt. Gox quebró.",
                  "La fórmula (véase p. ej. MC-01. Otra) sigue.", "Fin."]
    assert all(f in t for f in fs)


def test_marcas():
    assert rp.marcas("**X**: vale `a = b` > 3 (Mark, 1995) y 7,5 billones") == ["formula", "umbral", "definicion", "cita", "cifra"]
    assert rp.marcas("Declara siempre la dirección de lectura.") == []


def test_candidatas_solo_de_metodo_y_conocimientos_y_copia_exacta():
    t = prompt(secciones={i: ("- **Fuera**: `x = y` > 3 en la sección {i}" if i not in (6, 10) else "") for i in range(1, 13)})
    cs = rp.candidatas(t, rp.secciones(t), 6, 10)
    assert cs and all(c["seccion"].split(".")[0] in ("6", "10") for c in cs)
    assert all(c["texto"] in t for c in cs)
    assert not any("Inventario" in (c["subarea"] or "") or "Referencias" in (c["subarea"] or "") for c in cs)
    lineas = t.splitlines()
    assert all(c["texto"].splitlines()[0] in lineas[c["linea"] - 1] for c in cs)


def test_candidatas_llevan_su_referencia():
    t = prompt()
    cs = {c["texto"]: c for c in rp.candidatas(t, rp.secciones(t), 6, 10)}
    c = next(v for k, v in cs.items() if k.startswith("**Enigma"))
    assert c["referencia_citada"] == "Rogoff, 1996, «The Purchasing Power Parity Puzzle»"
    d = next(v for k, v in cs.items() if k.startswith("**Paridad cubierta"))
    assert not any(k.startswith("La divisa de tipo alto") for k in cs)    # sin marca técnica: no es candidata
    assert d["referencia_citada"] is None and d["referencia_del_elemento"] is None


def test_muestra_determinista_de_tamano_fijo_y_ordenada():
    cands = [{"i": i} for i in range(40)]
    a = rp.muestra(cands, "s", "x.md")
    assert a == rp.muestra(cands, "s", "x.md") and len(a) == rp.MUESTRA_POR_PROMPT == 10
    assert [c["i"] for c in a] == sorted(c["i"] for c in a)
    assert a != rp.muestra(cands, "otra", "x.md") and a != rp.muestra(cands, "s", "y.md")
    assert rp.muestra(cands[:4], "s", "x.md") == cands[:4]


# ---------------------------------------------------------------- tamaños
def test_tamano_con_tope_propio_con_tope_de_analista_y_sin_tope():
    t = prompt()
    secs = rp.secciones(t)
    topes = {"AG-10": 10 ** 6, "AG-11": 1, "analista": 10 ** 6}
    a = rp.revisar_tamano(t, secs, "AG-10", topes, {"AG-03"}, 10, EJECUTOR)
    b = rp.revisar_tamano(t, secs, "AG-11", topes, {"AG-03"}, 10, EJECUTOR)
    c = rp.revisar_tamano(t, secs, "AG-03", topes, {"AG-03"}, 10, EJECUTOR)
    d = rp.revisar_tamano(t, secs, "AG-19", topes, {"AG-03"}, 10, EJECUTOR)
    assert a["dentro"] is True and b["dentro"] is False and a["medida"] == a["tokens_aprox"]
    assert c["dentro"] is True and c["medida"] < c["tokens_aprox"]
    assert d["dentro"] is None and d["tope"] is None
    assert a["palabras"] == len(t.split()) and a["lineas"] == len(t.splitlines())


# ---------------------------------------------------------------- de punta a punta
def _repo(tmp: Path, tope=True) -> Path:
    (tmp / "bloque_a" / "01_Gobernanza").mkdir(parents=True)
    (tmp / "bloque_a" / "01_Gobernanza" / "Documento 0 - Protocolo maestro del Bloque A - V9.md").write_text(D0, "utf-8")
    dp = tmp / "bloque_a" / "02_System_prompts"
    dp.mkdir(parents=True)
    (dp / "System prompt - Analista de Divisas - Versión óptima V5.0.md").write_text(prompt(), "utf-8")
    (dp / "System prompt - MC-01 Algo - Versión óptima V5.0.md").write_text(
        prompt(titulos={6: "Estrategia de análisis"}), "utf-8")
    (dp / "Marco común (plantilla) - V5.0.md").write_text(prompt({i: "" for i in range(1, 13) if i not in (6, 10)}), "utf-8")
    cfg = tmp / "bloque_a" / "11_Ejecutor" / "config"
    cfg.mkdir(parents=True)
    (cfg / "por_defecto.yaml").write_text("v6:\n  tope_tokens_system: {analista: 100000, AG-10: 1}\n" if tope else "v6: {}\n",
                                          "utf-8")
    return tmp


def _correr(raiz: Path, *extra: str) -> int:
    return rp.principal(["--raiz", str(raiz), "--salida", str(raiz / "out"), "--ejecutor", str(EJECUTOR), *extra])


def test_de_punta_a_punta_y_comprobar(tmp_path):
    raiz = _repo(tmp_path)
    assert _correr(raiz) == 0
    inf = (raiz / "out" / "informe_pb51.md").read_text("utf-8")
    m = json.loads((raiz / "out" / "muestra_afirmaciones.json").read_text("utf-8"))
    assert "2 de 2 prompts (100.0 %)" in inf and "faltan [6, 10]" in inf
    assert "Estrategia de análisis** (no coincide)" in inf
    assert m["total"] == sum(1 for a in m["afirmaciones"]) and {a["agente_id"] for a in m["afirmaciones"]} == {"AG-05", None}
    assert {a["id"].rsplit("-", 1)[0] for a in m["afirmaciones"]} == {"AF-AG-05", "AF-MC-01"}
    assert all(a["veredicto"] is None and a["nota"] is None for a in m["afirmaciones"])
    texto = (raiz / "bloque_a" / "02_System_prompts" / "System prompt - Analista de Divisas - Versión óptima V5.0.md").read_text("utf-8")
    assert all(a["texto"] in texto for a in m["afirmaciones"] if a["agente_id"] == "AG-05")
    assert _correr(raiz, "--comprobar") == 0
    (raiz / "out" / "informe_pb51.md").write_text(inf + "x", "utf-8")
    assert _correr(raiz, "--comprobar") == 1


def test_determinista_entre_ejecuciones(tmp_path):
    a, b = _repo(tmp_path / "a"), _repo(tmp_path / "b")
    _correr(a)
    _correr(b)
    for n in ("informe_pb51.md", "muestra_afirmaciones.json"):
        assert (a / "out" / n).read_text("utf-8") == (b / "out" / n).read_text("utf-8")


def test_falla_cerrado_sin_documento_0_o_sin_topes(tmp_path):
    raiz = _repo(tmp_path / "a")
    (raiz / "bloque_a" / "01_Gobernanza" / "Documento 0 - Protocolo maestro del Bloque A - V9.md").unlink()
    assert _correr(raiz) == 2 and not (raiz / "out").exists()
    assert _correr(_repo(tmp_path / "b", tope=False)) == 2


def test_falla_cerrado_con_dos_documentos_0(tmp_path):
    raiz = _repo(tmp_path)
    (raiz / "bloque_a" / "01_Gobernanza" / "Documento 0 - Protocolo maestro del Bloque A - V10.md").write_text(D0, "utf-8")
    assert _correr(raiz) == 2


# ---------------------------------------------------------------- paso 3: contraste de los revisores
NOTA = "Fuente consultada. Conocimiento propio."


def _afs(n_por_prompt=(3, 2)):
    out = []
    for k, n in enumerate(n_por_prompt):
        cod = f"AG-0{k + 1}"
        out += [{"id": f"AF-{cod}-{i:02d}", "prompt": f"System prompt - P{k}.md", "agente": f"P{k}", "agente_id": cod,
                 "linea": 10 + i, "texto": f"Frase {i} | con barra"} for i in range(1, n + 1)]
    return out


def _lote(n, vs, revisor="rev", notas=None):
    notas = notas or {}
    return {"archivo": f"lote_{n}.json", "lote": n, "revisor": revisor,
            "veredictos": [{"id": i, "veredicto": v, "nota": notas.get(i, NOTA)} for i, v in vs]}


def _coment(erratas=(), dudosas=(), discutibles=(), sens=(), cita="Fuente consultada. Conocimiento"):
    return {"erratas": {i: {"error": "e", "correccion": "c", "cita_nota": cita} for i in erratas},
            "criterio_dudosas": "CORRECTA con matiz.",
            "dudosas": {i: "matiz" for i in dudosas}, "dudosas_cita_nota": {i: "Matiz: el año." for i in dudosas},
            "discutibles": list(discutibles), "sensibilidad": {"ids": list(sens), "motivo": "Elegidos por el comentario."}}


VS = [("AF-AG-01-01", "CORRECTA"), ("AF-AG-01-02", "ERRONEA"), ("AF-AG-01-03", "NO_VERIFICABLE"),
      ("AF-AG-02-01", "CORRECTA"), ("AF-AG-02-02", "CORRECTA")]
CON_MATIZ = {"AF-AG-02-01": "Correcta. Matiz: el año. Conocimiento propio."}


def test_contraste_recuentos_por_lote_por_prompt_y_totales():
    c = rp.contraste(_afs(), [_lote(1, VS[:2]), _lote(2, VS[2:], notas=CON_MATIZ)],
                     _coment(erratas=["AF-AG-01-02"], dudosas=["AF-AG-02-01"], sens=["AF-AG-01-02"]))
    assert c["total"] == {"CORRECTA": 3, "ERRONEA": 1, "NO_VERIFICABLE": 1} and c["n"] == 5
    assert c["verificables"] == 4 and c["pct_verificables"] == 75.0 and c["pct_total"] == 60.0 and c["supera"] is False
    assert [(x["lote"], x["CORRECTA"], x["ERRONEA"], x["NO_VERIFICABLE"], x["prompts"]) for x in c["por_lote"]] == \
        [(1, 1, 1, 0, ["AG-01"]), (2, 2, 0, 1, ["AG-01", "AG-02"])]
    assert [(f["codigo"], f["CORRECTA"], f["ERRONEA"], f["NO_VERIFICABLE"], f["lotes"]) for f in c["por_prompt"]] == \
        [("AG-01", 1, 1, 1, ["lote_1.json", "lote_2.json"]), ("AG-02", 2, 0, 0, ["lote_2.json"])]
    assert [e["id"] for e in c["erratas"]] == ["AF-AG-01-02"] and c["erratas"][0]["correccion"] == "c"
    assert [e["id"] for e in c["dudosas"]] == ["AF-AG-02-01"]
    s = c["sensibilidad"]
    assert (s["como_correctas"]["correctas"], s["como_correctas"]["erroneas"], s["como_correctas"]["supera"]) == (4, 0, True)
    assert (s["sin_ellas"]["correctas"], s["sin_ellas"]["verificables"], s["sin_ellas"]["supera"]) == (3, 3, True)
    texto = "\n".join(rp.informe_contraste(c))
    assert "| AF-AG-01-02 | P0 (12) | Frase 2 \\| con barra | e | c | Fuente consultada. Conocimiento |" in texto
    assert "| AF-AG-02-01 | P1 (11) | matiz | Matiz: el año. |" in texto
    assert "75.0 %" in texto and "60.0 %" in texto and "NO SUPERA" in texto and "el veredicto **cambia**" in texto
    assert "Elegidos por el comentario." in texto and "llama discutibles en su nota: ninguna" in texto


def test_contraste_cuenta_verificables_por_prompt_y_lista_los_cortos():
    """QA r01, H-02: la columna «Verificables» y la lista de prompts por debajo de 10."""
    afs = _afs((10, 10))
    vs = [(a["id"], "CORRECTA") for a in afs[:10]] + [(a["id"], "CORRECTA") for a in afs[10:13]] + \
         [(a["id"], "NO_VERIFICABLE") for a in afs[13:]]
    c = rp.contraste(afs, [_lote(1, vs)], _coment())
    assert [(f["codigo"], f["verificables"]) for f in c["por_prompt"]] == [("AG-01", 10), ("AG-02", 3)]
    assert [(f["agente"], f["verificables"]) for f in c["cortos"]] == [("P1", 3)]
    texto = "\n".join(rp.informe_contraste(c))
    assert "| P1 | AG-02 | 1 | 3 | 0 | 7 | 3 | 100.0 % |" in texto
    assert "1 de 2 prompts quedan por debajo de 10 verificables: P1 3." in texto


def test_contraste_cuenta_veredictos_por_fuente():
    """QA r01, H-04: la fuente que declara la nota, con «sin búsqueda web» como memoria."""
    notas = {"AF-AG-01-01": "Confirmado. Búsqueda web: ejemplo.org.", "AF-AG-01-02": "Conocimiento propio, sin búsqueda web.",
             "AF-AG-01-03": "Regla interna.", "AF-AG-02-01": "Comprobado a mano: 2 + 2 = 4.", "AF-AG-02-02": "Web: x.eu."}
    c = rp.contraste(_afs(), [_lote(1, VS, notas=notas)], _coment(erratas=["AF-AG-01-02"], cita="sin búsqueda web"))
    f = c["por_fuente"]
    assert f[("CORRECTA", "búsqueda web")] == 2 and f[("ERRONEA", "memoria (conocimiento propio)")] == 1
    assert f[("NO_VERIFICABLE", rp.SIN_FUENTE)] == 1 and f[("CORRECTA", "cálculo a mano")] == 1
    assert sum(f.values()) == 5
    texto = "\n".join(rp.informe_contraste(c))
    assert "| CORRECTA | 2 | 0 | 1 | 0 |" in texto and "| NO_VERIFICABLE | 0 | 0 | 0 | 1 |" in texto


def test_contraste_umbral_en_el_limite_y_no_verificables_fuera_del_denominador():
    afs = [{"id": f"AF-AG-01-{i:02d}", "prompt": "p.md", "agente": "P", "agente_id": "AG-01", "linea": i, "texto": "t"}
           for i in range(1, 51)]
    vs = [(a["id"], "CORRECTA") for a in afs[:19]] + [(afs[19]["id"], "ERRONEA")] + \
         [(a["id"], "NO_VERIFICABLE") for a in afs[20:]]
    c = rp.contraste(afs, [_lote(1, vs)], _coment(erratas=[afs[19]["id"]]))
    assert c["pct_verificables"] == 95.0 and c["supera"] is True and c["pct_total"] == 38.0
    vs2 = [(a["id"], "CORRECTA") for a in afs[:18]] + [(afs[18]["id"], "ERRONEA")] + \
          [(a["id"], "NO_VERIFICABLE") for a in afs[19:]]
    assert rp.contraste(afs, [_lote(1, vs2)], _coment(erratas=[afs[18]["id"]]))["supera"] is False
    assert rp.porcentajes({"CORRECTA": 0, "ERRONEA": 0, "NO_VERIFICABLE": 3})["supera"] is False


@pytest.mark.parametrize("vs, motivo", [
    (VS[:-1], "faltan"),
    (VS + [("AF-AG-09-01", "CORRECTA")], "sobran"),
    ([VS[0], ("AF-AG-01-02", "FALSA")] + VS[2:], "veredicto desconocido"),
    ([VS[0], ("AF-AG-01-02", ["ERRONEA"])] + VS[2:], "veredicto desconocido"),
    (VS + [VS[0]], "duplicado"),
])
def test_contraste_falla_cerrado_con_ids_o_veredictos_que_no_casan(vs, motivo):
    with pytest.raises(rp.ContrasteInvalido, match=motivo):
        rp.contraste(_afs(), [_lote(1, vs)], _coment(erratas=["AF-AG-01-02"]))


def test_contraste_falla_cerrado_con_un_id_repetido_entre_lotes():
    with pytest.raises(rp.ContrasteInvalido, match="duplicado: AF-AG-01-01 \\(lote_1.json y lote_2.json\\)"):
        rp.contraste(_afs(), [_lote(1, VS[:2]), _lote(2, VS[2:] + VS[:1])], _coment(erratas=["AF-AG-01-02"]))


def test_contraste_nota_de_40_palabras_vale_y_de_41_vacia_o_sin_letras_falla():
    for nota, falla in ((" ".join(["palabra"] * rp.MAX_PALABRAS_NOTA), False),
                        (" ".join(["palabra"] * (rp.MAX_PALABRAS_NOTA + 1)), True), ("", True), ("—", True), ("  ", True)):
        lt = _lote(1, VS)
        lt["veredictos"][3]["nota"] = nota
        if falla:
            with pytest.raises(rp.ContrasteInvalido, match="AF-AG-02-01"):
                rp.contraste(_afs(), [lt], _coment(erratas=["AF-AG-01-02"]))
        else:
            assert rp.contraste(_afs(), [lt], _coment(erratas=["AF-AG-01-02"]))["n"] == 5
    assert rp.MAX_PALABRAS_NOTA == 40


def _sin(d, k):
    return {x: y for x, y in d.items() if x != k}


@pytest.mark.parametrize("coment, motivo", [
    (_coment(), "erratas"),
    (_coment(erratas=["AF-AG-01-02", "AF-AG-01-01"]), "erratas"),
    (_coment(erratas=["AF-AG-01-02"]) | {"erratas": {"AF-AG-01-02": {"error": "e", "correccion": " ",
                                                                      "cita_nota": "Fuente"}}}, "correccion"),
    (_coment(erratas=["AF-AG-01-02"], dudosas=["AF-AG-01-03"]), "dudoso no es CORRECTA"),
    (_coment(erratas=["AF-AG-01-02"], dudosas=["AF-AG-01-01"]), "criterio"),
    (_coment(erratas=["AF-AG-01-02"], discutibles=["AF-AG-01-01"]), "discutible no es ERRONEA"),
    (_coment(erratas=["AF-AG-01-02"], discutibles=["AF-AG-01-02"]), "nota no lo dice"),
    (_coment(erratas=["AF-AG-01-02"], discutibles=[["AF-AG-01-02"]]), "lista de ids"),
    (_coment(erratas=["AF-AG-01-02"], sens=["AF-AG-01-01"]), "sensibilidad no es ERRONEA"),
    (_coment(erratas=["AF-AG-01-02"]) | {"sensibilidad": {"ids": ["AF-AG-01-02"], "motivo": " "}}, "motivo"),
    (_coment(erratas=["AF-AG-01-02"]) | {"sensibilidad": {"ids": [["AF-AG-01-02"]], "motivo": "m"}}, "ids"),
    (_sin(_coment(erratas=["AF-AG-01-02"]), "sensibilidad"), "necesita"),
    (_sin(_coment(erratas=["AF-AG-01-02"]), "dudosas"), "necesita"),
    (_sin(_coment(erratas=["AF-AG-01-02"]), "dudosas_cita_nota"), "dudosas_cita_nota"),
])
def test_contraste_falla_cerrado_si_el_comentario_no_casa(coment, motivo):
    with pytest.raises(rp.ContrasteInvalido, match=motivo):
        rp.contraste(_afs(), [_lote(1, VS)], coment)


def test_contraste_dudosas_exactamente_las_correctas_con_matiz():
    """QA r01, H-03: falta una CORRECTA con matiz en la nota, o sobra; y el matiz no puede estar vacío."""
    with pytest.raises(rp.ContrasteInvalido, match="criterio"):
        rp.contraste(_afs(), [_lote(1, VS, notas=CON_MATIZ)], _coment(erratas=["AF-AG-01-02"]))
    com = _coment(erratas=["AF-AG-01-02"], dudosas=["AF-AG-02-01"])
    com["dudosas"]["AF-AG-02-01"] = ""
    with pytest.raises(rp.ContrasteInvalido, match="«matiz»"):
        rp.contraste(_afs(), [_lote(1, VS, notas=CON_MATIZ)], com)


def test_contraste_falla_cerrado_si_la_cita_no_esta_en_la_nota():
    """QA r01, H-03: cada errata y cada dudosa citan literalmente la nota de su revisor."""
    with pytest.raises(rp.ContrasteInvalido, match="AF-AG-01-02: «cita_nota»"):
        rp.contraste(_afs(), [_lote(1, VS)], _coment(erratas=["AF-AG-01-02"], cita="los revisores la consideran discutible"))
    with pytest.raises(rp.ContrasteInvalido, match="«cita_nota»"):
        rp.contraste(_afs(), [_lote(1, VS)], _coment(erratas=["AF-AG-01-02"], cita="—"))
    com = _coment(erratas=["AF-AG-01-02"], dudosas=["AF-AG-02-01"])
    com["dudosas_cita_nota"]["AF-AG-02-01"] = "la búsqueda web no confirmó el año"
    with pytest.raises(rp.ContrasteInvalido, match="AF-AG-02-01: «cita_nota»"):
        rp.contraste(_afs(), [_lote(1, VS, notas=CON_MATIZ)], com)
    notas = {"AF-AG-01-02": "Discutible: la cifra varía según el año."}
    c = rp.contraste(_afs(), [_lote(1, VS, notas=notas)], _coment(erratas=["AF-AG-01-02"], discutibles=["AF-AG-01-02"],
                                                                     cita="la cifra varía"))
    assert c["discutibles"] == ["AF-AG-01-02"] and c["sensibilidad_ids"] == ["AF-AG-01-02"]


def test_contraste_falla_cerrado_con_una_cita_de_menos_de_tres_palabras():
    """QA r02, H-09: «a» o « de » son subcadenas de cualquier nota y no sostienen nada."""
    assert rp.MIN_PALABRAS_CITA == 3
    notas = {"AF-AG-01-02": "Año erróneo: es de 2017. Búsqueda web."}
    for cita, vale in (("a", False), (" de ", False), ("es de", False), ("Año erróneo:", False),
                       ("es de 2017.", True), ("Año erróneo: es", True)):
        com = _coment(erratas=["AF-AG-01-02"], cita=cita)
        if vale:
            assert rp.contraste(_afs(), [_lote(1, VS, notas=notas)], _coment(erratas=["AF-AG-01-02"], cita=cita))["n"] == 5
        else:
            with pytest.raises(rp.ContrasteInvalido, match="menos de 3 palabras"):
                rp.contraste(_afs(), [_lote(1, VS, notas=notas)], com)
    com = _coment(erratas=["AF-AG-01-02"], dudosas=["AF-AG-02-01"], cita="es de 2017.")
    com["dudosas_cita_nota"]["AF-AG-02-01"] = "Matiz: el"
    with pytest.raises(rp.ContrasteInvalido, match="AF-AG-02-01: «cita_nota» tiene menos de 3"):
        rp.contraste(_afs(), [_lote(1, VS, notas=notas | CON_MATIZ)], com)


def test_leer_lotes_falla_cerrado_sin_lotes_o_con_formato_malo(tmp_path):
    with pytest.raises(rp.ContrasteInvalido, match="no hay lotes"):
        rp.leer_lotes(tmp_path)
    (tmp_path / "lote_1.json").write_text("{", "utf-8")
    with pytest.raises(rp.ContrasteInvalido, match="JSONDecodeError"):
        rp.leer_lotes(tmp_path)
    (tmp_path / "lote_1.json").write_text(json.dumps({"revisor": "r", "veredictos": [{"veredicto": "CORRECTA"}]}), "utf-8")
    with pytest.raises(rp.ContrasteInvalido, match="sin «id»"):
        rp.leer_lotes(tmp_path)
    for revisor in (None, "  ", "—"):
        (tmp_path / "lote_1.json").write_text(json.dumps({"revisor": revisor, "veredictos": []}), "utf-8")
        with pytest.raises(rp.ContrasteInvalido, match="revisor"):
            rp.leer_lotes(tmp_path)
    for n in (10, 2):
        (tmp_path / f"lote_{n}.json").write_text(json.dumps({"lote": n, "revisor": "r", "veredictos": []}), "utf-8")
    (tmp_path / "lote_1.json").write_text(json.dumps({"lote": 1, "revisor": "r", "veredictos": []}), "utf-8")
    assert [x["lote"] for x in rp.leer_lotes(tmp_path)] == [1, 2, 10]


def _veredictos_para(raiz: Path) -> Path:
    """Escribe en `out/veredictos` un lote que juzga toda la muestra generada (una ERRONEA) y su comentario."""
    m = json.loads((raiz / "out" / "muestra_afirmaciones.json").read_text("utf-8"))
    ids = [a["id"] for a in m["afirmaciones"]]
    dv = raiz / "out" / "veredictos"
    dv.mkdir()
    vs = [{"id": i, "veredicto": "ERRONEA" if k == 0 else "CORRECTA", "nota": NOTA} for k, i in enumerate(ids)]
    (dv / "lote_1.json").write_text(json.dumps({"lote": 1, "revisor": "r", "veredictos": vs}), "utf-8")
    (dv / "comentario.json").write_text(json.dumps(_coment(erratas=[ids[0]])), "utf-8")
    return dv


@pytest.mark.parametrize("estropear", [
    lambda dv: (dv / "lote_1.json").write_bytes((dv / "lote_1.json").read_bytes()[:-3] + b"\xff\xfe}"),
    lambda dv: (dv / "comentario.json").write_bytes(b"\xff" + (dv / "comentario.json").read_bytes()),
    lambda dv: (dv / "lote_9.json").mkdir(),
    lambda dv: (dv / "comentario.json").unlink() or (dv / "comentario.json").mkdir(),
], ids=["lote_utf8_invalido", "comentario_utf8_invalido", "lote_es_carpeta", "comentario_es_carpeta"])
def test_entradas_que_no_se_pueden_leer_salen_con_2_sin_traza(tmp_path, estropear):
    """QA r01, H-05: UnicodeDecodeError y OSError también son fallo cerrado (los casos de r01_03)."""
    raiz = _repo(tmp_path)
    assert _correr(raiz) == 0
    estropear(_veredictos_para(raiz))
    assert _correr(raiz) == 2


def test_de_punta_a_punta_con_veredictos_y_fallo_cerrado(tmp_path):
    raiz = _repo(tmp_path)
    assert _correr(raiz) == 0
    inf0 = (raiz / "out" / "informe_pb51.md").read_text("utf-8")
    assert "Paso 3 · Contraste" not in inf0 and "## Paso 3 · Muestra\n" in inf0
    dv = _veredictos_para(raiz)
    assert _correr(raiz, "--comprobar") == 1          # el contraste cambia el informe
    assert _correr(raiz) == 0
    inf = (raiz / "out" / "informe_pb51.md").read_text("utf-8")
    assert "## Paso 3 · Contraste de la muestra" in inf and "| Paso 3 · afirmaciones correctas |" in inf
    assert "sin juzgar" not in inf                    # QA r01, H-07
    assert _correr(raiz, "--comprobar") == 0
    m = json.loads((raiz / "out" / "muestra_afirmaciones.json").read_text("utf-8"))
    assert all(a["veredicto"] is None for a in m["afirmaciones"])     # la muestra no se rellena
    lote = json.loads((dv / "lote_1.json").read_text("utf-8"))
    lote["veredictos"][1]["veredicto"] = "DUDOSA"
    (dv / "lote_1.json").write_text(json.dumps(lote), "utf-8")
    assert _correr(raiz) == 2 and _correr(raiz, "--comprobar") == 2
    assert (raiz / "out" / "informe_pb51.md").read_text("utf-8") == inf      # no escribe nada
    (tmp_path / "vacia").mkdir()
    assert _correr(raiz, "--veredictos", str(tmp_path / "vacia")) == 2
    (dv / "lote_1.json").unlink()
    (dv / "comentario.json").unlink()
    assert _correr(raiz) == 2                         # carpeta de veredictos sin lotes


def test_corpus_real_el_contraste_supera_el_criterio():
    """Los veredictos guardados: 350 afirmaciones y PB-51 supera el 95 % sobre las verificables (INC-T187-02)."""
    if "PB51_MODULO" in os.environ:
        pytest.skip("con un mutante no se compara con lo guardado")
    m = json.loads((DATOS / "muestra_afirmaciones.json").read_text("utf-8"))
    c = rp.leer_contraste(DATOS / "veredictos", m["afirmaciones"])
    assert (c["n"], c["total"]) == (350, {"CORRECTA": 260, "ERRONEA": 9, "NO_VERIFICABLE": 81})
    assert c["supera"] and round(c["pct_verificables"], 1) == 96.7 and round(c["pct_total"], 1) == 74.3
    assert [(x["CORRECTA"], x["ERRONEA"], x["NO_VERIFICABLE"]) for x in c["por_lote"]] == \
        [(66, 2, 22), (58, 5, 27), (74, 2, 14), (62, 0, 18)]
    assert c["sensibilidad"]["como_correctas"]["supera"] and c["sensibilidad"]["sin_ellas"]["supera"]
    assert c["discutibles"] == [] and len(c["cortos"]) == 28 and c["cortos"][0]["verificables"] == 2
    assert [d["id"] for d in c["dudosas"]] == ["AF-MC-02-04", "AF-MC-06-02", "AF-MC-07-10", "AF-AG-13-09", "AF-AG-17-04"]

# ---------------------------------------------------------------- regresión sobre el corpus real
def test_corpus_real_lo_generado_coincide_con_lo_guardado():
    """El informe y la muestra guardados son los que da el script sobre el corpus actual (cambia el corpus o el script:
    se regeneran a propósito)."""
    if "PB51_MODULO" in os.environ:
        pytest.skip("con un mutante no se compara con lo guardado")
    assert rp.principal(["--raiz", str(RAIZ), "--salida", str(DATOS), "--comprobar"]) == 0
