# -*- coding: utf-8 -*-
"""Pruebas unitarias de HT-02 con un servidor HTTP local (http.server en un hilo); sin red externa."""
import csv
import datetime as dt
import io
import json
import os
import sys
import tempfile
import threading
import time
import unittest
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, RAIZ)

import ht02_verificador_enlaces as h  # noqa: E402

TEXTO_BASE = ("Este artículo documenta el momentum temporal en futuros de índices, divisas, materias primas y bonos. "
              "La rentabilidad propia pasada de doce meses predice la futura durante aproximadamente un año. "
              "Los autores analizan costes de transacción, robustez por subperiodos y comportamiento en crisis. "
              "Las conclusiones se mantienen tras controlar por factores conocidos y por la liquidez de cada contrato. "
              "El trabajo discute además la relación con la teoría de reacción insuficiente y excesiva del inversor.")
PAGINA_OK = f"<html><head><title>Time Series Momentum</title></head><body><p>{TEXTO_BASE}</p><p>Visitas: 12345</p></body></html>"
PAGINA_CASI = PAGINA_OK.replace("aproximadamente", "alrededor de").replace("12345", "99999")
PAGINA_DISTINTA = ("<html><head><title>Nueva</title></head><body><p>Página completamente distinta sobre política de "
                   "privacidad, cookies, condiciones de uso, contacto, aviso legal y mapa del sitio web de la editorial "
                   "con enlaces a otras secciones que no guardan relación con el artículo original registrado.</p></body></html>")
PAGINA_MURO = ("<html><head><title>Article</title></head><body><p>Abstract only.</p><p>Subscribe to read the full text."
               "</p><p>Access through your institution</p><button>Buy article</button></body></html>")
PAGINA_RETRACTADA = "<html><head><title>Retracted</title></head><body><p>Retraction notice: this article has been retracted.</p></body></html>"
PAGINA_404_BLANDA = "<html><head><title>Página no encontrada</title></head><body><p>Lo sentimos.</p></body></html>"


class Manejador(BaseHTTPRequestHandler):
    contadores: dict = {}

    def log_message(self, *a):  # silencio
        pass

    def _responder(self, codigo, cuerpo=b"", tipo="text/html; charset=utf-8", cabeceras=None):
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        for k, v in (cabeceras or {}).items():
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(cuerpo)

    def _ruta(self):
        u = urllib.parse.urlsplit(self.path)
        return u.path, urllib.parse.parse_qs(u.query)

    def do_HEAD(self):
        ruta, _ = self._ruta()
        if ruta == "/head405":
            return self._responder(405)
        return self.do_GET()

    def do_GET(self):  # noqa: C901
        ruta, q = self._ruta()
        clave = (self.command, ruta)
        Manejador.contadores[clave] = Manejador.contadores.get(clave, 0) + 1
        n = Manejador.contadores[clave]
        if ruta in ("/ok", "/head405", "/conarchivo-ok", "/"):
            return self._responder(200, PAGINA_OK.encode())
        if ruta == "/casi":
            return self._responder(200, PAGINA_CASI.encode())
        if ruta == "/cambiado":
            return self._responder(200, PAGINA_DISTINTA.encode())
        if ruta == "/redir301":
            return self._responder(301, cabeceras={"Location": "/ok"})
        if ruta == "/redir302":
            return self._responder(302, cabeceras={"Location": "/ok"})
        if ruta == "/soft404":
            return self._responder(301, cabeceras={"Location": "/"})
        if ruta == "/titulo404":
            return self._responder(200, PAGINA_404_BLANDA.encode())
        if ruta in ("/roto", "/conarchivo-roto"):
            return self._responder(404, b"<html><title>404</title></html>")
        if ruta == "/error500":
            return self._responder(500)
        if ruta == "/inestable":
            return self._responder(503 if n == 1 else 200, PAGINA_OK.encode())
        if ruta == "/muro":
            return self._responder(200, PAGINA_MURO.encode())
        if ruta == "/pago402":
            return self._responder(402, b"payment required")
        if ruta == "/retractado":
            return self._responder(200, PAGINA_RETRACTADA.encode())
        if ruta == "/lento":
            time.sleep(1.5)
            return self._responder(200, PAGINA_OK.encode())
        if ruta == "/pdf":
            return self._responder(200, b"%PDF-1.4 contenido binario", "application/pdf")
        if ruta.startswith("/doi/10.1234/bueno"):
            return self._responder(302, cabeceras={"Location": "/ok"})
        if ruta.startswith("/doi/"):
            return self._responder(404)
        if ruta == "/wayback/available":
            url = q.get("url", [""])[0]
            if "conarchivo" in url:
                datos = {"archived_snapshots": {"closest": {"available": True, "status": "200", "timestamp": "20250101000000",
                                                            "url": f"http://web.archive.org/web/20250101000000/{url}"}}}
            else:
                datos = {"archived_snapshots": {}}
            return self._responder(200, json.dumps(datos).encode(), "application/json")
        return self._responder(404)


