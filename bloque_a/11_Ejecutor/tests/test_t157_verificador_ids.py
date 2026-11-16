"""T-157 (Fase 0) · Verificador de consistencia de identificadores del Bloque A.

Un corpus de juguete con al menos un fallo de cada clase (a) a (f), los contextos que no son citas, el fallo cerrado, el
determinismo, el esquema del informe, la orden de consola y una pasada por el corpus y el código reales cuyas cifras se cuentan
aquí con código propio (no con el del verificador).
"""
import copy
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

import jsonschema
import pytest
from bloque_a.herramientas import verificador_ids as vi
from bloque_a.motor import servicio

from bloque_a import contratos

DIR_EJECUTOR = Path(__file__).resolve().parents[1]
RAIZ_BLOQUE = DIR_EJECUTOR.parent

DOC0 = """# DOCUMENTO 0 — PROTOCOLO DE PRUEBA

## Bloque de juguete · Versión óptima V9.1

## 1. REGLAS CRÍTICAS (R1–R3)

| # | Regla | Contenido |
|---|---|---|
| R1 | Uno | Cita CT-01 y F1. |
| R2 | Dos | — |
| R3 | Tres | — |

## 5. ARCHIVOS

### 5.1 Inventario de archivos

| Código | Archivo | Contenido |
|---|---|---|
| F1 | Registro maestro de tendencias | — |
| F2 | **Historial de análisis** (nuevo) | — |
| F3 | Registro de fuentes | — |
| F5 | Memoria de aprendizaje | — |
| FM | Fondo metodológico (ecosistema) | — |

### 5.2 Reglas de los archivos

Nada.

## 6. MAPA

### 6.1 Contratos en vigor (CT-01 a CT-03)

| Código | Emisor → receptor | Objeto | Tipo |
|---|---|---|---|
| CT-01 | A → B | Uno | Servicio |
| CT-02 | B → A | Dos | Servicio |
| CT-03 | A ↔ B | Tres | Servicio |

### 6.2 Reglas comunes

Nada.

## 7. CICLOS

### 7.3 Fases de un análisis (F0–F2)

Texto que no se lee.

## 9. PUNTUACIONES

### 9.3 Puertas de selección PS1–PS2

| Puerta | Condición | Estado |
|---|---|---|
| PS1 Evidencia | — | — |
| PS2 Datos | — | — |

### 9.4 Otra cosa
"""

CATALOGO = """# Catálogo de juguete

**Versión V9.0** · `catalog_version` 9.0.

## 4. Índice de fichas

| ficha_id | Nombre | Prioridad | Madurez |
|---|---|---|---|
| AA-ALFA-001 | Alfa | P0 | IMPLEMENTADO (pruebas) |
| AA-BETA-001 | Beta | P1 | DOCUMENTADO |
| AA-DELTA-001 | Delta | P1 | IMPLEMENTADO (casos de control) |
| BB-REX-001 | Re-ejecución | P0 | IMPLEMENTADO (casos de control) |
| AA-OMEGA-001 | Omega | P2 | DOCUMENTADO |

Total: 4 fichas.

## 5. Cobertura

Nada.

## 6. Fichas heredadas

### AA-ALFA-001 · Alfa

### AA-BETA-001 · Beta

## 7. Fichas nuevas V9.0 — juguete

### AA-DELTA-001 · Delta

### BB-REX-001 · Re-ejecución
"""

PROMPT = """# System prompt de juguete

Usa CT-01, CT-02 y CT-04 (no existe). Cumple R1 y R9 (no existe). Escribe en F1, en F2 y en F7 (no existe).
La fase F0 no es un archivo. Aplica PS1 y PS3 (no existe). Y F05 (no existe) y F5.
Calcula con la ficha AA-ALFA-001, la AA-BETA-001 y la AA-GAMA-001 (no existe) del Catálogo V8.0.
Lee RF-0002, RF-0099 (no existe), RF-0003 (de baja), la tarjeta RF-1, TA-01 y TM-07 (no existe).
Filtro por códigos JEL (E43, R30, F31).
Pendiente `(F1 − F12) / F12`.
{"serie_ht01":"AA-SERIE-001","ficha_id":"AA-ZETA-001"}
La serie AA-SERIE-001 no es una ficha.
"""

FUNCIONES = """# Funciones de juguete

| ID | Función | Salidas |
|---|---|---|
| MOT-F01 | Primera | — |
| MOT-F04 | Cuarta | Resultados F01–F04 |
"""

