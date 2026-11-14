"""Diseño V6 del Bloque A (T-101): el rediseño aspirante con menos papeles de IA.

Se activa con `diseno: v6` (por defecto `v5`). Recoge la propuesta de Claude (`.docs/diseno/bloque_a/propuesta_claude.md`),
los cambios de la revisión C-01 de Astra que acepta la decisión de Claude (`decision_claude_c01.md`) y sus ideas nuevas:

- GC1 por código antes del Analista, con catálogo mínimo de señales por perfil, paso marcado de lo que no tiene señal
  medible y exploración sembrada para medir falsos negativos;
- Prospectiva una vez por ciclo, en lotes por tamaño y con control de cobertura por identificador (A-02);
- Contradictor solo de la selección provisional y de sus sustitutas; lo que no se ha podido criticar no se entrega (A-01);
- integración determinista antes de G3 y Sintetizador (AG-26) después, sobre el paquete validado;
- registro de cobertura del embudo y muestra de descartes con seguimiento contrafactual (A-05).

Las funciones reciben el `Bloque` y reutilizan sus piezas: los contratos, los archivos y las herramientas no cambian.
"""
from __future__ import annotations

import copy
import hashlib
import math
import numbers
import re
import unicodedata
from typing import Any

import pandas as pd

from . import sintesis as sint
from .configuracion import NOMBRE_CLASE, parametro
from .contratos import AGENTE_CLASE
from .herramientas.ht01_datos import DatosNoDisponibles, FugaDeInformacion

DISENOS = ("v5", "v6")
# Señales numéricas que calcula el Motor para cada ámbito (`Bloque.senales_clase`): las que puede usar GC1 por perfil (H-19)
SENALES_GC1 = ("senal_compuesta", "momentum_12_1", "pct_momentum_clase", "z_momentum_clase", "senal_tsmom", "vol_20d", "vol_ewma",
               "p_tendencia", "pendiente_sen_semanal", "riesgo_1a5", "mdd", "drawdown_actual", "z_precio_3a", "pct_precio_3a",
               "rent_1s", "rent_1m", "rent_3m", "rent_12m", "familias_concordantes")
FAMILIAS_SENAL_COMPUESTA = 3   # momento, tendencia y valoración relativa (`Bloque.senales_clase`)
BOLSA_GLOBAL = "V6_GLOBAL"   # bolsa de las llamadas de todo el ciclo (Prospectiva, Contradictor y Sintetizador)


def _entero(cfg, clave, minimo):
    v = parametro(cfg, f"v6.{clave}")
    if isinstance(v, bool) or not isinstance(v, int) or v < minimo:
        raise ValueError(f"v6.{clave} debe ser un entero ≥ {minimo} (es {v!r})")


def validar(cfg: dict) -> bool:
    """`diseno` debe ser «v5» o «v6» y, con la V6, su sección `v6` debe ser legible (falla cerrado al crear el Bloque; QA r01
    de T-101, H-07). Devuelve si el diseño es V6."""
    d = cfg.get("diseno", "v5")
    if d not in DISENOS:
        raise ValueError(f"`diseno` desconocido: {d!r} (v5 | v6)")
    if d != "v6":
        return False
    for clave, minimo in (("gc1.exploracion_celdas", 0), ("prospectiva.max_encargos_por_lote", 1),
                          ("contradictor.max_rondas_sustitucion", 0), ("cobertura.muestra_descartes", 0),
                          ("contradictor.max_evidencias", 1), ("contradictor.contrarreplica_max", 1),
                          ("cobertura.dias_max_espera_precio", 0)):
        _entero(cfg, clave, minimo)
    fr = parametro(cfg, "v6.auditoria_fraccion")
    if isinstance(fr, bool) or not isinstance(fr, (int, float)) or not 0 <= float(fr) <= 1:
        raise ValueError(f"v6.auditoria_fraccion debe estar entre 0 y 1 (es {fr!r})")
    if parametro(cfg, "v6.analista.base_conocimientos") not in ("ninguna", "completa"):
        raise ValueError("v6.analista.base_conocimientos debe ser «ninguna» o «completa»")
    if parametro(cfg, "v6.contradictor.proveedor") not in ("mismo", "otro"):
        raise ValueError("v6.contradictor.proveedor debe ser «mismo» u «otro»")
    if parametro(cfg, "v6.cobertura.horizonte_contrafactual") not in parametro(cfg, "horizontes"):
        raise ValueError("v6.cobertura.horizonte_contrafactual debe ser un horizonte de `horizontes`")
    from .configuracion import CLASES
    spp = ((cfg.get("v6") or {}).get("gc1") or {}).get("senal_por_perfil") or {}
    if not isinstance(spp, dict) or any(k not in CLASES or v not in SENALES_GC1 for k, v in spp.items()):
        raise ValueError(f"v6.gc1.senal_por_perfil debe ser {{tipo de activo: señal del Motor}}, con señales de {SENALES_GC1}")
    # T-117: umbral de GC1 por tipo de activo y concordancia mínima de familias de la señal compuesta (Anexo A)
    upp = ((cfg.get("v6") or {}).get("gc1") or {}).get("umbral_por_perfil")
    upp = {} if upp is None else upp
    if not isinstance(upp, dict) or any(k not in CLASES or isinstance(v, bool) or not isinstance(v, (int, float))
                                        or not math.isfinite(float(v)) or not 0 < float(v) <= 1 for k, v in upp.items()):
        raise ValueError("v6.gc1.umbral_por_perfil debe ser {tipo de activo: umbral}, con umbrales mayores que 0 y hasta 1")
    fmin = ((cfg.get("v6") or {}).get("gc1") or {}).get("familias_min", 0)
    if isinstance(fmin, bool) or not isinstance(fmin, int) or not 0 <= fmin <= FAMILIAS_SENAL_COMPUESTA:
        raise ValueError(f"v6.gc1.familias_min debe ser un entero de 0 a {FAMILIAS_SENAL_COMPUESTA}")
    lim = parametro(cfg, "v6.sintetizador_limites")
    for k in ("regimen", "factor", "lectura", "texto_minimo", "preguntas", "limitaciones", "limitacion"):
        if isinstance(lim.get(k), bool) or not isinstance(lim.get(k), int) or lim[k] < 1:
            raise ValueError(f"v6.sintetizador_limites.{k} debe ser un entero ≥ 1")
    return True


def op(bloque, clave: str) -> Any:
    return parametro(bloque.cfg, f"v6.{clave}")


def activo(bloque, clave: str) -> bool:
    return bool(getattr(bloque, "v6", False)) and bool(op(bloque, clave))


def _sembrado(*partes) -> str:
    return hashlib.sha256("|".join(str(p) for p in partes).encode()).hexdigest()


def _ref(clase: str, f: dict) -> str:
    return f"{clase}:{f['proxy']}"


def _lotes(items: list, por_lote: int) -> list[list]:
    n = max(1, int(por_lote))
    return [items[i:i + n] for i in range(0, len(items), n)]


# ======================================================================================================
# Presupuesto: las llamadas de todo el ciclo salen de lo que cada tipo reservaba para ellas
# ======================================================================================================
def repartir_presupuesto(bloque, asign: dict[str, float], clases: list[str], fija: float | None = None) -> dict[str, float]:
    """Con Prospectiva y Contradictor por ciclo, la parte de `reparto_fases` de prospectiva y refutación de cada tipo pasa
    a una bolsa común del ciclo (`V6_GLOBAL`): el total no cambia (R5)."""
    if not activo(bloque, "prospectiva.global"):
        return asign
    rep = parametro(bloque.cfg, "presupuesto_uc.reparto_fases")
    fr = float(rep["prospectiva"]) + float(rep["refutacion"])
    out = dict(asign)
    if fija is not None:   # QA r02, H-18: un `presupuesto_override` de la bolsa del ciclo se respeta tal cual
        out[BOLSA_GLOBAL] = float(fija)
        return out
    out[BOLSA_GLOBAL] = 0.0
    for c in clases:
        parte = round(out[c] * fr, 6)
        out[c] = round(out[c] - parte, 6)
        out[BOLSA_GLOBAL] = round(out[BOLSA_GLOBAL] + parte, 6)
    return out


# ======================================================================================================
# GC1 por código (PA-04)
# ======================================================================================================
def _bajo_umbral(valor: float, umbral: float) -> str:
    """Una señal que no llega al umbral, con dos decimales; si así redondeada lo alcanzaría, con las cifras que hagan falta
    para que el motivo no diga «0.65 < 0.65» (QA r01 de T-117, H-06)."""
    corto = f"{valor:.2f}"
    return corto if float(corto) < umbral else f"{valor:.8g}"


def umbral_gc1(bloque, clase: str) -> float:
    """Umbral de GC1 del tipo de activo en el diseño V6: el suyo (`v6.gc1.umbral_por_perfil`) o, si no lo tiene, el general.
    QA r01 de T-117, H-01: es el mismo que el encargo CT-06 le comunica al Analista."""
    propio = (op(bloque, "gc1.umbral_por_perfil") or {}).get(clase)
    return float(propio if propio is not None else parametro(bloque.cfg, "seleccion.umbral_senal_gc1"))


