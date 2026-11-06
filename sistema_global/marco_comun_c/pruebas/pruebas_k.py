"""Pruebas de K: emisión del sello (Q-01..Q-13), validación del sello (S-01..S-11) y caducidad.
Datos SIMULADOS. Cada caso inválido rompe exactamente una regla.

Uso: python3 pruebas/pruebas_k.py     (escribe en pruebas/k/ y ejecuta)
"""
import copy
import json
import math
import sys
from datetime import date, timedelta
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
from k_calidad import construir_sello, validar_sello, estado_sello, hash_serie, hash_del_sello  # noqa: E402

CAL = {"version": "CAL-2026.1",
       "mercados": {"FX": {"anios": [2026, 2027], "festivos": ["2026-12-25", "2027-01-01"],
                           "hora_cierre_utc": "22:00"}}}   # T-26: el cierre diario de FX (17:00 de Nueva York)
CTX = {"ahora": "2026-11-06T08:00:00+00:00", "secuencia": 1}


def dias_habiles_entre(a, b):
    d, out = a, []
    while d <= b:
        if d.weekday() < 5:
            out.append(d)
        d += timedelta(days=1)
    return out


def serie(base, amp, desde, hasta, fase=0.0):
    out, prev = [], None
    for i, d in enumerate(dias_habiles_entre(desde, hasta)):
        c = round(base * (1 + amp * math.sin(i / 3 + fase)), 6)
        ap = prev if prev is not None else c
        out.append({"fecha": str(d), "apertura": ap, "maximo": round(max(ap, c) * 1.001, 6),
                    "minimo": round(min(ap, c) * 0.999, 6), "cierre": c, "volumen": 1000 + i})
        prev = c
    return out


def cruce(a, b):
    out = []
    for x, y in zip(a, b):
        r = {k: round(x[k] * y[k], 6) for k in ("apertura", "maximo", "minimo", "cierre")}
        r["fecha"] = x["fecha"]; r["volumen"] = x["volumen"]
        r["maximo"] = max(r["maximo"], r["apertura"], r["cierre"]); r["minimo"] = min(r["minimo"], r["apertura"], r["cierre"])
        out.append(r)
    return out


def PROC(fid, obtenido="2026-11-05T22:00:00+00:00", licencia="INTERMEDIARIO-USO-INTERNO"):
    """Procedencia simulada de una fuente (T-26): proveedor, licencia, cuándo se obtuvo y referencia."""
    return {"proveedor": "PROV-SIM", "licencia": licencia, "obtenido_en": obtenido, "referencia": f"conjunto simulado {fid}"}


def EVENTO(fecha, instrumentos, tipo="DATO_MACRO", descripcion="dato macro simulado", anunciado_en="2026-10-01T08:00:00+00:00"):
    return {"fecha": fecha, "tipo": tipo, "instrumentos": instrumentos, "descripcion": descripcion, "anunciado_en": anunciado_en}


def entrada_base(hasta=date(2026, 11, 5), solicitada="2026-11-05", cartera="TACTICA"):
    d0 = date(2026, 9, 24)
    eur = serie(1.10, 0.004, d0, hasta)
    usd = serie(150.0, 0.004, d0, hasta, 1.0)
    fu = lambda i, s, **k: {"fuente_id": i, "instrumento": i[4:], "version_conjunto": "DS-1", "serie": s, "procedencia": PROC(i, f"{hasta}T22:30:00+00:00"), **k}
    return {
        "mercado": "FX", "cartera": cartera, "fecha_corte_solicitada": solicitada,
        "fuentes": [
            fu("SRC-EURUSD", eur, critico=True, contraste=["SRC-EURUSD-B"]),
            fu("SRC-EURUSD-B", [dict(o, cierre=o["cierre"]) for o in eur]),
            fu("SRC-USDJPY", usd),
            fu("SRC-EURJPY", cruce(eur, usd)),
            fu("SRC-GBPUSD", serie(1.30, 0.004, d0, hasta, 2.0)),
        ],
        "cruces": [{"a": "SRC-EURUSD", "b": "SRC-USDJPY", "c": "SRC-EURJPY"}],
        "ajustes": {"version": "AJ-2026.1", "items": []},
        "eventos": [],
    }


