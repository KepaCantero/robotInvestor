"""T-180 · hallazgos de la QA r01 de T-163 (`.docs/tickets/T-163/qa.md`).

- H-01: CT-04 (y con él `certificados_vigentes` y la revisión) exige que el cálculo de soporte del certificado lo pidiera el
  Evaluador (AG-20) y cumpla el criterio del certificado con los umbrales de la configuración (n_eff, extremo inferior del IC del
  BSS, ECE frente al q90 del nulo y frente al tope, p de DM-HLN ≤ α), con la materialidad si su CT-10 es DENTRO_TOLERANCIA. Con
  una sola celda candidata también se aplica Holm (la prueba de DM-HLN a α), para que la propuesta y CT-04 miren lo mismo.
- H-02: dos celdas de la misma clase en H2 y H3 con las mismas entradas tienen cada una su soporte (el horizonte va en la petición
  FC-EVAL-001 y, con él, en la clave de la caché del Motor).
- H-03: pruebas que matan los mutantes N03 (muestra efectiva), N04 (Brier de referencia) y N07 (lote con dos PROPUESTO de una
  celda) de `.docs/tickets/T-163/revisores/r01_02_mutantes.py`. Las de t53 y t66 que afirmaban «se revoca» afirman ahora por qué.

Todo con el cliente simulado y sin red. Cada prueba de fallo cerrado falla sin el cambio que cubre (ver pruebas.md del ticket).
"""
import copy

import numpy as np
import pandas as pd
import pytest
from bloque_a.evaluador import CAMPOS_MUESTRA, campos_certificado
from bloque_a.motor.servicio import Motor
from conftest import certificado_con_reejecucion, nuevo_bloque
from test_fase4_huecos import _sembrar_celda
from test_t160_reejecucion_certificado import (
    REVISION,
    TOL,
    _bloque,
    _certs,
    _incidencias,
)


def _propuesto(b):
    cert, = b.evaluador.revisar_certificados(REVISION)["emitidos"]
    assert cert["estado"] == "PROPUESTO" and b.evaluador.motivo_sin_reejecucion(cert) is None
    return cert


def _no_aprueba(b, ids, fragmento):
    """CT-04 rechaza con el motivo `fragmento` (expresión regular) y F6 no cambia."""
    n = len(b.almacen.leer("F6"))
    with pytest.raises(ValueError, match=f"re-ejecución CT-10 coincidente.*{fragmento}"):
        b.evaluador.aprobar_certificados(ids if isinstance(ids, list) else [ids], REVISION)
    assert len(b.almacen.leer("F6")) == n


def _debil(tmp_path, universo):
    """Una celda RV|H3 de habilidad débil (frecuencia real 0,5 + 0,6·(p − 0,5), 150 PRG en fechas distintas): BSS 0,053 con IC
    [−0,064; 0,16] y p de DM-HLN 0,20. No certifica; es la de H-01 de la QA r01 de T-163."""
    b = nuevo_bloque(tmp_path, universo)
    b.reloj.fijar(REVISION)
    _sembrar_celda(b, "RV", 150, lambda p: 0.5 + 0.6 * (p - 0.5), 5001)
    return b


def _soporte(b, celda, entradas, tasa_base, solicitante="AG-20", motor=None):
    """Lo que puede hacer quien tenga los permisos del Evaluador: pedir al Motor un FC-EVAL-001 de la celda con las entradas
    que quiera y su re-ejecución CT-10 como AG-20."""
    pet = {"operacion": "FC-EVAL-001", "plan": "PLAN_MIN", "clase": celda["clase"], "horizonte": celda["horizonte"],
           "datos": [{"valores": entradas}], "fecha_corte": REVISION,
           "parametros": {**b.evaluador._parametros_certificado(), "horizonte": celda["horizonte"], "tasa_base": tasa_base,
                          "metodo": celda.get("metodo")}}
    res = (motor or b.motor).servir(pet, solicitante)
    assert str(res["estado"]).startswith("SERVED"), res
    rex = b.motor.reejecutar(res["calc_id"], "prueba T-180", "AG-20")
    assert rex["coincide"] == "SI", rex
    return res, rex


