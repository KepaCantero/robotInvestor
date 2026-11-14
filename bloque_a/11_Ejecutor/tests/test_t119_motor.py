"""T-119 · Motor: integración de las diez fichas P2 del Catálogo V5.0 (CT-09, CT-10, Registro de cálculos y Catálogo)."""
import copy
import hashlib
import json
import math
import os
import subprocess
import sys
from pathlib import Path

import pytest
from bloque_a.almacen import Almacen
from bloque_a.configuracion import cargar_config
from bloque_a.motor import fichas_p2, servicio

pytestmark = pytest.mark.filterwarnings("ignore::RuntimeWarning")   # las entradas hostiles desbordan a propósito

P2 = sorted(fichas_p2.FICHAS)
CASOS = [(f, i) for f in P2 for i in range(len(fichas_p2.CASOS_CONTROL[f]))]
CORTE = "2026-11-13"


class _Proveedor:
    as_of = None
    nombre = "pruebas"


def _motor(tmp_path, cfg=None):
    return servicio.Motor(Almacen(Path(tmp_path)), _Proveedor(), cfg or cargar_config())


def _peticion(ficha, i=0, **extra):
    caso = servicio.CASOS_CONTROL[ficha][i]
    return {"operacion": ficha, "datos": copy.deepcopy(caso["datos"]), "parametros": copy.deepcopy(caso["parametros"]),
            "fecha_corte": CORTE, **extra}


def _no_finitos(x):
    if isinstance(x, dict):
        return any(_no_finitos(v) for v in x.values())
    if isinstance(x, list):
        return any(_no_finitos(v) for v in x)
    return isinstance(x, float) and not math.isfinite(x)


# ================================================================================================== Catálogo y despacho
def test_son_las_diez_fichas_p2_y_el_catalogo_las_da_por_implementadas():
    assert len(P2) == 10 and servicio.P2 == frozenset(P2) and not servicio.P2 & (servicio.FASE1 | servicio.FASE2)
    assert servicio.ESTRICTAS == servicio.FASE1 | servicio.FASE2 | servicio.P2 and not servicio.ACEPTA_SEMILLA & servicio.P2
    mad = servicio.madurez_catalogo()
    catalogo = servicio.DIR_EJECUTOR.parent.joinpath(*servicio.RUTA_CATALOGO).read_text(encoding="utf-8")
    for f in P2:
        assert f in servicio.FICHAS_CATALOGO and servicio.servible(f)
        assert servicio.IMPLEMENTADAS[f]["fn"].__module__.endswith("fichas_p2")
        assert mad[f] == "IMPLEMENTADO (ejecutor, casos de control registrados (T-119))"
        fila = next(x for x in catalogo.split("\n") if x.startswith(f"| {f} |"))
        assert "| P2 | IMPLEMENTADO" in fila                                # la prioridad sigue siendo P2
        seccion = catalogo[catalogo.index(f"\n### {f} ·"):]
        assert "**Prioridad y madurez.** P2 · IMPLEMENTADO (ejecutor, casos de control registrados (T-119))." in seccion[:seccion.index("\n### ", 1) if "\n### " in seccion[1:] else None]


def test_ya_no_queda_ninguna_ficha_documentada():
    mad = servicio.madurez_catalogo()
    assert len(mad) == 81 and all(v.startswith("IMPLEMENTADO") for v in mad.values())
    assert len(servicio.IMPLEMENTADAS) == 80 and set(servicio.FICHAS_CATALOGO) - set(servicio.IMPLEMENTADAS) == servicio.SERVICIOS_CT10
    catalogo = servicio.DIR_EJECUTOR.parent.joinpath(*servicio.RUTA_CATALOGO).read_text(encoding="utf-8")
    assert ("Estado actual de las 81 fichas: 81 **IMPLEMENTADO** (14 del ejecutor V1.0 con pruebas unitarias y 67 con casos de "
            "control registrados, T-106, T-112 y T-119); ninguna queda en **DOCUMENTADO**. Ninguna ficha está VALIDADA.") in catalogo
    assert catalogo.count("ejecutor, casos de control registrados (T-119)") == 20   # fila del §4 y línea de cada ficha