class BaseServidor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = ThreadingHTTPServer(("127.0.0.1", 0), Manejador)
        cls.hilo = threading.Thread(target=cls.srv.serve_forever, daemon=True)
        cls.hilo.start()
        cls.base = f"http://127.0.0.1:{cls.srv.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()

    def setUp(self):
        Manejador.contadores = {}
        self.cfg = h.Config(timeout=1.0, reintentos=1, espera_base=0, doi_base=self.base + "/doi/",
                            wayback_api=self.base + "/wayback/available", usar_proxy_entorno=False)
        self.hoy = dt.date(2026, 11, 2)

    def ficha_md(self, fid, ruta=None, doi=None, q=80, nivel="A", extra=""):
        lineas = [f"#### {fid} · Q {q} ({nivel}) — Título {fid}"]
        if ruta is not None:
            lineas.append(f"- **URL:** {self.base}{ruta}")
        if doi:
            lineas.append(f"- **DOI:** {doi}")
        lineas.append("- **Estado del enlace:** OK")
        lineas.append("- **Última verificación:** 2026-10-25")
        if extra:
            lineas.extend(extra.strip("\n").split("\n"))
        return "\n".join(lineas) + "\n\n"

    def verificar(self, md, fid=None):
        res = h.verificar_archivo(md.splitlines(keepends=True), self.cfg, self.hoy, [fid] if fid else None, hilos=2)
        return res[0] if fid or len(res) == 1 else res


class TestLectura(unittest.TestCase):
    def test_cabecera_y_campos(self):
        md = ("# F7\n\n## TA-05\n\n#### ANA-DOC-0001 · Q 88 (A) — Jegadeesh y Titman (1993)\n"
              "- **DOI:** 10.1111/j.1540-6261.1993.tb04702.x\n- **URL:** <https://example.org/x>\n"
              "- **Estado del enlace:** OK\n\n#### ANA-DOC-0002 — Sin calidad\n- **URL:** [pdf](https://e.org/y.pdf)\n\n## Registro de bajas\n")
        f = h.leer_fichas(md.splitlines(keepends=True))
        self.assertEqual([x.id for x in f], ["ANA-DOC-0001", "ANA-DOC-0002"])
        self.assertEqual((f[0].q, f[0].nivel), (88, "A"))
        self.assertIsNone(f[1].q)
        self.assertEqual(h.extraer_url(f[0].campo("URL")), "https://example.org/x")
        self.assertEqual(h.extraer_url(f[1].campo("URL")), "https://e.org/y.pdf")
        self.assertEqual(h.extraer_doi(f[0].campo("DOI")), "10.1111/j.1540-6261.1993.tb04702.x")
        self.assertEqual(f[1].linea_fin, md.splitlines().index("## Registro de bajas"))

    def test_similitud_simhash(self):
        a = h.normalizar_contenido(PAGINA_OK.encode(), "text/html")
        b = h.normalizar_contenido(PAGINA_CASI.encode(), "text/html")
        c = h.normalizar_contenido(PAGINA_DISTINTA.encode(), "text/html")
        self.assertNotIn("12345", a)  # tokens con cifras fuera
        self.assertEqual(h.similitud_simhash(h.simhash64(a), h.simhash64(a)), 1.0)
        self.assertGreaterEqual(h.similitud_simhash(h.simhash64(a), h.simhash64(b)), 0.8)
        self.assertLess(h.similitud_simhash(h.simhash64(a), h.simhash64(c)), 0.8)


