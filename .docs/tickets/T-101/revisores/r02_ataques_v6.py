"""QA r02 de T-101 · Ataques a las correcciones de la ronda r02 del diseño V6 del Bloque A (cliente simulado, coste cero).

Busca regresiones de las correcciones de H-01 a H-11: el filtro R13/R21 de los textos del Sintetizador, el estado PARCIAL
nuevo, la validación de la sección `v6`, el reintento con `reintento_de_cobertura`, las filas nuevas de cobertura, el
contrafactual aplazado, la nota de GC1 y el presupuesto con override.

Uso (desde la raíz del repositorio; la raíz del código a atacar es opcional, por defecto el repositorio):
  .venv/bin/python -I .docs/tickets/T-101/revisores/r02_ataques_v6.py [<raiz_repo>] [-k <filtro>]

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
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, fusionar, parametro  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402

assert Path(v6.__file__).resolve().is_relative_to(EJEC.resolve()), v6.__file__
RES: list[tuple[str, str, str]] = []
UNIVERSO = cargar_universo(RUTA_UNIVERSO_EJEMPLO)


def informe(nombre, estado, detalle=""):
    RES.append((nombre, estado, detalle))
    print(f"[{estado:5}] {nombre}: {detalle}", flush=True)


def cfg(diseno="v6", perfiles=("DIV",), **extra):
    base = {"perfiles": {"activos": list(perfiles)}, "seleccion": {"umbral_senal_gc1": 0.55}}
    return config_pruebas(diseno=diseno, **fusionar(base, extra))


def bloque(c, cliente=None, **kw):
    tmp = Path(tempfile.mkdtemp(prefix="r02_t101_"))
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


def espiar_mensajes(b, contratos=("CT-06", "CT-12", "CT-13")):
    cuerpos = {c: [] for c in contratos}
    crear = b.mensajeria.crear

    def _crear(contrato, emisor, receptor, cuerpo, **k):
        if contrato in cuerpos:
            cuerpos[contrato].append(json.loads(json.dumps(cuerpo, default=str)))
        return crear(contrato, emisor, receptor, cuerpo, **k)
    b.mensajeria.crear = _crear
    return cuerpos


def entregadas(r):
    return {(c, o["opp_id"], o["indicador_seguimiento"]["simbolo"]) for c, d in r["paquete"]["clases"].items() for o in d["opciones"]}


def semana(k):
    return str((pd.Timestamp(AS_OF) + pd.Timedelta(days=7 * k)).date())


# ======================================================================================================== H-09: filtro R13/R21
LEGITIMOS = [   # textos que el Sintetizador puede escribir sin incumplir R13 ni R21 (R21: el Bloque A trabaja por segmentos)
    "Un 5 % del capital ya está en opciones del mismo clúster.",
    "La probabilidad es baja; aun así, un 5 % del capital comparte el factor de riesgo.",
    "Los pronósticos con probabilidad alta acertaron el 62 % de las veces en el historial.",
    "¿Conviene vender USD frente al EUR si el diferencial de tipos se estrecha?",
    "El Analista prefiere no comprar RF larga mientras suba la inflación.",
    "Con el dólar fuerte, puede tener sentido vender EM y esperar.",
    "El ETF de referencia (SPY) sigue al índice; no es una recomendación.",
    "El índice VIX sube; el riesgo de cola de RV aumenta.",
    "Si la curva se empina, el segmento de vender HY pierde atractivo.",
]
PROHIBIDOS = [   # probabilidades numéricas sin certificar (R13) o compra de un instrumento concreto (R21)
    ("R13", "Probabilidad del 87 % de que el dólar suba este trimestre."),
    ("R13", "Hay un 70 % de probabilidad de subida."),
    ("R13", "La probabilidad de subida es de 0,87."),
    ("R13", "Vemos un 87 por ciento de probabilidades de subida."),
    ("R13", "Un 80 % de posibilidades de que el euro baje."),
    ("R13", "El escenario base tiene un 65 % de opciones de cumplirse."),
    ("R21", "Conviene comprar AAPL cuanto antes."),
    ("R21", "Compra acciones de Apple (AAPL)."),               # el ejemplo de la QA r01 (H-09)
    ("R21", "compra acciones de Apple (AAPL) esta semana."),
    ("R21", "Comprar AAPL es la mejor idea."),
    ("R21", "Recomendamos la compra de AAPL y de MSFT."),
    ("R21", "Conviene entrar en Tesla antes de resultados."),
    ("R21", "Sobreponderar Microsoft Corp frente al índice."),
    ("R21", "Comprar el bono del Tesoro a 10 años con vencimiento 2034."),
]


def at_filtro_falsos_positivos():
    """El filtro no debe tirar textos legítimos (segmentos y divisas en mayúsculas, porcentajes que no son probabilidades)."""
    malos = [(t, v6.texto_prohibido(t)) for t in LEGITIMOS if v6.texto_prohibido(t)]
    informe("filtro_falsos_positivos", "FALLO" if malos else "OK",
            f"{len(malos)}/{len(LEGITIMOS)} textos legítimos descartados: {malos}")


def at_filtro_falsos_negativos():
    """El filtro debe cazar al menos los casos evidentes de R13 y R21 (el README dice «nunca»)."""
    pasan = [(r, t) for r, t in PROHIBIDOS if v6.texto_prohibido(t) is None]
    informe("filtro_falsos_negativos", "FALLO" if pasan else "OK",
            f"{len(pasan)}/{len(PROHIBIDOS)} textos prohibidos que pasan el filtro: {pasan}")


def _sintetizador_con(campos):
    def f(orig):
        def g(msg, ctx, rng):
            out = orig(msg, ctx, rng)
            for k, v in campos.items():
                if k == "frases_30s":
                    out["frases_30s"] = [v] + out["frases_30s"][1:]
                else:
                    out[k] = v
            return out
        return g
    return f


def at_sintetizador_ejemplo_r01_extremo_a_extremo():
    """El ejemplo de H-09 de la QA r01 («compra acciones de Apple (AAPL)»), en la lectura del conjunto y en una frase llana."""
    txt = "Para esta semana, compra acciones de Apple (AAPL) antes de resultados."
    with Parche(_sintetizador=_sintetizador_con({"lectura_conjunto": txt, "frases_30s": txt})):
        b = bloque(cfg())
        r = b.ciclo(AS_OF)
    paq = json.dumps(r["paquete"], ensure_ascii=False)
    ent = json.dumps(r.get("entregables") or {}, ensure_ascii=False, default=str)
    llega = "Apple (AAPL)" in paq or "Apple (AAPL)" in ent
    informe("sintetizador_ejemplo_r01", "FALLO" if llega else "OK",
            f"«{txt}» llega al paquete={'Apple (AAPL)' in paq}, a los entregables={'Apple (AAPL)' in ent}; dictamen 2ª pasada="
            f"{(r.get('g3_entregables') or {}).get('dictamen')}")


def at_sintetizador_falso_positivo_extremo_a_extremo():
    """Una frase llana legítima con una divisa en mayúsculas tira TODOS los textos llanos del Sintetizador."""
    txt = "El sistema no ve motivos para vender USD esta semana."
    with Parche(_sintetizador=_sintetizador_con({"frases_30s": txt})):
        b = bloque(cfg())
        r = b.ciclo(AS_OF)
    lim = [x for x in r["paquete"]["limitaciones"] if "Textos llanos del Sintetizador descartados" in x]
    informe("sintetizador_falso_positivo", "FALLO" if lim else "OK",
            f"frase legítima «{txt}» → textos llanos sustituidos por los de defecto: {bool(lim)} {lim[:1]}")


# ======================================================================================================== H-01: filas de cobertura
def at_cobertura_sin_duplicados_ciclos():
    """Ningún símbolo con dos filas contradictorias en el mismo tipo y run; ninguna elegida sin símbolo en la muestra."""
    b = bloque(cfg(perfiles=("DIV", "RV", "IDX", "FON", "MON")))
    for k in range(3):
        b.ciclo(semana(k))
    dups, nulas = {}, {}
    for e in cobertura(b):
        for c, d in e["clases"].items():
            vistos = {}
            for f in d["filas"]:
                if f.get("simbolo"):
                    vistos.setdefault(f["simbolo"], []).append(f["fase"])
            dd = {s: fs for s, fs in vistos.items() if len(fs) > 1}
            if dd:
                dups[f"{e['fecha']}:{c}"] = dd
            n = [x["opp_id"] for x in d["elegidas"] if not x.get("simbolo")]
            if n:
                nulas[f"{e['fecha']}:{c}"] = len(n)
    informe("cobertura_duplicados", "FALLO" if dups else "OK", f"símbolos con más de una fila: {dups or 'ninguno'}")
    informe("cobertura_elegidas_sin_simbolo", "FALLO" if nulas else "OK",
            f"elegidas (top-3) sin símbolo ni precio en la muestra contrafactual (vigentes arrastradas): {nulas or 'ninguna'}")


def at_cobertura_n1_rotacion():
    """En un ciclo N1 (REVISION_VIGENTES) el Analista recibe la rotación exploratoria: ¿tiene fila en la cobertura?"""
    def f(orig):   # el Analista de N1 devuelve una «exploratoria» de la rotación (el simulado solo lo hace con señal ≥ 0,75)
        def g(msg, ctx, rng, inyectado):
            out = orig(msg, ctx, rng, inyectado)
            if msg.get("fase") == "REVISION_VIGENTES" and not out.get("exploratorias"):
                rot = [u for u in msg.get("universo", []) if u["simbolo"] in (msg.get("rotacion_exploratoria") or [])]
                if rot:
                    out["exploratorias"] = [mr._ficha(rot[0], msg, ctx, rng, inyectado)]
            return out
        return g
    b = bloque(cfg(perfiles=("DIV", "MON", "FON")))
    cuerpos = espiar_mensajes(b)
    b.ciclo(semana(0))
    n0 = len(cuerpos["CT-06"])
    with Parche(_analista=f):
        r2 = b.ciclo(semana(1))
    cob = cobertura(b)[-1]
    faltan = {}
    for m in cuerpos["CT-06"][n0:]:
        if m.get("fase") != "REVISION_VIGENTES":
            continue
        c = m["clase"]
        vistos = {u["simbolo"] for u in m.get("universo", [])}
        filas = {f.get("simbolo") for f in cob["clases"][c]["filas"]}
        sin = sorted(vistos - filas)
        if sin:
            faltan[c] = f"{len(sin)}/{len(vistos)} {sin}"
    informe("cobertura_n1_rotacion", "FALLO" if faltan else "OK",
            f"niveles={r2['nivel_por_clase']}; ámbitos que el Analista recibió en N1 sin fila: {faltan or 'ninguno'}")
    # Las «exploratorias» de N1 se dan de alta en F3 como CANDIDATA: ¿tienen fila?
    expl = [(e["clase"], e.get("simbolo_seguimiento"), e["opp_id"]) for e in b.almacen.leer("F3")
            if e.get("tipo_entrada") == "ALTA" and e.get("exploratoria_prometedora") and r2["run_id"] in (e.get("run_ids") or [])]
    sin = [x for x in expl if x[1] not in {f.get("simbolo") for f in cob["clases"][x[0]]["filas"]}]
    informe("cobertura_n1_candidatas_f3", "FALLO" if sin else ("OK" if expl else "OBS"),
            f"altas CANDIDATA (exploratoria prometedora) en F3 en el run N1: {expl or 'ninguna'}; sin fila en COBERTURA: {sin or 'ninguna'}")


def at_cobertura_vigente_no_propuesta():
    """Vigente que pasa GC1 y el Analista no vuelve a proponer: arrastrada en el top-3. ¿Fila ANALISTA y SELECCION_FINAL a la vez?
    ¿puede la muestra de descartes elegir una opción del top-3?"""
    b = bloque(cfg())
    r1 = b.ciclo(AS_OF)
    vig = sorted(x[2] for x in entregadas(r1))
    quitar = vig[0] if vig else None

    def f(orig):
        def g(msg, ctx, rng, inyectado):
            out = orig(msg, ctx, rng, inyectado)
            if msg.get("fase") == "CRIBADO_E_INVESTIGACION":
                out["finalistas"] = [x for x in out["finalistas"] if x["indicador_seguimiento"]["simbolo"] != quitar]
            return out
        return g
    with Parche(_analista=f):
        r2 = b.ciclo(semana(1), nivel_forzado="N2")
    cob = cobertura(b)[-1]["clases"]["DIV"]
    filas = [x for x in cob["filas"] if x.get("simbolo") == quitar]
    en_top = quitar in {x[2] for x in entregadas(r2)}
    en_muestra = quitar in {x["simbolo"] for x in cob["muestra_descartes"]}
    eleg = [x for x in cob["elegidas"] if x.get("simbolo") == quitar or not x.get("simbolo")]
    contradice = en_top and any(x["fase"] != "SELECCION_FINAL" for x in filas)
    informe("cobertura_vigente_no_propuesta", "FALLO" if contradice else "OK",
            f"{quitar}: en el top-3={en_top}; filas={[(x['fase'], x['motivo'][:45]) for x in filas]}; en la muestra de descartes="
            f"{en_muestra}; elegidas sin símbolo={len([x for x in eleg if not x.get('simbolo')])}")


def at_gc1_puenteado_y_entregado():
    """Variante: el Analista devuelve como única finalista un ámbito que GC1 descartó y no le envió. ¿Llega al Broker?"""
    div = list(UNIVERSO.loc[UNIVERSO["clase"] == "DIV", "simbolo"])
    estado = {}

    def f(orig):
        def g(msg, ctx, rng, inyectado):
            out = orig(msg, ctx, rng, inyectado)
            if msg.get("fase") == "CRIBADO_E_INVESTIGACION" and out.get("finalistas"):
                enviados = {u["simbolo"] for u in msg["universo"]}
                fuera = [s for s in div if s not in enviados]
                if fuera:
                    x = copy.deepcopy(out["finalistas"][0])
                    x["indicador_seguimiento"] = {**x["indicador_seguimiento"], "simbolo": fuera[0]}
                    x["nombre"] = f"Ámbito {fuera[0]}"
                    out["finalistas"] = [x]
                    estado["sym"] = fuera[0]
            return out
        return g
    with Parche(_analista=f):
        b = bloque(cfg(seleccion={"umbral_senal_gc1": 0.75}, v6={"gc1": {"exploracion_celdas": 0}}))
        r = b.ciclo(AS_OF)
    sym = estado.get("sym")
    cob = cobertura(b)[-1]["clases"]["DIV"]
    fases = [(x["fase"], x["motivo"][:50]) for x in cob["filas"] if x.get("simbolo") == sym]
    sale = sym in {x[2] for x in entregadas(r)}
    informe("gc1_puenteado_entregado", "FALLO" if sale else "OK", f"{sym}: filas={fases}; entregado al Broker={sale}; estado={r['estado']}")


def at_gc1_puenteado_por_el_analista():
    """El Analista propone como finalista un ámbito del tipo que GC1 (código) descartó y no le envió: ¿se acepta?"""
    div = list(UNIVERSO.loc[UNIVERSO["clase"] == "DIV", "simbolo"])
    estado = {}

    def f(orig):
        def g(msg, ctx, rng, inyectado):
            out = orig(msg, ctx, rng, inyectado)
            if msg.get("fase") == "CRIBADO_E_INVESTIGACION" and out.get("finalistas"):
                enviados = {u["simbolo"] for u in msg["universo"]}
                fuera = [s for s in div if s not in enviados]
                if fuera:
                    x = copy.deepcopy(out["finalistas"][0])
                    x["indicador_seguimiento"] = {**x["indicador_seguimiento"], "simbolo": fuera[0]}
                    x["nombre"] = f"Ámbito {fuera[0]}"
                    out["finalistas"] = [x] + out["finalistas"][:3]
                    estado["sym"] = fuera[0]
            return out
        return g
    with Parche(_analista=f):
        b = bloque(cfg(seleccion={"umbral_senal_gc1": 0.75}, v6={"gc1": {"exploracion_celdas": 0}}))
        r = b.ciclo(AS_OF)
    sym = estado.get("sym")
    cob = cobertura(b)[-1]["clases"]["DIV"]
    fases = [x["fase"] for x in cob["filas"] if x.get("simbolo") == sym]
    aceptada = any(x != "GC1" for x in fases)
    informe("gc1_puenteado", "FALLO" if aceptada else "OK",
            f"ámbito descartado por GC1 y no enviado: {sym}; filas={fases}; entregado={sym in {x[2] for x in entregadas(r)}}")


# ======================================================================================================== H-03: PARCIAL
def at_parcial_por_omision_fuera_del_top3():
    """Prospectiva omite una finalista que no iba a entrar en el top-3: ¿el run pasa a PARCIAL? (OBS: efecto del estado nuevo)"""
    estado = {}

    def f(orig):
        def g(msg, ctx, rng):
            out = orig(msg, ctx, rng)
            refs = [e["ref"] for e in msg["encargos"]]
            estado.setdefault("ultima", refs[-1])
            out["resultados"] = [x for x in out["resultados"] if x["ref"] != estado["ultima"]]
            return out
        return g
    with Parche(_prospectiva=f):
        b = bloque(cfg())
        r = b.ciclo(AS_OF)
    ref = estado.get("ultima")
    en_top = ref and ref.split(":")[1] in {x[2] for x in entregadas(r)}
    lim = [x for x in r["paquete"]["limitaciones"] if "Prospectiva" in x or "pronóstico" in x]
    informe("parcial_omision", "OBS", f"omitida {ref} (habría estado en el top-3: {en_top}); estado={r['estado']}; limitaciones={lim[:2]}")


def at_parcial_v5_no_cambia():
    """Con la V5, `incompleto_v6` no puede dejar el run PARCIAL (info_prosp e info_critica son None)."""
    r = bloque(cfg(diseno="v5")).ciclo(AS_OF)
    informe("parcial_v5", "OK" if r["estado"] == "COMPLETO" else "FALLO", f"V5 estado={r['estado']}")


def at_contradictor_mudo_declarado():
    """H-03 con el ataque de la r01 corregido: el texto de la limitación nueva es «no devolvió la crítica», no «Sin crítica»."""
    def f(orig):
        def g(msg, ctx, rng):
            if "contrarreplicas" in msg:
                return orig(msg, ctx, rng)
            return {"resultados": [], "autoevaluacion": "nada"}
        return g
    with Parche(_contrarias=f):
        b = bloque(cfg(perfiles=("DIV", "RV")))
        r = b.ciclo(AS_OF)
    cob = cobertura(b)[0]
    sr = cob["critica"]["sin_respuesta"]
    lim = [x for x in r["paquete"]["limitaciones"] if "no devolvió la crítica" in x]
    declaradas = all(s in " ".join(lim) for s in sr)
    filas_ok = all(any(f.get("simbolo") == s.split(":")[1] and f["fase"] == "CRITICA" for f in cob["clases"][s.split(":")[0]]["filas"]) for s in sr)
    nuevas = [x for x in entregadas(r) if r["nivel_por_clase"][x[0]] in ("N2", "N3")]
    ok = sr and declaradas and filas_ok and not nuevas and r["estado"] == "PARCIAL"
    informe("contradictor_mudo_declarado", "OK" if ok else "FALLO",
            f"sin_respuesta={len(sr)}; declaradas={declaradas}; filas CRITICA={filas_ok}; entregadas nuevas={len(nuevas)}; estado={r['estado']}")


# ======================================================================================================== H-07: validación y presupuesto
def at_validacion_configuraciones_legitimas():
    """Configuraciones legítimas de la sección v6 que no deben rechazarse, y la V5 con una sección v6 rota."""
    legit = [{"auditoria_fraccion": 0}, {"auditoria_fraccion": 1}, {"cobertura": {"muestra_descartes": 0}},
             {"contradictor": {"max_rondas_sustitucion": 0}}, {"gc1": {"exploracion_celdas": 0}},
             {"cobertura": {"horizonte_contrafactual": "H1"}}, {"cobertura": {"horizonte_contrafactual": "H5"}},
             {"analista": {"base_conocimientos": "completa"}}, {"contradictor": {"proveedor": "otro"}},
             {"gc1": {"senal_por_perfil": {"DIV": "momentum_12_1"}}}, {"sintetizador_limites": {"regimen": 500}},
             {"prospectiva": {"max_encargos_por_lote": 1}}]
    malas = []
    for x in legit:
        try:
            bloque(cfg(v6=x))
        except Exception as ex:   # noqa: BLE001
            malas.append((x, f"{type(ex).__name__}: {ex}"))
    informe("validacion_legitimas", "FALLO" if malas else "OK", f"rechazadas: {malas or 'ninguna'}")
    rotas = []
    for x in ({"auditoria_fraccion": 7}, {"gc1": {"exploracion_celdas": -3}}, {"sintetizador_limites": None}):
        try:
            r = bloque(cfg(diseno="v5", v6=x)).ciclo(AS_OF) if x is not None else None
            rotas.append((x, r["estado"] if r else None))
        except Exception as ex:   # noqa: BLE001
            rotas.append((x, f"{type(ex).__name__}"))
    informe("validacion_v5_no_afectada", "OK" if all(s == "COMPLETO" for _, s in rotas) else "FALLO",
            f"V5 con sección v6 rota: {rotas}")


def at_validacion_tipos_raros():
    """Tipos inesperados en la sección v6: deben fallar cerrado con ValueError (no con otro error ni aceptarse)."""
    casos = [{"auditoria_fraccion": float("nan")}, {"auditoria_fraccion": "0.25"}, {"cobertura": {"muestra_descartes": 2.0}},
             {"gc1": None}, {"gc1": {"senal_por_perfil": ["DIV"]}}, {"sintetizador_limites": {"preguntas": -1}},
             {"cobertura": {"horizonte_contrafactual": None}}]
    res = []
    for x in casos:
        try:
            bloque(cfg(v6=x))
            res.append((x, "ACEPTADA"))
        except ValueError:
            res.append((x, "ValueError"))
        except Exception as ex:   # noqa: BLE001
            res.append((x, type(ex).__name__))
    raros = [(x, s) for x, s in res if s != "ValueError"]
    informe("validacion_tipos_raros", "OBS" if raros else "OK", f"{res}")


def at_validacion_clave_de_senal_inexistente():
    """Una clave de señal mal escrita en `senal_por_perfil` pasa la validación y GC1 deja pasar todo como «sin señal medible»."""
    b = bloque(cfg(v6={"gc1": {"senal_por_perfil": {"DIV": "senal_compuessta"}}}))
    b.ciclo(AS_OF)
    g = cobertura(b)[-1]["clases"]["DIV"]["gc1"]
    informe("gc1_clave_inexistente", "FALLO" if not g["pasan"] and g["sin_senal_medible"] else "OK",
            f"pasan={g['pasan']}; sin señal medible={len(g['sin_senal_medible'])}/{g['universo']}; sin aviso en la validación")


def at_presupuesto_override_bolsa():
    """El override de la bolsa del ciclo (`V6_GLOBAL`) después de la corrección de H-07, y el cierre parcial con la bolsa vacía."""
    from bloque_a import orquestacion as orq
    capt = []
    P = orq.Presupuesto

    class Espia(P):
        def __init__(self, asign, cfg_):
            capt.append(dict(asign))
            super().__init__(asign, cfg_)
    orq.Presupuesto = Espia
    try:
        b = bloque(cfg())
        b._solicitar_ampliacion = lambda *a, **k: False
        r = b.ciclo(AS_OF, presupuesto_override={v6.BOLSA_GLOBAL: 0.001})
    finally:
        orq.Presupuesto = P
    bolsa = capt[-1].get(v6.BOLSA_GLOBAL)
    informe("override_de_la_bolsa", "FALLO" if bolsa > 0.01 else "OK",
            f"override V6_GLOBAL=0.001 → bolsa real={bolsa}; estado={r['estado']}; entregadas nuevas={len(entregadas(r))}")
    # Bolsa vacía por otra vía (sin override): el cierre parcial debe seguir funcionando
    orig = v6.repartir_presupuesto

    def vacia(bl, asign, clases):
        out = orig(bl, asign, clases)
        out["COMUN"] += out[v6.BOLSA_GLOBAL] - 0.001
        out[v6.BOLSA_GLOBAL] = 0.001
        return out
    v6.repartir_presupuesto = vacia
    try:
        cli = MockClient()
        b = bloque(cfg(perfiles=("DIV", "RV")), cli)
        b._solicitar_ampliacion = lambda *a, **k: False
        r = b.ciclo(AS_OF)
    finally:
        v6.repartir_presupuesto = orig
    nuevas = [x for x in entregadas(r) if r["nivel_por_clase"][x[0]] in ("N2", "N3")]
    informe("bolsa_vacia_cierra_parcial", "OK" if not nuevas and r["estado"] == "PARCIAL" else "FALLO",
            f"estado={r['estado']}; entregadas nuevas={sorted(nuevas)}")


def at_presupuesto_override_clase():
    """Override de un tipo: el total coincide con el de la V5 con el mismo override."""
    from bloque_a import orquestacion as orq
    capt = {}
    P = orq.Presupuesto

    class Espia(P):
        def __init__(self, asign, cfg_):
            capt.setdefault("a", []).append(dict(asign))
            super().__init__(asign, cfg_)
    orq.Presupuesto = Espia
    try:
        for d in ("v5", "v6"):
            bloque(cfg(diseno=d, perfiles=("DIV", "RV"))).ciclo(AS_OF, tipo="AD_HOC", presupuesto_override={"DIV": 30.0})
    finally:
        orq.Presupuesto = P
    a5, a6 = capt["a"][0], capt["a"][-1]
    ok = abs(sum(a5.values()) - sum(a6.values())) < 1e-6
    informe("override_de_un_tipo", "OK" if ok else "FALLO", f"V5 Σ={sum(a5.values()):.4f}; V6 Σ={sum(a6.values()):.4f}; DIV V6={a6['DIV']}")


# ======================================================================================================== H-04: reintento
def at_reintento_lote_de_uno_contradictor():
    """Lote de uno en el Contradictor (máx. 1 por lote) y la ref omitida siempre: el reintento llega al modelo, una sola vez."""
    vistos = []

    def f(orig):
        def g(msg, ctx, rng):
            if "contrarreplicas" in msg:
                return orig(msg, ctx, rng)
            vistos.append(("R" if "reintento_de_cobertura" in msg else "1", [p["ref"] for p in msg["peticiones"]]))
            out = orig(msg, ctx, rng)
            out["resultados"] = [x for x in out["resultados"] if x["ref"] != vistos[0][1][0]]
            return out
        return g
    with Parche(_contrarias=f):
        cli = MockClient()
        b = bloque(cfg(v6={"prospectiva": {"max_encargos_por_lote": 1}}), cli)
        r = b.ciclo(AS_OF)
    victima = vistos[0][1][0]
    veces = [k for k, refs in vistos if victima in refs]
    ok = veces == ["1", "R"] and victima.split(":")[1] not in {x[2] for x in entregadas(r)}
    informe("reintento_contradictor_lote_de_uno", "OK" if ok else "FALLO",
            f"{victima}: llamadas al simulado={veces} (esperado una normal y un reintento); estado={r['estado']}")


def at_reintento_mismo_ciclo_repetido():
    """Repetir el mismo ciclo (misma fecha) en un estado nuevo: el reintento es determinista (mismas llamadas)."""
    def correr():
        def f(orig):
            def g(msg, ctx, rng):
                out = orig(msg, ctx, rng)
                if "reintento_de_cobertura" not in msg:
                    out["resultados"] = out["resultados"][1:]
                return out
            return g
        with Parche(_prospectiva=f):
            cli = MockClient()
            b = bloque(cfg(), cli)
            b.ciclo(AS_OF)
        return [x["agente"] for x in cli.llamadas], cobertura(b)[-1]["prospectiva"]
    a, pa = correr()
    b_, pb = correr()
    informe("reintento_determinista", "OK" if a == b_ and pa == pb else "FALLO", f"llamadas iguales={a == b_}; prospectiva={pa}")


# ======================================================================================================== H-10: contrafactual
def at_contrafactual_sin_precios_nunca():
    """Sin precios al vencer, nunca: el contrafactual se aplaza indefinidamente (sin tope ni marca NO_RESOLUBLE)."""
    b = bloque(cfg())
    b.ciclo(AS_OF)
    cob = cobertura(b)[0]
    vence = v6._fecha_vencimiento(b, cob["fecha"], cob["horizonte_contrafactual"])
    orig = v6._precio
    v6._precio = lambda bl, sim, fecha: None if pd.Timestamp(fecha) == vence else orig(bl, sim, fecha)
    try:
        n = []
        for k in range(6):
            dia = vence + pd.Timedelta(days=7 * k)
            b.fijar_fecha(dia)
            n.append(len(v6.resolver_contrafactual(b, dia, f"RUN-X{k}")))
    finally:
        v6._precio = orig
    informe("contrafactual_aplazado_sin_fin", "OBS", f"resoluciones en 6 ciclos tras vencer sin precios: {n} (sin tope; sin estado NO_RESOLUBLE)")


def at_contrafactual_una_sola_vez_tras_aplazar():
    """Aplazado un ciclo y resuelto el siguiente: una sola entrada CTF- aunque se llame varias veces."""
    b = bloque(cfg())
    b.ciclo(AS_OF)
    cob = cobertura(b)[0]
    vence = v6._fecha_vencimiento(b, cob["fecha"], cob["horizonte_contrafactual"])
    b.fijar_fecha(vence + pd.Timedelta(days=14))
    orig = v6._precio
    v6._precio = lambda bl, sim, fecha: None if pd.Timestamp(fecha) == vence else orig(bl, sim, fecha)
    try:
        a = len(v6.resolver_contrafactual(b, vence, "RUN-A"))
    finally:
        v6._precio = orig
    c = [len(v6.resolver_contrafactual(b, vence + pd.Timedelta(days=7 * k), f"RUN-B{k}")) for k in range(3)]
    ctf = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "CONTRAFACTUAL"]
    ok = a == 0 and c == [1, 0, 0] and len(ctf) == 1
    informe("contrafactual_una_vez", "OK" if ok else "FALLO", f"aplazado={a}; después={c}; CTF- en HA={len(ctf)}")


def at_contrafactual_clase_sin_precio_con_otra_con_precio():
    """Dos tipos: uno sin precios al vencer y otro con precios. Se resuelve con `sin_precio` en el primero y no se reintenta."""
    b = bloque(cfg(perfiles=("DIV", "RV")))
    b.ciclo(AS_OF)
    cob = cobertura(b)[0]
    vence = v6._fecha_vencimiento(b, cob["fecha"], cob["horizonte_contrafactual"])
    div = set(UNIVERSO.loc[UNIVERSO["clase"] == "DIV", "simbolo"])
    orig = v6._precio
    v6._precio = lambda bl, sim, fecha: None if pd.Timestamp(fecha) == vence and sim in div else orig(bl, sim, fecha)
    b.fijar_fecha(vence)
    try:
        r = v6.resolver_contrafactual(b, vence, "RUN-X")
    finally:
        v6._precio = orig
    d = r[0]["clases"]["DIV"] if r else {}
    informe("contrafactual_parcial", "OBS", f"resueltas={len(r)}; DIV={d}; la parte de DIV queda resuelta sin datos y no se reintenta")


def at_contrafactual_solo_vigentes():
    """Un run en el que el top-3 son vigentes arrastradas y no hay descartes: ¿qué resuelve el contrafactual?"""
    b = bloque(cfg(perfiles=("DIV", "RV")))
    b.ciclo(semana(0))
    b.ciclo(semana(1))
    cob = cobertura(b)[-1]
    vence = v6._fecha_vencimiento(b, cob["fecha"], cob["horizonte_contrafactual"])
    b.fijar_fecha(vence)
    r = [x for x in v6.resolver_contrafactual(b, vence, "RUN-X") if x["cobertura_id"] == cob["id"]]
    informe("contrafactual_solo_vigentes", "OBS",
            f"COB {cob['id']}: elegidas={ {c: [x['simbolo'] for x in d['elegidas']] for c, d in cob['clases'].items()} }; "
            f"muestra={ {c: len(d['muestra_descartes']) for c, d in cob['clases'].items()} }; resuelto={r[0]['clases'] if r else None}")


# ======================================================================================================== H-05: nota de GC1
def at_nota_gc1_solo_con_gc1():
    """La nota va con GC1 por código en CRIBADO, no en REVISION_VIGENTES ni con `gc1.por_codigo: false`, y nunca en la V5."""
    def instrucciones(c, fechas):
        cli = MockClient()
        vis = []
        gen = cli.generar

        def _gen(**kw):
            if kw["agente"] == "AG-05":
                vis.append(kw["mensajes"][0]["content"])
            return gen(**kw)
        cli.generar = _gen
        b = bloque(c, cli)
        for f in fechas:
            b.ciclo(f)
        return vis
    nota = "ya ha aplicado GC1"
    v6_ = instrucciones(cfg(), [semana(0), semana(1)])
    sin = instrucciones(cfg(v6={"gc1": {"por_codigo": False}}), [semana(0)])
    v5_ = instrucciones(cfg(diseno="v5"), [semana(0)])
    con = [nota in t for t in v6_]
    ok = con and con[0] and not any(nota in t for t in sin + v5_)
    informe("nota_gc1", "OK" if ok else "FALLO", f"V6 por ciclo={con}; con por_codigo false={[nota in t for t in sin]}; V5={[nota in t for t in v5_]}")


ATAQUES = [v for k, v in sorted(globals().items()) if k.startswith("at_")]

if __name__ == "__main__":
    for f in ATAQUES:
        if FILTRO and FILTRO not in f.__name__:
            continue
        try:
            f()
        except Exception as ex:   # noqa: BLE001
            informe(f.__name__, "ERROR", f"{type(ex).__name__}: {ex} · {traceback.format_exc()[-900:]}")
    print("\nResumen:", {e: sum(1 for x in RES if x[1] == e) for e in ("OK", "FALLO", "OBS", "ERROR")})
    sys.exit(1 if any(x[1] in ("FALLO", "ERROR") for x in RES) else 0)
