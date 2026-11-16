"""QA r01 de T-156 · mutantes propios del revisor (S01–S14), sobre lo que cambia T-156 y lo que la prueba nueva de F9 por
lista debería ver.

Uso: python r01_02_mutantes_qa.py <copia desechable con «qa25_» y «_mut» en la ruta y `bloque_a/` entero> [--scripts]
Cada mutante se aplica en la copia, se pasan las pruebas de `PRUEBAS` (con -x) y se restaura. Vivo = ninguna prueba lo
detecta. Con `--scripts`, a cada vivo se le pasa además `r01_01_rango_cobro.py` de esta ronda. Los equivalentes (no cambian
ningún comportamiento observable) se marcan con «(equivalente)» y su supervivencia no es un hallazgo. Termina con 1 si
alguno no aplica o si vive uno que no es equivalente."""
import subprocess
import sys
import tempfile
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "qa25_" in str(COPIA) and "_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir()
SCRIPTS = "--scripts" in sys.argv[2:]
AQUI = Path(__file__).resolve().parent
CO, LL, OR = (f"bloque_a/11_Ejecutor/bloque_a/{f}.py" for f in ("consumo", "llm", "orquestacion"))
PRUEBAS = ["tests/test_t154.py", "tests/test_t151_reintentos.py", "tests/test_t88_consumo.py", "tests/test_t146_presupuesto.py"]
CHEQUEO = "not ESTADO_HTTP_MIN <= desde <= PRIMER_ESTADO_5XX:"
MUTANTES = [
    ("S01", "H-01: el tope es estricto (500 deja de valer)", LL, CHEQUEO, "not ESTADO_HTTP_MIN <= desde < PRIMER_ESTADO_5XX:"),
    ("S02", "H-01: el mínimo es estricto (100 deja de valer)", LL, CHEQUEO, "not ESTADO_HTTP_MIN < desde <= PRIMER_ESTADO_5XX:"),
    ("S03", "H-01: el tope es 599 (el fin de la clase 5xx: 501…599 fallan abierto)", LL,
     "ESTADO_HTTP_MIN, PRIMER_ESTADO_5XX = 100, 500", "ESTADO_HTTP_MIN, PRIMER_ESTADO_5XX = 100, 599"),
    ("S04", "H-01: el mínimo es 0", LL, "ESTADO_HTTP_MIN, PRIMER_ESTADO_5XX = 100, 500", "ESTADO_HTTP_MIN, PRIMER_ESTADO_5XX = 0, 500"),
    ("S05", "H-01: vuelve la validación de antes de T-156 (entero ≥ 0)", LL, CHEQUEO, "desde < 0:"),
    ("S06", "H-01: sin el rango por arriba", LL, CHEQUEO, "not ESTADO_HTTP_MIN <= desde:"),
    ("S07", "H-01: sin comprobar que es entero (500.0 vale; «500» da TypeError)", LL,
     "if isinstance(desde, bool) or not isinstance(desde, int) or not ESTADO_HTTP_MIN",
     "if isinstance(desde, bool) or not ESTADO_HTTP_MIN"),
    ("S08", "H-01: sin rechazar booleanos (equivalente: True y False quedan fuera del rango)", LL,
     "if isinstance(desde, bool) or not isinstance(desde, int) or not ESTADO_HTTP_MIN",
     "if not isinstance(desde, int) or not ESTADO_HTTP_MIN"),
    ("S09", "H-01: un valor alto se recorta a 500 en silencio en vez de rechazarse", LL,
     CHEQUEO, "not ESTADO_HTTP_MIN <= desde:\n            raise ValueError(\"llm.reintentos.cobro_posible_desde\")\n"
     "        desde = min(desde, PRIMER_ESTADO_5XX)\n        if False:"),
    ("S10", "H-01: la clasificación ignora la configuración (500 escrito en el código)", LL,
     "        if error.status_code >= regla.cobro_posible:", "        if error.status_code >= PRIMER_ESTADO_5XX:"),
    ("S11", "H-01: el error no nombra la clave", LL,
     'raise ValueError(f"llm.reintentos.cobro_posible_desde debe ser un estado HTTP entero entre',
     'raise ValueError(f"valor fuera de rango: debe ser un estado HTTP entero entre'),
    ("S12", "H-02: `algo` olvida las peticiones sin respuesta", CO,
     "        return bool(self.cierres or self.recortes or self.excesos or self.sin_respuesta)",
     "        return bool(self.cierres or self.recortes or self.excesos)"),
    ("S13", "H-02: los recortes solo salen en F5 si también hay excesos", OR,
     "               if presupuesto.recortes else {}),", "               if presupuesto.excesos else {}),"),
    ("S14", "H-02: la F9 declara todo el presupuesto y no el tramo de después de la marca", OR,
     '"fase": "F9", **self._f5_presupuesto(tramo)})', '"fase": "F9", **self._f5_presupuesto(presupuesto)})'),
    ("S15", "H-02: el tramo ignora la marca (todo lo de antes del RUN otra vez)", CO,
     "list(getattr(self, k)[marca.get(k, 0):])", "list(getattr(self, k))"),
]
EQUIVALENTES = {"S08"}


def pasar(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=3600).returncode


def main() -> int:
    sin_aplicar, vivos = [], []
    ej = COPIA / "bloque_a" / "11_Ejecutor"
    for mid, que, ruta, viejo, nuevo in MUTANTES:
        f = COPIA / ruta
        original = f.read_text(encoding="utf-8")
        if original.count(viejo) != 1:
            print(f"{mid} NO APLICA ({original.count(viejo)} apariciones): {que}", flush=True)
            sin_aplicar.append(mid)
            continue
        f.write_text(original.replace(viejo, nuevo), encoding="utf-8")
        extra = ""
        try:
            muerto = pasar([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS], ej) != 0
            if not muerto and SCRIPTS:
                with tempfile.TemporaryDirectory(prefix="qa25_r0102_", dir=COPIA.parent) as t:
                    u = pasar([sys.executable, "-I", str(AQUI / "r01_01_rango_cobro.py"), str(ej), t], COPIA)
                extra = f" · r01_01 {'lo detecta' if u else 'no'}"
        finally:
            f.write_text(original, encoding="utf-8")
        print(f"{mid} {'muerto' if muerto else 'VIVO  '} · {que}{extra}", flush=True)
        if not muerto:
            vivos.append(mid)
    malos = [m for m in vivos if m not in EQUIVALENTES]
    print(f"{len(MUTANTES) - len(vivos) - len(sin_aplicar)}/{len(MUTANTES)} muertos; vivos: {', '.join(vivos) or 'ninguno'} "
          f"(no equivalentes: {', '.join(malos) or 'ninguno'}); sin aplicar: {', '.join(sin_aplicar) or 'ninguno'}")
    return 1 if sin_aplicar or malos else 0


if __name__ == "__main__":
    sys.exit(main())
