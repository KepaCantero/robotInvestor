"""Pruebas del gate tras quitar el Bloque A Forex (T-204, orden del operador del 25-11-2026: «olvídate del bloque A forex.
Elimínalo»).

- `tools/check_all.sh` y `tools/cuotas.txt` (y los scripts que enumeran los bloques: `preparar_entorno.sh`, `qa_rama.sh`,
  `corpus_integridad.py` y `requisitos_entorno.txt`) no vuelven a nombrar el Forex;
- el gate solo nombra bloques que existen, con sus cuotas y su configuración, y cuenta 10 comprobaciones (7 con `--core`):
  se ejecuta el `check_all.sh` real en una raíz temporal con herramientas falsas que anotan con qué se las llama;
- `preparar_entorno.sh` instala justo los ejecutores del gate y `qa_rama.sh` prueba justo sus paquetes;
- la prueba del gate `refs-vivas` (`prueba_refs_vivas.py`, con los casos del bloque retirado) pasa.
Uso: .venv/bin/python -m pytest -q .docs/scripts/pruebas_gate_bloques.py (lo ejecuta `pruebas_scripts.sh`)."""
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
CHECK_ALL = RAIZ / "tools" / "check_all.sh"
CUOTAS = RAIZ / "tools" / "cuotas.txt"
# Cualquier forma de nombrar el Bloque A Forex: la carpeta, el comando, «A Forex», «A-Forex», la abreviatura FX de las
# cuotas y los textos del gate («mypy FX», «FX ≥ 68», «bloque_a_fx»).
RE_FOREX = re.compile(r"forex|(?<![a-z0-9])fx(?![a-z0-9])|_fx(?![a-z0-9])", re.IGNORECASE)
SIN_FOREX = [CHECK_ALL, CUOTAS, RAIZ / ".docs" / "scripts" / "preparar_entorno.sh", RAIZ / ".docs" / "scripts" / "qa_rama.sh",
             RAIZ / "tools" / "corpus_integridad.py", RAIZ / "tools" / "requisitos_entorno.txt"]


def _lista_bash(texto: str, nombre: str) -> list[str]:
    m = re.search(rf"^{nombre}=\(([^)]*)\)", texto, re.MULTILINE)
    assert m, f"check_all.sh sin {nombre}=(…)"
    return m.group(1).split()


def _cuotas() -> dict[str, str]:
    return dict(l.split("=", 1) for l in CUOTAS.read_text(encoding="utf-8").splitlines() if l and not l.startswith("#"))


@pytest.mark.parametrize("ruta", SIN_FOREX, ids=lambda p: p.name)
def test_el_gate_y_sus_scripts_no_nombran_el_forex(ruta):
    lineas = [f"{i}: {l}" for i, l in enumerate(ruta.read_text(encoding="utf-8").splitlines(), 1) if RE_FOREX.search(l)]
    assert not lineas, f"{ruta.relative_to(RAIZ)} vuelve a nombrar el Bloque A Forex (eliminado con T-204): {lineas}"


@pytest.mark.parametrize("linea", [
    "EJECUTORES=(bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor)",
    'pytest_con_base "pytest bloque_a_forex"  "${EJECUTORES[1]}" "$(cuota pytest_bloque_a_forex)"',
    "mypy_bloque_a_forex=174", "pytest_bloque_a_forex=68", "-e bloque_a_forex/11_Ejecutor", "bloque-a-forex",
    "# 10-12. pytest ×3 (A ≥ 607 · FX ≥ 68 · B ≥ 174)", 'gate_cuota "mypy FX"', "mypy_bloque_a_fx=1", "Bloque A FOREX",
    "(arch 9.0.0 suma dos errores de mypy en A y en A-Forex)",
])
def test_el_detector_ve_las_formas_de_nombrar_el_forex(linea):
    assert RE_FOREX.search(linea)


@pytest.mark.parametrize("linea", ["EJECUTORES=(bloque_a/11_Ejecutor bloque_b/11_Ejecutor)", "mypy_bloque_b=159",
                                   "ruff=1604", "fix", "prefix", "FXA", "flujo"])
def test_el_detector_no_salta_con_lo_que_no_es_el_forex(linea):
    assert not RE_FOREX.search(linea)


