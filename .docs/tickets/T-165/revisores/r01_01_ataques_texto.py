"""T-165 QA r01 · ataques del revisor a la lectura del texto de G3-MET-13 (`ht09.comprobar_madurez`, `ht09.textos_de`,
`ht09.texto_html`), con el Catálogo REAL (81 fichas IMPLEMENTADO, ninguna VALIDADO: «validado» de cualquiera es falso) y con la
preparación de PB-47 (ML-CLUS-001 en DOCUMENTADO, que el Motor no sirve).

Dos direcciones:
- `test_escapa_*`: una madurez falsa que G3-MET-13 tendría que bloquear. Si la prueba falla, la madurez falsa pasa.
- `test_fp_*`: frases legítimas (las de los prompts de los Analistas, variantes realistas y prosa financiera con «validado» en
  otro sentido) que no deberían bloquear. Si la prueba falla, es un falso positivo.
- `test_control_*`: lo que el implementador dice que hace y debe seguir haciendo (comprobación de que el banco de casos no es vacuo).

Las pruebas que fallan son hallazgos (ver qa.md, ronda r01). Sin red ni gasto.

Uso, desde bloque_a/11_Ejecutor:
    ../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-165/revisores/r01_01_ataques_texto.py -rf
"""
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

RAIZ = Path.cwd()
sys.path.insert(0, str(RAIZ))
from bloque_a import sintesis as sint  # noqa: E402
from bloque_a.herramientas import ht09  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402

assert Path(sint.__file__).resolve().is_relative_to(RAIZ.resolve()), f"importa otra copia: {sint.__file__}"
BLOQUE = SimpleNamespace(motor=SimpleNamespace(raiz=None))


def _real(textos):
    return sint._comprobar_met13(BLOQUE, textos)


def _pb47(textos, monkeypatch):
    original = servicio.madurez_catalogo
    monkeypatch.setattr(servicio, "madurez_catalogo", lambda raiz=None: {**original(raiz), "ML-CLUS-001": "DOCUMENTADO"})
    return sint._comprobar_met13(BLOQUE, textos)


def _txt(t):
    return [("r", t, "BLOQUEO")]


def _json(obj):
    return [(r, t, "BLOQUEO") for r, t in ht09.textos_de(obj, "paquete")]


def test_control_catalogo_real():
    m = servicio.madurez_catalogo()
    assert len(m) == 81 and not [f for f, e in m.items() if ht09.nivel_catalogo(e) != 2]


# ------------------------------------------------------------------ 1. ¿se escapa? (Catálogo real)
ESCAPA_TEXTO = {
    # otras formas del verbo y sinónimos
    "E01_valido_preterito": "VOL-GARCH-001 se validó con datos de 2010 a 2024.",
    "E02_validacion_superada": "VOL-GARCH-001 ha superado la validación fuera de muestra.",
    "E03_revalidado": "VOL-GARCH-001, revalidado en 2025, sostiene la banda.",
    "E04_verificado_probado": "VOL-GARCH-001 es un método verificado y probado en producción.",
    # la excepción «validado por» + lista cerrada, pero dicho del método
    "E05_por_los_datos": "VOL-GARCH-001 está validado por los datos fuera de muestra.",
    "E06_por_el_mercado": "VOL-GARCH-001, validado por el mercado en tres crisis.",
    "E07_por_la_evidencia": "La volatilidad sale de VOL-GARCH-001, un método validado por la evidencia empírica.",
    "E08_por_datos_historicos": "ST-DESC-001 validado por datos históricos de diez años.",
    # la ficha con otra grafía
    "E09_guion_no_separable": "VOL‑GARCH‑001 está validado.",
    "E10_guion_largo": "VOL–GARCH–001 está validado.",
    "E11_minusculas": "vol-garch-001 está validado.",
    "E12_parcial_sin_numero": "VOL-GARCH está validado.",
    "E13_espacios": "VOL GARCH 001 está validado.",
    # la frase repartida
    "E14_dos_frases_punto": "La volatilidad sale de VOL-GARCH-001. El método está validado.",
    "E15_dos_frases_punto_y_coma": "La volatilidad sale de VOL-GARCH-001; es un método validado.",
    "E16_salto_de_linea": "Método: VOL-GARCH-001\nEstado: validado",
    "E17_tabla_markdown": "| Método | Estado |\n|---|---|\n| VOL-GARCH-001 | validado |",
    # trucos tipográficos (adversarios: un modelo no suele escribirlos)
    "E18_cirilico": "VOL-GARCH-001 está vаlidado.",
    "E19_guion_blando": "VOL-GARCH-001 está vali­dado.",
    "E20_ancho_cero": "VOL-GARCH-001 está vali​dado.",
    # doble negación
    "E21_doble_negacion": "Nadie diría que VOL-GARCH-001 no está validado.",
}

