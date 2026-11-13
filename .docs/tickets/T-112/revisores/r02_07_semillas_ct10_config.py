"""QA r02 de T-112 · semillas raras, idempotencia, CT-10 en las 35 fichas, AUD-REX-001, configuración y Catálogo.

 1. Semillas raras o no hashables en `semilla` y en `parametros.semilla` (H-05 de la r01): sin excepción, una entrada en RC
    y, si se sirve, la semilla del artefacto es la usada.
 2. Idempotencia y orden de las llamadas: A, B, A en un Motor y B, A en otro dan lo mismo; repetir es CACHE_HIT.
 3. CT-10: cada una de las 35 fichas, servida con su primer caso de control y re-ejecutada ⇒ SI; con semilla solo en la
    petición; entradas que no son SERVICIO; artefacto con un parámetro que la ficha rechaza; motivo vacío.
 4. AUD-REX-001: casos de control (CT-10) y rechazo por CT-09.
 5. Configuración del Motor distinta de la de por defecto (H-04): ¿la siguen todas las fichas que usan un número de la
    configuración? (H5 en sesiones, ventana de datos, umbrales de HT-03, réplicas). Y CT-10 después de cambiarla.
 6. Catálogo ↔ manejadores: 71 IMPLEMENTADO (70 por CT-09 + AUD-REX-001 por CT-10) y 10 DOCUMENTADO sin código.
Uso: .venv/bin/python -I r02_07_semillas_ct10_config.py
"""
import copy
import decimal
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

C.preparar(["x"])
import numpy as np  # noqa: E402
from bloque_a.almacen import Almacen  # noqa: E402
from bloque_a.configuracion import cargar_config, parametro, sesiones_horizonte  # noqa: E402
from bloque_a.motor import fichas_reales, fichas_riesgo, fichas_series, fichas_valoracion, servicio  # noqa: E402

K = C.Contador("r02_07 semillas, CT-10, configuración y Catálogo")


def base(f, i=0):
    c = servicio.CASOS_CONTROL[f][i]
    return {"operacion": f, "datos": copy.deepcopy(c.get("datos") or []), "parametros": dict(c.get("parametros") or {}),
            "fecha_corte": c.get("fecha_corte")}


def llamar(m, pet, sol="AG-18"):
    antes = len(m.almacen.leer("RC"))
    try:
        r, exc = m.servir(pet, sol), None
    except BaseException as e:  # noqa: BLE001
        r, exc = None, f"{type(e).__name__}: {str(e)[:100]}"
    return r, exc, len(m.almacen.leer("RC")) - antes


print("1. semillas raras")
RARAS = [True, False, 1.0, 1.5, -1, 0, 2 ** 63 - 1, 2 ** 63, 2 ** 64, 10 ** 400, "7", b"7", [7], (7,), {"a": 1}, {7}, float("nan"),
         float("inf"), np.int64(7), np.float64(7.0), np.array([7]), decimal.Decimal(7), 1 + 0j, None]
mal, mentiras, servidas = [], [], []
for f in ("SIM-MC-001", "FX-REGIME-001", "ML-CAL-001", "REI-CAP-001"):
    for donde in ("peticion", "parametros", "ambas_distintas", "ambas_iguales"):
        for s in RARAS:
            m = C.motor()
            pet = base(f)
            pet["parametros"].pop("semilla", None)
            if donde in ("peticion", "ambas_iguales"):
                pet["semilla"] = s
            if donde in ("parametros", "ambas_iguales"):
                pet["parametros"]["semilla"] = s
            if donde == "ambas_distintas":
                pet["semilla"], pet["parametros"]["semilla"] = s, 3
            r, exc, nrc = llamar(m, pet)
            if exc or nrc != 1:
                mal.append((f, donde, repr(s)[:16], exc or f"RC {nrc}"))
                continue
            if r["estado"] != "RECHAZADO":
                e = m.almacen.estado("RC")[r["calc_id"]]
                usada = r["resultado"].get("semilla") if isinstance(r["resultado"], dict) else None
                servidas.append((f, donde, repr(s)[:16], e.get("semilla"), usada))
                if usada is not None and e.get("semilla") is not None and e.get("semilla") != usada:
                    mentiras.append((f, donde, repr(s)[:16], e.get("semilla"), usada))
                if donde == "ambas_distintas" and f in servicio.ACEPTA_SEMILLA and s is not None and s != 3:
                    mentiras.append((f, donde, repr(s)[:16], "servida con dos semillas distintas"))
