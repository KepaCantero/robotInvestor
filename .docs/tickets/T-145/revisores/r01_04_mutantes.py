"""QA r01 de T-145 · mutantes del revisor (los del implementador están en `mutantes_t145.py`): tramos de la cota del ciclo,
de R8 y de la comprobación de datos que no reintroducen un hallazgo concreto sino que rompen la cuenta en silencio.

Uso, desde la raíz:  python r01_04_mutantes.py <copia desechable de la raíz, con «_mut» en la ruta>
"""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir()
CT = "bloque_a/11_Ejecutor/bloque_a/contratos.py"
EST, CD = ".docs/scripts/estimar_coste_ciclo_a.py", ".docs/scripts/comprobar_datos_a.py"
PRUEBAS = ["tests/test_t145.py", "tests/test_t140.py", "tests/test_t136_r8.py", "tests/test_t136_coste.py",
           "tests/test_t131_preparativos.py", "tests/test_t130_r8.py", "tests/test_t123_r02.py",
           "tests/test_t123_r8_iban_y_tarjetas.py", "tests/test_t129_modo_sombra.py"]
MUTANTES = [
    ("R01", "la integración no lee el cribado", EST, "(\"integracion\", \"AG-02\", 1, \"COMUN\", (\"cribado\",))",
     "(\"integracion\", \"AG-02\", 1, \"COMUN\", ())"),
    ("R02", "el encargo de los tipos no acumula lo anterior", EST, "            leido += salida\n", "            leido = salida\n"),
    ("R03", "la ampliación es la menor de las dos", EST, "    amp = max(float(", "    amp = min(float("),
    ("R04", "sin el suelo de la bolsa común", EST, "max(tope - base, minimo_comun)", "(tope - base)"),
    ("R05", "solo el reparto con todos en N2", EST, "    for k in range(len(tipos) + 1):", "    for k in [len(tipos)]:"),
    ("R06", "sin la última llamada de cada bolsa", EST, "    ultimas = sum(", "    ultimas = 0 * sum("),
    ("R07", "sin la prima de caché", EST, "            r_[\"prima_uc\"] += 0.5 *", "            r_[\"prima_uc\"] += 0 *"),
    ("R08", "la comprobación S3 admite una llamada de más", EST, "if k > previstas.get(a, 0)", "if k > previstas.get(a, 0) + 1"),
    ("R09", "precio por UC sin la lectura de caché", EST, "               2 * uc[0] * p[\"lectura_cache\"] / uc[2]) / 1e6",
     "               0) / 1e6"),
    ("R10", "R8: la serie no prueba la tarjeta que empieza en el primer grupo", CT, "    for i in range(n - 4, -1, -1):",
     "    for i in range(n - 4, 0, -1):"),
    ("R11", "R8: el final de la serie (lista vacía) no cuenta como reparto", CT, "            if detras is not None:",
     "            if detras:"),
    ("R12", "ANTIGUO sin su último dato", CD, "        f.update(estado=\"ANTIGUO\", hasta=ultimo.date().isoformat(),",
     "        f.update(estado=\"ANTIGUO\","),
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
