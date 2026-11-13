"""QA r03 de T-91 · 03: mutantes de la ronda r03 (alineación repetida y su salvaguarda) y nueva pasada de los que la r03 da
por equivalentes (Q2, Q3, Q7, Q10, Q11), con el motor de `.docs/tickets/T-88/revisores/r01_mutar.py`, sobre una COPIA
completa del repo (worktree con `bloque_a` entero).

  .venv/bin/python -I .docs/tickets/T-91/revisores/r03_03_mutantes.py RAIZ_DE_UNA_COPIA [--sin-suite] [--solo=W1,Q2] [--suite=...]

Primero `test_t91_resolucion.py` y `test_t65_qa_r04.py`; si sobrevive, la segunda etapa (--suite); si sigue vivo, los
detectores propios: r03_01 (oráculo cerrado, 200 escenarios) y r03_02 G (proveedor que ignora `hasta`)."""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[1] / "T-88" / "revisores"))
from r01_mutar import ejecutar  # noqa: E402

E = "bloque_a/evaluador.py"
PX = ('                        rp, d1 = self.rentabilidad(p["variable"]["serie_ht01"], p["clase"], f0, f1, hz, base=p.get("nivel_referencia"),\n'
      '                                                   hasta=corte)\n')
RF = '                        rr, d1b = self.rentabilidad(p["referencia_indice"], p["clase"], f0, f1, hz, base=base_ref, hasta=corte)\n'
GR = '                        if previo_corte is not None and corte >= previo_corte:   # no baja: no se alinean (falla cerrado)\n'
GC = '                if previo is not None and corte >= previo:   # la fecha común no baja: no se puede alinear (falla cerrado)\n'
MUTANTES = [
    ("W1", "resolver: una sola vuelta de alineación (vuelta a la r02)", E, "                    while d1b != d1:\n",
     "                    if d1b != d1:\n"),
    ("W2", "CESTA: una sola vuelta de alineación (vuelta a la r02)", E, "            while len({f for _, f in patas}) > 1:\n",
     "            if len({f for _, f in patas}) > 1:\n"),
    ("W3", "resolver: solo se realinea mientras la referencia sea la más antigua (Q8 con `while`)", E,
     "                    while d1b != d1:\n", "                    while d1b < d1:\n"),
    ("G1", "resolver: sin la salvaguarda «la fecha común no baja»", E, GR, "                        if False:\n"),
    ("G2", "CESTA: sin la salvaguarda «la fecha común no baja»", E, GC, "                if False:\n"),
    ("G3", "resolver: la salvaguarda con `>` en vez de `>=`", E, GR, GR.replace("corte >= previo_corte", "corte > previo_corte")),
    ("Q2", "el proxy se vuelve a medir sin horizonte", E, PX, PX.replace("f0, f1, hz, base=p.get", "f0, f1, None, base=p.get")),
    ("Q3", "la referencia se vuelve a medir sin horizonte", E, RF, RF.replace("f0, f1, hz, base=base_ref", "f0, f1, None, base=base_ref")),
    ("Q7", "la CESTA se vuelve a medir sin horizonte", E,
     "                patas = [self.rentabilidad(s, clase, f0, f1, horizonte, base=b, hasta=corte) for s, b in sorted(bases.items())]",
     "                patas = [self.rentabilidad(s, clase, f0, f1, None, base=b, hasta=corte) for s, b in sorted(bases.items())]"),
    ("Q10", "fecha_dato solo del proxy", E, '"fecha_dato": max(d1, d1b) if d1b is not None else d1, ', '"fecha_dato": d1, '),
    ("Q11", "la CESTA devuelve la fecha más reciente", E,
     "            return float(np.mean([v for v, _ in patas])), min(f for _, f in patas)",
     "            return float(np.mean([v for v, _ in patas])), max(f for _, f in patas)"),
]
DET = [("r03_01 n=200", [AQUI / "r03_01_oraculo_fecha_comun.py", "--ejecutor", "{EJ}", "--n=200"]),
       ("r03_02 G", [AQUI / "r03_02_bucle_y_calendarios.py", "--ejecutor", "{EJ}", "G"])]
ejecutar(MUTANTES, ["tests/test_t91_resolucion.py", "tests/test_t65_qa_r04.py"], DET)
