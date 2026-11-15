"""QA r01 de T-127 · frontera con el Bloque B (1.6): ¿se reconstruye la cifra de un emisor o token por otras vías?

Vías que no son las de T-119 r02_01 (casi clones a 1e-9, peso casi total, dispersión de 3), todas en UNA petición:
 E. copias a escala: el emisor X repetido con TODOS sus datos multiplicados por 1,02^i (difieren un 2 % > tolerancia de
    clon, pero los cocientes que calcula la ficha son idénticos): FIR-CRED (10), REI-LEV (3), CHR-TOKEN (2 y 7).
 Z. rellenos de cifra nula: X con un peso moderado (< 95 %) y rellenos con PD 0 (FIR-CRED) o deuda neta 0 (REI-LEV);
    la media ponderada dividida por el peso de X (que conoce quien pide) es la cifra de X.
 O. con 7 o más componentes, el máximo de la dispersión es la cifra del componente con mayor valor (declarado).
También: la parte de T-119 r02_01 que no llega a ejecutarse (REI-LEV y CHR-TOKEN) con la dispersión `null`, y
`verificar_casos_control` de las 80 fichas.
Uso: .venv/bin/python -I .docs/tickets/T-127/revisores/r01_01_frontera_otras_vias.py [ejecutor]
"""
import copy
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "T-118" / "revisores"))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
from bloque_a.motor import fichas_p2 as P  # noqa: E402

K = C.Contador("r01_01 T-127 frontera, otras vías")
m = C.motor()


def servir(f, valores, parametros=None):
    p = C.peticion(f)
    p["datos"][0]["valores"] = valores
    if parametros is not None:
        p["parametros"] = parametros
    r, exc, _ = C.servir_contando(m, p)
    if exc is not None:
        return "X", str(exc)
    return ("S", r["resultado"]) if str(r["estado"]).startswith("SERVED") else ("R", r["detalle"])


def escalar(c, k, claves, ident):
    c = copy.deepcopy(c)
    c["id"] = ident
    for q in claves:
        if c.get(q) is not None:
            c[q] = c[q] * k
    return c


def cerca(a, b, tol=1e-9):
    return a is not None and b is not None and abs(a - b) <= tol * max(1.0, abs(b))


fugas = []
# ------------------------------------------------------------------ FIR-CRED-001
print("[FIR-CRED-001] (datos del caso de control 1, «sistema de Merton»)")
v0 = C.valores("FIR-CRED-001", 1)
cifras = [P._fc_directo(V, sV, D) for V, sV, D, _ in P._FC_ACTIVOS]
ix = max(range(len(cifras)), key=lambda i: cifras[i]["pd"])        # el más arriesgado
x0, cx = cifras[ix], v0["componentes"][ix]
print(f"    {cx['id']} a mano (fórmulas directas de la ficha): DD {x0['dd']:.9f} · PD {x0['pd'] * 100:.9f} %")
v = copy.deepcopy(v0)
v["componentes"] = [escalar(cx, 1.02 ** i, ("capitalizacion", "deuda_corto", "deuda_largo"), f"E{i}") for i in range(10)]
st, r = servir("FIR-CRED-001", v, {})
ok = True
if st == "S":
    dd, pd_ = r["neutral_al_riesgo"]["dd"], r["neutral_al_riesgo"]["pd_pct"]
    print(f"    E (10 copias a escala 1,02^i): SERVIDO · DD media {dd['media_ponderada_deuda']:.9f} mín {dd['minimo']:.9f} "
          f"máx {dd['maximo']:.9f} · PD media {pd_['media_ponderada_deuda']:.9f} %")
    ok = not cerca(dd["media_ponderada_deuda"], x0["dd"], 1e-6)
    if not ok:
        fugas.append(f"FIR-CRED-001: 10 copias a escala de {cx['id']} dan su DD y su PD (y la dispersión colapsa en ellas)")
else:
    print(f"    E: {st} {str(r)[:160]}")
K.comprobar("FIR-CRED-001 E: copias a escala no dan la DD de un emisor", ok)

# Z: X con el 30 % o el 60 % de la deuda y 9 rellenos de PD 0 (capitalización enorme frente a la deuda, volatilidad baja)
dX = cx["deuda_corto"] + cx["deuda_largo"]   # la base de pesos de la ficha (deudas.append(corto + largo))
for peso in (0.30, 0.60):
    resto = dX * (1 - peso) / peso
    reparto = [1 + 0.05 * i for i in range(9)]
    rellenos = [{"id": f"Z{i}", "capitalizacion": 1e6 * (1 + 0.1 * i), "volatilidad_acciones": 0.05 + 0.01 * i,
                 "deuda_corto": resto * reparto[i] / sum(reparto), "deuda_largo": 0.0, "mu_historico": 0.05} for i in range(9)]
    v = copy.deepcopy(v0)
    v["componentes"] = [cx] + rellenos
    st, r = servir("FIR-CRED-001", v, {})
    if st != "S":
        print(f"    Z ({peso:.0%}): {st} {str(r)[:200]}")
        continue
    deudas = [dX] + [z["deuda_corto"] for z in rellenos]
    wX = deudas[0] / sum(deudas)
    pd_rec = r["neutral_al_riesgo"]["pd_pct"]["media_ponderada_deuda"] / wX
    print(f"    Z ({cx['id']} con {wX:.1%} de la deuda + 9 rellenos de PD 0): PD media / peso = {pd_rec:.9f} % "
          f"({cx['id']}: {x0['pd'] * 100:.9f} %) · PD máxima {r['neutral_al_riesgo']['pd_pct']['maximo']:.9f} %")
    if cerca(pd_rec, x0["pd"] * 100, 1e-6):
        fugas.append(f"FIR-CRED-001: con rellenos de PD 0, PD media / peso = PD de {cx['id']} (peso {wX:.0%} < 95 %)")
    K.comprobar(f"FIR-CRED-001 Z{peso:.0%}: rellenos de PD 0 no dan la PD de un emisor", not cerca(pd_rec, x0["pd"] * 100, 1e-6))
    K.comprobar(f"FIR-CRED-001 O{peso:.0%}: el máximo de la PD no es la de un emisor (declarado en INC-T127-01)",
                not cerca(r["neutral_al_riesgo"]["pd_pct"]["maximo"], x0["pd"] * 100, 1e-6))

