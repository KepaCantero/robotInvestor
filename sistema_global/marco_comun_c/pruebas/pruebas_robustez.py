"""Pruebas de robustez de F, D y CT-G-14 (V0.37, Pieza 1). Datos SIMULADOS.

Uso: python3 pruebas/pruebas_robustez.py

Demuestra con entradas mutadas al azar, con semilla fija (random.Random(20261107), nunca el random
global), que tres validadores cumplen sus promesas: nunca lanzan, no mutan la entrada, son
deterministas y fallan cerrado. Una comprobación puede cubrir N casos («no lanza en 500 mutaciones»
cuenta como una).

Mutaciones: borrar una clave (o un elemento de lista) o añadir una clave extra; cambiar un valor por
None, "", "x", [], {}, True, 0, -1, 1e308, NaN, +inf, -inf o un número como texto («1.1»); y cambiar
una fecha por «2026-13-45», «ayer» o una fecha sin zona horaria.

Las mutaciones «de forma» de la solicitud, la cartera, la política, el contexto o el instante (clave de
más o de menos, tipo cambiado) deben acabar en VETADO con F-01; las del registro CT-G-14, en RM-01.
Las «de valor» (un número por otro número, un texto por otro texto) solo deben cumplir las promesas
generales.

Excepciones por diseño (no son defectos; cada una tiene su comprobación):
- el contexto de F admite None en `eventos`, `precio_intermediario` y `mandato.instrumentos_permitidos`:
  pasar de la lista o el diccionario a None no da F-01 (dan F-21 o F-23, que es lo correcto) y los
  cambios entre None, lista y diccionario cuentan como «de valor», no «de forma»;
- la raíz entera del CONTEXTO sustituida por None es el uso de E sin contexto (APROBADO por diseño,
  r03): los bucles aleatorios no la exigen como «de forma» ni comparan el informe resultante — que se
  veta «falta el contexto» — con el controlar(None) del uso de E; el barrido sistemático y las
  comprobaciones fijas lo demuestran aparte;
- un CT-G-14 LIBRE admite borrar `via_acceso` (la vía es obligatoria salvo en una operación libre):
  sigue válido;
- `validar_informe_f` no puede detectar por recálculo un `event_id` cambiado (no hay valor esperado que
  comparar): lo cubren el hash del mensaje entero, que liga la pantalla de aprobación (O-27) y el
  duplicado (O-03); la comprobación correspondiente lo demuestra.
"""
from __future__ import annotations

import copy
import math
import random
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))

from comparador import comparar_candidatos  # noqa: E402
from control_f import ENVOLTURA, POLITICA_DEFECTO, construir_informe, controlar, hash_contenido, validar_informe_f  # noqa: E402
from manual_g import validar_manual  # noqa: E402
from pruebas_comparador import cand  # noqa: E402
from pruebas_control_f import AHORA_F, CART, informe_f, solicitud  # noqa: E402
from pruebas_control_f_t22 import CTX  # noqa: E402
from pruebas_manual import T1, T2, libre  # noqa: E402
from pruebas_orquestador import AHORA, Arnes, nuevo, hasta  # noqa: E402

SEMILLA = 20261107
CASOS_F = 500        # controlar: 100 por cada una de las cinco entradas (rotación)
CASOS_INFORME = 200  # construir_informe: 40 por cada una de las cinco entradas (rotación)
CASOS_CF = 300       # validar_informe_f sobre el informe mutado
CASOS_D = 500        # comparar_candidatos: 250 mutando cada candidato (alternando)
CASOS_RM = 300       # validar_manual sobre el registro LIBRE mutado

VENENO = [None, "", "x", [], {}, True, 0, -1, 1e308, float("nan"), float("inf"), -float("inf"), "1.1"]
FECHAS_MALAS = ["2026-13-45", "ayer", "2026-11-06T09:00:00"]   # fecha imposible, texto y fecha sin zona
_FH = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})\Z")
_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}\Z")
# Los diez motivos de exclusión de la cabecera de validador/comparador.py
MOTIVOS_D = {"FORMA", "DUPLICADO", "EXCLUSION_DURA", "CADUCADO", "SIN_ESCENARIOS", "SIN_RETORNO_POSITIVO",
             "NO_SUPERA_REFERENCIA", "ESCENARIOS_SUPUESTO", "SIN_CONFIANZA", "SIN_STOP"}
# Nodos del contexto de F que admiten None por diseño (T-22): entre sus formas legales no hay «tipo cambiado»
OPCIONALES_NONE_F = {("eventos",), ("precio_intermediario",), ("mandato", "instrumentos_permitidos")}


def _parece_fecha(x):
    return isinstance(x, str) and bool(_FH.match(x) or _FECHA.match(x))


def _tipo(x):
    if isinstance(x, bool):
        return "bool"
    if isinstance(x, (int, float)):
        return "num"
    if isinstance(x, str):
        return "str"
    if x is None:
        return "none"
    if isinstance(x, list):
        return "list"
    if isinstance(x, dict):
        return "dict"
    return "otro"


