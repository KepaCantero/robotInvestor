# -*- coding: utf-8 -*-
"""Pruebas unitarias de HT-03 Forex (puntuaciones con la A FX, RK, elegibilidad y top-3 por segmento)."""
import json
import os
import sys
import tempfile
import unittest
from fractions import Fraction

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, RAIZ)

import ht03_puntuaciones as h  # noqa: E402

P = h.PARAMETROS_POR_DEFECTO
PUERTAS = {g: True for g in P["puertas_obligatorias"]}


def todas(nombre, v):
    return {k: v for k in P["pesos"][nombre]}


def dims(t=70, e=70, a=70, m=50):
    return {"T": "NA" if t == "NA" else todas("T", t), "E": todas("E", e), "M": todas("M", m),
            "A": todas("A", a), "P": {"novedad": 60, "incertidumbre_reducible": 60, "coste_eficiencia": 60}}


def opcion(oid="OPP-FX-1", segmento="G10N", **kw):
    o = {"opp_id": oid, "segmento": segmento, "dimensiones": dims(), "puertas": dict(PUERTAS), "objeciones_fuertes_abiertas": 0}
    o.update(kw)
    return o


def evaluada(oid, rk, e=70, cluster="c1", vigente=False, cola=None, elegible=True, expo=None):
    return {"opp_id": oid, "elegible": elegible, "vigente": vigente, "cluster": cluster, "riesgo_cola": cola,
            "exposiciones": [{"divisa": d, "lado": l} for d, l in (expo or [])],
            "puntuaciones": {"RK": rk, "E": e}, "motivos_no_elegible": [] if elegible else [{"codigo": "E_BAJO", "detalle": "E=50 < 60", "falta": 10}]}


class TestRedondeo(unittest.TestCase):
    def test_multiplo_de_5_empate_abajo(self):
        r = h.redondear_abajo_en_empate
        self.assertEqual(r(Fraction(725, 10), 5), 70)
        self.assertEqual(r(Fraction(726, 10), 5), 75)
        self.assertEqual(r(Fraction(775, 10), 5), 75)
        self.assertEqual(r(Fraction(674, 10), 5), 65)
        self.assertEqual(r(Fraction(70), 5), 70)
        self.assertEqual(r(Fraction(7175, 100), 1), 72)
        self.assertEqual(r(Fraction(715, 10), 1), 71)


class TestPuntuacion(unittest.TestCase):
    def test_media_ponderada(self):
        d = {"calidad_raices": 80, "cobertura_variables": 80, "calidad_metodologica": 70, "trazabilidad": 80,
             "actualidad": 70, "discrepancias_resueltas": 70, "objeciones_respondidas": 70}
        r = h.calcular_puntuacion("E", d, P["pesos"]["E"])
        self.assertEqual(r["media_exacta"], 75.5)
        self.assertEqual(r["total"], 75)

    def test_na_redistribuye(self):
        d = todas("A", 60)
        d["asimetria"] = "NA"   # peso 30 fuera: el resto (70) se reescala
        d["valoracion"] = 100   # 20/70 del peso efectivo
        r = h.calcular_puntuacion("A", d, P["pesos"]["A"])
        esperado = (20 * 100 + 50 * 60) / 70  # 71,43
        self.assertAlmostEqual(r["media_exacta"], round(esperado, 4))
        self.assertEqual(r["total"], 70)
        self.assertEqual(r["desglose"]["asimetria"]["peso_efectivo"], 0)
        self.assertAlmostEqual(r["desglose"]["valoracion"]["peso_efectivo"], round(20 / 70 * 100, 4))

    def test_ne_puntua_cero(self):
        d = todas("A", 80)
        d["carry"] = "NE"   # peso 15 (A FX): 85·80/100 = 68
        r = h.calcular_puntuacion("A", d, P["pesos"]["A"])
        self.assertEqual(r["media_exacta"], 68.0)
        self.assertEqual(r["total"], 70)

    def test_maximo_dos_na_ne(self):
        d = todas("A", 80)
        d.update({"momento_posicionamiento": "NE", "catalizadores": "NA", "convertibilidad": "NA"})
        with self.assertRaises(h.ErrorEntrada):
            h.calcular_puntuacion("A", d, P["pesos"]["A"])

    def test_multiplo_de_10_y_rango(self):
        d = todas("A", 80)
        d["carry"] = 75
        with self.assertRaises(h.ErrorEntrada):
            h.calcular_puntuacion("A", d, P["pesos"]["A"])
        d["carry"] = 110
        with self.assertRaises(h.ErrorEntrada):
            h.calcular_puntuacion("A", d, P["pesos"]["A"])

    def test_dimensiones_faltantes_o_desconocidas(self):
        d = todas("A", 80)
        del d["carry"]
        with self.assertRaises(h.ErrorEntrada):
            h.calcular_puntuacion("A", d, P["pesos"]["A"])
        d = todas("A", 80)
        d["inventada"] = 10
        with self.assertRaises(h.ErrorEntrada):
            h.calcular_puntuacion("A", d, P["pesos"]["A"])

    def test_saturacion_narrativa(self):
        o = opcion(saturacion_narrativa=True)
        o["dimensiones"]["A"]["valoracion"] = 90
        r = h.evaluar_opcion(o)
        self.assertEqual(r["desglose"]["A"]["desglose"]["valoracion"]["valor"], 40)
        self.assertTrue(any("saturación" in n for n in r["desglose"]["A"]["notas"]))


