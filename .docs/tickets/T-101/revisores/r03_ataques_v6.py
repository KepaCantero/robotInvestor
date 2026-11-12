"""QA r03 de T-101 · Ataques a las correcciones de la ronda r03 del diseño V6 del Bloque A (cliente simulado, coste cero).

Busca regresiones de las correcciones de H-12 a H-22: el filtro R13/R21 nuevo (falsos positivos en textos normales de un
informe de divisas, índices, materias primas, derivados y tipos; falsos negativos evidentes; los códigos permitidos del
universo), las filas de cobertura de los ciclos N1 y de las vigentes, el embudo con el GC1 del código y F5, el override de
la bolsa del ciclo, la validación de `senal_por_perfil` y el contrafactual NO_RESOLUBLE.

Uso (desde la raíz del repositorio; la raíz del código a atacar es opcional, por defecto el repositorio):
  .venv/bin/python -I .docs/tickets/T-101/revisores/r03_ataques_v6.py [<raiz_repo>] [-k <filtro>]

Cada ataque imprime OK, FALLO (contradice el ticket, el diseño, la documentación o una regla) u OBS (observación sin
veredicto). Sale con 1 si hay algún FALLO o ERROR. No escribe nada fuera de carpetas temporales.
"""
from __future__ import annotations

import copy
import json
import sys
import tempfile
import traceback
from pathlib import Path

ARGS = list(sys.argv[1:])
FILTRO = None
if "-k" in ARGS:
    i = ARGS.index("-k")
    FILTRO = ARGS[i + 1]
    del ARGS[i:i + 2]
RAIZ = Path(ARGS[0] if ARGS else ".").resolve()
EJEC = RAIZ / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJEC / "tests"))
sys.path.insert(0, str(EJEC))

import pandas as pd  # noqa: E402
from conftest import AS_OF, DATOS, config_pruebas  # noqa: E402

from bloque_a import diseno_v6 as v6  # noqa: E402
from bloque_a import mock_respuestas as mr  # noqa: E402
from bloque_a.configuracion import CLASES, RUTA_UNIVERSO_EJEMPLO, fusionar  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402

assert Path(v6.__file__).resolve().is_relative_to(EJEC.resolve()), v6.__file__
RES: list[tuple[str, str, str]] = []
UNIVERSO = cargar_universo(RUTA_UNIVERSO_EJEMPLO)


def informe(nombre, estado, detalle=""):
    RES.append((nombre, estado, detalle))
    print(f"[{estado:5}] {nombre}: {detalle}", flush=True)


def cfg(diseno="v6", perfiles=("DIV",), umbral=0.55, **extra):
    base = {"perfiles": {"activos": list(perfiles)}, "seleccion": {"umbral_senal_gc1": umbral}}
    return config_pruebas(diseno=diseno, **fusionar(base, extra))


def bloque(c, cliente=None, **kw):
    tmp = Path(tempfile.mkdtemp(prefix="r03_t101_"))
    return Bloque(c, ProveedorCSV(DATOS), UNIVERSO, cliente or MockClient(), tmp / "estado", tmp / "ent", **kw)


class Parche:
    """Sustituye funciones del simulador durante un ataque."""

    def __init__(self, **funcs):
        self.funcs, self.orig = funcs, {}

    def __enter__(self):
        for k, f in self.funcs.items():
            self.orig[k] = getattr(mr, k)
            setattr(mr, k, f(self.orig[k]))
        return self

    def __exit__(self, *a):
        for k, f in self.orig.items():
            setattr(mr, k, f)


def cobertura(b):
    return [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "COBERTURA"]


def entregadas(r):
    return {(c, o["opp_id"], o["indicador_seguimiento"]["simbolo"]) for c, d in r["paquete"]["clases"].items() for o in d["opciones"]}


def semana(k):
    return str((pd.Timestamp(AS_OF) + pd.Timedelta(days=7 * k)).date())


def permitidos_reales(perfiles=("DIV",)):
    return v6.permitidos_r21(bloque(cfg(perfiles=perfiles)))


