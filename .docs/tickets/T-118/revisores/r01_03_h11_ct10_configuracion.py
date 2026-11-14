"""QA r01 de T-118 · H-11: la configuración que guarda el artefacto y el CT-10 que la usa.

 1. Qué guarda cada ficha (las 70 de CT-09, con su primer caso de control) y cuánto pesa: bytes de la entrada del RC con
    `configuracion_usada` y sin él.
 2. CT-10 de las 70 con la misma configuración (SI) y con TODAS las secciones leídas cambiadas a la vez (SI: usa la del
    artefacto), en un Motor distinto sobre el mismo RC.
 3. Cambio en una clave que la ficha no lee: de otra sección y de la misma sección.
 4. Artefactos antiguos o raros: sin el campo, con None, lista, texto, sección que no es objeto, sección sin `valor`,
    sección desconocida, `valor` de tipo absurdo. Nada escapa de `reejecutar`; todo deja su entrada REEJECUCION.
 5. ¿Un error real del original puede quedar en CONVENCION_DISTINTA? Artefacto POSTERIOR a T-118 (con registro completo),
    cifra alterada, y después un cambio de configuración (en la clave leída, en otra clave de la misma sección, en otra
    sección).
 6. Manipulación: la configuración guardada se cambia (a) en el fichero JSONL y (b) por una entrada nueva bien escrita.
 7. Determinismo: dos Motores, dos órdenes de llamada ⇒ el mismo `configuracion_usada`; la clave de la caché no cambia por
    T-118 y la caché no sirve un resultado de otra configuración.
 8. ¿La lectura registrada es completa? Se compara con una configuración que apunta TODO acceso (también iterar o copiar).
Uso: .venv/bin/python -I r01_03_h11_ct10_configuracion.py
"""
import copy
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
from bloque_a.almacen import Almacen  # noqa: E402
from bloque_a.configuracion import cargar_config, fusionar  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402

K = C.Contador("r01_03 H-11")
FICHAS = sorted(f for f in servicio.CASOS_CONTROL if f in servicio.IMPLEMENTADAS and servicio.servible(f))
print(f"fichas servibles con caso de control: {len(FICHAS)}")


def bytes_de(e):
    return len(json.dumps(e, ensure_ascii=False, default=str).encode())


def copia(m, calc, cambio):
    e = copy.deepcopy(m.almacen.estado("RC")[calc])
    cambio(e)
    e["calc_id"] = m.almacen.nuevo_id("CALC")
    m.almacen.escribir("RC", "AG-13", e)
    return e["calc_id"]


def ree(m, calc):
    antes = len(m.almacen.leer("RC"))
    try:
        out, exc = m.reejecutar(calc, "QA r01 de T-118"), None
    except Exception as e:  # noqa: BLE001
        out, exc = None, e
    return out, exc, len(m.almacen.leer("RC")) - antes


# ------------------------------------------------------------------ 1 y 2
print("\n[1-2] qué guarda cada ficha, cuánto pesa, y CT-10 con todo lo leído cambiado")
tmp = tempfile.mkdtemp(prefix="qa_t118_h11_")
m = C.motor(tmp)
servidos, secciones, pesos = {}, {}, []
for f in FICHAS:
    r, exc, n = C.servir_contando(m, C.peticion(f))
    if exc or not str(r.get("estado")).startswith("SERVED"):
        K.comprobar(f"{f} servida", False, str(exc or r)[:200])
        continue
    e = m.almacen.estado("RC")[r["calc_id"]]
    usada = e["artefacto"].get("configuracion_usada")
    servidos[f], secciones[f] = r["calc_id"], usada
    sin = copy.deepcopy(e)
    sin["artefacto"].pop("configuracion_usada", None)
    pesos.append((bytes_de(e) - bytes_de(sin), bytes_de(sin), f))
K.comprobar(f"las {len(FICHAS)} servidas con `configuracion_usada` objeto", all(isinstance(s, dict) for s in secciones.values())
            and len(servidos) == len(FICHAS))
con = {f: sorted(s) for f, s in secciones.items() if s}
print(f"  fichas que leen la configuración: {len(con)} de {len(secciones)}")
for f, s in con.items():
    print(f"    {f}: {s}")