CONTROL_BLOQUEA = {
    "C01_mayusculas": "VOL-GARCH-001 está VALIDADO.",
    "C02_comillas": "VOL-GARCH-001 está «validado».",
    "C03_comillas_rectas": 'VOL-GARCH-001 está "validado".',
    "C04_nivel": "Nivel de madurez de VOL-GARCH-001: VALIDADO",
    "C05_femenino": "La ficha VOL-GARCH-001 está validada.",
    "C06_plural": "VOL-GARCH-001 y ST-DESC-001, validados.",
    "C07_ingles": "VOL-GARCH-001 has been fully validated.",
    "C08_negacion_trampa": "VOL-GARCH-001 no es experimental sino que fue validado.",
    "C09_sin_duda": "Sin duda, VOL-GARCH-001 está validado.",
    "C10_por_el_motor": "VOL-GARCH-001 validado por el Motor.",
    "C11_emoji": "VOL-GARCH-001 — VALIDADO ✓",
    "C12_backticks": "`VOL-GARCH-001` validado",
    "C13_negrita_md": "**VOL-GARCH-001** (validado)",
    "C14_nbsp": "VOL-GARCH-001 está validado.",
    "C15_inventada": "La señal sale de ML-SUPER-001.",
}


@pytest.mark.parametrize("caso", sorted(ESCAPA_TEXTO))
def test_escapa_texto(caso):
    c = _real(_txt(ESCAPA_TEXTO[caso]))
    assert c["resultado"] == "BLOQUEO", f"{caso}: pasa ({c['resultado']}) «{ESCAPA_TEXTO[caso]}»"


@pytest.mark.parametrize("caso", sorted(CONTROL_BLOQUEA))
def test_control_bloquea(caso):
    assert _real(_txt(CONTROL_BLOQUEA[caso]))["resultado"] == "BLOQUEO", caso


ESCAPA_HTML = {
    "H01_tabla": "<table><tr><th>Método</th><th>Estado</th></tr><tr><td>VOL-GARCH-001</td><td>validado</td></tr></table>",
    "H02_lista_y_parrafo": "<p>La volatilidad sale de VOL-GARCH-001.</p><p>Es un método validado.</p>",
    "H03_atributo_title": '<span title="VOL-GARCH-001 validado">Volatilidad del 18 %</span>',
    "H04_palabra_partida": "<p>VOL-GARCH-001 está <b>vali</b>dado</p>",
    "H05_guion_blando_entidad": "<p>VOL-GARCH-001 está vali&shy;dado</p>",
    "H06_br": "<p>VOL-GARCH-001<br>validado</p>",
}


@pytest.mark.parametrize("caso", sorted(ESCAPA_HTML))
def test_escapa_html(caso):
    c = _real(_txt(ht09.texto_html(ESCAPA_HTML[caso])))
    assert c["resultado"] == "BLOQUEO", f"{caso}: pasa ({c['resultado']})"


