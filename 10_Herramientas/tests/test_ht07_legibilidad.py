# -*- coding: utf-8 -*-
"""Pruebas unitarias de HT-07 (legibilidad). Ejecutar: python3 -m pytest tests  (o python3 -m unittest)."""
import json
import os
import sys
import tempfile
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, RAIZ)

import ht07_legibilidad as h  # noqa: E402


class TestSilabeo(unittest.TestCase):
    CASOS = {
        "casa": "ca-sa", "perro": "pe-rro", "chico": "chi-co", "calle": "ca-lle", "cuidado": "cui-da-do",
        "país": "pa-ís", "teatro": "te-a-tro", "poesía": "po-e-sí-a", "aire": "ai-re", "huevo": "hue-vo",
        "guerra": "gue-rra", "pingüino": "pin-güi-no", "construcción": "cons-truc-ción", "inflación": "in-fla-ción",
        "hablar": "ha-blar", "estudiáis": "es-tu-diáis", "rentabilidad": "ren-ta-bi-li-dad", "atlántico": "at-lán-ti-co",
        "muy": "muy", "hoy": "hoy", "ayer": "a-yer", "río": "rí-o", "aéreo": "a-é-re-o", "uruguay": "u-ru-guay",
        "que": "que", "quiero": "quie-ro", "acción": "ac-ción", "instante": "ins-tan-te", "obstáculo": "obs-tá-cu-lo",
        "emplear": "em-ple-ar", "instrucción": "ins-truc-ción", "leía": "le-í-a", "buey": "buey", "creer": "cre-er",
        "ciudad": "ciu-dad", "diurno": "diur-no", "cooperar": "co-o-pe-rar", "oír": "o-ír",
    }

    def test_palabras_de_referencia(self):
        for palabra, esperado in self.CASOS.items():
            with self.subTest(palabra=palabra):
                self.assertEqual("-".join(h.silabear(palabra)), esperado)

    def test_mayusculas_y_guiones(self):
        self.assertEqual(h.contar_silabas("Construcción"), 3)
        self.assertEqual(h.contar_silabas("franco-alemán"), 5)

    def test_numeros(self):
        self.assertEqual(h.contar_silabas("12,5"), h.SILABAS_POR_NUMERO)


class TestFrases(unittest.TestCase):
    def test_abreviaturas_y_decimales(self):
        f = h.dividir_frases("El Sr. Pérez dijo que sí. ¿Vienes? Sube un 1.5 % en EE. UU. y p. ej. más.")
        self.assertEqual(len(f), 3)
        self.assertTrue(f[2].startswith("Sube un 1.5"))

    def test_lineas_en_blanco_y_vinetas(self):
        f = h.dividir_frases("Título\n\n- uno\n- dos\nlínea continuada")
        self.assertEqual(f, ["Título", "uno", "dos línea continuada"])


class TestIndice(unittest.TestCase):
    def test_formula_fernandez_huerta(self):
        # 2 frases, 7 palabras, 11 sílabas: P = 157,14; F (corregida, Law 2011) = 3,5 palabras por frase
        r = h.analizar("La casa es roja. El perro come.", es_html=False)
        self.assertEqual((r["frases"], r["palabras"], r["silabas"]), (2, 7, 11))
        esperado = round(206.84 - 0.60 * (100 * 11 / 7) - 1.02 * (7 / 2), 2)
        self.assertAlmostEqual(r["fernandez_huerta"], esperado, places=2)
        original = round(206.84 - 0.60 * (100 * 11 / 7) - 1.02 * (100 * 2 / 7), 2)
        self.assertAlmostEqual(r["fernandez_huerta_original_informativo"], original, places=2)
        self.assertTrue(r["cumple_fh"])

    def test_texto_dificil_no_cumple(self):
        t = ("La heterogeneidad institucional condiciona significativamente la transmisión intertemporal "
             "de perturbaciones macroeconómicas internacionales sobre determinadas valoraciones patrimoniales "
             "correspondientes a instrumentos estructurados, particularmente durante episodios caracterizados "
             "por restricciones extraordinarias de financiación interbancaria.")
        r = h.analizar(t, es_html=False)
        self.assertFalse(r["cumple_fh"])
        self.assertEqual(r["pct_frases_mas_de_20"], 100.0)
        self.assertEqual(len(r["frases_largas"]), 1)

    def test_texto_vacio(self):
        r = h.analizar("", es_html=False)
        self.assertIsNone(r["fernandez_huerta"])
        self.assertFalse(r["cumple_fh"])


