"""QA r02 de T-112 · H-07 de la r01 generalizado: datos en línea fechados después de la fecha de corte, y caché.

 1. Para cada ficha de la Fase 2 cuyo caso de control trae fechas ISO en `valores`: se sirve con `fecha_corte` = la última
    fecha de los datos (debe servirse igual que sin corte) y con `fecha_corte` = un día antes de la última fecha, y diez
    años antes de la primera (ningún dato era conocible): debe RECHAZAR, o al menos declararlo como limitación.
 2. Caché: la misma petición con dos fechas de corte no comparte entrada; con la misma, CACHE_HIT; el resultado que
    devuelve la caché no se puede corromper mutando la respuesta anterior.
 3. Serie de HT-01 con `as_of` del proveedor y `fecha_corte` anterior / posterior.
Uso: .venv/bin/python -I r02_03_fecha_corte_y_cache.py
"""
import copy
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

C.preparar(["x"])
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402

K = C.Contador("r02_03 fecha de corte y caché")
_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def aplanar(x):
    if isinstance(x, dict):
        return {k: aplanar(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [aplanar(v) for v in x]
    if isinstance(x, np.ndarray):
        return [aplanar(v) for v in x.tolist()]
    if isinstance(x, np.generic):
        return x.item()
    if isinstance(x, (dt.date, pd.Timestamp)):
        return str(x)[:10]
    return x


def fechas(x, ruta=""):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from fechas(v, f"{ruta}.{k}")
    elif isinstance(x, list):
        for v in x:
            yield from fechas(v, ruta + "[]")
    elif isinstance(x, str) and _ISO.match(x):
        yield ruta, x


def base(f, i=0):
    c = servicio.CASOS_CONTROL[f][i]
    return {"operacion": f, "datos": aplanar(copy.deepcopy(c.get("datos") or [])), "parametros": dict(c.get("parametros") or {}),
            "fecha_corte": c.get("fecha_corte")}


print("1. datos en línea posteriores a la fecha de corte")
sin_fechas, fugas, parciales, rotas = [], [], [], []
for f in sorted(servicio.FASE2):
    hallado = False
    for i in range(len(servicio.CASOS_CONTROL[f])):
        pet = base(f, i)
        fs = sorted(fechas(pet["datos"]), key=lambda t: t[1])
        if not fs:
            continue
        ref = C.motor().servir(copy.deepcopy(pet), "AG-18")
        if ref["estado"] == "RECHAZADO":
            continue
        hallado = True
        ultima, primera = fs[-1][1], fs[0][1]
        claves_ultima = sorted({r for r, x in fs if x == ultima})
        r_igual = C.motor().servir({**copy.deepcopy(pet), "fecha_corte": ultima}, "AG-18")
        if r_igual["estado"] == "RECHAZADO":
            rotas.append((f, i, ultima, r_igual["detalle"][:100]))
        antes = (dt.date.fromisoformat(ultima) - dt.timedelta(days=1)).isoformat()
        r1 = C.motor().servir({**copy.deepcopy(pet), "fecha_corte": antes}, "AG-18")
        muy_antes = (dt.date.fromisoformat(primera) - dt.timedelta(days=3653)).isoformat()
        r2 = C.motor().servir({**copy.deepcopy(pet), "fecha_corte": muy_antes}, "AG-18")
        for nombre, r, corte in (("un día antes de la última fecha", r1, antes), ("diez años antes de la primera", r2, muy_antes)):
            if r["estado"] == "RECHAZADO":
                continue
            declarado = any("corte" in x or "posterior" in x for x in r.get("limitaciones") or [])
            (parciales if declarado else fugas).append((f, i, nombre, corte, r["estado"], claves_ultima[:3]))
        break
    if not hallado:
        sin_fechas.append(f)
print("   fichas sin fechas en sus casos de control (no comprobable aquí):", sin_fechas)
for x in fugas:
    print("   FUGA (servida sin declararlo):", x)
for x in parciales:
    print("   servida con limitación declarada:", x)
for x in rotas:
    print("   RECHAZA con corte = última fecha:", x)
K.comprobar("ninguna ficha sirve en silencio datos fechados después de la fecha de corte", not fugas,
            f"{len({x[0] for x in fugas})} fichas: {sorted({x[0] for x in fugas})}")
K.comprobar("con fecha de corte = última fecha de los datos, se sirve", not rotas, str(rotas)[:300])

print("2. caché")
m = C.motor()
pet = base("FIR-CURVE-001")
f_curva = pet["datos"][0]["valores"]["curva"]["fecha"]
a = m.servir({**copy.deepcopy(pet), "fecha_corte": "2030-01-01"}, "AG-18")
b = m.servir({**copy.deepcopy(pet), "fecha_corte": "2000-01-01"}, "AG-18")
c = m.servir({**copy.deepcopy(pet), "fecha_corte": "2030-01-01"}, "AG-18")
K.comprobar("corte posterior servido, corte anterior a los datos rechazado (no sale de la caché)",
            a["estado"].startswith("SERVED") and b["estado"] == "RECHAZADO", f"{a['estado']} / {b['estado']} (curva del {f_curva})")
K.comprobar("misma petición y mismo corte: CACHE_HIT", c.get("cache_hit") is True)
# orden inverso
m = C.motor()
b = m.servir({**copy.deepcopy(pet), "fecha_corte": "2000-01-01"}, "AG-18")
a = m.servir({**copy.deepcopy(pet), "fecha_corte": "2030-01-01"}, "AG-18")
K.comprobar("orden inverso: el rechazo no se cachea como respuesta de la otra", a["estado"].startswith("SERVED") and b["estado"] == "RECHAZADO")
# fecha de corte equivalente escrita de otra forma
m = C.motor()
a = m.servir({**copy.deepcopy(pet), "fecha_corte": "2030-01-01"}, "AG-18")
a2 = m.servir({**copy.deepcopy(pet), "fecha_corte": "2030-01-01T00:00:00"}, "AG-18")
print("   corte «2030-01-01» y «2030-01-01T00:00:00»:", a["estado"], a2["estado"], "cache_hit", a2.get("cache_hit"))
# mutar la respuesta no debe corromper la caché
m = C.motor()
pet = base("REI-CAP-001")
a = m.servir(copy.deepcopy(pet), "AG-18")
original = copy.deepcopy(a["resultado"])


def ensuciar(x):
    for k in list(x):
        if isinstance(x[k], dict):
            ensuciar(x[k])
        elif isinstance(x[k], float):
            x[k] = -999.0


ensuciar(a["resultado"])
b = m.servir(copy.deepcopy(pet), "AG-18")
K.comprobar("mutar la respuesta servida no corrompe lo que devuelve la caché", b["resultado"] == original,
            "la caché devuelve el mismo objeto: el segundo cliente recibe las cifras alteradas por el primero")
rc = m.almacen.estado("RC")[a["calc_id"]]
K.comprobar("mutar la respuesta servida no altera el artefacto del RC en memoria", rc["resultado"]["payload"] == original)

print("3. serie de HT-01 con fecha de corte")


class Prov:
    nombre = "qa-r02"

    def __init__(self, as_of):
        self.as_of = pd.Timestamp(as_of) if as_of else None
        idx = pd.bdate_range("2020-01-01", "2026-12-31")
        rng = np.random.default_rng(7)
        self.s = pd.Series(100 * np.exp(np.cumsum(rng.normal(0, 0.01, len(idx)))), index=idx)

    def cierres(self, serie, inicio=None, fin=None):
        s = self.s
        if self.as_of is not None:
            s = s[s.index <= self.as_of]
        if inicio:
            s = s[s.index >= pd.Timestamp(inicio)]
        if fin:
            s = s[s.index <= pd.Timestamp(fin)]
        return s

    def huella(self, serie, inicio=None, fin=None):
        from bloque_a.herramientas.ht06_indice import clave_hash
        return clave_hash([float(x) for x in self.cierres(serie, inicio, fin).values])[:16]


import tempfile  # noqa: E402

from bloque_a.almacen import Almacen  # noqa: E402
from bloque_a.configuracion import cargar_config  # noqa: E402


def motor_p(as_of):
    return servicio.Motor(Almacen(Path(tempfile.mkdtemp(prefix="qa_r02_"))), Prov(as_of), cargar_config())


for ficha, extra in (("FX-BRK-001", {}), ("FX-REGIME-001", {})):
    mm = motor_p("2026-06-30")
    d = [{"serie": "X", "inicio": "2024-06-01"}]
    r_ok = mm.servir({"operacion": ficha, "datos": d, "parametros": extra}, "AG-18")
    r_fuga = mm.servir({"operacion": ficha, "datos": [{"serie": "X", "inicio": "2024-06-01", "fin": "2026-12-01"}], "parametros": extra},
                       "AG-18")
    r_antes = mm.servir({"operacion": ficha, "datos": d, "parametros": extra, "fecha_corte": "2025-06-30"}, "AG-18")
    e = mm.almacen.estado("RC")
    K.comprobar(f"{ficha} con serie de HT-01: servida con el corte del proveedor", r_ok["estado"].startswith("SERVED"), str(r_ok)[:200])
    K.comprobar(f"{ficha}: `fin` posterior al corte ⇒ FUGA_DE_INFORMACION", r_fuga.get("motivo") == "FUGA_DE_INFORMACION", str(r_fuga)[:200])
    ult = e[r_antes["calc_id"]]["datos"][0]["fecha_dato"] if r_antes["estado"].startswith("SERVED") else None
    K.comprobar(f"{ficha}: con corte 2025-06-30 el último dato usado no es posterior", ult is None or ult <= "2025-06-30", str(ult))
    K.comprobar(f"{ficha}: distinto corte ⇒ distinto resultado (no caché)", r_antes.get("cache_hit") is not True
                and r_antes.get("resultado") != r_ok.get("resultado"))
    out = mm.reejecutar(r_antes["calc_id"], "QA r02") if r_antes["estado"].startswith("SERVED") else {"coincide": "-"}
    K.comprobar(f"{ficha}: CT-10 del cálculo con serie de HT-01 coincide", out["coincide"] in ("SI", "-"), str(out)[:200])
sys.exit(K.fin())