def _forjar(b, cid, celda, res, rex, estado="PROPUESTO"):
    """Un CERT- en F6 con las cifras, el soporte, la huella y la CT-10 de `res` y `rex`: todo lo que T-163 ata, de verdad."""
    s = b.almacen.estado("RC")[res["calc_id"]]
    cert = {"tipo_entrada": "CERT", "id": cid, "estado": estado, "celda": dict(celda), **campos_certificado(res["resultado"]),
            "holm_superado": True, "calc_soporte": res["calc_id"], "curva_fiabilidad": res["calc_id"],
            "huella_entradas": s["datos"][0]["huella"], "reejecucion": rex["calc_id"]}
    b.almacen.escribir("F6", "AG-20", cert)
    return cert


def _soporte_de_las_entradas_reales(b):
    """El soporte y la CT-10 de las entradas reales (los PRG resueltos) de la celda RV|H3 de `_debil`."""
    k = ("RV", "H3", None)
    v = [p for p in b.evaluador.resueltos(REVISION) if (p["clase"], p["horizonte"], p.get("metodo")) == k]
    entradas, tb = b.evaluador._entradas_celda(v)
    return _soporte(b, {"clase": "RV", "horizonte": "H3", "metodo": None}, entradas, tb)


def _con_soporte_cambiado(b, c, cambio):
    """Contexto de `motivo_sin_reejecucion` con el `payload` del soporte de `c` cambiado por `cambio` (en memoria, sin tocar el
    Registro de cálculos) y un CERT- con las cifras de ese payload: solo cambia lo que mira el criterio."""
    ctx = b.evaluador._contexto_reejecucion()
    s = copy.deepcopy(ctx["rc"][c["calc_soporte"]])
    cambio(s["resultado"]["payload"])
    ctx["rc"][c["calc_soporte"]] = s
    return ctx, {**c, **campos_certificado(s["resultado"]["payload"])}


# ================================================================================ H-01 · el soporte cumple el criterio
def test_h01_ct04_no_aprueba_un_certificado_cuyo_soporte_no_cumple_el_criterio(tmp_path, universo):
    """El soporte y la CT-10 de las entradas reales de una celda de habilidad débil, escritos como AG-20: antes de T-180 el
    PROPUESTO entraba en vigor."""
    b = _debil(tmp_path, universo)
    res0 = b.evaluador.revisar_certificados(REVISION)
    assert res0["emitidos"] == [] and not res0["evaluadas"]["RV|H3"]["certificable"]          # la celda no certifica
    res, rex = _soporte_de_las_entradas_reales(b)
    falso = _forjar(b, "CERT-2026-0950", {"clase": "RV", "horizonte": "H3", "metodo": None}, res, rex)
    motivo = b.evaluador.motivo_sin_reejecucion(falso)
    assert "no cumple el criterio del certificado" in motivo and "extremo inferior del IC del BSS" in motivo, motivo
    assert "DM-HLN p = " in motivo and "> alfa Holm" in motivo, motivo
    _no_aprueba(b, falso["id"], f"{res['calc_id']} no cumple el criterio del certificado")
    assert b.evaluador.certificados_vigentes(REVISION) == []


def test_h01_la_revision_revoca_un_vigente_cuyo_soporte_no_cumple_el_criterio(tmp_path, universo):
    b = _debil(tmp_path, universo)
    res, rex = _soporte_de_las_entradas_reales(b)
    falso = _forjar(b, "CERT-2026-0951", {"clase": "RV", "horizonte": "H3", "metodo": None}, res, rex, estado="VIGENTE")
    assert b.evaluador._vigentes_en_f6(REVISION) and b.evaluador.certificados_vigentes(REVISION) == []    # no habilita
    r1 = b.evaluador.revisar_certificados(REVISION)
    assert r1["revocados"] == [falso["id"]] and "no cumple el criterio" in r1["vigentes_sin_reejecucion"][falso["id"]]
    cert = b.almacen.estado("F6", clave="id")[falso["id"]]
    assert cert["estado"] == "REVOCADO" and "no cumple el criterio del certificado" in cert["motivo_cambio"]
    assert r1["emitidos"] == []                                          # la celda se vuelve a evaluar y no certifica
    r2 = b.evaluador.revisar_certificados(REVISION)                    # idempotente
    assert r2["revocados"] == [] and r2["vigentes_sin_reejecucion"] == {}


