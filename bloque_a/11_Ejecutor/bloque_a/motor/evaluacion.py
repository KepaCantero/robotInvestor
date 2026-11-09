"""Evaluación predictiva (MC-10): fichas FC-EVAL-001 y FC-CAL-001 y criterio de certificado (R13, Anexo A).

- Brier, log-score (p recortada a [0,01; 0,99]; se informa la pérdida logarítmica media, menor es mejor),
  descomposición de Murphy, acierto direccional con prueba binomial e IC de Wilson.
- BSS frente a la referencia ingenua con IC por bootstrap de bloques móviles (semilla fija).
- Diebold-Mariano con corrección de Harvey-Leybourne-Newbold (HLN).
- ECE con nulo por simulación bajo calibración perfecta (Bröcker y Smith, 2007): media y percentil 90.
- T-66 (PA-03): muestra efectiva n_eff con el efecto de diseño de Kish por conglomerados de fecha (los pronósticos
  que se resuelven el mismo día comparten el choque de mercado) y bootstrap del BSS por conglomerados de fecha.
"""
from __future__ import annotations

import math
from collections.abc import Sequence

import numpy as np
from scipy import stats

EPS = 0.01


def _pares(p, o):
    p = np.asarray(p, dtype=float)
    o = np.asarray(o, dtype=float)
    if p.shape != o.shape:
        raise ValueError("p y o deben tener la misma longitud")
    return p, o


def brier(p, o) -> float:
    p, o = _pares(p, o)
    return float(np.mean((p - o) ** 2)) if len(p) else float("nan")


def log_score(p, o) -> float:
    p, o = _pares(p, o)
    pc = np.clip(p, EPS, 1 - EPS)
    return float(-np.mean(o * np.log(pc) + (1 - o) * np.log(1 - pc))) if len(p) else float("nan")


def murphy(p, o, bins: Sequence[float] | None = None) -> dict:
    """Descomposición de Murphy (1973) agrupando por valores de p (exacta con probabilidades discretas)."""
    p, o = _pares(p, o)
    n = len(p)
    obar = float(o.mean())
    rel = res = 0.0
    for v in np.unique(p if bins is None else np.digitize(p, bins)):
        m = (p == v) if bins is None else (np.digitize(p, bins) == v)
        nk = m.sum()
        pk, ok = float(p[m].mean()), float(o[m].mean())
        rel += nk * (pk - ok) ** 2
        res += nk * (ok - obar) ** 2
    return {"fiabilidad": rel / n, "resolucion": res / n, "incertidumbre": obar * (1 - obar)}


def wilson(k: int, n: int, nivel: float = 0.90) -> list[float | None]:
    if n == 0:
        return [None, None]
    z = stats.norm.ppf(1 - (1 - nivel) / 2)
    ph = k / n
    den = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / den
    m = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / den
    return [max(0.0, c - m), min(1.0, c + m)]


def acierto_direccional(o: Sequence[int], tasa_base: float = 0.5, nivel: float = 0.90) -> dict:
    o = np.asarray(o, dtype=int)
    n, k = len(o), int(o.sum())
    if n == 0:
        return {"n": 0, "aciertos": 0, "tasa": None, "ic": [None, None], "p_binomial": None}
    p_bin = float(stats.binomtest(k, n, p=tasa_base, alternative="greater").pvalue)
    return {"n": n, "aciertos": k, "tasa": k / n, "ic": wilson(k, n, nivel), "p_binomial": p_bin, "tasa_base": tasa_base}


def _bloques(n: int, b: int, rng: np.random.Generator) -> np.ndarray:
    k = math.ceil(n / b)
    inicios = rng.integers(0, max(n - b + 1, 1), size=k)
    idx = np.concatenate([np.arange(s, s + b) for s in inicios])[:n]
    return np.clip(idx, 0, n - 1)