ARCHIVOS = {
    "Registro maestro de tendencias (esquema V2.0).md": "# Esquema de archivo operativo — F1 Registro maestro de tendencias\n",
    "Historial de análisis (esquema V2.0).md": "# Esquema de archivo operativo — F2 Historial de análisis\n",
    "Registro de Fuentes - V3.2.md": """# Archivo operativo F3 — Registro de Fuentes para otra cosa

## TF-01 Bancos centrales

#### RF-0001 · Q 90 (A) — Una

#### RF-0002 · Q 80 (B) — Otra

## Registro de bajas

| REF-id | Título | Motivo | Fecha | Sustituta |
|---|---|---|---|---|
| RF-0003 | Repetida | Duplicado de RF-0001 | 2026-11-02 | RF-0001 |
""",
    "Documentación - V3.2.md": "# Archivo operativo F4 — Documentación para nadie\n\n## TA-01 Macro\n\n## TM-01 Estadística\n",
    "Fondo - V3.1.md": "# Archivo operativo FM — Fondo metodológico\n",
}


def corpus_juguete(raiz: Path, doc0: str = DOC0, catalogo: str | None = CATALOGO, prompt: str = PROMPT,
                   funciones: str = FUNCIONES, archivos_05: dict | None = None) -> Path:
    archivos = {
        "01_Gobernanza/Documento 0 - Protocolo de prueba - V9.1.md": doc0,
        "02_System_prompts/System prompt - Motor de juguete - V9.0.md": prompt,
        "03_Funciones/Funciones – Motor de juguete.md": funciones,
        **{f"05_Archivos_operativos/{k}": v for k, v in (archivos_05 or ARCHIVOS).items()},
        # nada de esto se lee
        "99_Historico_V1.0/02_System_prompts/viejo.md": "Cita CT-99, R99, F99, PS99 y RF-9999.\n",
        "01_Gobernanza/99_Historico_V9.0/Documento 0 - viejo.md": "Cita CT-97.\n",
        "11_Ejecutor/README.md": "Cita CT-98.\n",
        ".oculta/notas.md": "Cita CT-96.\n",
    }
    (raiz / "04_Motor_conocimiento_y_catalogo").mkdir(parents=True, exist_ok=True)
    if catalogo is not None:
        archivos["04_Motor_conocimiento_y_catalogo/Catálogo de cálculos del Motor - V9.0.md"] = catalogo
    for rel, texto in archivos.items():
        p = raiz / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(texto, encoding="utf-8")
    return raiz


def codigo_juguete(**cambios) -> vi.Codigo:
    base = {"catalog_version": "9.0", "fichas_catalogo": ("AA-ALFA-001", "AA-DELTA-002", "BB-REX-001", "CC-SOLO-001"),
            "manejadores": frozenset({"AA-ALFA-001", "AA-DELTA-002", "CC-SOLO-001"}), "servicios_ct10": frozenset({"BB-REX-001"}),
            "ruta_catalogo": ("04_Motor_conocimiento_y_catalogo", "Catálogo de cálculos del Motor - V9.0.md"),
            "canales": frozenset({"CT-01", "CT-02", "CT-05"}), "canales_admitidos": frozenset({"CT-01", "CT-05"}),
            "campos_minimos": frozenset({"CT-01"}), "fuentes": {"bloque_a/motor/servicio.py": "0" * 64}}
    base.update(cambios)
    return vi.Codigo(**base)


def _de(informe, clase, codigo=None, nivel=None):
    return {h["id"] for h in informe["hallazgos"]
            if h["clase"] == clase and (codigo is None or h["codigo"] == codigo) and (nivel is None or h["nivel"] == nivel)}


@pytest.fixture
def informe(tmp_path):
    return vi.verificar(corpus_juguete(tmp_path), codigo_juguete())


# ---------------------------------------------------------------- CA-2 y CA-3: un fallo de cada clase
def test_a_contratos(informe):
    assert _de(informe, "a", "CT_INEXISTENTE", "ERROR") == {"CT-04"}
    assert _de(informe, "a", "CT_SIN_CANAL") == {"CT-03"}       # en §6.1, no en CANALES
    assert _de(informe, "a", "CT_CANAL_VACIO") == {"CT-02"}     # en CANALES, pero canal_permitido no admite ningún par
    assert _de(informe, "a", "CT_SOLO_CODIGO") == {"CT-05"}     # en CANALES, no en §6.1
    fila = {f["id"]: f for f in informe["contratos"]["filas"]}
    assert fila["CT-01"]["campos_minimos"] and not fila["CT-02"]["campos_minimos"] and fila["CT-04"]["citas"] == 1


def test_b_reglas(informe):
    assert _de(informe, "b", "R_INEXISTENTE", "ERROR") == {"R9"}
    assert informe["reglas"]["definidas"] == ["R1", "R2", "R3"]


