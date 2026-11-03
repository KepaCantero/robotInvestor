# -*- coding: utf-8 -*-
"""Pruebas de HT-10 (anexo de datos y cálculos en XLSX y CSV)."""
import csv
import json
import os
import sys
import tempfile
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, RAIZ)

import ht10_anexo_datos as h  # noqa: E402

EJEMPLO = os.path.join(RAIZ, "ejemplos", "paquete_analisis_mercado_ejemplo.json")


class TestAnexo(unittest.TestCase):
    def setUp(self):
        self.p = json.load(open(EJEMPLO, encoding="utf-8"))

    def test_hojas_desde_paquete(self):
        hojas = h.construir_hojas(self.p)
        for k in ("Leeme", "Puntuaciones", "Cifras", "Fuentes", "Universo_RV", "Universo_FON", "Universo_RF",
                  "Escenarios", "Sensibilidades", "Pronosticos", "Artefactos", "Encargos_C"):
            self.assertIn(k, hojas)
        self.assertNotIn("Universo_DIV", hojas)
        self.assertEqual(len(hojas["Universo_RV"]["filas"]), 5)
        self.assertEqual(len(hojas["Encargos_C"]["filas"]), 11)     # 10 del top-N + 1 por cobertura de eslabón (V2.1)
        self.assertEqual(len(hojas["Eslabones"]["filas"]), 5)
        self.assertEqual(len(hojas["Opciones_eslabon"]["filas"]), 10)
        self.assertEqual(len(hojas["Emergentes"]["filas"]), 3)
        f = next(x for x in hojas["Eslabones"]["filas"] if x["eslabon_id"] == "ESL-02")
        import ht03_puntuaciones as h3
        self.assertEqual(f["PCB"], h3.calcular_PCB(f["severidad"], f["persistencia"], f["relevancia_valor"]))
        self.assertTrue(any(f["campo"] == "AVISO" for f in hojas["Leeme"]["filas"]))
        self.assertNotIn("probabilidad_interna", h.COLUMNAS["Pronosticos"])

    def test_universo_completo_y_csv(self):
        datos = {"universo": {"RV": [{"tipo_activo": "RV", "id": "X", "invertible": False, "motivo_exclusion": "PUREZA_INSUFICIENTE",
                                       "PE": 10, "roic": 0.1}]},
                 "cifras": [{"id": "CALC-B-2026-0901", "valor": 7, "unidad": "%"}]}
        with tempfile.TemporaryDirectory() as d:
            r = h.generar_anexo(self.p, d, "anexo", datos)
            self.assertTrue(os.path.exists(r["xlsx"]))
            filas = list(csv.DictReader(open(os.path.join(r["csv"], "Universo_RV.csv"), encoding="utf-8-sig")))
            self.assertEqual(filas[0]["comp_PE"], "10")
            self.assertIn("roic", filas[0])
            from openpyxl import load_workbook
            wb = load_workbook(r["xlsx"])
            self.assertEqual(wb["Cifras"].max_row, 2)

    def test_plantilla(self):
        with tempfile.TemporaryDirectory() as d:
            r = h.generar_plantilla(d, "plantilla")
            self.assertEqual(set(r["filas_por_hoja"]) - {"Leeme"}, {"Puntuaciones", "Cifras", "Fuentes", "Universo_RV",
                             "Escenarios", "Sensibilidades", "Pronosticos", "Artefactos", "Encargos_C", "Eslabones",
                             "Opciones_eslabon", "Emergentes"})
            self.assertEqual(r["filas_por_hoja"]["Cifras"], 0)

    def test_cli(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(h.main([EJEMPLO, "--salida", d, "--nombre", "x"]), 0)
            self.assertTrue(os.path.exists(os.path.join(d, "x.xlsx")))


if __name__ == "__main__":
    unittest.main()