def test_una_ficha_p2_degradada_en_el_catalogo_deja_de_servirse(tmp_path):
    """Manda el Catálogo (T-65, CS-08): con la fila de vuelta a «Documentado», el código no entrega cifras."""
    real = servicio.DIR_EJECUTOR.parent.joinpath(*servicio.RUTA_CATALOGO).read_text(encoding="utf-8")
    destino = Path(tmp_path, "raiz").joinpath(*servicio.RUTA_CATALOGO)
    destino.parent.mkdir(parents=True)
    destino.write_text(real.replace("| H4 | P2 | IMPLEMENTADO (ejecutor, casos de control registrados (T-119)) |",
                                    "| H4 | P2 | Documentado |"), encoding="utf-8")
    cfg = cargar_config()
    cfg.setdefault("rutas", {})["raiz_paquete"] = str(Path(tmp_path, "raiz"))
    m = _motor(tmp_path / "rc", cfg)
    assert servicio.madurez_catalogo(m.raiz)["PRV-PME-001"] == "Documentado"
    r = m.servir(_peticion("PRV-PME-001"), "AG-21")
    assert r["estado"] == "RECHAZADO" and r["motivo"] == "METODO_NO_IMPLEMENTADO" and "Documentado" in r["detalle"]
    assert m.servir(_peticion("CHR-TOKEN-001"), "AG-21")["estado"].startswith("SERVED")   # H2–H4: su fila no cambió


# ================================================================================================== CT-09, RC y CT-10
@pytest.mark.parametrize("ficha,i", CASOS, ids=[f"{f}:{i}" for f, i in CASOS])
def test_cada_caso_de_control_se_sirve_por_ct09_queda_en_rc_y_se_reejecuta_por_ct10(tmp_path, ficha, i):
    m = _motor(tmp_path)
    caso = servicio.CASOS_CONTROL[ficha][i]
    r = m.servir(_peticion(ficha, i), "AG-21", run_id="RUN-T119")
    assert r["estado"] in ("SERVED", "SERVED_WITH_LIMITATIONS"), r
    assert caso["comprobar"](r["resultado"]) and not _no_finitos(r["resultado"])
    assert r["resultado"]["advertencias"] == fichas_p2.ADVERTENCIAS[ficha]
    assert not set(r["limitaciones"]) & set(fichas_p2.ADVERTENCIAS[ficha])
    assert r["clase_cifra"] == fichas_p2.FICHAS[ficha]["cifra"] and r["referencia_ingenua"] == fichas_p2.FICHAS[ficha]["ri"]
    e = m.almacen.estado("RC")[r["calc_id"]]
    assert e["tipo_entrada"] == "SERVICIO" and e["operacion"]["ficha_version"] == fichas_p2.FICHAS[ficha]["version"]
    assert e["operacion"]["op_sin_ficha"] is False and e["modulos"] == [fichas_p2.FICHAS[ficha]["modulo"]]
    assert "fichas_p2" in e["artefacto"]["code_ref"] and e["verificacion_interna"]["identity_checks"] == "doble pasada idéntica"
    assert e["as_of"] == CORTE and e["semilla"] is None and e["incidencias"] == []
    d = e["datos"][0]
    assert d["huella"] == servicio.clave_hash(d["valor"])[:16] and e["clave_idempotencia"]
    out = m.reejecutar(r["calc_id"], "auditoría de T-119")
    assert (out["coincide"], out["categoria"], out["diferencias"]) == ("SI", None, [])
    otra = m.servir(_peticion(ficha, i), "AG-21", run_id="RUN-T119")
    assert otra["cache_hit"] and otra["calc_id"] == r["calc_id"]