for x in mal[:30]:
    print("   ESCAPE o RC:", x)
raras_servidas = sorted({(f, s) for f, d, s, *_ in servidas if f in servicio.ACEPTA_SEMILLA and s not in ("0", "None", "np.int64(7)", "9223372036854775")})
print("   semillas no enteras servidas en fichas con azar:", raras_servidas)
K.comprobar("semillas raras: sin excepción y con una entrada en RC", not mal, f"{len(mal)}")
K.comprobar("la semilla del artefacto es la usada; dos distintas se rechazan", not mentiras, str(mentiras[:6]))
K.comprobar("ninguna semilla booleana, fraccionaria o textual se sirve en una ficha con azar",
            not [x for x in raras_servidas if x[1] in ("True", "False", "1.5", "'7'", "b'7'")], str(raras_servidas))

print("2. idempotencia y orden")
m1, m2 = C.motor(), C.motor()
A, B = base("SIM-MC-001"), base("FX-PPA-001")
a1 = m1.servir(copy.deepcopy(A), "AG-18")
b1 = m1.servir(copy.deepcopy(B), "AG-18")
a1b = m1.servir(copy.deepcopy(A), "AG-18")
b2 = m2.servir(copy.deepcopy(B), "AG-18")
a2 = m2.servir(copy.deepcopy(A), "AG-18")
K.comprobar("A, B, A y B, A dan los mismos resultados", a1["resultado"] == a2["resultado"] == a1b["resultado"] and b1["resultado"] == b2["resultado"])
K.comprobar("repetir es CACHE_HIT y no gasta", a1b.get("cache_hit") is True and a1.get("cache_hit") is False)
tipos = [e.get("tipo_entrada") for e in m1.almacen.leer("RC")]
K.comprobar("RC: SERVICIO, SERVICIO, CACHE_HIT", tipos == ["SERVICIO", "SERVICIO", "CACHE_HIT"], str(tipos))
p1 = base("SIM-MC-001")
s_ = p1["parametros"].pop("semilla")
ra = C.motor().servir({**copy.deepcopy(p1), "semilla": s_}, "AG-18")
rb = C.motor().servir(base("SIM-MC-001"), "AG-18")
K.comprobar("semilla en la petición o en los parámetros: mismo resultado", ra.get("resultado") == rb.get("resultado"), ra.get("detalle", ""))

print("3. CT-10 en las 35 fichas")
no_si, errores = [], []
m = C.motor()
for f in sorted(servicio.FASE2):
    pet = base(f)
    sol = "AG-18"
    r = m.servir(pet, sol)
    if not r["estado"].startswith("SERVED"):
        errores.append((f, r.get("detalle", "")[:80]))
        continue
    try:
        out = m.reejecutar(r["calc_id"], "QA r02")
        if (out["coincide"], out["categoria"]) != ("SI", None):
            no_si.append((f, out["coincide"], out["categoria"], out["diferencias"][:2]))
    except Exception as e:  # noqa: BLE001
        errores.append((f, f"{type(e).__name__}: {str(e)[:100]}"))
K.comprobar("las 35 fichas servidas y re-ejecutadas: SI", not no_si and not errores, f"{no_si[:4]} {errores[:4]}")
pet = base("SIM-MC-001")
sem = pet["parametros"].pop("semilla")
r = m.servir({**pet, "semilla": sem + 1}, "AG-18")
out = m.reejecutar(r["calc_id"], "QA r02")
e = m.almacen.estado("RC")[r["calc_id"]]
K.comprobar("semilla solo en la petición: viaja en los parámetros del artefacto y la re-ejecución da SI",
            out["coincide"] == "SI" and e["parametros"].get("semilla") == sem + 1 == e["semilla"], f"{out} {e.get('semilla')}")