class TestOpcion(unittest.TestCase):
    def test_rk_empate_hacia_abajo(self):
        # 0,45·70 + 0,35·80 + 0,20·70 = 73,5 → empate: hacia abajo
        r = h.evaluar_opcion(opcion(dimensiones=dims(70, 80, 70)))
        self.assertEqual(r["desglose"]["RK"]["exacto"], 73.5)
        self.assertEqual(r["puntuaciones"]["RK"], 73)

    def test_p_usa_t_total(self):
        r = h.evaluar_opcion(opcion(dimensiones=dims(80, 70, 70)))
        self.assertEqual(r["desglose"]["P"]["desglose"]["T"]["valor"], 80)
        self.assertEqual(r["puntuaciones"]["P"], 70)  # (40·80 + 60·60)/100 = 68 → 70

    def test_t_na_tactica(self):
        r = h.evaluar_opcion(opcion(dimensiones=dims("NA", 70, 60)))
        self.assertEqual(r["puntuaciones"]["T"], "NA")
        self.assertEqual(r["puntuaciones"]["RK"], 64)  # (0,45·60 + 0,35·70)/0,8 = 64,375
        self.assertFalse(r["elegible"])
        self.assertIn("A_BAJO", [m["codigo"] for m in r["motivos_no_elegible"]])
        r = h.evaluar_opcion(opcion(dimensiones=dims("NA", 70, 80)))
        self.assertTrue(r["elegible"], r["motivos_no_elegible"])

    def test_umbrales(self):
        r = h.evaluar_opcion(opcion(dimensiones=dims(40, 50, 40)))
        codigos = {m["codigo"] for m in r["motivos_no_elegible"]}
        self.assertTrue({"E_BAJO", "A_BAJO", "T_BAJO"} <= codigos)

    def test_banda_marginal_sin_y_con_segunda_pasada(self):
        r = h.evaluar_opcion(opcion(dimensiones=dims(70, 60, 70)))
        self.assertFalse(r["elegible"])
        self.assertIn("PS8_BANDA_MARGINAL", [m["codigo"] for m in r["motivos_no_elegible"]])
        self.assertEqual(r["banda_marginal"][0]["umbrales"][0]["distancia"], 0)
        o = opcion(dimensiones=dims(70, 60, 70), segunda_pasada={"E": todas("E", 60)})
        r = h.evaluar_opcion(o)
        self.assertTrue(r["elegible"], r["motivos_no_elegible"])
        o = opcion(dimensiones=dims(70, 60, 70), segunda_pasada={"E": todas("E", 50)})
        r = h.evaluar_opcion(o)
        self.assertEqual(r["puntuaciones"]["E"], 50)  # se usa el menor
        self.assertIn("E_BAJO", [m["codigo"] for m in r["motivos_no_elegible"]])

    def test_segunda_pasada_mayor_no_sube(self):
        o = opcion(dimensiones=dims(70, 60, 70), segunda_pasada={"E": todas("E", 70)})
        r = h.evaluar_opcion(o)
        self.assertEqual(r["puntuaciones"]["E"], 60)

    def test_cambio_material(self):
        r = h.evaluar_opcion(opcion(anterior={"A": 85, "E": 75}))
        self.assertEqual([x["puntuacion"] for x in r["exige_justificacion"]], ["A"])

    def test_puertas_y_objeciones(self):
        o = opcion()
        o["puertas"]["PS3"] = False
        del o["puertas"]["G4"]
        o["objeciones_fuertes_abiertas"] = 1
        r = h.evaluar_opcion(o)
        codigos = [m["codigo"] for m in r["motivos_no_elegible"]]
        self.assertIn("PUERTA_NO_SUPERADA", codigos)
        self.assertIn("PUERTA_SIN_DATO", codigos)
        self.assertIn("OBJECION_FUERTE", codigos)

    def test_error_no_rompe_lote(self):
        o = opcion()
        o["dimensiones"]["E"]["actualidad"] = 55
        res = h.procesar({"opciones": [o, opcion("OPP-FX-2")]})
        self.assertFalse(res["opciones"][0]["elegible"])
        self.assertTrue(res["opciones"][1]["elegible"])


