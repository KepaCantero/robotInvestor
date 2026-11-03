# -*- coding: utf-8 -*-
"""Pruebas de HT-03 del Bloque B (estrategia, A/E/C, veredictos, S, selección y diversidad)."""
import json
import os
import sys
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, RAIZ)

import ht03_puntuaciones as h  # noqa: E402

EJEMPLO = os.path.join(os.path.dirname(RAIZ), "06_Plantillas_entregables",
                       "Ejemplo - Paquete de análisis de mercado - Bloque B - V2.0.json")


class TestMatriz(unittest.TestCase):
    def test_columnas_suman_100(self):
        for obj, col in h.MATRIZ.items():
            self.assertEqual(sum(col.values()), 100, obj)

    def test_playbooks_suman_100(self):
        for t, pb in h.PLAYBOOKS.items():
            self.assertEqual(sum(v for v in pb["pesos"].values() if v is not None), 100, t)

    def test_regla_de_profundidad(self):
        for peso, p in ((12, "P3"), (11, "P2"), (7, "P2"), (6, "P1"), (4, "P1"), (3, "P0"), (0, "P0")):
            self.assertEqual(h.profundidad_por_peso(peso), p)

    def test_matriz_inicial_coincide_con_profundidad_de_8_3_1(self):
        # En H3 el único modulador distinto de 1 es D9 × 1,1: D9 gana un punto y el resto apenas cambia
        e = h.estrategia("SECTOR", "H3")
        self.assertEqual(e["pesos_efectivos"]["D9"], 13)
        self.assertLessEqual(sum(abs(e["pesos_efectivos"][d] - h.MATRIZ["SECTOR"][d]) for d in h.DIMENSIONES), 2)
        self.assertEqual(e["profundidad"]["D4"], "P3")
        self.assertEqual(e["profundidad"]["D1"], "P1")

    def test_moduladores_y_minimos(self):
        e = h.estrategia("ESTRATEGIA_FACTOR", "H1", ["DIV"])
        self.assertEqual(sum(e["pesos_efectivos"].values()), 100)
        self.assertIn(e["profundidad"]["D9"], ("P2", "P3"))
        self.assertNotEqual(e["profundidad"]["D12"], "P0")
        self.assertGreater(e["pesos_efectivos"]["D10"], h.MATRIZ["ESTRATEGIA_FACTOR"]["D10"])

    def test_media_geometrica_de_varios_tipos(self):
        uno = h.estrategia("SECTOR", "H3", ["RV"])["pesos_efectivos"]
        dos = h.estrategia("SECTOR", "H3", ["RV", "RF"])["pesos_efectivos"]
        self.assertNotEqual(uno, dos)

    def test_n1_y_n3(self):
        n1 = h.estrategia("TEMATICA", "H3", nivel="N1")
        self.assertTrue(all(p != "P0" for p in n1["profundidad"].values()))
        self.assertEqual(n1["profundidad"]["D9"], "P2")
        self.assertEqual(n1["profundidad"]["D12"], "P1")     # TEMATICA H3: D12 era P1 (A.2)
        self.assertEqual(h.estrategia("ESTRATEGIA_FACTOR", "H3", nivel="N1")["profundidad"]["D12"], "P2")
        self.assertTrue(all(v["codigo"] == "L" for k, v in n1["activacion"].items() if v["activo"] and k != "AG-B24"))
        self.assertTrue(n1["activacion"]["AG-B24"]["activo"])   # V2.1: excepción declarada de AG-B24 en las celdas A
        n3 = h.estrategia("TEMATICA", "H3", nivel="N3")
        self.assertTrue(all(n3["profundidad"][d] == "P3" for d, w in n3["pesos_efectivos"].items() if w >= 9))

    def test_desviacion_recortada(self):
        e = h.estrategia("SECTOR", "H3", desviaciones={"D5": 9})
        self.assertTrue(e["avisos"])
        self.assertEqual(e["desviaciones"][0]["puntos"], 5)
        self.assertEqual(sum(e["pesos_efectivos"].values()), 100)

    def test_condicional(self):
        e = h.estrategia("CADENA_DE_VALOR", "H4", ["RV"])
        self.assertFalse(e["activacion"]["AG-B10"]["activo"])   # D10 con peso ≤ 4
        self.assertEqual(e["activacion"]["AG-B03"]["codigo"], "L")
        s = h.estrategia("SEGMENTO_DE_CLASE", "H3", ["MP"], segmento_tipo="MP")
        self.assertEqual(s["activacion"]["AG-B05"]["codigo"], "L")


