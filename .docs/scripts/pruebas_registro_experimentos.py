"""Pruebas del registro de experimentos (T-99). Uso: .venv/bin/python -m pytest -q .docs/scripts/pruebas_registro_experimentos.py"""
import json
import subprocess
import sys
import unicodedata
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import registro_experimentos as rx

AHORA = "2026-11-12T10:00:00+00:00"
DESPUES = "2026-11-12T11:00:00+00:00"
ANTES = "2026-11-12T09:00:00+00:00"


def pre(**cambios):
    d = {"hipotesis": "Quitar la segunda pasada del Seleccionador no empeora la calidad", "objeto": "RECORTE",
         "metrica": "exceso frente a la cesta de la clase", "datos": "backtest 2026-03 a 2026-05, cliente simulado",
         "desde": "2026-03-06", "hasta": "2026-05-29", "semilla": 7,
         "criterio_exito": "rango del 90 % de la diferencia por encima de cero", "max_variantes": 2}
    d.update(cambios)
    return d


@pytest.fixture
def reg(tmp_path):
    return rx.Registro(tmp_path / "registro.jsonl")


def test_prerregistro_valido_sellado(reg):
    e = reg.prerregistrar(pre(), "claude", AHORA)
    assert e["exp_id"] == "EXP-2026-0001" and e["huella_prerregistro"] == rx.huella(e["contenido"])
    assert reg.prerregistrar(pre(), "claude", AHORA)["exp_id"] == "EXP-2026-0002"
    assert reg.verificar() == 2


@pytest.mark.parametrize("cambio", [{"hipotesis": "corta"}, {"objeto": "CAPRICHO"}, {"max_variantes": 0}, {"max_variantes": True},
                                    {"max_variantes": 2.5}, {"semilla": "7"}, {"desde": "2026-06-01"}, {"hasta": "29-05-2026"},
                                    {"criterio_exito": ""}])
def test_prerregistro_mal_formado_no_escribe_nada(reg, cambio):
    with pytest.raises(rx.RegistroError):
        reg.prerregistrar(pre(**cambio), "claude", AHORA)
    assert not reg.ruta.exists()


def test_prerregistro_incompleto(reg):
    d = pre()
    del d["criterio_exito"]
    with pytest.raises(rx.RegistroError, match="faltan"):
        reg.prerregistrar(d, "claude", AHORA)


def test_sin_prerregistro_no_hay_intento_ni_resultado(reg):
    with pytest.raises(rx.RegistroError, match="no está prerregistrado"):
        reg.intento("EXP-2026-0009", "v1", AHORA)
    e = reg.prerregistrar(pre(), "claude", AHORA)
    with pytest.raises(rx.RegistroError, match="no tiene el intento"):
        reg.resultado(e["exp_id"], 1, "mejor", ahora=DESPUES)


def test_un_resultado_no_se_reescribe_ni_lleva_un_veredicto_inventado(reg):
    e = reg.prerregistrar(pre(), "claude", AHORA)
    reg.intento(e["exp_id"], "v1", DESPUES)
    with pytest.raises(rx.RegistroError, match="no válido"):
        reg.resultado(e["exp_id"], 1, "casi mejor", ahora=DESPUES)
    reg.resultado(e["exp_id"], 1, "peor", ahora=DESPUES)
    with pytest.raises(rx.RegistroError, match="ya tiene resultado"):
        reg.resultado(e["exp_id"], 1, "mejor", ahora=DESPUES)


def test_cuentan_todos_los_intentos_y_las_variantes_de_mas(reg):
    exp = reg.prerregistrar(pre(max_variantes=2), "claude", AHORA)["exp_id"]
    for v, ver in (("v1", "peor"), ("v1", "fallido"), ("v2", "todavía no se sabe"), ("v3", "mejor")):
        n = reg.intento(exp, v, DESPUES)["n"]
        reg.resultado(exp, n, ver, ahora=DESPUES)
    reg.intento(exp, "v2", DESPUES)   # sin resultado: cuenta igual
    r = reg.resumen(exp)
    assert r["intentos"] == 5 and r["variantes"] == 3 and r["sin_resultado"] == [5]
    assert r["fuera_del_maximo"] == [4] and r["adoptables"] == [] and not reg.adoptable(exp)   # la que ganó es la variante de más


