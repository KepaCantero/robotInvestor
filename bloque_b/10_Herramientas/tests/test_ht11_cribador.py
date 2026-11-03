# -*- coding: utf-8 -*-
"""Pruebas de HT-11 (cribador de universos en punto del tiempo con filtros de invertibilidad)."""
import json
import os
import sys
import tempfile
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, RAIZ)

import ht11_cribador as h  # noqa: E402

CSV = os.path.join(RAIZ, "ejemplos", "universo_rv_ejemplo.csv")


def fuente(filas, nombre="f"):
    return [{"nombre": nombre, "filas": filas}]


class TestRV(unittest.TestCase):
    def test_ejemplo(self):
        u = h.construir_universo("RV", fuente(h.leer_csv(CSV)), "2026-10-30", "redes_electricas_europa")
        incl = {f["id"] for f in u["incluidos"]}
        self.assertEqual(incl, {"PRY", "NKT", "ENR"})
        motivos = {e["id"]: e["motivo"] for e in u["excluidos"]}
        self.assertEqual(motivos["MICRO"], "NO_INVERTIBLE")
        self.assertEqual(motivos["OTC1"], "FUERA_DE_MARCO")
        self.assertEqual(motivos["SANC"], "NO_INVERTIBLE")
        self.assertEqual(motivos["SINDATO"], "DATOS_INSUFICIENTES")
        self.assertNotIn("BAJA", incl | set(motivos))       # dada de baja antes de la fecha
        self.assertNotIn("FUT", incl | set(motivos))        # aún no cotizaba
        self.assertNotIn("OTRO_AMB", incl | set(motivos))   # otro ámbito

    def test_punto_en_el_tiempo_sin_supervivencia(self):
        u = h.construir_universo("RV", fuente(h.leer_csv(CSV)), "2025-05-30", "redes_electricas_europa")
        self.assertIn("BAJA", {f["id"] for f in u["incluidos"]})   # cotizaba entonces: no se elimina a posteriori

    def test_instantaneas(self):
        filas = [{"id": "A", "tipo_activo": "RV", "region_mercado": "EEE", "capitalizacion_meur": "200", "volumen_medio_meur": "2",
                  "flotante_pct": "50", "ejercicios_auditados": "5", "fecha_dato": "2025-01-01"},
                 {"id": "A", "tipo_activo": "RV", "region_mercado": "EEE", "capitalizacion_meur": "500", "volumen_medio_meur": "2",
                  "flotante_pct": "50", "ejercicios_auditados": "5", "fecha_dato": "2026-01-01"}]
        self.assertEqual(h.construir_universo("RV", fuente(filas), "2025-06-01")["tamano_invertible"], 0)
        self.assertEqual(h.construir_universo("RV", fuente(filas), "2026-06-01")["tamano_invertible"], 1)
        self.assertEqual(h.construir_universo("RV", fuente(filas), "2024-06-01")["fuera_de_fecha"], 1)

    def test_fusion_lista_y_marco(self):
        filas = h.leer_csv(CSV)
        u = h.construir_universo("RV", fuente(filas, "a") + fuente(filas[:2], "b"), "2026-10-30",
                                 lista_restriccion=["PRY"])
        self.assertEqual([f["id"] for f in u["incluidos"]], ["PRY"])
        self.assertEqual(u["incluidos"][0]["_fuentes"], ["a", "b"])
        u = h.construir_universo("RV", fuente(filas), "2026-10-30", marco={"exclusiones": ["NKT"]})
        self.assertIn(("NKT", "FUERA_DE_MARCO"), [(e["id"], e["motivo"]) for e in u["excluidos"]])
        u = h.construir_universo("RV", fuente(filas), "2026-10-30", marco={"permitir_microcap": True})
        det = {e["id"]: e["detalle"] for e in u["excluidos"]}
        self.assertIn("volumen", det["MICRO"])     # ya no falla por capitalización, sino por liquidez