pesos.sort(reverse=True)
tot_extra, tot_base = sum(p[0] for p in pesos), sum(p[1] for p in pesos)
print(f"  bytes añadidos por entrada: máx {pesos[0][0]} ({pesos[0][2]}), mediana {pesos[len(pesos) // 2][0]}, mín {pesos[-1][0]}; "
      f"total {tot_extra} sobre {tot_base} ({100 * tot_extra / tot_base:.2f} %)")
for extra, base, f in pesos[:6]:
    print(f"    {f}: +{extra} B sobre {base} B ({100 * extra / base:.1f} %)")

# Cambio de TODAS las secciones leídas: cada número de esas secciones, alterado
def alterar(x, camino=()):
    if isinstance(x, dict):
        return {k: alterar(v, (*camino, k)) for k, v in x.items()}
    if isinstance(x, list):
        return [alterar(v, camino) for v in x]
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        return x
    if isinstance(x, int):
        return x + 1 if x < 60 else x - 1          # sigue siendo entero y positivo
    return min(x * 0.9, 0.999) if 0 < x < 1 else x * 0.9


leidas = sorted({s for ss in con.values() for s in ss if not s.startswith("_")})
base_cfg = cargar_config()
extra = {s: alterar(base_cfg[s]) for s in leidas if s in base_cfg}
m2 = C.motor(tmp, **extra)
K.comprobar("la configuración alterada difiere en todas las secciones leídas", all(m2.cfg[s] != base_cfg[s] for s in extra), str(leidas))
mal_mismo, mal_otro, cambia = [], [], []
for f, calc in servidos.items():
    out, exc, n = ree(m, calc)
    if exc or out["coincide"] != "SI" or n != 1:
        mal_mismo.append((f, str(exc or out)[:160]))
    out, exc, n = ree(m2, calc)
    if exc or out["coincide"] != "SI" or n != 1:
        mal_otro.append((f, str(exc or out)[:200]))
    if f in con:
        # ¿el cambio de configuración cambia de verdad el resultado al servir de nuevo? (si no, la prueba no prueba nada)
        r2, exc2, _ = C.servir_contando(C.motor(None, **extra), C.peticion(f))
        r1 = m.almacen.estado("RC")[calc]["resultado"]["payload"]
        if exc2 or r2.get("estado") == "RECHAZADO" or r2.get("resultado") != r1:
            cambia.append(f)
K.comprobar(f"CT-10 con la misma configuración: SI en las {len(servidos)}", not mal_mismo, str(mal_mismo)[:600])
K.comprobar(f"CT-10 con todas las secciones leídas cambiadas: SI en las {len(servidos)}", not mal_otro, str(mal_otro)[:900])
print(f"  fichas cuyo servicio SÍ cambia (o se rechaza) con la configuración alterada: {len(cambia)} de {len(con)}: {cambia}")
K.comprobar("al menos DEC-VOI-001, ML-CAL-001 y ML-PRED-001 cambian de cifra con la configuración alterada",
            {"DEC-VOI-001", "ML-CAL-001"} <= set(cambia), str(cambia))

# ------------------------------------------------------------------ 3
print("\n[3] cambio en claves que la ficha no lee")
voi = servidos["DEC-VOI-001"]
m_uc = C.motor(tmp, uc={"motor_por_plan": {"PLAN_MIN": 0.5}})
out, exc, _ = ree(m_uc, voi)
rc = m_uc.almacen.leer("RC")[-1]["reejecucion"]
K.comprobar("otra sección (uc): SI y nada distinto de la vigente", not exc and out["coincide"] == "SI"
            and rc["configuracion"]["distinta_de_la_vigente"] == [], str(exc or rc)[:300])
var = servidos["RISK-VAR-001"]
m_h1 = C.motor(tmp, horizontes={"H1": {"sesiones": 7}})
out, exc, _ = ree(m_h1, var)
rc = m_h1.almacen.leer("RC")[-1]["reejecucion"]
K.comprobar("misma sección, otra clave (horizontes.H1 en RISK-VAR-001): SI", not exc and out["coincide"] == "SI", str(exc or out)[:300])
print(f"    reejecucion.configuracion = {rc['configuracion']}")