# ================================================================================================ H-12: filtro R13/R21
# Frases que un informe del Bloque A escribe con normalidad (régimen, lectura del conjunto, factores, preguntas, textos llanos).
# Ninguna da una probabilidad numérica (R13) ni propone un valor, emisión, fondo, contrato o token concreto (R21).
LEGITIMOS = {
    "general (el término «opciones» del propio Bloque)": [
        "Las opciones de renta fija ganan un 3 % en el mes.",
        "Las tres opciones de RV acumulan un 4,2 % desde la última revisión.",
        "Las opciones del mismo clúster comparten una correlación de 0,8.",
        "Dos de las opciones vigentes caen más de un 5 % y siguen por encima de su invalidación.",
    ],
    "DER (opciones como derivado)": [
        "La venta de opciones de compra sobre el S&P 500 rinde un 1,5 % mensual.",
        "Las opciones sobre el VIX cotizan con una prima del 12 % sobre la media.",
        "Vender volatilidad con opciones de venta cubiertas rinde un 0,9 % al mes.",
    ],
    "IDX y macro (porcentajes que no son probabilidades)": [
        "La probabilidad de un recorte de la Fed hasta el 4,25 % ha subido.",
        "El mercado descuenta con alta probabilidad que el BCE deje el depósito en el 2 %.",
        "Conviene vender MSCI World frente a emergentes según el régimen.",
        "El índice ISM manufacturero sube; se compra DXY en la sesión.",
    ],
    "DIV (pares sin la barra)": [
        "El Analista no ve motivos para vender EURUSD tras el dato de empleo.",
        "Los fondos tienden a comprar GBPUSD cuando sube el diferencial de tipos.",
        "El mercado vende JPY y compra MXN por el carry.",
    ],
    "MP (referencias de materias primas)": [
        "Los operadores vuelven a la compra de WTI tras el recorte de la OPEP.",
        "Los bancos centrales siguen comprando oro; la venta de GNL a Europa crece.",
        "Los inversores venden BRENT y compran oro.",
    ],
    "TCV (símbolos del propio universo)": [
        "El diferencial BAMLH0A0HYM2 se estrecha 20 pb en el mes.",
        "La pendiente CURVA-USD-2S10S-TR vuelve a positivo.",
    ],
}
# Casos evidentes con patrón (el README promete: «un ticker fuera de filtro_r21_codigos y del universo»). El nombre propio
# suelto («entrar en Tesla») es límite declarado y no se incluye.
PROHIBIDOS = [
    ("R21", "Recomendamos invertir en NVDA este trimestre."),
    ("R21", "Conviene vender las acciones de TSLA."),
    ("R21", "Comprar el ETF QQQ es la mejor forma de exponerse."),
    ("R21", "Comprar ETF ARKK para la innovación."),
    ("R21", "Tomar posiciones en MSFT y GOOGL."),
    ("R21", "Vender un poco de META y comprar algo de NFLX."),
    ("R21", "Abrir largos en AMZN ya."),
    ("R21", "Conviene comprar GLD como cobertura."),        # GLD es un fondo concreto, aunque sea el proxy del universo
    ("R21", "Sobreponderar XLK frente al índice."),         # ídem, XLK
    ("R13", "Probabilidad de subida: 87 %."),
    ("R13", "Es probable al 80 % que el euro baje."),
    ("R13", "Vemos un 87 % de confianza en la subida."),
]


def at_filtro_falsos_positivos():
    """Con los códigos permitidos reales (configuración y universo), frases normales de cada perfil no deben descartarse."""
    perm = permitidos_reales(tuple(CLASES))
    malos, total = [], 0
    for grupo, textos in LEGITIMOS.items():
        for t in textos:
            total += 1
            r = v6.texto_prohibido(t, perm)
            if r:
                malos.append((grupo, r, t))
    informe("filtro_falsos_positivos", "FALLO" if malos else "OK", f"{len(malos)}/{total} textos legítimos descartados: "
            + "; ".join(f"[{g}] {r}: «{t}»" for g, r, t in malos))


