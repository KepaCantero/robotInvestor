"""QA r01 de T-162 (revisor) · sondas propias de la respuesta final por CT-03 (PB-07).

Uso, desde `bloque_a/11_Ejecutor` de la copia de trabajo:
  ../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-162/revisores/r01_01_sondas.py
Todo con el cliente simulado, sin red ni coste. Cada prueba es una sonda: verdad de la final (referencias de ese RUN- y
nada más, PRG- de otros RUN-, G3, opciones inventadas, confianza), R8 (texto del error, datos protegidos en una opción o en
las limitaciones) e idempotencia en hilos. Las de procesos, reinicio y comparación con la base están en r01_02.
"""
import copy
import json
import sys
import threading
from pathlib import Path

import pytest

EJECUTOR = Path(__file__).resolve().parents[4] / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJECUTOR / "tests"))
sys.path.insert(0, str(EJECUTOR))

from bloque_a import respuesta_final
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config
from bloque_a.contratos import DatosSensibles
from bloque_a.herramientas.ht01_datos import cargar_universo
from conftest import AS_OF, nuevo_bloque

PB07 = "¿Qué opinas de la renta variable india frente a la indonesia a 6 meses?"
ORO = "¿Qué opinas del oro frente a la plata a 6 meses?"
IBAN = "ES91 2100 0418 4502 0005 1332"
CORREO = "ana.garcia.qa@ejemplo.com"


@pytest.fixture(scope="module")
def universo():
    return cargar_universo(RUTA_UNIVERSO_EJEMPLO)


def _espiar(b):
    vistos = []
    crear = b.mensajeria.crear

    def f(*a, **k):
        m = crear(*a, **k)
        vistos.append(copy.deepcopy(m))
        return m

    b.mensajeria.crear = f
    return vistos


def _ret03(ms):
    return [m for m in ms if m["contrato"] == "CT-03" and m["tipo_mensaje"] == "RETORNO"]


def _finales_f5(b, q):
    return [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "QRY" and e.get("id") == q and e.get("respuesta_final")]


def _claves(b, run_id):
    """Las claves de entrada de F1–F5 (como `_existentes`, pero escrito de nuevo por el revisor)."""
    f5 = b.almacen.estado("F5", clave="id")
    return {"RUN": {k for k, v in f5.items() if v.get("tipo_entrada") == "RUN"},
            "TND": set(b.almacen.estado("F1")), "OPP": set(b.almacen.estado("F3")),
            "CLM": {e["clm_id"] for e in b.almacen.leer("F2") if e.get("tipo_entrada") == "CLM"},
            "PRG": {e["prg_id"]: e for e in b.almacen.leer("F4") if e.get("tipo_entrada") == "ALTA"}}


@pytest.fixture(scope="module")
def dos_runs(tmp_path_factory, universo):
    """Un ciclo de RV (RUN-1) y una consulta que escala a RV (RUN-2): las mismas opciones pueden salir en los dos."""
    b = nuevo_bloque(tmp_path_factory.mktemp("r01s"), universo)
    r1 = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    ms = _espiar(b)
    q = b.consulta(PB07, as_of=AS_OF)
    return b, r1, q, ms


# ------------------------------------------------------------------ 1 · la final dice la verdad
def test_s01_solo_cita_lo_de_su_run(dos_runs):
    b, r1, q, ms = dos_runs
    fin = q["respuesta_final"]
    run2 = q["escalado"]["run_id"]
    assert run2 != r1["run_id"] and fin["respuesta_final"]["resultado_analisis"] == "ENTREGADO"
    c = _claves(b, run2)
    f5 = b.almacen.estado("F5", clave="id")
    f3 = b.almacen.estado("F3")
    top = [o for lst in f5[run2]["top3_por_clase"].values() for o in lst]
    ct02 = next(m for m in ms if m["contrato"] == "CT-02" and m.get("run_id") == run2)
    assert top == [o for lst in ct02["resumen"]["top3_por_clase"].values() for o in lst]   # lo que de verdad salió
    refs = fin["referencias"]
    assert [r for r in refs if r.startswith("RUN-")] == [run2]                 # ningún otro RUN-
    assert [r for r in refs if r.startswith("OPP-")] == top
    for r in refs:
        pref = r.split("-")[0]
        assert r in c[pref], r
    # PRG-: solo los congelados por este RUN- y de una opción citada (no los del RUN-1 de la misma opción)
    prg = [r for r in refs if r.startswith("PRG-")]
    assert prg and all(c["PRG"][p]["run_id"] == run2 and c["PRG"][p]["opp_id"] in top for p in prg)
    assert set(prg) == {p for p, e in c["PRG"].items() if e["run_id"] == run2 and e.get("opp_id") in top and p.startswith("PRG-")}
    # TND- y CLM-: solo de las opciones citadas
    tnd = {t for o in top for t in f3[o]["tnd_ids"]}
    clm = {x for o in top for x in f3[o]["evidencias"]}
    assert {r for r in refs if r.startswith("TND-")} == tnd and {r for r in refs if r.startswith("CLM-")} == clm
    # cada OPP- citada en el texto es del top-3, y no aparece ningún OPP- más
    import re
    assert set(re.findall(r"OPP-\d{4}-\d{4,}", fin["respuesta"])) == set(top)
    assert set(re.findall(r"RUN-\d{4}-\d{4,}", fin["respuesta"])) == {run2}
    assert fin["confianza"] == min((f3[o]["confianza"] for o in top), key=respuesta_final.CONFIANZAS.index)