def gc1(bloque, clase: str, universo: list[dict], vigentes: list[dict], as_of) -> tuple[list[dict], dict]:
    """Filtra el universo que recibe el Analista. Pasan como mucho `seleccion.max_candidatas` ámbitos cuya señal llega al
    umbral de su tipo (`v6.gc1.umbral_por_perfil`; si no lo tiene, `seleccion.umbral_senal_gc1`) y, cuando manda la señal
    compuesta, con al menos `v6.gc1.familias_min` familias concordantes (Anexo A; T-117); un ámbito sin señal medible no se descarta (pasa marcado: la falta de señal no prueba la
    falta de oportunidad); `v6.gc1.exploracion_celdas` de los que no pasan llegan igualmente, elegidos por una semilla del
    corte, para medir los falsos negativos; las vigentes siempre llegan. Devuelve el universo y el registro de GC1."""
    clave = (op(bloque, "gc1.senal_por_perfil") or {}).get(clase) or "senal_compuesta"
    umbral = umbral_gc1(bloque, clase)
    fam_min = int(op(bloque, "gc1.familias_min") or 0) if clave == "senal_compuesta" else 0
    maxc = int(parametro(bloque.cfg, "seleccion.max_candidatas"))
    n_expl = int(op(bloque, "gc1.exploracion_celdas"))
    from .orquestacion import simbolo_seguimiento
    simb_vig = {simbolo_seguimiento(v) for v in vigentes}
    con: list[dict] = []
    sin: list[dict] = []
    for u in universo:
        v = (u.get("senales") or {}).get(clave)
        # H-06 (QA r01): una señal NaN o infinita no es una señal medible: pasa marcada, no ordena ni descarta
        medible = isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(float(v))
        (con if medible else sin).append(u)
    orden = sorted(con, key=lambda u: (-float(u["senales"][clave]), u["simbolo"]))
    def pocas_familias(u) -> bool:
        """Con la señal compuesta, el Anexo A pide además concordancia de familias. Si el Motor no da el recuento, no se
        descarta por esto: la falta del dato no prueba la falta de concordancia."""
        n = (u.get("senales") or {}).get("familias_concordantes")
        if fam_min <= 0 or isinstance(n, bool) or not isinstance(n, numbers.Real):   # H-02: también float o numpy enteros
            return False
        return math.isfinite(float(n)) and float(n) < fam_min

    pasan = [u for u in orden if float(u["senales"][clave]) >= umbral and not pocas_familias(u)][:maxc]
    ids_pasan = {u["simbolo"] for u in pasan}
    resto = [u for u in orden if u["simbolo"] not in ids_pasan]
    expl = sorted(resto, key=lambda u: _sembrado(pd.Timestamp(as_of).date(), clase, u["simbolo"]))[:n_expl]
    ids_expl = {u["simbolo"] for u in expl}
    marca = {}
    for u in pasan:
        marca[u["simbolo"]] = "PASA"
    for u in expl:
        marca[u["simbolo"]] = "EXPLORACION"
    for u in sin:
        marca[u["simbolo"]] = "SIN_SENAL_MEDIBLE"
    for u in universo:
        if u["simbolo"] in simb_vig and u["simbolo"] not in marca:
            marca[u["simbolo"]] = "VIGENTE"
    filtrado = []
    for u in universo:
        if u["simbolo"] in marca:
            filtrado.append({**u, "gc1": marca[u["simbolo"]]})
    descartes = [{"simbolo": u["simbolo"], "senal": round(float(u["senales"][clave]), 4),
                  "motivo": f"{clave} {_bajo_umbral(float(u['senales'][clave]), umbral)} < {umbral}" if float(u["senales"][clave]) < umbral
                  else (f"{u['senales']['familias_concordantes']} familias concordantes < {fam_min}" if pocas_familias(u)
                        else f"fuera de las {maxc} candidatas con más señal")}
                 for u in resto if u["simbolo"] not in ids_expl and marca.get(u["simbolo"]) != "VIGENTE"]
    reg = {"clave_senal": clave, "umbral": umbral, "familias_min": fam_min, "universo": len(universo), "pasan": sorted(ids_pasan),
           "exploracion": sorted(ids_expl), "sin_senal_medible": sorted(u["simbolo"] for u in sin),
           "vigentes": sorted(s for s, m in marca.items() if m == "VIGENTE"), "descartes": descartes, "falsos_negativos": []}
    return filtrado, reg


NOTA_GC1 = (" El ejecutor ya ha aplicado GC1 por código (diseño V6). Cada ámbito del universo lleva la marca `gc1`: PASA (su señal "
            "llega al umbral), EXPLORACION (no llega, pero se te ofrece para medir lo que el filtro deja escapar), "
            "SIN_SENAL_MEDIBLE (el Motor no tiene señal para él) o VIGENTE. Evalúa todos con la estrategia de tu tipo de activo: "
            "no descartes un ámbito EXPLORACION o SIN_SENAL_MEDIBLE solo por su señal; propónlo como finalista si tu análisis lo "
            "sostiene. En `cribado`, `paso_gc1` es tu juicio sobre el ámbito, no la marca del ejecutor.")


def gc1_decisiones(an: dict) -> list[dict] | None:
    """QA r02, H-16: con GC1 por código, las decisiones de GC1 (embudo del paquete y F5) son las del código, no el `paso_gc1`
    del Analista. None si el tipo no pasó por GC1 por código."""
    g = an.get("gc1")
    if not g:
        return None
    out = [{"objeto": x, "resultado": True, "motivo": f"{g['clave_senal']} ≥ {g['umbral']}"} for x in g["pasan"]]
    out += [{"objeto": x, "resultado": False, "motivo": "no llega al umbral: se ofrece al Analista como exploración"} for x in g["exploracion"]]
    out += [{"objeto": x, "resultado": False, "motivo": "sin señal medible: se ofrece al Analista sin descartar"} for x in g["sin_senal_medible"]]
    out += [{"objeto": d["simbolo"], "resultado": False, "motivo": d["motivo"]} for d in g["descartes"]]
    return out


def gc1_falsos_negativos(out: dict) -> None:
    """Un ámbito de exploración que el Analista convierte en finalista es un falso negativo de GC1 (idea 5)."""
    reg = out.get("gc1")
    if not reg:
        return
    expl = set(reg["exploracion"])
    reg["falsos_negativos"] = sorted({f["proxy"] for f in out["finalistas"] if f["proxy"] in expl})


# ======================================================================================================
# Prospectiva una vez por ciclo (A-02)
# ======================================================================================================
INSTR_PROSPECTIVA = ("Para cada encargo, construye escenarios por horizonte y propone un pronóstico verificable por horizonte pedido: "
                     "vista (alcista/bajista para DIRECCIONAL; relativa_favorable/relativa_desfavorable para RELATIVO frente a la "
                     "referencia), probabilidad interna (0,05–0,95), afirmación inequívoca y escenario. Devuelve un resultado por "
                     "cada «ref» recibida: los encargos son de tipos de activo distintos y no comparten razonamiento.")


def prospectiva_global(bloque, grupos: dict[str, list[dict]], as_of, run_id, presupuesto, hz_interes) -> dict:
    """Prospectiva de las finalistas de todos los tipos, en lotes de `v6.prospectiva.max_encargos_por_lote` (o uno por tipo
    si `lotes_por_perfil`). Un encargo sin resultado se pide una vez más en un lote aparte; si sigue faltando, la finalista
    queda sin pronóstico, marcada y declarada (nunca como pronóstico negativo)."""
    certs = [c["celda"] for c in bloque.evaluador.certificados_vigentes(as_of) if c["celda"].get("metodo")]
    encargos, por_ref = [], {}
    for clase, finales in grupos.items():
        for f in finales:
            ref_i = bloque._referencia(clase, f["proxy"])
            tipo_p = "DIRECCIONAL" if ref_i is None or ref_i == f["proxy"] else "RELATIVO"
            hs = [h for h in f.get("horizontes_aplicables", []) if h in hz_interes]
            f["_tipo_pronostico"], f["_referencia"] = tipo_p, (None if tipo_p == "DIRECCIONAL" else ref_i)
            r = _ref(clase, f)
            por_ref[r] = f
            encargos.append({"ref": r, "clase": clase, "opp_id": f.get("opp_id"), "tesis": f["tesis"], "proxy": f["proxy"],
                             "referencia_indice": f["_referencia"], "tipo_pronostico": tipo_p, "horizontes": hs,
                             "datos": {k: v for k, v in f["senales"].items() if k != "calc_ids"},
                             "catalizadores_conocidos": f.get("catalizadores", []), "invalidacion_propuesta": f.get("invalidacion", []),
                             "certificado_r13": {h: False for h in hs},
                             "metodos_certificados_por_horizonte": {h: sorted(c["metodo"] for c in certs if c["clase"] == clase
                                                                             and c["horizonte"] == h) for h in hs}})
    if not encargos:
        return {"lotes": 0, "encargos": 0, "omitidos": []}
    if op(bloque, "prospectiva.lotes_por_perfil"):
        lotes = [[e for e in encargos if e["clase"] == c] for c in grupos if any(e["clase"] == c for e in encargos)]
    else:
        lotes = _lotes(encargos, op(bloque, "prospectiva.max_encargos_por_lote"))
    res: dict[str, dict] = {}
    n_lotes = 0

    def _llamar(lote, reintento=False):
        nonlocal n_lotes
        n_lotes += 1
        msg = {"encargos": lote, "fecha_limite_informacion": str(pd.Timestamp(as_of).date())}
        if reintento:   # QA r01 de T-101, H-04: otro encargo, que no sale de la caché HT-06 con la misma respuesta incompleta
            msg["reintento_de_cobertura"] = {"motivo": "estos encargos no volvieron en la primera llamada", "refs": [e["ref"] for e in lote]}
        bloque.mensajeria.crear("CT-12", "AG-02", "AG-10", msg, run_id=run_id, presupuesto={"uc": presupuesto.asignado.get(BOLSA_GLOBAL)})
        r = bloque._invocar("AG-10", "CT-12", msg, "PROSPECTIVA", INSTR_PROSPECTIVA, as_of, run_id, None, "prospectiva",
                            presupuesto, bolsa=BOLSA_GLOBAL)
        pedidos = {e["ref"] for e in lote}
        for x in (r.datos or {}).get("resultados", []) if r and r.datos else []:
            if isinstance(x, dict) and x.get("ref") in pedidos and x["ref"] not in res:
                res[x["ref"]] = x

    for lote in lotes:
        _llamar(lote)
    faltan = [e for e in encargos if e["ref"] not in res]
    if faltan:   # control de cobertura: una vez más, solo con lo que falta
        for lote in _lotes(faltan, op(bloque, "prospectiva.max_encargos_por_lote")):
            _llamar(lote, reintento=True)
    omitidos = []
    for r, f in por_ref.items():
        f["_prospectiva"] = res.get(r)
        if f["_prospectiva"] is None:
            f["_prospectiva_omitida"] = True
            omitidos.append(r)
    return {"lotes": n_lotes, "encargos": len(encargos), "omitidos": sorted(omitidos)}


# ======================================================================================================
# Contradictor de la selección provisional y de sus sustitutas (A-01)
# ======================================================================================================
INSTR_REFUTACION = ("Refuta de forma independiente cada tesis: objeciones graduadas (fuerte, moderada, débil) con id OBJ-<ref>-nn, "
                    "tipo, argumento, evidencia y qué la resolvería; veredicto global por tesis. Devuelve un resultado por cada «ref».")