def rehash(e):
    for fu in e["fuentes"]:
        if "serie" in fu:
            try:
                fu["hash_declarado"] = hash_serie(fu["serie"])
            except RecursionError:
                fu["hash_declarado"] = "0" * 64
    return e


def gbp(e):
    return next(f for f in e["fuentes"] if f["fuente_id"] == "SRC-GBPUSD")


def escalar_desde(s, k, factor):
    for o in s[k:]:
        for c in ("apertura", "maximo", "minimo", "cierre"):
            o[c] = round(o[c] * factor, 6)


def escala_todo(s, factor):
    escalar_desde(s, 0, factor)


def construir(mut=None, rh=True, ctx=None, cal=None, **kw):
    e = entrada_base(**kw)
    if mut:
        mut(e)
    if rh:
        rehash(e)
    return e, construir_sello(e, cal or CAL, ctx or CTX)


# ----------------------------------------------------------------- mutaciones
def m_fin_de_semana(e): pass


def m_salto(f):
    return lambda e: escalar_desde(gbp(e)["serie"], 15, f)


def m_salto_ajustado(e):
    s = gbp(e)["serie"]; escalar_desde(s, 15, 1.6)
    e["ajustes"]["items"].append({"fuente_id": "SRC-GBPUSD", "fecha_efectiva": s[15]["fecha"], "tipo": "SPLIT", "factor": 1.6})


def m_salto_evento(e):
    s = gbp(e)["serie"]; escalar_desde(s, 15, 1.25); gbp(e)["instrumento"] = "GBPUSD"
    e["eventos"].append(EVENTO(s[15]["fecha"], ["GBPUSD"], descripcion="dato de empleo simulado que explica el salto"))


def m_salto_ajuste_otro_dia(e):
    s = gbp(e)["serie"]; escalar_desde(s, 15, 1.7)
    e["ajustes"]["items"].append({"fuente_id": "SRC-GBPUSD", "fecha_efectiva": s[10]["fecha"], "tipo": "SPLIT", "factor": 1.7})


def m_quitar(n):
    def f(e):
        s = gbp(e)["serie"]
        for i in (5, 9, 13, 17)[:n]:
            s.pop(i - (5, 9, 13, 17).index(i))
    return f


def m_set(campo, valor, idx=10):
    def f(e): gbp(e)["serie"][idx][campo] = valor
    return f


def m_acumulado(e):
    s = gbp(e)["serie"]
    for k, f in ((15, 1.18), (16, 1.18), (17, 1.18)):
        escalar_desde(s, k, f)


def m_ajuste_en_hueco(e):
    s = gbp(e)["serie"]; falta = s[15]["fecha"]; s.pop(15); escalar_desde(s, 15, 1.6)
    e["ajustes"]["items"].append({"fuente_id": "SRC-GBPUSD", "fecha_efectiva": falta, "tipo": "SPLIT", "factor": 1.6})


def m_ajuste_factor_no_cuadra(e):
    s = gbp(e)["serie"]; escalar_desde(s, 15, 3.0)
    e["ajustes"]["items"].append({"fuente_id": "SRC-GBPUSD", "fecha_efectiva": s[15]["fecha"], "tipo": "DIVIDENDO", "factor": 1.0})


def m_ultimas(n):
    def f(e): gbp(e)["serie"][:] = gbp(e)["serie"][-n:]
    return f


def m_sabado(e):
    s = gbp(e)["serie"]; i = next(k for k, o in enumerate(s) if o["fecha"] == "2026-10-05")
    s.insert(i, {**s[i - 1], "fecha": "2026-10-03"})


def m_rango(e): gbp(e)["serie"][10]["maximo"] = 1e9


def m_sin_cruces(e): e["cruces"] = []


def m_cruces_ausentes(e): e.pop("cruces")


def m_corta(e):
    s = gbp(e)["serie"]
    while s[-1]["fecha"] > "2026-11-03":
        s.pop()


def m_todas_no_disponibles(e):
    for fu in e["fuentes"]:
        fu["disponible"] = False


def m_hash_malo(e): pass


def m_dup(e):
    s = gbp(e)["serie"]; s.insert(11, dict(s[10]))


def m_desorden(e):
    s = gbp(e)["serie"]; s[10], s[11] = s[11], s[10]