def _construir_con(b, q, f5=None, f3=None):
    """`construir` con la vista consolidada de F5/F3 retocada (sin escribir nada en el almacén)."""
    qry = b.almacen.estado("F5", AS_OF, clave="id")[q["query_id"]]
    real_estado = b.almacen.estado

    def estado(archivo, as_of=None, clave=None, **k):
        out = real_estado(archivo, as_of, clave, **k)
        if archivo == "F5" and f5:
            f5(out)
        if archivo == "F3" and f3:
            f3(out)
        return out

    b.almacen.estado = estado
    try:
        return respuesta_final.construir(b.almacen, qry, q["msg_id"], AS_OF)
    finally:
        b.almacen.estado = real_estado


def test_s02a_opcion_evidencia_y_tendencia_inventadas_no_se_citan(dos_runs):
    b, _, q, _ = dos_runs
    run2 = q["escalado"]["run_id"]
    top = b.almacen.estado("F5", clave="id")[run2]["top3_por_clase"]["RV"]

    def f5(out):
        out[run2]["top3_por_clase"] = {"RV": ["OPP-2026-9999", *top]}

    def f3(out):
        out[top[0]]["evidencias"] = [*out[top[0]]["evidencias"], "CLM-2026-9999", 7, None]
        out[top[0]]["tnd_ids"] = ["TND-2026-9999"]

    cuerpo, _, est, desc = _construir_con(b, q, f5, f3)
    assert "OPP-2026-9999" not in json.dumps(cuerpo) and "TND-2026-9999" not in cuerpo["referencias"]
    assert "CLM-2026-9999" not in cuerpo["referencias"] and {"CLM-2026-9999", "TND-2026-9999"} <= set(desc)
    respuesta_final.validar(cuerpo, est)


@pytest.mark.xfail(strict=True, reason="H-03 (baja): las referencias de cada campo no se filtran por su prefijo")
@pytest.mark.parametrize("ajeno", ["RUN-2026-0001", "HIT-2026-0001"])
def test_s02b_un_id_existente_de_otro_tipo_en_las_evidencias(dos_runs, ajeno):
    """`evidencias` de una opción con un identificador que existe pero no es un CLM- (estado manipulado): debería
    descartarse; hoy un RUN- ajeno se cita y un HIT- hace fallar toda la final por el patrón del esquema."""
    b, _, q, _ = dos_runs
    run2 = q["escalado"]["run_id"]
    top = b.almacen.estado("F5", clave="id")[run2]["top3_por_clase"]["RV"]

    def f3(out):
        out[top[0]]["evidencias"] = [*out[top[0]]["evidencias"], ajeno]

    cuerpo, _, est, _ = _construir_con(b, q, None, f3)
    respuesta_final.validar(cuerpo, est)
    assert ajeno not in cuerpo["referencias"]


def test_s03_g3_bloquea_en_la_primera_o_la_segunda_pasada(tmp_path, universo):
    for paso in ("g3", "g3b"):
        b = nuevo_bloque(tmp_path / paso, universo)
        if paso == "g3":
            real = b._validar_g3

            def g3(*a, _real=real, **k):
                p, g = _real(*a, **k)
                return p, {**g, "dictamen": "BLOQUEADO"}
            b._validar_g3 = g3
        else:
            real = b._redactar

            def red(*a, _real=real, **k):
                e, g, r = _real(*a, **k)
                return e, {**g, "dictamen": "BLOQUEADO"}, r
            b._redactar = red
        ms = _espiar(b)
        q = b.consulta(PB07, as_of=AS_OF)
        fin = q["respuesta_final"]
        run_id = q["escalado"]["run_id"]
        assert b.almacen.estado("F5", clave="id")[run_id]["entrega"] == "BLOQUEADA"
        assert fin["respuesta_final"]["resultado_analisis"] == "SIN_ENTREGA" and fin["estado"] == "SIN_RESULTADO"
        assert fin["referencias"] == [run_id] and "G3 bloqueó" in fin["respuesta"]
        assert "OPP-" not in json.dumps(fin) and "CLM-" not in json.dumps(fin) and "PRG-" not in json.dumps(fin)
        assert not any(m["contrato"] == "CT-02" for m in ms)


