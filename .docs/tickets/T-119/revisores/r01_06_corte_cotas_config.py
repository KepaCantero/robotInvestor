"""QA r01 de T-119 · fecha de corte, cotas y coste, configuración y CT-10 tras cambiarla.

 1. Fecha de corte: en cada ficha, la fecha de corte justo antes de la última fecha observada de cada campo fechado ⇒
    RECHAZADO; en la última fecha observada ⇒ servido. Fechas contractuales (vencimientos, desbloqueos) posteriores al
    corte ⇒ servido; ¿puede colarse una observación por ahí? (vencimiento anterior a la fecha, desbloqueos pasados).
    El corte también llega por `proveedor.as_of`. La caché no sirve con un corte anterior lo servido con uno posterior.
 2. Cotas: cada lista y cada parámetro de tamaño en su máximo (servido o rechazado por otra regla, pero no por la cota)
    y con uno más (rechazado, rápido). Tiempo del servicio en el máximo.
 3. Configuración: FX-BEER-001 sigue `evaluacion.nivel_ic` del Motor; el artefacto guarda la sección usada; CT-10 tras
    cambiar la configuración ⇒ SI; configuración inválida ⇒ RECHAZADO.
"""
import copy
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from bloque_a.configuracion import cargar_config  # noqa: E402
from bloque_a.motor import fichas_p2, servicio  # noqa: E402

K = C.Contador("r01_06 fecha de corte, cotas y configuración")
CONTRACTUALES = ("vencimientos", "desbloqueos")


def fechas(x, ruta=()):
    """(ruta, fecha) de cada hoja de texto que es una fecha («fecha», «vintage»)."""
    if isinstance(x, dict):
        for k, v in x.items():
            if k in ("fecha", "vintage") and isinstance(v, str):
                yield ruta + (k,), pd.Timestamp(v)
            else:
                yield from fechas(v, ruta + (k,))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from fechas(v, ruta + (i,))


def campo(ruta):
    return ".".join(str(k) for k in ruta if not isinstance(k, int))


print("1. fecha de corte")
for f in C.P2:
    v, p = C.caso(f, 1)
    por_campo = {}
    for ruta, d in fechas(v):
        c = campo(ruta)
        por_campo[c] = max(por_campo.get(c, d), d)
    obs = {c: d for c, d in por_campo.items() if not any(x in c for x in CONTRACTUALES)}
    ult = max(obs.values())
    r = C.servir(C.motor(), f, v, p, fecha_corte=str(ult.date()))
    K.comprobar(f"{f}: corte = última observación ({ult.date()}) ⇒ servido", r["estado"] != "RECHAZADO", str(r.get("detalle"))[:160])
    for c, d in obs.items():
        r = C.servir(C.motor(), f, v, p, fecha_corte=str((d - pd.Timedelta(days=1)).date()))
        K.comprobar(f"{f}: corte un día antes de la última «{c}» ({d.date()}) ⇒ RECHAZADO", r["estado"] == "RECHAZADO"
                    and "corte" in r["detalle"], str(r.get("detalle"))[:160])
    cont = {c: d for c, d in por_campo.items() if c not in obs}
    if cont:
        print(f"   {f}: fechas contractuales {[(c, str(d.date())) for c, d in cont.items()]} posteriores al corte {ult.date()}: servido (arriba)")
    # el corte por proveedor.as_of (sin fecha_corte en la petición)
    m = C.motor()
    m.proveedor.as_of = ult - pd.Timedelta(days=1)
    r = C.servir(m, f, v, p)
    K.comprobar(f"{f}: corte por as_of del proveedor ⇒ RECHAZADO", r["estado"] == "RECHAZADO", str(r.get("detalle"))[:120])
    m.proveedor.as_of = None
    # caché: servido con corte posterior y pedido después con corte anterior
    m = C.motor()
    r1 = C.servir(m, f, v, p, fecha_corte=str(ult.date()))
    r2 = C.servir(m, f, v, p, fecha_corte=str((ult - pd.Timedelta(days=1)).date()))
    K.comprobar(f"{f}: la caché no sirve con un corte anterior", r1["estado"] != "RECHAZADO" and r2["estado"] == "RECHAZADO")