@pytest.mark.parametrize("cambio, fragmento", [
    (lambda m: m.update(n_eff=99.9), "n_eff = 99.9 < 100"),
    (lambda m: m.update(n_eff=None), "n_eff no disponible"),
    (lambda m: m["bss"].update(ic=[0.0, m["bss"]["ic"][1]]), "extremo inferior del IC del BSS 0.0 ≤ 0"),
    (lambda m: m["bss"].update(ic=[-0.01, m["bss"]["ic"][1]]), "extremo inferior del IC del BSS -0.01 ≤ 0"),
    (lambda m: m["calibracion"].update(ece=m["ece_nulo"]["q90"] * 1.5), "> q90 nulo"),
    (lambda m: (m["calibracion"].update(ece=0.15), m["ece_nulo"].update(q90=0.3)), "ECE 0.15 ≥ 0.15"),
    (lambda m: m["dm_hln"].update(p_unilateral=0.2), "DM-HLN p = 0.2 > alfa Holm 0.1000"),
    (lambda m: m["dm_hln"].update(p_unilateral=None), "DM-HLN p = None > alfa Holm"),
])
def test_h01_cada_condicion_del_criterio_cuenta_en_el_soporte(tmp_path, universo, cambio, fragmento):
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    ctx, cert = _con_soporte_cambiado(b, c, lambda m: None)
    assert b.evaluador.motivo_sin_reejecucion(cert, ctx) is None                            # sin cambio, vale
    ctx, cert = _con_soporte_cambiado(b, c, cambio)
    motivo = b.evaluador.motivo_sin_reejecucion(cert, ctx)
    assert motivo and "no cumple el criterio del certificado" in motivo and fragmento in motivo, motivo


@pytest.mark.parametrize("cambio", [lambda m: m.update(n_eff=str(m["n_eff"])),
                                    lambda m: m["dm_hln"].update(p_unilateral=str(m["dm_hln"]["p_unilateral"]))])
def test_h01_un_soporte_con_cifras_de_otra_forma_no_lanza_y_no_vale(tmp_path, universo, cambio):
    """Una cifra del soporte que no es un número (igual en el CERT-, así que la comparación de T-163 no la marca): el criterio
    no se puede aplicar y el certificado no vale, sin excepción."""
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    ctx, cert = _con_soporte_cambiado(b, c, cambio)
    assert "no se pueden comprobar con el criterio del certificado (TypeError)" in b.evaluador.motivo_sin_reejecucion(cert, ctx)


@pytest.mark.parametrize("clave", ["min_certificar", "ece_max", "alfa_holm"])
def test_h01_los_umbrales_del_criterio_salen_de_la_configuracion(tmp_path, universo, clave):
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    pay = b.almacen.estado("RC")[c["calc_soporte"]]["resultado"]["payload"]
    valor, fragmento = {"min_certificar": (int(c["n_eff"]) + 1, f"< {int(c['n_eff']) + 1}"),
                        "ece_max": (c["ece"], f"≥ {c['ece']}"),
                        "alfa_holm": (pay["dm_hln"]["p_unilateral"] / 2, "> alfa Holm")}[clave]
    b.cfg["evaluacion"][clave] = valor
    assert fragmento in b.evaluador.motivo_sin_reejecucion(c)
    _no_aprueba(b, c["id"], "no cumple el criterio del certificado")
    del b.cfg["evaluacion"][clave]                                       # con el valor de la entrega, vuelve a valer
    assert b.evaluador.motivo_sin_reejecucion(c) is None