def at_filtro_falsos_negativos():
    """Casos evidentes con patrón (ticker en mayúsculas con un verbo de inversión, o probabilidad con dos puntos)."""
    perm = permitidos_reales(tuple(CLASES))
    pasan = [(r, t) for r, t in PROHIBIDOS if v6.texto_prohibido(t, perm) is None]
    informe("filtro_falsos_negativos", "FALLO" if pasan else "OK",
            f"{len(pasan)}/{len(PROHIBIDOS)} textos prohibidos que pasan: " + "; ".join(f"{r}: «{t}»" for r, t in pasan))


def at_filtro_solo_primera_palabra():
    """El código tras el verbo solo se mira en la primera palabra: con un artículo delante, el ticker no se ve."""
    perm = permitidos_reales()
    pares = [("Comprar AAPL.", "Comprar las AAPL."), ("Vender TSLA.", "Vender ya TSLA."), ("Comprar QQQ.", "Comprar el QQQ.")]
    res = [(a, v6.texto_prohibido(a, perm), b, v6.texto_prohibido(b, perm)) for a, b in pares]
    roto = [x for x in res if x[1] and not x[3]]
    informe("filtro_solo_primera_palabra", "FALLO" if roto else "OK",
            "; ".join(f"«{a}»→{ra} / «{b}»→{rb}" for a, ra, b, rb in res))


def at_filtro_universo_permite_comprar_fondos():
    """Los símbolos del universo (fondos y tokens concretos: GLD, XLK, SPY, ETH-USD…) valen junto a «comprar»."""
    perm = permitidos_reales(tuple(CLASES))
    casos = ["Comprar SPY.", "Comprar GLD.", "Sobreponderar XLK.", "Vender TLT.", "Comprar BTC-USD.", "Comprar ETH-USD."]
    res = {t: v6.texto_prohibido(t, perm) for t in casos}
    informe("filtro_universo_permite_comprar_fondos", "OBS", f"{res} (BTC-USD sí se caza porque el código se corta en «BTC»)")


def _paquete_con_sintetizador(perfiles, cambiar):
    """Un ciclo V6 en el que el Sintetizador simulado escribe los textos que da `cambiar(out)`."""
    def f(orig):
        def g(msg, ctx, rng):
            out = orig(msg, ctx, rng)
            cambiar(out)
            return out
        return g
    b = bloque(cfg(perfiles=perfiles))
    with Parche(_sintetizador=f):
        r = b.ciclo(AS_OF)
    return b, r


def at_sintetizador_lectura_con_opciones_y_porcentaje():
    """Frase corriente de la lectura del conjunto: «Las opciones de DIV ganan un 1,2 % en el mes». ¿Llega al paquete?"""
    t = "Las opciones de DIV ganan un 1,2 % en el mes y comparten el factor dólar."

    def cambiar(out):
        out["lectura_conjunto"] = t
    b, r = _paquete_con_sintetizador(("DIV",), cambiar)
    p = r["paquete"]
    llega = p.get("x_lectura_conjunto") == t
    decl = [x for x in p["limitaciones"] if "descartados por R13" in x]
    informe("sintetizador_lectura_opciones_porcentaje", "OK" if llega else "FALLO",
            f"llega al paquete={llega}; limitación={decl[:1]}")


def at_sintetizador_una_tarjeta_tira_todos_los_llanos():
    """Una sola tarjeta llana con «las opciones … %» hace que se usen los textos por defecto en todas las demás."""
    def cambiar(out):
        if out.get("tarjetas"):
            out["tarjetas"][0]["por_que_llano"] = "Las opciones de este tipo subieron un 2 % el último mes."
    b, r = _paquete_con_sintetizador(("DIV",), cambiar)
    lim = [x for x in r["paquete"]["limitaciones"] if x.startswith("Textos llanos del Sintetizador descartados")]
    informe("sintetizador_tarjeta_tira_llanos", "FALLO" if lim else "OK", f"limitación={lim[:1]}")