def test_adoptable_solo_si_mejor_dentro_del_maximo_y_despues_del_prerregistro(reg):
    exp = reg.prerregistrar(pre(), "claude", AHORA)["exp_id"]
    n = reg.intento(exp, "v1", DESPUES)["n"]
    reg.resultado(exp, n, "mejor", ahora=DESPUES)
    assert reg.adoptable(exp) and reg.resumen(exp)["adoptables"] == [1]
    exp2 = reg.prerregistrar(pre(), "claude", AHORA)["exp_id"]
    n = reg.intento(exp2, "v1", ANTES)["n"]   # el intento es anterior al prerregistro: el resultado no vale
    reg.resultado(exp2, n, "mejor", ahora=DESPUES)
    assert not reg.adoptable(exp2)


def test_reescribir_una_linea_rompe_la_cadena(reg):
    exp = reg.prerregistrar(pre(), "claude", AHORA)["exp_id"]
    reg.intento(exp, "v1", DESPUES)
    reg.resultado(exp, 1, "peor", ahora=DESPUES)
    lineas = reg.ruta.read_text(encoding="utf-8").splitlines()
    e = json.loads(lineas[2])
    e["veredicto"] = "mejor"   # cambiar el resultado a posteriori
    reg.ruta.write_text("\n".join(lineas[:2] + [json.dumps(e, ensure_ascii=False)]) + "\n", encoding="utf-8")
    with pytest.raises(rx.RegistroError, match="cadena rota"):
        reg.verificar()
    with pytest.raises(rx.RegistroError):
        reg.intento(exp, "v2", DESPUES)   # con la cadena rota no se anota nada más


def test_quitar_un_intento_fallido_rompe_la_cadena(reg):
    exp = reg.prerregistrar(pre(), "claude", AHORA)["exp_id"]
    for v in ("v1", "v2"):
        reg.intento(exp, v, DESPUES)
    lineas = reg.ruta.read_text(encoding="utf-8").splitlines()
    reg.ruta.write_text("\n".join([lineas[0], lineas[2]]) + "\n", encoding="utf-8")
    with pytest.raises(rx.RegistroError, match="cadena rota"):
        reg.verificar()


def test_cambiar_el_criterio_despues_rompe_la_cadena(reg):
    reg.prerregistrar(pre(), "claude", AHORA)
    e = json.loads(reg.ruta.read_text(encoding="utf-8"))
    e["contenido"]["criterio_exito"] = "cualquier mejora, aunque el rango incluya el cero"
    reg.ruta.write_text(json.dumps(e, ensure_ascii=False) + "\n", encoding="utf-8")
    with pytest.raises(rx.RegistroError):
        reg.verificar()


def test_linea_que_no_es_json(reg):
    reg.prerregistrar(pre(), "claude", AHORA)
    with open(reg.ruta, "a", encoding="utf-8") as f:
        f.write('{"tipo": "INTEN\n')
    with pytest.raises(rx.RegistroError, match="no es JSON"):
        reg.verificar()


def test_linea_de_ordenes(tmp_path, capsys):
    f = tmp_path / "pre.json"
    f.write_text(json.dumps(pre()), encoding="utf-8")
    r = str(tmp_path / "r.jsonl")
    assert rx.main(["--registro", r, "prerregistrar", str(f), "--autor", "claude"]) == 0
    exp = rx.Registro(r).anotaciones()[0]["exp_id"]
    assert rx.main(["--registro", r, "intento", exp, "--variante", "v1"]) == 0
    assert rx.main(["--registro", r, "resultado", exp, "1", "peor"]) == 0
    assert rx.main(["--registro", r, "resultado", exp, "1", "mejor"]) == 2   # no se reescribe
    assert rx.main(["--registro", r, "verificar"]) == 0
    assert rx.main(["--registro", r, "ver", exp]) == 0
    assert '"intentos": 1' in capsys.readouterr().out


# ---------------------------------------------------------------- ronda r02 (QA r01 NO APTO): una prueba por hallazgo


def _resellar(reg):
    """Lo que haría quien reescribe a propósito: rehacer también el sello (contra eso solo vale el ancla de git)."""
    lineas = [json.loads(x) for x in reg.ruta.read_text(encoding="utf-8").splitlines()]
    s = {"seq": lineas[-1]["_seq"], "hash": lineas[-1]["_hash"]} if lineas else {"seq": 0, "hash": "0" * 64}
    reg.sello.write_text(json.dumps(s) + "\n", encoding="utf-8")


def _rehacer_cadena(anotaciones):
    """Lo que haría quien reescribe el fichero: recalcular la cadena entera tras cambiar algo."""
    prev, out = "0" * 64, []
    for i, e in enumerate(anotaciones, 1):
        e = {k: v for k, v in e.items() if k not in ("_seq", "_hash_prev", "_hash")}
        e.update(_seq=i, _hash_prev=prev)
        e["_hash"] = rx.huella(e)
        prev = e["_hash"]
        out.append(json.dumps(e, ensure_ascii=False, sort_keys=True))
    return "\n".join(out) + ("\n" if out else "")


