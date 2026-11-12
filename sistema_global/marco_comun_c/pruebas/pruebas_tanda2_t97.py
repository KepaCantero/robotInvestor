"""Pruebas de T-97 (V0.74): valores por defecto de la tanda 2. Tope anual de gasto en IA y datos en % del capital (O-43), F-14 y
F-16 (semana) también en % del capital, tolerancia del tipo de cambio por divisa y MIG-010. Datos SIMULADOS.

Uso: python3 pruebas/pruebas_tanda2_t97.py
"""
import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
import migraciones as mg  # noqa: E402
from control_f import POLITICA_DEFECTO, VERSION_REGLAS, controlar, controles_de_contexto, politica_valida  # noqa: E402
from orquestador import CONFIG_DEFECTO, Orquestador  # noqa: E402
from pruebas_control_f import AHORA_F, CART, solicitud  # noqa: E402
from pruebas_control_f_t22 import CTX, cx  # noqa: E402
from pruebas_k import CAL, construir  # noqa: E402
from pruebas_orquestador import AHORA, CART_E, CFG, Arnes, encargo, nuevo  # noqa: E402

P = POLITICA_DEFECTO
SIN_TOPE_DE_PRUEBAS = {"tope_anual_gasto_pct_capital": 0.5, "capital_referencia_eur": None}   # los valores de partida, no los de mecánica


def regla(r, nombre):
    return [c for c in r["controles"] if c["regla"] == nombre]


def detectar(o, n):
    return o.detectar(f"EXP-{n:04d}", f"COR-{n:04d}", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)


def emitir(o, n):
    assert detectar(o, n)["ok"]
    return o.emitir_encargo(f"EXP-{n:04d}", encargo(n), "GESTOR_TACTICA", AHORA)


def foto(capital=100000.0, usd=1.0, hora="2026-11-06T08:55:00+00:00"):
    return {**copy.deepcopy(CART_E), "fecha_hora": hora, "capital_eur": capital, "tipos_cambio_eur": {"USD": usd}}