def m_barra(e):
    o = gbp(e)["serie"][10]; o["maximo"] = round(o["cierre"] * 0.99, 6)


def m_eurjpy(f):
    def g(e):
        escala_todo(next(x for x in e["fuentes"] if x["fuente_id"] == "SRC-EURJPY")["serie"], f)
    return g


def m_ajustes(v):
    def g(e): e["ajustes"] = v
    return g


def m_sin_ajustes(e): e.pop("ajustes")


def m_contraste(v):
    def g(e): e["fuentes"][0]["contraste"] = v
    return g


def m_contraste_no_disponible(e):
    e["fuentes"][0]["contraste"] = ["SRC-EURUSD-B"]; e["fuentes"][1]["disponible"] = False


def m_post(e):
    s = gbp(e)["serie"]; x = dict(s[-1]); x["fecha"] = "2026-11-06"; s.append(x)


def m_no_disp(e): e["fuentes"].append({"fuente_id": "SRC-CAIDA", "disponible": False})


def m_largo_plazo(e):
    for fu in e["fuentes"]:
        s = fu["serie"]
        while s[-1]["fecha"] > "2026-11-02":
            s.pop()


# ----------------------------------------------------------------- casos
VALIDOS = [
    ("valido_base", {}, {}, {}),
    ("valido_fin_de_semana", {"hasta": date(2026, 11, 6), "solicitada": "2026-11-07",
                              "ctx": {"ahora": "2026-11-07T08:00:00+00:00", "secuencia": 1}}, m_fin_de_semana, {"Q-01": "ADVERTENCIA"}),   # T-26: tras el cierre del viernes
    ("valido_fuente_no_disponible", {}, m_no_disp, {}),
    ("valido_salto_explicado_por_ajuste", {}, m_salto_ajustado, {}),
    ("valido_salto_moderado_con_evento_sigue_avisando", {}, m_salto_evento, {"Q-04": "ADVERTENCIA"}),
    ("valido_ajuste_en_dia_sin_observacion", {}, m_ajuste_en_hueco, {"Q-05": "ADVERTENCIA"}),
    ("valido_largo_plazo_con_3_dias_de_antiguedad", {"cartera": "LARGO_PLAZO"}, m_largo_plazo, {}),
]

