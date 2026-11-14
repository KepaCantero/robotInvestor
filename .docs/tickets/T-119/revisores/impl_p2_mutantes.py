"""T-119 · mutantes de las fórmulas y de las reglas de `bloque_a/motor/fichas_p2.py`.

Cada mutante cambia una fórmula, una cota o una regla de rechazo en una COPIA de `bloque_a/11_Ejecutor`; el árbol del
repositorio no se toca. Para cada mutante se mira quién lo caza:

  - CC: los casos de control de la ficha (`CASOS_CONTROL`: dos pasadas que deben coincidir y `comprobar`), que es lo que
        decide la promoción a IMPLEMENTADO (§20.2 del Catálogo);
  - T:  las pruebas del módulo (`tests/test_t119_p2.py`, con `-x`). Para no gastar una pasada entera por mutante, primero
        se ejecutan solo las pruebas de su ficha (`-k`); si el mutante sobrevive a ellas, se ejecuta el fichero entero.

Un mutante vivo frente a CC y T es una regla sin red. Los mutantes de reglas de rechazo y de cotas no tienen CC (los casos de
control solo ven resultados servidos): para ellos solo cuenta T.

Uso (desde la raíz del repositorio):
    .venv/bin/python -I -B .docs/tickets/T-119/revisores/impl_p2_mutantes.py DESTINO [--solo ID] [--python RUTA]
DESTINO es una carpeta de trabajo desechable (p. ej. `…/scratchpad/p2_mut`); se crea dentro `copia_ejecutor/`.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
args = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith("--") and sys.argv[i - 1] not in ("--solo", "--python")]
if not args:
    sys.exit(__doc__)
DESTINO = Path(args[0]).resolve()
SOLO = sys.argv[sys.argv.index("--solo") + 1] if "--solo" in sys.argv else None
PY = sys.argv[sys.argv.index("--python") + 1] if "--python" in sys.argv else (
    str(RAIZ / ".venv" / "bin" / "python") if (RAIZ / ".venv" / "bin" / "python").exists() else sys.executable)
PRUEBAS = "tests/test_t119_p2.py"
MODULO = "bloque_a/motor/fichas_p2.py"

# (id, ficha para CC o None si es una regla de rechazo o una cota, [(texto original, texto mutado)], descripción)
MUTANTES: list[tuple[str, str | None, list[tuple[str, str]], str]] = [
    # ---------------------------------------------------------------- FIR-CRED-001
    ("M01", "FIR-CRED-001", [('D = corto + u["factor_deuda_largo"] * largo', "D = corto + largo")], "punto de impago con toda la deuda a largo"),
    ("M02", "FIR-CRED-001", [("d2 = d1 - raiz\n    dd_real", "d2 = d1 + raiz\n    dd_real")], "signo de d₂"),
    ("M03", "FIR-CRED-001", [("dd_real = (math.log(V / D) + (mu - 0.5 * sV * sV) * T) / raiz", "dd_real = (math.log(V / D) + (mu + 0.5 * sV * sV) * T) / raiz")],
     "DD real con +σ²/2"),
    ("M04", "FIR-CRED-001", [("pd_rn = float(special.ndtr(-d2))", "pd_rn = float(special.ndtr(-d1))")], "PD con d₁"),
    ("M05", "FIR-CRED-001", [("dif = -math.log(float(special.ndtr(d2)) + recuperado) / T ", "dif = -math.log(float(special.ndtr(d2))) / T ")],
     "diferencial implícito sin recuperación"),
    ("M06", "FIR-CRED-001", [("sV = E / V * sE + D / V * (a_sd + b_sd * sE)", "sV = E / V * sE")], "ingenuo sin volatilidad de la deuda"),
    ("M07", "FIR-CRED-001", [("w = np.array(deudas) / float(np.sum(deudas))", "w = np.full(len(deudas), 1 / len(deudas))")],
     "media sin ponderar por deuda"),
    ("M08", "FIR-CRED-001", [('float(np.mean(dd < u["dd_umbral"])) * PCT', 'float(np.mean(dd <= u["dd_umbral"] + 1)) * PCT')], "umbral de DD < 2 movido"),
    ("M09", "FIR-CRED-001", [("tri = -math.log1p(-pd_rn) / T * (1 - recuperado / pd_rn)", "tri = pd_rn / T * (1 - recuperado / pd_rn)")],
     "triángulo con la PD y no con la intensidad"),
    ("M10", "FIR-CRED-001", [("return float(special.ndtr(opcion(V, s)[1])) * s * V / E - sE", "return s * V / E - sE")],
     "segunda ecuación de Merton sin N(d₁)"),
    ("M11", "FIR-CRED-001", [('real = bloque(col["dd_real"], col["pd_real"])', 'real = bloque(col["dd"], col["pd"])')], "bloque real con las medidas neutrales"),
    ("M12", None, [('        raise ErrorFicha(f"{F}: rechazo: la ficha no es válida para segmentos de bancos y aseguradoras")', "        pass")],
     "sin el rechazo de bancos y aseguradoras"),
    ("M13", None, [('    if isinstance(comps, list) and len(comps) < u["componentes_minimos"]:', "    if False:")], "sin el rechazo por < 10 componentes"),
    ("M14", None, [('    if cobertura < u["cobertura_minima"]:', "    if False:")], "sin el rechazo por cobertura"),
    ("M15", None, [('"T_maximo_anios": ANIOS_H5_MAX,', '"T_maximo_anios": ANIOS_H5_MAX + 1,')], "cota de T"),
    ("M16", "FIR-CRED-001", [("pd_ref = (real or neutral)", "pd_ref = neutral")], "referencia ingenua contra la PD neutral"),
    # ---------------------------------------------------------------- FX-BEER-001
    ("M17", "FX-BEER-001", [("filas = np.arange(k + 1, T_ - k)\n    Z = np.column_stack([np.ones(len(filas)), X[filas]] + [dX[filas - 1 + j] for j in range(-k, k + 1)])",
                             "filas = np.arange(k + 1, T_ - k)\n    Z = np.column_stack([np.ones(len(filas)), X[filas]] + [dX[filas - 1 + j] for j in range(-k, 1)])")],
     "DOLS sin adelantos"),
    ("M18", "FX-BEER-001", [("z = sin_centrar - const ", "z = sin_centrar - const * 0.999 ")], "desalineamiento sin media nula"),
    ("M19", "FX-BEER-001", [("des = math.expm1(float(z[-1])) * PCT", "des = float(z[-1]) * PCT")], "desalineamiento en logaritmos"),
    ("M20", "FX-BEER-001", [("d = X[-1] - X.mean(axis=0)", "d = X[-1]")], "IC sin centrar los fundamentales"),
    ("M21", "FX-BEER-001", [("zc = float(stats.norm.ppf(1 - (1 - nivel_ic) / 2))", "zc = float(stats.norm.ppf(nivel_ic))")], "IC de una cola"),
    ("M22", "FX-BEER-001", [("S = S + (1 - rez / (rezagos + 1)) * (G + G.T)", "S = S + (G + G.T)")], "HAC sin el núcleo de Bartlett"),
    ("M23", "FX-BEER-001", [("ppa = math.expm1(float(q[-1] - np.mean(q))) * PCT", "ppa = math.expm1(float(q[-1] - np.median(q))) * PCT")],
     "PPA con la mediana"),
    ("M24", "FX-BEER-001", [('"vida_media_anios": None if vm["vida_media_periodos"] is None else vm["vida_media_periodos"] / TRIMESTRES_ANIO',
                             '"vida_media_anios": None if vm["vida_media_periodos"] is None else vm["vida_media_periodos"]')], "vida media en trimestres"),
    ("M25", "FX-BEER-001", [("beta = -vec[1:m + 1] / vec[0]", "beta = vec[1:m + 1] / vec[0]")], "signo del vector de Johansen"),
    ("M26", "FX-BEER-001", [("critico = fs._critico(fs._CRIT_TAU, m + 1, nivel)", "critico = fs._critico(fs._CRIT_TAU, m, nivel)")],
     "valor crítico con una variable menos"),
    ("M27", None, [('    if n < u["anios_rechazo"] * TRIMESTRES_ANIO:', "    if False:")], "sin el rechazo por < 15 años"),
    ("M28", None, [("    if vintage < t.index[-1]:", "    if False:")], "sin la regla del vintage"),
    ("M29", None, [('"rango_retardos": (1, 4)', '"rango_retardos": (1, 5)')], "cota de retardos"),
    ("M30", "FX-BEER-001", [('"velocidad_correccion_trimestral": vm["rho"] - 1', '"velocidad_correccion_trimestral": vm["rho"]')], "velocidad = ρ"),
    # ---------------------------------------------------------------- CMD-REAL-001
    ("M31", "CMD-REAL-001", [("real = precio * ipc[-1] / ipc", "real = precio * ipc / ipc[-1]")], "deflactor invertido"),
    ("M32", "CMD-REAL-001", [("real = precio * ipc[-1] / ipc", "real = precio * ipc[0] / ipc")], "base en el primer mes"),
    ("M33", "CMD-REAL-001", [("return math.expm1(MESES_ANIO * pendiente) * PCT", "return MESES_ANIO * pendiente * PCT")], "tendencia sin componer"),
    ("M34", "CMD-REAL-001", [("mk = op.mann_kendall(np.log(real),", "mk = op.mann_kendall(real,")], "tendencia sobre el nivel"),
    ("M35", "CMD-REAL-001", [('i_p = int(np.argmax(acumulada >= p["percentil_coste"] * acumulada[-1] * (1 - tol)))',
                              'i_p = int(np.argmax(acumulada > p["percentil_coste"] * acumulada[-1] * (1 + tol)))')], "percentil de costes estricto"),
    ("M36", "CMD-REAL-001", [("pares = sorted((_rango(_dict(tr", "pares = list((_rango(_dict(tr")], "curva de costes sin ordenar"),
    ("M37", "CMD-REAL-001", [("coste_real = coste * float(ipc[-1] / ipc[mes])", "coste_real = coste")], "coste sin deflactar"),
    ("M38", "CMD-REAL-001", [('"precio_sobre_coste": actual / coste_real', '"precio_sobre_coste": float(precio[-1]) / coste')], "razón en nominal"),
    ("M39", None, [('    if n < u["anios_rechazo"] * MESES_ANIO:', "    if False:")], "sin el rechazo por < 15 años"),
    ("M40", None, [('    if _texto(v.get("ipc_moneda"), f"{F}: «ipc_moneda»") != moneda:', "    if False:")], "sin la regla del IPC de la moneda"),
    ("M41", None, [("    if mes < 0:", "    if False:")], "curva de costes fuera de la serie"),
    # ---------------------------------------------------------------- REI-LEV-001
    ("M42", "REI-LEV-001", [('("neta", deuda - caja)', '("neta", deuda)')], "LTV con deuda bruta"),
    ("M43", "REI-LEV-001", [("prox = perfil[perfil.index <= horizonte]", "prox = perfil[perfil.index < horizonte]")], "borde de los 24 meses"),
    ("M44", "REI-LEV-001", [('horizonte = fecha + pd.DateOffset(months=u["meses_vencimientos"])', 'horizonte = fecha + pd.DateOffset(months=u["meses_vencimientos"] + 1)')],
     "25 meses"),
    ("M45", "REI-LEV-001", [("coste_nuevo = swap + margen", "coste_nuevo = swap")], "coste de refinanciación sin margen"),
    ("M46", "REI-LEV-001", [('"impacto_ffo_pct": -tot["extra"] / tot["ffo"] * PCT', '"impacto_ffo_pct": tot["extra"] / tot["ffo"] * PCT')], "signo del impacto en FFO"),
    ("M47", "REI-LEV-001", [('f"{c:g}": tot["neta"] / (tot["gav"] * (1 + c)) * PCT', 'f"{c:g}": tot["neta"] / (tot["gav"] * (1 - c)) * PCT')], "LTV estresado con la caída al revés"),
    ("M48", "REI-LEV-001", [('"icr_veces": tot["ebitda"] / tot["gf"]', '"icr_veces": tot["gf"] / tot["ebitda"]')], "ICR invertido"),
    ("M49", "REI-LEV-001", [("holg_icr.append(ebitda / gf - imin)", "holg_icr.append(imin - ebitda / gf)")], "holgura de ICR al revés"),
    ("M50", "REI-LEV-001", [("float(np.mean(neta_cov / (gav_cov * (1 + c)) > lmax_a)) * PCT", "float(np.mean(neta_cov / gav_cov > lmax_a)) * PCT")],
     "incumplimiento estresado sin la caída"),
    ("M51", None, [("        if err > tol:                                                   # «Verificación»", "        if False:  #")],
     "sin la verificación suma de vencimientos = deuda"),
    ("M52", None, [("        if perfil.index[0] < fecha:", "        if False:")], "vencimientos ya pasados"),
    ("M53", None, [('    if not tot["ffo"] > 0:', "    if False:")], "FFO agregado no positivo"),
    ("M54", "REI-LEV-001", [("caida_rompe.append((ltv_i / lmax - 1) * PCT)", "caida_rompe.append((lmax / ltv_i - 1) * PCT)")], "caída que agota el LTV invertida"),
    # ---------------------------------------------------------------- CHR-ONCHAIN-001
    ("M55", "CHR-ONCHAIN-001", [("sd = float(np.std(cm, ddof=1))", "sd = float(np.std(cm))")], "σ poblacional"),
    ("M56", "CHR-ONCHAIN-001", [("mvrv, z, nvt = cm / cr, (cm - cr) / sd, cm / vol", "mvrv, z, nvt = cm / cr, (cm - cr) / float(np.std(cr, ddof=1)), cm / vol")],
     "MVRV-Z con σ de la realizada"),
    ("M57", "CHR-ONCHAIN-001", [("mvrv, z, nvt = cm / cr, (cm - cr) / sd, cm / vol", "mvrv, z, nvt = cm / cr, (cm - cr) / sd, cr / vol")], "NVT con la realizada"),
    ("M58", "CHR-ONCHAIN-001", [('senal = cm[w - 1:] / (np.convolve(vol, np.ones(w), "valid") / w)', 'senal = cm[w - 1:] / (np.convolve(vol, np.ones(w), "valid") / (w + 1))')],
     "media móvil con otro divisor"),
    ("M59", "CHR-ONCHAIN-001", [('senal = cm[w - 1:] / (np.convolve(vol, np.ones(w), "valid") / w)', 'senal = (np.convolve(cm, np.ones(w), "valid") / w) / (np.convolve(vol, np.ones(w), "valid") / w)')],
     "señal NVT con la capitalización también promediada"),
    ("M60", None, [('    if n < u["dias_minimos"]:', "    if False:")], "sin el mínimo de 2 años"),
    ("M61", None, [('    if p["fuente"] is not None and p["fuente"] != fuente:\n        raise ErrorFicha(f"{F}: los datos son de la fuente', '    if False:\n        raise ErrorFicha(f"{F}: los datos son de la fuente')],
     "fuente de la petición sin comprobar"),
    ("M62", None, [('"rango_media_nvt": (1, DIAS_ANIO)', '"rango_media_nvt": (1, DIAS_ANIO + 1)')], "cota de media_nvt"),
    ("M63", None, [('        lim.append(f"pocos ciclos: {n} días', '        pass; (f"pocos ciclos: {n} días')], "sin la limitación «pocos ciclos»"),
    # ---------------------------------------------------------------- CHR-TOKEN-001
    ("M64", "CHR-TOKEN-001", [("fdv.append(precio * (maxima if maxima is not None else total))", "fdv.append(precio * total)")], "FDV con la oferta total"),
    ("M65", "CHR-TOKEN-001", [("neta.append((emision - quema) / circ)", "neta.append((emision - quema) / total)")], "inflación sobre la oferta total"),
    ("M66", "CHR-TOKEN-001", [("neta.append((emision - quema) / circ)", "neta.append((emision + quema) / circ)")], "quema sumada"),
    ("M67", "CHR-TOKEN-001", [("desb[w].append(math.fsum(c for f_d, c in futuros if f_d <= limite) / circ)", "desb[w].append(math.fsum(c for f_d, c in futuros if f_d < limite) / circ)")],
     "borde de la ventana de desbloqueo"),
    ("M68", "CHR-TOKEN-001", [("            if f_d > fecha:\n                futuros.append((f_d, cantidad))", "            if f_d >= fecha:\n                futuros.append((f_d, cantidad))")],
     "desbloqueo del día de los datos contado"),
    ("M69", "CHR-TOKEN-001", [("w_cm = a_cm / float(np.sum(a_cm))", "w_cm = np.full(len(a_cm), 1 / len(a_cm))")], "agregado equiponderado"),
    ("M70", "CHR-TOKEN-001", [('abierto_hi=True) - neta[-1]))', 'abierto_hi=True) + neta[-1]))')], "rendimiento real = nominal + inflación"),
    ("M71", None, [("        if circ > total or (maxima is not None and total > maxima):", "        if circ > total:")], "sin total ≤ máxima"),
    ("M72", None, [("        if pendiente > bloqueada * (1 + tol) + tol * total:", "        if False:")], "desbloqueos por encima de la oferta no circulante"),
    ("M73", "CHR-TOKEN-001", [("holgura = min(holgura, (bloqueada - pendiente) / total)", "holgura = min(holgura, (bloqueada - pendiente) / circ)")], "holgura sobre la circulante"),
    # ---------------------------------------------------------------- PRV-PME-001 y PRV-CF-001
    ("M74", "PRV-PME-001", [("factor = float(niveles[f_nav]) / niveles.reindex(fl.index).to_numpy()", "factor = niveles.reindex(fl.index).to_numpy() / float(niveles[f_nav])")],
     "factor del índice invertido"),
    ("M75", "PRV-PME-001", [("ks = (vf_d + nav) / vf_c", "ks = vf_d / vf_c")], "KS-PME sin NAV"),
    ("M76", "PRV-PME-001", [('"alfa_directo_pct_anual": None if capitalizada is None else math.log1p(capitalizada) * PCT', '"alfa_directo_pct_anual": None if capitalizada is None else capitalizada * PCT')],
     "alfa directo sin logaritmo"),
    ("M77", "PRV-PME-001", [("lam = (vf_c - nav) / vf_d", "lam = vf_c / vf_d")], "λ de PME+ sin NAV"),
    ("M78", "PRV-PME-001", [("t = (dias - dias[0]) / DIAS_ANIO", "t = (dias - dias[0]) / (DIAS_ANIO + 0.25)")], "TIR con 365,25 días"),
    ("M79", "PRV-PME-001", [('"tvpi_veces": (float(np.sum(D)) + nav) / float(np.sum(C)), "dpi_veces"', '"tvpi_veces": (float(np.sum(D))) / float(np.sum(C)), "dpi_veces"')], "TVPI sin NAV"),
    ("M80", None, [("    faltan = [f for f in [*fl.index, f_nav] if f not in niveles.index]", "    faltan = []")], "índice sin nivel en una fecha de flujo"),
    ("M81", None, [('    if ind.get("rentabilidad_total") is not True:', "    if False:")], "índice de precios admitido"),
    ("M82", None, [("    if cambios > 1:\n        lim.append", "    if cambios > 3:\n        lim.append")], "sin el aviso de múltiples soluciones"),
    ("M83", "PRV-CF-001", [("d = max(y_min, (t / vida) ** bow) * nav * (1 + g)", "d = max(y_min, (t / vida) ** bow) * nav")], "distribución sin crecimiento"),
    ("M84", "PRV-CF-001", [("nav = nav * (1 + g) + c - d", "nav = nav * (1 + g) - d")], "NAV sin la aportación"),
    ("M85", "PRV-CF-001", [("c = tasas[min(t, len(tasas)) - 1] * max(compromiso - aportado, 0.0)", "c = tasas[min(t, len(tasas)) - 1] * compromiso")], "aportación sobre el compromiso total"),
    ("M86", "PRV-CF-001", [("c = tasas[min(t, len(tasas)) - 1] * max(compromiso - aportado, 0.0)", "c = tasas[0] * max(compromiso - aportado, 0.0)")], "tasa del primer año siempre"),
    ("M87", "PRV-CF-001", [("edad = int((f_nav - fl.index[0]).days // DIAS_ANIO)", "edad = int((f_nav - fl.index[0]).days // DIAS_ANIO) + 1")], "edad con un año de más"),
    ("M88", "PRV-CF-001", [("acumulado = np.cumsum(D - C)", "acumulado = np.cumsum(C - D)")], "curva J con el signo cambiado"),
    ("M89", "PRV-CF-001", [('"rvpi_veces": nav / aportado', '"rvpi_veces": nav / compromiso')], "RVPI sobre el compromiso"),
    ("M90", None, [('"rango_bow": (1, 5)', '"rango_bow": (1, 6)')], "cota del bow"),
    ("M91", None, [("    if f_nav < fl.index[-1]:\n        raise ErrorFicha(f\"{F}: el último NAV", "    if False:\n        raise ErrorFicha(f\"{F}: el último NAV")], "NAV anterior al último flujo"),
    # ---------------------------------------------------------------- ALT-HF-001
    ("M92", "ALT-HF-001", [("r, rf, Fm = (r[1:] - phi * r[:-1]) / (1 - phi), rf[1:], Fm[1:]", "r, rf, Fm = (r[1:] - phi * r[:-1]) / (1 - phi), rf[1:], Fm[:-1]")],
     "factores desalineados un mes tras desuavizar"),
    ("M93", "ALT-HF-001", [("r, rf, Fm = (r[1:] - phi * r[:-1]) / (1 - phi), rf[1:], Fm[1:]", "r, rf, Fm = (r[1:] - phi * r[:-1]), rf[1:], Fm[1:]")], "Geltner sin dividir por 1 − φ"),
    ("M94", "ALT-HF-001", [("    y = r - rf\n", "    y = r\n")], "sin restar el tipo sin riesgo"),
    ("M95", "ALT-HF-001", [("base = fv._regresion(y, Fm, nombres, MESES_ANIO, lim, F)", "base = fv._regresion(y, Fm, nombres, TRIMESTRES_ANIO, lim, F)")], "alfa anualizada con 4 periodos"),
    ("M96", "ALT-HF-001", [('"exceso_periodo_pct": media - pasiva', '"exceso_periodo_pct": media')], "referencia ingenua sin restar la cartera pasiva"),
    ("M97", None, [('    if n < u["observaciones_minimas"]:\n        raise ErrorFicha(f"{F}: rechazo: {n} observaciones mensuales', '    if False:\n        raise ErrorFicha(f"{F}: rechazo: {n} observaciones mensuales')],
     "sin el rechazo por < 36 observaciones"),
    ("M98", None, [("        if not -1 < phi < 1:", "        if False:")], "φ fuera de (−1, 1)"),
    ("M99", "ALT-HF-001", [("    if p[\"desuavizar\"]:\n        phi = _ar1(r)", "    if not p[\"desuavizar\"]:\n        phi = _ar1(r)")], "desuavizar al revés"),
    # ---------------------------------------------------------------- ALT-AUC-001
    ("N01", "ALT-AUC-001", [("    M[filas, per[[b for _, b in utiles]]] = 1.0\n    M[filas, per[[a for a, _ in utiles]]] = -1.0", "    M[filas, per[[b for _, b in utiles]]] = -1.0\n    M[filas, per[[a for a, _ in utiles]]] = 1.0")],
     "signos de compra y venta cambiados"),
    ("N02", "ALT-AUC-001", [("return BASE_INDICE * np.exp(np.concatenate([[0.0], coef]))", "return BASE_INDICE * (1 + np.concatenate([[0.0], coef]))")], "índice sin exponencial"),
    ("N03", "ALT-AUC-001", [("return float((ind[-1] / ind[0] * (1 - coste)) ** (1 / (P - 1)) - 1) * PCT", "return float((ind[-1] / ind[0] * (1 - coste)) ** (1 / P) - 1) * PCT")], "anualización con un año de más"),
    ("N04", "ALT-AUC-001", [("return float((ind[-1] / ind[0] * (1 - coste)) ** (1 / (P - 1)) - 1) * PCT", "return float((ind[-1] / ind[0]) ** (1 / (P - 1)) - 1 - coste) * PCT")], "comisiones restadas cada año"),
    ("N05", "ALT-AUC-001", [('"volatilidad_pct": float(np.std(ind[1:] / ind[:-1] - 1, ddof=1)) * PCT', '"volatilidad_pct": float(np.std(ind[1:] / ind[:-1] - 1)) * PCT')], "volatilidad poblacional"),
    ("N06", "ALT-AUC-001", [('"desviacion_residual_pct": math.sqrt(float(e @ e) / principal["gl"]) * PCT', '"desviacion_residual_pct": math.sqrt(float(e @ e) / len(e)) * PCT')], "dispersión sin grados de libertad"),
    ("N07", "ALT-AUC-001", [("    utiles = [(a, b) for a, b in pares if per[a] != per[b]]", "    utiles = pares")], "pares del mismo año admitidos"),
    ("N08", "ALT-AUC-001", [("orden = sorted(range(len(ids)), key=lambda i: (ids[i], fechas[i], i))", "orden = sorted(range(len(ids)), key=lambda i: (ids[i], i))")], "ventas sin ordenar por fecha"),
    ("N09", None, [('    if isinstance(trans, list) and len(trans) < u["transacciones_minimas"]:', "    if False:")], "sin el rechazo por < 500 transacciones"),
    ("N10", None, [('    if vr["indice"] is not None and vr["n_pares"] < u["pares_minimos"]:', "    if False:")], "sin el rechazo por < 200 pares"),
    ("N11", None, [("    if len(np.unique(per)) < P:", "    if False:")], "años sin transacciones"),
    ("N12", "ALT-AUC-001", [('ref["rentabilidad_real_anual_pct"] = ((1 + bruta / PCT) / (1 + infl) - 1) * PCT', 'ref["rentabilidad_real_anual_pct"] = bruta - infl * PCT')], "rentabilidad real por resta"),
    ("N13", "ALT-AUC-001", [("    X = np.column_stack([np.ones(len(lp)), car, dum[:, 1:]])", "    X = np.column_stack([np.ones(len(lp)), dum[:, 1:]])\n    car = car[:, :0]")], "hedónico sin características"),
    ("N14", None, [('"rango_comisiones": (0.10, 0.25)', '"rango_comisiones": (0.10, 0.30)')], "cota de comisiones"),
    # ---------------------------------------------------------------- comunes
    ("N15", None, [("MAGNITUD_MAX = 1e100", "MAGNITUD_MAX = 1e400")], "sin la cota de magnitud"),
    ("N16", None, [("    desconocidos = set(params) - set(PARAMETROS_POR_DEFECTO[ficha]) - AJENOS\n    if desconocidos:", "    desconocidos = set(params) - set(PARAMETROS_POR_DEFECTO[ficha]) - AJENOS\n    if False:")],
     "parámetros no declarados admitidos"),
    ("N17", None, [("    fijos = set(params) & set(UMBRALES[ficha])\n    if fijos:", "    fijos = set(params) & set(UMBRALES[ficha])\n    if False:")], "umbrales cambiables desde la petición"),
    ("N18", None, [("    if len(lst) > maximo:\n        raise ErrorFicha(f\"{que}: {len(lst)} elementos (máximo {maximo})\")\n    return lst\n\n\ndef _tabla_acotada",
                    "    if False:\n        raise ErrorFicha(f\"{que}: {len(lst)} elementos (máximo {maximo})\")\n    return lst\n\n\ndef _tabla_acotada")], "listas de datos sin cota"),
    ("N19", None, [("    f = _fecha(v.get(clave), f\"{que}: «{clave}»\")\n    _hasta_corte([f], corte, f\"{que}: «{clave}»\")", "    f = _fecha(v.get(clave), f\"{que}: «{clave}»\")")],
     "fechas sueltas sin fecha de corte"),
    ("N20", None, [("COMPONENTES_MAX = 500 ", "COMPONENTES_MAX = 501 ")], "cota de componentes"),
    ("N21", None, [('"transacciones_maximas": 50_000', '"transacciones_maximas": 50_001')], "cota de transacciones"),
    ("N22", None, [('"tolerancia_raiz": 1e-13,\n                     "iteraciones_maximas": 200},', '"tolerancia_raiz": 1e-3,\n                     "iteraciones_maximas": 200},')],
     "tolerancia de la raíz de Merton relajada"),
    ("N23", None, [('            if isinstance(ent, dict) and (ent.get("series") or ent.get("series_rol")):', "            if False:")], "series de HT-01 ignoradas en silencio"),
    ("N24", None, [("    if rango < P - 1:", "    if False:")], "ventas repetidas sin comprobar el rango"),
    ("N25", None, [("    if rango < X.shape[1]:", "    if False:")], "hedónico sin comprobar el rango"),
]

GUION_CC = r"""
import copy, sys
sys.path.insert(0, ".")
from bloque_a.motor import fichas_p2 as m
from bloque_a.motor import servicio
f = sys.argv[1]
ok = True
for c in m.CASOS_CONTROL[f]:
    try:
        v = {}
        for d in c["datos"]:
            v.update(copy.deepcopy(d["valores"]))
        r1, _ = m.FICHAS[f]["fn"]({"valores": copy.deepcopy(v), "series": {}, "series_rol": {}}, dict(c["parametros"]))
        r2, _ = m.FICHAS[f]["fn"]({"valores": copy.deepcopy(v), "series": {}, "series_rol": {}}, dict(c["parametros"]))
        ok = ok and bool(c["comprobar"](r1)) and servicio._limpio(r1) == servicio._limpio(r2)
    except Exception:
        ok = False
