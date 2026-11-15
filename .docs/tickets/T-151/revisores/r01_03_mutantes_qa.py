"""QA r01 de T-151 · mutantes propios del revisor (distintos de N01–N18 de `mutantes_t151.py`).

Uso: python r01_03_mutantes_qa.py <copia desechable con «qa24_» y «_mut» en la ruta y `bloque_a/` entero>
Cada mutante se aplica, se pasan `tests/test_t151_reintentos.py` y `tests/test_t146_presupuesto.py` (con -x) y se restaura.
Vivo = ninguna prueba lo detecta. Termina con 1 si alguno no aplica (texto no encontrado una vez); los vivos se informan."""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "qa24_" in str(COPIA) and "_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir()
CO, LL, OR = (f"bloque_a/11_Ejecutor/bloque_a/{f}.py" for f in ("consumo", "llm", "orquestacion"))
PRUEBAS = ["tests/test_t151_reintentos.py", "tests/test_t146_presupuesto.py"]
MUT = [
    ("Q01", "el SDK recibido sale con un reintento propio", LL, "sdk = sdk.with_options(max_retries=0)",
     "sdk = sdk.with_options(max_retries=1)"),
    ("Q02", "un timeout nunca cuenta como cobrado", LL, "        return regla is not None, True", "        return regla is not None, False"),
    ("Q03", "cerrar carga lo sin respuesta pero no suelta su reserva (reserva colgada)", CO,
     "            self.p.cargar(self.bolsa, self._sin_respuesta)\n            self.p.liberar(self.bolsa, self._sin_respuesta)\n",
     "            self.p.cargar(self.bolsa, self._sin_respuesta)\n"),
    ("Q04", "H-11: pagar_resto no cierra la generación (la reparación no observa)", CO,
     "        self._abiertas.clear()\n        self._pagado = Uso()\n", "        self._abiertas.clear()\n"),
    ("Q05", "retry-after-ms leído como segundos", LL, "((\"retry-after-ms\", 1000.0), (\"retry-after\", 1.0))",
     "((\"retry-after-ms\", 1.0), (\"retry-after\", 1.0))"),
    ("Q06", "un reintento de más", LL, "reintento >= self.reintentos.maximo:", "reintento > self.reintentos.maximo:"),
    ("Q07", "H-12: el resultado del RUN sin análisis sin su presupuesto", OR,
     "        if pres_c5 is not None:\n            resultado[\"presupuesto\"] = pres_c5.resumen()\n", ""),
    ("Q08", "el motivo de la petición sin respuesta no dice el error", LL, "guarda.fallida(cobro, type(e).__name__)",
     "guarda.fallida(cobro, \"error\")"),
    ("Q09", "retry-after infinito o NaN aceptado", LL, "            if math.isfinite(v) and v > 0:", "            if v > 0:"),
    ("Q10", "x-should-retry sensible a mayúsculas", LL, "\"x-should-retry\", \"\")).lower()", "\"x-should-retry\", \"\"))"),
    ("Q11", "crear_cliente sin la regla (en producción no se reintenta)", LL, "reintentos=ReglaReintentos.de_config(cfg))",
     "reintentos=None)"),
    ("Q12", "el reintento que no cabe acaba como error del proveedor", LL,
     "            if fallo == \"presupuesto_agotado\":\n", "            if False:\n"),
    ("Q13", "la petición sin respuesta se carga pero no se anota (F5 no la declara)", CO,
     "        self.p.anotar(\"sin_respuesta\", {", "        (lambda *x: None)(\"sin_respuesta\", {"),
    ("Q14", "max_reintentos_api = True aceptado", LL, "if isinstance(maximo, bool) or not isinstance(maximo, int)",
     "if not isinstance(maximo, int)"),
    ("Q15", "un 400 (no reintentable) cuenta como cobrado", LL,
     "return reintenta, reintenta and error.status_code not in regla.sin_cobro",
     "return reintenta, error.status_code not in regla.sin_cobro"),
    ("Q16", "lo apartado de un timeout no se carga si la llamada se cae (KeyboardInterrupt)", CO,
     "        if self._sin_respuesta:\n            self.p.cargar(self.bolsa, self._sin_respuesta)\n",
     "        if self._sin_respuesta and False:\n            self.p.cargar(self.bolsa, self._sin_respuesta)\n"),
]

malos, vivos = [], []
for mid, que, ruta, viejo, nuevo in MUT:
    f = COPIA / ruta
    original = f.read_text(encoding="utf-8")
    if original.count(viejo) != 1:
        print(f"{mid} NO APLICA ({original.count(viejo)} apariciones): {que}", flush=True)
        malos.append(mid)
        continue
    f.write_text(original.replace(viejo, nuevo, 1), encoding="utf-8")
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS],
                           cwd=COPIA / "bloque_a" / "11_Ejecutor", capture_output=True, text=True, timeout=3600)
        muerto = r.returncode != 0
    finally:
        f.write_text(original, encoding="utf-8")
    print(f"{mid} {'muerto' if muerto else 'VIVO  '} · {que}", flush=True)
    if not muerto:
        vivos.append(mid)
print(f"{len(MUT) - len(malos) - len(vivos)}/{len(MUT)} muertos; vivos: {', '.join(vivos) or 'ninguno'}; "
      f"sin aplicar: {', '.join(malos) or 'ninguno'}")
sys.exit(1 if malos else 0)
