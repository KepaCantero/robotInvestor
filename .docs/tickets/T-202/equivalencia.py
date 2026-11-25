"""T-202 · prueba de equivalencia: las salidas del ejecutor del Bloque A son las mismas en develop y en la rama.

Los tickets de cuotas no deben cambiar ningún comportamiento, así que en lugar de mutantes de lógica se deja esta
comparación. Ejecuta en las dos copias, cada una con su Python (el de develop con su entorno y el de la rama con el suyo,
con los stubs), lo mismo:

1. un ciclo C1 simulado (`--cliente mock`, `--as-of 2026-06-05`) y una consulta CT-03 sobre ese estado;
2. el backtest del README de `bloque_a/11_Ejecutor` (2024-01-05 a 2024-03-29);
3. una petición CT-01 (`ejemplos/peticiones/peticion_ad_hoc.json`);
4. las fichas cuyo código cambia (ST-INF-001 con wilcoxon y mann_whitney en las tres alternativas, ALT-DESMOOTH-001 GLM
   con k = 1, 2, 3, DER-SKEW-001 SVI) y todos los casos de control de sus tres módulos (fichas_series, fichas_reales,
   fichas_fon_der), con los resultados en JSON con `repr` de cada número, para ver hasta el último bit.

Los dos lados se ejecutan en la MISMA carpeta (`<trabajo>/en_curso`, que después se renombra a `develop` o `rama`):
F5 guarda las rutas de las salidas y su cadena de huellas depende de ellas, así que con otra carpeta todo F5 diferiría.
Después compara byte a byte cada fichero que dejan (salidas y estado F1–F11, HA, acuses…) y la salida de cada orden. Solo
se normalizan la ruta de cada copia y las latencias medidas con el reloj, que cambian de una ejecución a otra en la misma
copia: `"latencia_s": <número>` en JSON y la columna `latencia_s` de `consumo.csv`. Una base SQLite (los acuses de la
mensajería) se compara por su volcado SQL (`iterdump`), con la misma normalización. Con `--normalizar` se puede añadir otra
expresión. Termina con 0 si todo es igual y 1 si algo difiere, con la lista.

Uso (desde cualquier carpeta; `--trabajo` fuera del repositorio):
  python3 equivalencia.py --base <copia de develop> --base-python <python de develop> \
      --nuevo <copia de la rama> --nuevo-python <python de la rama> --trabajo <carpeta temporal>
"""
from __future__ import annotations

import argparse
import filecmp
import os
import re
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

COMUNES = ["--cliente", "mock", "--datos", "ejemplos/datos_sinteticos", "--universo", "config/universo_ejemplo.csv"]
CONSULTA = "¿Por qué no aparece la renta fija esta semana?"