def test_c_archivos_y_mapa_por_h1(informe):
    assert _de(informe, "c", "F_INEXISTENTE", "ERROR") == {"F05", "F7"}  # F0 es una fase, F1 y F2 archivos (y fases)
    assert _de(informe, "c", "F_SIN_ARCHIVO", "ERROR") == {"F5"}        # en §5.1, sin archivo que lo declare en su H1
    assert _de(informe, "c", "F_SOLO_ARCHIVO", "ERROR") == {"F4"}       # un H1 dice F4 y §5.1 no lo tiene
    assert _de(informe, "c", "F_NOMBRE_DISTINTO", "AVISO") == {"F3"}    # §5.1 y el H1 no coinciden
    mapa = {m["codigo"]: m for m in informe["archivos"]["mapa"]}
    assert mapa["F2"]["archivo"] == "05_Archivos_operativos/Historial de análisis (esquema V2.0).md"
    assert mapa["F2"]["nombre_doc0"] == "Historial de análisis"         # sin negritas ni «(nuevo)»
    assert mapa["F1"]["nombre_h1"] == "Registro maestro de tendencias" and mapa["FM"]["archivo"].endswith("Fondo - V3.1.md")
    assert informe["archivos"]["fases"] == ["F0", "F1", "F2"]


def test_d_fichas_cuatro_clases(informe):
    clase = {f["id"]: f["clase"] for f in informe["fichas"]["filas"]}
    assert clase["AA-ALFA-001"] == "IMPLEMENTADO"
    assert clase["BB-REX-001"] == "IMPLEMENTADO"                         # por CT-10, sin manejador CT-09
    assert clase["AA-BETA-001"] == "SOLO_CATALOGO"
    assert clase["CC-SOLO-001"] == "SOLO_CODIGO"
    assert clase["AA-DELTA-001"] == clase["AA-DELTA-002"] == "ID_DISTINTO"
    fila = {f["id"]: f for f in informe["fichas"]["filas"]}
    assert fila["AA-DELTA-002"]["similar_a"] == "AA-DELTA-001" and fila["BB-REX-001"]["manejador"] == "CT-10"
    assert _de(informe, "d", "SOLO_CODIGO", "ERROR") == {"CC-SOLO-001"}
    assert _de(informe, "d", "ID_DISTINTO", "ERROR") == {"AA-DELTA-002"}
    assert _de(informe, "d", "SOLO_CATALOGO", "AVISO") == {"AA-BETA-001"}   # DOCUMENTADO y sin código: coherente, aviso
    assert _de(informe, "d", "INDICE_SIN_FICHA", "ERROR") == {"AA-OMEGA-001"}
    assert _de(informe, "d", "FALTA_EN_FICHAS_CATALOGO") == {"AA-BETA-001"}
    assert _de(informe, "d", "FICHA_CITADA_INEXISTENTE", "ERROR") == {"AA-GAMA-001", "AA-ZETA-001"}
    assert informe["fichas"]["conteo_clases"] == {"IMPLEMENTADO": 2, "SOLO_CATALOGO": 2, "SOLO_CODIGO": 1, "ID_DISTINTO": 2}


def test_d_menciones_de_otra_version_y_secciones(informe):
    assert _de(informe, "d", "MENCION_OTRA_VERSION", "AVISO") == {"Catálogo V8.0"}
    m = informe["fichas"]["menciones_otra_version"]
    assert m == [{"version": "8.0", "menciones": 1, "en_prompts": 1,
                  "archivos": ["02_System_prompts/System prompt - Motor de juguete - V9.0.md"]}]
    f = informe["fichas"]
    assert (f["nuevas_en_version"], f["anteriores_a_version"], f["total_declarado"], f["encabezados"]) == (2, 2, 4, 4)


def test_e_referencias(informe):
    assert _de(informe, "e", "REF_INEXISTENTE", "ERROR") == {"RF-0099", "TM-07"}
    assert _de(informe, "e", "REF_DE_BAJA", "AVISO") == {"RF-0003"}
    assert _de(informe, "e", "REF_FORMA_DISTINTA", "AVISO") == {"RF-1"}
    pref = {p["prefijo"]: p for p in informe["referencias"]["prefijos"]}
    assert pref["RF"]["existentes"] == 1 and pref["TA"]["existentes"] == 1 and pref["TM"]["inexistentes"] == 1


def test_f_puertas(informe):
    assert _de(informe, "f", "PS_INEXISTENTE", "ERROR") == {"PS3"}


def test_un_error_de_cada_clase(informe):
    for c in "abcdef":
        assert informe["resumen"][c]["ERROR"] >= 1, c
    assert informe["errores"] == sum(1 for h in informe["hallazgos"] if h["nivel"] == "ERROR")


def _motivos(informe):
    return {(h["id"], h["mensaje"].split(" aparece como ")[1].rsplit(": no se cuenta", 1)[0]) for h in informe["hallazgos"]
            if h["codigo"] == "CITA_EN_CONTEXTO_AJENO"}


def test_contextos_que_no_son_citas(informe):
    info = _motivos(informe)
    assert ("R30", "código JEL de clasificación de la literatura económica") in info
    assert ("F31", "código JEL de clasificación de la literatura económica") in info
    assert ("F12", "notación dentro de una fórmula") in info
    assert ("F01", "abreviatura de la función MOT-F01 del mismo documento, en el rango F01–F04") in info
    serie_motivo = ("símbolo de una serie (valor de «serie_ht01» en "
                    "02_System_prompts/System prompt - Motor de juguete - V9.0.md:9), no una ficha")
    assert ("AA-SERIE-001", serie_motivo) in info
    serie = [h for h in informe["hallazgos"] if h["id"] == "AA-SERIE-001"]
    assert len(serie) == 1 and [u["linea"] for u in serie[0]["ubicaciones"]] == [9, 10]   # también en prosa, ya declarada
    errores = {h["id"] for h in informe["hallazgos"] if h["nivel"] == "ERROR"}
    assert not errores & {"R30", "F31", "F12", "F01", "F04", "AA-SERIE-001"}