sys.exit(0 if ok else 1)
"""


def main() -> int:
    copia = DESTINO / "copia_ejecutor"
    if copia.exists():
        shutil.rmtree(copia)
    shutil.copytree(RAIZ / "bloque_a" / "11_Ejecutor", copia, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    # el Catálogo (lo lee `servicio`): una copia al lado, como en el repositorio
    cat = RAIZ / "bloque_a" / "04_Motor_conocimiento_y_catalogo"
    (DESTINO / cat.name).mkdir(exist_ok=True)
    for md in cat.glob("*.md"):
        shutil.copy(md, DESTINO / cat.name / md.name)
    fuente = copia / MODULO
    original = fuente.read_text(encoding="utf-8")
    entorno = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "BLOQUE_A_RAIZ": str(DESTINO)}
    vivos, total, actual = [], 0, None
    for ident, ficha, cambios, desc in MUTANTES:
        actual = ficha or actual            # una regla sin ficha es de la sección de la última ficha vista
        if ident >= "N15":                  # las reglas comunes no son de ninguna ficha
            actual = None
        if SOLO and ident != SOLO:
            continue
        total += 1
        texto = original
        for a, b in cambios:
            if texto.count(a) != 1:
                print(f"{ident}: el texto original aparece {texto.count(a)} veces (se esperaba 1): {a[:70]!r}")
                return 2
            texto = texto.replace(a, b)
        fuente.write_text(texto, encoding="utf-8")
        cc = None
        if ficha:
            cc = subprocess.run([PY, "-B", "-c", GUION_CC, ficha], cwd=copia, env=entorno, capture_output=True, check=False).returncode != 0
        base = [PY, "-B", "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider", PRUEBAS]
        t = False
        if actual:
            clave = f"{actual} or {actual[:-4].lower().replace('-', '_')}" + (" or tir" if actual.startswith("PRV") else "")
            t = subprocess.run([*base, "-k", clave], cwd=copia, env=entorno, capture_output=True, check=False).returncode == 1
        if not t:
            t = subprocess.run(base, cwd=copia, env=entorno, capture_output=True, check=False).returncode != 0
        estado = "muere" if (cc or t) else "VIVE"
        print(f"{ident} {estado:5s} CC={'-' if cc is None else 'sí' if cc else 'no'} T={'sí' if t else 'no'} · {ficha or 'regla'} · {desc}", flush=True)
        if not (cc or t):
            vivos.append(ident)
    fuente.write_text(original, encoding="utf-8")
    print(f"\n{total} mutantes; vivos: {vivos or 'ninguno'}")
    return 1 if vivos else 0


if __name__ == "__main__":
    sys.exit(main())
