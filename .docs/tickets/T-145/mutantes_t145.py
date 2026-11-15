"""T-145 · mutantes de lo que cambia T-145 (R8 en series largas, cota del ciclo, comprobación de datos, borrador del
Anexo B), con los vivos de la QA r01 de T-140 (K04, V02, T06, T07) reescritos sobre el código nuevo.

Uso, desde la raíz:  python .docs/tickets/T-145/mutantes_t145.py <copia desechable de la raíz, con «_mut» en la ruta>
"""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir()
CT = "bloque_a/11_Ejecutor/bloque_a/contratos.py"
EST, CD, BO = ".docs/scripts/estimar_coste_ciclo_a.py", ".docs/scripts/comprobar_datos_a.py", ".docs/scripts/borrador_anexo_b.py"
PRUEBAS = ["tests/test_t145.py", "tests/test_t140.py", "tests/test_t136_r8.py", "tests/test_t136_coste.py",
           "tests/test_t131_preparativos.py", "tests/test_t130_r8.py", "tests/test_t123_r02.py",
           "tests/test_t123_r8_iban_y_tarjetas.py", "tests/test_t129_modo_sombra.py"]
MUTANTES = [
    ("T06", "caducidad: mes 00–12", CT, "and 1 <= int(g[:2]) <= 12", "and 0 <= int(g[:2]) <= 12"),
    ("T07", "caducidad: mes 01–19", CT, "and 1 <= int(g[:2]) <= 12", "and 1 <= int(g[:2]) <= 19"),
    ("T10", "el año vuelve a valer como fecha", CT, "and 1 <= int(g[:2]) <= 12",
     "and (1 <= int(g[:2]) <= 12 or g[:2] in (\"19\", \"20\"))"),
    ("T11", "lo que sobra no tiene que ser caducidad", CT, "if i + 4 < n and _forma_de_caducidad(grupos[i + 4])",
     "if i + 4 < n"),
    ("T12", "un grupo delante de la serie vale", CT, "    return resto[0]\n",
     "    return resto[0] if resto[0] is not None else resto[1]\n"),
    ("T13", "sin Luhn en las tarjetas de la serie", CT, "if not (_red_de_tarjeta(c) and _luhn(c)):", "if not _red_de_tarjeta(c):"),
    ("T14", "sin caducidad (solo tarjetas seguidas)", CT, "        siguientes = [i + 4] + ([i + 5] if", "        siguientes = [i + 4] + ([] if"),
    ("K04", "calcular no pasa las reparaciones al peor caso medido", EST,
     "                int((cfg.get(\"llm\") or {}).get(\"reintento_reparacion\", 0)))", "                0)"),
    ("K05", "sin la contrarréplica en la tabla", EST, "(\"contrarreplica\", (\"AG-11\",), 1, False)",
     "(\"contrarreplica\", (\"AG-11\",), 0, False)"),
    ("K06", "un solo dictamen G3", EST, "(\"dictamen_g3\", \"AG-18\", 2, None, \"*\")", "(\"dictamen_g3\", \"AG-18\", 1, None, \"*\")"),
    ("K07", "la reparación no reenvía lo generado", EST, "+ (r + v) * max_tokens", "+ v * max_tokens"),
    ("K08", "sin el mensaje de errores de la reparación", EST, " + r * tok_reparacion", ""),
    ("K09", "el encargo no lee lo que escriben los demás", EST,
     "\"encargo_tok\": max(encargo(x) for x in ags) + leido,", "\"encargo_tok\": max(encargo(x) for x in ags),"),
    ("K10", "la cota es la mayor de las dos", EST, "\"cota\": min(cota_llamadas, cota_presupuesto)",
     "\"cota\": max(cota_llamadas, cota_presupuesto)"),
    ("K11", "el presupuesto sin la ampliación", EST, "limites = max(limites, (1 + amp) *", "limites = max(limites, (1 + 0) *"),
    ("K12", "las peticiones de conocimiento sin búsqueda", EST, "casos = [(peor(a, leido, web and a in con_busqueda), a)",
     "casos = [(peor(a, leido, False), a)"),
    ("V02", "ventana solo de la tasa base (sin el margen de señales)", CD,
     "    ini = min(corte_ts - pd.DateOffset(years=int(sen[\"ventana_anios\"]), days=int(sen[\"margen_dias\"])),",
     "    ini = max(corte_ts - pd.DateOffset(years=int(sen[\"ventana_anios\"]), days=int(sen[\"margen_dias\"])),"),
    ("V04", "sin datos en la ventana siempre es FALTA", CD, "        if ultimo is None:\n", "        if True:\n"),
    ("B02", "el §1 vuelve a decir CT-06 a CT-14", BO, "(f\"Retornos internos ({_tramos(RETORNOS_INTERNOS)})\"",
     "(\"Retornos internos (CT-06 a CT-14)\""),
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