def test_s04_falla_despues_de_registrar_el_run(tmp_path, universo):
    """El RUN- se registra y se entrega (CT-02), pero algo falla después (auditoría): FALLIDO, solo el RUN-."""
    b = nuevo_bloque(tmp_path, universo)

    def auditar(*a, **k):
        raise KeyError(f"fallo con {CORREO} y {IBAN}")

    b._auditar = auditar
    ms = _espiar(b)
    q = b.consulta(PB07, as_of=AS_OF)
    fin = q["respuesta_final"]
    run_id = q["escalado"]["run_id"]
    assert run_id and q["escalado"]["estado_run"] == "FALLIDO"
    assert fin["respuesta_final"]["resultado_analisis"] == "FALLIDO" and fin["referencias"] == [run_id]
    assert fin["run_id"] == run_id and "OPP-" not in json.dumps(fin)
    todo = json.dumps(ms, ensure_ascii=False) + json.dumps(b.almacen.leer("HA"), ensure_ascii=False) \
        + json.dumps(b.almacen.leer("F5"), ensure_ascii=False)
    assert CORREO not in todo and "2100 0418" not in todo
    inc = [e for e in b.almacen.leer("HA") if e.get("tipo") == "HERRAMIENTA" and q["query_id"] in e.get("detalle", "")]
    assert len(inc) == 1 and inc[0]["detalle"].endswith("(KeyError)")


def test_s05_confianza_mas_baja_y_valor_raro(dos_runs):
    b, _, q, _ = dos_runs
    qry = b.almacen.estado("F5", AS_OF, clave="id")[q["query_id"]]
    top = [o for lst in b.almacen.estado("F5", clave="id")[q["escalado"]["run_id"]]["top3_por_clase"].values() for o in lst]
    real_estado = b.almacen.estado
    for valor, esperado in (("en disputa", "en disputa"), ("alta", "especulativo"), (None, "especulativo")):
        def estado(archivo, as_of=None, clave=None, _v=valor, **k):
            out = real_estado(archivo, as_of, clave, **k)
            if archivo == "F3":
                out[top[-1]]["confianza"] = _v
                for o in top[:-1]:
                    out[o]["confianza"] = "establecido"
            return out
        b.almacen.estado = estado
        try:
            cuerpo, _, _, _ = respuesta_final.construir(b.almacen, qry, q["msg_id"], AS_OF)
        finally:
            b.almacen.estado = real_estado
        assert cuerpo["confianza"] == esperado, (valor, cuerpo["confianza"])


def test_s06_run_parcial_no_se_presenta_como_completo(dos_runs):
    b, _, q, _ = dos_runs
    qry = b.almacen.estado("F5", AS_OF, clave="id")[q["query_id"]]
    run2 = q["escalado"]["run_id"]
    real_estado = b.almacen.estado

    def estado(archivo, as_of=None, clave=None, **k):
        out = real_estado(archivo, as_of, clave, **k)
        if archivo == "F5":
            out[run2]["estado"] = "PARCIAL"
        return out

    b.almacen.estado = estado
    try:
        cuerpo, _, est, _ = respuesta_final.construir(b.almacen, qry, q["msg_id"], AS_OF)
    finally:
        b.almacen.estado = real_estado
    assert cuerpo["respuesta_final"]["resultado_analisis"] == "ENTREGADO_PARCIAL" and est == "PARCIAL"
    assert "con alcance parcial" in cuerpo["respuesta"] and "completo" not in cuerpo["respuesta"].split("(")[0]


# ------------------------------------------------------------------ 2 · R8
@pytest.mark.parametrize("donde", ["nombre", "limitaciones"])
def test_s07_dato_protegido_en_una_opcion_no_llega(tmp_path, universo, monkeypatch, donde):
    b = nuevo_bloque(tmp_path, universo)
    b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    real = respuesta_final.enviar
    monkeypatch.setattr(respuesta_final, "enviar", lambda *a, **k: None)
    q = b.consulta(PB07, as_of=AS_OF)
    monkeypatch.setattr(respuesta_final, "enviar", real)
    run2 = q["escalado"]["run_id"]
    if donde == "nombre":
        opp = b.almacen.estado("F5", clave="id")[run2]["top3_por_clase"]["RV"][0]
        b.almacen.escribir("F3", "AG-02", {"tipo_entrada": "ACTUALIZACION", "opp_id": opp, "nombre": f"Cartera de {CORREO}"})
    else:
        b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "RUN", "id": run2, "limitaciones": [f"IBAN del cliente {IBAN}"]})
    ms = _espiar(b)
    n_f5 = len(b.almacen.leer("F5"))
    with pytest.raises(DatosSensibles):
        real(b, q["query_id"], q["msg_id"], AS_OF)
    assert not ms and len(b.almacen.leer("F5")) == n_f5 and not _finales_f5(b, q["query_id"])
    ha = json.dumps(b.almacen.leer("HA"), ensure_ascii=False)
    assert CORREO not in ha and "2100 0418" not in ha
    assert any(e.get("tipo") == "SEGURIDAD" for e in b.almacen.leer("HA"))
    # el revisor anota lo que ve la CLI: la consulta entera se cae después de la provisional
    return q


