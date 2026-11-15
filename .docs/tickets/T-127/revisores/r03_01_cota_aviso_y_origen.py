"""QA r03 de T-127 · la cota de la aportación con signo (H-05), el aviso de un dato movido (H-04) y de dónde salen los
componentes (el motivo del límite declarado).

 K. Cota «(1 − k)/(2 − k)»: 4000 casos aleatorios propios (n de 2 a 12, pesos de escalas muy distintas, copias con la misma
    cifra, resto con los dos signos y rellenos grandes que se compensan, construidos cerca del borde). Para cada caso que
    `_aportacion_maxima` deja pasar (≤ k), el agregado · Σden / den_G de CADA grupo (no solo del primero) tiene un error
    relativo ≥ cota. Además, la cota es justa: con un resto de −c·num_G (c = cota·(1 ± ε)) y dos rellenos +Y y −Y se sirve
    con ε > 0 y se rechaza con ε < 0.
 A. Aviso: (1) ningún caso de control de FIR-CRED, REI-LEV, CHR-TOKEN y REI-NAV lo da, ni ninguna entrada de RC de
    `verificar_casos_control`; (2) frecuencia con «datos corrientes» simulados (sectores realistas, cifras redondeadas como
    las escribiría un analista); (3) un ejemplo concreto de tokens reales de oferta fija y redonda; (4) vías que lo esquivan
    con un solo dato de ENTRADA movido (REI-NAV sin `otros_pasivos`: el derivado se mueve solo); (5) la petición no cambia
    `AVISO_B` ni `FRONTERA_B`.
 O. Origen de las peticiones: todas las llamadas a `Motor.servir` del paquete (AST), con la operación que piden.
Uso: .venv/bin/python -I .docs/tickets/T-127/revisores/r03_01_cota_aviso_y_origen.py [ejecutor]
"""
import ast
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "T-118" / "revisores"))
import r01_comun as C  # noqa: E402

EJE = C.preparar(sys.argv)
import numpy as np  # noqa: E402
from bloque_a.motor import fichas_p2 as fp  # noqa: E402
from bloque_a.motor import fichas_reales as fr  # noqa: E402
from bloque_a.motor import frontera_b as fb  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402
from bloque_a.motor.operaciones import ErrorFicha  # noqa: E402

K_ = C.Contador("r03_01 T-127 cota, aviso y origen")
AVISO = "aviso (1.6)"
k = fb.FRONTERA_B["peso_maximo_componente"]
tol = fb.FRONTERA_B["tolerancia_clon"]
cota = (1 - k) / (2 - k)
rng = np.random.default_rng(20261115)


def grupos_de(num, den):
    x = num / den
    ax = np.abs(x)
    cerca = np.abs(x[:, None] - x[None, :]) <= tol * np.maximum(ax[:, None], ax[None, :])
    np.fill_diagonal(cerca, True)
    return cerca


# ------------------------------------------------------------------ K: la cota
print(f"[K] cota (1 − k)/(2 − k) = {cota:.6f} con k = {k}")
casos, servidos, violaciones, peor = 0, 0, [], np.inf
for _ in range(4000):
    casos += 1
    n = int(rng.integers(2, 13))
    den = np.exp(rng.uniform(-3, 3, n))                     # pesos de escalas muy distintas
    x = rng.normal(0, 1, n)
    modo = rng.integers(0, 4)
    if modo == 1 and n >= 3:                                # copias de la cifra del primero
        m = int(rng.integers(1, n - 1))
        x[1:1 + m] = x[0] * (1 + rng.uniform(-0.009, 0.009, m))
    num = den * x
    if modo >= 2:                                           # resto construido cerca del borde, con los dos signos
        c = cota * (1 + rng.uniform(-0.2, 0.6)) * rng.choice([-1, 1])
        R = c * num[0]
        resto = rng.normal(0, 1, n - 1) * abs(num[0]) * rng.uniform(0, 5)
        if modo == 3 and n >= 3:                            # rellenos que se compensan
            resto[0], resto[1] = 10 * abs(num[0]), -10 * abs(num[0])
        resto += (R - resto.sum()) / (n - 1)
        num[1:] = resto
    if fb._aportacion_maxima(num, den, tol, 0.0) > k:
        continue
    servidos += 1
    S = float(np.sum(num))
    cerca = grupos_de(num, den)
    for i in range(n):
        g = cerca[i]
        num_g, den_g = float(num[g].sum()), float(den[g].sum())
        if num_g == 0:
            continue
        err = abs(S / den_g - num_g / den_g) / abs(num_g / den_g)
        peor = min(peor, err / cota)
        if err < cota * (1 - 1e-9):
            violaciones.append((n, int(modo), i, err))
