"""QA r01 de T-119 · frontera con el Bloque B (1.6 del Catálogo, 2.4–2.5 y R21): ¿se pueden sacar cifras por emisor,
activo o token concreto de FIR-CRED-001, REI-LEV-001 y CHR-TOKEN-001?

 1. Ningún resultado (ni limitación) lleva identificadores de componente ni una lista con una fila por componente.
 2. Agregado de un solo componente: REI-LEV-001 y CHR-TOKEN-001 con uno; FIR-CRED-001 con 10 copias del mismo emisor (ids
    distintos). Si se sirve, la cifra del «agregado» es la del emisor.
 3. Mínimo y máximo de la dispersión: con dos componentes son las dos cifras individuales.
 4. Diferencia entre dos peticiones (con y sin un componente): recupera la cifra del componente (inherente a un agregado).
"""
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
K = C.Contador("r01_08 frontera con el Bloque B")
m = C.motor()

print("1. identificadores y filas por componente")
for f, clave, i in (("FIR-CRED-001", "componentes", 1), ("REI-LEV-001", "componentes", 0), ("CHR-TOKEN-001", "tokens", 1)):
    v, p = C.caso(f, i)
    for j, c in enumerate(v[clave]):
        c["id"] = f"EMISOR_SECRETO_{j:03d}"
    r = C.servir(m, f, v, p)
    txt = json.dumps({"resultado": r["resultado"], "limitaciones": r["limitaciones"]}, ensure_ascii=False)
    K.comprobar(f"{f}: ningún identificador de componente en el resultado ni en las limitaciones", "EMISOR_SECRETO" not in txt)
    n = len(v[clave])

    def listas(x, ruta=""):
        if isinstance(x, dict):
            for k, val in x.items():
                yield from listas(val, f"{ruta}.{k}")
        elif isinstance(x, list):
            yield ruta, len(x)
            for val in x:
                yield from listas(val, ruta + "[]")
    por_comp = [(ru, ln) for ru, ln in listas(r["resultado"]) if ln == n and "advertencias" not in ru and n > 3]
    K.comprobar(f"{f}: ninguna lista con una fila por componente ({n})", not por_comp, str(por_comp))
    # mensajes de rechazo: ¿llevan el id?
    v2 = copy.deepcopy(v)
    v2[clave][1]["id"] = v2[clave][0]["id"]
    r2 = C.servir(m, f, v2, p)
    K.comprobar(f"{f}: el rechazo por ids repetidos no cita el id", r2["estado"] == "RECHAZADO" and "EMISOR_SECRETO" not in r2["detalle"], r2.get("detalle", "")[:120])

print("2. agregado de un solo componente")
v, p = C.caso("REI-LEV-001", 0)
uno = {**v, "componentes": [v["componentes"][1]]}
r = C.servir(m, "REI-LEV-001", uno, p)
c = v["componentes"][1]
if r["estado"] != "RECHAZADO":
    x = r["resultado"]
    print(f"   REI-LEV-001 con 1 componente: {r['estado']}; LTV {x['ltv_pct']:.4f} % = (deuda − caja)/GAV del emisor {(c['deuda'] - c['caja']) / c['gav'] * 100:.4f} %; "
          f"ICR {x['icr_veces']:.4f} = {c['ebitda'] / c['gastos_financieros']:.4f}; holgura LTV {x['covenants'] and x['covenants']['holgura_ltv_pp']['mediana']}; "
          f"limitaciones: {r['limitaciones']}")
K.comprobar("REI-LEV-001 con un solo componente ⇒ RECHAZADO (o, al menos, declarado en limitaciones)", r["estado"] == "RECHAZADO"
            or any("un solo" in s or "1 componente" in s or "un componente" in s for s in r["limitaciones"]), f"{r['estado']}: entrega LTV, ICR, vencimientos, impacto en FFO y holgura de covenants del emisor")
# con ello se ordenan emisores: una petición por emisor
orden = []
for c in v["componentes"]:
    r = C.servir(m, "REI-LEV-001", {**v, "componentes": [c]}, p)
    if r["estado"] != "RECHAZADO":
        orden.append((r["resultado"]["ltv_pct"], c["id"]))