def test_s08_r8_desde_la_consulta_entera(tmp_path, universo, monkeypatch):
    """Si el dato protegido está en la memoria cuando llega la consulta, ¿qué ve quien llama a `consulta`?"""
    b = nuevo_bloque(tmp_path, universo)
    real_construir = respuesta_final.construir

    def construir(*a, **k):
        cuerpo, run_id, est, desc = real_construir(*a, **k)
        cuerpo["limitaciones"] = [*cuerpo["limitaciones"], f"Contacto {CORREO}"]
        return cuerpo, run_id, est, desc

    monkeypatch.setattr(respuesta_final, "construir", construir)
    ms = _espiar(b)
    with pytest.raises(DatosSensibles):
        b.consulta(ORO, as_of=AS_OF, ejecutar_escalado=False)
    # la provisional ya salió y la QRY ya está en F5, pero la final no; y no hay manera de reenviarla sin el msg_id
    prov = _ret03(ms)
    assert len(prov) == 1
    qry = [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "QRY"]
    assert len(qry) == 1 and "respuesta_final" not in qry[0]
    assert prov[0]["msg_id"] not in json.dumps(qry[0])     # F5 no guarda el msg_id de la provisional


# ------------------------------------------------------------------ 3 · idempotencia y determinismo (hilos)
def test_s09_ocho_hilos(tmp_path, universo, monkeypatch):
    b = nuevo_bloque(tmp_path, universo, cfg=cargar_config(extra={"modo": "backtest"}))
    real = respuesta_final.enviar
    monkeypatch.setattr(respuesta_final, "enviar", lambda *a, **k: None)
    q = b.consulta(ORO, as_of=AS_OF)
    monkeypatch.setattr(respuesta_final, "enviar", real)
    ms = _espiar(b)
    barrera = threading.Barrier(8)
    salidas, errores = [], []

    def uno():
        barrera.wait()
        try:
            salidas.append(real(b, q["query_id"], q["msg_id"], AS_OF))
        except Exception as e:   # noqa: BLE001
            errores.append(e)

    hs = [threading.Thread(target=uno) for _ in range(8)]
    for h in hs:
        h.start()
    for h in hs:
        h.join()
    assert not errores
    assert sorted(s["repetido"] for s in salidas) == [False] + [True] * 7
    assert len({json.dumps({k: v for k, v in s.items() if k != "repetido"}, sort_keys=True) for s in salidas}) == 1
    assert len(_ret03(ms)) == 1 and len(_finales_f5(b, q["query_id"])) == 1


def test_s10_dos_consultas_con_el_mismo_run(dos_runs, monkeypatch):
    """Una segunda QRY- cuyo `escalado` apunta al RUN- de la primera (estado manipulado): ¿la final lo comprueba?"""
    b, _, q, _ = dos_runs
    run2 = q["escalado"]["run_id"]
    real = respuesta_final.enviar
    monkeypatch.setattr(respuesta_final, "enviar", lambda *a, **k: None)
    q2 = b.consulta(ORO, as_of=AS_OF, ejecutar_escalado=False)
    monkeypatch.setattr(respuesta_final, "enviar", real)
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "QRY", "id": q2["query_id"],
                                       "escalado": {**q2["escalado"], "run_id": run2, "estado_run": "COMPLETO"}})
    fin2 = real(b, q2["query_id"], q2["msg_id"], AS_OF)
    fin1 = real(b, q["query_id"], q["msg_id"], AS_OF)
    assert fin1["repetido"] and not fin2["repetido"] and fin1["msg_id"] != fin2["msg_id"]
    disparador = b.almacen.estado("F5", clave="id")[run2]["disparador"]
    # se anota lo que pasa: la final de QRY-2 cita el RUN- lanzado por QRY-1
    print("S10", {"fin2_resultado": fin2["respuesta_final"]["resultado_analisis"], "cita_run_ajeno": run2 in fin2["referencias"],
            "disparador_qry": disparador.get("qry_id"), "qry2": q2["query_id"]})