class TestEstados(BaseServidor):
    def test_ok(self):
        r = self.verificar(self.ficha_md("R1", "/ok"))
        self.assertEqual((r["estado"], r["accion"]), ("OK", "NINGUNA"))
        self.assertTrue(r["hash"].startswith("sha256:"))
        self.assertTrue(r["huella"].startswith("simhash64:"))

    def test_redireccion_permanente_y_temporal(self):
        r = self.verificar(self.ficha_md("R1", "/redir301"))
        self.assertEqual((r["estado"], r["accion"]), ("REDIRIGIDO", "REPARAR"))
        self.assertTrue(r["url_final"].endswith("/ok"))
        r = self.verificar(self.ficha_md("R1", "/redir302"))
        self.assertEqual((r["estado"], r["accion"]), ("REDIRIGIDO", "NINGUNA"))

    def test_head_no_permitido_usa_get(self):
        r = self.verificar(self.ficha_md("R1", "/head405"))
        self.assertEqual(r["estado"], "OK")
        self.assertEqual(r["head_codigo"], 405)

    def test_reintentos(self):
        self.cfg.descargar_contenido = True
        r = self.verificar(self.ficha_md("R1", "/inestable"))
        self.assertEqual(r["estado"], "OK")
        self.assertGreaterEqual(r["intentos"], 2)

    def test_roto_primer_fallo(self):
        r = self.verificar(self.ficha_md("R1", "/roto"))
        self.assertEqual((r["estado"], r["accion"], r["confirmado"]), ("ROTO", "NINGUNA", False))
        self.assertEqual(r["primer_fallo"], "2026-11-02")
        r = self.verificar(self.ficha_md("R1", "/error500"))
        self.assertEqual(r["estado"], "ROTO")
        self.assertEqual(r["codigo_http"], 500)

    def test_roto_confirmado_y_baja(self):
        r = self.verificar(self.ficha_md("R1", "/roto", extra="- **Primer fallo:** 2026-11-01"))
        self.assertEqual((r["estado"], r["accion"], r["confirmado"]), ("ROTO", "DEGRADAR", True))
        r = self.verificar(self.ficha_md("R1", "/roto", extra="- **Primer fallo:** 2026-10-26"))
        self.assertEqual(r["accion"], "BORRAR")
        self.assertIn("dos barridos", r["motivo"])

    def test_roto_con_copia_archivada(self):
        r = self.verificar(self.ficha_md("R1", "/conarchivo-roto"))
        self.assertEqual((r["estado"], r["accion"]), ("ROTO", "REPARAR"))
        self.assertIn("web.archive.org", r["copia_archivada"]["url"])

    def test_roto_con_doi_alternativo(self):
        r = self.verificar(self.ficha_md("R1", "/roto", doi="10.1234/bueno"))
        self.assertEqual((r["estado"], r["accion"]), ("ROTO", "REPARAR"))
        self.assertTrue(r["doi_resuelto"])
        self.assertIn("DOI", r["motivo"])

    def test_solo_doi(self):
        r = self.verificar(self.ficha_md("R1", None, doi="10.1234/bueno"))
        self.assertEqual((r["estado"], r["accion"]), ("OK", "NINGUNA"))
        r = self.verificar(self.ficha_md("R1", None, doi="10.9999/inexistente"))
        self.assertEqual(r["estado"], "ROTO")
        self.assertFalse(r["doi_resuelto"])

    def test_sin_url_ni_doi(self):
        r = self.verificar("#### R1 · Q 70 (B) — Sin enlace\n- **Autores:** X\n")
        self.assertEqual((r["estado"], r["accion"]), ("ROTO", "REPARAR"))

    def test_tiempo_limite(self):
        self.cfg.reintentos = 0
        r = self.verificar(self.ficha_md("R1", "/lento"))
        self.assertEqual(r["estado"], "ROTO")
        self.assertIsNone(r["codigo_http"])

    def test_muro_de_pago(self):
        r = self.verificar(self.ficha_md("R1", "/muro"))
        self.assertEqual((r["estado"], r["accion"]), ("MURO_PAGO", "DEGRADAR"))
        self.assertGreaterEqual(len(r["indicios_muro_pago"]), 2)
        r = self.verificar(self.ficha_md("R1", "/pago402"))
        self.assertEqual(r["estado"], "MURO_PAGO")

    def test_soft404(self):
        self.assertEqual(self.verificar(self.ficha_md("R1", "/soft404"))["estado"], "ROTO")
        self.assertEqual(self.verificar(self.ficha_md("R1", "/titulo404"))["estado"], "ROTO")

    def test_retractacion(self):
        r = self.verificar(self.ficha_md("R1", "/retractado", extra="- **Evidencias:** EVD-2026-0001"))
        self.assertEqual(r["accion"], "BORRAR")
        self.assertTrue(r["retractacion"])
        self.assertIn("Curador", r["aviso_curador"])

    def test_pdf(self):
        r = self.verificar(self.ficha_md("R1", "/pdf"))
        self.assertEqual(r["estado"], "OK")

    def _huellas_ok(self):
        texto = h.normalizar_contenido(PAGINA_OK.encode(), "text/html; charset=utf-8")
        return f"- **Hash de contenido:** {h.sha256_texto(texto)}\n- **Huella de contenido:** {h.simhash64(texto)}"

    def test_contenido_igual_casi_y_cambiado(self):
        extra = self._huellas_ok()
        r = self.verificar(self.ficha_md("R1", "/ok", extra=extra))
        self.assertEqual((r["estado"], r["similitud"]), ("OK", 1.0))
        r = self.verificar(self.ficha_md("R1", "/casi", extra=extra))
        self.assertEqual(r["estado"], "OK")
        self.assertGreaterEqual(r["similitud"], 0.8)
        r = self.verificar(self.ficha_md("R1", "/cambiado", extra=extra))
        self.assertEqual((r["estado"], r["accion"]), ("CONTENIDO_CAMBIADO", "DEGRADAR"))
        self.assertLess(r["similitud"], 0.8)

    def test_baja_por_calidad(self):
        r = self.verificar(self.ficha_md("R1", "/ok", q=45, nivel="D", extra="- **Último uso:** 2026-03-01"))
        self.assertEqual(r["accion"], "BORRAR")
        r = self.verificar(self.ficha_md("R1", "/ok", q=45, nivel="D", extra="- **Último uso:** 2026-10-01"))
        self.assertEqual(r["accion"], "NINGUNA")