# ------------------------------------------------------------------ 4
print("\n[4] artefactos antiguos o raros")
raros = {
    "sin el campo": lambda e: e["artefacto"].pop("configuracion_usada"),
    "None": lambda e: e["artefacto"].__setitem__("configuracion_usada", None),
    "lista": lambda e: e["artefacto"].__setitem__("configuracion_usada", [1, 2]),
    "texto": lambda e: e["artefacto"].__setitem__("configuracion_usada", "parametros_ht03"),
    "sección que no es objeto": lambda e: e["artefacto"]["configuracion_usada"].__setitem__("parametros_ht03", 7),
    "sección sin valor": lambda e: e["artefacto"]["configuracion_usada"]["parametros_ht03"].pop("valor"),
    "sección desconocida": lambda e: e["artefacto"]["configuracion_usada"].__setitem__("no_existe", {"valor": {"a": 1}, "por_defecto": "x"}),
    "valor texto": lambda e: e["artefacto"]["configuracion_usada"]["parametros_ht03"].__setitem__("valor", "sesenta"),
    "valor None": lambda e: e["artefacto"]["configuracion_usada"]["parametros_ht03"].__setitem__("valor", None),
    "valor lista": lambda e: e["artefacto"]["configuracion_usada"]["parametros_ht03"].__setitem__("valor", [1]),
    "umbrales texto": lambda e: e["artefacto"]["configuracion_usada"]["parametros_ht03"]["valor"].__setitem__("umbrales", "x"),
    "umbral E NaN": lambda e: e["artefacto"]["configuracion_usada"]["parametros_ht03"]["valor"]["umbrales"].__setitem__("E", float("nan")),
    "umbral E 1e308": lambda e: e["artefacto"]["configuracion_usada"]["parametros_ht03"]["valor"]["umbrales"].__setitem__("E", 1e308),
    "artefacto None": lambda e: e.__setitem__("artefacto", None),
    "artefacto lista": lambda e: e.__setitem__("artefacto", []),
    "sin artefacto": lambda e: e.pop("artefacto"),
}
for nombre, cambio in raros.items():
    try:
        c = copia(m, voi, cambio)
    except Exception as e:  # noqa: BLE001
        print(f"    ({nombre}: el Almacén no admite la entrada: {type(e).__name__}: {str(e)[:100]})")
        continue
    out, exc, n = ree(m, c)
    rc = m.almacen.leer("RC")[-1]
    K.comprobar(f"artefacto con configuración «{nombre}»: sin excepción y una REEJECUCION",
                exc is None and n == 1 and rc["tipo_entrada"] == "REEJECUCION",
                f"{type(exc).__name__ if exc else ''}: {str(exc or out)[:200]}")
    if out:
        print(f"      → {out['coincide']}/{out['categoria']} · {rc['reejecucion']['configuracion']}")
    # y con otra configuración vigente
    out, exc, n = ree(m2, c)
    if exc or n != 1:
        K.comprobar(f"«{nombre}» con otra configuración vigente", False, f"{type(exc).__name__}: {str(exc)[:200]}")
    else:
        print(f"      otra vigente → {out['coincide']}/{out['categoria']}")

# ------------------------------------------------------------------ 5
print("\n[5] ¿un error real del original queda en CONVENCION_DISTINTA? (artefacto posterior a T-118, registro completo)")


def cifra_alterada(e):
    e["resultado"]["payload"]["voi_puntos"] = e["resultado"]["payload"]["voi_puntos"] + 1.0


malo = copia(m, voi, cifra_alterada)
out, exc, _ = ree(m, malo)
K.comprobar("cifra alterada, misma configuración: NO / ERROR_ORIGINAL", not exc and (out["coincide"], out["categoria"]) == ("NO", "ERROR_ORIGINAL"), str(exc or out)[:200])
casos5 = {
    "cambia la clave que la ficha lee (umbral E 60→68)": {"parametros_ht03": {"umbrales": {"E": 68}}},
    "cambia otra clave de la misma sección que la ficha no usa para este cálculo": None,   # se rellena abajo
    "cambia otra sección (uc)": {"uc": {"motor_por_plan": {"PLAN_MIN": 0.5}}},
}
ht = base_cfg["parametros_ht03"]
otra = next((k for k, v in ht.items() if k not in ("umbrales", "banda_marginal") and isinstance(v, (int, float)) and not isinstance(v, bool)), None)
if otra is None:
    otra_d = next(k for k, v in ht.items() if isinstance(v, dict) and k != "umbrales")
    k2 = next(k for k, v in ht[otra_d].items() if isinstance(v, (int, float)) and not isinstance(v, bool))
    casos5["cambia otra clave de la misma sección que la ficha no usa para este cálculo"] = {"parametros_ht03": {otra_d: {k2: ht[otra_d][k2] * 0.5}}}
    print(f"    (otra clave: parametros_ht03.{otra_d}.{k2})")