def test_control_html_en_linea_y_entidades():
    assert _real(_txt(ht09.texto_html("<li>VOL-GARCH-001 está <strong>validado</strong></li>")))["resultado"] == "BLOQUEO"
    assert _real(_txt(ht09.texto_html("<p>VOL-GARCH-001 est&aacute; validado</p>")))["resultado"] == "BLOQUEO"
    assert _real(_txt(ht09.texto_html("<p>VOL-GARCH-001 est&#225; &#118;alidado</p>")))["resultado"] == "BLOQUEO"


ESCAPA_JSON = {
    "J01_booleano": {"metodo": "VOL-GARCH-001", "validado": True},
    "J02_ficha_en_la_clave": {"estado_madurez_metodos": {"VOL-GARCH-001": "validado"}},
    "J03_clave_ficha_valor": {"VOL-GARCH-001": "VALIDADO"},
    "J04_lista_partida": {"estado_madurez_metodos": ["VOL-GARCH-001", "validado"]},
    "J05_objeto_sin_clave_madurez": {"estado_madurez_metodos": [{"ficha": "VOL-GARCH-001", "estado": "validado"}]},
    "J06_ficha_id": {"ficha_id": "VOL-GARCH-001", "estado_madurez": "validado"},
    "J07_id": {"metodos": [{"id": "VOL-GARCH-001", "madurez": "VALIDADO"}]},
    "J08_ingles": {"method": "VOL-GARCH-001", "maturity": "validated"},
    "J09_numero_nivel": {"metodo": "VOL-GARCH-001", "nivel_madurez": 3},
}


@pytest.mark.parametrize("caso", sorted(ESCAPA_JSON))
def test_escapa_json(caso):
    c = _real(_json(ESCAPA_JSON[caso]))
    assert c["resultado"] == "BLOQUEO", f"{caso}: pasa ({c['resultado']}) {ESCAPA_JSON[caso]}"


def test_control_json():
    assert _real(_json({"metodo": "VOL-GARCH-001", "estado_madurez_metodo": "validado"}))["resultado"] == "BLOQUEO"
    assert _real(_json({"estado_madurez_metodos": ["VOL-GARCH-001 validado"]}))["resultado"] == "BLOQUEO"
    assert _real(_json({"ficha": "VOL-GARCH-001", "madurez": "VALIDADO"}))["resultado"] == "BLOQUEO"


# ------------------------------------------------------------------ 1 bis. ¿se escapa? (preparación de PB-47)
ESCAPA_PB47 = {
    "P01_declarado_y_luego_validado": "ML-CLUS-001: documentado; en la práctica, validado.",
    "P02_rechazado_pero_por_datos": "ML-CLUS-001 rechazado por el Motor, pero validado por los datos.",
    "P03_dos_frases": "ML-CLUS-001 no servido hoy. Validado en ciclos anteriores.",
    "P04_tabla": "| ML-CLUS-001 | documentado | validado en backtest |",
    # la sonda de T-159 con guiones no separables: ni la regla A ni la B (no se reconoce la ficha)
    "P05_guion_no_separable": "Los clústeres de exposición se calculan con ML\u2011CLUS\u2011001, un método validado.",
}


@pytest.mark.parametrize("caso", sorted(ESCAPA_PB47))
def test_escapa_pb47(caso, monkeypatch):
    c = _pb47(_txt(ESCAPA_PB47[caso]), monkeypatch)
    assert c["resultado"] == "BLOQUEO", f"{caso}: pasa ({c['resultado']}) «{ESCAPA_PB47[caso]}»"


def test_control_pb47(monkeypatch):
    for t in ("Los clústeres de exposición se calculan con ML-CLUS-001, un método validado.",
              "ML-CLUS-001 validado por el mercado",          # la excepción, pero la regla B: no se sirve ni se declara
              "ML-CLUS-001 está implementado", "N efectivo ML-CLUS-001: 7"):
        assert _pb47(_txt(t), monkeypatch)["resultado"] == "BLOQUEO", t


