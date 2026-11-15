"""QA r01 de T-133 (revisor sin contexto): mutantes de lo que cambia T-133 en R8 (`contratos.py`) y en la cota del coste
(`estimar_coste_ciclo_a.py`), contra las pruebas de T-133 y las vecinas de R8.

Uso, desde la raíz:  python .docs/tickets/T-136/revisores/r01_03_mutantes.py <copia desechable de la raíz del repo, con «_mut» en la ruta>
(la copia necesita `bloque_a/11_Ejecutor` y `.docs/scripts/estimar_coste_ciclo_a.py`)
"""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir()
CT, EST = "bloque_a/11_Ejecutor/bloque_a/contratos.py", ".docs/scripts/estimar_coste_ciclo_a.py"
PRUEBAS = ["tests/test_t133_r8.py", "tests/test_t133_coste.py", "tests/test_t130_r8.py", "tests/test_t123_r02.py",
           "tests/test_t123_r8_iban_y_tarjetas.py", "tests/test_t122_hallazgos.py", "tests/test_t120_r8_y_lecciones.py"]
MUTANTES = [
    ("C01", "sin la comprobación de la caja", CT, "            if not _misma_caja(tal_cual[:largo]):\n                continue\n", ""),
    ("C02", "sin la regla de la cifra suelta", CT, "    return not any(len(g) == 1 and g.isdigit() for g in grupos[:-1])", "    return True"),
    ("C03", "sin la regla de las palabras de más de 4 letras", CT,
     "    if any(g.isalpha() and len(g) > LETRAS_GRUPO_MAX for g in grupos):\n        return False\n", ""),
    ("C04", "sin la estructura del país (solo la longitud)", CT, "    if patron is None or not patron.fullmatch(compacto[4:]):",
     "    if patron is None:"),
    ("C05", "Rumanía con cifras donde van letras o cifras («4a16n»)", CT, '"RO": "4a16c"', '"RO": "4a16n"'),
    ("C06", "Letonia «4a13n»", CT, '"LV": "4a13c"', '"LV": "4a13n"'),
    ("C07", "Chipre «3n5n16n»", CT, '"CY": "3n5n16c"', '"CY": "3n5n16n"'),
    ("C08", "Italia sin el CIN de letra («1c5n5n12c»)", CT, '"IT": "1a5n5n12c"', '"IT": "1c5n5n12c"'),
    ("C09", "Francia: el número de cuenta solo de cifras («5n5n11n2n»)", CT, '"FR": "5n5n11c2n"', '"FR": "5n5n11n2n"'),
    ("C10", "sin la regla de la fila de tabla", CT, "GRUPOS_FILA_DE_TABLA = 5 ", "GRUPOS_FILA_DE_TABLA = 99 "),
    ("C11", "fila de tabla desde 4 grupos (mataría las tarjetas 4-4-4-4)", CT, "GRUPOS_FILA_DE_TABLA = 5 ", "GRUPOS_FILA_DE_TABLA = 4 "),
    ("C12", "fila de tabla desde 6 grupos", CT, "GRUPOS_FILA_DE_TABLA = 5 ", "GRUPOS_FILA_DE_TABLA = 6 "),
    ("K01", "la cota sin el margen de tokens", EST, "entrada_cota = (x[\"sys_tok\"] + x[\"user_tok\"]) * factor_tokens",
     "entrada_cota = (x[\"sys_tok\"] + x[\"user_tok\"])"),
    ("K02", "la cota con las lecturas de caché del simulador", EST,
     "cota = vueltas * _coste(p, 0, 0, entrada_cota, 0)", "cota = vueltas * _coste(p, 0, 0, entrada_cota - lect, lect)"),
    ("K03", "la cota sin continuaciones", EST, "vueltas = 1 + (continuaciones if x[\"agente\"] in agentes_busqueda else 0)", "vueltas = 1"),
    ("K04", "la cota con la salida por vuelta (lo que pide la QA r01 de T-133)", EST,
     "+ _coste(p, 0, x[\"max_tokens\"], 0, 0)", "+ vueltas * _coste(p, 0, x[\"max_tokens\"], 0, 0)"),
]
for mid, que, rel, viejo, nuevo in MUTANTES:
    ruta = COPIA / rel
    original = ruta.read_text(encoding="utf-8")
    assert original.count(viejo) == 1, f"{mid}: el texto no aparece exactamente una vez"
    ruta.write_text(original.replace(viejo, nuevo), encoding="utf-8")
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS],
                           cwd=COPIA / "bloque_a" / "11_Ejecutor", capture_output=True, text=True)
    finally:
        ruta.write_text(original, encoding="utf-8")
    assert r.returncode in (0, 1), r.stdout[-1500:] + r.stderr[-1500:]
    print(f"{mid} | {que} | {'MUERTO · ' + r.stdout.strip().splitlines()[-1] if r.returncode else 'VIVO'}", flush=True)
