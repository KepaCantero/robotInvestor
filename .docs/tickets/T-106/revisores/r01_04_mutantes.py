"""QA r01 de T-106 · Mutantes propios del revisor en las fórmulas de las fichas V5.0.

Cada mutante rompe una fórmula de la ficha (cambio de base, de signo, de exponente, de ventana…). Se aplica sobre una
copia temporal del ejecutor y se mira quién lo caza:
  - CC: los casos de control de la ficha (`Motor.verificar_casos_control`, lo que decide la promoción en el Catálogo);
  - T:  las pruebas de su familia (`tests/test_fase1_*.py`) y `tests/test_t106_motor.py`.
Un mutante que sobrevive a CC y a T es una fórmula sin red. Uno que sobrevive a CC pero no a T indica que los casos de
control de la «Verificación» no bastan por sí solos para promover la ficha.

Uso: .venv/bin/python -I -B .docs/tickets/T-106/revisores/r01_04_mutantes.py [RAIZ] [--solo FICHA]
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("--")]
RAIZ = Path(args[0] if args else C.raiz_por_defecto()).resolve()
SOLO = sys.argv[sys.argv.index("--solo") + 1] if "--solo" in sys.argv else None
EJEC = RAIZ / "bloque_a" / "11_Ejecutor"
PY = str(RAIZ / ".venv" / "bin" / "python") if (RAIZ / ".venv" / "bin" / "python").exists() else sys.executable

MI, FD, TC = "fichas_mon_idx.py", "fichas_fon_der.py", "fichas_tcv.py"
PRUEBA = {MI: "tests/test_fase1_mon_idx.py", FD: "tests/test_fase1_fon_der.py", TC: "tests/test_fase1_tcv.py"}
MUTANTES = [
    # (id, archivo, ficha, [(viejo, nuevo)…], descripción)
    ("M01", MI, "MON-YLD-001", [("precio = 1 - x * t / BASE_360", "precio = 1 - x * t / DIAS_ANIO"),
                                ("return (1 - precio) * BASE_360 / t", "return (1 - precio) * DIAS_ANIO / t")],
     "descuento en base 365 (coherente ida y vuelta)"),
    ("M02", MI, "MON-YLD-001", [("precio = (1 + x) ** (-t / DIAS_ANIO)", "precio = (1 + x) ** (-t / BASE_360)"),
                                ("return float(precio ** (-DIAS_ANIO / t) - 1)", "return float(precio ** (-BASE_360 / t) - 1)")],
     "TAE con exponente 360/t"),
    ("M03", MI, "MON-YLD-001", [("* (spot / fwd)", "* (fwd / spot)")], "cubierto con F/S en vez de S/F"),
    ("M04", MI, "MON-EXP-001", [("r0 = oficial - dif", "r0 = oficial + dif")], "diferencial estable con el signo cambiado"),
    ("M05", MI, "MON-EXP-001", [("en_reunion = (rk - previo) / incremento", "en_reunion = (rk - r0) / incremento")],
     "movimiento de la reunión contra el vigente, no contra la reunión anterior"),
    ("M06", MI, "MON-REAL-001", [("ex_ante = (1 + i_nom) / (1 + pi_e) - 1", "ex_ante = i_nom - pi_e")],
     "Fisher aproximado ex ante"),
    ("M07", MI, "MON-REAL-001", [("real_p = nom / infl - 1", "real_p = nom - infl")], "Fisher aproximado ex post"),
    ("M08", MI, "MON-FIX-001", [('sendas["plana"] = [fwd[0]] * n_per', 'sendas["plana"] = [fwd[-1]] * n_per')],
     "senda plana al último forward"),
    ("M09", MI, "MON-FIX-001", [("fwd = [(math.exp(ldf[k] - ldf[k + 1]) - 1) * base / n_dias[k]",
                                 "fwd = [(math.exp(ldf[k] - ldf[k + 1]) - 1) * DIAS_ANIO / n_dias[k]")],
     "forwards anualizados en 365 con curva en 360"),
    ("M10", MI, "IDX-ERP-001", [("dval = (m_obj / m_act) ** (1 / N) - 1", "dval = (m_obj / m_act - 1) / N")],
     "cambio de valoración lineal, no compuesto"),
    ("M11", MI, "IDX-ERP-001", [("m_obj = m_act + lam * (mediana - m_act)", "m_obj = mediana + lam * (m_act - mediana)")],
     "λ invertida (fracción que queda, no la que se cierra)"),
    ("M12", MI, "IDX-ERP-001", [('"er_real": er - pi_e', '"er_real": er')], "E[R] real sin restar la inflación"),
    ("M13", MI, "IDX-CONC-001", [("return float(sum(w * w for w in pesos.values()))",
                                  "return float(sum(w ** 3 for w in pesos.values()))")], "HHI con cubos"),
    ("M14", MI, "IDX-CONC-001", [("sum(pesos[k] for k in orden[:top_n])", "sum(pesos[k] for k in orden[:top_n - 1])")],
     "top-n con n − 1"),
    ("M15", MI, "IDX-REL-001", [('"brecha": float(a.iloc[-1] / b.iloc[-1] - 1)', '"brecha": float(b.iloc[-1] / a.iloc[-1] - 1)')],
     "brecha B/A"),
    ("M16", MI, "IDX-REL-001", [("float(r[-1 - salto] / r[-1 - retro] - 1)", "float(r[-1] / r[-1 - retro] - 1)")],
     "momentum 12-0 en vez de 12-1"),
    ("M17", MI, "IDX-REB-001", [('"demanda": dw * aum,', '"demanda": dw * vol,')], "demanda con el volumen, no con los activos"),
    ("M18", MI, "IDX-REB-001", [("v2 = ar[ie + 1:ie + 1 + n_post]", "v2 = ar[ie:ie + n_post]")],
     "ventana posterior que incluye el día de efectividad"),
    ("M19", FD, "FON-DISC-001", [("filas.append(pr / nav - 1)", "filas.append(nav / pr - 1)")], "descuento NAV/P"),
    ("M20", FD, "FON-DISC-001", [("d_obj = d + kappa * (pos[\"media\"] - d)", "d_obj = d + (1 - kappa) * (pos[\"media\"] - d)")],
     "κ complementaria"),
    ("M21", FD, "FON-LEV-001", [("A = 0.5 * (L * L - L) * T", "A = 0.5 * (L * L - 1) * T")], "arrastre ½(L² − 1)"),
    ("M22", FD, "FON-LEV-001", [("math.exp(-0.5 * (L * L - L) * var_T)", "math.exp(-0.5 * (L * L) * var_T)")],
     "fórmula R_L con ½L²σ²T"),
    ("M23", FD, "FON-TD-001", [("float(np.std(rv[ini:] - ri[ini:], ddof=1)) * math.sqrt(SESIONES_ANIO)",
                                "float(np.std(rv[ini:] - ri[ini:], ddof=1)) * SESIONES_ANIO")], "TE anualizado con 252, no √252"),
    ("M24", FD, "DER-VRP-001", [("var = 2 / T * float(", "var = 1 / T * float(")], "réplica con 1/T"),
    ("M25", FD, "DER-VRP-001", [("math.exp(r * T) * Q))", "math.exp(-r * T) * Q))")], "réplica con e^{−rT}"),
    ("M26", FD, "DER-VRP-001", [("- (fwd / k0 - 1) ** 2 / T", "+ (fwd / k0 - 1) ** 2 / T")], "término de corrección de K₀ sumado"),
    ("M27", FD, "DER-VRP-001", [("vrp_var = float(var_imp[-1]) - e_rv", "vrp_var = float(var_imp[-2]) - e_rv")],
     "VRP ex ante con la implícita de ayer"),
    ("M28", FD, "DER-SKEW-001", [("return float(stats.norm.cdf((-k + 0.5 * sd * sd) / sd))",
                                  "return float(stats.norm.cdf((-k - 0.5 * sd * sd) / sd))")], "delta con N(d2)"),
    ("M29", FD, "DER-SKEW-001", [("w2 = b * s * s / raiz ** 3", "w2 = b * s / raiz ** 3")], "w'' de SVI mal derivada"),
    ("M30", FD, "DER-SKEW-001", [("return (float(np.interp(1 - delta, xs, ys)), float(np.interp(delta, xs, ys)),",
                                  "return (float(np.interp(delta, xs, ys)), float(np.interp(1 - delta, xs, ys)),")],
     "put y call de 25Δ intercambiadas"),
    ("M31", FD, "DER-TERM-001", [('"sigma_fwd_pct": math.sqrt((sb * sb * tb - sa * sa * ta) / (tb - ta)) * A_PCT',
                                  '"sigma_fwd_pct": math.sqrt((sb * sb * tb - sa * sa * ta) / tb) * A_PCT')], "σ_fwd / T₂"),
    ("M32", FD, "DER-ROLL-001", [("carry = np.log(Fp / S) / T", "carry = (Fp / S - 1) / T")], "carry simple, no logarítmico"),
    ("M33", FD, "DER-ROLL-001", [("roll = float((Fp[i] / Fp[j] - 1) * anual / (dias[j] - dias[i]))",
                                  "roll = float((Fp[i] / Fp[j] - 1) * anual / dias[j])")], "roll anualizado con días al 2.º"),
    ("M34", FD, "DER-ROLL-001", [('"roll_pct": (fut_r - spot_r) * A_PCT', '"roll_pct": (fut_r - spot_r - col) * A_PCT')],
     "descomposición: roll sin colateral"),
    ("M35", TC, "TCV-CDS-001", [("lam = s / PB_POR_UNIDAD / (1 - R)", "lam = s / PB_POR_UNIDAD / R")], "λ = s/R"),
    ("M36", TC, "TCV-CDS-001", [("el = pd_anual * (1 - R) * PB_POR_UNIDAD", "el = pd_anual * PB_POR_UNIDAD")],
     "pérdida esperada sin (1 − R)"),
    ("M37", TC, "TCV-VIXTS-001", [("roll_dia = float((precios[0] - spot) / dias[0])", "roll_dia = float((precios[1] - spot) / dias[0])")],
     "roll con el segundo futuro"),
    ("M38", TC, "TCV-BEI-001", [("return float(((1 + y_fin) ** t_fin / (1 + y_ini) ** t_ini) ** (1 / (t_fin - t_ini)) - 1)",
                                 "return float(((1 + y_fin) ** t_fin / (1 + y_ini) ** t_ini) ** (1 / t_fin) - 1)")],
     "forward con 1/t_fin"),
    ("M39", TC, "TCV-TP-001", [("A[n] = A[n - 1] + Bp @ (mu - lam0) + (Bp @ Sigma @ Bp + sigma2) / 2 - delta0",
                                "A[n] = A[n - 1] + Bp @ (mu - lam0) + (Bp @ Sigma @ Bp + sigma2) - delta0")],
     "ACM sin el ½ de convexidad (generación y estimación comparten la recursión)"),
    ("M40", TC, "TCV-TP-001", [("lam0 = proy @ (a + (Bstar @ Sigma.ravel() + sigma2) / 2)", "lam0 = proy @ a")],
     "λ₀ sin la corrección de convexidad"),
    ("M41", TC, "TCV-TP-001", [("B[n] = Bp @ (Phi - lam1) - delta1", "B[n] = Bp @ (Phi + lam1) - delta1")],
     "recursión de B con Φ + λ₁ (compartida con el generador sintético)"),
]

base = Path(tempfile.mkdtemp(prefix="qa_t106_mut_"))
copia = base / "11_Ejecutor"
shutil.copytree(EJEC, copia, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache", ".mypy_cache",
                                                             "*.egg-info", "build"))
entorno = {**os.environ, "PYTHONPATH": str(copia), "BLOQUE_A_RAIZ": str(RAIZ / "bloque_a"), "PYTHONDONTWRITEBYTECODE": "1"}
CC = """
import sys, tempfile
from pathlib import Path
from bloque_a.motor import servicio as S
assert Path(S.__file__).resolve().is_relative_to(Path({copia!r}).resolve()), S.__file__
from bloque_a.almacen import Almacen
from bloque_a.configuracion import cargar_config
class P: as_of=None; nombre="m"
m = S.Motor(Almacen(Path(tempfile.mkdtemp())), P(), cargar_config())
r = m.verificar_casos_control([{ficha!r}])[{ficha!r}]
print("SUPERA" if r["superados"] else "CAZADO", [c["nombre"][:50] for c in r["casos"] if not c["superado"]])
"""
vivos_cc, vivos_total = [], []
for mid, arch, ficha, cambios, desc in MUTANTES:
    if SOLO and ficha != SOLO:
        continue
    ruta = copia / "bloque_a" / "motor" / arch
    original = ruta.read_text(encoding="utf-8")
    texto = original
    for viejo, nuevo in cambios:
        if texto.count(viejo) != 1:
            C.informe(f"{mid} {ficha}: el mutante se aplica", False, f"«{viejo[:60]}» aparece {texto.count(viejo)} veces")
            break
        texto = texto.replace(viejo, nuevo)
    else:
        ruta.write_text(texto, encoding="utf-8")
        try:
            cc = subprocess.run([PY, "-B", "-c", CC.format(copia=str(copia), ficha=ficha)], capture_output=True, text=True,
                                cwd=copia, env=entorno, timeout=300)
            cazado_cc = "CAZADO" in cc.stdout or cc.returncode != 0
            t = subprocess.run([PY, "-B", "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", PRUEBA[arch],
                                "tests/test_t106_motor.py"], capture_output=True, text=True, cwd=copia, env=entorno, timeout=600)
            cazado_t = t.returncode != 0
            linea = (cc.stdout.strip() or cc.stderr.strip().splitlines()[-1])[:110]
            print(f"{mid} {ficha:13s} CC={'cazado' if cazado_cc else 'VIVO  '} T={'cazado' if cazado_t else 'VIVO  '} · {desc} · {linea}",
                  flush=True)
            if not cazado_cc:
                vivos_cc.append(f"{mid} {ficha} ({desc})")
            if not cazado_cc and not cazado_t:
                vivos_total.append(f"{mid} {ficha} ({desc})")
        finally:
            ruta.write_text(original, encoding="utf-8")
shutil.rmtree(base, ignore_errors=True)
print(f"\nVivos frente a los casos de control (CC): {len(vivos_cc)}")
for x in vivos_cc:
    print("   ·", x)
C.informe("ningún mutante sobrevive a casos de control y pruebas a la vez", not vivos_total, "; ".join(vivos_total))
sys.exit(C.resumen())
