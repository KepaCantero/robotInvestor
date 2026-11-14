"""QA r01 de T-119 · mutantes propios de `bloque_a/motor/fichas_p2.py` (ninguno repite los 124 de `impl_p2_mutantes.py`).

Cada mutante se aplica en una COPIA desechable del ejecutor (con el Catálogo al lado) y se mira quién lo caza: los casos de
control de la ficha (CC) y las pruebas del paquete de T-119 (`tests/test_t119_p2.py` y `tests/test_t119_motor.py`, `-x`).
Uso: r01_09_mutantes.py DESTINO [--solo ID[,ID]]      (DESTINO: carpeta desechable; se borra al acabar si no hay --solo)
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
DESTINO = Path(sys.argv[1]).resolve()
SOLO = sys.argv[sys.argv.index("--solo") + 1].split(",") if "--solo" in sys.argv else None
PY = sys.executable
MODULO = "bloque_a/motor/fichas_p2.py"
PRUEBAS = ["tests/test_t119_p2.py", "tests/test_t119_motor.py"]

M = [
    # ---- fórmulas
    ("Q01", "FIR-CRED-001", "desc = D * math.exp(-r * T)\n    vmax, raiz", "desc = D * math.exp(-r)\n    vmax, raiz", "descuento de la deuda sin T en el sistema de Merton"),
    ("Q02", "FIR-CRED-001", "deudas.append(corto + largo)", "deudas.append(D)", "pesos por el punto de impago y no por la deuda total"),
    ("Q03", "FIR-CRED-001", "recuperado = V * math.exp(r * T) / D * float(special.ndtr(-d1))", "recuperado = V / D * float(special.ndtr(-d1))", "recuperación sin capitalizar"),
    ("Q04", "FIR-CRED-001", '"cobertura_segmento_pct": cobertura * PCT', '"cobertura_segmento_pct": cobertura', "cobertura sin pasar a %"),
    ("Q05", "FIR-CRED-001", "d1 = (math.log(V / D) + (r + 0.5 * sV * sV) * T) / raiz\n    d2 = d1 - raiz", "d1 = (math.log(V / D) + (r + 0.5 * sV * sV)) / raiz\n    d2 = d1 - raiz", "d₁ de las medidas sin T en la deriva"),
    ("Q06", "FX-BEER-001", "filas = np.arange(k + 1, T_ - k)", "filas = np.arange(k, T_ - k)", "muestra del DOLS con una fila de más (Δx envuelto)"),
    ("Q07", "FX-BEER-001", 'nivel_ic = _rango(parametro(ent.get("configuracion"), "evaluacion.nivel_ic")', 'nivel_ic = _rango(parametro(None, "evaluacion.nivel_ic")', "nivel del IC de la configuración por defecto, no la del Motor"),
    ("Q08", "FX-BEER-001", "prueba = fs.adf(z, False, fs.rezagos_regla(n))", "prueba = fs.adf(z, True, fs.rezagos_regla(n))", "ADF de los residuos con constante"),
    ("Q09", "FX-BEER-001", '"equilibrio": math.exp(const + float(X[-1] @ beta))', '"equilibrio": math.exp(float(X[-1] @ beta))', "equilibrio sin la constante"),
    ("Q10", "FX-BEER-001", "critico = fs._critico(fs._CRIT_TRAZA, m + 1, nivel)", "critico = fs._critico(fs._CRIT_TRAZA, m, nivel)", "crítico de la traza con una variable menos"),
    ("Q11", "FX-BEER-001", "ee_z = math.sqrt(max(float(d @ est[\"cov\"] @ d), 0.0))", "ee_z = math.sqrt(max(float(d @ d), 0.0))", "IC sin la covarianza de β"),
    ("Q12", "CMD-REAL-001", 'mk = op.mann_kendall(np.log(real), u["nivel_tendencia"], True)', 'mk = op.mann_kendall(np.log(real), u["nivel_tendencia"], False)', "Mann-Kendall sin la corrección de autocorrelación"),
    ("Q13", "CMD-REAL-001", '[anual(mk["ic_pendiente"][0]), anual(mk["ic_pendiente"][1])]', '[anual(mk["ic_pendiente"][0]), anual(mk["ic_pendiente"][0])]', "IC de la tendencia con el mismo extremo dos veces"),
    ("Q14", "CMD-REAL-001", '"ri_mh": pos["media"], "ri_pa": actual', '"ri_mh": pos["media"], "ri_pa": float(precio[-1] / ipc[-1])', "RI-PA con otra base"),
    ("Q15", "REI-LEV-001", '"deuda_neta_sobre_ebitda_veces": tot["neta"] / tot["ebitda"],', '"deuda_neta_sobre_ebitda_veces": tot["deuda"] / tot["ebitda"],', "deuda bruta/EBITDA"),
    ("Q16", "REI-LEV-001", '"vencimientos_24m_pct": _distribucion(a["venc"] / a["deuda"] * PCT)', '"vencimientos_24m_pct": _distribucion(a["venc"] / a["neta"] * PCT)', "dispersión de vencimientos sobre la deuda neta"),
    ("Q17", "REI-LEV-001", '(np.array(holg_ltv) < 0) | (np.array(holg_icr) < 0)', '(np.array(holg_ltv) < 0) & (np.array(holg_icr) < 0)', "incumplimiento solo si fallan los dos covenants"),
    ("Q18", "REI-LEV-001", '"vencimientos_24m_pct": tot["venc"] / tot["deuda"] * PCT,', '"vencimientos_24m_pct": tot["venc"] / tot["neta"] * PCT,', "vencimientos sobre la deuda neta"),
    ("Q19", "REI-LEV-001", '"icr_veces": _distribucion(a["ebitda"] / a["gf"])', '"icr_veces": _distribucion(a["gf"] / a["ebitda"])', "dispersión del ICR invertida"),
    ("Q20", "CHR-ONCHAIN-001", '"senal_nvt": _posicion(float(senal[-1]), senal)["percentil"]', '"senal_nvt": _posicion(float(senal[-1]), nvt)["percentil"]', "percentil de la señal frente a la historia del NVT"),
    ("Q21", "CHR-ONCHAIN-001", '"mvrv_z": _posicion(float(z[-1]), z)["percentil"]', '"mvrv_z": _posicion(float(z[-1]), mvrv)["percentil"]', "percentil del MVRV-Z frente a la historia del MVRV"),
    ("Q22", "CHR-TOKEN-001", "return float(sum(c * x for c, x in pares)) / peso * PCT, peso / float(np.sum(a_cm)) * PCT", "return float(sum(c * x for c, x in pares)) / peso * PCT, len(pares) / len(tokens) * PCT", "cobertura por número de tokens"),
    ("Q23", "CHR-TOKEN-001", "abierto_hi=True) - neta[-1]))", "abierto_hi=True) - neta[0]))", "rendimiento real con la inflación del primer token"),
    ("Q24", "CHR-TOKEN-001", '"inflacion_neta_pct_anual": _distribucion(a_neta * PCT)', '"inflacion_neta_pct_anual": _distribucion(a_neta)', "dispersión de la inflación sin pasar a %"),
    ("Q25", "PRV-PME-001", "tir_ind = _tir(*_con_nav(fl, lam * D - C, f_nav, nav), u, lim, \"PME+\")", "tir_ind = _tir(*_con_nav(fl, D - lam * C, f_nav, nav), u, lim, \"PME+\")", "PME+ con λ sobre las aportaciones"),
    ("Q26", "PRV-PME-001", '"dpi_veces": float(np.sum(D)) / float(np.sum(C)),\n        "pme_plus"', '"dpi_veces": (float(np.sum(D)) + nav) / float(np.sum(C)),\n        "pme_plus"', "DPI con el NAV"),
    ("Q27", "PRV-PME-001", '"exceso_ks_pme": ks - 1', '"exceso_ks_pme": ks', "exceso de KS-PME sin restar 1"),
    ("Q28", "PRV-PME-001", "(None if tir is None or tir_ind is None else (tir - tir_ind) * PCT)", "(None if tir is None or tir_ind is None else (tir_ind - tir) * PCT)", "signo del diferencial de TIR"),
    ("Q29", "PRV-CF-001", "c = tasas[min(t, len(tasas)) - 1] * max(compromiso - aportado, 0.0)", "c = tasas[min(t - edad, len(tasas)) - 1] * max(compromiso - aportado, 0.0)", "tasa por año de proyección y no por año de vida"),
    ("Q30", "PRV-CF-001", '"minimo_sobre_compromiso": float(acumulado[i_min]) / compromiso', '"minimo_sobre_compromiso": float(acumulado[i_min]) / aportado', "mínimo de la curva J sobre lo aportado"),
    ("Q31", "PRV-CF-001", 'ref["diferencia_tir_pct"] = None if tir is None else tir * PCT - ref["tir_mediana_pct"]', 'ref["diferencia_tir_pct"] = None if tir is None else tir - ref["tir_mediana_pct"]', "diferencia de TIR con unidades mezcladas"),
    ("Q32", "PRV-CF-001", '"tvpi_final_veces": (di_f + nav_f) / ap_f', '"tvpi_final_veces": di_f / ap_f', "TVPI final sin el NAV"),
    ("Q33", "PRV-CF-001", "edad = int((f_nav - fl.index[0]).days // DIAS_ANIO)", "edad = int((fl.index[-1] - fl.index[0]).days // DIAS_ANIO)", "edad hasta el último flujo y no hasta el NAV"),
    ("Q34", "ALT-HF-001", "r, rf, Fm = (r[1:] - phi * r[:-1]) / (1 - phi), rf[1:], Fm[1:]", "r, rf, Fm = (r[1:] - phi * r[:-1]) / (1 - phi), rf[:-1], Fm[1:]", "rf desalineado un mes tras desuavizar"),
    ("Q35", "ALT-HF-001", '        if phi < 0:\n            lim.append(f"φ estimado negativo ({phi:.4f}): sin evidencia de suavizado")\n', "", "sin la limitación de φ negativo"),
    ("Q36", "ALT-HF-001", "pasiva = float(sum(base[\"betas\"][nb][\"beta\"] * float(np.mean(Fm[:, j])) for j, nb in enumerate(nombres)))", "pasiva = float(sum(base[\"betas\"][nb][\"beta\"] * float(np.median(Fm[:, j])) for j, nb in enumerate(nombres)))", "cartera pasiva con la mediana de los factores"),
    ("Q37", "ALT-AUC-001", 'out.update({"indice": _indice(b[1 + car.shape[1]:])', 'out.update({"indice": _indice(b[car.shape[1]:][:P - 1])', "hedónico: efectos temporales desplazados un coeficiente"),
    ("Q38", "ALT-AUC-001", '"iqr_residual_pct": (q75 - q25) * PCT', '"iqr_residual_pct": (q75 - q25)', "IQR sin pasar a %"),
    ("Q39", "ALT-AUC-001", 'ref["exceso_sobre_rv_global_pct"] = bruta - rv * PCT', 'ref["exceso_sobre_rv_global_pct"] = bruta - rv', "exceso con unidades mezcladas"),
    ("Q40", "ALT-AUC-001", '"diferencia_maxima_indice": float(np.max(np.abs(otra["indice"] - ind)))', '"diferencia_maxima_indice": float(np.min(np.abs(otra["indice"] - ind)))', "diferencia mínima en vez de máxima"),
    ("Q41", "ALT-AUC-001", '"diferencia_pct": bruta - anual(otra["indice"]),', '"diferencia_pct": anual(otra["indice"]) - bruta,', "signo de la diferencia con la segunda vía"),
    # ---- fecha de corte, campo a campo
    ("Q50", None, '    _hasta_corte(t.index, corte, f"{F}: serie")\n    _consecutivas(t.index, "Q", f"{F}: serie")', '    _consecutivas(t.index, "Q", f"{F}: serie")', "FX-BEER: serie sin fecha de corte"),
    ("Q51", None, '    _hasta_corte(t.index, corte, f"{F}: serie")\n    _consecutivas(t.index, "M", f"{F}: serie")\n    n = len(t)\n    if n < u["anios_rechazo"]', '    _consecutivas(t.index, "M", f"{F}: serie")\n    n = len(t)\n    if n < u["anios_rechazo"]', "CMD-REAL: serie sin fecha de corte"),
    ("Q52", None, '    _hasta_corte(t.index, _corte(ent), f"{F}: serie")\n    _consecutivas(t.index, "D", f"{F}: serie")', '    _consecutivas(t.index, "D", f"{F}: serie")', "CHR-ONCHAIN: serie sin fecha de corte"),
    ("Q53", None, '    _hasta_corte(fl.index, corte, f"{F}: flujos")\n', "", "PRV: flujos sin fecha de corte"),
    ("Q54", None, '    _hasta_corte(niveles.index, corte, f"{F}: indice.niveles")\n', "", "PRV-PME: niveles del índice sin fecha de corte"),
    ("Q55", None, '    _hasta_corte(navs.index, corte, f"{F}: navs")\n', "", "PRV-CF: NAV sin fecha de corte"),
    ("Q56", None, '    _hasta_corte(t.index, _corte(ent), f"{F}: serie")\n    _consecutivas(t.index, "M", f"{F}: serie")', '    _consecutivas(t.index, "M", f"{F}: serie")', "ALT-HF: serie sin fecha de corte"),
    ("Q57", None, '    _hasta_corte(fechas, _corte(ent), f"{F}: transacciones")\n', "", "ALT-AUC: transacciones sin fecha de corte"),
    ("Q58", None, '    f_cc = _fecha_dato(cc, "fecha", corte, f"{F}: curva_costes")', '    f_cc = _fecha_dato(cc, "fecha", None, f"{F}: curva_costes")', "CMD-REAL: curva de costes sin fecha de corte"),
    ("Q59", None, '    vintage = _fecha_dato(v, "vintage", corte, F)', '    vintage = _fecha_dato(v, "vintage", None, F)', "FX-BEER: vintage sin fecha de corte"),
    ("Q60", None, '    f_nav = _fecha_dato(nd, "fecha", corte, f"{F}: nav_final")', '    f_nav = _fecha_dato(nd, "fecha", None, f"{F}: nav_final")', "PRV-PME: NAV final sin fecha de corte"),
    ("Q61", None, '    fecha = _fecha_dato(v, "fecha", _corte(ent), F)\n    moneda', '    fecha = _fecha_dato(v, "fecha", None, F)\n    moneda', "REI-LEV: fecha sin fecha de corte"),
    ("Q62", None, '    fecha = _fecha_dato(v, "fecha", _corte(ent), F)\n    fuente', '    fecha = _fecha_dato(v, "fecha", None, F)\n    fuente', "CHR-TOKEN: fecha sin fecha de corte"),
    ("Q63", None, '    fecha = _fecha_dato(v, "fecha", _corte(ent), F)\n    seg', '    fecha = _fecha_dato(v, "fecha", None, F)\n    seg', "FIR-CRED: fecha sin fecha de corte"),
    # ---- validaciones y cotas
    ("Q70", None, "    return isinstance(x, (np.integer, np.floating)) and abs(float(x)) > MAGNITUD_MAX", "    return False", "magnitud: los tipos de numpy no se miran"),
    ("Q71", None, "    if len(per) >= 2 and not bool(np.all(np.diff(per.asi8) == 1)):", "    if len(per) >= 2 and not bool(np.all(np.diff(per.asi8) >= 1)):", "series con huecos admitidas"),
    ("Q72", None, "    if len(set(ids)) != len(ids):", "    if False:", "identificadores de componente repetidos admitidos"),
    ("Q73", None, "        if n - k - 1 <= (m + 1) * (k + 1) + 1:", "        if False:", "Johansen sin comprobar la identificación"),
    ("Q74", None, '    if f_nav < fl.index[-1]:\n        raise ErrorFicha(f"{F}: el NAV final', '    if False:\n        raise ErrorFicha(f"{F}: el NAV final', "PRV-PME: NAV anterior al último flujo admitido"),
    ("Q75", None, '        if perfil.index[0] < fecha:', '        if False:', "REI-LEV: vencimientos anteriores a la fecha admitidos"),
    ("Q76", None, '"vencimientos_maximos": 100,', '"vencimientos_maximos": 101,', "cota de vencimientos por componente"),
    ("Q77", None, '"desbloqueos_maximos": 1000,', '"desbloqueos_maximos": 1001,', "cota de desbloqueos por token"),
    ("Q78", None, '"flujos_maximos": 10_000,\n                    "rango_tir"', '"flujos_maximos": 10_001,\n                    "rango_tir"', "PRV-PME: cota de flujos"),
    ("Q79", None, '"caracteristicas_maximas": 20,', '"caracteristicas_maximas": 21,', "cota de características"),
    ("Q80", None, 'u["anios_historia_maximos"] * MESES_ANIO, opcionales=("rf",))', 'u["anios_historia_maximos"] * MESES_ANIO + 1, opcionales=("rf",))', "ALT-HF: cota de la serie"),
    ("Q81", None, '"tramos_maximos": 1000,', '"tramos_maximos": 1001,', "cota de tramos de la curva de costes"),
    ("Q82", None, '"dias_maximos": ANIOS_H5_MAX * DIAS_ANIO}', '"dias_maximos": ANIOS_H5_MAX * DIAS_ANIO + 1}', "CHR-ONCHAIN: cota de días"),
    ("Q83", None, '        if cambios > 1:', '        if cambios > 2:', "aviso de múltiples soluciones solo con más de dos cambios de signo"),
    ("Q84", None, '    if ind.get("rentabilidad_total") is not True:', '    if not ind.get("rentabilidad_total"):', "rentabilidad_total: cualquier valor verdadero"),
    ("Q85", None, "        if circ > total or (maxima is not None and total > maxima):", "        if maxima is not None and total > maxima:", "circulante > total admitido"),
    ("Q86", None, '        if not -1 < phi < 1:', '        if not -1 <= phi <= 1:', "φ = ±1 admitido"),
    ("Q87", None, '    if P < u["periodos_minimos"]:', '    if P < u["periodos_minimos"] - 1:', "ALT-AUC: índice con dos periodos"),
    ("Q88", None, '"rango_comisiones": (0.10, 0.25)', '"rango_comisiones": (0.10, 0.26)', "rango de comisiones"),
    ("Q89", None, '    if _texto(ind.get("moneda"), f"{F}: indice.moneda") != moneda:', '    if False:', "PRV-PME: índice en otra moneda admitido"),
    ("Q90", None, '    if vintage < t.index[-1]:', '    if False:', "FX-BEER: vintage anterior a la última observación (repite M28 a propósito, de control)"),
]

GUION_CC = r"""
import copy, sys
sys.path.insert(0, ".")
from bloque_a.motor import fichas_p2 as m
from bloque_a.motor import servicio
ok = True
for c in m.CASOS_CONTROL[sys.argv[1]]:
    try:
        v = {}
        for d in c["datos"]:
            v.update(copy.deepcopy(d["valores"]))
        r1, _ = m.FICHAS[sys.argv[1]]["fn"]({"valores": copy.deepcopy(v), "series": {}, "series_rol": {}}, dict(c["parametros"]))
        ok = ok and bool(c["comprobar"](r1))
    except Exception:
        ok = False