# (nombre, kwargs, mutación, rehash, resultado esperado {regla: nivel})
INVALIDOS = [
    ("Q02_fuente_vieja", {}, m_corta, True, {"Q-02": "BLOQUEO"}),
    ("Q02_ninguna_fuente_disponible", {}, m_todas_no_disponibles, True, {"Q-02": "BLOQUEO"}),
    ("Q03_cierre_nulo", {}, m_set("cierre", None), True, {"Q-03": "BLOQUEO"}),
    ("Q03_precio_negativo", {}, m_set("apertura", -1.0), True, {"Q-03": "BLOQUEO"}),
    ("Q03_precio_texto", {}, m_set("minimo", "1.2"), True, {"Q-03": "BLOQUEO"}),
    ("Q03_precio_nan", {}, m_set("cierre", float("nan")), True, {"Q-03": "BLOQUEO"}),
    ("Q03_precio_booleano", {}, m_set("cierre", True), True, {"Q-03": "BLOQUEO"}),
    ("Q03_volumen_negativo", {}, m_set("volumen", -5), True, {"Q-03": "BLOQUEO"}),
    ("Q03_falta_campo", {}, lambda e: gbp(e)["serie"][10].pop("maximo"), True, {"Q-03": "BLOQUEO"}),
    ("Q04_salto_25", {}, m_salto(1.25), True, {"Q-04": "ADVERTENCIA"}),
    ("Q04_salto_70", {}, m_salto(1.7), True, {"Q-04": "BLOQUEO"}),
    ("Q04_ajuste_de_otro_dia", {}, m_salto_ajuste_otro_dia, True, {"Q-04": "BLOQUEO"}),
    ("Q04_ajuste_con_factor_que_no_cuadra", {}, m_ajuste_factor_no_cuadra, True, {"Q-04": "BLOQUEO"}),
    ("Q04_movimiento_acumulado_escalonado", {}, m_acumulado, True, {"Q-04": "BLOQUEO"}),
    ("Q05_historia_insuficiente", {}, m_ultimas(10), True, {"Q-05": "BLOQUEO"}),
    ("Q05_una_sola_observacion", {}, m_ultimas(1), True, {"Q-05": "BLOQUEO"}),
    ("Q06_observacion_en_sabado", {}, m_sabado, True, {"Q-06": "BLOQUEO"}),
    ("Q07_rango_intradia_absurdo", {}, m_rango, True, {"Q-07": "BLOQUEO"}),
    ("Q09_fx_sin_cruces", {}, m_sin_cruces, True, {"Q-09": "ADVERTENCIA"}),
    ("Q09_fx_cruces_ausentes", {}, m_cruces_ausentes, True, {"Q-09": "ADVERTENCIA"}),
    ("Q13_corte_en_el_futuro", {"hasta": date(2026, 11, 9), "solicitada": "2026-11-09"}, lambda e: None, True, {"Q-13": "BLOQUEO", "Q-14": "BLOQUEO"}),   # T-26: también obtenido en el futuro
    ("Q05_un_hueco", {}, m_quitar(1), True, {"Q-05": "ADVERTENCIA"}),
    ("Q05_cuatro_huecos", {}, m_quitar(4), True, {"Q-05": "BLOQUEO"}),
    ("Q06_fecha_duplicada", {}, m_dup, True, {"Q-06": "BLOQUEO"}),
    ("Q06_fuera_de_orden", {}, m_desorden, True, {"Q-06": "BLOQUEO"}),
    ("Q07_maximo_bajo_cierre", {}, m_barra, True, {"Q-07": "BLOQUEO"}),
    ("Q08_ajustes_sin_version", {}, m_ajustes({"items": []}), True, {"Q-08": "BLOQUEO"}),
    ("Q08_version_ajustes_con_espacio", {}, m_ajustes({"version": "AJ 1", "items": []}), True, {"Q-08": "BLOQUEO"}),
    ("Q08_sin_ajustes", {}, m_sin_ajustes, True, {"Q-08": "BLOQUEO"}),
    ("Q08_factor_cero", {}, m_ajustes({"version": "AJ-1", "items": [{"fuente_id": "SRC-GBPUSD", "fecha_efectiva": "2026-10-01", "tipo": "SPLIT", "factor": 0}]}), True, {"Q-08": "BLOQUEO"}),
    ("Q08_tipo_desconocido", {}, m_ajustes({"version": "AJ-1", "items": [{"fuente_id": "SRC-GBPUSD", "fecha_efectiva": "2026-10-01", "tipo": "OTRO", "factor": 2}]}), True, {"Q-08": "BLOQUEO"}),
    ("Q08_items_no_lista", {}, m_ajustes({"version": "AJ-1", "items": "x"}), True, {"Q-08": "BLOQUEO"}),
    ("Q09_cruce_0_2pct", {}, m_eurjpy(1.002), True, {"Q-09": "ADVERTENCIA"}),
    ("Q09_cruce_2pct", {}, m_eurjpy(1.02), True, {"Q-09": "BLOQUEO"}),
    ("Q10_sin_contraste", {}, m_contraste([]), True, {"Q-10": "ADVERTENCIA"}),
    ("Q10_contraste_es_ella_misma", {}, m_contraste(["SRC-EURUSD"]), True, {"Q-10": "ADVERTENCIA"}),
    ("Q10_contraste_no_disponible", {}, m_contraste_no_disponible, True, {"Q-10": "ADVERTENCIA"}),
    ("Q12_hash_distinto", {}, lambda e: e["fuentes"][2].update(hash_declarado="0" * 64), False, {"Q-12": "BLOQUEO"}),
    ("Q12_sin_hash", {}, lambda e: e["fuentes"][2].pop("hash_declarado", None), False, {"Q-12": "BLOQUEO"}),
    ("Q12_dato_cambiado_tras_hash", {}, lambda e: (rehash(e), gbp(e)["serie"][3].update(volumen=1)), False, {"Q-12": "BLOQUEO"}),
    ("Q13_dato_posterior_al_corte", {}, m_post, True, {"Q-13": "BLOQUEO", "Q-14": "BLOQUEO"}),   # T-26: y posterior a su obtención
]
# casos que cortan antes de evaluar el resto: (nombre, cal, mutación, regla)
CORTES = [
    ("Q11_calendario_sin_el_anio", {"version": "C", "mercados": {"FX": {"anios": [2025], "festivos": []}}}, None, "Q-11"),
    ("Q11_mercado_sin_calendario", {"version": "C", "mercados": {"BOLSA": {"anios": [2026], "festivos": []}}}, None, "Q-11"),
    ("Q11_serie_empieza_en_anio_no_cubierto", CAL, lambda e: gbp(e)["serie"].insert(0, {**gbp(e)["serie"][0], "fecha": "2025-12-30"}), "Q-11"),
    ("K00_cartera_desconocida", CAL, lambda e: e.update(cartera="OTRA"), "K-00"),
    ("K00_fecha_mal_formada", CAL, lambda e: e.update(fecha_corte_solicitada="05/11/2026"), "K-00"),
    ("K00_fecha_inexistente", CAL, lambda e: e.update(fecha_corte_solicitada="2026-02-30"), "K-00"),
    ("K00_fecha_formato_compacto", CAL, lambda e: e.update(fecha_corte_solicitada="20261105"), "K-00"),
    ("K00_sin_fuentes", CAL, lambda e: e.update(fuentes=[]), "K-00"),
    ("K00_fuente_id_repetido", CAL, lambda e: e["fuentes"][1].update(fuente_id="SRC-EURUSD"), "K-00"),
    ("K00_serie_vacia", CAL, lambda e: gbp(e).update(serie=[]), "K-00"),
    ("K00_fecha_de_observacion_mala", CAL, lambda e: gbp(e)["serie"][3].update(fecha="ayer"), "K-00"),
    ("K00_observacion_no_objeto", CAL, lambda e: gbp(e)["serie"].__setitem__(3, 7), "K-00"),
    ("K00_disponible_no_booleano", CAL, lambda e: gbp(e).update(disponible="no"), "K-00"),
    ("K00_evento_mal_formado", CAL, lambda e: e.update(eventos=[{"fecha": "2026-10-01"}]), "K-00"),
    ("K00_cruce_mal_formado", CAL, lambda e: e.update(cruces=[{"a": 1}]), "K-00"),
    ("K00_mercado_con_espacio", CAL, lambda e: e.update(mercado="F X"), "K-00"),
    ("K00_fuente_id_con_ancho_cero", CAL, lambda e: gbp(e).update(fuente_id="SRC-GBP\u200bUSD"), "K-00"),
    ("K00_fuente_id_enorme", CAL, lambda e: gbp(e).update(fuente_id="SRC-" + "X" * 5_000_000), "K-00"),
    ("K00_version_conjunto_con_espacio", CAL, lambda e: gbp(e).update(version_conjunto="DS 1"), "K-00"),
    ("K00_clave_de_fuente_desconocida", CAL, lambda e: gbp(e).update(extra=1), "K-00"),
    ("K00_clave_de_observacion_desconocida", CAL, lambda e: gbp(e)["serie"][3].update(extra=1), "K-00"),
    ("K00_nan_en_campo_extra", CAL, lambda e: gbp(e)["serie"][3].update(extra=float("nan")), "K-00"),
    ("K00_anidamiento_extremo_en_volumen", CAL, lambda e: gbp(e)["serie"][3].update(volumen=PROFUNDO), "K-00"),
    ("K00_critico_texto", CAL, lambda e: e["fuentes"][0].update(critico="true"), "K-00"),
    ("K00_contraste_no_lista", CAL, lambda e: e["fuentes"][0].update(contraste="SRC-EURUSD-B"), "K-00"),
    ("K00_cruces_no_lista", CAL, lambda e: e.update(cruces="x"), "K-00"),
    ("K00_calendario_sin_version", {"mercados": {}}, None, "K-00"),
]


