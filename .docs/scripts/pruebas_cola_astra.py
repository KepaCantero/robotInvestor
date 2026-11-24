"""Pruebas de `cola_astra.py` (T-194) con una cola de prueba propia, en un repositorio git temporal.

Cada prueba crea un repositorio nuevo en `tmp_path`, copia allí `cola_astra.py` (o el mutante que diga
`COLA_ASTRA_SCRIPT`) y escribe una cola mínima con sus filas. No leen la cola real
(`.docs/tickets/_relevo/cola_astra.md`) ni tocan el árbol de trabajo: si la cola real cambia, estas pruebas no se
desfasan. La fecha de la cola (`FECHA_COLA`) se lee del script; los días de EN CURSO y la sección del rediseño de B,
no: son la regla documentada.
Uso: python -m pytest -q .docs/scripts/pruebas_cola_astra.py (lo ejecuta pruebas_scripts.sh).
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent
SCRIPT = Path(os.environ.get("COLA_ASTRA_SCRIPT") or SCRIPTS / "cola_astra.py")
COLA = ".docs/tickets/_relevo/cola_astra.md"
GENERICO = ("Claude", "noreply@anthropic.com")
PERSONAL = ("Persona Prueba", "persona@equipo-" + "local.invalid")   # ficticio, partido en dos cadenas

# La cola de prueba: (id, tipo, entregable). C-02 es la revisión de B, la que pide la sección «Rediseño».
FILAS = [
    ("C-01", "REVISION", "`.docs/diseno/bloque_a/revision_astra.md`"),
    ("C-02", "REVISION", "`.docs/diseno/bloque_b/revision_astra.md`"),
    ("C-03", "REVISION", "`.docs/diseno/bloque_c/revision_astra.md`"),
    ("C-04", "REVISION", "`.docs/diseno/bloque_d/revision_astra.md`"),
    ("C-05", "REVISION", "«.docs/diseno/bloque_e/revision_astra.md»"),
    ("C-06", "REVISION", "«.docs/diseno/bloque_f/revision_astra.md»"),
    ("C-07", "QA", "«.docs/tickets/T-90/qa.md»"),
    ("C-08", "IMPLEMENTAR", "«.docs/tickets/T-91/README.md»"),
]


def _modulo():
    spec = importlib.util.spec_from_file_location("cola_astra_t194", SCRIPT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _entorno(**extra):
    """El entorno del proceso sin GIT_AUTOR_* ni variables GIT_ que desvíen git a otro repositorio."""
    e = {k: v for k, v in os.environ.items() if not k.startswith(("GIT_AUTOR_", "GIT_"))}
    e.update({"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull}, **extra)
    return e


class Repo:
    """Un repositorio temporal con la cola de prueba; `correr()` ejecuta el script como lo haría Astra."""

    def __init__(self, raiz: Path):
        self.raiz = raiz
        self.estados = {i: "PENDIENTE" for i, _, _ in FILAS}
        raiz.mkdir()
        self.git("init", "-q")
        self.git("config", "user.name", GENERICO[0])
        self.git("config", "user.email", GENERICO[1])
        self.git("config", "commit.gpgsign", "false")
        (raiz / ".docs/scripts").mkdir(parents=True)
        (raiz / ".docs/tickets/_relevo").mkdir(parents=True)
        shutil.copy(SCRIPT, raiz / ".docs/scripts/cola_astra.py")
        self.escribir_cola()
        self.commit("cola")

    def git(self, *args, fecha=None):
        extra = {"GIT_COMMITTER_DATE": fecha, "GIT_AUTHOR_DATE": fecha} if fecha else {}
        r = subprocess.run(["git", *args], cwd=self.raiz, capture_output=True, text=True, env=_entorno(**extra), check=False)
        assert r.returncode == 0, r.stderr
        return r.stdout

    def escribir_cola(self, extra=""):
        lineas = ["# Cola de prueba", "", "| # | Tarea | Tipo | Encargo o ticket | Entregable | Estado | Commit | Nota |",
                  "| --- | --- | --- | --- | --- | --- | --- | --- |"]
        for i, tipo, entregable in FILAS:
            lineas.append(f"| {i} | Tarea {i} | {tipo} | encargo | {entregable} | {self.estados[i]} | | nota de {i} |")
        (self.raiz / COLA).write_text("\n".join(lineas) + "\n" + extra, encoding="utf-8")

    def estado(self, **cambios):
        for k, v in cambios.items():
            self.estados[k.replace("_", "-")] = v
        self.escribir_cola()
        self.commit("estados")

    def escribir(self, ruta, texto, commit=True, fecha=None):
        p = self.raiz / ruta
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(texto, encoding="utf-8")
        if commit:
            self.commit(f"escribe {ruta}", fecha=fecha)

    def commit(self, msg, fecha=None):
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", msg, fecha=fecha)

    def correr(self, *args, **env):
        r = subprocess.run([sys.executable, "-I", ".docs/scripts/cola_astra.py", *args], cwd=self.raiz,
                           capture_output=True, text=True, env=_entorno(**env), check=False)
        assert not r.stderr, r.stderr
        return r.returncode, r.stdout


@pytest.fixture
def repo(tmp_path):
    return Repo(tmp_path / "repo")


def _avisos(out):
    return [l for l in out.splitlines() if l.startswith("AVISO")]


def _errores(out):
    return [l for l in out.splitlines() if l.startswith("ERROR")]


# --- Las comprobaciones de siempre ------------------------------------------------------------------------------

def test_cola_limpia_sin_errores_y_la_siguiente_es_la_primera_pendiente(repo):
    rc, out = repo.correr()
    assert rc == 0 and not _errores(out) and not _avisos(out), out
    assert "Siguiente: C-01 · Tarea C-01 · entregable .docs/diseno/bloque_a/revision_astra.md" in out
    assert "Cola de Astra: 0 hechas, 0 en curso, 8 pendientes, 0 bloqueadas, 0 retiradas (de 8)" in out


def test_hecha_sin_entregable_es_error(repo):
    repo.estado(C_01="HECHA")
    rc, out = repo.correr()
    assert rc == 1 and re.search(r"^ERROR\s+C-01 \(Tarea C-01\): marcada HECHA pero el entregable no existe$", out, re.MULTILINE), out


def test_hecha_con_un_borrador_es_error(repo):
    repo.estado(C_01="HECHA")
    repo.escribir(".docs/diseno/bloque_a/revision_astra.md", "  borrador, sigue en la próxima sesión\n")
    rc, out = repo.correr()
    assert rc == 1 and re.search(r"^ERROR\s+C-01 .*el entregable es un borrador$", out, re.MULTILINE), out


def test_hecha_con_el_entregable_no_da_error_y_pasa_a_la_siguiente(repo):
    repo.estado(C_01="HECHA")
    repo.escribir(".docs/diseno/bloque_a/revision_astra.md", "# Revisión de A\n\nResumen; no es un BORRADOR.\n")
    rc, out = repo.correr()
    assert rc == 0 and not _errores(out) and not _avisos(out), out
    assert "1 hechas" in out and "Siguiente: C-02" in out


def test_hecha_con_el_entregable_sin_commit_es_error(repo):
    repo.estado(C_01="HECHA")
    repo.escribir(".docs/diseno/bloque_a/revision_astra.md", "# Revisión de A\n", commit=False)
    rc, out = repo.correr()
    assert rc == 1 and re.search(r"^ERROR\s+C-01 .*el entregable no está en git$", out, re.MULTILINE), out


def test_entregable_sin_marcar_hecha_es_aviso(repo):
    repo.escribir(".docs/diseno/bloque_c/revision_astra.md", "# Revisión de C\n")
    rc, out = repo.correr()
    assert rc == 0 and not _errores(out), out
    commit = repo.git("log", "-1", "--format=%h").strip()
    assert _avisos(out) == [f"AVISO  C-03 (Tarea C-03): el entregable ya está ({commit}) pero la tarea no está marcada HECHA"], out


def test_la_revision_de_b_sin_la_seccion_del_rediseno_es_error(repo):
    repo.estado(C_02="HECHA")
    repo.escribir(".docs/diseno/bloque_b/revision_astra.md", "# Revisión de B\n\nSin la sección.\n")
    rc, out = repo.correr()
    assert rc == 1 and re.search(r"^ERROR\s+C-02 .*falta la sección «Rediseño»$", out, re.MULTILINE), out
    repo.escribir(".docs/diseno/bloque_b/revision_astra.md", "# Revisión de B\n\n## Rediseño\n\nPropuesta.\n")
    rc, out = repo.correr()
    assert rc == 0 and not _errores(out), out


def test_la_seccion_del_rediseno_solo_la_pide_la_revision_de_b(repo):
    repo.estado(C_03="HECHA")
    repo.escribir(".docs/diseno/bloque_c/revision_astra.md", "# Revisión de C\n\nSin rediseño.\n")
    rc, out = repo.correr()
    assert rc == 0 and not _errores(out), out


def test_en_curso_viejo_es_aviso_y_es_la_siguiente(repo):
    repo.estado(C_04="EN CURSO 2026-01-01")
    rc, out = repo.correr()
    assert rc == 0, out
    assert "AVISO  C-04 (Tarea C-04): EN CURSO desde 2026-01-01; ¿trabajo abandonado? Nota: nota de C-04" in out
    assert "Siguiente: C-04" in out and "1 en curso" in out


def test_en_curso_el_limite_de_tres_dias(repo):
    """«Más de 3 días»: hace 3 días no avisa; hace 4, sí. Una fecha futura tampoco avisa."""
    hoy = date.today()
    repo.estado(C_03=f"EN CURSO {hoy - timedelta(days=3)}")
    _, out = repo.correr()
    assert "abandonado" not in out and "Siguiente: C-03" in out, out
    repo.estado(C_03=f"EN CURSO {hoy - timedelta(days=4)}")
    _, out = repo.correr()
    assert re.search(r"^AVISO\s+C-03 .*abandonado", out, re.MULTILINE), out
    repo.estado(C_03="EN CURSO 2099-01-01")
    _, out = repo.correr()
    assert "abandonado" not in out, out


def test_en_curso_sin_fecha_es_aviso(repo):
    repo.estado(C_03="EN CURSO")
    _, out = repo.correr()
    assert "AVISO  C-03: EN CURSO sin fecha" in out and "Siguiente: C-03" in out, out


def test_dos_en_curso_a_la_vez_es_aviso_y_manda_la_primera(repo):
    repo.estado(C_04="EN CURSO 2026-01-01", C_05="EN CURSO 2099-01-01")
    _, out = repo.correr()
    assert "AVISO  hay 2 tareas EN CURSO a la vez: C-04, C-05" in out and "Siguiente: C-04" in out, out
    repo.estado(C_04="PENDIENTE")
    _, out = repo.correr()
    assert "tareas EN CURSO a la vez" not in out and "Siguiente: C-05" in out, out


def test_cambios_sin_commit_en_un_entregable_es_aviso(repo):
    repo.estado(C_04="EN CURSO 2099-01-01")
    repo.escribir(".docs/diseno/bloque_d/revision_astra.md", "BORRADOR, sigue en la próxima sesión\n")
    _, out = repo.correr()
    assert "sin commit" not in out, out
    repo.escribir(".docs/diseno/bloque_d/revision_astra.md", "BORRADOR, más\n", commit=False)
    _, out = repo.correr()
    assert "AVISO  C-04: el entregable tiene cambios sin commit (trabajo sin subir)" in out, out


def test_un_entregable_nuevo_sin_anadir_en_una_carpeta_con_commit_es_aviso(repo):
    repo.escribir(".docs/diseno/bloque_d/otra.md", "# otra\n")
    repo.escribir(".docs/diseno/bloque_d/revision_astra.md", "# a medias\n", commit=False)
    _, out = repo.correr()
    assert "AVISO  C-04: el entregable tiene cambios sin commit (trabajo sin subir)" in out, out


def test_un_entregable_nuevo_sin_anadir_en_una_carpeta_nueva_es_aviso(repo):
    repo.escribir(".docs/diseno/bloque_d/revision_astra.md", "# a medias\n", commit=False)
    _, out = repo.correr()
    assert "AVISO  C-04: el entregable tiene cambios sin commit (trabajo sin subir)" in out, out


def _fecha_cola(dias=0):
    return (date.fromisoformat(_modulo().FECHA_COLA) + timedelta(days=dias)).isoformat() + "T12:00:00"


def test_qa_marcada_con_un_qa_md_anterior_a_la_cola_es_error(repo):
    repo.escribir(".docs/tickets/T-90/qa.md", "# QA\n\n## Veredicto\n\n**APTO**\n", fecha=_fecha_cola(-1))
    repo.estado(C_07="HECHA")
    rc, out = repo.correr()
    dia = _fecha_cola(-1)[:10]
    assert rc == 1 and re.search(rf"^ERROR\s+C-07 .*el entregable no ha cambiado desde la cola \({dia}\)$", out, re.MULTILINE), out


def test_qa_del_mismo_dia_de_la_cola_cuenta(repo):
    repo.escribir(".docs/tickets/T-90/qa.md", "# QA\n\n## Veredicto\n\n**NO APTO**\n", fecha=_fecha_cola(0))
    repo.estado(C_07="HECHA")
    rc, out = repo.correr()
    assert rc == 0 and not _errores(out), out


@pytest.mark.parametrize("texto", [
    "# QA\n\n## Veredicto\n\nAPTO / NO APTO\n\n**APTO**\n",   # la plantilla sin rellenar
    "# QA\n\nSin la sección.\n\n**APTO**\n",
    "# QA\n\n## Veredicto\n\n**APTO**\n\n## Veredicto r02\n\npendiente\n",   # cuenta el último veredicto
], ids=["plantilla", "sin_seccion", "ultimo_sin_rellenar"])
def test_qa_sin_veredicto_rellenado_es_error(repo, texto):
    repo.escribir(".docs/tickets/T-90/qa.md", texto)
    repo.estado(C_07="HECHA")
    rc, out = repo.correr()
    assert rc == 1 and re.search(r"^ERROR\s+C-07 .*sin veredicto rellenado$", out, re.MULTILINE), out


def test_qa_con_veredicto_sin_marcar_es_aviso(repo):
    repo.escribir(".docs/tickets/T-90/qa.md", "# QA r01\n\n## Veredicto\n\n**NO APTO**\n")
    _, out = repo.correr()
    assert re.search(r"^AVISO\s+C-07 .*no está marcada HECHA$", out, re.MULTILINE), out


@pytest.mark.parametrize("estado,hecha", [("EN QA (r01)", True), ("CERRADO (QA APTO)", True), ("EN CURSO", False)])
def test_implementar_cuenta_por_el_estado_del_ticket(repo, estado, hecha):
    repo.escribir(".docs/tickets/T-91/README.md", f"# T-91\n\n| Campo | Valor |\n| --- | --- |\n| Estado | {estado} |\n")
    repo.estado(C_08="HECHA")
    rc, out = repo.correr()
    if hecha:
        assert rc == 0 and not _errores(out), out
    else:
        assert rc == 1 and re.search(rf"^ERROR\s+C-08 .*estado del ticket «{estado}»$", out, re.MULTILINE), out


def test_retirada_con_entregable_no_avisa(repo):
    repo.escribir(".docs/diseno/bloque_c/revision_astra.md", "# Revisión de C\n")
    repo.estado(C_03="RETIRADA")
    rc, out = repo.correr()
    assert rc == 0 and not _avisos(out) and not _errores(out), out


def test_retirada_no_es_la_siguiente_y_se_cuenta(repo):
    repo.estado(C_01="RETIRADA", C_02="RETIRADA", C_03="BLOQUEADA")
    _, out = repo.correr()
    assert "Siguiente: C-04" in out and "2 retiradas" in out and "1 bloqueadas" in out and "5 pendientes" in out, out
    assert not _avisos(out), out


def test_sin_pendientes_no_hay_siguiente(repo):
    repo.estado(**{i.replace("-", "_"): "RETIRADA" for i, _, _ in FILAS})
    rc, out = repo.correr()
    assert rc == 0 and "Siguiente: nada pendiente" in out and "8 retiradas" in out, out


@pytest.mark.parametrize("estado", ["LISTA", "HECHO", "EN CURSO ayer"])
def test_estado_desconocido_es_aviso(repo, estado):
    repo.estado(C_06=estado)
    _, out = repo.correr()
    assert f"AVISO  C-06: estado desconocido «{estado}»" in out, out


def test_una_fila_con_columnas_de_menos_es_error(repo):
    repo.escribir_cola(extra="| C-09 | Tarea rota | REVISION | `x.md` | PENDIENTE |\n")
    repo.commit("fila rota")
    rc, out = repo.correr()
    assert rc == 1 and "ERROR  C-09: la fila tiene 5 columnas y no 8" in out, out


def test_json_da_la_cuenta_la_siguiente_y_los_errores(repo):
    repo.estado(C_01="HECHA", C_04="EN CURSO 2026-01-01")
    rc, out = repo.correr("--json")
    d = json.loads(out)
    assert rc == 1
    assert d["cuenta"] == {"HECHA": 1, "EN CURSO": 1, "PENDIENTE": 6, "BLOQUEADA": 0, "RETIRADA": 0}
    assert d["siguiente"] == {"id": "C-04", "tarea": "Tarea C-04", "entregable": ".docs/diseno/bloque_d/revision_astra.md"}
    assert len(d["errores"]) == 1 and d["errores"][0].startswith("C-01 ") and any("abandonado" in a for a in d["avisos"])


def test_los_dias_de_en_curso_son_los_del_docstring():
    m = _modulo()
    assert m.DIAS_EN_CURSO == 3 and "más de 3 días" in m.__doc__


# --- Autor genérico: lo que no cubre pruebas_autor_generico.py (allí, autor_efectivo con git simulado y main con
# --- el entorno). Aquí, el script entero sobre un repositorio de verdad: su git config, su .env y la salida --json.

def test_con_el_autor_generico_del_git_config_no_hay_error_de_autor(repo):
    rc, out = repo.correr()
    assert rc == 0 and "autor" not in out, out


@pytest.mark.parametrize("nombre,correo", [PERSONAL, (PERSONAL[0], GENERICO[1]), (GENERICO[0], PERSONAL[1])],
                         ids=["los_dos", "solo_el_nombre", "solo_el_correo"])
def test_un_git_config_personal_es_error_sin_repetirlo(repo, nombre, correo):
    repo.git("config", "user.name", nombre)
    repo.git("config", "user.email", correo)
    rc, out = repo.correr()
    assert rc == 1 and re.search(r"^ERROR\s+autor de los commits no genérico", out, re.MULTILINE), out
    assert PERSONAL[0] not in out and PERSONAL[1] not in out
    rc, out = repo.correr("--json")
    d = json.loads(out)
    assert rc == 1 and [e for e in d["errores"] if e.startswith("autor de los commits no genérico")]
    assert PERSONAL[0] not in out and PERSONAL[1] not in out


@pytest.mark.parametrize("dotenv", [
    f"GIT_AUTOR_NOMBRE={PERSONAL[0]}\nGIT_AUTOR_EMAIL={PERSONAL[1]}\n",
    f"GIT_AUTOR_NOMBRE=\"{GENERICO[0]}\"\nGIT_AUTOR_EMAIL='{PERSONAL[1]}'\n",
], ids=["los_dos", "solo_el_correo"])
def test_un_env_personal_en_la_raiz_es_error_aunque_el_git_config_sea_generico(repo, dotenv):
    repo.escribir(".env", dotenv, commit=False)
    rc, out = repo.correr()
    assert rc == 1 and "autor de los commits no genérico" in out and PERSONAL[1] not in out, out


def test_el_entorno_generico_manda_sobre_un_git_config_personal(repo):
    repo.git("config", "user.name", PERSONAL[0])
    repo.git("config", "user.email", PERSONAL[1])
    rc, out = repo.correr(GIT_AUTOR_NOMBRE="Astra", GIT_AUTOR_EMAIL="astra@users.noreply.github.com")
    assert rc == 0 and "autor" not in out, out


def test_el_entorno_generico_manda_sobre_un_env_personal(repo):
    repo.escribir(".env", f"GIT_AUTOR_NOMBRE={PERSONAL[0]}\nGIT_AUTOR_EMAIL={PERSONAL[1]}\n", commit=False)
    rc, out = repo.correr(GIT_AUTOR_NOMBRE="Astra", GIT_AUTOR_EMAIL="astra@users.noreply.github.com")
    assert rc == 0 and "autor" not in out, out


# --- QA r01 (ronda r02) ----------------------------------------------------------------------------------------

def _fila(i, tipo, entregable, estado):
    return f"| {i} | Tarea {i} | {tipo} | encargo | {entregable} | {estado} | | nota de {i} |\n"


def test_h01_pruebas_scripts_quita_cola_astra_script_antes_de_pytest():
    """Con COLA_ASTRA_SCRIPT exportado en la shell, el gate de .docs/scripts probaría otro fichero."""
    lineas = (SCRIPTS / "pruebas_scripts.sh").read_text(encoding="utf-8").splitlines()
    i_unset = next(i for i, l in enumerate(lineas) if l.startswith("unset COLA_ASTRA_SCRIPT"))
    i_pytest = next(i for i, l in enumerate(lineas) if "-m pytest" in l)
    assert i_unset < i_pytest


def test_h02_implementar_con_un_readme_anterior_a_la_cola_es_error(repo):
    repo.escribir(".docs/tickets/T-91/README.md", "# T-91\n\n| Campo | Valor |\n| --- | --- |\n| Estado | EN QA |\n",
                  fecha=_fecha_cola(-1))
    repo.estado(C_08="HECHA")
    rc, out = repo.correr()
    dia = _fecha_cola(-1)[:10]
    assert rc == 1 and re.search(rf"^ERROR\s+C-08 .*el entregable no ha cambiado desde la cola \({dia}\)$", out,
                                 re.MULTILINE), out


def test_h02_un_tipo_desconocido_marcado_hecha_es_error(repo):
    repo.escribir_cola(extra=_fila("C-09", "OTRO", "`.docs/otro/entregable.md`", "HECHA"))
    repo.escribir(".docs/otro/entregable.md", "# Entregable\n")
    rc, out = repo.correr()
    assert rc == 1 and re.search(r"^ERROR\s+C-09 \(Tarea C-09\): marcada HECHA pero tipo desconocido «OTRO»$", out,
                                 re.MULTILINE), out


def test_h03_una_revision_anterior_a_la_cola_cuenta(repo):
    repo.escribir(".docs/diseno/bloque_a/revision_astra.md", "# Revisión de A\n", fecha=_fecha_cola(-1))
    repo.estado(C_01="HECHA")
    rc, out = repo.correr()
    assert rc == 0 and not _errores(out) and "Siguiente: C-02" in out, out


def test_h03_el_estado_del_ticket_es_el_de_su_fila_a_principio_de_linea(repo):
    repo.escribir(".docs/tickets/T-91/README.md", "# T-91\n\nNo vale: texto | Estado | CERRADO | en medio.\n\n"
                  "| Campo | Valor |\n| --- | --- |\n| Estado | EN CURSO |\n")
    repo.estado(C_08="HECHA")
    rc, out = repo.correr()
    assert rc == 1 and re.search(r"^ERROR\s+C-08 .*estado del ticket «EN CURSO»$", out, re.MULTILINE), out


def test_h03_una_fila_rota_tambien_es_error_en_json(repo):
    repo.escribir_cola(extra="| C-09 | Tarea rota | REVISION | `x.md` | PENDIENTE |\n")
    repo.commit("fila rota")
    rc, out = repo.correr("--json")
    assert rc == 1 and "C-09: la fila tiene 5 columnas y no 8" in json.loads(out)["errores"], out


@pytest.mark.parametrize("añadido", [True, False], ids=["con_commit", "nuevo"])
def test_h07_un_entregable_con_ruta_no_ascii_y_cambios_sin_commit_es_aviso(repo, añadido):
    ruta = ".docs/diseño/bloque_g/revisión.md"
    repo.escribir_cola(extra=_fila("C-09", "REVISION", f"`{ruta}`", "EN CURSO 2099-01-01"))
    repo.commit("fila no ASCII")
    if añadido:
        repo.escribir(ruta, "BORRADOR\n")
    repo.escribir(ruta, "BORRADOR, más\n", commit=False)
    _, out = repo.correr()
    assert "AVISO  C-09: el entregable tiene cambios sin commit (trabajo sin subir)" in out, out


def test_h03_un_env_generico_entre_comillas_vale_aunque_el_git_config_sea_personal(repo):
    """El .env se lee quitando las comillas (R03 del revisor): un autor genérico entre comillas es genérico."""
    repo.git("config", "user.name", PERSONAL[0])
    repo.git("config", "user.email", PERSONAL[1])
    repo.escribir(".env", "GIT_AUTOR_NOMBRE=\"Astra\"\nGIT_AUTOR_EMAIL='astra@users.noreply.github.com'\n", commit=False)
    rc, out = repo.correr()
    assert rc == 0 and "autor" not in out, out
