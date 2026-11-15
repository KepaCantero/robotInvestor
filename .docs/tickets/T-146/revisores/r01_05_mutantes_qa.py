"""QA r01 de T-146 · mutantes propios del revisor (distintos de los M01–M26 de `mutantes_t146.py`).

Uso: python r01_05_mutantes_qa.py <copia desechable con «qa19_mut» en la ruta y `bloque_a/` entero>
Cada mutante se aplica, se pasan `tests/test_t146_presupuesto.py`, `tests/test_t88_consumo.py` y `tests/test_fase4_huecos.py`
(con -x) y se restaura. Vivo = ninguna prueba lo detecta."""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "qa19_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir()
CO, AG, LL, OR = (f"bloque_a/11_Ejecutor/bloque_a/{f}.py" for f in ("consumo", "agentes", "llm", "orquestacion"))
PRUEBAS = ["tests/test_t146_presupuesto.py", "tests/test_t88_consumo.py", "tests/test_fase4_huecos.py"]
MUT = [
    ("Q01", "pagar_resto no suelta las reservas que no salieron", CO,
     "        for w, _ in self._abiertas:\n            self.p.liberar(self.bolsa, w)\n        self._abiertas.clear()\n        self._pagado = Uso()",
     "        self._abiertas.clear()\n        self._pagado = Uso()"),
    ("Q02", "el recorte no reserva lo que envía", CO, "            if self.p.reservar(self.bolsa, w):\n                self.p.anotar(\"recortes\"",
     "            if True:\n                self.p.anotar(\"recortes\""),
    ("Q03", "la ampliación no cuenta lo reservado", CO, "falta = estimado + self._ocupado(clase) - actual", "falta = estimado + self.consumido[clase] - actual"),
    ("Q04", "absorber pierde los cierres de C5", CO, "            self.cierres.extend(cierres)\n", ""),
    ("Q05", "sin escala por tope_total", CO, "self._escala = min(1.0, float(tope_total) / total) if tope_total is not None and total > 0 else 1.0",
     "self._escala = 1.0"),
    ("Q06", "sin factor observado", CO, "            self.p.observar_factor(self.bolsa, entrada / bruto)", "            pass"),
    ("Q07", "los excesos no se anotan", CO, "            self.p.anotar(\"excesos\",", "            (lambda *a: None)(\"excesos\","),
    ("Q08", "los controles no admiten ampliación", OR, "            bolsa, est, control or fase in (", "            bolsa, est, fase in ("),
    ("Q09", "el cliente real no paga cada petición", LL, "            if guarda is not None:\n                guarda.pagar(u)", "            pass"),
    ("Q10", "la salida mínima no se exige", CO, "        if mt >= self.salida_minima:", "        if mt >= 1:"),
    ("Q11", "liquidar no suelta lo retenido", CO, "            self.retenido.clear()   # T-146", "            pass   # T-146"),
    ("Q12", "_cargar no usa el prefijo de la primera petición", OR,
     "self._cargar(presupuesto, bolsa, agente, r, guarda.prefijo if guarda is not None else None)",
     "self._cargar(presupuesto, bolsa, agente, r, None)"),
]
vivos = []
for mid, desc, rel, viejo, nuevo in MUT:
    f = COPIA / rel
    orig = f.read_text(encoding="utf-8")
    assert orig.count(viejo) == 1, (mid, "texto no encontrado una sola vez")
    f.write_text(orig.replace(viejo, nuevo), encoding="utf-8")
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS],
                           cwd=COPIA / "bloque_a" / "11_Ejecutor", capture_output=True, text=True, timeout=3600)
        muerto = r.returncode != 0
    finally:
        f.write_text(orig, encoding="utf-8")
    print(f"{mid} {'muerto' if muerto else 'VIVO  '} · {desc}", flush=True)
    if not muerto:
        vivos.append(mid)
print(f"{len(MUT) - len(vivos)}/{len(MUT)} muertos; vivos: {', '.join(vivos) or 'ninguno'}")
