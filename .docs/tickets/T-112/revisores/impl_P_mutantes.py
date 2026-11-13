"""T-112 · grupo P · mutantes de las fórmulas principales de `bloque_a/motor/fichas_reales.py`.

Cada mutante cambia una fórmula (o una regla de rechazo) en una COPIA de `bloque_a` (sin los .docx); el árbol del
repositorio no se toca. Para cada mutante se mira quién lo caza:

  - CC: los casos de control de la ficha (`CASOS_CONTROL`, dos pasadas que deben coincidir y `comprobar`), que es lo que
        decide la promoción a IMPLEMENTADO (§20.2 del Catálogo);
  - T:  las pruebas del grupo (`tests/test_fase2_reales.py`).

Un mutante vivo frente a CC y T es una regla sin red. Los mutantes de reglas de rechazo no tienen CC (los casos de control
solo ven resultados servidos): para ellos solo cuenta T.

Uso (desde la raíz del repositorio):
    .venv/bin/python -I -B .docs/tickets/T-112/revisores/impl_P_mutantes.py DESTINO [--solo ID]
DESTINO es una carpeta de trabajo (p. ej. el scratchpad de la sesión); se crea dentro `copia_bloque_a/`.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
args = [a for a in sys.argv[1:] if not a.startswith("--")]
if not args:
    sys.exit(__doc__)
DESTINO = Path(args[0]).resolve()
SOLO = sys.argv[sys.argv.index("--solo") + 1] if "--solo" in sys.argv else None
PY = str(RAIZ / ".venv" / "bin" / "python") if (RAIZ / ".venv" / "bin" / "python").exists() else sys.executable
PRUEBAS = "tests/test_fase2_reales.py"

# (id, ficha para CC o None si es una regla de rechazo, [(texto original, texto mutado)], descripción)
MUTANTES: list[tuple[str, str | None, list[tuple[str, str]], str]] = [
    # ---------------------------------------------------------------- REI-CAP-001
    ("P01", "REI-CAP-001", [("cap_tas = noi / valor_tas ", "cap_tas = noi / (valor_tas + noi) ")], "cap rate con NOI en el denominador"),
    ("P02", "REI-CAP-001", [("valor_mer = capit + deuda", "valor_mer = capit")], "valor implícito sin deuda neta"),
    ("P03", "REI-CAP-001", [("dif = (cap_tas - y10) * PB", "dif = (cap_tas - y10) * PCT")], "diferencial en pp y no en pb"),
    ("P04", "REI-CAP-001", [("cap_eq = r - g ", "cap_eq = r ")], "cap de equilibrio sin g_NOI"),
    ("P05", "REI-CAP-001", [('h = hist[hist.index > hist.index[-1] - pd.DateOffset(years=p["ventana"])]', "h = hist")],
     "percentil sin ventana"),
    ("P06", None, [('    if anios < u["anios_historia_minimos"]:\n        raise', "    if False:\n        raise")],
     "sin el rechazo por < 15 años"),
    ("P07", None, [('    if base != p["base_noi"]:', "    if False:")], "sin la aclaración por base del NOI distinta"),
    # ---------------------------------------------------------------- REI-NAV-001
    ("P08", "REI-NAV-001", [('primas = np.array([f["precio"] / f["nav_acc"] - 1 for', 'primas = np.array([f["precio"] / f["nav_acc"] for')],
     "P/NAV sin restar 1"),
    ("P09", "REI-NAV-001", [('w = np.array([f["capit"] / capit_total for f in filas])', "w = np.full(len(filas), 1 / len(filas))")],
     "agregado equiponderado en vez de por capitalización"),
    ("P10", "REI-NAV-001", [('f["gav"] * (f["cap"] / cap_obj)', 'f["gav"] * (cap_obj / f["cap"])')], "ratio de cap rates invertido"),
    ("P11", "REI-NAV-001", [('(f["cap"] / cap_obj) - f["deuda"] - f["otros"]', '(f["cap"] / cap_obj) - f["deuda"]')],
     "NAV ajustado sin otros pasivos"),
    ("P12", "REI-NAV-001", [("np.sum(w * (primas - prima_agg) ** 2)", "np.mean((primas - prima_agg) ** 2)")],
     "dispersión sin ponderar"),
    ("P13", None, [('        if fn_ + pd.DateOffset(months=u["meses_antiguedad_nav_max"]) < fp:', "        if False:")],
     "sin el rechazo por NAV de más de 12 meses"),
    ("P14", None, [("            if err > tol:", "            if False:")], "sin el rechazo NAV ≠ activos − pasivos"),
    # ---------------------------------------------------------------- REI-FFO-001
    ("P15", "REI-FFO-001", [("ffo = bn + am - pl ", "ffo = bn + am + pl ")], "FFO sumando las plusvalías"),
    ("P16", "REI-FFO-001", [("affo = ffo - capex - aj ", "affo = ffo - capex ")], "AFFO sin ajustes de rentas lineales"),
    ("P17", "REI-FFO-001", [('capex = p["capex_pct_rentas"] * _rango', 'capex = 2 * p["capex_pct_rentas"] * _rango')],
     "CAPEX estimado con el doble del %"),
    ("P18", "REI-FFO-001", [('"mediana": q50,', '"mediana": float(np.mean(cob)),')], "cobertura en media y no en mediana"),
    ("P19", "REI-FFO-001", [('p_ffo = cap_total / act["ffo"] if', 'p_ffo = cap_total / act["affo"] if')], "P/FFO con el AFFO"),
    ("P20", None, [('            if e.get("amortizaciones_inmobiliarias") is None:', "            if False:")],
     "sin el rechazo por amortizaciones sin desglosar"),
    ("P21", None, [('    if len(comunes) < u["ejercicios_minimos"]:', "    if False:")], "sin el rechazo por < 3 ejercicios"),
    # ---------------------------------------------------------------- CMD-INV-001
    ("P22", "CMD-INV-001", [("media = float(np.mean(xr))", "media = float(np.median(xr))")], "media estacional por mediana"),
    ("P23", "CMD-INV-001", [("for a in range(anio - anos, anio):", "for a in range(anio - anos - 1, anio):")],
     "un año estacional de más"),
    ("P24", "CMD-INV-001", [("        if a in excluir:\n            continue\n", "")], "sin excluir_anos"),
    ("P25", "CMD-INV-001", [("sd = float(np.std(xr, ddof=1))", "sd = float(np.std(xr, ddof=0))")], "z con desviación poblacional"),
    ("P26", "CMD-INV-001", [('"sorpresa": d_act - tipica,', '"sorpresa": d_act,')], "sorpresa sin restar la variación típica"),
    ("P27", "CMD-INV-001", [('"dias_cobertura": None if demanda is None else float(x[i]) / demanda',
                             '"dias_cobertura": None if demanda is None else media / demanda')], "cobertura con la media"),
    ("P28", "CMD-INV-001", [("pesos = np.r_[0.5, np.ones(P - 1), 0.5] / P", "pesos = np.ones(P + 1) / (P + 1)")],
     "segunda vía: media móvil 13 simple en vez de 2×12"),
    ("P29", "CMD-INV-001", [("esperado = nivel + s[periodo(i)] - centro", "esperado = nivel + s[periodo(i)]")],
     "segunda vía: índice estacional sin normalizar"),
    ("P30", None, [('    if anios < u["anios_rechazo"]:', "    if False:")], "sin el rechazo por < 3 años"),
    ("P31", None, [('        if not isinstance(o, dict) or o.get("fecha_publicacion") is None:', "        if not isinstance(o, dict):")],
     "sin el rechazo por falta de fecha de publicación"),
    # ---------------------------------------------------------------- CMD-RETDEC-001
    ("P32", "CMD-RETDEC-001", [("    roll = r_f - r_s\n", "    roll = r_f\n")], "roll sin restar el spot"),
    ("P33", "CMD-RETDEC-001", [("        col = r_tot - r_f\n", "        col = r_tot - r_s\n")], "colateral frente al spot"),
    ("P34", "CMD-RETDEC-001", [("col_tipo = tipo[:-1] * dias / DIAS_ANIO", "col_tipo = tipo[1:] * dias / DIAS_ANIO")],
     "colateral con el tipo del final del periodo"),
    ("P35", "CMD-RETDEC-001", [("if d <= fechas[i - 1]][-1]", "if d <= fechas[i]][-1]")], "contrato mantenido mal fechado"),
    ("P36", "CMD-RETDEC-001", [("anual = {k: float(np.mean(a)) * ppa * PCT", "anual = {k: float(np.median(a)) * ppa * PCT")],
     "componentes con la mediana"),
    ("P37", "CMD-RETDEC-001", [("        r_tot = r_f + col\n", "        r_tot = r_f\n")], "total sin colateral (contratos)"),
    ("P38", None, [('        if not isinstance(bloque.get("calendario_roll"), str) or not bloque["calendario_roll"].strip():',
                    "        if False:")], "sin el rechazo por falta de calendario del índice"),
    # ---------------------------------------------------------------- CHR-FUND-001
    ("P39", "CHR-FUND-001", [('t["tasa"] * (HORAS_DIA / horas) * DIAS_ANIO', 't["tasa"] * 3 * DIAS_ANIO')],
     "3 periodos al día siempre (ignora el de 4 h)"),
    ("P40", "CHR-FUND-001", [("fin = (A * W).sum(axis=1) / W.sum(axis=1)", "fin = A.mean(axis=1)")],
     "financiación sin ponderar por interés abierto"),
    ("P41", "CHR-FUND-001", [("* DIAS_ANIO / dias,", "* DIAS_ANIO / (dias + 1),")], "base con un día de más"),
    ("P42", "CHR-FUND-001", [('pd.Timedelta(days=p["ventana_percentil"])]', 'pd.Timedelta(days=2 * p["ventana_percentil"])]')],
     "percentil sobre 2 años"),
    ("P43", "CHR-FUND-001", [("np.mean(h.to_numpy() <= float(serie.iloc[-1]))", "np.mean(h.to_numpy() < float(serie.iloc[-1]))")],
     "percentil estricto"),
    ("P44", "CHR-FUND-001", [("abierto_lo=True) * PCT\n", "abierto_lo=True)\n")], "interés abierto/capitalización sin %"),
    ("P45", None, [('    if len(plat) < u["plataformas_minimas"]:', "    if False:")], "sin el rechazo por < 2 plataformas"),
    # ---------------------------------------------------------------- CHR-FLOW-001
    ("P46", "CHR-FLOW-001", [("mon = float(np.sum(fl[n - w:]))", "mon = float(np.sum(fl[n - w + 1:]))")],
     "acumulado con una sesión de menos"),
    ("P47", "CHR-FLOW-001", [("rel = mon / float(pat[n - w - 1])", "rel = mon / float(pat[n - 1])")],
     "% sobre el patrimonio final"),
    ("P48", "CHR-FLOW-001", [("/ float(pat[j - w]) for j in range(w, n)", "/ float(pat[j]) for j in range(w, n)")],
     "z con el patrimonio final de cada ventana"),
    ("P49", "CHR-FLOW-001", [("crecimiento = float(so.iloc[-1] / previos.iloc[-1] - 1)", "crecimiento = float(so.iloc[-1] / previos.iloc[0] - 1)")],
     "crecimiento desde el inicio y no a 30 días"),
    ("P50", "CHR-FLOW-001", [("so = s if so is None else", "so = s if True else")], "solo la última stablecoin"),
    ("P51", None, [('    if _anios(t.index) * DIAS_ANIO < u["dias_minimos"]:', "    if False:")], "sin el rechazo por < 120 días"),
    ("P52", None, [('        if not isinstance(f, dict) or f.get("fecha_publicacion") is None:', "        if not isinstance(f, dict):")],
     "sin el rechazo por flujos sin fecha de publicación"),
    # ---------------------------------------------------------------- ALT-DESMOOTH-001
    ("P53", "ALT-DESMOOTH-001", [("r = (rs[1:] - phi * rs[:-1]) / (1 - phi)", "r = (rs[1:] - phi * rs[:-1]) / (1 + phi)")],
     "Geltner dividiendo por 1 + φ"),
    ("P54", "ALT-DESMOOTH-001", [("r = (rs[1:] - phi * rs[:-1]) / (1 - phi)", "r = (rs[1:] - phi * rs[1:]) / (1 - phi)")],
     "Geltner sin rezago"),
    ("P55", "ALT-DESMOOTH-001", [("return float(np.sum((a - a.mean()) * db) / np.sum(db * db))", "return float(np.sum(a * b) / np.sum(b * b))")],
     "AR(1) sin constante"),
    ("P56", "ALT-DESMOOTH-001", [("anual = math.sqrt(TRIMESTRES_ANIO)", "anual = TRIMESTRES_ANIO")], "volatilidad anualizada × 4"),
    ("P57", "ALT-DESMOOTH-001", [("(rs[-1] - rs[0]) / (n - 1)", "(rs[-1] - rs[0]) / n")], "término de borde mal contado"),
    ("P58", "ALT-DESMOOTH-001", [("rr[t_ - k: t_][::-1]))) / theta[0]", "rr[t_ - k: t_][::-1])))")], "GLM sin dividir por θ0"),
    ("P59", "ALT-DESMOOTH-001", [("return _invertible(np.r_[1 - np.sum(t), t])", "return np.r_[1 - np.sum(t), t]")],
     "GLM sin la representación invertible"),
    ("P60", "ALT-DESMOOTH-001", [("np.max(1 - riqueza / np.maximum.accumulate(riqueza))", "np.max(1 - riqueza / riqueza[0])")],
     "MDD frente al inicio y no frente al máximo"),
    ("P61", "ALT-DESMOOTH-001", [("return float(np.sum(coef[1:]))", "return float(coef[1])")], "beta sin sumar los rezagos"),
    ("P62", None, [('    if n < u["observaciones_minimas"]:', "    if False:")], "sin el rechazo por < 24 observaciones"),
    # ---------------------------------------------------------------- comunes
    ("P63", None, [("    fijos = set(params) & set(UMBRALES[ficha])\n", "    fijos: set[str] = set()\n")],
     "los umbrales vuelven a poder cambiarse desde la petición"),
    ("P64", "REI-CAP-001", [('return {"percentil": float(np.mean(h <= valor)),', 'return {"percentil": float(np.mean(h < valor)),')],
     "percentil estricto (común)"),
    ("P65", None, [("            if malos:\n", "            if False:\n")], "la envoltura deja pasar no finitos"),
]

CC = """
import json, sys
from pathlib import Path
from bloque_a.motor import fichas_reales as M
assert Path(M.__file__).resolve().is_relative_to(Path({copia!r}).resolve()), M.__file__
malos = []
for caso in M.CASOS_CONTROL[{ficha!r}]:
    v = {{}}
    for d in caso["datos"]:
        v.update(d["valores"])
    try:
        ent = {{"valores": v, "series": {{}}, "series_rol": {{}}}}
        r1, _ = M.FICHAS[{ficha!r}]["fn"](ent, dict(caso["parametros"]))
        r2, _ = M.FICHAS[{ficha!r}]["fn"](ent, dict(caso["parametros"]))
        ok = bool(caso["comprobar"](r1)) and json.dumps(r1, sort_keys=True) == json.dumps(r2, sort_keys=True)
    except Exception as e:  # noqa: BLE001
        ok = False
    if not ok:
        malos.append(caso["nombre"][:50])
