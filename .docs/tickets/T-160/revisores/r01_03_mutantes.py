"""QA r01 de T-160 · mutantes propios del revisor (M01–M26) sobre `evaluador.py` y `motor/servicio.py`.

Uso, desde la raíz:  .venv/bin/python .docs/tickets/T-160/revisores/r01_03_mutantes.py <copia «qa31_…_mut» con bloque_a/ entero> [--scripts] [--solo M01,M26]
Cada mutante se aplica en la copia, se pasan las pruebas de `PRUEBAS` (con -x) y se restaura. Vivo = ninguna prueba lo detecta.
Con `--scripts`, a cada vivo se le pasa además `r01_01_ataques.py` de esta ronda (sin sus `test_h0*`, que fallan a propósito).
Los equivalentes se marcan en EQUIVALENTES. Termina con 1 si alguno no aplica o si vive uno que no es equivalente.
"""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "qa31_" in str(COPIA) and "_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir()
SCRIPTS = "--scripts" in sys.argv[2:]
SOLO = set(sys.argv[sys.argv.index("--solo") + 1].split(",")) if "--solo" in sys.argv else None
AQUI = Path(__file__).resolve().parent
PY = str(Path(__file__).resolve().parents[4] / ".venv" / "bin" / "python")
EV, SV = "bloque_a/11_Ejecutor/bloque_a/evaluador.py", "bloque_a/11_Ejecutor/bloque_a/motor/servicio.py"
PRUEBAS = ["tests/test_t160_reejecucion_certificado.py", "tests/test_t66_evaluacion.py", "tests/test_t66_propuestas.py"]
MUTANTES = [
    ("M01", "CT-04 no mira la re-ejecución", EV,
     "            sin = self.motivo_sin_reejecucion(c)\n            if sin:\n                raise ValueError",
     "            sin = None\n            if sin:\n                raise ValueError"),
    ("M02", "no se retiran las propuestas sin re-ejecución", EV,
     "            sin = self.motivo_sin_reejecucion(c)\n            if sin:\n                self.almacen.escribir",
     "            sin = None\n            if sin:\n                self.almacen.escribir"),
    ("M03", "una CT-10 «NO» vale", EV, 'COINCIDE_CT10 = ("SI", "DENTRO_TOLERANCIA")', 'COINCIDE_CT10 = ("SI", "DENTRO_TOLERANCIA", "NO")'),
    ("M04", "sin la comparación 1 (cifras del certificado frente al Motor)", EV,
     "        if difs:\n            return fallo(", "        if False:\n            return fallo("),
    ("M05", "tolerancia un millón de veces más ancha", EV,
     'tol = float(servicio.IMPLEMENTADAS[FICHA_CERTIFICADO]["tol"])', 'tol = float(servicio.IMPLEMENTADAS[FICHA_CERTIFICADO]["tol"]) * 1e6'),
    ("M06", "sin materialidad", EV, '            if not crit["certificable"]:\n                return fallo("diferencia',
     '            if False:\n                return fallo("diferencia'),
    ("M07", "pasos siempre 0 (nunca se mira la materialidad)", EV,
     'pasos = (0 if exactas else 1) + (0 if rex["coincide"] == "SI" else 1)', "pasos = 0"),
    ("M08", "la holgura no se acumula", EV, "return (1 + tol / (1 - tol)) ** pasos - 1", "return tol if pasos else 0.0"),
    ("M09", "la materialidad no mueve el ECE", EV, '"calibracion": {"ece": sube(c["ece"])}', '"calibracion": {"ece": c["ece"]}'),
    ("M10", "la materialidad no mueve n_eff", EV, '"n_eff": baja(c["n_eff"])', '"n_eff": c["n_eff"]'),
    ("M11", "la materialidad no mueve la p de DM", EV, 'sube(c["dm_p_unilateral"])', 'c["dm_p_unilateral"]'),
    ("M12", "la materialidad no mueve el q90 del nulo", EV, 'baja(c["ece_nulo_q90"])', 'c["ece_nulo_q90"]'),
    ("M13", "la materialidad no mueve el IC del BSS", EV, '[baja(ic[0]), ic[1]]', '[ic[0], ic[1]]'),
    ("M14", "sin comprobar el solicitante AG-20 de la CT-10", EV, ' or r.get("solicitante") != "AG-20"', ""),
    ("M15", "sin comprobar que la CT-10 re-ejecuta el soporte", EV, '        if rx.get("calc_original") != soporte:\n',
     "        if False:\n"),
    ("M16", "sin comprobar la celda del soporte", EV,
     '\n                or (s.get("clase"), s.get("horizonte")) != (celda.get("clase"), celda.get("horizonte"))):', "):"),
    ("M17", "sin comprobar la ficha del soporte", EV, 'op_.get("ficha_id") != FICHA_CERTIFICADO', "False"),
    ("M18", "catalog_version vuelve al 4.0", EV, '"catalog_version": servicio.CATALOG_VERSION,', '"catalog_version": "4.0",'),
    ("M19", "FC-EVAL-001 ignora las fechas", SV, '    fechas = v.get("fechas")\n', "    fechas = None\n"),
    ("M20", "FC-EVAL-001 con fechas y sin mínimo usa 10", SV,
     'int(params["min_conglomerados"]) if fechas is not None else None', 'int(params.get("min_conglomerados", 10)) if fechas is not None else None'),
    ("M21", "sin incidencia en HA", EV, '                        self.almacen.incidencia("HERRAMIENTA",', '                        (lambda *a, **k: None)("HERRAMIENTA",'),
    ("M22", "la CT-10 la pide el Auditor y no el Evaluador", EV,
     '"antes de proponerlo o emitirlo (PB-32, EVAL-F05)", "AG-20")', '"antes de proponerlo o emitirlo (PB-32, EVAL-F05)", "AG-18")'),
    ("M23", "la propuesta retirada no deja volver a proponer la celda", EV, "                retirados.append(c[\"id\"])\n                del propuestos[k]\n",
     "                retirados.append(c[\"id\"])\n"),
    ("M24", "las cifras siempre «exactas»", EV, "exactas = propias == del_motor", "exactas = True"),
    ("M25", "sin mirar el «coincide» de la CT-10", EV, '        if rex.get("coincide") not in COINCIDE_CT10:\n            return fallo(f"la re-ejecución',
     '        if False:\n            return fallo(f"la re-ejecución'),
    ("M26", "un Motor que no sirve se da por bueno", EV, 'not str(res.get("estado", "")).startswith("SERVED") or not isinstance(calc, str)',
     "not isinstance(calc, str)"),
]
EQUIVALENTES = {
    "M13": "el umbral del IC es 0 y la tolerancia es relativa: bajar un extremo positivo x a x − h·|x| (h < 1) nunca lo deja ≤ 0",
    "M14": "una CT-10 coincidente de otro solicitante (el Auditor) del mismo soporte también es una re-ejecución independiente",
}


