"""QA r01 de T-180 · los mutantes del revisor de T-163 (N01–N12, `.docs/tickets/T-163/revisores/r01_02_mutantes.py`, sin
cambiar ese script) contra las pruebas de esta ronda, más dos mutantes nuevos sobre el código de T-180 (V01, V02).

- Pruebas: las de T-163 más `tests/test_t180_hallazgos_t163.py`.
- Ataques a los vivos: r01_01 de T-163 sin sus `test_h0*` y sin las tres que fallan por diseño desde T-180 (forjan con datos que
  no cumplen el criterio), y r01_01 de esta ronda.

Uso, desde la raíz:  .venv/bin/python .docs/tickets/T-180/revisores/r01_02_mutantes.py <copia «…_mut» con bloque_a/ y .docs/> [--solo N05,V01]
"""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve()
ORIGEN = AQUI.parents[2] / "T-163" / "revisores" / "r01_02_mutantes.py"
fuente = ORIGEN.read_text(encoding="utf-8")


def cambiar(viejo: str, nuevo: str) -> None:
    global fuente
    assert fuente.count(viejo) == 1, viejo
    fuente = fuente.replace(viejo, nuevo)


cambiar('PRUEBAS = ["tests/test_t163_hallazgos_t160.py",', 'PRUEBAS = ["tests/test_t180_hallazgos_t163.py", "tests/test_t163_hallazgos_t160.py",')
cambiar('ATAQUES = ["../../.docs/tickets/T-163/revisores/r01_01_ataques.py", "-k", "not test_h0"]',
        'ATAQUES = ["--import-mode=importlib", "../../.docs/tickets/T-163/revisores/r01_01_ataques.py", "../../.docs/tickets/T-180/revisores/r01_01_ataques.py", '
        '"-k", "not test_h0 and not falso_desde_cero and not un_lote_con_dos and not segundo_certificado"]')
cambiar("EQUIVALENTES = {", '''MUTANTES += [
    ("V01", "T-180: la materialidad de CT-04 usa dos pasos con una CT-10 DENTRO_TOLERANCIA (más estricta que al proponer)", EV,
     'pasos_ct10 = 0 if rx.get("coincide") == "SI" else 1', 'pasos_ct10 = 0 if rx.get("coincide") == "SI" else 2'),
    ("V02", "T-180: CT-04 exige una muestra efectiva de min_certificar + 1", EV,
     "holgura_tolerancia(tol_ct04, pasos_ct10), n_cert, ece_max, alfa_holm)",
     "holgura_tolerancia(tol_ct04, pasos_ct10), n_cert + 1, ece_max, alfa_holm)"),
]
EQUIVALENTES = {''')
sys.argv = [str(ORIGEN), *sys.argv[1:]]
exec(compile(fuente, str(ORIGEN), "exec"), {"__name__": "__main__", "__file__": str(ORIGEN)})   # noqa: S102