hit = m.servir({**base("SIM-MC-001")}, "AG-18")
hit = m.servir({**base("SIM-MC-001")}, "AG-18")
for nombre, cid in (("un CACHE_HIT", hit.get("calc_id_cache")), ("un RECHAZO", m.servir({"operacion": "SIM-MC-001"}, "AG-18")["calc_id"]),
                    ("una REEJECUCION", out["calc_id"]), ("un id inexistente", "CALC-0000-9999"), ("None", None)):
    try:
        m.reejecutar(cid, "QA r02")
        K.comprobar(f"re-ejecutar {nombre}: imposible", False, "se re-ejecutó")
    except (KeyError, ValueError, NotImplementedError, TypeError) as ex:
        K.comprobar(f"re-ejecutar {nombre}: imposible ({type(ex).__name__})", True)
for motivo in ("", "   ", None, 0, [], "\n\t"):
    try:
        m.reejecutar(r["calc_id"], motivo)
        K.comprobar(f"CT-10 con motivo {motivo!r}: imposible", False)
    except ValueError:
        K.comprobar(f"CT-10 con motivo {motivo!r}: imposible", True)
n_antes = len(m.almacen.leer("RC"))
e2 = copy.deepcopy(e)
e2["parametros"]["n_trayectorias"] = 10 ** 9
e2["calc_id"] = m.almacen.nuevo_id("CALC")
m.almacen.escribir("RC", "AG-13", e2)
try:
    out2 = m.reejecutar(e2["calc_id"], "QA r02")
    print("   artefacto con un parámetro fuera de cota:", out2["coincide"], out2["categoria"])
    K.comprobar("CT-10 de un artefacto con un parámetro que la ficha rechaza: registrado, no excepción", True)
except Exception as ex:  # noqa: BLE001
    registrado = len(m.almacen.leer("RC")) - n_antes - 1
    print(f"   artefacto con un parámetro fuera de cota: excepción {type(ex).__name__} ({str(ex)[:90]}); entradas REEJECUCION escritas: {registrado}")
    K.comprobar("CT-10 de un artefacto con un parámetro que la ficha rechaza: registrado, no excepción", False,
                f"{type(ex).__name__} sin entrada en RC (observación de la r01, sigue igual)")

print("4. AUD-REX-001")
v = C.motor().verificar_casos_control(["AUD-REX-001"])["AUD-REX-001"]
K.comprobar(f"AUD-REX-001: {len(v['casos'])} casos de control superados (≥ 6, con el de parámetros)", v["superados"] and len(v["casos"]) >= 6,
            str([c for c in v["casos"] if not c["superado"]])[:300])
r = C.motor().servir({"operacion": "AUD-REX-001"}, "AG-18")
K.comprobar("AUD-REX-001 por CT-09: METODO_NO_IMPLEMENTADO con el aviso de CT-10", r["estado"] == "RECHAZADO" and "CT-10" in r["detalle"], str(r)[:200])

print("5. configuración del Motor distinta de la de por defecto")
cfg = cargar_config()
cfg2 = copy.deepcopy(cfg)
cfg2["horizontes"]["H5"] = {"meses": 60}            # 1 260 sesiones en lugar de 2 520
cfg2["senales"]["ventana_anios"] = 1
h5_def, h5_2 = sesiones_horizonte(cfg, "H5"), sesiones_horizonte(cfg2, "H5")
print(f"   H5 en sesiones: por defecto {h5_def}, modificada {h5_2}")


def motor_cfg(c):
    class Pv:
        as_of, nombre = None, "qa-r02"
    return servicio.Motor(Almacen(Path(tempfile.mkdtemp(prefix="qa_r02_"))), Pv(), c)


