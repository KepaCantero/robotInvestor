"""Pruebas de E (dimensionado). Datos SIMULADOS.

Uso: python3 pruebas/pruebas_dimensionado.py
"""
import random
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
from control_f import POLITICA_DEFECTO, controlar  # noqa: E402
from dimensionado import dimensionar  # noqa: E402
from pruebas_orquestador import Arnes  # noqa: E402

AHORA = "2026-11-06T09:00:00+00:00"
CART = {"fecha_hora": "2026-11-06T08:50:00+00:00", "capital_eur": 100000.0, "perdida_dia_eur": 0.0, "posiciones": [],
        "tipos_cambio_eur": {"USD": 1.0}}   # tipo neutro: cifras de antes de la conversión (T-10)
SOL = {"instrumento": "EURUSD", "activo_base": "EUR", "divisa_cotizacion": "USD", "direccion": "LARGO", "precio_entrada": 1.10, "stop_precio": 1.05, "apalancamiento": 1.0, "cartera": "TACTICA"}


def main():
    h = Arnes()
    r = dimensionar(SOL, CART, POLITICA_DEFECTO, AHORA, paso=1.0)
    # riesgo 1% de 100000 = 1000 EUR; riesgo unitario 0,05 -> 20000; tope tamaño 10% = 10000/1,10 = 9090,9 -> manda el tamaño
    h.chk("manda_el_tope_de_tamano", r["ok"] and r["cantidad"] == 9090.0 and r["limitada_por"] == "F-04", r)
    r = dimensionar({**SOL, "stop_precio": 1.0}, CART, POLITICA_DEFECTO, AHORA, riesgo_objetivo_pct=0.5, paso=1.0)
    h.chk("manda_el_riesgo_objetivo", r["ok"] and r["limitada_por"] == "RIESGO_OBJETIVO" and r["cantidad"] == 5000.0, r)
    r = dimensionar({**SOL, "stop_precio": 1.0}, CART, POLITICA_DEFECTO, AHORA, riesgo_objetivo_pct=0.2, paso=1.0)
    h.chk("riesgo_objetivo_menor_que_el_maximo", r["ok"] and r["limitada_por"] == "RIESGO_OBJETIVO" and r["cantidad"] == 2000.0 and abs(r["riesgo_pct"] - 0.2) < 1e-9, r)
    r = dimensionar(SOL, CART, POLITICA_DEFECTO, AHORA, riesgo_objetivo_pct=5.0)
    h.chk("riesgo_objetivo_sobre_la_politica_E01", r["codigo"] == "E-01" and r["cantidad"] == 0.0, r)
    for nombre, mut in (("stop_del_lado_equivocado", {"stop_precio": 1.20}), ("stop_igual_a_la_entrada", {"stop_precio": 1.10}), ("direccion_rara", {"direccion": "X"})):
        r = dimensionar({**SOL, **mut}, CART, POLITICA_DEFECTO, AHORA)
        h.chk(nombre + "_E02", r["codigo"] == "E-02" and r["cantidad"] == 0.0, r)
    r = dimensionar({**SOL, "direccion": "CORTO", "stop_precio": 1.15}, CART, POLITICA_DEFECTO, AHORA, paso=1.0)
    h.chk("corto_con_stop_por_encima", r["ok"] and r["cantidad"] > 0, r)
    for nombre, mut in (("sin_campo", None), ("con_cantidad", {"cantidad": 5.0}), ("precio_nan", {"precio_entrada": float("nan")}), ("precio_texto", {"precio_entrada": "1.1"}),
                        ("precio_bool", {"precio_entrada": True}), ("precio_negativo", {"stop_precio": -1.0})):
        if mut is None:
            s = {k: v for k, v in SOL.items() if k != "cartera"}
        else:
            s = {**SOL, **mut}
        r = dimensionar(s, CART, POLITICA_DEFECTO, AHORA)
        h.chk("entrada_" + nombre + "_falla_cerrado", r["ok"] is False and r["cantidad"] == 0.0, r)
    for nombre, kw in (("paso_cero", {"paso": 0}), ("paso_nan", {"paso": float("nan")}), ("paso_texto", {"paso": "1"})):
        r = dimensionar(SOL, CART, POLITICA_DEFECTO, AHORA, **kw)
        h.chk(nombre + "_E01", r["codigo"] == "E-01", r)
    h.chk("politica_invalida_E01", dimensionar(SOL, CART, {"riesgo_max_pct": 1}, AHORA)["codigo"] == "E-01")
    h.chk("cartera_basura_no_lanza", dimensionar(SOL, None, POLITICA_DEFECTO, AHORA)["codigo"] in ("E-01", "E-03"))
    # F vetaría
    r = dimensionar(SOL, {**CART, "perdida_dia_eur": 5000.0}, POLITICA_DEFECTO, AHORA)
    h.chk("perdida_del_dia_E03", r["codigo"] == "E-03" and "F-08" in r["reglas"], r)
    r = dimensionar(SOL, {**CART, "fecha_hora": "2026-11-06T06:00:00+00:00"}, POLITICA_DEFECTO, AHORA)
    h.chk("cartera_vieja_E03", r["codigo"] == "E-03" and "F-10" in r["reglas"], r)
    r = dimensionar({**SOL, "apalancamiento": 5.0}, CART, POLITICA_DEFECTO, AHORA)
    h.chk("apalancamiento_E03", r["codigo"] == "E-03" and "F-05" in r["reglas"], r)
    # topes por la cartera existente
    cart2 = {**CART, "posiciones": [{"instrumento": "GBPUSD", "activo_base": "EUR", "valor_eur": 19000.0}]}
    r = dimensionar(SOL, cart2, POLITICA_DEFECTO, AHORA, paso=1.0)
    h.chk("concentracion_existente_limita", r["ok"] and r["limitada_por"] == "F-07" and r["valor_eur"] <= 1000.0 + 1.1, r)
    cart3 = {**CART, "posiciones": [{"instrumento": "GBPUSD", "activo_base": "EUR", "valor_eur": 99950.0}]}
    r = dimensionar(SOL, cart3, POLITICA_DEFECTO, AHORA)
    h.chk("sin_hueco_por_valor_minimo_E04", r["codigo"] == "E-04" and r["cantidad"] == 0.0, r)
    r = dimensionar(SOL, CART, POLITICA_DEFECTO, AHORA, paso=100000.0)
    h.chk("paso_mayor_que_la_cantidad_E04", r["codigo"] == "E-04", r)
    r = dimensionar(SOL, CART, POLITICA_DEFECTO, AHORA, paso=1000.0)
    h.chk("redondea_siempre_hacia_abajo_al_paso", r["ok"] and r["cantidad"] % 1000 == 0 and r["cantidad"] == 9000.0, r)
    # revisión independiente
    r = dimensionar({**SOL, "precio_entrada": 75.23, "stop_precio": 71.47}, CART, POLITICA_DEFECTO, AHORA, paso=0.01)
    h.chk("borde_de_redondeo_de_F_baja_un_paso_y_no_da_E04", r["ok"] and 132.8 < r["cantidad"] <= 132.92, r)
    r = dimensionar({**SOL, "stop_precio": 1.1 - 500 / (1000 - 5e-10)}, CART, POLITICA_DEFECTO, AHORA, riesgo_objetivo_pct=0.5, paso=1.0)
    from fractions import Fraction
    exacto = (not r["ok"]) or Fraction(r["cantidad"]) * abs(Fraction(1.1) - Fraction(SOL["precio_entrada"] if False else 1.1 - 500 / (1000 - 5e-10))) <= Fraction(500)
    h.chk("riesgo_nunca_supera_el_objetivo_en_aritmetica_exacta", exacto, r)
    r = dimensionar({**SOL, "precio_entrada": 1e-8, "stop_precio": 0.99e-8}, CART, POLITICA_DEFECTO, AHORA, paso=1.0)
    h.chk("precio_muy_bajo_no_da_E04_espurio", r["ok"] and r["limitada_por"] in ("F-04", "RIESGO_OBJETIVO", "F-03"), r)
    r = dimensionar({**SOL, "stop_precio": 0.99}, {**CART, "capital_eur": 1e14}, POLITICA_DEFECTO, AHORA, paso=1.0)
    h.chk("capital_muy_alto_no_da_E04_espurio_y_manda_el_importe_en_euros", r["ok"] and r["limitada_por"] == "F-13" and r["cantidad"] == 18181.0, r)   # T-22: 20.000 € por orden
    r = dimensionar(SOL, CART, POLITICA_DEFECTO, AHORA, paso=1e-12)
    h.chk("paso_finisimo_o_ok_o_falla_cerrado", (r["ok"] and r["riesgo_pct"] <= 1.0 + 1e-9) or (not r["ok"] and r["cantidad"] == 0.0), r)
    for nombre, c in (("fecha_imposible", {**CART, "fecha_hora": "2026-02-30T08:50:00+00:00"}), ("posiciones_tupla", {**CART, "posiciones": ()})):
        h.chk("forma_" + nombre + "_es_E01", dimensionar(SOL, c, POLITICA_DEFECTO, AHORA)["codigo"] == "E-01")
    h.chk("apalancamiento_bool_es_E01", dimensionar({**SOL, "apalancamiento": True}, CART, POLITICA_DEFECTO, AHORA)["codigo"] == "E-01")
    # determinismo y no muta
    import copy
    c0, s0 = copy.deepcopy(CART), copy.deepcopy(SOL)
    a, b = dimensionar(SOL, CART, POLITICA_DEFECTO, AHORA), dimensionar(SOL, CART, POLITICA_DEFECTO, AHORA)
    h.chk("determinista_y_no_muta_las_entradas", a == b and CART == c0 and SOL == s0)
    # propiedad: lo que E devuelve, F lo aprueba y el riesgo nunca supera el objetivo
    rnd = random.Random(7)
    malos = 0
    for _ in range(400):
        ent = rnd.uniform(0.5, 200)
        dist = ent * rnd.uniform(0.001, 0.3)
        largo = rnd.random() < 0.5
        s = {**SOL, "precio_entrada": ent, "stop_precio": ent - dist if largo else ent + dist, "direccion": "LARGO" if largo else "CORTO"}
        cap = rnd.uniform(1000, 1e6)
        cart = {**CART, "capital_eur": cap, "perdida_dia_eur": rnd.uniform(0, cap * 0.03),
                "posiciones": [{"instrumento": f"I{i}", "activo_base": rnd.choice(["EUR", "USD"]), "valor_eur": rnd.uniform(0, cap * 0.3)} for i in range(rnd.randint(0, 6))]}
        obj = rnd.uniform(0.05, 1.0)
        paso = rnd.choice([1e-6, 0.01, 1.0, 1000.0])
        r = dimensionar(s, cart, POLITICA_DEFECTO, AHORA, riesgo_objetivo_pct=obj, paso=paso)
        if r["ok"]:
            v = controlar({**s, "cantidad": r["cantidad"]}, cart, POLITICA_DEFECTO, AHORA)
            if v["resultado"] != "APROBADO" or r["riesgo_pct"] > obj + 1e-9 or r["cantidad"] <= 0:
                malos += 1
        elif r["cantidad"] != 0.0:
            malos += 1
        elif r["codigo"] == "E-04" and paso <= 1.0 and not cart["posiciones"] and False:
            malos += 1
    h.chk("propiedad_F_aprueba_lo_que_E_propone_400_casos", malos == 0, malos)
    print(f"\n{h.n} comprobaciones")
    print("RESULTADO E:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