def at_sintetizador_falso_negativo_en_el_paquete():
    """«Conviene vender las acciones de TSLA y comprar el ETF QQQ» en la lectura: ¿llega al paquete con la 2.ª pasada APTO?"""
    t = "Conviene vender las acciones de TSLA y comprar el ETF QQQ esta semana."

    def cambiar(out):
        out["lectura_conjunto"] = t
    b, r = _paquete_con_sintetizador(("DIV",), cambiar)
    llega = r["paquete"].get("x_lectura_conjunto") == t
    entreg = r.get("entregables") or {}
    md = Path(entreg["informe_tecnico"]).read_text(encoding="utf-8") if entreg.get("informe_tecnico") else ""
    informe("sintetizador_falso_negativo", "FALLO" if llega else "OK",
            f"llega al paquete={llega}; en el informe técnico={'TSLA' in md}; estado={r['estado']}")


# ======================================================================================= H-13, H-14 y H-15: cobertura
def at_cobertura_vigente_arrastrada_fuera_del_top():
    """N2 en el que el Analista no vuelve a proponer ninguna vigente y propone tres ámbitos nuevos más fuertes: la vigente
    arrastrada que sale del top-3 sin cerrarse, ¿tiene fila?"""
    b = bloque(cfg())
    r1 = b.ciclo(AS_OF)
    vig = {x[2] for x in entregadas(r1)}

    def f(orig):
        def g(msg, ctx, rng, inyectado):
            out = orig(msg, ctx, rng, inyectado)
            if msg.get("fase") == "CRIBADO_E_INVESTIGACION" and out.get("finalistas"):
                base = max(out["finalistas"], key=lambda x: x["indicador_seguimiento"]["simbolo"] in vig)
                nuevos = [u["simbolo"] for u in msg["universo"] if u["simbolo"] not in vig]
                fins = []
                for s in nuevos:
                    x = copy.deepcopy(base)
                    x["indicador_seguimiento"] = {**x["indicador_seguimiento"], "simbolo": s}
                    x["nombre"] = f"Ámbito {s}"
                    x["dimensiones"] = {d: {k: 100 for k in v} for d, v in x["dimensiones"].items()}   # más fuertes que las vigentes
                    fins.append(x)
                out["finalistas"] = fins
            return out
        return g
    with Parche(_analista=f):
        r2 = b.ciclo(semana(1), nivel_forzado="N2")
    cob = cobertura(b)[-1]["clases"]["DIV"]
    top2 = {x[2] for x in entregadas(r2)}
    fuera = sorted(vig - top2)
    con_fila = {x.get("simbolo") for x in cob["filas"]}
    cerradas = [x for x in cob["filas"] if x["fase"] == "CIERRE"]
    sin_fila = [s for s in fuera if s not in con_fila]
    estado = "FALLO" if sin_fila and len(cerradas) < len(fuera) else ("OK" if fuera else "OBS")
    informe("cobertura_vigente_fuera_del_top", estado,
            f"vigentes={sorted(vig)}; top-3 del ciclo 2={sorted(top2)}; vigentes fuera del top-3={fuera}; sin fila (ni símbolo ni "
            f"CIERRE)={sin_fila}; filas CIERRE={[(x['opp_id'], x['motivo'][:40]) for x in cerradas]}")


def at_cobertura_n1_exploratoria_fuera_de_la_rotacion():
    """N1: el Analista propone una exploratoria de un ámbito del tipo que no estaba en la rotación (no se le envió). ¿Se da
    de alta en F3 sin fila en la cobertura?"""
    b = bloque(cfg())
    b.ciclo(AS_OF)
    div = list(UNIVERSO.loc[UNIVERSO["clase"] == "DIV", "simbolo"])
    est = {}

    def f(orig):
        def g(msg, ctx, rng, inyectado):
            out = orig(msg, ctx, rng, inyectado)
            if msg.get("fase") == "REVISION_VIGENTES":
                enviados = {u["simbolo"] for u in msg["universo"]}
                fuera = [s for s in div if s not in enviados]
                if fuera:
                    u = {"simbolo": fuera[0], "tipo_opcion": "PAR", "nombre": fuera[0], "senales": {"senal_compuesta": 0.9}}
                    plantilla = copy.deepcopy(msg["universo"][0]) if msg["universo"] else u
                    plantilla.update({"simbolo": fuera[0]})
                    out["exploratorias"] = [mr._ficha(plantilla, msg, ctx, rng, inyectado)]
                    est["sym"] = fuera[0]
                    est["rot"] = msg.get("rotacion_exploratoria")
            return out
        return g
    with Parche(_analista=f):
        b.ciclo(semana(1), nivel_forzado="N1")
    sym = est.get("sym")
    f3 = [e for e in b.almacen.leer("F3") if (e.get("indicador_seguimiento") or {}).get("simbolo") == sym]
    cob = cobertura(b)[-1]["clases"]["DIV"]
    filas = [x for x in cob["filas"] if x.get("simbolo") == sym]
    alta = bool(f3)
    informe("cobertura_n1_exploratoria_fuera_rotacion", "FALLO" if alta and not filas else "OK",
            f"rotación={est.get('rot')}; exploratoria no enviada={sym}; alta en F3={alta} "
            f"({[(e.get('opp_id'), e.get('estado')) for e in f3][:2]}); filas en la cobertura={[x['fase'] for x in filas]}")


