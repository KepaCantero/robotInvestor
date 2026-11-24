"""Mutantes propios de T-198: aplica cada mutación, corre tests/test_t198_buscador_ct19.py y restaura.
Uso (desde bloque_a/11_Ejecutor, o con la ruta de una copia): ../../.venv/bin/python ../../.docs/tickets/T-198/mutantes.py ."""
import subprocess
import sys
from pathlib import Path

EJ = Path(sys.argv[1])
FIA, ALM, ORQ = "bloque_a/fiabilidad_f9.py", "bloque_a/almacen.py", "bloque_a/orquestacion.py"
M = [
 # comprobación del CT-19 (falla cerrado)
 ("M1 cualquier emisor o receptor", FIA, "    if (msg.get(\"contrato\"), msg.get(\"emisor\"), msg.get(\"receptor\")) != (\"CT-19\", \"AG-20\", \"AG-16\"):",
  "    if msg.get(\"contrato\") != \"CT-19\":"),
 ("M2 cualquier tipo", FIA, "    if msg.get(\"tipo\") != \"FIABILIDAD_FUENTES\":", "    if False:"),
 ("M3 sin fuentes admitido", FIA, "    if not isinstance(fuentes, list) or not fuentes:", "    if not isinstance(fuentes, list):"),
 ("M4 campos de más o de menos", FIA, " or set(f) != set(CAMPOS_CT19):", ":"),
 ("M5 fue_id repetido admitido", FIA, " or fue_id in vistos:", ":"),
 ("M6 FUE- ausente admitida", FIA, "        if fue is None:\n            raise", "        if fue is None:\n            continue\n            raise"),
 ("M7 sin cotejo con F6", FIA, "        distintos = [k for k in CAMPOS_CT19 if fue.get(k) != f[k]]", "        distintos = []"),
 ("M8 sin cotejo del comunicado", FIA, "        if fue.get(\"comunicado_ct19\") != msg_id:", "        if False:"),
 ("M9 ref_id fuera de F9 admitido", FIA, "        if not fuente_de_opinion_registrada(f[\"ref_id\"], referencias):", "        if False:"),
 ("M10 sin msg_id admitido", FIA, "    if not isinstance(msg_id, str) or not msg_id:", "    if False:"),
 ("M11 no objeto admitido", FIA, "    if not isinstance(msg, dict):\n        raise", "    if False:\n        raise"),
 # escritura
 ("M12 sin transacción", FIA, "    with almacen._transaccion():\n        f6 = _fue_de_f6", "    if True:\n        f6 = _fue_de_f6"),
 ("M13 duplica lo atendido", FIA, "        nuevas = [f for f in fuentes if f[\"fue_id\"] not in hechas]", "        nuevas = list(fuentes)"),
 ("M14 escribe mientras comprueba (orden)", FIA, "        fuentes = comprobar_ct19(msg, f6, bloque.referencias, as_of)\n",
  "        fuentes = msg.get(\"fuentes\") if isinstance(msg, dict) and isinstance(msg.get(\"fuentes\"), list) else []\n"
  "        for _f in fuentes[:1]:\n            almacen.escribir(\"F9\", \"AG-16\", {\"tipo_entrada\": \"FIABILIDAD_MEDIDA\", \"ref_id\": _f.get(\"ref_id\") if isinstance(_f, dict) else None})\n"
  "        fuentes = comprobar_ct19(msg, f6, bloque.referencias, as_of)\n"),
 ("M15 resueltos = registrados", FIA, "\"resueltos\": f[\"n\"],", "\"resueltos\": registrados.get(f[\"ref_id\"], 0),"),
 ("M16 sin recibido_via", FIA, "\"recibido_via\": msg[\"msg_id\"],", "\"recibido_via\": None,"),
 ("M17 recalificación hecha", FIA, "\"recalificacion_q\": \"PENDIENTE\"", "\"recalificacion_q\": \"HECHA\""),
 ("M18 sin calc_id", FIA, "\"calc_id\": fue.get(\"calc_id\"),", "\"calc_id\": None,"),
 ("M19 registrados de todas las fuentes", FIA, "            cuenta[pf[\"ref_id\"]] = cuenta.get(pf[\"ref_id\"], 0) + 1",
  "            cuenta[pf[\"ref_id\"]] = len(almacen.estado(\"F2\", as_of, clave=\"clm_id\"))"),
 ("M20 ventana a mano", FIA, "    ventana = int(parametro(bloque.cfg, \"fiabilidad_fuentes.ventana_meses\"))", "    ventana = 12"),
 # pendientes, orden y contexto
 ("M21 reenvía lo atendido", FIA, " if f.get(\"fue_id\") not in hechas),", "),"),
 ("M22 orden inverso", FIA, "key=lambda f: (str(f.get(\"periodo\")), str(f.get(\"fue_id\"))))",
  "key=lambda f: (str(f.get(\"periodo\")), str(f.get(\"fue_id\"))), reverse=True)"),
 ("M23 anota también F7", FIA, "        if r.get(\"archivo\") == \"F9\" and r.get(\"ref_id\") in medida:", "        if r.get(\"ref_id\") in medida:"),
 ("M24 contexto con fuga", FIA, "            for ref, e in almacen.estado(\"F9\", as_of, clave=\"ref_id\").items()",
  "            for ref, e in almacen.estado(\"F9\", None, clave=\"ref_id\").items()"),
 # ciclo
 ("M25 el ciclo no atiende", ORQ, "                return fiabilidad_f9.atender_ct19(self, msg, as_of, run_id)", "                return []"),
 ("M26 sin incidencia", ORQ, "                self.almacen.incidencia(\"DATOS\", f\"CT-19 {msg['msg_id']} no atendido", "                (lambda *a, **k: None)(\"DATOS\", f\"CT-19 {msg['msg_id']} no atendido"),
 ("M27 sin anotar el comunicado", ORQ, "                self.almacen.escribir(\"F6\", \"AG-20\", {\"tipo_entrada\": \"FUE\", \"id\": f[\"fue_id\"], \"comunicado_ct19\": msg[\"msg_id\"]})",
  "                pass"),
 ("M28 el Buscador no ve la fiabilidad", ORQ, "        fiabilidad_f9.anotar_candidatas(self.almacen, as_of, cand[\"referencias\"])", "        pass"),
 ("M29 solo las nuevas (sin reintento)", ORQ, "            fue = fiabilidad_f9.por_comunicar(self.almacen, as_of)",
  "            fue = [f for f in fiabilidad_f9.por_comunicar(self.almacen, as_of) if not f.get(\"comunicado_ct19\")]"),
 # almacén
 ("M30 cualquiera escribe F9", ALM, "\"F9\": {\"AG-16\"}", "\"F9\": {\"AG-16\", \"AG-20\"}"),
 ("M31 cualquier tipo en F9", ALM, "        if archivo == \"F9\" and tipo not in TIPOS_F9:", "        if False:"),
 ("M32 sin sellar el archivo nuevo", ALM, "            for archivo in nuevos:\n                sellos[archivo] = self._ultimo([])\n", ""),
 ("M33 sella también el que existe", ALM, " and not (self.carpeta / ARCHIVOS[a]).exists()]", "]"),
 ("M34 no guarda el sello nuevo", ALM, "            elif nuevos:\n                self._guardar_json(self._ruta_sellos, sellos)\n", ""),
 # r02: los del revisor (revisores/r01_mutantes.py, R1–R6) y los de las correcciones
 ("R1 F2 sin as_of (fuga en pronosticos_registrados)", FIA, "    for clm in almacen.estado(\"F2\", as_of, clave=\"clm_id\").values():",
  "    for clm in almacen.estado(\"F2\", None, clave=\"clm_id\").values():"),
 ("R2 F6 sin as_of al atender (fuga)", FIA, "    with almacen._transaccion():\n        f6 = _fue_de_f6(almacen, as_of)",
  "    with almacen._transaccion():\n        f6 = _fue_de_f6(almacen, None)"),
 ("R3 sin métrica", FIA, "\"metrica\": fue.get(\"metodo\"),", "\"metrica\": None,"),
 ("R4 el ciclo sin cerrojo (dos procesos)", ORQ, "        with self.almacen._transaccion():\n            fue = fiabilidad_f9.por_comunicar(self.almacen, as_of)",
  "        if True:\n            fue = fiabilidad_f9.por_comunicar(self.almacen, as_of)"),
 ("R5 el CT-07 del ciclo con fuga (sin as_of)", ORQ, "        fiabilidad_f9.anotar_candidatas(self.almacen, as_of, cand[\"referencias\"])",
  "        fiabilidad_f9.anotar_candidatas(self.almacen, None, cand[\"referencias\"])"),
 ("R6 registrados de cualquier tipo de afirmación", FIA, "        if clm.get(\"tipo_afirmacion\") == \"PRONOSTICO_FUENTE\" and isinstance(pf, dict)",
  "        if isinstance(pf, dict)"),
 ("M35 H-01 sin apartar las no atendibles", ORQ, "            fue = fiabilidad_f9.apartar_no_atendibles(self.almacen, fue, self.referencias, run_id)", "            pass"),
 ("M36 H-01 se reenvían las declaradas", FIA, "    hechas = atendidas(almacen, as_of) | no_atendibles(almacen, as_of)", "    hechas = atendidas(almacen, as_of)"),
 ("M37 H-01 sin marca durable", FIA, "                           fue_no_atendible=f.get(\"fue_id\"), tratamiento=", "                           tratamiento="),
 ("M38 H-02 sella vacío cualquier archivo", ALM, "[a for a in ARCHIVOS_NUEVOS if a not in sellos", "[a for a in ARCHIVOS if a not in sellos"),
 ("M39 H-03 sin comprobar el timestamp", FIA, "    _fecha_del_mensaje(msg, as_of)\n", ""),
 ("M40 H-03 posterior a as_of admitido", FIA, "    if as_of is not None and fecha.isoformat() > str(as_of)[:10]:", "    if False:"),
 ("M41 H-03 timestamp no ISO admitido", FIA, "    if not isinstance(ts, str) or not RE_FECHA_ISO.fullmatch(ts.strip()):", "    if not isinstance(ts, str):"),
 ("M43 H-08 sin la guarda de F9 ilegible", FIA, "    if fues and not (getattr(referencias, \"fichas\", None) or {}).get(\"F9\"):", "    if False:"),
 ("M44 H-08 la guarda deja pasar el CT-19", FIA, "                           tratamiento=\"sin marca; reintento en el ciclo siguiente\")\n        return []",
  "                           tratamiento=\"sin marca; reintento en el ciclo siguiente\")\n        return fues"),
 ("M42 H-03 sin as_of al comprobar", FIA, "        fuentes = comprobar_ct19(msg, f6, bloque.referencias, as_of)\n", "        fuentes = comprobar_ct19(msg, f6, bloque.referencias)\n"),
]
vivos = []
for nombre, f, a, b in M:
    p = EJ / f
    orig = p.read_text(encoding="utf-8")
    assert orig.count(a) == 1, (nombre, orig.count(a))
    p.write_text(orig.replace(a, b), encoding="utf-8")
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "tests/test_t198_buscador_ct19.py"],
                           cwd=EJ, capture_output=True, text=True, check=False)
    finally:
        p.write_text(orig, encoding="utf-8")
    muerto = r.returncode != 0
    print(f"{nombre}: {'MUERTO' if muerto else 'VIVO'}", flush=True)
    if not muerto:
        vivos.append(nombre)
print(f"{len(M) - len(vivos)} de {len(M)} muertos" + (f"; vivos: {vivos}" if vivos else ""))
sys.exit(1 if vivos else 0)