print(f"    {casos} casos · {servidos} servidos (≤ k) · peor error / cota = {peor:.6f} · violaciones {len(violaciones)}")
K_.comprobar("K: con la aportación ≤ k, el error de agregado·Σden/den_G es ≥ (1 − k)/(2 − k) para todo grupo",
             not violaciones and servidos > 500, str(violaciones[:3]))
K_.comprobar("K: la cota es casi alcanzada por los casos construidos (peor/cota < 1,05)", peor < 1.05, f"{peor}")


def borde(eps):
    c = cota * (1 + eps)
    num = np.array([1.0, -c / 2 + 10, -c / 2 - 10])         # resto −c (con signo), rellenos ±10
    den = np.array([1.0, 1.0, 1.0])
    return fb._aportacion_maxima(num, den, tol, 0.0)


print(f"    borde: ε = +1e-6 → {borde(1e-6):.9f} · ε = −1e-6 → {borde(-1e-6):.9f} (k = {k})")
K_.comprobar("K: la cota es justa (ε > 0 se sirve, ε < 0 se rechaza)", borde(1e-6) <= k < borde(-1e-6))
# el caso del mismo signo: (1 − k)/k
num = np.array([1.0, (1 - k) / k * (1 + 1e-6)])
K_.comprobar("K: con el resto del mismo signo la cota es (1 − k)/k", fb._aportacion_maxima(num, np.ones(2), tol, 0.0) <= k)

# ------------------------------------------------------------------ A1: casos de control sin aviso
print("\n[A1] casos de control")
MOD = {"FIR-CRED-001": fp, "REI-LEV-001": fp, "CHR-TOKEN-001": fp, "REI-NAV-001": fr}


def correr(ficha, v, p):
    return MOD[ficha].FICHAS[ficha]["fn"]({"valores": copy.deepcopy(v), "series": {}, "series_rol": {}}, dict(p or {}))


def caso(ficha, i):
    return C.valores(ficha, i), dict(servicio.CASOS_CONTROL[ficha][i].get("parametros") or {})


con_aviso = []
for f in MOD:
    for i in range(len(servicio.CASOS_CONTROL[f])):
        v, p = caso(f, i)
        try:
            _, lim = correr(f, v, p)
        except ErrorFicha:
            continue
        if any(x.startswith(AVISO) for x in lim):
            con_aviso.append((f, i))
m = C.motor()
rv = m.verificar_casos_control()
rc_aviso = [e.get("operacion") for e in m.almacen.leer("RC") if any(str(x).startswith(AVISO) for x in e.get("limitaciones") or [])]
print(f"    con aviso: {con_aviso} · RC con aviso tras verificar_casos_control: {rc_aviso}")
K_.comprobar("A1: ningún caso de control da el aviso (las cuatro fichas y el RC de las 67)", not con_aviso and not rc_aviso)

# ------------------------------------------------------------------ A2: datos corrientes simulados
print("\n[A2] frecuencia del aviso con datos corrientes simulados (cifras redondeadas a 2 o 3 significativas)")


def redondo(x, sig):
    x = np.asarray(x, dtype=float)
    out = np.zeros_like(x)
    nz = x != 0
    e = np.floor(np.log10(np.abs(x[nz])))
    out[nz] = np.round(x[nz] / 10 ** (e - sig + 1)) * 10 ** (e - sig + 1)
    return out


def tasa(gen, n, veces=2000):
    con = 0
    for _ in range(veces):
        if fb._aviso_casi_clones(gen(n), tol, []):
            con += 1
    return con / veces