sys.exit(0 if ok else 1)
"""


def main() -> int:
    copia = DESTINO / "copia_ejecutor"
    if copia.exists():
        shutil.rmtree(copia)
    shutil.copytree(RAIZ / "bloque_a" / "11_Ejecutor", copia, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    cat = RAIZ / "bloque_a" / "04_Motor_conocimiento_y_catalogo"
    (DESTINO / cat.name).mkdir(exist_ok=True)
    for md in cat.glob("*.md"):
        shutil.copy(md, DESTINO / cat.name / md.name)
    fuente = copia / MODULO
    original = fuente.read_text(encoding="utf-8")
    entorno = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "BLOQUE_A_RAIZ": str(DESTINO)}
    vivos, total = [], 0
    try:
        for ident, ficha, a, b, desc in M:
            if SOLO and ident not in SOLO:
                continue
            if original.count(a) != 1:
                print(f"{ident}: el texto original aparece {original.count(a)} veces (se esperaba 1): {a[:70]!r}", flush=True)
                continue
            total += 1
            fuente.write_text(original.replace(a, b), encoding="utf-8")
            cc = None
            if ficha:
                cc = subprocess.run([PY, "-B", "-W", "ignore", "-c", GUION_CC, ficha], cwd=copia, env=entorno, capture_output=True).returncode != 0
            pr = subprocess.run([PY, "-B", "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider", *PRUEBAS], cwd=copia, env=entorno, capture_output=True, text=True)
            t = pr.returncode != 0
            quien = ""
            if t:
                ls = [x for x in pr.stdout.split("\n") if x.startswith("FAILED") or x.startswith("ERROR")]
                quien = ls[0][:110] if ls else pr.stdout[-150:].replace("\n", " ")
            estado = "muere" if (cc or t) else "VIVE"
            print(f"{ident} {estado:5s} CC={'-' if cc is None else 'sí' if cc else 'no'} T={'sí' if t else 'no'} · {ficha or 'regla'} · {desc} {('· ' + quien) if quien else ''}", flush=True)
            if not (cc or t):
                vivos.append(ident)
    finally:
        fuente.write_text(original, encoding="utf-8")
    print(f"\n{total} mutantes; vivos: {vivos or 'ninguno'}")
    if not SOLO:
        shutil.rmtree(DESTINO)
    return 1 if vivos else 0


if __name__ == "__main__":
    sys.exit(main())