def bss(p, o, p_ref, replicas: int = 2000, nivel: float = 0.90, semilla: int = 12345, bloque: int | None = None) -> dict:
    p, o = _pares(p, o)
    p_ref = np.asarray(p_ref, dtype=float)
    n = len(p)
    if n == 0:
        return {"valor": None, "ic": [None, None], "n": 0}
    bs, bsr = brier(p, o), brier(p_ref, o)
    valor = 1 - bs / bsr if bsr > 0 else None
    if n < 5:
        return {"valor": valor, "ic": [None, None], "n": n, "brier": bs, "brier_ref": bsr}
    b = bloque or max(1, int(round(n ** (1 / 3))))
    rng = np.random.default_rng(semilla)
    sims = []
    for _ in range(replicas):
        i = _bloques(n, b, rng)
        r = np.mean((p_ref[i] - o[i]) ** 2)
        if r > 0:
            sims.append(1 - np.mean((p[i] - o[i]) ** 2) / r)
    a = (1 - nivel) / 2
    ic = [float(np.quantile(sims, a)), float(np.quantile(sims, 1 - a))] if sims else [None, None]
    return {"valor": valor, "ic": ic, "n": n, "brier": bs, "brier_ref": bsr, "bloque": b, "replicas": replicas,
            "nivel": nivel, "semilla": semilla}


def _conglomerados(fechas, n: int) -> np.ndarray:
    """Índice de conglomerado (0…k−1, en orden de fecha) de cada observación. Falla cerrado ante una fecha ausente o
    una longitud distinta de la de los datos."""
    if fechas is None:
        raise ValueError("fechas de conglomerado ausentes")
    claves = []
    for f in fechas:
        if f is None or (isinstance(f, float) and not math.isfinite(f)) or not str(f).strip():
            raise ValueError(f"fecha de conglomerado ausente o no válida: {f!r}")
        claves.append(str(f).strip())
    if len(claves) != n:
        raise ValueError(f"fechas ({len(claves)}) y datos ({n}) deben tener la misma longitud")
    _, inv = np.unique(np.asarray(claves, dtype=object), return_inverse=True)
    return np.asarray(inv, dtype=int).reshape(-1)


def correlacion_intraclase(conglomerado, y) -> dict:
    """ρ intraclase de un ANOVA de un factor (ICC(1)), recortada a [0, 1].

    ρ = (MSB − MSW) / (MSB + (n₀ − 1)·MSW), con n₀ = (n − Σnᵢ²/n)/(k − 1). Falla cerrado (ρ = 1, máxima dependencia)
    cuando no se puede estimar: un solo conglomerado o residuos sin varianza. Con todos los conglomerados de tamaño 1
    no hay varianza intra que medir, pero el efecto de diseño es 1 sea cual sea ρ: se informa ρ = 0."""
    g = np.asarray(conglomerado, dtype=int)
    y = np.asarray(y, dtype=float)
    n = len(y)
    k = int(g.max()) + 1 if n else 0
    if k < 2:
        return {"rho": 1.0, "nota": "un solo conglomerado: ρ no estimable, se toma 1 (falla cerrado)"}
    if n == k:
        return {"rho": 0.0, "nota": "todos los conglomerados de tamaño 1: el efecto de diseño es 1"}
    tam = np.bincount(g, minlength=k).astype(float)
    medias = np.bincount(g, weights=y, minlength=k) / tam
    msb = float(np.sum(tam * (medias - y.mean()) ** 2) / (k - 1))
    msw = float(np.sum((y - medias[g]) ** 2) / (n - k))
    n0 = (n - float(np.sum(tam ** 2)) / n) / (k - 1)
    den = msb + (n0 - 1) * msw
    if not (math.isfinite(den) and den > 0):
        return {"rho": 1.0, "nota": "residuos sin varianza: ρ no estimable, se toma 1 (falla cerrado)"}
    bruto = (msb - msw) / den
    return {"rho": float(min(max(bruto, 0.0), 1.0)), "rho_bruto": float(bruto), "msb": msb, "msw": msw, "n0": float(n0),
            "nota": None}