pet = base("RISK-VAR-001")
pet["parametros"]["horizonte"] = h5_2 + 1
ra, rb = motor_cfg(cfg).servir(copy.deepcopy(pet), "AG-18"), motor_cfg(cfg2).servir(copy.deepcopy(pet), "AG-18")
K.comprobar("R (RISK-VAR-001): la cota del horizonte sigue a H5 de la configuración del Motor", ra["estado"].startswith("SERVED") and rb["estado"] == "RECHAZADO",
            f"{ra['estado']} / {rb['estado']}")
serie = [float(x) for x in np.where(np.arange(h5_2 + 200) < 700, 0.0, 3.0) + np.sin(np.arange(h5_2 + 200) * 1.7)]
pet = {"operacion": "FX-BRK-001", "datos": [{"valores": {"serie": serie}}], "parametros": {}}
ra, rb = motor_cfg(cfg).servir(copy.deepcopy(pet), "AG-18"), motor_cfg(cfg2).servir(copy.deepcopy(pet), "AG-18")
print(f"   S (FX-BRK-001) con {len(serie)} observaciones: por defecto {ra['estado']}, con H5 = {h5_2}: {rb['estado']} {rb.get('detalle', '')[:80]}")
K.comprobar("S (FX-BRK-001): la cota de observaciones «H5 en sesiones» sigue a la configuración del Motor", rb["estado"] == "RECHAZADO",
            f"cota fija en el código (OBS_MAXIMAS_SERIES = {fichas_series.OBS_MAXIMAS_SERIES}); con H5 = {h5_2} sesiones sirve {len(serie)} observaciones")
