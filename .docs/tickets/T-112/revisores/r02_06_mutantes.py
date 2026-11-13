"""QA r02 de T-112 · mutantes nuevos del revisor (ninguno repite los de `impl_*` ni los de `r01_10`).

Apuntan sobre todo a lo que cambió la corrección de la r01 (cotas, parámetros no declarados, configuración, fecha de corte,
semillas, clave de la caché, tolerancias del optimizador) y a algunas fórmulas más. Se aplican sobre una COPIA de
`bloque_a` (sin los `*.docx`) que se indica con --copia; nunca sobre el árbol principal. Para cada mutante:
  - CC: `verificar_casos_control` de la ficha;
  - T:  el fichero de pruebas de su grupo y `tests/test_t112_motor.py` (en `servicio.py`: `test_t112_motor.py`,
        `test_t106_motor.py`, `test_t106_r03.py` y los cuatro `test_fase2_*`), con -x.
Uso: r02_06_mutantes.py --copia <carpeta con bloque_a> [--solo ID]
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
PRUEBAS = {S: ["tests/test_fase2_series.py"], R: ["tests/test_fase2_riesgo.py"], V: ["tests/test_fase2_valoracion.py"],
           P: ["tests/test_fase2_reales.py"],
           X: ["tests/test_t106_motor.py", "tests/test_t106_r03.py", "tests/test_fase2_riesgo.py", "tests/test_fase2_reales.py",
               "tests/test_fase2_valoracion.py", "tests/test_fase2_series.py"]}

MUTANTES = [
    # (id, fichero, ficha para CC, viejo, nuevo, descripción)
    ("ZX01", X, "FIR-CURVE-001", 'base["semilla"], base["perfil"], fecha_corte)', 'base["semilla"], base["perfil"])',
     "la fecha de corte sale de la clave de la caché (H-07 de la r01)"),
    ("ZX02", X, "SIM-MC-001", "dos_semillas = semilla_p is not None and", "dos_semillas = False and",
     "dos semillas distintas ya no se rechazan (H-05)"),
    ("ZX03", X, "DEC-VOI-001", '        ent["configuracion"] = self.cfg\n', '        ent["configuracion"] = None\n',
     "las fichas dejan de recibir la configuración del Motor (H-04)"),
    ("ZX04", X, "ACC-VAL-001", '        ent["fecha_corte"] = fecha_corte\n', '        ent["fecha_corte"] = None\n',
     "las fichas dejan de recibir la fecha de corte (H-07)"),
    ("ZX05", X, "ML-CAL-001", "np.linalg.LinAlgError, MemoryError,\n                RecursionError) as e:", "np.linalg.LinAlgError) as e:",
     "MemoryError y RecursionError vuelven a escapar de servir (H-01)"),
    ("ZX06", X, "SIM-MC-001", '"semilla": params.get("semilla", peticion.get("semilla")), "as_of"', '"semilla": peticion.get("semilla"), "as_of"',
     "el artefacto registra la semilla de la petición y no la usada (H-05)"),
    ("ZX07", X, "BIB-MET-001", "not (isinstance(solicitante, str) and solicitante in SOLICITANTES_FICHA[ficha])",
     "solicitante not in SOLICITANTES_FICHA[ficha]", "solicitante no textual vuelve a lanzar TypeError (H-06)"),
    ("ZR01", R, "DEC-VOI-001", '    cfg = ent.get("configuracion")\n    if cfg is not None and not isinstance(cfg, dict):',
     '    cfg = None\n    if cfg is not None and not isinstance(cfg, dict):', "grupo R ignora la configuración del Motor (H-04)"),
    ("ZR02", R, "SIM-MC-001", '        if p["n_trayectorias"] * p["horizonte"] > presupuesto:', "        if False:",
     "SIM-MC sin presupuesto de trayectorias × pasos (H-01)"),
    ("ZR03", R, "RISK-VAR-001", "_TOL_OPTIMIZADOR = 1e-10", "_TOL_OPTIMIZADOR = 1e-3", "tolerancia del optimizador relajada (H-03)"),
    ("ZR04", R, "RISK-VAR-001", '"es": -mu + s * float(stats.norm.pdf(z)) / a, "media": mu', '"es": -mu + s * float(stats.norm.pdf(z)), "media": mu',
     "ES normal sin dividir por la probabilidad de cola"),
    ("ZR05", R, "ML-CAL-001", '"sesgo": float(np.mean(e))})', '"sesgo": float(np.median(e))})', "sesgo con la mediana"),
    ("ZR06", R, "DEC-VOI-001", "    desconocidos = set(params) - set(PARAMETROS_POR_DEFECTO[ficha]) - {\"clase\"}\n    if desconocidos:",
     "    desconocidos = set(params) - set(PARAMETROS_POR_DEFECTO[ficha]) - {\"clase\"}\n    if False:",
     "grupo R vuelve a ignorar los parámetros no declarados (H-02)"),
    ("ZS01", S, "FX-BRK-001", "    ultima = max(_fecha(f, que) for f in fechas)\n    if ultima > corte:",
     "    ultima = max(_fecha(f, que) for f in fechas)\n    if False:", "grupo S sin el rechazo de datos posteriores al corte"),
    ("ZS02", S, "FX-BRK-001", "    if maximo is not None and len(xs) > maximo:   # la cota se mira antes de convertir (H-01)",
     "    if False:", "grupo S sin la cota de observaciones en `_vector` (H-01)"),
    ("ZS03", S, "ST-INF-001", "acumulado = max(acumulado, min(1.0, (m - j) * pv[i]))", "acumulado = max(acumulado, min(1.0, m * pv[i]))",
     "Holm convertido en Bonferroni"),
    ("ZS04", S, "TEM-DIFF-001", '"B_maximo": 10000', '"B_maximo": 10 ** 12', "TEM-DIFF sin cota efectiva de B (H-01)"),
    ("ZS05", S, "REG-HMM-001", '"arranques_maximos": 50, "obs_maximas": 520', '"arranques_maximos": 10 ** 12, "obs_maximas": 520',
     "REG-HMM sin cota efectiva de arranques (H-01)"),
    ("ZV01", V, "ACC-VAL-001", "    if limite is not None and f > limite:\n        raise ErrorFicha(f\"{que}: dato del {f} posterior",
     "    if False:\n        raise ErrorFicha(f\"{que}: dato del {f} posterior", "grupo V sin el rechazo de datos no conocibles (H-07)"),
    ("ZV02", V, "FIR-CURVE-001", "    if n > maximo:\n        raise ErrorFicha(f\"{que}: {n} elementos (> {maximo}, cota de tamaño de la ficha)\")",
     "    if False:\n        raise ErrorFicha(f\"{que}: {n} elementos (> {maximo}, cota de tamaño de la ficha)\")", "grupo V sin topes de tamaño (H-01)"),
    ("ZV03", V, "ACC-FACT-001", '"alfa_anual_pct": ((1 + beta[0] / PCT) ** P - 1) * PCT,', '"alfa_anual_pct": beta[0] * P,',
     "α anual sin capitalización compuesta"),
    ("ZV04", V, "DER-OPT-001", "    d1 = (math.log(S / K) + (r - q + 0.5 * s * s) * T) / sd", "    d1 = (math.log(S / K) + (r + q + 0.5 * s * s) * T) / sd",
     "BSM: el dividendo suma en d₁"),
    ("ZP01", P, "CHR-FLOW-001", "    posteriores = [f for f in fechas if f > corte]\n    if posteriores:",
     "    posteriores = [f for f in fechas if f > corte]\n    if False:", "grupo P sin el rechazo de datos posteriores al corte (H-07)"),
    ("ZP02", P, "REI-CAP-001", "    desconocidos = set(params) - set(PARAMETROS_POR_DEFECTO[ficha]) - AJENOS\n    if desconocidos:",
     "    desconocidos = set(params) - set(PARAMETROS_POR_DEFECTO[ficha]) - AJENOS\n    if False:",
     "grupo P vuelve a ignorar los parámetros no declarados (H-02)"),
    ("ZP03", P, "CHR-FLOW-001", "        rel = mon / float(pat[n - w - 1])", "        rel = mon / float(pat[n - 1])",
     "% de patrimonio sobre el último y no sobre el previo a la ventana"),
    ("ZP04", P, "CMD-RETDEC-001", "    col_tipo = tipo[:-1] * dias / DIAS_ANIO", "    col_tipo = tipo[1:] * dias / DIAS_ANIO",
     "colateral con el tipo del final del periodo"),
    ("ZP05", P, "REI-CAP-001", "    sd = float(np.std(h, ddof=1)) if float(np.ptp(h)) > 0 else 0.0\n    media = float(np.mean(h))",
     "    sd = float(np.std(h, ddof=0)) if float(np.ptp(h)) > 0 else 0.0\n    media = float(np.mean(h))", "z con desviación poblacional"),
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
        return r.returncode, (r.stdout + r.stderr)[-300:]
    except subprocess.TimeoutExpired:
        return 99, "TIEMPO"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--copia", required=True)
    ap.add_argument("--solo")
    a = ap.parse_args()
    base = Path(a.copia).resolve()
    assert Path(__file__).resolve().parents[4] not in base.parents and (base / MOT).is_dir(), "la copia debe estar fuera del repo"
    eje = base / "11_Ejecutor"
    vivos = []
    for mid, fich, ficha, viejo, nuevo, desc in MUTANTES:
        if a.solo and mid not in a.solo.split(","):
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
            cc, _ = correr([PY, "-I", "-B", "-c", CC.format(eje=str(eje), ficha=ficha)], eje, 900)
            t, salida = correr([PY, "-I", "-B", "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider", "tests/test_t112_motor.py", *PRUEBAS[fich]],
                               eje, 3600)
        finally:
            ruta.write_text(orig, encoding="utf-8")
        estado = ("MUERE-CC" if cc != 0 else "vive-CC") + " " + ("MUERE-T" if t != 0 else "vive-T")
        if t == 0:
            vivos.append(mid)
        print(f"{mid} {estado} ({time.time() - t0:.0f} s) · {ficha} · {desc}", flush=True)
        if t != 0:
            print("     " + " ".join(salida.split())[-170:], flush=True)
    print("VIVOS:", vivos)
    return 1 if vivos else 0


sys.exit(main())