def at_cobertura_banco_sin_duplicados_ni_top_en_muestra():
    """Dos ciclos con cinco perfiles (N2 y N1): ningún símbolo con dos filas, la muestra sin nada del top-3 ni de F3, y las
    elegidas con símbolo y precio."""
    b = bloque(cfg(perfiles=("DIV", "RV", "MP", "IDX", "TCV")))
    rs = [b.ciclo(AS_OF), b.ciclo(semana(1)), b.ciclo(semana(2), nivel_forzado="N2")]
    malos = []
    for k, (r, e) in enumerate(zip(rs, cobertura(b))):
        top = {(x[0], x[2]) for x in entregadas(r)}
        for c, d in e["clases"].items():
            sims = [x.get("simbolo") for x in d["filas"] if x.get("simbolo")]
            dup = sorted({s for s in sims if sims.count(s) > 1})
            en_muestra_top = [x["simbolo"] for x in d["muestra_descartes"] if (c, x["simbolo"]) in top]
            sin_sim = [x for x in d["elegidas"] if not x.get("simbolo") or x.get("precio") is None]
            if dup or en_muestra_top or sin_sim:
                malos.append((k, c, dup, en_muestra_top, len(sin_sim)))
    informe("cobertura_sin_duplicados", "FALLO" if malos else "OK",
            f"niveles={[r['paquete'].get('tipo_run') or '' for r in rs]}; problemas (ciclo, tipo, duplicados, top en muestra, "
            f"elegidas sin símbolo o precio)={malos or 'ninguno'}")


# ==================================================================================================== H-16: embudo y F5
def at_embudo_monotono():
    """Con GC1 por código, el embudo del paquete debería ser no creciente: cribadas ≥ pasan_gc1 ≥ pasan_gc2 ≥ finalistas."""
    b = bloque(cfg(perfiles=("RV", "RF", "DIV", "MP", "IDX", "CRI", "TCV"), umbral=0.75))
    r = b.ciclo(AS_OF)
    raros = {c: d["embudo"] for c, d in r["paquete"]["clases"].items()
             if not (d["embudo"]["cribadas"] >= d["embudo"]["pasan_gc1"] >= d["embudo"]["pasan_gc2"] >= d["embudo"]["finalistas_gc3"])}
    f5 = b.almacen.leer("F5")[-1]
    gc1_no = {(x["clase"], x["objeto"]) for x in f5.get("decisiones_puertas", []) if x["puerta"] == "GC1" and not x["resultado"]}
    gc2_si = {(x["clase"], x["objeto"]) for x in f5.get("decisiones_puertas", []) if x["puerta"] == "GC2" and x["resultado"]}
    contradic = sorted(gc1_no & gc2_si)
    informe("embudo_monotono", "OBS" if raros or contradic else "OK",
            f"embudos con más ámbitos en GC2 que en GC1: {raros}; F5 con GC1 no superada y GC2 superada: {contradic[:6]}")


