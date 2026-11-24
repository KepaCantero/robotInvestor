"""QA r01 de T-183 (Claude). Ataques a PB-29: raíces y derivadas en F2 y G3-DAT-09 sobre un paquete real.

Ejecutar desde bloque_a/11_Ejecutor:
    ../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-183/revisores/r01_ataques_raices.py

Cada prueba afirma el comportamiento que pide el plan (PB-29), el Documento 0 o el esquema de F2. Las que fallan
son hallazgos del qa.md (se indica cuál en cada una).
"""
import copy
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path.cwd() / "tests"))
from conftest import AS_OF, nuevo_bloque, universo  # noqa: E402,F401

from bloque_a import mantenimiento_fuentes, sintesis  # noqa: E402
from bloque_a.referencias import Referencias  # noqa: E402

DIA = pd.Timestamp(AS_OF)


# ------------------------------------------------------------------ utilidades
def _bloque_con_f9(tmp_path, universo, fichas):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(DIA)
    ruta = tmp_path / "f9.md"
    ruta.write_text("\n".join(fichas))
    b.referencias = Referencias(b.cfg, {"F9": ruta})
    return b


def _ficha(rid, q=75, nivel="B", original=None, tipologia=None):
    t = f"#### {rid} · Q {q} ({nivel}) — Medio {rid}\n- **Año:** 2020\n"
    if tipologia:
        t += f"- **Tipología:** {tipologia}\n"
    if original:
        t += f"- **Fuente original:** {original}\n"
    return t


def _pieza(rid, texto, afirmacion="Resultado"):
    return {"fuente": "REF-" + rid, "extracto": texto, "direccion": "favorable", "afirmacion": afirmacion}


def _ingesta(b, piezas, run="RUN-2026-0001"):
    f = {"_piezas": piezas, "_refs_ofrecidas": [p["fuente"] for p in piezas], "proxy": "ABC"}
    b._registrar_evidencia_clase({"nivel": "N1", "clase": "RV", "finalistas": [f]}, DIA, run)
    evds = {k: v for k, v in b.almacen.estado("F2", clave="evd_id").items() if v.get("tipo_entrada") == "EVD"}
    clms = {k: v for k, v in b.almacen.estado("F2", clave="clm_id").items() if v.get("tipo_entrada") == "CLM"}
    return f, evds, clms


@pytest.fixture(scope="module")
def ciclo_real(tmp_path_factory, universo):  # noqa: F811
    """Un ciclo mock completo; se capturan los paquetes que pasan por HT-09."""
    capturas = []
    original = sintesis.ht09_validar

    def espia(b, paquete, extras, visual):
        r = original(b, paquete, extras, visual)
        capturas.append((copy.deepcopy(paquete), extras, visual, copy.deepcopy(r)))
        return r

    sintesis.ht09_validar = espia
    try:
        b = nuevo_bloque(tmp_path_factory.mktemp("ciclo183"), universo)
        b.ciclo(AS_OF)
    finally:
        sintesis.ht09_validar = original
    return b, capturas


def _g3(b, paquete, extras, visual):
    res = sintesis.ht09_validar(b, copy.deepcopy(paquete), extras, visual)
    return res, next(c for c in res["comprobaciones"] if c["id"] == "G3-DAT-09")


def _primera_opcion(paquete):
    return next(op for c in paquete["clases"].values() for op in c.get("opciones", []))


# ------------------------------------------------------------------ paquete real (G3-DAT-09)
def test_a01_ciclo_real_lleva_g3_dat_09_en_ok(ciclo_real):
    """Evidencia: G3-DAT-09 corre en los paquetes reales del ciclo mock y sale OK."""
    b, capturas = ciclo_real
    assert capturas
    for _, _, _, res in capturas:
        c = next(c for c in res["comprobaciones"] if c["id"] == "G3-DAT-09")
        assert c["resultado"] == "OK"