def test_el_gate_solo_nombra_bloques_que_existen():
    texto = CHECK_ALL.read_text(encoding="utf-8")
    ejecutores, paquetes = _lista_bash(texto, "EJECUTORES"), _lista_bash(texto, "PAQUETES")
    assert ejecutores == ["bloque_a/11_Ejecutor", "bloque_b/11_Ejecutor"] and paquetes == ["bloque_a", "bloque_b"]
    for ej, paq in zip(ejecutores, paquetes, strict=True):
        assert ej == f"{paq}/11_Ejecutor" and (RAIZ / ej / paq / "__init__.py").is_file()
    configs = re.findall(r"'([^']+/config/por_defecto\.yaml)'", texto)
    assert configs == [f"{ej}/config/por_defecto.yaml" for ej in ejecutores]
    assert all((RAIZ / c).is_file() for c in configs)
    assert 'for i in "${!PAQUETES[@]}"; do' in texto           # el bucle de mypy sigue a la lista, sin índices fijos
    pytest_ = re.findall(r'^pytest_con_base "pytest (\S+)"\s+"\$\{EJECUTORES\[(\d)\]\}" "\$\(cuota pytest_(\S+)\)"', texto,
                         re.MULTILINE)
    assert pytest_ == [(p, str(i), p) for i, p in enumerate(paquetes)]


def test_las_cuotas_son_de_bloques_que_existen():
    paquetes = _lista_bash(CHECK_ALL.read_text(encoding="utf-8"), "PAQUETES")
    cuotas = _cuotas()
    por_bloque = {k for k in cuotas if k.startswith(("mypy_", "pytest_"))}
    assert {k.split("_", 1)[1] for k in por_bloque} <= set(paquetes)
    assert {f"pytest_{p}" for p in paquetes} <= por_bloque      # la línea base de pruebas no desaparece al llegar a 0
    assert set(cuotas) - por_bloque <= {"ruff"}
    assert all(v.isdigit() for v in cuotas.values())


HERRAMIENTA_FALSA = """#!/usr/bin/env bash
echo "$(basename "$0") $*" >> "$(dirname "$0")/llamadas.log"
case "$(basename "$0")" in
  ruff) exit 0 ;;
  mypy) exit 0 ;;
  pytest) d="${@: -1}"; n="$(grep -m1 "^$d=" "$(dirname "$0")/pasan.txt" | cut -d= -f2)"; echo "${n:-0} passed in 0.01s" ;;
esac
"""


def _raiz_falsa(tmp: Path, pasan: dict[str, int]) -> Path:
    (tmp / "tools").mkdir()
    shutil.copy(CHECK_ALL, tmp / "tools" / "check_all.sh")
    shutil.copy(CUOTAS, tmp / "tools" / "cuotas.txt")
    for f in ("corpus_integridad.py", "nfc_check.py", "secrets_scan.py", "refs_vivas.py"):
        (tmp / "tools" / f).write_text("print('ok')\n", encoding="utf-8")
    for ej in _lista_bash(CHECK_ALL.read_text(encoding="utf-8"), "EJECUTORES"):
        (tmp / ej / "config").mkdir(parents=True)
        (tmp / ej / "config" / "por_defecto.yaml").write_text("a: 1\n", encoding="utf-8")
    bin_ = tmp / ".venv" / "bin"
    bin_.mkdir(parents=True)
    (bin_ / "python").write_text(f'#!/usr/bin/env bash\nexec "{sys.executable}" "$@"\n', encoding="utf-8")
    (bin_ / "python").chmod(0o755)
    for h in ("ruff", "mypy", "pytest"):
        (bin_ / h).write_text(HERRAMIENTA_FALSA, encoding="utf-8")
        (bin_ / h).chmod(0o755)
    (bin_ / "pasan.txt").write_text("".join(f"{d}={n}\n" for d, n in pasan.items()), encoding="utf-8")
    return tmp


def _gate(raiz: Path, *args: str) -> tuple[int, str, list[str]]:
    r = subprocess.run(["bash", str(raiz / "tools" / "check_all.sh"), *args], capture_output=True, text=True, cwd=raiz,
                       check=False)
    log = raiz / ".venv" / "bin" / "llamadas.log"
    return r.returncode, r.stdout + r.stderr, log.read_text(encoding="utf-8").splitlines() if log.exists() else []