def fir(n, sig=2):
    E = redondo(np.exp(rng.normal(21, 1.2, n)), sig)
    sE = np.round(rng.uniform(0.15, 0.6, n), 2)
    corto = np.where(rng.random(n) < 0.2, 0.0, redondo(np.exp(rng.normal(19, 1.2, n)), sig))
    largo = redondo(np.exp(rng.normal(20, 1.2, n)), sig)
    return list(zip(E, sE, corto, largo, strict=True))


def lev(n, sig=2):
    gav = np.exp(rng.normal(22, 1.0, n))
    return [tuple(redondo([g, g * rng.uniform(0.25, 0.55), g * rng.uniform(0, 0.05), g * rng.uniform(0.04, 0.07),
                           g * rng.uniform(0.005, 0.02), g * rng.uniform(0.02, 0.05)], sig)) for g in gav]


def nav(n, sig=2):
    filas = []
    for _ in range(n):
        acc = redondo([np.exp(rng.normal(18, 1))], sig)[0]
        navps = round(float(rng.uniform(5, 80)), 2)
        filas.append((round(navps * rng.uniform(0.6, 1.2), 2), acc, navps, redondo([acc * navps * rng.uniform(0.3, 0.8)], sig)[0],
                      0.0, round(float(rng.choice([0.045, 0.05, 0.055, 0.06])), 3)))
    return filas


def tok(n, sig=2):
    filas = []
    for _ in range(n):
        total = float(rng.choice([1e8, 1e9, 1e10, 21e6])) if rng.random() < 0.6 else redondo([np.exp(rng.normal(20, 2))], sig)[0]
        circ = total if rng.random() < 0.4 else redondo([total * rng.uniform(0.3, 0.95)], sig)[0]
        fija = rng.random() < 0.5
        filas.append((float(redondo([np.exp(rng.normal(0, 2))], 3)[0]), circ, total, total if fija else None,
                      0.0 if fija else redondo([circ * rng.uniform(0.01, 0.08)], sig)[0], 0.0))
    return filas


for nombre, gen, ns in (("FIR-CRED", fir, (10, 20, 30)), ("REI-LEV", lev, (3, 7, 15)), ("REI-NAV", nav, (3, 7, 15)),
                        ("CHR-TOKEN", tok, (5, 10, 20))):
    print(f"    {nombre}: " + " · ".join(f"n={n}: {tasa(gen, n):.1%}" for n in ns))
t20 = tasa(tok, 20)
K_.comprobar("A2: el aviso es raro con datos corrientes de FIR-CRED, REI-LEV y REI-NAV (< 2 % a n máximo)",
             max(tasa(fir, 30), tasa(lev, 15), tasa(nav, 15)) < 0.02)
print(f"    CHR-TOKEN con ofertas redondas y fijas (60 % redondas, 50 % sin emisión): {t20:.1%} de las peticiones de 20")

# ------------------------------------------------------------------ A3: ejemplo concreto de tokens corrientes
print("\n[A3] dos tokens reales de oferta fija y redonda, totalmente en circulación, sin emisión ni quema")
v, p = caso("CHR-TOKEN-001", 1)
base = v["tokens"][0]
nuevos = []
for j, (precio, st, co) in enumerate(((0.42, 0.031, 0.22), (7.9, 0.047, 0.41))):
    t = copy.deepcopy(base)
    t.update(id=f"GOB{j}", precio=precio, oferta_circulante=1e9, oferta_total=1e9, oferta_maxima=1e9, emision_anual=0.0,
             quema_anual=0.0, staking_nominal=st, concentracion_10_mayores=co)
    t["calendario"] = {"fuente": "documentación del proyecto", "desbloqueos": []}
    nuevos.append(t)
v["tokens"] = v["tokens"] + nuevos
try:
    _, lim = correr("CHR-TOKEN-001", v, p)
    av = [x for x in lim if x.startswith(AVISO)]
    print(f"    servido · avisos: {av}")
except ErrorFicha as e:
    av = None
    print(f"    rechazo: {e}")
K_.comprobar("A3: dos tokens distintos de 1e9 fijos (precios 0,42 y 7,9) no dan el aviso de «un mismo emisor»", av == [],
             "(da el aviso: falso positivo con datos corrientes)")