class TestPuntuacionesAmbito(unittest.TestCase):
    A = {"asimetria": 70, "valoracion_expectativas": 50, "calidad_crecimiento": 80, "ventaja_estructural": 80,
         "catalizadores": 70, "momento_flujos": 70, "riesgos": 50}

    def test_A_redondeo_a_5(self):
        r = h.calcular_A(self.A)
        self.assertEqual(r["exacto"], 66.5)
        self.assertEqual(r["total"], 65)

    def test_empate_hacia_abajo(self):
        self.assertEqual(h.redondear(67.5, 5), 65)
        self.assertEqual(h.redondear(71.5, 1), 71)
        self.assertEqual(h.redondear(71.51, 1), 72)

    def test_na_redistribuye_ne_cero(self):
        a = dict(self.A, catalizadores="NA")
        b = dict(self.A, catalizadores="NE")
        self.assertGreater(h.calcular_A(a)["exacto"], h.calcular_A(b)["exacto"])

    def test_mas_de_dos_na(self):
        a = dict(self.A, catalizadores="NA", riesgos="NE", momento_flujos="NA")
        self.assertFalse(h.calcular_A(a)["calculable"])

    def test_multiplos_de_10(self):
        with self.assertRaises(h.ErrorEntrada):
            h.calcular_A(dict(self.A, asimetria=72))

    def test_saturacion(self):
        a = dict(self.A, valoracion_expectativas=80)
        r = h.calcular_A(a, saturacion_narrativa=True)
        self.assertTrue(r["tope_saturacion_aplicado"])
        self.assertEqual(r["componentes"]["valoracion_expectativas"], 40)

    def test_RF_y_C(self):
        self.assertEqual(h.calcular_RF("robusta", 1), 90)
        self.assertEqual(h.calcular_RF("fragil", 6), 0)
        self.assertEqual(h.calcular_RF("refutada"), 0)
        c = h.calcular_C(65, 70, 90, 65)
        self.assertEqual(c["C"], 73)
        tope = h.calcular_C(100, 50, 100, 100)
        self.assertEqual(tope["C"], 60)
        self.assertTrue(tope["tope_aplicado"])
        sin_re = h.calcular_C(60, 60, 50, None)      # N1 sin RE: peso redistribuido (A.2)
        self.assertEqual(sin_re["C"], 57)


class TestVeredicto(unittest.TestCase):
    OK = {f"PA{i}": "OK" for i in range(1, 9)}

    def test_umbral(self):
        self.assertEqual(h.veredicto_ambito_provisional(70, 70, 70, self.OK)["veredicto"], "INVERTIR")
        self.assertEqual(h.veredicto_ambito_provisional(62, 62, 60, self.OK)["veredicto"], "INVERTIR_ESCALONADO")
        self.assertEqual(h.veredicto_ambito_provisional(62, 55, 60, self.OK)["veredicto"], "VIGILAR")
        self.assertEqual(h.veredicto_ambito_provisional(45, 80, 80, self.OK)["veredicto"], "DESCARTAR")

    def test_escalonado_por_flag(self):
        v = h.veredicto_ambito_provisional(70, 70, 70, self.OK, {"valoracion_parcialmente_descontada": True})
        self.assertEqual(v["veredicto"], "INVERTIR_ESCALONADO")

    def test_puertas(self):
        p = dict(self.OK, PA3="BLOQUEA")
        self.assertEqual(h.veredicto_ambito_provisional(80, 80, 80, p)["veredicto"], "VIGILAR")
        self.assertEqual(h.veredicto_ambito_provisional(80, 80, 80, self.OK, {"tesis_refutada": True})["veredicto"], "DESCARTAR")
        self.assertEqual(h.veredicto_ambito_provisional(80, 80, 80, self.OK, {"integridad": True})["veredicto"], "DESCARTAR")

    def test_relevancia_y_paso(self):
        self.assertEqual(h.relevancia_decisional("INVERTIR", 70, 72, 4, "H3")[0], "ALTA")
        self.assertEqual(h.relevancia_decisional("INVERTIR", 70, 72, 3, "H3", tipos_prioritarios=["CRI"])[0], "ALTA")
        self.assertEqual(h.relevancia_decisional("VIGILAR", 80, 60, 2, "H3")[0], "ALTA")
        self.assertEqual(h.relevancia_decisional("INVERTIR_ESCALONADO", 65, 70, 3, "H4")[0], "MEDIA")
        self.assertEqual(h.relevancia_decisional("VIGILAR", 55, 70, 2, "H3")[0], "BAJA")
        self.assertEqual(h.relevancia_decisional("VIGILAR", 55, 70, 2, "H3", disparador_cercano=True)[0], "MEDIA")
        self.assertEqual(h.siguiente_paso("INVERTIR", 2), "ENVIAR_CANDIDATOS_A_C")
        self.assertEqual(h.siguiente_paso("VIGILAR", 0, "NO_CONCLUYENTE"), "PROFUNDIZAR_EN_B")
        self.assertEqual(h.siguiente_paso("DESCARTAR", 0), "DESCARTAR")