TRAMPAS = PROMPT + """{"estado_madurez_metodos":"AA-CARYY-001: implementado"}
{"metodo":"Brier frente a la referencia (AA-ETA-001)"}
Clasificación JEL de la fuente; el contrato CT-27 manda y la regla R28 también.
Regla de corte: `R29 = R1 + R2`.
Usa la ficha ZZ-ALFA-001 y la QQ-WXYZ-001.
Según el catálogo v7.0 del Motor.
Contrato CT\u201106 con guion no separable.
"""


def test_r02_contextos_no_excusan_de_mas(tmp_path):
    """QA r01, H-02 y H-03: una ficha en un valor JSON o en prosa dentro de él, un CT en una línea con «JEL», una R en una
    fórmula y un F13 en prosa de un documento con la función MOT-F13 son errores; H-05: familia desconocida, mayúsculas y
    guion U+2011."""
    raiz = corpus_juguete(tmp_path, prompt=TRAMPAS,
                          funciones=FUNCIONES + "| MOT-F13 | Trece | — |\n\nEl archivo F13 no existe.\n")
    inf = vi.verificar(raiz, codigo_juguete())
    assert {"AA-CARYY-001", "AA-ETA-001"} <= _de(inf, "d", "FICHA_CITADA_INEXISTENTE", "ERROR")
    assert {"CT-06", "CT-27"} <= _de(inf, "a", "CT_INEXISTENTE", "ERROR")          # CT-06 escrito con U+2011
    assert {"R28", "R29"} <= _de(inf, "b", "R_INEXISTENTE", "ERROR")                # «JEL» en la línea; R en una fórmula
    assert "F13" in _de(inf, "c", "F_INEXISTENTE", "ERROR")
    assert "ZZ-ALFA-001" in _de(inf, "d", "FICHA_CITADA_INEXISTENTE", "ERROR")     # familia desconocida, parecida a AA-ALFA-001
    assert _de(inf, "d", "FAMILIA_DESCONOCIDA", "INFO") == {"QQ-WXYZ-001"}
    assert _de(inf, "d", "MENCION_OTRA_VERSION", "AVISO") == {"Catálogo V8.0", "Catálogo V7.0"}
    assert not {i for i, _ in _motivos(inf)} & {"AA-CARYY-001", "AA-ETA-001", "CT-27", "R28", "R29", "F13"}


def test_r02_rango_de_funciones_con_un_extremo_ajeno_no_excusa(tmp_path):
    raiz = corpus_juguete(tmp_path, funciones=FUNCIONES + "Resultados F04–F09.\n")   # MOT-F09 no existe
    assert "F09" in _de(vi.verificar(raiz, codigo_juguete()), "c", "F_INEXISTENTE", "ERROR")


def test_cada_hallazgo_con_ubicacion_real(informe, tmp_path):
    """Cada ubicación apunta a una línea del corpus que contiene el ID (o es su encabezado o tabla)."""
    for h in informe["hallazgos"]:
        if h["codigo"] in {"CT_INEXISTENTE", "R_INEXISTENTE", "F_INEXISTENTE", "PS_INEXISTENTE", "REF_INEXISTENTE",
                           "FICHA_CITADA_INEXISTENTE"}:
            assert h["ubicaciones"]
            for u in h["ubicaciones"]:
                linea = (tmp_path / u["archivo"]).read_text(encoding="utf-8").splitlines()[u["linea"] - 1]
                assert h["id"] in linea, (h["id"], u)


# ---------------------------------------------------------------- CA-7: ni 99_Historico* ni 11_Ejecutor
def test_no_lee_historico_ni_ejecutor(informe):
    ids = {h["id"] for h in informe["hallazgos"]}
    assert not ids & {"CT-96", "CT-97", "CT-98", "CT-99", "R99", "F99", "PS99", "RF-9999"}   # CT-96: carpeta con punto
    assert informe["entradas"]["md_escaneados"] == 9
    texto = json.dumps(informe, ensure_ascii=False)
    assert "99_Historico_V1.0" not in texto and "11_Ejecutor/README" not in texto


# ---------------------------------------------------------------- CA-4: falla cerrado
def test_sin_documento_0_falla_cerrado(tmp_path):
    raiz = corpus_juguete(tmp_path)
    (raiz / "01_Gobernanza/Documento 0 - Protocolo de prueba - V9.1.md").unlink()
    with pytest.raises(vi.EntradaInvalida, match="Documento 0: se esperaba exactamente uno .* hay 0"):
        vi.verificar(raiz, codigo_juguete())


