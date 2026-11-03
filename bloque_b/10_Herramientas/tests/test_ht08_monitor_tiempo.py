# -*- coding: utf-8 -*-
"""Pruebas de HT-08 (modelo de tiempos, PT30, PTA, opciones, política automática, puntos de control)."""
import json
import os
import sys
import tempfile
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, RAIZ)

import ht03_puntuaciones as h3  # noqa: E402
import ht08_monitor_tiempo as h  # noqa: E402


def plan(nivel="N2", tipos=("RV",), obj="SECTOR"):
    e = h3.estrategia(obj, "H3", list(tipos)[:1], nivel)
    return {"nivel": nivel, "profundidad": e["profundidad"], "pesos": e["pesos_efectivos"],
            "especialistas_activos": [a for a, v in e["activacion"].items() if v["activo"]],
            "tipos_activo": list(tipos), "universo_por_tipo": {t: 40 for t in tipos}}


class TestModelo(unittest.TestCase):
    def test_niveles_ordenados(self):
        n1 = h.estimar(plan("N1"))["minutos_p80"]
        n2 = h.estimar(plan("N2"))["minutos_p80"]
        n3 = h.estimar(plan("N3", ("RV", "FON", "RF")))["minutos_p80"]
        self.assertLess(n1, n2)
        self.assertLess(n2, n3)
        self.assertLessEqual(n2, 30)   # N2 de un tipo cabe en 30 min con el modelo inicial
        self.assertGreater(h.estimar(plan("N2", ("RV", "FON", "RF")))["minutos_p80"], 30)

    def test_p80(self):
        e = h.estimar(plan())
        self.assertAlmostEqual(e["minutos_p80"], round(e["minutos_p50"] * 1.2, 1), places=0)
        self.assertEqual(set(e["desglose_por_fase"]), set(h.FASES))

    def test_fases_restantes(self):
        e = h.estimar(plan(), fases=["F8", "F9", "F10"])
        self.assertEqual(set(e["desglose_por_fase"]), {"F8", "F9", "F10"})
        self.assertLess(e["minutos_p50"], h.estimar(plan())["minutos_p50"])

    def test_paralelismo_f4_f5(self):
        p = plan()
        d = h.estimar(p)["desglose_por_fase"]
        total = sum(v for k, v in d.items() if k not in ("F4", "F5")) + max(d["F4"], d["F5"])
        self.assertAlmostEqual(h.estimar(p)["minutos_p50"], round(total, 1), places=1)


class TestPuertas(unittest.TestCase):
    def test_previa(self):
        self.assertTrue(h.puerta_previa({"minutos_p80": 31}, "N2")["dispara"])
        self.assertFalse(h.puerta_previa({"minutos_p80": 30}, "N2")["dispara"])
        n3 = h.puerta_previa({"minutos_p80": 100}, "N3", n3_expreso=True)
        self.assertFalse(n3["dispara"])
        self.assertEqual(n3["minutos_autorizados"], 240)
        self.assertTrue(h.puerta_previa({"minutos_p80": 25}, "PERS", limite_min=20)["dispara"])

    def test_margen_pta(self):
        self.assertEqual(h.margen_pta(30), 5)
        self.assertEqual(h.margen_pta(120), 12)

    def test_en_ejecucion(self):
        r = h.evaluar_en_ejecucion(20, 32, 30)
        self.assertEqual(r["puerta"], "PT30")
        self.assertFalse(h.evaluar_en_ejecucion(20, 29, 30)["dispara"])
        self.assertFalse(h.evaluar_en_ejecucion(40, 74, 70)["dispara"])     # dentro del margen (+7)
        self.assertEqual(h.evaluar_en_ejecucion(40, 78, 70)["puerta"], "PTA")

    def test_proyeccion_escalada(self):
        pr = h.proyectar(20, 10, {"minutos_p50": 10})
        self.assertEqual(pr["ratio_observado"], 2.0)
        self.assertEqual(pr["restante_p50"], 20)
        lim = h.proyectar(50, 10, {"minutos_p50": 10})
        self.assertEqual(lim["ratio_observado"], 2.5)