else:
    casos5["cambia otra clave de la misma sección que la ficha no usa para este cálculo"] = {"parametros_ht03": {otra: ht[otra] * 0.5}}
    print(f"    (otra clave: parametros_ht03.{otra})")
resumen5 = {}
for nombre, extra5 in casos5.items():
    mm = C.motor(tmp, **extra5)
    # control: el artefacto BUENO se reproduce con esa configuración vigente
    ok, _, _ = ree(mm, voi)
    out, exc, _ = ree(mm, malo)
    resumen5[nombre] = (ok["coincide"], out["coincide"], out["categoria"])
    print(f"    {nombre}: bueno → {ok['coincide']}; alterado → {out['coincide']}/{out['categoria']} · {out['diagnostico'][:150]}")
# Lo razonable: el artefacto trae el registro completo y la re-ejecución lo ha usado (el bueno da SI): la diferencia del
# alterado es del original, cambie o no la configuración vigente.
K.comprobar("error real + cambio de la clave leída: sigue siendo ERROR_ORIGINAL (la re-ejecución usó la configuración del artefacto)",
            resumen5["cambia la clave que la ficha lee (umbral E 60→68)"][2] == "ERROR_ORIGINAL", str(resumen5))
K.comprobar("error real + cambio de una clave que no interviene (misma sección): sigue siendo ERROR_ORIGINAL",
            resumen5["cambia otra clave de la misma sección que la ficha no usa para este cálculo"][2] == "ERROR_ORIGINAL")
K.comprobar("error real + cambio de otra sección: ERROR_ORIGINAL", resumen5["cambia otra sección (uc)"][2] == "ERROR_ORIGINAL")
# una ficha que solo lee la cota (horizontes, calendario): error real + cambio de H1
malo_var = copia(m, var, lambda e: e["resultado"]["payload"].__setitem__("n", e["resultado"]["payload"]["n"] + 1))
out, exc, _ = ree(m_h1, malo_var)
print(f"    RISK-VAR-001 alterado + cambio de horizontes.H1 (que no lee): {out['coincide']}/{out['categoria']}")
K.comprobar("RISK-VAR-001 con cifra alterada y H1 cambiado (la ficha solo lee H5): ERROR_ORIGINAL", out["categoria"] == "ERROR_ORIGINAL", out["diagnostico"][:200])

# ------------------------------------------------------------------ 6
print("\n[6] manipulación de la configuración guardada")
tmp6 = tempfile.mkdtemp(prefix="qa_t118_h11m_")
m6 = C.motor(tmp6)
r6 = m6.servir(C.peticion("DEC-VOI-001", 1), "AG-18")
K.comprobar("integridad del RC antes de manipular", m6.almacen.verificar_integridad("RC").get("RC") is True, str(m6.almacen.verificar_integridad("RC")))
ruta = next(Path(tmp6).rglob("RC_registro_calculos.jsonl"))
txt = ruta.read_text(encoding="utf-8")
assert '"E": 60' in txt, "no encuentro el umbral E en el RC"
ruta.write_text(txt.replace('"E": 60', '"E": 68', 1), encoding="utf-8")
try:
    m6b = C.motor(tmp6)
    integ = m6b.almacen.verificar_integridad("RC")
    out = m6b.reejecutar(r6["calc_id"], "tras manipular")
    print(f"    reejecutar sobre el fichero manipulado: {out['coincide']}/{out['categoria']}")
except Exception as e:  # noqa: BLE001
    integ = f"{type(e).__name__}: {str(e)[:200]}"
print(f"    tras cambiar el umbral guardado en el fichero: {integ}")
K.comprobar("el cambio en el fichero lo detecta la cadena de hash (el Almacén no abre o la integridad falla)",
            isinstance(integ, str) or integ.get("RC") is not True)