def test_dos_documentos_0_fallan_cerrado(tmp_path):
    raiz = corpus_juguete(tmp_path)
    (raiz / "01_Gobernanza/Documento 0 - Protocolo de prueba - V9.2.md").write_text(DOC0, encoding="utf-8")
    with pytest.raises(vi.EntradaInvalida, match="hay 2"):
        vi.verificar(raiz, codigo_juguete())


def test_nombres_en_nfd_se_encuentran(tmp_path):
    """QA r01, H-07 (M14): el patrón del Catálogo lleva acentos; un nombre en NFD solo casa si se normaliza a NFC."""
    raiz = corpus_juguete(tmp_path)
    carpeta = raiz / "04_Motor_conocimiento_y_catalogo"
    nfc = "Catálogo de cálculos del Motor - V9.0.md"
    (carpeta / nfc).rename(carpeta / unicodedata.normalize("NFD", nfc))
    assert any(p.name != nfc and unicodedata.normalize("NFC", p.name) == nfc for p in carpeta.iterdir())
    inf = vi.verificar(raiz, codigo_juguete())
    assert inf["entradas"]["catalogo"]["archivo"] == f"04_Motor_conocimiento_y_catalogo/{nfc}"
    assert inf["fichas"]["encabezados"] == 4


def test_sin_catalogo_falla_cerrado(tmp_path):
    raiz = corpus_juguete(tmp_path, catalogo=None)
    with pytest.raises(vi.EntradaInvalida, match="Catálogo de cálculos del Motor: se esperaba exactamente uno"):
        vi.verificar(raiz, codigo_juguete())


@pytest.mark.parametrize("seccion", ["### 6.1 ", "### 5.1 ", "## 1. ", "### 9.3 ", "### 7.3 "])
def test_sin_seccion_del_documento_0_falla_cerrado(tmp_path, seccion):
    raiz = corpus_juguete(tmp_path, doc0=DOC0.replace(seccion, "### X.Y "))
    with pytest.raises(vi.EntradaInvalida, match="se esperaba una sección"):
        vi.verificar(raiz, codigo_juguete())


def test_rango_del_titulo_contra_la_tabla(tmp_path):
    raiz = corpus_juguete(tmp_path, doc0=DOC0.replace("| R3 | Tres | — |\n", "").replace("| CT-03 | A ↔ B | Tres | Servicio |",
                                                                                         "| CT-03 | A ↔ B | Tres | Servicio |\n| CT-07 | x | y | z |"))
    inf = vi.verificar(raiz, codigo_juguete())
    assert _de(inf, "b", "FALTA_EN_TABLA", "ERROR") == {"R3"}
    assert _de(inf, "a", "FUERA_DE_RANGO", "ERROR") == {"CT-07"}


def test_main_sale_2_y_no_escribe(tmp_path):
    raiz = corpus_juguete(tmp_path / "b", catalogo=None)
    salida = tmp_path / "informe.json"
    assert vi.main(["--raiz", str(raiz), "--json", str(salida)]) == 2
    assert not salida.exists()


# ---------------------------------------------------------------- CA-5 y CA-6: determinismo, versión, huellas y esquema
def test_determinista_con_version_y_huellas(tmp_path, informe):
    otro = vi.verificar(tmp_path, codigo_juguete())
    assert vi.a_json(otro) == vi.a_json(informe) and vi.a_markdown(otro) == vi.a_markdown(informe)
    d0 = informe["entradas"]["documento_0"]
    assert (d0["archivo"], d0["version_nombre"], d0["version_titulo"]) == (
        "01_Gobernanza/Documento 0 - Protocolo de prueba - V9.1.md", "9.1", "9.1")
    assert d0["sha256"] == hashlib.sha256((tmp_path / d0["archivo"]).read_bytes()).hexdigest()
    assert str(tmp_path) not in vi.a_json(informe)                       # sin rutas absolutas
    md = vi.a_markdown(informe)
    assert "Documento 0 - Protocolo de prueba - V9.1.md" in md and "V9.1 (título: V9.1)" in md


def test_version_del_titulo_distinta_avisa(tmp_path):
    raiz = corpus_juguete(tmp_path, doc0=DOC0.replace("Versión óptima V9.1", "Versión óptima V9.3"))
    assert _de(vi.verificar(raiz, codigo_juguete()), "entradas", "VERSION_DOC0_DISTINTA", "AVISO")


def test_informe_que_no_valida_no_se_escribe(informe):
    vi.validar_informe(informe)
    for romper in (lambda r: r["resumen"]["a"].__setitem__("ERROR", 99), lambda r: r["hallazgos"][0].__setitem__("nivel", "GRAVE"),
                   lambda r: r.__setitem__("extra", 1), lambda r: r["fichas"]["filas"][0].__setitem__("clase", "OTRA")):
        roto = copy.deepcopy(informe)
        romper(roto)
        with pytest.raises(jsonschema.ValidationError):
            vi.a_json(roto)
        with pytest.raises(jsonschema.ValidationError):
            vi.a_markdown(roto)


