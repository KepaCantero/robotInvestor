"""T-112 · grupo R (riesgo, simulación, backtest y modelos) · mutantes de la fórmula principal de cada ficha.

Cada mutante rompe una fórmula de `bloque_a/motor/fichas_riesgo.py` (cuantil, escala, signo, embargo, rango…). Se aplica
sobre una COPIA de `bloque_a` (sin los `*.docx`) en el directorio que se indica, nunca sobre el árbol principal, y se mira
quién lo caza:
  - CC: los casos de control de la ficha (lo que decide la promoción en el Catálogo);
  - T:  `tests/test_fase2_riesgo.py` (casos, rechazos, oráculos independientes…).
Un mutante que sobrevive a CC y a T es una fórmula sin red: el script termina con código 1.

Uso (desde la raíz del repo):
  .venv/bin/python -I -B .docs/tickets/T-112/revisores/impl_R_mutantes.py --copia DIR [--desde N] [--hasta N] [--solo M07]
DIR es un directorio vacío (o uno que ya usó este script) fuera del repositorio, p. ej. en el scratchpad.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
PY = str(RAIZ / ".venv" / "bin" / "python") if (RAIZ / ".venv" / "bin" / "python").exists() else sys.executable
MODULO = Path("11_Ejecutor") / "bloque_a" / "motor" / "fichas_riesgo.py"
PRUEBA = "tests/test_fase2_riesgo.py"

MUTANTES = [
    # (id, ficha, [(viejo, nuevo)…], descripción)
    ("M01", "RISK-VAR-001", [('        q = float(np.quantile(r, a))\n        return {"var": -q,',
                              '        q = float(np.quantile(r, a / 2))\n        return {"var": -q,')],
     "histórico con el cuantil de la mitad de la cola"),
    ("M02", "RISK-VAR-001", [('"es": -float(np.mean(r[r <= q])), "cuantil": q}', '"es": -float(np.mean(r[r < q])), "cuantil": q}')],
     "ES histórico sin la observación del cuantil"),
    ("M03", "RISK-VAR-001", [('"es": -mu + s * float(stats.norm.pdf(z)) / a,', '"es": -mu + s * float(stats.norm.pdf(z)) / nivel,')],
     "ES normal dividido por el nivel, no por la cola"),
    ("M04", "RISK-VAR-001", [("        esc = s * math.sqrt((nu - 2) / nu)\n        x = float(stats.t.ppf(a, nu))",
                              "        esc = s\n        x = float(stats.t.ppf(a, nu))")], "t sin reescalar a la varianza"),
    ("M05", "RISK-VAR-001", [("- (2 * x ** 3 - 5 * x) * S * S / 36", "+ (2 * x ** 3 - 5 * x) * S * S / 36")],
     "Cornish-Fisher con el término S² sumado"),
    ("M06", "RISK-VAR-001", [("    escala = math.sqrt(h)\n", "    escala = h\n")], "horizonte por h y no por √h"),
    ("M07", "RISK-VAR-001", [('"es": (var + beta - xi * umbral) / (1 - xi)', '"es": (var + beta) / (1 - xi)')],
     "ES de EVT sin −ξu"),
    ("M08", "RISK-VAR-001", [('sig = math.sqrt(g["sigma2_siguiente"])', "sig = math.sqrt(float(np.var(r)))")],
     "histórico filtrado con la varianza incondicional"),
    ("M09", "SIM-MC-001", [("out[0::2], out[1::2] = z, -z", "out[0::2], out[1::2] = z, z")], "antitéticas iguales, no opuestas"),
    ("M10", "SIM-MC-001", [('h = din["omega"] + din["alpha"] * eps * eps + din["beta"] * h',
                            'h = din["omega"] + din["beta"] * eps * eps + din["alpha"] * h')], "GARCH con α y β cambiados"),
    ("M11", "SIM-MC-001", [('np.sqrt(k) * din["desv_salto"]', 'k * din["desv_salto"]')], "dispersión de saltos con k, no √k"),
    ("M12", "SCN-H-001", [("ra = (np.array(medias) + z * np.array(desv)).sum(axis=1)",
                           "ra = (np.array(medias) + z * np.array(desv)).mean(axis=1)")], "H4 con la media de los bloques"),
    ("M13", "SCN-H-001", [('fav, adv = float(np.quantile(y, u["cuantil_favorable"])), float(np.quantile(y, u["cuantil_adverso"]))',
                           'fav, adv = float(np.quantile(y, u["cuantil_adverso"])), float(np.quantile(y, u["cuantil_favorable"]))')],
     "favorable y adverso cambiados"),
    ("M14", "SCN-H-001", [("            ajuste = math.log1p(aj)\n", "            ajuste = aj\n")],
     "ajuste de valoración sumado en log sin ln(1 + a)"),
    ("M15", "SCN-H-001", [('pasos3 = sesiones_horizonte(None, "H3")', 'pasos3 = sesiones_horizonte(None, "H2")')],
     "H3 simulado con los pasos de H2"),
    ("M16", "BT-DSR-001", [("den = 1 - g3 * sr + (g4 - 1) / 4 * sr * sr", "den = 1 - g3 * sr + (g4 - 3) / 4 * sr * sr")],
     "EE de Mertens con la curtosis en exceso"),
    ("M17", "BT-DSR-001", [(('sr0 = math.sqrt(var_sr_p) * ((1 - g) * float(stats.norm.ppf(1 - 1 / N))\n'
                             '                                     + g * float(stats.norm.ppf(1 - 1 / (N * math.e))))'),
                            ('sr0 = math.sqrt(var_sr_p) * (g * float(stats.norm.ppf(1 - 1 / N))\n'
                             '                                     + (1 - g) * float(stats.norm.ppf(1 - 1 / (N * math.e))))'))],
     "SR*₀ con los pesos de γ cambiados"),
    ("M18", "BT-DSR-001", [("ee = math.sqrt(den / (T - 1))", "ee = math.sqrt(den / T)")], "EE con T y no T − 1"),
    ("M19", "BT-DSR-001", [('sr_ref = p["SR_referencia"] / math.sqrt(q)', 'sr_ref = p["SR_referencia"] / q')],
     "referencia anual pasada a periodo con q y no √q"),
    ("M20", "BT-DSR-001", [("return q / math.sqrt(q + 2 * suma)", "return q / math.sqrt(q + suma)")], "Lo sin el factor 2"),
    ("M21", "BT-PBO-001", [("w = rangos[fila, mejor] / (N + 1)", "w = rangos[fila, mejor] / N")], "ω = rango/N"),
    ("M22", "BT-PBO-001", [("mejor = np.argmax(dentro, axis=1)", "mejor = np.argmax(fuera, axis=1)")],
     "mejor configuración elegida fuera de muestra"),
    ("M23", "BT-PBO-001", [("pbo = float(np.mean(lam <= 0))", "pbo = float(np.mean(lam < 0))")], "PBO con λ < 0"),
    ("M24", "BT-PBO-001", [("fuera = sharpe(s1.sum(axis=0) - is1, s2.sum(axis=0) - is2)", "fuera = sharpe(is1, is2)")],
     "fuera de muestra = dentro"),
    ("M25", "BT-VAR-001", [("    l1 = special.xlogy(T - x, 1 - f) + special.xlogy(x, f)",
                            "    l1 = special.xlogy(T - x, 1 - p) + special.xlogy(x, p)")], "Kupiec sin la proporción observada"),
    ("M26", "BT-VAR-001", [("    exc = res < -var_p\n", "    exc = res < var_p\n")], "excedencia contra +VaR"),
    ("M27", "BT-VAR-001", [("l1 = (special.xlogy(n00, 1 - pi01) + special.xlogy(n01, pi01) + special.xlogy(n10, 1 - pi11)",
                            "l1 = (special.xlogy(n00, 1 - pi11) + special.xlogy(n01, pi11) + special.xlogy(n10, 1 - pi01)")],
     "Christoffersen con π₀₁ y π₁₁ cambiadas"),
    ("M28", "BT-VAR-001", [("z2 = float(np.sum(res * exc / (T * p * es_p)) + 1)", "z2 = float(np.sum(res * exc / (T * p * es_p)) - 1)")],
     "Z₂ con −1"),
    ("M29", "BT-VAR-001", [('zona = "verde" if x250 <= u["verde_max"]', 'zona = "verde" if x250 < u["verde_max"]')],
     "zona verde con < 4"),
    ("M30", "ML-CAL-001", [('"rmse": float(math.sqrt(np.mean(e * e)))', '"rmse": float(np.mean(e * e))')], "RMSE sin raíz"),
    ("M31", "ML-CAL-001", [("esc = float(np.mean(np.abs(np.diff(y))))", "esc = float(np.mean(np.abs(y)))")],
     "MASE escalado con |y|"),
    ("M32", "ML-CAL-001", [("ref[1:] = y[:-1] if tipo == \"nivel\" else np.cumsum(y)[:-1] / np.arange(1, n)",
                            "ref[1:] = y[:-1] if tipo == \"nivel\" else np.cumsum(y)[1:] / np.arange(2, n + 1)")],
     "RI-TB con la realización del propio periodo (anticipación)"),
    ("M33", "ML-CAL-001", [("perd = np.maximum(cuantil * e, (cuantil - 1) * e)", "perd = np.maximum(cuantil * e, (1 - cuantil) * e)")],
     "pinball con el signo de la rama inferior cambiado"),
    ("M34", "ML-CAL-001", [("    a = (1 - nivel) / 2\n    ic = [", "    a = 1 - nivel\n    ic = [")], "IC con toda la cola en cada lado"),
    ("M35", "ML-PRED-001", [("fin = a - emb                                   #", "fin = a - 1                                     #")],
     "entrenamiento hasta la víspera de la prueba (sin embargo)"),
    ("M36", "ML-PRED-001", [("ref = np.array([acum[t - emb + 1] / (t - emb + 1) for t in idx])",
                             "ref = np.array([acum[t + 1] / (t + 1) for t in idx])")], "RI-TB con etiquetas aún no conocidas"),
    ("M37", "ML-PRED-001", [("mu, sd = X.mean(axis=0), X.std(axis=0, ddof=1)", "mu, sd = Xn.mean(axis=0), Xn.std(axis=0, ddof=1)")],
     "estandarización con la ventana de prueba"),
    ("M38", "ML-PRED-001", [("    pen = np.full(Z.shape[1], lam)\n    pen[0] = 0.0\n    previo",
                             "    pen = np.full(Z.shape[1], lam)\n    previo")], "logística que penaliza el intercepto"),
    ("M39", "DEC-VOI-001", [("e_max = ((hi - c) * ((hi + c) / 2 - u)) / (hi - lo)", "e_max = ((hi - c) * ((hi + c) / 2 - u)) / (hi - lo) / 2")],
     "EVPI uniforme a la mitad"),
    ("M40", "DEC-VOI-001", [("(s - u) * float(stats.norm.cdf((s - x_corte) / sigma))", "(s - u) * float(stats.norm.cdf((x_corte - s) / sigma))")],
     "EVSI con la regla de Bayes invertida"),
    ("M41", "DEC-VOI-001", [('alcanza = pri["hi"] >= u - banda and pri["lo"] <= u + banda', 'alcanza = pri["hi"] >= u and pri["lo"] <= u')],
     "regla simple sin la banda marginal"),
    ("M42", "DEC-VOI-001", [("    return e_max - max(pri[\"media\"] - u, 0.0)\n", "    return e_max\n")],
     "EVPI sin restar el valor de decidir sin información"),
    ("M43", "DEC-VOI-001", [("return float(x + sigma * (stats.norm.pdf(a) - stats.norm.pdf(b)) / masa)",
                             "return float(x + sigma * (stats.norm.pdf(b) - stats.norm.pdf(a)) / masa)")],
     "media posterior truncada con el signo cambiado"),
]

CORRER_CASOS = """
import sys, copy
import bloque_a
assert bloque_a.__file__.startswith(sys.argv[1]), bloque_a.__file__
from bloque_a.motor import fichas_riesgo as R
ficha = sys.argv[2]
for c in R.CASOS_CONTROL[ficha]:
    v = {}
    for d in c["datos"]:
        v.update(copy.deepcopy(d["valores"]))
    try:
        r1, _ = R.FICHAS[ficha]["fn"]({"valores": v, "series": {}, "series_rol": {}}, dict(c["parametros"]))
        r2, _ = R.FICHAS[ficha]["fn"]({"valores": copy.deepcopy(v), "series": {}, "series_rol": {}}, dict(c["parametros"]))
        ok = bool(c["comprobar"](r1)) and r1 == r2
    except Exception as e:  # noqa: BLE001 — un caso que revienta no se supera
        ok = False
    if not ok:
        print("CAZADO", c["nombre"])
        sys.exit(0)
