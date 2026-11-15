"""QA r02 de T-119 · frontera con el Bloque B (1.6): ¿se sacan las cifras de un solo emisor o token tras la r02?

Vías (ninguna es un clon exacto ni un solo componente, que la r02 ya rechaza):
 A. casi clones: el emisor X repetido con una diferencia relativa de 1e-9 por copia (FIR-CRED: 10; REI-LEV: 3; CHR-TOKEN: 2);
 B. un componente con peso casi total: X y relleno de tamaño 1e-6 de X;
 C. la dispersión: con 3 componentes, mínimo, mediana y máximo son las tres cifras individuales.
Se mide si la salida da la cifra de X (comparada con la de X calculada a mano con la fórmula de la ficha, o con la dispersión
del caso de control) y si dos emisores quedan ordenados.
Uso: .venv/bin/python -I .docs/tickets/T-119/revisores/r02_01_frontera_b.py [ejecutor]
"""
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "T-118" / "revisores"))
import r01_comun as C118  # noqa: E402   (utilidades de la QA r01 de T-118: Motor con Almacén temporal)

C118.preparar(sys.argv)

K = C118.Contador("r02_01 T-119 frontera con B")
m = C118.motor()


def servir(f, valores):
    p = C118.peticion(f)
    p["datos"][0]["valores"] = valores
    r, exc, n = C118.servir_contando(m, p)
    if exc is not None:
        return "X", str(exc)
    return ("S", r) if str(r["estado"]).startswith("SERVED") else ("R", r["detalle"])


def escala(c, k, claves, ident):
    c = copy.deepcopy(c)
    c["id"] = ident
    for q in claves:
        c[q] = c[q] * k
    return c


fugas = []
# ------------------------------------------------------------------ FIR-CRED-001
print("[FIR-CRED-001] casi clones (10 copias de un emisor, diferencia relativa 1e-9 en la capitalización)")
v0 = C118.valores("FIR-CRED-001")
dds = {}
for x in ("C00", "C05", "C09"):
    base = next(c for c in v0["componentes"] if c["id"] == x)
    v = copy.deepcopy(v0)
    v["componentes"] = [escala(base, 1 + i * 1e-9, ("capitalizacion",), f"{x}-{i}") for i in range(10)]
    st, r = servir("FIR-CRED-001", v)
    if st == "S":
        dd = r["resultado"]["neutral_al_riesgo"]["dd"]
        dds[x] = dd["mediana"]
        print(f"    {x}: SERVIDO · DD mediana {dd['mediana']:.6f} · mínimo {dd['minimo']:.6f} · máximo {dd['maximo']:.6f}")
    else:
        print(f"    {x}: {st} {str(r)[:150]}")
if len(dds) == 3:
    fugas.append(f"FIR-CRED-001: DD de un emisor con 10 casi clones: {dds}")
K.comprobar("FIR-CRED-001: 10 casi clones de un emisor no dan su DD", len(dds) < 2, str(dds))
v = copy.deepcopy(v0)
big = next(c for c in v0["componentes"] if c["id"] == "C00")
v["componentes"] = [big] + [escala(c, 1e-6, ("capitalizacion", "deuda_corto", "deuda_largo"), c["id"]) for c in v0["componentes"][1:10]]
st, r = servir("FIR-CRED-001", v)
if st == "S":
    print(f"    peso casi total (C00 + 9 a escala 1e-6): media ponderada por deuda DD {r['resultado']['neutral_al_riesgo']['dd']['media_ponderada_deuda']:.4f}")

# ------------------------------------------------------------------ REI-LEV-001
print("\n[REI-LEV-001]")
v0 = C118.valores("REI-LEV-001")
st, r0 = servir("REI-LEV-001", copy.deepcopy(v0))
disp0 = r0["resultado"]["dispersion"]["ltv_pct"]
ltv_ind = {c["id"]: (c["deuda"] - c["caja"]) / c["gav"] * 100 for c in v0["componentes"]}
print(f"    caso de control (3 componentes): dispersión LTV {disp0} · LTV de cada uno a mano {ltv_ind}")
trio = sorted([disp0["minimo"], disp0["mediana"], disp0["maximo"]])
K.comprobar("REI-LEV-001: con 3 componentes la dispersión no da las tres cifras individuales",
            sorted(round(x, 9) for x in ltv_ind.values()) != [round(x, 9) for x in trio], f"{trio} = {sorted(ltv_ind.values())}")