# ---------------------------------------------------------------- código frente al Catálogo
def test_version_ruta_y_madurez_leida_del_codigo(tmp_path):
    raiz = corpus_juguete(tmp_path)
    inf = vi.verificar(raiz, codigo_juguete(catalog_version="8.0", ruta_catalogo=("04", "Catálogo - V8.0.md"),
                                            madurez_leida={"AA-ALFA-001": "DOCUMENTADO"},
                                            versiones_en_codigo=(("11_Ejecutor/x.py", 3, "8.0", True),
                                                                 ("11_Ejecutor/y.py", 1, "8.0", False))))
    assert _de(inf, "d", "CATALOG_VERSION_DISTINTA", "ERROR") == {"CATALOG_VERSION"}
    assert _de(inf, "d", "RUTA_CATALOGO_DISTINTA", "ERROR") == {"RUTA_CATALOGO"}
    assert "AA-ALFA-001" in _de(inf, "d", "MADUREZ_LEIDA_DISTINTA", "ERROR")
    assert _de(inf, "d", "CATALOG_VERSION_LITERAL", "ERROR") == {"catalog_version 8.0"}
    assert _de(inf, "d", "MENCION_OTRA_VERSION_CODIGO", "AVISO") == {"Catálogo V8.0 (código)"}


def test_catalogo_que_promete_lo_que_el_codigo_no_sirve(tmp_path):
    raiz = corpus_juguete(tmp_path, catalogo=CATALOGO.replace("| AA-BETA-001 | Beta | P1 | DOCUMENTADO |",
                                                               "| AA-BETA-001 | Beta | P1 | IMPLEMENTADO |"))
    assert _de(vi.verificar(raiz, codigo_juguete()), "d", "SOLO_CATALOGO", "ERROR") == {"AA-BETA-001"}


def test_codigo_sin_promover_y_no_servible(tmp_path):
    raiz = corpus_juguete(tmp_path)
    inf = vi.verificar(raiz, codigo_juguete(manejadores=frozenset({"AA-ALFA-001", "AA-BETA-001", "AA-DELTA-002", "CC-SOLO-001"}),
                                            servibles=frozenset()))
    assert _de(inf, "d", "CODIGO_SIN_PROMOVER", "AVISO") == {"AA-BETA-001"}
    assert _de(inf, "d", "NO_SERVIBLE_HOY", "AVISO") == {"AA-ALFA-001"}


# ---------------------------------------------------------------- CA-1: la orden de consola y la auditoría
def test_orden_de_consola_escribe_json_y_markdown(tmp_path):
    raiz = corpus_juguete(tmp_path / "bloque")
    js, md = tmp_path / "i.json", tmp_path / "i.md"
    r = subprocess.run([sys.executable, "-m", "bloque_a.herramientas.verificador_ids", "--raiz", str(raiz), "--json", str(js),
                        "--md", str(md)], cwd=DIR_EJECUTOR, capture_output=True, text=True, timeout=300, check=False)
    assert r.returncode == 1, r.stderr                        # el código real frente al corpus de juguete: hay errores
    inf = json.loads(js.read_text(encoding="utf-8"))
    vi.validar_informe(inf)
    assert md.read_text(encoding="utf-8").startswith("# Informe de consistencia de identificadores del Bloque A")
    assert "verificador_ids:" in r.stderr and "errores" in r.stderr


def test_auditoria_solo_cambia_entre_marcas(tmp_path, informe):
    doc = tmp_path / "auditoria.md"
    doc.write_text(f"# Auditoría\n\nantes\n\n{vi.MARCA_INICIO}\nviejo\n{vi.MARCA_FIN}\n\n## Decisiones\n\ndespués\n", encoding="utf-8")
    vi.actualizar_auditoria(doc, vi.a_markdown(informe))
    t = doc.read_text(encoding="utf-8")
    assert t.startswith("# Auditoría\n\nantes\n") and t.endswith(f"{vi.MARCA_FIN}\n\n## Decisiones\n\ndespués\n")
    assert "viejo" not in t and "## Informe de consistencia" in t and "### (a) Contratos CT" in t
    sin = tmp_path / "sin.md"
    sin.write_text("sin marcas\n", encoding="utf-8")
    with pytest.raises(vi.EntradaInvalida):
        vi.actualizar_auditoria(sin, "x")
    assert sin.read_text(encoding="utf-8") == "sin marcas\n"


# ---------------------------------------------------------------- CA-8: el corpus y el código reales, contados aparte
@pytest.fixture(scope="module")
def informe_real():
    return vi.verificar(RAIZ_BLOQUE)


