"""T-125 · Ronda r02: correcciones de la QA r01 (`.docs/tickets/T-125/qa.md`), H-01 a H-08.

- H-01: el bloque `pronostico_fuente` de una afirmación del Analista o de una referencia del Buscador llega a F2 y el camino
  entero (Analista/Buscador → F2 → Evaluador → FUE- → CT-19) funciona en ciclos.
- H-02: una fecha con zona horaria se lee sin zona; un fallo de la fiabilidad no tumba el resto del C5.
- H-03: solo cuenta un pronóstico registrado en F2 antes de su fecha objetivo. H-04: su fuente es una fuente de F9.
- H-05: el mismo pronóstico en dos afirmaciones cuenta una vez. H-06: una FUE- por fuente y mes.
- H-07: ventana, antigüedad del cierre, no vencidos, bordes de «dentro», tope de puntos y probabilidades 0 y 1.
- H-08: la probabilidad sin declarar es la de la banda «más probable que no»; la FUE- lleva el `calc_id` del Motor.
"""
import pandas as pd
import pytest
from bloque_a.almacen import Almacen
from bloque_a.configuracion import parametro
from bloque_a.evaluador import Evaluador, motivo_pronostico_fuente_no_registrable
from bloque_a.herramientas.ht01_datos import ProveedorCSV
from bloque_a.referencias import Referencias
from conftest import AS_OF, DATOS, config_pruebas, nuevo_bloque

from bloque_a import mock_respuestas

SERIE = "SPY"
FUENTE_A, FUENTE_B = "REF-RF-0001", "REF-RF-0003"          # fuentes registradas en F9