def refutacion_global(bloque, grupos: dict[str, list[dict]], nivel: dict[str, str], as_of, run_id, presupuesto) -> dict:
    """La misma refutación de PA-05 que la V5 (objeciones con id del código, respuesta del Analista acusado y contrarréplica
    con evidencia verificable de la propia opción), pero con una llamada al Contradictor por lote para todos los tipos.
    Una opción que el Contradictor no devuelve ni en un segundo intento queda sin crítica y no se puede entregar."""
    from .orquestacion import INSTR
    todas = []
    for clase, fs in grupos.items():
        bloque._filtrar_evidencia(fs, as_of)
        todas += [(clase, f) for f in fs]
    if not todas:
        return {"criticadas": [], "sin_respuesta": []}
    peticiones = {}
    for clase, f in todas:
        peticiones[_ref(clase, f)] = {
            "ref": _ref(clase, f), "opp_id": f.get("opp_id"), "clase": clase, "nivel": nivel.get(clase),
            "afirmaciones_verificables": [{"horizonte": p.get("horizonte"), "vista": p.get("vista"), "afirmacion": p.get("afirmacion")}
                                          for p in (f.get("_prospectiva") or {}).get("pronosticos", [])],
            "evidencias": [{"fuente": p.get("fuente"), "afirmacion": p["afirmacion"], "direccion": p.get("direccion")}
                           for p in f["_piezas"]][:op(bloque, "contradictor.max_evidencias")],
            "calculos": f["senales"].get("calc_ids", [])}
    nivel_msg = "N3" if "N3" in nivel.values() else "N2"
    res: dict[str, dict] = {}

    def _llamar(lote, reintento=False):
        msg = {"peticiones": lote, "nivel": nivel_msg}
        if reintento:   # H-04
            msg["reintento_de_cobertura"] = {"motivo": "estas peticiones no volvieron en la primera llamada", "refs": [p["ref"] for p in lote]}
        bloque.mensajeria.crear("CT-13", "AG-02", "AG-11", msg, run_id=run_id, presupuesto={"uc": presupuesto.asignado.get(BOLSA_GLOBAL)})
        r = bloque._invocar("AG-11", "CT-13", msg, "REFUTACION", INSTR_REFUTACION, as_of, run_id, None, "refutacion", presupuesto,
                            bolsa=BOLSA_GLOBAL)
        pedidos = {p["ref"] for p in lote}
        for x in (r.datos or {}).get("resultados", []) if r and r.datos else []:
            if isinstance(x, dict) and x.get("ref") in pedidos and x["ref"] not in res:
                res[x["ref"]] = x

    por_lote = op(bloque, "prospectiva.max_encargos_por_lote")
    for lote in _lotes(list(peticiones.values()), por_lote):
        _llamar(lote)
    faltan = [p for r, p in peticiones.items() if r not in res]
    if faltan:
        for lote in _lotes(faltan, por_lote):
            _llamar(lote, reintento=True)
    pendientes: dict[str, list] = {}
    sin_respuesta = []
    for clase, f in todas:
        x = res.get(_ref(clase, f))
        f["_critica_pendiente"] = False
        if x is None:
            f["_refutacion"], f["_objeciones"], f["_sin_critica"] = None, [], True
            sin_respuesta.append(_ref(clase, f))
            continue
        f["_refutacion"], f["_objeciones"], f["_criticada"] = x, [], True
        for nn, o in enumerate(x.get("objeciones", []), start=1):
            oid = f"OBJ-{f['proxy']}-{nn:02d}"
            f["_objeciones"].append({"objecion_id": oid, "id_modelo": o.get("id"), "tipo": o.get("tipo"), "fuerza": o["fuerza"],
                                     "resumen": o["argumento"], "que_la_resolveria": o.get("que_la_resolveria"),
                                     "respuesta": None, "resuelta": False})
            if o["fuerza"] in ("fuerte", "moderada"):
                pendientes.setdefault(clase, []).append({"ref": f["proxy"], "objecion_id": oid, "fuerza": o["fuerza"], "argumento": o["argumento"],
                                                         "que_la_resolveria": o.get("que_la_resolveria"), "dimensiones_E": f["dimensiones"].get("E"),
                                                         "evidencia_disponible": bloque._evidencia_verificable(f)})
    replicas = []
    for clase, pend in pendientes.items():   # el Analista acusado responde: una llamada por tipo, con su kit
        agente = AGENTE_CLASE[clase]
        msg2 = {"clase": clase, "fase": "RESPUESTA_OBJECIONES", "nivel": nivel.get(clase), "opciones_vigentes": [], "lecciones": [],
                "objeciones": pend}
        bloque.mensajeria.crear("CT-06", "AG-02", agente, msg2, run_id=run_id, presupuesto={"uc": presupuesto.asignado.get(clase)})
        r2 = bloque._invocar(agente, "CT-06", msg2, "RESPUESTA_OBJECIONES", INSTR["RESPUESTA_OBJECIONES"], as_of, run_id, clase,
                             "respuesta_objeciones", presupuesto)
        resp = {x["objecion_id"]: x for x in (r2.datos or {}).get("respuestas", [])} if r2 and r2.datos else {}
        for f in grupos[clase]:
            verificables = set(bloque._evidencia_verificable(f))
            for o in f.get("_objeciones", []):
                x = resp.get(o["objecion_id"])
                if x and (x.get("respuesta") or "").strip():
                    o["respuesta"] = x["respuesta"]
                    if o["fuerza"] != "fuerte":
                        o["resuelta"] = True
                        continue
                    citada = [str(e) for e in (x.get("evidencia_citada") or []) if str(e) in verificables]
                    o["evidencia_citada"] = citada
                    if x.get("resuelta") and citada:
                        replicas.append({"ref": f["proxy"], "objecion_id": o["objecion_id"], "argumento": o["resumen"],
                                         "que_la_resolveria": o.get("que_la_resolveria"), "respuesta": x["respuesta"],
                                         "evidencia_citada": [bloque._contenido_evidencia(f, e, run_id) for e in citada]})
    if replicas:
        msg3 = {"peticiones": [], "contrarreplicas": replicas, "nivel": nivel_msg}
        bloque.mensajeria.crear("CT-13", "AG-02", "AG-11", msg3, run_id=run_id, presupuesto={"uc": presupuesto.asignado.get(BOLSA_GLOBAL)})
        r3 = bloque._invocar("AG-11", "CT-13", msg3, "CONTRARREPLICA", INSTR["CONTRARREPLICA"], as_of, run_id, None, "refutacion",
                             presupuesto, bolsa=BOLSA_GLOBAL)
        enviadas = {x["objecion_id"] for x in replicas}
        conf = {x["objecion_id"]: x for x in (r3.datos or {}).get("resultados", [])
                if isinstance(x, dict) and x.get("objecion_id") in enviadas} if r3 and r3.datos else {}
        for _, f in todas:
            for o in f.get("_objeciones", []):
                if o["fuerza"] == "fuerte" and o["objecion_id"] in conf:
                    o["resuelta"] = conf[o["objecion_id"]].get("resuelta") is True
                    o["contrarreplica"] = str(conf[o["objecion_id"]].get("motivo") or "")[:op(bloque, "contradictor.contrarreplica_max")]
    for _, f in todas:
        if f.get("_refutacion") is not None:
            f["_veredicto"] = bloque._veredicto_refutacion(f)
            f["_veredicto_contradictor"] = (f.get("_refutacion") or {}).get("veredicto_global")
    return {"criticadas": sorted(_ref(c, f) for c, f in todas if f.get("_criticada")), "sin_respuesta": sorted(sin_respuesta)}


def _top3(sel: dict) -> set[str]:
    return {t["opp_id"] for t in sel["seleccion"]["top3"]}


def seleccion_con_critica(bloque, clases, analisis, clusteres, nivel, as_of, run_id, hz_interes, presupuesto) -> tuple[dict, dict]:
    """A-01: selección provisional → crítica → selección final. Las finalistas nuevas de un tipo N2/N3 llegan a la selección
    provisional con la crítica pendiente; el Contradictor critica las que quedan en algún top-3; si alguna cae, la que entra
    pasa la misma crítica, hasta `v6.contradictor.max_rondas_sustitucion` rondas de sustitución. Al final, lo que no se ha
    podido criticar deja de ser elegible y no se entrega."""
    if not activo(bloque, "contradictor.solo_seleccion"):
        raise ValueError("v6.contradictor.solo_seleccion: false no está soportado con la Prospectiva global")
    for c in clases:
        if nivel[c] in ("N2", "N3"):
            for f in analisis[c]["finalistas"]:
                if f.get("_gc3") and f.get("_refutacion") is None:
                    f["_critica_pendiente"] = True

    def _seleccionar_todo():
        sel = {c: bloque._seleccionar(c, analisis[c], clusteres, as_of, run_id, hz_interes) for c in clases}
        bloque._deduplicar_entre_tipos(sel)
        return sel

    rondas = []
    max_rondas = int(op(bloque, "contradictor.max_rondas_sustitucion"))
    sel = _seleccionar_todo()
    for ronda in range(max_rondas + 1):
        grupos = {c: [f for f in sel[c]["candidatos"] if f["opp_id"] in _top3(sel[c]) and f.get("_critica_pendiente")] for c in clases}
        grupos = {c: fs for c, fs in grupos.items() if fs}
        if not grupos:
            break
        r = refutacion_global(bloque, grupos, nivel, as_of, run_id, presupuesto)
        rondas.append({"ronda": ronda, "tipo": "PROVISIONAL" if ronda == 0 else "SUSTITUCION", **r})
        sel = _seleccionar_todo()
    # Lo que sigue con la crítica pendiente deja de ser elegible; se declara lo que, por eso, no se entrega (estaba en un top-3)
    sin_critica: list[dict] = []
    no_criticadas: list[dict] = []
    for c in clases:
        top = _top3(sel[c])
        for f in analisis[c]["finalistas"]:
            if f.get("_critica_pendiente"):
                f["_critica_pendiente"], f["_sin_critica"] = False, True
                (sin_critica if f.get("opp_id") in top else no_criticadas).append({"clase": c, "proxy": f["proxy"], "opp_id": f.get("opp_id")})
    # QA r01 de T-101, H-03: lo que se envió al Contradictor (estaba en un top-3) y no volvió en dos intentos no se entrega
    # y se declara, aunque ya no sea elegible
    sin_respuesta = sorted({r for ronda in rondas for r in ronda.get("sin_respuesta", [])})
    if sin_critica:
        sel = _seleccionar_todo()
    return sel, {"rondas": rondas, "sin_critica": sin_critica, "sin_respuesta": sin_respuesta,
                 "no_criticadas_fuera_del_top3": no_criticadas}