def test_real_documento_0_por_patron(informe_real):
    candidatos = [p for p in (RAIZ_BLOQUE / "01_Gobernanza").iterdir() if p.name.startswith("Documento 0") and p.suffix == ".md"]
    assert len(candidatos) == 1
    d0 = informe_real["entradas"]["documento_0"]
    assert d0["archivo"] == f"01_Gobernanza/{candidatos[0].name}"
    assert d0["version_nombre"] == re.search(r"V(\d+\.\d+)", candidatos[0].name).group(1)


def test_real_fichas_contadas_aparte(informe_real):
    cat = next((RAIZ_BLOQUE / "04_Motor_conocimiento_y_catalogo").glob("Cat*logo de c*lculos del Motor*.md"))
    ids = re.findall(r"^### ([A-Z][A-Z0-9-]+-\d{3}) ", cat.read_text(encoding="utf-8"), re.MULTILINE)
    f = informe_real["fichas"]
    assert f["encabezados"] == len(set(ids)) == len(ids)
    assert f["en_fichas_catalogo"] == len(set(servicio.FICHAS_CATALOGO))
    assert f["manejadores_ct09"] == len(servicio.IMPLEMENTADAS)
    assert f["catalog_version_codigo"] == servicio.CATALOG_VERSION
    implementadas = {x for x in ids if x in servicio.IMPLEMENTADAS or x in servicio.SERVICIOS_CT10}
    assert f["conteo_clases"]["IMPLEMENTADO"] == len(implementadas)
    assert {r["id"] for r in f["filas"] if r["clase"] == "IMPLEMENTADO"} == implementadas


def test_real_contratos_contados_aparte(informe_real):
    d0 = next((RAIZ_BLOQUE / "01_Gobernanza").glob("Documento 0*.md")).read_text(encoding="utf-8")
    seccion = d0[d0.index("\n### 6.1 "):d0.index("\n### 6.2 ")]
    filas = re.findall(r"^\| (CT-\d+) \|", seccion, re.MULTILINE)
    assert informe_real["contratos"]["definidos_doc0"] == filas
    assert informe_real["contratos"]["definidos_codigo"] == sorted(contratos.CANALES, key=lambda x: int(x[3:]))


def test_real_no_lee_historico(informe_real):
    texto = json.dumps(informe_real, ensure_ascii=False)
    assert "99_Historico" not in texto.replace("99_Historico*/", "")
    total = sum(1 for p in RAIZ_BLOQUE.rglob("*.md")
                if not any(x == "11_Ejecutor" or x.startswith(("99_Historico", ".")) for x in p.relative_to(RAIZ_BLOQUE).parts[:-1]))
    assert informe_real["entradas"]["md_escaneados"] == total


# ---------------------------------------------------------------- QA r01: H-01 (determinismo entre procesos)
def test_r02_clave_id_desempata_por_la_cadena():
    assert vi._clave_id("F2") != vi._clave_id("F02")
    assert sorted({"F02", "F2", "F10", "F5", "F05"}, key=vi._clave_id) == ["F02", "F2", "F05", "F5", "F10"]


def test_r02_mismo_json_y_markdown_con_semillas_distintas(tmp_path):
    raiz = corpus_juguete(tmp_path / "bloque")
    salidas = []
    for semilla in ("0", "1", "3", "7"):
        js, md = tmp_path / f"{semilla}.json", tmp_path / f"{semilla}.md"
        r = subprocess.run([sys.executable, "-m", "bloque_a.herramientas.verificador_ids", "--raiz", str(raiz), "--json", str(js),
                            "--md", str(md)], cwd=DIR_EJECUTOR, capture_output=True, text=True, timeout=300, check=False,
                           env={**os.environ, "PYTHONHASHSEED": semilla})
        assert r.returncode == 1, r.stderr
        salidas.append((js.read_bytes(), md.read_bytes()))
    assert len(set(salidas)) == 1
    citas_f = [c["id"] for c in json.loads(salidas[0][0])["archivos"]["citas"]]
    assert citas_f.index("F05") < citas_f.index("F5")                  # el empate de F05 y F5 lo decide la cadena


# ---------------------------------------------------------------- QA r01: H-06 (destino imposible)
def test_r02_destino_imposible_sale_2_y_no_escribe_nada(tmp_path, informe):
    raiz = corpus_juguete(tmp_path / "b")
    audit = tmp_path / "auditoria.md"
    original = f"# A\n\n{vi.MARCA_INICIO}\nviejo\n{vi.MARCA_FIN}\n"
    audit.write_text(original, encoding="utf-8")
    md = tmp_path / "i.md"
    for destino in (tmp_path / "no" / "existe" / "i.json", tmp_path):   # carpeta inexistente; una carpeta como archivo
        assert vi.main(["--raiz", str(raiz), "--md", str(md), "--json", str(destino), "--auditoria", str(audit)]) == 2
        assert audit.read_text(encoding="utf-8") == original and not md.exists()
    js = tmp_path / "i.json"                                             # al revés: el JSON vale y el Markdown no
    assert vi.main(["--raiz", str(raiz), "--json", str(js), "--md", str(tmp_path / "no" / "i.md"), "--auditoria", str(audit)]) == 2
    assert not js.exists() and audit.read_text(encoding="utf-8") == original
    assert not list(tmp_path.glob(".*.tmp"))