def _bases() -> dict[str, int]:
    c = _cuotas()
    return {"bloque_a/11_Ejecutor": int(c["pytest_bloque_a"]), "bloque_b/11_Ejecutor": int(c["pytest_bloque_b"])}


def test_el_gate_completo_son_diez_comprobaciones_sobre_a_y_b(tmp_path):
    codigo, salida, llamadas = _gate(_raiz_falsa(tmp_path, _bases()))
    assert codigo == 0, salida
    assert "Gates ejecutados: 10" in salida and "Pasaron: 10" in salida and "Fallaron: 0" in salida
    assert sorted(l for l in llamadas if l.startswith("mypy")) == [
        "mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a",
        "mypy --ignore-missing-imports --no-error-summary bloque_b/11_Ejecutor/bloque_b"]
    assert [l for l in llamadas if l.startswith("pytest")] == ["pytest -q bloque_a/11_Ejecutor", "pytest -q bloque_b/11_Ejecutor"]
    assert [l for l in llamadas if l.startswith("ruff")] == [
        "ruff check --output-format=concise bloque_a/11_Ejecutor bloque_b/11_Ejecutor"]
    assert "ok bloque_a/11_Ejecutor/config/por_defecto.yaml" in salida and "ok bloque_b/11_Ejecutor/config/por_defecto.yaml" in salida


def test_el_gate_core_son_siete_comprobaciones(tmp_path):
    codigo, salida, llamadas = _gate(_raiz_falsa(tmp_path, _bases()), "--core")
    assert codigo == 0, salida
    assert "Gates ejecutados: 7" in salida and "Pasaron: 7" in salida
    assert not [l for l in llamadas if l.startswith(("ruff", "mypy"))]


@pytest.mark.parametrize("bloque", ["bloque_a/11_Ejecutor", "bloque_b/11_Ejecutor"])
def test_cada_bloque_se_mide_con_su_propia_linea_base(tmp_path, bloque):
    pasan = _bases()
    pasan[bloque] -= 1                                    # una prueba menos que su línea base: el gate falla por ese bloque
    codigo, salida, _ = _gate(_raiz_falsa(tmp_path, pasan))
    assert codigo == 1 and "Fallaron: 1" in salida
    paq = bloque.split("/")[0]
    assert f"pytest {paq}: {pasan[bloque]} < base {pasan[bloque] + 1}" in re.sub(r"\x1b\[[0-9;]*m", "", salida)


PYTHON_FALSO = """#!/usr/bin/env bash
echo "$*" >> "$(dirname "$0")/llamadas.log"
if [[ "$1" == "-c" ]]; then echo "3.12"; exit 0; fi
if [[ "$1 $2 $3" == "-m pip --version" ]]; then echo "pip 24.0"; exit 0; fi
if [[ "$1 $2 $3" == "-m pip freeze" ]]; then echo "numpy==2.1.0"; exit 0; fi
if [[ "$1 $2 $3" == "-m pip install" ]]; then exit 0; fi
if [[ "$1" == "-I" ]]; then shift; exec python3 -I "$@"; fi
exec python3 "$@"
"""


def test_preparar_entorno_instala_justo_los_ejecutores_del_gate(tmp_path):
    (tmp_path / ".docs" / "scripts").mkdir(parents=True)
    for f in ("preparar_entorno.sh", "common.sh"):
        shutil.copy(RAIZ / ".docs" / "scripts" / f, tmp_path / ".docs" / "scripts" / f)
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools" / "requisitos_entorno.txt").write_text("numpy==2.1.0\n", encoding="utf-8")
    bin_ = tmp_path / ".venv" / "bin"
    bin_.mkdir(parents=True)
    (bin_ / "python").write_text(PYTHON_FALSO, encoding="utf-8")
    (bin_ / "python").chmod(0o755)
    r = subprocess.run(["bash", str(tmp_path / ".docs" / "scripts" / "preparar_entorno.sh")], capture_output=True, text=True,
                       cwd=tmp_path, check=False)
    assert r.returncode == 0, r.stdout + r.stderr
    instalar = [l.split() for l in (bin_ / "llamadas.log").read_text(encoding="utf-8").splitlines() if l.startswith("-m pip install")]
    assert len(instalar) == 1
    editables = [instalar[0][i + 1] for i, a in enumerate(instalar[0]) if a == "-e"]
    assert editables == _lista_bash(CHECK_ALL.read_text(encoding="utf-8"), "EJECUTORES")


