"""QA r01 de T-154 · mutantes propios del revisor (distintos de P01–P18 de `mutantes_t154.py`).

Uso: python r01_03_mutantes_qa.py <copia desechable con «qa25_» y «_mut» en la ruta y `bloque_a/` entero> [--scripts]
Cada mutante se aplica en la copia, se pasan las pruebas de `PRUEBAS` (con -x) y se restaura. Vivo = ninguna prueba lo
detecta. Con `--scripts`, a cada vivo se le pasan además `r01_01_unidad_t154.py` y `r01_02_ciclo_f9.py` de esta ronda (dicen si
lo detectaría un ataque del revisor). Termina con 1 si alguno no aplica (texto no encontrado una vez); los vivos se informan."""
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
MUTANTES = [
    ("R01", "H-02: sin cierres no hay nada que declarar (`algo` olvida los cierres)", CO,
     "        return bool(self.cierres or self.recortes or self.excesos or self.sin_respuesta)",
     "        return bool(self.recortes or self.excesos or self.sin_respuesta)"),
    ("R02", "H-02: `algo` olvida los recortes", CO,
     "        return bool(self.cierres or self.recortes or self.excesos or self.sin_respuesta)",
     "        return bool(self.cierres or self.excesos or self.sin_respuesta)"),
    ("R03", "H-02: `algo` olvida los excesos", CO,
     "        return bool(self.cierres or self.recortes or self.excesos or self.sin_respuesta)",
     "        return bool(self.cierres or self.recortes or self.sin_respuesta)"),
    ("R04", "H-02: el tramo se salta la primera entrada nueva", CO, "list(getattr(self, k)[marca.get(k, 0):])",
     "list(getattr(self, k)[marca.get(k, 0) + 1:])"),
    ("R05", "H-01: el borde del cobro (> en vez de >=)", LL, "        if error.status_code >= regla.cobro_posible:",
     "        if error.status_code > regla.cobro_posible:"),
    ("R06", "H-03: se marca el grupo con cualquier reintento (también un 529, que no escribe)", OR,
     "        if presupuesto is not None and guarda is not None and guarda.sin_respuesta:\n",
     "        if presupuesto is not None and guarda is not None and guarda.peticiones > 1:\n"),
    ("R07", "H-03: se marca la bolsa en vez del grupo de prefijos", OR,
     "            presupuesto.grupo_sin_respuesta(grupo_primas(self.v6, agente))", "            presupuesto.grupo_sin_respuesta(bolsa)"),
    ("R08", "H-04: el tope de la espera es estricto (< en vez de <=)", LL, "return v if v <= self.espera_servidor_max_s else None",
     "return v if v < self.espera_servidor_max_s else None"),
    ("R09", "H-04: con la espera de más, se sale como presupuesto agotado", LL,
     "                if espera is None:   # T-154 (H-04): el servidor pide esperar más de lo admitido: no se reintenta\n"
     "                    return None, \"error_proveedor\"",
     "                if espera is None:   # T-154 (H-04): el servidor pide esperar más de lo admitido: no se reintenta\n"
     "                    return None, \"presupuesto_agotado\""),
    ("R10", "H-04: una espera de más se recorta al tope (se inventa una espera)", LL,
     "return v if v <= self.espera_servidor_max_s else None", "return min(v, self.espera_servidor_max_s)"),
    ("R11", "H-02: la F9 sin el resumen de después (el resumen vacío)", CO,
     "    def resumen(self) -> dict:\n        return self.origen.resumen()", "    def resumen(self) -> dict:\n        return {}"),
]


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
                with tempfile.TemporaryDirectory(prefix="qa25_r0103_") as t:
                    u = pasar([sys.executable, "-I", str(AQUI / "r01_01_unidad_t154.py"), str(ej)], COPIA)
                    c = pasar([sys.executable, "-I", str(AQUI / "r01_02_ciclo_f9.py"), str(ej), t], COPIA)
                extra = f" · r01_01 {'lo detecta' if u else 'no'} · r01_02 {'lo detecta' if c else 'no'}"
        finally:
            f.write_text(original, encoding="utf-8")
        print(f"{mid} {'muerto' if muerto else 'VIVO  '} · {que}{extra}", flush=True)
        if not muerto:
            vivos.append(mid)
    print(f"{len(MUTANTES) - len(vivos) - len(sin_aplicar)}/{len(MUTANTES)} muertos; vivos: {', '.join(vivos) or 'ninguno'}; "
          f"sin aplicar: {', '.join(sin_aplicar) or 'ninguno'}")
    return 1 if sin_aplicar else 0


if __name__ == "__main__":
    sys.exit(main())
