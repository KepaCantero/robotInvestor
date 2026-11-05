"""Pruebas de los candidatos apartados antes de comparar (T-36). Datos SIMULADOS.

Comprueba: un gestor solo aparta candidatos de su cartera; un candidato vivo apartado (observar o descartar) por quien no es
el operador sigue de «testigo» en las comparaciones de su cartera mientras su sobre esté vigente; si un testigo habría
ganado, D no da ganador (O-30, aviso ALTA) y elige el operador; lo que aparta el operador no deja testigo; un testigo alterado
detiene la comparación (O-13 y kill-switch).

Uso: python3 pruebas/pruebas_apartados.py
"""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
from pruebas_orquestador import AHORA, COND_OBS, ENTRADA, SALIDA, Arnes, dim, nuevo  # noqa: E402
from pruebas_propuesta import validar_con  # noqa: E402

BUENO = (3.0, -4.0, 6.0)      # mejor que el sobre por defecto
MALO = (-1.0, -4.0, 1.0)      # retorno esperado negativo: no supera la referencia


def dos(bueno_es=1, otro=None):
    """EXP-0001 (EUR/USD) y EXP-0002 (GBP/USD) VALIDADA; el bueno lleva escenarios mejores."""
    o = nuevo()
    validar_con(o, 1, escenarios=BUENO if bueno_es == 1 else otro)
    validar_con(o, 2, instrumento="GBP/USD", escenarios=BUENO if bueno_es == 2 else otro)
    return o


