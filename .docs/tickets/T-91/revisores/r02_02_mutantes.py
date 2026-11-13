"""QA r02 de T-91 · 02: mutantes de la ronda r02 (`hasta` en `Evaluador.rentabilidad`, frescura tras alinear, H-02 y H-04),
con el motor de `.docs/tickets/T-88/revisores/r01_mutar.py`.

  .venv/bin/python -I .docs/tickets/T-91/revisores/r02_02_mutantes.py RAIZ_DE_UNA_COPIA [--sin-suite] [--solo=Q1,Q2] [--suite=...]

Primero `test_t91_resolucion.py` y `test_t65_qa_r04.py`; si sobrevive, la segunda etapa; si sigue vivo, el detector propio
r02_01 (80 escenarios) y r01_01 H O (los cuatro casos de H-01 de la r01 y los PRG antiguos)."""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[1] / "T-88" / "revisores"))
from r01_mutar import ejecutar  # noqa: E402

E = "bloque_a/evaluador.py"
PX = ('                        rp, d1 = self.rentabilidad(p["variable"]["serie_ht01"], p["clase"], f0, f1, hz, base=p.get("nivel_referencia"),\n'
      '                                                   hasta=corte)\n')
RF = '                        rr, d1b = self.rentabilidad(p["referencia_indice"], p["clase"], f0, f1, hz, base=base_ref, hasta=corte)\n'
MUTANTES = [
    ("Q1", "frescura frente a la fecha común y no frente a la de resolución (vuelta a la r01)", E,
     "        motivo = self.motivo_no_fresca(d0, d1, f1, horizonte) if horizonte else (",
     "        motivo = self.motivo_no_fresca(d0, d1, f1 if hasta is None else hasta, horizonte) if horizonte else ("),
    ("Q2", "el proxy se vuelve a medir sin horizonte (solo exige un dato posterior a la base)", E, PX,
     PX.replace("f0, f1, hz, base=p.get", "f0, f1, None, base=p.get")),
    ("Q3", "la referencia se vuelve a medir sin horizonte", E, RF, RF.replace("f0, f1, hz, base=base_ref", "f0, f1, None, base=base_ref")),
    ("Q4", "el proxy no se vuelve a medir hasta la fecha común", E, PX,
     '                        rp, d1 = self.rentabilidad(p["variable"]["serie_ht01"], p["clase"], f0, f1, hz, base=p.get("nivel_referencia"))\n'),
    ("Q5", "la referencia no se vuelve a medir hasta la fecha común", E, RF, RF.replace(", hasta=corte)", ")")),
    ("Q6", "la CESTA ignora el `hasta` de fuera en la primera pasada", E,
     "            patas = [self.rentabilidad(s, clase, f0, f1, horizonte, base=b, hasta=hasta) for s, b in sorted(bases.items())]",
     "            patas = [self.rentabilidad(s, clase, f0, f1, horizonte, base=b) for s, b in sorted(bases.items())]"),
    ("Q7", "la CESTA se vuelve a medir sin horizonte", E,
     "                patas = [self.rentabilidad(s, clase, f0, f1, horizonte, base=b, hasta=corte) for s, b in sorted(bases.items())]",
     "                patas = [self.rentabilidad(s, clase, f0, f1, None, base=b, hasta=corte) for s, b in sorted(bases.items())]"),
    ("Q8", "solo se alinea si la referencia es la más antigua", E, "                    if d1b != d1:\n", "                    if d1b < d1:\n"),
    ("Q9", "H-04 vuelta atrás: la fecha de la base se lee siempre del dict", E,
     '            f_base = pd.Timestamp(nr["fecha"]) if isinstance(nr, dict) and nr.get("fecha") else f0',
     '            f_base = pd.Timestamp(nr["fecha"])'),
    ("Q10", "H-02 (b): fecha_dato solo del proxy", E, '"fecha_dato": max(d1, d1b) if d1b is not None else d1, ', '"fecha_dato": d1, '),
    ("Q11", "H-02 (c): la CESTA devuelve la fecha más reciente", E,
     "            return float(np.mean([v for v, _ in patas])), min(f for _, f in patas)",
     "            return float(np.mean([v for v, _ in patas])), max(f for _, f in patas)"),
    ("Q12", "la serie se mide siempre hasta f1 (se ignora `hasta`)", E,
     "        r, d0, d1 = self._rentabilidad_serie(simbolo, f0, f1 if hasta is None else hasta, base)",
     "        r, d0, d1 = self._rentabilidad_serie(simbolo, f0, f1, base)"),
]
DET = [("r02_01 n=80", [AQUI / "r02_01_frescura_y_alineacion.py", "--ejecutor", "{EJ}", "--n=80"]),
       ("r01_01 H O", [AQUI / "r01_01_resolucion_ataques.py", "--ejecutor", "{EJ}", "H", "O"])]
ejecutar(MUTANTES, ["tests/test_t91_resolucion.py", "tests/test_t65_qa_r04.py"], DET)
