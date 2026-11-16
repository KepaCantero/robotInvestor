"""T-157 (Fase 0) · Verificador de consistencia de identificadores del Bloque A.

Un corpus de juguete con al menos un fallo de cada clase (a) a (f), los contextos que no son citas, el fallo cerrado, el
determinismo, el esquema del informe, la orden de consola y una pasada por el corpus y el código reales cuyas cifras se cuentan
aquí con código propio (no con el del verificador).
"""
import copy
import hashlib
import json
import re
import subprocess
import sys
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
La fase F0 no es un archivo. Aplica PS1 y PS3 (no existe).
Calcula con la ficha AA-ALFA-001, la AA-BETA-001 y la AA-GAMA-001 (no existe) del Catálogo V8.0.
Lee RF-0002, RF-0099 (no existe), RF-0003 (de baja), la tarjeta RF-1, TA-01 y TM-07 (no existe).
Filtro por códigos JEL (E43, R30, F31).
Pendiente `(F1 − F12) / F12`.
{"serie_ht01":"AA-SERIE-001","ficha_id":"AA-ZETA-001"}
"""

FUNCIONES = """# Funciones de juguete

| ID | Función | Salidas |
|---|---|---|
| MOT-F04 | Cuarta | Resultados de F04 |
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


def corpus_juguete(raiz: Path, doc0: str = DOC0, catalogo: str | None = CATALOGO) -> Path:
    archivos = {
        "01_Gobernanza/Documento 0 - Protocolo de prueba - V9.1.md": doc0,
        "02_System_prompts/System prompt - Motor de juguete - V9.0.md": PROMPT,
        "03_Funciones/Funciones – Motor de juguete.md": FUNCIONES,
        **{f"05_Archivos_operativos/{k}": v for k, v in ARCHIVOS.items()},
        # nada de esto se lee
        "99_Historico_V1.0/02_System_prompts/viejo.md": "Cita CT-99, R99, F99, PS99 y RF-9999.\n",
        "01_Gobernanza/99_Historico_V9.0/Documento 0 - viejo.md": "Cita CT-97.\n",
        "11_Ejecutor/README.md": "Cita CT-98.\n",
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
    assert _de(informe, "c", "F_INEXISTENTE", "ERROR") == {"F7"}        # F0 es una fase, F1 y F2 archivos (y fases)
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


def test_contextos_que_no_son_citas(informe):
    info = {(h["id"], h["mensaje"].split(" aparece como ")[1].split(":")[0]) for h in informe["hallazgos"]
            if h["codigo"] == "CITA_EN_CONTEXTO_AJENO"}
    assert ("R30", "código JEL de clasificación de la literatura económica") in info
    assert ("F31", "código JEL de clasificación de la literatura económica") in info
    assert ("F12", "notación dentro de una fórmula") in info
    assert ("F04", "abreviatura de la función MOT-F04 del mismo documento") in info
    assert ("AA-SERIE-001", "valor del campo JSON «serie_ht01», que no es el de una ficha") in info
    errores = {h["id"] for h in informe["hallazgos"] if h["nivel"] == "ERROR"}
    assert not errores & {"R30", "F31", "F12", "F04", "AA-SERIE-001"}


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
    assert not ids & {"CT-97", "CT-98", "CT-99", "R99", "F99", "PS99", "RF-9999"}
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


def test_documento_0_en_nfd_se_encuentra(tmp_path):
    raiz = corpus_juguete(tmp_path)
    viejo = raiz / "01_Gobernanza/Documento 0 - Protocolo de prueba - V9.1.md"
    viejo.rename(raiz / "01_Gobernanza" / "Documento 0 - Protocolo maestro - Versión óptima V9.1.md".replace("ó", "ó"))
    assert vi.verificar(raiz, codigo_juguete())["entradas"]["documento_0"]["version_nombre"] == "9.1"


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
