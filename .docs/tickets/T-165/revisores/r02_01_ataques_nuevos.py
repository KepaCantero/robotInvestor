"""T-165 QA r02 · ataques NUEVOS a la lectura de G3-MET-13 (ninguno está en r01_01, en el test del ticket ni en
`r02_bancos_frases.py`, que se usaron para ajustar o medir la r02). Se buscan familias, no casos sueltos.

Catálogo REAL (81 fichas IMPLEMENTADO, ninguna VALIDADO: «validado» de cualquiera es falso) salvo en los casos PB-47, que ponen
ML-CLUS-001 en DOCUMENTADO (no se sirve).

- `test_escapa_*`: madurez falsa que G3-MET-13 tendría que bloquear. Si la prueba falla, pasa.
- `test_fp_*`: frases legítimas que no deberían bloquear. Si la prueba falla, es un falso positivo.
- `test_control_*`: lo que sí hace (el banco no es vacuo).
- `test_coste_*`: tiempo (CPU) con muchas fichas en un párrafo.

Uso, desde bloque_a/11_Ejecutor:
    ../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-165/revisores/r02_01_ataques_nuevos.py -rf
"""
import sys
import time
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


def _res(textos):
    return sint._comprobar_met13(BLOQUE, textos)["resultado"]


def _txt(t):
    return [("r", t, "BLOQUEO")]


def _json(obj):
    return [(r, t, "BLOQUEO") for r, t in ht09.textos_de(obj, "p")]


def _html(h):
    return [("visual", ht09.texto_html(h), "BLOQUEO")]


@pytest.fixture
def pb47(monkeypatch):
    original = servicio.madurez_catalogo
    monkeypatch.setattr(servicio, "madurez_catalogo", lambda raiz=None: {**original(raiz), "ML-CLUS-001": "DOCUMENTADO"})


# ------------------------------------------------------------------ 1. escapes (Catálogo real)
ESCAPA = {
    # N1 · el método descrito con un sustantivo de la lista «ligada» (indicador de tendencia, estrategia, modelo de previsión…):
    # el sustantivo ligado queda más cerca que la ficha y la palabra se descarta como prosa financiera
    "N1a_indicador_de_tendencia": "ST-DESC-001, indicador de tendencia validado en backtest.",
    "N1b_estrategia": "ST-DESC-001 es nuestra estrategia validada en diez años de datos.",
    "N1c_estrategia_delante": "La estrategia validada ST-DESC-001 entra en la cartera.",
    "N1d_modelo_de_prevision": "VOL-GARCH-001, modelo de previsión validado fuera de muestra.",
    "N1e_algoritmo_de_cruces": "FX-TREND-001, algoritmo de cruces validado en tres crisis.",
    # N2 · «: no …» detrás se lee como «validado: no»
    "N2a_dos_puntos_no_hay_dudas": "ST-DESC-001 está validado: no hay dudas.",
    "N2b_igual_no_cabe_duda": "ST-DESC-001 está validado = no cabe duda.",
    "N2c_dos_puntos_no_falla": "VOL-GARCH-001 quedó validado: no falla desde 2010.",
    # N3 · el sustantivo «validación» con el éxito a más de tres palabras, detrás de «:» o con otro verbo
    "N3a_con_exito_la_validacion": "ST-DESC-001 completó con éxito la validación fuera de muestra.",
    "N3b_fase_de_validacion": "ST-DESC-001 superó con nota la fase de validación.",
    "N3c_validacion_dos_puntos": "ST-DESC-001 · validación: superada.",
    "N3d_validacion_ok": "VOL-GARCH-001 — validación: OK.",
    "N3e_cuenta_con_validacion": "ST-DESC-001 cuenta con validación fuera de muestra completa.",
    "N3f_pruebas_de_validacion": "ST-DESC-001 superó todas las pruebas de validación.",
    "N3g_ingles": "ST-DESC-001 passed out-of-sample validation.",
    # N4 · la ficha con otro separador o con cuatro cifras: no se reconoce y la regla B (falla cerrado) no actúa
    "N4a_guion_bajo": "ST_DESC_001 está validado.",
    "N4b_guion_bajo_minusculas": "La volatilidad sale de vol_garch_001, un método validado.",
    "N4c_puntos": "ST.DESC.001 está validado.",
    "N4d_cuatro_cifras": "ST-DESC-0001 está validado.",
    # N5 · negación de otra cláusula dentro de la ventana
    "N5a_mas_que_nunca": "Hoy, más que nunca, ST-DESC-001 está validado.",
    "N5b_como_nunca": "Como nunca antes, VOL-GARCH-001 está validado.",
    # N6 · tiempos verbales que no están en la raíz
    "N6a_imperfecto": "ST-DESC-001 se validaba cada trimestre con datos nuevos.",
    "N6b_subjuntivo": "Basta con que ST-DESC-001 se valide una vez; ya está hecho.",
    # N7 · estructura: la ficha en un título y la afirmación dos párrafos después; tabla transpuesta
    "N7a_titulo_y_dos_parrafos": "## ST-DESC-001\n\nMide la posición del precio en su rango de tres años.\n\nMétodo validado en backtest.",
    "N7b_tabla_transpuesta": "| | ST-DESC-001 | VOL-GARCH-001 |\n|---|---|---|\n| Madurez | validado | validado |",
}