def main():
    h = Arnes()
    # ------------------------------------------------------------ control: sin apartar, gana el bueno
    o = dos()
    r = o.comparar(["EXP-0001", "EXP-0002"], "D", AHORA)
    h.chk("control_gana_el_bueno", r["ok"] and r["ganador"] == "EXP-0001", r)

    # ------------------------------------------------------------ apartar al rival para que gane otro
    for nombre, apartar in (("observar_gestor", lambda o: o.observar("EXP-0001", COND_OBS, "esperar", "GESTOR_TACTICA", AHORA)),
                            ("descartar_broker", lambda o: o.descartar("EXP-0001", "no me convence", "BROKER", AHORA)),
                            ("observar_D", lambda o: o.observar("EXP-0001", COND_OBS, "aparcar", "D", AHORA))):
        o = dos()
        h.chk(f"{nombre}_aparta", apartar(o)["ok"])
        r = o.comparar(["EXP-0002"], "D", AHORA)
        c = o.expedientes["EXP-0002"]["comparacion"]
        h.chk(f"{nombre}_el_apartado_habria_ganado_O30", r["codigo"] == "O-30" and r["ganador"] is None and r["apartado_mejor"] == "EXP-0001"
              and not c["ganador"] and c["aspirante"] and c["apartado_mejor"] == "EXP-0001" and c["testigos"] == ["EXP-0001"], (r, c))
        av = [x for x in o.avisos if x["codigo"] == "O-30"]
        h.chk(f"{nombre}_aviso_alto_al_operador", len(av) == 1 and av[0]["prioridad"] == "ALTA" and av[0]["ref"] == "EXP-0001", av)
        rp = o.proponer("EXP-0002", {**ENTRADA, "instrumento": "GBPUSD", "activo_base": "GBP"}, SALIDA, "GESTOR_TACTICA", AHORA)
        h.chk(f"{nombre}_sin_ganador_no_se_propone_O22", rp["codigo"] == "O-22", rp)
    o = dos()
    o.observar("EXP-0001", COND_OBS, "esperar", "GESTOR_TACTICA", AHORA)
    o.comparar(["EXP-0002"], "D", AHORA)
    h.chk("solo_el_operador_elige_O05", o.elegir("EXP-0002", "GESTOR_TACTICA", "x", AHORA)["codigo"] == "O-05")
    r = o.elegir("EXP-0002", "OPERADOR", "sé que EXP-0001 era mejor; lo apartamos por liquidez", AHORA)
    h.chk("el_operador_elige_sabiendolo", r["ok"] and o.expedientes["EXP-0002"]["comparacion"]["elegido_por_operador"] is not None, r)

    # ------------------------------------------------------------ lo que no deja testigo o no cambia el resultado
    o = dos()
    o.observar("EXP-0001", COND_OBS, "decisión del operador", "OPERADOR", AHORA)
    r = o.comparar(["EXP-0002"], "D", AHORA)
    h.chk("lo_que_aparta_el_operador_no_es_testigo", r["ok"] and r["codigo"] == "OK" and r["ganador"] == "EXP-0002"
          and o.expedientes["EXP-0002"]["comparacion"]["testigos"] == [], r)
    o = dos(bueno_es=2)
    o.descartar("EXP-0001", "flojo", "GESTOR_TACTICA", AHORA)          # aparta al peor: no cambia nada
    r = o.comparar(["EXP-0002"], "D", AHORA)
    c = o.expedientes["EXP-0002"]["comparacion"]
    h.chk("apartar_al_peor_no_cambia_el_ganador", r["codigo"] == "OK" and r["ganador"] == "EXP-0002" and c["testigos"] == ["EXP-0001"]
          and c["apartado_mejor"] is None and not [x for x in o.avisos if x["codigo"] == "O-30"], r)
    o = nuevo()
    o.detectar("EXP-0009", "COR-0009", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)
    o.observar("EXP-0009", COND_OBS, "aún sin análisis", "GESTOR_TACTICA", AHORA)
    from validar_sobre import _dt as _dt0
    h.chk("un_expediente_sin_sobre_no_es_testigo", o.expedientes["EXP-0009"]["estado"] == "EN_OBSERVACION" and o._testigos("TACTICA", _dt0(AHORA), set()) == [])

    # ------------------------------------------------------------ D se abstiene, pero el apartado superaba la referencia
    o = dos(otro=MALO)
    o.observar("EXP-0001", COND_OBS, "aparcar", "GESTOR_TACTICA", AHORA)
    r = o.comparar(["EXP-0002"], "D", AHORA)
    h.chk("abstencion_con_un_apartado_que_si_superaba_O30", r["codigo"] == "O-30" and r["apartado_mejor"] == "EXP-0001"
          and r["decision_global"] == "ABSTENERSE", r)

    # ------------------------------------------------------------ un gestor solo aparta en su cartera
    o = dos()
    h.rechaza("gestor_de_otra_cartera_no_observa_O05", o, lambda: o.observar("EXP-0001", COND_OBS, "y", "GESTOR_TRADING", AHORA), "O-05")
    h.rechaza("gestor_de_otra_cartera_no_descarta_O05", o, lambda: o.descartar("EXP-0001", "y", "GESTOR_LARGO_PLAZO", AHORA), "O-05")
    h.chk("el_gestor_de_la_cartera_si", o.descartar("EXP-0001", "y", "GESTOR_TACTICA", AHORA)["ok"])

    # ------------------------------------------------------------ el ganador propuesto apartado no se sustituye en silencio
    o = dos()
    o.comparar(["EXP-0001", "EXP-0002"], "D", AHORA)
    from pruebas_orquestador import ENTRADA as E1
    r = o.proponer("EXP-0001", E1, SALIDA, "GESTOR_TACTICA", AHORA, dim(o, "EXP-0001"))
    h.chk("el_bueno_se_propone", r["ok"], r)
    o.observar("EXP-0001", COND_OBS, "lo aparco", "GESTOR_TACTICA", AHORA)
    r = o.comparar(["EXP-0002"], "D", AHORA)
    h.chk("aparcar_al_propuesto_y_comparar_O30", r["codigo"] == "O-30" and r["apartado_mejor"] == "EXP-0001", r)

    # ------------------------------------------------------------ integridad de los apartados
    o = dos()
    o.observar("EXP-0001", COND_OBS, "aparcar", "GESTOR_TACTICA", AHORA)
    o.expedientes["EXP-0001"]["historial"][-1]["actor"] = "OPERADOR"   # finge que lo apartó el operador
    r = o.comparar(["EXP-0002"], "D", AHORA)
    h.chk("apartado_con_el_actor_falseado_O13_y_kill", r["codigo"] == "O-13" and o.kill is not None and o.expedientes["EXP-0002"]["estado"] == "VALIDADA", r)
    o = dos()
    o.descartar("EXP-0001", "x", "GESTOR_TACTICA", AHORA)
    o.expedientes["EXP-0001"]["sobre"]["documento"]["payload"]["capa2"]["escenarios"][0]["rentabilidad_neta_pct"] = -50.0
    r = o.comparar(["EXP-0002"], "D", AHORA)
    h.chk("apartado_con_el_sobre_alterado_O13", r["codigo"] == "O-13" and o.kill is not None, r)
    o = dos()
    o.descartar("EXP-0001", "x", "GESTOR_TACTICA", AHORA)
    o.comparar(["EXP-0002"], "D", AHORA)
    o.expedientes["EXP-0002"]["comparacion"]["apartado_mejor"] = None
    o.expedientes["EXP-0002"]["comparacion"]["ganador"] = True
    h.chk("borrar_la_marca_del_apartado_se_detecta", o.integridad() == ["EXP:EXP-0002"])

    # ------------------------------------------------------------ el testigo deja de contar cuando vence su sobre
    o = dos()
    o.descartar("EXP-0001", "x", "GESTOR_TACTICA", AHORA)
    validar_con(o, 3, instrumento="USD/JPY")
    vence = o.expedientes["EXP-0001"]["sobre"]["valid_until"]
    from validar_sobre import _dt
    h.chk("testigo_vigente", [x["expediente_id"] for x in o._testigos("TACTICA", _dt(AHORA), set())] == ["EXP-0001"])
    h.chk("testigo_vencido_no_cuenta", o._testigos("TACTICA", _dt(vence).replace(microsecond=1), set()) == [])

    # ------------------------------------------------------------ revisión independiente (regresiones)
    # G1: apartar en dos pasos no borra el testigo
    o = dos()
    o.observar("EXP-0001", COND_OBS, "esperar", "GESTOR_TACTICA", AHORA)
    o.descartar("EXP-0001", "ya no", "GESTOR_TACTICA", AHORA)
    r = o.comparar(["EXP-0002"], "D", AHORA)
    h.chk("G1_observar_y_luego_descartar_sigue_siendo_testigo_O30", r["codigo"] == "O-30" and r["apartado_mejor"] == "EXP-0001", r)
    # G2: apartar y reabrir (nuevo encargo) tampoco
    from pruebas_orquestador import encargo
    for nombre, despues in (("queda_en_analisis", None),
                            ("y_observar", lambda o: o.observar("EXP-0001", COND_OBS, "otra vez", "GESTOR_TACTICA", AHORA)),
                            ("y_descartar", lambda o: o.descartar("EXP-0001", "fuera", "BROKER", AHORA))):
        o = dos()
        o.observar("EXP-0001", COND_OBS, "actualizar", "GESTOR_TACTICA", AHORA)
        assert o.reabrir("EXP-0001", "que lo actualice", "OPERADOR", AHORA)["ok"]   # reabrir no es ratificar el apartado
        enc = encargo(1, corte="2026-11-05")
        enc["event_id"] = "EV-ENC-0101"
        enc["payload"]["mandato"]["instrumentos_permitidos"] = ["EUR/USD", "GBP/USD", "USD/JPY"]
        r0 = o.emitir_encargo("EXP-0001", enc, "GESTOR_TACTICA", AHORA)
        if despues:
            despues(o)
        r = o.comparar(["EXP-0002"], "D", AHORA)
        h.chk(f"G2_reabrir_{nombre}_sigue_siendo_testigo_O30", r0["ok"] and r["codigo"] == "O-30" and r["apartado_mejor"] == "EXP-0001", (r0, r))
    # G3: apartar después de comparar obliga a comparar de nuevo antes de proponer o autorizar
    o = dos()
    o.comparar(["EXP-0001", "EXP-0002"], "D", AHORA)
    o.proponer("EXP-0001", ENTRADA, SALIDA, "GESTOR_TACTICA", AHORA, dim(o, "EXP-0001"))
    r = o.comparar(["EXP-0002"], "D", AHORA)              # el bueno ya está propuesto: el segundo gana solo
    h.chk("G3_el_segundo_gana_mientras_el_bueno_sigue_en_juego", r["ganador"] == "EXP-0002", r)
    o.descartar("EXP-0001", "lo quito", "GESTOR_TACTICA", AHORA)
    rp = o.proponer("EXP-0002", {**ENTRADA, "instrumento": "GBPUSD", "activo_base": "GBP"}, SALIDA, "GESTOR_TACTICA", AHORA)
    h.chk("G3_apartado_tras_comparar_proponer_O22", rp["codigo"] == "O-22" and "compare de nuevo" in rp["motivo"], rp)
    h.chk("G3_y_al_comparar_de_nuevo_O30", o.comparar(["EXP-0002"], "D", AHORA)["codigo"] == "O-30")
    from pruebas_control_f import informe_f
    from pruebas_orquestador import autorizar_op
    o = dos()
    o.comparar(["EXP-0001", "EXP-0002"], "D", AHORA)
    o.proponer("EXP-0001", ENTRADA, SALIDA, "GESTOR_TACTICA", AHORA, dim(o, "EXP-0001"))
    validar_con(o, 3, instrumento="USD/JPY", escenarios=BUENO)   # llega un candidato nuevo y lo apartan sin compararlo
    o.observar("EXP-0003", COND_OBS, "aparcar", "GESTOR_TACTICA", AHORA)
    r = autorizar_op(o, "EXP-0001", informe_f(o, "EXP-0001", 1), AHORA)
    h.chk("G3_apartado_nuevo_tras_proponer_autorizar_O22", r["codigo"] == "O-22", r)
    o = dos()
    o.comparar(["EXP-0001", "EXP-0002"], "D", AHORA)
    o.proponer("EXP-0001", ENTRADA, SALIDA, "GESTOR_TACTICA", AHORA, dim(o, "EXP-0001"))
    o.descartar("EXP-0002", "perdió", "GESTOR_TACTICA", AHORA)    # el perdedor de esa misma comparación no bloquea
    r = autorizar_op(o, "EXP-0001", informe_f(o, "EXP-0001", 1), AHORA)
    h.chk("G3_el_perdedor_de_la_misma_comparacion_no_bloquea", r["ok"], r)
    # M4: alteraciones que sacaban a un candidato sin dejar rastro
    for nombre, mut in (("cartera_del_vivo", lambda o: o.expedientes["EXP-0001"].__setitem__("cartera_destino", "TRADING")),
                        ("sobre_del_apartado", lambda o: (o.observar("EXP-0001", COND_OBS, "y", "GESTOR_TACTICA", AHORA), o.expedientes["EXP-0001"].__setitem__("sobre", None))),
                        ("encargo_del_apartado", lambda o: (o.observar("EXP-0001", COND_OBS, "y", "GESTOR_TACTICA", AHORA), o.expedientes["EXP-0001"].__setitem__("encargo_actual", None)))):
        o = dos()
        mut(o)
        r = o.comparar(["EXP-0002"], "D", AHORA)
        h.chk(f"M4_alterar_{nombre}_O13_y_kill", r["codigo"] == "O-13" and o.kill is not None and "EXP:EXP-0001" in o.integridad(), r)
    # m5: el operador ratifica un apartado
    o = dos()
    o.descartar("EXP-0001", "F lo vetó", "GESTOR_TACTICA", AHORA)
    h.rechaza("ratificar_solo_el_operador_O05", o, lambda: o.ratificar_apartado("EXP-0001", "x", "GESTOR_TACTICA", AHORA), "O-05")
    h.rechaza("ratificar_sin_motivo_O15", o, lambda: o.ratificar_apartado("EXP-0001", " ", "OPERADOR", AHORA), "O-15")
    h.rechaza("ratificar_un_vivo_O04", o, lambda: o.ratificar_apartado("EXP-0002", "x", "OPERADOR", AHORA), "O-04")
    h.chk("m5_el_operador_ratifica", o.ratificar_apartado("EXP-0001", "F lo vetó: de acuerdo", "OPERADOR", AHORA)["ok"] and o.integridad() == [])
    r = o.comparar(["EXP-0002"], "D", AHORA)
    h.chk("m5_ratificado_ya_no_es_testigo", r["codigo"] == "OK" and r["ganador"] == "EXP-0002", r)
    h.rechaza("m5_no_se_ratifica_dos_veces_O04", o, lambda: o.ratificar_apartado("EXP-0001", "otra", "OPERADOR", AHORA), "O-04")

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO APARTADOS:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