class TestSeleccion(unittest.TestCase):
    def test_orden_y_empates(self):
        lst = [evaluada("A", 70, e=60), evaluada("B", 69, e=80), evaluada("C", 75, e=60), evaluada("D", 69, e=80, cola=1)]
        orden = [o["opp_id"] for o in h.ordenar(lst)]
        # C primero (75); entre A(70,E60), B(69,E80), D(69,E80,cola 1): dentro de ±2 manda E y luego menor cola
        self.assertEqual(orden, ["C", "D", "B", "A"])

    def test_empate_no_aplica_fuera_de_2(self):
        orden = [o["opp_id"] for o in h.ordenar([evaluada("A", 73, e=60), evaluada("B", 70, e=90)])]
        self.assertEqual(orden, ["A", "B"])

    def test_diversidad_cede_tercera(self):
        lst = [evaluada("A", 80, cluster="x"), evaluada("B", 78, cluster="x"), evaluada("C", 76, cluster="x"),
               evaluada("D", 67, cluster="y")]
        s = h.seleccionar_top3(lst)
        self.assertEqual([t["opp_id"] for t in s["top3"]], ["A", "B", "D"])
        self.assertTrue(s["diversidad"]["aplicada"])
        self.assertEqual(s["diversidad"]["sale"], ["C"])
        self.assertEqual(s["diversidad"]["entra"], ["D"])
        self.assertEqual([d["decision"] for d in s["decisiones"] if d["opp_id"] == "C"], ["CEDE_POR_DIVERSIDAD"])

    def test_diversidad_maximo_dos_por_cluster_sin_alternativa(self):
        # Sin alternativa de otro clúster a ≤ 10 puntos, el hueco queda vacío: nunca tres del mismo clúster
        lst = [evaluada("A", 80, cluster="x"), evaluada("B", 78, cluster="x"), evaluada("C", 76, cluster="x"),
               evaluada("D", 65, cluster="y")]
        s = h.seleccionar_top3(lst)
        self.assertEqual([t["opp_id"] for t in s["top3"]], ["A", "B"])
        self.assertTrue(s["diversidad"]["hueco_vacio"])
        self.assertIn("diversidad", s["menos_de_tres_motivo"]["texto"])

    def test_diversidad_misma_divisa_misma_direccion(self):
        # Tres opciones con el yen largo (en clústeres distintos): la tercera cede a una sin JPY LARGO
        lst = [evaluada("A", 80, cluster="a", expo=[("USD", "CORTO"), ("JPY", "LARGO")]),
               evaluada("B", 78, cluster="b", expo=[("EUR", "CORTO"), ("JPY", "LARGO")]),
               evaluada("C", 77, cluster="c", expo=[("AUD", "CORTO"), ("JPY", "LARGO")]),
               evaluada("D", 70, cluster="d", expo=[("EUR", "LARGO"), ("GBP", "CORTO")])]
        s = h.seleccionar_top3(lst)
        self.assertEqual([t["opp_id"] for t in s["top3"]], ["A", "B", "D"])
        self.assertIn("JPY LARGO", s["diversidad"]["motivo"])
        # La misma divisa con dirección opuesta sí cabe
        lst[2] = evaluada("C", 77, cluster="c", expo=[("JPY", "CORTO"), ("MXN", "LARGO")])
        self.assertEqual([t["opp_id"] for t in h.seleccionar_top3(lst)["top3"]], ["A", "B", "C"])

    def test_exposiciones_desde_par_y_composicion(self):
        self.assertEqual(h.exposiciones_de({"par": "USD/JPY", "direccion": "BAJISTA_BASE"}),
                         [{"divisa": "USD", "lado": "CORTO"}, {"divisa": "JPY", "lado": "LARGO"}])
        self.assertEqual(h.exposiciones_de({"par": "EUR/USD", "direccion": "ALCISTA_BASE"}),
                         [{"divisa": "EUR", "lado": "LARGO"}, {"divisa": "USD", "lado": "CORTO"}])
        comp = [{"divisa": "BRL", "peso": 0.5, "lado": "LARGO"}, {"divisa": "MXN", "peso": 0.5, "lado": "LARGO"},
                {"divisa": "USD", "peso": 1.0, "lado": "CORTO"}]
        self.assertEqual(len(h.exposiciones_de({"composicion": comp, "par": "USD/BRL", "direccion": "ALCISTA_BASE"})), 3)
        self.assertEqual(h.exposiciones_de({"par": "EUR/USD", "direccion": None, "vista_volatilidad": {"sentido": "ALZA", "plazo": "1M"}}), [])

    def test_continuidad_mantiene(self):
        lst = [evaluada("N1", 80, cluster="a"), evaluada("N2", 78, cluster="b"), evaluada("N3", 75, cluster="c"),
               evaluada("V", 71, cluster="d", vigente=True)]
        s = h.seleccionar_top3(lst)
        ids = [t["opp_id"] for t in s["top3"]]
        self.assertIn("V", ids)
        self.assertNotIn("N3", ids)
        self.assertTrue(any("Continuidad" in t["motivo"] for t in s["top3"] if t["opp_id"] == "V"))

    def test_continuidad_sustituye(self):
        lst = [evaluada("N1", 80, cluster="a"), evaluada("N2", 78, cluster="b"), evaluada("N3", 75, cluster="c"),
               evaluada("V", 69, cluster="d", vigente=True)]
        s = h.seleccionar_top3(lst)
        self.assertNotIn("V", [t["opp_id"] for t in s["top3"]])
        d = [x for x in s["decisiones"] if x["opp_id"] == "V"][0]
        self.assertEqual(d["decision"], "SUSTITUIDA")

    def test_vigente_no_elegible(self):
        s = h.seleccionar_top3([evaluada("V", 80, vigente=True, elegible=False)])
        self.assertEqual(s["decisiones"][0]["decision"], "VIGENTE_NO_ELEGIBLE")

    def test_menos_de_tres(self):
        s = h.seleccionar_top3([evaluada("A", 80), evaluada("B", 60, elegible=False)], candidatas_analizadas=9)
        self.assertEqual(len(s["top3"]), 1)
        m = s["menos_de_tres_motivo"]
        self.assertEqual((m["candidatas_analizadas"], m["elegibles"]), (9, 1))
        self.assertTrue(m["no_llegaron"][0]["que_tendria_que_ocurrir"])

    def test_cero_opciones(self):
        s = h.seleccionar_top3([], candidatas_analizadas=4)
        self.assertEqual(s["top3"], [])
        self.assertIn("0 opción", s["menos_de_tres_motivo"]["texto"])