# ================================================================================================ H-18: override de la bolsa
def at_override_bolsa_total():
    """Con un override de V6_GLOBAL, la parte de prospectiva y refutación de cada tipo se queda en el tipo: ¿el total cambia?"""
    from bloque_a import orquestacion as orq
    capt = []
    P = orq.Presupuesto

    class Espia(P):
        def __init__(self, asign, cfg_):
            capt.append(dict(asign))
            super().__init__(asign, cfg_)
    orq.Presupuesto = Espia
    try:
        res = {}
        for nombre, ov in (("sin override", None), ("V6_GLOBAL=10", {v6.BOLSA_GLOBAL: 10.0}), ("V6_GLOBAL=-5", {v6.BOLSA_GLOBAL: -5.0}),
                           ("V6_GLOBAL=nan", {v6.BOLSA_GLOBAL: float("nan")})):
            capt.clear()
            b = bloque(cfg(perfiles=("DIV", "RV")))
            try:
                r = b.ciclo(AS_OF, presupuesto_override=ov)
                a = capt[-1]
                res[nombre] = (round(sum(v for v in a.values() if v == v), 4), a.get("DIV"), a.get(v6.BOLSA_GLOBAL), r["estado"])
            except Exception as e:   # noqa: BLE001
                res[nombre] = (type(e).__name__, str(e)[:80])
    finally:
        orq.Presupuesto = P
    informe("override_bolsa_total", "OBS", f"(Σ asignado, DIV, bolsa, estado): {res}")


# ============================================================================================ H-19: senal_por_perfil
def at_senal_por_perfil_escala():
    """El catálogo admite cualquier señal del Motor, pero el umbral de GC1 es común (0,75 por defecto) y pensado para la señal
    compuesta en [0, 1]. Con una señal de otra escala o de signo contrario, ¿qué pasa sin aviso?"""
    out = {}
    for sen in ("senal_compuesta", "vol_20d", "mdd", "familias_concordantes", "riesgo_1a5", "rent_1m"):
        b = bloque(cfg(umbral=0.75, v6={"gc1": {"senal_por_perfil": {"DIV": sen}}}))
        r = b.ciclo(AS_OF)
        g = cobertura(b)[-1]["clases"]["DIV"]["gc1"]
        out[sen] = (len(g["pasan"]), len(g["exploracion"]), len(g["sin_senal_medible"]), r["estado"])
    informe("senal_por_perfil_escala", "OBS", f"(pasan, exploración, sin señal, estado) por señal: {out}")


def at_senales_gc1_existen():
    """Cada señal de SENALES_GC1 debe existir en las señales que el Motor calcula para algún ámbito (si no, H-19 vuelve)."""
    vistas = set()

    def f(orig):
        def g(msg, ctx, rng, inyectado):
            for u in msg.get("universo", []):
                vistas.update(k for k, v in (u.get("senales") or {}).items() if isinstance(v, (int, float)) and not isinstance(v, bool))
            return orig(msg, ctx, rng, inyectado)
        return g
    with Parche(_analista=f):
        bloque(cfg(perfiles=tuple(CLASES), v6={"gc1": {"por_codigo": False}})).ciclo(AS_OF)
    faltan = [k for k in v6.SENALES_GC1 if k not in vistas]
    informe("senales_gc1_existen", "FALLO" if faltan else "OK",
            f"señales de SENALES_GC1 que no trae ningún ámbito del universo: {faltan or 'ninguna'}; numéricas vistas que no están en "
            f"SENALES_GC1: {sorted(vistas - set(v6.SENALES_GC1))}")


# ================================================================================================= H-20: contrafactual
def _cob_y_vence(perfiles=("DIV",)):
    b = bloque(cfg(perfiles=perfiles))
    b.ciclo(AS_OF)
    cob = cobertura(b)[0]
    return b, cob, v6._fecha_vencimiento(b, cob["fecha"], cob["horizonte_contrafactual"])


def at_contrafactual_borde_espera():
    """Sin precios al vencer: el día vence + dias_max_espera_precio todavía espera; el siguiente, NO_RESOLUBLE (una vez)."""
    b, cob, vence = _cob_y_vence()
    n = int(v6.op(b, "cobertura.dias_max_espera_precio"))
    orig = v6._precio
    v6._precio = lambda bl, sim, fecha: None if pd.Timestamp(fecha) == vence else orig(bl, sim, fecha)
    try:
        res = []
        for d in (0, n, n + 1, n + 2):
            dia = vence + pd.Timedelta(days=d)
            b.fijar_fecha(dia)
            r = v6.resolver_contrafactual(b, dia, f"RUN-B{d}")
            res.append((d, [x["estado"] for x in r]))
    finally:
        v6._precio = orig
    ok = res[0][1] == [] and res[1][1] == [] and res[2][1] == ["NO_RESOLUBLE"] and res[3][1] == []
    informe("contrafactual_borde_espera", "OK" if ok else "FALLO", f"(días tras vencer, estados): {res}")