def _cand(i, S, **kw):
    c = {"cand_id": f"CAND-B-2026-{i:04d}", "S": S, "ic90_S": [S - 6, S + 6], "ic90_rango": [i, i], "pureza": 0.6}
    c.update(kw)
    return c


class TestSeleccion(unittest.TestCase):
    def test_percentiles_y_winsor(self):
        p = h.percentiles_winsorizados({"a": 1, "b": 2, "c": 3, "d": 1000})
        self.assertEqual(p["a"], 0.0)
        self.assertEqual(p["d"], 100.0)
        inv = h.percentiles_winsorizados({"a": 1, "b": 2, "c": None}, inversa=True)
        self.assertEqual(inv["a"], 100.0)
        self.assertIsNone(inv["c"])

    def test_normalizar_y_S(self):
        filas = [{"cand_id": "X", "pureza": 0.9, "roic": 0.2, "volumen_medio_meur": 50, "momento_12_1": 0.3},
                 {"cand_id": "Y", "pureza": 0.3, "roic": 0.1, "volumen_medio_meur": 5, "momento_12_1": -0.1}]
        comp = h.normalizar_universo(filas, "RV")
        self.assertEqual(comp["X"]["CO"], "NA")
        self.assertEqual(comp["X"]["PE"], 100.0)
        self.assertEqual(comp["X"]["VA"], "NE")      # sin métricas de valoración
        s = h.calcular_S(comp["X"], "RV")
        self.assertTrue(s["calculable"])
        mal = dict(comp["X"], QL="NE", MO="NE")
        self.assertFalse(h.calcular_S(mal, "RV")["calculable"])

    def test_S_ejemplo(self):
        des = {"PE": 90, "QL": 80, "VA": 65, "MO": 85, "RI": 70, "LA": 90, "CO": "NA"}
        self.assertEqual(h.calcular_S(des, "RV")["S"], 79)

    def test_puertas_y_exclusiones(self):
        cs = [_cand(1, 80), _cand(2, 75, pureza=0.1), _cand(3, 70, invertible=False),
              _cand(4, 72, alertas=[{"senal": "impago_reestructuracion"}]), _cand(5, 45)]
        r = h.seleccionar(cs, "RV", "N2")
        self.assertEqual(r["excluidos_por_motivo"], {"PUREZA_INSUFICIENTE": 1, "NO_INVERTIBLE": 1, "ALERTA_CRITICA": 1,
                                                     "S_INSUFICIENTE": 1})
        self.assertEqual([c["cand_id"] for c in r["top_n"]], ["CAND-B-2026-0001"])
        self.assertIsNotNone(r["menos_de_N_motivo"])

    def test_diversidad_subcluster_y_alternativas(self):
        cs = [_cand(i, 90 - i, subcluster="cables" if i <= 3 else f"s{i}") for i in range(1, 9)]
        r = h.seleccionar(cs, "RV", "N2")
        top = [c["cand_id"] for c in r["top_n"]]
        self.assertEqual(len(top), 5)
        self.assertNotIn("CAND-B-2026-0003", top)
        self.assertEqual(r["sustituciones_diversidad"][0]["desplazado"], "CAND-B-2026-0003")
        self.assertIn("CAND-B-2026-0003", [c["cand_id"] for c in r["alternativas"]])

    def test_mismo_indice_y_emisor_rf(self):
        cs = [_cand(1, 80, indice_replicado="IDX1"), _cand(2, 78, indice_replicado="IDX1"), _cand(3, 70)]
        r = h.seleccionar(cs, "FON", "N2")
        self.assertNotIn("CAND-B-2026-0002", [c["cand_id"] for c in r["top_n"]])
        rf = [_cand(i, 80 - i, emisor="E1", pureza=0.5) for i in range(1, 5)]
        r2 = h.seleccionar(rf, "RF", "N2")
        self.assertEqual(sum(1 for c in r2["top_n"] if c["emisor"] == "E1"), 2)

    def test_correlacion(self):
        cs = [_cand(1, 80), _cand(2, 79), _cand(3, 70)]
        r = h.seleccionar(cs, "RV", "N2", correlaciones={"CAND-B-2026-0002|CAND-B-2026-0001": 0.95})
        self.assertNotIn("CAND-B-2026-0002", [c["cand_id"] for c in r["top_n"]])

    def test_veredictos_candidato(self):
        cs = [_cand(1, 80), _cand(2, 66, ic90_S=[54, 74]), _cand(3, 60), _cand(4, 70, ic90_rango=[3, 7]),
              _cand(5, 75, objecion_fuerte_sin_resolver=True)]
        r = h.seleccionar(cs, "RV", "N2")
        v = {c["cand_id"]: c["veredicto"] for c in r["top_n"]}
        self.assertEqual(v["CAND-B-2026-0001"], "PRIORITARIO_PARA_C")
        self.assertEqual(v["CAND-B-2026-0002"], "SECUNDARIO")   # IC inferior < 55 (PC6)
        self.assertEqual(v["CAND-B-2026-0003"], "SECUNDARIO")   # S < 65
        self.assertEqual(v["CAND-B-2026-0004"], "SECUNDARIO")   # FRONTERA
        self.assertEqual(v["CAND-B-2026-0005"], "SECUNDARIO")   # PC5
        r2 = h.seleccionar(cs, "RV", "N2", veredicto_ambito="VIGILAR")
        self.assertFalse(r2["prioritarios"])

    def test_banda_marginal_candidato(self):
        cs = [_cand(1, 66, S_segunda_pasada=64), _cand(2, 67)]
        r = h.seleccionar(cs, "RV", "N2")
        c1 = next(c for c in r["top_n"] if c["cand_id"] == "CAND-B-2026-0001")
        self.assertEqual(c1["S"], 64)
        c2 = next(c for c in r["top_n"] if c["cand_id"] == "CAND-B-2026-0002")
        self.assertTrue(c2.get("banda_sin_segunda_pasada"))
        self.assertEqual(c2["veredicto"], "SECUNDARIO")      # PC7 limita

    def test_gc3(self):
        cs = [dict(_cand(i, 90 - i), puertas={"PC1": "OK"}) for i in range(1, 15)]
        fin, resto = h.lista_corta_gc3(cs, 5)
        self.assertEqual(len(fin), 10)
        self.assertEqual(len(resto), 4)

    def test_apuestas(self):
        cs = [{"cand_id": "a", "emisor": "X"}, {"cand_id": "b", "emisor": "X"}, {"cand_id": "c"}, {"cand_id": "d"}]
        r = h.apuestas_independientes(cs, {"c|d": 0.95})
        self.assertEqual(r["apuestas_independientes"], 2)