def test_h01_ct04_no_aprueba_un_soporte_que_no_pidio_el_evaluador(tmp_path, universo):
    """La misma petición servida por otro Motor (sin caché) a AG-18 y a AG-20, cada una con su CT-10 del Evaluador: solo cambia
    el solicitante del soporte."""
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    s = b.almacen.estado("RC")[c["calc_soporte"]]
    entradas, tb = s["datos"][0]["valor"], s["parametros"]["tasa_base"]
    otro = Motor(b.almacen, None, b.cfg)
    res18, rex18 = _soporte(b, c["celda"], entradas, tb, "AG-18", motor=otro)
    assert res18["calc_id"] != c["calc_soporte"] and res18["resultado"] == s["resultado"]["payload"]
    f18 = _forjar(b, "CERT-2026-0952", c["celda"], res18, rex18)
    assert b.evaluador.motivo_sin_reejecucion(f18) == f"{res18['calc_id']} no lo pidió el Evaluador (AG-20), sino AG-18"
    _no_aprueba(b, f18["id"], "no lo pidió el Evaluador")
    res20, rex20 = _soporte(b, c["celda"], entradas, tb, "AG-20", motor=Motor(b.almacen, None, b.cfg))
    assert b.evaluador.motivo_sin_reejecucion(_forjar(b, "CERT-2026-0953", c["celda"], res20, rex20)) is None   # control


def test_h01_con_una_ct10_dentro_de_tolerancia_el_soporte_se_mira_con_la_materialidad(tmp_path, universo):
    """ECE del soporte a media tolerancia por debajo del q90 del nulo: cumple con la CT-10 «SI»; con DENTRO_TOLERANCIA, movidas las
    cifras en contra lo que permite su tolerancia (como al proponer), ya no."""
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    ctx, cert = _con_soporte_cambiado(b, c, lambda m: m["calibracion"].update(ece=m["ece_nulo"]["q90"] * (1 - TOL / 2)))
    assert b.evaluador.motivo_sin_reejecucion(cert, ctx) is None
    r = copy.deepcopy(ctx["rc"][c["reejecucion"]])
    r["reejecucion"]["coincide"] = "DENTRO_TOLERANCIA"
    ctx["rc"][c["reejecucion"]] = r
    motivo = b.evaluador.motivo_sin_reejecucion(cert, ctx)
    assert motivo and "DENTRO_TOLERANCIA" in motivo and "> q90 nulo" in motivo, motivo
    ctx2, cert2 = _con_soporte_cambiado(b, c, lambda m: None)            # lejos del umbral, DENTRO_TOLERANCIA también vale
    ctx2["rc"][c["reejecucion"]] = r
    assert b.evaluador.motivo_sin_reejecucion(cert2, ctx2) is None


def test_h01_con_una_sola_celda_candidata_tambien_se_aplica_holm(tmp_path, universo):
    """Una sola celda hábil (p de DM-HLN 7·10⁻⁴) con α = 10⁻⁴: Holm con una hipótesis es la prueba a α y no se propone. Antes de
    T-180 no se miraba la p con una celda (se habría propuesto, o con la comprobación de CT-04 nueva habría dejado una incidencia
    Material en cada revisión)."""
    b = _bloque(tmp_path, universo)
    b.cfg["evaluacion"]["alfa_holm"] = 1e-4
    res = b.evaluador.revisar_certificados(REVISION)
    crit = res["evaluadas"]["RF|H3"]
    assert res["emitidos"] == [] and not _certs(b) and not crit["certificable"]
    assert [m for m in crit["motivos"]] == [m for m in crit["motivos"] if m.startswith("DM-HLN p = ")] == crit["motivos"][:1]
    assert "> alfa Holm 0.0001" in crit["motivos"][0]
    assert res["sin_reejecucion_coincidente"] == {} and not _incidencias(b, "RF|H3")
    del b.cfg["evaluacion"]["alfa_holm"]                                 # con el α de la entrega (0,10) se propone
    cert, = b.evaluador.revisar_certificados(REVISION)["emitidos"]
    assert cert["holm_superado"] is True and b.evaluador.motivo_sin_reejecucion(cert) is None