serie = [float(x) for x in np.random.default_rng(1).normal(0, 1, 600) * np.where((np.arange(600) // 60) % 2, 1, 3)]
pet = {"operacion": "FX-REGIME-001", "datos": [{"valores": {"serie": serie}}], "parametros": {}}
rb = motor_cfg(cfg2).servir(copy.deepcopy(pet), "AG-18")
K.comprobar("S (FX-REGIME-001): la cota «senales.ventana_anios × 252» sigue a la configuración del Motor", rb["estado"] == "RECHAZADO",
            f"cota fija {fichas_series.UMBRALES['FX-REGIME-001']['obs_maximas']}; con ventana_anios = 1 (252 sesiones) sirve 600 observaciones")
print("   constantes de horizonte escritas en fichas_reales:", {k: getattr(fichas_reales, k) for k in dir(fichas_reales)
                                                              if k.isupper() and ("H5" in k or "H2" in k or "SESIONES" in k)})
print("   en la configuración: H2 =", parametro(cfg, "horizontes.H2"), "· H5 =", parametro(cfg, "horizontes.H5"), "· calendario =", parametro(cfg, "calendario"))
usa_cfg = {md.__name__.split(".")[-1]: ("configuracion" in Path(md.__file__).read_text(encoding="utf-8").split('"""', 2)[2])
           for md in (fichas_series, fichas_riesgo, fichas_valoracion, fichas_reales)}
print("   módulos cuyo código lee ent['configuracion']:", usa_cfg)

# CT-10 después de un cambio de configuración: el artefacto no guarda los números de configuración que usó la ficha
cfg4 = copy.deepcopy(cfg)
cfg4["parametros_ht03"]["umbrales"]["E"] = 68
tmp_rc = Path(tempfile.mkdtemp(prefix="qa_r02_"))


class Pv0:
    as_of, nombre = None, "qa-r02"


ma = servicio.Motor(Almacen(tmp_rc), Pv0(), cfg)
cc = servicio.CASOS_CONTROL["DEC-VOI-001"][1]
rr = ma.servir({"operacion": "DEC-VOI-001", "datos": copy.deepcopy(cc["datos"]), "parametros": dict(cc["parametros"])}, "AG-18")
o1 = ma.reejecutar(rr["calc_id"], "QA r02")
o2 = servicio.Motor(Almacen(tmp_rc), Pv0(), cfg4).reejecutar(rr["calc_id"], "QA r02")
print(f"   DEC-VOI-001 re-ejecutada con la misma configuración: {o1['coincide']}; con el umbral E de HT-03 cambiado (60 → 68): "
      f"{o2['coincide']} / {o2['categoria']}")
K.comprobar("CT-10 tras un cambio de configuración no culpa al cálculo original (ERROR_ORIGINAL)", o2["categoria"] != "ERROR_ORIGINAL",
            f"{o2['coincide']}/{o2['categoria']}: el artefacto no registra los umbrales de configuración con que se calculó")

print("6. Catálogo ↔ manejadores")
mad = servicio.madurez_catalogo()
impl = {f for f, e in mad.items() if e.startswith("IMPLEMENTADO")}
doc = {f for f, e in mad.items() if e.upper().startswith("DOCUMENTADO")}
K.comprobar("Catálogo: 81 fichas, 71 IMPLEMENTADO y 10 DOCUMENTADO", (len(mad), len(impl), len(doc)) == (81, 71, 10), f"{len(mad)} {len(impl)} {len(doc)}")
K.comprobar("FICHAS_CATALOGO del servicio = las 81 del Catálogo", set(servicio.FICHAS_CATALOGO) == set(mad) and len(servicio.FICHAS_CATALOGO) == 81)
K.comprobar("70 manejadores = IMPLEMENTADO menos AUD-REX-001", set(servicio.IMPLEMENTADAS) == impl - {"AUD-REX-001"} and len(servicio.IMPLEMENTADAS) == 70,
            str(sorted(set(servicio.IMPLEMENTADAS) ^ (impl - {'AUD-REX-001'}))))
K.comprobar("FASE2 = 35 fichas, las del plan", len(servicio.FASE2) == 35 and not (servicio.FASE2 & servicio.FASE1))
K.comprobar("las 10 DOCUMENTADO no tienen manejador ni casos de control", not (doc & (set(servicio.IMPLEMENTADAS) | set(servicio.CASOS_CONTROL))))
mm = C.motor()
malos = []
for f in sorted(doc):
    r = mm.servir({"operacion": f, "datos": [{"valores": {"x": 1}}]}, "AG-18")
    if not (r["estado"] == "RECHAZADO" and r["motivo"] == "METODO_NO_IMPLEMENTADO"):
        malos.append((f, r))
    if r.get("alternativa") and not servicio.servible(r["alternativa"]):
        malos.append((f, "alternativa no servible", r["alternativa"]))
K.comprobar("las 10 DOCUMENTADO responden METODO_NO_IMPLEMENTADO y solo anuncian alternativas servibles", not malos, str(malos)[:300])
r = mm.servir({"operacion": "NO-EXISTE-001"}, "AG-18")
K.comprobar("una ficha ajena al Catálogo: OPERACION_SIN_FICHA", r.get("motivo") == "OPERACION_SIN_FICHA")
vv = C.motor().verificar_casos_control(sorted(servicio.FASE2))
K.comprobar("las 35 fichas superan sus casos de control (verificar_casos_control)", all(x["superados"] for x in vv.values()),
            str([f for f, x in vv.items() if not x["superados"]]))
print("   casos de control de la Fase 2:", sum(len(x["casos"]) for x in vv.values()))
# sin Catálogo legible, nada se sirve
import os  # noqa: E402

tmp = tempfile.mkdtemp(prefix="qa_r02_raiz_")
os.environ["BLOQUE_A_RAIZ"] = tmp
try:
    cfg3 = copy.deepcopy(cfg)
    cfg3.setdefault("rutas", {})["raiz_paquete"] = tmp
    r = motor_cfg(cfg3).servir(base("REI-CAP-001"), "AG-18")
    K.comprobar("sin Catálogo legible, la ficha no se sirve (falla cerrado)", r["estado"] == "RECHAZADO", str(r)[:200])
finally:
    os.environ.pop("BLOQUE_A_RAIZ", None)
sys.exit(K.fin())