# ======================================================================================================
# Integración determinista (antes de G3) y Sintetizador (después)
# ======================================================================================================
def integracion_determinista(bloque, seleccion, analisis, as_of) -> dict:
    """La integración que hacía el Analizador (AG-02), sin modelo: el régimen de cada tipo y los cambios frente al run
    anterior. La lectura del conjunto y los factores los escribe el Sintetizador sobre el paquete ya validado."""
    reg = [f"{NOMBRE_CLASE[c]}: {analisis[c].get('regimen')}" for c in seleccion if (analisis[c].get("regimen") or "").strip()]
    anterior = [r for r in bloque.almacen.leer("F5", as_of) if r.get("tipo_entrada") == "RUN"]
    previo = (anterior[-1].get("top3_por_clase") if anterior else None) or {}
    cambios = []
    for c, s in seleccion.items():
        ahora_ids = [t["opp_id"] for t in s["seleccion"]["top3"]]
        antes = [x if isinstance(x, str) else x.get("opp_id") for x in (previo.get(c) or [])]
        entran, salen = [x for x in ahora_ids if x not in antes], [x for x in antes if x and x not in ahora_ids]
        if entran or salen:
            cambios.append(f"{NOMBRE_CLASE[c]}: entran {', '.join(entran) or 'ninguna'}; salen {', '.join(salen) or 'ninguna'}")
    return {"regimen_macro": ("; ".join(reg) if reg else "Régimen por tipo no disponible en este ciclo")[:op(bloque, "sintetizador_limites")["regimen"]],
            "factores_dominantes": [], "lectura_conjunto": "Integración determinista (diseño V6): la lectura del conjunto la "
            "escribe el Sintetizador sobre el paquete validado.", "preguntas_sugeridas": [], "limitaciones": [],
            "cambios_vs_anterior": "; ".join(cambios) if cambios else "Sin cambios en los top-3 frente al run anterior."}


INSTR_SINTESIS = ("Sobre el paquete ya validado: escribe la integración (régimen macro común, el factor que domina cada clúster, "
                  "la lectura del conjunto, preguntas sugeridas para el Broker y limitaciones) y los textos llanos del informe "
                  "visual (exactamente dos frases para «la semana en 30 segundos»: el código pone delante una tercera, con las cuentas; por cada opción «por qué» y «qué podría salir mal» "
                  "(≤ 20 palabras, sin jerga o explicada entre paréntesis), motivos llanos de los tipos sin tres opciones, un "
                  "glosario de hasta 5 términos y una frase honesta sobre el historial). Índice Fernández-Huerta ≥ 70. No cambies "
                  "la selección ni las cifras: vienen calculadas y validadas. Regla de escritura (§4 del prompt): NO escribas "
                  "ninguna cifra ni ningún código de un activo concreto; para nombrar una opción usa {opp:OPP-…}, para un tipo "
                  "{tipo:RV}: el código los rellena. No cuentes: las cuentas (ideas, tipos, apuestas, candidatas) las escribe el código. "
                  "Una frase con una cifra, también en letra, un código de un activo o un marcador desconocido o de cuenta se quita.")
_CAMPOS_REDACCION = ("frases_30s", "tarjetas", "motivos_llanos", "glosario", "frase_historial")


# Filtro de los textos del Sintetizador. T-102 ronda r03 (decisión del operador del 12-11-2026, tras tres rondas de QA en que
# un filtro de patrones sobre texto libre no convergía): el Sintetizador escribe con MARCADORES que rellena el código, y su
# texto libre sigue una regla estricta que no depende de cómo se redacte. Se aplica FRASE A FRASE: una frase que la incumple
# se quita (falla cerrado), el resto del texto se conserva con sus separadores y lo quitado se declara.
# - Marcadores: {opp:OPP-…} (el nombre llano de la opción), {tipo:RV} (el nombre del tipo de activo), {n:RV} (opciones del
#   tipo), {candidatas:RV} (ideas analizadas del tipo), {n_ideas}, {n_tipos} y {n_apuestas}. Uno desconocido o mal formado, o
#   una llave suelta, quita la frase (MARCADOR).
# - CIFRA: ninguna cifra en el texto libre (protege R13 y R21: sin cifras no hay probabilidad numérica, ISIN, ticker con
#   números ni vencimiento); tampoco «por ciento», «N de cada M» en letra ni una fracción junto a una palabra de probabilidad.
# - R21: ningún código en mayúsculas que sea un instrumento (todo lo que no sea un código de `v6.filtro_r21_codigos`, una
#   calificación, un par de divisas o una serie del universo), esté donde esté y con o sin verbo; ningún sufijo societario o
#   de fondo («Inc», «plc», «S.A.», «FI»); ninguna selección unitaria (`sintesis._UNITARIA`).
# Límite declarado: un nombre propio sin código ni sufijo («Tesla») no se detecta; con los marcadores el Sintetizador no
# necesita escribir ninguno, y lo revisa el Auditor por muestreo.
_MARCADOR = re.compile(r"\{(?:(opp|tipo|n|candidatas):([A-Za-z0-9-]{1,40})|(n_ideas|n_tipos|n_apuestas))\}")
_MARCADOR_NUM = re.compile(r"\{(?:(?:n|candidatas):[A-Za-z0-9-]{1,40}|n_ideas|n_tipos|n_apuestas)\}")
_LLAVE = re.compile(r"[{}]")
# T-102 r04 (QA r03, H-20): una cifra es cualquier carácter numérico de Unicode (categorías Nd, No y Nl: «⁷», «⅔», «Ⅶ»)
# T-102 r06 (decisión del operador del 13-11-2026, tras la QA r05): los marcadores numéricos ({n:…}, {candidatas:…},
# {n_ideas}, {n_tipos}, {n_apuestas}) ya no valen en el texto libre: dos marcadores juntos componían cifras que no están en
# el paquete («{n:RV},{n:RF}» da «1,3»; H-42). Las cuentas las escribe el código en frases propias (`_frases_del_codigo`).
# T-102 r05 y r06: un número en letra es una cifra en cualquier frase. «uno»/«una», «medio», «mitad», «doble» y los ordinales
# solo cuentan en las formas que expresan una cantidad: «una de cada», «un cuarto de», «una cuarta parte», «y medio», «la
# mitad de las ideas», «el doble de». No cuentan «a corto y medio plazo», «un medio de cobertura», «el doble mandato», «en
# mitad de la tormenta», «Oriente Próximo y Medio» ni «un quinto mes» (H-40).
_NUM_LETRA = (r"(?:cero|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|trece|catorce|quince|dieci\w+|veinte|"
              r"veinti\w+|treinta|cuarenta|cincuenta|sesenta|setenta|ochenta|noventa|cien|ciento|\w*cient[oa]s|quinient[oa]s|"
              r"setecient[oa]s|novecient[oa]s|mil|millones?|mill[oó]n|millar(?:es)?|tercios?|docenas?|decenas?|centenar(?:es)?|"
              r"mil[eé]sim[oa]s?|cent[eé]sim[oa]s?|\w+(?:ceav|teav|ntav)[oa]s?|"
              # r06 (H-43): en inglés, que el Sintetizador no debe usar y que nunca es un giro español
              r"two|three|four|five|six|seven|eight|nine|ten|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|"
              r"thousand|percent|fifty-fifty)")
_UNO = r"(?:un[oa]?)"
_FIN_CANTIDAD = r"(?=\s+(?:del?|al|en|por|m[aá]s|menos|sobre)\b|\s*[.,;:)]|\s*$)"   # «un cuarto de…», «una décima al mes»; no «un quinto mes»
_CIFRA_EN_LETRA = re.compile(   # «%», «‰» o «٪» se miran por su nombre Unicode; «por ciento» ya es un número en letra
    rf"\b{_NUM_LETRA}\b"
    rf"|\b{_UNO}\s+(?:sobre|entre|de\s+cada|contra|en|a|por\s+cada)\s+{_UNO}\b"   # «una de cada una», «uno a uno»
    rf"|\b{_UNO}\s+(?:cuart|quint|sext|s[eé]ptim|octav|noven|d[eé]cim)[oa]s?\b{_FIN_CANTIDAD}"   # «un cuarto de», «una décima.»
    r"|\b(?:tercera|cuarta|quinta|sexta|s[eé]ptima|octava|novena|d[eé]cima)s?\s+partes?\b"
    r"|\by\s+(?-i:medio)\b(?!\s+plazo)|\bmedio\s+punto\b|\bmedia\s+docena\b"
    r"|\bel\s+(?:doble|triple|cu[aá]druple)\b(?=\s+(?:de|que)\b|\s*[.,;:)]|\s*$)"
    r"|(?<!primera\s)(?<!segunda\s)(?<!\ba\s)(?<!\ben\s)\bmitad\b(?!\s+del?\s+(?:año|ciclo|mes|semana|trimestre|semestre|"
    r"camino|periodo|década|sesión|jornada))", re.IGNORECASE)
# T-102 r04 (QA r03, H-21): el sufijo también con punto («Apple Inc.»); y no tras un artículo («Las SICAV», H-25)
# r05 (QA r04, H-32 y H-37) y r06 (QA r05, H-44): sufijos de sociedad y de fondo, en mayúscula o en minúscula, con o sin
# punto. Cada palabra del nombre empieza donde no hay otra letra y tiene un tope de longitud (lineal). Un determinante
# no es un nombre («Cada ETF», «Ningún ETF»); un infinitivo al abrir la frase solo se exceptúa delante de un sufijo de
# fondo («Sobreponderar ETF»), no de uno de sociedad («Pfizer Inc.», «Schlumberger Ltd.»).
_DETERMINANTE = (r"(?:El|La|Los|Las|Un|Una|Unos|Unas|Estas?|Estos|Esos?|Esas?|Aquel(?:la|los|las)?|Sus?|Varios|Varias|"
                 r"Algunos|Algunas|Muchos|Muchas|Pocos|Pocas|Otros?|Otras?|Ambos|Ambas|Nuestros?|Nuestras?|Cada|Tod[oa]s?|"
                 r"Cualquier|Ning[uú]n|Ninguna|Ciertos?|Ciertas?|Dichos?|Dichas?|Mismos?|Mismas?|Tal(?:es)?)")