if sorted(round(x, 9) for x in ltv_ind.values()) == [round(x, 9) for x in trio]:
    fugas.append(f"REI-LEV-001: mínimo/mediana/máximo = LTV de los tres componentes {trio}")
S = {c["id"]: c for c in v0["componentes"]}
res_cc = {}
for x in S:
    v = copy.deepcopy(v0)
    v["componentes"] = [escala(S[x], 1 + i * 1e-9, ("gav",), f"{x}-{i}") for i in range(3)]
    st, r = servir("REI-LEV-001", v)
    res_cc[x] = (st, r["resultado"]["ltv_pct"] if st == "S" else str(r)[:120])
print(f"    casi clones (3 copias, 1e-9): {res_cc}")
K.comprobar("REI-LEV-001: 3 casi clones de un emisor no dan su LTV", not all(s == "S" for s, _ in res_cc.values()), str(res_cc))
if all(s == "S" for s, _ in res_cc.values()):
    fugas.append(f"REI-LEV-001 casi clones: {res_cc}")
res_peso = {}
for x in S:
    v = copy.deepcopy(v0)
    otros = [c for c in v0["componentes"] if c["id"] != x]
    v["componentes"] = [S[x]] + [escala(c, 1e-6, ("gav", "deuda", "caja", "ebitda", "gastos_financieros", "ffo"), c["id"]) for c in otros]
    for c in v["componentes"][1:]:
        for vto in c["vencimientos"]:
            vto["importe"] *= 1e-6
    st, r = servir("REI-LEV-001", v)
    res_peso[x] = (st, round(r["resultado"]["ltv_pct"], 6) if st == "S" else str(r)[:120], round(ltv_ind[x], 6),
                   round(r["resultado"]["icr_veces"], 6) if st == "S" else None, round(S[x]["ebitda"] / S[x]["gastos_financieros"], 6))
print(f"    peso casi total (X + 2 a escala 1e-6): (estado, LTV agregado, LTV de X, ICR agregado, ICR de X) {res_peso}")
casi = [x for x, t in res_peso.items() if t[0] == "S" and abs(t[1] - t[2]) < 1e-3]
K.comprobar("REI-LEV-001: un componente con peso casi total no da su LTV", not casi, str(res_peso))
if casi:
    fugas.append(f"REI-LEV-001 peso casi total: LTV agregado = LTV del emisor en {casi}")

# ------------------------------------------------------------------ CHR-TOKEN-001
print("\n[CHR-TOKEN-001]")
v0 = C118.valores("CHR-TOKEN-001")
T = v0["tokens"][0]
v = copy.deepcopy(v0)
v["tokens"] = [T, escala(T, 1 + 1e-9, ("precio",), "TKA-bis")]
st, r = servir("CHR-TOKEN-001", v)
print(f"    TKA + casi clon, ámbito sector: {st} · {r['resultado']['capitalizacion_circulante'] if st == 'S' else str(r)[:150]} (TKA solo: {T['precio'] * T['oferta_circulante']:.0f})")
K.comprobar("CHR-TOKEN-001: un token y su casi clon no dan sus cifras como sector", st != "S", str(r)[:120])
if st == "S":
    fugas.append("CHR-TOKEN-001: un token y su casi clon se sirven como sector")
v = copy.deepcopy(v0)
v["tokens"] = [T, escala(v0["tokens"][1], 1e-9, ("precio",), "relleno")]
st, r = servir("CHR-TOKEN-001", v)
print(f"    TKA + relleno de precio 1e-9: {st} · capitalización {r['resultado']['capitalizacion_circulante'] if st == 'S' else str(r)[:120]}")

# ------------------------------------------------------------------ REI-NAV-001 (T-112; r02 le pone mínimo 2)
print("\n[REI-NAV-001] (fuera de las 10 P2; la r02 le pone un mínimo de 2 componentes)")
st, r = servir("REI-NAV-001", C118.valores("REI-NAV-001"))
print(f"    claves del resultado: {sorted(r['resultado']) if st == 'S' else r}")
if st == "S" and isinstance(r["resultado"].get("componentes"), dict):
    print(f"    filas por componente con su identificador: {list(r['resultado']['componentes'])} → {[(k, round(c['prima_pct'], 3)) for k, c in r['resultado']['componentes'].items()]}")

print("\n== vías que dan las cifras de un solo emisor o token:")
for f in fugas:
    print("   ", f)
sys.exit(K.fin())