class TestEscritura(BaseServidor):
    def test_aplicar(self):
        md = (f"# F7\n\n" + self.ficha_md("R1", "/ok") + self.ficha_md("R2", "/roto")
              + self.ficha_md("R3", "/ok", extra="- **Primer fallo:** 2026-10-30") + "## Registro de bajas\n")
        lineas = md.splitlines(keepends=True)
        res = h.verificar_archivo(lineas, self.cfg, self.hoy)
        nuevas = "".join(h.aplicar_resultados(lineas, res))
        fichas = {f.id: f for f in h.leer_fichas(nuevas.splitlines(keepends=True))}
        self.assertEqual(fichas["R1"].campo("Última verificación"), "2026-11-02")
        self.assertTrue(fichas["R1"].campo("Hash de contenido").startswith("sha256:"))
        self.assertEqual(fichas["R2"].campo("Estado del enlace"), "ROTO")
        self.assertEqual(fichas["R2"].campo("Primer fallo"), "2026-11-02")
        self.assertIsNone(fichas["R3"].campo("Primer fallo"))  # acierto: se limpia
        # Los campos insertados quedan dentro de la ficha, antes de la siguiente cabecera
        self.assertLess(nuevas.index("Hash de contenido"), nuevas.index("#### R2"))
        # Una segunda verificación tras aplicar compara contra la huella guardada
        res2 = h.verificar_archivo(nuevas.splitlines(keepends=True), self.cfg, self.hoy, ["R1"])
        self.assertEqual(res2[0]["similitud"], 1.0)

    def test_borrar_con_registro_existente(self):
        md = ("# F7\n\n" + self.ficha_md("R1", "/ok") + self.ficha_md("R2", "/roto", extra="- **Evidencias:** EVD-2026-0009")
              + "## Registro de bajas\n\n| REF-id | Título | Motivo | Fecha | Sustituta |\n|---|---|---|---|---|\n"
              + "| R0 | Antigua | Retractada | 2026-10-01 | — |\n\n## Otra sección\n")
        nuevas, info = h.borrar_ficha(md.splitlines(keepends=True), "R2", "Enlace roto sin alternativa", self.hoy, "R1")
        texto = "".join(nuevas)
        self.assertNotIn("#### R2", texto)
        self.assertIn("#### R1", texto)
        self.assertIn("| R2 | Título R2 | Enlace roto sin alternativa | 2026-11-02 | R1 |", texto)
        self.assertLess(texto.index("| R2 |"), texto.index("## Otra sección"))
        self.assertGreater(texto.index("| R2 |"), texto.index("| R0 |"))
        self.assertIn("aviso_curador", info)

    def test_borrar_crea_registro_y_exige_motivo(self):
        md = "# F8\n\n" + self.ficha_md("M1", "/ok")
        nuevas, _ = h.borrar_ficha(md.splitlines(keepends=True), "M1", "Redundante con M2 (Q mayor)", self.hoy)
        texto = "".join(nuevas)
        self.assertIn("## Registro de bajas", texto)
        self.assertIn("| M1 | Título M1 | Redundante con M2 (Q mayor) | 2026-11-02 | — |", texto)
        with self.assertRaises(ValueError):
            h.borrar_ficha(md.splitlines(keepends=True), "M1", "", self.hoy)
        with self.assertRaises(ValueError):
            h.borrar_ficha(md.splitlines(keepends=True), "NOEXISTE", "x", self.hoy)


