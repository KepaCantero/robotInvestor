"""Pruebas de los niveles de autonomía L0/L1/L2 y la degradación automática (D-12, D-16, T-18)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "validador"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from ejecucion_g import BrokerSimulado, cerrar, ejecutar  # noqa: E402
from vigilancia import vigilar  # noqa: E402
from pruebas_ejecucion_g import autorizado  # noqa: E402
from pruebas_orquestador import AHORA, Arnes, nuevo  # noqa: E402
from pruebas_control_f import informe_f  # noqa: E402
from pruebas_orquestador import hasta  # noqa: E402

T1 = "2026-11-06T09:05:00+00:00"
T2 = "2026-11-06T09:10:00+00:00"
PID = "POS-EXP-0001"
L1 = {"nivel_autonomia": {"TACTICA": "L1"}}
L2 = {"nivel_autonomia": {"TACTICA": "L2"}}


def datos(p, hora=T1):
    return {"EURUSD": {"precio": p, "hora": hora}}


def abierta(cfg):
    o, b = autorizado(o=nuevo(cfg))
    assert ejecutar(o, "EXP-0001", b, AHORA)["ok"]
    return o, b


def main():
    h = Arnes()
    # --- configuración
    for nombre, cfg in (("nivel_L9", {"nivel_autonomia": {"TACTICA": "L9"}}), ("cartera_inventada", {"nivel_autonomia": {"X": "L1"}}),
                        ("no_dict", {"nivel_autonomia": "L1"}), ("nivel_numero", {"nivel_autonomia": {"TACTICA": 2}})):
        try:
            from orquestador import Orquestador
            from pruebas_orquestador import CAL, CFG
            Orquestador({**CFG, **cfg}, CAL); h.chk(f"config_{nombre}_se_rechaza", False)
        except ValueError:
            h.chk(f"config_{nombre}_se_rechaza", True)
    o = nuevo({"nivel_autonomia": {}})
    h.chk("sin_dato_el_nivel_es_L1", o.nivel("TACTICA") == "L1" and o.nivel("TRADING") == "L1")
    # --- autorizar por la matriz exige L2
    o = nuevo({"matriz_autonomia": {"TACTICA": True}, **L1}); hasta(o, "PROPUESTA")
    r = o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", informe_f(o), AHORA)
    h.chk("matriz_en_L1_no_autoriza", r["codigo"] == "O-05" and o.expedientes["EXP-0001"]["estado"] == "PROPUESTA", r)
    h.chk("operador_si_autoriza_en_L1", o.autorizar("EXP-0001", "OPERADOR", informe_f(o, n=2), AHORA)["ok"])
    o = nuevo({"matriz_autonomia": {"TACTICA": True}, **{"nivel_autonomia": {"TACTICA": "L0"}}}); hasta(o, "PROPUESTA")
    h.chk("matriz_en_L0_no_autoriza", o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", informe_f(o), AHORA)["codigo"] == "O-05")
    o = nuevo({"matriz_autonomia": {"TACTICA": True}, **L2}); hasta(o, "PROPUESTA")
    h.chk("matriz_en_L2_autoriza", o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", informe_f(o), AHORA)["ok"])
    # --- H en L1: prepara, no cierra
    o, b = abierta(L1)
    h.chk("la_posicion_guarda_su_nivel", o.posiciones[PID]["nivel"] == "L1")
    r = vigilar(o, b, datos(1.30), T1)
    h.chk("L1_objetivo_cumplido_H10_no_cierra", [a["regla"] for a in r["acciones"]] == ["H-10"] and o.posiciones[PID]["estado"] == "ABIERTA"
          and len(b.posiciones()) == 1 and len(o.posiciones[PID]["propuestas"]) == 1, r)
    vigilar(o, b, datos(1.30, T2), T2)
    h.chk("L1_no_repite_la_propuesta", len(o.posiciones[PID]["propuestas"]) == 1)
    r = cerrar(o, PID, b, T2, actor="OPERADOR", motivo="confirmo el cierre por objetivo")
    h.chk("L1_el_operador_confirma_y_se_cierra", r["ok"] and o.posiciones[PID]["estado"] == "CERRADA" and b.posiciones() == [], r)
    # --- L1: G no cierra solo por una condición
    o, b = abierta(L1)
    r = cerrar(o, PID, b, T1, condicion={"id": "OBJ-1", "valor_observado": 1.30})
    h.chk("L1_G_no_cierra_por_condicion_O05", r["codigo"] == "G-06" and "L1" in r["motivo"] and o.posiciones[PID]["estado"] == "ABIERTA", r)
    # --- L1: el stop ya ejecutado por el intermediario se confirma igualmente (es un hecho)
    o, b = abierta(L1)
    b.mover_precio("EURUSD", 1.04, T1)
    r = vigilar(o, b, datos(1.04), T1)
    h.chk("L1_stop_ejecutado_se_concilia", [a["regla"] for a in r["acciones"]] == ["H-01"] and o.posiciones[PID]["estado"] == "CERRADA" and b.posiciones() == [], r)
    # --- L1: stop cumplido sin ejecutar: H prepara
    o, b = abierta(L1)
    b.precios["EURUSD"] = 1.04
    r = vigilar(o, b, datos(1.04), T1)
    h.chk("L1_stop_cumplido_sin_ejecutar_H10", [a["regla"] for a in r["acciones"]] == ["H-10"] and o.posiciones[PID]["estado"] == "ABIERTA", r)
    # --- L2: cierra solo
    o, b = abierta(L2)
    r = vigilar(o, b, datos(1.30), T1)
    h.chk("L2_objetivo_cumplido_cierra", [a["regla"] for a in r["acciones"]] == ["H-02"] and o.posiciones[PID]["estado"] == "CERRADA", r)
    # --- degradación automática
    o, b = abierta(L2)
    h.chk("L2_nivel_inicial", o.nivel("TACTICA") == "L2")
    r = vigilar(o, b, datos(1.10, "2026-11-06T08:00:00+00:00"), T1)
    h.chk("dato_viejo_degrada_a_L1", o.nivel("TACTICA") == "L1" and "TACTICA" in o.degradadas, o.degradadas)
    r = vigilar(o, b, datos(1.30, T2), T2)
    h.chk("degradada_H_ya_no_cierra", [a["regla"] for a in r["acciones"]] == ["H-10"] and o.posiciones[PID]["estado"] == "ABIERTA", r)
    h.chk("la_degradacion_deja_aviso_O19", any(x["codigo"] == "O-19" for x in o.avisos))
    r = o.restablecer_nivel("TACTICA", "OPERADOR", T2)
    h.chk("restablecer_con_avisos_sin_acusar_O06", r["codigo"] == "O-06" and o.nivel("TACTICA") == "L1", r)
    for av in list(o.avisos):
        o.acusar_aviso(av["id"], "OPERADOR", T2)
    h.chk("restablecer_solo_operador", o.restablecer_nivel("TACTICA", "G", T2)["codigo"] == "O-05" and o.nivel("TACTICA") == "L1")
    h.chk("restablecer_acusado_vuelve_a_L2", o.restablecer_nivel("TACTICA", "OPERADOR", T2)["ok"] and o.nivel("TACTICA") == "L2")
    h.chk("restablecer_dos_veces_O12", o.restablecer_nivel("TACTICA", "OPERADOR", T2)["codigo"] == "O-12")
    # --- una discrepancia degrada
    o, b = abierta(L2)
    o.reportar_discrepancia([{"tipo": "POSICION_NO_REGISTRADA", "ref": "X", "detalle": "d"}], "G", T1)
    h.chk("discrepancia_degrada_las_carteras_con_autonomia", "TACTICA" in o.degradadas and o.nivel("TACTICA") == "L1" and "TRADING" not in o.degradadas)
    # --- G-08 (estado incierto) degrada
    o, b = autorizado(o=nuevo(L2))
    from ejecucion_g import _incierto
    _incierto(o, "EXP-0001", AHORA, "prueba")
    h.chk("estado_incierto_G08_degrada", o.nivel("TACTICA") == "L1", o.degradadas)
    # --- degradar manual
    o = nuevo(L2)
    h.chk("degradar_actor_no_valido_O05", o.degradar("TACTICA", "x", "BROKER", AHORA)["codigo"] == "O-05")
    h.chk("degradar_cartera_invalida_O15", o.degradar("NADA", "x", "H", AHORA)["codigo"] == "O-15")
    h.chk("degradar_sin_motivo_O15", o.degradar("TACTICA", " ", "H", AHORA)["codigo"] == "O-15")
    h.chk("degradar_ok", o.degradar("TACTICA", "intermediario caído", "G", AHORA)["ok"] and o.nivel("TACTICA") == "L1")
    o2 = nuevo({"nivel_autonomia": {"TACTICA": "L0"}}); o2.degradar("TACTICA", "x", "G", AHORA)
    h.chk("degradar_L0_se_queda_en_L0_sin_aviso_falso", o2.nivel("TACTICA") == "L0" and not o2.degradadas and not o2.avisos)
    # --- el flag de "stop ejecutado" no se puede falsificar
    for cfg, nom in ((L1, "L1"), ({"nivel_autonomia": {"TACTICA": "L0"}}, "L0")):
        o, b = abierta(cfg)
        falso = {"id": "OBJ-1", "valor_observado": 1.30, "stop_ejecutado_orden_id": "ORD-EXP-0001-S-1"}
        h.chk(f"{nom}_condicion_no_stop_con_prueba_falsa_O05", o.posicion_transicion(PID, "CERRANDO", "G", T1, condicion=falso)["codigo"] == "O-05")
        falso2 = {"id": "STOP-1", "valor_observado": 1.0, "stop_ejecutado_orden_id": "ORD-INVENTADA"}
        h.chk(f"{nom}_orden_que_no_es_proteccion_O05", o.posicion_transicion(PID, "CERRANDO", "F", T1, condicion=falso2)["codigo"] == "O-05")
        falso3 = {"id": "STOP-1", "valor_observado": 1.0, "stop_ejecutado_orden_id": "ORD-EXP-0001-S-1"}
        h.chk(f"{nom}_reducir_no_se_beneficia_O05", o.posicion_transicion(PID, "REDUCIENDO", "G", T1, condicion=falso3)["codigo"] == "O-05")
        h.chk(f"{nom}_estado_intacto", o.posiciones[PID]["estado"] == "ABIERTA")
    o, b = abierta({"nivel_autonomia": {"TACTICA": "L0"}})
    h.chk("L0_H_prepara_y_no_cierra", [a["regla"] for a in vigilar(o, b, datos(1.30), T1)["acciones"]] == ["H-10"] and len(b.posiciones()) == 1)
    # --- propuestas de H: una sola aunque cambie el precio
    o, b = abierta(L1)
    for i, p in enumerate((1.30, 1.31, 1.32, 1.33)):
        t = f"2026-11-06T09:{5 + i:02d}:00+00:00"
        vigilar(o, b, datos(p, t), t)
    h.chk("H10_una_propuesta_aunque_cambie_el_precio", len(o.posiciones[PID]["propuestas"]) == 1, o.posiciones[PID]["propuestas"])
    # --- una autorización automática no se ejecuta si la cartera se degrada antes
    o = nuevo({"matriz_autonomia": {"TACTICA": True}, **L2}); hasta(o, "PROPUESTA")
    from pruebas_ejecucion_g import broker as _br
    b = _br()
    from ejecucion_g import cartera_para_f
    o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", informe_f(o, "EXP-0001", n=1, cartera=cartera_para_f(b)), AHORA)
    o.degradar("TACTICA", "discrepancia", "G", AHORA)
    r = ejecutar(o, "EXP-0001", b, AHORA)
    h.chk("autorizada_por_matriz_y_degradada_no_ejecuta", not r["ok"] and b.posiciones() == [] and "EXP-0001" not in {p["expediente_id"] for p in o.posiciones.values()}, r)
    o, b = autorizado(o=nuevo({"matriz_autonomia": {"TACTICA": True}, **L1}))
    h.chk("autorizada_por_el_operador_si_ejecuta_en_L1", ejecutar(o, "EXP-0001", b, AHORA)["ok"])
    # --- H concilia antes de cerrar solo: stop cancelado en el intermediario + objetivo cumplido en L2
    o, b = abierta(L2)
    b.cancelar("ORD-EXP-0001-S-1")
    r = vigilar(o, b, datos(1.30), T1)
    h.chk("L2_con_discrepancia_previa_no_cierra_solo", o.nivel("TACTICA") == "L1" and o.posiciones[PID]["estado"] == "ABIERTA"
          and [a["regla"] for a in r["acciones"] if a["posicion"]] == ["H-10"], r)
    # --- restablecer: un aviso nuevo posterior al acuse vuelve a bloquear
    o, b = abierta(L2)
    o.degradar("TACTICA", "a", "G", T1)
    for av in list(o.avisos):
        o.acusar_aviso(av["id"], "OPERADOR", T1)
    o._aviso("O-18", "otra diferencia", T1, "Z")
    h.chk("aviso_nuevo_tras_el_acuse_bloquea_restablecer", o.restablecer_nivel("TACTICA", "OPERADOR", T1)["codigo"] == "O-06")
    h.chk("integridad_tras_degradar", o.integridad() == [])
    print(f"\n{h.n} comprobaciones")
    print("RESULTADO NIVELES:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
