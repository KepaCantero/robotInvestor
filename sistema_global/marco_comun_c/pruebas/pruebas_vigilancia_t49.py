"""Pruebas de T-49: H vigila los escenarios de fallo del Contradictor, las invalidez por otras métricas y la pérdida no realizada.
Ninguna de esas señales vende: piden revisión (EN_REVISION) y dejan una propuesta. Incluye las regresiones de la revisión
independiente de T-49 (R-01 a R-07). Datos e intermediario SIMULADOS."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))

import contratos as ct  # noqa: E402
from ejecucion_g import cartera_para_f, ejecutar  # noqa: E402
from orquestador import Orquestador, nivel_perdida, perdida_pct  # noqa: E402
from vigilancia import vigilar  # noqa: E402
from pruebas_contradictor import ESC, informe as informe_ctr  # noqa: E402
from pruebas_control_f import informe_f  # noqa: E402
from pruebas_ejecucion_g import autorizado, broker  # noqa: E402
from pruebas_orquestador import (AHORA, CAL, CFG, ENTRADA, INV, OBJ, SALIDA, STOP, Arnes, autorizar_op, dim, elegir_si_hace_falta,  # noqa: E402
                                 encargo, nuevo, sobre, sobre_para)

T1 = "2026-11-06T09:05:00+00:00"
T2 = "2026-11-06T09:10:00+00:00"
T3 = "2026-11-06T09:15:00+00:00"
PID = "POS-EXP-0001"
EF_PRECIO = {**ESC, "id": "EF-PRECIO", "descripcion": "El par pierde el soporte de 1,07 y la tesis de rebote no se sostiene",
             "disparador": {"metrica": "precio", "operador": "<", "umbral": 1.07, "unidad": "USD"}}
EF_TIPOS = {**ESC, "id": "EF-TIPOS", "descripcion": "El diferencial de tipos se cierra y desaparece el carry", "consecuencia": "PERDIDA",
            "perdida_pct": -8.0, "disparador": {"metrica": "diferencial_tipos", "operador": "<=", "umbral": 0.5, "unidad": "pp"}}
ANCHA = {**SALIDA, "condiciones": [{**STOP, "umbral": 0.90}, OBJ, INV]}   # stop lejos: la alerta de pérdida llega antes
K_EF, K_TIPOS, K_INV = "CONTRADICTOR:EF-PRECIO", "CONTRADICTOR:EF-TIPOS", "INVALIDEZ:INV-1"


def datos(precio, hora=T1, **metricas):
    """Precio fresco y, aparte, métricas {valor, unidad}: un número suelto se toma como {valor, USD}."""
    d = {"precio": precio, "hora": hora}
    if metricas:
        d["metricas"] = {k: (v if isinstance(v, dict) else {"valor": v, "unidad": "USD"}) for k, v in metricas.items()}
    return {"EURUSD": d}


def preparar(escenarios=None, salida=None):
    """Hasta la propuesta del EXP-0001; su sobre llegó con el informe del Contradictor (y sus escenarios de fallo)."""
    o = nuevo()
    for n in (1, 2):
        eid = f"EXP-{n:04d}"
        assert o.detectar(eid, f"COR-{n:04d}", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
        assert o.emitir_encargo(eid, encargo(n), "GESTOR_TACTICA", AHORA)["ok"]
        s = sobre_para(n, salida)   # T-17: el rival con el mismo stop y límite (D mide el riesgo hasta el stop)
        inf = informe_ctr(s, n=n, escenarios=escenarios) if n == 1 and escenarios else None
        r = o.entregar_sobre(eid, s, AHORA, inf)
        if not r["ok"]:
            return o, r
    assert o.comparar(["EXP-0001", "EXP-0002"], "D", AHORA)["ok"]
    elegir_si_hace_falta(o, "EXP-0001", AHORA)
    return o, None


def abierta_con(escenarios=None, salida=None):
    o, err = preparar(escenarios, salida)
    assert err is None, err
    b = broker()
    sal = salida or SALIDA
    assert o.proponer("EXP-0001", ENTRADA, sal, "GESTOR_TACTICA", AHORA, dim(o, "EXP-0001", None, sal))["ok"]
    assert autorizar_op(o, "EXP-0001", informe_f(o, "EXP-0001", n=1, cartera=cartera_para_f(b)), AHORA)["ok"]
    assert ejecutar(o, "EXP-0001", b, AHORA)["ok"]
    return o, b


def abierta():
    o, b = autorizado()
    assert ejecutar(o, "EXP-0001", b, AHORA)["ok"]
    return o, b


def reglas(r):
    return [a["regla"] for a in r["acciones"]]


def main():
    h = Arnes()

    # ---------------------------------------------------------------- lo que se lleva la posición
    o, b = abierta_con([EF_PRECIO, EF_TIPOS])
    p = o.posiciones[PID]
    h.chk("posicion_lleva_precio_de_entrada", p["precio_entrada"] == 1.10, p.get("precio_entrada"))
    h.chk("posicion_lleva_escenarios_e_invalidez", [x["clave"] for x in p["senales"]] == [K_EF, K_TIPOS, K_INV], p["senales"])
    h.chk("escenarios_en_la_huella_del_sobre", o.expedientes["EXP-0001"]["contradictor"]["escenarios_fallo"][0]["id"] == "EF-PRECIO" and o.integridad() == [])
    h.chk("sin_contradictor_solo_la_invalidez", [x["clave"] for x in abierta_con()[0].posiciones[PID]["senales"]] == [K_INV])

    # ---------------------------------------------------------------- H-16: escenario de fallo por precio (L2: aun así no vende)
    n_ord = len(b.ordenes)
    r = vigilar(o, b, datos(1.06), T1)
    p = o.posiciones[PID]
    h.chk("H16_escenario_de_fallo_pide_revision", "H-16" in reglas(r) and p["estado"] == "EN_REVISION" and p["senales_disparadas"] == [K_EF]
          and p["propuestas"][-1]["texto"].startswith("ESCENARIO DE FALLO: EF-PRECIO"), (r, p["estado"]))
    h.chk("H16_no_envia_nada_al_intermediario", len(b.ordenes) == n_ord and p["cantidad"] == 100.0 and b.posiciones()[0]["cantidad"] == 100.0)
    r2 = vigilar(o, b, datos(1.06), T2)
    h.chk("H16_una_sola_vez", "H-16" not in reglas(r2) and o.posiciones[PID]["senales_disparadas"] == [K_EF], r2)
    al = ct.alertas_posicion(o, PID)
    h.chk("CT_G_10_escenario_de_fallo", al[-1]["payload"]["tipo"] == "ESCENARIO_FALLO" and al[-1]["version_esquema"] == "0.2.0"
          and all(ct.validar(x) == [] for x in al), [ct.validar(x) for x in al])
    h.chk("integridad_tras_la_senal", o.integridad() == [], o.integridad())
    # escenario por otra métrica, con la posición ya en revisión: propone sin otro cambio de estado
    r = vigilar(o, b, datos(1.08, hora=T3, diferencial_tipos={"valor": 0.4, "unidad": "pp"}), T3)
    p = o.posiciones[PID]
    h.chk("H16_metrica_propia_con_la_posicion_en_revision", "H-16" in reglas(r) and p["estado"] == "EN_REVISION"
          and p["senales_disparadas"] == [K_EF, K_TIPOS] and "diferencial_tipos" in p["propuestas"][-1]["texto"], r)

    # ---------------------------------------------------------------- invalidez por otra métrica (la del sobre: precio_cierre)
    o, b = abierta()
    r = vigilar(o, b, datos(1.06, precio_cierre=1.04), T1)
    p = o.posiciones[PID]
    h.chk("H16_invalidez_cualitativa_propone_no_vende", "H-16" in reglas(r) and p["estado"] == "EN_REVISION" and p["cantidad"] == 100.0
          and p["propuestas"][-1]["texto"].startswith("INVALIDEZ: INV-1"), r)
    h.chk("CT_G_10_invalidez", ct.alertas_posicion(o, PID)[-1]["payload"]["tipo"] == "INVALIDEZ")
    o, b = abierta()
    r = vigilar(o, b, datos(1.06, precio_cierre=1.06), T1)
    h.chk("invalidez_no_cumplida_no_hace_nada", r["acciones"] == [] and o.posiciones[PID]["estado"] == "ABIERTA", r)
    r = vigilar(o, b, datos(1.06, precio_cierre="x"), T2)
    h.chk("H18_dato_no_numerico_no_se_evalua", any(x["regla"] == "H-18" for x in r["no_evaluadas"]) and o.posiciones[PID]["estado"] == "ABIERTA", r)

    # ---------------------------------------------------------------- H-17: pérdida no realizada
    o, b = autorizado(salida=ANCHA)
    assert ejecutar(o, "EXP-0001", b, AHORA)["ok"]
    n_ord = len(b.ordenes)
    h.chk("perdida_pct_largo", abs(perdida_pct(o.posiciones[PID], 1.045) - (-5.0)) < 1e-9)
    r = vigilar(o, b, datos(1.06), T1)
    h.chk("perdida_bajo_el_umbral_no_alerta", "H-17" not in reglas(r) and o.posiciones[PID]["estado"] == "ABIERTA", r)
    r = vigilar(o, b, datos(1.04), T1)
    p = o.posiciones[PID]
    h.chk("H17_alerta_de_perdida", "H-17" in reglas(r) and p["estado"] == "EN_REVISION" and p["perdida_alertada"] == 1
          and p["propuestas"][-1]["texto"].startswith("ALERTA DE PÉRDIDA"), r)
    h.chk("H17_no_envia_nada", len(b.ordenes) == n_ord and p["cantidad"] == 100.0)
    r = vigilar(o, b, datos(1.03, hora=T2), T2)
    h.chk("H17_mismo_nivel_no_repite", "H-17" not in reglas(r), r)
    r = vigilar(o, b, datos(0.98, hora=T3), T3)
    h.chk("H17_siguiente_multiplo_vuelve_a_alertar", "H-17" in reglas(r) and o.posiciones[PID]["perdida_alertada"] == 2, r)
    h.chk("CT_G_10_perdida", ct.alertas_posicion(o, PID)[-1]["payload"]["tipo"] == "PERDIDA" and o.integridad() == [])
    q = dict(o.posiciones[PID], direccion="CORTO")
    h.chk("perdida_pct_corto_sube_el_precio", perdida_pct(q, 1.155) < -4.99)

    # ---------------------------------------------------------------- las salidas declaradas mandan y no se añade ruido
    o, b = abierta()
    b.precios["EURUSD"] = 1.04   # el stop se cumple (y la pérdida pasa del 5 %)
    r = vigilar(o, b, datos(1.04, precio_cierre=1.0), T1)
    h.chk("stop_cumplido_cierra_sin_senales", reglas(r) == ["H-05"] and o.posiciones[PID]["estado"] == "CERRADA", r)
    o, b = abierta()
    r = vigilar(o, b, datos(1.30, precio_cierre=1.0), T1)
    h.chk("objetivo_cumplido_cierra_sin_senales", reglas(r) == ["H-02"], r)

    # ---------------------------------------------------------------- integridad: las señales están en la cadena
    for campo, valor in (("senales", []), ("senales_disparadas", [K_INV]), ("precio_entrada", 2.0), ("perdida_alertada", 5)):
        o, b = abierta()
        o.posiciones[PID][campo] = valor
        r = vigilar(o, b, datos(1.04, precio_cierre=1.0), T1)
        h.chk(f"alterar_{campo}_se_detecta_H13", o.integridad() != [] and "H-13" in reglas(r) and "H-16" not in reglas(r) and "H-17" not in reglas(r), r)

    # ---------------------------------------------------------------- registrar_senal: guardas
    o, b = abierta()
    h.chk("registrar_solo_H", o.registrar_senal(PID, "SENAL", K_INV, 1.0, "GESTOR_TACTICA", T1)["codigo"] == "O-05")
    h.chk("registrar_senal_desconocida", o.registrar_senal(PID, "SENAL", "INVALIDEZ:EF-9", 1.0, "H", T1)["codigo"] == "O-01")
    h.chk("registrar_por_id_sin_origen_no_vale", o.registrar_senal(PID, "SENAL", "INV-1", 1.0, "H", T1)["codigo"] == "O-01")
    h.chk("registrar_valor_que_no_cumple", o.registrar_senal(PID, "SENAL", K_INV, 1.06, "H", T1)["codigo"] == "O-01")
    h.chk("registrar_valor_no_numerico", o.registrar_senal(PID, "SENAL", K_INV, "bajo", "H", T1)["codigo"] == "O-01")
    h.chk("registrar_tipo_desconocido", o.registrar_senal(PID, "NOTICIA", None, 1.0, "H", T1)["codigo"] == "O-01")
    h.chk("registrar_perdida_que_no_llega", o.registrar_senal(PID, "PERDIDA", None, 1.08, "H", T1)["codigo"] == "O-02")
    h.chk("registrar_bien", o.registrar_senal(PID, "SENAL", K_INV, 1.0, "H", T1)["ok"])
    h.chk("registrar_dos_veces_O02", o.registrar_senal(PID, "SENAL", K_INV, 1.0, "H", T2)["codigo"] == "O-02")
    antes = copy.deepcopy(o.posiciones)
    h.chk("rechazos_sin_cambios", o.registrar_senal(PID, "SENAL", "INVALIDEZ:EF-9", 1.0, "H", T2)["codigo"] == "O-01" and o.posiciones == antes)
    o, b = abierta()
    b.mover_precio("EURUSD", 1.04, T1)
    vigilar(o, b, datos(1.04), T1)
    h.chk("registrar_en_cerrada_O04", o.registrar_senal(PID, "SENAL", K_INV, 1.0, "H", T2)["codigo"] == "O-04")

    # ---------------------------------------------------------------- configuración y contrato
    for nombre, v in (("cero", 0), ("positivo", 3.0), ("bajo_menos_100", -150), ("texto", "-5"), ("menos_60", -60),
                      ("minusculo", -5e-324), ("milesima", -0.001), ("infinito", float("-inf"))):
        try:
            Orquestador({**CFG, "alerta_perdida_pct": v}, CAL)
            h.chk(f"config_alerta_{nombre}_se_rechaza", False)
        except ValueError:
            h.chk(f"config_alerta_{nombre}_se_rechaza", True)
    h.chk("config_alerta_en_los_limites_se_acepta", all(Orquestador({**CFG, "alerta_perdida_pct": v}, CAL) for v in (-50, -0.5)))
    h.chk("alerta_en_la_huella", nuevo().configuracion()["huella"] != nuevo({"alerta_perdida_pct": -3.0}).configuracion()["huella"])
    reg = {c["tipo"]: c for c in ct.registro()["contratos"]}["CT-G-10"]
    h.chk("registro_10_en_020_con_010_retirada", reg["version"] == "0.2.0" and [v["estado"] for v in reg["versiones"]] == ["VIGENTE", "RETIRADA"])

    # ================================================================ regresiones de la revisión independiente
    # R-01: un entero enorme en las métricas no rompe la pasada; un fallo inesperado en una posición no deja sin vigilar a las demás
    o, b = abierta()
    try:
        r = vigilar(o, b, datos(1.06, precio_cierre=10 ** 400), T1)
        h.chk("R01_entero_enorme_es_H18", any(x["regla"] == "H-18" for x in r["no_evaluadas"]) and o.posiciones[PID]["estado"] == "ABIERTA", r)
    except Exception as ex:   # noqa: BLE001
        h.chk("R01_entero_enorme_es_H18", False, type(ex).__name__)
    o, b = abierta()
    q = copy.deepcopy(o.posiciones[PID])
    q.update({"posicion_id": "POS-EXP-0009", "instrumento": "GBPUSD", "activo_base": "GBP", "protecciones": [], "historial": [],
              "senales": [], "senales_disparadas": [], "propuestas": []})
    o.posiciones["POS-EXP-0009"] = q
    o._anota_pos(q, None, "ABIERTA", "G", T1, "posición de prueba")
    o.registrar_senal = lambda *a, **k: 1 / 0   # fallo inesperado al vigilar POS-EXP-0001
    try:
        r = vigilar(o, b, {**datos(1.06, precio_cierre=1.04), "GBPUSD": {"precio": 1.00, "hora": T1}}, T1)
        h.chk("R01_fallo_en_una_posicion_es_H19_y_sigue", [(x["posicion"], x["regla"]) for x in r["acciones"] if x["posicion"]]
              == [(PID, "H-19"), ("POS-EXP-0009", "H-10")] and r["acciones"][0]["aviso_registrado"], r)
    except Exception as ex:   # noqa: BLE001
        h.chk("R01_fallo_en_una_posicion_es_H19_y_sigue", False, type(ex).__name__)

    # R-02: un escenario del Contradictor con el mismo id que una invalidez no la tapa: cada una se dispara por su lado
    EF_INV1 = {**EF_TIPOS, "id": "INV-1"}
    o, b = abierta_con([EF_INV1])
    r = vigilar(o, b, datos(1.06, precio_cierre=1.04), T1)
    h.chk("R02_invalidez_con_id_repetido_se_dispara", o.posiciones[PID]["senales_disparadas"] == [K_INV] and r["acciones"][-1]["ok"], r)
    r = vigilar(o, b, datos(1.06, hora=T2, diferencial_tipos={"valor": 0.4, "unidad": "pp"}), T2)
    h.chk("R02_y_el_escenario_tambien", o.posiciones[PID]["senales_disparadas"] == [K_INV, "CONTRADICTOR:INV-1"] and r["acciones"][-1]["ok"], r)
    o, b = abierta_con([EF_INV1])   # al revés: primero el escenario, y la invalidez sigue viva
    vigilar(o, b, datos(1.06, diferencial_tipos={"valor": 0.4, "unidad": "pp"}), T1)
    r = vigilar(o, b, datos(1.06, hora=T2, precio_cierre=1.04), T2)
    h.chk("R02_escenario_primero_no_silencia_la_invalidez", o.posiciones[PID]["senales_disparadas"] == ["CONTRADICTOR:INV-1", K_INV]
          and o.posiciones[PID]["propuestas"][-1]["texto"].startswith("INVALIDEZ: INV-1"), r)

    # R-03: métricas con grafía canónica y precios en la divisa de cotización; la unidad del dato se contrasta
    for nombre, disp in (("PRECIO_mayusculas", {"metrica": "PRECIO", "operador": "<", "umbral": 1.07, "unidad": "USD"}),
                         ("precio_en_pct", {"metrica": "precio", "operador": "<", "umbral": -3, "unidad": "PCT"}),
                         ("precio_en_otra_divisa", {"metrica": "precio", "operador": ">", "umbral": 0.95, "unidad": "EUR"}),
                         ("precio_cierre_en_otra_divisa", {"metrica": "precio_cierre", "operador": "<", "umbral": 1.0, "unidad": "EUR"})):
        _, err = preparar([{**EF_PRECIO, "disparador": disp}])
        h.chk(f"R03_informe_{nombre}_se_rechaza", err is not None and err["codigo"] == "O-01" and "no se puede vigilar" in err["motivo"], err)
    o, err = preparar()
    sal = {**SALIDA, "condiciones": [STOP, OBJ, {**INV, "unidad": "EUR"}]}
    r = o.proponer("EXP-0001", ENTRADA, sal, "GESTOR_TACTICA", AHORA, dim(o, "EXP-0001", None, sal))
    h.chk("R03_invalidez_de_precio_en_otra_divisa_O21", r["codigo"] == "O-21" and "no se puede vigilar" in r["motivo"], r)
    o, b = abierta()
    r = vigilar(o, b, datos(1.06, precio_cierre={"valor": 1.04, "unidad": "EUR"}), T1)
    h.chk("R03_dato_en_otra_unidad_es_H18", "H-16" not in reglas(r) and any(x["regla"] == "H-18" for x in r["no_evaluadas"]), r)
    d = datos(1.06)
    d["EURUSD"]["metricas"] = {"precio_cierre": 1.04}
    r = vigilar(o, b, d, T2)
    h.chk("R03_dato_sin_unidad_es_H18", "H-16" not in reglas(r) and any(x["regla"] == "H-18" for x in r["no_evaluadas"]), r)

    # R-04: las propuestas y alertas a la posición están en la cadena
    for nombre, cambio in (("rebajar", lambda p: p["propuestas"][-1].update(texto="REVISIÓN: todo en orden")),
                           ("borrar", lambda p: p["propuestas"].clear())):
        o, b = abierta()
        vigilar(o, b, datos(1.06, precio_cierre=1.04), T1)
        cambio(o.posiciones[PID])
        h.chk(f"R04_{nombre}_una_alerta_se_detecta", o.integridad() != [] and not o.posicion_integra(PID))
    o, b = abierta()
    o.posiciones[PID]["cantidad"] = 1.0   # una propuesta no puede blanquear un estado alterado
    h.chk("R04_proponer_sobre_estado_alterado_O13", o.proponer_sobre_posicion(PID, "nota", "OPERADOR", T1)["codigo"] == "O-13" and o.integridad() != [])
    o, b = abierta()
    h.chk("R04_proponer_anota_sin_cambiar_estado", o.proponer_sobre_posicion(PID, "nota", "OPERADOR", T1)["ok"]
          and o.posiciones[PID]["estado"] == "ABIERTA" and o.integridad() == [])

    # R-05: una descripción que no es texto se rechaza al proponer
    o, err = preparar()
    sal = {**SALIDA, "condiciones": [STOP, OBJ, INV, {**INV, "id": "INV-2", "descripcion": 7}]}
    r = o.proponer("EXP-0001", ENTRADA, sal, "GESTOR_TACTICA", AHORA, dim(o, "EXP-0001", None, sal))
    h.chk("R05_descripcion_no_texto_O01", r["codigo"] == "O-01" and "texto" in r["motivo"], r)

    # R-07: la pérdida la calcula el Orquestador con el precio; la puerta de H es el propio nivel (corto al 5 % exacto)
    o, b = abierta()
    for nombre, v in (("cero", 0), ("negativo", -1e6), ("infinito", float("inf"))):
        h.chk(f"R07_registrar_perdida_con_precio_{nombre}_O01", o.registrar_senal(PID, "PERDIDA", None, v, "H", T1)["codigo"] == "O-01")
    h.chk("R07_perdida_alertada_intacta", o.posiciones[PID]["perdida_alertada"] == 0 and o.integridad() == [])
    h.chk("R07_corto_al_5_exacto_es_nivel_1", nivel_perdida({"precio_entrada": 1.10, "direccion": "CORTO"}, 1.155, -5.0)[1] == 1)
    h.chk("R07_precio_extremo_no_rompe", nivel_perdida({"precio_entrada": 1e-300, "direccion": "CORTO"}, 1e300, -0.5) is None)

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO VIGILANCIA T-49:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