class TestOpciones(unittest.TestCase):
    def test_version_recortada_respeta_integridad(self):
        p = plan("N2", ("RV", "FON", "RF"))
        v = h.version_recortada(p)
        self.assertTrue(v["alcanza_objetivo"])
        self.assertIn(v["plan_modificado"]["profundidad"]["D9"], ("P2", "P3"))
        self.assertNotEqual(v["plan_modificado"]["profundidad"]["D12"], "P0")
        self.assertIn("G3 (HT-09)", v["controles_no_recortados"])

    def test_opciones_y_recomendacion(self):
        p = plan("N3", ("RV", "FON", "RF"), "CADENA_DE_VALOR")
        e = h.estimar(p)
        o = h.opciones(p, e)
        nombres = [x["opcion"] for x in o["opciones"]]
        self.assertEqual(nombres, ["CONTINUAR", "VERSION_30_MIN", "DIVIDIR_EN_FASES", "CANCELAR"])
        self.assertIn(o["recomendacion_bloque"]["opcion"], h.OPCIONES)
        self.assertEqual(h.opciones(p, e, relevancia="ALTA")["recomendacion_bloque"]["opcion"], "CONTINUAR")

    def test_sin_f5_no_hay_division(self):
        p = plan()
        o = h.opciones(p, h.estimar(p, fases=["F8", "F9", "F10"]), 25, fases_restantes=["F8", "F9", "F10"])
        self.assertNotIn("DIVIDIR_EN_FASES", [x["opcion"] for x in o["opciones"]])


class TestPolitica(unittest.TestCase):
    REGLAS = [{"regla_id": "POL-1", "condicion": {"relevancia": "ALTA", "nivel": ["N2", "N3"]}, "accion": "AUTORIZAR_HASTA", "minutos": 90},
              {"regla_id": "POL-2", "condicion": {"origen": "BLOQUE_A"}, "accion": "AUTORIZAR_HASTA", "minutos": 60},
              {"regla_id": "POL-3", "condicion": {"minutos_max": 1000}, "accion": "ELEGIR_OPCION", "opcion": "DIVIDIR_EN_FASES"}]

    def test_reglas(self):
        r = h.aplicar_politica(self.REGLAS, {"relevancia": "ALTA", "nivel": "N2"}, 70)
        self.assertEqual((r["resultado"], r["regla_id"]), ("AUTORIZA", "POL-1"))
        r = h.aplicar_politica(self.REGLAS, {"relevancia": "MEDIA", "nivel": "N2", "origen": "BLOQUE_A"}, 55)
        self.assertEqual(r["regla_id"], "POL-2")
        r = h.aplicar_politica(self.REGLAS, {"relevancia": "MEDIA", "origen": "LIBRE"}, 150)
        self.assertEqual((r["regla_id"], r["opcion"]), ("POL-3", "DIVIDIR_EN_FASES"))

    def test_politica_del_runbook(self):
        # Ejemplo de la sección 3.3 del Runbook: POL-3 divide en fases si el p80 alcanza 120 min
        pol = [{"regla_id": "POL-1", "condicion": {"origen": "BLOQUE_A", "siguiente_paso_A": "ENVIAR_A_BLOQUE_B", "nivel": ["N2"]},
                "accion": "AUTORIZAR_HASTA", "minutos": 60},
               {"regla_id": "POL-2", "condicion": {"relevancia": "ALTA", "nivel": ["N2", "N3"]}, "accion": "AUTORIZAR_HASTA", "minutos": 90},
               {"regla_id": "POL-3", "condicion": {"minutos_p80_min": 120}, "accion": "ELEGIR_OPCION", "opcion": "DIVIDIR_EN_FASES"}]
        ctx = {"origen": "BLOQUE_A", "siguiente_paso_A": "ENVIAR_A_BLOQUE_B", "nivel": "N2", "relevancia": "MEDIA"}
        self.assertEqual(h.aplicar_politica(pol, ctx, 55)["regla_id"], "POL-1")
        self.assertEqual(h.aplicar_politica(pol, dict(ctx, relevancia="ALTA"), 80)["regla_id"], "POL-2")
        r = h.aplicar_politica(pol, ctx, 150)
        self.assertEqual((r["regla_id"], r["opcion"]), ("POL-3", "DIVIDIR_EN_FASES"))
        self.assertEqual(h.aplicar_politica(pol, dict(ctx, origen="LIBRE"), 100)["resultado"], "NO_CUBRE")

    def test_sin_politica_y_tope(self):
        self.assertEqual(h.aplicar_politica([], {}, 40)["resultado"], "NO_CUBRE")
        r = h.aplicar_politica([{"regla_id": "P", "condicion": {}, "accion": "AUTORIZAR_HASTA", "minutos": 999}], {}, 300)
        self.assertEqual(r["resultado"], "NO_CUBRE")      # por encima del tope de 240 min

    def test_caducidad(self):
        self.assertEqual(h.estado_autorizacion("2026-11-01T10:00:00", "2026-11-01T20:00:00"), "PENDIENTE")
        self.assertEqual(h.estado_autorizacion("2026-11-01T10:00:00", "2026-11-02T11:00:00"), "RECORDATORIO")
        self.assertEqual(h.estado_autorizacion("2026-11-01T10:00:00", "2026-11-08T10:00:00"), "CADUCADA")