def _leer(reg):
    return [json.loads(x) for x in reg.ruta.read_text(encoding="utf-8").splitlines()]


def _git(carpeta, *args):
    subprocess.run(["git", "-C", str(carpeta), *args], check=True, capture_output=True,
                   env={"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
                        "HOME": str(carpeta), "PATH": "/usr/bin:/bin"})


@pytest.fixture
def reg_en_git(tmp_path):
    _git(tmp_path, "init", "-q")
    r = rx.Registro(tmp_path / "registro.jsonl")
    exp = r.prerregistrar(pre(), "claude", AHORA)["exp_id"]
    r.intento(exp, "v1", DESPUES)
    r.resultado(exp, 1, "peor", ahora=DESPUES)
    _git(tmp_path, "add", "registro.jsonl")
    _git(tmp_path, "commit", "-q", "-m", "registro")
    return r, exp


def test_h01_ancla_en_git_quitar_las_ultimas_o_recalcular_se_detecta(reg_en_git):
    r, exp = reg_en_git
    original = r.ruta.read_text(encoding="utf-8")
    r.intento(exp, "v2", DESPUES)   # lo nuevo sin subir sí se admite (el registro crece)
    assert r.verificar() == 4
    lineas = original.splitlines()
    r.ruta.write_text("\n".join(lineas[:-1]) + "\n", encoding="utf-8")   # quitar la última anotación subida
    with pytest.raises(rx.RegistroError, match="HEAD"):
        r.verificar()
    anot = [json.loads(x) for x in lineas]
    anot[2]["veredicto"] = "mejor"
    r.ruta.write_text(_rehacer_cadena(anot), encoding="utf-8")   # reescribir y recalcular la cadena entera
    with pytest.raises(rx.RegistroError, match="HEAD"):
        r.verificar()
    r.ruta.unlink()   # borrar el registro entero
    with pytest.raises(rx.RegistroError, match="HEAD"):
        r.verificar()
    assert rx.main(["--registro", str(r.ruta), "verificar"]) == 2


def test_h01_huella_del_prerregistro_y_del_intento_se_contrastan(reg):
    exp = reg.prerregistrar(pre(), "claude", AHORA)["exp_id"]
    reg.intento(exp, "v1", DESPUES)
    anot = _leer(reg)
    a = json.loads(json.dumps(anot))
    a[0]["contenido"]["criterio_exito"] = "cualquier mejora, aunque el rango incluya el cero"   # cambio del criterio, cadena rehecha
    reg.ruta.write_text(_rehacer_cadena(a), encoding="utf-8")
    with pytest.raises(rx.RegistroError, match="huella del prerregistro"):
        reg.verificar()
    b = json.loads(json.dumps(anot))
    b[1]["huella_prerregistro"] = "f" * 64
    reg.ruta.write_text(_rehacer_cadena(b), encoding="utf-8")
    with pytest.raises(rx.RegistroError, match="cita otro prerregistro"):
        reg.verificar()


def test_h01_verificar_sin_registro_da_error(tmp_path):
    assert rx.main(["--registro", str(tmp_path / "no.jsonl"), "verificar"]) == 2


_HIJO = """
import sys
sys.path.insert(0, {scripts!r})
import registro_experimentos as rx
r = rx.Registro({ruta!r})
if sys.argv[1] == "pre":
    print(r.prerregistrar({pre!r}, "claude")["exp_id"])
else:
    for _ in range(40):
        r.intento("EXP-2026-0001", sys.argv[1], "2026-11-12T11:00:00+00:00")
"""


def test_h02_dos_procesos_a_la_vez_no_rompen_la_cadena(reg):
    reg.prerregistrar(pre(max_variantes=5), "claude", AHORA)
    codigo = _HIJO.format(scripts=str(Path(rx.__file__).parent), ruta=str(reg.ruta), pre=pre())
    py = sys.executable
    hijos = [subprocess.Popen([py, "-c", codigo, v]) for v in ("a", "b")]
    assert [h.wait() for h in hijos] == [0, 0]
    assert reg.verificar() == 81
    hijos = [subprocess.Popen([py, "-c", codigo, "pre"], stdout=subprocess.PIPE, text=True) for _ in range(2)]
    ids = sorted(h.communicate()[0].strip() for h in hijos)
    assert len(set(ids)) == 2 and reg.verificar() == 83