def test_a02_f2_manipulada_bloquea_el_paquete_real(ciclo_real):
    """Evidencia: una cifra de raíces manipulada en F2 bloquea el dictamen de un paquete real."""
    b, capturas = ciclo_real
    paquete, extras, visual, _ = capturas[0]
    clms = b.almacen.estado("F2", paquete["fecha"], clave="clm_id")
    cid = next(c for op in (o for cl in paquete["clases"].values() for o in cl["opciones"])
               for c in op["evidencias"] if "evidencias_ps1" in clms.get(c, {}))
    viejo = clms[cid]["raices_independientes"]
    b.almacen.escribir("F2", "AG-12", {**clms[cid], "raices_independientes": viejo + 5})
    try:
        res, c = _g3(b, paquete, extras, visual)
        assert c["resultado"] == "BLOQUEO" and res["dictamen"] == "BLOQUEADO"
    finally:
        b.almacen.escribir("F2", "AG-12", {**clms[cid], "raices_independientes": viejo})


def test_a03_h01_ps1_del_paquete_sin_respaldo_en_f2_no_pasa(ciclo_real):
    """H-01: G3-DAT-09 compara el resumen de raíces de la conclusión con F2. Si F2 dice que las raíces de la opción
    son de nivel C (PS1 no superada) y el paquete sigue declarando PS1 superada, debe bloquear."""
    b, capturas = ciclo_real
    paquete, extras, visual, _ = capturas[0]
    op = _primera_opcion(paquete)
    assert op["puertas"]["PS1"] is True
    clms = b.almacen.estado("F2", paquete["fecha"], clave="clm_id")
    evds = b.almacen.estado("F2", paquete["fecha"], clave="evd_id")
    tocadas = []
    for cid in op["evidencias"]:
        for eid in clms[cid].get("evidencias_ps1", []):
            tocadas.append(dict(evds[eid]))
            b.almacen.escribir("F2", "AG-12", {**evds[eid], "nivel_fuente": "C", "tipo_fuente": "SECUNDARIA"})
    try:
        evds2 = b.almacen.estado("F2", paquete["fecha"], clave="evd_id")
        union = {}
        for cid in op["evidencias"]:
            union.update(sintesis.raices_de_clm(clms[cid], evds2))
        assert not b._ps1(union)          # F2 ya no sostiene PS1
        _, c = _g3(b, paquete, extras, visual)
        assert c["resultado"] == "BLOQUEO", "G3-DAT-09 no mira el PS1 que declara el paquete"
    finally:
        for e in tocadas:
            b.almacen.escribir("F2", "AG-12", e)


def test_a04_h02_clm_sin_traza_ps1_tambien_se_comprueba(ciclo_real):
    """H-02: una CLM sin `evidencias_ps1` (0 raíces) con `raices_independientes` manipulado pasa G3-DAT-09 en silencio."""
    b, capturas = ciclo_real
    paquete, extras, visual, _ = capturas[0]
    clms = b.almacen.estado("F2", paquete["fecha"], clave="clm_id")
    cid, op = next((c, op) for cl in paquete["clases"].values() for op in cl["opciones"]
                   for c in op["evidencias"] if "evidencias_ps1" not in clms.get(c, {}))
    b.almacen.escribir("F2", "AG-12", {**clms[cid], "raices_independientes": 5})
    try:
        _, c = _g3(b, paquete, extras, visual)
        assert c["resultado"] == "BLOQUEO"
    finally:
        b.almacen.escribir("F2", "AG-12", clms[cid])


def test_a05_h02_clm_citada_que_no_existe_en_f2_bloquea(ciclo_real):
    """H-02: una opción que cita una CLM que no está en F2 a la fecha del paquete sale OK (falla abierto)."""
    b, capturas = ciclo_real
    paquete, extras, visual, _ = capturas[0]
    paquete = copy.deepcopy(paquete)
    _primera_opcion(paquete)["evidencias"].append("CLM-2099-9999")
    _, c = _g3(b, paquete, extras, visual)
    assert c["resultado"] == "BLOQUEO"