PROFUNDO = []
for _ in range(100000):
    PROFUNDO = [PROFUNDO]


def nivel_no_ok(res):
    return {x["regla"]: x["resultado"] for x in res["resultados"] if x["resultado"] != "OK"}


def main():
    (AQUI / "k").mkdir(exist_ok=True)
    for v in (AQUI / "k").glob("*.json"):
        v.unlink()
    ok = True

    def informe(nombre, bien, detalle=""):
        nonlocal ok
        print(("OK   " if bien else "FALLA"), nombre, detalle)
        ok &= bien

    sellos = {}
    for nombre, kw, mut, esperado in VALIDOS:
        e, r = construir(mut, **kw)
        bien = r["sello"] is not None and nivel_no_ok(r) == esperado and not validar_sello(r["sello"], {"calendario": CAL})
        informe(nombre, bien, "" if bien else f"{nivel_no_ok(r)} {validar_sello(r['sello'], {'calendario': CAL}) if r['sello'] else ''}")
        if r["sello"]:
            sellos[nombre] = r["sello"]
            (AQUI / "k" / f"{nombre}.sello.json").write_text(json.dumps(r["sello"], ensure_ascii=False, indent=2), encoding="utf-8")
    for nombre, kw, mut, rh, esperado in INVALIDOS:
        e, r = construir(mut, rh=rh, **kw)
        glob = max(esperado.values(), key=lambda n: {"ADVERTENCIA": 1, "BLOQUEO": 2}[n])
        bien = nivel_no_ok(r) == esperado and r["resultado_global"] == glob and (r["sello"] is None) == (glob == "BLOQUEO")
        if r["sello"]:   # una advertencia sí emite sello, y debe ser válido
            bien &= not validar_sello(r["sello"], {"calendario": CAL})
        informe("inv_" + nombre, bien, "" if bien else f"obtenido={nivel_no_ok(r)} global={r['resultado_global']}")
        (AQUI / "k" / f"inv_{nombre}.json").write_text(json.dumps(e, ensure_ascii=False, indent=2, allow_nan=True), encoding="utf-8")
    for nombre, cal, mut, regla in CORTES:
        e, r = construir(mut, cal=cal)
        bien = r["sello"] is None and r["resultado_global"] == "BLOQUEO" and [x["regla"] for x in r["resultados"]] == [regla]
        informe("inv_" + nombre, bien, "" if bien else f"{r['resultados']}")
    # entradas que no son objetos: no lanzan excepciones
    for nombre, ent, ctx in (("K00_entrada_lista", [], CTX), ("K00_entrada_nula", None, CTX), ("K00_ctx_nulo", entrada_base(), None),
                             ("K00_ctx_sin_ahora", entrada_base(), {"secuencia": 1}),
                             ("K00_ahora_sin_zona", entrada_base(), {"ahora": "2026-11-06T08:00:00", "secuencia": 1}),
                             ("K00_secuencia_cero", entrada_base(), {"ahora": CTX["ahora"], "secuencia": 0}),
                             ("K00_secuencia_booleana", entrada_base(), {"ahora": CTX["ahora"], "secuencia": True}),
                             ("K00_reemplaza_a_malo", entrada_base(), {**CTX, "reemplaza_a": "x"}),
                             ("K00_ahora_sin_segundos", entrada_base(), {"ahora": "2026-11-06T08:00+00:00", "secuencia": 1}),
                             ("K00_ahora_con_espacio", entrada_base(), {"ahora": "2026-11-06 08:00:00+00:00", "secuencia": 1}),
                             ("K00_ahora_compacto", entrada_base(), {"ahora": "20261106T080000+00:00", "secuencia": 1}),
                             ("K00_reemplaza_a_si_mismo", entrada_base(), {**CTX, "reemplaza_a": "K-20261105-001"}),
                             ("K00_reemplaza_corte_posterior", entrada_base(), {**CTX, "reemplaza_a": "K-20991231-001"}),
                             ("K00_calendario_nulo", entrada_base(), CTX)):
        r = construir_sello(rehash(ent) if isinstance(ent, dict) else ent, None if nombre == "K00_calendario_nulo" else CAL, ctx)
        bien = r["sello"] is None and [x["regla"] for x in r["resultados"]] == ["K-00"]
        informe("inv_" + nombre, bien, "" if bien else f"{r['resultados']}")

    # ---- validación del sello
    base = sellos["valido_base"]; fds = sellos["valido_fin_de_semana"]

    def S(nombre, sello, esperada, ctx=None):
        esp = {esperada} if isinstance(esperada, str) else set(esperada)
        obt = {x["regla"] for x in validar_sello(sello, ctx if ctx is not None else {"calendario": CAL})}
        informe("sello_" + nombre, obt == esp, f"esperada={sorted(esp)} obtenida={sorted(obt)}")

    def cambia(s, fn, rehash_=True):
        s = copy.deepcopy(s); fn(s)
        if rehash_ and isinstance(s, dict) and "hash_sello" in s:
            s["hash_sello"] = hash_del_sello(s)
        return s

    S("S01_falta_campo", cambia(base, lambda s: s.pop("version_reglas")), "S-01")
    S("S01_campo_extra", cambia(base, lambda s: s.update(x=1)), "S-01")
    S("S01_id_mal_formado", cambia(base, lambda s: s.update(sello_id="K-SELLO-2026-11-05")), "S-01")
    S("S01_hash_no_hex", cambia(base, lambda s: s["fuentes"][0].update(hash="Z" * 64)), "S-01")
    S("S01_disponible_sin_hash", cambia(base, lambda s: s["fuentes"][0].pop("hash")), "S-01")
    S("S01_no_disponible_con_hash", cambia(base, lambda s: s["fuentes"].append({"fuente_id": "SRC-X", "estado": "NO_DISPONIBLE", "hash": "0" * 64})), "S-01")
    S("S01_no_es_objeto", [], "S-01")
    S("S01_nulo", None, "S-01")
    S("S01_ctx_calendario_malo", base, "S-01", {"calendario": {"x": 1}})
    S("S02_id_otra_fecha", cambia(base, lambda s: s.update(sello_id="K-20261104-001")), "S-02")
    S("S03_global_no_es_el_peor", cambia(fds, lambda s: s.update(resultado_global="OK")), "S-03")
    S("S03_bloqueo_en_sello_emitido", cambia(base, lambda s: (s["resultado_reglas"][4].update(resultado="BLOQUEO", detalle="x"), s.update(resultado_global="BLOQUEO"))), "S-03")
    S("S04_regla_repetida", cambia(base, lambda s: s["resultado_reglas"][12].update(regla="Q-01")), "S-04")
    S("S05_fuente_repetida", cambia(base, lambda s: s["fuentes"][1].update(fuente_id=s["fuentes"][0]["fuente_id"])), "S-05")
    S("S05_observacion_posterior", cambia(base, lambda s: s["fuentes"][0].update(ultima_observacion="2026-11-06")), ("S-05", "S-14"), {})   # y posterior a su obtención
    S("S05_antiguedad_sobre_tope", cambia(base, lambda s: s["fuentes"][0].update(antiguedad_dias_habiles=2)), "S-05", {})
    S("S05_ninguna_disponible", cambia(base, lambda s: s.update(fuentes=[{"fuente_id": "SRC-X", "estado": "NO_DISPONIBLE"}])), "S-05")
    S("S06_emitido_antes_del_corte", cambia(base, lambda s: s.update(emitido_en="2026-11-04T08:00:00+00:00")), ("S-06", "S-14"))   # y obtenido después
    S("S06_corte_posterior_a_lo_solicitado", cambia(base, lambda s: s.update(fecha_solicitada="2026-11-04")), {"S-06", "S-13"})
    S("S07_se_reemplaza_a_si_mismo", cambia(base, lambda s: s.update(reemplaza_a=s["sello_id"])), "S-07")
    S("S07_reemplaza_corte_posterior", cambia(base, lambda s: s.update(reemplaza_a="K-20261106-001")), "S-07")
    S("S08_anulado_cuando_se_exige_vigente", cambia(base, lambda s: s.update(estado="ANULADO")), "S-08", {"exigir_vigente": True})
    S("S09_advertencia_sin_detalle", cambia(fds, lambda s: s["resultado_reglas"][0].pop("detalle")), "S-09")
    S("S09_ok_con_detalle", cambia(base, lambda s: s["resultado_reglas"][0].update(detalle="x")), "S-09")
    S("S10_antiguedad_no_cuadra", cambia(base, lambda s: s["fuentes"][0].update(antiguedad_dias_habiles=1)), "S-10")
    S("S10_version_calendario_distinta", cambia(base, lambda s: s["mercados"][0].update(version_calendario="CAL-X")), "S-10")
    S("S10_corte_en_fin_de_semana", cambia(base, lambda s: (s.update(sello_id="K-20261107-001", fecha_corte="2026-11-07", fecha_solicitada="2026-11-07", emitido_en="2026-11-09T08:00:00+00:00"))), "S-10")
    S("S11_version_reglas", cambia(base, lambda s: s.update(version_reglas="Q-9.9")), "S-11")
    S("S11_version_esquema", cambia(base, lambda s: s.update(version_esquema="0.9.0")), "S-01")   # 0.2.0: la versión es constante en el esquema

    S("S06_emitido_antes_del_corte_en_UTC", cambia(base, lambda s: s.update(emitido_en="2026-11-05T00:00:00+14:00")), ("S-06", "S-14"))
    S("S05_mercado_repetido", cambia(base, lambda s: s["mercados"].append(dict(s["mercados"][0]))), "S-05")
    S("S12_contenido_alterado_sin_rehash", cambia(base, lambda s: s["fuentes"][0].update(version_conjunto="DS-9"), rehash_=False), "S-12")
    S("S12_resultado_reglas_alterado", cambia(base, lambda s: s.update(version_ajustes="AJ-9"), rehash_=False), "S-12")
    S("S12_estado_no_afecta_al_hash", cambia(base, lambda s: s.update(estado="CADUCADO"), rehash_=False), set())
    S("S13_corte_difiere_sin_aviso_Q01", cambia(base, lambda s: s.update(fecha_solicitada="2026-11-07")), "S-13")
    S("S13_aviso_Q01_sin_diferencia", cambia(fds, lambda s: s.update(fecha_solicitada=s["fecha_corte"])), "S-13")
    S("S01_hash_sello_ausente", cambia(base, lambda s: s.pop("hash_sello"), rehash_=False), "S-01")
    profundo = []
    for _ in range(100000):
        profundo = [profundo]
    S("S01_anidamiento_extremo_no_lanza", cambia(base, lambda s: s["fuentes"][0].update(hash=profundo), rehash_=False), "S-01")

    # ---- caducidad
    def E(nombre, sello, uso, cartera, esperado, cal=CAL):
        obt = estado_sello(sello, uso, cartera, cal)
        informe("estado_" + nombre, obt == esperado, f"esperado={esperado} obtenido={obt}")

    viernes = fds   # corte 2026-11-06 (viernes)
    E("viernes_sirve_el_lunes", viernes, "2026-11-09", "TACTICA", "VIGENTE")
    E("viernes_caduca_el_martes", viernes, "2026-11-10", "TACTICA", "CADUCADO")
    E("mismo_dia", viernes, "2026-11-06", "TRADING", "VIGENTE")
    E("largo_plazo_5_dias", viernes, "2026-11-13", "LARGO_PLAZO", "VIGENTE")
    E("largo_plazo_6_dias", viernes, "2026-11-16", "LARGO_PLAZO", "CADUCADO")
    E("uso_anterior_al_corte", viernes, "2026-11-05", "TACTICA", "CADUCADO")
    E("anulado", cambia(viernes, lambda s: s.update(estado="ANULADO")), "2026-11-06", "TACTICA", "ANULADO")
    E("cartera_desconocida", viernes, "2026-11-06", "OTRA", "CADUCADO")
    E("fecha_mala", viernes, "mañana", "TACTICA", "CADUCADO")
    E("calendario_sin_cobertura", viernes, "2028-01-03", "TACTICA", "CADUCADO")
    E("sello_roto", {}, "2026-11-06", "TACTICA", "CADUCADO")
    lp = sellos["valido_largo_plazo_con_3_dias_de_antiguedad"]
    E("emitido_para_largo_plazo_no_sirve_a_trading", lp, "2026-11-05", "TRADING", "CADUCADO")
    E("emitido_para_largo_plazo_sirve_a_largo_plazo", lp, "2026-11-05", "LARGO_PLAZO", "VIGENTE")
    E("antiguedad_de_fuente_manipulada", cambia(base, lambda s: s["fuentes"][0].update(antiguedad_dias_habiles=99)), "2026-11-05", "TACTICA", "CADUCADO")
    E("tactica_sirve_a_largo_plazo", base, "2026-11-06", "LARGO_PLAZO", "VIGENTE")
    E("festivo_no_cuenta", sellos["valido_base"], "2026-11-06", "TACTICA", "VIGENTE")

    print("\nRESULTADO K:", "TODAS LAS PRUEBAS PASAN" if ok else "HAY FALLOS")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