def n_efectiva(fechas, residuos) -> dict:
    """PA-03: muestra efectiva con el efecto de diseño de Kish por conglomerados de fecha.

    n_eff = n / (1 + (m̄ − 1)·ρ), con m̄ = n/k el tamaño medio del conglomerado y ρ la correlación intraclase de los
    residuos (resultado − probabilidad) estimada por ANOVA y recortada a [0, 1]. Falla cerrado: residuos no finitos,
    fechas ausentes o longitudes distintas lanzan ValueError."""
    r = np.asarray(residuos, dtype=float).reshape(-1)
    if not np.all(np.isfinite(r)):
        raise ValueError("residuos no finitos")
    n = len(r)
    g = _conglomerados(fechas, n)
    if n == 0:
        return {"n": 0, "n_eff": 0.0, "conglomerados": 0, "m_medio": None, "rho": None, "efecto_diseno": None,
                "metodo": "Kish por conglomerados de fecha", "nota": "sin observaciones"}
    k = int(g.max()) + 1
    icc = correlacion_intraclase(g, r)
    m_medio = n / k
    deff = 1.0 + (m_medio - 1.0) * icc["rho"]
    return {"n": n, "n_eff": float(n / deff), "conglomerados": k, "m_medio": float(m_medio), "rho": icc["rho"],
            "rho_bruto": icc.get("rho_bruto"), "efecto_diseno": float(deff),
            "metodo": "Kish por conglomerados de fecha; ρ intraclase de los residuos por ANOVA, recortada a [0, 1]",
            "nota": icc["nota"]}


def bss_conglomerados(p, o, p_ref, fechas, replicas: int, nivel: float, semilla: int, min_conglomerados: int) -> dict:
    """PA-03: BSS con IC por bootstrap de conglomerados de fecha (se remuestrean fechas completas con reemplazo; semilla
    fija). Con menos de `min_conglomerados` fechas distintas no hay IC (falla cerrado: no certifica)."""
    p, o = _pares(p, o)
    p_ref = np.asarray(p_ref, dtype=float)
    n = len(p)
    g = _conglomerados(fechas, n)
    if n == 0:
        return {"valor": None, "ic": [None, None], "n": 0, "conglomerados": 0}
    k = int(g.max()) + 1
    bs, bsr = brier(p, o), brier(p_ref, o)
    out: dict = {"valor": 1 - bs / bsr if bsr > 0 else None, "ic": [None, None], "n": n, "brier": bs, "brier_ref": bsr,
           "metodo": "bootstrap por conglomerados de fecha", "conglomerados": k, "min_conglomerados": int(min_conglomerados),
           "replicas": replicas, "nivel": nivel, "semilla": semilla}
    if k < int(min_conglomerados):
        out["nota"] = f"{k} conglomerados de fecha < {int(min_conglomerados)}: sin IC (falla cerrado)"
        return out
    # Suma de pérdidas por conglomerado: el BSS de una réplica es 1 − Σ pérdida / Σ pérdida_ref de las fechas elegidas
    s = np.bincount(g, weights=(p - o) ** 2, minlength=k)
    s_ref = np.bincount(g, weights=(p_ref - o) ** 2, minlength=k)
    elegidos = np.random.default_rng(semilla).integers(0, k, size=(replicas, k))
    num, den = s[elegidos].sum(axis=1), s_ref[elegidos].sum(axis=1)
    sims = 1 - num[den > 0] / den[den > 0]
    a = (1 - nivel) / 2
    if len(sims):
        out["ic"] = [float(np.quantile(sims, a)), float(np.quantile(sims, 1 - a))]
    return out


def diebold_mariano_hln(perdida_a: Sequence[float], perdida_b: Sequence[float], h: int = 1) -> dict:
    """DM con corrección HLN. d = pérdida_a − pérdida_b; estadístico < 0 ⇒ a mejor que b.
    p-valor unilateral (a mejor que b) y bilateral, con t de Student n−1 g.l."""
    d = np.asarray(perdida_a, float) - np.asarray(perdida_b, float)
    n = len(d)
    if n < 3:
        return {"estadistico": None, "p_unilateral": None, "p_bilateral": None, "n": n, "h": h}
    dbar = d.mean()
    gam = [np.mean((d[k:] - dbar) * (d[:n - k] - dbar)) for k in range(h)]
    var = (gam[0] + 2 * sum(gam[1:])) / n
    if var <= 0:
        return {"estadistico": 0.0, "p_unilateral": 0.5, "p_bilateral": 1.0, "n": n, "h": h}
    dm = dbar / math.sqrt(var)
    hln = math.sqrt((n + 1 - 2 * h + h * (h - 1) / n) / n)
    est = dm * hln
    return {"estadistico": float(est), "p_unilateral": float(stats.t.cdf(est, n - 1)),
            "p_bilateral": float(2 * (1 - stats.t.cdf(abs(est), n - 1))), "n": n, "h": h}