print("SOBREVIVE")
"""


MARCA = ".copia_impl_R"


def preparar_copia(destino: Path) -> Path:
    """Copia limpia de `bloque_a` (sin `*.docx`) en un directorio propio: se rehace en cada ejecución para no arrastrar
    una copia vieja ni cambios de otra sesión. Solo se borra un directorio que este script marcó como suyo."""
    if destino.exists() and any(destino.iterdir()) and not (destino / MARCA).exists():
        raise SystemExit(f"{destino} no es una copia de este script (falta {MARCA}): elija un directorio vacío")
    copia = destino / "bloque_a"
    if copia.exists():
        shutil.rmtree(copia)
    shutil.copytree(RAIZ / "bloque_a", copia, ignore=shutil.ignore_patterns("*.docx", "__pycache__", ".pytest_cache"))
    (destino / MARCA).write_text("copia de trabajo de impl_R_mutantes.py\n", encoding="utf-8")
    return copia


def correr(copia: Path, ficha: str) -> tuple[bool, bool, str]:
    ejec = copia / "11_Ejecutor"
    entorno = {**os.environ, "PYTHONPATH": str(ejec), "PYTHONDONTWRITEBYTECODE": "1"}
    cc = subprocess.run([PY, "-c", CORRER_CASOS, str(ejec), ficha], cwd=ejec, env=entorno, capture_output=True,
                        text=True, timeout=600, check=False)
    cazado_cc = cc.stdout.strip().startswith("CAZADO")
    if cc.returncode != 0:
        return True, True, f"el módulo mutado no importa: {cc.stderr.strip().splitlines()[-1][:120]}"
    t = subprocess.run([PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", PRUEBA], cwd=ejec, env=entorno,
                       capture_output=True, text=True, timeout=900, check=False)
    fallo = next((x for x in t.stdout.splitlines() if x.startswith("FAILED")), "")
    return cazado_cc, t.returncode != 0, (cc.stdout.strip()[:110] + " | " + fallo[:110]).strip(" |")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--copia", required=True, help="directorio de trabajo (scratchpad) donde vive la copia de bloque_a")
    ap.add_argument("--desde", type=int, default=1)
    ap.add_argument("--hasta", type=int, default=len(MUTANTES))
    ap.add_argument("--solo")
    a = ap.parse_args()
    destino = Path(a.copia).resolve()
    if RAIZ in destino.parents or destino == RAIZ:
        print("la copia no puede estar dentro del repositorio")
        return 2
    destino.mkdir(parents=True, exist_ok=True)
    copia = preparar_copia(destino)
    ruta = copia / MODULO
    original = ruta.read_text(encoding="utf-8")
    sel = [m for i, m in enumerate(MUTANTES, 1) if a.desde <= i <= a.hasta and (not a.solo or m[0] == a.solo)]
    vivos, sin_aplicar = [], []
    try:
        for mid, ficha, cambios, desc in sel:
            texto = original
            for viejo, nuevo in cambios:
                if texto.count(viejo) != 1:
                    sin_aplicar.append(mid)
                    break
                texto = texto.replace(viejo, nuevo)
            else:
                ruta.write_text(texto, encoding="utf-8")
                cc, t, det = correr(copia, ficha)
                marca = "CC+T" if cc and t else "CC" if cc else "T" if t else "VIVO"
                print(f"{mid} {ficha:13} {marca:5} {desc} · {det}", flush=True)
                if not (cc or t):
                    vivos.append(mid)
                continue
            print(f"{mid} {ficha:13} NO APLICA {desc}", flush=True)
    finally:
        ruta.write_text(original, encoding="utf-8")
    print(f"\n{len(sel)} mutantes · vivos: {vivos or 'ninguno'} · sin aplicar: {sin_aplicar or 'ninguno'}")
    return 1 if vivos or sin_aplicar else 0


if __name__ == "__main__":
    sys.exit(main())
