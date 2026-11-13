"""QA r01 de T-112 · mutantes nuevos del revisor sobre los cuatro módulos y `servicio.py`.

Ninguno repite los de `impl_*_mutantes.py`. Se aplican sobre una COPIA de `bloque_a` (sin los `*.docx`) que se indica con
--copia; nunca sobre el árbol principal. Para cada mutante:
  - CC: `verificar_casos_control` de la ficha (lo que decide la promoción);
  - T:  el fichero de pruebas de su grupo y `tests/test_t112_motor.py` (con -x);
  - TODO: solo para los que sobreviven a T, la suite completa de A (con -x), si se pasa --todo.
Uso: r01_10_mutantes.py --copia <carpeta con bloque_a> [--solo ID] [--todo]
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

PY = str(Path(__file__).resolve().parents[4] / ".venv" / "bin" / "python")
MOT = Path("11_Ejecutor/bloque_a/motor")
S, R, V, P, X = (MOT / "fichas_series.py", MOT / "fichas_riesgo.py", MOT / "fichas_valoracion.py", MOT / "fichas_reales.py",
                 MOT / "servicio.py")
PRUEBAS = {S: "tests/test_fase2_series.py", R: "tests/test_fase2_riesgo.py", V: "tests/test_fase2_valoracion.py",
           P: "tests/test_fase2_reales.py", X: "tests/test_t106_motor.py"}

MUTANTES = [
    # (id, fichero, ficha para CC, viejo, nuevo, descripción)
    ("QS01", S, "FX-REGIME-001", 'bic = -2 * aj["loglik"] + n_par * math.log(n)', 'bic = -2 * aj["loglik"] + 2 * n_par', "AIC en lugar de BIC"),
    ("QS02", S, "FX-REGIME-001", "n_par = (k - 1) + k * (k - 1) + ", "n_par = k * (k - 1) + ", "BIC sin los k − 1 parámetros iniciales"),
    ("QS03", S, "FX-REGIME-001", "loglik = loglik + s[:, -1] + np.log(sa[:, -1])", "loglik = loglik + s[:, -1]",
     "log-verosimilitud sin el último factor de normalización"),
    ("QS04", S, "FX-COINT-001", "return math.floor(4 * (T / 100) ** (2 / 9))", "return math.floor(12 * (T / 100) ** (1 / 4))",
     "regla de rezagos de Schwert en lugar de la de ACC-FACT-001"),
    ("QS05", S, "FX-COINT-001", "aic[p_] = len(yy) * math.log(max(float(e @ e), EPS) / len(yy)) + 2 * X.shape[1]",
     "aic[p_] = len(yy) * math.log(max(float(e @ e), EPS) / len(yy)) + math.log(len(yy)) * X.shape[1]", "ADF por BIC"),
    ("QS06", S, "FX-COINT-001", "1: (12.7676, 9.1645, 7.5567)", "1: (12.7676, 9.2445, 7.5567)", "valor crítico de la traza al 5 % alterado"),
    ("QS07", S, "REG-HMM-001", "k = min(bics, key=lambda x: (bics[x], x))", "k = max(bics, key=lambda x: (bics[x], x))",
     "BIC: el peor número de estados"),
    ("QS08", S, "ST-INF-001", "acumulado = min(acumulado, m * pv[i] / (j + 1))", "acumulado = min(1.0, m * pv[i] / (j + 1))",
     "BH sin la monotonía (mínimo sobre j ≥ i)"),
    ("QR01", R, "BT-DSR-001", "sr0 = math.sqrt(var_sr_p) * ((1 - g) * float(stats.norm.ppf(1 - 1 / N))",
     "sr0 = math.sqrt(var_sr_p) * (g * float(stats.norm.ppf(1 - 1 / N))", "SR*₀ con γ en lugar de 1 − γ en el primer término"),
    ("QR02", R, "BT-VAR-001", 'x250 = int(exc[-u["dias_semaforo"]:].sum())', 'x250 = int(exc[:u["dias_semaforo"]].sum())',
     "semáforo con las primeras 250 y no las últimas"),
    ("QR03", R, "RISK-VAR-001", "ratio = n / nu_ * a", "ratio = nu_ / n * a", "EVT-POT con el cociente de excedencias invertido"),
    ("QR04", R, "RISK-VAR-001", "    om = var * (1 - al - be)\n", "    om = var * (1 - al)\n", "GARCH: ω sin el objetivo de varianza"),
    ("QR05", R, "BT-PBO-001", "lam = np.log(w / (1 - w))", "lam = np.log(w)", "λ sin logit (PBO igual, λ publicado distinto)"),
    ("QR06", R, "BT-DSR-001", "ee = math.sqrt(den / (T - 1))", "ee = math.sqrt(den / T)", "EE del Sharpe con T y no T − 1"),
    ("QV01", V, "DER-OPT-001", "    return {k: (a[k] + b[k]) / 2 for k in a if k in b}", "    return {k: a[k] for k in a if k in b}",
     "CRR sin el promedio N/N + 1"),
    ("QV02", V, "DER-OPT-001", "    if black:\n        rho = -T * bsm(S, K, T, r, q, s, call)\n", "", "ρ de Black-76 como si fuera BSM"),
    ("QV03", V, "DER-OPT-001", "lado_c, lado_p = K >= Fw, K <= Fw", "lado_c, lado_p = K <= Fw, K >= Fw", "lados de la sonrisa cambiados en RR25"),
    ("QV04", V, "FIR-PRICE-001", '"dv01": d_mod * P / PB_POR_UNIDAD}', '"dv01": d_mac * P / PB_POR_UNIDAD}', "DV01 con D_mac"),
    ("QV05", V, "FIR-CURVE-001", '"3m10y": [0.25, 10]', '"3m10y": [0.5, 10]', "pendiente 3m10y con el 6m"),
    ("QV06", V, "ACC-VAL-001", '"sensibilidad_g_pp": 0.5', '"sensibilidad_g_pp": 0.25', "sensibilidad de g ±0,25 pp"),
    ("QP01", P, "REI-NAV-001", "dispersion = math.sqrt(float(np.sum(w * (primas - prima_agg) ** 2)))",
     "dispersion = float(np.std(primas, ddof=1))", "dispersión sin ponderar"),
    ("QP02", P, "ALT-DESMOOTH-001", "riqueza = np.concatenate([[1.0], np.cumprod(1 + r)])", "riqueza = np.cumprod(1 + r)",
     "MDD sin el punto de partida"),
    ("QP03", P, "ALT-DESMOOTH-001", "bd = _dimson(pd.Series(r, index=fechas), merc, k)", "bd = _dimson(pd.Series(r, index=fechas), merc, k - 1)",
     "beta de Dimson desuavizada con un rezago menos"),
    ("QP04", P, "CHR-FUND-001", "- 1) * DIAS_ANIO / dias,", "- 1) * 360 / dias,", "base anualizada con 360"),
    ("QX01", X, "BIB-MET-001", "        if ficha in SOLICITANTES_FICHA and solicitante not in SOLICITANTES_FICHA[ficha]:",
     "        if False and ficha in SOLICITANTES_FICHA and solicitante not in SOLICITANTES_FICHA[ficha]:", "BIB-MET-001 sin restricción de solicitantes"),
    ("QX02", X, "SIM-MC-001", "        if ficha in ACEPTA_SEMILLA and peticion.get(\"semilla\") is not None:",
     "        if False and ficha in ACEPTA_SEMILLA and peticion.get(\"semilla\") is not None:", "la semilla de la petición no llega a la ficha"),
    ("QX03", X, "AUD-REX-001", "                huellas_en_linea.append(clave_hash(d[\"valor\"])[:16] == d.get(\"huella\"))",
     "                huellas_en_linea.append(True)", "CT-10 sin comprobar la huella de los valores en línea"),
    ("QX04", X, "AUD-REX-001", "coincide, categoria = \"NO\", (\"ERROR_ORIGINAL\" if version else \"CONVENCION_DISTINTA\")",
     "coincide, categoria = \"NO\", (\"CONVENCION_DISTINTA\" if version else \"ERROR_ORIGINAL\")", "CT-10: ERROR_ORIGINAL y CONVENCION_DISTINTA cambiadas"),
    ("QX05", X, "AUD-REX-001", "            res = self._casos_aud_rex() if ficha in SERVICIOS_CT10 else []", "            res = []",
     "AUD-REX-001 sin casos de control (¿se da por superada?)"),
    ("QX06", X, "IDX-CONC-001", "ESTRICTAS = FASE1 | FASE2", "ESTRICTAS = FASE1", "el Motor deja de rechazar no finitos en la Fase 2"),
    ("QX07", X, "AUD-REX-001", "        if nuevo != nuevo2:\n            coincide, categoria = \"NO\", \"NO_DETERMINISMO\"\n",
     "        if False:\n            coincide, categoria = \"NO\", \"NO_DETERMINISMO\"\n", "CT-10 sin la doble pasada"),
    ("QX08", X, "AUD-REX-001", "        nuevo, _ = IMPLEMENTADAS[ficha][\"fn\"](copy.deepcopy(ent), copy.deepcopy(orig[\"parametros\"]))",
     "        nuevo, _ = IMPLEMENTADAS[ficha][\"fn\"](copy.deepcopy(ent), {})", "CT-10 sin los parámetros del artefacto"),
]

CC = """
import sys; sys.path.insert(0, {eje!r})
from pathlib import Path; import tempfile
from bloque_a.almacen import Almacen
from bloque_a.configuracion import cargar_config
from bloque_a.motor import servicio
class P: as_of = None; nombre = "qa"
m = servicio.Motor(Almacen(Path(tempfile.mkdtemp())), P(), cargar_config())
v = m.verificar_casos_control([{ficha!r}])[{ficha!r}]
print("CC", v.get("superados"), len(v.get("casos") or []))
sys.exit(0 if v.get("superados") and v.get("casos") else 1)
"""


def correr(cmd, cwd, limite):
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=limite)
        return r.returncode, (r.stdout + r.stderr)[-400:]
    except subprocess.TimeoutExpired:
        return 99, "TIEMPO"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--copia", required=True)
    ap.add_argument("--solo")
    ap.add_argument("--todo", action="store_true")
    a = ap.parse_args()
    base = Path(a.copia).resolve()
    eje = base / "11_Ejecutor"
    vivos = []
    for mid, fich, ficha, viejo, nuevo, desc in MUTANTES:
        if a.solo and mid != a.solo:
            continue
        ruta = base / fich
        orig = ruta.read_text(encoding="utf-8")
        n = orig.count(viejo)
        if n != 1:
            print(f"{mid} NO APLICA ({n} apariciones): {desc}", flush=True)
            continue
        ruta.write_text(orig.replace(viejo, nuevo), encoding="utf-8")
        t0 = time.time()
        try:
            cc, salida_cc = correr([PY, "-I", "-B", "-c", CC.format(eje=str(eje), ficha=ficha)], eje, 900)
            pruebas = [PRUEBAS[fich], "tests/test_t112_motor.py"] if fich != X else ["tests/test_t112_motor.py", "tests/test_t106_motor.py",
                                                                                     "tests/test_t106_r03.py"]
            t, salida_t = correr([PY, "-I", "-B", "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider", *pruebas], eje, 2400)
            todo = None
            if t == 0 and a.todo:
                todo, _ = correr([PY, "-I", "-B", "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider", "tests"], eje, 3600)
        finally:
            ruta.write_text(orig, encoding="utf-8")
        estado = ("MUERE-CC" if cc != 0 else "vive-CC") + " " + ("MUERE-T" if t != 0 else "vive-T") + \
                 ("" if todo is None else (" MUERE-TODO" if todo != 0 else " vive-TODO"))
        if t == 0 and (todo is None or todo == 0):
            vivos.append(mid)
        print(f"{mid} {estado} ({time.time() - t0:.0f} s) · {ficha} · {desc}", flush=True)
        if cc == 99 or t == 99:
            print("   tiempo agotado", flush=True)
    print("VIVOS:", vivos)
    return 1 if vivos else 0


sys.exit(main())