_NOMBRE = r"(?<![\w&.-])[A-Z][\w&.-]{0,40}(?:\s+[A-Z][\w&.-]{0,40}){0,6},?\s+"
_SUF_SOCIEDAD = (r"(?:Corp|Corporation|Inc|Incorporated|Ltd|Ltda|Limited|plc|PLC|Plc|AG|NV|N\.V|SE|S\.A|SA|S\.p\.A|SpA|GmbH|"
                 r"LLC|KGaA|Oyj|Bhd|Group|Holdings?|Aktiengesellschaft|Co(?=\.)|FI|FIL|SICAV|Sicav|SOCIMI|Socimi|"
                 r"(?i:inc|corp|corporation|incorporated|ltd|ltda|limited|spa|gmbh|llc|plc|sicav|socimi|kgaa|oyj|bhd))\.?(?!\w)")
_SUF_FONDO = r"(?:Fund|Trust|UCITS\s+ETF|ETF|ETC|ETP)\.?(?!\w)"
_SUFIJO = re.compile(rf"(?!{_DETERMINANTE}\b){_NOMBRE}{_SUF_SOCIEDAD}"
                     rf"|(?!{_DETERMINANTE}\b)(?!(?<=\A)[A-Z][a-záéíóú]+(?:ar|er|ir)\b){_NOMBRE}{_SUF_FONDO}"
                     r"|(?<![\w&.-])[a-z][\w&-]{0,40}\s+(?:inc|corp|corporation|incorporated|ltd|ltda|plc|llc|gmbh|"
                     r"(?:co|spa|ag|nv)(?=\.))\.?(?!\w)")
_CODIGO = re.compile(r"(?<![\w&.^=-])\$?([A-Z][A-Z0-9&.^=/-]{1,14})(?![\w&])")
# H-22: un código tras «_», «-» o «=» también cuenta (la variante de arriba no lo ve)
_CODIGO_PEGADO = re.compile(r"(?:[_=]|(?<=[a-záéíóúñ])[-.])([A-Z]{2,6})(?![\w&])|\$([A-Za-z]{1,6})\b")
# H-22: tras un vehículo, el código puede ir en minúscula o tener una sola letra («el ETF qqq», «el REIT O»)
_VEHICULO = re.compile(r"\b(?:ETF|ETP|ETN|ETC|REIT|SOCIMI|fondo|ticker|s[ií]mbolo|acci[oó]n(?:es)?\s+de|futuros?\s+(?:de|sobre)|"
                       r"opci[oó]n(?:es)?\s+(?:de|sobre))\s+([A-Za-z][A-Za-z0-9.]{0,6})(?![\w&])")
# r06 (QA r05, H-41): palabras corrientes que siguen a «ETF», «fondo» o «REIT» y no son un ticker en minúscula
_PALABRA_COMUN = frozenset({"de", "del", "la", "el", "los", "las", "que", "en", "con", "por", "sobre", "más", "mas", "y", "o", "a",
                            "al", "un", "una", "su", "sus", "este", "esta", "ese", "esa", "como", "para", "sin", "no", "se",
                            "es", "son", "era", "fue", "va", "van", "ha", "han", "hay", "sube", "suben", "cae", "caen", "gana",
                            "ganan", "baja", "bajan", "paga", "pagan", "pesa", "pesan", "rinde", "sigue", "muy", "bien",
                            "mal", "ya", "aún", "solo", "sólo", "tiene", "puede", "debe", "deben", "mejor", "peor", "menos",
                            "tanto", "otro", "otra", "cada", "todo", "toda", "e", "u", "ni", "pero", "si", "sí", "tras", "hoy",
                            "nunca", "casi", "algo", "le", "les", "lo", "nos", "cuyo", "cuya"})
_CALIFICACION = re.compile(r"(?:AAA|AA|A|BBB|BB|B|CCC|CC|C|D)[+-]?")
_CONTEXTO_CALIFICACION = re.compile(r"\b(?:cr[eé]dito|calificaci[oó]n|rating|grado|bonos?|deuda|emisor(?:es)?|tramo)\b", re.IGNORECASE)
# Abreviaturas que llevan punto y no acaban la frase: se protegen antes de dividir
_ABREV = re.compile(r"\b(?:EE\.\s?UU|S\.\s?A|S\.\s?L|p\.\s?ej|etc|Inc|Corp|Ltd|Sr|Sra|Dr|núm|aprox|vs|pág)\.(?=\s|$|[,;:)])")
_PUNTO = "․"
# H-26: sin cuantificadores que se solapen (antes, cuadrático con muchos espacios seguidos)
_SEPARADOR = re.compile(r"((?<=[.;!?…])\s+|(?<![^\S\n])[^\S\n]*+\n\s*+)")


_MARCA_ESPANOLA = {"\u0301": "aeiouAEIOU", "\u0303": "nN", "\u0308": "uU"}   # tilde en vocal, ñ, ü


def _sin_marcas(t: str) -> str:
    """Quita las marcas combinantes, también las de una letra compuesta («Ṅ», «N̲»), salvo las del español (á, ñ, ü)."""
    out: list[str] = []
    for ch in unicodedata.normalize("NFKD", t):
        if unicodedata.category(ch) in ("Mn", "Me"):
            if out and out[-1] in _MARCA_ESPANOLA.get(ch, ""):
                out.append(ch)
            continue
        out.append(ch)
    return "".join(out)


def _hay_cifra(t: str) -> bool:
    return any(unicodedata.category(ch).startswith("N") for ch in t)


def _es_instrumento(cod: str, perm, contexto: str = "") -> bool:
    """Un código en mayúsculas es un instrumento concreto salvo que sea un código permitido (divisa, tipo de activo, sigla de
    índice, región, materia prima o segmento), una calificación crediticia, un par de divisas permitidas con o sin barra
    («EURUSD», «EUR/USD») o una serie del universo que no es un ticker de fondo."""
    c = cod.lstrip("$").rstrip(".")
    if c in perm["codigos"] or c in perm["series"] or re.fullmatch(r"X{0,3}(?:IX|IV|V?I{0,3})", c):   # «siglo XXI»
        return False
    if _CALIFICACION.fullmatch(c):   # H-22: una calificación solo lo es junto a «crédito», «rating», «bonos»…
        return not _CONTEXTO_CALIFICACION.search(contexto)
    partes = c.split("/")
    if len(partes) == 2 and all(x in perm["codigos"] for x in partes):
        return False
    if len(c) == 6 and c.isalpha() and c[:3] in perm["codigos"] and c[3:] in perm["codigos"]:
        return False
    return any(ch.isupper() for ch in c) and len(c) >= 2


def _clave(m) -> str:
    return f"{m.group(1)}:{m.group(2)}" if m.group(1) else m.group(3)


def marcadores(paquete: dict, perm=None) -> dict[str, str]:
    """Lo que vale cada marcador de texto en este paquete ({opp:…} y {tipo:…}). Desde la r06 no hay marcadores de cuenta en el
    texto libre: las cuentas las escribe el código (`_cuenta_motivo` y la primera frase de 30 s). Con `perm`, un
    `nombre_llano` que incumpliría la regla (lo escribe un Analista) se cambia por «esta idea» (r04, H-27)."""
    out: dict[str, str] = {}
    for c, d in (paquete.get("clases") or {}).items():
        out[f"tipo:{c}"] = NOMBRE_CLASE.get(c, c).lower()
        for o in d.get("opciones") or []:
            nombre = str(o.get("nombre_llano") or "esta idea")
            if perm is not None and frase_prohibida(nombre, perm):
                nombre = "esta idea"
            out[f"opp:{o['opp_id']}"] = nombre
    return out


