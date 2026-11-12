"""Pruebas del registro de experimentos (T-99). Uso: .venv/bin/python -m pytest -q .docs/scripts/pruebas_registro_experimentos.py"""
import json
import sys
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
        f.write('{"tipo": "INTEN')
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