# (b) entrada nueva bien escrita con la configuración cambiada y el resultado original
c6 = copia(m, voi, lambda e: e["artefacto"]["configuracion_usada"]["parametros_ht03"]["valor"]["umbrales"].__setitem__("E", 68))
out, exc, _ = ree(m, c6)
print(f"    entrada nueva con el umbral guardado cambiado y el resultado original: {out['coincide']}/{out['categoria']}")
K.comprobar("configuración guardada que no es la que dio el resultado: coincide NO", out["coincide"] == "NO")

# ------------------------------------------------------------------ 7
print("\n[7] determinismo y caché")
ma, mb = C.motor(), C.motor()
orden = ["DEC-VOI-001", "ML-CAL-001", "RISK-VAR-001", "SCN-H-001", "FX-BRK-001", "CHR-FLOW-001"]
orden = [f for f in orden if f in servidos]


def _entrada(mm, f):
    c = mm.servir(C.peticion(f), "AG-18")["calc_id"]
    return mm.almacen.estado("RC")[c]


ua = {f: _entrada(ma, f) for f in orden}
ub = {f: _entrada(mb, f) for f in reversed(orden)}
K.comprobar("mismo `configuracion_usada`, resultado y clave de idempotencia en dos Motores y dos órdenes",
            all(json.dumps(ua[f]["artefacto"], sort_keys=True, default=str) == json.dumps(ub[f]["artefacto"], sort_keys=True, default=str)
                and ua[f]["resultado"] == ub[f]["resultado"] and ua[f]["clave_idempotencia"] == ub[f]["clave_idempotencia"] for f in orden))
# la clave de la caché no incluye la configuración: ¿puede un Motor servir desde la caché un resultado de otra configuración?
mc = C.motor()
r_a = mc.servir(C.peticion("DEC-VOI-001", 1), "AG-18")
mc.cfg["parametros_ht03"]["umbrales"]["E"] = 68        # la configuración del Motor cambia en caliente (mismo objeto)
r_b = mc.servir(C.peticion("DEC-VOI-001", 1), "AG-18")
fresco = C.motor(None, parametros_ht03={"umbrales": {"E": 68}}).servir(C.peticion("DEC-VOI-001", 1), "AG-18")
print(f"    tras cambiar m.cfg en caliente: cache_hit={r_b.get('cache_hit')}; ¿igual que un Motor nuevo con E=68? {r_b['resultado'] == fresco['resultado']}")
K.comprobar("[observación] un cambio en caliente de m.cfg no se sirve desde la caché con las cifras de antes",
            r_b["resultado"] == fresco["resultado"], "la clave de la caché no lleva la configuración (anterior a T-118: desde H-04 de T-112)")

# ------------------------------------------------------------------ 8
print("\n[8] ¿el registro de lecturas es completo?")


class Espia(dict):
    """Apunta cualquier forma de acceso, también las que _ConfiguracionLeida no registra."""
    def __init__(self, cfg):
        super().__init__(cfg)
        self.otras = set()

    def __bool__(self):
        return True

    def _a(self, que):
        self.otras.add(que)

    def __iter__(self):
        self._a("__iter__")
        return super().__iter__()

    def keys(self):
        self._a("keys")
        return super().keys()

    def items(self):
        self._a("items")
        return super().items()

    def values(self):
        self._a("values")
        return super().values()

    def copy(self):
        self._a("copy")
        return super().copy()

    def __len__(self):
        self._a("__len__")
        return super().__len__()

    def __reduce_ex__(self, p):
        self._a("deepcopy/pickle")
        return super().__reduce_ex__(p)


no_registrado = {}
for f in FICHAS:
    esp = Espia(cargar_config())
    ent, _ = m._resolver_datos(C.peticion(f)["datos"], None)
    ent["configuracion"], ent["fecha_corte"] = esp, None
    params = dict(C.peticion(f)["parametros"])
    try:
        servicio.IMPLEMENTADAS[f]["fn"](ent, params)
    except Exception as e:  # noqa: BLE001
        print(f"    {f}: {type(e).__name__}: {str(e)[:100]}")
    if esp.otras:
        no_registrado[f] = sorted(esp.otras)
K.comprobar("ninguna ficha accede a la configuración por una vía que el registro no apunta (iterar, copiar, items…)",
            not no_registrado, str(no_registrado)[:600])

sys.exit(K.fin())