print("CAZADO" if malos else "SUPERA", malos)
"""


def main() -> int:
    base = DESTINO / "copia_bloque_a"
    if base.exists():
        shutil.rmtree(base)
    shutil.copytree(RAIZ / "bloque_a", base / "bloque_a", ignore=shutil.ignore_patterns(
        "__pycache__", "*.pyc", ".pytest_cache", ".mypy_cache", "*.egg-info", "build", "*.docx"))
    copia = base / "bloque_a" / "11_Ejecutor"
    entorno = {k: v for k, v in os.environ.items() if k != "BLOQUE_A_RAIZ"}
    entorno.update({"PYTHONPATH": str(copia), "PYTHONDONTWRITEBYTECODE": "1"})
    t0 = subprocess.run([PY, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", PRUEBAS], capture_output=True, text=True,
                        cwd=copia, env=entorno, timeout=1800)
    print("copia sin mutar:", (t0.stdout.strip().splitlines() or [""])[-1])
    if t0.returncode != 0:
        print("las pruebas no pasan en la copia sin mutar: «cazado» no significaría nada")
        return 2
    ruta = copia / "bloque_a" / "motor" / "fichas_reales.py"
    original = ruta.read_text(encoding="utf-8")
    vivos_cc, vivos, n = [], [], 0
    for mid, ficha, cambios, desc in MUTANTES:
        if SOLO and mid != SOLO:
            continue
        texto = original
        for viejo, nuevo in cambios:
            if texto.count(viejo) != 1:
                print(f"{mid}: el mutante no se aplica («{viejo[:60]}» aparece {texto.count(viejo)} veces)")
                return 3
            texto = texto.replace(viejo, nuevo)
        n += 1
        ruta.write_text(texto, encoding="utf-8")
        try:
            if ficha:
                cc = subprocess.run([PY, "-B", "-c", CC.format(copia=str(copia), ficha=ficha)], capture_output=True,
                                    text=True, cwd=copia, env=entorno, timeout=600)
                cazado_cc: bool | None = "CAZADO" in cc.stdout or cc.returncode != 0
                linea = (cc.stdout.strip() or (cc.stderr.strip().splitlines() or [""])[-1])[:90]
            else:
                cazado_cc, linea = None, ""
            t = subprocess.run([PY, "-B", "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", PRUEBAS], capture_output=True,
                               text=True, cwd=copia, env=entorno, timeout=1800)
            cazado_t = t.returncode != 0
            fallo = next((x for x in t.stdout.splitlines() if x.startswith("FAILED")), "")[:100]
            et_cc = "—     " if cazado_cc is None else ("cazado" if cazado_cc else "VIVO  ")
            print(f"{mid} {str(ficha or 'regla'):16s} CC={et_cc} T={'cazado' if cazado_t else 'VIVO  '} · {desc}"
                  f"{' · ' + linea if linea else ''}{' · ' + fallo if fallo else ''}", flush=True)
            if cazado_cc is False:
                vivos_cc.append(mid)
            if not cazado_cc and not cazado_t:
                vivos.append(f"{mid} ({desc})")
        finally:
            ruta.write_text(original, encoding="utf-8")
    con_cc = sum(1 for m in MUTANTES if m[1] and (not SOLO or m[0] == SOLO))
    print(f"\n{n} mutantes · {con_cc} de fórmula con CC: {con_cc - len(vivos_cc)} cazados por los casos de control"
          f" · vivos frente a CC y T: {len(vivos)}")
    for v in vivos:
        print("  VIVO:", v)
    return 1 if vivos else 0


if __name__ == "__main__":
    sys.exit(main())