def test_h03_repetir_una_variante_no_la_hace_adoptable(reg):
    exp = reg.prerregistrar(pre(max_variantes=3), "claude", AHORA)["exp_id"]
    for v, ver in (("v1", "peor"), ("v1", "peor"), ("v1", "mejor"),     # repetir hasta que salga «mejor»
                   ("v2", "fallido"), ("v2", "mejor"),                   # el primero que no es «fallido» cuenta
                   ("v3", "mejor"), ("v3", "todavía no se sabe")):       # un «mejor» que no se repite
        n = reg.intento(exp, v, DESPUES)["n"]
        reg.resultado(exp, n, ver, ahora=DESPUES)
    r = reg.resumen(exp)
    assert r["por_variante"]["v1"]["veredicto"] == "peor" and r["por_variante"]["v1"]["contradictoria"]
    assert r["por_variante"]["v2"]["cuenta"] == 5 and not r["por_variante"]["v2"]["contradictoria"]
    assert r["por_variante"]["v3"]["contradictoria"]
    assert r["contradictorias"] == ["v1", "v3"] and r["adoptables"] == [5] and r["adoptable"]


def test_h04_separadores_unicode_y_fichero_sin_salto_final(reg):
    exp = reg.prerregistrar(pre(hipotesis="Una hipótesis con separador\u0085y otro"), "claude", AHORA)["exp_id"]
    reg.intento(exp, "v ", DESPUES)
    assert reg.verificar() == 2 and _leer(reg)[0]["contenido"]["hipotesis"].count(" ") == 1
    texto = reg.ruta.read_text(encoding="utf-8")
    reg.ruta.write_text(texto.rstrip("\n"), encoding="utf-8")
    with pytest.raises(rx.RegistroError, match="salto de línea"):
        reg.intento(exp, "v2", DESPUES)
    assert reg.ruta.read_text(encoding="utf-8") == texto.rstrip("\n")   # no se escribió nada


@pytest.mark.parametrize("cambio", [{"datos": None}, {"datos": 3}, {"datos": ["a"]}, {"datos": ""}, {"desde": "2026-02-30"},
                                    {"hasta": "2026-13-01"}, {"desde": "0000-00-00"}, {"extra": float("nan")}])
def test_h05_h09_prerregistro_que_no_validaria_no_escribe(reg, cambio):
    with pytest.raises(rx.RegistroError):
        reg.prerregistrar(pre(**cambio), "claude", AHORA)
    assert not reg.ruta.exists()


@pytest.mark.parametrize("detalle", [["a"], "texto", 3, {"x": float("nan")}])
def test_h05_detalle_que_no_es_un_objeto_json(reg, detalle):
    exp = reg.prerregistrar(pre(), "claude", AHORA)["exp_id"]
    reg.intento(exp, "v1", DESPUES)
    with pytest.raises(rx.RegistroError):
        reg.resultado(exp, 1, "peor", detalle, ahora=DESPUES)
    assert reg.verificar() == 2


def test_h05_n_booleano_ahora_mal_formado_y_exp_sin_cifras(reg, monkeypatch):
    exp = reg.prerregistrar(pre(), "claude", AHORA)["exp_id"]
    reg.intento(exp, "v1", DESPUES)
    with pytest.raises(rx.RegistroError):
        reg.resultado(exp, True, "peor", ahora=DESPUES)
    for malo in ("2026-11-12", "2026-11-12T10:00:00", "ayer", "2026-11-31T10:00:00+00:00"):
        with pytest.raises(rx.RegistroError):
            reg.intento(exp, "v1", malo)
    monkeypatch.setattr(rx, "MAX_EXP_POR_ANIO", 1)
    with pytest.raises(rx.RegistroError, match="no admite más"):
        reg.prerregistrar(pre(), "claude", AHORA)
    assert reg.verificar() == 2


def test_h05_todo_lo_escrito_valida_con_las_reglas_de_ct24(reg):
    exp = reg.prerregistrar(pre(otra="clave"), "claude", AHORA)["exp_id"]
    reg.intento(exp, "v1", DESPUES)
    reg.resultado(exp, 1, "mejor", {"x": [1, 2]}, ahora=DESPUES)
    for e in _leer(reg):
        rx.validar_anotacion(e)