print("   emisores ordenados por LTV con una petición por emisor:", sorted(orden))
K.comprobar("REI-LEV-001: no se puede ordenar emisores por LTV con una petición por emisor", len(orden) < 2, str(sorted(orden)))

v, p = C.caso("FIR-CRED-001", 1)
r9 = C.servir(m, "FIR-CRED-001", {**v, "componentes": v["componentes"][:9]}, p)
K.comprobar("FIR-CRED-001 con 9 componentes ⇒ RECHAZADO", r9["estado"] == "RECHAZADO")
orden = []
for c in v["componentes"][:4]:
    clones = [{**c, "id": f"{c['id']}_{j}"} for j in range(10)]
    r = C.servir(m, "FIR-CRED-001", {**v, "componentes": clones}, p)
    if r["estado"] != "RECHAZADO":
        orden.append((round(r["resultado"]["neutral_al_riesgo"]["dd"]["mediana"], 6), round(r["resultado"]["neutral_al_riesgo"]["pd_pct"]["mediana"], 6), c["id"]))
print("   FIR-CRED-001 con 10 copias del mismo emisor (ids distintos): (DD, PD %, emisor)", orden)
K.comprobar("FIR-CRED-001: 10 copias idénticas de un emisor ⇒ RECHAZADO (el mínimo de 10 no se burla clonando)", not orden, f"{len(orden)} servidas")

v, p = C.caso("CHR-TOKEN-001", 1)
r = C.servir(m, "CHR-TOKEN-001", {**v, "tokens": [v["tokens"][0]]}, p)
print(f"   CHR-TOKEN-001 con 1 token (ámbito «{v['ambito']}»): {r['estado']}; la ficha lo admite «cuando el ámbito es la propia red»; limitaciones: {r['limitaciones']}")
K.comprobar("CHR-TOKEN-001 con un token y ámbito de sector ⇒ RECHAZADO o declarado (la ficha solo lo admite si el ámbito es la propia red)",
            r["estado"] == "RECHAZADO" or any("un solo" in s or "propia red" in s or "1 token" in s for s in r["limitaciones"]), r["estado"])

print("3. mínimo y máximo de la dispersión con dos componentes")
v, p = C.caso("REI-LEV-001", 0)
dos = {**v, "componentes": v["componentes"][:2]}
r = C.servir(m, "REI-LEV-001", dos, p)
if r["estado"] != "RECHAZADO":
    d = r["resultado"]["dispersion"]["ltv_pct"]
    ind = sorted((c["deuda"] - c["caja"]) / c["gav"] * 100 for c in dos["componentes"])
    print(f"   REI-LEV-001 con 2: dispersión LTV mínimo/máximo {d['minimo']:.4f}/{d['maximo']:.4f} = LTV de cada emisor {ind}")
    K.comprobar("(informativo) con 2 componentes, mínimo y máximo son las dos cifras individuales (sin saber de quién)", abs(d["minimo"] - ind[0]) < 1e-9 and abs(d["maximo"] - ind[1]) < 1e-9)

print("4. diferencia entre peticiones (inherente a cualquier agregado)")
v, p = C.caso("FIR-CRED-001", 1)
extra = {**v["componentes"][0], "id": "NUEVO", "capitalizacion": 33.0, "deuda_corto": 70.0}
a = C.servir(m, "FIR-CRED-001", v, p)["resultado"]
b = C.servir(m, "FIR-CRED-001", {**v, "componentes": v["componentes"] + [extra]}, p)["resultado"]
D0 = sum(c["deuda_corto"] + c["deuda_largo"] for c in v["componentes"])
De = extra["deuda_corto"] + extra["deuda_largo"]
pd_e = (b["neutral_al_riesgo"]["pd_pct"]["media_ponderada_deuda"] * (D0 + De) - a["neutral_al_riesgo"]["pd_pct"]["media_ponderada_deuda"] * D0) / De
print(f"   PD del emisor añadido recuperada por diferencia de las medias ponderadas: {pd_e:.6f} % (máximo del segmento con él: {b['neutral_al_riesgo']['pd_pct']['maximo']:.6f} %)")
sys.exit(K.fin())
