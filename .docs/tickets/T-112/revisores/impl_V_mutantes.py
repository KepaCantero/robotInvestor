"""T-112 · grupo V (implementación) · Mutantes de las fórmulas principales de `motor/fichas_valoracion.py`.

Cada mutante rompe una fórmula de una ficha (signo, exponente, base, término omitido…). Se aplica sobre una COPIA de
`bloque_a` (sin los `.docx`) en un directorio temporal del scratchpad, nunca sobre el árbol principal, y se mira quién lo
caza:
  - CC: los casos de control de la ficha (`CASOS_CONTROL`, dos pasadas que deben coincidir: lo que decide la promoción);
  - T:  `tests/test_fase2_valoracion.py` (sin la prueba de integración con el Motor, que depende de `servicio.py`, en
        obras por la integración).
Antes de mutar se comprueba que la copia sin mutar supera CC y T (línea base); si no, el script se detiene.
Un mutante vivo ante CC y T es una fórmula sin red.

Uso: .venv/bin/python -I -B .docs/tickets/T-112/revisores/impl_V_mutantes.py [--raiz RAIZ] [--destino DIR] [--solo FICHA]
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

MOD = "bloque_a/motor/fichas_valoracion.py"
PRUEBA = "tests/test_fase2_valoracion.py"
EXCLUIR = "not test_los_casos_de_control_pasan_por_el_motor"

MUTANTES = [
    # (id, ficha, [(viejo, nuevo)…], descripción)
    ("V01", "FIR-PRICE-001", [("t = (1 - a) + np.arange(n, dtype=float)", "t = (1 - a / 2) + np.arange(n, dtype=float)")],
     "periodo fraccionario mal calculado"),
    ("V02", "FIR-PRICE-001", [("    d_mod = d_mac * v\n", "    d_mod = d_mac\n")], "D_mod = D_mac"),
    ("V03", "FIR-PRICE-001", [("conv = float(np.sum(t * (t + 1) * pv))", "conv = float(np.sum(t * t * pv))")],
     "convexidad sin el término t + 1"),
    ("V04", "FIR-PRICE-001", [("a = (liq - prev).days / (sig - prev).days", "a = (liq - prev).days / DIAS_POR_ANIO * f")],
     "cupón corrido ACT/365 en vez de ACT/ACT ICMA"),
    ("V05", "FIR-PRICE-001", [("+ (min(d2.day, MES_30E) - min(d1.day, MES_30E)))", "+ (d2.day - d1.day))")],
     "30E/360 sin tope del día 31"),
    ("V06", "FIR-CURVE-001", [("    return _l1(x) - np.exp(-np.asarray(x, dtype=float))",
                               "    return _l1(x) - np.exp(-2 * np.asarray(x, dtype=float))")], "carga de curvatura mal"),
    ("V07", "FIR-CURVE-001", [("out=np.ones_like(x), where=x > 0)", "out=np.zeros_like(x), where=x > 0)")],
     "límite de la carga de pendiente en τ = 0"),
    ("V08", "FIR-CURVE-001", [("f = b[0] + b[1] * np.exp(-x1) + b[2] * x1 * np.exp(-x1)",
                               "f = b[0] + b[1] * np.exp(-x1) + b[2] * np.exp(-x1)")], "forward sin el factor x"),
    ("V09", "FIR-CURVE-001", [('lam_fijo = 1 / (u["lambda_diebold_li_mes"] * MESES_POR_ANIO)',
                               'lam_fijo = u["lambda_diebold_li_mes"] * MESES_POR_ANIO')], "λ de Diebold-Li invertido"),
    ("V10", "FIR-CARRY-001", [("    rolldown = -d_mod * (yr - yt)", "    rolldown = d_mod * (yr - yt)")],
     "rolldown con el signo cambiado"),
    ("V11", "FIR-CARRY-001", [("    d_mod = tau / (1 + yt)\n", "    d_mod = tau\n")], "D_mod = τ (sin 1 + y)"),
    ("V12", "FIR-CARRY-001", [("    carry = (yt - fin_pct / PCT) * dt", "    carry = (yt - fin_pct / PCT)")],
     "carry sin Δt"),
    ("V13", "FIR-SPREAD-001", [("perdida = pd_anual * (1 - rec) * PB_POR_UNIDAD", "perdida = pd_anual * rec * PB_POR_UNIDAD")],
     "pérdida esperada con R en vez de 1 − R"),
    ("V14", "FIR-SPREAD-001", [('"percentil": float(np.mean(h <= valor))', '"percentil": float(np.mean(h < valor))')],
     "percentil con < en vez de ≤"),
    ("V15", "FX-MOM-001", [("carry = float(sum(dif_pct[k - 1] / PCT", "carry = float(sum(dif_pct[k] / PCT")],
     "carry con el diferencial del final del tramo (mira adelante)"),
    ("V16", "FX-MOM-001", [("    var = float(spot[i1] / spot[i0] - 1)", "    var = float(np.log(spot[i1] / spot[i0]))")],
     "variación del spot logarítmica"),
    ("V17", "FX-MOM-001", [("dif_pct[k - 1] / PCT * (fechas[k] - fechas[k - 1]).days / DIAS_POR_ANIO",
                            "dif_pct[k - 1] / PCT * (fechas[k] - fechas[k - 1]).days / BASE_30E")],
     "carry en base 360"),
    ("V18", "FX-PPA-001", [('q = np.log(S) + np.log(ib["valores"]) - np.log(ic["valores"])',
                            'q = np.log(S) - np.log(ib["valores"]) + np.log(ic["valores"])')], "tipo real con índices cruzados"),
    ("V19", "FX-PPA-001", [("vida = math.log(0.5) / math.log(phi) * paso / MESES_POR_ANIO",
                            "vida = math.log(0.5) / math.log(phi) * paso")], "vida media en meses"),
    ("V20", "ACC-ERP-001", [("vt = cf0 * (1 + g5) ** n * (1 + gL) / (r - gL)", "vt = cf0 * (1 + g5) ** n / (r - gL)")],
     "valor terminal sin (1 + g_L)"),
    ("V21", "ACC-ERP-001", [("prm, simple, ecy = r * PCT - rf,", "prm, simple, ecy = r * PCT - rr,")],
     "PRM frente al tipo real"),
    ("V22", "ACC-FACT-001", [("        w = 1 - rez / (rezagos + 1)\n        G = g[rez:]", "        w = 1\n        G = g[rez:]")],
     "Newey-West sin núcleo de Bartlett"),
    ("V23", "ACC-FACT-001", [("    return math.floor(4 * (n / 100) ** (2 / 9))", "    return math.floor(4 * (n / 100) ** (1 / 9))")],
     "regla de rezagos con exponente 1/9"),
    ("V24", "ACC-FACT-001", [('"alfa_anual_pct": ((1 + beta[0] / PCT) ** P - 1) * PCT',
                              '"alfa_anual_pct": beta[0] * P')], "α anualizado aritmético"),
    ("V25", "ACC-FACT-001", [("contrib[\"residuo\"] = float(np.var(e) / vt * PCT)", "contrib[\"residuo\"] = float(np.var(e) / vt)")],
     "contribución del residuo sin pasar a %"),
    ("V26", "ACC-VAL-001", [("vp = [f / (1 + tasa) ** k for k, f in enumerate(flujos, start=1)]",
                             "vp = [f / (1 + tasa) ** (k - 1) for k, f in enumerate(flujos, start=1)]")],
     "descuento un periodo corto"),
    ("V27", "ACC-VAL-001", [("        vt = flujos[-1] * (1 + g_t) / (tasa - g_t)", "        vt = flujos[-1] / (tasa - g_t)")],
     "Gordon sin (1 + g)"),
    ("V28", "ACC-VAL-001", [("wacc = (cap * ke + d_pos * kd * (1 - t)) / (cap + d_pos)", "wacc = (cap * ke + d_pos * kd) / (cap + d_pos)")],
     "WACC sin escudo fiscal"),
    ("V29", "ACC-VAL-001", [('- ult["capex"] - ult["variacion_circulante"]', '- ult["capex"] + ult["variacion_circulante"]')],
     "FCFF suma la variación de circulante"),
    ("V30", "DER-OPT-001", [("return float(K * math.exp(-r * T) * N(-d2) - S * math.exp(-q * T) * N(-d1))",
                             "return float(K * math.exp(-r * T) * N(-d1) - S * math.exp(-q * T) * N(-d1))")], "put con N(−d1)"),
    ("V31", "DER-OPT-001", [("d1 = (math.log(S / K) + (r - q + 0.5 * s * s) * T) / sd",
                             "d1 = (math.log(S / K) + (r + 0.5 * s * s) * T) / sd")], "d1 sin dividendo"),
    ("V32", "DER-OPT-001", [('"vega": float(vega) / PCT,', '"vega": float(vega),')], "vega por unidad, no por punto"),
    ("V33", "DER-OPT-001", [("pr = (math.exp((r - q) * dt) - dn) / (up - dn)", "pr = (math.exp(r * dt) - dn) / (up - dn)")],
     "árbol CRR sin dividendo"),
    ("V34", "DER-OPT-001", [('"theta_dia": float(theta) / DIAS_POR_ANIO,', '"theta_dia": float(theta) / SESIONES_POR_ANIO,')],
     "θ por sesión en vez de por día"),
]

CC = r'''
import copy, json, sys
from bloque_a.motor import fichas_valoracion as V
solo = sys.argv[1] if len(sys.argv) > 1 else None
fallos = []
for f, casos in V.CASOS_CONTROL.items():
    if solo and f != solo:
        continue
    for c in casos:
        v = {}
        for d in c["datos"]:
            v.update(copy.deepcopy(d["valores"]))
        try:
            r1, _ = V.FICHAS[f]["fn"]({"valores": copy.deepcopy(v)}, dict(c["parametros"]))
            r2, _ = V.FICHAS[f]["fn"]({"valores": copy.deepcopy(v)}, dict(c["parametros"]))
            ok = bool(c["comprobar"](r1)) and json.dumps(r1, sort_keys=True) == json.dumps(r2, sort_keys=True)
        except Exception as e:  # noqa: BLE001
            ok = False
        if not ok:
            fallos.append(f"{f}: {c['nombre']}")
print(V.__file__)
print(json.dumps(fallos, ensure_ascii=False))
sys.exit(1 if fallos else 0)
'''


def _copia(raiz: Path, destino: Path) -> Path:
    dst = destino / "bloque_a"
    shutil.copytree(raiz / "bloque_a", dst, ignore=shutil.ignore_patterns("*.docx", "__pycache__", ".pytest_cache"))
    return dst / "11_Ejecutor"


def _correr(ejec: Path, py: str, solo: str | None) -> tuple[bool, bool, str]:
    """(CC superados, T superadas, ruta del módulo importado)."""
    entorno = {**os.environ, "PYTHONPATH": str(ejec), "PYTHONDONTWRITEBYTECODE": "1", "BLOQUE_A_RAIZ": str(ejec.parent)}
    cc = subprocess.run([py, "-B", "-c", CC] + ([solo] if solo else []), cwd=ejec, env=entorno, capture_output=True,
                        text=True, timeout=600, check=False)
    ruta = (cc.stdout.splitlines() or [""])[0]
    t = subprocess.run([py, "-B", "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "--no-header", PRUEBA, "-k", EXCLUIR],
                       cwd=ejec, env=entorno, capture_output=True, text=True, timeout=1200, check=False)
    return cc.returncode == 0, t.returncode == 0, ruta


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", default=str(Path(__file__).resolve().parents[4]))
    ap.add_argument("--destino", default=None, help="directorio de trabajo (por defecto, uno temporal)")
    ap.add_argument("--solo", default=None, help="solo los mutantes de esta ficha")
    a = ap.parse_args()
    raiz = Path(a.raiz).resolve()
    py = str(raiz / ".venv" / "bin" / "python") if (raiz / ".venv" / "bin" / "python").exists() else sys.executable
    base = Path(tempfile.mkdtemp(prefix="impl_V_mutantes_", dir=a.destino))
    try:
        ejec = _copia(raiz, base)
        mod = ejec / MOD
        original = mod.read_text(encoding="utf-8")
        cc, t, ruta = _correr(ejec, py, None)
        if not Path(ruta).resolve().is_relative_to(base.resolve()):
            print(f"ABORTA: se importó {ruta}, no la copia de {base}")
            return 2
        print(f"línea base (copia sin mutar en {base}): CC {'superados' if cc else 'FALLAN'} · T {'superadas' if t else 'FALLAN'}")
        if not (cc and t):
            print("ABORTA: la copia sin mutar no supera CC y T")
            return 2
        vivos = 0
        print(f"{'id':4} {'ficha':15} {'CC':6} {'T':6} descripción")
        for mid, ficha, cambios, desc in MUTANTES:
            if a.solo and ficha != a.solo:
                continue
            texto = original
            for viejo, nuevo in cambios:
                if texto.count(viejo) != 1:
                    print(f"{mid}: el patrón no aparece exactamente una vez: {viejo[:60]!r}")
                    return 3
                texto = texto.replace(viejo, nuevo)
            mod.write_text(texto, encoding="utf-8")
            try:
                cc, t, _ = _correr(ejec, py, ficha)
            finally:
                mod.write_text(original, encoding="utf-8")
            muerto_cc, muerto_t = not cc, not t
            vivos += not (muerto_cc or muerto_t)
            print(f"{mid:4} {ficha:15} {'muere' if muerto_cc else 'VIVE':6} {'muere' if muerto_t else 'VIVE':6} {desc}")
        print(f"mutantes vivos ante CC y T: {vivos}")
        return 1 if vivos else 0
    finally:
        shutil.rmtree(base, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