FICHAS = r'''
import copy, json, sys
from bloque_a.motor import fichas_fon_der as D, fichas_reales as R, fichas_series as S

def correr(mod, ficha, valores, params):
    ent = {"valores": copy.deepcopy(valores), "series": {}, "series_rol": {}}
    try:
        return {"ok": mod.FICHAS[ficha]["fn"](ent, dict(params))}
    except Exception as e:   # la comparación también cubre los rechazos: mismo tipo y mismo texto
        return {"error": type(e).__name__ + ": " + str(e)}

out = {"modulos": [m.__file__ for m in (S, R, D)], "bateria": {}, "control": {}}
b = out["bateria"]
muestras = {"una": {"muestra": [0.5, 1.1, 0.3, 2.0, 0.9, -0.4, 1.7, -0.2]},
            "pareada": {"muestra_a": [1.0, 2.5, 3.1, 4.8, 5.0, 2.2, 3.3], "muestra_b": [0.8, 2.0, 3.5, 4.1, 4.2, 2.9, 1.0]}}
for alt in ("bilateral", "mayor", "menor"):
    for nombre, m in muestras.items():
        b[f"ST-INF-001/wilcoxon/{nombre}/{alt}"] = correr(S, "ST-INF-001", {"contrastes": [dict(nombre="w", **m)]},
                                                         {"tipo_contraste": "wilcoxon", "alternativa": alt})
    b[f"ST-INF-001/mann_whitney/{alt}"] = correr(
        S, "ST-INF-001", {"contrastes": [{"nombre": "u", "muestra_a": [1.2, 3.4, 2.2, 5.1, 0.7, 2.9],
                                          "muestra_b": [2.0, 4.1, 3.3, 6.2, 1.9, 3.8, 4.4]}]},
        {"tipo_contraste": "mann_whitney", "alternativa": alt})
for k in (1, 2, 3):
    b[f"ALT-DESMOOTH-001/GLM/k={k}"] = correr(R, "ALT-DESMOOTH-001", R._datos_alt(R._AD_OBS_GLM), {"metodo": "GLM", "k": k})
b["DER-SKEW-001/SVI"] = correr(D, "DER-SKEW-001", D._ctl_skew_svi(), {"metodo": "SVI"})
for mod in (S, R, D):
    for ficha, casos in sorted(mod.CASOS_CONTROL.items()):
        for i, caso in enumerate(casos):
            valores = {}
            for d in caso["datos"]:
                valores.update(copy.deepcopy(d["valores"]))
            out["control"][f"{ficha}/{i}"] = correr(mod, ficha, valores, caso.get("parametros") or {})
json.dump(out, sys.stdout, ensure_ascii=False, sort_keys=True, indent=1, default=repr)
'''


def ordenes(trabajo: Path) -> list[tuple[str, list[str]]]:
    t = str(trabajo)
    return [
        ("ciclo", [*COMUNES, "--estado", f"{t}/est_ciclo", "--salida", f"{t}/ciclo", "--as-of", "2026-06-05", "ciclo"]),
        ("consulta", [*COMUNES, "--estado", f"{t}/est_ciclo", "--salida", f"{t}/ciclo", "--as-of", "2026-06-05",
                      "consulta", CONSULTA]),
        ("backtest", [*COMUNES, "--estado", f"{t}/est_bt", "--salida", f"{t}/bt", "backtest", "--desde", "2024-01-05",
                      "--hasta", "2024-03-29"]),
        ("peticion", [*COMUNES, "--estado", f"{t}/est_pet", "--salida", f"{t}/pet", "--as-of", "2026-06-05",
                      "peticion", "--json", "ejemplos/peticiones/peticion_ad_hoc.json"]),
    ]


def ejecutar(nombre: str, repo: Path, python: str, trabajo: Path, destino: Path) -> None:
    ejecutor = repo / "bloque_a" / "11_Ejecutor"
    for d in (trabajo, destino):
        if d.exists():
            shutil.rmtree(d)
    trabajo.mkdir(parents=True)
    env = {**os.environ, "PYTHONPATH": str(ejecutor), "PYTHONHASHSEED": "0"}
    for orden, args in ordenes(trabajo):
        r = subprocess.run([python, "-m", "bloque_a.cli", *args], cwd=ejecutor, env=env, capture_output=True, check=False)
        (trabajo / f"{orden}.salida").write_bytes(r.stdout)
        (trabajo / f"{orden}.errores").write_bytes(r.stderr)
        (trabajo / f"{orden}.codigo").write_text(str(r.returncode), encoding="utf-8")
        print(f"{nombre} {orden}: código {r.returncode}")
    r = subprocess.run([python, "-c", FICHAS], cwd=ejecutor, env=env, capture_output=True, check=False)
    (trabajo / "fichas.json").write_bytes(r.stdout)
    (trabajo / "fichas.errores").write_bytes(r.stderr)
    (trabajo / "fichas.codigo").write_text(str(r.returncode), encoding="utf-8")
    print(f"{nombre} fichas: código {r.returncode}")
    trabajo.rename(destino)