print("   fechas contractuales: ¿se cuela una observación?")
v, p = C.caso("REI-LEV-001", 0)
v2 = copy.deepcopy(v)
v2["componentes"][0]["vencimientos"][0]["fecha"] = "2026-06-29"            # vencimiento ya pasado en la fecha de los datos
r = C.servir(C.motor(), "REI-LEV-001", v2, p, fecha_corte="2026-06-30")
K.comprobar("REI-LEV: vencimiento anterior a la fecha de los datos ⇒ RECHAZADO", r["estado"] == "RECHAZADO", str(r.get("detalle"))[:120])
v2 = copy.deepcopy(v)
v2["fecha"] = "2026-07-01"
r = C.servir(C.motor(), "REI-LEV-001", v2, p, fecha_corte="2026-06-30")
K.comprobar("REI-LEV: fecha de los datos posterior al corte ⇒ RECHAZADO", r["estado"] == "RECHAZADO")
v, p = C.caso("CHR-TOKEN-001", 1)
r0 = C.servir(C.motor(), "CHR-TOKEN-001", v, p, fecha_corte="2026-06-30")
v2 = copy.deepcopy(v)
# un desbloqueo «contractual» fechado después del corte con una cantidad distinta: cambia la cifra (es el dato), se declara
des = v2["tokens"][0]["calendario"]["desbloqueos"]
print("   CHR-TOKEN desbloqueos del caso:", des, "limitaciones:", r0["limitaciones"][:2])

print("2. cotas y coste")
rng = np.random.default_rng(7)
u = fichas_p2.UMBRALES


def medir(etiqueta, ficha, valores, params, espera_cota):
    m = C.motor()
    t0 = time.time()
    r, exc, nrc = C.llamar(m, C.peticion(ficha, valores, params))
    dt = time.time() - t0
    det = (exc or str(r.get("detalle") or ""))[:150]
    por_cota = (not exc) and r["estado"] == "RECHAZADO" and ("máximo" in det or "maxim" in det or "más de" in det or "fuera de" in det
                                                             or "[" in det and "]" in det)
    if espera_cota:
        K.comprobar(f"{etiqueta}: RECHAZADO por la cota en {dt:.2f} s", por_cota and dt < 10 and nrc == 1, det)
    else:
        K.comprobar(f"{etiqueta}: en el máximo no se rechaza por la cota; {('servido' if not exc and r['estado'] != 'RECHAZADO' else 'rechazado: ' + det[:90])} en {dt:.1f} s",
                    not exc and nrc == 1 and dt < 90 and not (r["estado"] == "RECHAZADO" and ("máximo" in det and "elementos" in det)), det)
    return r, dt


def comp_fc(i):
    return {"id": f"C{i}", "capitalizacion": float(rng.uniform(20, 900)), "volatilidad_acciones": float(rng.uniform(0.15, 0.9)),
            "deuda_corto": float(rng.uniform(1, 300)), "deuda_largo": float(rng.uniform(5, 800)), "mu_historico": 0.05}


v, p = C.caso("FIR-CRED-001", 1)
for n, cota in ((500, False), (501, True)):
    medir(f"FIR-CRED componentes {n}", "FIR-CRED-001", {**v, "componentes": [comp_fc(i) for i in range(n)]}, p, cota)
medir("FIR-CRED T = 30", "FIR-CRED-001", v, {"T": 30}, False)
medir("FIR-CRED T = 30.001", "FIR-CRED-001", v, {"T": 30.001}, True)
# caso caro: 500 componentes muy apalancados y T = 30 (raíces anidadas)
vx = {**v, "componentes": [{**comp_fc(i), "capitalizacion": 1e-3 * (i + 1), "deuda_corto": 1e6, "volatilidad_acciones": 9.9} for i in range(500)]}
medir("FIR-CRED 500 componentes extremos (E ≪ D, σ_E 990 %, T 30)", "FIR-CRED-001", vx, {"T": 30}, False)