# ---------------------------------------------------------------- QA r01: H-07 (protecciones sin prueba)
def test_r02_filas_y_fichas_duplicadas_y_total(tmp_path):
    raiz = corpus_juguete(tmp_path, doc0=DOC0.replace("| R2 | Dos | — |", "| R2 | Dos | — |\n| R2 | Otra vez | — |"),
                          catalogo=CATALOGO.replace("Total: 4 fichas.", "Total: 5 fichas.")
                          + "\n### AA-ALFA-001 · Alfa repetida\n")
    inf = vi.verificar(raiz, codigo_juguete(fichas_catalogo=("AA-ALFA-001", "AA-ALFA-001", "AA-DELTA-002", "BB-REX-001")))
    assert _de(inf, "b", "FILA_DUPLICADA", "ERROR") == {"R2"}
    assert _de(inf, "d", "FICHA_DUPLICADA", "ERROR") == {"AA-ALFA-001"}
    assert _de(inf, "d", "TOTAL_DISTINTO", "ERROR") == {"Total"}
    assert _de(inf, "d", "FICHA_DUPLICADA_CODIGO", "ERROR") == {"AA-ALFA-001"}


def test_r02_ct_solo_en_canales_v6_o_campos_minimos(tmp_path):
    inf = vi.verificar(corpus_juguete(tmp_path), codigo_juguete(canales_v6=frozenset({"CT-08"}),
                                                                campos_minimos=frozenset({"CT-01", "CT-09"})))
    assert {"CT-08", "CT-09"} <= _de(inf, "a", "CT_SOLO_CODIGO", "ERROR")


def test_r02_alternativa_sin_ficha_y_referencia_definida_y_de_baja(tmp_path):
    archivos = dict(ARCHIVOS)
    archivos["Registro de Fuentes - V3.2.md"] += "| RF-0002 | Otra | Retirada | 2026-11-02 | — |\n"
    inf = vi.verificar(corpus_juguete(tmp_path, archivos_05=archivos), codigo_juguete(alternativas={"AA-ALFA-001": "ZZ-NO-001"}))
    assert _de(inf, "d", "ALTERNATIVA_SIN_FICHA", "ERROR") == {"ZZ-NO-001"}
    assert _de(inf, "e", "REF_DEFINIDA_Y_DE_BAJA", "AVISO") == {"RF-0002"}


def test_r02_versiones_escritas_en_los_py(tmp_path):
    paquete = tmp_path / "11_Ejecutor" / "paquete"
    paquete.mkdir(parents=True)
    (paquete / "a.py").write_text('X = {"catalog_version": "4.0"}\n', encoding="utf-8")
    (paquete / "b.py").write_text('"""Fichas del Catálogo de cálculos V4.0."""\nY = "catálogo v5.0"\n', encoding="utf-8")
    assert vi.versiones_en_py(paquete, tmp_path, tmp_path) == [("11_Ejecutor/paquete/a.py", 1, "4.0", True),
                                                               ("11_Ejecutor/paquete/b.py", 1, "4.0", False),
                                                               ("11_Ejecutor/paquete/b.py", 2, "5.0", False)]


def test_r02_el_paquete_real_no_escribe_otra_version_del_catalogo():
    codigo = vi.Codigo.desde_paquete(RAIZ_BLOQUE)
    assert codigo.versiones_en_codigo                                   # el escaneo encuentra las menciones a la vigente
    assert {v for _, _, v, _ in codigo.versiones_en_codigo} == {servicio.CATALOG_VERSION}


def test_r02_validar_informe_comprueba_errores_y_auditoria_marcas_repetidas(tmp_path, informe):
    roto = copy.deepcopy(informe)
    roto["errores"] += 1
    with pytest.raises(jsonschema.ValidationError):
        vi.validar_informe(roto)
    doc = tmp_path / "a.md"
    doc.write_text(f"{vi.MARCA_INICIO}\n{vi.MARCA_FIN}\n{vi.MARCA_INICIO}\n{vi.MARCA_FIN}\n", encoding="utf-8")
    with pytest.raises(vi.EntradaInvalida):
        vi.actualizar_auditoria(doc, "x")


def test_r02_orden_de_hallazgos_con_desempate_por_codigo(tmp_path):
    raiz = corpus_juguete(tmp_path, catalogo=CATALOGO.replace("| AA-BETA-001 | Beta | P1 | DOCUMENTADO |",
                                                               "| AA-BETA-001 | Beta | P1 | IMPLEMENTADO |"))
    beta = [h["codigo"] for h in vi.verificar(raiz, codigo_juguete())["hallazgos"]
            if h["id"] == "AA-BETA-001" and h["nivel"] == "ERROR"]
    assert beta == ["FALTA_EN_FICHAS_CATALOGO", "SOLO_CATALOGO"]       # se crean al revés; el orden es por código