@pytest.mark.parametrize("mutar,motivo", [
    (lambda a: a[1].pop("tipo"), "tipo"),
    (lambda a: a[1].update(tipo="BORRADO"), "tipo"),
    (lambda a: a.append(json.loads(json.dumps(a[0]))), "dos veces"),
    (lambda a: a[1].update(dentro_del_maximo=True), "máximo"),
    (lambda a: a[1].update(n=5), "correlativo"),
    (lambda a: a[1].update(extra=1), "forma"),
])
def test_h06_forma_y_semantica_al_leer(reg, mutar, motivo):
    exp = reg.prerregistrar(pre(max_variantes=1), "claude", AHORA)["exp_id"]
    reg.intento(exp, "v1", DESPUES)
    reg.intento(exp, "v2", DESPUES)   # fuera del máximo
    a = _leer(reg)
    a[1], a[2] = a[2], a[1]            # la de fuera del máximo primero, para que el falseo de «dentro» se note
    a[1]["n"], a[2]["n"] = 1, 2
    a[1]["dentro_del_maximo"], a[2]["dentro_del_maximo"] = True, False
    reg.ruta.write_text(_rehacer_cadena(a), encoding="utf-8")
    _resellar(reg)
    assert reg.verificar() == 3       # un registro rehecho (también su sello) pero coherente se lee
    a = _leer(reg)
    mutar(a)
    if motivo == "máximo":
        a[2]["dentro_del_maximo"] = True
        motivo = "máximo"
    reg.ruta.write_text(_rehacer_cadena(a), encoding="utf-8")
    _resellar(reg)
    with pytest.raises(rx.RegistroError, match=motivo):
        reg.verificar()
    assert rx.main(["--registro", str(reg.ruta), "ver"]) == 2


def test_h07_instantes_y_anio_en_utc(reg):
    exp = reg.prerregistrar(pre(), "claude", "2026-11-12T10:00:00-02:00")["exp_id"]   # 12:00 UTC
    n = reg.intento(exp, "v1", "2026-11-12T11:00:00+00:00")["n"]                     # una hora ANTES
    reg.resultado(exp, n, "mejor", ahora="2026-11-12T13:00:00+00:00")
    assert not reg.adoptable(exp)
    exp2 = reg.prerregistrar(pre(), "claude", "2026-11-12T12:00:00Z")["exp_id"]
    n = reg.intento(exp2, "v1", "2026-11-12T12:00:00+00:00")["n"]                     # el mismo instante con otra escritura
    reg.resultado(exp2, n, "mejor", ahora="2026-11-12T13:00:00+00:00")
    assert reg.adoptable(exp2)
    assert reg.prerregistrar(pre(), "claude", "2027-01-01T00:30:00+01:00")["exp_id"] == "EXP-2026-0003"


def test_h09_bytes_no_utf8_y_variantes(reg):
    exp = reg.prerregistrar(pre(), "claude", AHORA)["exp_id"]
    for v in (None, "", "  ", 1, {"a": 1}):
        with pytest.raises(rx.RegistroError):
            reg.intento(exp, v, DESPUES)
    nfc, nfd = unicodedata.normalize("NFC", "única"), unicodedata.normalize("NFD", "única")
    reg.intento(exp, nfc, DESPUES)
    reg.intento(exp, nfd, DESPUES)
    assert reg.resumen(exp)["variantes"] == 1
    with open(reg.ruta, "ab") as f:
        f.write(b"\xff\xfe\n")
    with pytest.raises(rx.RegistroError, match="UTF-8"):
        reg.verificar()


def test_h09_h10_linea_de_ordenes(tmp_path):
    f = tmp_path / "pre.json"
    r = str(tmp_path / "r.jsonl")
    f.write_text("null", encoding="utf-8")
    assert rx.main(["--registro", r, "prerregistrar", str(f)]) == 2
    f.write_text(json.dumps(pre()), encoding="utf-8")
    assert rx.main(["prerregistrar", str(f), "--registro", r]) == 0   # --registro también detrás de la orden
    assert rx.main(["intento", "EXP-" + _anio() + "-0001", "--variante", "v1", "--registro", r]) == 0
    assert rx.main(["resultado", "EXP-" + _anio() + "-0001", "1", "peor", "--detalle", '{"x": NaN}', "--registro", r]) == 2
    assert rx.main(["resultado", "EXP-" + _anio() + "-0001", "1", "peor", "--detalle", "[1]", "--registro", r]) == 2
    with pytest.raises(SystemExit):
        rx.main(["--registro", r, "intento", "EXP-" + _anio() + "-0001"])   # la variante es obligatoria en la línea de órdenes


def _anio():
    from datetime import UTC, datetime
    return str(datetime.now(UTC).year)


