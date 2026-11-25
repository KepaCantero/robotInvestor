"""QA r01 de T-196 (revisor independiente): mutantes propios de lo esencial que no cubren los 33 del implementador. Aplica cada
mutación, corre tests/test_t196.py y restaura. Uso (desde bloque_a/11_Ejecutor):
../../.venv/bin/python ../../.docs/tickets/T-196/revisores/r01_mutantes.py . [R1 R2 …]"""
import subprocess
import sys
from pathlib import Path

EJ = Path(sys.argv[1])
TIEMPO = 900
COLA, RF, ORQ, CLI = "bloque_a/cola_peticiones.py", "bloque_a/respuesta_final.py", "bloque_a/orquestacion.py", "bloque_a/cli.py"
M = [
 ("R1 recibir sin idempotencia", COLA, "        res, repetido = self.bloque.mensajeria.procesar_una_vez(msg, _proc)",
  "        res, repetido = _proc(msg), False"),
 ("R2 PERIODICO sin pasar a AD_HOC", COLA, "        tipo = \"AD_HOC\" if tipo == \"PERIODICO\" else tipo", "        pass"),
 ("R3 PROFUNDIZACION sin N3", COLA, "nivel = forzado or (\"N3\" if tipo == \"PROFUNDIZACION\" else \"N2\")", "nivel = forzado or \"N2\""),
 ("R4 clases sin filtrar por las activas", COLA, "if c in activas]   # las que", "if True]   # las que"),
 ("R5 fallo sin incidencia", COLA, "        self.almacen.incidencia(\"HERRAMIENTA\", f\"La petición", "        (lambda *a, **k: None)(\"HERRAMIENTA\", f\"La petición"),
 ("R6 solo Exception (KeyboardInterrupt sin FALLIDA)", COLA, "        except BaseException as e:   # se registra", "        except Exception as e:   # se registra"),
 ("R7 recepción sin transacción", COLA, "        with self.almacen._transaccion():\n            plazo = self._plazo(nueva, t)",
  "        if True:\n            plazo = self._plazo(nueva, t)"),
 ("R8 urgencia medida desde la recepción", COLA, "margen_h = (self._instante(pet[\"fecha_objetivo\"]) - t)", "margen_h = (self._instante(pet[\"fecha_objetivo\"]) - recibida)"),
 ("R9 consulta encolada con el as_of del llamante", ORQ, "            as_of = instante_cola.tz_localize(None).normalize()\n", ""),
 ("R10 CLI consulta encolada sin instante", CLI, "instante=_instante(a, bloque) if a.encolar_escalado else None)", "instante=None)"),
 ("R11 fecha_objetivo sin normalizar a la zona", COLA,
  "fecha_objetivo = None if fo is None else _fecha_hora(fo, self.bloque.reloj.zona, \"fecha_objetivo\").isoformat()",
  "fecha_objetivo = None if fo is None else (_fecha_hora(fo, self.bloque.reloj.zona, \"fecha_objetivo\") and fo)"),
 ("R12 la FALLIDA sin run_id", COLA, "\"error\": error, \"run_id\": run_id, \"fin\"", "\"error\": error, \"run_id\": None, \"fin\""),
 ("R13 la ATENDIDA sin estado_run", COLA, "\"run_id\": res[\"run_id\"], \"estado_run\": res[\"estado\"]})", "\"run_id\": res[\"run_id\"]})"),
 ("R14 el acuse sin presupuesto", COLA, "nivel=res[\"nivel\"], presupuesto_uc=res[\"presupuesto_uc\"],", "nivel=res[\"nivel\"],"),
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