def test_a06_h03_la_baja_de_una_fuente_deja_f2_coherente(ciclo_real):
    """H-03: tras la baja de una fuente (T-181, `avisar_curador`), F2 debe seguir coherente: la CLM afectada recalcula
    sus raíces. Hoy queda la cifra antigua y G3-DAT-09 bloquea la entrega siguiente que cite esa CLM."""
    b, capturas = ciclo_real
    paquete, extras, visual, _ = capturas[0]
    clms = b.almacen.estado("F2", paquete["fecha"], clave="clm_id")
    evds = b.almacen.estado("F2", paquete["fecha"], clave="evd_id")
    cid, eid = next((c, e) for op in (o for cl in paquete["clases"].values() for o in cl["opciones"])
                    for c in op["evidencias"] for e in clms.get(c, {}).get("evidencias_ps1", [])
                    if evds[e]["ref_id"].startswith("REF-"))
    ref = evds[eid]["ref_id"]
    estado_previo = {k: dict(v) for k, v in evds.items() if v.get("ref_id") == ref}
    mantenimiento_fuentes.avisar_curador(b.almacen, b.mensajeria, DIA, "RUN-2026-0999", {("F7", ref, AS_OF)})
    try:
        clm = b.almacen.estado("F2", paquete["fecha"], clave="clm_id")[cid]
        evds2 = b.almacen.estado("F2", paquete["fecha"], clave="evd_id")
        _, c = _g3(b, paquete, extras, visual)
        assert clm["raices_independientes"] == len(sintesis.raices_de_clm(clm, evds2)), \
            f"F2 incoherente tras la baja; G3-DAT-09 = {c['resultado']}"
    finally:
        for e in estado_previo.values():
            b.almacen.escribir("F2", "AG-12", e)


# ------------------------------------------------------------------ PB-29: 1 raíz y 20 derivadas
def test_a07_raiz_primaria_de_nivel_a_supera_ps1_con_veinte_derivadas(tmp_path, universo):  # noqa: F811
    """Cláusula «salvo que la raíz sea primaria de nivel A»: sin prueba en test_t183 (H-05)."""
    fichas = [_ficha("RF-0000", 90, "A", tipologia="primaria")] + [_ficha(f"RF-{n:04d}", original="REF-RF-0000") for n in range(1, 21)]
    b = _bloque_con_f9(tmp_path, universo, fichas)
    piezas = [_pieza(f"RF-{n:04d}", f"Versión {n}") for n in range(21)]
    f, evds, clms = _ingesta(b, piezas)
    clm, = clms.values()
    assert f["_ps1"] and clm["raices_independientes"] == 1 and clm["ps1_cumple"]


def test_a08_h04_derivada_sin_original_ingerido_cumple_el_esquema_de_f2(tmp_path, universo):  # noqa: F811
    """H-04: esquema de F2 (§4): `raiz_evd_id` es obligatorio si no es RAIZ: «EVD- o "no identificada" con motivo».
    Veinte derivadas cuyo original no llega quedan con `raiz_evd_id = None`."""
    fichas = [_ficha("RF-0000")] + [_ficha(f"RF-{n:04d}", original="REF-RF-0000") for n in range(1, 21)]
    b = _bloque_con_f9(tmp_path, universo, fichas)
    f, evds, clms = _ingesta(b, [_pieza(f"RF-{n:04d}", f"Versión {n}") for n in range(1, 21)])
    clm, = clms.values()
    assert clm["raices_independientes"] == 0 and not f["_ps1"]
    for e in evds.values():
        assert e["grado_independencia"] == "DERIVADA"
        assert e["raiz_evd_id"] is not None and (str(e["raiz_evd_id"]).startswith("EVD-") or e.get("motivo_raiz"))