def caminos(x, base=()):
    """Las rutas (tuplas de claves e índices) a todos los nodos del objeto, raíz incluida."""
    out = [base]
    if isinstance(x, dict):
        for k, v in x.items():
            out += caminos(v, base + (k,))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            out += caminos(v, base + (i,))
    return out


def _veneno_distinto(nodo, rng):
    return rng.choice([v for v in VENENO if v != nodo])


def _mutar_en_sitio(c, rng):
    """Aplica UNA mutación al azar en un camino al azar sobre `c` (en sitio) y devuelve (objeto, registro)
    con {ruta, op, antes, despues} para clasificarla. En la raíz escalar devuelve el objeto nuevo."""
    ruta = rng.choice(caminos(c))
    if not ruta:
        padre, clave, nodo = None, None, c
    else:
        cont = c
        for k in ruta[:-1]:
            cont = cont[k]
        clave = ruta[-1]
        padre, nodo = cont, cont[clave]
    ops = []
    if padre is not None:
        ops.append("borrar")
    if isinstance(nodo, dict):
        ops += ["extra", "extra"]
    ops += ["valor", "valor"]
    if _parece_fecha(nodo):
        ops.append("fecha")
    op = rng.choice(ops)
    info = {"ruta": ruta, "op": op, "antes": nodo, "despues": None}
    if op == "borrar":
        if isinstance(padre, dict):
            del padre[clave]
        else:
            padre.pop(clave)
    elif op == "extra":
        nodo["extra"] = "x"
        info["antes"], info["despues"] = None, "x"
    else:
        nuevo = rng.choice(FECHAS_MALAS) if op == "fecha" else _veneno_distinto(nodo, rng)
        info["despues"] = nuevo
        if padre is None:   # la raíz es un escalar (el instante): se sustituye entera
            return nuevo, info
        padre[clave] = nuevo
    return c, info


def mutar(obj, rng):
    """Copia profunda de `obj` con una mutación al azar en un camino al azar."""
    c, _ = _mutar_en_sitio(copy.deepcopy(obj), rng)
    return c


def _es_forma(info):
    """True si la mutación es «de forma»: clave de menos, clave de más o tipo cambiado."""
    if info["op"] in ("borrar", "extra"):
        return True
    tv, tn = _tipo(info["antes"]), _tipo(info["despues"])
    if tv == tn:
        return False
    if info["ruta"] in OPCIONALES_NONE_F and {tv, tn} <= {"none", "list", "dict"}:
        return False   # entre las formas legales de un campo que admite None: es «de valor»
    return True


def _es_uso_de_E(info, entrada):
    """True si la mutación sustituyó el CONTEXTO entero (raíz) por None: es el uso de E sin contexto,
    APROBADO por diseño (r03): no es «de forma», no exige F-01 y el informe se veta «falta el contexto»
    sin compararse con el controlar(None) del uso de E. Para cualquier otra entrada es «de forma"."""
    return entrada == "contexto" and info["ruta"] == () and info["despues"] is None


def _numeros_raros(x):
    """Los números no finitos colgando de una estructura (NaN o infinitos)."""
    if isinstance(x, dict):
        return sum(_numeros_raros(v) for v in x.values())
    if isinstance(x, list):
        return sum(_numeros_raros(v) for v in x)
    return 1 if (isinstance(x, float) and not isinstance(x, bool) and not math.isfinite(x)) else 0


def _igual_nan(a, b):
    """Igualdad profunda que trata NaN == NaN (r04): el generador puede dejar la RAÍZ del objeto en NaN
    (jugada legal del veneno) y `nan != nan` es cierto aunque nadie haya tocado nada, de modo que la
    comparación llana con != contaría una mutación inexistente."""
    if isinstance(a, float) and isinstance(b, float):
        if math.isnan(a) and math.isnan(b):
            return True
        return a == b
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_igual_nan(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_igual_nan(x, y) for x, y in zip(a, b))
    try:
        return bool(a == b)
    except Exception:   # noqa: BLE001
        return a is b


def _veta_f01(r):
    return isinstance(r, dict) and r.get("resultado") == "VETADO" and any(
        c.get("regla") == "F-01" and c.get("resultado") == "VETA" for c in r.get("controles", []))


def _veta_f12(r):
    """VETADO por F-12: sin tipo de cambio no se puede valorar en euros (la regla que aplica F a una
    cartera con la tabla de cambios sin la divisa que hace falta)."""
    return isinstance(r, dict) and r.get("resultado") == "VETADO" and any(
        c.get("regla") == "F-12" and c.get("resultado") == "VETA" for c in r.get("controles", []))


