"""QA r03 de T-106 · ¿Se puede saltar todavía un umbral fijo de MON e IDX (H-14)? Ataques por el Motor (CT-09).

1. Cada clave de `UMBRALES` de cada ficha MON/IDX, en la petición y con su MISMO valor por defecto: RECHAZADO con
   «umbrales fijos» y entrada en RC (no basta con que un valor más laxo se rechace por rango).
2. Claves que se escapan del conjunto: mayúsculas, espacios, homoglifos, el umbral anidado en `parametros`, en
   `operacion`, en la raíz de la petición, en `clase` o en los datos en línea (`valores`). Con un caso que la ficha
   RECHAZA por ese umbral, ninguna variante debe convertirlo en servido; con el caso de control, ninguna debe cambiar el
   resultado servido.
3. Auditoría del código: toda clave que un manejador MON/IDX lee de `p` está declarada en `PARAMETROS_POR_DEFECTO` o es
   un parámetro opcional conocido; se listan las que no.
4. Parámetros de ventana sin rango (los que no son umbrales y siguen en la petición): 0, negativos y no enteros. Una
   ventana de 0 o negativa no es un parámetro del método; si se sirve, el número publicado no es el de la ficha.
5. Contraste en FON, DER y TCV: sus umbrales (`MINIMOS`, `RANGOS`, `UMBRALES`) en la petición no cambian nada.

Uso: .venv/bin/python -I -B .docs/tickets/T-106/revisores/r03_01_umbrales.py [RAIZ]
"""
from __future__ import annotations

import copy
import inspect
import json
import re
import shutil
import sys
import tempfile
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

M = C.preparar(sys.argv[1] if len(sys.argv) > 1 else None)
S = M["servicio"]
MI, FD, TC = M["mods"]
warnings.simplefilter("ignore")
TMP = Path(tempfile.mkdtemp(prefix="qa_r03_t106_umb_"))
MO = C.motor(TMP)
SERVIDO = ("SERVED", "SERVED_WITH_LIMITATIONS")


def caso(ficha, i=0):
    c = S.CASOS_CONTROL[ficha][i]
    return C.entrada(c)["valores"], dict(c.get("parametros") or {})


def servir(ficha, valores, params, **extra):
    n = len(MO.almacen.leer("RC"))
    pet = {"operacion": ficha, "datos": [{"valores": valores}], "parametros": params, "fecha_corte": "2026-11-12", **extra}
    try:
        r = MO.servir(pet, "AG-21")
        return r, len(MO.almacen.leer("RC")) - n, None
    except Exception as e:  # noqa: BLE001
        return None, len(MO.almacen.leer("RC")) - n, f"{type(e).__name__}: {e}"[:160]


def huella(r):
    return json.dumps(r.get("resultado"), sort_keys=True, default=str) if r else None


# ------------------------------------------------------------------ 1. cada umbral, con su valor por defecto
faltan = []
for ficha in sorted(MI.UMBRALES):
    v, p = caso(ficha)
    for clave in sorted(MI.UMBRALES[ficha]):
        r, n_rc, e = servir(ficha, copy.deepcopy(v), {**p, clave: copy.deepcopy(MI.PARAMETROS_POR_DEFECTO[ficha][clave])})
        if e or r["estado"] != "RECHAZADO" or "umbrales fijos" not in r["detalle"] or n_rc != 1:
            faltan.append(f"{ficha}.{clave}: {e or r['estado']}")
n_umb = sum(len(x) for x in MI.UMBRALES.values())
C.informe(f"las {n_umb} claves de UMBRALES, con su valor por defecto en la petición: RECHAZADO «umbrales fijos» y en RC",
          not faltan, "; ".join(faltan[:6]))
C.informe("UMBRALES cubre exactamente las claves de umbral de PARAMETROS_POR_DEFECTO (sufijo _min, _rango, _recomendados)",
          all({k for k in d if re.search(r"(_min|_rango|_recomendados|_min_anios)$", k)} <= MI.UMBRALES[f]
              for f, d in MI.PARAMETROS_POR_DEFECTO.items()), "")

# ------------------------------------------------------------------ 2. variantes que se escapan del conjunto
casos_rechazo = []
v, p = caso("IDX-ERP-001")
v["historia_multiplo"] = v["historia_multiplo"][-24:]
casos_rechazo.append(("IDX-ERP-001", "historia del múltiplo de 2 años", v, p, "anios_historia_min", 1))
v, p = caso("IDX-REL-001")
for k in ("indice_a", "indice_b"):
    v[k]["historia"] = v[k]["historia"][-36:]
