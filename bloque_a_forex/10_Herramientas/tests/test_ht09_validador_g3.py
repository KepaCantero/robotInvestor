# -*- coding: utf-8 -*-
"""Pruebas unitarias de HT-09 Forex (validador determinista G3 del paquete de oportunidades en divisas)."""
import copy
import json
import os
import sys
import tempfile
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
EJ = os.path.join(RAIZ, "ejemplos")
sys.path.insert(0, RAIZ)

import ht09_validador_g3 as h  # noqa: E402


def cargar(nombre):
    with open(os.path.join(EJ, nombre), encoding="utf-8") as fh:
        return json.load(fh)


class Base(unittest.TestCase):
    def setUp(self):
        self.paquete = cargar("paquete_oportunidades_ejemplo.json")
        self.certs = cargar("certificados_ejemplo.json")["certificados"]
        self.desgloses = cargar("desgloses_ejemplo.json")
        self.trazas = cargar("trazas_ejemplo.json")
        self.artefactos = cargar("artefactos_ejemplo.json")
        self.informe = os.path.join(EJ, "informe_visual_ejemplo.html")

    def validar(self, paquete=None, **kw):
        args = dict(certificados=self.certs, informe_visual=self.informe, desgloses=self.desgloses,
                    trazas=self.trazas, artefactos=self.artefactos)
        args.update(kw)
        return h.validar(paquete if paquete is not None else self.paquete, **args)

    def op(self, p, i=0, seg="G10N"):
        return p["segmentos"][seg]["opciones"][i]

    def comprobacion(self, res, cid):
        return next(c for c in res["comprobaciones"] if c["id"] == cid)

    def assertBloquea(self, res, cid, fragmento=None):
        self.assertEqual(res["dictamen"], "BLOQUEADO")
        c = self.comprobacion(res, cid)
        self.assertEqual(c["resultado"], "BLOQUEO", c)
        if fragmento:
            self.assertTrue(any(fragmento in i["detalle"] for i in c["incidencias"]), c["incidencias"])

    def assertOK(self, res, cid):
        self.assertEqual(self.comprobacion(res, cid)["resultado"], "OK", self.comprobacion(res, cid))


class TestEjemplo(Base):
    def test_ejemplo_completo_apto(self):
        res = self.validar()
        self.assertEqual(res["dictamen"], "APTO", [c for c in res["comprobaciones"] if c["resultado"] != "OK"])
        self.assertEqual(len(res["comprobaciones"]), 30)   # C01–C19 (V1.1: C17–C19) + G3-FX-01…11
        self.assertEqual([c["id"] for c in res["comprobaciones"]][-11:], [f"G3-FX-{i:02d}" for i in range(1, 12)])
        self.assertGreaterEqual(self.comprobacion(res, "C12")["datos"]["fernandez_huerta"], 70)
        neta = self.comprobacion(res, "G3-FX-08")["datos"]["exposicion_neta_calculada"]
        self.assertEqual(neta["USD"], -5.0)   # V1.1: añade EUR/USD estructural (H5) en G10N
        self.assertAlmostEqual(neta["JPY"], 0.5)

    def test_sin_entradas_auxiliares(self):
        res = h.validar(self.paquete)
        self.assertBloquea(res, "C07", "sin certificado")
        self.assertEqual(self.comprobacion(res, "C04")["resultado"], "ADVERTENCIA")
        self.assertEqual(self.comprobacion(res, "C12")["resultado"], "ADVERTENCIA")

    def test_advertencias_sin_bloqueo(self):
        res = self.validar(informe_visual=None)
        self.assertEqual(res["dictamen"], "APTO_CON_ADVERTENCIAS")