class TestForex(unittest.TestCase):
    def test_pesos_de_a_fx(self):
        self.assertEqual(P["pesos"]["A"], {"asimetria": 30, "valoracion": 20, "carry": 15, "catalizadores": 15,
                                           "momento_posicionamiento": 10, "convertibilidad": 10})
        self.assertEqual(sum(P["pesos"]["A"].values()), 100)
        self.assertEqual(P["pesos_rk"], {"A": 0.45, "E": 0.35, "T": 0.20})
        self.assertEqual((P["max_opciones_por_segmento"], P["max_por_cluster"], P["max_divisa_misma_direccion"]), (3, 2, 2))

    def test_dimensiones_del_bloque_general_rechazadas(self):
        for retirada, equivalente in (("invertibilidad", "convertibilidad"), ("momento", "momento_posicionamiento"),
                                      ("costes_implementacion", "convertibilidad")):
            d = todas("A", 70)
            d[retirada] = 70
            with self.assertRaisesRegex(h.ErrorEntrada, equivalente):
                h.calcular_puntuacion("A", d, P["pesos"]["A"])

    def test_carry_pondera_15_y_convertibilidad_10(self):
        d = todas("A", 60)
        d["carry"] = 100        # 0,85·60 + 0,15·100 = 66
        self.assertEqual(h.calcular_puntuacion("A", d, P["pesos"]["A"])["media_exacta"], 66.0)
        d = todas("A", 60)
        d["convertibilidad"] = 100   # 0,90·60 + 0,10·100 = 64
        self.assertEqual(h.calcular_puntuacion("A", d, P["pesos"]["A"])["media_exacta"], 64.0)

    def test_seis_segmentos(self):
        self.assertEqual(h.SEGMENTOS, ("G10N", "G10M", "EMAS", "EMLA", "EMEA", "ESTR"))
        ops = [opcion(f"OPP-FX-{t}", t) for t in reversed(h.SEGMENTOS)]
        res = h.procesar({"opciones": ops})
        self.assertEqual(list(res["seleccion"]), list(h.SEGMENTOS))
        self.assertTrue(all(len(v["top3"]) == 1 for v in res["seleccion"].values()))
        self.assertEqual(res["opciones"][0]["segmento"], "ESTR")
        # alias «clase» aceptado por compatibilidad
        o = opcion("OPP-FX-X")
        del o["segmento"]
        o["clase"] = "EMLA"
        self.assertEqual(list(h.procesar({"opciones": [o]})["seleccion"]), ["EMLA"])

    def test_segmento_desconocido_o_incoherente(self):
        with self.assertRaisesRegex(h.ErrorEntrada, "desconocido"):
            h.procesar({"opciones": [opcion(segmento="RV")]})
        with self.assertRaisesRegex(h.ErrorEntrada, "distinto"):
            h.procesar({"opciones": [opcion(segmento="G10N", clase="EMAS")]})
        with self.assertRaisesRegex(h.ErrorEntrada, "desconocidos"):
            h.procesar({"opciones": [opcion()], "candidatas_analizadas": {"DIV": 3}})

    def test_segmentos_activos_configurables(self):
        with self.assertRaises(h.ErrorEntrada):
            h.procesar({"parametros": {"segmentos": ["G10N", "G10M"]}, "opciones": [opcion(segmento="ESTR")]})