# ------------------------------------------------------------------ REI-LEV-001
print("\n[REI-LEV-001]")
v0 = C.valores("REI-LEV-001")
S1 = v0["componentes"][0]
ltv1, icr1 = (S1["deuda"] - S1["caja"]) / S1["gav"] * 100, S1["ebitda"] / S1["gastos_financieros"]
st, r0 = servir("REI-LEV-001", copy.deepcopy(v0))
print(f"    caso de control (3): estado {st}; dispersión {r0.get('dispersion') if st == 'S' else r0}")
K.comprobar("REI-LEV-001: con 3 componentes la dispersión es null y se declara",
            st == "S" and r0["dispersion"] is None)
NUM = ("gav", "deuda", "caja", "ebitda", "gastos_financieros", "ffo")
for n in (3, 7):
    v = copy.deepcopy(v0)
    comps = []
    for i in range(n):
        c = escalar(S1, 1.02 ** i, NUM, f"E{i}")
        for vto in c["vencimientos"]:
            vto["importe"] *= 1.02 ** i
        comps.append(c)
    v["componentes"] = comps
    st, r = servir("REI-LEV-001", v)
    if st == "S":
        print(f"    E ({n} copias de S1 a escala): SERVIDO · LTV {r['ltv_pct']:.9f} (S1 {ltv1:.9f}) · ICR {r['icr_veces']:.9f} (S1 {icr1:.9f})"
              f" · impacto FFO {r['impacto_ffo_pct']:.6f}")
        if cerca(r["ltv_pct"], ltv1) and cerca(r["icr_veces"], icr1):
            fugas.append(f"REI-LEV-001: {n} copias de S1 a escala dan su LTV, ICR, impacto en FFO y holguras")
    else:
        print(f"    E ({n}): {st} {str(r)[:160]}")
    K.comprobar(f"REI-LEV-001 E{n}: copias a escala no dan el LTV y el ICR de S1",
                not (st == "S" and cerca(r["ltv_pct"], ltv1) and cerca(r["icr_veces"], icr1)))

# ------------------------------------------------------------------ CHR-TOKEN-001
print("\n[CHR-TOKEN-001]")
v0 = C.valores("CHR-TOKEN-001", 1)
T = v0["tokens"][0]
infl = (T["emision_anual"] - T["quema_anual"]) / T["oferta_circulante"] * 100
for n in (2, 7):
    v = copy.deepcopy(v0)
    toks = []
    for i in range(n):
        t = escalar(T, 1.02 ** i, ("oferta_circulante", "oferta_total", "oferta_maxima", "emision_anual", "quema_anual"), f"E{i}")
        for d in (t.get("calendario") or {}).get("desbloqueos", []):
            d["cantidad"] *= 1.02 ** i
        toks.append(t)
    v["tokens"] = toks
    st, r = servir("CHR-TOKEN-001", v, {})
    if st == "S":
        print(f"    E ({n} copias de TKA a escala): SERVIDO · inflación neta {r['inflacion_neta_pct_anual']:.9f} (TKA {infl:.9f}) · "
              f"dilución 90 d {r['desbloqueos_pct']}")
        if cerca(r["inflacion_neta_pct_anual"], infl):
            fugas.append(f"CHR-TOKEN-001: {n} copias de TKA a escala dan su inflación neta y su dilución como «sector»")
    else:
        print(f"    E ({n}): {st} {str(r)[:160]}")
    K.comprobar(f"CHR-TOKEN-001 E{n}: copias a escala no dan la inflación neta de un token",
                not (st == "S" and cerca(r["inflacion_neta_pct_anual"], infl)))

# ------------------------------------------------------------------ casos de control
print("\n[casos de control]")
rc = m.verificar_casos_control()
mal = {f: x for f, x in rc.items() if not (x.get("superados") if isinstance(x, dict) else x)}
print(f"    fichas: {len(rc)} · no superadas: {sorted(mal)[:10]}")
K.comprobar("verificar_casos_control: todas las fichas con casos (66 + AUD-REX) superadas, las tres de T-127 entre ellas",
            not mal and len(rc) == 67 and {"FIR-CRED-001", "REI-LEV-001", "CHR-TOKEN-001"} <= set(rc), f"{len(rc)} {sorted(mal)[:5]}")

print("\n== vías que dan la cifra de un solo emisor o token:")
for f in fugas:
    print("   ", f)
sys.exit(K.fin())
