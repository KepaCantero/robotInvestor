"""Mutantes propios de T-196: aplica cada mutación, corre tests/test_t196.py y restaura.
Uso (desde bloque_a/11_Ejecutor): ../../.venv/bin/python ../../.docs/tickets/T-196/mutantes.py . [M1 M2 …] (solo esos)
Un mutante que cuelga la suite (más de TIEMPO segundos) cuenta como muerto: la prueba lo detecta (no termina)."""
import subprocess
import sys
from pathlib import Path

EJ = Path(sys.argv[1])
TIEMPO = 900
COLA, RF, ORQ, CLI = "bloque_a/cola_peticiones.py", "bloque_a/respuesta_final.py", "bloque_a/orquestacion.py", "bloque_a/cli.py"
M = [
 ("M1 sin envejecimiento", COLA, "min(math.floor(espera_h) * float(", "min(0 * float("),
 ("M2 envejecimiento sin máximo", COLA, "                             float(parametro(self.cfg, \"cola_peticiones.envejecimiento_max\")))",
  "                             math.inf)"),
 ("M3 envejecimiento continuo", COLA, "min(math.floor(espera_h) * float(", "min(espera_h * float("),
 ("M4 sin urgencia", COLA, "            if margen_h < float(", "            if False and margen_h < float("),
 ("M5 urgencia en el margen justo", COLA, "            if margen_h < float(", "            if margen_h <= float("),
 ("M6 desempate por nivel invertido", COLA, "-p[\"_prioridad\"][\"efectiva\"], NIVELES.index(p[\"nivel\"]),",
  "-p[\"_prioridad\"][\"efectiva\"], -NIVELES.index(p[\"nivel\"]),"),
 ("M7 desempate por llegada invertido", COLA, "                                          self._instante(p[\"recibida\"]), p[\"_llegada\"]))",
  "                                          -p[\"_llegada\"]))"),
 ("M8 menor prioridad primero", COLA, "key=lambda p: (-p[\"_prioridad\"][\"efectiva\"]", "key=lambda p: (p[\"_prioridad\"][\"efectiva\"]"),
 ("M9 instante anterior admitido", COLA, "        if espera_h < 0:", "        if False:"),
 ("M10 prioridad sin validar", COLA, "        if prioridad not in PRIORIDADES:", "        if False:"),
 ("M11 nivel N0 admitido", COLA, "if forzado is not None and forzado not in NIVELES:", "if forzado is not None and forzado not in (*NIVELES, \"N0\"):"),
 ("M12 fecha sin formato", COLA, "        if not RE_FECHA_HORA.fullmatch(valor):", "        if False:"),
 ("M13 N3 sin repartir", COLA, "    if tipo != \"PERIODICO\" and any(nivel[c] == \"N3\" for c in clases):", "    if False:"),
 ("M14 toma sin transacción", COLA, "        with self.almacen._transaccion():\n            orden = self.orden(t)",
  "        if True:\n            orden = self.orden(t)"),
 ("M15 la toma no marca EN_CURSO", COLA, "            self.almacen.escribir(\"F5\", \"AG-01\", {\"tipo_entrada\": \"PETICION\", \"id\": pet[\"id\"], \"estado\": \"EN_CURSO\",",
  "            dict(**{\"tipo_entrada\": \"PETICION\", \"id\": pet[\"id\"], \"estado\": \"EN_CURSO\","),
 ("M16 fallo sin registrar", COLA, "            self._fallida(pet, type(e).__name__, t)\n", "            pass\n"),
 ("M17 sin final al atender", COLA, "            servida[\"respuesta_final\"] = respuesta_final.enviar(", "            servida[\"respuesta_final\"] = (lambda *a: None)("),
 ("M18 escalado sin el RUN-", COLA, "            self._escalado(pet[\"qry_id\"], res[\"run_id\"], res[\"estado\"])", "            pass"),
 ("M19 consulta escalada nunca en cola", RF, "    return pet.get(\"tipo_entrada\") == \"PETICION\" and pet.get(\"estado\") in (\"ENCOLADA\", \"EN_CURSO\")",
  "    return False"),
 ("M20 EN_CURSO no cuenta como en cola", RF, "pet.get(\"estado\") in (\"ENCOLADA\", \"EN_CURSO\")", "pet.get(\"estado\") in (\"ENCOLADA\",)"),
 ("M21 pendientes no salta las de la cola", RF, "                and not consulta_en_cola(almacen, q)):", "                and True):"),
 ("M22 enviar no salta las de la cola", RF, "        if consulta_en_cola(almacen, qry):", "        if False:"),
 ("M23 pendientes con la fecha de la consulta", RF, "q[\"_ultima_fecha\"] if q.get(\"peticion_cola\") else ", ""),
 ("M24 la consulta encola y además ejecuta", ORQ, "            elif ejecutar_escalado:", "            if ejecutar_escalado:"),
 ("M25 prioridad de la consulta fija", COLA, "\"prioridad\": self._prioridad_de_consulta(urgencia),", "\"prioridad\": \"NORMAL\","),
 ("M26 posición contada desde 0", COLA, "        return {\"posicion\": k + 1,", "        return {\"posicion\": k,"),
 ("M27 UC por delante con la propia", COLA, "float(p[\"presupuesto_uc\"]) for p in orden[:k]", "float(p[\"presupuesto_uc\"]) for p in orden[:k + 1]"),
 ("M28 máximo sin validar", COLA, "        if maximo is not None and (isinstance(maximo, bool)", "        if False and (isinstance(maximo, bool)"),
 ("M29 la consulta no anota la PET-", ORQ, "            entrada[\"peticion_cola\"] = en_cola[\"nueva\"][\"id\"]", "            pass"),
 ("M30 urgencia de consulta sin validar", ORQ, "            self.cola._prioridad_de_consulta(urgencia)\n", ""),
 ("M31 el RUN- sin pet_id", COLA, "        disparador = {\"origen\": pet[\"origen\"], \"msg_id\": pet[\"msg_id\"], \"pet_id\": pet[\"id\"]}",
  "        disparador = {\"origen\": pet[\"origen\"], \"msg_id\": pet[\"msg_id\"]}"),
 ("M32 las ATENDIDAS vuelven a la cola", COLA, "    def _en_cola(self, estados=(\"ENCOLADA\",), hasta",
  "    def _en_cola(self, estados=(\"ENCOLADA\", \"ATENDIDA\"), hasta"),
 ("M33 _reparto sin la regla compartida", ORQ, "        asign = presupuesto_por_clase(self.cfg, tipo, clases, nivel)",
  "        asign = {c: float(parametro(self.cfg, f\"presupuesto_uc.{nivel[c]}\")) for c in clases}"),
 # r02 (QA r01): los vivos del revisor (H-08 y H-09; R11 es equivalente) y lo nuevo de la ronda
 ("M34 R2 PERIODICO sin pasar a AD_HOC", COLA, "        tipo = \"AD_HOC\" if tipo == \"PERIODICO\" else tipo", "        pass"),
 ("M35 R4 clases sin filtrar por las activas", COLA, "if c in activas]   # las que", "if True]   # las que"),
 ("M36 R6 solo Exception", COLA, "        except BaseException as e:   # se registra", "        except Exception as e:   # se registra"),
 ("M37 R9 consulta encolada con el as_of del llamante", ORQ, "            as_of = instante_cola.tz_localize(None).normalize()\n", ""),
 ("M38 R10 CLI consulta encolada sin instante", CLI, "instante=_instante(a, bloque) if a.encolar_escalado else None)", "instante=None)"),
 ("M39 R12 la FALLIDA sin run_id", COLA, "\"error\": error, \"run_id\": run_id, \"fin\"", "\"error\": error, \"run_id\": None, \"fin\""),
 ("M40 R13 la ATENDIDA sin estado_run", COLA, "\"run_id\": res[\"run_id\"], \"estado_run\": res[\"estado\"]})", "\"run_id\": res[\"run_id\"]})"),
 ("M41 H-01 sin filtrar por recibida", COLA, "                if hasta is not None and self._instante(e.get(\"recibida\")) > hasta:",
  "                if False:"),
 ("M42 H-01 reloj de un solo instante", COLA, "        reloj = instante if callable(instante) else (lambda: instante)",
  "        _fijo = instante() if callable(instante) else instante\n        reloj = (lambda: _fijo)"),
 ("M43 H-07 sin exigir clases", COLA, "        previa = self._nueva(\"PET-?\", datos, t, exigir_clases=True)",
  "        previa = self._nueva(\"PET-?\", datos, t, exigir_clases=False)"),
 ("M44 H-03 huérfana sin incidencia", COLA, "            if pid not in avisadas:", "            if False:"),
 ("M45 H-03 incidencia repetida", COLA, "            if pid not in avisadas:", "            if True:"),
 ("M46 H-03 la toma sin el proceso", COLA, "\"orden_servicio\": k, **_proceso()})", "\"orden_servicio\": k})"),
 ("M47 H-03 reconcilia una no huérfana", COLA, "            if e.get(\"tipo_entrada\") != \"PETICION\" or not self._es_huerfana(pet_id, e):",
  "            if e.get(\"tipo_entrada\") != \"PETICION\":"),
 ("M48 H-03 reconciliar sin final", COLA, "            final = respuesta_final.enviar(self.bloque, pet[\"qry_id\"], None, fin.tz_localize(None).normalize())",
  "            final = None"),
 ("M49 H-03 enviar_pendientes no avisa", RF, "        cola.huerfanas()\n", "        pass\n"),
 ("M50 H-03 reconciliar con el día del reloj", COLA, "        self.bloque.fijar_fecha(fin.tz_localize(None).normalize())   # la FALLIDA",
  "        (lambda *a: None)(fin.tz_localize(None).normalize())   # la FALLIDA"),
 ("M51 H-05 sin comprobar el cambio de hora", COLA, "        if cero.utcoffset() != uno.utcoffset():", "        if False:"),
 ("M52 H-04 nanosegundos sin truncar", COLA, "        valor = pd.Timestamp(valor).floor(\"us\")", "        pass"),
 ("M53 H-06 servir sin comprobar la toma", COLA,
  "        if actual.get(\"tipo_entrada\") != \"PETICION\" or actual.get(\"estado\") != \"EN_CURSO\" or actual.get(\"pid\") != os.getpid():",
  "        if False:"),
 ("M55 R7 recepción sin transacción", COLA, "        with self.almacen._transaccion():\n            plazo = self._plazo(nueva, t)",
  "        if True:\n            plazo = self._plazo(nueva, t)"),
 ("M54 H-03 la de este proceso nunca huérfana", COLA, "                return self._clave(pet_id) not in _EN_MARCHA", "                return False"), # r03 (QA r02): N-01, N-02 y los vivos del revisor (Q2, Q8, Q10, Q11)
 ("M56 N-01 deja de estar en marcha antes de servir", COLA, "            return self._servir_en_marcha(pet, t)",
  "            with _EN_MARCHA_LOCK:\n                _EN_MARCHA.discard(self._clave(pet[\"id\"]))\n            return self._servir_en_marcha(pet, t)"),
 ("M57 N-02 reloj que retrocede admitido", COLA, "            if t < previo:", "            if False:"),
 ("M58 Q2 huérfana sin mirar el host", COLA, "if e.get(\"estado\") != \"EN_CURSO\" or e.get(\"host\") != _proceso()[\"host\"]:",
  "if e.get(\"estado\") != \"EN_CURSO\":"),
 ("M59 Q8 servir sin mirar el proceso", COLA, " or actual.get(\"pid\") != os.getpid():", ":"),
 ("M60 Q10 atender sin el día de la toma", COLA,
  "            self.bloque.fijar_fecha(t.tz_localize(None).normalize())   # r02: lo que se escribe", "            pass   # r02: lo que se escribe"),
 ("M61 Q11 el pid vivo cuenta como huérfana", COLA, "        return _pid_vivo(e.get(\"pid\")) is False", "        return _pid_vivo(e.get(\"pid\")) is not None"),
 # ronda de cierre de la QA r03 (M-01): P1 del revisor
 ("M62 P1 el retroceso solo contra el primer instante", COLA, "            previo = t\n", ""),
]
vivos = []
SOLO = sys.argv[2:]
M = [m for m in M if not SOLO or m[0].split()[0] in SOLO]
for nombre, f, a, b in M:
    p = EJ / f
    orig = p.read_text(encoding="utf-8")
    assert orig.count(a) == 1, (nombre, orig.count(a))
    p.write_text(orig.replace(a, b), encoding="utf-8")
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "tests/test_t196.py"],
                           cwd=EJ, capture_output=True, text=True, check=False, timeout=TIEMPO)
        muerto = r.returncode != 0
    except subprocess.TimeoutExpired:
        muerto = True
    finally:
        p.write_text(orig, encoding="utf-8")
    print(f"{nombre}: {'MUERTO' if muerto else 'VIVO'}", flush=True)
    if not muerto:
        vivos.append(nombre)
print(f"{len(M) - len(vivos)} muertos, {len(vivos)} vivos: {vivos}")
sys.exit(1 if vivos else 0)