class TestCLI(BaseServidor):
    def test_informes_y_aplicar(self):
        md = "# F9\n\n" + self.ficha_md("RF-0001", "/ok") + self.ficha_md("RF-0002", "/muro") + "## Registro de bajas\n"
        with tempfile.TemporaryDirectory() as d:
            ruta = os.path.join(d, "f9.md")
            with open(ruta, "w", encoding="utf-8") as fh:
                fh.write(md)
            pj, pc = os.path.join(d, "i.json"), os.path.join(d, "i.csv")
            args = [ruta, "--salida-json", pj, "--salida-csv", pc, "--aplicar", "--fecha", "2026-11-02", "--timeout", "1",
                    "--reintentos", "0", "--espera", "0", "--sin-proxy", "--doi-base", self.base + "/doi/",
                    "--wayback-api", self.base + "/wayback/available"]
            self.assertEqual(h.main(args), 0)
            with open(pj, encoding="utf-8") as fh:
                inf = json.load(fh)
            with open(pc, encoding="utf-8") as fh:
                filas = list(csv.DictReader(fh))
            with open(ruta, encoding="utf-8") as fh:
                actualizado = fh.read()
            self.assertEqual(inf["resumen"]["por_estado"]["OK"], 1)
            self.assertEqual(inf["resumen"]["por_estado"]["MURO_PAGO"], 1)
            self.assertEqual(inf["resumen"]["salud_enlaces_pct_ok"], 50.0)
            self.assertEqual([f["estado"] for f in filas], ["OK", "MURO_PAGO"])
            self.assertEqual(set(filas[0].keys()), set(h.COLUMNAS_CSV))
            self.assertIn("- **Estado del enlace:** MURO_PAGO", actualizado)
            # Borrado por CLI
            self.assertEqual(h.main([ruta, "--borrar", "RF-0002", "--motivo", "Muro de pago sin alternativa", "--fecha", "2026-11-02"]), 0)
            with open(ruta, encoding="utf-8") as fh:
                tras = fh.read()
            self.assertNotIn("#### RF-0002", tras)
            self.assertIn("| RF-0002 |", tras)
            self.assertEqual(h.main([ruta, "--borrar", "RF-0001"]), 2)  # sin motivo

    def test_incidencia_de_red_no_aplica(self):
        md = "# F9\n\n#### RF-0009 · Q 70 (B) — Inalcanzable\n- **URL:** http://127.0.0.1:9/nada\n- **Estado del enlace:** OK\n"
        with tempfile.TemporaryDirectory() as d:
            ruta = os.path.join(d, "f9.md")
            with open(ruta, "w", encoding="utf-8") as fh:
                fh.write(md)
            pj = os.path.join(d, "i.json")
            h.main([ruta, "--aplicar", "--salida-json", pj, "--timeout", "1", "--reintentos", "0", "--espera", "0",
                    "--wayback", "nunca", "--sin-proxy"])
            with open(pj, encoding="utf-8") as fh:
                inf = json.load(fh)
            with open(ruta, encoding="utf-8") as fh:
                self.assertEqual(fh.read(), md)
        self.assertTrue(inf["resumen"]["incidencia_red"])
        self.assertIn("aviso", inf)

    def test_ejemplo_se_lee(self):
        with open(os.path.join(RAIZ, "ejemplos", "referencias_ejemplo.md"), encoding="utf-8") as fh:
            f = h.leer_fichas(fh.readlines())
        self.assertEqual(len(f), 4)
        self.assertEqual(f[-1].q, 45)


if __name__ == "__main__":
    unittest.main()
