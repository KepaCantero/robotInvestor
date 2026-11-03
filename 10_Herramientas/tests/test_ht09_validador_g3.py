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
        self.assertEqual(len(res["comprobaciones"]), 19)
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
        self.assertEqual(h.TABLA_HORIZONTES["FON"], {"H1": "NO", "H2": "LIMITADO", "H3": "SI", "H4": "SI", "H5": "LIMITADO"})
        self.assertEqual(h.TABLA_HORIZONTES["DER"]["H4"], "NO")
        self.assertEqual(h.TABLA_HORIZONTES["MON"], {"H1": "LIMITADO", "H2": "SI", "H3": "SI", "H4": "NO", "H5": "NO"})
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


class TestV51(Base):
    """V5.1: horizonte principal y naturaleza de la inversión (C17), H5 con hitos (C18), supuestos declarados (C19),
    informe de seguimiento de opción (validar_seguimiento)."""

    def h5(self, p):
        return self.op(p, 1)["horizontes"]["H5"]

    def test_tabla_h5(self):
        self.assertEqual(h.HORIZONTES, ("H1", "H2", "H3", "H4", "H5"))
        self.assertEqual({k: v["H5"] for k, v in h.TABLA_HORIZONTES.items()},
                         {"RV": "SI", "RF": "LIMITADO", "DIV": "LIMITADO", "MP": "SI", "IDX": "SI", "FON": "LIMITADO",
                          "DER": "NO", "INM": "LIMITADO", "CRI": "LIMITADO", "ALT": "SI", "MON": "NO", "TCV": "NO"})
        self.assertEqual(h.NATURALEZAS["ESTRUCTURAL"], ("H4", "H5"))
        self.assertEqual(h.NATURALEZAS["TACTICA"], ("H1", "H2"))

    def test_horizonte_principal_obligatorio(self):
        for campo in ("horizonte_principal", "naturaleza_inversion"):
            p = copy.deepcopy(self.paquete)
            del self.op(p)[campo]
            self.assertBloquea(self.validar(p), "C17", "ausente")

    def test_principal_no_ofrecido_o_desconocido(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["horizonte_principal"] = "H4"
        self.assertBloquea(self.validar(p), "C17", "no figura")
        p = copy.deepcopy(self.paquete)
        self.op(p)["horizonte_principal"] = "H9"
        self.assertBloquea(self.validar(p), "C17", "desconocido")
        p = copy.deepcopy(self.paquete)
        self.op(p)["naturaleza_inversion"] = "ESPECULATIVA"
        self.assertBloquea(self.validar(p), "C17", "no permitido")

    def test_fuera_de_rango_sin_y_con_justificacion(self):
        p = copy.deepcopy(self.paquete)
        self.op(p)["naturaleza_inversion"] = "TACTICA"      # principal H3 fuera de H1–H2
        self.assertBloquea(self.validar(p), "C17", "fuera del rango H1–H2")
        self.op(p)["justificacion_horizonte"] = "Catalizador táctico identificado: resultados del 4T."
        res = self.validar(p)
        self.assertEqual(self.comprobacion(res, "C17")["resultado"], "ADVERTENCIA")
        self.assertEqual(res["dictamen"], "APTO_CON_ADVERTENCIAS")

    def test_principal_en_celda_no(self):
        p = copy.deepcopy(self.paquete)
        TestV5.opcion_en(self, p, "DER", "OPP-2026-0610", nombre="Prima de varianza en índices europeos",
                         naturaleza_inversion="ESTRUCTURAL", horizonte_principal="H5",
                         horizontes={"H5": {"vista": "alcista", "banda": "incierto", "prob": None, "prg_id": "PRG-2026-0910"}})
        res = self.validar(p, desgloses={})
        self.assertBloquea(res, "C17", "celda «No»")
        self.assertBloquea(res, "C06", "no aplicable a DER")

    def test_principal_limitado_sin_catalizador(self):
        p = copy.deepcopy(self.paquete)
        o = TestV5.opcion_en(self, p, "FON", "OPP-2026-0611", nombre="Cambio estructural hacia ETF activos",
                             naturaleza_inversion="ESTRUCTURAL", horizonte_principal="H5", catalizadores=[],
                             justificacion_horizonte="Tesis estructural sin catalizador fechado: aplicabilidad limitada declarada",
                             horizontes={"H5": copy.deepcopy(self.h5(self.paquete))})
        res = self.validar(p, desgloses={})
        c17 = self.comprobacion(res, "C17")
        self.assertEqual(c17["resultado"], "ADVERTENCIA", c17)
        self.assertTrue(any("limitado" in i["detalle"] for i in c17["incidencias"]))
        self.assertEqual(self.comprobacion(res, "C06")["resultado"], "ADVERTENCIA")
        o["justificacion_horizonte"] = None
        self.assertBloquea(self.validar(p, desgloses={}), "C06", "catalizador identificado o justificación")

    def test_h5_relevancia_alta(self):
        op_h5 = {"puntuaciones": {}, "horizonte_principal": "H5", "horizontes": {"H5": {"prg_id": "PRG-1"}}}
        self.assertEqual(h.relevancia_esperada_alta(op_h5, "RV", True, {}), ["horizonte principal H5"])

    def test_h5_valido_en_ejemplo(self):
        res = self.validar()
        self.assertEqual(self.comprobacion(res, "C18")["resultado"], "OK")

    def test_h5_con_probabilidad_numerica(self):
        p = copy.deepcopy(self.paquete)
        self.h5(p)["prob"] = 0.7
        self.assertBloquea(self.validar(p), "C18", "siempre cualitativa")

    def test_h5_sin_hitos_o_insuficientes(self):
        p = copy.deepcopy(self.paquete)
        self.h5(p)["hitos"] = []
        self.assertBloquea(self.validar(p), "C18", "sin hitos")
        p = copy.deepcopy(self.paquete)
        self.h5(p)["hitos"] = self.h5(p)["hitos"][:2]
        self.assertBloquea(self.validar(p), "C18", "< 3")
        p = copy.deepcopy(self.paquete)
        del self.h5(p)["hitos"][0]["criterio"]
        self.assertBloquea(self.validar(p), "C18", "obligatorios")
        p = copy.deepcopy(self.paquete)
        self.h5(p)["hitos"][1]["hit_id"] = "H-2"
        self.assertBloquea(self.validar(p), "C18", "HIT-")

    def test_h5_espaciado_de_hitos(self):
        p = copy.deepcopy(self.paquete)
        self.h5(p)["hitos"][0]["fecha"] = "2028-06-30"   # primer hito a ~20 meses
        self.h5(p)["hitos"][2]["fecha"] = "2034-03-31"   # 60 meses tras el segundo
        c18 = self.comprobacion(self.validar(p), "C18")
        self.assertEqual(c18["resultado"], "ADVERTENCIA", c18)
        self.assertEqual(len(c18["incidencias"]), 2)

    def test_h5_certificado_no_habilita_probabilidad(self):
        p = copy.deepcopy(self.paquete)
        self.h5(p)["prob"] = 0.6
        certs = self.certs + [{"clase": "RV", "horizonte": "H5", "vigente": True}]
        self.assertBloquea(self.validar(p, certificados=certs), "C18")

    def test_supuestos_declarados(self):
        p = copy.deepcopy(self.paquete)
        p["supuestos_declarados"][0]["cns_id"] = None
        self.assertBloquea(self.validar(p), "C19", "CNS-")
        p["supuestos_declarados"] = "texto"
        self.assertBloquea(self.validar(p), "C19", "lista")
        p = copy.deepcopy(self.paquete)
        del p["supuestos_declarados"][0]["efecto_si_falso"]
        self.assertEqual(self.comprobacion(self.validar(p), "C19")["resultado"], "ADVERTENCIA")

    def test_valor_de_credencial(self):
        p = copy.deepcopy(self.paquete)
        p["limitaciones"].append('{"valor_credencial": "abc123"}')
        p["x"] = {"valor_credencial": "abc123"}
        self.assertBloquea(self.validar(p), "C13")

    def test_bloque_b_horizonte_principal(self):
        p = copy.deepcopy(self.paquete)
        p["paquete_para_bloque_B"][0]["horizonte_principal"] = "H2"
        self.assertBloquea(self.validar(p), "C11", "horizonte principal")
        p = copy.deepcopy(self.paquete)
        del p["paquete_para_bloque_B"][0]["horizonte_principal"]
        self.assertBloquea(self.validar(p), "C11", "ausente")

    # Informe de seguimiento de opción (ciclo C6, 14.4)
    def seguimiento(self, **kw):
        s = {"seg_id": "SEG-2026-0007", "opp_id": "OPP-2026-0011", "run_id": "RUN-2026-0201", "ciclo": 3, "fecha": "2026-11-23",
             "tipo_activo": "RV", "horizonte_principal": "H3", "sin_novedad": False, "semaforo": "VERDE",
             "que_ha_cambiado": ["Revisiones de beneficios al alza en el segmento"],
             "senales_interes": [{"senal": "PMI de la zona euro", "estado": "por debajo de 50"}],
             "invalidacion": [{"condicion": "Rentabilidad relativa < −5 % en 3 meses", "distancia": "7 pp", "activada": False}],
             "catalizadores": [{"evento": "PMI zona euro", "fecha": "2026-12-01", "estado": "PENDIENTE"}],
             "puntuaciones": {"T": 60, "E": 65, "A": 60, "RK": 62, "variacion_RK": 5, "elegible": True},
             "pronosticos_abiertos": [{"prg_id": "PRG-2026-0103", "horizonte": "H3", "estado": "EN_CURSO", "hitos": []},
                                      {"prg_id": "PRG-2026-0104", "horizonte": "H5", "estado": "EN_CURSO_CONFORME",
                                       "hitos": [{"hit_id": "HIT-2026-0001", "estado": "PENDIENTE"}]}],
             "recomendacion": "MANTENER_VIGILANCIA", "motivo": "Mejora sin catalizador inmediato.",
             "sugerir_profundizacion_N3": False, "paquete_para_bloque_B": None, "supuestos_declarados": [], "limitaciones": []}
        s.update(kw)
        return s

    def test_seguimiento_apto(self):
        res = h.validar_seguimiento(self.seguimiento())
        self.assertEqual(res["dictamen"], "APTO", res["comprobaciones"])
        self.assertTrue(res["elegible_recalculado"])

    def test_seguimiento_envio_a_b(self):
        res = h.validar_seguimiento(self.seguimiento(recomendacion="PROPONER_ENVIO_A_B"))
        self.assertEqual(res["dictamen"], "BLOQUEADO")
        self.assertIn("paquete_para_bloque_B", json.dumps(res["comprobaciones"], ensure_ascii=False))
        ok = h.validar_seguimiento(self.seguimiento(recomendacion="PROPONER_ENVIO_A_B",
                                                    paquete_para_bloque_B={"opp_id": "OPP-2026-0011", "horizonte_principal": "H3"}))
        self.assertEqual(ok["dictamen"], "APTO")
        no_eleg = h.validar_seguimiento(self.seguimiento(
            recomendacion="PROPONER_ENVIO_A_B", paquete_para_bloque_B={"opp_id": "OPP-2026-0011"},
            puntuaciones={"T": 60, "E": 55, "A": 60, "RK": 59, "elegible": False}))
        self.assertEqual(no_eleg["dictamen"], "BLOQUEADO")

    def test_seguimiento_valores_y_rk(self):
        self.assertEqual(h.validar_seguimiento(self.seguimiento(recomendacion="VENDER"))["dictamen"], "BLOQUEADO")
        self.assertEqual(h.validar_seguimiento(self.seguimiento(semaforo="GRIS"))["dictamen"], "BLOQUEADO")
        malo = self.seguimiento(puntuaciones={"T": 60, "E": 65, "A": 60, "RK": 70, "elegible": True})
        self.assertEqual(h.validar_seguimiento(malo)["dictamen"], "BLOQUEADO")
        sin_hitos = self.seguimiento()
        sin_hitos["pronosticos_abiertos"][1]["hitos"] = []
        self.assertEqual(h.validar_seguimiento(sin_hitos)["dictamen"], "BLOQUEADO")

    def test_seguimiento_brevedad_y_credenciales(self):
        res = h.validar_seguimiento(self.seguimiento(), texto_breve="palabra " * 320)
        self.assertEqual(res["dictamen"], "APTO_CON_ADVERTENCIAS")
        res = h.validar_seguimiento(self.seguimiento(limitaciones=['"api_key": "sk-ABCDEFGHIJKLMNOPQRSTUVWX12"']))
        self.assertEqual(res["dictamen"], "BLOQUEADO")


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
            seg = os.path.join(d, "seg.json")
            with open(seg, "w", encoding="utf-8") as fh:
                json.dump(TestV51.seguimiento(self), fh, ensure_ascii=False)
            self.assertEqual(h.main([seg, "--seguimiento", "--salida", out]), 0)


if __name__ == "__main__":
    unittest.main()