def test_h01_sello_quitar_las_ultimas_sin_git_se_detecta(reg):
    exp = reg.prerregistrar(pre(), "claude", AHORA)["exp_id"]
    reg.intento(exp, "v1", DESPUES)
    reg.resultado(exp, 1, "fallido", ahora=DESPUES)
    texto = reg.ruta.read_text(encoding="utf-8")
    lineas = texto.splitlines()
    for quedan in (2, 1):   # quitar el «fallido», o el intento entero con su resultado
        reg.ruta.write_text("\n".join(lineas[:quedan]) + "\n", encoding="utf-8")
        with pytest.raises(rx.RegistroError, match="sello"):
            reg.verificar()
    reg.ruta.write_text(texto, encoding="utf-8")
    assert reg.verificar() == 3
    reg.sello.unlink()
    with pytest.raises(rx.RegistroError, match="falta el sello"):
        reg.verificar()
    reg.sello.write_text("{roto", encoding="utf-8")
    with pytest.raises(rx.RegistroError, match="sello"):
        reg.verificar()


# ---------------------------------------------------------------- ronda r03 (QA r02 NO APTO): una prueba por hallazgo

def _git_ok(carpeta, *args):
    _git(carpeta, *args)


def _commit(carpeta, *ficheros, mensaje="registro"):
    _git(carpeta, "add", *ficheros)
    _git(carpeta, "commit", "-q", "-m", mensaje)


def test_h13_un_recorte_subido_con_commit_se_detecta(reg_en_git):
    r, _exp = reg_en_git
    lineas = r.ruta.read_text(encoding="utf-8").splitlines()
    r.ruta.write_text("\n".join(lineas[:2]) + "\n", encoding="utf-8")   # se quita el resultado…
    _resellar(r)
    _commit(r.ruta.parent, "registro.jsonl", "registro.jsonl.sello")    # …y se sube el recorte
    with pytest.raises(rx.RegistroError, match="perdió o cambió"):
        r.verificar()


def test_h13_cambiar_un_veredicto_y_subirlo_se_detecta(reg_en_git):
    r, _exp = reg_en_git
    a = _leer(r)
    a[2]["veredicto"] = "mejor"
    r.ruta.write_text(_rehacer_cadena(a), encoding="utf-8")
    _resellar(r)
    _commit(r.ruta.parent, "registro.jsonl", "registro.jsonl.sello")
    with pytest.raises(rx.RegistroError, match="perdió o cambió"):
        r.verificar()


def test_h13_sacar_el_registro_de_head_se_detecta(reg_en_git):
    r, _exp = reg_en_git
    texto = r.ruta.read_text(encoding="utf-8")
    _git(r.ruta.parent, "rm", "-q", "--cached", "registro.jsonl")
    _git(r.ruta.parent, "commit", "-q", "-m", "fuera")
    r.ruta.write_text(texto, encoding="utf-8")
    with pytest.raises(rx.RegistroError, match="se quitó del repositorio"):
        r.verificar()


def test_h13_resolver_una_fusion_quedandose_con_un_lado_se_detecta(reg_en_git):
    r, exp = reg_en_git
    d = r.ruta.parent
    _git(d, "checkout", "-q", "-b", "otra")
    r.intento(exp, "vB", DESPUES)
    _commit(d, "registro.jsonl", "registro.jsonl.sello", mensaje="B")
    _git(d, "checkout", "-q", "-")
    r.intento(exp, "vA", DESPUES)
    _commit(d, "registro.jsonl", "registro.jsonl.sello", mensaje="A")
    texto_a = r.ruta.read_text(encoding="utf-8")
    sello_a = r.sello.read_text(encoding="utf-8")
    subprocess.run(["git", "-C", str(d), "merge", "-q", "otra"], capture_output=True,
                   env={"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
                        "HOME": str(d), "PATH": "/usr/bin:/bin"}, check=False)   # da conflicto: se resuelve a mano
    r.ruta.write_text(texto_a, encoding="utf-8")   # se resuelve el conflicto quedándose con el lado A
    r.sello.write_text(sello_a, encoding="utf-8")
    _commit(d, "registro.jsonl", "registro.jsonl.sello", mensaje="fusión")
    with pytest.raises(rx.RegistroError, match="perdió o cambió"):
        r.verificar()