# ------------------------------------------------------------------ 2. ¿bloquea de más? (Catálogo real)
PROMPTS = Path(RAIZ).parent / "02_System_prompts"


def _ejemplos_prompts():
    import re
    out = set()
    for f in sorted(PROMPTS.glob("*.md")):
        t = f.read_text(encoding="utf-8")
        out |= {m.group(1) for m in re.finditer(r'"estado_madurez_metodos":"([^"…]+)"', t)}
    return sorted(out)


EJEMPLOS = _ejemplos_prompts()


def test_control_hay_ejemplos_de_prompts():
    assert len(EJEMPLOS) >= 12, EJEMPLOS


@pytest.mark.parametrize("texto", EJEMPLOS)
def test_fp_ejemplos_de_los_prompts(texto, monkeypatch):
    assert _real(_txt(texto))["resultado"] == "OK", texto
    assert _real(_json({"estado_madurez_metodos": texto}))["resultado"] == "OK", texto


FP = {
    # variantes realistas de estado_madurez_metodos (lo que un modelo escribe al parafrasear el ejemplo)
    "F01_pendiente_de_ser_validado": "VOL-GARCH-001: implementado, pendiente de ser validado",
    "F02_sin_estar_validado": "VOL-GARCH-001: implementado, sin estar validado",
    "F03_a_la_espera_de_ser": "VOL-GARCH-001 implementado, a la espera de ser validado fuera de muestra",
    "F04_validado_no": "VOL-GARCH-001: implementado; validado: no",
    "F05_cuatro_auxiliares": "VOL-GARCH-001 implementado, no ha sido todavía formalmente validado",
    "F06_sin_haber_sido": "VOL-GARCH-001 implementado, sin haber sido validado",
    "F07_no_puede_considerarse": "VOL-GARCH-001 implementado, no puede considerarse validado",
    "F08_no_guion": "VOL-GARCH-001 implementado (no-validado)",
    "F09_non_validated": "VOL-GARCH-001 implemented, non-validated",
    "F10_hasta_que_sea": "VOL-GARCH-001 implementado; se usará con cautela hasta que sea validado",
    "F11_plural_pendientes": "FX-PPA-001 y FX-COINT-001: implementados, pendientes de ser validados",
    # prosa financiera: «validado» en otro sentido, en una frase que cita una ficha
    "F20_ruptura_volumen": "La ruptura quedó validada por el volumen, con la volatilidad VOL-GARCH-001 en el 18 %.",
    "F21_ruptura_parentesis": "Ruptura alcista validada (percentil 96 %, ST-DESC-001).",
    "F22_cruce_de_medias": "Señal técnica validada con el cruce de medias, y el precio en el percentil 40 % (ST-DESC-001).",
    "F23_soporte": "El soporte de 4.200 puntos fue validado tres veces, con el precio en el percentil 35 % (ST-DESC-001).",
    "F24_hipotesis": "Hipótesis validada: el precio está en el percentil 12 % (ST-DESC-001).",
    "F25_consenso": "El escenario base, validado por el consenso de analistas, deja el carry (FX-CARRY-001) en positivo.",
    "F26_comite": "Con el umbral de 0,7 validado por el comité de riesgos, ML-CLUS-001 agrupa las series.",
    "F27_tesis_validada_con": "La tesis quedó validada con el dato de inflación, y el percentil (ST-DESC-001) sigue bajo.",
}

