"""Pruebas de T-33 (V0.38): tope diario por cartera de las operaciones LIBRES declaradas (CT-G-14).

Lo que demuestra: la configuración libres_tope_dia_eur (CFG-0.8.0) se valida; una LIBRE se acepta igual
bajo el tope y se acepta también al superarlo (con aviso O-37 de prioridad ALTA y degradación de la
cartera a L1); el importe en euros sale de la última foto de G (None si no hay foto, divisa o tipo, o si
el producto no es finito); el tope se acumula por cartera y día UTC y se empieza de cero cada día; F-14
cuenta las LIBRES del día en importe_dia_eur (de todas las carteras, con reproducibilidad CF-09: un
informe emitido antes del registro sigue validando y uno emitido después las cuenta y recorta).

Uso: python3 pruebas/pruebas_libres_t33.py
"""
import copy
import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))

from control_f import POLITICA_DEFECTO, validar_informe_f  # noqa: E402
from orquestador import CONFIG_DEFECTO, PRIORIDAD_AVISO  # noqa: E402
from pruebas_control_f import CART, informe_f, registrar_foto  # noqa: E402
from pruebas_manual import T1, libre  # noqa: E402
from pruebas_orquestador import AHORA, Arnes, autorizar_op, nuevo, hasta  # noqa: E402

# las dos fotos de prueba: tipos neutros con el GBP valorado (y sin él, para el caso sin tipo)
FOTO = {**CART, "tipos_cambio_eur": {"USD": 1.0, "GBP": 1.2}}
FOTO_SIN_GBP = {**CART, "tipos_cambio_eur": {"USD": 1.0}}
DIA1, DIA2 = "2026-11-06", "2026-11-07"
T_MAN = "2026-11-07T09:00:00+00:00"   # el día siguiente (UTC)


def avisos(o, codigo):
    return [x for x in o.avisos if x["codigo"] == codigo]


def registrar(o, **kw):
    """Registra una LIBRE con su instante (T1 por defecto) y devuelve la respuesta."""
    instante = kw.pop("registrado_en", T1)
    return o.registrar_manual(libre(**kw), instante)


def suma_del_dia(o, cartera, dia):
    return math.fsum(x["importe_eur"] for x in o.libres if x["cartera"] == cartera and x["dia"] == dia
                     and x["importe_eur"] is not None)


def vf(o, inf):
    """La verificación CF del informe con el contexto que el Orquestador recalcula en su emisión (CF-09)."""
    x = o.expedientes["EXP-0001"]
    return sorted({z["regla"] for z in validar_informe_f(inf, {"ahora": inf["emitido_en"], "expediente_id": "EXP-0001",
                                                               "correlation_id": x["correlation_id"], "divisa_cotizacion": "USD",
                                                               "propuesta": x["propuesta"], "cartera_destino": x["cartera_destino"],
                                                               "politica": o.cfg["politica_f"], "contexto": o._contexto_de_informe("EXP-0001", inf)})})


