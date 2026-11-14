#!/usr/bin/env python3
"""T-116 · Fase 4 del Bloque A: evidencias del Plan de pruebas V3.0 (PB-01 a PB-67).

Lee el plan (`bloque_a/09_Pruebas/Plan de pruebas del Bloque A - V3.0.md`) y el mapa verificado
(`bloque_a/11_Ejecutor/tests/mapa_plan_pruebas.json`), que dice para cada prueba del plan qué pruebas automáticas la
cubren, qué comprueban y qué no.

Uso, desde la raíz del repositorio y con el Python del `.venv`:
    .venv/bin/python .docs/scripts/evidencias_plan_a.py              comprueba el mapa (no ejecuta pruebas); 1 si hay problemas
    .venv/bin/python .docs/scripts/evidencias_plan_a.py --ejecutar   ejecuta las pruebas citadas y escribe docs/evidencias_pruebas_bloque_a.md
    .venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-07   ejecuta solo las pruebas de esa fila y enseña su resultado
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
BLOQUE = RAIZ / "bloque_a"
PLAN = BLOQUE / "09_Pruebas" / "Plan de pruebas del Bloque A - V3.0.md"
MAPA = BLOQUE / "11_Ejecutor" / "tests" / "mapa_plan_pruebas.json"
SALIDA = RAIZ / "docs" / "evidencias_pruebas_bloque_a.md"
CARPETAS = ("11_Ejecutor", "10_Herramientas")      # cada una se ejecuta desde dentro, como en su README
CON_PRUEBAS = ("AUTOMATICA", "PARCIAL")
SIN_PRUEBAS = {"PENDIENTE_API": "Pendiente API", "REQUIERE_USUARIOS": "Requiere usuarios", "DOCUMENTAL": "Revisión documental",
               "SIN_PRUEBA": "Sin prueba"}
CAMPOS = ("cobertura", "pruebas", "comprueba", "no_comprueba")


def leer_plan() -> dict[str, dict]:
    """PB-xx → título, tipo y criterio de aprobación, tal como están en el plan."""
    texto = PLAN.read_text(encoding="utf-8")
    plan = {}
    cabeceras = re.findall(r"^#+ *PB-.*$", texto, flags=re.MULTILINE)
    raras = [c for c in cabeceras if not re.fullmatch(r"### PB-\d\d · \S.*", c)]
    if raras:   # QA r01 de T-116, H-03: una prueba del plan con otra forma no se pierde en silencio
        raise SystemExit(f"el plan tiene cabeceras de prueba que no se reconocen: {raras[:5]}")
    for m in re.finditer(r"^### (PB-\d\d) · (.+?)\n(.*?)(?=^##+ |\Z)", texto, flags=re.MULTILINE | re.DOTALL):
        campos = dict(re.findall(r"^\| ([^|]+?) \| (.*?) \|$", m.group(3), flags=re.MULTILINE))
        plan[m.group(1)] = {"titulo": m.group(2).strip(), "tipo": campos.get("Tipo", ""),
                            "criterio": campos.get("Criterio de aprobación", "")}
    return plan


def leer_mapa() -> dict[str, dict]:
    return json.loads(MAPA.read_text(encoding="utf-8"))


def _pytest(carpeta: str, args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-m", "pytest", "-p", "no:cacheprovider", *args], cwd=BLOQUE / carpeta,
                          capture_output=True, text=True, check=False)


def recoger() -> set[str]:
    """Identificadores de todas las pruebas que pytest recoge, con el prefijo de su carpeta y sin parámetros."""
    nodos = set()
    for carpeta in CARPETAS:
        r = _pytest(carpeta, ["--collect-only", "-q", "tests"])
        if r.returncode != 0:
            raise SystemExit(f"pytest no pudo recoger las pruebas de {carpeta}:\n{r.stdout[-1500:]}{r.stderr[-1500:]}")
        nodos |= {f"{carpeta}/{linea.strip().split('[')[0]}" for linea in r.stdout.splitlines() if "::" in linea}
    return nodos


def comprobar(plan: dict, mapa: dict, nodos: set[str]) -> list[str]:
    """Problemas del mapa frente al plan y frente a la suite; lista vacía si está bien."""
    problemas = [f"{pb}: está en el plan y falta en el mapa" for pb in sorted(set(plan) - set(mapa))]
    problemas += [f"{pb}: está en el mapa y no en el plan" for pb in sorted(set(mapa) - set(plan))]
    problemas += [f"{pb}: el plan no da su título o su criterio de aprobación" for pb, p in sorted(plan.items())
                  if not p["titulo"].strip() or not p["criterio"].strip()]
    for pb, fila in sorted(mapa.items()):
        if set(fila) != set(CAMPOS):
            problemas.append(f"{pb}: campos {sorted(fila)}; se esperan {sorted(CAMPOS)}")
            continue
        cobertura, pruebas = fila["cobertura"], fila["pruebas"]
        if cobertura not in CON_PRUEBAS and cobertura not in SIN_PRUEBAS:
            problemas.append(f"{pb}: cobertura desconocida {cobertura!r}")
        if (cobertura in CON_PRUEBAS) != bool(pruebas):
            problemas.append(f"{pb}: {cobertura} con {len(pruebas)} pruebas citadas")
        if cobertura in CON_PRUEBAS and not fila["comprueba"].strip():
            problemas.append(f"{pb}: falta decir qué comprueban sus pruebas")
        if cobertura != "AUTOMATICA" and not fila["no_comprueba"].strip():
            problemas.append(f"{pb}: {cobertura} sin decir qué queda sin comprobar")
        if len(set(pruebas)) != len(pruebas):
            problemas.append(f"{pb}: pruebas repetidas")
        problemas += [f"{pb}: la prueba citada no existe: {n}" for n in pruebas if n not in nodos]
    return problemas


def ejecutar(nodos: list[str]) -> dict[str, str]:
    """Ejecuta las pruebas citadas, cada carpeta desde dentro. Nodo → SUPERADA, FALLA o NO EJECUTADA."""
    resultado = {}
    for carpeta in CARPETAS:
        propios = sorted({n[len(carpeta) + 1:] for n in nodos if n.startswith(carpeta + "/")})
        if not propios:
            continue
        with tempfile.TemporaryDirectory() as tmp:
            informe = Path(tmp) / "junit.xml"
            # QA r01 de T-116, H-02: `--runxfail` hace que una prueba marcada como fallo esperado cuente por lo que hace
            _pytest(carpeta, ["-q", "--runxfail", f"--junitxml={informe}", "-o", "junit_family=xunit1", *propios])
            casos: dict[str, list[str]] = {}
            if informe.is_file():
                for caso in ET.parse(informe).getroot().iter("testcase"):
                    estado = "FALLA" if caso.find("failure") is not None or caso.find("error") is not None else (
                        "NO EJECUTADA" if caso.find("skipped") is not None else "SUPERADA")
                    fichero = caso.get("file") or caso.get("classname", "").replace(".", "/") + ".py"
                    nombre = caso.get("name", "").split("[")[0]
                    casos.setdefault(f"{fichero}::{nombre}", []).append(estado)
        for n in propios:
            fichero, nombre = n.split("::")[0], n.split("::")[-1]
            estados = casos.get(f"{fichero}::{nombre}", [])
            resultado[f"{carpeta}/{n}"] = ("NO EJECUTADA" if not estados else "FALLA" if "FALLA" in estados else
                                           "NO EJECUTADA" if "NO EJECUTADA" in estados else "SUPERADA")
    return resultado


def resultado_fila(fila: dict, resultados: dict[str, str]) -> str:
    if fila["cobertura"] in SIN_PRUEBAS:
        return SIN_PRUEBAS[fila["cobertura"]]
    estados = [resultados.get(n, "NO EJECUTADA") for n in fila["pruebas"]]
    if "FALLA" in estados:
        return "FALLA"
    if "NO EJECUTADA" in estados:
        return "No ejecutada"
    return "Superada" if fila["cobertura"] == "AUTOMATICA" else "Superada en parte"


def orden(fila: dict) -> list[str]:
    """Órdenes para repetir la fila, una por carpeta."""
    salida = []
    for carpeta in CARPETAS:
        propios = [n[len(carpeta) + 1:] for n in fila["pruebas"] if n.startswith(carpeta + "/")]
        if propios:
            salida.append(f"(cd bloque_a/{carpeta} && ../../.venv/bin/python -m pytest -q " + " ".join(f"'{n}'" for n in propios) + ")")
    return salida


def documento(plan: dict, mapa: dict, resultados: dict[str, str], fecha: str, commit: str) -> str:
    filas = {pb: resultado_fila(mapa[pb], resultados) for pb in sorted(mapa)}
    cuenta: dict[str, int] = {}
    for r in filas.values():
        cuenta[r] = cuenta.get(r, 0) + 1
    lineas = ["# Evidencias del Plan de pruebas del Bloque A (Fase 4, T-116)", "",
              (f"Generado por `.docs/scripts/evidencias_plan_a.py --ejecutar` el {fecha} sobre el commit `{commit}`, con el cliente "
              "simulado (`MockClient`): sin red, sin clave y sin coste. No se edita a mano: se regenera."), "",
              "Qué significa cada resultado:", "",
              ("- **Superada:** las pruebas citadas pasan y comprueban todo el criterio de aprobación del plan, salvo lo que solo "
              "existe con tiempo real o con el modelo real, que se dice en «No comprueba»."),
              ("- **Superada en parte:** las pruebas citadas pasan, pero queda alguna cláusula del criterio que el ejecutor podría "
              "comprobar y ninguna prueba comprueba. Está en «No comprueba»."),
              "- **Pendiente API:** el criterio lo juzga el modelo real; no se ejecuta en esta fase.",
              "- **Requiere usuarios**, **Revisión documental:** no son pruebas del ejecutor.",
              "- **Sin prueba:** ninguna prueba automática cubre el caso.",
              "- **FALLA**, **No ejecutada:** alguna prueba citada falla o no se pudo ejecutar.", "",
              ("Con el cliente simulado se valida la tubería (canales, archivos, puertas, herramientas, cálculos), no la calidad "
              "analítica de los agentes (R22)."), "", "## Resumen", "", "| Resultado | Pruebas del plan |", "| --- | --- |"]
    lineas += [f"| {r} | {n} |" for r, n in sorted(cuenta.items(), key=lambda x: (-x[1], x[0]))]
    lineas += [f"| **Total** | **{len(filas)}** |", "", "## Tabla", "", "| Prueba | Resultado | Comprueba | No comprueba |",
               "| --- | --- | --- | --- |"]
    for pb in sorted(mapa):
        fila = mapa[pb]
        lineas.append(f"| {pb} {plan[pb]['titulo']} | {filas[pb]} | {fila['comprueba'] or '—'} | {fila['no_comprueba'] or '—'} |")
    lineas += ["", "## Cómo repetir cada fila", "",
               "Desde la raíz del repositorio. También: `.venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-NN`.", ""]
    for pb in sorted(mapa):
        fila = mapa[pb]
        if not fila["pruebas"]:
            continue
        lineas += [f"### {pb} · {plan[pb]['titulo']}", "", f"Criterio de aprobación del plan: {plan[pb]['criterio']}", "", "```bash",
                   *orden(fila), "```", ""]
        lineas += [f"- `{n}`: {resultados.get(n, 'NO EJECUTADA')}" for n in fila["pruebas"]] + [""]
    return "\n".join(lineas).rstrip("\n") + "\n"


def filas_del_documento(texto: str) -> dict[str, tuple[str, str, str]]:
    """PB-xx → (resultado, comprueba, no comprueba) de la tabla del documento de evidencias."""
    filas = {}
    for linea in texto.splitlines():
        m = re.fullmatch(r"\| (PB-\d\d) .*? \| ([^|]+) \| ([^|]*) \| ([^|]*) \|", linea)
        if m:
            filas[m.group(1)] = (m.group(2).strip(), m.group(3).strip(), m.group(4).strip())
    return filas


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Evidencias del Plan de pruebas del Bloque A (T-116).")
    ap.add_argument("--ejecutar", action="store_true", help="ejecuta las pruebas citadas y escribe el documento de evidencias")
    ap.add_argument("--pb", help="ejecuta solo las pruebas de una fila (PB-NN) y enseña su resultado")
    args = ap.parse_args(argv)
    plan, mapa = leer_plan(), leer_mapa()
    problemas = comprobar(plan, mapa, recoger())
    for p in problemas:
        print("PROBLEMA · " + p, file=sys.stderr)
    if problemas:
        print(f"mapa del plan de pruebas: {len(problemas)} problemas")
        return 1
    cuenta: dict[str, int] = {}
    for fila in mapa.values():
        cuenta[fila["cobertura"]] = cuenta.get(fila["cobertura"], 0) + 1
    print(f"mapa del plan de pruebas: {len(mapa)} pruebas del plan, {len({n for f in mapa.values() for n in f['pruebas']})} "
          "pruebas automáticas citadas y todas existen · " + ", ".join(f"{k} {v}" for k, v in sorted(cuenta.items())))
    if args.pb:
        if args.pb not in mapa:
            print(f"{args.pb} no está en el plan", file=sys.stderr)
            return 1
        resultados = ejecutar(mapa[args.pb]["pruebas"])
        for n in mapa[args.pb]["pruebas"]:
            print(f"{resultados.get(n, 'NO EJECUTADA'):<13} {n}")
        print(f"{args.pb} {plan[args.pb]['titulo']}: {resultado_fila(mapa[args.pb], resultados)}")
        superadas = all(resultados.get(n) == "SUPERADA" for n in mapa[args.pb]["pruebas"])
        return 0 if superadas else 1   # H-02: una prueba citada que falla o no se ejecuta no da un 0
    if args.ejecutar:
        import datetime as dt
        resultados = ejecutar(sorted({n for f in mapa.values() for n in f["pruebas"]}))
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=RAIZ, capture_output=True, text=True, check=False).stdout.strip()
        SALIDA.write_text(documento(plan, mapa, resultados, dt.date.today().isoformat(), commit or "sin commit"), encoding="utf-8")
        fallan = sorted(n for n, r in resultados.items() if r != "SUPERADA")
        for n in fallan:
            print(f"{resultados[n]} · {n}", file=sys.stderr)
        print(f"escrito {SALIDA.relative_to(RAIZ)} · {len(resultados) - len(fallan)} de {len(resultados)} pruebas citadas superadas")
        return 1 if fallan else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