CONTROL_OK = {
    "O01_no_validado": "VOL-GARCH-001 implementado, no validado.",
    "O02_validacion_pendiente": "VOL-GARCH-001: implementado (validación fuera de muestra pendiente)",
    "O03_sin_validar": "VOL-GARCH-001 implementado, aún sin validar",
    "O04_operador": "Umbral del percentil (ST-DESC-001) validado por el operador.",
    "O05_dato_de_empleo": "La tesis, validada por el dato de empleo, se apoya en ST-DESC-001.",
    "O06_otra_frase": "La ruptura quedó validada por el volumen; volatilidad VOL-GARCH-001 del 18 %.",
    "O07_implementado_bce": "Implementado el recorte del BCE, el carry (FX-CARRY-001) mejora.",
    "O08_valido": "El dato de empleo validó la tesis, con ST-DESC-001 en el percentil 70.",
}


@pytest.mark.parametrize("caso", sorted(FP))
def test_fp(caso):
    c = _real(_txt(FP[caso]))
    assert c["resultado"] == "OK", f"{caso}: bloquea «{FP[caso]}»: {[i['detalle'][:90] for i in c['incidencias']]}"


@pytest.mark.parametrize("caso", sorted(CONTROL_OK))
def test_control_ok(caso):
    assert _real(_txt(CONTROL_OK[caso]))["resultado"] == "OK", caso


# PB-47 bien declarado en una tabla o en dos celdas: el Analista hace lo que le pide su prompt
FP_PB47 = {
    "Q01_tabla_md": "| Método | Madurez |\n|---|---|\n| ML-CLUS-001 | documentado |",
    "Q02_dos_lineas": "Método: ML-CLUS-001\nMadurez: documentado (no se sirve)",
}


@pytest.mark.parametrize("caso", sorted(FP_PB47))
def test_fp_pb47_declarado_en_otra_celda(caso, monkeypatch):
    c = _pb47(_txt(FP_PB47[caso]), monkeypatch)
    assert c["resultado"] == "OK", f"{caso}: bloquea: {[i['detalle'][:90] for i in c['incidencias']]}"


def test_fp_pb47_html_tabla(monkeypatch):
    t = ht09.texto_html("<table><tr><td>ML-CLUS-001</td><td>documentado</td></tr></table>")
    c = _pb47(_txt(t), monkeypatch)
    assert c["resultado"] == "OK", [i["detalle"][:90] for i in c["incidencias"]]


# ------------------------------------------------------------------ 3. localización: qué retira F6
def _afectadas(comp):
    """La regla de F6 (`orquestacion._validar_g3`): los OPP- de la ruta y del detalle de cada incidencia BLOQUEO."""
    import re
    return {x for i in comp["incidencias"] if i["severidad"] == "BLOQUEO"
            for x in re.findall(r"OPP-\d{4}-\d{4,}", i["ruta"] + " " + i["detalle"])}


def test_fp_retira_una_opcion_que_solo_se_cita():
    """La opción A afirma la madurez falsa y cita la opción B en la misma frase: F6 retira también B (el extracto del detalle)."""
    paquete = {"clases": {"RV": {"opciones": [
        {"opp_id": "OPP-2026-0001", "mecanismo": "Complementa a OPP-2026-0002, y VOL-GARCH-001 está validado."},
        {"opp_id": "OPP-2026-0002", "mecanismo": "Persistencia del impulso."}]}}}
    c = sint.g3_met13(BLOQUE, paquete, {}, None)
    assert c["resultado"] == "BLOQUEO"
    assert _afectadas(c) == {"OPP-2026-0001"}, _afectadas(c)


# ------------------------------------------------------------------ 4. coste: una frase larga
def test_tiempo_lineal_en_una_frase_larga():
    """36 KB sin punto (2000 «no está validado,» tras una ficha): la negación se busca en todo el prefijo de cada palabra, y el
    coste crece con el cuadrado de la frase (6 s con la máquina cargada; 88 s con 144 KB). Lineal serían milisegundos."""
    import time
    t = "ST-DESC-001 " + " ".join(["no está validado,"] * 2000)
    t0 = time.perf_counter()
    assert _real(_txt(t))["resultado"] == "OK"
    assert time.perf_counter() - t0 < 2.0