# ------------------------------------------------------------------ A4: un solo dato de entrada movido, sin aviso
print("\n[A4] REI-NAV-001: A en 2 partes con el NAV por acción ±4 % y sin `otros_pasivos` (el derivado se mueve solo)")
v, p = caso("REI-NAV-001", 2)
a = v["componentes"][0]
partes = []
for j, d in enumerate((0.04, -0.04)):
    c = copy.deepcopy(a)
    c.update(id=f"P{j}", acciones=a["acciones"] / 2, nav_por_accion=a["nav_por_accion"] / (1 + d),
             deuda_neta=a["deuda_neta"] / 2, gav=a["gav"] / 2)
    c.pop("otros_pasivos", None)
    partes.append(c)
v["componentes"] = partes
try:
    res, lim = correr("REI-NAV-001", v, p)
    av = [x for x in lim if x.startswith(AVISO)]
    prima_a = (a["precio"] / a["nav_por_accion"] - 1) * 100
    print(f"    servido · prima {res['prima_agregada_pct']:.9f} (A {prima_a:.9f}) · avisos {len(av)}")
    esquiva = abs(res["prima_agregada_pct"] - prima_a) < 1e-6 and not av
except ErrorFicha as e:
    print(f"    rechazo: {e}")
    esquiva = False
print(f"    → {'sin aviso: un dato de entrada movido, dos en la firma (límite del aviso: «moviendo dos datos»)' if esquiva else 'con aviso o rechazo'}")

# ------------------------------------------------------------------ A5: la petición no cambia las reglas
print("\n[A5] la petición no cambia AVISO_B ni FRONTERA_B")
v, p = caso("FIR-CRED-001", 1)
base = v["componentes"][11]
comps = []
for j, d in enumerate((0.02, 0.04, 0.06, 0.08, 0.10)):
    for sg in (1, -1):
        c = copy.deepcopy(base)
        c["id"] = f"E{j}{sg}"
        c["volatilidad_acciones"] = base["volatilidad_acciones"] * (1 + sg * d)
        comps.append(c)
v["componentes"] = comps
for extra in ({"datos_distintos_aviso": 0}, {"tolerancia_clon": 0.0}, {"peso_maximo_componente": 1.0}):
    try:
        _, lim = correr("FIR-CRED-001", v, {**p, **extra})
        r = "aviso" if any(x.startswith(AVISO) for x in lim) else "SIN aviso"
    except ErrorFicha as e:
        r = f"rechazo ({str(e)[:70]})"
    print(f"    {extra}: {r}")
    K_.comprobar(f"A5: {extra} en la petición no quita el aviso", r == "aviso" or r.startswith("rechazo"))

# ------------------------------------------------------------------ O: origen de las peticiones
print("\n[O] llamadas a Motor.servir / reejecutar en el paquete (AST)")
paquete = EJE / "bloque_a"
CON_COMPONENTES = {"FIR-CRED-001", "REI-LEV-001", "CHR-TOKEN-001", "REI-NAV-001", "REI-FFO-001", "IDX-REB-001",
                   "FON-DISC-001", "FON-TD-001", "CHR-FLOW-001", "IDX-CONC-001", "CHR-FUND-001"}
llamadas = []
for py in sorted(paquete.rglob("*.py")):
    arbol = ast.parse(py.read_text(encoding="utf-8"))
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Attribute) and nodo.func.attr in ("servir", "reejecutar"):
            op = "?"
            if nodo.args and isinstance(nodo.args[0], ast.Dict):
                for kk, vv in zip(nodo.args[0].keys, nodo.args[0].values, strict=True):
                    if isinstance(kk, ast.Constant) and kk.value == "operacion":
                        op = vv.value if isinstance(vv, ast.Constant) else ast.unparse(vv)
            llamadas.append((str(py.relative_to(EJE)), nodo.lineno, nodo.func.attr, op))
for x in llamadas:
    print(f"    {x[0]}:{x[1]} {x[2]} → {x[3]}")
fuera = [x for x in llamadas if not x[0].startswith("bloque_a/motor/servicio.py")]
ops = {x[3] for x in fuera}
K_.comprobar("O: fuera del propio servicio (casos de control y CT-10), ninguna llamada pide una ficha con componentes",
             not (ops & CON_COMPONENTES) and all(o != "?" for o in ops), str(ops))
sys.exit(K_.fin())