def test_h01_el_ayudante_de_pruebas_escribe_un_certificado_que_cumple_el_criterio(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.reloj.fijar(REVISION)
    celda = {"clase": "RV", "horizonte": "H2", "metodo": "ACC-MOM-001"}
    cert = certificado_con_reejecucion(b.almacen, celda, "CERT-2026-0954", motor=b.motor)
    assert cert["n_eff"] >= b.cfg["evaluacion"]["min_certificar"] and cert["bss_ic90"][0] > 0
    assert b.evaluador.motivo_sin_reejecucion(cert) is None
    assert [x["id"] for x in b.evaluador.certificados_vigentes(REVISION)] == ["CERT-2026-0954"]
    assert b.almacen.estado("RC")[cert["calc_soporte"]]["parametros"]["horizonte"] == "H2"


def test_limite_declarado_un_soporte_con_entradas_inventadas_que_cumplen_el_criterio_entra(tmp_path, universo):
    """INC-T160-01: se ata el certificado a su soporte y el soporte al criterio, no el soporte a los PRG de la celda. Con los
    permisos del Evaluador, unas entradas inventadas que cumplen el criterio pasan CT-04 en una celda sin habilidad. Documenta el
    límite (pasa); si algún día se atan las entradas a F4, esta prueba tiene que cambiar."""
    b = _bloque(tmp_path, universo, clases=(("RV", "azar"),))
    assert b.evaluador.revisar_certificados(REVISION)["emitidos"] == []
    falso = certificado_con_reejecucion(b.almacen, {"clase": "RV", "horizonte": "H3", "metodo": None}, "CERT-2026-0955",
                                        estado="PROPUESTO", motor=b.motor)
    assert [h["id"] for h in b.evaluador.aprobar_certificados([falso["id"]], REVISION)] == [falso["id"]]


# ================================================================================ H-02 · el horizonte en la petición
def _sembrar(b, clase, horizonte, n, desde):
    """Como `_sembrar_celda` de test_fase4_huecos (pronosticador hábil, misma semilla), con el horizonte como parámetro."""
    rng = np.random.default_rng(1)
    for i in range(n):
        p = float(rng.choice([0.3, 0.7]))
        o = int(rng.random() < p)
        pid = f"PRG-2026-{desde + i:04d}"
        b.almacen.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": pid, "clase": clase, "horizonte": horizonte,
                                           "prob_interna": p, "referencia_ingenua": {"valor_o_prob": 0.5}, "en_informe": True,
                                           "sentido": "POSITIVO", "fecha_emision": "2025-01-02", "estado": "ABIERTO",
                                           "fecha_resolucion": str((pd.Timestamp("2025-07-02") + pd.offsets.BDay(i)).date())})
        b.almacen.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": pid, "estado": "RESUELTO",
                                           "resolucion": {"resultado_binario": o, "valor_observado": 0.01,
                                                          "comprobacion_fuga": "SUPERADA", "fecha_resuelto": "2025-07-02"}})