casos_rechazo.append(("IDX-REL-001", "historia común de 3 años", v, p, "anios_min", 1))
v, p = caso("MON-FIX-001")
v["curva"] = [v["curva"][0], v["curva"][-1]]
casos_rechazo.append(("MON-FIX-001", "dos nodos hasta T", v, p, "nodos_min", 1))
v, p = caso("IDX-CONC-001")
casos_rechazo.append(("IDX-CONC-001", "top_n = 1", v, {**p, "top_n": 1}, "top_n_rango", [0, 10 ** 6]))
v, p = caso("IDX-ERP-001")
casos_rechazo.append(("IDX-ERP-001", "λ = 2", v, {**p, "lambda_reversion": 2}, "lambda_reversion_rango", [-9, 9]))


def variantes(clave, valor):
    homo = clave.replace("o", "о", 1) if "o" in clave else clave.replace("a", "а", 1)   # o/a cirílicas
    return {
        "MAYÚSCULAS": ({"parametros": {clave.upper(): valor}}, None),
        "Capitalizada": ({"parametros": {clave.capitalize(): valor}}, None),
        "con espacio final": ({"parametros": {clave + " ": valor}}, None),
        "con espacio inicial": ({"parametros": {" " + clave: valor}}, None),
        "homoglifo cirílico": ({"parametros": {homo: valor}}, None),
        "guion en vez de guion bajo": ({"parametros": {clave.replace("_", "-"): valor}}, None),
        "anidado en parametros.parametros": ({"parametros": {"parametros": {clave: valor}}}, None),
        "anidado en parametros.umbrales": ({"parametros": {"umbrales": {clave: valor}}}, None),
        "en operacion": ({"operacion_extra": {clave: valor}}, None),
        "en la raíz de la petición": ({"raiz": {clave: valor}}, None),
        "en clase": ({"clase": {clave: valor}}, None),
        "en los datos en línea": ({"valores": {clave: valor}}, None),
        "en un segundo bloque de datos": ({"datos2": {clave: valor}}, None),
    }


escapes = []
for ficha, que, v, p, clave, valor in casos_rechazo:
    r0, _, e0 = servir(ficha, copy.deepcopy(v), dict(p))
    if e0 or r0["estado"] != "RECHAZADO":
        C.informe(f"{ficha}: {que}: el caso base se rechaza", False, e0 or r0["estado"])
        continue
    for nombre, (cambio, _) in variantes(clave, valor).items():
        vv, pp, extra = copy.deepcopy(v), dict(p), {}
        if "parametros" in cambio:
            pp.update(cambio["parametros"])
        if "operacion_extra" in cambio:
            extra["operacion"] = {"ficha_id": ficha, **cambio["operacion_extra"], "parametros": cambio["operacion_extra"]}
        if "raiz" in cambio:
            extra.update(cambio["raiz"])
        if "clase" in cambio:
            extra["clase"] = cambio["clase"]
        if "valores" in cambio:
            vv.update(cambio["valores"])
        if "datos2" in cambio:
            n = len(MO.almacen.leer("RC"))
            try:
                r = MO.servir({"operacion": ficha, "datos": [{"valores": vv}, {"valores": cambio["datos2"]}], "parametros": pp,
                               "fecha_corte": "2026-11-12"}, "AG-21")
                e = None
            except Exception as exc:  # noqa: BLE001
                r, e = None, f"{type(exc).__name__}: {exc}"[:120]
        else:
            r, _, e = servir(ficha, vv, pp, **extra)
        if e or r["estado"] in SERVIDO:
            escapes.append(f"{ficha} {clave} {nombre}: {e or r['estado']}")
C.informe(f"ninguna de {13 * len(casos_rechazo)} variantes (mayúsculas, espacios, homoglifos, anidados, raíz, clase, datos) "
          "convierte un rechazo por umbral en servido", not escapes, "; ".join(escapes[:6]))

