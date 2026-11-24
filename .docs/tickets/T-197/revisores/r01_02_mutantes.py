"""T-197 QA r01 · mutantes del revisor (además de los 32 de `mutantes.py`). Aplica cada mutación en una COPIA del ejecutor,
corre las pruebas de PB-09 y restaura.

Uso: python r01_02_mutantes.py <copia de bloque_a/11_Ejecutor> [R1 R2 …]
(la copia, p. ej. de `git archive HEAD bloque_a`, para no tocar el árbol de trabajo mientras corren otras pruebas)."""
import subprocess
import sys
from pathlib import Path

EJ = Path(sys.argv[1])
HT05, PLAN, ORQ, CLI = ("bloque_a/herramientas/ht05_planificador.py", "bloque_a/planificacion_c1.py", "bloque_a/orquestacion.py",
                        "bloque_a/cli.py")
PRUEBAS = ["tests/test_t197_periodicidad.py",
           "tests/test_t87_contratos.py::test_ct04_conserva_frecuencia_y_aplica_desde_fecha_efecto"]
M = [
 ("R1 la CLI dispara siempre (sin --ejecutar también)", CLI, "disparar(bloque, as_of, ejecutar=a.ejecutar)", "disparar(bloque, as_of, ejecutar=True)"),
 ("R2 la CLI nunca dispara", CLI, "disparar(bloque, as_of, ejecutar=a.ejecutar)", "disparar(bloque, as_of, ejecutar=False)"),
 ("R3 cambio de P-01 el mismo día del C1 ignorado", PLAN, "if dia < f <= c.date()", "if dia < f < c.date()"),
 ("R4 entrega en el mismo instante que la ejecución", HT05, "if cand > ejecucion_dt and", "if cand >= ejecucion_dt and"),
 ("R5 ancla quincenal en la semana del inicio", HT05, "    return primero - dt.timedelta(days=primero.weekday())",
  "    return inicio - dt.timedelta(days=inicio.weekday())"),
 ("R6 entrega a la hora exacta: RECUPERADO → EMITIDO", PLAN, "(\"RECUPERADO\" if t >= entrega else \"EMITIDO\")",
  "(\"RECUPERADO\" if t > entrega else \"EMITIDO\")"),
 ("R7 mensual sin el día 7", HT05, "        return dia.day <= 7", "        return dia.day < 7"),
 ("R8 el C1 a su minuto exacto no se dispara", HT05, "and _en_hora(dia, ejecucion) <= hasta:", "and _en_hora(dia, ejecucion) < hasta:"),
 ("R9 la entrega diaria exige el día de la semana", HT05, "(periodicidad == \"DIARIA\" or dia.weekday() == d)", "dia.weekday() == d"),
 ("R10 el planificador ve cambios de F10 posteriores a ahora", PLAN,
  "    est = bloque.almacen.estado(\"F10\", str(conocido.date()), efectivo_el=str(dia)).get(\"P-01\")",
  "    est = bloque.almacen.estado(\"F10\", None, efectivo_el=str(dia)).get(\"P-01\")"),
 ("R11 sin segundos a cero", PLAN, "    return t.to_pydatetime().replace(second=0, microsecond=0)", "    return t.to_pydatetime()"),
 ("R12 el CT-04 ignora el P-01 vigente", ORQ, "ht05.leer_p01(calendario or ht05.P01_INICIAL)", "ht05.leer_p01(ht05.P01_INICIAL)"),
 ("R13 franja abierta por abajo", HT05, "    if desde_h <= hora // 60 < hasta_h:", "    if desde_h < hora // 60 < hasta_h:"),
 ("R14 diaria: límite del día anterior estricto", HT05, "and hh * 60 + mm - adelanto < 0:", "and hh * 60 + mm - adelanto <= 0:"),
 ("R15 el P-01 de dos partes no deduce la ejecución", PLAN,
  "        ejecucion = ht05.ejecucion_para_entrega(periodicidad, entrega, parametro(bloque.cfg, \"planificador\"))",
  "        ejecucion = \"SAB 06:00\""),
 ("R16 sin fecha del almacén en el disparo", PLAN, "    bloque.fijar_fecha(t)\n", ""),
 ("R17 el disparo no apunta el P-01", PLAN, "**{k: prog[k] for k in (\"programado\", \"entrega\", \"p01\", \"cfg_id\")}",
  "**{k: prog[k] for k in (\"programado\", \"entrega\")}"),
]
SOLO = set(sys.argv[2:])
if SOLO:
    M = [m for m in M if m[0].split()[0] in SOLO]
vivos = []
for nombre, f, a, b in M:
    p = EJ / f
    orig = p.read_text(encoding="utf-8")
    assert orig.count(a) == 1, (nombre, orig.count(a))
    p.write_text(orig.replace(a, b), encoding="utf-8")
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS],
                           cwd=EJ, capture_output=True, text=True, check=False)
    finally:
        p.write_text(orig, encoding="utf-8")
    muerto = r.returncode != 0
    print(f"{nombre}: {'MUERTO' if muerto else 'VIVO'}", flush=True)
    if not muerto:
        vivos.append(nombre)
print(f"{len(M) - len(vivos)} muertos de {len(M)}; vivos: {vivos}")
sys.exit(1 if vivos else 0)