@pytest.mark.parametrize("ficha", P2)
def test_ct10_detecta_un_resultado_alterado_y_unos_datos_alterados(tmp_path, ficha):
    m = _motor(tmp_path)
    r = m.servir(_peticion(ficha, 1), "AG-21")
    orig = m.almacen.estado("RC")[r["calc_id"]]

    def copia(cambio):
        e = copy.deepcopy(orig)
        cambio(e)
        e["calc_id"] = m.almacen.nuevo_id("CALC")
        m.almacen.escribir("RC", "AG-13", e)
        return e["calc_id"]

    def mover(e):
        pila = [e["resultado"]["payload"]]
        while pila:
            x = pila.pop()
            for k, v in (x.items() if isinstance(x, dict) else enumerate(x)):
                if isinstance(v, float) and v != 0:
                    x[k] = v * (1 + 1e-3)
                    return
                if isinstance(v, (dict, list)):
                    pila.append(v)
        raise AssertionError("sin cifras")

    out = m.reejecutar(copia(mover), "auditoría de T-119")
    assert (out["coincide"], out["categoria"]) == ("NO", "ERROR_ORIGINAL") and out["diferencias"]
    out = m.reejecutar(copia(lambda e: e["datos"][0].update(huella="0" * 16)), "auditoría de T-119")
    assert (out["coincide"], out["categoria"]) == ("NO", "DATOS_DISTINTOS")


def test_los_casos_de_control_de_las_diez_se_superan_y_quedan_en_rc(tmp_path):
    m = _motor(tmp_path)
    res = m.verificar_casos_control(P2, run_id="RUN-T119")
    assert set(res) == set(P2) and all(r["superados"] for r in res.values()), {f: r for f, r in res.items() if not r["superados"]}
    assert sum(len(r["casos"]) for r in res.values()) == 33
    rc = [e for e in m.almacen.leer("RC") if e.get("tipo_entrada") == "CASOS_CONTROL"]
    assert len(rc) == 10 and all(e["superados"] and e["estado"] == "SERVED" and e["run_id"] == "RUN-T119" for e in rc)
    assert all(c["superado"] and c["nombre"] for e in rc for c in e["casos_control"])


@pytest.mark.parametrize("ficha", P2)
def test_un_caso_que_falla_no_se_supera_y_se_registra(tmp_path, monkeypatch, ficha):
    casos = [dict(c) for c in servicio.CASOS_CONTROL[ficha]]
    casos[-1]["comprobar"] = lambda r: False
    monkeypatch.setitem(servicio.CASOS_CONTROL, ficha, casos)
    m = _motor(tmp_path)
    r = m.verificar_casos_control([ficha])[ficha]
    assert not r["superados"] and [c["superado"] for c in r["casos"]] == [True] * (len(casos) - 1) + [False]
    assert m.almacen.leer("RC")[-1]["estado"] == "REJECTED"


# ================================================================================================== fallo cerrado en el servicio
@pytest.mark.parametrize("ficha", P2)
def test_un_dato_posterior_a_la_fecha_de_corte_es_un_rechazo_con_su_entrada_en_rc(tmp_path, ficha):
    m = _motor(tmp_path)
    r = m.servir(_peticion(ficha, 1, fecha_corte="2009-12-31"), "AG-21")
    assert r["estado"] == "RECHAZADO" and r["motivo"] == "DATOS_INSUFICIENTES" and "posterior a la fecha de corte" in r["detalle"]
    e = m.almacen.leer("RC")[-1]
    assert e["tipo_entrada"] == "RECHAZO" and e["as_of"] == "2009-12-31" and e["calc_id"] == r["calc_id"]