class TestBloqueos(Base):
    def test_campo_obligatorio(self):
        p = copy.deepcopy(self.paquete)
        del p["regimen_macro"]
        del self.op(p)["invalidacion"]
        self.assertBloquea(self.validar(p), "C01", "ausente")

    def test_valores_no_permitidos(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["confianza"] = "segurísimo"
        self.op(p)["riesgo_1a5"] = 7
        p["segmentos"]["G10N"]["estado_semaforo"] = "ROJO"
        p["regimen_cambiario"]["dolar"] = "por las nubes"
        self.assertBloquea(self.validar(p), "C01", "no permitido")

    def test_prefijos_fx(self):
        p = copy.deepcopy(self.paquete)
        p["run_id"] = "RUN-2026-0019"
        self.assertBloquea(self.validar(p), "C01", "RUN-FX-")
        p = copy.deepcopy(self.paquete)
        self.op(p)["opp_id"] = "OPP-2026-0007"
        self.assertBloquea(self.validar(p, desgloses={}), "C01", "OPP-FX-")
        p = copy.deepcopy(self.paquete)
        self.op(p)["horizontes"]["H2"]["prg_id"] = "PRG-2026-0041"
        self.assertBloquea(self.validar(p), "C01", "PRG-FX-")
        p = copy.deepcopy(self.paquete)
        self.op(p)["tnd_ids"] = ["TND-2026-0003"]
        self.assertBloquea(self.validar(p), "C01", "TND-FX-")
        p = copy.deepcopy(self.paquete)
        self.op(p)["evidencias"] = ["CLM-2026-0101"]
        self.op(p)["calculos"] = ["CALC-2026-0033"]
        res = self.validar(p, trazas=None, artefactos=None)
        self.assertBloquea(res, "C01", "CLM-FX-")
        self.assertBloquea(res, "C01", "CALC-FX-")

    def test_mas_de_tres(self):
        p = copy.deepcopy(self.paquete)
        ops = p["segmentos"]["G10N"]["opciones"]
        for k in range(2):
            extra = copy.deepcopy(ops[1])
            extra["opp_id"] = f"OPP-FX-2026-09{k}0"
            extra["rango"] = 3 + k
            extra["cluster"] = f"CL-{90 + k}"
            ops.append(extra)
        self.assertBloquea(self.validar(p), "C02", "máximo 3")

    def test_rangos(self):
        p = copy.deepcopy(self.paquete)
        self.op(p, 1)["rango"] = 1
        self.assertBloquea(self.validar(p), "C02")

    def test_menos_de_tres_sin_motivo(self):
        p = copy.deepcopy(self.paquete)
        p["segmentos"]["EMEA"]["menos_de_tres_motivo"] = None
        self.assertBloquea(self.validar(p), "C03")

    def test_rk_no_reconstruible(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["puntuaciones"]["RK"] = 79
        self.assertBloquea(self.validar(p, desgloses={}), "C04", "RK declarado 79")

    def test_desglose_discrepante(self):
        d = copy.deepcopy(self.desgloses)
        d["OPP-FX-2026-0007"]["dimensiones"]["A"]["asimetria"] = 100
        self.assertBloquea(self.validar(desgloses=d), "C04", "HT-03")

    def test_desglose_con_dimensiones_del_bloque_general(self):
        d = copy.deepcopy(self.desgloses)
        dims_a = d["OPP-FX-2026-0007"]["dimensiones"]["A"]
        dims_a["invertibilidad"] = dims_a.pop("convertibilidad")
        self.assertBloquea(self.validar(desgloses=d), "C04", "convertibilidad")

    def test_total_no_multiplo_de_5(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["puntuaciones"]["M"] = 52
        self.assertBloquea(self.validar(p), "C04", "múltiplo de 5")

    def test_elegibilidad(self):
        p = copy.deepcopy(self.paquete)
        self.op(p, 1)["puntuaciones"].update({"E": 55, "RK": 63})
        self.assertBloquea(self.validar(p, desgloses={}), "C05", "E=55 < 60")

    def test_puerta_ps(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["puertas"]["PS3"] = False
        self.assertBloquea(self.validar(p), "C05", "PS3")

    def test_banda_marginal_desde_desglose(self):
        d = copy.deepcopy(self.desgloses)
        p = copy.deepcopy(self.paquete)
        d["OPP-FX-2026-0008"]["dimensiones"]["E"] = {k: 60 for k in d["OPP-FX-2026-0008"]["dimensiones"]["E"]}
        self.op(p, 1)["puntuaciones"].update({"E": 60, "RK": 65})
        self.assertBloquea(self.validar(p, desgloses=d), "C05", "PS8")

    def test_probabilidad_sin_certificado(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["horizontes"]["H2"]["prob"] = 0.55
        self.assertBloquea(self.validar(p), "C07", "G10N×H2")

    def test_certificado_no_vigente(self):
        certs = [dict(self.certs[0], vigente=False)]
        self.assertBloquea(self.validar(certificados=certs), "C07")

    def test_evidencias_y_calculos(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["evidencias"] = []
        self.op(p, 1)["calculos"] = ["CALC-FX-2026-7777"]
        res = self.validar(p)
        self.assertBloquea(res, "C08", "Sin evidencias")
        self.assertTrue(any("CALC-FX-2026-7777" in i["detalle"] for i in self.comprobacion(res, "C08")["incidencias"]))

    def test_traza_clm_sin_evd(self):
        trazas = dict(self.trazas)
        del trazas["CLM-FX-2026-0102"]
        self.assertBloquea(self.validar(trazas=trazas), "C08", "CLM-FX-2026-0102")

    def test_objecion_fuerte_sin_resolver(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["objeciones"].append({"fuerza": "fuerte", "resumen": "Riesgo de intervención del Ministerio de Finanzas", "respuesta": ""})
        self.assertBloquea(self.validar(p), "C09", "fuerte")

    def test_objecion_fuerte_respondida_pero_no_resuelta(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["objeciones"].append({"fuerza": "fuerte", "resumen": "x", "respuesta": "y", "resuelta": False})
        self.assertBloquea(self.validar(p), "C09")

    def test_relevancia_incoherente(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["riesgo_1a5"] = 4
        self.assertBloquea(self.validar(p), "C10", "riesgo 4/5")
        p = copy.deepcopy(self.paquete)
        self.op(p, 1)["reversibilidad"] = "baja"
        self.assertBloquea(self.validar(p), "C10", "reversibilidad baja")

    def test_relevancia_alta_anexo_a_forex(self):
        f = h.relevancia_esperada_alta
        self.assertEqual(f({"puntuaciones": {"E": 65, "A": 75}}, "G10N", True, {}),
                         ["E 65 < 70 con A 75 ≥ 75 (atractiva pero incierta)"])
        h4 = {"H4": {"prg_id": "PRG-FX-1"}}
        self.assertEqual(f({"puntuaciones": {}, "horizontes": h4, "riesgo_1a5": 3}, "ESTR", True, {}),
                         ["horizonte H4 con riesgo ≥ 3 o liquidez baja"])
        self.assertEqual(f({"puntuaciones": {}, "horizontes": h4, "riesgo_1a5": 2}, "ESTR", True, {}), [])   # H4 solo no basta
        self.assertEqual(f({"puntuaciones": {}, "horizontes": h4, "riesgo_1a5": 2, "liquidez": "baja"}, "G10M", True, {}),
                         ["horizonte H4 con riesgo ≥ 3 o liquidez baja"])
        self.assertEqual(f({"puntuaciones": {}, "tipo_opcion": "REGIMEN"}, "EMEA", True, {}), ["opción de tipo REGIMEN"])
        self.assertEqual(f({"puntuaciones": {}, "liquidez": "baja"}, "EMLA", True, {}), ["divisa emergente de liquidez baja"])
        self.assertEqual(f({"puntuaciones": {}, "liquidez": "baja"}, "G10M", True, {}), [])

    def test_riesgo_minimo_con_controles(self):
        p = copy.deepcopy(self.paquete)
        o = self.op(p, 0, "EMAS")
        o["convertibilidad"]["controles_capitales"] = True
        self.assertBloquea(self.validar(p), "G3-FX-04", "mínimo 4")

    def test_paquete_bloque_b(self):
        p = copy.deepcopy(self.paquete)
        p["paquete_para_bloque_B"] = []
        self.assertBloquea(self.validar(p), "C11", "ENVIAR_A_BLOQUE_B")
        p = copy.deepcopy(self.paquete)
        p["paquete_para_bloque_B"][0]["invalidacion"] = []
        self.assertBloquea(self.validar(p), "C11", "vacío")

    def test_legibilidad(self):
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as fh:
            fh.write("<p>La heterogeneidad institucional condiciona significativamente la transmisión intertemporal de "
                     "perturbaciones macroeconómicas internacionales sobre determinadas paridades cambiarias.</p>")
        try:
            self.assertBloquea(self.validar(informe_visual=fh.name), "C12", "Fernández-Huerta")
        finally:
            os.unlink(fh.name)
        self.assertBloquea(self.validar(informe_visual="/no/existe.html"), "C12")

    def test_credenciales(self):
        p = copy.deepcopy(self.paquete)
        p["limitaciones"].append('api_key: "sk-ABCDEFGHIJKLMNOPQRSTUVWX123"')
        self.assertBloquea(self.validar(p), "C13")


class TestForex(Base):
    """Seis segmentos, tabla 8.3 Forex, frontera con el Bloque B y comprobaciones G3-FX-01 a G3-FX-11 (Anexo 1 del Plan de pruebas)."""

    def opcion_en(self, p, seg, oid, horizontes=None, **kw):
        o = copy.deepcopy(self.op(p, 1))
        o.update({"opp_id": oid, "rango": 1, "segmento": seg, "relevancia_decisional": "MEDIA", "cluster": "CL-77"})
        o.update(kw)
        if horizontes is not None:
            o["horizontes"] = horizontes
        p["segmentos"][seg] = {"estado_semaforo": "AMBAR", "regimen_segmento": "Régimen de prueba del segmento.", "candidatas_analizadas": 3,
                               "opciones": [o], "menos_de_tres_motivo": "Solo una elegible en la prueba."}
        return o

    def test_seis_segmentos_y_tabla_8_3(self):
        self.assertEqual(h.SEGMENTOS, ("G10N", "G10M", "EMAS", "EMLA", "EMEA", "ESTR"))
        self.assertEqual(set(h.TABLA_HORIZONTES), set(h.SEGMENTOS))
        self.assertEqual(h.TABLA_HORIZONTES["ESTR"], {"H1": "NO", "H2": "SI", "H3": "SI", "H4": "SI", "H5": "LIMITADO"})
        for s in ("EMAS", "EMLA", "EMEA"):
            self.assertEqual(h.TABLA_HORIZONTES[s], {"H1": "LIMITADO", "H2": "SI", "H3": "SI", "H4": "LIMITADO", "H5": "LIMITADO"})
        self.assertEqual({k: v for k, v in h.TABLA_HORIZONTES["G10N"].items() if k != "H5"}, {f"H{i}": "SI" for i in range(1, 5)})
        # V1.1: H5 «limitado» en los seis segmentos
        self.assertEqual({h.TABLA_HORIZONTES[s]["H5"] for s in h.SEGMENTOS}, {"LIMITADO"})

    def test_segmento_desconocido_o_incoherente(self):
        p = copy.deepcopy(self.paquete)
        p["segmentos"]["DIV"] = copy.deepcopy(p["segmentos"]["EMEA"])
        self.assertBloquea(self.validar(p), "C01", "Segmento desconocido")
        p = copy.deepcopy(self.paquete)
        self.op(p)["segmento"] = "G10M"
        self.assertBloquea(self.validar(p), "C01", "segmento")

    def test_estr_h1_no(self):
        p = copy.deepcopy(self.paquete)
        o = self.op(p, 0, "ESTR")
        o["horizontes"]["H1"] = {"vista": "alcista", "banda": "incierto", "prob": None, "prg_id": "PRG-FX-2026-0901",
                                 "referencia": "paseo aleatorio", "advertencia": "Menor fiabilidad"}
        self.assertBloquea(self.validar(p), "C06", "no aplicable a ESTR")

    def test_limitado_exige_catalizador_y_liquidez(self):
        p = copy.deepcopy(self.paquete)
        o = self.op(p, 0, "EMLA")
        o["horizontes"]["H1"] = {"vista": "bajista", "banda": "incierto", "prob": None, "prg_id": "PRG-FX-2026-0902",
                                 "referencia": "paseo aleatorio", "advertencia": "Menor fiabilidad"}
        res = self.validar(p)
        self.assertEqual(self.comprobacion(res, "C06")["resultado"], "ADVERTENCIA")   # con catalizador y liquidez alta
        o["catalizadores"] = []
        self.assertBloquea(self.validar(p), "C06", "catalizador")
        p = copy.deepcopy(self.paquete)
        o = self.op(p, 0, "EMAS")
        o["horizontes"]["H4"] = {"vista": "bajista", "banda": "incierto", "prob": None, "prg_id": "PRG-FX-2026-0903",
                                 "referencia": "paseo aleatorio"}
        o["liquidez"] = "baja"
        self.assertBloquea(self.validar(p), "C06", "liquidez")

    def test_ps3_convertibilidad(self):
        p = copy.deepcopy(self.paquete)
        self.op(p, 0, "EMAS")["convertibilidad"]["ndf"] = False
        self.assertBloquea(self.validar(p), "G3-FX-04", "no convertible")
        p = copy.deepcopy(self.paquete)
        self.op(p, 0, "EMAS")["convertibilidad"].update({"ndf": False, "exposicion_alternativa": True})
        self.assertOK(self.validar(p), "G3-FX-04")
        p = copy.deepcopy(self.paquete)
        self.op(p)["convertibilidad"]["impiden_exposicion"] = True
        self.assertBloquea(self.validar(p), "G3-FX-04", "repatriación")
        p = copy.deepcopy(self.paquete)
        del self.op(p)["convertibilidad"]["profundidad"]
        self.assertBloquea(self.validar(p), "G3-FX-04", "incompleto")
        p = copy.deepcopy(self.paquete)
        self.op(p, 1)["regimen_cambiario_divisa"] = "TIPO_FIJO"
        self.assertBloquea(self.validar(p), "G3-FX-04", "tipo fijo")

    def test_notacion_del_par(self):
        for par, frag in (("USDJPY", "BASE/COTIZADA"), ("USD/XYZ", "ISO 4217"), ("usd/jpy", "BASE/COTIZADA"), ("JPY/JPY", "coinciden")):
            p = copy.deepcopy(self.paquete)
            self.op(p)["par"] = par
            self.assertBloquea(self.validar(p), "G3-FX-01", frag)
        p = copy.deepcopy(self.paquete)
        o = self.op(p)
        o.update({"par": "JPY/USD", "direccion": "ALCISTA_BASE"})
        o["composicion"] = [{"divisa": "JPY", "peso": 1.0, "lado": "LARGO"}, {"divisa": "USD", "peso": 1.0, "lado": "CORTO"}]
        self.assertBloquea(self.validar(p), "G3-FX-01", "convención")
        self.assertTrue(h.notacion_convencional("EUR", "USD") and h.notacion_convencional("USD", "MXN")
                        and h.notacion_convencional("ZAR", "JPY") and h.notacion_convencional("EUR", "PLN"))
        self.assertFalse(h.notacion_convencional("MXN", "USD") or h.notacion_convencional("USD", "EUR"))

    def test_direccion_composicion_y_financiacion(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["direccion"] = "SUBE"
        self.assertBloquea(self.validar(p), "G3-FX-01", "ALCISTA_BASE o BAJISTA_BASE")
        p = copy.deepcopy(self.paquete)
        self.op(p)["divisa_financiacion"] = "JPY"
        self.assertBloquea(self.validar(p), "G3-FX-01", "debería ser USD")
        p = copy.deepcopy(self.paquete)
        self.op(p)["composicion"][0]["lado"] = "LARGO"
        self.assertBloquea(self.validar(p), "G3-FX-01", "incoherente con la composición")
        p = copy.deepcopy(self.paquete)
        self.op(p)["divisa_financiacion"] = None
        self.assertBloquea(self.validar(p), "G3-FX-01", "PS4")
        p = copy.deepcopy(self.paquete)
        self.op(p)["nombre_llano"] = "El dólar podría ganar valor frente al yen"
        self.assertBloquea(self.validar(p), "G3-FX-01", "contradice")
        self.assertEqual(h.lados_desde_nombre_llano("El dólar australiano podría subir frente al neozelandés"), None)
        self.assertEqual(h.lados_desde_nombre_llano("El peso mexicano podría ganar valor frente al dólar"), {"MXN": "LARGO", "USD": "CORTO"})

    def test_ps4_cesta_sin_pesos_o_sin_financiacion(self):
        p = copy.deepcopy(self.paquete)
        del self.op(p, 0, "ESTR")["composicion"][0]["peso"]
        self.assertBloquea(self.validar(p), "G3-FX-02", "PS4")
        p = copy.deepcopy(self.paquete)
        self.op(p, 0, "ESTR")["divisa_financiacion"] = None
        self.assertBloquea(self.validar(p), "G3-FX-02", "divisa de financiación")
        p = copy.deepcopy(self.paquete)
        self.op(p, 0, "ESTR")["composicion"][0]["peso"] = 0.6
        self.assertBloquea(self.validar(p), "G3-FX-02", "suman")
        p = copy.deepcopy(self.paquete)
        self.op(p, 0, "ESTR")["direccion"] = "ALCISTA_BASE"
        self.assertBloquea(self.validar(p), "G3-FX-01", "composicion")

    def test_volatilidad_y_regimen(self):
        p = copy.deepcopy(self.paquete)
        o = self.op(p)
        o["tipo_opcion"] = "VOLATILIDAD"
        self.assertBloquea(self.validar(p), "G3-FX-01", "vista_volatilidad")
        o.update({"direccion": None, "vista_volatilidad": {"sentido": "ALZA", "plazo": "3M"},
                  "carry": {"anual_pct": None, "signo": "no aplicable", "ajustado_vol": None}})
        for hv in o["horizontes"].values():
            hv["tipo_rentabilidad"] = "NIVEL_VOLATILIDAD"
        res = self.validar(p)
        self.assertNotEqual(self.comprobacion(res, "G3-FX-01")["resultado"], "BLOQUEO", self.comprobacion(res, "G3-FX-01"))
        self.assertOK(res, "G3-FX-05")
        self.assertOK(res, "G3-FX-11")
        p = copy.deepcopy(self.paquete)
        o = self.op(p, 0, "EMLA")
        o["tipo_opcion"] = "REGIMEN"
        o["relevancia_decisional"] = "ALTA"
        res = self.validar(p)
        self.assertBloquea(res, "G3-FX-04", "régimen")
        self.assertBloquea(res, "G3-FX-04", "mínimo 4")
        o["regimen_cambiario_divisa"] = "TIPO_FIJO"
        o["riesgo_1a5"] = 4
        res = self.validar(p)
        self.assertEqual(self.comprobacion(res, "G3-FX-04")["resultado"], "OK", self.comprobacion(res, "G3-FX-04"))
        self.assertEqual(self.comprobacion(res, "C10")["resultado"], "OK", self.comprobacion(res, "C10"))

    def test_asignacion_de_segmento(self):
        f = h.segmento_esperado
        casos = {("PAR", "USD/MXN"): "EMLA", ("CRUCE", "EUR/PLN"): "EMEA", ("CRUCE", "AUD/JPY"): "G10M", ("CRUCE", "EUR/NOK"): "G10M",
                 ("CRUCE", "GBP/JPY"): "G10N", ("CRUCE", "CAD/MXN"): "EMLA", ("CRUCE", "CNH/JPY"): "EMAS", ("CRUCE", "ZAR/JPY"): "EMEA",
                 ("VOLATILIDAD", "EUR/CHF"): "G10N"}
        for (t, par), seg in casos.items():
            self.assertEqual(f({"tipo_opcion": t, "par": par}), seg, par)
        self.assertEqual(f({"tipo_opcion": "ESTRATEGIA"}), "ESTR")
        self.assertEqual(f({"tipo_opcion": "VOLATILIDAD", "par": None}), "ESTR")
        self.assertEqual(f({"tipo_opcion": "CESTA", "composicion": [{"divisa": d} for d in ("BRL", "MXN", "USD")]}), "ESTR")
        p = copy.deepcopy(self.paquete)
        self.opcion_en(p, "EMEA", "OPP-FX-2026-0610", nombre="AUD/JPY alcista", par="AUD/JPY", direccion="ALCISTA_BASE", divisa_financiacion="JPY",
                       composicion=[{"divisa": "AUD", "peso": 1.0, "lado": "LARGO"}, {"divisa": "JPY", "peso": 1.0, "lado": "CORTO"}],
                       tipo_opcion="CRUCE", ambito={"incluye": "Cruce AUD/JPY", "excluye": "x"})
        self.assertBloquea(self.validar(p, desgloses={}), "G3-FX-03", "G10M")
        p["segmentos"]["EMEA"]["opciones"][0]["motivo_asignacion_segmento"] = "Motivo registrado por el Analizador en la prueba."
        self.assertEqual(self.comprobacion(self.validar(p, desgloses={}), "G3-FX-03")["resultado"], "ADVERTENCIA")

    def test_carry_incoherente(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["carry"]["signo"] = "a favor"
        self.assertBloquea(self.validar(p), "G3-FX-05", "incoherente")
        p = copy.deepcopy(self.paquete)
        self.op(p)["carry"]["diferencial_tipos_pct"] = -3.1
        self.assertBloquea(self.validar(p), "G3-FX-05", "diferencial")
        for campo, frag in (("ajustado_vol", "ajustado"), ("calc_id", "CALC-FX-"), ("anual_pct", "carry anual")):
            p = copy.deepcopy(self.paquete)
            del self.op(p)["carry"][campo]
            self.assertBloquea(self.validar(p), "G3-FX-05", frag)

    def test_referencias_ingenuas_y_tipo_de_rentabilidad(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["horizontes"]["H2"]["referencia"] = "forward"
        self.assertEqual(self.comprobacion(self.validar(p), "G3-FX-06")["resultado"], "ADVERTENCIA")
        p = copy.deepcopy(self.paquete)
        self.op(p, 1, "EMLA")["horizontes"]["H3"]["referencia"] = "paseo aleatorio"
        c = self.comprobacion(self.validar(p), "G3-FX-06")
        self.assertTrue(any("forward" in i["detalle"] for i in c["incidencias"]))
        p = copy.deepcopy(self.paquete)
        self.op(p, 0, "ESTR")["horizontes"]["H3"]["referencia"] = "paseo aleatorio"
        self.assertEqual(self.comprobacion(self.validar(p), "G3-FX-06")["resultado"], "ADVERTENCIA")
        p = copy.deepcopy(self.paquete)
        del self.op(p)["horizontes"]["H2"]["tipo_rentabilidad"]
        self.assertBloquea(self.validar(p), "G3-FX-11", "tipo_rentabilidad")
        p = copy.deepcopy(self.paquete)
        self.op(p)["horizontes"]["H2"]["divisa_medicion"] = None
        self.assertBloquea(self.validar(p), "G3-FX-11", "divisa de medición")

    def test_anticipacion_en_fijaciones(self):
        p = copy.deepcopy(self.paquete)
        p["paquete_para_bloque_B"][0]["niveles_referencia"]["nivel_actual"]["conocible_desde"] = "2026-11-03T15:30"
        self.assertBloquea(self.validar(p), "G3-FX-07", "anticipación")
        p = copy.deepcopy(self.paquete)
        del p["paquete_para_bloque_B"][0]["niveles_referencia"]["nivel_actual"]["hora_fijacion"]
        self.assertBloquea(self.validar(p), "G3-FX-07", "hora y zona")

    def test_capas_transversales(self):
        p = copy.deepcopy(self.paquete)
        del p["informes_transversales"]
        self.assertEqual(self.comprobacion(self.validar(p), "G3-FX-10")["resultado"], "ADVERTENCIA")
        p["informes_transversales"] = {"BCM": None, "PFV": None, "nota": "Se reutilizan los informes del ciclo anterior (GC0 sin cambio)."}
        self.assertOK(self.validar(p), "G3-FX-10")

    def test_no_se_proponen_instrumentos(self):
        casos = [("nombre", "Comprar un ETF de yenes frente al dólar", "instrumento"),
                 ("tesis", "La tesis se captura mejor con opciones call sobre el yen a 6 meses.", None),
                 ("tesis", "Proponemos operar mediante CFDs con apalancamiento de 10 veces.", "instrumento"),
                 ("tesis", "Nivel de entrada recomendado: 150,00; stop loss en 158.", "ejecución"),
                 ("tipo_opcion", "SECTOR", "Bloque A general"), ("tipo_opcion", "INSTRUMENTO", "instrumentos"),
                 ("instrumento", "Forward a 6 meses", "Bloque B"), ("apalancamiento", 5, "Bloque B"),
                 ("ambito", None, "ámbito"), ("indicador_seguimiento", None, "indicador de seguimiento"),
                 ("ejemplos_ilustrativos", ["ETF X"], "granularidad"), ("nombre", "Bono US0378331005", "ISIN")]
        for campo, valor, fragmento in casos:
            p = copy.deepcopy(self.paquete)
            if valor is None:
                del self.op(p)[campo]
            else:
                self.op(p)[campo] = valor
            self.assertBloquea(self.validar(p), "C15", fragmento)
        p = copy.deepcopy(self.paquete)
        p["paquete_para_bloque_B"][0]["consideraciones_implementacion"].append("Recomendamos utilizar futuros de CME para el par.")
        self.assertBloquea(self.validar(p), "C15", "instrumento")

    def test_citar_instrumentos_solo_para_invertibilidad_o_preguntas(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["convertibilidad"]["nota"] = "Existen futuros y opciones líquidos sobre el par: el mercado es invertible."
        p["paquete_para_bloque_B"][0]["preguntas_para_B"].append("¿Es preferible un forward o una opción con este carry negativo?")
        p["paquete_para_bloque_B"][0]["consideraciones_implementacion"].append("Existe un mercado de futuros y opciones muy líquido sobre el par.")
        self.assertOK(self.validar(p), "C15")

    def test_duplicado_en_dos_segmentos(self):
        p = copy.deepcopy(self.paquete)
        self.opcion_en(p, "ESTR", "OPP-FX-2026-0602", nombre="EUR/GBP ALCISTA (euro al alza frente a la libra)",
                       ambito={"incluye": "Otro ámbito distinto", "excluye": "nada"})
        self.assertBloquea(self.validar(p, desgloses={}), "C16", "nombre")
        p = copy.deepcopy(self.paquete)
        self.opcion_en(p, "EMEA", "OPP-FX-2026-0603", nombre="Otro nombre", ambito={"incluye": "Otro ámbito", "excluye": "x"})
        self.assertBloquea(self.validar(p, desgloses={}), "C16", "exposición")
        p = copy.deepcopy(self.paquete)
        self.opcion_en(p, "EMEA", "OPP-FX-2026-0007", nombre="Otra cosa", par="EUR/PLN", direccion="BAJISTA_BASE", divisa_financiacion="EUR",
                       composicion=[{"divisa": "EUR", "peso": 1.0, "lado": "CORTO"}, {"divisa": "PLN", "peso": 1.0, "lado": "LARGO"}],
                       ambito={"incluye": "Cruce EUR/PLN", "excluye": "x"})
        self.assertBloquea(self.validar(p, desgloses={}), "C16", "figura en G10N y en EMEA")

    def test_diversidad_del_segmento(self):
        p = copy.deepcopy(self.paquete)
        ops = p["segmentos"]["EMLA"]["opciones"]
        extra = copy.deepcopy(ops[0])
        extra.update({"opp_id": "OPP-FX-2026-0922", "rango": 3, "par": "USD/COP", "nombre": "USD/COP bajista",
                      "composicion": [{"divisa": "USD", "peso": 1.0, "lado": "CORTO"}, {"divisa": "COP", "peso": 1.0, "lado": "LARGO"}],
                      "ambito": {"incluye": "Tipo de cambio USD/COP", "excluye": "x"}})
        ops.append(extra)
        res = self.validar(p, desgloses={})
        self.assertBloquea(res, "C02", "clúster")
        self.assertBloquea(res, "G3-FX-09", "USD CORTO en 3 opciones")

    def test_exposicion_agregada(self):
        p = copy.deepcopy(self.paquete)
        p["exposicion_agregada"]["USD"] = "larga"
        self.assertBloquea(self.validar(p), "G3-FX-08", "neta corta")
        p = copy.deepcopy(self.paquete)
        p["exposicion_agregada"]["USD"] = "muy corta"
        self.assertBloquea(self.validar(p), "G3-FX-08", "no permitido")
        p = copy.deepcopy(self.paquete)
        del p["exposicion_agregada"]["MXN"]
        self.assertEqual(self.comprobacion(self.validar(p), "G3-FX-08")["resultado"], "ADVERTENCIA")
        p = copy.deepcopy(self.paquete)
        p["exposicion_agregada"] = {}
        self.assertBloquea(self.validar(p), "G3-FX-08", "ausente")

    def test_contradiccion_entre_segmentos_sin_justificar(self):
        # NZD es pata activa corta en G10M (AUD/NZD) y larga en el carry G10 de ESTR: contradicción real
        p = copy.deepcopy(self.paquete)
        p["contradicciones_entre_segmentos"] = [c for c in p["contradicciones_entre_segmentos"] if c["divisa"] != "NZD"]
        self.assertBloquea(self.validar(p), "G3-FX-08", "NZD como pata activa larga")
        # JPY largo en G10N (USD/JPY) y corto en ESTR solo como financiación del carry: no es contradicción (9.6.6)
        self.assertNotIn("JPY", [c["divisa"] for c in self.paquete["contradicciones_entre_segmentos"]])
        self.assertEqual(self.comprobacion(self.validar(self.paquete), "G3-FX-08")["resultado"], "OK")
        # Si el Analista declara el JPY como pata activa de la estrategia, sí lo es y exige justificación
        p = copy.deepcopy(self.paquete)
        self.op(p, 0, "ESTR")["pata_activa"] = ["JPY"]
        self.assertBloquea(self.validar(p), "G3-FX-08", "JPY como pata activa")

    def test_patas_activas(self):
        f = h.patas_activas
        par = lambda par_, d: {"tipo_opcion": "PAR", "par": par_, "composicion": [
            {"divisa": par_[:3], "peso": 1, "lado": "LARGO" if d == "A" else "CORTO"},
            {"divisa": par_[4:], "peso": 1, "lado": "CORTO" if d == "A" else "LARGO"}]}
        self.assertEqual(f(par("USD/JPY", "B")), {"JPY": "LARGO"})            # el USD es contrapartida
        self.assertEqual(f(par("USD/BRL", "A")), {"BRL": "CORTO"})
        self.assertEqual(f(par("EUR/PLN", "A")), {"PLN": "CORTO"})            # el EUR es contrapartida
        self.assertEqual(f(par("EUR/USD", "A")), {"EUR": "LARGO"})            # ambas contrapartidas: la larga
        self.assertEqual(f({**par("AUD/NZD", "A"), "tipo_opcion": "CRUCE"}), {"AUD": "LARGO", "NZD": "CORTO"})
        cesta = {"tipo_opcion": "CESTA", "divisa_financiacion": "EUR", "composicion": [
            {"divisa": "USD", "peso": 1, "lado": "LARGO"}, {"divisa": "EUR", "peso": 0.5, "lado": "CORTO"},
            {"divisa": "JPY", "peso": 0.5, "lado": "CORTO"}]}
        self.assertEqual(f(cesta), {"USD": "LARGO"})                          # dólar amplio: el USD es la tesis
        self.assertEqual(f({"tipo_opcion": "VOLATILIDAD", "composicion": []}), {})
        self.assertEqual(f({**cesta, "pata_activa": ["JPY"]}), {"JPY": "CORTO"})

    def test_encargo_para_bloque_b(self):
        for campo in ("consideraciones_implementacion", "carry_esperado", "metricas_clave", "preguntas_para_B", "indicador_seguimiento",
                      "ambito", "direccion", "composicion"):
            p = copy.deepcopy(self.paquete)
            del p["paquete_para_bloque_B"][0][campo]
            self.assertBloquea(self.validar(p), "C11", "ausente")
        p = copy.deepcopy(self.paquete)
        p["paquete_para_bloque_B"][0]["segmento"] = "G10M"
        self.assertBloquea(self.validar(p), "C11", "distinto")
        p = copy.deepcopy(self.paquete)
        p["paquete_para_bloque_B"][0]["direccion"] = "ALCISTA_BASE"
        self.assertBloquea(self.validar(p), "C11", "distinto")
        p = copy.deepcopy(self.paquete)
        p["paquete_para_bloque_B"][0]["pronosticos"] = ["PRG-FX-2026-0999"]
        self.assertEqual(self.comprobacion(self.validar(p), "C11")["resultado"], "ADVERTENCIA")


class TestV11HorizontePrincipalYH5(Base):
    """V1.1 (03/11/2026): regla de adecuación del horizonte (C17), H5 limitado con hitos (C18), supuestos (C19), R8."""

    def h5(self, p):
        return next(o for o in p["segmentos"]["G10N"]["opciones"] if o["opp_id"] == "OPP-FX-2026-0009")

    def test_ejemplo_tiene_h5_y_naturalezas(self):
        res = self.validar()
        for c in ("C17", "C18", "C19"):
            self.assertOK(res, c)
        o = self.h5(self.paquete)
        self.assertEqual((o["naturaleza_inversion"], o["horizonte_principal"]), ("ESTRUCTURAL", "H5"))
        self.assertGreaterEqual(len(o["horizontes"]["H5"]["hitos"]), 3)

    def test_naturaleza_ausente_o_liquidez(self):
        p = copy.deepcopy(self.paquete)
        self.op(p).pop("naturaleza_inversion")
        self.assertBloquea(self.validar(p), "C17", "Naturaleza de la inversión ausente")
        p = copy.deepcopy(self.paquete)
        self.op(p)["naturaleza_inversion"] = "LIQUIDEZ"
        self.assertBloquea(self.validar(p), "C17", "Bloque A general")

    def test_horizonte_principal_ausente_o_no_ofrecido(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["horizonte_principal"] = None
        self.assertBloquea(self.validar(p), "C17", "Horizonte principal ausente")
        p = copy.deepcopy(self.paquete)
        self.op(p)["horizonte_principal"] = "H4"
        self.assertBloquea(self.validar(p), "C17", "no figura entre los horizontes")

    def test_fuera_de_rango_sin_y_con_justificacion(self):
        p = copy.deepcopy(self.paquete)
        o = self.op(p)
        o["naturaleza_inversion"] = "TACTICA"   # H3 fuera de H1–H2
        self.assertBloquea(self.validar(p), "C17", "fuera del rango de la naturaleza TACTICA")
        o["justificacion_horizonte"] = "El evento decisivo (reunión del BoJ) cae a 7 semanas, pero la tesis se mide en H3"
        res = self.validar(p)
        self.assertEqual(res["dictamen"], "APTO_CON_ADVERTENCIAS")
        self.assertEqual(self.comprobacion(res, "C17")["resultado"], "ADVERTENCIA")

    def test_h5_con_naturaleza_no_estructural(self):
        p = copy.deepcopy(self.paquete)
        self.h5(p)["naturaleza_inversion"] = "CICLICA"
        res = self.validar(p)
        self.assertBloquea(res, "C18", "solo para naturaleza ESTRUCTURAL")
        self.assertBloquea(res, "C17", "exige naturaleza ESTRUCTURAL")

    def test_h5_fuera_de_ambito_con_probabilidad_o_sin_hitos(self):
        p = copy.deepcopy(self.paquete)
        o = self.h5(p)
        o["horizontes"]["H5"]["ambito_h5"] = "MOMENTUM"
        o["ambito_h5"] = None
        self.assertBloquea(self.validar(p), "C18", "fuera de los tres ámbitos")
        p = copy.deepcopy(self.paquete)
        self.h5(p)["horizontes"]["H5"]["prob"] = 0.6
        self.assertBloquea(self.validar(p), "C18", "probabilidad numérica")
        p = copy.deepcopy(self.paquete)
        self.h5(p)["horizontes"]["H5"]["hitos"] = self.h5(p)["horizontes"]["H5"]["hitos"][:2]
        self.assertBloquea(self.validar(p), "C18", "mínimo 3")

    def test_h5_espaciado_y_campos_de_hitos(self):
        p = copy.deepcopy(self.paquete)
        hs = self.h5(p)["horizontes"]["H5"]["hitos"]
        hs[0]["fecha"] = "2028-06-30"                      # primer hito a > 12 meses
        self.assertBloquea(self.validar(p), "C18", "Primer hito")
        p = copy.deepcopy(self.paquete)
        hs = self.h5(p)["horizontes"]["H5"]["hitos"]
        hs[2]["fecha"] = "2032-06-30"                      # > 24 meses entre hitos
        self.assertBloquea(self.validar(p), "C18", "meses entre los hitos")
        p = copy.deepcopy(self.paquete)
        hs = self.h5(p)["horizontes"]["H5"]["hitos"]
        hs[1]["criterio"] = ""
        hs[1]["hit_id"] = "HIT-2026-0002"
        res = self.validar(p)
        self.assertBloquea(res, "C18", "Campo del hito")
        self.assertBloquea(res, "C18", "HIT-FX-")

    def test_relevancia_alta_por_h5_principal(self):
        p = copy.deepcopy(self.paquete)
        self.h5(p)["relevancia_decisional"] = "MEDIA"
        self.assertBloquea(self.validar(p), "C10", "horizonte principal H5")

    def test_encargo_bloque_b_con_otro_horizonte_principal(self):
        p = copy.deepcopy(self.paquete)
        p["paquete_para_bloque_B"][0]["horizonte_principal"] = "H2"
        self.assertBloquea(self.validar(p), "C11", "horizonte principal")
        p = copy.deepcopy(self.paquete)
        p["paquete_para_bloque_B"][0].pop("horizonte_principal")
        self.assertBloquea(self.validar(p), "C11")

    def test_supuestos_declarados(self):
        p = copy.deepcopy(self.paquete)
        p["supuestos_declarados"] = []
        self.assertBloquea(self.validar(p), "C19", "CNS-FX-2026-0004")
        p = copy.deepcopy(self.paquete)
        p["supuestos_declarados"][0]["efecto_si_falso"] = ""
        p["supuestos_declarados"][0]["cns_id"] = "CNS-0004"
        res = self.validar(p)
        self.assertBloquea(res, "C19", "Campo ausente o vacío")
        self.assertBloquea(res, "C19", "CNS-FX-AAAA-NNNN")

    def test_valor_de_credencial_bloquea_alias_no(self):
        p = copy.deepcopy(self.paquete)
        p["limitaciones"].append({"credencial_ref": "vault://ht01/vol-fx-prov", "estado": "PROVISTA"})
        self.assertOK(self.validar(p), "C13")
        p["limitaciones"].append({"clave_api": "abc123def456ghi"})
        self.assertBloquea(self.validar(p), "C13", "Valor de credencial")


class TestV11Seguimiento(unittest.TestCase):
    """Informe de seguimiento de opción (ciclo C6, 14.4 y Anexo B V1.1)."""

    def setUp(self):
        self.inf = {"seg_id": "SEG-FX-2026-0003", "opp_id": "OPP-FX-2026-0106", "run_id": "RUN-FX-2026-0071", "ciclo": 2,
                    "fecha": "2026-12-01", "segmento": "G10N", "par": "USD/JPY", "direccion": "BAJISTA_BASE",
                    "horizonte_principal": "H3", "sin_novedad": False, "semaforo": "VERDE",
                    "que_ha_cambiado": ["USD/JPY cae un 1,8 % en la semana"],
                    "senales_interes": [{"senal": "USD/JPY por debajo de 140", "estado": "no activada (143,2)"}],
                    "invalidacion": [{"condicion": "USD/JPY > 158,5", "distancia": "10 %", "activada": False}],
                    "catalizadores": [{"evento": "Reunión del BoJ", "fecha": "2026-12-18", "estado": "PENDIENTE"}],
                    "puntuaciones": {"T": 60, "E": 65, "A": 62, "RK": 63, "variacion_RK": 5, "elegible": True, "fuente": "HT-03"},
                    "carry": {"anual_pct": -2.8, "signo": "en contra"},
                    "pronosticos_abiertos": [{"prg_id": "PRG-FX-2026-0301", "horizonte": "H3", "estado": "EN_CURSO", "hitos": []}],
                    "recomendacion": "MANTENER_VIGILANCIA", "motivo": "Sin cambio material en la tesis",
                    "sugerir_profundizacion_N3": False, "paquete_para_bloque_B": None, "supuestos_declarados": [],
                    "limitaciones": []}

    def test_apto(self):
        self.assertEqual(h.validar_seguimiento(self.inf)["dictamen"], "APTO")

    def test_ejemplo_de_plantillas_apto(self):
        # El mismo ejemplo está en 06_Plantillas_entregables (Ejemplo - Informe de seguimiento de opción - V1.1)
        self.assertEqual(h.validar_seguimiento(cargar("informe_seguimiento_ejemplo.json"))["dictamen"], "APTO")

    def test_vocabularios_y_prefijos(self):
        i = copy.deepcopy(self.inf)
        i["semaforo"], i["recomendacion"], i["seg_id"] = "AZUL", "COMPRAR", "SEG-2026-3"
        r = h.validar_seguimiento(i)
        self.assertEqual(r["dictamen"], "BLOQUEADO")
        det = " ".join(x["detalle"] for c in r["comprobaciones"] for x in c["incidencias"])
        for frag in ("AZUL", "COMPRAR", "SEG-FX-"):
            self.assertIn(frag, det)

    def test_envio_a_b_exige_elegibilidad_y_paquete(self):
        i = copy.deepcopy(self.inf)
        i["recomendacion"] = "PROPONER_ENVIO_A_B"
        i["puntuaciones"]["elegible"] = False
        r = h.validar_seguimiento(i)
        s02 = next(c for c in r["comprobaciones"] if c["id"] == "S02")
        self.assertEqual(s02["resultado"], "BLOQUEO")
        self.assertEqual(len(s02["incidencias"]), 2)

    def test_no_congela_pronosticos_ni_h5_sin_hitos(self):
        i = copy.deepcopy(self.inf)
        i["pronosticos_abiertos"] = [{"prg_id": "PRG-FX-2026-0400", "horizonte": "H5", "nuevo": True}]
        r = h.validar_seguimiento(i)
        s04 = next(c for c in r["comprobaciones"] if c["id"] == "S04")
        self.assertEqual(len(s04["incidencias"]), 2)

    def test_credencial_y_texto_largo(self):
        i = copy.deepcopy(self.inf)
        i["limitaciones"] = [{"token": "abcdefghijklmnop"}]
        self.assertEqual(h.validar_seguimiento(i)["dictamen"], "BLOQUEADO")
        r = h.validar_seguimiento(self.inf, texto="palabra " * 320)
        self.assertEqual(r["dictamen"], "APTO_CON_ADVERTENCIAS")

    def test_cli_seguimiento(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = os.path.join(d, "seg.json")
            with open(ruta, "w", encoding="utf-8") as fh:
                json.dump(self.inf, fh)
            self.assertEqual(h.main([ruta, "--seguimiento"]), 0)


class TestCLI(Base):
    def test_codigos_de_salida(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "r.json")
            base = [os.path.join(EJ, "paquete_oportunidades_ejemplo.json"), "--salida", out]
            completo = base + ["--certificados", os.path.join(EJ, "certificados_ejemplo.json"),
                               "--informe-visual", self.informe, "--desgloses", os.path.join(EJ, "desgloses_ejemplo.json"),
                               "--trazas", os.path.join(EJ, "trazas_ejemplo.json"),
                               "--artefactos", os.path.join(EJ, "artefactos_ejemplo.json")]
            self.assertEqual(h.main(completo), 0)
            self.assertEqual(h.main(completo[:-6]), 1)  # sin desgloses: C04 solo reconstruye RK → advertencia
            self.assertEqual(h.main(base), 2)
            with open(out, encoding="utf-8") as fh:
                self.assertEqual(json.load(fh)["dictamen"], "BLOQUEADO")
            malo = os.path.join(d, "malo.json")
            with open(malo, "w") as fh:
                fh.write("{no es json")
            self.assertEqual(h.main([malo]), 3)


if __name__ == "__main__":
    unittest.main()
