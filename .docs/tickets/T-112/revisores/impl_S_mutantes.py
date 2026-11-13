"""T-112 · grupo S · mutantes de las fórmulas principales de `motor/fichas_series.py`.

Cada mutante cambia una línea de la fórmula principal (o de una regla de rechazo) de una ficha del grupo S y se mide si
lo cazan (CC) los casos de control de la ficha, ejecutados como `Motor.verificar_casos_control` (dos pasadas, que deben
coincidir, y la comprobación), y (T) las pruebas de la ficha en `tests/test_fase2_series.py`.

Trabaja sobre una copia de `bloque_a` entero (sin `*.docx` ni cachés) en el directorio que se le pase, nunca sobre el
árbol del repositorio: así el ejecutor copiado encuentra el Catálogo en su propia raíz, como en el repositorio.

Uso: .venv/bin/python -I -B .docs/tickets/T-112/revisores/impl_S_mutantes.py DIRECTORIO_DE_TRABAJO [--solo ID[,ID…]] [-j N]
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
PY = str(RAIZ / ".venv" / "bin" / "python")
MODULO = Path("bloque_a") / "motor" / "fichas_series.py"
PRUEBAS = "tests/test_fase2_series.py"

# Palabras de -k de pytest por ficha (ids parametrizados con el identificador y pruebas propias con su prefijo).
CLAVE = {"ST-INF-001": "ST-INF-001 or st_inf", "FX-BRK-001": "FX-BRK-001 or fx_brk", "FX-STL-001": "FX-STL-001 or fx_stl",
         "FX-REGIME-001": "FX-REGIME-001 or fx_regime", "REG-HMM-001": "REG-HMM-001 or reg_hmm",
         "FX-COINT-001": "FX-COINT-001 or fx_coint", "BIB-MET-001": "BIB-MET-001 or bib_met",
         "TEM-DIFF-001": "TEM-DIFF-001 or tem_diff"}

# (id, ficha, [(texto original, texto mutado)], descripción)
MUTANTES: list[tuple[str, str, list[tuple[str, str]], str]] = [
    # ------------------------------------------------------------------ ST-INF-001
    ("S01", "ST-INF-001", [("        t = (media - mu0) / ee\n", "        t = (media - mu0) / sd\n")],
     "t con la desviación en lugar del error estándar"),
    ("S02", "ST-INF-001", [("        c = float(stats.t.ppf(1 - nivel / 2, gl))\n", "        c = float(stats.t.ppf(1 - nivel, gl))\n")],
     "IC bilateral con el cuantil unilateral"),
    ("S03", "ST-INF-001", [("        acumulado = max(acumulado, min(1.0, (m - j) * pv[i]))", "        acumulado = max(acumulado, min(1.0, m * pv[i]))")],
     "Holm sustituido por Bonferroni"),
    ("S04", "ST-INF-001", [("        acumulado = min(acumulado, m * pv[i] / (j + 1))", "        acumulado = min(acumulado, m * pv[i] / (j + 2))")],
     "Benjamini-Hochberg con el rango desplazado"),
    ("S05", "ST-INF-001", [("        gl = (v1 + v2) ** 2 / ((v1 ** 2 / (n1 - 1) if v1 else 0.0) + (v2 ** 2 / (n2 - 1) if v2 else 0.0))",
                            "        gl = n1 + n2 - 2")], "Welch con los grados de libertad de varianzas iguales"),
    ("S06", "ST-INF-001", [('        metodo = "holm" if p["correccion"] in ("auto", "holm") else "bh"',
                            '        metodo = "holm" if p["correccion"] == "holm" else "bh"')], "auto ⇒ BH en lugar de Holm"),
    ("S07", "ST-INF-001", [('        return float(2 * stats.t.sf(abs(t), gl))', '        return float(stats.t.sf(abs(t), gl))')],
     "p bilateral sin duplicar"),
    ("S08", "ST-INF-001", [("    fijos = set(params) & set(UMBRALES[F])\n", "    fijos = set()\n")],
     "la petición vuelve a cambiar umbrales (todas las fichas)"),
    ("S09", "ST-INF-001", [('    desconocidos = set(params) - set(PARAMETROS_POR_DEFECTO[F]) - {"clase"}',
                            '    desconocidos = set()')], "parámetros desconocidos aceptados en silencio"),
    ("S10", "ST-INF-001", [("            if malos:\n                raise ErrorFicha", "            if False:\n                raise ErrorFicha")],
     "se sirven cifras no finitas"),
    # ------------------------------------------------------------------ FX-BRK-001
    ("B01", "FX-BRK-001", [("            b = dosll + k_par * math.log(n)", "            b = dosll + k_par * 2")],
     "AIC en lugar de BIC"),
    ("B02", "FX-BRK-001", [('        h = max(math.ceil(p["recorte"] * n), q[tipo] + 1)', '        h = q[tipo] + 1')],
     "sin recorte de segmentos"),
    ("B03", "FX-BRK-001", [("            C = syy - sy ** 2 / largo\n", "            C = syy - sy ** 2 / (largo + 1)\n")],
     "SSR de la media mal calculada"),
    ("B04", "FX-BRK-001", [("            anchura = math.floor(c_bai * s2 / delta ** 2) + 1", "            anchura = math.floor(c_bai * s2 / abs(delta)) + 1")],
     "IC de Bai con δ en lugar de δ²"),
    ("B05", "FX-BRK-001", [("    S = np.cumsum(s - s.mean())[:-1] / (sd * math.sqrt(n))", "    S = np.cumsum(s - s.mean())[:-1] / (sd * n)")],
     "CUSUM mal normalizado"),
    ("B06", "FX-BRK-001", [('    if n < p["obs_una_ruptura"]:', '    if n < 10:')], "mínimo de 30 observaciones quitado"),
    ("B07", "FX-BRK-001", [('    if M > 1 and n < p["obs_varias_rupturas"]:', '    if False:')], "mínimo de 50 para varias rupturas quitado"),
    ("B08", "FX-BRK-001", [("        + 1.5 * math.exp(x + float(stats.norm.logcdf(-1.5 * r))))", "        - 1.5 * math.exp(x + float(stats.norm.logcdf(-1.5 * r))))")],
     "CDF de Bai con el signo cambiado"),
    # ------------------------------------------------------------------ FX-STL-001
    ("L01", "FX-STL-001", [('            L = np.convolve(L, np.ones(3) / 3, "valid")', '            L = np.convolve(L, np.ones(3) / 2.9, "valid")')],
     "media móvil de 3 del filtro de paso bajo mal normalizada"),
    ("L02", "FX-STL-001", [("            S = C[np_: np_ + n] - L\n", "            S = C[np_: np_ + n]\n")],
     "estacional sin restar el paso bajo"),
    ("L03", "FX-STL-001", [("    w = np.where(u < 1, (1 - u ** 3) ** 3, 0.0)", "    w = np.where(u < 1, (1 - u ** 2) ** 3, 0.0)")],
     "pesos del LOESS no tricúbicos"),
    ("L04", "FX-STL-001", [('            esquema = "multiplicativo" if rel_m < rel_a else "aditivo"', '            esquema = "multiplicativo" if rel_m > rel_a else "aditivo"')],
     "criterio del esquema invertido"),
    ("L05", "FX-STL-001", [('    if ciclos < p["ciclos_minimos"]:', '    if ciclos < 1:')], "mínimo de 2 ciclos quitado"),
    ("L06", "FX-STL-001", [("        ajustada = y - S\n", "        ajustada = y - T\n")], "serie ajustada mal calculada"),
    # ------------------------------------------------------------------ FX-REGIME-001 y REG-HMM-001
    ("H01", "FX-REGIME-001", [("    cuenta = xi.sum(1)\n", "    cuenta = np.swapaxes(xi.sum(1), -1, -2)\n")],
     "matriz de transición traspuesta en el paso M"),
    ("H02", "FX-REGIME-001", [("            cov_n = np.where(hay[..., None], Sk / Nk_s[..., None], cov)",
                               "            cov_n = np.where(hay[..., None], Sk / (Nk_s[..., None] + 1), cov)")],
     "varianza del paso M sesgada"),
    ("H03", "FX-REGIME-001", [("    return -0.5 * (d * math.log(2 * math.pi) + logdet[:, None, :] + maha)",
                               "    return -0.5 * (d * math.log(2 * math.pi) + logdet[:, None, :] + 2 * maha)")],
     "densidad de emisión mal escrita"),
    ("H04", "FX-REGIME-001", [('        clave = aj["cov"][:, 0] if p["varianzas_distintas"] else aj["mu"][:, 0]',
                               '        clave = -aj["cov"][:, 0] if p["varianzas_distintas"] else aj["mu"][:, 0]')],
     "etiquetado por varianza invertido"),
    ("H05", "FX-REGIME-001", [('    n_par = (k - 1) + k * (k - 1) + (k if p["medias_distintas"] else 1) + (k if p["varianzas_distintas"] else 1)',
                               '    n_par = k * (k - 1) + (k if p["medias_distintas"] else 1) + (k if p["varianzas_distintas"] else 1)')],
     "BIC sin los parámetros de la distribución inicial"),
    ("H06", "FX-REGIME-001", [('    if n < p["obs_minimas"]:\n        raise ErrorFicha(f"{F}: {n} observaciones (< {p[\'obs_minimas\']})")\n    if n < p["obs_recomendadas"]:',
                               '    if False:\n        raise ErrorFicha(f"{F}: {n} observaciones (< {p[\'obs_minimas\']})")\n    if n < p["obs_recomendadas"]:')],
     "mínimo de 100 observaciones quitado"),
    ("H07", "FX-REGIME-001", [("        xi = filtradas[:, :-1, :, None] * M * beta[:, 1:, None, :]",
                               "        xi = filtradas[:, :-1, :, None] * M * beta[:, :-1, None, :]")],
     "ξ con β desfasada"),
    ("H08", "REG-HMM-001", [("    Z = (X - media) / sd\n", "    Z = X - media\n")], "variables sin estandarizar"),
    ("H09", "REG-HMM-001", [("    k = min(bics, key=lambda x: (bics[x], x))", "    k = max(bics, key=lambda x: (bics[x], x))")],
     "número de estados por el peor BIC"),
    ("H10", "REG-HMM-001", [('        return _ordenar(aj, aj["mu"][:, 0])', '        return _ordenar(aj, -aj["mu"][:, 0])')],
     "etiquetas por medias invertidas"),
    ("H11", "REG-HMM-001", [("        cov_n = cov_n + np.diag(suelo)[None, None]", "        cov_n = cov_n + 10 * np.diag(suelo)[None, None] + 0.01")],
     "regularización de la covarianza completa inflada"),
    # ------------------------------------------------------------------ FX-COINT-001
    ("C01", "FX-COINT-001", [("    traza = [float(-T * np.sum(np.log(1 - lam[r:]))) for r in range(q)]",
                              "    traza = [float(-T * np.sum(np.log(1 - lam[r + 1:]))) for r in range(q)]")],
     "traza sin el autovalor r + 1"),
    ("C02", "FX-COINT-001", [("    crit = _critico(_CRIT_TAU, q, nivel)", "    crit = _critico(_CRIT_TAU, 1, nivel)")],
     "Engle-Granger con el valor crítico del ADF simple"),
    ("C03", "FX-COINT-001", [("        return {\"rho\": rho, \"vida_media_periodos\": math.log(0.5) / math.log(rho)}",
                              "        return {\"rho\": rho, \"vida_media_periodos\": math.log(0.5) / rho}")],
     "vida media mal calculada"),
    ("C04", "FX-COINT-001", [("    X = np.column_stack([np.ones(T_), Y[:, 1:]])\n    b, _, z = _mco(Y[:, 0], X)",
                              "    X = np.column_stack([np.zeros(T_), Y[:, 1:]])\n    b, _, z = _mco(Y[:, 0], X)")],
     "regresión de cointegración sin constante"),
    ("C05", "FX-COINT-001", [('    if T_ < p["obs_minimas"]:', '    if T_ < 5:')], "mínimo de 50 observaciones quitado"),
    ("C06", "FX-COINT-001", [("    beta_n, alfa_n = jo[\"beta\"] / b0, jo[\"alfa\"] * b0", "    beta_n, alfa_n = jo[\"beta\"] / b0, jo[\"alfa\"]")],
     "velocidad de ajuste sin renormalizar"),
    ("C07", "FX-COINT-001", [("        rechaza = jo[\"traza\"][r] > cr", "        rechaza = jo[\"traza\"][r] > cr / 2")],
     "contraste de la traza con el valor crítico a la mitad"),
    # ------------------------------------------------------------------ BIB-MET-001
    ("M01", "BIB-MET-001", [("    hhi = float(np.sum(cuotas ** 2))", "    hhi = float(np.sum(cuotas) ** 2)")], "HHI mal calculado"),
    ("M02", "BIB-MET-001", [('    for clave in ("hash", "titulo"):', '    for clave in ("hash",):')],
     "duplicados solo por huella"),
    ("M03", "BIB-MET-001", [('"hash": str(fi["hash"]).strip().lower() if fi.get("hash") else None', '"hash": str(fi["hash"]).strip() if fi.get("hash") else None')],
     "huella sensible a mayúsculas"),
    ("M04", "BIB-MET-001", [("    anios = (len(periodos) - 1) / por_anio", "    anios = len(periodos) / por_anio")],
     "años del CAGR mal contados"),
    ("M05", "BIB-MET-001", [('        if faltan:\n            raise ErrorFicha(f"{F}: conjunto corrupto (ficha {i} sin {\', \'.join(faltan)})")',
                             '        if False:\n            raise ErrorFicha(f"{F}: conjunto corrupto (ficha {i} sin {\', \'.join(faltan)})")')],
     "fichas incompletas aceptadas"),
    # ------------------------------------------------------------------ TEM-DIFF-001
    ("D01", "TEM-DIFF-001", [("    return m / (1 + np.exp(-k * (t - t0)))", "    return m / (1 + np.exp(-k * (t - t0) / 2))")],
     "logística con la tasa a la mitad"),
    ("D02", "TEM-DIFF-001", [("    return origen + math.log(q_ / p_) / (p_ + q_) if q_ > p_ else None", "    return origen + math.log(q_ / p_) / q_ if q_ > p_ else None")],
     "inflexión de Bass mal calculada"),
    ("D03", "TEM-DIFF-001", [('    return "introduccion" if cuota < umbrales[0] else', '    return "introduccion" if cuota < umbrales[1] else')],
     "umbral de introducción del 50 %"),
    ("D04", "TEM-DIFF-001", [("        aic = n * math.log(max(ssr, EPS * float(np.sum(y ** 2))) / n) + 2 * k_par",
                              "        aic = n * math.log(max(ssr, EPS * float(np.sum(y ** 2))) / n)")], "AIC sin penalización"),
    ("D05", "TEM-DIFF-001", [("    if not np.any((dy[1:] > dy[:-1]) & (dy[:-1] > 0)):", "    if False:")],
     "rechazo sin tramo de aceleración quitado"),
    ("D06", "TEM-DIFF-001", [('    bandas = {f"p{round(c * 100)}": np.quantile(sims_a, c, axis=0) for c in qs}',
                              '    bandas = {f"p{round(c * 100)}": np.quantile(sims_a, 1 - c, axis=0) for c in qs}')],
     "bandas del bootstrap invertidas"),
    ("D07", "TEM-DIFF-001", [("    return m * np.exp(-np.exp(-k * (t - t0)))", "    return m * np.exp(-np.exp(-k * (t - t0))) ** 0.5")],
     "Gompertz mal escrita"),
    ("D08", "TEM-DIFF-001", [('    if n < p["obs_minimas"]:\n        raise ErrorFicha(f"{F}: {n} observaciones (< {p[\'obs_minimas\']})")\n    if np.any(np.diff(t) <= 0):',
                              '    if n < 4:\n        raise ErrorFicha(f"{F}: {n} observaciones (< {p[\'obs_minimas\']})")\n    if np.any(np.diff(t) <= 0):')],
     "mínimo de 8 observaciones quitado"),
]

CC = """
import sys
from pathlib import Path
from bloque_a.motor import fichas_series as S
assert Path(S.__file__).resolve().is_relative_to(Path({copia!r}).resolve()), S.__file__
import json
fallos = []
for caso in S.CASOS_CONTROL[{ficha!r}]:
    try:
        v = {{}}
        for d in caso["datos"]:
            v.update(d["valores"])
        r1, _ = S.FICHAS[{ficha!r}]["fn"]({{"valores": v}}, dict(caso["parametros"]))
        r2, _ = S.FICHAS[{ficha!r}]["fn"]({{"valores": v}}, dict(caso["parametros"]))
        ok = bool(caso["comprobar"](r1)) and json.dumps(r1, sort_keys=True) == json.dumps(r2, sort_keys=True)
    except Exception as e:  # noqa: BLE001 — un caso que falla por cualquier motivo no se supera
        ok = False
    if not ok:
        fallos.append(caso["nombre"][:50])