def pytest(args, cwd):
    r = subprocess.run([PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *args], cwd=cwd, capture_output=True, text=True,
                       timeout=3600)
    return r.returncode == 0, (r.stdout.strip().splitlines() or [""])[-1]


ejec = COPIA / "bloque_a" / "11_Ejecutor"
ok, ultima = pytest(PRUEBAS, ejec)
assert ok, f"las pruebas no pasan sin mutar: {ultima}"
vivos, no_aplica = [], []
for mid, desc, ruta, viejo, nuevo in MUTANTES:
    if SOLO and mid not in SOLO:
        continue
    f = COPIA / ruta
    texto = f.read_text(encoding="utf-8")
    if texto.count(viejo) != 1:
        no_aplica.append(mid)
        print(f"{mid} NO APLICA ({texto.count(viejo)} apariciones): {desc}")
        continue
    f.write_text(texto.replace(viejo, nuevo), encoding="utf-8")
    try:
        pasa, ultima = pytest(PRUEBAS, ejec)
        estado = "vivo" if pasa else "muerto"
        if pasa and SCRIPTS:
            pasa_s, ultima_s = pytest([str(AQUI / "r01_01_ataques.py"), "-k", "not test_h0"], ejec)
            estado = "vivo (también frente a r01_01)" if pasa_s else "muerto por r01_01"
            pasa = pasa_s
        if pasa:
            vivos.append(mid)
        print(f"{mid} {estado}{' [equivalente: ' + EQUIVALENTES[mid] + ']' if mid in EQUIVALENTES else ''}: {desc}")
    finally:
        f.write_text(texto, encoding="utf-8")
reales = [m for m in vivos if m not in EQUIVALENTES]
print(f"\n{len(MUTANTES)} mutantes · muertos {len(MUTANTES) - len(vivos) - len(no_aplica)} · vivos {vivos} · no aplican {no_aplica}")
sys.exit(1 if reales or no_aplica else 0)