@pytest.mark.parametrize("ficha", P2)
def test_umbrales_parametros_no_declarados_y_semillas(tmp_path, ficha):
    m = _motor(tmp_path)
    umbral = next(iter(fichas_p2.UMBRALES[ficha]))
    pet = _peticion(ficha)
    r = m.servir({**pet, "parametros": {**pet["parametros"], umbral: fichas_p2.UMBRALES[ficha][umbral]}}, "AG-21")
    assert r["estado"] == "RECHAZADO" and "umbrales fijos" in r["detalle"]
    r = m.servir({**pet, "parametros": {**pet["parametros"], "no_declarado": 1}}, "AG-21")
    assert r["estado"] == "RECHAZADO" and "no declarados" in r["detalle"]
    # las diez declaran semilla null: una semilla en los parámetros no es de la ficha; dos distintas, tampoco
    r = m.servir({**pet, "parametros": {**pet["parametros"], "semilla": 5}}, "AG-21")
    assert r["estado"] == "RECHAZADO" and "no declarados" in r["detalle"]
    r = m.servir({**pet, "semilla": 7, "parametros": {**pet["parametros"], "semilla": 5}}, "AG-21")
    assert r["estado"] == "RECHAZADO" and "dos semillas distintas" in r["detalle"]
    # la semilla de la petición no llega a la ficha (no la usa) y queda registrada tal cual en el artefacto
    r = m.servir({**pet, "semilla": 7}, "AG-21")
    assert r["estado"].startswith("SERVED") and m.almacen.estado("RC")[r["calc_id"]]["semilla"] == 7
    sin = m.servir(pet, "AG-21")
    assert sin["resultado"] == r["resultado"] and len(m.almacen.leer("RC")) == 6


def _hojas(x, ruta=()):
    if isinstance(x, dict):
        for k in sorted(x, key=str):
            yield from _hojas(x[k], ruta + (k,))
    elif isinstance(x, list):
        for i, e in enumerate(x):
            yield from _hojas(e, ruta + (i,))
    else:
        yield ruta


def _poner(v, ruta, valor):
    for k in ruta[:-1]:
        v = v[k]
    v[ruta[-1]] = valor


HOSTILES = [math.nan, math.inf, -math.inf, "texto", True, None, [1.0], {"valor": 1.0}, 1e308, -1e308, 10 ** 400, 0, -1, ""]