class TestPuntosControl(unittest.TestCase):
    def test_guardar_cargar_y_alteracion(self):
        with tempfile.TemporaryDirectory() as d:
            r = h.guardar_punto_control(d, "CKP-2026-0001", {"fase": "F2", "x": [1, 2]})
            self.assertEqual(h.cargar_punto_control(r)["fase"], "F2")
            c = json.load(open(r, encoding="utf-8"))
            c["datos"]["fase"] = "F9"
            json.dump(c, open(r, "w", encoding="utf-8"))
            with self.assertRaises(h.ErrorEntrada):
                h.cargar_punto_control(r)


class TestVarios(unittest.TestCase):
    def test_recalibrar(self):
        hist = [{"fase": "F2", "estimado_p50": 10, "real": 15}] * 20 + [{"fase": "F5", "estimado_p50": 5, "real": 5}] * 3
        r = h.recalibrar(hist)
        self.assertEqual(r["factores"]["F2"], 1.5)
        self.assertFalse(r["informe"]["F5"]["aplicado"])
        r2 = h.recalibrar([{"fase": "F3", "estimado_p50": 1, "real": 10}] * 25)
        self.assertEqual(r2["factores"]["F3"], 3.0)   # banda

    def test_cronometro(self):
        t = [0.0]
        c = h.Cronometro(lambda: t[0], consumido_previo=10)
        c.abrir("F1")
        t[0] = 4
        c.cerrar("F1", uc=2)
        self.assertEqual(c.consumido(), 14)
        self.assertEqual(c.resumen()["uc_total"], 2)

    def test_instancias(self):
        o = h.ordenes_instancias({"AG-B04": 7, "AG-B21": 5, "AG-B05": 1})
        self.assertEqual({x["agente"]: x["accion"] for x in o}, {"AG-B04": "ABRIR", "AG-B21": "REORDENAR"})

    def test_cli(self):
        with tempfile.TemporaryDirectory() as d:
            f = os.path.join(d, "p.json")
            json.dump(plan("N2", ("RV", "FON", "RF")), open(f, "w"))
            self.assertEqual(h.main([f]), 1)
            json.dump(plan("N1"), open(f, "w"))
            self.assertEqual(h.main([f]), 0)


class TestCapasV21(unittest.TestCase):
    """V2.1 (7.10): estimación por capa, acumulado y opción HASTA_PV2."""

    def test_desglose_por_capa_suma_total(self):
        e = h.estimar(plan())
        self.assertEqual(set(e["desglose_por_capa"]), {"0", "1", "2", "3", "4"})
        self.assertAlmostEqual(sum(e["desglose_por_capa"].values()), sum(e["desglose_por_fase"].values()), delta=0.05)
        self.assertLess(e["minutos_p80_hasta_pv2"], e["minutos_p80"])

    def test_opcion_hasta_pv2(self):
        p = plan()
        e = h.estimar(p)
        r = h.opciones(p, e, 0.0, pv2_pendiente=True)
        nombres = [o["opcion"] for o in r["opciones"]]
        self.assertIn("HASTA_PV2", nombres)
        self.assertNotIn("HASTA_PV2", [o["opcion"] for o in h.opciones(p, e, 0.0)["opciones"]])
        o = next(o for o in r["opciones"] if o["opcion"] == "HASTA_PV2")
        self.assertAlmostEqual(o["minutos_p80"], e["minutos_p80_hasta_pv2"], delta=0.1)

    def test_politica_elige_hasta_pv2(self):
        r = h.aplicar_politica([{"regla_id": "POL-4", "condicion": {"origen": "LIBRE"}, "accion": "ELEGIR_OPCION",
                                 "opcion": "HASTA_PV2"}], {"origen": "LIBRE"}, 50)
        self.assertEqual((r["resultado"], r["opcion"]), ("AUTORIZA", "HASTA_PV2"))


if __name__ == "__main__":
    unittest.main()