def main():
    h = Arnes()
    L2 = {"nivel_autonomia": {"TRADING": "L2", "TACTICA": "L2", "LARGO_PLAZO": "L2"}}

    # ------------------------------------------------------------------ configuración (CFG-0.8.0)
    h.chk("version_CFG_080_y_topes_por_defecto", tuple(map(int, CONFIG_DEFECTO["version_config"][4:].split("."))) >= (0, 8, 0)   # V0.53: 0.11.0 integra 0.8.0
          and CONFIG_DEFECTO["libres_tope_dia_eur"] == {"TRADING": 2000.0, "TACTICA": 2000.0, "LARGO_PLAZO": 2000.0}
          and nuevo().cfg["libres_tope_dia_eur"] == CONFIG_DEFECTO["libres_tope_dia_eur"])
    for nombre, tope_malo in (("config_falta_una_cartera", {"TRADING": 2000.0, "TACTICA": 2000.0}),
                              ("config_con_una_cartera_de_mas", {"TRADING": 2000.0, "TACTICA": 2000.0, "LARGO_PLAZO": 2000.0, "OTRA": 1.0}),
                              ("config_tope_negativo", {"TRADING": -1.0, "TACTICA": 2000.0, "LARGO_PLAZO": 2000.0}),
                              ("config_tope_nan", {"TRADING": float("nan"), "TACTICA": 2000.0, "LARGO_PLAZO": 2000.0}),
                              ("config_tope_texto", {"TRADING": "2000", "TACTICA": 2000.0, "LARGO_PLAZO": 2000.0})):
        bien = True
        try:
            nuevo({"libres_tope_dia_eur": tope_malo})
            bien = False   # tenía que rechazarlo
        except ValueError:
            pass
        h.chk(nombre, bien)
    try:
        o = nuevo({**L2, "libres_tope_dia_eur": {"TRADING": 0.0, "TACTICA": 0.0, "LARGO_PLAZO": 0.0}})
    except ValueError:
        o = None
    # r03 (revisión): la comprobación ya no afirma una literal — comprueba que el tope 0.0 se admite (la prohibición, la de abajo)
    h.chk("config_tope_cero_es_valido_y_prohibe", o is not None
          and o.cfg["libres_tope_dia_eur"] == {"TRADING": 0.0, "TACTICA": 0.0, "LARGO_PLAZO": 0.0}, o)
    if o is None:   # el tope 0.0 dejó de admitirse: no hay nada más que comprobar en esta batería
        print(f"RESULTADO T-33: HAY FALLOS ({h.n} comprobaciones)")
        return 1
    registrar_foto(o, FOTO_SIN_GBP)
    r = registrar(o, instrumento="EURUSD", activo_base="EUR", cantidad=100.0, precio=1.0,
                  event_id="EV-MAN-0002", ref_intermediario="MAN-CERO-1")
    h.chk("con_tope_cero_cualquier_libre_lo_supera", r["ok"] and r["tope_libres_superado"] is True
          and len(avisos(o, "O-37")) == 1 and o.nivel("TACTICA") == "L1", r)

    # ------------------------------------------------------------------ bajo el tope: aceptado, sin O-37, con importe
    o = nuevo(L2)
    registrar_foto(o, FOTO)
    r = registrar(o)   # GBPUSD 50 × 1,30 con USD a 1,0 -> 65 EUR
    h.chk("bajo_el_tope_sin_O37_ni_degradacion", r["ok"] and r["tope_libres_superado"] is False
          and avisos(o, "O-37") == [] and "TACTICA" not in o.degradadas and o.nivel("TACTICA") == "L2", r)
    h.chk("la_fila_del_registro_en_libres", len(o.libres) == 1
          and set(o.libres[0]) == {"cartera", "dia", "importe_eur", "registrado_en", "event_id"}
          and o.libres[0]["cartera"] == "TACTICA" and o.libres[0]["dia"] == DIA1
          and abs(o.libres[0]["importe_eur"] - 65.0) < 1e-9   # GBPUSD cotiza en USD: 50 × 1,30 × 1,0
          and o.libres[0]["registrado_en"] == T1
          and o.libres[0]["event_id"] == "EV-MAN-0010", o.libres)
    h.chk("registro_aparte_manuales_sigue_igual", len(o.manuales) == 1 and o.manuales[0]["event_id"] == "EV-MAN-0010"
          and "vinculo" in o.manuales[0] and "dia" not in o.manuales[0], o.manuales[0])
    o2 = nuevo({**L2, "tolerancia_tipo_k_rel": 0.5, "tolerancia_tipo_k_rel_principales": 0.5})   # el cierre de K no lleva este tipo: holgura de contraste para la foto de la prueba
    registrar_foto(o2, {**CART, "tipos_cambio_eur": {"USD": 1.15}})
    registrar(o2, instrumento="EURUSD", activo_base="EUR", cantidad=100.0, precio=1.10,
              event_id="EV-MAN-0011", ref_intermediario="MAN-USD-1")
    h.chk("un_libre_en_usd_se_valora_con_el_tipo_de_la_foto", abs(o2.libres[0]["importe_eur"] - 126.5) < 1e-9
          and o2.libres[0]["dia"] == DIA1, o2.libres)
    o3 = nuevo({**L2, "divisas_cotizacion": {"IBEX": "EUR"}})
    registrar(o3, instrumento="IBEX", activo_base="EUR", cantidad=0.5, precio=3000.0,
              event_id="EV-MAN-0012", ref_intermediario="MAN-EUR-1")
    h.chk("un_libre_en_euros_se_valora_con_uno", o3.libres[0]["importe_eur"] == 1500.0
          and o3.libres[0]["importe_eur"] < o3.cfg["libres_tope_dia_eur"]["TACTICA"], o3.libres)

    # ------------------------------------------------------------------ el tope se supera: O-37, degradación, aceptado
    o = nuevo(L2)
    registrar_foto(o, FOTO)
    r = registrar(o, cantidad=20000.0, event_id="EV-MAN-0013", ref_intermediario="MAN-BIG-1")
    suma = suma_del_dia(o, "TACTICA", DIA1)
    o37 = avisos(o, "O-37")
    h.chk("al_superar_el_tope_O37_alta_con_cartera", r["ok"] and r["tope_libres_superado"] is True and len(o37) == 1
          and o37[0]["prioridad"] == "ALTA" and o37[0]["carteras"] == ["TACTICA"] and o37[0]["ref"] == "EV-MAN-0013"
          and o37[0]["motivo"] == f"operaciones libres de TACTICA el {DIA1}: {suma} EUR por encima del tope 2000.0 EUR", o37)
    h.chk("la_cartera_superada_se_degrada_a_L1", o.nivel("TACTICA") == "L1" and list(o.degradadas) == ["TACTICA"]
          and any(x["codigo"] == "O-19" and x["carteras"] == ["TACTICA"] for x in o.avisos), o.degradadas)
    h.chk("las_otras_carteras_sin_tocar", o.nivel("TRADING") == "L2" and o.nivel("LARGO_PLAZO") == "L2"
          and "TRADING" not in o.degradadas and "LARGO_PLAZO" not in o.degradadas)
    h.chk("el_registro_sigue_aceptado_y_esta_en_manuales", r["codigo"] == "OK" and len(o.manuales) == 1
          and o.manuales[0]["instrumento"] == "GBPUSD" and o.eventos["EV-MAN-0013"]["expediente_id"] is None, r)

    o = nuevo(L2)
    registrar_foto(o, FOTO)
    r1 = registrar(o, cantidad=1000.0, event_id="EV-MAN-0015", ref_intermediario="MAN-DOS-1")   # 1.300 EUR
    r2 = registrar(o, cantidad=800.0, event_id="EV-MAN-0016", ref_intermediario="MAN-DOS-2")    # 2.340 EUR en el día
    h.chk("dos_libres_que_juntos_superan_el_tope", r1["tope_libres_superado"] is False and r2["tope_libres_superado"] is True
          and len(avisos(o, "O-37")) == 1 and o.nivel("TACTICA") == "L1", (r1, r2))

    # ------------------------------------------------------------------ el día siguiente (UTC) se empieza de cero
    r3 = registrar(o, cantidad=800.0, event_id="EV-MAN-0017", ref_intermediario="MAN-D3-1",
                   emitido_en="2026-11-07T08:59:00+00:00", ejecutado_en="2026-11-07T08:58:00+00:00", registrado_en=T_MAN)
    h.chk("al_dia_siguiente_se_empieza_de_cero", r3["ok"] and r3["tope_libres_superado"] is False
          and len(avisos(o, "O-37")) == 1, r3)
    r4 = registrar(o, cantidad=800.0, event_id="EV-MAN-0018", ref_intermediario="MAN-D3-2",
                   emitido_en="2026-11-07T08:59:00+00:00", ejecutado_en="2026-11-07T08:58:00+00:00",
                   registrado_en="2026-11-07T09:01:00+00:00")
    suma2 = suma_del_dia(o, "TACTICA", DIA2)
    o37b = avisos(o, "O-37")
    h.chk("el_aviso_del_nuevo_dia_solo_suma_su_dia", r4["tope_libres_superado"] is True and len(o37b) == 2
          and o37b[1]["motivo"] == f"operaciones libres de TACTICA el {DIA2}: {suma2} EUR por encima del tope 2000.0 EUR"
          and str(DIA1) not in o37b[1]["motivo"] and abs(suma2 - 2080.0) < 1e-9, o37b[1])

    # ------------------------------------------------------------------ sin poder valorar: tope superado (falla cerrado)
    o = nuevo(L2)   # sin foto de G: no hay tipos de cambio
    r = registrar(o)
    h.chk("sin_foto_se_trata_como_tope_superado", r["ok"] and r["tope_libres_superado"] is True
          and o.libres[0]["importe_eur"] is None
          and avisos(o, "O-37")[0]["motivo"] == f"operaciones libres de TACTICA el {DIA1}: sin poder valorarlas en euros"
          and o.nivel("TACTICA") == "L1", r)
    o = nuevo(L2)
    registrar_foto(o, FOTO_SIN_GBP)   # la foto no lleva el tipo del JPY, la divisa en que cotiza el USDJPY
    r = registrar(o, instrumento="USDJPY", activo_base="USD", cantidad=10000.0, precio=150.0,
                  event_id="EV-MAN-0019b", ref_intermediario="MAN-JPY-1")
    h.chk("una_divisa_sin_tipo_se_trata_como_tope_superado", r["ok"] and r["tope_libres_superado"] is True
          and o.libres[0]["importe_eur"] is None and len(avisos(o, "O-37")) == 1 and "TACTICA" in o.degradadas, r)
    o = nuevo(L2)
    registrar_foto(o, FOTO)
    r = registrar(o, instrumento="XAU", activo_base="XAU", cantidad=1.0, precio=1800.0,
                  event_id="EV-MAN-0019", ref_intermediario="MAN-XAU-1")
    h.chk("un_instrumento_sin_divisa_conocida_sin_valor", r["ok"] and r["tope_libres_superado"] is True
          and o.libres[0]["importe_eur"] is None and "sin poder valorarlas" in avisos(o, "O-37")[0]["motivo"], r)
    o = nuevo(L2)
    registrar_foto(o, FOTO_SIN_GBP)
    r = registrar(o, instrumento="EURUSD", activo_base="EUR", cantidad=1e308, precio=1e308,
                  event_id="EV-MAN-0020", ref_intermediario="MAN-OVF-1")
    h.chk("un_producto_no_finito_no_se_valora", r["ok"] and r["tope_libres_superado"] is True
          and o.libres[0]["importe_eur"] is None and len(avisos(o, "O-37")) == 1, r)
    # r02 (revisión): un producto que subdesborda a 0.0 tampoco se valora — con tope 0.0 no puede pasar por un importe real de 0 EUR
    o = nuevo({**L2, "libres_tope_dia_eur": {"TRADING": 0.0, "TACTICA": 0.0, "LARGO_PLAZO": 0.0}})
    registrar_foto(o, FOTO_SIN_GBP)
    r = registrar(o, instrumento="EURUSD", activo_base="EUR", cantidad=1e-200, precio=1e-200,
                  event_id="EV-MAN-0020e", ref_intermediario="MAN-SUB-1")
    h.chk("r02_un_producto_que_subdesborda_a_cero_no_se_valora_como_cero", r["ok"] and r["tope_libres_superado"] is True
          and o.libres[0]["importe_eur"] is None and "sin poder valorarlas" in avisos(o, "O-37")[0]["motivo"], r)
    o = nuevo(L2)
    registrar_foto(o, FOTO_SIN_GBP)
    r = registrar(o, instrumento="EURUSD", activo_base="EUR", cantidad=10**300, precio=10**300,
                  event_id="EV-MAN-0020b", ref_intermediario="MAN-OVF-2")
    h.chk("defecto_01_dos_enteros_enormes_se_aceptan_y_no_se_valoran", r["ok"] and r["tope_libres_superado"] is True
          and o.libres[0]["importe_eur"] is None and "sin poder valorarlas" in avisos(o, "O-37")[0]["motivo"], r)
    o = nuevo(L2)
    registrar_foto(o, FOTO_SIN_GBP)
    r1 = registrar(o, instrumento="EURUSD", activo_base="EUR", cantidad=1e308, precio=1.0,
                   event_id="EV-MAN-0020c", ref_intermediario="MAN-OVF-3")   # importe 1e308, finito
    r2 = registrar(o, instrumento="EURUSD", activo_base="EUR", cantidad=1e308, precio=1.0,
                   event_id="EV-MAN-0020d", ref_intermediario="MAN-OVF-4")   # la suma se desborda a infinito: aviso, no excepción
    h.chk("defecto_02_la_suma_desbordada_avisa_y_no_lanza", r1["ok"] and r2["ok"] and r2["tope_libres_superado"] is True
          and o.libres[0]["importe_eur"] == 1e308 and "por encima del tope" in avisos(o, "O-37")[0]["motivo"], (r1, r2))

    # ------------------------------------------------------------------ una LIBRE tardía cuenta en su día de ejecución
    o = nuevo(L2)
    registrar_foto(o, FOTO)
    hasta(o, "PROPUESTA")
    r = registrar(o, cantidad=20000.0, event_id="EV-MAN-0021", ref_intermediario="MAN-TAR-1",
                  emitido_en=T1, ejecutado_en="2026-11-05T15:00:00+00:00")   # ejecutada el día 5, declarada el día 6
    h.chk("una_libre_tardia_avisa_por_su_dia_de_ejecucion", r["ok"] and r["tope_libres_superado"] is True
          and o.libres[0]["dia"] == "2026-11-05"
          and f"operaciones libres de TACTICA el 2026-11-05: {suma_del_dia(o, 'TACTICA', '2026-11-05')} EUR" in avisos(o, "O-37")[0]["motivo"],
          avisos(o, "O-37"))
    h.chk("y_no_infla_el_importe_de_hoy_en_F", o.contexto_f("EXP-0001", "2026-11-06T10:00:00+00:00")["actividad"]["importe_dia_eur"] == 0.0)

    # ------------------------------------------------------------------ F-14 ve las LIBRES (contexto y CF-09)
    o = nuevo(L2)
    registrar_foto(o, FOTO)
    hasta(o, "PROPUESTA")
    registrar(o, event_id="EV-MAN-0022", ref_intermediario="MAN-C1-1", emitido_en=T1, ejecutado_en=AHORA)   # 65 EUR, el de hoy no: el de ayer
    registrar(o, cantidad=100.0, event_id="EV-MAN-0023", ref_intermediario="MAN-C1-2",
              emitido_en="2026-11-07T08:59:00+00:00", ejecutado_en="2026-11-07T08:58:00+00:00", registrado_en=T_MAN)   # 130 EUR hoy
    h.chk("contexto_f_incluye_el_libre_de_hoy_y_no_el_de_ayer",
          o.contexto_f("EXP-0001", "2026-11-06T10:00:00+00:00")["actividad"]["importe_dia_eur"] == 65.0
          and o.contexto_f("EXP-0001", "2026-11-07T10:00:00+00:00")["actividad"]["importe_dia_eur"] == 130.0)
    o = nuevo(L2)
    registrar_foto(o, FOTO)
    hasta(o, "PROPUESTA")
    registrar(o, event_id="EV-MAN-0024", ref_intermediario="MAN-CT-1")                                        # TACTICA: 65 EUR
    registrar(o, cartera="TRADING", event_id="EV-MAN-0025", ref_intermediario="MAN-CT-2", cantidad=1000.0)    # TRADING: 1.300 EUR
    h.chk("los_libres_de_todas_las_carteras_cuentan_en_F",
          o.contexto_f("EXP-0001", "2026-11-06T10:00:00+00:00")["actividad"]["importe_dia_eur"] == 1365.0)

    # el informe emitido antes de la LIBRE sigue validando (CF-09); el emitido después la cuenta y F-14 recorta
    POL = {**POLITICA_DEFECTO, "importe_max_dia_eur": 5000.0, "importe_max_orden_eur": 5000.0}
    o = nuevo({"politica_f": POL, **L2})
    hasta(o, "PROPUESTA")
    inf1 = informe_f(o, "EXP-0001", 2, emitido_en="2026-11-06T09:10:00+00:00")
    h.chk("el_informe_anterior_es_valido", vf(o, inf1) == [], vf(o, inf1))
    r = registrar(o, instrumento="EURUSD", activo_base="EUR", cantidad=4450.0, precio=1.10,
                  event_id="EV-MAN-0026", ref_intermediario="MAN-F14-1",
                  emitido_en="2026-11-06T09:15:00+00:00", ejecutado_en="2026-11-06T09:14:00+00:00",
                  registrado_en="2026-11-06T09:15:00+00:00")   # 4.895 EUR, después del informe
    h.chk("el_informe_anterior_sigue_validando_tras_la_libre", r["ok"] and vf(o, inf1) == [], vf(o, inf1))
    assert o.registrar_cotizacion({"instrumento": "EURUSD", "valor": 1.10, "fecha_hora": "2026-11-06T09:14:00+00:00"},
                                  "G", "2026-11-06T09:16:00+00:00")["ok"]   # G refresca el precio: sin F-23 el recorte es de F-14
    inf2 = informe_f(o, "EXP-0001", 3, emitido_en="2026-11-06T09:20:00+00:00")
    ctx2 = o.contexto_f("EXP-0001", "2026-11-06T09:20:00+00:00")
    importe = o.libres[0]["importe_eur"]
    c14 = next(c for c in inf2["resultado_politica"]["controles"] if c["regla"] == "F-14")
    h.chk("un_informe_posterior_cuenta_la_libre", vf(o, inf2) == [] and ctx2["actividad"]["importe_dia_eur"] == importe
          and abs(importe - 4895.0) < 1e-6, (vf(o, inf2), ctx2["actividad"]))
    h.chk("f14_recorta_cuando_el_dia_ya_va_cargado", inf2["resultado_politica"]["resultado"] == "REDUCIDO"
          and c14["resultado"] == "REDUCE" and abs(c14["limite"] - (5000.0 - importe) / 1.1) < 1e-9
          and abs(inf2["payload"]["cantidad_aprobada"] - c14["limite"]) < 2e-6   # F redondea la cantidad a 1e-6
          and 90.0 < inf2["payload"]["cantidad_aprobada"] < 100.0, c14)

    # r01 (revisión): una LIBRE declarada entre el informe y la autorización frena a esta — el guardia de T-22
    # solo veía a otros expedientes, y el día quedaba cargado por encima del tope de F-14 sin veto ni aviso
    POLr1 = {**POLITICA_DEFECTO, "importe_max_dia_eur": 150.0, "importe_max_orden_eur": 150.0}
    o = nuevo({"politica_f": POLr1, **L2})
    hasta(o, "PROPUESTA")
    registrar_foto(o, FOTO)
    infr1 = informe_f(o, "EXP-0001", 1, cartera={**FOTO}, emitido_en=AHORA)
    assert infr1["resultado_politica"]["resultado"] == "APROBADO", infr1["resultado_politica"]["resultado"]
    registrar(o, instrumento="GBPUSD", activo_base="GBP", cantidad=50.0, precio=1.30,
              event_id="EV-MAN-0030", ref_intermediario="MAN-R01-1",   # 65 EUR, bajo el tope de cartera: sin O-37
              emitido_en="2026-11-06T09:05:00+00:00", ejecutado_en="2026-11-06T09:04:00+00:00",
              registrado_en="2026-11-06T09:05:00+00:00")
    rar1 = autorizar_op(o, "EXP-0001", infr1, "2026-11-06T09:10:00+00:00")
    h.chk("r01_una_libre_posterior_al_informe_frena_la_autorizacion", not rar1["ok"] and rar1["codigo"] == "O-10"
          and "LIBRE" in rar1["motivo"] and o.expedientes["EXP-0001"]["estado"] != "AUTORIZADA", rar1)

    # V0.53 (revisión de la integración, g05 M1): la suma exactamente igual al tope no avisa; un céntimo por encima, sí
    importe = 50.0 * 1.30 * 1.0   # la LIBRE de libre(): 50 GBPUSD a 1,30 USD, con USD a 1,0 EUR
    for nombre, tope, avisa in (("igual_al_tope_no_avisa", importe, False), ("por_encima_avisa", importe - 0.01, True)):
        o = nuevo({"libres_tope_dia_eur": {"TRADING": 2000.0, "TACTICA": tope, "LARGO_PLAZO": 2000.0}})
        registrar_foto(o, FOTO)
        r = registrar(o)
        h.chk(f"r04_suma_{nombre}", r["ok"] and r["tope_libres_superado"] is avisa and bool(avisos(o, "O-37")) is avisa, r)

    # ------------------------------------------------------------------ el aviso nuevo y su prioridad
    h.chk("O37_es_un_aviso_de_prioridad_ALTA", PRIORIDAD_AVISO["O-37"] == "ALTA")

    print(f"RESULTADO T-33: {'TODAS LAS PRUEBAS PASAN' if h.ok else 'HAY FALLOS'} ({h.n} comprobaciones)")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