class TestProcesoYCLI(unittest.TestCase):
    def test_parametros_personalizados(self):
        res = h.procesar({"parametros": {"umbrales": {"E": 75}}, "opciones": [opcion()]})
        self.assertFalse(res["opciones"][0]["elegible"])
        self.assertEqual(res["parametros"]["umbrales"]["A"], 55)

    def test_duplicados(self):
        with self.assertRaises(h.ErrorEntrada):
            h.procesar({"opciones": [opcion(), opcion()]})

    def test_cli_ejemplo(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "o.json")
            self.assertEqual(h.main([os.path.join(RAIZ, "ejemplos", "ht03_entrada_ejemplo.json"), "--salida", out]), 0)
            with open(out, encoding="utf-8") as fh:
                res = json.load(fh)
        g10n = res["seleccion"]["G10N"]
        # 0008 (JPY largo por tercera vez y tercera del clúster «yen_refugio») cede su puesto a EUR/GBP (RK a ≤ 10)
        self.assertEqual([t["opp_id"] for t in g10n["top3"]], ["OPP-FX-2026-0007", "OPP-FX-2026-0009", "OPP-FX-2026-0010"])
        dec = {d["opp_id"]: d["decision"] for d in g10n["decisiones"]}
        self.assertEqual(dec["OPP-FX-2026-0008"], "CEDE_POR_DIVERSIDAD")
        self.assertEqual(dec["OPP-FX-2026-0011"], "SUSTITUIDA")       # vigente a más de 10 puntos de la mejor nueva
        self.assertEqual([t["opp_id"] for t in res["seleccion"]["EMLA"]["top3"]], ["OPP-FX-2026-0021"])   # táctica T = NA
        self.assertIsNotNone(res["seleccion"]["EMLA"]["menos_de_tres_motivo"])
        # Orden canónico de la tabla 2.6 y segmento sin opciones con motivo
        self.assertEqual(list(res["seleccion"]), ["G10N", "EMAS", "EMLA", "ESTR"])
        self.assertEqual(res["seleccion"]["EMAS"]["top3"], [])
        self.assertEqual(res["seleccion"]["EMAS"]["menos_de_tres_motivo"]["candidatas_analizadas"], 5)
        self.assertEqual([t["opp_id"] for t in res["seleccion"]["ESTR"]["top3"]], ["OPP-FX-2026-0030"])

    def test_determinismo(self):
        ruta = os.path.join(RAIZ, "ejemplos", "ht03_entrada_ejemplo.json")
        with open(ruta, encoding="utf-8") as fh:
            entrada = json.load(fh)
        self.assertEqual(json.dumps(h.procesar(entrada), sort_keys=True), json.dumps(h.procesar(entrada), sort_keys=True))


if __name__ == "__main__":
    unittest.main()