def frase_prohibida(t: str, perm, marcas: dict | None = None) -> str | None:
    """«MARCADOR», «CIFRA», «R21» o None para UNA frase (ya normalizada con NFKC por `limpiar`). Con `marcas`, un marcador que
    no está en este paquete también quita la frase; sin ellas (pruebas unitarias), basta con que esté bien formado."""
    # r05 (QA r04, H-33): fuera los caracteres de formato (espacio de ancho cero, guion blando, unión de palabras), que parten
    # un código sin que se vea («N\u200bV\u200bD\u200bA» se lee «NVDA»)
    orig = "".join(ch for ch in t.replace(_PUNTO, ".") if unicodedata.category(ch) != "Cf")
    if _hay_cifra(_MARCADOR.sub(" ", orig)):   # antes de normalizar: «Ⅶ» pasaría a ser «VII», letras
        return "CIFRA"
    # r06 (QA r05, H-46): fuera también las marcas combinantes, también las de una letra compuesta («ṄVDA», «N̲V̲D̲A»)
    t = unicodedata.normalize("NFKC", _sin_marcas(orig))
    if marcas is not None and any(_clave(m) not in marcas for m in _MARCADOR.finditer(t)):
        return "MARCADOR"
    if _MARCADOR_NUM.search(t):   # r06 (H-42): las cuentas las escribe el código, no el texto libre
        return "MARCADOR"
    libre = _MARCADOR.sub(" ", t)
    if _LLAVE.search(libre) or any("CURLY BRACKET" in unicodedata.name(ch, "") for ch in libre):   # también «❴ ❵»
        return "MARCADOR"
    if re.search(r"\b(?:n_ideas|n_tipos|n_apuestas)\b|\b(?:opp|tipo|n|candidatas):[A-Za-z0-9-]", libre):   # r05: «〔n_ideas〕»
        return "MARCADOR"
    if _hay_cifra(libre) or _CIFRA_EN_LETRA.search(libre) \
            or any(("PERCENT" in unicodedata.name(ch, "") or "PER MILLE" in unicodedata.name(ch, "")) for ch in libre):   # «٪»
        return "CIFRA"
    if _SUFIJO.search(libre.lstrip(" \t-•*")):
        return "R21"
    for m in sint._UNITARIA.finditer(libre):
        # r06 (QA r05, H-41): «la acción de los bancos centrales» o «el bono de referencia» no nombran un título concreto
        if m.group(0).rstrip().lower().endswith(" de") and re.match(r"\s*[a-záéíóúñ]", libre[m.end():]):
            continue
        return "R21"
    libre = re.sub(r"\bEE\.\s?UU\.", "EEUU", libre)
    # r04 (H-22) y r05 (QA r04): una letra de otro alfabeto (griego, cirílico, cheroqui: posibles homoglifos), una versalita o
    # un indicador regional en un texto en español falla cerrado («ΝVDA», «ᏚᏢᎩ», «ɴᴠᴅᴀ», «🇳🇻🇩🇦»)
    if any((unicodedata.category(ch).startswith("L") and "LATIN" not in unicodedata.name(ch, ""))
           or any(x in unicodedata.name(ch, "") for x in ("SMALL CAPITAL", "REGIONAL INDICATOR", "MODIFIER LETTER", "SQUARED LATIN",
                                                          "CIRCLED LATIN", "PARENTHESIZED LATIN")) for ch in libre):
        return "R21"   # r04 (H-22): letras de otros alfabetos en un texto en español: posible homoglifo, falla cerrado
    # r06 (QA r05, H-46): letras sueltas en mayúscula separadas por espacios, «_» o el blanco Braille («N V D A», «N_V_D_A»)
    if re.search(r"(?<![\w])[A-Z](?:[\s_\u2800·‧∙•.\-/][A-Z]){2,}(?![\w])", libre):   # T-113 (H-53): también «N·V·D·A»
        return "R21"
    codigos = _CODIGO.findall(libre) + [a or b for a, b in _CODIGO_PEGADO.findall(libre)]
    if any(m.startswith("$") or _es_instrumento(m, perm, libre) for m in codigos) or any(
            b for _, b in _CODIGO_PEGADO.findall(libre)):
        return "R21"
    # r04 (H-22): mayúsculas y minúsculas mezcladas como un código («AApl»); no los plurales de una sigla («ETFs», «REITs»)
    for m in re.finditer(r"\b([A-Z]{2,})([a-z]+)\b", libre):
        if not (m.group(2) == "s" and m.group(1) in perm["codigos"]):
            return "R21"
    for m in re.finditer(r"\b(?:acci[oó]n|valor|t[ií]tulo)\s+([a-z][a-z0-9]{0,5})\b", libre):   # T-113 (H-34)
        if m.group(1).upper() in perm.get("tickers", ()) and m.group(1) not in _PALABRA_COMUN:
            return "R21"
    # T-113 (T-109): un número romano como cantidad («las VII ideas») es una cifra; tras un nombre propio («Basilea III»,
    # «Solvencia II») o «siglo» sigue siendo un nombre
    if re.search(r"\b(?:[Ll]os|[Ll]as|[Uu]nos|[Uu]nas|[Ss]us|[Ee]stos|[Ee]stas|[Ee]sos|[Ee]sas)\s+(?=[IVXLC]{2,}\b)(?:X{0,3})(?:IX|IV|V?I{0,3})\b",
                 libre):
        return "CIFRA"
    for m in _VEHICULO.finditer(libre):
        c = m.group(1).rstrip(".")   # r06 (H-44): «el fondo vwrl.»
        if not c or (c.islower() and c in _PALABRA_COMUN) or (c[0].islower() and len(c) > 5):
            continue
        # la minúscula solo tras un vehículo que se nombra por su ticker (no tras «opciones de», «acciones de» o «fondo»)
        por_ticker = bool(re.match(r"(?:ETF|ETP|ETN|ETC|REIT|SOCIMI|ticker|s[ií]mbolo)\b", m.group(0)))
        # r05 (H-36) y r06 (H-44): una palabra con mayúscula inicial es un nombre («acciones de Europa») salvo tras un vehículo
        # que se nombra por su ticker («el ETF Nvda», «el REIT Realty»)
        if not por_ticker and len(c) >= 3 and c[0].isupper() and c[1:].islower():
            continue
        ticker = por_ticker or (m.group(0).lower().startswith("fondo") and len(c) <= 4)
        if c.upper() not in perm["codigos"] and ((c.islower() and ticker) or (len(c) == 1 and c.isupper())
                                                 or (por_ticker and c[0].isupper() and c[1:].islower())
                                                 or (not c.islower() and _es_instrumento(c, perm, libre))):
            return "R21"
    return None


def rellenar(t: str, marcas: dict) -> str:
    """Sustituye los marcadores por su valor (después de filtrar: lo que pone el código no se filtra)."""
    return _MARCADOR.sub(lambda m: marcas.get(_clave(m), m.group(0)), t)


def _trozos(t: str) -> list[str]:
    """[frase, separador, frase, separador, …]: se divide por «.», «;», «!», «?», «…» y saltos de línea, sin partir las
    abreviaturas (H-04); los separadores se conservan para volver a juntar el texto tal cual."""
    protegido = _ABREV.sub(lambda m: m.group(0).replace(".", _PUNTO), t)
    return _SEPARADOR.split(protegido)


def _frases(t: str) -> list[str]:
    return [x for x in _trozos(t.strip())[::2] if x.strip()]


def texto_prohibido(t, permitidos=None, marcas: dict | None = None) -> str | None:
    """La primera regla que incumple alguna frase del texto, o None."""
    if not isinstance(t, str):
        return None
    perm = permitidos if isinstance(permitidos, dict) else {"codigos": frozenset(permitidos or ()), "series": frozenset()}
    return next((r for r in (frase_prohibida(f, perm, marcas) for f in _frases(t)) if r), None)


def limpiar(t, perm, marcas: dict | None = None) -> tuple[str, list[str]]:
    """El texto sin las frases que incumplen la regla (cada una con el separador que la sigue) y con los marcadores
    rellenados (si se dan `marcas`), y las reglas incumplidas. Un texto sin nada prohibido ni marcadores sale igual."""
    if not isinstance(t, str):
        return t, []
    trozos = _trozos(t)
    quedan, reglas = [], []
    for k in range(0, len(trozos), 2):
        f, sep = trozos[k], (trozos[k + 1] if k + 1 < len(trozos) else "")
        r = frase_prohibida(f, perm, marcas) if f.strip() else None
        if r:
            reglas.append(r)
        else:
            quedan.append(f + sep)
    salida = t if not reglas else "".join(quedan).replace(_PUNTO, ".").strip()
    if reglas and salida[:1].islower():   # T-113 (H-49): lo que queda tras quitar la frase de delante empieza en mayúscula
        salida = salida[0].upper() + salida[1:]
    # H-28: con marcas, la salida se normaliza con NFKC antes de rellenar («｛n_ideas｝» es «{n_ideas}»)
    return (rellenar(unicodedata.normalize("NFKC", salida), marcas) if marcas is not None else salida), reglas


def permitidos_r21(bloque) -> dict:
    """Los códigos de la configuración (`v6.filtro_r21_codigos`) y las series del universo que no son tickers de fondo."""
    simbolos = set(bloque.universo["simbolo"].astype(str))
    if "subyacente" in bloque.universo:
        simbolos |= {str(x) for x in bloque.universo["subyacente"].dropna()}
    # T-102 r02 (H-02): un símbolo con sufijo de bolsa («XEON.DE», «ITX.MC») es un fondo o una acción, no una serie
    # T-102 r03 (QA r02, H-17): un token frente a una divisa («BTC-USD», «SOL-USD») es un instrumento concreto, no una serie
    series = {x for x in simbolos if (re.search(r"[=^\-\d/]", x) or len(x) > 5) and not re.fullmatch(r"[A-Z0-9]{1,6}\.[A-Z]{1,3}", x)
              and not re.fullmatch(r"[A-Z0-9]{2,10}-(?:USD|EUR|USDT|USDC|BTC)", x)}
    series |= {x.split("=")[0] for x in simbolos if "=" in x}   # «EURUSD=X» también como «EURUSD»
    # T-113 (H-34 de T-109): los tickers del universo (sin sufijo de bolsa), para cazarlos en minúscula tras «la acción», «el
    # valor» o «el título»; uno que no está en el universo sigue siendo un límite declarado
    tickers = {x.split(".")[0] for x in simbolos if x not in series and re.fullmatch(r"[A-Z0-9]{1,6}(?:\.[A-Z]{1,3})?", x)}
    return {"codigos": frozenset(str(x) for x in op(bloque, "filtro_r21_codigos")), "series": frozenset(series),
            "tickers": frozenset(tickers)}


def _textos(x) -> list:
    if isinstance(x, str):
        return [x]
    if isinstance(x, dict):
        return [t for v in x.values() for t in _textos(v)]
    if isinstance(x, list):
        return [t for v in x for t in _textos(v)]
    return []


def _aplicar_integracion(paquete: dict, d: dict, lim: dict, permitidos=None) -> list[str]:
    """Solo se toman textos (el Sintetizador no puede cambiar la selección, las puntuaciones, las fechas ni las cifras), con las
    longitudes de `v6.sintetizador_limites`; de cada texto se quitan las frases que incumplen la regla y se rellenan los
    marcadores. Devuelve lo quitado."""
    perm = permitidos or {"codigos": frozenset(), "series": frozenset()}
    marcas = marcadores(paquete, perm)
    descartados: list[str] = []

    def _limpio(campo, t):
        if not isinstance(t, str):
            return None
        t2, reglas = limpiar(t, perm, marcas)
        descartados.extend(f"{campo} ({r})" for r in reglas)
        return t2.strip() if len(t2.strip()) >= lim["texto_minimo"] else None
    reg = _limpio("regimen_macro", d.get("regimen_macro"))
    if reg:
        paquete["regimen_macro"] = reg[:lim["regimen"]]
    fact = {}
    for x in d.get("factores_dominantes") or []:
        if isinstance(x, dict):
            t = _limpio("factores_dominantes", x.get("factor"))
            if t:
                fact[str(x.get("cluster_id"))] = t
    for c in paquete.get("clusteres_exposicion", []):
        if c["cluster_id"] in fact:
            c["factor_dominante"] = fact[c["cluster_id"]][:lim["factor"]]
    preg = [t for t in (_limpio("preguntas_sugeridas", x) for x in d.get("preguntas_sugeridas") or []) if t][:lim["preguntas"]]
    if preg:
        paquete["preguntas_sugeridas"] = preg
    lec = _limpio("lectura_conjunto", d.get("lectura_conjunto"))
    if lec:
        paquete["x_lectura_conjunto"] = lec[:lim["lectura"]]
    nuevas = [f"Sintetizador: {t}"[:lim["limitacion"]] for t in (_limpio("limitaciones", x) for x in d.get("limitaciones") or []) if t]
    nuevas = nuevas[:lim["limitaciones"]]
    if descartados:
        nuevas.append(f"Frases del Sintetizador quitadas (cifras, códigos de instrumento o marcadores): {len(descartados)} ("
                      + ", ".join(dict.fromkeys(descartados)) + ")")
    if nuevas:
        paquete["limitaciones"] = [x for x in paquete["limitaciones"] if not x.startswith("Ninguna limitación")] + nuevas
    return descartados


