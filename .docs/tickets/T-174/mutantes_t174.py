"""Uso: mutantes_t174.py <carpeta bloque_a> <copia> [filtro, p. ej. "H-07|H-08"]. Mutantes propios de T-174: cada uno debe hacer fallar tests/test_t174_pb61_revision_c2.py."""
import shutil, subprocess, sys, pathlib
SRC = pathlib.Path(sys.argv[1]); TMP = pathlib.Path(sys.argv[2])
M = {
 "M1 no abre revisión": ("bloque_a/interfaz_broker.py", "entregados = self._entregados_con(cns_id, as_of) if nuevos else []", "entregados = []"),
 "M2 RUN sin supuestos_cns": ("bloque_a/orquestacion.py", '**({"supuestos_cns": sc} if (sc := sorted({s["cns_id"] for s in paquete.get("supuestos_declarados") or []})) else {})', "**{}"),
 "M3 sin nota en limitaciones": ("bloque_a/orquestacion.py", "limitaciones += self.consultas.nota_revision(disparador)", "pass"),
 "M4 reabre siempre": ("bloque_a/interfaz_broker.py", "nuevos = sorted(set(textos) - previos)", "nuevos = sorted(set(textos))"),
 "M5 cuenta RUN bloqueados": ("bloque_a/interfaz_broker.py", 'and e.get("entrega") == "ENTREGADA" and cns_id', "and cns_id"),
 "M6 C6 sin supuestos_cns": ("bloque_a/seguimiento.py", '**({"supuestos_cns": sc} if (sc := sorted({s["cns_id"] for s in informe["supuestos_declarados"]})) else {})', "**{}"),
 "M7 esconde errores de control": ("bloque_a/interfaz_broker.py", "if respuesta_final.para_la_consulta(self.b.almacen, e):", "if False:"),
 "M8 admite índices booleanos": ("bloque_a/interfaz_broker.py", "isinstance(i, int) and not isinstance(i, bool)", "isinstance(i, int)"),
 "M9 sin tipos de los revisados": ("bloque_a/interfaz_broker.py", 'if c.get("clases") else sorted(vistas)', 'if c.get("clases") else []'),
 "M10 la revisión ve la consulta sin la respuesta registrada": ("bloque_a/interfaz_broker.py", '"cns_id": cns_id, "estado": estado,\n                    "respuestas": respuestas,', '"cns_id": cns_id, "estado": c.get("estado"),\n                    "respuestas": respuestas,'),
 "M11 copia el texto del error": ("bloque_a/interfaz_broker.py", 'f"La revisión C2 de {cns_id} falló ({fallo})"', 'f"La revisión C2 de {cns_id} falló ({e})"'),
 "M12 (H-01) sin cerrojo": ("bloque_a/interfaz_broker.py", "            with self.b.almacen._transaccion():\n                c = self._todas().get(cns_id) or c", "            if True:\n                c = self._todas().get(cns_id) or c"),
 "M13 (H-01) sin releer la consulta": ("bloque_a/interfaz_broker.py", "            c = self._todas().get(cns_id) or c\n", "            pass\n"),
 "M14 (H-02) sin INTERRUMPIDA": ("bloque_a/interfaz_broker.py", '{"estado": "INTERRUMPIDA", "fallo": fallo}', '{"estado": "EN_CURSO", "fallo": fallo}'),
 "M15 (H-02) responder no relanza": ("bloque_a/interfaz_broker.py", 'estados=("INTERRUMPIDA", "PENDIENTE"))', 'estados=())'),
 "M16 (H-02) relanza las EN_CURSO": ("bloque_a/interfaz_broker.py", 'estados=("INTERRUMPIDA", "PENDIENTE"))', 'estados=("INTERRUMPIDA", "PENDIENTE", "EN_CURSO"))'),
 "M17 (H-03) sin intersección": ("bloque_a/interfaz_broker.py", 'sorted(set(c["clases"]) & vistas)', 'sorted(set(c["clases"]))'),
 "M18 (H-04) sin fecha en lo entregado": ("bloque_a/interfaz_broker.py", 'estado("F5", as_of, clave="id")', 'estado("F5", clave="id")'),
 "M19 (H-05) siempre FALLIDA": ("bloque_a/interfaz_broker.py", 'estado_final = (run.get("entrega") or "FALLIDA") if run else "FALLIDA"', 'estado_final = "FALLIDA"'),
 "M20 (H-06) sin escalado": ("bloque_a/interfaz_broker.py", 'f"La revisión C2 de {cns_id} falló ({fallo})", "AG-01",\n                                          tratamiento=tratamiento, escalado_operador=True)', 'f"La revisión C2 de {cns_id} falló ({fallo})", "AG-01")'),
 "M22 (H-07) sin huerfanas en el ciclo": ("bloque_a/orquestacion.py", "        self.consultas.huerfanas()   #", "        pass   #"),
 "M23 (H-07) avisa en cada ciclo": ("bloque_a/interfaz_broker.py", '                    if not actual.get("aviso_huerfana"):', '                    if True:'),
 "M24 (H-07) sin conjunto en marcha": ("bloque_a/interfaz_broker.py", 'return (str(Path(self.b.almacen.carpeta).resolve()), cns_id, r.get("msg_id")) not in _EN_MARCHA', "return True"),
 "M25 (H-07) pid muerto no cuenta": ("bloque_a/interfaz_broker.py", 'return None if vivo is None else not vivo', "return False"),
 "M26 (H-07) sin marca huerfana en la lista": ("bloque_a/interfaz_broker.py", 'if (k, r.get("msg_id")) in huerf:\n                    out.append({"cns_id": k, **r, "huerfana": True})', 'if (k, r.get("msg_id")) in huerf:\n                    out.append({"cns_id": k, **r})'),
 "M27 (H-08) relanzar no mira lo entregado": ("bloque_a/interfaz_broker.py", 'if hecho and actual.get("estado") in ("EN_CURSO", "INTERRUMPIDA"):', "if False:"),
 "M28 (H-08) no incrementa el intento": ("bloque_a/interfaz_broker.py", '"intentos": int(actual.get("intentos") or 0) + 1})', '"intentos": int(actual.get("intentos") or 0)})'),
 "M29 (H-09) alta tras escribir la reserva": ("bloque_a/interfaz_broker.py", "                if rev and ejecutar_revision:   # ronda de cierre (H-09)", "                if False:   # ronda de cierre (H-09)"),
 "M30 (H-09) sin baja si falla la escritura": ("bloque_a/interfaz_broker.py", "            if clave:\n                self._en_marcha(cns_id, msg[\"msg_id\"], False)", "            if False:\n                pass"),
 "M31 (H-10) clave sin carpeta": ("bloque_a/interfaz_broker.py", 'clave = (str(Path(self.b.almacen.carpeta).resolve()), cns_id, msg_id)', 'clave = ("", cns_id, msg_id)'),
 "M32 (H-11) sin marca de no juzgable": ("bloque_a/interfaz_broker.py", 'out.append({"cns_id": k, **r, "huerfana": None, "nota_huerfana": "no se puede juzgar desde este host"})', 'out.append({"cns_id": k, **r})'),
 "M33 (H-11) otro host se juzga por el pid": ("bloque_a/interfaz_broker.py", 'if not p or p.get("host") != socket.gethostname():\n            return None', 'if not p:\n            return None'),
 "M21 (H-06) relanzar sin reclamar": ("bloque_a/interfaz_broker.py", '                if not actual or actual.get("estado") not in estados:\n                    continue', '                if not actual:\n                    continue'),
}
FILTRO = sys.argv[3] if len(sys.argv) > 3 else ""   # p. ej. «H-07|H-08»: solo los mutantes cuyo nombre lo contenga
vivos = []
M = {"M0 sin mutar (debe VIVIR)": ("bloque_a/interfaz_broker.py", "MODOS = ", "MODOS = "), **M}
for nombre, (f, a, b) in M.items():
    if FILTRO and not nombre.startswith("M0") and not any(x in nombre for x in FILTRO.split("|")):
        continue
    if TMP.exists(): shutil.rmtree(TMP)
    shutil.copytree(SRC, TMP, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    p = TMP / "11_Ejecutor" / f; s = p.read_text(encoding="utf-8")
    assert s.count(a) == 1, (nombre, s.count(a)); p.write_text(s.replace(a, b), encoding="utf-8")
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "tests/test_t174_pb61_revision_c2.py"], cwd=TMP / "11_Ejecutor", capture_output=True, text=True)
    estado = "MUERE" if r.returncode else "VIVE"
    print(f"{nombre}: {estado}", flush=True)
    if (not r.returncode) != nombre.startswith("M0"): vivos.append(nombre)
print("vivos:", vivos); sys.exit(1 if vivos else 0)