nb = list(u["FX-BEER-001"]["fundamentales"])
for n, cota in ((400, False), (401, True)):
    fq = pd.date_range("1900-03-31", periods=n, freq="QE")
    X = np.cumsum(rng.normal(0, 0.02, (n, 4)), axis=0)
    q = 4.6 + X @ np.array([0.5, 0.8, 0.3, 1.2]) + rng.normal(0, 0.02, n)
    vb = {"vintage": str(fq[-1].date()), "serie": [{"fecha": str(d.date()), "reer": float(math.exp(q[i])), **{k: float(X[i, j]) for j, k in enumerate(nb)}}
                                                   for i, d in enumerate(fq)]}
    for met in ("DOLS", "Johansen"):
        medir(f"FX-BEER serie {n} trimestres, {met}, retardos 4", "FX-BEER-001", vb, {"metodo": met, "retardos": 4}, cota)
vb0, _ = C.caso("FX-BEER-001", 0)
medir("FX-BEER retardos 5", "FX-BEER-001", vb0, {"retardos": 5}, True)

for n, tr, cota in ((1200, 1000, False), (1201, 6, True), (372, 1001, True)):
    fm = pd.date_range("1920-01-31", periods=n, freq="ME")
    vc = {"moneda": "USD", "ipc_moneda": "USD", "serie": [{"fecha": str(d.date()), "precio": float(50 + i % 17), "ipc": 100.0 + i} for i, d in enumerate(fm)],
          "curva_costes": {"fecha": str(fm[-5].date()), "fuente": "x", "tramos": [{"coste": 10.0 + j, "produccion": 1.0 + j % 5} for j in range(tr)]}}
    medir(f"CMD-REAL serie {n} meses, {tr} tramos", "CMD-REAL-001", vc, {}, cota)

v, p = C.caso("REI-LEV-001", 0)
c0 = v["componentes"][0]


def comp_rl(i, nv=3):
    imp = [10.0 + (i + j) % 7 for j in range(nv)]
    return {**copy.deepcopy(c0), "id": f"R{i}", "deuda": float(sum(imp)),
            "vencimientos": [{"fecha": str((pd.Timestamp("2026-07-01") + pd.Timedelta(days=j)).date()), "importe": x, "coste": 0.02} for j, x in enumerate(imp)]}


for n, nv, cota in ((500, 100, False), (501, 3, True), (3, 101, True)):
    medir(f"REI-LEV {n} componentes × {nv} vencimientos", "REI-LEV-001", {**v, "componentes": [comp_rl(i, nv) for i in range(n)]}, p, cota)
medir("REI-LEV 12 caídas", "REI-LEV-001", v, {"caidas_valor": [-0.05 * (i + 1) for i in range(12)]}, False)
medir("REI-LEV 13 caídas", "REI-LEV-001", v, {"caidas_valor": [-0.05 * (i + 1) for i in range(13)]}, True)

fuente = {"nombre": "F", "metodologia": "m", "filtros": "f"}
for n, w, cota in ((10950, 365, False), (10951, 90, True), (800, 366, True)):
    fd = pd.date_range("1990-01-01", periods=n, freq="D")
    vo = {"fuente": fuente, "serie": [{"fecha": str(d.date()), "capitalizacion": 1e9 + i * 1e5, "capitalizacion_realizada": 8e8 + i * 5e4,
                                       "volumen_ajustado": 5e7 + (i % 13) * 1e6} for i, d in enumerate(fd)]}
    medir(f"CHR-ONCHAIN {n} días, media_nvt {w}", "CHR-ONCHAIN-001", vo, {"media_nvt": w}, cota)

v, p = C.caso("CHR-TOKEN-001", 1)
t0_ = v["tokens"][0]


def tok(i, nd=4):
    return {**copy.deepcopy(t0_), "id": f"T{i}", "calendario": {"fuente": "doc", "desbloqueos": [
        {"fecha": str((pd.Timestamp("2026-07-01") + pd.Timedelta(days=j)).date()), "cantidad": 1000.0} for j in range(nd)]}}


for n, nd, cota in ((500, 1000, False), (501, 4, True), (2, 1001, True)):
    medir(f"CHR-TOKEN {n} tokens × {nd} desbloqueos, 12 ventanas", "CHR-TOKEN-001", {**v, "tokens": [tok(i, nd) for i in range(n)]},
          {"ventanas_desbloqueo": [10950 - i for i in range(12)]}, cota)