class TestProcesar(unittest.TestCase):
    def entrada(self, **kw):
        e = {"nivel": "N2", "horizonte": "H4", "riesgo_1a5": 3,
             "A": TestPuntuacionesAmbito.A,
             "E": {"calidad_raices": 70, "cobertura_dimensional": 80, "calidad_metodologica": 70, "trazabilidad": 80,
                   "actualidad": 70, "discrepancias_resueltas": 60, "hipotesis_cerradas": 70},
             "refutacion": {"veredicto_tesis": "robusta", "moderadas_sin_resolver": 1}, "RE": 65,
             "segunda_pasada": {"A": 65}, "candidatos_por_tipo": {"RV": {"candidatos": [_cand(1, 80), _cand(2, 70)]}}}
        e.update(kw)
        return e

    def test_orden_de_calculo(self):
        r = h.procesar(self.entrada())
        self.assertEqual(r["puntuaciones"]["A"], 65)
        self.assertEqual(r["puntuaciones"]["C"], 73)
        self.assertEqual(r["veredicto"]["valor"], "INVERTIR")
        self.assertEqual(r["veredicto"]["siguiente_paso_sugerido"], "ENVIAR_CANDIDATOS_A_C")

    def test_sin_vehiculo_baja_a_vigilar(self):
        r = h.procesar(self.entrada(candidatos_por_tipo={"RV": {"candidatos": [_cand(1, 60), _cand(2, 58)]}}))
        self.assertEqual(r["veredicto"]["valor"], "VIGILAR")
        self.assertEqual(r["veredicto"]["motivo"], "sin vehículo de captura adecuado")

    def test_banda_sin_segunda_pasada_bloquea_pa7(self):
        r = h.procesar(self.entrada(segunda_pasada=None))
        self.assertEqual(r["puertas_ambito"]["PA7"], "BLOQUEA")
        self.assertEqual(r["veredicto"]["valor"], "VIGILAR")

    def test_pa8_sin_universo(self):
        r = h.procesar(self.entrada(candidatos_por_tipo={"RV": {"candidatos": [_cand(1, 80, invertible=False)]}}))
        self.assertEqual(r["puertas_ambito"]["PA8"], "BLOQUEA")

    def test_ejemplo_de_06_reconstruible(self):
        with open(EJEMPLO, encoding="utf-8") as fh:
            p = json.load(fh)
        rv = p["candidatos_por_tipo"]["RV"]["top_n"]
        for c in rv:
            comp = {k: ("NA" if v is None else v) for k, v in c["desglose"].items()}
            self.assertEqual(h.calcular_S(comp, "RV")["S"], c["S"])
        e = h.estrategia("CADENA_DE_VALOR", "H4", ["RV"], "N2")
        self.assertEqual(e["pesos_efectivos"], p["estrategia"]["pesos_efectivos"])

    def test_cli(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            ent = os.path.join(d, "e.json")
            sal = os.path.join(d, "s.json")
            json.dump(self.entrada(), open(ent, "w", encoding="utf-8"))
            self.assertEqual(h.main([ent, "--salida", sal]), 0)
            self.assertEqual(json.load(open(sal, encoding="utf-8"))["veredicto"]["valor"], "INVERTIR")
            json.dump({"tipo_objeto": "SECTOR", "horizonte": "H3"}, open(ent, "w"))
            self.assertEqual(h.main([ent, "--estrategia", "--salida", sal]), 0)


class TestV21CadenaYPuertas(unittest.TestCase):
    """V2.1: H5, AG-B24, PCB, AE, PEM, PV1–PV3 y mejores opciones por eslabón (7.10, 8.7, 9.12–9.13)."""

    def test_h5_moduladores_y_d9(self):
        e = h.estrategia("TEMATICA", "H5")
        self.assertEqual(sum(e["pesos_efectivos"].values()), 100)
        self.assertIn(e["profundidad"]["D9"], ("P2", "P3"))     # D9 nunca baja de P2 (8.3.2)
        e4 = h.estrategia("TEMATICA", "H4")
        self.assertGreater(e["pesos_efectivos"]["D5"], e4["pesos_efectivos"]["D5"])
        self.assertLess(e["pesos_efectivos"]["D10"], e4["pesos_efectivos"]["D10"])

    def test_activacion_ag_b24(self):
        self.assertTrue(h.estrategia("SECTOR", "H3")["activacion"]["AG-B24"]["activo"])
        self.assertTrue(h.estrategia("CADENA_DE_VALOR", "H4")["activacion"]["AG-B24"]["activo"])
        f = h.estrategia("ESTRATEGIA_FACTOR", "H2")["activacion"]["AG-B24"]
        self.assertEqual(f["codigo"], "C")
        self.assertFalse(f["activo"])                            # D4/D5 con peso < 7
        self.assertTrue(h.estrategia("ESTRATEGIA_FACTOR", "H2", nivel="N3")["activacion"]["AG-B24"]["activo"])
        self.assertEqual(h.estrategia("SECTOR", "H3")["activacion"]["AG-B24"]["dimensiones"], [])

    def test_capas_dimensiones(self):
        e = h.estrategia("SECTOR", "H3")
        self.assertTrue({"D2", "D4", "D8", "D9"} <= set(e["dimensiones_capa2"]))
        self.assertEqual(sorted(e["dimensiones_capa2"] + e["dimensiones_capa3"], key=lambda d: int(d[1:])), list(h.DIMENSIONES))

    def test_pcb_formula_y_umbral(self):
        self.assertEqual(h.calcular_PCB(4, 3, 4), 38)              # round(100·48/125) = 38,4
        self.assertEqual(h.calcular_PCB(5, 5, 5), 100)
        self.assertEqual(h.calcular_PCB(1, 1, 1), 1)
        with self.assertRaises(h.ErrorEntrada):
            h.calcular_PCB(0, 3, 3)
        self.assertEqual(h.estado_indicador_cuello("utilizacion", 0.93), "ROJO")
        self.assertEqual(h.estado_indicador_cuello("utilizacion", 0.87), "AMBAR")
        self.assertEqual(h.estado_indicador_cuello("inventarios_percentil", 8), "ROJO")
        self.assertEqual(h.estado_indicador_cuello("inventarios_percentil", 20), "AMBAR")
        self.assertEqual(h.estado_indicador_cuello("capacidad_vs_deficit", 1.0), "AMBAR")
        self.assertEqual(h.estado_indicador_cuello("insumo_sin_sustituto", True), "ROJO")
        r = h.evaluar_cuello([{"indicador": "utilizacion", "valor": 0.93}, {"indicador": "book_to_bill", "valor": 1.25},
                              {"indicador": "plazo_entrega_ratio", "valor": 1.6}], 30, 4)
        self.assertEqual((r["severidad"], r["persistencia"], r["PCB"]), (3, 4, 38))
        self.assertTrue(r["material"])
        r2 = h.evaluar_cuello([{"indicador": "utilizacion", "valor": 0.93}], 30, 5)
        self.assertFalse(r2["material"])                           # un solo indicador en rojo

    def test_ae_y_pem(self):
        ae = h.calcular_AE({"crecimiento": 80, "margen_roic": 70, "poder_negociacion": 70, "cuello": None,
                            "expectativas_inv": 60, "sustitucion_inv": 70}, PCB=38)
        self.assertEqual(ae["componentes"]["cuello"], 40)
        self.assertEqual(ae["total"], 64)
        self.assertTrue(ae["atractivo"])
        pem = h.calcular_PEM({"tecnologia": 70, "traccion": 60, "equipo": 60, "financiacion": 50, "posicion_cadena": 70,
                              "via_exposicion": 30})
        self.assertEqual(pem["total"], 59)          # 14 + 15 + 9 + 7,5 + 10,5 + 3

    def test_pv1(self):
        base = {"tipos_con_invertible": 2, "instrumentos_invertibles": 12, "capitalizacion_agregada_meur": 50000}
        self.assertEqual(h.evaluar_pv1(base)["resultado"], "SUPERADA")
        self.assertEqual(h.evaluar_pv1(dict(base, ya_descontado=True))["resultado"], "SUPERADA")   # una debilidad
        r = h.evaluar_pv1(dict(base, ya_descontado=True, sin_mecanismo=True))
        self.assertEqual(r["resultado"], "NO_SUPERADA")
        r = h.evaluar_pv1(dict(base, tipos_con_invertible=0))
        self.assertEqual([m["criterio"] for m in r["motivos"]], ["SIN_INVERTIBILIDAD"])
        r = h.evaluar_pv1(dict(base, instrumentos_invertibles=2, alerta_integridad=True))
        self.assertEqual(r["resultado"], "NO_SUPERADA")

    def test_pv2(self):
        self.assertEqual(h.evaluar_pv2(60, 60, True)["resultado"], "SUPERADA")
        r = h.evaluar_pv2(60, 40, True, fuentes_para_cerrar_E=True)
        self.assertEqual(r["resultado"], "NO_SUPERADA")
        self.assertTrue(r["proponer_consulta"])
        self.assertFalse(h.evaluar_pv2(40, 40, True, True)["proponer_consulta"])
        self.assertEqual(h.evaluar_pv2(70, 70, False)["motivos"][0]["criterio"], "TESIS_REFUTADA")

    def _esl(self):
        return [{"eslabon_id": "ESL-01", "atractivo": {"AE": 72}, "cuello_botella": {"PCB": 10, "indicadores": []}},
                {"eslabon_id": "ESL-02", "atractivo": {"AE": 40},
                 "cuello_botella": {"PCB": 38, "material": True, "indicadores": [{"estado": "ROJO"}, {"estado": "ROJO"}]}},
                {"eslabon_id": "ESL-03", "atractivo": {"AE": 45}, "cuello_botella": {"PCB": 5, "indicadores": []}}]

    def test_pv3(self):
        ok = {"PC1": "OK", "PC2": "OK", "PC3": "OK", "PC4": "OK"}
        c = [{"cand_id": "A", "eslabon_id": "ESL-03", "S": 80, "puertas": ok}]
        self.assertEqual(h.evaluar_pv3(self._esl(), c)["resultado"], "NO_SUPERADA")      # ESL-03 no cualifica
        c.append({"cand_id": "B", "eslabon_id": "ESL-02", "S": 55, "puertas": ok})
        self.assertEqual(h.evaluar_pv3(self._esl(), c)["resultado"], "SUPERADA")
        c[1]["S"] = 45
        self.assertEqual(h.evaluar_pv3(self._esl(), c)["resultado"], "NO_SUPERADA")

    def test_mejores_por_eslabon(self):
        ok = {f"PC{i}": "OK" for i in range(1, 9)}
        cs = [{"cand_id": f"C{i}", "eslabon_id": "ESL-01", "S": 90 - i * 3, "puertas": ok, "pureza_eslabon": 0.5,
               "en_top_n": i < 2, "veredicto": "PRIORITARIO_PARA_C" if i < 2 else "SECUNDARIO"} for i in range(8)]
        cs.append({"cand_id": "X", "eslabon_id": "ESL-01", "S": 49, "puertas": ok})
        r = h.mejores_por_eslabon(self._esl(), {"RV": cs[:5], "FON": cs[5:]}, "N2", "INVERTIR")
        t = r["tablas"]["ESL-01"]["opciones"]
        self.assertEqual(len(t), 5)                               # hasta cinco
        self.assertTrue(t[0]["en_top_n_tipo"] and t[1]["en_top_n_tipo"] and not t[2]["en_top_n_tipo"])
        self.assertEqual(t[2]["veredicto"], "PRIORITARIO_PARA_C")  # S = 84 ≥ 65, añadido por cobertura
        self.assertNotIn("X", [o["cand_id"] for o in t])
        self.assertIn("ESL-02", r["tablas"])
        self.assertIsNotNone(r["tablas"]["ESL-02"]["sin_opciones_motivo"])
        self.assertNotIn("ESL-03", r["tablas"])
        r1 = h.mejores_por_eslabon(self._esl(), {"RV": cs}, "N1", "INVERTIR", eslabon_critico="ESL-01")
        self.assertEqual(len(r1["tablas"]["ESL-01"]["opciones"]), 3)
        self.assertEqual(list(r1["tablas"]), ["ESL-01"])
        rv = h.mejores_por_eslabon(self._esl(), {"RV": cs}, "N2", "VIGILAR")
        self.assertTrue(all(o["veredicto"] == "SECUNDARIO" for o in rv["tablas"]["ESL-01"]["opciones"] if not o["en_top_n_tipo"]))


if __name__ == "__main__":
    unittest.main()
