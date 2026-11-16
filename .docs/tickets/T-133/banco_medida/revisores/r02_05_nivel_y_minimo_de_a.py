"""T-133 QA r02 · Nivel mínimo 0,90 y mínimo de fechas leído de la configuración de A (banco 0.5.0, r02 H-08).

1. `_minimo_de_a` con la configuración de A rota o rara (sin fichero, sin la clave, True, 10.5, 3): se copia el banco a un
   árbol temporal con su propia «bloque_a/11_Ejecutor/config/por_defecto.yaml» y se importa en un proceso aparte (-I).
   ¿Falla cerrado con BancoError? ¿Qué cota queda si A baja su mínimo?
2. Calibración de `diferencia` sin habilidad con lo que el banco admite: nivel 0,90 y exactamente 10 fechas por lado
   (normal, t de 3 grados y lognormal), y con 3 fechas (lo que admitiría si A bajara su mínimo a 3).
Uso: .venv/bin/python -B r02_05_nivel_y_minimo_de_a.py <carpeta de banco_medida.py> [simulaciones]"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.dont_write_bytecode = True
CARPETA = Path(sys.argv[1]).resolve()
SIMS = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
sys.path.insert(0, str(CARPETA))
import banco_medida as bm

fallos, notas = [], []


def ok(cond, msg):
    print(("OK   " if cond else "FALLO ") + msg, flush=True)
    if not cond:
        fallos.append(msg)


def nota(msg):
    print("NOTA  " + msg, flush=True)
    notas.append(msg)


TMP = Path(tempfile.mkdtemp(prefix="r02_t133_minimo_"))
print("1. configuración de A rara")
for nombre, yaml_txt in (("sin fichero", None), ("sin la clave", "evaluacion: {}\n"), ("True", "evaluacion:\n  min_conglomerados_bootstrap: true\n"),
                         ("10.5", "evaluacion:\n  min_conglomerados_bootstrap: 10.5\n"),
                         ("3", "evaluacion:\n  min_conglomerados_bootstrap: 3\n")):
    raiz = TMP / nombre.replace(" ", "_")
    (raiz / ".docs" / "scripts").mkdir(parents=True)
    shutil.copy(CARPETA / "banco_medida.py", raiz / ".docs" / "scripts")
    conf = raiz / "bloque_a" / "11_Ejecutor" / "config"
    conf.mkdir(parents=True)
    if yaml_txt is not None:
        (conf / "por_defecto.yaml").write_text(yaml_txt, encoding="utf-8")
    codigo = ("import sys; sys.path.insert(0, sys.argv[1]); import banco_medida as bm\n"
              "print('importado', bm.MIN_EFECTIVAS_MIN)\n"
              "try:\n"
              "    r = bm.diferencia([0.05, -0.01] * 2, [-0.05, 0.01] * 2, 300, 1, nivel=0.9, min_efectivas=bm.MIN_EFECTIVAS_MIN)\n"
              "    print('diferencia admite min_efectivas', bm.MIN_EFECTIVAS_MIN, r['veredicto'])\n"
              "except bm.BancoError as e:\n"
              "    print('BancoError', e)\n")
    r = subprocess.run([sys.executable, "-I", "-B", "-c", codigo, str(raiz / ".docs" / "scripts")], capture_output=True,
                       text=True, timeout=120, check=False)
    ultima = (r.stdout.strip().splitlines() or [""])[-1] if r.returncode == 0 else r.stderr.strip().splitlines()[-1]
    print(f"   {nombre}: código {r.returncode} · {ultima[:160]}")
    if r.returncode != 0:
        ok(ultima.split(":")[0].endswith("BancoError"), f"1. «{nombre}»: falla cerrado con BancoError al importar ({ultima[:100]})")
    elif nombre == "3":
        nota("1b. si A baja `evaluacion.min_conglomerados_bootstrap` a 3, el banco admite experimentos con 3 fechas por "
             "lado sin que nada lo diga (su cota sigue a la de A; ninguna prueba fija un suelo propio)")

print(f"2. calibración sin habilidad, {SIMS} simulaciones por caso, 2 selecciones por fecha con choque común")
rng = np.random.default_rng(2026)


def muestra(n, dist):
    choque = {"normal": rng.normal(0, 1, n), "t3": rng.standard_t(3, n), "lognormal": rng.lognormal(0, 1, n) - np.exp(0.5)}[dist]
    x = np.repeat(choque, 2) + rng.normal(0, 0.5, 2 * n)
    return list(x), [f"f{i}" for i in np.repeat(np.arange(n), 2)]


for n in (10, 3):
    for dist in ("normal", "t3", "lognormal"):
        firmes = 0
        for k in range(SIMS):
            a, ga = muestra(n, dist)
            b, gb = muestra(n, dist)
            d = bm.diferencia(a, b, 500, k, nivel=0.90, min_efectivas=bm.MIN_EFECTIVAS_MIN, grupos_a=ga, grupos_b=gb)
            firmes += d["veredicto"] in ("mejor", "peor") or (n < bm.MIN_EFECTIVAS_MIN and bm.veredicto(d["rango"]) in ("mejor", "peor"))
        pct = 100 * firmes / SIMS
        print(f"   n={n:2d} {dist:9s}: {pct:5.1f} % de rangos firmes (nominal 10 %)" + ("" if n >= bm.MIN_EFECTIVAS_MIN else
                                                                                       "  [con 3 fechas el banco no da veredicto hoy]"))
        if n >= bm.MIN_EFECTIVAS_MIN:
            ok(pct < 15, f"2. nivel 0,90 y {n} fechas ({dist}): {pct:.1f} % por debajo del techo del 15 % (CA-3)")
            if pct > 12:
                nota(f"2b. nivel 0,90 con {n} fechas ({dist}): {pct:.1f} % de firmes, por encima del 10 % nominal")
shutil.rmtree(TMP, ignore_errors=True)
print(f"\n{len(fallos)} fallo(s), {len(notas)} nota(s)")
for f in fallos:
    print(" - " + f)
sys.exit(1 if fallos else 0)
