"""r01_08 · Línea de órdenes del registro: --registro donde lo pone el uso del docstring, ficheros ausentes o mal formados,
--detalle raro, registro inexistente en «verificar». Nunca se llama sin --registro (no toca el del repositorio).
Uso: python3 -B r01_08_linea_de_ordenes.py <raíz>"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import RAIZ, caso, fin, lineas, pre, registro_temporal  # noqa: E402

CLI = RAIZ / ".docs" / "scripts" / "registro_experimentos.py"


def run(*args):
    p = subprocess.run([sys.executable, "-B", str(CLI), *args], capture_output=True, text=True, cwd=str(RAIZ))
    return p.returncode, (p.stdout + p.stderr).strip().splitlines()[-1:] or [""]


reg = registro_temporal(); R = str(reg.ruta)
f = reg.ruta.parent / "pre.json"; f.write_text(json.dumps(pre()), encoding="utf-8")

# 1. el uso del docstring pone --registro detrás de la orden
rc, out = run("prerregistrar", str(f), "--registro", R, "--autor", "qa")
caso("«prerregistrar <f> --registro R» (como dice el uso del docstring) funciona", rc == 0, f"rc={rc} · {out[0][:110]}")
rc, out = run("verificar", "--registro", R)
caso("«verificar --registro R» (como dice el uso) funciona", rc == 0, f"rc={rc} · {out[0][:110]}")

# 2. órdenes nominales con --registro delante
rc, out = run("--registro", R, "prerregistrar", str(f), "--autor", "qa"); exp = json.loads(lineas(reg)[-1])["exp_id"]
caso("prerregistrar con --registro delante", rc == 0 and out[0].startswith(exp), out[0][:80])
rc, out = run("--registro", R, "intento", exp)
caso("intento con la variante por defecto", rc == 0 and json.loads(lineas(reg)[-1])["variante"] == "única")

# 3. ficheros de prerregistro ausentes o malos: 2 y sin escribir
antes = reg.ruta.read_bytes()
for nombre, contenido in (("ausente", None), ("no JSON", "{hola"), ("lista", "[1,2]"), ("null", "null"), ("con BOM", "﻿" + json.dumps(pre()))):
    g = reg.ruta.parent / f"p_{abs(hash(nombre))}.json"
    if contenido is not None:
        g.write_text(contenido, encoding="utf-8")
    rc, out = run("--registro", R, "prerregistrar", str(g))
    caso(f"prerregistro {nombre}: código 2 con mensaje y sin escribir", rc == 2 and reg.ruta.read_bytes() == antes,
         f"rc={rc} · {out[0][:110]}")

# 4. --detalle raro
for det in ("{roto", "[1]", "NaN", '"texto"'):
    r2 = registro_temporal(); R2 = str(r2.ruta)
    run("--registro", R2, "prerregistrar", str(f)); e2 = json.loads(lineas(r2)[-1])["exp_id"]; run("--registro", R2, "intento", e2)
    antes2 = r2.ruta.read_bytes()
    rc, out = run("--registro", R2, "resultado", e2, "1", "peor", "--detalle", det)
    caso(f"--detalle {det}: código 2 y sin escribir", rc == 2 and r2.ruta.read_bytes() == antes2, f"rc={rc} · {out[0][:100]}")

# 5. n no entero y veredicto con espacios
rc, out = run("--registro", R, "resultado", exp, "uno", "peor")
caso("n no entero: código 2 (argparse)", rc == 2)
rc, out = run("--registro", R, "resultado", exp, "1", "todavía no se sabe")
caso("veredicto con espacios en un solo argumento", rc == 0, f"rc={rc} · {out[0][:100]}")

# 6. «verificar» y «ver» sobre un registro que no existe (¿lo han borrado entero?)
r3 = registro_temporal(); R3 = str(r3.ruta)
rc, out = run("--registro", R3, "verificar")
caso("«verificar» de un registro que no existe avisa de que no existe (no lo da por íntegro)", rc != 0 or "íntegro" not in out[0],
     f"rc={rc} · {out[0]}")
rc, out = run("--registro", R3, "ver")
caso("«ver» de un registro vacío", rc == 0 and out[0] == "]" or out[0] == "[]", out[0])
caso("ninguna orden de lectura crea el fichero", not r3.ruta.exists())
fin()