def test_h02_dos_horizontes_con_las_mismas_entradas_tienen_cada_uno_su_soporte(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.reloj.fijar(REVISION)
    _sembrar(b, "RF", "H3", 150, 5001)
    _sembrar(b, "RF", "H2", 150, 6001)                                   # mismas p, resultados y fechas
    res = b.evaluador.revisar_certificados(REVISION)
    assert res["sin_reejecucion_coincidente"] == {} and not _incidencias(b, "RF|H2")
    certs = {c["celda"]["horizonte"]: c for c in res["emitidos"]}
    assert set(certs) == {"H2", "H3"}
    h2, h3 = certs["H2"], certs["H3"]
    assert h2["huella_entradas"] == h3["huella_entradas"] and h2["calc_soporte"] != h3["calc_soporte"]
    rc = b.almacen.estado("RC")
    for h, c in certs.items():
        s = rc[c["calc_soporte"]]
        assert (s["horizonte"], s["parametros"]["horizonte"], s["tipo_entrada"]) == (h, h, "SERVICIO")
    assert sorted(x["id"] for x in b.evaluador.aprobar_certificados([h2["id"], h3["id"]], REVISION)) == sorted([h2["id"], h3["id"]])
    assert {x["celda"]["horizonte"] for x in b.evaluador.certificados_vigentes(REVISION)} == {"H2", "H3"}


# ================================================================================ H-03 · mutantes N03, N04 y N07
@pytest.mark.parametrize("campo, cambio", [*[("muestra_efectiva", k) for k in CAMPOS_MUESTRA], ("brier_ref", None)])
def test_h03_n03_n04_ct04_compara_la_muestra_efectiva_y_el_brier_de_referencia(tmp_path, universo, campo, cambio):
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    if campo == "muestra_efectiva":
        nuevo = {**c["muestra_efectiva"], cambio: c["muestra_efectiva"][cambio] * 1.001 + 0.5}
    else:
        nuevo = c["brier_ref"] * 1.001
    e = {k: v for k, v in c.items() if not k.startswith("_")}
    b.almacen.escribir("F6", "AG-20", {**e, campo: nuevo})
    _no_aprueba(b, c["id"], f"las cifras del certificado no son las de .*{campo}")
    assert b.evaluador.certificados_vigentes(REVISION) == []


def test_h03_n07_un_lote_con_dos_propuestos_validos_de_la_misma_celda_no_aprueba_ninguno(tmp_path, universo):
    """Dos PROPUESTO de la celda RF|H3, cada uno con su soporte, su CT-10 y un criterio que se cumple: en un lote, en los dos
    órdenes, CT-04 no aprueba ninguno; uno a uno, el primero entra y el segundo no (la celda ya tiene un VIGENTE)."""
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    otro = certificado_con_reejecucion(b.almacen, c["celda"], "CERT-2026-0956", estado="PROPUESTO", motor=b.motor)
    assert b.evaluador.motivo_sin_reejecucion(otro) is None and b.evaluador.motivo_sin_reejecucion(c) is None
    for lote in ([c["id"], otro["id"]], [otro["id"], c["id"]]):
        n = len(b.almacen.leer("F6"))
        with pytest.raises(ValueError, match="ya tiene un certificado VIGENTE"):
            b.evaluador.aprobar_certificados(lote, REVISION)
        assert len(b.almacen.leer("F6")) == n and b.evaluador.certificados_vigentes(REVISION) == []
    assert [h["id"] for h in b.evaluador.aprobar_certificados([c["id"]], REVISION)] == [c["id"]]
    with pytest.raises(ValueError, match="ya tiene un certificado VIGENTE"):
        b.evaluador.aprobar_certificados([otro["id"]], REVISION)
    assert [x["id"] for x in b.evaluador.certificados_vigentes(REVISION)] == [c["id"]]
    assert b.evaluador.revisar_certificados(REVISION)["emitidos"] == []        # y la revisión no propone un tercero


# ------------------------------------------------------------- ronda de cierre (QA r01 de T-180, H-01, baja)
def test_cierre_h01_en_el_borde_ct04_no_es_mas_estricto_que_la_propuesta(tmp_path, universo):
    """QA r01 de T-180, H-01 (mutante V01 de `revisores/r01_02_mutantes.py`). El ECE del soporte queda a q90·(1 − 3·tol) con la
    CT-10 DENTRO_TOLERANCIA. Con un paso de holgura, el que aguantó la propuesta, cumple; con dos, no. Un CT-04 más estricto
    que la propuesta revocaría certificados legítimos en el borde."""
    b = _bloque(tmp_path, universo)
    c = _propuesto(b)
    ctx = b.evaluador._contexto_reejecucion()
    s = copy.deepcopy(ctx["rc"][c["calc_soporte"]])
    m = s["resultado"]["payload"]
    m["calibracion"]["ece"] = m["ece_nulo"]["q90"] * (1 - 3 * TOL)
    ctx["rc"][c["calc_soporte"]] = s
    cert = {**c, **campos_certificado(m)}
    r = copy.deepcopy(ctx["rc"][c["reejecucion"]])
    r["reejecucion"]["coincide"] = "DENTRO_TOLERANCIA"
    ctx["rc"][c["reejecucion"]] = r
    assert b.evaluador.motivo_sin_reejecucion(cert, ctx) is None