def test_h14_el_ancla_no_se_apaga_en_silencio(reg_en_git, monkeypatch):
    r, _exp = reg_en_git
    lineas = r.ruta.read_text(encoding="utf-8").splitlines()
    monkeypatch.setenv("GIT_DIR", "/no/existe")   # un GIT_DIR ajeno no desactiva el ancla
    r.ruta.write_text("\n".join(lineas[:-1]) + "\n", encoding="utf-8")
    with pytest.raises(rx.RegistroError, match="HEAD"):
        r.verificar()
    monkeypatch.setattr(rx.shutil, "which", lambda _: None)
    with pytest.raises(rx.RegistroError, match="git no está instalado"):
        r.verificar()
    monkeypatch.undo()
    real = rx.Registro._git

    def dañado(raiz, *args):
        if args and args[0] == "cat-file":
            return subprocess.CompletedProcess(args, 128, b"", b"fatal: bad object")
        return real(raiz, *args)
    monkeypatch.setattr(rx.Registro, "_git", staticmethod(dañado))
    r.ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    with pytest.raises(rx.RegistroError, match="dañado"):
        r.verificar()


def test_h15_un_intento_pendiente_bloquea_la_adopcion(reg):
    exp = reg.prerregistrar(pre(max_variantes=2), "claude", AHORA)["exp_id"]
    reg.intento(exp, "v1", DESPUES)                                    # sin resultado todavía
    n = reg.intento(exp, "v1", DESPUES)["n"]
    reg.resultado(exp, n, "mejor", ahora=DESPUES)
    r = reg.resumen(exp)
    assert r["por_variante"]["v1"]["pendiente"] and r["por_variante"]["v1"]["veredicto"] is None and not r["adoptable"]
    n = reg.intento(exp, "v2", DESPUES)["n"]
    reg.resultado(exp, n, "mejor", ahora=DESPUES)
    reg.intento(exp, "v2", DESPUES)                                    # una repetición pendiente
    assert not reg.adoptable(exp)
    reg.resultado(exp, 4, "mejor", ahora=DESPUES)
    assert reg.adoptable(exp) and reg.resumen(exp)["adoptables"] == [3]


def test_h16_si_falla_el_sello_el_registro_sigue_vivo(reg, monkeypatch):
    exp = reg.prerregistrar(pre(), "claude", AHORA)["exp_id"]
    real = rx.Registro._escribir_sello

    def falla(self, e, temporal=None):
        raise rx.RegistroError("no se pudo poner al día el sello (disco lleno)")
    monkeypatch.setattr(rx.Registro, "_escribir_sello", falla)
    with pytest.raises(rx.RegistroError, match="sello"):
        reg.intento(exp, "v1", DESPUES)
    monkeypatch.setattr(rx.Registro, "_escribir_sello", real)
    assert reg.verificar() == 2                                        # el sello va una anotación por detrás: se admite
    reg.intento(exp, "v2", DESPUES)                                    # y la siguiente escritura lo pone al día
    assert json.loads(reg.sello.read_text(encoding="utf-8"))["seq"] == 3 and reg.verificar() == 3


def test_h17_un_registro_por_agente():
    carpeta = str(Path(rx.__file__).parent)
    codigo = f"import sys; sys.path.insert(0, {carpeta!r}); import registro_experimentos as rx; print(rx.REGISTRO_DEFECTO.name)"
    out = subprocess.run([sys.executable, "-c", codigo],
                         capture_output=True, text=True, env={"RI_AGENTE": "astra", "PATH": "/usr/bin:/bin"}, check=True)
    assert out.stdout.strip() == "registro_astra.jsonl"
    assert rx.REGISTRO_DEFECTO.name == f"registro_{rx.AGENTE}.jsonl"


def test_h18_un_clon_sin_sello_se_lee_si_es_lo_subido(tmp_path):
    _git(tmp_path, "init", "-q")
    r = rx.Registro(tmp_path / "registro.jsonl")
    exp = r.prerregistrar(pre(), "claude", AHORA)["exp_id"]
    r.intento(exp, "v1", DESPUES)
    _commit(tmp_path, "registro.jsonl")
    r.sello.unlink()
    assert r.verificar() == 2                                          # idéntico a HEAD: git hace de ancla
    r2 = rx.Registro(tmp_path / "registro.jsonl", ancla_git=False)
    with pytest.raises(rx.RegistroError, match="falta el sello"):
        r2.verificar()


_HIJO_BUSCA = """
import sys
sys.path.insert(0, {scripts!r})
import registro_experimentos as rx
r = rx.Registro({ruta!r})
e, nuevo = r.buscar_o_prerregistrar(lambda c: c.get("hipotesis") == {hip!r}, {pre!r}, "claude")
print(e["exp_id"])
"""


