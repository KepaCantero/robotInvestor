"""QA r02 de T-196 (revisor): mutantes propios de las correcciones de la r02. Uso (desde bloque_a/11_Ejecutor):
../../.venv/bin/python ../../.docs/tickets/T-196/revisores/r02_mutantes.py . [Q1 Q2 …]"""
import subprocess
import sys
from pathlib import Path

EJ = Path(sys.argv[1])
TIEMPO = 900
COLA, RF, ORQ, CLI = "bloque_a/cola_peticiones.py", "bloque_a/respuesta_final.py", "bloque_a/orquestacion.py", "bloque_a/cli.py"
M = [
 ("Q1 la incidencia de huérfana se repite", COLA, "            if pid not in avisadas:", "            if True:"),
 ("Q2 huérfana sin mirar el host", COLA, "if e.get(\"estado\") != \"EN_CURSO\" or e.get(\"host\") != _proceso()[\"host\"]:",
  "if e.get(\"estado\") != \"EN_CURSO\":"),
 ("Q3 reconciliar sin exigir huérfana", COLA, "if e.get(\"tipo_entrada\") != \"PETICION\" or not self._es_huerfana(pet_id, e):\n                raise",
  "if e.get(\"tipo_entrada\") != \"PETICION\":\n                raise"),
 ("Q4 el orden ve las posteriores", COLA, "                if hasta is not None and self._instante(e.get(\"recibida\")) > hasta:",
  "                if False:"),
 ("Q5 atender con un solo instante", COLA, "        reloj = instante if callable(instante) else (lambda: instante)",
  "        reloj = (lambda v=(instante() if callable(instante) else instante): v)"),
 ("Q6 sin rechazo del cambio de hora", COLA, "        if cero.utcoffset() != uno.utcoffset():", "        if False:"),
 ("Q7 CT-01 sin clases activas admitido", COLA, "previa = self._nueva(\"PET-?\", datos, t, exigir_clases=True)",
  "previa = self._nueva(\"PET-?\", datos, t, exigir_clases=False)"),
 ("Q8 servir sin mirar el proceso", COLA, " or actual.get(\"pid\") != os.getpid():", ":"),
 ("Q9 enviar_pendientes sin avisar de huérfanas", RF, "        cola.huerfanas()\n", "        pass\n"),
 ("Q10 atender sin el día de la toma", COLA,
  "            self.bloque.fijar_fecha(t.tz_localize(None).normalize())   # r02: lo que se escribe", "            pass   # r02: lo que se escribe"),
 ("Q11 el pid vivo cuenta como huérfana", COLA, "        return _pid_vivo(e.get(\"pid\")) is False", "        return _pid_vivo(e.get(\"pid\")) is not None"),
 ("Q12 nanosegundos sin truncar", COLA, "        valor = pd.Timestamp(valor).floor(\"us\")", "        pass"),
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
