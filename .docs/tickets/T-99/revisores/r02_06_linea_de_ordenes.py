"""r02_06 · Línea de órdenes del registro 0.2.0, con un intento de verdad (r01_08 no pasaba --variante, que ahora es
obligatoria, y sus casos de --detalle fallaban por no haber intento, no por el detalle). Siempre con --registro temporal.
Uso: python3 -B r02_06_linea_de_ordenes.py <raíz>"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r02_comun import RAIZ, caso, fin, leer, pre, registro_temporal  # noqa: E402

CLI = RAIZ / ".docs" / "scripts" / "registro_experimentos.py"


def run(*args, cwd=None):
    p = subprocess.run([sys.executable, "-B", str(CLI), *args], capture_output=True, cwd=str(cwd or RAIZ))
    salida = (p.stdout + p.stderr).decode("utf-8", "replace").strip().splitlines()
    return p.returncode, (salida[-1] if salida else ""), p


def nuevo():
    reg = registro_temporal(); R = str(reg.ruta)
    f = reg.ruta.parent / "pre.json"; f.write_text(json.dumps(pre()), encoding="utf-8")
    rc, out, _ = run("--registro", R, "prerregistrar", str(f), "--autor", "qa")
    return reg, R, f, out.split()[0]


# 1. --registro delante y detrás; --variante obligatoria
reg, R, f, exp = nuevo()
rc, out, _ = run("prerregistrar", str(f), "--registro", R)
caso("«prerregistrar <f> --registro R» (como dice el uso)", rc == 0, out[:80])
rc, out, _ = run("--registro", R, "intento", exp)
caso("(regla declarada) intento sin --variante: código 2 y sin escribir", rc == 2 and len(reg.anotaciones()) == 2, out[:90])
rc, out, _ = run("intento", exp, "--variante", "v1", "--registro", R)
caso("intento con --variante y --registro detrás", rc == 0, out)
rc, out, _ = run("--registro", R, "resultado", exp, "1", "todavía no se sabe")
caso("veredicto con espacios en un solo argumento (r01_08 caso 5, con intento)", rc == 0, out)

# 2. --detalle raro sobre un intento que existe
for det in ("{roto", "[1]", "NaN", '"texto"', "Infinity", '{"a": -Infinity}', '{"a": [NaN]}', "null", "1e999",
            '{"a": "\\ud800"}'):
    reg, R, f, exp = nuevo(); run("--registro", R, "intento", exp, "--variante", "v1")
    antes = leer(reg.ruta)
    rc, out, _ = run("--registro", R, "resultado", exp, "1", "peor", "--detalle", det)
    caso(f"--detalle {det}: código 2 y sin escribir", rc == 2 and leer(reg.ruta) == antes, f"rc={rc} · {out[:90]}")
reg, R, f, exp = nuevo(); run("--registro", R, "intento", exp, "--variante", "v1")
rc, out, _ = run("--registro", R, "resultado", exp, "1", "peor", "--detalle", '{"nota": "bien"}')
caso("--detalle objeto válido: código 0", rc == 0, out)

# 3. n y variantes raros
reg, R, f, exp = nuevo(); run("--registro", R, "intento", exp, "--variante", "v1")
for n in ("0", "-1", "2", "1.0"):
    antes = leer(reg.ruta)
    rc, out, _ = run("--registro", R, "resultado", exp, n, "peor")
    caso(f"resultado del intento {n}: código 2 y sin escribir", rc == 2 and leer(reg.ruta) == antes, out[:80])
for v in ("", "   ", "\u2028", "\udcff"):
    reg, R, f, exp = nuevo(); antes = leer(reg.ruta)
    try:
        rc, out, _ = run("--registro", R, "intento", exp, "--variante", v)
    except (UnicodeEncodeError, ValueError) as e:
        rc, out = "no se pudo lanzar", str(e)
    caso(f"variante {v!r}: código 2 y sin escribir (salvo U+2028, que es texto)", (rc == 2 and leer(reg.ruta) == antes)
         or (v == "\u2028" and rc == 0), f"rc={rc} · {out[:80]}")

# 4. prerregistros raros
reg = registro_temporal(); R = str(reg.ruta)
for nombre, contenido in (("null", "null"), ("lista", "[1]"), ("surrogate", json.dumps(pre(hipotesis="Hipótesis \ud800 larga"))),
                          ("NaN", json.dumps(pre(semilla=float("nan")))), ("bool en semilla", json.dumps(pre(semilla=True))),
                          ("max 1001", json.dumps(pre(max_variantes=1001))), ("datos objeto", json.dumps(pre(datos={"a": 1})))):
    g = reg.ruta.parent / f"p_{nombre.replace(' ', '_')}.json"; g.write_text(contenido, encoding="utf-8")
    rc, out, _ = run("--registro", R, "prerregistrar", str(g))
    caso(f"prerregistro {nombre}: código 2 y sin escribir", rc == 2 and not reg.ruta.exists(), f"rc={rc} · {out[:90]}")

# 5. Rutas de registro raras: vacía, directorio, y el registro del repositorio sin --registro con «ver» (solo lectura)
rc, out, _ = run("--registro", "", "verificar")
caso("--registro vacío: código 2", rc == 2, out[:80])
d = registro_temporal().ruta.parent
rc, out, _ = run("--registro", str(d), "verificar")
caso("--registro que es un directorio: código 2 y sin traza", rc == 2 and "Traceback" not in out, out[:90])
rc, out, _ = run("--registro", str(d / "no" / "existe.jsonl"), "ver")
caso("«ver» de un registro que no existe: «[]» y no crea nada", rc == 0 and out == "[]" and not (d / "no").exists(), out)
rc, out, _ = run("--registro", str(d / "no" / "existe.jsonl"), "intento", "EXP-2026-0001", "--variante", "v")
caso("(baja) un intento rechazado no crea carpetas ni «.lock» (validar antes de mutar)", not (d / "no").exists(),
     f"rc={rc}; queda: {sorted(x.name for x in (d / 'no').iterdir()) if (d / 'no').exists() else '-'}")
fin()