class TestHTML(unittest.TestCase):
    def test_solo_texto_visible(self):
        doc = ("<html><head><title>T</title><style>p{}</style><script>var a='oculto';</script></head>"
               "<body><h1>Hola</h1><p>Uno <b>dos</b>.<br>Tres</p><div hidden><p>secreto</div>"
               "<p style='display:none'>nada</p><span aria-hidden='true'>icono</span><p>fin</p></body></html>")
        texto = h.extraer_texto_html(doc)
        for oculto in ("oculto", "secreto", "nada", "icono", "p{}"):
            self.assertNotIn(oculto, texto)
        self.assertEqual(h.dividir_frases(texto), ["Hola", "Uno dos.", "Tres", "fin"])

    def test_deteccion_automatica(self):
        r = h.analizar("<p>La casa es roja.</p><p>El perro come.</p>")
        self.assertTrue(r["entrada_html"])
        self.assertEqual(r["frases"], 2)


class TestJerga(unittest.TestCase):
    def test_lista_inicial_amplia(self):
        self.assertGreaterEqual(len(set(h.JERGA_FINANCIERA_POR_DEFECTO)), 60)

    def test_explicada_y_sin_explicar(self):
        t = "La volatilidad (cuánto se mueve el precio) es alta. La liquidez es baja. Otra vez volatilidad."
        j = {x["termino"]: x for x in h.detectar_jerga(t, h.JERGA_FINANCIERA_POR_DEFECTO)}
        self.assertTrue(j["volatilidad"]["explicado_primera_vez"])
        self.assertEqual(j["volatilidad"]["apariciones"], 2)
        self.assertFalse(j["liquidez"]["explicado_primera_vez"])

    def test_coincidencia_mas_larga_y_sin_tildes(self):
        t = "Sube la volatilidad implicita y la PRIMA DE RIESGO."
        j = {x["termino"] for x in h.detectar_jerga(t, h.JERGA_FINANCIERA_POR_DEFECTO)}
        self.assertIn("volatilidad implícita", j)
        self.assertNotIn("volatilidad", j)
        self.assertIn("prima de riesgo", j)

    def test_lista_configurable(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as fh:
            fh.write("# comentario\nchiringuito\n")
        try:
            terminos = h.cargar_jerga(fh.name)
            self.assertEqual(terminos, ["chiringuito"])
            r = h.analizar("Fuimos al chiringuito.", es_html=False, terminos_jerga=terminos)
            self.assertEqual(r["jerga_sin_explicar"], ["chiringuito"])
        finally:
            os.unlink(fh.name)


class TestCLI(unittest.TestCase):
    def test_ejemplo_html(self):
        with tempfile.TemporaryDirectory() as d:
            salida = os.path.join(d, "r.json")
            codigo = h.main([os.path.join(RAIZ, "ejemplos", "informe_visual_ejemplo.html"), "--salida", salida])
            with open(salida, encoding="utf-8") as fh:
                r = json.load(fh)
        self.assertEqual(codigo, 0)
        self.assertGreaterEqual(r["fernandez_huerta"], 70)
        self.assertNotIn("apalancamiento", [j["termino"] for j in r["jerga"]])  # estaba oculto


if __name__ == "__main__":
    unittest.main()