def _cuenta_motivo(paquete: dict, clase: str) -> str:
    """La frase con las cuentas de un tipo, escrita por el código con datos del paquete (T-102 r06)."""
    d = (paquete.get("clases") or {}).get(clase) or {}
    n, cand = len(d.get("opciones") or []), int(d.get("candidatas_analizadas") or 0)
    tipo = NOMBRE_CLASE.get(clase, clase).lower()
    ideas = "idea" if cand == 1 else "ideas"
    analizadas = "analizada" if cand == 1 else "analizadas"
    return f"De {cand} {ideas} de {tipo} {analizadas}, {n} {'pasó' if n == 1 else 'pasaron'} todos los filtros."


def _redaccion_segura(bloque, paquete, d, permitidos=None) -> dict:
    """Los textos llanos del Sintetizador, frase a frase: una frase que incumple R13 o R21 se quita; si un texto se queda vacío,
    toma el texto por defecto de ese mismo elemento (no de todos). Se declara cuántas frases se quitaron (T-102)."""
    defecto = bloque.redaccion.textos_por_defecto(paquete)
    if not d:
        return defecto
    perm = permitidos or {"codigos": frozenset(), "series": frozenset()}
    marcas = marcadores(paquete, perm)
    red = copy.deepcopy({k: d[k] for k in _CAMPOS_REDACCION})
    quitadas: list[str] = []

    def _uno(t, por_defecto):
        t2, reglas = limpiar(t, perm, marcas)
        quitadas.extend(reglas)
        return t2 if not reglas else (t2.strip() or por_defecto)
    # r06 (decisión del operador, H-42): la primera frase de 30 s, con las cuentas, la escribe el código; el Sintetizador
    # escribe las siguientes, sin marcadores numéricos
    # T-113 (H-50 de T-110): el esquema admite de una a tres frases. Las de más se descartan y lo que falta toma su texto por
    # defecto, y se declara (antes, una o tres frases rechazaban la respuesta entera sin decirlo)
    escritas = [t for t in (red.get("frases_30s") or []) if isinstance(t, str)]
    huecos = len(defecto["frases_30s"]) - 1
    if len(escritas) != huecos:
        quitadas.append("FORMATO")
    escritas = (escritas + [""] * huecos)[:huecos]
    propias = [_uno(t, defecto["frases_30s"][i + 1]) if t.strip() else defecto["frases_30s"][i + 1] for i, t in enumerate(escritas)]
    red["frases_30s"] = [defecto["frases_30s"][0]] + [x for x in propias if x.strip()]
    def_tarj = {x["opp_id"]: x for x in defecto["tarjetas"]}
    for x in red.get("tarjetas") or []:
        base = def_tarj.get(x.get("opp_id"), {})
        for k in ("por_que_llano", "que_puede_salir_mal_llano", "ambito_llano"):
            if isinstance(x.get(k), str):
                x[k] = _uno(x[k], base.get(k, ""))
    # r06 (H-42): las cuentas del motivo (ideas analizadas y las que pasaron) las escribe el código delante del texto
    # T-113 (H-49 de T-110): solo para los tipos del paquete; una clave que no lo es se quita y se declara
    clases_paquete = set(paquete.get("clases") or {})
    ajenas = [k for k in (red.get("motivos_llanos") or {}) if k not in clases_paquete]
    quitadas.extend("FORMATO" for _ in ajenas)
    red["motivos_llanos"] = {k: f"{_cuenta_motivo(paquete, k)} {v2}".strip() for k, v in (red.get("motivos_llanos") or {}).items()
                             if k in clases_paquete and isinstance(v, str) and (v2 := _uno(v, "").strip())}
    glosario = []
    for g in red.get("glosario") or []:
        if not isinstance(g, dict):
            continue
        if not isinstance(g.get("termino"), str) or not isinstance(g.get("definicion"), str):
            quitadas.append("FORMATO")   # r04 (H-24): una entrada que no es texto se quita, no rompe el ciclo
            continue
        g = {**g, "termino": unicodedata.normalize("NFKC", g["termino"]), "definicion": unicodedata.normalize("NFKC", g["definicion"])}
        r = frase_prohibida(g["termino"], perm, marcas) or texto_prohibido(g["definicion"], perm, marcas)
        if r:   # T-102 r02 (H-05): la entrada quitada se cuenta y se declara
            quitadas.append(r)
        else:
            glosario.append({**g, "termino": rellenar(str(g.get("termino", "")), marcas),
                             "definicion": rellenar(g["definicion"], marcas) if isinstance(g.get("definicion"), str) else g.get("definicion")})
    red["glosario"] = glosario
    red["frase_historial"] = _uno(red.get("frase_historial"), defecto["frase_historial"])
    # T-102 r02 (H-06): se declara lo de la redacción que se entrega; la de una respuesta anterior (reescritura) se retira
    previa = "Frases llanas del Sintetizador quitadas"
    paquete["limitaciones"] = [x for x in paquete["limitaciones"] if not x.startswith(previa)]
    if quitadas:
        paquete["limitaciones"] = [x for x in paquete["limitaciones"] if not x.startswith("Ninguna limitación")] + [
            f"{previa} ({', '.join(sorted(set(quitadas)))}): {len(quitadas)}; el resto de sus textos se conserva"]
    elif not paquete["limitaciones"]:
        paquete["limitaciones"] = ["Ninguna limitación adicional a las declaradas por opción"]
    return red


def sintetizar(bloque, paquete, extras, as_of, run_id, presupuesto, estado_run) -> tuple[dict, dict, dict]:
    """El Sintetizador (AG-26) en una llamada sobre el paquete validado por G3; después, la generación determinista de los
    entregables con su segunda pasada de HT-09 (esquema JSON, coherencia y legibilidad). Si el índice de legibilidad no
    llega, una reescritura, como con el Redactor."""
    msg = {"paquete_sintesis": sint.mensaje_redactor(paquete), "clusteres": [c["cluster_id"] for c in paquete.get("clusteres_exposicion", [])],
           "regimenes": paquete.get("regimen_macro"), "cambios_vs_anterior": paquete.get("x_cambios_vs_anterior")}
    bloque.mensajeria.crear("CT-15", "AG-02", "AG-26", {"paquete_sintesis": msg["paquete_sintesis"]}, run_id=run_id,
                            presupuesto={"uc": presupuesto.asignado.get("COMUN")})
    perm = permitidos_r21(bloque)
    # r04 (QA r03, H-25): el Sintetizador recibe la lista de siglas que puede usar; cualquier otra quita la frase
    # r05 (QA r04, H-39): no se ofrecen siglas con cifras («G7», «G20»): la regla CIFRA las quitaría siempre
    instr = INSTR_SINTESIS + " Siglas que puedes usar: " + ", ".join(sorted(c for c in perm["codigos"] if not _hay_cifra(c))) + "."
    r = bloque._invocar("AG-26", "CT-15", msg, "SINTESIS", instr, as_of, run_id, None, "redaccion", presupuesto, bolsa="COMUN")
    d = r.datos if r and r.datos else None
    lim = op(bloque, "sintetizador_limites")
    if d:
        _aplicar_integracion(paquete, d, lim, perm)
    red = _redaccion_segura(bloque, paquete, d, perm)
    entreg, g3b = bloque.redaccion.generar(bloque, paquete, extras, red, as_of, run_id, estado_run)
    if g3b["dictamen"] == "BLOQUEADO" and any(c == "C12" for c in g3b.get("bloqueos", [])):
        msg2 = {**msg, "reescritura": {"fernandez_huerta": g3b.get("legibilidad"), "frases_largas": g3b.get("frases_largas", [])}}
        r2 = bloque._invocar("AG-26", "CT-15", msg2, "SINTESIS", instr + " Reescribe: el índice no alcanza 70.", as_of, run_id,
                             None, "redaccion", presupuesto, bolsa="COMUN")
        if r2 and r2.datos:
            red = _redaccion_segura(bloque, paquete, r2.datos, perm)
            entreg, g3b = bloque.redaccion.generar(bloque, paquete, extras, red, as_of, run_id, estado_run)
    return entreg, g3b, red


# ======================================================================================================
# Registro de cobertura del embudo y muestra de descartes (A-05, ideas 3 y 4)
# ======================================================================================================
def _precio(bloque, simbolo, fecha) -> float | None:
    try:
        return float(bloque.proveedor.valor_en(simbolo, fecha)[1])
    except (DatosNoDisponibles, FugaDeInformacion, KeyError, TypeError, ValueError, IndexError):
        return None