medir("CHR-TOKEN 13 ventanas", "CHR-TOKEN-001", v, {"ventanas_desbloqueo": list(range(1, 14))}, True)
medir("CHR-TOKEN ventana 10951 d", "CHR-TOKEN-001", v, {"ventanas_desbloqueo": [10951]}, True)

for n, cota in ((10000, False), (10001, True)):
    ff = pd.date_range("1990-01-01", periods=n, freq="D")
    fl = [{"fecha": str(d.date()), "aportacion": 1.0 if i < n // 2 else 0.0, "distribucion": 0.0 if i < n // 2 else 1.3} for i, d in enumerate(ff)]
    niv = [{"fecha": str(d.date()), "nivel": 100.0 + i * 0.01} for i, d in enumerate(ff)]
    vp = {"moneda": "USD", "flujos": fl, "nav_final": {"fecha": str(ff[-1].date()), "valor": 10.0},
          "indice": {"nombre": "I", "moneda": "USD", "rentabilidad_total": True, "riesgo_comparable": "sí", "niveles": niv}}
    medir(f"PRV-PME {n} flujos", "PRV-PME-001", vp, {"metodo": "PME+"}, cota)
    medir(f"PRV-CF {n} flujos y {n} NAV", "PRV-CF-001", {"compromiso": 1e4, "flujos": fl, "navs": [{"fecha": x["fecha"], "valor": 5.0} for x in fl],
                                                        "vida_anios": 30}, {"tasas_aportacion": [0.1] * 30, "crecimiento": 0.1}, cota)
vcf, _ = C.caso("PRV-CF-001", 0)
medir("PRV-CF 31 tasas", "PRV-CF-001", vcf, {"tasas_aportacion": [0.1] * 31, "crecimiento": 0.1}, True)
medir("PRV-CF vida 31", "PRV-CF-001", {**vcf, "vida_anios": 31}, {"tasas_aportacion": [0.1], "crecimiento": 0.1}, True)
medir("PRV-CF bow 5.001", "PRV-CF-001", vcf, {"bow": 5.001}, True)
vpm, _ = C.caso("PRV-PME-001", 1)
v2 = copy.deepcopy(vpm)
v2["flujos"][0]["fecha"] = "1919-01-01"
v2["indice"]["niveles"].append({"fecha": "1919-01-01", "nivel": 1.0})
medir("PRV-PME flujos de más de 100 años", "PRV-PME-001", v2, {}, True)

for n, k, cota in ((1200, 12, False), (1201, 7, True), (48, 13, True)):
    fm = pd.date_range("1920-01-31", periods=n, freq="ME")
    nom = [f"F{j}" for j in range(k)]
    Fx = rng.normal(0, 3, (n, k))
    vh = {"serie": [{"fecha": str(d.date()), "r": float(Fx[i].sum() * 0.1 + rng.normal()), "rf": 0.1, **{nm: float(Fx[i, j]) for j, nm in enumerate(nom)}}
                    for i, d in enumerate(fm)]}
    medir(f"ALT-HF {n} meses, {k} factores", "ALT-HF-001", vh, {"factores": nom}, cota)

for n, anios, kc, cota in ((50000, 100, 20, False), (50001, 5, 2, True), (600, 101, 2, True), (600, 5, 21, True)):
    tr = []
    for i in range(n):
        a = (i * 37 + (i // 2) * 11) % anios if i % 2 else (i // 2 * 13) % anios
        tr.append({"id_pieza": f"P{i // 2}", "fecha": f"{1900 + a}-{1 + i % 12:02d}-15", "precio": float(100 * math.exp(0.03 * a + 0.2 * math.sin(i))),
                   "caracteristicas": {f"c{j}": float(math.sin(i * (j + 1) * 0.7)) for j in range(kc)}})
    for met in (("ventas_repetidas", "hedonico") if not cota else ("ventas_repetidas",)):
        medir(f"ALT-AUC {n} transacciones, {anios} años, {kc} características, {met}", "ALT-AUC-001", {"categoria": "c", "transacciones": tr},
              {"metodo": met, "comisiones": 0.25}, cota)
medir("ALT-AUC comisiones 0.2501", "ALT-AUC-001", C.caso("ALT-AUC-001", 0)[0], {"comisiones": 0.2501}, True)
medir("ALT-AUC comisiones 0.0999", "ALT-AUC-001", C.caso("ALT-AUC-001", 0)[0], {"comisiones": 0.0999}, True)

print("3. configuración")
vb0, _ = C.caso("FX-BEER-001", 0)
cfg = cargar_config()
base = C.servir(C.motor(), "FX-BEER-001", vb0, {})["resultado"]
cfg2 = copy.deepcopy(cfg)
cfg2["evaluacion"]["nivel_ic"] = 0.5
m = C.motor(cfg2)
r = C.servir(m, "FX-BEER-001", vb0, {})
x = r["resultado"]
amp0 = base["ic_desalineamiento_pct"][1] - base["ic_desalineamiento_pct"][0]
amp = x["ic_desalineamiento_pct"][1] - x["ic_desalineamiento_pct"][0]
from scipy import stats  # noqa: E402
K.comprobar(f"FX-BEER sigue evaluacion.nivel_ic del Motor ({base['nivel_ic']} → {x['nivel_ic']})", x["nivel_ic"] == 0.5 and base["nivel_ic"] == cfg["evaluacion"]["nivel_ic"])
K.cerca("la amplitud del IC (en logaritmos) escala con z(0,75)/z(0,95)",
        (math.log1p(x["ic_desalineamiento_pct"][1] / 100) - math.log1p(x["ic_desalineamiento_pct"][0] / 100))
        / (math.log1p(base["ic_desalineamiento_pct"][1] / 100) - math.log1p(base["ic_desalineamiento_pct"][0] / 100)),
        stats.norm.ppf(0.75) / stats.norm.ppf(0.95), 1e-9)
e = m.almacen.estado("RC")[r["calc_id"]]
usada = e["artefacto"].get("configuracion_usada")
print("   configuracion_usada:", str(usada)[:200])
K.comprobar("el artefacto guarda la sección de la configuración usada (evaluacion, nivel_ic 0,5)", isinstance(usada, dict)
            and "evaluacion" in usada and usada["evaluacion"]["valor"]["nivel_ic"] == 0.5)
m.cfg["evaluacion"]["nivel_ic"] = 0.99
re_ = m.reejecutar(r["calc_id"], "QA: tras cambiar la configuración")
K.comprobar(f"CT-10 tras cambiar la configuración ⇒ SI ({re_.get('coincide')})", re_.get("coincide") == "SI")
r3 = C.servir(m, "FX-BEER-001", vb0, {})
K.comprobar("y un servicio nuevo usa ya la configuración vigente (0,99; no la caché)", r3["resultado"]["nivel_ic"] == 0.99 and not r3.get("cache_hit"),
            f"nivel_ic {r3['resultado'].get('nivel_ic')} cache_hit {r3.get('cache_hit')}")
for malo in (1.5, 0, 1, "0.9", None, float("nan"), True, [0.9]):
    cfg3 = copy.deepcopy(cfg)
    cfg3["evaluacion"]["nivel_ic"] = malo
    r, exc, nrc = C.llamar(C.motor(cfg3), C.peticion("FX-BEER-001", vb0, {}))
    K.comprobar(f"nivel_ic = {malo!r} en la configuración ⇒ RECHAZADO sin excepción", not exc and r["estado"] == "RECHAZADO" and nrc == 1, exc or r["estado"])
# las otras nueve no leen la configuración: su artefacto no guarda nada y un cambio no las mueve
for f in C.P2:
    if f == "FX-BEER-001":
        continue
    v, p = C.caso(f, 1)
    m = C.motor(cfg2)
    r = C.servir(m, f, v, p)
    usada = m.almacen.estado("RC")[r["calc_id"]]["artefacto"].get("configuracion_usada")
    K.comprobar(f"{f}: no lee la configuración ({usada}) y da lo mismo con otra", not usada and r["resultado"] == C.servir(C.motor(), f, v, p)["resultado"])
# Johansen de FX-BEER no usa nivel_ic
r = C.servir(C.motor(cfg2), "FX-BEER-001", vb0, {"metodo": "Johansen"})
K.comprobar("FX-BEER Johansen: nivel_ic null (no hay IC)", r["resultado"]["nivel_ic"] is None)
sys.exit(K.fin())