def test_a09_h04_derivada_de_otra_afirmacion_apunta_a_su_raiz(tmp_path, universo):  # noqa: F811
    """H-04: el original sustenta otra CLM (otra redacción de la afirmación): la derivada no se enlaza."""
    fichas = [_ficha("RF-0000"), _ficha("RF-0001", original="REF-RF-0000")]
    b = _bloque_con_f9(tmp_path, universo, fichas)
    _ingesta(b, [_pieza("RF-0000", "Original", "El PIB crece")])
    _, evds, _ = _ingesta(b, [_pieza("RF-0001", "Copia", "El producto interior crece")], run="RUN-2026-0002")
    raiz = next(e for e in evds.values() if e["ref_id"] == "REF-RF-0000")
    der = next(e for e in evds.values() if e["ref_id"] == "REF-RF-0001")
    assert der["raiz_evd_id"] == raiz["evd_id"]


def test_a10_h04_original_sin_prefijo_o_en_cadena(tmp_path, universo):  # noqa: F811
    """H-04: «Fuente original: RF-0000» (sin REF-) y una derivada de derivada deben apuntar a la raíz."""
    fichas = [_ficha("RF-0000"), _ficha("RF-0001", original="RF-0000"), _ficha("RF-0002", original="REF-RF-0001")]
    b = _bloque_con_f9(tmp_path, universo, fichas)
    _, evds, _ = _ingesta(b, [_pieza(r, r) for r in ("RF-0000", "RF-0001", "RF-0002")])
    raiz = next(e for e in evds.values() if e["ref_id"] == "REF-RF-0000")
    for r in ("REF-RF-0001", "REF-RF-0002"):
        assert next(e for e in evds.values() if e["ref_id"] == r)["raiz_evd_id"] == raiz["evd_id"], r


def test_a11_idempotencia_y_orden_entre_ciclos(tmp_path, universo):  # noqa: F811
    """Las derivadas llegan en un ciclo y el original en el siguiente; repetir la ingesta no duplica nada."""
    fichas = [_ficha("RF-0000")] + [_ficha(f"RF-{n:04d}", original="REF-RF-0000") for n in range(1, 21)]
    b = _bloque_con_f9(tmp_path, universo, fichas)
    _ingesta(b, [_pieza(f"RF-{n:04d}", f"Versión {n}") for n in range(1, 21)])
    piezas = [_pieza(f"RF-{n:04d}", f"Versión {n}") for n in range(21)]
    _ingesta(b, piezas, run="RUN-2026-0002")
    f, evds, clms = _ingesta(b, piezas, run="RUN-2026-0003")
    clm, = clms.values()
    assert len(evds) == 21 and clm["raices_independientes"] == 1 and not f["_ps1"]
    raiz, = (e for e in evds.values() if e["grado_independencia"] == "RAIZ")
    assert sum(e.get("raiz_evd_id") == raiz["evd_id"] for e in evds.values()) == 20


def test_a12_h06_veinte_medios_con_variaciones_menores_sin_metadatos(tmp_path, universo):  # noqa: F811
    """H-06: el caso del plan tal cual (un informe reproducido por 20 medios con variaciones menores), sin el campo
    «Fuente original», que ninguna ficha real de F9 tiene: hoy salen 21 raíces y PS1 superada."""
    fichas = [_ficha(f"RF-{n:04d}") for n in range(21)]
    b = _bloque_con_f9(tmp_path, universo, fichas)
    base = "El organismo X prevé que el PIB crezca un 3 % en 2026, según su informe trimestral"
    piezas = [_pieza(f"RF-{n:04d}", base + ("." if n == 0 else f" (medio {n}).")) for n in range(21)]
    f, evds, clms = _ingesta(b, piezas)
    clm, = clms.values()
    assert clm["raices_independientes"] == 1 and not f["_ps1"]