def main():
    h = Arnes()

    # ------------------------------------------------------------------ configuración y valores de partida
    h.chk("valores_de_partida", CONFIG_DEFECTO["tope_anual_gasto_pct_capital"] == 0.5 and CONFIG_DEFECTO["capital_referencia_eur"] is None
          and CONFIG_DEFECTO["tolerancia_tipo_k_rel_principales"] == 0.005 and CONFIG_DEFECTO["tolerancia_tipo_k_rel"] == 0.03
          and CONFIG_DEFECTO["divisas_principales"] == ["USD", "GBP", "JPY", "CHF"] and CONFIG_DEFECTO["version_config"] == "CFG-0.12.0"
          and P["importe_max_dia_pct"] == 25.0 and P["perdida_semana_max_pct_trading"] == 4.0
          and P["perdida_semana_max_pct_tactica"] == 5.0 and P["perdida_semana_max_pct_largo_plazo"] == 5.0 and VERSION_REGLAS == "F-0.4.0")
    malas = (("principales_mas_laxa_que_la_general", {"tolerancia_tipo_k_rel": 0.03, "tolerancia_tipo_k_rel_principales": 0.04}),
             ("principales_cero", {"tolerancia_tipo_k_rel_principales": 0.0}),
             ("divisa_principal_eur", {"divisas_principales": ["USD", "EUR"]}),
             ("divisa_principal_repetida", {"divisas_principales": ["USD", "USD"]}),
             ("divisa_principal_mal_formada", {"divisas_principales": ["usd"]}),
             ("divisas_principales_no_lista", {"divisas_principales": "USD"}),
             ("tope_anual_cero", {"tope_anual_gasto_pct_capital": 0.0}),
             ("tope_anual_mayor_que_10", {"tope_anual_gasto_pct_capital": 10.5}),
             ("tope_anual_infinito", {"tope_anual_gasto_pct_capital": float("inf")}),
             ("capital_referencia_negativo", {"capital_referencia_eur": -1.0}),
             ("capital_referencia_cero", {"capital_referencia_eur": 0.0}),
             ("capital_referencia_texto", {"capital_referencia_eur": "1000"}))
    for nombre, cambio in malas:
        try:
            Orquestador({**CFG, **cambio}, CAL)
            h.chk(f"config_{nombre}_no_arranca", False, cambio)
        except ValueError:
            h.chk(f"config_{nombre}_no_arranca", True)
    for nombre, pol in (("dia_pct_mayor_que_100", {**P, "importe_max_dia_pct": 150.0}), ("semana_pct_cero", {**P, "perdida_semana_max_pct_tactica": 0.0}),
                        ("sin_las_claves_nuevas", {k: v for k, v in P.items() if k != "importe_max_dia_pct"})):
        h.chk(f"politica_{nombre}_invalida", not politica_valida(pol))

    # ------------------------------------------------------------------ tope anual de gasto (E2)
    o = nuevo(SIN_TOPE_DE_PRUEBAS)
    r = emitir(o, 1)
    h.chk("sin_foto_ni_capital_declarado_no_hay_encargo_con_coste", not r["ok"] and r["codigo"] == "O-43" and "sin foto" in r["motivo"], r)
    o = nuevo({**SIN_TOPE_DE_PRUEBAS, "capital_referencia_eur": 1000.0})   # 0,5 % de 1.000 € = 5 € al año; cada encargo reserva 5 €
    h.chk("con_capital_declarado_el_primero_cabe", emitir(o, 1)["ok"])
    r = emitir(o, 2)
    h.chk("el_segundo_no_cabe_por_la_reserva_del_primero_O43", not r["ok"] and r["codigo"] == "O-43" and "tope anual" in r["motivo"], r)
    r = o.registrar_gasto("EV-ENC-0001", 5.0, 1.0, AHORA)
    h.chk("al_llegar_al_tope_registrar_gasto_avisa_O43", r["ok"] and "O-43" in r["alertas"]
          and any(a["codigo"] == "O-43" and a["prioridad"] == "ALTA" for a in o.avisos), r)
    h.chk("una_rutina_sin_IA_sigue_con_el_tope_agotado", o.registrar_cartera(foto(capital=1000.0), "G", AHORA, cuenta="SIM-1")["ok"])
    o = nuevo({**SIN_TOPE_DE_PRUEBAS, "capital_referencia_eur": 1000.0})
    assert o.registrar_cartera(foto(), "G", AHORA, cuenta="SIM-1")["ok"]   # 100.000 € en la foto: 500 € al año
    h.chk("con_foto_manda_la_foto_y_no_el_capital_declarado", emitir(o, 1)["ok"] and emitir(o, 2)["ok"])
    ga, ra, tope = o._gasto_anio(datetime(2026, 11, 6, 9, tzinfo=timezone.utc))
    h.chk("tope_en_euros_y_reservas", abs(tope - 500.0) < 1e-9 and ga == 0.0 and abs(ra - 10.0) < 1e-9, (ga, ra, tope))
    o.gasto_dia["2025-12-31"] = {"coste": 400.0, "tiempo": 1.0}
    o.gasto_dia["2026-01-02"] = {"coste": 7.0, "tiempo": 1.0}
    ga, _, _ = o._gasto_anio(datetime(2026, 11, 6, 9, tzinfo=timezone.utc))
    h.chk("el_anio_natural_no_arrastra_el_anterior", abs(ga - 7.0) < 1e-9, ga)
    o = nuevo()   # las pruebas de mecánica (10 % de 100.000 €) no tocan el tope
    h.chk("el_tope_diario_sigue_siendo_el_segundo_limite", o.cfg["dia_coste_max_eur"] == 50.0 and emitir(o, 1)["ok"])

    # ------------------------------------------------------------------ F-14 y F-16 (semana) en % del capital (F1 y F2)
    sol = solicitud(cantidad=100000.0)
    ent_eur = sol["precio_entrada"] * CART["tipos_cambio_eur"]["USD"]   # euros por unidad (tipo neutro de las pruebas de F)
    peq = controlar(sol, {**CART, "capital_eur": 20000.0}, P, AHORA_F, cx(actividad__importe_dia_eur=4500.0))
    f14 = regla(peq, "F-14")[0]
    h.chk("cartera_pequena_F14_frena_al_25_por_ciento", f14["resultado"] == "REDUCE" and abs(f14["limite"] * ent_eur - 500.0) < 1e-6, f14)
    gra = controlar(sol, {**CART, "capital_eur": 1e6}, P, AHORA_F, cx(actividad__importe_dia_eur=4500.0))
    f14g = regla(gra, "F-14")[0]
    h.chk("cartera_grande_F14_como_en_V073_en_euros", abs(f14g["limite"] * ent_eur - 45500.0) < 1e-6, f14g)
    pol_v073 = {**P, "importe_max_dia_pct": 100.0, "perdida_semana_max_pct_trading": 100.0, "perdida_semana_max_pct_tactica": 100.0,
                "perdida_semana_max_pct_largo_plazo": 100.0}
    h.chk("cartera_grande_mismo_resultado_que_sin_los_porcentajes",
          {k: gra[k] for k in ("resultado", "cantidad_aprobada")} == {k: controlar(sol, {**CART, "capital_eur": 1e6}, pol_v073, AHORA_F, cx(actividad__importe_dia_eur=4500.0))[k] for k in ("resultado", "cantidad_aprobada")})
    sem = cx(actividad__perdida_semana_eur=800.0)   # 4 % de 20.000 €
    tr = controlar(solicitud(cartera="TRADING"), {**CART, "capital_eur": 20000.0}, P, AHORA_F, sem)
    ta = controlar(solicitud(cartera="TACTICA"), {**CART, "capital_eur": 20000.0}, P, AHORA_F, sem)
    lp = controlar(solicitud(cartera="LARGO_PLAZO"), {**CART, "capital_eur": 20000.0}, P, AHORA_F, cx(actividad__perdida_semana_eur=1000.0))
    h.chk("trading_con_4_por_ciento_en_la_semana_no_abre", tr["resultado"] == "VETADO" and [c for c in regla(tr, "F-16") if c["resultado"] == "VETA"], tr["controles"])
    h.chk("tactica_con_4_por_ciento_si_abre", ta["resultado"] != "VETADO", ta["controles"])
    h.chk("largo_plazo_con_5_por_ciento_no_abre", lp["resultado"] == "VETADO", lp["controles"])
    gr = controlar(solicitud(cartera="TRADING"), {**CART, "capital_eur": 1e6}, P, AHORA_F, sem)
    h.chk("cartera_grande_la_semana_manda_en_euros", gr["resultado"] != "VETADO"
          and any(c["limite"] == 5000.0 for c in regla(gr, "F-16")), regla(gr, "F-16"))
    h.chk("al_enviar_con_capital_se_aplica_el_porcentaje",
          any(c["regla"] == "F-16" and c["resultado"] == "VETA" for c in controles_de_contexto(solicitud(cartera="TRADING"), P, AHORA_F, sem, 20000.0)))
    h.chk("al_enviar_sin_capital_solo_euros",
          not any(c["resultado"] == "VETA" for c in controles_de_contexto(solicitud(cartera="TRADING"), P, AHORA_F, sem)))
    for nombre, cap in (("cero", 0.0), ("negativo", -5.0), ("infinito", float("inf")), ("texto", "20000")):
        c = controles_de_contexto(solicitud(cartera="TRADING"), P, AHORA_F, CTX, cap)
        h.chk(f"al_enviar_capital_{nombre}_falla_cerrado", len(c) == 1 and c[0]["regla"] == "F-01" and c[0]["resultado"] == "VETA", c)

    # ------------------------------------------------------------------ tolerancia del tipo de cambio por divisa (A3)
    _, r = construir()
    s = r["sello"]
    k = 1 / next(x for x in s["fuentes"] if x["fuente_id"] == "SRC-EURUSD")["ultimo_cierre"]   # euros por dólar según K

    def contraste(cfg, usd):
        o = Orquestador({**CFG, **cfg}, CAL)
        assert o.registrar_sello(s, AHORA)["ok"]
        return o.registrar_cartera(foto(usd=round(usd, 8)), "G", AHORA, cuenta="SIM-1")
    defecto = {"tolerancia_tipo_k_rel": 0.03, "tolerancia_tipo_k_rel_principales": 0.005, "divisas_principales": ["USD", "GBP", "JPY", "CHF"]}
    r = contraste(defecto, k * 1.006)
    h.chk("usd_principal_con_0_6_por_ciento_se_rechaza", not r["ok"] and r["codigo"] == "O-29" and "0,5 %" not in r["motivo"] and "0.5%" in r["motivo"], r)
    h.chk("usd_principal_con_0_4_por_ciento_pasa", contraste(defecto, k * 1.004)["ok"])
    h.chk("usd_sin_ser_principal_con_0_6_por_ciento_pasa", contraste({**defecto, "divisas_principales": ["GBP"]}, k * 1.006)["ok"])
    r = contraste({**defecto, "divisas_principales": ["GBP"]}, k * 1.031)
    h.chk("usd_sin_ser_principal_con_3_1_por_ciento_se_rechaza", not r["ok"] and r["codigo"] == "O-29" and "3%" in r["motivo"], r)
    h.chk("usd_principal_con_3_1_por_ciento_se_rechaza", contraste(defecto, k * 1.031)["codigo"] == "O-29")
    o = Orquestador({**CFG, **defecto}, CAL)
    h.chk("divisa_sin_clasificar_usa_la_general", o.tolerancia_tipo_k("SEK") == 0.03 and o.tolerancia_tipo_k("USD") == 0.005)

    # ------------------------------------------------------------------ MIG-010
    cfg_v073 = copy.deepcopy({k: v for k, v in CONFIG_DEFECTO.items() if k not in ("tope_anual_gasto_pct_capital", "capital_referencia_eur",
                                                                                   "tolerancia_tipo_k_rel_principales", "divisas_principales")})
    cfg_v073["version_config"] = "CFG-0.11.0"
    cfg_v073["tolerancia_tipo_k_rel"] = 0.002   # una copia que ya era más estricta que el 0,5 %
    cfg_v073["politica_f"] = {k: v for k, v in POLITICA_DEFECTO.items() if k not in ("importe_max_dia_pct", "perdida_semana_max_pct_trading",
                                                                                     "perdida_semana_max_pct_tactica", "perdida_semana_max_pct_largo_plazo")}
    cfg_v073["politica_f"]["importe_max_dia_eur"] = 12345.0   # un valor personalizado
    m = mg._v074({"cfg": copy.deepcopy(cfg_v073)})["cfg"]
    h.chk("MIG010_anade_las_claves_con_su_valor_de_partida", m["tope_anual_gasto_pct_capital"] == 0.5 and m["capital_referencia_eur"] is None
          and m["divisas_principales"] == ["USD", "GBP", "JPY", "CHF"] and m["politica_f"]["importe_max_dia_pct"] == 25.0
          and m["politica_f"]["perdida_semana_max_pct_tactica"] == 5.0 and m["version_config"] == "CFG-0.12.0", m)
    h.chk("MIG010_no_cambia_lo_que_ya_tenia", m["politica_f"]["importe_max_dia_eur"] == 12345.0 and m["tolerancia_tipo_k_rel"] == 0.002)
    h.chk("MIG010_la_tolerancia_principal_nunca_mas_laxa_que_la_general", m["tolerancia_tipo_k_rel_principales"] == 0.002)
    propia = mg._v074({"cfg": {**copy.deepcopy(cfg_v073), "version_config": "CFG-7.7.7"}})["cfg"]
    h.chk("MIG010_una_version_propia_no_se_pisa", propia["version_config"] == "CFG-7.7.7")
    viejo = (AQUI / "estados" / "estado_V0_52.json").read_text(encoding="ascii")
    r = mg.migrar(viejo, "2026-11-12T10:00:00+00:00", "Paso el estado guardado al código de V0.74")
    o2 = r.get("orquestador")
    antes = json.loads(viejo)["estado"]["cfg"]
    h.chk("MIG010_en_la_cadena_desde_un_estado_guardado", r["ok"] and "MIG-010" in r["migraciones"] and o2.integridad() == []
          and o2.cfg["tope_anual_gasto_pct_capital"] == 0.5 and o2.cfg["politica_f"]["importe_max_dia_pct"] == 25.0
          and o2.cfg["nivel_autonomia"] == antes["nivel_autonomia"] and o2.cfg["version_config"] == "CFG-0.12.0", r.get("motivo"))

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO TANDA 2 T-97:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