class TestOtrosTipos(unittest.TestCase):
    def un(self, tipo, fila, **kw):
        base = {"id": "X", "tipo_activo": tipo, "region_mercado": "EEE"}
        base.update(fila)
        return h.construir_universo(tipo, fuente([base]), "2026-10-30", **kw)

    def test_rf(self):
        ok = {"precio_observable": "si", "saldo_vivo_meur": "500", "folleto": "si", "vencimiento": "2030-01-01",
              "calificacion": "BBB", "denominacion_min_eur": "100000"}
        u = self.un("RF", ok)
        self.assertEqual(u["tamano_invertible"], 1)
        self.assertTrue(u["avisos"])
        self.assertEqual(self.un("RF", dict(ok, vencimiento="2027-01-01"))["excluidos"][0]["motivo"], "NO_INVERTIBLE")
        self.assertEqual(self.un("RF", dict(ok, tipo_emisor="soberano"))["tamano_invertible"], 0)

    def test_der_binarias_y_cfd(self):
        ok = {"tipo_instrumento": "futuro", "mercado_regulado": "si", "kid": "si", "interes_abierto": "5000"}
        self.assertEqual(self.un("DER", ok)["tamano_invertible"], 1)
        self.assertEqual(self.un("DER", dict(ok, tipo_instrumento="opcion_binaria"))["tamano_invertible"], 0)
        self.assertEqual(self.un("DER", dict(ok, tipo_instrumento="cfd"))["tamano_invertible"], 0)
        self.assertEqual(self.un("DER", dict(ok, tipo_instrumento="cfd"), marco={"permitir_cfd": True})["tamano_invertible"], 1)

    def test_fon_cri_inm_mon_tcv(self):
        fon = {"ucits": "si", "kid": "si", "patrimonio_meur": "150", "historial_anos": "3", "clase_eur_o_cubierta": "si"}
        self.assertEqual(self.un("FON", fon)["tamano_invertible"], 1)
        self.assertEqual(self.un("FON", dict(fon, patrimonio_meur="60"))["tamano_invertible"], 0)
        self.assertEqual(self.un("FON", dict(fon, patrimonio_meur="60", gestion="activa"))["tamano_invertible"], 1)
        cri = {"acceso_mica_o_etp": "si", "capitalizacion_meur": "900", "historial_meses": "30"}
        self.assertEqual(self.un("CRI", cri)["tamano_invertible"], 1)
        self.assertEqual(self.un("CRI", dict(cri, stablecoin="si"))["tamano_invertible"], 0)
        inm = {"capitalizacion_meur": "900", "volumen_medio_meur": "1", "nav_frecuencia_meses": "6", "cuentas_auditadas": "si", "ltv": "0.7"}
        self.assertEqual(self.un("INM", inm)["tamano_invertible"], 0)
        self.assertEqual(self.un("MON", {"tipo_instrumento": "letra", "tipo_emisor": "soberano", "plazo_dias": "180"})["tamano_invertible"], 1)
        self.assertEqual(self.un("MON", {"tipo_instrumento": "pagare", "calificacion_corto": "A-3"})["tamano_invertible"], 0)
        tcv = {"ucits": "si", "kid": "si", "volumen_medio_meur": "3", "apalancado_o_inverso": "si"}
        self.assertEqual(self.un("TCV", tcv)["tamano_invertible"], 0)
        self.assertEqual(h.construir_universo("TCV", fuente([dict(tcv, id="X", tipo_activo="TCV", region_mercado="EEE")]),
                                              "2026-10-30", horizonte="H1")["tamano_invertible"], 1)

    def test_vehiculo_colectivo_va_a_fon(self):
        # 2.6, regla 2: un ETF o fondo nunca entra en un universo distinto de FON (coherente con G3B-SEL-09)
        tcv = {"ucits": "si", "kid": "si", "volumen_medio_meur": "3", "tipo_instrumento": "etf"}
        u = self.un("TCV", tcv)
        self.assertEqual(u["tamano_invertible"], 0)
        self.assertIn("FON", u["excluidos"][0]["detalle"])
        self.assertEqual(self.un("MON", {"tipo_instrumento": "fondo", "tipo_emisor": "soberano", "plazo_dias": "90"})["tamano_invertible"], 0)
        self.assertEqual(self.un("TCV", dict(tcv, tipo_instrumento="etn"))["tamano_invertible"], 1)

    def test_div_mp_idx_alt(self):
        self.assertEqual(self.un("DIV", {"controles_capital": "no", "instrumento_acceso": "futuro CME", "instrumento_en_marco": "si"})["tamano_invertible"], 1)
        self.assertEqual(self.un("MP", {"tipo_instrumento": "etc", "colateral_auditado": "si", "emisor": "E"})["tamano_invertible"], 1)
        self.assertEqual(self.un("IDX", {"metodologia_publica": "si", "replicable_ucits_o_futuro": "si", "historial_anos": "1"})["tamano_invertible"], 0)
        self.assertEqual(self.un("ALT", {"cotizado_o_eltif": "si", "nav_frecuencia_meses": "3", "nav_auditado": "si",
                                         "mecanismo_liquidez": "cotización", "gestor_regulado": "si"})["tamano_invertible"], 1)


class TestCLI(unittest.TestCase):
    def test_cli(self):
        with tempfile.TemporaryDirectory() as d:
            sal = os.path.join(d, "u.json")
            self.assertEqual(h.main(["--tipo", "RV", "--csv", CSV, "--fecha", "2026-10-30", "--ambito",
                                     "redes_electricas_europa", "--salida", sal]), 0)
            self.assertEqual(json.load(open(sal, encoding="utf-8"))["tamano_invertible"], 3)
            self.assertEqual(h.main(["--tipo", "RV", "--csv", os.path.join(d, "no.csv"), "--fecha", "2026-10-30"]), 3)


if __name__ == "__main__":
    unittest.main()