def at_contrafactual_sin_precio_en_la_muestra():
    """Si la muestra se tomó sin precio en la fecha de corte (`precio: null`), no hay nada medible: ¿se da por RESUELTO?"""
    b, cob, vence = _cob_y_vence()
    orig = v6._precio
    v6._precio = lambda bl, sim, fecha: None if pd.Timestamp(fecha) == pd.Timestamp(AS_OF) else orig(bl, sim, fecha)
    try:
        b2 = bloque(cfg())
        b2.ciclo(AS_OF)
    finally:
        v6._precio = orig
    c2 = cobertura(b2)[0]["clases"]["DIV"]
    b2.fijar_fecha(vence)
    r = v6.resolver_contrafactual(b2, vence, "RUN-Z")
    est = [(x["estado"], x["clases"]["DIV"]) for x in r]
    malo = bool(r) and r[0]["estado"] == "RESUELTO" and r[0]["clases"]["DIV"]["descartes"] + r[0]["clases"]["DIV"]["elegidas"] == 0
    informe("contrafactual_muestra_sin_precio", "FALLO" if malo else "OK",
            f"muestra={len(c2['muestra_descartes'])} y elegidas={len(c2['elegidas'])}, todas con precio nulo; resultado={est}")


def at_contrafactual_espera_cero():
    """`dias_max_espera_precio: 0`: sin precios, el día del vencimiento espera y el siguiente cierra."""
    b = bloque(cfg(v6={"cobertura": {"dias_max_espera_precio": 0}}))
    b.ciclo(AS_OF)
    cob = cobertura(b)[0]
    vence = v6._fecha_vencimiento(b, cob["fecha"], cob["horizonte_contrafactual"])
    orig = v6._precio
    v6._precio = lambda bl, sim, fecha: None if pd.Timestamp(fecha) == vence else orig(bl, sim, fecha)
    try:
        res = []
        for d in (0, 1):
            dia = vence + pd.Timedelta(days=d)
            b.fijar_fecha(dia)
            res.append([x["estado"] for x in v6.resolver_contrafactual(b, dia, f"RUN-C{d}")])
    finally:
        v6._precio = orig
    informe("contrafactual_espera_cero", "OK" if res == [[], ["NO_RESOLUBLE"]] else "FALLO", f"{res}")


def at_contrafactual_validacion_espera():
    """`dias_max_espera_precio` negativo, decimal o texto se rechaza al crear el Bloque."""
    res = {}
    for v in (-1, 1.5, "30", None, True):
        try:
            bloque(cfg(v6={"cobertura": {"dias_max_espera_precio": v}}))
            res[repr(v)] = "ACEPTADA"
        except Exception as e:   # noqa: BLE001
            res[repr(v)] = type(e).__name__
    malos = [k for k, x in res.items() if x == "ACEPTADA"]
    informe("contrafactual_validacion_espera", "FALLO" if malos else "OK", f"{res}")


# ============================================================================================================ ejecución
ATAQUES = [v for k, v in sorted(globals().items()) if k.startswith("at_") and callable(v)]
if __name__ == "__main__":
    for f in ATAQUES:
        if FILTRO and FILTRO not in f.__name__:
            continue
        try:
            f()
        except Exception as e:   # noqa: BLE001
            informe(f.__name__, "ERROR", f"{type(e).__name__}: {e} · {traceback.format_exc()[-600:]}")
    cuenta = {k: sum(1 for x in RES if x[1] == k) for k in ("OK", "FALLO", "OBS", "ERROR")}
    print(f"\nResumen: {cuenta}")
    sys.exit(1 if cuenta["FALLO"] or cuenta["ERROR"] else 0)