def main():
    rng = random.Random(SEMILLA)
    h = Arnes()

    # ---------------------------------------------------------------- el generador de mutaciones
    d = {"a": 1, "b": [10, {"c": None}]}
    esperadas = {(), ("a",), ("b",), ("b", 0), ("b", 1), ("b", 1, "c")}
    h.chk("generador_caminos_lista_todos_los_nodos", set(caminos(d)) == esperadas, sorted(map(str, caminos(d))))

    def plantilla():
        return {"n": 1.5, "s": "texto", "f": "2026-11-06T09:00:00+00:00", "l": [1, {"k": "v"}], "d": {"m": None}}
    bien, distintas = True, set()
    for _ in range(200):
        orig = plantilla()
        foto = copy.deepcopy(orig)
        m = mutar(orig, rng)
        bien &= orig == foto and m != orig
        distintas.add(repr(m))
    h.chk("generador_mutar_da_copia_y_no_toca_el_original", bien and len(distintas) > 5, f"{len(distintas)} mutaciones distintas")
    a = [repr(mutar(plantilla(), random.Random(SEMILLA))) for _ in range(50)]
    b = [repr(mutar(plantilla(), random.Random(SEMILLA))) for _ in range(50)]
    h.chk("generador_con_la_misma_semilla_da_las_mismas_mutaciones", a == b)

    # ---------------------------------------------------------------- F: controlar (500 casos)
    sol0, cart0, pol0, ahora0, ctx0 = solicitud(), {**CART}, dict(POLITICA_DEFECTO), AHORA_F, copy.deepcopy(CTX)
    h.chk("F_base_aprobado_sin_mutar", controlar(sol0, cart0, pol0, ahora0, ctx0)["resultado"] == "APROBADO"
          and controlar(sol0, cart0, pol0, ahora0)["resultado"] == "APROBADO")

    def entradas_f():
        return {"solicitud": copy.deepcopy(sol0), "cartera": copy.deepcopy(cart0), "politica": copy.deepcopy(pol0),
                "ahora": ahora0, "contexto": copy.deepcopy(ctx0)}

    ROTACION_F = ("solicitud", "cartera", "politica", "ahora", "contexto")
    st = {n: {"lanz": 0, "muta": 0, "res": 0, "cant": 0, "det": 0, "forma": 0, "forma_mal": 0, "valor": 0, "fx": 0,
              "de_menos": [0, 0], "de_mas": [0, 0], "tipo": [0, 0], "malas": []} for n in ROTACION_F}
    casos_malos = []
    for i in range(CASOS_F):
        nombre = ROTACION_F[i % 5]
        fuentes = entradas_f()
        fuentes[nombre], info = _mutar_en_sitio(fuentes[nombre], rng)
        antes = copy.deepcopy(fuentes)
        sol, cart, pol, ahora, ctx = (fuentes["solicitud"], fuentes["cartera"], fuentes["politica"],
                                      fuentes["ahora"], fuentes["contexto"])
        s = st[nombre]
        try:
            r = controlar(sol, cart, pol, ahora, ctx)
        except Exception as ex:   # noqa: BLE001
            s["lanz"] += 1
            casos_malos.append(f"{nombre}: lanza {type(ex).__name__}")
            continue
        if fuentes != antes:
            s["muta"] += 1
            casos_malos.append(f"{nombre}: muta la entrada")
        if r.get("resultado") not in ("APROBADO", "REDUCIDO", "VETADO"):
            s["res"] += 1
            casos_malos.append(f"{nombre}: resultado {r.get('resultado')!r}")
        elif r["resultado"] == "VETADO" and r["cantidad_aprobada"] != 0.0:
            s["cant"] += 1
            casos_malos.append(f"{nombre}: veto con cantidad {r['cantidad_aprobada']}")
        if r.get("resultado") in ("APROBADO", "REDUCIDO"):
            q = sol.get("cantidad") if isinstance(sol, dict) else None
            if not isinstance(q, (int, float)) or isinstance(q, bool) or r["cantidad_aprobada"] > q:
                s["cant"] += 1
                casos_malos.append(f"{nombre}: aprueba más de lo solicitado")
        r2 = controlar(copy.deepcopy(sol), copy.deepcopy(cart), copy.deepcopy(pol), ahora, copy.deepcopy(ctx))
        if r2 != r:
            s["det"] += 1
            casos_malos.append(f"{nombre}: no es determinista")
        if _es_uso_de_E(info, nombre):
            s["valor"] += 1   # la raíz del contexto a None es el uso de E: APROBADO por diseño, no exige F-01 (r03)
        elif _es_forma(info):
            s["forma"] += 1
            en_fx = info["ruta"][:1] == ("tipos_cambio_eur",) and info["ruta"] != ("tipos_cambio_eur",)
            if _veta_f01(r) or (en_fx and nombre == "cartera" and _veta_f12(r)):
                s["fx"] += 1 if (en_fx and not _veta_f01(r)) else 0
            else:
                s["forma_mal"] += 1
                caso = f"{nombre}: forma sin F-01: {info['op']} en {info['ruta']} " \
                       f"({info['antes']!r} -> {info['despues']!r})"
                casos_malos.append(caso)
                s["malas"].append(caso)
            sub = "de_menos" if info["op"] == "borrar" else "de_mas" if info["op"] == "extra" else "tipo"
            s[sub][1] += 1
            s[sub][0] += 0 if (_veta_f01(r) or (en_fx and _veta_f12(r))) else 1
        else:
            s["valor"] += 1
    tot = lambda k: sum(st[n][k] for n in ROTACION_F)
    h.chk("F_no_lanza_en_500_mutaciones", tot("lanz") == 0, casos_malos[:5])
    h.chk("F_no_muta_las_entradas_en_500_mutaciones", tot("muta") == 0, casos_malos[:5])
    h.chk("F_resultado_siempre_entre_APROBADO_REDUCIDO_VETADO_en_500_mutaciones", tot("res") == 0, casos_malos[:5])
    h.chk("F_vetado_con_cantidad_cero_y_nunca_mas_de_lo_solicitado_en_500_mutaciones", tot("cant") == 0, casos_malos[:5])
    h.chk("F_determinista_en_500_mutaciones", tot("det") == 0, casos_malos[:5])
    for n, etiqueta in (("solicitud", "de_la_solicitud"), ("cartera", "de_la_cartera"), ("politica", "de_la_politica"),
                        ("contexto", "del_contexto"), ("ahora", "del_instante_cobertura_extra")):
        s = st[n]
        detalle = {k: v for k, v in s.items() if k in ("forma", "forma_mal", "valor", "fx", "de_menos", "de_mas", "tipo", "malas")}
        h.chk(f"F_forma_{etiqueta}_veta_F01_en_{s['forma']}_casos", s["forma"] > 0 and s["forma_mal"] == 0, detalle)

    def barrida(nombre, fabrica):
        """Barrido sistemático, sin azar: borrar cada clave de primer nivel, añadir «extra» y sustituir el
        objeto entero. Todo debe acabar en VETADO con F-01. El contexto entero a None no va: es el uso
        de E sin contexto, y tiene su comprobación fija aparte."""
        mal = []
        base = fabrica()
        for k in sorted(base) if isinstance(base, dict) else []:
            b = fabrica()
            del b[k]
            if not _veta_f01(controlar(*_args_con(nombre, b))):
                mal.append(f"sin {k}")
        for v in ([], "x", {}, 0) if nombre == "contexto" else ([], "x", None, 0):
            if not _veta_f01(controlar(*_args_con(nombre, v))):
                mal.append(f"objeto {v!r}")
        b = fabrica()
        b["extra"] = "x"
        if not _veta_f01(controlar(*_args_con(nombre, b))):
            mal.append("con extra")
        return mal

    def _args_con(nombre, valor):
        f = {"solicitud": copy.deepcopy(sol0), "cartera": copy.deepcopy(cart0), "politica": copy.deepcopy(pol0),
             "ahora": ahora0, "contexto": copy.deepcopy(ctx0)}
        f[nombre] = valor
        return f["solicitud"], f["cartera"], f["politica"], f["ahora"], f["contexto"]
    mal = barrida("solicitud", lambda: solicitud())
    h.chk("F_barrido_sistematico_de_la_solicitud_veta_F01", not mal, mal)
    mal = barrida("cartera", lambda: {**CART})
    h.chk("F_barrido_sistematico_de_la_cartera_veta_F01", not mal, mal)
    mal = barrida("politica", lambda: dict(POLITICA_DEFECTO))
    h.chk("F_barrido_sistematico_de_la_politica_veta_F01", not mal, mal)
    mal = barrida("contexto", lambda: copy.deepcopy(CTX))
    h.chk("F_barrido_sistematico_del_contexto_veta_F01", not mal, mal)
    r_e = controlar(sol0, cart0, pol0, ahora0, None)
    h.chk("F_sin_contexto_es_el_uso_de_E_y_no_aplica_las_reglas_de_contexto_por_diseno",
          r_e["resultado"] == "APROBADO" and not any(c["regla"] in ("F-18", "F-21", "F-22", "F-23") for c in r_e["controles"]) and any(c["regla"] == "F-13" for c in r_e["controles"]), r_e)
    cart_fx = copy.deepcopy(CART)   # r05: copia profunda; una copia al primer nivel mutilaría la CART compartida
    del cart_fx["tipos_cambio_eur"]["USD"]
    h.chk("F_cartera_con_la_tabla_de_cambios_sin_la_divisa_da_F12_por_diseno",
          _veta_f12(controlar(sol0, cart_fx, pol0, ahora0)), controlar(sol0, cart_fx, pol0, ahora0))
    h.chk("r05_la_comprobacion_f12_no_mutila_la_cartera_compartida",
          CART["tipos_cambio_eur"].get("USD") == 1.0, CART["tipos_cambio_eur"])
    r01_mal = []
    for pe, sp, fx in ((5e-324, 1e-310, 5e-324), (1e-170, 1e-171, 1e-170)):
        try:
            rr01 = controlar(solicitud(precio_entrada=pe, stop_precio=sp),
                             {**copy.deepcopy(CART), "tipos_cambio_eur": {"USD": fx}}, pol0, ahora0,
                             copy.deepcopy(CTX))
            if not (rr01.get("resultado") == "VETADO" and rr01.get("cantidad_aprobada") == 0.0):
                r01_mal.append(f"precio {pe} con cambio {fx}: resultado {rr01.get('resultado')!r}")
        except Exception as ex:   # noqa: BLE001
            r01_mal.append(f"precio {pe} con cambio {fx}: lanza {type(ex).__name__}")
    h.chk("r01_controlar_no_lanza_con_precio_y_cambio_que_subdesbordan_a_cero", not r01_mal, r01_mal)

    # ---------------------------------------------------------------- F: construir_informe (200 casos)
    o = nuevo()
    hasta(o, "PROPUESTA")
    prop = copy.deepcopy(o.expedientes["EXP-0001"]["propuesta"])
    base_inf = informe_f(o)
    si = {"lanz": 0, "muta": 0, "forma": 0, "res": 0, "cant": 0, "coher": 0, "det": 0, "n": 0, "sin_ctx": 0}
    ROTACION_I = ("solicitud", "cartera", "politica", "ahora", "contexto")
    for i in range(CASOS_INFORME):
        nombre_i = ROTACION_I[i % 5]
        fuentes = entradas_f()
        fuentes[nombre_i], info_i = _mutar_en_sitio(fuentes[nombre_i], rng)
        antes = copy.deepcopy(fuentes)
        sol, cart, pol, ahora, ctx = (fuentes["solicitud"], fuentes["cartera"], fuentes["politica"],
                                      fuentes["ahora"], fuentes["contexto"])
        try:
            inf = construir_informe("EV-F-0901", "EXP-0001", "COR-0001", prop, sol, cart, pol, ahora,
                                    "2026-11-07T09:00:00+00:00", contexto=ctx)
        except Exception as ex:   # noqa: BLE001
            si["lanz"] += 1
            continue
        si["n"] += 1
        if fuentes != antes:
            si["muta"] += 1
        if not (isinstance(inf, dict) and set(inf) == ENVOLTURA):
            si["forma"] += 1
            continue
        res, cant = inf["resultado_politica"]["resultado"], inf["payload"]["cantidad_aprobada"]
        if res not in ("APROBADO", "REDUCIDO", "VETADO"):
            si["res"] += 1
        elif res == "VETADO" and cant != 0.0:
            si["cant"] += 1
        if _es_uso_de_E(info_i, nombre_i):
            si["sin_ctx"] += 1   # el informe sin contexto se veta «falta el contexto» (F-01) y controlar(None) es el uso de E: no se comparan (r03)
        else:
            r = controlar(sol, cart, pol, ahora, ctx)
            if res != r["resultado"] or cant != r["cantidad_aprobada"]:
                si["coher"] += 1
        inf2 = construir_informe("EV-F-0901", "EXP-0001", "COR-0001", prop, copy.deepcopy(sol), copy.deepcopy(cart),
                                 copy.deepcopy(pol), ahora, "2026-11-07T09:00:00+00:00", contexto=copy.deepcopy(ctx))
        if inf2 != inf:
            si["det"] += 1
    h.chk("F_informe_no_lanza_en_200_mutaciones", si["lanz"] == 0, si)
    h.chk("F_informe_no_muta_las_entradas_en_200_mutaciones", si["muta"] == 0, si)
    h.chk("F_informe_envoltura_y_resultado_validos_en_200_mutaciones", si["forma"] == 0 and si["res"] == 0, si)
    h.chk("F_informe_vetado_con_cantidad_cero_en_200_mutaciones", si["cant"] == 0, si)
    h.chk("F_informe_coherente_con_controlar_en_200_mutaciones", si["coher"] == 0, si)
    h.chk("F_informe_determinista_en_200_mutaciones", si["det"] == 0, si)
    inf_sc = construir_informe("EV-F-0901", "EXP-0001", "COR-0001", prop, copy.deepcopy(sol0), copy.deepcopy(cart0),
                               copy.deepcopy(pol0), ahora0, "2026-11-07T09:00:00+00:00", contexto=None)
    h.chk("r03_la_raiz_del_contexto_a_none_es_el_uso_de_E_y_no_exige_F01_ni_coherencia",
          _es_uso_de_E({"ruta": (), "op": "valor", "antes": "diccionario", "despues": None}, "contexto")
          and not _es_uso_de_E({"ruta": (), "op": "valor", "antes": "diccionario", "despues": None}, "solicitud")
          and inf_sc["resultado_politica"]["resultado"] == "VETADO" and r_e["resultado"] == "APROBADO",
          {"informe sin contexto": inf_sc["resultado_politica"], "controlar sin contexto": r_e["resultado"]})

    # ---------------------------------------------------------------- CF: validar_informe_f (300 casos)
    x = o.expedientes["EXP-0001"]

    def ctx_valido(informe):
        return {"ahora": AHORA, "expediente_id": "EXP-0001", "correlation_id": x["correlation_id"], "divisa_cotizacion": "USD",
                "propuesta": x["propuesta"], "cartera_destino": x["cartera_destino"], "politica": o.cfg["politica_f"],
                "contexto": o._contexto_de_informe("EXP-0001", informe)}

    h.chk("CF_base_informe_valido", validar_informe_f(base_inf, ctx_valido(base_inf)) == [],
          validar_informe_f(base_inf, ctx_valido(base_inf)))
    scf = {"lanz": 0, "nolista": 0, "muta": 0, "env": [0, 0], "int": [0, 0], "malas": []}
    for _ in range(CASOS_CF):
        m, info = _mutar_en_sitio(copy.deepcopy(base_inf), rng)
        foto = copy.deepcopy(m)
        try:
            fallos = validar_informe_f(m, ctx_valido(m))
        except Exception as ex:   # noqa: BLE001
            scf["lanz"] += 1
            scf["malas"].append(f"lanza {type(ex).__name__} en {info['ruta']}")
            continue
        if not isinstance(fallos, list):
            scf["nolista"] += 1
            continue
        if not _igual_nan(m, foto):
            scf["muta"] += 1
        hueco = len(info["ruta"]) <= 1
        if info["ruta"] == ("event_id",):
            continue   # por diseño: el recálculo no puede verlo; se comprueba aparte más abajo
        if hueco:
            scf["env"][1] += 1
            if not fallos:
                scf["env"][0] += 1
                scf["malas"].append(f"envoltura sin fallo: {info['ruta']} {info['op']}")
        else:
            scf["int"][1] += 1
            if not fallos:
                scf["int"][0] += 1
                scf["malas"].append(f"interna sin fallo: {info['ruta']} {info['op']}")
    h.chk("CF_validar_no_lanza_y_devuelve_lista_en_300_mutaciones", scf["lanz"] == 0 and scf["nolista"] == 0, scf["malas"][:5])
    h.chk("CF_validar_no_muta_el_informe_en_300_mutaciones", scf["muta"] == 0, scf["malas"][:5])
    h.chk("CF_toda_mutacion_de_envoltura_da_al_menos_un_fallo_salvo_event_id", scf["env"][0] == 0 and scf["env"][1] > 0,
          {"sin fallo": scf["env"][0], "casos": scf["env"][1], "malas": scf["malas"][:5]})
    h.chk("CF_toda_mutacion_interna_da_al_menos_un_fallo", scf["int"][0] == 0 and scf["int"][1] > 0,
          {"sin fallo": scf["int"][0], "casos": scf["int"][1], "malas": scf["malas"][:5]})
    eve = {"sin_fallos": 0, "hash_cambia": 0, "casos": 0}
    for vid in ("x", "1.1", None):
        m = copy.deepcopy(base_inf)
        m["event_id"] = vid
        eve["casos"] += 1
        eve["sin_fallos"] += int(not validar_informe_f(m, ctx_valido(m)))
        eve["hash_cambia"] += int(hash_contenido(m) != hash_contenido(base_inf))
    h.chk("CF_event_id_cambiado_no_lo_ve_el_recalculo_lo_cubren_el_hash_O27_y_el_duplicado_O03",
          eve["sin_fallos"] == 2 and eve["hash_cambia"] == 3, eve)
    r04_mal = []
    if not _igual_nan(float("nan"), float("nan")):
        r04_mal.append("nan != nan sigue contando como mutación")
    d4 = {"a": 1.0, "b": [1, {"c": float("nan")}]}
    if not _igual_nan(d4, copy.deepcopy(d4)):
        r04_mal.append("falso mutado con NaN anidado")
    if _igual_nan({"a": 1.0}, {"a": 2.0}) or _igual_nan({"a": 1.0}, {"a": 1.0, "b": 2}):
        r04_mal.append("la comparación ya no ve cambios reales")
    h.chk("r04_la_comparacion_no_muta_trata_nan_igual_a_nan", not r04_mal, r04_mal)

    # ---------------------------------------------------------------- D: comparar_candidatos (500 casos)
    a0, b0 = cand(1), cand(2, esperado=(3.0, 0.5, -4.0))
    r = comparar_candidatos([copy.deepcopy(a0), copy.deepcopy(b0)], AHORA)
    h.chk("D_base_ordena_los_dos_candidatos", r["ok"] and [d["expediente_id"] for d in r["grupos"]["Q"]["ranking"]]
          == ["EXP-0001", "EXP-0002"] and r["decision_global"] == "INVERTIR", r)
    sd = {"lanz": 0, "ok_mal": 0, "fuera": 0, "raros": 0, "orden": 0, "det": 0, "muta": 0, "n_ok": 0, "malas": []}
    for i in range(CASOS_D):
        par = [copy.deepcopy(a0), copy.deepcopy(b0)]
        par[i % 2], info = _mutar_en_sitio(par[i % 2], rng)
        a, b = par
        objetivo = par[i % 2]
        foto = copy.deepcopy((a, b))
        try:
            r = comparar_candidatos([a, b], AHORA)
        except Exception as ex:   # noqa: BLE001
            sd["lanz"] += 1
            sd["malas"].append(f"lanza {type(ex).__name__} en {info['ruta']}")
            continue
        if (a, b) != foto:
            sd["muta"] += 1
            sd["malas"].append(f"muta el candidato en {info['ruta']}")
        if not (r.get("ok") is True or r.get("codigo") == "D-01"):
            sd["ok_mal"] += 1
            sd["malas"].append(f"ok={r.get('ok')!r} codigo={r.get('codigo')!r}")
            continue
        if r["ok"] is True:
            sd["n_ok"] += 1
            id_mut = objetivo.get("expediente_id") if isinstance(objetivo, dict) else None
            if not isinstance(id_mut, str):
                id_mut = None
            ids_ranking = {d2["expediente_id"] for g in r["grupos"].values() for d2 in g["ranking"]}
            excl = [(e2.get("expediente_id"), e2.get("motivo")) for e2 in r["excluidos"]]
            if not (id_mut in ids_ranking or any(eid == id_mut and mot in MOTIVOS_D for eid, mot in excl)):
                sd["fuera"] += 1
                sd["malas"].append(f"mutado ni está en ranking ni excluido con motivo conocido: {id_mut!r} {info['ruta']}")
            if _numeros_raros(r["grupos"]):
                sd["raros"] += 1
                sd["malas"].append("número no finito en el ranking")
        r_inv = comparar_candidatos([copy.deepcopy(b), copy.deepcopy(a)], AHORA)
        if r_inv != r:
            sd["orden"] += 1
            sd["malas"].append(f"el orden cambia el resultado en {info['ruta']}")
        r2 = comparar_candidatos([copy.deepcopy(a), copy.deepcopy(b)], AHORA)
        if r2 != r:
            sd["det"] += 1
            sd["malas"].append("no es determinista")
    h.chk("D_no_lanza_en_500_mutaciones", sd["lanz"] == 0, sd["malas"][:5])
    h.chk("D_ok_o_D01_en_500_mutaciones", sd["ok_mal"] == 0, sd["malas"][:5])
    h.chk("D_el_mutado_esta_en_ranking_o_en_excluidos_con_motivo_de_la_cabecera_en_500_casos",
          sd["fuera"] == 0 and sd["n_ok"] > 0, {"fuera": sd["fuera"], "ok": sd["n_ok"], "malas": sd["malas"][:5]})
    h.chk("D_ranking_sin_nan_ni_infinitos_en_500_mutaciones", sd["raros"] == 0, sd["malas"][:5])
    h.chk("D_el_orden_de_entrada_no_cambia_el_resultado_en_500_mutaciones", sd["orden"] == 0, sd["malas"][:5])
    h.chk("D_determinista_en_500_mutaciones", sd["det"] == 0, sd["malas"][:5])
    h.chk("D_no_muta_los_candidatos_en_500_mutaciones", sd["muta"] == 0, sd["malas"][:5])
    r02_mal = []
    for grafia_a, grafia_b in (("EURUSD", "EUR/USD"), ("EURUSD", "EUR-USD"), ("EURUSD", "ＥＵＲＵＳＤ")):
        rr02 = comparar_candidatos([copy.deepcopy(cand(1, instrumento=grafia_a)),
                                    copy.deepcopy(cand(2, instrumento=grafia_b, esperado=(3.0, 0.5, -4.0)))], AHORA)
        en_ranking = [d2["expediente_id"] for g in rr02.get("grupos", {}).values() for d2 in g["ranking"]]
        dups = [e2["expediente_id"] for e2 in rr02.get("excluidos", []) if e2.get("motivo") == "DUPLICADO"]
        if len(en_ranking) != 1 or len(dups) != 1:
            r02_mal.append(f"{grafia_a} vs {grafia_b}: ranking={en_ranking} duplicados={dups}")
        elif not all(d2["instrumento"] == "EURUSD" for g in rr02["grupos"].values() for d2 in g["ranking"]):
            r02_mal.append(f"{grafia_a} vs {grafia_b}: el ranking no muestra la forma canónica")
    h.chk("r02_la_dedup_de_instrumento_usa_la_identidad_de_SC1_norm", not r02_mal, r02_mal)

    def _sitio(eid, rr06):
        """'ranking', la lista de motivos de exclusión o 'D-01'."""
        if not rr06.get("ok"):
            return "D-01"
        if any(d2["expediente_id"] == eid for g in rr06["grupos"].values() for d2 in g["ranking"]):
            return "ranking"
        return [e2["motivo"] for e2 in rr06["excluidos"] if e2["expediente_id"] == eid]
    r06_mal = []
    c6 = cand(3)
    c6["sobre"]["payload"]["entrada_salida"]["entrada"]["ventana_hasta"] = "2026-11-06T08:00:00+00:00"
    r_t = comparar_candidatos([copy.deepcopy(cand(1)), copy.deepcopy(c6)], AHORA)
    if _sitio("EXP-0003", r_t) != ["CADUCADO"]:
        r06_mal.append(f"testigo: ventana cerrada con campo presente -> {_sitio('EXP-0003', r_t)}")
    del c6["sobre"]["payload"]["entrada_salida"]["entrada"]
    r_t = comparar_candidatos([copy.deepcopy(cand(1)), copy.deepcopy(c6)], AHORA)
    if _sitio("EXP-0003", r_t) == "ranking":
        r06_mal.append("sin 'entrada' se salta el control de ventana y se ordena")
    elif _sitio("EXP-0003", r_t) != ["FORMA"]:
        r06_mal.append(f"sin 'entrada' el motivo es {_sitio('EXP-0003', r_t)}")
    c7 = cand(4, esperado=(3.0, 0.5, -4.0))
    c7["sobre"]["resultado_politica"]["resultado"] = "RECHAZADO"
    r_t = comparar_candidatos([copy.deepcopy(cand(1)), copy.deepcopy(c7)], AHORA)
    if _sitio("EXP-0004", r_t) != ["EXCLUSION_DURA"]:
        r06_mal.append(f"testigo: sobre rechazado con campo presente -> {_sitio('EXP-0004', r_t)}")
    del c7["sobre"]["resultado_politica"]
    r_t = comparar_candidatos([copy.deepcopy(cand(1)), copy.deepcopy(c7)], AHORA)
    if _sitio("EXP-0004", r_t) == "ranking":
        r06_mal.append("sin 'resultado_politica' un sobre RECHAZADO se ordena")
    elif _sitio("EXP-0004", r_t) != ["FORMA"]:
        r06_mal.append(f"sin 'resultado_politica' el motivo es {_sitio('EXP-0004', r_t)}")
    h.chk("r06_d_falla_cerrado_sin_entrada_o_sin_resultado_politica", not r06_mal, r06_mal)

    # ---------------------------------------------------------------- CT-G-14: validar_manual (300 casos)
    ctx_rm = {"ahora": T1, "expediente": None, "posicion": None, "tolerancia_precio": 0.05}
    h.chk("RM_base_libre_valido", validar_manual(libre(), copy.deepcopy(ctx_rm)) == [],
          validar_manual(libre(), copy.deepcopy(ctx_rm)))
    srm = {"lanz": 0, "nolista": 0, "muta": 0, "det": 0, "forma": 0, "forma_mal": 0, "opc": 0, "opc_mal": 0,
           "emisor": 0, "identidad": 0, "malas": []}
    for _ in range(CASOS_RM):
        m, info = _mutar_en_sitio(libre(), rng)
        foto = copy.deepcopy(m)
        try:
            fallos = validar_manual(m, copy.deepcopy(ctx_rm))
        except Exception as ex:   # noqa: BLE001
            srm["lanz"] += 1
            srm["malas"].append(f"lanza {type(ex).__name__} en {info['ruta']}")
            continue
        if not isinstance(fallos, list):
            srm["nolista"] += 1
            continue
        if not _igual_nan(m, foto):
            srm["muta"] += 1
            srm["malas"].append(f"muta el registro en {info['ruta']}")
        if validar_manual(copy.deepcopy(m), copy.deepcopy(ctx_rm)) != fallos:
            srm["det"] += 1
            srm["malas"].append("no es determinista")
        reglas = {f2.get("regla") for f2 in fallos}
        if info["op"] == "borrar" and info["ruta"] == ("payload", "via_acceso"):
            srm["opc"] += 1
            if "RM-01" in reglas:
                srm["opc_mal"] += 1
        elif info["ruta"] == ("producer",):
            # el emisor tiene su regla propia (RM-02): cualquier productor que no sea el operador, sea del
            # tipo que sea, da RM-02; RM-01 solo si además rompe la envoltura
            srm["emisor"] += 1
            if not ({"RM-02", "RM-01"} & reglas):
                srm["forma_mal"] += 1
                srm["malas"].append(f"emisor sin RM-02 ni RM-01: {info['antes']!r} -> {info['despues']!r}")
        elif info["ruta"] in (("expediente_id",), ("correlation_id",)):
            # la identidad de la envoltura admite None (LIBRE) o un identificador válido: un valor bien
            # formado que no identifica el caso da RM-11 por diseño; mal formado, RM-01 (envoltura)
            srm["identidad"] += 1
            if not ({"RM-11", "RM-01"} & reglas):
                srm["forma_mal"] += 1
                srm["malas"].append(f"identidad sin RM-11 ni RM-01: {info['antes']!r} -> {info['despues']!r}")
        elif _es_forma(info):
            srm["forma"] += 1
            if "RM-01" not in reglas:
                srm["forma_mal"] += 1
                srm["malas"].append(f"forma sin RM-01: {info['op']} en {info['ruta']} -> {sorted(reglas)}")
    h.chk("RM_no_lanza_y_devuelve_lista_en_300_mutaciones", srm["lanz"] == 0 and srm["nolista"] == 0, srm["malas"][:5])
    h.chk("RM_no_muta_la_entrada_en_300_mutaciones", srm["muta"] == 0, srm["malas"][:5])
    h.chk("RM_determinista_en_300_mutaciones", srm["det"] == 0, srm["malas"][:5])
    h.chk(f"RM_toda_mutacion_de_forma_da_RM01_en_{srm['forma']}_casos", srm["forma"] > 0 and srm["forma_mal"] == 0,
          {"forma": srm["forma"], "malas": srm["malas"][:5]})
    h.chk("RM_borrar_via_acceso_de_un_LIBRE_sigue_valido_por_diseno", srm["opc_mal"] == 0, srm["malas"][:5])
    sin_via = libre()
    del sin_via["payload"]["via_acceso"]
    h.chk("RM_barrido_fijo_sin_via_acceso_en_LIBRE_es_valido", validar_manual(sin_via, copy.deepcopy(ctx_rm)) == [],
          validar_manual(sin_via, copy.deepcopy(ctx_rm)))
    h.chk("RM_fecha_bien_formada_incoherente_da_RM03_y_no_RM01",
          {f2["regla"] for f2 in validar_manual(libre(ejecutado_en=T2), copy.deepcopy(ctx_rm))} == {"RM-03"},
          validar_manual(libre(ejecutado_en=T2), copy.deepcopy(ctx_rm)))

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO ROBUSTEZ:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