@pytest.mark.parametrize("caso", sorted(ESCAPA))
def test_escapa_texto(caso):
    assert _res(_txt(ESCAPA[caso])) == "BLOQUEO", ESCAPA[caso]


ESCAPA_JSON = {
    # J1 · una clave de madurez con valor «sí», «yes», 1 o «3» (texto o número que no es 1–3 en una clave de nivel)
    "J1a_validado_si": {"ficha": "ST-DESC-001", "validado": "sí"},
    "J1b_validado_yes": {"ficha": "ST-DESC-001", "validated": "yes"},
    "J1c_entero": {"ficha": "ST-DESC-001", "is_validated": 1},
    "J1d_nivel_texto": {"ficha": "ST-DESC-001", "nivel_madurez": "3"},
    # J2 · la madurez anidada un nivel por debajo de la ficha, o la ficha anidada por debajo de la madurez
    "J2a_madurez_anidada": {"ficha": "ST-DESC-001", "madurez": {"nivel": "VALIDADO"}},
    "J2b_ficha_anidada": {"calculo": {"ficha": "ST-DESC-001"}, "madurez": "validado"},
    "J2c_lista_de_ids": {"metodos": [{"id": "ST-DESC-001"}], "estado": "validado"},
    # J3 · la ficha en un campo y la afirmación en otro del mismo registro
    "J3a_campos_hermanos": {"metodo_principal": "ST-DESC-001", "justificacion": "Método validado en backtest."},
    "J3b_validacion_superada": {"ficha": "ST-DESC-001", "validacion": "superada"},
}


@pytest.mark.parametrize("caso", sorted(ESCAPA_JSON))
def test_escapa_json(caso):
    assert _res(_json(ESCAPA_JSON[caso])) == "BLOQUEO", ESCAPA_JSON[caso]


ESCAPA_HTML = {
    "H1_titulo_y_dos_parrafos": "<h3>ST-DESC-001</h3><p>Percentil del precio.</p><p>Método validado.</p>",
    "H2_tabla_transpuesta": "<table><tr><th></th><th>ST-DESC-001</th></tr><tr><td>Madurez</td><td>validado</td></tr></table>",
}


@pytest.mark.parametrize("caso", sorted(ESCAPA_HTML))
def test_escapa_html(caso):
    assert _res(_html(ESCAPA_HTML[caso])) == "BLOQUEO", ESCAPA_HTML[caso]


# PB-47 · regla B: cualquier «rechazado» (también negado o de otra cosa) o código del Motor en la misma unidad declara la ficha
ESCAPA_PB47 = {
    "B1_no_fue_rechazado": "ML-CLUS-001 no fue rechazado y agrupa las series en tres clústeres.",
    "B2_el_motor_no_ha_rechazado": "El Motor no ha rechazado ML-CLUS-001: agrupa las series.",
    "B3_otra_cosa_rechazada": "Los clústeres salen de ML-CLUS-001; la alternativa fue rechazada.",
    "B4_codigo_negado": "ML-CLUS-001 agrupa las series; METODO_NO_IMPLEMENTADO no aparece en este ciclo.",
    "B5_no_se_sirven_otras": "ML-CLUS-001 agrupa las series y se sirve con normalidad; no se sirven otras.",
}


@pytest.mark.parametrize("caso", sorted(ESCAPA_PB47))
def test_escapa_pb47(caso, pb47):
    assert _res(_txt(ESCAPA_PB47[caso])) == "BLOQUEO", ESCAPA_PB47[caso]


