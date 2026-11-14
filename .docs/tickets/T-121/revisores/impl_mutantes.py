"""Mutantes de las correcciones de T-121 (y del ajuste del solicitante). Se aplican en una copia desechable del ejecutor
(DESTINO/11_Ejecutor, con el Catálogo al lado) y se ejecutan `tests/test_t121_hallazgos.py` y
`tests/test_t118_hallazgos.py` (-x). MUERTO = alguna prueba falla.
Uso: python impl_mutantes.py ORIGEN_EJECUTOR DESTINO [--solo ID,ID]   (DESTINO: carpeta desechable fuera del repo; sin
--solo se borra al acabar)"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

ORIGEN = Path(sys.argv[1]).resolve()
BASE = Path(sys.argv[2]).resolve()
assert not (BASE / ".git").exists() and BASE != ORIGEN, "DESTINO debe ser una carpeta desechable"
COPIA = BASE / "11_Ejecutor"
SOLO = sys.argv[sys.argv.index("--solo") + 1].split(",") if "--solo" in sys.argv else None
PY = "/home/user/robotinvestor/.venv/bin/python"
PRUEBAS = ["tests/test_t121_hallazgos.py", "tests/test_t118_hallazgos.py", "tests/test_t112_motor.py"]
MO, TC, FD, SV, SE = (f"bloque_a/motor/{n}.py" for n in ("fichas_mon_idx", "fichas_tcv", "fichas_fon_der", "servicio",
                                                          "fichas_series"))

if BASE.exists():
    shutil.rmtree(BASE)
BASE.mkdir(parents=True)
shutil.copytree(ORIGEN, COPIA, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
shutil.copytree(ORIGEN.parent / "04_Motor_conocimiento_y_catalogo", BASE / "04_Motor_conocimiento_y_catalogo")

M = []
# H-04: cada llamada a la comprobación del corte, neutralizada (los argumentos se siguen evaluando)
for mod in (MO, TC, FD):
    for n, linea in enumerate((COPIA / mod).read_text(encoding="utf-8").splitlines(), 1):
        if re.search(r"_hasta_corte(_peticion)?\(", linea) and "def _hasta_corte" not in linea:
            M.append((f"C{len(M) + 1:02d}", mod, n, re.sub(r"_hasta_corte(_peticion)?\(", "(lambda *a: None)(", linea, count=1),
                      f"{mod.split('/')[-1]}:{n} sin corte"))
fijos = [
    ("B01", MO, "    posteriores = [f for f in map(_dia, fechas) if f > corte]", "    posteriores = [f for f in map(_dia, fechas) if f >= corte]", "mon_idx: el día del corte no es conocible"),
    ("B02", MO, "    posteriores = [f for f in map(_dia, fechas) if f > corte]", "    posteriores = [f for f in fechas if f > corte]", "mon_idx: con hora y no por día"),
    ("B03", TC, "    posteriores = [f for f in fechas if f > corte]", "    posteriores = [f for f in fechas if f >= corte]", "tcv: el día del corte no es conocible"),
    ("B04", FD, "    if ultima > corte:", "    if ultima >= corte:", "fon_der: el día del corte no es conocible"),
    ("B05", TC, "        except _PosteriorAlCorte:", "        except ZeroDivisionError:", "tcv: la segunda vía posterior al corte se degrada a limitación"),
    ("B06", TC, "        if isinstance(fc, bool) or not isinstance(fc, (str, date, np.datetime64)):", "        if False:", "tcv: un corte que no es fecha se acepta"),
    ("B07", MO, "    return (t if t.tz is None else t.tz_convert(None)).normalize()", "    return (t if t.tz is None else t.tz_convert(None))", "mon_idx: _dia sin normalizar"),
    # H-01
    ("A01", SV, "        elif difs and no_reproducidas:", "        elif difs and (sin_registro or cambiadas):", "CT-10: vuelve la regla de T-118"),
    ("A02", SV, "                                                      or (reg.get(\"por_defecto\") != vigente[k][\"por_defecto\"]", "                                                      or (False", "CT-10: no mira el por_defecto"),
    ("A04", SV, "        return True\n    return isinstance(valor, dict) and all(", "        return False\n    return isinstance(valor, dict) and all(", "_cubre: nunca cubre (vuelve el ablandamiento tras T-57)"),
    ("A05", SV, "    return isinstance(valor, dict) and all(k in valor and _cubre(valor[k], d) for k, d in defecto.items())", "    return True", "_cubre: siempre cubre (un valor parcial culpa al original)"),
    ("A03", SV, "        no_reproducidas = sorted(set(sin_registro) |", "        no_reproducidas = sorted(set() |", "CT-10: no mira sin_registro"),
    # H-02
    ("D01", SV, "        if ilegibles:", "        if False:", "servir: no comprueba que se pueda escribir"),
    ("D02", SV, "            if peticion.get(campo) is not None and not isinstance(peticion[campo], str):", "            if False:", "servir: horizonte, modo, prioridad sin tipo"),
    ("D03", SV, "        if not forma and raros:", "        if False:", "servir: argumentos raros sin rechazo"),
    ("D04", SV, "            motivo_forma = \"CANAL_NO_AUTORIZADO\" if \"solicitante\" in raros else motivo_forma", "            pass", "servir: solicitante raro con DATOS_INCOHERENTES"),
    ("D05", SV, "            f_ = f_ if isinstance(f_, str) and _escribible(f_) else None", "            f_ = f_ if isinstance(f_, str) else None", "servir: la ficha ilegible va al RC"),
    ("D06", SV, "        if copiar:\n            copy.deepcopy(x)", "        if False:\n            copy.deepcopy(x)", "_escribible sin copiar"),
    # H-03
    ("E01", SV, "        except (DatosNoDisponibles, FugaDeInformacion) as exc:", "        except (ZeroDivisionError,) as exc:", "reejecutar: datos irresolubles escapan"),
    ("E02", SV, "        except (KeyError, TypeError, ValueError, AttributeError, IndexError, OverflowError, RecursionError, MemoryError) as exc:", "        except (ZeroDivisionError,) as exc:", "reejecutar: artefacto alterado escapa"),
    ("E03", SV, "            if not isinstance(orig[\"parametros\"], dict) or \"payload\" not in orig[\"resultado\"]:", "            if False:", "reejecutar: sin comprobar parámetros y resultado"),
    # H-05
    ("F01", SE, "    if F == \"REG-HMM-001\":   # T-121 (H-05): H5 en semanas, con la configuración del Motor\n        return _semanas_h5(cfg)\n", "", "REG-HMM sin seguir a la configuración"),
    ("F02", SE, "            return max(x * numerador // denominador, 1)", "            return max(x * 4, 1)", "REG-HMM: 4 semanas por mes"),
    ("F03", SE, "            if isinstance(x, bool) or not isinstance(x, int) or x < 1:", "            if False:", "H5 sin validar"),
]
for i, mod, a, b, d in fijos:
    M.append((i, mod, a, b, d))

vivos = []
for mid, mod, a, b, desc in M:
    if SOLO and mid not in SOLO:
        continue
    ruta = COPIA / mod
    orig = ruta.read_text(encoding="utf-8")
    if isinstance(a, int):
        lineas = orig.split("\n")
        lineas[a - 1] = b
        nuevo = "\n".join(lineas)
    else:
        if orig.count(a) != 1:
            print(f"{mid}: el texto aparece {orig.count(a)} veces; no se aplica · {desc}", flush=True)
            continue
        nuevo = orig.replace(a, b)
    ruta.write_text(nuevo, encoding="utf-8")
    try:
        r = subprocess.run([PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS], cwd=COPIA,
                           capture_output=True, text=True, timeout=1800, check=False)
        muerto = r.returncode != 0
        fallo = next((ln for ln in r.stdout.splitlines() if ln.startswith(("FAILED", "ERROR"))), "")
    finally:
        ruta.write_text(orig, encoding="utf-8")
    print(f"{mid} {'muere' if muerto else 'VIVE '} · {desc} · {fallo[:140]}", flush=True)
    if not muerto:
        vivos.append(mid)
print(f"\n{len([m for m in M if not SOLO or m[0] in SOLO])} mutantes; vivos: {', '.join(vivos) or 'ninguno'}")
if not SOLO:
    shutil.rmtree(BASE)
