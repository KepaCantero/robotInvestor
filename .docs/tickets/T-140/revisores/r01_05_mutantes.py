"""QA r01 de T-137 (revisor sin contexto): mutantes de lo que cambia T-137 (R8 en series largas, `_fecha_de_calendario`,
cota del coste, ventana de la comprobación de datos y borrador del Anexo B), contra las pruebas de T-137 y las vecinas.

Uso, desde la raíz:  python .docs/tickets/T-140/revisores/r01_05_mutantes.py <copia desechable de la raíz, con «_mut» en la ruta>
"""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir()
CT, EV = "bloque_a/11_Ejecutor/bloque_a/contratos.py", "bloque_a/11_Ejecutor/bloque_a/evaluador.py"
EST, CD, BO = ".docs/scripts/estimar_coste_ciclo_a.py", ".docs/scripts/comprobar_datos_a.py", ".docs/scripts/borrador_anexo_b.py"
PRUEBAS = ["tests/test_t137.py", "tests/test_t136_r8.py", "tests/test_t136_coste.py", "tests/test_t131_preparativos.py",
           "tests/test_t134_r03_t125.py", "tests/test_t125_r02.py", "tests/test_t125_r03.py", "tests/test_t130_r8.py",
           "tests/test_t123_r02.py", "tests/test_t123_r8_iban_y_tarjetas.py"]
MUTANTES = [
    ("T01", "solo desde el principio (sin el reparto desde el final)", CT,
     "for inicios in (list(range(0, n - 3, 4)), list(range(n - 4, -1, -4))):", "for inicios in (list(range(0, n - 3, 4)),):"),
    ("T02", "solo desde el final", CT,
     "for inicios in (list(range(0, n - 3, 4)), list(range(n - 4, -1, -4))):", "for inicios in (list(range(n - 4, -1, -4)),):"),
    ("T03", "lo que sobra no tiene que ser fecha", CT, "_forma_de_fecha(grupos[j]) for j in range(n) if j not in cubiertos)",
     "True for j in range(n) if j not in cubiertos)"),
    ("T04", "fecha: solo MMAA (sin años)", CT, "(1 <= int(g[:2]) <= 12 or g[:2] in (\"19\", \"20\"))", "(1 <= int(g[:2]) <= 12)"),
    ("T05", "fecha: solo años (sin MMAA)", CT, "(1 <= int(g[:2]) <= 12 or g[:2] in (\"19\", \"20\"))", "(g[:2] in (\"19\", \"20\"))"),
    ("T06", "fecha: mes 00–12", CT, "(1 <= int(g[:2]) <= 12 or", "(0 <= int(g[:2]) <= 12 or"),
    ("T07", "fecha: mes 01–19 (cualquier cosa que empiece por 0 o 1)", CT, "(1 <= int(g[:2]) <= 12 or", "(1 <= int(g[:2]) <= 19 or"),
    ("T08", "sin Luhn en las tarjetas de la serie", CT, "if all(_red_de_tarjeta(c) and _luhn(c) for c in tarjetas)",
     "if all(_red_de_tarjeta(c) for c in tarjetas)"),
    ("T09", "basta una tarjeta válida de las del reparto", CT, "if all(_red_de_tarjeta(c) and _luhn(c) for c in tarjetas)",
     "if any(_red_de_tarjeta(c) and _luhn(c) for c in tarjetas)"),
    ("F01", "sin comprobar la fecha de calendario", EV, "            t.date()   # T-137", "            pass   # T-137"),
    ("F02", "sin capturar NotImplementedError", EV, "except (NotImplementedError, OverflowError, ValueError) as e:",
     "except (OverflowError, ValueError) as e:"),
    ("K01", "la cota sin reparaciones", EST, "for r in range(1 + reparaciones):", "for r in range(1):"),
    ("K02", "la reparación no reenvía lo generado", EST,
     "entrada_cota + (r * vueltas + v) * x[\"max_tokens\"]", "entrada_cota + v * x[\"max_tokens\"]"),
    ("K03", "las continuaciones no reenvían lo generado", EST,
     "entrada_cota + (r * vueltas + v) * x[\"max_tokens\"]", "entrada_cota + r * vueltas * x[\"max_tokens\"]"),
    ("K04", "main no pasa las reparaciones", EST, "                int((cfg.get(\"llm\") or {}).get(\"reintento_reparacion\", 0)))",
     "                0)"),
    ("V01", "comprobación sin ventana (toda la historia)", CD, "s = prov.cierres(u[\"simbolo\"], ini, as_of)",
     "s = prov.cierres(u[\"simbolo\"], None, as_of)"),
    ("V02", "ventana solo de la tasa base (sin el margen de señales)", CD,
     "    ini = min(corte_ts - pd.DateOffset(years=int(sen[\"ventana_anios\"]), days=int(sen[\"margen_dias\"])),",
     "    ini = max(corte_ts - pd.DateOffset(years=int(sen[\"ventana_anios\"]), days=int(sen[\"margen_dias\"])),"),
    ("V03", "sin el aviso de lo anterior a la ventana", CD,
     "                    f[\"aviso\"] = f\"dato inválido anterior", "                    f[\"aviso\"] = \"\" or f\"\"  # dato inválido anterior"),
    ("B01", "CT-09 y CT-10 como retornos de ESQUEMAS otra vez", BO, "RETORNOS_DEL_MOTOR = {\"CT-09\", \"CT-10\"}",
     "RETORNOS_DEL_MOTOR: set = set()"),
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