def registrar_cobertura(bloque, run_id, as_of, clases, analisis, seleccion, info_prosp, info_critica) -> dict:
    """Una entrada COB- en HA por run: para cada tipo, hasta dónde llegó cada candidata y por qué se quedó; y la muestra de
    descartes con su precio en la fecha de corte, para el seguimiento contrafactual."""
    if not activo(bloque, "cobertura.registrar"):
        return {}
    n_muestra = int(op(bloque, "cobertura.muestra_descartes"))
    omitidas = set((info_prosp or {}).get("omitidos", []))
    sin_critica = {(x["clase"], x["proxy"]) for x in (info_critica or {}).get("sin_critica", [])}
    sin_respuesta = set((info_critica or {}).get("sin_respuesta", []))
    por_clase = {}
    for c in clases:
        an, s = analisis[c], seleccion[c]
        top = _top3(s)
        ev = {e["opp_id"]: e for e in s["evaluadas"]}
        filas = []
        for d in (an.get("gc1") or {}).get("descartes", []):
            filas.append({"simbolo": d["simbolo"], "fase": "GC1", "motivo": d["motivo"]})
        for f in an["finalistas"]:
            if not f.get("_gc2"):
                fase, motivo = "GC2", "E provisional, mecanismo o datos insuficientes"
            elif not f.get("_gc3"):
                fase, motivo = "GC3", "fuera de las finalistas con más RK"
            elif _ref(c, f) in omitidas:
                fase, motivo = "PROSPECTIVA", "sin pronóstico: omitido por Prospectiva dos veces (declarado, no negativo)"
            elif _ref(c, f) in sin_respuesta:   # QA r01 de T-101, H-03
                fase, motivo = "CRITICA", "el Contradictor no la devolvió en dos intentos: no se entrega (A-01)"
            elif (c, f["proxy"]) in sin_critica:
                fase, motivo = "CRITICA", "sin crítica del Contradictor: no se entrega (A-01)"
            elif f.get("opp_id") in top:
                fase, motivo = "SELECCION_FINAL", "en el top-3"
            elif f.get("_sin_critica"):
                fase, motivo = "SELECCION", "no llegó a un top-3 mientras había crítica disponible: no criticada y no elegible"
            else:
                e = ev.get(f.get("opp_id")) or {}
                mot = "; ".join(m.get("codigo", "") for m in e.get("motivos_no_elegible", [])) if not e.get("elegible", True) else "RK menor que las elegidas"
                fase, motivo = "SELECCION", mot or "no elegida"
            filas.append({"simbolo": f["proxy"], "opp_id": f.get("opp_id"), "fase": fase, "motivo": motivo,
                          "criticada": bool(f.get("_criticada")), "exploracion": f["proxy"] in set((an.get("gc1") or {}).get("exploracion", []))})
        # QA r01 de T-101, H-01: también lo que el Analista recibió y no propuso, y las vigentes (mantenidas o cerradas)
        g = an.get("gc1") or {}
        finalistas = {f["proxy"] for f in an["finalistas"]}
        motivos_an = {str(d.get("nombre")): d.get("motivo") for d in an.get("descartadas", []) if isinstance(d, dict)}
        en_top = {x.get("proxy") for x in s["candidatos"] if x.get("opp_id") in top}
        vigentes_sim = set(g.get("vigentes", [])) | {x.get("proxy") for x in s["candidatos"] if x.get("_vigente") or x.get("_arrastre")}
        for sim in sorted(set(g.get("pasan", [])) | set(g.get("exploracion", [])) | set(g.get("sin_senal_medible", []))):
            # QA r02, H-14: una vigente que sigue en el top-3 tiene su fila de selección, no la de «no propuesta»
            if sim not in finalistas and sim not in en_top and sim not in vigentes_sim:
                filas.append({"simbolo": sim, "fase": "ANALISTA", "exploracion": sim in set(g.get("exploracion", [])),
                              "motivo": f"el Analista no la propuso como finalista ({motivos_an.get(sim) or 'sin motivo declarado'})"})
        por_opp = {f.get("opp_id") for f in an["finalistas"]}
        for x in s["candidatos"]:
            if x.get("opp_id") in top and x.get("opp_id") not in por_opp:
                filas.append({"simbolo": x.get("proxy"), "opp_id": x["opp_id"], "fase": "SELECCION_FINAL", "vigente": True,
                              "criticada": bool(x.get("_criticada")), "motivo": "vigente mantenida en el top-3 (arrastre verificado)"})
        for x in s.get("cerradas", []):
            filas.append({"opp_id": x["opp_id"], "simbolo": None, "fase": "CIERRE", "vigente": True,
                          "motivo": f"vigente cerrada: {x.get('motivo_cierre')} ({x.get('comentario')})"})
        # QA r02, H-13: la rotación exploratoria de un ciclo ligero (N1) y lo que el Analista propone de ella (alta en F3)
        expl_f3 = {(f.get("indicador_seguimiento") or {}).get("simbolo") for f in an.get("exploratorias", [])}
        for sim in an.get("rotacion", []):
            if sim in expl_f3:
                filas.append({"simbolo": sim, "fase": "EXPLORATORIA_F3", "exploracion": True,
                              "motivo": "rotación exploratoria del ciclo ligero: el Analista la propone y queda en F3 como CANDIDATA"})
            elif sim not in en_top:
                filas.append({"simbolo": sim, "fase": "ROTACION", "exploracion": True,
                              "motivo": "rotación exploratoria del ciclo ligero: el Analista no la propone"})
        descartes = [x for x in filas if x["fase"] not in ("SELECCION_FINAL", "CIERRE", "EXPLORATORIA_F3") and x.get("simbolo")
                     and x["simbolo"] not in en_top]
        muestra = sorted(descartes, key=lambda x: _sembrado(run_id, c, x["simbolo"]))[:n_muestra]
        fecha = str(pd.Timestamp(as_of).date())
        # QA r02, H-15: también las vigentes arrastradas, con su símbolo y su precio
        elegidas = [{"opp_id": x["opp_id"], "simbolo": x.get("proxy"), "precio": _precio(bloque, x.get("proxy"), as_of) if x.get("proxy") else None}
                    for x in s["candidatos"] if x.get("opp_id") in top]
        por_clase[c] = {"filas": filas, "gc1": {k: v for k, v in (an.get("gc1") or {}).items() if k != "descartes"},
                        "muestra_descartes": [{"simbolo": x["simbolo"], "fase": x["fase"], "precio": _precio(bloque, x["simbolo"], as_of)}
                                              for x in muestra],
                        "elegidas": elegidas, "fecha": fecha}
    entrada = {"tipo_entrada": "COBERTURA", "id": bloque.almacen.nuevo_id("COB"), "run_id": run_id, "fecha": str(pd.Timestamp(as_of).date()),
               "horizonte_contrafactual": op(bloque, "cobertura.horizonte_contrafactual"),
               "prospectiva": info_prosp or {}, "critica": info_critica or {}, "clases": por_clase}
    bloque.almacen.escribir("HA", "AG-18", entrada)
    return entrada


def _fecha_vencimiento(bloque, fecha, horizonte) -> pd.Timestamp:
    from .herramientas.ht05_planificador import fecha_resolucion
    return pd.Timestamp(fecha_resolucion(pd.Timestamp(fecha), horizonte, parametro(bloque.cfg, "horizontes")))


def resolver_contrafactual(bloque, as_of, run_id) -> list[dict]:
    """Idea 4: cuando vence el horizonte de una muestra de descartes, compara, sin IA y con los datos de HT-01 hasta la fecha
    de hoy, la rentabilidad de los descartes muestreados con la de las opciones elegidas del mismo tipo y fecha. Escribe una
    entrada CTF- por cobertura resuelta (una sola vez)."""
    hechas = {e.get("cobertura_id") for e in bloque.almacen.leer("HA") if e.get("tipo_entrada") == "CONTRAFACTUAL"}
    out = []
    hoy = pd.Timestamp(as_of)
    for e in bloque.almacen.leer("HA", as_of):
        if e.get("tipo_entrada") != "COBERTURA" or e["id"] in hechas:
            continue
        try:
            vence = _fecha_vencimiento(bloque, e["fecha"], e["horizonte_contrafactual"])
        except (KeyError, TypeError, ValueError):   # horizonte o fecha ilegibles: no se resuelve (falla cerrado)
            continue
        if vence > hoy:
            continue
        clases: dict[str, dict[str, Any]] = {}
        for c, d in e["clases"].items():
            def _rent(x, vence=vence):
                if not x.get("simbolo") or not x.get("precio"):
                    return None
                p1 = _precio(bloque, x["simbolo"], vence)
                return None if p1 is None else round(p1 / x["precio"] - 1, 6)
            items = list(d.get("muestra_descartes", [])) + list(d.get("elegidas", []))
            rd = [r for r in (_rent(x) for x in d.get("muestra_descartes", [])) if r is not None]
            re_ = [r for r in (_rent(x) for x in d.get("elegidas", [])) if r is not None]
            media_e = sum(re_) / len(re_) if re_ else None
            medibles = sum(1 for x in items if x.get("simbolo") and x.get("precio"))
            clases[c] = {"descartes": len(rd), "elegidas": len(re_), "sin_precio": medibles - len(rd) - len(re_),
                         "rent_media_descartes": round(sum(rd) / len(rd), 6) if rd else None,
                         "rent_media_elegidas": round(media_e, 6) if media_e is not None else None,
                         "descartes_que_superan": sum(1 for r in rd if media_e is not None and r > media_e),
                         # QA r02, H-20: cada tipo dice si se pudo medir
                         "estado": "RESUELTO" if rd or re_ else ("SIN_DATOS" if medibles else "SIN_MUESTRA")}
        # QA r01 de T-101, H-10: si al vencer no hay ningún precio de lo que se podía medir, se espera al ciclo siguiente
        # (sin datos no hay conclusión); con datos parciales se resuelve y se cuenta lo que faltó (`sin_precio`)
        estado = "RESUELTO"
        if any(v["sin_precio"] for v in clases.values()) and not any(v["descartes"] + v["elegidas"] for v in clases.values()):
            # QA r02, H-20: se espera como mucho `dias_max_espera_precio` días; después se cierra como NO_RESOLUBLE
            if hoy <= vence + pd.Timedelta(days=int(op(bloque, "cobertura.dias_max_espera_precio"))):
                continue
            estado = "NO_RESOLUBLE"
        ctf = {"tipo_entrada": "CONTRAFACTUAL", "id": bloque.almacen.nuevo_id("CTF"), "run_id": run_id, "cobertura_id": e["id"],
               "fecha_muestra": e["fecha"], "fecha_resolucion": str(vence.date()), "estado": estado, "clases": clases}
        bloque.almacen.escribir("HA", "AG-18", ctf)
        out.append(ctf)
    return out


def auditar_este_run(bloque, run_id: str) -> bool:
    """Auditor por muestreo sembrado (V6): audita la fracción `v6.auditoria_fraccion` de los runs."""
    h = int(hashlib.sha256(run_id.encode()).hexdigest(), 16) % 10000
    return h < int(10000 * float(op(bloque, "auditoria_fraccion")))


def limitaciones_diseno(bloque) -> list[str]:
    """Lo que la V6 declara de sí misma en cada informe."""
    out = []
    if bloque.v6 and op(bloque, "contradictor.proveedor") == "otro" and "AG-11" not in bloque.agentes.clientes:
        out.append("Contradictor del mismo proveedor de IA: el segundo proveedor no está configurado (decisión 2 de la tanda 1); "
                   "la independencia del contraste es menor de la prevista")
    elif bloque.v6 and "AG-11" not in bloque.agentes.clientes:
        out.append("Contradictor del mismo proveedor de IA que el resto del bloque (segundo proveedor aún sin contratar)")
    if bloque.v6 and not op(bloque, "curacion_llm"):
        out.append("Curación determinista: independencia de las raíces por fuente declarada, sin evaluación semántica (la revisa "
                   "el Auditor por muestreo)")
    return out

