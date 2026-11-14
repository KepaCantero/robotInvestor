"""QA r01 de T-118 · H-12: ¿siguen las cotas a la configuración del Motor? ¿Queda algún número de la configuración a mano?

 1. Las 56 fichas con caso de control, servidas por dos Motores: configuración por defecto y una con H5 de 10 sesiones,
    una sesión por semana y por mes: la ficha cuya cota sigue a la configuración rechaza (y cita la cota nueva); la que
    no, sirve igual. Se compara con lo que el código declara.
 2. Bordes por el Motor con H5 en 60 meses (1 260), `senales.ventana_anios` 1 (252) y 4 sesiones por semana.
 3. Literales: números de `config/por_defecto.yaml` (horizontes, calendario, senales, evaluacion, umbrales de HT-03) que
    aparecen escritos en los cuatro módulos fuera de los casos de control y de los comentarios.
Uso: .venv/bin/python -I r01_04_h12_configuracion.py
"""
import ast
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

EJE = C.preparar(sys.argv)
import numpy as np  # noqa: E402
from bloque_a.motor import fichas_reales as P  # noqa: E402
from bloque_a.motor import fichas_riesgo as R  # noqa: E402
from bloque_a.motor import fichas_series as S  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402

K = C.Contador("r01_04 H-12")

# ------------------------------------------------------------------ 1
print("[1] qué fichas siguen a la configuración (H5 = 10 sesiones; 1 sesión por semana y por mes; ventana de señales 1 año)")
m0 = C.motor()
m1 = C.motor(None, horizontes={"H5": {"sesiones": 10}}, calendario={"sesiones_por_semana": 1, "sesiones_por_mes": 1},
             senales={"ventana_anios": 1})
fichas = sorted(f for f in servicio.CASOS_CONTROL if servicio.servible(f))
siguen, detalle = set(), {}
for f in fichas:
    for i in range(len(servicio.CASOS_CONTROL[f])):
        r0, e0, _ = C.servir_contando(m0, C.peticion(f, i))
        r1, e1, _ = C.servir_contando(m1, C.peticion(f, i))
        if e0 or e1:
            K.comprobar(f"{f} caso {i} sin excepción", False, str(e0 or e1)[:150])
            continue
        if str(r0["estado"]).startswith("SERVED") and (r1["estado"] == "RECHAZADO" or r1.get("resultado") != r0.get("resultado")):
            siguen.add(f)
            detalle.setdefault(f, r1.get("detalle", "otra cifra")[:120])
for f in sorted(siguen):
    print(f"    {f}: {detalle[f]}")
declaradas = set(S.FICHAS_OBS_H5) | {"FX-REGIME-001"} | {f for f in R.FICHAS if "observaciones_maximas" in R.UMBRALES[f]} | {"DEC-VOI-001"}
print(f"    declaradas en el código como dependientes de la configuración: {sorted(declaradas)}")
print(f"    declaradas que no cambian con esta configuración (sus casos no llegan a la cota): {sorted(declaradas - siguen)}")
print(f"    cambian sin estar declaradas: {sorted(siguen - declaradas)}")

# ------------------------------------------------------------------ 2
print("\n[2] bordes por el Motor con otra configuración")
mc = C.motor(None, horizontes={"H5": {"meses": 60}}, senales={"ventana_anios": 1}, calendario={"sesiones_por_semana": 4})
# con 4 sesiones por semana y 21 por mes, H5 = 60 × 21 = 1 260
rng = np.random.default_rng(3)