# ------------------------------------------------------------------ 2. falsos positivos (frases legítimas nuevas)
FP = {
    # S · sinónimos de «validado» añadidos en la r02 (comprobado, contrastado, probado, verificado) en su uso normal: comprobar
    # un dato o un cálculo con la ficha
    "S1_hemos_comprobado_con": "Hemos comprobado con ST-DESC-001 que el precio está en el percentil 95 %.",
    "S2_comprobado_a_fecha": "ST-DESC-001 comprobado a fecha 2026-03-01: percentil 88 %.",
    "S3_contrastado_con_proveedor": "El cálculo de ST-DESC-001 se ha contrastado con la serie del proveedor.",
    "S4_probado_con_la_serie": "ST-DESC-001 probado con la serie semanal: el percentil es 95 %.",
    "S5_riesgo_verificado": "Riesgo verificado con RISK-DD-001: caída máxima del 22 %.",
    # D · la declaración honesta de R22 («ninguna está validada») con «ninguno/ningún» o con la negación interrumpida
    "D1_ninguno_validado": "El ciclo usa ST-DESC-001 y VOL-GARCH-001, ambos implementados y ninguno validado todavía.",
    "D2_ninguna_ficha": "ST-DESC-001 está implementado; ninguna ficha del Catálogo está validada.",
    "D3_tampoco": "Ningún método del ciclo, tampoco ST-DESC-001, está validado.",
    "D4_inciso": "ST-DESC-001 no está, por ahora, validado.",
    "D5_no_se_considera": "ST-DESC-001 no se considera validado.",
    "D6_dista_de": "ST-DESC-001 dista de estar validado.",
    "D7_lejos_de": "ST-DESC-001 está lejos de estar validado.",
    # P · prosa financiera con un sustantivo que no está en la lista
    "P1_regimen_por_la_curva": "Con VOL-GARCH-001 la volatilidad anualizada es del 18 %; el régimen de baja volatilidad está validado por la curva.",
    "P2_curva_invertida": "La curva invertida, validada por tres trimestres de datos, refuerza la lectura de ST-DESC-001.",
}


@pytest.mark.parametrize("caso", sorted(FP))
def test_fp(caso):
    assert _res(_txt(FP[caso])) == "OK", FP[caso]


FP_PB47 = {
    # H-08 residual: la declaración en el párrafo siguiente al título, o en una nota
    "F1_titulo_y_madurez": "## ML-CLUS-001\n\nMadurez: documentado; no se usa.",
    "F2_nota": "ML-CLUS-001 (ver nota).\n\nNota: documentado, el Motor no lo sirve.",
}


@pytest.mark.parametrize("caso", sorted(FP_PB47))
def test_fp_pb47(caso, pb47):
    assert _res(_txt(FP_PB47[caso])) == "OK", FP_PB47[caso]


# ------------------------------------------------------------------ 3. controles (lo que sí hace)
CONTROL_BLOQUEA = ["ST-DESC-001 fue validado.", "Hemos validado ST-DESC-001 en backtest.", "ST-DESC-001 (madurez: validado)",
                   "ST-DESC-001 quedó validado.", "ST-DESC-001 superó la validación.", "El nivel de ST-DESC-001 está validado.",
                   "ST-DESC-001 está validado por el equipo de riesgos.", "Sin duda alguna ST-DESC-001 está validado."]
CONTROL_OK = ["ST-DESC-001 está implementado (no validado).", "ST-DESC-001 todavía sin validar.",
              "La OPEP validó el recorte de producción; ST-DESC-001 lo refleja.",
              "ST-DESC-001 está implementado, pero no ha sido validado fuera de muestra."]


@pytest.mark.parametrize("t", CONTROL_BLOQUEA)
def test_control_bloquea(t):
    assert _res(_txt(t)) == "BLOQUEO"


@pytest.mark.parametrize("t", CONTROL_OK)
def test_control_ok(t):
    assert _res(_txt(t)) == "OK"


def test_control_pb47_sin_declarar(pb47):
    assert _res(_txt("ML-CLUS-001 está en uso.")) == "BLOQUEO"


# ------------------------------------------------------------------ 4. coste: muchas fichas en un párrafo (sin línea en blanco)
def _cpu(t):
    t0 = time.process_time()
    _res(_txt(t))
    return time.process_time() - t0


def test_coste_lineal_en_fichas_por_parrafo():
    _res(_txt("ST-DESC-001"))
    a = _cpu("ST-DESC-001 implementado. " * 2000)
    b = _cpu("ST-DESC-001 implementado. " * 8000)
    print(f"\n  2000 fichas: {a:.2f} s · 8000 fichas: {b:.2f} s · razón {b / max(a, 1e-3):.1f} (lineal ≈ 4, cuadrático ≈ 16)")
    assert b < 8 * max(a, 0.05), f"crece más que linealmente: {a:.2f} s → {b:.2f} s"