def _bloque(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    return b


def _pf(ref_id, objetivo, umbral, direccion="por_encima", prob=0.7, emision=None, serie=SERIE):
    pf = {"ref_id": ref_id, "variable": "cierre", "serie_ht01": serie, "fecha_objetivo": objetivo, "umbral_o_rango": umbral,
          "direccion": direccion, "probabilidad": prob,
          "fecha_emision": emision or str((pd.Timestamp(str(objetivo)[:10]) - pd.Timedelta(days=30)).date())}
    if prob is None:
        pf.pop("probabilidad")
    return pf


def _clm(b, clm_id, pf, registro=None, texto=None):
    """Una CLM PRONOSTICO_FUENTE escrita en F2 con el reloj en su fecha de registro (por defecto, la de emisión)."""
    reloj = b.almacen.reloj
    reloj.fijar(registro or str(pf["fecha_emision"])[:10])
    try:
        b.almacen.escribir("F2", "AG-12", {"tipo_entrada": "CLM", "clm_id": clm_id, "afirmacion": texto or f"{pf['ref_id']} · {clm_id}",
                                           "tipo_afirmacion": "PRONOSTICO_FUENTE", "evidencias": [], "pronostico_fuente": pf})
    finally:
        reloj.fijar(AS_OF)


def _sembrar(b, ref_id, aciertos, fallos, prob=0.7, desde="2025-01-06", inicio=1):
    for i, f in enumerate(pd.bdate_range(desde, periods=aciertos + fallos)):
        _, v = b.proveedor.valor_en(SERIE, f)
        _clm(b, f"CLM-2025-{inicio + i:04d}", _pf(ref_id, str(f.date()), v - 1 if i < aciertos else v + 1, prob=prob))


def _cuentan(b, pf, registro=None, clm_id="CLM-2025-0900"):
    _clm(b, clm_id, pf, registro)
    return [p["clm_id"] for p in b.evaluador.pronosticos_de_fuentes(AS_OF)] == [clm_id]


def _valor(b, fecha):
    return b.proveedor.valor_en(SERIE, fecha)[1]


# ---------------------------------------------------------------- H-01 · camino entero en ciclos
def _vivo(tmp_path, universo):
    """En modo vivo: en backtest, las fuentes de F9 sin fecha no son accesibles (`_filtrar_evidencia`) y no entra ninguna."""
    return nuevo_bloque(tmp_path, universo, cfg=config_pruebas(modo="vivo"))


def _analista_con_pronosticos(monkeypatch, ref_id=FUENTE_A):
    """El Analista simulado devuelve en cada finalista dos afirmaciones con un pronóstico explícito de `ref_id` (lo más que
    puede hacer el modelo real), con fecha objetivo 10 y 20 días hábiles después del ciclo."""
    original = mock_respuestas._ficha

    def ficha(u, msg, ctx, rng, inyectado):
        f = original(u, msg, ctx, rng, inyectado)
        sym = f["indicador_seguimiento"]["simbolo"]
        hoy = pd.Timestamp(ctx["fecha_as_of"])
        for k in (10, 20):
            obj = str((hoy + pd.offsets.BDay(k)).date())
            f["afirmaciones"].append({"afirmacion": f"{ref_id} prevé {sym} por encima de 1 el {obj}", "fuente": ref_id, "direccion": "favorable",
                                      "pronostico_fuente": _pf(ref_id, obj, 1.0, prob=0.8, emision=str(hoy.date()), serie=sym)})
        return f
    monkeypatch.setattr(mock_respuestas, "_ficha", ficha)


def test_r02_h01_del_analista_a_f2_al_evaluador_a_la_fue_y_al_ct19(tmp_path, universo, monkeypatch):
    _analista_con_pronosticos(monkeypatch)
    b = _vivo(tmp_path, universo)
    r1 = b.ciclo("2026-04-03", alcance={"clases": ["RV"]})
    f2 = [c for c in b.almacen.estado("F2", clave="clm_id").values() if c.get("tipo_entrada") == "CLM"]
    con_bloque = [c for c in f2 if c.get("tipo_afirmacion") == "PRONOSTICO_FUENTE" and isinstance(c.get("pronostico_fuente"), dict)]
    assert r1["estado"] in ("COMPLETO", "PARCIAL") and len(con_bloque) >= 5                     # llegan a F2 con su bloque
    evd = {e["evd_id"]: e for e in b.almacen.estado("F2", clave="evd_id").values() if e.get("tipo_entrada") == "EVD"}
    assert all(any(evd[x]["ref_id"] == FUENTE_A for x in c["evidencias"]) for c in con_bloque)   # con su fuente como evidencia
    assert r1["evaluacion"]["fiabilidad_fuentes"] == []                                         # aún no han vencido
    r2 = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    fue = r2["evaluacion"]["fiabilidad_fuentes"]
    assert [f["ref_id"] for f in fue] == [FUENTE_A] and fue[0]["n"] == len(con_bloque) and fue[0]["calc_id"]
    assert set(fue[0]["pronosticos"]) == {c["clm_id"] for c in con_bloque}
    f6 = b.almacen.estado("F6", clave="id")[fue[0]["fue_id"]]
    ct19 = [m for m in b.mensajeria.registro if m["contrato"] == "CT-19" and m["receptor"] == "AG-16"]
    assert len(ct19) == 1 and f6["comunicado_ct19"] == ct19[0]["msg_id"]


def test_r02_h01_la_referencia_del_buscador_trae_su_pronostico_a_f2(tmp_path, universo, monkeypatch):
    original = mock_respuestas._analista

    def analista(msg, ctx, rng, inyectado):
        r = original(msg, ctx, rng, inyectado)
        for f in r.get("finalistas", []):   # una petición CT-07 al Buscador de Fuentes (F9)
            f["peticiones_conocimiento"] = [{"tipo": "CT-07", "pregunta": "¿Qué prevén las fuentes?", "objetivo": "confirmar"}]
        return r

    def busqueda(msg, ctx, rng):
        hoy = pd.Timestamp(ctx["fecha_as_of"])
        obj = str((hoy + pd.offsets.BDay(15)).date())
        refs = [{"ref_id": r["ref_id"], "afirmacion": f"{r['ref_id']} prevé {msg['para']} por encima de 1 el {obj}", "direccion": "favorable",
                 "pronostico_fuente": _pf(r["ref_id"], obj, 1.0, emision=str(hoy.date()), serie=msg["para"])}
                for r in (msg.get("referencias_candidatas") or [])[:1]]
        return {"referencias": refs, "sintesis": "Pronósticos registrados.", "contradicciones": [], "lagunas": []}
    monkeypatch.setattr(mock_respuestas, "_analista", analista)
    monkeypatch.setattr(mock_respuestas, "_busqueda", busqueda)
    b = _vivo(tmp_path, universo)
    b.ciclo("2026-04-03", alcance={"clases": ["RV"]})
    pfs = [c for c in b.almacen.estado("F2", clave="clm_id").values() if isinstance(c.get("pronostico_fuente"), dict)]
    assert pfs and all(c["tipo_afirmacion"] == "PRONOSTICO_FUENTE" for c in pfs)
    assert all(b.referencias.por_id(c["pronostico_fuente"]["ref_id"])["archivo"] == "F9" for c in pfs)


def test_r02_h01_un_bloque_no_registrable_no_entra_y_queda_en_ha(tmp_path, universo, monkeypatch):
    """El caso del revisor (`r01_03`): un bloque con fecha objetivo ya pasada y de otra fuente que la de la pieza no se
    guarda; la afirmación queda como PREVISION y el rechazo, con su motivo, en HA."""
    original, curador = mock_respuestas._ficha, mock_respuestas._curador

    def ficha(u, msg, ctx, rng, inyectado):
        f = original(u, msg, ctx, rng, inyectado)
        for a in f["afirmaciones"]:
            a["pronostico_fuente"] = _pf(FUENTE_A, "2025-06-02", 1.0, emision="2025-05-01")
        return f

    def cur(msg, ctx, rng):
        r = curador(msg, ctx, rng)
        for p in r["piezas"]:
            p["tipo_afirmacion"] = "PRONOSTICO_FUENTE"
        return r
    monkeypatch.setattr(mock_respuestas, "_ficha", ficha)
    monkeypatch.setattr(mock_respuestas, "_curador", cur)
    b = _vivo(tmp_path, universo)
    b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    clm = [c for c in b.almacen.estado("F2", clave="clm_id").values() if c.get("tipo_entrada") == "CLM"]
    assert clm and not [c for c in clm if c.get("pronostico_fuente") or c["tipo_afirmacion"] == "PRONOSTICO_FUENTE"]
    incs = [e["detalle"] for e in b.almacen.leer("HA") if e.get("tipo") == "DATOS" and "Pronóstico de fuente no registrable" in e.get("detalle", "")]
    assert incs and all("posterior al registro" in d or "no es la fuente de la pieza" in d for d in incs)


@pytest.mark.parametrize("cambio, motivo", [
    ({}, None),
    ({"ref_id": "REF-ANA-DOC-0061"}, "no es una fuente registrada en F9"),              # F7, no F9
    ({"ref_id": "REF-9999"}, "no es una fuente registrada en F9"),
    ({"fecha_objetivo": "2026-06-05"}, "posterior al registro"),                        # objetivo = registro
    ({"fecha_emision": "2026-06-06"}, "emitido después de la fecha de registro"),
    ({"probabilidad": 1.0}, "probabilidad"), ({"direccion": "sube"}, "dirección"), ({"umbral_o_rango": [2, 1], "direccion": "dentro"}, "umbral"),
    ({"fecha_objetivo": 20260701}, "faltan campos"),
])
def test_r02_h01_que_bloque_puede_registrarse(cambio, motivo):
    refs = Referencias(config_pruebas())
    pf = {**_pf(FUENTE_A, "2026-07-01", 1.0, emision="2026-06-01"), **cambio}
    m = motivo_pronostico_fuente_no_registrable(pf, pf["ref_id"], AS_OF, refs)
    assert (m is None) if motivo is None else (motivo in m)
    assert "no es la fuente de la pieza" in motivo_pronostico_fuente_no_registrable(_pf(FUENTE_A, "2026-07-01", 1.0, emision="2026-06-01"),
                                                                                    FUENTE_B, AS_OF, refs)


# ---------------------------------------------------------------- H-02 · zona horaria
@pytest.mark.parametrize("objetivo", ["2025-06-02T10:00:00+05:00", "2025-06-02T23:30:00Z", "2025-06-02T23:59:00", "2025-06-02"])
def test_r02_h02_una_fecha_con_zona_u_hora_cuenta_sin_excepcion(tmp_path, universo, objetivo):
    b = _bloque(tmp_path, universo)
    ps = None
    _clm(b, "CLM-2025-0001", _pf(FUENTE_A, objetivo, _valor(b, "2025-06-02") - 1, emision="2025-05-01T09:00:00+02:00"), "2025-05-01")
    ps = b.evaluador.pronosticos_de_fuentes(AS_OF)
    assert [(p["fecha_objetivo"], p["resultado"]) for p in ps] == [("2025-06-02", 1)]


def test_r02_h02_una_pieza_con_zona_no_tumba_el_c5_del_ciclo(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    _sembrar(b, FUENTE_A, 5, 0)
    _clm(b, "CLM-2025-0900", _pf(FUENTE_B, "2025-06-02T10:00:00+05:00", 1.0, emision="2025-05-01"), "2025-05-01")
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert "error" not in r["evaluacion"] and [f["ref_id"] for f in r["evaluacion"]["fiabilidad_fuentes"]] == [FUENTE_A]
    assert not [e for e in b.almacen.leer("HA") if e.get("tipo") == "HERRAMIENTA" and "Evaluador" in e.get("detalle", "")]


def test_r02_h02_si_la_fiabilidad_falla_el_resto_del_c5_sigue(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)

    def rota(as_of):
        raise TypeError("fallo simulado")
    monkeypatch.setattr(b.evaluador, "fiabilidad_fuentes", rota)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert "error" not in r["evaluacion"] and r["evaluacion"]["fiabilidad_fuentes"] == [] and "metricas" in r["evaluacion"]
    assert [e["detalle"] for e in b.almacen.leer("HA") if e.get("tipo") == "HERRAMIENTA"] == [
        "Fiabilidad de las fuentes no calculada en este ciclo: fallo simulado"]


# ---------------------------------------------------------------- H-03 · conocibilidad
@pytest.mark.parametrize("registro, cuenta", [("2025-05-01", True), ("2025-06-01", True), ("2025-06-02", False),
                                              ("2026-06-05", False), ("2025-04-30", False)])
def test_r02_h03_solo_cuenta_lo_registrado_antes_de_su_fecha_objetivo(tmp_path, universo, registro, cuenta):
    b = _bloque(tmp_path, universo)
    assert _cuentan(b, _pf(FUENTE_A, "2025-06-02", _valor(b, "2025-06-02") - 1, emision="2025-05-01"), registro) is cuenta


def test_r02_h03_cuenta_el_bloque_tal_como_se_registro(tmp_path, universo):
    """Una reescritura posterior del bloque (otra fecha objetivo u otro umbral, ya conocido el resultado) no cuenta."""
    b = _bloque(tmp_path, universo)
    v = _valor(b, "2025-06-02")
    _clm(b, "CLM-2025-0001", _pf(FUENTE_A, "2025-06-02", v + 1, emision="2025-05-01"))        # falla
    _clm(b, "CLM-2025-0001", _pf(FUENTE_A, "2025-06-02", v - 1, emision="2025-05-01"), "2026-06-05")   # «corregido» después
    assert [p["resultado"] for p in b.evaluador.pronosticos_de_fuentes(AS_OF)] == [0]


# ---------------------------------------------------------------- H-04 · la fuente es de F9
def test_r02_h04_un_ref_id_que_no_es_una_fuente_de_f9_no_cuenta(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    for k, ref in enumerate(["cualquier cosa", "OPP-2026-0001", "REF-9999", "REF-ANA-DOC-0061", "RF-0001"]):
        _sembrar(b, ref, 5, 0, inicio=1 + 100 * k)
    assert b.evaluador.pronosticos_de_fuentes(AS_OF) == [] and b.evaluador.fiabilidad_fuentes(AS_OF) == []
    _sembrar(b, FUENTE_A, 5, 0, inicio=900)
    assert [f["ref_id"] for f in b.evaluador.fiabilidad_fuentes(AS_OF)] == [FUENTE_A]


def test_r02_h04_sin_registro_de_referencias_no_cuenta_ninguno(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    _sembrar(b, FUENTE_A, 5, 0)
    ev = Evaluador(b.almacen, b.proveedor, b.motor, b.cfg, b.universo)            # sin `referencias`
    assert ev.pronosticos_de_fuentes(AS_OF) == []


# ---------------------------------------------------------------- H-05 · el mismo pronóstico en dos afirmaciones
def test_r02_h05_el_mismo_pronostico_en_dos_afirmaciones_cuenta_una_vez(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    for i, d in enumerate(pd.bdate_range("2025-01-06", periods=5)):
        for rep in range(2):
            _clm(b, f"CLM-2025-{1 + 2 * i + rep:04d}", _pf(FUENTE_A, str(d.date()), _valor(b, d) - 1, emision="2024-12-01"),
                 texto=f"{FUENTE_A} dice {i} (mención {rep})")
    fue = b.evaluador.fiabilidad_fuentes(AS_OF)
    assert [(f["n"], f["pronosticos"]) for f in fue] == [(5, [f"CLM-2025-{1 + 2 * i:04d}" for i in range(5)])]


# ---------------------------------------------------------------- H-06 · una FUE- por fuente y mes
def test_r02_h06_una_fuente_que_llega_a_la_muestra_a_mitad_de_mes_sale_ese_mes(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    _sembrar(b, FUENTE_A, 5, 0)
    assert [f["ref_id"] for f in b.evaluador.fiabilidad_fuentes(AS_OF)] == [FUENTE_A]
    _sembrar(b, FUENTE_B, 5, 0, inicio=500)
    b.fijar_fecha("2026-06-12")
    assert [f["ref_id"] for f in b.evaluador.fiabilidad_fuentes("2026-06-12")] == [FUENTE_B]     # la A no se repite en junio
    assert b.evaluador.fiabilidad_fuentes("2026-06-19") == []
    b.fijar_fecha("2026-07-03")
    assert [f["ref_id"] for f in b.evaluador.fiabilidad_fuentes("2026-07-03")] == [FUENTE_A, FUENTE_B]


# ---------------------------------------------------------------- H-07 · las reglas que no tenían prueba
def test_r02_h07_ventana_de_24_meses_con_su_borde(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    meses = parametro(b.cfg, "fiabilidad_fuentes.ventana_meses")
    borde = pd.Timestamp(AS_OF) - pd.DateOffset(months=meses)
    fuera = borde - pd.Timedelta(days=1)
    assert _cuentan(b, _pf(FUENTE_A, str(borde.date()), _valor(b, borde) - 1), clm_id="CLM-2025-0001")
    b2 = _bloque(tmp_path / "b", universo)
    assert not _cuentan(b2, _pf(FUENTE_A, str(fuera.date()), _valor(b2, fuera) - 1))           # hay dato, pero fuera de la ventana


def test_r02_h07_no_cuenta_lo_que_no_ha_vencido_aunque_haya_cierre(tmp_path, universo):
    """La regla no depende de que el proveedor recorte en `as_of`: con datos hasta una semana después, un pronóstico que
    vence después del corte de la evaluación no cuenta en ese corte (sí en el suyo)."""
    b = _bloque(tmp_path, universo)
    b.proveedor.fijar_as_of("2026-06-12")
    lunes = "2026-06-08"
    assert b.proveedor.valor_en(SERIE, lunes)[0] == pd.Timestamp(lunes)                       # hay cierre de ese día
    _clm(b, "CLM-2025-0001", _pf(FUENTE_A, lunes, 1.0, emision="2026-05-01"))
    assert b.evaluador.pronosticos_de_fuentes(AS_OF) == []
    assert [p["clm_id"] for p in b.evaluador.pronosticos_de_fuentes("2026-06-12")] == ["CLM-2025-0001"]


def test_r02_h07_no_cuenta_lo_emitido_en_su_fecha_objetivo(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    assert not _cuentan(b, _pf(FUENTE_A, "2025-06-02", 1.0, emision="2025-06-02"), "2025-06-02")


def test_r02_h07_antiguedad_del_cierre_con_su_borde(tmp_path):
    datos = tmp_path / "datos"
    datos.mkdir()
    df = pd.read_csv(DATOS / f"{SERIE}.csv")
    df[(df["fecha"] <= "2025-05-26") | (df["fecha"] > "2025-06-06")].to_csv(datos / f"{SERIE}.csv", index=False)   # hueco
    cfg = config_pruebas()
    dias = int(parametro(cfg, "ps2_antiguedad_maxima_dias.H2"))
    prov = ProveedorCSV(datos)
    prov.fijar_as_of(AS_OF)
    alm = Almacen(tmp_path / "estado")
    ev = Evaluador(alm, prov, None, cfg, None, referencias=Referencias(cfg))
    ultimo = pd.Timestamp("2025-05-26")
    for i, (obj, cuenta) in enumerate([(ultimo + pd.Timedelta(days=dias), True), (ultimo + pd.Timedelta(days=dias + 1), False)]):
        alm.reloj.fijar("2025-05-01")
        alm.escribir("F2", "AG-12", {"tipo_entrada": "CLM", "clm_id": f"CLM-2025-000{i}", "afirmacion": f"x{i}", "tipo_afirmacion": "PRONOSTICO_FUENTE",
                                     "pronostico_fuente": _pf(FUENTE_A, str(obj.date()), 1.0, emision="2025-05-01")})
    assert [p["clm_id"] for p in ev.pronosticos_de_fuentes(AS_OF)] == ["CLM-2025-0000"]


@pytest.mark.parametrize("direccion, desde, ocurre", [("dentro", 0, 1), ("dentro", -1, 1), ("fuera", 0, 0), ("fuera", -1, 0)])
def test_r02_h07_los_bordes_del_rango_estan_dentro(tmp_path, universo, direccion, desde, ocurre):
    b = _bloque(tmp_path, universo)
    v = _valor(b, "2025-06-02")
    rango = [v, v + 1] if desde == 0 else [v - 1, v]                                           # el valor justo en un borde
    _clm(b, "CLM-2025-0001", _pf(FUENTE_A, "2025-06-02", rango, direccion=direccion))
    assert [p["resultado"] for p in b.evaluador.pronosticos_de_fuentes(AS_OF)] == [ocurre]


@pytest.mark.parametrize("prob", [0, 1, 0.0, 1.0])
def test_r02_h07_una_probabilidad_de_0_o_1_no_cuenta(tmp_path, universo, prob):
    b = _bloque(tmp_path, universo)
    assert not _cuentan(b, _pf(FUENTE_A, "2025-06-02", 1.0, prob=prob))


def test_r02_h07_los_puntos_no_bajan_de_0(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    _sembrar(b, FUENTE_A, 0, 25, prob=0.99)                                                  # siempre 0,99 y siempre falla
    f = b.evaluador.fiabilidad_fuentes(AS_OF)[0]
    assert f["bss_contraido"] < -1 and f["puntos_historial"] == 0


# ---------------------------------------------------------------- H-08 · probabilidad sin declarar y calc_id
def test_r02_h08_la_probabilidad_sin_declarar_es_la_de_la_banda_y_la_fue_lleva_calc_id(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    assert parametro(b.cfg, "fiabilidad_fuentes.prob_sin_declarar") == b.evaluador.prob_de_banda["MAS_PROBABLE_QUE_NO"]
    _sembrar(b, FUENTE_A, 5, 0, prob=None)
    assert {p["prob"] for p in b.evaluador.pronosticos_de_fuentes(AS_OF)} == {b.evaluador.prob_de_banda["MAS_PROBABLE_QUE_NO"]}
    f = b.evaluador.fiabilidad_fuentes(AS_OF)[0]
    rc = [r for r in b.almacen.leer("RC") if r.get("tipo_entrada") == "SERVICIO" and r.get("calc_id") == f["calc_id"]]
    assert f["calc_id"] and [r["operacion"]["ficha_id"] for r in rc] == ["FC-EVAL-001"]


def test_r02_h08_sin_el_motor_no_hay_fue(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    _sembrar(b, FUENTE_A, 5, 0)
    b.evaluador.motor = None
    assert b.evaluador.fiabilidad_fuentes(AS_OF) == []
    assert not [e for e in b.almacen.leer("F6") if e.get("tipo_entrada") == "FUE"]