# Con el caso de control servido, ninguna variante cambia la cifra
cambian = []
for ficha in sorted(MI.UMBRALES):
    v, p = caso(ficha)
    r0, _, _ = servir(ficha, copy.deepcopy(v), dict(p))
    for clave in sorted(MI.UMBRALES[ficha]):
        valor = MI.PARAMETROS_POR_DEFECTO[ficha][clave]
        valor = [x * 0 for x in valor] if isinstance(valor, list) else 0
        for pp in ({**p, clave.upper(): valor}, {**p, "parametros": {clave: valor}}):
            r, _, e = servir(ficha, copy.deepcopy(v), pp)
            if e or (r["estado"] in SERVIDO and huella(r) != huella(r0)):
                cambian.append(f"{ficha} {sorted(pp)[-1]}: {e or 'cifra distinta'}")
        vv = copy.deepcopy(v)
        vv[clave] = valor
        r, _, e = servir(ficha, vv, dict(p))
        if e or (r["estado"] in SERVIDO and huella(r) != huella(r0)):
            cambian.append(f"{ficha} valores.{clave}: {e or 'cifra distinta'}")
C.informe("con el caso de control, el umbral escrito de otra forma o en los datos no cambia la cifra servida", not cambian,
          "; ".join(cambian[:6]))

# ------------------------------------------------------------------ 3. auditoría: claves leídas de `p`
no_declaradas = {}
for nombre, fn in inspect.getmembers(MI, inspect.isfunction):
    if not nombre.startswith(("f_", "_estudio", "_evento", "_car")):
        continue
    src = inspect.getsource(fn)
    leidas = set(re.findall(r'\bp\["([A-Za-z_0-9]+)"\]', src)) | set(re.findall(r'\bp\.get\("([A-Za-z_0-9]+)"', src))
    declaradas = set().union(*MI.PARAMETROS_POR_DEFECTO.values())
    extra = sorted(leidas - declaradas)
    if extra:
        no_declaradas[nombre] = extra
C.informe("auditoría: claves que los manejadores MON/IDX leen de los parámetros sin estar en PARAMETROS_POR_DEFECTO "
          "(informativo: opcionales de la petición)", True, json.dumps(no_declaradas, ensure_ascii=False))
fuera = {f: sorted(k for k in d if k not in MI.UMBRALES[f] and re.search(r"(umbral|minimo|maximo|_max)$", k))
         for f, d in MI.PARAMETROS_POR_DEFECTO.items()}
C.informe("ningún parámetro con nombre de umbral (umbral, minimo, maximo, _max) queda fuera de UMBRALES",
          not any(fuera.values()), json.dumps({k: x for k, x in fuera.items() if x}, ensure_ascii=False))

# ------------------------------------------------------------------ 4. ventanas sin rango: 0, negativas, no enteras
VENTANAS = [("MON-EXP-001", "diferencial_estable_dias", "historia_diferencial"),
            ("IDX-CONC-001", "media_amplitud", None),
            ("IDX-REB-001", "sesiones_estimacion", None),
            ("IDX-REB-001", "ventana_post_sesiones", None),
            ("IDX-REL-001", "momentum_retro_meses", None),
            ("IDX-REL-001", "momentum_salto_meses", None),
            ("IDX-REL-001", "momentum_corto_meses", None),
            ("IDX-REL-001", "ventana_anios", None),
            ("IDX-CONC-001", "ventana_percentil_anios", None),
            ("MON-REAL-001", "plazo_meses", None),
            ("MON-FIX-001", "tau_meses", None)]
servidas = []
for ficha, clave, requiere in VENTANAS:
    base_c = None
    for i, c in enumerate(S.CASOS_CONTROL[ficha]):
        vv, pp = caso(ficha, i)
        if requiere and requiere not in vv:
            continue
        if requiere == "historia_diferencial":
            vv.pop("diferencial_estable", None)
        r0, _, e0 = servir(ficha, copy.deepcopy(vv), dict(pp))
        if not e0 and r0["estado"] in SERVIDO:
            base_c = (vv, pp, r0)
            break
    if base_c is None and requiere == "historia_diferencial":
        vv, pp = caso(ficha)
        dif = vv.pop("diferencial_estable", 0.001)
        vv["historia_diferencial"] = [dif] * 30
        r0, _, e0 = servir(ficha, copy.deepcopy(vv), dict(pp))
        base_c = (vv, pp, r0) if not e0 and r0["estado"] in SERVIDO else None
    if base_c is None:
        C.informe(f"{ficha}.{clave}: hay un caso servido de partida", False, "")
        continue
    vv, pp, r0 = base_c
    for valor in (0, -1, -20, 2.5):
        if clave in ("ventana_percentil_anios", "ventana_anios") and valor == 2.5:
            continue
        r, _, e = servir(ficha, copy.deepcopy(vv), {**pp, clave: valor})
        if e:
            servidas.append(f"{ficha}.{clave}={valor}: excepción {e[:60]}")
        elif r["estado"] in SERVIDO:
            servidas.append(f"{ficha}.{clave}={valor}: {r['estado']}" + (" (misma cifra)" if huella(r) == huella(r0) else ""))