def _tramos(p: np.ndarray, n_tramos: int | None) -> np.ndarray:
    n = len(p)
    if n_tramos is None:
        n_tramos = 10 if n >= 200 else 5
    if n >= 200:
        bordes = np.linspace(0, 1, n_tramos + 1)
    else:
        bordes = np.unique(np.quantile(p, np.linspace(0, 1, n_tramos + 1)))
        if len(bordes) < 2:
            bordes = np.array([0.0, 1.0])
    idx = np.clip(np.searchsorted(bordes, p, side="right") - 1, 0, len(bordes) - 2)
    return idx


def ece(p, o, n_tramos: int | None = None) -> dict:
    p, o = _pares(p, o)
    n = len(p)
    if n == 0:
        return {"ece": None, "mce": None, "curva": []}
    idx = _tramos(p, n_tramos)
    e, mce, curva = 0.0, 0.0, []
    for t in np.unique(idx):
        m = idx == t
        pk, ok, nk = float(p[m].mean()), float(o[m].mean()), int(m.sum())
        e += nk / n * abs(pk - ok)
        mce = max(mce, abs(pk - ok))
        curva.append({"p_media": pk, "frecuencia": ok, "n": nk})
    return {"ece": float(e), "mce": float(mce), "curva": curva, "tramos": len(curva)}


def ece_nulo(p, simulaciones: int = 2000, semilla: int = 54321, n_tramos: int | None = None) -> dict:
    """Distribución del ECE de un pronosticador perfectamente calibrado con las mismas p (o* ~ Bernoulli(p))."""
    p = np.asarray(p, float)
    if len(p) == 0:
        return {"media": None, "q90": None}
    rng = np.random.default_rng(semilla)
    vals = [ece(p, (rng.random(len(p)) < p).astype(float), n_tramos)["ece"] for _ in range(simulaciones)]
    return {"media": float(np.mean(vals)), "q90": float(np.quantile(vals, 0.90)), "simulaciones": simulaciones}


def evaluar_celda(p, o, p_ref, tasa_base: float = 0.5, replicas: int = 2000, simulaciones: int = 2000,
                  nivel: float = 0.90, semilla: int = 12345, h: int = 1, fechas=None,
                  min_conglomerados: int | None = None) -> dict:
    """Métricas completas de una celda clase × horizonte (FC-EVAL-001 + FC-CAL-001).

    Con `fechas` (una por pronóstico: la de su conglomerado), añade la muestra efectiva (`n_eff`, PA-03) y el IC del BSS
    sale del bootstrap por conglomerados de fecha (exige `min_conglomerados`). Sin fechas, `n_eff` es None (no
    certificable) y el IC es el del bootstrap de bloques móviles."""
    p, o = _pares(p, o)
    p_ref = np.asarray(p_ref, float)
    n = len(p)
    out: dict = {"n": n}
    if n == 0:
        return out
    perd = (p - o) ** 2
    perd_ref = (p_ref - o) ** 2
    if fechas is not None:
        if min_conglomerados is None:
            raise ValueError("evaluar_celda: con fechas de conglomerado hace falta min_conglomerados (configuración)")
        muestra = n_efectiva(fechas, o - p)
        ic_bss = bss_conglomerados(p, o, p_ref, fechas, replicas, nivel, semilla, min_conglomerados)
    else:
        muestra = {"n": n, "n_eff": None, "nota": "sin fechas de conglomerado: n_eff no calculable (no certifica)"}
        ic_bss = bss(p, o, p_ref, replicas, nivel, semilla)
    out.update({
        "n_eff": muestra["n_eff"], "muestra_efectiva": muestra,
        "brier": brier(p, o), "brier_ref": brier(p_ref, o), "log_score": log_score(p, o), "log_score_ref": log_score(p_ref, o),
        "murphy": murphy(p, o), "acierto": acierto_direccional(o, tasa_base, nivel),
        "bss": ic_bss, "dm_hln": diebold_mariano_hln(perd, perd_ref, h),
        "calibracion": ece(p, o), "ece_nulo": ece_nulo(p, simulaciones, semilla + 1),
        "calibracion_global": {"p_media": float(p.mean()), "frecuencia": float(o.mean())},
    })
    return out


