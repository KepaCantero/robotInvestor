"""QA r02 de T-106 · Mutantes nuevos del revisor sobre el código de la r02: las tres familias de fichas (sobre todo lo
que la r02 rehízo o añadió: MON-EXP, validación, envolturas, y las fichas que la r01 no mutó) y `servicio.py`
(«manda el Catálogo», rechazo de excepciones y de cifras no finitas, registro de los casos de control).

Cada mutante se aplica sobre una copia del ejecutor en una carpeta temporal (el árbol revisado no se toca) y se mira quién
lo caza:
  - CC: los casos de control de la ficha (`Motor.verificar_casos_control`; lo que decide la promoción);
  - T:  las pruebas (`tests/test_fase1_*.py` de su familia y `tests/test_t106_motor.py`; para `servicio.py`, las cuatro
        de T-106 y las del Motor existentes).
Un mutante vivo frente a CC y T es una regla sin red. Los mutantes de `servicio.py` no tienen CC propio (CC = «—»).

Uso: .venv/bin/python -I -B .docs/tickets/T-106/revisores/r02_04_mutantes.py [RAIZ] [--solo ID]
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

MI, FD, TC, SV = "fichas_mon_idx.py", "fichas_fon_der.py", "fichas_tcv.py", "servicio.py"
T106 = ["tests/test_fase1_mon_idx.py", "tests/test_fase1_fon_der.py", "tests/test_fase1_tcv.py", "tests/test_t106_motor.py"]
PRUEBA = {MI: [T106[0], T106[3]], FD: [T106[1], T106[3]], TC: [T106[2], T106[3]],
          SV: T106 + ["tests/test_unitarias.py", "tests/test_t65_resto_t53.py", "tests/test_t87_contratos.py", "tests/test_t92_revision.py"]}
MUTANTES = [
    # ---------------------------------------------------------------- MON-EXP-001 (rehecho en la r02)
    ("X01", MI, "MON-EXP-001", [("if utiles <= n_tramos and not alineada:", "if False:")],
     "sin la regla de contraste (sistema justo con nodos fuera de las reuniones)"),
    ("X02", MI, "MON-EXP-001", [("if err > max(tol * (abs(r_nodo) if r_nodo != 0 else 1.0), declarada or 0.0):",
                                 "if err > max(tol * (abs(r_nodo) if r_nodo != 0 else 1.0), declarada or 1e-4):")],
     "tolerancia de reproducción de 1 pb sin precisión declarada"),
    ("X03", MI, "MON-EXP-001", [("if not c < incremento:", "if not c < 4 * incremento:")],
     "identificación frente al redondeo con 4 Δ"),
    ("X04", MI, "MON-EXP-001", [('precision.append(declarada if declarada is not None else _media_unidad(n["tipo"]))',
                                 "precision.append(declarada if declarada is not None else 0.0)")],
     "sin el redondeo implícito de cada cotización (curva OIS)"),
    ("X05", MI, "MON-EXP-001", [("acumulados = (rk + dif - oficial) / incremento", "acumulados = (rk - oficial) / incremento")],
     "acumulados contra el tipo oficial sin el diferencial"),
    ("X06", MI, "MON-EXP-001", [("        if d_h > d_fin:", "        if d_h >= d_fin:")], "H-10 deshecho (horizonte = último nodo)"),
    ("X07", MI, "MON-EXP-001", [('if p["convexidad"] and d > limite:', "if False:")],
     "futuros a más de 1 año sin ajuste de convexidad ni truncamiento"),
    ("X08", MI, "MON-EXP-001", [("y[i] = lg - min(d, cortes[1]) * l0", "y[i] = lg - min(d, cortes[1]) * l0 * 0.5")],
     "tramo previo a la primera reunión mal descontado"),
    # ---------------------------------------------------------------- validación y envoltura (MON/IDX)
    ("X09", MI, "IDX-REL-001", [("    if len(saltos) and not (saltos == 1).all():", "    if False:")], "H-07 deshecho (historia no mensual)"),
    ("X10", MI, "MON-YLD-001", [("    if not isinstance(x, (str, dt.date, pd.Timestamp, np.datetime64)):", "    if False:")],
     "H-11 deshecho (fecha numérica como epoch)"),
    ("X11", MI, "IDX-REL-001", [("            if malos:\n                raise ErrorFicha(f\"{ficha}: resultado no finito",
                                 "            if False:\n                raise ErrorFicha(f\"{ficha}: resultado no finito")],
     "envoltura MON/IDX sin el rechazo de cifras no finitas"),
    # ---------------------------------------------------------------- FON / DER
    ("Y01", FD, "FON-DISC-001", [("mediana = np.median(D, axis=0)", "mediana = np.mean(D, axis=0)")], "agregado por media, no mediana"),
    ("Y02", FD, "FON-DISC-001", [("vida_meses = vida * paso.days * MESES_ANIO / DIAS_ANIO", "vida_meses = vida * paso.days / 30")],
     "vida media en meses de 30 días"),
    ("Y03", FD, "FON-DISC-001", [('m_media = fechas > corte - pd.Timedelta(weeks=float(p["ventana_media"]))',
                                  'm_media = fechas > corte - pd.Timedelta(weeks=2 * float(p["ventana_media"]))')],
     "ventana media de 104 semanas"),
    ("Y04", FD, "FON-FLOW-001", [('acum[str(k)] = {"moneda": mon, "pct_aum": mon / float(ap[i0]) * A_PCT}',
                                  'acum[str(k)] = {"moneda": mon, "pct_aum": mon / float(ap[-1]) * A_PCT}')],
     "acumulado relativo al AUM del último periodo"),
    ("Y05", FD, "FON-FLOW-001", [("mz = ff > corte - pd.DateOffset(months=vz)", "mz = ff > corte - pd.DateOffset(months=2 * vz)")],
     "z frente a 72 meses"),
    ("Y06", FD, "FON-FLOW-001", [("return float(np.sum(d[k:] * d[:-k]) / den)", "return float(np.sum(d[k:] * d[:-k]) / float(np.sum(d[k:] ** 2)))")],
     "autocorrelación con otro denominador"),
    ("Y07", FD, "DER-TERM-001", [("return math.sqrt(float(np.interp(t, T, w)) / t)", "return float(np.interp(t, T, vol))")],
     "interpolación lineal en σ, no en varianza total"),
    ("Y08", FD, "DER-TERM-001", [('"sigma_fwd_pct": math.sqrt((sb * sb * tb - sa * sa * ta) / (tb - ta)) * A_PCT',
                                  '"sigma_fwd_pct": math.sqrt((sb * sb * tb - sa * sa * ta) / tb) * A_PCT')], "σ_fwd dividida por T₂"),
    ("Y09", FD, "DER-TERM-001", [("var_e = s_con * s_con * tc - sb_ * sb_ * tc", "var_e = s_con * s_con - sb_ * sb_")],
     "varianza del evento sin T"),
    ("Y10", FD, "DER-TERM-001", [("if np.any(np.diff(w) < -tol * w[:-1]):\n        raise", "if False:\n        raise")],
     "sin el rechazo por arbitraje de calendario"),
    ("Y11", FD, "FON-LEV-001", [("        malos = _no_finitos(res)\n        if malos:", "        malos = _no_finitos(res)\n        if False:")],
     "envoltura FON/DER sin el rechazo de cifras no finitas"),
    # ---------------------------------------------------------------- TCV
    ("Z01", TC, "TCV-SLOPE-001", [("w = 1 - rez / (rezagos + 1)", "w = 1.0")], "HAC con pesos uniformes (no Bartlett)"),
    ("Z02", TC, "TCV-SLOPE-001", [("return math.floor(4 * (n / 100) ** (2 / 9))", "return math.floor(4 * (n / 100) ** (1 / 4))")],
     "otra regla de rezagos"),
    ("Z03", TC, "TCV-SLOPE-001", [("idx_est = np.where(en_ventana)[0][:-1]", "idx_est = np.where(en_ventana)[0]")],
     "la observación actual entra en la estimación"),
    ("Z04", TC, "TCV-SLOPE-001", [('c = (ca["carry"] / ca["d_mod"] - cb["carry"] / cb["d_mod"]) * PB_POR_UNIDAD',
                                   'c = (ca["carry"] - cb["carry"]) * PB_POR_UNIDAD')], "carry sin neutralizar el DV01"),
    ("Z05", TC, "TCV-VIXTS-001", [("roll_pct_mes = float((precios[0] - spot) / precios[0] * vc / dias[0] * PCT)",
                                   "roll_pct_mes = float((precios[0] - spot) / spot * vc / dias[0] * PCT)")], "roll % sobre el spot"),
    ("Z06", TC, "TCV-VIXTS-001", [("w = float((dias[i + 1] - vc) / (dias[i + 1] - dias[i]))",
                                   "w = float((vc - dias[i]) / (dias[i + 1] - dias[i]))")], "pesos de interpolación a 30 días cruzados"),
    ("Z07", TC, "TCV-VIXTS-001", [("es_corta = float(-np.mean(corta[corta <= q]))", "es_corta = float(-q)")], "VaR en lugar de ES"),
    ("Z08", TC, "TCV-VIXTS-001", [("estado = _estado([spot, float(precios[0]), float(precios[1])])",
                                   "estado = _estado([float(precios[0]), float(precios[1])])")], "estado sin el spot"),
    ("Z09", TC, "TCV-TP-001", [("    if plazos[-1] != max_m:", "    if plazos[-1] > 10 * max_m:")], "plazos más allá de 10 años"),
    # ---------------------------------------------------------------- servicio.py
    ("S01", SV, None, [('return estado.startswith("IMPLEMENTADO") or estado.startswith("VALIDADO")', "return bool(estado)")],
     "sirve también lo «Documentado» del Catálogo"),
    ("S02", SV, None, [("for m in _FILA_CATALOGO.finditer(texto[i:j]):", "for m in _FILA_CATALOGO.finditer(texto):")],
     "H-06 deshecho (cualquier fila del documento)"),
    ("S03", SV, None, [("except (OSError, ValueError):   # QA r01", "except OSError:   # QA r01")], "H-05 deshecho (bytes no UTF-8)"),
    ("S04", SV, None, [("self.raiz = raiz_paquete(cfg)", "self.raiz = None")], "H-04 deshecho (raíz configurada ignorada)"),
    ("S05", SV, None, [("return dict(_madurez(str(ruta), mtime))", "return dict(_madurez(str(ruta), 0))")],
     "caché sin la fecha de modificación (H-06)"),
    ("S06", SV, None, [("and ficha not in DOCUMENTADAS_CON_CODIGO\n", "\n")], "sirve las DOCUMENTADAS_CON_CODIGO"),
    ("S07", SV, None, [("        except (ValueError, TypeError, ArithmeticError, KeyError, IndexError, AttributeError, np.linalg.LinAlgError) as e:",
                        "        except ZeroDivisionError as e:")], "H-02 deshecho en el Motor (excepciones al llamador)"),
    ("S08", SV, None, [("if ficha in FASE1 and (_no_finito(resultado) or _no_finito(resultado2)):", "if False:")],
     "H-02 deshecho en el Motor (cifras no finitas)"),
    ("S09", SV, None, [("superados = bool(res) and all(x[\"superado\"] for x in res)", "superados = all(x[\"superado\"] for x in res)")],
     "una ficha sin casos de control se da por superada"),
    ("S10", SV, None, [("and _limpio(r1) == _limpio(r2), None", ", None")], "casos de control sin comparar las dos pasadas"),
    ("S11", SV, None, [('if ficha == "VOL-GARCH-001" and citable_segun_catalogo(ficha, self.raiz) and not garch_disponible():',
                        "if False:")], "H-12 deshecho (detalle de GARCH sin arch)"),
    ("S12", SV, None, [('i, j = texto.find("\\n## 4."), texto.find("\\n## 5.")', 'i, j = 0, len(texto)')],
     "sin acotar la tabla del §4 (equivalente a S02)"),
]

# Copia del bloque_a entero (sin .docx), para que el ejecutor copiado encuentre el Catálogo y los prompts en su propia
# raíz (`DIR_EJECUTOR.parent`), como en el repositorio: las pruebas de T-106 leen el Catálogo de ahí.
base = Path(tempfile.mkdtemp(prefix="qa_r02_t106_mut_"))
shutil.copytree(RAIZ / "bloque_a", base / "bloque_a", ignore=shutil.ignore_patterns(
    "__pycache__", "*.pyc", ".pytest_cache", ".mypy_cache", "*.egg-info", "build", "*.docx"))
copia = base / "bloque_a" / "11_Ejecutor"
entorno = {k: v for k, v in os.environ.items() if k != "BLOQUE_A_RAIZ"}
entorno.update({"PYTHONPATH": str(copia), "PYTHONDONTWRITEBYTECODE": "1"})
base_t = subprocess.run([PY, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *PRUEBA[SV]], capture_output=True, text=True,
                        cwd=copia, env=entorno, timeout=1800)
C.informe("las pruebas pasan en la copia sin mutar (si no, «cazado» no significaría nada)", base_t.returncode == 0,
          (base_t.stdout.strip().splitlines() or [""])[-1][:120])
if base_t.returncode != 0:
    sys.exit(C.resumen())
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
vivos_cc, vivos_total, n = [], [], 0
for mid, arch, ficha, cambios, desc in MUTANTES:
    if SOLO and mid != SOLO:
        continue
    ruta = copia / "bloque_a" / "motor" / arch
    original = ruta.read_text(encoding="utf-8")
    texto = original
    for viejo, nuevo in cambios:
        if texto.count(viejo) != 1:
            C.informe(f"{mid}: el mutante se aplica", False, f"«{viejo[:70]}» aparece {texto.count(viejo)} veces")
            break
        texto = texto.replace(viejo, nuevo)
    else:
        n += 1
        ruta.write_text(texto, encoding="utf-8")
        try:
            if ficha:
                cc = subprocess.run([PY, "-B", "-c", CC.format(copia=str(copia), ficha=ficha)], capture_output=True, text=True,
                                    cwd=copia, env=entorno, timeout=300)
                cazado_cc = "CAZADO" in cc.stdout or cc.returncode != 0
                linea = (cc.stdout.strip() or (cc.stderr.strip().splitlines() or [""])[-1])[:100]
            else:
                cazado_cc, linea = None, ""
            t = subprocess.run([PY, "-B", "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBA[arch]],
                               capture_output=True, text=True, cwd=copia, env=entorno, timeout=1800)
            cazado_t = t.returncode != 0
            fallo_t = next((x for x in t.stdout.splitlines() if x.startswith("FAILED")), "")[:110]
            et_cc = "—     " if cazado_cc is None else ("cazado" if cazado_cc else "VIVO  ")
            print(f"{mid} {str(ficha or 'servicio'):13s} CC={et_cc} T={'cazado' if cazado_t else 'VIVO  '} · {desc}"
                  f"{' · ' + linea if linea else ''}{' · ' + fallo_t if fallo_t else ''}", flush=True)
            if cazado_cc is False:
                vivos_cc.append(f"{mid} {ficha} ({desc})")
            if not cazado_cc and not cazado_t:
                vivos_total.append(f"{mid} {ficha or 'servicio'} ({desc})")
        finally:
            ruta.write_text(original, encoding="utf-8")
shutil.rmtree(base, ignore_errors=True)
print(f"\n{n} mutantes aplicados. Vivos frente a los casos de control (CC): {len(vivos_cc)}")
for x in vivos_cc:
    print("   ·", x)
print(f"Vivos frente a CC y T a la vez: {len(vivos_total)}")
for x in vivos_total:
    print("   ·", x)
C.informe("ningún mutante sobrevive a casos de control y pruebas a la vez", not vivos_total, "; ".join(vivos_total))
sys.exit(C.resumen())