def test_qa_rama_prueba_justo_los_paquetes_del_gate():
    m = re.search(r"^for ej in ([^;]+); do", (RAIZ / ".docs" / "scripts" / "qa_rama.sh").read_text(encoding="utf-8"), re.MULTILINE)
    assert m and m.group(1).split() == _lista_bash(CHECK_ALL.read_text(encoding="utf-8"), "PAQUETES")


def test_la_prueba_de_refs_vivas_pasa_con_los_casos_del_bloque_retirado():
    r = subprocess.run([sys.executable, "-I", str(RAIZ / ".docs" / "scripts" / "prueba_refs_vivas.py")], capture_output=True,
                       text=True, check=False)
    assert r.returncode == 0, r.stdout
    assert "bloque retirado: carpeta sola falla" in r.stdout and "bloque retirado: en un ticket pasa" in r.stdout


# --- r02 (QA r01 de T-204) ---------------------------------------------------------------------------------------------

def _leer(rel: str) -> str:
    return (RAIZ / rel).read_text(encoding="utf-8")


def test_h01_avance_no_da_por_aplicada_otra_version_de_la_constitucion():
    const = re.search(r"— (V\d+\.\d+)", _leer("sistema_global/constitucion/Constitucion_Global.md").splitlines()[0]).group(1)
    assert all(v == const for v in re.findall(r"Constitución pasa a la (V\d+\.\d+)", _leer("docs/AVANCE.md")))
    assert "la enmienda de la Constitución queda propuesta, sin aplicar (INC-T204-01)" in _leer("docs/AVANCE.md") or const != "V0.6"


@pytest.mark.parametrize("ruta", [".agents/skills/ri-probar/SKILL.md", "CLAUDE.md"])
def test_h04_las_lineas_base_citadas_son_las_de_cuotas(ruta):
    c = _cuotas()
    base = {"A": c["pytest_bloque_a"], "B": c["pytest_bloque_b"]}
    citadas = re.findall(r"\b([AB]) ≥ (\d+)", _leer(ruta))
    assert citadas and all(n == base[b] for b, n in citadas), citadas


def test_h05_hallazgos_de_secrets_baseline_y_gates_del_pre_commit():
    import json
    n = sum(len(v) for v in json.loads(_leer(".secrets.baseline"))["results"].values())
    citados = re.findall(r"\.secrets\.baseline` \((\d+) hallazgos", _leer("CLAUDE.md"))
    assert citados and all(int(x) == n for x in citados), (citados, n)
    gates = re.findall(r"\((\d+) gates\)", _leer(".pre-commit-config.yaml"))
    assert gates == ["10"]


RUFF = RAIZ / ".venv" / "bin" / "ruff"


@pytest.mark.skipif(not RUFF.exists(), reason="sin .venv/bin/ruff")
def test_h07_la_cuota_de_ruff_es_la_medida_como_el_gate():
    ejecutores = _lista_bash(CHECK_ALL.read_text(encoding="utf-8"), "EJECUTORES")
    r = subprocess.run([str(RUFF), "check", "--output-format=concise", *ejecutores], cwd=RAIZ, capture_output=True, text=True,
                       check=False)
    assert int(_cuotas()["ruff"]) == r.stdout.count("\n")   # igual que `… | wc -l` del gate: la cuota baja a lo que mide