def serie_brk(n):
    return [float(x) for x in np.where(np.arange(n) < n // 2, 0.0, 3.0) + np.sin(np.arange(n) * 1.7)]


def est(r, exc):
    return f"EXCEPCION {exc}" if exc else (r["estado"] if r["estado"] != "RECHAZADO" else "RECHAZADO: " + r["detalle"][:110])


casos = [
    ("FX-BRK-001", lambda n: {"serie": serie_brk(n)}, {}, 1260),
    ("FX-STL-001", lambda n: {"serie": [float(10 + np.sin(i * 2 * np.pi / 12) + 0.01 * i + 0.1 * rng.standard_normal()) for i in range(n)],
                              "periodo": 12}, {}, 1260),
    ("FX-COINT-001", lambda n: (lambda a: {"series": {"a": [float(x) for x in a],
                                                      "b": [float(x) for x in a + rng.standard_normal(n)]}})(np.cumsum(rng.standard_normal(n))), {}, 1260),
    ("ST-INF-001", lambda n: {"contrastes": [{"nombre": "c", "muestra": [float(x) for x in rng.standard_normal(n)], "mu0": 0.0}]},
     {"tipo_contraste": "t_una_muestra"}, 1260),
    ("FX-REGIME-001", lambda n: {"serie": [float(x) for x in rng.normal(0, 1, n) * np.where((np.arange(n) // 60) % 2, 1, 3)]}, {}, 252),
    ("RISK-VAR-001", lambda n: {"rendimientos": [float(x) for x in 0.01 * rng.standard_normal(n)]}, {}, 1260),
    ("BT-DSR-001", lambda n: {"rendimientos": [float(x) for x in 0.01 * rng.standard_normal(n)],
                              "varianza_sr_ensayos": {"valor": 0.5, "unidad": "anual"}}, {"N": 10}, 1260),
    ("BT-VAR-001", lambda n: {"var_previsto": [0.02] * n, "resultados": [float(x) for x in 0.01 * rng.standard_normal(n)]}, {}, 1260),
]
for f, datos, params, cota in casos:
    for n, esperado in ((cota, "no por la cota"), (cota + 1, "rechazo por la cota")):
        try:
            v = datos(n)
        except Exception as e:  # noqa: BLE001
            print(f"    {f}: no sé construir el caso ({e})")
            continue
        r, exc, k = C.servir_contando(mc, {"operacion": f, "datos": [{"valores": v}], "parametros": dict(params)})
        e = est(r, exc)
        por_cota = e.startswith("RECHAZADO") and str(cota) in e and ("máximo" in e or "cota" in e or ">" in e)
        print(f"    {f} con {n}: {e[:150]}")
        K.comprobar(f"{f} con {n} observaciones y la cota en {cota}: {esperado}", (por_cota if n > cota else not por_cota) and not exc and k == 1, e)
# CHR-FLOW-001: ventanas hasta 8 semanas × 4 sesiones = 32
for vent, ok in ((32, True), (33, False)):
    pet = C.peticion("CHR-FLOW-001")
    pet["parametros"]["ventanas"] = [vent]
    r, exc, k = C.servir_contando(mc, pet)
    e = est(r, exc)
    print(f"    CHR-FLOW-001 ventanas [{vent}] con 4 sesiones por semana: {e[:140]}")
    K.comprobar(f"CHR-FLOW-001 ventana de {vent} sesiones con 4 por semana: {'no se rechaza por el tope' if ok else 'se rechaza'}",
                (("ventanas" not in e) if ok else ("ventanas" in e and e.startswith("RECHAZADO"))) and not exc, e)
# REG-HMM-001: su cota (520) se declara como «H5, 120 meses, en semanas»: ¿sigue a horizontes.H5?
x = rng.standard_normal((300, 1))
r, exc, _ = C.servir_contando(mc, {"operacion": "REG-HMM-001", "datos": [{"valores": C.valores("REG-HMM-001")}],
                                   "parametros": dict(servicio.CASOS_CONTROL["REG-HMM-001"][0].get("parametros") or {})})
n_hmm = max((len(v) for v in C.valores("REG-HMM-001").values() if isinstance(v, list)), default=None)
print(f"    REG-HMM-001 (caso de control, con H5 en 60 meses = 260 semanas): {est(r, exc)[:120]}; cota en el código: "
      f"{S._obs_maximas('REG-HMM-001', mc.cfg)} (con la configuración por defecto: {S._obs_maximas('REG-HMM-001', None)})")
K.comprobar("REG-HMM-001: la cota «H5, 120 meses, en semanas» (520) sigue a `horizontes.H5` de la configuración del Motor",
            S._obs_maximas("REG-HMM-001", mc.cfg) != S._obs_maximas("REG-HMM-001", None),
            "520 con H5 en 120 meses y 520 con H5 en 60 meses: el número está escrito en UMBRALES")
# configuración mal formada: falla cerrado, sin excepción
for nombre, extra in (("H5 con texto", {"horizontes": {"H5": {"meses": "ciento veinte"}}}), ("H5 negativo", {"horizontes": {"H5": {"meses": -1}}}),
                      ("H5 cero", {"horizontes": {"H5": {"sesiones": 0}}}), ("sesiones por semana 0", {"calendario": {"sesiones_por_semana": 0}}),
                      ("ventana_anios 0", {"senales": {"ventana_anios": 0}}), ("ventana_anios 1.5", {"senales": {"ventana_anios": 1.5}}),
                      ("H5 inmenso", {"horizontes": {"H5": {"meses": 10 ** 12}}})):
    try:
        mm = C.motor(None, **extra)
    except Exception as e:  # noqa: BLE001
        print(f"    {nombre}: el Motor no arranca ({type(e).__name__})")
        continue
    for f in ("FX-BRK-001", "FX-REGIME-001", "RISK-VAR-001", "CHR-FLOW-001"):
        r, exc, k = C.servir_contando(mm, C.peticion(f))
        K.comprobar(f"configuración «{nombre}» · {f}: sin excepción y una entrada en RC", exc is None and k == 1, f"{type(exc).__name__ if exc else ''} {exc}")
        if nombre in ("H5 con texto", "H5 negativo", "H5 cero") and f in ("FX-BRK-001", "RISK-VAR-001") or \
                nombre.startswith("ventana_anios") and f == "FX-REGIME-001" or nombre.startswith("sesiones por semana") and f == "CHR-FLOW-001":
            print(f"      {f}: {est(r, exc)[:130]}")

# ------------------------------------------------------------------ 3
print("\n[3] literales que coinciden con números de la configuración, fuera de comentarios, casos de control y pruebas")
SOSPECHOSOS = {2520: "H5 en sesiones", 756: "senales.ventana_anios × 252", 520: "H5 en semanas", 126: "H3 en sesiones",
               504: "H5 en semanas hábiles", 21: "calendario.sesiones_por_mes", 2000: "evaluacion.bootstrap_replicas",
               120: "horizontes.H5 (meses)"}
for mod in ("servicio.py", "fichas_riesgo.py", "fichas_series.py", "fichas_reales.py"):
    ruta = EJE / "bloque_a" / "motor" / mod
    arbol = ast.parse(ruta.read_text(encoding="utf-8"))
    lineas = ruta.read_text(encoding="utf-8").splitlines()
    hallados = []
    # se excluyen las funciones y asignaciones de casos de control (nombres con _caso, CASOS, _datos_, _R_, _control)
    excluidas = set()
    for nodo in ast.walk(arbol):
        nombre = getattr(nodo, "name", None) or (nodo.targets[0].id if isinstance(nodo, ast.Assign) and isinstance(nodo.targets[0], ast.Name) else None)
        if nombre and any(t in nombre for t in ("caso", "CASO", "_control", "_ctrl", "_R_", "_S_", "_P_", "_DSR", "_PBO", "_datos", "_serie_", "_ejemplo", "_sint",
                                                "_verifica", "_comprueba", "_oraculo", "_esperad", "_genera", "_pred_", "_cal_", "_var_", "_mc_", "_voi", "_scn")):
            excluidas.update(range(nodo.lineno, getattr(nodo, "end_lineno", nodo.lineno) + 1))
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Constant) and type(nodo.value) in (int, float) and nodo.value in SOSPECHOSOS and nodo.lineno not in excluidas:
            hallados.append((nodo.lineno, nodo.value))
    print(f"    {mod}: {len(hallados)}")
    for ln, v in sorted(set(hallados))[:25]:
        print(f"       línea {ln} · {v} ({SOSPECHOSOS[v]}): {lineas[ln - 1].strip()[:150]}")

sys.exit(K.fin())