def normalizar(texto: bytes, nombre: str, repo: Path, extra: list[str]) -> bytes:
    t = texto
    for ruta in sorted({str(repo.resolve()), str(repo)}, key=len, reverse=True):
        # solo la ruta entera: la del trabajo puede empezar igual («…/t202» y «…/t202_med»)
        t = re.sub(re.escape(ruta).encode() + rb"(?![\w.-])", b"<REPO>", t)
    t = re.sub(rb'"latencia_s": [0-9.eE+-]+', b'"latencia_s": <LATENCIA>', t)
    if nombre == "consumo.csv":   # la última columna es latencia_s (se comprueba en la cabecera)
        lineas = t.split(b"\n")
        if lineas and lineas[0].rstrip(b"\r").split(b",")[-1] == b"latencia_s":
            t = b"\n".join([lineas[0]] + [re.sub(rb",[^,]*$", b",<LATENCIA>", x) if x else x for x in lineas[1:]])
    for patron in extra:
        t = re.sub(patron.encode(), b"<NORMALIZADO>", t)
    return t


def leer(p: Path) -> bytes:
    if p.suffix == ".sqlite3":
        con = sqlite3.connect(f"file:{p}?mode=ro", uri=True)
        try:
            return "\n".join(con.iterdump()).encode()
        finally:
            con.close()
    return p.read_bytes()


def comparar(tb: Path, rb: Path, tn: Path, rn: Path, extra: list[str]) -> list[str]:
    difs = []
    lb = sorted(p.relative_to(tb) for p in tb.rglob("*") if p.is_file())
    ln = sorted(p.relative_to(tn) for p in tn.rglob("*") if p.is_file())
    for p in sorted(set(lb) ^ set(ln)):
        difs.append(f"solo en {'develop' if p in lb else 'la rama'}: {p}")
    iguales = 0
    for p in sorted(set(lb) & set(ln)):
        if filecmp.cmp(tb / p, tn / p, shallow=False):
            iguales += 1
            continue
        a = normalizar(leer(tb / p), p.name, rb, extra)
        b = normalizar(leer(tn / p), p.name, rn, extra)
        if a == b:
            iguales += 1
        else:
            difs.append(f"distinto: {p}")
    print(f"{iguales} ficheros iguales (byte a byte o tras normalizar la ruta de la copia y las latencias), "
          f"{len(difs)} diferencias")
    return difs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", type=Path, required=True)
    ap.add_argument("--base-python", required=True)
    ap.add_argument("--nuevo", type=Path, required=True)
    ap.add_argument("--nuevo-python", required=True)
    ap.add_argument("--trabajo", type=Path, required=True)
    ap.add_argument("--normalizar", action="append", default=[], help="expresión regular que se sustituye en los dos")
    a = ap.parse_args()
    trabajo = a.trabajo.resolve()
    for repo in (a.base, a.nuevo):
        if trabajo.is_relative_to(repo.resolve()):
            sys.exit("--trabajo tiene que estar fuera de las copias")
    tb, tn, en_curso = trabajo / "develop", trabajo / "rama", trabajo / "en_curso"
    ejecutar("develop", a.base, a.base_python, en_curso, tb)
    ejecutar("rama", a.nuevo, a.nuevo_python, en_curso, tn)
    for lado, t, repo in (("develop", tb, a.base), ("rama", tn, a.nuevo)):
        modulos = (t / "fichas.json").read_text(encoding="utf-8")
        if str((repo / "bloque_a" / "11_Ejecutor").resolve()) not in modulos:
            sys.exit(f"{lado}: las fichas no se cargaron de su copia (mira PYTHONPATH)")
    difs = comparar(tb, a.base, tn, a.nuevo, a.normalizar)
    for d in difs:
        print("  " + d)
    return 1 if difs else 0


if __name__ == "__main__":
    sys.exit(main())
