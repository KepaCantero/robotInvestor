"""QA r01 de T-91 · 02: mutantes de la corrección (evaluador.py, calendario.py, sintesis.py, backtest.py y la H-29 (a) de
orquestacion.py), con el motor de `.docs/tickets/T-88/revisores/r01_mutar.py`.

  .venv/bin/python -I .docs/tickets/T-91/revisores/r01_02_mutantes.py RAIZ_DE_UNA_COPIA [--sin-suite] [--solo=N1,N2]
N1, N2 y N12 son (b), (c) y (a) de H-29 (QA r05 de T-65) adaptadas al código nuevo."""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[1] / "T-88" / "revisores"))
from r01_mutar import ejecutar  # noqa: E402

E, CAL, S, B, O = "bloque_a/evaluador.py", "bloque_a/calendario.py", "bloque_a/sintesis.py", "bloque_a/backtest.py", "bloque_a/orquestacion.py"
MUTANTES = [
    ("N1", "H-29 (b): fecha_dato solo del proxy", E, '"fecha_dato": max(d1, d1b) if d1b is not None else d1, ', '"fecha_dato": d1, '),
    ("N2", "H-29 (c): la CESTA devuelve la fecha más reciente", E,
     "            return float(np.mean([v for v, _ in patas])), min(f for _, f in patas)",
     "            return float(np.mean([v for v, _ in patas])), max(f for _, f in patas)"),
    ("N3", "CESTA alineada a la fecha más reciente", E, "            corte = min(f for _, f in patas)", "            corte = max(f for _, f in patas)"),
    ("N4", "sin alinear los miembros de la CESTA", E, "            if any(f != corte for _, f in patas):", "            if False:"),
    ("N5", "sin alinear proxy y referencia", E, "                    if d1b != d1:", "                    if False:"),
    ("N6", "proxy y referencia alineados a la más reciente", E, "                        corte = min(d1, d1b)", "                        corte = max(d1, d1b)"),
    ("N7", "H-26 vuelta atrás: H1 en días hábiles sin festivos", E,
     "return _sesiones_entre(desde, hasta, self._festivos_ps2) if horizonte == \"H1\"",
     "return dias_habiles_entre(pd.Timestamp(desde), pd.Timestamp(hasta)) if horizonte == \"H1\""),
    ("N8", "calendario sin el lunes de Pascua", CAL, '    if festivos["lunes_de_pascua"]:', "    if False:"),
    ("N9", "PRG antiguo de CESTA sin bases: no se congelan antes de alinear", E,
     '                    if base_ref is None and p["referencia_indice"] == "CESTA":', "                    if False:"),
    ("N10", "pronosticos.csv: fecha_dato_referencia con la del proxy", B,
     '"fecha_dato_referencia": r.get("fecha_dato_referencia")})', '"fecha_dato_referencia": r.get("fecha_dato_proxy")})'),
    ("N11", "criterio congelado sin la regla de alineación", S,
     '"de resolución, que la antigüedad de PS2 de su horizonte (H1 en sesiones sin los festivos de PS2); si las "\n'
     '                       "series acaban en fechas distintas, todas se miden hasta la más antigua; suceso: {suceso}")',
     '"de resolución, que la antigüedad de PS2 de su horizonte (H1 en sesiones sin los festivos de PS2); suceso: {suceso}")'),
    ("N12", "H-29 (a): PS2 con la referencia ausente usa la fecha del proxy", O, None, None),
    ("N13", "realineación del proxy con el nivel conocido en vez del congelado", E,
     '                        rp, d1 = self.rentabilidad(p["variable"]["serie_ht01"], p["clase"], f0, corte, base=p.get("nivel_referencia"))',
     '                        rp, d1 = self.rentabilidad(p["variable"]["serie_ht01"], p["clase"], f0, corte)'),
]
# N12: la misma sustitución que r05_05 (primera «fecha_dato = None» dentro de _puertas)
texto = (Path(sys.argv[1]).resolve() / "bloque_a" / "11_Ejecutor" / O).read_text(encoding="utf-8")
i = texto.index("    def _puertas")
j = texto.index("                fecha_dato = None", i)
k = texto.rfind("\n", 0, j - 1)
viejo = texto[k:j + len("                fecha_dato = None")]
MUTANTES[11] = ("N12", MUTANTES[11][1], O, viejo, viejo.replace("                fecha_dato = None", "                pass"))
if texto.count(viejo) != 1:
    MUTANTES[11] = ("N12", MUTANTES[11][1], O, viejo + texto[j + 33:j + 120], (viejo + texto[j + 33:j + 120]).replace("fecha_dato = None", "pass", 1))
DET = [("r01_01 A C", [AQUI / "r01_01_resolucion_ataques.py", "--ejecutor", "{EJ}", "A", "C"])]
ejecutar(MUTANTES, ["tests/test_t91_resolucion.py", "tests/test_t65_qa_r04.py"], DET)