print("CAZADO" if fallos else "SUPERA", fallos[:2])
"""


def preparar(destino: Path) -> Path:
    base = Path(tempfile.mkdtemp(prefix="impl_S_mut_", dir=destino))
    shutil.copytree(RAIZ / "bloque_a", base / "bloque_a", ignore=shutil.ignore_patterns(
        "__pycache__", "*.pyc", ".pytest_cache", ".mypy_cache", "*.egg-info", "build", "*.docx"))
    return base / "bloque_a" / "11_Ejecutor"


def entorno(copia: Path) -> dict[str, str]:
    e = {k: v for k, v in os.environ.items() if k != "BLOQUE_A_RAIZ"}
    e.update({"PYTHONPATH": str(copia), "PYTHONDONTWRITEBYTECODE": "1"})
    return e


def probar(copia: Path, mutante: tuple[str, str, list[tuple[str, str]], str]) -> str:
    mid, ficha, cambios, desc = mutante
    ruta = copia / MODULO
    original = ruta.read_text(encoding="utf-8")
    texto = original
    for viejo, nuevo in cambios:
        if texto.count(viejo) != 1:
            return f"{mid} NO SE APLICA: «{viejo[:60]}» aparece {texto.count(viejo)} veces"
        texto = texto.replace(viejo, nuevo)
    ruta.write_text(texto, encoding="utf-8")
    try:
        env = entorno(copia)
        cc = subprocess.run([PY, "-B", "-c", CC.format(copia=str(copia), ficha=ficha)], capture_output=True, text=True, check=False,
                            cwd=copia, env=env, timeout=900)
        cazado_cc = "CAZADO" in cc.stdout or cc.returncode != 0
        t = subprocess.run([PY, "-B", "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", PRUEBAS, "-k", CLAVE[ficha]],
                           capture_output=True, text=True, check=False, cwd=copia, env=env, timeout=1800)
        cazado_t = t.returncode != 0
        fallo = next((x for x in t.stdout.splitlines() if x.startswith("FAILED")), "")[:100]
        return (f"{mid} {ficha:13s} CC={'cazado' if cazado_cc else 'VIVO  '} T={'cazado' if cazado_t else 'VIVO  '} · {desc}"
                f"{' · ' + fallo if fallo else ''}")
    finally:
        ruta.write_text(original, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("destino", type=Path)
    ap.add_argument("--solo")
    ap.add_argument("-j", type=int, default=2)
    a = ap.parse_args()
    a.destino.mkdir(parents=True, exist_ok=True)
    lista = [m for m in MUTANTES if not a.solo or m[0] in a.solo.split(",")]
    copias = [preparar(a.destino) for _ in range(min(a.j, len(lista)))]
    base = subprocess.run([PY, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", PRUEBAS], capture_output=True, check=False,
                          text=True, cwd=copias[0], env=entorno(copias[0]), timeout=3600)
    print("pruebas en la copia sin mutar:", (base.stdout.strip().splitlines() or [""])[-1], flush=True)
    if base.returncode != 0:
        return 1
    lineas: list[str] = []
    with cf.ThreadPoolExecutor(len(copias)) as ex:
        futuros = {}
        libres = list(copias)
        pendientes = list(lista)
        while pendientes or futuros:
            while libres and pendientes:
                copia, m = libres.pop(), pendientes.pop(0)
                futuros[ex.submit(probar, copia, m)] = copia
            hecho = next(cf.as_completed(futuros))
            libres.append(futuros.pop(hecho))
            linea = hecho.result()
            print(linea, flush=True)
            lineas.append(linea)
    for c in copias:
        shutil.rmtree(c.parents[1], ignore_errors=True)
    vivos_cc = [x for x in lineas if "CC=VIVO" in x]
    vivos = [x for x in lineas if "CC=VIVO" in x and "T=VIVO" in x]
    no_aplicados = [x for x in lineas if "NO SE APLICA" in x]
    print(f"\n{len(lineas) - len(no_aplicados)} mutantes aplicados; vivos frente a los casos de control: {len(vivos_cc)}; "
          f"vivos frente a casos de control y pruebas a la vez: {len(vivos)}; no aplicados: {len(no_aplicados)}")
    for x in vivos + no_aplicados:
        print("   ·", x)
    return 1 if vivos or no_aplicados else 0


if __name__ == "__main__":
    sys.exit(main())
