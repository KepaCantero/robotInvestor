"""QA r01 de T-124 · ¿El re-congelado de los goldens solo cambia lo que dice su motivo?

1. `formas_flujos_mock.json` antes (d1ff926) y después (HEAD): por flujo y contrato, qué rutas entran, salen, cambian de
   tipo o pasan de «a veces» a «siempre» (H-08) y al revés. En los ocho flujos que T-124 no toca, lo único admisible es el
   paso «a veces» → «siempre» de rutas con clave genérica («<…>»), sin cambios de tipo ni rutas perdidas.
2. `aceptaciones_rechazos.json`: los casos de antes siguen con el mismo resultado; los nuevos son los ocho de la batería.
3. Con `--copia <copia desechable>` (ruta con «qa8_mut»): se pone en la copia el código de producción de d1ff926 (antes de
   T-123 r02, T-125, T-126 y T-127) con los goldens y `goldens_ct.py` de HEAD y se ejecuta `goldens_ct.py`: si coincide, el
   re-congelado no esconde ningún cambio de lo que emite el ejecutor. La copia se restaura al acabar (git checkout).

Uso, desde la raíz:  python .docs/tickets/T-124/revisores/r01_01_que_cambia_el_recongelado.py [--copia <copia>]
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
G = "bloque_a/11_Ejecutor/tests/goldens/"
PY = "/home/user/robotinvestor/.venv/bin/python"
ANTES = "d1ff926"
fallos: list[str] = []


def git_json(rev: str, ruta: str) -> dict:
    return json.loads(subprocess.run(["git", "-C", str(RAIZ), "show", f"{rev}:{ruta}"], capture_output=True, text=True,
                                     check=True).stdout)


def comprobar(nombre: str, ok: bool, detalle: str = "") -> None:
    print(f"  {'ok   ' if ok else 'FALLA'} {nombre} {detalle if not ok else ''}")
    if not ok:
        fallos.append(nombre)


print("[1] formas de los flujos")
a, d = git_json(ANTES, G + "formas_flujos_mock.json"), json.loads((RAIZ / G / "formas_flujos_mock.json").read_text())
TOCADOS = {"consulta_que_escala", "peticion_ad_hoc", "informe_de_aprendizaje"}
for flujo in sorted(set(a["flujos"]) | set(d["flujos"])):
    fa, fd = a["flujos"].get(flujo, {}).get("mensajes", {}), d["flujos"].get(flujo, {}).get("mensajes", {})
    raros = []
    for ct in sorted(set(fa) | set(fd)):
        if ct not in fd:
            raros.append(f"{ct} desaparece")
            continue
        if ct not in fa:
            if flujo not in TOCADOS:
                raros.append(f"{ct} nuevo")
            continue
        sa = {**{k: ("s", v) for k, v in fa[ct].get("rutas_siempre", {}).items()}, **{k: ("v", v) for k, v in fa[ct].get("rutas_a_veces", {}).items()}}
        sd = {**{k: ("s", v) for k, v in fd[ct].get("rutas_siempre", {}).items()}, **{k: ("v", v) for k, v in fd[ct].get("rutas_a_veces", {}).items()}}
        for r in sorted(set(sa) | set(sd)):
            if r not in sd:
                raros.append(f"{ct} pierde {r}")
            elif r not in sa:
                if flujo not in TOCADOS:
                    raros.append(f"{ct} gana {r}")
            elif sa[r][1] != sd[r][1]:
                if flujo not in TOCADOS:
                    raros.append(f"{ct} {r}: tipo {sa[r][1]} → {sd[r][1]}")
            elif sa[r][0] != sd[r][0]:
                h08 = sa[r][0] == "v" and sd[r][0] == "s" and "<" in r
                if not h08 and flujo not in TOCADOS:
                    raros.append(f"{ct} {r}: {sa[r][0]} → {sd[r][0]}")
        for campo in ("emisores", "receptores"):
            if fa[ct].get(campo) != fd[ct].get(campo) and flujo not in TOCADOS:
                raros.append(f"{ct} {campo} {fa[ct].get(campo)} → {fd[ct].get(campo)}")
    nuevos = sorted(set(fd) - set(fa))
    print(f"    {flujo:24s} contratos {len(fa):2d} → {len(fd):2d}  nuevos: {nuevos if flujo in TOCADOS else '-'}")
    comprobar(f"{flujo}: solo cambia lo que dice el motivo", not raros, str(raros[:6]))

print("[2] aceptaciones y rechazos")
aa, ad = git_json(ANTES, G + "aceptaciones_rechazos.json"), json.loads((RAIZ / G / "aceptaciones_rechazos.json").read_text())


def casos(x):
    if isinstance(x, dict) and "casos" in x:
        x = x["casos"]
    return x if isinstance(x, dict) else {str(i): c for i, c in enumerate(x)}


ca, cd = casos(aa), casos(ad)
cambiados = [k for k in ca if k in cd and ca[k] != cd[k]]
perdidos = [k for k in ca if k not in cd]
nuevos = [k for k in cd if k not in ca]
print(f"    casos {len(ca)} → {len(cd)}; nuevos: {nuevos}")
comprobar("ningún caso de antes cambia ni se pierde", not cambiados and not perdidos, f"{cambiados[:5]} {perdidos[:5]}")
comprobar("los nuevos son ocho", len(nuevos) == 8, str(len(nuevos)))

if "--copia" in sys.argv:
    copia = Path(sys.argv[sys.argv.index("--copia") + 1]).resolve()
    assert "qa8_mut" in str(copia), "solo en una copia desechable"
    print(f"[3] código de producción de {ANTES} con los goldens de HEAD, en {copia}")
    pkg = "bloque_a/11_Ejecutor/bloque_a"
    subprocess.run(["git", "-C", str(copia), "checkout", "-q", ANTES, "--", pkg], check=True)
    try:
        r = subprocess.run([PY, "tests/goldens_ct.py"], cwd=copia / "bloque_a/11_Ejecutor", capture_output=True, text=True)
        print("    " + (r.stdout + r.stderr).strip().replace("\n", "\n    ")[:1500])
        comprobar("con el código de antes, los goldens de HEAD coinciden", r.returncode == 0, f"código {r.returncode}")
    finally:
        subprocess.run(["git", "-C", str(copia), "checkout", "-q", "HEAD", "--", pkg], check=True)
        st = subprocess.run(["git", "-C", str(copia), "status", "--short"], capture_output=True, text=True).stdout
        print(f"    copia restaurada; git status: {st.strip() or 'limpio'}")

print(f"== r01_01 T-124: {'sin fallos' if not fallos else 'fallos: ' + ', '.join(fallos)}")
sys.exit(1 if fallos else 0)