def test_h08_inc_t204_04_cita_todo_lo_que_nombra_el_forex_en_a_y_b():
    texto = _leer("docs/incidencias.md")
    inc = texto[texto.index("**INC-T204-04"):]
    inc = inc[:inc.find("\n**INC-", 1)] if "\n**INC-" in inc[1:] else inc
    r = subprocess.run(["git", "grep", "-l", "-I", "-E", "A Forex|A-Forex|F9 Forex", "--", "bloque_a", "bloque_b",
                        ":!*99_Historico*"], cwd=RAIZ, capture_output=True, text=True, check=False)
    ficheros = [l.strip('"') for l in r.stdout.splitlines() if l]
    if any("\\" in f for f in ficheros):             # git cita los nombres no ASCII: se leen sin comillas
        r = subprocess.run(["git", "-c", "core.quotePath=false", "grep", "-l", "-I", "-E", "A Forex|A-Forex|F9 Forex", "--",
                            "bloque_a", "bloque_b", ":!*99_Historico*"], cwd=RAIZ, capture_output=True, text=True, check=False)
        ficheros = [l for l in r.stdout.splitlines() if l]
    assert ficheros
    faltan = [f for f in ficheros if f"`{f}`" not in inc]
    assert not faltan, faltan


def _limpiar():
    import importlib.util
    spec = importlib.util.spec_from_file_location("limpiar_docs_t204", RAIZ / ".docs" / "tickets" / "T-204" / "limpiar_docs.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.limpiar


@pytest.mark.parametrize("linea", [
    "| `bloque_a_forex/` | Eliminado el 25-11-2026 por orden del operador (T-204) |",
    "- Gate completo 12/12: A 439 (nueva línea base), A-Forex 68 y B 176; ruff baja a 3072 y mypy de A queda en 115.",
    "Gate `./tools/check_all.sh`: 12 de 12 en verde. Las cuotas: ruff 3086 de 3109; mypy A 123, A-Forex 174 y B 159.",
    "| pytest bloque_a · bloque_a_forex · bloque_b | ✓ 326 · 68 · 176 passed |",
    "- mypy A, A-Forex y B;",
    "Resultado completo: A 58, Forex 68, B 142 (134 previas y ocho nuevas). Los doce controles del repositorio pasaron.",
    "Observaciones: **O-1** el mismo patrón antiguo sigue en el Forex (declarado en «No entra»).",
    "  - **Bloque A Forex V1.1**;",
    # r03 (QA r02, H-11): evidencia que la r02 no reconocía
    "- `./tools/check_all.sh --core` en verde (8/8): corpus íntegro (705 archivos), nombres NFC, YAML, secretos, refs vivas y "
    "las tres suites (A 8 272 pasadas, A-Forex 68, B 176; ninguna por debajo de su línea base).",
    "con el `.venv` del proyecto enlazado y `PYTHONPATH` apuntando a los tres ejecutores de la extracción (comprobado que "
    "`bloque_a`, `bloque_a_forex` y `bloque_b` se importan de ahí).",
    "| Inventario | búsqueda propia de `sleep` y `Event` en las tres suites | A-Forex y B: nada. A: ningún `perf_counter` |",
    "Gate: 11 de 12 en verde; falla A-Forex por un fichero de los tres bloques.",
    "Resultado: A 300 pasadas, A-Forex 68 y B 174.",
    # cierre de la QA r03 (H-14): mayúsculas y recuento que sigue a su «mypy» en otra línea
    "  - Pytest: A 8415 (antes 8400), FX 68, B 176.",
    "  - Mypy: A 102, FX 174, B 159, todos en su cuota.",
    "  T-201 sola), A-Forex 174, B 159. **Equivalencia** de la combinación contra la base: **IGUALES** (90 ficheros).",
    "  - Pytest: A 8415 (antes 8400), A-Forex 68 y B 176.",      # solo la regla de mayúsculas la protege (M40)
    "  - RUFF de los tres ejecutores 2807; A-Forex sin tocar y B sin tocar.",
])
def test_h03_limpiar_conserva_la_marca_la_evidencia_y_las_citas(linea):
    nuevo, cambios = _limpiar()(linea)
    assert nuevo == linea and not cambios


def test_h03_limpiar_borra_lo_que_solo_habla_del_forex_y_recorta_lo_mixto():
    limpiar = _limpiar()
    nuevo, cambios = limpiar("Antes.\n- El Bloque A Forex queda para T-115.\nDespués.")
    assert nuevo == "Antes.\nDespués." and len(cambios) == 1 and "BORRADA" in cambios[0]
    nuevo, cambios = limpiar("Sin comprobar: el gate entero y las suites de A-Forex y B (fuera del encargo).")
    assert nuevo == "Sin comprobar: el gate entero y la suite de B (fuera del encargo)." and "AHORA" in cambios[0]
    nuevo, _ = limpiar("```\nexport PYTHONPATH=$W/bloque_a_forex/11_Ejecutor\n```")
    assert "bloque_a_forex" in nuevo                       # dentro de un bloque de código, literal


def test_h03_limpiar_no_entra_en_los_encargos_ni_en_el_ticket():
    import importlib.util
    spec = importlib.util.spec_from_file_location("limpiar_docs_t204b", RAIZ / ".docs" / "tickets" / "T-204" / "limpiar_docs.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    docs = [p.relative_to(RAIZ).as_posix() for p in mod._documentos()]
    assert docs and not [d for d in docs if "encargo_revision_astra" in d or d.startswith((".docs/tickets/T-204/", ".docs/scripts/"))]


def _version_constitucion() -> tuple[int, int]:
    m = re.search(r"— V(\d+)\.(\d+)", _leer("sistema_global/constitucion/Constitucion_Global.md").splitlines()[0])
    assert m, "la cabecera de la Constitución no dice su versión"
    return int(m.group(1)), int(m.group(2))


def test_h02_la_enmienda_6_de_la_constitucion():
    """V0.6: el parche guardado es el que se genera. Desde la V0.7, con la enmienda 6 aplicada (r02b, «Todo»), invariantes
    del contenido, no el parche, para que una enmienda posterior legítima no la rompa (QA r02, H-10)."""
    const = _leer("sistema_global/constitucion/Constitucion_Global.md")
    if _version_constitucion() >= (0, 7):
        lineas = const.splitlines()
        enm = next(l for l in lineas if l.startswith("**Enmiendas.**"))
        assert "**enmienda 6** (T-204)" in enm
        d48 = [l for l in lineas if l.startswith("| D-48 |")]
        assert len(d48) == 1 and "Enmienda 6" in d48[0] and "Bloque A Forex" in d48[0]
        # el cambio 17, solo en la tabla «Qué cambia respecto a la V0.1» del §0 (la de riesgos del §15 también numera filas)
        s0 = lineas[:next(i for i, l in enumerate(lineas) if l.startswith("## 1."))]
        for fila, donde in (("| D-20 |", lineas), ("| 17 |", s0)):
            f = [l for l in donde if l.startswith(fila)]
            assert len(f) == 1 and "enmienda 6, D-48" in f[0] and "A Forex" not in f[0], fila
        sueltas = [l for l in lineas if re.search(r"(?i)\bA[- ]Forex\b", l) and "enmienda 6" not in l.lower()
                   and not l.startswith("| 43 |")]
        assert not sueltas, sueltas                     # el A Forex solo en las líneas que describen la enmienda 6
        return
    assert const.startswith("# Constitución Global del Robot Inversor — V0.6")
    r = subprocess.run([sys.executable, "-I", str(RAIZ / ".docs" / "tickets" / "T-204" / "generar_enmienda.py"), "--comprobar"],
                       cwd=RAIZ, capture_output=True, text=True, check=False)
    assert r.returncode == 0, r.stdout
    parche = _leer(".docs/tickets/T-204/enmienda4_constitucion.patch")
    assert "**enmienda 6**" in parche and "**enmienda 4**" not in parche and "+Nov 25, 2026 ·" in parche


def test_h09_los_documentos_vivos_dicen_el_estado_aplicado():
    v = "V%d.%d" % _version_constitucion()
    assert re.findall(r"Constitución global \((V\d+\.\d+) desde", _leer("sistema_global/README.md")) == [v]
    if _version_constitucion() >= (0, 7):
        fila = next(l for l in _leer("sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md").splitlines()
                    if l.startswith("| T-204 |"))
        memoria = _leer(".docs/memoria/compartida/2026-11-25_bloque-a-forex-eliminado.md")
        for nombre, texto in (("fila T-204", fila), ("memoria", memoria)):
            assert not re.search(r"(?i)Pendiente del operador|no se ha tocado|solo propone|sin aplicar", texto), nombre
        t54 = next(l for l in _leer("sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md").splitlines()
                   if l.startswith("| T-54 |"))
        assert "A Forex y B Forex fuera" not in t54 or "enmienda 6, D-48" in t54   # cierre de la QA r03, H-13