def criterio_certificado(m: dict, n_min: int = 100, ece_max: float = 0.15, alfa_holm: float | None = None) -> dict:
    """Anexo A: n ≥ 100; extremo inferior del IC 90 % del BSS > 0; ECE ≤ q90 del nulo y ECE < 0,15.
    T-66 (PA-03): el mínimo de muestra se exige a la muestra efectiva `n_eff`, no a la n nominal; sin `n_eff` no se
    certifica (falla cerrado).
    `alfa_holm`: si se evalúan varias celdas, se exige además p_unilateral DM ≤ alfa corregido por Holm."""
    motivos = []
    n = m.get("n", 0)
    n_eff = m.get("n_eff")
    if n_eff is None:
        motivos.append(f"n_eff no disponible (n nominal = {n}): sin fechas de conglomerado no se certifica")
    elif not (math.isfinite(n_eff) and n_eff >= n_min):
        motivos.append(f"n_eff = {n_eff:.1f} < {n_min} (n nominal = {n})")
    ic = (m.get("bss") or {}).get("ic") or [None, None]
    if ic[0] is None or ic[0] <= 0:
        motivos.append(f"extremo inferior del IC del BSS {ic[0]} ≤ 0")
    e = (m.get("calibracion") or {}).get("ece")
    q90 = (m.get("ece_nulo") or {}).get("q90")
    if e is None or q90 is None or e > q90:
        motivos.append(f"ECE {e} > q90 nulo {q90}")
    if e is None or e >= ece_max:
        motivos.append(f"ECE {e} ≥ {ece_max}")
    if alfa_holm is not None:
        pdm = (m.get("dm_hln") or {}).get("p_unilateral")
        if pdm is None or pdm > alfa_holm:
            if alfa_holm <= 0:
                motivos.append(f"DM-HLN p = {pdm}: el procedimiento de Holm se detuvo en una celda con p menor (no se rechaza)")
            else:
                motivos.append(f"DM-HLN p = {pdm} > alfa Holm {alfa_holm:.4f}")
    return {"certificable": not motivos, "motivos": motivos, "n": n, "n_eff": n_eff}


def holm(p_valores: dict[str, float], alfa: float = 0.10) -> dict[str, float]:
    """Umbral efectivo de Holm (1979) por celda, procedimiento escalonado (step-down).

    Se recorren las p de menor a mayor comparando la i-ésima (i = 0…m−1) con alfa/(m−i). En cuanto una
    no se rechaza, el procedimiento se detiene y ninguna de las siguientes se rechaza: su umbral efectivo
    es 0,0. (No hay p ≤ 0 después de la parada: todas son ≥ la p fallida, que es > alfa/(m−i) > 0.)
    Una celda se rechaza (supera Holm) si y solo si su p ≤ su umbral efectivo. El orden en caso de empate
    es el alfabético de la clave (determinista)."""
    def _valida(p) -> bool:
        return p is not None and math.isfinite(p)

    # una p ausente o no finita cuenta como «no rechazable» (falla cerrado) y se ordena la última
    orden = sorted(p_valores.items(), key=lambda kv: (kv[1] if _valida(kv[1]) else math.inf, kv[0]))
    m = len(orden)
    out: dict[str, float] = {}
    detenido = False
    for i, (k, p) in enumerate(orden):
        if detenido:
            out[k] = 0.0
            continue
        out[k] = alfa / (m - i)          # la celda donde se detiene conserva su umbral nominal (y no lo supera)
        if not _valida(p) or p > out[k]:
            detenido = True
    return out


def holm_rechazos(p_valores: dict[str, float], alfa: float = 0.10) -> dict[str, bool]:
    """Celdas cuya hipótesis nula se rechaza con el procedimiento escalonado de Holm."""
    u = holm(p_valores, alfa)
    return {k: (p is not None and math.isfinite(p) and p <= u[k]) for k, p in p_valores.items()}
