# -*- coding: utf-8 -*-
"""Pruebas unitarias de HT-09 (validador determinista G3)."""
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

    def op(self, p, i=0, clase="RV"):
        return p["clases"][clase]["opciones"][i]

    def comprobacion(self, res, cid):
        return next(c for c in res["comprobaciones"] if c["id"] == cid)

    def assertBloquea(self, res, cid, fragmento=None):
        self.assertEqual(res["dictamen"], "BLOQUEADO")
        c = self.comprobacion(res, cid)
        self.assertEqual(c["resultado"], "BLOQUEO", c)
        if fragmento:
            self.assertTrue(any(fragmento in i["detalle"] for i in c["incidencias"]), c["incidencias"])


class TestEjemplo(Base):
    def test_ejemplo_completo_apto(self):
        res = self.validar()
        self.assertEqual(res["dictamen"], "APTO", [c for c in res["comprobaciones"] if c["resultado"] != "OK"])
        self.assertEqual(len(res["comprobaciones"]), 16)
        self.assertGreaterEqual(self.comprobacion(res, "C12")["datos"]["fernandez_huerta"], 70)

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
        res = self.validar(p)
        self.assertBloquea(res, "C01", "ausente")

    def test_valores_no_permitidos(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["confianza"] = "segurísimo"
        self.op(p)["riesgo_1a5"] = 7
        p["clases"]["RV"]["estado_semaforo"] = "ROJO"
        self.assertBloquea(self.validar(p), "C01", "no permitido")

    def test_mas_de_tres(self):
        p = copy.deepcopy(self.paquete)
        ops = p["clases"]["RV"]["opciones"]
        for k in range(2):
            extra = copy.deepcopy(ops[1])
            extra["opp_id"] = f"OPP-2026-09{k}0"
            extra["rango"] = 3 + k
            ops.append(extra)
        self.assertBloquea(self.validar(p), "C02", "máximo 3")

    def test_rangos(self):
        p = copy.deepcopy(self.paquete)
        self.op(p, 1)["rango"] = 1
        self.assertBloquea(self.validar(p), "C02")

    def test_menos_de_tres_sin_motivo(self):
        p = copy.deepcopy(self.paquete)
        p["clases"]["RF"]["menos_de_tres_motivo"] = None
        self.assertBloquea(self.validar(p), "C03")

    def test_rk_no_reconstruible(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["puntuaciones"]["RK"] = 75
        self.assertBloquea(self.validar(p, desgloses={}), "C04", "RK declarado 75")

    def test_desglose_discrepante(self):
        d = copy.deepcopy(self.desgloses)
        d["OPP-2026-0007"]["dimensiones"]["A"]["asimetria"] = 100
        self.assertBloquea(self.validar(desgloses=d), "C04", "HT-03")

    def test_total_no_multiplo_de_5(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["puntuaciones"]["M"] = 52
        self.assertBloquea(self.validar(p), "C04", "múltiplo de 5")

    def test_elegibilidad(self):
        p = copy.deepcopy(self.paquete)
        self.op(p, 1)["puntuaciones"].update({"E": 55, "RK": 64})
        self.assertBloquea(self.validar(p, desgloses={}), "C05", "E=55 < 60")

    def test_puerta_ps(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["puertas"]["PS3"] = False
        self.assertBloquea(self.validar(p), "C05", "PS3")

    def test_banda_marginal_desde_desglose(self):
        d = copy.deepcopy(self.desgloses)
        p = copy.deepcopy(self.paquete)
        d["OPP-2026-0011"]["dimensiones"]["E"] = {k: 60 for k in d["OPP-2026-0011"]["dimensiones"]["E"]}
        self.op(p, 1)["puntuaciones"].update({"E": 60, "RK": 62})
        self.assertBloquea(self.validar(p, desgloses=d), "C05", "PS8")

    def test_horizonte_no_aplicable(self):
        p = copy.deepcopy(self.paquete)
        alt = copy.deepcopy(self.op(p, 1))
        alt.update({"opp_id": "OPP-2026-0500", "rango": 1, "relevancia_decisional": "ALTA"})
        alt["horizontes"] = {"H1": {"vista": "alcista", "banda": "incierto", "prob": None, "prg_id": "PRG-2026-0900"}}
        p["clases"]["ALT"] = {"estado_semaforo": "AMBAR", "regimen_clase": "…x", "candidatas_analizadas": 3,
                              "opciones": [alt], "menos_de_tres_motivo": "Solo una elegible."}
        self.assertBloquea(self.validar(p, desgloses={}), "C06", "no aplicable a ALT")

    def test_horizonte_limitado_sin_catalizador(self):
        p = copy.deepcopy(self.paquete)
        o = self.op(p)
        o["catalizadores"] = []
        o["horizontes"]["H1"] = {"vista": "alcista", "banda": "incierto", "prob": None, "prg_id": "PRG-2026-0999",
                                 "advertencia": "Menor fiabilidad"}
        self.assertBloquea(self.validar(p), "C06", "exige catalizador")

    def test_horizonte_sin_prg(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["horizontes"]["H2"]["prg_id"] = None
        self.assertBloquea(self.validar(p), "C06", "PRG-")

    def test_probabilidad_sin_certificado(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["horizontes"]["H2"]["prob"] = 0.55
        self.assertBloquea(self.validar(p), "C07", "RV×H2")

    def test_certificado_no_vigente(self):
        certs = [dict(self.certs[0], vigente=False)]
        self.assertBloquea(self.validar(certificados=certs), "C07")

    def test_evidencias_y_calculos(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["evidencias"] = []
        self.op(p, 1)["calculos"] = ["CALC-2026-7777"]
        res = self.validar(p)
        self.assertBloquea(res, "C08", "Sin evidencias")
        self.assertTrue(any("CALC-2026-7777" in i["detalle"] for i in self.comprobacion(res, "C08")["incidencias"]))

    def test_traza_clm_sin_evd(self):
        trazas = {"CLM-2026-0101": ["EVD-2026-0200"]}  # falta CLM-2026-0102
        self.assertBloquea(self.validar(trazas=trazas), "C08", "CLM-2026-0102")

    def test_objecion_fuerte_sin_resolver(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["objeciones"].append({"fuerza": "fuerte", "resumen": "Riesgo regulatorio inminente", "respuesta": ""})
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

    def test_relevancia_atractiva_pero_incierta(self):
        self.assertEqual(h.relevancia_esperada_alta({"puntuaciones": {"E": 65, "A": 75}}, "RV", True, {}),
                         ["E 65 < 70 con A 75 ≥ 75 (atractiva pero incierta)"])
        self.assertTrue(h.relevancia_esperada_alta({"puntuaciones": {}}, "CRI", False, {}))
        self.assertFalse(h.relevancia_esperada_alta({"puntuaciones": {}}, "CRI", True, {}))
        op_h4 = {"puntuaciones": {}, "liquidez": "baja", "horizontes": {"H4": {"prg_id": "PRG-1"}}}
        self.assertEqual(h.relevancia_esperada_alta(op_h4, "INM", True, {}), ["horizonte H4 con iliquidez"])

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
                     "perturbaciones macroeconómicas internacionales sobre determinadas valoraciones patrimoniales.</p>")
        try:
            self.assertBloquea(self.validar(informe_visual=fh.name), "C12", "Fernández-Huerta")
        finally:
            os.unlink(fh.name)
        self.assertBloquea(self.validar(informe_visual="/no/existe.html"), "C12")

    def test_credenciales(self):
        p = copy.deepcopy(self.paquete)
        p["limitaciones"].append('api_key: "sk-ABCDEFGHIJKLMNOPQRSTUVWX123"')
        self.assertBloquea(self.validar(p), "C13")


class TestV5(Base):
    """Doce tipos, tabla 8.3 V5.0, PS3 invertibilidad del ámbito, frontera con el Bloque B y duplicados entre tipos."""

    def opcion_en(self, p, tipo, oid, horizontes=None, **kw):
        o = copy.deepcopy(self.op(p, 1))
        o.update({"opp_id": oid, "rango": 1, "tipo_activo": tipo, "relevancia_decisional": "MEDIA"})
        o.update(kw)
        if horizontes is not None:
            o["horizontes"] = horizontes
        p["clases"][tipo] = {"estado_semaforo": "AMBAR", "regimen_clase": "Régimen de prueba del tipo.", "candidatas_analizadas": 3,
                             "opciones": [o], "menos_de_tres_motivo": "Solo una elegible en la prueba."}
        return o

    def test_doce_tipos_y_tabla_8_3(self):
        self.assertEqual(h.CLASES, ("RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV"))
        self.assertEqual(set(h.TABLA_HORIZONTES), set(h.CLASES))
        self.assertEqual(h.TABLA_HORIZONTES["FON"], {"H1": "NO", "H2": "LIMITADO", "H3": "SI", "H4": "SI"})
        self.assertEqual(h.TABLA_HORIZONTES["DER"]["H4"], "NO")
        self.assertEqual(h.TABLA_HORIZONTES["MON"], {"H1": "LIMITADO", "H2": "SI", "H3": "SI", "H4": "NO"})
        self.assertEqual(h.TABLA_HORIZONTES["INM"]["H1"], "NO")
        self.assertEqual(h.TABLA_HORIZONTES["TCV"]["H4"], "LIMITADO")
        self.assertEqual(h.TABLA_HORIZONTES["IDX"]["H1"], "LIMITADO")

    def test_tipo_nuevo_valido(self):
        p = copy.deepcopy(self.paquete)
        self.opcion_en(p, "MON", "OPP-2026-0600", nombre="Letras de la zona del euro a 6–12 meses",
                       ambito={"incluye": "Letras del Tesoro de la zona del euro a 6–12 meses", "excluye": "Bonos a más de 12 meses",
                               "region": "Zona del euro"})
        res = self.validar(p, desgloses={})
        self.assertNotEqual(self.comprobacion(res, "C01")["resultado"], "BLOQUEO", self.comprobacion(res, "C01"))
        self.assertEqual(self.comprobacion(res, "C15")["resultado"], "OK")
        self.assertEqual(self.comprobacion(res, "C16")["resultado"], "OK")

    def test_horizontes_no_de_los_tipos_nuevos(self):
        for tipo, hz in (("FON", "H1"), ("DER", "H4"), ("MON", "H4")):
            p = copy.deepcopy(self.paquete)
            self.opcion_en(p, tipo, "OPP-2026-0601", nombre=f"Prueba {tipo}",
                           horizontes={hz: {"vista": "alcista", "banda": "incierto", "prob": None, "prg_id": "PRG-2026-0901",
                                            "advertencia": "Menor fiabilidad"}})
            self.assertBloquea(self.validar(p, desgloses={}), "C06", f"no aplicable a {tipo}")

    def test_tipo_activo_incoherente(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["tipo_activo"] = "IDX"
        self.assertBloquea(self.validar(p), "C01", "tipo_activo")

    def test_ps3_invertibilidad_del_ambito(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["invertibilidad"]["universo_suficiente"] = False
        self.assertBloquea(self.validar(p), "C05", "PS3")

    def test_seleccion_de_activo_concreto(self):
        casos = [("tipo_opcion", "INSTRUMENTO_GENERICO", "granularidad"), ("tipo_opcion", "INDUSTRIA", "SUBSECTOR"),
                 ("ambito", None, "ámbito"), ("indicador_seguimiento", None, "indicador de seguimiento"),
                 ("vehiculos_genericos", ["ETF UCITS de bancos"], "retirado"), ("nombre", "Acción US0378331005", "ISIN")]
        for campo, valor, fragmento in casos:
            p = copy.deepcopy(self.paquete)
            if valor is None:
                del self.op(p)[campo]
            else:
                self.op(p)[campo] = valor
            self.assertBloquea(self.validar(p), "C15", fragmento)
        p = copy.deepcopy(self.paquete)
        self.op(p)["ambito"]["excluye"] = ""
        self.assertBloquea(self.validar(p), "C15", "incompleta")
        p = copy.deepcopy(self.paquete)
        p["paquete_para_bloque_B"][0]["vehiculos_genericos"] = ["ETF"]
        self.assertBloquea(self.validar(p), "C15", "retirado")

    def test_ejemplos_ilustrativos_permitidos(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["ejemplos_ilustrativos"] = ["Grandes bancos minoristas españoles (ilustración)", "US0378331005"]
        self.assertEqual(self.comprobacion(self.validar(p), "C15")["resultado"], "OK")

    def test_duplicado_en_dos_tipos_por_nombre(self):
        p = copy.deepcopy(self.paquete)
        self.opcion_en(p, "IDX", "OPP-2026-0602", nombre="BANCOS europeos", ambito={"incluye": "Otro ámbito distinto",
                                                                                   "excluye": "nada", "region": "Europa"})
        self.assertBloquea(self.validar(p, desgloses={}), "C16", "nombre")

    def test_duplicado_en_dos_tipos_por_ambito(self):
        p = copy.deepcopy(self.paquete)
        amb = copy.deepcopy(self.op(p)["ambito"])
        amb["incluye"] = amb["incluye"].upper() + "."
        self.opcion_en(p, "FON", "OPP-2026-0603", nombre="Otro nombre", ambito=amb)
        res = self.validar(p, desgloses={})
        self.assertBloquea(res, "C16", "ámbito")

    def test_mismo_opp_id_en_dos_tipos(self):
        p = copy.deepcopy(self.paquete)
        self.opcion_en(p, "TCV", "OPP-2026-0007", nombre="Otra cosa", ambito={"incluye": "Pendiente de la curva", "excluye": "x",
                                                                            "region": "Zona del euro"})
        self.assertBloquea(self.validar(p, desgloses={}), "C16", "figura en RV y en TCV")

    def test_encargo_para_bloque_b(self):
        for campo in ("criterios_seleccion_sugeridos", "metricas_clave", "preguntas_para_B", "indicador_seguimiento", "ambito"):
            p = copy.deepcopy(self.paquete)
            del p["paquete_para_bloque_B"][0][campo]
            self.assertBloquea(self.validar(p), "C11", "ausente")
        p = copy.deepcopy(self.paquete)
        p["paquete_para_bloque_B"][0]["tipo_activo"] = "RF"
        self.assertBloquea(self.validar(p), "C11", "distinto")
        p = copy.deepcopy(self.paquete)
        p["paquete_para_bloque_B"][0]["pronosticos"] = ["PRG-2026-0999"]
        self.assertEqual(self.comprobacion(self.validar(p), "C11")["resultado"], "ADVERTENCIA")


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