@pytest.mark.parametrize("ficha", P2)
def test_ninguna_excepcion_escapa_del_servicio_y_nada_no_finito_se_sirve(tmp_path, ficha):
    """Datos y parámetros hostiles por `Motor.servir`: o se sirve con cifras finitas o se rechaza; siempre una entrada en RC."""
    m = _motor(tmp_path)
    pet = _peticion(ficha, 1)
    hojas = list(_hojas(pet["datos"][0]["valores"]))
    paso = max(1, len(hojas) // 12)
    peticiones = []
    for ruta in hojas[::paso] + hojas[:6] + hojas[-6:]:
        for malo in HOSTILES:
            p = copy.deepcopy(pet)
            _poner(p["datos"][0]["valores"], ruta, malo)
            peticiones.append(p)
    for k in fichas_p2.PARAMETROS_POR_DEFECTO[ficha]:
        for malo in [*HOSTILES, 1e12, 20261110, [10 ** 9] * 3, list(range(100))]:
            peticiones.append({**pet, "parametros": {**pet["parametros"], k: malo}})
    for clave in list(pet["datos"][0]["valores"]):
        p = copy.deepcopy(pet)
        del p["datos"][0]["valores"][clave]
        peticiones.append(p)
    peticiones += [{**pet, "datos": []}, {**pet, "datos": [{"valores": {}}]}, {**pet, "parametros": {"x": object}},
                   {**pet, "datos": [{"valores": {"serie": [[[[]]]] * 10}}]}]
    antes = len(m.almacen.leer("RC"))
    for p in peticiones:
        r = m.servir(p, "AG-21")
        assert r["estado"] in ("SERVED", "SERVED_WITH_LIMITATIONS", "RECHAZADO"), r
        if r["estado"] != "RECHAZADO":
            assert not _no_finitos(r["resultado"])
            json.dumps(r["resultado"], allow_nan=False)
    assert len(m.almacen.leer("RC")) == antes + len(peticiones)


@pytest.mark.parametrize("ficha", P2)
@pytest.mark.parametrize("error", [MemoryError, RecursionError, ZeroDivisionError, KeyError])
def test_un_manejador_que_falla_o_da_no_finitos_es_un_rechazo(tmp_path, monkeypatch, ficha, error):
    def roto(ent, params):
        raise error("provocado")
    monkeypatch.setitem(servicio.IMPLEMENTADAS, ficha, {**servicio.IMPLEMENTADAS[ficha], "fn": roto})
    m = _motor(tmp_path)
    r = m.servir(_peticion(ficha), "AG-21")
    assert r["estado"] == "RECHAZADO" and m.almacen.leer("RC")[-1]["tipo_entrada"] == "RECHAZO"
    monkeypatch.setitem(servicio.IMPLEMENTADAS, ficha, {**servicio.IMPLEMENTADAS[ficha], "fn": lambda e, p: ({"x": math.inf}, [])})
    r = m.servir(_peticion(ficha, 1), "AG-21")
    assert r["estado"] == "RECHAZADO" and "no finitas" in r["detalle"]


def test_las_fichas_reciben_la_configuracion_del_motor(tmp_path):
    """FX-BEER-001 lee el nivel de su IC de `evaluacion.nivel_ic` de la configuración del Motor, no de la de por defecto."""
    cfg = cargar_config()
    cfg["evaluacion"]["nivel_ic"] = 0.5
    con = _motor(tmp_path / "a", cfg).servir(_peticion("FX-BEER-001"), "AG-21")["resultado"]
    sin = _motor(tmp_path / "b").servir(_peticion("FX-BEER-001"), "AG-21")["resultado"]
    assert con["nivel_ic"] == 0.5 and sin["nivel_ic"] == cargar_config()["evaluacion"]["nivel_ic"] == 0.90
    assert con["ic_desalineamiento_pct"][1] - con["ic_desalineamiento_pct"][0] < sin["ic_desalineamiento_pct"][1] - sin["ic_desalineamiento_pct"][0]
    assert con["desalineamiento_pct"] == sin["desalineamiento_pct"]


def test_la_fecha_de_corte_entra_en_la_clave_de_la_cache(tmp_path):
    m = _motor(tmp_path)
    a = m.servir(_peticion("REI-LEV-001"), "AG-21")
    b = m.servir(_peticion("REI-LEV-001", fecha_corte="2026-06-30"), "AG-21")
    assert not b["cache_hit"] and b["calc_id"] != a["calc_id"] and b["resultado"] == a["resultado"]
    assert m.servir(_peticion("REI-LEV-001", fecha_corte="2026-06-29"), "AG-21")["estado"] == "RECHAZADO"


# ================================================================================================== determinismo
_GUION = """
import copy, hashlib, json, sys
from bloque_a.motor import fichas_p2 as m
out = {}
for f, casos in sorted(m.CASOS_CONTROL.items()):
    for i, c in enumerate(casos):
        v = {}
        for d in c["datos"]:
            v.update(copy.deepcopy(d["valores"]))
        r, lim = m.FICHAS[f]["fn"]({"valores": v, "series": {}, "series_rol": {}, "fecha_corte": "2026-11-13"}, dict(c["parametros"]))
        out[f"{f}:{i}"] = [r, lim]
sys.stdout.write(hashlib.sha256(json.dumps(out, sort_keys=True, allow_nan=False).encode()).hexdigest())
"""


def test_mismo_resultado_en_dos_procesos():
    """Dos procesos nuevos, con semillas de hash distintas, dan byte a byte los mismos resultados en los 33 casos."""
    huellas = []
    for semilla in ("0", "12345"):
        entorno = {**os.environ, "PYTHONHASHSEED": semilla, "PYTHONPATH": str(servicio.DIR_EJECUTOR)}
        salida = subprocess.run([sys.executable, "-c", _GUION], capture_output=True, text=True, env=entorno, check=True,
                                cwd=str(servicio.DIR_EJECUTOR))
        huellas.append(salida.stdout.strip())
    out = {}
    for f, casos in sorted(fichas_p2.CASOS_CONTROL.items()):
        for i, c in enumerate(casos):
            v = {}
            for d in c["datos"]:
                v.update(copy.deepcopy(d["valores"]))
            r, lim = fichas_p2.FICHAS[f]["fn"]({"valores": v, "series": {}, "series_rol": {}, "fecha_corte": CORTE}, dict(c["parametros"]))
            out[f"{f}:{i}"] = [r, lim]
    aqui = hashlib.sha256(json.dumps(out, sort_keys=True, allow_nan=False).encode()).hexdigest()
    assert len(huellas[0]) == 64 and huellas[0] == huellas[1] == aqui
