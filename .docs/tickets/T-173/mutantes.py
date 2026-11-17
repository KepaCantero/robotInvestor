"""Mutantes propios de T-173: aplica cada mutación, corre tests/test_t173.py y restaura.
Uso (desde bloque_a/11_Ejecutor): python ../../.docs/tickets/T-173/mutantes.py ."""
import subprocess, sys
from pathlib import Path
EJ = Path(sys.argv[1])
M = [
 ("M1 nunca degrada", "bloque_a/evaluador.py", '"degradar": bool(pv is not None and _finito(pv) and pv <= u)})', '"degradar": bool(pv is not None and _finito(pv) and pv < 0)})'),
 ("M2 cola contraria", "bloque_a/evaluador.py", "d = pd.Series((pr - oo) ** 2 - (pp - oo) ** 2)", "d = pd.Series((pp - oo) ** 2 - (pr - oo) ** 2)"),
 ("M3 la familia admite «Limitado»", "bloque_a/evaluador.py", 'if motivo is None and (matriz.get(c) or {}).get(h) != "SI":', 'if motivo is None and (matriz.get(c) or {}).get(h) == "NO":'),
 ("M4 sin muestra mínima", "bloque_a/evaluador.py", 'if muestra["n_eff"] < n_min or muestra["conglomerados"] < min_cong:', "if False:"),
 ("M5 sin un escalón por trimestre", "bloque_a/evaluador.py", "            if self._p31_ya_movida(f6, ambito, trimestre):\n                celda[\"motivo\"]", "            if False:\n                celda[\"motivo\"]"),
 ("M6 contaminados cuentan", "bloque_a/evaluador.py", "        for p in self.resueltos(as_of):\n            if p.get(\"horizonte\") != \"H5\":", "        for p in self.resueltos(as_of, admisibles=False):\n            if p.get(\"horizonte\") != \"H5\":"),
 ("M7 incluye H5 en DM", "bloque_a/evaluador.py", 'if p.get("horizonte") != "H5":\n                celdas[(p["clase"], p["horizonte"])].append(p)', 'if True:\n                celdas[(p["clase"], p["horizonte"])].append(p)'),
 ("M8 publica también los no abiertos", "bloque_a/evaluador.py", '            if p.get("estado") != "ABIERTO":\n                continue\n            pron[pid]', '            pron[pid]'),
 ("M9 sin F6 EH5", "bloque_a/evaluador.py", '        self.almacen.escribir("F6", "AG-20", ent)\n        return ent', '        return ent'),
 ("M10 paquete sin x_estados_h5", "bloque_a/sintesis.py", '        paquete["x_estados_h5"] = eh5', '        pass'),
 ("M11 hito estado invertido", "bloque_a/evaluador.py", 'return "CUMPLIDO" if int(h["resolucion"]["resultado_binario"]) else "FALLADO"', 'return "FALLADO" if int(h["resolucion"]["resultado_binario"]) else "CUMPLIDO"'),
 ("M12 técnico sin tabla H5", "bloque_a/redaccion.py", "        if e5:   # T-173", "        if False:   # T-173"),
 ("M13 sin estado del hito en el técnico", "bloque_a/redaccion.py", '+ (f" · estado: {x[\'estado\']}" if x.get("estado") else "")', '+ ""'),
 ("M14 C5 sin degradación DM", "bloque_a/evaluador.py", "degradacion_dm = self.aplicar_degradacion_dm(as_of, run_id)   # T-173", "degradacion_dm = []   # T-173"),
 # r02 (QA r01): H-01, H-02 y H-03
 ("M15 H-01 DM por PRG, no por conglomerado", "bloque_a/evaluador.py", ".groupby(pd.Series(fechas)).mean().sort_index()", ""),
 ("M16 H-01 sin exigir conglomerados mínimos", "bloque_a/evaluador.py", 'or muestra["conglomerados"] < min_cong:', ":"),
 ("M17 H-01 n en lugar de n_eff", "bloque_a/evaluador.py", 'if muestra["n_eff"] < n_min or', 'if muestra["n"] < n_min or'),
 ("M18 H-01 sin fechas sigue", "bloque_a/evaluador.py", '            if fechas is None:\n                motivo = "sin fechas de conglomerado (PA-03)"', '            if fechas is None:\n                fechas = [str(i) for i in range(len(lst))]'),
 ("M19 H-02 sin anular el AJU-", "bloque_a/evaluador.py", '"estado": "ANULADO",\n', '"estado": "CONFIRMADO",\n'),
 ("M20 H-02 sin revertir el CFG- de P-31", "bloque_a/evaluador.py", "            if escrito31:\n                try:", "            if False:\n                try:"),
 ("M21 H-02 los ANULADO cuentan", "bloque_a/evaluador.py", 'and a.get("estado") != "ANULADO"', ""),
 ("M22 H-03 sin Holm", "bloque_a/evaluador.py", "umbrales = ev.holm(familia, alfa) if familia else {}", "umbrales = {k: alfa for k in familia}"),
 ("M23 H-03 en cada C5", "bloque_a/evaluador.py", "        if rdm_id in self.almacen.estado(\"F6\", as_of, clave=\"id\"):\n            return []", ""),
 ("M24 H-03 la familia incluye las celdas que no pueden bajar", "bloque_a/evaluador.py", 'if motivo is None and (matriz.get(c) or {}).get(h) != "SI":', "if False:"),
 ("M25 H-05 la reversión hereda la versión nueva", "bloque_a/evaluador.py", '{**comun, "methodology_version": {"de": mv["de"], "a": mv["de"]},', '{**comun,'),
 ("M26 H-06 familia solo con las celdas evaluables", "bloque_a/evaluador.py", 'familia: dict[str, float | None] = {f"{c}|{h}": None for c, fila in sorted(matriz.items()) for h in HORIZONTES_DM\n                                            if (fila or {}).get(h) == "SI"}', 'familia: dict[str, float | None] = {}'),
]
vivos = []
for nombre, f, a, b in M:
    p = EJ / f; orig = p.read_text(encoding="utf-8")
    assert orig.count(a) == 1, (nombre, orig.count(a))
    p.write_text(orig.replace(a, b), encoding="utf-8")
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "tests/test_t173.py"], cwd=EJ, capture_output=True, text=True)
    finally:
        p.write_text(orig, encoding="utf-8")
    muerto = r.returncode != 0
    print(f"{nombre}: {'MUERTO' if muerto else 'VIVO'}", flush=True)
    if not muerto: vivos.append(nombre)
print("vivos:", vivos)