C.informe("una ventana 0, negativa o no entera en MON/IDX se rechaza (no se sirve una cifra con otra ventana)", not servidas,
          "; ".join(servidas))

# 4b. Lo mismo en las 21, de forma genérica: cada parámetro numérico positivo por defecto (no umbral), con 0 y −1, sobre el
# caso de control. «cambia» = se sirve otra cifra (el parámetro se usa y se acepta fuera de dominio); «igual» = se sirve la
# misma (el caso no ejercita ese parámetro: informativo).
defectos = {**MI.PARAMETROS_POR_DEFECTO, **FD.PARAMETROS_POR_DEFECTO, **TC.PARAMETROS_POR_DEFECTO}
cambia, igual = [], []
for ficha in sorted(S.CASOS_CONTROL):
    v, p = caso(ficha)
    r0, _, e0 = servir(ficha, copy.deepcopy(v), dict(p))
    if e0 or r0["estado"] not in SERVIDO:
        continue
    umbr = MI.UMBRALES.get(ficha, frozenset()) | set(TC.UMBRALES.get(ficha, {}))
    for clave, val in sorted(defectos[ficha].items()):
        if clave in umbr or isinstance(val, bool) or not isinstance(val, (int, float)) or val <= 0:
            continue
        for x in (0, -1):
            lo_hi = FD.RANGOS.get(ficha, {}).get(clave)
            if lo_hi and lo_hi[0] <= x <= lo_hi[1]:
                continue   # dentro del rango que da la ficha (p. ej., κ = 0 en FON-DISC): es un valor admitido
            r, _, e = servir(ficha, copy.deepcopy(v), {**p, clave: x})
            if e:
                cambia.append(f"{ficha}.{clave}={x}: excepción")
            elif r["estado"] in SERVIDO:
                (cambia if huella(r) != huella(r0) else igual).append(f"{ficha}.{clave}={x}")
fam = sorted({x.split(".")[0] for x in cambia})
C.informe("en las 21, ningún parámetro numérico de ventana o plazo en 0 o negativo da una cifra servida distinta", not cambia,
          f"fichas: {fam} · " + "; ".join(cambia))
print(f"      (informativo) servidos con la misma cifra (el caso no ejercita el parámetro): {'; '.join(igual)}")

# ------------------------------------------------------------------ 5. contraste: FON, DER y TCV
cambios = []
for ficha in sorted(FD.MINIMOS):
    v, p = caso(ficha)
    r0, _, _ = servir(ficha, copy.deepcopy(v), dict(p))
    for clave, val in sorted(FD.MINIMOS[ficha].items()):
        laxo = 0 if isinstance(val, (int, float)) and not isinstance(val, bool) else val
        r, _, e = servir(ficha, copy.deepcopy(v), {**p, clave: laxo})
        if e or (r["estado"] in SERVIDO and huella(r) != huella(r0)) or (r0["estado"] == "RECHAZADO" and r["estado"] in SERVIDO):
            cambios.append(f"{ficha}.{clave}: {e or r['estado']}")
for ficha in sorted(TC.UMBRALES):
    v, p = caso(ficha)
    for clave, val in sorted(TC.UMBRALES[ficha].items()):
        r, _, e = servir(ficha, copy.deepcopy(v), {**p, clave: val})
        if e or r["estado"] != "RECHAZADO":
            cambios.append(f"{ficha}.{clave}: {e or r['estado']}")
C.informe("FON/DER: un mínimo de MINIMOS en la petición no cambia la cifra; TCV: un UMBRALES en la petición se rechaza",
          not cambios, "; ".join(cambios[:6]))

shutil.rmtree(TMP, ignore_errors=True)
sys.exit(C.resumen())