def test_h19_buscar_o_prerregistrar_a_la_vez_crea_uno(reg):
    p = pre()
    codigo = _HIJO_BUSCA.format(scripts=str(Path(rx.__file__).parent), ruta=str(reg.ruta), hip=p["hipotesis"], pre=p)
    hijos = [subprocess.Popen([sys.executable, "-c", codigo], stdout=subprocess.PIPE, text=True) for _ in range(4)]
    ids = {h.communicate()[0].strip() for h in hijos}
    assert len(ids) == 1 and reg.verificar() == 1


def test_h20_sustituto_suelto(reg):
    with pytest.raises(rx.RegistroError, match="UTF-8"):
        reg.prerregistrar(pre(hipotesis="Una hipótesis con un sustituto \udc80 suelto"), "claude", AHORA)
    assert not reg.ruta.exists()


def test_h21_lectores_durante_una_escritura_y_espera_del_cerrojo(reg, monkeypatch):
    import fcntl
    reg.prerregistrar(pre(max_variantes=5), "claude", AHORA)
    codigo = _HIJO.format(scripts=str(Path(rx.__file__).parent), ruta=str(reg.ruta), pre=pre())
    escritor = subprocess.Popen([sys.executable, "-c", codigo, "a"])
    lecturas = 0
    while escritor.poll() is None:
        reg.verificar()                                                # nunca una falsa alarma de manipulación
        lecturas += 1
    assert escritor.wait() == 0 and lecturas > 0 and reg.verificar() == 41
    monkeypatch.setattr(rx, "CERROJO_ESPERA_S", 0.2)
    with open(reg.ruta.with_name(reg.ruta.name + ".lock"), "a", encoding="utf-8") as fl:
        fcntl.flock(fl.fileno(), fcntl.LOCK_EX)
        with pytest.raises(rx.RegistroError, match="ocupado"):
            reg.intento("EXP-2026-0001", "v9", DESPUES)


def test_h21_un_intento_rechazado_no_crea_nada(tmp_path):
    r = rx.Registro(tmp_path / "nueva" / "registro.jsonl")
    with pytest.raises(rx.RegistroError, match="no está prerregistrado"):
        r.intento("EXP-2026-0001", "v1", DESPUES)
    assert not (tmp_path / "nueva").exists()


def test_h22_registro_sin_sello_de_la_010_y_detalle_null(reg, tmp_path):
    exp = reg.prerregistrar(pre(), "claude", AHORA)["exp_id"]
    reg.intento(exp, "v1", DESPUES)
    reg.sello.unlink()                                                 # como un registro de la 0.1.0
    with pytest.raises(rx.RegistroError, match="sellar"):
        reg.verificar()
    assert rx.main(["--registro", str(reg.ruta), "sellar"]) == 0 and reg.verificar() == 2
    assert rx.main(["--registro", str(reg.ruta), "sellar"]) == 2       # no se vuelve a sellar
    assert rx.main(["--registro", str(reg.ruta), "resultado", exp, "1", "peor", "--detalle", "null"]) == 2


def test_h16_si_el_sello_no_se_puede_preparar_no_se_escribe_nada(reg, monkeypatch):
    exp = reg.prerregistrar(pre(), "claude", AHORA)["exp_id"]
    antes = reg.ruta.read_text(encoding="utf-8")

    def falla(self, e):
        raise rx.RegistroError("no se puede preparar el sello del registro (simulado): no se escribe nada")
    monkeypatch.setattr(rx.Registro, "_preparar_sello", falla)
    with pytest.raises(rx.RegistroError, match="no se escribe nada"):
        reg.intento(exp, "v1", DESPUES)
    assert reg.ruta.read_text(encoding="utf-8") == antes


def test_qa_r02_variantes_nfd_de_un_registro_antiguo(reg):
    exp = reg.prerregistrar(pre(max_variantes=1), "claude", AHORA)["exp_id"]
    nfd = unicodedata.normalize("NFD", "única")
    a = _leer(reg)
    intento = {"tipo": "INTENTO", "exp_id": exp, "n": 1, "variante": nfd, "inicio": DESPUES,
               "huella_prerregistro": a[0]["huella_prerregistro"], "dentro_del_maximo": True}
    reg.ruta.write_text(_rehacer_cadena([a[0], intento]), encoding="utf-8")   # como lo escribiría la 0.1.0, sin normalizar
    _resellar(reg)
    reg.intento(exp, unicodedata.normalize("NFC", "única"), DESPUES)
    r = reg.resumen(exp)
    assert r["variantes"] == 1 and r["fuera_del_maximo"] == []
